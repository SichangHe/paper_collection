arXiv:1903.04159v1 [cs.SE] 11



                                       Towards Deriving Verification Properties

                                                                  Michael Winikoff

                                                                   March 12, 2019


                                1   Introduction

                                     “There are two key problems that occur in all such approaches: (1) what
                                     properties do we verify; and (2) where do the probabilities come from. The
                                     first of these remains a problem with all formal analysis techniques and,
                                     clearly, significant work must be done in capturing the requirements of the system
                                     in a formal and logical way.” [5] (emphasis added)
                                Formal software verification uses mathematical techniques to establish that software
                                has certain properties. For example, that the behaviour of a software system S sat-
                                isfies certain logically-specified properties. A common approach is model checking [2]
                                which takes a model of a system (M )) and a property φ (typically specified in some

                                                                             1
temporal logic), and can return either a guarantee that the behaviour of M satisfies φ,
or a counter-example: a possible behaviour of M that violates φ.
Formal methods have a long history [4, 3, 1] but, as suggested by the opening quote,
a recurring assumption is that the property φ is known, or provided as part of the
requirements elicitation process.
This working note considers the question: where does φ come from?
Our answer to this question is a pragmatic one: we define a process that can be used
to systematically identify a set of verification properties.
The high-level idea is that we start with a well-justified (and universal?) collection
of generic high-level properties (“tenets”) such as “do no harm”. We then systemat-
ically (but informally) derive contextualised more specific properties, using domain
knowledge and elements of the system’s design. These more specific properties cap-
ture the ways in which the specific system can violate the desired high-level proper-
ties.
For example, imagine a robot that assists an elderly person living in their home. One
high-level property (“tenet”) might be that the person should be kept safe (i.e. safe
from harm, and healthy). This high-level property clearly cannot be specified for-
mally. However, what we can do is carefully (and systematically) consider all the
ways in which the person could come to harm, given the context of the system and
its functionality, along with domain knowledge. This might allow us to (informally)
derive specific properties, such as that the person is accompanied if they leave the
house, and that they are reminded to take medication.

                                          2
We now define the high-level process in a little more detail. We assume (see Figure 1)
that a well-defined design process (A) is followed, which results in some design mod-
els (B), and that these are then refined and implemented (C), yielding code in some
appropriate programming language, such as a BDI (Belief-Desire-Intention) agent-
oriented programming language (D).
The process that we follow then takes as input high-level generic properties (“tenets”)
(E), as well as domain knowledge (F), and information about the design (B) and pos-
sibly even the implementation (D), and uses the domain and design information to
contextualise and refine (G) the high-level properties into more specific properties
(H). These specific properties and the software can be model checked. Note that this
process proceeds from informal to formal.
For the remainder of this document we make the following assumptions about the
specific forms of these different artefacts.
For the design model (B) we remain as agnostic as possible, and only assume some
form of goal model where goals are related to their sub-goals. This sort of model is
common to many AOSE methodologies [11].
For the implementation (D) we actually do not need to make any assumptions, as
long as (B) has a goal model. If it does not, then, if the implementation uses a notion
of goals, then we can extract a goal-tree from the implementation, shown as a dashed
line in Figure 1.
For the tenets (E), we assume simply English text. We do not believe that it is possible
to effectively formalise high-level notions such as “does no harm”, in fact, the whole

                                           3
     (A) Design            (B) Design                                  (D) BDI
                                               (C) Implement
      Process                Model                                  Implementation



    (E) Generic          (G) Refine &                                   Model
                                               (H) Properties
     properties          Contextualise                                 Checking



                          (F) Domain          Key:       Artifact        Process
                          Knowledge


                            Figure 1: High-level process

point of the process we propose, is to allow such properties to be captured formally
by making them more specific in the context of the system at hand.
Domain knowledge (F) could be represented in a number of ways. We assume (fol-
lowing [10]) that it is represented as a collection of implications. However, we could
also explore using a graphical model instead of logical formulae. Note that domain
knowledge is also refined and extended as part of the process (G), indicated by the
bi-directional arrow between (G) and (F).



                                          4
Properties to be verified (H) are logical formulae. A wide range of logics could be
used, but for the present paper we simply assume Linear Temporal Logic (LTL). Other
richer logics could be used, but there is the standard trade-off that the richer the logic,
the harder verification becomes.
The remainder of this document provides a sketch for a possible process, illustrated
using a running example. This process is an early sketch, and is intended as a starting
point for discussion and refinement.
Before proceeding further, it is worth briefly mentioning a key paper that informs this
work.
The process of deriving ways in which a tenet could be compromised has similari-
ties with a 2000 paper by van Lamsweerde and Letier (henceforth “vLL”) [10]. Very
briefly, they begin with leaf goals (i.e. requirements, which are formalised in logic),
and derive obstacles to these requirements, using domain knowledge.
Although the starting point is different, a formally specified system goal in their ap-
proach vs. an informal generic tenet in ours, the general idea of deriving a more de-
tailed obstacle for the starting point, by using domain knowledge, is similar. Note
that sometimes the derivation of obstacles in their method uses not domain knowl-
edge, but a general pattern that a goal G can go wrong by not being done at all, or by
being done wrongly, where “done wrongly” can refer to any aspect of the goal. So, for
example, if the goal is to send a message, then it could go wrong by the message not
being sent, or it could be sent to the wrong recipient, or sent with incorrect contents.
One difference, is that whereas they start with a specific goal, we start with a high-

                                            5
level tenet. This is because the tenets are what we care about and want to ensure,
whereas not all goals are important. For example, in a home-care robot scenario,
checking that the fridge is not left open is not that important, whereas ensuring that
the person being cared for is reminded to take their medication is very important.



2    Artefacts

This section briefly describes the artefacts that play a role in the process. As depicted
in Figure 1, the process (G) involves tenets (E), a design model, specifically a goal
tree (B), and domain knowledge (F). It results in formally specified properties to be
verified (H).
We have already noted that the tenets (E) are simply high-level and generic state-
ments in English, for example “do not harm humans”, or “ensure the system is able
to continue to function”.
We have also already noted that the formulae to be verified (H) are specified in Linear
Temporal Logic (LTL), but that other logics are also possible.
We now turn our attention to the goal tree (B) and domain knowledge (F). We also
define an intermediate data structure: the refinement tree (see Section 2.3). Figure 2
shows the process, along with the key artefacts.




                                           6
                            (B) Design Model
                                (goal tree)




       (E) Tenets             (G) Detailed                                           (H) Properties
                                                        Refinement Tree
        (English)               Process                                                  (LTL)



                               (F) Domain
                            Knowledge (logical
                              implications)


                                Figure 2: Zooming in on step G

2.1    Goal Tree

The design model that we use is a goal tree (see example in Figure 3). This is a
tree1 where nodes are (sub-)goals, and arrows link goals to their sub-goals. The rela-
tionship of a goal to its children is indicated as being either “AND” or “OR” (in the
example in Figure 3 all the relationships are “AND”). Such trees can be constructed
and refined by asking “Why?” to identify parents of goals, and asking “How?” to
   1
   More precisely a directed acyclic graph, since a sub-goal can be reused, i.e. it can be the child of
multiple parents.


                                                  7
identify children of goals [9, 6]. Such trees are commonly used in methodologies for
engineering autonomous systems [11].
The tree in Figure 3 relates to a Care-O-bot scenario [7]. This scenario involves a
robot in the home of an elderly person. The robot reminds the person to eat, drink,
and take their medication, is able to monitor them and alert medical authorities if
required, and also performs a range of other support tasks (e.g. checking if the fridge
door is left open, watching TV together, following orders to fetch items, answering
the door).


                                                     Support
 Why?


 How?                   Keep                                                              8:
                                                 Keep Safe                   Assist
                       Healthy                                                         Recharge


   1: Remind   2: Remind   3: Remind                               5:      6: Follow   7: Remind
                                           4: Monitor
      to Eat    to Drink   Medication                          Accompany    Orders       Fridge

                                       4a:
                                                     4b: Critical
                                    Behaviour


                                 Figure 3: Example Goal Tree




                                                 8
2.2   Domain Knowledge

The third artefact is domain knowledge which we model as implications in a suitable
logic (for example, LTL, following vLL).
One example domain knowledge rule captures that issuing reminders (e.g. to take
medication) tends to lead to the task in question being done. This is actually diffi-
cult to formalise precisely, since the reminders do not actually guarantee compliance.
For simplicity we formalise the overly-strong property that reminding will ensure
compliance:
                                 2(remind (X) → do(X))                             (1)
Of course, this is too strong, and a more nuanced formalisation might involve a logic
with probabilities, allowing one to capture that reminders reduce the probability of
forgetting, while not eliminating it entirely.
Conversely, we may also know that reminders have value because the person being
cared for is forgetful, and is more likely to remember to perform a task if they are
reminded. Again, a correct formalisation would require probabilities, but for now we
formalise using an overly strong property that reminders are necessary (i.e. without
reminders, the person will forget):
                             2(¬remind (X) → ¬do(X))                               (2)
(of course, we could simply have written the earlier property using ↔)
Note: For convenience, we adopt the convention (used by vLL) that A ⇒ B is nota-
tional shorthand for 2(A → B), which allows us to write the first domain knowledge

                                          9
above as simply reminder (X) ⇒ do(X).
Other examples of domain knowledge include defining high-level concepts, e.g. that
“not getting enough food” means having fewer than three meals a day (and obviously
there need to be conditions on what those meals are), and that “not drinking enough”
is less than around 1.2 litres per day. We use “≡” to define such equivalences, which
logically is treated as bidirectional implication.

        not enough food     ≡    <3 meals a day                                  (3)
       not enough drink     ≡    <1.2L/day                                       (4)
   accompany excursion      ≡    follow or delegate-by-informing                 (5)
            keep healthy    ⇒    enough food ∧ enough drink ∧ correct medication (6)
              <1.2L/day     ≡    ¬(do(drinkregularly))                           (7)
      correct medication    ≡    issued = prescribed                             (8)
         <3 meals a day     ≡    ¬(do(breakfast) ∧ do(lunch) ∧ do(dinner ))      (9)

Additionally, note that the goal tree can be seen as specifying implied domain knowl-
edge, for instance if a goal G0 has a child goal G1 then this indicates that G1 is part of
achieving G0 . However, in the detailed process presented below, we keep the goal-
tree distinct, rather than mapping it to domain knowledge rules.




                                           10
2.3   Refinement Tree

The artefacts discussed so far are the inputs to the process. The process uses, and
potentially modifies, these to progressively generate a refinement tree. This is an
intermediate artefact (hence shown dashed in Figure 2) that captures the process of
refining the tenet. In practice, this tree is valuable for traceability. However, it is not
required: we could equally well work with just a set of nodes (the frontier of the
refinement tree).
The root of a refinement tree is a tenet, and, once the process is completed, its leaves
are each an LTL property. Each node in the refinement tree is a description (formal or
informal) of a set of behaviours. That is, the node specifies a subset of the possible be-
haviours of the system. The subset of behaviours is described in terms of a condition,
which, since it can be instantaneous, or over a time period, is formalised (eventually)
in LTL.
The relationship between a node and its children is implication: if node B is a child
of node A, then that means that any behaviour that satisfies B will also satisfy A. So,
for example, given a node “not enough food”, with a child node “<3 meals a day”,
this implication holds. Since having less than 3 meals a day is (according to domain
knowledge Equation 3) the definition of not having enough food, any behaviour that
meets the condition of not having 3 meals a day, by definition also meets the condition
of not having enough food. Similarly, consider a node “harm” with two child nodes:
“not kept healthy” and “put at risk”. A behaviour that satisfies one of these, by either
not keeping the person healthy or by putting them at risk, also is considered to be


                                            11
meeting the definition of causing them harm2 .



3        Process

The basic idea is that we start with a negated tenet. For example, if we want to “not
harm a person”, then we begin with “harming a person” and then consider how this
could occur in the current context (i.e. with respect to the domain knowledge and
system at hand), this is done by asking questions such as:
        • “What goals contribute to/against this tenet?”
        • “How (in this context) could this tenet be violated?”
        • “What does this mean (in this context)?”
This process is iterated until all leaf nodes are formalised. The results (the leaf nodes)
are negated, yielding a collection of properties to be checked. It is also possible to use
obstacle derivation a la vLL to explore the assumptions underlying the achievement
of these properties.
    2
    Note that in this example we are considering putting a person at risk of coming to harm, in a
situation where the system cannot prevent the harm, as being equivalent to actually causing harm,
even though the person might be lucky and not come to harm, despite being put at risk. For instance,
a young child crossing a busy road may not come to harm, but we consider preventing this situation
part of keeping them safe.



                                                12
In essence, the process takes a negated tenet, and derives a collection of properties,
such that each of the properties, if it holds, implies the negation of the tenet. There-
fore, in order for the desired tenet to hold, the negation of each of the properties must
hold. For example, given the tenet that we want to avoid harm to the human, we
might derive a collection of (formally specified) properties that include that we re-
mind the elderly person to eat their lunch, and that we ensure that the medication
they take match what is prescribed.
At a high level, the detailed process is as follows (where the numbers on the left mark
different cases, discussed below):
    Initialise root node N with the negation of a tenet
    Repeat until all leaves of refinement tree are formalised
         Select a leaf node N
    0. If N can be formalised then formalise it
    1. Elseif can refine N using domain knowledge then do so (see Section 3.2)
    2. Elseif can refine N using the goal tree then do so (see Section 3.3)
    3. Else
    3a.      If can refine the goal tree by adding relevant goals
                       then do so (see Section 3.4)
    3b.      Else elicit additional relevant domain knowledge (see Section 3.5)
    EndRepeat
    Return the negations of leaf nodes
We now consider the different cases. The “base case” is when the node is specific
enough that it can be directly formalised (case 0), in which case we simply formalise

                                           13
the node. The other cases are: refining using domain knowledge (1), using the goal
tree (2), and expanding either the goal tree (3a) or domain knowledge (3b). Note that
in a situation where a node N can be refined by applying either domain knowledge
or the knowledge implied by the goal-tree, then the process prioritises the domain
knowledge, since it is more general (associated with the problem and the domain),
whereas the goal-tree is more specific (associated with a particular solution).


3.1   Formalisation (case 0)

If the node’s (informal) description is sufficiently specific that it can be directly for-
malised, then we refine the node, replacing it with a node containing an LTL formula.
Writing a formula may require some attention to the implementation, what infor-
mation can be monitored, and in what (logical) form it is provided. For example, in
issuing medicine, the implementation (i.e. the agent’s beliefs) may provide predicates
such as issued (M ) indicating that medication M was issued, and this predicate would
be used in formalising a node specifying that correct medication was issued. On the
other hand, if the belief used was, say, medicationIssued (M, P, D, T ), indicating that
medication M was issued to patient P on day D and time T , then this predicate would
need to be used instead.
We assume that formalisation is possible in the following cases in our running exam-
ple. Some of the formalisations below could be improved to be made more precise.
For example, instead of emergency ⇒ alerted we might require that should an emer-


                                           14
gency occur, an alert is sent within a certain time window.
We also assume the obvious compositional property, that a compound formula (e.g. a
conjunction, or negation) can be formalised exactly when its sub-formulae can be
formalised.

              Informal Text                  Corresponding Formalisation
                remind(X)                                 Φ(X)
 (where X ∈ {breakfast, lunch, dinner})
         remind(drinkregularly)                             Ψ
           issued 6= prescribed         3(issued(M ) ∧ prescribed(M 0 ) ∧ M 6= M 0 )
    follow ∨ delegate-by-informing             leave ⇒ (follow ∨ inform)
        monitor critical incident                 emergency ⇒ alerted
            monitor behaviour                    deteriorated ⇒ alerted
               out of charge                          3charge = 0
                   obey                         request(X ) ⇒ 3done(X)

Where we define Φ(X) (when X is a meal), as being true if, at the time of that meal,
either the person is eating, or the system is about to issue a reminder:

                 Φ(X) ≡ 2(time(X) → (eating(X) ∨ eremind (X)))

We also define Ψ as being true if the system regularly reminds the person to drink.
Specifically, Ψ holds if, whenever it has been more than 2 hours (“2h”) since the last
drink, either the system has issued a reminder within the last 15 minutes (“<15m ”),

                                         15
or the system is about to issue a reminder. In other words, if the person has not had
a drink within the past two hours, then reminders are issued every 15 minutes (until
they drink).

Ψ ≡ 2(lastDrink (T )∧now (T 0 )∧T 0 > T +2h → (<15m remind (drink )∨ eremind (drink )))


3.2    Refining with respect to Domain Knowledge (case 1)

When refining with respect to domain knowledge, we follow vLL’s process: given a
domain knowledge rule of the form 2(A → P 0 ), and a node N containing P (where P
is in a positive context, and ∃θ.P θ = P 0 θ), then we refine N with3 N [P/Aθ] (i.e. replace
P with Aθ). This gives us the desired relationship between a node and its child: if
A → P then N [P/A] → N .
Similarly, if P occurs in a negative context (i.e. within the scope of an odd number of
negations), then the rule 2(P → A) can be applied to replace P with A, which gives
the desired implication relationship: since P → A we have (¬A) → (¬P ) and hence
(¬N [P/A]) → (¬N ) as desired.
Note that in either case, if the new node is of the form ¬(N1 ∧ . . . ∧ Ni ) then we break it
into multiple nodes ¬Ni . For example, we can use the domain knowledge that keep-
ing someone healthy means (Equation 6) that they have enough food, enough drink,
   3
    The notation N [A/B] denotes the result obtained by taking N , and replacing the sub-expression A
with B.


                                                 16
and correct medication. When we refine the node ¬keep healthy then we replace
it with the node ¬(enough food ∧ enough drink ∧ correct medication), which is then
broken into three nodes.
Note that if the domain knowledge is in the form of a definition (P 0 ≡ A), then, given
P θ = P 0 θ, we can replace P with Aθ in any context. Note that this rule could be
applied repeatedly giving a loop, by replacing A with P . We avoid this by assuming
that definitions are directional: defining something in terms of something else more
specific, and that the human following the process only goes in the direction of in-
creasing specificity. For example, it would make sense to refine “not enough food” to
“<3 meals a day”, but not the reverse.
However, what we want to identify as a result of this whole process is not just some
ways in which the underlying tenet (e.g. “no harm”) can be violated, but all ways in
which it can be violated. Therefore, when refining, we consider not just one domain
rule of the form 2(X → Y ), but all such rules.
Specifically, after refining we ask the question: “is this complete?”. Specifically, given
a node N , and its refinements N1 . . . Ni , the refinements are complete if (following
vLL) (¬N1 ∧ . . . ∧ ¬Ni ) → ¬N . Of course, since nodes being refined have not yet been
formalised, this cannot be checked formally, but informally, using the question4 : “if
all of these refinements fail to hold, does the original node also necessarily fail to hold?”.
For example, when refining “not kept healthy”, we refine it into the three sub-nodes:
“not enough food”, “not enough drink”, and “no/wrong medication”. We then con-
  4
      Note that if the domain knowledge rule used is of the form A ≡ P 0 then by definition it is complete.


                                                    17
sider the question: “is enough food, enough drink, and correct medication sufficient to guar-
antee good health?”. In this case we might consider that the answer is “no”, because
health also requires exercise, and attention to psychological well-being (e.g. compan-
ionship, social activities, and a sense of meaning). These additional nodes could be
added (not shown in Figure 5) and further elaborated.


3.3      Refining with respect to Goals (case 2)

When refining with respect to goals we derive the process by considering the goal-
tree as specifying “implied” domain knowledge. In essence, a goal-subgoal relation-
ship of the form G0 −→ G1 (i.e. G1 is a sub-goal of G0 ), is read as implying domain
knowledge that bringing about G1 implies G0 . In the case where G0 has multiple chil-
dren, then when the decomposition is OR each child implies the parent, and when
the decomposition is AND then the conjunction of all the children implies the parent.
If the (parent) goal G appears in the node N in a positive context (i.e. it is not in the
scope of a negation5 ), then we simply use this domain knowledge. Specifically, we
use the implied knowledge of the form X → G to create a refined node N [G/X].
There are two sub-cases: if G is OR-refined, then the implied domain knowledge
consists of rules Gi → G for each child of G in the goal tree. In this case, we collect the
rule applications, giving us multiple children of N , each of the form N [G/Gi ]. In the
second case, where G is AND-refined in the goal-tree, we create a single child of N :
  5
      Or, more precisely, it is in the scope of an even number of negations.



                                                     18
     V
N [G/ i Gi ]. Note that if G only has a single child, then both sub-cases are equivalent:
we add a refined node N [G/G1 ].
For example, given a node keep safe we can refine it using the goal-tree. Recall
(Figure 3) that the goal “keep safe” has two (AND-refined) sub-goals (“monitor”
and “accompany”). Therefore, we have implied domain knowledge that (monitor ∧
accompany) → keep safe. This can be applied, in a similar way to other domain
knowledge, to refine keep safe to monitor ∧ accompany.
However, what can we do if the node is actually negated, e.g. ¬keep safe? In this
case we need to consider strengthening the goal-tree.
The domain knowledge that we need to refine the node N into more specific sub-
nodes is now of the form ¬C → ¬G (where “C” denotes an appropriate logical formula
combining G’s children). However, this is not what the goal-tree implies, it implies
C → G and hence ¬G → ¬C. In order to be able to use the goal-tree in this situation,
we need to consider cases where the goal decomposition in the goal tree is essential,
that is, where the decomposition of G into C is such that not only does C imply G, but
it is actually necessary not just sufficient, so that we have G ↔ C. Then, if G appears
in a negative context in the node N then we use the implied knowledge of the form
G → C.
There are two cases. If G is OR-refined, then we have G → (G1 ∨ . . . ∨ Gi ) and hence
¬(G1 ∨. . .∨Gi ) → (¬G) and we replace G (in a negative context in N ) with G1 ∨. . .∨Gi .
The second case is when G is AND-refined, in which case we have G → (G1 ∧. . .∧Gi ),
hence ¬(G1 ∧ . . . ∧ Gi ) → (¬G) and we replace G (in a negative context in N ) with


                                           19
G1 ∧ . . . ∧ Gi , which can be split into multiple sub-nodes Ni = N [G/Gi ].
For the example goal-plan tree we assume that this strengthened relationship holds
for each of the following nodes and their children: monitor, keep safe, and ¬harm
(also shown as bold labels in shaded nodes in Figure 4). So, for the example we
would be able to refine ¬keep safe into two nodes: ¬accompany, and ¬monitor.
Finally, for the “G appears in a negative context in N ” case, there is one special case
to consider, where instead of N = ¬G, we have ¬N = G, i.e. instead of G appearing
in N , actually N appears in G. In this case we apply the same logic as the other
negative cases, but, because G doesn’t actually appear in N (and N isn’t necessarily
a negation), we cannot just replace N with N [G/ . . .]. Instead, we replace N with ¬G
where G is the appropriate logical combination of the children of G. For example, if G
has a single child, G1 , then the implied domain knowledge (assuming a strengthened
relationship) is G → G1 and hence (¬G1 ) → (¬G). We then have that N is implied by
(and hence can be replaced by) ¬G1 , because (¬G1 ) → (¬G) and ¬G = ¬¬N ≡ N .
These cases are summarised in the following table. Note that when refining, we want
to make things more specific, so we always refine a goal in terms of its children, rather
than its parent.




                                           20
 Goal Tree          Implied Domain Knowledge           N        N0
 G −→ OR(G1 , G2 )  Gi → G                             N [G]    {N [G1 ], N [G2 ]}
 G −→ AND(G1 , G2 ) (G1 ∧ G2 ) → G                     N [G]    N [G1 ∧ G2 ]
 G ←→ OR(G1 , G2 )  G → (G1 ∨ G2 )
                     ∴ ¬(G1 ∨ G2 ) → ¬G                ¬N [G] ¬N [G1 ∨ G2 ]
 G ←→ AND(G1 , G2 ) G → (G1 ∧ G2 )
                     ∴ ¬(G1 ∧ G2 ) → ¬G
                     ∴ ((¬G1 ) ∨ (¬G2 )) → ¬G          ¬N [G] {¬N [G1 ], ¬N [G2 ]}
 G ←→ OR(G1 , G2 )  G → (G1 ∨ G2 )                          (where G = ¬N )
                     ∴ ¬(G1 ∨ G2 ) → ¬G                N       ¬(G1 ∨ G2 )
 G ←→ AND(G1 , G2 ) G → (G1 ∧ G2 )                          (where G = ¬N )
                     ∴ ¬(G1 ∧ G2 ) → ¬G
                     ∴ ((¬G1 ) ∨ (¬G2 )) → ¬G          N        {¬G1 , ¬G2 }


3.4   Expanding the Goal Tree (case 3a)

There is one slight complication when refining with respect to goals. This is a sit-
uation where the goal-tree is “missing” a goal. That is, where instead of having
G −→ G1 (G1 has G as a parent), G1 has a different, more general, parent goal. For
instance, in the goal-tree of Figure 3 the two goals “Keep Healthy” and “Keep Safe”
have as their parent the (more general) goal “Support”, rather than a more specific
goal “Keep from harm”. This means that if the refinement tree has a node relating to
harming someone, then we cannot use the goal tree to refine the node.


                                        21
In this situation, where we might want to use the child goals to refine nodes, we may
need to conceptually consider additional “phantom” nodes in the goal-tree. This is
done by adding intermediate nodes to the tree, as illustrated below.

                      Support



   Keep                                        8:
              Keep Safe         Assist
  Healthy                                   Recharge           Support


                                               Don't Harm                            8:
                                                                         Assist
                                                                                  Recharge
                                          Keep
                                                       Keep Safe
                                         Healthy

The resulting goal-tree is shown in Figure 4 (on page 23). It adds an intermediate
node “¬harm”.


3.5   Expanding the Domain Knowledge (case 3b)

Finally, if neither case applies, then we can proceed by expanding domain knowledge.
This is done by considering the node and asking “how can this occur?”, or “what does
this mean?” (specifically: “what counts as this node?”). The new domain knowledge
can then be used to continue the process.


                                             22
                                                                                    support




                                                ¬harm                                                          assist       recharge




                        keep healthy                                        keep safe          follow orders            remind fridge




     remind to eat   remind to drink   remind medication        monitor            accompany excursion




                                            monitor behaviour             monitor critical incident



Figure 4: Revised Example Goal Tree (bold shaded nodes indicate ones with strength-
ened relationship to their children)




                                                           23
4        Results

For the running example, starting with the high-level tenet “do not harm”, the given
goal tree, and the domain knowledge, following the process might6 yield the refine-
ment tree shown in Figure 5. Annotations in the tree of the form “dn” indicate that
the node was refined using domain knowledge rule n. An annotation of “g” indicates
that the goal tree was used, and “f” indicates that the node was able to be formalised.

                                                                                                     ¬do(breakfast):d2   ¬remind(breakfast):f     ¬Φbreakfast
                                                                               ¬do(breakfast)
                                    ¬enough food:d3     <3 meals a day:d9       ∧do(lunch)           ¬do(lunch):d2       ¬remind(lunch):f    ¬Φlunch
                                                                               ∧do(dinner):d2
                                                                                                     ¬do(dinner):d2      ¬remind(dinner):f      ¬Φdinner
                 ¬keep healthy:d6
                                    ¬enough drink:d4     <1.2L/day:d7          ¬do(drinkregularly):d2     ¬remind(drinkregularly):f   ¬Ψ

                                    ¬correct medication:d8    issued 6= prescribed:f   3(issued(m)∧prescribed(mp)∧neq(m,mp))
harm:g
                                                       ¬monitor behaviour:f      ¬ (deteriorated⇒alerted)
                                    ¬monitor:g
                                                       ¬monitor critical incident:f    ¬ (emergency⇒alerted)
                 ¬keep safe:g
                                    ¬accompany excursion:d5     ¬follow or delegate-by-informing:f      ¬ (leave⇒follow∨inform)



                           Figure 5: Refinement Tree for Tenet “do not harm”

This figure shows a process that began with the root node “harm” (the negated tenet),
and was then refined by considering the goal-tree, where the goals “keep healthy”
and “keep safe” both interfere with the negated tenet (and where the goal tree had
been refined to create a “do not harm” parent to these goals).
    6
        Since the process is a design process, followed by humans, it is not deterministic.


                                                                        24
Each of these goals is then refined by eliciting additional domain knowledge and ap-
plying that. Specifically, that being healthy involves having enough to eat, enough to
drink, and taking medication; and that being safe involves ensuring adequate moni-
toring when leaving the house, and adequate monitoring to detect any health emer-
gencies or accidents.
We then further refine these nodes with (existing) domain knowledge. For instance,
that “not enough food” means fewer than three meals a day. We also use domain
knowledge that ensuring (e.g.) three meals a day can be achieved by issuing appro-
priate reminders. Then, since this is sufficiently specific, we formalise this. Similarly,
we can refine not having enough drink to drinking regularly, and formalise it in terms
of reminders.
Then we can take the negated leaf nodes of the refinement tree, which gives us the
following formulae for verification:

                           Φ(breakfast), Φ(lunch), Φ(dinner )

2(lastDrink (T ) ∧ now (T 0 ) ∧ T 0 > T + 2h → (<15m remind (drink ) ∨ eremind (drink )))
                      2(issued (M ) ∧ prescribed (M 0 )) → M = M 0
                             2(leave → (follow ∨ inform))
                                 2emergency → alerted
                                2deteriorated → alerted
where Φ(X) ≡ 2(time(X) → (eating(X) ∨ eremind (X)))

                                           25
5    Next Steps

This working note presented a high-level process that can be used by a human de-
signer to systematically identify a set of verification properties.
However, there is still much work to be done. In particular, we need to find answers
to the following questions:
    • Can this process be used in practice by designers (other than the author of this
      paper)?
    • Can this process be used for a wider range of examples, including larger and
      more complicated ones?
    • How effective is this process at identifying important properties to be verified?
    • How can this process be supported by tools?
Other areas for future work include: richer representation (e.g. logic with probabil-
ities, other design models, graphical model for domain knowledge); priorities be-
tween tenets, perhaps linking to ideas on human values (e.g. [8]); and dealing with
conflict between goals, for instance in the running example we want the system to
obey the user, but what if the user asks the system to stop issuing reminder to drink?




                                          26
References

[1] R.S. Boyer and J.S. Moore, editors. The Correctness Problem in Computer Science.
    Academic Press, London, 1981.
[2] E.M. Clarke, O. Grumberg, and D.A. Peled, editors. Model Checking. The MIT
    Press, 2000.
[3] R.A. DeMillo, R.J. Lipton, and A.J. Perlis. Social processes and proofs of theo-
    rems of programs. ACM Communications, 22(5):271–280, 1979.
[4] J.H. Fetzer. Program verification: The very idea.        ACM Communications,
    31(9):1048–1063, 1988.
[5] Savas Konur, Michael Fisher, Simon Dobson, and Stephen Knox. Formal verifi-
    cation of a pervasive messaging system. Formal Aspects of Computing, 26(4):677–
    694, 2014. doi:10.1007/s00165-013-0277-4.
[6] Lin Padgham and Michael Winikoff. Developing intelligent agent systems: A prac-
    tical guide. John Wiley & Sons, Chichester, 2004. ISBN 0-470-86120-7.
[7] Ulrich Reiser, Christian Pascal Connette, Jan Fischer, Jens Kubacki, Alexander
    Bubeck, Florian Weisshardt, Theo Jacobs, Christopher Parlitz, Martin Hägele,
    and Alexander Verl. Care-o-bot R 3 - creating a product vision for service
    robot applications by integrating design and technology. In IEEE/RSJ Interna-
    tional Conference on Intelligent Robots and Systems, pages 1992–1998. IEEE, 2009.
    doi:10.1109/IROS.2009.5354526.


                                        27
 [8] SH Schwartz. An Overview of the Schwartz Theory of Basic Values. Online
     Readings in Psychology and Culture, 2(1), 2012. doi:10.9707/2307-0919.1116.
 [9] A. van Lamsweerde. Goal-Oriented Requirements Engineering: A Guided Tour.
     In Proceedings of the 5th IEEE International Symposium on Requirements Engineering
     (RE’01), pages 249–263, Toronto, August 2001.
[10] Axel van Lamsweerde and Emmanuel Letier. Handling Obstacles in Goal-
     Oriented Requirements Engineering. IEEE Trans. Software Eng., 26(10):978–1005,
     2000. doi:10.1109/32.879820.
[11] Michael Winikoff and Lin Padgham. Agent Oriented Software Engineering. In
     Gerhard Weiß, editor, Multiagent Systems, chapter 15, pages 695–757. MIT Press,
     2 edition, 2013.




                                          28
