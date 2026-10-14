                                                             Why does it fail?
                                                     Explanation of verification failures

                                                                        Lars-Henrik Eriksson

                                             Department of Information Technology, Uppsala University, Uppsala, Sweden
                                                                          lhe@it.uu.se
arXiv:2603.21788v1 [cs.LO] 23 Mar 2026




                                               Abstract. Satisfiability solving is a common technique for formal ver-
                                               ification forming the basis of many proof and model checking systems.
                                               Failure to show a proof obligation will produce a counterexample or
                                               failure trace with typically many thousands or even millions of boolean
                                               variables. Interpreting such a counterexample poses a challenge. Even if
                                               the individual variables are all understood, it is difficult to form a “big
                                               picture” of the situation causing the failure. We consider the case where
                                               verification conditions are expressed using concepts from a formal appli-
                                               cation domain model in a language based on predicate logic or a similar
                                               language. We introduce a method to explain verification failures in ap-
                                               plication domain terms. A measure of the relative relevance of predicates
                                               is used to extract the parts of a formula most likely to contribute mean-
                                               ingfully to the explanation. Dependencies between predicates are used
                                               to form a branching sequence of successive explanations. These explana-
                                               tions can help a practitioner find faults in the system being verified. The
                                               method is demonstrated on examples and compared to other methods.

                                               Keywords: Formal verification, Failure explanation, Model exploration.


                                         1   Introduction

                                         Satisfiability (SAT) solving is a fundamental proof technique that is used as
                                         the underlying method of many proof and model checking tools used for formal
                                         modelling and verification, notably the Alloy Analyzer [7]. Many verification
                                         problems expressed in a rich specification language can be naturally translated
                                         into propositional logic. Even though such translations typically give rise to very
                                         large SAT problems with hundreds of thousands or even several million proposi-
                                         tional variables, modern SAT solving engines solve such problems efficiently [3].
                                         When formal verification fails, the tool will provide a counterexample – a set
                                         of facts, such as combination of inputs and outputs or parts of a trace, which
                                         disagrees with the formal specification.
                                             When traditional testing fails, the specific situation that leads to an error
                                         is given by the test case. In formal verification there are no test cases as such,
                                         instead a particular situation where the error occurs is implicit in the counterex-
                                         ample. It is then necessary to analyse the counterexample to reconstruct a “test
                                         case” after the fact to be able to understand why the failure occurred. Given the
2       L.-H. Eriksson

large amount of low-level data involved in the counterexample and that most of
it will be unrelated to the fault, this is a daunting task to take on.
    A formal domain model [2] is a mathematical description of the environment
(application domain) in which a computer system operates. A well-structured
model helps the software engineer to better understand the application domain
and thus to write better formal requirements specifications of a software system.
It also makes it easier for application domain experts who are not themselves
formal methods practitioners to understand formal specifications.
    A formal domain model can describe the environment on different levels. For
example, in the railway domain, a domain model can describe the kinds of entities
and their possible relationships such as the physical tracks, signalling systems,
train movements, time tables, rolling stock management, reservations, ticketing
etc. depending on the purpose of the software to be designed [11]. Combining the
domain model with data about concrete entities and relations, e.g. descriptions
of the actual tracks, signals etc. of a particular railway [5, 6], yields a model of
the environment in which a specific computer system operates.
    Formal domain models can be used to create high-level descriptions of coun-
terexamples. Low-level counterexample data can be translated back to concepts
defined in the domain models. For example, in the railway domain individual
signal lamp status signals can be translated back to abstract signal aspects.
However, there need also be a mechanism to filter out relevant data from the
counterexamples. As an example, if a railway signalling system omits a neces-
sary check of a status signal, causing a high-level requirement to be violated, an
explanation of the counterexample could point to that particular status signal.
    We have developed a method to create such explanations. Compared to other
methods, the main innovation is the use of a concept of “interest” to extract
the information most likely to give a useful explanation. The method has been
implemented and experimentally tested on the verification tool GTO [6, 12].
    The method can of course also explain “positive” results e.g. why a formula
is true, but it was developed primarily with failure explanations in mind.
    This article is organised as follows: In section 2 we summarise our logical
formalism. Section 3 describes our method for explanation-finding while section
4 given an applied example. Section 5 discusses the method and compares it
to an alternative method. Section 6 discusses relevant existing work. Finally, in
section 7 we give conclusions and directions for further work.


2   Foundations

We consider the problem of finding explanations to failed formal verification
problems in many-sorted first-order (predicate) logic with finite universes (bounded
quantification), such as can be found using SAT solvers. In this section we sum-
marise the necessary logical concepts. They are for the most part standard and
are included as a reference to the particular variant of formalism we use.
   The formulæ of our logic are constructed in the standard way from a set of
predicate symbols including equality, constant symbols, variables, and the op-
                                                                    Why does it fail ...   3

erators ¬, ∧, ∨, →, ↔, ∀, ∃. Predicate symbols (or simply “predicates”) take zero
or more variables or constants as arguments. (Zero argument predicates are
the same as propositional symbols.) For simplicity, we do not include function
symbols in the language, but generalisation to a logic with function symbols is
straightforward. An atom is a predicate applied to a set of arguments (constants
or variables). A literal is an atom or a negated atom. We will write predicates,
variables and constants in lowercase and use uppercase names for formulæ.
    Our logic also has definitions of the form p(x1 , . . . , xn ) ≡ P, n ≥ 0 where the
xi are distinct variables. Logically, they represent the formulæ

                          ∀x1 , . . . , xn .(p(x1 , . . . , xn ) ↔ P )

but provide additional information to our explanation algorithm.
    Free and bound variables are defined in the usual way. Variables range over
objects of some particular subset of a universe, depending on their sorts. We
assume that every object in the universe is associated with an individual con-
stant symbol. To simplify the presentation, we will identify objects with their
corresponding constants. A closed formula is a formula with no free variables.
    We will sometimes use sets of formulæ in place of a single formula. Such a
set should be understood as a representation of the conjunction of all formulæ
in the set. The empty set represents a formula that is always true.
    An interpretation, I, is an assignment of truth values to ground (variable-
free) atoms. Thus under an interpretation any closed formula has a particular
truth value. In the sequel, we will identify an interpretation with the set of atoms
true under the interpretation. The standard definition of an interpretation in
predicate logic is a structure which includes the universe. Here we separate the
two and take the universe (and the sorts) as given. This is motivated below.
    An interpretation I satisfies a closed formula P , formally I ⊨ P , iff P is true
under I. A formula is satisfiable if there is a satisfying interpretation, otherwise
unsatisfiable. Note that if I ̸⊨ P , then I ⊨ ¬P and vice versa.
    In the literature, the term model is used with two different meanings. One is
for a set of logical axioms – a theory – that describes some system, the other is
for an interpretation such that all the axioms of a theory are true. Here we will
only use the term “model” in the first sense. When the second sense is needed,
we will talk about a “satisfying interpretation”.
    R is a logical consequence of P iff every interpretation that satisfies P also
satisfies R. Formally, we write P ⊨ R. As a special case, ⊨ R means that R is
true in every interpretation or, equivalently, that there is no interpretation that
satisfies ¬R. P ⊨ R means that every interpretation either makes P false or R
true. This is the same as ⊨ P → R, so to show P ⊨ R, it suffices to show that
there is no interpretation satisfying ¬(P → R) or, equivalently, P ∧ ¬R.
    SAT solvers find satisfying interpretations of formulæ in propositional logic.
To use a SAT solver with predicate logic, formulæ must first be transformed into
a propositional formulæ. With a finite universe, this can be done by rewriting
every quantified (sub)formula as a conjunction (for ∀) or a disjunction (for ∃)
of the set of instances of the quantified formula obtained by substituting bound
4       L.-H. Eriksson

variables with each constant of the universe belonging to the sort of the variable.
Formally, ∀x.P is rewritten as P [c1 /x] ∧ · · · ∧ P [cn /x] where {c1 , . . . , cn } is the
set of constants belonging to the sort, and analogously for ∃.
    With all quantified formulæ rewritten, the atoms are ground and can be
regarded as a propositional symbol so the rewritten formula can be used by a
SAT solver. If the formula is satisfiable the SAT solver will give a truth value to
each atom, i.e. an interpretation. The fact that the rewriting uses a particular
universe motivates the separation of the universe from the interpretation.
    A formal verification problem involves showing that a satisfying interpreta-
tion of a model of the system to be verified, P , meets requirements expressed by a
verification condition R, given an application domain model D. Some predicates
are used to represent inputs to the system, others are used to represent outputs or
internal states. Thus an interpretation expresses a certain combination of inputs,
outputs and states. A system is correct if every input-output-state combination
made possible by the system is also allowed by the requirement. Formally, we
must show that every satisfying interpretation of the system and the domain
also satisfies the requirement, or P, D ⊨ R. This is the same as ̸⊨ P ∧ D ∧ ¬R.
If there actually is a satisfying interpretation of P ∧ D ∧ ¬R, then it describes a
situation occurring in the system which is not allowed by the requirements. Our
goal is to describe ways to explain why that situation has arisen.


3    Finding explanations
Explanations are always in the context of a particular interpretation. When
stating that a formula is true or false, it is with respect to that interpretation.
    Our method proceeds in two alternating phases. One phase gives an expla-
nation for a particular formula, while the other phase creates a tree of successive
explanations. We will introduce the first phase by an example.

Example 1. Let p be the characteristic predicate of a set and let q represent an
interesting property. Assume a single sort with universe {a, b, c} and an inter-
pretation such that p(a), q(a), q(c) are all true and p(b), p(c), q(b) are all false.
That is, the set characterised by p is {a} and a and c both have the property.
    Now, the formula ∀x.(p(x) → q(x)) is true under the interpretation. What
atom is intuitively the most important one for understanding why the formula
is true? Arguably, it is q(a). Why? Atoms of the form p(x) serve as “filters” to
decide for what objects we should check the property and are thus less interesting
in themselves. As b and c are “filtered out”, q(b) and q(c) do not affect the truth
value of the formula and are thus also less interesting. We say that the set
{q(a)} is the explanation of why ∀x.(p(x) → q(x)) is true (This example will be
described in more detail after the definition of the algorithm.)

    Our algorithm will compute exactly that explanation. It works by selecting
“interesting” parts of the formula using two criteria. One criterion is that an
immediate subformula is interesting if changing its truth value would change the
truth value of the whole formula.
                                                         Why does it fail ...     5

Example 2. Suppose that P is true and Q is false. Then the explanation of Q is
also an explanation of why P ∧ Q is false, as changing the truth value of Q to
true will also change the truth value of P ∧ Q from false to true.
   If changing the truth value of any single subformula will change the truth
value of the whole formula, then instead an “interest measure”, intr , on formulæ is
used. The explanation will be taken from the highest interest subformula. If both
subformulæ have the same measure, then the explanations of the subformulæ
together is the explanation of the whole formula.
Example 3. Suppose that P and Q are both true and that intr (P ) = intr (Q).
Then the explanations of P and Q together is the explanation of why P ∧ Q is
true. Suppose instead that intr (P ) > intr (Q). Then only the explanation of P
is an explanation of why P ∧ Q is true.
    If the truth value of a formula is unchanged unless the truth value of both
subformulæ are changed, then instead we use the explanation of the subformula
with the least interest measure. If both subformulæ have the same measure,
one explanation is chosen arbitrarily. This is motivated later in this section and
further discussed in section 5.
Example 4. Suppose that P and Q are both false and that intr (P ) = intr (Q).
Neither P nor Q provides an explanation to why P ∧ Q is false according to our
first criterion as changing the truth value of either (alone) does not change the
truth value of P ∧ Q. As the falsity of P and Q separately explains the falsity
P ∧ Q, the explanation of one of them is arbitrarily chosen. Suppose instead
that intr (P ) > intr (Q). Then the explanation of the subformula with the lesser
interest, Q, is chosen as the explanation of why P ∧ Q is false.
    These principles are applied recursively in a bottom-up manner. Initial in-
terest measures are applied to predicates and explanation formulæ inherit the
measure of their explanation subformulæ. Atoms are negated in explanations if
they are false. Formally, the explanation function expl and the interest measure
function intr are defined together as:
Definition 1 (expl and intr ).
                     (                                
                       {A}       when A is true       
         expl (A) =
                                                      
                       {¬A} when A is false              if A is an atom
                                                      
         intr (A) = (depending   on the application)
                                                      
         expl (¬P ) = expl (P )
         intr (¬P ) = intr(P )
         expl (P ∧ Q) =
                             according to Table 1
         intr (P ∧ Q) =                 
         expl (P ) = expl (rewrite(P ))
                                          in other cases, see definition 2
         intr (P ) = intr (rewrite(P ))

The auxiliary function rewrite is defined as:
6       L.-H. Eriksson

Definition 2 (rewrite).
           rewrite(P1 ∨ · · · ∨ Pn ) = ¬(¬P1 ∧ · · · ∧ ¬Pn )
           rewrite(P → Q) = ¬(P ∧ ¬Q)
           rewrite(P ↔ Q) = (P → Q) ∧ (Q → P )
           rewrite(∀x.P ) = P [c1 /x] ∧ · · · ∧ P [cn /x]
           rewrite(∃x.P ) = ¬(∀x.¬P )
           where the ci are the constants belonging to the sort of x.



            P    Q       intr (P ) vs. intr (Q)       expl (P ∧ Q)          intr (P ∧ Q)
          false false             <                      expl (P )            intr (P )
          false f alse            =               expl (P ) alt. expl (Q)     intr (P )
          false false             >                      expl (Q)             intr (Q)
          false true                                     expl (P )            intr (P )
          true false                                     expl (Q)             intr (Q)
          true true               <                      expl (Q)             intr (Q)
          true true               =                expl (P ) ∪ expl (Q)       intr (Q)
          true true               >                      expl (P )            intr (P )
                                Table 1. Explanations of ∧



     It may seem counterintuitive that in the false-false case for ∧ in Table 1,
we chose the explanation of the subformula with the least interest measure. To
see why, let’s examine Example 1 in more detail. According to the definition of
rewrite, the quantified formula ∀x.(p(x) → q(x)) is rewritten as a conjunction of
all instantiations of the quantified subformula. Also, the implications are rewrit-
ten as negated conjunctions. We get a conjunction of three (true) conjuncts.
                                   ¬(p(a) ∧ ¬q(a))          (1)
                                   ¬(p(b) ∧ ¬q(b))          (2)
                                   ¬(p(c) ∧ ¬q(c))          (3)
The explanations of (1) and (2) are {q(a)} and {¬p(b)}, respectively. As (1)
and (2) are both true and p is less interesting than q, the explanation of their
conjunction, ¬(p(a) ∧ ¬q(a)) ∧ ¬(p(b) ∧ ¬q(b)) will be {q(a)}. But what about
(3)? Both p(c) and ¬q(c) are false, so there are two possibilities. If we use the
most interesting one, ¬q(c), for the explanation of (3), the explanation of the
conjunction of (1), (2), and (3) – and thus the quantified formula – will be
{q(a), q(c)} – as q(a) and q(c) are of equal interest. That is not what we intended.
If we (according to Table 1) instead choose the less interesting one, ¬p(c), from
(3) it will be discarded when compared to q(a), as both are true. The explanation
of the whole formula will then be as intended, {q(a)}.
    In the second phase, we attempt to find further explanations of any defined
explanation literals. For example, if q is defined by q(x) ≡ r(x) ∨ s(x) the def-
inition is used on q(a) to obtain r(a) ∨ s(a). The explanation process is then
                                                            Why does it fail ...     7

repeated on this new formula. In Example 1, the explanation only included one
literal, but generally there can be more than one. In that case we will get a
branching structure of explanations – an “explanation tree”. The larger example
in section 4 includes an explanation tree.
    We have not attempted to give a formal characterisation of explanations.
Ultimately, it is the practical usefulness of explanations that matters and not if
they have a formal characterisation.


4     A worked example
As an application of explanation finding, we will use a fragment of a formal
verification problem taken from the railway domain. The problem is to verify
that the system controlling signals and points (switches) of the railway – the
interlocking – sets a signal to display a “proceed” aspect (green light) only when
it is safe to do so. The methodology used is described in more detail in [5, 6].
Consider the small railway system in Figure 1.




                                Fig. 1. Railway system


    The railway system is divided into units (sections) while signals control train
movements. There are train routes – sets of units over which trains move. Train
routes start at a signal and extend to the next signal. They are identified by
these signals, e.g. rt2131 will designate the train route starting at signal 21 and
ending at signal 31. In all, there are 8 different train routes in this example1 .
    The universe has constant symbols for the designators of track units, signals
and train routes. In the sequel, variables u have the sort of track units, p of
points (a subset of track units), s of signals and r of train routes.
    The verification condition is expressed in a generic way independent of a
particular track layout using concepts from a formal domain theory. By supplying
a description of the railway system, the verification condition becomes applicable
to that particular system. Finally, the abstract model is combined with a model
of the actual interlocking giving a complete verification problem.
    The domain theory has a set of predicates to describe the track layout.



1
    Routes from signals 41 and 42 are not considered as they extend outside the railway
    system under consideration.
8         L.-H. Eriksson

     connectsto(u1 , u2 )   Track units u1 and u2 are adjacent to each other.
     leftbranch(p, u)       In the left position, points p lead to unit u.
     rightbranch(p, u)      In the right position, points p lead to unit u.
     partof (u, r)          Unit u is part of the train route r.
     before(u, r)           A train enters train route r from unit u.
     ahead (s, u)           Signal s is located at one end of unit u, facing it.
     inrear (s, u)          Signal s is located at one end of unit u, facing away
                            from the unit.

    The theory includes axioms that constrain these predicates to what is physi-
cally possible, e.g. that connectsto is symmetric. When using the domain theory
in a particular application, they are defined to reflect the layout of the track sys-
tem. For the particular railway system of Figure 1, one definition would begin

              partof (u, r) ≡ r = rt2131 ∧ (u = pt21 ∨ u = track1 ) ∨
                              r = rt2133 ∧ (u = pt21 ∨ u = track2 ) ∨ . . .

It should be clear how the other predicates would be defined for this example.
    Additional predicates are used for high-level representation of (abstract) in-
put signals coming from the track system. A predicate instance is true if the
corresponding input signal is present.

     left(p)                Points p are in the left position.
     occupied (u)           (Part of) a train is occupying unit u.
     proceed (s)            Signal s is showing a “proceed” aspect.
     right(p)               Points p are in the right position.
     routelocked (r)        Route r is reserved for a train movement.

      Predicates representing various concepts can now be defined.

     conflict(r1 , r2 )     Routes r1 and r2 can not safely be used by different
                            trains at the same time.
     entry(s, r)            Signal s controls train entry into route r.
     first(u, r)            u is the first track unit of route r. (In the direction
                            of train movement.)
     inconflict(r)          Route r is currently in conflict with another locked
                            (reserved) route.
     pointsok (r)           All points in route r are set in the positions appro-
                            priate to the route.
     safe(r)                Route r is safe for train movements.
     unoccupied (r)         The whole of route r is free of trains.

   Signals beginning a route show a “proceed” aspect (green light) into the route
only when it is safe to do so. Entering a train route is considered safe whenever
    – the route is “locked”, i.e. it is reserved for a train movement (routelocked ).
    – points in the route are in the correct position for train movement (pointsok ).
                                                           Why does it fail ...      9

 – there are no other trains occupying any part of the route (unoccupied ).
 – no other locked train route is overlapping this route (negation of inconflict).
The definitions of these predicates are
    conflict(r1 , r2 ) ≡ r1 ̸= r2 ∧ ∃u.(partof (u, r1 ) ∧ partof (u, r2 ))
    entry(s, r) ≡
      ∃u.(ahead (s, u) ∧ before(u, r)) ∧ ∃u.(inrear(s, u) ∧ first(u, r))
    first(u, r) ≡ partof (u, r) ∧ ∀u1 .(before(u1 , r) → connectsto(u, u1 ))
    inconflict(r) ≡ ∃r1 .(r1 ̸= r ∧ routelocked (r1 ) ∧ conflict(r, r1 ))
    pointsok (r) ≡ ∀p.(partof (p, r) →
      (∃u.(leftbranch(p, u) ∧ (partof (u, r) ∨ before(u, r))) → left(p)) ∧
      (∃u.(rightbranch(p, u) ∧ (partof (u, r) ∨ before(u, r))) → right(p)))
    safe(r) ≡ routelocked (r) ∧ pointsok (r) ∧ unoccupied (r) ∧ ¬inconflict(r)
    unoccupied (r) ≡ ∀u.(partof (u, r) → ¬occupied (u))
Using these definitions, the verification condition can be stated as
                    ∀s.(proceed (s) → ∃r.(entry(s, r) ∧ safe(r)))
I.e. if a signal shows a “proceed” aspect, then it must lead to a safe route.
    We now turn to the interlocking to be verified. Suppose that an interlocking
of the rail system in the figure correctly implements the verification condition
and that the part controlling signal 21 is modelled by these definitions:
                 green21 ≡ lock21 ∧ ¬lock32 ∧ ¬lock34 ∧ tc21 ∧
                          (left21 ∧ tc2 ∧ (¬lock22 ∨ left22 )∨
                            right21 ∧ tc1 ∧ (¬lock22 ∨ right22 ))
                 red21 ≡ ¬green21
    The propositional symbols green21 and red21 represent outputs from the
interlocking to the lights in the signal. The other propositional symbols represent
states or inputs of the interlocking, being true when a route from a signal is locked
(e.g. lock21 ), when a set of points is in a particular position (e.g. left21 ) or when
a track unit is free from trains (e.g. tc21 is true if points 21 are free).
    Additionally, we need the axiom
                                 ¬(left21 ∧ right21 )
to express the physical fact that points 21 can’t be in both the left and the
right positions simultaneously. (However, it is possible for them to be in an
intermediate position.)
    Finally, we need to connect the predicates of the domain model representing
“abstract” status with the concrete status signals of the interlocking.
left(p) ≡ p = pt21 ∧ left21 ∨ p = pt22 ∧ left22
occupied (u) ≡ u = north ∧ ¬tcn ∨ u = pt21 ∧ ¬tc21 ∨ u = track1 ∧ ¬tc1 ∨ . . .
proceed (s) ≡ s = si21 ∧ green21 ∧ ¬red21 ∨ s = si22 ∧ green22 ∧ ¬red21 ∨ . . .
right(p) ≡ p = pt21 ∧ right21 ∨ p = pt22 ∧ right22
routelocked (r) ≡ lock21 ∧ (r = rt2131 ∧ right21 ∨ r = rt2133 ∧ left21 ) ∨ . . .
10     L.-H. Eriksson

The verification condition ∀s.(proceed (s) → ∃r.(entry(s, r) ∧ safe(r))) is prov-
able given these definitions and axioms. Now suppose we create a fault in the
interlocking by dropping tc1 from the definition of green21 . The verification con-
dition will now be falsifiable and a SAT solver will find an interpretation where
green21 and right21 are true while tc1 is false.
    Before applying the explanation algorithm on this counterexample, we have
to decide on the interest measure of the different predicates. We use a “syntactic”
approach to make the explanation process more automated and not require the
user to manually assign interest values. Free predicates (predicates without a
definition) are considered most interesting. In this example free predicates rep-
resent input signals to the interlocking – directly pointing to a condition in the
actual railway system. Predicates are then assigned lower interest measures ac-
cording to how their definitions depend on other predicates. Interest measures
are assigned in descending order as follows:
 – predicates without a definition (most interesting), e.g. tc1
 – defined predicates that – directly or indirectly – depend on at least one
   predicate not having a definition, e.g. occupied
 – defined predicates that – directly or indirectly – depend on some other pred-
   icate, but only on predicates having a definition, e.g. conflict
 – defined predicates that do not depend on other predicates, e.g. partof
 – equality (least interesting)
   To understand the reason for the failure of the verification condition, we first
apply the explanation function expl to it, which gives

                 {proceed (si21 ), ¬safe(rt2131 ), ¬safe(rt2133 )}

Each literal starts a new branch in the explanation tree. Secondly, we use the
definitions of proceed and safe on these literals to obtain the three formulæ

              si21 = si21 ∧ green21 ∧ ¬red21 ∨
                si21 = si22 ∧ green(si22 ) ∧ ¬red(si22 ) ∨ . . . (1)
              ¬(routelocked (rt2131 ) ∧ pointsok (rt2131 )∧
                 unoccupied (rt2131 ) ∧ ¬inconflict(rt2131 )) (2)
              ¬(routelocked (rt2133 ) ∧ pointsok (rt2133 )∧
                 unoccupied (rt2133 ) ∧ ¬inconflict(rt2133 )) (3)
    expl is again applied to each of the formulæ to create new branches and
definitions are again applied to each new explanation literal, and so on until no
more explanations are obtained. This gives the explanation tree in Figure 2.
    The tree is cut off at the second occurrence of green21 , as there already is
an explanation for that literal being true.
    One explanation of the failure is that signal 21 is showing a “proceed” aspect.
Further explanations show that the green light in the signal is turned on and the
red light turned off, which is expected. Another explanation is that the route
from signal 21 to signal 31 is not safe. Further explanations show that this is
due to the route not being unoccupied, to track 1 being occupied and finally to
                                                                   Why does it fail ...   11

                    ∀s.(proceed (s) → ∃r.(entry(s, r) ∧ safe(r)))

              proceed (si21 )        ¬safe(rt2131 )           ¬safe(rt2133 )

                                  ¬unoccupied (rt2131 ) ¬routelocked (rt2133 )

                                    occupied (track1 )      ¬pointsok (rt2133 )

                         ¬red21             ¬tc1               ¬left(pt21 )

          green21       green21                                     ¬left21




           lock21    ¬lock32      ¬lock34     tc21       right21     ¬lock22


                                Fig. 2. Explanation tree


input signal tc1 not being true. The interlocking logic for signal 21 (definition
of green21 ) indeed does not depend on tc1 so this is the reason for the failure.
    One branch remains. Signal 21 is also the starting point of the unsafe train
route to signal 33. That, however, turns out to be because points 21 are not
set to the left, which is expected as the route takes the right path through the
points. We can see that the interlocking does check that condition properly.
    To see some details, consider ¬unoccupied (rt2131 ). The definition of unoccupied
gives ¬∀u.(partof (u, rt2131 ) → ¬occupied (u)). Applying expl gives
          expl (¬∀u.(partof (u, rt2131 ) → ¬occupied (u)))
          = expl (∀u.(partof (u, rt2131 ) → ¬occupied (u)))
          = expl (rewrite(∀u.(partof (u, rt2131 ) → ¬occupied (u))))
          = expl ((partof (track1 , rt2131 ) → ¬occupied (track1 )) ∧
                  (partof (track2 , rt2131 ) → ¬occupied (track2 )) ∧ . . . )
All conjuncts of the last argument to expl are true except the first one which is
false. According to Table 1, only the explanation of that conjunct will contribute
to the explanation of the whole formula, so we continue
         = expl (partof (track1 , rt2131 ) → ¬occupied (track1 ))
         = expl (rewrite(partof (track1 , rt2131 ) → ¬occupied (track1 )))
         = expl (¬(partof (track1 , rt2131 ) ∧ ¬¬occupied (track1 )))
         = expl (partof (track1 , rt2131 ) ∧ ¬¬occupied (track1 ))
Now both conjuncts of the last argument to expl are true so, again according to
Table 1, the one with the highest interest measure is chosen. As we mentioned
above, occupied is of higher interest than partof , so the final explanation becomes
the explanation of ¬¬occupied (track1 ), which is {occupied (track1 )}.
12     L.-H. Eriksson

5    Discussion
While pinpointing the relevant reason for the failure, the explanation tree of Fig-
ure 2 also includes some redundant information that does not contribute to the
understanding of the failure. For example, the subtrees beginning with ¬red21
and ¬safe(rt2133 ) do not point to the actual cause of failure. The subtree be-
ginning with ¬red21 could be seen as redundant as it is cut off at green21 which
has occurred earlier in the tree. However, even with such pruning if the branch
with ¬red21 had been developed before the branch with green21 , we would get
the tree of Figure 3. This tree arguably does not give a better explanation as it
has the “detour” through ¬red21 to get to the explanations of green21 .


                   ∀s.(proceed (s) → ∃r.(entry(s, r) ∧ safe(r)))

            proceed (si21 )         ¬safe(rt2131 )            ¬safe(rt2133 )

               ¬red21         ¬unoccupied (rt2131 ) ¬routelocked (rt2133 )

                                occupied (track1 )          ¬pointsok (rt2133 )

               green21                  ¬tc1                   ¬left(pt21 )

                                                                 ¬left21

               lock21     ¬lock32      ¬lock34       tc21      right21     ¬lock22


                          Fig. 3. Alternative explanation tree


    The explanation trees have three distinct branches of which only one actually
gives the desired explanation. It is not clear how to algorithmically pinpoint
that branch as that would require an actual understanding of the purpose of the
system being verified. The explanation that signal 21 shows a proceed aspect
is valid, as forcing the signal to red at all times would make the verification
succeed. However, that would also make the interlocking system unfit for its
intended purpose. The remaining explanation (¬left21 ) could in principle have
been caused by an incorrect check of the points position for train route rt2133 .
    The false-false case of Table 1 could appear to lose information when the
interest levels of the two explanations are the same as only one of the explana-
tions of the two conjuncts, P and Q, is used. This could matter if the falsity
of the conjuncts is independently caused by faults in the system being verified.
For example, if the quantified subformula of the example verification condition,
proceed (s) → ∃r.(entry(s, r) ∧ safe(r))), was false for two or more different sig-
nals, s, only one signal would figure in the explanation.
                                                              Why does it fail ...   13

    However, information would not actually be lost in a practical verification
setting. Generally all faults in a system will not manifest in a single verification
counterexample. Once one fault has been identified, to find another one the
verification must be retried with assumptions added that exclude the situation
leading to the identified fault, generally giving a different counterexample2 .
    In the case of P ∧Q where P and Q are false because of independent faults and
the explanation of P is chosen, excluding that fault situation in a new verification
attempt would make P true and then the explanation would be based on Q. For
the same reason it doesn’t matter for completeness that when the interest levels
of the two explanations are different, the least interesting one is used.
    In the railway example, changing the false-false case with equal interests to
use both explanations would not add any more information to the explanation
tree. It would, however, create an additional short branch in the tree which would
be redundant in the same way as the ¬red21 − green21 branch.


6     Related work
Broadly speaking, there are two main approaches to explaining the causes of
counterexamples – with and without the presence of a domain model. In the
approach without a domain model, the explanation focuses on what atoms in
the model of the system to be verified have values that “cause” a verification
condition to fail. In approaches with a domain model, the explanation is given
in terms of that model. Our approach is primarily an example of the latter.
    Most work on explanation of interpretations in terms from a theory/model
have been done in the context of the Alloy Analyzer [7]. This includes model ex-
ploration which is technically very similar to counterexample explanation. The
purpose of explanation in model exploration is to identify the formulæ that
“cause” a particular aspect of a satisfying interpretation for the purpose of help-
ing a user to understand or debug a model of some software or system.
    The second phase of our method finds explanations of literals using defini-
tions. This has the drawback that literals with predicates that are not explicitly
defined can’t be explained. Nelson et al. [10] give an algorithm to find prove-
nances – explanations of literals using arbitrary formulæ –– not just definitions.
A provenance is a finite set of formulæ which explain why a literal is true in the
sense that the literal is a logical consequence of the provenance (and the model),
while the provenance formulæ are independent of the literal in the sense that
they remain true even if the truth value of the literal would be reversed.
    We will compare their approach to ours, using the interpretation of defini-
tional formulæ as equivalences. As the description in [10] uses the relational logic
of the Alloy Analyzer3 [7], we have reformulated it in appendix A in the context
of predicate logic. Also, as the description in [10] is somewhat hard to follow, we
have modified it slightly for simplicity and clarity. Thus our formulation of the
provenance algorithm can also be of interest in its own right.
2
    This methodology is further described in [6].
3
    As is the case with our logic, quantifiers in the logic of Alloy are bounded.
14       L.-H. Eriksson

     In the example, the explanation of the starting formula was the set

                  {proceed (si21 ), ¬safe(rt2131 ), ¬safe(rt2133 )}

For these three literals, the provenance algorithm gives the same result as our use
of definitions. However, further down the tree, using the provenance algorithm
on ¬unoccupied (rt2131 ) gives two possible explanations. One is the same we get
using definitions, ¬∀u.(partof (u, rt2131 ) → ¬occupied (u)), the other is the set

 {¬safe(rt2131 ), routelocked (rt2131 ) ∧ pointsok (rt2131 ), ¬inconflict(rt2131 )}

¬safe(rt2131 ) is redundant, having already been encountered in the tree. The
other two formulæ do not point to facts relevant to the failure. The reason is that
the provenance algorithm lacks the sense of direction that definitions provide.
In this example, by pruning explanations including literals already encountered
(such as ¬safe(rt2131 )), we actually do obtain the same tree as in Figure 2.
     In some cases the lack of a sense of direction could be advantageous. For
example, using the axiom ¬left21 ∨ ¬right21 , the provenance algorithm explains
¬left21 by right21 being true. In conclusion, while the provenance algorithm
could give some additional explanations, its lack of direction also causes difficul-
ties.
     Dougherty et.al. [4, 13, 14] have studied how finding satisfying interpretations
which are, in a sense, minimal can help provide explanations. Zheng et.al. [17]
describes a fault localisation method for Alloy models using SAT solving to find
interpretations that exhibit a fault as well as those that do not. Failing and non-
failing interpretations are compared and the differences are used to pinpoint
parts of the model likely to contribute to the failure. Wang et.al. [8, 16] use a
test-driven approach, which is similar in that interpretations are compared, but
where they are generated by mutating failing properties. Satisfying interpreta-
tions using different tests are compared to find parts of the model that likely
contribute to the failure.
     The work of Siegel et.al. [15] does not use a domain theory but otherwise has
some similarities to ours, pinpointing the parts of verification conditions that
contribute to the failure (i.e. to the condition being false).


7     Conclusions and further work
We have devised and implemented a method for giving high-level explanations of
failures of verification proofs carried out by SAT solvers. The main contribution is
combining the use of a domain theory to define high-level concepts with a concept
of interest to extract the information most likely to give a useful explanation.
The method has been demonstrated using a small but realistic example. Some
shortcomings have been discussed which could be addressed by further work.
Also possible extensions using the related work of Nelson et al. [10] have been
discussed. It would also be of interest to implement the method for the Alloy
Analyzer to gain experience with the large amount of models developed for Alloy.
                                                          Why does it fail ...     15

    Natural extensions of our approach would be to use temporal logic and un-
bounded quantification (infinite domains). Extension to linear time temporal
logic (LTL) with past-time operators [9] seems straightforward. Instead of a
single interpretation, we would have a sequence of interpretations (a trace).
The explanation algorithm would first use the final interpretation of the se-
quence and move back one step in the sequence when encountering the previous-
moment operator, ⊖. The since connective, S, could be handled by replacing
every (sub)formula P S Q with a new unique predicate psq and for all such
predicates adding the axiom psq ↔ P ∨ Q ∧ ⊖psq. As past-time and standard
(future-time) LTL have the same expressibility over finite traces [9], formulæ of
standard LTL can be handled by translating into past-time LTL.
    Handling unbounded quantification would allow explanations of failing inter-
pretations generated by SMT solvers [1] and could also be advantageous when
quantifying over finite domains so large that the basic method gives unwieldy
results. How to accomplish this is less clear, as the first phase of our method
relies on expanding universal quantifiers to a conjunction of instances of the
quantified formula. In the case where the quantified formula is false, according
to Table 1 the explanation of any single formula instantiated with a witness to
the falsity will do. In the case where the quantified formula is true, then – again
according to Table 1 – the explanation should be made up of the explanations
of all the infinite number of instances, which is not possible.
    In the case that true instances have uniform explanations (identical except
for the instantiation of the quantified variable), a single explanation including
the quantified variable could be given. That approach could also be used in
the case of bounded quantification, in particular when the domain is large. The
question then, is how to determine that all instances have uniform explanations?
On the other hand, the Alloy Analyzer has been very successful using only finite
domains, so maybe an extension to unbounded quantification is not so important.

A    Provenances
This appendix gives the provenance algorithm of [10] reformulated for clarity
and using predicate logic rather than relational logic.
    Given a theory (set of formulæ) T , a satisfying interpretation M of T with
a finite universe U, and a literal L true under M, we want to explain why L
is true. A provenance for L is a finite (possibly empty) set of true formulæ Pi
which explains why L is true in the sense that L is a logical consequence of the
Pi and T while at the same time, each Pi will remain true even if the truth value
of L is reversed. (I.e. the truth of the Pi do not depend on the truth value of L.)
Definition 3 (L-alternate). Given an interpretation M and a true literal L,
the L-alternate, ML , is the same interpretation as M except that L is false, i.e.
the atom of L has the different truth value in ML .
Definition 4 (Provenance). A provenance for a literal L (true in M), with
respect to a set of formulæ T (all true in M), is a set of formulæ {P1 , . . . , Pn },
for n ≥ 0, such that each Pi is true in both M and ML , and T ∪{P1 , . . . , Pn } ⊨ L.
16      L.-H. Eriksson

    Provenances are obtained by the “explanation function” Y, parameterised
by M and L, so that Y(T ) gives the set of all provenances of L. Y is defined
on formulæ true in M but false in ML . Strictly speaking we must also have
ML ⊭ T , but if we did not L would be independent of T and then there would
be no provenance anyway.
    The auxiliary function Y¬ handles the dual case, being defined on formulæ
false in M but true in ML . The auxiliary function rewrite (parameterised by U)
is as defined in section 3.

Definition 5 (Y).

             Y(A) = {∅}, if A is San atom
             Y(P1 ∧ · · · ∧ Pn ) = {Y(Pi ) | 1 ≤ i ≤ n, ML ⊭ Pi }
             Y(¬P ) = Y¬ (P )
             Y(P ) = Y(rewrite(P )), in all other cases

             Y¬ (A) = {∅}, if A is an atom
             Y¬ (P1 ∧ · · · ∧ Pn ∧ Q1 ∧ · · · ∧ Qm ) =
                                                      ∪       ∪
              {{P1 , . . . , Pn } ∪ P | P ∈ (Y¬ (Q1 ) × . . . × Y¬ (Qm ))},
               where M ⊨ Pi , 1 ≤ i ≤ n and M ̸⊨ Qj , 1 ≤ j ≤ m
             Y¬ (¬P ) = Y(P )
             Y¬ (P ) = Y¬ (rewrite(P )), in all other cases
                ∪
             A × B = {a ∪ b | a ∈ A, b ∈ B}

Note that the requirement that the argument of Y is true in M but false in ML
means that in the atom case, the argument can only be L. Similarly for Y¬ where
the negation of an atomic argument must be L. Also, in the case for ∧ in Y¬ , we
could have n = 0 but must have m > 0 as the argument of Y¬ is always false.

Example 5. (Adapted from [10].) We give a simple theory for undirected graphs
where nodes are coloured either blue or red and are coloured blue iff they have at
most one neighbour. The universe is the set of nodes. The predicate neighbours
relates nodes which are connected by an edge. The set T consists of the formulæ

     ∀x.∀y.(neighbours(x, y) → neighbours(y, x))
     ∀n.(red (n) ↔ ¬blue(n))
     ∀n.(blue(n) ↔ ¬∃x.∃y.(neighbours(n, x) ∧ neighbours(n, y) ∧ x ̸= y))

   Let M = {neighbours(n0 , n1 ), neighbours(n1 , n0 ), blue(n0 ), blue(n1 )} with U =
{n0 , n1 }. Now, we ask why L = blue(n0 ) is true.

Y(T ) = {{¬red (n0 )}, {¬∃x.∃y.(neighbours(n0 , x) ∧ neighbours(n0 , y) ∧ x ̸= y))}

That is, there are two distinct reasons why n0 is blue. 1) it is not red and 2) it
has at most one neighbour.
                                                             Why does it fail ...     17

References

 1. Barrett, C., Tinelli, C.: Satisfiability modulo theories. In: Handbook of model
    checking, pp. 305–343. Springer (2018)
 2. Bjørner, D.: Domain modelling: A foundation for software development. In: The-
    ories of Programming and Formal Methods: Essays Dedicated to Jifeng He on
    the Occasion of His 80th Birthday, pp. 165–210. No. 14080 in Lecture Notes in
    Computer Science, Springer (2023)
 3. Codel, C., Fazekas, K., Heule, M.J.H., Iser, M. (eds.): Proceedings of SAT
    Competition 2025: Solver and Benchmark Descriptions. TU Wien (2025).
    https://doi.org/10.34726/10379
 4. Dougherty, D.J.: Model finding for exploration. In: Dougherty, D., Meseguer,
    J., Mödersheim, S.A., Rowe, P.D. (eds.) Protocols, Strands, and Logic - Es-
    says Dedicated to Joshua Guttman on the Occasion of his 66.66th Birthday.
    Lecture Notes in Computer Science, vol. 13066, pp. 156–174. Springer (2021).
    https://doi.org/10.1007/978-3-030-91631-2_9
 5. Eriksson, L.H.: Use of domain theories in applied formal methods. Tech.
    Rep. 2006-029, Uppsala University, Dept. of Information Technology (2006),
    https://www.diva-portal.org/smash/get/diva2:48912/FULLTEXT01.pdf
 6. Eriksson, L.H.: The GTO toolset and method. In: Proceedings of the 6th Inter-
    national Workshop on Automated Verification of Critical Systems (AVoCS 2006).
    Electronic Notes in Theoretical Computer Science. vol. 185, pp. 77–91. Elsevier
    (2007). https://doi.org/10.1016/j.entcs.2007.05.030
 7. Jackson, D.: Alloy: a language and tool for exploring software designs. Commun.
    ACM 62(9), 66–76 (2019). https://doi.org/10.1145/3338843
 8. Khan, T.A., Sullivan, A., Wang, K.: Alloyfl: a fault localization framework for
    Alloy. In: Proceedings of the 29th ACM Joint Meeting on European Software En-
    gineering Conference and Symposium on the Foundations of Software Engineering.
    pp. 1535–1539 (2021)
 9. Lichtenstein, O., Pnueli, A., Zuck, L.D.: The glory of the past. In: Parikh, R. (ed.)
    Logics of Programs, Conference, Brooklyn College, New York, NY, USA, June 17-
    19, 1985, Proceedings. Lecture Notes in Computer Science, vol. 193, pp. 196–218.
    Springer (1985). https://doi.org/10.1007/3-540-15648-8_16
10. Nelson, T., Danas, N., Dougherty, D.J., Krishnamurthi, S.: The power of “why”
    and “why not”: enriching scenario exploration with provenance. In: Bodden, E.,
    Schäfer, W., van Deursen, A., Zisman, A. (eds.) Proceedings of the 2017 11th Joint
    Meeting on Foundations of Software Engineering, ESEC/FSE 2017. pp. 106–116.
    ACM (2017). https://doi.org/10.1145/3106237.3106272
11. Penicka, M.: Towards a Theory of Railways. Ph.D. thesis, Czech Technical Univer-
    sity and Technical University of Denmark (2006)
12. Saadoun, R.: Implementation of Explanatory Algorithm for Logical Models. Bach-
    elor thesis, Uppsala University (2022)
13. Saghafi, S., Danas, R., Dougherty, D.J.: Exploring theories with a model-finding
    assistant. In: Felty, A.P., Middeldorp, A. (eds.) Automated Deduction - CADE-25 -
    25th International Conference on Automated Deduction, Berlin, Germany, August
    1-7, 2015, Proceedings. Lecture Notes in Computer Science, vol. 9195, pp. 434–449.
    Springer (2015). https://doi.org/10.1007/978-3-319-21401-6_30
14. Saghafi, S., Dougherty, D.J.: Razor: Provenance and exploration in model-
    finding. In: Schulz, S., de Moura, L., Konev, B. (eds.) 4th Workshop on
18      L.-H. Eriksson

    Practical Aspects of Automated Reasoning, PAAR@IJCAR 2014, Vienna, Aus-
    tria, 2014. EPiC Series in Computing, vol. 31, pp. 76–93. EasyChair (2014).
    https://doi.org/10.29007/TCVW
15. Siegel, M., Maggiore, A., Pichler, C.: Untwist your brain: efficient debugging and
    diagnosis of complex assertions. In: Proceedings of the 46th Annual Design Au-
    tomation Conference. p. 644–647. DAC ’09, Association for Computing Machinery,
    New York, NY, USA (2009). https://doi.org/10.1145/1629911.1630081
16. Wang, K., Sullivan, A., Marinov, D., Khurshid, S.: Fault localization for declar-
    ative models in Alloy. In: 2020 IEEE 31st International Symposium on Software
    Reliability Engineering (ISSRE). pp. 391–402. IEEE (2020)
17. Zheng, G., Nguyen, T., Brida, S.G., Regis, G., Frias, M.F., Aguirre, N., Bagheri,
    H.: Flack: Counterexample-guided fault localization for Alloy models. In: 2021
    IEEE/ACM 43rd International Conference on Software Engineering (ICSE). pp.
    637–648. IEEE (2021)
