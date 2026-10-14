                                         Coinductive Proofs for Temporal Hyperliveness
                                         ARTHUR CORRENSON, CISPA Helmholtz Center for Information Security, Germany
                                         BERND FINKBEINER, CISPA Helmholtz Center for Information Security, Germany
arXiv:2501.07920v1 [cs.PL] 14 Jan 2025




                                         Temporal logics for hyperproperties have recently emerged as an expressive speciﬁcation technique for re-
                                         lational properties of reactive systems. While the model checking problem for such logics has been widely
                                         studied, there is a scarcity of deductive proof systems for temporal hyperproperties. In particular, hyper-
                                         properties with an alternation of universal and existential quantiﬁcation over system executions are rarely
                                         supported. In this paper, we focus on hyperproperties of the form ∀∗ ∃∗𝜓 , where 𝜓 is a safety relation. We show
                                         that hyperproperties of this class – which includes many hyperliveness properties of interest – can always be
                                         approximated by coinductive relations. This enables intuitive proofs by coinduction. Based on this observa-
                                         tion, we deﬁne HyCo (Hyperproperties, Coinductively), a mechanized framework to reason about temporal
                                         hyperproperties within the Coq proof assistant. We detail the construction of HyCo, provide a proof of its
                                         soundness, and exemplify its use by applying it to the veriﬁcation of reactive systems modeled as imperative
                                         programs with nondeterminism and I/O.
                                         CCS Concepts: • Theory of computation → Modal and temporal logics; Program veriﬁcation; Logic and
                                         veriﬁcation.
                                         Additional Key Words and Phrases: Coinduction, Temporal Hyperproperties, Coq
                                         ACM Reference Format:
                                         Arthur Correnson and Bernd Finkbeiner. 2025. Coinductive Proofs for Temporal Hyperliveness. Proc. ACM
                                         Program. Lang. 9, POPL, Article 53 (January 2025), 29 pages. https://doi.org/10.1145/3704889

                                         1   Introduction
                                         Temporal logics for hyperproperties like HyperLTL [16] combine temporal reasoning over inﬁnite
                                         executions with the ability to quantify universally and existentially over multiple executions. Such
                                         logics are ideally suited to verify reactive systems, where the continuous interaction of the system
                                         with its environment results in an inﬁnite sequence of events. In this context, temporal logics
                                         for hyperproperties enable the speciﬁcation of information-ﬂow security policies as well as other
                                         relational properties like robustness, knowledge, and causality. For example, the information-ﬂow
                                         policy of noninference [32] requires that an observer of a system should not be able to observe
                                         any diﬀerence in the behavior of the system if we replace its high-security inputs by a dummy
                                         value 𝜆. Thus, from the point of view of a potential attacker, sensitive data manipulated by the
                                         system are indistinguishable from 𝜆. Expressing this requirement formally requires quantiﬁcation
                                         over several executions of the system. In HyperLTL, noninference is expressed as the formula
                                                                                  ∀𝜏1 ∃𝜏2     (ℎ𝑖𝜏2 = 𝜆 ∧ 𝑙𝑜𝜏1 = 𝑙𝑜𝜏2 )
                                         where ℎ𝑖 denotes the high-security inputs and 𝑙𝑜 the low-security outputs of the system. This
                                         formula requires for every execution the existence of another execution where the high-security
                                         Authors’ Contact Information: Arthur Correnson, CISPA Helmholtz Center for Information Security, Saarbruecken, Ger-
                                         many, arthur.correnson@cispa.de; Bernd Finkbeiner, CISPA Helmholtz Center for Information Security, Saarbruecken, Ger-
                                         many, ﬁnkbeiner@cispa.de.

                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for proﬁt or commercial advantage and that copies bear this notice and
                                         the full citation on the ﬁrst page. Copyrights for third-party components of this work must be honored. For all other uses,
                                         contact the owner/author(s).
                                         © 2025 Copyright held by the owner/author(s).
                                         ACM 2475-1421/2025/1-ART53
                                         https://doi.org/10.1145/3704889


                                                                          Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:2                                                                           Arthur Correnson and Bernd Finkbeiner


inputs to the system are replaced by a dummy value 𝜆 and yet the low-security outputs remain
the same. Noninference is an example of hyperliveness property [17].
   There has been a lot of recent research on ﬁnite-state and abstraction-based model checking for
temporal hyperproperities [10, 12, 13, 26, 28]. Somewhat surprisingly, however, there is a scarcity
of deductive proof systems supporting logics like HyperLTL. In particular, contrary to more tra-
ditional Hoare-style program logics, there exists, to the best of our knowledge, no mechanized
framework to reason about temporal hyperproperties within a proof assistant. This is unfortu-
nate, because the automated approaches are still very limited in their scalability; the veriﬁcation
of realistic systems appears far out of reach.
   A fragment that is often supported by deductive approaches is the special case of 𝑘-hypersafety [2,
24, 25, 37], where all executions are quantiﬁed universally. This case is attractive, because the ver-
iﬁcation of a 𝑘-hypersafety property can be reduced to the veriﬁcation of a trace property of the
𝑘-fold selfcomposition of the given system.
   The general case is much more diﬃcult. Hyperliveness properties like noninference contain an
alternation between universal and existential quantiﬁcation. The ∀∃ pattern occurs in many hy-
perproperties where the existential quantiﬁer resolves the potential nondeterminism in the system.
To prove such hyperproperties, we must, for every execution, establish the existence of another
execution such that the two executions respect a speciﬁed temporal relation. A straight-forward
idea is to provide an explicit witness for the existential quantiﬁer (cf. [31]). One way to do this is
to view the interaction between the universal and existential quantiﬁers as an inﬁnite game, such
that a winning strategy for the existential player provides a witness for the existential quantiﬁer.
For ﬁnite-state systems, the winning strategy can be found using techniques from reactive syn-
thesis [18]. In the deductive setting, guessing a winning strategy upfront is not only diﬃcult; any
error in the initial choice of strategy might furthermore only be revealed very late in the proof, re-
quiring a restart of the proof from the very beginning. A practical proof technique should therefore
be incremental, reﬁning the instantiation of the existential quantiﬁer on-the-ﬂy as needed during
the proof.
   In this paper, we present such an incremental proof technique. We accomplish this by linking
temporal hyperproperties to coinductive relations. Coinductive relations are supported by param-
eterized coinduction [29], a powerful proof technique with built-in support for incremental proofs.
This coalgebraic view precisely coincides with the game-theoretic interpretation in the sense that
they can prove exactly the same properties. However, the coalgebraic approach is much better
suited for an interactive proof assistant. In summary, we make the following contributions:


(1) We introduce HyCo, a coinductive relation to reason about the diﬃcult class of hyperproperties
    of the form ∀∗ ∃∗𝜓 , where 𝜓 is a safety relation between traces. Importantly, HyCo is language
    agnostic: it does not commit to a speciﬁc programming language to model systems, nor to a
    particular logic to specify trace relations.
(2) We formally prove the soundness of HyCo in the Coq proof assistant. Our proof relies on a
    subtle use of the axiom of functional choice to resolve the underlying existential quantiﬁcation.
(3) We further equip HyCo with a collection of incremental reasoning rules, useful up-to tech-
    niques, and specialized rules for the case where properties are speciﬁed using LTL-style tem-
    poral modalities. The soundness of the rules for temporal modalities critically relies on the
    notion of derivatives of trace relations, combined with the idea to reason up to stronger trace
    relations.


Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                     53:3


(4) Finally, we show that HyCo applies naturally to the veriﬁcation of reactive systems modeled
    as imperative programs with I/O. We provide specialized reasoning rules for this case, and give
    examples of program proofs using HyCo in Coq.

2 Preliminaries
2.1 Infinite Sequences and Set Notations
Given an alphabet Σ, we note Σ𝜔 the set of all inﬁnite sequences of letters in Σ. Given an inﬁnite
sequence 𝜏 ∈ Σ𝜔 , we note 𝜏 [𝑖] (𝑖 ∈ N) the letter at position 𝑖 in 𝜏, and we note 𝜏 [𝑖...] the inﬁnite
trace obtained by ignoring the ﬁrst 𝑖 letters of 𝜏. In particular, if 𝜏 = 𝜏0𝜏1𝜏2 ... we have 𝜏 [0] = 𝜏0 and
𝜏 [1...] = 𝜏1𝜏2 .... Given two sets 𝐴 and 𝐵, note 𝐴 ≡ 𝐵 if 𝐴 and 𝐵 are mutually included.

2.2   Labeled Transition Systems
Throughout this paper, we model reactive systems as labeled transition systems (LTS). Formally, a
LTS is a triple (S, E, I, →) where S is an arbitrary set of states, E is an arbitrary set of observable
events, I ∈ S is an initial state, and → ⊆ S×E ∪{∅}×S is a labeled transition relation between two
                                                                                       ∅
states and an (optional) event. Given two states 𝑠 1, 𝑠 2 ∈ S, the relation 𝑠 1 →
                                                                                − 𝑠 2 indicates that 𝑠 1 can
                                                                   𝑒
transition to 𝑠 2 without emitting any event. When 𝑒 ∈ E, 𝑠 1 →    − 𝑠 2 indicates that 𝑠 1 can transition
to 𝑠 2 while emitting the observable event 𝑒. We also adopt the following notation conventions:
                                                   ∅
                                → stands for →
                                             −
                               →∗     is the reﬂexive transitive closure of →
                                 𝑒                                  𝑒
                                      is a shorthand for →∗→
                                                           −
  Trace Semantics. Given a LTS TS = (S, E, I, →), a trace originating from a state 𝑠 ∈ S is an
inﬁnite sequence of events 𝜏 ∈ E 𝜔 such that there exists an inﬁnite sequence of states 𝜋 ∈ S𝜔
with
                                                               𝜏𝑖
                                            𝜋0 = 𝑠 ∧ ∀𝑖, 𝜋𝑖         𝜋𝑖+1
   Given a state 𝑠 ⊆ S, we note Traces TS (𝑠) ⊆ E 𝜔 the set of traces originating from 𝑠. When
the transition system being considered is clear from context, we simply note Traces(𝑠) for the
                                             Ð
traces of 𝑠. If 𝑆 ⊆ S we note Traces TS (𝑆) , 𝑠 ∈𝑆 Traces(𝑠). If I is the initial state of TS, we note
Traces(TS) , Traces(I) the traces of TS.

2.3   Temporal Hyperproperties
To specify hyperproperties of LTS, we introduce Hyper𝐸 , an event-based variant of HyperLTL
with support for arbitrary temporal relations between traces. A Hyper𝐸 formula Ψ starts with a
sequence of 𝑛 quantiﬁers ranging over the traces of some LTS and then speciﬁes a 𝑚-ary (𝑚 ≥ 𝑛)
trace relation 𝜓 .
                                          Ψ ::= ∀TS Ψ | ∃TS Ψ | 𝜓
  Given an (ordered) 𝑛-tuple of traces Γ, we note Γ |= Ψ when Γ satisﬁes the relation speciﬁed
by Ψ. The model relation is deﬁned as follows:
                               Γ |= ∀TS 𝜓 ⇐⇒ ∀𝜏 ∈ Traces(TS), (Γ, 𝜏) |= 𝜓
                               Γ |= ∃TS 𝜓 ⇐⇒ ∃𝜏 ∈ Traces(TS), (Γ, 𝜏) |= 𝜓
                                     Γ |= 𝜓 ⇐⇒ Γ ∈ 𝜓

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:4                                                                           Arthur Correnson and Bernd Finkbeiner


We will often consider relations 𝜓 expressed in (a fragment) of linear temporal logic. The basic
assertions are 𝑛-ary relations 𝜑 between events, and formulas are obtained by using boolean con-
nectives, and the temporal modalities W (weak-until), (always), and (next).

                                  𝜓 ::= 𝜑 | 𝜓 ∧ 𝜓 | 𝜓 ∨ 𝜓 | 𝜓 W 𝜓 |         𝜓 |     𝜓

   Given an 𝑛-tuple of traces Γ = (𝜏1, ..., 𝜏𝑛 ), we note Γ |= 𝜓 when Γ satisﬁes the temporal relation
deﬁned by 𝜓 . We note Γ [𝑖] the 𝑛-tuple of events (𝜏1 [𝑖], ..., 𝜏𝑛 [𝑖]), and Γ [𝑖...] the 𝑛-tuple of traces
(𝜏1 [𝑖...], ..., 𝜏𝑛 [𝑖...]). The interpretation of the modalities is deﬁned as follows:

                   Γ |= 𝜑 ⇐⇒ Γ [0] ∈ 𝜑
                 Γ |=    𝜓 ⇐⇒ Γ [1...] |= 𝜓
                 Γ |=    𝜓 ⇐⇒ ∀𝑖, Γ [𝑖...] |= 𝜓
             Γ |= 𝜓 1 W 𝜓 2 ⇐⇒ (∀𝑖, Γ [𝑖...] |= 𝜓 1 ) ∨ (∃𝑖, Γ [𝑖...] |= 𝜓 2 ∧ ∀𝑗 < 𝑖, Γ [ 𝑗 ...] |= 𝜓 1 )

 When 𝜓 is deﬁned using combinations of LTL modalities, we freely interchange 𝜓 and its set of
models { Γ | Γ |= 𝜓 }.

2.4    Parameterized Coinduction
We recall some basics about coinduction. Let (P (𝐴), ⊆, ∪) be the complete lattice of subsets of 𝐴,
                   mon
and let 𝐹 : P (𝐴) −−−→ P (𝐴) be a monotone operator on subsets. Then, 𝐹 has a greatest ﬁxed point
𝜈 .𝐹 and
                                           Ø
                                    𝜈 .𝐹 =   { 𝑅 | 𝑅 ⊆ 𝐹 (𝑅) }
   An immediate consequence of this observation is that whenever we have a property 𝑃 deﬁned
as a greatest ﬁxed point 𝑃 = 𝜈 .𝐹𝑃 (i.e., deﬁned coinductively), we have a systematic method to show
that an element 𝑥 satisﬁes 𝑃: it suﬃces to prove that 𝑥 is in some postﬁxed point 𝑅 of 𝐹𝑃 . In this
context, 𝑅 is usually called the coinduction hypothesis.

   Lemma 2.1 (Coinduction principle). 𝑋 ⊆ 𝜈 .𝐹 ⇐⇒ ∃𝑅, 𝑋 ⊆ 𝑅 ∧ 𝑅 ⊆ 𝐹 (𝑅)

   A common use case for coinduction is proofs by simulation. As an example, let us consider the
following two ﬁnite LTSs:
                                                                                            𝑏
                                        𝑎   𝑞1       𝑏
                 𝑇 𝑆1:             𝑞0                      𝑇 𝑆2:               𝑠0       𝑎
                                                                                            𝑠1
                                        𝑎   𝑞2       𝑐
                                                                                            𝑐
Clearly, all traces of TS 1 are also valid traces of TS 2 (i.e., TS 1 reﬁnes TS 2 ). To prove this fact, one way
is to enumerate the traces of TS 1 , but this would be impossible if the number of traces was inﬁnite.
Another way it to reduce the reasoning about traces to reasoning about states by establishing a
simulation relation. The idea is to show the existence of a mapping 𝑅 ⊆ S1 × S2 between states
                                                                                                            𝑒
of TS 1 and TS 2 such that (𝑞 0 , 𝑠 0 ) ∈ 𝑅, and such that for every pair of states (𝑞, 𝑠) ∈ 𝑅, if 𝑞          𝑞′
                                         𝑒
then there exists a state 𝑠 ′ with 𝑠       𝑠 ′ and (𝑞 ′ , 𝑠 ′ ) is again in 𝑅. The existence of such a mapping
ensures that for all traces originating from 𝑞 0 , there is a way to reproduce the same trace from
𝑠 0 . This intuition can be understood in coalgebraic terms by observing that the existence of a
simulation relation 𝑅 containing (𝑞 0, 𝑠 0 ) simply amounts to proving (𝑞 0, 𝑠 0 ) ∈ sim where sim is

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                     53:5


the coinductive relation deﬁned as follows:

                                                      𝑒                     𝑒
                  simF(𝑅) , {(𝑞, 𝑠) | ∀𝑒.∀𝑞 ′ .𝑞          𝑞 ′ =⇒ ∃𝑠 ′ , 𝑠       𝑠 ′ ∧ (𝑞 ′ , 𝑠 ′ ) ∈ 𝑅}
                        sim , 𝜈 .simF


By Lemma 2.1, (𝑞 0, 𝑠 0 ) ∈ sim if and only if there exists some relation 𝑅 containing (𝑞 0, 𝑠 0 ) and such
that 𝑅 ⊆ simF(𝑅). Going back to our simple example, 𝑅 = {(𝑞 0, 𝑠 0 ), (𝑞 1 , 𝑠 1 ), (𝑞 2, 𝑠 1 )} is a postﬁxed
point of simF, which proves trace-inclusion.
   For our previous example, guessing a simulation 𝑅 was not too diﬃcult. For larger examples,
especially if we consider transition systems with inﬁnite state-spaces, ﬁnding 𝑅 can be extremely
tedious. Instead we could also start with 𝑅 = {(𝑞 0 , 𝑠 0 )}, and explore the transition systems from
there, carefully matching transitions in the left-hand transition system with corresponding transi-
tions in the right-hand transition system and adding pairs of states to 𝑅 until we reach a postﬁxed
point. To achieve this incremental proof style, Hur et al. proposed parameterized coinduction [29].
The key idea is to replace the greatest ﬁxed point 𝜈 .𝐹 with a parameterized variant 𝐺 𝐹 (𝐻 ) where 𝐻
is a current guess for the coinduction hypothesis 𝑅. The parameterized greatest ﬁxed point operator
is deﬁned as

                                         𝐺 𝐹 (𝐻 ) , 𝜈 .(𝜆𝑋 .𝐹 (𝑋 ∪ 𝐻 ))


By deﬁnition, we have 𝜈 .𝐹 ≡ 𝐺 𝐹 (∅), which means that any time we need to prove a theorem of
the form 𝑋 ⊆ 𝜈 .𝐹 , we can prove 𝑋 ⊆ 𝐺 𝐹 (∅) instead. An important diﬀerence, however, is that 𝐺 𝐹
can be equipped with the following set of incremental reasoning rules:




                       Init               Accumulate                 Step
                       𝑋 ⊆ 𝐺 𝐹 (∅)        𝑋 ⊆ 𝐺 𝐹 (𝐻 ∪ 𝑋 )           𝑋 ⊆ 𝐹 (𝐻 ∪ 𝐺 𝐹 (𝐻 ))
                         𝑋 ⊆ 𝜈𝐹                 𝑋 ⊆ 𝐺 𝐹 (𝐻 )                𝑋 ⊆ 𝐺 𝐹 (𝐻 )
                                  Fig. 1. Rules of parameterized coinduction




  Brieﬂy,

  (1) The rule Init exploits the equation 𝜈𝐹 ≡ 𝐺 𝐹 (∅) to initiate a proof by parameterized coinduc-
      tion.
  (2) The rule Accumulate allows us to incrementally extend the current guess 𝐻
  (3) The rule Step allows us to make progress in the proof by unfolding the ﬁxed point equation
      𝐺 𝐹 (𝐻 ) = 𝐹 (𝐻 ∪ 𝐺 𝐹 (𝐻 ))

We refer the reader to [29] for a more detailed explanation of parameterized coinduction and for
proofs of these reasoning rules. For now, let us go back to our simulation example, and give an
incremental proof by parameterized coinduction.

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:6                                                                                                Arthur Correnson and Bernd Finkbeiner




             (𝑞 0, 𝑠 0 ) ∈ 𝜈 .simF
    ⇐⇒ (𝑞 0, 𝑠 0 ) ∈ 𝐺 simF (∅)                                                                                                        (by Init)
                         𝑎                                                   𝑎
       ⇐= ∃𝑠 ′, 𝑠 0           𝑠 ′ ∧ (𝑞 1 , 𝑠 ′ ) ∈ 𝐺 simF (∅) ∧ ∃𝑠 ′, 𝑠 0        𝑠 ′ ∧ (𝑞 2, 𝑠 ′ ) ∈ 𝐺 simF (∅)                        (by Step)
          |                         {z                      } |                        {z                     }
                                                 𝑎                                                      𝑎
                     ﬁnd a step matching 𝑞 0 →
                                             − 𝑞1                          ﬁnd a step matching 𝑞 0 →
                                                                                                   − 𝑞2
       ⇐= (𝑞 1, 𝑠 1 ) ∈ 𝐺 simF (∅) ∧ (𝑞 2, 𝑠 1 ) ∈ 𝐺 simF (∅)                                                                   (pick 𝑠 ′ = 𝑠 1 )
       ⇐= (𝑞 1, 𝑠 1 ) ∈ 𝐺 simF ({(𝑞 1 , 𝑠 1 )}) ∧ (𝑞 2 , 𝑠 1 ) ∈ 𝐺 simF ({(𝑞 2 , 𝑠 1 )})                                (by Accumulate)
                         𝑏
       ⇐= ∃𝑠 ′, 𝑠 1           𝑠 ′ ∧ (𝑞 1 , 𝑠 ′ ) ∈ {(𝑞 1, 𝑠 1 )} ∪ 𝐺 simF ({(𝑞 1 , 𝑠 1 )}) ∧                                           (by Step)
          |                                        {z                                   }
                                                                 𝑏
                                     ﬁnd a step matching 𝑞 1 →
                                                             − 𝑞1
                         𝑐
             ∃𝑠 ′, 𝑠 1        𝑠 ′ ∧ (𝑞 2 , 𝑠 ′ ) ∈ {(𝑞 2, 𝑠 1 )} ∪ 𝐺 simF ({(𝑞 2 , 𝑠 1 )})
             |                                     {z                                   }
                                                                 𝑐
                                     ﬁnd a step matching 𝑞 2 →
                                                             − 𝑞2
       ⇐= (𝑞 1, 𝑠 1 ) ∈ {(𝑞 1, 𝑠 1 )} ∧ (𝑞 2 , 𝑠 1 ) ∈ {(𝑞 2 , 𝑠 1 )}                                                           (pick 𝑠 ′ = 𝑠 1 )

3      Hyperliveness and Relational Invariance, Coinductively
In the previous section, we recalled that trace inclusion between two transition systems can be
reduced to reasoning about states by ﬁnding a simulation relation. Further, parameterized coinduc-
tion can be used to construct a simulation relation incrementally. Trace inclusion is an example of
hyperliveness property: given two transition systems TS 1 and TS 2 emitting events in E, it can be
speciﬁed as the formula ∀TS1 ∃TS2 eq where eq = { (𝑒, 𝑒) | 𝑒 ∈ E } is equality of events. In this
section, we show that parameterized coinduction can also be used for incremental proofs of any
hyperproperties of the form ∀∃ 𝜑 where 𝜑 is a binary relation between events. To do so, we gen-
eralize the operator simF and deﬁne a coinductive relation fei𝜑 that soundly underapproximates
∀∃ 𝜑. We describe the construction of fei𝜑 , show that it can be equipped with useful reasoning
rules, and propose a formal proof of soundness via the axiom of functional choice. In Section 4,
we extend this construction to support the more general class of ∀∃𝜓 hyperproperties where 𝜓 is
a safety relation between traces.

3.1       Generalizing Simulation Relations
For the remainder of this section, let TS 1 = (S1, E1, I1, →1 ) and TS 2 = (S2, E2, →2 ) be two LTSs,
and let us ﬁx a binary relation between events 𝜑 ⊆ E1 × E2 . We deﬁne the relation fei𝜑 (forall,
exists, invariant) as follows:
                                                            𝑒1                      𝑒2
                   feiF𝜑 (𝑅) , { (𝑠 1, 𝑠 2 ) | ∀𝑠 1                  𝑠 1′ =⇒ ∃𝑠 2        𝑠 2′ ∧ (𝑒 1 , 𝑒 2 ) ∈ 𝜑 ∧ 𝑅(𝑠 1′ , 𝑠 2′ ) }
                             fei𝜑 , 𝜈 .feiF𝜑

  As expected, the fei𝜑 relation provides a sound proof technique to verify hyperproperties of
the form ∀∃ 𝜑. More precisely, if the initial states of TS 1 and TS 2 are related by fei𝜑 , it can then
be concluded that ∀TS1 ∃TS2 𝜑 is valid.

    Theorem 3.1 (Soundness of fei𝜑 ). Let TS 1 and TS 2 be two LTSs and let 𝜑 ⊆ E1 × E2 . We have

                                                (I1, I2 ) ∈ fei𝜑 =⇒ |= ∀TS1 ∃TS2                    𝜑

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                          53:7


   While this theorem might seem like an unsurprising generalization of simulation proofs, its for-
mal proof turns out to be much more involved. Indeed, to prove this theorem we need to ﬁnd a
suitable trace to instantiate the inner existential quantiﬁer. Note that in the simpler case of simu-
lation proofs, since the two quantiﬁed traces are required to be equal, the existential quantiﬁer is
superﬂuous and it suﬃces to instantiate it with a copy of the universal trace. In the more general
case of ∀∃ 𝜑, the witness for the existential quantiﬁer depends on the relation 𝜑 (and the quan-
tiﬁed systems) and we need to somehow extract it from the proof of (I1 , I2 ) ∈ fei𝜑 . We delay the
explanation of this process to Section 3.4.

3.2 Incremental Proofs
As discussed in the preliminaries, a limitation of standard coinductive proofs is that they require
us to ﬁnd a coinduction hypothesis up-front. Instead, parameterized coinduction [29] allows us to
perform coinductive proofs incrementally by starting from ∅ and progressively guessing portions
of a coinductive hypothesis until a postﬁxed point is reached. In this section, we leverage pa-
rameterized coinduction to prove hyperproperties incrementally via fei. Taking inspiration from
notations introduced in [15], we start by deﬁning the following two semantic quadruples:
                               𝐻 ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 } , (𝑠 1, 𝑠 2 ) ∈ 𝐺 feiF𝜑 (𝐻 )
                               𝐻 ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 } , (𝑠 1, 𝑠 2 ) ∈ 𝐻 ∪ 𝐺 feiF𝜑 (𝐻 )

    Note that (𝑠 1, 𝑠 2 ) ∈ fei𝜑 ⇐⇒ ∅ ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 }. In turn, to prove |= ∀TS1 ∃TS2 𝜑, it
suﬃces to show ∅ ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 }. Further, since these quadruples are deﬁned in terms of the
parameterized greatest ﬁxed point operator 𝐺, they admit incremental reasoning principles. The
intention behind the choice of notation is that 𝐻 represents a guarded coinduction hypothesis
(i.e., it cannot yet be used to conclude a proof), whereas 𝐻 represents an unguarded coinduction
hypothesis (i.e., it can be used to immediately conclude a proof if (𝑠 1 , 𝑠 2 ) ∈ 𝐻 ). The core reasoning
rules associated with these quadruples are presented in Figure 2. In the conclusion of some rules,
we note 𝐻 ? instead of 𝐻 or 𝐻 when the rule can be applied regardless of whether the hypothesis
is currently guarded or not.

                           Init                                          Cycle
                               ∅ ⊢inv I1 ∀ | I2 ∃ { 𝜑 }                           (𝑠 1 , 𝑠 2 ) ∈ 𝐻
                                           TS 1 TS2
                                    |= ∀      ∃           𝜑                 𝐻 ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 }

                       Step
                               𝑒1                  𝑒2
                        ∀𝑠 1         𝑠 1′ , ∃𝑠 2        𝑠 2′ , (𝑒 1 , 𝑒 2 ) ∈ 𝜑 ∧ 𝐻 ⊢inv 𝑠 1′ ∀ | 𝑠 2′ ∃ { 𝜑 }
                                                        𝐻 ? ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 }

                     Invariant
                      (𝑠 1 , 𝑠 2 ) ∈ 𝐻 ′           ∀(𝑠 1 , 𝑠 2 ) ∈ 𝐻 ′ , 𝐻 ∪ 𝐻 ′ ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 }
                                                        𝐻 ? ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 }

                                       Fig. 2. Incremental reasoning rules for fei

  All rules are derived from the soundness of fei (Theorem 3.1), the rules of parameterized coin-
duction (Figure 1), and the deﬁnition of feiF. The rule Init exploits the soundness of fei to initiate

                                    Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:8                                                                                    Arthur Correnson and Bernd Finkbeiner


a proof by parameterized coinduction. When focusing on a pair of states (𝑠 1, 𝑠 2 ), the rule Step re-
                                                   𝑒1 ′                                                   𝑒2 ′
quires to prove that for every transition 𝑠 1          𝑠 1 , there exists a corresponding transition 𝑠 2     𝑠2
such that 𝑒 1 and 𝑒 2 satisfy the event-invariant 𝜑. Applying Step transfers the focus to the pairs of
states (𝑠 1′ , 𝑠 2′ ) and releases the guard. Cycle allows us to ﬁnish a proof by creating a cycle: if we
already encountered a pair (𝑠 1, 𝑠 2 ) earlier in the proof (i.e., if (𝑠 1, 𝑠 2 ) ∈ 𝐻 ) we can use this fact to
immediately conclude. Note that applying Cycle requires the hypothesis to be unguarded. Finally,
the rule Invariant is a reformulation of the rule Accumulate of parameterized coinduction. It
extends the current coinduction hypothesis 𝐻 with a larger guess 𝐻 ∪ 𝐻 ′ , where 𝐻 ′ contains at
least the current pair of states. The cost to pay is that applying Invariant restores the guard, and
requires to prove a quadruple for every state in 𝐻 ∪ 𝐻 ′ instead of just the initial pair of states. The
beneﬁt is that, after applying the rule Invariant, we can conclude a proof as soon as we reach
again a pair of states that satisfy the invariant 𝐻 ′ . We note that the rules Step and Invariant can
be applied regardless of whether the hypothesis is currently guarded or not.
   Example 3.2. Let us consider the following transition system, whose events are E = {𝑎, 𝑏}:
                                                                     𝑠1        𝑎
                                                           𝑠0
                                                                     𝑠2        𝑏

Suppose we wish to prove |= ∀TS ∃TS (𝑎 1 ↔ 𝑏 2 ) where 𝑎 1 ↔ 𝑏 2 stands for the binary relation
{ (𝑎, 𝑏), (𝑏, 𝑎) }. We give an incremental proof using the rules of Figure 2. The proof starts by
exploring the system until we reach states 𝑠 1 and 𝑠 2 :
                 |= ∀TS ∃TS (𝑎 1 ↔ 𝑏 2 )
        ⇐=       ∅ ⊢inv 𝑠 0 ∀ | 𝑠 0 ∃ { 𝑎 1 ↔ 𝑏 2 }                                                       (by Init)
                              ∀      ∃                                     ∀       ∃
        ⇐=       ∅ ⊢inv 𝑠 1 | 𝑠 2 { 𝑎 1 ↔ 𝑏 2 } ∧ ∅ ⊢inv 𝑠 2 | 𝑠 1 { 𝑎 1 ↔ 𝑏 2 }                          (by Step)
Then, we observe that the only way out of the pair (𝑠 1 , 𝑠 2 ) (resp. (𝑠 2, 𝑠 1 )) is to go back to (𝑠 1 , 𝑠 2 )
(resp. (𝑠 2, 𝑠 1 )). This indicates that 𝐻 1 = {(𝑠 1 , 𝑠 2 )} and 𝐻 2 = {(𝑠 2, 𝑠 1 )} are good choices of coinduction
hypotheses. We therefore extend our current hypotheses with 𝐻 1 and 𝐻 2 using Invariant:
             ∅ ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝑎 1 ↔ 𝑏 2 } ∧ ∅ ⊢inv 𝑠 2 ∀ | 𝑠 1 ∃ { 𝑎 1 ↔ 𝑏 2 }
       ⇐=    𝐻 1 ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝑎 1 ↔ 𝑏 2 } ∧ 𝐻 2 ⊢inv 𝑠 2 ∀ | 𝑠 1 ∃ { 𝑎 1 ↔ 𝑏 2 }              (by Invariant)
Using Step, 𝑎-transitions out of 𝑠 1 are matched with 𝑏-transitions out of 𝑠 2 (and vice-versa), thus
maintaining the event-invariant 𝑎 1 ↔ 𝑏 2 . Note that taking a step releases the guard! Since transi-
tioning out of (𝑠 1, 𝑠 2 ) (resp. (𝑠 2, 𝑠 1 )) cycles back to (𝑠 1, 𝑠 2 ) (resp. (𝑠 2 , 𝑠 1 )), we can then conclude with
Cycle:
               𝐻 1 ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝑎 1 ↔ 𝑏 2 } ∧ 𝐻 2 ⊢inv 𝑠 2 ∀ | 𝑠 1 ∃ { 𝑎 1 ↔ 𝑏 2 }
       ⇐=      𝐻 1 ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝑎 1 ↔ 𝑏 2 } ∧ 𝐻 2 ⊢inv 𝑠 2 ∀ | 𝑠 1 ∃ { 𝑎 1 ↔ 𝑏 2 }                 (by Step)
       ⇐=     (𝑠 1 , 𝑠 2 ) ∈ 𝐻 1 = {(𝑠 1, 𝑠 2 )} ∧ (𝑠 2 , 𝑠 1 ) ∈ 𝐻 2 = {(𝑠 2, 𝑠 1 )}                     (by Cycle)

3.3 Alignment Rules
Sometimes, it is convenient to be able to step through the execution from the left state and the
right state at diﬀerent paces in order to align the states in a certain way before establishing an
invariant via Invariant. As an example, consider the following two transition systems:

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                           53:9


                           TS1 :           𝑠0           𝑠1        𝑎          TS2 :         𝑞0      𝑏

    Clearly, |= ∀TS1 ∃TS2 (𝑎 1 ∧ 𝑏 2 ). One way to prove it is to use the Step rule to reach (𝑠 1, 𝑞 0 ), then
Invariant to add (𝑠 1, 𝑞 0 ) to the current coinduction hypothesis, and conclude by using Step and
Cycle. While this proof is perfectly valid, it forces us to use the Step rule two times to prove that
an 𝑎 on the left-hand transition system can always be matched by a 𝑏 in the right-hand system. For
such a small example, duplicating the reasoning is not diﬃcult, but for more complicated systems,
it might actually be extremely tedious. Instead, what we would like to do is to ﬁrst align the states
𝑠 1 and 𝑞 0 by taking one step of computation in the left-hand transition system, then add (𝑠 1, 𝑞 0 ) to
the current hypothesis, and ﬁnish the proof with a single application of the rule Step followed by
Cycle. In this section, we introduce reasoning rules to support this intuition.
    To reproduce the proof we just described, we would need a rule of the following form:
                                          𝑠 1 →∗ 𝑠 1′        𝐻 ⊢inv 𝑠 1′ ∀ | 𝑠 2 ∃ { 𝜑 }
                                                   𝐻 ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 }
   This rule would allow us to skip silent computation steps in the left-hand transition system.
Unfortunately, it is unsound in the presence of nondeterminism. Indeed, if along the path from 𝑠 1
to 𝑠 1′ , there are possibilities to branch out to some other state 𝑠 1′′ , this rule would not ensure that
the step to 𝑠 1′′ can be matched by a corresponding step from 𝑠 2 . A potential solution would be to
determinize the rule by universally quantifying on the post-states of 𝑠 1 :
                                      ∀𝑠 1′ , 𝑠 1 →∗ 𝑠 1′ =⇒ 𝐻 ⊢inv 𝑠 1′ ∀ | 𝑠 2 ∃ { 𝜑 }
                                                   𝐻 ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 }
  This rule is naturally sound, as it forces us to cover all possible ways to transition out of 𝑠 1 .
However, instead of solving the initial problem, it makes it even worse by generating redundant
proof obligations. Indeed, if we have a path 𝑠 1 → 𝑠 11 → 𝑠 12 ... → 𝑠 1′ , this rule will generate a
proof obligation for all 𝑠 1𝑖 . Instead, what we would like is to merge as many steps as possible to
minimize the number of proof obligations. To achieve this goal, we need to be able to distinguish
deterministic sequences of computations from nondeterministic ones. To this eﬀect, we introduce
the deterministic transition relation →det deﬁned as follows:
                                                                       𝑒
                     𝑠 →det 𝑠 ′ ⇐⇒ 𝑠 → 𝑠 ′ ∧ (∀𝑒∀𝑠 ′′ , 𝑠 →
                                                          − 𝑠 ′′ =⇒ 𝑠 ′ = 𝑠 ′′ ∧ 𝑒 = ∅)
Intuitively, a deterministic transition 𝑠 1 →det 𝑠 2 indicates that 𝑠 2 is the only possible successor of
𝑠 1 and further, that no event can be emitted by the transition to 𝑠 2 . Using →det instead of →, we
obtain the following sound rules:

          Steps-L                                                     Steps-R
          𝑠 1 →∗det 𝑠 1′           𝐻 ⊢inv 𝑠 1′ ∀ | 𝑠 2 ∃ { 𝜑 }        𝑠 2 →∗ 𝑠 2′      𝐻 ⊢inv 𝑠 1 ∀ | 𝑠 2′ ∃ { 𝜑 }
                     𝐻 ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 }                                 𝐻 ⊢inv 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜑 }

3.4   Soundness Proof
The initial claim that motivated the previous section is that fei𝜑 is a sound approximation of
the hyperproperty ∀∃ 𝜑. This section is dedicated to the proof of this fact. While the high-level
intuition is relatively straightforward, the formal proof turns out to be more involved. We start by
giving an intuitive informal proof, and we then present a formal proof via the axiom of functional
choice. The latter has been mechanized in the Coq proof assistant.

                                     Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:10                                                                                                     Arthur Correnson and Bernd Finkbeiner


Informal proof. Let 𝜑 ⊆ E1 × E2 be a relation on events, 𝑠 1 ∈ S1 and 𝑠 2 ∈ S2 be two states, and
assume that (𝑠 1, 𝑠 2 ) ∈ fei𝜑 . Under these assumptions, we would like to prove
                                  ∀𝜏1 ∈ Traces(𝑠 1 ), ∃𝜏2 ∈ Traces(𝑠 2 ), (𝜏1 , 𝜏2 ) ∈                            𝜑
  Given a trace 𝜏1 ∈ Traces(𝑠 1 ), we need to construct an appropriate trace 𝜏2 to instantiate the
existential quantiﬁer. Since 𝜏1 ∈ Traces(𝑠 1 ), there has to exist some state 𝑠 1′ such that
                                                    𝜏1 [0] ′
                                          (1) 𝑠 1         𝑠1               (2) 𝜏1 [1...] ∈ Traces(𝑠 1′ )
Since (𝑠 1 , 𝑠 2 ) ∈ fei𝜑 = 𝜈 .feiF𝜑 , by unfolding the ﬁxed point equation fei𝜑 = feiF𝜑 (𝜈 .feiF𝜑 ),
unfolding the deﬁnition of feiF, and using (1) we obtain the existence of an event 𝑒 20 and a state
𝑠 2′ such that
                                     𝑒 20
                        (3) 𝑠 2              𝑠 2′     (4) (𝜏1 [0], 𝑒 20 ) ∈ 𝜑                     (5) (𝑠 1′ , 𝑠 2′ ) ∈ fei𝜑
   We can repeat this reasoning from the assumption that (𝑠 1′ , 𝑠 2′ ) ∈ fei𝜑 and from (2) to obtain a
state 𝑠 1′′ , and event 𝑒 21 , and a state 𝑠 2′′ such that
                                   𝑒 21
                       (6) 𝑠 2′             𝑠 2′′     (7) (𝜏1 [1], 𝑒 21 ) ∈ 𝜑                     (8) (𝑠 1′′ , 𝑠 2′′ ) ∈ fei𝜑
  Iterating this process an inﬁnite number of times, we obtain a sequence of events 𝜏2 = 𝑒 20𝑒 21𝑒 22 ....
By construction 𝜏2 ∈ Traces(𝑠 2 ) and clearly (𝜏1 , 𝜏2 ) ∈ 𝜑 since (𝜏 [𝑖], 𝑒 2𝑖 ) ∈ 𝜑.
Formal Proof via Classical Choice. The main challenge when mechanizing the previous proof in
the Coq proof assistant is to formalize the intuition of "iterating this process an inﬁnite number of
times". We propose a solution in four stages:
  (1) We start by deﬁning an abstract labeled transition system between proof states. Transitions
      are labeled by events.
  (2) We prove that this abstract system is progressive: for any proof state, we can always transi-
      tion to a successor state.
  (3) Using the axiom of functional choice and (2), we extract a deterministic and executable ver-
      sion of the abstract transition system that produces exactly one trace
  (4) Using (3), we compute the unique trace of the abstract transition system. The system is
      constructed in such a way that this trace is guaranteed to be a valid witness for the existential
      quantiﬁer.
   Given a relation 𝜑 ⊆ E1 × E2 , we deﬁne the set of proof states Π𝜑 as follows:
                 Π𝜑 ⊆ S1 × S2 × S1𝜔 , { (𝑠 1 , 𝑠 2, 𝜏1 ) | 𝜏1 ∈ Traces(𝑠 1 ) ∧ (𝑠 1 , 𝑠 2 ) ∈ fei𝜑 }

                                                                                                  −
   We then deﬁne the following labeled proof-step relation −
                                                           →𝜑 ⊆ Π𝜑 × E2 × Π𝜑 :
                                                               𝑒1                     𝑒2
                            𝜏1 = 𝑒 1 · 𝜏1′              𝑠1          𝑠 1′         𝑠2        𝑠 2′         (𝑒 1 , 𝑒 2 ) ∈ 𝜑
                                                                            𝑒2
                                                      (𝑠 1, 𝑠 2, 𝜏1 ) −→𝜑 (𝑠 1′ , 𝑠 2′ , 𝜏1′ )
  This transition relation describes an abstract transition system over proof states, and such that
each transition generates an event in E2 . Importantly, it can be proven that this abstract transition
system is progressive: every proof state has a successor.
                                                                                                  𝑒2
   Lemma 3.3 (Progress). ∀𝜋 ∈ Π𝜑 , ∃(𝑒 2, 𝜋 ′ ) ∈ E2 × Π𝜑 , 𝜋 −→𝜑 𝜋 ′

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                                   53:11


  Proof. Let (𝑠 1, 𝑠 2, 𝜏1 ) ∈ Π𝜑 . By deﬁnition we have 𝜏1 ∈ Traces(𝑠 1 ) and (𝑠 1 , 𝑠 2 ) ∈ fei𝜑 . By
unfolding the the deﬁnition of Traces, we easily obtain the existence of a state 𝑠 1′ such that
                                                   𝜏1 [0] ′
                                              𝑠1         𝑠 1 ∧ 𝜏1 [1...] ∈ Traces(𝑠 1′ )
                                                                                           𝜏1 [0]
By unfolding the deﬁnition of fei𝜑 and using the fact that 𝑠 1                                      𝑠 1′ , we obtain the existence of
an event 𝑒 2 and a state 𝑠 2′ such that
                                         𝑒2
                                  𝑠2          𝑠 2′ ∧ (𝜏1 [0], 𝑒 2 ) ∈ 𝜑 ∧ (𝑠 1′ , 𝑠 2′ ) ∈ fei𝜑
                                                                                 𝑒2
Clearly, we have (𝑠 1′ , 𝑠 2′ , 𝜏 [1...]) ∈ Π𝜑 , and (𝑠 1, 𝑠 2 , 𝜏1 ) −→𝜑 (𝑠 1′ , 𝑠 2′ , 𝜏1 [1...]), which concludes our
proof.                                                                                                                

  By the axiom of functional choice, the previous lemma guarantees the existence of a function
progress : Π𝜑 → E2 × Π𝜑 that computes an event and a successor state. We start by recalling
the axiom in set-theoretic terms for clarity (the Coq implementation of the proof relies on a type-
theoretic formulation of the same axiom).
   Deﬁnition 3.4 (Functional Choice). Let 𝐴 and 𝐵 be two sets and 𝑅 ⊆ 𝐴 × 𝐵 a binary relation
such that ∀𝑎 ∈ 𝐴, ∃𝑏 ∈ 𝐵, (𝑎, 𝑏) ∈ 𝑅. Then, there exists a function 𝑓 : 𝐴 → 𝐵 such that ∀𝑎 ∈
𝐴, (𝑎, 𝑓 (𝑎)) ∈ 𝑅
  Corollary 3.5. There exists a function progress𝜑 : Π𝜑 → E2 × Π𝜑 such that for any proof state
𝜋 we have
                                                           𝑒
                            (𝑒, 𝜋 ′ ) = progress𝜑 (𝜋) =⇒ 𝜋 →
                                                           − 𝜑 𝜋′
   Using the progress function provided by this corollary, for any proof state 𝜋 we can construct
a sequence witness(𝜋) ∈ E2 deﬁned coinductively as follows:
                      witness(𝜋) , let (𝑒, 𝜋 ′ ) = progress(𝜋) in 𝑒 · witness(𝜋 ′ )
   By construction, the witness function satisﬁes the following properties.
  Lemma 3.6 (Witness). Let 𝜋 = (𝑠 1, 𝑠 2, 𝜏1 ) ∈ Π𝜑 and let 𝜏2 = witness(𝜋). Then 𝜏2 ∈ Traces(𝑠 2 )
and (𝜏1, 𝜏2 ) ∈ 𝜑
   Proof. Both facts follow from the deﬁnition of the proof-step relation →𝜑 . Indeed, if we have
a sequence of proof states
                                                     𝑒 20                 𝑒 21
                                (𝑠 10, 𝑠 20, 𝜏10 ) −→𝜑 (𝑠 11 , 𝑠 21, 𝜏11 ) −→𝜑 (𝑠 12, 𝑠 22 , 𝜏12 ) . . .
                                  𝑒 𝑖2
then in particular ∀𝑖 ∈ N, 𝑠 2𝑖           𝑠 2𝑖+1 (thus proving that 𝜏2 is a valid trace), and ∀𝑖 ∈ N, (𝜏1𝑖 [0], 𝑒 2𝑖 ) ∈ 𝜑
(thus proving that (𝜏1, 𝜏2 ) ∈           𝜑).                                                                             

   We can now easily prove the soundness of fei𝜑 (Theorem 3.1).

   Proof. Suppose (𝑠 1 , 𝑠 2 ) ∈ fei𝜑 , and let 𝜏1 ∈ Traces(𝑠 1 ), we show
                                              ∃𝜏2 ∈ Traces(𝑠 2 ), (𝜏1 , 𝜏2 ) ∈            𝜑
We pose 𝜋 , (𝑠 1, 𝑠 2 , 𝜏1 ). Clearly, 𝜋 ∈ Π𝜑 . We then choose 𝜏2 = witness(𝜋). By the previous lemma,
𝜏2 ∈ Traces(𝑠 2 ) and (𝜏1, 𝜏2 ) ∈ 𝜑. If we consider 𝑠 1 = I1 and 𝑠 2 = I2 , the above construction gives
a proof of |= ∀TS1 ∃TS2 𝜑.                                                                            

                                Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:12                                                                                 Arthur Correnson and Bernd Finkbeiner


4 From Relational Invariants to Safety Relations
While formulas of the form ∀∃ 𝜑 are already covering relevant hyperproperties such as trace-
inclusion and several variants of generalized non-interference, many temporal hyperproperties of
interest are of the more general form ∀∃𝜓 where 𝜓 is an arbitrary safety relation between traces. In
this section, we extend the coinductive relation fei to support reasoning about arbitrary safety re-
lations. Further, we develop reasoning rules for the speciﬁc case where safety relations are deﬁned
using LTL-style temporal modalities.

4.1     It’s All About Staying Safe
Intuitively, safety relations are relations that specify the absence of bad interactions between two
traces. More formally, safety relations between inﬁnite traces are exactly these for which it suf-
ﬁces to look at ﬁnite preﬁxes to determine whether the relation is violated. In other words, for
every safety relation there exists a so called monitor that, given a pair of trace preﬁxes, checks
wether or not they are compatible with the relation. Further, two traces satisfy a safety relation
if and only if all their preﬁxes are accepted by the monitor. Following this intuition, establishing
a safety property 𝜓 can always be reduced to a proof of invariance: it suﬃces to run the system
and the monitor for 𝜓 concurrently, and to prove the invariant "the monitor never reports any
violation". However, extracting an appropriate monitor for any arbitrary safety relation 𝜓 is non-
trivial, especially when the relation 𝜓 is expressed in an expressive temporal logic. One way to
systematically extract a monitor from a high-level logical speciﬁcation is by computing a ﬁnite-
word safety automaton that accepts all pairs of preﬁxes compatible with a trace relation. While
this approach works well for automated veriﬁcation (because veriﬁcation can then be reduced to
eﬃcient operations on automata), it it not a satisfactory solution for interactive veriﬁcation inside
a proof assistant. First of all, translating a high-level speciﬁcation expressed in a temporal logic
to an equivalent automaton is a non-trivial task. Further, we would also need to formally verify
the correctness of this translation. Finally, even assuming that we have a certiﬁed algorithm to
translate high-level speciﬁcations to automata [23], we would then need to reason about states
and transitions of these automata rather than reasoning about the original logical speciﬁcations.
This would lead to tedious and unintuitive proofs. Instead, we propose a solution via the notion
of property derivatives [14, 39]. The key insight is to observe that given a safety relation 𝜓 and
two traces 𝜏1 , 𝜏2 , there is a systematic way to decompose a proof of (𝜏1, 𝜏2 ) ∈ 𝜓 into a condition
on 𝜏1 [0], 𝜏2 [0] expressing what needs to hold now in order for 𝜓 to not be immediately violated;
and a proof of (𝜏1 [1...], 𝜏2 [1...]) ∈ 𝜓 ′ for some carefully chosen 𝜓 ′ expressing what need to hold
next in order for 𝜓 to not be violated later. In this section, we exploit this observation to extend
the coinductive relation fei presented in the previous section to a more general relation fe that
supports reasoning about arbitrary safety relations.

4.2     Coinductive Safety Proofs
Formally, safety relations between traces can be deﬁned in terms of a safety closure operator |−| safe :
                 mon
P (E1𝜔 × E2𝜔 ) −−−→ P (E1𝜔 × E2𝜔 ). Given a trace relation 𝜓 , the safety closure |𝜓 | safe is extracting the
safety part of 𝜓 by relating all pairs of traces such that all their preﬁxes are compatible with 𝜓 (i.e.,
there exists a way to extend the preﬁxes into inﬁnite traces that satisfy 𝜓 ).

    Deﬁnition 4.1 (Safety closure). Let 𝜓 ⊆ E1𝜔 × E2𝜔 be a binary trace relation. The safety closure of
𝜓 , noted |𝜓 | safe is the binary trace relation deﬁned as follows:

                |𝜓 | safe = {(𝜏1 , 𝜏2 ) | ∀𝑛, ∃𝜏1′ , 𝜏2′ ∈ E1𝜔 × E2𝜔 , (𝜏1 [𝑛...] · 𝜏1′ , 𝜏2 [𝑛..] · 𝜏2′ ) ∈ 𝜓 }

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                   53:13


  Safety properties are then deﬁned to be all ﬁxed points of | − | safe , i.e., all the trace relations
that are equivalent to their safety closure. Since 𝜓 ⊆ |𝜓 | safe for any 𝜓 , safety relations can be
equivalently characterized as preﬁxed points of | − | safe .
  Deﬁnition 4.2 (Safety relations). A trace relation 𝜓 is said to be a safety relation iﬀ |𝜓 | safe ⊆ 𝜓
   We observe that the safety closure of a relation can equivalently be deﬁned as a greatest ﬁxed
point. We start by introducing an operator Δ, inspired by the notion of derivatives introduced by
Brzozowski [14]. Given two events 𝑒 1 ∈ E1, 𝑒 2 ∈ E2 , the derivative of 𝜓 , noted Δ𝑒1,𝑒2 (𝜓 ), is the
relation that should be satisﬁed by suﬃxes 𝜏1 ∈ E1𝜔 , 𝜏2 ∈ E2𝜔 in order for the traces (𝑒 1𝜏1 , 𝑒 2𝜏2 ) to
satisfy 𝜓 . Formally, we have:
                                  Δ𝑒1,𝑒2 (𝜓 ) , { (𝜏1 , 𝜏2 ) | (𝑒 1𝜏1 , 𝑒 2𝜏2 ) ∈ 𝜓 }
  Two traces 𝜏1 = 𝑒 1𝜏1′ and 𝜏2 = 𝑒 2𝑡 2′ are in the safety closure of 𝜑 if the derivative Δ𝑒1,𝑒2 (𝜓 ) is
non-empty (i.e., the ﬁrst two symbols are not trivially violating the relation), and if the suﬃxes
𝜏1′ , 𝜏2′ are again in the closure of Δ𝑒1,𝑒2 (𝜓 ). This intuition is formally captured by the deﬁnition of a
ternary coinductive relation safe ∈ P (E1𝜔 × E2𝜔 × P (E1𝜔 × E2𝜔 ))
                  safeF(𝐶) , {(𝑒 1𝜏1, 𝑒 2𝜏2,𝜓 ) | Δ𝑒1,𝑒2 (𝜑) ≠ ∅ ∧ (𝜏1, 𝜏2 , Δ𝑒1,𝑒2 (𝜓 )) ∈ 𝐶}
                        safe , 𝜈 .safeF
The relation safe precisely characterizes the safety closure in the sense of the following lemma:
  Lemma 4.3. (𝜏1 , 𝜏2 ) ∈ |𝜓 | safe ⇐⇒ (𝜏1 , 𝜏2,𝜓 ) ∈ safe
  Proof.
   • (⇐=) By induction on the length of the preﬁxes in the deﬁnition of | − | safe , unfolding the
     ﬁxed point equation safe = safeF(safe), and exploiting the fact that Δ𝑒1,𝑒2 (𝜓 ) ≠ ∅ ⇐⇒
     ∃(𝜏1, 𝜏2 ), (𝑒 1𝜏1, 𝑒 2𝜏2 ) ∈ 𝜓 (∗).
   • (=⇒) By coinduction with 𝑅 = { (𝜏1, 𝜏2,𝜓 ) | (𝜏1, 𝜏2 ) ∈ 𝜓 } as the coinduction hypothesis.
     The fact that 𝑅 is a postﬁxed point of safeF follows from (∗) and the additional observation
     that (𝑒 1𝜏1, 𝑒 2𝜏2 ) ∈ |𝜓 | safe =⇒ (𝜏1, 𝜏2 ) ∈ |Δ𝑒1,𝑒2 (𝜓 )| safe .
                                                                                                 
  As an immediate corollary, we can use coinduction to prove that a pair of traces satisﬁes any
safety relation.
  Corollary 4.4 (Coinductive safety proofs). Let 𝜓 be a safety property, then
                       (𝜏1 , 𝜏2 ) ∈ 𝜓 ⇐⇒ (𝜏1 , 𝜏2 ) ∈ |𝜓 | safe ⇐⇒ (𝜏1 , 𝜏2,𝜓 ) ∈ safe
  A useful interpretation of this corollary is that, given two traces 𝜏1, 𝜏2 and a safety property𝜓 , the
derivative operator gives a systematic way to split the proof of (𝜏1, 𝜏2 ) ∈ 𝜓 into what needs to hold
now (i.e., Δ𝜏1 [0],𝜏2 [0] (𝜓 ) ≠ ∅) and what needs to hold next (i.e., (𝜏1 [1...], 𝜏2 [1...], Δ𝜏1 [0],𝜏2 [0] (𝜓 )) ∈
safe). The next subsection builds on this intuition to construct a coinductive relation fe that
extends fei with support for reasoning about arbitrary safety relations.

4.3   A Coinductive Relation Supporting Safety Specifications
For the rest of this section, we ﬁx two LTSs TS 1 = (S1 , E1, I1 , →1 ) and TS 2 = (S2 , E2, I2 , →2 ). To
extend fei to the more general case of arbitrary safety relations, we replace the functor feiF𝜑 :
               mon
P (S1 × S2 ) −−−→ P (S1 × S2 ), with a new functor feF that has the following signature:
                                                            mon
                  feF : P (S1 × S2 × P (E1𝜔 × E2𝜔 )) −−−→ P (S1 × S2 × P (E1𝜔 × E2𝜔 ))

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:14                                                                                              Arthur Correnson and Bernd Finkbeiner


The associated greatest ﬁxed point fe , 𝜈 .feF relates two states and a trace relation. The intention
is that for any safety relation 𝜓 , a proof of (𝑠 1 , 𝑠 2,𝜓 ) ∈ fe should guarantee that (𝑠 1, 𝑠 2 ) ∈ ∀TS1 ∃TS2𝜓 .
Importantly, with this more general signature, the trace relation 𝜓 can change over the course of
a coinductive proof. This will allow us to use the notion of derivatives to unroll 𝜓 . We start by
deﬁning an operator next𝑒𝑅1,𝑒2 (𝜓 ) ⊆ S1 × S2 :
                    next𝑒𝑅1 ,𝑒2 (𝜓 ) , { (𝑠 1 , 𝑠 2 ) | Δ𝑒1,𝑒2 (𝜓 ) ≠ ∅ ∧ (𝑠 1, 𝑠 2, Δ𝑒1,𝑒2 (𝜓 )) ∈ 𝑅 }
We use next to deﬁne the coinductive relation fe:
                                                         𝑒1                   𝑒2
                   feF(𝑅) , { (𝑠 1 , 𝑠 2,𝜓 ) | ∀𝑠 1            𝑠 1′ , ∃𝑠 2           𝑠 2′ , (𝑠 1′ , 𝑠 2′ ) ∈ next𝑒𝑅1,𝑒2 (𝜓 ) }
                         fe , 𝜈 .feF
   Theorem 4.5 (Soundness of fe). Let 𝜓 be a safety relation,
                                          (I1 , I2 ,𝜓 ) ∈ fe =⇒ |= ∀TS1 ∃TS2𝜓
  Proof. The proof follows exactly the same structure as for fei, we just slightly change the
abstract transition system. We extend the set of proof states to be Π , { (𝑠 1, 𝑠 2 , 𝜏1,𝜓 ) | 𝜏1 ∈
Traces(𝑠 1 ) ∧ (𝑠 1, 𝑠 2 ,𝜓 ) ∈ fe } and the transition relation is deﬁned as follows:
                                                   𝑒1                        𝑒2
                            𝜏1 = 𝑒 1𝜏1′       𝑠1        𝑠 1′        𝑠2             𝑠 2′       Δ𝑒1,𝑒2 (𝜓 ) ≠ ∅
                                                        𝑒2
                                    (𝑠 1, 𝑠 2, 𝜏1 ,𝜓 ) −→proof (𝑠 1′ , 𝑠 2′ , 𝜏1′ , Δ𝑒1,𝑒2 (𝜓 ))
Given two states and a safety relation 𝜓 such that (𝑠 1, 𝑠 2,𝜓 ) ∈ fe, and provided 𝜏1 ∈ Traces, we
can execute the abstract transition system from the initial proof state (𝑠 1, 𝑠 2, 𝜏1 ) to obtain a trace
𝜏2 . We pick 𝜏2 as a witness for the existential quantiﬁer. It remains to prove that (𝜏1, 𝜏2 ) ∈ 𝜓 . Since
𝜓 is a safety relation, by 4.3 it suﬃces to show (𝜏1 , 𝜏2 ,𝜓 ) ∈ safe. This fact is easily proven by
coinduction (exploiting (𝑠 1 , 𝑠 2,𝜓 ) ∈ fe and the fact that 𝜏2 is generated by executing the abstract
transition system deﬁned by →proof ).                                                                    

  As for fei, the deﬁnition of fe as a greatest ﬁxed point immediately gives us the ability to
perform incremental proofs by parameterized coinduction. To use fe in incremental proofs, we
redeﬁne our semantic quadruples using feF instead of feiF as the underlying functor:
                                𝐻 ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜓 } , (𝑠 1, 𝑠 2,𝜓 ) ∈ 𝐺 feF (𝐻 )
                                𝐻 ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜓 } , (𝑠 1, 𝑠 2,𝜓 ) ∈ 𝐻 ∪ 𝐺 feF (𝐻 )
  Note that here, 𝜓 is not just a relation between events, but a relation between inﬁnite traces. For
convenience, we also introduce the following sextuple:
                        𝐻 ⊢ 𝑒 1 ⊲ 𝑠 1 ∀ | 𝑒 2 ⊲ 𝑠 2 ∃ { 𝜓 } , (𝑠 1, 𝑠 2 ) ∈ next𝑒𝐻1,𝑒∪2 𝐺 feF (𝐻 ) (𝜓 )
    The corresponding reasoning rules are presented in Figure 3.
    The rules Init, Cycle, Step, and Invariant are similar to the ones of Figure 2. The main dif-
ference is that the Step rule suspends the proof temporarily by requiring us to check whether the
                         𝑒2 ′                                   𝑒1 ′
choice of transition 𝑠 2    𝑠 2 in reaction to a transition 𝑠 1    𝑠 1 is compatible with the safety relation
𝜓 . This is reﬂected by a premise of the form 𝐻 ⊢ 𝑒 1 ⊲ 𝑠 1 ∀ | 𝑒 2 ⊲ 𝑠 2 ∃ { 𝜓 } that can be discharged
using the rule Deriv. The rule Deriv requires us to prove two things:
  (1) 𝜓 should not be immediately violated by the choice of event 𝑒 2 ; formalized by Δ𝑒1,𝑒2 (𝜓 ) ≠ ∅
  (2) 𝜓 should not be violated later; formalized by 𝐻 ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { Δ𝑒1,𝑒2 (𝜓 ) }

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                            53:15


               Init                                                                          Cycle
               𝜓 is a safety relation                     ∅ ⊢ I1 ∀ | I2 ∃ { 𝜓 }                    (𝑠 1, 𝑠 2,𝜓 ) ∈ 𝐻
                                         |= ∀TS 1 ∃TS2𝜓                                          𝐻 ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 }

                              Step
                                     𝑒1                  𝑒2
                              ∀𝑠 1         𝑠 1′ , ∃𝑠 2        𝑠 2′ , 𝐻 ⊢ 𝑒 1 ⊲ 𝑠 1′ ∀ | 𝑒 2 ⊲ 𝑠 2′ ∃ { 𝜓 }
                                                         𝐻 ? ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 }

                      Invariant
                      (𝑠 1 , 𝑠 2,𝜓 ) ∈ 𝐻 ′           ∀(𝑠 1 , 𝑠 2,𝜓 ) ∈ 𝐻 ′ , 𝐻 ∪ 𝐻 ′ ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜓 }
                                                         𝐻 ? ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 }

                                Deriv
                                 Δ𝑒1,𝑒2 (𝜓 ) ≠ ∅                   𝐻 ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { Δ𝑒1,𝑒2 (𝜓 ) }
                                                  𝐻 ⊢ 𝑒1 ⊲ 𝑠1 ∀ | 𝑒2 ⊲ 𝑠2 ∃ { 𝜓 }

                                         Fig. 3. Incremental reasoning rules for fe



Note that the guard around 𝐻 is only released after an application of Deriv. In addition to the
rules presented in Figure 3, fe also inherits the Steps-L and Steps-R rules of fei (adapted to
triples (𝑠 1, 𝑠 2,𝜓 ) in an obvious way).

4.4 Handling Derivatives
While all rules presented in Figure 3 are sound, they can be diﬃcult to use in practice because
of the semantic treatment of derivatives (as opposed to a more syntactic one). First, the Deriv
rule requires us to prove the non-emptiness of a trace relation. Further, after a relation 𝜓 has
been derived, the proof focuses on a new relation Δ𝑒1,𝑒2 (𝜓 ). There is a priori no reason to believe
that Δ𝑒1,𝑒2 (𝜓 ) has been encountered before, and therefore, it is not obvious that it will later be
possible to use the rule Cycle to conclude the proof. Fortunately, when 𝜓 is expressed using LTL
modalities, there is a systematic way to determine an LTL representation of Δ𝑒1,𝑒2 (𝜓 ) by recursing
on the syntactic structure of the formula. Figure 4 describes how1 .
   We note that for temporal modalities and W, the original formula occurs as a subformula in
the derivative. In a sense, the Δ operator reveals the coinductive nature of these modalities. This
will help us closing cycles in proofs.

   Example 4.6. We consider the following transition systems:
                                TS 1 :                            TS 2 :
                                               𝑞0                             𝑠0     𝑎
                                                              𝑎                             𝑠1        𝑏


1 To the best of our knowledge, the notion of derivatives has never explicitly been formalized for LTL-deﬁned languages.

However, derivatives have been applied to languages over inﬁnite words expressed as omega-regular expressions [39].
Further, derivatives are easily recovered from the expansion laws of temporal modalities [3].


                                  Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:16                                                                                 Arthur Correnson and Bernd Finkbeiner



                                Δ𝑒1,𝑒2 ( 𝜓 ) ≡ Δ𝑒1,𝑒2 (𝜓 ) ∧ 𝜓
                           Δ𝑒1,𝑒2 (𝜓 1 ∧ 𝜓 2 ) ≡ Δ𝑒1,𝑒2 (𝜓 1 ) ∧ Δ𝑒1,𝑒2 (𝜓 2 )
                           Δ𝑒1,𝑒2 (𝜓 1 ∨ 𝜓 2 ) ≡ Δ𝑒1,𝑒2 (𝜓 1 ) ∨ Δ𝑒1,𝑒2 (𝜓 2 )
                           Δ𝑒1,𝑒2 (𝜓 1 W 𝜓 2 ) ≡ Δ𝑒1,𝑒2 (𝜓 2 ) ∨ [Δ𝑒1,𝑒2 (𝜓 1 ) ∧ (𝜓 1 W 𝜓 2 )]
                               Δ𝑒1,𝑒2 ( 𝜓 ) ≡ 𝜓
                                              
                                                true            if (𝑒 1 , 𝑒 1 ) ∈ 𝜑
                                 Δ𝑒1,𝑒2 (𝜑) ≡ false             otherwise

                               Fig. 4. Derivatives of common temporal modalities


We wish to prove |= ∀TS1 ∃TS2 (𝑎 1 ∧ 𝑎 2 ) W 𝑏 2 . We start by applying Init, followed by Step to match
the 𝑎-transition in TS 1 with an 𝑎-transition in TS 2 .
                          |= ∀TS1 ∃TS2 (𝑎 1 ∧ 𝑎 2 ) W 𝑏 2
                 ⇐=       ∅ ⊢ 𝑞 0 ∀ | 𝑠 0 ∃ { (𝑎 1 ∧ 𝑎 2 ) W 𝑏 2 }                                (by Init)
                 ⇐=       ∅ ⊢ 𝑎 ⊲ 𝑞 0 ∀ | 𝑎 ⊲ 𝑠 1 ∃ { (𝑎 1 ∧ 𝑎 2 ) W 𝑏 2 }                     (by Step)
To make further progress, we need to prove that emitting two 𝑎’s does not immediately violate the
current temporal relation. To do so, we apply the rule Deriv and we obtain
           Δ𝑎,𝑎 ((𝑎 1 ∧ 𝑎 2 ) W 𝑏 2 ) ≠ ∅ ∧ ∅ ⊢ 𝑞 0 ∀ | 𝑠 1 ∃ { Δ𝑒1,𝑒2 ((𝑎 1 ∧ 𝑎 2 ) W 𝑏 2 ) }       (by Deriv)
Using known derivatives (Figure 4), we can easily show that Δ𝑎,𝑎 ((𝑎 1 ∧𝑎 2 ) W 𝑏 2 ) ≡ (𝑎 1 ∧𝑎 2 ) W 𝑏 2 ≠ ∅.
After substituting the result of the derivative we are therefore left with the goal
                                         ∅ ⊢ 𝑞 0 ∀ | 𝑠 1 ∃ { (𝑎 1 ∧ 𝑎 2 ) W 𝑏 2 }
By Step we match an 𝑎-transition in TS 1 with a 𝑏-transition in TS 2 and we obtain
                              ∅ ⊢ 𝑎 ⊲ 𝑞 0 ∀ | 𝑏 ⊲ 𝑠 1 ∃ { (𝑎 1 ∧ 𝑎 2 ) W 𝑏 2 }        (by Step)
Again, by Deriv, we have to prove two goals:
           Δ𝑎,𝑏 ((𝑎 1 ∧ 𝑎 2 ) W 𝑏 2 ) ≠ ∅ ∧ ∅ ⊢ 𝑞 0 ∀ | 𝑠 1 ∃ { Δ𝑒1,𝑒2 ((𝑎 1 ∧ 𝑎 2 ) W 𝑏 2 ) }       (by Deriv)
Since Δ𝑎,𝑏 ((𝑎 1 ∧ 𝑎 2 ) W 𝑏 2 ) ≡ true ≠ ∅, it suﬃces to prove the following:
                                                ∅ ⊢ 𝑞 0 ∀ | 𝑠 1 ∃ { true }
Using Invariant we set the current coinduction hypothesis to be 𝐻 , { (𝑞 0 , 𝑠 1, true) }
                                    𝐻 ⊢ 𝑞 0 ∀ | 𝑠 1 ∃ { true }       (by Invariant)
By Step we again match an 𝑎-transition with a 𝑏-transition and we get
                                   𝐻 ⊢ 𝑎 ⊲ 𝑞 0 ∀ | 𝑏 ⊲ 𝑠 1 ∃ { true }        (by Step)
Since the derivative of true is true for any pair of events, by Deriv we obtain
                                       𝐻 ⊢ 𝑞 0 ∀ | 𝑠 1 ∃ { true }      (by Deriv)
Finally, since (𝑞 0, 𝑠 1 , true) ∈ 𝐻 , we can conclude using Cycle.                                                      
   While it is correct, the proof presented above suﬀers from several limitations.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                   53:17


   Limitation 1. Even though we purposely gave a very detailed proof, the example discussed above
still seems abnormally long. In particular, the last application of the rule Step seems redundant.
Indeed, if we look at the structure of the two transition systems, the proof should only have two
easy steps: one to match the 𝑎-transition with an 𝑎-transition, and a second one to match an 𝑎-
transition with a 𝑏-transition. More precisely, once we reached the goal ∅ ⊢ 𝑞 0 ∀ | 𝑠 1 ∃ { true },
we would like to be able to conclude right away. This goal should, in principle, immediately follow
from the previous and intuitively more diﬃcult goal ∅ ⊢ 𝑞 0 ∀ | 𝑠 1 ∃ { (𝑎 1 ∧ 𝑎 2 ) W 𝑏 2 }.
   Limitation 2. Another and more subtle concern is the fact that whenever we applied Deriv, we
had to explicitly compute the derivative of the current trace relation, and substitute the result
back in the current goal. Substituting a relation with an equivalent one is not an issue when doing
informal reasoning in set theory; however, in type-theory based proof assistants such as Coq, this
is not possible in general. By default, we can only substitute a relation for another one if both
relations are equal in the sense of propositional equality. One solution would be to assume the
axiom of predicate extensionality that precisely stipulates that two equivalent predicates are also
equal.
Axiom 1 (Predicate Extensionality). Let 𝑃, 𝑄 ∈ P (𝐴) be predicates over 𝐴, then 𝑃 ≡ 𝑄 =⇒ 𝑃 =
𝑄.
  Note however that this approach is not entirely satisfactory as it would make our development
depends on a second axiom in addition to functional choice.

4.5   Strengthening Is All We Need
Instead of relying on additional axioms, a more general solution to address the two limitations
presented in the previous section is to prove once and for all that our coinductive relation supports
the following strengthening rule:
                                      Strengthen
                                      𝜓′ ⊆ 𝜓          𝐻 ? ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 ′ }
                                                𝐻 ? ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 }
Note that the two question marks in Strengthen should be interpreted as follows: the rule can be
applied both when 𝐻 is guarded or unguarded, but it never modiﬁes the guard (in particular, if the
hypothesis was guarded, it remains guarded). The addition of Strengthen would clearly solve
the ﬁrst limitation we discussed: it can factor redundant proof steps by reusing results already
established for stronger trace relations. Further, it also solves the substitution problem. Indeed,
substituting a trace relation with an equivalent one is just a special case of strengthening.
   Unfortunately, with our current deﬁnition of semantic quadruples, Strengthen is unsound. To
understand why, let us ﬁrst observe that the following weaker version of the rule is sound:
                                      𝜓′ ⊆ 𝜓           ∅ ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 ′ }
                                                𝐻 ? ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 }
Note that in this variant, 𝐻 is replaced by ∅ after applying the rule! In other words, if we need to
prove 𝐻 ? ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜓 }, it suﬃces to prove that the property holds for a stronger trace relation
𝜓 ′ ⊆ 𝜓 , but at the cost of forgetting all knowledge previously accumulated in the proof. This
essentially ruins the beneﬁts of having an incremental proof system. Intuitively the reason why
we need to reset 𝐻 is that the triples we explore during the proof of 𝐻 ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜓 ′ } are not
necessarily the same as the triples explored during a proof of 𝐻 ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜓 }. In particular,
instead of considering the successive derivatives of 𝜓 , we are instead considering the successive

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:18                                                                                      Arthur Correnson and Bernd Finkbeiner


derivatives of 𝜓 ′ . In turn, if we use 𝐻 to reason about triples emanating from (𝑠 1, 𝑠 2 ,𝜓 ′ ), there is no
reason to believe that the same reasoning carries over to triples emanating from (𝑠 1, 𝑠 2,𝜓 ) without
further assumptions. Fortunately, we can slightly generalize our coinductive relation in such a way
that Strengthen (in its more general version) is provably sound, and all other proof rules remain
valid as well. The next section discusses this generalization.
   For now, let us assume that Strengthen is sound. Using the equivalences listed in Figure 4,
Strengthen can be combined with Deriv to obtain a set of rules for handling temporal modalities.
Figure 5 presents a selection of such rules.


                 Deriv-                                                      Deriv-
                  (𝑒 1, 𝑒 2 ) ∈ 𝜑         𝐻 ⊢ 𝑠1 ∀ | 𝑠2 ∃ {      𝜑}          𝜓≠∅             𝐻 ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 }
                         𝐻 ⊢ 𝑒1 ⊲ 𝑠1 ∀ | 𝑒2 ⊲ 𝑠2 ∃ {       𝜑}                  𝐻 ⊢ 𝑒1 ⊲ 𝑠1 ∀ | 𝑒2 ⊲ 𝑠2 ∃ {     𝜓}

        Deriv-W-Now                                                   Deriv-W-Later
        (𝑒 1 , 𝑒 2 ) ∈ 𝜑 2          𝐻 ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { true }        (𝑒 1 , 𝑒 2 ) ∈ 𝜑 1      𝐻 ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜑1 W 𝜑2 }
             𝐻 ⊢ 𝑒1 ⊲ 𝑠1 ∀ | 𝑒2 ⊲ 𝑠2 ∃ { 𝜑1 W 𝜑2 }                            𝐻 ⊢ 𝑒1 ⊲ 𝑠1 ∀ | 𝑒2 ⊲ 𝑠2 ∃ { 𝜑1 W 𝜑2 }

                                     Fig. 5. Selection of proof rules for temporal modalities




5     Up-to Techniques
5.1      Reasoning Up-to Stronger Trace Relations
Often times, we have a goal of the form 𝐻 ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜓 } where the triple (𝑠 1, 𝑠 2,𝜓 ) almost
belongs to 𝐻 (which would allow us to conclude using the rule Cycle), but not exactly. In other
words, we would like to be able to reason up to slight enlargements of the coinduction hypothesis
[36]. As discussed in the previous section, a typical occurrence of this pattern is when we have a
goal of the form 𝐻 ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜓 } but 𝐻 only contains (𝑠 1 , 𝑠 2,𝜓 ′ ) for some stronger relation
𝜓 ′ ⊂ 𝜓 . In [34] and [35], Pous developed systematic ways to soundly integrate up-to techniques in
coinductive proofs. Building on these ideas, Zakowski et al. later showed that the parameterized
greatest ﬁxed point operator 𝐺 can be generalized to support up-to techniques as well as other
enhancements [43]. This generalization, usually referred to as GPACO, preserves the ability to
perform incremental proofs. The reasoning rules of GPACO are presented in Figure 6. We note that
the original deﬁnition by Zakowski et al. is more involved, and we refer the readers to [43] for a
more in-depth presentation. However, our Coq development relies on an instance of GPACO which
exposes exactly the simpliﬁed interface described in Figure 6. Contrary to standard parameterized
coinduction, GPACO explicitly marks when the current assumption can be used or not: we note
 𝐺 𝐹 (𝐻 ) when the assumption 𝐻 is guarded, and 𝐺 𝐹 (𝐻 ) when it is unguarded. When proof rules
can be applied regardless of whether the coinduction hypothesis is guarded or not, we note 𝐺 𝐹? (𝐻 ).
   As for parameterized coinduction (Figure 1), the rule Step releases the guard. When the current
hypothesis is unguarded, the rule Cycle can be invoked to conclude a proof. Finally, the rule Up-to
enables up-to reasoning. The idea is that given an operator clo that satisﬁes a certain compatibility
criterion (Formally, clo is compatible with 𝐹 iﬀ clo ◦ 𝐹 ⊆ 𝐹 ◦ clo [35]), the goal 𝑋 ⊆ 𝐺 ? (𝐻 ) can be
replaced by the hopefully simpler goal 𝑋 ⊆ clo(𝐺 ? (𝐻 )). Typically, we choose clo to be a closure
operator (hence the naming convention clo) so that clo(𝐺 ? (𝐻 )) is larger than 𝐺 ? (𝐻 ). To support

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                              53:19


                        Init                     Step                            Accumulate
                        𝑋 ⊆ 𝐺 𝐹 (∅)               𝑋 ⊆ 𝐹 ( 𝐺 𝐹 (𝐻 ) )              𝑋 ⊆ 𝐺 𝐹 (𝑋 ∪ 𝐻 )
                               𝑋 ⊆ 𝜈 .𝐹              𝑋 ⊆ 𝐺 𝐹? (𝐻 )                    𝑋 ⊆ 𝐺 𝐹? (𝐻 )

                                    Cycle                       Up-to
                                          𝑋 ⊆𝐻                  clo is compatible with 𝐹
                                    𝑋 ⊆ 𝐺 𝐹 (𝐻 )                 clo(𝐺 𝐹? (𝐻 )) ⊆ 𝐺 𝐹? (𝐻 )


                                                  Fig. 6. Rules of GPACO


up-to techniques, we redeﬁne our semantic tuples using GPACO as follows:
                                     𝐻 ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜓 } , (𝑠 1, 𝑠 2,𝜓 ) ∈ 𝐺 feF (𝐻 )
                                     𝐻 ⊢ 𝑠 1 ∀ | 𝑠 2 ∃ { 𝜓 } , (𝑠 1, 𝑠 2,𝜓 ) ∈ 𝐺 feF (𝐻 )
                                                                                  𝐺 feF (𝐻 )
                         𝐻 ⊢ 𝑒 1 ⊲ 𝑠 1 ∀ | 𝑒 2 ⊲ 𝑠 2 ∃ { 𝜓 } , (𝑠 1, 𝑠 2 ) ∈ next𝑒1,𝑒2       (𝜓 )
   All the reasoning rules previously introduced are preserved by this change. However, this gen-
eralization naturally inherits the Up-to rule. In particular, it allows us to reason up to stronger
trace relations. The associated closure operator strclo is deﬁned as follows:
                               strclo(𝐻 ) , { (𝑠 1, 𝑠 2,𝜓 ) | ∃𝜓 ′ ⊆ 𝜓, (𝑠 1, 𝑠 2,𝜓 ′ ) ∈ 𝐻 }
    By deﬁnition, to prove that a triple (𝑠 1, 𝑠 2 ,𝜓 ) belongs to strclo(𝐻 ), it suﬃces to prove that
(𝑠 1, 𝑠 2,𝜓 ′ ) is in 𝐻 for some relation 𝜓 ′ ⊆ 𝜓 . Importantly, we observe that strclo is compatible
with the monotone functor feF. Consequently, Strengthen is just an instance of Up-to with feF
as the underlying functor, and strclo as the (compatible) closure operator.

5.2   Reasoning Up-to Simulation
To prove a universal trace property ∀TS𝜓 , it suﬃces to show that the property hold for any superset
𝑇 ⊇ Traces(TS). Dually, to prove an existential trace property ∃TS𝜓 , it suﬃces to show that the
property holds for a subset 𝑇 ⊆ Traces(TS). In turn, to prove a ∀∃ hyperproperty, it suﬃces to con-
sider an over-approximation of the universally quantiﬁed traces and an under-approximation of
the existentially quantiﬁed traces. In some cases, reasoning about approximated sets of traces can
greatly simplify proofs. This intuition about traces can be lifted at the level of states if we consider
simulation instead of trace inclusion. In particular, our coinductive relation can be equipped with
the following sound rules:
         Sim-L                                                       Sim-R
          (𝑠 1, 𝑠 1′ ) ∈ sim       𝐻 ? ⊢ 𝑠 1′ ∀ | 𝑠 2 ∃ { 𝜓 }         (𝑠 2′ , 𝑠 2 ) ∈ sim     𝐻 ? ⊢ 𝑠 1 ∀ | 𝑠 2′ ∃ { 𝜓 }
                      𝐻 ? ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 }                                     𝐻 ? ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 }
These rules can be used at any point in a proof to replace a state with a similar state of our choice.
The soundness of Sim-L and Sim-R is immediately obtained from Up-to by reasoning up to simu-
lation. We deﬁne the corresponding (compatible) closure operator as follows:
           simclo(𝐻 ) , { (𝑠 1, 𝑠 2 ) | ∃(𝑠 1′ , 𝑠 2′ ), (𝑠 1, 𝑠 1′ ) ∈ sim ∧ (𝑠 2′ , 𝑠 2 ) ∈ sim ∧ (𝑠 1′ , 𝑠 2′ ) ∈ 𝐻 }
  We refer the readers to our Coq development for a proof that simclo is compatible with feF.
Since simulation is just a special instance of fe with 𝜓 = eq, we note that the simulation rules

                                   Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:20                                                                                     Arthur Correnson and Bernd Finkbeiner


can be reformulated purely in terms of our semantic quadruples as follows:
Sim-L (internalized)                                                   Sim-R (internalized)
 ∅ ⊢ 𝑠 1 ∀ | 𝑠 1′ ∃ {   eq }        𝐻 ? ⊢ 𝑠 1′ ∀ | 𝑠 2 ∃ { 𝜓 }          ∅ ⊢ 𝑠 2′ ∀ | 𝑠 2 ∃ {   eq }      𝐻 ? ⊢ 𝑠 1 ∀ | 𝑠 2′ ∃ { 𝜓 }
                  𝐻 ? ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 }                                                𝐻 ? ⊢ 𝑠1 ∀ | 𝑠2 ∃ { 𝜓 }

6 From ∀∃ to ∀∗ ∃∗
In the previous sections, we focused exclusively on hyperproperties with one universal quanti-
ﬁer followed by one existential quantiﬁer. We note that our coinductive relations can naturally
be extended to support the more general case of hyperproperties of the form ∀∗ ∃∗ (i.e., 0 or more
universal quantiﬁers followed by 0 or more existential quantiﬁers). Given a family of 𝑚 + 𝑛 tran-
sition systems TS 1, . . . , TS𝑛+𝑚 such that TS𝑖 = (S𝑖 , E𝑖 , I𝑖 , →𝑖 ) for all 0 ≤ 𝑖 ≤ 𝑛 + 𝑚, we deﬁne the
coinductive relation hyco𝑚,𝑛 ⊆ S1 × . . . × S𝑛+𝑚 × P (E1𝜔 × . . . × E𝑛+𝑚     𝜔 ) as follows:

             hycoF𝑚,𝑛 (𝑅) , { (𝑠 1, . . . 𝑠𝑚 , 𝑠𝑚+1 , . . . , 𝑠𝑚+𝑛 ) |
                                           𝑒1                    𝑒𝑚                𝑒𝑚+1 ′               𝑒𝑚+𝑛 ′
                                    ∀𝑠 1        𝑠 1′ . . . ∀𝑠𝑚         ′
                                                                      𝑠𝑚 , ∃𝑠𝑚+1       𝑠𝑚+1 . . . ∃𝑠𝑚+𝑛     𝑠𝑚+𝑛 ,
                                    Δ𝑒1,...,𝑒𝑛+𝑚 (𝜓 ) ≠ ∅ ∧ (𝑠 1′ , . . . , 𝑠𝑚+𝑛
                                                                             ′
                                                                                 , Δ𝑒1,...,𝑒𝑛+𝑚 (𝜓 )) ∈ 𝑅 }
The associated greatest ﬁxed point hyco𝑚,𝑛 , 𝜈 .hycoF𝑚,𝑛 gives a sound proof technique for ∀∗ ∃∗
hyperproperties.
   Theorem 6.1. Let 𝜓 ⊆ P (E1𝜔 × . . . × E𝑛+𝑚
                                          𝜔 ) be a (𝑚 + 𝑛)-ary safety relation. Then,

                    (I1 , . . . , I𝑚+𝑛 ,𝜓 ) ∈ hyco𝑚,𝑛 =⇒ |= ∀TS1 . . . ∀TS𝑚 ∃𝑇 𝑆𝑚+1 . . . ∃TS𝑚+𝑛 𝜓

7 Proving Temporal Hyperproperties of Imperative Programs with I/O
So far, we have introduced a general framework to prove ∀∃ hyperproperties with a safety relation
between the universal and existential traces. In this section, we show that this framework natu-
rally applies to the veriﬁcation of imperative programs with inputs, outputs, and nondeterminism
(IMPio ).

7.1 An Imperative Programming Language with Nondeterminism and I/O
IMPio programs support inﬁnite loops, inputs, outputs, conditionals, and nondeterministic gener-
ation of constant values. The syntax is described in Figure 7.


            𝑃 ::= loop 𝑃 | if 𝑐 then 𝑃 else 𝑃 | input 𝑥 | output 𝑒 | havoc 𝑥 | 𝑃 ; 𝑃 | 𝑥 := 𝑒

                  𝑒 ::= 𝑥 | 𝑒 + 𝑒 | 𝑒 - 𝑒 | 0 | 1 | 2 | ...             𝑐 ::= true | false | e < 𝑒 | 𝑒 = 𝑒 | ...

                                                    Fig. 7. Syntax of IMPio


   In Figure 7, 𝑥 denotes a variable drawn from a set of program variables X, 𝑃 denotes a program,
𝑒 an arithmetic expression, and 𝑐 a boolean expression. Given a memory 𝑚 : X → Z, we denote
by È𝑒É𝑚 ∈ Z (resp. È𝑐É𝑚 ∈ {true, false}) the value of arithmetic (resp. boolean) expressions. We in-
terpret IMPio programs as labeled transition systems by giving a small-step operational semantics
which, in turn, naturally induces a trace semantics.
   We note that havoc and input have the same eﬀect on the memory, but input eﬀects are
recorded in program traces, whereas havoc is used to model silent nondeterministic assignments

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                   53:21


            Loop                                       Continue

             hloop 𝑃, 𝑚i → h𝑃; loop 𝑃, 𝑚i               h(𝑃1 ; 𝑃2 ) ; 𝑃3 , 𝑚i → h𝑃1 ; (𝑃2 ; 𝑃3 ), 𝑚i

            Input                                                Output
                                𝑣∈Z                                            𝑣 = È𝑒É𝑚
                                  in(𝑣)                                                 out(𝑣)
             hinput 𝑥 ; 𝑃, 𝑚i −−−−→ h𝑃, 𝑚[𝑥 ← 𝑣]i                houtput 𝑒 ; 𝑃, 𝑚i −−−−−→ h𝑃, 𝑚i

             Havoc                                             Assign
                                𝑣∈Z                                          𝑣 = È𝑒É𝑚
              hhavoc 𝑥 ; 𝑃, 𝑚i → h𝑃, 𝑚[𝑥 ← 𝑣]i                 h𝑥 := 𝑒 ; 𝑃, 𝑚i → h𝑃, 𝑚[𝑥 ← 𝑣]i

            Ite-true                                         Ite-false
                         È𝑐É𝑚 = true                                       È𝑐É𝑚 = false
            hif 𝑐 then 𝑃1 else 𝑃2 , 𝑚i → h𝑃1 , 𝑚i             hif 𝑐 then 𝑃1 else 𝑃2 , 𝑚i → h𝑃2 , 𝑚i

                                     Fig. 8. Operational semantics of IMPio


and does not emit any event. Further, since we are considering only truly reactive programs, we
do not assign a meaning to basic instructions when they are not followed by more instructions
(see rules Input, Output, Havoc, and Assign). Such programs would not have any inﬁnite trace
anyway.

7.2 A Deductive System for Hyperproperties of Imperative Programs
Let P be the set of all programs, S , P × Z X be the set of all program states (pairs of a program
and a memory), and E , {in(𝑥) | 𝑥 ∈ Z} ∪ {out(𝑥) | 𝑥 ∈ Z} be the set of possible events emitted
by IMP io programs. Any program 𝑃 can be viewed as labeled transition system TS𝑃 , (S, E, I𝑃 , →
) where → is the small-step operational semantics of IMPio , and I𝑃 , h𝑃, _ ↦→ 0i is the state
initiating the execution of 𝑃 in a zero-initialized memory. In the following, we will write 𝑃 for TS𝑃 .
In this setting, we can immediately use our coinductive relation fe to verify hyperproperties of
programs. Nonetheless, instead of reasoning with the high-level rules presented in the previous
sections, we can exploit the syntactic structure of programs to obtain more convenient reasoning
rules as well as dedicated proof tactics. Figure 9 presents a selection of such reasoning rules. Many
more can be derived.
Proof Management. The ﬁrst rule, Init, exploits the soundness of fe (Theorem 4.5) to initialize a
proof by parameterized coinduction. The second rule, Memory-Invariant, is derived from Invari-
ant and allows to extend the current coinduction hypothesis with a relation that should hold for
every pairs of memories from the point of application on. Importantly, contrary to the Invariant
rule (see Figure 3), where the extension of the coinduction hypothesis refers to states of the under-
lying LTSs, Memory-Invariant is restricted to invariants that only refer to the memories of the
two programs (ignoring the code of the programs themselves, and the current temporal relation 𝜓 ).
This is not a hard restriction (we could still use the more general rule), but we adopt this version
for convenience as it is relatively unusual to allow invariants to refer to the syntactic structure of
a program or to a logical speciﬁcation. A memory-invariant INV is lifted to a relation on triples in
a natural way. More concretely, we deﬁne
                     INV @(𝑃1 , 𝑃2 ,𝜓 ) , { (h𝑃1 , 𝑚 1 i, h𝑃2 , 𝑚 2 i,𝜓 ) | (𝑚 1 , 𝑚 2 ) ∈ INV }

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:22                                                                          Arthur Correnson and Bernd Finkbeiner


The rule Memory-Invariant extends the current coinduction hypothesis with INV @(𝑃1 , 𝑃2 ,𝜓 ),
allowing to ﬁnish a proof at a later point if we cycle back to a state where the same pair of programs
has to be matched with the same temporal relation 𝜓 .
Handling I/O. To handle inputs and outputs, we introduce two specialized rules Input-input and
output-output. These rules are exploiting the fact that if the next instruction to be executed in
both programs is an I/O operation, the only way to make progress is to ensure that any event
produced by the left-hand program can be matched with a corresponding event in the right-hand
program. Once the appropriate event for the right-hand program has been chosen, the new goal
is guarded by a next operator, forcing us to compute the derivative of the current property 𝜓 and
prove that it is not trivially violated.
Handling Nondeterminism. Nondeterministic assignments are covered by the rules Havoc-L and
Havoc-R. When the next instruction to execute in the left-hand program is a nondeterministic
assignment of 𝑥, Havoc-L requires us to consider an arbitrary new value 𝑣 for 𝑥 (i.e., the new goal is
guarded by a universal quantiﬁcation over 𝑣). Dually, the rule Havoc-R handles nondeterministic
assignments in the right-hand program by requiring us to choose a new value 𝑣 for 𝑥 (i.e., the
new goal is guarded by an existential quantiﬁcation over 𝑣). The rules Havoc-R and Havoc-L are
derived from the more general Steps-L and Steps-R and from the operational semantics of IMPio .
Handling Loops. To handle loops, one could simply use the rules Steps-L and Steps-R to unfold
a loop either in the right-hand or the left-hand program. However, we almost always wish to
establish an invariant when a loop is encountered. The rules Loop-L and Loop-R combine an
application of Steps-L (or Steps-R) with an application of Memory-Invariant to simultaneously
unfold loops and establish a new memory-invariant.
Handling Derivatives. We note that after applying I/O rules, the new goals are always of the form
 𝐻 ⊢ . . . ⊲ . . . ∀ | . . . ⊲ . . . ∃ { 𝜓 }, forcing us to derive the current relation 𝜓 to check that the emitted
events are not immediately violating it. To do so, we use the rules for derivatives introduced in
Figure 5.




Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                    53:23




                                               Proof Management

                              Init
                              𝜓 is a safety relation            ∅ ⊢ I𝑃1 ∀ | I𝑃2 ∃ { 𝜓 }
                                                      |= ∀𝑃1 ∃𝑃2𝜓

    Memory-Invariant
    (𝑚 1 , 𝑚 2 ) ∈ INV       ∀(𝑚 1, 𝑚 2 ) ∈ INV , 𝐻 ∪ INV @(𝑃1 , 𝑃2 ,𝜓 ) ⊢ h𝑃1 , 𝑚 1 i ∀ | h𝑃2 , 𝑚 2 i ∃ { 𝜓 }
                                         𝐻 ⊢ h𝑃1 , 𝑚 1 i ∀ | h𝑃2 , 𝑚 2 i ∃ { 𝜓 }


                                                          I/O
           Input-input
           ∀𝑣 1, ∃𝑣 2, 𝐻 ⊢ in(𝑣 1 ) ⊲ h𝑃1 , 𝑚 1 [𝑥 1 ↦→ 𝑣 1 ]i ∀ | in(𝑣 2 ) ⊲ h𝑃2 , 𝑚 2 [𝑥 2 ↦→ 𝑣 2 ]i ∃ { 𝜓 }
                           𝐻 ⊢ hinput 𝑥 1 ; 𝑃1 , 𝑚 1 i ∀ | hinput 𝑥 2 ; 𝑃2 , 𝑚 2 i ∃ { 𝜓 }

                     Output-output
                      𝐻 ⊢ out(È𝑒 1 É𝑚1 ) ⊲ h𝑃1 , 𝑚 1 i ∀ | out(È𝑒 2 É𝑚2 ) ⊲ h𝑃2 , 𝑚 2 i ∃ { 𝜓 }
                         𝐻 ⊢ houtput 𝑒 1 ; 𝑃1 , 𝑚 1 i ∀ | houtput 𝑒 2 ; 𝑃2 , 𝑚 2 i ∃ { 𝜓 }


                                                Nondeterminism
   Havoc-L                                                    Havoc-R
   ∀𝑣, 𝐻 ⊢ h𝑃1 , 𝑚 1 [𝑥 ↦→ 𝑣]i ∀ | h𝑃2 , 𝑚 2 i ∃ { 𝜓 }        ∃𝑣, 𝐻 ⊢ h𝑃1 , 𝑚 1 i ∀ | h𝑃2 , 𝑚 2 [𝑥 ↦→ 𝑣]i ∃ { 𝜓 }
     𝐻 ⊢ hhavoc 𝑥 ; 𝑃1 , 𝑚 1 i ∀ | h𝑃2 , 𝑚 2 i ∃ { 𝜓 }          𝐻 ⊢ h𝑃1 , 𝑚 1 i ∀ | hhavoc 𝑥 ; 𝑃2 , 𝑚 2 i ∃ { 𝜓 }


                                                        Loops

       Loop-L
                                          (𝑚 1, 𝑚 2 ) ∈ INV
       ∀(𝑚 1 , 𝑚 2 ) ∈ INV , 𝐻 ∪ INV @(loop 𝑃1 , 𝑃2 ,𝜓 ) ⊢ h𝑃1 ; loop 𝑃1 , 𝑚 1 i ∀ | h𝑃2 , 𝑚 2 i ∃ { 𝜓 }
                                     𝐻 ⊢ hloop 𝑃1 , 𝑚 1 i ∀ | h𝑃2 , 𝑚 2 i ∃ { 𝜓 }

       Loop-R
                                             (𝑚 1, 𝑚 2 ) ∈ INV
       ∀(𝑚 1 , 𝑚 2 ) ∈ INV , 𝐻 ∪ INV @(𝑃1 , loop 𝑃2 ,𝜓 ) ⊢ h𝑃1 ; loop 𝑃1 , 𝑚 1 i ∀ | h𝑃2 , 𝑚 2 i ∃ { 𝜓 }
                                     𝐻 ⊢ hloop 𝑃1 , 𝑚 1 i ∀ | h𝑃2 , 𝑚 2 i ∃ { 𝜓 }


                                     Fig. 9. Selection of proof rules for IMPio




                                Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:24                                                                          Arthur Correnson and Bernd Finkbeiner


7.3 Examples in Coq
  Example 7.1. Consider the following example of a simple echo server:
                                                       loop
                                              echo:      input 𝑥
                                                         output 𝑥
   We use HyCo to prove that for all executions of echo, there exists another execution such
that the outputs of the second execution are always exactly the double of the outputs in the ﬁrst
execution. The inputs are never compared. Formally, we prove ∀echo ∃echo double where double ,
{ (𝑒 1 , 𝑒 2 ) | 𝑒 1 = out(𝑥) =⇒ 𝑒 2 = out(2 ∗ 𝑥) }. The proof script (slightly simpliﬁed for readability)
corresponding to the proof of this example is the following:
                                  Proof.
                                    hyco_init. hyco_sync. hyco_step.
                                    intros v1. exists (2 * v1).
                                    hyco_deriv. hyco_step.
                                      ...
                                    hyco_cycle.
                                  Qed.
   In this script, the tactic hyco_init exploits the rule Init to initialize a proof by coinduction.
It also implicitly uses the rule Invariant to add the initial states to the current coinduction hy-
pothesis. The tactic hyco_sync then steps through the execution of the two programs until both
reach an I/O instruction. In our case, the programs are executed until their ﬁrst input instruction.
The tactic hyco_step determines which I/O rule should be applied to make further progress in the
coinductive proof. Gere, Input-input is selected and it remains to match any input 𝑣 1 with some
input 𝑣 2 . We pick 𝑣 2 = 2∗𝑣 1 . After choosing an appropriate input, we need to check that this choice
is compatible with the current trace relation by computing its derivative. The tactic hyco_deriv
selects the appropriate derivation rule (see Figure 5). Here, the rule Deriv- is applied and requires
us to prove that the two outputs out(𝑣 1 ) and out(2 ∗ 𝑣 1 ) are satisfying the event-invariant double.
This fact is trivially proven by unfolding the deﬁnition of double and reading the current content
of the memories. Finally, the tactic hyco_cycle terminates the proof by applying the coinduction
hypothesis. Indeed, after completing one iteration of the loop, the two programs remaining to be
executed are again two copies of echo, and the property we need to verify is still double; we
cycled back to the initial state of the proof. We note that the repeated use of the tactics hyco_sync
and hyco_step could be partially automated, allowing us to focus only on the interesting part of
the proof: picking the appropriate input for the right-hand program.

   Example 7.2. We describe a second example that requires us to use the rule Invariant as well
as the alignment rules discussed in Section 3.3. We consider the two following programs incr and
ndet_add:
                                                                      𝑥 := 0
                                 𝑥 := 0
                                                                      loop
                                 loop
                           incr:                            ndet_add:    havoc 𝑦
                                    𝑥 := 𝑥 + 1
                                                                         𝑥 := 𝑥 + 𝑦
                                    output 𝑥
                                                                         output 𝑥
  As for the previous example, we wish to verify ∀incr ∃ndet_add                double. The corresponding proof
script is presented below.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                   53:25

                   Proof.
                     hyco_init.
                     hyco_left 2. hyco_right 2.
                     hyco_invariant (fun m1 m2 => 2 * m1 "x" = m2 "x").
                       ...
                     hyco_left 3. hyco_right 3.
                     apply (hyco_havoc_r 2). hyco_right 2.
                     hyco_step.
                     ... rewrite <- INV. ...
                     hyco_cycle.
                     ... rewrite <- INV. ...
                   Qed.
   The proof starts by executing both programs until the beginning of the loop is reached. To do so,
we use the tactics hyco_left and hyco_right. These tactics exploit the rules Steps-L and Steps-R
(see section 3.3) to perform 𝑛 silent computation steps in the left-hand or the right-hand program.
Once the beginning of both loops is reached, we use the tactic hyco_invariant to establish the
memory-invariant 𝑥 2 = 2 ∗ 𝑥 1 . After proving that the invariant is satisﬁed initially, we again step
through the programs and we resolve the nondeterministic assignment havoc 𝑦 from the right-
hand program by choosing 𝑦 = 2. Note that at this point of the proof, the left-hand program is
ready to emit an output while the right-hand program still needs to update its variable 𝑥. We
use the tactic hyco_right to align both programs, and the tactic hyco_step to match the two
outputs. We note that in order to be able to prove that the event-invariant double is preserved
after emitting the outputs, we critically need to use the memory-invariant (this corresponds to the
instruction rewrite <- INV in the script). Once we proved that the event-invariant is maintained,
we can conclude the proof with an application of hyco_cycle.

8   Related Work and Discussion
8.1 Game-Based Verification of Hyperliveness
Our approach is connected to a game-theoretic interpretation of hyperproperties introduced by
Coenen et al. [18]. In their approach, the task of verifying a ∀∃ property is viewed as a game be-
tween a universal player, and an existential player. The moves of the universal player correspond to
transitions in the left-hand system, and the existential player is forced to answer with correspond-
ing transitions in the right-hand system. The existential player wins the game if there is a strategy
to answer any move of the universal player without immediately violating the speciﬁcation. In
that case, the targeted hyperproperty holds. In the coalgebraic reading we presented in this paper,
the greatest ﬁxed point 𝜈 .feF can be interpreted as the winning region of the game: the set of game
states from which the existential player is guaranteed to win.
   Originally, the game-based approach was introduced with the goal of automating the veriﬁca-
tion of ∀∃ temporal hyperproperties. The key insight is that when the systems being veriﬁed are
ﬁnite-state, the game arena can be eﬀectively constructed and sent to an eﬃcient game solver. In
the case of inﬁnite-state systems described by programs, the arena cannot be constructed explicitly
and we need to resort to ﬁnite approximations in order to automatically solve the game. For exam-
ple, Beutner and Finkbeiner [12] used predicate abstraction to construct a ﬁnite approximation of
the game.
   An important advantage of the coalgebraic approach over the game-based approach is that it
does not require us to explicitly construct an approximation of the the game. Instead, we implicitly
deﬁne the exact wining region as a coinductive relation. This allows us to leverage parameterized

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:26                                                                          Arthur Correnson and Bernd Finkbeiner


coinduction as a deductive system to prove that the existential player has a winning strategy. Fur-
thermore, by embedding our coalgebraic approach in a proof assistant such as Coq, we immediately
beneﬁt from its rich logic and its ecosystem of mathematical libraries to reason about the game.

8.2     Program Logics for Hyperproperties
There is a long tradition of verifying relational properties of sequential programs using extensions
of Hoare logics (cf. [33]). Relational Hoare Logic (RHL) was originally introduced by Benton [9] and
later extended to higher-order programs [1], separation logic [42], probabilistic computations [6],
and quantum computations [7, 40]. D’Osualdo et al. introduced hyper-triples [22] as a unifying
compositional building block for proofs of 𝑘-hypersafety properties. Cartesian hoare logic [38] is
a sound and relatively complete calculus for 𝑘-safety properties.
   Most relational logics are restricted to properties that express a condition over a given set of
programs or a 𝑘-fold self-composition of some program for some ﬁxed 𝑘. Some extensions that
go beyond 𝑘-safety are directed at speciﬁc properties such as diﬀerential privacy [8] and sensitiv-
ity [5]. There are also several extensions that provide more general support for ∀∃ hyperproperties.
Dardinier and Müller [20] introduced Hyper Hoare Logic, a generalization of Hoare logic that lifts
assertions to properties of arbitrary sets of states. Hyper Hoare Logic can reason about both the
absence and the existence of combinations of executions. Other extensions to ∀∃ hyperproper-
ties include Forall-Exist Hoare Tuples (FEHT) [10], reﬁnement quadruples [4] and RHLE triples [21].
Some of these approaches have been mechanized in a proof assistant (cf. [20]). However, all these
approaches are limited to the analysis of pre-post style relational speciﬁcations. Unlike our ap-
proach, they are thus are not well-suited to reason about reactive systems whose executions are
inherently inﬁnite. By contrast, the coalgebraic approach goes beyond pre-post style speciﬁcations
to reason about inﬁnite sequences of events.

8.3     Mechanized Frameworks for Simulation Proofs
Interaction Trees (ITrees) [41] have recently been introduced as a general-purpose coinductive
structure to model potentially non-terminating computations within the Coq proof assistant. Sev-
eral approaches have been developed to establish trace inclusion (resp. equivalence) between
ITrees using simulation (resp. bisimulation) techniques [15, 43]. Similar to the framework pre-
sented in this paper, these approaches are based on variants of parameterized coinduction. How-
ever, they do not support temporal reasoning. An interesting and natural direction would be to
apply our approach to the veriﬁcation of temporal hyperproperties of programs modeled as ITrees.
   Another Coq-based framework for simulation proofs is Simuliris [27]. It combines Iris [30],
a powerful concurrent separation logic, with simulation techniques. While Simuliris does not
target temporal hyperproperties, integrating our framework within a separation logic in a simi-
lar way is an interesting research direction. It would enable intuitive reasoning about temporal
hyperproperties of heap-manipulating programs.

9     Conclusion
We have presented HyCo, a mechanized framework for the veriﬁcation of temporal hyperprop-
erties within the Coq proof assistant. Our approach provides a foundation for the construction
of trustworthy proofs of temporal hyperproperties in complex reactive systems. Since we use the
full logic of Coq as the underlying assertion language, the expressiveness of the hyperproperties
considered here is far beyond the scope of currently available automated approaches. In particular,
HyCo can easily be applied to new programming languages and new temporal logics.
   In future work, we plan to build on our framework to design a fully-featured mechanized
program logic for temporal hyperproperties of reactive systems. Another important direction is

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                       53:27


to investigate the completeness of the approach. It is well-known that the game-theoretic ap-
proach is incomplete in general [18]. For ﬁnite-state systems, the problem has been mitigated by
adding prophecy variables that inform the existential player about future choices of the universal
player [11]. Our proof system would likely beneﬁt from the introduction of prophecy variables in
a similar manner.

Data Availability
The Coq development accompanying this paper is available on GitHub at the following address:
                               https://github.com/acorrenson/hyco-popl-2025
   Additionally, an archive containing the development version at the time this paper was submit-
ted, together with detailed installation and evaluation instructions, can be found on Zenodo at the
following address [19]:
                                     https://zenodo.org/records/14055009

Acknowledgements
This work was supported by the European Research Council (ERC) Grant HYPER (No. 101055412).
Views and opinions expressed are however those of the authors only and do not necessarily reﬂect
those of the European Union or the European Research Council Executive Agency. Neither the
European Union nor the granting authority can be held responsible for them. A. Correnson carried
out this work as a member of the Saarbrücken Graduate School of Computer Science.

References
 [1] Alejandro Aguirre, Gilles Barthe, Marco Gaboardi, Deepak Garg, and Pierre-Yves Strub. 2019. A relational logic for
     higher-order programs. J. Funct. Program. 29 (2019), e16. https://doi.org/10.1017/S0956796819000145
 [2] Timos Antonopoulos, Paul Gazzillo, Michael Hicks, Eric Koskinen, Tachio Terauchi, and Shiyi Wei. 2017. Decomposi-
     tion instead of self-composition for proving the absence of timing channels. In Proceedings of the 38th ACM SIGPLAN
     Conference on Programming Language Design and Implementation, PLDI 2017, Barcelona, Spain, June 18-23, 2017, Albert
     Cohen and Martin T. Vechev (Eds.). ACM, 362–375. https://doi.org/10.1145/3062341.3062378
 [3] Christel Baier and Joost-Pieter Katoen. 2008. Principles of model checking. MIT Press, 249–253.
 [4] Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2013. Beyond 2-Safety: Asymmetric Product Programs for Re-
     lational Program Veriﬁcation. In Logical Foundations of Computer Science, Sergei Artemov and Anil Nerode (Eds.).
     Springer Berlin Heidelberg, Berlin, Heidelberg, 29–43.
 [5] Gilles Barthe, Thomas Espitau, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2018. Proving expected sensitiv-
     ity of probabilistic programs. Proc. ACM Program. Lang. 2, POPL (2018), 57:1–57:29. https://doi.org/10.1145/3158145
 [6] Gilles Barthe, Benjamin Grégoire, and Santiago Zanella Béguelin. 2009. Formal certiﬁcation of code-based cryp-
     tographic proofs. In Proceedings of the 36th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Lan-
     guages, POPL 2009, Savannah, GA, USA, January 21-23, 2009, Zhong Shao and Benjamin C. Pierce (Eds.). ACM, 90–101.
     https://doi.org/10.1145/1480881.1480894
 [7] Gilles Barthe, Justin Hsu, Mingsheng Ying, Nengkun Yu, and Li Zhou. 2020. Relational proofs for quantum programs.
     Proc. ACM Program. Lang. 4, POPL (2020), 21:1–21:29. https://doi.org/10.1145/3371089
 [8] Gilles Barthe, Boris Köpf, Federico Olmedo, and Santiago Zanella Béguelin. 2013. Probabilistic Relational Reasoning
     for Diﬀerential Privacy. ACM Trans. Program. Lang. Syst. 35, 3 (2013), 9:1–9:49. https://doi.org/10.1145/2492061
 [9] Nick Benton. 2004. Simple relational correctness proofs for static analyses and program transformations. In Proceed-
     ings of the 31st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2004, Venice, Italy,
     January 14-16, 2004, Neil D. Jones and Xavier Leroy (Eds.). ACM, 14–25. https://doi.org/10.1145/964001.964003
[10] Raven Beutner. 2024. Automated Software Veriﬁcation of Hyperliveness. In Tools and Algorithms for the Construc-
     tion and Analysis of Systems - 30th International Conference, TACAS 2024, Held as Part of the European Joint Confer-
     ences on Theory and Practice of Software, ETAPS 2024, Luxembourg City, Luxembourg, April 6-11, 2024, Proceedings,
     Part II (Lecture Notes in Computer Science, Vol. 14571), Bernd Finkbeiner and Laura Kovács (Eds.). Springer, 196–216.
     https://doi.org/10.1007/978-3-031-57249-4_10


                                 Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
53:28                                                                              Arthur Correnson and Bernd Finkbeiner


[11] R. Beutner and B. Finkbeiner. 2022. Prophecy Variables for Hyperproperty Veriﬁcation. In 2022 2022 IEEE 35th
     Computer Security Foundations Symposium (CSF) (CSF). IEEE Computer Society, Los Alamitos, CA, USA, 471–485.
     https://doi.org/10.1109/CSF54842.2022.9919658
[12] Raven Beutner and Bernd Finkbeiner. 2022. Software Veriﬁcation of Hyperproperties Beyond k-Safety. In Com-
     puter Aided Veriﬁcation - 34th International Conference, CAV 2022, Haifa, Israel, August 7-10, 2022, Proceedings,
     Part I (Lecture Notes in Computer Science, Vol. 13371), Sharon Shoham and Yakir Vizel (Eds.). Springer, 341–362.
     https://doi.org/10.1007/978-3-031-13185-1_17
[13] Raven Beutner and Bernd Finkbeiner. 2023. AutoHyper: Explicit-State Model Checking for HyperLTL. In Tools and
     Algorithms for the Construction and Analysis of Systems - 29th International Conference, TACAS 2023, Held as Part of the
     European Joint Conferences on Theory and Practice of Software, ETAPS 2022, Paris, France, April 22-27, 2023, Proceedings,
     Part I (Lecture Notes in Computer Science, Vol. 13993), Sriram Sankaranarayanan and Natasha Sharygina (Eds.). Springer,
     145–163. https://doi.org/10.1007/978-3-031-30823-9_8
[14] Janusz A. Brzozowski. 1964.          Derivatives of Regular Expressions.        J. ACM 11, 4 (oct 1964), 481–494.
     https://doi.org/10.1145/321239.321249
[15] Minki Cho, Youngju Song, Dongjae Lee, Lennard Gäher, and Derek Dreyer. 2023. Stuttering for Free. Proc. ACM
     Program. Lang. 7, OOPSLA2, Article 281 (oct 2023), 28 pages. https://doi.org/10.1145/3622857
[16] Michael R. Clarkson, Bernd Finkbeiner, Masoud Koleini, Kristopher K. Micinski, Markus N. Rabe, and César Sánchez.
     2014. Temporal Logics for Hyperproperties. In Proc. POST. 265–284.
[17] Michael R. Clarkson and Fred B. Schneider. 2008. Hyperproperties. In 2008 21st IEEE Computer Security Foundations
     Symposium. 51–65. https://doi.org/10.1109/CSF.2008.7
[18] Norine Coenen, Bernd Finkbeiner, César Sánchez, and Leander Tentrup. 2019. Verifying Hyperliveness. In Com-
     puter Aided Veriﬁcation - 31st International Conference, CAV 2019, New York City, NY, USA, July 15-18, 2019, Proceed-
     ings, Part I (Lecture Notes in Computer Science, Vol. 11561), Isil Dillig and Serdar Tasiran (Eds.). Springer, 121–139.
     https://doi.org/10.1007/978-3-030-25540-4_7
[19] Arthur Correnson. 2024. Coinductive Proofs for Temporal Hyperliveness. https://doi.org/10.5281/zenodo.14055009
[20] Thibault Dardinier and Peter Müller. 2024. Hyper Hoare Logic: (Dis-)Proving Program Hyperproperties. Proc. ACM
     Program. Lang. 8, PLDI, Article 207 (jun 2024), 25 pages. https://doi.org/10.1145/3656437
[21] Robert Dickerson, Qianchuan Ye, Michael K. Zhang, and Benjamin Delaware. 2022. RHLE: Modular Deductive Ver-
     iﬁcation of Relational ∀∃ Properties. In Programming Languages and Systems: 20th Asian Symposium, APLAS 2022,
     Auckland, New Zealand, December 5, 2022, Proceedings (Auckland, New Zealand). Springer-Verlag, Berlin, Heidelberg,
     67–87. https://doi.org/10.1007/978-3-031-21037-2_4
[22] Emanuele D’Osualdo, Azadeh Farzan, and Derek Dreyer. 2022. Proving hypersafety compositionally. Proc. ACM
     Program. Lang. 6, OOPSLA2, Article 135 (oct 2022), 26 pages. https://doi.org/10.1145/3563298
[23] Javier Esparza, Peter Lammich, René Neumann, Tobias Nipkow, Alexander Schimpf, and Jan-Georg Smaus. 2013. A
     Fully Veriﬁed Executable LTL Model Checker. In Computer Aided Veriﬁcation, Natasha Sharygina and Helmut Veith
     (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 463–478.
[24] Azadeh Farzan and Anthony Vandikas. 2019. Automated Hypersafety Veriﬁcation. In Computer Aided Ver-
     iﬁcation - 31st International Conference, CAV 2019, New York City, NY, USA, July 15-18, 2019, Proceedings,
     Part I (Lecture Notes in Computer Science, Vol. 11561), Isil Dillig and Serdar Tasiran (Eds.). Springer, 200–218.
     https://doi.org/10.1007/978-3-030-25540-4_11
[25] Azadeh Farzan and Anthony Vandikas. 2020. Reductions for safety proofs. Proc. ACM Program. Lang. 4, POPL (2020),
     13:1–13:28. https://doi.org/10.1145/3371081
[26] Bernd Finkbeiner, Markus N. Rabe, and Cesar Sanchez. 2015. Algorithms for Model Checking HyperLTL and Hyper-
     CTL*. In Proc. CAV, 2015.
[27] Lennard Gäher, Michael Sammler, Simon Spies, Ralf Jung, Hoang-Hai Dang, Robbert Krebbers, Jeehoon Kang, and
     Derek Dreyer. 2022. Simuliris: a separation logic framework for verifying concurrent program optimizations. Proc.
     ACM Program. Lang. 6, POPL, Article 28 (jan 2022), 31 pages. https://doi.org/10.1145/3498689
[28] Tzu-Han Hsu, César Sánchez, and Borzoo Bonakdarpour. 2021. Bounded Model Checking for Hyperproperties. In
     Tools and Algorithms for the Construction and Analysis of Systems - 27th International Conference, TACAS 2021, Held as
     Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2021, Luxembourg City, Luxembourg,
     March 27 - April 1, 2021, Proceedings, Part I (Lecture Notes in Computer Science, Vol. 12651), Jan Friso Groote and
     Kim Guldstrand Larsen (Eds.). Springer, 94–112. https://doi.org/10.1007/978-3-030-72016-2_6
[29] Chung-Kil Hur, Georg Neis, Derek Dreyer, and Viktor Vafeiadis. 2013. The power of parameterization in coin-
     ductive proof. In Proceedings of the 40th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Program-
     ming Languages (Rome, Italy) (POPL ’13). Association for Computing Machinery, New York, NY, USA, 193–206.
     https://doi.org/10.1145/2429069.2429093



Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
Coinductive Proofs for Temporal Hyperliveness                                                                         53:29


[30] Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. 2015.
     Iris: Monoids and Invariants as an Orthogonal Basis for Concurrent Reasoning. In Proceedings of the 42nd Annual
     ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (Mumbai, India) (POPL ’15). Association
     for Computing Machinery, New York, NY, USA, 637–650. https://doi.org/10.1145/2676726.2676980
[31] Leslie Lamport and Fred B. Schneider. 2021.            Verifying Hyperproperties With TLA. In 34th IEEE Com-
     puter Security Foundations Symposium, CSF 2021, Dubrovnik, Croatia, June 21-25, 2021. IEEE, 1–16.
     https://doi.org/10.1109/CSF51468.2021.00012
[32] John McLean. 1994. A General Theory of Composition for Trace Sets Closed Under Selective Interleaving Functions.
     In Proc. IEEE Symposium on Security and Privacy. 79–93.
[33] David A. Naumann. 2020. Thirty-Seven Years of Relational Hoare Logic: Remarks on Its Principles and History. In
     Leveraging Applications of Formal Methods, Veriﬁcation and Validation: Engineering Principles, Tiziana Margaria and
     Bernhard Steﬀen (Eds.). Springer International Publishing, Cham, 93–116.
[34] Damien Pous. 2007. Complete Lattices and Up-To Techniques. In Programming Languages and Systems, Zhong Shao
     (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 351–366.
[35] Damien Pous. 2016. Coinduction All the Way Up. In Proceedings of the 31st Annual ACM/IEEE Symposium on Logic
     in Computer Science (New York, NY, USA) (LICS ’16). Association for Computing Machinery, New York, NY, USA,
     307–316. https://doi.org/10.1145/2933575.2934564
[36] Damien Pous and Davide Sangiorgi. 2011. Enhancements of the bisimulation proof method. Cambridge University
     Press, 233–289.
[37] Ron Shemer, Arie Gurﬁnkel, Sharon Shoham, and Yakir Vizel. 2019. Property Directed Self Composition. In Com-
     puter Aided Veriﬁcation - 31st International Conference, CAV 2019, New York City, NY, USA, July 15-18, 2019, Proceed-
     ings, Part I (Lecture Notes in Computer Science, Vol. 11561), Isil Dillig and Serdar Tasiran (Eds.). Springer, 161–179.
     https://doi.org/10.1007/978-3-030-25540-4_9
[38] Marcelo Sousa and Isil Dillig. 2016. Cartesian hoare logic for verifying k-safety properties. SIGPLAN Not. 51, 6 (jun
     2016), 57–69. https://doi.org/10.1145/2980983.2908092
[39] Peter Thiemann and Martin Sulzmann. 2015. From 𝜔-Regular Expressions to Büchi Automata via Partial Derivatives.
     In Language and Automata Theory and Applications, Adrian-Horia Dediu, Enrico Formenti, Carlos Martín-Vide, and
     Bianca Truthe (Eds.). Springer International Publishing, Cham, 287–298.
[40] Dominique Unruh. 2019. Quantum relational Hoare logic. Proc. ACM Program. Lang. 3, POPL (2019), 33:1–33:31.
     https://doi.org/10.1145/3290346
[41] Li-yao Xia, Yannick Zakowski, Paul He, Chung-Kil Hur, Gregory Malecha, Benjamin C. Pierce, and Steve Zdancewic.
     2019. Interaction trees: representing recursive and impure programs in Coq. Proc. ACM Program. Lang. 4, POPL,
     Article 51 (dec 2019), 32 pages. https://doi.org/10.1145/3371119
[42] Hongseok Yang. 2007.            Relational separation logic.       Theor. Comput. Sci. 375, 1-3 (2007), 308–334.
     https://doi.org/10.1016/j.tcs.2006.12.036
[43] Yannick Zakowski, Paul He, Chung-Kil Hur, and Steve Zdancewic. 2020. An equational theory for weak bisimulation
     via generalized parameterized coinduction. In Proceedings of the 9th ACM SIGPLAN International Conference on Certi-
     ﬁed Programs and Proofs (New Orleans, LA, USA) (CPP 2020). Association for Computing Machinery, New York, NY,
     USA, 71–84. https://doi.org/10.1145/3372885.3373813

Received 2024-07-11; accepted 2024-11-07




                                 Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 53. Publication date: January 2025.
