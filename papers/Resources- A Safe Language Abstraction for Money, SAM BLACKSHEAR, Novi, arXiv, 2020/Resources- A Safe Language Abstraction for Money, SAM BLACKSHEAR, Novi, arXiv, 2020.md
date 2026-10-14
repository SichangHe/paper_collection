                                         Resources: A Safe Language Abstraction for Money

                                         SAM BLACKSHEAR, Novi
                                         DAVID L. DILL, Novi
                                         SHAZ QADEER, Novi
arXiv:2004.05106v2 [cs.PL] 23 Jul 2020




                                         CLARK W. BARRETT, Stanford University
                                         JOHN C. MITCHELL, Stanford University
                                         ODED PADON, Stanford University
                                         YONI ZOHAR, Stanford University
                                         Smart contracts are programs that implement potentially sophisticated transactions on modern blockchain
                                         platforms. In the rapidly evolving blockchain environment, smart contract programming languages must allow
                                         users to write expressive programs that manage and transfer assets, yet provide strong protection against
                                         sophisticated attacks. Addressing this need, we present flexible and reliable abstractions for programming
                                         with digital currency in the Move language [Blackshear et al. 2019]. Move uses novel linear [Girard 1987]
                                         resource types with semantics drawing on C++11 [Stroustrup 2013] and Rust [Matsakis and Klock 2014]: when
                                         a resource value is assigned to a new memory location, the location previously holding it must be invalidated.
                                         In addition, a resource type can only be created or destroyed by procedures inside its declaring module. We
                                         present an executable bytecode language with resources and prove that it enjoys resource safety, a conservation
                                         property for program values that is analogous to conservation of mass in the physical world.



                                         1   INTRODUCTION
                                         The emergence of Bitcoin [Nakamoto 2008] and Ethereum [Wood 2014] has created significant
                                         interest in the computational model of a replicated state machine synchronized by a distributed
                                         consensus protocol. In this programming model, a command is executed as an atomic and determin-
                                         istic transaction that is replicated consistently across all nodes participating in consensus. While
                                         cryptocurrency and decentralized finance are the most prominent applications of programmable
                                         blockchains, there are other important use-cases such as tracking supply chains [Casey and Wong
                                         2017] and clearing global markets [Armstrong 2019].
                                            Transactions are programmed as smart contracts, a catchy name [Szabo 1997] for program units
                                         installed for atomic execution on the blockchain. If the contract language is sufficently expressive,
                                         then smart contracts are attractive implementaions for a wide variety of conventional functions such
                                         as bank deposit and withdrawal, cross-border funds transfer, point-of-sale online payment, escrow
                                         agreements, futures contracts, and derivatives. To meet these goals, a smart-contract programming
                                         language must allow users to write programs that manage and transfer assets while providing
                                         extremely trustworthy protection against sophisticated attacks.
                                            In this paper, we describe and analyze flexible and reliable abstractions for programming with
                                         digital currency and other assets in the Move language [Blackshear et al. 2019]. Move uses novel
                                         linear [Girard 1987] resource types that draw on experience with C++11 [Stroustrup 2013] and
                                         Rust [Matsakis and Klock 2014] to preserve integrity and prevent copying of assets. When combined
                                         with other abstraction features of Move, linearity ensures resource conservation. Whereas data
                                         abstraction ensures that a resource may only be created and destroyed by the defining module,
                                         linearity further prevents duplication and unintended loss. We present an executable Move bytecode
                                         language with move semantics and show that it satisfies a set of resource safety guarantees.

                                            Contributions. This paper adds rigor to the informal description of Move [Blackshear et al. 2019].
                                         Its key contributions are:

                                                                                               1
,,         Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar


      • We introduce resources, an intuitive abstraction for currency-like values, and demonstrate
        their utility compared to existing language constructs (Section 2).
      • We explain the key features of the Move bytecode language and explain how their design
        supports support resource-oriented programming (Section 3)
      • We formalize the semantics of the Move bytecode interpreter for the subset of Move analyzed
        in this paper (Section 4).
      • We formally define resource safety properties and prove that execution of Move bytecode
        programs is resource-safe (Section 5).
      • We describe our implementation of the Move virtual machine, its integration in the Libra
        blockchain [Amsden et al. 2019], and the adoption of Move in other contexts (Section 6).

2     PROGRAMMING WITH MONEY
Move is designed to support a rich variety of economic and financial activities by supporting
fundamental conservation properties, not only for built-in currencies, but also for programmer-
defined assets. We believe this is essential. To begin with, smart contracts provide customizable logic
for sending, receiving, storing, and apportioning digital funds that cannot be arbitrarily created,
lost, or destroyed. Further, the internal balance in a bank account, the monetary value inherent in a
contract for future payment, or an escrow contract all represent assets that must be conserved in
the same ways as conventional currency. Thus, smart contracts must be able to implement new
assets with expected conservation properties and appropriately control the exchange of one asset
for another.

2.1     Savings Bank Example
With this goal in mind, we use a simple bank account contract to illustrate the key features of
Move for programming with assets and demonstrate by example the advantages of Move over two
alternative contract programming languages where notable problems have occurred in practice.
Figure 1 implements a savings bank with the following requirements:
      • A customer should be able to deposit money worth N via the deposit procedure and subse-
        quently extract money worth N via the withdraw procedure.
      • No customer should be able to withdraw money deposited by another customer.
   Even in this simplest of examples, there are already two assets: the funds deposited into the
bank contract, and the bank credit that the customer can use to withdraw the funds in the future.
Most smart contract platforms have a native asset such as Ether in Ethereum [Wood 2014] that is
implemented as part of the core platform and guarantees conservation. But even if the deposited
funds are represented using the native asset, the bank contract must correctly implement deposit
and withdraw to ensure conservation for the bank credit asset. Programming mistakes in this
setting can be extremely costly;high-profile bugs in Ethereum, e.g., [Atzei et al. 2017; Buterin 2016;
Palladino 2017], have resulted in the theft of digital assets worth tens of millions of dollars. To
summarize, programming challenges in this environment include:
     (1) Conservation. Transfers must preserve the total supply of money in the system, including
         custom assets defined by contracts.
     (2) Unique atomic transfer. The sender of an asset must relinquish all control of the asset.
         This ownership transfer should be atomic because any non-atomic exchange risks leaving
         one or both parties empty-handed.
     (3) Authority. Smart contract programmers must represent authority carefully and restrict
         access to privileged operations. Contracts are deployed on a public platform open to both
         benign customers and bad actors.

                                                         2
Resources: A Safe Language Abstraction for Money                                                                   ,,


                                       contract Bank
                                       field credit: Map Address Uint;   module Bank
                                                                         use 0x0::Coin;
                                       transition deposit()              resource T { balance: Coin::T }
                                         accept;                         resource Credit { amt: u64, bank: address }
                                         match credit[_sender] with
  contract Bank                          Some(amt) =>                    fun deposit(
  mapping (address => uint) credit;        credit[_sender] :=              coin: Coin::T,
                                             amt + _amount                 bank: address
  function deposit() payable {           None =>                         ): Credit {
    amt =                                  credit[_sender] := _amount      let amt = Coin::value(&coin);
      credit[msg.sender] + msg.value     end                               let t = borrow_global<T>(copy bank);
    credit[msg.sender] = amt           end                                 Coin::deposit(&mut t.balance, move coin);
  }                                                                        return Credit {
                                       transition withdraw()                 amt: move amt, bank: move bank
  function withdraw() {                  match credit[_sender] with        };
    uint amt = credit[msg.sender];       Some(amt) =>                    }
    msg.sender.transfer(amt);              msg = {
    credit[msg.sender] = 0;                  _recipient: _sender;        fun withdraw(credit: Credit): Coin::T {
  }                                          _amount: amt                  Credit { amt, bank } = move credit;
                                           };                              let t = borrow_global<T>(move bank);
                                           credit[_sender] := 0;           return Coin::withdraw(
                                           send msg                          &mut t.balance, move amt
                                         None => ()                        );
                                         end                             }
                                       end


Fig. 1. A simple bank contract in Solidity (left), Scilla (middle), and Move (right). Each code snippet must
implement bidirectional exchanges of the language’s native currency for a bank credit currency defined by
the contract. In Solidity and Scilla, both native and custom currencies are represented indirectly via maps of
identities to integers, whereas in Move, currency is represented directly with resources.



   Move represents money using user-defined linear resource types. Move has ordinary types like
integers and addresses that can be copied, but resources can only be moved. Linearity prevents
“double spending” by moving a resource twice (e.g., into two different callees) and forces a well-typed
procedure to move all of its resources, avoiding accidental loss.
   Figure 1 provides a Move representation of the simple bank along with an implementation
in Solidity [Foundation 2018a] and Scilla [Sergey et al. 2019]. Solidity is a source language for
Ethereum [Wood 2014] and the first to provide an expressive smart contract programming model.
Scilla is a newer language designed by programming language researchers to simplify formal
verification of contracts and incorporate lessons learned from Solidity design flaws. Although
many other contract languages have been proposed (see Section 7), these two represent the state of
practice (Solidity) and the state of the art (Scilla).
   Solidity, Scilla and other account-based languages often use a model in which each contract has
an implicit balance in the platform’s native currency. This balance can only be modified by special
instructions. However, the properties ensured by these special instructions are not available to
programmers that wish to implement custom currencies such as bank credits. A common strategy
used instead is illustrated in Figure 1: a map, credit, is employed to map creditor identities to
integers. The integers in the range of the map represent money and must be manipulated carefully
to provide the global conservation invariants associated with monetary assets. However, as we
will see by examining the code samples, properties guaranteed by construction in Move are more
difficult to ensure via ad hoc programming in other languages. Although the bank is a somewhat
artificial example, it is adapted from similar examples in the Solidity/Scilla documentation and
concisely captures the key idioms of typical contracts: sending/receiving/atomically exchanging
money and implementing a new money-like construct.

                                                         3
,,        Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar


   Solidity and Scilla deposit. The first task of the deposit procedure in Figure 1 is to accept the
language’s native currency. In Solidity, native currency sent by a caller is implicitly deposited into
the contract’s balance before the callee code is executed, provided the receiving function is marked
as payable. If not, an attempted deposit causes a runtime failure that reverts all changes performed
by the current transaction.
   In Scilla, money is transferred from caller to callee via an explicit accept construct which avoids
runtime failures but introduces other problems. Although money not accepted by the callee will be
silently returned, bugs may occur if the programmer forgets to accept funds. For example, accepting
on one control-flow path but not another (e.g., only in the None branch) would allow the caller to
steal funds deposited by another user by subsequently invoking Withdraw.
   The second task of deposit is to update the caller’s bank credits by the transferred amount. In
both languages, the amount sent by the caller is available through special integer-typed expressions:
msg.value in Solidity and _amount in Scilla. The identity of the caller is represented by msg.sender
or _sender, respectively. The programmer must be careful to increment the caller’s credit balance
by the transferred quantity exactly once. Forgetting to update the balance is stealing funds from the
caller, whereas updating more than once allows the caller to steal funds from other customers. There
are no special checks on integer expressions to prevent either programmer error from violating
conservation of funds.
   Solidity and Scilla withdrawal. The withdraw procedure exchanges bank credits for native cur-
rency. Although this is logically the inverse of deposit, the implementation looks quite different.
This is because Solidity and Scilla do not have language support for returning native or custom
currency to the calling procedure. Instead, the code uses language primitives for sending currency
to the address that stores the contract whose procedure invoked withdraw.
   In Solidity, the relevant primitive is msg.sender.transfer. Subtly, this is a virtual call that invokes
a user-defined procedure known as a fallback function in the callee. The decision to make every
payment of native currency a virtual call has led to infamous re-entrancy vulnerabilities such as
the DAO [Buterin 2016] attack that led to theft of digital assets worth over $60 million. The key
issues are that (a) the update to the credit map via credit[msg.sender] = 0 and the sending of funds
via transfer are not atomic, and (b) the map update occurs after the virtual transfer call. If the
virtual call invokes a user-defined function that calls back into withdraw, the caller can steal funds
deposited by a different customer.
   Scilla improves on Solidity by defining a more restricted message-passing primitive for sending
money to addresses. The _amount: amt code snippet implicitly withdraws amt units of money from
the contract’s available balance. Then, the _sender’s balance in the credit map is zeroed out before
using the send primitive to transfer the money to its recipient. Scilla’s type system forces any global
side effect like a message send to occur at the end of the procedure; for our example, it would not
allow the update to credit to occur after the send. In addition, Scilla does not have virtual calls.
These restrictions prevent re-entrancy issues.
   However, the Scilla design introduces a new kind of issue: using emit msg instead of send msg
in the example would cause the money in the message to be destroyed. The emit construct emits the
message as a client-facing event rather than sending it to an address. This mistake permanently
reduces the supply of money in the system. Scilla programmers have encountered this problem in
practice ([Sergey et al. 2019], Section 5.2), though Scilla has an auxiliary “cashflow” static analyzer
for detecting problems like this.
  Move Bank. The Move implementations of the deposit and withdraw procedures are symmetric.
The deposit procedure says that it requires payment by declaring a parameter of type Coin::T and
that it intends to credit the caller by declaring a return value of type Bank::Credit. The withdraw

                                                        4
Resources: A Safe Language Abstraction for Money                                                  ,,


procedure does the inverse. Coin::T represents native currency; it is a resource type defined in
a separate Coin module that we describe in Section 6.2. Since both Coin::T and Bank::Credit are
resources, the type system will reject any implementation that fails to consume the input resource
or return ownership of the output resource. Both resources can leverage the same language feature
(move semantics) for atomic ownership transfer into and out of the procedure.
   The deposit code consumes its input resource by acquiring a reference to a Bank::T value
published in global storage and moving the coin resource into the bank’s balance via the call to
Coin::deposit. It then packs (constructs) a Credit resource and returns it to the caller.
   The withdraw code consumes its input Credit resource by unpacking it. Unpacking destroys a
resource and returns its contents. Only the Bank module can pack, unpack, and acquire references
to the fields of the Credit resource; code outside the module can only access Credit through the
procedures exposed by Bank. Finally, withdraw extracts native currency from the bank’s balance via
Coin::withdraw and returns it to the caller.

  Resources as Capabilities. We conclude our discussion of the Move bank by noting that the
advantage of an explicit type for money goes beyond safety: resources enable flexible programming
patterns that would not be possible with an implicit representation of money. For example: say
that Alice is a customer of the Bank and wants to give another user Bob permission to withdraw
the funds she has deposited. Alice can simply transfer ownership of her Bank::Credit to Bob, who
can use it to invoke withdraw at his leisure—no change to the Bank code is required. Bob could also
choose to store his Bank::Credit in another resource that (e.g.) allows multiple parties to access it
or prevents it from being redeemed until a certain time.
  By contrast, the Solidity and Scilla implementations of the Bank cannot support this feature
without modifying the original contract to support it. In essence, the credit map approach im-
plements an access control list for withdrawing native currency, whereas the resource approach
implements a linear capability for withdrawals [Hardy 1994; Miller et al. 2003; Swasey et al. 2017].
Capability-based programming enables some powerful design patterns, as we will see in Section 6.2.

3     MOVE OVERVIEW
This section provides an informal overview of the key concepts and design decisions of the Move
language that support safe and expressive programming with resources.

3.1    Executable Bytecode With Resources
The Move execution platform relies on a compiler to transform source language programs into
programs in the Move bytecode language. For example, Figure 1 contains Move source code that
compiles to an executable bytecode representation (see Figure 2 for an example). Bytecode – not
source code – is stored and executed on the Libra blockchain.
   Because Move programs are deployed in the open alongside other (potentially untrusted) Move
programs, it is important for key properties like resource safety to hold for all Move bytecode
programs. If the safety guarantees were only enforced by the source language compiler, an adversary
could subvert them by writing malicious bytecode directly and entering it into the execution
environment without using a compiler. Thus, we focus on the design and semantic properties of
the Move bytecode language here, although we write illustrative examples in the source language
for readability.
   The Move execution platform relies on a load-time bytecode verifier, in a manner similar to the
Java Virtual Machine [Lindholm and Yellin 1997] and Common Language Runtime [Meijer et al.
2000]. The bytecode verifier enforces type, memory, and resource safety. Because the goal of the
present paper is to explain and formalize properties of Move that provide key advantages over

                                                   5
,,            Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar



     Bytecode              Source code
     MvLoc ⟨x 0 ⟩          move credit
     Unpack ⟨s 1 ⟩         Credit {amt, bank}=...
     BorrowGlobal ⟨s 0 ⟩   borrow_global<T>(...)
     BorrowField ⟨f 0 ⟩    &mut t.balance
     Call ⟨h 0 ⟩           Coin::withdraw(...)
     Ret                   return



Fig. 2. Bytecode for the withdraw procedure from Figure 1 (left) and an example global state containing
resources from Figure 1 (right). The global state contains three account addresses with different combinations
of resources. Address 0x1 has a Coin resource with value 5 and a Credit with value 10 that can be redeemed
at the Bank resource owned by 0x2. Address 0x3 also has a Bank resource, but it holds a Coin with value 0.


prior smart contract languages (i.e. resource values with ironclad safety guarantees), we focus on
a concrete semantics for Move with dynamic checks for type, resource, and memory safety and
leave formalization of the bytecode verifier to future work. Our formalization and resource safety
theorem (Theorem 5.10) therefore do not depend on any of the invariants ensured by the bytecode
verifier; the presence of the verifier just allows an optimized implementation to skip these checks.
The analyses performed by the bytecode verifier are sufficiently interesting and complex to fill a
paper of their own (particularly reference safety, which has similarities to the Rust borrow checker;
see Section 7).
   Persistent Global State. Move execution occurs in the context of a persistent global state organized
as a partial map from account addresses to resource data values. Each address can store an arbitrary
number of resources, but at most one of any given type at the top level. For example, the account
address 0x in Figure 2 holds two Coin::T resources, but one is at the top level and one is stored
inside a Bank::T resource.
   In addition, an address can store zero or more code modules. The global state is updated via
transactions that contain a sender account address and a transaction script consisting of a single main
procedure. Transaction scripts update the global state by invoking procedures of published modules
that mutate stored resources, add new resources to an address, or remove existing resources from
an address. A transaction has all-or-nothing semantics; either the entire script is executed without
errors or it aborts and reverts all changes to the global state.
   Procedure Calls. Execution of a Move program begins by executing the distinguished main pro-
cedure of the transaction script and proceeds via the evaluation mechanics shown in Figure 3. A
procedure is defined by a type signature and an executable body comprising a linear sequence of
Move bytecode commands. Procedure calls are implemented using a standard call stack containing
frames with a procedure name, a set of local variables, and a return address. When one procedure
calls another, the calling procedure pushes its callee’s arguments onto the operand stack and
invokes the Call bytecode command, which pops the arguments off the stack and stores them in
the actuals of the callee (which become a subset of the callee’s local variables). Before returning,
the callee pushes its return values on the stack and invokes the Ret bytecode command, which
pops the current stack frame and returns control to the return address.
  Modules. A Move module such as our Bank from Figure 1 can declare both record types and
procedures. Records can store primitive data values (including booleans, unsigned integers, and
account addresses) as well as other record values, but not references. Each record is nominally
declared as a resource or non-resource. Non-resource records cannot store resource records, and
only resources can be stored in the global state.

                                                            6
Resources: A Safe Language Abstraction for Money                                                            ,,


                                        Ret
                      Localsi+1
                                     Call
                                  MvLoc CpLoc                    MoveTo
                                    BorrowLoc Operand               Global
                       Localsi
                                               stack   MoveFrom    resources
                                      StLoc           BorrowGlobal
                          ...


Fig. 3. Execution mechanics of the Move bytecode interpreter. The global state holds resources that can be
moved onto the operand stack or borrowed by pushing a reference onto the stack. Resources can be published
to the global state by moving them from the stack into an account address. Each call stack frame (blue) has
its own local variables to store values popped off the stack. Formal parameters and return values are passed
between caller and callee using the shared operand stack.

     local variable instructions      MvLoc ⟨x⟩ | CpLoc ⟨c⟩ | StLoc ⟨x⟩ | BorrowLoc ⟨x⟩
     reference instructions           ReadRef | WriteRef | FreezeRef
     record instructions              Pack | Unpack | BorrowField ⟨f ⟩
     global state instructions        MoveTo ⟨s⟩ | MoveFrom ⟨s⟩ | BorrowGlobal ⟨s⟩ | Exists ⟨s⟩
     stack instructions               Pop | LoadConst ⟨a⟩ | Op
     procedure instructions           Call ⟨h⟩ | Ret

Fig. 4. List of Move instructions. The local variable instructions move or copy values between local variables
and the operand stack. Reference instructions operate on reference values stored on the operand stack.
The global state instructions move values between the operand stack and persistent global storage. Stack
instructions manage the operand stack by popping unused values, pushing constants, and performing
arithmetic/bitwise operations via Op. Finally, the procedure instructions create and destroy call stack frames.


   Modules support strong encapsulation for their declared types. Consider the bytecode translation
of the withdraw procedure from our running example shown in Figure 2. The struct definitions si
and field definitions fi used by the bytecode instructions are implemented as integer indexes into
internal tables of the current module. This design ensures that privileged operations on the module’s
declared types can only be performed by procedures in the module, encapsulating creation via Pack,
destruction via Unpack, accessing fields via BorrowField, publishing via MoveTo, removing via
MoveFrom, and accessing (either to read or write) via BorrowGlobal. For example: the withdraw
bytecode is able to access a field of its declared T type, but it would not be able to access a field of
the Coin::T type except via the API exposed by the Coin module.
   A module may import a type or procedure declared in another module using its storing address
as a namespace. For example, the use 0x0::Coin line from our running example indicates that the
current module should link against the module named Coin stored at account address 0x0. The
combination of encapsulation and resource safety enables modules to safely interoperate while
maintaining strong internal invariants.
   References. Move supports references to records and primitive values (but not to other references).
In a manner similar to Rust, references are either exclusive/mutable (written &mut) or read-only
(written &). All reads and writes of record fields occur through a reference.

                                                      7
,,        Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar


 resource R {}                                               resource R {}
 fun copy_resource_bad(r: R) {                               fun double_move_bad(r: R): R {
   let x = copy r; // no; copies r                             let x = move r;
 }                                                             let y = move r; // no; r already moved
 fun deref_resource_bad(ref: &R): R {                          let z = move_from<R>(0x1);
   return *ref; // no; copies target of ref                    return move_from<R>(0x1); // no; 0x1.R moved
 }                                                           }



 resource R {}
 fun destroy_via_assign_bad(r1: R, r2: R) {
   let loc = move r1;
   loc = move r2; // no; destroys old value of loc
                                                             resource R {}
 }
                                                             fun double_move_to_bad(r1: R, r2: R)) {
 fun destroy_via_write_bad(ref: &mut R, r: R) {
                                                                move_to<R>(0x1, move r1);
   *ref = move r; // no; destroys target of ref
                                                                move_to<R>(0x1, move r2); // no; overwrites r1
 }
                                                             }
 fun unused_resource_local_bad(r: R) {
   let local = move r;
   return; // no; would destroy resource in local
 }


Fig. 5. Top: Examples of bad Move code that must be rejected due to resource duplication. Bottom: examples
of bad Move code that must be rejected due to destruction of resources. The programs on the left would all
be accepted if type R was declared as a struct instead of a resource, or if R was replaced with a primitive
type like u64.


   References are different from other Move values because they are transient: as explained above,
persistent global state consists of resource records, which cannot have fields of reference type. This
means that each reference must be created during the execution of a transaction script and released
before the end of that transaction script. Thus, each individual record value is a tree, and the global
state is a forest whose roots are account addresses.

3.2   Language Design for Resource Safety
At the beginning and end of a transaction script, all of the resources in the system reside in the
global state GS. Resource safety is a conservation property that relates the set of resources present
in state GS pr e before the script to the set of resources present in state GS post after the script. In
general terms, we would like the language to guarantee that:
   (1) A resource M::T that is present in post-state GS post was also present in pre-state GS pr e unless
        it is introduced by a Pack inside M during script execution
   (2) A resource M::T that was present in pre-state GS pr e is also present in post-state GS post unless
        it is eliminated by an Unpack inside M during script execution
   It is helpful to look at each of the instructions in Figure 4 and consider what precautions must
be taken in order to ensure that properties (1) and (2) hold. For property (1), we must be careful
not to introduce instructions that can duplicate a resource value. Move achieves this by providing
both MvLoc and CpLoc instructions for transferring a value from a local variable to the operand
stack. As the copy_resource_bad function in Figure 5 demonstrates, the CpLoc instruction cannot
be applied to a resource value. The MvLoc, MoveTo, and MoveFrom instructions for transferring
values prevent double moves that would allow a programmer to “spend” the same resource multiple
times (see double_move_bad).
   References must also be managed carefully to avoid duplication. The ReadRef for dereferencing
a reference value can only be applied to a non-resource reference. Allowing a dereference of a
resource like deref_resource_bad in Figure 5 would copy the resource value behind the reference.

                                                        8
Resources: A Safe Language Abstraction for Money                                                   ,,


   Property (2) is further challenging because conventional languages provide a number of ways
to indiscriminately discard values. At the instruction level, restrictions must be placed on Pop,
StLoc, WriteRef, and MoveTo. Most obviously, popping a resource off the operand stack with
Pop must be disallowed. If a local variable is of type resource, StLoc can only be applied when
the variable is uninitialized. Code like destroy_via_assign_bad in Figure 5 would violate property
(2) by discarding the old value stored in the local. Similarly, a WriteRef like *ref = move r in
destroy_via_write_bad must not execute if ref points to a resource. This destructive update would
destroy the value previously pointed to by ref. Finally, the MoveTo instruction for moving a
resource into global storage aborts if the move would overwrite an existing resource at the given
address. For example, double_move_to_bad would fail at runtime because the memory 0x1.R is
already occupied.
   Instruction-level protections are not quite enough to ensure property (2). There are two remaining
holes that could allow resource destruction: values left in local variables when a procedure returns
(e.g., unused_resource_local_bad in Figure 5), and values left on the operand stack at the end of
script execution. Move prevents both with extra discipline in the calling convention:
     • The values on the operand stack match the types of formal parameters/return values before
        a Call/Ret (respectively).
     • Ret cannot be invoked if a local variable holds a resource value or the operand stack holds
        extra (non-return) values.
     • A script terminates in a non-aborting state only when both the call stack and operand stack
        are empty.
   The reader might wonder: can resources left on the stack and in locals be destroyed by a mid-
script abort? This would be indeed be a problem in a conventional language, but the all-or-nothing
semantics of Move transactions saves us. An aborting transaction script evaluates to the pre-state
of the script, at which point all resources reside safely in global storage.
   What Resource Safety Accomplishes for Programmers. At this point, it’s worthwhile to take a
step back and briefly discuss what resource safety does and does not guarantee. For concreteness,
let’s consider our running example in Figure 1 once more. Resource safety would not preclude
an implementation of deposit whose first line was let amt = 7; that is, it cannot protect the
programmer from mistakes in implementing a custom asset. It does, however, isolate and localize
such decisions. For example, it prevents the Bank from violating the invariants established for the
imported Coin::T type inside its own declaring module.
   This observation suggests a clear division of responsibilities. It is the module author’s job to
define and correctly implement safety invariants for the types inside her module. Once she has
done so, encapsulaton and resource safety will ensure that her local invariants are also global
invariants—no possible client can ever violate them (similar to the “robust safety” of [Swasey et al.
2017]). This is quite powerful because Move modules give programmers an unusual amount of
control over declared types (e.g., restricting publishing and destroying types as described above),
and this control can be used to establish strong invariants. For example, it is possible to define a
type that can only be created after a certain time, a type that can never be destroyed, or a type that
can only be created by a caller that has paid ten coins. In Section 6.2, we will show how resource
safety allows us to establish global conservation of native currency in the Libra platform via a local
invariant of the Coin module.

4   MOVE BYTECODE INTERPRETER
Next, we present operational semantics for a call-free subset of the Move bytecode that simulates a
single transaction of arbitrary length. Generalizing to multiple transactions with procedure calls is

                                                   9
,,         Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar


                   locations                   L
                   primitive data values       P
                   addresses                   A⊆P
                   resource types              T
                   resource tags               R
                   tags                        T = R ⊎ {U}
                   field names                 F (finite)
                   paths                       F∗
                   values                      V (see Definition 4.1)
                   tagged values               TV (see Definition 4.1)
                   record values               V \P
                   memories                    M = L ⇀ TV
                   references                  Re f = L × F ∗ × {mut, immut}
                   stack values                SV = TV ∪ Re f
                   local values                LV = L ∪ Re f
                   local variables             V
                   local states                M × (V ⇀ LV ) × SV ∗
                   global resource ids         G =A×T
                   global states               GS = M × (G ⇀ L) × (V ⇀ LV ) × SV ∗
                   program locations           PC
                   program states              PC × GS

Fig. 6. Definitions for the semantics of Move. For a set X , X ∗ denotes the set of (finite) lists of elements from
X.



conceptually straightforward, but would be significantly less concise. This semantics will be used
in Section 5 to formalize and prove resource safety.
   As explained in Section 3.1, Move uses a bytecode verifier to ensure type safety and memory
safety of smart contracts. Our formalism here, focusing on resource safety, does not depend on the
bytecode verifier. Instead, our semantics gets stuck in errournous states, e.g. when encountering a
dangling reference or an ill-typed operation. The bytecode verifier ensures additional invariants (e.g.,
no dangling references, well-typedness) such that programs that pass the bytecode verifier cannot
get stuck due to memory or type errors. As a result, our resource safety theorem (Theorem 5.10)
does not depend on the bytecode verifier.
   We will begin with preliminary definitions and notation for values, types, memory, and persistent
global state, before introducing evaluation rules. The notation is summarized in Figure 6.

4.1   Definitions and Notation
   Notation for partial functions and lists. We use standard operations on partial functions (used to
represent record values or mappings in local and global states); operations on lists are similarly
standard and used in several ways.
   Following common convention, if f : A ⇀ B is a partial function from A to B, then dom(f ) is the
set of all a ∈ A for which f (a) is defined, and imд(f ) is the set of all b ∈ B for which f (a) = b for
some a ∈ A. We use f [a 7→ b] to denote the function that is equivalent to f on every input except
a and which maps a to b. Similarly, f \ a is the partial function equivalent to f except that it is
undefined at a.

                                                         10
Resources: A Safe Language Abstraction for Money                                                               ,,


     We use lists to represent a sequece of field accesses and in components of semantic states. We
write [] for the empty list and e :: l for the result of placing e at the front of list l. Similarly, l :: e is
the list with e appended to l and, by slight abuse of notation, l :: l ′ the concatenation of lists l and
l ′.
   Values and their types. We begin with primitive types, field names, and tags, using these three
elements to define the values used in computation. While tags are used to state and prove semantic
properties, tags are not needed in the Move virtual machine.
   Let P be the set of primitive data values, including Booleans, integers, and addresses, F a fixed,
finite set of field names and T the set of tags, where each tag may be a resource tag from a set R or
the distinguished element U indicating a value that is not a resource.
    Definition 4.1. The set V of values and the set TV of tagged values are defined together from the
primitive values, tags and field names as the least sets satisfying:
   (i) P ⊆ V ;
  (ii) for every v ∈ V and t ∈ T , ⟨v, t⟩ ∈ TV ; and
 (iii) if n ≥ 1, f 1 . . . fn ∈ F are pair-wise distinct, and tv 1 . . . tvn ∈ TV , then {(fi , tvi )|1 ≤ i ≤ n} ∈
       V.
The values arising from condition (iii) are non-empty partial functions from F to TV , which we
call record values. We use ordinary function notation when using them (e.g., when writing v(f ) to
refer to the value associated with field f in the record value v).
   Although types are not used extensively in this paper, we leverage the fact that typing distin-
guishes resource values from non-resource values. We write v : s to indicate that value v has a
type s. If T is the set of resource types, v : s, and s ∈ T , then we say that v is a resource value and
⟨v, t⟩ is a resource tagged value, or simply resource; otherwise, v is a non-resource value and ⟨v, t⟩ is
a non-resource tagged value. 1
    Paths and Trees. In the semantics, a path is a possibly empty list of field names, which we think
of as representing a sequence of field selections.
    A tagged value may be regarded as a labeled tree, in the usual way that expressions are parsed
as trees, with nodes labeled by tags and edges labeled by field names. Specifically, a primitive value
is a tree consisting of a leaf. The tree associated with a tagged record value consists of a node
labeled with the tag and a subtree for each record component. If r is a record value, then for each
(f , tv) ∈ r , there is an edge from r to the subtree for tv labeled by f .
    Two useful operations on values and paths are (i) the subterm tv[p] of tv located at path p, and
(ii) the term tv[p := tv ′] obtained by replacing the subterm at path p with term tv ′. The subterm
identified by following the empty path is the term itself, i.e. tv[[]] = tv. These operations are
formalized as follows.
  Definition 4.2. If tv = ⟨v, t⟩ ∈ TV , then tv[p] is defined inductively by:
  (1) tv[[]] = tv
  (2) tv[f :: p ′] = v(f )[p ′] if v is a record value and f ∈ dom(v)
  (3) undefined otherwise
Similarly, if tv = ⟨v, t⟩ and tv ′ are both tagged values, then tv[p := tv ′] is defined inductively by:
  (1) tv[[] := tv ′] = tv ′
  (2) tv[f :: p ′ := tv ′] = ⟨v [f 7→ v(f )[p ′ := tv ′]], t⟩ if v is a record value and f ∈ dom(v)
  (3) undefined otherwise
1 In a well-formed tagged value, the type of the value must be consistent with the tag (see Definition 5.1).



                                                             11
,,        Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar


   States. In the Move semantics, a state comprises persistent global storage, local memory, operand
stack and local variables.
   If L is the set of memory locations, then a reference is a triple ref ⟨c, p, q⟩ consisting of a location
c ∈ L, path p, and mutability qualifier q ∈ {mut, immut}.
   Local states and global states include memories, which are mappings from locations to values,
and stacks. Specifically, a memory M is a partial function from L to TV . Defining local values to be
locations or references, a local memory is similarly a partial function from V to local values, where
V is a set of local variables. A local stack is a list of stack values, which may be tagged values or
references.
   Global resources are identified by an address and a resource type. If A is the set of addresses,
then the set G = A × T of global resource ids consists of pairs ⟨a, R⟩, each associating a primitive
value a ∈ A of type addresses with a resource type R ∈ T . A global store G is a partial function
from global resource ids G to L.
   A global state is a tuple ⟨M, G, L, S⟩, where M is a memory, L is a local memory, S is a local stack,
and G is a global store. A local state is similar with the global store omitted.
   A Move program P is a mapping from program locations PC to operations and, if pc ∈ PC
represents the current program counter, then P[pc] is the current instruction and P[pc + 1] is the
next instruction under normal execution. A program state consists of a program counter pc ∈ PC
and a global state.

4.2   Local State Rules
Each rule in Figure 7 operates on local states (global storage is unchanged and thus omitted to keep
the presentation simple) and takes the form
                                                       φ
                                                                              Rule1
                                     ⟨⟨M, L, S⟩, op ⟨·⟩⟩ →0 ⟨M ′, L ′, S ′⟩
where Rule1 is the name of the rule, φ is a precondition for applying it, ⟨M, L, S⟩ and ⟨M ′, L ′, S ′⟩
are local states, and op ⟨·⟩ is an operation parameterized by a field, variable, or record declaration
of the current module. When there are no parameters, we simply write op. We use the following
variable conventions: c ∈ L; x ∈ V; t ∈ T ; v ∈ V ; tv ∈ TV ; f ∈ F ; p is a path; q is a mutability
qualifier; r is a stack value; and s is a type.
    The MvLoc rules show how the state changes when a local value is moved from a local variable
x onto the stack. Note that if the value moved is not a reference, it is removed from memory when
it is placed on the stack. The CpLoc rules copy local values to the stack. In this case, the local
variable x (and memory if applicable) retain their values. Note that these rules can only be applied
if the local value is not a resource. The StLoc rules take the top stack value and store it in the local
variable x. There are two versions of the rule, depending on the current local value of x. If x has no
value or contains a reference, it is always possible to store the stack value in x (note that we can
always choose a c ′ not currently in the domain of M). However, if x contains a tagged value, then
the rule can only be applied if the tagged value is not a resource.
    BorrowLoc pushes a reference to the local value in x onto the stack. BorrowField takes a
reference r from the top of the stack and pushes a new reference onto the stack that points to the
tagged value in field f of the record pointed to by r . FreezeRef turns a mutable reference into an
immutable reference. ReadRef makes a copy of the tagged value pointed to by a reference on top
of the stack and pushes it onto the stack (note that the value must be a non-resource). ReadRef can
be applied to either a mutable reference or an immutable reference. WriteRef takes a non-resource
tagged value tv ′ and a reference r from the stack, and replaces the tagged value tv pointed to by r
(which must also be a non-resource and of the same type) by tv ′. It can only be applied when r is a

                                                        12
Resources: A Safe Language Abstraction for Money                                                                      ,,


                                             L(x) = c      c ∈ dom(M)
                                                                                            MvLoc
                              ⟨⟨M, L, S⟩, MvLoc ⟨x⟩⟩ →0 ⟨M \ c, L \ x, M(c)::S⟩

                                               L(x) = ref ⟨c, p, q⟩
                                                                                          MvLoc-Ref
                                ⟨⟨M, L, S⟩, MvLoc ⟨x⟩⟩ →0 ⟨M, L \ x, L(x)::S⟩

L(x) = c     c ∈ dom(M) M(c) = ⟨v, U⟩                                r = L(x) = ref ⟨c, p, q⟩
                                                  CpLoc                                                    CpLoc-Ref
⟨⟨M, L, S⟩, CpLoc ⟨x⟩⟩ →0 ⟨M, L, M(c)::S⟩                  ⟨⟨M, L, S⟩, CpLoc ⟨x⟩⟩ →0 ⟨M, L, r ::S⟩
         r ∈ TV     (x < dom(L) ∨ L(x) ∈ Re f ∨ (L(x) = c ∧ M(c) = ⟨v, U⟩)) c ′ < dom(M)
                                                                                                                StLoc − TV
                        ⟨⟨M, L, r ::S⟩, StLoc ⟨x⟩⟩ →0 ⟨M [c ′ 7→ r ] , L [x 7→ c ′] , S⟩
                  r ∈ Re f     (x < dom(L) ∨ L(x) ∈ Re f ∨ (L(x) = c ∧ M(c) = ⟨v, U⟩))
                                                                                                        StLoc − Ref
                               ⟨⟨M, L, r ::S⟩, StLoc ⟨x⟩⟩ →0 ⟨M, L [x 7→ r ] , S⟩
                                                     L(x) = c
                                                                                                 BorrowLoc
                       ⟨⟨M, L, S⟩, BorrowLoc ⟨x⟩⟩ →0 ⟨M, L, ref ⟨c, [], mut⟩::S⟩

                    r = ref ⟨c, p, q⟩ c ∈ dom(M) M(c)[p] = (f , tv f ), · · · , t
                                                                
                                                                                                      BorrowField
                     ⟨⟨M, L, r ::S⟩, BorrowField ⟨f ⟩⟩ →0 ⟨M, L, ref ⟨c, p :: f , q⟩::S⟩
                                                                                                        FreezeRef
                  ⟨⟨M, L, ref ⟨c, p, q⟩::S⟩, FreezeRef⟩ →0 ⟨M, L, ref ⟨c, p, immut⟩::S⟩

                             r = ref ⟨c, p, q⟩     c ∈ dom(M) M(c)[p] = ⟨v, U⟩
                                                                                             ReadRef
                                 ⟨⟨M, L, r ::S⟩, ReadRef⟩ →0 ⟨M, L, ⟨v, U⟩::S⟩

                  r = ref ⟨c, p, mut⟩       tv = M(c) tv[p] = ⟨v, U⟩                tv ′ = ⟨v ′, U⟩
                                                                                                        WriteRef
                     ⟨⟨M, L, tv ′::r ::S⟩, WriteRef⟩ →0 ⟨M [c 7→ tv[p := tv ′]] , L, S⟩

                        tv = ⟨v, U⟩                                            r = ref ⟨c, p, q⟩
                                                     Pop                                                    Pop-Ref
            ⟨⟨M, L, tv::S⟩, Pop⟩ →0 ⟨M, L, S⟩                        ⟨⟨M, L, r ::S⟩, Pop⟩ →0 ⟨M, L, S⟩

        s∈T       {(fi , tvi ) | 1 ≤ i ≤ n} : s    tv = ⟨{(fi , tvi ) | 1 ≤ i ≤ n}, t⟩        t ∈ R is fresh
                                                                                                                Pack-R
                             ⟨⟨M, L, tv 1 :: · · · ::tvn ::S⟩, Pack ⟨s⟩⟩ →0 ⟨M, L, tv::S⟩

        s<T       {(fi , tvi ) | 1 ≤ i ≤ n} : s    tv = ⟨{(fi , tvi ) | 1 ≤ i ≤ n}, U⟩         tvi = ⟨vi , U⟩
                                                                                                                Pack-U
                             ⟨⟨M, L, tv 1 :: · · · ::tvn ::S⟩, Pack ⟨s⟩⟩ →0 ⟨M, L, tv::S⟩
                                        tv = ⟨{(fi , tvi ) | 1 ≤ i ≤ n}, t⟩
                                                                                               Unpack
                         ⟨⟨M, L, tv::S⟩, Unpack ⟨s⟩⟩ →0 ⟨M, L, tv 1 :: · · · ::tvm ::S⟩
                                                                                           LoadConst
                               ⟨⟨M, L, S⟩, LoadConst ⟨a⟩⟩ →0 ⟨M, L, ⟨a, U⟩::S⟩
                                    tvi = ⟨vi , U⟩      legal (Op, v 1 , . . . , vn )
                                                                                                      StackOp
                     ⟨⟨M, L, tv 1 ::· · · tvn ::S⟩, Op⟩ →0 ⟨M, L, ⟨Op(v 1 , . . . , vn ), U⟩::S⟩

                      Fig. 7. Operational Semantics of Move: operations on local state


                                                           13
,,        Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar


           tv 1 = ⟨a, U⟩    a∈A       tv 2 = ⟨v, t⟩    v :s     s∈T      ⟨a, s⟩ < dom(G) c < dom(M)
                                                                                                         MoveTo
                 ⟨⟨M, G, L, tv 1 ::tv 2 ::S⟩, MoveTo ⟨s⟩⟩ →0 ⟨M [c 7→ tv 2 ] , G [⟨a, s⟩ 7→ c] , L, S⟩

                           s∈T      tv = ⟨a, U⟩       a∈A       G(⟨a, s⟩) = c   M(c) = tv ′
                                                                                                 MoveFrom
                       ⟨⟨M, G, L, tv::S⟩, MoveFrom ⟨s⟩⟩ →0 M \ c, G \ ⟨a, s⟩, L, tv ′ ::S

                                  s∈T       tv = ⟨a, U⟩       a∈A      G(⟨a, s⟩) = c
                                                                                                    BorrowGlobal
                    ⟨⟨M, G, L, tv::S⟩, BorrowGlobal ⟨s⟩⟩ →0 ⟨M, G, L, ref ⟨c, [], mut⟩::S⟩

                                  tv = ⟨a, U⟩     a∈A         b ⇔ ⟨a, s⟩ ∈ dom(G)
                                                                                         Exists
                               ⟨⟨M, G, L, tv::S⟩, Exists ⟨s⟩⟩ →0 ⟨M, G, L, ⟨b, U⟩::S⟩

                       Fig. 8. Operational Semantics of Move: Global state operations


mutable reference. The distinction between mutable and immutable references is not particularly
useful in the semantics. However, we include these qualifiers because they are crucially important
for the correct operation of the Move bytecode verifier and because we want the semantics to
accurately reflect the real implementaion.
   The Pop rules pop a stack value off the top of the stack (so long as it is not a resource). The
Pack rules (Pack-R and Pack-U) create a record of a given type s. The Unpack rule decomposes
a record into its fields. For resources, Pack-R pairs the record with a fresh resource tag, i.e., in each
application of the rule a new unique tag is created. The Unpack rule discards the tag associated with
the unpacked record, but freshness guarantees the discarded tag will not be reused. LoadConst
places a constant primitive value a onto the stack. StackOp is a meta-rule: there is an instance of
the rule for every operation on primitive data values (e.g. negation and conjunction on Booleans,
addition and subtraction on integers, etc.). The instantiated rules are formed by replacing Op by
the specific operation and replacing legal by a condition that specifies legal operands for each Op
(e.g. that the divisor is non-zero for a division operation).

4.3   Global State Rules
The rules of Figure 8 are similar except that they operate on global states. MoveTo takes an address
and a resource from the stack and puts the resource in the global storage at the location indexed
by the address and the resource type. Conversely, MoveFrom removes a resource from global
storage and puts it on the stack. BorrowGlobal gets a reference to a resource in global storage.
And finally, Exists checks whether the global storage currently contains a resource for a particular
global resource id. In this rule, b is set to true if ⟨a, s⟩ is in the domain of G, and is false otherwise.

4.4   Program State Rules
The rules of Figure 9 lift the small-step semantics presented so far to semantics of call-free Move
programs that can model loops and conditional branching using unstructured control-flow. They
assume an abstract set PC of program locations over which a program counter pc ranges. A program
P is a mapping from such program locations to operations. The combined global, local, and memory
state (represented in the rule Step as σ ) is extended with the pc to obtain a program state, and the
rules simply implement sequential and branching control flow in a straightforward way.
   These evaluation rules intentionally get stuck in the presence of resource, type, or memory
errors (e.g., CpLoc on a variable that contains a resource). As we mentioned in Section 3.1, the
Move bytecode verifier performs checks that preclude these errors. However, there are two kinds

                                                           14
Resources: A Safe Language Abstraction for Money                                                                               ,,


                                               P [pc] = op, ⟨σ , op⟩ →0 σ ′
                                                                                   Step
                                             P ⊢ ⟨pc, σ ⟩ → ⟨pc + 1, σ ′⟩
                                       P [pc] = Branch ⟨ℓ⟩ , M(c) = ⟨true, U⟩
                                                                                          Branch-T
                                       P ⊢ ⟨pc, ⟨M, L, c::S⟩⟩ → ⟨ℓ, ⟨M, L, S⟩⟩
                                      P [pc] = Branch ⟨ℓ⟩ , M(c) = ⟨f alse, U⟩
                                                                                             Branch-F
                                    P ⊢ ⟨pc, ⟨M, L, c::S⟩⟩ → ⟨pc + 1, ⟨M, L, S⟩⟩

                                               Fig. 9. Program counter rules


of runtime errors not caught by the bytecode verifier that we also model as stuck execution for
convenience:
   (1) Errors in Op such as division by zero and arithmetic over/underflow (which Move chooses to
       treat as errors);
   (2) Overwriting an existing global resource id in MoveTo or accessing a global resource id that
       does not exist in MoveFrom or BorrowGlobal.
In practice, these runtime errors trigger an abort that terminates the current transaction and reverts
any changes to global state.

5    RESOURCE SAFETY
In this section, we prove that the operational semantics introduced above enforces a conservation
property: a resource cannot be created or destroyed except by the privileged Pack and Unpack
constructs available in its declaring module. We define a set of well-formed states (Definition 5.5),
show that the semantic rules preserve well-formedness (Proposition 5.7), and finally, that well-
formedness guarantees resource safety (Theorem 5.10). We start by introducing the parts of a
well-formed state.
  Definition 5.1 (Well-formed tagged value). A tagged value tv = ⟨v, t⟩ with v : s is well-formed if s ∈
T iff t ∈ R, and in addition, one of the following holds: (i) v is primitive; (ii) v = {(fi , tvi ) | 1 ≤ i ≤ n}
such that every tvi is well-formed, and if s < T then for every i, tvi is not a resource.
Intuitively, in a well-formed tagged value, a resource value is never nested inside of an non-resource
value, and the tag corresponds to the type.
   Definition 5.2 (Globally consistent state). We say that a state ⟨M, G, L, S⟩ is globally consistent
if the following holds: (i) Every tagged value in imд(M) or in S is well-formed; (ii) dom(M) =
imд(G) ∪ (imд(L) ∩ L); (iii) For every ⟨a, s⟩ ∈ dom(G), M(G(⟨a, s⟩)) = ⟨v, t⟩ with v : s.
Intuitively, (i) means that tagged values in the state are well-formed; (ii) means that global resource
ids and local variables only point to locations in the memory (no dangling references) and the
memory only contains locations pointed to by some global resource id or local variable (no garbage);
(iii) means that global values have their expected types.
    Definition 5.3 (Tag-consistent state). A state ⟨M, G, L, S⟩ is tag-consistent if the following holds:
(i) if M(c 1 )[p1 ] = ⟨v 1 , t⟩, M(c 2 )[p2 ] = ⟨v 2 , t⟩, and t , U, then c 1 = c 2 and p1 = p2 ; (ii) If S =
[. . . , si 1 , . . . , si 2 , . . .], si 1 [p1 ] = ⟨v 1 , t⟩, si 2 [p2 ] = ⟨v 2 , t⟩, and t , U, then i 1 = i 2 and p1 = p2 ; and
(iii) It is never the case that S = [. . . , si , . . .], M[c][pc ] = ⟨v 1 , t⟩, si [pi ] = ⟨v 2 , t⟩, and t , U.
Intuitively, being tag-consistent means that resource tags are unique, i.e. a resource tag can appear
in the memory and the stack at most once.

                                                               15
,,         Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar


     Definition 5.4 (Non-aliasing). A state ⟨M, G, L, S⟩ is non-aliasing if the following holds: (i) If
x 1 , x 2 ∈ dom(L) with x 1 , x 2 and L(x 1 ), L(x 2 ) ∈ L, then L(x 1 ) , L(x 2 ); (ii) If д1 , д2 ∈ G with д1 , д2 ,
then G(д1 ) , G(д2 ); and (iii) If д ∈ G and x ∈ dom(L) then G(д) , L(x).
Intuitively, a state is non-aliasing if different global or local identifiers cannot point to the same
memory location.
  Definition 5.5 (Well-formed state). A state ⟨M, G, L, S⟩ is well-formed if it is globally consistent,
tag-consistent, and non-aliasing.
Well-formed states ensure that global resource identifiers and local variables only point to locations
that are in the memory, and do not alias. Note, however, that according to these semantics, a
well-formed state may still contain dangling references i.e., ref ⟨c, p, q⟩ ∈ imд(L) ∪S s.t. c < dom(M),
as well as aliasing between references. As explained in Section 3.1, the bytecode veirifer ensures
stronger guarantees (e.g., no dangling references), but in this section we do not depend on these
stronger invariants.
   We now show that the operational semantics preserves well-formedness of states.
   Definition 5.6 (Well-formed execution sequence). Let P be a program. An execution sequence of
P is π = ⟨pc 0 , σ0 ⟩ , . . . , ⟨pc n , σn ⟩ such that pc i ∈ dom(P) for every 0 ≤ i ≤ n and P ⊢ pc i , σi →
 pc i+1 , σi+1 for every 0 ≤ i < n. An execution sequence is called well-formed if each σi is well-
formed.
   Proposition 5.7. Let P be a program and π = ⟨pc 0 , σ0 ⟩ , . . . , ⟨pc n , σn ⟩ an execution sequence of P.
If σ0 is well-formed, then π is well-formed, i.e., σ1 , . . . , σn are all well-formed.
   Proof. The proof is by induction on n, and amounts to a routine check that the rules of Figure 7
and Figure 8, as well as the Branch-F and Branch-T rules of Figure 9 preserve well-formedness.
We explicitly prove this for MvLoc. The rest are verified similarly. Global Consistency: (i) follows
from the induction hypothesis since the set of tagged values in the memory and the stack are not
changed. (ii) is also preserved: by the induction hypothesis, ⟨M, G, L, S⟩ is non-aliasing. Thus, the
fact that x is removed from L also means that c is removed from imд(G) ∪ (imд(L) ∩ L). Since c
is also removed from M, it follows that (ii) holds. (iii) is preserved since G is unchanged and no
locations are added to M. Tag Consistency: (i) is preserved as the memory only gets smaller after
MvLoc. (ii) and (iii) hold initially by the induction hypotehsis; it is easy to see that both must also
hold after moving a value from memory to the stack. Non-Aliasing: (ii) holds since the global
state is unchanged. Additionally, (i) and (iii) are preserved as L only gets smaller after MvLoc. □

   Next, we define the resources of a state, and what it means for resources to be introduced or
eliminated in an execution sequence. We can then prove the resource safety theorem.
  Definition 5.8 (State Resources). Let σ = ⟨M, G, L, S⟩ be a state. The resources of σ , denoted R(σ ),
are defined as follows: R(⟨M, G, L, S⟩) = {t ∈ R | ⟨v, t⟩ ∈ imд(M) ∪ S }
Intuitively, resources of a state are the resource tags that occur in a tagged value of the state.
   Definition 5.9 (Resources Introduced and Eliminated). Let P be a program and π =
⟨pc 0 , σ0 ⟩ , . . . , ⟨pc n , σn ⟩ an execution sequence of P. The set of resources introduced in π , denoted
R I (π ), is: {t ∈ R | ∃ 0 ≤ i < n. P pc i = Pack and σi+1 = ⟨M, G, L, ⟨v, t⟩::S⟩}. The set of
                                                   

resources eliminated in π , denoted R E (π ), is: {t ∈ R | ∃ 0 ≤ i < n. P pc i = Unpack and
                                                                                         

σi = ⟨M, G, L, ⟨v, t⟩::S⟩}.

                                                         16
Resources: A Safe Language Abstraction for Money                                                               ,,


Intuitively, R I (π ) collects all resource tags that were created (using Pack) during the execution;
similarly, R E (π ) collects all resource tags that were consumed (using Unpack) during the execution.
Notice that these sets are not necessarily disjoint. That is, a resource that is created and later
consumed during π will appear both in R I (π ) and in R E (π ).
   Theorem 5.10 (Resource Safety). Let P be a program and π = ⟨pc 0 , σ0 ⟩ , . . . , ⟨pc n , σn ⟩ a well-
formed execution sequence of P. Then, R(σn ) = R(σ0 ) ∪ R I (π ) \ R E (π ).
   Proof. The proof is by induction on n. The base case (n = 0) is straightforward (in this case,
R I (π ) = R E (π ) = ∅). For the induction step, the induction hypothesis provides:
                                       (∗) R(σn−1 ) = R(σ0 ) ∪ R I (π ′) \ R E (π ′)
where π ′ = ⟨pc 0 , σ0 ⟩ , . . . , ⟨pc n−1 , σn−1 ⟩. If P pc n−1 < {Pack ⟨s⟩ , Unpack}, then examination of the
                                                               

rules shows that R(σn ) = R(σn−1 ) (i.e. for all rules other than the Pack and Unpack rules, the set of
resource tags in the global state remains the same after the application of the rule). By Definition 5.9,
R I (π ) = R I (π ′
                ) and R E (π ) = R E (π ). Using (∗), we
                                              ′
                                                                     n ) = R(σ0 )∪R I (π )\R E (π ). The proof is
                                                               get R(σ
similar if P pc n−1 = Pack ⟨s⟩ and s < T or if P pc n−1 = Unpack and σn−1 = ⟨M, G, L, ⟨v, U⟩::S⟩.
If P pc n−1 = Pack ⟨s⟩ for a resource type s, then by Pack-R, R(σn ) = R(σn−1 ) ∪ {t } where
            

σn = ⟨M, G, L, ⟨v, t⟩::S⟩. We know t is fresh, so it is not in R E (π ′). By Definition 5.9, R I (π ) =
R I (π ′) ∪ {t} and R E (π ) = R E (π ′). Thus, by (∗), R(σn ) = R(σ0 ) ∪ R I (π ) \ R E (π ). The proof is
similar if P pc n−1 = Unpack and σn−1 = ⟨M, G, L, ⟨v, t⟩::S⟩, t , U.                                            □

6     EXPERIENCE WITH MOVE
In this section, we describe the open-source implementation of the Move language, report on our
experience using Move in the Libra blockchain, and mention efforts that have adopted or built on
the language.

6.1    Implementation
   Move Compiler. We have implemented2 a compiler from the Move source code used in Figure 1
and Figure 5 to the Move bytecode language. The source language adds structured control flow
for convenience and expressions to abstract away the operand stack, but the programming model
otherwise matches the bytecode language. Although all of the examples in this paper use explicit
copy and move directives when accessing variables (e.g., let x = copy r), the compiler does not
require these directives. In the absence of a directive, the compiler uses liveness analysis to emit
a move for the last usage of a variable and a copy for all other uses. In addition, the compiler
implements source code equivalents of the bytecode verifier analyses with friendly error messages.
   Move Virtual Machine. The Move virtual machine implements a superset of the bytecode inter-
preter semantics described in Section 4. The implemented interpreter includes gas metering similar
to the EVM [Wood 2014], support for a limited form of generics, and a vector type. The virtual
machine also includes the bytecode verifier, which performs static checks for type safety, usage
of uninitialized variables, reference safety, and stack balancing (to ensure that the callee cannot
illegally access stack locations belonging to a caller). The bytecode verifier has a linker for ensuring
that the usage of external types in a module are consistent with their declarations (e.g., procedure
p invoked in module M1 exists and matches the type signature of its declaring module M2). The
implementation3 of both components consists of about 17K lines of Rust code.
2 https://github.com/libra/libra/tree/master/language/move-lang
3 https://github.com/libra/libra/tree/master/language



                                                          17
,,          Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar


   Although the Move language was originally created to serve as the execution layer for the Libra
blockchain, we have maintained a clean separation between the platform-agnostic Move language
layer implemented in the virtual machine and the Libra-specific layer implemented in the Libra
adapter component and Libra’s Move standard library. This flexible architecture has facilitated
adoption of Move outside of Libra (see Section 6.3).
   Tooling. In addition to the compiler and virtual machine, we have implemented several tools4 to
facilitate testing and analysis of Move code:
      • A testing framework5 that allows users to write multi-transaction test scenarios.
      • A bytecode code coverage tool that attaches to the testing framework and records the bytecode
        instructions exercised by each test.
      • A Move bytecode disassembler similar to the javap utility for Java bytecode. The disassembler
        prints raw bytecode, but can also accept an optional source to bytecode map that augments
        the result with variable names and line numbers.

6.2     Integration With the Libra Blockchain
The Move VM implements the transaction execution layer in the Libra blockchain [Amsden et al.
2019]. At a high level, a blockchain is a simple replicated state machine [Lamport 1984]. Libra
validators (replicas) collectively maintain a distributed database that encodes the global state
structure described in Section 3. Users submit transactions to the system that are batched into a
block, or ordered list of transactions. The role of the transaction execution layer is to take a block
of transactions and the current global state as input and execute each transaction to produce a
write set representing the effects of the transaction on the global state. The effect of the block is the
ordered composition of the effects of each of its transactions.
   The logic for Libra execution lives in two separate places: the Libra adapter, and Libra’s Move
standard library. The Libra adapter contains about 1K lines of Rust code that wrap the Move virtual
machine. The adapter implements logic for splitting a Libra block into transactions, checking a
cryptographic signature on the transaction, extracting a Move transaction script, arguments, and
gas budget to pass to the Move virtual machine, and applying the effects of executing the transaction
to the storage layer.
  Move Standard Library. Libra’s Move standard library consists of 40 modules totalling about
3K lines of Move source code that compile to 44KB of bytecode. Broadly speaking, these modules
implement four categories of functionality:
     (1) Coins: implementations of both single-currency stablecoins and the multi-currency LBR coin
         as described in [The Libra Association 2020]
     (2) Accounts: several different account types, sequence number logic to prevent replay attacks,
         sender authentication, key rotation, events for notifying clients
     (3) Validator management: adding/removing validators, paying gas fees to validators, rotating
         validator cryptographic keys
     (4) Utility modules such as Option, Compare, and FixedPoint32
   We will present a subset of the Coin and Account APIs to give the reader a sense of how Move’s
resources give us the flexibility to implement our own version of concepts that must be baked into
the semantics of other smart contract languages.


4 https://github.com/libra/libra/tree/master/language/tools
5 https://libra.org/en-US/blog/how-to-use-the-end-to-end-tests-framework-in-move/



                                                              18
Resources: A Safe Language Abstraction for Money                                                 ,,


resource T { value: u64 }
resource MarketCap { total_value: u64 }

// create a Coin with value=0
fun zero(): Coin::T
// Consume c and increment c_ref by its value
fun deposit(c_ref: &mut Coin::T, c: Coin::T)
// Decrement c_ref by amt, create Coin with value=amt
fun withdraw(c_ref: &mut Coin::T, amt: u64): Coin::T
// create Coin with value=amt, update MarketCap by amt. privileged operation
fun mint(amt: u64): Coin::T


                                    Fig. 10. A subset of the Coin module API.


resource T { bal: Coin::T, seq_num: u64, auth_key: vector<u8>, has_withdraw_cap: bool, ... }
// represents the permission to withdraw from account
resource WithdrawCap { account: address }
fun create(addr: address) // publish a T under addr
// debits the tx sender's balance by amt
fun withdraw_from_sender(amt: u64): Coin::T
// credits recipient's balance by c.value
fun deposit(recipient: address, c: Coin::T)
fun rotate_sender_auth_key(new_auth_key: bytes)
// acquire unique withdraw capability for sender
fun extract_sender_withdraw_cap(): Account::WithdrawCap
// debits the balance at cap.account by amt
fun withdraw(amt: u64, cap: &Account::WithdrawCap): Coin::T


                                  Fig. 11. A subset of the Account module API.


   Coin Module. The Coin module in Figure 10 implements the native currency of the Libra platform
by wrapping an integer value with a safe API. This module clearly illustrates the value of combining
linearity with traditional modularity. Any user can create a coin worth zero, combine two coins
with deposit, or split a single coin into two coins with withdraw. The reader might wonder why
withdraw chooses to mutate a &mut Coin::T rather than expose a functional API that takes two
Coin::T’s and returns a new one. The answer is that the reference parameter provides needed
flexibility for updating a Coin::T object stored in the field of another resource. For example: the
functional API could not be used to update the balance field of the Bank::T resource in Figure 1.
   The privileged mint operation allows a privileged user (the body contains a permission check)
to create new currency and update the integer value stored in the MarketCap resource. The body
of the procedure also ensures that there is a single MarketCap resource in the system published at
address a.
   The conservation of currency in the Libra system can thus be stated as a local invariant of the
Coin module: the sum of the values of each Coin::T resource in the system must be equal to the
total_value field of the MarketCap resource. The combination of the strong encapsulation described
in Section 3.1 and resource safety guarantees defined in Section 5 ensure that Coin::T’s cannot
be created, destroyed, or modified by code outside the Coin module. The Coin module needs only
to ensure that deposit and withdraw conserve the value fields of the input/output field and that
the MarketCap is updated appropriately whenever new coins are created. This can be verified with
straightforward local reasoning over the Coin module.
   To the best of our knowledge, no other blockchain platform has made a rigorous argument
for the conservation of its native currency. We note that there are known counterexamples for
conservation such as the Scilla emit bug described in Section 2.

                                                         19
,,          Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar


   Account Module. A Libra user account at address a is represented by storing an Account::T
resource under a. This resource holds all of the information a user needs to transact: a balance,
a sequence number to prevent replay attacks, and an authentication key. The module exposes
procedures for withdrawing funds and rotating authentication keys (for the transaction sender
only) and depositing funds (to any address).
   In addition, the module allows the holder of the WithdrawCap capability to debit an account (similar
to the Bank::Credit resource in Figure 1). The implementation of extract_sender_withdraw_cap
(not shown) uses the has_withdraw_cap field to ensure that there is at most one WithdrawCap for
each account in the system. An account whose WithdrawCap has been extracted can no longer use
withdraw_from_sender—using the unique capability for account address a is the only way to debit
the balance of a. Similar to native currency conservation in Coin, the uniqueness property for
WithdrawCap can be established with simple local reasoning in the Account module.
   In addition, using a resource to explicitly represent the permission to withdraw from an account
provides significant flexibility for users of Libra. A common use-case for contracts is placing
preconditions on the funds stored in certain addresses; for example:
      • Funds should only be sent to recipients in a whitelist
      • Funds should only be transferred after a certain date
      • Funds should only be withdrawn with the approval of a quorum
Each of these policies can be implemented by creating a resource that stores a WithdrawCap and
restricts access accordingly. Platforms like Ethereum [Wood 2014] support this use case by imple-
menting payments with dynamic dispatch and allowing contracts to override the default payment
behavior, but (as we explained in Section 2), this is a dangerous pattern because payment to an
unknown address can call arbitrary code. The capability-based approach of WithdrawCap enables
custom payment logic without dynamic dispatch by moving the dynamism to the withdrawal code
(known and trusted by the sender) instead of the recipient code (unknown and not trusted by the
sender).
   Deployment in the Libra Testnet. The Move VM is currently running as part of the public Libra
testnet6 that previews the functionality of the Libra payment system (expected to launch in 2020
pending regulatory approval). The testnet supports a whitelist of transaction scripts that exercise
all of the modules in the Move standard library. To limit the scope and risk of the launch, the testnet
does not currently allow users to publish new modules. We hope that this will change in time as the
Libra Association works with regulators to define appropriate safeguards for third-party publishing
of smart contracts.

6.3    Move Usage Outside of Libra
The flexibility of the Move language and the modularity of the Move VM has facilitated external
interest in/adoption of Move in both academic and industrial contexts.
  Other Blockchains. Solana7 is a multi-language blockchain that supports Move smart contracts
and has publicly launched. The dfinance8 and OpenLibra9 blockchain platforms are using Move,
but have not yet launched. The Flow blockchain is an upcoming project from Dapper Labs, the
creator of the popular CryptoKitties project in Ethereum. Dapper is considering using the Move

6 https://developers.libra.org/docs/my-first-transaction
7 https://solana-labs.github.io/book/embedding-move.htm
8 https://docs.dfinance.co/move_vm
9 https://www.openlibra.io/



                                                           20
Resources: A Safe Language Abstraction for Money                                                    ,,


bytecode as the compilation target for its Cadence source language.10 PRISM [Yang et al. 2019] is an
academic project that seeks to significantly enhance the scalability of existing blockchain platforms.
PRISM has recently implemented smart contract support for both Move and the EVM [Wang et al.
2020].
  Verification Tools. The Move Prover [Zhong et al. 2020] implements a specification language and
functional verification tool for Move. It has been used to specify and verify pre- and post-conditions
for several of the Libra standard library modules. A verification startup called Synthetic Minds
verified key properties of an earlier version of the Coin/Account Libra modules and wrote/verified
several new modules.11

7   RELATED WORK
  Rust. Mozilla’s Rust [Matsakis and Klock 2014] language is used at large companies such as
Google, Amazon, and Facebook. Rust uses a clever affine type system to provide type and memory
safety along with data-race freedom. Move is strongly influenced by Rust, but there are several
important differences:
  (1) Affine vs linear: Rust structs can be silently discarded, but Move resources must be explicitly
      Unpack’ed. This is a profound difference that is required for resource safety, but presents
      complications in the design of many language features (see Section 3.2).
  (2) A subset of Move without the persistent global state GS is superficially similar to a linear
      variant of Rust with many features removed (e.g., references in structs, heap allocation,
      collections, traits, generics, concurrency, unsafe). However, the persistent global state of
      Move gives programmers access to a shared, mutable global state. There is no equivalent
      feature in Rust, and the restrictions of Rust’s borrow checker make it impossible to emulate
      this feature in safe Rust. A key contribution of Move is a representation of global state
      expressive enough to represent complex smart contracts, yet simple enough to preserve the
      safety guarantees we desire.
  (3) Rust is a source language that compiles to an executable representation, whereas Move
      bytecode is itself an executable representation. The key difference is that the guarantees
      enforced by the Move language hold directly on the executable representation (no need to
      trust a compiler) and continue to hold when Move programs are linked against untrusted
      code. This property is a requirement for smart contracts, which are deployed in the open and
      must tolerate arbitrary interactions with untrusted code. Thus, even if the Rust language (or
      a subset) had exactly the properties we wanted, it would not be usable as a smart contract
      language.
   Substructural Type Systems and Ownership Types. Rust is the most mainstream language with a
substructural type system, but it follows in the footsteps of other cleverly designed languages such
as Cyclone [Grossman et al. 2002], Clean [Smetsers et al. 1994], Pony [Clebsch et al. 2015], and
Alms [Tov and Pucella 2011]. A related line of work involves ownership type systems [Clarke et al.
2013] for controlling aliasing in languages with reference semantics. A common theme in both
areas is leveraging types for safe memory management to avoid undefined behavior due to data
races or accessing deallocated/uninitialized memory, but without relying on garbage collection.
   Move also builds on this tradition, but our usage of linearity is broader and more ambitious
than memory management: linear resources are a natural abstraction for digital money and other
programmer-defined assets. The resource safety guarantee from Section 5 is a novel semantic
10 https://medium.com/dapperlabs/libra-and-flow-combining-resources-for-open-source-40530e53fa01
11 https://synthetic-minds.com/pages/blog/blog-2019-09-11.html



                                                         21
,,         Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar


conservation property similar to (e.g.) conservation of mass, stated in a way that is independent
from any particular enforcement mechanism (e.g., linear type or dynamic checks).
   Linear Logic. The modern era of substructural logics and associated type systems began with
Girard’s linear logic [Girard 1987]. In his early explanation of its resource sensitivity, Girard used
an intuitive representation of money. In that account, each number of fixed-value coins has a
different type: two coins would have type C ⊗ C and three coins C ⊗ C ⊗ C. While this encoding of
money illustrates a fundamental difference between linear and intuitionistic logic, the approach
resembles giving each individual integer a different type. (If each integer has a different type, then
any straightforward type system would prohibit a single addition function from being used to add
arbitrary pairs of integers.) Instead of segregating different monetary values in different types, we
need resource types (such as the Coin module in Section 6.2) that create coins of any value which
cannot be duplicated or destroyed outside the control of their defining module. Thus, while Move
draws on Girard’s key insight relating linearity to assets, Move resources give programmers both
provable resource safety and flexibility in representing money-like types.
   Account-based Blockchain Languages. Account-based blockchain languages mimic a classic bank
ledger by representing global state as a map from account addresses to integer balances and
exposing language primitives for debiting one balance and crediting another. We discussed two
prominent executable account-based languages [Sergey et al. 2019; Wood 2014] in Section 2; many
others like IELE [Kasampalis et al. 2019], Agoric JS [Agoric 2019], Michelson [Foundation 2018b],
and Pact [Popejoy 2017] have been proposed in the past few years. Move implements a more
expressive variant of the account-based model where account addresses are associated with a direct
representation of money (programmable resources) instead of an indirect one (integer balances).
   UTXO-based Blockchain Languages. UTXO (unspent transaction output) blockchain languages
represent the global state as a set of (authentication policy, amount) pairs. Programs transfer money
by satisfying the authentication policy of one or more input UTXOs and creating a set of fresh
output UTXOs whose amounts sum to the amounts included in the inputs. Program execution
removes the input UTXOs from the state and adds the fresh ones. This model was pioneered by
Bitcoin’s [Nakamoto 2008] Script [Wiki line] language, and has been adopted by a few more recent
languages such as Simplicity [OâĂŹConnor 2017] and Plutus [Foundation 2019]. Though UTXOs
are a good choice for a platform with a single native currency and limited programmability, they
are cumbersome to use for general-purpose state changes. We feel that Move’s resources are a
more flexible approach to implementing diverse financial assets with customizable behaviors.
  Blockchain Source Languages with Linear Types. Flint [Schrans et al. 2019] and Obsidian [Coblenz
2017; Coblenz et al. 2019] are contract programming languages that use linear types as an explicit
representation of assets. These languages enforce linearity at the source level, but compile to an
executable representation (EVM bytecode [Wood 2014] and a Java subset used by Hyperledger
Fabric [Foundation 2018c], respectively) without the same protections. Nomos [Das et al. 2019]
uses session types to achieve even stronger static protections, but also does not consider the
problem of applying the type system to an executable blockchain representation. The Cadence
source language12 has linear types and is considering Move bytecode as a compilation target (see
Section 6.3).
  The distinguishing feature of Move is an executable bytecode representation with resource
safety guarantees for all programs. This is crucially important given the open deployment model
for contracts—recall that any contract must tolerate arbitrary interactions with untrusted code.
12 https://docs.onflow.org/docs/cadence



                                                         22
Resources: A Safe Language Abstraction for Money                                                                             ,,


Source-level linearity has limited value if it can be violated by untrusted code at the executable
level (e.g., untrusted code that duplicates a source-level linear type).

8   CONCLUSION
We have introduced language support for a specific form of linear resource types, formalized
corresponding semantic resource safety properties, and proved that they hold for successful concrete
execution of Move programs. The language construct provides a safe abstraction for currency-like
values in the Move language, as illustrated by example in Section 2 and through more extensive
experience summarized in Section 6. In future work, we plan to describe and formalize the Move
bytecode verifier, which involves interesting and novel static analyses for ensuring type, resource,
and reference safety invariants. One goal of the verifier is to ensure progress for concrete execution
of Move programs in the checking semantics of the present paper, complementing the safety
guarantees proved here. Overall, we believe the semantic guarantees and successful programming
experience presented in this paper suggest that the language design and implementation provide
better language support and more effective design patterns for the growing range of resource-
sensitive applications of blockchain and related platforms.

REFERENCES
Agoric. 2019. https://github.com/Agoric/SES
Zachary Amsden, Ramnik Arora, Shehar Bano, Mathieu Baudet, Sam Blackshear, Abhay Bothra, George Cabrera, Christian
   Catalini, Konstantinos Chalkias, Evan Cheng, Avery Ching, Andrey Chursin, George Danezis, Gerardo Di Giacomo,
   David L. Dill, Hui Ding, Nick Doudchenko, Victor Gao, Zhenhuan Gao, FranÃğois Garillot, Michael Gorven, Philip Hayes,
   J. Mark Hou, Yuxuan Hu, Kevin Hurley, Kevin Lewi, Chunqi Li, Zekun Li, Dahlia Malkhi, Sonia Margulis, Ben Maurer,
   Payman Mohassel, Ladi de Naurois, Valeria Nikolaenko, Todd Nowacki, Oleksandr Orlov, Dmitri Perelman, Alistair Pott,
   Brett Proctor, Shaz Qadeer, Rain, Dario Russi, Bryan Schwab, Stephane Sezer, Alberto Sonnino, Herman Venter, Lei Wei,
   Nils Wernerfelt, Brandon Williams, Qinfan Wu, Xifan Yan, Tim Zakian, and Runtian Zhou. 2019. The Libra Blockchain.
   https://developers.libra.org/docs/the-libra-blockchain-paper.
R. Armstrong. 2019. JPMorgan plan to coin it on the blockchain. Financial Times. https://www.ft.com/content/0bafd9d6-
   307e-11e9-8744-e7016697f225
Nicola Atzei, Massimo Bartoletti, and Tiziana Cimoli. 2017. A Survey of Attacks on Ethereum Smart Contracts (SoK). In
   Principles of Security and Trust - 6th International Conference, POST 2017, Held as Part of the European Joint Conferences on
   Theory and Practice of Software, ETAPS 2017, Uppsala, Sweden, April 22-29, 2017, Proceedings. 164–186.
Sam Blackshear, Evan Cheng, David L. Dill, Victor Gao, Ben Maurer, Todd Nowacki, Alistair Pott, Shaz Qadeer, Rain,
   Dario Russi, Stephane Sezer, Tim Zakian, and Runtian Zhou. 2019. Move: A Language With Programmable Resources.
   https://developers.libra.org/docs/move-paper.
Vitalik Buterin. 2016. Critical update re DAO.            https://ethereum.github.io/blog/2016/06/17/critical-update-re-dao-
   vulnerability
M.J. Casey and P. Wong. 2017. Global Supply Chains Are About to Get Better, Thanks to Blockchain. Harvard Business
   Review.
Dave Clarke, Johan Östlund, Ilya Sergey, and Tobias Wrigstad. 2013. Ownership Types: A Survey. In Aliasing in Object-
   Oriented Programming. Types, Analysis and Verification. 15–58. https://doi.org/10.1007/978-3-642-36946-9_3
Sylvan Clebsch, Sophia Drossopoulou, Sebastian Blessing, and Andy McNeil. 2015. Deny capabilities for safe, fast actors. In
   Proceedings of the 5th International Workshop on Programming Based on Actors, Agents, and Decentralized Control, AGERE!
   2015, Pittsburgh, PA, USA, October 26, 2015. 1–12. https://doi.org/10.1145/2824815.2824816
Michael J. Coblenz. 2017. Obsidian: a safer blockchain programming language. In Proceedings of the 39th International
   Conference on Software Engineering, ICSE 2017, Buenos Aires, Argentina, May 20-28, 2017 - Companion Volume. 97–99.
   https://doi.org/10.1109/ICSE-C.2017.150
Michael J. Coblenz, Reed Oei, Tyler Etzel, Paulette Koronkevich, Miles Baker, Yannick Bloem, Brad A. Myers, Joshua Sunshine,
   and Jonathan Aldrich. 2019. Obsidian: Typestate and Assets for Safer Blockchain Programming. CoRR abs/1909.03523
   (2019). arXiv:1909.03523 http://arxiv.org/abs/1909.03523
Ankush Das, Stephanie Balzer, Jan Hoffmann, and Frank Pfenning. 2019. Resource-Aware Session Types for Digital Contracts.
   arXiv:cs.PL/1902.06056
Ethereum Foundation. 2018a. Solidity Documentation. http://solidity.readthedocs.io
IOHK Foundation. 2019. Plutus: A Functional Contract Platform. https://testnet.iohkdev.io/plutus.

                                                              23
,,         Sam Blackshear, David L. Dill, Shaz Qadeer, Clark W. Barrett, John C. Mitchell, Oded Padon, and Yoni Zohar


Tezos Foundation. 2018b. Michelson: the language of Smart Contracts in Tezos. http://tezos.gitlab.io/mainnet/whitedoc/
   michelson.html.
The Linux Foundation. 2018c. Hyperledger Fabric. https://www.hyperledger.org/projects/fabric.
Jean-Yves Girard. 1987. Linear Logic. Theor. Comput. Sci. (1987).
Dan Grossman, J. Gregory Morrisett, Trevor Jim, Michael W. Hicks, Yanling Wang, and James Cheney. 2002. Region-Based
   Memory Management in Cyclone. In Proceedings of the 2002 ACM SIGPLAN Conference on Programming Language Design
   and Implementation (PLDI), Berlin, Germany, June 17-19, 2002. 282–293. https://doi.org/10.1145/512529.512563
Norman Hardy. 1994. The Confused Deputy (or why capabilities might have been invented). ACM SIGOPS Operating
   Systems Review 22 (1994), 36–38.
Theodoros Kasampalis, Dwight Guth, Brandon M. Moore, Traian-Florin Serbanuta, Yi Zhang, Daniele Filaretti, Virgil Nicolae
   Serbanuta, Ralph Johnson, and Grigore Rosu. 2019. IELE: A Rigorously Designed Language and Tool Ecosystem for the
   Blockchain. In Formal Methods - The Next 30 Years - Third World Congress, FM 2019, Porto, Portugal, October 7-11, 2019,
   Proceedings. 593–610.
Leslie Lamport. 1984. Using Time Instead of Timeout for Fault-Tolerant Distributed Systems. ACM Trans. Program. Lang.
   Syst. (1984).
Tim Lindholm and Frank Yellin. 1997. The Java Virtual Machine Specification. Addison-Wesley.
Nicholas D. Matsakis and Felix S. Klock, II. 2014. The Rust Language. Ada Lett. 34, 3 (Oct. 2014), 103–104. https:
   //doi.org/10.1145/2692956.2663188
Erik Meijer, Redmond Wa, and John Gough. 2000. Technical Overview of the Common Language Runtime.
Mark S. Miller, Ka-Ping Yee, and Jonathan Shapiro. 2003. Capability Myths Demolished. Technical Report.
Satoshi Nakamoto. 2008. Bitcoin: A peer-to-peer electronic cash system. (2008). http://bitcoin.org/bitcoin.pdf
Russell OâĂŹConnor. 2017. Simplicity: A New Language for Blockchains. https://blockstream.com/simplicity.pdf
Santiago Palladino. 2017. The Parity wallet hack explained. https://blog.zeppelin.solutions/on-the-parity-wallet-multisig-
   hack-405a8c12e8f7
Stuart Popejoy. 2017. The Pact Smart-Contract Language. http://kadena.io/docs/Kadena-PactWhitepaper.pdf.
Franklin Schrans, Daniel Hails, Alexander Harkness, Sophia Drossopoulou, and Susan Eisenbach. 2019. Flint for Safer Smart
   Contracts. CoRR abs/1904.06534 (2019). arXiv:1904.06534 http://arxiv.org/abs/1904.06534
Ilya Sergey, Vaivaswatha Nagaraj, Jacob Johannsen, Amrit Kumar, Anton Trunov, and Ken Chan Guan Hao. 2019. Safer
   smart contract programming with Scilla. PACMPL 3, OOPSLA (2019), 185:1–185:30. https://doi.org/10.1145/3360611
Sjaak Smetsers, Erik Barendsen, Marko C. J. D. van Eekelen, and Marinus J. Plasmeijer. 1994. Guaranteeing Safe Destructive
   Updates Through a Type System with Uniqueness Information for Graphs. In Proceedings of the International Workshop
   on Graph Transformations in Computer Science. Springer-Verlag, Berlin, Heidelberg, 358–379. http://dl.acm.org/citation.
   cfm?id=647364.725667
Bjarne Stroustrup. 2013. The C++ Programming Language (4th ed.). Addison-Wesley Professional.
David Swasey, Deepak Garg, and Derek Dreyer. 2017. Robust and compositional verification of object capability patterns.
   PACMPL 1, OOPSLA (2017), 89:1–89:26. https://doi.org/10.1145/3133913
Nick Szabo. 1997. Formalizing and Securing Relationships on Public Networks. First Monday 2, 9 (1997). https://ojphi.org/
   ojs/index.php/fm/article/view/548
The Libra Association. 2020. The Libra White Paper v2.0. https://libra.org/en-us/white-paper.
Jesse A. Tov and Riccardo Pucella. 2011. Practical affine types. In Proceedings of the 38th ACM SIGPLAN-SIGACT Symposium
   on Principles of Programming Languages, POPL 2011, Austin, TX, USA, January 26-28, 2011. 447–458. https://doi.org/10.
   1145/1926385.1926436
Gerui Wang, Shuo Wang, Vivek Bagaria, David Tse, and Pramod Viswanath. 2020. Prism Removes Consensus Bottleneck
   for Smart Contracts. arXiv:cs.DC/2004.08776
Bitcoin Wiki. online. Bitcoin Script. https://en.bitcoin.it/wiki/Script
Gavin Wood. 2014. Ethereum: A secure decentralised generalised transaction ledger. (2014). https://ethereum.github.io/
   yellowpaper/paper.pdf
Lei Yang, Vivek Bagaria, Gerui Wang, Mohammad Alizadeh, David Tse, Giulia Fanti, and Pramod Viswanath. 2019. Prism:
   Scaling Bitcoin by 10,000x. arXiv:cs.DC/1909.11261
Jingyi Emma Zhong, Kevin Cheang, Shaz Qadeer, Wolfgang Grieskamp, Sam Blackshear, Yoni Zohar, Clark Barrett, and
   David L. Dill. 2020. The Move Prover. To appear in CAV 2020.




                                                           24
