        Interface Generation and Compositional
             Verification in JavaPathfinder

                Dimitra Giannakopoulou and Corina S. Păsăreanu

              Carnegie Mellon University/NASA Ames Research Center,
                           Moﬀett Field, CA 94035, USA,
             {dimitra.giannakopoulou,corina.s.pasareanu}@nasa.gov



       Abstract. We present a novel algorithm for interface generation of soft-
       ware components. Given a component, our algorithm uses learning tech-
       niques to compute a permissive interface representing legal usage of the
       component. Unlike our previous work, this algorithm does not require
       knowledge about the component’s environment. Furthermore, in con-
       trast to other related approaches, our algorithm computes permissive in-
       terfaces even in the presence of non-determinism in the component. Our
       algorithm is implemented in the JavaPathﬁnder model checking frame-
       work for UML statechart components. We have also added support for
       automated assume-guarantee style compositional veriﬁcation in JavaP-
       athﬁnder, using component interfaces. We report on the application of
       the approach to interface generation for ﬂight-software components.


1    Introduction
Component interfaces are a central concept in component-based software engi-
neering. Although in current practice, interfaces typically describe the services
that a component provides and requires at a purely syntactic level, the need
has been identiﬁed for interfaces that document richer aspects of component
behavior. Such extended interfaces are usually not provided, which makes their
automatic generation an area of active research [1,10,5].
   This paper addresses the automatic generation of interfaces that describe le-
gal sequences of component calls. Such interfaces can serve as a documentation
aid to application programmers, but can also be used by veriﬁcation tools in
checking that components are invoked correctly within a system. In fact, com-
ponent interfaces are key for modular program analysis. They reduce the task of
verifying a system consisting of a component and a client, to the more tractable
task of verifying that the client satisﬁes the component’s interface.
   In previous work [6,16], we presented a framework based on learning, to per-
form automated assume-guarantee model checking of safety properties. To check
that a system consisting of components M1 and M2 satisﬁes a safety property
P , the framework automatically builds and reﬁnes assumptions A for one of the
components, for example M1 , to satisfy P , which it then tries to discharge on
the other component, M2 . Although assumptions A essentially constitute inter-
faces for component M1 , their generation relies on knowledge of component M2 .

M. Chechik and M. Wirsing (Eds.): FASE 2009, LNCS 5503, pp. 94–108, 2009.

c Springer-Verlag Berlin Heidelberg 2009
      Interface Generation and Compositional Veriﬁcation in JavaPathﬁnder       95

Moreover, the focus of the framework was to compute assumptions that would
allow to prove or disprove the property in the system, rather than assumptions
that precisely document the behavior of a component.
    The algorithm presented here for interface generation is also based on learn-
ing. However, in contrast to our work discussed above, it concentrates on the
creation of precise component interfaces, irrespective of the component clients.
By precise, we mean safe and permissive, as deﬁned in [10]. An interface is safe
if it accepts no illegal sequence of calls to the component. An interface is per-
missive if it includes all the legal sequences of calls to the component. Moreover,
in [8], we presented an algorithm for generating what we call weakest assumptions
in the context of Labeled Transition Systems. Weakest assumptions essentially
constitute precise component interfaces. The diﬀerence of the current algorithm
is that it is iterative, meaning that it can return partial results. Moreover, the
approach in [8] required an expensive determinization step that we avoid here by
dealing with the non-determinism in the component dynamically, during compo-
nent analysis, as guided by counter-examples. Furthermore, our past experience,
as well as other independent work [5], has indicated that the learning-based
approach is more eﬃcient for components that have relatively small interfaces.
    Henzinger et al. also target the generation of safe and permissive interfaces
in [10]. Unlike our framework, their work based on abstraction techniques and
it is only applicable to components that are visibly deterministic. The latter
requires that the behavior of the component be deterministic with respect to
the methods / actions in its communication interface (we will henceforth call the
communication interface of a component its alphabet in order to avoid confusion
with interface in this context). In the applications that we have been dealing
with, this requirement proved too restrictive. For example, we often need to
generate interfaces that focus on speciﬁc aspects of the component behavior, and
that therefore include only a subset of the component’s alphabet. Components
that are visibly deterministic with respect to their full alphabet, typically lose
this property when a subset of that alphabet is considered. Finally, Alur et
al. [1] also use learning to synthesize interface speciﬁcations for abstracted Java
components. However, their approach is heuristic-based, i.e., they do not always
obtain precise interfaces.
    We have implemented our algorithms in the JavaPathﬁnder (JPF) model
checking framework for UML statechart components [11]. We have also added
support for automated assume-guarantee style compositional veriﬁcation in JPF,
using component interfaces. JPF is an open source model checker for Java pro-
grams which, until now, provided no support for compositional veriﬁcation.
    The contributions of this work can be summarized as follows:

 1. A novel algorithm for automated generation of precise component interfaces,
    also applicable to components that are not visibly deterministic
 2. Implementation of our algorithm in the JPF open source model checker. In
    addition to interface generation, we have provided support for veriﬁcation
    of safety properties expressed as ﬁnite state automata as well as assume-
    guarantee reasoning in JPF, where assumptions and guarantees are both
96      D. Giannakopoulou and C.S. Păsăreanu

    expressed as ﬁnite-state automata. The implementation is freely available as
    JPF’s compositional veriﬁcation (cv) extension.
 3. Case studies in the context of NASA applications that demonstrate the use
    of our algorithm in practice.

Related Work. The work closest to ours was discussed above. Several other
approaches to automatic generation of component interfaces have been proposed
in the literature. For example, Whaley et al. [19] use a combination of static and
dynamic analyses to generate interfaces for Java components. Tkachuk et. al [18]
use static analysis to obtain component abstractions, used as environments dur-
ing modular analysis. Some approaches are based on extracting interfaces from
sample execution traces [3]. All these techniques generate approximate interfaces,
as opposed to our work that aims at producing precise interfaces that provide
correctness guarantees. Interface generation is related to compositional veriﬁca-
tion. In particular, assume-guarantee reasoning is a compositional approach that
uses assumptions when reasoning about components in isolation [12,17,2,7] and
component interfaces can be used as assumptions in this context. Finally, learn-
ing has also been used to generate models for formal veriﬁcation [14,9]; those
approaches do not address interface generation or compositional reasoning.


2    Background

We model software components using labeled ﬁnite state transition systems
(LTSs), where transitions are labeled with component actions.
   Let Act be the universal set of observable actions and let τ denote a local
action unobservable to a component’s environment. Let π denote a special error
state, which models safety violations in the associated transition system.

LTSs. An LTS M is a four-tuple Q, αM, δ, q0  where: Q is a ﬁnite non-empty
set of states; αM ⊆ Act is a set of observable actions called the alphabet of M ;
δ ⊆ Q × (αM ∪ {τ }) × Q is a transition relation; and q0 ∈ Q is the initial state.
   Let M = Q, αM, δ, q0  and M  = Q , αM  , δ  , q0 . M transits into M  with
                        a
action a, denoted M −→ M  , if (q0 , a, q0 ) ∈ δ, Q = Q , αM = αM  , and δ = δ  .
   An LTS M = Q, αM, δ, q0  is non-deterministic if it contains τ -transitions
or if there exists (q, a, q  ), (q, a, q  ) ∈ δ such that q  = q  . Otherwise, M is
deterministic.

Traces. A trace t of an LTS M is a ﬁnite sequence of observable actions that
label the transitions that M can perform starting at its initial state, ignoring
the τ -transitions. For Σ ⊆ Act, we use t ↑ Σ to denote the trace obtained
by removing from t all occurrences of actions a ∈/ Σ. For a set of traces T ,
T ↑ Σ = {t|∃t ∈ T.t ↑ Σ = t}.

Parallel Composition. Parallel composition “ ” is a commutative and associa-
tive operator: given LTSs M1 = Q1 , αM1 , δ 1 , q01  and M2 = Q2 , αM2 , δ 2 , q02 ,
       Interface Generation and Compositional Veriﬁcation in JavaPathﬁnder        97

M1 M2 is an LTS M = Q, αM, δ, q0 , where Q = Q1 × Q2 , q0 = (q01 , q02 ),
                                                            a
αM = αM1 ∪ αM2 , and δ is deﬁned as follows: (1) M1 M2 −→ M1 M2
       a                                a                    a
if M1 −→ M1 and a ∈ / αM2 , (2) M1 M2 −→ M1 M2 if M2 −→ M2 and
                                                     
                      a                a           a
a∈ / αM1 , (3) M1 M2 −→ M1 M2 if M1 −→ M1 , M2 −→ M2 , and a = τ .

3     Interface Generation
In this section we deﬁne safe and permissive interfaces for software components
and we describe our approach to synthesizing such interfaces automatically.

3.1   Safe and Permissive Interfaces
Let M be a software component. For simplicity of presentation, we will ﬁrst
assume that M includes an error state that expresses the undesired behavior of
M (for example, some assertion violations). Later in this section we will discuss
the more general case where the component property is given as a separate
(safety) automaton.
   Let Σ ⊆ αM denote the communication alphabet of component M , i.e., the
set of actions through which M communicates with its environment. Our goal
is to compute M ’s precise interface as a ﬁnite state automaton A over Σ. As
mentioned, we need to make sure that A is both safe and permissive, as deﬁned
formally below.
   Let us ﬁrst deﬁne the legal and illegal languages of component M . A word
t ∈ αM ∗ is illegal if it corresponds to some trace of M that leads to error state
π; otherwise, the word is legal. Then Llegal (M ) denotes the set of legal words of
M and Lillegal (M ) denotes the set of illegal words of M . Note that Llegal (M )
and Lillegal (M ) are complementary. Furthermore, note that, while illegal words
correspond to actual traces in the component, legal words may also represent
behavior that is never executed by the component (and hence could never lead
to violations).
Definition 1. A is a safe interface iﬀ Llegal (A) ∩ Lillegal (M ) ↑ Σ = ∅.
In other words, an interface is safe if it accepts no illegal words of M .
Definition 2. A is a permissive interface iﬀ Llegal (M ) ↑ Σ ⊆ Llegal (A).
In other words, an interface is permissive if it accepts all legal words of M .

3.2   Learning Interface Specifications with L*
Our approach for learning interface speciﬁcations is illustrated in Figure 1. We
use an oﬀ-the-shelf learning algorithm, L* [4], to iteratively compute interface
speciﬁcation A for M that is both safe and permissive. L* learns an unknown
language (over a given alphabet) and produces a minimal deterministic ﬁnite
state automaton that accepts it; the learning process is iterative and it uses a
teacher that provides answers to queries and counterexamples to conjectures (for
details on L* see [4]). In our framework, the problem of answering queries and
counterexamples is reduced to reachability problems, solved by a model checker.
98        D. Giannakopoulou and C.S. Păsăreanu


                                                                Teacher

           return true
                                            no
           query: trace w
                                π reachable in lts(w)M
           return false                     yes

           return t ↑ Σ
                                             yes and
                                             trace t
           conjecture: A
                             Oracle 1: π reachable in AM
                                             no (and A)
     L*

                                                                     no   interface
                             Oracle 2: (π,ok ) reachable in Aπ MC        specification A
                                     yes and
                                     trace t       backtrack

                               π reachable in lts(t ↑ Σ)M
           return t ↑ Σ                    no




                     Fig. 1. Learning interface speciﬁcations with L*


Queries L* is ﬁrst used to repeatedly query M to check whether or not, in the
context of strings w, M violates the property. This is equivalent with checking
if an error state π is reachable in lts(w) M . Here lts(w) denotes an LTS over
Σ that accepts string w (and its preﬁxes). The results of the queries are used
by L* to ﬁrst make a “conjecture”, i.e. it builds an automaton A that accepts
all the strings for the positive queries (the case error unreachable), and does not
accept the strings for the negative queries (the case error reachable).
   The conjectured automaton A is then checked to make sure it is both safe and
permissive. This is done with the help of a teacher that implements two oracles
as described below.

Oracle 1 checks if A is safe by checking whether π is reachable in A M . If it
is, then it means that A is un-safe. The resulting counterexample t, projected on
the interface alphabet Σ, is returned to L* to reﬁne its conjecture. If the error
state is un-reachable, then it means A is safe and we proceed to Oracle 2.

Oracle 2 checks if safe interface A is also permissive, i.e. we want to check
that Llegal (M ) ↑ Σ ⊆ Llegal (A). This amounts to making sure that there are no
words w ∈ Σ ∗ such that w ∈ Llegal (M ) ↑ Σ ∩ Lillegal (A). This is equivalent to
w ∈ Lillegal (A) and ∀t ∈ αM such that w = t ↑ Σ, t ∈ Llegal (M ).
   We search for such words using a special reachability procedure performed
on Aπ MC (see pseudo-code in Figure 2). Here Aπ denotes the completion
of A with an error state, i.e. we complete each state with outgoing transitions
to π, such that each state has outgoing transitions labeled with every action in
Σ. Similarly, MC denotes the completion of M with a special sink state. We
      Interface Generation and Compositional Veriﬁcation in JavaPathﬁnder         99

Oracle 2
input: safe interface A;
begin
(1) Model-check Aπ MC :
(2)      if (π, ok ) is reachable by trace t then
(3)          if π is not reachable in lts(t ↑ Σ)M then
(4)             return t ↑ Σ to L*;
(5)          else
(6)             backtrack;
(7) output: safe and permissive interface A;
end.

                                  Fig. 2. Oracle 2

need these constructions to reason about traces in Lillegal (A) and Llegal (M ),
respectively. Note that Lillegal (A) = Lillegal (Aπ ) and Llegal (M ) = Llegal (MC ).
Note also that for Oracle 2, since both Aπ and MC contain error states, we need
to distinguish between the two in Aπ MC (this was not necessary for queries
and Oracle 1).
   Given the above constructions, checking permissiveness reduces to checking
reachability of states of the form: (π, ok ), were π is an error state coming from Aπ
and ok denotes a non-error state in MC . If such a combined state is found, then
the trace t leading to it may indicate that A is not permissive, since w = t ↑ Σ
leads to an error state in Aπ but it is legal in MC (and hence in M ). However,
due to non-determinism in M (and hence in MC ), it may be the case that on
another path, t does lead to the error state. Even if this is not the case, there
may exist other traces t such that w = t ↑ Σ and t leads to an error in MC on
a diﬀerent path (see Figure 3).
   We check both these cases by performing a query on t ↑ Σ. Note that we do
not stop the state space exploration, but rather, we take trace t that is returned,
and we check if, in the context of t ↑ Σ, M violates its properties.
   If the query returns true, then it means the interface is not permissive, and
therefore t ↑ Σ is returned to L* for reﬁnement, and the learning process con-
tinues with more queries and eventually with a new conjecture.
   If the query returns false, then t does not correspond to a real counterexample.
Model checking therefore ignores this state; it backtracks, and then continues its
state space exploration. If no traces that satisfy the condition above exist, then
indeed the conjectured automaton is also the most permissive interface, and
therefore it is output to the user.
   We note that every query is stored in the L* memoized table, so the result of
the query on the same trace t ↑ Σ later (when A is the same) will be obtained
directly (and faster) from the table.

Properties as safety automata. Assume now that M does not have error
states, and we want to generate an interface speciﬁcation for ensuring a property
P , given as a (deterministic) safety automaton, encoding all the desired behaviors
of the component. Conversely, Pπ encodes all the un-desired behaviors of the
100    D. Giannakopoulou and C.S. Păsăreanu

              State space of Aπ  MC



                                    (sA    M
                                      0 , s0 )
                                                          t ↑ Σ = t ↑ Σ


                         Trace t                 Trace t
                                    ...

                                                 (π, π)
                        (π,sink )




            Fig. 3. Example for Oracle 2: dealing with non-determinism

component. The procedure described above will be exactly applicable to this
case as well, if we treat M ||Pπ as M above.

3.3   Correctness and Termination

We argue here the correctness and termination of our approach. To argue cor-
rectness, we ﬁrst show that Oracle 1 (and similarly the queries) guarantee a safe
interface while Oracle 2 guarantees a permissive interface; therefore, the teacher
implemented by our approach is correct.

Proposition 1. Oracle 1 returns A iﬀ Llegal (A) ∩ Lillegal (M ) ↑ Σ = ∅.

Proposition 2. Oracle 2 returns A iﬀ Llegal (M ) ↑ Σ ⊆ Llegal (A).

Due to lack of space we omit the proofs here; they proceed by contradiction and
follow the arguments given informally in the previous section.

Theorem 1. Given component ﬁnite state M (that may include error states),
the algorithm implemented by our approach terminates and it returns a safe and
permissive interface A.
Proof. Correctness follows from the two propositions above. Termination follows
from the correctness of L*, which is guaranteed that, if it keeps receiving coun-
terexamples, it will eventually terminate.

Discussion. As mentioned, in previous work we deﬁned an algorithm for build-
ing safe and permissive interfaces for ﬁnite state components [8]. That algorithm
involves the determinization of M (using the sub-set construction) that results
in an exponential cost in computation time, regardless of the size of the interface
speciﬁcation. However, for components with small interfaces, the interface au-
tomaton is expected to be much smaller than the component itself. We address
       Interface Generation and Compositional Veriﬁcation in JavaPathﬁnder   101

this problem by using L*, which builds incrementally automata with increasing
size, ﬁnishing with the minimal deterministic automaton representing a safe and
permissive interface.
   We also note here that the approach of Henzinger et al. [10] can only handle
components that are visibly deterministic, and therefore could not handle the
case illustrated in Figure 3. On the other hand, the approach of Alur et al. [1]
handles non-deterministic components, but it does not guarantee that the inter-
face is permissive, since it only uses heuristics to implement what it amounts
to Oracle 2 (called “superset query” in [1]). That work argues that the superset
query can not be implemented eﬃciently, since it involves the determinization
of component M . In our work we avoid an explicit determinization step of M .
Instead, our approach deals with the non-determinism in the component dynam-
ically (during model checking of the component) and only selectively (as guided
by counterexamples).


4     Compositional Verification in JPF

4.1   Java PathFinder

Java PathFinder (JPF) [11] is an open-source veriﬁcation framework developed
by the RSE group at NASA Ames. It has been started as an explicit state model
checker for Java byte-code. The focus of JPF is on ﬁnding bugs, such as con-
currency related bugs (deadlocks, races, missed signals etc.), runtime related
bugs (e.g. unhandled exceptions), etc. JPF can also check for violations of user-
speciﬁed assertions that encode application speciﬁc requirements. JPF uses a
variety of scalability enhancing mechanisms, such as user extensible state ab-
straction and matching, on-the-ﬂy partial order reduction, conﬁgurable search
strategies, and user deﬁnable heuristics (searches, choice generators).


4.2   JPF’s UML Statechart Extension

JPF has recently been extended with a statechart modeling and analysis ca-
pability that allows Java modeling of UML state machines [15]. Many UML
development systems can produce code from diagrams, but this code is usually
aimed at production systems, and is not suitable for software model checkers.
The approach taken in JPF (Figure 4(left)) is based on a speciﬁc translation
scheme from UML state charts into Java code that (a) is highly readable, (b)
shows close correspondence between diagram and program, (c) provides a 1:1
mapping between model and program states, and (d) imposes few restrictions
about aspects and actions that can be modeled.
   The JPF Statechart extension is specialized to handle the obtained Java mod-
els more eﬃciently than random Java code. These Java models can be run in
isolation, which corresponds to running them in the context of an external en-
vironment that may provide any input event at any stage (we will call this the
universal environment). Alternatively, a guidance script may be provided by the
102    D. Giannakopoulou and C.S. Păsăreanu




 Fig. 4. Example illustrating JPF’s UML extension (left) and JPF’s listener (right)

user, which represents the input event sequences that can be provided by the
external environment.
   We have used the JPF statechart extension to implement our interface syn-
thesis algorithms for components expressed in the JPF statechart framework.
Note that we do not attempt to perform compositional reasoning for UML stat-
echarts, which is a theoretical challenge that is beyond the scope of this work.
Rather, we use UML statecharts, as supported by JPF, to represent ﬁnite state
components with Labeled Transition System semantics. Therefore composition
of components comes down to LTS composition, as described in Section 2. The
interfaces that we generate are expressed as LTSs in the FSP notation [13].

4.3   Assume-Guarantee Reasoning in JPF
We have implemented assume-guarantee reasoning in JPF. As mentioned, com-
ponents are given as UML statecharts (instances of class CVState). Both proper-
ties and assumptions are represented as ﬁnite state automata (instances of class
gov.nasa.jpf.cv.SCSafetAutomaton).
   Model checking using assumptions and properties has been implemented using
JPF listeners (Figure 4(right)). A listener is essentially conﬁgured client code
that is notiﬁed when certain events occur while JPF performs its search. The no-
tiﬁed listener code can interact with JPF, e.g. a JPF “property” listener informs
JPF if the property holds via the return value of its check() method.
   Checking for both assumptions and properties is implemented with the
gov.nasa.jpf.cv.SCSafetyListener class. On creation, a SCSafetyListener
is associated with a ﬁnite state automaton P , which expresses the property or
assumption to be used during model checking. Note that the state of a listener
      Interface Generation and Compositional Veriﬁcation in JavaPathﬁnder      103

is not included in the state that JPF explores / stores during model checking.
However, the state of the automaton P needs to be part of the state space for
correct state-space exploration and backtracking. We perform this by adding a
static integer ﬁeld of class CVState for the cv extension, which is set from within
the listener.
   An SCSafetyListener listens for and reacts to the following events:

 – instructionExecuted: Signals to the listener that an instruction was ex-
   ecuted by JPF. The listener reacts by invoking method advance(...) on
   the automaton P . Advancing the automaton corresponds to making a state
   transition, if the instruction that was executed corresponds to an action in
   the alphabet of the automaton. If a transition on an alphabet action is un-
   deﬁned from the current state, this is an illegal transition (corresponds to a
   transition to the error state π). For properties, this means that an error has
   occurred, so the result returned by the listener’s check() method is false.
 – choiceGeneratorAdvanced: Signals that the next statechart action is se-
   lected for execution. The reaction of the listener is to check whether this
   action would make P transition to the error state if it were to be exe-
   cuted (this does not change the state of P since the transition is not really
   executed yet). Reaching an error state in an assumptions means that the
   current path explored is not a valid path under this assumption and must
   therefore be ignored. The listener forces JPF to backtrack (by executing
   vm.getSystemState().setIgnored(true)).
 – stateBacktracked: When the model checker backtracks, then the automa-
   ton must backtrack accordingly.

For example, in order to check some property described as an automaton pro-
vided in some ﬁle Foo, we need to include the following arguments when running
JPF’s main class gov.nasa.jpf.JPF:
   +jpf.listener=.cv.SCSafetyListener
   +safetyListener1.property= Foo
The ﬁrst argument informs JPF that an SCSafetyListener will need to be
notiﬁed of speciﬁc events, and the second one provides details for the listener,
i.e., its unique id is “1”, it is of type property (as opposed to assumption), and
the automaton associated with it is provided in ﬁle Foo (this may also include
the full path to Foo).


4.4   Interface Generation and Discharge

The interface generation in JPF is implemented in the main class
gov.nasa.jpf.tools.cv.ScRunCV. The user can customize the generation via
the following arguments:
   +assumption.alphabet=<actions> deﬁnes the interface alphabet;
   +assumption.outputFile=<file name> deﬁnes a ﬁle in which the generated
interface is output.
104      D. Giannakopoulou and C.S. Păsăreanu

public boolean query(Vector sequence) throws SETException {

    Boolean recalled = memoized_.getResult(sequence);
    if (recalled != null) {
        return (!recalled.booleanValue());
    } else {
        // play the query as an assumption
        System.out.println("\n New query: " + sequence);
        SCSafetyListener assumption = new SCSafetyListener(
            new SCSafetyAutomaton
                    (true, sequence, alphabet_, "Query", module1_));

        JPF jpf = createJPFInstance(assumption, property, module1_);
        jpf.run();
        boolean violating = jpf.foundErrors();
        memoized_.setResult(sequence, violating);
        return (!violating);
    }
}

                   Fig. 5. Answering queries in SCModularTeacher

   This allows for a generated interface to be used for subsequent reasoning, ei-
ther as an assumption, or as a property. The format currently used for expressing
the interface is the FSP language.
   The main method of gov.nasa.jpf.tools.cv.ScRunCV creates an instance of
class gov.nasa.jpf.tools.cv.SETLearner to carry out the learning of the in-
terface; an associated instance of gov.nasa.jpf.tools.cv.SCModularTeacher
serves as the teacher. Our learning algorithm implementation uses JPF to per-
form the model checking steps described in Section 3. JPF model checks in-
dividual components in the context of the universal environment. Listeners are
added as necessary to reﬂect the work of the Teacher, which consists of answering
Queries, and implementing Oracle 1 and Oracle 2 in order to answer conjectures,
as described in more detail below.

Queries and Oracle 1. Queries and Oracle 1 are performed in a similar fash-
ion because they are concerned with checking whether error states are reachable
in the component, in the context of a particular sequence (for queries) or ﬁnite
state automaton (for Oracle1). As illustrated in Figure 5, to respond to a query,
a listener instance assumption is created with an associated automaton that re-
ﬂects the particular sequence that is being queried. JPF is then invoked, together
with the assumption listener. If JPF returns errors, the answer to the query is
false, otherwise the answer is true. Oracle 1 works in a similar fashion, with
the diﬀerence that it also returns a counterexample.

Oracle 2. Oracle 2 checks for permissiveness of a computed interface. It needs
to work on the completed component, as described in Section 3. This is a man-
ual step that we intend to automate in the future. It similarly invokes JPF,
      Interface Generation and Compositional Veriﬁcation in JavaPathﬁnder        105

but performs the search in the context of a specialized type of listener, the
gov.nasa.jpf.cv.SCConformanceListener. Its aim is to detect the reachabil-
ity of a (π, ok) combination of states in the interface and component where the
interface is in an error state, while the component is in an non-error state.
   The gov.nasa.jpf.cv.SCConformanceListener listens for and reacts to the
following events:

 – executeInstruction: When the instruction about to be executed by JPF
   is an assertion violation, then it means that the component has entered an
   error state. Since such states are not targeted by the listener, it performs
   ti.skipInstruction();
   vm.getSystemState().setIgnored(true);.
   The ﬁrst command ensures that the exception is not processed by JPF, for
   eﬃciency. The second asks JPF to backtrack since this path cannot lead to
   the targeted combination of states.
 – instructionExecuted: Similar to gov.nasa.jpf.cv.SCSafetyListener.
   When the automaton associated with the listener moves to an error state,
   the result returned by the check() method of the listener is set to false,
   since the component is in a legal state (illegal states are never reached since
   the listener advises JPF to backtrack when it reacts to executeInstruction
   events), while the interface is in an error state.
 – stateBacktracked: Similar to gov.nasa.jpf.cv.SCSafetyListener.

As described in Section 3, when an (π, ok) state is detected by the model checker,
the counterexample leading to this state is queried, and if it is not a real coun-
terexample, the model checker will backtrack. Since a query involved calling the
model checker, this would involve nested model checker calls. To avoid such nest-
ing, our implementation exploits a memoized table that is used by the learner to
store results of previous queries. Oracle 2 checks for the reachability of (π, ok)
states in a loop. Whenever a counterexample is obtained by the model checker,
then OraclE2 invokes a query on it. Each query stores its result in the memoized
table.
   Whenever a real counterexample is obtained, Oracle 2 exits the loop and re-
ports the result to the learner. When a counterexample is spurious, then another
iteration of the loop is entered. In this iteration, we wish to ensure that the model
checker will not report the same spurious counterexample. We achieve this as
follows. When a gov.nasa.jpf.cv.SCSafetyAutomaton is asked to advance in
the context of a gov.nasa.jpf.cv.SCConformanceListener, if the automaton
reaches an error state, it will get the path to this state from JPF. It will then
check the memoized table to see if there is a result for the corresponding se-
quence stored there. If there is, and the result is true, then it means that this is
a spurious counterexample, and it notiﬁes JPF to backtrack. Therefore, we have
implemented the nested model checking calls by consecutive calls to the model
checker, where the information of spurious counterexamples is shared through
the memoized table.
106     D. Giannakopoulou and C.S. Păsăreanu




      Fig. 6. Model of the Ascent and Earth Orbit ﬂight phases of a spacecraft


Interface discharge. For compositional reasoning, one needs to also discharge
the generated interface on the component environment. This can be performed
by model checking the environment component in the presence of a
gov.nasa.jpf.cv.SCSafetyListener using the interface as a property.


5     Experience

In order to evaluate our implementation, we used a statechart model of the
Ascent and EarthOrbit ﬂight phases of a space-craft (see Figure 6). The JAVA
model is available with the JPF distribution under examples/jpfESAS. The
UML statechart diagrams for the model are included in examples/jpfESAS.doc.
  The model was created and used to demonstrate the features of the JPF
UML statechart extension to our NASA mission customers. Several properties
were analyzed on the model, and JPF returned violations for some of these
properties. When the counterexamples obtained were analyzed, it was clear that
some of the violations were spurious. The violations were related to the following
properties:

 – An event lsamRendezvous, which represents a docking maneuver with an-
   other spacecraft, fails if the LAS (launch abort system) is still attached to
   the spacecraft.
 – Event tliBurn (trans-lunar interface burn takes spacecraft out of the earth
   orbit and gets it into transition to the moon) can only be invoked if EDS
   (Earth Departure Stage) rocket is available.

   These violations were due to the fact that the universal environment was too
general. The models had been created under the assumption that the use of the
model respects some implicit ﬂight rules. We decided to use our interface genera-
tion techniques to formalize the ﬂight rules. More speciﬁcally, for each property,
      Interface Generation and Compositional Veriﬁcation in JavaPathﬁnder                           107

               Interface 1:                               Interface 2:
                      lasJetisson                                 lsamRendezvous
                                         lasJetisson                               tliBurn
                 0                  1    lsamRendezvous     0                  1   lsamRendezvous




                              Fig. 7. Generated interface speciﬁcations

we generated a safe and permissive interface to eliminate its corresponding vio-
lations. To do this, we added a listener that eliminated all assertion violations
that were not related to the targeted property, through the following arguments:
  +jpf.listener=.tools.ChoiceTracker:.cv.AssertionFilteringListener
  +assertionFilter.include=<method name>
These arguments specify that all assertion violations that occur outside the
particular <method name> will be ignored.
   The generated interface speciﬁcations are illustrated in Figure 7. The ﬁrst one
expresses the fact that the lsamRendezvous maneuvers cannot start before the
las module of the spacecraft has jettisoned. According to the second one, it does
not make sense to perform tliBurn prior to performing lsamRendezvous. These
interfaces were inspected by the developer of the model that conﬁrmed that they
encode actual ﬂight rules. Interface generation can therefore be used by develop-
ers to help them in the expression of the assumptions that their models encode.
We note that other examples, including the input-output example from [6], are
available with the JPF distribution.


6   Conclusions
We have proposed an algorithm for automatically synthesizing behavioral inter-
face speciﬁcations for ﬁnite state software components. Our algorithm is the ﬁrst
iterative approach that is guaranteed to compute interfaces that are both safe
and permissive, even in the presence of non-determinism in the visible behav-
ior of a component. We have implemented our approach in the JavaPathﬁnder
model checking framework for UML statechart components, and have obtained
promising results from its application to several systems. The source code for
the implementation and the examples is available through JPF’s distribution.
   In the future, we plan to investigate interface generation for methods with pa-
rameters. We have made some initial experiments using JPF’s symbolic execution
extension to generate values for parameters with inﬁnite domains, and used these
values to deﬁne ﬁnite interface alphabets related to their corresponding methods.
We wish to pursue this direction further, and also plan to extend our results to
generic Java components. For components that may be inﬁnite-state, we will com-
bine our approach with techniques such as predicate abstraction (similar to [1]).
Finally, we plan to perform extensive evaluations of our approach.


Acknowledgements
We thank Peter Mehlitz and Suzette Person for helping with the implementation.
108     D. Giannakopoulou and C.S. Păsăreanu

References
 1. Alur, R., Cerny, P., Madhusudan, P., Nam, W.: Synthesis of interface speciﬁcations
    for Java classes. In: Proceedings of POPL 2005, pp. 98–109 (2005)
 2. Alur, R., Henzinger, T., Mang, F., Qadeer, S., Rajamani, S., Tasiran, S.: MOCHA:
    Modularity in Model Checking. In: Vardi, M.Y. (ed.) CAV 1998. LNCS, vol. 1427,
    pp. 521–525. Springer, Heidelberg (1998)
 3. Ammons, G., Bodik, R., Larus, J.R.: Mining speciﬁcations. In: Proceedings of ACM
    POPL 2002, pp. 4–16 (2002)
 4. Angluin, D.: Learning regular sets from queries and counterexamples. Information
    and Computation 75(2), 87–106 (1987)
 5. Beyer, D., Henzinger, T.A., Singh, V.: Algorithms for Interface Synthesis. In:
    Damm, W., Hermanns, H. (eds.) CAV 2007. LNCS, vol. 4590, pp. 4–19. Springer,
    Heidelberg (2007)
 6. Cobleigh, J.M., Giannakopoulou, D., Pasareanu, C.S.: Learning Assumptions for
    Compositional Veriﬁcation. In: Garavel, H., Hatcliﬀ, J. (eds.) TACAS 2003. LNCS,
    vol. 2619, pp. 331–346. Springer, Heidelberg (2003)
 7. Flanagan, C., Freund, S.N., Qadeer, S.: Thread-Modular Veriﬁcation for Shared-
    Memory Programs. In: Le Métayer, D. (ed.) ESOP 2002. LNCS, vol. 2305, pp.
    262–277. Springer, Heidelberg (2002)
 8. Giannakopoulou, D., Pasareanu, C.S., Barringer, H.: Assumption Generation for
    Software Component Veriﬁcation. In: Proceedings of ASE 2002, pp. 3–12. IEEE
    Computer Society, Los Alamitos (2002)
 9. Groce, A., Peled, D., Yannakakis, M.: Adaptive Model Checking. In: Katoen, J.-
    P., Stevens, P. (eds.) TACAS 2002. LNCS, vol. 2280, p. 357. Springer, Heidelberg
    (2002)
10. Henzinger, T.A., Jhala, R., Majumdar, R.: Permissive Interfaces. In: Proceedings
    of ESEC/SIGSOFT FSE 2005, pp. 31–40 (2005)
11. Java PathFinder, http://javapathfinder.sourceforge.net
12. Jones, C.B.: Speciﬁcation and Design of (Parallel) Programs. In: Information Pro-
    cessing 1983: Proceedings of the IFIP 9th World Congress, IFIP, pp. 321–332.
    North Holland, Amsterdam (1983)
13. Magee, J., Kramer, J.: Concurrency: State Models & Java Programs. John Wiley
    & Sons, Chichester (1999)
14. Margaria, T., Raﬀelt, H., Steﬀen, B., Leucker, M.: The LearnLib in FMICS-jETI.
    In: Proceedings of ICECCS 2007 (2007)
15. Mehlitz, P.: Trust Your Model - Verifying Aerospace System Models with Java
    Pathﬁnder. In: IEEE/Aero (2008)
16. Pasareanu, C.S., Giannakopoulou, D., Gheorghiu Bobaru, M., Cobleigh, J.M., Bar-
    ringer, H.: Learning to Divide-and-Conquer: Applying the L* Algorithm to Auto-
    mate Assume-Guarantee Reasoning. In: FMSD (January 2008)
17. Pnueli, A.: In Transition from Global to Modular Temporal Reasoning about Pro-
    grams. In: Logic and Models of Concurrent Systems, vol. 13, pp. 123–144 (1984)
18. Tkachuk, O., Dwyer, M.B.: Adapting side eﬀects analysis for modular program
    model checking. In: Johansson, T. (ed.) FSE 2003. LNCS, vol. 2887, pp. 188–197.
    Springer, Heidelberg (2003)
19. Whaley, J., Martin, M.C., Lam, M.S.: Automatic extraction of object-oriented
    component interfaces. In: Proceedings of ISSTA 2002, pp. 218–228 (2002)
