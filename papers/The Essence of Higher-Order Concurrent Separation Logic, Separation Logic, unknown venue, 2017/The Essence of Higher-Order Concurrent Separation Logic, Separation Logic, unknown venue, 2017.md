       The Essence of Higher-Order Concurrent
                  Separation Logic

    Robbert Krebbers1(B) , Ralf Jung2 , Aleš Bizjak3 , Jacques-Henri Jourdan2 ,
                      Derek Dreyer2 , and Lars Birkedal3
               1
                Delft University of Technology, Delft, The Netherlands
                             mail@robbertkrebbers.nl
          2
            MPI-SWS, Saarland Informatics Campus, Saarbrücken, Germany
                       {jung,jjourdan,dreyer}@mpi-sws.org
                       3
                         Aarhus University, Aarhus, Denmark
                           {abizjak,birkedal}@cs.au.dk

        Abstract. Concurrent separation logics (CSLs) have come of age, and
        with age they have accumulated a great deal of complexity. Previous
        work on the Iris logic attempted to reduce the complex logical mecha-
        nisms of modern CSLs to two orthogonal concepts: partial commutative
        monoids (PCMs) and invariants. However, the realization of these con-
        cepts in Iris still bakes in several complex mechanisms—such as weakest
        preconditions and mask-changing view shifts—as primitive notions.
           In this paper, we take the Iris story to its (so to speak) logical conclu-
        sion, applying the reductionist methodology of Iris to Iris itself. Speciﬁ-
        cally, we deﬁne a small, resourceful base logic, which distills the essence
        of Iris: it comprises only the assertion layer of vanilla separation logic,
        plus a handful of simple modalities. We then show how the much fancier
        logical mechanisms of Iris—in particular, its entire program speciﬁcation
        layer—can be understood as merely derived forms in our base logic. This
        approach helps to explain the meaning of Iris’s program speciﬁcations
        at a much higher level of abstraction than was previously possible. We
        also show that the step-indexed “later” modality of Iris is an essential
        source of complexity, in that removing it leads to a logical inconsistency.
        All our results are fully formalized in the Coq proof assistant.

1     Introduction
In his paper The Next 700 Separation Logics, Parkinson [26] observed that “sep-
aration logic has brought great advances in the world of veriﬁcation. However,
there is a disturbing trend for each new library or concurrency primitive to
require a new separation logic.” He argued that what is needed is a general
logic for concurrent reasoning, into which a variety of useful speciﬁcations can
be encoded via the abstraction facilities of the logic. “By ﬁnding the right core
logic,” he wrote, “we can concentrate on the diﬃcult problems.”
    The logic he suggested as a potential candidate for such a core concurrency
logic was deny-guarantee [12]. Deny-guarantee was indeed groundbreaking in its
support for “ﬁctional separation”—the idea that even if threads are concurrently
manipulating the same shared piece of physical state, one can view them as oper-
ating on logically disjoint pieces of it and use separation logic to reason modularly

c Springer-Verlag GmbH Germany 2017
H. Yang (Ed.): ESOP 2017, LNCS 10201, pp. 696–723, 2017.
DOI: 10.1007/978-3-662-54434-1 26
                  The Essence of Higher-Order Concurrent Separation Logic       697

about those pieces. It was, however, far from the last word on the subject. Rather,
it spawned a new breed of logics with ever more powerful ﬁctional-separation
mechanisms for reasoning modularly about interference [9,11,16,27,29,30]. Sev-
eral of these also incorporated support for impredicative invariants [4,17,18,28],
which are needed if one aims to verify code in languages with semantically cyclic
features (such as ML or Rust, which support higher-order state).
    Although exciting, the progress in this area has come at a cost: as these new
separation logics become ever more expressive, each one accumulates increasingly
baroque and bespoke proof rules, which are primitive in the sense that their
soundness is established by direct appeal to the also baroque and bespoke model
of the logic. As a result, it is diﬃcult to understand what program speciﬁcations
in these logics really mean, how they relate to one another, or whether they can
be soundly combined in one reasoning framework. In short, we feel, it is high
time to renew Parkinson’s quest for “the right core logic” of concurrency.
    Toward this end, Jung et al. [17,18] recently developed Iris, a higher-order
concurrent separation logic with the goal of simpliﬁcation and consolidation. The
key idea of Iris is that even the fanciest of the interference-control mechanisms in
recent concurrency logics can be expressed by a combination of two orthogonal
ingredients: partial commutative monoids (PCMs) and invariants. PCMs enable
the user of the logic to roll their own type of ﬁctional (or “logical” or “ghost”)
state, and invariants serve to tie that ﬁctional state to the underlying physical
state of the program. Using just these two mechanisms, Jung et al. showed how
to take complex primitive proof rules from prior logics and derive them within
Iris, leading to the slogan: “Monoids and invariants are all you need.”
    Unfortunately, that slogan does not tell the whole story. Although monoids
and invariants do indeed constitute the two main conceptual elements of Iris—
and they are arguably “canonical” in their simplicity and universality—the real-
ization of these concepts in Iris involves a number of interacting logical mecha-
nisms, some of which are simple and canonical, others not so much:

– Ownership assertions, a γ , for logical (ghost) state.
– Named invariant assertions, P ι , asserting that ι is the name of an invariant
  that enforces that P holds of some piece of the shared state. Invariants in Iris
  are impredicative, which means that P ι can be used anywhere where normal
  assertions can be used, e.g., in invariants themselves.
– A necessity modality,  P , which asserts that P holds persistently, as opposed
  to an assertion describing exclusive ownership of some resource.
– A “later” modality,  P . To support impredicative higher-order quantiﬁcation
  and recursively deﬁned assertions, the model of Iris employs the technique
  of step-indexing [2]. This is reﬂected in the logic in the form of  P , which
  roughly asserts that P will be true after the next step of computation.
– Invariant masks, E, which are sets of invariant names, ι. Masks are used to
  track which invariants are enabled (i.e., currently satisﬁed by some piece of
  shared state) at a given point in a program proof.
698     R. Krebbers et al.

– Mask-changing view shifts, P E1 E2 Q. These describe a kind of logical update
  operation, asserting (roughly) that, if the invariants in E1 hold, P can be
  transformed to Q, after which point the invariants in E2 hold. These view
  shifts are useful for expressing the temporary disabling and re-enabling of
  invariants within the veriﬁcation of an atomic step of computation.
– Weakest preconditions, wpE e {Φ}, which establish that e is safe to execute
  assuming the invariants in E hold, and that if e computes to a value v, then
  Φ(v) holds. Hoare triples are encodable in terms of weakest preconditions.

    Associated with each of these logical mechanisms are a signiﬁcant number of
primitive proof rules. For certain features, such as the  P modality, the rules
are mostly standard, and the model is very simple. In contrast, the primitive
proof rules for weakest preconditions and view shifts are non-standard, and the
model of these features is extremely involved, making the justiﬁcation of the
primitive rules—not to mention the very meaning of Iris’s Hoare-style program
speciﬁcations—painfully diﬃcult to understand or explain. Indeed, the previous
Iris papers [17,18] have avoided even attempting to present the formal model of
program speciﬁcations in any detail at all.
    In the present paper, we rectify this situation by taking the Iris story to
its (so to speak) logical conclusion—that is, by applying the reductionist Iris
methodology to Iris itself! Speciﬁcally, we present a small, resourceful base logic,
which distills the essence—the minimal, primitive core—of Iris: it comprises only
the assertion layer of vanilla separation logic (i.e., including P ∗ Q but not Hoare
triples) extended with  P,  P , and a simple, novel, monadic update modality,
|P . Using these basic mechanisms, the fancier mechanisms of mask-changing
view shifts and weakest preconditions—and their associated proof rules—can all
be derived within the logic. And by expressing the fancier mechanisms as derived
forms, we can now explain the meaning of Iris’s program speciﬁcations at a much
higher level of abstraction than was previously possible.
    In Sect. 2, we begin by presenting from ﬁrst principles the reduced base logic
that constitutes the primitive core of our new version of Iris (version 3.0). Then,
in Sect. 3, we explain step-by-step how to encode weakest preconditions in the
Iris 3.0 base logic. Next, in Sect. 4, we show how our base logic is suﬃcient to
derive the remaining mechanisms and proof rules of full Iris, including named
invariants and mask-changing view shifts.
    On the negative side, there is one point of unfortunate complexity that Iris 3.0
inherits from earlier versions without simpliﬁcation: the aforementioned “later”
modality,  P . The Iris rule for accessing an invariant P ι says that when we
gain control of the resource satisfying the invariant, we only learn  P , not P . It
has proven very diﬃcult to explain to users of Iris the role of  here because it
boils down to “the model made me do it”: the  reﬂects a corresponding place
in the existing step-indexed model of Iris where the step-index is decreased to
ensure a well-founded construction. Moreover,  P is in general strictly weaker
than P , and experience working with Iris has shown that in certain cases this
weakness forces the user of the logic into painful workarounds. In Sect. 5, we
                    The Essence of Higher-Order Concurrent Separation Logic          699

show that in the proof rule for accessing an invariant, the use of  (or something
like it) is in fact essential, because if  is removed from the rule, Iris becomes
inconsistent. This provides evidence that  is a kind of necessary evil.
    Finally, in Sect. 6, we discuss related work, and in Sect. 7, we conclude.
    All results in this paper have been formalized in the Coq proof assistant [1].


2     The Iris 3.0 Base Logic
The goal of this section is to introduce the Iris 3.0 base logic, which is the core
logic that all of Iris rests on: all its program-logic mechanisms will be deﬁned in
terms of just the primitive assertions of our base logic.
    The Iris base logic is a higher-order logic with a couple of extensions, most
of which are standard. We will discuss each of these extensions in turn. The
primitive logical assertions are deﬁned by the following grammar:

 P, Q, R ∈ Prop ::= True | False | t = u | P ∧ Q | P ∨ Q | P ⇒ Q | ∀x. P | ∃x. P
                   | P ∗ Q | P −∗ Q | Own(a) | V(a) |  P | |P | μ x. P |  P

Since the logic is higher-order, the full grammar of (multi-sorted) terms also
involves the usual connectives of the simply-typed lambda calculus. This is com-
mon practice; the full details are spelled out in the technical appendix [1].
    The rules for the logical entailment1 P Q are displayed in Fig. 1. Note that
P     Q is shorthand for having both P Q and Q P .
    We omit the ordinary rules for intuitionistic higher-order logic with equality,
which are standard and displayed in the appendix [1]. The remaining connectives
and proof principles fall into two broad categories: those dealing with ownership
of resources (Sects. 2.1–2.5) and those related to step-indexing (Sects. 2.6–2.7).

2.1     Separation Logic
The connectives ∗ and −∗ of bunched implications [25] make our base logic a
separation logic: they let us reason about ownership of resources. The key point
is that P ∗ Q describes ownership of a resource that can be separated into two
disjoint pieces, one satisfying P and one satisfying Q. This is in contrast to P ∧Q,
which describes ownership of a resource satisfying both P and Q.
    For example, consider the resources owned by diﬀerent threads in a concur-
rent program. Because these threads operate concurrently, it is crucial that their
ownership is disjoint. As a consequence, separating conjunction is the natural
operator to combine the ownership of concurrent threads.
    Together with separating conjunction, we have a second form of implication:
the magic wand P −∗ Q. It describes ownership of “Q minus P ”, i.e., it describes
resources such that, if you (disjointly) add resources satisfying P , you obtain
resources satisfying Q.
1
    The full judgment is of the shape Γ | P  Q, where Γ assigns types to free variables.
    However, since Γ only plays a role in the rules for quantiﬁers, we omit it.
700      R. Krebbers et al.

Laws of (aﬃne) bunched implications.

      True ∗ P  P                                          −∗-intro           −∗-elim
                                  ∗-mono
        P ∗Q  Q∗P                P1  Q1       P2  Q2       P ∗QR            P  Q −∗ R
(P ∗ Q) ∗ R  P ∗ (Q ∗ R)           P1 ∗ P2  Q1 ∗ Q2        P  Q −∗ R          P ∗QR

Laws for resources and validity.
  own-op                                    own-unit               own-core
  Own(a) ∗ Own(b)  Own(a · b)             True  Own(ε)          Own(a)   Own(|a|)

            own-valid                  valid-op                    valid-always
            Own(a)  V(a)              V(a · b)  V(a)             V(a)   V(a)

Laws for the basic update modality.
      upd-mono
        P Q             upd-intro          upd-trans              upd-frame
      |P  |Q          P  |P            ||P  |P            Q ∗ |P  |(Q ∗ P )

                                upd-update
                                         aB
                                Own(a)  |∃b ∈ B. Own(b)

Laws for the always modality.

                                             True   True                P  P
  -mono
    P Q               -elim           (P ∧ Q)   (P ∗ Q)          ∀x.  P   ∀x. P
   P  Q             P  P           P ∧ Q  P ∗ Q                   ∃x. P  ∃x.  P

Laws for the later modality.
-mono                               ∀x.  P   ∀x. P                (P ∗ Q)   P ∗  Q
  P Q         Löb
               ( P ⇒ P )  P         ∃x. P   False ∨ ∃x.  P            P    P
P  Q

Laws for timeless assertions.
          -timeless                             -own
           P   False ∨ ( False ⇒ P )          Own(a)  ∃b. Own(b) ∧ (a = b)


                       Fig. 1. Proof rules of the Iris 3.0 base logic.


2.2     Resource Algebras

The purpose of the Own(a) connective is to assert ownership of the resource a.
Before we go on introducing this connective, we need to answer the following
question: what is a resource?
    The Iris base logic does not answer this question by ﬁxing a particular set of
resources. Instead, the set of resources is kept general, and it is up to the user
                          The Essence of Higher-Order Concurrent Separation Logic                 701

of the logic to make a suitable choice. All the logic demands is that the set of
resources forms a unital resource algebra (uRA), as deﬁned in Fig. 2.


A resource algebra (RA) is a tuple (M, V ⊆ M, |−| : M → M ? , (·) : M × M → M )
satisfying:

          ∀a, b, c. (a · b) · c = a · (b · c)        ∀a, b. a · b = b · a
              ∀a, b. (a · b) ∈ V ⇒ a ∈ V               ∀a. |a| ∈ M ⇒ |a| · a = a
                  ∀a. |a| ∈ M ⇒ ||a|| = |a|          ∀a, b. |a| ∈ M ∧ a      b ⇒ |b| ∈ M ∧ |a|   |b|
                  ?                              ?               ?       ?
 where        M       M              with       a ·⊥       ⊥·a       a
          a       b   ∃c ∈ M. b = a · c
      a       B       ∀c? ∈ M ? . a · c? ∈ V ⇒ ∃b ∈ B. b · c? ∈ V
         a        b   a    {b}

A unital resource algebra (uRA) is a resource algebra M with an element ε satisfying:

                      ε∈V                  ∀a ∈ M. ε · a = a                  |ε| = ε


                                     Fig. 2. Resource algebras.


   Resource algebras are similar to partial commutative monoids (PCMs), which
are often used to describe ownership in concurrent separation logics because:
– Ownership of diﬀerent threads can be composed using the · operator.
– Composition of ownership is associative and commutative, reﬂecting the asso-
  ciative and commutative semantics of parallel composition.
– Combinations of ownership that do not make sense are ruled out by partiality,
  e.g., multiple threads claiming to have ownership of an exclusive resource.
However, there are some diﬀerences between RAs and PCMs:
1. Instead of partiality, RAs use validity to rule out invalid combinations of
   ownership. Speciﬁcally, there is a subset V of valid elements. As shown pre-
   viously [17], this take on partiality is necessary when deﬁning higher-order
   ghost state, which we will need for modeling invariants in Sect. 4.3.
2. Instead of having one “unit” that acts as the identity for every element, RAs
   have a partial function |−| assigning the (duplicable) core |a| to each element
   a. The core of an RA is a strict generalization of the unit of a PCM: the core
   can be diﬀerent for diﬀerent elements, and since the core is partial, there can
   actually be elements of the RA for which there is no identity element.
    Although the Iris base logic is parameterized by a uRA (that is, an RA with
a single, global unit), we do not demand that every RA have a unit because we
typically compose RAs from smaller parts. Requiring all of these “intermediate”
RAs to be unital would render many of our compositions impossible [17].
    Let us now give some examples of RAs; more appear in Sects. 3.3 and 4.2.
702    R. Krebbers et al.

Exclusive. Given a set X, the task of the exclusive RA Ex(X) is to make sure
that one party exclusively owns a value x ∈ X. (We are using a datatype-like
notation to declare the possible elements of Ex(X).)

      Ex(X)  ex(x : X) |          V  {ex(x) | x ∈ X}         |ex(x)|  ⊥

Composition is always undeﬁned (using the invalid dummy element ) to ensure
that ownership is exclusive, i.e., exactly one party has full control over the
resource. This RA does not have a unit.

Finite Partial Function. Given a set of keys K and an RA M , the ﬁnite partial
                 fin
function uRA K − M is deﬁned by lifting the core and the composition operator
pointwise, and by deﬁning validity as the conjunction of pointwise validities. The
unit ε is deﬁned to be the empty partial function ∅.

2.3   Resource Ownership
Having completed the discussion of RAs, we now come back to the base logic and
its connective Own(a), which describes ownership of the RA element a. It forms
the “primitive” form of ownership in our logic, which can then be composed
into more interesting assertions using the previously described connectives. The
most important fact about ownership is that separating conjunction “reﬂects”
the composition operator of RAs into the logic (own-op).
    Besides the Own(a) connective, we have the primitive connective V(a), which
reﬂects validity of RA elements into the logic. Note that ownership is connected
to validity: the rule own-valid says that only valid elements can be owned.

2.4   Resource Updates
So far, resources have been static: the logic provides assertions to reason about
resources you own, the consequences of that ownership, and how ownership can
be disjointly separated. The (basic) update modality |P , however, lets you talk
about what you could own after performing an update to what you do own.
    Updates to resources are called frame-preserving updates and can be per-
formed using the rule upd-update. We can perform a frame-preserving update
a  B if for any resource (called a frame) af such that a · af ∈ V, there exists
a resource b ∈ B such that b · af ∈ V. If we think of those frames as being the
resources owned by other threads, then a frame-preserving update is guaranteed
not to invalidate the resources of concurrently-running threads. By doing only
frame-preserving updates, we know we will never “step on anybody else’s toes”.
    Before discussing how frame-preserving updates are reﬂected into the logic,
we give some examples of frame-preserving updates. Since ownership in the exclu-
sive RA is exclusive, there is nobody whose assumptions could be invalidated by
changing the value of the resource. To that end, we have ex(x)  ex(y) for any
                                                          fin
x and y. The updates for the ﬁnite partial functions K − M are as follows:
                   The Essence of Higher-Order Concurrent Separation Logic        703

             fpfn-update                         fpfn-alloc
                         a M B                  a∈V        K inﬁnite
             f [i := a]  {f [i := b] | b ∈ B}   ∅  {[i := a] | i ∈ K}

 The ﬁrst rule witnesses pointwise lifting of updates on M . The second rule is
more interesting: it allows us to allocate a fresh slot in the ﬁnite partial function.
This is always possible because only ﬁnitely many indices i ∈ K will be used at
any given point in time.
    The update modality reﬂects frame-preserving updates into the logic, in the
sense that |P asserts ownership of resources that can be updated to resources
satisfying P . The rule upd-update witnesses this relationship, while the remain-
ing proof rules essentially say that | is a strong monad with respect to sepa-
rating conjunction [19,20].
    This gives rise to an alternative interpretation of the basic update modal-
ity: we can think of |P as a thunk that captures some resources in its envi-
ronment and that, when executed, will “return” resources satisfying P . The
various proof rules then let us perform additional reasoning on the result of the
thunk (upd-mono), create a thunk that does nothing (upd-intro), compose two
thunks into one (upd-trans), and add resources to those captured by the thunk
(upd-frame).


2.5   The Always Modality

The intuition for the always modality  P is that P holds without asserting
any exclusive ownership. This is useful because an assumption  P can be used
arbitrarily often, i.e., it cannot be “used up”. In particular, while P −∗ Q is a
“linear implication” and can only be applied once, (P −∗ Q) can be applied
arbitrarily often. We use this in the encoding of Hoare triples in Sect. 3.2.
    We call an assertion P persistent if proofs of P can never assert exclusive
ownership, which formally means it enjoys P  P . As soon as either P or Q is
persistent, their separating conjunction (P ∗ Q) and normal conjunction (P ∧ Q)
coincide, thus enabling one to use “normal” intuitionistic reasoning.
    Under which circumstances is Own(a) persistent? RAs provide a ﬂexible
answer to this: the core |a| deﬁnes the duplicable part of a, and hence Own(|a|)
does not assert any exclusive ownership, which is reﬂected into the logic using
the rule own-core. In Sect. 4.2, we will consider an example of an RA with a
non-trivial core, and we will make use of the fact that Own(|a|) is persistent.


2.6   The Later Modality and Guarded Fixed-Points

Although RAs provide a powerful way to instantiate our logic with the user’s
custom type of resources, they have an inherent limitation: the user-chosen RA
must be deﬁned a priori. But what if the user wants to deﬁne their resources in
terms of the assertions of the logic? In prior work [17], we called this phenomenon
higher-order ghost state, and showed how to incorporate it into the Iris 2.0 logic.
Iris 3.0 inherits higher-order ghost state from Iris 2.0 without change.
704     R. Krebbers et al.

    The challenge of supporting higher-order ghost state is that the user-chosen
RA depends on the type of propositions of our logic, which in turn depends
on the user-chosen RA. In Iris 2.0, we showed how to cut this circularity using
a novel algebraic structure called a CMRA (“camera”), which synthesizes the
features of an RA together with a step-indexed structure [2]. Since a proper
understanding of CMRAs is not needed in order to appreciate the contribution
of the present paper, we refer the reader to the Iris 2.0 paper [17] for details, and
instead focus brieﬂy here on how the presence of higher-order ghost state aﬀects
our base logic. (We will see a concrete instance of higher-order ghost state in
Sect. 4.2, where we use it to encode impredicative invariants.)
    The step-indexing aspect of CMRAs is internalized into the logic by adding
a new modality: the later modality,  P [3,23]. Intuitively,  P asserts that P
holds “at the next step-index” (or “one step later”). In the deﬁnition of weakest
preconditions in Sect. 3.3, we connect  to computation steps, allowing one to
think of  P as saying that P holds at the next step of computation.
    Beyond higher-order ghost state, step-indexing allows us to include a ﬁxed-
point operator μ x. P into the logic, which can be used to deﬁne recursive predi-
cates without any restriction on the variance of the recursive occurrences of x in
P . Instead, all recursive occurrences must be guarded : they have to appear below
a later modality . In Sect. 3, we will show how guarded recursion is used for
deﬁning weakest preconditions. Moreover, as shown in [28], guarded recursion is
useful to deﬁne speciﬁcations for higher-order concurrent data structures.
    A crucial proof rule for  is Löb, which facilitates proving properties about
ﬁxed-points: we can essentially assume that the recursive occurrences are already
proven correct (as they are under a later). Note that many of the usual rules
for later, such as introduction P  P ) and commutativity with other operators
((P ∧ Q)        P ∧  Q) are derivable from the rules in Fig. 1.

2.7   Timeless Assertions
There are some occasions where we inevitably end up with hypotheses below a
later. An example is the Iris rule for accessing invariants (wp-inv in Sect. 4).
Although one can always introduce a later, one cannot just eliminate a later,
so the later may make certain reasoning steps impossible. However, as we will
prove in Sect. 5, it is crucial for logical consistency that the later is present in
wp-inv.
    Still, for many assertions, their semantics is independent of step-indexing, so
adding a  in front of them does not really “change” anything. When accessing
an invariant containing such an assertion, we thus do not want the later to be
in the way. Ideally, for such assertions, we would like to have  P P . However,
that does not work: indeed, at step-index 0,  P trivially holds and, consequently,
does not imply P . Instead, we say that an assertion P is timeless when  P      P,
where the modality is deﬁned by P  P ∨  False. We call this new modality
“except 0”: it states that the given assertion holds at all step-indices greater
than 0. Under this modality, we can strip away a later from a timeless assertion,
i.e., given a timeless P , to prove  P     Q, it is suﬃcient to prove P     Q.
                  The Essence of Higher-Order Concurrent Separation Logic      705

    Using the rules for timeless assertions in Fig. 1, we can prove that some fre-
quently occurring assertions are timeless. In particular, if a CMRA is discrete—
i.e., if it degenerates to a plain RA that ignores the step-indexing structure, as
is the case for many types of resources—then equality, ownership and validity
of such resources are timeless. Furthermore, most of the connectives of our logic
(not including ) preserve timelessness.


2.8   Consistency

Logical consistency is usually stated as True  False, i.e., from a closed context
one cannot prove a contradiction. However, when building a program logic within
our base logic, we wish to prove that the postconditions of our Hoare triples
actually represent program behavior (Sect. 4.6), so we need a stronger statement:

Theorem 2.1 (Soundness of first-order interpretation). Given a ﬁrst-
order proposition φ (not involving ownership, higher-order quantiﬁcation, nor
any of the modalities) and True     (|)n φ, then the “standard” (meta-logic)
interpretation of φ holds. Here, (|)n is notation for nesting | n times.

    The proposition φ should be a ﬁrst-order predicate to ensure it can be used
both inside our logic and at the meta-level. Furthermore, the theorem makes
sure that even when reasoning below any combination of modalities, we cannot
prove a contradiction. Consistency, i.e., True  False, is a trivial consequence of
this theorem: just pick φ = False and n = 0.
    Theorem 2.1 is proven by deﬁning a suitable semantic domain of assertions,
interpreting all connectives into that domain, and proving soundness of all proof
rules. For further details, we refer the reader to [1,17].


3     Weakest Preconditions

This section shows how to encode a program logic in the Iris base logic. Usu-
ally, program logics are centered around Hoare triples, but instead of directly
deﬁning Hoare triples in the base logic, we ﬁrst deﬁne the notion of a weakest
precondition. There are two reasons for deﬁning Hoare triples in terms of the
weakest precondition connective: First, weakest preconditions are more primi-
tive and, as such, more natural to encode. Second, weakest preconditions are
more convenient for performing interactive proofs with Iris [21].
    We will ﬁrst give some intuition about weakest preconditions and how to work
with them. After that, we present the encoding of weakest preconditions in three
stages, gradually adding support for reasoning about state and concurrency. For
simplicity, we use a concrete programming language in this section. The version
including all features of Iris for an arbitrary language is given in Sect. 4.
706      R. Krebbers et al.

3.1    Programming Language
For the purpose of this example, we use a call-by-value λ-calculus with references
and fork. The syntax and semantics are given in Fig. 3.
    Head-reduction (e, σ) →h (e , σ  , ef ) is deﬁned on pairs (e, σ) consisting of
an expression e and a shared heap σ (a ﬁnite partial map from locations to
values). Moreover, ef is a list of forked oﬀ expressions, which is used to deﬁne
the semantics of fork {e}. The head-reduction is lifted to a per-thread reduction
(e, σ) → (e , σ  , ef ) using evaluation contexts. We deﬁne an expression e to be
reducible in a shared heap σ, and we note red(e, σ), if it can make a thread-local
step. The thread-pool reduction (T, σ) →tp (T  , σ  ) is an interleaving semantics
where the thread-pool T denotes the existing threads as a list of expressions.


Syntax:          v ∈ Val ::= () | | λx.e
                e ∈ Expr ::= v | x | e1 (e2 ) | fork {e} | ref(e) | ! e | e1 ← e2
                K ∈ Ctx ::= • | K(e) | v(K) | ref(K) | ! K | K ← e | v ← K

Head reduction:                                              Thread-local reduction:
      ((λx.e)v, σ) →h (e[v/x]      )                                  (e, σ) →h (e , σ ef )
                                                                  (K[ e ], σ) → (K[ e ], σ ef )
           (!    ) →h (       )            if σ( ) = v
      ( ← w, σ) →h ((), σ[ := w] )         if σ( ) = v       Thread-pool semantics:
      (ref(v), σ) →h (     [ := v] )       if σ( ) = ⊥                 (e, σ) → (e , σ ef )
   (fork {e} , σ) →h ((), σ, e)                               (T1 ; e; T2 , σ) →tp (T1 ; e ; T2 ; ef , σ )



                   Fig. 3. Lambda calculus with references and fork.



3.2    Proof Rules
Before coming to the actual contribution of this section—which is the encoding
of weakest preconditions using our base logic in Sect. 3.3—we give some idea of
how to reason using weakest preconditions by discussing its proof rules. These
proof rules are inspired by [15], but presented in weakest precondition style.
    Given a predicate Φ : Val → Prop, called the postcondition, the connective
wp e {Φ} gives the weakest precondition under which all executions of e are safe,
and all return values v of e satisfy the postcondition Φ(v). For an execution to
be safe, we demand that it does not get stuck, which in the case of our language
means the program must never access invalid locations.
    Figure 4 shows some rules of the wp e {Φ} connective. To reason about state,
we use the well-known points-to assertion → v, which states that we exclusively
own the location , and that it currently stores value v. As part of deﬁning
weakest preconditions, we will also have to deﬁne the points-to assertion.
    As usual in a weakest precondition style system [10], the postcondition of the
conclusion of each rule involves an arbitrary predicate Φ. For example, imagine
                    The Essence of Higher-Order Concurrent Separation Logic            707

we want to prove → v ∗ P wp ( ← w) {Φ}. The rule wp-store tells us what
we have to show about Φ for this to hold:
              P ∗ −→w       Φ()
                                           Wand-intro
                        P     → w −∗ Φ()
                              −
                                                     Sep-mono, -intro
                 → v ∗ P      → v ∗ ( −
                               −        → w −∗ Φ())
                                                     wp-store
                → v ∗ P     wp ( ← w) {Φ}
Here, we use −∗ mono to show that we own the location – this should not be
surprising; in a separation logic, we have to demonstrate ownership of a location
to access it. Furthermore, using our remaining resources P we have to prove
  → w −∗ Φ(). It does not matter what Φ says for values other than (), which
  −
corresponds to the fact that the store expression terminates with ().
    Notice the end-to-end eﬀect of applying this little derivation: we had to show
that we own → v, and it got replaced in our context with → w. However, this
was all expressed in the premise of wp-store (and similarly for the other rules),
with the conclusion applying to an arbitrary postcondition Φ. We could have
equivalently written the rule as −→ v −∗ wp ( ← w) { − → w}, but applying rules
in such a style requires using the rules of framing (wp-frame) and monotonicity
(wp-mono) for every instruction. We thus prefer the style of rules in Fig. 4.

 wp-mono                      wp-frame           wp-val          wp-bind
   ∀v. Φ(v)     Ψ (v)         P ∗ wp e {Φ}        Φ(v)           wp e {v. wp K[ v ] {Φ}}
 wp e {Φ      wp e {Ψ }        wp e {P ∗ Φ}       wp v {Φ}             wp K[ e ] {Φ}

      wp-fork                        wp-λ                    wp-load
        () ∗ wp e {v. True}           wp e[v/x] {Φ}           → v ∗ ( → v −∗ Φ(v))
        wp fork {e} {Φ}              wp (λx.e)v {Φ}                  wp ! {Φ}

                wp-store                              wp-alloc
                 → v ∗ ( → w −∗ Φ())                   (∀   → v −∗ Φ( ))
                    wp ( ← w) {Φ}                         wp ref(v) {Φ}


                          Fig. 4. Rules for weakest preconditions.



Hoare Triples. Traditional Hoare triples can be deﬁned in terms of weakest
preconditions as {P } e {Φ}  (P −∗ wp e {Φ}). The  modality ensures that the
triple asserts no exclusive ownership, and as such, can be used multiple times.


3.3     Definition of Weakest Preconditions

We now discuss how to deﬁne weakest preconditions using the Iris base logic,
proceeding in three stages of increasing complexity.
708     R. Krebbers et al.

First Stage. To get started, let us assume the program we want to verify makes
no use of fork or shared heap access. The idea of wp e {Φ} is to ensure that given
any reduction (e, σ) → · · · → (en , σn ), either (en , σn ) is reducible, or the program
terminated, i.e., en is a value v for which we have Φ(v). The natural candidate
for encoding this is using the ﬁxed-point operator μ x. P of our logic. Consider
the following:

wp e {Φ}  (e ∈ Val ∧ Φ(e))                                         (return value)
           
         ∨ e∈ / Val ∧ ∀σ. red(e, σ)                                 (saf ety)
                                                                                       
              ∧  (∀e2 , σ2 . (e, σ) → (e2 , σ2 , ) −∗ wp e2 {Φ})   (preservation)

Weakest precondition is deﬁned by case-distinction: either the program has
already terminated (e is a value), in which case the postcondition should hold.
Alternatively, the program is not a value, in which case there are two require-
ments. First, for any possible heap σ, the program should be reducible (called
program safety). Second, if the program makes a step, then the weakest precon-
dition of the reduced program e2 must hold (called preservation).
    Note that the recursive occurrence wp e2 {Φ} appears under a -modality, so
the above can indeed be deﬁned using the ﬁxed-point operator μ. In some sense,
this “ties” the steps of the program to the step-indices implicit in the logic, by
adding another  for every program step.
    So, how useful is this deﬁnition? The rules wp-val and wp-λ are almost
trivial, and using Löb induction we can prove wp-mono, wp-frame and wp-
bind. We can thus reason about programs that do not fork or make use of the
heap.
    But unfortunately, this deﬁnition cannot be used to verify programs involving
heap accesses: the states σ and σ2 are universally quantiﬁed and not related to
anything. The program must always be able to proceed under any heap, so we
cannot possibly prove the rules of the load, store and allocation constructs.
    The usual way to proceed in constructing a separation logic is to deﬁne the
pre- and post-conditions as predicates over states, but that is not the direction
we take. After all, our base logic already has a notion of “resources that can be
updated”—i.e., a notion of state—built in to its model of assertions. Of course
we want to make use of this power in building our program logic.


Second Stage: Adding State. We now consider programs that access the
shared heap but still do not fork. To use the resources provided by the Iris base
logic, we have to start by thinking about the right RA. An obvious candidate
                     fin
would be to use Loc − Ex(Val) (which is isomorphic to ﬁnite partial functions
with composition being disjoint union) and deﬁne −    → v as Own([ := ex(v)]).
However, that leaves us with a problem: how do we tie those resources to the
actual heap that the program executes on? We have to make sure that from
owning − → v, we can actually deduce that is allocated in σ.
                   The Essence of Higher-Order Concurrent Separation Logic             709

     To this end, we will actually have two heaps in our resources, both elements of
      fin
Loc − Ex(Val ). The authoritative heap • σ is managed by the weakest precon-
dition, and tied to the physical state occurring in the program reduction. There
will only ever be one authoritative heap resource, i.e., we want • σ · • σ  to be
invalid. At the same time, the heap fragments ◦ σ will be owned by the program
itself and used to give meaning to −     → v. These fragments can be composed the
usual way (◦ σ·◦ σ  = ◦ (σσ  )). Finally, we need to tie these two pieces together,
making sure that the fragments are always a “part” of the authoritative state:
if • σ · ◦ σ  is valid, then σ   σ should hold.
                                                           fin
     This is called the authoritative RA, Auth(Loc − Ex(Val)) [18]. Before
we explain how to deﬁne the authoritative RA, let us see why it is useful
in the deﬁnition of weakest preconditions. The new deﬁnition is (changes are
in red):

   wp e {Φ}  (e ∈ Val ∧ |Φ(e))
              
             ∨ e∈/ Val ∧ ∀σ. Own(• σ) −∗ | red(e, σ)
                                                                                   
                 ∧  (∀e2 , σ2 . (e, σ) → (e2 , σ2 , ) −∗ |Own(• σ2 ) ∗ wp e2 {Φ})
        → v  Own(◦ [ := v])
        −

The diﬀerence from the ﬁrst deﬁnition is that the second disjunct (the one
covering the case of a program that can still reduce) requires proving safety
and preservation under the assumption that the authoritative heap • σ matches
the physical one. Moreover, when the program makes a step to some new
state σ2 , the proof must be able to produce a matching authoritative heap.
Finally, the basic update modality permits the proof to perform frame-preserving
updates.
    To see why this is useful, consider proving wp-load, the weakest precondi-
tion of ! . After picking the right disjunct and introducing all assumptions, we
can combine the assumptions made by the rule, → v, with the assumptions pro-
vided by the deﬁnition of weakest preconditions to obtain Own(• σ · ◦ [ := v]).
By own-valid, we learn that this RA element is valid, which (as discussed
above) implies [ := v]  σ, so σ( ) = v. In other words, because the RA ties
the authoritative heap and the heap fragments together, and because weakest
precondition ties the authoritative heap and the physical heap used in program
reduction together, we can make a connection between → v and the physical
heap.
    Completing the proof of safety and progress now is straightforward. Since all
possible reductions of ! do not change the heap, we can produce the authorita-
tive heap • σ2 by just “forwarding” the one we got earlier in the proof. In this
case, we did not even make use of the fact that we are allowed to perform frame-
preserving updates. This is, however, necessary to prove weakest preconditions
of operations that actually change the state (like allocation or storing), because
in these cases, the authoritative heap needs to be changed likewise.
710       R. Krebbers et al.

Authoritative RA. To complete the deﬁnition, we need to deﬁne the author-
itative RA [18]. We can do so in general (i.e., the deﬁnition is not speciﬁc to
heaps), so assume we are given some uRA M and let:

                 Auth(M )  Ex(M )? × M
                                                                             
                                                               
                             V  {(⊥, b) | b ∈ V} ∪ (ex(a), b)  a ∈ V ∧ b  a)
          (x1 , b1 ) · (x2 , b2 )  (x1 · x2 , b2 · b2 )
                       |(x, b)|  (⊥, |b|)

With a ∈ M , we write • a for (ex(a), ε) to denote authoritative ownership of a
and ◦ a for (⊥, a) to denote fragmentary ownership of a.
    It can be easily veriﬁed that this RA has the three key properties discussed
above: ownership of • a is exclusive, ownership of ◦ a composes like that of a, and
the two are tied together in the sense that validity of • a·◦ b implies b  a. Beyond
this, it turns out that we can show the following frame-preserving updates that
are needed for wp-store and wp-alloc:

                • σ · ◦ [ := v]  • σ[ := w] · ◦ [ := w]
                            • σ  • σ[ := w] · ◦ [ := w]          if     ∈
                                                                         / dom(σ)

Third Stage: Adding Fork. Our previous deﬁnition of wp e {Φ} only talked
about reductions (e, σ) → (e2 , σ2 , ) which do not fork oﬀ threads, and hence
one could not prove wp-fork. This new deﬁnition lifts this limitation:

      wp e {Φ}  (e ∈ Val ∧ |Φ(e))
                 
                ∨ e∈/ Val ∧ ∀σ. Own(• σ) −∗ | red(e, σ)
                   ∧  (∀e2 , σ2 , ef . (e, σ) → (e2 , σ2 , ef ) −∗ |
                                       Own(• σ2 ) ∗ wp e2 {Φ} ∗   ∗               
                                                                                           
                                                                           ef wp e {v.True})
                                                                       e ∈

           → v  Own(◦ [ := v])
           −

Instead of just demanding a proof of the weakest precondition of the thread e
under consideration, we also demand proofs that all the forked-oﬀ threads ef are
safe. We do not care about their return values, so the postcondition is trivial.
    This encoding shows how much mileage we get out of building on top of the
Iris base logic. Because said logic supports ownership and step-indexing, we can
get around explicitly managing resources and step-indices in the weakest pre-
condition deﬁnition. We do not have to explicitly account for the way resources
are subdivided between the current thread and the forked-oﬀ thread. Instead,
all we have to do is surgically place some update modalities, a single , and
some standard separation logic connectives. This keeps the deﬁnition of, and the
reasoning about, weakest preconditions nice and compact.
                   The Essence of Higher-Order Concurrent Separation Logic        711

4     Recovering the Iris Program Logic
In this section, we show how to encode the reasoning principles of full Iris [17,18]
within our base logic. The main remaining challenge is to encode invariants,
which are the key feature for reasoning about sharing in concurrent programs [5].
    An invariant is simply a property that holds at all times: each thread access-
ing the state may assume the invariant holds before each step of its computation,
but it must also ensure that it continues to hold after each step. Since we work in
a separation logic, the invariant does not just “hold”; it expresses ownership of
some resources, and threads accessing the invariant get access to those resources.
The rule that realizes this idea looks as follows:
             wp-inv
              P    wpE\{ι} e {v.  P ∗ Φ(v)}      atomic(e)      ι∈E
                                      ι
                                  P       wpE e {Φ}
This rule is quite a mouthful, so we will go over it carefully. First of all, there is
a new assertion P ι , which states that P (an arbitrary assertion) is maintained
as an invariant. The rule says that having this assertion in the context permits
us to access the invariant, which involves acquiring ownership of  P before the
veriﬁcation of e and giving back ownership of  P after said veriﬁcation. Cru-
cially, we require that e is atomic, meaning that computation is guaranteed to
complete in a single step. This is essential for soundness: the rule allows us to
temporarily use and even break the invariant, but after a single atomic step (i.e.,
before any other thread could take a turn), we have to establish it again.
     The  modality arises because of the inherently cyclic nature (i.e., impred-
icativity) of our invariants: P can be any assertion, including assertions about
invariants. We will show in Sect. 5 that removing the  leads to an unsound logic.
     Finally, we come to the mask E and invariant name ι: they avoid the issue of
reentrancy. We have to make sure that the same invariant is not accessed twice
at the same time, as that would incorrectly duplicate the underlying resource.
To this end, each invariant has a name ι identifying it. Furthermore, weakest
preconditions are annotated with a mask to keep track of which invariants are
still enabled. Accessing an invariant removes its name from the mask, ensuring
that it cannot be accessed again in a nested fashion.
     In order to recover the full power of the Iris program logic (including wp-
inv), we start this section by lifting a limitation of the base logic, namely, that
it is restricted to a single uRA of resources (Sect. 4.1). Then we explain how
resources are used to keep track of invariants (Sect. 4.2), and deﬁne world satis-
faction, a protocol enforcing how invariants are maintained (Sect. 4.3). We follow
on by deﬁning the fancy update modality, which supports accessing invariants
(Sect. 4.4), before ﬁnally giving an enriched version of weakest preconditions that
validates wp-inv (Sect. 4.5).

4.1   Dynamic Composable Resources
The base logic as described in Sect. 2 is limited to resources formed by a single
RA. However, for the construction in this section, we will need multiple RAs,
712    R. Krebbers et al.

so we need to ﬁnd a way to lift this limitation. Furthermore, we frequently need
to use not just a single instance of an RA, but multiple, entirely independent
instances (e.g., one instance of the RA per instance of a data structure).
    As prior work already observed [17,18], it turns out that RAs themselves
are already ﬂexible enough to solve this, we just have to pick the right RA.
Concretely, assume we are given a family of RAs (Mi )i∈I indexed by some ﬁnite
index set I. Then, we instantiate our base logic with the following global resource
algebra:
                                       fin
                                M       N − Mi
                                        i∈I

First of all, we use a ﬁnite partial function to obtain an arbitrary number of
instances of any of the given RAs. Furthermore, we take the product over the
entire family to make all the chosen RAs available inside the logic.
    Typically, we will only own some resource a in one particular instance named
γ ∈ N of a given RA Mi . To express that, we introduce the following notation:

                    a : Mi γ  Own((. . . , ∅, i : [γ := a], ∅, . . .))

Often, we will even leave away the Mi because it is clear from context.
   All the rules about Own(·) can now also be derived for · · . In addition, we
obtain a rule to create new instances of RAs with an arbitrary valid initial state:

                             a ∈ VMi      |∃γ. a : Mi γ


Obtaining Modular Proofs. Even with multiple RAs at our disposal, it may
still seem like we have a modularity problem: every proof is done in an instanti-
ation of Iris with some particular family of RAs. As a result, if two proofs make
diﬀerent choices about the RAs, they are carried out in entirely diﬀerent logics
and hence cannot be composed.
     To solve this problem, we generalize our proofs over the family of RAs that
Iris is instantiated with. So in the following, all proofs are carried out in Iris
instantiated with some unknown (Mi )i∈I . If the proof needs a particular RA, it
further assumes that there exists some j s.t. Mj is the desired RA. Composing
two proofs is thus easily possible; the resulting proof works in any family of RAs
that contains all the particular RAs needed by either proof. Finally, if we want
to obtain a “closed form” of some particular proof in a concrete instance of Iris,
we simply construct a family of RAs that contains everything the proof needs.


4.2   A Registry of Invariants

Since we wish to be able to share the P ι assertion among threads, we will need
a central “invariant registry” that keeps track of all invariants and witnesses the
fact that P has been registered as invariant.
                    The Essence of Higher-Order Concurrent Separation Logic                   713

    In Sect. 3.3, we already saw the authoritative resource algebra. This RA
allowed us to have an “authoritative” registry with fragments shared by various
parties. However, for the case of invariants, we are not interested in expressing
exclusive ownership of invariants, like we did for heap locations. Instead, the
entire point of invariants is sharing, so we need that everybody agrees on what
the invariant with a given name is. An RA for agreement on a set X is deﬁned
by:

           Ag(X)  ag(x : X) |                                         V  {ag(x) | x ∈ X}
                      ⎧
                      ⎨ag(x) if x = y
      ag(x) · ag(y)                                           |ag(x)|  ag(x)
                      ⎩     otherwise

The key property of this RA is that from ag(x)·ag(y) ∈ V, we can deduce x = y.
  We can then compose our RAs as follows to obtain an “invariant registry”:
                                                 fin
                              inv  Auth(N − Ag(Prop))

This construction is an example of higher-order ghost state, which we already
mentioned in Sect. 2.6. The Prop here is actually a recursive occurrence of logical
assertions within resources, which has to be guarded by a “type-level later” .
Furthermore, to make this really work, the agreement RA must be generalized
to a proper CMRA (Sect. 2.6), so the actual deﬁnition is more involved. See the
Iris 2.0 paper for details [17].
    For present purposes, the only relevant outcome is the following assertions:
– ◦ [ι := P ] γ , stating that P is registered as an invariant with name ι; and
                                  fin
– • I γ , stating that I ∈ N − Prop is the full map of all registered invariants.
These assertions enjoy the following three rules:


           ◦ [ι := P ] γinv     ◦ [ι := P ]
                                               γinv
                                                                               (invreg-persist)
• I γinv ∗ ◦ [ι := P ] γinv     I(ι) ⇔  P                                     (invreg-agree)
                       γinv                      γinv                   γinv
  ι∈
   / dom(I) ∧ • I              | • I[ι := P ]          ∗ ◦ [ι := P ]            (invreg-alloc)

Intuitively, invreg-persist states that the non-authoritative fragment is persis-
tent, i.e., that it can be freely moved below the  modality and shared. invreg-
agree witnesses that the registry and the fragments agree on the proposition
managed at a particular name. Note that we only get the equivalence with a 
because the deﬁnition of the RA (inv) contains a . Finally, invreg-alloc lets
one create a new invariant, provided the new name is not already used.

4.3    World Satisfaction
To recover the invariant mechanism of Iris, we need to attach a meaning to
the invariant registry from Sect. 4.2, in the sense that we must make sure that
714      R. Krebbers et al.

the invariants actually hold ! We do this by deﬁning a single global invariant
called world satisfaction, which enforces the meaning of the invariant registry.
World satisfaction itself will be enforced by threading it through the weakest
preconditions.
    Naively, we may think that world satisfaction always requires all invariants
to hold. However, this does not work: after all, threads are allowed to temporarily
break invariants for an atomic “instant” during program execution. To support
this, world satisfaction keeps invariants in one of two states: either they are
enabled (currently enforced), or they are disabled (currently broken by some
thread). The deﬁnition of the weakest precondition connective will then ensure
that invariants are never disabled for more than an atomic period of time. That
is, no invariant is left disabled between physical computation steps.
    The protocol for opening (i.e., disabling) and closing (i.e., re-enabling) an
invariant employs two exclusive tokens: an enabled token, which witnesses that
the invariant is currently enabled and giving the right to disable it; and dually,
a disabled token. These tokens are controlled by the following two simple RAs:

                     En  ℘(N)                        Dis  ℘fin (N)

The composition for both RAs is disjoint union.2
   We can now give the actual deﬁnition of world satisfaction, W . To this end,
we need instances of Inv, En and Dis, which we assume to have names γInv ,
γEn and γDis , respectively:

            W  ∃I. • I γinv ∗      ∗ι∈dom(I)    ( I(ι) ∗ {ι} γDis ) ∨ {ι} γEn
           P ι  ◦ [ι := P ] γinv

World satisfaction controls the authoritative registry I of all existing invariants.
This allows it to maintain an additional assertion for every single one of them,
namely: either the invariant is enabled and maintained—in which case world
satisfaction actually owns  I(ι)—or the invariant is disabled. Unsurprisingly,
 P ι just means that the registry maps ι to P —but ι may or may not be enabled.
    With this encoding, we can prove the following key properties modeling the
allocation, opening, and closing of invariants:
    wsat-alloc
              E is inﬁnite
                                         wsat-openclose
    W ∗  P −∗ | W ∗ ∃ι ∈ E. P ι          P ι     W ∗ {ι} γEn ⇔ W ∗  P ∗ {ι} γDis

Let us look at the proof of the direction P ι W ∗ {ι} γEn ⇒ W ∗ P ∗ {ι} γDis of
wsat-openclose in slightly more detail. We start by using invreg-agree to
learn that the authoritative registry I maintained by world satisfaction contains
our invariant P at index ι. We thus obtain from the big separating conjunction
that  P ∗ {ι} γDis ∨ {ι} γEn . Since we moreover own the enabled token {ι} γEn ,
we can exclude the right disjunct and deduce that the invariant is currently
2
    Implicitly, they also have an invalid element , for composition of overlapping sets.
                    The Essence of Higher-Order Concurrent Separation Logic       715

enabled. So we take out the  P and the disabled token, and instead put the
enabled token into W , disabling the invariant. This concludes the proof.
    The proof of wsat-alloc is slightly more subtle. In particular, we have to
be careful in picking the new invariant name such that: (a) it is in E, (b) it is
not used in I yet, and (c) we can create a disabled token for that name and put
it into W alongside  P . Since disabled tokens are modeled by ﬁnite sets, only
ﬁnitely many of them can ever be allocated, so it is always possible to pick an
appropriate fresh name.

4.4      Fancy Update Modality
Before we will prove the rules for invariants, there is actually one other piece of
the original Iris logic we should cover: view shifts. View shifts serve three roles:
1. They permit frame-preserving updates (like the basic update modality does).
2. They allow one to access invariants. The mask E deﬁnes which invariants are
   available.
3. They allow one to strip away the  modality from timeless assertions (like
   the modality does, see Sect. 2.7).
   The view shifts of the original Iris were of the form P E1 E2 Q where P is the
precondition, Q the postcondition, and E1 and E2 are invariant masks. For the
same reason that we prefer weakest preconditions over Hoare triples (Sect. 3),
we will present view shifts as a modality instead of a binary connective. The
                                              E    E
modality, called the fancy update modality 1 | 2 , is deﬁned as follows:
   E1     E                                                               E   E
        | 2 P  W ∗ E1 γEn −∗ | (W ∗ E2 γEn ∗ P )             |E P  | P


    In the same way that Hoare triples are deﬁned in terms of weakest precon-
ditions, the binary view shift can be deﬁned in terms of the modality.
                         E    E
    The intuition behind 1 | 2 P is to express ownership of resources such that,
if we further assume that the invariants in E1 are enabled, we can perform a
frame-preserving update to the resources and the invariants, and we end up
owning P and the invariants in E2 are enabled. By looking at the deﬁnition, we
can see how it supports all the fancy features formerly handled by view shifts:
1. At the heart of the fancy update modality is a basic update modality, which
   permits doing frame-preserving updates (see the rule fup-upd in Fig. 5).
2. The modality “threads through” world satisfaction, in the sense that a proof
      E    E
   of 1 | 2 P can use W , but also has to prove it again. Furthermore, con-
   trolled by the two masks E1 and E2 , the modality provides and takes away
   enabled tokens. The ﬁrst mask controls which invariants are available to the
   modality, while the second mask controls which invariants remain available
   after (see inv-open). Furthermore, it is possible to allocate new invariants
   (inv-alloc).
3. Finally, the modality is able to remove laters from timeless assertions by
   incorporating the “except 0” modality (see Sect. 2.7 and fup-timeless).
716          R. Krebbers et al.

   fup-mono                                      fup-intro-mask
        P Q                                            E2 ⊆ E 1                           fup-trans
      E1
           | E2 P    E1    E2
                                Q                P     E1       E2 E2
                                                                        | E1 P            E1
                                                                                             | E2 E 2 | E3 P    E1   E3
                                                                                                                          P

                                                                                                      fup-timeless
       fup-frame                                                            fup-upd                   timeless(P )
       Q ∗ E1 | E 2 P        E1     f       E2    f
                                                      Q∗P                   | P     EP                          EP

                          inv-alloc                                 inv-open
inv-persist                    E is inﬁnite                                                     ι∈E
   ι        ι                                               ι               ι     E   E\{ι}
 P       P                              E   ∃ι ∈ E. P                   P                        ∗(       −∗ E\{ι}| E True)


                    Fig. 5. Rules for the fancy update modality and invariants.


    Ignoring the style of presentation as a modality, there are some diﬀerences
here from view shifts in previous versions of Iris. Firstly, in previous versions,
the rule fup-trans had a side condition restricting the masks it could be
instantiated with, whereas now it does not. Secondly, in previous versions,
instead of fup-intro-mask, only mask-invariant view shifts could be introduced
(P    |E P ). The reason we can now support fup-intro-mask is that masks
are actually just sugar for owning or providing particular resources (namely,
the enabled tokens). This is in contrast to previous versions of Iris, where masks
were entirely separate from resources and treated in a rather ad-hoc manner. Our
more principled treatment of masks signiﬁcantly simpliﬁes building abstractions
involving invariants; however, for lack of space, we cannot further discuss these
abstractions.
    The rules fup-mono, fup-trans, and fup-frame correspond to the related
rules of the basic update modality in Fig. 1. The rule inv-open may look fairly
cryptic; we will see in the next section how it can be used to derive wp-inv.

4.5        Weakest Preconditions
We will now deﬁne weakest preconditions that support not only the rules in
Fig. 4, but also the ones in Fig. 6. We will also show how, from wp-atomic and
inv-open, we can derive the rule motivating this entire section, wp-inv.

                                                                   wp-atomic
                                                                                              atomic(e)
 wp-vup                                                            E1       E2
 | E wpE e v. | E Φ(v)                  wpE e {Φ}                       |        wpE2 e v. E2 | E1 Φ(v)        wpE1 e {Φ}


                    Fig. 6. New rules for weakest precondition with invariants.


   Compared to the deﬁnition developed in Sect. 3, there are two key diﬀer-
ences: ﬁrst of all, we use the fancy update modality instead of the basic update
                  The Essence of Higher-Order Concurrent Separation Logic          717

modality. Secondly, we do not want to tie the deﬁnition of weakest precondi-
tions to a particular language, and instead operate generically over any notion
of expressions and state, and any reduction relation.
    As a consequence of this generality, we can no longer assume that our physical
state is a heap of values with disjoint union as composition. Therefore, instead
of using the authoritative heap deﬁned in Sect. 3.3, we parameterize weakest
preconditions by a predicate I : State → iProp called the state interpretation. In
                  fin
case State = Loc − Val, we can recover the deﬁnition and rules from Sect. 3.3
by taking:

                         I(σ)  • σ : Loc − Ex(Val) γ
                                             fin


More sophisticated forms of separation like fractional permissions [7,8] can be
encoded by using an appropriate RA and deﬁning I accordingly.
    Given an I : State → iProp, our deﬁnition of weakest precondition looks as
follows (changes from Sect. 3 are colored red):

      wpE e {Φ}  (e ∈ Val ∧ |E Φ(e))
                                       E ∅
                 ∨ e∈/ Val ∧ ∀σ. I(σ) −∗ | red(e, σ)
                                                                 ∅   E
                     ∧  (∀e2 σ2 ef . (e, σ) → (e2 , σ2 , ef ) −∗ |
                              I(σ2 ) ∗ wpE e2 {Φ} ∗   ∗               
                                                                               
                                                              ef wp e {v.True})
                                                          e ∈

The mask E of wpE e {Φ} is used for the “outside” of the fancy update modal-
ities, providing them with access to these invariants. The “inner” masks are ∅,
indicating that the reasoning about safety and progress can temporarily open
all invariants (and none have to be left enabled). The forked-oﬀ threads ef have
access to the full mask  as they will only start running in the next instruction,
so they are not constrained by whatever invariants are available right now. Note
that the deﬁnition requires all invariants in E to be enabled again after every
physical step: this corresponds to the fact that an invariant can only be opened
atomically.
    In addition to the rules already presented in Sect. 3, this version of the weak-
est precondition connective lets us prove (among others) the new rules in Fig. 6.
wp-vup witnesses that the entire connective as well as its postcondition are liv-
ing below the fancy update modality, so we can freely add/remove that modality.
    Finally, we come to wp-atomic to open an invariant around an atomic
expression. The rule is similar to wp-vup, with the key diﬀerence being that
it can change the mask. On the left hand side of the turnstile, we are allowed to
ﬁrst open some invariants, then reason about e, and then close invariants again.
This is sound because e is atomic. wp-atomic is the rule we need to derive
wp-inv:
718     R. Krebbers et al.

                                   P  wpE\{ι} e {v.  P ∗ Φ(v)}
                                                                       wp-frame
                      E\{ι}   E
       P ∗ ( P −∗    | True)                            
            wpE\{ι} e v.  P ∗ Φ(v) ∗ ( P −∗ E\{ι}|E1 True)
                                                                wp-mono
       P ∗ ( P −∗ E\{ι}|E True)  wpE\{ι} e v. E\{ι}|E Φ(v)
                                                                        inv-open
                              P ι  E |E\{ι} wpE\{ι} e x. E\{ι}|E Φ(v)
                                                                          wp-atomic
                              P ι  wpE e {Φ}


4.6   Adequacy
To demonstrate that wp e {φ} actually makes the expected statements about
program executions, we prove the following adequacy theorem.

Theorem 4.1 (Adequacy of weakest preconditions). Let φ be a ﬁrst-order
predicate. If True | I(σ) ∗ wp e {φ} and (e, σ) →∗tp (e1 . . . en , σ  ), then:

1. For any ei we have that either ei is a value, or red(ei , σ  );
2. If e1 (the main thread) is a value v, then φ(v).

   The proof of this theorem relies on Theorem 2.1 (in Sect. 2.8). We also impose
the same restrictions on φ as we have done there: φ has to be a ﬁrst-order
predicate. This ensures we can use φ both inside our logic and at the meta level.


5     Paradoxes Involving the “later” Modality
A recurring element of concurrent separation logics with impredicative invari-
ants [17,18,28] is the later modality , which is used to guard resources when
opening invariants. The use of  has heretofore been forced by the models which
were used to show soundness of these logics. It has been an open question, how-
ever, whether the need for the later modality is a mere artifact of the model, or
whether it is in some sense required. In this section, we show that at the very
least it plays an essential role: if we omit the later modality from the invariant
opening rule, then we can derive a contradiction in the logic.

Theorem 5.1. Assume we add the following proof rule to Iris:


                                                ι∈E
                              ι   E    E\{ι}               E\{ι}   E
                         P            |       P ∗ (P −∗       | True)

Then, if we pick an appropriate RA, True               | False.

Notice that the above rule is the same as inv-open in Fig. 5, except that it does
not add a  in front of P .
                   The Essence of Higher-Order Concurrent Separation Logic             719

    Of course, this does not prove that we absolutely must have a  modality,
but it does show that the stronger rule one would prefer to have for invariants
is unsound. Step-indexing is but one way to navigate around this unsoundness.
However, we are not aware of another technique that would yield a logic with
comparably powerful impredicative invariants.
    The proof of this theorem does not use the fact that fancy updates are deﬁned
in a particular way in terms of basic updates, but just uses the proof rules for this
modality. The proof also makes no use of higher-order ghost state. In fact, the
result holds for all versions of Iris [17,18], as is shown by the following theorem:


Theorem 5.2. Assume a higher-order separation logic with  and an update
modality with a binary mask |{0,1} (think: empty mask and full mask) satisfying
strong monad rules with respect to separating conjunction and such that:

                                       weaken-mask
                                       |0 P     |1 P


Assume a type I and an assertion · · : I → Prop → Prop satisfying:

                                                            inv-open-nolater
       inv-alloc                 inv-persist                P ∗Q       |0 (P ∗ R)
                        ι               ι          ι              ι
       P    |1 ∃ι. P              P         P               P       ∗Q     |1 R


Finally, assume the existence of a type G and two tokens s · : G → Prop and
f · : G → Prop parameterized by G and satisfying the following properties:

start-alloc         start-finish            start-not-finished         finished-dup
   |0 ∃γ. s γ      s γ     |0 f γ            s γ∗ f γ   False            f γ   f γ∗ f γ


Then True    |1 False.
    In other words, the theorem requires three ingredients to be present in the
logic in order to derive a contradiction:
– An update modality that satisﬁes the laws of Iris’s basic update modality
  (Fig. 1). The modality needs a mask for the same reason that Iris’s fancy
  update modality has a mask: to prevent opening the same invariant twice.
– Invariants that can be opened around the update modality, and that can be
  opened without a later.
– A two-state protocol whose only transition is from the ﬁrst to the last state.
  This is what s · and f · encode. The proof does not actually depend on how
  that protocol is made available to the logic. For example, to apply this proof to
  iCAP [28], one could use iCAP’s built-in support for state-transition systems
720      R. Krebbers et al.

    to achieve the same result. However, for the purpose of the theorem, we had to
    pick some way of expressing protocols. We picked the token-based approach
    common in Iris.
All versions of Iris easily satisfy the ﬁrst and third of these requirements, by
using fancy updates (Iris 3) or primitive view shifts (Iris 1 and 2) for the update
modality, and by constructing an appropriate RA (Iris 2 and 3) or PCM (Iris 1)
for the two-state protocol. Of course, inv-open-nolater is the one assumption
of the theorem that no version of Iris satisﬁes, which is the entire point.
    Unsurprisingly, the proof works by constructing an assertion that is equiv-
alent (in some rather loose sense) to its own negation. The full details of this
construction are spelled out in the appendix [1].

6     Related Work
Since O’Hearn introduced the original concurrent separation logic (CSL) [24],
many more CSLs have been developed [9,11,12,14,16–18,27–30]. Though these
logics have explored diﬀerent techniques for reasoning about concurrency, they
have one thing in common: their proof rules and models are complicated.
     There have been attempts at mitigating the diﬃculty of the models of these
logics. Most notably, Svendsen and Birkedal [28] deﬁned the model of the iCAP
logic in the internal logic of the topos of trees, which includes a later connective
to reason about step-indexing abstractly. However, their model of Hoare triples
still involves explicit resource management, which ours does not.
     On the other end of the spectrum, there has been work on encoding binary
logical relations in a concurrent separation logic [13,21,22,30]. These encodings
are relying on a base logic that already includes a plethora of high-level concepts,
such as weakest preconditions and view shifts. Our goal, in contrast, is precisely
to deﬁne these concepts in simpler terms.
     FCSL [27] takes an opposite approach to our work. To ease reasoning about
programs in a proof assistant, they avoid reasoning in separation logic as much
as possible, and reason mostly in the model of their logic. This requires the
model to stay as simple as possible; in particular, FCSL does not make use of
step-indexing. As a consequence, they do not support impredicative invariants,
which we believe are an important feature of Iris. For example, they are needed
to model impredicative type systems [21] or to model a reentrant event loop
library [28]. Furthermore, as we have shown in recent work [21], one can actually
reason conveniently in a separation logic in Coq, so the additional complexity of
our model is hardly visible to users of our logic.
     Additionally, there is a diﬀerence in expressiveness w.r.t. “hiding” of invari-
ants. FCSL supports a certain kind of hiding, namely the ability to transfer some
local state into an invariant (actually a “concurroid”), which is enforced during
the execution of a single expression e, but after which the state governed by the
invariant is returned to local control. Iris can support such hiding as well, via
an encoding of what we call “cancelable invariants” [1]. Additionally, we allow
a diﬀerent kind of hiding, namely the ability to hide invariants used by (nested)
                  The Essence of Higher-Order Concurrent Separation Logic        721

Hoare-triple speciﬁcations. For example, a higher-order function f may return
another function g, whose Hoare-triple speciﬁcation is only correct under some
invariant I (which was established during execution of f ). Since invariants in Iris
are persistent assertions, I can be hidden, i.e., it need not infect the speciﬁcation
of f or g. To our knowledge, FCSL does not support hiding of this form.
    The Veriﬁed Software Toolchain (VST) [4] is a framework that provides
machinery for constructing sophisticated higher-order separation logics with sup-
port for impredicative invariants in Coq. However, VST is not a logic and, as
such, does not abstract over step-indices and resources the way working in a logic
like Iris 3.0 does. Deﬁning a program logic in VST thus still requires signiﬁcant
manual management of such details, which are abstracted away when deﬁning
a program logic in the Iris base logic. Furthermore, VST has so far only been
demonstrated in the context of sequential reasoning and coarse-grained (lock-
based) concurrency [6], whereas the focus of Iris is on ﬁne-grained concurrency.


7   Conclusion

We have presented a minimal base logic in which we can deﬁne concurrent sepa-
ration logics in a concise and abstract way. This has the beneﬁt of making higher-
level concepts (like weakest preconditions) easier to deﬁne, easier to understand,
and easier to reason about.
    Deﬁnitions become simpler as they can be performed at a much higher level of
abstraction. In particular, the deﬁnitions of logical connectives such as the fancy
update modality and weakest preconditions do not have to deal with any details
about disjointness of resources or step-indexing—this is all abstractly handled
by the base logic. Proofs become simpler since only the rules of the primitive
connectives of the base logic have to be veriﬁed w.r.t. the model. The proofs
about fancier connectives are carried out inside the logic, again abstracting over
details that have to be managed manually when working in the model.
    Thanks to these simpliﬁcations, we are able now, for the ﬁrst time, to explain
what the program logic connectives in Iris actually mean. Furthermore, we have
ported the Coq formalization of Iris [1], including a rich body of examples, over
to the new connectives deﬁned in the base logic. The interactive proof mode
(IPM) [21] provided crucial tactic support for reasoning with interesting combi-
nations of separation-logic assertions and our modalities (as they arise, e.g., in
weakest preconditions). In performing the port, the deﬁnitions and proofs related
to weakest preconditions, view shifts, and invariants shrank in size signiﬁcantly,
indicating that proofs and deﬁnitions can now be carried out with considerably
greater ease.

Acknowledgments. This research was supported in part by a European Research
Council (ERC) Consolidator Grant for the project “RustBelt”, funded under the Euro-
pean Union’s Horizon 2020 Framework Programme (grant agreement no. 683289); and
by the ModuRes Sapere Aude Advanced Grant from The Danish Council for Indepen-
dent Research for the Natural Sciences (FNU).
722     R. Krebbers et al.

References
 1. The Iris 3.0 documentation and Coq development. Available on the Iris project
    website at: http://iris-project.org
 2. Appel, A., McAllester, D.: An indexed model of recursive types for foundational
    proof-carrying code. TOPLAS 23(5), 657–683 (2001)
 3. Appel, A., Melliès, P.-A., Richards, C., Vouillon, J.: A very modal model of a
    modern, major, general type system. In: POPL (2007)
 4. Appel, A.W. (ed.): Program Logics for Certiﬁed Compilers. Cambridge University
    Press, Cambridge (2014)
 5. Ashcroft, E.A.: Proving assertions about parallel programs. JCSS 10(1), 110–135
    (1975)
 6. Beringer, L., Stewart, G., Dockins, R., Appel, A.W.: Veriﬁed compilation for
    shared-memory C. In: Shao, Z. (ed.) ESOP 2014. LNCS, vol. 8410, pp. 107–127.
    Springer, Heidelberg (2014). doi:10.1007/978-3-642-54833-8 7
 7. Bornat, R., Calcagno, C., O’Hearn, P.W., Parkinson, M.J.: Permission accounting
    in separation logic. In: POPL, pp. 259–270 (2005)
 8. Boyland, J.: Checking interference with fractional permissions. In: Cousot, R. (ed.)
    SAS 2003. LNCS, vol. 2694, pp. 55–72. Springer, Heidelberg (2003). doi:10.1007/
    3-540-44898-5 4
 9. Rocha Pinto, P., Dinsdale-Young, T., Gardner, P.: TaDA: a logic for time and
    data abstraction. In: Jones, R. (ed.) ECOOP 2014. LNCS, vol. 8586, pp. 207–231.
    Springer, Heidelberg (2014). doi:10.1007/978-3-662-44202-9 9
10. Dijkstra, E.W.: Guarded commands, nondeterminacy and formal derivation of pro-
    grams. CACM 18(8), 453–457 (1975)
11. Dinsdale-Young, T., Dodds, M., Gardner, P., Parkinson, M.J., Vafeiadis, V.: Con-
    current abstract predicates. In: D’Hondt, T. (ed.) ECOOP 2010. LNCS, vol. 6183,
    pp. 504–528. Springer, Heidelberg (2010). doi:10.1007/978-3-642-14107-2 24
12. Dodds, M., Feng, X., Parkinson, M., Vafeiadis, V.: Deny-guarantee reasoning. In:
    Castagna, G. (ed.) ESOP 2009. LNCS, vol. 5502, pp. 363–377. Springer, Heidelberg
    (2009). doi:10.1007/978-3-642-00590-9 26
13. Dreyer, D., Neis, G., Rossberg, A., Birkedal, L.: A relational modal logic for higher-
    order stateful ADTs. In: POPL (2010)
14. Hobor, A., Appel, A.W., Nardelli, F.Z.: Oracle semantics for concurrent separa-
    tion logic. In: Drossopoulou, S. (ed.) ESOP 2008. LNCS, vol. 4960, pp. 353–367.
    Springer, Heidelberg (2008). doi:10.1007/978-3-540-78739-6 27
15. Ishtiaq, S.S., O’Hearn, P.W.: BI as an assertion language for mutable data struc-
    tures. In: POPL, pp. 14–26 (2001)
16. Jacobs, B., Piessens, F.: Expressive modular ﬁne-grained concurrency speciﬁcation.
    In: POPL (2011)
17. Jung, R., Krebbers, R., Birkedal, L., Dreyer, D.: Higher-order ghost state. In:
    ICFP, pp. 256–269 (2016)
18. Jung, R., Swasey, D., Sieczkowski, F., Svendsen, K., Turon, A., Birkedal, L.,
    Dreyer, D.: Iris: Monoids and invariants as an orthogonal basis for concurrent
    reasoning. In: POPL, pp. 637–650 (2015)
19. Kock, A.: Monads on symmetric monoidal closed categories. Arch. Math. 21(1),
    1–10 (1970)
20. Kock, A.: Strong functors and monoidal monads. Arch. Math. 23(1), 113–120
    (1972)
                   The Essence of Higher-Order Concurrent Separation Logic        723

21. Krebbers, R., Timany, A., Birkedal, L.: Interactive proofs in higher-order concur-
    rent separation logic. In: POPL, pp. 205–217 (2017)
22. Krogh-Jespersen, M., Svendsen, K., Birkedal, L.: A relational model of types-and-
    eﬀects in higher-order concurrent separation logic. In: POPL (2017)
23. Nakano, H.: A modality for recursion. In: LICS (2000)
24. O’Hearn, P.: Resources, concurrency, and local reasoning. TCS 375(1), 271–307
    (2007)
25. O’Hearn, P.W., Pym, D.J.: The logic of bunched implications. Bull. Symb. Logic
    5(2), 215–244 (1999)
26. Parkinson, M.: The next 700 separation logics. In: Leavens, G.T., O’Hearn, P.,
    Rajamani, S.K. (eds.) VSTTE 2010. LNCS, vol. 6217, pp. 169–182. Springer, Hei-
    delberg (2010). doi:10.1007/978-3-642-15057-9 12
27. Sergey, I., Nanevski, A., Banerjee, A.: Mechanized veriﬁcation of ﬁne-grained con-
    current programs. In: PLDI, pp. 77–87 (2015)
28. Svendsen, K., Birkedal, L.: Impredicative concurrent abstract predicates. In:
    Shao, Z. (ed.) ESOP 2014. LNCS, vol. 8410, pp. 149–168. Springer, Heidelberg
    (2014). doi:10.1007/978-3-642-54833-8 9
29. Svendsen, K., Birkedal, L., Parkinson, M.: Modular reasoning about separa-
    tion of concurrent data structures. In: Felleisen, M., Gardner, P. (eds.) ESOP
    2013. LNCS, vol. 7792, pp. 169–188. Springer, Heidelberg (2013). doi:10.1007/
    978-3-642-37036-6 11
30. Turon, A., Dreyer, D., Birkedal, L.: Unifying reﬁnement and Hoare-style reasoning
    in a logic for higher-order concurrency. In: ICFP, pp. 377–390 (2013)
