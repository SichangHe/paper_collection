Innovations in Systems and Software Engineering (2022) 18:523–541
https://doi.org/10.1007/s11334-021-00416-4

    S.I. : DETECT 2020



Formal verification and validation of run-to-completion style state
charts using Event-B
K. Morris1      · C. Snook2 · T. S. Hoang2 · G. Hulette1 · R. Armstrong1 · M. Butler2

Received: 5 January 2021 / Accepted: 15 August 2021 / Published online: 4 March 2022
© National Technology & Engineering Solutions of Sandia, LLC 2022


Abstract
State chart notations with ‘run to completion’ semantics are popular with engineers for designing controllers that react to
environment events with a sequence of state transitions but lack formal refinement and rigorous verification methods. State
chart models are typically used to design complex control systems that respond to environmental triggers with a sequential
process. The model is usually constructed at a concrete level and verified and validated using animation techniques relying
on human judgement. Event-B, on the other hand, is based on refinement from an initial abstraction and is designed to make
formal verification by automatic theorem provers feasible. Abstraction and formal verification provide greater assurance that
critical (e.g. safety or security) properties are not violated by the control system. In this paper, we introduce a notion of
refinement into a ‘run to completion’ state chart modelling notation and leverage Event-B’s tool support for theorem proving.
We describe the difficulties in translating ‘run to completion’ semantics into Event-B refinements and suggest a solution.
We illustrate our approach and show how models can be validated at different refinement levels using our scenario checker
animation tools. We show how critical invariant properties can be verified by proof despite the reactive nature of the system
and how behavioural aspects of the system can be verified by testing the expected reactions using a temporal logic, model
checking approach. To verify liveness, we outline a proof that the run to completion is deadlock-free and converges to complete
the run.

Keywords Run to completion · State charts · Refinement · Event-B


                                                                            1 Introduction

                                                                            Reactive State charts are open systems capable of receiv-
                                                                            ing potentially non-deterministic input. State charts provide
B K. Morris                                                                 a graphical language, generalised from state machines,
     knmorri@sandia.gov                                                     that is popular with engineers. Variants appear in MAT-
     C. Snook                                                               LAB Simulink/Stateflow [13] and the ANSYS tools. It is
     cfs@soton.ac.uk                                                        particularly attractive, to provide accessibility to abstrac-
     T. S. Hoang                                                            tion/refinement via Rodin/Event-B which has an intuitive
     t.s.hoang@soton.ac.uk                                                  metaphor in the State chart semantics [15–17]. The hope is
     G. Hulette                                                             that engineers can better understand the origin of proof obli-
     ghulett@sandia.gov                                                     gations in refinements and achieve formal guarantees earlier
     R. Armstrong                                                           in their designs where it is most tractable. Our approach is
     rob@sandia.gov                                                         focused on a mapping to Event-B where safety properties
     M. Butler                                                              preservation is key. In our version of State chart semantics,
     mjb@soton.ac.uk                                                        refinement means a subset of traces from an abstraction. This
                                                                            has the beneficial effect of preserving safety properties from
1    Sandia National Laboratories, 7011 East Avenue Livermore,              abstraction to refinement and permits proofs to be discharged
     California 94550, USA
                                                                            at the highest tractable level of abstraction where they are the
2    ECS, University of Southampton, Southampton SO17 1BJ,                  easiest to discharge.
     UK


                                                                                                                                 123
524                                                                                                                           K. Morris et al.


    This manuscript is structure as follows: Sect. 2 discusses      ear temporal logic (LTL) and use the ProB1 model checker
related work on refinement and what are the different types.        to verify it, as we have shown in previous work [16]. In this
Section 3 provides background material. Section 4 discusses         paper, we outline a proof of liveness properties that relies on
the State chart concept of ‘run to completion’ and how it           reasoning about deadlock-freeness and event convergence.
can be specified in Event-B. Section 5 states the different            A method that is closely related to Event-B and also
state chart refinement rules we use to construct models. Sec-       supports reasoning about safety and liveness properties is
tion 6 introduces our example case study: a drone. Section 7        TLA+ [11]. TLA+ is supported by the TLA+ Toolbox [9].
gives an outline of our translation from State Chart XML            On the one hand, temporal properties (both safety and live-
(SCXML) to Event-B via UML-B. Section 8 describes the               ness) are explicitly stated as properties of the TLA+ models
use of UML-B animation and Scenario Checking tools to               and reasoning about them often requires applying proof rules
validate translated SCXMLmodels. Section 9 illustrates our          related to properties of traces. On the other hand, Event-
approach to verifying safety invariant properties. Section 10       B defines proof obligations based on the underlying trace
illustrates our approach to verifying control responses, and        semantics [1,7,8], and hence, reasoning about implicit tem-
Sect. 11 concludes.                                                 poral properties in Event-B simply involves discharging the
                                                                    relevant proof obligations. Furthermore, at the time of writ-
                                                                    ing, the TLA+ Proof System (part of the TLA+ Toolbox) does
                                                                    not fully support the reasoning with many temporal opera-
                                                                    tors. 2
2 Related work

Many incompatible definitions of refinement have been               3 Background
posed by others [12,20] and that can lead to confusion.
Though these separate refinements have different goals, all         3.1 Event-B
of which may be attractive to systems designers in different
ways, they will not always preserve safety properties. From         Event-B [1,6] is a formal method for system design. It uses
the Event-B vernacular, it might be better to relabel these         refinement to introduce system details gradually into the for-
other approaches not as methods of model ‘refinement’, but          mal model. An Event-B model contains two parts: contexts
rather methods of model ‘elaboration’. Preservation of safety       and machines. Contexts contain carrier sets, constants, and
properties across refinement requires only a few restric-           axioms constraining the carrier sets and constants. Machines
tions to the original [5] State charts (e.g. transitions cannot     contain variables v, invariants I(v) constraining the variables,
cross containment boundaries arbitrarily), but still allows         and events. An event consists of a guard denoting its enabled
for both parallel and hierarchical composition. With these          condition and an action defining the value of variables after
restrictions, composition becomes a refinement, but not all         the event is executed. In general, an event e has the form:
refinements are compositions. Such a unification of compo-          any t where G(t, v) then S(t, v) end where t are the event
sition and refinement can lead, not only to code reuse, but         parameters, G(t, v) is the guard of the event, and S(t, v) is
reuse of proofs.                                                    the action of the event.
    If an Event-B model B can be shown (via the construction           Machines can be refined by adding more details. Refine-
rules of the Event-B language as well as the proof obligations)     ment can be done by extending the machine to include
to refine another Event-B model A, then we know that every          additional variables (superposition refinement) representing
behaviour of B is also a behaviour of A. This definition yields     new features of the system, or by replacing some (abstract)
a useful principle of preservation of safety—if we can show         variables by new (concrete) variables (data refinement).
that a bad thing never happens in A, then we can add detail         Refinement in Event-B is reasoned on an event basis. A (con-
via refinements in B, knowing that the bad thing will continue      crete) event f refines an (abstract) event e if whenever f is
to never happen in B. That is, Event-B refinements preserve         enabled, then e is also enabled (guard strengthening), and
safety properties in the sense adopted by Lamport [10]. This        the action of f is the same or equivalent to e (where equiva-
makes refinement a useful technique in developing safety-           lence is given by some relationship defined in the invariants).
critical systems: one can analyse a simpler abstract model          New events are said to refine ‘skip’ (an implicit abstract event
for critical safety properties and then add detail to the model     that did nothing) and therefore do not alter abstract vari-
via refinements, secure in the knowledge that the safety prop-
erties will be preserved. While Event-B refinements have also       1 ProB is an animator, constraint solver and model checker for the B-
been shown to preserve some liveness properties under cer-          Method. https://www3.hhu.de/stups/prob.
tain conditions [7], there are not yet efficient supporting tools   2 http://tla.msr-inria.inria.fr/tlaps/content/Documentation/

for the technique. Instead, we can express the property in lin-     Unsupported_features.html (accessed June 2021).


123
Formal verification and validation of run-to-completion…                                                                                   525


ables. More information about Event-B refinement can be                 simple guarded action semantics and does not have a con-
found in [1]. Event-B is supported by the Rodin Platform                cept of triggers and run to completion. Here, we make use of
(Rodin3 ) [2].                                                          UML-B’s state machine translation but provide a completely
   Proof obligations are generated to ensure the consistency            different semantic by generating a behaviour into the under-
of Event-B models. An important proof obligation in Event-              lying Event-B events that are linked to the generated UML-B
B is invariant preservation to prove that safety properties             transitions.
(encoded as invariants of the models) will not be violated for
any reachable states. In this paper, we also make use of other          3.3 SCXML
proof obligations in Event-B such as (relative) deadlock-
freeness and (conditional) event convergence to construct               SCXMLis a modelling language based on Harel state charts
our proof of liveness properties under some fairness assump-            with facilities for adding data elements that are modified by
tions.                                                                  transition actions and used in conditions for their firing [21].
   For the trace semantics corresponding to Event-B machines            SCXMLfollows a ‘run to completion’ semantics, where trig-
and the interpretation of LTL properties over traces, we refer          ger events4 may be needed to enable transitions. Trigger
the readers to [7]. Here, we recall the notation for fair-              events are queued when they are raised, and then, one is
ness assumptions underlying event-based formalisms such as              de-queued and consumed by firing all the transitions that it
Event-B [8,10]. Given an event e , a weak-fairness assump-              enables, followed by firing the untriggered transitions that
tion WF(e) states that if e is enabled continually, then it must        become enabled due to the change of state caused by the
occur infinitely often. Similarly, a strong-fairness assumption         initial transition firing. This is repeated until no transitions
SF(e) states that if e is enabled infinitely often, then it must        are enabled, and then, the next trigger is de-queued and con-
occur infinitely often. Formally,                                       sumed. Note that the enabledness of transitions is calculated
                                                                        batch-wise at each step, not after each and every transition.
           WF(a) ⇔ (FG enabled(e) ⇒ GF [e]) , and
                                                                        Hence, the set of parallel transitions that are enabled by a trig-
            SF(a) ⇔ (GF enabled(e) ⇒ GF [e]) ,
                                                                        ger is calculated and then only those are fired, irrespective
where G and F are the temporal operators denoting globally,             of whether firing one may disable or enable another. Sim-
and finally, respectively, and enabled(e) denotes that event            ilarly, the set of parallel untriggered transitions to be fired
e is enabled and [e] denotes an occurrence of event e .                 is calculated at each iteration before any is fired. There are
                                                                        two kinds of triggers: internal triggers are raised by tran-
3.2 UML-B State machines                                                sitions, and external triggers are raised by the environment
                                                                        (non-deterministically for the purpose of our analysis). An
UML-B [18] provides a diagrammatic modelling notation for               external trigger may only be consumed when the internal
Event-B in the form of state machines and class diagrams.               trigger queue has been emptied.
The diagrammatic models relate to an Event-B machine and                    State charts, with ‘run to completion’ semantics, are con-
generate or contribute to parts of it. For example, a state             sidered to be a synchronous language in the sense that
machine will automatically generate the Event-B data ele-               the external triggering event waits for the behaviour that
ments (sets, constants, axioms, variables, and invariants) to           it enables to complete before making any further progress.
implement the states. Transitions contribute further guards             In contrast, Event-B has an asynchronous semantics due to
and actions representing their state change, to the events that         the non-deterministic selection of events to fire. Of course,
they elaborate. State machines are typically refined by adding          synchronous behaviour can be explicitly modelled by the
nested state machines to states. Each state is encoded as a             addition of control variables that define the enabledness of
Boolean variable, and the current state is indicated by one             events (i.e. remove the non-determinism). This is how we
of the Boolean variables being set to TRUE. An invariant                can define the translation suggested in this paper. UML-B
ensures that only one state is set to TRUE at a time. Events            state machines constrain the firing of transitions to some
change the values of state variables to move the TRUE value             extent but, like Event-B, do not have an underlying fully
according to the transitions in the state machine. While the            synchronous semantics. The advantage of an asynchronous
UML-B translation deals with the basic data formalisation               semantics is its flexibility. However, when we wish to model
of state machines, it differs significantly from the seman-             processes that are essentially synchronous in nature, the need
tics discussed in this manuscript. UML-B adopts Event-B’s               to explicitly add the synchronous semantics to each model
                                                                        becomes a burden, obscuring the particular problem being
3 An extensible toolkit which includes facilities for modelling, ver-
                                                                        modelled. Since many components (e.g. controllers) used
ifying the consistency of models using theorem proving and model
checking techniques, and validating models with simulation-based        4 In SCXML, the triggers are called ‘events’; however, we refer to them

approaches.                                                             as ‘triggers’ to avoid confusion with Event-B.


                                                                                                                                   123
526                                                                                                                    K. Morris et al.


in a system are based on synchronous behaviour, we are                  The specification of this basis consists of an Event-B con-
interested in adapting a modelling language with run-to-            text and machine that are the same for all input models and
completion semantics to support Event-B style refinement.           are refined by the specific output of the translation. The basis
We chose SCXMLas our source language because it is                  context, shown in Listing 2, introduces a set of all pos-
relatively simple compared to some run-to-completion mod-           sible triggers, SCXML\_TRIGGER which is partitioned into
elling languages yet has a well-defined action language and         internal and external triggers (e.g. FutureInternalTrigger and
simulation tool support.                                            FutureExternalTrigger, respectively), some of which will be
                                                                    introduced in future refinements. At each refinement, these
                                                                    trigger sets are further partitioned to introduce more concrete
 1   while running:                                                 triggers, leaving a new abstract set to represent the remaining
 2    while completion = false                                      triggers yet to be introduced.
 3      if untriggered_enabled                                          The context also models sequences of triggers as a data
 4        execute(untriggered())
                                                                    type to be used for the trigger queues. Our initial work mod-
 5      elseif IQ = ∅
 6        execute(IQ.dequeue)                                       elled queues abstractly as sets of triggers which was adequate
 7      else                                                        for most verification purposes but does not enforce fairness
 8        completion = true                                         on trigger consumption [15–17]. Hence, we were forced to
 9      endif
                                                                    introduce fairness assumptions regarding trigger consump-
10    endwhile
11    if EQ = ∅                                                    tion in order to verify liveness properties. In this paper, we
12      execute(EQ.dequeue)                                         introduce sequences to properly model the trigger queues
13      completion = false                                          which are an implementation of this fairness property. Note
14    endif
                                                                    that the queue also enables the same trigger to be raised twice
15   endwhile
                                                                    in the queue which was not possible in a set. The constant Seq
Listing 1 Pseudocode for ’run to completion’                        returns the set of all possible sequences of a given subset of
                                                                    triggers and is defined using lambda calculus. Constant func-
                                                                    tions are also defined for the usual operations on sequences:
                                                                    length of a given sequence, append a trigger to the end of a
    Listing 1 shows a pseudocode representation of the run-         sequence to give a new sequence, concatenate two sequences
to-completion semantics as defined within the latest W3C            to give a new sequence, return the trigger at the head of a
recommendation document [21]. Here, IQ and EQ are the               sequence, return the sequence that makes up the tail of a
triggers present in the internal and external queues, respec-       sequence, and return the content (set of triggers) involved in
tively. We adopt the commonly used terminology where a              a sequence. The basis context also defines several theorem
single transition is called a micro-step and a complete run         properties about sequences that are needed to discharge proof
(between de-queueing external triggers) is referred to as a         obligations. These are omitted from Listing 2 for brevity.
macro-step.                                                             Each of the transitions in the basis (see Fig. 1) repre-
    SCXMLdoes not contain any notion of refinement. A sin-          sents an abstract event of the basis machine (Listing 3) that
gle model contains all details to the finest level, hence making    describes the generic behaviour of models under a run-to-
it difficult to verify and validate that the model behaves safely   completion semantics. These events provide an abstraction
and as intended. Our aim in this work is to support for-            that defines the altering of trigger queues and completion
mal refinement of SCXMLmodels so that verification can              flag. Event-B refinement rules prohibit new events from
be carried out at abstract levels before all details are present.   modifying abstract variables (i.e. new events refine ‘skip’).
However, applying the refinement rules in the presence of           Hence, since SCXMLtransitions need to modify the trigger
the run-to-completion semantics is not straightforward. For         queues, etc., used to capture the SCXMLrun-to-completion
example, if we apply Rule A (see Sect. 5) to a transition, it is    semantics, all events generated by translation of the spe-
more easily disabled causing the run to complete earlier (i.e.      cific SCXMLmodel must refine abstract events introduced
completion has a weaker guard), breaking Rule A.                    for this purpose in the basis. The basis machine also declares
                                                                    variables that correspond to the currently de-queued trigger,
                                                                    dt, the queue of internal triggers raised by actions within
4 Run to completion                                                 the model, iQ, the queue of external triggers raised by the
                                                                    environment, eQ, and a flag, uc, that signals when a run-to-
The run-to-completion semantics is specified via an abstract        completion macro-step has been completed. (No untriggered
basis that is extended by the model [15,17]. Figure 1 shows a       transitions are enabled.) Note that, for convenience, the cur-
state chart representation of how the basis enforces the run-       rently de-queued trigger, dt, is modelled as a singleton set
to-completion semantics on the model transitions.


123
Formal verification and validation of run-to-completion…                                                                       527




Fig. 1 Abstract representation of run-to-completion basis


which may be empty (i.e. consumed) or contain the single            allel is needed because of the batch enabling semantics of
trigger to be consumed.                                             the SCXML run to completion (see Sect. 3.3). The actions of
    The trigger queues and de-queued trigger are                    these transitions may also raise triggers of their own in the
initialised to empty and uc is set to FALSE so that any enabled     internal trigger queue iQ.
untriggered transitions are dealt with via the                          Completion of triggered and untriggered transitions may
futureUntriggeredTransitionSet event when the system first          be non-deterministically premature to allow future refine-
starts (see Listing 1). This will subsequently enable com-          ments to strengthen the guards of transitions (i.e. to disable
pletion and reset the uc flag to TRUE. The abstract event           them resulting in an earlier completion). In the process
futureRaiseExternalTrigger represents the raising of an             of refining a model, a designer takes advantage of this
external trigger (not shown in Fig. 1). After completion, a         non-determinism in the abstraction by adding nested sub-
queued trigger can be prepared for consumption by mov-              states and explicit guards to transitions. When a refine-
ing it to the de-queued trigger, dt. Internal triggers have a       ment level is reached where the designer wants to enforce
higher priority, since the external trigger queue is only de-       a requirement (i.e. prevent it being bypassed by a non-
queued if the iQ is empty (see dequeueExternalTriggered             deterministic completion), the model needs to be finalised
and dequeueInternalTriggered in Fig. 1). The abstract event         (see Sect. 7 for more on finalisation). The SCXMLtrans-
futureTriggeredTransitionSet represents a combination of            lation tool will then automatically strengthen the guards
parallel transitions that may be simultaneously triggered by        of      events      noTriggeredTransitionsEnabled          and
the de-queued trigger, dt. When the actual example SCXM-            noUntriggeredTransitionsEnabled, to ensure that the run-
Lis translated, a separate refinement of this abstract event will   to-completion sequence is not interrupted by non-determini-
be generated for each subset of the set of parallel transitions     stic behaviour. To do this, we need to guard completion
that could fire in parallel in order to cater for all possibili-    so that it cannot happen, while any relevant transition is
ties of enablement; however, as the model is refined, some          still enabled. To finalise a triggered transition, the guard of
combinations may be eliminated as the guards are strength-          noTriggeredTransitionsEnabled is strengthened by adding
ened. This approach to generating an event for each possible        the conjunction of the negated guards of all transitions
combination of each set of transitions that could fire in par-      that can fire in parallel with the transition being finalised.


                                                                                                                        123
528                                                                                                                                                                   K. Morris et al.


                                                                                                6      uc
 1   context                                                                                                // run to completion flag
 2    basis_c                                                                                   7      dt
            // (generated for SCXML)                                                                        // dequeued trigger for this run
 3   sets                                                                                       8    INVARIANTS
 4    SCXML_TRIGGER                                                                             9      iQ ∈ InternalQueueType
            // all possible triggers                                                                        // internal queue
 5   constants                                                                                  10     eQ ∈ ExternalQueueType
 6    FutureInternalTrigger                                                                                 // external queue
            // all possible internal triggers                                                   11     uc ∈ BOOL
 7    FutureExternalTrigger                                                                                 // completion flag
            // all possible external triggers                                                   12     dt ⊆ SCXML_TRIGGER
 8    Seq                                                                                                   // dequeued trigger
            // return all possible sequences of given set of triggers                           13     dt=∅ ⇒(∃t.dt={t})
 9    length                                                                                                // at most one dequeued trigger
            // return the length of a sequence of triggers                                      14   EVENTS
10    append                                                                                    15    INITIALISATION
            // return the result of appending trigger to a sequence                                         // queues empty, completion false, no dequeued triggers
11    concat                                                                                    16       iQ, eQ, uc, dt := ∅, ∅, FALSE, ∅
            // return the concatenation of two sequences of triggers                            17    END
12    head                                                                                      18
            // return the trigger at head of a sequence of triggers                             19    futureRaiseExternalTrigger
13    tail                                                                                                 //basis of future event to raise an external trigger
            // return the sequence at tail of a sequence of triggers                            20      ANY raisedTrigger WHERE raisedTrigger ∈ FutureExternalTrigger
14    content                                                                                   21      THEN eQ:=append(eQ → raisedTrigger)
            // return the set of triggers in a sequence of triggers
15    InternalQueueType                                                                         22    END
            // type of internal queues                                                          23
16    ExternalQueueType                                                                         24    dequeueInternalTriggered
            // type of external queues                                                                    //event to dequeue an internal trigger
17                                                                                              25     WHEN iQ=∅ ∧ dt=∅ ∧ uc=TRUE
18   axioms                                                                                     26     THEN dt, iQ, uc := {head(iQ)}, tail(iQ), FALSE
19    partition(SCXML_TRIGGER, FutureInternalTrigger, FutureExternalTrigger)                    27    END
20    Seq = (λ T . T ⊆ SCXML_TRIGGER | {n, s . n ∈ N∧ s ∈ 0 .. n − 1 → T| s})                   28
21    length = (λs . s ∈ Seq(SCXML_TRIGGER) | card(s))                                          29    dequeueExternalTriggered
22    append = (λ s → t . s ∈ Seq(SCXML_TRIGGER) ∧ t ∈ SCXML_TRIGGER |                                    //event to dequeue an external trigger
23      {i →v | i ∈ 0 .. length(s) ∧ (i < length(s) ⇒ v = s(i)) ∧ (i = length(s) ⇒ v = t) } )   30     WHEN eQ=∅ ∧ dt=∅ ∧ uc=TRUE ∧ iqQ∅
24    concat = (λ s1 → s2 . s1 ∈ Seq(SCXML_TRIGGER) ∧ s2 ∈ Seq(SCXML_TRIGGER)                   31     THEN dt, eQ, uc := {head(eQ)}, tail(eQ), FALSE
            |                                                                                   32    END
25      {i →v | i ∈ 0 .. length(s1) + length(s2) − 1 ∧ (i < length(s1) ⇒                        33

26                   v = s1(i)) ∧ (i ≥ length(s1) ⇒ v = s2(i − length(s1))) } )                 34    futureTriggeredTransitionSet
                                                                                                            //basis of future event representing triggered transitions
27    head = (λs . s ∈ Seq(SCXML_TRIGGER) ∧ s = ∅ | s(0))                                      35      ANY trigger, raisedTriggers WHERE
28    tail = (λs. s∈Seq(SCXML_TRIGGER) ∧ s =∅ | {i→v | i∈0..length(s)−2 ∧ v=s(i+               36       trigger ∈ dt ∧ uc = FALSE ∧ raisedTriggers ∈ Seq(FutureInternalTrigger)
            1)} )                                                                               37      THEN dt, iQ := ∅ , concat(iQ→raisedTriggers)
29    content = (λs . s ∈ Seq(SCXML_TRIGGER) | ran(s))                                          38    END
30    InternalQueueType = Seq(FutureInternalTrigger)                                            39
31    ExternalQueueType = Seq(FutureExternalTrigger)                                            40    noTriggeredTransitionsEnabled
32   end                                                                                                   //event to fire when no triggered transitions enabled
33                                                                                              41     WHEN uc=FALSE ∧ dt=∅
                                                                                                42     THEN dt := ∅
                                                                                                43    END
Listing 2 Abstract basis context                                                                44
                                                                                                45    futureUntriggeredTransitionSet
Similarly, to finalise an untriggered transition, the guard                                                //basis of future event representing untriggered transitions
                                                                                                46      ANY raisedTriggers WHERE uc=FALSE ∧ dt=∅ ∧ raisedTriggers∈Seq(
of noUntriggeredTransitionsEnabled is strengthened by                                                      FutureInternalTrigger)
                                                                                                47      THEN iQ := concat(iQ→raisedTriggers)
adding the conjunction of the negated guards of all untrig-                                     48    END
gered transitions that can fire in parallel. It may seem                                        49
                                                                                                50    noUntriggeredTransitionsEnabled
that finalisation could cause an unmanageable explosion of                                                //event fired when no untriggered transitions enabled
guards. However, to fire in parallel, transitions must be con-                                  51     WHEN uc=FALSE ∧ dt=∅
                                                                                                52     THEN uc := TRUE
tained in parallel regions and also be enabled by the same                                      53    END
                                                                                                54   END
trigger (or be untriggered). In practice, since most systems do                                 55
not contain many parallel regions, the number of transitions
that can fire in parallel is limited. Transition finalisation can                               Listing 3 Abstract basis machine
be left until it is needed for the proof of a particular property
and does not generate any new proof obligations since adding
guards is a trivial refinement step. Finalisation is also needed                                5 State chart refinement
in order to remove non-deterministic behaviours when the
model is animated for validation purposes.                                                      The work presented here includes three refinement rules.

 1   MACHINE basis
          // (generated for SCXML)
 2   SEES basis_ctx                                                                             1. Rule A: Guard conditions on a transition can be strength-
 3   VARIABLES
 4     iQ
                                                                                                   ened (but not weakened); this can be done by adding
          // internal trigger queue                                                                textual guards to the transition, or changing the source of
 5     eQ
          // external trigger queue                                                                the transition to a nested state.


123
Formal verification and validation of run-to-completion…                                                                           529

Fig. 2 State chart refinement
rules




2. Rule B: Transitions can have additional actions, provided       that obey the rules. This will allow us to prove properties of
   they do not modify variables appearing in the abstraction;      the model in a very strategic fashion, as properties proven
   this can be accomplished by adding textual action to the        of early abstraction levels are preserved in later refinements.
   transition or by changing the target to nested state.           Unlike other case studies previously presented [14,15,17],
3. Rule C: A state chart can be embedded within a state of         this drone example illustrated the model construction and
   another state chart—sometimes called hierarchical com-          analysis of a more complex system with several parallel com-
   position or hierarchical refinement.                            ponents and refinement levels.
                                                                       The initial abstraction and first refinement of the model,
   The application of these rules is illustrated in Fig. 2. Rule   shown in Fig. 3, capture the basic functionality of the drone.
A is applied to refine the abstract transition from SA to SB       The abstract model is shown in blue; the model’s initial state
after adding child states SC and SD. The refinement strength-      is OFF and as a result of the on and toTakeoﬀ external trig-
ens the guard of the transition by restricting it to SD. On        gers it transitions to the START and OPERATIONAL states,
the other hand, Rule B refines the abstraction by introduc-        respectively.5 The drone reacts to the oﬀ external trigger
ing a new concrete variable, x, into the model. The abstract       by shutting down and subsequently transitioning to the OFF
transition is refined by the actions associated with this new      state. The first refinement is constructed using Rule C, which
variable. Finally, Rule C constructs a refinement introduc-        adds details within the OPERATIONAL state (grey states in
ing state charts SC, SD and SG, SH through hierarchical and        Fig. 3). Within the OPERATIONAL state, the drone will tran-
parallel composition, respectively.                                sition to FLY or DESCEND after the internal trigger toFly
   Via the translation explained in Sect. 7, these rules rely      or toLand is raised, respectively. In refinement level one,
on the usual Event-B proof obligations to ensure that they do      these internal triggers are raised non-deterministically in the
indeed yield refinements in the Event-B semantics.                 system by functionality not currently defined. As additional
                                                                   details are incorporated into the model in later refinements,
                                                                   some of that non-determinism is removed and replaced by
6 Description of the sample application                            transitions with actions that raised the previously defined
                                                                   internal triggers. A further external trigger, landed, directs
To illustrate the development and analysis process of a design     the system to progress to the LANDED state. It should be noted
using the previously described state chart semantics, we           that this abstraction of the drone model includes a transition
will discuss a quadrotor helicopter or quadrotor application       from TAKEOFF to DESCEND (dashed transition in Fig. 3).
similar to the one presented by Syriani et al. [20]. The appli-    This allows for the drone to respond to a toLand trigger if it
cation will focus on the incremental design of some of the         encounters some problems while in the TAKEOFF state. Syr-
drone’s required functionality. The constructed model must         iani et al. [20] introduce this transition in later refinements
obey state chart refinement rules listed in Sect. 5, and these
rules are proven within the Rodin tool. The structure of the
state chart for this model at each subsequent abstraction level    5 Transitions in Figs. 3 and 4 are labelled with trigger names (e.g.

restricts further the development of the model to refinements      toTakeoff, toFly) not with event names as it is in UML-B.


                                                                                                                               123
530                                                                                                                             K. Morris et al.




Fig. 3 State chart of drone application. Abstract level including only generic start/shutdown behaviour (shown in blue). The first refinement
introducing main operational sub-states is shown in grey


under Rule 8 path refinement rule. This rule is inconsistent            al. [20] As part of this refinement, we introduced an untrig-
with our rules of refinement as it results in a concrete event          gered transition responsible for raising the toFly internal
with no corresponding behaviour in the abstraction.                     trigger and therefore removed some of the non-determinisms
   Figure 4 builds in Fig. 3 to show three more refinements             concerning this trigger.
to the drone model. The second refinement (shown in green                   The fourth refinement of the drone model (shown in lilac)
in Fig. 4) extends the capabilities within OPERATIONAL by               uses Rule C to introduce additional implementation details to
using Rule C to make it a parallel state that controls flying and       allow a take-off to be cancelled in response to an external trig-
battery related functionality. This is the same as Rule 4 and-          ger cancel. If the trigger is raised, the climbing process must
state rule defined by Syriani et al. [20]. The charge within the        be aborted and the drone descending sequence shall start.
drone battery is monitored by the parallel BATTERYOP state.             This refinement level is done differently to Syriani et al. [20],
A new ancillary variable, charge, is introduced to keep track           which follows Rule 7 state extension rule. The aforemen-
of the amount of charge left in the drone. It is decreased by a         tioned rule requires a data remapping of the abstract states
self-transition on state BATTERYOK in response to an exter-             TAKEOFF, CLIMB, and HOVER, which should be distinct from
nal trigger decreaseCharge. If the battery monitor works                the states in this refinement, as the state ABORT is introduced.
correctly, we would expect the battery charge to have at least          In contrast, we implement this refinement using a rule similar
20% capacity while in the state BATTERYOK. This can be                  to Syriani et al.’s Rule 2 basic-to-or state rule, which intro-
expressed as an invariant property:                                     duces the concrete states CLIMB2 and ABORT to the abstract
                                                                        state CLIMB.
          (BATTERYOK = TRUE) ⇒ charge > 20% .                               Although the autonomous drone example in this paper
                                                                        is based on the example described in [20], the definition of
When the monitored charge drops to 20% or less, the                     refinement used in that work is quite different from our own.
BATTERY state chart raises the internal trigger toLand, which           This forces some differences in our refinement rules, and
will cause a reaction in the FLYOP start chart to bring it out of       consequently, the way the example is developed. In [20],
TAKEOFF or FLY and into DESCEND (hence removing some                    ‘refinement’ is a transformation of the model which pre-
of the non-determinism concerning where toLand is raised).              serves reachability of a state with respect to sequences of
While in the TAKEOFF state, we would expect the battery                 inputs. However, this also allows the possibility of introduc-
monitor to be in the BATTERYOK state or to have raised a                ing new behaviours in the concrete model that the abstraction
toLand trigger.                                                         does not exhibit. While this notion of refinement seems use-
   (TAKEOFF = TRUE) ⇒ (BATTERYOK = TRUE ∨ toLand) .                     ful in certain contexts, unlike refinement in Event-B it does
                                                                        not guarantee preservation of safety properties. Therefore, it
    To ensure the drone only enters TAKEOFF or FLY with                 should be considered less suited to development of safety-
enough battery power, we strengthen the guards of transitions           critical systems.
to the FLY and TAKEOFF states (Rule A). We will discuss how
these state-invariant properties are verified in Sect. 9.
    The third refinement of the model (shown in beige) refines
the state TAKEOFF by applying Rule B and C. Under these
rules, we introduce child states and new model variables,
similar to Rule 2 basic-to-or state rule defined by Syriani et


123
Formal verification and validation of run-to-completion…                                                                                  531




Fig. 4 State chart of drone application. Second refinement for battery monitoring functionality (shown in green). Third refinement introducing
details for take-off (shown in beige). Fourth refinement level to allow cancelling during take-off (shown in lilac)


7 SCXMLtranslation to UML-B/Event-B                                         set), is introduced to define the raised triggers parameter.
                                                                            The subset used in the guard retains non-determinism to
The translation of a specific SCXMLmodel to UML-B and                       allow more triggers to be raised in later refinements. For
Event-B comprises the following stages:                                     triggered transitions, the trigger is specified by a guard
                                                                            that defines the value of the trigger parameter.
 – Firstly, a basis machine and context are created to embody             – Thirdly, at each refinement level, the SCXMLstate chart
   the semantics of the SCXMLlanguage (as described in                      is translated into a corresponding UML-B state machine
   Sect. 4). The basis provides variables and events to model               whose transitions elaborate (i.e. add state change details
   the queue of triggers as well as abstract versions of events             to) the transition combination events that the transition
   to model transitions firing. The basis is independent of the             may be involved in. A transition may fire in parallel with
   particular SCXMLmodel which is added in subsequent                       transitions of parallel nested state machines that have the
   refinements. Hence, it is not necessary to re-prove any of               same (possibly null) trigger.
   the proof obligations associated with this basis.                      – Finally, the UML-B state machine is translated into
 – Secondly, all possible combinations of each set of transi-               Event-B by programmatically invoking the UML-B
   tions that can fire together are calculated and correspond-              translator.
   ing events are generated, at appropriate refinement levels
   (given by the refinement annotations embedded in the                     A previous version of the translator was described in [15,
   SCXMLmodel) that refine the abstract basis events. The                16]. New features of the translation added since [15,16] are
   transitions that can fire together are those that are trig-           as follows:
   gered by the same trigger (or are both untriggered) and
   are in different parallel (‘and’) sub-states. For example,                Trigger queues in basis: The encoding of trigger queues in
   the untriggered transitions shown in the parallel states                  the abstract basis context and machine has been improved
   FLYOP and BATTERYOP of Fig. 4 are combined into                           so that a queue is properly modelled as a sequence of
   an event in the Event-B representation of the model,                      triggers. This more accurately reflects the SCXMLse-
   through a conjunction of the guards and actions of                        mantics.
   each of the transitions. If these transitions raise internal              De-queuing triggers from queues: The abstract basis
   triggers, a guard, {i1, i2, ...} ⊆ content(raisedTriggers)                machine has been improved so that triggers are properly
   (where i1, i2, ... have been added to the internal triggers               de-queued before potential use, which allows triggers to


                                                                                                                                  123
532                                                                                                                        K. Morris et al.




Fig. 5 Generated UML-B state machine for drone refinement level 2


      be discarded if the controller cannot respond to them.            SCXMLmeta-model provided by Sirius [4] which has good
      This more accurately reflects the SCXMLsemantics and              support for extensibility. The UML-B state machine is sub-
      was necessary in order to model the new drone case study          sequently translated into Event-B using the standard UML-B
      properly.                                                         translation which provides variables to model the current
      Finalisation: Transitions can be flagged as finalised which       state and guards and actions to model the state changes that
      means their guards can not be strengthened in subsequent          transitions perform.
      refinements. This allows them to ‘enforced’ when they                Figure 5 shows the UML-B model of the drone at refine-
      are enabled (i.e. completion cannot occur until they have         ment level 2 (equivalent to Fig. 4 without the detail inside
      fired) which is needed for verification.                          TAKEOFF). The structure of the state machine is similar to
      Restricted raising of internal triggers: Once a trigger is        the SCXMLversion with purple shading indicating the pre-
      introduced, it must immediately be raised at that refine-         viously added states and light blue shading indicating the
      ment level by any transitions that wish to do so. It cannot       detail added at this refinement level. State invariants (prop-
      be raised in later refinements except by newly introduced         erties that should hold while that state is active) are shown in
      transitions. This restriction was necessary to make simu-         TAKEOFF, FLY and BATTERYOK. Verification of these invari-
      lation more useful by removing non-deterministic raising          ants is discussed in Sect. 9.
      of triggers in anticipation of refinements.
      Context instantiation: The axioms of the basis context,
      that allow future triggers to be added, have been improved
                                                                        8 Validation
      so that ProB6 can automatically create an instantiation.
                                                                        One of the attractions of ‘run to completion’ style modelling
                                                                        languages such as SCXMLis their execution semantics which
   A tool to automatically translate SCXMLsource mod-                   provides a method for animating models to validate their
els into UML-B has been produced. The tool is based                     behaviour. Our approach to SCXMLrefinement results in a
on the Eclipse Modelling Framework (EMF) and uses an                    single SCXMLfinal model which can be animated using the
                                                                        existing SCXMLanimation tools. However, we would like to
6 ProB is an animator, constraint solver and model checker for the B-   validate the developing UML-B model at intermediate refine-
Method. https://www3.hhu.de/stups/prob.                                 ment levels.


123
Formal verification and validation of run-to-completion…                                                                           533




Fig. 6 Using Scenario Checker to validate behaviour of refinement 1—recording


    In previous work [19], we have developed a scenario-               and then automatically fires internal events until none are
based approach to formal modelling using abstract scenarios            enabled. The right-hand view shows the scenario checker
to validate abstract models. The method is supported by a              console, listing each big step and its run to completion in
‘Scenario Checker’ tool, based on the ProB model checker,              terms of internal events. The bottom centre view shows the
that allows scenarios to be recorded and then replayed to              state of the system at the end of the last run.
check that important state has not changed since the original             Figure 7 shows the recorded scenario being played back.
run of the scenario. The Scenario Checker supports the con-            In the control panel, external events are greyed out as they are
cept of a controller executing a process in response to changes        being selected from the recording each time the Big Step but-
in the environment which is similar to the run-to-completion           ton is pressed. The state view shows a discrepancy from when
concept addressed in our work here. Events may be annotated            the scenario was recorded, and the state machine is in the FLY
as internal to indicate that, when enabled, they should be fired       state instead of the DESCEND state. Comparing the history
automatically until none remain. Internal events may also be           in the console panels reveals that cause: an internal trigger,
prioritised to give a simple representation of process order           toLand, was non-deterministically raised during recording
in the controller (even if it is left non-deterministic in the         but not during playback. This is because the model allows
model). The user only has to select external events that trigger       for future raising of internal triggers in later refinements.
the controllers responses. Since our SCXMLderived models                  Figure 8 shows the scenario being played back at a later
already contain an implementation of run to completion, the            refinement where the raising of the toFly and toLand internal
support provided by the Scenario Checker is sufficient to              triggers has been defined. While the scenario checker allows
validate this behaviour. If desired, internal variables that rep-      us to animate that the main expected run-to-completion
resent the controllers processing (e.g. the variables that model       behaviour is possible, recall that unless the transitions have
the SCXMLrun-to-completion variables) can be annotated as              all been finalised (i.e. no further refinement is permitted),
private so that only the application state is checked during           other behaviours are possible due to the non-deterministic
replay. To help visualise the state of the model, the gener-           completion incorporated in case transition guards are later
ated UML-B state machine is animated during the scenario               strengthened.
validation.
    Figure 6 shows a scenario being recorded. The main (top
left) editing view shows the state machine being animated;             9 Verification of safety properties
the model is currently in the DESCEND state. The bottom
left view is the scenario checker control panel where exter-           In a state chart model, we naturally wish to verify properties
nal events can be fired to start a run to completion. In our           of the form; a property P that is expected to hold true in a
model, only the external-trigger-raising events (representing          particular state S. Hence, all of the safety properties that we
the environment) are enabled. The main button to be used               consider are captured as invariants of the form: S=TRUE ⇒ P
is the Big Step button which fires the selected external event         where the antecedent is implicit from the containment of P


                                                                                                                            123
534                                                                                                                        K. Morris et al.




Fig. 7 Using Scenario Checker to validate behaviour of refinement 1—playback




Fig. 8 Using Scenario Checker to validate behaviour of refinement 3—playback


within S. There are two kinds of properties that we might want         S in which the property is expected to hold. To cater for this,
to verify in an SCXMLstate chart: 1) properties concerning             we express P in a modified form P’ that allows time for the
the values of auxiliary data maintained by the system and              reaction to take place. There are two forms of reaction that
2) constraints about the state of another parallel state chart         can be used to exit S: a) an untriggered transition or b) a tran-
region. SCXMLmodels represent components that react to                 sition that is triggered by an internally raised trigger. For a),
received triggers and cannot be perfectly synchronised with            the modified property P’ becomes P ∨ untriggered transi-
changes to the monitored properties. Hence, P may be tem-              tions are not complete, and for b), P’ becomes P ∨ trigger t
porarily violated until the system reacts by leaving the state         is in the internal queue or de-queued (where t is the internal


123
Formal verification and validation of run-to-completion…                                                                            535


trigger raised when the violation of P is detected). Hence, P           isation means that we cannot strengthen its guards in future
is checked only in stable states that are reachable according           refinements as is normally permitted, since its reaction is
to the run-to-completion semantics.                                     needed to ensure the invariant is preserved. If the user for-
    In this section, we illustrate a typical example of the type        goes the finalisation, the property would not be verifiable at
of properties that we imagine could be verified in a reactive           that refinement level and it will need to be verified in later
SCXMLsystem. All of the proof obligations are automat-                  refinements. After translation to Event-B via UML-B, the
ically discharged for our example.7 Since our models are                invariant in state BATTERYOK is
strictly structured and proof obligations will always have this
common form, we are optimistic that proofs will always dis-                (BATTERYOK = TRUE) ⇒ (uc = FALSE ∨ charge>20) .
charge automatically. We model the safety property features                 The only events that can break this invariant are ones
at an early level of refinement where the models are rela-              that make the antecedent become true or the consequent
tively simple, so that the validity of verification conditions          become false and we deal with these as follows: the tran-
is clear. Detail is then added in later refinements which are           sitions that enter state OPERATIONAL and initialise the
proven (automatically) to preserve the previously verified              BATTERY region by entering BATTERYOK (hence making the
safety properties. In our example, some auxiliary data are              antecedent become true) contain the guard that charge>50
monitored by one state chart region, while a parallel region            (since we do not allow the drone to take off unless the bat-
refers to the state of the monitoring region. Hence, the reac-          tery is well charged) and hence the invariant is satisfied.
tion consists of an untriggered transition in the monitoring            The self-transition that decreases charge (and hence could
region which sends an internal trigger to the other region              potentially falsify the consequent) is guarded by uc = FALSE
when it leaves the desired monitor state.                               since it is a triggered transition, and hence, the disjunction
    For our drone model, the safety property that we wish to            in the consequent ensures it remains true. The comple-
verify is that the control system does not continue to take off         tion event NoUntriggeredTransitionsEnabled of the basis
or fly if the battery charge drops below a certain threshold            machine resets uc = TRUE to indicate completion of the
(say 21%). By refinement level 1, we have developed the                 cycle and hence could potentially break the invariant. How-
drone’s state to the point where we distinguish the TAKEOFF             ever, finalising the transition BATTERYOK_BATTERYLOW
and FLY states (Fig. 3). In refinement level 2, we therefore            (that leaves BATTERYOK when charge>20 becomes false)
introduce the battery charge monitoring function along with             means that the negation of its guard is added to the comple-
the associated safety properties. A parallel state chart region,        tion event by the translation. Since this transition fires when
with sub-states BATTERYOK and BATTERYLOW, is added to                   BATTERYOK = TRUE (i.e. its source state) and charge≤20,
the state OPERATIONAL (Fig. 4). The BATTERYOK sub-state                 the completion event is guarded by ¬(BATTERYOK= TRUE∧
is used in the safety invariant of the TAKEOFF and FLY states.          charge≤20) which means that it does not fire when it could
Thus, we split the verification into two parts: a type b proof to       break the invariant (i.e. forcing the untriggered reaction to
show that the system reacts to the battery charge decreasing            fire first).
below 21% (an external event) by leaving the BATTERYOK
sub-state and a type a proof to show that when the system
leaves the BATTERYOK state, it subsequently (within the run             System Subsequently Leaves the FLY or TAKEOFF States
to completion) leaves the FLY or TAKEOFF states. Both parts             The safety property of the TAKEOFF and FLY states can now
are described in more detail as follows.                                be simply stated as BATTERYOK = TRUE. However, since this
                                                                        relies on a particular internal trigger (toLand) to make the
System Reacts to the Low Battery Charge An external trig-               appropriate reaction, we also need to specify that trigger as
ger indicates that the battery charge has dropped by 10% and            an attribute of the invariant in the SCXMLmodel. After trans-
this is used by a self-transition to decrement the controllers          lation to Event-B via UML-B, the invariant in state TAKEOFF
data value for charge. The BATTERYOK state is supposed to               becomes
indicate that the battery charge is ok (>20%) and to ensure                (TAKEOFF = TRUE)
that it does, we add a state invariant to this effect (charge>20).         ⇒
When charge decreases to 20 (or less), an untriggered transi-              (toLand ∈ content(iQ) ∨ toLand∈dt ∨ BATTERYOK=TRUE).
tion immediately reacts by switching to the BATTERYLOW
state. To ensure that this reaction is not bypassed by the              The invariant for the FLY state is similar with a correspond-
non-determinism that we incorporated to allow for future                ing antecedent. The transitions that enter TAKEOFF (which
refinement, we flag it as finalised at refinement level 2. Final-       make the antecedent true) simultaneously enter BATTERYOK
                                                                        ensuring the consequent is true. The only transition that enters
7 We use a strong prover configuration including AtelierB provers and   FLY (which makes the antecedent of the FLY invariant true)
SMT solvers.                                                            comes from the TAKEOFF state and hence the consequent is


                                                                                                                             123
536                                                                                                                     K. Morris et al.


already true. The transition that leaves BATTERYOK (making               • The de-queue external trigger event (i.e. dequeue
the last disjunct of the consequent false) raises the toLand               ExternalTriggered): These events de-queue the exter-
trigger making the first disjunct true. Some transitions leave             nal trigger queue and will start a run.
the superstates of BATTERYOK, but these either simultane-                • Internal system events: These events belong to the
ously leave OPERATIONAL (the superstate of TAKEOFF and                     internal behaviour of the system to accommodate the
FLY), or re-enter BATTERYOK. The basis contains an event                   runs for external triggers. These events can be seen
to de-queue the internal triggers which preserves the over-                in different groups as in Fig. 1.
all consequent because it establishes the second conjunct as                 • The de-queue internal trigger event (i.e. dequeue
it falsifies the first (i.e. it removes toLand from the iQ but                  InternalTriggered): These events de-queue the
simultaneously adds it to dt). The only events that falsify                     internal triggers queue and will start a run.
the second conjunct are the transitions triggered by toLand                  • Triggered events: The events corresponding to
which leave the TAKEOFF or FLY states making the antecedent                     the event fired by (external or internal) triggers.
false.                                                                       • The discard trigger event (i.e. noTriggered
    Hence, invariant properties that follow these suggested                     TransitionsEnabled): This event will move the
patterns are automatically proven due to simple logic about                     system from the FIRING TRIGGERED state to the
the changes in state.                                                           FIRING UNTRIGGERED state in the case where no
                                                                                triggered transition events are enabled.
                                                                             • Untriggered events: These are all the untriggered
                                                                                events in the systems.
10 Verification of control responses                                         • The completion event (i.e. noUntriggered
                                                                                TransitionsEnabled): This event will move the
A model that has been proven to satisfy some safety (e.g.                       system from FIRING UNTRIGGERED state to the
invariant) properties may still not behave in a useful way.                     READY TO DE−QUEUE state in the case where
Therefore, as well as verifying invariant properties, we would                  no untriggered transition events are enabled.
like to verify the system’s liveness (e.g. responsive) proper-
ties. That is, we want to ensure that the controller responds       Events from different categories have different roles in our
to external triggers and makes appropriate modifications to         reasoning about responsive properties.
the system variables. These kind of liveness properties are            We now present a theorem and a corollary related to (rela-
difficult to prove via invariant preservation since they are        tive) deadlock-freeness properties for a different set of events.
temporal properties. In this section, we present our approach
to verify the responsive properties of the system.                  Theorem 1 (Internal System Events are Relative Deadlock-
   We first start with some generic properties of our gener-        Free) Under the condition that iQ = ∅ ∨ uc = FALSE ∨ dt = ∅,
ated Event-B model and the fairness assumption about the            the internal system events are deadlock-free, i.e. there must
executions of the events. We then discuss the proof for ter-        be one internal system event enabled.
mination of responses for external triggers in Sect. 10.1 and
correctness of the responses for external triggers in Sect. 10.2.   Proof This is based on the generation of our Event-B
                                                                    model (according to the basis structure as shown in Fig. 1).
                                                                    In particular, we consider the different cases correspond-
Event Categories. In our Event-B model, the events can be           ing to the different ‘states’, i.e. READY TO DE−QUEUE,
separated into the following categories.                            FIRING TRIGGERED, and FIRING UNTRIGGERED.

                                                                     – When the system is in the READY TO DE−QUEUE state,
 – External events: These events raise external triggers.              we know that uc = TRUE ∧ dt = ∅. According to our
 – System events: Events other than external events are                assumption, we then have iQ = ∅, hence dequeue
   called system events. They are the events by which the              InternalTriggered event is enabled.
   system responds to the external triggers (by creating dif-        – When the system is in the FIRING TRIGGERED state,
   ferent runs or simulation paths). These events can be seen          either one of the triggered events is enabled or the
   in Fig. 1 and are further categorised as follows.                   noTriggeredTransitionsEnabled event is enabled.
      • Future system events: These events might raise               – Similarly, when the system is in the FIRING UNTRIGGERED
        internal triggers, i.e. futureTriggeredTransitionSet,          state, either one of the untriggered events is enabled or
        and futureUntriggeredTransitionSet. The purpose                the noUntriggeredTransitionsEnabled event is enabled.
        of these events is to enable future introduction of more
        system details via refinement.                                                                                               
                                                                                                                                     


123
Formal verification and validation of run-to-completion…                                                                       537


Corollary 1 (System Events are Relative Deadlock-Free)              are anticipated, the system’s internal queue is always even-
Under the condition that eQ = ∅ ∨ iQ = ∅ ∨ uc = FALSE ∨           tually empty and the system transitions to the Ready to
dt = ∅, the system events are deadlock-free, i.e. there must       De-queue state, i.e.
be one system event enabled.
                                                                                 GF(iQ = ∅ ∧ uc = TRUE ∧ dt = ∅) .
Proof This is based on the generation of our Event-B model
                                                                    Proof Assuming that the properties are not satisfied, i.e.
(according to the basis structure as shown in Fig. 1) and
                                                                    eventually, it is always the case that iQ = ∅ ∨ uc = FALSE ∨
Theorem 1.
                                                                    dt = ∅. This can be formalised as follows.
 – In the case where iQ = ∅ ∨ uc = FALSE ∨ dt = ∅, accord-                    FG(iQ = ∅ ∨ uc = FALSE ∨ dt = ∅) .
   ing to Theorem 1, one of the internal events is enabled.
                                                                    Observe that in the states satisfying this condition, the
 – Otherwise, i.e. iQ = ∅ ∧ uc = TRUE ∧ dt = ∅, according
                                                                    dequeueExternalTriggered event is disabled. Furthermore,
   to our assumption, eQ = ∅. In this case, the dequeue
                                                                    according to Theorem 1, the internal events will always be
   ExternalTriggered event is enabled.
                                                                    deadlock-free, and as a result, at least one of the internal
                                                                    event is enabled infinitely often, hence under Assumption 1,
                                                               
                                                               
                                                                    this event occurs infinitely often. According to Definition 1,
   In order to reason about any liveness properties for an          the variant will be decreased infinitely which violate the con-
event system, we have to make assumptions about how often           dition that the variant is defined on an well-founded order.
events will be fired. Here, we assume that all the system           Here, the external events are anticipated to ensure that the
events are strongly fair.                                           variant does not increase and hence does not interfere with
                                                                    the convergence of the internal events.                      
                                                                                                                                 
Assumption 1 (Fair System Events) We assume that all
internal system event e is strongly fair, i.e. SF(e) ; and             Note that Theorem 2 relies on convergence of internal
the de-queue external trigger event is weakly fair, i.e.            events and anticipation of external events, which we will
WF(dequeueExternalTriggered) .                                      prove later.

This assumption will ensure that the system will response           Theorem 3 (Responsiveness to External Triggers) If an
no matter how often the external triggers are raised by the         external trigger is raised, then eventually, it will be de-
external events.                                                    queued.
                                                                    G([externalTrigger.t] ⇒ F([dequeueExternalTriggered.t])) ,
10.1 Termination of responses for external triggers
                                                                    where we use externalTrigger.t (resp. [dequeueExternal
We first define the notion of event convergence and event           Triggered.t]) to denote the occurrence of externalTrigger
anticipation.                                                       (resp. dequeueExternalTriggered) with parameter t.
Definition 1 (Event Convergence) A set of events is said to         Proof Assuming that [externalTrigger.t] hence t ∈ content
be convergent if they all decrease a variant according to some      (eQ), i.e. eQ = ∅. According to Theorem 2, we have that
well-founded order.                                                 dequeueExternalTriggered is enabled infinitely often. Since
                                                                    dequeueExternalTriggered is weakly fair (Assumption 1),
Definition 2 (Event Anticipation) Given a set of convergent         it is taken infinitely. We have two cases.
events with respect to a variant, another set of events is antic-
ipated with respect to the same variant if they do not increase      – If t = head(eQ), it means we have [dequeueExternal
the variant.                                                           Triggered.t]
   Note that the anticipated events augment the set of con-          – If t = head(eQ), an occurrence of dequeueExternal
vergent events and respect the variant used to prove the               Triggered will move t closer to be the head of the exter-
convergence property.                                                  nal queue eQ and eventually it will become the head of
   We start first by stating the main theorem about termina-           the queue and subsequently be processed eventually.
tion of responses for external triggers: it is always the case
that the system will come back to the READY TO DE−QUEUE                                                                          
                                                                                                                                 
state and iQ = ∅, i.e. the system is ready to de-queue an exter-
nal trigger (if any). This is stated as the following theorem.      10.1.1 Proof of convergence and anticipation

Theorem 2 (Termination of Internal System Events) Given             The responsiveness to external triggers presented in Theo-
that the internal events are convergent and the external events     rem 3 relies on Theorem 2, which in turn relies on the proof


                                                                                                                        123
538                                                                                                                        K. Morris et al.


of convergence for internal system events and anticipation for        eQ. Note that we do not attempt to prove the convergence
external events. These proof will need to be done for each            of any future events here. Instead, we assume that these
individual SCXML state chart as they do not hold a priori. We         future events will be proved to be convergent later. While
present a systematic approach to reason about the proof of            these future events raise new internal triggers (hence will
convergence and anticipation relying on lexicographic order           increase variant VdequeueI nter nalT rigger ed ), ultimately, they
as follow.                                                            will be converted to internal triggered and untriggered events.
   A variant in Event-B can be a natural number (bounded              These events will need to be proved to be convergent by
bellow by 0) or a finite set (bounded below by the empty              state machine-based variants which has higher priority than
set ∅). Moreover, for a set of events, the variants V1 , V2 , ...     VdequeueI nter nalT rigger ed . At the moment, we do not have the
are combined into a lexicographic variant, i.e. (V1 , V2 , ...)       notation of anticipation for a subset of a lexicographic vari-
with V1 has a higher priority than V2 , etc. An event is said         ant. This can be introduced into Event-B in the future.
to decrease this lexicographic variant if it either decreases            We now discuss the specific variants for the Drone exam-
V1 or if it keeps V1 the same and decreases V2 , so on and            ple based on the actual state chart as shown in Fig. 4. The
so forth. Lexicographic variants are supported in the latest          variants are for the internally triggered events and untrig-
Rodin (version 3.5).                                                  gered events. The lexicographic order of the variant use is
   Our generic approach to construct a lexicographic variant          to prove the convergence of the events depending (1) on the
is according to the following order and the rule for each             nested structure of the state chart and (2) on the order of
variant.                                                              the transitions with the same state chart. For example, the
                                                                      variant for proving the convergence for the transition from
1. Vexter nalT rigger = dt ∩ ExternalTrigger. This variant is         SHUTDOWN to OFF will have a higher priority than the one
   used to prove the convergence for any externally triggered         for the transition from TAKEOFF to FLY, and this variant sub-
   events (i.e. triggered event by some external trigger).            sequently has higher priority than the one for the transition
   These event remove the external trigger from dt and                from CLIMB to HOVER. Furthermore, the variant for proving
   hence ‘decrease’ dt to the empty set.                              the convergence for the transition from TAKEOFF to FLY has
2. Variants based on the state machine to prove the con-              higher priority than the one for the transition from FLY to
   vergence of internally triggered events and untriggered            DESCEND.
   events. This depends on the SCXML diagram, and we                     The translation of SCXML state chart into UML-B/Event-
   will illustrate this on the example later.                         B represents each state by a Boolean variable, TRUE if the
3. VdequeueI nter nalT rigger ed = length(iQ). This variant is        system in that state and FALSE otherwise. As a result, the
   used to prove the convergence of the dequeueInternal               variant for proving the convergence of an event going out
   Triggered event. Since this event removes the head of              of a state S can be {S, FALSE}: the transition ‘decreases’ the
   the iQ, it decreases the length of the iQ trivially, while         value of the variant from {TRUE, FALSE} to FALSE.
   other events might increase iQ, by raising new internal               Based on the above analysis, the variants that we used for
   triggers. However, these events should have been proved            proving the convergence of the internally triggered events
   to converge using higher-priority variants.                        and untriggered events in the Drone example are.
4. VnoT rigger edT ransitions Enabled = dt. This variant is used
   to prove the convergence of the noTriggeredTransitions              – {SHUTDOWN, FALSE}
   Enabled event. The event discards the trigger in dt and             – {TAKEOFF, FALSE}
   hence ‘decreases’ dt to the empty set.                              – {FLY, FALSE}
5. VnoU ntrigger edT ranstitions Enabled = {uc, TRUE}. This vari-      – {BATTERYOK, FALSE}
   ant is used to prove the convergence of the noUntriggered           – {CLIMB, FALSE}
   TransitionsEnabled event. The event changes uc flag                 – {CLIMB2, FALSE}
   from FALSE to TRUE and hence ‘decreases’ the variant
   from {FALSE, TRUE} to {TRUE}.
                                                                         This variant proof is available in the Rodin archive at
Note that except for the variant related to the internally            https://tinyurl.com/ISSE-Drone.
triggered events and untriggered events, i.e. (2), all other
variants, i.e. Vexter nalT rigger , VdequeueI nter nalT rigger ed ,   10.2 Correct responses to external triggers
VnoT rigger edT ransitions Enabled ,                          and
VnoU ntrigger edT ranstitions Enabled are generic according to the    In the previous section, we illustrate the reasoning about the
underlying run-to-completion semantics.                               responsiveness of the system to external triggers. However,
   The external events are anticipated according to the above         we also need to prove that the response to the external triggers
variants trivially since they only modify the external queue          is correct. In our conference paper [16], we illustrate the use


123
Formal verification and validation of run-to-completion…                                                                      539


of ProB model checker to reason about such a property. Here,           Coming back to our example, we first prove that the Event-
we show how we can prove such a property.                            B model satisfies the following important unless property.
   Once again, we assume that the system events are strongly
                                                                     Theorem 5 The drone system satisfies the following unless
fair as in Assumption 1. In general, our correct-response
                                                                     property.
properties will have the following form:

       G([external_trigger_event] ⇒ F{predicate}) ,                     BATTERYOK = TRUE ∧ charge > 20 ∧ decreaseCharge
                                                                                     ∈ content(eQ) ∧ oﬀ ∈ / dt ∧
where the predicate concerns variables v that the system                 (∀ i ∈ dom(eQ) . eQ(i) = oﬀ ⇒ (∃j ∈ dom(eQ) . eQ(j)
maintains, and may refer to old values old(v) that existed                           = decreaseCharge ∧ j < i))
when the external trigger occurred. The translator generates a                                  unless
separate ‘branch’ refinement for each LTLproperty to be ver-         BATTERYOK = TRUE ∧ charge > 20 ∧ dt = {decreaseCharge}
ified. In this special refinement, history variables are added to
record the value at the state when the external trigger occurs,      Proof (Sketch) The proof relies on Theorem 4, i.e. reasoning
of any variables that are referenced as ‘old’ values.                per event. The encoding of the proof obligations is available
    We illustrate the method with an example of a temporal           from the Rodin archive. We informally explain why this prop-
property that we expect to hold in the drone SCXMLsystem.            erty holds for different class of events below.
The liveness property that we wish to verify is that, after an
external trigger event decreaseCharge, the battery charge             – External events: The external events raise a new exter-
value should decrease in value, i.e.                                    nal trigger and append the new trigger to eQ. Given that



G ([ExternalTriggerEvent_decreaseCharge] ⇒ F{charge < old(charge)}) .


As discussed in [16], this above property is too strong and             decreaseCharge is already in eQ, even if the new trig-
does not hold for the SCXML drone model. We have to                     ger is oﬀ, this trigger cannot over take decreaseCharge
weaken the property to state that the expected behaviour is             in the queue, i.e. it is always behind decreaseCharge.
only achieved if the external trigger is raised at the right time,      These external events therefore maintain the left-hand
specified as {BATTERYOK=TRUE ∧ charge>20}, and there                    side of the unless property.
are no external conflict triggers, here oﬀ, in processing or          – De-queue external trigger: If the de-queued external trig-
that has been raised, i.e. oﬀ ∈
                              / dt ∪ content{eQ}. The prop-             ger is decreaseCharge, we will have dt = {decrease
erty can be formalised as follows                                       Charge}, and hence, we establish the right-hand side of

     G([ExternalTriggerEvent_decreaseCharge] ∧
{BATTERYOK=TRUE ∧ charge>20 ∧ oﬀ∈dt / ∧ oﬀ ∈/ content(eQ)}
            ⇒ F {charge < old(charge)}) .


In order to prove the above property, we first recall the defi-
nition of unless property [3,8].                                        the unless property. If it is not decreaseCharge (that is
                                                                        decreaseCharge is still in the queue), the de-queued trig-
Definition 3 (Unless Properties) An unless property of the              ger also cannot be oﬀ (as any oﬀ trigger in eQ has to be
following form                                                          behind a decreaseCharge trigger). As a result, the condi-
                                                                        tion that oﬀ is behind decreaseCharge in the remaining
                             P unless Q
                                                                        queue is maintained and oﬀ cannot be in dt after the event
means that if P holds, then it will hold continuously unless            execution.
Q hold.                                                               – Internal system events: For the internal systems events,
                                                                        we separate them into those that are outside the BATTERY
We restate the Unless rule (Theorem 1 in [8]) here.                     state and those that are inside of the BATTERY state.
Theorem 4 An event system satisfies the unless property P                 • For those that are outside the BATTERY state, they
unless Q, if for every event, if it starts in a state satisfying            maintain the left-hand side of the unless property
P ∧ ¬ Q, it will reach a state satisfying P ∨ Q.                            trivially (by leaving external queue unchanged and


                                                                                                                       123
540                                                                                                                          K. Morris et al.


        does not alter the relevant state, i.e. BATTERY or the    that can be translated to Event-B for verification. Invariant
        charge).                                                  properties about the expected coordination of states can be
      • For the self-transition which is triggered by decrease    added and are interpreted with additional allowance for the
        Charge inside the BATTERY state, the proof of the         reactions to take place. That is, they hold only after the reac-
        unless property is trivial, since we assume the nega-     tion has taken place. Such invariants prove automatically with
        tion of the right-hand side of the unless property,       the existing Rodin theorem provers. We also demonstrate a
        including that that decreaseCharge is not in dt. For      complementary process for verifying expected reactions to
        the transition from BATTERYOK to BATTERYLOW,              environmental triggers that uses the LTLmodel checker. We
        the proof of the unless property is also trivial, since   show how liveness can be verified to show that the ‘run’ con-
        we assume the left-hand side of the unless property,      verges to completion, i.e. transition loops and raised internal
        including that charge > 20.                               triggers do not introduce endless live-lock, but eventually
                                                                  terminate to allow the next external trigger to be consumed.
                                                             
                                                                 This convergence proof uses lexicographic variants which
                                                                  (at our suggestion) have recently been added to the Rodin
   Theorem 5 means that the system will continuously satisfy      toolset for Event-B. These verifications do not validate that
the following conditions:                                         the model behaviour is useful. For this, the SCXML model
                                                                  should be animated so that its behaviour can be observed by
 – in the BATTERYOK state ,                                       a domain expert. Elsewhere [19] we have developed a ‘Sce-
 – charge is more than 20 ,                                       nario Checker’ tool and methods for animating pre-defined
 – decreaseCharge is in the external queue eQ .                   domain specific scenarios at various levels of abstraction. We
 – oﬀ is not in dt .                                              demonstrate the use of this tool for automatically executing
 – if oﬀ is in the external queue eQ then it is behind a          the run to completion in order to validate that the expected
   decreaseCharge trigger .                                       behaviour is emerging and is useful.
                                                                     In future work, we intend to formalise the semantics of
unless it reaches a state satisfying the following conditions:    our extended SCXMLnotation in order to define its notion of
                                                                  refinement and correspondence to Event-B.
 – in the BATTERYOK state ,                                          All data supporting this study are openly available at
 – charge is more than 20 ,                                       https://tinyurl.com/ISSE-Drone.
 – decreaseCharge is in dt.
                                                                  Acknowledgements Sandia National Laboratories is a multimission
                                                                  laboratory managed and operated by National Technology & Engineer-
    Coming back to the proof for our correct-response
                                                                  ing Solutions of Sandia, LLC, a wholly owned subsidiary of Honeywell
property, assume that the system is at the right time             International Inc., for the US Department of Energy’s National Nuclear
and the [ExternalTriggerEvent_decreaseCharge] event hap-          Security Administration under contract DE-NA0003525.
pens. Notice that at that particular moment, the left-hand
                                                                  Open Access This article is licensed under a Creative Commons
side of the progress property in Theorem 5 is also satis-         Attribution 4.0 International License, which permits use, sharing, adap-
fied. According to Theorem 3, eventually, [dequeueExternal        tation, distribution and reproduction in any medium or format, as
Triggered.decreaseCharge] is fired (and dt = {decrease            long as you give appropriate credit to the original author(s) and the
Charge}), i.e. decreaseCharge is de-queued from the eQ into       source, provide a link to the Creative Commons licence, and indi-
                                                                  cate if changes were made. The images or other third party material
dt. And at that time, according to Theorem 5, we also have        in this article are included in the article’s Creative Commons licence,
BATTERYOK = TRUE and charge > 20. That ensures the trig-          unless indicated otherwise in a credit line to the material. If material
gered transition event for decreaseCharge is enabled (and         is not included in the article’s Creative Commons licence and your
it is the only internal event enabled) and will be eventually     intended use is not permitted by statutory regulation or exceeds the
                                                                  permitted use, you will need to obtain permission directly from the copy-
taken and hence decrease the charge’s value accordingly.          right holder. To view a copy of this licence, visit http://creativecomm
                                                                  ons.org/licenses/by/4.0/.

11 Conclusion

Reactive State charts are useful and widely used by engineers     References
for modelling the design of control systems. Event-B pro-
vides an effective language for formally verifying properties      1. Abrial JR (2010) Modeling in Event-B: system and software engi-
                                                                      neering. Cambridge University Press, Cambridge
via incremental refinements. However, it is not straightfor-
                                                                   2. Abrial JR, Butler M, Hallerstede S, Hoang T, Mehta F, Voisin
ward to apply the latter to the former. We have demonstrated a        L (2010) Rodin: an open toolset for modelling and reasoning in
technique for introducing refinement of reactive State charts         Event-B. Softw Tools Technol Transf 12(6):447–466


123
Formal verification and validation of run-to-completion…                                                                                    541


 3. Chandy KM, Misra J (1989) Parallel program design: a foundation.    15. Morris K, Snook C, Hoang TS, Armstrong R, Butler M (2019)
    Addison-Wesley, New York                                                Refinement of statecharts with run-to-completion semantics. In:
 4. Eclipse Foundation: Sirius project website. https://eclipse.org/        Artho C, Ölveczky PC (eds) Formal techniques for safety-critical
    sirius/overview.html (2016)                                             systems. Springer, Cham, pp 121–138
 5. Harel D (1987) Statecharts: a visual formalism for complex sys-     16. Morris K, Snook C, Hoang TS, Hulette G, Armstrong R, Butler,
    tems. Sci Comput Program 8(3):231–274. https://doi.org/10.1016/         M.: Formal verification of run-to-completion style statecharts using
    0167-6423(87)90035-9                                                    event-b. In: Muccini H (ed) Software architecture. ECSA 2020.
 6. Hoang, T.S.: An introduction to the Event-B modelling method. In:       Communications in computer and information science, vol 1269.
    Industrial deployment of system engineering methods. Springer, pp       Springer, Cham. https://doi.org/10.1007/978-3-030-59155-7_24
    211–236 (2013)                                                      17. Morris K, Snook C, Hoang TS, Hulette G, Armstrong R, Butler
 7. Hoang TS, Schneider S, Treharne H, Williams D (2016) Founda-            M (2020) Refinement and verification of responsive control sys-
    tions for using linear temporal logic in event-b refinement. Form       tems. In: Raschke A, Méry D, Houdek F (eds) Rigorous state-based
    Asp Comput. https://doi.org/10.1007/s00165-016-0376-0                   methods. Springer, Cham, pp 272–277
 8. Hudon S, Hoang TS, Ostroff JS (2016) The Unit-B method: refine-     18. Snook C, Butler M (2006) UML-B: Formal modeling and design
    ment guided by progress concerns. Softw Syst Model 15(4):1091–          aided by UML. ACM Trans Softw Eng Methodol 15(1):92–122.
    1116. https://doi.org/10.1007/s10270-015-0456-2                         https://doi.org/10.1145/1125808.1125811
 9. Kuppe MA, Lamport L, Ricketts D (2019) The TLA+ toolbox. In:        19. Snook C, Hoang TS, Dghaym D, Fathabadi AS, Butler M (2020)
    Monahan R, Prevosto V, Proença J (eds) Proceedings fifth work-          Domain-specific scenarios for refinement-based methods. (to be
    shop on formal integrated development environment, F-IDE@FM             published in) J Syst Archit
    2019, Porto, Portugal, 7th October 2019. EPTCS, vol 310, pp 50–     20. Syriani E, Sousa V, Lúcio L (2019) Structure and behavior preserv-
    62. https://doi.org/10.4204/EPTCS.310.6                                 ing statecharts refinements. Sci Comput Program 170(15):45–79.
10. Lamport L (1977) Proving the correctness of multiprocess pro-           https://doi.org/10.1016/j.scico.2018.10.005
    grams. IEEE Trans Softw Eng 2:125–143                               21. W3C (2015) State chart XML SCXML: state machine notation for
11. Lamport L (2002) Specifying systems, the TLA+ language and              control abstraction. http://www.w3.org/TR/scxml/
    tools for hardware and software engineers. Addison-Wesley, New
    York
12. Maraninchi, F.: The Argos language: graphical representation of
                                                                        Publisher’s Note Springer Nature remains neutral with regard to juris-
    automata and description of reactive systems. In: IEEE workshop
                                                                        dictional claims in published maps and institutional affiliations.
    on visual languages (1991)
13. MATLAB: 9.7.0.1190202 (R2019b). The MathWorks Inc., Natick,
    Massachusetts
14. Morris K, Snook C (2016) Reconciling SCXML statechart repre-
    sentations and Event-B lower level semantics. In: HCCV: workshop
    on high-consequence control verification. http://www.sandia.gov/
    hccv/_assets/documents/HCCV_2016_Morris.pdf




                                                                                                                                   123
