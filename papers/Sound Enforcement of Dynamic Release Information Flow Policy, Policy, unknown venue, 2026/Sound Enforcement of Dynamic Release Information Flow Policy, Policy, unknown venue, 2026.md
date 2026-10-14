                                         Sound Enforcement of Dynamic Release Information Flow
                                         Policy
                                         JEFFREY CHING, Duke University, USA
                                         DANFENG ZHANG✉ , Duke University, USA
                                         Information flow analysis is the de facto method of assessing confidentiality and integrity issues. However,
                                         the widespread adoption of information flow analysis in real-world systems is still lacking, partly due to a
                                         fundamental gap between theory and practice: the dynamic nature of security concerns in real-world systems
arXiv:2608.09506v2 [cs.PL] 19 Aug 2026




                                         goes beyond the scope of existing techniques that assume a static policy (i.e., data secrecy does not change).
                                            Recognizing the fundamental gap, a substantial amount of research has studied various aspects of it
                                         (e.g., enabling declassification, endorsement, and revocation policies). A recent work takes a step further by
                                         formalizing a promising end-to-end policy called dynamic release that unifies prior formalizations by allowing
                                         information flow restrictions to downgrade and upgrade in arbitrary ways. However, how to soundly enforce
                                         the powerful dynamic release policy is still an open question.
                                            In this paper, we present the first type system that enforces dynamic release policy and formally prove its
                                         soundness. More specifically, we (1) formalize a core language that enables dynamic release policy, (2) develop
                                         a type system that checks dynamic release policy, (3) develop new proof techniques and formally prove that
                                         the type system enforces dynamic release policy, and (4) implement a prototype of the type system as an
                                         extension to the Rust language, along with case studies on a conference reviewing system and Civitas.
                                         CCS Concepts: • Security and privacy → Formal security models; • Theory of computation → Program
                                         analysis.
                                         Additional Key Words and Phrases: Information flow; Dynamic policy; Type system
                                         ACM Reference Format:
                                         Jeffrey Ching and Danfeng Zhang. 2026. Sound Enforcement of Dynamic Release Information Flow Policy.
                                         Proc. ACM Program. Lang. 10, OOPSLA2, Article 360 (October 2026), 46 pages. https://doi.org/10.1145/3839492

                                         1   Introduction
                                         Many security concerns in computer systems can be understood in terms of information flows. For
                                         example, it is crucial to ensure that private and untrusted data, as well as any data derived from
                                         them, never influence unintended channels (e.g., a public channel) within a computer system. For
                                         decades, noninterference [24] has been the de facto security policy for specifying and checking
                                         information flow requirements. However, a fundamental assumption of noninterference is that the
                                         confidentiality and integrity of information do not change over time, whereas security concerns in
                                         real-world applications are rarely static, making it infeasible to safeguard them via noninterference.
                                         This critical gap prevents widespread adoption of information flow analysis in real-world systems.
                                            Therefore, to better describe information flow restrictions in real-world applications, researchers
                                         have introduced policies that allow sensitivity to change over time, known as dynamic policies.
                                         For example, declassification policy [35] allows the release of sensitive information to the public
                                         under certain conditions. Other dynamic policies have been explored, such as gradual release [7]
                                         Authors’ Contact Information: Jeffrey Ching, Duke University, Durham, USA, jeffrey.ching@duke.edu; Danfeng Zhang,
                                         Duke University, Durham, USA, danfeng.zhang@duke.edu.



                                         This work is licensed under a Creative Commons Attribution 4.0 International License.
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM 2475-1421/2026/10-ART360
                                         https://doi.org/10.1145/3839492


                                                                  Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:2                                                                               Jeffrey Ching and Danfeng Zhang


and its extended version called tight gradual release [8]. Erasure policy [20], on the other hand,
requires public information to become more sensitive or be completely removed. It is required in
applications on untrustworthy storage [6, 50] and secure voting systems [21].
   While prior work studies instances of dynamic information flow policies, the field is overloaded
with inconsistent terminology, formalisms, and sometimes contradictory semantics [34]. These
obstacles make it difficult even for veteran researchers to follow, let alone compare, different policies.
For instance, existing definitions of dynamic policies can have vastly different syntax for defining
policies [44, 45], differing natures of security conditions, and even disagreements on whether or not
a program is secure based on different variants of the same policy [13]. Moreover, many policies
lack robust enforcement mechanisms, and only a limited number, notably the erasure policy [20],
have been implemented as an extension to Jif [38].
   A recent work, Dynamic Release [34], provides a promising solution: it generalizes various kinds
of dynamic policies for the first time via a novel formalization. Beyond expressing various dynamic
policies, the original work also allows apples-to-apples comparison between different dynamic
policies and creates new insights on existing definitions. However, as a pioneering work, it comes
without any enforcement mechanism. In this paper, we tackle the following goal: to develop a sound
and general enforcement mechanism for various kinds of dynamic policies. While dynamic release
policy provides a general platform for reasoning about various dynamic policies, we need to tackle
several technical challenges for its enforcement. First, we need a metalanguage with its security
specification, along with its operational semantics. A challenge in language design is to strike
a balance between expressiveness and simplicity. To do so, we carefully design some language
features tailored for dynamic release policy, including (1) a distinguished set of security events
along with distinguished commands to set and unset those events during program execution, (2)
controlled output commands in the form of output(𝐿, 𝑒, using s0 . . . sk ), which reveal the value of
𝑒 to security level 𝐿 only if all security events s0 . . . sk are met, and (3) a novel relabel command
that performs permissive yet sound conversion between various kinds of labels.
   Second, we must enforce the specified dynamic release policy on the program. To achieve this,
we develop a novel type system that primarily controls information flow at compile time. One
challenge is to achieve a balance between soundness and permissiveness, given the fact that the
meaning of each label can change throughout program execution. To tackle the challenge, we
define two sets of static semantics that we show soundly control information flows according to
dynamic release semantics. In particular, the “flows-to” relation specifies which label is allowed to
flow to another, including flows between dynamic labels and static levels, and even flows between
different kinds of policies (e.g., declassification and endorsement). The “release-to” relation checks
if we can safely release information to a security level at a given program point. Thanks to the
simplicity of the type system, we also implement it as an extension to the Rust language.
   Third, we formally prove that the type system enforces the specified dynamic release policy for
all program executions. For noninterference with a static policy, various proof techniques (e.g., [33,
40, 49]) have been developed. However, these techniques are not applicable for dynamic release
for two major reasons. First, standard noninterference proofs are built on an indistinguishability
relation on memory states: two memory states are said to be indistinguishable when they agree
on the public set of variables. As the set of public variables stays the same throughout program
execution, a standard proof then proceeds by showing that the indistinguishability relation is
an invariance throughout program execution. However, due to the dynamic nature of dynamic
release policy, the set of public variables changes over time, making it impossible to establish
such an invariance. To address the challenge, we introduce a novel indistinguishability relation
parameterized on a security event trace (Definition 10). Moreover, dynamic release is built on the
notion of consistency (Definition 7), which is absent in standard noninterference. To accommodate

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                                                   360:3


that, we introduce unique conditions in several lemmas and theorems to reflect when intentional
leakage is allowed.
   In summary, we make the following contributions.
    • We present a metalanguage together with its security specification for dynamic release
       policies (Section 3). We further formalize the semantics of dynamic security labels, as well as
       the semantics of several new constructs tailored to dynamic release policies.
    • We present a type system that employs two sets of static inference rules to reason about and
       verify information flows within a program (Section 4).
    • We develop novel proof techniques (Section 5) to establish the soundness of our type system.
       In particular, we prove that any well-typed program satisfies its specified dynamic release
       policy across all possible executions.
    • We implement a prototype of our language and its type system as an extension to the
       Rust language. Moreover, we incorporate all the examples presented in the paper, and port
       Civitas [21, 30], originally implemented in Jif [38], as well as a conference management system
       developed in Lifty [39], to our Rust-based implementation (Section 6). We demonstrate that
       these applications, which embody realistic security requirements, can be successfully verified
       using our enforcement mechanism, while incurring only minimal runtime overhead.

2    Background and Overview
   Noninterference. Noninterference [24] is the de facto policy enforced by information flow con-
trol [43]. Intuitively, noninterference requires that for any two runs of a program such that only se-
cret inputs change, the program always produces the same publicly observable outputs (i.e., confiden-
tial inputs do not affect public outputs). However, noninterference is well-recognized [15, 26, 29, 43]
to be too strict for real-world applications. One fundamental gap there is that noninterference
assumes that the secrecy and integrity of information are static (i.e., they do not change). But
in reality, the dynamic nature of security concerns demands information flow policies that can
accommodate evolving secrecy and integrity constraints.
  Dynamic Policy. Dynamic policies allow the sensitivity and/or integrity of information to change
throughout its lifetime. There are mainly three kinds of such dynamic policies in the literature:
    • Declassification/Endorsement [7, 10, 15]: a declassification (resp. endorsement) policy allows
      the sensitivity (resp. integrity) of a piece of information to be downgraded. For example,
      consider a bidding game illustrated in Figure 1-i, which can release the highest bid to the
      public only if the bidding is over, indicated by setting release at Line 7. The bid cannot be
      released before the bidding concludes, making both Line 5 and Line 6 insecure. However,

     1   //wbid: P                                                                                    1   //Alice: P
                                                      1   //store: M
     2   //bid, bid1, bid2: ¬release?S →𝑡 P                                                           2   //notes, book: (¬return?P →𝑝 S)
                                                      2   //copy, credit_card:(¬trans?M →𝑡 ⊤)
     3   eventoff(release);                                                                           3   eventoff(return);
                                                      3   eventoff(trans);
     4   bid = bid1 > bid2 ? bid1 : bid2;                                                             4   notes= chap(book);
                                                      4   copy = credit_card;
     5   wbid = bid; //insecure                                                                       5   output(P,notes, using return);
                                                                                                                                 
                                                      5   // use copy to finish transaction
     6   output(P, wbid, using release); //insecure                                                   6   eventon(return);
                                                      6   output(M, copy, using trans);
                                                                                    
     7   eventon(release);                                                                            7   Alice = relabel //insecure
                                                      7   eventon(trans);
     8   wbid=relabel                                                                                 8    (book, return?P →𝑝 S to S using return);
                                                      8   store = credit_card; //insecure
     9   (bid, ¬release?S →𝑡 P to P using release);                                                   9   output(P, book, using return); //insecure
                                                      9   output(M, copy, using trans); //insecure
    10   output(P, wbid, using release);                                                             10   output(P, notes, using onotes @P);
                (i). Bidding Game                                  (ii). Credit Card                            (iii). Library System


Fig. 1. Examples of the dynamic policies in the order of declassification, erasure and revocation. The shaded lines
use novel language features that we introduce in this work. Insecure code is marked in red. Predicates trans
                                                                                                          and
return
 indicate that the corresponding security events trans and return are never set to true.


                                  Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:4                                                                               Jeffrey Ching and Danfeng Zhang


      after the previously sensitive bids are declassified to the public at Line 7, the highest bid can
      be released to the public as shown in Line 10.
    • Erasure [6, 19, 20]: an erasure policy allows the sensitivity of a piece of information (and
      its derivatives) to be upgraded. One important use case of the erasure policy is to upgrade
      sensitivity so that no memory can hold the information anymore (effectively enforces it to be
      removed from the whole system). For example, consider an online payment system illustrated
      in Figure 1-ii, which takes credit card information from customers to complete the purchase
      as in Lines 4–6. However, it also needs to upgrade the sensitivity of credit_card and copy
      after Line 7 to avoid information leakage after the transaction is complete. Hence, Lines 8
      and 9 are considered insecure as they leak the credit card after the transaction is complete.
    • Delegation and Revocation [23, 37]: delegation and revocation are usually expressed in a role-
      based system to add and remove access permission for each role respectively. For example,
      consider a library system illustrated in Figure 1-iii, where Alice is allowed to access the
      book and take notes during the borrowing period. However, once the book is returned, she
      cannot access the book anymore as shown in Lines 7–9. While revocation also upgrades
      the sensitivity of information, it differs from erasure that Alice can still access information
      released during the borrowing period (e.g., her notes) as shown in Line 10.

    Dynamic Release Policy. To relieve system developers from having to understand different kinds
of dynamic policies as well as the nuances among policies that appear similar on the surface but
differ in important ways, a recent work by Li and Zhang [34] presents a promising end-to-end policy
called dynamic release that unifies prior formalizations by allowing information flow restrictions
to downgrade and upgrade in arbitrary ways. Furthermore, dynamic release is formalized in a
framework that allows apples-to-apples comparisons across existing dynamic policies.
    More specifically, a dynamic release policy is specified by a dynamic security label in the form
of cnd?𝑝 1 ⋄ 𝑝 2 (see the full syntax in Section 3.3), where the condition cnd specifies when data
sensitivity (or integrity) changes, and ⋄ specifies both the direction and kind of change. Each
policy can either be transient or persistent, where intuitively a transient policy (resp. a persistent
policy) disallows (resp. allows) information that was leaked in the past to be revealed afterwards
if information flow restrictions upgrade. In this paper, we use →𝑡 and ↔𝑡 (resp. →𝑝 and ↔𝑝 ) to
denote possible directions for transient (resp. persistent) policies. We simply use arrows without
subscripts when the kind of policy is irrelevant.
    With dynamic release policy, we can concisely and precisely specify the information security
requirements for each of the examples in Figure 1 as dynamic security labels (annotated in gray):

    • In Figure 1.i, we can specify the dynamic security label on bids as ¬release?S →𝑡 P, meaning
      that they are initially S and hence, cannot be released during the bidding phase. However,
      once the bidding has ended (signaled by the condition release), the sensitivity of wbid can
      be downgraded to P, making it publicly available. Moreover, according to the policy, the
      commands from Lines 8–10 are secure as bids are already declassified at those points. But
      the commands on Lines 5–6 releasing the bids before the bidding period ends are insecure.
    • In Figure 1.ii, we can specify the dynamic security label on the credit card and its copy as
      ¬trans? M →𝑡 ⊤, meaning that before the transaction is complete, the merchant can use both
      information at level M. But once the transaction is complete, their sensitivity becomes the
      highest level ⊤, to ensure that they cannot be used in the rest of the system. Therefore, the
      commands on Lines 4–5 that take credit card information from customers to complete the
      purchase are secure according to the policy, while the commands on Lines 8–9, which leak
      credit card information after the transaction is complete, are insecure.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                   360:5


    • In Figure 1.iii, we can specify the dynamic security label on book and notes as ¬return?P →𝑝
      S meaning that information cannot be released after return is set, unless the same information
      was released before the change (as this is a persistent policy with →𝑝 ). Therefore, the
      command at Line 10 is secure according to the policy, since the notes were released to Alice
      before the book is returned. But releasing the book after it is returned on Lines 7–9 is insecure,
      as it was not (completely) released before the book is returned.
Note that Figures 1.ii and 1.iii both employ an upgrade policy, but differ in a subtle yet important
way. In the former, information released prior to the sensitivity upgrade cannot be revealed after the
upgrade, whereas in the latter such release remains permitted. This distinction also arises in other
policies: for instance, gradual release [7] is a persistent policy, while cryptographic erasure [6],
along with other erasure-based approaches, follows a transient policy semantics.
   Sound Enforcement Overview. As illustrated in Figure 1, dynamic release policy provides a unified
framework to specify and reason about a broad range of dynamic policies. However, prior work [34]
formulates security as an end-to-end semantic property quantified over all possible pairs of program
executions (Section 3.4). Hence, it remains an open question of how to statically determine whether
a given program (e.g., the ones in Figure 1) complies with its specified policy.
   The goal of this work is to develop a programming language that enables programmers to (i)
implement programs, (ii) specify desired dynamic release policies, and (iii) verify that the source
code satisfies its claimed dynamic release policy. So far, we have introduced several key components
of the language. First, the core is an imperative language with standard constructs, including
assignments, conditionals, loops, and output operations. Second, dynamic release policies are
specified via annotations on variables at the beginning of the program. Third, policy changes are
governed by security events, which can be toggled on and off through the distinguished functions
eventon and eventoff. Finally, the language features relabel and output commands that enable
permissive checking of information flows across different dynamic release labels.
   To illustrate how to check the dynamic release policy in a static way, we revisit the code in
Figure 1.i. The bidding game has a dynamic policy ¬release?S →𝑡 P. To check if the code satisfies
this policy, we first need a sound mechanism to directly compare dynamic labels at each program
point, such as Lines 8–9. This is achieved via a “flows to” relation ⊏    ∼ on labels, which essentially
defines a security lattice on dynamic release labels. Compared with (static) lattices that are typically
used in information flow systems, the security lattices for dynamic release policies are more
complicated as the interpretation of a label changes over time. Hence, the lattice over the “flows to”
relation is parameterized by some facts of security events that must hold at each program point. For
example, on Lines 8–9, the label of bid, namely ¬release?S →𝑡 P, can safely flow to P whenever
release has been true in the event trace (intuitively, since it has been declassified). We formalize
the “flow to” relation on labels in Section 4 and prove its soundness: for any two labels 𝑆 ⊢ 𝑝 1 , 𝑝 2
and security event trace 𝜎, 𝑝 1 ⊏∼ 𝜎 𝑝 2 if and only if 𝑝 2 is always at least as restrictive as that of 𝑝 1
on any extension of 𝜎 (Theorem 1), assuming that 𝜎 meets all security events in 𝑆. A type system
built on the relation can reject insecure assignments, such as Line 5, where the relation cannot be
statically verified.
   Moreover, the command output(𝐿, 𝑒, using s0 . . . sk ) reveals the value of 𝑒 to the security level
𝐿. To check if the policy on 𝑒 allows its value to be released at that point, such as Line 6 and Line 10
in Figure 1.i, we formalize the “release to” relation on labels in Section 4.3 and prove its soundness:
for any label 𝑝, level 𝐿 and a set of security events 𝑆 such that 𝑆 ⊢ 𝑝 <  ∼ 𝐿, information with label 𝑝
can be released on a channel at level 𝐿 under any execution trace that satisfies 𝑆 (Theorem 2). With
the relation, we develop a type system that accepts the secure release in Line 10, but also rejects
the insecure release in Line 6. One subtlety of checking an output command is that a persistent

                        Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:6                                                                               Jeffrey Ching and Danfeng Zhang


                          Variables 𝑥, 𝑦, 𝑧
                       Expressions 𝑒 ::= 𝑥 | 𝑛 | 𝑒 op 𝑒
                             Levels 𝐿 ∈ L
                     Sec. Events(S) s | ¬s | o𝑥 @𝐿
                       Commands 𝑐 ::= skip | 𝑥 := 𝑒 | while (𝑒) do 𝑐 |
                                      if (𝑒) then 𝑐 1 else 𝑐 2 | 𝑐 1 ; 𝑐 2 | eventon(s) |
                                      eventoff(s) | output(𝐿, 𝑒, using s0 . . . sk ) |
                                      output(𝐿, 𝑒, using o𝑥 , s1 . . . sk ) |
                                      𝑥 := relabel(𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk )
                     Sec. Labels(B) 𝑝, 𝑞 ::= 𝐿 | cnd? 𝑝 ⋄ 𝑞
                        Conditions cnd ::= s | b s | cnd ∧ cnd | cnd ∨ cnd | ¬cnd
                           Mut. Dir. ⋄ ::=→𝑡 |↔𝑡 |→𝑝 |↔𝑝
                               Fig. 2. Language syntax with security specification.


policy allows information revealed in the past to be released again regardless of the current policy.
To do so, the security event trace also tracks a history of released information (Section 3.2).
   Finally, we formally prove that the type system enforces the end-to-end dynamic release policy:
for any well-typed program with annotated dynamic release labels, the knowledge gained from
observing each program output does not exceed the “allowance” prescribed by the policy. A central
technical challenge in this proof arises from the dynamic nature of release labels, which causes both
the security lattice and the release-to relation to evolve during execution. Consequently, existing
proof techniques (e.g., [33]) cannot be applied directly. We address these challenges and present a
proof sketch in Section 5, with the full formal proof provided in [17].

3     Language
We first present a simple imperative language with its security specification, along with the
operational semantics and the semantics on dynamic release labels.

3.1     Syntax
The language in Figure 2 provides standard features such as variables and expressions, along with
commands such as branches, loops, sequential commands, and assignments. The remaining features
are designed for security purposes:
      • We assume a predefined lattice L consists of a set of static security levels. Here, L is an
        arbitrary security lattice, which can represent confidentiality levels, integrity levels, or a
        combination of both. For simplicity, though, we assume a confidentiality lattice throughout
        the paper. We further assume at least two levels in most examples: P for public and S for secret,
        while the language supports an arbitrary lattice. The assumption is general enough to support
        both Denning-style lattice [22] (e.g., with P ⊏ S), and principal/role-based model [3, 23, 37]
        (e.g., with {alice, bob} ⊏ {alice}, stating that information accessible to both Alice and Bob
        is less restrictive than information accessible to Alice only).
      • In the simplest case, a security label 𝑝 ∈ B is a security level taken from the security lattice.
        In general, a security label can be dynamic, as specified in the form of cnd?𝑝 ⋄ 𝑞 where the
        condition cnd controls whether 𝑝 or 𝑞 takes effect, and the mutation ⋄ controls the direction
        and kind of the transition. In particular, there are three possible directions of mutation, →,
        ← and ↔. 𝑝 → 𝑞 (resp. 𝑝 ← 𝑞) specifies a one-time transition from 𝑝 to 𝑞 (resp. from 𝑞 to 𝑝)

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                   360:7


      when its corresponding condition cnd evaluates to false (resp. true) the first time. Since
      cnd?𝑝 ← 𝑞 is semantically identical to ¬cnd?𝑞 → 𝑝, our syntax omits the ← form and treats
      it as syntactic sugar for the latter. Direction ↔ means that the transition can happen in both
      directions depending on the value of cnd. Moreover, there are two types of policies: transient
      and persistent, specified with subscripts 𝑡 and 𝑝 respectively. The main difference between
      them is that a persistent policy always allows to reveal information that has been revealed in
      the past, while a transient policy does not [34].
  To strike a balance between expressiveness and enforcement, we carefully designed a few
language features in Figure 2, making it substantially different from the one presented in the
dynamic release paper [34]:
    • Rather than allowing the condition cnd to be an arbitrary program expression, we restrict it
      to a set of distinguished, predefined security events s ∈ S. These security events can be viewed
      as special Boolean variables, distinct from ordinary program variables such as 𝑥, 𝑦, 𝑧, and may
      only be modified via the distinguished functions eventon and eventoff. This restriction
      enables tractable reasoning about event status within a type system.
      Besides user-defined security events above, the language also supports predicates over them,
      such as standard logical operations on security events and b   s, which holds when the security
      event s has never been set to true. Moreover, to enable reasoning about whether a variable’s
      value has been released in the past, we introduce a new class of security events, denoted by
      o𝑥 @𝐿, indicating that the variable 𝑥 has previously been released at security level 𝐿.
    • Rather than associating each output channel with a dynamic release label, we restrict output
      commands to fixed security levels, written as output(𝐿, 𝑒, using s0 . . . sk ). As is standard,
      we assume that only observers at or above level 𝐿 can access the value of 𝑒 produced by
      this command. Furthermore, the expression 𝑒 is revealed only if all security events in the
      sequence s0, . . . , sk are enabled at the time the command is executed. Otherwise, the output
      command has no effect (i.e., it behaves as a nop). Consistent with prior works on dynamic
      policies [7, 20, 34], we assume that information is only released with output commands in
      the language; assignments to variables do not reveal any information directly.
    • We introduce a relabel command that can also “peek” at the current status of security events
      and utilize more permissive information flow reasoning rules when possible. In particular,
      𝑥 := relabel (𝑒, 𝑝 to 𝐿 using s0 . . . sk ) updates 𝑥 to the value of 𝑒 if the events s0 . . . sk are
      all enabled at the time the command is executed. Otherwise, the command has no effect
      (i.e., it behaves as a nop). Note that the command is also annotated with a security label 𝑝,
      and a security level 𝐿; the idea is that since information only flows from 𝑒 to 𝑥 when all
      security events s0 . . . sk are enabled, a type system can rely on this assumption to reason
      more permissively about whether a flow from 𝑒 to 𝑥 is secure under this assumption.
   For example, consider Lines 8–9 in Figure 1.i, where release is a security event that turns true
after bidding is complete. At runtime, we know that release holds, and hence, the relabel command
writes the value of bid to wbid. Statically, the type system relies on the using annotations to
determine which security events hold at each program point, which in this example is release.
With the assumption, the dynamic label on wbid, which is ¬release?S →𝑡 P, can be leaked to P as
the information is already declassified whenever release holds. Hence, the novel design of relabel
command allows a static type system to soundly prove security without deep knowledge of the
program state at each program point. We formalize and enforce such reasoning in our type system
(Section 4.4).
   One caveat is that the design also relies on a programmer, or an advanced program analysis, to
properly annotate the clause after using to preserve the original semantics of a program. We leave

                        Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:8                                                                               Jeffrey Ching and Danfeng Zhang


           OS-eventon                                      OS-eventoff
           ⟨𝑚, eventon(s), 𝜎⟩ → ⟨𝑚, skip, 𝜎 · s⟩           ⟨𝑚, eventoff(s), 𝜎⟩ → ⟨𝑚, skip, 𝜎 · ¬s⟩

                OS-Output-Succ                                   (
                                  ∀𝑖 ∈ 0...𝑘.                     𝜎 · o𝑥 @L, 𝑒 is a variable 𝑥
                 ⟨𝑚, 𝑒⟩ ⇓ 𝑣                       𝜎′ =
                               eval(si, 𝜎) = true                 𝜎,         otherwise
                                                                    ⟨𝐿,𝑣,𝜎 ⟩
                         ⟨𝑚, output(𝐿, 𝑒, using s0 . . . sk ), 𝜎⟩ −−−−−→ ⟨𝑚, skip, 𝜎 ′ ⟩

                           OS-Output-fail
                                                           ∃𝑖 ∈ 0...𝑘.
                                      ⟨𝑚, 𝑒⟩ ⇓ 𝑣
                                                       eval(si, 𝜎) = false
                            ⟨𝑚, output(𝐿, 𝑒, using s0 . . . sk ), 𝜎⟩ →
                                                                     − ⟨𝑚, skip, 𝜎⟩

               OS-Relabel-Succ
                                ⟨𝑚, 𝑒⟩ ⇓ 𝑛         ∀𝑖 ∈ 0...𝑘. eval(si, 𝜎) = true
               ⟨𝑚, 𝑥 := relabel(𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ → ⟨𝑚[𝑥 := 𝑛], skip, 𝜎⟩

                   OS-Relabel-Fail
                                        ∃𝑖 ∈ 0...𝑘. eval(si, 𝜎) = false
                    ⟨𝑚, 𝑥 := relabel(𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ → ⟨𝑚, skip, 𝜎⟩

        Fig. 3. Small-Step Semantics of Selected Commands, which eval checks the value of s on trace 𝜎.


this as orthogonal future work, as our primary goal of this work is to develop a core language with
sound enforcement of dynamic release policies, assuming that an oracle is provided.

3.2     Semantics of Commands
We model a program state as memory, written as 𝑚: a mapping from program variables to their
corresponding values. For an expression 𝑒, its big-step semantics is written as ⟨𝑚, 𝑒⟩ ⇓ 𝑛, which
means that 𝑒 evaluates to value 𝑛 under memory 𝑚. For commands, we use small-step semantics
since the dynamic nature of information flow policy requires step-by-step details during a program
execution. The small-step semantics is written as:
                                                      ⟨𝐿,𝑣,𝜎 ⟩
                                          ⟨𝑚, 𝑐, 𝜎⟩ −−−−−→ ⟨𝑚 ′, 𝑐 ′, 𝜎 ′ ⟩
where 𝜎 and 𝜎 ′ are sequences of triggered security events (e.g., s1 · ¬s2 · o𝑥 @P).
   Each step emits a (potentially empty) output event ⟨𝐿, 𝑣, 𝜎⟩, which indicates the output of value 𝑣
to an output channel at level 𝐿 under the security event trace 𝜎. We assume that all security events
are initialized. By default, the condition is set to true in right-arrow and bi-directional policies. Only
output commands reveal information to entities and, hence, generate output events, as formalized
in Rule (OS-Output-Succ) in Figure 3. Moreover, changes to security events are tracked in the
security event trace, by rules (OS-EventOn), (OS-EventOff) and (OS-Output-Succ).
   It is worth noting that both the output and relabel commands are syntactically associated with
using clauses. These using annotations specify sufficient conditions on security events under which
the corresponding commands are considered secure. For example, the output command at Line 6 in
Figure 1.i can reveal wbid to the public only when release is set. Accordingly, when these using
clauses are satisfied, the corresponding commands behave identically to their standard semantics.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                   360:9



                                                               {|𝐿|}𝜎 = 𝐿
                                                     (
                                                         {|𝑝 }| 𝜎      first(cnd, false, 𝜎) = −1
                        {|cnd?𝑝 → 𝑞|}𝜎 =
                                                         {|𝑞|}𝜎 [𝑖:]   𝑖 = first(cnd, false, 𝜎)
                                              (
                                                  {|𝑝 }| 𝜎 [𝑖+1:]      𝑖 = last(cnd, false, 𝜎) ≠ ∥𝜎 ∥
                     {|cnd?𝑝 ↔ 𝑞|}𝜎 =
                                                  {|𝑞|}𝜎 [𝑖+1:]        𝑖 = last(cnd, true, 𝜎) ≠ ∥𝜎 ∥
                                                     Fig. 4. Label semantics.


Otherwise (namely, when any security event appearing after the using keyword evaluates to
false) the command instead behaves as a nop. For example, the output command at Line 6 in
Figure 1.i produces no outputs due to Rule (OS-Output-Fail), as release is not set at that point.
  As we elaborate in Section 4.4, a type system can statically verify that these programmer-provided
annotations are sufficient conditions for end-to-end security. Hence, the using annotations affect
the observable behavior of the original program only in two cases: either the annotations are
overly restrictive, preventing an otherwise secure command from executing, or the corresponding
commands in the original program would violate the security policy (e.g., Line 6 in Figure 1.i) and
must therefore be suppressed.
  Finally, as introduced informally earlier, the relabel command has the same semantics as a
normal assignment 𝑥 := 𝑒 when all the security events’ values are as expected; otherwise, the
command is the same as a nop instruction. The semantics of other commands are standard and are
included in [17].
  One program execution under initial state ⟨𝑚 0, 𝑐 0, 𝜎0 ⟩ produces an execution trace 𝜏 as follows:
                                     ⟨𝐿0 ,𝑣0 ,𝜎0 ⟩                          ⟨𝐿𝑛−1 ,𝑣𝑛−1 ,𝜎𝑛−1 ⟩
                       ⟨𝑚 0, 𝑐 0, 𝜎0 ⟩ −−−−−−−→ ⟨𝑚 1, 𝑐 1, 𝜎1 ⟩ · · · −−−−−−−−−−−−−→ ⟨𝑚𝑛 , 𝑐𝑛 , 𝜎𝑛 ⟩
   We use ⟨𝑚, 𝑐, 𝜎⟩ ↩→ 𝜏 to denote that execution from ⟨𝑚, 𝑐, 𝜎⟩ produces an execution trace 𝜏. We
use 𝜏 [𝑖 ] to denote the configuration after the 𝑖-th evaluation step in 𝜏, 𝜏 [:𝑖 ] to denote a sub-trace
from the initial point to the i-th evaluation step, and 𝜏 [𝑖:𝑗 ] to denote a sub-trace between 𝑖-th and
𝑗-th evaluation steps. We use ∥𝜏 ∥ to denote the number of evaluation steps in the trace. Since 𝜎 is a
sequence of events, we use similar annotation for its subsequences.

3.3   Semantics of Security Labels
To interpret dynamic release labels, we treat each label cnd?𝑝 ⋄ 𝑞 as an “expression” and evaluate
its value (i.e., a security level from a predefined lattice in our setting) at the end of a trace 𝜎 as
shown in Figure 4. In the definition, taken from [34], the helper function first returns the first
index of 𝜎 such that cnd evaluates to the second parameter, or -1 if no such index is found; and
last returns the last index of 𝜎 such that cnd evaluates to the second parameter, or -1 if no such
index is found. As for ↔, the labels may transit an arbitrary number of times whenever the value
of cnd changes, which is mainly used in the revocation dynamic policy.
   Intuitively, {|𝑝 }| 𝜎 computes the least restrictive security level that 𝑝 can flow to at the end of
𝜎. More specifically, for a static level 𝐿, its interpretation is simply 𝐿. For dynamic labels like
cnd?𝑝 → 𝑞, a one-time sensitivity change from 𝑝 to 𝑞 occurs when cnd first evaluates to false.
Let 𝑖 be the first index in 𝜎 such that cnd evaluates to false. {|cnd?𝑝 → 𝑞|}𝜎 reduces to {|𝑝 }| 𝜎 if no
such 𝑖 exists; otherwise, it reduces to {|𝑞|}𝜎 [𝑖:] . Bi-directional labels are interpreted based on the last
configuration of 𝜎, where 𝑖 is the last index at which cnd evaluates to false. Therefore, 𝑖 ≠ ∥𝜎 ∥
implies that cnd evaluates to true at the end of 𝜎, and the label reduces to 𝑝. The label 𝑝 is then
evaluated under 𝜎 [𝑖+1] , ensuring that any potentially nested conditions are handled properly.

                        Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:10                                                                              Jeffrey Ching and Danfeng Zhang


    The interpretation of the labels above specifies when and where information can be released to:
information with label 𝑝 can be released to entities at or above level {|𝑝 }| 𝜎 at the end of 𝜎. However,
it is not suitable for information flow enforcement, since it does not allow direct comparison of
dynamic labels at each program point. For example, label ¬release?S →𝑡 P (declassification policy)
and label S both evaluate to S when the security event release evaluates to false under 𝜎. However,
information flow from S to ¬release?S →𝑡 P is obviously insecure as if the flow happens, the
former is effectively declassified once release becomes true.
    To address the challenge above, we observe that for a secure flow from label 𝑝 to 𝑞 under an
event trace 𝜎, we need to examine all possible extensions of 𝜎 so that 𝑝 is always bounded by 𝑝 ′ in
the future (i.e., ∀𝜎 ⪯ 𝜎 ′ . {|𝑝 }| 𝜎 ′ ⊑ {|𝑝 ′ }| 𝜎 ′ ). Consequently, we write 𝑝 ⊑𝜎 𝑝 ′ to denote that 𝑝 ′ is at
least as restrictive as 𝑝 at 𝜎: that is, for all future extensions of 𝜎, wherever information with label
𝑝 ′ can be released, information with label 𝑝 can also be released:
  Definition 1 (Partial Ordering on Dynamic Release Labels).
                        ∀𝑝, 𝑝 ′, 𝜎. 𝑝 ⊑𝜎 𝑝 ′ ⇐⇒ ∀𝜎 ′ . (𝜎 ⪯ 𝜎 ′ ⇒ {|𝑝 }| 𝜎 ′ ⊑ {|𝑝 ′ }| 𝜎 ′ )
   Note that with dynamic release labels, the ordering on labels is parameterized on a security
event trace as the relation changes during program execution. This contrasts with standard nonin-
terference, where the security lattice remains fixed throughout program execution. For example,
consider two security event traces 𝜎1 and 𝜎2 (𝜎1 ⪯ 𝜎2 ), where release is always false in 𝜎1 , but it
turned true in 𝜎2 . It is easy to check that (¬release?S → P ̸⊑𝜎1 P) and (¬release?S → P ⊑𝜎2 P),
meaning that the declassification label cannot flow to P under 𝜎1 but it can flow to P under 𝜎2 . On
the other hand, (S ̸⊑𝜎1 ¬release?S → P) and (S ̸⊑𝜎2 ¬release?S → P), meaning that S can never
flow to information with the declassification label.
   Persistent vs. Transient Label. Our partial ordering definition on dynamic release labels (Defini-
tion 1) does not distinguish between persistent and transient labels. This might be surprising as
intuition might suggest that a persistent policy is less restrictive than its counterpart of a transient
policy (i.e., s?𝑝 →𝑡 𝑞 is strictly more restrictive than s?𝑝 →𝑝 𝑞). However, we found this intuition
to be incorrect, as the difference between persistent and transient labels only shows up in the
end-to-end security condition of dynamic release, rather than where information can be released
to at each program point. We will elaborate on their differences in the type system (Section 4.4).

3.4      Dynamic Release Policy
Dynamic release [34] is the first end-to-end information flow policy that generalizes multiple kinds
of dynamic information flow policies. Its precise definition is a bit involved and we only present
the essentials in this section to provide sufficient background information to understand how to
soundly enforce it, which is the main contribution of this paper. We follow the notations in the
original paper, other than a few minor changes for readability.
   Informally, a program 𝑐 satisfies dynamic release policy iff for any output 𝑡 produced by 𝑐, the
knowledge gained about any variable 𝑥 by observing 𝑡 is bounded by what’s allowed by the policy
of 𝑥 at the program point that outputs 𝑡.
   To formalize this, we first define “indistinguishable” memory set w.r.t. some memory 𝑚 and a set
of variables 𝑋 as the set of memories that are equivalent to 𝑚 on the values of all variables in 𝑋 .
   Definition 2 (Memory Closure). Given a memory 𝑚 and a set of variables 𝑋 , the memory
closure of 𝑚 on 𝑋 is the set of memories that agree with 𝑚 on all variables in 𝑋 :
                                   J𝑚K𝑋 ≜ {𝑚 ′ | ∀𝑥 ∈ 𝑋 . 𝑚(𝑥) = 𝑚 ′ (𝑥)}

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                 360:11


  Given a memory 𝑚 and a security label 𝑝, we write J𝑚K≠𝑝 as the set of memories that agree with
𝑚 on all variables except those whose security label is 𝑝. That is, J𝑚K≠𝑝 ≜ J𝑚K {𝑥 |Γ (𝑥 )≠𝑝 } . Intuitively,
only the values of variables with label 𝑝 may differ between 𝑚 and any 𝑚 ′ ∈ J𝑚K≠𝑝 .
  In addition to memory, we need to utilize a filter function on output traces, in order to precisely
capture what an attacker can learn from a trace: the filter function returns false for irrelevant
outputs on a trace. With any trace filter 𝑓 , we define a trace projection as follows:
  Definition 3 (Projection of Trace Filter).
                                     ⌊𝜏⌋ 𝑓 ≜ ⟨⟨𝑙, 𝑣, 𝜎⟩ ∈ 𝜏 | 𝑓 (𝑙, 𝑣, 𝜎)⟩
   To formalize the attacker’s observation, we define a trace projection up to level 𝐿, ⌊𝜏⌋ 𝐿 ≜
⌊𝜏⌋ 𝜆𝑙,𝑣,𝜎 . 𝑙 ≤𝐿 that takes in the attacker’s level 𝐿 and returns a sub-trace of output events that are
visible to the attacker.
   Attacker’s Knowledge from an Output Trace. Consider an attacker at security level L. The attacker
is able to observe all output events ⟨𝐿 ′, 𝑣, 𝜎⟩ such that 𝐿 ′ ⊑ L. Hence, two traces 𝜏1 and 𝜏2 are
indistinguishable to the attacker, written as 𝜏1 ∼L 𝜏2 , if they agree on all outputs at or below
attacker’s level L. More formally,
  Definition 4 (Indistinguishability).
                                       ∼𝐿 ≜ {(𝜏1, 𝜏2 ) | ⌊𝜏1 ⌋ 𝐿 ⪯ ⌊𝜏2 ⌋ 𝐿 }
  Therefore, the “knowledge” gained by observing an output trace 𝜏 produced by a program 𝑐 is
defined as all initial memory states that can produce an indistinguishable trace from 𝜏:
  Definition 5 (Knowledge Gained from Output Trace).
                              𝑘 1 (𝑐, 𝜏, 𝐿) ≜ {𝑚 | ⟨𝑚, 𝑐, ∅⟩ ↩→ 𝜏 ′ ∧ 𝜏 ∼𝐿 𝜏 ′ }
   Intuitively, the knowledge set consists of all initial memory states that remain possible given the
portion of the execution trace observable to the attacker. Moreover, the smaller the knowledge set,
the more information the attacker has learned from the program’s execution.
   By definition, the knowledge set monotonically decreases as additional events are produced along
the execution trace, making it well suited for formalizing declassification policies [7]. In contrast,
it is inadequate for erasure policies, which require reasoning about increases in uncertainty, or
equivalently, expanding the knowledge set. Consider the credit-card example in Figure 1-ii. After
the first output, the attacker learns the credit card number, so the knowledge set contains only
those initial memories with the actual credit card number. After Line 7, however, the credit card
number should no longer be inferable. Accordingly, the knowledge set should again include all
possible credit card numbers, reflecting the restored uncertainty required by the erasure policy.
To accommodate both kinds of dynamic policies within a unified framework, Dynamic Release
reasons about the knowledge gained from each individual output event, rather than from the entire
execution trace. We introduce this notion next.
   Attacker’s Knowledge from the Last Event. While the attacker’s security level remains fixed
throughout program execution, the meaning of a dynamic label may change over time. To precisely
define what can be revealed at each program point, a major challenge solved by [34], we begin
with one key observation: events produced by two program executions are not, in general, aligned
according to their positions in the corresponding execution traces. The reason is that due to
downgrading, the publicly observable outputs of different executions may have different lengths
(Observation 2 in [34]). To address this issue, we introduce the secret projection of an execution
trace, parameterized by an attacker at security level 𝐿 and a secret labeled 𝑝. The secret projection

                        Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:12                                                                                           Jeffrey Ching and Danfeng Zhang


retains only the effective outputs, namely, those outputs produced while information labeled 𝑝 is
considered secret from an attacker at level 𝐿.
   Definition 6 (Secret Projection of Trace). Given a policy 𝑝 and an attacker at level 𝐿, the
secret projection of a trace is the subtrace containing outputs visible at level 𝐿 that occur while 𝑝
remains secret from an attacker at level 𝐿:
                                        ⌊𝜏⌋ 𝑝,𝐿 ≜ ⌊𝜏⌋ 𝜆𝑙,𝑣,𝜎 . 𝑙 ⊑𝐿 ∧ {|𝑝 |}𝜎 ̸ ⊑𝐿
    Using effective outputs, we introduce a notion of trace consistency. Two execution traces, 𝜏1 and
𝜏2 , are said to be consistent with respect to an attacker at security level 𝐿 and a secret labeled 𝑝 if
their effective outputs (1) have the same length, and (2) end with the same output event.
  Definition 7 (Consistency). Two output sequences 𝜏1 and 𝜏2 are consistent w.r.t. a policy 𝑝 and
an attack level 𝐿, written as 𝜏1 ≡𝑝,𝐿 𝜏2 if
                                                                         [𝑛]         [𝑛]
                               𝑛 = ∥ ⌊𝜏1 ⌋ 𝑝,𝐿 ∥ = ∥ ⌊𝜏2 ⌋ 𝑝,𝐿 ∥ ∧ ⌊𝜏1 ⌋ 𝑝,𝐿 = ⌊𝜏2 ⌋ 𝑝,𝐿
   With the above definitions, we can build the definition of the knowledge gained by the attacker
at level 𝐿 by observing the last event.
   Definition 8 (Attacker’s Knowledge Gained from the Last Event). For an attacker at level
𝐿, the attacker’s knowledge w.r.t. information with policy 𝑝, after observing the last event of an output
sequence traces program 𝑐, is the set of all initial memories that produce an output sequence that is
indistinguishable to some consistent counterpart of the trace 𝜏:
                                                    Ø
                      𝑘 2 (𝑐, 𝜏, 𝐿, 𝑝) =                            𝑘 1 (𝑐, 𝜏 ′[:𝑗 ] , 𝐿)
                                           ∃.𝑚 ′ ,𝜎,𝑗 . ⟨𝑚 ′ ,𝑐,𝜎 ⟩↩→𝜏 ′ ∧𝜏 ′[:𝑗 ] ≡𝑝,𝐿 𝜏

  Finally, we define dynamic release security. For every output event produced during program
execution, the attacker’s knowledge gained from observing that output (Definition 8) must be
bounded by the policy allowance at the corresponding program point. For a transient policy, the
policy allowance is simply J𝑚K≠𝑝 , where only the values of variables labeled 𝑝 are treated as
secret. For a persistent policy, the allowance is instead defined as J𝑚K≠𝑝 ∩ 𝑘 1 (𝑐, 𝜏 [:𝑖 −1] , 𝐿), thereby
permitting the attacker to retain any knowledge acquired through previous outputs while still
preventing any additional information beyond what the policy allows from being learned.
    Definition 9 (Dynamic Release).
    ∀𝑚, 𝐿 ⊆ L, 𝑝 ∈ B, 𝜎, 𝜏 . ⟨𝑚, 𝑐, 𝜎⟩ ↩→ 𝜏 ⇒ ∀1 ≤ 𝑖 ≤ ∥𝜏 ∥.
                                                                                (
                                                                                    J𝑚K≠𝑝 ,                           transient
                                                  𝑘 2 (𝑐, 𝜏 [:𝑖 ] , 𝐿, 𝑝) ⊇
                                                                                    J𝑚K≠𝑝 ∩ 𝑘 1 (𝑐, 𝜏 [:𝑖 −1] , 𝐿),   persistent

4    Type System
To enforce dynamic release policy, we develop a static type system to control information flow at
compile time. One challenge of doing so is to achieve a balance between soundness and permis-
siveness, given the fact that the meaning of each label can change throughout program execution.
To address this challenge, we first introduce two static relations, each parameterized by 𝑆, a set
of statically computed facts about security events that must hold at each program point. The
relations approximate when information can securely flow between dynamic labels, and be released
respectively at compile time. Built on them, we define a type system that enforces the end-to-end
dynamic release policy on the whole program.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                      360:13


                                             General Lattice Rules
                          Lattice                         Trans
                             𝐿 ⊑ 𝐿′                        𝑆 ⊢𝑝 ⊏
                                                                ∼𝑝
                                                                   ′
                                                                               𝑆 ⊢ 𝑝′ ⊏
                                                                                      ∼𝑝
                                                                                         ′′

                                      ′                                       ′′
                          𝑆 ⊢𝐿⊏
                              ∼𝐿                                      𝑆 ⊢𝑝 ⊏
                                                                           ∼𝑝
                                           Directional Inference Rules
  R-To                            R-From                          D-To
                      ′
  𝑆 ⊨ ¬s2        ⊢𝐿⊏
                   ∼𝑞             𝑆 ⊨ ¬s1       ⊢ 𝑝′ ⊏
                                                     ∼𝐿           𝑆 ⊨ ¬s2       ¬s1 ⇒ ¬s2        ⊢ s1 ?𝐿 → 𝑝 ′ ⊏
                                                                                                               ∼𝑞
                                                                                                                  ′

                      ′
      𝑆 ⊢𝐿⊏
          ∼ s2 ?𝑞 → 𝑞              𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                                                   ∼𝐿                        𝑆 ⊢ s1 ?𝐿 → 𝑝 ′ ⊏
                                                                                             ∼ s2 ?𝑞 → 𝑞
                                                                                                         ′


            D-To Two                            R-To Two
                      ′                                                           ′
            𝑆 ⊢𝑝 ⊏
                 ∼𝐿 ⊢𝑝 ⊏∼𝐿                      ¬s2 ⇒ ¬s1        𝑆 ⊢𝑝 ⊏
                                                                      ∼ s2 ?𝑞 → 𝑞       ⊢ 𝑝′ ⊏
                                                                                             ∼ s2 ?𝑞 → 𝑞
                                                                                                         ′

             𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                             ∼𝐿                                 𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                                                                                ∼ s2 ?𝑞 → 𝑞
                                                                                            ′


                                          Bi-directional Inference Rules
        Bi-To                             Bi-From                           Bi-Both
                        ′
        ⊢𝐿⊏ ∼𝑞     ⊢𝐿⊏
                     ∼𝑞                   ⊢𝑝 ⊏∼𝐿      ⊢ 𝑝′ ⊏
                                                           ∼𝐿               s1 ⇔ s2      ⊢𝑝 ⊏
                                                                                            ∼𝑞        ⊢ 𝑝′ ⊏
                                                                                                           ∼𝑞
                                                                                                              ′

                         ′
         𝑆 ⊢𝐿⊏
             ∼ s2 ?𝑞 ↔ 𝑞                   𝑆 ⊢ s1 ?𝑝 ↔ 𝑝 ′ ⊏
                                                           ∼𝐿                  𝑆 ⊢ s1 ?𝑝 ↔ 𝑝 ′ ⊏
                                                                                               ∼ s2 ?𝑞 ↔ 𝑞
                                                                                                           ′



Fig. 5. Selected Static Rules for “Flows-to” Relation, which 𝑆 ⊨ s1 denotes that s1 must have been true given 𝑆.


4.1    Oracle on Security Events
Since the interpretation of dynamic release labels relies on a security event trace 𝜎, the type system
inevitably requires knowledge of the existence or absence of security events up to some program
point. Moreover, for a persistent policy, dynamic release also depends on the outputs in the past
(Definition 9). To decouple the reasoning of security events and outputs from information flow
enforcement, we follow a simple design where the type system only uses the facts established
by the using keyword in the output and relabel commands. For example, a set of facts 𝑆 =
{s1, ¬s1, ¬s2, sb3, o𝑥 @P} states that up to the program point of interest, s1 must have been both
true and false, s2 must have been false (and may be true), sb3 has never been true, and the
value of 𝑥 has been released to level 𝐿 already. These facts are checked by commands such as
output(P, 𝑥, using s1, ¬s1, ¬s2, sb3, o𝑥 @P) when any condition evaluates to false, the command
behaves like a nop command (Section 3.2). In general, we can also estimate 𝑆 statically, such as
using dataflow analysis [2], which we leave as future work. Hereafter, we use 𝑆 ⊨ s2 to indicate that
s2 must have been true given 𝑆, and 𝑆 ⊨ sb2 to indicate that s2 must never have been true given 𝑆.

4.2    Static Rules for Flows-to Relation
We first define a flows-to relation on dynamic labels, parameterized by a set of security events 𝑆,
such as {s1, ¬s2 }. Intuitively, the flows-to relation 𝑆 ⊢ 𝑝 ⊏
                                                             ∼ 𝑞 holds if label 𝑝 is less restrictive than,
or equivalent to 𝑞 for any event trace 𝜎 that satisfies 𝑆 and its extensions. A selection of rules for
the flows-to relation is summarized in Figure 5; all rules are included in [17].
  Base Cases. Rules (Lattice) and (Trans) are general rules based on Denning-style security lattice
and the rule of transitivity. These rules are the same as a typical static information flow system.
  Directional Cases. Rule (R-To) compares a static level 𝐿 against a dynamic label s2 ?𝑞 → 𝑞 ′ under
the assumption that ¬s2 evaluates to true (i.e., s2 evaluates to false). Hence, we can simplify
the dynamic label to 𝑞 ′ , as the transition to 𝑞 ′ must have happened. Rule (R-From) is symmetric

                          Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:14                                                                              Jeffrey Ching and Danfeng Zhang


to Rule (R-To). Note that in both rules, we intentionally omit the event facts 𝑆 before ⊢ from the
assumptions to ensure soundness. The reason is that, with nested conditions, events in 𝑆 may be
triggered before the top-level condition is evaluated. Consequently, propagating them to the more
deeply nested sub-label may be unsound.
   The general case when both ends of flows-to relation involve dynamic labels is a bit more
complicated. To illustrate the subtlety, we consider a naive but incorrect extension to Rule (R-To)
                                          𝑆 ⊨ ¬s2       ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                                                                      ∼𝑞
                                                                         ′

                                           𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                                                           ∼ s2 ?𝑞 → 𝑞
                                                                       ′


At first glance, this rule is legit as it follows the same argument as (R-To): it only reduces s2 ?𝑞 → 𝑞 ′
when s2 turns false. However, this rule is unsound when 𝑞 ′ has nested conditions. To see why,
consider the following counterexample:

                                                 ∼ s2 ?P → (s1 ?P → S)
                                       s1 ?P → S ⊏
and a trace 𝜎 where s1 is set to false and then to true in sequence. After that, s2 turns false, as
illustrated below.
                                                                {|S|}#⋢{|41? P → S|}#
                                                                                        (
                                    s1=false     s1=true    s2 =false

  At the end of 𝜎, ¬s2 holds. Hence, we can instantiate 𝑆 with ¬s2 in the proposed rule, and derive
                                     ¬s2 ⊨ ¬s2       ⊢ s1 ?P → S ⊏
                                                                 ∼ s1 ?P → S
                                     ¬s2 ⊢ s1 ?P → S ⊏
                                                     ∼ s2 ?P → (s1 ?P → S)
where the assumption that ⊢ s1 ?P → S ⊏      ∼ s1 ?P → S holds trivially as both sides are identical.
     However, we next show that the derived flow-to relation is unsound. By the semantics, {|s1 ?P →
S|}𝜎 reduces to S as s1 turned to false on the trace. Moreover, {|s2 ?P → (s1 ?P → S)|}𝜎 reduces
to {|s1 ?P → S|}𝜎 [𝑖:] where 𝑖 is the first index when s2 turned to false. Note that even though s1
was false on the whole trace 𝜎, the nested condition s1 is evaluated on the sub-trace after the
top-level condition s2 is triggered (Figure 4). On that sub-trace 𝜎 [𝑖:] , s1 evaluates to true. Hence,
{|s1 ?P → S|}𝜎 [𝑖:] further reduces to P. Hence, {|s1 ?P → S|}𝜎 = S ̸⊑ P = {|s2 ?P → (s1 ?P → S)|}𝜎 ,
indicating that s1 ?P → S is not always bounded by s2 ?P → (s1 ?P → S) at 𝜎 (i.e., s1 ?P → S ̸⊑𝜎
s2 ?P → (s1 ?P → S), Definition 1). A similar issue occurs when 𝑝 contains nested conditions.
     To ensure soundness while permitting permissiveness when possible, we observe that the
soundness issue above can be avoided if 𝑝 has no nested conditions (i.e., it is a level 𝐿), and s1 is
never false before s2 turns false, which can be captured as (¬s1 ⇒ ¬s2 ), where ⇒ is a logical
implication. The general case is included in the sound derivation rule (D-To) in Figure 5. The
symmetric version Rule (D-From) is included in [17].
     When the permissive rules (D-To) and (D-From) are not applicable, rule (R-To Two) conserva-
tively checks that s1 ?𝑝 → 𝑝 ′ can flow to some level 𝐿. For the general case of s1 ?𝑝 → 𝑝 ′ ⊏ ∼ s2 ?𝑞 →
𝑞 ′ , similar to Rule (D-To), Rule (D-To Two) assumes that (¬s2 ⇒ ¬s1 ) to be sound.
   Bi-Directional Cases. Finally, we introduce the static rules for bi-directional policies, which align
with the design of →. Bi-directional policies only have the less permissive rules as the condition
can change throughout trace extensions, and it is hard to define rules without binding to both
ends. Rules (Bi-To) and (Bi-From) correspond to the cases where one side is a plain static level 𝐿 in
the single-direction cases, checking bounds for both parts of the dynamic policy. Rule (Bi-Both)
assumes that the dynamic labels on both sides have equivalent conditions, and then checks the
“flows-to” relation on the corresponding components.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                                 360:15


  Lattice         Trans                             R-From-P                  R-From-F                    Bi-From
    𝐿 ⊑ 𝐿′        𝑆 ⊢𝐿<∼𝐿
                          ′
                                  𝑆 ⊢ 𝐿′ <
                                         ∼𝐿
                                            ′′
                                                    𝑆 ⊨ ¬s1 ⊢ 𝑝 ′ <
                                                                  ∼𝐿          𝑆⊨¬d s1 𝑆 ⊢ 𝑝 <
                                                                                            ∼𝐿            ⊢𝑝 <∼𝐿       ⊢ 𝑝′ <
                                                                                                                            ∼𝐿
              ′                       ′′                             ′ <                        ′ <
  𝑆 ⊢𝐿<
      ∼𝐿                   𝑆 ⊢𝐿<
                               ∼𝐿                   𝑆 ⊢ s1 ?𝑝 → 𝑝 ∼ 𝐿          𝑆 ⊢ s1 ?𝑝 → 𝑝 ∼ 𝐿          𝑆 ⊢ s1 ?𝑝 ↔ 𝑝 ′ <
                                                                                                                          ∼𝐿

                                       Fig. 6. Static Rules for “Release-to” Relation.


  Next, we establish the soundness of the static inference rules: for any labels 𝑝, 𝑞 and a set of
security events 𝑆, 𝑆 ⊢ 𝑝 ⊏
                         ∼ 𝑞 implies that 𝑞 is more restrictive or equal to 𝑝 on any event trace 𝜎
where 𝑆 holds, as well as on any extension of 𝜎.
   Theorem 1 (Soundness of Flows-To Relation). For all policies p and q, a trace 𝜎, a set of
                                           ∼ 𝑞 and 𝑆 hold on 𝜎, then 𝑝 ⊑𝜎 𝑞.
security events 𝑆 = s0 . . . sk , if 𝑆 ⊢ 𝑝 ⊏
Proof sketch. We proceed by induction on the static inference rules. We present the proof for
Cases (R-To) and (D-To) here; the complete proof is available in [17].
  By Definition 1, it is sufficient to show that for any 𝜎 ′ such that 𝜎 ⪯ 𝜎 ′ , we have {|𝑝 }| 𝜎 ′ ⊑ {|𝑞|}𝜎 ′ .
   • (R-To): By the assumption, we have ⊢ 𝐿 ⊏                         ′
                                                              ∼ 𝑞 and 𝑆 ⊨ ¬s2 . Since 𝑆 holds on 𝜎 by assumption,
      𝜎 ⪯ 𝜎 , and 𝑆 ⊨ ¬s2 , there must be some index 𝑖 on 𝜎 ′ at which s2 first turns false. According
                ′

      to the semantics of Figure 4, we know that {|s2 ?𝑞 → 𝑞 ′ }| 𝜎 ′ = {|𝑞 ′ }| 𝜎 ′[𝑖:] .
      From the induction hypothesis and the assumption that ⊢ 𝐿 ⊏                           ′                             ′
                                                                                         ∼ 𝑞 , we get {|𝐿|}𝜎 ′[𝑖:] ⊑ {|𝑞 }| 𝜎 ′[𝑖:] .
                                                        ′                      ′
      Hence, {|𝐿|}𝜎 ′ = 𝐿 = {|𝐿|}𝜎 ′[𝑖:] ⊑ {|𝑞 }| 𝜎 ′[𝑖:] = {|s2 ?𝑞 → 𝑞 }| 𝜎 ′ .
   • (D-To): Similar to (R-To), we first derive {|s2 ?𝑞 → 𝑞 ′ }| 𝜎 ′ = {|𝑞 ′ }| 𝜎 ′[𝑖:] from the assumptions,
      where 𝑖 is the index when s2 first turns false.
      If s1 has been false on 𝜎 ′ , let 𝑗 be the index when it turns false the first time. Since ¬s1 ⇒
      ¬s2 , it is guaranteed that 𝑗 ≥ 𝑖. According to the semantics of Figure 4, we know that
      {|s1 ?𝐿 → 𝑝 ′ }| 𝜎 ′ = {|𝑝 ′ }| 𝜎 ′[ 𝑗 :] = {|s1 ?𝐿 → 𝑝 ′ }| 𝜎 ′[𝑖:] where the second equation holds as s1 must
      remain true between 𝑖 and 𝑗. Moreover, from the induction hypothesis and the assumption
      ⊢ s1 ?𝐿 → 𝑝 ′ ⊏               ′                                      ′           ′
                            ∼ 𝑞 , we know that {|s1 ?𝐿 → 𝑝 }| 𝜎 ′[𝑖:] ⊑ {|𝑞 }| 𝜎 ′[𝑖:] . Hence {|s1 ?𝐿 → 𝑝 }| 𝜎 ′ =
                                                                                                                         ′
                      ′                 ′                         ′
      {|s1 ?𝐿 → 𝑝 }| 𝜎 ′[𝑖:] ⊑ {|𝑞 }| 𝜎 ′[𝑖:] = {|s2 ?𝑞 → 𝑞 }| 𝜎 ′ .
      If s1 has never been false on 𝜎 ′ , we know that {|s1 ?𝐿 → 𝑝 ′ }| 𝜎 ′ = 𝐿 = {|s1 ?𝐿 → 𝑝 ′ }| 𝜎 ′[𝑖:] . From
      the induction hypothesis and the assumption ⊢ s1 ?𝐿 → 𝑝 ′ ⊏                              ′
                                                                                          ∼ 𝑞 , we know that {|s1 ?𝐿 →
      𝑝 }| 𝜎 ′[𝑖:] ⊑ {|𝑞 }| 𝜎 ′[𝑖:] . Hence {|s1 ?𝐿 → 𝑝 }| 𝜎 ′ = {|s1 ?𝐿 → 𝑝 }| 𝜎 ′[𝑖:] ⊑ {|𝑞 ′ }| 𝜎 ′[𝑖:] = {|s2 ?𝑞 → 𝑞 ′ }| 𝜎 ′ .
        ′               ′                                  ′                      ′

                                                                                                                                    □

4.3    Static Rules for Release-to Relation
Dynamic release policy controls information release at output commands. More formally, for
each output command output(𝐿, 𝑒, using s0 . . . sk ), information with label 𝑝 can be released when
{|𝑝 }| 𝜎 ⊑ 𝐿 (Figure 4). Accordingly, we define a release-to relation, written as 𝑆 ⊢ 𝑝 <
                                                                                        ∼ 𝐿, to statically
check if we can safely release information with label 𝑝 to output command at level 𝐿 under the
assumption that 𝑆 holds when the output occurs. Compared with the flows-to relation ⊏              ∼ , the
release-to relation is simpler as (1) the target (i.e. the right-hand side) is always a security level by
design, and (2) we do not need to consider any changes to 𝑝 after the release.
    Both rules (R-From-P) and (Bi-From) are similar to their counterparts in the flows-to relation.
The key difference is in rule (R-From-F): it reduces the dynamic label to 𝑝 whenever 𝑆 ⊨ ¬s     c1 . This
is sound for the release-to relation as by definition (Figure 4), how the interpretation of where
information can be released to is only determined by the current event trace. But for the flows-to
relation, we have to consider all extensions to the current trace, which may violate the assumption.


                            Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:16                                                                                    Jeffrey Ching and Danfeng Zhang


                                Seqence                         If
           Skip                 𝑝𝑐, Γ ⊢ 𝑐 1 𝑝𝑐, Γ ⊢ 𝑐 2          Γ ⊢ 𝑒 : 𝑝𝑐 ′   𝑝𝑐 ′, Γ ⊢ 𝑐 1   𝑝𝑐 ′, Γ ⊢ 𝑐 2   ⊢ 𝑝𝑐 ⊏
                                                                                                                     ∼ 𝑝𝑐
                                                                                                                          ′

           𝑝𝑐, Γ ⊢ skip               𝑝𝑐, Γ ⊢ 𝑐 1 ; 𝑐 2                     𝑝𝑐, Γ ⊢ if (𝑒) then 𝑐 1 else 𝑐 2

                  Assign                                         While
                       ∼ Γ(𝑥)         Γ ⊢ 𝑒 : Γ(𝑥)               Γ ⊢ 𝑒 : 𝑝𝑐 ′   𝑝𝑐 ′, Γ ⊢ 𝑐               ′
                  ⊢ 𝑝𝑐 ⊏                                                                        ⊢ 𝑝𝑐 ⊏
                                                                                                     ∼ 𝑝𝑐
                          𝑝𝑐, Γ ⊢ 𝑥 := 𝑒                                 𝑝𝑐, Γ ⊢ while (𝑒) do 𝑐

      Output                                                  Output-Per
      Γ ⊢𝑒 :𝑝       s0 ...sk ⊢ 𝑝 <
                                 ∼𝐿        ⊢ 𝑝𝑐 ⊏
                                                ∼𝐿            𝑥 immutable          Γ(𝑥) is persistent           ⊢ 𝑝𝑐 ⊏
                                                                                                                     ∼𝐿
          𝑝𝑐, Γ ⊢ output(𝐿, 𝑒, using s0 ...sk )                   𝑝𝑐, Γ ⊢ output(𝐿, 𝑥, using o𝑥 @L, s0 ...sk )

  Relabel
  Γ ⊢ 𝑒 : 𝑝𝑓            ∼ Γ(𝑥)
                   ⊢ 𝑝𝑐 ⊏                            ∼ Γ(𝑥)
                                       s0 ...s𝑘 ⊢ 𝐿𝑡 ⊏             EventOn(s)                       EventOff(s)
  s0 ...s𝑘 ⊢ 𝑝 𝑓 ⊏
                 ∼ 𝐿𝑡                                                  ⊢ 𝑝𝑐 ⊏
                                                                            ∼⊥                          ⊢ 𝑝𝑐 ⊏
                                                                                                             ∼⊥
      𝑝𝑐, Γ ⊢ 𝑥 := relabel(𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 ...sk )           𝑝𝑐, Γ ⊢ EventOn(s)               𝑝𝑐, Γ ⊢ EventOff(s)

                                           Fig. 7. Typing Rules for Commands.



  Theorem 2 (Soundness of Release-To Relation). For all policies p, a trace 𝜎, a set of security
events 𝑆 = s0 . . . sk , if 𝑆 ⊢ 𝑝 <
                                  ∼ 𝐿 and 𝑆 holds on 𝜎, then {|𝑝 }| 𝜎 ⊑ 𝐿.
  The proof is similar to the proof of Theorem 1. The full proof is included in [17].

4.4      Typing Rules
Lastly, we present a type system that enforces the end-to-end dynamic release policy on the
whole program. The overall structure of the typing rules is similar to other information flow type
systems [19, 20, 43], where each command is checked under two conditions 𝑝𝑐 and Γ. Here, 𝑝𝑐
is the standard program counter label used to control implicit information flows [43], and Γ is a
mapping that assigns each variable to its security label. The typing rules on expressions, in the
form of Γ ⊢ 𝑒 : 𝑝, are completely standard, which is included in [17].
   Several typing rules for commands are standard. Rule (skip) denotes that a nop command is
always secure. Rule (Seqence) enforces that both commands in a sequence are typed under the
same 𝑝𝑐 label. Rule (If) guards both branches of a conditional with a program counter 𝑝𝑐 ′ , which
must be at least as restrictive as the condition’s label, in order to control implicit flows. Rule (While)
is similar to Rule (If). Rule (Assign) requires that the policy on 𝑥 is at least as restrictive as that on
𝑒 to control explicit information flow from 𝑒 to 𝑥.
   Other rules are novel and carefully designed to check the dynamic release policy. Rule (Relabel)
is the first rule that utilizes annotated events s0 . . . s𝑘 to check information flow from 𝑒 to 𝑥 in a
more permissive way than Rule (Assign). It allows information to be “relabeled” when possible.

   Example 1: Bidding Game (Figure 1.i). We examine the relabel command on Line 9, which occurs
after release is set to true. This line type-checks under rule (Relabel) as follows (we omit less
interesting parts of the proof for simplicity):
                                                               release ⊨ release          ⊢P⊏
                                                                                            ∼P
                          Γ ⊢ bid : ¬release?S →𝑡 P
                                                              release ⊢ ¬release?S →𝑡 P ⊏
                                                                                        ∼P
                       P, Γ ⊢ wbid := relabel(bid, ¬release?S →𝑡 P to P using release)

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                 360:17


   Recall that at runtime, relabel checks if all events after using hold; it turns the command into
a nop if any assumed event is not correct (Figure 3). Hence, the typing rule can safely use event
release to check if a flow from dynamic label ¬release?S →𝑡 P to P is secure, via the permissive
Rule (R-From) in Figure 5.
   Rule (Output) is the second typing rule that utilizes annotated events s0 . . . sk to check if the
value of 𝑒 can be released in a permissive way.
  Example 2: Credit Card (Figure 1.ii). Both variables copy and credit_card are labeled with
dynamic labels trans?M →𝑡 ⊤. The output in Line 6 can be type checked by the rule (Output),
which allows the value of copy to be released as ¬trans
                                                  at the point:
                                                            trans
                                                             ⊨ trans
                                                                               ⊢M<
                                                                                  ∼M
                            Γ ⊢ copy : ¬trans?M →𝑡 ⊤
                                                           ⊢ ¬trans?M →𝑡 ⊤ <
                                                          trans             ∼M
                                       M, Γ ⊢ output(M, copy, using trans)
                                                                    

Recall that at runtime, the output command checks if all events after using are correct; it turns the
command into a nop if any assumed event is not correct (Figure 3). Hence, the typing rule can use
                                                to check if dynamic label ¬trans?M →𝑡 ⊤ can
the fact that trans has never been true (i.e., trans)
be released to M, via Rule (R-From-F) in Figure 6.
  On the other hand, the same output command at Line 9, after the transaction is completed, is
insecure. Although the command can still be type checked, we note that since the transaction is
completed, the assumed event trans
                                 is no longer correct. Hence, nothing will be released at runtime
(Rule (OS-Output-Fail) in Figure 3).
  Rule (Output-Per) is a more permissive version of Rule (Output), in the sense that it allows
the value of 𝑥 to be released again when 𝑥 is immutable and Γ(𝑥) has a persistent policy. Here, the
output event o𝑥 assumes that 𝑥 has already been released before the current output command.
   Example 3: Library System (Figure 1.iii). Before Alice returns the book, the variable notes was
released in Line 5, which can be type-checked in the same way as in Line 6 of the credit card
example described above. According to the semantics of the output command, the output event
onotes is added to the execution trace at that point. After Alice returns the book on Line 6, the same
value that was released on Line 5 can still be safely released again on Line 10 as the policy on notes
and book is a persistent policy. This can be confirmed by the following proof tree:
                                   notes immutable       Γ (notes) is persistent
                                     P, Γ ⊢ output(P, notes, using onotes @P)

On the other hand, if we replace the same line with output(P, book, using obook ), the command is
insecure as book was never released before it was returned. In this case, the insecure command is
still type-checked. But since the assumed event obook is no longer correct, nothing will be released
at runtime (Rule (OS-Output-Fail) in Figure 3).
   Finally, Rules (eventon(s)) and (eventoff(s)) handle distinguished commands that set/unset
security events. For both of them, we require that the 𝑝𝑐 label be public (i.e., at the lowest level P
in the lattice). The reason is to avoid label channels, where secret information interferes with the
sensitivity level of variables [20].

5   Soundness Proof
The hallmark of information flow security is its ability to maintain end-to-end confidentiality
and integrity across all system executions. For noninterference with a static policy, various proof
techniques (e.g., [33, 40, 49]) have been developed to prove that static type systems can soundly
enforce noninterference policy.

                        Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:18                                                                                                         Jeffrey Ching and Danfeng Zhang


                                        unclassified (U) ≤ confidential (C) ≤ secret (S) ≤ topsecret (T)




                                   U            C            f: ¬change?S → C               U              C


                                    S           T                                            S             T
                                                                          C




Fig. 8. An example in a multi-level military system, where the variable 𝑓 belongs to levels before and after the
security event change is set to true.

   In those standard noninterference proofs, all variables’ sensitivity/integrity are assumed to be
fixed throughout program execution. Hence, for any attacker at a certain security level L, we can
statically partition all variables into two sets: public set {𝑥 | Γ(𝑥) ⊑ L} and secret set {𝑥 | Γ(𝑥) ̸⊑ L}.
At a high level, standard noninterference proofs are built on an indistinguishability relation on
memory states: two memory states 𝑚 1 and 𝑚 2 are said to be indistinguishable for an attacker at L
when they agree on the public set of variables:
                                𝑚 1 ≈ 𝑚 2 ≜ ∀𝑥 . Γ(𝑥) ⊑ L ⇒ 𝑚 1 (𝑥) = 𝑚 2 (𝑥)
Then, a standard proof proceeds by showing that the indistinguishability relation is an invariance
on any two program executions with indistinguishable initial memory states.
   To see the invariance more clearly, we consider a military-grade security system that includes
four security levels: unclassified (U), confidential (C), secret (S), and top secret (T) in Figure 8. Here,
an attacker with a confidential security clearance can access only unclassified and confidential files.
Hence, two memory states are considered indistinguishable if they agree on {𝑥 | Γ(𝑥) = U ∨ Γ(𝑥) =
C}. Note that for a static policy, the set remains unchanged throughout program execution.
   However, in the presence of dynamic labels, such a proof strategy no longer applies, as the set of
secret variables can change throughout program execution. Suppose that there is a variable 𝑓 asso-
ciated with dynamic release label ¬change?S →𝑡 C. A naive extension of the indistinguishability
relation to the dynamic setting is as follows:
                             𝑚 1 ≈𝜎 𝑚 2 ≜ ∀𝑥 . {|Γ(𝑥)|}𝜎 ⊑ C ⇒ 𝑚 1 (𝑥) = 𝑚 2 (𝑥)
However, maintaining such an indistinguishability relation is impossible. Let 𝜎 and 𝜎 ′ be traces
right before and after change is set to true in Figure 8. Given 𝑚 1 ≈𝜎 𝑚 2 , 𝑚 1 (𝑓 ) and 𝑚 2 (𝑓 ) might
hold different values since {|Γ(𝑓 )|}𝜎 ̸⊑ C. Hence, we are unable to prove 𝑚 1 ≈𝜎 ′ 𝑚 2 which requires
that 𝑚 1 (𝑓 ) = 𝑚 2 (𝑓 ) as {|Γ(𝑓 )|}𝜎 ′ ⊑ C.
   To address the challenge, in addition to the attacker level L, we also introduce a distinguished,
arbitrary dynamic release label B and prove that the desired property of dynamic release (Defini-
tion 9) holds against any attacker’s level L and source’s label B ∈ B. Intuitively, B is a distinguished
dynamic label denoting the source label that is considered “sensitive” per security reasoning. With
a fixed attacker level L and a fixed source label B, indistinguishability in memory is defined as
  Definition 10. Two memories 𝑚 1 and 𝑚 2 are indistinguishable under an event trace 𝜎 if they
agree on all variables such that B ̸⊑𝜎 Γ(𝑥):
                            𝑚 1 ≈𝜎 𝑚 2 ⇐⇒ ∀𝑥 . B ̸⊑𝜎 Γ(𝑥) ⇒ 𝑚 1 (𝑥) = 𝑚 2 (𝑥)
  Recall that by Definition 1, 𝑝 ⊑𝜎 𝑝 ′ denotes that {|𝑝 }| 𝜎 ′ ⊑ {|𝑝 ′ }| 𝜎 ′ for any extension 𝜎 ′ of 𝜎.
  A key insight here is that we can maintain the invariance since the size of {𝑥 | B ̸⊑𝜎 Γ(𝑥)} can
never increase through program execution due to the following fact.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                                             360:19


   Lemma 1 (Trace Preservation).
                                     ∀𝑝, 𝑝 ′, 𝜎. 𝑝 ⊑𝜎 𝑝 ′ ⇒ (∀𝜎 ′ . 𝜎 ⪯ 𝜎 ′ ⇒ 𝑝 ⊑𝜎 ′ 𝑝 ′ )

   The second challenge is that given an attacker’s level L and the source label B, information
leakage is allowed under some circumstances. Recall that under Definition 8, the consistency
relation on traces ignores all outputs produced when {|B|}𝜎 ⊑ L (i.e., when information with B
can be released to the attacker at L). Moreover, when B is a persistent policy, dynamic release
allows information leaked in the past to be revealed again (Definition 9). Accordingly, in a few
lemmas and theorems in the soundness proof, we added extra conditions under which intentional
leakage is allowed. For persistent policy, note that the type system conservatively allows leakage
when the value of 𝑥 has been revealed previously (by checking o𝑥 under using) and that 𝑥 is
immutable (Rule (Output-Per) in Figure 7). Hence, the relaxing condition is that the command 𝑐
being executed can be type-checked by Rule (Output-Per).
   The formal soundness proof follows a previous small-step noninterference proof [33], with
notable changes as stated above. In the concrete proof, we introduce an augmented semantics where
the “tainted” values are wrapped in brackets, written as [𝑛] instead of 𝑛. Moreover, instructions
executed under “tainted” branch conditions (i.e., branch conditions that evaluate to bracketed
values) are also wrapped in brackets, written as [𝑐] instead of 𝑐. A memory is said to be “well-
formed” if all bracketed values are only stored in variables that are considered sensitive to an
attacker at level L.
   The full soundness proof, including definition of the augmented language, bracketed values and
extended semantics, is provided in [17]. Next, we highlight important results and a proof sketch.
   We consider any attacker’s level L and source label B in the proof. The first important lemma
states that indistinguishability in memory (Definition 10) is preserved in each step, as long as starting
memories 𝑚 1 and 𝑚 2 are indistinguishable and each is well-formed (𝜎 |= 𝑚 1 and 𝜎 |= 𝑚 2 ), 𝑐 1 and 𝑐 2
both type-check and are equivalent (𝑐 1 ≈ 𝑐 2 ), and the relaxing conditions are not met (i.e., {|𝐵|}𝜎 ̸⊑ L
and both 𝑐 1 and 𝑐 2 type-check without using the relax rule (Output-Per)). Note that the Lemma
also allows 𝑐 2 to diverge, making the dynamic release assurance termination-insensitive [5, 7].
   Lemma 2 (Unwinding).
   ∀𝑚 1, 𝑚 2, 𝑐 1, 𝑐 2, 𝜏1, 𝜏2, 𝜎, 𝑥, 𝑝𝑐, Γ. 𝜎 |= 𝑚 1 ∧ 𝜎 |= 𝑚 2 ∧ 𝑚 1 ≈𝜎 𝑚 2 ∧
                                                                                                              𝜏1
          (𝑐 1 ≠ output(𝐿 ′, 𝑥, using o𝑥 , s0 . . . sk )) ∧ {|B|}𝜎 ̸⊑ L ∧ 𝑐 1 ≈ 𝑐 2 ∧ ⟨𝑚 1, 𝑐 1, 𝜎⟩ −→ ⟨𝑚 1′ , 𝑐 1′ , 𝜎 ′ ⟩ ⇒
                              𝜏2 ∗
(∃𝑚 2′ , 𝑐 2′ , 𝜏2 .⟨𝑚 2, 𝑐 2, 𝜎⟩ −→ ⟨𝑚 2′ , 𝑐 2′ , 𝜎 ′ ⟩ ∧𝑚 1′ ≈𝜎 ′ 𝑚 2′ ∧𝑐 1′ ≈ 𝑐 2′ ∧ ⌊𝜏1 ⌋ L = ⌊𝜏2 ⌋ L ) ∨ (∃𝑐. 𝑐 2 = [𝑐] and 𝑐 diverges)

Proof sketch. We sketch the proof of the most interesting case with Rule (Output) here.
    • (Output): Based on the assumption that 𝑐 1 ≠ output(𝐿 ′, 𝑥, using o𝑥 , s0 . . . sk ), we know
      that only the typing rule (Output) is applicable in this case. As 𝑐 1 ≈ 𝑐 2 , it is trivial that
      skip ≈ skip and 𝑚 1′ = 𝑚 1 ≈𝜎 𝑚 2 = 𝑚 2′ . To prove ⌊𝜏1 ⌋ L = ⌊𝜏2 ⌋ L , there are two cases.
      – 𝐿 ′ ⊑ L: We show that ⟨𝑚, 𝑒⟩ ⇓ 𝑣 for some 𝑛 without brackets in this case. We proceed by
        assuming that ⟨𝑚, 𝑒⟩ ⇓ [𝑛] and show a contradiction.
        From the typing rule, we know that Γ ⊢ 𝑒 : 𝑝 and s0 . . . sk ⊢ 𝑝 <        ′
                                                                               ∼ 𝐿 . From the assumption
        ⟨𝑚, 𝑒⟩ ⇓ [𝑛] and Lemma 4 in [17], we have B ⊑𝜎 𝑝, which implies {|B|}𝜎 ⊑ {|𝑝 }| 𝜎 by definition.
        By Theorem 2 and s0 . . . sk ⊢ 𝑝 <  ′                        ′
                                         ∼ 𝐿 , we know {|𝑝 }| 𝜎 ⊑ 𝐿 whenever the output semantics
                                                       ′
        is not a nop. Hence, we can derive {|B|}𝜎 ⊑ 𝐿 ⊑ L, which contradicts the assumption that
        {|B|}𝜎 ̸⊑ L in the theorem statement.
        Hence, it must be true that ⟨𝑚 1, 𝑒⟩ ⇓ 𝑛 for some 𝑛. By Lemma 6 in [17], ⟨𝑚 2, 𝑒⟩ ⇓ 𝑛 too.
        Hence, both output traces under 𝑚 1 and 𝑚 2 produce the same output event ⟨𝐿 ′, 𝑛, 𝜎⟩.

                               Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:20                                                                                                             Jeffrey Ching and Danfeng Zhang

                           𝜏[:i] and 𝜏′ [:j] are consistent
                                        ⟨ L′, v1, σ1 ⟩                                 ⟨ L′, vi, σi ⟩
                         𝜏 ⟨m1,c1,σ1⟩                ⟨m2,c2,σ2⟩              ⟨mi,ci,σi⟩               ⟨mi+1,ci+1,σi+1⟩


                                           B⋢ σ1 L                                          B⋢ σi L
                                                                                                        Either diverges or ∃j′



                         𝜏′ ⟨m′1,c′1,σ1⟩          ⟨m′2,c′2,σ2⟩               ⟨m′j,c′j,σj⟩          * ⟨m′j′ c′ j′,σ j′ ⟩
                               Induction Hypothesis                           To prove: Use Unwinding Lemma

                        (a) The Figure illustrates the proof concept on transient policy. The
                        orange part is the induction hypothesis and the green part is the part
                        to be proved with the Unwinding Lemma.
                           Hypothesis: m′ ∈ 𝑘1(𝑐, 𝜏 [:𝑖−1] , 𝐿)                To prove: m′ ∈ 𝑘1(𝑐, 𝜏 [:𝑖] , 𝐿)
                         m                                              k       i-1                            i      ⎣𝜏⎦L
                                    1


                              output1(L,x)               outputk(L,x)            outputi(L,x)               𝜏[i]
                                               ...                            ...
                                                                                      =
                                   =




                                                            =




                              output1(L,x)               outputk(L,x)            outputj(L,x)               𝜏′ [j]

                         m′         1                                   k′      j′                             j
                                                                                                                      ⎣𝜏′ ⎦L


                        (b) This Figure shows that 𝑚 ′ ∈ 𝑘 1 (𝑐, 𝜏 [:𝑖 ],𝐿 ), which indicates the
                        variable 𝑥 has been released. This difference causes the proof not
                        to be concluded with Unwinding Lemma. We only show part of the
                        output syntax due to space.

 Fig. 9. Illustrations on the proof of Theorem 3. Conceptual proof on (a) transient policy, (b) persistent policy.


         – 𝐿 ′ ̸⊑ L: The projection traces on L are empty (⌊𝜏1 ⌋ L = ∅ = ⌊𝜏2 ⌋ L ) as 𝐿 ′ ̸⊑ L.
                                                                                                                                                     □
  Based on the unwinding lemma, we next show the main soundness result.
   Theorem 3 (End-to-end Soundness). For all command 𝑐 and typing environment Γ, if 𝑝𝑐, Γ ⊢ 𝑐
for some program counter 𝑝𝑐, then the program 𝑐 satisfies dynamic release policy, which means
                                                                                                  (
                                                                                                      J𝑚K≠B ,                           transient
   ∀𝑚, 𝜎, 𝜏 . ⟨𝑚, 𝑐, 𝜎 ⟩ ↩→ 𝜏 ⇒ ∀1 ≤ 𝑖 ≤ ∥𝜏 ∥. 𝑘 2 (𝑐, 𝜏 [:𝑖 ] , L, B) ⊇
                                                                                                      J𝑚K≠B ∩ 𝑘 1 (𝑐, 𝜏 [:𝑖 −1] , L),   persistent

Proof sketch. We conduct a proof of induction on the trace length 𝑖. Note that unlike a traditional
proof for static noninterference, we need to show that under two indistinguishable initial memories,
they both produce consistent, rather than indistinguishable traces.
  Transient. For a transient policy B, proving 𝑘 2 (𝑐, 𝜏 [:𝑖 ] , L, B) ⊇ J𝑚K≠B boils down, after expanding
the definitions of 𝑘 1 and 𝑘 2 , to show that for any 𝑚 ′ indistinguishable from 𝑚 and ⟨𝑚 ′, 𝑐, 𝜎⟩ ↩→ 𝜏 ′ ,
we can find some index 𝑗 on 𝜏 ′ such that 𝜏 ′[:𝑗 ] and 𝜏 [:𝑖 ] are consistent (i.e., 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 ] ). The
induction step is illustrated in Figure 9a, where the green part illustrates the new index 𝑗 ′ that
we need to find in order to match index 𝑖 + 1 on trace 𝜏. The orange part illustrates the induction
hypothesis: traces 𝜏 [:𝑖 ] and 𝜏 ′[:𝑗 ] are consistent.
  There are two cases to consider at each induction step: {|B|}𝜎𝑖 ̸⊑ L and {|B|}𝜎𝑖 ⊑ L.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                        360:21

                                                                                              ′
      • When {|B|}𝜎𝑖 ̸⊑ L, we can directly apply Lemma 2 to show that ⌊𝜏 ′[ 𝑗:𝑗 ] ⌋ 𝐵,𝐿 = ⌊𝜏 [𝑖:𝑖+1] ⌋ 𝐵,𝐿 . In
                                                                    ′
        addition to the induction hypothesis, we know that 𝜏 ′[:𝑗 ] ≡𝐵,𝐿 𝜏 [:𝑖+1] stands.
      • When {|B|}𝜎𝑖 ⊑ L, the event 𝑣 produced by ⟨𝑚𝑖 , 𝑐𝑖 , 𝜎𝑖 ⟩ (in the green part of Figure 9a) must
        have an empty projection:
                                                ⟨𝐿 ′ ,𝑣,𝜎𝑖 ⟩
                                 ⌊⟨𝑚𝑖 , 𝑐𝑖 , 𝜎𝑖 ⟩ −−−−−−→ ⟨𝑚𝑖+1, 𝑐𝑖+1, 𝜎𝑖+1 ⟩⌋ B,L ≜ ∅
                                                               ′                       ′
        Hence, we simply set 𝑗 ′ = 𝑗 and have 𝜏 ′[:𝑗 ] ≡𝐵,𝐿 𝜏 [:𝑖+1] as 𝜏 ′[:𝑗 ] = 𝜏 ′[:𝑗 ] , 𝜏 [:𝑖 ] = 𝜏 ′[:𝑖+1] and,
        from the induction hypothesis, 𝜏 ′[:𝑗 ] ≡𝐵,𝐿 𝜏 [:𝑖 ] .
   Persistent. For persistent policy, the proof is mostly identical to the transient case, since, by
definition, its security condition is a relaxation of its corresponding transient policy. The exception
is for the case of
                        (𝑐𝑖 = output(𝐿 ′, 𝑥, using o𝑥 , s0 . . . sk )) ∧ (𝑥 is immutable)
because the unwinding lemma (Lemma 2) is not applicable. We need a new proof strategy for
this case, which is illustrated by the green dotted box in Figure 9b. To proceed, we utilize the
fact that 𝑚 ′ ∈ 𝑘 1 (𝑐, 𝜏 [:𝑖 −1] , L) in the definition of persistent policy. By definition of 𝑘 1 , we further
                                     ′
know that ⌊𝜏 [:𝑖 −1] ⌋ L ⪯ ⌊𝜏 ′[:𝑗 ] ⌋ L where 𝑗 ′ is the index that corresponds to 𝑖 − 1 from the induction
hypothesis, as illustrated in the orange part in Figure 9b. Moreover, from the induction hypothesis
           ′
that 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 −1] , we know that all past outputs of 𝑥 must produce the same value, say 𝑛.
                                                             ′
Note that since 𝑥 is immutable, both 𝜏 [𝑖+1] and 𝜏 ′[ 𝑗 +1] will output the same value 𝑛. Hence, we let
𝑗 = 𝑗 ′ + 1 and have 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖+1] .                                                                 □

6     Implementation
Prior work such as Jif [38] provides fine-grained information flow control for a Java-like language,
but its implementation requires modifications to the programming language and relies on non-
standard compilation tools. To make our language and type system more accessible to end users,
we follow the approach of recent systems such as Cocoon [32], Carapace [12], and Filament [18],
which are implemented as Rust libraries without requiring language and compiler modifications.
   In particular, our prototype implementation is built on top of Filament [18], which provides
Jif-like fine-grained information flow control for Rust. Consequently, our implementation is fully
compatible with the standard Rust language and compiler.

6.1    Dynamic Release on Rust
The recent work Filament [18] presents a static information flow library in Rust that enforces
noninterference with no runtime checks. To attach a value with a label, a Filament program wraps
the value in a generic struct Label⟨𝑇 , 𝐿⟩, where 𝑇 is the data type and 𝐿 is a (static) security level
drawn from a predefined lattice. Filament uses traits to define the ordering of security levels (i.e.,
the lattice structure) based on these labels. However, Filament only supports static security levels.
   To support dynamic release labels, we expand the generic struct to support dynamic labels
and leverage Rust’s phantom types for compile-time checking. More specifically, we define our
label and value wrapper as a generic struct DRLabel⟨𝑇 , 𝑆, 𝐿𝐹𝑟𝑜𝑚, 𝐿𝑇𝑜⟩, representing data of type 𝑇
associated with a security label 𝑆?𝐿𝐹𝑟𝑜𝑚 → 𝐿𝑇𝑜 using the syntax in Figure 2, where 𝐿𝐹𝑟𝑜𝑚 and
𝐿𝑇𝑜 are security levels1 . Moreover, we maintain both a Boolean variable s and a unique type 𝑆 to
represent a security event. The difference is that s can be set by library functions eventon and
eventoff, while 𝑆 is a static type indicating s holds. The event trace 𝜎 is implemented as a vector
that tracks eventon/eventoff operations at runtime. The library function relabel only statically
1 Our current implementation does not support first-order functions; we leave this feature for future work (Section 8.2).



                          Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
    360:22                                                                                  Jeffrey Ching and Danfeng Zhang


1   impl<T, S, P, Pp, L> FlowsTo<DRLabel<T, S, L, L>>              1     impl<L, S, Q, Qq> FlowsTo<(DRLabel<(), S, Q, Qq>,
      for (DRLabel<T, S, P, Pp>, DynamicLabel<P, Pp>)                      DynamicLabel<Q, Qq>)> for DRLabel<(), S, L, L>
2       where Pp: LEQ<L>, SEvent<S>: Holds, {}                     2         where L: LEQ<Qq>, SEvent<S>: Holds {}
    (a) Implementing rule (R-From) with Rust’s trait.                      (b) Implementing rule (R-To) with Rust’s trait.

                              Fig. 10. Rule (R-From) and (R-To) from the implementation.


    checks information flow constraints with the assumption that 𝑆 holds when s is set; otherwise,
    it does nothing (see (OS-Relabel-Succ) and (OS-Relabel-Fail) in Figure 3). Similarly to prior
    works ([12, 18, 32]), our implementations of flows-to and release-to relations use Rust traits for
    compile-time checking as shown in Figure 10, covering the cases from the typing rules in Figures 5
    and 6. The trait implementation models the security lattice, and by encoding these rules directly in
    the security functions (relabel and Output), we are able to implement and type-check all secure
    examples throughout the paper with our prototype.
       Following Filament, our implementation also supports procedure calls, where labeled parameters
    and return values are statically checked. Consider the following example:
    1   fn pwd_reminder(..., mut password: DRLabel<
                                                               1       let password=DRLabel::<String, B1, S, P> {
          String, B1, S, P>,)-> DRLabel<String, B1, P, P
                                                               2           value: "secret123".to_string(),
          > {
                                                               3           cond: false,...};
    2     //set B1 if the user owns the password
                                                               4       let reminder = pwd_reminder(..., password);
    3     ...}
       The parameter password is annotated with the label B1?𝑆 → 𝑃, where the security event B1
    is set when the user owns the password. Our implementation statically checks that the label of
    the actual argument password does not exceed the corresponding annotation in pwd_reminder.
    Moreover, Rust’s type system automatically infers the label of reminder to match the function’s
    declared return label.
       For simplicity, our prototype currently lacks the following features (1) nested dynamic labels, (2)
    user-defined security events and (3) first-order functions. We plan to add them in future work.

    6.2      Case Studies
    To demonstrate the efficacy of dynamic release policy, we ported a conference management system
    written in Lifty [39] and Civitas [21, 30] (excluding its cryptography proof component) written
    in Jif in approximately 1,700 lines of Rust code on top of our prototype implementation. The
    evaluation demonstrates that, in contrast to prior systems, each built for a specific dynamic policy
    and its corresponding enforcement mechanism, our framework can accommodate a broader class
    of dynamic policies within the same type system. For example, Lifty supports only declassification
    policies and therefore cannot express erasure policies required by Civitas. The full implementation
    of the case studies is available in [16].
    6.2.1 Conference Reviewing system. HotCRP [31] is a widely used conference reviewing system
    with known security flaws [51]. Previous work Lifty [39] provides several code snippets that model
    the essence of those flaws in their Haskell-like domain specific language. Under the hood, Lifty
    detects such flaws by combining Labeled IO (LIO) [46] with Liquid Types [42]. We port the Lifty-
    based implementation with all core features such as score release, review release, and password
    reminder. Below, we discuss two representative examples.
       Password Disclosure. A representative security vulnerability in HotCRP involves password dis-
    closure [51]. HotCRP has two features. First, when a user forgets the password, HotCRP sends a
    reminder email to the user. Second, HotCRP has an email preview mode that allows an adminis-
    trator to display emails in the browser, including those reminder emails as shown in Figure 11b.

    Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                    360:23


 1    eventoff(&mut password);                              1 //password: ¬checkuser?S→ P, passcode:P
 2    if is_requester_owner(current_user,                   2 eventoff(checkuser);
        password_owner) {                                   3 if (isUser == true) {   //check user
 3      eventon(&mut password);                             4   eventon(checkuser);
 4      let relabel_result = relabel::< _, TrueB1, S,       5     passcode=relabel(password,"¬checkuser?S→ P"
        P, P, P > (&password, &conditions);                       to "P" using checkuser);
 5      relabel_result.assign_to(&mut passcode_out);        6     output(P, passcode, using checkuser);}
 6      output_to(&output_label, &passcode_out, &           7   else { // administrator
        conditions);}                                       8     passcode = password; //reject
 7    else {//reject, line 8-9 in pseudocode}               9     output(P, passcode, using checkuser);}//nop

       (a) Implementation on the password example.                 (b) Pseudocode of the password example.

                    Fig. 11. Password Disclosure Example from Conference Reviewing System.


Consequently, in the email preview mode, an administrator can trigger a reminder email, which
directly reveals a user’s password in the browser to the administrator [51].
   To prevent the accidental leak of a password, we assign it the label ¬checkuser?S →𝑡 P. This
label ensures the password remains at a high security level until a specific security event, checkuser,
is activated (eventon from line 3 in Figure 11a). To achieve this, the implementation checks the
functions relabel and output_to at compile time. This check is enforced by the flows-to relations:
if it compiles, then the execution reaches lines 4-6 in Figure 11b; otherwise, it fails to compile
according to the type system.
   Releasing papers’ score. The system checks other scenarios, including paper score release, which
is a microbenchmark used in Lifty [39]. This scenario requires that the paper’s score should be
visible only when the review is finished. To address this, the scores of the papers are labeled with
¬done?S →𝑡 P. The typing rule relabel checks the status indicator done, which determines when
the result can be viewed.
6.2.2 Secure voting system. Civitas [21, 30] is a secure voting system that enforces declassification
and erasure policies across four phases: setup, registration, voting, and tabulation. Prior case
studies [20] highlight two erasure scenarios involving credential shares by authorities and voters,
written in Jif [38]. We ported all Civitas components related to vote delivery and credential erasure.
   For authorities, the credentials must be removed to ensure voters’ anonymity after they are
delivered to the voters. Hence, we label credentials with ¬delivered?M → ⊤, so that the credential
must be erased after delivery. The output rule uses the fact that delivered has never been true (i.e.,
delivered)
  to check that the dynamic label can be released through the output channel.
   For voters, each share on the voter side is labeled with ¬postCombined?M → ⊤. After receiving
all the shares from the authorities and combining the shares, the voter should delete any record
provided by the authorities. The proof tree for output is the same as the previous example. The
code is available in [16].

6.3     Performance and Correctness
We implemented the semantics shown in Figure 3 for the novel constructs introduced in our
language. Since the unique semantics require tracking a trace of security events and evaluating
event conditions at runtime, our approach may introduce additional runtime overhead. To assess
this overhead, we measured the median execution time over 100 runs for both the original and the
verified Rust implementations across our case studies. The results are shown below.
   The evaluation results suggest that the overhead is low. We attribute the low overhead to the fact
that even though the event trace grows during program execution, the overall overhead remains

                          Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:24                                                                              Jeffrey Ching and Danfeng Zhang


                                                      Original     IFC
                                      conference       0.029ms 0.033ms
                                      Civitas          5.694ms 5.736ms

low as (1) event trace only grows with eventon/eventoff, and output commands, and (2) the trace
is only checked with a relabel command. Since both kinds of policy-specific commands occur
infrequently in practice, the overall overhead remains low.
   Moreover, because relabel and output commands may alter program semantics when the
corresponding using clauses are not satisfied, we verified that all case studies produce the same
outputs as the original programs without information flow control.

7     Related Work
   Dynamic Policies. To address the limitations of noninterference, prior work introduces various
mechanisms [7, 8, 19–21] to allow information sensitivity/integrity to change over time. Additional
studies include extensions to gradual release [10], temporally verified logic [9], and security-specific
languages [28, 48], which support role-based information flow policies with dynamic updates. These
works enable flexible label updates while accommodating both Denning-style and role-based lattices.
Recent work [14] introduces nonmalleable progress leakage, adapting nonmalleable information
flow to secure progress channels for downgrading policies. More recently, Ahmadian [1] introduced
an attacker knowledge-based information flow policy. Zegarelli et al. [52] propose a modular
enforcement mechanism that supports multiple interpretations of facets within a single framework.
In contrast, our work uses the dynamic release policy [34], which provides a uniform formalization
of various dynamic policies.
   Enforcement of Dynamic Policies in Applications. Building on Myers’ influential work [36] in
establishing a formal semantics for decentralized labels, various applications have been built on
top of Jif [38], including some that involve dynamic policies such as declassification and erasure.
Dynamic policies are also widely used in systems research. Guarnieri et al. [26, 27] explore the
“forgetful attacker” model [4] to implement declassification via a security monitor. In addition,
dynamic policies have been applied to applications such as conference reviewing systems [39, 46],
Battleship Game [38, 47], and social media platforms [11].
   In comparison, our dynamic release Rust library constitutes the first approach capable of ex-
pressing and verifying the full range of such policies. A detailed comparison with dynamic release
policy and other variants of dynamic policies can be found in [34].
   Soundness Proof. Most information flow policies enforce noninterference, and are typically
enforced via static type systems, whose soundness has been proven using both big- and small-step
semantics [15, 25, 33, 40, 41, 49]. As discussed in Section 5, these proof techniques are not directly
applicable to dynamic policies.
   Prior work in dynamic policies, notably [20], established the soundness of static enforcement
for declassification and erasure. Unlike [20], which uses two separate sets of rules, our dynamic
release policy is a superset of those supported policies and provides a single set of rules for various
dynamic policies. Furthermore, differences in policy formalization mean that the soundness proof
of [20] is not applicable to our dynamic release enforcement.

8     Discussion and Future work
8.1      Annotation Burden
In this paper, we assume that using clauses are provided by programmers. From the programmer’s
perspective, an appropriate annotation should specify, for each output and relabel command: (1)

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                 360:25


the conditions under which information may be released safely, thereby enabling the command to
satisfy the typing rules (Section 4.4); and (2) the conditions that hold at the corresponding program
point, ensuring that the annotated program exhibits the same behavior as the original program
whenever the original program is secure (Section 3.2). Across all of our case studies (Section 6),
these conditions are sufficiently simple to identify and annotate manually. However, constructing
such annotations may become more challenging in large code bases. Hence, an important direction
for future work is the automatic inference of using clauses through static analysis. Our language
design is well suited to this objective because security events are explicitly distinguished from
ordinary program variables and can only be modified by the eventon and eventoff commands
(Section 3.1). This separation enables a compositional inference strategy that we plan to explore: an
intraprocedural dataflow analysis can propagate event-related facts along the control-flow graph
to infer conditions that must hold at each program point, while the effect of each procedure on
security events can be summarized independently by the set of events it may modify.
   Moreover, our type system currently does not support label inference. Consequently, all label
annotations, including the “from” and “to” labels in relabel commands, must be provided explicitly
by programmers. A promising direction for future work is to extend the language with automatic
label inference by formulating the flows-to relation as a system of constraints to be solved by
a constraint solver. The primary challenge lies in the presence of dynamic release labels, which
introduce dependencies among these constraints and substantially complicate the inference process.
Addressing such dependencies is beyond the capabilities of our current Rust-based implementation.


8.2    Language Features
Our primary goal is to establish a theoretical foundation for enforcing dynamic release policies.
In this context, the use of a minimal imperative language is deliberate and consistent with prior
type systems that come with formal soundness proofs. Building on this foundation, an important
direction for future work is to extend both the source language and the type system with more
expressive language features, such as first-class functions and heap manipulation. In pursuing these
extensions, we plan to draw on established designs such as Jif [38] and Cocoon [32].
   For example, supporting first-class functions requires assigning security labels to those functions
(including their parameters, return values, and side effects) just as for any other value in the
program. These labels capture the security constraints governing the use of a function, such as the
maximum sensitivity of its arguments and the minimum security level of the 𝑝𝑐 context in which it
may be invoked securely. In the setting of dynamic release policies, an additional challenge arises
because these constraints also depend on the state of security events at the call site. Consequently,
the annotation may also require a using clause, specifying the necessary event states to ensure
that function invocations remain secure.


9     Conclusion
In this paper, we present the first sound enforcement of the dynamic release policy introduced
by Li and Zhang [34]. Compared to prior enforcements of dynamic policies, which are based on
ad hoc, policy-specific enforcement mechanisms, our work offers simple, intuitive, and unified
enforcement of various dynamic policies, such as declassification, endorsement, and erasure poli-
cies. We developed a metalanguage with carefully designed features, such as relabel, eventon,
eventoff commands for writing code governed by embedded dynamic release policies. We further
developed a type system that is formally proven to soundly enforce dynamic release policies, and
implemented a prototype as an extension to Rust.

                        Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:26                                                                                 Jeffrey Ching and Danfeng Zhang


Data Availability Statement
An initial artifact for this paper consists of the prototype and the case studies from Section 6. A
version of the source code is available at the link [16]. The full proof can be found in [17].

Acknowledgments
We would like to express our gratitude to the anonymous reviewers for their insightful feedback
and suggestions. We also appreciate the insights from Peixuan Li and Quan Zhou. This research is
sponsored by National Science Foundation grants CNS 2401496 and CNS 2401182.

References
 [1] Amir M Ahmadian and Musard Balliu. 2022. Dynamic policies revisited. In 2022 IEEE 7th European Symposium on
     Security and Privacy (EuroS&P). IEEE, 448–466. doi:10.1109/EuroSP53844.2022.00035
 [2] Alfred V. Aho, Monica S. Lam, Ravi Sethi, and Jeffrey D. Ullman. 2007. Compilers: Principles, Techniques & Tools (2nd
     ed.). Pearson Education, Boston, MA, USA.
 [3] Owen Arden, Jinyang Liu, and Andrew C. Myers. 2015. Flow-Limited Authorization. In 2015 IEEE 28th Computer
     Security Foundations Symposium (CSF). IEEE, 569–583. doi:10.1109/CSF.2015.42
 [4] Aslan Askarov and Stephen Chong. 2012. Learning is Change in Knowledge: Knowledge-based Security for Dynamic
     Policies. In 2012 IEEE 25th Computer Security Foundations Symposium. IEEE, 308–322. doi:10.1109/CSF.2012.31
 [5] Aslan Askarov, Sebastian Hunt, Andrei Sabelfeld, and David Sands. 2008. Termination-insensitive noninterference
     leaks more than just a bit. In Computer Security – ESORICS 2008: 13th European Symposium on Research in Computer
     Security, Málaga, Spain, October 6–8, 2008. Proceedings. Springer, 333–348. doi:10.1007/978-3-540-88313-5_22
 [6] Aslan Askarov, Scott Moore, Christos Dimoulas, and Stephen Chong. 2015. Cryptographic Enforcement of Language-
     based Information Erasure. In 2015 IEEE 28th Computer Security Foundations Symposium (CSF). IEEE, 334–348. doi:10.
     1109/CSF.2015.30
 [7] Aslan Askarov and Andrei Sabelfeld. 2007. Gradual Release: Unifying Declassification, Encryption and Key Release
     Policies. In 2007 IEEE Symposium on Security and Privacy (SP’07). IEEE, 207–221. doi:10.1109/SP.2007.22
 [8] Aslan Askarov and Andrei Sabelfeld. 2009. Tight Enforcement of Information-Release Policies for Dynamic Languages.
     In 2009 22nd IEEE Computer Security Foundations Symposium. IEEE, 43–59. doi:10.1109/CSF.2009.22
 [9] Musard Balliu, Mads Dam, and Gurvan Le Guernic. 2011. Epistemic Temporal Logic for Information Flow Security. In
     Proceedings of the ACM SIGPLAN 6th Workshop on Programming Languages and Analysis for Security (PLAS). ACM,
     1–12. doi:10.1145/2166956.2166962
[10] Anindya Banerjee, David A. Naumann, and Stan Rosenberg. 2008. Expressive Declassification Policies and Modular
     Static Enforcement. In 2008 IEEE Symposium on Security and Privacy (SP 2008). IEEE, 339–353. doi:10.1109/SP.2008.20
[11] Thomas Bauereiss, Armando Pesenti Gritti, Andrei Popescu, and Franco Raimondi. 2018. CoSMed: A confidentiality-
     verified social media platform. Journal of Automated Reasoning 61 (2018), 113–139. doi:10.1007/s10817-017-9443-3
[12] Vincent Beardsley, Chris Xiong, Ada Lamba, and Michael D Bond. 2025. Carapace: Static–Dynamic Information Flow
     Control in Rust. Proceedings of the ACM on Programming Languages 9, OOPSLA1 (2025), 364–392. doi:10.1145/3720427
[13] Niklas Broberg, Bart van Delft, and David Sands. 2015. The Anatomy and Facets of Dynamic Policies. In 2015 IEEE
     28th Computer Security Foundations Symposium (CSF). IEEE, 122–136. doi:10.1109/CSF.2015.16
[14] Ethan Cecchetti. 2025. Nonmalleable Progress Leakage. In 2025 IEEE 38th Computer Security Foundations Symposium
     (CSF). IEEE, 537–552. doi:10.1109/CSF64896.2025.00029
[15] Ethan Cecchetti, Siqiu Yao, Haobin Ni, and Andrew C. Myers. 2021. Compositional Security for Reentrant Applications.
     In 2021 IEEE Symposium on Security and Privacy (SP). IEEE, 1249–1267. doi:10.1109/SP40001.2021.00084
[16] Jeffrey Ching and Danfeng Zhang. 2026. Sound Enforcement of Dynamic Release Information Flow Policy Artifact.
     doi:10.5281/zenodo.21943585
[17] Jeffrey C. Ching and Danfeng Zhang. 2026. Sound Enforcement of Dynamic Release Information Flow Policy – Full
     Version. arXiv preprint arXiv:2608.09506 (2026). arXiv:2608.09506
[18] Jeffrey C Ching, Quan Zhou, and Danfeng Zhang. 2026. Filament: Denning-Style Information Flow Control for Rust.
     arXiv preprint arXiv:2604.14357 (2026). arXiv:2604.14357
[19] Stephen Chong and Andrew C. Myers. 2005. Language-Based Information Erasure. In Proceedings of the 18th IEEE
     Computer Security Foundations Workshop (CSFW). IEEE, 241–254. doi:10.1109/CSFW.2005.19
[20] Stephen Chong and Andrew C. Myers. 2008. End-to-End Enforcement of Erasure and Declassification. In Proceedings
     of the 21st IEEE Computer Security Foundations Symposium (CSF). IEEE, 98–111. doi:10.1109/CSF.2008.12
[21] Michael R. Clarkson, Stephen Chong, and Andrew C. Myers. 2008. Civitas: Toward a Secure Voting System. In 2008
     IEEE Symposium on Security and Privacy (SP 2008). IEEE, 354–368. doi:10.1109/SP.2008.32


Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                       360:27


[22] Dorothy E Denning. 1976. A lattice model of secure information flow. Commun. ACM 19, 5 (1976), 236–243. doi:10.
     1145/360051.360056
[23] David Ferraiolo, Janet Cugini, and D. Richard Kuhn. 1995. Role-based Access Control (RBAC): Features and Motivations.
     In Proceedings of the 11th Annual Computer Security Applications Conference (ACSAC). IEEE Computer Society, 241–248.
[24] Joseph A. Goguen and José Meseguer. 1982. Security Policies and Security Models. In Proceedings of the 1982 IEEE
     Symposium on Security and Privacy (SP). IEEE, 11–20. doi:10.1109/SP.1982.10014
[25] Simon Oddershede Gregersen, Johan Bay, Amin Timany, and Lars Birkedal. 2021. Mechanized logical relations for
     termination-insensitive noninterference. Proceedings of the ACM on Programming Languages 5, POPL (2021), 1–29.
     doi:10.1145/3434291
[26] Marco Guarnieri, Musard Balliu, Daniel Schoepe, David Basin, and Andrei Sabelfeld. 2019. Information-Flow Control
     for Database-Backed Applications. In 2019 IEEE European Symposium on Security and Privacy (EuroS&P). IEEE, 79–94.
     doi:10.1109/EuroSP.2019.00016
[27] Marco Guarnieri, Srdjan Marinovic, and David Basin. 2016. Strong and Provably Secure Database Access Control. In
     2016 IEEE European Symposium on Security and Privacy (EuroS&P). IEEE, 163–178. doi:10.1109/EuroSP.2016.23
[28] Michael Hicks, Stephen Tse, Boniface Hicks, and Steve Zdancewic. 2005. Dynamic updating of information-flow
     Policies. In Proceedings of the International Workshop on Foundations of Computer Security (FCS). 7–18.
[29] Catalin Hritcu, John Hughes, Benjamin C Pierce, Antal Spector-Zabusky, Dimitrios Vytiniotis, Arthur Azevedo de
     Amorim, and Leonidas Lampropoulos. 2013. Testing noninterference, quickly. ACM SIGPLAN Notices 48, 9 (2013),
     455–468. doi:10.1145/2500365.2500574
[30] Ari Juels, Dario Catalano, and Markus Jakobsson. 2005. Coercion-Resistant Electronic Elections. In Proceedings of the
     2005 ACM Workshop on Privacy in the Electronic Society (WPES). ACM, 61–70. doi:10.1145/1102199.1102213
[31] Eddie Kohler. 2013. HotCRP. https://hotcrp.com/. Accessed: 19 September 2025.
[32] Ada Lamba, Max Taylor, Vincent Beardsley, Jacob Bambeck, Michael D Bond, and Zhiqiang Lin. 2024. Cocoon: Static
     Information Flow Control in Rust. Proceedings of the ACM on Programming Languages 8, OOPSLA1 (2024), 166–193.
     doi:10.1145/3649817
[33] Peixuan Li and Danfeng Zhang. 2017. Towards a Flow- and Path-Sensitive Information Flow Analysis: Technical
     Report. arXiv preprint arXiv:1706.01407 (2017). arXiv:1706.01407
[34] Peixuan Li and Danfeng Zhang. 2022. Towards a General-Purpose Dynamic Information Flow Policy. In 2022 IEEE 35th
     Computer Security Foundations Symposium (CSF). IEEE, 260–275. doi:10.1109/CSF54842.2022.9919639
[35] Andrew C Myers and Barbara Liskov. 1997. A decentralized model for information flow control. ACM SIGOPS Operating
     Systems Review 31, 5 (1997), 129–142. doi:10.1145/269005.266669
[36] Andrew C. Myers and Barbara Liskov. 1998. Complete, safe information flow with decentralized labels. In Proceedings
     of the 1998 IEEE Symposium on Security and Privacy (SP). IEEE, 186–197. doi:10.1109/SECPRI.1998.674834
[37] Andrew C Myers and Barbara Liskov. 2000. Protecting privacy using the decentralized label model. ACM Transactions
     on Software Engineering and Methodology (TOSEM) 9, 4 (2000), 410–442. doi:10.1145/363516.363526
[38] Andrew C. Myers, Lantian Zheng, Steve Zdancewic, Stephen Chong, and Nathaniel Nystrom. 2006. Jif 3.0: Java
     information flow. (July 2006). http://www.cs.cornell.edu/jif
[39] Nadia Polikarpova, Deian Stefan, Jean Yang, Shachar Itzhaky, Travis Hance, and Armando Solar-Lezama. 2020. Liquid
     information flow control. Proceedings of the ACM on Programming Languages 4, ICFP (2020), 1–30. doi:10.1145/3408987
[40] François Pottier and Vincent Simonet. 2002. Information Flow Inference for ML. In Proceedings of the 29th ACM
     SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL). ACM, Portland, OR, USA, 319–330.
     doi:10.1145/503272.503302
[41] Vineet Rajani and Deepak Garg. 2020. On the expressiveness and semantics of information flow types. Journal of
     Computer Security 28, 1 (2020), 129–156. doi:10.3233/JCS-191382
[42] Patrick M Rondon, Ming Kawaguci, and Ranjit Jhala. 2008. Liquid types. In Proceedings of the 29th ACM SIGPLAN
     Conference on Programming Language Design and Implementation. ACM, 159–169. doi:10.1145/1375581.1375602
[43] Andrei Sabelfeld and Andrew C. Myers. 2003. Language-based information-flow security. IEEE Journal on Selected
     Areas in Communications 21, 1 (January 2003), 5–19. doi:10.1109/JSAC.2002.806121
[44] Andrei Sabelfeld and David Sands. 2005. Dimensions and principles of declassification. In 18th IEEE Computer Security
     Foundations Workshop (CSFW’05). IEEE, 255–269. doi:10.1109/CSFW.2005.15
[45] Andrei Sabelfeld and David Sands. 2009. Declassification: Dimensions and principles. Journal of Computer Security 17,
     5 (2009), 517–548. doi:10.3233/JCS-2009-0352
[46] Deian Stefan, Alejandro Russo, John C. Mitchell, and David Mazières. 2011. Flexible Dynamic Information Flow Control
     in Haskell. In Proceedings of the 4th ACM Symposium on Haskell. ACM, 95–106. doi:10.1145/2096148.2034688
[47] Alley Stoughton, Andrew Johnson, Samuel Beller, Karishma Chadha, Dennis Chen, Kenneth Foner, and Michael
     Zhivich. 2014. You sank my battleship! A case study in secure programming. In Proceedings of the Ninth Workshop on
     Programming Languages and Analysis for Security. ACM, 2–14. doi:10.1145/2637113.2637115


                          Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:28                                                                               Jeffrey Ching and Danfeng Zhang


[48] Nikhil Swamy, Michael Hicks, Stephen Tse, and Steve Zdancewic. 2006. Managing policy updates in security-typed
     languages. In 19th IEEE Computer Security Foundations Workshop (CSFW’06). IEEE, 13–pp. doi:10.1109/CSFW.2006.17
[49] Dennis Volpano, Cynthia Irvine, and Geoffrey Smith. 1996. A sound type system for secure flow analysis. Journal of
     computer security 4, 2-3 (1996), 167–187. doi:10.3233/JCS-1996-42-304
[50] Lucas Waye, Pablo Buiras, Owen Arden, Alejandro Russo, and Stephen Chong. 2017. Cryptographically Secure
     Information Flow Control on Key-Value Stores. In Proceedings of the 2017 ACM SIGSAC Conference on Computer and
     Communications Security (CCS). ACM, 1893–1907. doi:10.1145/3133956.3134036
[51] Alexander Yip, Xi Wang, Nickolai Zeldovich, and M. Frans Kaashoek. 2009. Improving Application Security with Data
     Flow Assertions. In Proceedings of the ACM SIGOPS 22nd Symposium on Operating Systems Principles (SOSP). ACM,
     291–304. doi:10.1145/1629575.1629604
[52] Antonio Zegarelli, Niki Vazou, and Marco Guarnieri. 2024. Modular Implementation and Formalization of Dynamic
     Policies: Work in Progress. In Proceedings of the 2024 Workshop on Foundations of Computer Security (FCS). Informal
     Proceedings.




Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                           360:1


                                                      ⟨𝑚, 𝑒 1 ⟩ ⇓ 𝑛 1       ⟨𝑚, 𝑒 2 ⟩ ⇓ 𝑛 2         𝑛 3 = 𝑛 1 op 𝑛 2
      ⟨𝑚, 𝑛⟩ ⇓ 𝑛             ⟨𝑚, 𝑥⟩ ⇓ 𝑚(𝑥)                               ⟨𝑚, 𝑒 1 op 𝑒 2 ⟩ ⇓ 𝑛 3

                                     Fig. 12. Big-Step Semantics of Expression


                                                                         OS-Seqence
                             OS-Skip                                           ⟨𝑚, 𝑐 1, 𝜎⟩ → ⟨𝑚 ′, 𝑐 1′ , 𝜎 ′ ⟩
                              ⟨𝑚, skip; 𝑐, 𝜎⟩ → ⟨𝑚, 𝑐, 𝜎⟩                ⟨𝑚, 𝑐 1 ; 𝑐 2, 𝜎⟩ → ⟨𝑚 ′, 𝑐 1′ ; 𝑐 2, 𝜎 ′ ⟩

     OS-Assign                                             OS-If-True
                     ⟨𝑚, 𝑒 1 ⟩ ⇓ 𝑛                                              ⟨𝑚, 𝑒⟩ ⇓ true
     ⟨𝑚, 𝑥 := 𝑒 1, 𝜎⟩ → ⟨𝑚[𝑥 := 𝑛], skip, 𝜎⟩               ⟨𝑚, if (𝑒) then 𝑐 1 else 𝑐 2, 𝜎⟩ → ⟨𝑚, 𝑐 1, 𝜎⟩

                                OS-If-False
                                                 ⟨𝑚, 𝑒⟩ ⇓ false
                                ⟨𝑚, if (𝑒) then 𝑐 1 else 𝑐 2, 𝜎⟩ → ⟨𝑚, 𝑐 2, 𝜎⟩

            OS-While

             ⟨𝑚, while (𝑒) do 𝑐, 𝜎⟩ → ⟨𝑚, if (𝑏) then (𝑐; while (𝑏) do 𝑐) else skip, 𝜎⟩

               OS-Output-Succ                                  (
                               ∀𝑖 ∈ 0...𝑘.                      𝜎 · ox @L, 𝑒 is a variable 𝑥
                ⟨𝑚, 𝑒⟩ ⇓ 𝑣                        𝜎′ =
                               eval(si, 𝜎) = true               𝜎,         otherwise
                                                                    ⟨𝐿,𝑣,𝜎 ⟩
                        ⟨𝑚, output(𝐿, 𝑒, using s0 . . . sk ), 𝜎⟩ −−−−−→ ⟨𝑚, skip, 𝜎⟩

 OS-Output-fail
                             ∃𝑖 ∈ 0...𝑘.
           ⟨𝑚, 𝑒⟩ ⇓ 𝑣                                                   OS-eventon
                             eval(si, 𝜎) = false
                                                                        ⟨𝑚, eventon(s), 𝜎⟩ → ⟨𝑚, skip, 𝜎 · s⟩
  ⟨𝑚, output(𝐿, 𝑒, using s0 . . . sk ), 𝜎⟩ →
                                           − ⟨𝑚, skip, 𝜎⟩

                                 OS-eventoff
                                 ⟨𝑚, eventoff(s), 𝜎⟩ → ⟨𝑚, skip, 𝜎 · ¬s⟩

              OS-Relabel-Succ
                               ⟨𝑚, 𝑒⟩ ⇓ 𝑛        ∀𝑖 ∈ 0...𝑘. eval(si, 𝜎) = true
              ⟨𝑚, 𝑥 := relabel(𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ → ⟨𝑚[𝑥 := 𝑛], skip, 𝜎⟩

                   OS-Relabel-Fail
                                        ∃𝑖 ∈ 0...𝑘. eval(si, 𝜎) = false
                   ⟨𝑚, 𝑥 := relabel(𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ → ⟨𝑚, skip, 𝜎⟩

                                 Fig. 13. Operational Semantics for Commands




                        Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:2                                                                                   Jeffrey Ching and Danfeng Zhang


                                             General Lattice Rules
                            Lattice                            Trans
                               𝐿 ⊑ 𝐿′                          ⊢𝑝 ⊏
                                                                  ∼𝑝
                                                                     ′
                                                                                  ⊢ 𝑝′ ⊏
                                                                                       ∼𝑝
                                                                                          ′′

                                        ′                                       ′′
                            𝑆 ⊢𝐿⊏
                                ∼𝐿                                      𝑆 ⊢𝑝 ⊏
                                                                             ∼𝑝
                                         Directional Inference Rules
               R-To                               D-To
                                ′
               𝑆 ⊨ ¬s2     ⊢𝐿⊏
                             ∼𝑞                   𝑆 ⊨ ¬s2          ¬s1 ⇒ ¬s2            ⊢ s1 ?𝐿 → 𝑝 ′ ⊏
                                                                                                      ∼𝑞
                                                                                                         ′

                                   ′
                𝑆 ⊢𝐿⊏
                    ∼ s2 ?𝑞 → 𝑞                                𝑆 ⊢ s1 ?𝐿 → 𝑝 ∼ s2 ?𝑞 → 𝑞 ′
                                                                                  ′ ⊏


               R-From                             D-From
               𝑆 ⊨ ¬s1     ⊢ 𝑝′ ⊏
                                ∼𝐿                𝑆 ⊨ ¬s1           ¬s2 ⇒ ¬s1           ⊢ 𝑝′ ⊏
                                                                                             ∼ s2 ?𝐿 → 𝑞
                                                                                                         ′

                𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                                ∼𝐿                             𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                                                                               ∼ s2 ?𝐿 → 𝑞
                                                                                           ′


          D-To Two                            R-To Two
           𝑆 ⊢𝑝 ⊏
                ∼𝐿       ⊢ 𝑝′ ⊏
                              ∼𝐿              ¬s2 ⇒ ¬s1         𝑆 ⊢𝑝 ⊏
                                                                     ∼ s2 ?𝑞 → 𝑞
                                                                                 ′
                                                                                             ⊢ 𝑝′ ⊏
                                                                                                  ∼ s2 ?𝑞 → 𝑞
                                                                                                              ′

            𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                            ∼𝐿                                𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                                                                              ∼ s2 ?𝑞 → 𝑞
                                                                                          ′


          D-From Two                         R-From Two
                              ′
           𝑆 ⊢𝐿⊏
               ∼𝑝        ⊢𝐿⊏
                           ∼𝑝                 ¬s1 ⇒ ¬s2        𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                                                                               ∼𝑞            ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                                                                                                           ∼𝑞
                                                                                                              ′

                            ′
            𝑆 ⊢𝐿⊏
                ∼ s2 ?𝑞 → 𝑞                                   𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏
                                                                              ∼ s2 ?𝑞 → 𝑞
                                                                                          ′


                                        Bi-directional Inference Rules
    Bi-To                              Bi-From                              Bi-Both
                           ′
    ⊢𝐿⊏
      ∼𝑞              ⊢𝐿⊏
                        ∼𝑞             ⊢𝑝 ⊏
                                          ∼𝐿         ⊢ 𝑝′ ⊏
                                                          ∼𝐿                s1 ⇔ s2          ⊢𝑝 ⊏
                                                                                                ∼𝑞       ⊢ 𝑝′ ⊏
                                                                                                              ∼𝑞
                                                                                                                 ′

                        ′
        𝑆 ⊢𝐿⊏
            ∼ s2 ?𝑞 ↔ 𝑞                 𝑆 ⊢ s1 ?𝑝 ↔ 𝑝 ′ ⊏
                                                        ∼𝐿                       𝑆 ⊢ s1 ?𝑝 ↔ 𝑝 ′ ⊏
                                                                                                 ∼ s2 ?𝑞 ↔ 𝑞
                                                                                                             ′



 Fig. 14. In top-down order, these are the general rules, the directional inference rules, and bidirectional rules.



                                            Op                                                   SubType
         Var              Num               Γ ⊢ 𝑒1 : 𝑝1      Γ ⊢ 𝑒2 : 𝑝2         ⊢ 𝑝1 ⊏
                                                                                      ∼ 𝑝2       Γ ⊢𝑒 :𝑝      ⊢𝑝 ⊏
                                                                                                                 ∼𝑝
                                                                                                                    ′

         Γ ⊢ 𝑥 : Γ(𝑥)      Γ ⊢𝑛 :⊥                        Γ ⊢ 𝑒 1 op 𝑒 2 : 𝑝 2                         Γ ⊢ 𝑒 : 𝑝′

                                        Fig. 15. Typing Rules for Expressions.



A       Full Operational Semantics of Expressions and Commands
Figure 12 and Figure 13 present the full operational semantics.

B       Full Static Flows-to Rules
Figure 14 presents the full static flows-to rules.

C       Typing Rules for Expressions
The typing rules for expressions are in Figure 15.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                                            360:3


D     Soundness of Flows-To and Release-To Relation
  Theorem (Local Soundness, Theorem 1). For all policies p and q, a trace 𝜎, a set of security
events 𝑆 = s0 . . . sk , if 𝑆 ⊢ 𝑝 ⊏
                                  ∼ 𝑞 and 𝑆 holds on 𝜎, then 𝑝 ⊑𝜎 𝑞.
    Proof. By Definition 1, it is sufficient to show that for any 𝜎 ′ such that 𝜎 ⪯ 𝜎 ′ , we have
{|𝑝 }| 𝜎 ′ ⊑ {|𝑞|}𝜎 ′ . The proof is by induction on the static inference rules:
       • (Lattice) (𝑆 ⊢ 𝐿 ⊏                   ′
                                       ∼ 𝐿 ): It is trivial.
       • (Trans) (𝑆 ⊢ 𝑝 ⊏                  ′′
                                    ∼ 𝑝 ): It is trivial.
       • (R-To) (𝑆 ⊢ 𝐿 ⊏          ∼ s2 ?𝑞 →   − 𝑞 ′ ): By the assumption, we have ⊢ 𝐿 ⊏                ′
                                                                                                   ∼ 𝑞 and 𝑆 ⊨ ¬s2 . Since 𝑆 holds
           on 𝜎 by assumption, 𝜎 ⪯ 𝜎 , and 𝑆 ⊨ ¬s2 , there must be some index 𝑖 on 𝜎 ′ at which s2 first
                                                      ′

           turns false. According to the semantics of Figure 4, we know that {|s2 ?𝑞 → 𝑞 ′ }| 𝜎 ′ = {|𝑞 ′ }| 𝜎 ′[𝑖:] .
           From the induction hypothesis and the assumption that ⊢ 𝐿 ⊏                                ′                           ′
                                                                                                   ∼ 𝑞 , we get {|𝐿|}𝜎 ′[𝑖:] ⊑ {|𝑞 }| 𝜎 ′[𝑖:] .
                                                             ′
           Hence, {|𝐿|}𝜎 ′ = 𝐿 = {|𝐿|}𝜎 ′[𝑖:] ⊑ {|𝑞 }| 𝜎 ′[𝑖:] = {|s2 ?𝑞 → 𝑞 }| 𝜎 ′ .′

       • (R-From) Symmetric to the case above.
       • (D-To) Similar to (R-To), we first derive {|s2 ?𝑞 → 𝑞 ′ }| 𝜎 ′ = {|𝑞 ′ }| 𝜎 ′[𝑖:] from the assumptions,
           where 𝑖 is the index when s2 first turns false.
           If s1 has been false on 𝜎 ′ , let 𝑗 be the index when it turns false the first time. Since ¬s1 ⇒
           ¬s2 , it is guaranteed that 𝑗 ≥ 𝑖. According to the semantics of Figure 4, we know that
           {|s1 ?𝐿 → 𝑝 ′ }| 𝜎 ′ = {|𝑝 ′ }| 𝜎 ′[ 𝑗 :] = {|s1 ?𝐿 → 𝑝 ′ }| 𝜎 ′[𝑖:] where the second equation holds as s1 must
           remain true between 𝑖 and 𝑗. Moreover, from the induction hypothesis and the assumption
           ⊢ s1 ?𝐿 → 𝑝 ′ ⊏                ′                                       ′              ′
                                   ∼ 𝑞 , we know that {|s1 ?𝐿 → 𝑝 }| 𝜎 ′[𝑖:] ⊑ {|𝑞 }| 𝜎 ′[𝑖:] . Hence {|s1 ?𝐿 → 𝑝 }| 𝜎 ′ =
                                                                                                                                  ′
                             ′                  ′                      ′
           {|s1 ?𝐿 → 𝑝 }| 𝜎 ′[𝑖:] ⊑ {|𝑞 }| 𝜎 ′[𝑖:] = {|s2 ?𝑞 → 𝑞 }| 𝜎 ′ .
           If s1 has never been false on 𝜎 ′ , we know that {|s1 ?𝐿 → 𝑝 ′ }| 𝜎 ′ = 𝐿 = {|s1 ?𝐿 → 𝑝 ′ }| 𝜎 ′[𝑖:] . From
           the induction hypothesis and the assumption ⊢ s1 ?𝐿 → 𝑝 ′ ⊏                                    ′
                                                                                                     ∼ 𝑞 , we know that {|s1 ?𝐿 →
           𝑝 }| 𝜎 ′[𝑖:] ⊑ {|𝑞 }| 𝜎 ′[𝑖:] . Hence {|s1 ?𝐿 → 𝑝 }| 𝜎 ′ = {|s1 ?𝐿 → 𝑝 }| 𝜎 ′[𝑖:] ⊑ {|𝑞 ′ }| 𝜎 ′[𝑖:] = {|s2 ?𝑞 → 𝑞 ′ }| 𝜎 ′ .
             ′                  ′                                 ′                     ′

       • (D-From) Symmetric to the case above.
       • (D-To Two) (𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏                  ∼ 𝐿): By the assumption, we have 𝑆 ⊢ 𝑝 ⊏              ∼ 𝐿 and ⊢ 𝑝 ⊏
                                                                                                                             ′
                                                                                                                               ∼ 𝐿.
                                                    ′                                              ′
           If s1 has been false on 𝜎 , let 𝑖 be the first such index on 𝜎 . By the semantics of Figure 4,
           we have {|s1 ?𝑝 → 𝑝 ′ }| 𝜎 ′ = {|𝑝 ′ }| 𝜎 ′[𝑖:] . From the induction hypothesis we can derive that
           {|𝑝 ′ }| 𝜎 ′[𝑖:] ⊑ {|𝐿|}𝜎 ′[𝑖:] = 𝐿 = {|𝐿|}𝜎 ′ . So {|s1 ?𝑝 → 𝑝 ′ }| 𝜎 ′ ⊑ {|𝐿|}𝜎 ′ .
           If s1 has never been false on 𝜎 ′ , by the semantics of Figure 4, we have {|s1 ?𝑝 → 𝑝 ′ }| 𝜎 ′ = {|𝑝 }| 𝜎 ′ .
           From the induction hypothesis we can derive that {|𝑝 }| 𝜎 ′ ⊑ {|𝐿|}𝜎 ′ . So {|s1 ?𝑝 → 𝑝 ′ }| 𝜎 ′ ⊑ {|𝐿|}𝜎 ′ .
       • (D-From Two) Symmetric to the case above.
       • (R-To Two) (𝑆 ⊢ s1 ?𝑝 → 𝑝 ′ ⊏                                ′
                                                        ∼ s2 ?𝑞 → 𝑞 ): By the assumption, we have 𝑆 ⊢ 𝑝 ⊏                 ∼ s2 ?𝑞 → 𝑞
                                                                                                                                            ′

           and ⊢ 𝑝 ⊏      ′                   ′
                            ∼ s2 ?𝑞 → 𝑞 .
           If s2 has been false on 𝜎 ′ and let 𝑖 be the first such index on 𝜎 ′ . Since ¬s2 ⇒ ¬s1 , it is
           guaranteed that s1 has been false on 𝜎 ′ with the first index 𝑗 such that 𝑗 ≤ 𝑖. According to the
           semantics of Figure 4, we know that {|s2 ?𝑞 → 𝑞 ′ }| 𝜎 ′ = {|𝑞 ′ }| 𝜎 ′[𝑖:] = {|s2 ?𝑞 → 𝑞 ′ }| 𝜎 ′[ 𝑗 :] where the
           second equation holds as s2 must remain true between 𝑗 and 𝑖. Moreover, from the induction
           hypothesis and the assumption ⊢ 𝑝 ′ ⊏                                  ′                        ′                      ′
                                                                ∼ s2 ?𝑞 → 𝑞 , we know that {|𝑝 }| 𝜎 ′[ 𝑗 :] ⊑ {|s2 ?𝑞 → 𝑞 }| 𝜎 ′[ 𝑗 :] .
                                        ′             ′                         ′
           Hence {|s1 ?𝑝 → 𝑝 }| 𝜎 ′ = {|𝑝 }| 𝜎 ′[ 𝑗 :] ⊑ {|s2 ?𝑞 → 𝑞 }| 𝜎 ′[ 𝑗 :] = {|s2 ?𝑞 → 𝑞 }| 𝜎 ′ .   ′

           If s1 has never been false on 𝜎 ′ , we have {|s1 ?𝑝 → 𝑝 ′ }| 𝜎 ′ = {|𝑝 }| 𝜎 ′ according to the semantics
           of Figure 4. Moreover, from the induction hypothesis and the assumption 𝑆 ⊢ 𝑝 ⊏                                                  ′
                                                                                                                          ∼ s2 ?𝑞 → 𝑞 ,
                                            ′
                                                              ′ ′
                                                                                          ′
           we know that {|𝑝 }| 𝜎 ⊑ {|s2 ?𝑞 → 𝑞 }| 𝜎 . Hence {|s1 ?𝑝 → 𝑝 }| 𝜎 ⊑ {|s2 ?𝑞 → 𝑞 }| 𝜎 .
                                                                                                ′
                                                                                                                  ′  ′

       • (R-From Two) Symmetric to the case above.
       • (Bi-Both): By the assumption, we have s1 ⇔ s2 , ⊢ 𝑝 ⊏                                           ′     ′
                                                                                       ∼ 𝑞 and ⊢ 𝑝 ⊏         ∼𝑞.
           With s1 ⇐⇒ s2 , it is guaranteed that conditions s2 and s1 have the same value. If they both
           turn from true to false at index 𝑖 towards the end of 𝜎 ′ , we have {|s1 ?𝑝 ↔ 𝑝 ′ }| 𝜎 ′ = {|𝑝 ′ }| 𝜎 ′[𝑖+1:]

                              Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:4                                                                                         Jeffrey Ching and Danfeng Zhang


        and {|s2 ?𝑞 ↔ 𝑞 ′ }| 𝜎 ′ = {|𝑞 ′ }| 𝜎 ′[𝑖+1:] according to the semantics of Figure 4. Moreover, by the
        induction hypothesis and the assumption that ⊢ 𝑝 ′ ⊏                        ′                  ′                ′
                                                                                 ∼ 𝑞 , we have {|𝑝 }| 𝜎 ′[𝑖+1:] ⊑ {|𝑞 }| 𝜎 ′[𝑖+1:] .
                                   ′
        Hence, {|s1 ?𝑝 ↔ 𝑝 }| 𝜎 ′ ⊑ {|s2 ?𝑞 ↔ 𝑞 }| 𝜎 ′ .  ′

        If they both turn from false to true at index 𝑖 towards the end of 𝜎 ′ , we have {|s1 ?𝑝 ↔ 𝑝 ′ }| 𝜎 ′ =
        {|𝑝 }| 𝜎 ′[𝑖+1:] and {|s2 ?𝑞 ↔ 𝑞 ′ }| 𝜎 ′ = {|𝑞|}𝜎 ′[𝑖+1:] according to the semantics of Figure 4. Moreover,
        by the induction hypothesis and the assumption that ⊢ 𝑝 ⊏                   ∼ 𝑞, we have {|𝑝 }| 𝜎 ′[𝑖+1:] ⊑ {|𝑞|}𝜎 ′[𝑖+1:] .
        Hence, {|s1 ?𝑝 ↔ 𝑝 ′ }| 𝜎 ′ ⊑ {|s2 ?𝑞 ↔ 𝑞 ′ }| 𝜎 ′ .
      • (Bi-To) (𝑆 ⊢ 𝐿 ⊏                      ′                                                                  ′
                               ∼ s2 ?𝑞 ↔ 𝑞 ): By the assumption we have ⊢ 𝐿 ⊏             ∼ 𝑞 and ⊢ 𝐿 ⊏       ∼ 𝑞 . If s2 turns
        from true to false at index 𝑖 towards the end of 𝜎 , we have {|s2 ?𝑞 ↔ 𝑞 }| 𝜎 ′ = {|𝑞 ′ }| 𝜎 ′[𝑖+1:]
                                                                               ′                            ′

        according to the semantics of Figure 4. By the induction hypothesis and the assumption that
        ⊢𝐿⊏          ′                                ′                                                                ′
                ∼ 𝑞 , we have {|𝐿|}𝜎 ′[𝑖+1:] ⊑ {|𝑞 }| 𝜎 ′[𝑖+1:] . Hence, {|𝐿|}𝜎 ′ = 𝐿 = {|𝐿|}𝜎 ′[𝑖+1:] ⊑ {|s2 ?𝑞 ↔ 𝑞 }| 𝜎 ′ .
        If s2 turns from false to true at index 𝑖 towards the end of 𝜎 , we have {|s2 ?𝑞 ↔ 𝑞 ′ }| 𝜎 ′ =
                                                                                           ′

        {|𝑞|}𝜎 ′[𝑖+1:] according to the semantics of Figure 4. By the induction hypothesis and the assump-
        tion that ⊢ 𝐿 ⊏     ∼ 𝑞, we have {|𝐿|}𝜎 ′[𝑖+1:] ⊑ {|𝑞|}𝜎 ′[𝑖+1:] . Hence, {|𝐿|}𝜎 ′ = 𝐿 = {|𝐿|}𝜎 ′[𝑖+1:] ⊑ {|s2 ?𝑞 ↔
        𝑞 ′ }| 𝜎 ′ .
      • (Bi-From) Symmetric to the case above.
                                                                                                                                □
   Theorem (Soundness of Release-To Relation, Theorem 2). For all policies p, a trace 𝜎, a set
of security events 𝑆 = s0 . . . sk , if 𝑆 ⊢ 𝑝 <
                                              ∼ 𝐿 and 𝑆 holds on 𝜎, then {|𝑝 }| 𝜎 ⊑ 𝐿.
  Proof. The proof is by induction on the static inference rules. The only interesting case is
Rule (R-From-F); the rest are the same as their corresponding rules in Theorem 1.
   • (R-From-F) (𝑆 ⊢ s1 ?𝑝 →     − 𝑝′ <
                                      ∼ 𝐿): By the assumption, we have 𝑆 ⊢ 𝑝 <    ∼ 𝐿 and 𝑆 ⊨ ¬s
                                                                                              c1 . Since 𝑆
      holds on 𝜎 and 𝑆 ⊭ ¬s1 , according to the semantics of Figure 4, we know that {|𝑐?𝑝 → 𝑝 ′ }| 𝜎
      evaluates to {|𝑝 }| 𝜎 . From the induction hypothesis and the assumption that 𝑆 ⊢ 𝑝 <   ∼ 𝐿, we get
      {|𝑝 }| 𝜎 ⊑ 𝐿. Hence, {|cnd?𝑝 → 𝑝 ′ }| 𝜎 = {|𝑝 }| 𝜎 ⊑ 𝐿 which the relation stands.
                                                                                                         □

E     Soundness of Type System
The structure of the proof follows a previous small-step noninterference proof [33], formed with
supporting lemmas. In the rest of the proof, we introduce a distinguished dynamic label B to denote
the source label that is considered “sensitive” per security reasoning. In addition, we introduce a
distinguished level L to denote the output that can be viewed by an attacker at the security level L.
Since the proof below is applicable to any B and L, we show that dynamic release policy is enforced
by the proposed type system.

E.1     Typing Rules for Expressions
The typing rules for expressions (Figure 15) are straightforward. Rules (Var) and (Num) compute
the policy on a variable and a value, respectively. Rule (Op) ensures that the policy 𝑝 2 serves as an
upper-bound on the policies on subexpressions 𝑒 1 and 𝑒 2 . Since our type system supports dynamic
labels, we include a subtyping rule (SubType) to compute the upper bound of an expression and
enable comparisons among different labels.

E.2     Augmented Language
Following [33], we first introduce an augmented semantics that “protects” all sensitive values with
brackets. Hence, a memory is said to be “well-formed” if all sensitive values with brackets are only
stored in variables that are considered as sensitive at the end of 𝜎: B ⊑𝜎 Γ(𝑥).

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                                       360:5


                                                                                                   𝑐 1 ≈ 𝑐 1′           𝑐 2 ≈ 𝑐 2′
              𝑛 ≈𝑛           [𝑛 1 ] ≈ [𝑛 2 ]          [𝑐] ≈ [𝑐 ′ ]               skip ≈ skip             𝑐 1 ; 𝑐 2 ≈ 𝑐 1′ ; 𝑐 2′

                     𝑐 1 ≈ 𝑐 1′       𝑐 2 ≈ 𝑐 2′                                                𝑐 ≈ 𝑐′
     if (𝑒) then 𝑐 1 else 𝑐 2 ≈ if (𝑒) then 𝑐 1′ else 𝑐 2′                        while (𝑒) do 𝑐 ≈ while (𝑒) do 𝑐 ′

                                                   s0 . . . sk = s0′ . . . sk′
       𝑥 := relabel(𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ) ≈ 𝑥 := relabel(𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0′ . . . sk′ )

                             s = s′                                                    s = s′
                EventOn(s) ≈ EventOn(s′ )                               EventOff(s) ≈ EventOff(s′ )

            Fig. 16. Two commands are equivalent if they are equal modulo bracketed commands.


E.2.1 Augmented Syntax. We augment memories to allow mapping variables 𝑥 to a bracketed value.
Intuitively, a bracketed value is information to be protected: given any two executions on initial
memory states that agree on all labels except B, only bracketed values might differ throughout
program execution. In this sense, we augment the language syntax to include bracketed commands
and values.
                                                      𝑒 ::= · · · | [𝑛]
                                                      𝑐 ::= · · · | [𝑐]
E.2.2 Equivalence on Commands and Memories. Based on the intuition that bracketed values are
the “sensitive” data to be protected, we define an equivalence relation ≈ on values and commands in
Figure 16. Two values are indistinguishable if either (1) they both have the same value without brack-
ets, or (2) both have bracketed values. Accordingly, two memories 𝑚 1 and 𝑚 2 are indistinguishable
if for each variable 𝑥 that is considered as sensitive, 𝑚 1 (𝑥) and 𝑚 2 (𝑥) are indistinguishable:
                           𝑚 1 ≈𝜎 𝑚 2 ⇐⇒ ∀𝑥 . B ̸⊑𝜎 Γ(𝑥) ⇒ 𝑚 1 (𝑥) ≈ 𝑚 2 (𝑥)
  Bracketed commands represent the commands being executed under “high” 𝑝𝑐, in order to
rule out implicit flows. Hence, two equivalent commands are either structurally the same with
equivalent expressions, or both of them are bracketed commands.
E.2.3 Memory Well-Formedness. Intuitively, labels that are more restrictive than B under the
current event trace 𝜎 are considered to be sensitive. Hence, only those variables can hold bracketed
values. This property is formalized below as Memory Well-Formedness:
  Definition 11 (Memory Well-Formedness).
                                  𝜎 |= 𝑚 ≜ ∀𝑥 . (∃𝑛. 𝑚(𝑥) = [𝑛]) ⇒ B ⊑𝜎 Γ(𝑥)

E.2.4 Augmented operational semantics. The operational semantics is extended to model the
bracketed syntax, as shown in Figures 17 and 18. The rules here are extended for operational
semantics with brackets, nothing special on the computational perspective. The interesting part
only happens in assignment and relabel commands, where three cases are distinguished depending
on whether 𝑥 and 𝑒 has a bracket or not. For assignments, there are three rules. (OS-Assign-B1)
makes sure when a variable 𝑥 satisfies B ⊑𝜎 Γ(𝑥), it is assigned to a bracketed value. (OS-Assign-B2)

                        Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:6                                                                                Jeffrey Ching and Danfeng Zhang


                                               𝐵 ̸⊑𝜎 Γ(𝑥) ∨ 𝑚(𝑥) = [𝑛]               𝐵 ⊑𝜎 Γ(𝑥) ∧ 𝑚(𝑥) = 𝑛
                ⟨𝑚, [𝑛]⟩ ⇓𝜎 [𝑛]                      ⟨𝑚, 𝑥⟩ ⇓𝜎 𝑚(𝑥)                          ⟨𝑚, 𝑥⟩ ⇓𝜎 [𝑛]

                            ⟨𝑚, 𝑒 1 ⟩ ⇓𝜎 [𝑛 1 ]        ⟨𝑚, 𝑒 2 ⟩ ⇓𝜎 𝑛 2     𝑛 = 𝑛 1 op 𝑛 2
                                                  ⟨𝑚, 𝑒 1 𝑜𝑝 𝑒 2 ⟩ ⇓𝜎 [𝑛]

                            ⟨𝑚, 𝑒 1 ⟩ ⇓𝜎 𝑛 1         ⟨𝑚, 𝑒 2 ⟩ ⇓𝜎 [𝑛 2 ]    𝑛 = 𝑛 1 op 𝑛 2
                                                  ⟨𝑚, 𝑒 1 𝑜𝑝 𝑒 2 ⟩ ⇓𝜎 [𝑛]

                           ⟨𝑛, 𝑒 1 ⟩ ⇓𝜎 [𝑛 1 ]        ⟨𝑚, 𝑒 2 ⟩ ⇓𝜎 [𝑛 2 ]   𝑛 = 𝑛 1 op 𝑛 2
                                                  ⟨𝑚, 𝑒 1 𝑜𝑝 𝑒 2 ⟩ ⇓𝜎 [𝑛]

                           Fig. 17. Augmented operational semantics for expressions.


is trivial. (OS-Assign-B3) states that when 𝐵 ̸⊑𝜎 Γ(𝑥), the value 𝑛 is not bracketed. The augmented
rules for relabel commands are similar.
E.2.5 Extra typing rules. Since the static semantics are augmented, under the definition of memory
well-formedness, we also need to provide a type (i.e., label) for bracketed values and commands.
We define extra typing rules for (AugNum) and (AugComm) in Figure 19 for that purpose. These
rules ensure that the type system treats the label of bracketed expressions as sensitive (i.e., higher
than the distinguished B). Bracketed commands are treated as commands that can be type-checked
under a sensitive 𝑝𝑐 label.
E.2.6 Completeness. Completeness means that every step in the augmented semantics (with
brackets) can be performed in the non-augmented semantics. Therefore, any full evaluation of a
program in the original language can be simulated in the augmented language. With an augmented
program 𝑐 and memory 𝑚, ⌊𝑐⌋ denotes removing all the brackets from 𝑐 and ⌊𝑚⌋ as the converted
memory. Completeness can be expressed with the following lemma.
   Lemma 3. Completeness of the augmented language
  Γ, 𝑝𝑐 ⊢ 𝑐 ∧ ⟨⌊𝑐⌋, ⌊𝑚⌋, 𝜎⟩ →∗ ⟨skip, 𝑚 ′, 𝜎 ′ ⟩ → ∃𝑚 ′′ . ⟨𝑐, 𝑚, 𝜎⟩ →∗ ⟨skip, 𝑚 ′′, 𝜎⟩ ∧ 𝑚 ′ = ⌊𝑚 ′′ ⌋
   Proof. By induction on each evaluation step.                                                                   □

E.3     Useful Lemmas
We first show that for any well-formed memory, the label of any expression 𝑒 that evaluates to a
bracketed value [𝑛] must always be sensitive (i.e., B ⊑𝜎 𝑝 where 𝑝 is the label of 𝑒).
   Lemma 4. Expression evaluation
                      ∀𝑚, 𝜎, 𝑒, 𝑝, Γ. 𝜎 |= 𝑚 ∧ Γ ⊢ 𝑒 : 𝑝 ∧ ∃𝑛.⟨𝑚, 𝑒⟩ ⇓ [𝑛] ⇒ B ⊑𝜎 𝑝
   Proof. By structural induction on 𝑒:
      • case 𝑒 = 𝑛: vacuously true since 𝑛 evaluates to a value without brackets.
      • case 𝑒 = [𝑛]: by the typing rules (AugNum) and (SubType), we have ⊢ B ⊏ ∼ 𝑝. Hence, we have
        B ⊑𝜎 𝑝 by Theorem 1.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                   360:7


                                                                                − ⟨𝑚 ′, 𝑐 ′, 𝜎 ′ ⟩
                                                                      ⟨𝑚, 𝑐, 𝜎⟩ →
                ⟨𝑚, [skip], 𝜎⟩ → ⟨𝑚, skip, 𝜎⟩                                  − ⟨𝑚 ′, [𝑐 ′ ], 𝜎 ′ ⟩
                                                                   ⟨𝑚, [𝑐], 𝜎⟩ →

                                                ⟨𝑚, 𝑒⟩ ⇓ [true]
                              ⟨𝑚, if (𝑒) then 𝑐 1 else 𝑐 2, 𝜎⟩ → ⟨𝑚, [𝑐 1 ], 𝜎⟩

                                                            OS-Assign-b1
                       ⟨𝑚, 𝑒⟩ ⇓ [false]                              ⟨𝑚, 𝑒⟩ ⇓ 𝑛             B ⊑𝜎 Γ(𝑥)
       ⟨𝑚, if (𝑒) then 𝑐 1 else 𝑐 2, 𝜎⟩ → ⟨𝑚, [𝑐 2 ], 𝜎⟩ ⟨𝑚, 𝑥 := 𝑒, 𝜎⟩ → ⟨𝑚[𝑥 := [𝑛]], skip, 𝜎⟩

       OS-Assign-b2                                            OS-Assign-b3
                       ⟨𝑚, 𝑒⟩ ⇓ [𝑛]                                    ⟨𝑚, 𝑒⟩ ⇓ 𝑛            B ̸⊑𝜎 Γ(𝑥)
       ⟨𝑚, 𝑥 := 𝑒, 𝜎⟩ → ⟨𝑚[𝑥 := [𝑛]], skip, 𝜎⟩                 ⟨𝑚, 𝑥 := 𝑒, 𝜎⟩ → ⟨𝑚[𝑥 := 𝑛], skip, 𝜎⟩

             OS-Relabel-r1
                      ⟨𝑚, 𝑒⟩ ⇓ 𝑛       B ⊑𝜎 Γ(𝑥)         ∀𝑖 ∈ 0...𝑘. eval(si, 𝜎) = true
             ⟨𝑚, 𝑥 := relabel(𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ → ⟨𝑚[𝑥 := [𝑛]], skip, 𝜎⟩

             OS-Relabel-r2
                             ⟨𝑚, 𝑒⟩ ⇓ [𝑛]        ∀𝑖 ∈ 0...𝑘. eval(si, 𝜎) = true
             ⟨𝑚, 𝑥 := relabel(𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ → ⟨𝑚[𝑥 := [𝑛]], skip, 𝜎⟩

              OS-Relabel-r3
                      ⟨𝑚, 𝑒⟩ ⇓ 𝑛       B ̸⊑𝜎 Γ(𝑥)        ∀𝑖 ∈ 0...𝑘. eval(si, 𝜎) = true
              ⟨𝑚, 𝑥 := relabel(𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ → ⟨𝑚[𝑥 := 𝑛], skip, 𝜎⟩

               OS-Output                                       (
                              ∀𝑖 ∈ 0...𝑘.                       𝜎 · ox @L, 𝑒 is a variable 𝑥
                ⟨𝑚, 𝑒⟩ ⇓ 𝑣                       𝜎′ =
                              eval(si, 𝜎) = true                𝜎,         otherwise
                                                                   ⟨𝐿,𝑣,𝜎 ⟩
                       ⟨𝑚, output(𝐿, 𝑒, using s0 . . . sk ), 𝜎⟩ −−−−−→ ⟨𝑚, skip, 𝜎 ′ ⟩

                          Fig. 18. Augmented operational semantics for commands.


                                                                    AugComm
                                      AugNum                        𝑝𝑐, Γ ⊢ 𝑐         B, Γ ⊢ 𝑐
                                      Γ ⊢ [𝑛] : B
                                                                              𝑝𝑐, Γ ⊢ [𝑐]

                             Fig. 19. Augmented typing rules for bracketed syntax.


    • case 𝑒 = 𝑥: Due to the semantics, we have 𝑚(𝑥) = [𝑛]. Since 𝑚 is well-formed, we have
      B ⊑𝜎 Γ(𝑥). From Rules (Var), (SubType) and the assumption that Γ ⊢ 𝑥 : 𝑝, we have
      ⊢ Γ(𝑥) ⊏∼ 𝑝, which implies Γ(𝑥) ⊑𝜎 𝑝 by Theorem 1. Hence, 𝐵 ⊑𝜎 Γ(𝑥) ⊑𝜎 𝑝.
    • case 𝑒 = 𝑒 1 op 𝑒 2 : From the assumption of Rule (Op), we have ⊢ 𝑒 1 : 𝑝 1 , ⊢ 𝑒 2 : 𝑝 2 and ⊢ 𝑝 1 ⊏
                                                                                                          ∼ 𝑝2.
      By evaluation rules, at least one of 𝑒 1 and 𝑒 2 is evaluated to some [𝑚]. By the induction

                        Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:8                                                                                 Jeffrey Ching and Danfeng Zhang


        hypothesis, at least one of B ⊑𝜎 𝑝 1 and B ⊑𝜎 𝑝 2 is correct. The harder case is when B ⊑𝜎 𝑝 1 .
        Since ⊢ 𝑝 1 ⊏
                    ∼ 𝑝 2 , we have 𝑝 1 ⊑𝜎 𝑝 2 by Theorem 1. Hence, B ⊑𝜎 𝑝 2
                                                                                                                     □
  We next show that if a program is well-typed under a program counter label 𝑝𝑐, then it is also
well-typed under any 𝑝𝑐 ′ such that ⊢ 𝑝𝑐 ′ ⊏
                                           ∼ 𝑝𝑐.
   Lemma 5. PC subsumption
                              ∀𝑝𝑐, 𝑝𝑐 ′, Γ, 𝑐. 𝑝𝑐, Γ ⊢ 𝑐∧ ⊢ 𝑝𝑐 ′ ⊏
                                                                 ∼ 𝑝𝑐 ⇒ 𝑝𝑐 , Γ ⊢ 𝑐
                                                                          ′


   Proof. By induction on the typing derivation 𝑝𝑐, Γ ⊢ 𝑐:
    • case 𝑝𝑐, Γ ⊢ skip: Trivial.
    • case 𝑝𝑐, Γ ⊢ 𝑥 := 𝑒: From the typing rule (Assign), we have ⊢ 𝑝𝑐 ⊏                      ∼ Γ(𝑥) and Γ ⊢ 𝑒 : Γ(𝑥).
      Since ⊢ 𝑝𝑐 ′ ⊏                           ∼ Γ(𝑥) by transitivity. So 𝑝𝑐 , Γ ⊢ 𝑥 := 𝑒.
                                             ′                                       ′
                     ∼ 𝑝𝑐, we have ⊢ 𝑝𝑐 ⊏
    • case 𝑝𝑐, Γ ⊢ 𝑐 1 ; 𝑐 2 : From typing rules, 𝑝𝑐, Γ ⊢ 𝑐 1 and 𝑝𝑐, Γ ⊢ 𝑐 2 . With the induction hypothesis,
      we have 𝑝𝑐 ′, Γ ⊢ 𝑐 1 and 𝑝𝑐 ′, Γ ⊢ 𝑐 2 . Hence, 𝑝𝑐 ′, Γ ⊢ 𝑐 1 ; 𝑐 2 .
    • case 𝑝𝑐, Γ ⊢ if (𝑒) then 𝑐 1 else 𝑐 2 : From typing rules, we have Γ ⊢ 𝑒 : 𝑝𝑐 1 , 𝑝𝑐 1, Γ ⊢ 𝑐 1 ,
      𝑝𝑐 1, Γ ⊢ 𝑐 2 , and ⊢ 𝑝𝑐 ⊏     ∼ 𝑝𝑐 1 for some 𝑝𝑐 1 . With the relation ⊢ 𝑝𝑐 ⊏
                                                                                               ′
                                                                                                 ∼ 𝑝𝑐, we know that
      ⊢ 𝑝𝑐 ′ ⊏   𝑝𝑐   still holds   due  to transitivity. Therefore,       𝑝𝑐 ′ , Γ ⊢ if (𝑒) then 𝑐 else 𝑐 stands
               ∼ 1                                                                                    1           2
      under the same 𝑝𝑐 1 .
    • case 𝑝𝑐, Γ ⊢ while (𝑒) do 𝑐: From typing rules, we have Γ ⊢ 𝑒 : 𝑝𝑐 1 , 𝑝𝑐 1, Γ ⊢ 𝑐 and ⊢ 𝑝𝑐 ⊏                 ∼ 𝑝𝑐 1
      for some 𝑝𝑐 1 . With the relation ⊢ 𝑝𝑐 ′ ⊏       ∼  𝑝𝑐, the   condition         ⊢  𝑝𝑐 ′ ⊏ 𝑝𝑐 still holds due to
                                                                                              ∼    1
      transitivity. Therefore, 𝑝𝑐 ′, Γ ⊢ while (𝑒) do 𝑐 stands under 𝑝𝑐 1 .
    • case 𝑝𝑐, Γ ⊢ 𝑥 := relabel (𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ): From the typing rule (Relabel) and
      the assumption, we have ⊢ 𝑝𝑐 ⊏        ∼ Γ(𝑥), Γ ⊢ 𝑒 : 𝑝 𝑓 , s0 . . . sk ⊢ 𝐿𝑡 ⊏   ∼ Γ(𝑥), and s0 . . . sk ⊢ 𝑝 𝑓 ⊏
                                                                                                                     ∼ 𝐿𝑡 .
      Moreover, by ⊢ 𝑝𝑐 ′ ⊏        𝑝𝑐, we  have  ⊢ 𝑝𝑐 ′ ⊏ Γ(𝑥). The other conditions do not change under
                                 ∼                      ∼
      𝑝𝑐 ′ . Therefore, 𝑝𝑐 ′, Γ ⊢ 𝑥 := relabel (𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ).
    • case 𝑝𝑐, Γ ⊢ output(𝐿, 𝑒, using s0 . . . sk ): From typing rules, we have Γ ⊢ 𝑒 : 𝑝, s0 . . . sk ⊢ 𝑝 <            ∼
                                                            ∼ 𝐿. Therefore, 𝑝𝑐 , Γ ⊢ output(𝐿, 𝑒, using s0 . . . sk )
      𝐿 and ⊢ 𝑝𝑐 ⊏                  ′                     ′                            ′
                    ∼ 𝐿. By ⊢ 𝑝𝑐 ⊏    ∼ 𝑝𝑐, we have ⊢ 𝑝𝑐 ⊏
      stands.
    • case 𝑝𝑐, Γ ⊢ output(𝐿, 𝑥, using o𝑥 , s1 . . . sk ): same as the case above.
    • case 𝑝𝑐, Γ ⊢ eventon(s): From the typing rules, we have ⊢ 𝑝𝑐 ⊏                                  ′
                                                                                         ∼ ⊥. By ⊢ 𝑝𝑐 ⊏ ∼ 𝑝𝑐, we have
      ⊢ 𝑝𝑐 ⊏ ′   ⊥. Therefore,     the rule  stands.
               ∼
    • case 𝑝𝑐, Γ ⊢ eventoff(s): Same as the case above.
    • case 𝑝𝑐, Γ ⊢ [𝑐]: From the typing rule, we have 𝑝𝑐, Γ ⊢ 𝑐 and B, Γ ⊢ 𝑐. By the induction
      hypothesis and the assumption that ⊢ 𝑝𝑐 ′ ⊏           ∼ 𝑝𝑐, we have 𝑝𝑐 , Γ ⊢ 𝑐. Therefore, 𝑝𝑐 , Γ ⊢ [𝑐]
                                                                                      ′                         ′

      stands.
                                                                                                                        □
   Next, we show that for any expression that evaluates to a value under some memory 𝑚 1 , it
must evaluate to an equivalent value under any 𝑚 2 that is equivalent to 𝑚 1 , under the equivalence
relation in Figure 16.
   Lemma 6. Expression preserves equivalence
               ∀𝑚 1, 𝑚 2, 𝜎, 𝑒, 𝑣 1, 𝑣 2 . 𝑚 1 ≈𝜎 𝑚 2 ∧ ⟨𝑚 1, 𝑒⟩ ⇓ 𝑣 1 ⇒ ∃𝑣 2 .⟨𝑚 2, 𝑒⟩ ⇓ 𝑣 2 ∧ 𝑣 1 ≈ 𝑣 2
   Proof. By induction on the structure of expression 𝑒.
    • case 𝑒 = 𝑛. We have ⟨𝑚, 𝑒⟩ ⇓ 𝑛 for both 𝑚 1 and 𝑚 2 . So 𝑣 1 = 𝑣 2 = 𝑛.
    • case 𝑒 = [𝑛]. Since we have ⟨𝑚, 𝑒⟩ ⇓ [𝑛] for both 𝑚 1 and 𝑚 2 , so 𝑣 1 = 𝑣 2 = [𝑛].

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                                 360:9


      • case 𝑒 = 𝑥. When B ̸⊑𝜎 Γ(𝑥), we have 𝑣 1 = 𝑚 1 (𝑥) ≈ 𝑚 2 (𝑥) = 𝑣 2 from the assumption that
        𝑚 1 ≈𝜎 𝑚 2 . Otherwise, we have 𝑣 1 = [𝑛 1 ] ≈ [𝑛 2 ] = 𝑣 2 for some 𝑛 1 and 𝑛 2 from the semantics.
      • case 𝑒 = 𝑒 1 op 𝑒 2 . By the semantics, ⟨𝑚 1, 𝑒 1 ⟩ ⇓ 𝑣 3 , ⟨𝑚 2, 𝑒 1 ⟩ ⇓ 𝑣 3′ , ⟨𝑚 1, 𝑒 2 ⟩ ⇓ 𝑣 4 , ⟨𝑚 2, 𝑒 2 ⟩ ⇓ 𝑣 4′ .
        – If 𝑣 3 , 𝑣 4 have no brackets, 𝑣 3 = 𝑣 3′ and 𝑣 4 = 𝑣 4′ by the induction hypothesis. Further, 𝑣 1 = 𝑣 2 .
        – When one of 𝑣 3 or 𝑣 4 is a bracketed value, 𝑣 3′ or 𝑣 4′ are bracketed value by the induction
          hypothesis. From the semantics, we know 𝑒 has to be evaluated to bracketed values under
          both memories 𝑚 1 and 𝑚 2 . So 𝑣 1 ≈ 𝑣 2 .
                                                                                                                                  □

   Next, we show that the partial ordering on dynamic release labels is preserved over any extension
of the current event. Intuitively, this property is important to show that after any changes to the
event trace, with eventon and eventoff commands, the “protected” values with brackets are still
stored in “protected” memory locations (Lemma 7, Preservation).
  Lemma. Trace Preservation, Lemma 1
                                  ∀𝑝, 𝑝 ′, 𝜎. 𝑝 ⊑𝜎 𝑝 ′ ⇒ (∀𝜎 ′ . 𝜎 ⪯ 𝜎 ′ ⇒ 𝑝 ⊑𝜎 ′ 𝑝 ′ )
    Proof. Consider any extension of 𝜎, denoted as 𝜎 ′ . By Definition 1, it is sufficient to show
that ∀𝜎 ′′ . 𝜎 ′ ⪯ 𝜎 ′′ ⇒ {|𝑝 }| 𝜎 ′′ ⊑ {|𝑝 ′ }| 𝜎 ′′ . Note that any such 𝜎 ′′ is also an extension of 𝜎. Hence,
{|𝑝 }| 𝜎 ′′ ⊑ {|𝑝 ′ }| 𝜎 ′′ by the definition of 𝑝 ⊑𝜎 𝑝 ′ .
                                                                                                               □

E.4     Preservation
We prove that program evaluation under the augmented semantics preserves typing and well-
formedness during evaluation.
  Lemma 7. Preservation
      ∀𝑐, 𝑐 ′, 𝜎, 𝜎 ′, 𝑚, 𝑚 ′, 𝑝𝑐, Γ. 𝜎 |= 𝑚 ∧ 𝑝𝑐, Γ ⊢ 𝑐 ∧ ⟨𝑚, 𝑐, 𝜎⟩ → ⟨𝑚 ′, 𝑐 ′, 𝜎 ′ ⟩ ⇒ 𝜎 ′ |= 𝑚 ′ ∧ 𝑝𝑐, Γ ⊢ 𝑐 ′


  Proof. By induction on evaluation rules of ⟨𝑚, 𝑐, 𝜎⟩ → ⟨𝑚 ′, 𝑐 ′, 𝜎 ′ ⟩.
   • case ⟨𝑚, [skip], 𝜎⟩ → ⟨𝑚, skip, 𝜎⟩: Trivial, since 𝑚 ′ and 𝜎 ′ remain the same and skip type
     checks under any Γ, 𝑝𝑐.
   • case ⟨𝑚, [𝑐], 𝜎⟩ → ⟨𝑚 ′, [𝑐 ′ ], 𝜎 ′ ⟩: From the evaluation rule, we have ⟨𝑚, 𝑐, 𝜎⟩ → ⟨𝑚 ′, 𝑐 ′, 𝜎 ′ ⟩.
     From the typing rule (AugComm), we know 𝑝𝑐 ′, Γ ⊢ 𝑐 and B, Γ ⊢ 𝑐. By 𝑝𝑐 ′, Γ ⊢ 𝑐 and the
     assumption that 𝜎 |= 𝑚, we have 𝑝𝑐 ′, Γ ⊢ 𝑐 ′ and 𝜎 ′ |= 𝑚 ′ by the induction hypothesis.
     Similarly, from B, Γ ⊢ 𝑐, we also have B, Γ ⊢ 𝑐 ′ . Hence, we can derive 𝑝𝑐, Γ ⊢ [𝑐 ′ ].
   • case ⟨𝑚, 𝑥 := 𝑒, 𝜎⟩ → ⟨𝑚[𝑥 := 𝑛], skip, 𝜎⟩: We have 𝑝𝑐, Γ ⊢ skip by typing rule (skip). From
     the evaluation rule of ⟨𝑚, 𝑥 := 𝑒, 𝜎⟩ → ⟨𝑚[𝑥 := 𝑛], skip, 𝜎⟩, we know that B ̸⊑𝜎 Γ(𝑥), and
     ⟨𝑚, 𝑒⟩ ⇓ 𝑛. With 𝜎 |= 𝑚, we know 𝑚 ′ is still well-formed as the command sets 𝑥 to 𝑛 without
     brackets.
   • case ⟨𝑚, 𝑥 := 𝑒, 𝜎⟩ → ⟨𝑚[𝑥 := [𝑛]], skip, 𝜎⟩: We have 𝑝𝑐, Γ ⊢ skip by typing rule (Skip). Next,
     we show that 𝑚[𝑥 := [𝑛]] is well-formed. From typing rule (Assign), we have Γ ⊢ 𝑒 : Γ(𝑥).
     From the evaluation rules with ⟨𝑚, 𝑥 := 𝑒, 𝜎⟩ → ⟨𝑚[𝑥 := [𝑛]], skip, 𝜎⟩, there are two
     possibilities:
     – Rule (OS-Assign-b1): 𝑚[𝑥 := [𝑛]] is still well-formed under trace 𝜎 since we have B ⊑𝜎
       Γ(𝑥) in the rule assumption. Hence, 𝑥 can hold bracketed values. For other variables, we
       still have 𝜎 |= 𝑚 ′ as the assignment does not change any values other than 𝑥’s.

                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:10                                                                                 Jeffrey Ching and Danfeng Zhang


      – Rule (OS-Assign-b2): by rule assumption, ⟨𝑚, 𝑒⟩ ⇓ [𝑛] for some 𝑛. From the typing rule,
        we have Γ ⊢ 𝑒 : Γ(𝑥). So by Lemma 4, we have B ⊑𝜎 Γ(𝑥). Hence, 𝑥 can hold bracketed
        values. For other variables, we still have 𝜎 |= 𝑚 ′ as the assignment does not change any
        values other than 𝑥’s.
    • case ⟨𝑚, 𝑐 1 ; 𝑐 2, 𝜎⟩ → ⟨𝑚 ′, 𝑐 1′ ; 𝑐 2, 𝜎 ′ ⟩: From the evaluation rule we have ⟨𝑚, 𝑐 1, 𝜎⟩ → ⟨𝑚 ′, 𝑐 1′ , 𝜎 ′ ⟩.
      From the typing rule (Seq), we have 𝑝𝑐, Γ ⊢ 𝑐 1 and 𝑝𝑐, Γ ⊢ 𝑐 2 . By the induction hypothesis,
      we get 𝑚 ′ |= 𝜎 ′ and 𝑝𝑐, Γ ⊢ 𝑐 1′ . Therefore we can derive 𝑝𝑐, Γ ⊢ 𝑐 1′ ; 𝑐 2 .
    • case ⟨𝑚, skip; 𝑐, 𝜎⟩ → ⟨𝑚, 𝑐, 𝜎⟩: From typing rule (Seq), we have 𝑝𝑐, Γ ⊢ 𝑐. We can also derive
      that 𝑚 |= 𝜎 as both 𝑚 and 𝜎 do not change.
    • case ⟨𝑚, if (𝑒) then 𝑐 1 else 𝑐 2, 𝜎⟩ → ⟨𝑚, 𝑐 1, 𝜎⟩: From the evaluation rule, we know that
      ⟨𝑚, 𝑒⟩ ⇓ true. From the typing rule (If), we have Γ ⊢ 𝑒 : 𝑝𝑒 , 𝑝𝑒 , Γ ⊢ 𝑐 1 , and ⊢ 𝑝𝑐 ⊏          ∼ 𝑝𝑒 for some
      𝑝𝑒 . With 𝑝𝑐 ⊏   ∼  𝑝 𝑒 , 𝑝 𝑒 , Γ ⊢ 𝑐 1 and Lemma     5, we have  𝑝𝑐,  Γ ⊢ 𝑐 1 . Therefore, the type of the true
      branch is preserved. Moreover, 𝑚 is still well-formed as both 𝑚 and 𝜎 do not change.
    • case ⟨𝑚, if (𝑒) then 𝑐 1 else 𝑐 2, 𝜎⟩ → ⟨𝑚, 𝑐 2, 𝜎⟩: similar to the case above.
    • case ⟨𝑚, if (𝑒) then 𝑐 1 else 𝑐 2, 𝜎⟩ → ⟨𝑚, [𝑐 1 ], 𝜎⟩: From the evaluation rule, we know that
      ⟨𝑚, 𝑒⟩ ⇓ [true]. From the typing rule (If), we have Γ ⊢ 𝑒 : 𝑝𝑒 , 𝑝𝑒 , Γ ⊢ 𝑐 1 , and ⊢ 𝑝𝑐 ⊏              ∼ 𝑝𝑒 for
      some 𝑝𝑒 .
      Since 𝑒 evaluates to a value with brackets, we have ⊢ B ⊏                   ∼ 𝑝𝑒 according to Lemma 4. By
      Lemma 5, we have 𝑝𝑐, Γ ⊢ 𝑐 1 and B, Γ ⊢ 𝑐 1 . Hence, we can type check [𝑐 1 ] under 𝑝𝑐 and Γ as
      follows:
                                                  𝑝𝑐, Γ ⊢ 𝑐 1     B, Γ ⊢ 𝑐 1
                                                     𝑝𝑐, Γ ⊢ [𝑐 1 ]
      𝑚 is still well-formed as both 𝑚 and 𝜎 do not change.
    • case ⟨𝑚, if (𝑒) then 𝑐 1 else 𝑐 2, 𝜎⟩ → ⟨𝑚, [𝑐 2 ], 𝜎⟩: similar to the case above.
    • case ⟨𝑚, while (𝑒) do 𝑐, 𝜎⟩ → ⟨𝑚, if (𝑒) then 𝑐; (while (𝑒) do 𝑐) else skip, 𝜎⟩:
      From the typing rule (While), we have three assumptions, 𝐴 = Γ ⊢ 𝑒 : 𝑝𝑒 , 𝐵 = 𝑝𝑐 ⊏ ∼ 𝑝𝑒 and
      𝐶 = 𝑝𝑒 , Γ ⊢ 𝑐 for some 𝑝𝑒 . Therefore, the program after evaluation on the right hand side
      must look like this:
                                                𝐴                     𝐵
                                            Γ ⊢ 𝑒 : 𝑝𝑒          ⊢ 𝑝𝑐 ⊏
                                                                     ∼ 𝑝𝑒
                                    𝐴                    𝐵               𝐶
                 𝐶             Γ ⊢ 𝑒 : 𝑝𝑒           ⊢ 𝑝𝑐 ⊏
                                                         ∼ 𝑝𝑒             𝑝𝑒 , Γ ⊢ 𝑐
             𝑝𝑒 , Γ ⊢ 𝑐                     𝑝𝑒 , Γ ⊢ while (𝑒) do 𝑐
                                 𝑝𝑒 , Γ ⊢ 𝑐; while (𝑒) do 𝑐                               𝑝𝑒 , Γ ⊢ skip
                            𝑝𝑐, Γ ⊢ if (𝑒) then 𝑐; (while (𝑒) do 𝑐) else skip
      𝑚 is still well-formed as both 𝑚 and 𝜎 do not change.
    • case: ⟨𝑚, eventon(s), 𝜎⟩ → ⟨𝑚, skip, 𝜎 · s⟩: We have 𝑝𝑐, Γ ⊢ skip by typing rule (skip).
      For each variable 𝑥, we have 𝑚 ′ (𝑥) = 𝑚(𝑥) as the command only changes security event
      status. Hence,
      – If ∃ 𝑛. 𝑚 ′ (𝑥) = [𝑛], we know that 𝑚(𝑥) = [𝑛] as well. Since 𝜎 |= 𝑚, we know that
        B ⊑𝜎 Γ(𝑥). By Lemma 1 (Trace Preservation), we have B ⊑𝜎 ·s Γ(𝑥). Hence, 𝜎 · s |= 𝑚 ′ .
      – If ∃ 𝑛. 𝑚 ′ (𝑥) = 𝑛, we know that it can be hold in any variable according to Definition 11 .
    • case ⟨𝑚, eventoff(s), 𝜎⟩ → ⟨𝑚, skip, 𝜎 · ¬s⟩: Same as the eventon case.
    • case ⟨𝑚, 𝑥 := relabel (𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ → ⟨𝑚[𝑥 := 𝑛], skip, 𝜎⟩: We have
      𝑝𝑐, Γ ⊢ skip by typing rule (skip). Since 𝜎 does not change and only the value of 𝑥 changes

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                   360:11


        in 𝑚, 𝑚 is still well-formed under 𝜎 for variables other than 𝑥. For 𝑥, we know that 𝑛 can be
        hold in any variable according to Definition 11 .
      • case ⟨𝑚, 𝑥 := relabel (𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ → ⟨𝑚[𝑥 := [𝑛]], skip, 𝜎⟩: We have
        𝑝𝑐, Γ ⊢ skip by typing rule (skip). Next, we show that 𝜎 |= 𝑚[𝑥 := [𝑛]].
        – Rule (OS-Relabel-r1): From the evaluation rule, we have that B ⊑𝜎 Γ(𝑥). Hence, the
          variable 𝑥 can hold a bracketed value: 𝑚[𝑥 := [𝑛]] is still well-formed.
        – Rule (OS-Relabel-r2): From the evaluation rule, we have that ⟨𝑚, 𝑒⟩ ⇓ [𝑛] and s0 . . . sk
          holds on 𝜎. From Lemma 4, we have ⊢ B ⊏   ∼ 𝑝 𝑓 , where Γ ⊢ 𝑒 : 𝑝 𝑓 , which implies B ⊑𝜎 𝑝 𝑓 by
          Theorem 1. From the typing rule, we know that s0 . . . sk ⊢ 𝐿𝑡 ⊏∼ Γ(𝑥) and s0 . . . sk ⊢ 𝑝 𝑓 ⊏
                                                                                                       ∼ 𝐿𝑡 .
          By Theorem 1, we have 𝐿𝑡 ⊑𝜎 Γ(𝑥) and 𝑝 𝑓 ⊑𝜎 𝐿𝑡 . Hence, we have B ⊑𝜎 𝑝 𝑓 ⊑𝜎 𝐿𝑡 ⊑𝜎 Γ(𝑥)
          due to transitivity. So memory 𝑚 ′ stays well-formed after setting 𝑥, whose label is at least
          as restrictive as B, to [𝑛].
      • case ⟨𝑚, 𝑥 := relabel (𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ → ⟨𝑚, skip, 𝜎⟩: This is a trivial case
        as 𝑚 and 𝜎 remain the same and skip can be type-checked under any environment.
                                                         ⟨𝐿 ′ ,𝑣1 ,𝜎 ⟩
      • case ⟨𝑚, output(𝐿 ′, 𝑒, using s0 . . . sk ), 𝜎⟩ −−−−−−→ ⟨𝑚, skip, 𝜎 ′ ⟩: same to the case above when
        𝑒 is not a variable 𝑥. Otherwise, we have 𝜎 ′ = 𝜎 · ox @L. By Lemma 1 (Trace Preservation),
        we know for any 𝑥 such that B ⊑𝜎 Γ(𝑥), it must be true that B ⊑𝜎 ·ox @L Γ(𝑥). Hence, they can
        still hold bracketed values. For other variables, they previously hold non-bracketed values
        due to the well-formed-memory assumption. Those values can be stored in any memory
        location. Therefore, 𝜎 · s |= 𝑚 ′ .
      • case ⟨𝑚, output(𝐿 ′, 𝑒, using s0 . . . sk ), 𝜎⟩ →
                                                        − ⟨𝑚, skip, 𝜎⟩: same to the case above.
                                                                                                           □

E.5     High Step
Next, we show that whenever the sources is considered as secret ({|B|}𝜎 ̸⊑ L), a step of well-typed
bracketed command (1) cannot leak any sensitive information to the output channel with attacker’s
level L, and (2) cannot emit new security events.
  Lemma 8 (High Step).
                                                                  𝜏
  ∀𝑚, 𝑐, 𝑥, 𝑝𝑐, 𝜎, Γ. 𝑝𝑐, Γ ⊢ [𝑐]∧{|B|}𝜎 ̸⊑ L∧⟨𝑚, [𝑐], 𝜎⟩ →
                                                          − ⟨𝑚 ′, 𝑐 ′, 𝜎 ′ ⟩ ⇒ 𝑚 ≈𝜎 ′ 𝑚 ′ ∧| ⌊𝜏⌋ L | = 0∧𝜎 = 𝜎 ′
   Proof. From the typing rule (AugComm), we have B, Γ ⊢ 𝑐. We proceed by induction on the
structure of 𝑐.
    • cases where 𝑐 is (skip), (if (𝑒) then 𝑐 1 else 𝑐 2 ), (while (𝑒) do 𝑐), (Output-Fail) and (Relabel-
      Fail) are trivial since those commands do no modify memory and execution trace.
    • case where 𝑐 is 𝑥 := 𝑒: by augmented bracket semantics for commands, we have that ⟨𝑚, 𝑥 :=
               ∅
              − ⟨𝑚 ′, skip, 𝜎⟩. Hence, it is easy to check that | ⌊𝜏⌋ L | = 0 ∧ 𝜎 = 𝜎 ′ .
        𝑒, 𝜎⟩ →
        By the typing rule, we have that B, Γ ⊢ 𝑥 := 𝑒. Via typing rule (Assign), we have B ⊏              ∼ Γ(𝑥).
        There are two cases for 𝑚 ′ :
        – 𝑚[𝑥 := [𝑛]] via the evaluation rule (OS-Assign-B1) and (OS-Assign-B2). Since B ⊏                 ∼ Γ(𝑥),
           we clearly have 𝑚 ≈𝜎 𝑚[𝑥 := [𝑛]] by definition.
        – 𝑚[𝑥 := 𝑛] via the evaluation rule (OS-Assign-b3). By that fact that B ⊏    ∼ Γ(𝑥) and Theorem 1,
           we can derive that B ⊑𝜎 Γ(𝑥) which contradicts the assumption B ̸⊑𝜎 Γ(𝑥) in Rule (OS-
           Assign-b3). Hence, this case is not applicable.
                                                                              𝜏
                                                                              − ⟨𝑚 ′, 𝑐 1′ , 𝜎 ′ ⟩. By typing rule,
      • case where 𝑐 is 𝑐 1 ; 𝑐 2 : from evaluation rule, we have ⟨𝑚, 𝑐 1, 𝜎⟩ →
        we have that B, Γ ⊢ 𝑐 1 and B, Γ ⊢ 𝑐 2 . So by typing rule (AugComm), we have 𝑝𝑐, Γ ⊢ [𝑐 1 ] and
        𝑝𝑐, Γ ⊢ [𝑐 2 ]. Hence, the conclusion is correct by the induction hypothesis.

                          Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:12                                                                                          Jeffrey Ching and Danfeng Zhang


      • case where 𝑐 is output(𝐿 ′, 𝑒, using s0 . . . sk ): there are two possible rules to type-check
        an output command: rule (Output) and rule (Output-Per). In either case, we know that
        ⊢B⊏      ′                                     ′                            ′
              ∼ 𝐿 . By Theorem 1, we have B ⊑𝜎 𝐿 which implies {|B|}𝜎 ⊑ 𝐿 by definition.
            ′
        If 𝐿 ⊑ L, where L is the fixed attacker’s level, we can derive {|B|}𝜎 ⊑ L, which contradicts the
        assumption that {|B|}𝜎 ̸⊑ L.
        Otherwise, | ⌊𝜏⌋ L | = 0 as the output is not visible to level L (Definition 3). The other conclusions
        are trivial as the output command does not modify memory and execution trace.
      • case where 𝑐 is 𝑥 := relabel (𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ): By typing rule (Relabel), we
        know that B ⊏  ∼ Γ(𝑥).
        There are two cases for 𝑚 ′ :
        – 𝑚[𝑥 := [𝑛]] from evaluation rules (OS-Relabel-R1) and (OS-Relabel-R2). Since B ⊏             ∼ Γ(𝑥),
           we clearly have 𝑚 ≈𝜎 𝑚[𝑥 := [𝑛]] by definition. Moreover, we know that 𝜏 is empty since
           the command does not change outputs and security events.
        – 𝑚[𝑥 := 𝑛] from evaluation rule (OS-Relabel-R3). By the fact that B ⊏         ∼ Γ(𝑥) and Theorem 1,
           we have B ⊑𝜎 Γ(𝑥) which contradicts the assumption B ̸⊑𝜎 Γ(𝑥) in Rule (OS-Relabel-R3).
           Hence, this case is not applicable.
      • case where 𝑐 is eventon(s): by typing rule, we have B, Γ ⊢ eventon(s) and therefore, B ⊏          ∼ ⊥.
        By Theorem 1, we can derive that B ⊑𝜎 ⊥, which implies {|B|}𝜎 ⊑ ⊥ ⊑ L by definition. This
        contradicts the assumption that {|B|}𝜎 ̸⊑ L. Hence, this rule is not applicable.
      • case where 𝑐 is eventoff(s): Similar as the case above.
                                                                                                                               □

E.6      Unwinding
Finally, we need a lemma to show that equivalence and well-formedness is preserved in each step.
That is, for each step taken by one of the two equivalent programs, either the other program takes a
number of steps to reach the same program state, or the program diverges inside a bracket. Besides
equivalence and well-formedness the trace of output channels and security events generated by
the two memories is the same.

   Lemma. Unwinding, Lemma 2

   ∀𝑚 1, 𝑚 2, 𝑐 1, 𝑐 2, 𝜏1, 𝜏2, 𝜎, 𝑥, 𝑝𝑐, Γ. 𝜎 |= 𝑚 1 ∧ 𝜎 |= 𝑚 2 ∧ 𝑚 1 ≈𝜎 𝑚 2 ∧
                                                                                                         𝜏1
   (𝑐 1 ≠ output(𝐿 ′, 𝑥, using o𝑥 , s0 . . . sk )) ∧ {|B|}𝜎 ̸⊑ L ∧ 𝑐 1 ≈ 𝑐 2 ∧ ⟨𝑚 1, 𝑐 1, 𝜎⟩ −→ ⟨𝑚 1′ , 𝑐 1′ , 𝜎 ′ ⟩ ⇒
                              𝜏2 ∗
(∃𝑚 2′ , 𝑐 2′ , 𝜏2 .⟨𝑚 2, 𝑐 2, 𝜎⟩ −→ ⟨𝑚 2′ , 𝑐 2′ , 𝜎 ′ ⟩∧𝑚 1′ ≈𝜎 ′ 𝑚 2′ ∧𝑐 1′ ≈ 𝑐 2′ ∧⌊𝜏1 ⌋ L = ⌊𝜏2 ⌋ L )∨(∃𝑐. 𝑐 2 = [𝑐] and 𝑐 diverges )
                                                                      𝜏1
   Proof. By rule induction on the step ⟨𝑚 1, 𝑐 1, 𝜎⟩ −→ ⟨𝑚 1′ , 𝑐 1′ , 𝜎 ′ ⟩.
                               𝜏1
      • case ⟨𝑚 1, [𝑐 3 ], 𝜎⟩ −→ ⟨𝑚 1′ , [𝑐 3′ ], 𝜎 ′ ⟩:
        From 𝑐 1 ≈ 𝑐 2 , we know that 𝑐 2 = [𝑐 4 ] for some command 𝑐 4 . By Lemma 8 (High Step), we
        have that 𝑚 1′ ≈𝜎 𝑚 1 ≈𝜎 𝑚 2 , | ⌊𝜏1 ⌋ L | = 0 and 𝜎 ′ = 𝜎. Hence, we select 𝑐 2′ to be the same as 𝑐 2
        and make 0 steps on it. It is easy to check that all desired conditions hold.
      • case ⟨𝑚 1, [skip], 𝜎⟩ → ⟨𝑚 1, skip, 𝜎 ′ ⟩:
        From 𝑐 1 ≈ 𝑐 2 , we know that 𝑐 2 = [𝑐 4 ] for some command 𝑐 4 . If 𝑐 4 diverges under 𝑚 2 , then let
        𝑐 = 𝑐 4 , we have (∃𝑐. 𝑐 2 = [𝑐] and 𝑐 diverges).
        If 𝑐 4 terminates, we know that there must be an execution trace like
                                                 𝜏2
                               ⟨𝑚 2, [𝑐 4 ], 𝜎⟩ −→ ⟨𝑚 2′ , [𝑐 4′ ], 𝜎2′ ⟩ →
                                                                          − · · · ⟨𝑚 2′′, skip, 𝜎2′′ ⟩

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                     360:13


      By Lemma 8 (High Step), we have that 𝑚 2′ ≈ 𝑚 2 ≈ 𝑚 1 , | ⌊𝜏2 ⌋ L | = 0 and 𝜎2′ = 𝜎. We can repeat
      the same on the rest of the execution trace and derive that 𝜎2′′ = 𝜎 ∧ 𝑚 2′′ ≈𝜎2′′ 𝑚 2 ≈𝜎2′′ 𝑚 1 and
      the whole trace produces no output events on the projection of L. So the first condition in
      the conclusion holds.
                            ∅
    • case ⟨𝑚 1, 𝑥 := 𝑒, 𝜎⟩ →
                            − ⟨𝑚 1 [𝑥 := 𝑛], skip, 𝜎⟩:
      From 𝑐 1 ≈ 𝑐 2 , we know 𝑐 2 is 𝑥 := 𝑒. From the evaluation rule, we know ⟨𝑚 1, 𝑒⟩ ⇓ 𝑛. From
      Lemma 6, we have that ⟨𝑚 2, 𝑒⟩ ⇓ 𝑛. Since 𝑚 1 ≈𝜎 𝑚 2 , we have 𝑚 1′ = 𝑚 1 [𝑥 := 𝑛] ≈𝜎 𝑚 2 [𝑥 :=
      𝑛] = 𝑚 2′ regardless the label of 𝑥. skip ≈ skip is trivial. The results on 𝜏1 and 𝜏2 are also
      trivial as assignments does not modify the trace.
                               ∅
    • case ⟨𝑚 1, 𝑥 := 𝑒, 𝜎⟩ →
                            − ⟨𝑚 1 [𝑥 := [𝑛]], skip, 𝜎⟩:
      From 𝑐 1 ≈ 𝑐 2 , we know that 𝑐 2 is 𝑥 := 𝑒. There are two cases:
      – (Evaluation rule (OS-Assign-b1)) We have B ⊑𝜎 Γ(𝑥) from the assumption. Hence, ⟨𝑚 2, 𝑥 :=
                ∅
              − ⟨𝑚 2 [𝑥 := [𝑛 ′ ]], skip, 𝜎⟩ for some 𝑛 ′ . Since 𝑚 1 ≈𝜎 𝑚 2 , we have that 𝑚 2 [𝑥 :=
        𝑒, 𝜎⟩ →
           ′
        [𝑛 ]] ≈𝜎 𝑚 1 [𝑥 := [𝑛]]. skip ≈ skip is trivial. The results on 𝜏1 and 𝜏2 are also trivial as
        they remain unchanged.
      – (Evaluation rule (OS-Assign-b2)) We have ⟨𝑚 1, 𝑒⟩ ⇓ [𝑛] in this case. From Lemma 6, we
                                                                                   ∅
         have that ⟨𝑚 2, 𝑒⟩ ⇓ [𝑛 ′ ] for some 𝑛 ′ . Hence, ⟨𝑚 2, 𝑥 := 𝑒, 𝜎⟩ →     − ⟨𝑚 2 [𝑥 := [𝑛 ′ ]], skip, 𝜎⟩ for
         some 𝑛 . Since 𝑚 1 ≈𝜎 𝑚 2 , we have 𝑚 1 [𝑥 := [𝑛]] ≈𝜎 𝑚 2 [𝑥 := [𝑛 ′ ]]. skip ≈ skip is trivial.
                  ′

         The results on 𝜏1 and 𝜏2 are also trivial as they remain unchanged.
                                   𝜏1
    • case ⟨𝑚 1, 𝑐 3 ; 𝑐 4, 𝜎⟩ −→ ⟨𝑚 1′ , 𝑐 3′ ; 𝑐 4, 𝜎1 ⟩:
      Command 𝑐 1 has the form (𝑐 3 ; 𝑐 4 ), so command 𝑐 2 must have the same form (𝑐 5 ; 𝑐 6 ) where
                                                                                                     𝜏1
      𝑐 3 ≈ 𝑐 5 and 𝑐 4 ≈ 𝑐 6 . According to the evaluation rule, we know that ⟨𝑚 1, 𝑐 3, 𝜎⟩ −→ ⟨𝑚 1′ , 𝑐 3′ , 𝜎1 ⟩.
      By the induction hypothesis, we know from 𝑐 3 ≈ 𝑐 5 that either ⟨𝑚 2, 𝑐 5, 𝜎⟩ diverges, or
                     𝜏2 ∗
      ⟨𝑚 2, 𝑐 5, 𝜎⟩ −→ ⟨𝑚 2′ , 𝑐 5′ , 𝜎2 ⟩ where 𝜎2 = 𝜎1 , 𝑚 1′ ≈𝜎1 𝑚 2′ and ⌊𝜏1 ⌋ L = ⌊𝜏2 ⌋ L . In either case, we
      select 𝑐 2′ as 𝑐 5′ ; 𝑐 6 . In the first case, 𝑐 2′ diverges. In the second case, from the evaluation rule,
                                   𝜏2 ∗
      we have ⟨𝑚 2, 𝑐 5 ; 𝑐 6, 𝜎1 ⟩ −→ ⟨𝑚 2′ , 𝑐 5′ ; 𝑐 6, 𝜎2′ ⟩ where 𝑚 1′ ≈𝜎1 𝑚 2′ and ⌊𝜏1 ⌋ L = ⌊𝜏2 ⌋ L , and 𝜎1 = 𝜎2
      from the induction hypothesis.
                                                   ∅
    • case ⟨𝑚 1, if (𝑒) then 𝑐 3 else 𝑐 4, 𝜎⟩ →
                                              − ⟨𝑚 1, 𝑐 3, 𝜎⟩:
      As 𝑐 1 ≈ 𝑐 2 , we know that 𝑐 2 has the form of if (𝑒) then 𝑐 5 else 𝑐 6 where 𝑐 3 ≈ 𝑐 5 , and
      𝑐 4 ≈ 𝑐 6 . From the evaluation rule, we know that ⟨𝑚 1, 𝑒⟩ ⇓ true. By the assumption that
      𝑚 1 ≈𝜎 𝑚 2 and Lemma 6 (expression preserves), we have ⟨𝑚 2, 𝑒⟩ ⇓ true. Hence, we have that
                                             ∅
      ⟨𝑚 2, if (𝑒) then 𝑐 5 else 𝑐 6, 𝜎⟩ →
                                         − ⟨𝑚 2, 𝑐 5, 𝜎⟩. Since 𝑐 3 ≈ 𝑐 5 and both traces under 𝑚 1 and 𝑚 2
      are empty, we know that by selecting 𝑐 2′ to be 𝑐 5 , all conditions in the conclusion holds.
                                                   ∅
    • case ⟨𝑚 1, if (𝑒) then 𝑐 3 else 𝑐 4, 𝜎⟩ →
                                              − ⟨𝑚 1, 𝑐 4, 𝜎⟩: Similar to the case above.
                                                   ∅
    • case ⟨𝑚 1, if (𝑒) then 𝑐 3 else 𝑐 4, 𝜎⟩ →− ⟨𝑚 1, [𝑐 3 ], 𝜎⟩:
      As 𝑐 1 ≈ 𝑐 2 , we know that 𝑐 2 has the form of if (𝑒) then 𝑐 5 else 𝑐 6 where 𝑐 3 ≈ 𝑐 5 , and 𝑐 4 ≈ 𝑐 6 .
      From the evaluation rule, we know that ⟨𝑚 1, 𝑒⟩ ⇓ [true]. By the assumption that 𝑚 1 ≈𝜎 𝑚 2
      and Lemma 6 (expression equivalence), it must be true that ⟨𝑚 2, 𝑒⟩ ⇓ [𝑏] for some boolean
      value 𝑏. Without losing generality, we consider the case where ⟨𝑚 2, 𝑒⟩ ⇓ [false] so that
                                              ∅
                                         − ⟨𝑚 2, [𝑐 6 ], 𝜎⟩ by the evaluation rule. Let 𝑐 2′ = [𝑐 6 ] ≈ [𝑐 3 ],
      ⟨𝑚 2, if (𝑒) then 𝑐 5 else 𝑐 6, 𝜎⟩ →
      we have 𝑚 2′ = 𝑚 2 ≈𝜎 𝑚 1 = 𝑚 1′ , and the conditions on 𝜏1 and 𝜏2 are trivially true as both 𝑐 1
      and 𝑐 2 produce empty traces.
                                                   ∅
    • case ⟨𝑚 1, if (𝑒) then 𝑐 3 else 𝑐 4, 𝜎⟩ →
                                              − ⟨𝑚 1, [𝑐 4 ], 𝜎⟩: Similar to the case above.


                         Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:14                                                                                     Jeffrey Ching and Danfeng Zhang

                                           ∅
    • case ⟨𝑚 1, while (𝑒) do 𝑐 3, 𝜎⟩ →
                                      − ⟨𝑚 1, if ((𝑒) then 𝑐 3 ; while (𝑒) do 𝑐 3 ) else skip, 𝜎⟩:
      Since 𝑐 1 ≈ 𝑐 2 , we know that 𝑐 2 = while (𝑒) do 𝑐 4 where 𝑐 3 ≈ 𝑐 4 . By the evaluation rule, we
                                           ∅
         have ⟨𝑚 2, while (𝑒) do 𝑐 4, 𝜎⟩ →
                                         − ⟨𝑚 2, if (𝑒) then 𝑐 4 ; while (𝑒) do 𝑐 4 else skip, 𝜎⟩. Hence,
         the conclusion is trivial by selecting 𝑐 2′ as if (𝑒) then 𝑐 4 ; while (𝑒) do 𝑐 4 else skip.
                                                                                     ∅
    • case ⟨𝑚 1, 𝑥 := relabel (𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ →
                                                                    − ⟨𝑚 1 [𝑥 := 𝑛], skip, 𝜎⟩:
      From 𝑐 1 ≈ 𝑐 2 , we know 𝑐 2 has the same form as 𝑐 1 . From the evaluation rule, we have ⟨𝑚 1, 𝑒⟩ ⇓
      𝑛. From Lemma 6 (expression equivalence) and the assumption that 𝑚 1 ≈𝜎 𝑚 2 , we know
                                                                                                             ∅
      ⟨𝑚 2, 𝑒⟩ ⇓ 𝑛. Further, we have ⟨𝑚 2, 𝑥 := relabel (𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ →
                                                                                              − ⟨𝑚 2 [𝑥 :=
      𝑛], skip, 𝜎⟩. Hence, 𝑚 1 [𝑥 := 𝑛] ≈𝜎 𝑚 2 [𝑥 := 𝑛] regardless of the label of 𝑥. skip ≈ skip is
      trivial. The results on 𝜏1 and 𝜏2 are also trivial as the relabel command does not generate any
      events.
                                                                    ∅
    • case ⟨𝑚 1, 𝑥 := relabel (𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ →
                                                                    − ⟨𝑚 1 [𝑥 := [𝑛]], skip, 𝜎⟩:
      From 𝑐 1 ≈ 𝑐 2 , we know 𝑐 2 has the same form as 𝑐 1 . There are two corresponding evaluation
      rules (OS-Relabel-r1) and (OS-Relabel-r2). The proofs are the same as the cases of (OS-
      Assign-b1) and (OS-Assign-b2) respectively.
                                                                                     ∅
    • case ⟨𝑚 1, 𝑥 := relabel (𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ →
                                                                    − ⟨𝑚 1, skip, 𝜎⟩:
      From 𝑐 1 ≈ 𝑐 2 , we know 𝑐 2 has the same form as 𝑐 1 . Since both 𝑐 1 and 𝑐 2 are evaluated under
      the same 𝜎, we know that evaluating 𝑐 2 under 𝜎 also follows Rule (RelabelFail), and hence,
                                                                             ∅
         ⟨𝑚 2, 𝑥 := relabel (𝑒, 𝑝 𝑓 to 𝐿𝑡 using s0 . . . sk ), 𝜎⟩ →
                                                                  − ⟨𝑚 2, skip, 𝜎⟩. skip ≈ skip is trivial.
         The results on 𝜏1 and 𝜏2 are also trivial as relabel does not modify the trace.
                                                           ⟨𝐿 ′ ,𝑣1 ,𝜎 ⟩
    • case: ⟨𝑚 1, output(𝐿 ′, 𝑒, using s0 . . . sk ), 𝜎⟩ −−−−−−→ ⟨𝑚 1, skip, 𝜎 ′ ⟩:

         Based on the assumption that 𝑐 ≠ output(𝐿 ′, 𝑥, using o𝑥 , s0 . . . sk ), we know that only the
         typing rule (Output) is applicable in this case.
         As 𝑐 1 ≈ 𝑐 2 , we have 𝑐 2 = output(𝐿 ′, 𝑒, using s0 . . . sk ) and
                                                                           ⟨𝐿 ′ ,𝑣2 ,𝜎 ⟩
                       ⟨𝑚 2, output(𝐿 ′, 𝑒, using s0 . . . sk ), 𝜎⟩ −−−−−−→ ⟨𝑚 2, skip, 𝜎 ′ ⟩

         It is easy to show that skip ≈ skip and 𝑚 1′ = 𝑚 1 ≈𝜎′ 𝑚 2 = 𝑚 2′ . To prove ⌊𝜏1 ⌋ L = ⌊𝜏2 ⌋ L , there
         are two cases, 𝐿 ′ ⊑ L and 𝐿 ′ ̸⊑ L.
         – 𝐿 ′ ⊑ L: We show that ⟨𝑚, 𝑒⟩ ⇓ 𝑛 for some 𝑛 without brackets in this case. We proceed by
            assuming that ⟨𝑚, 𝑒⟩ ⇓ [𝑛] and show contradiction.
            From typing rule (Output), we know that Γ ⊢ 𝑒 : 𝑝, s0 . . . sk ⊢ 𝑝 <            ′
                                                                                        ∼ 𝐿 . From Lemma 4
            and the assumption that ⟨𝑚, 𝑒⟩ ⇓ [𝑛], we have B ⊑𝜎 𝑝, which implies {|𝐵|}𝜎 ⊑ {|𝑝 }| 𝜎 by
            definition. By Theorem 2 and s0 . . . sk ⊢ 𝑝 <     ′                     ′
                                                           ∼ 𝐿 , we know {|𝑝 }| 𝜎 ⊑ 𝐿 , which when combined
            with {|𝐵|}𝜎 ⊑ {|𝑝 }| 𝜎 can derive {|𝐵|}𝜎 ⊑ 𝐿 . By the assumption that 𝐿 ′ ⊑ L, we get {|𝐵|}𝜎 ⊑ L,
                                                        ′

            which contradicts the assumption that {|𝐵|}𝜎 ̸⊑ L in the theorem statement.
            Hence, it must be true that ⟨𝑚 1, 𝑒⟩ ⇓ 𝑛 for some 𝑛. From Lemma 6, we have ⟨𝑚 2, 𝑒⟩ ⇓ 𝑛
            too. Hence, both output traces under 𝑚 1 and 𝑚 2 produce the same output event ⟨𝐿 ′, 𝑛, 𝜎⟩ =
            ⟨𝐿 ′, 𝑛, 𝜎⟩.
         – 𝐿 ′ ̸⊑ L: The projection traces on L are empty ⌊𝜏1 ⌋ L = ∅ = ⌊𝜏2 ⌋ L by definition of ⌊⌋ L
            (Definition 3). Also, the security event traces are still identical has they remain the same.
                                                          ∅
    • case ⟨𝑚 1, output(𝐿 ′, 𝑒, using s0 . . . sk ), 𝜎⟩ →
                                                        − ⟨𝑚 1, skip, 𝜎⟩:
      From 𝑐 1 ≈ 𝑐 2 , we know 𝑐 2 has the same form as 𝑐 1 . Since 𝑐 2 is executed under the same
                                                                                              ∅
         event trace 𝜎, we know that ⟨𝑚 2, output(𝐿 ′, 𝑒, using s0 . . . sk ), 𝜎2 ⟩ →
                                                                                    − ⟨𝑚 2, skip, 𝜎2 ⟩ as well.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                                        360:15


      Hence, we can easily check 𝑚 2′ = 𝑚 2 ≈𝜎 𝑚 1 = 𝑚 1′ and skip ≈ skip. The results on 𝜏1 and 𝜏2
      are also trivial as they are both empty.
    • case ⟨𝑚 1, eventon(s), 𝜎⟩ → ⟨𝑚 1, skip, 𝜎 · s⟩:
      From 𝑐 1 ≈ 𝑐 2 , 𝑐 2 has the same form of 𝑐 1 . From evaluation rule, we have ⟨𝑚 2, eventon(s), 𝜎⟩ →
      ⟨𝑚 2, skip, 𝜎 · s⟩. Hence, it is easy to check that 𝑚 2′ = 𝑚 2 ≈ 𝑚 1 = 𝑚 1′ and skip ≈ skip.
      Moreover, both traces produce the same security event s, and produce 𝜎 · s. Since there are
      no outputs, ⌊𝜏1 ⌋ L = ∅ = ⌊𝜏2 ⌋ L .
    • case ⟨𝑚, eventoff(s), 𝜎1 ⟩ → ⟨𝑚, skip, 𝜎1 · ¬s⟩: Similar to the previous case.
                                                                                                         □
  Theorem (End-to-end Soundness, Theorem 3). For all commands c and memory 𝑚, an arbitrary
source label B, an arbitrary attacker’s level L, if 𝑝𝑐, Γ ⊢ 𝑐 for some program counter 𝑝𝑐 and typing
environment Γ, then the program c satisfies dynamic release, which means that


  ∀𝑚, 𝜏 . ⟨𝑚, 𝑐, 𝜎⟩ ↩→ 𝜏 ⇒ ∀1 ≤ 𝑖 ≤ ∥𝜏 ∥.
                                                                                     (
                                                                 [:𝑖 ]                   J𝑚K≠B,                            transient
                                                     𝑘 2 (𝑐, 𝜏           , L, B) ⊇
                                                                                         J𝑚K≠B ∩ 𝑘 1 (𝑐, 𝜏 [:𝑖 −1] , L),   persistent
   Proof. We conduct a proof by induction on the trace length for both transient and persistent
policies. Note that unlike a traditional proof for static noninterference, we need to show that under
two indistinguishable initial memories, they both produce consistent, rather than indistinguishable
traces. According to its definition (Definition 7), proving consistency boils down to filtering out
sub-traces where {|B|}𝜎 ⊑ L (i.e., when information with label B can be released), and showing the
remaining sub-traces are indistinguishable.
  Transient policy. We approach the proof by showing that a slightly stronger result holds:
  ∀𝑚, 𝑚 ′, 𝜏, 𝑐, 𝑝𝑐, Γ, 𝜎. 𝜎 |= 𝑚 ∧ 𝜎 |= 𝑚 ′ ∧ 𝑝𝑐, Γ ⊢ 𝑐 ∧ ⟨𝑚, 𝑐, 𝜎⟩ ↩→ 𝜏 ∧ 𝑚 ≈ 𝑚 ′ ⇒
                                                                                         ∀0 ≤ 𝑖 ≤ ∥𝜏 ∥. 𝑚 ′ ∈ 𝑘 2 (𝑐, 𝜏 [:𝑖 ] , L, B)   (1)
The reason is that ∀𝑚 ′ ∈ J𝑚K≠B (i.e., only the values of variables with label B differ), 𝑚 ′ ≈ 𝑚 by
definition of ≈.
  Further, by expending the definition of 𝑘 2 , we argue that it is sufficient to prove the following
condition.
  ∀𝑚, 𝑚 ′, 𝜏, 𝜏 ′, 𝑐, 𝑝𝑐, Γ, 𝜎. 𝜎 |= 𝑚 ∧ 𝜎 |= 𝑚 ′ ∧ 𝑝𝑐, Γ ⊢ 𝑐 ∧ ⟨𝑚, 𝑐, 𝜎⟩ ↩→ 𝜏 ∧ ⟨𝑚 ′, 𝑐, 𝜎⟩ ↩→ 𝜏 ′ ∧𝑚 ≈ 𝑚 ′ ⇒
                                                                                          ∀1 ≤ 𝑖 ≤ ∥𝜏 ∥. ∃𝑗 . 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 ] . (2)
The reason is that if the claim is correct, then
                           𝑚 ′ ∈ 𝑘 1 (𝑐, 𝜏 ′[:𝑗 ] , L)                                                                                  (3)
                                                          Ø
                                ⊆                                                        𝑘 1 (𝑐, 𝜏 ′′[:𝑘 ] , L)                         (4)
                                    ∃𝑚 ′′ , 𝑘. ⟨𝑚 ′′ ,𝑐 ⟩↩→𝜏 ′′ ∧𝜏 ′′[:𝑘 ] ≡B,L𝜏 [:𝑖 ]

                                ≜ 𝑘 2 (𝑐, 𝜏 [:𝑖 ] , L, B)                                                                               (5)
where (3) is true since ⟨𝑚 ′, 𝑐, 𝜎⟩ ↩→ 𝜏 ′ , and (4) is true since we know that ⟨𝑚 ′, 𝑐, 𝜎⟩ ↩→ 𝜏 ′ ∧
𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 ] .
    Next, we perform induction on 𝑖 to prove that Equation (2) holds.
       • Base case: This case is trivial, as any trace is consistent with an empty trace by definition.

                        Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:16                                                                                                                  Jeffrey Ching and Danfeng Zhang

                                      𝜏[:i] and 𝜏′ [:j] are consistent
                                                   ⟨ L′, v1, σ1 ⟩                      ⟨ L′, vi, σi ⟩
                                    𝜏 ⟨m1,c1,σ1⟩                ⟨m2,c2,σ2⟩   ⟨mi,ci,σi⟩               ⟨mi+1,ci+1,σi+1⟩


                                                      B⋢ σ1 L                               B⋢ σi L
                                                                                                        Either diverges or ∃j′



                                    𝜏′ ⟨m′1,c′1,σ1⟩          ⟨m′2,c′2,σ2⟩    ⟨m′j,c′j,σj⟩          * ⟨m′j′ c′ j′,σ j′ ⟩
                                          Induction Hypothesis                To prove: Use Unwinding Lemma


Fig. 20. The orange part is the induction hypothesis for the transient policy statement, and the green part is the
step to be proved with the Unwinding Lemma.


    • Inductive case: Based on the induction hypothesis, we know that at step 𝑖, ∃𝑗 . 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 ] .
                                                          ′
      We need to prove that at step 𝑖 + 1, ∃𝑗 ′ . 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖+1] . Next, we use 𝜎𝑖 to denote 𝜏 [:𝑖 ] and
      𝜎𝑖+1 to denote 𝜏 [:𝑖+1] . The proof is separated into two cases:
      – Case where {|B|}𝜎𝑖 ̸⊑ L: Following Figure 20, the green part illustrate the new index 𝑗 ′ that
        we need to find in order to match index 𝑖 + 1 on the first trace, while the orange part is
        given from the induction hypothesis: the two traces 𝜏 [:𝑖 ] and 𝜏 ′[:𝑗 ] are consistent. The main
        result we use to find 𝑗 ′ to finish the green part is the unwinding lemma (Lemma 2).
        From the induction hypothesis, we also have that 𝜎𝑖 |= 𝑚𝑖 , 𝜎𝑖 |= 𝑚𝑖′ , and 𝑚𝑖 ≈ 𝑚𝑖′ at step 𝑖.
        Moreover, by Lemma 7 (Preservation), we have 𝑝𝑐, Γ ⊢ 𝑐𝑖 and 𝑝𝑐, Γ ⊢ 𝑐 ′𝑗 (i.e., the programs 𝑐𝑖
        and 𝑐 ′𝑗 remain well-typed during evaluation). For the extra event 𝑣𝑖 produced by ⟨𝑚𝑖 , 𝑐𝑖 , 𝜎𝑖 ⟩
        (in the green part of Figure 20), we know that by Definition 6,
                                                                      (
                                    ⟨𝐿 ′ ,𝑣,𝜎𝑖 ⟩                        {𝑣 }, when 𝐿 ′ ⊑ L
                  ⌊⟨𝑚𝑖 , 𝑐𝑖 , 𝜎𝑖 ⟩ −−−−−−→ ⟨𝑚𝑖+1, 𝑐𝑖+1, 𝜎𝑖+1 ⟩⌋ B,L ≜
                                                                        ∅, when 𝐿 ′ ̸⊑ L
           ∗ In the first case where 𝐿 ′ ⊑ L, from Lemma 2, either the program ⟨𝑚 ′𝑗 ′ , 𝑐 ′𝑗 ′ , 𝜎 𝑗 ′ ⟩ diverges
             or, there exists 𝑗 ′ such that
                            𝜏′ ∗                                                                                                         ′
           ⟨𝑚 ′𝑗 , 𝑐 ′𝑗 , 𝜎 𝑗 ⟩ −→ ⟨𝑚 ′𝑗 ′ , 𝑐 ′𝑗 ′ , 𝜎 𝑗 ′ ⟩ ∧ 𝑚𝑖+1 ≈ 𝑚 ′𝑗 ′ ∧ 𝑐𝑖+1 ≈ 𝑐 ′𝑗 ′ ∧ ⌊⟨𝐿 ′, 𝑣, 𝜎𝑖 ⟩⌋ L = ⌊𝜏 ′[ 𝑗:𝑗 ] ⌋ L
                                                                    ′                                                            ′
             Since 𝐿 ′ ⊑ L, we have ⌊𝜏 ′[ 𝑗:𝑗 ] ⌋ L = ⟨𝐿 ′, 𝑣, 𝜎𝑖 ⟩, and hence, ⌊𝜏 ′[ 𝑗:𝑗 ] ⌋ B,L = ⟨𝐿 ′, 𝑣, 𝜎𝑖 ⟩ =
             ⌊𝜏 [𝑖:𝑖+1] ⌋ B,L as {|B|}𝜎𝑖 ̸⊑ L. By induction hypothesis and the fact that the segment 𝜏 [𝑖:𝑖+1]
                          ′                                             ′
             and 𝜏 [ 𝑗:𝑗 ] are also consistent, we know that 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖+1] stands.
             In the case where the program ⟨𝑚 ′𝑗 ′ , 𝑐 ′𝑗 ′ , 𝜎 𝑗 ′ ⟩ diverges, we note that the dynamic re-
             lease policy is defined as a termination insensitive policy. Hence, the policy incurs no
             restrictions in this case.
           ∗ In the second case where 𝐿 ′ ̸⊑ L, no output observable to the attacker at level L is
                                                                              ′                      ′
             produced. Hence, we simply set 𝑗 ′ = 𝑗 and have 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖+1] as 𝜏 ′[:𝑗 ] = 𝜏 ′[:𝑗 ] ,
             𝜏 [:𝑖 ] = 𝜏 ′[:𝑖+1] and from the induction hypothesis, 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 ] .
         – Case where {|B|}𝜎𝑖 ⊑ L: By the induction hypothesis, the two traces 𝜏 [:𝑖 ] and 𝜏 ′[:𝑗 ] are
           consistent. For the extra event 𝑣𝑖 produced by ⟨𝑚𝑖 , 𝑐𝑖 , 𝜎𝑖 ⟩ (in the green part of Figure 20),
           we know that by Definition 6,
                                                             ⟨𝐿 ′ ,𝑣,𝜎𝑖 ⟩
                                     ⌊⟨𝑚𝑖 , 𝑐𝑖 , 𝜎𝑖 ⟩ −−−−−−→ ⟨𝑚𝑖+1, 𝑐𝑖+1, 𝜎𝑖+1 ⟩⌋ B,L ≜ ∅
           since by definition, the projection only includes events produced when {|B|}𝜎𝑖 ̸⊑ L.
                                                       ′                         ′
           Hence, we simply set 𝑗 ′ = 𝑗 and have 𝜏 ′[:𝑗 ] ≡𝐵,𝐿 𝜏 [:𝑖+1] as 𝜏 ′[:𝑗 ] = 𝜏 ′[:𝑗 ] , 𝜏 [:𝑖 ] = 𝜏 ′[:𝑖+1] and
           from the induction hypothesis, 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 ] .

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
Sound Enforcement of Dynamic Release Information Flow Policy                                                              360:17


                                 Hypothesis: m′ ∈ 𝑘1(𝑐, 𝜏 [:𝑖−1] , 𝐿)         To prove: m′ ∈ 𝑘1(𝑐, 𝜏 [:𝑖] , 𝐿)
                               m                                        k     i-1                   i     ⎣𝜏⎦L
                                         1


                                    output1(L,x)         outputk(L,x)          outputi(L,x)      𝜏[i]
                                                   ...                       ...




                                                                                    =
                                        =




                                                            =
                                    output1(L,x)         outputk(L,x)          outputj(L,x)      𝜏′ [j]

                               m′        1                              k′    j′                    j
                                                                                                          ⎣𝜏′ ⎦L



Fig. 21. This Figure shows that 𝑚 ′ ∈ 𝑘 1 (𝑐, 𝜏 [:𝑖 ],𝐿 ), which indicates the variable 𝑥 has previously been output. This
difference causes the proof not to be concluded with Unwinding Lemma.


   Persistent policy. We approach the proof by showing that a slightly stronger result holds:
   ∀𝑚, 𝑚 ′, 𝜏, 𝜏 ′, 𝑐, 𝑝𝑐, Γ, 𝜎. 𝜎 |= 𝑚 ∧ 𝜎 |= 𝑚 ′ ∧ 𝑝𝑐, Γ ⊢ 𝑐 ∧ ⟨𝑚, 𝑐, 𝜎⟩ ↩→ 𝜏 ∧ 𝑚 ≈ 𝑚 ′ ⇒
                                                   ∀0 ≤ 𝑖 ≤ ∥𝜏 ∥. 𝑚 ′ ∈ 𝑘 1 (𝑐, 𝜏 [:𝑖 −1] , L) ⇒ 𝑚 ′ ∈ 𝑘 2 (𝑐, 𝜏 [:𝑖 ] , L, B)
   The reason is similar to the transient policy case, except that a persistent policy allows previous
outputs to be released once again by having 𝑚 ′ ∈ 𝑘 1 (𝑐, 𝜏 [:𝑖 −1] , L) as an assumption before the
conclusion 𝑚 ′ ∈ 𝑘 2 (𝑐, 𝜏 [:𝑖 ] , L, B).
   Further, by expending the definition of 𝑘 1 and 𝑘 2 , we argue that it is sufficient to show the
following
   ∀𝑚, 𝑚 ′, 𝜏, 𝜏 ′, 𝑐, 𝑝𝑐, Γ, 𝜎. 𝜎 |= 𝑚 ∧ 𝜎 |= 𝑚 ′ ∧ 𝑝𝑐, Γ ⊢ 𝑐 ∧ ⟨𝑚, 𝑐, 𝜎⟩ ↩→ 𝜏 ∧ ⟨𝑚 ′, 𝑐, 𝜎⟩ ↩→ 𝜏 ′ ∧𝑚 ≈ 𝑚 ′ ⇒
                                                     ∀1 ≤ 𝑖 ≤ ∥𝜏 ∥. ⌊𝜏 [:𝑖 −1] ⌋ L ⪯ ⌊𝜏 ′ ⌋ L ⇒ ∃𝑗 . 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 ] . (6)
  The reason is that
  (1) We can rewrite 𝑚 ′ ∈ 𝑘 1 (𝑐, 𝜏 [:𝑖 −1] , L) to ⌊𝜏 [:𝑖 −1] ⌋ L ⪯ ⌊𝜏 ′ ⌋ L by the definition of 𝑘 1 .
  (2) Similar to Equations (3)-(5), we can replace the requirement that 𝑚 ′ ∈ 𝑘 2 (𝑐, 𝜏 [:𝑖 ] , L, B) with
      𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 ] .
  Next, we perform induction on 𝑖 to prove that Equation (6) holds.
  The proof is mostly identical to the transient case as Equation 6 is a relaxed version of Equation 2.
The exception is for the case of
                          (𝑐 = output(𝐿, 𝑥, using o𝑥 , s0 . . . sk )) ∧ 𝑥 is immutable)
because we cannot use the unwinding lemma (Lemma 2) to derive low equivalence on traces when
the 𝑖-th step on 𝜏, from index 𝑖 to 𝑖 + 1. We need a new proof strategy for this case, which is
illustrated by the green dotted box in Figure 21.
    When evaluation rule (Output-Fail) is applied at index 𝑖, the command has the same semantics
                                                                               ′                     ′
as a skip command. Hence, we simply set 𝑗 ′ = 𝑗 and have 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖+1] as 𝜏 ′[:𝑗 ] = 𝜏 ′[:𝑗 ] ,
𝜏 [:𝑖 ] = 𝜏 ′[:𝑖+1] and from the induction hypothesis, 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 ] .
    When evaluation rule (Output-Succ) is applied at index 𝑖, we know that 𝑥 has been released at
some level 𝐿 ′ ⊑ L in the past. That is, an output ⟨𝐿 ′, 𝑣, 𝜎⟩ ∈ ⌊𝜏 [:𝑖 −1] ⌋ L for some value 𝑣 and 𝜎 was
produced by an output command output(𝐿 ′, 𝑥, using s0 . . . sk ) executed on trace 𝜏 [:𝑖 −1] , where
𝐿 ′ ⊑ L. Hence, on trace 𝜏, step 𝑖 produces an output event ⟨𝐿 ′, 𝑣, 𝜎 ′ ⟩ for some 𝜎 ′ . Note that since 𝑥
is immutable, the output value must be the same as the previous output 𝑣.
                                                                                      ′
    On trace 𝜏 ′ , by induction hypothesis, there must be some 𝑗 ′ such that 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 −1] . Due to
                                                                                                              ′
the assumption that ⌊𝜏 [:𝑖 −1] ⌋ L ⪯ ⌊𝜏 ′ ⌋ L , we know that there must be an output ⟨𝐿 ′, 𝑣, 𝜎 ′′ ⟩ ∈ ⌊𝜏 ′[:𝑗 ] ⌋ L
                                                                                                                 ′
for some 𝜎 ′′ produced by an output command output(𝐿 ′, 𝑥, using s0 . . . sk ) executed on trace 𝜏 ′[:𝑗 ] .

                          Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
360:18                                                                                   Jeffrey Ching and Danfeng Zhang


This is illustrated in Figure 21: the orange part shows that before index 𝑖 − 1, the projection on L has
𝑘 output events, which are identical to the first 𝑘 output events on trace ⌊𝜏 ′ ⌋ L due to the induction
hypothesis. Hence, we let 𝑗 = 𝑗 ′ + 1. On trace 𝜏 ′ , step 𝑗 produces an output event ⟨𝐿 ′, 𝑣, 𝜎 ′ ⟩. Again,
since 𝑥 is immutable, the output value must be the same as the previous output 𝑣. Since the outputs
are the same at 𝜏 [𝑖 ] and 𝜏 ′[ 𝑗 ] , the 𝜏 [:𝑖 ] and 𝜏 ′[:𝑗 ] are still consistent 𝜏 ′[:𝑗 ] ≡B,L 𝜏 [:𝑖 ] , as illustrated in
the green part of Figure 21.                                                                                                □

Received 2026-03-17; accepted 2026-08-06




Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 360. Publication date: October 2026.
