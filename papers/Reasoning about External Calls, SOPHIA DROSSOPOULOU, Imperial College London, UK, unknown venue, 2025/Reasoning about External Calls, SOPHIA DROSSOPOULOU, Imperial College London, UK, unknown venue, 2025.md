                                         Reasoning about External Calls – Extended Version∗
                                         SOPHIA DROSSOPOULOU, Imperial College London, UK
                                         JULIAN MACKAY, Kry10 Ltd, and Victoria University of Wellington, NZ
                                         SUSAN EISENBACH, Imperial College London, UK
                                         JAMES NOBLE, Creative Research & Programming, NZ
                                         In today’s complex software, internal trusted code is tightly intertwined with external untrusted code. To
                                         reason about internal code, programmers must reason about the potential effects of calls to external code,
arXiv:2506.06544v2 [cs.PL] 23 Nov 2025




                                         even though that code is not trusted and may not even be available. The effects of external calls can be limited
                                         if internal code is programmed defensively, limiting potential effects by limiting access to the capabilities
                                         necessary to cause those effects.
                                             This paper addresses the specification and verification of internal code that relies on encapsulation and
                                         object capabilities to limit the effects of external calls. We propose new assertions for access to capabilities,
                                         new specifications for limiting effects, and a Hoare logic to verify that a module satisfies its specification, even
                                         while making external calls. We illustrate the approach though a running example with mechanised proofs,
                                         and prove soundness of the Hoare logic.
                                         ACM Reference Format:
                                         Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble. 2025. Reasoning about External
                                         Calls – Extended Version. 1, 1 (November 2025), 90 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn

                                         1 Introduction
                                         This paper addresses reasoning about external calls — when module 𝑀𝑖𝑛𝑡𝑙
                                         trusted internal code calls out to untrusted, unknown external          method m1 ..
                                         code: In the code sketch to the right, an internal module, 𝑀𝑖𝑛𝑡𝑙 ,         ... trusted code ...
                                         has two methods. Method m2 takes an untrusted parameter                 method m2(untrst:external)
                                         untrst, and calls an unknown external method unkn passing                  ... trusted code ...
                                         itself as an argument. The challenge is: What effects will that             untrst.unkn(this)
                                         external call have? What if untrst calls back into 𝑀𝑖𝑛𝑡𝑙 ?                 ... trusted code ...
                                            External calls need not have arbitrary effects. If the programming language supports encapsulation
                                         (e.g. no address forging, privacy, etc.) then internal modules can be written so that effects are
                                               • Precluded, i.e. guaranteed to never happen. E.g., a correct implementation of the DAO [25]
                                               can ensure that its balance never falls below the sum of the balances of its subsidiary accounts,
                                               or
                                               • Limited, i.e. they may happen, but only in well-defined circumstances. E.g., while the DAO
                                               does not preclude that a signatory’s balance will decrease, it does ensure that the balance
                                               decreases only as a direct consequence of calls from the signatory.
                                         Precluded effects are special case of limited effects, and have been studied extensively in the context
                                         of object invariants [9, 41, 67, 91, 111]. In this paper, we tackle the more general, and more subtle
                                         case of reasoning about limited effects for external calls.
                                            The Object Capability Model combines the capability model of operating system security [69, 118]
                                         with pure object-oriented programming [1, 108, 114]. Capability-based operating systems reify
                                         ∗ This extended version of our work contains an appendix with full formal definitions, examples, more explanations, and

                                         worked out proofs. Citations should use the original version of the paper, [42].

                                         Authors’ Contact Information: Sophia Drossopoulou, Imperial College London, UK, scd@imperial.ac.uk; Julian Mackay,
                                         Kry10 Ltd, and Victoria University of Wellington, NZ, julian.mackay@ecs.vuw.ac.nz; Susan Eisenbach, Imperial College
                                         London, UK, susan@imperial.ac.uk; James Noble, Creative Research & Programming, Wellington, NZ, kjx@acm.org.

                                         2025. ACM XXXX-XXXX/2025/11-ART
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn


                                                                                                        , Vol. 1, No. 1, Article . Publication date: November 2025.
2                                                   Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


resources as capabilities — unforgeable, distinct, duplicable, attenuable, communicable bitstrings
which both denote a resource and grant rights over that resource. Effects can only be caused by
invoking capabilities: controlling effects reduces to controlling capabilities.
   Mark Miller’s [84] object-capability model treats object references as capabilities. Building on
early object-capability languages such as E [84, 87] and Joe-E [81], a range of recent programming
languages and web systems [20, 54, 103] including Newspeak [17], AmbientTalk [33] Dart [16],
Grace [12, 60], JavaScript (aka Secure EcmaScript [86]), and Wyvern [80] have adopted the object
capability model. Security and encapsulation is encoded in the relationships between the objects,
and the interactions between them. As argued in [43], object capabilities make it possible to write
secure programs, but cannot by themselves guarantee that any particular program will be secure.
   Logics for Reasoning with Capabilities have been proposed in [71, 100, 109, 112], primarily in
object-based settings – our work operates in a class-based setting. More importantly, in these
works, capabilities are statically embedded within objects, and authority is conferred through the
object’s interface. In contrast, our approach models capabilities in a manner that is, in some sense,
the dual of theirs: capabilities are not intrinsic to objects but may be dynamically accessible to the
callee—typically via ambient authority in the execution environment.
   This distinction carries important implications for reasoning about effects. In [71, 100, 109, 112],
one can argue that if an object is exported with an interface that omits certain capabilities, then
the corresponding effects are ruled out. However, this argument hinges on the assumption that the
exporting site has precise knowledge of the object’s embedded capabilities. Our model requires
no such assumption. Instead, we reason about potential effects based on the capabilities available
in the receiving context. As long as the target context lacks access to specific capabilities, we can
guarantee that the corresponding effects are unobservable —regardless of the object’s interface.
   Our earlier work [44, 76] follows a similar dynamic model of object capabilities, though without
addressing external effects. Specifically, [44] introduces “holistic specifications” to capture a mod-
ule’s emergent behavior, while [76] proposes a logic for proving that modules devoid of external
calls conform to their holistic specifications.
   This paper contributes (1) protection assertions to limit access to object-capabilities, (2) a specifi-
cation language to define how limited access to capabilities should limit effects, (3) a Hoare logic
to reason about external calls and to prove that modules satisfy their specifications, (4) proof of
soundness, (5) a worked illustrative example with a mechanised proof in Coq.
   Structure of this paper: Sect. 2 outlines the main ingredients of our approach in terms of an
example. Sect. 3 outlines a simple object-oriented language used for our work. Sect. 4 and 5 give
syntax and semantics of assertions and specifications. Sect. 6 develops a Hoare logic to prove
external calls, and modules’ adherance to specifications, and summarises our proof of the running
example (Coq at [75]). Sect. 7 outlines proof of soundness of the Hoare logic. Sect. 8 concludes. Full
technical details can be found in the appendices of this paper.

2    The problem and our approach
We introduce the problem through an example, and outline our approach. We work with a small,
class-based object-oriented, sequential language similar to Joe-E [81] with modules, module-private
fields (accessible only from methods from the same module), and unforgeable, un-enumerable
addresses. We distinguish between internal objects — instances of our internal module 𝑀’s classes
— and external objects defined in any number of external modules 𝑀.1 Private methods may only
be called by objects of the same module, while public methods may be called by any object with

1We use the notation 𝑧 for a sequence of 𝑧, i.e. for 𝑧 , 𝑧 , ...𝑧
                                                      1 2         𝑛



, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                           3


a reference to the method receiver, and with actual arguments of dynamic types that match the
declared formal parameter types.2
   We are concerned with guarantees made in an open setting; Our internal module 𝑀 must be
programmed so that execution of 𝑀 together with any unknown, arbitrary, external modules 𝑀 will
satisfy these guarantees – without relying on any assumptions about 𝑀’s code.3 All we can rely on,
is the guarantee that external code interacts with the internal code only through public methods;
such a guarantee may be given by the programming language or by the underlying platform.4

2.1    Shop – Illustrating Limited Effects
Consider below the internal module 𝑀shop , with classes Item, Shop, Account, and Inventory.
Classes Inventory and Item are straightforward: we elide their details. Accounts hold a
balance and have a key. Access to an Account, allows one to pay money into it, and access to an
Account and its Key, allows one to withdraw money from it. A Shop has an Account, and a
public method buy to allow a buyer — an external object — to buy and pay for an Item:
  1 module M𝑠ℎ𝑜𝑝
  2   ...
  3   class Shop
  4     field accnt:Account, invntry:Inventory, clients:external
  5
  6        public method buy(buyer:external, anItem:Item)
  7          int price = anItem.price
  8          int oldBlnce = this.accnt.blnce
  9          buyer.pay(this.accnt, price)
 10          if (this.accnt.blnce == oldBlnce+price)
 11             this.send(buyer,anItem)
 12          else
 13             buyer.tell("you have not paid me")
 14
 15        private method send(buyer:external, anItem:Item)                              ....

The sketch below shows a possible heap snippet.
                           External objects are red; internal objects are green. Each object has a
                           number, and an abbreviated class name: 𝑜 1 , 𝑜 2 and 𝑜 5 are a Shop, an
                           Inventory, and an external object. Curved arrows indicate field values:
                           𝑜 1 has three fields, pointing to 𝑜 4 , 𝑜 5 and 𝑜 2 . Fields denote direct access.
                           The transitive closure of direct access gives indirect (transitive) access: 𝑜 1
                           has direct access to 𝑜 4 , and indirect access to 𝑜 6 . Object 𝑜 6 — highlighted
                           with a dark outline — is the key capability that allows withdrawal from
                           𝑜 4 . The critical point in our code is the external call on line 9, where the
                           Shop asks the buyer to pay the price of that item, by calling pay on
                           buyer and passing the Shop’s account as an argument.
   As buyer is an external object, the module 𝑀shop has no method specification for pay, and no
certainty about what its implementation might do. What are the possible effects of that external
call? At line 9, the Shop hopes the buyer will have deposited the price into its account, but needs
to be certain the buyer cannot have emptied that account instead. Can the Shop be certain?
2 As in Joe-E, we leverage module-based privacy to restrict propagation of capabilities, and reduce the need for reference

monitors etc, c.f. Sect 3 in [81].
3 This is a critical distinction from e.g. cooperative approaches such as rely/guarantee [53, 115].
4 Thus our approach is also applicable to inter-language safety.



                                                                   , Vol. 1, No. 1, Article . Publication date: November 2025.
4                                                Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


    Indeed, if
    (A) Prior to the call of buy, the buyer has no eventual access to the account’s key, —- and
    (B) 𝑀shop ensures that
      (a) access to keys is not leaked to external objects, —- and
      (b) funds cannot be withdrawn unless the external entity responsible for the withdrawal
          (eventually) has access to the account’s key,
        —- then
    (C) The external call on line 9 can never result in a decrease in the shop’s account balance.
The remit of this paper is to provide specification and verification tools that support arguments
like the one above. This gives rise to the following two challenges: 1𝑠𝑡 : A specification language
which describes access to capabilities and limited effects, 2𝑛𝑑 : A Hoare Logic for adherence to such
specifications.

2.2    1𝑠𝑡 Challenge: Specification Language
We want to give a formal meaning to the guarantee that for some effect, 𝐸, and an object 𝑜𝑐 which
is the capability for 𝐸:
         𝐸 (e.g. the account’s balance decreases) can be caused only by external objects calling
   (*) methods on internal objects,
         and only if the causing object has access to 𝑜𝑐 (e.g. the key).
The first task is to describe that effect 𝐸 took place: if we find some assertion 𝐴 (e.g. balance is ≥
some value 𝑏) which is invalidated by 𝐸, then, (*) can be described by something like:
   (**) If 𝐴 holds, and if no external access to 𝑜𝑐 then 𝐴 holds in the future.
We next make more precise that “no external access to 𝑜𝑐 ”, and that “𝐴 holds in the future”.
   In a first attempt, we could say that “no external access to 𝑜𝑐 ” means that no external object
exists, nor will any external objects be created. This is too strong, however: it defines away the
problem we are aiming to solve.
   In a second attempt, we could say that “no external access to 𝑜𝑐 ” means that no external object
has access to 𝑜𝑐 , nor will ever get access to 𝑜𝑐 . This is also too strong, as it would preclude 𝐸 from
ever happening, while our remit is that 𝐸 may happen but only under certain conditions.
   This discussion indicates that the lack of external access to 𝑜𝑐 is not a global property, and that
the future in which 𝐴 will hold is not permanent. Instead, they are both defined from the perspective
of the current point of execution.
   Thus:
            If 𝐴 holds, and if no external object reachable from the current point of execution has
   (***) access to 𝑜𝑐 , and if no internal objects pass 𝑜𝑐 to external objects,
            then
            𝐴 holds in the future scoped by the current point of execution.
We will shortly formalize “reachable from the current point of execution” as protection in §2.2.1,
and then “future scoped by the current point of execution” as scoped invariants in §2.2.2. Both of
these definitions are in terms of the “current point of execution”:
The Current Point of Execution is characterized by the heap, and the activation frame of the currently
executing method. Activation frames (frames for short) consist of a variable map and a continuation
– the statements remaining to be executed in that method. Method calls push frames onto the stack
of frames; method returns pop frames off. The frame on top of the stack (the most recently pushed
frame) belongs to the currently executing method.
   Fig. 1 illustrates the current point of execution. The left pane, 𝜎1 , shows a state with the same
heap as earlier, and where the top frame is 𝜙 1 – it could be the state before a call to buy. The middle

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                                  5


pane, 𝜎2 , is a state where we have pushed 𝜙 2 on top of the stack of 𝜎1 – it could be a state during
execution of buy. The right pane, 𝜎3 , is a state where we have pushed 𝜙 3 on top of the stack of 𝜎2 –
it could be a state during execution of pay.
   States whose top frame has a receiver (this) which is an internal object are called internal states,
the other states are called external states. In Fig 1, states 𝜎1 and 𝜎2 are internal, and 𝜎3 is external.




                  𝜎1 , top frame 𝜙 1                    𝜎2 , top frame 𝜙 2                   𝜎3 , top frame 𝜙 3

Fig. 1. The current point of execution before buy, during buy, and during pay. Frames 𝜙 1 , 𝜙 2 are green as
their receiver (this) is internal; 𝜙 3 is red as its receiver is external. Continuations are omitted.



2.2.1    Protection.
Protection Object 𝑜 is protected from object 𝑜 ′ , formally ⟨𝑜⟩⟩←
                                                                ×− 𝑜 ′ , if no external object indirectly
                        ′
     accessible from 𝑜 has direct access to 𝑜. Object 𝑜 is protected, formally ⟨ o⟩⟩ , if no external
     object indirectly accessible from the current frame has direct access to 𝑜, and if the receiver
     is external then 𝑜 is not an argument.5 More in Def. 4.4.
   Fig. 2 illustrates protected and protected from. Object 𝑜 6 is not protected in states 𝜎1 and 𝜎2 , but is
protected in state 𝜎3 . This is so, because the external object 𝑜 5 is indirectly accessible from the top
frame in 𝜎1 and in 𝜎2 , but not from the top frame in 𝜎3 – in general, calling a method (pushing a
frame) can only ever decrease the set of indirectly accessible objects. Object 𝑜 4 is protected in states
𝜎1 and 𝜎2 , and not protected in state 𝜎3 because though neither object 𝑜 5 nor 𝑜 7 have direct access
to 𝑜 4 , in state 𝜎3 the receiver is external and 𝑜 4 is one of the arguments.

                                        heap                  𝜎1               𝜎2               𝜎3
                               ... |= ⟨𝑜 6 ⟩ ← ×− 𝑜 4   𝜎1 ̸ |= ⟨𝑜 6 ⟩   𝜎2 ̸ |= ⟨𝑜 6 ⟩   𝜎3 |= ⟨𝑜 6 ⟩
                               ... ̸ |= ⟨𝑜 6 ⟩ ←
                                               ×− 𝑜 5   𝜎1 |= ⟨𝑜 4 ⟩     𝜎2 |= ⟨𝑜 4 ⟩     𝜎3 ̸ |= ⟨𝑜 4 ⟩

                            Fig. 2. Protected from and Protected. – continuing from Fig, 1.


  If a protected object 𝑜 is never passed to external objects (i.e. never leaked) then 𝑜 will remain
protected during the whole execution of the current method, including during any nested calls.
This is the case even if 𝑜 was not protected before the call to the current method. We define scoped
invariants to describe property preservation within the current and all its nested calls.

5 An object has direct access to another object if it has a field pointing to the latter; it has indirect access to another object if

there exists a sequence of field accesses (direct references) leading to the other object; an object is indirectly accessible from
the frame if one of the frame’s variables has indirect access to it.


                                                                         , Vol. 1, No. 1, Article . Publication date: November 2025.
6                                                  Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


2.2.2    Scoped Invariants. We build on the concept of history invariants [28, 68, 70] and define:
                           A
Scoped invariants 𝑥 : 𝐶.{𝐴} expresses that if an external state 𝜎 has objects 𝑥 of class 𝐶, and
        satisfies 𝐴, then all external states which are part of the scoped future of 𝜎 will also satisfy 𝐴.
        The scoped future contains all states which can be reached through any program execution
        steps, including further method calls and returns, but stopping just before returning from the
        call active in 𝜎 6 – c.f. Def 3.2.
   Fig. 3 shows the states of an unspecified execution starting at internal state 𝜎3 and terminating at
internal state 𝜎24 . It distinguishes between steps within the same method (→), method calls (↑), and
method returns (↓). The scoped future of 𝜎6 consists of 𝜎6 -𝜎21 , but does not contain 𝜎22 onwards,
since scoped future stops before returning. Similarly, the scoped future of 𝜎9 consists of 𝜎9 , 𝜎10 , 𝜎11 ,
𝜎12 , 𝜎13 , and 𝜎14 , and does not include, e.g., 𝜎15 , or 𝜎18 .




                Fig. 3. Execution. Green disks represent internal states; red disks external states.

                                A
  The scoped invariant 𝑥 : 𝐶.{𝐴0 } guarantees that if 𝐴0 holds in 𝜎8 , then it will also hold in 𝜎9 ,
𝜎13 , and 𝜎14 ; it doesn’t have to hold in 𝜎10 , 𝜎11 , and 𝜎12 as these are internal states. Nor does it have
have to hold at 𝜎15 as it is not part of 𝜎9 ’s scoped future.
Example 2.1. The following scoped invariants
                    A                                                             A
        𝑆 1 ≜ a : Account.{⟨⟨a⟩⟩ }                      𝑆 2 ≜ a : Account.{⟨⟨a.key⟩⟩ }
                    A
        𝑆 3 ≜ a : Account, b : int.{⟨⟨a.key⟩⟩ ∧ a.blnce ≥ b}
guarantee that accounts are not leaked (𝑆 1 ), keys are not leaked (𝑆 2 ), and that the balance does
not decrease unless there is unprotected access to the key (𝑆 3 ).
This example illustrates three crucial properties of our invariants:
     Conditional: They are preserved, but unlike object invariants, they do not always hold. E.g.,
     buy cannot assume ⟨ 𝑎.key⟩⟩ holds on entry, but guarantees that if it holds on entry, then it
     will still hold on exit.
     Scoped: They are preserved during execution of a specific method but not beyond its return.
     It is, in fact, expected that the invariant will eventually cease to hold after its completion.
     For instance, while ⟨ 𝑎.key⟩⟩ may currently hold, it is possible that an earlier (thus quiescent)
     method invocation frame has direct access to 𝑎.key – without such access, 𝑎 would not be
     usable for payments. Once control flow returns to the quiescent method (i.e. enough frames
     are popped from the stack) ⟨ 𝑎.key⟩⟩ will no longer hold.
     Modular: They describe externally observable effects (e.g. key stays protected) across whole
     modules, rather than the individual methods (e.g. set) making up a module’s interface. Our
6 Here lies the difference to history invariants, which consider all future states, including returning from the call active in 𝜎.



, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                               7


       example specifications will characterize any module defining accounts with a blnce and a
       key – even as ghost fields – irrespective of their APIs.
Example 2.2. We now use the features from the previous section to specify methods.
       𝑆 4 ≜ { ⟨ this.accnt.key⟩⟩←      ×− buyer ∧ this.accnt.blnce = 𝑏 }
                    public Shop :: buy(buyer : external, anItem : Item)
                { this.accnt.blnce ≥ 𝑏 } ∥ {...}
𝑆 4 guarantees that if the key was protected from buyer before the call, then the balance will not
decrease7 . It does not guarantee buy will only be called when ⟨ this.accnt.key⟩⟩ ←×    − buyer
holds: as a public method, buy can be invoked by external code that ignores all specifications.
Example 2.3. We illustrate the meaning of our specifications using three versions (Mgood , Mbad , and
Mfine ) of the 𝑀shop module [76]; these all share the same transfer method to withdraw money:
module Mgood
  class Shop    ... as earlier ...
  class Account
    field blnce:int
    field key:Key
    public method transfer(dest:Account, key':Key, amt:nat)
       if (this.key==key') this.blnce-=amt; dest.blnce+=amt
    public method set(key':Key)
       if (this.key==null) this.key=key'

Now consider modules Mbad and Mfine , which differ from Mgood only in their set methods. Whereas
Mgood ’s key is fixed once it is set, Mbad allows any client to set an account’s key at any time, while
Mfine requires the existing key in order to replace it.

      module Mbad                                    module Mfine
        ... as earlier ...                             ... as earlier ...
        public method set(key':Key)                    public method set(key',key'':Key)
          this.key=key'                                  if (this.key==key') this.key=key''

   Thus, in all three modules, the key is a capability which enables the withdrawal of the money.
Moreover, in Mgood and Mfine , the key capability is a necessary precondition for withdrawal of money,
while in in Mbad it is not. Using Mbad , it is possible to start in a state where the account’s key is
unknown, modify the key, and then withdraw the money. Code such as
     k=new Key; acc.set(k); acc.transfer(rogue_accnt,k,1000)
is enough to drain acc in Mbad without knowing the key. Even though transfer in Mbad is “safe”
when considered in isolation, it is not safe when considered in conjunction with other methods
from the same module.
   Mgood and Mfine satisfy 𝑆 2 and 𝑆 3 , while Mbad satisfies neither. So if Mbad was required to satisfy
either 𝑆 2 or 𝑆 3 then it would be rejected by our inference system as not safe. None of the three
versions satisfy 𝑆 1 because pay could leak an Account.

2.3    2𝑛𝑑 Challenge: A Hoare Logic for Adherence to Specifications
2.3.1 Hoare Quadruples. Scoped invariants require quadruples, rather than classical triples. Specif-
ically,
                                     A
                                𝑥 : 𝐶.{𝐴}
asserts that if an external state 𝜎 satisfies 𝑥 : 𝐶 ∧ 𝐴, then all its scoped external future states will
7We ignore the ... for the time being.



                                                       , Vol. 1, No. 1, Article . Publication date: November 2025.
8                                                Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


also satisfy 𝐴. For example, if 𝜎 was an external state executing a call to Shop::buy, then a
scoped external future state could be reachable during execution of the call pay. This implies that
we consider not only states at termination but also external states reachable during execution of
statements. To capture this, we extend traditional Hoare triples to quadruples of form
                              { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }
promising that if a state satisfies 𝐴 and executes 𝑠𝑡𝑚𝑡, any terminating state will satisfy 𝐴′ , and
and any intermediate external states reachable during execution of 𝑠𝑡𝑚𝑡 satisfy 𝐴′′ – c.f. Def. 5.2.
   We assume an underlying Hoare logic of triples 𝑀 ⊢𝑢𝑙 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ }, which does not have
the concept of protection – that is, the assertions 𝐴 in the ⊢𝑢𝑙 -triples do not mention protection. We
then embed the ⊢𝑢𝑙 -logic into the quadruples logic ( ⊢𝑢𝑙 -triples whose statements do not contain
method calls give rise to quadruples in our logic – see rule below). We extend assertions 𝐴 so they
may mention protection and add rules about protection (e.g. newly created objects are protected –
see rule below), and add usual conditional and substructural rules. More in Fig.6 and 19.


     𝑀 ⊢𝑢𝑙 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } 𝑠𝑡𝑚𝑡 calls no methods
            𝑀 ⊢ { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }                        𝑀 ⊢ { 𝑡𝑟𝑢𝑒 } 𝑢 = new 𝐶 { ⟨𝑢⟩⟩ } ∥ { 𝐴 }


2.3.2 Well-formed modules and External Calls. A module is well-formed, if its specification is
well-formed, its public methods preserve the module’s scoped invariants, and all methods satisfy
their specifications - c.f. Fig. 8. E.g., to prove that Shop::buy satisfies 𝑆 4 , taking 𝑠𝑡𝑚𝑡𝑠𝑏 for the
body of buy, we have to prove:
       { buyer : extl ∧ ⟨ this.accnt.key⟩⟩←                   ×− buyer ∧ this.accnt.blnce = 𝑏 }
 (0)            𝑠𝑡𝑚𝑡𝑠𝑏
       { this.accnt.blnce ≥ 𝑏 } || { ... }
   The proof proceeds using our Hoare quadruples logic. The treatment of external calls is of special
interest. Here, the challenge is the external call on line 9. We need to establish the Hoare quadruple:
         { buyer : extl ∧ ⟨ this.accnt.key⟩⟩←                   ×− buyer ∧ this.accnt.blnce = 𝑏 }
   (1)            buyer.pay(this.accnt,price)
         { this.accnt.blnce ≥ 𝑏 } || { ... }
which says that if the shop’s account’s key is protected from buyer, then the account’s balance
will not decrease after the call of pay.
   To prove (1), we aim to use 𝑆 3 , but this is not straightforward: 𝑆 3 requires ⟨ this.accnt.key⟩⟩ ,
which is not provided by the precondition of (1) . More alarmingly, ⟨ this.accnt.key⟩⟩ may
not hold at the time of the call. For example, in state 𝜎2 (Fig. 2), which could initiate the call to pay,
we have 𝜎2 |= ⟨𝑜 4 .key⟩⟩←  ×− 𝑜 7 , but 𝜎2 ̸ |= ⟨𝑜 4 .key⟩⟩ .
   Fig. 2 provides insights into addressing this issue. Upon entering the call, in state 𝜎3 , we find that
𝜎3 |= ⟨𝑜 4 .key⟩⟩ . More generally, if ⟨ this.accnt.key⟩⟩←            ×− buyer holds before the call to pay,
then ⟨ this.accnt.key⟩⟩ holds upon entering the call. This is because any objects indirectly
accessible during pay must have been indirectly accessible from the call’s receiver (buyer) or
arguments (this.accnt and price) when pay was called.
   In general, if ⟨ x⟩⟩ ←×
                         − y𝑖 holds for all y𝑖 , before a call y0 .𝑚(y1, ..., y𝑛 ), then ⟨ x⟩⟩ holds upon
entering the call. Here we have ⟨ this.accnt.key⟩⟩←                ×− buyer by precondition. We also have
that price is a scalar and therefore ⟨ this.accnt.key⟩⟩←                ×− price. And the type information
gives that all fields transitively accessible from an Account are scalar or internal; this gives
that ⟨ this.accnt.key⟩⟩ ←−         × this.accnt. This enables the application of 𝑆 3 in (1). The
corresponding Hoare logic rule is shown in Fig. 7.


, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                            9


2.4    Summary
In an open world, external objects can execute arbitrary code, invoke any public internal methods,
access any other external objects, and even collude with each another. The external code may be
written in the same or a different programming language than the internal code – all we need is
that the platform protects direct external read/write of the internal private fields, while allowing
indirect manipulation through calls of public methods.
   The conditional and scoped nature of our invariants is critical to their applicability. Protection
is a local condition, constraining accessible objects rather than imposing a structure across the
whole heap. Scoped invariants are likewise local: they do not preclude some effects from the
whole execution of a program, rather the effects are precluded only in some local contexts. While
𝑎.blnce may decrease in the future, this can only happen in contexts where an external object
has direct access to 𝑎.key. Enforcing these local conditions is the responsibility of the internal
module: precisely because these conditions are local, they can be enforced locally within a module,
irrespective of all the other modules in the open world.

3     The Underlying Programming Language ℒ𝑢𝑙
3.1    ℒ𝑢𝑙 Syntax and Runtime Configurations
This work is based on ℒ𝑢𝑙 , a minimal, imperative, sequential, class based, typed, object-oriented
language. We believe, however, that the work can easily be adapted to any capability safe language
with some form of encapsulation, and that it can also support inter-language security, provided
that the platform offers means to protect a module’s private state; cf capability-safe hardware as
in Cheri [32]. Wrt to encapsulation and capability safety, ℒ𝑢𝑙 supports private fields, private and
public methods, unforgeable addresses, and no ambient authority (no static methods, no address
manipulation). To reduce the complexity of our formal models, as is usually done, e.g. [35, 58, 97], ℒ𝑢𝑙
lacks many common languages features, omitting static fields and methods, interfaces, inheritance,
subsumption, exceptions, and control flow. In our examples, we use numbers and booleans – these
can be encoded.
    Fig. 4 shows the ℒ𝑢𝑙 syntax. Statements, 𝑠𝑡𝑚𝑡, are three-address instructions, method calls,
or empty, 𝜖. Expressions, e, are ghost code; as such, they may appear in assertions but not in
statements, and have no side-effects [23, 46]. Expressions may contain fields, e.𝑓 , or ghost-fields,
e0 .𝑔𝑓 (e). The meaning of e is module-dependent; e.g. a.blnce is a field lookup in Mgood , but in a
module which stores balances in a table it would be a recursive lookup through that table – c.f.
example in §app:BankAccount:ghost. 8 In line with most tools, we support ghost-fields, but they
are not central to our work.
    ℒ𝑢𝑙 states, 𝜎, consist of a heap 𝜒 and a stack. A stack is a sequence of frames, 𝜙 1 ·...·𝜙𝑛 . A frame,
𝜙, consists of a local variable map and a continuation, i.e.the statements to be executed. The top
frame, i.e. the frame most recently pushed onto the stack, in a state (𝜙 1 ·...·𝜙𝑛 , 𝜒) is 𝜙𝑛 .
    Notation. We adopt the following unsurprising notation:
      • An object is uniquely identified by the address that points to it. We shall be talking of objects
        𝑜, 𝑜 ′ when talking less formally, and of addresses, 𝛼, 𝛼 ′ , 𝛼 1 , ... when more formal.
      • 𝑥, 𝑥 ′ , 𝑦, 𝑧, 𝑢, 𝑣, 𝑤 are variables; 𝑑𝑜𝑚(𝜙) and 𝑅𝑛𝑔(𝜙) indicate the variable map in 𝜙; 𝑑𝑜𝑚(𝜎)
        and 𝑅𝑛𝑔(𝜎) indicate the variable map in the top frame in 𝜎
      • 𝛼 ∈ 𝜎 means that 𝛼 is defined in the heap of 𝜎, and 𝑥 ∈ 𝜎 means that 𝑥 ∈ 𝑑𝑜𝑚(𝜎). Conversely,
        𝛼 ∉ 𝜎 and 𝑥 ∉ 𝜎 have the obvious meanings. ⌊𝛼⌋ 𝜎 is 𝛼; and ⌊𝑥⌋ 𝜎 is the value to which 𝑥 is

8 For convenience, e.𝑔𝑓 is short for e.𝑔𝑓 ( ). Thus, e.𝑔𝑓 may be simple field lookup in some modules, or ghost-field in others.



                                                                   , Vol. 1, No. 1, Article . Publication date: November 2025.
10                                                    Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


      𝑀𝑑𝑙      ::=     𝐶 ↦→ 𝐶𝐷𝑒 𝑓                         Module Def.          𝑓 𝑙𝑑     ::=    field 𝑓 : 𝑇             Field Def.
     𝐶𝐷𝑒 𝑓     ::=     class 𝐶 { 𝑓 𝑙𝑑; 𝑚𝑡ℎ; 𝑔𝑓 𝑙𝑑; }        Class Def.         𝑇        ::=    𝐶                              Type
     𝑚𝑡ℎ       ::=     𝑝 method 𝑚 (𝑥 : 𝑇 ): 𝑇 { 𝑠 }       Method Def.          𝑝        ::=    private | public          Privacy

 𝑠𝑡𝑚𝑡        ::=     𝑥 := 𝑦 | 𝑥 := 𝑣 | 𝑥 := 𝑦.𝑓 | 𝑥 .𝑓 := 𝑦 | 𝑥 := 𝑦0 .𝑚 (𝑦) | 𝑥 := new 𝐶 | 𝑠𝑡𝑚𝑡 ; 𝑠𝑡𝑚𝑡 | 𝜖
 𝑔𝑓 𝑙𝑑       ::=     ghost 𝑔𝑓 (𝑥 : 𝑇 ) { e } : 𝑇                                                                        Ghosts
  e          ::=     𝑥 | 𝑣 | e.𝑓 | e.𝑔𝑓 (e)

        𝜎     ::=     (𝜙, 𝜒 )         Program State                      𝐶, 𝑓 , 𝑚, 𝑔𝑓 , 𝑥, 𝑦   ::=   𝐼𝑑𝑒𝑛𝑡𝑖 𝑓 𝑖𝑒𝑟
        𝜙     ::=     ( 𝑥 ↦→ 𝑣; 𝑠 )            Frame                     𝑜                     ::=   ( 𝐶; 𝑓 ↦→ 𝑣 )   Object
         𝜒    ::=     ( 𝛼 ↦→ 𝑜 )                   Heap                  𝑣                     ::=   𝛼 | null        Value


Fig. 4. ℒ𝑢𝑙 Syntax. We use 𝑥, 𝑦, 𝑧 for variables, 𝐶, 𝐷 for class identifiers, 𝑓 for field identifier, 𝑔𝑓 for ghost
field identifiers, 𝑚 for method identifiers, 𝛼 for addresses.


         mapped in the top-most frame of 𝜎’s stack, and ⌊𝑒.𝑓 ⌋ 𝜎 looks up in 𝜎’s heap the value of 𝑓
         for the object ⌊𝑒⌋ 𝜎 .
       • 𝜙 [𝑥 ↦→ 𝛼] updates the variable map of 𝜙, and 𝜎 [𝑥 ↦→ 𝛼] updates the top frame of 𝜎. 𝐴[e/𝑥]
         is textual substitution where we replace all occurrences of 𝑥 in 𝐴 by e.
       • As usual, 𝑞 stands for sequence 𝑞 1 , ... 𝑞𝑛 , where 𝑞 can be an address, a variable, a frame, an
         update or a substitution. Thus, 𝜎 [𝑥 ↦→ 𝛼] and 𝐴[𝑒/𝑦] have the expected meaning.
       • 𝜙 .cont is the continuation of frame 𝜙, and 𝜎.cont is the continuation in the top frame.
                txt
       • 𝑡𝑒𝑥𝑡 1 = 𝑡𝑒𝑥𝑡 2 expresses that 𝑡𝑒𝑥𝑡 1 and 𝑡𝑒𝑥𝑡 2 are the same text.
       • We define the depth of a stack as |𝜙 1 ...𝜙𝑛 | ≜ 𝑛. For states, |(𝜙, 𝜒)| ≜ |𝜙 |. The operator 𝜎 [𝑘]
         truncates the stack up to the 𝑘-th frame: (𝜙 1 ...𝜙𝑘 ...𝜙𝑛 , 𝜒) [𝑘] ≜ (𝜙 1 ...𝜙𝑘 , 𝜒)
       • 𝑉𝑠 (𝑠𝑡𝑚𝑡) returns the variables which appear in 𝑠𝑡𝑚𝑡. For example,𝑉𝑠 (𝑢 := 𝑦.𝑓 )={𝑢, 𝑦}.

3.2      ℒ𝑢𝑙 Execution
Fig. 5 describes ℒ𝑢𝑙 execution by a small steps operational semantics with shape 𝑀; 𝜎 d 𝜎 ′ . 𝑀
stands for one or more modules, where a module, 𝑀, maps class names to class definitions. The
functions classOf(𝜎, 𝑥), Meth(𝑀, 𝐶, 𝑚), 𝑓 𝑖𝑒𝑙𝑑𝑠 (𝑀, 𝐶), 𝑆𝑎𝑚𝑒𝑀𝑜𝑑𝑢𝑙𝑒 (𝑥, 𝑦, 𝜎, 𝑀), and 𝑃𝑟𝑚𝑠 (𝜎, 𝑀),
return the class of 𝑥, the method 𝑚 for class 𝐶, the fields for class 𝐶, whether 𝑥 and 𝑦 belong to the
same module, and the formal parameters of the method currently executing in 𝜎 – c.f. Defs A.2 –
A.7. Initial states, Initial(𝜎), contain a single frame with single variable this pointing to a single
object in the heap and a continuation, c.f. def:initial.
   The semantics is unsurprising: The top frame’s continuation (𝜎.cont) contains the statement to
be executed next. We dynamically enforce a simple form of module-wide privacy: Fields may be
read or written only if they belong to an object (here 𝑦) whose class comes from the same module
as the class of the object reading or writing the fields (this). 9 Wlog, to simplify some proofs we
require, as in Kotlin, that method bodies do not assign to formal parameters.
   Private methods may be called only if the class of the callee (the object whose method is being
called – here 𝑦0 ) comes from the same module as the class of the caller (here this). Public methods
may always be called. When a method is called, a new frame is pushed onto the stack; this frame
maps this and the formal parameters to the values for the receiver and other arguments, and the
continuation to the body of the method. Method bodies are expected to store their return values in

9 More fine-grained privacy, e.g. C++ private fields or ownership types, would provide all the guarantees needed in our work.



, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                               11


                         txt
             𝜎 .cont = 𝑥 := 𝑦.𝑓 ; 𝑠𝑡𝑚𝑡               𝑥 ∉ 𝑃𝑟𝑚𝑠 (𝜎, 𝑀 )    𝑆𝑎𝑚𝑒𝑀𝑜𝑑𝑢𝑙𝑒 (this, 𝑦, 𝜎, 𝑀 )
                                                                                                            (Read)
                                   𝑀, 𝜎 d 𝜎 [𝑥 ↦→ ⌊𝑦.𝑓 ⌋ 𝜎 } ] [cont ↦→ 𝑠𝑡𝑚𝑡 ]

                                   txt
                           𝜎 .cont = 𝑥 .𝑓 := 𝑦; 𝑠𝑡𝑚𝑡          𝑆𝑎𝑚𝑒𝑀𝑜𝑑𝑢𝑙𝑒 (this, 𝑥, 𝜎, 𝑀 )
                                                                                                (Write)
                                 𝑀, 𝜎 d 𝜎 [ ⌊𝑥 ⌋ 𝜎 .𝑓 ↦→ ⌊𝑦 ⌋ 𝜎 ] [cont ↦→ 𝑠𝑡𝑚𝑡 ]

                   txt
           𝜎 .cont = 𝑥 := new 𝐶; 𝑠𝑡𝑚𝑡                𝑥 ∉ 𝑃𝑟𝑚𝑠 (𝜎, 𝑀 )     fields(𝑀, 𝐶 ) = 𝑓     𝛼 fresh in 𝜎
                                                                                                                 (New)
                          𝑀, 𝜎 d 𝜎 [𝑥 ↦→ 𝛼 ] [𝛼 ↦→ ( 𝐶; 𝑓 ↦→ null ) ] [cont ↦→ 𝑠𝑡𝑚𝑡 ]

                                         txt
                           𝜙𝑛 .cont = 𝑢 := 𝑦0 .𝑚 (𝑦); _       𝑢 ∉ 𝑃𝑟𝑚𝑠 ( (𝜙 · 𝜙𝑛 , 𝜒 ), 𝑀 )
                         Meth(𝑀, classOf( (𝜙𝑛 , 𝜒 ), 𝑦0 ), 𝑚) = 𝑝 𝐶 ::𝑚 (𝑥 : 𝑇 ): 𝑇 { 𝑠𝑡𝑚𝑡 }
                             𝑝 = public ∨ 𝑆𝑎𝑚𝑒𝑀𝑜𝑑𝑢𝑙𝑒 (this, 𝑦0 , (𝜙𝑛 , 𝜒 ), 𝑀 )
                                                                                                        (Call)
                  𝑀, (𝜙 · 𝜙𝑛 , 𝜒 ) d (𝜙 · 𝜙𝑛 · ( this ↦→ ⌊𝑦0 ⌋ 𝜙𝑛 , 𝑥 ↦→ ⌊𝑦 ⌋ 𝜙𝑛 ; 𝑠𝑡𝑚𝑡 ), 𝜒 )

                                               txt                txt
                               𝜙𝑛+1 .cont = 𝜖           𝜙𝑛 .cont = 𝑥 := 𝑦0 .𝑚 (𝑦); 𝑠𝑡𝑚𝑡
                                                                                                      (Return)
                 𝑀, (𝜙 · 𝜙𝑛 · 𝜙𝑛+1 , 𝜒 ) d (𝜙 · 𝜙𝑛 [𝑥 ↦→ ⌊res⌋ 𝜙𝑛+1 ] [cont ↦→ 𝑠𝑡𝑚𝑡 ], 𝜒 )

                                                 Fig. 5. ℒ𝑢𝑙 operational Semantics


the implicitly defined variable res10 . When the continuation is empty (𝜖), the frame is popped and
the value of res from the popped frame is stored in the variable map of the top frame.
   Thus, when 𝑀; 𝜎 d 𝜎 ′ is within the same method we have |𝜎 ′ |= |𝜎 |; when it is a call we have
|𝜎 |= |𝜎 | + 1; and when it is a return we have |𝜎 ′ |= |𝜎 | − 1. Fig. 3 from §2 distinguishes d execution
  ′

steps into: steps within the same call (→), entering a method (↑), returning from a method (↓).
Therefore 𝑀; 𝜎8 d 𝜎9 is a step within the same call, 𝑀; 𝜎9 d 𝜎10 is a method entry with 𝑀; 𝜎12 d 𝜎13
the corresponding return. In general, 𝑀; 𝜎 d ∗ 𝜎 ′ may involve any number of calls or returns: e.g.
𝑀; 𝜎10 d ∗ 𝜎15 , involves no calls and two returns.

3.3    Fundamental Concepts
The novel features of our assertions — protection and scoped invariants — are both defined in
terms of the current point of execution. Therefore, for the semantics of our assertions we need to
represent calls and returns, scoped execution, and (in)directly accessible objects.
3.3.1 Method Calls and Returns. These are characterized through pushing/popping frames : 𝜎 ▽ 𝜙
pushes frame 𝜙 onto the stack of 𝜎, while 𝜎 △ pops the top frame and updates the continuation
and variable map.
Definition 3.1. Given a state 𝜎, and a frame 𝜙, we define
      • 𝜎 ▽ 𝜙 ≜ (𝜙 · 𝜙, 𝜒) if 𝜎 = (𝜙, 𝜒).
      • 𝜎 △ ≜ (𝜙 · (𝜙𝑛 [cont ↦→ 𝑠𝑡𝑚𝑡] [𝑥 ↦→ ⌊res⌋ 𝜙𝑛 ]), 𝜒) if
                                                      txt
                𝜎 = (𝜙 · 𝜙𝑛 · 𝜙𝑛+1, 𝜒), and 𝜙𝑛 (cont) = 𝑥 := 𝑦0 .𝑚(𝑦); 𝑠𝑡𝑚𝑡
Consider Fig. 3 again: 𝜎8 = 𝜎7 ▽ 𝜙 for some 𝜙, and 𝜎15 =𝜎14 △ .
3.3.2 Scoped Execution. In order to give semantics to scoped invariants (introduced in §2.2.2 and
to be fully defined in Def. 5.4), we need a new definition of execution, called scoped execution.
Definition 3.2 (Scoped Execution). Given modules 𝑀, and states 𝜎, 𝜎1 , 𝜎𝑛 , and 𝜎 ′ , we define:
10 For ease of presentation, we omit assignment to res in methods returning void.



                                                                        , Vol. 1, No. 1, Article . Publication date: November 2025.
12                                                 Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


      • 𝑀; 𝜎 ⇝ 𝜎 ′           ≜    𝑀; 𝜎 d 𝜎 ′ ∧ |𝜎 | ≤ |𝜎 ′ |
      • 𝑀; 𝜎1 ⇝∗𝜎𝑛           ≜    𝜎1 = 𝜎𝑛 ∨ ∃𝜎2, ...𝜎𝑛−1 .∀𝑖 ∈ [1..𝑛) [ 𝑀; 𝜎𝑖 d 𝜎𝑖+1 ∧ |𝜎1 | ≤ |𝜎𝑖+1 | ]
      • 𝑀; 𝜎⇝∗fin 𝜎 ′        ≜    𝑀; 𝜎⇝∗𝜎 ′ ∧ |𝜎 | = |𝜎 ′ | ∧ 𝜎 ′ .cont = 𝜖
   Consider Fig. 3 : Here |𝜎8 | ≤ |𝜎9 | and thus 𝑀; 𝜎8 ⇝ 𝜎9 . Also, 𝑀; 𝜎14 d 𝜎15 but |𝜎14 | ≰ |𝜎15 | (this
step returns from the active call in 𝜎14 ), and hence 𝑀; 𝜎14 ̸⇝ 𝜎15 . Finally, even though |𝜎8 | = |𝜎18 |
and 𝑀; 𝜎8 d∗ 𝜎18 , we have 𝑀; 𝜎8 ⇝      ̸ ∗𝜎18 : This is so, because the execution 𝑀; 𝜎8 d ∗ 𝜎18 goes
through the step 𝑀; 𝜎14 d 𝜎15 and |𝜎8 | ≰ |𝜎15 | (this step returns from the active call in 𝜎8 ).
  The relation ⇝∗ contains more than the transitive closure of ⇝. E.g.,, 𝑀; 𝜎9 ⇝∗𝜎13 , even though
𝑀; 𝜎9 ⇝ 𝜎12 and 𝑀; 𝜎12 ⇝ ̸ ∗𝜎13 . Lemma 3.3 says that the value of the parameters does not change
during execution of the same method. Appendix B discusses proofs, and further properties.
Lemma 3.3. For all 𝑀, 𝜎, 𝜎 ′ :           𝑀; 𝜎⇝∗𝜎 ′ ∧ |𝜎 | = |𝜎 ′ |          =⇒ ∀𝑥 ∈ 𝑃𝑟𝑚𝑠 (𝑀, 𝜎).[ ⌊𝑥⌋ 𝜎 = ⌊𝑥⌋ 𝜎 ′ ]
3.3.3 Reachable Objects, Locally Reachable Objects, and Well-formed States. To define protection
(no external object indirectly accessible from the top frame has access to the protected object, c.f.
§ 2.2.1) we first define reachability. An object 𝛼 is locally reachable, i.e. 𝛼 ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎), if it is
reachable from the top frame on the stack of 𝜎.
Definition 3.4. We define
   • 𝑅𝑐ℎ𝑏𝑙 (𝛼, 𝜎)  ≜ { 𝛼 ′ | ∃𝑛 ∈ N.∃𝑓1, ...𝑓𝑛 .[ ⌊𝛼 .𝑓1 ...𝑓𝑛 ⌋ 𝜎 = 𝛼 ′ ] }.
   • 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎) ≜ { 𝛼 | ∃𝑥 ∈ 𝑑𝑜𝑚(𝜎) ∧ 𝛼 ∈ 𝑅𝑐ℎ𝑏𝑙 ( ⌊𝑥⌋ 𝜎 , 𝜎) }.
   In well-formed states, 𝑀 |= 𝜎, the value of a parameter in any callee (𝜎 [𝑘]) is also the value of
some variable in the caller (𝜎 [𝑘 −1]), and any address reachable from any frame (𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 [𝑘]))
is reachable from some formal parameter of that frame.
Definition 3.5 (Well-formed states). For modules 𝑀, and states 𝜎, 𝜎 ′ :
  𝑀 |= 𝜎 ≜ ∀𝑘 ∈ N.[ 1 < 𝑘 ≤ |𝜎 | =⇒
               [ ∀𝑥 ∈ 𝑃𝑟𝑚𝑠 (𝜎 [𝑘], 𝑀).[ ∃𝑦. ⌊𝑥⌋ 𝜎 [𝑘 ] = ⌊𝑦⌋ 𝜎 [𝑘−1] ]          ∧
                                   Ð
                 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 [𝑘]) = 𝑧 ∈𝑃𝑟𝑚𝑠 (𝜎 [𝑘 ],𝑀 ) 𝑅𝑐ℎ𝑏𝑙 ( ⌊𝑧⌋ 𝜎 [𝑘 ] , 𝜎)   ]
  Lemma 3.6 says that (1) execution preserves well-formedness, and (2) any object which is locally
reachable after pushing a frame was locally reachable before pushing that frame.
Lemma 3.6. For all modules 𝑀, states 𝜎, 𝜎 ′ , and frame 𝜙:
  (1) 𝑀 |= 𝜎 ∧ 𝑀, 𝜎 d 𝜎 ′ =⇒ 𝑀 |= 𝜎 ′
  (2) 𝜎 ′ = 𝜎 ▽ 𝜙 ∧ 𝑀 |= 𝜎 ′ =⇒ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 ′ ) ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎)

4     Assertions
Our assertions are standard (e.g. properties of the values of expressions, connectives, quantification
etc.) or about protection (i.e. ⟨ e⟩⟩←
                                     ×− e and ⟨ e⟩⟩ ).
Definition 4.1. Assertions, 𝐴, are defined as follows:
   𝐴 ::= e | e : 𝐶 | ¬𝐴 | 𝐴 ∧ 𝐴 | ∀𝑥 : 𝐶.𝐴 | e : extl | ⟨ e⟩⟩←
                                                             ×− e | ⟨ e⟩⟩                                         11

     𝐹𝑣 (𝐴) returns the free variables in 𝐴; for example, 𝐹𝑣 (𝑎 :𝐴𝑐𝑐𝑜𝑢𝑛𝑡 ∧ ∀𝑏 : 𝑖𝑛𝑡 .[𝑎.blnce = 𝑏])={𝑎}.
Definition 4.2 (Shorthands). We write e : intl for ¬(e : extl), and extl. resp. intl for
this : extl resp. this : intl. Forms such as 𝐴 → 𝐴′ , 𝐴 ∨ 𝐴′ , and ∃𝑥 : 𝐶.𝐴 can be encoded.
11 Addresses in assertions as e.g. in 𝛼 .𝑏𝑙𝑛𝑐𝑒 > 700, are useful when giving semantics to universal quantifiers c.f. Def. 4.3.(5),

when the local map changes e.g. upon call and return, and in general, for scoped invariants, c.f. Def. 5.4.

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                         13


Satisfaction of Assertions by a module and a state is expressed through 𝑀, 𝜎 |= 𝐴 and defined by
cases on the shape of 𝐴, in definitions 4.3 and 4.4. 𝑀 is used to look up the definitions of ghost
fields, and to find class definitions to determine whether an object is external.

4.1    Semantics of Assertions – First Part
To determine satisfaction of an expression, we use the evaluation relation, 𝑀, 𝜎, 𝑒 ↩→ 𝑣, which says
that the expression 𝑒 evaluates to value 𝑣 in the context of state 𝜎 and module 𝑀. Ghost fields
may be recursively defined, thus evaluation of e might not terminate. Nevertheless, the logic of
assertions remains classical because recursion is restricted to expressions.
Definition 4.3 (Satisfaction of Assertions – first part). We define satisfaction of an assertion 𝐴 by
a state 𝜎 with module 𝑀 as:
   (1) 𝑀, 𝜎 |= e ≜ 𝑀, 𝜎, e ↩→ true
   (2) 𝑀, 𝜎 |= e : 𝐶 ≜ 𝑀, 𝜎, e ↩→ 𝛼 ∧ classOf(𝛼, 𝜎) = 𝐶
   (3) 𝑀, 𝜎 |= ¬𝐴 ≜ 𝑀, 𝜎 ̸ |= 𝐴
   (4) 𝑀, 𝜎 |= 𝐴1 ∧ 𝐴2 ≜ 𝑀, 𝜎 |= 𝐴1 ∧ 𝑀, 𝜎 |= 𝐴2
   (5) 𝑀, 𝜎 |= ∀𝑥 : 𝐶.𝐴 ≜ ∀𝛼 .[ 𝑀, 𝜎 |= 𝛼 : 𝐶 =⇒ 𝑀, 𝜎 |= 𝐴[𝛼/𝑥] ]
   (6) 𝑀, 𝜎 |= e : extl ≜ ∃𝐶.[ 𝑀, 𝜎 |= e : 𝐶 ∧ 𝐶 ∉ 𝑀 ]
   Note that while execution takes place in the context of one or more modules, 𝑀, satisfaction
of assertions considers exactly one module 𝑀 – the internal module. 𝑀 is used to look up the
definitions of ghost fields, and to determine whether objects are external.

4.2    Semantics of Assertions - Second Part
In §2.2.1 we introduced protection – we will now formalize this concept.
   An object is protected from another object, ⟨ 𝛼⟩⟩←  ×− 𝛼𝑜 , if the two objects are not equal, and no
external object reachable from 𝑎𝑜 has a field pointing to 𝛼. This ensures that the last element on
any path leading from 𝛼𝑜 to 𝛼 in an internal object.
   An object is protected, ⟨ 𝛼⟩⟩ , if no external object reachable from any of the current frame’s
arguments has a field pointing to 𝛼; and furthermore, if the receiver is external, then no parameter
to the current method call directly refers to 𝛼. This ensures that no external object reachable from
the current receiver or arguments can “obtain” 𝛼, where obtain 𝛼 is either direct access through a
field, or by virtue of the method’s receiver being able to see all the arguments.
Definition 4.4 (Satisfaction of Assertions – Protection). – continuing definitions in 4.3:
  (1) 𝑀, 𝜎 |= ⟨ e⟩⟩←
                   ×− e𝑜 ≜ ∃𝛼, 𝛼𝑜 .[
    (a) 𝑀, 𝜎, e ↩→ 𝛼 ∧ 𝑀, 𝜎, e𝑜 ↩→ 𝛼𝑜 ∧ 𝛼 ≠ 𝛼 0 ,
    (b) ∀𝛼 ′ ∈ 𝑅𝑐ℎ𝑏𝑙 (𝛼𝑜 , 𝜎).∀𝑓 .[ 𝑀, 𝜎 |= 𝛼 ′ : extl =⇒ ⌊𝛼 ′ .𝑓 ⌋ 𝜎 ≠ 𝛼 ] ].
  (2) 𝑀, ⟨ e⟩⟩ |= ≜ ∃𝛼 .[
    (a) 𝑀, 𝜎, e ↩→ 𝛼,
    (b) 𝑀, 𝜎 |= extl =⇒ ∀𝑥 ∈ 𝜎. 𝑀, 𝜎 |= 𝑥 ≠ 𝛼,
    (c) ∀𝛼 ′ ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎).∀𝑓 .[ 𝑀, 𝜎 |= 𝛼 ′ : extl =⇒ ⌊𝛼 ′ .𝑓 ⌋ 𝜎 ≠ 𝛼 ] ].
   We illustrate “protected” and “protected from” in Fig. 2 in §2. and Fig. 12 in App. C. In general,
⟨ 𝛼⟩⟩←×− 𝛼𝑜 ensures that 𝛼𝑜 will get access to 𝛼 only if another object grants that access. Similarly,
⟨ 𝛼⟩⟩ ensures that during execution of the current method, no external object will get direct access
to 𝛼 unless some internal object grants that access12 . Thus, protection together with protection
preservation (i.e. no internal object gives access) guarantee lack of eventual external access.
12 This is in line with the motto "only connectivity begets connectivity" from [84].



                                                                  , Vol. 1, No. 1, Article . Publication date: November 2025.
14                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


4.2.1 Discussion. Lack of eventual direct access is a central concept in the verification of code
with calls to and callbacks from untrusted code. It has already been over-approximated in several
different ways, e.g. 2nd-class [96, 119] or borrowed (“2nd-hand”) references [15, 24], textual modules
[76], information flow [112], runtime checks [4], abstract data type exports [71], separation-based
invariants Iris [49, 101], – more in § 8. In general, protection is applicable in more situations (i.e. is
less restrictive) than most of these approaches, although more restrictive than the ideal “lack of
eventual access”.

An alternative definition might consider 𝛼 as protected from 𝛼𝑜 , if any path from
𝛼𝑜 to 𝛼 goes through at least one internal object. With this definition, 𝑜 4 would be
protected from 𝑜 1 in the heap shown here. However, 𝑜 1 can make a call to 𝑜 2 , and
this call could return 𝑜 3 . Once 𝑜 1 has direct access to 𝑜 3 , it can also get direct access
to 𝑜 4 . The example justifies our current definition.
4.3     Preservation of Assertions
Program logics require some form of framing, i.e. conditions under which satisfaction of assertions
is preserved across program execution. This is the subject of the current subsection.
   Def. 4.5 turns an assertion 𝐴 to the equivalent variable-free from by replacing all free variables
from 𝐴 by their values in 𝜎. Then, Lemma 4.5 says that satisfaction of an assertion is not affected
by replacing free variables by their values, nor by changing the sate’s continuation.
Definition and Lemma 4.5. For all 𝑀, 𝜎, 𝑠𝑡𝑚𝑡, 𝐴, and 𝑥 where 𝑥 = 𝐹𝑣 (𝐴):
   • 𝜎⌈𝐴⌉ ≜ 𝐴[⌊𝑥⌋ 𝜎 /𝑥]
   • 𝑀, 𝜎 |= 𝐴 ⇐⇒ 𝑀, 𝜎 |= 𝜎⌈𝐴⌉ ⇐⇒ 𝑀, 𝜎 [cont ↦→ 𝑠𝑡𝑚𝑡] |= 𝐴
We now move to assertion preservation across method call and return.
4.3.1 Stability. In most program logics, satisfaction of variable-free assertions is preserved when
pushing/popping frames – i.e. immediately after entering a method or returning from it. But this is
not so for our assertions, where protection depends on the heap but also on the range of the top
frame. E.g., Fig. 2: 𝜎2 ̸ |= ⟨𝑜 6 ⟩ , but after pushing a frame, we have 𝜎3 |= ⟨𝑜 6 ⟩ .
    Assertions which do not contain ⟨ _⟩⟩ are called 𝑆𝑡𝑏𝑙 (_), while assertions which do not contain
⟨ _⟩⟩ in negative positions are called 𝑆𝑡𝑏 + (_). Sect 4.3.2 shows some examples. Lemma 4.6 says
that 𝑆𝑡𝑏𝑙 (_) assertions are preserved when pushing/popping frames, and 𝑆𝑡𝑏 + (_) assertions are
preserved when pushing internal frames. C.f. Appendix D for definitions and proofs.
Lemma 4.6. For all states 𝜎, frames 𝜙, all assertions 𝐴 with 𝐹𝑣 (𝐴) = ∅
   • 𝑆𝑡𝑏𝑙 (𝐴) =⇒ [ 𝑀, 𝜎 |= 𝐴 ⇐⇒ 𝑀, 𝜎 ▽ 𝜙 |= 𝐴 ]
   • 𝑆𝑡𝑏 + (𝐴) ∧ 𝑀 · 𝑀 |= 𝜎 ▽ 𝜙 ∧ 𝑀, 𝜎 ▽ 𝜙 |= intl ∧ 𝑀, 𝜎 |= 𝐴 =⇒                           𝑀, 𝜎 ▽ 𝜙 |= 𝐴
     While 𝑆𝑡𝑏 + assertions are preserved when pushing internal frames, they are not necessarily
preserved when pushing external frames nor when popping frames (c.f. Ex. 4.7).
Example 4.7. Fig. 2 illustrates that
– 𝑆𝑡𝑏 + not necessarily preserved by External Push: Namely, 𝜎2 |= ⟨𝑜 4 ⟩ , pushing frame 𝜙 3 with an
external receiver and 𝑜 4 as argument gives 𝜎3 , we have 𝜎3 ̸ |= ⟨𝑜 4 ⟩ .
 – 𝑆𝑡𝑏 + not necessarily preserved by Pop: Namely, 𝜎3 |= ⟨𝑜 6 ⟩ , returning from 𝜎3 would give 𝜎2 , and
we have 𝜎2 ̸ |= ⟨𝑜 6 ⟩ .
   We work with 𝑆𝑡𝑏 + assertions (the 𝑆𝑡𝑏𝑙 requirement is too strong). But we need to address the
lack of preservation of 𝑆𝑡𝑏 + assertions for external method calls and returns. We do the former
through adaptation (−▽ in Sect 6.2.2), and the latter through deep satisfaction (§7).

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                   15


4.3.2 Encapsulation. As external code is unknown, it could, in principle, have unlimited effect
and invalidate any assertion, and thus make reasoning about external calls impossible. However,
because fields are private, assertions which read internal fields only, cannot be invalidated by
external execution steps. Reasoning about external calls relies on such encapsulated assertions.
   Judgment 𝑀 ⊢ 𝐸𝑛𝑐 (𝐴), defined in D.4, requires that 𝐴 looks up the contents of internal objects
only, that 𝐴 does not contain ⟨ _⟩⟩ in negative positions, nor does it contain ⟨ _⟩⟩←
                                                                                    ×− _ in any position.
Lemma 4.8 says that 𝑀 ⊢ 𝐸𝑛𝑐 (𝐴) implies that any external scoped execution step which involves
𝑀 and any set of other modules 𝑀 preserves satisfaction of 𝐴.
Lemma 4.8 (Encapsulation). For all modules 𝑀, and assertions 𝐴:
   • 𝑀 ⊢ 𝐸𝑛𝑐 (𝐴) =⇒ ∀𝑀, 𝜎, 𝜎 ′ .[ 𝑀, 𝜎 |= (𝐴 ∧ extl) ∧ 𝑀 ·𝑀; 𝜎 ⇝ 𝜎 ′ =⇒ 𝑀, 𝜎 ′ |= 𝜎⌈𝐴⌉ ]
The example below compares the judgments 𝑆𝑡𝑏𝑙 (_), 𝑆𝑡𝑏 + (_), and 𝐸𝑛𝑐 (_).
                    z.f ≥ 3      ⟨ x⟩⟩ ¬( ⟨ x⟩⟩ )     ⟨ y⟩⟩←×− x    ¬( ⟨ y⟩⟩←×− x )
         𝑆𝑡𝑏𝑙 (_)     ✓            ×       ×               ✓               ✓
        𝑆𝑡𝑏 + (_)     ✓           ✓        ×               ✓               ✓
         𝐸𝑛𝑐 (_)      ✓           ✓        ×               ×               ×

5     Specifications
5.1    Syntax, Semantics, and Examples of Specifications
Definition 5.1 (Specifications Syntax). We define the syntax of specifications, 𝑆:
                          A
              𝑆 ::=      𝑥 : 𝐶.{𝐴} | { 𝐴 } 𝑝 𝐶 ::𝑚(𝑦 : 𝐶) { 𝐴 } ∥ {𝐴} | 𝑆 ∧ 𝑆
               𝑝 ::= private | public
   In Def. 5.6 later on we describe well-formedness of 𝑆, but we first discuss semantics and some
examples. We use quadruples involving states: 𝑀; 𝑀 |= { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝐴′′ } says that if 𝜎 satisfies
𝐴, then any terminating scoped execution of its continuation (𝑀 ·𝑀; 𝜎⇝∗fin 𝜎 ′ ) will satisfy 𝐴′ , and
any intermediate reachable external state (𝑀 ·𝑀; 𝜎⇝∗𝜎 ′′ ) will satisfy the “mid-condition”, 𝐴′′ .
Definition 5.2. For modules 𝑀, 𝑀, state 𝜎, and assertions 𝐴, 𝐴′ and 𝐴′′ , we define:
   • 𝑀; 𝑀 |= { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝐴′′ } ≜ ∀𝜎 ′, 𝜎 ′′ .[
       𝑀, 𝜎 |= 𝐴 =⇒ [ 𝑀 ·𝑀; 𝜎⇝∗fin 𝜎 ′ =⇒ 𝑀, 𝜎 ′ |= 𝐴′ ] ∧
                       [ 𝑀 ·𝑀; 𝜎⇝∗𝜎 ′′ =⇒ 𝑀, 𝜎 ′′ |= (extl → 𝜎⌈𝐴′′ ⌉) ] ]
Example 5.3. Consider ...; ... |= { 𝐴1 } 𝜎4 { 𝐴2 } ∥ { 𝐴3 } for Fig. 3. It means that if 𝜎4 satisfies 𝐴1 ,
then 𝜎23 will satisfy 𝐴2 , while 𝜎6 -𝜎9 , 𝜎13 -𝜎17 , and 𝜎20 -𝜎21 will satisfy 𝐴3 . It does not imply anything
about 𝜎24 because ...; 𝜎4 ⇝ ̸ ∗𝜎24 . Similarly, if 𝜎8 satisfies 𝐴1 then 𝜎14 will satisfy 𝐴2 , and 𝜎8 , 𝜎9 , 𝜎13 ,
𝜎14 will satisfy 𝐴3 , while making no claims about 𝜎10 , 𝜎11 , 𝜎12 , nor about 𝜎15 onwards.
                            A
   Now we define 𝑀 |= 𝑥 : 𝐶.{𝐴} to mean that if an external state 𝜎 satisfies 𝐴, then all future
external states reachable from 𝜎—including nested calls and returns but stopping before returning
from the active call in 𝜎— also satisfy 𝐴. And 𝑀 |= { 𝐴1 } 𝑝 𝐷 ::𝑚(𝑦 : 𝐷) { 𝐴2 } ∥ {𝐴3 } means that
scoped execution of a call to 𝑚 from 𝐷 in states satisfying 𝐴1 leads to final states satisfying 𝐴2 (if it
terminates), and to intermediate external states satisfying 𝐴3 .
Definition 5.4 (Semantics of Specifications). We define 𝑀 |= 𝑆 by cases over 𝑆:
             A
  (1) 𝑀 |= 𝑥 : 𝐶.{𝐴} ≜ ∀𝑀, 𝜎.[ 𝑀; 𝑀 |= { extl ∧ 𝑥 : 𝐶 ∧ 𝐴 } 𝜎 { 𝐴 } ∥ { 𝐴 } ].
  (2) 𝑀 |= { 𝐴1 } 𝑝 𝐷 ::𝑚(𝑦 : 𝐷) { 𝐴2 } ∥ {𝐴3 } ≜
                              txt
       ∀𝑀, 𝜎, 𝑦0, 𝑦.[ 𝜎.cont = 𝑢 := 𝑦0 .𝑚(𝑦1, ..𝑦𝑛 ) =⇒
                      𝑀; 𝑀 |= { 𝑦0 : 𝐷, 𝑦 : 𝐷 ∧ 𝐴[𝑦0 /this] } 𝜎 { 𝐴2 [𝑢/𝑟𝑒𝑠, 𝑦0 /this] } ∥ { 𝐴3 } ]

                                                            , Vol. 1, No. 1, Article . Publication date: November 2025.
16                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


     (3) 𝑀 |= 𝑆 ∧ 𝑆 ′       ≜     𝑀 |= 𝑆 ∧ 𝑀 |= 𝑆 ′
                                                              A
   Fig. 3 in §2.2.2 illustrated the meaning of 𝑥 : 𝐶.{𝐴0 }. Moreover, 𝑀𝑔𝑜𝑜𝑑 |= 𝑆 2 ∧ 𝑆 3 ∧ 𝑆 4 , and
𝑀 𝑓 𝑖𝑛𝑒 |= 𝑆 2 ∧ 𝑆 3 ∧ 𝑆 4 , while 𝑀𝑏𝑎𝑑 ̸ |= 𝑆 2 . More examples below and in Appendix E.
Example 5.5 (Scoped Invariants and Method Specs). 𝑆 5 says that non-null keys are immutable:
                   A
       𝑆5 ≜        a : Account, k : Key.{null ≠ k = a.key}
𝑆 9 guarantees that set preserves the protectedness of any account, and any key.
        𝑆 9 ≜ { 𝑎 : Account, 𝑎 ′ : Account ∧ ⟨ 𝑎⟩⟩ ∧ ⟨ 𝑎 ′ .key⟩⟩ }
                       public Account :: set(key’ : Key)
                  { ⟨ 𝑎⟩⟩ ∧ ⟨ 𝑎 ′ .key⟩⟩ } ∥ {⟨⟨𝑎⟩⟩ ∧ ⟨ 𝑎 ′ .key⟩⟩ }
Note that 𝑎, 𝑎 ′ are disjoint from this and the formal parameters of set. In that sense, 𝑎 and 𝑎 ′ are
universally quantified; a call of set will preserve protectedness for all accounts and their keys.

5.2     Well-formed Specifications
We now define what it means for a specification to be well-formed:
Definition 5.6. Well-formedness of specifications, ⊢ 𝑆, is defined by cases on 𝑆:
           A
   • ⊢ 𝑥 : 𝐶.{𝐴} ≜ 𝐹𝑣 (𝐴) ⊆ {𝑥 } ∧ 𝑀 ⊢ 𝐸𝑛𝑐 (𝑥 : 𝐶 ∧ 𝐴).
   • ⊢ { 𝑥 : 𝐶 ′ ∧ 𝐴 } 𝑝 𝐶 ::𝑚(𝑦 : 𝐶) { 𝐴′ } ∥ {𝐴′′ } ≜
          [ res, this ∉𝑥, 𝑦 ∧ 𝐹𝑣 (𝐴) ⊆ 𝑥, 𝑦, this ∧ 𝐹𝑣 (𝐴′ ) ⊆ 𝑥, 𝑦, this, res ∧ 𝐹𝑣 (𝐴′′ ) ⊆ 𝑥
            ∧ 𝑆𝑡𝑏 + (𝐴) ∧ 𝑆𝑡𝑏 + (𝐴′ ) ∧ 𝑀 ⊢ 𝐸𝑛𝑐 (𝑥 : 𝐶 ′ ∧ 𝐴′′ ) ]
   • ⊢ 𝑆 ∧ 𝑆 ′ ≜ ⊢ 𝑆 ∧ ⊢ 𝑆 ′.
   Def 5.6’s requirements about free variables are relatively straightforward – c.f. §E.1.1.
   Def 5.6’s requirements about encapsulation are motivated by Def. 5.4. If 𝑥 : 𝐶 ∧ 𝐴 in the scoped
invariant were not encapsulated, then it could be invalidated by some external code, and it would
be impossible to ever satisfy Def. 5.4(1). Similarly, if a method specification’s mid-condition, 𝐴′′ ,
could be invalidated by some external code, then it would be impossible to ever satisfy Def. 5.4(2).
   Def 5.6’s requirements about stability are motivated by our Hoare logic rule for internal calls,
[Call_Int], Fig 7. The requirement 𝑆𝑡𝑏 + (𝐴) for the method’s precondition gives that 𝐴 is preserved
when an internal frame is pushed, c.f. Lemma 4.6. The requirement 𝑆𝑡𝑏 + (𝐴′ ) for the method’s
postcondition gives, in the context of deep satisfaction, that 𝐴′ is preserved when an internal frame
is popped, c.f. Lemma H.42. This is crucial for soundness of [Call_Int].
   In §Appendix ?? we discuss the encapsulation requirements, and why these do not restrict
expressiveness.

5.3     Discussion
Difference with Object and History Invariants. Our scoped invariants are similar to, but different
from, history invariants and object invariants. We compare through an example:

State 𝜎𝑎 is making a call transitioning to 𝜎𝑏 , execution of 𝜎𝑏 ’s continuation
eventually results in 𝜎𝑐 , and 𝜎𝑐 returns to 𝜎𝑑 . Suppose all four states are external,
                                    A
and the module guarantees 𝑥 : 𝑂𝑏 𝑗𝑒𝑐𝑡 .{𝐴}, and 𝜎𝑎 ̸ |= 𝐴, but 𝜎𝑏 |= 𝐴. Scoped
invariants ensure 𝜎𝑐 |= 𝐴, but allow 𝜎𝑑 ̸ |= 𝐴.
   History invariants [28, 68, 70], instead, consider all future states including any method returns, and
therefore would require that 𝜎𝑑 |= 𝐴. Thus, they are, for our purposes, both unenforceable and overly
                                      txt
restrictive. Unenforceable: Take 𝐴 = ⟨ acc.key⟩⟩ , assume in 𝜎𝑎 a path to an external object which
has access to acc.key, assume that path is unknown in 𝜎𝑏 : then, the transition from 𝜎𝑏 to 𝜎𝑐 cannot

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                             17

                                                                        txt
eliminate that path—hence, 𝜎𝑑 ̸ |= ⟨ acc.key⟩⟩ . Restrictive: Take 𝐴 = ⟨ acc.key⟩⟩ ∧ 𝑎.blnce ≥ 𝑏;
then, requiring 𝐴 to hold in all states from 𝜎𝑎 until termination would prevent all future withdrawals
from 𝑎, rendering the account useless.
   Object invariants [9, 67, 82, 83, 91], on the other hand, expect invariants to hold in all (visible)
states, here would require, e.g. that 𝜎𝑎 |= 𝐴. Thus, they are inapplicable for us: They would require,
e.g., that for all acc, in all (visible) states, ⟨ acc.key⟩⟩ , and thus prevent any withdrawals from
any account in any state.
Difference between Postconditions and Invariants. In all method specification examples so far, the
post-condition and mid-condition were identical. However, this need not be so. Assume a method
tempLeak defined in Account, with an external argument extArg, and method body:
        extArg.m(this.key); this.key:=new Key
Then, the assertion ⟨ this.key⟩⟩ is invalidated by the external call extArg.m(this.key),
but is established by this.key:=new Key. Therefore, ⟨ this.key⟩⟩ is a valid post-condition
but not a valid mid-condition. The specification of tempLeak could be
        𝑆 tempLeak ≜ { true }
                                  public Account :: tempLeak(extArg : external)
                              { ⟨ this.key⟩⟩ } ∥ { true }
Expressiveness In §F we argue the expressiveness of our approach through a sequence of capability
patterns studied in related approaches from the literature [34, 76, 98, 100, 112] and written in our
specification language. These approaches are based on temporal logics [76, 98], or on extensions of
Coq/Iris [34, 100, 112], and do not offer Hoare logic rules for external calls.


6     Hoare Logic
We develop an inference system for adherence to our specifications. We distinguish three phases:
   First Phase: We assume an underlying Hoare logic, 𝑀 ⊢𝑢𝑙 {𝐴} 𝑠𝑡𝑚𝑡 {𝐴′ }, and extend it to a
logic 𝑀 ⊢ { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } with the expected meaning, i.e. (*) execution of statement 𝑠𝑡𝑚𝑡 in a
state satisfying 𝐴 will lead to a state satisfying 𝐴′ . These triples only apply to 𝑠𝑡𝑚𝑡’s that do not
contain method calls (even internal) – this is so, because method calls may make further calls to
external methods. In our extension we introduce judgements which talk about protection.
   Second Phase: We develop a logic of quadruples 𝑀 ⊢ { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }. These promise
(*) and in addition, that (**) any intermediate external states reachable during execution of that
𝑠𝑡𝑚𝑡 satisfy the mid-condition 𝐴′′ . We incorporate the triples from the first phase, introduce mid-
conditions, give the usual substructural rules, and deal with method calls. For internal calls we use
the methods’ specs. For external calls, we use the module’s invariants.
   Third Phase: We prove adherence to our specifications. For method specifications we require
that the body maps the precondition to the postcondition and preserves the method’s mid-condition.
For module invariants we require that they are preserved by all public methods of the module.
Preliminaries: The judgement ⊢ 𝑀 : 𝑆 expresses that 𝑆 is part of 𝑀’s specification. In particular,
it allows safe renamings. These renamings are a convenience, akin to the Barendregt convention,
and allow simpler Hoare rules – c.f. Sect. 6.3, Def. G.1, and Ex. G.2. We also require an underlying
Hoare logic with judgements 𝑀 ⊢𝑢𝑙 {𝐴}𝑠𝑡𝑚𝑡 {𝐴′ } – c.f. Ax. G.3.


6.1    First Phase: Triples
In Fig. 6 we introduce our triples, of the form 𝑀 ⊢ { 𝐴 }𝑠𝑡𝑚𝑡 { 𝐴′ }. These promise, as expected,
that any execution of 𝑠𝑡𝑚𝑡 in a state satisfying 𝐴 leads to a state satisfying 𝐴′ .

                                                      , Vol. 1, No. 1, Article . Publication date: November 2025.
18                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


                                        [embed_ul]                                                     [prot-new]
               𝑠𝑡𝑚𝑡 contains no method call                                               txt
       𝑆𝑡𝑏𝑙 (𝐴) 𝑆𝑡𝑏𝑙 (𝐴′ )  𝑀 ⊢𝑢𝑙 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ }                                   𝑢 ≠𝑥
                  𝑀 ⊢ { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ }                             𝑀 ⊢ { 𝑡𝑟𝑢𝑒 } 𝑢 = new 𝐶 { ⟨𝑢⟩⟩ ∧ ⟨𝑢⟩⟩←
                                                                                                        ×− 𝑥 }


                                           [prot-1]                                                    [prot-2]
                                                                                                           txt
      𝑠𝑡𝑚𝑡 is free of meth. cals, or assignment to 𝑧              𝑠𝑡𝑚𝑡 is either 𝑥 := 𝑦 or 𝑥 := 𝑦.𝑓 𝑧, 𝑧 ′ ≠ 𝑥
             𝑀 ⊢ { 𝐴∧e =𝑧 } 𝑠𝑡𝑚𝑡 { e =𝑧 }                         𝑀 ⊢ { 𝐴∧𝑧 =e ∧ 𝑧 ′=e′ } 𝑠𝑡𝑚𝑡 { 𝑧 =e ∧ 𝑧 ′=e′ }
             𝑀 ⊢ { 𝐴∧⟨⟨e⟩⟩ } 𝑠𝑡𝑚𝑡 { ⟨ e⟩⟩ }                        𝑀 ⊢ { 𝐴∧⟨⟨e⟩⟩←   ×− e′ } 𝑠𝑡𝑚𝑡 { ⟨ e⟩⟩←
                                                                                                        ×− e′ }

                                             [prot-3]                                                  [prot-4]
                             txt                                      txt                           txt
                        𝑥 ≠𝑧                                       𝐴 = ⟨ 𝑥⟩⟩←           ×− 𝑦 ′
                                                                            ×− 𝑧 ∧ ⟨ 𝑥⟩⟩←        𝐴′ = ⟨ 𝑥⟩⟩←
                                                                                                           ×− 𝑧
       𝑀 ⊢ { ⟨𝑦.𝑓 ⟩ ←
                    ×− 𝑧 } 𝑥 = 𝑦.𝑓 { ⟨ 𝑥⟩⟩←
                                          ×− 𝑧 }                            𝑀 ⊢ { 𝐴 } 𝑦.𝑓 = 𝑦 ′ { 𝐴′ }

                          Fig. 6. Embedding the Underlying Hoare Logic, and Protection



   With rule embed_ul in Fig. 6, any triple {𝐴}𝑠𝑡𝑚𝑡 {𝐴′ } whose statement does not contain a
method call, and which can be proven in the underlying Hoare logic, can also be proven in our
logic. In Prot-1, we see that protection of an object 𝑜 is preserved by internal code which does not
call any methods: namely any heap modifications will ony affect internal objects, and this will not
expose new, unmitigated external access to 𝑜. Prot-2, Prot-3 and Prot-4 describe the preservation
of relative protection. Proofs of soundness for these rules can be found in App.H.5.1.

6.2     Second Phase: Quadruples
6.2.1 Mid-conditions and Substructural Rules. We now introduce quadruple rules. Rule mid embeds
triples 𝑀 ⊢ { 𝐴 } 𝑠 { 𝐴′ } into quadruples 𝑀 ⊢ { 𝐴 } 𝑠 { 𝐴′ } ∥ { 𝐴′′ }. This is sound, because 𝑠𝑡𝑚𝑡
is guaranteed not to contain method calls (by lemma G.5).
                                                                     [Mid]
                                             𝑀 ⊢ { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ }
                                          𝑀 ⊢ { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }
   Substructural quadruple rules appear in Fig. 19, and are as expected: Rules seq and conseq
are the usual rules for statement sequences and consequence, adapted to quadruples. Rule combine
combines two quadruples for the same statement into one. Rule Absurd allows us to deduce
anything out of false precondition, and Cases allows for case analysis. These rules apply to any
statements – even those containing method calls.

6.2.2 Adaptation. In the outline of the Hoare proof of the external call in §2.3.2, we saw that an
assertion of the form ⟨ 𝑥⟩⟩←
                           ×− 𝑦 at the call site may imply ⟨ 𝑥⟩⟩ at entry to the call. More generally,
the −▽ operator adapts an assertion from the view of the callee to that of the caller, and is used in
the Hoare logic for method calls. It is defined below.

Definition 6.1. [The −▽ operator]
              ⟨ e⟩⟩ −▽𝑦 ≜ ⟨ e⟩⟩←
                               ×− 𝑦                      (𝐴1 ∧ 𝐴2 ) −▽𝑦     ≜   (𝐴1 −▽𝑦) ∧ (𝐴2 −▽𝑦)
      (⟨⟨e⟩⟩←
            ×− 𝑢) −▽𝑦 ≜ ⟨ e⟩⟩← ×− 𝑢                     (∀𝑥 : 𝐶.𝐴) −▽𝑦      ≜   ∀𝑥 : 𝐶.(𝐴−▽𝑦)
     (e : extl) −▽𝑦 ≜ e : extl                                (¬𝐴) −▽𝑦      ≜   ¬(𝐴−▽𝑦)
                  e−▽𝑦 ≜ e                                  (e : 𝐶) −▽𝑦     ≜   e :𝐶

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                 19


   Only the first equation in Def. 6.1 is interesting: for e to be protected at a callee with arguments
𝑦, it should be protected from these arguments – thus ⟨ e⟩⟩ −▽𝑦 = ⟨ e⟩⟩←    ×− 𝑦. The notation ⟨ e⟩⟩←
                                                                                                    ×− 𝑦
stands for ⟨ e⟩⟩← ×− 𝑦0 ∧ ... ∧ ⟨ e⟩⟩←
                                     ×− 𝑦𝑛 , assuming that 𝑦=𝑦0, ...𝑦𝑛 .
   Lemma 6.2 states that indeed, −▽ adapts assertions from the callee to the caller, and is the
counterpart to the ▽ . In particular: (1): −▽ turns an assertion into a stable assertion. (2): If the
caller, 𝜎, satisfies 𝐴 ▽ 𝑅𝑛𝑔(𝜙), then the callee, 𝜎 ▽ 𝜙, satisfies 𝐴. (3): When returning from external
states, an assertion implies its adapted version. (4): When calling from external states, an assertion
implies its adapted version.
Lemma 6.2. For states 𝜎, assertions 𝐴, so that 𝑆𝑡𝑏 + (𝐴) and 𝐹𝑣 (𝐴) = ∅, frame 𝜙, variables 𝑦0 , 𝑦:
  (1) 𝑆𝑡𝑏𝑙 ( 𝐴−▽(𝑦0, 𝑦) )
  (2) 𝑀, 𝜎 |= 𝐴−▽𝑅𝑛𝑔(𝜙)       =⇒ 𝑀, 𝜎 ▽ 𝜙 |= 𝐴
  (3) 𝑀, 𝜎 ▽ 𝜙 |= 𝐴 ∧ extl     =⇒ 𝑀, 𝜎 |= 𝐴−▽𝑅𝑛𝑔(𝜙)
  (4) 𝑀, 𝜎 |= 𝐴 ∧ extl ∧ 𝑀 · 𝑀 |= 𝜎 ▽ 𝜙       =⇒ 𝑀, 𝜎 ▽ 𝜙 |= 𝐴−▽𝑅𝑛𝑔(𝜙)
  Proofs in Appendix G.5. Example 6.3 demonstrates the need for extl requirement in (3).
Example 6.3 (When returning from internal states, 𝐴 does not imply 𝐴−▽𝑅𝑛𝑔(𝜙)). In Fig. 2 we
have 𝜎2 = 𝜎1 ▽ 𝜙 2 , and 𝜎2 |= ⟨𝑜 1 ⟩ , and 𝑜 1 ∈ 𝑅𝑛𝑔(𝜙 2 ), but 𝜎1 ̸ |= ⟨𝑜 1 ⟩ ←
                                                                                ×− 𝑜 1 .
6.2.3 Calls. is described in Fig. 7. Call_Int for internal methods, whether public or private; and
Call_Ext_Adapt and Call_Ext_Adapt_Strong for external methods.

                                                                                     [Call_Int]
                                 ⊢ 𝑀 : { 𝐴1 } 𝑝 𝐶 ::𝑚(𝑥 : 𝐶) { 𝐴2 } ∥ {𝐴3 }
                        𝐴1′ = 𝐴1 [𝑦0, 𝑦/this, 𝑥]      𝐴2′ = 𝐴2 [𝑦0, 𝑦, 𝑢/this, 𝑥, res]
                       𝑀 ⊢ { 𝑦0 : 𝐶, 𝑦 : 𝐶 ∧ 𝐴1 } 𝑢 := 𝑦0 .𝑚(𝑦1, ..𝑦𝑛 ) { 𝐴2′ } ∥ { 𝐴3 }
                                              ′


                                                                           [Call_Ext_Adapt]
                                                     A
                                       ⊢ 𝑀 : 𝑥 : 𝐶.{𝐴}
          𝑀 ⊢ { 𝑦0 : extl ∧ 𝑥 : 𝐶 ∧ 𝐴−▽(𝑦0, 𝑦) } 𝑢 := 𝑦0 .𝑚(𝑦1, ..𝑦𝑛 ) { 𝐴−▽(𝑦0, 𝑦) } ∥ { 𝐴 }

                                                                        [Call_Ext_Adapt_Strong]
                                                     A
                                       ⊢ 𝑀 : 𝑥 : 𝐶.{𝐴}
      𝑀 ⊢ { 𝑦0 : extl ∧ 𝑥 : 𝐶 ∧ 𝐴 ∧ 𝐴−▽(𝑦0, 𝑦) } 𝑢 := 𝑦0 .𝑚(𝑦1, ..𝑦𝑛 ) { 𝐴 ∧ 𝐴−▽(𝑦0, 𝑦) } ∥ { 𝐴 }

            Fig. 7. Hoare Quadruples for Internal and External Calls – here 𝑦 stands for 𝑦1, ...𝑦𝑛

    For internal calls, we start, as usual, by looking up the method’s specification, and substituting the
formal by the actual parameters parameters (this, 𝑥 by 𝑦0, 𝑦). Call_Int is as expected: we require
the precondition, and guarantee the postcondition and mid-condition. Call_Int is applicable
whether the method is public or private.
    For external calls, we consider the module’s invariants. If the module promises to preserve 𝐴,
               A
i.e. if ⊢ 𝑀 : 𝑥 : 𝐷.{𝐴}, and if its adapted version, 𝐴−▽(𝑦0, 𝑦), holds before the call, then it also
holds after the call (Call_Ext_Adapt). If, in addition, the un-adapted version also holds before
the call, then it also holds after the call (Call_Ext_Adapt_Strong).
    Notice that internal calls, Call_Int, require the un-adapted method precondition (i.e. 𝐴1′ ), while
external calls, both Call_Ext_Adapt and Call_Ext_Adapt_Strong, require the adapted invariant
(i.e. 𝐴−▽(𝑦0, 𝑦)). This is sound, because internal callees preserve 𝑆𝑡𝑏 + (_)-assertions – c.f. Lemma
4.6. On the other hand, external callees do not necessarily preserve 𝑆𝑡𝑏 + (_)-assertions – c.f. Ex.

                                                          , Vol. 1, No. 1, Article . Publication date: November 2025.
20                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


4.7. Therefore, in order to guarantee that 𝐴 holds upon entry to the callee, we need to know that
𝐴−▽(𝑦0, 𝑦) held at the caller site – c.f. Lemma 6.2.
   Remember that popping frames does not necessarily preserve 𝑆𝑡𝑏 + (_) assertions – c.f. Ex. 4.7.
Nevertheless, Call_Int guarantees the unadapted version, 𝐴, upon return from the call. This is
sound, because of our deep satisfaction of assertions – more in Sect. 7.
   Polymorphic Calls. Our rules do not directly address scenaria where the receiver may be internal
or external, andthe choice about this is made at runtime. However, such scenaria are indirectly
supported, through our rules of consequence and case-split. More in Appendix I.6.
Example 6.4 (Proving external calls). We continue our discussion from §2.3.2 on how to establish
the Hoare triple (1) :
        { buyer : extl ∧ ⟨ this.accnt.key⟩⟩←              ×− buyer ∧ this.accnt.blnce = 𝑏 }
   (1?)          buyer.pay(this.accnt,price)
        { this.accnt.blnce ≥ 𝑏 } || { ⟨ a.key⟩⟩ ∧ a.blnce ≥ b }
                                    A
We use 𝑆 3 , which says that a : Account, b : int.{⟨⟨a.key⟩⟩ ∧ a.blnce ≥ b}. We can apply
rule Call_Ext_Adapt, by taking 𝑦0 ≜ buyer, and 𝑥 : 𝐷 ≜ a : Account, b : int, and 𝐴 ≜
⟨ a.key⟩⟩ ∧ a.blnce ≥ b, and 𝑚 ≜ pay, and 𝑦 ≜ this.accnt, price, and provided that we
can establish that
  (2?) ⟨ this.accnt.key⟩ ←      ×− ( buyer, this.accnt, price)
holds. Using type information, we get that all fields transitively accessible from this.accnt.key,
or price are internal or scalar. This implies
  (3) ⟨ this.accnt.key⟩ ←    ×− this.accnt ∧ ⟨ this.accnt.key⟩ ←           ×− price
Using then Def. 6.1, we can indeed establish that
   (4) ⟨ this.accnt.key⟩ ←     ×− ( buyer, this.accnt, price) = ⟨ this.accnt.key⟩ ←        ×− buyer
Then, by application of the rule of consequence, (4), and the rule Call_Ext_Adapt, we can
establish (1). More details in §I.3.

6.3    Third Phase: Adherence to Module Specifications
In Fig. 8 we define the judgment ⊢ 𝑀, which says that 𝑀 has been proven to be well formed.

                              WellFrm_Mod                             Comb_Spec
      ⊢ 𝒮𝑝𝑒𝑐 (𝑀)              𝑀 ⊢ 𝒮𝑝𝑒𝑐 (𝑀)               𝑀 ⊢ 𝑆1       𝑀 ⊢ 𝑆2
                  ⊢𝑀                                         𝑀 ⊢ 𝑆1 ∧ 𝑆2
                                                                             method
                           mBody(𝑚, 𝐷, 𝑀) = 𝑝 (𝑦 : 𝐷){ 𝑠𝑡𝑚𝑡 }
             𝑀 ⊢ { this : D, 𝑦 : 𝐷 ∧ 𝐴1 } 𝑠𝑡𝑚𝑡 { 𝐴2 ∧ 𝐴2 −▽res } ∥ { 𝐴3 }
                         𝑀 ⊢ { 𝐴1 } 𝑝 𝐷 ::𝑚(𝑦 : 𝐷) { 𝐴2 } ∥ {𝐴3 }
                                                                              invariant
      ∀𝐷, 𝑚. mBody(𝑚, 𝐷, 𝑀) = public (𝑦 : 𝐷){ 𝑠𝑡𝑚𝑡 } =⇒
       𝑀 ⊢ { this : D, 𝑦 : 𝐷, 𝑥 : 𝐶 ∧ 𝐴 ∧ 𝐴−▽(this, 𝑦) } 𝑠𝑡𝑚𝑡 { 𝐴 ∧ 𝐴−▽res } ∥ { 𝐴 }
                                                          A
                                         𝑀 ⊢ 𝑥 : 𝐶.{𝐴}

                            Fig. 8. Methods’ and Modules’ Adherence to Specification

   WellFrm_Mod and Comb_Spec say that 𝑀 is well-formed if its specification is well-formed
(according to Def. 5.6), and if 𝑀 satisfies all conjuncts of the specification. Method says that a
module satisfies a method specification if the body satisfies the corresponding pre-, post- and
midcondition. In the postcondition we also ask that 𝐴−▽res, so that res does not leak any of the

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                   21


values that 𝐴 promises will be protected. Invariant says that a module satisfies a specification
A
 𝑥 : 𝐶.{𝐴}, if the method body of each public method has 𝐴 as its pre-, post- and midcondition.
Moreover, the precondition is strengthened by 𝐴−▽(this, 𝑦) – this is sound because the caller is
external, and by Lemma 6.2, part (4).
   Barendregt In method we implicitly require the free variables in a method’s precondition
not to overlap with variables in its body, unless they are the receiver or one of the parameters
(𝑉𝑠 (𝑠𝑡𝑚𝑡) ∩ 𝐹𝑣 (𝐴1 ) ⊆ {this, 𝑦1, ...𝑦𝑛 }). And in invariant we require the free variables in 𝐴 (which
are a subset of 𝑥) not to overlap with the variable in 𝑠𝑡𝑚𝑡 (𝑉𝑠 (𝑠𝑡𝑚𝑡) ∩ 𝑥 = ∅). This can easily be
achieved through renamings, c.f. Def. G.1.

Example 6.5 (Proving a public method). Consider the proof that Account::set from 𝑀 𝑓 𝑖𝑛𝑒
satisfies 𝑆 2 . Applying rule invariant, we need to establish:
           { ... a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                    ×− ( key’, key” ) }
    (5?)           body_of_set_in_Account_in_𝑀 𝑓 𝑖𝑛𝑒
           { ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res } || { ⟨ a.key⟩⟩ }
 Given the conditional statement in set, and with the obvious treatment of conditionals (c.f. Fig.
19), among other things, we need to prove for the true-branch that:
           { ... ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                      ×− ( key’, key” ) ∧ this.key = key’ }
(6?)                this.key := key”
           { ⟨ a.key⟩⟩ } || { ⟨ a.key⟩⟩ }
 We can apply case-split (c.f. Fig. 19) on whether this=a, and thus a proof of (7?) and (8?),
would give us a proof of (6?):
           { ... ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                      ×− ( key’, key” ) ∧ this.key =key’ ∧ this =a }
(7?)                this.key := key”
           { ⟨ a.key⟩⟩ } || { ⟨ a.key⟩⟩ }
and also
           { ...⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                     ×− ( key’, key” ) ∧ this.key =key’ ∧ this ≠ a }
(8?)               this.key := key”
           { ⟨ a.key⟩⟩ } || { ⟨ a.key⟩⟩ }
If this.key=key’ ∧ this=a, then a.key=key’. But ⟨ a.key⟩⟩←             ×− key’ and Prot-Neq from
Fig. 20 give a.key ≠ key’. So, by contradiction (c.f. Fig. 19), we can prove (7?). If this ≠ a, then
we obtain from the underlying Hoare logic that the value of a.key did not change. Thus, by rule
Prot_1, we obtain (8?). More details in §I.5.
On the other hand, set from 𝑀𝑏𝑎𝑑 cannot be proven to satisfy 𝑆 2 , because it requires proving
           { ... ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                      ×− ( key’, key” ) }
(???)               this.key := key”
           { {⟨⟨a.key⟩⟩ } || { ⟨ a.key⟩⟩ }
and without the condition this.key=key’ there is no way we can prove (???).

6.4        Our Example Proven
Using our Hoare logic, we have developed a mechanised proof in Coq, that, indeed, 𝑀𝑔𝑜𝑜𝑑 ⊢ 𝑆 2 ∧ 𝑆 3 .
This proof is part of the accompanying artifact.
   Our proof models ℒ𝑢𝑙 , the assertion language, the specification language, and the Hoare logic
from §6.1, §6.2, §6.3, §G and Def. 6.1. In keeping with the start of §6, our proof assumes the
existence of an underlying Hoare logic, and several, standard, properties of that underlying logic,
the assertions logic (e.g. equality of objects implies equality of field accesses) and of type systems
(e.g. fields of objects of different types cannot be aliases of one another). All assumptions are clearly
indicated in the associated artifact. Appendix I outlines that proof.

                                                            , Vol. 1, No. 1, Article . Publication date: November 2025.
22                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


7    Soundness
We now give a synopsis of the proof of soundness of the logic from §6, and outline the two most
interesting aspects: deep satisfaction, and summarized execution.
Deep Satisfaction We are faced with the challenge that assertions are not always preserved when
the top frame is popped (c.f. Ex. 4.7), yet we must be able to argue that method return pre-
serves the method body’s postconditions. For this, we introduce a “deeper” notion of assertion
satisfaction, which an assertion be satisfied not only from the view of the top frame, but also
from the view of every frame starting from the 𝑘-th frame onwards: 𝑀, 𝜎, 𝑘 |= 𝐴 says that
∀𝑗 .[ 𝑘 ≤ 𝑗 ≤ |𝜎 | ⇒ 𝑀, 𝜎 [ 𝑗] |= 𝐴 ]. Accordingly, we introduce deep specification satisfaction,
𝑀; 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝐴′′ }, which promises for all 𝑘 ≤ |𝜎 |, if 𝑀, 𝜎, 𝑘 |= 𝐴, and if scoped
execution of 𝜎’s continuation leads to final state 𝜎 ′ and intermediate external state 𝜎 ′′ , then
𝑀, 𝜎 ′, 𝑘 |= 𝐴′ , and 𝑀, 𝜎 ′′, 𝑘 |= 𝐴′′ - c.f. App.H.3.
   Here how deep satisfaction addresses this problem: Assume state 𝜎1 right before entering a call,
𝜎2 and 𝜎3 at start and end of the call’s body, and 𝜎4 upon return. If a pre-condition holds at 𝜎1 , then
it holds for a 𝑘 ≤ |𝜎1 |; hence, if the postcondition holds for 𝑘 at 𝜎3 , and because |𝜎3 | = |𝜎1 |+1, it also
holds for 𝜎4 . Deep satisfaction is stronger than shallow (i.e. specification satisfaction as in Def. 5.2).

Lemma 7.1. For all 𝑀, 𝑀, 𝐴, 𝐴′ , 𝐴′′ , 𝜎:
     • 𝑀; 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝐴′′ } =⇒ 𝑀; 𝑀 |= { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝐴′′ }

Soundness of the Triples Logic We require the assertion logic, 𝑀 ⊢ 𝐴, and the underlying Hoare
logic, 𝑀 ⊢𝑢𝑙 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ }, to be be sound. Such sound logics do exist. Namely, one can build
an assertion logic, 𝑀 ⊢ 𝐴, by extending a logic which does not talk about protection, through the
addition of structural rules which talk about protection; this extension preserves soundness - c.f.
App. H.1. Moreover, since the assertions 𝐴 and 𝐴′ in 𝑀 ⊢𝑢𝑙 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } may, but need not, talk
about protection, one can take a Hoare logic from the literature as the ⊢𝑢𝑙 -logic.
  We then prove soundness of the rules about protection from Fig. 6, and, based on this, we prove
soundness of the inference system for triples – c.f. Appendix H.5.
Theorem 7.2. For module 𝑀 such that ⊢ 𝑀, and for any assertions 𝐴, 𝐴′ , 𝐴′′ and statement 𝑠𝑡𝑚𝑡:
                     𝑀 ⊢ { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ }          =⇒         𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }

Summarised Execution Execution of an external call may consist of any number of external transi-
tions, interleaved with calls to public internal methods, which in turn may make any number of
further internal calls (public or private), and these, again may call external methods. For the proof
of soundness, internal and external transitions use different arguments. For external transitions
we consider small steps and argue in terms of preservation of encapsulated properties, while for
internal calls, we use large steps, and appeal to the method’s specification. Therefore, we define
sumarized executions, where internal calls are collapsed into one, large step, e.g. below:

                                                              summarized
                                                                 to


   Lemma H.28 says that any terminating execution starting in an external state consists of a
sequence of external states interleaved with terminating executions of public methods. Lemma
H.29 says that such an execution preserves an encapsulated assertion 𝐴 provided that all these
finalising internal executions also preserve 𝐴.

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                               23


 Soundness of the Quadruples Logic Proving soundness of our quadruples requires induction on the
execution in some cases, and induction on the derivation of the quadruples in others. We address
this through a well-founded ordering that combines both, c.f. Def. H.22 and Lemma H.23. Finally,
in §H.16, we prove soundness:
     Theorem 7.3. For module 𝑀, assertions 𝐴, 𝐴′ , 𝐴′′ , state 𝜎, and specification 𝑆:
    (A) : ⊢ 𝑀 ∧ 𝑀 ⊢ { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }           =⇒        𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }
    (B) : 𝑀 ⊢ 𝑆      =⇒       𝑀 |=𝑑𝑒𝑒𝑝 𝑆

8    Conclusion: Summary, Related Work and Further Work
Our motivation comes from the OCAP approach to security, whereby object capabilities guard
against unsanctioned effects. Miller [84, 86] advocates defensive consistency: whereby “An object
is defensively consistent when it can defend its own invariants and provide correct service to its
well behaved clients, despite arbitrary or malicious misbehaviour by its other clients.” Defensively
consistent modules are hard to design and verify, but make it much easier to make guarantees
about systems composed of multiple components [92].
Our work aims to elucidate such guarantees. We want to formalize and prove that [45]:
       Lack of eventual access implies that certain properties will be preserved, even in the
       presence of external calls.
For this, we had to model the concept of lack of eventual access, determine the temporal scope of
the preservation, and develop a Hoare logic framework to formally prove such guarantees.
   For lack of eventual access, we introduced protection, a property of all the paths of all external
objects accessible from the current stack frame. For the temporal scope of preservation, we developed
scoped invariants, which ensure that a given property holds as long as we have not returned from the
current method. (top of current stack has not been popped yet). For our Hoare logic, we introduced
an adaptation operator, which translates assertions between the caller’s and callee’s frames. Finally,
to prove the soundness of our approach, we developed the notion of deep satisfaction, which
mandates that an assertion must be satisfied from a particular stack frame onward. Thus, most
concepts in this work are scope-aware, as they depend on the current stack frame.
   With these concepts, we developed a specification language for modules limiting effects, a Hoare
Logic for proving external calls, protection, and adherence to specifications, and have proven it
sound.
Lack of Eventual Access Efforts to restrict “eventual access” have been extensively explored, with
Ownership Types being a prominent example [21, 27]. These types enforce encapsulation boundaries
to safeguard internal implementations, thereby ensuring representation independence and defensive
consistency [7, 26, 94]. Ownership is fundamental to key systems like Rust’s memory safety [61, 63],
Scala’s Concurrency [51, 52], Java’s heap analyses [55, 88, 99], and it plays a critical role in program
verification [14, 66] including Spec# [9, 10], universes [36, 37, 73], Borrowable Fractional Ownership
[93], and recently has been integrated into languages like OCAML [72, 77].
   Ownership types are closely related to the notion of protection: both are scoped relative to a
frame. However, ownership requires an object to control some part of the path, while protection
demands that module objects control the endpoints of paths.
   In future work we want to explore how to express protection within Ownership Types, with
the primary challenge being how to accommodate capabilities accessible to some external objects
while still inaccessible to others. Moreover, tightening some rules in our current Hoare logic
(e.g. Def. 4.4) may lead to a native Hoare logic of ownership. Also, recent approaches like the
Alias Calculus [64, 104], Reachability Types [8, 116] and Capturing Types [13, 18, 120] abstract

                                                        , Vol. 1, No. 1, Article . Publication date: November 2025.
24                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


fine-grained method-level descriptions of references and aliases flowing into and out of methods
and fields, and likely accumulate enough information to express protection. Effect exclusion [74]
directly prohibits nominated effects, but within a closed, fully-typed world.
Temporal scope of the guarantee Starting with loop invariants[48, 56], property preservation at
various granularities and durations has been widely and successfully adapted and adopted [9, 28,
41, 57, 67, 68, 70, 82, 83, 91]. In our work, the temporal scope of the preservation guarantee includes
all nested calls, until termination of the currently executing method, but not beyond. We compare
with object and history invariants in §3.3.2.
    Such guarantees are maintained by the module as a whole. Drossopoulou et al. [44] proposed
“holistic specifications” which take an external perspective across the interface of a module. Mackay
et al. [76] builds upon this work, offering a specification language based on necessary conditions
and temporal operators. Neither of these systems support any kind of external calls. Like [44, 76]
we propose “holistic specifications”, albeit without temporal logics, and with sufficient conditions.
In addition, we introduce protection, and develop a Hoare logic for protection and external calls.
Hoare Logics were first developed in Hoare’s seminal 1969 paper [56], and have inspired a plethora
of influential further developments and tools. We shall discuss a few only.
    Separation logics [59, 102] reason about disjoint memory regions. Incorporating Separation
Logic’s powerful framing mechanisms will pose several challenges: We have no specifications and
no footprint for external calls. Because protection is “scope-aware”, expressing it as a predicate
would require quantification over all possible paths and variables within the current stack frame.
We may also require a new separating conjunction operator. Hyper-Hoare Logics [31, 40] reason
about the execution of several programs, and could thus be applied to our problem, if extended to
model all possible sequences of calls of internal public methods.
    Incorrectness Logic [95] under-approximates postconditions, and thus reasons about the presence
of bugs, rather than their absence. Our work, like classical Hoare Logic, over-approximates postcon-
ditions, and differs from Hoare and Incorrectness Logics by tolerating interactions between verified
code and unverified components. Interestingly, even though in earlier works[44, 76] we employed
necessary conditions for effects (i.e. under-approximate pre-conditions), we can, instead, employ
sufficient conditions for the lack of effects (over-approximate postconditions). Incorporating our
work into Incorrectness Logic might require under-approximating eventual access, while protection
over-approximates it.
    Rely-Guarantee [53, 115] and Deny-Guarantee [39] distinguish between assertions guaranteed
by a thread, and those a thread can reply upon. Our Hoare quadruples are (roughly) Hoare triples
plus the “guarantee” portion of rely-guarantee. When a specification includes a guarantee, that
guarantee must be maintained by every “atomic step” in an execution [53], rather than just at
method boundaries as in visible states semantics [41, 91, 110]. In concurrent reasoning, this is
because shared state may be accessed by another coöperating thread at any time: while in our case,
it is because unprotected state may be accessed by an untrusted component within the same thread.
Models and Hoare Logics for the interaction with the the external world Murray [92] made the first
attempt to formalise defensive consistency, to tolerate interacting with any untrustworthy object,
although without a specification language for describing effects (i.e. when an object is correct).
    Cassez et al. [22] propose one approach to reason about external calls. Given that external
callbacks are necessarily restricted to the module’s public interface, external callsites are replaced
with a generated externalcall() method that nondeterministically invokes any method in
that interface. Rao et al. [101]’s Iris-Wasm is similar. WASM’s modules are very loosely coupled: a
module has its own byte memory and object table. Iris-Wasm ensures models can only be modified
via their explicitly exported interfaces.

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                              25


   Swasey et al. [112] designed OCPL, a logic that separates internal implementations (“high
values”) from interface objects (“low values”). OCPL supports defensive consistency (called “robust
safety” after the security literature [11]) by ensuring low values can never leak high values, a
and prove object-capability patterns, such as sealer/unsealer, caretaker, and membrane. RustBelt
[61] developed this approach to prove Rust memory safety using Iris [62], and combined with
RustHorn [79] for the safe subset, produced RustHornBelt [78] that verifies both safe and unsafe
Rust programs. Similar techniques were extended to C [105].
   Devriese et al. [34] deploy step-indexing, Kripke worlds, and public/private state machines to
model problems including the DOM wrapper and a mashup application. Their distinction between
public and private transitions is similar to our distinction between internal and external objects.
VMSL is an Iris-based separation logic for virtual machines to assure defensive consistency [71].
Cerise uses Iris invariants to support proofs of programs with outgoing calls and callbacks, on
capability-safe CPUs [49]. [109] supports several different wrappers on the same object. Besides
the distinction between the object-based and class-based approach, our work differs from [34, 49,
71, 78, 101, 109, 112] in that they follow a “static” capability model whereby authority is conferred
though an object’s interface, whereas we follow a “dynamic” model whereby authority may be
stored in the callee’s context.
   Anderson et al. [3] extend memory safety arguments to “stack safety”, ensuring that method
calls and returns are well bracketed, and preserving the integrity of caller and callee. Schaefer et al.
[106] adopt an information-flow approach to ensure confidentially by construction.
Smart Contracts also pose the problem of external calls. Rich-Ethereum [19] assumes instance-
private and unaliased contract fields , and employs a “finished” flag to manage callbacks. Scilla
[107], a minimalist functional alternative to Ethereum, helps prevent common contract errors.
   The VerX tool can verify specifications for Solidity contracts automatically [98]. VerX’s specifi-
cation language is based on temporal logic. It is restricted to “effectively call-back free” programs
[2, 50], delaying any callbacks until the incoming call to the internal object has finished.
   ConSol [117] provides a specification langauge for smart contracts, checked at runtime [47].
SCIO* [4], implemented in F*, supports both verified and unverified code. Both Consol and SCIO*
are similar to gradual verification techniques [29, 121] that insert dynamic checks between verified
and unverified code, and contracts for general access control [30, 38, 89].
Future work includes the application of our techniques to languages that rely on lexical nesting for
access control, e.g. Javascript [85], to languages that support ownership types, e.g. Rust, leveraged
for verification [6, 65, 78], and to features such as uniqueness[72, 77]. These different language
paradigms may lead to a refined view of the meaning of protection. We also want to investigate
tighter integrations with the underlying Hoare logic and its framing operators.


Acknowledgements
We are grateful for the feedback from Lars Birkedal, David Swasey, Peter Müller, Derek Dreyer,
Dominique Devriese, and the anonymous OOPSLA reviewers. We are especially thankful to Re-
viewer B, and even more so to Reviewer C, whose sustained engagement across multiple rounds of
discussion went well beyond expectations and was instrumental in helping us clarify parts of the
work that were initially unclear.


A   Appendix to Section 3 – The programming language ℒ𝑢𝑙
We introduce ℒ𝑢𝑙 , a simple, typed, class-based, object-oriented language.


                                                       , Vol. 1, No. 1, Article . Publication date: November 2025.
26                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


A.1     Syntax
The syntax of ℒ𝑢𝑙 is given in Fig. 413 . To reduce the complexity of our formal models, as is usually
done, CITE - CITE, ℒ𝑢𝑙 lacks many common languages features, omitting static fields and methods,
interfaces, inheritance, subsumption, exceptions, and control flow. ℒ𝑢𝑙 and which may be defined
recursively.
   ℒ𝑢𝑙 modules (𝑀) map class names (𝐶) to class definitions (ClassDef). A class definition consists
of a list of field definitions, ghost field definitions, and method definitions. Fields, ghost fields, and
methods all have types, 𝐶; types are classes. Ghost fields may be optionally annotated as intrnl,
requiring the argument to have an internal type, and the body of the ghost field to only contain
references to internal objects. This is enforced by the limited type system of ℒ𝑢𝑙 . A program state
(𝜎) is a pair of of a stack and a heap. The stack is a a stack is a non-empty list of frames (𝜙), and the
heal (𝜒) is a map from addresses (𝛼) to objects (𝑜). A frame consists of a local variable map and a
continuation .cont that represents the statements that are yet to be executed (𝑠). A statement is
either a field read (𝑥 := 𝑦.𝑓 ), a field write (𝑥 .𝑓 := 𝑦), a method call (𝑢 := 𝑦0 .𝑚(𝑦)), a constructor call
(new 𝐶), a sequence of statements (𝑠; 𝑠), or empty (𝜖).
   ℒ𝑢𝑙 also includes syntax for expressions e that may be used in writing specifications or the
definition of ghost fields.

A.2     Semantics
ℒ𝑢𝑙 is a simple object oriented language, and the operational semantics (given in Fig. 5 and discussed
later) do not introduce any novel or surprising features. The operational semantics make use of
several helper definitions that we define here.
   We provide a definition of reference interpretation in Definition A.1
Definition A.1. For a frame 𝜙 = (𝑥 ↦→ 𝑣, 𝑠), and a program state 𝜎 = (𝜙 · 𝜙, , 𝜒), we define:
   • ⌊𝑥⌋ 𝜙 ≜ 𝑣𝑖 if 𝑥 = 𝑥𝑖
   • ⌊𝑥⌋ 𝜎 ≜ ⌊𝑥⌋ 𝜙
   • ⌊𝛼 .𝑓 ⌋ 𝜎 ≜ 𝑣𝑖 if 𝜒 (𝛼) = (_; 𝑓 ↦→ 𝑣), and 𝑓𝑖 = 𝑓
   • ⌊𝑥 .𝑓 ⌋ 𝜎 ≜ ⌊𝛼 .𝑓 ⌋ 𝜎 where ⌊𝑥⌋ 𝜎 = 𝛼
   • 𝜙 .cont ≜ 𝑠
   • 𝜎.cont ≜ 𝜙 .cont
   • 𝜙 [cont ↦→ 𝑠 ′ ] ≜ (𝑥 ↦→ 𝑣, 𝑠 ′ )
   • 𝜎 [cont ↦→ 𝑠 ′ ] ≜ ( 𝜙 · 𝜙 [cont ↦→ 𝑠 ′ ], 𝜒 )
   • 𝜙 [x’ ↦→ 𝑣 ′ ] ≜ ( (𝑥 ↦→ 𝑣) [x’ ↦→ 𝑣 ′ ], 𝑠 )
   • 𝜎 [x’ ↦→ 𝑣 ′ ] ≜ ( (𝜙 · (𝜙 [x’ ↦→ 𝑣 ′ ]), 𝜒)
   • 𝜎 [𝛼 ↦→ 𝑜] ≜ ( (𝜙 · 𝜙), 𝜒 [𝛼 ↦→ 𝑜] )
   • 𝜎 [𝛼 .𝑓 ′ ↦→ 𝑣 ′ ] ≜ 𝜎 [𝛼 ↦→ 𝑜] if 𝜒 (𝛼) = (𝐶, 𝑓 ↦→ 𝑣), and 𝑜 = ( 𝐶; (𝑓 ↦→ 𝑣) [𝑓 ′ ↦→ 𝑣 ′ ] )
   That is, a variable 𝑥, or a field access on a variable 𝑥 .𝑓 has an interpretation within a program
state of value 𝑣 if 𝑥 maps to 𝑣 in the local variable map, or the field 𝑓 of the object identified by 𝑥
points to 𝑣.
   Definition A.2 defines the class lookup function an object identified by variable 𝑥.
Definition A.2 (Class Lookup). For program state 𝜎 = (𝜙 · 𝜙, 𝜒), class lookup is defined as
                                    classOf(𝜎, 𝑥) ≜ 𝐶          if 𝜒 ( ⌊𝑥⌋ 𝜎 ) = (𝐶, _)
     Module linking is defined for modules with disjoint definitions:
13 Our motivating example is provided in a slightly richer syntax for greater readability.



, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                             27


Definition A.3. For all modules 𝑀 and 𝑀, if the domains of 𝑀 and 𝑀 are disjoint, we define the
module linking function as 𝑀 · 𝑀 ≜ 𝑀 ∪ 𝑀 ′ .
  That is, their linking is the union of the two if their domains are disjoint.
  Definition A.4 defines the method lookup function for a method call 𝑚 on an object of class 𝐶.
Definition A.4 (Method Lookup). For module 𝑀, class 𝐶, and method name 𝑚, method lookup is
defined as
                         Meth(𝑀, 𝐶, 𝑚) ≜ 𝑝𝑟 method 𝑚 (𝑥 : 𝑇 ): 𝑇 { 𝑠 }
if there exists an 𝑀 in 𝑀, so that 𝑀 (𝐶) contains the definition 𝑝𝑟 method 𝑚 (𝑥 : 𝑇 ): 𝑇 { 𝑠 }
  Definition A.5 looks up all the field identifiers in a given class
Definition A.5 (Fields Lookup). For modules 𝑀,and class 𝐶, fields lookup is defined as
           𝑓 𝑖𝑒𝑙𝑑𝑠 (𝑀, 𝐶) ≜ { 𝑓 | ∃𝑀 ∈ 𝑀.𝑠.𝑡 .𝑀 (𝐶)contains the definitionfield 𝑓 : 𝑇 }
  We define what it means for two objects to come from the same module
Definition A.6 (Same Module). For program state 𝜎, modules 𝑀, and variables 𝑥 and 𝑦, we defone
𝑆𝑎𝑚𝑒𝑀𝑜𝑑𝑢𝑙𝑒 (𝑥, 𝑦, 𝜎, 𝑀) ≜ ∃𝐶, 𝐶 ′, 𝑀 [ 𝑀 ∈ 𝑀 ∧𝐶, 𝐶 ′ ∈ 𝑀 ∧classOf(𝜎, 𝑥) = 𝐶 ∧classOf(𝜎, 𝑦) = 𝐶 ′ ]
   As we already said in §3.3.3, we forbid assignments to a method’s parameters. To do that, the
following function returns the identifiers of the formal parameters of the currently active method.
Definition A.7. For program state 𝜎:
  𝑃𝑟𝑚𝑠 (𝜎, 𝑀) ≜ 𝑥 such that ∃𝜙, 𝜙𝑘 , 𝜙𝑘+1, 𝐶, 𝑝.
                     [ 𝜎 = (𝜙 · 𝜙𝑘 · 𝜙𝑘+1 , 𝜒) ∧ 𝜙𝑘 .cont = _ := 𝑦0 .𝑚(_); _ ∧
                     classOf((𝜙𝑘+1, 𝜒), this) ∧ Meth(𝑀, 𝐶, 𝑚) = 𝑝 𝐶 :: 𝑚(𝑥 : _): _{_} ]
   While the small-step operational semantics of ℒ𝑢𝑙 is given in Fig. 5, specification satisfaction is
defined over an abstracted notion of the operational semantics that models the open world.
   An Initial program state contains a single frame with a single local variable this pointing to a
single object in the heap of class Object, and a continuation.
Definition A.8 (Initial Program State). A program state 𝜎 is said to be an initial state (Initial(𝜎))
if and only if
    • 𝜎 = (((this ↦→ 𝛼), 𝑠); (𝛼 ↦→ (Object, ∅)
for some address 𝛼 and some statement 𝑠.
   We provide a semantics for expression evaluation is given in Fig. 9. That is, given a module 𝑀 and
a program state 𝜎, expression 𝑒 evaluates to 𝑣 if 𝑀, 𝜎, 𝑒 ↩→ 𝑣. Note, the evaluation of expressions is
separate from the operational semantics of ℒ𝑢𝑙 , and thus there is no restriction on field access.
Proof of lemma 3.6 The first assertion is proven by unfolding the definition of _ |= _.
  The second assertion is proven by case analysis on the execution relation _, 𝜎 d 𝜎 ′ . The
assertion gets established when we call a method, and is preserved through all the execution steps,
because we do not allow assignments to the formal parameters.
End Proof
  We now prove lemma B.2:
Proof of lemma B.2
    • We first show that (𝑀, 𝜎𝑠𝑐 ); 𝜎 ⇝ 𝜎 ′ ∧ 𝑘 < |𝜎 |𝑠𝑐 =⇒ ⌊𝑦⌋ 𝜎 [𝑘 ] = ⌊𝑦⌋ 𝜎 ′ [𝑘 ] This follows
      easily from the operational semantics, and the definitions.

                                                      , Vol. 1, No. 1, Article . Publication date: November 2025.
28                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


    • By induction on the earlier part, we obtain that 𝑀; 𝜎⇝∗𝜎 ′ ∧ 𝑘 < |𝜎 | =⇒ ⌊𝑦⌋ 𝜎 [𝑘 ] = ⌊𝑦⌋ 𝜎 ′ [𝑘 ]
    • We now show that 𝑀; 𝜎⇝∗fin 𝜎 ′ ∧ 𝑦 ∉ 𝑉𝑠 (𝜎.cont) =⇒ ⌊𝑦⌋ 𝜎 = ⌊𝑦⌋ 𝜎 ′ by induction on the
      number of steps, and using the earlier lemma.
End Proof
  Lemma A.9 states that initila states are well-formed, and that (2) a pre-existing object, locally
reachable after any number of scoped execution steps, was locally reachable at the first step.


Lemma A.9. For all modules 𝑀, states 𝜎, 𝜎 ′ , and frame 𝜙:
  (1) Initial(𝜎) =⇒ 𝑀 |= 𝜎
  (2) 𝑀; 𝜎⇝∗𝜎 ′ =⇒ 𝑑𝑜𝑚(𝜎) ∩ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 ′ ) ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎)
   Consider Fig. 3 . Lemma A.9, part 2 promises that any objects locally reachable in 𝜎14 which
already existed in 𝜎8 , were locally reachable in 𝜎8 . However, the lemma is only applicable to scoped
execution, and as 𝑀; 𝜎8 ⇝  ̸ ∗𝜎17 , the lemma does not promise that objects locally reachable in 𝜎17
which already existed in 𝜎8 , were locally accessible in 𝜎8 – namely it could be that objects are made
globally reachable upon method return, during the step from 𝜎14 to 𝜎15 .



     Finally, we define the evaluation of expressions, which, as we already said, represent ghost code.

                                                                                      𝑀, 𝜎, e ↩→ 𝛼
         𝑀, 𝜎, 𝑣 ↩→ 𝑣   (E-Val)           𝑀, 𝜎, 𝑥 ↩→ ⌊𝑥 ⌋ 𝜎    (E-Var)                                     (E-Field)
                                                                                  𝑀, 𝜎, e.𝑓 ↩→ ⌊𝛼 .𝑓 ⌋ 𝜎

𝑀, 𝜎, e0 ↩→ 𝛼      𝑀, 𝜎, e ↩→ 𝑣      𝑀 (classOf(𝜎, 𝛼 ) ) contains ghost 𝑔𝑓 (𝑥 : 𝑇 ) {e} : 𝑇 ′    𝑀, 𝜎, [𝑣/𝑥 ]e ↩→ 𝑣
                                                                                                                       (E-Ghost)
                                                𝑀, 𝜎, e0 .𝑔𝑓 (e) ↩→ 𝑣


                                           Fig. 9. ℒ𝑢𝑙 Expression evaluation




A.3      𝑀𝑔ℎ𝑜𝑠𝑡 Accounts expressed through ghost fields
We revisit the bank account example, to demonstrate the use of ghost fields. In Fig. 10, accounts
belong to banks, and their blnce is kept in a ledger. Thus, account.blnce is a ghost field
which involves a recursive search through that ledger.




, Vol. 1, No. 1, Article . Publication date: November 2025.
     Reasoning about External Calls – Extended Version                                                                  29


 1   module 𝑀𝑔ℎ𝑜𝑠𝑡
 2
 3     class Shop       ...
 4
 5     class Account
 6       field bank: Bank
 7       field key:Key
 8       public method transfer(dest:Account, key':Key, amt:nat)
 9         if (this.key==key')
10            this.bank.decBalance(this,amt);
11            this.bank.incBalance(dest.amt);
12       public method set(key':Key)
13         if (this.key==null) this.key=key'
14       ghost balance(): int
15           res:=bank.balance(this)
16
17     class Bank
18       field ledger: Ledger
19       method incBalance(a:Account, amt: nat)
20           this.ledger.decBalance(a,amt)
21       private method decBalance(a:Account, amt: nat)
22           this.ledger.decBalance(a,amt)
23       ghost balance(acc):int
24           res:=this.ledger.balance(acc)
25
26       class Ledger
27          acc:Acc
28          bal:int
29          next:Ledger
30          ghost balance(a:Acc):int
31            if this.acc==a
32              res:=retrun bal
33            else
34              res:=this.next.balance(a)


                                       Fig. 10. 𝑀𝑔ℎ𝑜𝑠𝑡 – a module with ghost fields




                                                                , Vol. 1, No. 1, Article . Publication date: November 2025.
30                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


B    Appendix to Section 3.3 – Fundamental Concepts
Lemma B.1 says, essentially, that scoped executions describe the same set of executions as those
starting at an initial state14 . For instance, revisit Fig. 3 , and assume that 𝜎6 is an initial state. We
have 𝑀; 𝜎10 d ∗ 𝜎14 and 𝑀; 𝜎10 ⇝   ̸ ∗𝜎14 , but also 𝑀; 𝜎6 ⇝∗𝜎14 .
Lemma B.1. For all modules 𝑀, state 𝜎𝑖𝑛𝑖𝑡 , 𝜎, 𝜎 ′ , where 𝜎𝑖𝑛𝑖𝑡 is initial:
   • 𝑀; 𝜎⇝∗𝜎 ′ =⇒ 𝑀; 𝜎 d∗ 𝜎 ′
   • 𝑀; 𝜎𝑖𝑛𝑖𝑡 d ∗ 𝜎 ′ =⇒ 𝑀; 𝜎𝑖𝑛𝑖𝑡 ⇝∗𝜎 ′ .
  Lemma B.2 says that scoped execution does not affect the contents of variables in earlier frames.
and that the interpretation of a variable remains unaffected by scoped execution of statements
which do not mention that variable. More in Appendix B.
Lemma B.2. For any modules 𝑀, states 𝜎, 𝜎 ′ , variable 𝑦, and number 𝑘:
   • 𝑀; 𝜎⇝∗𝜎 ′ ∧ 𝑘 < |𝜎 | =⇒ ⌊𝑦⌋ 𝜎 [𝑘 ] = ⌊𝑦⌋ 𝜎 ′ [𝑘 ]
   • 𝑀; 𝜎⇝∗fin 𝜎 ′ ∧ 𝑦 ∉ 𝑉𝑠 (𝜎.cont) =⇒ ⌊𝑦⌋ 𝜎 = ⌊𝑦⌋ 𝜎 ′




             a heap                       Locally Reachable from 𝜙 1                   Locally Reachable from 𝜙 2

                                          Fig. 11. -Locally Reachable Objects

     Fig. 11 illustrates local reachability: In the middle pane the top frame is 𝜙 1 which maps this to
𝑜 1 ; all objects are locally reachable. In the right pane the top frame is 𝜙 2 , which maps this to 𝑜 3 ,
and 𝑥 to 𝑜 7 ; now 𝑜 1 and 𝑜 2 are no longer locally reachable.
Proof of lemma B.1
      • By unfolding and folding the definitions.
      • By unfolding and folding the definitions, and also, by the fact that |𝜎𝑖𝑛𝑖𝑡 |=1, i.e. minimal.
End Proof



Proof of lemma B.2
   • We unfolding the definition of 𝑀; 𝜎 ⇝ 𝜎 ′ 𝑀; 𝜎 ⇝ 𝜎 ′ and the rules of the operational
     semantics.
   • Take 𝑘 = |𝜎 |. We unfold the definition from 3.2, and obtain that 𝜎 = 𝜎 ′ or, ∃𝜎1, ...𝜎𝑛1 .∀𝑖 ∈
     [1..𝑛) [ 𝑀; 𝜎𝑖 d 𝜎𝑖+1 ∧ |𝜎1 | ≤ |𝜎𝑖+1 | ∧ 𝜎 = 𝜎1 ∧ 𝜎 ′ = 𝜎𝑛 ]
     Consider the second case. Take any 𝑖 ∈ [1..𝑛). Then, by Definition, 𝑘 ≤ |𝜎 |. If 𝑘 = |𝜎𝑖 |, then
     we are executing part of 𝜎.𝑝𝑟𝑔𝑐𝑜𝑛𝑡, and because 𝑦 ∉ 𝑉𝑠 (𝜎.cont), we get ⌊𝑦⌋ 𝜎 [𝑖 ] = ⌊𝑦⌋ 𝜎𝑖+1 [𝑘 ] .
     If 𝑘 = |𝜎𝑖 |, then we apply the bullet from above, and also obtain ⌊𝑦⌋ 𝜎 [𝑖 ] = ⌊𝑦⌋ 𝜎𝑖+1 [𝑘 ]
     This gives that ⌊𝑦⌋ 𝜎 [𝑘 ] = ⌊𝑦⌋ 𝜎 ′ [𝑘 ] . Moreover, because 𝑀; 𝜎⇝∗fin 𝜎 ′ we obtain that |𝜎 | = |𝜎 ′ | =
     𝑘. Therefore, we have that ⌊𝑦⌋ 𝜎 = ⌊𝑦⌋ 𝜎 ′ .
14 An Initial state’s heap contains a single object of class Object, and its stack consists of a single frame, whose local

variable map is a mapping from this to the single object, and whose continuation is any statement. (See Def. A.8)

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                 31


End Proof



   We also prove that in well-formed states (|= 𝜎), all objects locally reachable from a given frame
also locally reachable from the frame below.
Lemma B.3. |= 𝜎 ∧ 𝑘 < |𝜎 |            =⇒      𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 [𝑘 + 1]) ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 [𝑘])
   Proof. By unfolding the definitions: Everything that is in 𝜎 [𝑘 + 1] is reachable from its frame,
and everything that is reachable from the frame of 𝜎 [𝑘 + 1] is also reachable from the frame of
𝜎 [𝑘]. We then apply that |= 𝜎
                                                                                                  □



Proof of lemma 3.6
  (1) By unfolding and folding the definitions. Namely, everything that is locally reachable in 𝜎 ′ is
      locally reachable through the frame 𝜙, and everything in the frame 𝜙 is locally reachable in
      𝜎.
  (2) We require that |= 𝜎 – as we said earlier, we require this implicitly. Here we apply induction
      on the execution. Each step is either a method call (in which case we apply the bullet from
      above), or a return statement (then we apply lemma B.3), or the creation of a new object (in
      which case reachable set is the same as that from previous state plus the new object), or an
      assignment to a variable (in which case the locally reachable objects in the new state are a
      subset of the locally reachable from the old state), or a an assignment to a field. In the latter
      case, the locally reachable objects are also a subset of the locally reachable objects from the
      previous state.
End Proof




                                                          , Vol. 1, No. 1, Article . Publication date: November 2025.
32                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


C    Appendix to Section 4 – Assertions
Figure 12 illustrates “protected from” and “protected”. In the first row we highlight in yellow the
objects protected from other objects. Thus, all objects except 𝑜 6 are protected from 𝑜 5 (left pane);
all objects expect 𝑜 8 are protected from 𝑜 7 (middle pane); and all objects except 𝑜 3 , 𝑜 6 , 𝑜 7 , and 𝑜 8 are
protected from 𝑜 2 (right pane). Note that 𝑜 6 is not protected from 𝑜 2 , because 𝑜 5 is reachable from
𝑜 2 , is external, and has direct access to 𝑜 6 .
     In the third row of Figure 12 we show three states: 𝜎1 has top frame 𝜙 1 , which has one variable,
this, pointing to 𝑜 1 , while 𝜎2 has top frame 𝜙 2 ; it has two variables, this and x pointing to
𝑜 3 and 𝑜 7 , and 𝜎3 has top frame 𝜙 3 ; it has two variables, this and x, pointing to 𝑜 7 and 𝑜 3 . We
also highlight the protected objects with a yellow halo. Note that 𝑜 3 is protected in 𝜎2 , but is not
protected in 𝜎3 . This is so, because ⌊this⌋ 𝜎3 is external, and 𝑜 3 is an argument to the call. As a
result, during the call, 𝑜 7 may obtain direct access to 𝑜 3 .




          protected from 𝑜 5                          protected from 𝑜 7                    protected from 𝑜 2




            protected in 𝜎1                             protected in 𝜎2                      protected in 𝜎3

                  Fig. 12. Protection. Pink objects are external, and green objects are internal.

  In order to prove 4.5 from the next appendix, we first formulate and prove the following auxiliary
lemma, which allows us to replace any variable 𝑥 in an extended expression e, by its interpretation
Lemma C.1. For all extended expressions e, addresses 𝛼 and variables 𝑥, so that 𝑥 ∈ 𝑑𝑜𝑚(𝜎) :
   • 𝑀, 𝜎, e ↩→ 𝛼 ⇐⇒ 𝑀, 𝜎, e[⌊𝑥⌋ 𝜎 /𝑥] ↩→ 𝛼
  Note that in the above we require that 𝑥 ∈ 𝑑𝑜𝑚(𝜎), in order to ensure that the replacement
[⌊𝑥⌋ 𝜎 /𝑥] is well-defined. On the other hand, we do not require that 𝑥 ∈ 𝐹𝑣 (e), because if 𝑥 ∉ 𝐹𝑣 (e),
                  txt
then e[⌊𝑥⌋ 𝜎 /𝑥] = e and the guarantee from above becomes a tautology.
Proof of Lemma C.1 The proof goes by induction on the structure of e – as defined in Def. 4.1 –
and according to the expression evaluation rules from Fig. 9. End of Proof




, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                               33


D     Appendix to Section 4.3 – Preservation of Satisfaction
Proof of lemma 4.5
  We first prove that for any 𝑀 𝐴, 𝜎
    (1) To show that 𝑀, 𝜎 |= 𝐴 ⇐⇒        𝑀, 𝜎 |= 𝐴[⌊𝑥⌋ 𝜎 /𝑥]
        The proof goes by induction on the structure of 𝐴, application of Defs. 4.3, 4.4, and 4.4.
    (2) To show that 𝑀, 𝜎 |= 𝐴 ⇐⇒ 𝑀, 𝜎 [cont ↦→ 𝑠𝑡𝑚𝑡] |= 𝐴
        The proof goes by induction on the structure of 𝐴, application of Defs. 4.3, 4.4, and 4.4.
  The lemma itself then follows form (1) and (2) proven above.
End Proof
  In addition to what is claimed in Lemma 4.5, it also holds that

Lemma D.1. 𝑀, 𝜎, e ↩→ 𝛼 =⇒ [ 𝑀, 𝜎 |= 𝐴 ⇐⇒ 𝑀, 𝜎 |= 𝐴[𝛼/e] ]

  Proof. by induction on the structure of 𝐴, application of Defs. 4.3, 4.4, and 4.4, and , and auxiliary
lemma C.1.
                                                                                                       □

D.1     Stability
We first give complete definitions for the concepts of 𝑆𝑡𝑏𝑙 (_]) and 𝑆𝑡𝑏 + (_)

Definition D.2. [𝑆𝑡𝑏𝑙 (_)] assertions:
                              𝑆𝑡𝑏𝑙 (⟨⟨e⟩⟩ ) ≜ 𝑓 𝑎𝑙𝑠𝑒
    𝑆𝑡𝑏𝑙 (⟨⟨e⟩⟩←
               ×− 𝑢) = 𝑆𝑡𝑏𝑙 (e : intl) = 𝑆𝑡𝑏𝑙 (e) = 𝑆𝑡𝑏𝑙 (e : 𝐶) ≜ 𝑡𝑟𝑢𝑒
    𝑆𝑡𝑏𝑙 (𝐴1 ∧ 𝐴2 ) ≜ 𝑆𝑡𝑏𝑙 (𝐴1 ) ∧ 𝑆𝑡𝑏𝑙 (𝐴2 )        𝑆𝑡𝑏𝑙 (∀𝑥 : 𝐶.𝐴) = 𝑆𝑡𝑏𝑙 (¬𝐴) ≜ 𝑆𝑡𝑏𝑙 (𝐴)

Definition D.3 (𝑆𝑡𝑏 + (_)). assertions:
                                 ×− 𝑢) = 𝑆𝑡𝑏 + (e : intl) = 𝑆𝑡𝑏 + (e) = 𝑆𝑡𝑏 + (e : 𝐶) ≜ 𝑡𝑟𝑢𝑒
    𝑆𝑡𝑏 + (⟨⟨e⟩⟩ ) = 𝑆𝑡𝑏 + (⟨⟨e⟩⟩←
                              𝑆𝑡𝑏 + (𝐴1 ∧ 𝐴2 ) ≜ 𝑆𝑡𝑏 + (𝐴1 ) ∧ 𝑆𝑡𝑏 + (𝐴2 )
                                     𝑆𝑡𝑏 + (∀𝑥 : 𝐶.𝐴) ≜ 𝑆𝑡𝑏 + (𝐴)
                                        𝑆𝑡𝑏 + (¬𝐴) ≜ 𝑆𝑡𝑏𝑙 (𝐴)

  The definition of 𝑆𝑡𝑏 + (_) is less general than would be possible. E.g., (⟨⟨𝑥⟩⟩ → 𝑥 .𝑓 = 4) → 𝑥 𝑓 .3 = 7
does not satisfy our definition of 𝑆𝑡𝑏 + (_). We have given these less general definitions in order to
simplify both our defintions and our proofs.
Proof of lemma 4.6 Take any state 𝜎, frame 𝜙, assertion 𝐴,
      • To show
        𝑆𝑡𝑏𝑙 (𝐴) ∧ 𝐹𝑣 (𝐴) = ∅ =⇒ [ 𝑀, 𝜎 |= 𝐴 ⇐⇒ 𝑀, 𝜎 ▽ 𝜙 |= 𝐴 ]
        By induction on the structure of the definition of 𝑆𝑡𝑏𝑙 (𝐴).
      • To show
        𝑆𝑡𝑏 + (𝐴) ∧ 𝐹𝑣 (𝐴) = ∅ ∧ 𝑀 · 𝑀 |= 𝜎 ▽ 𝜙 ∧ 𝑀, 𝜎 |= 𝐴 ∧ 𝑀, 𝜎 ▽ 𝜙 |= intl =⇒
                         𝑀, 𝜎 ▽ 𝜙 |= 𝐴
        By induction on the structure of the definition of 𝑆𝑡𝑏 + (𝐴). The only interesting case is
        when 𝐴 has the form ⟨ e⟩⟩ . Because 𝑓 𝑣 (𝐴) = ∅, we know that ⌊e⌋ 𝜎 =⌊e⌋ 𝜎 ▽ 𝜙 . Therefore,
        we assume that ⌊e⌋ 𝜎 = 𝛼 for some 𝛼, assume that 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩ , and want to show that
        𝑀, 𝜎 ▽ 𝜙 |= ⟨ 𝛼⟩⟩ . From 𝑀 · 𝑀 |= 𝜎 ▽ 𝜙 we obtain that 𝑅𝑛𝑔(𝜙) ⊆ 𝑅𝑛𝑔(𝜎). From this, we obtain
        that 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 ▽ 𝜙) ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎). The rest follows by unfolding and folding Def. 4.4.
End Proof

                                                        , Vol. 1, No. 1, Article . Publication date: November 2025.
34                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


D.2     Encapsulation
Proofs of adherence to ℒ 𝑠𝑝𝑒𝑐 specifications hinge on the expectation that some, specific, assertions
cannot be invalidated unless some internal (and thus known) computation took place. We call
such assertions encapsulated. We define the judgement, 𝑀 ⊢ 𝐸𝑛𝑐 (𝐴), in terms of the judgment
𝑀; Γ ⊢ 𝐸𝑛𝑐 (𝐴); Γ ′ from Fig. 13. This judgements ensures that any objects whose fields are read in
the validation of 𝐴 are internal, that ⟨ _⟩⟩←×− _ does not appear in 𝐴, and that protection assertions (ie
⟨ ⟩ or ⟨ _⟩⟩←×− _) do not appear in negative positions in 𝐴. The second environment in this judgement,
Γ ′ , is used to keep track of any variables introduces in that judgment, e.g. we would have that
          𝑀𝑔𝑜𝑜𝑑 , ∅ ⊢ 𝐸𝑛𝑐 (𝑎 : Account ∧ 𝑘 : Key ∧ ⟨ 𝑎.key⟩⟩ ∧ 𝑎.key ≠ 𝑘); (𝑎 : Account, 𝑘 : Key.
     We assume a type judgment 𝑀; Γ ⊢ 𝑒 : intl which says that in the context of Γ, the expression
𝑒 belongs to a class from 𝑀. We also assume that the judgement 𝑀; Γ ⊢ 𝑒 : intl can deal with
ghostfields – namely, ghost-methods have to be type checked in the contenxt of 𝑀 and therefor
they will only read the state of internal objects. Note that it is possible for 𝑀; Γ ⊢ 𝐸𝑛𝑐 (e); Γ ′ to hold
and 𝑀; Γ ⊢ 𝑒 : intl not to hold – c.f. rule Enc_1.

                           Enc_1                                       Enc_2                                  Enc_3
         𝑀; Γ ⊢ e : intl                                                                  𝑀; Γ ⊢ 𝐸𝑛𝑐 (𝐴); Γ ′
         𝑀; Γ ⊢ 𝐸𝑛𝑐 (e); Γ ′                         𝑀; Γ ⊢ 𝐸𝑛𝑐 (e); Γ ′                  𝐴 does not contain ⟨ _⟩⟩
         𝑀; Γ ⊢ 𝐸𝑛𝑐 (e.𝑓 ); Γ ′                 𝑀; Γ ⊢ 𝐸𝑛𝑐 (e : 𝐶); (Γ ′, e : 𝐶)           𝑀; Γ ⊢ 𝐸𝑛𝑐 (¬𝐴); Γ ′

                          Enc_4                                       Enc_5                                    Enc_6
       𝑀; Γ ⊢ 𝐸𝑛𝑐 (𝐴1 ); Γ ′′
       𝑀; Γ ′′ ⊢ 𝐸𝑛𝑐 (𝐴2 ); Γ ′                 𝑀; Γ, 𝑥 : 𝐶 ⊢ 𝐸𝑛𝑐 (𝐴); Γ ′                   𝑀; Γ ⊢ 𝐸𝑛𝑐 (e); Γ ′
      𝑀; Γ ⊢ 𝐸𝑛𝑐 (𝐴1 ∧ 𝐴2 ); Γ ′                𝑀; Γ ⊢ 𝐸𝑛𝑐 (∀𝑥 : 𝐶.𝐴); Γ ′               𝑀; Γ ⊢ 𝐸𝑛𝑐 (e : extl); Γ ′

                           Enc_7
        𝑀; Γ ⊢ 𝐸𝑛𝑐 (e); Γ ′
       𝑀; Γ ⊢ 𝐸𝑛𝑐 (⟨⟨e⟩⟩ ); Γ ′

                                       Fig. 13. The judgment 𝑀; Γ ⊢ 𝐸𝑛𝑐 (𝐴); Γ ′


Definition D.4 (An assertion 𝐴 is encapsulated by module 𝑀).

      • 𝑀 ⊢ 𝐸𝑛𝑐 (𝐴) ≜ ∃Γ.[ 𝑀; ∅ ⊢ 𝐸𝑛𝑐 (𝐴); Γ ] as defined in Fig. 13.
  To motivate the design of our judgment 𝑀; Γ ⊢ 𝐸𝑛𝑐 (𝐴); Γ ′ , we first give a semantic notion of
encapsulation:
Definition D.5. An assertion 𝐴 is semantically encapsulated by module 𝑀:
   • 𝑀 |= 𝐸𝑛𝑐 (𝐴) ≜ ∀𝑀, 𝜎, 𝜎 ′ .[ 𝑀, 𝜎 |= (𝐴 ∧ extl) ∧ 𝑀 ·𝑀; 𝜎 ⇝ 𝜎 ′ =⇒ 𝑀, 𝜎 ′ |= 𝜎⌈𝐴⌉ ]
More on Def. D.5 If the definition D.5 or in lemma 4.8 we had used the more general execution,
𝑀 · 𝑀; 𝜎 d 𝜎 ′ , rather than the scoped execution, 𝑀 · 𝑀; 𝜎 ⇝ 𝜎 ′ , then fewer assertions would
have been encapsulated. Namely, assertions like ⟨ 𝑥 .𝑓 ⟩ would not be encapsulated. Consider, e.g.,
a heap 𝜒, with objects 1, 2, 3 and 4, where 1, 2 are external, and 3, 4 are internal, and 1 has fields
pointing to 2 and 4, and 2 has a field pointing to 3, and 3 has a field 𝑓 pointing to 4. Take state
𝜎=(𝜙 1 ·𝜙 2, 𝜒), where 𝜙 1 ’s receiver is 1, 𝜙 2 ’s receiver is 2, and there are no local variables. We have
...𝜎 |= extl ∧ ⟨ 3.𝑓 ⟩ . We return from the most recent all, getting ...; 𝜎 d 𝜎 ′ where 𝜎 ′ = (𝜙 1, 𝜒); and
have ..., 𝜎 ′ ̸ |= ⟨ 3.𝑓 ⟩ .

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                 35


Example D.6. For an assertion 𝐴𝑏𝑎𝑙 ≜ 𝑎 : Account ∧ 𝑎.balance = 𝑏, and modules Mbad and
Mfine from § 2, we have Mbad |= 𝐸𝑛𝑐 (𝐴𝑏𝑎𝑙 ), and Mbad |= 𝐸𝑛𝑐 (𝐴𝑏𝑎𝑙 ).
Example D.7. Assume further modules, M𝑢𝑛𝑝 and M𝑝𝑟𝑡 , which use ledgers mapping accounts
to their balances, and export functions that update this map. In M𝑢𝑛𝑝 the ledger is part of the
internal module, while in M𝑝𝑟𝑡 it is part of the external module. Then M𝑢𝑛𝑝 ̸ |= 𝐸𝑛𝑐 (𝐴𝑏𝑎𝑙 ), and
M𝑝𝑟𝑡 |= 𝐸𝑛𝑐 (𝐴𝑏𝑎𝑙 ). Note that in both M𝑢𝑛𝑝 and M𝑝𝑟𝑡 , the term a.balance is a ghost field.
Note D.8. Relative protection is not encapsulated, (e.g. 𝑀 ̸ |= 𝐸𝑛𝑐 (⟨⟨𝑥⟩⟩←
                                                                          ×− 𝑦)), even though absolute
protection is (e.g. 𝑀 |= 𝐸𝑛𝑐 (⟨⟨𝑥⟩⟩ )). Encapsulation of an assertion does not imply encapsulation of
its negation; for example, 𝑀 ̸ |= 𝐸𝑛𝑐 (¬⟨⟨𝑥⟩⟩ ).
More on Def. D.4 This definition is less permissive than necessary. For example 𝑀 ⊬ 𝐸𝑛𝑐 (¬(¬⟨⟨𝑥⟩⟩ ))
even though 𝑀 |= 𝐸𝑛𝑐 (¬(¬⟨⟨𝑥⟩⟩ )). Namely, ¬(¬⟨⟨𝑥⟩⟩ ) ≡ ⟨ 𝑥⟩⟩ and 𝑀 ⊢ 𝐸𝑛𝑐 (⟨⟨𝑥⟩⟩ ). A more permissive,
sound, definition, is not difficult, but not the main aim of this work. We gave this, less permissive
definition, in order to simplify the definitions and the proofs.
Proof of lemma 4.8 This says that 𝑀 ⊢ 𝐸𝑛𝑐 (𝐴) implies that 𝑀 ⊢ 𝐸𝑛𝑐 (𝐴).
We fist prove that
   (*) Assertions 𝐴𝑝𝑜𝑜𝑟 which do not contain ⟨ _⟩⟩ or ⟨ _⟩⟩←×− _ are preserved by any external step.
Namely, such an assertion only depends on the contents of the fields of internal objects, and these
are not modified by external steps. Such an 𝐴𝑝𝑜𝑜𝑟 is defined essentially through
    𝐴𝑝𝑜𝑜𝑟 ::= e | e : 𝐶 | ¬𝐴𝑝𝑜𝑜𝑟 | 𝐴𝑝𝑜𝑜𝑟 ∧ 𝐴𝑝𝑜𝑜𝑟 | ∀𝑥 : 𝐶.𝐴𝑝𝑜𝑜𝑟 | e : extl
We can prove (*) by induction on the structure of 𝐴𝑝𝑜𝑜𝑟 and case analysis on the execution step.
We then prove Lemma 4.8 by induction on the structure of 𝐴.
— The cases Enc_1, Enc_2, and Enc_6 are straight application of (*).
— The case Enc_3 also follows from (*), because any 𝐴 which satisfies 𝐸𝑛𝑐 (𝐴) and which does not
 contain ⟨ _⟩⟩ is an 𝐴𝑝𝑜𝑜𝑟 assertion.
— The cases Enc_4 and Enc_5 follow by induction hypothesis.
— The case Enc_7 is more interesting.
We assume that 𝜎 is an external state, that ...; 𝜎 ⇝ 𝜎 ′ , and that ..𝜎 |= ⟨ e⟩⟩ . By definition, the latter
 means that
      (**) no locally reachable external object in 𝜎 has a field ponting to e,
           nor is e one of the variables.
We proceed by case analysis on the step ...; 𝜎 ⇝ 𝜎 ′ .
- If that step was an assignment to a local variable 𝑥, then this does not affect ⟨ 𝜎⌈e⌉⟩⟩ because in
 ⌊e⌋ 𝜎 =⌊ 𝜎⌈e⌉⌋ 𝜎 ′ , and ...𝜎 ′ |= 𝑥 ≠ 𝑟𝑒.
- If that step was an assignment to an external object’s field, of the form 𝑥 .𝑓 := 𝑦 then this does not
 affect ⟨ 𝜎⌈e⌉⟩⟩ either. This is so, because 𝐸𝑛𝑐 (e) gives that ⌊e⌋ 𝜎 =⌊ ′ ⌋ 𝜎 𝜎⌈e⌉ – namely the evaluation of
 e does not read 𝑥’s fields, since 𝑥 is external. And moreover, the assignment 𝑥 .𝑓 := 𝑦 cannot create
 a new, unprotected path to e (unprotected means here that the penultimate element in that path is
 external), because then we would have had in 𝜎 an unprotected path from 𝑦 to e.
- If that step was a method call, then we apply lemma 3.6 which says that all objects reachable in 𝜎 ′
were already reachable in 𝜎.
- Finally, we do not consider method return (i.e. the rule Return), because we are looking at
 ...; _ ⇝ _ execution steps rather than ...; _ d _ steps.                               End Proof




                                                          , Vol. 1, No. 1, Article . Publication date: November 2025.
36                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


E     Appendix to Section 5 – Specifications
Example E.1 (Badly Formed Method Specifications). 𝑆 9,𝑏𝑎𝑑_1 is not a well-formed specification,
because 𝐴′ is not a formal parameter, nor free in the precondition.
        𝑆 9,𝑏𝑎𝑑_1 ≜ { 𝑎 : Account ∧ ⟨ 𝑎⟩⟩ }
                            public Account :: set(key’ : Key)
                       { ⟨ 𝑎⟩⟩ ∧ ⟨ 𝑎 ′ .key⟩⟩ } ∥ {𝑡𝑟𝑢𝑒}
        𝑆 9,𝑏𝑎𝑑_2 ≜ { 𝑎 : Account ∧ ⟨ 𝑎⟩⟩ }
                            public Account :: set(key’ : Key)
                       { ⟨ 𝑎⟩⟩ ∧ ⟨ 𝑎 ′ .key⟩⟩ } ∥ {this.blnce }

Example E.2 (More Method Specifications). 𝑆 7 below guarantees that transfer does not affect
the balance of accounts different from the receiver or argument, and if the key supplied is not that
of the receiver, then no account’s balance is affected. 𝑆 8 guarantees that if the key supplied is that
of the receiver, the correct amount is transferred from the receiver to the destination. 𝑆 9 guarantees
that set preserves the protectedness of a key.
       𝑆7    ≜    { 𝑎 : Account ∧ 𝑎.blnce = 𝑏 ∧ (dst ≠ 𝑎 ≠ this ∨ key’ ≠ 𝑎.key) }
                       public Account :: transfer(dst : Account, key’ : Key, amt : nat)
                  { 𝑎.blnce = 𝑏 } ∥ {𝑎.blnce = 𝑏}
       𝑆8    ≜    { this ≠ dst ∧ this.blnce = 𝑏 ∧ dst.blnce = 𝑏 ′ }
                       public Account :: transfer(dst : Account, key’ : Key, amt : nat)
                  { this.blnce = 𝑏 − amt ∧ dst.blnce = 𝑏 ′ + amt }
                   ∥ {this.blnce = 𝑏 ∧ dst.blnce = 𝑏 ′ }
       𝑆9    ≜    { 𝑎 : Account ∧ ⟨ 𝑎.key⟩⟩ }
                       public Account :: set(key’ : Key)
                  { ⟨ 𝑎.key⟩⟩ } ∥ {⟨⟨𝑎.key⟩⟩ }

E.1    Examples of Semantics of our Specifications
Example E.3. We revisit the specifications given in Sect. 2.1, the three modules from Sect. 2.2.2,
and Example E.2
   Mgood |= 𝑆 1 Mgood |= 𝑆 2 Mgood |= 𝑆 3 Mgood |= 𝑆 5
   Mbad |= 𝑆 1 Mbad ̸ |= 𝑆 2 Mbad ̸ |= 𝑆 3 Mbad ̸ |= 𝑆 5
   Mfine |= 𝑆 1 Mfine |= 𝑆 2 Mfine ̸ |= 𝑆 3 Mfine ̸ |= 𝑆 5

Example E.4. For Example 5.5, we have Mgood |= 𝑆 7 and Mbad |= 𝑆 7 and Mfine |= 𝑆 7 . Also, Mgood |= 𝑆 8
and Mbad |= 𝑆 8 and Mfine |= 𝑆 8 . However, Mgood |= 𝑆 9 , while Mbad ̸ |= 𝑆 9 .

Example E.5. For any specification 𝑆 ≜ { 𝐴 } 𝑝 𝐶 ::𝑚(𝑥 : 𝐶) { 𝐴′ } and any module 𝑀 which does
not have a class 𝐶 with a method 𝑚 with formal parameter types 𝐶, we have that 𝑀 |= 𝑆. Namely,
if a method were to be called with that signature on a 𝐶 from 𝑀, then execution would be stuck,
and the requirements from Def. 5.4(3) would be trivially satisfied. Thus, Mfine |= 𝑆 8 .

E.1.1 Free variables in well-formed specifications. We now discuss the requirements about free
variables in well-formed specifications as defined in Def. 5.6. In scoped invariants, 𝐴 may only
mention variables introduced by the quantifier, 𝑥. In method specifications, the precondition,
𝑥 : 𝐶 ′ ∧ 𝐴, may only mention the receiver, this, the formal parameters, 𝑦, and the explicitly
introduced variables, 𝑥; it may not mention the result res. The postcondition, 𝐴′ , may mention
these variables, and in addition, may mention the result, res. The mid-condition, 𝐴′′ is about
a state which has at least one more frame than the current method’s, and therefore it may not
mention this, nor 𝑦, nor res.

, Vol. 1, No. 1, Article . Publication date: November 2025.
     Reasoning about External Calls – Extended Version                                                              37


     F     Expressiveness


 1   module DOM
 2      class Node
 3         field cnt: int
 4         field parent: Node
 5
 6         class Proxy
 7            field hght: nat
 8            field node: Node
 9
10            public method set(newCnt:int, up:nat): void
11                  if this.hght >= up
12                     setPrivate(newCnt, up)
13                  else
14                     return
15
16            private method setPrivate(newCnt:int, up:nat): void
17                  if up==0 then
18                     this.node.cnt := nwCnt
19                  else
20                     setPrivate(newCnt, up-1)


                                 Fig. 14. The DOM module – classes Node and Proxy


        We argue the expressiveness of our approach by comparing with example specifications proposed
     in [34, 76, 100].

     F.1    The DOM
     F.1.1 The Problem. This is the motivating example in [34]. It deals with a tree of DOM nodes:
     Access to a DOM node gives access to all its parents, with the ability to modify the node’s
     contents – where parent and cnt are fields in class Node. Since the top nodes of the tree usually
     contain privileged information, while the lower nodes contain less crucial third-party information,
     we must be able to limit access given to third parties to only the lower part of the DOM tree.
        To do this, Devriese et al. [34] propose a Proxy class, which has a field node pointing to a Node,
     and a field height (hght), which restricts the range of Nodes which may be modified through
     the use of the particular Proxy. Namely, a Proxy may modify the cnt of all the ancestors of its
     node, up to the hght-th ancestor of that node.
        A possible implementation of such Node and Proxy classes is shown in Fig. 14, while the
     creation of a tree, three proxies, and passing the proxies to the external world is shown in Fig 15.
        In Fig. 16 we show a diagram of a tree consisting of the five nodes, nd1, nd2, nd3, nd4 and
     nd5, and three proxies, prx10, prx11, and prx12. These are created in lines 6-15 in the code
     in Fig. 15. Moreover, in Fig. 17 we revisit the diagram, and show highlight that three objects have
     capability on nd4.cnt, while two objects have capability on nd2.cnt, and finally, only one
     object has capability on nd1.cnt.
        We now consider the remaining code in Fig. 15:
           • The first external call, in line 18, does not affect the DOM tree or is cnt, because untrst
             has no access to it.

                                                            , Vol. 1, No. 1, Article . Publication date: November 2025.
     38                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


 1   module DOM
 2      ... as before ...
 3      class Example
 4         public method demo(untrst:external) : void
 5             // create a tree of Node𝑠
 6            nd1 := new Node; nd1.cnt := 1
 7            nd2 := new Mode; nd2.parent:= nd1; nd2,ctns:=2;
 8            nd3 := new Mode; nd3.parent:= nd1; nd3,ctns:=3;
 9            nd4 := new Mode; nd4.parent:= nd2; nd4,ctns:=4;
10            nd5 := new Mode; nd5.parent:= nd2; nd5,ctns:=5;
11
12                // create three Proxy𝑠
13                prx10 := newProxy; prx10.height:=2; prx10.node:=nd4;
14                prx11 := newProxy; prx10.height:=1; prx10.node:=nd4;
15                prx12 := newProxy; prx10.height:=0; prx10.node:=nd4;
16
17                // External calls:
18                untrst.meth_A();                   // no modification in the tree
19
20                untrst.meth_B(nd2);                // no modification in the tree
21
22                untrst.meth_C(prx12);              // nd4.cnt may have changed;
23                                                   // all else has stayed the same
24
25                nd4.ctns:=4                        // re-establish old value of nd4.ctns
26                untrst.meth_A( );                  // nd4.cnt may have changed again;
27                                                   // all else has stayed the same
28
29                untrst.meth_C(prx12);              // nd4.cnt, nd2.cnt, and nd1.ctns may have changed;
30                                                   // all else has stayed the same
31
32               // Revocation:
33                prx12.height := 1;                 // revocation
34                nd1.ctns:=1                        // re-establigh the old value of nd1.ctns
35                untrst.meth_C(prx12);              // nd1.ctns does not change


                                   Fig. 15. The DOM module continued – class Example




          • The second external call, in line 20, also does not affect the DOM tree or is cnt – even though
            untrst has access to a Node, because the class has no public method, none of its fields
            may be modified.
          • The third external call, in line 22, may affect the contents of nd4.ctns, because we have
            passed the capability prx12 in the call. From then on, the capability is no longer protected.
          • Before the fourth external call, on line 25, we restore the value of nd4.cnt to what it was
            earlier. Nevertheless, even though the fourth external call, on line 26, is identical to the from
            line 19, it may result in a modification of nd4.ctns. This is so, because prx12 is no longer
            protected.
          • The fifth external call, on line 29, may result in the modification of nd4.ctns, nd2.ctns,
            and nd1.ctns, because we have passed the capability prx10.

     , Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                      39


    • We now revoke the capability of prx12, on line 34, so that it can only affect nd4.cnt and
      nd2.cnt. We re-establish the value of nd1.cnt on line 35, and on line 36 we make an
      external call. We know that this call cannot affect the value of nd1.cnt. 15




                       Fig. 16. DOM tree and Proxies, created as in the code from Fig 15




 prx10, prx10, and prx12 are the                 prx10 and prx11 are the                    prx10 is the
     capabilities for nd4.cnt                     capabilities for nd2.cnt             capability for nd1.cnt

Fig. 17. Capabilities for the DOM tree from Fig. 16. In particular, notice the many-to-many relation between
capabilities and effects: For example, there are three capabilities on nd4.cnt. And prx10 has capabilities
on cnt of three objects.


F.1.2 Specifications. We now discuss possible specifications. For this, we will use the predicate
𝑚𝑎𝑦_𝑚𝑜𝑑𝑖 𝑓 𝑦 ⊆ Proxy × Node, which says that prx has modification-capabilities on nd, where
prx is a Proxy and nd is a Node, if nd is the prx𝑘 𝑡ℎ parent of pr.node where 𝑘 ≤ nd.hght.
The formal definition is as follows:
      𝑚𝑎𝑦_𝑚𝑜𝑑𝑖𝑓𝑦 (prx, nd) ≜ ∃𝑘 : N.[ prx.node.parent𝑘 = nd ∧ 𝑘 ≤ prx.hght]
Thus, a Proxy object prx, which satisfies 𝑚𝑎𝑦_𝑚𝑜𝑑𝑖𝑓𝑦 (prx, nd) is a capability which may modify
the node nd.
We now use 𝑚𝑎𝑦_𝑚𝑜𝑑𝑖 𝑓 𝑦 in writing the specifications. Below, 𝑆𝑑𝑜𝑚_1 mandates that nodes, nd
are not leaked. Moreover, 𝑆𝑑𝑜𝑚_2 and 𝑆𝑑𝑜𝑚_3 mandate that the parent node of a Node cannot be
modified by external code: Similarly, 𝑆𝑑𝑜𝑚_4 mandates that proxies which 𝑚𝑎𝑦_𝑚𝑜𝑑𝑖𝑓𝑦 (prx, nd)
are not leaked. Finally, 𝑆𝑑𝑜𝑚_5 mandates that proxies which 𝑚𝑎𝑦_𝑚𝑜𝑑𝑖𝑓𝑦 (prx, nd) are not leaked,
and that when a node 𝑛𝑑 is protected, and all proxies that can 𝑚𝑎𝑦_𝑚𝑜𝑑𝑖𝑓𝑦 (prx, nd) are protected,
then the 𝑐𝑛𝑡 of 𝑛𝑑 cannot be modified by external code.
15 Another example of a revocation would be to set the parent of nd4 to be nd3; then, prx11 would have capability on

nd4 and nd3. On the other hand, setting the parent of nd4 to be nd1 would augment the capability of prx11; such an
augmentation would, however be forbidden by 𝑆𝑑𝑜𝑚4 , if the corresponding capability was had already been exported to the
external world.


                                                               , Vol. 1, No. 1, Article . Publication date: November 2025.
    40                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble

                           A
            𝑆𝑑𝑜𝑚_1 ≜          nd : Node.{ ⟨ nd⟩⟩ ] }
                          A
            𝑆𝑑𝑜𝑚_2 ≜        nd : Node, nd’ : Node.{ nd.parent = nd′ }
                          A
            𝑆𝑑𝑜𝑚_3 ≜        nd : Node.{ nd.parent = null }
                           A
            𝑆𝑑𝑜𝑚_4 ≜          nd : Node.{ ∀prx : Proxy.[ 𝑚𝑎𝑦_𝑚𝑜𝑑𝑖𝑓𝑦 (prx, nd) → ⟨ prx⟩⟩ ] }

           𝑆𝑑𝑜𝑚_5 ≜ ∀nd : Node.∀val : Object.
                      { ⟨ nd⟩⟩ ∧ ∀prx : Proxy.[ 𝑚𝑎𝑦_𝑚𝑜𝑑𝑖𝑓𝑦 (prx, nd) → ⟨ prx⟩⟩ ] ∧ nd.cnt = val }
       Note that 𝑆𝑑𝑜𝑚_5 is strictly stronger than 𝑆𝑑𝑜𝑚_4 . The module shown in Fig. 14 and 15 does satisfy
    all the specifications from above.
       The careful reader might worry that the method demo in class Example in Fig. 15 breaks
    specifications 𝑆𝑑𝑜𝑚_1 , and 𝑆𝑑𝑜𝑚_4 , since it does export nd1 and prx12. However, there is no
    external state between the creation of nd1 and its export, and so our scoped invariant is preserved.
    Similarly, there is no external state between the creation of prx10 and its export, and so our
    scoped invariant is preserved.
       To prove that the external calls in Fig. 15 preserve the stated properties we need to apply the
    specifications 𝑆𝑑𝑜𝑚_2 , and 𝑆𝑑𝑜𝑚_5 , but we do not need 𝑆𝑑𝑜𝑚_1 or 𝑆𝑑𝑜𝑚_3 .

    F.1.3    Other Specifications. Mackay et al. [76] specify this as:

1   DOMSpec ≜ from nd : Node ∧ nd.property = p to nd.property != p
2     onlyIf ∃ o.[ o : extl ∧
3        (∃ nd':Node.[ ⟨o access nd’⟩ ] ∨
4         ∃ pr:Proxy,k:N.[ ⟨o access pr⟩ ∧ nd.parentk =pr.node.parentpr.height ]                                )    ]


       DomSpec states that the property of a node can only change if some external object presently
    has access to a node of the DOM tree, or to some Proxy with modification-capabilties to the node
    that was modified. The assertion ∃𝑜.[ o : extl ∧ ⟨o access pr⟩ ] is the contrapositive of our
    ⟨ 𝑝𝑟 ⟩ , but is is weaker than that, because it does not specify the frame from which 𝑜 is accessible.
    Therefore, DOMSpec is a stronger requirement than 𝑆𝑑𝑜𝑚_1 .

    F.2     DAO
    The Decentralized Autonomous Organization (DAO) [25] is a well-known Ethereum contract
    allowing participants to invest funds. The DAO famously was exploited with a re-entrancy bug in
    2016, and lost $50M. Here we provide specifications that would have secured the DAO against such
    a bug.
                          A
           𝑆𝑑𝑎𝑜_1 ≜ 𝑑 : DAO.{ ∀𝑝 : Participant.[ 𝑑.𝑒𝑡ℎ𝑒𝑟 ≥ 𝑑.𝑏𝑎𝑙𝑎𝑛𝑐𝑒 (𝑝) ] }
                          A                  Í
           𝑆𝑑𝑎𝑜_2 ≜ 𝑑 : DAO.{ 𝑑.𝑒𝑡ℎ𝑒𝑟 ≥ 𝑝 ∈𝑑.𝑝𝑎𝑟𝑡𝑖𝑐𝑖𝑎𝑛𝑡𝑠 𝑑.𝑏𝑎𝑙𝑎𝑛𝑐𝑒 (𝑝) }
       The specifications above say the following:
         𝑆𝑒𝑑𝑎𝑜_1 guarantees that the DAO holds more ether than the balance of any of its participant’s.

                  guarantees that that the DAO holds more ether than the sum of the balances held by
            𝑆𝑑𝑎𝑜_2
                  DAO’s participants.
      𝑆𝑑𝑎𝑜_2 is stronger than 𝑆𝑑𝑎𝑜_1 . They would both have precluded the DAO bug. Note that these
    specifications do not mention capabilities. They are, essentially, simple class invariants and could
    have been expressed with the techniques proposed already by [82]. The only difference is that
    𝑆𝑑𝑎𝑜_1 and 𝑆𝑑𝑎𝑜_2 are two-state invariants, which means that we require that they are preserved, i.e.

    , Vol. 1, No. 1, Article . Publication date: November 2025.
    Reasoning about External Calls – Extended Version                                                                  41


    if they hold in one (observable) state they have to hold in all successor states, while class invariants
    are one-state, which means they are required to hold in all (observable) states. 16

      We now compare with the specification given in [76]. DAOSpec1 in similar to 𝑆𝑑𝑎𝑜_1 : iy says
    that no participant’s balance may ever exceed the ether remaining in DAO. It is, essentially, a
    one-state invariant.
1   DAOSpec1 ≜ from d : DAO ∧ p : Object
2               to d.balance(p) > d.ether
3               onlyIf false

    DAOSpec1, similarly to 𝑆𝑑𝑎𝑜_1 , in that it enforces a class invariant of DAO, something that could
    be enforced by traditional specifications using class invariants.
      [76] gives one more specification:
1   DAOSpec2 ≜ from d : DAO ∧ p : Object
2               next d.balance(p) = m
3               onlyIf ⟨p calls d.repay(_) ⟩ ∧ m = 0 ∨ ⟨p calls d.join(m) ⟩ ∨ d.balance(p) = m

       DAOSpec2 states that if after some single step of execution, a participant’s balance is m, then
    either
    (a) this occurred as a result of joining the DAO with an initial investment of m,
    (b) the balance is 0 and they’ve just withdrawn their funds, or
    (c) the balance was m to begin with

    F.3   ERC20
    The ERC20 [113] is a widely used token standard describing the basic functionality of any Ethereum-
    based token contract. This functionality includes issuing tokens, keeping track of tokens belonging
    to participants, and the transfer of tokens between participants. Tokens may only be transferred if
    there are sufficient tokens in the participant’s account, and if either they (using the transfer
    method) or someone authorised by the participant (using the transferFrom method) initiated
    the transfer.
       For an 𝑒 : ERC20, the term 𝑒.𝑏𝑎𝑙𝑎𝑛𝑐𝑒 (𝑝) indicates the number of tokens in participant 𝑝’s
    account at 𝑒. The assertion 𝑒.𝑎𝑙𝑙𝑜𝑤𝑒𝑑 (𝑝, 𝑝 ′ ) expresses that participant 𝑝 has been authorised to
    spend moneys from 𝑝 ′ ’s account at 𝑒.
       The security model in Solidity is not based on having access to a capability, but on who the
    caller of a method is. Namely, Solidity supports the construct sender which indicates the identity
    of the caller. Therefore, for Solidity, we adapt our approach in two significant ways: we change
    the meaning of ⟨ e⟩⟩ to express that e did not make a method call. Moreover, we introduce a new,
                                                                        A
    slightly modified form of two state invariants of the form 𝑥 : 𝐶.{𝐴}.{𝐴′ } which expresses that
    any execution which satisfies 𝐴, will preserve 𝐴′ .
       We specify the guarantees of ERC20 as follows:
                        A
           𝑆𝑒𝑟𝑐_2 ≜       𝑒 : ERC20, 𝑝, 𝑝 ′ : Participant, 𝑛 : N.
                                  { ∀𝑝 ′ .[ (𝑒.𝑎𝑙𝑙𝑜𝑤𝑒𝑑 (𝑝 ′, 𝑝) → ⟨ 𝑝 ′ ⟩ ] }.{ 𝑒.𝑏𝑎𝑙𝑎𝑛𝑐𝑒 (𝑏) = 𝑛 }
                        A
           𝑆𝑒𝑟𝑐_3 ≜       𝑒 : ERC20, 𝑝, 𝑝 ′ : Participant.
                                  { ∀𝑝 ′ .[ (𝑒.𝑎𝑙𝑙𝑜𝑤𝑒𝑑 (𝑝 ′, 𝑝) → ⟨ 𝑝 ′ ⟩ ] }.{ ¬(𝑒.𝑎𝑙𝑙𝑜𝑤𝑒𝑑 (𝑝 ′′, 𝑝) }

    16 This should have been explained somewhere earlier.



                                                               , Vol. 1, No. 1, Article . Publication date: November 2025.
    42                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


         The specifications above say the following:
                    guarantees that the the owner of an account is always authorized on that account –
           𝑆𝑒𝑟𝑐_1
                    this specification is expressed using the original version of two-state invariants.

                     guarantees that any execution which does not contain calls from a participant 𝑝 ′
                     authorized on 𝑝’s account will not affect the balance of 𝑒’s account. Namely, if the
           𝑆𝑒𝑟𝑐_2
                     execution starts in a state in which 𝑒.𝑏𝑎𝑙𝑎𝑛𝑐𝑒 (𝑏) = 𝑛, it will lead to a state where
                     𝑒.𝑏𝑎𝑙𝑎𝑛𝑐𝑒 (𝑏) = 𝑛 also holds.

                     guarantees that any execution which does not contain calls from a participant 𝑝 ′
                     authorized on 𝑝’s account will not affect who else is authorized on that account.
           𝑆𝑒𝑟𝑐_3
                     That is, if the execution starts in a state in which ¬(𝑒.𝑎𝑙𝑙𝑜𝑤𝑒𝑑 (𝑝 ′′, 𝑝), it will lead to
                     a state where ¬(𝑒.𝑎𝑙𝑙𝑜𝑤𝑒𝑑 (𝑝 ′′, 𝑝) also holds.


       We compare with the specifications given in [76]: Firstly, ERC20Spec1 says that if the balance of
    a participant’s account is ever reduced by some amount 𝑚, then that must have occurred as a result
    of a call to the transfer method with amount 𝑚 by the participant, or the transferFrom
    method with the amount 𝑚 by some other participant.
1   ERC20Spec1 ≜ from e : ERC20 ∧ e.balance(p) = m + m' ∧ m > 0
2                 next e.balance(p) = m'
3                 onlyIf ∃ p' p''.[⟨p’ calls e.transfer(p, m) ⟩ ∨
4                        e.allowed(p, p'') ≥ m ∧ ⟨p” calls e.transferFrom(p’, m) ⟩]

    Secondly, ERC20Spec2 specifies under what circumstances some participant p’ is authorized to
    spend m tokens on behalf of p: either p approved p’, p’ was previously authorized, or p’ was
    authorized for some amount m + m’, and spent m’.
1   ERC20Spec2 ≜ from e : ERC20 ∧ p : Object ∧ p' : Object ∧ m : Nat
2                 next e.allowed(p, p') = m
3                 onlyIf ⟨p calls e.approve(p’, m) ⟩ ∨
4                        (e.allowed(p, p') = m ∧
5                         ¬ (⟨p’ calls e.transferFrom(p, _) ⟩ ∨
6                                 ⟨p calls e.allowed(p, _) ⟩)) ∨
7                        ∃ p''. [e.allowed(p, p') = m + m' ∧ ⟨p’ calls e.transferFrom(p”, m’) ⟩]

      ERC20Spec1 is related to 𝑆𝑒𝑟𝑐_2 . Note that ERC20Spec1 is more API-specific, as it expresses
    the precise methods which caused the modification of the balance.

    F.4     Wasm, Iris, and the stack
    In [100], they consider inter-language safety for Wasm. They develop Iris-Wasm, a mechanized
    higher-order separation logic mechanized in Coq and the Iris framework. Using Iris-Wasm, with
    the aim to specify and verify individual modules separately, and then compose them modularly
    in a simple host language featuring the core operations of the WebAssembly JavaScript Interface.
    They develop a logical relation that enforces robust safety: unknown, adversarial code can only
    affect other modules through the functions that they explicitly export. They do not offer however a
    logic to deal with the effects of external calls.
       As a running example, they use a stack module, which is an array of values, and exports func-
    tions to inspect the stack contents or modify its contents. Such a setting can be expressed in our lan-
    guage through a stack and a modifier capability. Assuming a predicate 𝐶𝑜𝑛𝑡𝑒𝑛𝑡𝑠 (stack, i, v),
    which expresses that the contents of stack at index i is v, we can specify the stack through

    , Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                           43



                            A
              𝑆𝑠𝑡𝑎𝑐𝑘 ≜         𝑠 : Stack, 𝑖 : N, v : Value.{ ⟨ s.modifier⟩⟩ ∧ 𝐶𝑜𝑛𝑡𝑒𝑛𝑡𝑠 (s, 𝑖, v) }
   In that work, they provide a tailor-made proof that indeed, when the stack makes an external call,
passing only the inspect-capability, the contents will not change. However, because the language is
essentially functional, they do not consider the possibility that the external call might already have
stored the modifier capability. Moreover, the proof does not make use of a Hoare logic.

F.5    Sealer-Unsealer pattern
The sealer-unsealer pattern, proposed by Morris Jr. [90], is a security pattern to enforce data
abstraction while interoperating with untrusted code. He proposes a function makeseal which
generating pairs of functions (seal, unseal ), such that seal takes a value 𝑣 and returns a
low-integrity value 𝑣 ′ . The function unseal when given 𝑣 ′ will return 𝑣. But there is no other
way to obtain 𝑣 out of 𝑣 ′ except throughthe use of the usealer. Thus, 𝑣 ′ can securely be shared
with untrusted code. This pattern has been studied by Swasey et al. [112].
  We formulate this pattern here. As we are working with an object oriented rather than a functional
language, we assume the existence of a class DynamicSealer with two methods, seal, and
unseal. And we define a predicate 𝑆𝑒𝑎𝑙𝑒𝑑 (𝑣, 𝑣 ′, 𝑢𝑠) to express that 𝑣 has been sealed into 𝑣 ′ and
can be unsealed using 𝑢𝑠.
  Then, the scoped invariants
                                           A
                          𝑆𝑠𝑒𝑎𝑙𝑒𝑟 _1 ≜        v, v′, us : Object.{ ⟨ us⟩⟩ ∧ 𝑆𝑒𝑎𝑙𝑒𝑑 (v, v′, us)}

                                      A
                    𝑆𝑠𝑒𝑎𝑙𝑒𝑟 _2 ≜        v, v′, us : Object.{ ⟨ v⟩⟩ ∧ ⟨ us⟩⟩ ∧ 𝑆𝑒𝑎𝑙𝑒𝑑 (v, v′, us)}
expresses that the unsealer is not leaked to external code (𝑆𝑠𝑒𝑎𝑙𝑒𝑟 _1 ), and that if the external world
has no access to the high-integrity value v nor to the its unsealer us, then it will not get access to
the value (𝑆𝑠𝑒𝑎𝑙𝑒𝑟 _2 ).

F.6    Access Security for Hotel Electronic Keys
A hotel giving access to rooms through cards with electronic keys is a case study in [5]. This
paper17 , argue that security should be understood in terms of necessary (rather than sufficient) pre-
conditions – this is as we already proposed in the FASE and our OOPSLA 22 paper. In contrast to our
OOPSLA’22 and the current paper, rather than fall back on a the negation of sufficient conditions,
t[5] propose a Hoare logic for necessary conditions. They propose what the call accessibility tuples,
of the form
                               < 𝑃 > 𝐶 < 𝑄 >
which express that for any states 𝜎,𝜎 ′ , if execution of command 𝐶 in state 𝜎 leads to state 𝜎 ′ , and
if 𝜎 ′ satisfies 𝑄, then 𝜎 must satisfy 𝑃. Moreover, in contrast to our work, the [5] accessibility
tuples are in terms of two conditions and a command, whereas our tuples are only in terms of two
conditions – we quantify universally over the commands.
   The Access Security for Hotel Electronic Keys problem as proposed in [5], in a hotel that uses
cards to control access to its room, the room’s door has a battery-powered lock which has an
electronic door key, dk. A card holds two electronic keys, ck1 and ck2. Such a card can be used to
update the lock’s key: if ck1 is the same as dk, then dk is set to ck2. From then on, ck2 may be
used to open the door. A possible implementation in our toy language looks, essentially, as follows
17 at the time of writing not yet officially published, but fresh in arXive



                                                                    , Vol. 1, No. 1, Article . Publication date: November 2025.
     44                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble



 1   module Hotel
 2      class Card
 3         field ck1, ck2: Object
 4         private init(k1, k2: Object)
 5             this.ck1:= k1;
 6             this.ck2:=k2
 7
 8         class Lock
 9           field dk: Object
10           field is_open: bool
11           private init(k1, k2: Object)
12               this.ck1:= k1;
13               this.ck2:=k2
14
15            public open(card:Card) : void
16                if (this.dk == card.ck1)
17                     this.dk := card.ck2
18                     is_open := true
19                else
20                     is_open := (this.dk == card.ck2)
21


        The code for the electronic keys given in [5] is essentially a snippet – no modules, classes,
     or methods. The paper does not give a specification for the code either, but we assume that the
     specification would be, roughly
        (∗) < c.ck1 == l.dk ∨ c.ck2 == l.dk > l.open(c) < l.is_open >
     where c is a Card and l is a Lock. Notice, that in this work, the specification is over one method,
     nothing prevents another method in the nodule – or a sequence of methods for that matter – to
     break the necessity requirement that the door cannot be opened unless the card had access to the
     two keys.
        In contrast, our specification is holistic, and would not be concerned over whether the opening
     is effected through a call to a method open, or any other method from that module. However,
     the spec does assume that opening can only be effected through possession of a card with the
     appropriate electronic keys,
              A
         (∗∗) cd : Card, lk : Lock.{ ¬lk.isOpen ∧ (lk.dk ∈ {cd.ck1, cd.ck2} → ⟨ cd⟩⟩ ) }
        The implementation also satisfies the specification (∗∗∗) below, which says that regardless of
     the state of the lock, no card containing either of the the lock’s keys may be leaked:
                  A
         (∗∗∗) cd : Card, lk : Lock.{ lk.dk ∈ {cd.ck1, cd.ck2} → ⟨ cd⟩⟩ }
        Note, that while (∗∗∗) and (∗) share the part about (lk.dk ∈ {cd.ck1, cd.ck2} → ⟨ cd⟩⟩ )
     neither of the two is stronger than the other.

     F.7    Access through any element out of a set of Electronic Keys
     Another case study proposed in [5], is that access should only be granted through possession of
     any out of a set of keys.
 1   module Vault
 2         field keys: List< Object >
 3         field isOpen: boolean
 4
 5            private init(keys:List<Object>)
 6                ...
 7
 8            public open(key:Object) : bool


     , Vol. 1, No. 1, Article . Publication date: November 2025.
     Reasoning about External Calls – Extended Version                                                                           45


 9                    keysList := keys
10                    while keysList.notEmpty() do
11                            firstKey := keysList.top();
12                        if (firstKey == this.key) then
13                           isOpen:= true
14                            return true
15                        keysList.pop();
16                    return false
17


        The paper [5] is concerned with the verification of the body of open, and in particular the
     while-loop,. And so, they could prove that18 a call to v.open(k) returns true only if k is one
     of the keys of v:
        (∗) < v.keys.contains(k) > v.open(k) < ret == true >
     where v is a Vault and contains is assumed to be a method in List checking whether its
     argument is in the list.
        With our approach, we would use a standard, sufficient condition Hoare logic to obtain that
        (∗∗) {¬v.keys.contains(k) ∧ ¬v.isOpen }
                 l.open(k)
             { ¬v.keys.contains(k) ∧ ¬v.isOpen }
     The triple from (∗∗) together with the fact that open is the only public method would allow us to
     prove that if the vault is not open, and none of its keys are externally accessible, then it remains
     not open, and its keys remain externally in-accessible, i.e.
                 A
        (∗∗∗) v : Vault.{ ¬v.isOpen ∧ ∀k : Object.[ v.keys.contains(k) → ⟨ k⟩⟩ ] }
        The implementation also satisfies spec, (∗∗∗∗) below, which says that regardless of the state of
     the vault, none of its keys are leaked:
                  A
        (∗∗∗∗) v : Vault.{ ∀k : Object.[ v.keys.contains(k) → ⟨ k⟩⟩ ] }




     18 To be precise, their proof is only for the body of open because their logic lacks support function calls. However, that lack

     is not a severe limitation; function calls can be easily added.

                                                                        , Vol. 1, No. 1, Article . Publication date: November 2025.
46                                                  Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


G     Appendix to Section 6
G.1     Preliminaries: Specification Lookup, Renamings, Underlying Hoare Logic
                                                         txt
Definition G.1 is broken down as follows: 𝑆 1 ≤ 𝑆 2 says that 𝑆 1 is textually included in 𝑆 2 ; 𝑆 ∼ 𝑆 ′ says
that 𝑆 is a safe renaming of 𝑆 ′ ; ⊢ 𝑀 : 𝑆 says that 𝑆 is a safe renaming of one of the specifications
given for 𝑀.
                                              A
   In particular, a safe renaming of 𝑥 : 𝐶.{𝐴} can replace any of the variables 𝑥. A safe renaming of
{ 𝐴1 } 𝑝 𝐷 ::𝑚(𝑦 : 𝐷) { 𝐴2 } ∥ {𝐴3 } can replace the formal parameters (𝑦) by actual parameters (𝑦 ′ )
but requires the actual parameters not to include this, or res, (i.e. this, res ∉ 𝑦 ′ ). – Moreover,
it can replace the free variables which do not overlap with the formal parameters or the receiver (
𝑥 = 𝐹𝑣 (𝐴1 ) \ {𝑦, this}).
Definition G.1. For a module 𝑀 and a specification 𝑆, we define:
           txt               txt              txt               txt               txt
      • 𝑆 1 ≤ 𝑆 2 ≜ 𝑆 1 = 𝑆 2 , or 𝑆 2 = 𝑆 1 ∧ 𝑆 3 , or 𝑆 2 = 𝑆 3 ∧ 𝑆 1 , or 𝑆 2 = 𝑆 3 ∧ 𝑆 1 ∧ 𝑆 4 for some 𝑆 3 , 𝑆 4 .
      • 𝑆 ∼ 𝑆 ′ is defined by cases
          A                 A
        – 𝑥 : 𝐶.{𝐴} ∼ 𝑥 ′ : 𝐶.{𝐴′ [𝑥 ′ /𝑥]}
        – { 𝐴1 } 𝑝 𝐷 ::𝑚(𝑦 : 𝐷) { 𝐴2 } ∥ {𝐴3 } ∼ { 𝐴1′ } 𝑝 𝐷 ::𝑚(𝑦 ′ : 𝐷) { 𝐴2′ } ∥ {𝐴3′ }
                          ≜ 𝐴1 = 𝐴1′ [𝑦/𝑦 ′ ] [𝑥/𝑥 ′ ], 𝐴2 = 𝐴2′ [𝑦/𝑦 ′ ] [𝑥/𝑥 ′ ], 𝐴3 = 𝐴3′ [𝑦/𝑦 ′ ] [𝑥/𝑥 ′ ], ∧
                               this, res ∉ 𝑦 ′, 𝑥 = 𝐹𝑣 (𝐴1 ) \ {𝑦, this}
                                        txt
      •⊢ 𝑀 : 𝑆         ≜    ∃𝑆 ′ .[ 𝑆 ′ ≤ 𝒮𝑝𝑒𝑐 (𝑀) ∧ 𝑆 ′ ∼ 𝑆 ]
   The restriction on renamings of method specifications that the actual parameters should not to
include this or res is necessary because this and res denote different objects from the point
of the caller than from the point of the callee. It means that we are not able to verify a method call
whose actual parameters include this or res. This is not a serious restriction: we can encode any
such method call by preceding it with assignments to fresh local variables, this’:=this, and
res’:=res, and using this’ and res’ in the call.
Example G.2. The specification from Example 5.5 can be renamed as
           𝑆 9𝑟   ≜    { 𝑎1 : Account, 𝑎2 : Account ∧ ⟨ 𝑎1⟩⟩ ∧ ⟨ 𝑎2.key⟩⟩ }
                            public Account :: set(nKey : Key)
                       { ⟨ 𝑎1⟩⟩ ∧ ⟨ 𝑎2.key⟩⟩ } ∥ {⟨⟨𝑎1⟩⟩ ∧ ⟨ 𝑎2.key⟩⟩ }
Axiom G.3. Assume Hoare logic with judgements 𝑀 ⊢𝑢𝑙 {𝐴}𝑠𝑡𝑚𝑡 {𝐴′ }, with 𝑆𝑡𝑏𝑙 (𝐴), 𝑆𝑡𝑏𝑙 (𝐴′ ).

G.2     Types
The rules in Fig. 18 allow triples to talk about the types Rule types-1 promises that types of local
variables do not change. Rule types-2 generalizes types-1 to any statement, provided that there
already exists a triple for that statement.
                  types-1
                   𝑠𝑡𝑚𝑡 contains no method call                 𝑠𝑡𝑚𝑡 contains no assignment to 𝑥
                                                𝑀 ⊢ { 𝑥 : 𝐶 } 𝑠𝑡𝑚𝑡 { 𝑥 : 𝐶 }

                  types-2
                            𝑀 ⊢ { 𝐴 } 𝑠 { 𝐴′ } ∥ { 𝐴′′ }
                   𝑀 ⊢ { 𝑥 : 𝐶 ∧ 𝐴 } 𝑠 { 𝑥 : 𝐶 ∧ 𝐴′ } ∥ { 𝐴′′ }

                                                        Fig. 18. Types


, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                47


  In types-1 we restricted to statements which do not contain method calls in order to make lemma
G.5 valid.

G.3    Second Phase - more
in Fig. 19, we extend the Hoare Quadruples Logic with substructural rules, rules for conditionals,
case analysis, and a contradiction rule. For the conditionals we assume the obvious operational.
semantics, but do not define it in this paper

                                         [combine]                                               [seq]
               𝑀 ⊢ { 𝐴1 } 𝑠 { 𝐴2 } ∥ { 𝐴 }                          𝑀 ⊢ { 𝐴1 } 𝑠 1 { 𝐴2 } ∥ { 𝐴 }
               𝑀 ⊢ { 𝐴3 } 𝑠 { 𝐴4 } ∥ { 𝐴 }                          𝑀 ⊢ { 𝐴2 } 𝑠 2 { 𝐴3 } ∥ { 𝐴 }
            𝑀 ⊢ { 𝐴1 ∧ 𝐴3 } 𝑠 { 𝐴2 ∧ 𝐴4 } ∥ { 𝐴 }                  𝑀 ⊢ { 𝐴1 } 𝑠 1 ; 𝑠 2 { 𝐴3 } ∥ { 𝐴 }

                                                                      [conseq]
  𝑀 ⊢ { 𝐴4 } 𝑠 { 𝐴5 } ∥ { 𝐴6 }           𝑀 ⊢ 𝐴1 → 𝐴4           𝑀 ⊢ 𝐴5 → 𝐴2          𝑀 ⊢ 𝐴6 → 𝐴3
                                      𝑀 ⊢ { 𝐴1 } 𝑠 { 𝐴2 } ∥ { 𝐴3 }
                                                                       [If_Rule]
                                 𝑀 ⊢ { 𝐴 ∧ 𝐶𝑜𝑛𝑑 } 𝑠𝑡𝑚𝑡 1 { 𝐴′ } ∥ { 𝐴′′ }
                                𝑀 ⊢ { 𝐴 ∧ ¬𝐶𝑜𝑛𝑑 } 𝑠𝑡𝑚𝑡 2 { 𝐴′ } ∥ { 𝐴′′ }
                         𝑀 ⊢ { 𝐴 } if 𝐶𝑜𝑛𝑑 then 𝑠𝑡𝑚𝑡 1 else 𝑠𝑡𝑚𝑡 2 { 𝐴′ } ∥ { 𝐴′′ }

                                                                                                [Cases]
                                             [Absurd]
                                                                𝑀 ⊢ { 𝐴 ∧ 𝐴1 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }
                                                                𝑀 ⊢ { 𝐴 ∧ 𝐴2 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }
      𝑀 ⊢ { 𝑓 𝑎𝑙𝑠𝑒 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }
                                                              𝑀 ⊢ { 𝐴 ∧ (𝐴1 ∨ 𝐴2 ) } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }
                      Fig. 19. Hoare Quadruples - substructural rules, and conditionals


G.4    Extend the semantics and Hoare logic to accommodate scalars and conditionals
We extend the notion of protection to also allow it to apply to scalars.
Definition G.4 (Satisfaction of Assertions – Protected From). extending the definition of Def 4.4.
We use 𝛼 to range over addresses, 𝛽 to range over scalars, and 𝛾 to range over addresses or scalars.
We define 𝑀, 𝜎 |= ⟨𝛾⟩⟩←   ×− 𝛾𝑜 as:
  (1) 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩← ×− 𝛼𝑜 ≜
      • 𝛼 ≠ 𝛼 0 , and
      • ∀𝑛 ∈ N.∀𝑓1, ...𝑓𝑛 ..[ ⌊𝛼𝑜 .𝑓1 ...𝑓𝑛 ⌋ 𝜎 = 𝛼 =⇒ 𝑀, 𝜎 |= ⌊𝛼𝑜 .𝑓1 ...𝑓𝑛−1 ⌋ 𝜎 : 𝐶 ∧ 𝐶 ∈ 𝑀 ]
  (2) 𝑀, 𝜎 |= ⟨𝛾⟩⟩← ×− 𝛽𝑜 ≜ 𝑡𝑟𝑢𝑒
  (3) 𝑀, 𝜎 |= ⟨ 𝛽⟩⟩←×− 𝛼𝑜 ≜ 𝑓 𝑎𝑙𝑠𝑒
  (4) 𝑀, 𝜎 |= ⟨ e⟩⟩←
                   ×− e𝑜 ≜
      ∃𝛾, 𝛾𝑜 .[ 𝑀, 𝜎, e ↩→ 𝛾 ∧ 𝑀, 𝜎, e0 ↩→ 𝛾 0 ∧ 𝑀, 𝜎 |= ⟨𝛾⟩⟩←×− 𝛾𝑜 ]
   The definition from above gives rise to further cases of protection; we supplement the triples
from Fig. 6 with some further inference rules, given in Fig. 20. Namely, any expression e is protected
from a scalar (rules Prot-In, Prot-Bool and Prot-Str). Moreover, if starting at some e𝑜 and
following any sequence of fields 𝑓 we reach internal objects or scalars (i.e. never reach an external
object), then any e is protected from e𝑜 (rule Prot_Intl).
Lemma G.5. If 𝑀 ⊢ { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ }, then 𝑠𝑡𝑚𝑡 contains no method calls.

                                                         , Vol. 1, No. 1, Article . Publication date: November 2025.
48                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


      𝑀 ⊢ e𝑜 : int → ⟨ e⟩⟩←
                          ×− e𝑜          [Prot-Int]              𝑀 ⊢ e𝑜 : bool → ⟨ e⟩⟩←
                                                                                      ×− e𝑜      [Prot-Bool]

 𝑀 ⊢ e𝑜 : str → ⟨ e⟩⟩←
                     ×− e𝑜            [Prot-Str]                       ×− e𝑜 ∧ e : intl → e ≠ 𝑒 ′
                                                              𝑀 ⊢ ⟨ e⟩⟩←                              [Prot-Neq]

       𝑀 ⊢ 𝐴 → ∀𝑓 .[ e𝑜 .𝑓 : intl ∨ e𝑜 .𝑓 : int ∨ e𝑜 .𝑓 : bool ∨ e𝑜 .𝑓 : str ]
                                                                                                 [Prot-Intl]
                                        𝑀 ⊢ 𝐴 → ⟨ e⟩⟩←
                                                     ×− e𝑜

                                  Fig. 20. Protection for Scalar and Internal Types


     Proof. By induction on the rules in Fig. 6.
                                                                                                                   □

G.5     Adaptation
We now discuss the proof of Lemma 6.2.

Proof of lemma 6.2, part 1
To Show: 𝑆𝑡𝑏𝑙 ( 𝐴−▽(𝑦0, 𝑦) )
By structural induction on 𝐴.
End Proof



     For parts 2, 3, and 4, we first prove the following auxiliary lemma:
Auxiliary Lemma G.6. For all 𝛼, 𝜙 1 , 𝜙 2 , 𝜙 2 , 𝜙 and 𝜒
   (𝐿1) 𝑀, (𝜙 1, 𝜒) |= ⟨ 𝛼⟩⟩← ×− 𝑅𝑛𝑔(𝜙) =⇒ 𝑀, (𝜙 2 · 𝜙, 𝜒) |= ⟨ 𝛼⟩⟩
   (𝐿2) 𝑀, (𝜙 1 · 𝜙, 𝜒) |= ⟨ 𝛼⟩⟩ ∧ extl =⇒ 𝑀, (𝜙 2, 𝜒) |= ⟨ 𝛼⟩⟩←    ×− 𝑅𝑛𝑔(𝜙)
   (𝐿3) 𝑀, (𝜙 1 · 𝜙 1, 𝜒) |= ⟨ 𝛼⟩⟩ ∧ extl ∧ 𝑅𝑛𝑔(𝜙) ⊆ 𝑅𝑛𝑔(𝜙 1 ) =⇒ 𝑀, (𝜙 2, 𝜒) |= ⟨ 𝛼⟩⟩←
                                                                                      ×− 𝑅𝑛𝑔(𝜙)


 Proof.
We first prove (L1):

We define 𝜎1 ≜ (𝜙 1, 𝜒), and 𝜎2 ≜ (𝜙 2 · 𝜙, 𝜒).
The above definitions imply that:
  (1) ∀𝛼 ′, ∀𝑓 .[ ⌊𝛼 ′ .𝑓 ⌋ 𝜎1 = ⌊𝛼 ′ .𝑓 ⌋ 𝜎2 ]
  (2) ∀𝛼 ′ .[ 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎1 ) = 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎2 ) ]
  (3) 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎2 ) = 𝛼 ′ ∈𝑅𝑛𝑔 (𝜙 ) 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎2 ).
                            Ð
We now assume that
  (4) 𝑀, 𝜎1 |= ⟨ 𝛼⟩⟩←   ×− 𝑅𝑛𝑔(𝜙).
and want to show that
  (A?) 𝑀, 𝜎2 |= ⟨ 𝛼⟩⟩
From (4) and by definitions, we obtain that
  (5) ∀𝛼 ′ ∈ 𝑅𝑛𝑔(𝜙).∀𝛼 ′′ ∈ 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎1 ).∀𝑓 .[ 𝑀, 𝜎1 |= 𝛼 ′′ : extl → 𝛼 ′′ .𝑓 ≠ 𝛼 ],             and also
  (6) 𝛼 ∉ 𝑅𝑛𝑔(𝜙)
From (5) and (3) we obtain:
  (7) ∀𝛼 ′ ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎2 ).∀𝑓 .[ 𝑀, 𝜎1 |= 𝛼 ′ : extl → 𝛼 ′ .𝑓 ≠ 𝛼 ]

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                               49


From (7) and (1) and (2) we obtain:
  (8) ∀𝛼 ′ ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎2 ).∀𝑓 .[ 𝑀, 𝜎2 |= 𝛼 ′ : extl → 𝛼 ′ .𝑓 ≠ 𝛼 ]
From (8), by definitions, we obtain
  (10) 𝑀, 𝜎2 |= ⟨ 𝛼⟩⟩
which is (A?).
This completes the proof of (L1).

We now prove (L2):

We define 𝜎1 ≜ (𝜙 1 · 𝜙, 𝜒), and 𝜎2 ≜ (𝜙 2, 𝜒).
The above definitions imply that:
  (1) ∀𝛼 ′, ∀𝑓 .[ ⌊𝛼 ′ .𝑓 ⌋ 𝜎1 = ⌊𝛼 ′ .𝑓 ⌋ 𝜎2 ]
  (2) ∀𝛼 ′ .[ 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎1 ) = 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎2 ) ]
  (3) 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎1 ) = 𝛼 ′ ∈𝑅𝑛𝑔 (𝜙 ) 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎1 ).
                            Ð
We assume that
  (4) 𝑀, 𝜎1 |= ⟨ 𝛼⟩⟩ ∧ extl.
and want to show that
  (A?) 𝑀, 𝜎2 |= 𝐴−▽𝑅𝑛𝑔(𝜙).
From (4), and unfolding the definitions, we obtain:
  (5) ∀𝛼 ′ ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎1 ).∀𝑓 .[ 𝑀, 𝜎1 |= 𝛼 ′ : extl → 𝛼 ′ .𝑓 ≠ 𝛼 ], and
  (6) ∀𝛼 ′ ∈ 𝑅𝑛𝑔(𝜙).[ 𝛼 ′ ≠ 𝛼 ].
From(5), and using (3) and (2) we obtain:
  (7) ∀𝛼 ′ ∈ 𝑅𝑛𝑔(𝜙).∀𝛼 ′′ ∈ 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎2 ).∀𝑓 .[ 𝑀, 𝜎2 |= 𝛼 ′′ : extl → 𝛼 ′′ .𝑓 ≠ 𝛼 ]
From (5) and (7) and by definitions, we obtain
  (8) ∀𝛼 ′ ∈ 𝑅𝑛𝑔(𝜙).[ |= 𝛼 ⟨ 𝛼⟩⟩←      ×− 𝛼 ′ ].
From (8) and definitions we obtain (A?).
This completes the proof of (L2).

We now prove (L3):

We define 𝜎1 ≜ (𝜙 1 · 𝜙 1, 𝜒), and 𝜎2 ≜ (𝜙 2, 𝜒).
The above definitions imply that:
  (1) ∀𝛼 ′, ∀𝑓 .[ ⌊𝛼 ′ .𝑓 ⌋ 𝜎1 = ⌊𝛼 ′ .𝑓 ⌋ 𝜎2 ]
  (2) ∀𝛼 ′ .[ 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎1 ) = 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎2 ) ]
  (3) 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎1 ) = 𝛼 ′ ∈𝑅𝑛𝑔 (𝜙 1 ) 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎1 ).
                            Ð
We assume that
  (4a) 𝑀, 𝜎1 |= ⟨ 𝛼⟩⟩ ∧ extl, and (4b) 𝑅𝑛𝑔(𝜙) ⊆ 𝑅𝑛𝑔(𝜙 1 )
We want to show that
  (A?) 𝑀, 𝜎2 |= 𝐴−▽𝑅𝑛𝑔(𝜙).
From (4a), and unfolding the definitions, we obtain:
  (5) ∀𝛼 ′ ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎1 ).∀𝑓 .[ 𝑀, 𝜎1 |= 𝛼 ′ : extl → 𝛼 ′ .𝑓 ≠ 𝛼 ], and
  (6) ∀𝛼 ′ ∈ 𝑅𝑛𝑔(𝜙 1 ).[ 𝛼 ′ ≠ 𝛼 ].
From(5), and (3) and (2) and (4b) we obtain:
  (7) ∀𝛼 ′ ∈ 𝑅𝑛𝑔(𝜙).∀𝛼 ′′ ∈ 𝑅𝑐ℎ𝑏𝑙 (𝛼 ′, 𝜎2 ).∀𝑓 .[ 𝑀, 𝜎2 |= 𝛼 ′′ : extl → 𝛼 ′′ .𝑓 ≠ 𝛼 ]
From(6), and (4b) we obtain:
  (8) ∀𝛼 ′ ∈ 𝑅𝑛𝑔(𝜙 1 ).[ 𝛼 ′ ≠ 𝛼 ].


                                                        , Vol. 1, No. 1, Article . Publication date: November 2025.
50                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


From (8) and definitions we obtain (A?).
This completes the proof of (L3).
                                                                                                                   □
Proof of lemma 6.2, part 2
To Show: (∗) 𝑀, 𝜎 |= 𝐴−▽𝑅𝑛𝑔(𝜙)                        =⇒      𝑀, 𝜎 ▽ 𝜙 |= 𝐴

By induction on the structure of 𝐴. For the case where 𝐴 has the form ⟨ 𝛼 .𝑓 ⟩ , we use lemma
G.6,(L1), taking 𝜙 1 = 𝜙 2 , and 𝜎 ≜ (𝜙 1, 𝜒).
End Proof



Proof of lemma 6.2, part 3
To Show (∗) 𝑀, 𝜎 ▽ 𝜙 |= 𝐴 ∧ extl                     =⇒       𝑀, 𝜎 |= 𝐴−▽𝑅𝑛𝑔(𝜙)

We apply induction on the structure of 𝐴. For the case where 𝐴 has the form ⟨ 𝛼 .𝑓 ⟩ , we apply lemma
G.6,(L2), using 𝜙 1 = 𝜙 2 , and 𝜎 ≜ (𝜙 1, 𝜒).
End Proof



Proof of lemma 6.2, part 4
To Show: (*) 𝑀, 𝜎 |= 𝐴 ∧ extl ∧ 𝑀 · 𝑀 |= 𝜎 ▽ 𝜙                       =⇒       𝑀, 𝜎 ▽ 𝜙 |= 𝐴−▽𝑅𝑛𝑔(𝜙)

By induction on the structure of 𝐴. For the case where 𝐴 has the form ⟨ 𝛼 .𝑓 ⟩ , we want to ap-
ply lemma G.6,(L3). We take 𝜎 to be (𝜙 1 · 𝜙 1, 𝜒), and 𝜙 2 = 𝜙 1 · 𝜙 1 · 𝜙. Moreover, 𝑀 · 𝑀 |= 𝜎 ▽ 𝜙 gives
that 𝑅𝑛𝑔(𝜙) ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎2 ). Therefore, (*) follows by application of lemma G.6,(L3).
End Proof




, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                  51


H     Appendix to Section 7 – Soundness of the Hoare Logics
H.1    Expectations
Axiom H.1. We require a sound logic of assertions (𝑀 ⊢ 𝐴), and a sound Hoare logic , i.e. that for
all 𝑀, 𝐴, 𝐴′ , 𝑠𝑡𝑚𝑡:
                              𝑀 ⊢ 𝐴 =⇒ ∀𝜎.[ 𝑀, 𝜎 |= 𝐴 ].
                     𝑀 ⊢𝑢𝑙 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } =⇒ 𝑀 |= { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ }
   The expectation that 𝑀 ⊢𝑢𝑙 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } is sound is not onerous: since the assertions 𝐴 and
 ′
𝐴 do not talk about protection, many Hoare logics from the literature could be taken.
  On the other hand, in the logic 𝑀 ⊢ 𝐴 we want to allow the assertion 𝐴 to talk about protection.
Since protection is a novel concept, the literature offers no such logics. Nevertheless, such a logic
can be constructed by extending and underlying assertion logic 𝑀 ⊢𝑢𝑙 𝐴 which does not talk about
protection. We show such an extension in Fig 21.

                                                                     [Ext-1]
                                                    𝑀 ⊢𝑢𝑙 𝐴
                                                    𝑀 ⊢𝑢𝑙 𝐴

                                        [Ext-2]                                              [Ext-3]
                     𝑀 ⊢ 𝐴 → 𝐴′                                          𝑀 ⊢ 𝐴 → 𝐴′
       𝑀 ⊢ (𝐴 ∧ ⟨ e⟩⟩←×− e′ ) → (𝐴′ ∧ ⟨ e⟩⟩←
                                           ×− e′ )                𝑀 ⊢ (𝐴 ∧ ⟨ e⟩⟩ ) → (𝐴′ ∧ ⟨ e⟩⟩ )

                                                                     [Ext-4]

                                       ×− e′ )) ↔ ((𝐴1 ∧ ⟨ e⟩⟩←
                𝑀 ⊢ ((𝐴1 ∨ 𝐴2 ) ∧ ⟨ e⟩⟩←                      ×− e′ ) ∨ (𝐴2 ∧ ⟨ e⟩⟩←
                                                                                   ×− e′ ))

                                                                     [Ext-5]

                          𝑀 ⊢ ((𝐴1 ∨ 𝐴2 ) ∧ ⟨ e⟩⟩ ) ↔ ((𝐴1 ∧ ⟨ e⟩⟩ ) ∨ (𝐴2 ∧ ⟨ e⟩⟩ ))

                                        Fig. 21. From 𝑀 ⊢𝑢𝑙 𝐴 to 𝑀 ⊢ 𝐴

The extension shown in in Fig. 21 preserves soundness of the logic:
Lemma H.2. Assume a logic ⊢𝑢𝑙 , such that
                                𝑀 ⊢𝑢𝑙 𝐴 =⇒ ∀𝜎.[ 𝑀, 𝜎 |= 𝐴 ].
Extend this logic according to the rules in Fig. 21 and in Fig 20, and obtain 𝑀 ⊢ 𝐴. Then, we have:
                                 𝑀 ⊢ 𝐴 =⇒ ∀𝜎.[ 𝑀, 𝜎 |= 𝐴 ].
    Proof. By induction over the derivation that 𝑀 ⊢ 𝐴.                                                            □
   Note that the rules in in Fig. 21 allow the derivation of 𝑀 ⊢ 𝐴, for which 𝑆𝑡𝑏 + (𝐴) does not hold –
e.g. we can derive 𝑀 ⊢ ⟨ e⟩⟩ → ⟨ e⟩⟩ through application of rule Ext-3. However, this does not affect
soundness of our logic – 𝑆𝑡𝑏 + (_) is required only in specifications.

H.2    Deep satisfaction of assertions
Definition H.3. For a state 𝜎, and a number 𝑖 ∈ N with 𝑖 ≤ |𝜎 |, module 𝑀, and assertions 𝐴, 𝐴′
we define:

                                                           , Vol. 1, No. 1, Article . Publication date: November 2025.
52                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


      • 𝑀, 𝜎, 𝑘 |= 𝐴     ≜     𝑘 ≤ |𝜎 | ∧ ∀𝑖 ∈ [𝑘...|𝜎 |].[ 𝑀, 𝜎 [𝑖] |= 𝐴[⌊𝑧⌋ 𝜎 /𝑧] ] where 𝑧 = 𝐹𝑣 (𝐴).
   Remember the definition of 𝜎 [𝑘], which returns a new state whose top frame is the 𝑘-th frame
from 𝜎. Namely, (𝜙 1 ...𝜙𝑖 ...𝜙𝑛 , 𝜒) [𝑖] ≜ (𝜙 1 ...𝜙𝑖 , 𝜒)
Lemma H.4. For a states 𝜎, 𝜎 ′ , numbers 𝑘, 𝑘 ′ ∈ N, assertions 𝐴, 𝐴′ , frame 𝜙 and variables 𝑧, 𝑢:
     (1) 𝑀, 𝜎, |𝜎 | |= 𝐴 ⇐⇒ 𝑀, 𝜎 |= 𝐴
     (2) 𝑀, 𝜎, 𝑘 |= 𝐴 ∧ 𝑘 ≤ 𝑘 ′ =⇒ 𝑀, 𝜎, 𝑘 ′ |= 𝐴
     (3) 𝑀, 𝜎 |= 𝐴 ∧ 𝑆𝑡𝑏𝑙 (𝐴) =⇒ ∀𝑘 ≤ |𝜎 |.[ 𝑀, 𝜎, 𝑘 |= 𝐴 ]
     (4) 𝑀 |= 𝐴 → 𝐴′ =⇒ ∀𝜎.∀𝑘 ≤ |𝜎 |.[ 𝑀, 𝜎, 𝑘 |= 𝐴 =⇒ 𝑀, 𝜎, 𝑘 |= 𝐴′ ]
Proof Sketch
     (1) By unfolding and folding the definitions.
     (2) By unfolding and folding the definitions.
     (3) By induction on the definition of 𝑆𝑡𝑏𝑙 (_).
     (4) By contradiction: Assume that there exists a 𝜎, and a 𝑘 ≤ |𝜎 |, such that
                         𝑀, 𝜎, 𝑘 |= 𝐴 and ¬(𝑀, 𝜎, 𝑘 |= 𝐴′ )
         The above implies that
                         ∀𝑖 ≥ 𝑘.[ 𝑀, 𝜎 [𝑖] |= 𝐴[⌊𝑧⌋ 𝜎 /𝑧] ], and
                         ∃𝑗 ≥ 𝑘.[ 𝑀, 𝜎 [ 𝑗] ̸ |= 𝐴′ [⌊𝑧⌋ 𝜎 /𝑧] ],
         where 𝑧 ≜ 𝐹𝑣 (𝐴) ∪ 𝐹𝑣 (𝐴′ ).
         Take 𝜎 ′′ ≜ 𝜎 [ 𝑗]. Then we have that
                         𝑀, 𝜎 ′′ |= 𝐴[⌊𝑧⌋ 𝜎 /𝑧], and 𝑀, 𝜎 ′′ ̸ |= 𝐴′ [⌊𝑧⌋ 𝜎 /𝑧].
         This contradicts 𝑀 |= 𝐴 → 𝐴′ .

End Proof Sketch
  Finally, the following lemma allows us to combine shallow and Deep satisfaction:
Lemma H.5. For states 𝜎, 𝜎 ′ , frame 𝜙 such that 𝜎 ′ = 𝜎 ▽ 𝜙, and for assertion 𝐴, such that 𝑓 𝑣 (𝐴) = ∅:
      • 𝑀, 𝜎, 𝑘 |= 𝐴 ∧ 𝑀, 𝜎 ′ |= 𝐴         ⇐⇒        𝑀, 𝜎 ′, 𝑘 |= 𝐴
  Proof. By structural induction on 𝐴, and unfolding/folding the definitions. Using also lemma
H.19 from later.                                                                             □

H.3     Shallow and Deep Semantics of Hoare tuples
Another example demonstrating that assertions at the end of a method execution might not hold
after the call:
Example H.6 (𝑆𝑡𝑏 + not always preserved by Method Return). Assume state 𝜎𝑎 , such that ⌊this⌋ 𝜎𝑎 =
𝑜 1 , ⌊this.𝑓 ⌋ 𝜎 = 𝑜 2 , ⌊𝑥⌋ 𝜎 = 𝑜 3 , ⌊𝑥 .𝑓 ⌋ 𝜎 = 𝑜 2 , and ⌊𝑥 .𝑔⌋ 𝜎 = 𝑜 4 , where 𝑜 2 is external and all other
objects are internal. We then have .., 𝜎𝑎 |= ⟨𝑜 4 ⟩ . Assume the continuation of 𝜎𝑎 consists of a method
𝑥 .𝑚(). Then, upon entry to that method, when we push the new frame, we have state 𝜎𝑏 , which also
satisfies .., 𝜎𝑏 |= ⟨𝑜 4 ⟩ . Assume the body of 𝑚 is this.𝑓 .𝑚1(this.𝑔); this.𝑓 := this; this.𝑔 :=
this, and the external method 𝑚1 stores in the receiver a reference to the argument. Then, at
the end of method execution, and before popping the stack, we have state 𝜎𝑐 , which also satisfies
.., 𝜎𝑐 |= ⟨𝑜 4 ⟩ . However, after we pop the stack, we obtain 𝜎𝑑 , for which .., 𝜎𝑑 ̸ |= ⟨𝑜 4 ⟩ .
Definition H.7 (Deep Satisfaction of Quadruples by States). For modules 𝑀, 𝑀, state 𝜎, and
assertions 𝐴, 𝐴′ and 𝐴′′

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                              53


      • 𝑀; 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝐴′′ } ≜
           ∀𝑘, 𝑧, 𝜎 ′, 𝜎 ′′ .[𝑀, 𝜎, 𝑘 |= 𝐴 =⇒
                                            [ 𝑀 ·𝑀; 𝜎⇝∗fin 𝜎 ′ ⇒ 𝑀, 𝜎 ′, 𝑘 |= 𝐴′ ] ∧
                                            [ 𝑀 ·𝑀; 𝜎⇝∗𝜎 ′′ ⇒ 𝑀, 𝜎 ′′, 𝑘 |= (extl → 𝐴′′ [⌊𝑧⌋ 𝜎 /𝑧]) ]
                               ]
                               where 𝑧 = 𝐹𝑣 (𝐴)
Lemma H.8. For all 𝑀, 𝑀 𝐴, 𝐴′ , 𝐴′′ and 𝜎:
   • 𝑀; 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝐴′′ } =⇒ 𝑀; 𝑀 |= { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝐴′′ }
   We define the meaning of our Hoare triples, { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ }, in the usual way, i.e. that execution
of 𝑠𝑡𝑚𝑡 in a state that satisfies 𝐴 leads to a state which satisfies 𝐴′ . In addition to that, Hoare
quadruples, { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }, promise that any external future states scoped by 𝜎 will
satisfy 𝐴′′ . We give both a weak and a shallow version of the semantics
Definition H.9 (Deep Semantics of Hoare triples). For modules 𝑀, and assertions 𝐴, 𝐴′ we define:
   • 𝑀 |= { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ≜
       ∀𝑀.∀𝜎.[ 𝜎.cont = 𝑠𝑡𝑚𝑡 =⇒ 𝑀; 𝑀 |= { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝑡𝑟𝑢𝑒 } ]
                           txt

   • 𝑀 |= { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ } ≜
       ∀𝑀.∀𝜎.[ 𝜎.cont = 𝑠𝑡𝑚𝑡 =⇒ 𝑀; 𝑀 |= { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝐴′′ } ]
                           txt

   • 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ≜
         ∀𝑀.∀𝜎.[ 𝜎.cont = 𝑠𝑡𝑚𝑡 =⇒ 𝑀; 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝑡𝑟𝑢𝑒 } ]
                              txt

      • 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ } ≜
          ∀𝑀.∀𝜎.[ 𝜎.cont = 𝑠𝑡𝑚𝑡 =⇒ 𝑀; 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝜎 { 𝐴′ } ∥ { 𝐴′′ } ]
                              txt


Lemma H.10 (Deep vs Shallow Semantics of Quadruples). For all 𝑀, 𝐴, 𝐴′ , and 𝑠𝑡𝑚𝑡:
   • 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ } =⇒ 𝑀 |= { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }
  Proof. By unfolding and folding the definitions                                                              □

H.4     Deep satisfaction of specifications
We now give a Deep meaning to specifications:
Definition H.11 (Deep Semantics of Specifications). We define 𝑀 |=𝑑𝑒𝑒𝑝 𝑆 by cases:
                A
  (1) 𝑀 |=𝑑𝑒𝑒𝑝 𝑥 : 𝐶.{𝐴} ≜ ∀𝜎.[ 𝑀 |=𝑑𝑒𝑒𝑝 { extl ∧ 𝑥 : 𝐶 ∧ 𝐴 } 𝜎 { 𝐴 } ∥ { 𝐴 } ]
  (2) 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴1 } 𝑝 𝐷 ::𝑚(𝑦 : 𝐷) { 𝐴2 } ∥ {𝐴3 } ≜
               ∀𝑦0, 𝑦, 𝜎 [ 𝜎cont = 𝑢 := 𝑦0 .𝑚(𝑦1, ..𝑦𝑛 ) =⇒ 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴1′ } 𝜎 { 𝐴2′ } ∥ { 𝐴3′ } ]
                                      txt


               where
                𝐴1′ ≜ 𝑦0 : 𝐷, 𝑦 : 𝐷 ∧ 𝐴[𝑦0 /this], 𝐴2′ ≜ 𝐴2 [𝑢/𝑟𝑒𝑠, 𝑦0 /this], 𝐴3′ ≜ 𝐴3 [𝑦0 /this]
  (3) 𝑀 |=𝑑𝑒𝑒𝑝 𝑆 ∧ 𝑆 ′     ≜ 𝑀 |=𝑑𝑒𝑒𝑝 𝑆 ∧ 𝑀 |=𝑑𝑒𝑒𝑝 𝑆 ′
Lemma H.12 (Deep vs Shallow Semantics of Quadruples). For all 𝑀, 𝑆:
   • 𝑀 |=𝑑𝑒𝑒𝑝 𝑆 =⇒ 𝑀 |= 𝑆

H.5     Soundness of the Hoare Triples Logic
Auxiliary Lemma H.13. For any module 𝑀, assertions 𝐴, 𝐴′ and 𝐴′′ , such that 𝑆𝑡𝑏 + (𝐴), and
𝑆𝑡𝑏 + (𝐴′ ), and a statement 𝑠𝑡𝑚𝑡 which does not contain any method calls:
                   𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } =⇒ 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥ { 𝐴′′ }
  Proof.                                                                                                       □

                                                       , Vol. 1, No. 1, Article . Publication date: November 2025.
54                                                 Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


H.5.1     Lemmas about protection.
Definition H.14. 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎, 𝑘)               ≜     {𝛼 | ∃𝑖.[ 𝑘 ≤ 𝑖 ≤ |𝜎 | ∧ 𝛼 ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 [𝑖]) ]
   Lemma H.15 guarantees that program execution reduces the locally reachable objects, unless it
allocates new ones. That is, any objects locally reachable in the 𝑘-th frame of the new state (𝜎 ′ ),
are either new, or were locally reachable in the 𝑘-th frame of the previous state (𝜎).
Lemma H.15. For all 𝜎, 𝜎 ′ , and 𝛼, where |= 𝜎, and where 𝑘 ≤ |𝜎 |:
   • 𝑀 · 𝑀; 𝜎 ⇝ 𝜎 ′ =⇒ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 ′, 𝑘) ∩ 𝜎 ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎, 𝑘)
   • 𝑀 · 𝑀; 𝜎⇝∗𝜎 ′ =⇒ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 ′, 𝑘) ∩ 𝜎 ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎, 𝑘)
     Proof.
      • If the step is a method call, then the assertion follows by construction. If the steps is a local
        execution in a method, we proceed by case analysis. If it is an assignment to a local variable,
        then ∀𝑘.[ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 ′, 𝑘) = 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎, 𝑘) ]. If the step is the creation of a new object, then
        the assertion holds by construction. If it it is a field assignment, say, 𝜎 ′ = 𝜎 [𝛼 1, 𝑓 ↦→ 𝛼 2 ],
        then we have that 𝛼 1, 𝛼 2 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎, |𝜎 |). And therefore, by Lemma B.3, we also have that
        𝛼 1, 𝛼 2 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎, 𝑘) All locally reachable objects in 𝜎 ′ were either already reachable in 𝜎 or
        reachable through 𝛼 2 , Therefore, we also have that 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 ′, 𝑘) ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎, 𝑘) And
        by definition of _; _ ⇝ _, it is not a method return.
      • By induction on the number of steps in 𝑀 ·𝑀; 𝜎⇝∗𝜎 ′ . For the steps that correspond to method
        calls, the assertion follows by construction. For the steps that correspond to local execution
        in a method, the assertion follows from the bullet above. For the steps that correspond to
        method returns, the assertion follows by lemma B.3.
                                                                                                         □
  Lemma H.16 guarantees that any change to the contents of an external object can only happen
during execution of an external method.
Lemma H.16. For all 𝜎, 𝜎 ′ :
   • 𝑀 · 𝑀; 𝜎 ⇝ 𝜎 ′ ∧ 𝜎 |= 𝛼 : extl ∧ ⌊𝛼 .𝑓 ⌋ 𝜎 ≠ ⌊𝛼 .𝑓 ⌋ 𝜎 ′ =⇒ 𝑀, 𝜎 |= extl
     Proof. Through inspection of the operational semantics in Fig. 5, and in particular rule Write.
                                                                                                  □
  Lemma H.17 guarantees that internal code which does not include method calls preserves absolute
protection. It is used in the proof of soundness of the inference rule Prot-1.
Lemma H.17. For all 𝜎, 𝜎 ′ , and 𝛼:
   • 𝑀, 𝜎, 𝑘 |= ⟨ 𝛼⟩⟩ ∧ 𝑀, 𝜎 |= intl ∧ 𝜎.cont contains no method calls ∧ 𝑀 · 𝑀; 𝜎 ⇝ 𝜎 ′ =⇒
     𝑀, 𝜎 ′, 𝑘 |= ⟨ 𝛼⟩⟩
   • 𝑀, 𝜎, 𝑘 |= ⟨ 𝛼⟩⟩ ∧ 𝑀, 𝜎 |= intl ∧ 𝜎.cont contains no method calls ∧ 𝑀 · 𝑀; 𝜎⇝∗𝜎 ′ =⇒
     𝑀, 𝜎 ′, 𝑘 |= ⟨ 𝛼⟩⟩
     Proof.
      • Because 𝜎.cont contains no method calls, we also have that |𝜎 ′ | = |𝜎 |. Let us take 𝑚 = |𝜎 |.
        We continue by contradiction. Assume that 𝑀, 𝜎, 𝑘 |= ⟨ 𝛼⟩⟩ and 𝑀, 𝜎, 𝑘 ̸ |= ⟨ 𝛼⟩⟩
        Then:
        (*) ∀𝑓 .∀𝑖 ∈ [𝑘..𝑚].∀𝛼𝑜 ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎, 𝑖).[ 𝑀, 𝜎 |= 𝛼𝑜 : extl ⇒ ⌊𝛼𝑜 .𝑓 ⌋ 𝜎 ≠ 𝛼 ∧ 𝛼𝑜 ≠ 𝛼 ].
        (**) ∃𝑓 .∃𝑗 ∈ [𝑘..𝑚].∃𝛼𝑜 ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 ′, 𝑗).[ 𝑀, 𝜎 ′ |= 𝛼𝑜 : extl ∧ ⌊𝛼𝑜 .𝑓 ⌋ 𝜎 ′ = 𝛼 ∨ 𝛼𝑜 = 𝛼 ]
        We proceed by cases

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                 55


         1st Case 𝛼𝑜 ∉ 𝜎, i.e. 𝛼𝑜 is a new object. Then, by our operational semantics, it cannot have a
          field pointing to an already existing object (𝛼), nor can it be equal with 𝛼. Contradiction.
         2nd Case 𝛼𝑜 ∈ 𝜎. Then, by Lemma H.15, we obtain that 𝛼𝑜 ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎, 𝑗). Therefore,
          using (*), we obtain that ⌊𝛼𝑜 .𝑓 ⌋ 𝜎 ≠ 𝛼, and therefore ⌊𝛼𝑜 .𝑓 ⌋ 𝜎 ≠ ⌊𝛼𝑜 .𝑓 ⌋ 𝜎 ′ . By lemma H.16,
          we obtain 𝑀, 𝜎 |= extl. Contradiction!
      • By induction on the number of steps, and using the bullet above.
                                                                                                          □
Lemma H.18. For all 𝜎, 𝜎 ′ , and 𝛼:
                  ×− 𝛼𝑜 ∧ 𝜎.heap = 𝜎 ′ .heap =⇒ 𝑀, 𝜎 ′ |= ⟨ 𝛼⟩⟩←
   • 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←                                            ×− 𝛼𝑜
  Proof. By unfolding and folding the definitions.                                                                □
Lemma H.19. For all 𝜎, and 𝛼, 𝛼𝑜 , 𝛼 1 , 𝛼 2 :
   • 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←
                  ×− 𝛼𝑜 ∧ 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←  ×− 𝛼 1 =⇒ 𝑀, 𝜎 [𝛼 2, 𝑓 ↦→ 𝛼 1 ] |= ⟨ 𝛼⟩⟩←
                                                                                  ×− 𝛼𝑜
Definition H.20.           • 𝑀, 𝜎 |= e : intl* ≜ ∀𝑓 .[ 𝑀, 𝜎 |= e.𝑓 : intl ]
Lemma H.21. For all 𝜎, and 𝛼𝑜 and 𝛼:
   • 𝑀, 𝜎 |= 𝛼𝑜 : intl* =⇒ 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←
                                        ×− 𝛼𝑜
Proof Sketch Theorem 7.2 The proof goes by case analysis over the rules from Fig. 6 applied to
obtain 𝑀 ⊢ {𝐴} 𝑠𝑡𝑚𝑡 {𝐴′ }:
embed_ul By soundness of the underlying Hoare logic (axiom H.1), we obtain that 𝑀 |= { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ }.
      By axiom G.3 we also obtain that 𝑆𝑡𝑏𝑙 (𝐴) and 𝑆𝑡𝑏𝑙 (𝐴′ ). This, together with Lemma H.4, part
      3, gives us that 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ }. By the assumption of extend, 𝑠𝑡𝑚𝑡 does not contain
      any method call. Rest follows by lemma H.13.
Prot-New By operational semantics, no field of another object will point to 𝑢, and therefore 𝑢 is
      protected, and protected from all variables 𝑥.
Prot-1 by Lemma H.17. The rule premise 𝑀 ⊢ { 𝑧 = 𝑒 } 𝑠𝑡𝑚𝑡 { 𝑧 = 𝑒 } allows us to consider
      addresses, 𝛼, rather than expressions, 𝑒.
Prot-2 by Lemma H.18. The rule premise 𝑀 ⊢ { 𝑧 = 𝑒 ∧ 𝑧 = 𝑒 ′ } 𝑠𝑡𝑚𝑡 { 𝑧 = 𝑒 ∧ 𝑧 = 𝑒 ′ } allows
      us to consider addresses 𝛼, 𝛼 ′ rather than expressions 𝑒, 𝑒 ′ .
Prot-3 also by Lemma H.18. Namely, the rule does not change, and 𝑦.𝑓 in the old state has the
      same value as 𝑥 in the new state.
Prot-4 by Lemma H.19.
types-1 Follows from type system, the assumption of types-1 and lemma H.13.
 End Proof Sketch

H.6     Well-founded ordering
Definition H.22. For a module 𝑀, and modules 𝑀, we define a measure, [ 𝐴, 𝜎, 𝐴′, 𝐴′′ ] 𝑀,𝑀 , and
based on it, a well founded ordering (𝐴1, 𝜎1, 𝐴2, 𝐴3 ) ≪𝑀,𝑀 (𝐴4, 𝜎2, 𝐴5, 𝐴6 ) as follows:
   • [ 𝐴, 𝜎, 𝐴′, 𝐴′′ ] 𝑀,𝑀 ≜ (𝑚, 𝑛), where
     – 𝑚 is the minimal number of execution steps so that 𝑀 · 𝑀; 𝜎⇝∗fin 𝜎 ′ for some 𝜎 ′ , and ∞
       otherwise.
     – 𝑛 is minimal depth of all proofs of 𝑀 ⊢ { 𝐴 } 𝜎.cont{ 𝐴′ } ∥ { 𝐴′′ }.
   • (𝑚, 𝑛) ≪ (𝑚 ′, 𝑛 ′ ) ≜ 𝑚 < 𝑚 ′ ∨ (𝑚 = 𝑚 ′ ∧ 𝑛 < 𝑛 ′ ).
   • (𝐴1, 𝜎1, 𝐴2, 𝐴3 ) ≪𝑀,𝑀 (𝐴4, 𝜎2, 𝐴5, 𝐴6 ) ≜ [ 𝐴1, 𝜎1, 𝐴2, 𝐴3 ] 𝑀,𝑀 ≪ [ 𝐴4, 𝜎2, 𝐴5 .𝐴6 ] 𝑀,𝑀

                                                          , Vol. 1, No. 1, Article . Publication date: November 2025.
56                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


Lemma H.23. For any modules 𝑀 and 𝑀, the relation _ ≪𝑀,𝑀 _ is well-founded.

H.7     Public States, properties of executions consisting of several steps
We t define a state to be public, if the currently executing method is public.
Definition H.24. We use the form 𝑀, 𝜎 |= pub to express that the currently executing method is
public.19 Note that pub is not part of the assertion language.
Auxiliary Lemma H.25 (Enclosed Terminating Executions). For modules 𝑀, states 𝜎, 𝜎 ′ , 𝜎1 :
      • 𝑀; 𝜎⇝∗fin 𝜎 ′ ∧ 𝑀; 𝜎⇝∗𝜎1              =⇒      ∃𝜎2 .[ 𝑀; 𝜎1 ⇝∗fin 𝜎2 ∧ (𝑀, 𝜎); 𝜎2 ⇝∗𝜎 ′ ]

Auxiliary Lemma H.26 (Executing sequences). For modules 𝑀, statements 𝑠 1 , 𝑠 2 , states 𝜎, 𝜎 ′ ,
𝜎 ′′′ :
       • 𝜎.cont = 𝑠 1 ; 𝑠 2 ∧ 𝑀; 𝜎⇝∗fin 𝜎 ′ ∧ 𝑀; 𝜎⇝∗𝜎 ′′
         =⇒
         ∃𝜎 ′′ .[ 𝑀; 𝜎 [cont ↦→ 𝑠 1 ]⇝∗fin 𝜎 ′′ ∧ 𝑀; 𝜎 ′′ [cont ↦→ 𝑠 2 ]⇝∗fin 𝜎 ′ ∧
                  [ 𝑀; 𝜎 [cont ↦→ 𝑠 1 ]⇝∗𝜎 ′′ ∨ 𝑀; 𝜎 ′′ [cont ↦→ 𝑠 2 ]⇝∗fin 𝜎 ′′′ ] ]

H.8     Summarised Executions
We repeat the two diagrams given in §7.
    The diagram opposite shows such an execu-
    tion: 𝑀 · 𝑀; 𝜎2 ⇝∗fin 𝜎30 consists of 4 calls to
    external objects, and 3 calls to internal ob-
    jects. The calls to external objects are from
    𝜎2 to 𝜎3 , from 𝜎3 to 𝜎4 , from 𝜎9 to 𝜎10 , and
    from 𝜎16 to 𝜎17 . The calls to internal objects
    are from 𝜎5 to 𝜎6 , rom 𝜎7 to 𝜎8 , and from 𝜎21
    to 𝜎23 .
    In terms of our example, we want to sum-
    marise the execution of the two “outer” inter-
    nal, public methods into the “large” steps 𝜎6
    to 𝜎19 and 𝜎23 to 𝜎24 . And are not concerned
    with the states reached from these two public
    method executions.
In order to express such summaries, Def. H.27 introduces the following concepts:
   • (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎⇝∗𝑒 𝜎 ′ execution from 𝜎 to 𝜎 ′ scoped by 𝜎𝑠𝑐 , involving external states only.
   • (𝑀 · 𝑀); 𝜎⇝𝑝∗ 𝜎 ′ pb 𝜎1         𝜎 is an external state calling an internal public method, and
                             𝜎 ′ is the state after return from the public method, and
                             𝜎1 is the first state upon entry to the public method.
Continuing with our example, we have the following execution summaries:
     (1) (𝑀 · 𝑀, 𝜎3 ); 𝜎3 ⇝∗𝑒 𝜎5 Purely external execution from 𝜎3 to 𝜎5 , scoped by 𝜎3 .
     (2) (𝑀 · 𝑀); 𝜎5 ⇝𝑝∗ 𝜎20 pb 𝜎6 . Public method call from external state 𝜎5 into nternal state 𝜎6
         returning to 𝜎20 . Note that this summarises two internal method executions (𝜎6 − 𝜎19 , and
         𝜎8 − 𝜎14 ), and two external method executions (𝜎6 − 𝜎19 , and 𝜎8 − 𝜎14 ).
     (3) (𝑀 · 𝑀, 𝜎3 ); 𝜎20 ⇝∗𝑒 𝜎21 .
19 This can be done by looking in the caller’s frame – ie the one right under the topmost frame – the class of the current

receiver and the name of the currently executing method, and then looking up the method definition in the module 𝑀; if
not defined there, then it is not public.


, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                 57


  (4) (𝑀 · 𝑀); 𝜎21 ⇝𝑝∗ 𝜎25 pb 𝜎23 . Public method call from external state 𝜎21 into internal state 𝜎23 ,
      and returning to external state 𝜎25 .
  (5) (𝑀 · 𝑀, 𝜎3 ); 𝜎25 ⇝∗𝑒 𝜎28 . Purely external execution from 𝜎25 to 𝜎28 , scoped by 𝜎3 .
Definition H.27. For any module 𝑀 where 𝑀 is the internal module, external modules 𝑀, and
states 𝜎𝑠𝑐 , 𝜎, 𝜎1 , ... 𝜎𝑛 , and 𝜎 ′ , we define:
                                           
                                           
                                            𝑀, 𝜎 |= extl ∧
                                           
                                           
   (1) (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎⇝ 𝑒 𝜎   ∗  ′     ≜ [ 𝜎 = 𝜎 ′ ∧ |𝜎𝑠𝑐 | ≤ |𝜎 | ∧ |𝜎𝑠𝑐 | ≤ |𝜎 ′′ | ∨
                                           
                                            ∃𝜎 ′′ [ (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎 ⇝ 𝜎 ′′ ∧ (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎 ′′ ⇝∗𝑒 𝜎 ′ ] ]
                                           
                                           
                                                  
                                                  
                                                   𝑀, 𝜎 |= extl ∧
                         ∗   ′
                                                  
                                                  
   (2) (𝑀 · 𝑀); 𝜎⇝𝑝 𝜎 pb 𝜎1                   ≜ ∃𝜎1′ [ (𝑀 · 𝑀, 𝜎); 𝜎 ⇝ 𝜎1 ∧ 𝑀, 𝜎1 |= pub ∧
                                                  
                                                           𝑀 · 𝑀; 𝜎1 ⇝∗fin 𝜎1′ ∧ 𝑀 · 𝑀; 𝜎1′ ⇝ 𝜎 ′ ]
                                                  
                                                  
                                                  
   (3) (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎⇝𝑒,𝑝    ∗ 𝜎 ′ pb 𝜖 ≜ (𝑀 · 𝑀, 𝜎 ); 𝜎⇝∗ 𝜎 ′′
                                                        ( 𝑠𝑐         𝑒

                              ∗ 𝜎 ′ pb 𝜎 ≜ ∃𝜎 ′ , 𝜎 ′ .    (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎⇝∗𝑒 𝜎1′ ∧ (𝑀 · 𝑀); 𝜎1′ ⇝𝑝∗ 𝜎2′ pb 𝜎1 ∧
   (4) (𝑀·𝑀, 𝜎𝑠𝑐 ); 𝜎⇝𝑒,𝑝                1         1 2
                                                           (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎2′ ⇝∗𝑒 𝜎 ′
                      ∗ 𝜎 ′ pb 𝜎 ...𝜎 ≜ ∃𝜎 ′ .[ (𝑀·𝑀, 𝜎 ); 𝜎⇝∗ 𝜎 ′ pb 𝜎 ∧ (𝑀 · 𝑀, 𝜎 ); 𝜎 ′ ⇝∗ 𝜎 ′ pb 𝜎 ...𝜎
  (5) (𝑀·𝑀, 𝜎𝑠𝑐 ); 𝜎⇝𝑒,𝑝        1    𝑛    1              𝑠𝑐      𝑒,𝑝 1      1         𝑠𝑐 1 𝑒,𝑝        2
                 ∗ 𝜎′
  (6) 𝑀 · 𝑀; 𝜎⇝𝑒,𝑝                                                   ∗ 𝜎 ′ pb 𝜎 ...𝜎
                               ≜ ∃𝑛 ∈ N.∃𝜎1, ...𝜎𝑛 . (𝑀 · 𝑀, 𝜎); 𝜎⇝𝑒,𝑝         1    𝑛


  Note that (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎⇝∗𝑒 𝜎 ′ implies that 𝜎 is external, but does not imply that 𝜎 ′ is external.
(𝑀 · 𝑀, 𝜎); 𝜎⇝∗𝑒 𝜎 ′ . On the other hand, (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎⇝𝑒,𝑝 ∗ 𝜎 ′ pb 𝜎 ...𝜎 implies that 𝜎 and 𝜎 ′ are
                                                                          1    𝑛
external, and 𝜎1 , ... 𝜎1 are internal and public. Finally, note that in part (6) above it is possible that
𝑛 = 0, and so 𝑀 · 𝑀; 𝜎⇝𝑒,𝑝   ∗ 𝜎 ′ also holds when Finally, note that the decomposition used in (5) is

not unique, but since we only care for the public states this is of no importance.
  Lemma H.28 says that

  (1) Any terminating execution which starts at an external state (𝜎) consists of a number of
      external states interleaved with another number of terminating calls to public methods.
  (2) Any execution execution which starts at an external state (𝜎) and reaches another state (𝜎 ′ )
      also consists of a number of external states interleaved with another number of terminating
      calls to public methods, which may be followed by a call to some public method (at 𝜎2 ), and
      from where another execution, scoped by 𝜎2 reaches 𝜎 ′ .
Auxiliary Lemma H.28. [Summarised Executions] For module 𝑀, modules 𝑀, and states 𝜎, 𝜎 ′ :

If 𝑀, 𝜎 |= extl, then
  (1) 𝑀 · 𝑀; 𝜎⇝∗fin 𝜎 ′ =⇒ 𝑀 · 𝑀; 𝜎⇝𝑒,𝑝  ∗ 𝜎′

  (2) 𝑀 · 𝑀; 𝜎⇝ 𝜎 ∗  ′    =⇒
    (a)     𝑀 · 𝑀; 𝜎⇝𝑒,𝑝 ∗ 𝜎′ ∨

    (b)                           ∗ 𝜎 ∧ 𝑀 · 𝑀; 𝜎 ⇝ 𝜎 ∧ 𝑀, 𝜎 |= pub ∧ 𝑀 · 𝑀; 𝜎 ⇝∗ 𝜎 ′ ]
            ∃𝜎𝑐 , 𝜎𝑑 .[ 𝑀 · 𝑀; 𝜎⇝𝑒,𝑝 𝑐          𝑐   𝑑      𝑐                 𝑑

Auxiliary Lemma H.29. [Preservation of Encapsulated Assertions] For any module 𝑀, modules
𝑀, assertion 𝐴, and states 𝜎𝑠𝑐 , 𝜎, 𝜎1 ... 𝜎𝑛 , 𝜎𝑎 , 𝜎𝑏 and 𝜎 ′ :
If
   𝑀 ⊢ 𝐸𝑛𝑐 (𝐴) ∧ 𝑓 𝑣 (𝐴) = ∅ ∧ 𝑀, 𝜎, 𝑘 |= 𝐴 ∧ 𝑘 ≤ |𝜎𝑠𝑐 |.
Then

                                                          , Vol. 1, No. 1, Article . Publication date: November 2025.
58                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


     (1) 𝑀, 𝜎 |= extl ∧ (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎 ⇝ 𝜎 ′ =⇒ 𝑀, 𝜎 ′, 𝑘 |= 𝐴
     (2) (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎⇝∗𝑒 𝜎 ′ =⇒ 𝑀, 𝜎 ′, 𝑘 |= 𝐴
                            ∗ 𝜎 ′ pb 𝜎 ...𝜎 ∧
     (3) (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎⇝𝑒,𝑝           1    𝑛
            ∀𝑖 ∈ [1..𝑛].∀𝜎 𝑓 .[ 𝑀, 𝜎𝑖 , 𝑘 |= 𝐴 ∧ 𝑀 · 𝑀; 𝜎𝑖 ⇝∗fin 𝜎 𝑓 =⇒ 𝑀, 𝜎 𝑓 , 𝑘 |= 𝐴 ]
         =⇒
            𝑀, 𝜎 ′, 𝑘 |= 𝐴
            ∧
            ∀𝑖 ∈ [1..𝑛].𝑀, 𝜎𝑖 , 𝑘 |= 𝐴
            ∧
            ∀𝑖 ∈ [1..𝑛].∀𝜎 𝑓 .[ 𝑀 · 𝑀; 𝜎𝑖 ⇝∗fin 𝜎 𝑓 =⇒ 𝑀, 𝜎 𝑓 , 𝑘 |= 𝐴 ]
Proof Sketch
  (1) is proven by Def. of 𝐸𝑛𝑐 (_) and the fact |𝜎 ′ | ≥ |𝜎𝑠𝑐 | and therefore 𝑘 ≤ |𝜎 ′ |. In particular,
      the step (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎 ⇝ 𝜎 ′ may push or pop a frame onto 𝜎. If it pops a frame, then
      𝑀, 𝜎 ′, 𝑘 |= 𝐴 holds by definition. If is pushes a frame, then 𝑀, 𝜎 ′ |= 𝐴, by lemma 4.8; this
      gives that 𝑀, 𝜎 ′, 𝑘 |= 𝐴.
  (2) by induction on the number of steps in (𝑀 · 𝑀, 𝜎𝑠𝑐 ); 𝜎⇝∗𝑒 𝜎 ′ , and using (1).
  (3) by induction on the number of states appearing in 𝜎1 ...𝜎𝑛 , and using (2).
  End Proof Sketch

H.9     Sequences, Sets, Substitutions and Free Variables
Our system makes heavy use of textual substitution, textual inequality, and the concept of free
variables in assertions.
   In this subsection we introduce some notation and some lemmas to deal with these concepts.
These concepts and lemmas are by no means novel; we list them here so as to use them more easily
in the subsequent proofs.
Definition H.30 (Sequences, Disjointness, and Disjoint Concatenation). For any variables 𝑣, 𝑤,
and sequences of variables 𝑣, 𝑤 we define:
   • 𝑣 ∈ 𝑤 ≜ ∃𝑤 1, 𝑤 1 [ 𝑤 = 𝑤 1, 𝑣, 𝑤 2 ]
                   txt
   • 𝑣#𝑤 ≜ ¬(𝑣 = 𝑤).
   • 𝑣 ⊆ 𝑤 ≜ ∀𝑣.[ 𝑣 ∈ 𝑣 ⇒ 𝑣 ∈ 𝑤 ]
   • 𝑣#𝑤 ≜ ∀𝑣 ∈ 𝑣.∀𝑤 ∈ 𝑤 .[ 𝑣#𝑤 ]
   • 𝑣 ∩ 𝑤 ≜ 𝑢, such that ∀𝑢.[ 𝑢 ∈ 𝑣 ∩ 𝑤 ⇔ [ 𝑢 ∈ 𝑣 ∧ 𝑢 ∈ 𝑤 ]
   • 𝑣 \ 𝑤 ≜ 𝑢, such that ∀𝑢.[ 𝑢 ∈ 𝑣 \ 𝑤 ⇔ [ 𝑢 ∈ 𝑣 ∧ 𝑢 ∉ 𝑤 ]
   • 𝑣; 𝑤 ≜ 𝑣, 𝑤 if 𝑣#𝑤 and undefined otherwise.
Lemma H.31 (Substitutions and Free Variables). For any sequences of variables 𝑥, 𝑦, 𝑧, 𝑣, 𝑤, a
variable 𝑤, any assertion 𝐴, we have
     (1) 𝑥 [𝑦/𝑥] = 𝑦
     (2) 𝑥#𝑦 ⇒ 𝑦 [𝑧/𝑥] = 𝑦
     (3) 𝑧 ⊆ 𝑦 ⇒ 𝑦 [𝑧/𝑥] ⊆ 𝑦
     (4) 𝑦 ⊆ 𝑧 ⇒ 𝑦 [𝑧/𝑥] ⊆ 𝑧
     (5) 𝑥#𝑦 ⇒ 𝑧 [𝑦/𝑥]#𝑥
     (6) 𝐹𝑣 (𝐴[𝑦/𝑥]) = 𝐹𝑣 (𝐴) [𝑦/𝑥]
     (7) 𝐹𝑣 (𝐴) = 𝑥; 𝑣, 𝐹𝑣 (𝐴[𝑦/𝑥]) = 𝑦; 𝑤 =⇒ 𝑣 = (𝑦 ∩ 𝑣); 𝑤
                                         txt
     (8) 𝑣#𝑥#𝑦#𝑢      =⇒ 𝑤 [𝑢/𝑥] [𝑣/𝑦] = 𝑤 [𝑣/𝑦] [𝑢/𝑥]

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                            59

                                             txt
  (9) 𝑣#𝑥#𝑦#𝑢      =⇒ 𝐴[𝑢/𝑥] [𝑣/𝑦] = 𝐴[𝑣/𝑦] [𝑢/𝑥]
 (10) (𝑓 𝑣 (𝐴[𝑦/𝑥]) \ 𝑦) # 𝑥
 (11)

  Proof. (1) by induction on the number of elements in 𝑥
  (2) by induction on the number of elements in 𝑦
  (3) by induction on the number of elements in 𝑦
  (4) by induction on the number of elements in 𝑦
  (5) by induction on the structure of 𝐴
  (6) by induction on the structure of 𝐴
  (7) Assume that
      (𝑎𝑠𝑠1) 𝐹𝑣 (𝐴) = 𝑥; 𝑣,
      (𝑎𝑠𝑠2) 𝐹𝑣 (𝐴[𝑦/𝑥]) = 𝑦; 𝑤
      We define:
      (𝑎) 𝑦0 ≜ 𝑣 ∩ 𝑦, 𝑣 2 ≜ 𝑣 \ 𝑦, 𝑦1 = 𝑦0 [𝑥/𝑦]
      This gives:
      (𝑏) 𝑦0 #𝑣 2
      (𝑐) 𝑣 = 𝑦0 ; 𝑣 2
      (𝑑) 𝑦1 ⊆ 𝑦
      (𝑒) 𝑣 2 [𝑦/𝑥] = 𝑣 2 , from assumption and (a) we have 𝑥#𝑣 2 and by Lemma H.31) part (2)
      We now calculate
         𝐹𝑣 (𝐴[𝑦/𝑥]) = (𝑥; 𝑣) [𝑦/𝑥]                    by (ass1), and Lemma H.31 part (5).
                        = (𝑥; 𝑦0 ; 𝑣 2 ) [𝑦/𝑥]         by (c) above
                        = 𝑥 [𝑦/𝑥], 𝑦0 [𝑦/𝑥], 𝑣 2 [𝑦/𝑥] by distributivity of [../..]
                        = 𝑦, 𝑦1, 𝑣 2                   by Lemma H.31 part (1), (a), and (e).
                        = 𝑦; 𝑣 2                       because (d), and 𝑦#𝑣 2
         𝐹𝑣 (𝐴[𝑦/𝑥]) = 𝑦; 𝑤                            by (ass2)
      The above gives that 𝑣 2 = 𝑤. This, together with (a) and (c) give that 𝑣 = (𝑦 ∩ 𝑣); 𝑤
  (8) By case analysis on whether 𝑤 ∈ 𝑥 ... etc
  (9) By induction on the structure of 𝐴, and the guarantee from (8).
 (10) We take a variable sequence 𝑧 such that
      (𝑎) 𝐹𝑣 (𝐴) ⊆ 𝑥; 𝑧
      This gives that
      (𝑏) 𝑥#𝑧
      Part (6) of our lemma and (a) give
      (𝑐) 𝐹𝑣 (𝐴[𝑦/𝑥]) ⊆ 𝑦, 𝑧
      Therefore
      (𝑑) 𝐹𝑣 (𝐴[𝑦/𝑥]) \ 𝑦 ⊆ 𝑧
      The above, together with (b) conclude the proof
                                                                                                             □
Lemma H.32 (Substitutions and Adaptations). For any sequences of variables 𝑥, 𝑦, sequences of
expressions 𝑒, and any assertion 𝐴, we have
                                     txt
    • 𝑥#𝑦     =⇒     (𝐴[𝑒/𝑥]) −▽𝑦 = (𝐴−▽𝑦) [𝑒/𝑥]
  Proof. We first consider 𝐴 to be ⟨ 𝑒⟩⟩0 , and just take one variable. Then,
                      txt
  (⟨⟨𝑒 0 ⟩ [𝑒/𝑥]) −▽𝑦 = ⟨ 𝑒 0 [𝑒/𝑥]⟩⟩←
                                     ×− 𝑦,
and

                                                     , Vol. 1, No. 1, Article . Publication date: November 2025.
60                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble

                         txt
  (⟨⟨𝑒 0 ⟩ −▽𝑦) [𝑒/𝑥] = ⟨ 𝑒 0 [𝑒/𝑥]⟩⟩←
                                     ×− 𝑦 [𝑒/𝑥].
When 𝑥#𝑦 then the two assertions from above are textually equal. The rest follows by induction on
the length of 𝑥 and the structure of 𝐴.                                                         □
Lemma H.33. For assertion 𝐴, variables 𝑥, 𝑣, 𝑦, 𝑤, 𝑣 1 , addresses 𝛼𝑥 , 𝛼 𝑦 , 𝛼 𝑣 , and 𝛼 𝑣1
If
               txt                   txt
   a. 𝐹𝑣 (𝐴) = 𝑥; 𝑣, 𝐹𝑣 (𝐴[𝑦/𝑥]) = 𝑦; 𝑤,
   b. ∀𝑥 ∈ 𝑥 .[ 𝑥 [𝑦/𝑥] [𝛼 𝑦 /𝑦] = 𝑥 [𝛼𝑥 /𝑥] ]
        txt            txt
   c. 𝑣 = 𝑣 1 ; 𝑤, 𝑣 1 = 𝑦 ∩ 𝑣, 𝛼 𝑣,1 = 𝑣 1 [𝛼 𝑣 /𝑣]
then
                        txt
   • 𝐴[𝑦/𝑥] [𝛼 𝑦 /𝑦] = 𝐴[𝛼𝑥 /𝑥] [𝛼 𝑣,1 /𝑣 1 ]
  Proof.
  From Lemma H.31, part 7, we obtain (∗) 𝑣 = (𝑦 ∩ 𝑣); 𝑤
  We first prove that
                                                          txt
                      (∗∗) ∀𝑧 ∈ 𝐹𝑣 (𝐴) [ 𝑧 [𝑦/𝑥] [𝛼 𝑦 /𝑦] = 𝑧 [𝛼𝑥 /𝑥] [𝛼 𝑣,1 /𝑣 1 ].
  Take any arbitrary 𝑧 ∈ 𝐹𝑣 (𝐴).
Then, by assumptions a. and c., and (*) we have that either 𝑧 ∈ 𝑥, or 𝑧 ∈ 𝑣 1 , or 𝑧 ∈ 𝑤.
1st Case 𝑧 ∈ 𝑥. Then, there exists some 𝑦𝑧 ∈ 𝑦, and some 𝛼𝑧 ∈ 𝛼 𝑦 , such that 𝑧 [𝑦/𝑥] = 𝑦𝑧 and
     𝑦𝑧 [𝛼 𝑦 /𝑦] = 𝛼𝑧 . On the other hand, by part b. we obtain, that 𝑧 [𝛼𝑥 /𝑥] = 𝛼𝑧 . And because
     𝑣 1 #𝛼𝑥 we also have that 𝛼𝑧 [𝛼 𝑣,1 /𝑣 1 ]=𝛼𝑧 . This concludes the case.
2nd Case 𝑧 ∈ 𝑣 1 , which means that 𝑧 ∈ 𝑦 ∩ 𝑣. Then, because 𝑥#𝑣, we have that 𝑧 [𝑦/𝑥] = 𝑧. And
     because 𝑧 ∈ 𝑦, we obtain that there exists a 𝛼𝑧 , so that 𝑧 [𝛼 𝑦 /𝑦] = 𝛼𝑧 . Similarly, because 𝑥#𝑣,
     we also obtain that 𝑧 [𝛼𝑥 /𝑥] = 𝑧. And because 𝑣 1 ⊆ 𝑦, we also obtain that 𝑧 [𝛼 𝑣,1 /𝑣 1 ]=𝑧 [𝛼 𝑦 /𝑦].
     This concludes the case.
3rd Case 𝑧 ∈ 𝑤. From part a. of the assumptions and from (*) we obtain 𝑤#𝑦#𝑥, which implies that
     𝑧 [𝑦/𝑥] [𝛼 𝑦 /𝑦]=𝑧. Moreover, (*) also gives that 𝑤#𝑣 1 , and this gives that 𝑧 [𝛼𝑥 /𝑥] [𝛼 𝑣,1 /𝑣 1 ]=𝑧.
     This concludes the case
  The lemma follows from (*) and structural induction on 𝐴.                                                □

H.10 Reachability, Heap Identity, and their properties
We consider states with the same heaps (𝜎 ∼ 𝜎 ′ ) and properties about reachability of an address
from another address (𝑅𝑒𝑎𝑐ℎ(𝛼, 𝛼 ′ )𝜎 ).
Definition H.34. For any state 𝜎, addresses 𝛼, 𝛼 ′ , we define
      • 𝑅𝑒𝑎𝑐ℎ(𝛼, 𝛼 ′ )𝜎 ≜ ∃𝑓 .[ ⌊𝛼 .𝑓 ⌋ 𝜎 = 𝛼 ′ ]
      • 𝜎 ∼ 𝜎 ′ ≜ ∃𝜒, 𝜙 1, 𝜙 2 .[ 𝜎 = (𝜙 1, 𝜒) ∧ 𝜎 ′ = (𝜙 1, 𝜒) ]
Lemma H.35. For any module 𝑀, state 𝜎, addresses 𝛼, 𝛼 ′ , 𝛼 ′′
                   ×− 𝛼 ′ ∧ 𝑅𝑒𝑎𝑐ℎ(𝛼 ′, 𝛼 ′′ )𝜎 =⇒ 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←
  (1) 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←                                            ×− 𝛼 ′′
  (2) 𝜎 ∼ 𝜎 ′ =⇒ [ 𝑅𝑒𝑎𝑐ℎ(𝛼, 𝛼 ′ )𝜎 ⇐⇒ 𝑅𝑒𝑎𝑐ℎ(𝛼, 𝛼 ′ )𝜎 ′ ]
  (3) 𝜎 ∼ 𝜎 ′ =⇒ [ 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩← ×− 𝛼 ′′ ⇐⇒ 𝑀, 𝜎 ′ |= ⟨ 𝛼⟩⟩←
                                                            ×− 𝛼 ′′ ]
  (4) 𝜎 ∼ 𝜎 ′ ∧ 𝐹𝑣 (𝐴) = ∅ ∧ 𝑆𝑡𝑏𝑙 (𝐴) =⇒ [ 𝑀, 𝜎 |= 𝐴 ⇐⇒ 𝑀, 𝜎 ′ |= 𝐴 ]
     Proof.
     (1) By unfolding/folding the definitions
     (2) By unfolding/folding the definitions

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                   61


   (3) By unfolding/folding definitions.
   (4) By structural induction on 𝐴, and Lemma H.35 part 3.
                                                                                                                    □

H.11    Preservation of assertions when pushing or popping frames
In this section we discuss the preservation of satisfaction of assertions when calling methods or
returning from methods – i.e. when pushing or popping frames. Namely, since pushing/popping
frames does not modify the heap, these operations should preserve satisfaction of some assertion 𝐴,
up to the fact that a) passing an object as a parameter of a a result might break its protection, and b)
the bindings of variables change with pushing/popping frames. To deal with a) upon method call,
we require that the fame being pushed or the frame to which we return is internal (𝑀, 𝜎 ′ |= intl),
or require the adapted version of an assertion (i.e. 𝐴−▽𝑣 rather than 𝐴). To deal with b) we either
require that there are no free variables in 𝐴, or we break the free variables of 𝐴 into two parts, i.e.
𝐹𝑣 (𝐴𝑖𝑛 ) = 𝑣 1 ; 𝑣 2 , where the value of 𝑣 3 in the caller is the same as that of 𝑣 1 in the called frame. This
is described in lemmas H.40 - H.42.
   We have four lemmas: Lemma H.40 describes preservation from a caller to an internal called,
lemma H.41 describes preservation from a caller to any called, Lemma H.42 describes preservation
from an internal called to a caller, and Lemma H.43 describes preservation from an any called to a
caller, These four lemmas are used in the soundness proof for the four Hoare rules about method
calls, as given in Fig. 7.
   In the rest of this section we will first introduce some further auxiliary concepts and lemmas,
and then state, discuss and prove Lemmas H.40 - H.42.



  Plans for next three subsections Lemmas H.40-H.41 are quite complex, because they deal with
substitution of some of the assertions’ free variables. We therefore approach the proofs gradually:
We first state and prove a very simplified version of Lemmas H.40-H.41, where the assertion (𝐴𝑖𝑛 or
𝐴𝑜𝑢𝑡 ) is only about protection and only contains addresses; this is the only basic assertion which is
not 𝑆𝑡𝑏𝑙. We then state a slightly more general version of Lemmas H.40-H.41, where the assertion
(𝐴𝑖𝑛 or 𝐴𝑜𝑢𝑡 ) is variable-free.

H.12    Preservation of variable-free simple protection when pushing/popping frames
We now move to consider preservation of variable-free assertions about protection when push-
ing/popping frames
Lemma H.36 (From caller to called - protected, and variable-free). For any address 𝛼, addresses 𝛼,
states 𝜎, 𝜎 ′ , and frame 𝜙.
If 𝜎 ′ = 𝜎 ▽ 𝜙 then
    a. 𝑀, 𝜎, 𝑘 |= ⟨ 𝛼⟩⟩ ∧ 𝑀, 𝜎 ′ |= intl ∧ 𝑅𝑛𝑔(𝜙) ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎)           =⇒      𝑀, 𝜎 ′, 𝑘 |= ⟨ 𝛼⟩⟩
    b. 𝑀, 𝜎, 𝑘 |= ⟨ 𝛼⟩⟩← ×− 𝛼 ∧ 𝑅𝑛𝑔(𝜙) ⊆ 𝛼                                    =⇒ 𝑀, 𝜎 ′ |= ⟨ 𝛼⟩⟩
     c. 𝑀, 𝜎, 𝑘 |= ⟨ 𝛼⟩⟩ ∧ ⟨ 𝛼⟩⟩←
                                ×− 𝛼 ∧ 𝑅𝑛𝑔(𝜙) ⊆ 𝛼                           =⇒ 𝑀, 𝜎 ′, 𝑘 |= ⟨ 𝛼⟩⟩
   Proof.
    a. (1) Take any 𝛼 ′ ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 ′ ). Then, by assumptions, we have 𝛼 ′ ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎). This
       gives, again by assumptions, that 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←   ×− 𝛼 ′ . By the construction of 𝜎, and lemma
                                           ′        ×− 𝛼 . From (1) and (2) and because 𝑀, 𝜎 ′ |= intl
       H.35 part 1, we obtain that (2) 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←   ′
                           ′
       we obtain that 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩ . Then apply lemma H.35 part H.5, and we are done.
    b. By unfolding and folding the definitions, and application of Lemma H.35 part 1.

                                                            , Vol. 1, No. 1, Article . Publication date: November 2025.
62                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


   c. By part H.35 part b. and H.5.
  Notice that part H.36 requires that the called (𝜎 ′ ) is internal, but parts b. and c. do not.
  Notice also that the conclusion in part b. is 𝑀, 𝜎 ′ |= ⟨ 𝛼⟩⟩ and not 𝑀, 𝜎 ′, 𝑘 |= ⟨ 𝛼⟩⟩ . This is so,
because it is possible that 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←
                                         ×− 𝛼 but 𝑀, 𝜎 ̸ |= ⟨ 𝛼⟩⟩ .
                                                                                                      □
Lemma H.37 (From called to caller – protected, and variable-free). For any states 𝜎, 𝜎 ′ , variable 𝑣,
address 𝛼 𝑣 , addresses 𝛼, and statement 𝑠𝑡𝑚𝑡.
If 𝜎 ′ = (𝜎 △ ) [𝑣 ↦→ 𝛼 𝑣 ] [cont ↦→ 𝑠𝑡𝑚𝑡],
then
    a. 𝑀, 𝜎, 𝑘 |= ⟨ 𝛼⟩⟩ ∧ 𝑘 < |𝜎 | ∧ 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←
                                                  ×− 𝛼 𝑣                   =⇒ 𝑀, 𝜎 ′, 𝑘 |= ⟨ 𝛼⟩⟩ .
    b. 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩ ∧ 𝛼 ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎)                                =⇒ 𝑀, 𝜎 ′, 𝑘 |= ⟨ 𝛼⟩⟩←    ×− 𝛼.
     Proof.
      a. (1) Take any 𝑖 ∈ [𝑘..|𝜎 ′ |). Then, by definitions and assumption, we have 𝑀, 𝜎 [𝑖] |= ⟨ 𝛼⟩⟩ . Take
         any 𝛼 ′ ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 [𝑖]). We obtain that 𝑀, 𝜎 [𝑖] |= ⟨ 𝛼⟩⟩←    ×− 𝛼 ′ . Therefore, 𝑀, 𝜎 [𝑖] |= ⟨ 𝛼⟩⟩ .
                             ′                                        ′
         Moreover, 𝜎 [𝑖]=𝜎 [𝑖], and we therefore obtain (2) 𝑀, 𝜎 [𝑖] |= ⟨ 𝛼⟩⟩ .
         (3) Now take a 𝛼 ′ ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 ′ ).
         Then, we have that either (A): 𝛼 ′ ∈ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎 [|𝜎 ′ |]), or (B): 𝑅𝑒𝑎𝑐ℎ(𝛼𝑟 , 𝛼 ′ )𝜎 ′ .
         In the case of (A): Because 𝑘, |𝜎 | = |𝜎 ′ | + 1, and because 𝑀, 𝜎, 𝑘 |= ⟨ 𝛼⟩⟩ we have 𝑀, 𝜎 |=
              ×− 𝛼 ′ . Because 𝜎 ∼ 𝜎 ′ and Lemma H.35 part 3, we obtain (A’) 𝑀, 𝜎 ′ |= ⟨ 𝛼⟩⟩←
         ⟨ 𝛼⟩⟩←                                                                                    ×− 𝛼 ′
         In the case of (B): Because 𝜎 ∼ 𝜎 and lemma H.35 part 2, we obtain 𝑅𝑒𝑎𝑐ℎ(𝛼𝑟 , 𝛼 ′ )𝜎 . Then,
                                               ′

         applying Lemma H.35 part 3 and assumptions, we obtain (B’) 𝑀, 𝜎 ′ |= ⟨ 𝛼⟩⟩←          ×− 𝛼 ′ .
                                                                ′
         From (3), (A), (A’), (B) and (B’) we obtain: (4) 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩ .
         With (1), (2), (4) and Lemma H.35 part 4 we are done.
      b. From the definitions we obtain that 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←   ×− 𝛼. Because 𝜎 ∼ 𝜎 ′ and lemma H.35 part 3,
                          ′
         we obtain 𝑀, 𝜎 |= ⟨ 𝛼⟩⟩←    ×− 𝛼. And because of lemma H.4, part 3, we obtain 𝑀, 𝜎 ′, 𝑘 |= ⟨ 𝛼⟩⟩←×− 𝛼.
                                                                                                             □

H.13      Preservation of variable-free, 𝑆𝑡𝑏𝑙 + , assertions when pushing/popping frames
We now move consider preservation of variable-free assertions when pushing/popping frames, and
generalize the lemmas H.36 and H.37
Lemma H.38 (From caller to called - variable-free, and 𝑆𝑡𝑏𝑙 + ). For any assertion 𝐴, addresses 𝛼,
states 𝜎, 𝜎 ′ , and frame 𝜙.
If 𝜎 ′ = 𝜎 ▽ 𝜙 and 𝑆𝑡𝑏 + (𝐴), and 𝐹𝑣 (𝐴) = ∅,
then
    a. 𝑀, 𝜎, 𝑘 |= 𝐴 ∧ 𝑀, 𝜎 ′ |= intl ∧ 𝑅𝑛𝑔(𝜙) ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎)                  =⇒      𝑀, 𝜎 ′, 𝑘 |= 𝐴
    b. 𝑀, 𝜎, 𝑘 |= 𝐴−▽(𝛼) ∧ 𝑅𝑛𝑔(𝜙) ⊆ 𝛼                                            =⇒ 𝑀, 𝜎 ′ |= 𝐴
    c. 𝑀, 𝜎, 𝑘 |= 𝐴 ∧ 𝐴−▽(𝛼) ∧ 𝑅𝑛𝑔(𝜙) ⊆ 𝛼                                      =⇒ 𝑀, 𝜎 ′, 𝑘 |= 𝐴
     Proof.
      a. By Lemma H.36, part H.36 and structural induction on the definition of 𝑆𝑡𝑏 + (_).
      b. By Lemma H.36, part H.36 and structural induction on the definition of 𝑆𝑡𝑏 + (_).
      c. By part b. and Lemma H.4.
                                                                                                                   □
Lemma H.39 (From called to caller – protected, and variable-free). For any states 𝜎, 𝜎 ′ , variable 𝑣,
address 𝛼 𝑣 , addresses 𝛼, and statement 𝑠𝑡𝑚𝑡.

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                             63


If 𝜎 ′ = (𝜎 △ ) [𝑣 ↦→ 𝛼 𝑣 ] [cont ↦→ 𝑠𝑡𝑚𝑡], and 𝑆𝑡𝑏 + (𝐴), and 𝐹𝑣 (𝐴) = ∅
then
    a. 𝑀, 𝜎, 𝑘 |= 𝐴 ∧ 𝑘 < |𝜎 | ∧ 𝑀, 𝜎 |= 𝐴−▽𝛼 𝑣                                                    =⇒ 𝑀, 𝜎 ′, 𝑘 |= 𝐴 .
    b. 𝑀, 𝜎 |= 𝐴 ∧ 𝛼 ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎)                                                             =⇒ 𝑀, 𝜎 ′, 𝑘 |= 𝐴−▽(𝛼).
   Proof.
    a. By Lemma H.37, part a. and structural induction on the definition of 𝑆𝑡𝑏 + (_).
    b. By Lemma H.37, part b. and structural induction on the definition of 𝑆𝑡𝑏 + (_).
                                                                                                                              □

H.14      Preservation of assertions when pushing or popping frames – stated and proven
Lemma H.40 (From caller to internal called). For any assertion 𝐴𝑖𝑛 , states 𝜎, 𝜎 ′ , variables 𝑣 1 , 𝑣 2 ,
𝑣 3 , 𝑣 4 , 𝑣 6 , and frame 𝜙.
If
      (i) 𝑆𝑡𝑏 + (𝐴𝑖𝑛 ),
    (ii) 𝐹𝑣 (𝐴𝑖𝑛 ) = 𝑣 1 ; 𝑣 2 20 , 𝐹𝑣 (𝐴𝑖𝑛 [𝑣 3 /𝑣 1 ]) = 𝑣 3 ; 𝑣 4 , 𝑣 6 ≜ 𝑣 2 ∩ 𝑣 3 ; 𝑣 4 ,
   (iii) 𝜎 ′ = 𝜎 ▽ 𝜙 ∧ 𝑅𝑛𝑔(𝜙) = ⌊𝑣 3 ⌋ 𝜎
   (iv) ⌊𝑣 1 ⌋ 𝜎 ′ = ⌊𝑣 3 ⌋ 𝜎 ,
then
       a. 𝑀, 𝜎, 𝑘 |= 𝐴𝑖𝑛 [𝑣 3 /𝑣 1 ] ∧ 𝑀, 𝜎 ′ |= intl                                     =⇒    𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑖𝑛 [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ]
       b. 𝑀, 𝜎, 𝑘 |= (𝐴𝑖𝑛 [𝑣 3 /𝑣 1 ]) −▽(𝑣 3 )                                              =⇒    𝑀, 𝜎 ′ |= 𝐴𝑖𝑛 ⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ].
   Discussion of Lemma. In lemma H.40, state 𝜎 is the state right before pushing the new frame on
the stack, while state 𝜎 ′ is the state right after pushing the frame on the stack. That is, 𝜎 is the last
state before entering the method body, and 𝜎 ′ is the first state after entering the method body. 𝐴𝑖𝑛
stands for the method’s precondition, while the variables 𝑣 1 stand for the formal parameters of the
method, and 𝑣 3 stand for the actual parameters of the call. Therefore, 𝑣 1 is the domain of the new
frame, and 𝜎𝑣 3 is its range. The variables 𝑣 6 are the free variables of 𝐴𝑖𝑛 which are not in 𝑣 1 – c.f.
Lemma H.31 part ( 7). Therefore if (a.) the callee is internal, and 𝐴𝑖𝑛 [𝑣 3 /𝑣 1 ] holds at the call point,
or if (b.) (𝐴𝑖𝑛 [𝑣 3 /𝑣 1 ]) −▽(𝑣 3 ) holds at the call point, then 𝐴𝑖𝑛 [.../𝑣 6 1] holds right after pushing 𝜙
onto the stack. Notice the difference in the conclusion in (a.) and (b.): in the first case we have deep
satisfaction, while in the second case we only have shallow satisfaction.
  Proof.
  We will use 𝛼 1 as short for {⌊𝑣 1 ⌋ 𝜎 ′ , and 𝛼 3 as short for ⌊𝑣 3 ⌋ 𝜎 .
We aslo define 𝑣 6,1 ≜ 𝑣 2 ∩ 𝑣 3 , 𝛼 6,1 ≜ 𝑣 6,1 [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ]
We establish that
                                      txt
 (∗) 𝐴𝑖𝑛 [𝑣 3 /𝑣 1 ] [⌊𝑣 3 ⌋ 𝜎 /𝑣 3 ] = 𝐴𝑖𝑛 [𝛼 1 /𝑣 1 ] [𝛼 6,1 /𝑣 6,1 ]
This holds by By Lemma H.33 and assumption (iv) of the current lemma.
And we define 𝑣 6,2 ≜ 𝑣 2 \ 𝑣 3 , 𝛼 6,2 ≜ 𝑣 62 [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ].
   a. Assume
      𝑀, 𝜎, 𝑘 |= 𝐴𝑖𝑛 [𝑣 3 /𝑣 1 ].         By Lemma 4.5 this implies that
      𝑀, 𝜎, 𝑘 |= 𝐴𝑖𝑛 [𝑣 3 /𝑣 1 ] [𝛼 3 /𝑣 3 ]      By (*) from above we have
      𝑀, 𝜎, 𝑘 |= 𝐴𝑖𝑛 [𝛼 1 /𝑣 1 [𝛼 6,1 /𝑣 6,1 ]
                          The above, and Lemma 4.5 give that
20 As we said earlier. this gives also that the variable sequences are pairwise disjoint, i.e. 𝑣 #𝑣 .
                                                                                                1 2


                                                                     , Vol. 1, No. 1, Article . Publication date: November 2025.
64                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


        𝑀, 𝜎, 𝑘 |= 𝐴𝑖𝑛 [𝛼 1 /𝑣 1 ] [𝛼 6,1 /𝑣 6,1 ] [𝛼 6,2 /𝑣 6,2 ]
        The assertion above is variable-free.Therefore, by Lemma H.38 part a. we also obtain
        𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑖𝑛 [𝛼 1 /𝑣 1 ] [𝛼 6,1 /𝑣 6,1 ] [𝛼 6,2 /𝑣 6,2 ]
        With 4.5 the above gives
        𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑖𝑛 [⌊𝑣 1 ⌋ 𝜎 ′ /𝑣 1 ] [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ]
        By Lemma 4.5 , we obtain
        𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑖𝑛 [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ]
     b. Assume
        𝑀, 𝜎, 𝑘 |= (𝐴𝑖𝑛 [𝑣 3 /𝑣 1 ]) −▽(𝑣 3 ).          By Lemma 4.5 this implies that
        𝑀, 𝜎, 𝑘 |= ((𝐴𝑖𝑛 [𝑣 3 /𝑣 1 ]) −▽(𝑣 3 )) [𝛼 3 /𝑣 3 ]          which implies that
        𝑀, 𝜎, 𝑘 |= (𝐴𝑖𝑛 [𝑣 3 /𝑣 1 ] [𝛼 3 /𝑣 3 ]) −▽(𝛼 3 )          By (*) from above we have
        𝑀, 𝜎, 𝑘 |= (𝐴𝑖𝑛 [𝛼 1 /𝑣 1 ] [𝛼 6,1 /𝑣 6,1 ]) −▽(𝛼 3 )
                         The above, and Lemma 4.5 give that
        𝑀, 𝜎, 𝑘 |= ((𝐴𝑖𝑛 [𝛼 1 /𝑣 1 ] [𝛼 6,1 /𝑣 6,1 ]) −▽(𝛼 3 )) [𝛼 6,2 /𝑣 6,2 ]
                          And the above gives
        𝑀, 𝜎, 𝑘 |= (𝐴𝑖𝑛 [𝛼 1 /𝑣 1 ] [𝛼 6,1 /𝑣 6,1 ] [𝛼 6,2 /𝑣 6,2 ]) −▽(𝛼 3 )
        The assertion above is variable-free.Therefore, by Lemma H.38 part b. we also obtain
        𝑀𝜎 ′ |= 𝐴𝑖𝑛 [𝛼 1 /𝑣 1 ] [𝛼 6,1 /𝑣 6,1 ] [𝛼 6,2 /𝑣 6,2 ]
        We apply Lemma 4.5 , and Lemma 4.5 , and obtain
        𝑀, 𝜎 ′ |= 𝐴𝑖𝑛 [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ]
                                                                                                                   □

Lemma H.41 (From caller to any called). For any assertion 𝐴𝑖𝑛 , states 𝜎, 𝜎 ′ , variables 𝑣 3 statement
𝑠𝑡𝑚𝑡, and frame 𝜙.
If
    (i) 𝑆𝑡𝑏 + (𝐴𝑖𝑛 ),
   (ii) 𝐹𝑣 (𝐴𝑖𝑛 ) = ∅,
  (iii) 𝜎 ′ = 𝜎 ▽ 𝜙 ∧ 𝑅𝑛𝑔(𝜙) = ⌊𝑣 3 ⌋ 𝜎 ,
then
     a. 𝑀, 𝜎, 𝑘 |= 𝐴𝑖𝑛 −▽(𝑣 3 )                                                             =⇒       𝑀, 𝜎 ′ |= 𝐴𝑖𝑛 .
     b. 𝑀, 𝜎, 𝑘 |= (𝐴𝑖𝑛 ∧ (𝐴𝑖𝑛 −▽(𝑣 3 )))                                                   =⇒      𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑖𝑛

     Proof.        a. Assume that
         𝑀, 𝜎, 𝑘 |= 𝐴𝑖𝑛 −▽(𝑣 3 )
         By Lemma 4.5 this implies that
         𝑀, 𝜎, 𝑘 |= 𝐴𝑖𝑛 −▽( ⌊𝑣 3 ⌋ 𝜎 ).
         We now have a variable-free assertion, and by Lemma H.38, part b., we obtain
         𝑀, 𝜎 ′ |= 𝐴𝑖𝑛 .
      b. Assume that
         𝑀, 𝜎, 𝑘 |= 𝐴𝑖𝑛 ∧ 𝐴𝑖𝑛 −▽(𝑣 3 )
         By Lemma 4.5 this implies that
         𝑀, 𝜎, 𝑘 |= 𝐴𝑖𝑛 ∧ 𝐴𝑖𝑛 −▽( ⌊𝑣 3 ⌋ 𝜎 ).
         We now have a variable-free assertion, and by Lemma H.38, part b., we obtain
         𝑀, 𝜎 ′, 𝑘 |= |=𝐴𝑖𝑛 .
                                                                                                                   □

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                  65


    Discussion of Lemma H.41. In this lemma, as in lemma H.40, 𝜎 stands for the last state before
entering the method body, and 𝜎 ′ for the first state after entering the method body. 𝐴𝑖𝑛 stands for
a module invariant in which all free variables have been substituted by addresses. The lemma is
intended for external calls, and therefore we have no knowledge of the method’s formal parameters.
The variables 𝑣 3 stand for the actual parameters of the call, and therefore ⌊𝑣 3 ⌋ 𝜎 is the range of
the new frame. Therefore if (a.) the adapted version, 𝐴𝑖𝑛 −▽(𝑣 3 ), holds at the call point, then the
unadapted version, 𝐴𝑖𝑛 holds right after pushing 𝜙 onto the stack. Notice that even though the
premise of (a.) requires deep satisfaction, the conclusion promises only weak satisfaction. Moreover,
if (b.) the adapted as well as the unadapted version, 𝐴𝑖𝑛 ∧ 𝐴𝑖𝑛 −▽(𝑣 3 ) holds at the call point, then
the unadapted version, 𝐴𝑖𝑛 holds right after pushing 𝜙 onto the stack. Notice the difference in the
conclusion in (a.) and (b.): in the first case we have shallow satisfaction, while in the second case
we only have deep satisfaction.
Lemma H.42 (From internal called to caller). For any assertion 𝐴𝑜𝑢𝑡 , states 𝜎, 𝜎 ′ , variables 𝑟𝑒𝑠, 𝑢
variable sequences 𝑣 1 , 𝑣 3 , 𝑣 5 , and statement 𝑠𝑡𝑚𝑡.
If
     (i) 𝑆𝑡𝑏 + (𝐴𝑜𝑢𝑡 ),
    (ii) 𝐹𝑣 (𝐴𝑜𝑢𝑡 ) ⊆ 𝑣 1 ,
   (iii) ⌊𝑣 5 ⌋ 𝜎 ′ , ⌊𝑟𝑒𝑠⌋ 𝜎 ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎) ∧ 𝑀, 𝜎 ′ |= intl.
   (iv) 𝜎 ′ = (𝜎 △ ) [𝑢 ↦→ ⌊𝑟𝑒𝑠⌋ 𝜎 ] [cont ↦→ 𝑠𝑡𝑚𝑡] ∧ ⌊𝑣 1 ⌋ 𝜎 = ⌊𝑣 3 ⌋ 𝜎 ′ .
then
      a. 𝑀, 𝜎, 𝑘 |= 𝐴𝑜𝑢𝑡 ∧ (𝐴𝑜𝑢𝑡 −▽𝑟𝑒𝑠) ∧ |𝜎 ′ | ≥ 𝑘                          =⇒ 𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑜𝑢𝑡 [𝑣 3 /𝑣 1 ] .
      b. 𝑀, 𝜎 |= 𝐴𝑜𝑢𝑡                                             =⇒ 𝑀, 𝜎 ′, 𝑘 |= (𝐴𝑜𝑢𝑡 [𝑣 3 /𝑣 1 ]) −▽𝑣 5 .
   Discussion of Lemma H.42. State 𝜎 stands for the last state in the method body, and 𝜎 ′ for the first
state after exiting the method call. 𝐴𝑜𝑢𝑡 stands for a method postcondition. The lemma is intended
for internal calls, and therefore we know the method’s formal parameters. The variables 𝑣 1 stand for
the formal parameters of the method, and 𝑣 3 stand for the actual parameters of the call. Therefore
the formal parameters of the called have the same values as the actual parameters in the caller
⌊𝑣 1 ⌋ 𝜎 = ⌊𝑣 3 ⌋ 𝜎 ′ . Therefore ( a.) and (b.) promise that if the postcondition 𝐴𝑜𝑢𝑡 holds before popping
the frame, then it also holds after popping frame after replacing the the formal parameters by
the actual parameters 𝐴𝑜𝑢𝑡 [𝑣 3 /𝑣 1 ]. As in earlier lemmas, there is an important difference between
(a.) and (b.): In (a.), we require deep satisfaction at the called, and obtain at the deep satisfaction
of the unadapted version (𝐴𝑜𝑢𝑡 [𝑣 3 /𝑣 1 ]) at the return point; while in (b.), we only require shallow
satisfaction at the called, and obtain deep satisfaction of the adapted version ((𝐴𝑜𝑢𝑡 [𝑣 3 /𝑣 1 ]) −▽𝑣 5 ), at
the return point.

  Proof.
  We use the following short hands: 𝛼 as ⌊𝑟𝑒𝑠⌋ 𝜎 , 𝛼 1 for ⌊𝑣 1 ⌋ 𝜎 , 𝛼 5 as short for ⌊𝑣 5 ⌋ 𝜎 ′ .
   a. Assume that
      𝑀, 𝜎, 𝑘 |= 𝐴𝑜𝑢𝑡 ∧ 𝐴𝑜𝑢𝑡 −▽𝑟𝑒𝑠
      By Lemma 4.5 this implies that
      𝑀, 𝜎, 𝑘 |= 𝐴𝑜𝑢𝑡 [𝛼 1 /𝑣 1 ] ∧ (𝐴𝑜𝑢𝑡 [𝛼 1 /𝑣 1 ]) −▽𝛼.
      We now have a variable-free assertion, and by Lemma H.39, part a., we obtain
      𝑀, 𝜎, 𝑘 |= 𝐴𝑜𝑢𝑡 [𝛼 1 /𝑣 1 ].
      By Lemma 4.5 , and because ⌊𝑣 1 ⌋ 𝜎 = ⌊𝑣 3 ⌋ 𝜎 ′ this implies that
      𝑀, 𝜎, 𝑘 |= 𝐴𝑜𝑢𝑡 [𝑣 3 /𝑣 1 ].

                                                           , Vol. 1, No. 1, Article . Publication date: November 2025.
66                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


     b. Assume that
        𝑀, 𝜎 |= 𝐴𝑜𝑢𝑡
        By Lemma 4.5 this implies that
        𝑀, 𝜎 |= 𝐴𝑜𝑢𝑡 [𝛼 1 /𝑣 1 ]
        We now have a variable-free assertion, and by Lemma H.39, part b., we obtain
        𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑜𝑢𝑡 [𝛼 1 /𝑣 1 ] −▽𝛼 5
        By Lemma 4.5 , and because ⌊𝑣 1 ⌋ 𝜎 = ⌊𝑣 3 ⌋ 𝜎 ′ and 𝛼 5 = ⌊𝑣 5 ⌋ 𝜎 ′ , we obtain
        𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑜𝑢𝑡 [𝑣 3 /𝑣 1 ] −▽𝑣 5
                                                                                                                   □
Lemma H.43 (From any called to caller). For any assertion 𝐴𝑜𝑢𝑡                    , states 𝜎, 𝜎 ′ , variables 𝑟𝑒𝑠, 𝑢
variable sequence 𝑣 5 , and statement 𝑠𝑡𝑚𝑡.
If
     (i) 𝑆𝑡𝑏 + (𝐴𝑜𝑢𝑡 ),
    (ii) 𝐹𝑣 (𝐴𝑜𝑢𝑡 ) = ∅,
   (iii) ⌊𝑣 5 ⌋ 𝜎 ′ , ⌊𝑟𝑒𝑠⌋ 𝜎 ⊆ 𝐿𝑜𝑐𝑅𝑐ℎ𝑏𝑙 (𝜎).
   (iv) 𝜎 ′ = (𝜎 △ ) [𝑢 ↦→ ⌊𝑟𝑒𝑠⌋ 𝜎 ] [cont ↦→ 𝑠𝑡𝑚𝑡].
then
      a. 𝑀, 𝜎 |= 𝐴𝑜𝑢𝑡                                          =⇒ 𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑜𝑢𝑡 −▽(𝑣 5 ).
      b. 𝑀, 𝜎, 𝑘 |= 𝐴𝑜𝑢𝑡 ∧ |𝜎 | ≥ 𝑘 ′                   =⇒ 𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑜𝑢𝑡 ∧ 𝐴𝑜𝑢𝑡 −▽(𝑣 5 )
     Proof.
      a. Assume that
           𝑀, 𝜎 |= 𝐴𝑜𝑢𝑡
         Since 𝐴𝑜𝑢𝑡 is a variable-free assertion, by Lemma H.39, part a., we obtain
           𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑜𝑢𝑡 −▽( ⌊𝑣 5 ⌋ 𝜎 ′ ).
         By Lemma 4.5 , we obtain
           𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑜𝑢𝑡 −▽(𝑣 5 )
      b. Similar argument to the proof of Lemma H.42, part (b).
                                                                                                                   □
   Discussion of lemma H.43. , Similarly to lemma H.42, in this lemma, state 𝜎 stands for the last
state in the method body, and 𝜎 ′ for the first state after exiting the method call. 𝐴𝑜𝑢𝑡 stands for a
method postcondition. The lemma is meant to apply to external calls, and therefore, we do not know
the method’s formal parameters, 𝐴𝑜𝑢𝑡 is meant to stand for a module invariant where all the free
variables have been substituted by addresses – i.e. 𝐴𝑜𝑢𝑡 has no free variables. The variables 𝑣 3 stand
for the actual parameters of the call. Parts (a.) and (b.) promise that if the postcondition 𝐴𝑜𝑢𝑡 holds
before popping the frame, then it its adapted version also holds after popping frame (𝐴𝑜𝑢𝑡 −▽𝑣 5 ). As
in earlier lemmas, there is an important difference between (a.) and (b.) In (a.), we require shallow
satisfaction at the called, and obtain deep satisfaction of the adapted version (𝐴𝑜𝑢𝑡 −▽𝑣 5 ) at the return
point; while in (b.), we require deep satisfaction at the called, and obtain deep satisfaction of the
conjuction of the unadapted with the adapted version (𝐴𝑜𝑢𝑡 ∧ 𝐴𝑜𝑢𝑡 −▽𝑣 5 ), at the return point.

H.15 Use of Lemmas H.40-H.41
As we said earlier, Lemmas H.40-H.41 are used to prove the soundness of the Hoare logic rules for
method calls.
   In the proof of soundness of Call_Int. we will use Lemma H.40 part (a.) and Lemma H.42 part
(a.). In the proof of soundness of Call_Int_Adapt we will use Lemma H.40 part (b.) and Lemma

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                        67


H.42 part (b.). In the proof of soundness of Call_Ext_Adapt we will use Lemma H.41 part (a.) and
Lemma H.43 part (a.). And finally, in the proof of soundness of Call_Ext_Adapt_Strong we will
use Lemma H.41 part (b.) and Lemma H.43 part (b.).

H.16     Proof of Theorem 7.3 – part (A)
Begin Proof
Take any 𝑀, 𝑀, with
                      (1) ⊢ 𝑀.
We will prove that
                      (∗) ∀𝜎, 𝐴, 𝐴′, 𝐴′′ .
                           [ 𝑀 ⊢ { 𝐴 } 𝜎.cont{ 𝐴′ } ∥ { 𝐴′′ } =⇒ 𝑀 |=𝑑𝑒𝑒𝑝 { 𝐴 } 𝑠𝑡𝑚𝑡 { 𝐴′ } ∥
   ′′
{ 𝐴 } ].
by induction on the well-founded ordering _ ≪𝑀,𝑀 _.
Take 𝜎, 𝐴, 𝐴′ , 𝐴′′ , 𝑧, 𝑤, 𝛼, 𝜎 ′ , 𝜎 ′′ arbitrary. Assume that
                      (2) 𝑀 ⊢ { 𝐴 } 𝜎.cont{ 𝐴′ } ∥ { 𝐴′′ }
                      (3) 𝑤 = 𝐹𝑣 (𝐴) ∩ 𝑑𝑜𝑚(𝜎), 𝑧 = 𝐹𝑣 (𝐴) \ 𝑑𝑜𝑚(𝜎) 21
                      (4) 𝑀, 𝜎, 𝑘 |= 𝐴[𝛼/𝑧]
To show
                      (∗∗) 𝑀 · 𝑀; 𝜎⇝∗fin 𝜎 ′ =⇒ 𝑀, 𝜎 ′, 𝑘 |= 𝐴′ [𝛼/𝑧]
                      (∗∗∗) 𝑀 · 𝑀; 𝜎⇝∗𝜎 ′′ =⇒ 𝑀, 𝜎 ′′, 𝑘 |= extl → 𝐴′′ [𝛼/𝑧] [⌊𝑤⌋ 𝜎 /𝑤]
We proceed by case analysis on the rule applied in the last step of the proof of (2). We only describe
some cases.
mid By Theorem 7.2.
seq Therefore, there exist statements 𝑠𝑡𝑚𝑡 1 and 𝑠𝑡𝑚𝑡 2 , and assertions 𝐴1 , 𝐴2 and 𝐴′′ , so that
     𝐴1 = 𝐴, and 𝐴2 = 𝐴′ , and 𝜎.cont = 𝑠𝑡𝑚𝑡 1 ; 𝑠𝑡𝑚𝑡 2 ,. We apply lemma H.26, and obtain that
         txt             txt               txt

     there exists an intermediate state 𝜎1 . The proofs for 𝑠𝑡𝑚𝑡 1 and 𝑠𝑡𝑚𝑡 2 , and the intermediate
     state 𝜎1 are in the ≪ relation. Therefore, we can apply the inductive hypothesis.
combine by induction hypothesis, and unfolding and folding the definitions
conseq using Lemma H.4 part 4 and axiom H.1
Call_Int Therefore, there exist 𝑢, 𝑦𝑜 , 𝐶, 𝑦, 𝐴𝑝𝑟𝑒 , 𝐴𝑝𝑜𝑠𝑡 , and 𝐴𝑚𝑖𝑑 , such that
                             txt
             (5) 𝜎.cont = 𝑢 := 𝑦0 .𝑚(𝑦),
             (6) ⊢ 𝑀 : { 𝐴𝑝𝑟𝑒 } 𝐷 ::𝑚(𝑥 : 𝐷) { 𝐴𝑝𝑜𝑠𝑡 } ∥ {𝐴𝑚𝑖𝑑 },
                   txt
             (7) 𝐴 = 𝑦0 : 𝐷, 𝑦 : 𝐷 ∧ 𝐴𝑝𝑟𝑒 [𝑦0, 𝑦/this, 𝑥],
                 𝐴′ = 𝐴𝑝𝑜𝑠𝑡 [𝑦0, 𝑦, 𝑢/this, 𝑥, res],
                    txt


                 𝐴′′ = 𝐴𝑚𝑖𝑑 .
                     txt

     Also,
             (8) 𝑀 · 𝑀; 𝜎 ⇝ 𝜎1 ,
     where
             (8𝑎) 𝜎1 ≜ (𝜎 ▽ (this ↦→ ⌊𝑦0 ⌋ 𝜎 , 𝑥 ↦→ ⌊𝑦⌋ 𝜎 ) [cont ↦→ 𝑠𝑡𝑚𝑡𝑚 ],
             (8𝑏) mBody(𝑚, 𝐷, 𝑀) = 𝑦 : 𝐷 { 𝑠𝑡𝑚𝑡𝑚 } .
     We define the shorthands:
             (9) 𝐴𝑝𝑟 ≜ this : 𝐷, 𝑥 : 𝐷 ∧ 𝐴𝑝𝑟𝑒 .
             (9𝑎) 𝐴𝑝𝑟𝑎 ≜ this : 𝐷, 𝑥 : 𝐷 ∧ 𝐴𝑝𝑟𝑒 ∧ 𝐴𝑝𝑟𝑒 −▽(𝑦0, 𝑦).
21 Remember that 𝑑𝑜𝑚 (𝜎 ) is the set of variables defined in the top frame of 𝜎



                                                                 , Vol. 1, No. 1, Article . Publication date: November 2025.
68                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


              (9𝑏) 𝐴𝑝𝑜𝑎 ≜ 𝐴𝑝𝑜𝑠𝑡 ∧ 𝐴𝑝𝑜𝑠𝑡 −▽res.
       By (1), (6), (7), (9), and definition of ⊢ 𝑀 in Section 6.3 rule Method and we obtain
              (10) 𝑀 ⊢ { 𝐴𝑝𝑟𝑎 } 𝑠𝑡𝑚𝑡𝑚 { 𝐴𝑝𝑜𝑎 } ∥ { 𝐴𝑚𝑖𝑑 }.
       From (8) we obtain
              (11) (𝐴𝑝𝑟𝑎 , 𝜎1, 𝐴𝑝𝑜𝑎 , 𝐴𝑚𝑖𝑑 ) ≪𝑀,𝑀 (𝐴, 𝜎, 𝐴′, 𝐴′′ )
       In order to be able to apply the induction hypothesis, we need to prove something of the
       form ...𝜎1 |= 𝐴𝑝𝑟 [../𝑓 𝑣 (𝐴𝑝𝑟 ) \ 𝑑𝑜𝑚(𝜎1 )]. To that aim we will apply Lemma H.40 part a. on
       (4), (8a) and (9). For this, we take
              (12) 𝑣 1 ≜ this, 𝑥, 𝑣 2 ≜ 𝐹𝑣 (𝐴𝑝𝑟 ) \ 𝑣 1 , 𝑣 3 ≜ 𝑦0, 𝑦, 𝑣 4 ≜ 𝐹𝑣 (𝐴) \ 𝑣 3
       These definitions give that
                         txt
              (12𝑎) 𝐴 = 𝐴𝑝𝑟 [𝑣 3 /𝑣 1 ],
              (12𝑏) 𝐹𝑣 (𝐴𝑝𝑟 ) = 𝑣 1 ; 𝑣 2 .
              (12𝑐) 𝐹𝑣 (𝐴) = 𝑣 3 ; 𝑣 4 .
       With (12a), (12b), (12c), ( and Lemma H.31 part (7), we obtain that
              (12𝑑) 𝑣 2 = 𝑦𝑟 ; 𝑣 4 , where 𝑦𝑟 ≜ 𝑣 2 ∩ 𝑣 3
       Furthermore, (8a), and (12) give that:
              (12𝑒) ⌊𝑣 1 ⌋ 𝜎1 = ⌊𝑣 3 ⌋ 𝜎
       Then, (4), (12a), (12c) and (12f) give that
              (13) 𝑀, 𝜎, 𝑘 |= 𝐴𝑝𝑟 [𝑣 3 /𝑣 1 ] [𝛼/𝑧]
       Moreover, we have that 𝑧#𝑣 3 . From Lemma H.31 part (10) we obtain 𝑧#𝑣 1 . And, because 𝛼 are
       addresses wile 𝑣 1 are variables, we also have that 𝛼#𝑣 1 . These facts, together with Lemma
       H.31 part (9) give that
                                            txt
              (13𝑎) 𝐴𝑝𝑟 [𝑣 3 /𝑣 1 ] [𝛼/𝑧] = 𝐴𝑝𝑟 [𝛼/𝑧] [𝑣 3 /𝑣 1 ]
       From (13a) and (13), we obtain
              (13𝑏) 𝑀, 𝜎, 𝑘 |= 𝐴𝑝𝑟 [𝛼/𝑧] [𝑣 3 /𝑣 1 ]
       From (4), (8a), (12a)-(12e) we see that the requirements of Lemma H.40 part a. are satisfied
       where we take 𝐴𝑖𝑛 to be 𝐴𝑝𝑟 [𝛼/𝑧]. We use the definition of 𝑦𝑟 in (12d), and define
              (13𝑐) 𝑣 6 ≜ 𝑦𝑟 ; (𝑣 4 \ 𝑧) which, with (12d) also gives: 𝑣 2 = 𝑣 6 ; 𝑧
       We apply Lemma H.40 part a. on (13b), (13c) and obtain
              (14𝑎) 𝑀, 𝜎1, 𝑘 |= 𝐴𝑝𝑟 [𝛼/𝑧] [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ].
       Moreover, we have the 𝑀, 𝜎1 |= intl. We apply lemma H.42.(H.42), and obtain
              (14𝑏) 𝑀, 𝜎1, 𝑘 |= 𝐴𝑝𝑟 [𝛼/𝑧] [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ] ∧ 𝐴𝑝𝑟 −▽(this, 𝑦).
       With similar re-orderings to earlier, we obain
              (14𝑏) 𝑀, 𝜎1, 𝑘 |= 𝐴𝑝𝑟𝑎 [𝛼/𝑧] [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ].
       For the proof of (∗∗) as well as for the proof of (∗∗∗), we will want to apply the inductive
       hypothesis. For this, we need to determine the value of 𝐹𝑣 (𝐴𝑝𝑟 ) \ 𝑑𝑜𝑚(𝜎1 ), as well as the
       value of 𝐹𝑣 (𝐴𝑝𝑟 ) ∩ 𝑑𝑜𝑚(𝜎1 ). This is what we do next. From (8a) we have that
              (15𝑎) 𝑑𝑜𝑚(𝜎1 ) = {this, 𝑥 }.
       This, with (12) and (12b) gives that
              (15𝑏) 𝐹𝑣 (𝐴𝑝𝑟𝑎 ) ∩ 𝑑𝑜𝑚(𝜎1 ) = 𝑣 1 .
              (15𝑐) 𝐹𝑣 (𝐴𝑝𝑟𝑎 ) \ 𝑑𝑜𝑚(𝜎1 ) = 𝑣 2 .
       Moreover, (12d) and (13d) give that
              (15𝑑) 𝐹𝑣 (𝐴𝑝𝑟𝑎 ) \ 𝑑𝑜𝑚(𝜎1 ) = 𝑧 2 = 𝑧; 𝑣 6 .

       Proving (∗∗). Assume that 𝑀 · 𝑀; 𝜎⇝∗fin 𝜎 ′ . Then, by the operational semantics, we obtain
       that there exists state 𝜎1′ , such that


, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                            69


             (16) 𝑀 · 𝑀; 𝜎1 ⇝∗fin 𝜎1′
             (17) 𝜎 ′ = (𝜎1′ △ ) [𝑢 ↦→ ⌊res⌋ 𝜎1′ ] [cont ↦→ 𝜖].
      We now apply the induction hypothesis on (14), (16), (15d), and obtain
             (18) 𝑀, 𝜎1′ , 𝑘 |= (𝐴𝑝𝑜𝑠𝑡 ) [𝛼/𝑧] [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ].
      We now want to obtain something of the form ...𝜎 ′ |= ...𝐴′ . We now want to be able to apply
      Lemma H.42, part a. on (18). Therefore, we define
             (18𝑎) 𝐴𝑜𝑢𝑡 ≜ 𝐴𝑝𝑜𝑎 [𝛼/𝑧] [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ]
             (18𝑏) 𝑣 1,𝑎 ≜ 𝑣 1, res, 𝑣 3,𝑎 ≜ 𝑣 3, 𝑢.
      The wellformedness condition for specifications requires that 𝐹𝑣 (𝐴𝑝𝑜𝑠𝑡 ) ⊆ 𝐹𝑣 (𝐴𝑝𝑟 ) ∪ {res}.
      This, together with (9), (12d) and (18b) give
             (19𝑎) 𝐹𝑣 (𝐴𝑜𝑢𝑡 ) ⊆ 𝑣 1,𝑎
      Also, by (18b), and (17), we have that
             (19𝑏) ⌊𝑣 3,𝑎 ⌋ 𝜎 ′ = ⌊𝑣 1,𝑎 ⌋ 𝜎1′ .
      From (4) we obtain that 𝑘 ≤ |𝜎 |. From (8a) we obtain that |𝜎1 | = |𝜎 | + 1. From (16) we obtain
      that |𝜎1′ | = |𝜎1 |, and from (17) we obtain that |𝜎 ′ | = |𝜎1′ | − 1. All this gives that:
             (19𝑐) 𝑘 ≤ |𝜎 ′ |
      We now apply Lemma H.42, part a., and obtain
             (20) 𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑜𝑢𝑡 [𝑣 3,𝑎 /𝑣 1,𝑎 ].
      We expand the definition from (18a), and re-order the substitutions by a similar argument as
      in in step (13a), using Lemma part (9), and obtain
             (20𝑎) 𝑀, 𝜎 ′, 𝑘 |= 𝐴𝑝𝑜𝑎 [𝑣 3,𝑎 /𝑣 1,𝑎 ] [𝛼/𝑧] [⌊𝑣 6 ⌋ 𝜎 /𝑣 6 ].
      By (20a), (18b), and because by Lemma B.2 we have that ⌊𝑣 6 ⌋ 𝜎 =⌊𝑣 6 ⌋ 𝜎 ′ , we obtain
             (21) 𝑀, 𝜎 ′, 𝑘 |= (𝐴𝑝𝑜𝑎 ) [𝑦0, 𝑦, 𝑢/this, 𝑥, res] [𝛼/𝑧]..
      With (7) we conclude.



       Proving (∗∗∗). Take a 𝜎 ′′ . Assume that
             (15) 𝑀 · 𝑀; 𝜎⇝∗𝜎 ′′
             (16) 𝑀 · 𝑀, 𝜎 ′′ |= extl.
       Then, from (8) and (15) we also obtain that
             (15) 𝑀 · 𝑀; 𝜎1 ⇝∗𝜎 ′′
       By (10), (11) and application of the induction hypothesis on (13), (14c), and (15), we obtain
       that
             (𝛽 ′ ) 𝑀, 𝜎 ′′, 𝑘 |= 𝐴𝑚𝑖𝑑 [𝛼/𝑧] [⌊𝑤⌋ 𝜎 /𝑤].
       and using (7) we are done.


Call_Ext_Adapt is in some parts, similar to Call_Int. We highlight the differences in green .
     Therefore, there exist 𝑢, 𝑦𝑜 , 𝐶, 𝐷, 𝑦, ands 𝐴𝑖𝑛𝑣 , such that
                        txt
          (5) 𝜎.cont = 𝑢 := 𝑦0 .𝑚(𝑦),
                            A
          (6) ⊢ 𝑀 : 𝑥 : 𝐶.{𝐴𝑖𝑛𝑣 },
                  txt
          (7) 𝐴 = 𝑦0 : external, 𝑥 : 𝐶 ∧ 𝐴𝑖𝑛𝑣 −▽(𝑦0, 𝑦),
               𝐴′ = 𝐴𝑖𝑛𝑣 −▽(𝑦0, 𝑦),
                   txt


               𝐴′′ = 𝐴𝑖𝑛𝑣 .
                    txt




                                                     , Vol. 1, No. 1, Article . Publication date: November 2025.
70                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


       Also,
              (8) 𝑀 · 𝑀; 𝜎 ⇝ 𝜎𝑎 ,
       where
              (8𝑎) 𝜎𝑎 ≜ (𝜎 ▽ (this ↦→ ⌊𝑦0 ⌋ 𝜎 , 𝑝 ↦→ ⌊𝑦⌋ 𝜎 ) [cont ↦→ 𝑠𝑡𝑚𝑡𝑚 ],
              (8𝑏) mBody(𝑚, 𝐷, 𝑀) = 𝑝 : 𝐷 { 𝑠𝑡𝑚𝑡𝑚 } .
              (8𝑐) 𝐷 is the class of ⌊𝑦0 ⌋ 𝜎 , and 𝐷 is external.
       By (7), and well-formedness of module invariants, we obtain
              (9𝑎) 𝐹𝑣 (𝐴𝑖𝑛𝑣 ) ⊆ 𝑥,
              (9𝑎) 𝐹𝑣 (𝐴) = 𝑦0, 𝑦, 𝑥
       By Barendregt, we also obtain that
              (10) 𝑑𝑜𝑚(𝜎) #𝑥
       This, together with (3) gives that
              (10) 𝑧 = 𝑥
       From (4), (7) and the definition of satisfaction we obtain
              (10) 𝑀, 𝜎, 𝑘 |= (𝑥 : 𝐶 ∧ 𝐴𝑖𝑛𝑣 ▽ 𝑦0, 𝑦) [𝛼/𝑧].
       The above gives that
              (10𝑎) 𝑀, 𝜎, 𝑘 |= ( (𝑥 : 𝐶) [𝛼/𝑧] ∧ (𝐴𝑖𝑛𝑣 [𝛼/𝑧]) ) ▽ 𝑦0, 𝑦 .
       We take 𝐴𝑖𝑛 to be (𝑥 : 𝐶) [𝛼/𝑧] ∧ (𝐴𝑖𝑛𝑣 [𝛼/𝑧]), and apply Lemma H.41, part a.. This gives
       that
              (11) 𝑀, 𝜎𝑎 |= (𝑥 : 𝐶) [𝛼/𝑧] ∧ 𝐴𝑖𝑛𝑣 [𝛼/𝑧]

       Proving (∗∗). We shall use the short hand
              (12) 𝐴𝑜 ≜ 𝛼 : 𝐶 ∧ 𝐴𝑖𝑛𝑣 [𝛼/𝑧].
       Assume that 𝑀 · 𝑀; 𝜎⇝∗fin 𝜎 ′ . Then, by the operational semantics, we obtain that there exists
       state 𝜎𝑏′ , such that
              (16) 𝑀 · 𝑀; 𝜎𝑎 ⇝∗fin 𝜎𝑏
              (17) 𝜎 ′ = (𝜎𝑏 △ ) [𝑢 ↦→ ⌊res⌋ 𝜎1′ ] [cont ↦→ 𝜖].
       By Lemma H.28 part 1, and Def. H.27, we obtain that there exists a sequence of states 𝜎1 , ...
       𝜎𝑛 , such that
              (17) (𝑀 · 𝑀, 𝜎𝑎 ); 𝜎𝑎 ⇝𝑒,𝑝  ∗ 𝜎 pb 𝜎 ...𝜎
                                             𝑏      1  𝑛
       By Def. H.27, the states 𝜎1 , ... 𝜎𝑛 are all public, and correspond to the execution of a public
       method. Therefore, by rule Invariant for well-formed modules, we obtain that
              (18) ∀𝑖 ∈ 1..𝑛.
                [ 𝑀 ⊢ { this : 𝐷𝑖 , 𝑝𝑖 : 𝐷𝑖 , 𝑥 : 𝐶 ∧ 𝐴𝑖𝑛𝑣 }𝜎𝑖 .cont{ 𝐴𝑖𝑛𝑣,𝑟 } ∥ { 𝐴𝑖𝑛𝑣 } ]
       where 𝐷𝑖 is the class of the receiver, 𝑝𝑖 are the formal parameters, and 𝐷𝑖 are the types of
       the formal parameters of the 𝑖-th public method, and where we use the shorthand 𝐴𝑖𝑛𝑣,𝑟 ≜
       𝐴𝑖𝑛𝑣 −▽res.
       Moreover, (17) gives that
              (19) ∀𝑖 ∈ 1..𝑛.[ 𝑀 · 𝑀; 𝜎⇝∗𝜎𝑖 ]
       From (18) and (19) we obtain
              (20) ∀𝑖 ∈ [1..𝑛].
                       [ (this : 𝐷𝑖 , 𝑝𝑖 : 𝐷𝑖 , 𝑥 : 𝐶 ∧ 𝐴𝑖𝑛𝑣 , 𝜎𝑖 , 𝐴𝑖𝑛𝑣,𝑟 , 𝐴𝑖𝑛𝑣 )
                             ≪𝑀,𝑀
                          (𝐴, 𝜎, 𝐴′, 𝐴′′ ) ]
       We take
              (21) 𝑘 = |𝜎𝑎 | By application of the induction hypothesis on (20) we obtain that

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                             71


           (22) ∀𝑖 ∈ [1..𝑛].∀𝜎 𝑓 .[ 𝑀, 𝜎𝑖 , 𝑘 |= 𝐴𝑜 ∧ 𝑀 · 𝑀; 𝜎𝑖 ⇝∗fin 𝜎 𝑓 =⇒ 𝑀, 𝜎 𝑓 , 𝑘 |= 𝐴𝑜 ]
      We can now apply Lemma H.29, part 3, and because |𝜎𝑎 | = |𝜎𝑏 |, we obtain that
           (23) 𝑀, 𝜎𝑏 |= 𝐴𝑖𝑛𝑣 [𝛼/𝑥]
      We apply Lemma H.43 part a., and obtain
           (24) 𝑀, 𝜎 ′ |= 𝐴𝑖𝑛𝑣 [𝛼/𝑥] −▽𝑦0, 𝑦
      And since 𝐴𝑖𝑛𝑣 [𝛼/𝑥] −▽𝑦0, 𝑦 is stable, and by rearranging, and applying (10), we obtain
           (25) 𝑀, 𝜎 ′, 𝑘 |= (𝐴𝑖𝑛𝑣 −▽𝑦0, 𝑦) [𝛼/𝑧]
      Apply (7), and we are done.

      Proving (∗∗∗). Take a 𝜎 ′′ . Assume that
             (12) 𝑀 · 𝑀; 𝜎⇝∗𝜎 ′′
             (13) 𝑀 · 𝑀, 𝜎 ′′ |= extl.
      We apply lemma 1, part 2 on (12) and see that there are two cases
      1st Case 𝑀 · 𝑀; 𝜎𝑎 ⇝𝑒,𝑝 ∗ 𝜎 ′′

      That is, the execution from 𝜎𝑎 to 𝜎 ′′ goes only through external states. We use (11), and that
      𝐴𝑖𝑛𝑣 is encapsulated, and are done with lemma H.29, part 1.
      2nd Case for some 𝜎𝑐 , 𝜎𝑑 . we have
                      ∗ 𝜎 ∧ 𝑀 · 𝑀; 𝜎 ⇝ 𝜎 ∧ 𝑀, 𝜎 |= pub ∧ 𝑀 · 𝑀; 𝜎 ⇝∗ 𝜎 ′
         𝑀 · 𝑀; 𝜎𝑎 ⇝𝑒,𝑝   𝑐             𝑐      𝑑        𝑑                   𝑑
      We apply similar arguments as in steps (17)-(23) and obtain
             (14) 𝑀, 𝜎𝑐 |= 𝐴𝑖𝑛𝑣 [𝛼/𝑥]
      State 𝜎𝑐 is a public, internal state; therefore there exists a Hoare proof that it preserves the
      invariant. By applying the inductive hypothesis, and the fact that 𝑧 = 𝑥, we obtain:
             (14) 𝑀, 𝜎 ′′ |= 𝐴𝑖𝑛𝑣 [𝛼/𝑧]


Call_Ext_Adapt_Strong is very similar to Call_Ext_Adaprt. We will summarize the similar
     steps, and highlight the differences in green .
     Therefore, there exist 𝑢, 𝑦𝑜 , 𝐶, 𝐷, 𝑦, ands 𝐴𝑖𝑛𝑣 , such that
                          txt
            (5) 𝜎.cont = 𝑢 := 𝑦0 .𝑚(𝑦),
                            A
            (6) ⊢ 𝑀 : 𝑥 : 𝐶.{𝐴𝑖𝑛𝑣 },
                   txt
            (7) 𝐴 = 𝑦0 : external, 𝑥 : 𝐶 ∧ 𝐴𝑖𝑛𝑣 ∧ 𝐴𝑖𝑛𝑣 −▽(𝑦0, 𝑦),
                 𝐴′ = 𝐴𝑖𝑛𝑣 ∧ 𝐴𝑖𝑛𝑣 −▽(𝑦0, 𝑦),
                    txt


                 𝐴′′ = 𝐴𝑖𝑛𝑣 .
                     txt

     Also,
            (8) 𝑀 · 𝑀; 𝜎 ⇝ 𝜎𝑎 ,
     By similar steps to (8a)-(10) from the previous case, we obtain
            (10𝑎) 𝑀, 𝜎, 𝑘 |= 𝐴𝑖𝑛𝑣 [𝛼/𝑧] ∧ ( (𝑥 : 𝐶) [𝛼/𝑧] ∧ (𝐴𝑖𝑛𝑣 [𝛼/𝑧]) ) ▽ 𝑦0, 𝑦.
     We now apply lemma apply Lemma H.41, part b.. This gives that
            (11) 𝑀, 𝜎𝑎 , 𝑘 |= ( (𝑥 : 𝐶) [𝛼/𝑧] ∧ 𝐴𝑖𝑛𝑣 [𝛼/𝑧] ∧ ( (𝑥 : 𝐶) [𝛼/𝑧]) ▽ 𝑦0, 𝑦 ).
     the rest is similar to earlier cases




End Proof



                                                      , Vol. 1, No. 1, Article . Publication date: November 2025.
72                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


H.17     Proof Sketch of Theorem 7.3 – part (B)
Proof Sketch By induction on the cases for the specification 𝑆. If it is a method spec, then the
theorem follows from 7.3. If it is a conjunction, then by inductive hypothesis.
                              txt A
The interesting case is 𝑆 = 𝑥 : 𝐶.{𝐴}.
Assume that 𝑀, 𝜎, 𝑘 |= 𝐴[𝛼/𝑥], that 𝑀, 𝜎 |= extl, that 𝑀 · 𝑀; 𝜎⇝∗𝜎 ′ , and that 𝑀, 𝜎 |= extl,
We want to show that 𝑀, 𝜎 ′, 𝑘 |= 𝐴[𝛼/𝑥].
Then, by lemma H.28, we obtain that either
     (1) 𝑀 · 𝑀; 𝜎⇝𝑒,𝑝∗ 𝜎 ′ , or

     (2) ∃𝜎1, 𝜎2 .[ 𝑀 · 𝑀; 𝜎⇝𝑒,𝑝  ∗ 𝜎 ∧ 𝑀 · 𝑀; 𝜎 ⇝ 𝜎 ∧ 𝑀, 𝜎 |= pub ∧ 𝑀 · 𝑀; 𝜎 ⇝∗ 𝜎 ′ ]
                                     1          1   2        2                  2
In Case (1), we apply H.29, part (3). In order to fulfill the second premise of Lemma H.29, part
(3), we make use of the fact that ⊢ 𝑀, apply the rule Method, and theorem 7.3. This gives us
𝑀, 𝜎 ′, 𝑘 |= 𝐴[𝛼/𝑥]
In Case (2), we proceed as in (1) and obtain that 𝑀, 𝜎1, 𝑘 |= 𝐴[𝛼/𝑥]. Because 𝑀 ⊢ 𝐸𝑛𝑐 (𝐴), we also
obtain that 𝑀, 𝜎2, 𝑘 |= 𝐴[𝛼/𝑥]. Since we are now executing a public method, and because ⊢ 𝑀, we
can apply Invariant, and theorem 7.3, and obtain 𝑀, 𝜎 ′, 𝑘 |= 𝐴[𝛼/𝑥]
 End Proof Sketch




, Vol. 1, No. 1, Article . Publication date: November 2025.
     Reasoning about External Calls – Extended Version                                                               73


     I     Proving Limited Effects for the Shop/Account Example
     In Section 2 we introduced a Shop that allows clients to make purchases through the buy method.
     The body if this method includes a method call to an unknown external object (buyer.pay(...)).
        In this section we use our Hoare logic from Section 6 to outline the proof that the buy method
     does not expose the Shop’s Account, its Key, or allow the Account’s balance to be illicitly
     modified.
        We outline the proof that 𝑀𝑔𝑜𝑜𝑑 ⊢ 𝑆 2 , and that 𝑀 𝑓 𝑖𝑛𝑒 ⊢ 𝑆 2 . We also show why 𝑀𝑏𝑎𝑑 ⊬ 𝑆 2 .
        We rewrite the code of 𝑀𝑔𝑜𝑜𝑑 and so 𝑀 𝑓 𝑖𝑛𝑒 so that it adheres to the syntax as defined in Fig. 4
     (§I.1). We extend the specification 𝑆 2 , so that is also makes a specification for the private method
     set (§I.2). After that, we outline the proofs that 𝑀𝑔𝑜𝑜𝑑 ⊢ 𝑆 2 , and that 𝑀 𝑓 𝑖𝑛𝑒 ⊢ 𝑆 2 (in §I.2), and that
     𝑀𝑔𝑜𝑜𝑑 ⊢ 𝑆 3 , and that 𝑀 𝑓 𝑖𝑛𝑒 ⊢ 𝑆 3 (§I.4). These proofs have been mechanized in Coq, and the source
     code will be submitted as an artefact. We also discuss why 𝑀𝑏𝑎𝑑 ⊬ 𝑆 2 (§I.3.2).

     I.1    Expressing the Shop example in the syntax from Fig. 4
     We now express our example in the syntax of Fig. 4. For this, we add a return type to each of the
     methods; We turn all local variables to parameter; We add an explicit assignment to the variable
     res: and We add a temporary variable tmp to which we assign the result of our void methods.
     For simplicity, we allow the shorthands += and -=. And we also allow definition of local variables,
     e.g. int price := ..

 1   module M𝑔𝑜𝑜𝑑
 2     ...
 3     class Shop
 4       field accnt : Account,
 5       field invntry : Inventory,
 6       field clients: ..
 7
 8         public method buy(buyer:external, anItem:Item, price: int,
 9                  myAccnt: Account, oldBalance: int, newBalance: int, tmp:int) : int
10           price := anItem.price;
11           myAccnt := this.accnt;
12           oldBalance := myAccnt.blnce;
13           tmp := buyer.pay(myAccnt, price)      // external call!
14           newBalance := myAccnt.blnce;
15           if (newBalance == oldBalance+price) then
16                tmp := this.send(buyer,anItem)
17           else
18              tmp := buyer.tell("you have not paid me") ;
19           res := 0
20
21           private method send(buyer:external, anItem:Item) : int
22            ...
23       class Account
24         field blnce : int
25         field key : Key
26
27         public method transfer(dest:Account, key':Key, amt:nat) :int
28           if (this.key==key') then
29             this.blnce-=amt;
30             dest.blnce+=amt
31           else
32             res := 0
33           res := 0


                                                             , Vol. 1, No. 1, Article . Publication date: November 2025.
     74                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


34
35           public method set(key':Key) : int
36            if (this.key==null) then
37                  this.key:=key'
38            else
39              res := 0
40            res := 0


     Remember that 𝑀 𝑓 𝑖𝑛𝑒 is identical to 𝑀𝑔𝑜𝑜𝑑 , except for the method set. We describe the module
     below.

 1   module M 𝑓 𝑖𝑛𝑒
 2     ...
 3     class Shop
 4         ... 𝑎𝑠 𝑖𝑛 𝑀𝑔𝑜𝑜𝑑
 5     class Account
 6       field blnce : int
 7       field key : Key
 8
 9          public method transfer(dest:Account, key':Key, amt:nat) :int
10             ... 𝑎𝑠 𝑖𝑛 𝑀𝑔𝑜𝑜𝑑
11
12           public method set(key':Key, k'':Key) : int
13            if (this.key==key') then
14                  this.key:=key''
15            else
16              res := 0
17            res := 0




     I.2    Proving that 𝑀𝑔𝑜𝑜𝑑 and 𝑀 𝑓 𝑖𝑛𝑒 satisfy 𝑆 2
     We redefine 𝑆 2 so that it also describes the behaviour of method send. and have:
            𝑆 2𝑎 ≜ { a : Account ∧ e : external ∧ ⟨ a.key⟩⟩←         ×− e }
                           private Shop :: send(buyer : external, anItem : Item)
                      { ⟨ a.key⟩⟩←  ×− 𝑒 } ∥ {⟨⟨a.key⟩⟩← ×− 𝑒}
            𝑆 2𝑏 ≜ { a : Account ∧ a.blnce = b }
                           private Shop :: send(buyer : external, anItem : Item)
                      { a.blnce = b } ∥ {a.blnce = b}
           𝑆 2,𝑠𝑡𝑟𝑜𝑛𝑔 ≜ 𝑆 2 ∧ 𝑆 2𝑎 ∧ 𝑆 2𝑏
       For brevity we only show that buy satisfies our scoped invariants, as the all other methods of
     the M𝑔𝑜𝑜𝑑 interface are relatively simple, and do not make any external calls.
       To write our proofs more succinctly, we will use ClassId::methId.body as a shorthand for
     the method body of methId defined in ClassId.

     Lemma I.1 (𝑀𝑔𝑜𝑜𝑑 satisfies 𝑆 2,𝑠𝑡𝑟𝑜𝑛𝑔 ). 𝑀𝑔𝑜𝑜𝑑 ⊢ 𝑆 2,𝑠𝑡𝑟𝑜𝑛𝑔

          Proof Outline In order to prove that

                                                       A
                                            𝑀𝑔𝑜𝑜𝑑 ⊢ a : Account.{⟨⟨a.key⟩⟩ }

     , Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                   75


we have to apply Invariant from Fig. 8. That is, for each class 𝐶 defined in 𝑀𝑔𝑜𝑜𝑑 , and for each
public method 𝑚 in 𝐶, with parameters 𝑦 : 𝐷, we have to prove that


            𝑀𝑔𝑜𝑜𝑑 ⊢ { this : C, 𝑦 : 𝐷, a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                          ×− (this, 𝑦) }
                               C :: m.body
                      { ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                             ×− res } || { ⟨ a.key⟩⟩ }




  Thus, we need to prove three Hoare quadruples: one for Shop::buy, one for Account::transfer,
and one for Account::set. That is, we have to prove that


                (1?) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑏𝑢𝑦 , a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                         ×− Ids𝑏𝑢𝑦 }
                                         Shop :: buy.body
                                 {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }
                  (2?) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑡𝑟𝑛𝑠 , a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                            ×− Ids𝑡𝑟𝑛𝑠 }
                                         Account :: transfer.body
                                 {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }
                  (3?) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑠𝑒𝑡 , a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                           ×− Ids𝑠𝑒𝑡 }
                                         Account :: set.body
                                 {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }


where we are using ? to indicate that this needs to be proven, and where we are using the shorthands
  A𝑏𝑢𝑦        ≜     this : Shop, buyer : external, anItem : Item, price : int,
                    myAccnt : Account, oldBalance : int, newBalance : int, tmp : int.
  Ids𝑏𝑢𝑦      ≜     this, buyer, anItem, price, myAccnt, oldBalance, newBalance, tmp.
  A𝑡𝑟𝑛𝑠       ≜     this : Account, dest : Account, key’ : Key, amt : nat
  Ids𝑡𝑟𝑛𝑠     ≜     this, dest, key’, amt
  A𝑠𝑒𝑡        ≜     this : Account, key’ : Key, key” : Key.
  Ids𝑠𝑒𝑡      ≜     this, key’, key”.
  We will also need to prove that Send satisfies specifications 𝑆 2𝑎 and 𝑆 2𝑏 .
  We outline the proof of (1?) in Lemma I.3,and the proof of (2) in Lemma I.4. We do not prove (3),
but will prove that set from 𝑀 𝑓 𝑖𝑛𝑒 satisfies 𝑆 2 ; shown in Lemma I.5 – ie for module 𝑀 𝑓 𝑖𝑛𝑒 .
                                                                                                  □
  We also want to prove that 𝑀 𝑓 𝑖𝑛𝑒 satisfies the specification 𝑆 2,𝑠𝑡𝑟𝑜𝑛𝑔 .


Lemma I.2 (𝑀 𝑓 𝑖𝑛𝑒 satisfies 𝑆 2,𝑠𝑡𝑟𝑜𝑛𝑔 ). 𝑀 𝑓 𝑖𝑛𝑒 ⊢ 𝑆 2,𝑠𝑡𝑟𝑜𝑛𝑔


  Proof Outline The proof of


                                             A
                                    𝑀 𝑓 𝑖𝑛𝑒 ⊢ a : Account.{⟨⟨a.key⟩⟩ }

                                                            , Vol. 1, No. 1, Article . Publication date: November 2025.
76                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


goes along similar lines to the proof of lemma I.1. Thus, we need to prove the following three Hoare
quadruples:

                  (4?) 𝑀 𝑓 𝑖𝑛𝑒 ⊢ { A𝑏𝑢𝑦 , a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                             ×− Ids𝑏𝑢𝑦 }
                                             Shop :: buy.body
                                    {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }
                   (5?) 𝑀 𝑓 𝑖𝑛𝑒 ⊢ { A𝑡𝑟𝑛𝑠 , a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                               ×− Ids𝑡𝑟𝑛𝑠 }
                                             Account :: transfer.body
                                    {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }
                   (6?) 𝑀 𝑓 𝑖𝑛𝑒 ⊢ { A𝑠𝑒𝑡 , a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                              ×− Ids𝑠𝑒𝑡 }
                                             Account :: set.body
                                    {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }

  The proof of (4?) is identical to that of (1?); the proof of (5?) is identical to that of (2?). We outline
the proof (6?) in Lemma I.5 in §I.2.
                                                                                                           □

Lemma I.3 (Shop::buy satisfies 𝑆 2 ).

               (1) 𝑀𝑔𝑜𝑜𝑑 ⊢{ A𝑏𝑢𝑦 a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                    ×− Ids𝑏𝑢𝑦 }
                                         Shop :: buy.body
                                {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }

   Proof Outline We will use the shorthand A1 ≜ A𝑏𝑢𝑦 , a : Account. We will split the proof
into 1) proving that statements 10, 11, 12 preserve the protection of a.key from the buyer, 2)
proving that the external call
1st Step: proving statements 10, 11, 12
   We apply the underlying Hoare logic and prove that the statements on lines 10, 11, 12 do not
affect the value of a.key, ie that for a 𝑧 ∉ {price, myAccnt, oldBalance}, we have


                      (10) 𝑀𝑔𝑜𝑜𝑑 ⊢𝑢𝑙 { A1 ∧ 𝑧 = a.key}
                                                   price:=anItem.price;
                                                   myAccnt:=this.accnt;
                                                   oldBalance := myAccnt.blnce;
                                          {𝑧 = a.key}

  We then apply Embed_UL, Prot-1 and Prot-2 and Combine and and Types-2 on (10) and use
the shorthand stmts10,11,12 for the statements on lines 10, 11 and 12, and obtain:


                          (11) 𝑀𝑔𝑜𝑜𝑑 ⊢{ A1 ∧ ⟨ a.key⟩⟩ ∧ ⟨ buyer⟩⟩←
                                                                  ×− a.key}
                                                     stmts10,11,12
                                            { ⟨ a.key⟩⟩ ∧ ⟨ buyer⟩⟩←
                                                                   ×− a.key}

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                 77


  We apply Mid on (11) and obtain


                      (12) 𝑀𝑔𝑜𝑜𝑑 ⊢{ A1 ∧ ⟨ a.key⟩⟩←
                                                  ×− buyer }
                                              stmts10,11,12
                                      { A1 ∧ ⟨ a.key⟩⟩ ∧ ⟨ buyer⟩⟩←
                                                                  ×− a.key } ||
                                      { ⟨ a.key⟩⟩ }


2nd Step: Proving the External Call
  We now need to prove that the external method call buyer.pay(this.accnt, price)
protects the key. i.e.


                (13?) 𝑀𝑔𝑜𝑜𝑑 ⊢{ A1 ∧ ⟨ a.key⟩⟩, ∧ ⟨ a.key⟩⟩←
                                                          ×− buyer}
                                         tmp := buyer.pay(myAccnt, price)
                                 { A1 ∧ ⟨ a.key⟩⟩ ∧ ⟨ buyer⟩⟩←
                                                             ×− a.key} ||
                                 { ⟨ a.key⟩⟩ }

                      A
  We use that 𝑀 ⊢ a : Account.{⟨⟨a.key⟩⟩ } and obtain


       (14) 𝑀𝑔𝑜𝑜𝑑 ⊢{ buyer : external, ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                            ×− (buyer, myAccnt, price) }
                             tmp := buyer.pay(myAccnt, price)
                     { ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                            ×− (buyer, myAccnt, price) } ||
                     { ⟨ a.key⟩⟩ }


  Moreover by the type declarations and the type rules, we obtain that all objects directly or
indirectly accessible accessible from myAccnt are internal or scalar. This, together with Prot-
Intl, gives that
    (15)     𝑀𝑔𝑜𝑜𝑑 ⊢ A1 −→ ⟨ a.key⟩⟩←  ×− myAccnt
Similarly, because price is a nat, and because of Prot-Int1 , we obtain
    (16)     𝑀𝑔𝑜𝑜𝑑 ⊢ A1 −→ ⟨ a.key⟩⟩←   ×− price
  We apply Conseq on (15), (16) and (14) and obtain (13)!
                                                                                             □

Lemma I.4 ( transfer satisfies 𝑆 2 ).

                 (2) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑡𝑟𝑛𝑠 , a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                          ×− Ids𝑡𝑟𝑛𝑠 }
                                        Account :: transfer.body
                                {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }

  Proof Outline
  To prove (2), we will need to prove that

                                                          , Vol. 1, No. 1, Article . Publication date: November 2025.
78                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble




                  (21?) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑡𝑟𝑛𝑠 , a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                             ×− Ids𝑡𝑟𝑛𝑠 }
                                             if (this.key==key’) then
                                               this.blnce:=this.blnce-amt
                                               dest.blnce:=dest.blnce+amt
                                             else
                                               res:=0
                                             res:=0
                                    {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }



     Using the underlying Hoare logic we can prove that no account’s key gets modified, namely



                         (22) 𝑀𝑔𝑜𝑜𝑑 ⊢𝑢𝑙 { A𝑡𝑟𝑛𝑠 , a : Account ∧ ⟨ a.key⟩⟩
                                                     if (this.key==key’) then
                                                        this.blnce:=this.blnce-amt
                                                        dest.blnce:=dest.blnce+amt
                                                     else
                                                        res:=0
                                                     res:=0
                                             {⟨⟨a.key⟩⟩ }



     Using (22) and [Prot-1], we obtain



                          (23) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑡𝑟𝑛𝑠 , a : Account ∧ 𝑧 = a.key}
                                                    if (this.key==key’) then
                                                       this.blnce:=this.blnce-amt
                                                       dest.blnce:=dest.blnce+amt
                                                    else
                                                       res:=0
                                                    res:=0
                                            {𝑧 = a.key}



     Using (23) and [Embed-UL], we obtain

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                    79




                        (24) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑡𝑟𝑛𝑠 , a : Account ∧ 𝑧 = a.key}
                                                if (this.key==key’) then
                                                    this.blnce:=this.blnce-amt
                                                    dest.blnce:=dest.blnce+amt
                                                else
                                                    res:=0
                                                res:=0
                                        {𝑧 = a.key} || {𝑧 = a.key}
  [Prot_Int] and the fact that 𝑧 is an int gives us that ⟨ a.key⟩⟩ −▽res. Using [Types], and
[Prot_Int] and [Conseq] on (24) we obtain (21?).
                                                                                           □
  We want to prove that this public method satisfies the specification 𝑆 2,𝑠𝑡𝑟𝑜𝑛𝑔 , namely
Lemma I.5 (set satisfies 𝑆 2 ).
                    (6) 𝑀 𝑓 𝑖𝑛𝑒 ⊢{ A𝑠𝑒𝑡 ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                               ×− Ids𝑠𝑒𝑡 }
                                           if (this.key==key’) then
                                             this.key:=key”
                                           else
                                             res:=0
                                           res:=0
                                   {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }
  Proof Outline We will be using the shorthand                       A2 ≜ a : Account, A𝑠𝑒𝑡 .

  To prove (6), we will use the Seqence rule, and we want to prove

                      (61?) 𝑀 𝑓 𝑖𝑛𝑒 ⊢{ A2 ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                 ×− Ids𝑠𝑒𝑡 }
                                                if (this.key==key’) then
                                                    this.key:=key”
                                                else
                                                    res:=0
                                        { A2 ∧ ⟨ a.key⟩⟩ } || {⟨⟨a.key⟩⟩ }
and that
                   (62?) 𝑀 𝑓 𝑖𝑛𝑒 ⊢{ A2 ∧ ⟨ a.key⟩⟩ }
                                               res:=0
                                    {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }
  (62?) follows from the types, and Prot-Int1 , the fact that a.key did not change, and Prot-1.

  We now want to prove (61?). For this, will apply the If-Rule. That is, we need to prove that

                                                             , Vol. 1, No. 1, Article . Publication date: November 2025.
80                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble




           (63?) 𝑀 𝑓 𝑖𝑛𝑒 ⊢{ A2 ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                      ×− Ids𝑠𝑒𝑡 ∧ this.key = key’ }
                                        this.key:=key”
                             {⟨⟨a.key⟩⟩ } || {⟨⟨a.key⟩⟩ }

     and that


           (64?) 𝑀 𝑓 𝑖𝑛𝑒 ⊢{ A2 ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                      ×− Ids𝑠𝑒𝑡 ∧ this.key ≠ key’ }
                                        res:=0
                             {⟨⟨a.key⟩⟩ } || {⟨⟨a.key⟩⟩ }

     (64?) follows easily from the fact that a.key did not change, and Prot-1.

  We look at the proof of (63?). We will apply the Cases rule, and distinguish on whether
a.key=this.key. That is, we want to prove that

(65?) 𝑀 𝑓 𝑖𝑛𝑒 ⊢{ A2 ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                           ×− Ids𝑠𝑒𝑡 ∧ this.key = key’ ∧ this.key = a.key}
                            this.key:=key”
                 {⟨⟨a.key⟩⟩ } || {⟨⟨a.key⟩⟩ }


and that


(66?) 𝑀 𝑓 𝑖𝑛𝑒 ⊢{ A2 ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                           ×− Ids𝑠𝑒𝑡 ∧ this.key = key’ ∧ this.key ≠ a.key’ }
                            this.key:=key”
                 {⟨⟨a.key⟩⟩     || {⟨⟨a.key⟩⟩ }

 We can prove (65?) through application of Absurd, ProtNeq, and Conseq, as follows


                                  (61c) 𝑀 𝑓 𝑖𝑛𝑒 ⊢{ 𝑓 𝑎𝑙𝑠𝑒}
                                                              this.key:=key”
                                                     {⟨⟨a.key⟩⟩ } || {⟨⟨a.key⟩⟩ }

     By ProtNeq, we have 𝑀 𝑓 𝑖𝑛𝑒 ⊢ ⟨ a.key⟩⟩←
                                            ×− key’ −→ a.key ≠ key’, and therefore obtain


(61d) 𝑀 𝑓 𝑖𝑛𝑒 ⊢ ... ∧ ⟨ a.key⟩⟩←
                               ×− Ids𝑠𝑒𝑡 ∧ this.key = a.key ∧ this.key = key’ −→ 𝑓 𝑎𝑙𝑠𝑒

     We apply Conseq on (61c) and (61d) and obtain (61aa?).

   We can prove (66?) by proving that this.key≠a.key implies that this ≠ a (by the underly-
ing Hoare logic), which again implies that the assignment this.key := ... leaves the value
of a.key unmodified. We apply Prot-1, and are done.
                                                                                         □

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                   81


I.3     Showing that 𝑀𝑏𝑎𝑑 does not satisfy 𝑆 2 nor 𝑆 3
I.3.1 𝑀𝑏𝑎𝑑 does not satisfy 𝑆 2 . 𝑀𝑏𝑎𝑑 does not satisfy 𝑆 2 . We can argue this semantically (as in
§I.3.2), and also in terms of the proof system (as in I.3.3).
I.3.2 𝑀𝑏𝑎𝑑 ⊭ 𝑆 2 . The reason is that 𝑀𝑏𝑎𝑑 exports the public method set, which updates the key
without any checks. So, it could start in a state where the key of the account was protected, and
then update it to something not protected.
    In more detail: Take any state 𝜎, where 𝑀𝑏𝑎𝑑 , 𝜎 |= 𝑎 0 : Account, 𝑘 0 : Key ∧ ⟨ 𝑎 0 .key⟩⟩ . Assume
also that 𝑀𝑏𝑎𝑑 , 𝜎 |= extl. Finally, assume that the continuation in 𝜎 consists of 𝑎 0 .set(𝑘 0 ).
Then we obtain that 𝑀𝑏𝑎𝑑 , 𝜎 {∗ 𝜎 ′ , where 𝜎 ′ = 𝜎 [𝑎 0 .key ↦→ 𝑘 0 ]. We also have that 𝑀𝑏𝑎𝑑 , 𝜎 ′ |=
extl, and because 𝑘 0 is a local variable, we also have that 𝑀𝑏𝑎𝑑 , 𝜎 ′ ⊭ ⟨𝑘 0 ⟩ . Moreover, 𝑀𝑏𝑎𝑑 , 𝜎 ′ |=
𝑎 0 .krey = 𝑘 0 . Therefore, 𝑀𝑏𝑎𝑑 , 𝜎 ′ ⊭ ⟨ 𝑎 0 .key⟩⟩ .
I.3.3 𝑀𝑏𝑎𝑑 ⊬ 𝑆 2 . In order to prove that 𝑀𝑏𝑎𝑑 ⊢ 𝑆 2 , we would have needed to prove, among other
things, that set satisfied 𝑆 2 , which means proving that

(ERR_1?) 𝑀𝑏𝑎𝑑 ⊢ { this : Account, k’ : Key, 𝑎 : Account ∧ ⟨ 𝑎.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                               ×− {this, k’} }
                               this.key:=k’;
                               res := 0
                     { ⟨ 𝑎.key⟩⟩ ∧ ⟨ 𝑎.key⟩⟩←
                                            ×− res } || {...}
   However, we cannot establish (ERR_1?). Namely, when we take the case where this = 𝑎, we would need
to establish, that


      (ERR_2?) 𝑀𝑏𝑎𝑑 ⊢ { this : Account, k’ : Key ∧ ⟨ this.key⟩⟩ ∧ ⟨ this.key⟩⟩←
                                                                              ×− {this, k’} }
                                  this.key:=k’
                        { ⟨ this.key⟩⟩ } || {...}
  And there is no way to prove (ERR_2?). In fact, (ERR_2?) is not sound, for the reasons outlined in §I.3.2.
I.3.4 𝑀𝑏𝑎𝑑 does not satisfy 𝑆 3 . We have already argued in Examples 2.3 and 6.5 that 𝑀𝑏𝑎𝑑 does not satisfy 𝑆 3 , by
giving a semantic argument – ie we are in state where ⟨ 𝑎 0 .key⟩⟩ , and execute a0 .set(k1); a0 .transfer(...k1).
    Moreover, if we attempted to prove that set satisfies 𝑆 3 , we would have to show that


               (ERR_3?) 𝑀𝑏𝑎𝑑 ⊢ { this : Account, k’ : Key, 𝑎 : Account, 𝑏 : int ∧
                                      ⟨ 𝑎.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                           ×− {this, k’} ∧ 𝑎.blnce ≥ 𝑏 }
                                              this.key:=k’;
                                              res := 0
                                    { ⟨ 𝑎.key⟩⟩ ∧ ⟨ 𝑎.key⟩⟩←
                                                           ×− res ∧ 𝑎.blnce ≥ 𝑏 } || {...}
  which, in the case of 𝑎 = this would imply that


          (ERR_4?) 𝑀𝑏𝑎𝑑 ⊢ { this : Account, k’ : Key, 𝑏 : int ∧
                               ⟨ this.key⟩⟩ ∧ ⟨ this.key⟩⟩←
                                                          ×− {this, k’} ∧ this.blnce ≥ 𝑏 }
                                       this.key:=k’
                             { ⟨ this.key⟩⟩ } || {...}
  And (ERR_4?) cannot be proven and does not hold.

                                                            , Vol. 1, No. 1, Article . Publication date: November 2025.
82                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


I.4     Demonstrating that 𝑀𝑔𝑜𝑜𝑑 ⊢ 𝑆 3 , and that 𝑀 𝑓 𝑖𝑛𝑒 ⊢ 𝑆 3
I.5     Extending the specification 𝑆 3
As in §I.2, we redefine 𝑆 3 so that it also describes the behaviour of method send. and have:

         𝑆 3,𝑠𝑡𝑟𝑜𝑛𝑔 ≜    𝑆 3 ∧ 𝑆 2𝑎 ∧ 𝑆 2𝑏

Lemma I.6 (module 𝑀𝑔𝑜𝑜𝑑 satisfies 𝑆 3,𝑠𝑡𝑟𝑜𝑛𝑔 ). 𝑀𝑔𝑜𝑜𝑑 ⊢ 𝑆 3,𝑠𝑡𝑟𝑜𝑛𝑔

      Proof Outline In order to prove that
                                    A
                           𝑀𝑔𝑜𝑜𝑑 ⊢ a : Account, 𝑏 : int.{ ⟨ a.key⟩⟩ ∧ a.blnce ≥ 𝑏 }

we have to apply Invariant from Fig. 8. That is, for each class 𝐶 defined in 𝑀𝑔𝑜𝑜𝑑 , and for each public method
𝑚 in 𝐶, with parameters 𝑦 : 𝐷, we have to prove that they satisfy the corresponding quadruples.
  Thus, we need to prove three Hoare quadruples: one for Shop::buy, one for Account::transfer,
and one for Account::set. That is, we have to prove that
 (31?) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑏𝑢𝑦 , a : Account, 𝑏 : int ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                    ×− Ids𝑏𝑢𝑦 ∧ a.blnce ≥ 𝑏 }
                               Shop :: buy.body
                        {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res ∧ a.blnce ≥ 𝑏} || {⟨⟨a.key⟩⟩ ∧ a.blnce ≥ 𝑏}
      (32?) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑡𝑟𝑛𝑠 , a : Account , 𝑏 : int ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                           ×− Ids𝑡𝑟𝑛𝑠 ∧ a.blnce ≥ 𝑏 }
                               Account :: transfer.body
                        {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res ∧ a.blnce ≥ 𝑏 } || {⟨⟨a.key⟩⟩ ∧ a.blnce ≥ 𝑏 }
      (33?) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑠𝑒𝑡 , a : Account , 𝑏 : int ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                          ×− Ids𝑠𝑒𝑡 ∧ a.blnce ≥ 𝑏 }
                               Account :: set.body
                        {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res ∧ a.blnce ≥ 𝑏 } || {⟨⟨a.key⟩⟩ ∧ a.blnce ≥ 𝑏 }

where we are using ? to indicate that this needs to be proven, and where we are using the shorthands
A𝑏𝑢𝑦 , Ids𝑏𝑢𝑦 , A𝑡𝑟𝑛𝑠 , Ids𝑡𝑟𝑛𝑠 , A𝑠𝑒𝑡 as defined earlier.
                                                                                                  □
      The proofs for 𝑀 𝑓 𝑖𝑛𝑒 are similar.
      We outline the proof of (31?) in Lemma I.7. We outline the proof of (32?) in Lemma I.8.

I.5.1    Proving that Shop::buy from 𝑀𝑔𝑜𝑜𝑑 satisfies 𝑆 3,𝑠𝑡𝑟𝑜𝑛𝑔 and also 𝑆 4 .

Lemma I.7 (function 𝑀𝑔𝑜𝑜𝑑 :: Shop :: buy satisfies 𝑆 3,𝑠𝑡𝑟𝑜𝑛𝑔 and also 𝑆 4 ).

      (31) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑏𝑢𝑦 , a : Account, 𝑏 : int, ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                         ×− Ids𝑏𝑢𝑦 ∧ a.blnce ≥ 𝑏 }
                               Shop :: buy.body
                        {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res ∧ a.blnce ≥ 𝑏} || {⟨⟨a.key⟩⟩ ∧ a.blnce ≥ 𝑏}

   Proof Outline Note that (31) is a proof that 𝑀𝑔𝑜𝑜𝑑 :: Shop :: buy satisfies 𝑆 3,𝑠𝑡𝑟𝑜𝑛𝑔 and also hat 𝑀𝑔𝑜𝑜𝑑 ::
Shop :: buy satisfies 𝑆 4 . This is so, because application of [Method] on 𝑆 4 gives us exactly the proof obligation
from (31).
   This proof is similar to the proof of lemma I.3, with the extra requirement here that we need to argue about
balances not decreasing. To do this, we will leverage the assertion about balances given in 𝑆 3 .
   We will use the shorthand A1 ≜ A𝑏𝑢𝑦 , a : Account, 𝑏 : int. We will split the proof into 1) proving that
statements 10, 11, 12 preserve the protection of a.key from the buyer, 2) proving that the external call
1st Step: proving statements 10, 11, 12
   We apply the underlying Hoare logic and prove that the statements on lines 10, 11, 12 do not affect the
value of a.key nor that of a.blnce. Therefore, for a 𝑧, 𝑧 ′ ∉ {price, myAccnt, oldBalance}, we have

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                               83




                       (40) 𝑀𝑔𝑜𝑜𝑑 ⊢𝑢𝑙 { A1 ∧ 𝑧 = a.key ∧ 𝑧 ′ = a.blnce}
                                                price:=anItem.price;
                                                myAccnt:=this.accnt;
                                                oldBalance := myAccnt.blnce;
                                        {𝑧 = a.key ∧ 𝑧 ′ = a.blnce}
  We then apply Embed_UL, Prot-1 and Prot-2 and Combine and and Types-2 on (10) and use the shorthand
stmts10,11,12 for the statements on lines 10, 11 and 12, and obtain:

                                                         ×− a.key ∧ 𝑧 ′ = a.blnce}
                 (41) 𝑀𝑔𝑜𝑜𝑑 ⊢{ A1 ∧ ⟨ a.key⟩⟩ ∧ ⟨ buyer⟩⟩←
                                        stmts10,11,12
                                                       ×− a.key ∧ 𝑧 ′ = a.blnce}
                                { ⟨ a.key⟩⟩ ∧ ⟨ buyer⟩⟩←
  We apply Mid on (11) and obtain
                                           ×− buyer ∧ 𝑧 ′ = a.blnce}
               (42) 𝑀𝑔𝑜𝑜𝑑 ⊢{ A1 ∧ ⟨ a.key⟩⟩←
                                      stmts10,11,12
                                                          ×− a.key ∧ 𝑧 ′ = a.blnce} ||
                              { A1 ∧ ⟨ a.key⟩⟩ ∧ ⟨ buyer⟩⟩←
                              { ⟨ a.key⟩⟩ ∧ 𝑧 ′ = a.blnce}

2nd Step: Proving the External Call
  We now need to prove that the external method call buyer.pay(this.accnt, price) protects the
key, and does nit decrease the balance, i.e.
                                                      ×− buyer ∧ 𝑧 ′ = a.blnce}
             (43?) 𝑀𝑔𝑜𝑜𝑑 ⊢{ A1 ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                    tmp := buyer.pay(myAccnt, price)
                                                        ×− a.key ∧ a.blnce ≥ 𝑧 ′ } ||
                            { A1 ∧ ⟨ a.key⟩⟩ ∧ ⟨ buyer⟩⟩←
                            { ⟨ a.key⟩⟩ ∧ a.blnce ≥ 𝑧 ′ }
                      A
  We use that 𝑀 ⊢ a : Account, b : int,.{⟨⟨a.key⟩⟩ ∧ a.blnce ≥ 𝑧 ′ } and obtain

                                                     ×− (buyer, myAccnt, price) ∧ 𝑧 ′ ≥ a.blnce}
(44) 𝑀𝑔𝑜𝑜𝑑 ⊢{ buyer : external, ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                      tmp := buyer.pay(myAccnt, price)
                                     ×− (buyer, myAccnt, price) ∧ 𝑧 ′ ≥ a.blnce} ||
              { ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
              { ⟨ a.key⟩⟩ ∧ 𝑧 ′ ≥ a.blnce}
    In order to obtain (43?) out of (44), we use the type system and type declarations and obtain that
all objects transitively reachable from myAccnt or price are scalar or internal. Thus, we apply
Prot-Intl, and obtain
      (45)     𝑀𝑔𝑜𝑜𝑑 ⊢ A1 ∧ ⟨ a.key⟩⟩ −→ ⟨ a.key⟩⟩←       ×− myAccnt
      (46)     𝑀𝑔𝑜𝑜𝑑 ⊢ A1 ∧ ⟨ a.key⟩⟩ −→ ⟨ a.key⟩⟩←       ×− price
      (47)     𝑀𝑔𝑜𝑜𝑑 ⊢ A1 ∧ 𝑧 ′ = a.blnce −→ 𝑧 ′ ≥ a.blnce
    We apply Conseq on (44), (45), (46) and (47) and obtain (43)!
3nd Step: Proving the Remainder of the Body
    We now need to prove that lines 15-19 of the method preserve the protection of a.key, and do
not decrease a.balance. We outline the remaining proof in less detail.
    We prove the internal call on line 16, using the method specification for send, using 𝑆 2𝑎 and
𝑆 2𝑏 , and applying rule [Call_Int], and obtain

                                                        , Vol. 1, No. 1, Article . Publication date: November 2025.
84                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble




                                                                     ×− (buyer ∧ 𝑧 ′ = a.blnce}
(48) 𝑀𝑔𝑜𝑜𝑑 ⊢ { buyer : external, item : Intem ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                         tmp := this.send(buyer,Item)
                                        ×− buyer ∧ 𝑧 ′ = a.blnce} ||
                 { ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                 { ⟨ a.key⟩⟩ ∧ 𝑧 ′ = a.blnce}

   We now need to prove that the external method call buyer.tell("You have not paid me")
also protects the key, and does nit decrease the balance. We can do this by applying the rule about
protection from strings [Pror_Str], the fact that 𝑀𝑔𝑜𝑜𝑑 ⊢ 𝑆 3 , and rule [Call_Extl_Adapt] and
obtain:


                                                                     ×− (buyer ∧ 𝑧 ′ /𝑔𝑒𝑞a.blnce}
(49) 𝑀𝑔𝑜𝑜𝑑 ⊢ { buyer : external, item : Intem ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                         tmp:=buyer.tell("You have not paid me")
                                        ×− buyer ∧ 𝑧 ′ ≥ a.blnce} ||
                 { ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                 { ⟨ a.key⟩⟩ ∧ 𝑧 ′ ≥ a.blnce}

     We can now apply [If_Rule, and [Conseq on (49) and (50), and obtain


                                                                     ×− (buyer ∧ 𝑧 ′ ≥ a.blnce}
(50) 𝑀𝑔𝑜𝑜𝑑 ⊢ { buyer : external, item : Intem ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                         if...then
                          tmp:=this.send(buyer,anItem)
                         else
                          tmp:=buyer.tell("You have not paid me")
                                        ×− buyer ∧ 𝑧 ′ ≥ a.blnce} ||
                 { ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                 { ⟨ a.key⟩⟩ ∧ 𝑧 ′ ≥ a.blnce}

     The rest follows through application of [Prot_Int, and [Seq].
                                                                                                                   □
Lemma I.8 (function 𝑀𝑔𝑜𝑜𝑑 :: Account :: transfer satisfies 𝑆 3 ).

     (32) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑡𝑟𝑛𝑠 , a : Account , 𝑏 : int ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                         ×− Ids𝑡𝑟𝑛𝑠 ∧ a.blnce ≥ 𝑏 }
                            Account :: transfer.body
                    {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res ∧ a.blnce ≥ 𝑏 } || {⟨⟨a.key⟩⟩ ∧ a.blnce ≥ 𝑏 }

   Proof Outline We will use the shorthand 𝑠𝑡𝑚𝑡𝑠 28−33 for the statements in the body of transfer. We
will prove the preservation of protection, separately from the balance not decreasing when the key is protcted.
   For the former, applying the steps in the proof of Lemma I.4, we obtain


                  (21) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑡𝑟𝑛𝑠 , a : Account ∧ ⟨ a.key⟩⟩ ∧ ⟨ a.key⟩⟩←
                                                                            ×− Ids𝑡𝑟𝑛𝑠 }
                                            𝑠𝑡𝑚𝑡𝑠 28−33
                                   {⟨⟨a.key⟩⟩ ∧ ⟨ a.key⟩⟩ −▽res} || {⟨⟨a.key⟩⟩ }

  For the latter, we rely on the underlying Hoare logic to ensure that no balance decreases, except
perhaps that of the receiver, in which case its key was not protected. Namely, we have that

, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                    85




        (71) 𝑀𝑔𝑜𝑜𝑑 ⊢𝑢 𝑙 { A𝑡𝑟𝑛𝑠 , a : Account ∧ a.blnce = 𝑏 ∧ (this ≠ a ∨ 𝑝𝑟𝑔𝑡ℎ𝑖𝑠.key ≠ key′ ) }
                                 𝑠𝑡𝑚𝑡𝑠 28−33
                         {a.blnce ≥ 𝑏}

      We apply rules Embed_UL and Mid on (71), and obtain

         (72) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑡𝑟𝑛𝑠 , a : Account ∧ a.blnce = 𝑏 ∧ (this ≠ a ∨ 𝑝𝑟𝑔𝑡ℎ𝑖𝑠.key ≠ key′ ) }
                                𝑠𝑡𝑚𝑡𝑠 28−33
                        {a.blnce ≥ 𝑏} || {a.blnce ≥ 𝑏}

      Moreover, we have
       (73)    𝑀𝑔𝑜𝑜𝑑 ⊢ ⟨ a.key⟩⟩←       ×− Ids𝑡𝑟𝑛𝑠 → ⟨ a.key⟩⟩←
                                                              ×− key’
       (74)    𝑀𝑔𝑜𝑜𝑑 ⊢ ⟨ a.key⟩⟩←       ×− key’ → a.key ≠ key’
       (75)    𝑀𝑔𝑜𝑜𝑑 ⊢ a.key ≠ key’ → a ≠ this ∨ this.key ≠ key′
      normalsize
      Applying (73), (74), (75) and Conseq on (72) we obtain:


                (76) 𝑀𝑔𝑜𝑜𝑑 ⊢ { A𝑡𝑟𝑛𝑠 , a : Account ∧ a.blnce = 𝑏 ∧ ⟨ a.key⟩⟩←
                                                                            ×− Ids𝑡𝑟𝑛𝑠 }
                                       𝑠𝑡𝑚𝑡𝑠 28−33
                               {a.blnce ≥ 𝑏} || {a.blnce ≥ 𝑏}

      We combine (72) and (76) through Combine and obtain (32).
                                                                                                                     □

I.6     Dealing with polymorphic function calls
The case split rules together with the rule of consequence allow our Hoare logic to formally reason about
polymorphic calls, where the receiver may be internal or external.
   We demonstrate this through an example where we may have an external receiver, or a receiver from a
class 𝐶. Assume we had a module 𝑀 with a scoped invariant (as in A), and an internal method specification as
in (B).
                         A
        (𝐴) 𝑀 ⊢         𝑦1 : 𝐷.{𝐴}
        (𝐵) 𝑀 ⊢ { 𝐴1 } p 𝐶 ::𝑚(𝑦1 : 𝐷) { 𝐴2 }∥ {𝐴3 }

Here p may be private or ublic; the argument apples either way.
Assume also implications as in (C)-(H)
     (𝐶) 𝑀 ⊢ 𝐴0 → 𝐴−▽(𝑦0, 𝑦1 )
     (𝐷) 𝑀 ⊢ 𝐴−▽(𝑦0, 𝑦1 ) → 𝐴4
     (𝐸) 𝑀 ⊢ 𝐴 → 𝐴5
     (𝐹 ) 𝑀 ⊢ 𝐴0 → 𝐴1 [𝑦0 /this]
     (𝐺) 𝑀 ⊢ 𝐴2 [𝑦0, 𝑢/this, 𝑟𝑒𝑠] → 𝐴4
     (𝐻 ) 𝑀 ⊢ 𝐴3 → 𝐴5
  Then, by application of Call_Ext_Adapt on (A) we obtain (I)
         (𝐼 ) 𝑀 ⊢ { 𝑦0 : 𝑒𝑥𝑡𝑒𝑟𝑛𝑎𝑙, 𝑦1 : 𝐷 ∧ 𝐴−▽(𝑦0, 𝑦1 ) } 𝑢 := 𝑦0 .𝑚(𝑦1 ) { 𝐴−▽(𝑦0, 𝑦1 ) } ∥ { 𝐴 }

      By application of the rule of consequence on (I) and (C), (D), and (E), we obtain
             (𝐽 ) 𝑀 ⊢ { 𝑦0 : 𝑒𝑥𝑡𝑒𝑟𝑛𝑎𝑙, 𝑦1 : 𝐷 ∧ 𝐴0 } 𝑢 := 𝑦0 .𝑚(𝑦1 ) { 𝐴4 } ∥ { 𝐴5 }

      Then, by application of [Call_Intl] on (B) we obtain (K)

                                                             , Vol. 1, No. 1, Article . Publication date: November 2025.
86                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


            (𝐾) 𝑀 ⊢ { 𝑦0 : 𝐶, 𝑦1 : 𝐷 ∧ 𝐴1 [𝑦0 /this] } 𝑢 := 𝑦0 .𝑚(𝑦1 ) { 𝐴2 [𝑦0, 𝑢/this, 𝑟𝑒𝑠] } ∥ { 𝐴3 }

     By application of the rule of consequence on (K) and (F), (G), and (H), we obtain
            (𝐿) 𝑀 ⊢ { 𝑦0 : 𝐶, 𝑦1 : 𝐷 ∧ 𝐴0 } 𝑢 := 𝑦0 .𝑚(𝑦1 ) { 𝐴4 } ∥ { 𝐴5 }

     By case split, [Cases], on (J) and (L), we obtain
            (𝑝𝑜𝑙𝑦𝑚𝑜𝑝𝑟ℎ𝑖𝑐) 𝑀 ⊢ { (𝑦0 : 𝑒𝑥𝑡𝑒𝑟𝑛𝑎𝑙 ∨ 𝑦0 : 𝐶), 𝑦1 : 𝐷 ∧ 𝐴0 } 𝑢 := 𝑦0 .𝑚(𝑦1 ) { 𝐴4 } ∥ { 𝐴5 }



References
  [1] Gul Agha and Carl Hewitt. 1987. Actors: A Conceptual Foundation for Concurrent Object-Oriented Programming. In
      Research Directions in Object-Oriented Programming, Bruce D. Shriver and Peter Wegner (Eds.). MIT Press, 49–74.
  [2] Elvira Albert, Shelly Grossman, Noam Rinetzky, Clara Rodríguez-Núñez, Albert Rubio, and Mooly Sagiv. 2023. Relaxed
      Effective Callback Freedom: A Parametric Correctness Condition for Sequential Modules With Callbacks. IEEE Trans.
      Dependable Secur. Comput. 20, 3 (2023), 2256–2273. https://doi.org/10.1109/TDSC.2022.3178836
  [3] Sean Noble Anderson, Roberto Blanco, Leonidas Lampropoulos, Benjamin C. Pierce, and Andrew Tolmach. 2023.
      Formalizing Stack Safety as a Security Property. In Computer Security Foundations Symposium. 356–371. doi:10.1109/
      CSF57540.2023.00037
  [4] Cezar-Constantin Andrici, Ştefan Ciobâcă, Catalin Hritcu, Guido Martínez, Exequiel Rivas, Éric Tanter, and Théo
      Winterhalter. 2024. Securing Verified IO Programs Against Unverified Code in F. POPL 8 (2024), 2226–2259. https:
      //doi.org/10.1145/3632916
  [5] Arnold Beckmann and Anton Setzer. [n. d.]. Access Hoare Logic. retrieved Novemebr 2025.
  [6] Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J. Summers. 2019. Leveraging Rust types for modular
      specification and verification. OOPSLA 3 (2019), 147:1–147:30. https://doi.org/10.1145/3360573
  [7] Anindya Banerjee and David A. Naumann. 2005. Ownership Confinement Ensures Representation Independence for
      Object-oriented Programs. J. ACM 52, 6 (Nov. 2005), 894–960. doi:10.1145/1101821.1101824
  [8] Yuyan Bao, Guannan Wei, Oliver Bracevac, Yuxuan Jiang, Qiyang He, and Tiark Rompf. 2021. Reachability types:
      tracking aliasing and separation in higher-order functional programs. OOPSLA 5 (2021), 1–32. https://doi.org/10.
      1145/3485516
  [9] Michael Barnett, Robert DeLine, Manuel Fähndrich, K. Rustan M. Leino, and Wolfram Schulte. 2004. Verification of
      Object-Oriented Programs with Invariants. J. Object Technol. 3, 6 (2004), 27–56. doi:10.5381/JOT.2004.3.6.A2
 [10] Mike Barnett, Rustan Leino, and Wolfram Schulte. 2005. The Spec♯ Programming System: An Overview. In CASSIS,
      Vol. LNCS3362. 49–69. doi:10.1007/978-3-540-30569-9_3
 [11] Jesper Bengtson, Kathiekeyan Bhargavan, Cedric Fournet, Andrew Gordon, and S.Maffeis. 2011. Refinement Types
      for Secure Implementations. TOPLAS (2011), 1– 45. https://doi.org/10.1145/1890028.1890031
 [12] Andrew Black, Kim Bruce, Michael Homer, and James Noble. 2012. Grace: the Absence of (Inessential) Difficulty. In
      Onwards. 85–98. https://doi.org/10.1145/2384592.2384601
 [13] Aleksander Boruch-Gruszecki, Martin Odersky, Edward Lee, Ondrej Lhoták, and Jonathan Immanuel Brachthäuser.
      2023. Capturing Types. TOPLAS 45, 4 (2023), 21:1–21:52. https://doi.org/10.1145/3618003
 [14] Chandrasekhar Boyapati, Barbara Liskov, and Liuba Shrira. 2003. Ownership types for object encapsulation. In POPL.
      213–223. doi:10.1145/604131.604156
 [15] John Boyland. 2001. Alias burying: Unique variables without destructive reads. In S:P&E. 533–553. https://doi.org/10.
      1002/spe.370
 [16] Gilad Bracha. 2015. The Dart Programming Language. Addison-Wesley. 224 pages. https://dart.dev
 [17] Gilad Bracha. 2017. The Newspeak Language Specification Version 0.1. (Feb. 2017). https://newspeaklanguage.org/
 [18] Jonathan Immanuel Brachthäuser, Philipp Schuster, Edward Lee, and Aleksander Boruch-Gruszecki. 2022. Effects,
      capabilities, and boxes: from scope-based reasoning to type-based reasoning and back. OOPSLA 6 (2022), 1–30.
      https://doi.org/10.1145/3527320
 [19] Christian Bräm, Marco Eilers, Peter Müller, Robin Sierra, and Alexander J. Summers. 2021. Rich specifications for
      Ethereum smart contract verification. OOPSLA 5 (2021), 1–30. https://doi.org/10.1145/3485523
 [20] Anton Burtsev, David Johnson, Josh Kunz, Eric Eide, and Jacobus E. van der Merwe. 2017. CapNet: security and least
      authority in a capability-enabled cloud. In SoCC. 128–141. doi:10.1145/3127479.3131209
 [21] Nicholas Cameron, Sophia Drossopoulou, and James Noble. 2013. Understanding Ownership Types with Dependent
      Types. In Aliasing in Object-Oriented Programming. Types, Analysis and Verification. 84–108. https://doi.org/10.1007/
      978-3-642-36946-9_5


, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                        87


 [22] Franck Cassez, Joanne Fuller, and Horacio Mijail Anton Quiles. 2024. Deductive verification of smart contracts with
      Dafny. Int. J. Softw. Tools Technol. Transf. 26, 2 (2024), 131–145. doi:10.1007/S10009-024-00738-1
 [23] Patrice Chalin, Joseph R. Kiniry, Gary T. Leavens, and Erik Poll. 2005. Beyond Assertions: Advanced Specification
      and Verification with JML and ESC/Java2. In FMCO. 342–363. https://doi.org/10.1007/11804192_16
 [24] Edwin C. Chan, John Boyland, and William L. Scherlis. 1998. Promises: Limited Specifications for Analysis and
      Manipulation. In ICSE. 167–176. https://doi.org/10.1109/ICSE.1998.671113
 [25] Christoph Jentsch. 2016. Decentralized Autonomous Organization to automate governance. (March 2016). https:
      //download.slock.it/public/DAO/WhitePaper.pdf
 [26] David G. Clarke, John M. Potter, and James Noble. 1998. Ownership Types for Flexible Alias Protection. In OOPSLA.
      48– 64. https://doi.org/10.1145/286936.286947
 [27] David G. Clarke, John M. Potter, and James Noble. 2001. Simple Ownership Types for Object Containment. In ECOOP.
      53–76. https://doi.org/10.1007/3-540-45337-7_4
 [28] Ernie Cohen, Michal Moskal, Wolfram Schulte, and Stephan Tobies. 2010. Local Verification of Global Invariants in
      Concurrent Programs. In CAV. 480–494. https://doi.org/10.1007/978-3-642-14295-6_42
 [29] David R. Cok and K. Rustan M. Leino. 2022. Specifying the Boundary Between Unverified and Verified Code. Chapter 6,
      105–128. doi:10.1007/978-3-031-08166-8_6
 [30] Joseph W. Cutler, Craig Disselkoen, Aaron Eline, Shaobo He, Kyle Headley, Michael Hicks, Kesha Hietala, Eleftherios
      Ioannidis, John H. Kastner, Anwar Mamat, Darin McAdams, Matt McCutchen, Neha Rungta, Emina Torlak, and
      Andrew Wells. 2024. Cedar: A New Language for Expressive, Fast, Safe, and Analyzable Authorization. 8, OOPSLA1
      (2024), 670–697. https://doi.org/10.1145/3649835
 [31] Thibault Dardinier and Peter Müller. 2024. Hyper Hoare Logic: (Dis-)Proving Program Hyperproperties. In PLDI,
      Vol. 8. 1485–1509. doi:10.1145/3656437
 [32] Brooks Davis, Robert N. M. Watson, Alexander Richardson, Peter G. Neumann, Simon W. Moore, John Baldwin,
      David Chisnall, James Clarke, Nathaniel Wesley Filardo, Khilan Gudka, Alexandre Joannou, Ben Laurie, A. Theodore
      Markettos, J. Edward Maste, Alfredo Mazzinghi, Edward Tomasz Napierala, Robert M. Norton, Michael Roe, Peter
      Sewell, Stacey Son, and Jonathan Woodruff. 2019. CheriABI: Enforcing Valid Pointer Provenance and Minimizing
      Pointer Privilege in the POSIX C Run-time Environment. In ASPLOS. 379–393. https://doi.org/10.1145/3297858.3304042
 [33] J. Dedecker, T. Van Cutsem, S. Mostinckx, T. D’Hondt, and W. De Meuter. 2006. Ambient-Oriented Programming in
      AmbientTalk. In ECOOP. 230–254. https://doi.org/10.1007/11785477_16
 [34] Dominique Devriese, Lars Birkedal, and Frank Piessens. 2016. Reasoning about Object Capabilities with Logical
      Relations and Effect Parametricity. In IEEE EuroS&P. 147–162. doi:10.1109/EuroSP.2016.22
 [35] W. Dietl, S. Drossopoulou, and P. Müller. 2007. Generic Universe Types. In ECOOP (LNCS, Vol. 4609). Springer, 28–53.
      http://www.springerlink.com
 [36] Werner Dietl, Sophia Drossopoulou, and Peter Müller. 2007. Generic Universe Types. In ECOOP, Vol. 4609. 28–53.
      https://doi.org/10.1007/978-3-540-73589-2_3
 [37] W. Dietl and P. Müller. 2005. Universes: Lightweight Ownership for JML. JOT 4, 8 (October 2005), 5–32. https:
      //doi.org/10.5381/jot.2005.4.8.a1
 [38] Christos Dimoulas, Scott Moore, Aslan Askarov, and Stephen Chong. 2014. Declarative Policies for Capability Control.
      In Computer Security Foundations Symposium (CSF). 3–17. https://doi.org/10.1109/CSF.2014.9
 [39] Mike Dodds, Xinyu Feng, Matthew Parkinson, and Viktor Vafeiadis. 2009. Deny-guarantee reasoning. In ESOP.
      363–377. https://doi.org/10.1007/978-3-642-00590-9_26
 [40] Emanuele D’Osualdo, Azadeh Farzan, and Derek Dreyer. 2022. Proving hypersafety compositionally. Proc. ACM
      Program. Lang. 6, OOPSLA2 (2022), 289–314. https://doi.org/10.1145/3563298
 [41] S. Drossopoulou, A. Francalanza, P. Müller, and A. J. Summers. 2008. A Unified Framework for Verification Techniques
      for Object Invariants. In ECOOP. 412–437. https://doi.org/10.1007/978-3-540-70592-5_18
 [42] Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble. 2025. Reasoning about External Calls. Proc.
      ACM Program. Lang. 9, OOPSLA2 (2025). doi:10.1145/3763064
 [43] Sophia Drossopoulou and James Noble. 2013. The need for capability policies. In FTfJP. 61–67. doi:10.1145/2489804.
      2489811
 [44] Sophia Drossopoulou, James Noble, Julian Mackay, and Susan Eisenbach. 2020. Holistic Specifications for Robust
      Programs. In FASE. 420–440. doi:10.1007/978-3-030-45234-6_21
 [45] Sophia Drossopoulou, James Noble, Mark Miller, and Toby Murray. 2016. Permission and Authority revisited –
      towards a formalization. In (FTfJP). 1 – 6. http://dl.acm.org/citation.cfm?id=2955821
 [46] J. C Filliatre, L. Gondelman, and A Pakevichl. 2016. The spirit of ghost code. In Formal Methods System Design. 1–16.
      https://doi.org/10.1007/978-3-319-08867-9_1
 [47] Robert Bruce Findler and Matthias Felleisen. 2001. Contract Soundness for object-oriented languages. In OOPSLA.
      1–15. doi:10.1145/504282.504283


                                                                 , Vol. 1, No. 1, Article . Publication date: November 2025.
88                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


 [48] Robert W. Floyd. 1967. Assigning Meanings to Programs. Marhematical Aspects of Computer Science 19 (1967), 19–32.
      https://people.eecs.berkeley.edu/~necula/Papers/FloydMeaning.pdf
 [49] Aïna Linn Georges, Armaël Guéneau, Thomas Van Strydonck, Amin Timany, Alix Trieu, Dominique Devriese, and
      Lars Birkedal. 2024. Cerise: Program Verification on a Capability Machine in the Presence of Untrusted Code. J. ACM
      71, 1 (2024), 3:1–3:59. https://doi.org/10.1145/3623510
 [50] Shelly Grossman, Ittai Abraham, Guy Golan-Gueta, Yan Michalevsky, Noam Rinetzky, Mooly Sagiv, and Yoni Zohar.
      2018. Online Detection of Effectively Callback Free Objects with Applications to Smart Contracts. POPL (2018).
      doi:10.1145/3158136
 [51] Philipp Haller. 2024. Lightweight Affine Types for Safe Concurrency in Scala (Keynote). In Programming. https:
      //doi.org/10.1145/3660829.3661033 https://speakerdeck.com/phaller/towards-safer-lightweight-concurrency-in-scala.
 [52] Philipp Haller and Alexander Loiko. 2016. LaCasa: lightweight affinity and object capabilities in Scala. In OOPSLA.
      272–291. doi:10.1145/2983990.2984042
 [53] Ian J. Hayes and Cliff B. Jones. 2018. A Guide to Rely/Guarantee Thinking. In SETSS 2017. 1–38. https://doi.org/10.
      1007/978-3-030-02928-9_1
 [54] Ian J. Hayes, Xi Wu, and Larissa A. Meinicke. 2017. Capabilities for Java: Secure Access to Resources. In APLAS.
      67–84. doi:10.1007/978-3-319-71237-6_4
 [55] Trent Hill, James Noble, and John Potter. 2002. Scalable Visualizations of Object-Oriented Systems with Ownership
      Trees. J. Vis. Lang. Comput. 13, 3 (2002), 319–339. https://doi.org/10.1006/jvlc.2002.0238
 [56] C. A. R. Hoare. 1969. An Axiomatic Basis for Computer Programming. Comm. ACM 12 (1969), 576–580. https:
      //doi.org/10.1145/363235.363259
 [57] C. A. R. Hoare. 1974. Monitors: an operating system structuring concept. Commun. ACM 17, 10 (1974), 549–557.
      https://doi.org/10.1145/355620.361161
 [58] Atsushi Igarashi, Benjamin C. Pierce, and Philip Wadler. 2001. Featherweight Java: a minimal core calculus for Java
      and GJ. ACM ToPLAS 23, 3 (2001), 396–450. doi:10.1145/503502.503505
 [59] S. S. Ishtiaq and P. W. O’Hearn. 2001. BI as an assertion language for mutable data structures. In POPL. 14–26.
      https://doi.org/10.1145/360204.375719
 [60] Timothy Jones, Michael Homer, James Noble, and Kim B. Bruce. 2016. Object Inheritance Without Classes. In ECOOP.
      13:1–13:26. doi:10.4230/LIPIcs.ECOOP.2016.13
 [61] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. RustBelt: Securing the Foundations of
      the Rust Programming Language. 2, POPL (2017), 66:1–66:34. https://doi.org/10.1145/3158154
 [62] Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and Derek Dreyer. 2018. Iris from the
      ground up: A modular foundation for higher-order concurrent separation logic. J. Funct. Program. 28 (2018), e20.
      https://doi.org/10.1017/S0956796818000151
 [63] Steve Klabnik and Carol Nichols. 2018. The Rust Programming Language (2nd ed.). No Starch Press. https://doc.rust-
      lang.org/book/
 [64] Alexander Kogtenkov, Bertrand Meyer, and Sergey Velder. 2015. Alias calculus, change calculus and frame inference.
      Sci. Comp. Prog. 97 (2015), 163–172. https://doi.org/10.1016/j.scico.2013.11.006
 [65] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno,
      and Chris Hawblitzel. 2023. Verus: Verifying Rust Programs using Linear Ghost Types. In OOPSLA, Vol. 7. 286–315.
      https://doi.org/10.1145/3586037
 [66] Dirk Leinenbach and Thomas Santen. 2009. Verifying the Microsoft Hyper-V Hypervisor with VCC. In Formal Methods.
      806–809. https://doi.org/10.1007/978-3-642-05089-3_51
 [67] K. R. M. Leino and P. Müller. 2004. Object Invariants in Dynamic Contexts. In ECOOP. 491–516. https://doi.org/10.
      1007/978-3-540-24851-4_22
 [68] K. Rustan M. Leino and Wolfram Schulte. 2007. Using History Invariants to Verify Observers. In ESOP. 80–94.
      https://doi.org/10.1007/978-3-540-71316-6_7
 [69] Henry M. Levy. 1984. Capability-Based Computer Systems. Butterworth-Heinemann. https://homes.cs.washington.
      edu/~levy/capabook/
 [70] Barbara Liskov and Jeanette Wing. 1994. A Behavioral Notion of Subtyping. ACM ToPLAS 16, 6 (1994), 1811–1841.
      https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf
 [71] Zongyuan Liu, Sergei Stepanenko, Jean Pichon-Pharabod, Amin Timany, Aslan Askarov, and Lars Birkedal. 2023.
      VMSL: A Separation Logic for Mechanised Robust Safety of Virtual Machines Communicating above FF-A. 7, PLDI
      (2023), 1438–1462. https://doi.org/10.1145/3591279
 [72] Anton Lorenzen, Stephen Dolan, Richard A. Eisenberg, and Sam Lindley. 2024. Oxidizing OCaml with Modal Memory
      Management. In ICFP. 448–475. https://doi.org/10.1145/3674642
 [73] Y. Lu and J. Potter. 2006. Protecting Representation with Effect Encapsulation.. In POPL. 359–371. https://dl.acm.org/
      doi/10.1145/1111320.1111069


, Vol. 1, No. 1, Article . Publication date: November 2025.
Reasoning about External Calls – Extended Version                                                                        89


 [74] Matthew Lutze, Magnus Madsen, Philipp Schuster, and Jonathan Immanuel Brachthäuser. 2023. With or Without
      You: Programming with Effect Exclusion. ICFP (2023), 448–475. doi:10.1145/3607846
 [75] Julian Mackay. 2025. Reasoning about External Calls - Coq Model. doi:10.5281/zenodo.16925157
 [76] Julian Mackay, Susan Eisenbach, James Noble, and Sophia Drossopoulou. 2022. Necessity Specifications for Robustness.
      Proc. ACM Program. Lang. 6, OOPSLA2, 811–840. doi:10.1145/3563317
 [77] Daniel Marshall and Dominic Orchard. 2024. Functional Ownership through Fractional Uniqueness. In OOPSLA.
      1040–1070. doi:10.1145/3649848
 [78] Yusuke Matsushita, Xavier Denis, Jacques-Henri Jourdan, and Derek Dreyer. 2022. RustHornBelt: a semantic
      foundation for functional verification of Rust programs with unsafe code. In PLDI. ACM, 841–856. https://dl.acm.org/
      doi/10.1145/3519939.3523704
 [79] Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. 2021. RustHorn: CHC-based Verification for Rust
      Programs. TOPLAS (2021), 15:1–15:54. https://doi.org/10.1145/3462205
 [80] Darya Melicher, Yangqingwei Shi, Alex Potanin, and Jonathan Aldrich. 2017. A Capability-Based Module System for
      Authority Control. In ECOOP. 20:1–20:27. doi:10.4230/LIPIcs.ECOOP.2017.20
 [81] Adrian Mettler, David Wagner, and Tyler Close. 2010. Joe-E a Security-Oriented Subset of Java. In NDSS. 357–374.
      https://www.ndss-symposium.org/ndss2010/joe-e-security-oriented-subset-java
 [82] Bertrand Meyer. 1992. Applying "Design by Contract". Computer 25, 10 (1992), 40–51. https://doi.org/10.1109/2.161279
 [83] B. Meyer. 1992. Eiffel: The Language. Prentice Hall.
 [84] Mark Samuel Miller. 2006. Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control.
      Ph. D. Dissertation. Johns Hopkins University, Baltimore, Maryland. https://papers.agoric.com/assets/pdf/papers/
      robust-composition.pdf
 [85] Mark Samuel Miller. 2011. Secure Distributed Programming with Object-capabilities in JavaScript. (Oct. 2011). Talk
      at Vrije Universiteit Brussel, mobicrant-talks.eventbrite.com.
 [86] Mark Samuel Miller, Tom Van Cutsem, and Bill Tulloh. 2013. Distributed Electronic Rights in JavaScript. In ESOP.
      1–20. https://doi.org/10.1007/978-3-642-37036-6_1
 [87] Mark Samuel Miller, Chip Morningstar, and Bill Frantz. 2000. Capability-based Financial Instruments: From Object to
      Capabilities. In Financial Cryptography. 349–378. https://doi.org/10.1007/3-540-45472-1_24
 [88] Nick Mitchell. 2006. The Runtime Structure of Object Ownership. In ECOOP. 74–98. https://doi.org/10.1007/11785477_5
 [89] Scott Moore, Christos Dimoulas, Robert Bruce Findler, Matthew Flatt, and Stephen Chong. 2016. Extensible access
      control with authorization contracts. In OOPSLA. 214–233. https://doi.org/10.1145/2983990.2984021
 [90] James H. Morris Jr. 1973. Protection in Programming Languages. CACM 16, 1 (1973), 15–21. https://doi.org/10.1145/
      361932.361937
 [91] P. Müller, A. Poetzsch-Heffter, and G. T. Leavens. 2006. Modular Invariants for Layered Object Structures. Science of
      Computer Programming 62 (2006), 253–286. https://doi.org/10.1016/j.scico.2006.03.001
 [92] Toby Murray. 2010. Analysing the Security Properties of Object-Capability Patterns. Ph. D. Dissertation. University of
      Oxford. http://ora.ox.ac.uk/objects/uuid:98b0b6b6-eee1-45d5-b32e-d98d1085c612
 [93] Takashi Nakayama, Yusuke Matsushita, Ken Sakayori, Ryosuke Sato, and Naoki Kobayashi. 2024. Borrowable
      Fractional Ownership Types for Verification. In VMCAI. 224–246. https://doi.org/10.1007/978-3-031-50521-8_11
 [94] James Noble, John Potter, and Jan Vitek. 1998. Flexible Alias Protection. In ECOOP. 158–185. https://doi.org/10.1007/
      BFb0054091
 [95] Peter W. O’Hearn. 2019. Incorrectness Logic. 4, POPL (2019), 1–32. doi:10.1145/3371078
 [96] Leo Osvald, Grégory M. Essertel, Xilun Wu, Lilliam I. González Alayón, and Tiark Rompf. 2016. Gentrification gone
      too far? affordable 2nd-class values for fun and (co-)effect. In OOPSLA. 234–251.
 [97] M. Parkinson and G. Bierman. 2005. Separation logic and abstraction. In POPL. 247–258. https://doi.org/10.1145/
      1040305.1040326
 [98] Anton Permenev, Dimitar Dimitrov, Petar Tsankov, Dana Drachsler-Cohen, and Martin Vechev. 2020. VerX: Safety
      Verification of Smart Contracts. In IEEE Symp. on Security and Privacy. 1661–1677. https://doi.org/10.1109/SP40000.
      2020.00024
 [99] John Potter, James Noble, and David G. Clarke. 1998. The Ins and Outs of Objects. In Australian Software Engineering
      Conference. 80–89. https://doi.org/10.1109/ASWEC.1998.730915
[100] Xiaojia Rao, Aïna Linn Georges, Maxime Legoupil, Conrad Watt, Jean Pichon-Pharabod, Philippa Gardner, and
      Lars Birkedal. 2023. Iris-Wasm: Robust and Modular Verification of WebAssembly Programs. In PLDI. 1096 – 1120.
      https://doi.org/10.1145/3591265
[101] Xiaojia Rao, Aïna Linn Georges, Maxime Legoupil, Conrad Watt, Jean Pichon-Pharabod, Philippa Gardner, and Lars
      Birkedal. 2023. Iris-Wasm: Robust and Modular Verification of WebAssembly Programs. PLDI 7 (2023), 1096–1120.
      https://doi.org/10.1145/3591265



                                                                 , Vol. 1, No. 1, Article . Publication date: November 2025.
90                                               Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble


[102] J. C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In LICS. IEEE Computer Society,
      55–74. https://doi.org/10.1109/LICS.2002.1029817
[103] Dustin Rhodes, Tim Disney, and Cormac Flanagan. 2014. Dynamic Detection of Object Capability Violations Through
      Model Checking. In DLS. 103–112. doi:10.1145/2661088.2661099
[104] Victor Rivera and Bertrand Meyer. 2020. AutoAlias: Automatic Variable-Precision Alias Analysis for Object-Oriented
      Programs. SN Comp. Sci. 1, 1 (2020), 12:1–12:15. https://doi.org/10.1007/s42979-019-0012-1
[105] Michael Sammler, Rodolphe Lepigre, Robbert Krebbers, Kayvan Memarian, Derek Dreyer, and Deepak Garg. 2021.
      RefinedC: automating the foundational verification of C code with refined ownership types. In PLDI. 158–174.
      https://dl.acm.org/doi/10.1145/3453483.3454036
[106] Ina Schaefer, Tobias Runge, Alexander Knüppel, Loek Cleophas, Derrick G. Kourie, and Bruce W. Watson. 2018.
      Towards Confidentiality-by-Construction. In ISOLA. 502–515. doi:10.1007/978-3-030-03418-4_30
[107] Ilya Sergey, Vaivaswatha Nagaraj, Jacob Johannsen, Amrit Kumar, Anton Trunov, and Ken Chan. 2019. Safer Smart
      Contract Programming with Scilla. In OOPSLA, Vol. 3. 1–30. https://doi.org/10.1145/3360611
[108] Randall B. Smith and David M. Ungar. 1995. Programming as an Experience: The Inspiration for Self. In ECOOP,
      Walter G. Olthoff (Ed.), Vol. 952. Springer, 303–330. doi:10.1007/3-540-49538-X_15
[109] Thomas Van Strydonck, Aïna Linn Georges, Armaël Guéneau, Alix Trieu, Amin Timany, Frank Piessens, Lars Birkedal,
      and Dominique Devriese. 2022. Proving full-system security properties under multiple attacker models on capability
      machines. In 35th IEEE Computer Security Foundations Symposium, CSF 2022, Haifa, Israel, August 7-10, 2022. IEEE,
      80–95. doi:10.1109/CSF54842.2022.9919645
[110] Alexander J. Summers and Sophia Drossopoulou. 2010. Considerate Reasoning and the Composite Pattern. In VMCAI.
      328–344. https://doi.org/10.1007/978-3-642-11319-2_24
[111] Alexander J. Summers, Sophia Drossopoulou, and Peter Müller. 2009. Universe-Type-Based Verification Techniques
      for Mutable Static Fields and Methods. J. Object Technol. 8, 4 (2009), 85–125. doi:10.5381/JOT.2009.8.4.A4
[112] David Swasey, Deepak Garg, and Derek Dreyer. 2017. Robust and compositional verification of object capability
      patterns. Proc. ACM Program. Lang. 1, OOPSLA (2017), 89:1–89:26. doi:10.1145/3133913
[113] The Ethereum Wiki. 2018. ERC20 Token Standard. (Dec. 2018). https://theethereum.wiki/w/index.php/ERC20_
      Token_Standard
[114] David M. Ungar and Randall B. Smith. 1991. SELF: The Power of Simplicity. LISP Symb. Comput. 4, 3 (1991), 187–205.
      https://doi.org/10.1007/3-540-49538-X_15
[115] Stephan van Staden. 2015. On Rely-Guarantee Reasoning. In MPC. 30–49. https://link.springer.com/chapter/10.1007/
      978-3-319-19797-5_2
[116] Guannan Wei, Oliver Bracevac, Songlin Jia, Yuyan Bao, and Tiark Rompf. 2024. Polymorphic Reachability Types:
      Tracking Freshness, Aliasing, and Separation in Higher-Order Generic Programs. OOPSLA 8 (2024), 393–424. https:
      //doi.org/10.1145/3632856
[117] Guannan Wei, Danning Xie, Wuqi Zhang, Yongwei Yuan, and Zhuo Zhang. 2024. Consolidating Smart Contracts
      with Behavioral Contracts. In PLDI. 965 – 989. doi:10.1145/3656416
[118] Maurice V. Wilkes and Roger M. Needham. 1980. The Cambridge Model Distributed System. ACM SIGOPS Oper. Syst.
      Rev. 14, 1 (1980), 21–29. doi:10.1145/850693.850695
[119] Anxhelo Xhebraj, Oliver Bracevac, Guannan Wei, and Tiark Rompf. 2022. What If We Don’t Pop the Stack? The
      Return of 2nd-Class Values. In ECOOP. 15:1–15:29. https://doi.org/10.4230/LIPIcs.ECOOP.2022.15
[120] Yichen Xu and Martin Odersky. 2024. A Formal Foundation of Reach Capabilities. In Programming. 134–138.
      https://doi.org/10.1145/3660829.3660851
[121] Conrad Zimmerman, Jenna DiVincenzo, and Jonathan Aldrich. 2024. Sound Gradual Verification with Symbolic
      Execution. POPL 8, 2547–2576. https://doi.org/10.1145/3632927




, Vol. 1, No. 1, Article . Publication date: November 2025.
