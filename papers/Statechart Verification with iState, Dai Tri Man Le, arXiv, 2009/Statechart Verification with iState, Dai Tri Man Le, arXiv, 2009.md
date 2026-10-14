                                                         Statechart Verification with iState

                                                                              Dai Tri Man Lê

                                                                     Department of Computer Science,
                                                                          University of Toronto,
                                                                      Toronto, ON, M5S 3G4 Canada
arXiv:0909.1361v1 [cs.SE] 8 Sep 2009




                                                                           ledt@cs.toronto.edu


                                              Abstract. This paper is the long version of the extended abstract with the same
                                              name [9]. We describe in detail the algorithm to generate verification conditions
                                              from statechart structures implemented in the iState tool. This approach also sug-
                                              gests us a novel method to define a version of predicate semantics for statecharts
                                              analogous to how we assign predicate semantics to programming languages.


                                       1 Introduction
                                       The statechart formalism, proposed by Harel [7] as an extension of conventional fi-
                                       nite state machines, is a visual language for specifying reactive systems. It addresses
                                       the state explosion problem of state transition diagrams when modeling systems with
                                       parallel threads of control by introducing the concepts of hierarchy, concurrency, and
                                       communication.
                                           The iState tool translates statecharts into various programming languages, currently
                                       the Abstract Machine Notation (AMN) of the B method [1], Pascal, and Java. The
                                       translation is based on a definition of statecharts in terms of an extension of Dijkstra’s
                                       guarded commands [15,16]. This work demonstrates a novel statechart verification ap-
                                       proach using state invariants that has been added to iState.

                                       2 Invariants
                                       Statecharts allow executable specifications to be derived from user requirements. We
                                       propose to supplement a statechart specification by invariants. These are attached to
                                       states and specify what has to hold in a state configuration. Invariants are also derived
                                       from the requirements. They are not meant for execution, but they allow the statechart
                                       specification to be cross-checked. By themselves, statecharts do not lead to opportuni-
                                       ties for consistency checks beyond well-formedness; invariants address this limitation
                                       and give a way of documenting the “purpose” of states.
                                           Formally, invariants are predicates over global variables, like x in the example be-
                                       low, and states (state tests):
                                                                                                         U (x > 6)
                                                   R (x > 1)                                             A ✲ M (x < 111)
                                                    ✲ S (x ≤ 100)           E [x 6= 5] / x := x + 10 ✲
                                                                                                         B ✲ N (x 6= 15)
2

The definition of statecharts in [15,16] translates states into variables and events into
(nondeterministic) operations, in which use of the independent (parallel) composition
of statements is made; the parallel composition operator is essential for translating
events with transitions in concurrent states. Using AMN, the states of the previous stat-
echart are translated to variables root ∈ {R, U}, r ∈ {S}, a ∈ {M} and b ∈ {N} and the
event E is translated to:

                 E , if root = R then
                         if r = S then
                            if x 6= 5 then
                               x := x + 10 k root := U k a := M k b := N
                             end
                         end
                       end

Let si: State → Condition be a function that assigns to each state the invariant specified
by the designer, or true if none is specified, together with a test for being in that state.
For example:

                                  si(S) = (r = S ∧ x ≤ 100)
                                 si(U) = (root = U ∧ x > 6)

By the hierarchical structure of statechart, being in a state also means being in all of its
ancestor states, in exactly one of its child states if the state is an XOR state, and in all of
its child states if the state is an AND state. Hence, we have to compose state invariants
together to create the accumulated invariant ai(s) of state s. For example:

         ai(S) = (root = R ∧ x > 1) ∧ (r = S ∧ x ≤ 100)
        ai(U) = (root = U ∧ x > 6) ∧ ((a = M ∧ x < 111) ∧ (b = N ∧ x 6= 15))

Formally, let Basic, XOR, AND be disjoint subsets of the set State. The accumulated
invariant ai: State → Condition is defined with the help of the child invariant ci: State
→ Condition as follows:
                          
                          si(s) ∧ V ci[children[{s}]] if s ∈ XOR
                                   N
                          
                   ci(s) , si(s) ∧ ci[children[{s}]] if s ∈ AND
                          
                            si(s)                         if s ∈ Basic
                          

                                 si[parent+ [{s}]] ∧ ci(s)
                             ^
                   ai(s) ,

Here, children[{s}] denotes the set of all child states of a state s and parent+ [{s}] de-
notes the set of all ancestor states of s, where parent is the inverse of the child relation,
parent = child−1 [15,16]. The operator
                                            N
                                                stands for xor. The definition reflects the
meaning of XOR and AND states.
                                                                                       3

3 Event Codes and Verification Tuples
For each transition E[guard]/action from state S to T, where action is a statement that
may read and write to global variables, may include state tests, and may broadcast other
events, a verification condition is generated:

                            {ai(S) ∧ guard} action {ai(T)}

In the case of broadcasting in action, the broadcast is replaced by a call to the corre-
sponding operation. In the case of transitions in concurrent states on the same event E,
a combined transition is considered. In the example, the verification condition for event
E is:

            {(root = R ∧ x > 1) ∧ (r = S ∧ x ≤ 100) ∧ x 6= 5}
             x := x + 10 k root := U k a := M k b := N
            {(root = U ∧ x > 6) ∧ ((a = M ∧ x < 111) ∧ (b = N ∧ x 6= 15))}

Hence, our goal is to automate the generating verification condition process. However,
before doing so we need to have data structures to store and manipulate the verification
conditions efficiently.
   Using the algorithm discussed in [15,16], we map each statechart data structure into
nondeterministic operations which is represented using an abstract syntax tree (AST).
The AST of intermediate language is stored using the data type EventCode

                         EventCode , Identifier →
                                                7 Statement

where S → 7 T denotes the set of partial function from S to T.
    Let P(S) and seq(S) denote the types power set of S and finite sequences of S re-
spectively. Also let S ↔ T denote the set of relation from S to T. Each Statement is then
defined as a recursive data type

                   Statement , StateAssign State
                               | Assignment Identifier Expression
                               | Bcast Identifier
                               | Guard Condition ↔ Statement
                               | Par seq(Statement)
                               | Seq seq(Statement)
                               | Skip

where:
 – StateAssign State: denotes the state assignment node.
 – Assignment Identifier Expression: denotes assignment node and the left hand side
   of the assignment is an identifier and the right hand side is an expression.
 – Bcast Identifier: denotes a broadcasting of an event whose name is represented
   using an identifier.
4

    – Guard Condition ↔ Statement: denotes an alternative choice where each choice
      is guarded using a condition. Notice that we use Condition ↔ Statement to empha-
      size the possible non-determinism. When several conditions are true at the same
      time, a choice is made non-deterministically.
    – Par seq(Statement): denotes the parallel composition of a sequence of statements.
      Due to the commutativity of parallel composition, we might use a set of statements
      instead of sequence. However, we decide to use sequence here only for the sake of
      determinism.
    – Seq seq(Statement): denotes the sequential composition of a sequence of state-
      ments.
    – Skip denotes the skip statement.
    The type Condition can either be a state test or a predicate, which is defined as
following
                           Condition , StateTest State
                                     | Predicate Expression
Notice that using a functional language like syntax to define Statement and Condition
allows us to employ pattern-matching on these data types when presenting our algo-
rithms.
    We then generate verification conditions from EventCode data structure. This will
be done by analyzing the structure of EventCode to generate local verification condi-
tions and composing them together suitably to produce the final verification conditions.
We treat all of these verification conditions uniformly using the notion of verification
tuple, which we think to be a more suitable representation of Hoare’s triple for our
verification purpose. The verification tuple type is define as following:
                  VTuple , P(State) × Expression × Statement × P(State)
where for each (s, g, a, t) ∈ VTuple we have:
    – s denotes the set of source states of the transition,
    – g denotes the guard condition of the transition,
    – a denotes the statement which changes the states of global variables (including state
      variables),
    – t denotes the set of target states of the transition.
Notice that each (s, g, a, t) ∈ VTuple is converted into the following verification condi-
tion                              ^               ^
                                 { ai[s] ∧ g} a { ai[t]}
which is verified as a normal Hoare’s triple. However, using sets of source of target
states gives a more optimal way of composing verification conditions together. This also
helps us avoiding redundancy when generating accumulating invariants due to states
having common ancestors. In other words, we use the following more efficient way
to calculate the acumulated invariant of a state set. Let the state set closure function
cl : P(State) → P(State) be defined as following

                                        {parent∗[{s}] | s ∈ ss}
                                        [
                             cl(ss) ,
                                                                                             5

where R∗ denotes the reflexive transitive closure of the relation R. We define the set
accumulated invariant function sai : P(State) → Condition as follows:
                      
                      si(s) if s ∈ Basic
                      
           si(s, ss) , si(s) if s ∈ AND ∪ XOR ∧ children(s) ∈ cl(ss)
                      
                        ci(s) otherwise
                      
                         ^
             sai(ss) ,      {si(s, ss) | s ∈ cl(ss)}

   For convenience, we let ast : String → Expression ∪ Statement denote the mapping
from a String to its AST. Hence, the verification condition discussed in our example
previously can be expresses using the following VTuple:

 ({R, S}, ast(“x 6= 5”), ast(“x := x + 10 k root := U k a := M k b := N”), {U, M, N})


4 Invariant Verification Algorithm

Before presenting the algorithm for generating verification tuples, we need several aux-
iliary functions. We divide Condition into StateTest and Predicate. The state test con-
dition StateTest are generated by EventCode generators using the algorithm in [15,16].
Hence, we let Predicate denote the transition guards supplied by users. To distinct these
two cases, we use the following function

   c2tuple : Condition → VTuple
                                           /
   c2tuple StateTest s = ({s}, true, Skip, 0)
                           / e, Skip, 0)
   c2tuple Predicate e = (0,          /

Considering the following example where you have:

                    if c1 then s1 else s2 end k if c2 then s3 else s4 end

For simplicity, we suppose these two statements are simply user statements without
state test or state assignment. Then the statement if c1 then s1 else s2 end corresponds
to the verification tuple set

                                   / c1 , s1 , 0),
                                 {(0,          / (0,
                                                   / ¬c1 , s2 , 0)}
                                                                /

and the statement if c2 then s3 else s4 end corresponds to the set

                                   / c2 , s3 , 0),
                                 {(0,          / (0,
                                                   / ¬c2 , s4 , 0)}
                                                                /

Since these two if statements are composed in parallel, we the resulted parallel product
verification tuple set for the whole statement is:

             / c1 ∧ c2 , s1 ks3 , 0),
           {(0,                   / (0,/ ¬c1 ∧ c2 , s2 ks3 , 0),
                                                             / (0,
                                                                 / ¬c1 ∧ c2 , s2 ks3 , 0),
                                                                                       /
                                      / ¬c1 ∧ ¬c2 , s2 ks4 , 0)}
                                    (0,                       /
6

The more general case including state tests are tackled using the following functions:

    parProd : seq(P(VTuple)) → P(VTuple)
    parProd [] = 0/
    parProd [s] = s
    parProd [s1 , . . . , sn ] = {concat1([t1, . . . , tn ]) | (t1 , . . . , tn ) ∈ s1 × . . . × sn }

    concat1 : seq(VTuple) → VTuple
    concat1 [] = (0,/ true, Skip, 0)    /
    concat1 [(si , gi , ai , ti ) | i = 1..n] = ( ni=1 si , ni=1 gi , Par [a1 , . . . , an ], ni=1 ti )
                                                 S         V                                 S


This function parProd is used very often in our implementation and it helps to simplify
the implementation substantially.
    Similar to the case of parallel composition is the case sequential composition. For
example, an event code

                      if c1 then s1 else s2 end ; if c2 then s3 else s4 end

will be translated into the following verification tuple set
               / c1 ∧ c2 , s1 ; s3 , 0),
             {(0,                    / (0,/ ¬c1 ∧ c2 , s2 ; s3 , 0),
                                                                 / (0,
                                                                     / ¬c1 ∧ c2 , s2 ; s3 , 0),
                                                                                            /
                                         / ¬c1 ∧ ¬c2 , s2 ; s4 , 0)}
                                       (0,                        /

Since the statements must be composed sequentially, the functions are implemented as
following.
    seqProd : seq(P(VTuple)) → P(VTuple)
    seqProd [] = 0/
    seqProd [s] = s
    seqProd [s1 , . . . , sn ] = {concat2([t1, . . . , tn ]) | (t1 , . . . , tn ) ∈ s1 × . . . × sn }

    concat2 : seq(VTuple) → VTuple
    concat2 [] = (0,/ true, Skip, 0)    /
    concat2 [(si , gi , ai , ti ) | i = 1..n] = ( ni=1 si , ni=1 gi , Seq [a1 , . . . , an ], ni=1 ti )
                                                 S         V                                 S


    We then define a function s2tuples which maps each statement node to a set of
verification tuples. Using pattern-matching, the function s2tuples can be defined as fol-
lowing:

    s2tuples : Statement → P(VTuple)
    s2tuples StateAssign s = {(0,/ rue, StateAssign s, {s})}
    s2tuples Assignment i e = {(0,/ true, Assignment i e, 0)}
                                                          /
                          / true, Bcast i, 0)}
    s2tuples Bcast i = {(0,                /
    s2tuples Guard r = {parProd([{c2tuple(c)}, s2tuples(s)]) | (c, s) ∈ r}
                         S

    s2tuples Par ss = parProd([s2tuples(s) | s ← ss])
    s2tuples Seq ss = seqProd([s2tuples(s) | s ← ss])
                      / true, Skip, 0)
    s2tuples Skip = (0,             /
                                                                                             7

   Hence, we can construct a global verification tuple map for all events using the fol-
lowing function:

    vtupleMap : EventCode → (Identifier → P(VTuple))
    vtupleMap ec = s2tuples ◦ ec

where the operation ◦ denotes the usual function composition, i.e, f ◦ g(x) , f (g(x)).
    Since each verification tuple (s, g, s, t) ∈ ran(vtupleMap), the action s might still
                                                S

contain event broadcasting. We deal with these event broadcasts similarly to the case of
parallel composition of event codes. We first apply topological sorting algorithm [10]
on vtupleMap(ec) to obtain a sequence

                tss = [(e1 , s1 ), . . . , (en , sn )] ∈ seq(Identifier × P(VTuple))

such that for each (ei , si ), the verification tuple set si contains the actions that board-
cast only the events in the set {e1 , . . . , ei−1 }. We can always obtain such a list with the
assumption that we don’t allow circular broadcasting [3]. We next define a function to
collect and filter the boardcasts from the action of a verification tuple as following:

    collectBcast : Statement → P(Identifier)
    collectBcast Bcast i = {i}
    collectBcast Guard {(ci , si ) | i S  = 1..n} = ni=1 collectBcast(si )
                                                     S
                                           n
    collectBcast Par [s1 , . . . , sn ] = Si=1 collectBcast(si )
    collectBcast Seq [s1 , . . . , sn ] = ni=1 collectBcast(si )
    collectBcast s = 0/

    filterBcast : Statement → Statement
    filterBcast Bcast i = Skip
    filterBcast Guard r = Guard {(c, s) | (c, s) ∈ r ∧ ¬isBcast(s)}
    filterBcast Par ss = Par [s | s ← ss ∧ ¬isBcast(s)]
    filterBcast Seq ss = Seq [s | s ← ss ∧ ¬isBcast(s)]
    filterBcast s = s

    isBcast : Statement → Boolean
    isBcast Bcast = true
    isBcast     = false

    In our real implementation, we filter and collect broadcasted events at the same time
for the sake of efficiency. We let a denote the sequence concatenation operator. Then
the process of translating verification tuples with broadcasting to ones without board-
casting is implemented as the following functions:

    vtupleNoBcast : (VTuple × seq(Identifier × P(VTuple))) → P(VTuple)
    vtupleNoBcast ((s, g, a, t) , tspre) =
                               / then
           if (collectBcast = 0)
               parProd([{(s, g, filterBcast(a), t)}]a
8

                                [si | (ei , si ) ← tspre ∧ ei ∈ collectBcast(a)])
            else
               {(s, g, a, t)}
            end

The function vtupleNoBcast takes a pair of verification tuples and tspre as inputs. The
argument tspre represents the set of prefix of tss where all boardcasting are already ex-
panded. Since we tss is already topologically sorted according to the dependencies of
boardcasting, the action a only broadcasts the events defined in tspre. Hence, we apply
the function parProd on the list consisting of the input verification tuples with all the
broadcasts filtered and the part of tspre chosen according the set of events that the action
a broadcasts.
    The rest of the elimination of broadcasting is defined in the next two functions.
We define a function vtupleSetNoBcast which is similar to vtupleNoBcast but apply on
verification tuple sets instead.

    vtupleSetNoBcast : (P(VTuple) × seq(Identifier × P(VTuple))) → P(VTuple)
    vtupleSetNoBcast ({vi | i = 1..n} , tspre) = ni=1 vtupleNoBcast(vi , tspre)
                                                 S


We then define the desired function vseqNoBcast which can now be applied to the
topological sort list tss to expand the event broadcasting to suitable verification tuple
sets. This function is defined as following:

    vseqNoBcast : seq(Identifier × P(VTuple)) → seq(Identifier × P(VTuple))
    vseqNoBcast [] = []
    vseqNoBcast [(ei , si ) | i = 1..n] = tsprea [(en , vtupleSetNoBcast(sn , tspre))]
          where tspre = vseqNoBcast([(ei , si ) | i = 1..n − 1])

Hence, we use the result vseqNoBcast(tss) to generate the verification conditions.

5 Predicate Semantics of Statecharts
Our verification approach reveals a strong connection between a statechart transition
and a verification tuple. This motivates us to provide a predicate semantic of statecharts
instead of the traditional operational way in [8,13,11]. We do so by introducing the
functions for translating statecharts to verification tuples. These functions are very sim-
ilar to the functions used in the previous section. In fact, we will use some auxiliary
functions defined previously.
     We first need to provide the data structure used to represent statecharts.
               State , Basic     Identifier
                      | And Identifier × seq(State)
                      | Xor Identifier × seq(State) × State × Transition
where Transition is a five-ary relation defined as following:
            Transition , State × Identifier × Condition × Statement × State
                                                                                               9

This definition says a statechart state can be either
 – a Basic state with a state name,
 – a composite And state encoded by a state name and a sequence of parallel sub
   states, or
 – a composite Xor state encoded by a state name, a sequence of sub states, an initial
   state and a transition relation.
Each transition is defined by its source state, triggering event, transition guard, action
and target state respectively.
   We also use an event-centric approach by dealing with each event separately. Hence,
we first define a function to return the restriction of a statechart with respect to a specific
event. We use hi to denote the empty identifier which indicate the “event name” of a
spontaneous transitions.

    resStateEvent : (Identifier × Sate) → State
    resStateEvent ( , Basic id s) = Basic id s
    resStateEvent (e , And id [si | i = 1..n]) = And id [resStateEvent(i, si ) | i = 1..n]
    resStateEvent (e , Xor id seqs init t)
            = Xor id seqs init [(ss, e′ , c, a, ts) | (ss, e′ , c, a, ts) ← t ∧ (e′ = e∨e′ = hi)]

We then need a function to return the verification tuple correspondent to the initializa-
tion of a state due to the fact that each composite XOR state must have an initial state.

    initialize : State → P(Vtuple)
    initialize s = case s of
         Basic id s → {(0,  / true, StateAssign s, {s})}
         And id [si | i = 1..n] →
                                                       / true, StateAssign s, {s})}])
             parProd([initialize(si ) | i = 1..n]a [{(0,
         Xor id [si | i = 1..n] init t →
             parProd([initialize(init)]a [{(0,/ true, StateAssign s, {s})}])

This function initialize will always return a singleton set, since we enforce only one
possibility to initialize a composite or basic state by disallowing some statecharts vari-
ants [15,16]. However, for convenience the returned type of this function is P(Vtuple)
to make it easier for composing verification tuples together in the intermediate compo-
sition steps. In other words, it allows us to treat this case as a special case of parallel
composition using the parProd function.
     The next step is to define a recursive function to generate verification tuples with
respect to statechart data structure. The base case is the the case of basic states and the
recursive cases deal with composite states. The most difficult problem is caused by the
existence of spontaneous transitions in composite XOR states. We define the following
two functions that take a child state of an XOR state and generate verification condi-
tions. When there are spontaneous transitions, the function getNext invokes getSpon to
search for the spontaneous transition going from the target states and generate verifica-
tion condition for them and then compose the verification conditions together properly.
10

     getNext : (State × Transition) → P(Vtuple)
     getNext (s, tr)
                                   / getSpon(t, tr)]) |(s, id, g, a, t) ∈ tr ∧ id 6= hi}
         = {parProd([{({s}, g, a, 0)},

     getSpon : (State × Transition) → P(Vtuple)
     getSpon (s, tr) = S ∪ parProd([{(0,  / G, Skip, 0)},
                                                     / initialize(s)])
         where
            S = {parProd([{( / g, a, 0)},
                             0,      / getSpon(t, tr)]) |(s, id, g, a, t) ∈ tr ∧ id = hi}
            G = {¬g | (s, id, g, , ) ∈ tr ∧ id = hi}
                V


The set S in function getSpon corresponds to the case the spontaneous transitions are
taken and the condition G is the condition for non of the spontaneous transition from
state s is taken.
    After having these two functions, the rest of the task of generating verification tuples
from a statechart state restricted to one event is defined in the following function.

     s2tuples : State → P(Vtuple)
     s2tuples s = case s of
         Basic id s → {({s}, true, Skip, 0)}/
         And id [si | i = 1..n] → parProd([s2tuples(si ) | i = 1..n]])
         Xor id [si | i = 1..n] init tr → S1 ∪ S2
             where
                S1 = ni=1 getNext(si , tr)
                      S

                G = {¬g | ( , g, , ) ∈ S}
                      V

                S2 = parProd([{(0,  / G, Skip, 0)}]
                                               / a[s2tuples(si )|i = 1..n])

To generate all the verification conditions of a statechart, we first collect the set of all
events in a given statechart. For each event we use the function resStateEvent to get the
restricted statechart to each event in the set and then apply the function s2tuples to the
root of the statecharts. As a result of this process, we will get a map from event names
to verification tuples exactly like the map vtupleMap previously. The branch statements
and event broadcasting in the actions of verification tuples can be easily expanded out
using the function s2tuples and vseqNoBcast defined in the last section.

6 Implementation
The iState tool currently uses the Simplify theorem prover [6] to discharge the generated
verification conditions because of its support of first order logic and linear arithmetic.
Simplify also has arrays built in, though currently iState does not use them. We are
working on extending iState with data types like arrays, rational numbers, and real
numbers. In future, we also plan to extend the verification theory to timed transitions
[14].

7 Discussion
                                                                                             11

Compared to the statechart verification approaches in [4,5,12], we use an event-centric
semantics of statecharts by looking at events as operations rather than data as in the
original state-centric semantics [8]. Instead of writing global temporal specification
(say in CTL or LTL) separately, inspired by nested invariant diagram [2], invariants
(safety properties) are attached to states.
    By attaching invariants to states and utilizing the guarded command representation
of statecharts [15,16], we arrive at a rather straightforward verification method. The
approach generating verification conditions leads to many small “local” verification
conditions and avoids some impossible configurations, compared to when specifying
invariants on the global level. As many small verification conditions are easier to handle
automatically than a few large ones, we believe that the approach can more easily scale
up for the verification of large systems.


References
 1. J.-R. Abrial. The B Book: Assigning Programs to Meaning. Cambridge University Press,
    1996.
 2. R. Back. Invariant based programming revisited. Technical Report 661, TUCS - Turku
    Centre for Computer Science, Turku, Finland, 2005.
 3. M. von der Beck. A comparison of statechart variants. In H. Langmaack, W.-P. deRoever,
    and J. Vytopil, editors, Formal Techniques in Real-Time and Fault-Tolerant Systems, Lecture
    Notes in Computer Science 863, pages 128–148. Springer-Verlag, 1994.
 4. P. Bhaduri and S. Ramesh. Model Checking of Statechart Models: Survey and Research
    Directions. ArXiv Computer Science e-prints, July 2004.
 5. E. Clarke and W. Heinle. Modular translation of statecharts to SMV. Technical Report CMU-
    CS-00-XXX, School of Computer Science, Carnegie Mellon University, August 2000.
 6. David Detlefs, Greg Nelson, and James B. Saxe. Simplify: a theorem prover for program
    checking. J. ACM, 52(3):365–473, 2005.
 7. D. Harel. Statecharts: A visual formalism for complex systems. Science of Computer Pro-
    gramming, 8:231–274, 1987.
 8. D. Harel and A. Naamad. The STATEMATE semantics of statecharts. ACM Transactions on
    Software Engineering and Methodology, 5(5):293–333, 1996.
 9. D.T.M. Le, E. Sekerinski, and S. West, Statechart Verification with iState, FM 06, Canada,
    2006.
10. C. E. Leiserson, R. L. Rivest, and C. Stein. Introduction to algorithms. MIT Press, Cam-
    bridge, MA, USA, 2001.
11. Andrea Maggiolo-Schettini, Adriano Peron, and Simone Tini. A comparison of statecharts
    step semantics. Theor. Comput. Sci., 290(1):465–498, 2003.
12. E. Mikk, Y. Lakhnech, M. Siegel, and G. J. Holzmann. Implementing statecharts in
    PROMELA/SPIN. WIFT, Los Alamitos, CA, USA, 1998. IEEE Computer Society.
13. Shengchao Qin and Wei-Ngan Chin. Mapping statecharts to verilog for hardware/software
    co-specification. In FME, pages 282–300, 2003.
14. S. Samet. Timed transitions in statecharts, from formalization to translation and code. Mas-
    ter’s thesis, McMaster University, Computing and Software Department, 2005.
15. E. Sekerinski and R. Zurob. iState: A statechart translator. In M. Gogolla and C. Kobryn,
    editors, UML 2001, LNCS, pages 376–390, Toronto, Canada, 2001. Springer-Verlag.
16. E. Sekerinski and R. Zurob. Translating statecharts to B. In M. J. Butler, L. Petre, and
    K. Sere, editors, IFM 2002, LNCS, pages 128–144, Turku, Finland, 2002. Springer-Verlag.
