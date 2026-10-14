                                            TREBL – A RELATIVE COMPLETE TEMPORAL EVENT-B LOGIC
                                                               PART I: THEORY

                                                    KLAUS-DIETER SCHEWE a , FLAVIO FERRAROTTI b , PETER RIVIÈRE a,c ,
                                                 NEERAJ KUMAR SINGH a , GUILLAUME DUPONT a , AND YAMINE AÏT AMEUR                                                       a


                                            a
                                                 Institut Nationale Polytechnique de Toulouse / ENSEEIHT, Toulouse, France
arXiv:2509.01462v5 [cs.LO] 2 Oct 2026




                                                 e-mail address: kd.schewe@gmail.com, {nsingh|yamine}@enseeiht.fr, guillaume.dupont@toulouse-inp.fr
                                             b
                                                 Software Competence Centre Hagenberg, Hagenberg, Austria
                                                 e-mail address: flavio.ferrarotti@scch.at
                                             c
                                                 Japan Advanced Institute of Science and Technology, Ishikawa, Japan
                                                 e-mail address: priviere@jaist.ac.jp


                                                    Abstract. The verification of liveness conditions is an important aspect of state-based
                                                    rigorous methods. This article addresses the extension of the logic of Event-B to a powerful
                                                    logic, in which properties of traces of an Event-B machine can be expressed. However,
                                                    all formulae of this logic are still interpreted over states of an Event-B machine rather
                                                    than traces. The logic exploits that for an Event-B machine M a state S determines all
                                                    traces of M starting in S. We identify a fragment called TREBL of this logic, in which all
                                                    liveness conditions of interest can be expressed, and define a set of sound derivation rules
                                                    for the fragment. We further show relative completeness of these derivation rules in the
                                                    sense that for every valid entailment of a formula φ one can find a derivation, provided
                                                    the machine M is sufficiently refined. The decisive property is that certain variant terms
                                                    must be definable in the refined machine. We show that such refinements always exist.
                                                    Throughout the article several examples from the field of security are used to illustrate the
                                                    theory.




                                                                                        Introduction
                                        State-based consistency conditions such as state or transition invariants are included in
                                        rigorous state-based methods such as B [Abr10a], Abstract State Machines (ASMs) [BS03],
                                        TLA+ [Lam02] or Event-B [Abr10b], just to mention the most important ones. The
                                        verification of such conditions is well supported by appropriate logics such as the logics for
                                           Key words and phrases: Event-B, logic of Event-B, temporal logic, liveness, variants, verification, relative
                                        completeness.
                                           The research of Flavio Ferrarotti has been funded by the Federal Ministry for Innovation, Mobility and
                                        Infrastructure (BMIMI), the Federal Ministry for Economy, Energy and Tourism (BMWET), and the State
                                        of Upper Austria in the frame of the COMET Module Dependable Production Environments with Software
                                        Security (DEPS) (FFG grant no. 888338) and the SCCH competence center INTEGRATE (FFG grant no.
                                        892418) in the COMET - Competence Centers for Excellent Technologies Programme managed by Austrian
                                        Research Promotion Agency FFG. .
                                           Part of this work is supported by the ANR project EBRP: EventB-Rodin-Plus under grant no. ANR-19-
                                        CE25-0010.


                                        Preprint submitted to                                    © K.-D. Schewe, F. Ferrarotti, P. Rivière, N. K. Singh, G. Dupont, and Y. Aït Ameur
                                        Logical Methods in Computer Science                      ⃝
                                                                                                 CC Creative Commons
2




Event-B [Sch12], TLA+ [Mer03], deterministic ASMs [SN01] and arbitrary non-deterministic
ASMs [FSTW18]. As the logics are definitional extensions of first-order logic with types,
they are complete [Vää24], which is a valuable asset for verification.
     It is important to note that in these logics not only conditions over states can be
expressed, but arbitrary conditions over finite sequences of states. However, the formulae
are interpreted over states. This reflects the basic property of rigorous state-based methods
that a state determines the traces starting in that state. For instance, for Event-B it is easy
to express the firing of a particular event by means of a transition invariant.
     Besides such consistency conditions other liveness conditions are likewise important.
These conditions comprise among others (conditional) progress, i.e. any state satisfying a
condition φ is always followed eventually (i.e. some time later) by a state satisfying ψ (for
φ = true we obtain unconditional progress, which is usually called existence), or persistence,
i.e. eventually a condition φ will hold forever. Fairness is a specific progress condition,
in which ψ is a transition condition expressing the firing of an event. The verification of
liveness conditions requires reasoning about complete traces of a specification, i.e. they are
intrinsically connected to temporal logic [KM08].
     Specific temporal logics that have been introduced for the verification of desirable liveness
properties of sequential and concurrent (interleaved) systems are Linear-Time Temporal Logic
(LTL) [Pnu77] and Computation Tree Logic (CTL) [CE82]. For many liveness conditions it
suffices to consider only the UNTIL-fragment of LTL [MP84]. These logics, however, have
been defined as temporal propositional logics, hence their expressiveness is limited: formulae
are built over a fixed, finite set of atomic propositions, and a state is simply an assignment
of truth values to these propositions. As a consequence, a transition condition that relates
the value of a variable ranging over an unbounded domain across two consecutive states
cannot be expressed directly. For instance, if an event performs the assignment x := x + 1
for a variable x ranging over the natural numbers, this cannot be captured by a single
LTL or CTL formula. Indeed an atomic proposition describes a property of one state in
isolation, so relating the value of x before and after the transition would require a separate
case for every possible value of x, i.e. infinitely many cases. In particular, they require
extensions when used in connection with any of the rigorous methods mentioned above, the
states of which are given by typed variables ranging over arbitrary, possibly infinite domains.
The same applies to extensions of these temporal logics such as HyperLTL, HyperCTL,
HyperCTL∗ emphasising variables for runs and quantification over them [CFK+ 14] as well
as TeamLTL and TeamCTL emphasising team semantics, i.e. the interpretation of formulae
over arbitrary sets of runs [GMOV22]. Although these logics add quantification over traces
or team semantics over sets of traces, their atomic propositions remain of the same fixed,
Boolean kind, so the limitation illustrated above persists for them as well.
     Hoang and Abrial started to investigate the use of the UNTIL-fragment of LTL in
connection with Event-B [HA11]. Based on their work Rivière et al. provided a tool support
using the EB4EB meta-theory in combination with RODIN [RSAD23]. Defining a logic that
integrates LTL with the logic of Event-B is rather straightforward; instead of propositions,
formulae that can be defined for a given Event-B machine need to be considered. In doing
so, NEXT-formulae are already covered by the logic of Event-B, and hence the omission of
the NEXT modal operator does no harm1.


    1Note that a similar argument is used for the logic of TLA+ [Mer03].
                                                                                                                    3




     Naturally, this integration yields a first-order modal logic (called LTL(EB) in [FRS+ 24]),
which cannot be complete. Nonetheless, Hoang and Abrial discovered a few derivation rules
for invariance, existence, progress and persistence and proved their soundness, thus showing
that if certain variant terms can be derived in an Event-B machine, such liveness properties
can be verified. However, the decisive remaining question is, if there exists a set of derivation
rules that is also complete, at least for a well-defined fragment of LTL(EB).
     In [FRS+ 24] Ferrarotti et al. approached this problem by defining a fragment □LTL
of LTL(EB) using the type of formulae in invariance, existence, progress and persistence
conditions as defining constructors. This enabled the soundness proofs from [HA11] to be
preserved with slight generalisations. In addition, a few standard derivation rules for modal
formulae were added, and it was shown that the set of all these derivation rules is relative
complete for the □LTL fragment, a problem that was left open in [HA11]. The meaning of
relative completeness is that all valid formulae are derivable, if appropriate variant terms can
be defined in Event-B machines. Furthermore, it was possible to prove that such variants
always exist in conservatively refined machines. The proof of relative completeness was
possible under the assumption that the machines are tail-homogeneous, which means that
the intrinsic non-determinism in Event-B is restricted. The tail-homogeneity restriction is
necessary, as a linear time temporal logic does not work well together with branching traces.
That is, the logic □LTL is sound and relative complete for proofs on sufficiently refined,
tail-homogeneous Event-B machines.

Rationale and Scope. Classical temporal logics such as LTL, CTL, CTL∗ , etc. are
complete—for instance, it is well known that LTL can be embedded into monadic first-order
logic—but their propositional nature severely limits their expressiveness for the verification
of liveness properties in connection with state-based rigorous methods such as B [Abr10a],
Abstract State Machines (ASMs) [BS03], TLA+ [Lam02] or Event-B [Abr10b]. If instead we
consider temporal extensions of (at least) first-order logic, we obtain significantly enlarged
temporal logics, but it is well known that such temporal logics cannot be complete. This
choice between Scylla and Charybdis—lack of expressiveness or incompleteness—is seriously
hampering verification of conditions that concern complete traces for any rigorous systems
specifications.
     At the core of the problem we find that temporal formulae are interpreted over arbitrary
traces, i.e. sequences of states that are defined as propositional theories over some fixed
signature2, with only few general restrictions. In rigorous state-based methods, however,
there is no interest in arbitrary traces, but in traces that are defined by a specification.
Therefore, the general idea is to combine non-propositional temporal logic with a restriction
of interpretations to traces defined by a machine (specified by one of these methods). Better
than this, the means for the specification of state transitions can be integrated into the
logic—so the logic becomes even more powerful—and temporal formulae can be simply
defined as shortcuts. Consequently, the interpretation over traces can be replaced by an
interpretation over states (the start states of the traces). The details of this approach will
be presented and discussed in this article.
     The most important consequence of this idea is that it allows us to prove relative
completeness, where “relative” refers to assumptions about the specified machines, which
can always be satisfied. This is the key problem addressed in this article. While we develop
   2That is, we assume a fixed finite set {p , . . . , p } of propositional variables, and a state (also called world)
                                             1       n
is given by assigning truth values to these variables.
4




the theory on grounds of the Event-B method [Abr10b], the general idea applies to other
state-based rigorous methods as well. In fact, the integration of update sets and their effects
is an intrinsic component of the logic of Abstract State Machines [FSTW18], but as long
as the method provides a logic, in which properties of states and state transitions can be
expressed, and permits the definition of update sets, it should not be a problem to adapt
the results of this article accordingly. This has already been sketched for Abstract State
Machines [FRS+ 24], and it should also be possible to define relative complete temporal
logics for B, TLA+ and other methods.


Contribution of this Article. As emphasised above, the key problems to be addressed in
a temporal Event-B logic are expressiveness and completeness. In particular, it is desirable
to preserve a key feature of the logic of Event-B, i.e. to enable reasoning over traces without
having to introduce traces as first-class objects in the logic. The objective of this article is
therefore to polish and extend the work on the complete fragment of LTL(EB) [FRS+ 24],
in particular to get rid of restrictions concerning the (relative) completeness results, to
highlight the applicability of the resulting temporal Event-B logic. In a forthcoming second
part we will show how the logic can be effectively supported by the EB4EB meta-theory in
connection with the RODIN tool. As reported in [RSAD23] this has already been done for
the fragment of the logic considered in [FRS+ 24].
     Concerning expressiveness we pick up a key idea from related work on ASMs. Differences
between states are captured by update sets and these can also be made explicit for any pairs
of states of an Event-B machine. Likewise, we can define the effect of an update set in the
logic of Event-B, i.e. we can introduce formulae ψ = [X]φ that express that after firing an
update set X a given formula φ holds. Such update sets can even be extended from state
transitions to transitions by multiple steps, and quantification over the number of states can
be enabled.
     Note that this defines a very powerful logic, in which arbitrary conditions over traces
can be expressed, an approach that Lamport characterised as “evil” [Lam10]. However,
as in [FS24] we only intend to exploit this logic to define the common temporal operators
as shortcuts; all derivation rules can then be expressed over a sufficiently large temporal
fragment. The advantage is that as for the logic of Event-B all formulae of the temporal
fragment will be interpreted over states rather than traces, which allows us to solve the
completeness problem.
     Therefore, a key contribution is the definition of common temporal operators (ALWAYS
□, EVENTUALLY ♢, UNTIL U) in the extension of the logic of Event-B. Then temporal
formulae express properties of traces of Event-B machines, but are interpreted over states,
which reflects the simple fact that a state of a given Event-B machine determines the set of
traces starting in that state. We can also distinguish formulae that are to hold in all traces
from those that are to hold in one trace or a selected set of traces. In doing so, the temporal
semantics exploited in [HA11, FRS+ 24] is nonetheless preserved.
     We proceed defining the TempoRal Event-B Logic (TREBL) as the fragment spanned
by formulae of the logic of Event-B for a given machine and selected temporal operators. For
this logic derivation rules are formulated, and their soundness is proven, which is just a slight
generalisation of the work by Hoang and Abrial [HA11], and Ferrarotti et al. [FRS+ 24].
Some of these derivation rules involve variant terms, i.e. terms that take values in some
well-founded set.
                                                                                                 5




     Finally, we prove the relative completeness of the defined set of derivation rules, i.e.
every valid formula can also be derived, provided that the machine is “sufficiently refined”,
meaning that all necessary variant terms can be defined. A key step in the proof is to show
that it is always possible to obtain such refinements.
     We demonstrate the application of TREBL and its supporting tool using challenging
desired properties in security. For instance, we see that in TREBL the non-interference
problem [Bis09, McL92] can be expressed by a rather simple invariance condition with a state
transition formula, whereas in logics such as LTL, CTL and the like transition conditions
can hardly be expressed.
     The research reported in this article is a significant extension of previous work [FRS+ 24].
The logic has been extended to capture not only conditions that are to hold in all traces,
but also those that are to hold in just one or in a well-defined subset of traces. All proofs
are included, and the restrictions in the previously obtained relative completeness result in
[FRS+ 24] have been removed.

Organisation of the Article. In Section 1 we introduce TREBL. As in [FRS+ 24] we first
give a brief introduction of the logic of Event-B, and highlight specific formulae for state
transitions, deadlock-freeness and event firing. Then we define the extensions mentioned
above concerning update sets and effects of update sets with respect to single and multiple
steps. This is used to define temporal operators as shortcuts of complex formulae of the
extended Event-B logic, which gives rise to the definition of the temporal fragment TREBL.
We show that by comparison with the semantics used in [HA11, FRS+ 24] we do not lose
anything, but gain the interpretability of TREBL-formulae over states rather than traces.
We show the usefulness of TREBL by several sophisticated examples with preference on
security conditions.
    Section 2 is dedicated to the soundness of TREBL. First we introduce several types of
variant terms that allow certain temporal formulae to be derived. We complement variants
for convergence and divergence by variants for eventuality. We prove that there always
exist refinements in which needed variant terms can be defined, which shows that the
corresponding temporal formulae can be mechanically proven, provided that appropriate
variants are defined. We proceed with derivation rules for TREBL and the proof of their
soundness, which slightly generalises the work in [HA11, FRS+ 24] and adopts extensions
from [FS24].
    In Section 3 we show the relative completeness of the set of derivation rules, which
generalises the main result of [FRS+ 24] and at the same time removes the restriction that
traces must be tail-homogeneous. We illustrate the theory for selected application examples.
    Section 4 provides a brief discussion of previous and related work, before we conclude
with a summary and valuation of the main results.


                            1. The Temporal Event-B Logic
The logic of Event-B is the result of integrating set theory and first-order logic (or equivalently
exploiting monadic second-order logic with definable sets, i.e. Henkin semantics). Formulae
in the logic are always interpreted over states. We assume familiarity with the well-known
Event-B method [Abr10b], and only recall some basic concepts fixing the notation needed in
the remainder of this article. Different to our approach in the previous conference paper
[FRS+ 24] we first extend the logic of Event-B in such a way that conditions over traces of a
6




machine can be expressed, while the interpretation over states is preserved. Then common
temporal operators can be expressed as shortcuts of this extended logic. Nonetheless, the
semantics used in [FRS+ 24, HA11] is preserved. Then TREBL is defined as a fragment of
this extended Event-B logic.

1.1. A Glimpse of Event-B. The basic schema views an Event-B machine as offering a set
of events E (operations), which are executed one at a time, i.e. only one event can be fired
at any time point. Events are usually parameterised, which results in invariant-preserving
state transitions. The firing of events is the only means for updating states.
     A state in Event-B is formed by a finite tuple of variables v̄ taking values in certain sets
with (explicitly or implicitly defined) auxiliary functions and predicates. We write valS (v)
for the value of the state variable v ∈ v̄ in the state S. Sets are usually specified in an
Event-B context, but syntactical details are of no importance here.
     Each event ei ∈ E has the form any x̄ where Gi (x̄, v̄) then Ai (x̄, v̄, v̄ ′ ) end, where x̄ are
the parameters, the first-order formula Gi (x̄, v̄) is the guard and Ai (x̄, v̄, v̄ ′ ) is the action
of ei .
     An event ei is enabled in state S with variables v̄, if there are values for its parameters
x̄ that make its guard Gi (x̄, v̄) hold in S. Otherwise, the event is disabled. If all events of a
machine M are disabled in a state S, then M is said to be deadlocked in S.
     An Event-B action Ai (x̄, v̄, v̄ ′ ) is a list of assignments of the form
                                   v1 , . . . , vn : | P (x̄, v̄, (v1′ , . . . , vn′ )) ,
where the vi are variables that occur in the tuple v̄ of state variables and P is a before-
after predicate relating the values of vi (before the action) and vi′ (after the action). The
values assigned to the vi are chosen non-deterministically3 from the set of values (v1′ , . . . , vn′ )
that satisfy P (x̄, v̄, (v1′ , . . . , vn′ )). Thus, each action Ai (x̄, v̄, v ′ ) corresponds to a before-
after predicate PAi (x̄, v̄, v̄ ′ ) formed by the conjunction of all before-after predicates of the
assignments in Ai (x, v̄, (v1′ , . . . , vn′ )). These predicates are defined using the language of set
theory, i.e. first order logic with the binary relation-symbol ∈. There are several dedicated
notations for (typed) set operations such as set comprehension, Cartesian product, etc. We
do not discuss them here as they are definable in first-order logic and well known.
     An action also allows assignments of the form v := E(x̄, v̄) and v :∈ E(x̄, v̄), where
E(x̄, v̄) is an expression. The assignment v := E(x̄, v̄) deterministically assigns the value of
E(x̄, v̄) to v, while v :∈ E(x̄, v̄) non-deterministically assigns an element of the set E(x̄, v̄)
to v. However, these two assignments are merely shortcuts of assignments in the general
form v : | P (x̄, v̄, v ′ ) with before-after predicates v ′ = E(x̄, v̄) and v ′ ∈ E(x̄, v̄), respectively.
     The values of the variables in the initial state are set by means of a special event called
init that has no parameters nor guard. The values that variables v̄ can take in a state
are constrained by invariants I(v̄). These invariants are to hold in every reachable state,
which is achieved by proving that they are established by the initialisation event init and
subsequently preserved by all other events.
     Given an event e, we say that a state S ′ is an e-successor state of S, if S ′ is a possible
after-state of the firing of e from the before-state S. Lifting the definition to a machine M ,
we say that S ′ is an M -successor state of S if there exists an event e of M such that S ′ is
an e-successor of S.
    3It is commonly assumed that this choice is external, i.e. the values are provided by the environment and
not by the machine itself.
                                                                                                               7




      Event-B defines a trace τ of a machine M as a (possibly infinite) sequence of states
S0 , S1 , S2 , . . . such that S0 is an initial state satisfying the after predicate defined by the
event init, and for every pair of consecutive states Si , Si+1 in τ , there is an event e such
that Si+1 is an e-successor state of Si . If the computation τ ends in a state Sn , i.e. the
computation terminates, then M must be deadlocked in Sn . For a trace τ = S0 , S1 , . . . let
ℓ(τ ) = n, if τ is finite and has length n, and let ℓ(τ ) = ω if it is infinite. Furthermore, let
τ (k) for 0 ≤ k ≤ ℓ(τ ) denote the sequence Sk , Sk+1 , . . . obtained from τ by removing its first
k elements.


1.2. The Logic of Event-B. Given a machine M we immediately obtain a logic L, in
which properties of M can be expressed. If the state variables of M are v̄, then the set
of basic well-formed formulae of L consists of the set of first-order logic formulae over the
signature τ of the machine M with all free variables among those in v̄. Such formulae are
interpreted in any state S of M , where the value of the free (state) variables is interpreted
by the value of these variables in S. That is, in L we can express properties of states4, and
such formulae are commonly referred to as the state formulae of M .
     We adopt common notation and write S |= φ iff the formula φ ∈ L holds in the state
S. Note that this requires that the free variables of φ are among the state variables v̄. A
particular case arises for sentences: if φ does not contain free variables, its validity does not
depend on the state S.
     For an arbitrary set Φ of L formulae we write S |= Φ iff S |= φ holds for all φ ∈ Φ.
Furthermore, Φ |= ψ holds (for ψ ∈ L and Φ ⊆ L) iff whenever S |= Φ holds, then also S |= ψ
holds. For the special case Φ = ∅ all states S satisfy all formulae in Φ, so ∅ |= ψ—abbreviated
as |= ψ—simply means that all states S satisfy ψ.
     We write M |= φ iff the initial state of the machine M satisfies the formula φ. Note
again that for sentences φ we have M |= φ iff |= φ holds, i.e. the validity of the formula is
independent from the states under consideration.
     Let E and v̄ denote the set of events and the sequence of state variables of an Event-
B machine M . For each ei ∈ E let Gi (x̄, v̄) and PAi (x̄, v̄, v̄ ′ ) denote the guard and the
before-after predicate corresponding to the action Ai (x̄, v̄, v̄ ′ ) of event ei , respectively. Then
the formula enabledi (x̄) ≡ Gi (x̄, v̄) holds in a state S iff the event ei with parameters x̄
is enabled in S and depending on the feasibility of the action can be fired to produce a
successor state. Analogously, the formula
                                                          ^
                              firedi (x̄) ≡ Gi (x̄, v̄) ∧   ¬Gj (x̄, v̄)                          (1.1)
                                                             ej ∈E
                                                              j̸=i

expresses that the event ei is the only event enabled in S (with parameters x̄). According
to the definition of traces this implies that if S is a state in the trace, then the event ei is
not only enabled in S, but will be fired. Such a condition is essential for the expression of
fairness5 properties.
   4Actually, the logic L permits the expression of more than just properties of states. Also properties of state
transitions and thus also of successor states can be expressed, but the formulae are nonetheless interpreted
over states. With a bit of technical effort one can even express properties of finite prefixes of traces, and for
the interpretation the first state in such sequences is needed.
    5Note that if for an event e that is enabled in a state S with some parameters x̄ always another event e
                                i                                                                               j
is also enabled with the same parameters, then we can obtain traces, in which ei is never fired.
8




    The logic L also contains formulae that express properties of state transitions, which
are therefore called state transition formulae. For instance, for any state formula φ we can
define the first-order formulae
                              ^                                                          
                   N φ(v̄) ≡      ∀x̄ Gi (x̄, v̄) → ∀v̄ ′ (PAi (x̄, v̄, v̄ ′ ) → φ(v̄ ′ ))  (1.2)
                                ei ∈E

and
                                  _                                                              
                    N 1 φ(v̄) ≡           ∃x̄ Gi (x̄, v̄) ∧ ∃v̄ ′ (PAi (x̄, v̄, v̄ ′ ) ∧ φ(v̄ ′ )) .   (1.3)
                                  ei ∈E

    The formula N φ holds in a state S, if the formula φ holds in all M -successor states of S,
and the formula N 1 φ holds in a state S, if the formula φ holds in at least one M -successor
state of S.
    Other important state or transition formulae in L that already appear in proof rules from
Hoang and Abrial [HA11] are leadsto(φ1 , φ2 ) and dlf(φ). For these let M be an Event-B
machine with a set E of events and state variables v̄. For state formulae φ1 and φ2 we say
that M leads from φ1 to φ2 iff the following sentence holds:
                                    ^                                                          
                                            ′                                       ′          ′
   leadsto(φ1 , φ2 ) ≡ ∀v̄ φ1 (v̄) →   ∀x̄v̄ φ1 (v̄) ∧ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ) → φ2 (v̄ ) .
                                            ei ∈E
                                                                                                       (1.4)

    Note that it only makes sense to have |= leadsto(φ1 , φ2 ), as the formula contains a
quantification over the state variables v̄. If |= leadsto(φ1 , φ2 ) holds, then in particular for
every trace τ = S0 , S1 , S2 , . . . of M and every 0 ≤ k < ℓ(τ ) it holds that whenever Sk |= φ1
then Sk+1 |= φ2 . However, the formula leadsto(φ1 , φ2 ) expresses more than that, as there
may exist states that satisfy φ1 , but do not appear in any trace.
    Therefore, it makes sense to also define a state-dependent formula leadslocto(φ1 , φ2 ),
which is not a sentence. We say that M leads from φ1 to φ2 in state S iff the following
formula holds for the state S with state variables v̄:
                                             ^                                                  
                                                      ′                             ′          ′
         leadslocto(φ1 , φ2 ) ≡ φ1 (v̄) →        ∀x̄v̄ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ) → φ2 (v̄ ) . (1.5)
                                                    ei ∈E

      We can also define the analogous sentence
                                        _                                                
             1                                  ′                             ′          ′
      leadsto (φ1 , φ2 ) ≡ ∀v̄ φ1 (v̄) →   ∀x̄v̄ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ) → φ2 (v̄ )   ,        (1.6)
                                               ei ∈E

which expresses that whenever φ1 holds in some state Sk of M , then any successor state
Sk+1 will satisfy φ2 , regardless, whether Sk occurs in some trace τ of M (with k < ℓ(τ )) or
not, as well as the “local” formula
                                         _                                                      
      leadslocto1 (φ1 , φ2 ) ≡ φ1 (v̄) →   ∀x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) → φ2 (v̄ ′ ) , (1.7)
                                               ei ∈E

which expresses that if φ1 holds in the state S of M , then there is a successor state S ′
satisfying φ2 .
                                                                                              9




     For a state formula φ we say that M is deadlock-free in φ iff the following sentence is
satisfied:
                                              _
                            dlf(φ) ≡ φ(v̄) →     ∃x̄ Gi (x̄, v̄).                      (1.8)
                                                ei ∈E
    It expresses that whenever a state satisfies φ, there is at least one event ei of M that is
enabled.
    Note that this definition is different from the one given by Hoang and Abrial [HA11],
which involves a quantification over state variables, and thus satisfaction means that at least
one event ei of M is enabled in every state S, in particular (but not only) in all states in a
trace τ . Then Sℓ(τ )−1 |= ¬φ holds for every finite trace τ = S0 , . . . , Sℓ(τ )−1 of M .
Example 1.1. Consider a simple Event-B machine M with a single state variable x ∈ N,
initialized to x := 0, and two events:
inc                                               dec
when x < N then x := x + 1 end                    when x > 0 then x := x − 1 end
where N ∈ N is a constant. The state formulae of L are first-order formulae over the variable
x, such as x = 0, x > 0, or x ≤ N .
Next-state operator. The formula N (x ≤ N ) holds in a state S iff every successor state
satisfies x ≤ N . By (1.2), this unfolds to:
                      (x < N → x + 1 ≤ N ) ∧ (x > 0 → x − 1 ≤ N ).
Both conjuncts hold for all x ∈ N, so |= N (x ≤ N ), confirming that x ≤ N is preserved by
every event of M .
Leads-to. The sentence leadsto(x = k, x = k+1 ∨ x = k−1) expresses that from any state
with x = k, every successor state has x = k ± 1. This holds for all 0 < k < N , since inc
increments x by one and dec decrements x by one, so no event changes x by more than one
in a single step.
Deadlock-freedom. The machine M is deadlock-free provided N > 0: in any state with
0 ≤ x ≤ N , either x < N enables inc, or x > 0 enables dec, or both. Formally, |= dlf(0 ≤
x ≤ N ) follows from (1.8) under the assumption N > 0. If N = 0, the machine deadlocks
immediately in the initial state x = 0, as neither event is enabled.


1.3. Invariants and Reachability. In addition, the specification of an Event-B machine
M always includes an invariant, i.e. a state formula ι(v̄) in the logic L. The invariant must
be satisfied in all states in all traces of M . This is intrinsically coupled with a consistency
proof obligation, which is to be proven inductively. That is, the invariant must be satisfied
by the initial state of M , which requires
                                          M |= ι(v̄) ,                                     (1.9)
and whenever a state S of M satisfies the invariant ι, then every successor state S ′ of
S—produced by firing one of the events of M —also satisfies ι, i.e.
                                                       
                               M |= ∀v̄ ι(v̄) → N ι(v̄) .                        (1.10)
     Note that the formula in (1.10) is a sentence. A machine M satisfying (1.9) and (1.10)
is called consistent.
10




    In Event-B we are only interested in consistent machines, so the consistency proof
obligation is integrated into common support tools such as RODIN, and a proof must be
given—the common terminology is to discharge the consistency proof obligation.
    However, a proof of (1.9) and (1.10) shows more we need. Condition (1.10) requires the
preservation of consistency with respect to ι by all events in all states S of M , but there
may exist states S satisfying ι that are not reachable from the initial state, i.e. S does not
occur in a trace of M , and for such states consistency preservation is obsolete.
    Unfortunately, reachability of a state is a property that is undecidable in general6. Hence
there is no way to replace (1.10) by a condition that excludes non-reachable states, so the
consistency proof obligation formulated above is the only feasible way to handle consistency7.
Phrased differently, while the logic L of Event-B is known to be complete, this does not
cover conditions that are to hold in all reachable states.
    We have to keep this in mind, when we prove relative completeness for the temporal
extension TREBL of L. We will only consider machines M that are consistent with respect
to the invariant ι that is an intrinsic part of the specification of M . We will further assume
that any state formula φ of L that is to hold in all reachable states of M is made part
of the invariant ι (using conjunction). For instance, if we need leadslocto(φ1 , φ2 ) to hold
in all reachable states, we assume that the formula is included in ι, so by (1.10) de facto
leadsto(ι ∧ φ1 , φ2 ) will be proven.

1.4. Multiple-Step Extension. We want to extend the logic of Event-B in such a way
that we can express conditions over traces. For this we first make the effect of firing an
event ei of an Event-B machine M explicit by means of update sets. If in some state S the
event ej ∈ E is fired with parameters x̄, then the corresponding update set is the set of all
pairs (vi , vi′ ), where the vi (1 ≤ i ≤ n) are the state variables (not their values in S) of M ,
and the vi′ are the selected values satisfying the before-after-predicate PAj (x̄, v̄, v̄ ′ ) of the
event ej . In order to represent such sets in the logic we need new constants8 ci that are in a
one-to-one correspondence with the state variables vi (1 ≤ i ≤ n). Then the formula
                                                                            _
   USetei (x̄, X) ≡ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧ ∀c, c′ (X(c, c′ ) ↔   (c = ci ∧ c′ = vi′ )) (1.11)
                                                                            1≤i≤n

holds in a state S, if X is the update set of the event ei with parameters x̄, where v1 , . . . , vn
are the state variables and v̄ ′ = (v1′ , . . . , vn′ ) are the values selected to fulfil the before-after
predicate PAi of the event ei . Furthermore, the formula
                                                   _
                               USet(X) ≡                 ∃x̄(USetei (x̄, X))                        (1.12)
                                                    ei ∈E

holds in state S, if X is a possible update set of M in that state. Note that as non-
determinism is permitted, there is usually more than one update set in a state S, but every
such update set is intrinsically connected to one of the possible successor states.
     6This is related to the problem that NEXT is not preserved by refinement in Event-B
     7Note that the problem of being unable to restrict the focus to reachable states is present also for all other
state-based rigorous methods.
   8Note that for the interpretation of logical formulae (in L and in extensions) we need to have a domain of
values, but the state variables vi are syntactic constants that can be used to define terms, but cannot appear
in the interpretation. Update sets, however, contain locations, i.e. state variables in Event-B, and thus they
must be represented by set values in the domain used for the interpretation.
                                                                                                               11




     In addition to these formulae that express that update sets are yielded by a machine in a
state, we need formulae that express the effect of applying an update set. First, if S is a state
of an Event-B machine M and ∆ is an update set for M , then S + ∆ denotes the well-defined
state S ′ , in which valS ′ (vi ) = vi′ holds for all (vi , vi′ ) ∈ ∆, and valS ′ (vi ) = valS (vi ) holds, if
no such pair exists in ∆. Here we use the common notation that valS (vi ) denotes the value
of the state variable vi in the state S.
     If X is a set variable9 in the logic L and the value of X in a state S under a variable
assignment10 ζ is a set of pairs (ci , c′i ) with the specific constants ci introduced above and
there are no two different pairs (ci , cji ) ∈ valS,ζ (X) (j = 1, 2), then we say that valS,ζ (X)
represents the update set ∆ = {(vi , c′i ) | (ci , c′i ) ∈ valS,ζ (X)}. In this way we capture
the subtle distinction between an update set ∆, which is an extra-logical concept, as it
contains the state variables vi , and a representing set value valS,ζ (X) in the domain for the
interpretation.
     The effect of applying an update set is then expressible by additional modal formulae
[X]φ, where X is a set variable and φ is a formula of the logic L. For the interpretation
of such a formula in a state S with a variable assignment ζ we obtain false, if valS,ζ (X)
represents the update set ∆ and the interpretation of φ in the state S + ∆ with assignment
ζ gives false. In all other cases we obtain true.
     Note that according to this definition we obtain true, if valS,ζ (X) represents the update
set ∆ and the interpretation of φ in the state S + ∆ with assignment ζ gives false. However,
we also obtain true, if valS,ζ (X) does not represent an update set. At first sight this appears
a bit strange. However, if we do not have an update set, then there is no successor state, so
it makes sense to define that any formula will hold.
     These additional formulae have been adopted from the logic of non-deterministic ASMs
[FSTW18]. This is easily possible, because Event-B supports the definition of arbitrary sets.
     We can now go one step further and consider update sets that combine the updates of
multiple steps. For this we use non-negative integers k in formulae USet∗ (k, X), which are
defined inductively by USet∗ (0, X) ↔ X = ∅ and
        USet∗ (k + 1, X) ↔ ∃Y, Z USet(Y ) ∧ [Y ]USet∗ (k, Z) ∧ comp(Y, Z, X) ,
                                                                                            
                                                                                                       (1.13)
where the formula
         comp(Y, Z, X) ≡ ∀c, c′ X(c, c′ ) ↔ (Y (c, c′ ) ∧ ¬∃c′′ (Z(c, c′′ ))) ∨ Z(c, c′ )
                                                                                         
                                                                                                          (1.14)
expresses that X is the sequential composition of Y followed by Z.
     Due to the interpretation of [Y ]φ above the case of finite traces is covered. If the length
of the trace is exceeded, the subformula [Y ]USet∗ (k, Z) will be interpreted as true, and
then USet∗ (k + 1, X) can only be interpreted as false, i.e. there is no update set capturing
the updates of k + 1 steps.
     We extend the logic L by the formulae USet∗ (k, X)—there is no need to use USet(X),
as it is equivalent to USet∗ (1, X)—as well as [X]φ, and we permit existential and universal
quantification over the variables in such formulae. The resulting logic will be denoted as Lext .
Note that still all formulae in Lext are interpreted over states. Nonetheless, they can be
   9Note that variables X representing update sets are set variables of arity 2, but the logic may use other
set variables as well.
   10As common in logic ζ assigns values in the domain to variables in formulae. Here we also have set
variables of some arity, so set variables of arity 2 are assigned sets of pairs, and if the first component of all
such pairs are constant ci representing the state variables vi , then the assigned value represents an update
set.
12




exploited to express properties of traces. In the following we will write M |= φ for formulae
φ ∈ Lext whenever we have S0 |= φ for any initial state S0 of M .
    The following is an informal summary of the interpretation of the formulae in Lext :
• The logic Lext contains all formulae φ of the logic L. Then S |= φ holds iff φ is interpreted
  as true, when each state variable v is interpreted by its value in the state S.
• The logic Lext contains formulae φ ≡ USet∗ (k, X), where k is a non-negative integer and
  X is a set variable. Then S |= φ holds iff there exists an update set ∆ and a set value V
  representing ∆ that is assigned to X such that ∆ is the composed update set yielded by k
  steps of the machine M starting in state S. The formal definitions are given in (1.12),
  (1.11), (1.13) and (1.14).
• The logic Lext contains formulae φ ≡ [X]ψ, where X is a set variable and ψ is a formula
  of Lext . Then S |= φ holds iff there exists an update set ∆ yielded in S and a set value V
  representing ∆ that is assigned to X such that S + ∆ |= ψ holds.



1.5. Temporal Operators. In order to support formal verification of computer programs
Pnueli introduced linear time temporal logic (LTL), which extends propositional logic with
modal operators referring to time [Pnu77]. There are different ways to define the basic
temporal operators; the most common ones are □ (always), ♢ (eventually, i.e. sometimes in
the future), U (until), and N (next). Most commonly used are the first three of them, as they
suffice to express the most important liveness conditions [MP84]. Thus formulae are built
from propositions, the usual Boolean operators ¬, ∧, ∨, →, and modal operators. However,
the propositional nature of LTL is a severe restriction, while an extension of first-order
logic or even second-order logic with Henkin semantics by these temporal operators leads to
incompleteness.
     Hoang and Abrial [HA11] extended LTL using Event-B state formulae instead of
propositions. Following this approach, Ferrarotti et al. [FRS+ 24] defined the logic LTL(EB),
the well-formed formulae of which were defined as the closure of the set L of basic state
formulae under the usual Boolean operators ¬, ∧, ∨, → and modal operators □ (always), ♢
(eventually) and U (until). Note that ♢ φ is merely a shortcut for true U φ, as can be easily
proven from the semantics we define below. As we saw above, the absence of the modal
operator N (next) does not matter, as conditions that are to hold in successor states are
already covered by the first-order logic of Event-B.
     As in LTL the formulae of LTL(EB) were interpreted over traces of Event-B machines
[FRS+ 24]. However, inspired by related research on modal extensions of the logic of Abstract
State Machines [FS24] we will now show that all temporal operators can be defined as
shortcuts of formulae of the logic Lext , while the defining properties over traces remain valid.
This will allow us some generalisations such as temporal formulae that hold over defined
sets of traces.


1.5.1. All-Traces Temporal Formulae. We say that the machine M satisfies the formula □φ
(with φ ∈ Lext )—interpreted as “φ always holds in all traces”—iff for all traces S0 , S1 , . . . of
M we have Si |= φ for all i ≥ 0; this is well defined, because Lext formulae are interpreted
over states. We write M |= □φ for this. Furthermore, for i ≥ 0 there must exist an update
set ∆ with Si = S0 + ∆ such that S0 |= USet∗ (i, X) with X representing ∆, and Si |= φ
                                                                                                 13




holds iff S0 |= [X]φ. Therefore, the formula □φ is merely a shortcut for the Lext formula
                                 ∀n∀X(USet∗ (n, X) → [X]φ) .                                 (1.15)
     Note that there is no problem with finite traces. If n exceeds the length of the trace,
the subformula USet∗ (n, X) will become false, regardless which value is assigned to X, and
then the implication is interpreted as true, so in essence only finitely many values for n
have to be considered.
     Due to the interpretation of [X]φ above the case of finite traces is covered. If n exceeds
the length of the trace, the subformula [Y ]USet∗ (k, Z) will be interpreted as true, and then
USet∗ (k + 1, X) can only be interpreted as false, i.e. there is no update set capturing the
updates of k + 1 steps.
     Analogously we say that M satisfies the formula ♢φ (with φ ∈ Lext )—denoting that “φ
eventually holds in all traces”—iff for all traces S0 , S1 , . . . of M we have Si |= φ for some
i ≥ 0. We write M |= ♢φ for this. We can see that ♢φ is also a shortcut of an Lext formula,
which in this case is slightly more complex.
     For this, consider the negation of ♢φ, so there exists a trace S0 , S1 , . . . of M with
Si |= ¬φ for all i ≥ 0. If all traces are infinite, then ∀n∃X(USet∗ (n, X) ∧ [X]¬φ) must
hold, i.e. after arbitrarily many steps of M we reach a state satisfying ¬φ. Furthermore,
all previous states in the same trace must also satisfy ¬φ. For this note that every update
set ∆ that results from n > 0 steps of a machine M in some state S can be written as
sequential composition of an update set ∆1 yielded from m < n steps in S and an update set
∆2 yielded from n − m steps in the m’th successor state of S resulting from applying ∆1 to
S. Sequential composition of update sets is expressed by formula comp(X1 , X2 , X) that we
introduced before, where X and Xi (i = 1, 2) represent ∆ and ∆i , respectively. That is, if
we decompose X into X1 and X2 for the first m and the following n − m steps, respectively,
we must also have that [X1 ]¬φ holds. Combining these two considerations, we obtain the
formula
                   
            ∀n∃X USet∗ (n, X) ∧ [X]¬φ ∧ ∀m m < n → ∀X1 X2 (USet∗ (m, X1 )∧
                                                                            
                  [X1 ]USet∗ (n − m, X2 ) ∧ comp(X1 , X2 , X) → [X1 ]¬φ) .

    In order to capture also finite traces we can replace USet∗ (n, X) herein by the formula
U∗c (n, X), which we define as a shortcut for
                                                                     ^
             USet∗ (n, X) ∨ ∃n′ n′ < n ∧ USet∗ (n′ , X) ∧ [X] ∀x̄
                                                                                        
                                                                            ¬Gi (x̄, v̄) .
                                                                    ei ∈E

    Taking again the negation we see that ♢φ is a shortcut for the following Lext formula
                 
           ∃n∀X (U∗c (n, X) ∧ [X]¬φ) → ∃m m < n ∧ ∃X1 X2 (USet∗ (m, X1 )∧
                                                                         
                            ∗
                                                                       
                   [X1 ]USet (n − m, X2 ) ∧ comp(X1 , X2 , X) ∧ [X1 ]φ) .            (1.16)

     We can also express UNTIL-formulae in Lext . M satisfies the formula φUψ (with
φ, ψ ∈ Lext )—denoting that “φ holds until ψ holds in all traces”—iff for all traces S0 , S1 , . . .
of M there exists some i ≥ 0 with Si |= ψ and Sj |= φ for all j < i. We write M |= φUψ for
this.
14




     Phrased differently, whenever in a trace we have a state Sm that does not satisfy φ or
that satisfies ψ (reachable from S0 by means of some m-step update set X), then there must
exist an earlier state Sn2 (reachable by means of some n2 -step update set Y with n2 ≤ m)
satisfying ψ such that all earlier states Sn1 (reachable by means of some n1 -step update set
X1 with n1 < n2 such that Y is the composition of X1 and some X2 ) satisfy φ. Hence φUψ
is the Lext formula
              ∀m∀X USet∗ (m, X) ∧ [X](¬φ ∨ ψ) → ∃n2 ∃Y n2 ≤ m∧
                USet∗ (n2 , Y ) ∧ [Y ]ψ ∧ ∀n1 ∀X1 , X2 (n1 < n2 ∧ USet∗ (n1 , X1 )∧
                       [X1 ]USet∗ (n2 − n1 , X2 ) ∧ comp(X1 , X2 , Y ) → [X1 ]φ) .
                                                                                  
                                                                                            (1.17)


1.5.2. One-Trace Temporal Formulae. The temporal Lext formulae □φ (ALWAYS φ), ♢φ
(EVENTUALLY φ) and φUψ (φ UNTIL ψ) defined above are interpreted over states S and
they hold in all traces of a machine M starting in this state S. Temporal logics such as CTL
and CTL∗ [CE82] also consider formulae that are to hold in just one trace. We show that
these one-trace analogues of temporal logic formulae can also be defined in Lext .
     We say that M satisfies the formula □1 φ (with φ ∈ Lext )—interpreted as “φ always
holds in some trace”—iff there exists a trace S0 , S1 , . . . of M with Si |= φ for all i ≥ 0. We
write M |= □1 φ for this. Then ¬□1 ¬φ should be equivalent to ♢φ. Hence □1 φ is a shortcut
for the Lext formula
                     
              ∀n∃X U∗c (n, X) ∧ [X]φ ∧ ∀m m < n → ∀X1 X2 (USet∗ (m, X1 )∧
                                                                              
                              ∗
                                                                            
                    [X1 ]USet (n − m, X2 ) ∧ comp(X1 , X2 , X) → [X1 ]φ) .                  (1.18)

     In the same way we say that M satisfies the formula ♢1 φ (with φ ∈ Lext )—denoting
that “φ eventually holds in some trace”—iff there exists a trace S0 , S1 , . . . of M with Si |= φ
for some i ≥ 0. We write M |= ♢1 φ for this. Then ¬♢1 ¬φ should be equivalent to □φ,
hence ♢1 φ is a shortcut for the formula
                                 ∃n∃X(USet∗ (n, X) ∧ [X]φ) .                                (1.19)
     Finally, we can express that “φ holds until ψ in some trace” by the Lext formula
              ∃n∃X USet∗ (n, X) ∧ [X]ψ ∧ ∀m∀X1 X2 (m < n ∧ USet∗ (m, X1 )∧
                     [X1 ]USet∗ (n − m, X2 ) ∧ comp(X1 , X2 , Y ) → [X1 ]φ) ,
                                                                           
                                                                                            (1.20)
and we write M |= φU 1 ψ for this. The formula expresses that there exists a run S0 , S1 , . . .
of M and some i ≥ 0 with Si |= ψ and Sj |= φ for all j < i.
     All modal operators □, ♢, U, □1 , ♢1 and U 1 can be freely combined in Lext . For instance
    1
♢□ φ expresses that in all traces S0 , S1 , . . . we reach a state Sk such that in one continuation
of the prefix S0 , . . . , Sk all states satisfy φ. Such formulae can now be interpreted over
states. There may be some doubts, whether there are many applications, where such general
conditions occur, but technically it is possible to handle them.
     Different to the work in [FRS+ 24] we now can also capture universal and existential
quantification over traces without leaving the Event-B frame of first-order logic and set
theory.
                                                                                                          15




1.5.3. Temporal Formulae over Definable Sets of Traces. Here we want to go one step further
and consider also trace quantifiers, by means of which we can define formulae that are to
hold over well-defined subsets of the set of traces. This has been inspired by temporal
logics with team semantics [GMOV22]. The sets of traces we are interested in are to be
characterised by a temporal formula, which according to the semantics of Lext must hold in
the inititial state(s) of the traces. The general study of temporal formulae over definable
sets of traces is beyond the scope of this article; we will only consider sets of traces defined
by temporal formulae of the form ♢□χ for some Lext formula χ. That is we consider traces
that either terminate with a state Sm satisfying χ or are infinite with a tail of states Sℓ
(ℓ ≥ k for some k) all satisfying χ. For short, we consider traces S0 , S1 , . . . , for which there
exists some k such that Sℓ satisfies χ for all ℓ ≥ k. In these cases we say that the trace
satisfies the selection condition ⟨χ⟩.
     We will write □χ φ for an Lext formula that is intended to hold in the initial state S0
of a machine M , if for all traces S0 , S1 , . . . that satisfy the selection condition ⟨χ⟩ we have
Si |= φ for all i ≥ 0. Analogously, we write ♢χ φ for an Lext formula that is intended to hold
in the initial state S0 of a machine M , if for all traces S0 , S1 , . . . that satisfy the selection
condition ⟨χ⟩ we have Si |= φ for at least one i ≥ 0.11
     In order to define □χ φ we need to modify the defining formula (1.15) for □φ. Herein
the subformula USet∗ (n, X) → [X]φ expresses that if after n steps we reach a state Sn and
the corresponding update set is X, then applying X leads to a successor state satisfying φ.
We need to restrict this to states that appear in a trace terminating with a state satisfying
χ or having an infinite tail of states all satisfying χ. This is the case, if there is an m-step
successor state corresponding to some update set Y and there is a continuation of this trace
with states all satisfying χ. With this we see that □χ φ is a shortcut for the Lext formula
                                                                        
              ∀n∀X USet∗ (n, X) ∧ ∃m∃Y [X]USet∗ (m, Y ) ∧ [Y ]□1 χ → [X]φ ,
                                                                  
                                                                                                      (1.21)

where the subformula □1 χ is defined by (1.18).
      A formula ¬♢χ ¬φ holds, if there exists a trace S0 , S1 , . . . satisfying the selection condition
⟨χ⟩ such that Si |= φ holds for all i ≥ 0. Consider again the case that χ holds for traces
S0 , S1 , . . . , for which there exists some k such that Sℓ satisfies χ for all ℓ ≥ k. In this case
we need to modify the defining formula (1.18) for □1 φ in such a way that the state reached
by means of the n-step update set X appears in a trace satisfying the selection condition
⟨χ⟩. Hence, ¬♢χ ¬φ is a shortcut of the Lext formula
                    
                ∀n∃X U∗c (n, X) ∧ [X]φ ∧ ∀m m < n → ∀X1 X2 (USet∗ (m, X1 )∧

                      [X1 ]USet∗ (n − m, X2 ) ∧ comp(X1 , X2 , X) → [X1 ]φ) ∧
                                                                           
                                                                
                                           ∗               1
                                                              
                            ∃m∃Y [X]USet (m, Y ) ∧ [Y ]□ χ ,



   11Note that by means of these formulae we define quantifiers for arbitrary Lext formulae χ, by means
of which the sets of traces satisfying the selection condition ⟨χ⟩ are defined, and with these quantifiers we
restrict the common temporal operators □ and ♢.
16




and by taking the negation we see that ♢χ φ is a shortcut of the Lext formula
                      
                ∃n∀X U∗c (n, X) ∧ ∀m m < n → ∀X1 X2 (USet∗ (m, X1 )∧

                    [X1 ]USet∗ (n − m, X2 ) ∧ comp(X1 , X2 , X) → [X1 ]¬φ) ∧
                                                                          
                                                                 
                                     ∗               1
                                                        
                      ∃m∃Y [X]USet (m, Y ) ∧ [Y ]□ χ → [X]φ .                                          (1.22)



1.6. Definition of TREBL. We now define the logic TREBL as a fragment of Lext , in
which important liveness conditions can be expressed. Of particular interest are the following
conditions:
Invariance.: An invariance condition is given by an Lext formula of the form □ φ for some
       L formula φ. Such a condition is satisfied by a machine M iff all states S in all traces
       of M satisfy φ.12
Existence.: An existence condition is given by an Lext formula of the form □♢φ for some
       L formula φ. Such a condition is satisfied by a machine M iff in every infinite trace of
       M there is an infinite subsequence of states satisfying φ, and every finite trace of M
       terminates in a state satisfying φ.
Progress.: A progress condition is given by an Lext formula of the form □(φ → ♢ψ) for some
       L formulae φ and ψ. Such a condition is satisfied by a machine M iff in every trace of
       M a state Si satisfying φ is followed some time later by a state Sj (j ≥ i) satisfying
       ψ. A progress condition with φ = true degenerates to an existence condition.
Persistence.: A persistence condition is given by an Lext formula of the form ♢□ φ for
       some L formula φ. Such a condition is satisfied by a machine M iff every infinite trace
       of M ends with an infinite sequence of states satisfying φ, i.e. for some k we have
       Si |= φ for all i ≥ k, and every finite trace of M terminates in a state satisfying φ.
Reachability.: A reachability condition is given by an Lext formula of the form ♢ φ for
       some L formula φ. Such a condition is satisfied by a machine M iff in all traces of M
       there exists a state S satisfying φ.
     For all four kinds of liveness conditions13 we can add variants by replacing one or both
of the temporal operator by the operators in (1.18) and (1.19) that refer to just one trace.
It also does not do any harm to generalise from L formulae to Lext formulae except for the
formulae φ in progress conditions.
     Then it makes sense to define TREBL as the closure of the L under a restrictive set of
temporal constructors, which basically have the form of the formulae above, so we get the
following definition.
Definition 1.2. The set LT of well-formed formulae of TREBL is the smallest set inductively
defined by the following rules:
• For φ ∈ L we also have φ ∈ LT ;
     12Note that invariance conditions have been an intrinsic part of Event-B (and likewise all other rigorous
methods) since the very beginnings, and for invariance alone there would be no need to consider a temporal
logic.
   13In [FRS+ 24] an existence condition was also called an unconditional progress condition, and a progress
condition was called conditional progress condition to emphasise that a progress condition with φ = true
degenerates to an existence condition.
                                                                                                          17




• For φ ∈ LT , ψ ∈ L, X ∈ {□, □1 } and Y ∈ {♢, ♢1 } the Lext formulae Xφ, Y φ, XY φ,
  Y Xφ and X(ψ → Y φ) are formulae in LT ;
• For φ ∈ LT the quantified Lext formulae ∀xφ and ∃xφ are formulae in LT .
     Note that TREBL is defined as the closure of the Event-B logic L under certain temporal
operators. We only need the temporal operators, but not the predicates USet, USet∗ and
[·] that were used to define them. These predicates are only used as a means that allows
temporal formulae to be defined as shortcuts14 for formulae in Lext that are interpreted over
states rather than traces. This even allows us to include arbitrary nesting of the defining
operators. We already mentioned before that this generality may be not needed for most
applications, but technically, it does do no harm. We will see this later, when we discuss
derivation rules for nested formulae.
     Further note that for the definition of TREBL we only used the operators occurring in
the common liveness conditions above, but we did not use U-formulae or definable sets of
traces. Definable sets of traces will nonetheless become relevant in the proofs in the next
section.
     In the next section we will present a sound set of derivation rules for LT , which modify
and extend the derivation rules discovered by Hoang and Abrial [HA11]. We then show that
together with derivation rules for first-order logic with types we obtain a relative complete set
of derivation rules, where relative completeness refers to the existence of derivations, if certain
variant terms can be defined for the Event-B machine under consideration. Fortunately,
we can also show that for sufficiently refined machines the existence of such variant terms
can always be guaranteed. In the completeness proof we will eliminate the restriction that
machines must be tail-homogeneous, which was assumed in [FRS+ 24].


1.7. Examples. We now look at some examples and their formalisation in TREBL. First we
consider non-interference of traces, an example often classified as a 2-safety hyperproperty
(as it compares pairs of traces). Then we give two examples of liveness conditions.
Example 1.3. Non-Interference of traces is a relevant security property when multiple
users with different access rights collaborate concurrently [Bis09]. We assume a set of
users u1 , . . . , un , each permitted to handle only events classified by linearly ordered labels
ℓ1 < · · · < ℓn , respectively. The system satisfies non-interference if, for each user ui , the
observable behavior of the system is unaffected by events classified at higher security levels
(ℓj for j > i), even when ui has full knowledge of the system’s specification and reasoning
capabilities.
     We define an Event-B machine for the multi-level stack example from [McL92] assuming
a set of users U = {u1 , . . . , uk }, a set of stacks P = {p1 , . . . , pn }, a set of data values D,
and a linearly ordered set of clearance levels L = {ℓ1 < · · · < ℓn }. The Event-B constants
user cl ∈ U → L and stack cl ∈ P → L assign to each user and each stack a corresponding
clearance level. The variable op cl ∈ L records the clearance level of the most recently
executed operation, and is initialized to the minimum clearance level ℓ1 . The variables
top ∈ P → N, store ∈ P × N → D, and answer ∈ U → D represent, respectively, the
   14According to Lamport [Lam10] the direct use of time or step variables leads to very complicated formulae
and therefore should be discouraged. Indeed, all defining formulae (1.15) – (1.22) are very complex, but this
complexity does not prevent the existence of a rather simple set of derivation rules, and the complexity will
not impact on the application; it will only be relevant for the proof of soundness and relative completeness.
18




current stack pointer, stack element storage, and last read result for each user; they are
initially empty.
     To prevent users with higher-level clearances from passing information to users with
lower-level clearances, users are forbidden to:
   (i) read stacks with clearance levels above their own clearance, and
  (ii) push or pop stacks with clearance levels below their own clearance.
     Each user with sufficient security clearance can execute push, pop, peek, and peek0
events, whose guards and actions enforce these constraints. The full Event-B machine M is
given below.

     sets U ; P ; L; D                            variables
     constants                                      top // current stack pointer
       user cl // user clearance                    store // stack element storage
       stack cl // stack clearance                  answer // last read result
       ℓ1 // minimum clearance level                op cl // current operation clearance

     axioms                       invariants                     init
       user cl ∈ U → L               op cl ∈ L                      op cl := ℓ1
       stack cl ∈ P → L              top ∈ P → N                    top := ∅
       ℓ1 = min(L)                   store ∈ P × N → D              store := ∅
                                     answer ∈ U → D                 answer := ∅

     push                                         pop
     any u, p, d                                  any u, p
     when                                         when
       u ∈ U; p ∈ P; d ∈ D                          u ∈ U; p ∈ P
       user cl(u) ≤ stack cl(p)                     top(p) > 0
     then                                           user cl(u) ≤ stack cl(p)
       op cl := user cl(u)                        then
       top(p) := top(p) + 1                         op cl := user cl(u)
       store(p, top(p)+1) := d                      top(p) := top(p) − 1
     end                                          end

     peek                                         peek0
     any u, p                                     any u, p
     when                                         when
       u ∈ U; p ∈ P                                 u ∈ U; p ∈ P
       top(p) > 0                                   top(p) = 0
       user cl(u) ≥ stack cl(p)                     user cl(u) ≥ stack cl(p)
     then                                         then
       op cl := user cl(u)                          op cl := user cl(u)
       answer(u) := store(p, top(p))                answer(u) := ∅
     end                                          end
                                                                                            19




     The guards enforce the access control policy: push and pop require user cl(u) ≤
stack cl(p), ensuring that a user may only write to stacks at or above their own clearance
level. Conversely, peek and peek0 require user cl(u) ≥ stack cl(p), ensuring that a user
may only read from stacks at or below their own clearance level. In every event, op cl
is updated to user cl(u), recording the clearance level of the most recently performed
operation.
     Non-interference requires that the observable output answer(u) of any user u is never
affected by operations performed at a strictly higher clearance level, and similarly that
the state of any stack p is not modified by operations at a clearance level strictly above
stack cl(p). Formally, the machine M must satisfy the invariances □φpush , □φpop , and
□φpeek , where, using primed variables to denote successor-state values:
    φpush ≡ ∀ℓ op cl′ = ℓ → ∀p (stack cl(p) < ℓ → top′ (p) = top(p) ∧
                             store′ (p, top′ (p)) = store(p, top(p))) ,
                                                                     
                                                                                        (1.23)

    φpop ≡ ∀ℓ op cl′ = ℓ → ∀p (stack cl(p) < ℓ → top′ (p) = top(p) ∧
                            store′ (p, top′ (p)) = store(p, top(p))) ,
                                                                    
                                                                                        (1.24)

    φpeek ≡ ∀ℓ op cl′ = ℓ → ∀u (user cl(u) < ℓ → answer′ (u) = answer(u)) .
                                                                                   
                                                                                        (1.25)
     The invariants are organised according to what each class of operation can actually
modify. push and pop never touch answer, so φpush and φpop only constrain the stack
state: after such an operation at clearance level ℓ, the top pointer and stored content of
every stack with a lower clearance level must be unchanged. Dually, peek and peek0 never
touch top or store, so φpeek only constrains answer: after a read at clearance level ℓ, the
answer of every user with a lower clearance level must be unchanged. Together, the three
invariants ensure that no information can flow from higher to lower clearance levels across
any single step. Since every event updates op cl to user cl(u) and the guards prevent any
event from accessing resources outside the permitted clearance range, this per-step condition
lifts by a straightforward induction on the number of steps along the trace to the global
non-interference property.
     Note that □φpush , □φpop , and □φpeek are in general trace properties, since they relate
each state to its immediate successor via the primed variables. However, the primed variables
refer to values that are definable in the next state, so the formulae above can be rewritten
into equivalent formulae in L using the next-operator N . Alternatively, one can introduce
auxiliary variables into the Event-B machine to record the previous values of op cl, top,
store, and answer, thereby reducing each trace property to a safety property expressible as
a plain state predicate. In either case, making these properties part of the invariant of the
(possibly enriched) machine gives rise to consistency proof obligations, so we in fact prove
more than the temporal invariances □φpush , □φpop , and □φpeek alone.
Example 1.4. Fairness for an Event-B machine means that every event that is enabled
must eventually be fired. This can be expressed by quantified progress conditions
                                                               
                            ∀x̄ □(enabledi (x̄) → ♢firedi (x̄))
for all events ei . A weaker form would be to require the progress conditions
                                                                    
                              □ ∃x̄ enabledi (x̄) → ♢∃ȳ firedi (ȳ)
for all events ei , where the enabled event will eventually be fired with different parameters.
20




Example 1.5. Bounded deducibility was introduced by Popescu et al. in [PLB14] as a
means to express privacy constraints in concurrent systems. In a nutshell, we assume an
observation infrastructure, which is defined by a partial function O, which may assign an
observation O(S) ∈ O to a state S. Then a trace S0 , S1 , . . . gives rise to a sequence Obs i of
lists of observations. Intuitively, an event that is fired in state Si either appends O(Si ) to the
value of a variable Obs—which is the empty list in the initial state—or leaves the value of
Obs unchanged. Informally, the list Obs i captures what an agent—a potential attacker—can
see from the prefix S0 , . . . , Si of the trace. We further assume a secrecy infrastructure, which
is defined by a partial function G, which may assign a secret G(S) ∈ G to a state S. Then a
trace S0 , S1 , . . . also gives rise to a sequence Sec i of lists of secrets.
      A bounded deducibility constraint (BD) comprises a declassification trigger ψ and a
declassification bound B. ψ is a formula that can be evaluated in a state, though it is tacitly
assumed that it is restricted to a formula that does not refer to any successor or predecessor
state. B is a binary relation on lists of secrets. For BD security we consider eligible prefixes
S0 , . . . , Sp of traces such that all states in the prefix satisfy ¬ψ. Then the machine M is
BD secure iff whenever we have (Sec p , G) ∈ B there exists an eligible prefix S0′ , . . . , Sq′ of
some trace with Obs p = Obs ′q and Sec ′q = G. Informally phrased, for every trace that might
reveal some secrets there exists an indistinguishable trace (by means of the observations), in
which the secrets are bounded and thus not revealed15.
      In [PLH21, PLB21] Popescu et al. used a simple conference management system CoCon
(inspired by EasyChair) as an application example for BD security. As a simple example
consider the privacy requirement that a group of users should learn nothing about the content
of a paper beyond the last submitted version, unless one of them becomes a co-author of
that paper. This constraint was named PAP2 in [PLH21]; together with other constraints it
merely ensures that PC members should only see the last version of any paper and only,
after the submission phase has been closed.
      This requirement can be captured by a BD constraint as shown in [PLH21]; we omit
the details here. However, in TREBL the requirement can be captured in a different way
using a transition invariant. For this we assume a set UIDs of valid user identifiers and a set
paperIDs of valid paper identifiers. Furthermore, assume functions authors, content and
final , which assign to a paper identifier pid and a version number i the set of authors, the
content and a Boolean value indicating, if the version is the final version. Then let ψ be the
formula
                ^
                    ∀uid pid i c uid ∈ UIDs ∧ pid ∈ paperIDs ∧ uid ∈     / authors(pid, i)∧
              e∈E
                                                                / output ′e (uid) ,
                      content(pid, i) = c ∧ ¬final (pid, i) → c ∈
where output e (uid) refers to the output of event e made to the user with the identifier uid.
Then □ψ captures the requirement PAP2 without referring to a BD constraint.



     15In essence, BD security requires a relation between different traces to hold, which is beyond the
fragment of Lext we are dealing within this article. Nonetheless, we should stress that the version of TREBL
investigated in this article seems not to be a maximal fragment of Lext with respect to having a sound and
relative complete set of derivation rules. However, for the sake of keeping this article reasonably compact,
we postpone further extensions to TREBL to future work. Here we leave it as an open conjecture, that an
extension capturing also BD security is possible.
                                                                                                  21




                                 2. Sound Derivation Rules
Our aim is to develop a proof system for TREBL based on the derivation rules in [HA11],
the modifications in [FRS+ 24] and the extensions in [FS24]. This will support mechanical
reasoning about liveness properties for Event-B machines.
     Let R be a set of axioms and inference rules. A formula φ ∈ Lext is derivable from a
set Φ of Lext formulae using R (denoted as Φ ⊢R φ, or simply Φ ⊢ φ when R is clear from
the context) iff there is a deduction from formulae in Φ to φ that only applies axioms and
inference rules from R. We write ⊢ φ as a shortcut for ∅ ⊢ φ.
     As we are interested in the derivation of formulae that are to hold for a given Event-B
machine M we consider derivations that depend on the specification of M , i.e. we refer to
the events of M , their guards and their actions. In this case we write M ⊢ φ.


2.1. Rules for Invariance. For invariance conditions we can exploit a simple induction
principle. In order to establish invariance of a formula φ ∈ L it suffices to show that φ
holds in the initial state of any trace S0 , S1 , . . . , and furthermore that for every 1 ≤ k < ℓ(σ)
whenever Sk |= φ holds, then also Sk+1 |= φ holds. In addition, invariance of a state formula
φ implies invariance of a weaker state formula ψ. This gives rise to the following lemma.
Lemma 2.1. For formulae φ, ψ ∈ L the derivation rules
                M ⊢ φ M ⊢ leadsto(φ, φ)                      ⊢ φ → ψ M ⊢ □φ
         INV1 :                                       INV2 :
                          M ⊢ □φ                                 M ⊢ □ψ
are sound for the derivation of invariance properties in TREBL.
Proof. Proof. Let S0 , S1 , . . . be an arbitrary trace of M . We proceed by induction on k.
If M |= φ holds, then S0 |= φ holds by definition, which gives the induction base. If for
arbitrary k we have Sk |= φ, then with M |= leadsto(φ, φ) we immediately get Sk+1 |= φ,
which completes the induction step and shows the soundness of INV1 .
     If M |= □φ holds, then we have Si |= φ for all i ≥ 0. As also |= φ → ψ holds, we get
Si |= ψ for all i ≥ 0, hence M |= □ψ, which shows the soundness of INV2 .
     For the invariant ι of M , the consistency proof obligation corresponds to the antecedents
of rule INV1 for the case φ ≡ ι, and the consequence expresses what we really want to have,
the satisfaction of ι in all reachable states. We also said that for any invariant ψ, a formula
in L, we assume that it is made a part of the invariant ι. Then ⊢ ι → ψ becomes a triviality.
For a consistent machine M we also get M ⊢ □ι and hence M ⊢ □ψ. Therefore, with the
general assumptions made the discharging of the consistency proof obligation suffices for
invariance proofs.
     If the antecedent M ⊢ leadsto(φ, φ) in the lemma is replaced by the weaker one-trace
analog M ⊢ leadsto1 (φ, φ), we obtain invariance of φ in one trace instead of all traces, hence
the following modified lemma.
Lemma 2.2. For formulae φ, ψ ∈ L the derivation rules

                   M ⊢ φ M ⊢ leadsto1 (φ, φ)                        ⊢ φ → ψ M ⊢ □1 φ
         INV11 :                                          INV12 :
                         M ⊢ □1 φ                                       M ⊢ □1 ψ
are sound for the derivation of one-trace invariance properties in TREBL.
22




Proof. We use induction on k to construct a trace S0 , S1 , . . . with Si |= φ for all i ≥ 0. If
we assume M |= φ, then by definition we have S0 |= φ for the initial state S0 . If Sk |= φ,
then as we assume M |= leadsto1 (φ, φ) there exists a successor state Sk+1 with Sk+1 |= φ,
which gives the desired trace and shows the soundness of the rule INV11 .
     Next let S0 , S1 , . . . be a trace of M with Si |= φ for all i ≥ 0. If we assume M |= □1 φ,
such a trace exists. If we further assume |= φ → ψ, we immediately get also Si |= ψ for all
i ≥ 0, which shows M |= □1 ψ and hence the soundness of the rule INV12 .
     As the antecedents in the rules INV1 and INV11 are formulae of L, Lemmata 2.1 and 2.2
reflect the known fact that invariance proofs do not require any investigation of temporal
logic. Note that for the soundness of rule INV1 we have M |= φ iff the initial state of M
satisfies φ. This will change for existence, persistence and reachability, and will require
rather sophisticated arguments for progress conditions.


2.2. Variant Terms and Formulae. We will first concentrate on existence, persistence
and reachability formulae in TREBL, in which subformulae are in L rather than in TREBL.
In [HA11] the notions of convergence and divergence have been introduced, which differ from
existence and persistence conditions only by the treatment of finite traces. For the sake of
consistent terminology16 we preserve these notions using the specific predicates conv(φ) and
div(φ) for convergence and divergence formulae, respectively, and formulate derivation rules
for them. These derivation rules exploit variant formulae in L defined by certain terms in
the Event-B machine M . We also preserve the terminology of c-variants and d-variants
used in [FRS+ 24] for these.
     As TREBL contains also formulae that are to hold in one trace rather than in all traces,
we generalise the investigation of variants for the modified existence and persistence formulae.
We also introduce e-variants to support proofs of reachability formulae.
     In addition to the proof of soundness of these derivation rules we show that it is always
possible to refine a machine M conservatively to a machine M ′ , in which the needed variant-
terms can be defined. These results (proven in our previous work [FRS+ 24] for the case
of existence and persistence for all-trace temporal formulae) will be the key for relative
completeness.


2.2.1. Variants for Existence Proofs. For a formula φ ∈ L a machine M satisfies the existence
formula □♢¬φ iff for every trace τ = S0 , S1 , . . . of M there is no k such that Sℓ |= φ holds
for all ℓ ≥ k. In this case we call M to be convergent in φ and we use the notation conv(φ)
for this [FRS+ 24, HA11].
     Hoang and Abrial showed that conv(φ) can be derived by means of variant terms
[HA11, p. 460]. For this suppose that t(v̄) is a well-formed term that takes values in some
well-founded set17 V with minimum 0, and let varc (t, φ) denote the sentence
           ^                                                                                     
       ∀v̄     ∀x̄v̄ ′ φ(v̄) ∧ Gi (x̄, v̄) → t(v̄) ̸= 0 ∧ (PAi (x̄, v̄, v̄ ′ ) → t(v̄ ′ ) < t(v̄)) . (2.1)
          ei ∈E

   16The terminology seems indeed to be counter-intuitive, because in the case of “convergence” we may
have a trace with infinitely many swaps between states satisfying φ and states satisfying ¬φ, whereas in the
case of “divergence” we may have traces with infinite tails of states all satisfying φ.
   17For instance, V could be the set N of natural numbers or the set HF(A) of hereditarily finite sets over
some finite set A, as used in [FRS+ 24].
                                                                                                      23




     We call the first-order sentence varc (t, φ) a c-variant formula, and the term t(v̄) a
c-variant. Then varc (t, φ) is satisfied iff for all states S, whenever φ holds and an event ei
is enabled, we have that t(v̄) evaluates to a non-zero element in V , and an execution of ei
decreases t(v̄). Hoang and Abrial showed the following:
Lemma 2.3. If varc (t, φ) is a valid formula for φ ∈ L and no trace of M terminates in a
state satisfying φ, then M satisfies the convergence formula conv(φ), in other words, the
derivation rule
                                    M ⊢ varc (t, φ) M ⊢ □dlf(φ)
                                           M ⊢ conv(φ)
is sound.
     Note that c-variant formulae are sentences, and we request the decrease of the variant in
all states satisfying φ, not just in reachable states. If we omitted the universal quantification
over v̄, we would instead get a state formula, and we could prove the lemma using an
invariance formula expressing the satisfaction in all reachable states satisfying φ. Then it
would become necessary to add this state formula to the invariant. With Lemma 2.4 we will
show that we can always establish the stronger condition in (2.1).
Proof. If M |= □dlf(φ) holds, then every finite trace of M terminates in a state satisfying
¬φ. If M |= varc (t, φ), but M ̸|= conv(φ), then by the definitions of temporal formulae
and varc (t, φ) there is an infinite subsequence Si , Si+1 , . . . of states of some trace τ of M
such that for the values bj of t(v̄) in Sj we have bi > bi+1 > . . . . As the order ≤ on V is
well-founded, this is not possible.
    As conv(φ) is merely another notation for an existence formula □♢¬φ, an immediate
consequence of Lemma 2.3 is that for φ ∈ L the derivation rule

                                      M ⊢ varc (t, ¬φ) M ⊢ □dlf(¬φ)
                              E:
                                                 M ⊢ □♢ φ
is also sound.
     The derivation rule E allows us to reduce proofs of existence conditions to proofs of
formulae in first-order logic, if we can find appropriate c-variant terms for M . We will show
that this is always possible in some conservative refinement of M . Let us write varc (M, t, φ)
for the sentence varc (t, φ) to emphasise that the set of events E is taken from the Event-B
machine M .
Lemma 2.4. Let M be an Event-B machine with state variables v̄ = (v0 , ..., vm ) satisfying a
convergence property conv (φ). Then there exists an Event-B machine M ′ with state variables
v̄ ′ = (v̄, w̄, l, s, u), where v̄, w̄ = (w0 , . . . , wm ), l, s and u are pairwise different variables,
and a term t(v̄, w̄, l, s, u) such that:
     (i) The formula var c (M, t, φ) is valid for M ′ .
    (ii) For each trace σ of M there exists a trace σ ′ of M ′ with σ = σ ′ |s=1,v̄ and vice versa,
         where σ ′ |s=1,v̄ is the sequence of states resulting from the selection of those with s = 1
         and projection to the state variables v̄.
    The full proof has been outsourced to Appendix A, because it was already published in
the extended version of [FRS+ 24]. The main idea in it can be sketched briefly as follows.
The machine M ′ uses a copy w̄ of the state variables, and events are first executed on them.
24




Furthermore, M ′ uses a status variable s. As long as the machine M ′ is in a state satisfying
φ and s = 0 holds, the tuple w̄ is added to a list l. In case of a state satisfying ¬φ the
machine will switch to status s = 1. As there can only be finite subsequences of states
satisfying φ, such a status switch will occur, unless the machine runs into a deadlock. When
the status s = 1 is reached, the collected tuples in the list ℓ will be one-by-one copied to the
original state variables v̄, until finally the machine switches back to status s = 0. In this
way all firing of events are first executed on a copy w̄, and the length of the list l defines the
desired variant term, which is reset by each status switch from s = 0 to s = 1. In addition,
a few subtle cases concerning deadlocks need to be considered separately, for which another
status variable u is used.

2.2.2. Local Convergence. For TREBL we also need to investigate all diversified existence
formulae XY φ with X ∈ {□, □1 }, Y ∈ {♢, ♢1 } and (for now) φ ∈ L. We will proceed
analogously using a one-trace counterpart of convergence, for which we define a predicate
conv1 (φ) for φ ∈ L.
     It is tempting to define that M satisfies conv1 (φ) iff there exists a trace S0 , S1 , . . . of
M such that there is no k with Sℓ |= φ for all ℓ ≥ k. If such a trace were finite, the last
state Sk would satisfy ¬φ; if the claimed trace were infinite, there would be infinitely many
states Si with Si |= ¬φ. However, as we will see soon, this definition would be too weak for
the required proofs by means of variants.
     Instead, we must require that there is no “fantail” of states all satisfying φ. That is, we
say that M is locally convergent in φ iff there exists a trace S0 , S1 , . . . of M such that there
is no k with Sℓ′ |= φ for all ℓ ≥ k and all traces S0′ , S1′ , . . . of M with Si′ = Si for all i ≤ k.
We write M |= conv1 (φ), if M is locally convergent in φ.
     We will now show that local convergence can be proven by means of variant terms—in
this case we will call them lc-variants—and this will give rise to derivation rules for all
diversified existence formulae that use at least one one-trace temporal operator. For this
suppose that t(v̄) is again a well-formed term that takes values in some well-founded set V
with minimum 0, and let var1c (t, φ) denote the sentence
                                   _                                                             
           ∀v̄ φ(v̄) → t(v̄) ̸= 0 ∧   ∃x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧ t(v̄ ′ ) < t(v̄) . (2.2)
                                     ei ∈E

      We call the first-order sentence var1c (t, φ) an lc-variant formula, and the term t(v̄) is
called an lc-variant. Then var1c (t, φ) is satisfied iff for all states S, whenever φ holds, then
t(v̄) evaluates to a non-zero element in V and there is an enabled event ei , the execution of
which decreases t(v̄). We can show the following:
Lemma 2.5. If var1c (t, φ) is a valid formula for φ ∈ L, then M satisfies the local convergence
formula conv1 (φ), in other words, the derivation rule

                                             M ⊢ var1c (t, φ)
                                             M ⊢ conv1 (φ)
is sound.
Proof. Assume that M |= var1c (t, φ), but M ̸|= conv1 (φ). Then for all traces S0 , S1 , . . . of
M there is some k such that Sℓ′ |= φ for all ℓ ≥ k and all traces S0′ , S1′ , . . . that coincide on
the first k + 1 states with S0 , . . . , Sk . According to the definition of var1c (t, φ) we obtain
                                                                                                           25




for each such trace a strictly decreasing sequence vk > vk+1 > . . . of values in V . As V is
well-founded, this is impossible.
     Let us now look at the diversified one-trace existence formulae. A formula □1 ♢1 φ is
equivalent to ¬♢□¬φ, and the subformula ♢□¬φ expresses that all traces of M have a ¬φ
fantail, i.e. □1 ♢1 φ is equivalent to conv1 (¬φ). Therefore, a direct consequence of Lemma
2.5 is the soundness of the derivation rule
                                                   M ⊢ var1c (t, ¬φ)
                                        E11 :
                                                    M ⊢ □1 ♢1 φ
    Analogously, for a formula □♢1 φ we must have the absence of ¬φ fantails for all traces.
In particular, traces cannot terminate in states satisfying ¬φ. Therefore, another direct
consequence of Lemma 2.5 is the soundness of the derivation rule

                                        M ⊢ var1c (t, ¬φ)   M ⊢ □dlf(¬φ)
                            E01 :                           1
                                                      M ⊢ □♢ φ
    Thirdly, for a formula □1 ♢φ we must have the absence of ¬φ fantails for some trace,
and in addition in every trace we must have a state satisfying φ. Therefore, another direct
consequence of Lemma 2.5 is the soundness of the derivation rule

                                           M ⊢ var1c (t, ¬φ)  M ⊢ ♢φ
                                E10 :                       1
                                                    M ⊢ □ ♢φ
     To complete the investigation of diversified existence formulae we show the analogue
of Lemma 2.4, i.e. the existence of variant terms for local convergence in a conservatively
refined Event-B machine. The proof of the following lemma will be mostly identical to the
proof of Lemma 2.4 and will be given in Appendix A.
Lemma 2.6. Let M be an Event-B machine with state variables v̄ = (v0 , ..., vm ) satisfying
a local convergence property conv 1 (φ). Then there exists an Event-B machine M ′ with state
variables v̄ ′ = (v̄, w̄, l, s, u, c), where v̄, w̄ = (w0 , . . . , wm ), l, s, u and c are pairwise different
variables, and a term t(v̄, w̄, l, s, u, c) such that:
   (i) The formula var 1c (M, t, φ) is valid for M ′ .
  (ii) For each trace σ of M there exists a trace σ ′ of M ′ with σ = σ ′ |s=1,v̄ and vice versa,
       where σ ′ |s=1,v̄ is the sequence of states resulting from the selection of those with s = 1
       and projection to the state variables v̄.


2.2.3. Variants for Persistence Proofs. Analogously, M satisfies a persistence formula ♢□ φ
with φ ∈ L iff for every trace τ = S0 , S1 , . . . of M there is a k such that Sk′ |= φ for
every k ′ ≥ k. This implies that finite traces must terminate in a state Sℓ(τ )−1 satisfying φ.
Disregarding restriction for finite traces leads to divergence. We say that M is divergent in
φ—notation: M |= div(φ)—iff for every infinite trace τ = S0 , S1 , . . . of M there is a k such
that Sk′ |= φ for every k ′ ≥ k.
     The trivial extension M̃ is defined by adding an event that fires in a state S iff no other
event can be fired, i.e. S |= ¬dlf(true) holds, and then it does nothing. Formally, the guard
of this dummy event is ¬dlf(true), and the action is the list of assignments vi := vi for all
state variables vi . Note that if M̃ |= div(φ) holds, then also M |= div(φ) holds, but the
26




converse is false in general. However, if M |= div(φ) holds and all finite traces terminate in
a state satisfying φ, then also M̃ |= div(φ) follows.
    Hoang and Abrial showed that div(φ) can also be derived by means of variant terms
[HA11, p. 460]. For this suppose again that t(v̄) is a well-formed term that takes values in
some well-founded set V with minimum 0, and let vard (t, φ) denote the sentence
            ^                                                                                       
       ∀v̄       ∀x̄v̄ ′ ¬φ(v̄) ∧ Gi (x̄, v̄) → t(v̄) ̸= 0 ∧ (PAi (x̄, v̄, v̄ ′ ) → t(v̄ ′ ) < t(v̄))
              ei ∈E
                                                                                   
                                                               ′        ′
                        ∧ φ(v̄) ∧ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ) → t(v̄ ) ≤ t(v̄))    .                     (2.3)

     We call the first-order sentence vard (t, φ) a d-variant formula, and the term t(v̄) is called
a d-variant. Then vard (t, φ) is satisfied iff for all states S, whenever ¬φ holds and an event
ei is enabled, we have that t(v̄) evaluates to a non-zero element of V , and an execution of ei
decreases t(v̄), and whenever φ holds and an event ei is enabled, we have that an execution
of ei does not increase t(v̄). Hoang and Abrial showed the following:
Lemma 2.7. If vard (t, φ) is a valid formula, then M is divergent in φ, in other words, the
derivation rule
                                                 M ⊢ vard (t, φ)
                                                  M ⊢ div(φ)
is sound.
Proof. If M |= vard (t, φ), but M ̸|= div(φ), then by the definition of div(φ) there is an
infinite trace σ = S0 , S1 , . . . of M such that for all i there is some ki ≥ i with Ski |= ¬φ.
Let bj denote the value of t(v̄) in Sj . Then by the definition of vard (t, φ) we have bi ≥ bi+1
and bki > bki +1 for all i. As the order ≤ on V is well-founded, this is not possible.
     As div(φ) ∧ □dlf(¬φ) is equivalent to the existence formula ♢□ φ, an immediate conse-
quence of Lemma 2.7 is that for φ ∈ L the derivation rule

                                        M ⊢ vard (t, φ)  M ⊢ □dlf(¬φ)
                                P:
                                                    M ⊢ ♢□ φ
is sound for the derivation of persistence formulae.
     The derivation rule P allows us to reduce proofs of persistence formulae to proofs of
formulae in first-order logic, if we can find appropriate d-variant terms. We will show that
this is always possible in a conservative refinement of the machine M . Let vard (M, t, φ)
denote the formulae vard (t, φ) to emphasise the dependence of the specification of M .
Lemma 2.8. Let M be an Event-B machine with state variables v̄ = (v0 , ..., vm ) satisfying
a divergence property div (φ). Then there exists an Event-B machine M ′ with state variables
v̄ ′ = (v̄, c̄, b̄), where c̄ = (c0 , . . . , cm ), b̄ = (b0 , . . . , bm ) and v̄ are pairwise different variables,
and a term t(v̄, c̄, b̄) such that:
     (i) The formula var d (M ′ , t, φ) is valid for M ′ ;
    (ii) For each trace σ of M there exists a trace σ ′ of M ′ with σ = σ ′ |v̄ and vice versa, where
         σ ′ |v̄ is the sequence of states resulting from the projection to the state variables v̄.
    Again before entering into the proof let us sketch the key idea as follows. For V we
encode all values as hereditarily finite sets in HF(A), which is naturally ordered, and the
                                                                                                                         27




order is well-founded. In M ′ for each state variable vi we add a state variable ci , which we
initialise as ∅, and into which a new value v ′ is inserted, whenever the machine makes a
step in a state satisfying ¬φ. Then the tuple (c0 , . . . , cm ) is a monotone increasing sequence
of tuples of sets. As in every trace there are only finitely many states satisfying ¬φ, there
exists a maximum tuple that will never be exceeded. In M ′ we initialise (b0 , . . . , bm ) by
these maximum set values, and never update these state variables. As the order ≤ on HF(A)
subsumes set inclusion, we can see that #(b0 , . . . , bm ) − #(c0 , . . . , cm ) defines the desired
variant term. The full proof is given in Appendix A. It also appeared in the extended version
of [FRS+ 24].


2.2.4. Local Divergence. For TREBL we also need to investigate all diversified persistence
formulae Y Xφ with X ∈ {□, □1 }, Y ∈ {♢, ♢1 } and φ ∈ L. We first introduce a one-trace
analogue of divergence, for which we define a predicate div1 (φ) for φ ∈ L. We say that M
is locally divergent in φ (notation: M |= div1 (φ) iff there exists a trace S0 , S1 , . . . of M and
some k such that Sℓ |= φ holds for all ℓ ≥ k.
     We will now show that local divergence can also be proven by means of variant terms—in
this case we will call them ld-variants—and this will give rise to a derivation rule for one of
the diversified persistence formulae that uses both one-trace temporal operators. For this
suppose that t(v̄) is again a well-formed term that takes values in some well-founded set V
with minimum 0, and let var1d (t, φ) denote the sentence
                                         _                                                     
         ∀v̄ ¬φ(v̄) → t(v̄) ̸= 0 ∧ ∃x̄v̄ ′   Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧ t(v̄ ′ ) < t(v̄) ∧
                                                    ei ∈E
                                                                                                              
                     _                             _                                                      
                             Gi (x̄, v̄) → ∃x̄v̄ ′   Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧ t(v̄ ′ ) ≤ t(v̄)
                                        
       φ(v̄) ∧ ∃x̄                                                                                                 .   (2.4)
                     ei ∈E                         ei ∈E

     We call the first-order sentence var1d (t, φ) an ld-variant formula, and the term t(v̄) is
called an ld-variant. We can show the following:
Lemma 2.9. If var1d (t, φ) is a valid formula, then M is locally divergent in φ, in other
words, the derivation rule

                                                     M ⊢ var1d (t, φ)
                                                       M ⊢ div1 (φ)
is sound.
Proof. If M |= var1d (t, φ), but M ̸|= div1 (φ), then by the definition of div1 (φ) any trace
S0 , S1 , . . . of M is either finite terminating in a state Sk with Sk |= ¬φ or is infinite with
infinitely many Si satisfying Si |= ¬φ. The first case is excluded, because by the definition
of var1d (t, φ) there exists an event ei that can be fired in Sk . In the second case the definition
of var1d (t, φ) implies that there exists an infinite decreasing sequence of values in V . As the
order ≤ on V is well-founded, this is not possible.
     The diversified persistence formula ♢1 □1 φ holds for M iff there exists a trace that is
either finite and terminates in a state satisfying φ or it is infinite and there are only finitely
many states in the trace satisfying ¬φ. That is, the formula is equivalent to div1 (φ). Hence,
a direct consequence of Lemma 2.9 is the soundness of the derivation rule
28




                                                           M ⊢ var1d (t, φ)
                                               P11 :
                                                               M ⊢ ♢1 □1 φ
    We can again show that ld-variants exist in sufficiently refined machines, which will
imply relative completeness. The proof of the following lemma is given in Appendix A.
Lemma 2.10. Let M be an Event-B machine with state variables v̄ = (v0 , ..., vm ) satisfying
a local divergence property div 1 (φ). Then there exists an Event-B machine M ′ with state
variables v̄ ′ = (v̄, c̄, b̄), where c̄ = (c0 , . . . , cm ), b̄ = (b0 , . . . , bm ) and v̄ are pairwise different
variables, and a term t(v̄, c̄, b̄) such that:
   (i) The formula var 1d (M ′ , t, φ) is valid for M ′ ;
  (ii) For each trace σ of M there exists a trace σ ′ of M ′ with σ = σ ′ |v̄ and vice versa, where
       σ ′ |v̄ is the sequence of states resulting from the projection to the state variables v̄.
      This leaves the cases of diversified persistence formulae, in which one temporal operator
refers to all traces and the other one to just one trace. M satisfies ♢□1 φ iff in every trace
S0 , S1 , . . . of M there exists a k such that there is a trace S0′ , S1′ , . . . with Si′ = Si for all
i ≤ k and Sℓ |= φ for all ℓ ≤ k. In particular, all finite traces end in a state Sk satisfying φ.
      Phrased differently, every trace has a prefix S0 , . . . , Sk , and in the “fantail” starting
with Sk there is one trace with only finitely many states Sℓ satisfying ¬φ, and in case of a
finite trace terminating in a state satisfying φ. Therefore, let t1 and t2 be terms that take
values in well-founded sets V1 and V2 , respectively, and let the minimal elements in these
sets be denoted as 0. Then define the sentence varp1    d (t, φ) with t = (t1 , t2 ) as
                                                _
                                                    ∃x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧
                                                                                             
                    ∀v̄       t1 (v̄) ̸= 0 → ¬φ →
                                                         ei ∈E
                           ^                                                                    
                                  ∀x̄v̄ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) → t1 (v̄ ′ ) < t1 (v̄)
                                       ′

                          ei ∈E
                           ^                                                                 
                  ∧ φ(v̄) →   ∀x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) → t1 (v̄ ′ ) ≤ t1 (v̄)
                                  ei ∈E
                                        _                                                                   
                                           ∃x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧ t2 (v̄ ′ ) < t2 (v̄)
                                                                                                           
 ∧ t1 (v̄) = 0 → ¬φ(v̄) → t2 (v̄) ̸= 0 ∧
                                                       ei ∈E
          _                  _                                                                   !!
                                ∃x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧ t2 (v̄ ′ ) ≤ t2 (v̄)
                                                                                                
 ∧ φ(v̄) ∧   ∃x̄Gi (x̄, v̄) →                                                                         . (2.5)
                ei ∈E                      ei ∈E

   We call this sentence a pld-variant formula and the pair term t = (t1 , t2 ) a pld-variant18.
We can show the following lemma:
Lemma 2.11. For t = (t1 , t2 ) and φ ∈ L the derivation rule

                                                           M ⊢ varp1
                                                                  d (t, φ)
                                               P01 :
                                                               M ⊢ ♢□1 φ
is sound.
     18This notation is motivated by the formula being a modification of var1 (t, φ) with prefixes for all traces.
                                                                                      d
                                                                                                           29




Proof. Assume that M satisfies varp1    d (t, φ) with t = (t1 , t2 ). As V1 is well-founded, there
cannot be a trace with infinitely many states satisfying ¬φ; in such states any firing of an
event strictly decreases the value of t1 . Thus, in every trace we either have a state Sk with
Sℓ |= φ for all ℓ ≥ k or Sk |= t1 (v̄) = 0.
     For a state Sk satisfying t1 (v̄) = 0 there exists a continuation of the trace, which either
terminates in a state satisfying φ or in which the values of the term t2 decrease, and they
decrease strictly for each state satisfying ¬φ. As V2 is well-founded, there cannot exist a
trace with a strictly decreasing sequence of values for the term t2 , which implies that we
must reach a state Sk with Sℓ |= φ for all ℓ ≥ k. Hence M satisfies ♢□1 φ as claimed.
     Analogously, M satisfies ♢1 □φ iff there exists one trace S0 , S1 , . . . and some k such that
Sℓ |= φ holds for all ℓ ≥ k and all traces S0′ , S1′ , . . . with Si′ = Si for all i ≤ k. Informally
  ′

phrased, there exists a trace with a fantail of states all satisfying φ. Therefore, let t1 and t2
be terms that take values in well-founded sets V1 and V2 , respectively, and let the minimal
elements in these sets be denoted as 0. Then define the sentence varpd (t, φ) with t = (t1 , t2 )
as
                                               _
                      ∀v̄ t1 (v̄) ̸= 0 → ∃x̄v̄ ′      Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ )
                                                       ei ∈E
                                                                                        
                       ∧(¬φ(v̄) → t1 (v̄ ′ ) < t1 (v̄)) ∧ (φ(v̄) → t1 (v̄ ′ ) ≤ t1 (v̄))
                                                           ^
                                      ∧ t1 (v̄) = 0 →            ∀x̄v̄ ′
                                                               ei ∈E
                                                                                                  
                 ¬φ(v̄) ∧ Gi (x̄, v̄) → t2 (v̄) ̸= 0 ∧ (PAi (x̄, v̄, v̄ ′ ) → t2 (v̄ ′ ) < t2 (v̄))
                                                                                      
                                                            ′            ′
                     ∧ φ(v̄) ∧ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ) → t2 (v̄ ) ≤ t2 (v̄)          .          (2.6)

   We call this sentence a pd-variant formula and the pair term t = (t1 , t2 ) a pd-variant19.
We can show the following lemma:
Lemma 2.12. For t = (t1 , t2 ) and φ ∈ L the derivation rule

                                                       M ⊢ varpd (t, φ)
                                           P10 :
                                                         M ⊢ ♢1 □ φ
is sound.
Proof. Assume that M satisfies varpd (t, φ) with pd-variant t = (t1 , t2 ). As V1 is well-founded,
there cannot exist a trace, in which the values of t1 (v̄) form a strictly decreasing sequence.
Therefore, the first part of (2.6) implies that there exists a trace with a finite prefix of states
satisfying t1 (v̄) ̸= 0 or there exists a trace S0 , S1 , . . . and a k such that Sℓ |= φ holds for all
ℓ ≥ k.
     In the former case for every trace S0 , S1 , . . . continuing this prefix there must exist a k
such that Sℓ |= φ holds for all ℓ ≥ k. Otherwise the second part of (2.6) would yield an infinite
strictly decreasing sequence of values in V2 . As V2 is well-founded, this is impossible.
Remark 2.13. Negations of existence formulae are persistence formulae and vice versa, so
the question arises why for persistence four different types of variants are needed, whereas
  19This notation is motivated by the formula being a modification of var (t, φ) with a prefix for some trace.
                                                                               d
30




for existence we only needed two. It is possible to define also prefix versions for convergence
and local convergence, but these will be equivalent to conv(φ) or conv1 (φ).
    To conclude the investigation of persistence formulae we address the existence of pld-
and pd-variants in refined machines, and prove the analog of Lemmata 2.8 and 2.10 for these
cases.
Lemma 2.14. Let M be an Event-B machine with state variables v̄ = (v0 , ..., vm ) satisfying
a diversified persistence condition ♢1 □φ or ♢□1 φ, respectively. Then there exists an Event-B
machine M ′ with state variables v̄ ′ = (v̄, c̄, b̄, p̄, q̄, s), where c̄ = (c0 , . . . , cm ), b̄ = (b0 , . . . , bm ),
p̄ = (p0 , . . . , pm ), q̄ = (q0 , . . . , qm ) and v̄ are pairwise different variables and s is a fresh
Boolean-valued variable,and terms t1 (v̄, p̄, q̄) and t2 (v̄, c̄, b̄) such that:
      (i) The formula var pd (M ′ , t, φ) (or var p1    ′
                                                   d (M , t, φ), respectively) with t = (t1 , t2 ) is valid
          for M ′ ;
     (ii) For each trace σ of M there exists a trace σ ′ of M ′ with σ = σ ′ |v̄ and vice versa, where
          σ ′ |v̄ is the sequence of states resulting from the projection to the state variables v̄.
Proof. We exploit the same idea as for the proofs of Lemmata 2.8 and 2.10. However, for
each state variable vi we now add two state variables ci and pi , both initialised as ∅, and
we use an additional status variable s that is initialised to 0. Into pi we insert a new value
v ′ whenever vi is updated to v ′ in a state satisfying ¬φ ∧ s = 0, and we insert v ′ into ci
whenever vi is updated to v ′ in a state satisfying ¬φ ∧ s = 1. Furthermore, we initialise q̄ to
a tuple of maximum values that are never exceeded in the prefix(es) of the trace(s) that are
guaranteed by ♢1 □φ or ♢□1 φ, respectively, and we initialise b̄ to a tuple of maximum values
that are never exceeded in the postfix(es) of the trace(s) that are guaranteed by ♢1 □φ or
♢□1 φ, respectively. In case an insertion into pi exceeds qi , the status variable s is changed
to 1.
      We define the variant term t = (t1 , t2 ) with t1 (v̄, p̄, q̄) = (q0 − p0 , . . . , qm − pm ) and
t2 (v̄, c̄, b̄) = (b0 − c0 , . . . , bm − cm ). Then the detailed arguments to show conditions (i) and
(ii) are exactly the same as in the proofs of Lemmata 2.8 and 2.10.

2.2.5. Variants for Reachability Proofs. To complete our investigation of proofs of liveness
conditions by means of variant formulae we now look at reachability formulae ♢φ and ♢1 φ.
In the former case for every trace S0 , S1 , . . . there must exist some minimal k such that
all states Si with i < k satisfy ¬φ. Therefore, let t1 be a term that takes values in some
well-founded set V with minimal element 0, and assume that one state variable b takes
Boolean values. In particular, b = vi and b′ = vi′ hold for some i. Then we define the
sentence vare (t, φ) with t = (t1 , b) as
                           ^          
                      ∀v̄       ∀x̄v̄ ′ φ(v̄) ∧ b = 0 ∧ Gi (x̄, v̄) →
                                 ei ∈E
                                                                                             
                                                     ′           ′                ′
                                                                                       
                        t1 (v̄) ̸= 0 ∧ (PAi (x̄, v̄, v̄ ) → t1 (v̄ ) < t1 (v̄) ∧ b = 0)          .               (2.7)

   We call this sentence an e-variant formula and the pair term t = (t1 , b) an e-variant.
We can show the following lemma:
Lemma 2.15. If □vare (t, ¬φ) with t = (t1 , b) is a valid formula, then every trace of M with
an initial state satisfying b = 0 reaches a state satisfying φ, in other words, the derivation
rule
                                                                                                        31




                                       M ⊢b=0           M ⊢ vare (t, ¬φ)
                               R:
                                                     M ⊢ ♢φ
is sound.
Proof. If M |= vare (t, ¬φ) ∧ b = 0 holds, but M ̸|= ♢φ, then by definition of vare (t, ¬φ)
there is a trace S0 , S1 , . . . with Si |= ¬φ ∧ b = 0 for all i, and for the values bi of t(v̄) in Si
we have bi > bi+1 > . . . . As the order ≤ on V is well-founded, this is not possible.
    For a one-trace reachability formula ♢1 φ we also use a pair term t = (t1 , b) as above,
which we call e1-variant, and define an e1-variant formula as
                                         
                                     ∀v̄ φ(v̄) ∧ b = 0 → t1 (v̄) ̸= 0
                  _                                                                             
                ∧      ∃x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧ t1 (v̄ ′ ) < t1 (v̄) ∧ b′ = 0 . (2.8)
                   ei ∈E

     The following lemma is the analog of Lemma 2.15 for the case of reachability of a state
satisfying φ in one trace.
Lemma 2.16. If var1e (t, ¬φ) with t = (t1 , b) is a valid formula, then there exists a trace of
M with an initial state satisfying b = 0 that reaches a state satisfying φ, in other words, the
derivation rule
                                        M ⊢b=0          M ⊢ var1e (t, ¬φ)
                              R1 :
                                                     M ⊢ ♢1 φ
is sound.
Proof. If M |= var1e (t, ¬φ) ∧ b = 0 holds, then by definition either M |= φ—and hence
immediately M |= ♢1 φ—or there is a trace S0 , S1 , . . . and a k such that Si |= ¬φ ∧ b = 0
holds for all i ≤ k, and for the values bi of t(v̄) in Si we have bi > bi+1 > . . . . As the order
≤ on V is well-founded, there must exists a maximal k with this property, and by definition
we get Sk |= φ, hence M |= ♢1 φ.
    To conclude the investigation of reachability formulae we show that in the case of
reachability of a state S satisfying φ in all traces or in one trace, respectively, we can always
define a conservative refinement, in which an e-variant or e1-variant can be defined. The
proof of the following lemma is given in Appendix A.
Lemma 2.17. Let M be an Event-B machine with state variables v̄ = (v0 , ..., vm ) satisfying
a reachability property ♢φ or a one-trace reachability property ♢1 φ. Then there exists an
Event-B machine M ′ with state variables v̄ ′ = (v̄, w̄, l, s, u, b), where v̄, w̄ = (w0 , . . . , wm ), l,
s, u and b are pairwise different variables, and a term t1 (v̄, w̄, l, s, u) such that:
   (i) The formula var e (M, t, φ) (or var e (M, t, φ), respectively) with t = (t1 , b) is valid for
       M ′.
  (ii) For each trace σ of M there exists a trace σ ′ of M ′ with σ = σ ′ |s=1,v̄ and vice versa,
       where σ ′ |s=1,v̄ is the sequence of states resulting from the selection of those with s = 1
       and projection to the state variables v̄.
   Lemmata 2.1 – 2.17 above imply that adding the derivation rules INV1 , INV2 , INV11 ,
INV2 , E, E10 , E01 , E11 , P, P10 , P01 , P11 , R and R1 to a sound and complete set of derivation
   1

rules for first-order logic (with set types) yields a sound set of derivation rules for the
derivation of all-traces and one-trace invariance and reachability formulae, all versions of
32




existence formulae and all versions of existence formulae, provided that the Event-B machines
are conservatively refined to guarantee the existence of the required variants. We use the
notion of relative completeness here to emphasise that the required refinements depend on
the formulae that are to be proven. Of course, for a proof of an existence, persistence or
reachability property the appropriate variant must be defined; the lemmata above only
guarantee that this is always possible. In these cases we say that M is sufficiently refined.
Note that the extensions exploited in the Lemmata 2.4, 2.6, 2.8, 2.10, 2.14 and 2.17 above
are indeed (1, n)-refinements.

2.3. Progress Derivation Rules. The thorough investigation of different types of variants
in the previous subsection enables the derivation of existence, persistence and reachability
conditions in case the subformulae are in L20. This leaves us with the handling of progress
formulae □(φ → ♢ψ) and their diversification resulting from replacing one or both of the
temporal operators by their one-trace analog.
     Hoang and Abrial showed the soundness of two derivation rules for progress conditions
[HA11]. However, these rules contain arbitrary UNTIL-formulae that are not covered by
TREBL. Therefore, we combined the rules into a single sound derivation rule [FRS+ 24].
With this rule it was also possible to achieve relative completeness, but only under the
assumption that machines are tail-homogeneous [FRS+ 24].
     We will now go one step further and remove restrictions in the relative completeness
result in our previous work. For this we need to exploit some Lext formulae of the form □χ φ
with specific formulae φ, which is inspired by related work in the context of ASMs [FS24].
In a second step we will introduce simultaneous and conditional variants, which will then
allow us to dispense with formulae that refer to subsets of the set of traces.
Lemma 2.18. For formulae φ, ψ, χ ∈ L the derivation rules

            M ⊢ ♢¬ψ □¬χ M ⊢ leadsto(χ ∧ ¬ψ, χ ∨ ψ) M ⊢ □¬ψ (φ ∧ ¬ψ → χ)                                    and
                                 M ⊢ □(φ → ♢ψ)
          M ⊢ ♢¬ψ □¬χ M ⊢ □¬ψ leadslocto(χ ∧ ¬ψ, χ ∨ ψ) M ⊢ □¬ψ (φ ∧ ¬ψ → χ)
                                  M ⊢ □(φ → ♢ψ)
are sound for the derivation of progress properties in TREBL.
Proof. A trace τ of M that satisfies ♢□¬ψ either has finite length and terminates in a state
Sk satisfying ¬ψ or has an infinite tail of states all satisfying ¬ψ, i.e. there exists some k
such that Sℓ |= ¬ψ holds for all ℓ ≥ k. Hence a trace not satisfying ♢□¬ψ is either finite
terminating in a state satisfying ψ or contains infinitely many states Si satisfying ψ. In
such a trace whenever there is a state Si satisfying φ there also exists a state Sj with j ≥ i
satisfying ψ, so the condition for □(φ → ♢ψ) is satisfied.
     Therefore, we can concentrate on traces satisfying ♢□¬ψ. Assuming that M satisfies
the antecedents of the rule, for such traces S0 , S1 , . . . of M every state Si satisfies ♢□¬χ,
leadslocto(χ ∧ ¬ψ, χ ∨ ψ) and φ ∧ ¬ψ → χ. Consider a state Sk with Sk |= φ. If also Sk |= ψ
holds, the condition for □(φ → ♢ψ) is satisfied by definition.
    20An extension to nested temporal operators as foreseen in the definition of TREBL will be dealt with
later. In fact, we will see that this nesting does not add much expressive power, so it is questionnable whether
it is useful to include it in TREBL, but on the other side they do not increase the difficulty of the proofs
either.
                                                                                                         33




     Otherwise, for Sk |= ¬ψ the third antecedent of the rule implies Sk |= χ. The first
antecedent of the rule implies that there exists some m such that Sm′ |= ¬χ holds for all
m′ ≥ m.
     Let m be minimal with this property, in particular m > k. Then the second antecedent
                                                                   ′
of the rule implies that there exists some ℓ < m such that σ (ℓ ) |= χ ∧ ¬ψ holds for all
k ≤ ℓ′ ≤ ℓ. If we take ℓ maximal with this property, we must have Sℓ |= ψ by the definition
of transition formulae. This shows again that the condition for □(φ → ♢ψ) is satisfied,
hence M |= □(φ → ♢ψ) as claimed.
     Note that the antecedents of the second derivation rule in Lemma 2.18 are slightly
weaker than those of the first derivation rule. We will need this second rule for the proof of
relative completeness, whereas in examples it may be easier to use the first rule, in which
the second antecedent does not refer to a formula over a defined subset of the set of traces.


2.3.1. Simultaneous Variants. The derivation rule in Lemma 2.18 involves antecedents that
are not covered by TREBL. We will therefore investigate rules for the derivation of the
antecedents with antecedents in TREBL.
     First consider the antecedent ♢¬ψ □¬χ, but for reasons of generality consider formulae
of the form ♢ψ □χ instead. Such a formula requires that traces either converge in ψ or
otherwise terminate in a state satisfying χ or diverge in χ. Therefore, we consider a term t
that can serve simultaneously for convergence of ψ and divergence of χ, i.e. we need to have
varc (t, ψ) ∨ vard (t, χ). Equivalently, t is a term taking values in a well-founded set V , and
we define the simultaneous cd-variant formula svarcd (t, (ψ, χ)) as
                                                 _                                  
                                               ′                                   ′
                ∀v̄ ψ(v̄) → ¬χ(v̄) → ∃x̄v̄           (Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ )) ∧
                                                     ei ∈E
                                  
         ^                                                                                       
                ∀x̄v̄ Gi (x̄, v̄) → ¬χ(v̄) → t(v̄) ̸= 0 ∧ PAi (x̄, v̄, v̄ ′ ) → t(v̄ ′ ) < t(v̄)
                     ′

        ei ∈E
                                                                                !
                                                                          
                                                       ′        ′
                              ∧ χ(v̄) ∧ PAi (x̄, v̄, v̄ ) → t(v̄ ) ≤ t(v̄)          .                  (2.9)

Lemma 2.19. For formulae ψ, χ ∈ L the derivation rule

                                            M ⊢ svarcd (t, (ψ, χ))
                                                 M ⊢ ♢ψ □χ
is sound.
    An immediate consequence of this lemma is that in the derivation rules in Lemma 2.18
the first antecedent can be replaced by □svarcd (t, (¬ψ, ¬χ)), which is an invariance formula
and hence is also a TREBL formula.
Proof. Assume that M |= svarcd (t, (ψ, χ)) holds for an appropriate term t. Let τ = S0 , S1 , . . .
be a trace of M . As (2.9) does not impose any restriction on states satisfying ¬ψ, the trace
may be finite terminating in a state satisfying ¬ψ or there may be infinitely many states Si
with Si |= ¬ψ. Such traces do not satisfy the selection condition ⟨χ⟩.
    Traces that satisfy the selection condition either terminate in a state Sk with Sk |= ψ
or there exists a k such that Sℓ |= ψ holds for all ℓ ≥ k. The first condition in the formula
34




(2.9) implies that a trace can only terminate in a state Sk satisfying ψ, if also Sk |= χ holds;
otherwise, there would exists an event that is enabled in Sk . Therefore, we can concentrate
on infinite traces, for which we fix k with Sℓ |= ψ for all ℓ ≥ k.
     Consider the sequence of states Sk , Sk+1 , . . . . The second condition in (2.9) yields
an infinite, decreasing sequence bk , bk+1 , . . . of the values of the term t in the sequence
Sk , Sk+1 , . . . , which is only possible, if there are only finitely many states Si with i ≥ k and
Si |= ¬χ. Otherwise we would get an infinite, strictly decreasing subsequence contradicting
the well-foundedness of V .
     As for other types of variant terms we can show that simultaneous cd-variant term
always exist in sufficiently refined machines. As before we emphasise the dependence of the
simultaneous variant formula on the machine by adding the machine name as a parameter
to the variant formula. The proof of the following lemma is given in Appendix A.

Lemma 2.20. Let M be an Event-B machine with state variables v̄ = (v0 , ..., vm ) satisfying
♢ψ □χ with ψ, χ ∈ L. Then there exists an Event-B machine M ′ with state variables
v̄ ′ = (v̄, c̄, b̄), where c̄ = (c0 , . . . , cm ), b̄ = (b0 , . . . , bm ) and v̄ are pairwise different variables,
and a term t(v̄, c̄, b̄) such that:

      (i) The formula svarcd (M ′ , t, (ψ, χ)) is valid for M ′ ;
     (ii) For each trace σ of M there exists a trace σ ′ of M ′ with σ = σ ′ |v̄ and vice versa, where
          σ ′ |v̄ is the sequence of states resulting from the projection to the state variables v̄.

     The proof is given in Appendix A. The basic idea is to construct M ′ as in the proof on
Lemma 2.8 with the only difference that the values b0 , . . . , bm are the maximum set values
in traces satisfying the selection condition ⟨ψ⟩.




2.3.2. Conditional Variants. Consider the second antecedent □¬ψ leadslocto(χ ∧ ¬ψ, χ ∨ ψ)
and the third antecedent □¬ψ (φ ∧ ¬ψ → χ) in the second derivation rule in Lemma 2.18. In
both cases we are dealing with invariance conditions—a transition invariant in case of the
second antecedent and a state invariant in case of the third antecedent—restricted to traces
satisfying ♢□¬ψ. That is, as soon as a trace reaches a state violating the invariant, the trace
should either converge in ¬ψ, i.e. contain infinitely many states satisfying ψ, or terminate in
a state satisfying ψ. The convergence can be expressed analogously to the case of c-variants,
but in this case we need to add the condition that the invariance is violated. While this
would refer to states in a trace, we also need to add some form of bookkeeping, i.e. if there
has been a violation of the invariance condition in an earlier state of a trace, this should
also be taken into consideration. This can be simply done by requiring a Boolean-valued
state variable, which at most once in a trace changes its value, so that in traces without
any such change the invariance condition holds, while the other traces converge in ¬ψ or
terminate in a state satisfying ψ.
     We therefore define a conditional c-variant by a pair t = (t1 , b) of terms, where t1 takes
values in some well-founded set V and b is a Boolean-valued state-variable, which initially
should be 0. The corresponding conditional c-variant formula cvarc (t, ψ, θ) for the invariant
                                                                                                                                           35




θ = leadslocto(φ1 , φ2 ) is then defined as

                                                                     ^            
                    ∀v̄       ψ(v̄) →             b=0→                      ∀x̄v̄ ′ φ1 (v̄) ∧ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ )
                                                                    ei ∈E
                                                                                                                               
                                                                                        
                       → φ2 (v̄ ) ∧ b = 0 ∨ t1 (v̄) ̸= 0 ∧ t1 (v̄ ′ ) < t1 (v̄) ∧ b′ = 1
                                        ′         ′
                                         

                                          _
                                             ∃x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ )
                                                                                      
                              ∧ b=1→
                                                                 ei ∈E
                                                                                                                                  !
            ^                                                                                               
        ∧           ∀x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) → t1 (v̄) ̸= 0 ∧ t1 (v̄ ′ ) < t1 (v̄) ∧ b′ = 1
            ei ∈E
                                                                                                                    !
                              ^                                                                 
                          ∧           ∀x̄v̄ ′ ¬ψ(v̄) ∧ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) → b′ = b                          .            (2.10)
                              ei ∈E


    Analogously, for the invariant θ = φ ∧ ¬ψ → χ the corresponding conditional c-variant
formula cvarc (t, ψ, θ) is defined as

                                                                  ^             
                               ∀v̄           b=0→                        ∀x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) →
                                                                 ei ∈E
                                                                                    !
                      ′     ′       ′                                   ′
                                                                                    
                  θ(v̄ ) ∧ b = 0 ∨ b = 1 ∧ ψ(v̄) → t1 (v̄) ̸= 0 ∧ t1 (v̄ ) < t1 (v̄)      ∧
                                                                     _                                             
                          ∧ b=1→                      ψ(v̄) →               ∃x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧
                                                                    ei ∈E
                                                ^                 
                                                        ∀x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) →
                                                ei ∈E
                                                                                                           !!
                                                                                      
                                  b′ = 1 ∧ ψ(v̄) → t1 (v̄) ̸= 0 ∧ t1 (v̄ ′ ) < t1 (v̄)                                 .                (2.11)


    For later use also consider the case of a conditional c-variant formula cvarc (t, ψ, θ) for
the invariant θ = leadslocto1 (φ1 , φ2 ), which is defined as

                                            _                                                                 
  ∀v̄       ψ(v̄) →        b = 0 ∧ φ1 (v̄) →   ∃x̄v̄ ′ ∧ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧ φ2 (v̄ ′ ) ∧ b′ = 0
                                                                 ei ∈E
                                            ^                
                                                         ′
                                                                 Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧ ¬φ2 (v̄ ′ )
                                                                                                                
                                    ∧            ∀x̄v̄
                                        ei ∈E
                                                                                                           
                                                                                          
                                            → b′ = 1 ∧ t1 (v̄) ̸= 0 ∧ t1 (v̄ ′ ) < t1 (v̄)
36



                                         _
                                            ∃x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ )
                                                                                     
                                   ∧ b=1→
                                                    ei ∈E
                                                                                                        !
            ^
                       ′                                    ′                       ′
                                                                                                    
                                                                                                     ′
       ∧           ∀x̄v̄ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ) → t1 (v̄) ̸= 0 ∧ t1 (v̄ ) < t1 (v̄) ∧ b = 1
           ei ∈E
                                                                                                 !
                               ^                                                            
                                           ′                                    ′       ′
                           ∧           ∀x̄v̄ ¬ψ(v̄) ∧ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ) → b = b        .        (2.12)
                               ei ∈E

Lemma 2.21. Let φ, ψ, χ ∈ L and let θ be either leadslocto(χ ∧ ¬ψ, χ ∨ ψ), leadslocto1 (χ ∧
¬ψ, χ ∨ ψ) or φ ∧ ¬ψ → χ. For t = (t1 , b) the derivation rule
                                         M ⊢ (b = 0 ↔ θ)             M ⊢ cvarc (t, ¬ψ, θ)
                                                                M ⊢ □¬ψ θ
is sound.
Proof. Assume first that M |= cvarc (t, ¬ψ, leadslocto(χ ∧ ¬ψ, χ ∨ ψ)) holds. Consider an
arbitrary trace τ = S0 , S1 , . . . of M . Then (2.10) implies that there is some k such that for the
first k states Si of τ , i.e. 0 ≤ i < k (k may be 0), we have Si |= b = 0∧leadslocto(χ∧¬ψ, χ∨ψ).
Let k be maximal with this property.
      For k = ω all states of τ satisfy leadslocto(χ∧¬ψ, χ∨ψ). The same holds for k = ℓ(τ ) < ω.
Otherwise we get Sℓ |= b = 1 for all ℓ ≥ k, and τ can only terminate in a state satisfying
ψ. Furthermore, there cannot exist an infinite subsequence Sm , Sm+1 , . . . of states with
Si |= ¬ψ for all i ≥ m ≥ k, because otherwise we would obtain an infinite, strictly decreasing
sequence bm , bm+1 , . . . of values in V contradicting that V is well-founded. That is, the
trace must contain infinitely many states satisfying ψ and thus does not fulfil the selection
condition ⟨¬ψ⟩ for the traces, which shows that M |= □¬ψ leadslocto(χ ∧ ¬ψ, χ ∨ ψ) must
hold.
      For the analogous case that M |= cvarc (t, ¬ψ, leadslocto1 (χ ∧ ¬ψ, χ ∨ ψ)) holds, (2.12)
implies the existence of a trace τ = S0 , S1 , . . . such that Si |= b = 0∧leadslocto1 (χ∧¬ψ, χ∨ψ)
holds for all i. Furthermore, for all traces not satisfying this condition there exists some k
with Sℓ |= b = 1 for all ℓ > k. Then there cannot exist an infinite subsequence Sm , Sm+1 , . . .
of states with Si |= ¬ψ for all i ≥ m ≥ k, because otherwise we would obtain an infinite,
strictly decreasing sequence bm , bm+1 , . . . of values in V contradicting that V is well-founded.
Hence the trace does not fulfil the selection condition ⟨¬ψ⟩, which shows that M |=
□¬ψ leadslocto1 (χ ∧ ¬ψ, χ ∨ ψ) must hold.
      Next assume that M |= cvarc (t, ¬ψ, φ ∧ ¬ψ → χ) holds, and again let τ = S0 , S1 , . . .
be an arbitrary trace of M . Further assume that in the initial state S0 we either have
S0 |= b = 0 ∧ (φ ∧ ¬ψ → χ) or S0 |= b = 1 ∧ φ ∧ ¬ψ ∧ ¬χ. From (2.11) we obtain prefixes
S0 , . . . , Sk of τ with Si |= b = 0 ∧ (φ ∧ ¬ψ → χ) for all 0 ≤ i < k. Here k may be 0, in which
case the prefix is empty. Let k be maximal with this property.
      For k = ω or k = ℓ(τ ) < ω all states of τ satisfy φ ∧ ¬ψ → χ. Otherwise we get
Sℓ |= b = 1 for all ℓ ≥ k, and τ can only terminate in a state satisfying ψ. Same as in the
first case there cannot exist an infinite subsequence Sm , Sm+1 , . . . of states with Si |= ¬ψ
for all i ≥ m ≥ k. Hence M |= □¬ψ (φ ∧ ¬ψ → χ) must hold.
      An immediate consequence of Lemma 2.21 is that in the second derivation rule in
Lemma 2.18 the second and third antecedents can be replaced by the antecedents of
the rules in the lemma, which are formulae in L and hence are also TREBL formulae.
                                                                                                     37




That is, with φ, ψ, χ ∈ L, a simultaneous cd-variant t′ , a conditional c-variant t = (t1 , b),
γ1 = cvarc (t, ¬ψ, leadslocto(χ ∧ ¬ψ, χ ∨ ψ)) and γ2 = cvarc (t, ¬ψ, φ ∧ ¬ψ → χ) the following
is a sound derivation rule for TREBL:
            M ⊢ (b = 0 ↔ (φ ∧ ¬ψ → χ))           M ⊢ svarcd (t′ , (¬ψ, ¬χ)) M ⊢ γ1 M ⊢ γ2
    PR:
                                              M ⊢ □(φ → ♢ψ)
    To complete the investigation of conditional variants in the derivation rule PR for
progress formulae in TREBL we show that the required conditional variants always exists in
a sufficiently refined machine M ′ . The proof idea is analogous to the proof of Lemma 2.4
with a few modifications. The proof of the following lemma is given in Appendix A.
Lemma 2.22. Let M be an Event-B machine with state variables v̄ = (v0 , ..., vm ) satisfying
□¬ψ θ, where θ is either leadslocto(χ ∧ ¬ψ, χ ∨ ψ), leadslocto1 (χ ∧ ¬ψ, χ ∨ ψ) or φ ∧ ¬ψ → χ.
Then there exists an Event-B machine M ′ with state variables v̄ ′ = (v̄, w̄, l, s, u, b), where v̄,
w̄ = (w0 , . . . , wm ), l, s, u and b are pairwise different variables, and a term t1 (v̄, w̄, l, s, u)
such that:
   (i) The formula cvar c (M, t, ¬ψ, θ) with t = (t1 , b) is valid for M ′ .
  (ii) For each trace σ of M there exists a trace σ ′ of M ′ with σ = σ ′ |s=1,v̄ and vice versa,
       where σ ′ |s=1,v̄ is the sequence of states resulting from the selection of those with s = 1
       and projection to the state variables v̄.


2.3.3. Diversified Progress Formulae. We now consider the remaining diversified progress
formulae X(φ → Y ψ) with X ∈ {□, □1 }, Y ∈ {♢, ♢1 } and φ, ψ ∈ L. First consider the case
Y = ♢ and X = □1 . In this case we can simply modify one antecedent of the second rule
in Lemma 2.18, requesting validity not for a set of traces defined by ¬ψ, but only for a
single trace. This should give us three sound derivation rules for the derivation of progress
formulae of the form □1 (φ → ♢ψ).
Lemma 2.23. For formulae φ, ψ, χ ∈ L the following derivation rules are sound for the
derivation of one-trace progress properties in TREBL:

    M ⊢ ♢1 □(¬ψ ∧ ¬χ) M ⊢ □¬ψ leadslocto(χ ∧ ¬ψ, χ ∨ ψ) M ⊢ □¬ψ (φ ∧ ¬ψ → χ)
                                 M ⊢ □1 (φ → ♢ψ)
          M ⊢ ♢¬ψ □¬χ M ⊢ □1 leadslocto(χ ∧ ¬ψ, χ ∨ ψ) M ⊢ □¬ψ (φ ∧ ¬ψ → χ)
                                 M ⊢ □1 (φ → ♢ψ)
          M ⊢ ♢¬ψ □¬χ M ⊢ □¬ψ leadslocto(χ ∧ ¬ψ, χ ∨ ψ) M ⊢ □1 (φ ∧ ¬ψ → χ)
                                 M ⊢ □1 (φ → ♢ψ)
Proof. Consider the first rule and assume that M satisfies the three antecedents. The first
antecedent yields a trace S0 , S1 , . . . and some k such that Sℓ |= ¬ψ ∧ ¬χ holds for all ℓ ≥ k.
In particular, the trace satisfies the selection condition for the other antecedents. Let i
be such that Si |= φ holds. If no such i exists or if Si |= ψ holds, we immediately get
M |= □1 (φ → ♢ψ). Therefore, assume Si |= ¬ψ, hence also Si |= χ holds by the third
antecedent. Then the second antecedent implies that in every continuing trace with a ¬ψ
tail the following states satisfy χ until we reach a state satisfying ψ, which by the first
antecedent must exist.
38




      Next consider the second rule and assume that M satisfies its three antecedents. The
second antecedent yields a trace S0 , S1 , . . . with Si |= leadslocto(χ ∧ ¬ψ, χ ∨ ψ) for all i. We
can assume without loss of generality that the trace does not terminate in a state satisfying
ψ or contains infinitely many states satisfying ψ, because in such cases we immediately get
M |= □1 (φ → ♢ψ). As for the first rule we can further assume some k with Sk |= φ ∧ ¬ψ,
hence also Sk |= χ by the third antecedent. Then by second antecedent the following states
Sk+1 , . . . satisfy χ until we reach a state Sj with Sj |= ψ, and such j must exist due to the
first antecedent.
      Finally consider the third rule and let M satisfy its three antecedents. The third
antecedent yields a trace S0 , S1 , . . . with Si |= φ ∧ ¬ψ → χ for all i. Again, we can assume
without loss of generality that the trace does not terminate in a state satisfying ψ or
contains infinitely many states satisfying ψ, because in such cases M |= □1 (φ → ♢ψ) follows
immediately. Then without loss of generality take k with Sk |= φ ∧ ¬ψ, hence also Sk |= χ.
The second antecedent implies that the following states satisfy χ until we reach a state Sj
with Sj |= ψ, and such j must exist due to the first antecedent.
      Using the results on conditional variants we can replace antecedents in the rules of
Lemma 2.23 by the corresponding simultaneous cd-variant formula (2.9) or the conditional
c-variant formulae (2.10) and (2.11), respectively, which give us three derivation rules PR10    1 ,
PR102  and    PR  10 for the derivation of one-trace progress formulae of the form □1 (φ → ♢ψ)
                  3
with φ, ψ ∈ L. The antecedents of these rules are either in L or they are one-trace invariance
or persistence conditions.
      Next consider the case Y = ♢1 and X = □. In this case we can simply modify the
second antecedent of the second rule in Lemma 2.18 using leadslocto1 (χ ∧ ¬ψ, χ ∨ ψ) instead
of leadslocto(χ ∧ ¬ψ, χ ∨ ψ).
Lemma 2.24. For formulae φ, ψ, χ ∈ L the derivation rule

        M ⊢ ♢¬ψ □¬χ M ⊢ □¬ψ leadslocto1 (χ ∧ ¬ψ, χ ∨ ψ) M ⊢ □¬ψ (φ ∧ ¬ψ → χ)
                                M ⊢ □(φ → ♢1 ψ)
is sound for the derivation of progress properties in TREBL.
Proof. Without loss of generality as in the proof of Lemma 2.18 we can concentrate on traces
satisfying ♢□¬ψ. Assuming that M satisfies the antecedents of the rule, for such traces
S0 , S1 , . . . of M every state Si satisfies ♢□¬χ, leadslocto1 (χ ∧ ¬ψ, χ ∨ ψ) and φ ∧ ¬ψ → χ.
Consider a state Sk with Sk |= φ. If also Sk |= ψ holds, the condition for □(φ → ♢1 ψ) is
satisfied by definition.
      Otherwise, for Sk |= ¬ψ the third antecedent of the rule implies Sk |= χ. The first
antecedent of the rule implies that in at least one such trace there exists some m such that
Sm′ |= ¬χ holds for all m′ ≥ m.
      Let m be minimal with this property, in particular m > k. Then the second antecedent
of the rule implies that there exists some ℓ < m such that Sℓ′ |= χ ∧ ¬ψ holds for all
k ≤ ℓ′ ≤ ℓ. If we take ℓ maximal with this property, we must have Sℓ |= ψ by the definition
of transition formulae. This shows again that M |= □(φ → ♢ψ) holds as claimed.
      Combining Lemma 2.24 and the results in Lemmata 2.19 and 2.21 we obtain a sound
derivation rule for progress conditions of the form □(φ → ♢1 ψ). That is, with φ, ψ, χ ∈ L, a
simultaneous cd-variant t′ , a conditional c-variant t = (t1 , b), γ1 = cvarc (t, ¬ψ, leadslocto1 (χ∧
¬ψ, χ ∨ ψ)) and γ2 = cvarc (t, ¬ψ, φ ∧ ¬ψ → χ) the following is a sound derivation rule for
TREBL:
                                                                                                   39




             M ⊢ (b = 0 ↔ (φ ∧ ¬ψ → χ))   M ⊢ svarcd (t′ , (ψ, χ)) M ⊢ γ1 M ⊢ γ2
   PR01 :
                                     M ⊢ □(φ → ♢1 ψ)
     The existence of the required simultaneous and conditional variants in a sufficiently
refined machine has already been shown in Lemmata 2.20 and 2.22.
     This leaves the case of progress formulae of the form □1 (φ → ♢1 ψ). For these we can
simply modify one antecedent of the second rule in Lemma 2.24, requesting validity not for
a set of traces defined by ¬ψ, but only for a single trace. This should give us three sound
derivation rules.
Lemma 2.25. For formulae φ, ψ, χ ∈ L the following derivation rules are sound for the
derivation of one-trace progress properties in TREBL:

    M ⊢ ♢1 □(¬ψ ∧ ¬χ) M ⊢ □¬ψ leadslocto1 (χ ∧ ¬ψ, χ ∨ ψ) M ⊢ □¬ψ (φ ∧ ¬ψ → χ)
                               M ⊢ □1 (φ → ♢1 ψ)
         M ⊢ ♢¬ψ □¬χ M ⊢ □1 leadslocto1 (χ ∧ ¬ψ, χ ∨ ψ) M ⊢ □¬ψ (φ ∧ ¬ψ → χ)
                                M ⊢ □1 (φ → ♢1 ψ)
         M ⊢ ♢¬ψ □¬χ M ⊢ □¬ψ leadslocto1 (χ ∧ ¬ψ, χ ∨ ψ) M ⊢ □1 (φ ∧ ¬ψ → χ)
                                M ⊢ □1 (φ → ♢1 ψ)
Proof. Consider the first rule and assume that M satisfies the three antecedents. The first
antecedent yields a trace S0 , S1 , . . . and some k such that Sℓ |= ¬ψ ∧ ¬χ holds for all
ℓ ≥ k. In particular, the trace satisfies the selection condition for the other antecedents.
Let i be such that Si |= φ holds. If no such i exists or if Si |= ψ holds, we immediately
get M |= □1 (φ → ♢1 ψ). Therefore, assume Si |= ¬ψ, hence also Si |= χ holds by the
third antecedent. Then the second antecedent implies that there is a continuing trace with
(¬ψ ∧ ¬χ)-tail, in which the following states satisfy χ until we reach a state satisfying ψ,
and such a state must exist due to the first antecedent.
      Next consider the second rule and assume that M satisfies its three antecedents. The
second antecedent yields a trace S0 , S1 , . . . with Si |= leadslocto1 (χ ∧ ¬ψ, χ ∨ ψ) for all i. We
can assume without loss of generality that the trace does not terminate in a state satisfying
ψ or contains infinitely many states satisfying ψ, because in such cases we immediately get
M |= □1 (φ → ♢1 ψ). As for the first rule we can further assume some k with Sk |= φ ∧ ¬ψ,
hence also Sk |= χ by the third antecedent. Then by second antecedent the following states
Sk+1 , . . . satisfy χ until we reach a state Sj with Sj |= ψ, and such j must exist due to the
first antecedent.
      Finally consider the third rule and let M satisfy its three antecedents. The third
antecedent yields a trace S0 , S1 , . . . with Si |= φ ∧ ¬ψ → χ for all i. Again, we can assume
without loss of generality that the trace does not terminate in a state satisfying ψ or contains
infinitely many states satisfying ψ, because in such cases M |= □1 (φ → ♢1 ψ) follows
immediately. Then without loss of generality take k with Sk |= φ ∧ ¬ψ, hence also Sk |= χ.
The second antecedent implies that the following states satisfy χ until we reach a state Sj
with Sj |= ψ, and such j must exist due to the first antecedent.
      Using the results on conditional variants we can replace antecedents in the rules of
Lemma 2.25 by the corresponding simultaneous cd-variant formula (2.9) or the conditional
c-variant formulae (2.12) and (2.11), respectively, which give us three derivation rules PR11      1 ,
PR112  and    PR 11 for the derivation of one-trace progress formulae of the form □1 (φ → ♢1 ψ)
                 3
40




with φ, ψ ∈ L. The antecedents of these rules are either in L or they are one-trace invariance
or persistence conditions.
    To complete our investigation of progress formulae, we consider the following derivation
rule:
                                               M ⊢ XY ψ
                                    PR0 :
                                             M ⊢ X(φ → Y ψ)
    This rule is obviously sound for X ∈ {□, □1 } and Y ∈ {♢, ♢1 }; it complements the
derivation rules for all variants of progress formulae covering cases, where a progress condition
holds, because a stronger existence condition holds.
    However, for the case of X = □1 the antecedent in the rule PR0 is too strong. For
the proof of Theorem 3.2 later in this section we will need a stronger rule with weaker
antecedents. We observe that M |= □1 (φ → Y ψ) already holds, if there is a trace S0 , S1 , . . .
and some k such that Sk |= □1 Y ψ holds and Si |= ¬φ holds for all i < k; in other words
there may be a prefix of states satisfying ¬φ that can be ignored.
    Therefore, with a Boolean-valued state variable b we define a prefix formula pre(φ, b) as
       ^                                                                               
                 ′                             ′              ′                  ′
                                                                                      
  ∀v̄       ∀x̄v̄ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ) → (φ(v̄) → b = b) ∧ (¬φ(v̄) → b = 1)    . (2.13)
       ei ∈E

      Consider a machine satisfying pre(¬φ, b), and assume that in the initial state we have φ
iff b = 1 holds. The value of b can be updated at most once from 0 to 1, and this is only
possible, when we reached a state satisfying φ. Thus, the formula captures that there exists
a (possible empty) prefix of states all satisfying ¬φ. With this we obtain the following two
derivation rules:
                    M ⊢ (b = 1 ↔ φ)          M ⊢ pre(¬φ, b)  M ⊢ □1 ♢(b = 0 ∨ ψ)
           PR10
             0 :
                                             M ⊢ □1 (φ → ♢ψ)
                    M ⊢ (b = 1 ↔ φ)         M ⊢ pre(¬φ, b)    M ⊢ □1 ♢1 (b = 0 ∨ ψ)
          PR11
            0 :
                                            M ⊢ □1 (φ → ♢1 ψ)
     The soundness of these two rules is easy to see. Furthermore, for a machine M with a
trace S0 , S1 , . . . , which terminates in a state satisfying ψ or contains infinitely many Si with
Si |= ψ it is straightforward to construct a refinement M ′ with a Boolean state variable b
such that in the initial state we have b = 1 iff φ holds, and M ′ satisfies pre(¬φ, b) as well as
□1 Y (b = 0 ∨ ψ).

2.4. Nested Temporal Operators. So far we dealt with sound derivation rules for TREBL
formulae of the form Xφ, Y φ, XY φ, Y Xφ and X(ψ → Y φ) with X ∈ {□, □1 }, Y ∈ {♢, ♢1 },
and φ, ψ ∈ L, but the definition of TREBL also allows formulae with φ ∈ LT . Sound
derivation rules for nested temporal formulae are dealt with in Appendix B.

2.5. Examples. We describe a system with a single producer and a single consumer who
communicate through a shared buffer. The buffer acts as a temporary storage area but has a
limited capacity, N . The producer’s role is to add items to the buffer, while the consumer’s
role is to remove them. In this model, the consumer must first make a “request” to signal
its intent.
                                                                                                41




    variables                         invariants                       init
    buf // items in buffer            inv1: 0 ≤ buf ≤ N                begin
    req // consumer request?          inv2: req ∈ {0, 1}                    buf := 0
                                                                            req := 0
                                                                       end

    produce                           consumer request                 consumer fulfill
    when                              when                             when
         buf < N                           req = 0                          req = 1
    then                              then                                  buf > 0
         buf := buf + 1                    req := 1                    then
    end                               end                                   buf := buf − 1
                                                                            req := 0
                                                                       end
Liveness Properties: This model demonstrates the following types of “long-term guarantees”,
which ensure the system makes meaningful progress and does not get stuck:
• Progress (Guaranteed Service). This property ensures that a request made by the consumer
  will eventually be fulfilled. That is, a pending request will not be ignored indefinitely.
                                   □(req = 1 → ♢(req = 0))
• Existence (Recurring Availability). This property guarantees that the producer is not
  permanently blocked, ensuring the system does not reach a permanent state of gridlock
  where the buffer is full forever.
                                      □♢(buf < N )


Proof Construction for □(req = 1 → ♢(req = 0)). We use the rule PR for progress. First,
we instantiate φ, ψ, and χ with the following concrete formulae from our bounded buffer
model.
• The condition that triggers the need for progress is φ ≡ req = 1.
• The goal state we must eventually reach is ψ ≡ req = 0.
• The intermediate condition, χ, is chosen to be the state where progress becomes inevitable.
  In this simple example, this coincides with the need for progress, i.e., χ ≡ req = 1.
     Next, we define the simultaneous cd-variant t′ = N + 1 − buf + 2 · req and the conditional
c-variant t = (t1 , b), where t1 = N − buf and b = 0.
     Finally, we verify the premises of PR rule:
• Premise 1: M ⊢ (b = 0 ↔ (φ ∧ ¬ψ → χ)). By the definition of b we get that b = 0 is
  always true. Since furthermore (φ ∧ ¬ψ → χ) ≡ req = 1 → req = 1 is a tautology, we get
  that Premise 1 is verified.
• Premise 2: M ⊢ svarcd (t′ , (¬ψ, ¬χ)). For the simultaneous cd-variant t′ = N + 1 − buf +
  2 · req, we must check that svarcd (t′ , (req = 1, req = 0)) (cf. (2.9)) allays holds. Since this
  formulae is trivially true whenever req = 0, we only need to check the case when req = 1.
  That is, we need to prove that whenever req = 1, (i) there is an event that can be fired
  and that (ii) every event that can be fired strictly decreases t′ . Clearly (i) holds since
  either produce or consumer fulfill can be fired whenever req = 1. Regarding (ii), if
42




  produce is fired, then N − buf′ < N − buf and req′ = req, which strictly decreases t′ .
  If instead consumer fulfill is fired, then buf′ = buf − 1 but at the same time req′ = 0.
  The former increases t′ by 1, but the latter decreases it by 2, which strictly decreases t′ .
  Finally, the event consumer request cannot be fired whenever req = 1.
• Premise 3 M ⊢ γ1 . We must check that
                   cvarc (t, req = 1, leadslocto(req = 1, req = 1 ∨ req = 0)),
  defined as in (2.10), always holds. This boils down to checking that: (i) whenever req = 1
  and an event is fired, then either req′ = 1 or req′ = 0; and (ii) whenever req = 0 and an
  event is fired, then b = b′ . Both conditions are trivially satisfied since req′ ∈ {0, 1} by
  inv2 and b = b′ = 0 by definition of b.
• Premise 4: M ⊢ γ2 . We must check that
                              cvarc (t, req = 1, req = 1 → req = 1),
     defined as in (2.11), always holds. Since independently of any fired event, by our definition
     of b it holds that b = b′ = 0, and furthermore req = 1 → req = 1 is a tautology, this is
     trivially the case.



Proof Construction for □♢(buf < N ). Let χ ≡ buf = N ∧ req = 1. Note that ¬χ is
equivalent to φ ≡ buf < N ∨ req = 0.
     The term t(buf) = buf is a c-variant for χ: whenever χ holds (buf = N and req = 1)
the only enabled event is consumer fulfill, which strictly decreases t. Hence varc (t, χ)
holds. Moreover, states satisfying χ are not terminal (the enabled consumer fulfill can
fire), so Dlf(χ) holds.
     Applying rule E with ¬φ = χ yields
                                                          
                              M |= □♢ buf < N ∨ req = 0 ,
i.e. M |= □♢(¬χ).
     Inspecting the events of the machine we obtain the following instances of Leadsto
(Eq. (1.4)):
                                                                          
           M ⊢ Leadsto buf = N ∧ req = 0, χ ,     M ⊢ Leadsto χ, buf < N .
Indeed, from any state with buf = N ∧req = 0 the only enabled event is consumer request
whose effect is req′ = 1 and buf′ = N , hence the post-state satisfies χ; from any state
satisfying χ the only enabled event is consumer fulfill whose effect yields buf′ < N .
     From the two Leadsto facts and the definition of φ we obtain, for every state S,
                               S |= (buf < N ) ⇒ S |= ♢(buf < N ),
and
                           S |= (buf = N ∧ ¬req) ⇒ S |= ♢(buf < N ),
because the first case gives buf < N immediately, and the second case reaches χ in one
step and then buf < N in a further step (hence ♢♢(buf < N ), which is equivalent to
♢(buf < N )).
                                                                                            43




    Finally, since we have established that M |= □♢φ and M |= φ → ♢(buf < N ), we have
that every recurrence of φ produces a subsequent occurrence of buf < N . It follows that
M |= □♢(buf < N ).

    As an additional example, consider next the following persistence (Eventual Stability)
property:
                              ♢□(produced count = M ),
where the producer had a finite quota M of items to create. The objective is to guarantee
that the producer eventually completes its quota, after which the system remains in a state
where no further items are produced.
    To express this property, we must use a slightly extended version of the single produc-
er/consumer Event-B model introduced above. In particular, we introduce a new variable
produced count, initialized to 0, to track the number of items produced, and we extend the
invariants with produced count ∈ {0, . . . , M }. Moreover, the guard for the event produce
must be changed to
                            buf < N ∧ produced count < M,
ensuring that the quota is not exceeded. Triggering this event now increases not only buf
but also produced count.
    Naturally, in this modified model the earlier progress property no longer holds unless
we also adjust the guard of the event consumer request to
                              req = 0 ∧ produced count < M.



Proof Construction for ♢□(produced count = M ). We use the rule P for persistency to
prove that the producer eventually completes its quota of M items and the system persists
in a stable state.
    Define the formula
                               φ ≡ produced count = M
and the lexicographic d-variant:
                                                            
                        t = M − produced count, buf, 1 − req ,
with lexicographic order over N3 . This variant is well-founded as each component is a natural
number and decreases only finitely many times.
• Whenever ¬φ holds, produced count < M and at least one component of t strictly
  decreases when any enabled event fires: a) If buf < N , produce decreases the first
  component M − produced count. b) If buf = N and req = 0, only consumer request
  is enabled, which decreases the third component 1 − req. c) If buf > 0 and req = 1,
  consumer fulfill decreases the second component buf. Hence, the d-variant strictly
  decreases whenever produced count < M
• Whenever φ holds, the first component of the d-variant, i.e., M − produced count, equals
  0 and this cannot change as the guard of produce is false. Likewise, the guard of
  consumer request is also false. The event consumer fulfill might still fire (once),
  but this decreases the second component of the d-variant, i.e., buf. Thus, either the
  lexicographic value of t decreases or the run stops as no further event can be fired.
44




     Therefore, the d-variant formula vard (t, φ) is satisfied.
     Regarding deadlock freeness, whenever produced count < M , at least one event is
enabled: If buf < N , produce is enabled. If buf = N and req = 0, consumer request
is enabled. If buf > 0 and req = 1, consumer fulfill is enabled. Therefore, no deadlock
occurs while ¬φ holds.
     By the derivation rule P, we get M ⊢ ♢□(produced count = M ), establishing that the
system eventually reaches a stable state where the producer has completed its quota.

                                 3. Relative Completeness
Taking all our derivation rules together we obtain a sound system R of derivation rules
for TREBL formula, which comprises a sound and complete set of derivation rules for
first-order logic with types and the 63 derivation rules INV1 , INV2 , INV11 , INV12 , E, E11 ,
E10 , E01 , P, P11 , P10 , P01 , R, R1 , PR, PR11      11     11    10    10       10     01
                                               1 , PR2 , PR3 , PR1 , PR2 , PR3 , PR , PR0 ,
PR0 , PR0 , N, NPR, PRE, PRE , PRP, PRP , PRP , PRP , PR E, PR E , PR1 E10 ,
    10      11                        11            10       01      11   1         1 00

PR1 E01 , PR1 E11 , PR1 P, PR1 P00 , PR1 P10 , PR1 P01 , PR1 P11 , PPR, PPR11          11     11
                                                                              1 , PPR2 , PPR3 ,
PPR10          10      10         01  1      1  11    1   11    1  11   1   10    1
      1 , PPR2 , PPR3 , PPR , P PR, P PR1 , P PR2 , P PR3 , P PR1 , P PR2 , P PR3 ,
                                                                                      10    1 10
  1    01
P PR , PRPR and PR PR.      1

     Taking the lemmata in the previous section together we have already shown the following
theorem.
Theorem 3.1. The system R of derivation rules is sound for the derivation of TREBL
formulae, i.e. for any TREBL formula φ such that M ⊢R φ holds we have M |= φ.
      We now want to show the converse, i.e. that for M |= φ we can always obtain a
derivation with rules in R. However, whenever we need to apply a derivation rule that
involves variant formulae as antecedents, this is only possible, if the corresponding variant
terms are defined for the machine M . We therefore consider only machines M satisfying the
following conditions:
    (i) M is consistent, i.e. the initial state S0 satisfies the invariant ι, and whenever a state
        S satisfies ι, then this is also the case for all successor states of S defined by the events
        of M ;
   (ii) Every state formula φ in the logic L that holds in all reachable states is included in
        the invariant ι;
  (iii) M is sufficiently refined, i.e. all required variant terms can be defined in M .
      A machine M satisfying these three conditions will be called to satisfy the relativity
assumptions.
      We already emphasised in Section 1 that the consistency condition in (i) is stronger
than needed, as it requires the preservation of ι not only for reachable states, but for all
states. This is a work-around for the undecidability of reachability of states. In addition, the
assumption in condition (ii) allows us to reduce all invariance properties to the consistency
proof obligation, as ι → φ will hold for all states. Concerning condition (iii) we exploit the
lemmata in the previous section showing that we can always define a conservative refinement
of M , in which these variants exist. We say that we obtain relative completeness, if we can
show that whenever M |= φ holds for a machine M satisfying the conditions above and
TREBL formula φ, then there exists a derivation, i.e. M ⊢ φ holds.
      This will then be the crucial steps in the proof of the following theorem. The rest is
just done by induction, for which we use a well-founded order on TREBL formulae. For
                                                                                           45




arbitrary TREBL formulae φ we first define a rank r(φ) inductively (with X ∈ {□, □1 } and
Y ∈ {♢, ♢1 }) as follows:

           r(φ) = 0 for φ ∈ L      r(Xφ) = r(φ) + 1                 r(Y φ) = r(φ) + 1
       r(XY φ) = r(φ) + 2        r(Y Xφ) = r(φ) + 2       r(X(φ → Y ψ)) = r(ψ) + 3

    We then get the desired order letting φ ≤ ψ for r(φ) ≤ r(ψ) ̸= 0. In addition, we let
φ ≤ ψ, Xφ ≤ Xψ and Y φ ≤ Y ψ for φ, ψ ∈ L with |= φ → ψ. Then for all derivation rules
except INV2 and INV12 the antecedents have smaller rank than the conclusion.

Theorem 3.2. The system R of derivation rules is relative complete for TREBL, i.e. for
any TREBL formula φ such that M |= φ holds we have M ⊢R φ, provided that M satisfies
the relativity assumptions above.

Proof. Let φ ∈ LT and assume that M |= φ holds. We use induction over ≤ (where ≤ is
the well-founded order on the rank r(φ) defined just above) to show that M ⊢R φ holds.
For r(φ) = 0, i.e. φ ∈ L we immediately get M ⊢R φ, because R contains a complete set of
derivation rules for first-order logic with types. In the following assume r(φ) > 0. Then we
distinguish several cases.
     Invariance. Consider an invariance formula φ = □ψ with ψ ∈ L. Then for an arbitrary
trace τ = S0 , S1 , . . . of M we have Sk |= ψ for all k. According to our assumption ψ is
included in the invariant ι of M , hence |= ι → ψ holds, and by the induction hypothesis we
get ⊢R ι → ψ. Furthermore, as M is consistent, so we have M |= □ι, hence also M ⊢R □ι.
Then we can apply the derivation rule INV2 we get M ⊢R □ψ as claimed.
     Analogously, for φ = □1 ψ with ψ ∈ L there exists a trace τ = S0 , S1 , . . . of M with
Sk |= ψ for all k. Again we get ⊢R ι → ψ and M ⊢R □1 ι. Then we can apply the derivation
rule INV12 we get M ⊢R □ψ as claimed.
     Reachability. Consider a reachability formula φ = ♢ψ with ψ ∈ L. As we assume
that M is sufficiently refined, Lemma 2.17 implies that there exists an e-variant t = (t1 , b)
such that M |= vare (t, ¬ψ) and M |= b = 0 hold. by the induction hypothesis we get
M ⊢R vare (t, ¬ψ) and M ⊢R b = 0. Then with the derivation rule R we get M ⊢R ♢ψ as
claimed.
     The case of a reachability formula φ = ♢1 ψ with ψ ∈ L is handled analogously using
Lemma 2.17 and the derivation rule R1 .
     Existence. Consider an existence formula φ = □♢ψ with ψ ∈ L. As M is sufficiently
refined, Lemma 2.4 implies the existence of a c-variant t such that M |= varc (t, ¬ψ) holds.
Furthermore, for an arbitrary trace τ = S0 , S1 , . . . of M we have Sk |= ♢ψ for all k. In
particular, τ cannot terminate in a state satisfying ¬ψ, hence M |= dlf(¬ψ). by the induction
hypothesis we get M ⊢R varc (t, ¬ψ) and M ⊢R dlf(¬ψ). Then we can apply the derivation
rule E, which yields M ⊢R φ as claimed.
     For an existence formula of the form φ = □1 ♢1 ψ with ψ ∈ L Lemma 2.6 implies the
existence of an lc-variant t such that M |= var1c (t, ¬ψ) holds. by the induction hypothesis
we get M ⊢R var1c (t, ¬ψ), and then we can apply rule E11 to get M ⊢R φ.
     Analogously, for φ = □1 ♢ψ or φ = □♢1 ψ with ψ ∈ L, respectively, we get an lc-variant
t from Lemma 2.6 such that M |= var1c (t, ¬ψ) holds. In the former case we must have in
addition M |= ♢ψ, and in the latter case we have M |= dlf(¬ψ). by the induction hypothesis
we get M ⊢R var1c (t, ¬ψ) and either M ⊢R ♢ψ or M ⊢R dlf(¬ψ), respectively. This allows
us to apply rule E10 or rule E01 , respectively, to yield M ⊢R φ.
46




     Persistence. Consider a persistence formula φ = ♢□ψ with ψ ∈ L. For an arbitrary
trace τ = S0 , S1 , . . . of M there exists some k such that Sℓ |= ψ holds for all ℓ ≥ k. In
particular, τ cannot terminate in a state satisfying ¬ψ, i.e. M |= dlf(¬ψ) must hold.
Furthermore, as M is assumed to be sufficiently refined, Lemma 2.8 implies the existence
of a d-variant t such that M |= vard (t, ψ) holds. by the induction hypothesis we get
M ⊢R vard (t, ψ) and M ⊢R dlf(¬ψ). We can apply rule P, which yiels M ⊢R φ as claimed.
     For diversified persistence formulae we proceed analogously. For φ = ♢1 □ψ with ψ ∈ L
we can use Lemma 2.10, hence there exists an ld-variant t such that M |= var1d (t, ψ) holds.
For φ = ♢□1 ψ with ψ ∈ L we can use Lemma 2.14, hence there exists a pld-variant
t = (t1 , t2 ) such that M |= varp1                             1
                                     d (t, ψ) holds. For φ = ♢ □ψ with ψ ∈ L we can also use
Lemma 2.14, which gives us a pd-variant t = (t1 , t2 ) such that M |= varpd (t, ψ) holds. In
these three cases we get M ⊢R var1d (t, ψ), M ⊢R varp1                       p
                                                         d (t, ψ) or M ⊢R vard (t, ψ), respectively,
by the induction hypothesis. Then we can apply the rules P11 , P01 and P10 , respectively,
which imply M ⊢R φ.
     Progress. Next consider a progress formula φ = □(φ1 → ♢φ2 ) with φ1 , φ2 ∈ L. Let
τ = S0 , S1 , . . . be a trace of M , and assume that there exists a k such that Sℓ |= ¬φ2 holds
for all ℓ ≥ k. According to Lemma 2.18 other traces can be ignored. We can also assume
that at least one such trace exists. Otherwise, M |= □♢φ2 holds, and by the induction
hypothesis we get M ⊢R □♢φ2 . We can apply rule PR0 , which gives us M ⊢R □(φ1 → ♢φ2 )
as claimed.
     Then τ contains only a finite number of states satisfying φ2 . We consider all states in
these traces that satisfy ¬φ2 and for which there exists a later state satisfying φ2 . Let φ3
be a common invariant for these states. More precisely, for a state S satisfying ¬φ2 take its
type, i.e. the set of all formulae in L that hold in S, let φS be an isolating formula for this
type, and define φ3 as the disjunction of all these formulae φS .
     Then by construction M |= □¬φ2 leadslocto(φ3 ∧ ¬φ2 , φ3 ∨ φ2 ) holds. As M is sufficiently
refined, we can apply Lemma 2.21, hence there exists a conditional c-variant t = (t1 , b) such
that M |= cvarc (t, ¬φ2 , leadslocto(φ3 ∧ ¬φ2 , φ3 ∨ φ2 )) holds. By the induction hypothesis
we have M ⊢R cvarc (t, ¬φ2 , leadslocto(φ3 ∧ ¬φ2 , φ3 ∨ φ2 )).
     If a trace has an tail of states satisfying ¬φ2 , these states must also satisfy ¬φ1 . Then
our construction implies that M |= □¬φ2 (φ1 ∧ ¬φ2 → φ3 ) holds. As M is sufficiently
refined, we can apply Lemma 2.21, hence there exists a conditional c-variant t = (t1 , b)
such that M |= cvarc (t, ¬φ2 , φ1 ∧ ¬φ2 → φ3 ). By the induction hypothesis we get M ⊢R
cvarc (t, ¬φ2 , φ1 ∧ ¬φ2 → φ3 ).
     Furthermore, as M is sufficiently refined, then for all traces τ that are divergent in
¬φ2 Lemma 2.8 implies the existence of a variant term t(v̄) such that vard (t, ¬φ1 ∧ ¬φ2 ) is
valid, in particular, t(v̄) > vmin is included in φ3 , and t(v̄) = vmin holds in all tailing states
satisfying ¬φ1 ∧ ¬φ2 . This implies M |= ♢¬φ2 □¬φ3 . We can apply Lemma 2.19 to get a
simultaneous cd-variant t′ such that M |= svarcd (t′ , (¬φ2 , ¬φ3 )). Then by the induction
hypothesis we get M ⊢R svarcd (t′ , (¬φ2 , ¬φ3 )). Finally, we can apply rule PR, which yields
M ⊢R □(φ1 → ♢φ2 ) as claimed.
     For a progress formula φ = □(φ1 → ♢1 φ2 ) with φ1 , φ2 ∈ L we can assume without loss
of generality that M ̸|= □♢1 φ2 holds. Otherwise by the induction hypothesis we would get
M ⊢R □♢1 φ2 , which allows us to apply rule PR0 to obtain M ⊢R □(φ1 → ♢1 φ2 ) as claimed.
     We concentrate again on traces τ = S0 , S1 , . . . of M such that there exists a k such that
Sℓ |= ¬φ2 holds for all ℓ ≥ k. According to Lemma 2.24 other traces can be ignored. Then
                                                                                                    47




we construct the formula φ3 analogously, but we only consider states in traces S0 , S1 , . . .
such that whenever Sk |= φ1 holds, also Sℓ |= φ2 holds for some ℓ ≥ k. Every state satisfying
φ2 appears in at least one such trace.
      By construction we get M |= □¬φ2 leadslocto1 (φ3 ∧ ¬φ2 , φ3 ∨ φ2 ). Furthermore, we get
immediately M |= □¬φ2 (φ1 ∧ ¬φ2 → φ3 ) and M |= ♢¬φ2 □¬φ3 using the same arguments as
above. As M is sufficiently refined, we can apply Lemmata 2.19 and 2.21, i.e. there exists a
simulataneous cd-variant t and a conditional c-variant t′ such that M |= svarcd (t, (¬φ2 , ¬φ3 ))
and M |= cvarc (t′i , ¬φ2 , θi ) for θ1 = φ1 ∧ ¬φ2 → φ3 and θ2 = leadslocto1 (φ3 ∧ ¬φ2 , φ3 ∨ φ2 ).
      By the induction hypothesis we get that M ⊢R svarcd (t, (¬φ2 , ¬φ3 )) and M ⊢R
cvarc (t′i , ¬φ2 , θi ) (i = 1, 2), which allows us to apply rule PR01 to infer M ⊢R □(φ1 → ♢1 φ2 )
as claimed.
      Next consider diversified progress formulae φ = □1 (φ1 → ♢φ2 ). We can assume that
there exists at least one trace of M , for which there exists a k such that Sℓ |= ¬φ2 holds
for all ℓ ≥ k. Otherwise M |= □♢ψ holds, and by the induction hypothesis we would get
M ⊢R □♢ψ. Then M ⊢R φ would follow immediately using rule PR0 .
      Assuming that M |= φ holds there exists a trace S0 , S1 , . . . of M such that Si |= φ1 →
♢φ2 holds for all i. Let us first assume that there is some k with Sℓ |= ¬φ2 for all ℓ ≥ k.
Then also Sℓ |= ¬φ1 holds for all ℓ ≥ k.
      Case 1. Assume that there exists a trace S0′ , S1′ , . . . and some k such that Sk′ |= φ1
and Sℓ′ |= ¬φ2 hold for all ℓ ≥ k. This cannot be the trace S0 , S1 , . . . . Then we consider all
finite subtraces Si′ , . . . , Sj′ of all traces with ¬φ2 -tail such that Si′ |= φ1 , Sx |= ¬φ2 for all
i ≤ x ≤ j, Sj+1 ′      |= φ2 and Si′ = Si . Consider all states Sx′ appearing in such subtraces, and
let φ3 be a common invariant, constructed as above.
      Then M |= □1 (φ1 ∧ ¬φ2 → φ3 ) holds, because φ1 ∧ ¬φ2 → φ3 is satisfied by all states Si .
Also M |= □¬φ2 leadslocto(¬φ2 ∧ φ3 , φ2 ∨ φ3 ) holds by construction, because in the selected
set of traces that states satisfying ¬φ2 ∧ φ3 are just the states used for the definition of φ3 ,
and the defining subtraces have been chosen such that they are always followed by a state
satisfying φ2 , and such a state must exists for all the subtraces with a start state Si′ = Si .
Furthermore, M |= ♢¬φ2 □¬φ3 holds by construction of φ3 .
      Then by Lemmata 2.19 and 2.21 there exist a simultaneous cd-variant t and a condi-
tional c-variant t′ such that M |= svarcd (t, (¬φ2 , ¬φ3 )) and M |= cvarc (t′i , ¬φ2 , θ) for θ =
leadslocto(φ3 ∧ ¬φ2 , φ3 ∨ φ2 ). By the induction hypothesis we get M ⊢R □1 (φ1 ∧ ¬φ2 → φ3 ),
M ⊢R svarcd (t, (¬φ2 , ¬φ3 )) and M ⊢R cvarc (t′i , ¬φ2 , θ). Then we can apply rule PR10    3 , which
yields M ⊢R φ.
      Case 2. Now assume that no such trace as in Case 1 exists, in particular, the states
in a ¬φ2 -tail also satisfy ¬φ1 . As in Case 1 consider subtraces Si′ , . . . , Sj′ of all traces with
¬φ2 -tail without requiring Si′ = Si , and construct again φ3 as a common invariant of all
states Sx′ appearing in such subtraces. We consider two subcases.
      Case 2a. First assume that there is no trace in the set of selected traces that contains a
state Sx′ satisfying φ3 and a successor state Sx+1   ′   satisfying ¬φ3 . Note that such a trace could
only exist, if Sℓ |= ¬φ2 holds for all ℓ ≥ x. Then M |= □¬φ2 leadslocto(¬φ2 ∧ φ3 , φ2 ∨ φ3 )
                     ′

still holds by construction. In addition, M |= □¬φ2 (φ1 ∧ ¬φ2 → φ3 ) holds, because states in
the tail of the traces under consideration do not contain states satisfying φ1 . Furthermore,
M |= ♢1 □(¬φ2 ∧ ¬φ3 ) holds, as the defining condition is satisfied by the trace S0 , S1 , . . . .
      As M is sufficiently refined, we can again exploit Lemma 2.21. Hence there exist
conditional c-variants t′i such that M |= cvarc (t′i , ¬φ2 , θi ) for θ1 = φ1 ∧ ¬φ2 → φ3 and
θ2 = leadslocto(φ3 ∧¬φ2 , φ3 ∨φ2 ). By the induction hypothesis we get M ⊢R cvarc (t′i , ¬φ2 , θi )
48




for i = 1, 2 as well as M ⊢R ♢1 □(¬φ2 ∧ ¬φ3 ). Hence, we can apply rule PR10        1 , which implies
again M ⊢R φ.
     Case 2b. Finally, assume that there exists a trace in the set of selected traces that
contains a state Sx′ satisfying φ3 and a successor state Sx+1       ′    satisfying ¬φ3 . Then still
         1
M |= □ leadslocto(¬φ2 ∧ φ3 , φ2 ∨ φ3 ) still holds by construction, as the defining condition
holds for the trace S0 , S1 , . . . . Also M |= □¬φ2 (φ1 ∧ ¬φ2 → φ3 ) still holds, because states in
the tail of the traces under consideration do not contain states satisfying φ1 . Furthermore,
M |= ♢¬φ2 □¬φ3 holds by construction of φ3 .
     Then by Lemmata 2.19 and 2.21 there exist a simultaneous cd-variant t and a con-
ditional c-variant t′ such that M |= svarcd (t, (¬φ2 , ¬φ3 )) and M |= cvarc (t′i , ¬φ2 , θ) for
θ = φ1 ∧ ¬φ2 → φ3 . By the induction hypothesis we get M ⊢R svarcd (t, (¬φ2 , ¬φ3 )),
M ⊢R cvarc (t′i , ¬φ2 , θ) and M ⊢R □1 leadslocto(¬φ2 ∧ φ3 , φ2 ∨ φ3 ). Hence, we can apply
rule PR102 , which implies again M ⊢R φ.
     Finally, if the trace S0 , S1 , . . . terminates in a state satisfying φ2 or Si |= φ2 holds for
infinitely many i, there exists a Boolean-valued variable b such that M |= (b = 1 ↔ φ1 ),
M |= pre(¬φ1 , b), and M |= □1 ♢(b = 0 ∨ φ2 ) hold. By the induction hypothesis we get
M ⊢R (b = 1 ↔ φ1 ), M ⊢R pre(¬φ1 , b), and M ⊢R □1 ♢(b = 0 ∨ φ2 ), so we can apply rule
PR100 to get M ⊢R φ.
     The case of diversified progress formulae φ = □1 (φ1 → ♢1 φ2 ) is handled analogously.
We only need to replace leadslocto by leadslocto1 and apply the rules PR11            j (1 ≤ j ≤ 3)
from Lemma 2.25 instead of the rules from Lemma 2.23, or rule PR11            0 .
     Nested Temporal Formulae. The extension to TREBL formulae that result from
multiple application of the constructors in Definition 1.2 is handled in Appendix B.



                              4. Discussion and Conclusions
In this article we developed a temporal Event-B logic and showed the existence of a sound
and relative complete set of derivation rules. First attempts in this direction go back to
the work of Hoang and Abrial, who discovered a simple set of sound derivation rules that
can be used to prove invariance, existence, progress and persistence conditions that are to
hold for all traces of an Event-B machine [HA11]. Their work was grounded on coupling the
UNTIL-fragment of LTL [Pnu77] with the logic of Event-B—the resulting logic was called
LTL(EB) in [FRS+ 24]—by means of which they could get rid of the intrinsic restriction
of LTL being in essence an extension of propositional logic. However, they preserved the
semantics of LTL, i.e. the interpretation of temporal formulae over arbitrary traces, so they
gained expressiveness and mechanical proof capability at the cost of losing completeness.
However, completeness is essential to ensure that a proof by means of derivation rules can
actually be conducted.
     Completeness for a fragment of LTL(EB) large enough to cover the most important
liveness conditions was addressed in our previous work [FRS+ 24], where we could show that
under some restrictions the derivation rules discovered by Hoang and Abrial with some
small modifications are relative complete for this fragment. That is, if a consistent Event-B
machine M is sufficiently refined, and M satisfies a formula in the fragment, then there also
exists a derivation for this formula. In other words, if there exists a proof of some liveness
condition, the proof can be done by using the derivation rules, provided that certain variant
terms are explicitly defined for M . The crucial point is to show that this is always possible,
                                                                                                             49




which reflects the intuitively clear fact, that any condition that holds for a machine must in
some way be reflected explicitly or implicitly in the specification.
     Still the work in [FRS+ 24] was insufficient, as the relative completeness result was
restricted to machines that are tail-homogeneous21, and the semantics definition does not
reflect the decisive fact that for a given Event-B machine any valid state S determines
already the traces starting in S. That is, if the building of successor states and successors
of successors, etc. is taken into the logic, we can obtain a logic that allows us to express
temporal properties, but is interpreted over states rather than traces, which is a significant
simplification and also removes the necessity to distinguish between state formulae and
temporal formulae. In this article we removed all these restrictions.
     A parallel treatment based on Abstract State Machines [FS24] defines a temporal
extension of the logic of non-deterministic ASMs [FSTW18], in which update sets defining
successor states are used as first class objects22, so it becomes possible to reason about
successor states, successors of successors, etc. In order to obtain formulae that express
properties of complete runs it was sufficient to extend the building of update sets to arbitray
sequences of steps. In doing so, all relevant temporal operators known from LTL or also
CTL [CE82] could be defined in the logic, so they are merely shortcuts for rather complex
formulae. Also, definable teams of traces (capturing the spirit of team semantics [GMOV22])
can be integrated, though this was only done for restricted cases.
     We concluded that it is a very promising idea to integrate the essential ideas of the
modal extensions of the logic of ASMs into our treatment of a temporal logic for Event-B.
As Event-B is grounded in the theory of sets, it is straightforward to define update sets,
and also the inductive definition of update sets expressing the changes of multiple steps
is straightforward. In this way we obtained an extension Lext of the logic of Event-B, in
which all temporal operators for all traces, for a single trace or for selected definable sets
of traces can be defined. This is the basis for the definition of TREBL as a sound and
relative complete fragment of Lext . The definable sets of traces allow us to remove the
tail-homogeneity restriction.
     We consider the definition of a sound and relative complete temporal logic for Event-B
a major breakthrough. The usefulness of known temporal logics such as LTL, CTL or
CTL∗ for the verification of liveness conditions of real systems is severely restricted by the
propositional nature of these logics. The tight coupling of temporal logic with Event-B
removes these restrictions, and allows us to obtain not only sound derivation rules, but also
relative completeness. Surely, proofs may require the definition of appropriate variant terms
as part of an Event-B specification, but proofs of complex conditions are never for free. We
only need to exploit two simple facts:
• States of a machine determine traces starting in that state, so the logic can be defined
  in a way that formulae are interpreted over states and temporal operators are merely
  shortcuts23.

   21Tail homogeneity requires that either all traces are divergent for state formulae appearing in the liveness
conditions to be proven or none.
   22This defines a complete second-order logic with Henkin semantics.
   23Leslie Lamport characterised the explicit quantification over the number of steps as evil and recommended
to stick to temporal logics as the lesser evil [Lam10]. Indeed, the defining formulae for the temporal operators
may appear horrible, but in TREBL they are not used. Once defined the temporal operators as in any other
temporal logic, but formulae are nonetheless interpreted over states and express properties of traces starting
in such states.
50




• Variant terms that are needed for the proofs can be made explicit by means of refinement.
    In addition to the theory of TREBL we are in the (almost completed) process of
integrating all our derivation rules into the RODIN proof tool using the EB4EB meta-theory,
which will be reported in a forthcoming Part II of our work. In doing so we provide a
desirable mechanical proof suppport for TREBL. We further demonstrated the power of
TREBL on various examples, in particular examples adressing security aspects. Some of
these conditions such as non-interference were considered to be very challenging, but in the
TREBL context they become almost trivial.
    During the development of this research we often discovered that we most likely could
further extend TREBL. For instance, it should be possible to also include UNTIL formulae
in the logic or try to integrate arbitrary definable teams of traces. Also the quantification
over traces is limited, and it seems likely that it can be handled more generally. As our
treatment until now has already grown significantly, we keep further extensions to TREBL
including sound derivation rules and a proof of relative completeness for future research.
    As a final remark it is clear that while our work here is based on Event-B, it should
be possible to conduct analogous research for any other state-based rigorous method. In
particular, the two decisive facts mentioned above are not bound to Event-B.


                                            References
[Abr10a]  Jean-Raymond Abrial. The B-book – Assigning programs to meanings. Cambridge University
          Press, 2010. doi:10.1017/CBO9780511624162.
[Abr10b] Jean-Raymond Abrial. Modeling in Event-B – System and Software Engineering. Cambridge
          University Press, 2010. doi:10.1017/CBO9781139195881.
[Bis09]   Joachim Biskup. Security in Computing Systems – Challenges, Approaches and Solutions. Springer,
          2009. doi:10.1007/978-3-540-78442-5.
[BS03]    Egon Börger and Robert Stärk. Abstract State Machines – A Method for High-Level System Design
          and Analysis. Springer, Berlin Heidelberg New York, 2003. doi:10.1007/978-3-642-18216-7.
[CE82]    Edmund M. Clarke and E. Allen Emerson. Design and synthesis of synchronization skeletons
          using branching-time temporal logic. In Dexter Kozen, editor, Logics of Programs, volume 131 of
          Lecture Notes in Computer Science, pages 52–71. Springer, 1982. doi:10.1007/BFB0025774.
[CFK+ 14] Michael R. Clarkson, Bernd Finkbeiner, Masoud Koleini, Kristopher K. Micinski, Markus N.
          Rabe, and César Sánchez. Temporal logics for hyperproperties. In Martı́n Abadi and Steve
          Kremer, editors, Principles of Security and Trust - Third International Conference (POST
          2014), volume 8414 of Lecture Notes in Computer Science, pages 265–284. Springer, 2014.
          doi:10.1007/978-3-642-54792-8\_15.
[FRS+ 24] Flavio Ferrarotti, Peter Rivière, Klaus-Dieter Schewe, Neeraj Kumar Singh, and Yamine Aı̈t
          Ameur. A complete fragment of LTL(EB). In Arne Meyer and Magdalena Ortiz, editors, Founda-
          tions of Information and Knowledge Systems (Proc. FoIKS 2024), volume 14589 of LNCS, pages
          237–255. Springer, 2024. an extended version is available at http://arxiv.org/abs/2401.16838,
          version 1. doi:10.1007/978-3-031-56940-1_13.
[FS24]    Flavio Ferrarotti and Klaus-Dieter Schewe. Modal extensions of the logic of abstract state
          machines. In Silvia Bonfanti et al., editors, Rigorous State-Based Methods (ABZ 2024), volume
          14759 of Lecture Notes in Computer Science, pages 123–140. Springer, 2024. doi:10.1007/
          978-3-031-63790-2\_8.
[FSTW18] Flavio Ferrarotti, Klaus-Dieter Schewe, Loredana Tec, and Qing Wang. A unifying logic for
          non-deterministic, parallel and concurrent Abstract State Machines. Ann. Math. Artif. Intell.,
          83(3-4):321–349, 2018. doi:10.1007/s10472-017-9569-3.
[GMOV22] Jens Oliver Gutsfeld, Arne Meier, Christoph Ohrem, and Jonni Virtema. Temporal team semantics
          revisited. In Christel Baier and Dana Fisman, editors, 37th Annual ACM/IEEE Symposium on
          Logic in Computer Science (LICS 2022), pages 44:1–44:13, 2022. doi:10.1145/3531130.3533360.
                                                                                                        51




[HA11]    Thai Son Hoang and Jean-Raymond Abrial. Reasoning about liveness properties in Event-B. In
          Shengchao Qin and Zongyan Qiu, editors, Formal Methods and Software Engineering (ICFEM
          2011), volume 6991 of Lecture Notes in Computer Science, pages 456–471. Springer, 2011. URL:
          https://doi.org/10.1007/978-3-642-24559-6_31.
[KM08]    Fred Kröger and Stephan Merz. Temporal Logic and State Systems. Texts in Theoretical Computer
          Science. An EATCS Series. Springer, 2008. doi:10.1007/978-3-540-68635-4.
[Lam02]   Leslie Lamport. Specifying Systems, The TLA+ Language and Tools for Hardware and Software
          Engineers. Addison-Wesley, 2002. URL: http://research.microsoft.com/users/lamport/tla/
          book.html.
[Lam10]   Leslie Lamport. Temporal logic: The lesser of three evils, 2010. Presentation at the Amir Pnueli
          Memorial Symposium. URL: https://cs.nyu.edu/acsys/pnueli/.
[McL92]   John McLean. Proving noninterference and functional correctness using traces. J. Comput. Secur.,
          1(1):37–58, 1992. doi:10.3233/JCS-1992-1103.
[Mer03]   Stephan Merz. On the logic of TLA+ . Comput. Artif. Intell., 22(3-4):351–379, 2003. URL:
          http://www.cai.sk/ojs/index.php/cai/article/view/460.
[MP84]    Zohar Manna and Amir Pnueli. Adequate proof principles for invariance and liveness properties of
          concurrent programs. Sci. Comput. Program., 4(3):257–289, 1984. doi:10.1016/0167-6423(84)
          90003-0.
[PLB14]   Andrei Popescu, Peter Lammich, and Thomas Bauereiss. Bounded-deducibility security. Archive of
          Formal Proofs, 2014. https://isa-afp.org/entries/Bounded_Deducibility_Security.html,
          Formal proof development.
[PLB21]   Andrei Popescu, Peter Lammich, and Thomas Bauereiss. CoCon: A confidentiality-verified
          conference management system. Arch. Formal Proofs, 2021. https://isa-afp.org/entries/
          CoCon.html, Formal proof development.
[PLH21]   Andrei Popescu, Peter Lammich, and Ping Hou. CoCon: A conference management system
          with formally verified document confidentiality. J. Autom. Reason., 65(2):321–356, 2021. doi:
          10.1007/S10817-020-09566-9.
[Pnu77]   Amir Pnueli. The temporal logic of programs. In 18th Annual Symposium on Foundations of
          Computer Science (FoCS 1977), pages 46–57. IEEE Computer Society, 1977. doi:10.1109/SFCS.
          1977.32.
[RSAD23] Peter Rivière, Neeraj Kumar Singh, Yamine Aı̈t Ameur, and Guillaume Dupont. Formalising
          liveness properties in Event-B with the reflexive EB4EB framework. In Kristin Yvonne Rozier
          and Swarat Chaudhuri, editors, NASA Formal Methods - 15th International Symposium (NFM
          2023), volume 13903 of Lecture Notes in Computer Science, pages 312–331. Springer, 2023.
          doi:10.1007/978-3-031-33170-1\_19.
[Sch12]   Matthias Schmalz. Formalizing the Logic of Event-B. PhD thesis, ETH Zürich, 2012. doi:
          10.3929/ethz-a-007577749.
[SN01]    Robert F. Stärk and Stanislas Nanchen. A logic for abstract state machines. Journal of Universal
          Computer Science, 7(11):980–1005, 2001. doi:10.3217/jucs-007-11-0980.
[Vää24] Jouko Väänänen. Second-order and Higher-order Logic. In Edward N. Zalta and Uri Nodelman,
          editors, The Stanford Encyclopedia of Philosophy. Metaphysics Research Lab, Stanford University,
          Winter 2024 edition, 2024. URL: https://plato.stanford.edu/archives/win2024/entries/
          logic-higher-order/.



                          Appendix A. Variant Existence Proofs
Proof (of Lemma 2.4). In the following, if F is a formula or set of actions and v, w are
variables, we use F (v/w) to denote the formula or set of actions obtained by substituting in
F each occurrence of v by w. Furthermore, we use list and list operators, with [] denoting
the empty list and l1 · l2 denoting concatenation of lists l1 and l2 . Of course, with proper
encoding we could use sets instead of lists, but lists give us a cleaner presentation for this
proof.
    Let M ′ be the Event-B machine built form M as follows:
52




• The initial event init ′ of M ′ is the result of first applying the substitution v̄/w̄ to the
  initial event init of M , and then adding the following actions: s, u := 0, v̄ : | ¬φ(v̄ ′ ) and
  l := [].
• We add to the set of events E ′ of M ′ the following event, which is triggered only once and
  only if the corresponding trace ofWM is of length 1.
  efirstA = any x̄ where u = 0 ∧ ¬ ei ∈E Gi (x̄, v̄/w̄) then {s := 1, u := 2, v̄ := w̄}.
• We add to the set of events E ′ of M ′ the following event, which is triggered only once and
  only if the corresponding trace of                   W M is of length > 1.
  efirstB = any x̄ where u = 0 ∧                          ei ∈E Gi (x̄, v̄/w̄) then {u := 1}.
• For each ei = any x̄ where Gi (x̄, v̄) then Ai (x̄, v̄, v̄ ′ ) end in the set of events E of M , we
  add the following two corresponding events to E ′ (the set of events of M ′ ).
  eia = any x̄ where Gia (x̄, v̄, w̄, l, s, u) then Aia (x̄, v̄, w̄, l, s, u, v̄ ′ , w̄′ , l′ , s′ , u′ )
  eib = any x̄ where Gib (x̄, v̄, w̄, l, s, u) then Aib (x̄, v̄, w̄, l, s, u, v̄ ′ , w̄′ , l′ , s′ , u′ )
  eic = any x̄ where Gic (x̄, v̄, w̄, l, s, u) then Aic (x̄, v̄, w̄, l, s, u, v̄ ′ , w̄′ , l′ , s′ , u′ )
  where
  – Gia (x̄, v̄, w̄, l, s, u) ≡ Gi (x̄, v̄/w̄) ∧ φ(v̄/w̄) ∧ s = 0 ∧ u = 1
     Aia (x̄, v̄, w̄, l, s, u, v̄ ′ , w̄′ , l′ , s′ , u′ ) =
                        Ai (x̄, v̄/w̄, v̄ ′ /w̄′ ) ∪ {l := l · [w̄]}
  – Gib (x̄, v̄, w̄, l, s, u) ≡ Gi (x̄, v̄/w̄) ∧ ¬φ(v̄/w̄) ∧ s = 0 ∧ u = 1 ∧ l ̸= []
     Aib (x̄, v̄, w̄, l, s, u, v̄ ′ , w̄′ , l′ , s′ , u′ ) =
                        Ai (x̄, v̄/w̄, v̄ ′ /w̄′ ) ∪ {s := 1, v̄ := head (l), l := tail (l) · [w̄]}
  – Gic (x̄, v̄, w̄, l, s, u) ≡ Gi (x̄, v̄/w̄) ∧ ¬φ(v̄/w̄) ∧ s = 0 ∧ u = 1 ∧ l = []
     Aic (x̄, v̄, w̄, l, s, u, v̄ ′ , w̄′ , l′ , s′ , u′ ) =
                        Ai (x̄, v̄/w̄, v̄ ′ /w̄′ ) ∪ {s := 1, v̄ := w̄}
• We add the following two additional events er and es to the set E ′ of M ′ :
  – Gr (x̄, v̄, w̄, l, s, u) ≡ l ̸= [] ∧ s = 1 ∧ u = 1
     Ar (x̄, v̄, w̄, l, s, v̄ ′ , w̄′ , l′ , s′ ) = {v̄ := head(l), l := tail(l)}
  – Gs (x̄, v̄, w̄, l, s, u) ≡ l = [] ∧ s = 1 ∧ u = 1
     As (x̄, v̄, w̄, l, s, u, v̄ ′ , w̄′ , l′ , s′ , u′ ) = {s := 0}

      Let t(v̄, w̄, l, s, u) be the term len(l), which gives us the length of the list l. We show
next that properties (i) and (ii) of the lemma hold. Let us start with (i), which can be
proven by showing that if M is convergent in φ, σ is a trace of M ′ and 0 ≤ k ≤ ℓ(σ), then
σ (k) |= var c (M, len(l), φ). Let us assume without loss of generality that σ = S0 , S1 , . . . is
infinite, i.e., ℓ(σ) = ω, and proceed by induction on k. Note that our proof below also holds
when σ is finite.
      Any trace σ of M ′ will have at least 2 states. This follows from the fact that init ′
sets the value of u in S0 to 0, and thus either event efirstA or efirstB will be enabled in S0 .
Therefore, we start the induction with k = 1. By definition of init ′ , we have that S0 ̸|= φ(v̄)
and thus that σ (0) |= var c (M, len(l), φ). If state S1 is the result of triggering efirstA , then by
construction of M ′ from M and the fact that M is convergent in φ, we get that S0 ̸|= φ(v̄/w̄).
We also get by the actions of efirstA that the value of v̄ in S1 is the same as the value of w̄ in
S0 . Then, S1 ̸|= φ(v̄). If state S1 is the result of triggering efirstB instead, then the value
of v̄ is not updated and thus it is the same in both S0 and S1 . This again gives us that
S1 ̸|= φ(v̄). We can then conclude that σ (1) |= var c (M, len(l), φ).
                                                             (k)
      If k+1 > 1, we know by inductive  W hypothesis that σ |= var c (M, len(l), φ). Thus,       either
(a) Sk ̸|= φ(v̄) or (b) Sk |= ∀x̄(¬ ei ∈E Gi (x̄, v̄)) or (c) Sk |= len(l) ̸= 0 ∧ len(l′ ) < len(l),
                                                                                                    53




where l′ is the value of l in state Sk+1 . In order to show that σ (k+1) |= var c (M, len(l), φ),
we consider the four different cases depending on the values of s in Sk and Sk+1 .
• If s = 0 in both Sk and Sk+1 , then an event of the form eia must have been triggered
  in Sk , as otherwise s would be 1 in Sk+1 or Sk would be the initial state and thus
  k + 1 = 1. We know that len(l′ ) > len(l) whenever an event of the form eia is triggered.
  Therefore, option (c) above is W     false and it must be the case by the inductive hypothesis
  that Sk ̸|= φ(v̄) or Sk |= ∀x̄(¬ ei ∈E Gi (x̄, v̄)). Since the actionWof an event eia does not
  update the value of v̄, it follows that Sk+1 ̸|= φ(v̄) or Sk |= ∀x̄(¬ ei ∈E Gi (x̄, v̄)), and thus
  σ (k+1) |= var c (M, len(l), φ).
• If s = 1 in Sk and s = 0 in Sk+1 , then event es was triggered in Sk , as otherwise s would be
  1 in Sk+1 . We know that len(l′ ) = len(l) since es does not update the value of l. Therefore,
  option (c) aboveWis false and it must be the case by the inductive hypothesis that Sk ̸|= φ(v̄)
  or Sk |= ∀x̄(¬ ei ∈E Gi (x̄, v̄)). Since es neither updates the value of v̄, it follows that
  Sk+1 ̸|= φ(v̄) or Sk |= ∀x̄(¬ ei ∈E Gi (x̄, v̄)), and thus σ (k+1) |= var c (M, len(l), φ).
                                  W
• If s = 0 in Sk and s = 1 in Sk+1 , then event elast or an event of the form eib or eic was
  triggered in Sk (notice that efirstA can only be triggered in state S0 ). Otherwise s would
  be 0 in Sk+1 .                                                           W
     We know that if event elast was triggered in Sk , then Sk |= ∀x̄(¬( ei ∈E G   Wi (x̄, v̄/w̄))) and
  that the value of v̄ in Sk+1 equals the value of w̄ in Sk . Thus, Sk+1 |= ∀x(¬( ei ∈E Gi (x̄, v̄))).
  Therefore, σ (k+1) |= var c (M, len(l), φ).
     If instead an event of the form eib was triggered in Sk , then l ̸= [] in Sk+1 . Then, the
  only event that can be triggered in Sk+1 is er and thus len(l′ ) < len(l). Consequently,
  σ (k+1) |= var c (M, len(l), φ).
     Finally, if an event of the form eic was triggered in Sk , then we know that Sk ̸|= φ(v̄/w̄)
  and that the value of v̄ in Sk+1 is equal to the value w̄ in Sk . Therefore, Sk+1 ̸|= φ(v̄),
  which implies that σ (k+1) |= var c (M, len(l), φ).
• If s = 1 in both Sk and Sk+1 , then event er was triggered in Sk , as otherwise s would be
  0 in Sk+1 . If tail (l) ̸= [] in Sk , then only event er can be triggered in Sk+1 . Triggering
  event er always results in len(l′ ) < len(l). Consequently, σ (k+1) |= var c (M, len(l), φ).
     On the other hand, if tail (l) = [] in Sk , then the value of v̄ in Sk+1 equals the value of
  head (l) in Sk . This value corresponds to the value w in the latest preceding state Si in the
  computation σ where an event of the form eib was triggered, meaning that Si ̸|= φ(v̄/w̄).
  Thus, Sk+1 ̸|= φ(v̄) and consequently σ (k+1) |= var c (M, len(l), φ).
    Next we show that property (ii) also holds, i.e. σ is a trace of M iff σ = σ ′ |s=1,v̄ for
some trace σ ′ of M ′ . We use the fact that M is convergent in φ to divide every trace σ of M
into contiguous segments s0 , s1 , . . ., where for each segment sj = Sj0 . . . Sjkj the following
holds:
• The first state in the segment sj+1 (if it exists) is the immediate successor in σ of the last
  state Sjkj in segment sj .
• Sjkj ̸|= φ(v̄).
• Sjm |= φ(v̄) for all 0 ≤ m < kj .
    It follows that for every segment sj of a trace σ of M there is a corresponding segment
sj of a computation σ ′ of M ′ such that sj = s′j |s=1,v̄ , and vice versa. Next we prove the first
 ′

direction of this fact by induction on j.
54




      For j = 0, let the initial segment s0 = S00 . . . S0k0 . By construction of init ′ , we get that
in the initial state S00′ of M ′ the value of w̄ coincides with that of v̄ in S . If k = 0, then
                                                                                          00       0
depending on whether ℓ(σ) = 1 or ℓ(σ) > 1, either event efirstA or efirstB can be triggered in
  ′ . In the former case, s = 1 in the next state S ′ in the trace of M ′ and the value of v̄
S00                                                       01
coincides with its value in S0 . A last step in the trace of M ′ triggers es , which leads to a
further state S02 ′ where s = 0. Thus, s = s′ |                   ′        ′     ′     ′
                                               0    0 s=1,v̄ for s0 = S00 S01 S02 . In the latter case,
                                     ′
the value of w̄ and s in state S01 coincide with the respective values in S00              ′ and an event of

the form eic will be triggered (notice that l = [] and an event ei was triggered by M in state
S00 as ℓ(σ) > 1). Thus, in the next state S02     ′ in the trace of M ′ we get that s = 1 and the

value of v̄ coincides with its value in S00 . An additional step of M ′ is triggered in state S02          ′
                                        ′                                ′                  ′
by the event es leading to state S03 where s = 0. Thus s0 = s0 |s=1,v̄ for s0 = S00 S01 S02 S03 .′   ′ ′   ′

      On the other hand, if in the initial segment s0 of σ we have that k0 > 0, then we know
by construction of M ′ that in its initial state S00    ′ event e
                                                                    firstB will be triggered, and that
                         ′
there is a trace of M in which it holds that the value of w̄ in S0m          ′      for each 1 ≤ m ≤ k0 + 1
coincides with the value of v̄ in S0m−1 . Moreover, we know that an event of the form eia is
then triggered in each of these states except for the last one S0k0 +1 . Consequently, in state
  ′
S0k      the list l is of length k0 and the element in the m-th position of l corresponds to
    0 +1
the value taken by v̄ in state S0m−1 . Furthermore, the state S0k          ′          in this traceof M ′ will
                                                                               0 +1
necessarily trigger an event of the form eib , resulting in a state S0k        ′         where s = 1 and the
                                                                                   0 +2
value of v̄ corresponds to its value in S00 . Clearly, the values that v̄ will take in the next
k0 states following S0k   ′      in this trace of M ′ will correspond to its values in S01 , . . . S0k0 ,
                            0 +2
respectively. In the last of these states, M ′ will trigger event es leading to a further state
where s takes again he value 0. Thus s0 = s′0 |s=1,v̄ , where s′0 is the trace of M ′ of length
2k0 + 3 described above.
      For the inductive step we assume that j + 1 > 0. The inductive hypothesis gives us
that for the segments sj and s′j of M and M ′ , respectively, it holds that sj = s′j |s=1,v̄ . It is
easy to see that the values of w̄ in the last state of Sjk   ′        ′
                                                               ′ of sj coincide with the value of v̄ in
                                                                 j
                                                        ′ , we can use a similar argument as
the last state Sjkj of sj . Since furthermore s = 0 in Sjk ′
                                                                     j
before to show that sj+1 = s′j+1 |s=1,v̄ . We omit the tedious but simple technical details.
    Likewise, we can prove (by induction on j) that for every segment s′j of a trace σ ′ of M ′
there is a corresponding segment sj of a trace σ of M such that sj = s′j |s=1,v̄ . Again, we
omit the tedious, but simple technical details.

Proof (of Lemma 2.6). We slightly modify the construction of M ′ from the proof of Lemma
2.4. As long as s = 0 holds, we also count the number of steps using the state variable c
for the step counter. Then let k be the constant in the definition of conv1 (φ). When the
value of c exceeds k, M ′ sets s to 1 and resets c to 0. This guarantees that traces of M with
infinitely many states satisfying φ are properly simulated by M ′ .
     Then the proof of (ii) remains the same. For the proof of (i) we need to consider only
the one trace defining the local convergence property. For this trace we obtain a sequence
of events. As there is no infinite sequence of states all satisfying φ the value of the variant
term strictly decreases until a state satisfying ¬φ is reached. As the variant term is defined
by the length of this sequence we get the validity of var 1c (M, t, φ).

Proof (of Lemma 2.8). As M |= div(φ) holds, in any trace σ there can only be finitely many
states satisfying ¬φ. Consequently, for each state variable vi there are only finitely many
                                                                                                                                  55




values that vi can take in any state satisfying ¬φ of any trace. Let Mi ∈ HF(A) be the set
of all these values.
       We define the machine M ′ with additional state variables c̄ = (c0 , . . . , cm ) and b̄ =
(b0 , . . . , bm ). The initialisation event of M ′ simply extends the event init of M by the
assigments ci := ∅ and bi := Mi . Then the projection of the initial state S0 of M ′ to the
state variables v̄ is the initial state of M .
       For each event e of M with guard Ge (x̄, v̄) and action Ae (x̄, v̄, v̄ ′ ) we define two events
e+ and e− of M ′ . The guard of e+ is Ge+ (x̄, v̄, c̄, b̄) = Ge (x̄, v̄) ∧ φ(v̄), and the action
Ae+ (x̄, v̄, c̄, b̄, v̄ ′ , c̄′ , b̄′ ) is the same as Ae (x̄, v̄, v̄ ′ ). The guard of e− is Ge− (x̄, v̄, c̄, b̄) =
Ge (x̄, v̄) ∧ ¬φ(v̄), and the action Ae− (x̄, v̄, c̄, b̄, v̄ ′ , c̄′ , b̄′ ) results from adding the assignments
ci := ci ∪ {vi′ } for all i = 1, . . . , m to the action Ae (x̄, v̄, v̄ ′ ).
       Regardless if M ′ is in a state satisfying φ or in a state satisfying ¬φ, the projection of
the action of either e+ or e− to the state variables v̄ yields the action of e. It follows that
property (ii) of the lemma holds.
       For property (i) we define the variant term t(v̄, c̄, b̄) = (b0 − c0 , . . . , bm − cm ). The values
of the state variables b̄ are never updated, and the values of c̄ are only updated by events
e− , i.e. only in states satisfying ¬φ. This implies that
                φ(v̄) ∧ Ge (x̄, v̄, c̄, b̄) ∧ PAe (x̄, v̄, c̄, b̄, v̄ ′ , c̄′ , b̄′ ) → t(v̄ ′ , c̄′ , b̄′ ) = t(v̄, c̄, b̄)   (A.1)
holds for all events e of M ′ and all x̄, v̄, c̄, b̄, v̄ ′ , c̄′ , b̄′ .
    As every event e− inserts additional values into the sets ci , the sequence of values for
the tuple (c0 , . . . , cm ) is strictly increasing in states satisfying ¬φ. We cannot have equality,
because otherwise we would have a state Si satisfying ¬φ with a possible successor state
Si+1 = Si resulting from firing some event e− . Then this event could be fired again and again,
thus leading to a trace with an infinite subsequence of states satisfying ¬φ contradicting
M |= div(φ). Then the sequence of tuples (b0 − c0 , . . . , bm − cm ) is strictly decreasing in
states satisfying ¬φ, i.e.
               ¬φ(v̄) ∧ Ge (x̄, v̄, c̄, b̄) ∧ PAe (x̄, v̄, c̄, b̄, v̄ ′ , c̄′ , b̄′ ) → t(v̄ ′ , c̄′ , b̄′ ) < t(v̄, c̄, b̄)   (A.2)
holds for all events e of M ′ and all x̄, v̄, c̄, b̄, v̄ ′ , c̄′ , b̄′ .
    Furthermore, the choice of the constants Mi stored in the state variable bi ensures that
always ci ⊊ bi holds, which implies
                     ¬φ(v̄) ∧ Ge (x̄, v̄, c̄, b̄) ∧ PAe (x̄, v̄, c̄, b̄, v̄ ′ , c̄′ , b̄′ ) → t(v̄, c̄, b̄) ̸= ∅               (A.3)
for all events e of M ′ and all x̄, v̄, c̄, b̄, v̄ ′ , c̄′ , b̄′ .
     Finally, (A.2), (A.3) and (A.1) together are equivalent to claim (i), which concludes the
proof.
Proof (of Lemma 2.10). The refined machine M ′ is constructed in the same way as in the
proof of Lemma 2.8 with the only difference that the set values bi are taken from the one
trace with a tail of states satisfying φ. The ld-variant term t is also defined in the same way.
Then we get that conditions (A.2), (A.3) and (A.1) hold for the states in one trace, hence
var 1d (M ′ , t, φ) is valid for M ′ .
Proof (of Lemma 2.17). For e-variants the construction of M ′ for is analogous to the con-
struction in the proof of Lemma 2.4 with the difference that an additional Boolean-valued
state variable b is used, and there is only once a switch from s = 0 to s = 1, and in this
transition also b is set to 1. When the list ℓ has been emptied, s is set to 2 and M ′ continues
in the same way as M ignoring the additional state variables. Then the sought e-variant
56




term is (t1 , b), where t1 is the length of ℓ. The detailed arguments are then exactly the same
as in the proof of Lemma 2.4.
     For e1-variants the construction of M ′ for is analogous to the construction in the proof
of Lemma 2.6 with the same modifications as in the proof of Lemma 2.17 exploiting the
constant k that is guaranteed by M |= ♢1 φ. M ′ uses an additional Boolean-valued state
variable b, and there is only once a switch from s = 0 to s = 1, and in this transition also b
is set to 1. When the list ℓ has been emptied, s is set to 2 and M ′ continues in the same
way as M ignoring the additional state variables. Then the sought e1-variant term is (t1 , b),
where t1 is the length of ℓ. The detailed arguments are then exactly the same as in the proof
of Lemma 2.6.
Proof (of Lemma 2.20). We construct M ′ in the same way as in the proof on Lemma 2.8
with the only difference that the values b0 , . . . , bm are the maximum set values in traces
satisfying the selection condition ⟨ψ⟩. For these traces S0 , S1 , . . . there exists a k such that
Sℓ |= ψ holds for all ℓ ≥ k, i.e. there are only finitely many states Si satisfying ¬ψ and
hence the maximum values b0 , . . . , bm exist.
     Then with the simultaneous cd-variant term t(v̄, c̄, b̄) = (b0 − c0 , . . . , bm − cm ) we can
use the same arguments as in the proof of Lemma 2.8 to show the required conditions (i)
and (ii).
Proof (of Lemma 2.22). The construction of M ′ is basically the same as in the proof of
Lemma 2.4 with the following modifications:
• We add a Boolean-valued state variable b. In the case that θ is φ ∧ ¬ψ → χ we initialise b
  as 0, if θ holds in the initial state of M , otherwise as 1. In the other two cases for θ we
  initialise b as 1 iff M satisfies conv(¬ψ).
• As long as M ′ is in a state satisfying b = 0 ∧ θ, M ′ executes the events of M directly. A
  switch from b = 0 to b = 1 is added to every event of M ′ , if the invariant θ is violated.
• With a switch to b = 1 M ′ operates in exactly the same way as constructed in the proof
  of Lemma 2.4.
     Then the claims (i) and (ii) follow using the same arguments as in the proof of Lemma
2.4.

                      Appendix B. Nested Temporal Operators
In Section 2 we dealt with sound derivation rules for TREBL formulae of the form Xφ,
Y φ, XY φ, Y Xφ and X(ψ → Y φ) with X ∈ {□, □1 }, Y ∈ {♢, ♢1 }, and φ, ψ ∈ L, but the
definition of TREBL also allows formulae with φ ∈ LT , which we will address now in this
appendix.
    For arbitrary φ ∈ LT —in fact, we could even consider φ ∈ Lext —the equivalences
□□φ ↔ □φ, □1 □φ ↔ □φ, □□1 φ ↔ □φ and □1 □1 φ ↔ □1 φ are easily proven, which
implies (for Xi ∈ {□, □1 } for 1 ≤ i ≤ m)
                                 (
                                  □φ if Xi = □ holds for at least one i
                 X1 . . . Xm φ ↔                                        .
                                  □1 φ if Xi = □1 holds for all i
     By duality we further get (for Yi ∈ {♢, ♢1 } for 1 ≤ i ≤ m)
                                 (
                                  ♢φ if Yi = ♢ holds for all i
                 Y1 . . . Ym φ ↔                                           .
                                  ♢1 φ if Yi = ♢1 holds for at least one i
                                                                                                57




     For alternating sequences of temporal operators the following equivalences are likewise
easily proven:
       □♢□φ ↔ ♢□φ            □♢□1 φ ↔ ♢□1 φ          ♢□♢φ ↔ □♢φ              ♢□♢1 φ ↔ □♢1 φ
    ♢1 □1 ♢1 φ ↔ □1 ♢1 φ ♢1 □1 ♢φ ↔ □1 ♢φ         □1 ♢1 □1 φ ↔ ♢1 □1 φ     □1 ♢1 □φ ↔ ♢1 □φ
     □♢1 □1 φ ↔ ♢□1 φ        □♢1 □φ ↔ ♢□φ          ♢□1 ♢1 φ ↔ □♢1 φ          ♢□1 ♢φ ↔ □♢φ
      ♢1 □♢φ ↔ □1 ♢φ       ♢1 □♢1 φ ↔ □1 ♢1 φ       □1 ♢□φ ↔ ♢1 □φ         □1 ♢□1 φ ↔ ♢1 □1 φ
     We can consider all these eqivalences above as a confluent set of term rewriting rules
(with the longer sequence of temporal operators on the left). Then any TREBL formula
of the form X1 . . . Xm φ with Xi ∈ {□, □1 , ♢, ♢1 } has a unique normal form N (X1 . . . Xm )φ,
where N (X1 . . . Xm ) is a sequence of at most two temporal operators. As we are dealing
with equivalences, we get a sound derivation rule

                                         M ⊢ N (X1 . . . Xm ) φ
                                   N:
                                          M ⊢ X1 . . . Xm φ
     It remains to investigate TREBL formulae, in which at least once a constructor for a
progress formula is used. First consider formulae of the form X1 . . . Xn (φ → Y1 . . . Ym ψ)
with Xn ∈ {□, □1 } and Y1 ∈ {♢, ♢1 }. The equivalences above imply directly that for
Xi , Yj ∈ {□, □1 , ♢, ♢1 }, φ ∈ L and ψ ∈ LT the following derivation rule is sound:

                                M ⊢ N (X1 . . . Xn )(φ → N (Y1 . . . Ym )ψ)
                       NPR:
                                   M ⊢ X1 . . . Xn (φ → Y1 . . . Ym ψ)


B.1. Prefixed Variants. With the results above we look at TREBL formulae of the form
□(φ → XY ψ) and □(φ → Y Xψ) with X ∈ {□, □1 }, Y ∈ {♢, ♢1 } and φ, ψ ∈ L. In all
cases, if τ = S0 , S1 , . . . is a trace of M let k be minimal with Sk |= φ—if no such k exists,
let k = ω.
     Clearly, for k = ω we have Si |= φ → XY ψ for all i, and for k < ω we have Si |= φ →
XY ψ for i ≥ k iff Si |= XY ψ. That is, every trace has a prefix, in which the required
condition trivially holds, while for the remainder of the trace it suffices to show that XY ψ
holds.
     Therefore, with a Boolean-valued state variable b we can exploit the prefix formula
pre(¬φ, b) defined in (2.13), and define prefixed variant formulae by modification of c-variants
and lc-variants as defined in (2.1) and (2.2):
                   pvarc (φ, (t, b), ¬ψ) ≡ pre(¬φ, b) ∧ varc (t, ψ ∧ b = 1) and
                     pvar1c (φ, (t, b), ¬ψ) ≡ pre(¬φ, b) ∧ var1c (t, ψ ∧ b = 1)             (B.1)
    For TREBL formulae of the form □(φ → XY ψ) we obtain sound derivation rules by
simple modifications of the rules E, E11 , E10 and E01 :

                  M ⊢ pvarc (φ, (t, b), ¬ψ) M ⊢ (φ ↔ b = 1) M ⊢ □ dlf(¬ψ ∧ b = 1)
       PRE:
                                           M ⊢ □(φ → □♢ ψ)
                                M ⊢ pvar1c (φ, (t, b), ¬ψ) M ⊢ (φ ↔ b = 1)
                   PRE11 :
                                           M ⊢ □(φ → □1 ♢1 ψ)
58




                   M ⊢ pvar1c (φ, (t, b), ¬ψ) M ⊢ (φ ↔ b = 1) M ⊢ □ dlf(¬ψ ∧ b = 1)
      PRE01 :
                                             M ⊢ □(φ → □♢1 ψ)
                    M ⊢ pvar1c (φ, (t, b), ¬ψ) M ⊢ (φ ↔ b = 1) M ⊢ □(b = 1 → ♢ψ)
       PRE10 :
                                             M ⊢ □(φ → □1 ♢ ψ)

     The soundness proofs are the same as in Lemmata 2.3 and 2.5, and the existence of the
variant terms follows as in Lemmata 2.4 and 2.6 with the small add-on of a prefix of states
all satisfying ¬φ.
     Analogously, for TREBL formulae of the form □(φ → Y Xψ) we obtain prefixed variant
formulae by modification of d-, ld-, pld- and pd-variants as defined in (2.3), (2.4), (2.5) and
(2.6):

                     pvard (φ, (t, b), ψ) ≡ pre(¬φ, b) ∧ vard (t, ψ ∧ b = 1) ,
                     pvar1d (φ, (t, b), ψ) ≡ pre(¬φ, b) ∧ var1d (t, ψ ∧ b = 1) ,
                  pvarp1                                 p1
                      d (φ, (t, b), ψ) ≡ pre(¬φ, b) ∧ vard (t, ψ ∧ b = 1) and
                     pvarpd (φ, (t, b), ψ) ≡ pre(¬φ, b) ∧ varpd (t, ψ ∧ b = 1)           (B.2)

    We then obtain the following sound derivation rules by simple modifications of the rules
P, P11 , P01 and P10 :

                  M ⊢ pvard (φ, (t, b), ψ) M ⊢ (φ ↔ b = 1) M ⊢ □ dlf(b = 1 ∧ ¬ψ)
       PRP:
                                           M ⊢ □(φ → ♢□ ψ)
                                 M ⊢ pvar1d (φ, (t, b), ψ) M ⊢ (φ ↔ b = 1)
                         11
                   PRP :
                                             M ⊢ □(φ → ♢1 □1 ψ)
                                 M ⊢ pvarp1
                                         d (φ, (t, b), ψ) M ⊢ (φ ↔ b = 1)
                        01
                   PRP :
                                           M ⊢ □(φ → ♢□1 ψ)
                                 M ⊢ pvarpd (φ, (t, b), ψ) M ⊢ (φ ↔ b = 1)
                   PRP10 :
                                              M ⊢ □(φ → ♢1 □ ψ)

     The soundness proofs are the same as in Lemmata 2.7, 2.9, 2.11 and 2.12, and the
existence of the variant terms follows as in Lemmata 2.8, 2.10 and 2.14 with the small add-on
of a prefix of states all satisfying ¬φ.



B.2. Prefixes in a Single Trace. For formulae of the form □1 (φ → XY ψ) we proceed
analogously. The only difference is that need to consider only a prefix with states satisfying
¬φ of one trace, which is captured by a sentence pre1 (φ, b) defined as
                               _
                                    ∃x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧ b′ = b
                                                                                      
                  ∀v̄ φ(v̄) →
                                 ei ∈E
                            ^                                                   
                  ∧ ¬φ(v̄) →   ∀x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) → b′ = 1
                                ei ∈E
                                                                                             59




     Then we get locally prefixed variant formulae again by modification of c-variants and
lc-variants as defined in (2.1) and (2.2):
                 lpvarc (φ, (t, b), ¬ψ) ≡ pre1 (¬φ, b) ∧ varc (t, ψ ∧ b = 1) and
                   lpvar1c (φ, (t, b), ¬ψ) ≡ pre1 (¬φ, b) ∧ var1c (t, ψ ∧ b = 1)         (B.3)
    Thise gives rise to the following two sound derivation rules:

                   M ⊢ lpvarc (φ, (t, b), ¬ψ) M ⊢ (φ ↔ b = 1) M ⊢ □ dlf(¬ψ ∧ b = 1)
     PR1 E00 :
                                             M ⊢ □1 (φ → □♢ ψ)
                  M ⊢ lpvar1c (φ, (t, b), ¬ψ) M ⊢ (φ ↔ b = 1) M ⊢ □ dlf(¬ψ ∧ b = 1)
     PR1 E01 :
                                            M ⊢ □1 (φ → □♢1 ψ)
     Again, the soundness proofs are the same as in Lemmata 2.3 and 2.5, and the existence
of the variant terms follows as in Lemmata 2.4 and 2.6 with the small add-on of a prefix of
states all satisfying ¬φ.
     The remaining two cases are simpler. If there exists a trace S0 , S1 , . . . with Si |= ¬φ
for all i, then the progress formula □1 (φ → XY ψ) is trivially satisfied for all X ∈ {□, □1 }
and Y ∈ {♢, ♢1 }. If all traces contain a state Si with Si |= φ, then the condition φ can be
ignored. Therefore, the following derivation rules are sound:

                                                M ⊢ □1 ¬φ
                               PR1 E:
                                            M ⊢ □1 (φ → XY ψ)
                                            M ⊢ ♢φ M ⊢ □1 ♢ ψ
                             PR1 E10 :
                                            M ⊢ □1 (φ → □1 ♢ ψ)
                                            M ⊢ ♢φ M ⊢ □1 ♢1 ψ
                             PR1 E11 :
                                            M ⊢ □1 (φ → □1 ♢1 ψ)
    For formulae of the form □1 (φ → Y Xψ) we obtain sound derivation rules in the same
way. If there exists a trace S0 , S1 , . . . with Si |= ¬φ for all i, then the progress formula
□1 (φ → Y Xψ) is trivially satisfied for all X ∈ {□, □1 } and Y ∈ {♢, ♢1 }. If all traces
contain a state Si with Si |= φ, then for Y = ♢1 the condition φ can be ignored. Therefore,
the following derivation rules are sound:

                                                M ⊢ □1 ¬φ
                               PR1 P:
                                            M ⊢ □1 (φ → Y X ψ)
                                            M ⊢ ♢φ M ⊢ ♢1 □ ψ
                             PR1 P10 :
                                            M ⊢ □1 (φ → ♢1 □ ψ)
                                            M ⊢ ♢φ M ⊢ ♢1 □1 ψ
                             PR1 P11 :
                                            M ⊢ □1 (φ → ♢1 □1 ψ)
   This leaves the cases with Y = ♢. We get locally prefixed variant formulae again by
modification of d-variants and pld-variants as defined in (2.3) and (2.5):
                 lpvard (φ, (t, b), ¬ψ) ≡ pre1 (¬φ, b) ∧ vard (t, ψ ∧ b = 1) and
                   lpvarp1                     1             p1
                        d (φ, (t, b), ¬ψ) ≡ pre (¬φ, b) ∧ vard (t, ψ ∧ b = 1)            (B.4)
    Thise gives rise to the following two sound derivation rules:
60




                    M ⊢ lpvard (φ, (t, b), ¬ψ) M ⊢ (φ ↔ b = 1) M ⊢ □ dlf(¬ψ ∧ b = 1)
     PR1 P00 :
                                              M ⊢ □1 (φ → ♢□ ψ)
                                   M ⊢ lpvarp1
                                            d (φ, (t, b), ¬ψ) M ⊢ (φ ↔ b = 1)
                   PR1 P01 :
                                                M ⊢ □1 (φ → ♢□1 ψ)
     Again, the soundness proofs are the same as in Lemmata 2.7 and 2.9, and the existence
of the variant terms follows as in Lemmata 2.8 and 2.14 with the small add-on of a prefix of
states all satisfying ¬φ.

B.3. Prefixes for Simultaneous and Conditional Variants. The rules above are for the
derivation of TREL formulae, where we use invariance, existence, persistence and reachability
constructors inside a progress rule constructor. We now investigate rules for formulae, where
a progress rule constructor is used inside invariance, existence, persistence and reachability
constructors. Due to rule NPR we have to consider formulae of the form ♢X(φ → Y ψ) or
♢1 X(φ → Y ψ) with X ∈ {□, □1 } and Y ∈ {♢, ♢1 }.
    In the former case for all traces S0 , S1 , . . . there exists some k such that Sk |= X(φ →
Y ψ). In the latter case there needs to exist just one such trace. For X(φ → Y ψ) we have
discovered the sound derivation rules PR, PR11       j , PR
                                                                  01 and PR10 (1 ≤ j ≤ 3). In addition we
                                                                           j
need to consider a prefix, i.e. S0 , . . . , Sk−1 , and this prefix may contain only finitely many
states Si with Si |= φ.
    That is, the prefix—in the obvious sense—behaves like a trace satisfying div(¬φ). We
therefore consider a term t taking values in some well-founded set V and a Boolean-valued
state variable b and define the sentence pre(φ, (t, b)) as
                     ^                                                              
                 ∀v̄     ∀x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) → b = 1 → b′ = 1 ∧
                      ei ∈E
           φ(v̄) ∧ b = 0 → t(v̄) ̸= 0 ∧ t(v̄ ′ ) < t(v̄) ∧ ¬φ(v̄) ∧ b = 0 → t(v̄ ′ ) ≤ t(v̄)
                                                                                            

    With this prefix formula we can then define prefixed simultaneous variant formulae
psvarcd (φ, (t′ , b), t, (ψ, χ)) and (with θ as in (2.10), (2.11) and (2.12)) prefixed conditional
variant formulae pcvarc (φ, (t′ , b), t, ψ, θ) as follows:
             psvarcd (φ, (t′ , b), t, (ψ, χ)) ≡ pre(φ, (t′ , b)) ∧ svarcd (t, (ψ ∧ b = 1, χ))      (B.5)
                               ′                         ′
                 pcvarc (φ, (t , b), t, ψ, θ) ≡ pre(φ, (t , b)) ∧ cvarc (t, ψ ∧ b = 1, θ)          (B.6)
    Now we only need to replace the simultaneous and conditional variant formulae in the
antecedents of the rules PR, PR11      j , PR
                                              01 and PR10 (1 ≤ j ≤ 3) by their prefixed versions
                                                         j
(B.5) and (B.6), respectively, which gives us derivation rules PPR, PPR11           j , PPR
                                                                                             01 and

PPRj (1 ≤ j ≤ 3) for the derivation of TREBL formulae ♢□(φ → ♢ψ), ♢□ (φ → ♢1 ψ),
     10                                                                                1

♢□(φ → ♢1 ψ) and ♢□1 (φ → ♢ψ), respectively.
    Using the same arguments as in the proofs of Lemmata 2.18, 2.23, 2.24, 2.25 in
combination with the proofs of Lemmata 2.19 and 2.21 we can show the soundness of
these derivation rules. We only need to take into account that the involved prefix formula
pre(φ, (t′ , b)) defines a prefix of traces with states satisfying b = 0, which contain only finitely
many states satisfying φ and do not terminate in a state satisfying φ. Using the same
arguments as in the proofs of Lemmata 2.20 and 2.22 we can show that prefixed simultaneous
and prefixed conditional variants exist in sufficiently refined machines. The only necessary
modification is to add a machine for the prefix. We omit the tedious technical details.
                                                                                                                61




     For TREBL formulae of the form ♢1 X(φ → Y ψ) we proceed analogously. Again we
need a prefix with only finitely many states satisfying φ, but such a prefix is only required
for one trace and not necessarily for all traces. For this we consider a term t taking values in
some well-founded set V and a Boolean-valued state variable b and define the prefix formula
pre1 (φ, (t, b)) as
                                       _                                                                
      ∀v̄ φ(v̄) ∧ b = 0 → t(v̄) ̸= 0 ∧       ∃x̄v̄ ′ Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) ∧ t(v̄ ′ ) < t(v̄)
                                                 ei ∈E
                ^                                                                                      
            ∧           ∀x̄v̄ ′ ¬φ(v̄) ∧ b = 0 → Gi (x̄, v̄) ∧ PAi (x̄, v̄, v̄ ′ ) → t(v̄ ′ ) ≤ t(v̄)
                ei ∈E
                                                                      
                                                               ′
                                                         
                                               ∧ b=1→b =1

    With this prefix formula we can define again prefixed simultaneous variant formulae
psvar1cd (φ, (t′ , b), t, (ψ, χ)) and (with θ as in (2.10), (2.11) and (2.12)) prefixed conditional
variant formulae pcvar1c (φ, (t′ , b), t, ψ, θ) as follows:
             psvar1cd (φ, (t′ , b), t, (ψ, χ)) ≡ pre1 (φ, (t′ , b)) ∧ svarcd (t, (ψ ∧ b = 1, χ))             (B.7)
                  pcvar1c (φ, (t′ , b), t, ψ, θ) ≡ pre1 (φ, (t′ , b)) ∧ cvarc (t, ψ ∧ b = 1, θ)              (B.8)
     Replacing the simultaneous and conditional variant formulae in the antecedents of the
rules PR, PR11 j , PR
                      01 and PR10 (1 ≤ j ≤ 3) by their prefixed versions (B.7) and (B.8),
                                 j
respectively, which gives us derivation rules P1 PR, P1 PR11   1
                                                          j , P PR
                                                                   01 and P1 PR10 (1 ≤ j ≤ 3)
                                                                               j
for the derivation of TREBL formulae ♢1 □(φ → ♢ψ), ♢1 □1 (φ → ♢1 ψ), ♢1 □(φ → ♢1 ψ) and
♢1 □1 (φ → ♢ψ), respectively.
     The soundness of these rules follows in the same way as in the proofs of Lemmata 2.18,
2.23, 2.24, 2.25 in combination with the proofs of Lemmata 2.19 and 2.21.
Remark B.1. Note that the rules for nested temporal TREBL formulae that we discovered
so far involve prefixed variant formulae, which are conjunctions of variant formulae and
prefix formulae. Thus, the antecedents of the rules can be split, and rules could be optimised
so that prefix formulae just need to be added as additional antecedents. We do not consider
such optimisation of the derivation rules in this article.



B.4. Nested Progress Operators. The only remaining cases concern nested formulae, in
which at least two progress operators are involved. It suffices to consider formulae of the
form □(φ → Y X(χ → Y ′ ψ)) or □1 (φ → Y X(χ → Y ′ ψ)).
    The former case is analogous to case handled above, where a variant of a persistence
formula is nested inside a progress formula with the difference that χ → Y ′ ψ is not a
formula in L. Nonetheless, the argument that traces require a prefix of states satisfying ¬φ
such that the remainder of the trace satisfies Y X(χ → Y ′ ψ) emains the same. If we use a
Boolean-valued state variable b to capture such a prefix, it follows that

                          M ⊢ pre(¬φ, b) M ⊢ Y X((χ ∧ b = 1) → Y ′ ψ) M ⊢ (φ ↔ b = 1)
        PRPR:
                                          M ⊢ □(φ → Y X(χ → Y ′ ψ))
62




is a sound derivation rule for TREBL formulae of the form □(φ → Y X(χ → Y ′ ψ)) with
X ∈ {□, □1 } and Y, Y ′ ∈ {♢, ♢1 }. While φ, χ ∈ L, we may have ψ ∈ LT , so multiple nesting
of progress operators is supported.
     The case of nested TREBL formulae of the form □1 (φ → Y X(χ → Y ′ ψ)) can be handled
in the same way using a prefix for a single trace rather than all traces. That is, we obtain
the following sound derivation rule:

                    M ⊢ pre1 (¬φ, b) M ⊢ Y X((χ ∧ b = 1) → Y ′ ψ) M ⊢ (φ ↔ b = 1)
      PR1 PR:
                                     M ⊢ □1 (φ → Y X(χ → Y ′ ψ))
    Concerning the proof of Theorem 3.2 we left out the cases of TREBL formulae that
result from multiple application of the constructors in Definition 1.2. These are handled
here.
Proof (extension of the proof of Theorem 3.2). If only the constructors for invariance, reach-
ability, existence and persistence formulae are applied, we get a formula φ = X1 . . . Xm ψ
with Xi ∈ {□, □1 , ♢, ♢1 } and ψ ∈ L. We know that this formula is equivalent to φ′ =
N (X1 . . . Xm )ψ. Therefore, if M |= φ holds, then also M |= φ′ holds. By the induction
hypothesis we get M ⊢R φ′ , and then the application of rule N gives us M ⊢R φ.
     Analogously, a TREBL formula φ = X1 . . . Xn (χY1 . . . Ym ψ) with Xi , Yj ∈ {□, □1 , ♢, ♢1 }
and ψ, χ ∈ L—such a formula arises from the application of the constructors for invariance,
reachability, existence and persistence plus a single progress operator—is equivalent to a
formula φ′ = N (X1 . . . Xn )(χN (Y1 . . . Ym )ψ). Hence, if M |= φ holds, then also M |= φ′
holds. By the induction hypothesis we get M ⊢R φ′ , and then the application of rule NPR
gives us M ⊢R φ.
     For TREBL formulae of the form φ = □(φ1 → XY φ2 ) with X ∈ {□, □1 }, Y ∈ {♢, ♢1 }
and φ1 , φ2 ∈ L there exist appropriate prefixed variant terms such that M satisfies the
antecedents of the rules PRE, PRE11 , PRE01 or PRE10 , respectively, By the induction
hypothesis, these antecedents are derivable by rules in R, and then the application of the
corresponding rule yields M ⊢R φ.
     The same arguments apply for TREBL formulae of the form φ = □(φ1 → Y Xφ2 )
with the difference that we use the rules PRP, PRP11 , PRP01 or PRP10 , respectively.
Analogously, for TREBL formulae of the form φ = □1 (φ1 → XY φ2 ) we use the rules
PR1 E, PR1 E00 , PR1 E11 , PR1 E01 or PR1 E10 , respectively, and for TREBL formulae of the
form φ = □1 (φ1 → Y Xφ2 ) we use the rules PR1 P, PR1 P00 , PR1 P11 , PR1 P01 or PR1 P10 ,
respectively.
     For TREBL formulae of the form φ = ♢1 X(χ → Y ψ) with X ∈ {□, □1 }, Y ∈ {♢, ♢1 }
and ψ, χ ∈ L there exist appropriate prefixed simultaneous and conditional variants such
that M satisfies the antecedents of the rules P1 PR, P1 PR01 , P1 PR10        1   11
                                                                     j or P PRj (1 ≤ j ≤ 3),
respectively. By the induction hypothesis, these antecedents are derivable by rules in R, and
then the application of the corresponding rule yields M ⊢R φ.
     Finally, for TREBL formulae with multiply nested progress operators we can concentrate
on φ = □(φ1 → Y X(φ2 → Y ′ φ3 )) or φ = □1 (φ1 → Y X(φ2 → Y ′ φ3 )) with X ∈ {□, □1 },
Y, Y ′ ∈ {♢, ♢1 } and φi ∈ L. Then the appropriate prefixes exists, and M satisfies the
antecedents of the rule PRPR (or PR1 PR, respectively). By the induction hypothesis, these
antecedents are derivable by rules in R, and then the application of the rule PRPR (or
PR1 PR, respectively) yields M ⊢R φ.


                                        This work is licensed under the Creative Commons Attribution License. To view a copy of this
                                        license, visit https://creativecommons.org/licenses/by/4.0/ or send a letter to Creative
                                        Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or Eisenacher Strasse 2,
                                        10777 Berlin, Germany
