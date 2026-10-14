                                               Probabilistic Rely-guarantee Calculus


                                             Annabelle McIver a Tahiry Rabehaja a Georg Struth b
                                                  a Department of Computing, Macquarie University, Australia

                                           b Department of Computer Science, University of Sheffield, United Kingdom
arXiv:1409.0582v3 [cs.LO] 2 Jun 2015




                                       Abstract

                                       Jones’ rely-guarantee calculus for shared variable concurrency is extended to include
                                       probabilistic behaviours. We use an algebraic approach that is based on a combina-
                                       tion of probabilistic Kleene algebra with concurrent Kleene algebra. Soundness of
                                       the algebra is shown relative to a general probabilistic event structure semantics.
                                       The main contribution of this paper is a collection of rely-guarantee rules built on
                                       top of that semantics. In particular, we show how to obtain bounds on probabili-
                                       ties of correctness by deriving quantitative extensions of rely-guarantee rules. The
                                       use of these rules is illustrated by a detailed verification of a simple probabilistic
                                       concurrent program: a faulty Eratosthenes sieve.

                                       Key words: probabilistic programs, concurrency, rely-guarantee, program
                                       verification, program semantics, Kleene algebra, event structures.




                                       1   Introduction


                                       The rigorous study of concurrent systems remains a difficult task due to the
                                       intricate interactions and interferences between their components. A formal
                                       framework for concurrent systems ultimately depends on the kind of con-
                                       currency considered. Jones’ rely-guarantee calculus provides a mathematical
                                       foundation for proving the correctness of programs with shared variables con-
                                       currencyin compositional fashion [1]. This paper extends Jones’ calculus to
                                       the quantitative correctness of probabilistic concurrent programs.

                                         This research was supported by an iMQRES from Macquarie University, the ARC
                                       Discovery Grant DP1092464 and the EPSRC Grant EP/J003727/1.
                                         Email addresses: annabelle.mciver@mq.edu.au (Annabelle McIver),
                                       tahiry.rabehaja@mq.edu.au (Tahiry Rabehaja), g.struth@sheffield.ac.uk
                                       (Georg Struth).


                                       Preprint submitted to Elsevier                                       28 August 2018
Probabilistic programs have become popular due to their ability to express
quantitative rather than limited qualitative properties. Probabilities are par-
ticularly important for protocols that rely on the unpredictability of proba-
bilistic choices. The sequential probabilistic semantics, originating with Kozen [2]
and Jones [3], have been extended with nondeterminism [4,5], to yield methods
for quantitative reasoning based on partial orders.

We aim to obtain similar methods for reasoning in compositional ways about
probabilistic programs with shared variable concurrency. In algebraic approaches,
compositionality arises quite naturally through congruence or monotonicity
properties of algebraic operations such as sequential and concurrent composi-
tion or probabilistic choice.

It is well known that compositional reasoning is nontrivial both for concurrent
and for sequential probabilistic systems. In the concurrent case, the obvious
source of non-compositionality is communication or interaction between com-
ponents. In the rely-guarantee approach, interference conditions are imposed
between individual components and their environment in order to achieve com-
positionality. Rely conditions account for the global effect of the environment’s
interference with a component; guarantee conditions express the effect of a
particular component on the environment. Compositionality is then obtained
by considering rely conditions within components and guarantee conditions
within the environment.

In the presence of probabilistic behaviours, a problem of congruence (and
hence non-compositionality) arises when considering the natural extension of
trace-based semantics to probabilistic automata [6], where a standard work-
around is to define a partial order based on simulations.

In this paper, we define a similar construct to achieve compositionality. How-
ever, simulation-based equivalences are usually too discriminating for pro-
gram verification. Therefore, we also use a weaker semantics that is essen-
tially based on sequential behaviours. Such a technique has been motivated
elsewhere [7], where the sequential order is usually not a congruence. There-
fore, the simulation-based order is used for properties requiring composition
while the second order provides a tool that captures the sequential behaviours
of the system.

Concurrent Kleene algebra [8,7] provides an algebraic account of Jones’ rely-
guarantee framework. Algebras provide an abstract view of a program by
focusing more on control flows rather than data flows. All the rely-guarantee
rules described in [8,7] were derived by equational reasoning from a finite set
of algebraic axioms. Often, the verification of these axioms on an intended
semantics is easier than proving the inference rules directly in that semantics.
Moreover, every structure satisfying these laws will automatically incorporate


                                       2
a direct interpretation of the rely-guarantee rules, as well as additional rules
that can be used for program refinement. Therefore, we also adopt an algebraic
approach to the quantitative extension of rely-guarantee, that is, we establish
some basic algebraic properties of a concrete event structure model and derive
the rely-guarantee rules by algebraic reasoning.

In summary, the main contribution of this paper is the development of a math-
ematical foundation for probabilistic rely-guarantee calculi. The inference rules
are expressed algebraically, and we illustrate their use on an example based on
the Sieve of Eratosthenes which incorporates a probability of failure. We also
outline two rules that provide probabilistic lower bounds for the correctness
of the concurrent execution of multiple components.

A short summary of the algebraic approach to rely-guarantee calculus and the
extension to probabilistic programs are found respectively in Section 2 and 5-
6. Section 3 and 4 are devoted to the construction of a denotational model for
probabilistic concurrent programs. Section 7 closes this paper with a detailed
verification of the faulty Eratosthenes sieve.



2   Non-probabilistic rely-guarantee calculus


The rely-guarantee approach, originally put forward by Jones [1], is a com-
positional method for developing and verifying large concurrent systems. An
algebraic formulation of the approach has been proposed recently in the con-
text of concurrent Kleene algebras [8]. In a nutshell, a bi-Kleene algebra is an
algebraic structure (K, +, ·, k, 0, 1,∗ ,(∗) ) such that (K, +, ·, 0, 1,∗ ) is a Kleene
algebra and (K, +, k, 0, 1,(∗) ) is a commutative Kleene algebra. The axioms of
Kleene algebra and related structures are in Appendix A .

Intuitively, the set K models the actions a system can take; the operation
(+) corresponds to the nondeterministic choice between actions, (·) to their
sequential composition and (k) to their parallel or concurrent composition.
The constant 0, the unit of addition, models the abortive action, 1, the unit of
sequential and concurrent composition, the ineffective action skip. The oper-
ation (∗ ) is a sequential finite iteration of actions; the corresponding parallel
finite iteration operation ((∗) ) is not considered further in this article. Two
standard models of bi-Kleene algebras are languages, with (+) interpreted as
language union, (·) as language product, (k) as shuffle product, 0 as the empty
language, 1 as the empty word language and (∗ ) as the Kleene star, and pomset
languages under operations similarly to those in Section 4.3 below (cf. [9]).

Language-style models with interleaving or shuffle also form the standard se-
mantics of rely-guarantee calculi. In that context, traces are typically of the


                                          3
form (s1 , s01 ), (s2 , s02 ) . . . (sk , s0k ), where the si and s0i denote states of a system,
pairs (si , s0i ) correspond to internal transitions of a component, and fragments
s0i ), (si+1 to transitions caused by interferences of the environment. Behaviours
of a concurrent system are associated with sets of such traces.

With semantics for concurrency in mind, a generalised encoding of the validity
of Hoare triples becomes useful:

                                 {P }S{Q} ⇔ P ·S ≤ Q,

where P ≤ Q ⇔ P ∪Q = Q. It has been proposed originally by Tarlecki [10]
for sequential programs with a relational semantics. In contrast to Hoare’s
standard approach, where P and Q are assertions and S a program, all three
elements are now allowed to be programs. In the context of traces, {P }S{Q}
holds if all traces that are initially in P and then in S are also in Q. This
comprises situations where program P models traces ending in a set of states
p (a precondition) and Q models traces ending in a set of states q (a postcondi-
tion). The Hoare triple then holds if all traces establishing precondition p can
be extended by program S to traces establishing postcondition q, whenever
y terminates, as in the standard interpretation. We freely write {p}S{q} in
such cases. It turns out that all the inference rules of Hoare logic except the
assignment rule can be derived in the setting of Kleene algebra [8].

For concurrency applications, the algebraic encoding of Hoare triples has been
expanded to Jones quintuples {P R}S{G Q}, also written R, G ` {P }S{Q},
with respect to rely conditions R and guarantee conditions G [8]. The ba-
sic intuition is as follows. A rely condition R is understood as a special
program that constrains the behaviour of a component S by executing it
in parallel as RkS. This is consistent with the above trace interpretation
where parallel composition is interpreted as shuffle and gaps in traces cor-
respond to interferences by the environment. Typical properties of relies are
1 ≤ R (where 1 is skip) and R∗ = R·R = RkR = R. Moreover, relies
distribute over nondeterministic choices as well as sequential and concur-
rent compositions: Rk(S+T ) = RkS+RkT , Rk(S·T ) = (RkS)·(RkT ) and
Rk(SkT ) = (RkS)k(RkT ), hence they apply to all subcomponents of a given
component [7]. A guarantee G of a given component S is only constrained by
the fact that it should include all behaviours of S, that is, S ≤ G.

Consequently, a Jones quintuple is valid if the component S constrained by
the rely satisfies the Hoare triple—the relationship between precondition and
postcondition—and the guarantee includes all behaviours of S [8]:

                      {P R}S{G Q} ⇔ {P }RkS{Q} ∧ S ≤ G.                                     (1)

The rules of Hoare logic without the assignment axiom are still derivable from
the axioms of bi-Kleene algebra, when Hoare triples are replaced by Jones


                                              4
quintuples [8]. To derive the standard rely-guarantee concurrency rule, one can
expand bi-Kleene algebra by a meet operation (u) and assume that (K, +, u)
forms a distributive lattice [7]. Then

            {P R}S{G Q} {P R0 }S 0 {G0 Q0 } G ≤ R0          G0 ≤ R
                                                                     .       (2)
                    {P RuR0 }SkS 0 {G+G0 QuQ0 , }

This inference rule demonstrates how the rely-guarantee specifications of com-
ponents can be composed into a rely-guarantee specification of a larger system.
If S and S 0 satisfy the premises, then SkS 0 satisfies both postconditions Q and
Q0 when run in an environment satisfying both relies R and R0 . Moreover, SkS 0
guarantees either of G or G0 .

Deriving these inference rules from the algebraic axioms mentioned makes
them sound with respect to all models of these axioms, including trace-based
semantics with parallel composition interpreted as interleaving, and true-
concurrency semantics such as pomset languages and the event structures
considered in this article. Without the algebraic layer, Dingel [11] and Cole-
man and Jones [12] have already proved the soundness of rely-guarantee rules
with respect to trace-based semantics, more precisely Aczel traces [13]. This
paper follows previous algebraic developments, but for probabilistic programs.

In Section 5, we provide a suitable extension of the rely-guarantee formalism,
in particular Rule (2), to probabilistic concurrent programs. The soundness of
such a formalism is shown relative to a semantic space that allows sequential
probabilistic programs to include concurrent behaviours.



3   Sequential probabilistic programs


We start by giving a brief summary of the denotation of sequential prob-
abilistic programs using the powerdomain construction of McIver and Mor-
gan [5]. All probabilistic programs are considered to have a finite state space
denoted by Ω. A distribution over the set Ω is a function µ:Ω→[0, 1] such that
P
   s∈Ω µ(s)=1. The set of distributions over Ω is denoted by DΩ. Since Ω is a
finite set, we identify a distribution with the associated measure. For every
                                      P
µ∈DΩ and O⊆Ω, we write µ(O)= s∈O µ(s). An example of distribution is
the point distribution δs , centred at the state s∈Ω, such that
                                    
                                    1       if s=s0 ,
                           δs (s0 ) = 
                                          0 otherwise.

A (nondeterministic) probabilistic program r modelled as a map of type
Ω→PDΩ such that r(s) is a non-empty, topologically closed and convex subset


                                          5
of DΩ for every state s∈Ω. The set DΩ is a topological sub-space of the finite
product RΩ (endowed with the usual product topology), and the topological
closure is considered with respect to the induced topology on Ω 1 . We denote
by H1 Ω the set of probabilistic programs that terminate almost certainly. No-
tice that the set DΩ contains only distributions instead of the subdistributions
considered by McIver and Morgan [5]. Therefore, we only model nondetermin-
istic programs that are terminating with probability 1.

Programs in H1 Ω are ordered by pointwise inclusion, i.e. r vH r0 if for every
s∈Ω, r(s) ⊆ r(s0 ). A program r is deterministic if, for every s, r(s) = {µs } (i.e.
a singleton) for some distribution µs ∈DΩ. The set of deterministic programs is
denoted by J1 Ω (as in Jones’ spaces [3]). If f ∈J1 Ω is a deterministic program
such that f (s) = {µs }, then we usually just write f (s) = µs . A particularly
useful example of a probabilistic deterministic program is the ineffectual pro-
gram skip, which we denote by δ. Thus δ(s) = {δs }.

Let p ∈ [0, 1]. The probabilistic combination of two probabilistic programs r
and r0 is defined as ([5, Def. 5.4.5])

                   (r⊕p r0 )(s) = {µ⊕p µ0 | µ∈r(s) ∧ µ0 ∈r0 (s)},               (3)

where (µ⊕p µ0 )(s) = (1−p)µ(s)+pµ0 (s) for every state s∈Ω. Thus, the program
r (resp. r0 ) is executed with probability 1−p (resp. p).

Nondeterminism is obtained as the set of all probabilistic choices ([5, Def.
5.4.6] ), that is,
                     (r+r0 )(s) = ∪p∈[0,1] (r⊕p r0 )(s).                 (4)

The sequential composition of r by r0 is defined as ([5, Def. 5.4.7]):

                 (r·r0 )(s) = {f ?µ| f ∈J1 Ω ∧ µ∈r(s) ∧ f vH r0 }               (5)

where
                         (f ?µ)(s0 ) =            f (s00 )(s0 )µ(s00 )
                                         X

                                         s00 ∈Ω
for every state s0 ∈Ω.

For r, r0 ∈H1 Ω, the binary Kleene star r∗r0 is the least fixed point of the func-
tion fr,r0 (X) = r0 +r·X in H1 Ω. It has been shown in [5] that the function
r0 7→ r·r0 is continuous —it preserves directed suprema. Notice that a topolog-
ical closure is sometimes needed to ensure that we obtain an element of H1 Ω.
Hence, the Kleene star r∗r0 is the program such that r∗r0 (s) = ∪n fr,r n
                                                                          0 (⊥)(s),

where A is the topological closure of the set A ⊆ DΩ and the constant ⊥ is
1 These healthiness conditions are set out and fully explained in the work of McIver
and Morgan [5].


                                            6
defined, as usual, such that r00 ·⊥=⊥·r00 =⊥, ⊥+r00 = r00 and ⊥ vH r00 for every
r00 ∈H1 Ω∪{⊥}.

We introduce tests, which are used for conditional constructs, following the
idea adopted in various algebras of programs. We define a test to be a map
b : Ω → PDΩ such that b(s) ⊆ {δs }. Indeed, an “if statement” is modelled
algebraically as b·r+(¬b)·r0 where (¬b)(s) = ∅ if the test underlying b holds
at state s and it is {δs } otherwise. The sub-expression b·r(s) still evaluates to
∅ if b(s) is empty, but care should be taken to avoid expressions such as r·b
(if f is a deterministic refinement of b, then f (s00 )(s0 ) may have no meaning if
b(s00 )=∅). A test that is always false can be identified with ⊥.

We denote by H1 Ω the set of tests together with the set of probabilistic pro-
grams. The refinement order vH is extended to H1 Ω in a straightforward man-
ner. For every test b, we have b vH δ; hence, we refer to tests as subidentities.
Every elements of H1 Ω are called programs, unless otherwise specified.




4   An event structures model for probabilistic concurrent programs


The set H1 Ω of probabilistic programs provides a full semantics for program
constructs such as (probabilistic) assignments, probabilistic choices, condi-
tionals and while loops that terminate almost surely. Unfortunately, it is im-
possible to define the concurrent composition of two sequential programs as
an operation on H1 Ω because the result would always be a sequential pro-
gram. Thus we are forced to look for a more general framework in order to
formally model concurrency. Fortunately, there are several suitable mathe-
matical models that allows the formal verification of programs with concur-
rent behaviours. A powerful example that accounts for true concurrency are
Winskel’s event structures [14,15]. In this section, we outline a denotational
semantics for probabilistic concurrent programs based on Langerak’s bundle
event structures [16], which have been extended successfully to quantitative
features [17,18,19]. This construction is necessary to ensure the soundness of
the extended rely-guarantee formalism.

A bundle event structure comprises events ranging over some set E of events
as its fundamental objects. Intuitively, an event is an occurrence of an action
at a certain moment in time. Thus an action can be repeated, but each of its
occurrences is associated with a unique event. Events are (partially) ordered
by a causality relation which we denote by 7→: if an event e00 causally depends
on either e or e0 (i.e. {e, e0 }7→e00 ) then either e or e0 must have happened
before e00 can happen or is enabled. The relationship between e and e0 is called
conflict, written e#e0 , because both events cannot occur simultaneously.


                                        7
In general, the conflict relation # is a binary relation on E. Given two subsets
x, x0 ⊆ E, the predicate x#x0 holds iff for every (e, e0 )∈x×x0 such that e6=e0 ,
we have e#e0 .

Definition 4.1 A quintuple E = (E, 7→, #, λ, Φ) is a bundle event structure
with internal probability (i.e. an ipBES) if

• # is an irreflexive symmetric binary relation on E, called conflict relation.
• 7→⊆ PE×E is a bundle relation, i.e. if x7→e for some x ⊆ E and e∈E,
  then x#x.
• λ:E→H1 Ω, i.e. it labels events with (atomic) probabilistic programs.
• Φ ⊆ PE such that x#x holds for every x∈Φ.

The finite state space Ω of the programs used as labels is fixed.

The intuition behind this definition is that events are occurrences of atomic
program fragments, i.e. they can happen without interferences from an envi-
ronment. Hence, we need to distinguish all atomic program fragments when
translating a program into a bundle event structure. Atomic programs can be
achieved by creating a construct that forces atomicity. Examples of such a
technique include “atomic brackets” [20]. In this paper, we always state which
actions are atomic rather than using such a device.

Given an ipBES E, a finite trace of E is a sequence of events e1 e2 . . . en such
that for all different 1 ≤ i, j ≤ n, ¬(ei #ej ) and if j=i+1 then there exists an
x ⊆ E such that x7→ej and ei ∈x [16,18,21]. In other words, a trace is safe (an
event may occur only when it is enabled) and is conflict free. The set of all
finite traces of E is denoted by T (E). The set of maximal traces of E (w.r.t the
prefix ordering) is denoted Tmax (E). We simply write T (resp. Tmax ) instead
of T (E) (resp. Tmax (E)) when no confusion may arise.

The aim of this section is to elaborate two relationships between the sets of
traces of given event structures. The first comparison is based on a sequential
reduction using schedulers; the second one is simulation. We will show that
the sequential comparison is strictly weaker than the simulation relation.


4.1   Schedulers on ipBES


As in the case of automata, we define schedulers on ipBES in order to obtain
a sequential equivalence on bundle event structures with internal probabil-
ity. Intuitively, a scheduler reduces an ipBES to a element of H1 Ω. While
the technicalities of the schedulers we define in this paper is tailored to-
wards a rely-guarantee reasoning, there might be relationships with previous
works [22,23] where schedulers (and associated testing theories) are restricted


                                       8
in order achieve a broader class observationally equivalent processes.

A subdistribution is a map µ : Ω → [0, 1] such that          s∈Ω µ(s) ≤ 1. The set of
                                                         P

subdistributions over Ω is denoted by D≤1 Ω.

Definition 4.2 A scheduler σ on an ipBES E is a map

                             σ:T →[(E×Ω)+D≤1 Ω]

such that for all α∈T :

(1) dom(σ(α)) = {(e, s) | αe∈T ∧ s∈Ω},
(2) there exists a function w:E×Ω→[0, 1] such that, for every (e, s)∈dom(σ(α)),
    σ(α)(e, s) = w(e, s)µ for some µ∈λ(e)(s).
                              P
(3) for every s∈Ω, we have (e,s)∈dom(σ(α)) w(e, s) = 1,
(4) for every (e, s)∈dom(σ(α)), if λ(e)(s)=∅, then w(e, s)=0 and σ(α)(e, s)=0
    (the subdistribution that evaluates to 0 everywhere).

The set of all schedulers on E is denoted by Sched(E).

Property 1 says that we may schedule an event provided it does not depend
on unscheduled events.

Property 2 states that, given a trace α, the scheduler will resolve the non-
determinism between events enabled after α byusing the weight function w.
This may include immediate conflicts or interleavings of concurrent events.
Moreover, the scheduler has access to the current program state when resolv-
ing that nondeterminism. This means that w(e, s) is the probability that the
event e is scheduled, knowing that the program state is s. If the event e is suc-
cessfully scheduled, then the scheduler performs a last choice of distribution,
say µ from λ(e)(s), to generate the next state of the program.

Property 3 ensures that when the state s is known, then the choice between
the events, enabled after the trace α, is indeed probabilistic.

Property 4 says that a scheduler is forced to choose events whose labels do
not evaluate to the empty set at the current state of the program. This is
particularly important when the program contains conditionals and the label
of an event is a test. A scheduler is forced to choose the branch whose test
holds. If two tests hold at state s, then a branch is chosen probabilistically
using the weight function w.

The motivation behind Property 4 is to ensure that, for every trace α such
that dom(σ(α))6=∅, and every state s∈Ω, we have
                               X
                                            σ(α)(e, s)∈DΩ,
                          (e,s)∈dom(σ(α))



                                            9
hence that sum is indeed a distribution. To ensure that a scheduler satisfy-
ing that condition can be constructed, we restrict ourselves to feasible event
structures. Given an element r∈H1 Ω, we write dom(r)={s | r(s)6=∅}.

Definition 4.3 An ipBES E is feasible if for every trace α∈T \Tmax , we have
∪αe∈T dom(λ(e))=Ω.

A consequence of this assumption is that an “if clause” always needs to have
a corresponding “else clause”.

Example 4.4 Let us consider the program r·(δ+r). In this program, r is
atomic deterministic (such as an assignment to a variable) and the associ-
ated event structure has three events:

 E = ({er , e0r , eδ }, {{er }7→eδ , {er }7→e0r }, {eδ #er2 }, {(er , r), (e0r , r), (eδ , δ)}, Φ),

where Φ = {{e0r , eδ }} (see Sec. 4.3 for an inductive construction of ipBES
from primitive blocks). This event structure is feasible and a scheduler σ on
E is characterised by a weight function w:{er , e0r , eδ }×Ω→[0, 1] resolving the
choice δ+r. In fact, for every fixed state s∈Ω, we have σ(er )(eδ , s)=w(eδ , s)δs
and σ(er )(e0r , s)=w(e0r , s)r(s) and w(eδ , s)+w(e0r , s)=1.


4.2   Generating sequential probabilistic programs from ipBES and schedulers


Similar to the case of probabilistic automata [6], our scheduler resolves branch-
ing as encoded in the conflict relation of an event structure. In addition, a
scheduler also “flattens” concurrency into interleaving by choosing an enabled
event according to the associated weight function. The flattening of concur-
rent behaviours is sound because actions labelling events are assumed atomic
and we are using schedulers to generate sequential behaviours from an ipBES.
True concurrency is accounted for in Sec. 4.4.

Let σ∈Sched(E) and s∈Ω be an initial state. We inductively construct a
sequence of functions ϕn that map a trace in T to a subdistribution on Ω
according to σ and s. Intuitively, if α∈T , then ϕn (α)∈D≤1 Ω is the sequential
composition of the n-first probabilistic actions labelling events in α applied
to the initial state s. This yields a subdistribution because α is weighted with
respect to the scheduler σ. The sequence of partial functions ϕn :T +D≤1 Ω is
the computation sequence of E with respect to σ from initial state s.

Formally, for each n∈N, we have dom(ϕn )=∪k≤n Tk , where Tn is the set of
traces of length n and

(1) ϕ0 (∅)=δs ,where s is the initial state,


                                               10
(2) if αe∈Tn+1 then
                                               X
                           ϕn+1 (αe)(s) =          [σ(α)(e, t)(s)]ϕn (α)(t)
                                               t∈Ω

    and ϕn+1 (αe)=ϕn (αe) otherwise.

To emphasises that this computation function refers to a specific initial state
t∈Ω we sometimes write ϕn,t instead of ϕn .

The complete run of E with respect to σ is the limit ϕ of that sequence, i.e.
ϕ=∪n ϕn , which exists because ϕn defines a sequence of partial functions such
that ϕn is the restriction of ϕn+1 to dom(ϕn ). Since we consider finite traces
only, we have dom(ϕ)=T . The sequential behaviour of E with respect to σ
from the initial state s is defined by the sum
                                                  X
                                    σs (E) =              ϕ(α).
                                                 α∈Tmax

Proposition 4.5 For every bundle event structure E, scheduler σ∈Sched(E)
and initial state s, σs (E) is a subdistribution.

Proof. Let ϕ be the complete run of E with respect to a given scheduler σ.
We show by induction on n that
                       X                              X             X
  µn (Ω) =                            ϕ(α)(Ω) =                                    ϕ(α)(t) = 1.
             α∈Tn ∪(Tmax ∩dom(ϕn ))                   t∈Ω α∈Tn ∪(Tmax ∩dom(ϕn ))


For the base case n = 0, we have µ0 (Ω) = ϕ(∅)(Ω) = δs (Ω) = 1, where s is
the initial state. Assume the induction hypothesis µn (Ω) = 1. We have
                          X
µn+1 (Ω) =                                ϕ(α)(Ω)
             α∈Tn+1 ∪(Tmax ∩dom(ϕn+1 ))

        =†
               X                             X
                       ϕ(α)(Ω)+                        ϕ(α)(Ω)
              α∈Tn+1                α∈Tmax ∩dom(ϕn )
               X       X                                          X
        =                     σ(α)(e, t)(Ω)ϕ(α)(t)+                          ϕ(α)(Ω)
             αe∈Tn+1 t∈Ω                                  α∈Tmax ∩dom(ϕn )
                X          X X                                          X
        =                           σ(α)(e, t)(Ω)ϕ(α)(t)+                            ϕ(α)(Ω)
             α∈Tn \Tmax αe∈T t∈Ω                                  α∈Tmax ∩dom(ϕn )
                                                            
                X                 X                                                X
        =                                   σ(α)(e, t)(Ω) ϕ(α)(t)+                            ϕ(α)(Ω)
             α∈Tn \Tmax    (e,t)∈dom(σ(α))                                   α∈Tmax ∩dom(ϕn )

        =‡
                 X                            X
                           ϕ(α)(Ω)+                       ϕ(α)(Ω)
              α∈Tn \Tmax               Tmax ∩dom(ϕn )

        = µn (Ω) = 1.

(†) Follows from Tn+1 ∪(Tmax ∩dom(ϕn+1 )) = Tn+1 ∪(Tmax ∩dom(ϕn )) and the
fact that the second union is disjoint.


                                                 11
(‡) The square-bracketed term equals 1 because of Properties 2 and 3 of the
scheduler σ.

Therefore, each partial computation ϕn can be seen as a probability distribu-
tion ϕn (−)(Ω) supported on Tn ∪(Tmax ∩dom(ϕn )). Hence, the limit is a sub-
distribution ϕ(−)(Ω) on Tmax . It does not necessarily add up to 1 because
elements of Tmax are finite maximal traces only and non-termination will de-
crease that quantity (we assume that the empty sum is 0. This occurs when
there are no maximal traces).                                              2

Given a state t∈Ω, σs (E)(t) is the probability that the concurrent probabilistic
program denoted by E terminates in state t when conflicts (resp. concurrent
events) are resolved (resp. interleaved) according to the scheduler σ. Since
we consider terminating programs only, we denote by Sched1 (E) the set of
schedulers of E such that, for every initial state s, σs (E) is a distribution.
A scheduler in Sched1 (E) generates a sequential behaviour that terminates
almost surely. This leads to our definition of a bracket [[ ]] that transform each
feasible ipBES to an element of H1 Ω:

                     [[E]](s) = conv{σs (E) | σ∈Sched1 (E)}

where conv(A) (resp. A) is the convex (resp. topological) closure of the set of
distributions A in RΩ .

Definition 4.6 Let E, F be two feasible event structures. We say that E (se-
quentially) refines F, denoted by E v F, if [[E]] vH [[F]] holds in H1 Ω.

The relation v is a preorder on ipBES. Whilst this order is not a congruence,
it is used to specify the desired sequential properties of a feasible event struc-
ture E with Sched1 (E)6=∅. We will show that feasibility and non-emptiness of
Sched1 are preserved by the regular operations of the next section (Props 4.8
and 4.15).



4.3   Regular operations on ipBES


This section provides interpretations of the operations (+, ·, ∗, k) and constants
0, 1 on event structures with disjoint sets of events. These definitions allow the
inductive translation of program texts into event structure objects.

- The algebraic constant 1 is interpreted as (e, ∅, ∅, {(e, δ)}, {e}).
- The algebraic constant 0 is interpreted as (∅, ∅, ∅, ∅, ∅).
- Each atomic action r∈H1 Ω is associated with ({e}, ∅, ∅, {(e, r)}, {e}). This
  event structure is again denoted by r.


                                       12
- The nondeterministic choice between the event structures E and F is con-
  structed as

         E+F = (E∪F, #E+F , 7→E ∪ 7→F , λE ∪λF , {x∪y | x∈ΦE ∧ y∈ΦF })

  where #E+F = [∪x∈ΦE ∧yΦF sym(x×y)]∪#E ∪#F ∪sym(in(E)×in(F)) and sym
  is the symmetric closure of a relation on E∪F . The square-bracketed set
  ensures that every final event in E is in conflict with every final event in F.
  This ensures that, if z∈ΦE+F , then z#z.
- The sequential composition of E by F is

  E·F = (E∪F, #E ∪#F , 7→E ∪ 7→F ∪{x 7→ e | e∈in(F)∧x∈ΦE }, λE ∪λF , ΦF ).

- The concurrent composition of E and F is

                  EkF = (E∪F, #E ∪#F , 7→E ∪ 7→F , λE ∪λF , ΦE ∪ΦF ).

- The binary Kleene star of E and F is the supremum of the sequence

                               F, F+E·F, F+E·(F+E · F), . . .

  of bundle event structures with respect to the ω-complete sub-BES or-
  der [24].

Example 4.7 Let us consider the sequential programs r, δ∈H1 Ω. A concur-
rent program that is skipping or running r in parallel with itself is algebraically
denoted by (rkr)+1. The construction of the associated event structure starts
from the innermost operation (rkr), assuming that each occurrence of the
atomic action r is associated with an event from {er , e0r }. Thus

                 Erkr = ({er , e0r }, ∅, ∅, {(er , r), (e0r , r)}, {{er }, {e0r }}).
                                             |        {z         }
                                                      λrkr


We can now construct the nondeterministic choice between rkr and δ as

  E(rkr)+1 = ({er , e0r , eδ }, {er #eδ , e0r #eδ }, ∅, λrkr ∪{(eδ , δ)}, {{, eδ } | ∈{er , e0r }}).

In this example, we have er #eδ and e0r #eδ but er and e0r are concurrent.

For every bundle event structure E, 0+E=E, 0·E=E·0=E, and in particular,
0·1=1. The constant 0 was only introduced to have a bottom element on the
set of bundle event structures with internal probabilities. It ensures that we
can compute the Kleene star inductively from the least element. Moreover, 0
will disappear in mixed expressions because of these properties.

We now show that the operations (+) and (·) are preserved by the map [[ ]].
The case of the binary Kleene star (∗) is proven in Prop. 4.15.


                                                 13
Proposition 4.8 For E, F non-zero, feasible and terminating event struc-
tures, we have [[E+F]] = [[E]]+[[F]] and [[E·F]] = [[E]]·[[F]].

Proof. For the case of nondeterminism (+), let s∈Ω be the initial state and
µ∈[[E+F]](s). Let us firstly assume that µ=σs (E) for some σ∈Sched1 (E+F).
By definition of the sum E+F, the set of events E and F are disjoints, so we
can define two schedulers σ E ∈Sched1 (E) and σ F ∈Sched1 (F) as follows. Let
α∈T (E+F) and (e, t)∈dom(σ(α)), we define

                                      
                                      σ(α)(e, t)   if α∈T (E)\{∅},
                    σ E (α)(e, t) =
                                       σ(∅)(e,t)   if α=∅.
                                           pE
                                            t

where pEt = e0 ∈in(E) w(e, t), w is the weight function associated to σ at the
             P

trace ∅ and s is the initial state. The real number pEt is just a normalisation
constant required by Property 3 in the definition of schedulers. 2 The sched-
uler σ F is similarly defined. It follows directly from these definition of σ E and
σ F that σ(∅)(e, t)=pEt σ(∅)(e, t)+pF                     E    F
                                     t σ(∅)(e, t) where pt +pt =1 because of Prop-
erty 3. Hence, σs (E)=pEs σsE (E)+pF    F
                                     s σs (F) i.e. σs (E)∈[[E]]+[[F]]. Since [[E]]+[[F]]
is convex and topologically closed, we deduce that [[E+F]](s) ⊆ ([[E]]+[[F]])(s).

For the converse inclusion ([[E]]+[[F]])(s)⊆[[E+F]](s), notice that conv(A) =
conv(A) holds for every subset A⊆RΩ . If we write A={σs (E) | σ∈Sched1 (E)}
and B={σs (F) | σ∈Sched1 (F)}, then

             ([[E]]+[[F]])(s) = conv(conv(A)∪conv(B)) = conv(A∪B).

But it is clear that A⊆[[E+F]](s) (a scheduler that does not choose F is
possible because E is feasible) and B⊆[[E+F]](s). Therefore, ([[E]]+[[F]])(s) =
conv(A∪B)⊆[[E+F]](s) because the last set is convex and topologically closed.

The sequential composition is proven using a similar reasoning. Let E, F be
two bundle event structures satisfying the hypothesis, and µ∈[[E·F]](s) for
some initial state s∈Ω.

The proof of [[E·F]](s) ⊆ [[E]]·[[F]](s) goes as follows. Firstly, let us assume
that there is a scheduler σ on E·F such that µ=σs (E·F). Since schedulers are
inductively constructed, there exists σ E ∈Sched(E) and σ F ∈Sched(F) such
that
                   
                   σ E (α)(e, t)if αe∈T (E),
      σ(α)(e, t) =  F 00
                    σ (α )(e, t) if α=α0 α00 and (α0 , α00 )∈Tmax (E)×T (F).


2   If pEt =0, then σ∈Sched1 (F).


                                              14
Let us denote by ϕn and ϕEn (resp. ϕF     n,t )
                                                3
                                                  the computation sequences as-
sociated to the respective schedulers σ and σ E (resp. σ F ) from the initial
state s (resp. t). It follows directly that ϕn (α)=ϕEn (α) for every α∈Tn (E). If
α0 ∈Tmax (E)∩Tn (E) and e∈in(F) then, for every state u∈Ω,

                        ϕn+1 (α0 e)(u) =              σ F (∅)(e, t)(u)ϕE (α0 )(t).
                                                X

                                                t∈Ω

Similarly, we have
                                                            "                                    #
                0   0                     F            0             F          0        E   0
                                X                               X
        ϕn+1 (α ee )(u) =               σ (e)(e, t )(u)             σ (∅)(e, t)(t )ϕ (α )(t)
                                t0 ∈Ω                         t∈Ω
                                                                                    

                                               σ F (e)(e, t0 )(u)σ F (∅)(e, t)(t0 ) ϕE (α0 )(t)
                                X         X
                            =         
                                t∈Ω    t0 ∈Ω

                                      ϕF       E  0
                                X
                            =          2,t (u)ϕ (α )(t).
                                t∈Ω



By simple induction on the length of α00 , we deduce that

                          ϕ(α0 α00 )(u) =              ϕF   00    E  0
                                                 X
                                                        t (α )(u)ϕ (α )(t),
                                                 t∈Ω


where ϕF                                                     F
         t is the complete run obtained from the sequence ϕn,t . It follows by
definition of the sequential composition on H1 Ω (Eqn. (5)) that

                                              σtF (F)(u)σsE (E)(t)∈[[E]]·[[F]](s)
                                        X
                    σs (E)(u) =
                                        t∈Ω


for every state u∈Ω. Secondly, since [[E]]·[[F]](s) is upclosed and topologically
closed, we deduce that [[E·F]](s) ⊆ [[E]]·[[F]](s).

Conversely, if µ∈[[E]]·[[F]](s), then either µ(u) = t∈Ω σtF (F)(u)σsE (E)(t) or
                                                                         P

µ is in the closure of the set of these distributions. Either way, the closure
properties of [[E·F]](s) implies that [[E]]·[[F]](s)⊆[[E·F]](s).             2


4.4    Simulation for ipBES


The partial order defined in Definition 4.6 compares the sequential behaviours
of two systems. However, it suffers from a congruence problem, i.e. there exist
programs E, F and G such that EvF but EkG6vFkG. A known technique for
achieving congruence is to construct an order based on simulations, which is
the subject of this section. We use a similar technique in this subsection.
3   Remind that ϕn,t is the computation function computed given the initial state t.


                                                       15
We say that a trace α is weakly maximal if it is maximal or there exist some
events e1 , . . . , en such that αe1 · · · en ∈Tmax and δvH λ(ei ) for every 1 ≤ i ≤ n.

Definition 4.9 A function f :T (E)→T (F) is called a t-simulation if the fol-
lowing conditions hold:

- if f (∅) = ∅ and f −1 (β) is a finite set for every β∈T (F),
- if αe∈T (E) then either:
  · f (αe) = f (α) and λ(e) vH δ holds in H1 Ω,
  · or there exists an event e0 of F such that λ(e)vH λ(e0 ) and f (αe)=f (α)e0 .
- if αe is maximal in T (E) then f (αe) = f (α)e0 , for some e0 (with λ(e) vH
  λ(e0 )), and f (αe) is weakly maximal in T (F) 4 .

We say that E is simulated by F, written E vsim F, if there exists a simulation
from E to F. The equivalence generated by this preorder is denoted ≡sim .

The notion of t-simulation has been designed to simulate event structures
correctly in the presence of tests. For instance, given a test b, the simulation
δ vsim (b+¬b) fails because a t-simulation is a total function and it does not
allow the removal of “internal” events labelled with subidentities during a
refinement step. The finiteness condition on f −1 (β) ensures that we do not
refine a terminating specification with a diverging implementation. Without
that constraint, we would be able to write the refinement


      if (0=1) then s:=0 else[if (0=1) then s:=0 else[. . . ]] vsim s:=0.


However, this should not hold because the left hand sides is a non-terminating
program and cannot refine the terminating assignment s :=0.

A t-simulation is used to compare bundle event structures without looking in
details at the labels of events. It can be seen as a refinement order on the
higher level structure of a concurrent program. Once a sequential behaviour
has to be checked, we use the previously defined functional equivalence on
event structures with internal probabilities.

Example 4.10 Consider a program variable x of type Boolean (with value 0
or 1). A t-simulation from (x=1)+(x6=1)·(x:=1) to 1+(x:=0u1) 5 is given by




4   If f (α) is maximal then α is necessarily maximal.
5   x:=0u1 is an atomic nondeterministic-assignment, it cannot be interfered with.


                                         16
the dotted arrow in the following diagram:

                     ∅                                    4/ ∅


              }                 $                                    #
           ex=1                ex6=1             1 eδ            2 ex:=0u1

                                    
                            ex6=1 ex:=1

This t-simulation refines two nondeterministic choices, one at the program
structure level and the other at the atomic level.

Proposition 4.11 The t-simulation relation vsim is a preorder.

Proof. Reflexivity follows from the identity function and transitivity is
obtained by composing t-simulations which will generate a new t-simulation.
Notice that care should be taken with respect to the third property of a t-
simulation. If f :T (E)→T (F), g:T (F)→T (G) are t-simulations, αe∈Tmax (E)
and λ(e)vH δ, then f (αe)=f (α)e0 for some e0 of F such that λ(e)vH λ(e0 ). If
λ(e0 )vH δ, then it is possible that g(f (α)e0 )=g(f (α)). However, since f (α)e0 is
weakly maximal, g(f (α)e0 ) is also weakly maximal and we can find an event
e00 ∈G such that f (α)e00 is weakly maximal and λ(e0 )vH λ(e00 ). We then map
αe to g(f (α))e00 in the t-simulation from E to F.                                2

Proposition 4.12 If E, F, G are ipBES, then

                              EkF ≡sim FkE,                                     (6)
                          Ek(FkG) ≡sim (EkF)kG,                                 (7)
                              E∗F ≡sim F+E·(E∗F),                               (8)
                          E vsim F ⇒ G+E vsim G+F,                              (9)
                          E vsim F ⇒ G·E vsim G·F,                             (10)
                          E vsim F ⇒ EkG vsim FkG.                             (11)


Proof. The constructions EkF and FkE result in the same event structure
and similarly for the associativity.

The Unfold Eqn. (8) is clear because the left and right hand side event struc-
tures are exactly the same up to renaming of events.

Implication (9) follows by considering the function idT (G) ∪f :T (G+E)→T (G+F).
It is indeed a function because the sets of events G and E (resp. F ) are dis-
joint. The property of a t-simulation follows directly because the set of traces
T (G+E) is the disjoint union T (G)∪T (E) (similarly for G+F).

For case of sequential composition (10), let f be a t-simulation from E to F.


                                          17
It is clear that the function g:T (G·E)→T (G·F), such that g(α)=α|G f (α|E ) is
a t-simulation.

For the Implication (11), let f :T (E)→T (F) be a t-simulation. Let us construct
a t-simulation g:T (EkG)→T (FkG) inductively. We set g(∅)=∅. Let α∈T (EkG)
and e∈E∪G such that αe is a trace of EkG. We write α|E the restriction of α
to the events occurring in E. The inductive definition of g is:
                         
                          g(α)e if e∈G,
                         
                         
                         
                         
                         
               g(αe) =     g(α) if e∈E and f (α|E e)=f (α|E ),
                         
                         
                         
                              0                               0
                         
                          g(α)e if e∈E and f (α|E e)=f (α|E )e .

Since the set of events of E and G are disjoint, the cases in the above definition
of g are disjoint. That is, g is indeed a function and it satisfies the second
property of a t-simulation. The last property is clear because if αe is maximal
in T (EkG), then either α|E is maximal in E and α|G e is maximal in T (G),
or α|E e is maximal in T (E) and α|G is maximal in T (G). In both cases,
g(αe)=g(α)e0 for some e0 ∈E∪G and g(αe) is weakly maximal in T (FkG).
2

We now state the main result of this section, which is the backbone of our
probabilistic rely-guarantee calculus.

Theorem 4.13 Let E and F be feasible and terminating ipBES. Then E vsim
F implies E v F.

Proof. Let f be a t-simulation from E to F, s∈Ω be the initial state,
σ∈Sched1 (E) and ϕ is the complete run of σ on E from s. We have to generate
a scheduler τ ∈Sched1 (F) such that the measures σs (E) and τs (F) are equal
i.e. they produce the same value for every state u∈Ω.

                              −1
For every β∈T (F), we define fmin (β) to be the set of minimal traces in f −1 (β),
that is,
             −1
            fmin (β) = {α | ∀e∈E : α=α0 e∈f −1 (β) ⇒ α0 ∈f
                                                        / −1 (β)}.
We now construct the scheduler τ . Let β∈T (F). We consider two cases:

• If f −1 (β) = ∅ then we set τ (β)(e, t) = 0∈D≤1 Ω, except for some particular
  maximal traces that are handled in (†) below.
• Otherwise, given a state t∈Ω, we define a normalisation factor
                                          X
                              Cβ,t =                ϕ(α)(t),
                                          −1
                                       α∈fmin (β)



                                         18
    and we set 6
                                                                                                           
                                                                                           k
                           1        X                                    X                Y
         τ (β)(e, t) =                    ϕ(α)(t)                        wi−1 (ei , t)µk 
                                                                                         
                          Cβ,t α∈f −1 (β)
                              
                                      min         αe ···e ∈f −1 (βe) i=1
                                                                  1       k    min



    where wi−1 (ei , t) is the weight function such that σ(αe1 · · · ei−1 )(ei , t) =
    wi−1 (ei )µ, and µ∈λ(ei ) (if λ(ei )(t) is empty then wi−1 (ei , t) = 0). The dis-
    tribution µk is chosen by σ from λ(ek )(t), when scheduling ek .

Firstly, we show that τ is indeed a scheduler on F. The Property(1) of Def-
inition 4.2 is clear. Let us show the other properties. Let βe∈T (E) and let
W :E×Ω→R be the weight function such that
                                                                   k
                        1     X                       X           Y
            W (e, t) =                 ϕ(α)(t)                        wi−1 (ei , t).
                       Cβ,t α∈f −1 (β)         αe ···e ∈f −1 (βe) i=1
                                    min                       1       k       min



Indeed, µ= τW   (β)(e,t)
                  (e,t)
                         is in λ(e)(t) 7 because λ(e)(t) is convex and for each
               −1
αe1 · · · ek ∈fmin (βe) and µk ∈λ(ek )(t)⊆λ(e)(t). Hence τ (β)(e) = We fe and τ
satisfies the Property (2) of Def. 4.2. As for Property (3), let s∈Ω and let us
compute the quantity
                                                      X
                                V (t) =                               W (e, t),
                                             (e,t)∈dom(τ (β))


for a fixed t∈Ω. Let us write dom(β) = {e | βe∈T (F)}.


                                                                            k
                     X           1     X                       X           Y
      V (t) =                                   ϕ(α)(t)                        wi−1 (ei , t)
                                C
                (e,t)∈dom(τ (β)) β,t α∈f −1 (β)         αe ···e ∈f −1 (βe) i=1
                                            min                           1    k     min
                                                                             k
                 1     X                      X                 X           Y
           =                    ϕ(α)(t)                                         wi−1 (ei , t)
                Cβ,t α∈f −1 (β)         (e,t)∈dom(τ (β)) αe ···e ∈f −1 (βe) i=1
                         min                                              1    k     min
                                                                                      k
                 1     X                           X                                  Y
           =                    ϕ(α)(t)                                                    wi−1 (ei , t).
                Cβ,t α∈f −1 (β)         αe ···e ∈∪                   −1       i=1
                         min                      1   k    e∈dom(β) fmin (βe)



From the second to the third expression, the two rightmost sums were merged
                           −1
into a single one because fmin (βe)∩f −1 (βe0 ) = ∅ (f is a function). It follows

6                                                                    −1
   Notice if Cβ,t = 0 for some t∈Ω then ϕ(α)(t) = 0 for every α∈fmin    (β). In other
words, none of these α will be scheduled at all. Hence, β need not be scheduled
either.
7 The case W (e, t) = 0 can be adapted easily because the numerator in the defini-

tion of τ (β)(e) is also 0. For instance, we can assume that 00 = 1.


                                                      19
                                α                                                    /7 β
                w0 (e01 ,t)              w0 (e1 ,t)
                                                                                          W (e,t)
                     {                          #                                         
              αe01                             αe1                                   =15 e
                                w1 (e02 ,t)               w1 (e2 ,t)

                                    |                            "
                              αe1 e02                         αe1 e2
We have V (t) = w0 (e01 , t) + w0 (e1 , t)w1 (e02 , t)w0 (e1 , t)w1 (e2 , t) = 1 because
w1 (e02 , t) + w1 (e2 , t) = 1 and w0 (e01 , t) + w0 (e1 , t) = 1 (Def. 4.2 Property (3)).
                         Fig. 1. An example showing that V (t) = 1.




from Property (3), applied on the weight wi−1 (ei , t) of σ, that




                                        X                    k
                                                             Y
                                                                     wi−1 (ei , s) = 1
                                                −1
                          αe1 ···ek ∈∪e∈dom(β) fmin (βe) i=1




and hence V = 1 (c.f. Figure 1 for a concrete example). The last Prop-
erty (4) of Def. 4.2 is clear because if λ(e)(t) = ∅, then the coefficient of
σ(αe1 · · · ek−1 )(ek , t) is 0 because λ(ek )(t) = ∅. Hence, the product is also 0.


Secondly, let ψ be the complete run of F with respect to τ . We now show by
induction on β that



                                                      X
                                 ψ(β) =                     ϕ(α) = Cβ,t ,                           (12)
                                                 −1
                                              α∈fmin (β)




where the empty sum evaluates to the identically zero distribution. The base
case is clear because ψ(∅)=δs =φ(∅) where s is the initial state. Let us as-
sume the above identity for β∈T (F) and let e∈F such that βe=T (E) and


                                                      20
 −1
fmin (βe)6=∅. By definition of ψ, if u∈Ω, we have:
           X 1              X                              X             k
                                                                         Y
ψ(βe)(u) =                            ϕ(α)(t)                                wi−1 (ei , t)µk (u)ψ(β)(t)
            Cβ,t            −1                              −1
              t∈Ω        α∈fmin (β)             αe1 ···ek ∈fmin (βe) i=1

              X       X               X           k
                                                  Y
          =                                              wi−1 (ei , t)µk (u)ϕ(α)(t)
              t∈Ω α∈f −1 (β) αe1 ···ek ∈f −1 (βe) i=1
                     min                 min

                 X              X            k
                                            XY
          =                                              wi−1 (ei , t)µk (u)ϕ(α)(t)
                 −1                  −1
              α∈fmin (β) αe1 ···ek ∈fmin (βe) t∈Ω i=1
                                                                                  " k                     #
                 X              X           XX                                     Y
                                                                     0
          =                                                w0 (e1 , t )δt0 (t)          wi−1 (ei , t)µk (u) ϕ(α)(t0 )
                 −1                  −1            0
              α∈fmin (β) αe1 ···ek ∈fmin (βe) t∈Ω t ∈Ω                            i=2

                 X              X            k
                                            XY
          =                                              wi−1 (ei , t)µk (u)ϕ(αe1 )(t)
                 −1                  −1
              α∈fmin (β) αe1 ···ek ∈fmin (βe) t∈Ω i=2
                                                                                  " k                     #
                 X              X           XX                                     Y
          =                                                w1 (e2 , t0 )δt0 (t)         wi−1 (ei , t)µk (u) ϕ(αe1 )(t0 )
                 −1                  −1            0
              α∈fmin (β) αe1 ···ek ∈fmin (βe) t∈Ω t ∈Ω                            i=3

          = ··· .
By continuing the above reasoning for all ei (induction), i ≤ k − 1, we obtain
                       X               X               X
    ψ(βe)(u) =                                             wk−1 (ek , t)µk (u)ϕ(αe1 · · · ek−1 )(t)
                       −1                  −1
                    α∈fmin (β) αe1 ···ek ∈fmin (βe) t∈Ω
                       X               X
                =                                      ϕ(αe1 · · · ek )(u).
                       −1                  −1
                    α∈fmin (β) αe1 ···ek ∈fmin (βe)

Hence,
                                                                  ϕ(α0 )(u).
                                                        X
                               ψ(βe)(u) =
                                                      −1
                                                 α0 ∈fmin (βe)
                                                              P
(†) We finally compute the sum τs (F) = β∈Tmax (F ) ψ(β). Notice firstly that
τ may not schedule some traces of F. In particular, the third property in
the definition of simulation implies that a maximal element of T (E) may be
mapped to a weakly maximal element of T (F). Hence, we need to extend
the scheduler τ so that it is non-zero for exactly one maximal element from
that weakly maximal trace. More precisely, if β 0 = f (α) is weakly maximal
for some maximal trace α∈Tmax (E), then there exists a sequence e1 , . . . , en
such that β = β 0 e1 · · · en ∈Tmax (F) and δ vH λ(ei ). We extend τ such that
τ (β 0 e1 · · · ei )(ei+1 , t) = δt . This implies that ψ(β)(t) = ψ(β 0 )(t). The other
case is that β is maximal and belongs to the image of f . In both cases, we
have                                            X
                                      ψ(β)(t) =     ϕ(α)(t),
                                      α∈Aβ
               −1                                        −1
where Aβ = fmin (β) if β is in the image of f , or Aβ = fmin (β 0 ) if there is such
a β 0 as above, otherwise, Aβ = ∅. Thus, Aβ contains maximal traces only (if


                                                      21
it is not empty). Since, f is a total function, the set {Aβ | β∈Tmax (F)} is a
partition of Tmax (E) and we have
            X                        X      X                      X
                      ψ(β)(t) =                     ϕ(α)(t) =                ϕ(α)(t),
         β∈Tmax (E)               β∈Tmax (E) α∈Aβ               α∈Tmax (E)


i.e. we obtain τs (F) = σs (E).                                                         2

Example 4.14 Reconsider the t-simulation of Example 4.10. By definition,
the unique scheduler σ on (x=1)+(x6=1)·(x:=1) satisfies:
                                                           
                                                           1 if s=t,
- σ(∅)(ex=t , s) = w(ex=t , s)δt where w(ex=t , s) =
                                                           0 otherwise.
- σ(ex=0 )(ex:=1 , s) = δ1 , for s∈{0, 1}.

The corresponding scheduler τ on 1+(x:=0u1), constructed (as per the proof
of Thm. 4.13) from σ using the illustrated t-simulation, satisfies:

- σ(∅)(eδ , 1) = w(ex=1 , 1)δ1 = δ1 and σ(∅)(eδ , 0) = 0,
- σ(∅)(ex:=0u1 , 1) = 0 and σ(∅)(ex:=0u1 , 0) = w(ex=0 , 0)δ1 = δ1 .

Since (x=1)+(x6=1)·(x:=1) is sequentially equivalent to x:=1, we can see that
the scheduler τ on 1+(x:=0u1) forces the final value of x to be 1 by resolving
(+) and (u) as they were resolved in the program (x=1)+(x6=1)·(x:=1).

We now show that the binary Kleene star is preserved by the semantics map.

Proposition 4.15 For every non-zero, feasible and terminating event struc-
ture E and F, we have [[E∗F]] = [[E]]∗[[F]].

Proof. For the binary Kleene product, since [[E]]∗[[F]] is the least fixed point
of f (X) = [[F]]+[[E]]·X in H1 Ω 8 , and E∗F satisfies

                                  F+E·(E∗F) ≡sim E∗F

by construction of the sequences of bundle event structures defining E∗F.
Therefore, Thm. 4.13 and Prop. 4.8 imply that [[E]]∗[[F]] vH [[E∗F]].

Conversely, let µ∈[[E∗F]](s) for some initial state s∈Ω. As in the case of
Prop. 4.8, we assume that µ is computed from a scheduler σ on E∗F. We
construct a sequence of schedulers σn that “converges” to σ as follows. We
set σ0 to be any element of Sched1 (F), σ1 (α)=σ(α) if α is a trace of F or
E, otherwise, we set σ1 (α0 α00 )=σ0 (α00 ) where α0 ∈Tmax (E) (notice that σ0 is ap-
plied to a different copy of F but this is not important as event names can be
8 Notice that the least fixed point is in H1 Ω but not H1 Ω. The reason is that [[E]]
and [[F]] are elements of H1 Ω because of feasibility and termination.


                                            22
abstracted.). Inductively, we define
                         
                         σ(α)
                         
                                         if α∈T (F+E·(. . . E·(F+E))),
              σn (α) =
                                                       |             {z               }
                                                            n occurrences of E
                         σ (α|
                                    F)    otherwise.
                         
                            0




Again, σ0 is applied to the n+1th copy of F. Indeed, we have

                     σn ∈Sched1 (F+E·(· · · E·(F+E·F)))
                                          |                 {z                }
                                                  n occurrences of E


by construction. On the one hand, the sequence of distributions σn,s (E) forms
a subset of [[E]]∗[[F]](s). On the other hand, let u∈Ω and let us denote

                         T≤n = T (F+E·(. . . E·(F+E·F))).
                                      |                {z                 }
                                              n occurrences of E


If we denote by ϕn the complete run of σn on E∗F, then we have


                                              X                                   X
    |σs (E)(u) − σn,s (α)(u)| =                        ϕ(α)(u)−                            ϕn (α)(u)
                                    α∈Tmax (E∗F )                      α∈Tn ∩Tmax (E∗F )

                                                  X
                                =                                (ϕ(α)(u)−ϕn (α)(u))
                                    α∈Tmax (E∗F )\T≤n−1
                                              X
                                ≤                                |ϕ(α)(u)−ϕn (α)(u)| .
                                    α∈Tmax (E∗F )\T≤n−1



The set Tmax (E∗F)\T≤n−1 shrinks, when n increases, because every finite trace
of E∗F belongs to some set T≤k . Therefore, the last sum above is decreasing to
0. Hence, since Ω is a finite set, the sequence σn,s (E∗F) converges (pointwise)
to σs (E∗F) in DΩ. Since [[E]]∗[[F]](s) is topologically closed, we deduce that
σs (E)∈[[E]]∗[[F]](s). Therefore, [[E∗F]] vH [[E]]∗[[F]].                     2

Proposition 4.16 Let r, r0 ∈H1 Ω be two atomic programs and let E, F be two
bundle event structures with internal probability, then

                            r∗ kr∗ vsim r∗ ,                                                       (13)
                             r∗ kr0 vsim r∗(r0 ·r∗ ),                                              (14)
                  r∗ k(b·E+c·F) vsim r∗(b·(r∗ kE)+c·(r∗ kE)),                                      (15)
                        r∗ k(r0 ·E) vsim r∗(r0 ·(r∗ kE)),                                          (16)

where r∗ = r∗1.


                                                  23
                         ∅                                                                                            /0 ∅

                                                                                                               
            δ            r                              ( 0
                                                         r                                              0/ r 0                    0.  r

                                        $                                                                                             
 δr0       rδ           rr                     rr0     r0 δ     r0 r                     r0 δ           r0 r                     1 rr 0    .2 rr

                                                                                                                                    
rδr0       rrδ rrr rrr0 rr0 δ rr0 r r0 rδ r0 rr                                         r0 rδ           rr0 r        rr0 δ       rr0 r . rrr0 0 rrr

                                                                                                                           
rrδr0                   . . .    . . .               . . .                . . .     r0 rrδ          . . .       r0 rrδ      . . .    . . .   . . .

 The “obvious” arrows, such as an arrow from r0 δ to r0 δ, have been left out to
keep the picture clear.
                                 Fig. 2. The t-simulation from r∗ kr0 to r∗(r0 ·r∗ ).

Proof. Let us denote by e1 and e2 (resp. e) the events that are labelled
by δ in the event structure associated to r∗ kr∗ (resp. r∗ ). Given a trace α
of r∗ kr∗ that does not contain any of the ei s, we denote by α0 unique trace
corresponding to α in r∗ (i.e. with the same number of events labelled by r).

A t-simulation from r∗ kr∗ to r∗ is obtained by considering a function f such
that                      
                                                      (α\{e1 , e2 })0
                                                     
                                                                                      if e1 ∈α
                                                                                            / or e2 ∈α,
                                                                                                    /
                                      f (α) =
                                                      (α\{e , e })0 e if e , e ∈α.
                                                     
                                                                1       2                1          2



The t-simulation (14) is constructed as follows. Let us abstract the event
names, i.e. rk would be a trace where each r is the label of a unique event.
Every trace of r∗ kr0 is a prefix of rm r0 rn δ or rm δr0 , for some m, n ≥ 0. Every
prefix of either trace corresponds to a unique trace of r∗(r0 ·r∗ ). For instance,
the maximal trace rm δr0 is associated to the weakly maximal trace rm r0 of
r∗(r0 ·r∗ ). Figure 2 shows an explicit construction of the t-simulation.

The Simulation (15 )is similar. Every trace of r∗ k(b·E+c·F) is a prefix of
rm bα or rm cβ or rm δbγ or rm δcζ, where α∈T (r∗ kE), β∈T (r∗ kF), γ∈T (E),
ζ∈F and n ≥ 0. Again, prefixes of the first two traces correspond to a unique
trace of r∗(b·(r∗ kE)+c·(r∗ kF)). The maximal trace rm δbγ is again mapped
to the weakly maximal trace rm bγ. Similarly for the fourth case. This indeed
results in a t-simulation.

The Simulation (16) is constructed as follows. Every trace of r∗ k(r0 ·E) is a
prefix of rm r0 α or rm δr0 β for some trace α∈T (r∗ kE) and β∈T (E). We continue
as in the previous case.                                                       2


                                                                        24
Prop. 4.16 is used mainly to interleave the right operand r∗ systematically
with the internal structure of E, while preserving the simulation order. More
precisely, these equations are applied to generate algebraic proofs for the re-
duction of one expression into another, where the occurrence of k is pushed
deeper into the sub-expressions (and possibly removed).



5   Probabilistic rely-guarantee conditions


Our first task towards the extension of the rely-guarantee method to prob-
abilistic systems is to provide a suitable definition of a rely condition that
contains sufficient quantitative information about the environment and the
components of a system.

From a relational point of view, as in Jones’ thesis [1], a guarantee condi-
tion expresses a constraint between a state and its successor by running the
relation as a nondeterministic program. Therefore, it is important to know
whether some action is executed atomically or whether it is split into smaller
components. For instance, when run in the same environment, a probabilistic
choice between x:=x+1 and x:=x−1 produced from an if...then...else
clause may behave differently from an atomic probabilistic assignment that
assigns x+1 and x−1 to x with the exact same probability.

Without probability, a common example of a guarantee condition for a given
program is the reflexive transitive closure with respect to (k) of the union of
all atomic actions in that program [25] which completely captures all possible
“effects” of the program. Such a closure property plays a crucial role in the
algebraic proof of Rule 2 is achieved through Prop. 4.16. This construction
was introduced by Jones [1] and later refined by others [11,20,25].

Non-probabilistic rely-guarantee conditions usually take the form ρ∗ for some
binary relation ρ, defined on the state space of the studied program. The
transitive closure of ρ with respect to the relational composition (·) is usually
a desirable property. To obtain a probabilistic guarantee condition from a
relation ρ⊆Ω×Ω, we construct a probabilistic program r∈H1 Ω such that

                   r(s) = {µ∈DΩ | µ({s0 | (s, s0 )∈ρ})
                                                  /    = 0}.

Equivalently, r is the convex closure of ρ. The following proposition then
follows from that construction.

Proposition 5.1 If a relation ρ⊆Ω×Ω is transitive, then the convex closure
r of ρ satisfies r·(r+δ) vH r.

Proof. Let ρ be a transitive relation, r its associated probabilistic program,


                                      25
s∈Ω a state and µ∈[r·(r+δ)](s). We need to show that µ∈r(s). By definition
of the sequential composition (·) (Eqn. (5)), there exists ν∈r(s) and a deter-
ministic program f vH (1+r) such that µ = f ?ν. Let u∈Ω such that (s, u)∈ρ,/
we are going to show that µ(u) = 0. We have:
         X                         X                                  X
µ(u) =         f (t)(s)ν(t) =                 f (t)(u)ν(t) =                         f (t)(u)ν(t).
         t∈Ω                    t∈Ω∧(s,t)∈ρ                    t∈Ω∧(s,t)∈ρ∧(t,u)∈ρ


The second equality follows from ν(t) = 0 for every (s, t)∈ρ./ Similarly, the last
equality follows from f (t)(u) = 0 for (t, u)∈ρ.
                                               / The last expression reduces to
P
  t∈Ω∧(s,u)∈ρ f (t)(u)ν(t), by transitivity of ρ, which is an empty sum because
(s, u)∈ρ.
      / Therefore, µ(u) = 0 for every (u, s)∈ρ,   / that is µ∈r(s).             2

The convex closure of a relation ρ, given in Prop. 5.1, sometimes provides a
very general rely condition that is too weak to be useful in the probabilis-
tic case. In practice, a probabilistic assignment is considered atomic and the
correctness of many protocols is based on that crucial assumption. Hence the
random choice and the writing of the chosen value into a program variable
x is assumed to happen instantaneously and no other program can modify
x during and in-between these two operations. Thus, probabilistic rely and
guarantee conditions need to capture the probabilistic information in such an
assignment.

Example 5.2 Let x be a (integer) program variable with values bounded by 0
and n. Let us write x:=uniform(0, n) for the program that assigns a random
integer between two integers 0 and n to the variable x. A probabilistic guarantee
condition for that assignment is obtained from the probabilistic program r that
satisfies, for every integer s ∈ [0, n],

                                                           1
                                                                 
                          r(s) = µ            µ({0, n}) ≥     .                               (17)
                                                          n+1

The condition r specifies the convex set of all probabilistic deterministic pro-
grams whose atomic actions establish a state in {0, n} with probability at least
 1
n+1
    . In particular, r is an overspecification of x:=uniform(0, x) where the rhs
occurrence of x is evaluated to the initial value of x. Since r is transitive, it
can prove useful to deduce quantitative properties of (x:=uniform(0, x))∗ .

In practice, constructing a useful transitive probabilistic rely-guarantee condi-
tion is difficult, but the standard technique is still valid: the strongest guaran-
tee condition of a given program is the nondeterministic choice of all atomic
actions found in that program.

Definition 5.3 A probabilistic rely or guarantee condition R is a probabilis-
tic concurrent program such that RkR vsim R.


                                                26
In particular, the concurrent program r∗ = r∗1 is a rely condition because

                                 r∗ kr∗ vsim r∗                            (18)

holds in the event structure model (Prop. 4.16 Eqn. (13)). This illustrates the
idea that a rely condition specifies an environment that can stutter or execute
a sequence of actions that are bounded by r.



6   Probabilistic rely-guarantee calculus


In this section, we develop the rely-guarantee rules governing programs in-
volving probability and concurrency. An example is given by Rule 2, which
allows us check the safety properties of the subsystems and infer the correct-
ness of the whole system in a compositional fashion. We provide a probabilistic
version of that rule.

In the previous sections, we have developed the mathematical foundations
needed for our interpretation of Hoare triples and guarantee relations, namely,
the sequential refinement v and simulation-based order vsim . Following [25],
we only adapt the orders in the algebraic interpretation of rely-guarantee quin-
tuples (Eqn. (1)). That is, validity of probabilistic rely-guarantee quintuples
is captured by

               {P R}E{G Q} ⇔ P ·(RkE) v Q ∧ E vsim G,

where P, E and Q are probabilistic concurrent programs and R and G are rely-
guarantee conditions. The first part is seen as a probabilistic instance of the
contraction of [7] which specifies the functional behaviour of RkE under a pre-
condition P . The second part uses the simulation order which is compositional
and very sensitive to the structural properties of the program.

The conditions R and G specify how the component E interacts with its en-
vironment. As we have discussed in the previous section, rely and guarantee
conditions are obtained by taking r∗ = r∗δ for some atomic probabilistic pro-
gram r. Therefore, E vsim r∗ implies that all actions carried by events in E
are either stuttering or satisfying the specification r. This corresponds to the
standard approach of Jones [20,1].

The following rules are probabilistic extensions of the related rely-guarantee
rules developed in [8,20]. These rules are sound with respect to the event
structure semantics of Section 4.

Atomic action: The rely-guarantee rule for an atomic statement r0 is pro-


                                      27
vided by the equation
                              r∗ kr0 vsim r∗(r0 ·r∗ )                        (19)
where r is the rely condition. This equation shows that a (background) pro-
gram satisfying the rely condition r will not interfere with the low level opera-
tions involved in the atomic execution of r0 . The programs will be interleaved.

Conditional statement: The rely-guarantee rule for conditional statement
is provided by the equation

                   r∗ k(b·E+c·F) vsim r∗(b·(r∗ kE)+c·(r∗ kF)).                  (20)

This equation shows how a rely condition r∗ distributes through branching
structures. The tests b and c are assumed to be atomic and their disjunction
is always true (this is necessary for feasibility). This assumption may be too
strong in general because b may involve the reading of some large data that is
too expensive to be performed atomically. However, we may assume that such
a reading is done before the guard b is checked and the non-atomic evaluation
of the variables involved in b may be assigned to some auxiliary variable that
is then checked atomically by b.

Prefixing: the sequential rely-guarantee rule for a probabilistic program
expressed using prefixing. We have

                          r∗ k(r0 ·E) vsim r∗(r0 ·(r∗ kE)).                     (21)

It generalises Rule 19 and tells us that a rely condition r∗ distributes through
the prefixing operation. In other words, the program r0 and E should tolerate
the same rely condition in order to prove any meaningful property of r·E. This
results from of our interpretation of k where no synchronisation is assumed.

Concurrent execution: in Rule 2, the concurrent composition EkE 0 requires
an environment that satisfies R∩R0 to establish the postcondition Q∩Q0 . How-
ever, such an intersection is not readily accessible at the structural level of
event structures. Therefore, the most general probabilistic extension of Rule 2
which applies to our algebraic setting is:

   {P R}E{G Q}           {P R0 }E 0 {G0 Q0 }   G vsim R0        G0 vsim R
                                                                            ,   (22)
                           {P R00 }EkE 0 {GkG0 Q}

where R00 is a rely condition such that R00 vsim R and R00 vsim R0 . The proof of
this rule is exactly the same as in [8,21]. In fact, we have R00 vsim R, E 0 vsim R,
RkR vsim R, therefore Eqn. (7) and Equational Implication (11) imply

                      R00 k(E 0 kE) vsim Rk(RkE) vsim RkE,

and we obtain P ·R00 k(E 0 kE) vsim P ·(RkE) by Eqn. (10). It follows from
Thm. 4.13 that P ·R00 k(E 0 kE) v Q.


                                        28
The conclusion does not contain any occurrence of Q0 , but by symmetry, it
is also valid if Q0 is substituted for Q. The combined rely condition R00 is
constructed such that it is below R and R0 . Indeed, if R, R0 have a greatest
lower bound with respect to vsim , then R00 can be taken as that bound, so
that the strengthening of the rely is as week as possible.

The above rule can be specialised by considering rely-guarantee conditions of
the form r∗ , where r is an atomic probabilistic program. The following rule
is expressed in exactly as in the standard case [8]. This is possible because
probabilities are internal.

Proposition 6.1 The following rule is valid in BES:

    {P r1∗ }E1 {g1∗ Q1 }    {P r2∗ }E2 {g2∗ Q2 }      g1 vH r2    g2 vH r1
                                   ∗                  ∗
                                                                             ,   (23)
                       {P (r1 ∩r2 ) }E1 kE2 {(g1 +g2 ) Q1 }

where r, r0 , g, g 0 ∈H1 Ω and g+g 0 is the nondeterministic choice on H1 Ω.

Proof. This follows from substituting R and G by respectively r∗ and g ∗
in Rule 22. Moreover g ∗ kg 0∗ vsim (g+g 0 )∗ holds because (g+g 0 )∗ k(g+g 0 )∗ vsim
(g+g 0 )∗ (Eqn. (18)).                                                             2

Recall that the nondeterministic choice of H1 Ω is obtained by the pointwise
union followed by the necessary closure properties for the elements of H1 Ω.
The intersection r∩r0 is obtained by pointwise intersection.

Iteration: a while program is modelled by using the binary Kleene star. The
idea is to unfold the loop as far as necessary. The conditional and prefix
(sequential) cases can then be applied on the unfolded structure to distribute
the rely condition. That is, we write


                 r∗ k((b·E)∗c) vsim r∗(c·r∗ +b·(r∗ k[E·(b·E∗c)])).


If E is sequential, then r∗ can be “interleaved” within the internal structure
of E·(b·E∗c) by applying the prefixing and conditional statement rules.

The sequential correctness is achieved by the usual generation of probability
distributions, obtained from terminating sequential behaviours, on the “to-
tally” unfolded event structure (assuming that E is sequential). The sequential
behaviours are usually obtained by interleaving the rely condition r∗ through
the internal structure of the unfolded loop. A bounded loop, such as a for loop,
should be modelled using a sequence of sequential compositions or prefixing.


                                         29
7   Application: a faulty Eratosthenes sieve


In this section, we show how to use the previously established rely-guarantee
rules to verify a probabilistic property of a faulty Eratosthenes sieve, which is
a quantitative variant Jones’ example [1].

Let n ≥ 2 be a√natural number and s0 = {2, 3, . . . , n}. For each integer i such
that 2 ≤ i ≤ n, we consider a program thdi that sequentially removes all
(strict) multiples of i from the shared set variable s with a fixed probability
p. More precisely, each thread thdi is implemented as the following program:

                  for(j = 2 to n/i)
                         ui,j : skip ⊕p remove(i*j from s);

where n/i is the integer division of n by i. Each ui,j can be seen as a faulty
action that removes the product ij from the current value of s with probability
p. The state space of each atomic deterministic program ui,j is Ω = {s | s⊆s0 }.
In H1 Ω, ui,j is defined by ui,j (s) = (1−p)δs +pδs\{ij} . The whole system is
specified by the concurrent execution
                                                 √
                                             n
                        thd2 k...kthd√n = ki=2 (ui,2 · · · ui,n/i ).
                        √
where, in the sequel,       n is computed without decimals.

Let π={2, 3, . . . , m} be the set of prime numbers in s0 . Our goal is to compute
a “good” lower bound probability that the final state is π, after executing the
threads thdi concurrently, from the initial state s0 .

We denote by Oi,j = {s | ij ∈s}
                            / ⊆ Ω and

               Qi,j (s) = {µ∈DΩ | µ(Oi,j )≥p ∧ µ({s0 | s0 ⊆s})=1}

a specification of a probabilistic program that removes ij from the state s with
                                                                             n/i
at least probability p and does not add anything to it. We define Oi = ∩j=2 Oi,j ,
Qi = Qi,2 ·Qi,3 · . . . ·Qi,n/i and r to be the probabilistic program such that r(s)
is the convex closure of {δs0 | s0 ⊆s}.

First, we show that every thread thdi guarantees r∗ . Second, we show that
thdi establishes Qi when run in an environment satisfying r, i.e. r∗ kthdi v Qi ,
using the atomic and prefix rules 19 and     √
                                                21. Finally, we apply the concur-
                                               n
rency rule 23 to deduce that the system ki=2     thdi establishes all postconditions
                 √
Q2 , Q3 , . . . Q n , when run in an environment satisfying r.

Establising thdi vsim r∗ and r∗ kthdi v Qi


                                            30
On the one hand, it is clear that ui,j vH r, for every i, j, and thus thdi vsim r∗
follows from the unfold (8). On the other hand, let us show that r∗ kthdi v Qi .
Multiple applications of the prefix-case give

                  r∗ kthdi vsim r∗(ui,2 ·(r∗(ui,3 ·(. . . r∗(ui,n/i ·r∗ ))))).

Since the right multiplication X 7→ X·r, by any program r∈H1 Ω, is the lower
adjoint in a Galois connection [5], the fixed point fusion theorem [26] implies

       r∗(ui,2 ·(r∗(ui,3 ·(. . . r∗(ui,n/i ·r∗ ))))) = r∗ ·ui,2 ·r∗ ·ui,3 · . . . r∗ ·ui,n/i ·r∗ ,

where the equality is in H1 Ω. Thus,

                         r∗ kthdi v r∗ ·ui,2 ·r∗ ·ui,3 · . . . ·r∗ ·ui,n/i ·r∗

follows from the fact that v is weaker than vsim (Thm. 4.13). The right hand
side explicitly states the interleaving of the rely condition r∗ in-between the
atomic executions in thdi as in [20].

Moreover, since r is the probabilistic version of a transitive binary relation,
Prop. 5.1 implies that r·(r+δ) vH r. Since H1 Ω is a probabilistic Kleene
algebra [27], the right induction law of pKA implies r∗ = δ+r. This reduction
of r∗ to δ+r illustrates the practical importance of transitive rely conditions.
Therefore,

               r∗ kthdi v (δ+r)·ui,2 ·(δ+r)·ui,3 · . . . (δ+r)·ui,n/i ·(δ+r),

where the left hand side is a sequential program (thus Prop. 4.8 enables us to
use the definition of sequential composition of H1 Ω) directly . Since ui,j v Qi,j ,
it remains to show that (δ+r)·Qi,2 ·(δ+r)·Qi,3 · . . . (δ+r)·Qi,n/i ·(δ+r) v Qi .

First we show that Qi,j ·(δ+r) v Qi,j and (δ+r)·Qi,j v Qi,j . Let s∈Ω and
ν∈(Qi,j ·(δ+r))(s). By definition of the sequential composition in H1 Ω, there
exists a probabilistic deterministic program f vH δ+r and a distribution
µ∈Qi,j (s) such that ν(s0 ) = t∈Ω f (t)(s0 )µ(t), for every s0 ∈Ω. Therefore,
                             P



            ν(Oi,j ∩{s0 | s0 ⊆s}) =
                                         X                            X
                                               f (t)(Oi,j )µ(t) =           f (t)(Oi,j )µ(t),
                                         t∈Ω                          t⊆s
where the second equality follows from µ({t | t6⊆s})=0, for every µ∈Qi,j . We
deduce t⊆s f (t)(Oi,j )µ(t) ≥ p, i.e. ν∈Qi,j (s), by observing
       P

      X                             X
            f (t)(Oi,j )µ(t) ≥               f (t)(Oi,j )µ(t) = µ(Oi,j ∩{t | t⊆s}) ≥ p,
      t⊆s                        ij ∈t∧t⊆s
                                    /

because f (t)(Oi,j )=1 for every t such that ij ∈t
                                                / and µ(Oi,j ∩{t | t⊆s}) = µ(Oij )
for every µ∈Qi,j (s). Consequently, Qi,j ·(δ+r) v Qi,j . Similarly, we can show
that (δ+r)·Qi,j v Qi,j and thus r∗ kthdi v Qi .


                                                  31
                                               √
                                  n
Establising the property of r∗ ki=2 thdi
                    √                                                 √
Applying the rule 23 n−1 times, we obtain, for every Qj such that 2≤j≤ n,
                                           √
                                            n
                                      r∗ ki=2 thdi v Qj .

Inferring a lower bound for the probability of correctness

Unfortunately, Rule 23 does not give any explicit quantitative bound in term
of probability for correctness. It does provide quantitative correctness, but all
the probabilities are buried in the Qi .

To obtain an explicit lower bound for the probability of removing all composite
numbers, we first study the case of two threads that run concurrently. We know
from Rule 23 that r∗ kthd2 kthd3 v Q2 and r∗ kthd2 kthd3 v Q3 . Therefore,
for every µ∈[[r∗ kthd2 kthd3 ]](s0 ), we have µ(O2 ) ≥ pn/2−1 and µ(O3 ) ≥ pn/3−1
because there are n/2−1 (resp. n/3−1) multiples of 2 (resp. 3) in [3, n] (resp.
[4, n]). Therefore, µ(O1 ∪O2 )+µ(O2 ∩O3 ) = µ(O1 ) + µ(O2 ) ≥ pn/2−1 +pn/3−1 and

                        µ(O2 ∩O3 ) ≥ p /2−1 +p /3−1 −1.
                                                    n    n
                                                                      (24)
In the construction of the lower bound in Eqn. (24), we have only used the
modularity of measures and, therefore, it can be transformed into a more
general rely-guarantee rule with explicit probabilities (Prop. 7.1).

Given a subset O⊆Ω and p∈[0, 1], we write [[E]](s0 )(O) ≥ p if for every
µ∈[[E]](s0 ) we have µ(O) ≥ p.

Proposition 7.1 For every initial state s0 and for all subsets O1 , O2 ⊆Ω,
[[r1∗ kE1 ]](s0 )(O1 ) ≥ p1 [[r2∗ kE2 ]](s0 )(O2 ) ≥ p2 E1 vsim g ∗ vsim r2∗ E2 vsim g 0∗ vsim r1∗
                                                                                                   .
                [[(r1 ∩r2 )∗ kE1 kE2 ]](s0 )(O1 ∩O2 ) ≥ p1 +p2 −1  E1 kE2 vsim (g+g 0 )∗


Proof. Let µ ∈ [[(r1 ∩r2 )∗ kEkE2 ]](s0 ), we need to show that µ(O1 ∩O2 ) ≥
p1 +p2 −1 with the above definition of p1 and p2 .

Let us define Q1 to be the (single event) ipBES whose event is labelled by the
probabilistic program u1 such that u1 (s0 ) = {µ | µ(O1 )≥p1 } else u1 (s) = DΩ
for s 6= s0 . Similarly, we define Q2 . Then the premises imply r1∗ kE1 v Q1 and
r2∗ kE2 v Q2 . By Prop. 6.1, we have

      [[(r1 ∩r2 )∗ kE1 kE2 ]] vH [[Q1 ]]           and   [[(r1 ∩r2 )∗ kE1 kE2 ]] vH [[Q2 ]].

Therefore µ(O1 ) ≥ p1 and µ(O2 ) ≥ p2 . Modularity of finite measures implies
that µ(O1 ∩O2 )+µ(O1 ∪O2 ) = µ(O1 )+µ(O2 ) ≥ p1 +p2 . Hence, µ(O1 ∩O2 ) ≥
p1 +p2 −µ(O1 ∪O2 ) ≥ p1 +p2 −1 since µ(O1 ∪O2 ) ≤ 1.

The simulation E1 kE2 vsim (g+g 0 )∗ is also clear from Prop. 6.1.                             2


                                                   32
We know from the above discussion that

                     [[r∗ kthd2 kthd3 ]](s0 )(O2 ∩O3 ) ≥ p /2−1 +p /3−1 −1.
                                                               n           n




Applying Prop. 7.1 on thd2 kthd3 and thd4 yields

         [[r∗ kthd2 kthd3 kthd4 ]](s0 )(O2 ∩O3 ∩O4 ) ≥ p /2−1 +p /3−1 +p /4−1 −2.
                                                                   n           n   n



         √
Thus         n−1 applications of Prop. 7.1 give
                                                 √
                                                   n
                 ∗
                     √
                      n
                                      √
                                        n                     √
                                                     p /i−1 −( n−2) = f (p, n).
                                                      n
                                                 X
               [[r ki=2 thdi ]](s0 )(∩i=2 Oi ) ≥
                                                 i=2

The lower bound f (p, n) sometimes provides √a bad lower-approximation for
                                                 n
the probability that the system establishes ∩i=2   Oi . However, it is clear that
limp→1 f (p, n) = f (1, n) = 1.
                                               √
In the particular case of n = 15, we have 15 = 3 and we only need to
consider thd2 and thd3 so that f (p, 15) = p6 +p4 −1. The plot of f (p, 15) in
Fig. 3 shows that f (p, 15) gives a positive lower bound when p ≥ 0.868, the
exact probability being p10 +4p9 (1−p)+4p8 (1−p)2 .

Refining the lower bound

We can use other internal properties of the system to obtain a better lower
bound. It is clear that Oi is an invariant for every thdj (for j6=i) and that all
actions ui,j (sequentially) commute with each other. Thus, we should obtain
a better lower bound by noticing that the system is “sequentially better”
than the following interleaving: thd2 removes all (strict) multiples of 2, thd3
removes all multiples of 3 assuming that all multiples of lcm0 (2, 3) (the lowest
common multiple of 2 and 3 that is strictly greater than both) have been
removed by thd2 , and so on 9 . Thus
     √                   √
        n                 n
[[r∗ ki=2                   Oi ) ≥ p /2−1 p /3−1−[ /6] p /4−1−[ /4−1] p /5−1−[ /10+ /15− /30] · · ·
                                        n    n         n   n           n       n   n   n   n
          thdi ]](s0 )(∩i=2
                                 = g(p, n),

where the square-bracketed terms are the numbers of multiples remove by
threads with smaller indices. For example, before thd5 runs, thd2 removes n/10
multiples of lcm0 (2, 5), thd3 removes n/15−n/30 multiples of lcm0 (3, 5) (not mul-
tiples of lcm0 (2, 5)), thus thd5 removes the remaining n/5−1−[n/10+n/15−n/30]
multiples of 5. In the particular case of n = 15, this yields

                     g(p, 15) = p /2−1 p /3−1− /6 = p7−1+5−1−2 = p8 .
                                   15       15        15



9 The probability of removing all composite numbers is usually above that bound
because 6 can be removed by either thd2 or thd3 .


                                                 33
Fig. 3. Comparison of the quantities f (p, 15) (dotted), g(p, 15) (dashed) and the
actual probability p10 +4p9 (1−p)+4p8 (1−p)2 (solid).

A graphical comparison of f, g and the actual probability is displayed in Fig-
ure 3 for n = 15.
                                   √
                               n
Establising the property of ki=2 thdi
                         √                             √
                          n                              n
Finally, notice that ∅∈∩i=2 Oi which means that r∗ ki=2    thdi can establish s = ∅
with a positive probability. This issue is resolved by using
                                                        √
                                                              a stronger guarantee
                                                          n
property such as “ui,j never removes√i”. Therefore, ki=2 thdi never removes any
                                       n
prime numbers i.e. any element of ∩i=2   Oi , that does not contain all the positive
prime numbers below n, occurs with probability 0.



8   Conclusion


We have presented an extension of the rely-guarantee calculus that accounts
for probabilistic programs running in a shared variable environment. The rely-
guarantee rules are expressed and derived by and large by using the algebraic
properties of a bundle event structure semantics for concurrent programs.

In our approach, the specification of a probabilistic concurrent program is
expressed with a rely-guarantee quintuple. Each quintuple is defined alge-
braically through the use of a sequential order v, which captures all possible
sequential behaviours when a suitable definition of the concurrency operation
k is given, and a simulation order vsim , which specifies the level of interference
between the specified component and the environment. Various probabilistic
rely-guarantee rules have been established and applied on a simple example
of a faulty concurrent system. We have also shown some rules that provide
explicit quantitative properties, including a lower bound for the probability
of correctness. In particular, a better lower-approximation can be derived if
further internal properties of the systems are known.


                                        34
The framework developed in this paper has its current limitations. Firstly,
neither the algebra nor the event structure model support non-terminating
probabilistic concurrent programs at the moment. That is, the rely-guarantee
rules of this paper can only be applied in a partial correctness setting. Secondly,
the concrete model is restricted to programs with finite state spaces. We will
focus particularly on the first limitation in our future work.



References


[1] C. B. Jones, Development methods for computer programs including a notion
     of interference, Ph.D. thesis, Oxford University (June 1981).
[2] D. Kozen, Semantics of probabilistic programs, J. Comput. Syst. Sci. 22 (3)
     (1981) 328–350.
[3] C. Jones, Probabilistic non-determinism, Ph.D. thesis, University of Edinburgh,
     Scotland, UK (1989).
[4] J. He, K. Seidel, A. McIver, Probabilistic models for the guarded command
     language, Sci. Comput. Program. 28 (2-3) (1997) 171–192.
[5] A. K. McIver, C. C. Morgan, Abstraction, Refinement And Proof For
     Probabilistic Systems, SpringerVerlag, 2004.
[6] R. Segala, N. A. Lynch, Probabilistic simulations for probabilistic processes.,
     Nord. J. Comput. 2 (2) (1995) 250–273.
[7] A. Armstrong, V. B. F. Gomes, G. Struth, Algebraic principles for rely-
     guarantee style concurrency verification tools, in: C. B. Jones, P. Pihlajasaari,
     J. Sun (Eds.), FM 2014, 2014, pp. 78–93.
[8] C. A. R. Hoare, B. Möller, G. Struth, I. Wehrman, Concurrent Kleene algebra
     and its foundations, J. Log. Algebr. Program. 80 (6) (2011) 266–296.
[9] S. L. Bloom, Z. Ésik, Free shuffle algebras in language varieties, Theoretical
     Computer Science 163 (1&2) (1996) 55–98.
[10] A. Tarlecki, A language of specified programs., Sci. Comput. Program. 5 (1)
     (1985) 59–81.
[11] J. Dingel, A refinement calculus for shared-variable parallel and distributed
     programming., Formal Asp. Comput. 14 (2) (2002) 123–197.
[12] J. W. Coleman, C. B. Jones, A structural proof of the soundness of Rely-
     guarantee rules., J. Log. Comput. 17 (4) (2007) 807–841.
[13] F. S. de Boer, U. Hannemann, W. P. de Roever, A compositional proof system
     for shared variable concurrency., in: J. S. Fitzgerald, C. B. Jones, P. Lucas
     (Eds.), FME, Vol. 1313 of LNCS, Springer, 1997, pp. 515–532.
[14] G. Winskel, Events in computation, Ph.D. thesis, University of Edinburgh,
     Scotland, UK (1980).
[15] G. Winskel, Event structures, in: W. Brauer, W. Reisig, G. Rozenberg (Eds.),
     Advances in Petri Nets, 1986, pp. 325–392.
[16] R. Langerak, Bundle event structures: a non-interleaving semantics for LOTOS,
     Memoranda informatica, University of Twente, 1992.


                                         35
[17] J.-P. Katoen, R. Langerak, D. Latella, Modeling systems by probabilistic
     process algebra: An event structures approach, in: TC6/WG6.1, FORTE ’93,
     North-Holland Publishing Co., The Netherlands, 1994, pp. 253–268.
[18] J. P. Katoen, Quantitative and qualitative extensions of event structures, Ph.D.
     thesis, University of Twente (1996).
[19] D. Varacca, Probability, nondeterminism and concurrency: two denotational
     models for probabilistic computation, Ph.D. thesis, University of Aarhus (2003).
[20] I. J. Hayes, C. B. Jones, C. R. J., Refining rely-guarantee thinking, Tech. rep.,
     Newcastle University, United Kingdom (2012).
[21] A. K. McIver, T. M. Rabehaja, G. Struth, Probabilistic concurrent Kleene
     algebra, in: L. Bortolussi, H. Wiklicky (Eds.), QAPL, Vol. 117 of EPTCS, 2013,
     pp. 97–115.
[22] S. Georgievska, S. Andova, Retaining the probabilities in probabilistic testing
     theory, in: L. Ong (Ed.), FOSSACS, Vol. 6014 of LNCS, Springer, 2010, pp.
     79–93.
[23] S. Georgievska, S. Andova, Probabilistic may/must testing: retaining
     probabilities by restricted schedulers, FAC 24 (4-6) (2012) 727–748.
[24] A. K. McIver, T. M. Rabehaja, G. Struth, An event structure model for
     probabilistic concurrent Kleene algebra., in: K. L. McMillan, A. Middeldorp,
     A. Voronkov (Eds.), LPAR, Vol. 8312 of LNCS, Springer, 2013, pp. 653–667.
[25] C. A. R. Hoare, B. Möller, G. Struth, I. Wehrman, Concurrent Kleene algebra.,
     in: M. Bravetti, G. Zavattaro (Eds.), CONCUR, Vol. 5710 of LNCS, Springer,
     2009, pp. 399–414.
[26] R. Backhouse, Galois connections and fixed point calculus, in: R. Backhouse,
     R. Crole, J. Gibbons (Eds.), ACM/MPC, Vol. 2297 of LNCS, Springer Berlin
     Heidelberg, 2002, pp. 89–150.
[27] A. K. McIver, T. Weber, Towards automated proof support for probabilistic
     distributed systems, in: G. Sutcliffe, A. Voronkov (Eds.), LPAR, Vol. 3835 of
     LNAI, Springer, 2005, pp. 534–548.




                                         36
A     Axioms of Kleene algebra and related structures


A.1    Idempotent semiring


An idempotent semiring is an algebraic structure (K, +, ·, 0, 1) such that, for
every x, y, z∈K, the following axioms hold


            x + x = x,                                                       (A.1)
            x + y = y + x,                                                   (A.2)
      x + (y + z) = (x + y) + z,                                             (A.3)
            x + 0 = x,                                                       (A.4)
              x·1 = x,                                                       (A.5)
              1·x = x,                                                       (A.6)
          x·(y·z) = (x·y) · z,                                               (A.7)
              0·x = 0,                                                       (A.8)
              x·0 = 0,                                                       (A.9)
        (x + y)·z = x·z + y · z,                                            (A.10)
        x·y + x·z = x·(y + z).                                              (A.11)



A.2    Kleene algebra


A Kleene algebra is an algebraic structure (K, +, ·,∗ , 0, 1) where (K, +, ·, 0, 1)
is an idempotent semiring and the Kleene star (∗ ) satisfies Kozen’s axioms:


               x∗ = 1 + x·x∗ ,                                              (A.12)
      z + x·y ≤ y ⇒ x∗ ·z ≤ y,                                              (A.13)
      z + y·x ≤ y ⇒ z·x∗ ≤ y.                                               (A.14)

The induction laws A.13 (resp. A.14) implies that x∗ is the least fixed point
of λy.1 + x·y (resp. λy.1 + y·x).



A.3    Probabilistic Kleene algebra


A probabilistic Kleene algebra has the same signature as Kleene algebra but
weakens the distributivity law A.11 and the induction rule A.14 to:


                                       37
              x·y + x·z ≤ x·(y + z),                                   (A.15)
      z + y·(x + 1) ≤ y ⇒ z·x∗ ≤ y.                                    (A.16)


A.4    Concurrent Kleene algebra


A concurrent Kleene algebra is composed of a Kleene algebra (K, +, ·,∗ , 0, 1)
and a commutative Kleene algebra (K, +, k,(∗) , 0, 1) (i.e. k is commutative)
linked by the interchange law:


      (xky) · (x0 ky 0 ) ≤ (x · x0 )k(yky 0 ).                         (A.17)




                                                 38
