                                                                                                                                                                  1

                                         Resource Specifications for Resource-Manipulating
                                         Programs
arXiv:2304.12530v2 [cs.PL] 18 Apr 2024




                                         ZACHARY GRANNAN, University of British Columbia, Canada
                                         ALEXANDER J. SUMMERS, University of British Columbia, Canada
                                         Speciﬁcations for modular program veriﬁers are expressed as constraints on program states (e.g. precondi-
                                         tions) and relations on program states (e.g. postconditions). For programs whose domain is managing re-
                                         sources of any kind (e.g. cryptocurrencies), such state-based speciﬁcations must make explicit properties that
                                         a human would implicitly understand for free. For example, it’s clear that depositing into your bank account
                                         will not change other balances, but classically this must be stated as a frame condition. As a result, classical
                                         speciﬁcations for resource-manipulating programs quickly become verbose and diﬃcult to interpret, write
                                         and debug.
                                            In this paper, we present a novel methodology that extends a modular program veriﬁer to support user-
                                         deﬁned ﬁrst-class resources, allowing resource-related operations and properties to be expressed directly and
                                         eliminating the need to reify implicit knowledge in the speciﬁcations. We implement our methodology as an
                                         extension of the program veriﬁer Prusti, and use it to verify real-world smart contracts and a key part of a
                                         blockchain application. Our evaluation demonstrates that speciﬁcations written with our methodology are
                                         more concise and substantially simpler than speciﬁcations written purely in terms of program states.

                                         1       INTRODUCTION
                                         The goal of program veriﬁcation is to ensure that a program will always operate in accordance
                                         with a formal speciﬁcation. In practice, this requires encoding the desired properties in the speci-
                                         ﬁcation language of a program veriﬁer that will be used to check conformance to such properties.
                                         The diﬀerence between our intuitive, human language description of desired properties and their
                                         representation in the speciﬁcation language is called the semantic gap [Hein 2010]. The larger this
                                         gap is in practice, the more diﬃcult it becomes to write, read, maintain, and debug speciﬁcations.
                                            In modular program veriﬁers, speciﬁcations are written and checked for each function sepa-
                                         rately, with the guarantee that separately veriﬁed functions compose to a veriﬁed whole. Speciﬁ-
                                         cation preconditions describe requirements on the program state at function call sites, and post-
                                         conditions describe the corresponding guarantees about the program state at return sites; the ver-
                                         iﬁer checks that, when the precondition holds, the function’s body ensures the postcondition, and
                                         reasons about function calls with respect to these speciﬁcations rather than the function’s imple-
                                         mentation. For example, the speciﬁcation for a function sort() that sorts a list in-place could be
                                         written as an expression relating the values of the input list both before and after the call; namely,
                                         stating that the latter should be a sorted permutation of the former. This design eﬀectively min-
                                         imises the semantic gap for properties naturally expressed as relations on program states, such as
                                         sortedness.
                                            However, properties about programs that manipulate resources, such as money, are more chal-
                                         lenging to specify correctly in this manner. For example, in a banking application, one might con-
                                         sider describing the eﬀect of a function deposit(acct_id, amt), using a postcondition:
                                             1   #[ensures(bank.balance(acct_id) == old(bank.balance(acct_id)) + amt)]
                                         which speciﬁes that after calling bank.deposit() the balance for acct_id will have increased by
                                         amt. However, this speciﬁcation misses an important property: the balance of all other accounts in
                                         Authors’ addresses: Zachary Grannan, University of British Columbia, Vancouver, Canada; Alexander J. Summers, Univer-
                                         sity of British Columbia, Vancouver, Canada.

                                         2018. 2475-1421/2018/1-ART1 $15.00
                                         https://doi.org/

                                                                         Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:2                                                                       Zachary Grannan and Alexander J. Summers


the bank must remain unchanged after the call1 . To address this, the traditional solution is to extend
the speciﬁcation with a frame condition [McCarthy and Hayes 1981]: an assertion that besides the
change to balance(acct_id), everything else stays the same. This results in the postcondition:


 1     #[ensures(bank.balance(acct_id) == old(bank.balance(acct_id)) + amt &&
 2       forall(|a_id: AcctId| a_id != acct_id ==>
 3         bank.balance(a_id) == old(bank.balance(a_id))))]



   This speciﬁcation is longer and more complicated; most of the complexity stems from describing
what’s unchanged by deposit() (this extra complexity grows rapidly for more complicated func-
tions). But in terms of an intuitive understanding of bank deposits, this property simply does not
need to be stated: it’s obvious to humans that depositing money into one account will not change
other balances. This suggests a wide semantic gap between the way we think about resources in
the real-world, and what can be expressed in classical techniques for formal speciﬁcation.
   An elegant way to close this gap is to introduce resources into the speciﬁcation language itself.
Various powerful frameworks (e.g. Iris [Jung et al. 2015]) facilitate this via substructural logic (e.g.
separation logic [Reynolds 2002]). However, many modern, widely-used program veriﬁers such
as Boogie [Leino 2008], Dafny [Leino 2010], and Why3 [Bobot et al. 2011] use classical logic. Al-
though, in general, such veriﬁers provide framing guarantees on a per-data-structure level (e.g. the
modifies clauses in Boogie), we observe that for ﬁne-grained changes there is still a need to de-
ﬁne frame conditions via pointwise assertions on program state, even in state-of-the art program
veriﬁers.
   In this paper, we present a novel methodology for extending an existing speciﬁcation language
with custom resources and operations in a lightweight manner. Our approach allows resource-
related properties to be expressed directly, eliminating the need to reify properties that are implicit
in our intuitive understanding of resources, while building in ubiquitous properties by default, e.g.
that the amount of a resource should remain constant unless explicitly created or destroyed.
   In our methodology, resources used in speciﬁcations are abstractions decoupled from the pro-
gram state. However, our technique allows coupling invariants to be deﬁned, specifying once and
for all the mapping between abstract resource notions and concrete program states. In contrast
to more sophisticated methodologies (e.g. for ﬁne-grained concurrency), our coupling invariants
are not required to be reﬂexive or transitive, and can be desugared via a straightforward syntactic
translation. Speciﬁcations per function can be written concisely and more simply using resource
abstractions, and the coupling invariants automatically and implicitly entail the right proof obli-
gations concerning changes to and constraints on concrete program states.
   Our paper makes the following main contributions:

      (1) We demonstrate the typical problems that arise when writing speciﬁcations of resource-
          manipulating programs in terms of program states (Sec. 2)
      (2) We present a methodology to solve these problems using ﬁrst-class resources (Sec. 3)
      (3) We implement our methodology, extending the Prusti veriﬁer (Sec. 4)
      (4) As a case study, we apply our methodology and implementation to verify a key component
          of a real-world Rust implementation of a cross-chain token transfer protocol (Sec. 5)
      (5) We perform a comparative evaluation of our methodology, showing that it enables shorter
          and simpler speciﬁcations for real-world resource-manipulating programs (Sec. 6)

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                               1:3


 1    type AcctId = u32;
 2    trait Bank {
 3      fn balance(&self, acct_id: AcctId) -> u128;
 4      fn deposit(&mut self, acct_id: AcctId, amt: u128);
 5      fn withdraw(&mut self, acct_id: AcctId, amt: u128);
 6    }

Fig. 1. Rust code defining a Bank interface. Monetary values are represented as unsigned 128-bit integers,
account identifiers are represented by values of type AcctId (u32).

2 MOTIVATION
To motivate our methodology, we ﬁrst present the challenges that arise when writing speciﬁcations
for a resource-manipulating program. Throughout this section, we consider a Rust interface for a
multi-account bank that stores (dollar) balances, shown in Fig. 1. Clients interact with a Bank via
the functions balance, deposit, and withdraw.
   These functions take as ﬁrst parameter a reference to a Bank instance. The syntax &self indi-
cates a Rust shared reference, with which the balance function cannot modify the Bank, while a
mutable reference such as the &mut self parameter of the other functions allows modiﬁcations.
   Speciﬁcations for the Bank interface play two main roles: deﬁning what it means for an imple-
mentation of these functions to be correct (e.g. an implementation of withdraw must correctly
update the correct balance internally), and deﬁning what client code should consider when using
this interface. For example, withdrawing more than the current balance should be forbidden, while
to specify (and modularly verify) a client function such as transfer below relies on having suitable
speciﬁcations for withdraw and deposit:
 1    fn transfer<B: Bank>(bank: &mut B, from: AcctId, to: AcctId, amt: u128) {
 2      bank.withdraw(from, amt); bank.deposit(to, amt);
 3    }
   Real-world programs are substantially more complex than our bank example, although we note
that the Bank trait itself is derived from similar interfaces found in real-world programs (e.g. the
BankKeeper trait described in our case study [Sec. 5]). Nonetheless, even for our simpliﬁed exam-
ple, writing correct speciﬁcations in a classical fashion, i.e. via pointwise assertions on the domain
of the balance function, can nonetheless be challenging and subtle. We now demonstrate three
speciﬁc issues that we encounter when trying to specify this kind of code.

2.1    Three Issues of Specifying Resource-Manipulating Programs
A typical speciﬁcation for our Bank interface would deﬁne postconditions for deposit and withdraw
in terms of calls to balance. As discussed in the introduction, an intuitive (but ultimately insuﬃ-
cient) postcondition for deposit could be written as follows:
 1    #[ensures(self.balance(acct_id) == old(self.balance(acct_id) + amt))]
 2    fn deposit(&mut self, acct_id: AcctId, amt: u128)
  Although a correct implementation should satisfy this postcondition, it is not suﬃcient for (mod-
ular) client reasoning: it speciﬁes the change to balance(acct_id) but doesn’t say anything about
other balances (which should be unchanged). The standard solution is to extend the postcondition
with a frame condition, specifying that the balances of all other accounts remain unchanged. The
withdraw function also requires similar frame conditions. A correct such speciﬁcation for deposit,
1 Strictly speaking, all other aspects of program state (e.g. objects other than bank) should also remain unchanged, however

many program veriﬁers provide some coarse-grained mechanism to facilitate such framing.

                                  Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:4                                                                       Zachary Grannan and Alexander J. Summers


 1     #[ensures(
 2       forall(|acct_id2: AcctId| if acct_id == acct_id2 {
 3          self.balance(acct_id) == old(self.balance(acct_id)) + amt
 4       } else {
 5          self.balance(acct_id2) == old(self.balance(acct_id2))
 6       })
 7     )]
 8     fn deposit(&mut self, acct_id: AcctId, amt: u128);
 9
10     #[requires(self.balance(acct_id) >= amt)]
11     #[ensures(
12       forall(|acct_id2: AcctId| if acct_id == acct_id2 {
13          self.balance(acct_id) == old(self.balance(acct_id)) - amt
14       } else {
15          self.balance(acct_id2) == old(self.balance(acct_id2))
16       })
17     )]
18     fn withdraw(&mut self, acct_id: AcctId, amt: u128);

Fig. 2. Specifications for the deposit and withdraw functions. Each includes an explicit frame condition;
specification lines used to encode the frame condition are highlighted in red.

and the analogous speciﬁcation for withdraw, are presented in Fig. 2. Adding frame conditions
makes the resulting speciﬁcations more complex: much of the speciﬁcation eﬀort is concerned
with precisely specifying what does not change. Similar frame conditions are also necessary for
any function with a mutable reference to a Bank, such as transfer above, whose postcondition
must specify overall what has not changed.
   Deriving a frame condition for transfer is not simply a matter of, say, conjoining those for the
two called functions; instead, one should rethink these speciﬁcations as describing state updates,
mentally compose these updates, and deduce the right end-to-end speciﬁcation of their composi-
tion: the appropriate postcondition of transfer is presented in Fig. 3. Note that the postcondition
does not directly use the speciﬁcation expressions from deposit or withdraw.

 1     #[requires(from != to && bank.balance(from) >= amt)]
 2     #[ensures(forall(|a_id: AcctId|
 3       if      a_id == from { bank.balance(a_id) == old(bank.balance(a_id)) - amt }
 4       else if a_id == to   { bank.balance(a_id) == old(bank.balance(a_id)) + amt }
 5       else                 { bank.balance(a_id) == old(bank.balance(a_id))       }))]
 6     fn transfer<B: Bank>(bank: &mut B, from: AcctId, to: AcctId, amt: u128) { ... }

      Fig. 3. A specification for the transfer function, which makes calls to withdraw and then deposit


      This demonstrates the ﬁrst issue with classical speciﬁcations in this context:
       Issue 1: Specifying resource operations using program states requires frame conditions

  Deriving frame conditions for the composition of multiple operations requires syntactic and
mental overhead. But similar composition issues can arise even without consideration of frame
conditions. For example, consider the function withdraw2 in Fig. 4, which performs two with-
drawal operations in sequence. When we consider how to specify the precondition of this function,
based on the precondition of the withdraw function (Fig. 2), we might consider using:

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                        1:5


 1   #[requires(bank.balance(acct_id1) >= 1 && bank.balance(acct_id2) >= 2)]
  This precondition is not strong enough however: when acct_id1 = acct_id2, the withdraw2
function withdraws $3 from the account. Therefore, a precise precondition needs to explicitly
branch on whether the identiﬁers are equal. Furthermore, the analogous issue exists with the
postcondition: the way we represent the change in program state diﬀers depending on whether the
parameters are equal. An accurate speciﬁcation for the withdraw2 function is presented in Fig. 5.

 1   fn withdraw2<B: Bank>(bank: &mut B, acct_id1: AcctId, acct_id2: AcctId) {
 2     bank.withdraw(acct_id1, 1); bank.withdraw(acct_id2, 2);
 3   }

Fig. 4. A function that performs two withdrawals in sequence. When acct_id1 and acct_id2 are the same,
this function performs two operations on the same account.



 1   #[requires(if(acct_id1 == acct_id2) { bank.balance(acct_id1) >= 3 }
 2     else { bank.balance(acct_id1) >= 1 && bank.balance(acct_id2) >= 2 })]
 3   #[ensures(if(acct_id1 == acct_id2) {
 4     bank.balance(acct_id1) == old(bank.balance(acct_id1) - 3)
 5   } else {
 6     bank.balance(acct_id1) == old(bank.balance(acct_id1) - 1) &&
 7     bank.balance(acct_id2) == old(bank.balance(acct_id2) - 2)
 8   } && forall(|acct_id: AcctId| (acct_id != acct_id1 && acct_id != acct_id2) ==>
 9       bank.balance(acct_id) == old(bank.balance(acct_id))
10   ))]
11   fn withdraw2<B: Bank>(bank: &mut B, acct_id1: AcctId, acct_id2: AcctId) { ... }

Fig. 5. The specifications for the withdraw2 function in Fig. 4. The conditional in the precondition is neces-
sary to handle the possible aliasing between acct_id1 and acct_id2. The postcondition includes an analo-
gous conditional, as well as a frame condition stating that other account balances remain unchanged.

   Again, to systematically derive such a speciﬁcation requires considering the updates described
by the speciﬁcations of the called functions, mentally composing these side-eﬀects, and mapping
the resulting transformation back to a state-based speciﬁcation, considering separate cases cor-
responding to the possible (in-)equalities between parameters as needed. The complexity of this
process increases signiﬁcantly as the number of operations increases. For example, the speciﬁ-
cation for a hypothetical withdraw3 function would need to branch on all equality possibilities
between three parameters. This illustrates the second issue:
     Issue 2: Speciﬁcations of resource operations using program states do not easily com-
     pose

  The speciﬁcations for the Bank should dictate how clients are allowed to interact with it. They
prevent e.g. overdrawing an account via the precondition self.balance(acct_id) >= amt on
withdraw. But they do not enforce inherent properties of how resources should behave. Note that
deposit does not have a precondition: the speciﬁcations do not restrict calls to deposit.
  Fig. 6 shows an alternative (faulty) transfer implementation: it deposits more money in ac-
count to than was withdrawn from account from, eﬀectively creating money out of nowhere. The
speciﬁcations for Bank do not prevent this behaviour: the transfer function veriﬁes. Technically,

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:6                                                                       Zachary Grannan and Alexander J. Summers


    1   #[requires(bank.balance(from) >= amt)]
    2   fn transfer<B: Bank>(bank: &mut B, from: AcctId, to: AcctId, amt: u128) {
    3     bank.withdraw(from, amt); bank.deposit(to, amt); bank.deposit(to, amt);
    4   }

Fig. 6. A buggy transfer function that performs two deposits instead of one. It will be accepted by the verifier,
despite creating money out of nowhere.

transfer is underspeciﬁed: with the complete functional speciﬁcation of its intended eﬀect on
the to account, the function would fail to verify. But the conceptual source of the bug is clear
from the code even with a weak speciﬁcation: it’s wrong for a resource acquired once to be spent
twice. Intuitively, the money spent by deposit should come from somewhere, but this relies on an
understanding of the speciﬁc resources the program works with, and of properties all resources
should have, that is only partially explicit in the program state and its classical speciﬁcations.

        Issue 3: Speciﬁcations using program states cannot easily enforce resource properties

   The root cause underlying all three of these issues is that program states are not the ideal ab-
straction for expressing and reasoning about the behaviour of resource-manipulating programs.
Intuitively, we think about such programs in terms of their operations on resources (e.g. spending
money), incorporating implicit common-sense understanding of how resources work in reality: for
example, resources cannot be duplicated. The key idea behind our work is to make this abstraction
directly available in the speciﬁcation language, reifying this informal intuition and all its beneﬁts
in a formal technique. Our technique is presented concretely in the next section, but the basic
idea is to allow (possibly multiple) custom resource types to be declared for a given program. The
notion of how much of each of these resources is currently held is made a (ghost) part of the pro-
gram state (the resource state), and new speciﬁcation features are provided that deﬁne how much
resource is transferred in and out of function calls.
   The default interpretation of these transfers is that if we don’t specify that one happens, it cannot,
allowing speciﬁcations to describe local updates without explicit frame conditions (Issue 1). Since
resource transfers directly express changes to the resource state, they compose easily (Issue 2).
Using a custom resource to represent withdrawn money prevents the faulty code in Fig. 6, since
the attempt to spend a resource which is no-longer held can be made explicit with our ﬁrst-class
resources and the built-in properties that come with our resource model (Issue 3).
   In the next section, we demonstrate how our methodology enables this kind of reasoning.

3       METHODOLOGY
The core idea of our approach is to enable program behaviour to be speciﬁed directly in terms
of notions of resource relevant to the program. Resources in our methodology are conceptually
a pair of a resource type and a resource amount (an integer). Resource types are organised into
parameterised resource kinds: a named resource constructor with ﬁxed arity (possibly zero) and
corresponding parameter types; each instantiation of these parameters yields a distinct resource
type. Any value that can be checked for equality and represented in the speciﬁcation syntax can
be used as a parameter to a resource constructor. For example, we might use a resource kind
Money with a single parameter of type AcctId to represent currency known to be deposited in the
corresponding bank account.
   In our Prusti implementation, such a resource kind is declared as a Rust struct annotated with
a #[resource_kind] tag, listing its parameter types; resource types are denoted by instantiating

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                        1:7


the struct with appropriate (Rust) expressions. For example, we can declare a resource constructor
for the amount of money belonging to a particular account as follows:
 1    #[resource_kind] struct Money(AcctId);
Resources of the same type are always aggregated to the sum of their amounts, and resources of
diﬀerent types are incomparable. In our example, the fact that for two diﬀerent account IDs id1
and id2, the corresponding resource types Money(id1) and Money(id2) are diﬀerent encodes the
property that money in diﬀerent accounts should not be fungible; withdrawing money from your
account should have a meaning distinct from withdrawing from someone else’s!
  We use the syntax resource(rtype, amt) to denote resources, where rtype is a resource type,
and amt is the amount. For example, the expression resource(Money(a_id), amt) refers to an
amount amt of money for the account associated with the identiﬁer a_id.

3.1    Resource Operations

 1    struct BankImpl { map: HashMap<AcctId, u128> };
 2    impl Bank for BankImpl {
 3      fn balance(&self, acct_id: AcctId) -> u128 {
 4        self.map.get(acct_id).unwrap_or(0) // 0 returned if no entry in map
 5      }
 6      fn deposit(&mut self, acct_id: AcctId, amt: u128) {
 7        let bal = self.balance(acct_id); self.map.insert(acct_id, bal + amt);
 8        produce!(resource(Money(acct_id), amt));
 9      }
10      fn withdraw(&mut self, acct_id: AcctId, amt: u128) {
11        let bal = self.balance(acct_id); self.map.insert(acct_id, bal - amt);
12        consume!(resource(Money(acct_id), amt));
13      }
14    }

Fig. 7. Rust code defining a BankImpl struct and implementation of banking operations. Account balances
are stored in a HashMap mapping AcctIds to u128 values; deposits and withdrawals update the map entries.
The produce! statement in deposit denotes the creation of the resource representing amt units of money
for account acct_id, the consume! statement in withdraw denotes its destruction.

    Conceptually, each stack frame owns a collection of resources. Our methodology deﬁnes three
resource operations: resources can be created (added to a stack frame), destroyed (removed from a
stack frame), and transferred (between stack frames, at call and return sites). We denote creation
and destruction by produce! and consume! respectively, they would appear e.g. in an implemen-
tation of the Bank trait (Fig. 7). In our Bank example, using the resource type Money(acct_id) to
represent deposited currency, deposits create this resource and withdrawals destroy it. Intuitively,
it is only possible to destroy a resource if it is currently held: our methodology requires that the
resource resource(Money(acct_id), amt) is available to destroy at the point of the consume!
inside withdraw (otherwise veriﬁcation will fail).
    Each function call performs a transfer of resources based on the callee’s speciﬁcation: concep-
tually, the resources in a callee’s precondition are transferred to it from its caller, and it returns
to the caller the resources in its postcondition. The Bank trait would be speciﬁed as in Fig. 8:
Bank.deposit returns an amount amt of the resource Money(acct_id)to the caller, Bank.withdraw
requires the caller to provide it.

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:8                                                                       Zachary Grannan and Alexander J. Summers


 1    trait Bank {
 2      fn balance(&self, acct_id: AcctId) -> u128;
 3
 4        #[ensures(resource(Money(acct_id), amt))]
 5        fn deposit(&mut self, acct_id: AcctId, amt: u128);
 6
 7        #[requires(resource(Money(acct_id), amt))]
 8        fn withdraw(&mut self, acct_id: AcctId, amt: u128);
 9    }

                  Fig. 8. The specification of Bank, described in terms of the resource Money.

3.2       Resource State
Our methodology associates every stack frame with a resource state, tracking the resources cur-
rently held by the function invocation. This is ghost state; we use it as a concept for static reason-
ing about the program only, but it need not (and will not) actually exist at runtime. A resource
state is a map from resource types to resource amounts, and resource operations are interpreted
with respect to the current resource state. Creation of a resource increases the corresponding map
entry, while destruction decreases it. Destruction operations entail a proof obligation: we need to
prove that suﬃcient resource is held before it is destroyed, otherwise a veriﬁcation error is raised.
   Resources are transferred between stack frames at call (and return) sites. The resource state of
each frame is initialised with only the resources transferred to it from its caller, according to the
callee’s precondition. Resources in the callee’s postcondition are those it transfers back to its caller.
Transfers also entail proof obligations: the veriﬁer must prove that the resources transferred away
are actually held. This model of resource state is suitable for modular veriﬁcation: each function’s
initial resource state is determined purely by its precondition, independently of call site.

3.3       Resource State Expressions
The speciﬁcations presented in Fig. 8 suﬃce to characterise the behaviour of the program in terms
of its resource operations. Reifying these resource transfers makes some important properties of
the program clearer: e.g. it is impossible to overdraw an account because withdrawals require a
resource representing at least part of the current balance (see Fig. 9).


 1    fn bad<B: Bank>(bank: &mut B, acct_id: AcctId, amt: u128) {
 2      bank.deposit(acct_id, amt); bank.withdraw(acct_id, amt);
 3      bank.withdraw(acct_id, amt); // ERROR: insufficient permission to resource
 4    }


Fig. 9. An example program that would not verify after annotating Bank with resource operations. The
first withdraw() is permitted, because suﬀicient resource Money(acct_id) is made available by the pre-
ceding deposit() call. A verification error is raised because there is no resource available for the second
withdraw().


   However, our resource speciﬁcations so far are completely independent of the actual program
state used to track resources. In particular, there is no speciﬁed relationship between resource
operations and Bank.balance() calls. Working towards this, we introduce resource state expres-
sions, which are used inside speciﬁcations to introspect on the resource state. These expressions

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                        1:9


 1   #[requires(resource(Money(a), 1))] // holds(Money(a)) == 1 1
 2   #[requires(resource(Money(a), 1))] // holds(Money(a)) == 2 2
 3   #[ensures(old(holds(Money(a))) == 2)]                       3
 4   #[ensures(holds(Money(a)) == 0)]                            4
 5   #[ensures(resource(Money(a), 1))] // holds(Money(a)) == 1 5
 6   fn take2return1<B: Bank>(bank: &mut B, a:AcctId){ bank.withdraw(a, 1); }
 7

 8   #[requires(resource(Money(a),3))]
 9   fn client<B: Bank>(bank: &mut B, a: AcctId){ take2return1(bank, a); }

Fig. 10. A program demonstrating resource operations and resource state expressions in specifications. The
function take2return1 requires 2 units of Money(a) from the caller and returns 1 unit.

are written holds(rtype), and (when used outside of function speciﬁcations e.g. as inline asser-
tions) denote the amount of resource type rtype held in the current resource state. For example,
holds(Money(acct_id)) denotes the amount of acct_id’s money in the current state.
   When holds is used in function speciﬁcations, we deﬁne its semantics diﬀerently, consider-
ing the fact that the caller and callee resource states may diﬀer. In such positions, our technique
interprets holds() expressions with respect to the amount of resource transferred so far by the
corresponding pre-/post-condition; this notion has the same meaning for both caller and callee.
   Fig. 10 illustrates this semantics. The ﬁrst precondition #[requires(resource(Money(a), 1))]
at line 1 speciﬁes a resource to be transferred from caller to callee. As that is the only resource
transferred so far, the (commented) assertion holds(Money(a)) == 1 holds at 1 . The subsequent
line speciﬁes the same resource transfer again, resulting in holds(Money(a)) == 2 ( 2 ).
   The ﬁrst postcondition old(holds(Money(a))) == 2) at 3 concerns (via old) the amount of
Money(a) transferred from the caller (this refers to the overall transfers made by the preconditions
together), while the second ( 4 ) states that no money has been transferred by the postconditions
up to this point. At 5 , located after the postcondition transferring resource(Money(a),1) to the
caller, the commented assertion holds(Money(a)) == 1 would instead be true.



3.4 Coupling Invariants
Finally, we use our resource state expressions to deﬁne connections between the resource state
and the actual program state. In our methodology, users declare coupling invariants to deﬁne these
connections. Coupling invariants are two-state expressions (using old to describe the prior state,
as in a postcondition) that relate the program and resource states at two points in the program;
these invariants are enforced at function return sites. Coupling invariants are expressed using
annotations of the form #[invariant_twostate(𝑡)], where 𝑡 is an expression that can include
speciﬁcation constructs such as holds() and old() expressions. Although declared once per type,
a coupling invariant 𝑡 is interpreted as an additional, implicit postcondition on every function
taking a mutable reference to this type as a parameter; eﬀectively, it is equivalent to adding the
postcondition #[ensures(𝑡)] to all such functions (this happens implicitly).
   The expressive power of coupling invariants stems from their ability to refer to the change in
resource state that occurs within a function (i.e., the diﬀerence between the resources it produces
and those it consumes), and relate it to a corresponding change in program state. While coupling
invariants only consider the function’s local resource state, with program state notionally repre-
senting the global amount of resources, we observe that the change in the amount of a resource is


                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:10                                                                       Zachary Grannan and Alexander J. Summers


 1     #[invariant_twostate(forall(|a_id: AcctId|
 2       holds(Money(a_id)) - old(holds(Money(a_id))) ==
 3       self.balance(a_id) - old(self.balance(a_id))))]

Fig. 11. A coupling invariant for the Bank struct, which is enforced between the beginning (via old) and end
of each function involving a mutable reference to a Bank.
            Coupling Invariant                           deposit() Speciﬁcation (Fig. 8)
              Shown in Fig. 11             Pre:      <none>
                                           Post:     #[ensures(resource(Money(acct_id), amt))]


                                                Resource Transfers Denoted by Speciﬁcation
                                                   Transferred In:    𝜖
                                                   Transferred Out:   {Money(acct_id) → amt}


                                                    View of Resource Transfers via holds()
                                      Before:   ∀a_id . old(holds(Money(a_id)))
                                                                             ( =0
                                                                              amt if a_id = acct_id
                                      After:    ∀a_id . holds(Money(a_id)) =
                                                                              0   otherwise


                                    Automatically Derived Postcondition for deposit() (c.f. Fig. 2)
                                                                              (
                                                                                amt if a_id = acct_id
                                 ∀a_id . balance(a_id) = old(balance(a_id)) +
                                                                                0   otherwise

Fig. 12. A diagram indicating how the coupling invariant from Fig. 11 combines with resource operations of
deposit() (Fig. 8) to derive a postcondition specifying the eﬀect deposit() has on the value of balance().
The derived postcondition is equivalent to the manually written postcondition of Fig. 2.

the same regardless of whether we consider all of the resources in a program, or just those avail-
able locally. Exploiting this property, coupling invariants enable assertions on program states to
be derived from (the aggregate of) a function’s resource operations.
   Fig. 11 shows a suitable coupling invariant for our Bank struct. It states that (across each func-
tion it applies to) the change in the value of balance(a_id) should correspond to the change
in resource Money(a_id) for all account identiﬁers a_id. To demonstrate the implications of this
invariant, we can consider how it applies to the deposit function (depicted graphically in Fig. 12).
   The function’s speciﬁcations using resource assertions prescribe the resources to be trans-
ferred into and out of the function call; in this example, none for the (empty) precondition and
resource(Money(acct_id), amt) for the postcondition. This is elaborated (automatically) to a
complete pointwise speciﬁcation of the eﬀects on all resource types, making explicit the cases of no
transfer via e.g. holds(Money(a_id) == 0) constraints. By conjoining the coupling invariant, this
logically implies a precise speciﬁcation relating the values of balance calls between the pre-state
and post-state; exactly the complex postcondition that had to be written manually for deposit
in Fig. 2. The combination of our novel resource speciﬁcations describing only the eﬀects that do
happen, our native resource semantics and an appropriate coupling invariant, results implicitly in
a logically-equivalent speciﬁcation expressed much more simply.
   Coupling invariants apply to all functions that take a (mutable) reference to a Bank (in particular,
they cannot be forgotten/ignored for a function; they deﬁne a constraint on operations on this
type in general). Fig. 13 shows the speciﬁcations for the transfer function implemented using

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                          1:11


our methodology; unlike the original version in Fig. 3, the speciﬁcation does not require explicit
frame conditions, and (with the exception of the extra precondition from != to) is a simple
composition of the corresponding speciﬁcations of withdraw and deposit from Fig. 8. Important
resource notions such as non-duplicability and a notion of resource amount are built-in: in short,
our new methodology addresses the three main speciﬁcation issues detailed in Sec. 2.


 1   #[requires(from != to)]
 2   #[requires(resource(Money(from), amt))]
 3   #[ensures(resource(Money(to), amt))]
 4   fn transfer<B: Bank>(bank: &mut B, from: AcctId, to: AcctId, amt: u128) { ... }

             Fig. 13. The specification of transfer(), described in terms of the resource Money.


  We note that the coupling invariants in our methodology are more lightweight than classical
type invariants, or invariants in substructural logics such as Iris [Jung et al. 2015]; they are not
required to be transitive or reﬂexive. Furthermore, they are not required to hold (and cannot be
assumed) within a function body. Rather, our invariants are interpreted simply as postconditions
on aﬀected functions and can be elaborated via a straightforward syntactic translation.
  The coupling invariants in our methodology depend on the function speciﬁcations summarising
the overall eﬀect of their function’s resource operations. Therefore, to extend our methodology to
support a concurrency model where resources can be transferred between threads, such transfers
would need to be encoded in the function speciﬁcation. Otherwise, if a resource appeared to be
destroyed (when in fact it was transferred), the coupling invariant would require a change to
program state that could not be justiﬁed. We expect that extending our methodology to support
such operations would be straightforward.

4 IMPLEMENTATION
We implemented our veriﬁcation technique as an extension of the Rust program veriﬁer Prusti.
Prusti veriﬁes Rust code by encoding the program and speciﬁcations into the intermediate veri-
ﬁcation language Viper [Müller et al. 2016], which supports permission-based reasoning using a
variant of implicit dynamic frames [Smans et al. 2009]. Although Prusti does not allow users to
directly access Viper’s permission primitives in speciﬁcations, it uses Viper permissions to encode
the guarantees provided by Rust’s ownership model; this enables heap framing without requir-
ing user annotations. Our methodology uses Viper’s permission-based reasoning capabilities to
extend Prusti with support for our novel resource reasoning technique.
   We note that our methodology is not speciﬁc to Rust or Viper. In particular, although the Rust
borrow-checker enables automatic coarse-grained framing of the heap, our methodology does not
assume these properties. Rather, this implementation demonstrates our methodology’s ability to
layer user-deﬁned resources on top of this existing coarse-grained framing.
   Although the usage of Viper’s resource primitives simpliﬁes our implementation, our method-
ology does not require resources to be available in the underlying program logic. Viper tracks re-
sources implicitly and transfers them via proof steps; however, this could also be done in e.g. Dafny
by tracking resources explicitly with a mutable map 2 . These two representations of resources have
been shown to be equivalent for traditional separation logics [Parkinson and Summers 2012].

2 In fact, the Viper veriﬁer Carbon performs such a translation to Boogie.



                                  Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:12                                                                      Zachary Grannan and Alexander J. Summers


4.1 The Viper Intermediate Verification Language
Viper is an imperative intermediate veriﬁcation language, in the spirit of Boogie [Leino 2008] and
Why3 [Bobot et al. 2011]. Program veriﬁers are built to translate source language (in our case,
Rust) veriﬁcation problems into Viper programs, which can then be checked by a Viper veriﬁer.
   A Viper program consists of a set of methods; Viper methods (whose bodies are statements) are
similar to functions in an imperative language. Viper statements include variable assignments and
method calls, as well as assume and assert statements that are interpreted in the standard way.
Viper also includes label statements: the statement label 𝑙 associates the point in the method
where the statement appears with the label 𝑙. The labels are used in Viper’s old expressions: the
expression old[𝑙](𝑒) refers to the value of the expression 𝑒 at the program point 𝑙.
   Viper supports separation-logic style reasoning: its language and logic has its own notion of
resource state, used to track a variety of resource assertions [Müller et al. 2016]. For the purposes
of this paper, the only relevant Viper resources are abstract predicate instances. Viper allows the
declaration of custom abstract predicates using the syntax predicate 𝑃 (𝑥 1 : 𝑇1 , . . . , 𝑥𝑛 : 𝑇𝑛 ), where
𝑃 is the predicate name, and 𝑥 1 : 𝑇1 , . . . , 𝑥𝑛 : 𝑇𝑛 are the names and types of its arguments. Each
instantiation 𝑃 (𝑒 1 , . . . , 𝑒𝑛 ) of the predicate is treated as a type of resource to be tracked.
   Expressions acc(𝑝, amt) denote an amount amt of the predicate instantiation 𝑝. Viper state-
ments inhale 𝑒 and exhale 𝑒 add/remove resources described by acc expressions in 𝑒; for non-
resource expressions they behave as assume/assert statements. Removing (via exhale) resources
not in the state causes a veriﬁcation error. Viper also supports perm() expressions that query an
amount of resource: an expression perm(𝑝) refers to the amount of the predicate instantiation 𝑝.

4.2    Encoding of Resources into Viper
An overview of our translation from our resource speciﬁcations into Viper is shown in Fig. 14.
The (overloaded) syntax ÈÉ denotes the translation of Prusti declarations, Rust statements, and
Rust types into Viper. We omit the translation of types, which is unchanged from the prior Prusti
encoding [Astrauskas et al. 2019]. Prusti’s encoding of pre-existing features is unchanged, except
for adding additional label statements (used for encoding our holds() expressions).
   The syntax ÈÉ 𝑜𝑐 denotes the encoding of a Prusti expression in the context 𝑐, 𝑜. The context
changes the way that holds() expressions are translated into Viper. The ﬁrst element, 𝑐, represents
the current context: either no label 𝜖, or a signed label -𝑙 or +𝑙 (denoting whether we are currently
removing or adding resources). The second element, 𝑜, represents the old context taking the form
of either old(𝑙) or cur(𝑙). These contexts prescribe where (with respect to which existing label)
generated perm() expressions should be evaluated and how they should be composed. For example,
the context +𝑙 ′ , old(𝑙), is used to encode old(holds()) expressions that occur in the postcondition
of a called function, and are computed by taking the diﬀerence of the perm() expressions taken
before and after exhaling the function precondition, corresponding to labels 𝑙 and 𝑙 ′ respectively.
4.2.1 Resources and Resource Operations. As described previously, resource types (via their Re-
source constructors) are declared in Prusti as a Rust struct, annotated with the tag #[resource_kind].
We encode resource constructors as abstract predicates in Viper; the ﬁelds of the struct are encoded
as the arguments to the abstract predicate. We chose this encoding because abstract predicates in
Viper are used to model resources in Viper’s resource model. Accordingly, we translate resource()
expressions directly into acc() expressions in Viper. Our produce! and consume! statements are
encoded as inhale and exhale statements in Viper; these provide our desired semantics directly.
   holds() expressions in the body of a Rust function are encoded as perm() expressions in Viper.
However, as described in Sec. 3.3, our holds() expressions have a diﬀerent semantics in pre-
/post-conditions (while Viper’s perm() expressions do not). Encoding our semantics requires a

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                                                         1:13

Declarations
 È#[resource_kind] struct 𝑅(𝑇1, . . . , 𝑇𝑛 ); É                              predicate 𝑅(arg1 : È𝑇1 É , . . . , argn : È𝑇𝑛 É )

                                                                            method 𝑓 (𝑥 1 : È𝑇1 É , . . . , 𝑥𝑛 : È𝑇𝑛 É ){
                                                                                               cur(𝑙 )
   #[requires(𝑓pre )]                                                        inhale 𝑓𝑝𝑟𝑒 𝜖 𝜖 ; label pre;
  #[ensures(𝑓post )]                                                       È𝑠 1 É ; . . . ; È𝑠𝑚 É
                                                                                                                 cur(pre)
   fn 𝑓 (𝑥 1 : 𝑇1, . . . , 𝑥𝑛 : 𝑇𝑛 ) {𝑠 1 ; . . . ; 𝑠𝑚 }
                                                                                                           
                                                                             label post; exhale 𝑓𝑝𝑜𝑠𝑡 -post
                                                                            }
Statements
                                                  cur(pre)                                                             cur(pre)
 Èproduce!(𝑡); É               inhale È𝑡É 𝜖                            Èconsume!(𝑡); É                 exhale È𝑡É 𝜖
                                                                                          cur(𝑙 )
                                 label 𝑙 pre; exhale 𝑓pre [𝑥 1 := 𝑡 1 , . . . , 𝑥𝑛 := 𝑡𝑛 ] -𝑙 𝜖
                                                                                              pre
 È𝑓 (𝑡 1, . . . , 𝑡𝑛 ); É                                                                    cur(𝑙 )
                                 label 𝑙 post ; inhale 𝑓post [𝑥 1 := 𝑡 1, . . . , 𝑥𝑛 := 𝑡𝑛 ] +𝑙 pre
                                                       
                                                                                                                post


Expressions
               cur(𝑙 )            old(𝑙 )
 Èold(𝑡)É 𝑐                  È𝑡É 𝑐
 È𝑅(𝑡 1, . . . , 𝑡𝑛 )É 𝑜𝑐     𝑅(È𝑡 1 É 𝑜𝑐 , . . . , È𝑡𝑛 É 𝑜𝑐 )             Èresource(𝑟, 𝑡)É 𝑜𝑐             acc(È𝑟 É 𝑜𝑐 , È𝑡É 𝑜𝑐 )
                   cur(𝑙 )                     cur(𝑙 )                                   old(𝑙 )                                    old(𝑙 )
 Èholds(𝑟 )É 𝜖                  perm(È𝑟 É 𝜖              )                 Èholds(𝑟 )É 𝜖                old[𝑙](perm(È𝑟 É 𝜖                    ))
                   cur(𝑙 )                      cur(𝑙 )                                    cur(𝑙 )
 Èholds(𝑟 )É +𝑙 ′               perm( È𝑟 É 𝜖              ) - old[𝑙 ′ ](perm( È𝑟 É 𝜖                 ))
             old(𝑙 )                               old(𝑙 )                           old(𝑙 )
 Èholds(𝑟 )É +𝑙 ′                old[𝑙](perm( È𝑟 É 𝜖       )) - old[𝑙 ′ ](perm( È𝑟 É 𝜖       ))
                   cur(𝑙 )                                       cur(𝑙 )                     cur(𝑙 )
 Èholds(𝑟 )É -𝑙 ′               old[𝑙 ′ ](perm( È𝑟 É 𝜖                     )) - perm( È𝑟 É 𝜖           )
             old(𝑙 )                              old(𝑙 )
 Èholds(𝑟 )É -𝑙 ′               old[𝑙](perm( È𝑟 É 𝜖       ))
Fig. 14. Encoding of Prusti resource constructs into Viper. Labels 𝑙 pre and 𝑙 post are assumed to be fresh. The
label 𝑙𝜖 denotes an arbitrary fresh label that is never referenced, i.e., a placeholder label used where old
expressions are not permitted.

more-complex translation, using the contexts on our translation function to calculate the correct
diﬀerences between perm() expressions at diﬀerent points in the program.


4.3 Coupling Invariants and Reborrowing
We directly encode coupling invariants (declared with #[invariant_twostate(𝑡)] annotations
on Rust structs) as postconditions on the corresponding translated Viper methods. One restric-
tion of our current methodology is that we do not support Rust functions that reborrow mutable
references, returning to the caller a live mutable reference to e.g. the internals of the Bank. An
example of such a function is shown in Fig. 15, where a mutable references to one of the balances
is handed out to the caller. Technically, this requires that the client code would become responsible
for maintaining the Bank’s two-state invariant. For untrusted client code (such as smart contracts
running on a blockchain infrastructure), this should not be relied upon, and rejecting such func-
tions (as we currently do) is the right approach. A similar issue and its solution has been discussed
in the context of single-state invariants for Prusti [Astrauskas et al. 2022]. However, for trusted
client code (e.g. other veriﬁed layers of the same software stack), we believe an adaptation of this
idea to support reborrowing with our two-state invariants, as future work (it remains to consider
exactly which pairs of states we would use to enforce our two-state invariants in a potential exten-
sion). This feature has not been needed in practice when applying our methodology to examples


                                            Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:14                                                                      Zachary Grannan and Alexander J. Summers


    1   struct Bank { balances: HashMap<AcctId, u32> }
    2   impl Bank {
    3     fn get_balance_ref(&mut self, acct_id: AcctId) -> &mut u32 {
    4       self.balances.get_mut(acct_id).unwrap()
    5     }
    6   }

Fig. 15. A function that performs a reborrow. The variable self is inaccessible at the end of the function
call and the returned reference can modify its internal state; the Bank’s two-state invariant cannot yet be
re-established.

(likely because this additional reliance on client code for correctness is often not desirable for such
programs).
   With this encoding in place (and implemented), we can verify Rust code speciﬁed in our method-
ology directly and automatically, as we evaluate in the following sections.

5       CASE STUDY
In this case study, we take the core of a Rust implementation [Informal Systems Inc. and ibc-rs authors
2022] of a cryptocurrency token transfer application running on the Interblockchain Communica-
tion Protocol (IBC) [Goes 2020]. The token transfer application enables tokens to be sent from one
blockchain to another, without the need for a trusted intermediary; a bug in the application could
inadvertently cause tokens to be destroyed or duplicated.

5.1 The Fungible Token Transfer Application
The IBC token transfer speciﬁcation allows tokens to be sent between blockchains with diﬀerent
implementations and consensus mechanisms. Its design requires that each chain track token own-
ership for accounts on the chain, but not for those on other chains. The application has access to
a ledger on each chain; allowing it to mint and burn tokens for arbitrary accounts on that chain.
It “transfers” a token between chains by making ledger updates on both chains.
   A naïve token transfer implementation could operate by destroying the tokens on one chain
and creating them on another. However, the naïve approach has two issues. First, a chain may
not have the capacity to mint some kinds of tokens, i.e., tokens with ﬁxed supply. Second, this
approach would allow an exploit allowing unrestricted minting of a token on one compromised
chain to allow obtaining an arbitrary amount of that token on any connected chain. In particular,
if a chain 𝐴 had a vulnerability allowing malicious arbitrary minting, an attacker could mint on 𝐴
a token that exists on chain 𝐵, and then transfer it to chain 𝐵.
   Instead, the fungible token transfer application performs a token transfer from chain 𝐴 to chain
𝐵 by ﬁrst sending the token to a special escrow account on chain 𝐴, and then minting a voucher
token on chain 𝐵 (shown in Fig. 16a). The denomination of the voucher token is created by preﬁxing
the denomination of 𝐴’s token with the identiﬁer of the channel connecting the two chains.
   Intuitively, the voucher token on 𝐵 corresponds to the escrowed token on 𝐴. In particular, when
the application transfers the voucher token back to 𝐴, it is burned on chain 𝐵, and the tokens in
the escrow account in chain 𝐴 are sent to the recipient (as shown in Fig. 16b). The advantage of
this design is that it does not require the token transfer application to mint or burn native (i.e.,
non-voucher) tokens. Because this design ensures that native tokens are never minted, exploits on
one chain cannot use the protocol to inﬂate the supply of native tokens on other chains.
   When a voucher token is transferred to a chain other than its originating chain, it is treated the
same as any other token. This enables tokens to be transferred transitively across multiple chains.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                       1:15


             Chain 𝐴                 Chain 𝐵                   Chain 𝐵                  Chain 𝐴

                 𝑡                                                                           𝑡
             escrow𝐵                                                                     escrow𝐵 unescrow
escrow
                                         𝑡′                       𝑡′
                 𝑡                                                                           𝑡
                                        dest
                                               mint             source burn
              source                                                                       dest
(a) Operations performed when sending a native           (b) Operations performed when sending a voucher
token on 𝐴 to another chain 𝐵. The token is es-          token back to its originating chain. The voucher is
crowed on 𝐴 and a voucher is minted on 𝐵.                burned on 𝐵 and the native token is unescrowed on
                                                         𝐴.
                            Fig. 16. Operations of the Token Transfer Application.
 1   struct PrefixedDenom {trace_path: TracePath, base_denom: BaseDenom}
 2   struct PrefixedCoin {denom: PrefixedDenom, amount: u32}
 3   trait BankKeeper {
 4     fn send_tokens(&mut self, from: AccountId, to: AccountId, coin: PrefixedCoin);
 5     fn burn_tokens(&mut self, from: AccountId, coin: PrefixedCoin);
 6     fn mint_tokens(&mut self, to: AccountId, coin: PrefixedCoin);
 7   }

                                      Fig. 17. The BankKeeper interface

For example, suppose 𝐴, 𝐵 and 𝐶 are blockchains, and 𝐵 is connected to both 𝐴 and 𝐶. Then, a token
on 𝐴 can be sent to 𝐶 by ﬁrst making a transfer from 𝐴 to 𝐵, and sending the voucher minted on
𝐵 to 𝐶. 𝐶 ends up with a voucher for the token on 𝐵, which itself is a voucher for the token on 𝐴.

5.2 Application Architecture
The token transfer application is deﬁned with respect to the BankKeeper trait shown in Fig. 17.
The application uses the BankKeeper to manage the ledger on a particular chain; transfers are
accomplished by interacting with instances of the BankKeeper trait on both chains.
   The struct AccountId identiﬁes an account; within BankKeeper these refer to local accounts
(not those on other chains). The struct PrefixedCoin consists of a token denomination and an
integer amount; this type is used in the bank interface to specify which token should be minted,
burned, or transferred. The struct PrefixedDenom refers to a token denomination: base_denom is
the name of the token on the originating chain, and trace_path denotes the sequence of token
transfers necessary to exchange a token of this denomination with the one on its original chain.

5.3 Properties of the Fungible Token Transfer Application
For our case study, we focused on verifying two key properties of the token transfer application.
We decided on the properties based on suggestions from collaborators at Informal Systems (re-
sponsible for the code). The properties are as follows:
     • Two-Way Peg: After transferring a token from one chain to another, it should be possible
       to send the token back to the original account. Performing this round-trip token transfer
       should not result in any balance changes on either chain.
     • Preservation of Supply: For any given native token, the sum of the native token (excluding
       tokens in escrow accounts) and all derived voucher tokens should remain constant.

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:16                                                                      Zachary Grannan and Alexander J. Summers


   These properties originate from the IBC speciﬁcation [Goes 2022], although the two-way peg
property we consider is stronger than the version in the original speciﬁcation. To verify the imple-
mentation, it was necessary to make some changes to the code in order to workaround limitations
of Prusti. For example, the TracePath data structure is implemented using data structures that
are not fully supported by Prusti; therefore, we simpliﬁed the deﬁnitions of such types. However,
these changes are orthogonal to our veriﬁcation methodology.
   The token transfer application relies on an implementation of the IBC core standards [IBC Standards Commi
2023] to coordinate communication across chains. We assume the correctness of this implementa-
tion, as veriﬁcation of these aspects would likely not beneﬁt from our resource reasoning method-
ology.

5.4 Encoding the Specification with Resources
We present our speciﬁcation by ﬁrst explaining the resource types that are used to model the
resources in the program (Sec. 5.4.1). We then demonstrate the speciﬁcations for the BankKeeper
(Sec. 5.4.2) and constituent functions of the token-transfer application (Sec. 5.4.3). In Sec. 5.4.4 we
present the speciﬁcations used to verify the properties.
5.4.1 Representing Tokens with Resource Types. We begin our presentation by identifying appro-
priate resource types for use in speciﬁcations. First, we note that the two properties above refer to
diﬀerent aspects of tokens: the two-way peg property is concerned with the tokens in each account,
while the preservation of supply considers the sum of unescrowed tokens across all accounts. The
latter property does not distinguish between native and voucher tokens; however, this distinction
is relevant for the former. Therefore, we deﬁne two diﬀerent resource constructors, each corre-
sponding to a diﬀerent aspect of the same tokens. We declare the ﬁrst constructor, which is used
to encode the two-way peg property, as follows:
 1     #[resource_kind] struct Money(BankID, AccountId, PrefixedDenom)
   Resources constructed using the constructor Money have distinct types if they belong to diﬀerent
banks, diﬀer in denomination, or have diﬀerent owners. We ensure the two-way peg property by
showing that round-trip transfers do not change the amount of Money in the resource state.
   Proving the second property requires showing that the total amount of all unescrowed tokens of
a particular base denomination remain unchanged. For this property, we use a diﬀerent resource
constructor, that treats tokens as having the same type when they are in the same bank and have
the same base denomination. We declare the constructor as follows:
 1     #[resource_kind] struct UnescrowedCoins(BankID, BaseDenom);
   As previously mentioned, each resource constructor corresponds to a diﬀerent view of the same
token. Therefore, operations on real tokens should aﬀect the corresponding resources for each view
in a uniform manner. Therefore, we can deﬁne a macro to describe these real-world operations in
terms of how they aﬀect each view of the resource; this macro simpliﬁes the speciﬁcation, since it
eliminates the need to write resource operations for each view separately.
   The resulting macro is presented in Fig. 18. The macro states that a transfer of a token should al-
ways move an instance of the Money resource constructor, but should only move the corresponding
UnescrowedCoins resource if the account $to is not an escrow account.
5.4.2 Specifying the BankKeeper. We use the transfer_money()!macro to annotate BankKeeper’s
associated functions with appropriate resource operations, as presented in Fig. 19.
   We then connect the resource operations to properties about the program state by establish-
ing coupling invariants on the BankKeeper function, which describe how changes to Money and

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                          1:17


 1   macro_rules! transfer_money { ($bank_id:expr, $to:expr, $coin:expr) => {
 2      resource(Money($bank_id, $to, $coin.denom), $coin.amount) &&
 3      if !is_escrow_account($to) {
 4        resource(UnescrowedCoins($bank_id, $coin.denom.base_denom), $coin.amount)
 5      } else { true }
 6   }}

Fig. 18. A macro that specifies what Prusti resources are changed (i.e., either created or destroyed) in re-
sponse to token operations. An operation on tokens will always change the Money resource, and also changes
the UnescrowedCoins resource if the target account is not an escrow account.
 1   trait BankKeeper {
 2     #[requires(transfer_money!(self.id(), from, coin))]
 3     #[ensures(transfer_money!(self.id(), to, coin))]
 4     fn send_tokens(&mut self, from: AccountId, to: AccountId, coin: PrefixedCoin);
 5
 6       #[requires(transfer_money!(self.id(), from, coin))]
 7       fn burn_tokens(&mut self, from: AccountId, coin: PrefixedCoin);
 8
 9       #[ensures(transfer_money!(self.id(), to, coin))]
10       fn mint_tokens(&mut self, to: AccountId, coin: PrefixedCoin);
11   }

             Fig. 19. The BankKeeper trait annotated with the appropriate resource operations.
 1   #[invariant(forall(|acct_id: AccountId, denom: PrefixedDenom|
 2     holds(Money(self.id(), acct_id, denom)) -
 3     old(holds(Money(self.id(), acct_id, denom))) ==
 4     self.balance(acct_id, denom) - old(self.balance(acct_id, denom))))]
 5   #[invariant(forall(|coin: BaseDenom|
 6     holds(UnescrowedCoins(self.id(), coin)) -
 7     old(holds(UnescrowedCoins(self.id(), coin))) ==
 8     self.unescrowed_coin_balance(coin) - old(self.unescrowed_coin_balance(coin))))]

Fig. 20. Coupling invariants connecting the resources Money and UnescrowedCoins to the methods
balance() and unescrowed_coin_balance() respectively.

UnescrowedCoinsin the resource state correspond to changes in functions balance and unescrowed_coin_ba
respectively. These invariants are shown in Fig. 20.
5.4.3 Verifying the Application Logic. We now focus our attention to the logic of the token-transfer
application itself. The application performs a token transfer from a chain 𝐴 to chain 𝐵 in two steps.
The ﬁrst step is performed by calling the function send_fungible_tokens (Fig. 21) on chain 𝐴,
which disposes of the tokens on 𝐴 by either escrowing or burning them. In the second step, it
eﬀectively causes the function on_recv_packet to be called on chain 𝐵, which produces the tokens
by either minting or unescrowing tokens as necessary3 .
   Fig. 21 shows a speciﬁcation and implementation of the send_fungible_tokens function (we
simplify some details for presentation here), which performs the initial step in the cross-chain
3 Technically, on_recv_packet in the original version is a callback that is triggered when a relayer sends a message to

chain 𝐵, however for veriﬁcation we consider this as a regular function call. The routing of callbacks is implemented as
part of the IBC core standard, which we assume to be correct and do not attempt to verify.


                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:18                                                                      Zachary Grannan and Alexander J. Summers


 1     #[requires(transfer_money!(bank.id(), sender, coin))]
 2     #[ensures(!coin.denom.trace_path.starts_with(port, channel) ==>
 3         transfer_money!(bank.id(), escrow_address(channel), coin))]
 4     fn send_fungible_tokens<B: Bank>(bank: &mut B, coin: &PrefixedCoin,
 5       sender: AccountId, port: Port, channel: ChannelEnd) {
 6         if coin.denom.trace_path.starts_with(port, channel) { bank.burn(sender, coin);}
 7         else { bank.send(sender, escrow_address(channel), coin); }
 8     }

                              Fig. 21. The first step of the fungible token transfer.
 1     #[ensures(forall(|acct_id2: AccountId, denom: PrefixedDenom|
 2         bank1.balance(acct_id2, denom) == old(bank1).balance(acct_id2, denom)))]
 3     #[ensures(forall(|acct_id2: AccountId, denom: PrefixedDenom|
 4         bank2.balance(acct_id2, denom) == old(bank2).balance(acct_id2, denom)))]
 5     fn round_trip<B: Bank>(bank1: &mut B, bank2: &mut B, coin: &PrefixedCoin,
 6         sender: AccountId, receiver: AccountId, ...) { ... }

Fig. 22. The relevant specifications for the two-way peg property. The function round_trip() performs
a token transfer from account sender to receiver, and then performs the same transfer in the opposite
direction.
 1     #[ensures(forall(|c: BaseDenom|
 2           bank1.unescrowed_coin_balance(c) + bank2.unescrowed_coin_balance(c) ==
 3       old(bank1.unescrowed_coin_balance(c) + bank2.unescrowed_coin_balance(c))))]
 4     fn transfer<B: Bank>(bank1: &mut B, bank2: &mut B, coin: &PrefixedCoin,
 5         sender: AccountId, receiver: AccountId, ...) { ... }

Fig. 23. The relevant specifications for the supply preservation property. The function transfer() performs
a token transfer from account sender to receiver.

token transfer. The arguments port and channel identify the chain that tokens will be transferred
to. The condition on line 6 checks if the token being sent is a voucher for a token on that chain.
If so, then the voucher is burned on this chain (and the next step will unlock the corresponding
token on the other chain). Otherwise, the token is moved to an escrow account on this chain.
   The precondition of send_fungible_tokens speciﬁes that calling the function transfers the to-
ken out of the sender’s account. The postcondition states that when the token did not originate on
the opposite chain (i.e., the chain identiﬁed by port and channel), it will be transferred to the es-
crow account. Due to space constraints, we do not present the speciﬁcations of on_recv_packet()
here; the relevant speciﬁcation is available in our supplementary material [Anonymous Authors
2024].


5.4.4 Verifying the Desired Properties. With the above speciﬁcations, we can then prove that the
token transfer application satisﬁes the properties described in Sec. 5.3. To prove the two-way peg
property, we construct a method that performs a round trip token transfer, and show that the
balances of all accounts are unchanged after the transfer. The relevant speciﬁcations are presented
in Fig. 22 (the body of the method is omitted for brevity). We verify the preservation of supply
property by showing that the supply is preserved after an arbitrary transfer; the speciﬁcations are
presented in Fig. 23. The speciﬁcations of both properties are expressed in terms of the functions
balance and unescrowed_coin_balance respectively.


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                         1:19


  In conclusion, we’ve shown that our methodology can be applied to a real-world resource-
manipulating program. Using our methodology, we were able to prove two important properties
about the token-transfer application: that it maintains a two-way peg and preserves total token
supply. Our technique allows us to verify the desired properties in a straightforward manner by
describing resource operations directly, without having to write frame conditions.

6 EVALUATION
To evaluate our technique, we consider how speciﬁcations written using our methodology com-
pare to speciﬁcations written in terms of program states. We consider three research questions:
RQ1 (Conciseness): Are our speciﬁcations smaller than the alternative?
RQ2 (Complexity): Are our speciﬁcations (syntactically) simpler than the alternative?
RQ3 (Veriﬁcation Time): Do our speciﬁcations require more time to verify than the alternative?
  To answer these questions, we compare the speciﬁcations we developed in Sec. 5 to alternative
speciﬁcations for the same implementation, written without using our methodology. In addition,
we perform a similar comparative evaluation for three other programs:

IBC Non-Fungible Token (NFT) Transfer. The NFT transfer application [Xi 2022] has a similar ar-
chitecture to the token transfer application. We wrote the implementation ourselves, based on
pseudocode in the speciﬁcation. A key diﬀerence in the application of our methodology between
the two protocols is that we use resources to model the permission to change ownership of a token,
rather than modelling the token itself.

ERC-721 Implementation. We veriﬁed a smart contract implementing NFT functionality (satisfying
the ERC-721 speciﬁcation [Entriken et al. 2018]), written using the ink! library [Parity Technologies
2020]. This smart contract was written by the ink! developers, and is presented on the project’s
homepage as an example application4 . As in the NFT transfer application, we use resources to
model permissions. We also use resources to represent token balances (i.e. the number of tokens
owned by an account). In addition, the ERC-721 protocol allows an account to approve other ac-
counts to transfer their tokens on their behalf, and we use resources to represent such approvals
as well.

PSP-22 Implementation. Finally, we veriﬁed a smart contract, also written with ink!, that imple-
ments fungible token functionality on the Aleph Zero blockchain [Aleph Zero Foundation 2018].
As of February 2024, this contract was used by the Panorama Swap decentralised exchange [Panorama Swap De
2021]. Similar to the ERC-721 protocol, PSP-22 allows accounts to grant allowances to other ac-
counts, allowing them to spend their tokens, up to an allowed amount. In addition to using re-
sources to model token balances, we also use them to to model these allowances.
  In total, we wrote speciﬁcations for (and veriﬁed) all 31 resource-related functions across the
four applications. We note that it crucial for these functions to be correct: bugs in the functions
could result in a loss (or inﬂation) of the digital assets they manipulate. In fact, in the process of
performing the evaluation we identiﬁed a bug in the ERC-721 implementation that could incor-
rectly cause a user’s balance to be decremented (this bug caused veriﬁcation to fail, as expected).
We corrected the bug, and submitted a pull request to the developers, which was accepted5 .

4 https://use.ink/
5<Github PR link redacted for double-blind submission>. We also identiﬁed a separate bug unrelated to resources (but

necessary for veriﬁcation) where a panic could occur in this same codebase. The corresponding PR was accepted as well:
<Redacted>.


                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:20                                                                      Zachary Grannan and Alexander J. Summers


   The speciﬁcations and implementation for all applications included in our evaluation are in-
cluded in our supplementary material [Anonymous Authors 2024]. We now consider each research
question in order, and discuss our overall results in Sec. 6.4.

6.1    Conciseness
To measure conciseness, we compared the number of lines of code used to specify resource-related
operations in both speciﬁcations. Speciﬁcation lines unrelated to resource operations are identical
in both versions and therefore are not considered in the comparison. Our results are presented
in Table 1. On average, speciﬁcations encoded using resource reasoning require 48% fewer lines
of code compared to the alternative speciﬁcation without resources. Of the 31 functions, using
resource speciﬁcations required fewer lines of code for 25 and the same number of lines for 3.
   Resource speciﬁcations required more lines of code for the remaining three functions. These
functions were part of the NFT transfer application, where resources describe permission to mod-
ify ownership of an NFT, rather than NFT ownership directly. Therefore, it is also necessary to
describe how the ownership changes, i.e. specifying which account becomes the new owner of the
token. As a result, these tokens must be referred to twice in the speciﬁcation with resources, but
only once in the speciﬁcation without resources. Because the application allows transferring mul-
tiple NFTs at once, specifying the tokens that are transferred by a function requires more complex
speciﬁcations than in the other speciﬁcations. In this case, the overhead of specifying permissions
in the resource speciﬁcation outweighs the increased speciﬁcation length due to frame conditions
in the alternative version.
   To use resources in our speciﬁcations, we must deﬁne the resources themselves, as well as as-
sociated coupling invariants. Table 2 shows the lines of code required for resource annotations in
the examples we consider consider. We note that they are essentially a one-time cost, as they only
need to be written once, regardless of the number of functions in the program.

6.2 Syntactic Complexity
More concise speciﬁcations are not necessarily simpler or more desirable. For example, a longer
speciﬁcation may be preferable to a shorter one if the latter involves complex nesting of condition-
als, implications, and quantiﬁers. To evaluate syntactic complexity, we considered the AST nodes
of the (parsed) speciﬁcation expressions. We quantify the complexity of an AST based on the total
number of nodes it contains and its maximum depth. As shown in Table 1, the speciﬁcations writ-
ten using our methodology are syntactically simpler in most cases: of the 31 functions, 29 of them
have speciﬁcations with smaller AST depth in our methodology, 26 have smaller size. On average,
the speciﬁcation ASTs have a 41% smaller size and 38% smaller depth.

6.3    Verification Time
We compared the runtime of speciﬁcations written using our methodology to the alternate version.
For each version, we performed ﬁve runs, all runs were performed a 10-core Apple M1 Max. Our
results are presented in Table 3; overall, the speciﬁcations using resources were 35% slower than
those without.This is most likely due to two reasons. Currently, our encoding into Viper requires
type-casting between the types used to represent resource amounts (i.e., rational numbers) and
other numeric values in the code (e.g. token balances, which are represented using integers). As
future work, we could try to reduce the performance overhead associated with such casts.
   Second, in some cases, the postconditions derived from coupling invariants are less eﬃcient
to verify compared to speciﬁcations that would be written manually. In particular, for methods

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                       1:21


                                                    Without Resources                      With Resources
   Application      Usage
                                                   Size   Depth    # Lines   Size (Diﬀ.)   Depth (Diﬀ.)   # Lines (Diﬀ.)
                    burn()                         45        8       27       5 (-89%)       3 (-63%)        1 (-96%)
                    mint()                         37        8       26       5 (-86%)       3 (-63%)        1 (-96%)
                    send()                         136       11      36      10 (-93%)       3 (-73%)        2 (-94%)
 Token Transfer     send_fungible_tokens()         34        6       13      20 (-41%)       6 (-0%)         3 (-77%)
                    on_recv_packet()               45        6       19      20 (-56%)       5 (-17%)        6 (-68%)
                    send_preserves()               47        7       16      57 (+21%)       6 (-14%)        16 (-0%)
                    round_trip()                   53        6       19      44 (-17%)       5 (-17%)       15 (-21%)
                    burn()                         31        9       8        14 (-55%)       4 (-56%)       2 (-75%)
                    mint()                         39        9       9        22 (-44%)       4 (-56%)       3 (-67%)
                    transfer()                     33        9       8        22 (-33%)       4 (-56%)       3 (-63%)
  NFT Transfer      create_or_update_class()       16        7       4        0 (-100%)      0 (-100%)      0 (-100%)
                    send_nft()                     108       11      24      115 (+6%)        9 (-18%)       26 (+8%)
                    on_recv_packet()               185       13      45      206 (+11%)      11 (-15%)      52 (+16%)
                    round_trip()                   126       10      35      144 (+14%)       10 (-0%)       37 (+6%)
                    set_approval_for_all()         72        9       10       31 (-57%)      7 (-22%)        3 (-70%)
                    approve()                      66        9       10       28 (-58%)      5 (-44%)        5 (-50%)
                    transfer()                     110       12      17       98 (-11%)      9 (-25%)       14 (-18%)
                    transfer_from()                104       11      17        98 (-6%)      7 (-36%)       15 (-12%)
                    mint()                         88        10      13       46 (-48%)      7 (-30%)        5 (-62%)
                    burn()                         83        10      13       39 (-53%)      8 (-20%)        13 (-0%)
    ERC-721
                    transfer_token_from()          104       11      17      114 (+10%)      8 (-27%)       15 (-12%)
                    remove_token_from()            76        9       14       28 (-63%)      4 (-56%)        6 (-57%)
                    add_token_to()                 84        10      13       54 (-36%)      5 (-50%)        7 (-46%)
                    approve_for_all()              72        9       10       31 (-57%)      7 (-22%)        3 (-70%)
                    approve_for()                  66        9       10       34 (-48%)      5 (-44%)        6 (-40%)
                    clear_approval()               64        8       8        19 (-70%)      5 (-38%)        4 (-50%)
                    transfer()                     86        11      20      42 (-51%)       6 (-45%)        4 (-80%)
                    transfer_from()                161       11      40      111 (-31%)      8 (-27%)       19 (-53%)
     PSP-22         approve()                      49        9       14      43 (-12%)       5 (-44%)        14 (-0%)
                    increase_allowance()           51        9       10      20 (-61%)       5 (-44%)        4 (-60%)
                    decrease_allowance()           60        12      12      20 (-67%)       6 (-50%)        3 (-75%)
Table 1. Comparison between the lines of code and syntactic complexity of specifications written with and
without resources. Each column considers the specifications for the function in that row. Size refers to the
total number of nodes in the ASTs. Depth refers to the height of the tallest AST. # Lines is the count of lines
in the specification. The percentages in the (Diﬀ.) columns is the ratio of the corresponding value for the
specification written with resources to the value for the specification written without resources.

                        Application        Resource Deﬁnitions      Coupling Invariants
                        Token Transfer               9                        25
                        NFT Transfer                 6                        10
                        ERC-721                      4                        37
                        PSP-22                       2                        14
Table 2. The number of lines of code defining resource kinds and coupling invariants for each application.

that do not produce or consume any resources, coupling invariants will introduce postcondi-
tions in the form of pointwise assertions on the program state, asserting that everything is un-
changed. In contrast, the hand-written postcondition could potentially be simpler. For example,




                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:22                                                                      Zachary Grannan and Alexander J. Summers


                Application         Without Resources (mean / sd)       With Resources (mean / sd)
                Token Transfer                61.83s / 0.27s                    78.37s / 0.18s
                NFT Transfer                 123.05s / 1.70s                    140.34s / 0.09s
                ERC-721                       62.72s / 0.10s                    98.16s / 0.19s
                PSP-22                        36.24s / 0.26s                    51.51s / 0.09s
Table 3. Comparison of verification time for the specifications written in the diﬀerent styles. Results are
presented for five runs of the verifier.

in the case where a map balanceMap type tracks account balanceMap in an application, the post-
condition balanceMap == old(balanceMap) introduces less veriﬁcation overhead than the au-
tomatically generated invariant postcondition forall(|a: AcctId| balanceMap.get(a) ==
old(balanceMap.get(a))).

6.4 Analysis / Conclusion
Our evaluation shows that speciﬁcations written in our methodology compare favourably to spec-
iﬁcations written in terms of program states. Our speciﬁcations require fewer lines of code and
are syntactically simpler. Although our speciﬁcations require more time to verify, the increase in
time is a reasonable trade-oﬀ to make for the simpler speciﬁcations.
   We hypothesise that, in additional to being more concise and syntactically simpler, speciﬁcations
written using our methodology are easier to understand, because they leverage our common-sense
notion of resources. Evaluating this claim, e.g. via a user study, is a potential area of future work.

7      RELATED WORK
Eﬀect systems [Lucassen and Giﬀord 1988] extend a type system to include the side-eﬀects via
eﬀect types, which typically over-approximate the side-eﬀects an expression is allowed to perform.
Our resource speciﬁcations can be seen as similar to a kind of eﬀect, but are precise, and apply only
to changes to our ghost resource state. This distinction (and indirection via our coupling invariants)
is crucial to obtaining strong frame properties while still writing local speciﬁcations.
   Linear type systems [Wadler 1990] enable values to be treated as resources: values of a linear
must be used exactly once. Bounded linear types allows resource amounts to be modelled by a
semiring [Ghica and Smith 2014]. Tracking resource usage with linear types requires associating
resource amounts with values in the program, tracking resources in this way may require changes
to the program (consuming a resource must coincide with the disposal of a linearly-typed value,
for example). In contrast, our methodology is more ﬂexible, as resources are tracked via ghost
state.
   Separation logic [Reynolds 2002] enables veriﬁcation of heap-manipulating programs using lo-
cal reasoning: assertions describe only the relevant part of the heap, rather than the heap as
a whole. Our resource reasoning technique takes clear inspiration from this idea of local rea-
soning, although our technique intentionally avoids explicit resource reasoning about the con-
crete program state. Extensions of separation logic facilitate abstraction with user-deﬁned predi-
cates [Parkinson and Bierman 2005], but we note that an abstraction of our e.g. Bank interface via
abstract predicates would typically suﬀer from the same need for frame conditions about how the
internals change over a side-eﬀectful function. Our holds construct, which allows introspection on
the local resource state, does not have an analogue in separation logic. However, the Viper interme-
diate language [Müller et al. 2016] supports resource reasoning and resource introspection via the
perm() expressions explained in Sec. 4. In contrast to our holds construct, Viper’s perm() expres-
sions cannot be used directly in method pre- and postconditions in a generally-sound way; their
semantics is not consistent between how a caller and callee interpret their meaning [Müller et al.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                       1:23


2016]. Being an intermediate language, Viper provides features powerful enough to encode our
reasoning principles, but places the burden on the user to use these features soundly. In contrast,
our holds expressions can be used freely in pre- and post-conditions without fear of unsoundness,
and the trickier parts of our encoding (Sec. 4) take care of a correct mapping to Viper automatically.
   Iris [Jung et al. 2015] is a concurrent separation logic that allows user to deﬁne resources using
ghost state, and establish invariants that tie ghost and program state. While Iris is more expressive
than our approach (and potentially useful as a tool to prove its soundness), it is not clear how it
could be integrated into an existing program veriﬁer. In contrast, extending an existing program
veriﬁer with our methodology is straightforward due to our lightweight approach.
   There is substantial prior work focused on veriﬁcation of smart contracts themselves [Ahrendt and Bubel
2020][Bräm et al. 2021][Mohajerani et al. 2022]: while not the speciﬁc focus of our work, these are
clearly resource-manipulating programs (used to handle cryptocurrency assets). The veriﬁcation
tool 2Vyper [Bräm et al. 2021] is closest to our work: it provides its own resource reasoning via ef-
fect clauses for smart contracts in the Vyper language: these can specify possible resource transfers,
and users can also deﬁne invariants that connect the resource state to the runtime state. However,
there are several technical diﬀerences with our work: unlike our system, 2Vyper’s resource spec-
iﬁcations describe approximations (in the style of eﬀect systems) of a function’s behaviour, and
over representations of the entire resource state; there is no way to partition the resource state
into the local part that a function is concerned with, which is what eliminates heavyweight frame
conditions in our work.
   2Vyper’s eﬀect-clauses consist of a multiset of the operations that will occur in their execution,
but only refer to resource operations performed directly by the function : because 2Vyper consid-
ers interactions with unveriﬁed external code, it is impossible to reason in general about external
resource operations. In contrast, because we do not allow untrusted external calls, speciﬁcations
in our methodology eﬀectively summarise the resource operations that occur within a method call.
We have not applied our technique to verify interactions with untrusted code; doing so could be
interesting future work.
   Ahrendt and Bubel verify Solidity contracts with a proof technique centred around two-state
invariants [Ahrendt and Bubel 2020]. They show that diﬀerences between wei amounts (the built-in
currency) are powerful for expressing such invariants, similar to the encoding of our holds feature
into Viper. They address untrusted code and security properties while we do not; on the other
hand, their work does not support custom notions of resource, build in resource-like properties, or
address data structure framing; their technique is concerned speciﬁcally with currency in Solidity.
   Other prior work has focused on veriﬁcation of smart contracts by modelling them as extended
ﬁnite state machines [Mohajerani et al. 2022]. Our approach is more general, as it is not limited to
the domain of smart contracts and does not assume any particular program architecture.
   The speciﬁcation language Chainmail [Drossopoulou et al. 2020] enables user-deﬁned invari-
ants using holistic speciﬁcations, which can be used to enforce a wide range of security-related
properties, including some related to resources in the program. For example, it is possible to deﬁne
an invariant that ensures any change in the balance of a particular account is associated with a call
to deposit referencing that account. Speciﬁcations in Chainmail must still ultimately be phrased
in terms of program states; leading to less direct and more-complex speciﬁcations. In contrast,
our methodology, which treats resources as ﬁrst class, allows speciﬁcations concerning resource
operations directly.
   Various smart contract languages provide ﬁrst-class support for resources. The Move language [Blackshear e
2019], originally developed by Facebook for the Diem blockchain, supports ﬁrst-class resources
that are implemented with linear types. Obsidian [Coblenz et al. 2020] uses both linear types and


                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:24                                                                        Zachary Grannan and Alexander J. Summers


typestate to prevent bugs related to improper handling of resources. Flint [Schrans et al. 2018] sup-
ports asset types that encapsulate unsafe operations and provide a safe interface. None of these
support static veriﬁcation concerning resource quantities, or built-in rules to enforce e.g. that are
by-default preserved.

8 CONCLUSION
In this paper, we examined the challenges encountered when writing speciﬁcations of resource-
manipulating programs in terms of program state. When using a modular veriﬁer, this approach
requires users to explicitly write frame conditions in speciﬁcations, and these frame conditions
make speciﬁcations lengthier and harder to interpret. Furthermore, such speciﬁcations do not eas-
ily compose, and are not expressive enough to rule out certain kinds of resource-related bugs.
   The root cause of these issues is the semantic gap between our expectations of how resources
behave, and the language used to write speciﬁcations. Therefore, we developed a new methodology
to support resource reasoning within speciﬁcations, thereby narrowing the semantic gap.
   The methodology we developed extends a program veriﬁer with a ﬁrst-class notion of resources,
without requiring support for resources in the source language. Instead, we allow users to deﬁne
coupling invariants to connect resource operations to program state. These invariants are checked
by the veriﬁer, allowing users to describe the behaviour of their program in terms of resource
operations rather than as relations on program states.
   We implemented our methodology as an extension to the program veriﬁer Prusti, and evaluated
it by using our extended version of Prusti to verify real-world resource-manipulating programs.
Our evaluation shows that, compared to a standard Prusti speciﬁcation written in terms of program
states, speciﬁcations written using our methodology are more concise and syntactically simpler.
   For future work, we would like to extend our methodology to facilitate interactions with un-
trusted or external code, as such interactions are typical in dealing with smart contracts. In partic-
ular, enforcing coupling invariants for functions that reborrow could increase the applicability of
our technique.

REFERENCES
Wolfgang Ahrendt and Richard Bubel. 2020. Functional Veriﬁcation of Smart Contracts via Strong Data Integrity.
   In Leveraging Applications of Formal Methods, Veriﬁcation and Validation: Applications - 9th International Sympo-
   sium on Leveraging Applications of Formal Methods, ISoLA 2020, Rhodes, Greece, October 20-30, 2020, Proceedings, Part
   III (Lecture Notes in Computer Science, Vol. 12478), Tiziana Margaria and Bernhard Steﬀen (Eds.). Springer, 9–24.
   https://doi.org/10.1007/978-3-030-61467-6_2
Aleph Zero Foundation. 2018. Aleph Zero. https://alephzero.org. Accessed: 2024-02-27.
Anonymous Authors. 2024. Supplementary Material. Supplementary material for the paper: Resource Speciﬁcations for
   Resource-Manipulating Programs.
Vytautas Astrauskas, Aurel Bílỳ, Jonáš Fiala, Zachary Grannan, Christoph Matheja, Peter Müller, Federico Poli, and Alexan-
   der J Summers. 2022. The Prusti Project: Formal Veriﬁcation for Rust. In NASA Formal Methods: 14th International
   Symposium, NFM 2022, Pasadena, CA, USA, May 24–27, 2022, Proceedings. Springer, 88–108.
Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J Summers. 2019. Leveraging Rust Types for Modular
   Speciﬁcation and Veriﬁcation. Proceedings of the ACM on Programming Languages 3, OOPSLA (2019), 1–30.
Sam Blackshear, Evan Cheng, David L Dill, Victor Gao, Ben Maurer, Todd Nowacki, Alistair Pott, Shaz Qadeer, Dario Russi
   Rain, Stephane Sezer, et al. 2019. Move: A Language with Programmable Resources. Libra Assoc (2019), 1.
François Bobot, Jean-Christophe Filliâtre, Claude Marché, and Andrei Paskevich. 2011. Why3: Shepherd Your Herd of
   Provers. In Boogie 2011: First International Workshop on Intermediate Veriﬁcation Languages. 53–64.
Christian Bräm, Marco Eilers, Peter Müller, Robin Sierra, and Alexander J Summers. 2021. Rich Speciﬁcations for Ethereum
   Smart Contract Veriﬁcation. Proceedings of the ACM on Programming Languages 5, OOPSLA (2021), 1–30.
Michael Coblenz, Reed Oei, Tyler Etzel, Paulette Koronkevich, Miles Baker, Yannick Bloem, Brad A Myers, Joshua Sunshine,
   and Jonathan Aldrich. 2020. Obsidian: Typestate and Assets for Safer Blockchain Programming. ACM Transactions on
   Programming Languages and Systems (TOPLAS) 42, 3 (2020), 1–82.


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Resource Specifications for Resource-Manipulating Programs                                                        1:25


Sophia Drossopoulou, James Noble, Julian Mackay, and Susan Eisenbach. 2020. Holistic Speciﬁcations for Robust Programs..
   In FASE. 420–440.
William Entriken, Dieter Shirley, Jacob Evans, and Nastassia Sachs. 2018. ERC-721: Non-Fungible Token Standard.
   https://eips.ethereum.org/EIPS/eip-721. Ethereum Improvement Proposals, no. 721. [Online serial].
Dan R Ghica and Alex I Smith. 2014. Bounded linear types in a resource semiring. In Programming Languages and Systems:
   23rd European Symposium on Programming, ESOP 2014, Held as Part of the European Joint Conferences on Theory and
   Practice of Software, ETAPS 2014, Grenoble, France, April 5-13, 2014, Proceedings 23. Springer, 331–350.
Christopher Goes. 2020. The Interblockchain Communication Protocol: An Overview. arXiv preprint arXiv:2006.15918
   (2020).
Christopher Goes. 2022. ICS-20 Fungible Token Transfer Speciﬁcation. https://github.com/cosmos/ibc/tree/main/spec/app/ics-020-fungib
Andreas M Hein. 2010. Identiﬁcation and Bridging of Semantic Gaps in the Context of Multi-domain Engineering. In Forum
   on Philosophy, Engineering & Technology. 58–57.
IBC Standards Committee. 2023. Interchain Standards. https://github.com/cosmos/ibc
Informal Systems Inc. and ibc-rs authors. 2022. ibc-rs. https://github.com/cosmos/ibc-rs
Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. 2015. Iris:
   Monoids and invariants as an orthogonal basis for concurrent reasoning. ACM SIGPLAN Notices 50, 1 (2015), 637–650.
K Rustan M Leino. 2008. This is Boogie 2. manuscript KRML 178, 131 (2008), 9.
K Rustan M Leino. 2010. Dafny: An automatic program veriﬁer for functional correctness. In International conference on
   logic for programming artiﬁcial intelligence and reasoning. Springer, 348–370.
J. M. Lucassen and D. K. Giﬀord. 1988. Polymorphic Eﬀect Systems. In Proceedings of the 15th ACM SIGPLAN-SIGACT
   Symposium on Principles of Programming Languages (San Diego, California, USA) (POPL ’88). Association for Computing
   Machinery, New York, NY, USA, 47–57. https://doi.org/10.1145/73560.73564
John McCarthy and Patrick J Hayes. 1981. Some Philosophical Problems from the Standpoint of Artiﬁcial Intelligence. In
   Readings in artiﬁcial intelligence. Elsevier, 431–450.
Sahar Mohajerani, Wolfgang Ahrendt, and Martin Fabian. 2022. Modeling and Security Veriﬁcation of State-Based Smart
   Contracts. IFAC-PapersOnLine 55, 28 (2022), 356–362.
Peter Müller, Malte Schwerhoﬀ, and Alexander J Summers. 2016. Viper: A Veriﬁcation Infrastructure for Permission-based
   Reasoning. In Veriﬁcation, Model Checking, and Abstract Interpretation: 17th International Conference, VMCAI 2016, St.
   Petersburg, FL, USA, January 17-19, 2016. Proceedings 17. Springer, 41–62.
Panorama Swap Developers. 2021. Panorama. https://panoramaswap.com. Accessed: 2024-02-27.
Parity Technologies. 2020. ink documentation. https://use.ink/. Accessed: 2024-02-27.
Matthew Parkinson and Gavin Bierman. 2005. Separation Logic and Abstraction. In Proceedings of the 32nd ACM SIGPLAN-
   SIGACT Symposium on Principles of Programming Languages (Long Beach, California, USA) (POPL ’05). Association for
   Computing Machinery, New York, NY, USA, 247–258. https://doi.org/10.1145/1040305.1040326
M. J. Parkinson and A. J. Summers. 2012. The Relationship Between Separation Logic and Implicit Dynamic Frames. Logical
   Methods in Computer Science 8, 3:01 (2012), 1–54. https://doi.org/10.1007/978-3-642-35182-2_8
John C Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In Proceedings 17th Annual IEEE
   Symposium on Logic in Computer Science. IEEE, 55–74.
Franklin Schrans, Susan Eisenbach, and Sophia Drossopoulou. 2018. Writing Safe Smart Contracts in Flint. In Companion
   Proceedings of the 2nd International Conference on the Art, Science, and Engineering of Programming. 218–219.
Jan Smans, Bart Jacobs, and Frank Piessens. 2009. Implicit Dynamic Frames: Combining Dynamic Frames and Separation
   Logic. In ECOOP 2009–Object-Oriented Programming: 23rd European Conference, Genoa, Italy, July 6-10, 2009. Proceedings
   23. Springer, 148–172.
Philip Wadler. 1990.            Linear Types can Change the World!. In Programming Concepts and Methods.
   https://api.semanticscholar.org/CorpusID:58535510
Haifeng Xi. 2022. ICS-721 Non-Fungible Token Transfer Speciﬁcation. https://github.com/cosmos/ibc/tree/main/spec/app/ics-721-nft-tran




                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
