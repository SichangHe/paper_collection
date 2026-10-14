                                         An Infinite Needle in a Finite Haystack: Finding Infinite
                                         Counter-Models in Deductive Verification
                                         NETA ELAD, Tel Aviv University, Israel
                                         ODED PADON, VMware Research, USA
arXiv:2310.16762v3 [cs.LO] 10 Sep 2024




                                         SHARON SHOHAM, Tel Aviv University, Israel
                                         First-order logic, and quantifiers in particular, are widely used in deductive verification of programs and
                                         systems. Quantifiers are essential for describing systems with unbounded domains, but prove difficult for
                                         automated solvers. Significant effort has been dedicated to finding quantifier instantiations that establish
                                         unsatisfiability of quantified formulas, thus ensuring validity of a system’s verification conditions. However, in
                                         many cases the formulas are satisfiable—this is often the case in intermediate steps of the verification process,
                                         e.g., when an invariant is not yet inductive. For such cases, existing tools are limited to finding finite models
                                         as counterexamples. Yet, some quantified formulas are satisfiable but only have infinite models, which current
                                         solvers are unable to find. Such infinite counter-models are especially typical when first-order logic is used to
                                         approximate the natural numbers, the integers, or other inductive definitions such as linked lists, which is
                                         common in deductive verification. The inability of solvers to find infinite models makes them diverge in these
                                         cases, providing little feedback to the user as they try to make progress in their verification attempts.
                                            In this paper, we tackle the problem of finding such infinite models, specifically, finite representations
                                         thereof that can be presented to the user of a deductive verification tool. These models give insight into the
                                         verification failure, and allow the user to identify and fix bugs in the modeling of the system and its properties.
                                         Our approach consists of three parts. First, we introduce symbolic structures as a way to represent certain
                                         infinite models, and show they admit an efficient model checking procedure. Second, we describe an effective
                                         model finding procedure that symbolically explores a given (possibly infinite) family of symbolic structures in
                                         search of an infinite model for a given formula. Finally, we identify a new decidable fragment of first-order
                                         logic that extends and subsumes the many-sorted variant of EPR, where satisfiable formulas always have a
                                         model representable by a symbolic structure within a known family, making our model finding procedure a
                                         decision procedure for that fragment.
                                            We evaluate our approach on examples from the domains of distributed consensus protocols and of heap-
                                         manipulating programs (specifically, linked lists). Our implementation quickly finds infinite counter-models
                                         that demonstrate the source of verification failures in a simple way, while state-of-the-art SMT solvers and
                                         theorem provers such as Z3, cvc5, and Vampire diverge or return “unknown”.

                                         CCS Concepts: • Networks → Protocol testing and verification; • Software and its engineering → Software
                                         verification; • Theory of computation → Logic and verification; Automated reasoning.

                                         Additional Key Words and Phrases: deductive verification, counter-models, infinite models, Paxos

                                         ACM Reference Format:
                                         Neta Elad, Oded Padon, and Sharon Shoham. 2024. An Infinite Needle in a Finite Haystack: Finding Infinite
                                         Counter-Models in Deductive Verification . Proc. ACM Program. Lang. 8, POPL, Article 33 (January 2024),
                                         38 pages. https://doi.org/10.1145/3632875

                                         Authors’ addresses: Neta Elad, Tel Aviv University, Tel Aviv, Israel, netaelad@mail.tau.ac.il; Oded Padon, VMware Research,
                                         Palo Alto, USA, oded.padon@gmail.com; Sharon Shoham, Tel Aviv University, Tel Aviv, Israel, sharon.shoham@cs.tau.ac.il.


                                         Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and
                                         the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses,
                                         contact the owner/author(s).
                                         © 2024 Copyright held by the owner/author(s).
                                         ACM 2475-1421/2024/1-ART33
                                         https://doi.org/10.1145/3632875


                                                                           Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:2                                                                       Neta Elad, Oded Padon, and Sharon Shoham


1      INTRODUCTION
A plethora of tools and techniques have emerged in recent years that use first-order logic (FOL)
with quantifiers for verification [Ball et al. 2014; Feldman et al. 2017; Goel and Sakallah 2021a,b;
Hance et al. 2021; Itzhaky et al. 2013; Karbyshev et al. 2017; Koenig et al. 2022; Löding et al. 2018;
Ma et al. 2019; Mathur et al. 2020; McMillan and Padon 2018; Murali et al. 2022; Padon et al. 2017,
2022; Taube et al. 2018; Yao et al. 2022, 2021]. These works all use quantified formulas in FOL to
encode the behavior of systems and specify desired properties and inductive invariants. Using FOL
to model (or abstract) verification problems has the advantage of completeness, meaning that every
formula has either a refutation or a satisfying model. Furthermore, FOL allows quantification, which
is essential for reasoning about unbounded domains, such as the set of processes participating in
a distributed protocol, the set of messages exchanged in a network, or the set of objects in the
heap. Following previous work, we target FOL without theories, which focuses the verification
challenge on dealing with quantifiers, while side-stepping the difficulty of combining theories with
quantifiers and uninterpreted symbols.
   Quantifiers provide expressivity, but pose a significant challenge for automated verification. SMT
solvers [Barbosa et al. 2022; de Moura and Bjørner 2008; Dutertre and De Moura 2006] and theorem
provers [Riazanov and Voronkov 1999; Weidenbach et al. 2009] often struggle and diverge while
searching for a refutation or a satisfying model, in which case they time out or return “unknown”.
   In many cases this divergence is not simply bad luck, but a result of a more fundamental problem:
formulas that are satisfiable but only have infinite models. Though infinite models typically do not
represent concrete states of a system, their existence may arise from the use of FOL to approximate
a stronger logic, for example least fixed-point. In such cases, the solution is to add additional
axioms that eliminate spurious behaviors [Hozzová et al. 2021; Löding et al. 2018; Murali et al.
2022; Reynolds and Kuncak 2015]. Infinite counter-models could provide useful guidance on how
to refine the FOL modeling with additional axioms, and ultimately allow the user to successfully
complete the verification task. However, existing solvers cannot find infinite counter-models. As a
result, when the FOL modeling is still missing some axiom (e.g., an induction principle), solvers
diverge, leaving the user with an inconclusive result and no actionable information.
   While a significant amount of research has been dedicated to developing algorithms and heuristics
for finding quantifier instantiations for refutation [Bansal et al. 2015; Bradley et al. 2006; de Moura
and Bjørner 2007; Detlefs et al. 2005; Dross et al. 2016; Ge and de Moura 2009; Jacobs 2009; Vazou
et al. 2018], ensuring that finite models exist [Itzhaky et al. 2013; Padon et al. 2017; Taube et al.
2018], and discovering finite models [Lynch 2013; Reger et al. 2016; Reynolds et al. 2013a,b], less
attention has been given to finding infinite models in the context of verification. Although there
are works on proving the existence or constructing infinite models (e.g., based on a saturated set
of clauses in resolution-based theorem proving [Bachmair and Ganzinger 2001; Peltier 2003], or
using the model evolution calculus [Baumgartner et al. 2006; Baumgartner and Tinelli 2003]; see
Sec. 8 for further discussion), finding infinite models has not (yet) made its way into common
verification frameworks based on SMT solvers. In this paper, we aim for a technique for finding
infinite models that can work well in the context of SMT-based deductive verification. To that end,
we seek a representation of first-order structures that captures models that appear in real-world
problems, admits an effective search procedure, and can be communicated to users.
   This paper develops a finite representation of (certain) infinite models, and an effective search
procedure for such models. Our key observation is that many of the infinite models arising in
practice have repeating patterns that can be summarized in a finite way. We are motivated by
examples from various domains such as heap-manipulating programs (in particular usage of linked
lists) [Löding et al. 2018; Murali et al. 2022] and distributed protocols [Padon et al. 2017, 2016] where


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                  33:3


a linearly ordered set is used to model reachability of objects in the heap or consecutive rounds of
execution (respectively). Importantly, these linear orders are intended to be finite, but may be infinite
under FOL semantics. Accordingly, we introduce symbolic structures as finite representations of
possibly infinite models. Symbolic structures use finitely many summary nodes to capture possibly
infinite sets of elements, and use the language of Linear Integer Arithmetic (LIA) to describe
repeating patterns. This allows us to check if a symbolic structure satisfies an FOL formula by
translating the formula into a (quantified) LIA formula, which solvers such as Z3 [de Moura and
Bjørner 2008] or cvc5 [Barbosa et al. 2022] can solve quickly. Our LIA-based symbolic structures
are particularly useful when verification uses FOL to (soundly) abstract common linear orders such
as the natural numbers or the integers, or to model (semi-) linear data structures such as linked
lists.
   Given that checking if a specific symbolic structure satisfies a formula is reducible to LIA, we can
obtain a procedure that searches for a symbolic model (i.e., a satisfying symbolic structure) for a
given formula by enumerating symbolic structures. However, such a procedure is inefficient. Instead
of enumerating all possible symbolic structures, we introduce an algorithm that can efficiently
search a (possibly infinite) space of symbolic structures, given by a template. A template specifies
the number of symbolic-structure nodes, as well as a subset of the LIA language to be used within
the symbolic structures. The search algorithm avoids explicitly constructing all potential symbolic
structures. Rather, it symbolically encodes the entire family of symbolic structures described by the
template into a single (quantified) LIA formula that, when satisfiable, induces a symbolic model
for the FOL formula at hand. This search procedure is sound for establishing the satisfiability of
any formula in FOL: if a symbolic structure is found, the formula is satisfiable. Further, we suggest
a simple heuristic template, parameterized by size, that captures non-trivial infinite models for a
variety of examples. As a notable example, using such a template, we are able to find an infinite
counter-model showing that the original inductive invariant of the Paxos distributed consensus
protocol [Lamport 1998] is not inductive in its FOL formalization given in [Goel and Sakallah
2021b].
   Although not every satisfiable FOL formula has a symbolic model (as expected, given that
satisfiability in FOL is not recursively enumerable), we identify a new decidable fragment of FOL
where that is the case, i.e., each satisfiable formula has a symbolic model. We further prove a “small
symbolic model property,” (1) bounding the size of potentially satisfying symbolic structures for
formulas in the fragment, and (2) characterizing a finite subset of the LIA language that is sufficient
for them. This makes our search algorithm a decision procedure for the fragment. Interestingly, our
decidability proof departs from the widely-used approach of establishing a finite model property,
as the underlying models we consider are infinite.
   The new decidable fragment, called Ordered Self Cycle (OSC), is an extension of the many-sorted
variant of the decidable Effectively PRopositional fragment (EPR, also known as the Bernays-
Schönfinkel-Ramsey class) [Lewis 1980; Ramsey 1930]1 . Many-sorted EPR already proved useful in
verifying systems from various domains, e.g., distributed protocols [Padon et al. 2017], networking
systems [Ball et al. 2014], and heap-manipulating programs [Itzhaky et al. 2014, 2013]. OSC extends
many-sorted EPR in that it relaxes some of the restrictions on quantifier alternations and function
symbols. Namely, OSC allows one sort, equipped with a linear order, to have cyclic functions (i.e.,
functions mapping the sort to itself), which is strictly beyond many-sorted EPR, and can be useful
in modeling verification problems.
1 Following previous papers, e.g., [Padon et al. 2017], we would henceforth take EPR to refer to the extension of the original

fragment from [Ramsey 1930] to many-sorted logic. The extension allows quantifier alternations and function symbols, as
long as no cycles are introduced, see Sec. 6 for a precise definition. The proofs of decidability and small model property of
EPR carry over to the many-sorted extension.


                                  Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:4                                                                       Neta Elad, Oded Padon, and Sharon Shoham


  There is a rich literature on decidable fragments of first-order logic (see e.g. [Börger et al. 2001;
Voigt 2019] and references therein). The OSC fragment is unique in that landscape as it extends
EPR with cyclic functions, and, unlike monadic logics (e.g., [Löb 1967; Shelah 1977]), allows a linear
order; to the best of our knowledge it is not subsumed by any existing decidable fragment.
  In summary, this paper makes the following contributions:
       • We introduce symbolic structures, a finite representation of infinite structures, in which
         functions and relations are defined using LIA terms and formulas (Sec. 4);
       • We provide an efficient way to find a symbolic model across a given (possibly infinite) search
         space, without an explicit enumeration, by reduction to LIA (Sec. 5);
       • We identify a new decidable fragment of FOL, which extends many-sorted EPR, where the
         satisfiability problem can be solved by restricting the search space to a set of symbolic
         structures of a bounded size, representing (possibly) infinite models. (Sec. 6);
       • We implement a tool called FEST (Find and Evaluate Symbolic structures via Templates) that
         finds symbolic models for FOL formulas using heuristically computed templates, and evaluate
         it on examples from the domains of distributed protocols and of heap-manipulating programs
         (specifically, linked lists), which exhibit infinite counter-models. While existing tools fail to
         produce an answer, FEST finds symbolic models for all 21 examples in our evaluation. (Sec. 7).
  The rest of this paper is organized as follows. Sec. 2 gives an informal overview of the key ideas.
Sec. 3 provides necessary background. Sec. 4 to 7 present the main contributions listed above.
Finally, Sec. 8 discusses related work and Sec. 9 concludes. Technical proofs are deferred to App. A.

2      OVERVIEW
In this section we use a simple example to demonstrate our approach for representing infinite
models and finding them automatically. The example also demonstrates the kind of verification
problems expressible in the decidable OSC fragment.

2.1     Motivation
Quantification is prevalent when modeling systems over unbounded domains in first-order logic.
As soon as quantifier alternations are introduced, infinite models, which are usually not intended,
may arise. An example for the emergence of infinite models is the Paxos [Lamport 1998] distributed
protocol for consensus. In [Padon et al. 2017], Paxos was verified in first-order logic, by carefully
rewriting and adapting the formalization of both the protocol and its inductive invariant to ensure
that the verification conditions are in EPR, avoiding problematic quantifier alternations. However,
this process requires creativity and can be quite tricky. It is therefore desirable to verify Paxos using
its natural first-order modeling, avoiding rewrites. Indeed, recently, [Goel and Sakallah 2021b]
considered the natural FOL modeling of Paxos as a benchmark for automatically inferring inductive
invariants. The invariants inferred match the natural hand-written ones [Lamport 1998], but to
obtain a complete mechanically-checked proof, one needs to mechanically verify their inductiveness.
(Recall that in a typical use-case of invariant inference, no reference inductive invariant is known.)
Unfortunately, the inductiveness of the inferred Paxos invariants hinges on the property that in
every moment in time, the sequence of rounds (also known as ballots) from the beginning of the
protocol is finite, i.e., induction on rounds is required. This property is lost in the FOL modeling of
the protocol. As a result, the invariants are not inductive in FOL, and exhibit an infinite counter-
model, in which an infinite chain of rounds leads to a violation of consistency. This counter-model
reveals the need for induction over the sequence of rounds as part of the inductiveness proof.
   The infinite counter-model is unintended, and perhaps unnatural, but it is an unavoidable artifact
of modeling in FOL. Therefore, a method to describe and find such infinite models is valuable for

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                             33:5


deductive verification in FOL. Presenting these models to the user provides a better experience
than timing out, as current tools do, and allows the user to gain insight into the problem, and refine
their modeling to eliminate these infinite models (e.g., by adding instances of induction axioms).

2.2   Running Example: The Echo Machine
Since Paxos is too complex to be used as a running example, we demonstrate our approach for
representing and finding infinite counter-models on the verification problem of an Echo Machine,
a simple system that captures concepts also found in more complex examples, such as Paxos.
   The Echo Machine is a reactive system that starts by reading some value as input and echoing it,
and later, upon request, recalls a previously echoed value and echoes it once more. It is designed to
satisfy the safety property that any two values echoed by the machine are identical. We use the
problem of verifying that the Echo Machine satisfies this property as our running example.

   Modeling in First-Order Logic. We model the verification problem of the Echo Machine in first
order logic, using an Ivy-like language [McMillan and Padon 2020; Padon et al. 2016], as presented
in Fig. 1. The modeling introduces a value sort and a round sort, a constant start of sort round to
record the start round, and a relation echo : round × value to record echoed values.
   At first, modeling round explicitly as the natural numbers (or integers) using the corresponding
theory might seem attractive. However, current off-the-shelf SMT solvers do not handle combina-
tions of uninterpreted functions with interpreted numerical sorts well in the presence of quantified
formulas. Indeed, in our example, they get stuck and ultimately return “unknown”.
   We therefore abstract the round sort into an uninterpreted sort, and introduce the ≺ relation,
axiomatized to be a strict linear order relation, to represent the < order over the natural numbers.
Additionally, the start constant is axiomatized to be the least element in round, according to ≺.
   The behavior of the Echo Machine is modeled as a first-order transition system, where the state
of the system is maintained by the echo relation, and the transitions are echo_start and echo_prev.
The semantics of each transition is given by a transition relation formula over a “double vocabulary”,
where the pre-state of a transition is denoted by the plain echo relation, and the post-state is denoted
by echo′ . For example, the transition relation for echo_start is:

       ∃v. (∀V. ¬echo(start,V)) ∧ (∀R,V. echo′ (R,V) ↔ ( echo(R,V) ∨ ( R = start ∧ V = v))).                        (1)

That is, the transition is only enabled when no value is echoed at start, as given by the assume
statement on line 13; the transition updates the echo relation by adding a single pair ( start, v), as
given by line 14. The echo_prev transition is enabled if no value has been echoed at round r (line 16),
and value v has been echoed at some round R ≺ r (see line 9, prev_echoed definition); it then echoes
v at round r (line 17). The initial condition, that no value has been echoed, and the safety property,
that all echoed values are the same, are also written in FOL (lines 11 and 18, respectively).
   To establish that the system satisfies the safety property, an inductive invariant that implies it is
specified. An inductive invariant is a property that holds in the initial states of the system and is
preserved by every transition, and hence holds in all the reachable states. The verification problem
is then to check that the conjunction of the provided invariants forms an inductive invariant.

   Checking inductiveness as a satisfiability problem. Verifying that a formula INV is inductive
amounts to checking unsatisfiability of the verification condition (VC) formulas INV ∧ TR𝑖 ∧ ¬INV′ for
every transition, where TR𝑖 is the transition formula and INV′ is obtained from INV by substituting
all mutable symbols by their primed versions. When the invariant is not inductive, a model of the

                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:6                                                                         Neta Elad, Oded Padon, and Sharon Shoham



 1     sort round , value                                     12   transition echo_start ( v : value ):
 2     immutable individual start : round                     13     assume ∀ V . ¬ echo ( start , V )
 3     mutable relation echo : round × value                  14     echo ( start , v ) ← true
 4     immutable relation ≺ : round × round                   15   transition echo_prev ( r : round , v : value ):
 5     axiom strict_linear_order ( ≺ )                        16     assume ( ∀ V . ¬ echo (r , V ))
 6     axiom ∀ R. R ≠ start ⇒ start ≺ R                                 ∧ prev_echoed (r , v )
 7                                                            17     echo (r , v ) ← true
 8     definition prev_echoed ( r : round , v : value ):      18   invariant [ safety ] ∀ V 1 ,V 2 .
 9       ∃ R. R ≺ r ∧ echo (R , v )                                  (( ∃ R . echo (R , V 1 )) ∧ ( ∃ R . echo (R , V 2 )))
10                                                                   ⇒ V1 = V2
11     init ∀ R ,V. ¬ echo (R , V )                           19   invariant ∀ R , V .
                                                                     ( echo (R , V ) ∧ R ≠ start )
                                                                     ⇒ prev_echoed (R , V )

                                      Fig. 1. The Echo Machine in pseudo-Ivy.


VC formula for some transition is a counterexample to induction (CTI)—a pair of states where the
pre-state satisfies the invariant but the post-state obtained after executing the transition does not.2
   It is easy to see that the Echo Machine satisfies its safety property, but the property alone is not
inductive, as it is not preserved by the echo_start transition: starting from a state where one value
has been echoed at round ≠ start, the echo_start transition can echo a different value at round
start, violating the property. (SMT solvers are able to find such a CTI.) To make the safety property
inductive, the invariant in line 19 is added, stating that every value that is echoed at round ≠ start
was previously echoed. This is meant to ensure that all echoed values are equal to the one echoed
at start, which proves the safety property.3
   Despite its simplicity, this example is beyond known decidable fragments of FOL and existing
SMT solvers as well as resolution-based theorem provers are unable to prove (or disprove) it.

2.3      Infinite Counterexample to Induction
In fact, the inability of solvers to handle this problem is not incidental. In contrast to the intuition
above (that holds when rounds correspond to natural numbers), the strengthened invariant is still
not inductive in the FOL semantics, and a CTI for transition echo_start still exists, as we explain
next. However, the CTI consists of infinitely many rounds, which existing solvers have no way of
representing, let alone constructing a CTI with.
   Before we explain the CTI, we note that the pre-state must satisfy the invariant of line 19, that is,
for every round and value in the echo relation there should exist a previous round when the value
was echoed. This ∀∃ quantifier alternation leads to a Skolem function prev : round × value → round,
which we make explicit in the CTI. Intuitively, the Skolem function maps each pair of round r and
value v in the echo relation to the witnessing (lower) round that made v safe to echo at round r.
   The CTI, depicted in Fig. 2a, consists of an infinite decreasing sequence of rounds, all of which
are greater than the initial round start. The prev function is defined arbitrarily for start (and any
value), and as the predecessor w.r.t. ≺ for other rounds (and any value). In the pre-state, all rounds
except for start have echoed the same value 𝑣 1 ; we can see that this state indeed satisfies both of
the invariants. However, by executing echo_start where a value v = 𝑣 0 ≠ 𝑣 1 is chosen for start,
we reach an unsafe state of the system.
2 Some papers consider the pre-state of the transition violating inductiveness of the invariant as a CTI. In this paper, we

follow the convention that the CTI consists of both the pre-state and the post-state.
3 The mechanism of the Echo Machine for ensuring that a value is “safe to echo,” by introducing rounds and using a previous

round as a witness, is reminiscent of the consensus mechanism in Paxos [Lamport 1998], where a value is “safe to propose”
if it was previously voted for by a member of a quorum and none of the quorum members voted for another value since.


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                                      33:7

                  𝑣0                                   𝑣1                              v      𝑣0                              𝑣1
           v
                                echo’                          echo           echo’                            echo’          echo
                                          echo         echo’
          echo’                                                                               𝛼                               𝛽
                                         echo’         echo             prev: 0       start        prev: 𝑥 1 − 1                     ≺: 𝑥1 < 𝑥2
 prev     start    ...                           ...                                                     ≺
                         prev            prev           prev                                                           𝑥 ≤0

(a) An infinite CTI. The interpretation of start and                  (b) A symbolic structure representing the infinite CTI
v are depicted as annotations of the corresponding                    from (a). Double lines denote summary nodes, for
elements. Interpretations depicted in magenta are                     which the subset formulas are written underneath.
relevant for the pre-state, cyan for the post-state, and              Terms and formulas defining functions, respectively
black for both. The interpretation of prev is depicted                relations, are written on the edges, using the syntax
as arrows from rounds to rounds, with the intention                   𝑎 : 𝑏, where 𝑎 is a function or relation and 𝑏 is a term
that for each round, the image of the function is the                 or formula, respectively. The formula on the edge is
same for both values. The interpretation of ≺ orders                  omitted when it is ⊤; and the entire edge is omitted
the rounds from left to right.                                        when the formula is ⊥.

               Fig. 2. A CTI for echo_start. Values are depicted as squares and rounds as circles.


  Fixing the model based on the infinite CTI. The infinite CTI stems from the fact that, in the FOL
semantics, each echoed value being echoed previously does not imply that it was echoed at start.
The CTI reveals that reaching this conclusion requires induction on the rounds. Indeed, when the
user adds the following instance of the induction scheme:
                  ∀V. (∃R. echo(R, V)) ⇒ ∃R. echo(R, V) ∧ ∀R’. R’ ≺ R ⇒ ¬echo(R’, V)
stating that if some value is echoed, then there is also a minimal round in which it is echoed, the
verification condition formulas become unsatisfiable, and existing solvers manage to prove it.
   Our goal. Unfortunately, despite its simplicity, to the best of our knowledge, no existing solver
is able to produce the infinite CTI. As such, the user receives no feedback from the solver, which
either diverges attempting to prove the verification conditions, or gives up and returns “unknown”.
Changing this unfortunate outcome is the goal of our work.

2.4     Symbolic Structures for Compacting the Infinite Pattern
The key to our approach for finding infinite counter-models is observing that though infinite, the
CTI in Fig. 2a can be described compactly: it has one unique start round, in which no value is
echoed in the pre-state and 𝑣 0 is echoed in the post-state; and a repeating pattern of infinitely many
rounds, each echoing 𝑣 1 (in both the pre- and post-state) and pointing to the prev one as a witness
for satisfying the invariant at line 19. Our symbolic structures (Sec. 4) generalize this observation
and formalize a way to express infinite models with similarly structured repetition. A symbolic
structure capturing the infinite model from Fig. 2a is depicted in Fig. 2b.
   Symbolic structure domain. Symbolic structures use “regular nodes” to represent single elements,
such as the start round (𝛼 in Fig. 2b), as well as the individual 𝑣 0 and 𝑣 1 values; and “summary
nodes” to represent (infinitely) repeating patterns in the model. A summary node represents a
(copy of a) subset of the integers, described by some Linear Integer Arithmetic (LIA) formula. In
our example, all rounds besides start are grouped into a summary node 𝛽, which is defined to
represent the integers ≤ 0.
   Each node in the symbolic structure represents a set of explicit elements, which together form
the domain of the infinite model represented by the symbolic structure. An explicit element is

                                        Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:8                                                                        Neta Elad, Oded Padon, and Sharon Shoham


a pair comprised of a node and an integer “index”. For uniformity, we use a pair with index 0
for regular nodes. For example, the explicit elements for the symbolic structure of Fig. 2b are
⟨𝛼, 0⟩, ⟨𝛽, 0⟩, ⟨𝛽, −1⟩, ⟨𝛽, −2⟩, · · · .
  Interpretation. A symbolic structure defines the interpretation of functions over its nodes by
specifying both the target node, and a LIA term to select one of its explicit elements. This term
may also refer to the index of the source nodes. For the prev function in Fig. 2b:
         prev (𝛼, 𝑣 0 ) = prev (𝛼, 𝑣 1 ) = ⟨𝛼, 0⟩                 prev (𝛽, 𝑣 0 ) = prev (𝛽, 𝑣 1 ) = ⟨𝛽, 𝑥 1 − 1⟩
where 𝑥 1 represents the index of the first argument. This means that the prev of the (only) explicit
element formed by the regular node 𝛼 is the same node (for any value), and the prev of each explicit
element ⟨𝛽, 𝑥 1 ⟩, formed by the summary node 𝛽, is the explicit element of 𝛽 whose index is smaller
by 1, i.e., ⟨𝛽, 𝑥 1 − 1⟩.
   Interpretations of relations are similarly defined by specifying for each tuple of nodes, which of
their explicit elements are in the relation. This is done by assigning a LIA formula over the indices
of the nodes. In our example, the echo, echo’, and ≺ relations are defined as follows:
               echo (𝛽, 𝑣 1 ) = ⊤                   echo’ (𝛼, 𝑣 0 ) = ⊤               𝛼 ≺𝛽=⊤
                                                    echo’ (𝛽, 𝑣 1 ) = ⊤               𝛽 ≺ 𝛽 = 𝑥1 < 𝑥2
where 𝑥 1, 𝑥 2 represent the indices of the first and second argument, respectively, and for all other
tuples the relations are defined as ⊥. The definition 𝛼 ≺ 𝛽 = ⊤ means all explicit elements of 𝛼
are ≺-related to all explicit elements of 𝛽. The definition 𝛽 ≺ 𝛽 = 𝑥 1 < 𝑥 2 means that among the
explicit elements associated with 𝛽, elements are only ≺-related to the elements whose integer
indices are strictly larger than theirs, forming an infinite ≺-decreasing sequence.
   Model checking symbolic structures. How do we know that the infinite model represented by
the symbolic structure, also called the explication of the symbolic structure, indeed satisfies the
formula of interest? It turns out that the model checking problem for symbolic structures reduces
to checking LIA formulas (Thm. 4.7). Given the symbolic structure in Fig. 2b, we transform the
original VC formula into a (quantified) LIA formula. Universal quantifiers are transformed into a
combination of conjunction (over nodes) and universal LIA quantifiers (over indices), and similarly
for existential quantifiers (with disjunctions and existential LIA quantifiers). Function and relation
applications are transformed into the LIA terms and formulas that interpret them in the symbolic
structure. Critically, the resulting LIA formula has no uninterpreted functions or relations. As we
show in Sec. 4.2, the resulting LIA formula is true (in LIA) if and only if the explication of the
symbolic structure satisfies the original FOL formula.
   For example, in the VC formula of the Echo Machine, the anti-reflexivity axiom for “≺” is
expressed as ∀𝑥 : round. ¬(𝑥 ≺ 𝑥). To check that the explication of the symbolic structure satisfies
this sub-formula, it is translated into ∀𝑥 : int. (𝑥 = 0 → ¬⊥) ∧ (𝑥 ≤ 0 → ¬(𝑥 < 𝑥)), which is true
in LIA. The first conjunct is generated from the regular node 𝛼, where the explicit elements are
characterized by 𝑥 = 0 and the definition of 𝛼 ≺ 𝛼 is ⊥; the second conjunct is generated from
the summary node 𝛽, where the explicit elements are characterized by 𝑥 ≤ 0 and the definition of
𝛽 ≺ 𝛽 results in 𝑥 < 𝑥. In this way, the translation “bakes” the nodes into the formula and keeps
only the LIA definitions from the symbolic structure to be checked in LIA.

2.5    Finding Symbolic Structures via Symbolic Search
The reducibility of the model-checking problem for symbolic structures to LIA establishes its
decdiability. (Recall that LIA is decidable even with quantifiers.) Our next goal is obtaining an
efficient process, by which to find a symbolic model (i.e., a satisfying symbolic structure) for a

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                             33:9


given formula. Enumeration is an example for a sound procedure that searches for a symbolic
model, but it is inefficient. Instead, we introduce the concept of a symbolic-structure template, as
a way to describe a family of symbolic structures, by limiting the terms and formulas allowed in
summary nodes to some finite subset of the LIA language. Such a template induces a search space
of symbolic structures, and in Sec. 5 we develop an efficient method to symbolically consider all
symbolic structures within that space and search among them for a possibly infinite satisfying
model for a given formula.
   Our search procedure encodes the entire family of symbolic structures induced by a template using
auxiliary Boolean and integer variables. It transforms the original FOL formula into a (quantified)
LIA formula whose structure is similar to the structure of the model checking formula except for
the use of the auxiliary variables. The resulting formula is satisfiable in LIA whenever at least one
of the symbolic structures in the family satisfies the original formula (Thm. 5.4), in which case the
assignment to the auxiliary variables induces the sought symbolic structure.
   The symbolic encoding moves the complexity of finding the right symbolic structure in a given
family into the hands of existing SMT solvers, which are able to solve LIA formulas quickly. However,
this symbolic search requires specifying a template in order to constrain the search space. Rather
than putting the burden of defining such a template on the user, we propose a simple (yet robust, see
Sec. 7) heuristic for computing a candidate template syntactically from the formula. The template
we propose uses simple building blocks for function terms and relation formulas: all functions use
the LIA terms 0 and 𝑥𝑖 ± 𝑘; unary relations use ⊤, ⊥, and 𝑥𝑖 = 0, binary relations additionally allow
comparisons 𝑥𝑖 ⊲⊳ 𝑥 𝑗 ± 𝑘, and ternary relations additionally allow a “between” formula 𝑥𝑖 ≤ 𝑥 𝑗 < 𝑥𝑘
(see Fig. 6 for the precise definition).
   By using such a template and enumerating over the number of nodes, finding a satisfying
symbolic structure for the Echo Machine takes less than one second.

2.6   Decidable Fragment
Rather than a fluke, we show that in the case of the Echo Machine, considering the proposed
templates is not just a heuristic. We prove that for the verification problem of the Echo Machine
(and other problems obeying a syntactic restriction) the set of symbolic structures induced by
such a template is always sufficient, provided that the formula is indeed satisfiable. Note that for
arbitrary satisfiable formulas it is not guaranteed that a symbolic model exists, let alone one from a
simple, predefined, family of templates. This is because not every infinite model can be represented
by a symbolic structure, and some satisfiable formulas are bound to have models that are not the
explication of any symbolic structure.
   That said, in Sec. 6 we identify a new fragment of FOL, the Ordered Self Cycle (OSC) fragment,
where all satisfiable formulas have a (possibly infinite) model that is representable by a symbolic
structure, thus making the satisfiability problem in this fragment decidable. The VC formula of the
Echo machine falls into OSC, both before and after the instance of the induction scheme is added.
   OSC extends the many-sorted variant of the Effectively PRopositional (EPR) decidable fragment
of FOL. While many-sorted EPR forbids all function definitions that form cycles between sorts,
OSC extends it to allow one “infinite” sort (round in our example) that is allowed to have cyclic
functions (such as prev), any number of relations where the infinite sort appears at most once
(such as the echo relation), and one binary relation, axiomatically defined to be a strict linear order,
and conventionally denoted ≺. Linear order is a common primitive in many verification problems,
especially when abstracting the naturals or the integers in FOL, or when verifying properties of
linear data-structures such as linked lists. The ability to add cyclic functions to the vocabulary,
which is strictly beyond EPR, makes the language more expressive and well-suited for a wider
variety of verification problems.

                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:10                                                                      Neta Elad, Oded Padon, and Sharon Shoham


   We prove the decidability of checking satisfiability of a formula in OSC by showing the fragment
enjoys a “small symbolic model property,” bounding the number of nodes in candidate symbolic
models in terms of syntactic parameters of the formula, and restricting the subset of the LIA
language needed in function terms and relation formulas (Thm. 6.1). I.e., the small symbolic model
property provides a cap for enumerating the number of nodes, and induces a definition of candidate
templates, which is strictly covered by our heuristic: for formulas in OSC only the ≺ relation may use
comparisons, and other relations only require ⊤ and ⊥. This makes our symbolic search a decision
procedure for OSC: when enumerating the heuristic templates up to the bound, if no symbolic
model is found, the formula is necessarily unsatisfiable. A notable property of our decidability proof
is that while the symbolic structures are finite (and bounded in size), the models they represent
can be infinite. Thus, OSC does not enjoy a finite model property, as opposed to many decidable
fragments, including EPR: for EPR, the syntactic restrictions imply a bound on the number of
ground terms, from which a finite model can always be constructed. In contrast, in the case of OSC,
the number of ground terms is infinite due to the cyclic functions, and the models, accordingly, are
potentially infinite.

2.7     Applicability of Symbolic Structures
The “small symbolic model property” establishes that the simple templates we consider are complete
for OSC. While the OSC fragment does not cover all of the examples we consider in this paper (e.g.,
complex distributed protocols), it does provide important theoretical justification for designing the
search space of symbolic structures and using our heuristic for computing a template for a formula.
These templates turn out to be valuable for a myriad of complex formulas that lie outside OSC.
   We implemented our symbolic search, combined with the heuristically computed symbolic-
structure templates, in our FEST tool (Find and Evaluate Symbolic structures via Templates) and
successfully applied our approach to examples that admit infinite counter-models, which can be
eliminated by additional FOL axioms (e.g., instances of an induction scheme). The examples are
taken from the domains of distributed protocols (including five variants of Paxos [Lamport 1998] ),
and of properties of linked lists [Löding et al. 2018]. All 21 examples in our evaluation, are solved by
FEST, which quickly finds infinite counter-models. Z3 [de Moura and Bjørner 2008], cvc5 [Barbosa
et al. 2022] and Vampire [Riazanov and Voronkov 1999] all fail to solve these examples.

3     BACKGROUND
    First-Order Logic. We use the usual definition of many-sorted first-order logic (FOL) with equality.
A vocabulary Σ consists of a set of sorts S, and constant, function and relation symbols, each with
a sorted signature. In the cases where Σ has a single sort, we will omit S and the signatures of
the symbols. We denote by X the set of variables used in FOL (we assume that each variable has a
designated sort, and omit sorts when they are clear from the context). Terms 𝑡 over Σ are either
constants 𝑐, variables 𝑥, or well-sorted function applications of the form 𝑓 (𝑡 1, . . . , 𝑡𝑘 ). Formulas
are defined recursively, where atomic formulas are either 𝑡 1 ≈ 𝑡 2 (we use ≈ as the logical equality
symbol) or 𝑅(𝑡 1, . . . , 𝑡𝑘 ), where 𝑅 is a relation symbol, and non-atomic formulas are built using
Boolean connectives ¬, ∧, ∨, → and quantifiers ∀, ∃. Given a formula 𝜑 (term 𝑡), FV(𝜑) (FV(𝑡))
denotes the set of free variables appearing in 𝜑 (𝑡). A term 𝑡 is ground if FV(𝑡) = ∅. A formula 𝜑 is
closed if FV(𝜑) = ∅. Models and assignments are defined in the usual way. A formula 𝜑 is satisfiable
if it has a satisfying model 𝑀, denoted 𝑀 |= 𝜑. We denote by ⊤ a quantifier-free closed tautology,
and by ⊥ a contradiction.
  Linear Integer Arithmetic. The interpreted theory of Linear Integer Arithmetic (LIA) is defined
over a vocabulary that includes the sort of integers, and standard constants, functions and relations

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                           33:11


of linear arithmetic (0, 1, +, −, <). Many SMT solvers support extensions of LIA where all integers
are considered constant symbols, functions include multiplication and division by a constant, and
relations include short-hand comparisons (>, ≤, ≥), and equality modulo a constant. We adopt these
extensions, and denote by TLIA the set of all LIA terms, and by QFLIA the set of all quantifier-free
LIA formulas. We distinguish between the LIA order < and any axiomatized FOL order relation,
for which we typically use ≺. We denote by |=LIA satisfiability in the standard model of integer
arithmetic, and recall that checking satisfiability of (quantified) LIA formulas is decidable [Cooper
1972] and supported by SMT solvers [Barbosa et al. 2022; de Moura and Bjørner 2008].

4     SYMBOLIC STRUCTURES AS REPRESENTATIONS OF INFINITE MODELS
In this section we introduce symbolic structures as a way to represent (certain) infinite structures.
We show how the model-checking problem for models represented by symbolic structures reduces
to the problem of checking satisfiability of a LIA formula, and is therefore decidable.

4.1    Symbolic Structures
Given a many-sorted vocabulary Σ with a set of sorts S, we define a symbolic structure as a triple
𝑆 = (D, B, I), where D is the domain of 𝑆, B is an assignment of bound formulas to the domain,
and I is an interpretation of the symbols in Σ, defined as follows.
   The domain of 𝑆 maps each sort 𝒔 ∈ S to a finite, non-empty, set of nodes D (𝒔), also denoted
D𝒔 , such that the domains of distinct sorts are disjoint, i.e., D𝒔 ∩ D𝒔 ′ = ∅ for any two sorts 𝒔 ≠ 𝒔 ′ .
For each sort 𝒔 ∈ S, the domain D𝒔 is partitioned into “summary nodes”, denoted D𝒔𝑆 , and “regular
nodes”, denoted D𝒔𝑅 , such that D𝒔 = D𝒔𝑆 ⊎ D𝒔𝑅 . Intuitively, each summary node represents a (partial)
copy of the integers, while each regular node represent an individual element.
   The bound assignment maps, for every sort 𝒔, every node 𝑛 ∈ D𝒔 to a satisfiable LIA formula
B (𝑛) ∈ QFLIA with at most one free variable, FV(B (𝑛)) ⊆ {𝑥 }. We further require that for regular
nodes, the bound formula is always 𝑥 ≈ 04 . We think of the bound formula as representing a subset
of the integers — those that satisfy B (𝑛) — and use the formula and the subset of Z it represents
interchangeably. Intuitively, B (𝑛) restricts the copy of the integers represented by 𝑛 to the elements
in B (𝑛) (for regular nodes, this is always a single integer, 0).
   Given 𝑧 ∈ B (𝑛), we refer to ⟨𝑛, 𝑧⟩ as an explicit element of 𝑛, and denote the union set of explicit
elements for a set of nodes 𝑁 by E B (𝑁 ) = {⟨𝑛, 𝑧⟩ | 𝑛 ∈ 𝑁 , 𝑧 ∈ B (𝑛)}.
   The interpretation function maps each symbol to its interpretation. A constant symbol 𝑐 of sort 𝒔
is mapped to an element of some node of sort 𝒔: I (𝑐) ∈ E B (D𝒔 ), also denoted 𝑐 𝑆 .
   The interpretation of a function symbol 𝑓 : 𝒔 1 × · · · × 𝒔𝑘 → 𝒔 is a function that maps nodes
of the argument sorts to an image node of the range sort, accompanied by an image LIA term:
I (𝑓 ) : D𝒔1 ×· · ·×D𝒔𝑘 → D𝒔 ×TLIA , also denoted 𝑓 𝑆 . We further require that if 𝑓 𝑆 (𝑛 1, . . . , 𝑛𝑘 ) = ⟨𝑛, 𝑠⟩,
                                             Ó
then FV(𝑠) ⊆ {𝑥𝑖 | 1 ≤ 𝑖 ≤ 𝑘 }, and that 𝑘𝑖=1 B (𝑛𝑖 ) [𝑥𝑖 /𝑥] |=LIA B (𝑛) [𝑠/𝑥]. Intuitively, we assign
a free variable 𝑥𝑖 to each argument 𝑛𝑖 , representing the specific element of node 𝑛𝑖 to which the
function is applied. The image term 𝑠 selects an element of the image node for each combination of
                                         Ó
argument elements. The requirement 𝑘𝑖=1 B (𝑛𝑖 ) [𝑥𝑖 /𝑥] |=LIA B (𝑛) [𝑠/𝑥] ensures that whenever the
argument elements are elements of the corresponding nodes 𝑛 1, . . . , 𝑛𝑘 , the selected element is an
element of 𝑛. In particular, if the image node 𝑛 is a regular node, the term must evaluate to 0.
   The interpretation of a relation symbol 𝑅 : 𝒔 1 × · · · × 𝒔𝑘 is a function that maps tuples of nodes of
the relevant sorts to a LIA formula:   I (𝑅) : D𝒔1 × · · · × D𝒔𝑘 → QFLIA , also denoted 𝑅𝑆 . We further
require that FV 𝑅 (𝑛 1, . . . , 𝑛𝑘 ) ⊆ {𝑥𝑖 | 1 ≤ 𝑖 ≤ 𝑘 }. Intuitively, the tuples of integers that satisfy
                     𝑆

the LIA formula define the elements of nodes 𝑛𝑖 for which the relation holds.
4We assign a bound formula to regular nodes only for the uniformity of the presentation.



                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:12                                                                                     Neta Elad, Oded Padon, and Sharon Shoham


  Example 4.1. The symbolic structure of Fig. 2b is 𝑆 = (D, B, I), where D ( value) = {𝑣 0, 𝑣 1 },
D ( round) = {𝛼, 𝛽}; 𝑣 0, 𝑣 1, 𝛼 are regular nodes with B (𝑛) = 𝑥 ≈ 0; 𝛽 is a summary node with
B (𝛽) = 𝑥 ≤ 0; and
                                                   n ⟨𝛼, 0⟩         𝑛1 = 𝛼                                        n⊤     𝑛 1 = 𝛽, 𝑛 2 = 𝑣1
      start𝑆 = ⟨𝛼, 0⟩        prev𝑆 (𝑛 1, 𝑛 2 ) =                                            echo𝑆 (𝑛 1, 𝑛 2 ) =
                                               ⟨𝛽, 𝑥 1 − 1⟩         𝑛1 = 𝛽                                     ⊥         otherwise
                                              (⊤                    𝑛 1 = 𝛼, 𝑛 2 = 𝛽                          (⊤         𝑛 1 = 𝛼, 𝑛 2 = 𝑣0
          v𝑆 = ⟨𝑣0, 0⟩            𝑛 1 ≺𝑆 𝑛 2 = 𝑥 1 < 𝑥 2            𝑛1 = 𝑛2 = 𝛽           echo’𝑆 (𝑛 1, 𝑛 2 ) = ⊤         𝑛 1 = 𝛽, 𝑛 2 = 𝑣1
                                               ⊥                    otherwise                                  ⊥         otherwise

   An example of a symbolic structure with two summary nodes appears in Fig. 11 in App. C.
    Explication. A symbolic structure 𝑆 = (D, B, I) represents a (possibly) infinite first-order struc-
ture, defined by its explication 𝑀 = E (𝑆).
    The domain of sort 𝒔 ∈ S in 𝑀, denoted D𝒔𝑀 , is the set of explicit elements E B (D𝒔 ), i.e., it
consists of all pairs ⟨𝑛, 𝑧⟩ of nodes 𝑛 in D𝒔 and integers 𝑧 that satisfy B (𝑛). Thus, each summary
node may contribute infinitely many elements to the explicit domain, while each regular node
contributes a single element. Note that the requirements for bound formulas to be satisfiable ensures
that the explicit domains of all sorts are non-empty.
    The interpretation of the symbols in 𝑀, denoted 𝛼 𝑀 for symbol 𝛼, is defined as follows. For
a constant symbol 𝑐, 𝑐 𝑀 = 𝑐 𝑆 . For a function symbol 𝑓 of arity 𝑘, 𝑓 𝑀 (⟨𝑛 1, 𝑧 1 ⟩, . . . , ⟨𝑛𝑘 , 𝑧𝑘 ⟩) =
  𝑛, 𝑣¯LIA (𝑠) , where ⟨𝑛, 𝑠⟩ = 𝑓 𝑆 (𝑛 1, . . . , 𝑛𝑘 ), 𝑣 LIA is an assignment such that 𝑣 LIA (𝑥𝑖 ) = 𝑧𝑖 , and
𝑣¯LIA extends 𝑣 LIA to all LIA terms in the standard way. That is, the function maps the elements
 ⟨𝑛 1, 𝑧 1 ⟩, . . . , ⟨𝑛𝑘 , 𝑧𝑘 ⟩ of the explicit domain to an element contributed by node 𝑛 that is deter-
mined by evaluating               the term 𝑠 on the specific elements 𝑧𝑖 of nodes 𝑛𝑖 . For a relation sym-
bol 𝑅, 𝑅 𝑀 = (⟨𝑛 1, 𝑧 1 ⟩, . . . , ⟨𝑛𝑘 , 𝑧𝑘 ⟩) | 𝑣 LIA |=LIA 𝑅𝑆 (𝑛 1, . . . , 𝑛𝑘 ) where 𝑣 LIA (𝑥𝑖 ) = 𝑧𝑖 ∈ B (𝑛𝑖 ) . That
is, the tuples of explicit elements in the relation are determined by evaluating the LIA formula
𝑅𝑆 (𝑛 1, . . . , 𝑛𝑘 ) on the specific elements 𝑧𝑖 of nodes 𝑛𝑖 .
  Example 4.2. Let us explicate the symbolic structure from Ex. 4.1. The explicit domains are
D 𝑀 ( value) = {⟨𝑣 0, 0⟩, ⟨𝑣 1, 0⟩} and D 𝑀 ( round) = {⟨𝛼, 0⟩} ∪ {⟨𝛽, 𝑧⟩ | 𝑧 ≤ 0}. The explication of the
constants is: start𝑀 = ⟨𝛼, 0⟩ and v𝑀 = ⟨𝑣 0, 0⟩. As for the function prev and the relations:
                                                             ≺ 𝑀 = { ( ⟨𝛼, 0⟩, ⟨𝛽, 𝑧 ⟩ ) | 𝑧 ≤ 0} ∪ { ( ⟨𝛽, 𝑧 1 ⟩, ⟨𝛽, 𝑧 2 ⟩ ) | 𝑧 1 < 𝑧 2 ≤ 0}
                             ⟨𝛼, 0⟩        𝑛=𝛼
 prev𝑀 (⟨𝑛, 𝑧 ⟩, 𝑣) =                                   echo𝑀 = { ( ⟨𝛽, 𝑧 ⟩, ⟨𝑣1, 0⟩ ) | 𝑧 ≤ 0}
                             ⟨𝛽, 𝑧 − 1⟩    𝑛=𝛽
                                                       echo’𝑀 = { ( ⟨𝛽, 𝑧 ⟩, ⟨𝑣1, 0⟩ ) | 𝑧 ≤ 0} ∪ { ( ⟨𝛼, 0⟩, ⟨𝑣0, 0⟩ ) }
   The resulting explicit model is isomorphic to the infinite model depicted in Fig. 2a.
   Remark 4.3. In fact, for the Echo Machine, the degenerate bound formula B (𝛽) = ⊤ would produce
a symbolic structure whose explication is a counter-model to the VC formula just as well (even though it
is not isomorphic to Fig. 2a). One may wonder therefore if bound formulas are necessary, or do regular
nodes (where B (𝑛) = 𝑥 ≈ 0) and unbounded summary nodes (where B (𝑛) = ⊤) suffice. An example
that requires a summary node with a bound formula other than ⊤ (e.g., 𝑥 ≥ 0) can be found in App. B.

4.2     Model Checking a Symbolic Structure
A symbolic structure 𝑆 represents an explicit model 𝑀 = E (𝑆). In this section we address the
problem of checking if E (𝑆) satisfies a given FOL formula 𝜑, in which case, we also say that 𝑆
satisfies 𝜑 (with abuse of notation). This is done by a transformation that “bakes” the symbolic
structure into the formula, resulting in a LIA formula that is true if and only if E (𝑆) |= 𝜑.
   We define the transformation recursively (over the inductive structure of formulas). As a result,
we must consider both closed formulas and formulas with free variables. To that end, we first define
assignments in symbolic structures.

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                 33:13


    Symbolic assignments. If 𝜑 has free variables, then its value in 𝑀 depends also on an assignment
𝑣 : X → D 𝑀 (which respects the sorts). We refer to such an assignment as an explicit assignment.
Recall that D 𝑀 ⊆ D 𝑆 × Z, i.e., explicit assignments map each variable to a node paired with an
integer. For the purpose of defining the transformation to LIA, we introduce symbolic assignments
where explicit integers are replaced by integer variables. In the sequel, let X LIA = {𝑥 LIA | 𝑥 ∈ X} be
a set of integer variables such that each variable 𝑥 ∈ X has a unique symbolically corresponding
LIA variable 𝑥 LIA ∈ X LIA .
  Definition 4.4. Given a symbolic structure 𝑆, a symbolic assignment is a mapping 𝑣 𝑆 : X →
D 𝑆 × X LIA such that for every variable 𝑥 ∈ X, 𝑣 𝑆 (𝑥) = ⟨𝑛, 𝑥 LIA ⟩ for some 𝑛 ∈ D 𝑆 .
   That is, a symbolic assignment fixes the node 𝑛 to which each variable 𝑥 is mapped, but leaves
the element of 𝑛 symbolic, captured by the integer variable 𝑥 LIA that uniquely corresponds to 𝑥.
   We denote by 𝑣¯𝑆 the extension of 𝑣 𝑆 to arbitrary terms over Σ. The extended assignment 𝑣¯𝑆
maps terms to nodes paired with LIA terms over X LIA . Formally, 𝑣¯𝑆 : T → D 𝑆 × TLIA is defined by
setting 𝑣¯𝑆 (𝑥) = 𝑣 𝑆 (𝑥); 𝑣¯𝑆 (𝑐) = 𝑐 𝑆 ; and 𝑣¯𝑆 (𝑓 (𝑡 1, . . . , 𝑡𝑘 )) = ⟨𝑛, 𝑠 [𝑠𝑖 /𝑥𝑖 ]⟩, where 𝑣¯𝑆 (𝑡𝑖 ) = ⟨𝑛𝑖 , 𝑠𝑖 ⟩ and
𝑓 𝑆 (𝑛 1, . . . , 𝑛𝑘 ) = ⟨𝑛, 𝑠⟩. That is, if 𝑣¯𝑆 interprets the terms 𝑡𝑖 as ⟨𝑛𝑖 , 𝑠𝑖 ⟩, and the symbolic structure
defines 𝑓 𝑆 (𝑛 1, . . . , 𝑛𝑘 ) = ⟨𝑛, 𝑠⟩, then 𝑣¯𝑆 interprets 𝑓 (𝑡 1, . . . , 𝑡𝑘 ) as the node 𝑛 and the term obtained
from 𝑠 by substituting 𝑠𝑖 for 𝑥𝑖 .
  Example 4.5. For the symbolic structure defined in Ex. 4.1, we can define an assignment          𝑣 𝑆 such
that 𝑣 𝑆 (𝑥 1 ) = 𝛽, 𝑥 1LIA . Given the term 𝑡 = prev ( prev (𝑥 1 )), 𝑣¯𝑆 (𝑆) = 𝛽, 𝑥 1LIA − 1 − 1 .
  The correspondence between FOL variables and their LIA counterparts allows us to “decompose”
an explicit assignment 𝑣 into a symbolic assignment where all integers are replaced by variables,
accompanied by a LIA assignment to X LIA , which captures the explicit integers from 𝑣.
  Definition 4.6. Given an explicit assignment 𝑣 : X → D 𝑀 , its symbolization is the symbolic
assignment 𝑣 𝑆 : X → D 𝑆 × X LIA defined by 𝑣 𝑆 (𝑥) = ⟨𝑛, 𝑥 LIA ⟩ whenever 𝑣 (𝑥) = ⟨𝑛, 𝑧⟩.
  The residual assignment of 𝑣 is the LIA assignment 𝑣 LIA : X LIA → Z defined by 𝑣 LIA (𝑥 LIA ) = 𝑧
whenever 𝑣 (𝑥) = ⟨𝑛, 𝑧⟩.
   We are now ready to define the recursive transformation that reduces model checking of symbolic
structures in FOL formulas to checking satisfiability of LIA formulas by “baking” a symbolic structure
and an explicit assignment into the FOL formula.
   Model checking symbolic structures by transforming FOL formulas to LIA. Given a FOL formula 𝜑,
a symbolic structure 𝑆 and an explicit assignment 𝑣, we use 𝑣 𝑆 , the symbolization of 𝑣, to translate
𝜑 into a LIA formula. When evaluated with the residual assignment, 𝑣 LIA , this formula captures
whether E (𝑆) and 𝑣 satisfy 𝜑. The transformation, trans𝑆𝑣𝑆 (𝜑), is defined in Fig. 3.
   The transformation uses the LIA terms and formulas that interpret function and relation symbols
in the symbolic structure as building blocks to transform the formula. Specifically, if 𝑣 𝑆 interprets
the terms 𝑡𝑖 as ⟨𝑛𝑖 , 𝑠𝑖 ⟩, then the atomic formula 𝑅(𝑡 1, . . . , 𝑡𝑘 ) is transformed to the LIA formula
𝑅𝑆 (𝑛 1, . . . , 𝑛𝑘 ), which the symbolic structure defines as the interpretation of 𝑅 on nodes 𝑛 1, . . . , 𝑛𝑘 ,
except that the variables 𝑥 1, . . . , 𝑥𝑘 that may appear in 𝑅𝑆 (𝑛 1, . . . , 𝑛𝑘 ) are substituted by the LIA
terms 𝑠 1, . . . , 𝑠𝑘 .
   Similarly, the atomic formula 𝑡 1 ≈ 𝑡 2 is transformed to the LIA formula 𝑠 1 ≈ 𝑠 2 if the nodes 𝑛 1
and 𝑛 2 are the same, requiring that 𝑡 1, 𝑡 2 are mapped not only to the same node but also to the same
element of the node, and transformed to ⊥ otherwise.
   The transformation of the Boolean connectives is straightforward.
   A universal quantifier ∀𝑥 is transformed into a universal quantifier over an integer variable 𝑥 LIA ,
such that for every node 𝑛 in the symbolic structure (captured by a conjunction over all nodes of the

                                  Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:14                                                                                          Neta Elad, Oded Padon, and Sharon Shoham

                  trans𝑆𝑣𝑆 (𝑅 (𝑡 1 , . . . , 𝑡𝑘 ) ) = 𝑅𝑆 (𝑛 1 , . . . , 𝑛𝑘 ) [𝑠𝑖 /𝑥𝑖 ] where 𝑣¯𝑆 (𝑡𝑖 ) = ⟨𝑛𝑖 , 𝑠𝑖 ⟩
                          trans𝑆𝑣𝑆 (𝑡 1 ≈ 𝑡 2 ) = 𝑠 1 ≈ 𝑠 2 if 𝑛 1 = 𝑛 2 and ⊥ otherwise, where 𝑣¯𝑆 (𝑡𝑖 ) = ⟨𝑛𝑖 , 𝑠𝑖 ⟩
                                                                   
                              trans𝑆𝑣𝑆 (¬𝜑 ) = ¬ trans𝑆𝑣𝑆 (𝜑 )

                           trans𝑆𝑣𝑆 (𝜑 ◦ 𝜓 ) = trans𝑆𝑣𝑆 (𝜑 ) ◦ trans𝑆𝑣𝑆 (𝜓 )      for ◦ ∈ {∧, ∨, →}
                                                         Û                                                                           
                        trans𝑆𝑣𝑆 (∀𝑥 : 𝒔.𝜑 ) = ∀𝑥 LIA .         B (𝑛) [𝑥 LIA /𝑥 ] → trans𝑆      LIA
                                                                                                                            (𝜑 )
                                                                                                       𝑣𝑆    𝑛,𝑥      /𝑥
                                                              𝑛∈D𝒔
                                                               Ü                                                                 
                        trans𝑆𝑣𝑆 (∃𝑥 : 𝒔.𝜑 ) = ∃𝑥 LIA .                B (𝑛) [𝑥 LIA /𝑥 ] ∧ trans𝑆                        (𝜑 )
                                                                                                     𝑣𝑆     𝑛,𝑥 LIA /𝑥
                                                              𝑛∈D𝒔


            Fig. 3. Model-checking symbolic structure 𝑆 and assignment 𝑣 by translation to LIA.



corresponding sort), all the elements of 𝑛, captured by assignments to 𝑥 LIA that satisfy the bound
formula of 𝑛, satisfy the body of the quantified formula. Similarly for an existential quantifier.
   Note that the quantifier structure of trans𝑆𝑣𝑆 (𝜑) is the same as that of 𝜑, except that quantification
is over integer variables. Further, if FV(𝜑) ⊆ {𝑥 1, . . . , 𝑥𝑘 } then FV(trans𝑆𝑣𝑆 (𝜑)) ⊆ {𝑥 1LIA, . . . , 𝑥𝑘LIA }.
Moreover, as expected, if two symbolic assignments agree on all the free variables of 𝜑, then they
result in the same LIA formula. In particular, for a closed formula, the transformation does not
depend on the symbolic assignment used. The following theorem, proven by structural induction
on 𝜑, summarizes the correctness of the transformation for model checking a symbolic structure.

  Theorem 4.7. Let 𝑆 be a symbolic structure, 𝑣 an explicit assignment, 𝑣 𝑆 its symbolization and 𝑣 LIA
the residual assignment. Then for every formula 𝜑 over Σ the following holds:

                                          E (𝑆), 𝑣 |= 𝜑 ⇐⇒ 𝑣 LIA |=LIA trans𝑆𝑣𝑆 (𝜑).

  Example 4.8. Continuing with our running example, let us          consider checking whether the
symbolic structure from Ex. 4.1 satisfies the formula 𝜑 = ∀𝑥 2 .¬ prev ( prev (𝑥 1 )) ≺ 𝑥 2 under some
explicit assignment 𝑣 where 𝑣 (𝑥 1 ) = ⟨𝛽, −7⟩. The transformation of 𝜑 w.r.t. 𝑣 𝑆 is
                                                                                       
          trans𝑆𝑣𝑆 (𝜑) = ∀𝑥 2LIA . 𝑥 2LIA ≈ 0 → ¬⊥ ∧ 𝑥 2LIA ≤ 0 → ¬ 𝑥 1LIA − 1 − 1 < 𝑥 2LIA .
                                                                              


(The blue color highlights the transformation of the atomic formula and the underline depicts the
transformation of the corresponding term.) Recall that in this example 𝑣 LIA (𝑥 1LIA ) = −7. Therefore,
𝑣 LIA ̸ |= trans𝑆𝑣𝑆 (𝜑), which is expected since E (𝑆), 𝑣 ̸ |= 𝜑 (see Ex. 4.2).

4.3     Beyond Single-Dimension Symbolic Structures
We illustrate one limitation of symbolic structures, and sketch a possible way to overcome it. The
summary nodes we have seen thus far represent a single dimension of infinity (a single copy
of Z), and symbolic structures can compactly describe infinite structures with relatively simple
repeating patterns using those summary nodes. However, they cannot represent structures with
more complex, e.g., “nested”, repeating patterns. One such example would be a structure where
domain elements are linearly ordered in a fashion akin to 𝜔 × 𝜔.
   Specifically, consider a vocabulary Σ = {𝑓 (·), 𝑃 (·), 𝑅(·, ·)}, where 𝑓 is a unary function, 𝑃 is
a unary relation, and 𝑅 is a binary relation. The formula 𝜑 + , defined by the conjunction of the
formulas in Tab. 1, requires its models to include an infinite repetition of infinitely many 𝑃’s,
followed by infinitely many ¬𝑃’s.

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                           33:15


                                Table 1. Conjuncts of 𝜑 + , which has a model akin to 𝜔 × 𝜔.

                           Conjunct                                                       Meaning
                           ∀𝑥, 𝑦, 𝑧.(𝑅 (𝑥, 𝑦) ∧ 𝑅 (𝑦, 𝑧 ) ) → 𝑅 (𝑥, 𝑧 )                  𝑅 is transitive
                           ∀𝑥 .¬𝑅 (𝑥, 𝑥 )                                                𝑅 is anti-reflexive
                           ∀𝑥, 𝑦.𝑅 (𝑥, 𝑦) ∨ 𝑅 (𝑦, 𝑥 ) ∨ 𝑥 ≈ 𝑦                            𝑅 is linear
                           ∀𝑥 .𝑅 (𝑥, 𝑓 (𝑥 ) )                                            𝑓 is “increasing”
                           ∀𝑥, 𝑦.𝑅 (𝑥, 𝑦) → (𝑅 (𝑓 (𝑥 ), 𝑦) ∨ 𝑓 (𝑥 ) ≈ 𝑦)                 𝑓 is a “successor”
                           ∀𝑥 .𝑃 (𝑥 )↔𝑃 (𝑓 (𝑥 ) )                                        𝑓 preserves 𝑃
                           ∀𝑥 .∃𝑦, 𝑧.𝑅 (𝑥, 𝑦) ∧ 𝑅 (𝑥, 𝑧 ) ∧ 𝑃 (𝑦) ∧ ¬𝑃 (𝑧 )              𝑃 alternates infinitely



        ⟨0, 0⟩
                 𝑓
                       ⟨0, 1⟩
                                      𝑓
                                             ⟨0, 2⟩
                                                      𝑓
                                                             ...      Fig. 4. Model 𝑀 for 𝜑 + , which is linearly ordered in a
  𝑃:
                                                                      fashion akin to 𝜔 × 𝜔. The relation 𝑅 is reflected by the
                 𝑓                    𝑓               𝑓
                                                             ...      ordering of the nodes, which are ordered top to bottom,
 ¬𝑃:    ⟨1, 0⟩         ⟨1, 1⟩                ⟨1, 2⟩
                                                                      left to right. 𝑃 alternates between the rows, i.e., either 𝑃
                 𝑓                    𝑓               𝑓               holds for an entire row or ¬𝑃 holds for an entire row (as
  𝑃:    ⟨2, 0⟩         ⟨2, 1⟩                ⟨2, 2⟩          ...
                                      ..                              noted to the left). The successor function 𝑓 always stays
                                       .                              within the same row, mapping each node to its immediate
                                                                      neighbor to the right.

  The conjunction 𝜑 + is satisfiable by the infinite model 𝑀 = D 𝑀 , I 𝑀 , depicted in Fig. 4, where
                                                                        

D 𝑀 = N × N and I 𝑀 is defined as
                                  𝑓 𝑀 ( ⟨𝑎, 𝑏 ⟩ ) = ⟨𝑎, 𝑏 + 1⟩             𝑃 𝑀 = { ⟨𝑎, 𝑏 ⟩ | 𝑎 ≡ 0 mod 2}
                                  𝑅 𝑀 = { ( ⟨𝑎 1 , 𝑏 1 ⟩, ⟨𝑎 2 , 𝑏 2 ⟩ ) | 𝑎 1 < 𝑎 2 ∨ (𝑎 1 = 𝑎 2 ∧ 𝑏 1 < 𝑏 2 ) }.

I.e., the domain consists of pairs of integers, 𝑓 𝑀 increments the second integer in each pair (along
the horizontal dimension in Fig. 4), 𝑃 𝑀 holds whenever the first integer in a pair is even (alternating
along the vertical dimension in Fig. 4), and 𝑅 𝑀 is the lexicographical order over pairs of integers.
   In order to represent this structure using a symbolic structure, infinitely many summary nodes
would be needed. However, symbolic structures can be naturally generalized to allow representation
of such structures by (1) letting each summary node represent a subset of Z × Z instead of Z, and,
accordingly, (2) attaching to each summary node 𝑛 two LIA variables, 𝑥 1 and 𝑥 2 , to be used in bound
formulas, and in the LIA terms and formulas that interpret   the function and relation symbols. The
intention is that an assignment 𝑥 1 ↦→ 𝑧 1, 𝑥 2 ↦→ 𝑧 2 represents the explicit element ⟨𝑛, 𝑧 1, 𝑧 2 ⟩ of 𝑛.
                                                      

   With this generalization, the structure 𝑀 from above, which satisfies 𝜑 + , can be represented by a
symbolic structure with a single summary node, 𝑇 = (D = {𝑛}, B, I), where B and I are defined
as
                      B (𝑛)       =        𝑥1 ≥ 0 ∧ 𝑥2 ≥ 0        𝑓 𝑇 (𝑛)       =      𝑛, 𝑥 11 , 𝑥 12 + 1
                                           𝑥 11 ≡ 0 mod 2                             𝑥 11 < 𝑥 21 ∨ 𝑥 11 = 𝑥 21 ∧ 𝑥 12 < 𝑥 22 .
                                                                                                                             
                     𝑃 𝑇 (𝑛)      =                             𝑅𝑇 (𝑛, 𝑛)       =
where 𝑥𝑖𝑗 is the variable representing the 𝑗’th copy of Z associated with the node used as the 𝑖’th
argument of a function / relation. That is, the lower indices refer to different arguments, as before,
while the upper indices refer to one of the copies of Z within a summary node.𝑇 represents an infinite
model, which is isomorphic to the model 𝑀 above. (The domain D 𝑀 = N×N maps straightforwardly
to the explicit domain of 𝑇 , {⟨𝑛, 𝑧 1, 𝑧 2 ⟩ ∈ {𝑛} × Z × Z | 𝑧 1 ≥ 0 ∧ 𝑧 2 ≥ 0} = {𝑛} × N × N.)
   We can further generalize and let the multiplicity of the copies of Z represented by each node be
a parameter of either the symbolic structure (as a whole) or each summary node (regular nodes can
be thought of as 0-dimension summary nodes). Both the explication and the translation at the heart
of the model checking procedure for symbolic structures can be generalized to multi-dimensional
symbolic structures such that the model-checking theorem (Thm. 4.7) still holds. However, note
that with any generalization, the fact that symbolic structures are encoded in a finite way and that
their model-checking is decidable means that some formulas will not have a symbolic structure: any

                                           Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:16                                                                      Neta Elad, Oded Padon, and Sharon Shoham


recursively enumerable set of models, for which model-checking is decidable, cannot be complete
since FOL satisfiability is not in RE.
   For the remainder of the paper, we exclusively use single-dimension symbolic structures, since
they effectively handle the examples we consider.

5   CHECKING SATISFIABILITY BY FINDING SYMBOLIC STRUCTURES
We now present an algorithm for finding a satisfying symbolic structure for a given FOL formula
within a given search space. Broadly, given a FOL formula, we leverage an SMT solver to symbolically
search for a symbolic model in a (possibly infinite) family of symbolic structures given by a template
(defined below). The idea is that given some FOL formula 𝜑 and a template, we construct a LIA
formula where a satisfying assignment induces a symbolic model for 𝜑. This process is sound for
any formula, i.e., whenever a symbolic model is found, its explication satisfies the formula. In Sec. 6
we present a class of formulas, for which this process is also complete: i.e., for any formula in that
class, there is a computable template, such that if the formula is satisfiable, a symbolic model is
guaranteed to be found when searching using this template.
   Symbolic-structure templates. To define the search space of symbolic structures, i.e., a symbolic
structure family, we use the notion of a symbolic-structure template. A symbolic-structure template,
similarly to a symbolic structure, fixes a finite set of nodes for each sort’s domain, but uses finite
sets of LIA terms and formulas with additional free variables as candidates for the bound formulas
and the interpretation of functions and relations. Formally:
  Definition 5.1. A symbolic-structure template for a vocabulary Σ is a triple 𝑆 ♯ = (D, B ♯ , I ♯ )
where D is a symbolic structure domain, B ♯ is a finite set of bound formulas for summary nodes,
and I ♯ defines the space of interpretations for function and relation symbols: for every function
symbol 𝑓 ∈ Σ, I ♯ (𝑓 ) ⊆ TLIA and for every relation symbol 𝑅 ∈ Σ, I ♯ (𝑅) ⊆ QFLIA , such that I ♯ (𝑓 )
and I ♯ (𝑅) are finite.
   We distinguish two kinds of free variables in bound formulas, function terms and relation
formulas in 𝑆 ♯ . Symbolic-structure free variables are the same as the free variables in symbolic
structures, used to identify explicit elements in nodes. Namely, they consist of 𝑥 in bound formulas
and of 𝑥 1, 𝑥 2, . . . in function terms and relation formulas, according to their arity (see Sec. 4). All
other free variables are considered template free variables, conventionally denoted 𝑑, 𝑑 1, 𝑑 2, . . . .
These variables are not part of a symbolic structure definition; they are used to capture infinitely
many similar LIA terms and formulas, and are replaced by an interpreted LIA constant (integer)
when the template is instantiated.
   A symbolic-structure template 𝑆 ♯ = (D, B ♯ , I ♯ ) represents the set of all symbolic structures
𝑆 over the domain D, where bound formulas are taken from B ♯ for summary nodes and are
𝑥 ≈ 0 for regular nodes, constants are interpreted as regular nodes, the terms and formulas in the
interpretations of function and relation symbols are taken from I ♯ , with all template free variables
substituted by integers. Note that these integers may be different in each use of a term or formula.
For example, two nodes may use the same bound formula 𝑥 ≥ 𝑑 ∈ B ♯ with different substitutions,
resulting in bounds 𝑥 ≥ 0, 𝑥 ≥ 1. The formal definition follows, where 𝑆𝐹𝑉 (𝑎) denotes the set of
template free variables appearing in a term or formula 𝑎.
  Definition    5.2. A symbolic
                                   structure 𝑆 = (D, B, I) is represented by a symbolic structure skele-
ton 𝑆 = D, B , I if (i) for every regular node 𝑛 ∈ D, B (𝑛) = 𝑥 ≈ 0, and for every sum-
       ♯             ♯  ♯

mary node 𝑛 ∈ D, B (𝑛) = 𝜓 𝑧 1 /𝑑 1, . . . , 𝑧𝑚 /𝑑𝑚 , where 𝜓 ∈ B ♯ , 𝑧 1, . . . , 𝑧𝑚 ∈ Z, and 𝑆𝐹𝑉 (𝜑) =
                                                           

 𝑑 , . . . , 𝑑𝑚 ; similarly, (ii) for every 𝑛 1, . . . , 𝑛𝑘 ∈ D and 𝑓 ∈ Σ (resp. 𝑅 ∈ Σ), 𝑓 𝑇 (𝑛 1, . . . , 𝑛𝑘 ) =
 1


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                           33:17


 𝑛, 𝑠 𝑧 1 /𝑑 1, . . . , 𝑧𝑚 /𝑑𝑚 (resp. 𝑅𝑇 (𝑛 1, . . . , 𝑛𝑘 ) = 𝜓 𝑧 1 /𝑑 1, . . . , 𝑧𝑚 /𝑑𝑚 ) for some node 𝑛 ∈ D, in-
                                                                                      

tegers 𝑧 1, . . . , 𝑧𝑚 and 𝑠 ∈ I ♯ (𝑓 ) (resp. 𝜓 ∈ I ♯ (𝑅)) s.t. 𝑆𝐹𝑉 (𝑡) = 𝑑 1, . . . , 𝑑𝑚 (resp. 𝑆𝐹𝑉 (𝜓 ) =
                                                                                       
 1
 𝑑 , . . . , 𝑑𝑚 ).
  In the sequel, we refer to the template and the set of symbolic structures it represents inter-
changeably, and write 𝑆 ∈ 𝑆 ♯ when 𝑆 is represented by 𝑆 ♯ .
   Example 5.3. To capture a family of symbolic structures where all summary nodes represent a
full copy of Z, we can define a template 𝑆 1♯ where B1♯ = {⊤}. The bound formula ⊤ has neither
template free variables nor symbolic-structure free variables. A richer family of symbolic structures,
where summary nodes may also represent the sets of positive or negative integers, can be captured
by a template 𝑆 2♯ where B2♯ = {⊤, 𝑥 ≥ 1, 𝑥 ≤ −1}. The bound formulas 𝑥 ≥ 1, 𝑥 ≤ −1 contain the
symbolic-structure free variable 𝑥 and no template free variables. Finally, to capture a family of
symbolic structures where summary nodes may represent any half-space of the integers, we can
use instead the bound formulas 𝑥 ≥ 𝑑, 𝑥 ≤ 𝑑 , where 𝑑 is a template free variable (and 𝑥 is still a
symbolic-structure free variable). Specific symbolic structures within this template would replace
𝑑 with specific LIA (integer) constants; for example, 𝑥 ≥ 3 or 𝑥 ≤ −2.
   Symbolic structure finding through LIA encoding. To check if a symbolic-structure template 𝑆 ♯
includes a symbolic model for a FOL formula, we use an encoding similar to the one used in Sec. 4.2
for model checking an individual symbolic structure. The key difference is that the bound formulas
and the interpretation are not (fully) specified in 𝑆 ♯ , and, instead, need to be found. To account for
this, the encoding introduces Boolean auxiliary variables that keep track of which interpretation
and bound formulas are used, and LIA auxiliary variables that keep track of the LIA constants
assigned to template free variables, such that each symbolic structure in 𝑆 ♯ is induced by some
assignment to the auxiliary variables.
    Auxiliary variables. We use the following Boolean auxiliary variables: a variable 𝑏𝑛 : 𝜓 for any
summary node 𝑛 and any bound formula 𝜓 ∈ B ♯ , represents the decision to use 𝜓 as the bound
formula for 𝑛; a variable 𝑏𝑐→𝑛 for any constant 𝑐 ∈ Σ and any regular node 𝑛, represents the decision
to define 𝑐𝑇 as ⟨𝑛, 0⟩; a variable 𝑏 𝑓 (𝑛1,...,𝑛𝑘 )→⟨𝑛,𝑠 ⟩ for any function 𝑓 ∈ Σ, any term 𝑠 ∈ I ♯ (𝑓 ),
and any nodes 𝑛 1, . . . , 𝑛𝑘 , 𝑛, represents the decision to define 𝑓 𝑇 (𝑛 1, . . . , 𝑛𝑘 ) as ⟨𝑛, 𝑠⟩, modulo the
substitutions of the template free variables in 𝑠; and a variable 𝑏 𝑅 (𝑛1,...,𝑛𝑘 ) : 𝜓 for any relation 𝑅 ∈ Σ,
any formula 𝜓 ∈ I ♯ (𝑅), and any nodes 𝑛 1, . . . , 𝑛𝑘 , represents the decision to define 𝑅𝑇 (𝑛 1, . . . , 𝑛𝑘 )
as 𝜓 , modulo the substitutions of the template free variables appearing in 𝜓 .
    To encode the possible substitutions of template free variables, allowing different substitutions
in different contexts, the following LIA auxiliary variables are used: a variable 𝑑𝑛 for any summary
node 𝑛 ∈ D, and any template free variable 𝑑 appearing in any bound formula 𝜓 ∈ B ♯ ; a variable
𝑑 𝑓 (𝑛1,...,𝑛𝑘 ) for any function 𝑓 ∈ Σ, nodes 𝑛 1, . . . , 𝑛𝑘 ∈ D, and any template free variable 𝑑 appearing
in any term 𝑠 ∈ I ♯ (𝑓 ); and a variable 𝑑𝑅 (𝑛1,...,𝑛𝑘 ) for any relation 𝑅 ∈ Σ, nodes 𝑛 1, . . . , 𝑛𝑘 ∈ D, and
any template free variable 𝑑 appearing in any formula 𝜓 ∈ I ♯ (𝑅).
   Encoding. Given a FOL formula 𝜑 and a symbolic-structure template 𝑆 ♯ , the “symbolic structure
finding” LIA formula is 𝜑𝑆 ♯ ∧ 𝜑 aux , where 𝜑𝑆 ♯ encodes satisfaction of 𝜑, and 𝜑 aux ensures that the
assignment to the Boolean auxiliary variables induces a well-defined symbolic structure. We obtain
𝜑𝑆 ♯ by transforming 𝜑 in a similar way to trans𝑇𝑣𝑇 (𝜑) (see Fig. 3). However, here we use the Boolean
auxiliary variables as guards and the LIA auxiliary variables as parameters in order to consider
different possibilities for bounds, constants, and function and relation applications. This  affects
the transformation of terms, atomic formulas and quantifiers. For example, for B ♯ = 𝑥 ≥ 𝑑, ⊤ ,

                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:18                                                                       Neta Elad, Oded Padon, and Sharon Shoham

                                                          
the encoding of quantifiers will use 𝑏𝑛 : 𝑥 ≥𝑑 → 𝑥 ≥ 𝑑𝑛 ∧ (𝑏𝑛 : ⊤ → ⊤) as the bound formula for
a summary node 𝑛, and simply 𝑥 ≈ 0 for regular nodes. Atomic formulas use a conjunction of
Boolean auxiliary variables, accumulating the decisions for the constants, functions and relations
that appear in them, with the LIA auxiliary variables substituting the template free variables. For
example, transforming 𝑅(𝑓 (𝑐)) involves case splits using conjunctions of auxiliary variables for 𝑐,
𝑓 and 𝑅. Lastly, if 𝜑 has any free variables, the transformation adds a disjunction over all possible
symbolic assignments 𝑣 𝑆 .
    We use 𝜑 aux to enforce the following constraints: (i) for every constant, function and relation
symbol, exactly one Boolean auxiliary variable is true for each combination of argument nodes;
(ii) for each node, exactly one of the Boolean bound variables is true; (iii) for every constant,
the Boolean auxiliary variables map it to a regular node; and (iv) for every function and every
combination of argument nodes, their image according to the Boolean auxiliary variables satisfies
the selected bound formula of the image node, according to the Boolean bound variables. There are
no constraints for the LIA auxiliary variables. (Details in App. D.)
    Ultimately, we can check if 𝜑 is satisfied by some symbolic structure in 𝑆 ♯ (and if so find the
satisfying symbolic structure) by checking the satisfiability of 𝜑𝑆 ♯ ∧ 𝜑 aux , which can be done using
an SMT solver.
  Theorem 5.4. Given a formula 𝜑 over Σ and a symbolic-structure template 𝑆 ♯ , there exists a
symbolic structure 𝑆 in 𝑆 ♯ and an explicit assignment 𝑣 for E (𝑆) such that E (𝑆), 𝑣 |= 𝜑 iff there exists
an assignment 𝑣 ′ such that 𝑣 ′ |=LIA 𝜑𝑆 ♯ ∧ 𝜑 aux . Furthermore, we can efficiently extract 𝑆 and 𝑣 from 𝑣 ′ .

6   DECIDABILITY VIA SYMBOLIC STRUCTURES
In this section we introduce the Ordered Self Cycle (OSC) fragment, a new decidable fragment of
FOL, where satisfiable formulas always have symbolic models. OSC extends the decidable many-
sorted EPR fragment. We establish decidability of OSC by proving a novel “small symbolic model
property”, showing that every satisfiable OSC formula has a (possibly infinite) model representable
by a symbolic structure of a bounded size that uses a small subset of LIA. The proof of the “small
symbolic model property” identifies a computable template, with which the symbolic search
algorithm of Sec. 5 is guaranteed to find a symbolic model for formulas in the fragment. Combined
with soundness of the symbolic search, this yields a decision procedure for formulas in OSC.
   This section is organized as follows: we start by giving necessary background on the EPR
fragment, followed by a formal definition of the OSC fragment; we then continue with the proof of
decidability which is done by first considering single-sort formulas (Sec. 6.1), and then generalizing
to the many-sorted case (Sec. 6.2).
   EPR. The Effectively PRopositional (EPR) fragment of many-sorted FOL consists of formulas
whose quantifier-alternation graph is acyclic. The quantifier-alternation graph of a formula 𝜑 is a
directed graph (𝑉 , 𝐸), where the set of vertices 𝑉 is the set of sorts and the set of edges 𝐸 includes
an edge from 𝒔 1 to 𝒔 2 whenever (i) 𝜑 includes a function symbol where 𝒔 1 is the sort of one of the
arguments and 𝒔 2 is the range sort, or (ii) 𝜑 includes an ∃𝑦 : 𝒔 2 quantifier in the scope of a ∀𝑥 : 𝒔 1
quantifier (assuming 𝜑 is in negation normal form; otherwise the definition is extended according
to the standard translation to negation normal form).
   Acyclicity of the quantifier-alternation graph ensures that after Skolemization, there are finitely
many ground terms. That is, the Herbrand universe, as used in the proof of Herbrand’s theorem,
is finite.5 This leads to a small model property: every satisfiable EPR formula has a model whose
5 Herbrand’s theorem considers FOL without equality, however it extends to equality through its axiomatization, leading to

the same bounds on domain sizes.


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                 33:19


domain size is bounded by the number of ground terms of its Skolemized version, which also makes
satisfiability checking decidable. Moreover, the number of ground terms can be effectively computed.
   The OSC fragment. OSC extends the EPR fragment by allowing a designated sort, 𝒔 ∞ , thought
of as an “infinite” sort, which may have self-loops in the quantifier-alternation graph and whose
domain does not have a finite model property. That is, some satisfiable OSC formulas are only
satisfied by models where the domain of 𝒔 ∞ is infinite. However, OSC restricts the use of 𝒔 ∞
such that models can always be represented using symbolic structures from a restricted family,
essentially by restricting the use of 𝒔 ∞ to be monadic except for one (optional) binary relation ≺
that is axiomatized to be a strict linear order over 𝒔 ∞ . Formally, an OSC formula is 𝐴 ≺ ∧ 𝜓 ,6 where:
   (1) 𝐴 ≺ encodes the axioms of a strict linear order for ≺ (anti-reflexivity 𝑥 ⊀ 𝑥, transitivity
       𝑥 ≺ 𝑦 ∧ 𝑦 ≺ 𝑧 → 𝑥 ≺ 𝑧, and linearity 𝑥 ≺ 𝑦 ∨ 𝑦 ≺ 𝑥 ∨ 𝑥 ≈ 𝑦).
   (2) 𝜓 uses only one logical variable, 𝑥, of sort 𝒔 ∞ . (Variables of other sorts are not restricted.)
   (3) In the quantifier alternation graph of 𝜓 the only cycles are self-loops at 𝒔 ∞ , and the only
       outgoing edges from 𝒔 ∞ are to 𝒔 ∞ .
   (4) Functions and relations other than ≺ used in 𝜓 have at most one argument of sort 𝒔 ∞ .
   (5) The only non-ground term of sort 𝒔 ∞ that appears in 𝜓 as an argument to functions is 𝑥.
       (That is, functions whose range sort is 𝒔 ∞ cannot be nested in non-ground terms.)
For example, the Echo Machine’s invariants (Fig. 1) and transition formulas (e.g., Eq. (1)) are in OSC,
while the following are not: ∀𝑥, 𝑦 : 𝒔 ∞ . 𝑥 ≺ 𝑦 → 𝑓 (𝑥) ≺ 𝑓 (𝑦) (violates 2); ∀𝑥 : 𝒔 ∞ . ∃𝑦 : 𝒔. 𝑅(𝑥, 𝑦)
(violates 3); ∀𝑥 : 𝒔 ∞ . 𝑄 (𝑥, 𝑥) (violates 4); and ∀𝑥 : 𝒔 ∞ . 𝑥 ≺ 𝑓 (𝑓 (𝑥)) (violates 5).
  The S template family. To establish decidability, we prove that satisfiable OSC formulas have
symbolic models, and that all symbolic structures needed to satisfy formulas in OSC can be
represented by templates from the following family, denoted S, where: (i) bound formulas for all
summary nodes are ⊤, (ii) all function terms are 0 or 𝑥 1 + 𝑘 for some 𝑘 ∈ Z, and (iii) all relation
formulas are degenerate (⊤ or ⊥), except for ≺, where they can also be 𝑥 1 < 𝑥 2 or 𝑥 1 ≤ 𝑥 2 .
Furthermore, given an OSC formula, we can compute a sufficient finite subset of S, which we can
enumerate. Formally:
   Theorem 6.1. There exists a computable function F : OSC → P (S), such that for every formula
𝜑 ∈ OSC, F (𝜑) is finite, and 𝜑 is satisfiable iff there exists a template 𝑆 ♯ ∈ F (𝜑), and a symbolic
structure 𝑆 ∈ 𝑆 ♯ therein, such that E (𝑆) |= 𝜑.
   Corollary 6.2. Satisfiability is decidable for formulas in OSC.
   We prove Thm. 6.1 in two steps: firstly, we discuss the case where there are no sorts other than
𝒔 ∞ (Sec. 6.1), and secondly, we generalize our construction to many sorts (Sec. 6.2).

6.1    Step 1: Single Sort Construction
In this first step of the proof, we consider the simpler case of OSC formulas where the only sort
appearing in a formula is the infinite sort. Let 𝜑 = 𝐴 ≺ ∧ 𝜓 be an OSC formula where the only
sort is 𝒔 ∞ . (Note that in the case of a single sort, all function and relation symbols in 𝜑, except
for ≺, must be unary.) The single-variable requirement ensures that 𝜓 can be Skolemized into an
equi-satisfiable formula 𝜓 ′ by introducing a Skolem constant for every existential quantifier (in
negation normal form), even if it is in the scope of a universal quantifier.

6 If 𝜓 does not include 𝒔 ∞ and/or ≺, then 𝐴
                                              ≺ may be omitted. Still, in that case, any model of 𝜓 can be extended to a model
of 𝐴 ≺ . Hence, adding 𝐴 ≺ does not restrict the set of models. For simplicity of the presentation, we therefore assume that ≺
and its axiomatization are always included in OSC formulas.


                                  Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:20                                                                      Neta Elad, Oded Padon, and Sharon Shoham


   Let 𝐺 denote the set of ground terms, ℓ the number of function symbols, and 𝑚 the number of
unary relations that appear in 𝜓 ′ . We show that if 𝜑 is satisfiable, there exists a template 𝑆 ♯ ∈ S
and a symbolic structure 𝑆 ∈ 𝑆 ♯ therein, such that E (𝑆) |= 𝜑. Further, 𝑆 ♯ (and 𝑆) has at most |𝐺 |
regular nodes and 𝑏 (ℓ + 1) · 2𝑚 (ℓ+1) · (|𝐺 | + 1) ℓ+1 summary nodes, where 𝑏 (𝑛) is the 𝑛’th ordered
Bell number counting the number of weak orderings on a set of n elements. In addition, all function
terms are 0 or 𝑥 1 + 𝑘 for some −ℓ ≤ 𝑘 ≤ ℓ. The bounds on the number of nodes and on 𝑘 restrict
the set of relevant templates in S to a finite subset, which defines F (𝜑) in Thm. 6.1.
   Skolemization ensures that the models of 𝜑 = 𝐴 ≺ ∧ 𝜓 are the same as the models of 𝐴 ≺ ∧ 𝜓 ′
when the latter are projected onto the original        vocabulary. It therefore suffices to reason about
models of 𝜑 ′ = 𝐴 ≺ ∧ 𝜓 ′ . Let 𝑀 = D 𝑀 , I 𝑀 be a model for 𝜑 ′ . We construct a symbolic structure
                                                

𝑆 = D 𝑆 , B𝑆 , I 𝑆 such that E (𝑆) |= 𝜑 ′ and therefore E (𝑆) |= 𝜑. (Note that E (𝑆) need not be
isomorphic to 𝑀.)
    Domain. To define the domain of 𝑆, we first partition the elements of D 𝑀 to equivalence classes
 according to whether or not they satisfy the following atoms in 𝑀:
(D-1) Element atoms: these consist of order element atoms, of the form 𝑥 ⊲⊳ 𝑔 where ⊲⊳ ∈ {≺, ≈, ≻}7
        and 𝑔 ∈ 𝐺; and relation element atoms, of the form 𝑅(𝑥), where 𝑅 is a unary relation symbol.
(D-2) Image atoms: these consist of order image atoms, of the form 𝑓 (𝑥) ⊲⊳ 𝑔; and relation image
        atoms, of the form 𝑅(𝑓 (𝑥)), where 𝑓 is a unary function symbol.
(D-3) Mixed atoms: 𝑡 ⊲⊳ 𝑡 ′ , where 𝑡, 𝑡 ′ ∈ {𝑥 } ∪ {𝑓 (𝑥) | 𝑓 is a unary function symbol}.
 Each class is labeled with the set of atoms satisfied by its elements. We introduce a node in the
 domain of the symbolic structure, D 𝑆 , for each class in the partition. Classes labeled by an atom of
 the form 𝑥 ≈ 𝑔 for some ground term 𝑔 are regular nodes (i.e., with bound formula 𝑥 ≈ 0), and the
 rest are summary nodes with bound formula ⊤. Note that for every ground term 𝑔 ∈ 𝐺, exactly
 one node is labeled 𝑥 ≈ 𝑔. This means that each ground term corresponds to a single regular node
 (a regular node may correspond to multiple ground terms that are equal in 𝑀). In particular, the
 number of regular nodes is bounded by |𝐺 |.
    The number of summary nodes is bounded by the number of feasible combinations of atoms:
 combinations of mixed atoms are bounded by 𝑏 (ℓ + 1), combinations of relation (element and image)
 atoms are bounded by 2𝑚 (ℓ+1) , and combinations of order (element and image) atoms are bounded
 by (|𝐺 | + 1) ℓ+1 (see discussion of segments delimited by ground terms below).
    For each element 𝑒 ∈ D 𝑀 we use    𝜏 (𝑒) 𝑀for the node in D that corresponds
                                                                   𝑆                    to its class, and for
 each node 𝑛 ∈ D we use 𝐸 (𝑛) = 𝑒 ∈ D | 𝜏 (𝑒) = 𝑛 for the set of D 𝑀 elements in its class. (For
                     𝑆

 regular nodes, 𝐸 (𝑛) is a singleton.) We assume an arbitrary strict linear order on the nodes, denoted
 ≪, which we use as a tiebreaker when defining the interpretation of ≺ and the function symbols.
    Note that the partitioning takes into account all the atoms that may appear as non-ground atomic
 formulas in 𝜓 ′ . Thus, grouping elements to classes according to atoms and defining a node for
 each class allows us to define a symbolic structure where the explicit elements of 𝑛 in E (𝑆) satisfy
 exactly the same atomic formulas as 𝐸 (𝑛) in 𝑀. This, in turn, ensures that E (𝑆) satisfies 𝜑 ′ .
    Interpretation of constants. For a constant
                                                𝑐, we define 𝑐 𝑆 to be 𝑐 𝑆 = ⟨𝑛, 0⟩, where 𝑛 is the regular
 node labeled 𝑥 ≈ 𝑐. Note that 𝑛 = 𝜏 𝑐 .  𝑀

    Interpretation of unary relations. Unary relations are determined to be either ⊤ or ⊥ for each
 node based on the relation element atoms that label it. Namely, 𝑅𝑆 (𝑛) is ⊤ if 𝑅(𝑥) labels 𝑛 and ⊥
 otherwise, for every unary relation 𝑅 and node 𝑛.
    Interpretation of ≺. Defining ≺𝑆 is not as straightforward, as it is not fully determined by the
 labeling. Since each ground term in 𝐺 has a corresponding regular node, the labeling by order
7We write 𝑥 ≻ 𝑔 for 𝑔 ≺ 𝑥.



Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                        33:21


element atoms essentially dictates an order on all the ground terms (and accordingly the regular
nodes), and places each summary node in a segment delimited by ground terms. For example, if
there are 3 ground terms 𝑔1, 𝑔2, 𝑔3 and the labeling dictates 𝑔1 ≺ 𝑔2 ≈ 𝑔3 , then one regular node
corresponds to 𝑔1 , another to 𝑔2 ≈ 𝑔3 , and each summary node is either smaller than 𝑔1 , between
𝑔1 and 𝑔2 ≈ 𝑔3 , or greater than 𝑔2 ≈ 𝑔3 . Therefore, the only remaining question is how to order
summary nodes that are in the same segment. We use this observation to distinguish between the
following cases in the definition of 𝑛 ≺𝑆 𝑛 ′ :
(O-1) If either of 𝑛, 𝑛 ′ is a regular node, then it corresponds to a ground term 𝑔 and 𝑛 ≺𝑆 𝑛 ′ is
      determined to be either ⊤ or ⊥ by the order induced by the labeling. For example, if 𝑛 is
      labeled 𝑥 ≈ 𝑔 and 𝑛 ′ is labeled 𝑥 ≻ 𝑔 then 𝑛 ≺𝑆 𝑛 ′ is ⊤.
(O-2) If both 𝑛 and 𝑛 ′ are summary nodes that belong to different segments, 𝑛 ≺𝑆 𝑛 ′ is determined
      by the labeling via transitivity. That is, if there exists some ground term 𝑔 such that 𝑛 is
      labeled 𝑥 ≺ 𝑔 and 𝑛 ′ is labeled 𝑥 ≻ 𝑔 (or vice versa), then 𝑛 ≺𝑆 𝑛 ′ is ⊤ (respectively, ⊥).
(O-3) For summary nodes 𝑛 and 𝑛 ′ that are in the same segment, we use the standard < order over
      the integers to determine the order between ⟨𝑛, 𝑧⟩ and ⟨𝑛 ′, 𝑧 ′ ⟩, and use ≪ as a tiebreaker
      when 𝑧 = 𝑧 ′ . Formally, we define 𝑛 ≺𝑆 𝑛 ′ to be 𝑥 1 ≤ 𝑥 2 if 𝑛 ≪ 𝑛 ′ and 𝑥 1 < 𝑥 2 otherwise.
   (O-3) means that within each segment that includes summary nodes, the ordering of the (infinitely
many) elements in E (𝑆) always alternates between elements from different summary nodes. For
example, if 𝑛 1 and 𝑛 2 are two summary nodes in the same segment with 𝑛 1 ≪ 𝑛 2 , then the ordering
in E (𝑆) is · · · ≺ E (𝑆 ) ⟨𝑛 1, −1⟩ ≺ E (𝑆 ) ⟨𝑛 2, −1⟩ ≺ E (𝑆 ) ⟨𝑛 1, 0⟩ ≺ E (𝑆 ) ⟨𝑛 2, 0⟩ ≺ E (𝑆 ) ⟨𝑛 1, 1⟩ ≺ E (𝑆 )
⟨𝑛 2, 1⟩ ≺ E (𝑆 ) · · · . For an illustration of ≺ E (𝑆 ) see App. B. We note that this ordering is independent
of 𝑀. That is, the ordering would be alternating as above even if ∀𝑒 ∈ 𝐸 (𝑛 1 ), 𝑒 ′ ∈ 𝐸 (𝑛 2 ). 𝑒 ≺𝑀 𝑒 ′ .
   Interpretation of unary functions. The most intricate step in our construction is showing that it is
possible to define an interpretation of the functions that is consistent with the labeling. For a unary
function symbol 𝑓 , we define the node in the image of 𝑓 𝑆 according to the image atoms of 𝑓 and
the corresponding term according to the mixed atoms.
   Specifically, for a node 𝑛 labeled with a set 𝐿 of image atoms for 𝑓 , let 𝑛 ′ be a node labeled with
a set 𝐿 ′ of element atoms, such that (i) {𝑎[𝑓 (𝑥)/𝑥] | 𝑎 ∈ 𝐿 ′ } = 𝐿 (i.e., the element atoms of 𝑛 ′
agree with the 𝑓 -image atoms of 𝑛), and (ii) if 𝑥 ≈ 𝑓 (𝑥) labels 𝑛, then 𝑛 ′ = 𝑛; otherwise, 𝑛 ′ is the
least according to ≪ among all nodes that satisfy (i).89 Furthermore, to define the term in 𝑓 𝑆 (𝑛)
while ensuring consistency with the mixed atoms that label 𝑛 (e.g., 𝑓 (𝑥) ≺ 𝑔(𝑥), 𝑓 (𝑥) ≈ 𝑔(𝑥)),
we observe that the mixed atoms partition 𝑆 = {𝑥 } ∪ {ℎ(𝑥) | ℎ is a unary function symbol} into
linearly ordered classes of “equal” terms. This order is isomorphic to {0, . . . , 𝑁 } for some natural
number 𝑁 < |𝑆 |, and we let 𝜇 be the mapping that assigns to each 𝑡 ∈ 𝑆 the number in {0, . . . , 𝑁 }
isomorphic to its class. For example, if 𝑆 = {𝑥, 𝑔(𝑥), ℎ(𝑥)} and 𝑛 is labeled with 𝑔(𝑥) ≺ 𝑥 and
ℎ(𝑥) ≈ 𝑥 then 𝜇 (𝑔(𝑥)) = 0, and 𝜇 (𝑥) = 𝜇 (ℎ(𝑥)) = 1. Finally, we let 𝑘 = 𝜇 (𝑓 (𝑥)) − 𝜇 (𝑥) be the
(possibly negative) “distance” between the classes of 𝑓 (𝑥) and 𝑥 according to the aforementioned
order, and define 𝑓 𝑆 (𝑛) using 𝑘 as follows:
                                     ( ′
                                      𝑛 ,0                                     if 𝑛 ′ is a regular node,                      (F -1)
                         𝑓 𝑆 (𝑛) =       ′
                                       𝑛 , 𝑥1 + 𝑘                              otherwise.                                     (F -2)

  The use of 𝑘 ensures function interpretations are consistent with 𝑛’s mixed atoms. Specifically, if
𝑥 ≈ 𝑓 (𝑥) labels 𝑛 then 𝑛 ′ = 𝑛 and 𝑘 = 0, and if 𝑔(𝑥) ≺ ℎ(𝑥) labels 𝑛 then the 𝑘 used for 𝑔 is smaller
than the 𝑘 used for ℎ. If the image nodes of both 𝑔(𝑥) and ℎ(𝑥) are summary nodes within the same

8 Such a node must exist (consider 𝜏 𝑓 𝑀 (𝑒 )
                                                
                                                    for some 𝑒 ∈ 𝐸 (𝑛)).
9We use the minimal according to ≪ only as a way to get a deterministic choice, since the choices made for different

functions should be consistent (e.g., if 𝑛 is labeled 𝑓 (𝑥 ) ≈ 𝑔 (𝑥 )). This is not related to the role of ≪ as a tiebreaker for ≺𝑆 .


                                     Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:22                                                                        Neta Elad, Oded Padon, and Sharon Shoham


Fig. 5. An infinite model 𝑀                                                                                    𝑓

and its constructed symbolic               𝑓                   𝑓               𝑓           𝑓                       𝑓
                                     ...       𝑅𝑀     𝑅𝑀                𝑐𝑀           𝑅𝑀                       𝑅𝑀       ...
structure 𝑆. The interpreta-
tion of ≺ orders elements
                                                                                                     𝑓
from left to right; adjacent                   𝑓
                                                                              𝑀
summary nodes are ordered                                  𝑓 : 𝑥1 − 1
                                                                              𝑆
                                                                                                 𝑓 : 𝑥1 + 1
alternatingly. Bound formu-                                                   𝑓 :0        𝑓 :0
                                                      𝑅𝑆                𝑐𝑆           𝑅𝑆                       𝑅𝑆
las for summary nodes are ⊤.                               𝑓 : 𝑥1 − 1
                                                                                                 𝑓 : 𝑥1 + 1




segment, the choice of 𝑘 ensures the the correct ordering of the images, otherwise, the order is
guaranteed by the ordering of the segments.
  The following lemma summarizes the correctness of the construction (see proof in App. A).
  Lemma 6.3. For any OSC formula 𝜑 where the only sort is 𝒔 ∞ , and any model thereof, if 𝑆 is the
symbolic structure obtained by the above construction, then E (𝑆) |= 𝜑.

   Example 6.4. Consider the model 𝑀 for 𝜑 = 𝐴 ≺ ∧ ¬𝑅(𝑐) ∧ 𝑅(𝑓 (𝑐)) ∧ ∀𝑥 .(𝑅(𝑥)↔¬𝑅(𝑓 (𝑥))) ∧
(𝑐 ≼ 𝑥↔𝑥 ≺ 𝑓 (𝑥)) ∧ 𝑥 ̸≈ 𝑓 (𝑥) depicted in Fig. 5 (top). The construction above yields the symbolic
structure 𝑆 shown in Fig. 5 (bottom). The formula has two ground terms, 𝑐 and 𝑓 (𝑐), so 𝑆 has two
regular nodes. As for summary nodes, observe that in 𝑀 elements fall into two segments (𝑀 has
no elements “between” 𝑐 and 𝑓 (𝑐)); moreover, the elements in each segment fall into one of two
equivalence classes, yielding a total of four summary nodes in 𝑆.
   Note that E (𝑆) and 𝑀 are not isomorphic. In particular, in 𝑀 there are two elements, adjacent
according to ≺𝑀 , that both satisfy 𝑅(𝑥) (e.g., the two top-left elements drawn in Fig. 5), whereas 𝑆
completely regularizes the pattern of alternating 𝑅(𝑥) and ¬𝑅(𝑥) elements.
   Remark 6.5. The restriction OSC imposes on nesting of 𝒔 ∞ functions is crucial for the construction,
but it is only essential for mixed atoms, where it disallows atoms like 𝑓 (𝑓 (𝑥)) ≺ 𝑥. Such atoms would
invalidate the construction that defines 𝑓 𝑆 (𝑛) solely according to the labeling of 𝑛. Note that an atom
like 𝑅(𝑓 (𝑓 (𝑥)))) can be simulated in OSC as 𝑅 ′ (𝑓 (𝑥)) where 𝑅 ′ is a fresh unary relation symbol
axiomatized by ∀𝑥 .𝑅 ′ (𝑥)↔𝑅(𝑓 (𝑥)). Atoms like 𝑓 (𝑓 (𝑥)) ≺ 𝑔 can be similarly encoded.

6.2 Step 2: Generalizing to Many Sorts
In the remainder of this section, we generalize the construction of the previous section to many
sorts, thus proving decidability of the OSC fragment. The generalization is done by refining the
partitions induced by the atoms defined in (D-1), (D-2) and (D-3).
   Given 𝜑 = 𝐴 ≺ ∧𝜓 , we first transform 𝜓 to 𝜓 ′ as in Sec. 6.1. In particular, all existential quantifiers
over sort 𝒔 ∞ are Skolemized by functions from sorts other than 𝒔 ∞ to 𝒔 ∞ . We observe that for each
sort 𝒔 ≠ 𝒔 ∞ only finitely many ground terms can be constructed, since the quantifier-alternation
graph of 𝜓 ′ is acyclic except for self-loops at 𝒔 ∞ and 𝒔 ∞ has no outgoing edges to other sorts.
Hence, given a model 𝑀 |= 𝜑 ′ = 𝐴 ≺ ∧ 𝜓 ′ , we can apply Herbrand’s construction (adapted to handle
equality) to obtain a model 𝑀 ′ |= 𝜑 ′ where the domain of each sort 𝒔 ≠ 𝒔 ∞ is bounded by the
number of ground terms (as in many-sorted EPR). Each element in these domains will become a
regular node in the symbolic structure 𝑆, setting bounds on the domain sizes of all sorts 𝒔 ≠ 𝒔 ∞ in
𝑆. The interpretation of all constant, relation and function symbols that do not include 𝒔 ∞ in 𝑆 will
be exactly as in 𝑀 ′ (using only ⊤ and ⊥ for relation formulas and 0 for function terms).
   Next, we address the elements of sort 𝒔 ∞ in 𝑀 ′ . These are grouped into finitely many summary
and regular nodes in 𝑆 by a variant of the construction from Sec. 6.1, where we use the ground
terms of the other sorts to refine the partition of the elements of 𝒔 ∞ . Specifically:

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                        33:23


   (1) We treat all (finitely many) instantiations of multi-ary functions with (one) argument and
range sort 𝒔 ∞ on the ground terms of sorts 𝒔 ≠ 𝒔 ∞ as unary functions from 𝒔 ∞ to 𝒔 ∞ , and extend the
sets of image- and mixed atoms to refer to them. For example, given 𝑓 : 𝒔 ∞ × 𝒔 → 𝒔 ∞ , we add the
atoms 𝑥 ≺ 𝑓 (𝑥, 𝑔), 𝑥 ≈ 𝑓 (𝑥, 𝑔), and 𝑥 ≻ 𝑓 (𝑥, 𝑔) as mixed atoms for each ground term 𝑔 of sort 𝒔.
   (2) We treat all (finitely many) instantiations of functions with range 𝒔 ∞ and no argument of
sort 𝒔 ∞ on the ground terms of the other sorts as additional ground terms of sort 𝒔 ∞ , and extend the
set of order (element and image) atoms to refer to them. For example, given ℎ : 𝒔 ′ → 𝒔 ∞ and 𝑓 as
before, we add the atoms 𝑥 ⊲⊳ ℎ(𝑔′ ) and 𝑓 (𝑥, 𝑔) ⊲⊳ ℎ(𝑔′ ) for all ground terms 𝑔′, 𝑔 of sorts 𝒔 ′, 𝒔, resp.
   (3) We treat all (finitely many) instantiations of relation symbols other than ≺ that include 𝒔 ∞
on the ground terms of the other sorts as additional unary relation symbols of sort 𝒔 ∞ , and add
the corresponding relation (element and image) atoms. For example, given 𝑅 : 𝒔 ∞ × 𝒔 ′ , we add the
atoms 𝑅(𝑥, 𝑔′ ) and 𝑅(𝑓 (𝑥, 𝑔), 𝑔′ ) for all ground terms 𝑔′, 𝑔 of sorts 𝒔 ′, 𝒔, resp.
   The interpretation of the constant, relation and function symbols that include 𝒔 ∞ in 𝑆 is defined
similarly to Sec. 6.1. Hence, we obtain a symbolic structure 𝑆, such that E (𝑆) |= 𝜑; the domain
of each sort 𝒔 ≠ 𝒔 ∞ consists only of regular nodes, whose number is bounded by the number of
ground terms of the corresponding sort; and the domain of 𝒔 ∞ consists of summary and regular
nodes, whose number is bounded by the equivalence classes of the refined partition. The function
terms and relation formulas used in 𝑆 are restricted as in Sec. 6.1. Thus, we have a computable
finite subset of S which includes a template 𝑆 ♯ such that 𝑆 ∈ 𝑆 ♯ . Relating back to 𝑇ℎ𝑚. 6.1, for any
formula 𝜑, we define F (𝜑) to be the finite subset of S that meets the restrictions above.

7   IMPLEMENTATION AND EVALUATION
We implemented the ideas presented in this paper in a tool named FEST (Find and Evaluate Symbolic
structures via Templates).10 FEST allows the user both to specify symbolic structures manually
and model-check them against FOL formulas, and to automatically find a symbolic model for a
given formula. The symbolic model finding procedure uses automatically-computed “heuristic”
templates, or a user-provided template. FEST is implemented in Python, takes input in SMTLIB
syntax [Barrett et al. 2017], and uses cvc5 [Barbosa et al. 2022] as the backend for checking LIA
formulas (per Thm. 4.7 and 5.4).
   We evaluated FEST’s symbolic model finding capabilities with the heuristic templates on a host
of examples with very positive results — FEST found symbolic models for all of the examples, and
many of the symbolic models are captured by the template family S of OSC. We compare against
the SMT solvers cvc5 and Z3 [de Moura and Bjørner 2008], and the resolution-based theorem
prover Vampire [Riazanov and Voronkov 1999], all of which diverge when run on these examples.

                                                                  ⊤, ⊥, 𝑥 1 < 𝑥 2 , 𝑥 1 ≤ 𝑥 2 , 𝑥 1 ≥ 𝑥 2 , 𝑥 1 > 𝑥 2 ,
                      ♯                                                                                                  
                    BH = ⊤, 𝑥 ≥ 𝑑 , 𝑥 ≤ 𝑑
                                                                 
                                                                                                                          
                                                                                                                           
                                                                                                                           
                                                         ♯
                  ♯                                    IH  (𝑅) =    𝑥 1 ≈ 0, 𝑥 1 ≈ 𝑥 2 , 𝑥 1 ≈ 𝑥 2 + 1, 𝑥 1 ≈ 𝑥 2 − 1,
                 IH (𝑓 ) = {0, 𝑥 1 , 𝑥 1 + 1, 𝑥 1 − 1}            𝑥 1 ≤ 𝑥 2 < 𝑥 3, 𝑥 3 ≤ 𝑥 2 < 𝑥 1, 𝑥 1 ≈ 𝑥 2 ≈ 𝑥 3
                                                                                                                          
                                                                                                                           
                                                                                                                          
                     Fig. 6. The heuristic template family H, parameterized by domain D.

   Heuristic templates. FEST uses the heuristic template family H defined in Fig. 6, and a domain
enumeration strategy for the number of regular and summary nodes. The design of H was motivated
by the S template family of OSC, extended11 to support functions and relations of greater arity
than what the syntactic restrictions of OSC allow. The H family uses bound formulas with template
free variables (𝑥 ≥ 𝑑, 𝑥 ≤ 𝑑 ) to represent half-space summary nodes, but avoids them in function
terms and relation formulas since they lead to harder LIA queries for the solver, and did not provide
10We plan to open-source the implementation once the paper is published.
11 Templates for OSC may include function terms 𝑥 ± 𝑘 where 1 < 𝑘 ≤ ℓ (see Sec. 6.1). However, in our benchmarks ℓ = 1.



                                   Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:24                                                                      Neta Elad, Oded Padon, and Sharon Shoham


a benefit for the examples we considered. The enumeration strategy prioritizes templates with
homogeneous domain sizes and smaller total domain size.

   Optimizations. FEST implements the translations to LIA developed in Sec. 4 and 5, with several
optimizations. First, when searching for a satisfying symbolic structure for a given formula, the
interpretation of one constant from each sort is arbitrarily fixed to the first regular node of that
sort, under an arbitrary node ordering. This symmetry breaking reduces the search space but does
not hurt completeness since any symbolic structure is isomorphic to one of the symbolic structures
considered. Second, since ≺ is assumed to be a strict linear order, we have that for 𝑥 ≠ 𝑦, 𝑥 ≺ 𝑦 iff
𝑦 ⊀ 𝑥. Thus, for every two nodes we define auxiliary variables for ≺ only for one of the two possible
permutations (and derive the other one). Third, for the interpretation of functions and relations, we
consider a term or formula with a symbolic-structure free variable 𝑥𝑖 only for arguments 𝑛 1, . . . , 𝑛𝑘
where 𝑛𝑖 is a summary node. For example, for a unary function 𝑓 the terms 𝑥 1, 𝑥 1 + 1, 𝑥 1 − 1 will only
be considered when the argument is a summary node; for regular nodes the term 0 will always be
used. This is in line with what OSC guarantees in symbolic models, and indeed works for examples
both in and outside of OSC.

   Evaluation. We evaluated FEST in comparison to Z3, cvc5 and Vampire. Current solvers do not
detect infinite models, and prior work on SMT-based verification circumvented them in various
ways. For example, [Feldman et al. 2017] avoids infinite counter-models by manually adding axioms,
and [Goel and Sakallah 2021b] checks only bounded instances and compares inferred invariants
to hand-written ones. As there is no standard benchmark suite for infinite models, we curated
a set of 21 examples of distributed protocols and programs manipulating linked lists, based on
prior work where FOL is used as an abstraction and infinite models may arise. We run the tools on
these examples using a Macbook Pro with an Apple M1 Pro CPU and 32 GB RAM, with Z3 version
4.12.2, cvc5 version 1.0.8, and Vampire version 4.5.1. The results are summarized in Tab. 2. For each
example, the table indicates if the example is in OSC, the number of regular and summary nodes in
the infinite sort, the numbers of nodes in other sorts, and the run time for finding the symbolic
model. Running time was averaged across 10 runs.
   FEST is able to effectively find symbolic models for all 21 examples. In contrast, Z3, cvc5 and
Vampire are unable to conclude that these examples are satisfiable, and consistently time out after
10 minutes or return “unknown” on all of these examples. (We do not expect the results to be
different for any higher timeout threshold.) To demonstrate the general usefulness of symbolic
structures for representing and finding infinite models we also include an anecdotal example where
we find a non-standard model of non-commutative addition. We briefly describe each example in
the sequel; the formal modeling and depictions of some of the symbolic structures are in App. B.
   Echo Machine. The running example from Sec. 2, inspired by the Paxos protocol.
   Paxos protocol and variants. These are distributed consensus protocols for agreeing on a value
among sets of “acceptors” and “values” of unknown size. Our FOL modeling follows [Goel and
Sakallah 2021b]. We present 5 variants of Paxos: abstract Paxos (“Voting” protocol [Lamport 2019]),
simple and implicit Paxos [Goel and Sakallah 2021b], regular Paxos [Lamport 1998], and flexible
Paxos, which considers a weaker quorum intersection assumption [Howard et al. 2016]. The infinite
counter-models resemble that of the Echo Machine, where rounds play a similar role.
   Line Leader. A simple distributed protocol to elect a leader for a set of nodes ordered in a line.
   Ring Leader. This example models a leader election protocol for a set of nodes ordered in a
ring topology [Chang and Roberts 1979], and tries to prove a simplified form of termination
following [Feldman et al. 2017; Padon et al. 2016]. The infinite counterexample essentially represents

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                        33:25


Table 2. Evaluation results for FEST. We report the mean and standard deviation of run time across 10 runs
with different random seeds. “-” denotes timeout after 10 minutes.
                               𝒔 ∞ Size        Others’                                                      𝒔 ∞ Size
    Example           In OSC                                Time (s)       Example                 In OSC                  Time (s)
                               (reg./sum.)     Sizes                                                        (reg./sum.)
    Echo Machine       Yes        1/1                 2      0.18 ± 0.01   List length †            No         1/1        0.09 ± 0.00
    Voting protocol    No         2/1           3, 2, 2     45.28 ± 6.95   List segment (const)     No         1/1        0.17 ± 0.01
    Simple Paxos       No         2/1           2, 2, 2     12.72 ± 0.14   List segment (var)       No         1/1        0.25 ± 0.01
    Implicit Paxos     No         2/1           3, 2, 2   133.09 ± 41.43   List segment (order)     No         2/1        0.97 ± 0.04
    Paxos              No         2/1           3, 3, 2    79.69 ± 22.22   List segment (rev)       No         1/1        0.54 ± 0.07
    Flexible Paxos     No         2/1        3, 3, 1, 1     27.51 ± 0.20   Doubly-linked list       No         1/1        0.16 ± 0.01
    Ring Leader        No         0/1              n/a       0.08 ± 0.00   Doubly-linked length     No         1/1        0.16 ± 0.01
    Line Leader        No         2/1              n/a       1.59 ± 0.08   Doubly-linked segment    No         1/1        0.35 ± 0.02
                                                                           Reverse list             No         2/1        0.86 ± 0.02
                                                                           Sorted list length †     No         1/1        0.09 ± 0.00
                                                                           Sorted list              No         1/1        0.10 ± 0.00
                                                                           Sorted list segment      No         1/1        0.20 ± 0.01
                                                                           Sorted list max          Yes        1/1        0.06 ± 0.00



an infinite ring. While the partial models presented in [Feldman et al. 2017] suggest to the user
that an infinite counterexample exists, FEST is able to find one explicitly.
   Linked Lists. The right-hand side of Tab. 2 contains examples of verification of linked lists
properties (e.g., that reversing a list does not change the set of elements within it). The first 12
examples consist of all of the linked lists examples from [Löding et al. 2018]. There, linked lists are
defined inductively, and the least-fixed-point semantics is approximated in FOL by manually adding
induction axioms. We remove the added axioms, and show that indeed infinite counter-models
arise. For two of the examples which mix LIA and uninterpreted FOL together (example 1 and 10,
marked by †), we model the LIA sort as an uninterpreted sort with a single, unbounded summary
node. This hints at the future possibility of combining symbolic structures with theories. The last
example (“Sorted list max”) was inspired by [Löding et al. 2018], but proves a different property of
sorted linked lists: that the last element is larger than the first.
   Axiomatic Arithmetic. For the standard axiomatization of Presburger arithmetic with successor
and addition (𝑠 (𝑥) ≠ 0, 𝑠 (𝑥)=𝑠 (𝑦) → 𝑥=𝑦, 𝑥 + 0 = 𝑥, 𝑥 + 𝑠 (𝑦) = 𝑠 (𝑥 + 𝑦)), it is well known
that proving commutativity of addition (by induction) requires auxiliary lemmas. Interestingly, a
counterexample demonstrating this can be represented by a symbolic structure. For this example,
the user must provide two additional function terms 𝑥 1 + 𝑥 2, 𝑥 1 + 𝑥 2 + 1. Using these, FEST finds a
symbolic structure that has two summary nodes in about 5 seconds (see Fig. 11 in App. B).

8   RELATED WORK
   Reasoning over specific infinite structures. Several seminal works [Büchi 1990; Büchi and Landweber
1969; Rabin 1969] consider monadic second-order logic (MSO) over the specific (infinite) structures
of lines (S1S) and trees (S2S). These works use finite state automata to represent infinite models.
Linear Temporal Logic (LTL) [Gerth et al. 1995; Rozier and Vardi 2007; Vardi 1995] also considers
verification in the context of the specific infinite structure of the naturals. [Klin and Szynwelski
2016] develops a verification framework over the naturals and the rationals. In contrast, we aim to
discover infinite counter-models for VCs that are meant to be valid over all structures.
   Representing infinite and unbounded structures. [Bárány et al. 2011; Blumensath and Grädel 2004;
Khoussainov and Nerode 1994] introduce automatic structures, which represent infinite structures
using automata and regular languages. However, they do not automatically find a satisfying structure
for a given formula, nor identify a decidable fragment where representable satisfying structures
are guaranteed to exist. The finite representation of infinite terms of co-datatypes introduced
in [Reynolds and Blanchette 2017] resemble summary nodes. However, summary nodes represent

                                   Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:26                                                                      Neta Elad, Oded Padon, and Sharon Shoham


infinitely many different elements while an infinite term represents a single element. Symbolic
structures are inspired by TVLA [Lev-Ami and Sagiv 2000; Sagiv et al. 1999], but whereas in TVLA
summary nodes represent an unbounded finite number of elements, we use summary nodes to
represent infinitely many elements. The use of LIA terms and formulas in symbolic structures
resembles symbolic automata [D’Antoni and Veanes 2021], where transitions carry predicates
over rich theories. Our construction of a symbolic structure in Sec. 6 bears some resemblances to
predicate abstraction [Graf and Saïdi 1997]. However, here it is only part of the decidability proof.
   Constructing infinite models. Existing SMT solvers [Barbosa et al. 2022; de Moura and Bjørner
2008; Dutertre and De Moura 2006] and resolution-based theorem provers [Riazanov and Voronkov
1999; Weidenbach et al. 2009] cannot construct infinite models. Resolution can sometimes terminate
when the clause set is saturated even if the counter-model is infinite. [Horbach and Sofronie-
Stokkermans 2013] uses constrained clauses in order to represent possibly infinite sets of saturated
clauses. [Bachmair and Ganzinger 2001; Peltier 2003] present theoretical constructions of counter-
models from saturated sets of clauses, but these constructions are not implemented in existing tools.
Recently, [Lynch and Miner 2023] showed that under certain restrictions, trigger-based quantifier
instantiation can be complete and used to prove satisfiability without an explicit construction
of the model. The model evolution calculus [Baumgartner et al. 2006; Baumgartner and Tinelli
2003] constructs Herbrand models based on a generalization of DPLL, where the interpretation
of relations is implicitly defined by a finite set of possibly non-ground literals. In contrast, our
approach represents the domain and the interpretation explicitly, using LIA formulas and terms.
Our approach is therefore complementary, and can give the user insight when other tools fail. In the
context of higher-order logic and inductive datatypes, [Blanchette and Claessen 2010] describes a
way to obtain finite fragments of nonstandard, infinite models, via a specific first-order abstraction.
Our approach finds entire infinite models for arbitrary first-order formulas, not tied to a specific
abstraction of inductive definitions, and yields a decidable fragment. Recently, [Parsert et al. 2023]
experimented with using syntax-guided synthesis [Alur et al. 2013] in order to construct infinite
models. Our use of templates resembles syntax-guided synthesis, but the partition of the domain
via summary nodes allows us to define more complex structures in a simpler way (using simpler
LIA terms).
   Decidable fragments of FOL in Verification. Existing verification approaches based on FOL either
restrict verification conditions to have finite models [Ge and de Moura 2009; Padon et al. 2017;
Taube et al. 2018], or use finite partial models that do not fully satisfy the formula but satisfy some
quantifier instantiations [Feldman et al. 2017; Neider et al. 2018; Preiner et al. 2017]. Complementary
to these approaches, we aim to explicitly find certain infinite models via a finite representation.
Coherent uninterpreted programs [Mathur et al. 2019, 2020] are another FOL-based approach where
programs are restricted such that safety verification is decidable. In contrast, we target a richer
formalism (in fact, Turing complete), focusing on VC checking rather than safety verification. There
is a rich literature on classical decidable fragments of FOL [Ackermann 1928; Börger et al. 2001;
Gödel 1932; Gurevich 1976; Lewis 1980; Löb 1967; Mortimer 1975; Shelah 1977; Voigt 2019]. Most of
these fragments have a finite model property, and many cannot axiomatize a linear order; to the
best of our knowledge, OSC is not subsumed by any known decidable fragment. Also related are
decidability results for finite satisfiability (e.g., [Danielski and Kieronski 2019; Shelah 1977]); these
fragments are similarly incomparable to OSC. Moreover, symbolic structures are useful beyond
OSC and extend the applicability of SMT solvers, which use the standard semantics of FOL.




Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                 33:27


9   CONCLUSION
This paper introduced symbolic structures as an efficient way to represent and discover infinite
models of FOL formulas. We presented a symbolic search algorithm to efficiently traverse vast
(possibly infinite) families of symbolic structures, encoded as symbolic-structure templates, and
designed a robust heuristic to construct such templates. Naturally, by restricting symbolic structures
via a template to use a finite subset of LIA, we are severely limiting the kind of symbolic structures
that can be found. Using empirically-proven templates strikes a balance between efficiency and
expressivity. Our evaluation of FEST demonstrates the effectiveness of the technique for finding
infinite counter-models. Beyond the empirical evaluation, we also made a theoretical contribution:
we identified a new decidable fragment of FOL, which extends EPR, where satisfiable formulas
always have a (possibly infinite) model representable by a symbolic model of a bounded size that
is captured by the aforementioned heuristic templates. Our technique can also be extended and
fine-tuned to different domains using specialized symbolic-structure templates. We consider this a
first step, and posit that automatic methods for finding infinite counter-models can have wide uses
in verification, in particular for guiding the user (or as part of a CEGAR-style algorithm) towards
amending the modeling, e.g., by adding instantiations of induction or other axiom schemes. Though
in some cases SMT solvers and theorem provers can use induction to find a refutation [Hajdú et al.
2021; Hozzová et al. 2021; Leino 2012; Reynolds and Kuncak 2015; Schoisswohl and Kovács 2021],
these mechanisms are incomplete and require heuristics [Kaufmann et al. 2013; Kaufmann and
Moore 1997]. Infinite counter-models obtained by integrating with FEST could provide hints for
instantiating the induction scheme.

DATA-AVAILABILITY STATEMENT
An extended version of this paper, with proofs and additional examples can be found at [Elad et al.
2023b]. An artifact for reproducing the results is available at [Elad et al. 2023a], and the latest
version of the tool can be obtained at [Elad et al. [n. d.]].

ACKNOWLEDGMENTS
We thank the anonymous reviewers and the artifact evaluation committee for comments which im-
proved the paper. We thank Raz Lotan and Yotam Feldman for insightful discussions and comments.
The research leading to these results has received funding from the European Research Council
under the European Union’s Horizon 2020 research and innovation programme (grant agreement
No [759102-SVIS]). This research was partially supported by the Israeli Science Foundation (ISF)
grant No. 2117/23.

REFERENCES
Wilhelm Ackermann. 1928. Über die Erfüllbarkeit gewisser Zählausdrücke. Math. Ann. 100, 1 (1928), 638–649. https:
   //doi.org/10.1007/BF01448869
Rajeev Alur, Rastislav Bodík, Garvit Juniwal, Milo M. K. Martin, Mukund Raghothaman, Sanjit A. Seshia, Rishabh Singh,
   Armando Solar-Lezama, Emina Torlak, and Abhishek Udupa. 2013. Syntax-guided synthesis. In Formal Methods in
   Computer-Aided Design, FMCAD 2013, Portland, OR, USA, October 20-23, 2013. IEEE, 1–8. https://doi.org/10.1109/FMCAD.
   2013.6679385
Leo Bachmair and Harald Ganzinger. 2001. Resolution Theorem Proving. In Handbook of Automated Reasoning. Elsevier and
   MIT Press, 19–99.
Thomas Ball, Nikolaj S. Bjørner, Aaron Gember, Shachar Itzhaky, Aleksandr Karbyshev, Mooly Sagiv, Michael Schapira, and
   Asaf Valadarsky. 2014. VeriCon: towards verifying controller programs in software-defined networks. In ACM SIGPLAN
   Conference on Programming Language Design and Implementation, PLDI ’14, Edinburgh, United Kingdom - June 09 - 11,
   2014, Michael F. P. O’Boyle and Keshav Pingali (Eds.). ACM, 282–293. https://doi.org/10.1145/2594291.2594317
Kshitij Bansal, Andrew Reynolds, Tim King, Clark W. Barrett, and Thomas Wies. 2015. Deciding Local Theory Extensions
   via E-matching. In CAV (2) (Lecture Notes in Computer Science, Vol. 9207). Springer, 87–105. https://doi.org/10.1007/978-3-


                                  Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:28                                                                         Neta Elad, Oded Padon, and Sharon Shoham


    319-21668-3_6
Vince Bárány, Erich Grädel, and Sasha Rubin. 2011. Automata-based presentations of infinite structures. In Finite and
    Algorithmic Model Theory. London Mathematical Society Lecture Note Series, Vol. 379. Cambridge University Press, 1–76.
    https://doi.org/10.1017/CBO9780511974960.002
Haniel Barbosa, Clark W. Barrett, Martin Brain, Gereon Kremer, Hanna Lachnitt, Makai Mann, Abdalrhman Mohamed,
    Mudathir Mohamed, Aina Niemetz, Andres Nötzli, Alex Ozdemir, Mathias Preiner, Andrew Reynolds, Ying Sheng,
    Cesare Tinelli, and Yoni Zohar. 2022. cvc5: A Versatile and Industrial-Strength SMT Solver. In Tools and Algorithms
    for the Construction and Analysis of Systems - 28th International Conference, TACAS 2022, Held as Part of the European
    Joint Conferences on Theory and Practice of Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part
    I (Lecture Notes in Computer Science, Vol. 13243), Dana Fisman and Grigore Rosu (Eds.). Springer, 415–442. https:
    //doi.org/10.1007/978-3-030-99524-9_24
Clark Barrett, Pascal Fontaine, and Cesare Tinelli. 2017. The SMT-LIB Standard: Version 2.6. Technical Report. Department of
    Computer Science, The University of Iowa. Available at www.SMT-LIB.org.
Peter Baumgartner, Alexander Fuchs, and Cesare Tinelli. 2006. Implementing the Model Evolution Calculus. Int. J. Artif.
    Intell. Tools 15, 1 (2006), 21–52. https://doi.org/10.1142/S0218213006002552
Peter Baumgartner and Cesare Tinelli. 2003. The Model Evolution Calculus. In CADE (Lecture Notes in Computer Science,
    Vol. 2741). Springer, 350–364. https://doi.org/10.1007/978-3-540-45085-6_32
Jasmin Christian Blanchette and Koen Claessen. 2010. Generating Counterexamples for Structural Inductions by Exploiting
    Nonstandard Models. In LPAR (Yogyakarta) (Lecture Notes in Computer Science, Vol. 6397). Springer, 127–141. https:
    //doi.org/10.1007/978-3-642-16242-8_10
Achim Blumensath and Erich Grädel. 2004. Finite Presentations of Infinite Structures: Automata and Interpretations. Theory
    Comput. Syst. 37, 6 (2004), 641–674. https://doi.org/10.1007/s00224-004-1133-y
Egon Börger, Erich Grädel, and Yuri Gurevich. 2001. The classical decision problem. Springer Science & Business Media.
Aaron R. Bradley, Zohar Manna, and Henny B. Sipma. 2006. What’s Decidable About Arrays?. In VMCAI (Lecture Notes in
    Computer Science, Vol. 3855). Springer, 427–442. https://doi.org/10.1007/11609773_28
J Richard Büchi. 1990. On a decision method in restricted second order arithmetic. In The collected works of J. Richard Büchi.
    Springer, 425–435. https://doi.org/10.1007/978-1-4613-8928-6_23
J. Richard Büchi and Lawrence H. Landweber. 1969. Definability in the Monadic Second-Order Theory of Successor. J. Symb.
    Log. 34, 2 (1969), 166–170. https://doi.org/10.2307/2271090
Ernest Chang and Rosemary Roberts. 1979. An improved algorithm for decentralized extrema-finding in circular configura-
    tions of processes. Commun. ACM 22, 5 (1979), 281–283. https://doi.org/10.1145/359104.359108
David C Cooper. 1972. Theorem proving in arithmetic without multiplication. Machine intelligence 7, 91-99 (1972), 300.
    https://doi.org/10.1007/10930755_5
Daniel Danielski and Emanuel Kieronski. 2019. Finite Satisfiability of Unary Negation Fragment with Transitivity. In MFCS
    (LIPIcs, Vol. 138). Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 17:1–17:15. https://doi.org/10.4230/LIPIcs.MFCS.
    2019.17
Loris D’Antoni and Margus Veanes. 2021. Automata modulo theories. Commun. ACM 64, 5 (2021), 86–95. https:
    //doi.org/10.1145/3419404
Leonardo Mendonça de Moura and Nikolaj S. Bjørner. 2007. Efficient E-Matching for SMT Solvers. In CADE (Lecture Notes
    in Computer Science, Vol. 4603). Springer, 183–198. https://doi.org/10.1007/978-3-540-73595-3_13
Leonardo Mendonça de Moura and Nikolaj S. Bjørner. 2008. Z3: An Efficient SMT Solver. In Tools and Algorithms for
    the Construction and Analysis of Systems, 14th International Conference, TACAS 2008, Held as Part of the Joint European
    Conferences on Theory and Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings
    (Lecture Notes in Computer Science, Vol. 4963), C. R. Ramakrishnan and Jakob Rehof (Eds.). Springer, 337–340. https:
    //doi.org/10.1007/978-3-540-78800-3_24
David Detlefs, Greg Nelson, and James B. Saxe. 2005. Simplify: a theorem prover for program checking. J. ACM 52, 3 (2005),
    365–473. https://doi.org/10.1145/1066100.1066102
Claire Dross, Sylvain Conchon, Johannes Kanig, and Andrei Paskevich. 2016. Adding Decision Procedures to SMT Solvers
    Using Axioms with Triggers. J. Autom. Reason. 56, 4 (2016), 387–457. https://doi.org/10.1007/s10817-015-9352-2
Bruno Dutertre and Leonardo De Moura. 2006. The yices smt solver. Tool paper at http://yices. csl. sri. com/tool-paper. pdf 2,
    2 (2006), 1–2.
Neta Elad, Oded Padon, and Sharon Shoham. [n. d.]. An Infinite Needle in a Finite Haystack: Finding Infinite Counter-Models
    in Deductive Verification (Artifact). https://doi.org/10.5281/zenodo.8404103
Neta Elad, Oded Padon, and Sharon Shoham. 2023a. An Infinite Needle in a Finite Haystack: Finding Infinite Counter-Models
    in Deductive Verification (Artifact). https://doi.org/10.5281/zenodo.10125136
Neta Elad, Oded Padon, and Sharon Shoham. 2023b. An Infinite Needle in a Finite Haystack: Finding Infinite Counter-Models
    in Deductive Verification. https://doi.org/10.48550/arXiv.2310.16762 arXiv:2310.16762 [cs.PL]


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                     33:29


Yotam M. Y. Feldman, Oded Padon, Neil Immerman, Mooly Sagiv, and Sharon Shoham. 2017. Bounded Quantifier Instantiation
   for Checking Inductive Invariants. In TACAS (1) (Lecture Notes in Computer Science, Vol. 10205). 76–95. https://doi.org/10.
   1007/978-3-662-54577-5_5
Yeting Ge and Leonardo Mendonça de Moura. 2009. Complete Instantiation for Quantified Formulas in Satisfiabiliby Modulo
   Theories. In Computer Aided Verification, 21st International Conference, CAV 2009, Grenoble, France, June 26 - July 2, 2009.
   Proceedings (Lecture Notes in Computer Science, Vol. 5643), Ahmed Bouajjani and Oded Maler (Eds.). Springer, 306–320.
   https://doi.org/10.1007/978-3-642-02658-4_25
Rob Gerth, Doron A. Peled, Moshe Y. Vardi, and Pierre Wolper. 1995. Simple on-the-fly automatic verification of linear
   temporal logic. In PSTV (IFIP Conference Proceedings, Vol. 38). Chapman & Hall, 3–18. https://doi.org/10.1007/978-0-387-
   34892-6_1
Kurt Gödel. 1932. Ein Spezialfall des Entscheidungsproblems der theoretischen Logik. Ergebnisse eines mathematischen
   Kolloquiums 2 (1932), 27–28.
Aman Goel and Karem A. Sakallah. 2021a. On Symmetry and Quantification: A New Approach to Verify Distributed Protocols.
   In NFM (Lecture Notes in Computer Science, Vol. 12673). Springer, 131–150. https://doi.org/10.1007/978-3-030-76384-8_9
Aman Goel and Karem A. Sakallah. 2021b. Towards an Automatic Proof of Lamport’s Paxos. In FMCAD. IEEE, 112–122.
   https://doi.org/10.34727/2021/isbn.978-3-85448-046-4_20
Susanne Graf and Hassen Saïdi. 1997. Construction of Abstract State Graphs with PVS. In Computer Aided Verification, 9th
   International Conference, CAV ’97, Haifa, Israel, June 22-25, 1997, Proceedings (Lecture Notes in Computer Science, Vol. 1254),
   Orna Grumberg (Ed.). Springer, 72–83. https://doi.org/10.1007/3-540-63166-6_10
Yuri Gurevich. 1976. The decision problem for standard classes. The Journal of Symbolic Logic 41, 2 (1976), 460–464.
   https://doi.org/10.1017/S0022481200051513
Márton Hajdú, Petra Hozzová, Laura Kovács, and Andrei Voronkov. 2021. Induction with Recursive Definitions in Superpo-
   sition. In FMCAD. IEEE, 1–10. https://doi.org/10.34727/2021/isbn.978-3-85448-046-4_34
Travis Hance, Marijn Heule, Ruben Martins, and Bryan Parno. 2021. Finding Invariants of Distributed Systems: It’s a Small
   (Enough) World After All. In 18th USENIX Symposium on Networked Systems Design and Implementation, NSDI 2021,
   April 12-14, 2021, James Mickens and Renata Teixeira (Eds.). USENIX Association, 115–131. https://www.usenix.org/
   conference/nsdi21/presentation/hance
Matthias Horbach and Viorica Sofronie-Stokkermans. 2013. Obtaining Finite Local Theory Axiomatizations via Saturation.
   In Frontiers of Combining Systems - 9th International Symposium, FroCoS 2013, Nancy, France, September 18-20, 2013.
   Proceedings (Lecture Notes in Computer Science, Vol. 8152), Pascal Fontaine, Christophe Ringeissen, and Renate A. Schmidt
   (Eds.). Springer, 198–213. https://doi.org/10.1007/978-3-642-40885-4_14
Heidi Howard, Dahlia Malkhi, and Alexander Spiegelman. 2016. Flexible Paxos: Quorum Intersection Revisited. In 20th
   International Conference on Principles of Distributed Systems, OPODIS 2016, December 13-16, 2016, Madrid, Spain (LIPIcs,
   Vol. 70), Panagiota Fatourou, Ernesto Jiménez, and Fernando Pedone (Eds.). Schloss Dagstuhl - Leibniz-Zentrum für
   Informatik, 25:1–25:14. https://doi.org/10.4230/LIPIcs.OPODIS.2016.25
Petra Hozzová, Laura Kovács, and Andrei Voronkov. 2021. Integer Induction in Saturation. In CADE (Lecture Notes in
   Computer Science, Vol. 12699). Springer, 361–377. https://doi.org/10.1007/978-3-030-79876-5_21
Shachar Itzhaky, Anindya Banerjee, Neil Immerman, Ori Lahav, Aleksandar Nanevski, and Mooly Sagiv. 2014. Modular
   reasoning about heap paths via effectively propositional formulas. In The 41st Annual ACM SIGPLAN-SIGACT Symposium
   on Principles of Programming Languages, POPL ’14, San Diego, CA, USA, January 20-21, 2014, Suresh Jagannathan and
   Peter Sewell (Eds.). ACM, 385–396. https://doi.org/10.1145/2535838.2535854
Shachar Itzhaky, Anindya Banerjee, Neil Immerman, Aleksandar Nanevski, and Mooly Sagiv. 2013. Effectively-Propositional
   Reasoning about Reachability in Linked Data Structures. In CAV (Lecture Notes in Computer Science, Vol. 8044). Springer,
   756–772. https://doi.org/10.1007/978-3-642-39799-8_53
Swen Jacobs. 2009. Incremental Instance Generation in Local Reasoning. In CAV (Lecture Notes in Computer Science, Vol. 5643).
   Springer, 368–382. https://doi.org/10.1007/978-3-642-02658-4_29
Aleksandr Karbyshev, Nikolaj S. Bjørner, Shachar Itzhaky, Noam Rinetzky, and Sharon Shoham. 2017. Property-Directed
   Inference of Universal Invariants or Proving Their Absence. J. ACM 64, 1 (2017), 7:1–7:33. https://doi.org/10.1145/3022187
Matt Kaufmann, Panagiotis Manolios, and J Strother Moore. 2013. Computer-aided reasoning: ACL2 case studies. Vol. 4.
   Springer Science & Business Media. https://doi.org/10.1007/978-1-4757-3188-0
Matt Kaufmann and J. Strother Moore. 1997. An Industrial Strength Theorem Prover for a Logic Based on Common Lisp.
   IEEE Trans. Software Eng. 23, 4 (1997), 203–213. https://doi.org/10.1109/32.588534
Bakhadyr Khoussainov and Anil Nerode. 1994. Automatic Presentations of Structures. In Logical and Computational
   Complexity. Selected Papers. Logic and Computational Complexity, International Workshop LCC ’94, Indianapolis, Indiana,
   USA, 13-16 October 1994 (Lecture Notes in Computer Science, Vol. 960), Daniel Leivant (Ed.). Springer, 367–392. https:
   //doi.org/10.1007/3-540-60178-3_93



                                   Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:30                                                                          Neta Elad, Oded Padon, and Sharon Shoham


Bartek Klin and Michal Szynwelski. 2016. SMT Solving for Functional Programming over Infinite Structures. In MSFP
   (EPTCS, Vol. 207). 57–75. https://doi.org/10.4204/EPTCS.207.3
Jason R. Koenig, Oded Padon, Sharon Shoham, and Alex Aiken. 2022. Inferring Invariants with Quantifier Alternations:
   Taming the Search Space Explosion. In Tools and Algorithms for the Construction and Analysis of Systems - 28th International
   Conference, TACAS 2022, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2022,
   Munich, Germany, April 2-7, 2022, Proceedings, Part I (Lecture Notes in Computer Science, Vol. 13243), Dana Fisman and
   Grigore Rosu (Eds.). Springer, 338–356. https://doi.org/10.1007/978-3-030-99524-9_18
Leslie Lamport. 1998. The Part-Time Parliament. ACM Trans. Comput. Syst. 16, 2 (1998), 133–169. https://doi.org/10.1145/
   279227.279229
Leslie Lamport. 2019. The Paxos Algorithm - or How to Win a Turing Award. https://lamport.azurewebsites.net/tla/paxos-
   algorithm.html
K. Rustan M. Leino. 2012. Automating Induction with an SMT Solver. In VMCAI (Lecture Notes in Computer Science, Vol. 7148).
   Springer, 315–331. https://doi.org/10.1007/978-3-642-27940-9_21
Tal Lev-Ami and Shmuel Sagiv. 2000. TVLA: A System for Implementing Static Analyses. In SAS (Lecture Notes in Computer
   Science, Vol. 1824). Springer, 280–301. https://doi.org/10.1007/978-3-540-45099-3_15
Harry R. Lewis. 1980. Complexity Results for Classes of Quantificational Formulas. J. Comput. Syst. Sci. 21, 3 (1980), 317–353.
   https://doi.org/10.1016/0022-0000(80)90027-6
Martin Löb. 1967. Decidability of the monadic predicate calculus with unary function symbols. Journal of Symbolic Logic 32,
   4 (1967), 563.
Christof Löding, P. Madhusudan, and Lucas Peña. 2018. Foundations for natural proofs and quantifier instantiation. Proc.
   ACM Program. Lang. 2, POPL (2018), 10:1–10:30. https://doi.org/10.1145/3158098
Christopher Lynch. 2013. Constructing Bachmair-Ganzinger Models. In Programming Logics (Lecture Notes in Computer
   Science, Vol. 7797). Springer, 285–301. https://doi.org/10.1007/978-3-642-37651-1_12
Christopher Lynch and Stephen Miner. 2023. Complete Trigger Selection in Satisfiability Modulo First-Order Theories.
   In Proceedings of the 21st International Workshop on Satisfiability Modulo Theories (SMT 2023) co-located with the 29th
   International Conference on Automated Deduction (CADE 2023), Rome, Italy, July, 5-6, 2023 (CEUR Workshop Proceedings,
   Vol. 3429), Stéphane Graham-Lengrand and Mathias Preiner (Eds.). CEUR-WS.org, 18–32. https://doi.org/10.48550/arXiv.
   2306.09436
Haojun Ma, Aman Goel, Jean-Baptiste Jeannin, Manos Kapritsos, Baris Kasikci, and Karem A. Sakallah. 2019. I4: incremental
   inference of inductive invariants for verification of distributed protocols. In SOSP. ACM, 370–384. https://doi.org/10.
   1145/3341301.3359651
Umang Mathur, P. Madhusudan, and Mahesh Viswanathan. 2019. Decidable verification of uninterpreted programs. Proc.
   ACM Program. Lang. 3, POPL (2019), 46:1–46:29. https://doi.org/10.1145/3290359
Umang Mathur, P. Madhusudan, and Mahesh Viswanathan. 2020. What’s Decidable About Program Verification Modulo
   Axioms?. In TACAS (2) (Lecture Notes in Computer Science, Vol. 12079). Springer, 158–177. https://doi.org/10.1007/978-3-
   030-45237-7_10
Kenneth L. McMillan and Oded Padon. 2018. Deductive Verification in Decidable Fragments with Ivy. In SAS (Lecture Notes
   in Computer Science, Vol. 11002). Springer, 43–55. https://doi.org/10.1007/978-3-319-99725-4_4
Kenneth L. McMillan and Oded Padon. 2020. Ivy: A Multi-modal Verification Tool for Distributed Algorithms. In CAV (2)
   (Lecture Notes in Computer Science, Vol. 12225). Springer, 190–202. https://doi.org/10.1007/978-3-030-53291-8_12
Michael Mortimer. 1975. On languages with two variables. Mathematical Logic Quarterly 21, 1 (1975), 135–140. https:
   //doi.org/10.1002/malq.19750210118
Adithya Murali, Lucas Peña, Eion Blanchard, Christof Löding, and P. Madhusudan. 2022. Model-guided synthesis of
   inductive lemmas for FOL with least fixpoints. Proc. ACM Program. Lang. 6, OOPSLA2 (2022), 1873–1902. https:
   //doi.org/10.1145/3563354
Daniel Neider, Pranav Garg, P. Madhusudan, Shambwaditya Saha, and Daejun Park. 2018. Invariant Synthesis for Incomplete
   Verification Engines. In TACAS (1) (Lecture Notes in Computer Science, Vol. 10805). Springer, 232–250. https://doi.org/10.
   1007/978-3-319-89960-2_13
Oded Padon, Giuliano Losa, Mooly Sagiv, and Sharon Shoham. 2017. Paxos made EPR: decidable reasoning about distributed
   protocols. Proc. ACM Program. Lang. 1, OOPSLA (2017), 108:1–108:31. https://doi.org/10.1145/3140568
Oded Padon, Kenneth L. McMillan, Aurojit Panda, Mooly Sagiv, and Sharon Shoham. 2016. Ivy: safety verification by
   interactive generalization. In PLDI. ACM, 614–630. https://doi.org/10.1145/2908080.2908118
Oded Padon, James R. Wilcox, Jason R. Koenig, Kenneth L. McMillan, and Alex Aiken. 2022. Induction duality: primal-dual
   search for invariants. Proc. ACM Program. Lang. 6, POPL (2022), 1–29. https://doi.org/10.1145/3498712
Julian Parsert, Chad E. Brown, Mikolas Janota, and Cezary Kaliszyk. 2023. Experiments on Infinite Model Finding in SMT
   Solving. In LPAR 2023: Proceedings of 24th International Conference on Logic for Programming, Artificial Intelligence and
   Reasoning, Manizales, Colombia, 4-9th June 2023 (EPiC Series in Computing, Vol. 94), Ruzica Piskac and Andrei Voronkov


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                   33:31


   (Eds.). EasyChair, 317–328. https://doi.org/10.29007/slrm
Nicolas Peltier. 2003. Building Infinite Models for Equational Clause Sets: Constructing Non-Ambiguous Formulae. Log. J.
   IGPL 11, 1 (2003), 97–129. https://doi.org/10.1093/jigpal/11.1.97
Mathias Preiner, Aina Niemetz, and Armin Biere. 2017. Counterexample-Guided Model Synthesis. In TACAS (1) (Lecture
   Notes in Computer Science, Vol. 10205). 264–280. https://doi.org/10.1007/978-3-662-54577-5_15
Michael O Rabin. 1969. Decidability of second-order theories and automata on infinite trees. Transactions of the american
   Mathematical Society 141 (1969), 1–35. https://doi.org/10.2307/1995086
Frank P Ramsey. 1930. On a Problem of Formal Logic. Procedures of London Mathematical Society 30 (1930), 264–285.
   https://doi.org/10.1007/978-0-8176-4842-8_1
Giles Reger, Martin Suda, and Andrei Voronkov. 2016. Finding Finite Models in Multi-sorted First-Order Logic. In Theory
   and Applications of Satisfiability Testing - SAT 2016 - 19th International Conference, Bordeaux, France, July 5-8, 2016,
   Proceedings (Lecture Notes in Computer Science, Vol. 9710), Nadia Creignou and Daniel Le Berre (Eds.). Springer, 323–341.
   https://doi.org/10.1007/978-3-319-40970-2_20
Andrew Reynolds and Jasmin Christian Blanchette. 2017. A Decision Procedure for (Co)datatypes in SMT Solvers. J. Autom.
   Reason. 58, 3 (2017), 341–362. https://doi.org/10.1007/s10817-016-9372-6
Andrew Reynolds and Viktor Kuncak. 2015. Induction for SMT Solvers. In VMCAI (Lecture Notes in Computer Science,
   Vol. 8931). Springer, 80–98. https://doi.org/10.1007/978-3-662-46081-8_5
Andrew Reynolds, Cesare Tinelli, Amit Goel, and Sava Krstic. 2013a. Finite Model Finding in SMT. In CAV (Lecture Notes in
   Computer Science, Vol. 8044). Springer, 640–655. https://doi.org/10.5555/2958031.2958040
Andrew Reynolds, Cesare Tinelli, Amit Goel, Sava Krstic, Morgan Deters, and Clark W. Barrett. 2013b. Quantifier Instantiation
   Techniques for Finite Model Finding in SMT. In CADE (Lecture Notes in Computer Science, Vol. 7898). Springer, 377–391.
   https://doi.org/10.1007/978-3-642-38574-2_26
Alexandre Riazanov and Andrei Voronkov. 1999. Vampire. In CADE (Lecture Notes in Computer Science, Vol. 1632). Springer,
   292–296. https://doi.org/10.1007/3-540-48660-7_26
Kristin Y. Rozier and Moshe Y. Vardi. 2007. LTL Satisfiability Checking. In SPIN (Lecture Notes in Computer Science, Vol. 4595).
   Springer, 149–167. https://doi.org/10.1007/s10009-010-0140-3
Shmuel Sagiv, Thomas W. Reps, and Reinhard Wilhelm. 1999. Parametric Shape Analysis via 3-Valued Logic. In POPL. ACM,
   105–118. https://doi.org/10.1145/514188.514190
Johannes Schoisswohl and Laura Kovács. 2021. Automating Induction by Reflection. In LFMTP (EPTCS, Vol. 337). 39–54.
   https://doi.org/10.4204/EPTCS.337.4
Saharon Shelah. 1977. Decidability of a portion of the predicate calculus. Israel Journal of Mathematics 28, 1 (1977), 32–44.
   https://doi.org/10.1007/BF02759780
Marcelo Taube, Giuliano Losa, Kenneth L. McMillan, Oded Padon, Mooly Sagiv, Sharon Shoham, James R. Wilcox, and Doug
   Woos. 2018. Modularity for decidability of deductive verification with applications to distributed systems. In PLDI. ACM,
   662–677. https://doi.org/10.1145/3192366.3192414
Moshe Y. Vardi. 1995. An Automata-Theoretic Approach to Linear Temporal Logic. In Banff Higher Order Workshop (Lecture
   Notes in Computer Science, Vol. 1043). Springer, 238–266. https://doi.org/10.1007/3-540-60915-6_6
Niki Vazou, Anish Tondwalkar, Vikraman Choudhury, Ryan G. Scott, Ryan R. Newton, Philip Wadler, and Ranjit Jhala.
   2018. Refinement reflection: complete verification with SMT. Proc. ACM Program. Lang. 2, POPL (2018), 53:1–53:31.
   https://doi.org/10.1145/3158141
Marco Voigt. 2019. Decidable fragments of first-order logic and of first-order linear arithmetic with uninterpreted predicates.
   Ph. D. Dissertation. Saarland University, Saarbrücken, Germany.
Christoph Weidenbach, Dilyana Dimova, Arnaud Fietzke, Rohit Kumar, Martin Suda, and Patrick Wischnewski. 2009. SPASS
   Version 3.5. In CADE (Lecture Notes in Computer Science, Vol. 5663). Springer, 140–145. https://doi.org/10.1007/978-3-642-
   02959-2_10
Jianan Yao, Runzhou Tao, Ronghui Gu, and Jason Nieh. 2022. DuoAI: Fast, Automated Inference of Inductive Invariants for
   Verifying Distributed Protocols. In 16th USENIX Symposium on Operating Systems Design and Implementation, OSDI 2022,
   Carlsbad, CA, USA, July 11-13, 2022, Marcos K. Aguilera and Hakim Weatherspoon (Eds.). USENIX Association, 485–501.
   https://www.usenix.org/conference/osdi22/presentation/yao
Jianan Yao, Runzhou Tao, Ronghui Gu, Jason Nieh, Suman Jana, and Gabriel Ryan. 2021. DistAI: Data-Driven Automated
   Invariant Learning for Distributed Protocols. In OSDI. USENIX Association, 405–421.




                                  Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:32                                                                      Neta Elad, Oded Padon, and Sharon Shoham


A       PROOFS
Proofs for Symbolic Structures as Representations of Infinite Models (Sec. 4)
   Lemma A.1. Let 𝑆 be a symbolic structure, 𝑣 an explicit assignment, 𝑣 𝑆 its symbolization, and 𝑣 LIA the
residual assignment. Then for every term 𝑡 over Σ, if 𝑣¯ (𝑡) = ⟨𝑛, 𝑧⟩ ∈ D𝐶 , then 𝑣¯𝑆 (𝑡) = ⟨𝑛, 𝑠⟩ ∈ D 𝑆 ×TLIA
for some LIA term 𝑠 such that 𝑣¯LIA (𝑠) = 𝑧.
    Proof for Lemma A.1. Structural induction over 𝑡.                                                            □
    The following technical lemmas will be useful in the sequel:
    Lemma A.2. (𝑣 [(𝑛, 𝑧)/𝑥])𝑆 = 𝑣 𝑆 𝑛, 𝑥 LIA /𝑥 .
                                                

    Lemma A.3. (𝑣 [(𝑛, 𝑧)/𝑥]) LIA = 𝑣 LIA 𝑧/𝑥 LIA .
                                                

    Proofs. Trivial.                                                                                             □
    Proof for Thm. 4.7. Structural induction over 𝜑.                                                             □

Proof for Checking Satisfiability by Finding Symbolic Structures (Sec. 5)
    Proof for Thm. 5.4. Structural induction over 𝜑.                                                             □

Proofs for Decidability via Symbolic Structures (Sec. 6)
  Correctness of the construction. To prove Lemma 6.3, we prove the following lemmas. First, we
show that 𝑆 is well-defined. Since all bound formulas are degenerate, all associated terms of function
will always be in bounds. What is left to prove is that 𝑓 𝑆 is well-defined:
  Lemma A.4. For every node 𝑛, there exists some 𝑛 ′ such that 𝐸 (𝑛 ′ ) ∩ 𝑓 𝑀 (𝑒) | 𝑒 ∈ 𝐸 (𝑛) ≠ ∅.
                                                                             

Consequently, 𝑓 𝑆 is well-defined.
    Next, we show that elements of 𝑀 and explicit elements of 𝑆 satisfy the same atomic formulas:
  Lemma A.5. For every node 𝑛 ∈ D 𝑆 , element 𝑒 ∈ 𝐸 (𝑛), assignments 𝑣, 𝑣 ′ for 𝑀 and E (𝑆) respectively,
and atom 𝑎, we have that 𝑀, 𝑣 [𝑒/𝑥] |= 𝑎 iff E (𝑆), 𝑣 ′ [⟨𝑛, 𝑧⟩/𝑥] |= 𝑎 for every 𝑧 ∈ Z.
  Since formulas in OSC have only universal quantifiers, Lemma A.5 implies that 𝑀 and E (𝑆) are
OSC-equivalent. Finally, we show that ≺ E (𝑆 ) is a strict total order:
    Lemma A.6. If 𝑀 |= 𝐴 ≺ then E (𝑆) |= 𝐴 ≺ .
                                                                    
    Proof for Lemma A.4. Trivial, since this holds for any 𝜏 𝑓 𝑀 (𝑒) where 𝑒 ∈ 𝐸 (𝑛).                            □
    For proving Lemma A.5, we first prove the following:
 Lemma A.7. For any node 𝑛, for any element atom 𝑎, if 𝑛 is marked by 𝑎[𝑓 (𝑥)/𝑥], then 𝑓 𝑆 (𝑛) is
marked by 𝑎.
  Proof. Let 𝑓 𝑆 (𝑛) = ⟨𝑛 ′, 𝑡⟩. Let 𝑎 be some element atom such that 𝑛 is marked by 𝑎[𝑓 (𝑥)/𝑥].
Let 𝑒 ∈ 𝐸 (𝑛) be an element such that 𝑓 𝑀 (𝑒) ∈ 𝐸 (𝑛 ′ ) By definition, 𝑀, 𝑣 [𝑒/𝑥] |= 𝑎[𝑓 (𝑥)/𝑥], or
equivalently, 𝑀, 𝑣 [𝑓 𝑀 (𝑒)/𝑥] |= 𝑎. Since element atoms agree for all class elements of a node, 𝑛 ′ is
marked by 𝑎.                                                                                         □
  Lemma A.8. For any node 𝑛, for any relation element atom 𝑎, if 𝑛 is marked by 𝑎, then for any
assignment 𝑣, for any 𝑖 ∈ Z, E (𝑆), 𝑣 [⟨𝑛, 𝑖⟩/𝑥] |= 𝑎.
    Proof. Trivial.                                                                                              □

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                           33:33


  Corollary A.9. For any relation element atom 𝑎, if 𝑛 is marked by 𝑎[𝑓 (𝑥)/𝑥], then for any
assignment 𝑣, for any 𝑖 ∈ Z, E (𝑆), 𝑣 [⟨𝑛, 𝑖⟩/𝑥] |= 𝑎[𝑓 (𝑥)/𝑥].
  Lemma A.10. Note that for any element 𝑒 in 𝑀, by definition of the partitions, 𝜏 (𝑒) is marked by
an atom 𝑎 iff 𝑒 satisfies that atom.
    Proof. By definition of the partitions.                                                                           □
                                                                                                 
   Lemma A.11. For any constant 𝑐, for any element atom 𝑎, 𝑀 |= 𝑎[𝑐/𝑥] iff 𝜏 𝑐 is marked by 𝑙 iff
                                                                                               𝑀

E (𝑆) |= 𝑎[𝑐/𝑥].
                                        
   Proof. Let 𝑛 = 𝜏 𝑐 𝑀 , then 𝐸 (𝑛) = 𝑐 𝑀 . 𝑀 |= 𝑎[𝑐/𝑥] ⇐⇒ for any assignment 𝑣, 𝑀, 𝑣 [𝑐 𝑀 /𝑥] |=
𝑎. If 𝑀, 𝑣 [𝑐 𝑀 /𝑥] |= 𝑎, then 𝑛 is marked by 𝑎.                                                □
  Lemma A.12. Let 𝑆 = {𝑥 } ∪ {ℎ(𝑥) | ℎ is a unary function symbol} be the set of mixed-atom terms.
For any node 𝑛 and terms 𝑡, 𝑡 ′ ∈ 𝑆 if 𝑛 is marked by 𝑎 = 𝑡 ⊲⊳ 𝑡 ′ , for some ⊲⊳ ∈ {≺, ≈, ≻}, then for any
assignment 𝑣, for any 𝑖 ∈ Z, E (𝑆), 𝑣 [(𝑛, 𝑖)/𝑥] |= 𝑎.
  Proof. Let us denote the interpretation of the terms 𝑡, 𝑡 ′ for 𝑥 ↦→ ⟨𝑛, 𝑖⟩: ⟨𝑚, 𝑗⟩ = [𝑥 ↦→ ⟨𝑛, 𝑖⟩] (𝑡),
⟨𝑚 ′, 𝑗 ′ ⟩ = [𝑥 ↦→ ⟨𝑛, 𝑖⟩] (𝑡 ′ ).
   In case either 𝑚 or 𝑚 ′ is a regular node. We consider the case for 𝑚 (and the case for 𝑚 ′ is
symmetrical). Since 𝑚 is a regular node, then 𝑗 = 0 (from Eq. (F -1)) and there exists a ground term
𝑔 such that 𝑚 is labeled by 𝑥 ≈ 𝑔 and 𝑔 E (𝑆 ) = ⟨𝑚, 0⟩.
   Necessarily, 𝑛 is marked by 𝑔 ⊲⊳ 𝑡 ′ , and from Lemma A.7 we get that 𝑚 ′ is marked with 𝑔 ⊲⊳ 𝑥.
From Def. (O-1), ⟨𝑚, 0⟩ ⊲⊳ E (𝑆 ) ⟨𝑚 ′, 𝑗 ′ ⟩, and therefore E (𝑆), 𝑣 [(𝑛, 𝑖)/𝑥] |= 𝑎.
    In case both 𝑚 and 𝑚 ′ are summary nodes. Let us denote by ⊲⊳LIA ∈ {<, =, >} the comparison
symbol that matches ⊲⊳. Since 𝑚, 𝑚 ′ are summary nodes, according to Eq. (F -2), 𝑗 = 𝑖 + 𝑘, 𝑗 ′ = 𝑖 + 𝑘 ′
then, since 𝜇 is defined according to the atoms of 𝑛 (𝑎 among them), 𝑘 ⊲⊳LIA 𝑘 ′ (and therefore
𝑗 ⊲⊳LIA 𝑗 ′ ).
    If there exists no ground term 𝑔 such that 𝑚 is marked by 𝑥 ≺ 𝑔 and 𝑚 ′ by 𝑥 ≻ 𝑔 or vice versa
(i.e., 𝑚 and 𝑚 ′ are in the same segment), then according to Def. (O-3), ⟨𝑚, 𝑗⟩ ⊲⊳ E (𝑆 ) ⟨𝑚 ′, 𝑗 ′ ⟩.
    Otherwise, there exists a ground term 𝑔 as above, and let us assume w.l.o.g. that 𝑚 is marked by
𝑥 ≺ 𝑔 and 𝑚 ′ by 𝑥 ≻ 𝑔, thus (from Lemma A.10) ⟨𝑚, 𝑗⟩ ≺ E (𝑆 ) 𝑔 E (𝑆 ) ≺ E (𝑆 ) ⟨𝑚 ′, 𝑗 ′ ⟩. 𝑛 is necessarily
marked with the atoms 𝑡 ≺ 𝑔 and 𝑡 ′ ≺ 𝑔, which must agree with 𝑎 (since ≺ is strict total order in
the original model 𝑀), E (𝑆), 𝑣 [(𝑛, 𝑖)/𝑥] |= 𝑎.                                                            □
    Proof for Lemma A.5. Follows from Lemmas A.7, A.8 and A.10 to A.12 and corollary A.9.                             □
  Proof for Lemma A.6. Follows from Def. (O-1) to (O-3) and strict total order properties of
≺𝑀 .                                                                                      □

B    EXAMPLES
Example for Symbolic Structures as Representations of Infinite Models (Sec. 4):
Half-space Summary Nodes
   Example B.1. Unbounded summary nodes, i.e., summary nodes whose bound formula is ⊤ that
represent a full copy of Z, are not always sufficient in order to represent satisfying models of formula.
As an example where a strict subset of Z is needed, consider the vocabulary Σ = {𝑐, 𝑓 (·), ≺}, and
the formula 𝜑 = 𝐴 ≺ ∧ ∀𝑥 . 𝑐 ≼ 𝑥 ∧ 𝑥 ≺ 𝑓 (𝑥) ∧ ∀𝑦. 𝑥 ≺ 𝑦 → 𝑓 (𝑥) ≼ 𝑦 where 𝑡 1 ≼ 𝑡 2 is a shorthand
for 𝑡 1 ≺ 𝑡 2 ∨ 𝑡 1 ≈ 𝑡 2 . The only model of 𝜑 is infinite, hence there must be at least one summary node
𝑛. Assuming that 𝑐 is interpreted as a regular node, and the interpretation of 𝑓 (𝑐) is some element

                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:34                                                                                                     Neta Elad, Oded Padon, and Sharon Shoham



                                                                                                          ⟨𝑆 4, 0⟩         ⟨𝑆 4, 1⟩
                                                       ⟨𝑆 2, 0⟩    ⟨𝑆 2, 1⟩
 ...       ⟨𝑆 1, 0⟩   ⟨𝑆 1, 1⟩   ...   ⟨𝑮1, 0⟩ . . .                                ...   ⟨𝑮2, 0⟩ . . .         ⟨𝑆 5, 0⟩         ⟨𝑆 5, 1⟩            ...   ⟨𝑮3 , 0⟩   ⟨𝑮4 , 0⟩
                                                             ⟨𝑆 3, 0⟩    ⟨𝑆 3, 1⟩
                                                                                                                      ⟨𝑆 6, 0⟩            ⟨𝑆 6, 1⟩



Fig. 7. Explication of a symbolic structure constructed as in Sec. 6.1. Each circle depicts an element. The
labels 𝑆𝑖 , 𝐺𝑖 denote different sets of atoms which correspond to different nodes in the symbolic structure. I.e.,
each 𝑆𝑖 and 𝐺 𝑗 is a unique set of element atoms (D-1), image atoms (D-2), and mixed atoms (D-3). The sets
𝐺 1, 𝐺 2, . . . include at least one atom of the form 𝑥 ≈ 𝑔, where 𝑔 is some ground term, thus refer to regular
nodes. The sets 𝑆 1, 𝑆 2, . . . do not include any atom of the form 𝑥 ≈ 𝑔, thus refer to summary nodes. The
arrows between the elements depict ≺ E (𝑆 ) by denoting immediate successors. Note that the order between
the explicit elements of, for example, 𝑆 4, 𝑆 5 and 𝑆 6 follows a fixed pattern.


(𝑛, 𝑧) of 𝑛, then 𝑧 has to be the minimal element in the subset associated with 𝑛, otherwise, we
could always find an element between 𝑐 and 𝑓 (𝑐). Therefore, in this example, 𝑛 must be bounded
by 𝑥 ≥ 𝑧. (Adding a regular node for 𝑓 (𝑐) does not solve the problem, only shifts it.)

Example for the Order Construction of Decidability via Symbolic Structures (Sec. 6)
An illustration of the interpretation of ≺, as defined in (O-1) to (O-3), is shown in Fig. 7. The
elements of 𝑆 2 are all greater than the elements 𝑆 1 , which means, according to (O-2), that there
exists some ground term 𝑔 such that 𝑥 ≺ 𝑔 ∈ 𝑆 1 and 𝑥 ≻ 𝑔 ∈ 𝑆 2 (and 𝑥 ≈ 𝑔 ∈ 𝐺 1 , which delimits
the two segments). The order of the elements of 𝑆 4, 𝑆 5 and 𝑆 6 indicates, according to (O-3), that
𝑆 4 ≪ 𝑆 5 ≪ 𝑆 6 , arbitrarily.

C    EVALUATION DETAILS
    Echo Machine. Defining
 prev_echoed [ T, V ] = prev ( T ) ≺ T ∧ echo ( prev ( T ), V )
        echo_start [ V ] = ∀ V′ .¬echo ( start, V′ )
                                                                  

                          ∧ ∀ T′ , V′ .echo′ ( T′ , V′ ) ↔ T′ ≈ start ∧ V′ ≈ V ∨ T′ 0 start ∧ V′ 0 V ∧ echo ( T′ , V′ )
                                                                                                                       

       echo_prev [ T, V ] = ∀ V′ .¬echo ( T, V′ ) ∧ prev_echoed [ T, V ]
                                                    

                          ∧ ∀ T′ , V′ .echo′ ( T′ , V′ ) ↔ T′ ≈ T ∧ V′ ≈ V ∨ T′ 0 T ∧ V′ 0 V ∧ echo ( T′ , V′ )
                                                                                                               

           transition = ∃ T, V.echo_start [ V ] ∨ echo_prev [ T, V ]
              safety = ∀ T, T′ , V, V′ . echo ( T, V ) ∧ echo ( T′ , V′ ) → V ≈ V′
                                                                                          

       aux_invariant = ∀ T, Vecho ( T, V ) → T ≈ start ∨ prev_echoed [ T, V ],
the formula we check is
                                 𝐴 ≺ ∧ safety ∧ aux_invariant ∧ transition ∧ ¬safety′ .
The symbolic model found by FEST is depicted in Fig. 2b.
    Ring Leader. Defining
                  safety = (∃ N.leader ( N ) ) ∨ (∃ N.¬sent (𝑁 ) ) ∨ ∃ N, N′ .pending ( N, N′ )
                                                                                                                                      

           aux_invariant = ∀ N.( sent ( N ) ∧ ¬leader ( N ) ) → ( pending ( N, target ( N ) ) ∨ N ≺ target ( N ) ),
where target is a Skolem function, the formula we check is
                                                  𝐴 ≺ ∧ aux_invariant ∧ ¬safety.
The symbolic model found by FEST is depicted in Fig. 8

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                     33:35

                                                                                 𝛼

                                              target : 𝑥 1 + 1                           ≺: 𝑥 1 < 𝑥 2

                                                                        𝑥 ≥0


Fig. 8. The symbolic model found by FEST for the Ring Leader example. The formulas for the relations are
sent(𝛼) = ⊤, leader(𝛼) = ⊥, and pending(𝛼, 𝛼) = ⊥.



                               ≺: 𝑥 1 < 𝑥 2                           next : 𝑥 1 + 1          nil         next : 0
                                                                             ≺
                                                     𝑥 ≥0


Fig. 9. The symbolic model found by FEST for the Sorted List example. For all nodes, the formula for sorted
is ⊤.



                                                                      lseg
                                          𝛼

                        lseg                         next : 𝑥 1 − 1                    lseg         nil          next : 0

                                    𝑥 ≤0                              lseg




Fig. 10. The symbolic model found by FEST for the List Segment example. The list formulas are list(nil) =
⊤ and list(𝛼) = ⊥.



   Sorted List. Defining
                linked_list = ∀ N.( N ≈ nil )↔( next ( N ) ≈ N )
                 sorted_def = ∀ N.sorted ( N )↔( N ≈ nil ∨ ( sorted ( next ( N ) ) ∧ next ( N ) ≺ N ) )
                   property = ∀ N.sorted ( N ) → nil ≼ N,

the formula we check is

                                𝐴 ≺ ∧ linked_list ∧ sorted_def ∧ ¬property.

The symbolic model found by FEST is depicted in Fig. 9.
   List Segment. Defining
                            nil_def = ( N ≈ nil )↔( next ( N ) ≈ N )
                           list_def = ∀ N.list ( N )↔( N ≈ nil ∨ list ( next ( N ) ) )
                           lseg_def = ∀ N, N′ .lseg ( N, N′ )↔ N ≈ N′ ∨ lseg next ( N ), N′
                                                                                                                     

                           property = ∀ N, N′ . lseg ( N, N′ ) ∧ list ( N′ ) → list ( N ),
                                                                            


the formula we check is

                                 nil_def ∧ list_def ∧ lseg_def ∧ ¬property.

The symbolic model found by FEST is depicted in Fig. 10.

                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:36                                                                               Neta Elad, Oded Padon, and Sharon Shoham
                           𝑠 : 𝑥1 + 1          𝑠 : 𝑥1 + 1
                                                                         +       zero               𝛼                    𝛽
                                    𝛼                   𝛽           zero     ⟨ zero, 0⟩          ⟨𝛼, 𝑥 2 ⟩            ⟨𝛽, 𝑥 2 ⟩
                   𝑠:0
         zero                                                           𝛼      ⟨𝛼, 𝑥 1 ⟩    ⟨𝛼, 𝑥 1 + 𝑥 2 + 1⟩     ⟨𝛽, 𝑥 1 + 𝑥 2 ⟩
                                                                        𝛽      ⟨𝛽, 𝑥 1 ⟩    ⟨𝛽, 𝑥 1 + 𝑥 2 + 1⟩   ⟨𝛼, 𝑥 1 + 𝑥 2 + 1⟩
                            𝑥 ≥0                𝑥 ≥0

                Fig. 11. Non-commutative addition. Note the difference between the highlighted cells.


    Axiomatic Presburger Arithmetic. Defining
                                                        𝐴1 = ∀𝑥 .𝑠 (𝑥 ) 0 zero
                                                        𝐴2 = ∀𝑥, 𝑦.𝑠 (𝑥 ) ≈ 𝑠 (𝑦) → 𝑥 ≈ 𝑦
                                                        𝐴3 = ∀𝑥 .𝑥 + zero ≈ 𝑥
                                                        𝐴4 = ∀𝑥, 𝑦.𝑥 + 𝑠 (𝑦) ≈ 𝑠 (𝑥 + 𝑦)
                         inductive_commutativity = ∀𝑥, 𝑦.(𝑥 + 𝑦 ≈ 𝑦 + 𝑥 ) → (𝑥 + 𝑠 (𝑦) ≈ 𝑠 (𝑦) + 𝑥 ),

the formula we check is

                                        𝐴1 ∧ 𝐴2 ∧ 𝐴3 ∧ 𝐴4 ∧ ¬inductive_commutativity.

The symbolic model found by FEST has 3 regular nodes and 1 summary node, and the different
regular nodes all behave as neutral elements (i.e., for all them it holds that ∀𝑥 .𝑥 + 𝑒 ≈ 𝑥 ). We refine
our modeling with the additional axiom

                                               𝐴5 = ∀𝑥, 𝑦.𝑥 + 𝑦 ≈ 𝑥 → 𝑦 ≈ zero.

This eliminates the three different “zeros” and instead FEST finds a symbolic model where there
are two summary nodes, representing a nonstandard model of arithmetic where there two parallel
“number lines”. See Fig. 11. This infinite model can be eliminated, by adding the lemma

                                                𝐴6 = ∀𝑥, 𝑦.𝑠 (𝑥) + 𝑦 ≈ 𝑠 (𝑥 + 𝑦),

which makes the formula unsatisfiable, proving the commutativity of addition.

D       TECHNICAL CONSTRUCTION FOR FINDING SYMBOLIC STRUCTURES
In this section, we fill out the technical details of the finding symbolic structures algorithm, presented
in Sec. 5.
   Recall that the model checking encoding of 𝜑 (over vocabulary Σ) w.r.t. a symbolic structure 𝑆 and
an explicit assignment 𝑣 : X → D E (𝑆 ) is defined w.r.t. to a symbolic assignment 𝑣 𝑆 : X → D × X LIA
obtained by the symbolization of 𝑣 (see Def. 4.6). In the model finding setting, an explicit assignment
is not given, but needs to be found together with the symbolic structurein 𝑆 ♯ . Each symbolic
assignment 𝑣 𝑆 is therefore used as a symbolic representation of all the explicit assignments whose
symbolization is 𝑣 𝑆 . Note that the domain of 𝑆 ♯ is fully specified, thus a symbolic assignment is
well-defined w.r.t. 𝑆 ♯ .
   In the model checking encoding, a symbolic assignment 𝑣 𝑆 is extended to any term over Σ
based on a specific symbolic structure 𝑆. Similarly, the model finding encoding extends a symbolic
assignment 𝑣 𝑆 according to a symbolic-structure template 𝑆 ♯ to any term 𝑡 over Σ via 𝑣 𝑆,𝑆 ♯ , which
reflects the possible interpretations of 𝑡 in any symbolic structure in 𝑆 ♯ . Formally, 𝑣𝑇 ,𝑆 ♯ : T →
P (Prop × D × TLIA ), is defined below, where Prop denotes the set of all propositional formulas
over the auxiliary Boolean variables, and the triple (𝑝, 𝑛, 𝑠) ∈ 𝑣𝑇 ,𝑆 ♯ (𝑡) is understood as “when 𝑝 is
true, it induces the interpretation ⟨𝑛, 𝑠⟩ for 𝑡”.

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
An Infinite Needle in a Finite Haystack                                                                                                   33:37


                                                                                                       !
         ♯
                                                  Û                        Û                                           h                     i
 transF𝑆𝑣𝑆 (𝑅(𝑡 1, . . . , 𝑡𝑘 )) =                                              𝑝𝑖 ∧ 𝑏 𝑅 (𝑛1,...,𝑛𝑘 ) : 𝜑 → 𝜑 [𝑠𝑖 /𝑥𝑖 ] 𝑑𝑅𝑗 (𝑛1,...,𝑛 ) /𝑑 𝑗
                                                                                                                                     𝑘
                                      (𝑝𝑖 , 𝑛𝑖 , 𝑠𝑖 ) ∈ 𝑣       (𝑡𝑖 ),      𝑖
                                                       𝑇 ,𝑆 ♯
                                              𝜑 ∈ I ♯ (𝑅)
                                                  Û
                                                                         (𝑝 ∧ 𝑝 ′ ) → eq (𝑛, 𝑠, 𝑛 ′, 𝑠 ′ )
                  ♯
         transF𝑆𝑣𝑆 (𝑡 1 ≈ 𝑡 2 ) =
                                       (𝑝, 𝑛, 𝑠 ) ∈ 𝑣 ♯ (𝑡 1 ),
                                                          𝑇 ,𝑆
                                      (𝑝 ′ , 𝑛 ′ , 𝑠 ′ ) ∈ 𝑣 ♯ (𝑡 2 )
                                                         𝑇 ,𝑆


                                                                                                   ⊥
                                                                                                  
                                                                                                  
                                                                                                                      if 𝑛 ≠ 𝑛 ′
                                                                                              ′   ′
                                                                         where eq (𝑛, 𝑠, 𝑛 , 𝑠 ) = ⊤                   if 𝑛 = 𝑛 ′ ∈ D 𝑅
                                                                                                   𝑠 ≈ 𝑠′
                                                                                                  
                                                                                                                       otherwise
                                                                                                
                     ♯                  ♯
             transF𝑆𝑣𝑆 (¬𝜑) = ¬ transF𝑆𝑣 ♯ (𝜑)
                                                      𝑇 ,𝑆
                  ♯                    ♯               ♯
          transF𝑆𝑣𝑆 (𝜑 ◦ 𝜓 ) = transF𝑆𝑣𝑆 (𝜑) ◦ transF𝑆𝑣𝑆 (𝜓 )
                      ♯
                                                 Û                         h       i           ♯
                                                                                                         
           transF𝑆𝑣𝑆 (∀𝑥 .𝜑) = ∀𝑥 LIA .                      B ♯ (𝑛) 𝑥 LIA /𝑥 𝑑𝑛𝑗 /𝑑 𝑗 → transF𝑆𝑣    (𝜑)
                                                                                  𝑆 [⟨𝑛,𝑥
                                                                                          LIA ⟩ /𝑥 ]
                                       𝑛∈ D
                  ♯
                                        Ü                    h      i          ♯
                                                                                                        
          transF𝑆𝑣𝑆 (∃𝑥 .𝜑) = ∃𝑥 LIA .        B ♯ (𝑛) 𝑥 LIA /𝑥 𝑑𝑛𝑗 /𝑑 𝑗 ∧ transF𝑆𝑣 𝑛,𝑥 LIA /𝑥 (𝜑)
                                                                                  𝑆 [⟨       ⟩ ]
                                                𝑛∈ D𝒔



                      Fig. 12. Parameteric transformation by symbolic-structure template 𝑆 ♯ .




                 𝑣𝑇 ,𝑆 ♯ (𝑥) = {(⊤, 𝑛, 𝑠)} where 𝑣 𝑆 (𝑥) = 𝑛, 𝑥 LIA and 𝑠 = 𝑥 LIA if 𝑛 ∈ D 𝑆 , 𝑠 = 0 otherwise
                                 
                 𝑣𝑇 ,𝑆 ♯ (𝑐) = (𝑏𝑐→𝑛 , 𝑛, 0) | 𝑛 ∈ D 𝑅
                                 ( Ó                                                           h                         i )
                                     𝑘                                                              𝑗
                                         𝑝 𝑖  ∧  𝑏  𝑓 (𝑛 1 ,...,𝑛   )→⟨𝑛,𝑠 ⟩ , 𝑛, 𝑠 [𝑠 𝑖 /𝑥 𝑖 ]  𝑑  𝑓 (𝑛 1 ,...,𝑛𝑘 )
                                                                                                                     /𝑑 𝑗   |
𝑣𝑇 ,𝑆 ♯ (𝑓 (𝑡 1, . . . , 𝑡𝑘 )) =     𝑖=1                          𝑘

                                        (𝑝𝑖 , 𝑛𝑖 , 𝑠𝑖 ) ∈ 𝑣𝑇 ,𝑆 ♯ (𝑡𝑖 ), 𝑛 ∈ D, 𝑠 ∈ I (𝑓 )        ♯


   Therefore, for each term 𝑡 over Σ, 𝑣𝑇 ,𝑆 ♯ defines the potential set of interpretations 𝑣ˆ𝑆 (𝑡) of 𝑡 in
symbolic structures represented by 𝑆 ♯ , where each interpretation is “guarded” by the assignment
to the auxiliary Boolean variables under which it is obtained.
   To capture satisfaction of 𝜑 in a symbolic structure in 𝑆 ♯ defined by some assignment to the aux-
iliary variables w.r.t. some explicit assignment represented by the symbolic assignmentt 𝑣 𝑆 we use
                             ♯
the transformation transF𝑆𝑣𝑆 (𝜑), defined in Fig. 12. The difference compared to the transformation
transF𝑇𝑣𝑆 (𝜑) used for model checking is in the transformation of atomic formulas, which for every
term 𝑡 over Σ considers the set of interpretations in 𝑣𝑇 ,𝑆 ♯ (𝑡), as opposed to 𝑣ˆ𝑆 (𝑡), and in the use of
the parametric bound formulas.

   Example D.1. Let us consider an example where the vocabulary has a single sort, a single        unary
function next, and a single binary relation symbol ≺, and a consider a template 𝑆 = D, B , I ♯ ,
                                                                                      ♯             ♯

whose domain includes two summary nodes D = {𝑛1, 𝑛 2 }, there are only degenerate bound formulas
B ♯ = {⊤}, and the interpretations are I ♯ ( next) = 0, 𝑥 1 + 𝑑 , and I (≺) = {⊤, ⊥, 𝑥 1 ≤ 𝑥 2, 𝑥 1 < 𝑥 2 }.
Let 𝑣 𝑆 be a symbolic assignment where 𝑣 𝑆 (𝑥) = ⟨𝑛 1, 𝑥 LIA ⟩. Then the parametrically transformed

                                     Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
33:38                                                                         Neta Elad, Oded Padon, and Sharon Shoham


formula for 𝑥 ≺ next (𝑥) is the conjunction of the following:
                 ..
                
                
                
                  .                                              
                      𝑏 next (𝑛1 )→⟨𝑛2,0⟩ ∧ 𝑏 ≺ (𝑛1,𝑛2 ) : ⊤  → ⊤
                
                
                
                
                      𝑏 next (𝑛1 )→⟨𝑛2,0⟩ ∧ 𝑏 ≺ (𝑛1,𝑛2 ) : ⊥  → ⊥
                
                
                
                                                                        LIA
                 𝑏 next (𝑛1 )→⟨𝑛2,0⟩ ∧ 𝑏 ≺ (𝑛1,𝑛2 ) : <  → 𝑥 LIA < 0
                
                
                
                
                      𝑏 next (𝑛1 )→⟨𝑛2,0⟩ ∧ 𝑏 ≺ (𝑛1,𝑛2 ) : ≤ → 𝑥 ≤ 0
                
                
                  ..
                
                
                   .                                                 
                
                                                                             LIA
                                                  ∧   ≺ (𝑛 1 ,𝑛 2 ) : < → 𝑥      < 𝑥 LIA + 𝑑 next (𝑛 )
                
                
                     𝑏 next (𝑛1 )→ ⟨𝑛2 ,𝑥 1 +𝑑 ⟩   𝑏
                
                                                                                                   1
                
                   .
                
                 . .
                
  Finally, to state that 𝜑 is satisfied by a symbolic structure in 𝑆 ♯ induced by the auxiliary variables
under some explicit assignment represented by some symbolic assignment, we define
                                               Ü                   ♯
                                        𝜑𝑆 ♯ =      𝑏 𝑣𝑆 ∧ transF𝑆𝑣𝑆 ,
                                                          𝜑
                                                     𝑣𝑆 ∈𝑉 ♯
                                                          𝑆
          𝜑
where 𝑉𝑆 ♯ denotes the set of different symbolic assignments to the free variables of 𝜑 in 𝑆 ♯ (where
a fixed arbitrary assignment is chosen to the remaining variables), and 𝑏 𝑣𝑆 is an auxiliary Boolean
variable, representing the choice of 𝑣 𝑆 . This set is finite as each symbolic assignment corresponds
                                         𝜑
to a node assignment. If 𝜑 is closed, 𝑉𝑆 ♯ consists of a single (arbitrary) symbolic assignment.

  Theorem 5.4. Given a formula 𝜑 over Σ and a symbolic-structure template 𝑆 ♯ , there exists a
symbolic structure 𝑆 in 𝑆 ♯ and an explicit assignment 𝑣 for E (𝑆) such that E (𝑆), 𝑣 |= 𝜑 iff there exists
an assignment 𝑣 ′ such that 𝑣 ′ |=LIA 𝜑𝑆 ♯ ∧ 𝜑 aux . Furthermore, we can efficiently extract 𝑆 and 𝑣 from 𝑣 ′ .
   Proof. Similarly to the proofs for Lemma A.1 and Thm. 4.7                                                        □

Received 2023-07-11; accepted 2023-11-07




Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 33. Publication date: January 2024.
