                                                       An Abstract Contract Theory for
                                                          Programs with Procedures
arXiv:2101.06087v2 [cs.LO] 11 Jun 2021




                                                               Full Version∗
                                                             Christian Lidström and Dilian Gurov
                                                 KTH Royal Institute of Technology, Stockholm, Sweden

                                                                              June 14, 2021


                                                                                  Abstract
                                                   When developing complex software and systems, contracts provide
                                               a means for controlling the complexity by dividing the responsibilities
                                               among the components of the system in a hierarchical fashion. In spe-
                                               cific application areas, dedicated contract theories formalise the notion
                                               of contract and the operations on contracts in a manner that supports
                                               best the development of systems in that area. At the other end, con-
                                               tract meta-theories attempt to provide a systematic view on the vari-
                                               ous contract theories by axiomatising their desired properties. However,
                                               there exists a noticeable gap between the most well-known contract meta-
                                               theory of Benveniste et al. [5], which focuses on the design of embedded
                                               and cyber-physical systems, and the established way of using contracts
                                               when developing general software, following Meyer’s design-by-contract
                                               methodology [18]. At the core of this gap appears to be the notion of pro-
                                               cedure: while it is a central unit of composition in software development,
                                               the meta-theory does not suggest an obvious way of treating procedures
                                               as components.
                                                      In this paper, we provide a first step towards a contract theory that
                                               takes procedures as the basic building block, and is at the same time an
                                               instantiation of the meta-theory. To this end, we propose an abstract con-
                                               tract theory for sequential programming languages with procedures, based
                                               on denotational semantics. We show that, on the one hand, the specifica-
                                               tion of contracts of procedures in Hoare logic, and their procedure-modular
                                               verification, can be cast naturally in the framework of our abstract con-
                                               tract theory. On the other hand, we also show our contract theory to fulfil
                                               the axioms of the meta-theory. In this way, we give further evidence for
                                            ∗ This is the full version of the paper An Abstract Contract Theory for Programs with Pro-

                                         cedures [17], published in Proceedings of the 24th International Conference on Fundamental
                                         Approaches to Software Engineering (FASE 2021), which includes the proofs of all theorems
                                         and additional examples. The conference version should always be cited.


                                                                                      1
      the utility of the meta-theory, and prepare the ground for combining our
      instantiation with other, already existing instantiations.


1    Introduction
Contracts. Loosely speaking, a contract for a software or system component
is a means of specifying that the component obliges itself to guarantee a certain
behaviour or result, provided that the user (or client) of the component obliges
itself to fulﬁl certain constraints on how it interacts with the component.
    One of the earliest inspirations for the notion of software contracts came
from the works of Floyd [10] and Hoare [15]. One outcome of this was Hoare
logic, which is a way of assigning meaning to sequential programs axiomati-
cally, through so-called Hoare triples. A Hoare triple {P }S{Q} consists of two
assertions P and Q over the program variables, called the pre-condition and
post-condition, respectively, and a program S. The triple states that if the
pre-condition P holds prior to executing S, then, if execution of S terminates,
the post-condition Q will hold upon termination. With the help of additional,
so-called logical variables, one can specify, with a Hoare triple, the desired rela-
tionship between the ﬁnal values of certain variables (such as the return value of
a procedure) and the initial values of certain other variables (such as the formal
parameters of the procedure).
    This style of specifying contracts has been advocated by Meyer [18], together
with the design methodology Design-by-Contract. A central characteristic of
this methodology is that it is well-suited for independent implementation and
verification, where software components are developed independently from each
other, based solely on the contracts, and without any knowledge of the imple-
mentation details of the other components.

Contract Theories. Since then, many other contract theories have emerged,
such as Rely/Guarantee reasoning [16, 22] and a number of Assume/Guaran-
tee contract theories [4, 6]. A contract theory typically formalises the notion
of contract, and develops a number of operations on contracts that support
typical design steps. This in turn has lead to a few developments of contract
meta-theories (e.g. [5, 2, 8]), which aim at unifying these, in many cases in-
compatible, contract theories. The most comprehensive, and well-known, of
these, is presented in Benveniste et al. [5], and is concerned speciﬁcally with the
design of cyber-physical systems. Here, all properties are derived from a most
abstract notion of a contract. The meta-theory focuses on the notion of contract
refinement, and the operations of contract conjunction and composition. The
intention behind reﬁnement and composition is to support a top-down design
ﬂow, where contracts are decomposed iteratively into sub-contracts; the task
is then to show that the composition of the sub-contracts reﬁnes the original
contract. These operations are meant to enable independent development and
reuse of components. In addition, the operation of conjunction is intended to
allow the superimposition of contracts over the same component, when they


                                         2
concern diﬀerent aspects of its behaviour. This also enables component reuse,
by allowing contracts to reveal only the behaviour relevant to the diﬀerent use
cases.

Motivation and Contribution. The meta-theory of Benveniste et al. focuses
on the design of embedded and cyber-physical systems. However, there exists a
noticeable gap between this meta-theory and the way contracts are used when
developing general software following Meyer’s design-by-contract methodology.
At the core of this gap appears to be the notion of procedure 1 . While the
procedure is a central unit of composition in software development, the meta-
theory does not suggest an obvious way of treating procedures as components.
This situation is not fully satisfactory, since the software components of most
embedded systems are implemented with the help of procedures (a typical C-
module, for instance, would consist of a main function and a number of helper
functions), and their development should ideally follow the same design ﬂow as
that of the embedded system as a whole.
    In this paper we provide a ﬁrst step towards a contract theory that takes pro-
cedures as the basic building block, and at the same time respects the axioms of
the meta-theory. Our contract theory is abstract, so that it can be instantiated
to any procedural language, and similarly to the meta-theory, is presented at the
semantics level only. Then, in the context of a simplistic imperative program-
ming language with procedures and its denotational semantics, we show that
the speciﬁcation of contracts of procedures in Hoare logic, and their procedure-
modular veriﬁcation, can be cast in the framework of our abstract contract
theory. We also show that our contract theory is an instance of the meta-theory
of Benveniste et al. With this we expect to contribute to the bridging of the
gap mentioned above, and to give a formal justiﬁcation of the design methodol-
ogy supported by the meta-theory, when applied to the software components of
embedded systems. Several existing contract theories have already been shown
to instantiate the meta-theory. In providing a contract theory for procedural
programs that also instantiates it, we increase the value of the meta-theory by
providing further evidence for its universality. In addition, we prepare the the-
oretical ground for combining our instantiation with other instantiations, which
may target components not to be implemented in software.
    Our theoretical development should be seen as a proof-of-concept. In future
work it will need to be extended to cover more programming language features,
such as object orientation, multi-threading, and exceptions.

Related Work. Software contracts and operations on contracts have long
been an area of intensive research, as evidenced, e.g., by [1]. We brieﬂy mention
some works related to our theory, in addition to the already mentioned ones.
   Reasoning from multiple Hoare triples is studied in [21], in the context of un-
available source code, where new properties cannot be derived by re-veriﬁcation.
  1 We use the term “procedure”, rather than “function” or “method”, to refer to the well-

known control abstraction mechanism of imperative programming languages.



                                            3
In particular, it is found that two Hoare-style rules, the standard rule of conse-
quence and a generalised normalisation rule, are suﬃcient to infer, from a set
of existing contracts for a procedure, any contract that is semantically entailed.
    Often-changing source code is a problem for contract-based reasoning and
contract reuse. In [13], abstract method calls are introduced to alleviate this
problem. Fully abstract contracts are then introduced in [7], allowing reasoning
about software to be decoupled from contract applicability checks, in a way that
not all veriﬁcation eﬀort is invalidated by changes in a speciﬁcation.
    The relation between behavioural speciﬁcations and assume/guarantee-style
contracts for modal transition systems is studied in [2], which shows how to build
a contract framework from any speciﬁcation theory supporting composition and
reﬁnement. This work is built on in [9], where a formal contract framework based
on temporal logic is presented, allowing veriﬁcation of correctness of contract
reﬁnement relative to a speciﬁc decomposition.
    A survey of behavioural speciﬁcation languages [14] found that existing lan-
guages are well-suited for expressing properties of software components, but it
is a challenge to express how components interact, making it diﬃcult to reason
about system and architectural level properties from detailed design speciﬁca-
tions. This provides additional evidence for the gap between contracts used in
software veriﬁcation and contracts as used in system design.

Structure. The paper is organised as follows. Section 2 recalls the concept of
contract based design and the contract meta-theory considered in the present
paper. In Section 3 we present a denotational semantics for programs with pro-
cedures, including a semantics for contracts for use in procedure-modular ver-
iﬁcation. Next, Section 4 presents our abstract contract theory for sequential
programs with procedures. Then, we show in Section 5 that our contract theory
fulﬁls the axioms of the meta-theory, while in Section 6 we show how the spec-
iﬁcation of contracts of procedures in Hoare logic and their procedure-modular
veriﬁcation can be cast in the framework of our abstract contract theory. We
conclude with Section 7.


2     Contract Based Design
This section describes the concept of contract based design, and motivates its use
in cyber-physical systems development. We then recall the contract meta-theory
by Benveniste et al. [5].

2.1    Contract Based Design of Cyber-Physical Systems
Contract based design is an approach to systems design, where the system is
developed in a top-down manner through the use of contracts for components,
which are incrementally assembled so that they preserve the desired system-
wide properties. Contracts are typically described by a set of assumptions the



                                        4
component makes on its environment, and a set of guarantees on the com-
ponent’s behaviour, given that it operates in an environment adhering to the
assumptions [5].
    Present-day cyber-physical systems, such as those found in the automotive,
avionics and other industries, are extremely complex. Products assembled by
Original Equipment Manufacturers (OEMs) often consist of components from
a number of diﬀerent suppliers, all using their own specialised design processes,
system architectures, development platforms, and tools. This is also true inside
the OEMs, where there are diﬀerent teams with diﬀerent viewpoints of the sys-
tem, and their own design processes and tools. In addition, the system itself
has several diﬀerent aspects that need to be managed, such as the architecture,
safety and security requirements, functional behaviour, and so on. Thus, a rigor-
ous design framework is called for that can solve these design-chain management
issues.
    Contract based design addresses these challenges through the principles, at
the speciﬁcation level, of refinement and abstraction, which are processes for
managing the design ﬂow between diﬀerent layers of abstraction, and composi-
tion and decomposition, which manage the ﬂow at the same level of abstraction.
Generally, when designing a system, at the top level of abstraction there will
be an overall system speciﬁcation (or contract). This top-level contract is then
reﬁned, to provide a more concrete contract for the system, and decomposed,
in order to obtain contracts for the sub-systems, and to separate the diﬀerent
viewpoints of the system. A system design typically iterates the decomposition-
and-reﬁnement process, resulting in several layers of abstraction, until contracts
are obtained that can be directly implemented, or for which implementations
already exist. An important requirement on this methodology of hierarchical
decomposition and reﬁnement of contracts is that it must guarantee that when
the low-level components implement their concrete contracts, and are combined
to form the overall system, then the top-level, abstract, contract shall hold.
    Furthermore, a contract framework in particular needs to support indepen-
dent development and component reuse. That is, speciﬁcations for components,
and their operations, must allow for components and speciﬁcations to be in-
dependently designed and implemented, and to be used in diﬀerent parts of
the system, each with their own assumptions on how the other components,
the environment, behave. This is achieved through the principle operations on
contracts: refinement, composition, and conjunction.
    Reﬁnement allows one to extract a contract at the appropriate level of ab-
straction. A desired property of reﬁnement is that components which have been
designed with reference to the more abstract (i.e., weaker) contract do not need
to be re-designed after the reﬁnement step. That is, in the early stages of devel-
opment an OEM may have provided a weak contract for some subsystem to an
external supplier, which implemented a component relying on this contract. As
development of the system progresses, and the contract is reﬁned, the compo-
nent supplied externally should still operate according to its guarantees without
needing to be changed, when instead assuming the new, reﬁned, contract.
    Composition enables one to combine contracts of diﬀerent components into

                                        5
a contract for the larger subsystem obtained when combining the components.
Again, a desirable property is that other components relying on one or more
of the individual contracts, can, after composition of the contracts, assume the
new contract and still perform its guarantees, without being re-designed, thus
ensuring that subsystems can be independently implemented.
    Finally, contract conjunction is another way of combining contracts, but now
for the diﬀerent viewpoints of a single component. This allows one to separate a
contract into several diﬀerent, ﬁner contracts for the same component, revealing
just enough information for each particular system that depends on it, so that
it can be reused in diﬀerent parts of the system, or in entirely diﬀerent systems.

2.2    A Contract Meta-Theory
We consider the meta-theory described in [5]. The stated purpose of the meta-
theory has been to distil the notion of a contract to its essence, so that it
can be used in system design methodologies without ambiguities. In particu-
lar, the meta-theory has been developed to give support for design-chain man-
agement, and to allow component reuse and independent development. It has
been shown that a number of concrete contract theories instantiate it, includ-
ing assume/guarantee-contracts, synchronous Moore interfaces, and interface
theories. To our knowledge, this is the only meta-theory of its purpose and
scope.
    We now present the formal deﬁnitions of the concepts deﬁned in the meta-
theory, and the properties that they entail. The meta-theory is deﬁned only in
terms of semantics, and it is up to particular concrete instantiations to provide
a syntax.

Components. The most basic concept in the meta-theory is that of a com-
ponent, which represents any concrete part of the system. Thus, we have an
abstract component universe M with components m ∈ M. Over pairs of compo-
nents, we have a composition operation ×. This operation is partially deﬁned,
and two components m1 and m2 are called composable when m1 × m2 is deﬁned.
In such cases, we call m1 an environment for m2 , and vice versa. In addition,
component composition must be both commutative and associative, in order to
ensure that diﬀerent components can be combined in any order.
    Typically, components are open, in the sense that they contain functionality
provided by other components, i.e., their environment. The environment in
which a component is to be placed is often unknown at development time, and
although a component cannot restrict it, it is designed for a certain context.

Contracts. In the meta-theory, the notion of contract is deﬁned in terms of
                                             def
sets of components. The contract universe C = 2M ×2M consists of contracts C =
(E, M ), where E and M are the sets of environments and implementations of C,
respectively. Importantly, each pair (m1 , m2 ) ∈ E × M must be composable.
This deﬁnition is intentionally abstract. The intuition is that contracts separate


                                        6
  Table 1: Properties that hold in theories that adhere to the meta-theory.
 # Property
     Refinement. When C1  C2 , every implementation of C1 is also an
 1
     implementation of C2 .
     Shared refinement. Any contract reﬁning C1 ∧ C2 also reﬁnes C1 and C2 .
 2 Any implementation of C1 ∧ C2 is a shared implementation of C1 and C2 .
     Any environment for C1 and C2 is an environment for C1 ∧ C2 .
     Independent implementability. Compatible contracts can be
 3
     independentlyimplemented.
     Independent refinement. For all contracts Ci and Ci′ , i ∈ I, if Ci , i ∈ I
 4 are compatible       and Ci′  Ci , i ∈ I hold, then Ci′ , i ∈ I are compatible
                   ′
          N             N
     and i∈I Ci  i∈I Ci
     Commutativity, sub-associativity. For     N any ﬁnite sets  N of contracts Ci ,
 5 i = 1, . . . , n, C1 ⊗ C2 = C2 ⊗ C1 and 1≤i≤n Ci  ( 1≤i<n Ci ) ⊗ Cn
     holds.
     Sub-distributivity. The following holds, if all contract compositions
 6 in the formula are well deﬁned:
     ((C11 ∧ C21 ) ⊗ (C12 ∧ C22 ))  ((C11 ⊗ C12 ) ∧ (C21 ⊗ C22 ))


the responsibilities of a component from the expectations on its environment.
Moreover, contracts are best seen as weak specifications of components: they
should expose just enough information to be adequate for their purpose.
   For a component m and a contract C = (E, M ), we shall sometimes write
m |=E C for m ∈ E, and m |=M C for m ∈ M . A contract C is said to be
consistent if it has at least one implementation, and compatible if it has at least
one environment.

Contract refinement. For two contracts C1 = (E1 , M1 ) and C2 = (E2 , M2 ),
C1 is said to refine C2 , denoted C1  C2 , iﬀ M1 ⊆ M2 and E2 ⊆ E1 . As an axiom
of the meta-theory, it is required that the greatest lower bound with respect
to reﬁnement exists, for all subsets of C. Table 1 summarises the important
properties of reﬁnement and the other operations on contracts that a concrete
contract theory needs to possess in order to be considered an instance of the
meta-theory.

Contract conjunction. The conjunction of two contracts C1 and C2 , denoted
C1 ∧C2 , is deﬁned as their greatest lower bound w.r.t. the reﬁnement order. (The
intention is that (E1 , M1 ) ∧ (E2 , M2 ) should equal (E1 ∪ E2 , M1 ∩ M2 ); however,
this cannot be taken as the deﬁnition since not every such pair necessarily con-
stitutes a contract.) Then, we have the three desirable properties of conjunction
listed in Table 1, which together are referred to as shared refinement.




                                         7
Contract composition. The composition of two contracts C1 = (E1 , M1 ) and
C2 = (E2 , M2 ), denoted C1 ⊗C2 = (E, M ), is deﬁned when every two components
m1 ∈ M1 and m2 ∈ M2 are composable, and must then be the least contract,
w.r.t. the reﬁnement order, satisfying the following conditions:
    (i) m1 ∈ M1 ∧ m2 ∈ M2 ⇒ m1 × m2 ∈ M ;
 (ii) e ∈ E ∧ m1 ∈ M1 ⇒ m1 × e ∈ E2 ; and
(iii) e ∈ E ∧ m2 ∈ M2 ⇒ e × m2 ∈ E2 .
If all of the above is satisﬁed, then properties 3-6 of Table 1 hold. The intention
is that composing two components implementing C1 and C2 should yield an
implementation of C1 ⊗ C2 , and composing an environment of C1 ⊗ C2 with an
implementation of C1 should result in a valid environment for C2 , and vice versa.
This is important in order to enable independent development.


3     Denotational Semantics of Programs and Con-
      tracts
In this section we summarise the background needed to understand the formal
developments later in the paper. First, we recall the standard denotational se-
mantics of programs with procedures on a typical toy programming language.
Next, we summarise Hoare logic and contracts, and provide a semantic justiﬁ-
cation of procedure-modular veriﬁcation, also based on denotational semantics.

3.1     The Denotational Semantics of Programs with Proce-
        dures
This section sketches the standard presentation of denotational semantics for
procedural languages, as presented in textbooks such as [23, 19]. This semantics
is the inspiration for the deﬁnition of components in our abstract contract theory
in Section 4.1. We start with a simplistic programming language not involving
procedures, and add procedures later to the language.
    The following toy sequential programming language is typically used to
present the denotational semantics of imperative languages:

          S ::= skip | x := a | S1 ; S2 | if b then S1 else S2 | while b do S

where S ranges over statements, a over arithmetic expressions, and b over
Boolean expressions.
    To deﬁne the denotational semantics of the language, we deﬁne the set State
of program states. A state s ∈ State is a mapping from the program variables
to, for simplicity, the set of integers.
    The denotation of a statement S, denoted [[S]], is typically given as a partial
function State ֒→ State such that [[S]] (s) = s′ whenever executing statement S
from the initial state s terminates in state s′ . In case that executing S from s

                                          8
does not terminate, the value of [[S]] (s) is undeﬁned. The deﬁnition of [[S]]
proceeds by induction on the structure of S. For example, the meaning of
sequential composition of statements is usually captured with relation compo-
                                              def
sition, as given by the equation [[S1 ; S2 ]] = [[S1 ]] ◦ [[S2 ]]. For the treatment of the
remaining statements of the language, the reader is referred to [23, 19].
    The deﬁnition of denotation captures through its type (as a partial func-
tion) that the execution of statements is deterministic. For non-deterministic
programs, the type of denotations is relaxed to [[S]] ⊆ State × State; then,
(s, s′ ) ∈ [[S]] captures that there is an execution of S starting in s that termi-
nates in s′ . For technical reasons that will become clear below, we shall use this
latter denotation type in our treatment.
    Note that we could alternatively have chosen State+ as the denotational do-
main, and most results would still hold in the context of ﬁnite-trace semantics.
However, we chose to develop the theory with a focus on Hoare-logic and de-
ductive veriﬁcation. In fact, the domain State × State can be seen as a special
case of ﬁnite traces. In future work, we will also investigate concrete contract
languages based on this semantics, and extend the theory for that context.

Procedures and Procedure Calls. To extend the language and its deno-
tational semantics with procedures and procedure calls, we follow again the
approach of [23], but adapt it to an “open” setting, where some called proce-
dures might not be declared. We consider programs in the context of a ﬁnite
set P of procedure names (of some larger, “closed” program), and a set of pro-
cedure declarations of the form proc p is Sp , where p ∈ P. Further, we extend
the toy programming language with the statement call p.
                        Listing 1: An even-odd toy program.
p r o c ev en i s i f n = 0 then r := 1 e l s e ( n := n − 1 ; c a l l odd ) ;
p r o c odd i s i f n = 0 then r := 0 e l s e ( n := n − 1 ; c a l l ev en )


    As an example, Listing 1 shows a (closed) program in the toy language,
implementing two mutually recursive procedures. The procedures check whether
the value of the global variable n is even or odd, respectively, and assign the
corresponding truth value to the variable r.
    Due to the (potential) recursion in the procedure declarations, the denota-
tion of call p, and thus of the whole language, cannot be deﬁned by structural
induction as directly as before. We therefore deﬁne, for any set P ⊆ P of proce-
dure names, the set EnvP = P → 2State×State of procedure environments, each
environment ρ ∈ EnvP thus providing a denotation for each procedure in P .
              def S
    Let Env = P ⊆P EnvP be the set of all procedure environments. We deﬁne
a partial order relation ⊑ on procedure environments, as follows. For any two
procedure environments ρ ∈ EnvP and ρ′ ∈ EnvP ′ , ρ ⊑ ρ′ if and only if P ⊆ P ′
and ∀p ∈ P. ρ(p) ⊆ ρ′ (p).
    Recall that a complete lattice is a partial order, every set of elements of
which has a greatest lower bound (glb) within the domain of the lattice (see,

                                            9
e.g., [23]). It is easy to show that for any P ⊆ P, (EnvP , ⊑) is a complete
lattice, since a greatest lower bound will exist within EnvP . Then, the least
upper bound (lub) ρ1 ⊔ ρ2 of any two function environments ρ1 ∈ EnvP1 and
ρ2 ∈ EnvP2 also exists, and is the environment ρ ∈ EnvP1 ∪P2 such that ∀p ∈
P1 ∪ P2 . ρ(p) = ρ1 (p) ∪ ρ2 (p).
    We will sometimes need a procedure environment that maps every procedure
in P to State × State, and we shall denote this environment by ρ⊤    P.
    Next, for sets of procedures, we shall need the notion of interface, which is
a pair (P − , P + ) of disjoint sets of procedure names, where P + ⊆ P is a set of
provided (or declared) procedures, and P − ⊆ P a set of required (or called, but
not declared) ones.
    Then, we (re)deﬁne the notion of denotation of statements S in the context
of a given interface (P − , P + ) and environments ρ− ∈ EnvP − and ρ+ ∈ EnvP + ,
                         ρ+                                   ρ+
and denote it by [[S]]ρ− . In particular, we deﬁne [[call p]]ρ− as ρ− (p) when p ∈ P −
and as ρ+ (p) when p ∈ P + .
   Intuitively, the denotation of a call to a procedure should be equal to the
denotation of the body of the latter.           We therefore introduce, given an
environment ρ− ∈ EnvP − , the function ξ : EnvP + → EnvP + deﬁned by
           def     ρ+
ξ(ρ+ )(p) = [[Sp ]]ρ− for any ρ+ ∈ EnvP + and p ∈ P + , and consider its ﬁxed
points. By the Knaster-Tarski Fixed-Point Theorem (as stated, e.g., in [23]),
since (EnvP + , ⊑) is a complete lattice and ξ is monotonic, ξ has a least ﬁxed-
point ρ+0.
    Finally, we deﬁne the notion of standard denotation of statement S in the
context of a given interface (P − , P + ) and environment ρ− ∈ EnvP − , denoted
                   def        ρ+
[[S]]ρ− , by [[S]]ρ− = [[S]]ρ0− , where ρ+
                                         0 is the least ﬁxed-point deﬁned above.
     For example, for the closed program in Listing 1, we have an interface with
                                                                 ρ+
P + = {even, odd } and P − = ∅. Then, (s, s′ ) ∈ [[Seven ]]ρ− if either s(n) = 0
and s′ = s[r 7→ 1], or else if s(n) > 0 and (s[n 7→ s(n) − 1], s′ ) ∈ ρ+ (odd ). The
                      ρ+
denotation [[Sodd ]]ρ− is analogous. The resulting least ﬁxed-point ρ+     0 is such
                                                                ρ+
that (s, s′ ) ∈ [[Seven ]]ρ− , or equivalently (s, s′ ) ∈ [[Seven ]]ρ0− , whenever s(n) ≥ 0,
and either s(n) is even and then s′ (n) = 0 and s′ (r) = 1, or else s(n) is odd
and then s′ (n) = 0 and s′ (r) = 0. The standard denotation [[Sodd ]]ρ− of odd is
analogous.

3.2     Hoare Logic and Contracts
In this section we summarise the denotational semantics of Hoare logic and the
semantic justiﬁcation of procedure-modular veriﬁcation, as developed by the
second author in [12]. These formalisations serve as the starting point for the
deﬁnition of contracts in our contract theory developed in Section 4.2.

Hoare Logic. The basic judgement of Hoare logic [15] is the Hoare triple,
written {P }S{Q}, where P and Q are assertions over the program state, and S


                                            10
is a program statement. The Hoare triple signiﬁes that if the statement S is
executed from a state that satisﬁes P (called the pre-condition), and if this
execution terminates, then the ﬁnal state of the execution will satisfy Q (called
the post-condition). Additionally, so-called logical variables can be used within
a Hoare triple, to specify the desired relationship between the values of variables
after execution and the values of variables before execution. The values of the
program variables are deﬁned by the notion of state; to give a meaning to the
logical variables we shall use interpretations I. We shall write s |=I P to signify
that the assertion P is true w.r.t. state s and interpretation I. The formal
validity of a Hoare triple is denoted by |=par {P }S{Q}, where the subscript
signiﬁes that validity is in terms of partial correctness, where termination of the
execution of S is not required.
    An example of a Hoare triple, stating the desired behaviour of procedure odd
from Listing 1, is shown below, where we use the logical variable n0 to capture
to the value of n prior to execution of odd :
 {n ≥ 0∧n = n0 } Sodd {(n0 mod 2 = 0 ⇒ r = 0)∧(n0 mod 2 = 1 ⇒ r = 1)} (1)
Procedure even is speciﬁed analogously.
    Hoare logic comes with a proof calculus for reasoning in terms of Hoare
triples, consisting of proof rules for the diﬀerent types of statements of the
programming language. An example is the rule for sequential composition:
                  {P } S1 {R}      {R} S2 {Q}
                                              Composition
                        {P } S1 ; S2 {Q}
which essentially states that if executing S1 from any state satisfying P ter-
minates (if at all) in some state satisfying R, and executing S2 from any state
satisfying R terminates (if at all) in some state satisfying Q, then it is the case
that executing the composition S1 ; S2 from any state satisfying P terminates
(if at all) in some state satisfying Q. The proof system is sound and relatively
complete w.r.t. the denotational semantics of the programming language (see,
e.g., [23, 19]).

Hoare Logic Contracts. One can view a Hoare triple {P }S{Q} as a contract
C = (P, Q) imposed on the program S. In many contexts it is meaningful to
separate the contract from the program; for instance, if the program is yet to
be implemented. In our earlier work [12], we gave such contracts a denotational
semantics as follows:
                        def
                   [[C]] = {(s, s′ ) | ∀I. (s |=I P ⇒ s′ |=I Q)}               (2)
The rationale behind this deﬁnition is the following desirable property: a pro-
gram meets a contract whenever its denotation is subsumed by the denotation
of the contract, i.e., S |=par C if and only if [[S]] ⊆ [[C]].
     For example, for the contract Codd induced by (1) we have that (s, s′ ) ∈
[[Codd ]] if and only if either s(n) < 0, or else s′ (r) = 0 if s(n) is even and
s′ (r) = 1 if s(n) is odd. The denotation of Ceven is analogous.

                                        11
The Denotational Semantics of Programs with Procedure Contracts.
Let S be a program with procedures, and let every declared procedure p ∈ P be
equipped with a procedure contract Cp . Procedure-modular verification refers to
techniques that verify every procedure in isolation. The key to this is to handle
procedure calls by using the contract of the called procedure rather than its
body (i.e., by contracting rather than by inlining [7]). In [12], a semantic justi-
ﬁcation of this is given by means of a contract-relative denotational semantics
of statements. The intuition behind this semantics is that procedure calls are
given a meaning through the denotation of the contract of the called procedure,
rather than through the denotation of its body.
    The contract-relative denotational semantics of a statement S, denoted [[S]]cr ,
is deﬁned with the help of the contract environment ρc that is induced by the
                                   def                             cr def
procedure contracts, i.e., ρc (p) = [[Cp ]] for all p ∈ P, as [[S]] = [[S]]ρc . Notice
that this deﬁnition does not involve solving any recursive equations (i.e., ﬁnding
ﬁxed points), and gives rise to a contract-relative notion of when a statement
                                                            cr
meets a contract, namely S |=cr   par C if and only if [[S]]   ⊆ [[C]]. This is exactly
the correctness notion that is the target of procedure-modular veriﬁcation. As
shown in [12], this notion is sound w.r.t. the original notion S |=par C, in the
sense that S |=cr   par C entails S |=par C. In other words, verifying a program
procedure-modularly establishes that the program is correct w.r.t. its contract
in the standard sense.
    For example, the contract-relative semantics of Seven is such that (s, s′ ) ∈
[[Seven ]]cr if either s(n) < 0, or s(n) = 0 and s′ = s[r 7→ 1], or else s′ (r) = 1
if s(n) is even and s′ (r) = 0 if s(n) is odd. The contract-relative semantics
of Sodd is analogous. Then, it is easy to check that both Seven |=cr      par Ceven and
Sodd |=cr par Codd hold.



4     An Abstract Contract Theory
This section presents an abstract contract theory for programs with procedures.
The theory builds on the basic notion of denotation as a binary relation over
states. As we will show later, it is both an abstraction of the denotational
semantic view on programs with procedures and procedure contracts presented
in Sections 3.1 and 3.2, and an instantiation of the meta-theory described in
Section 2.2.

4.1    Components
In the context of a concrete programming language, we view a component as a
module, consisting of a collection of procedures that are provided by the module.
The module may call required procedures that are external to the module. The
way the provided procedures transform the program state upon a call depends
on how the required procedures transform the state. We take this observation
as the basis of our abstract setting, in which state transformers are modelled
as denotations (i.e., as binary relations over states). A component will thus be


                                          12
simply a mapping from denotations of the required procedures to denotations of
the provided ones, both captured through the notion of procedure environments.
   The contract theory is abstract, in that it is not deﬁned for a particular
programming language, and may be instantiated with any procedural language.
As with the meta-theory, the abstract contract theory is also deﬁned only on
the semantic level.
   Recall the notions and notation from Section 3.1. A component interface
I = (P − , P + ) is a pair of disjoint, ﬁnite sets of procedure names, of the required
and the provided ones, respectively.
                                                              −    +
Definition 1 (Component). A component m with interface Im = (Pm , Pm ) is
a mapping m : EnvPm
                  − → Env + .
                           Pm

Let M denote the universe of all components over P.
    We assume that any system is built up from a set of base components, the
simplest components from which more complex components are then obtained
by composition. The base components must be monotonic functions over the
lattice deﬁned in Section 3.1.
            −
    When Pm    = ∅, we shall identify m with an element of EnvPm  + . In other

words, when a component is closed, i.e., is not dependent on any external pro-
cedures, the provided environment is constant.
Definition 2 (Component composability). Two components m1 and m2 are
                +      +
composable iff Pm 1
                    ∩ Pm 2
                           = ∅.
   When deﬁning the composition of two components, particular care is re-
quired in the treatment of procedure names that are provided by one of the
components while required by the other. Let µx. f (x) denote the least ﬁxed-
point of a function f , when it exists.
Definition 3 (Component composition). Given two composable components
m1 : EnvPm  −  → EnvPm+  and m2 : EnvPm
                                      −   → EnvPm + , their composition is
             1         1                2          2
defined as a mapping m1 × m2 : EnvP −     → EnvP +      such that:
                                                 m1 ×m2               m1 ×m2


                  +          def
                             +      +
                 Pm 1 ×m2
                          = Pm 1
                                 ∪ Pm 2

                  −          def
                              −      −         +      +
                 Pm 1 ×m2
                          = (Pm 1
                                  ∪ Pm 2
                                         ) \ (Pm 1
                                                   ∪ Pm 2
                                                          )
                             def
                 m1 × m2 = λρ−
                             m1 ×m2 ∈ EnvP −                      . µρ. χ+
                                                                         m1 ×m2 (ρ)
                                                         m1 ×m2



where χ+
       m1 ×m2 : EnvP +                  → EnvP +          is defined, in the context of a given
                         m1 ×m2                 m1 ×m2

ρ−
 m1 ×m2 ∈ EnvPm
              −            , as follows.       Let ρ+
                                                    m1 ×m2 ∈ EnvPm
                                                                 +    , and let ρ−
                                                                                 m1 ∈
                ×m   1   2                                         ×m      1   2
Env    −
      Pm     be the environment defined by:
         1


                                        ρ+                        −      +
                                    
                              def        m1 ×m2 (p)       if p ∈ Pm   ∩ Pm
                   ρ−
                    m1 (p) =
                                                                    1      2
                                        ρ−
                                         m1 ×m2 (p)
                                                                  −      +
                                                          if p ∈ Pm1 \ Pm2



                                                 13
and let ρ−
         m2 ∈ EnvPm−   be defined symmetrically. We then define:
                    2


                                        m1 (ρ−                +
                                      
                                  def        m1 )(p)  if p ∈ Pm
            χ+     (ρ +
             m1 ×m2 m1 ×m2   )(p) =          −                +
                                                                1
                                        m2 (ρm2 )(p)  if p ∈ Pm 2


    In the above deﬁnition, χ+ m1 ×m2 represents the denotations of the procedure
bodies of the procedures provided by the two composed components, given deno-
tations of procedure calls to the same procedures. The choice of least ﬁxed-point
will be crucial for the proof of Theorem 2(i) in Section 4.2 below.
    The deﬁnition is well-deﬁned, in the sense that the stated least ﬁxed-points
exist, and the resulting components are monotonic functions.
Theorem 1. Component composition is well-defined.
Proof. For any P ⊆ P, we have that (EnvP , ⊑) forms a complete lattice. Thus,
in particular, (EnvP +    , ⊑) is a complete lattice. By the Knaster-Tarski
                      m1 ×m2
Fixed-Point Theorem, as stated e.g. in [23], if (EnvP +            , ⊑) is a complete
                                                          m1 ×m2

lattice, and χ+
              m1 ×m2 : EnvPm
                           +           → EnvP +        is monotonic, then χ+
                                                                           m1 ×m2
                             ×m1   2          m1 ×m2
has a least ﬁxed-point.
    To prove that components are monotonic functions, we shall use structural
induction. Since base components are monotonic by deﬁnition, we only have
to show that composition preserves monotonicity. Assume that m1 and m2 are
monotonic. Since χ+m1 ×m2 is an application of either m1 or m2 , it must also be
monotonic, and thus have a least ﬁxed-point. The µ operator is itself monotonic,
and the component m1 × m2 must therefore be monotonic as well.

4.2    Denotational Contracts
We now deﬁne the notion of denotational contracts c in the style of assume/guar-
antee contracts [4, 6]. Contracts shall also be given interfaces.
Definition 4 (Denotational contract). A denotational contract c with interface
Ic = (Pc− , Pc+ ) is a pair (ρ−    +           −               +
                              c , ρc ), where ρc ∈ EnvPc− and ρc ∈ EnvPc+ .

The intended interpretation of the environment pair is as follows: assuming
that the denotation of every called procedure p ∈ Pc− is subsumed by ρ−  c (p),
then it is guaranteed that the denotation of every provided procedure p′ ∈ Pc+
is subsumed by ρ+     ′
                  c (p ).

Definition 5 (Contract implementation). A component m with interface Im =
   −    +
(Pm  , Pm ) is an implementation for, or implements, a contract c = (ρ−    +
                                                                      c , ρc )
                         − +                         −    −    +     +
with interface Ic = (Pc , Pc ), denoted m |= c, iff Pc ⊆ Pm , Pm ⊆ Pc , and
m(ρ−       ⊤           +
    c ⊔ ρP − \P − ) ⊑ ρc .
          m   c

The reason for not requiring the interfaces to be equal is that we aim at a subset
relation between components implementing a contract and those implementing
a reﬁnement of said contract, in the meta-theory instantiation.
    For a mapping h : A → B and set A′ ⊆ A, let h|A′ denote as usual the
restriction of h on A′ .

                                         14
Definition 6 (Contract environment). A component m is an environment for
contract c iff, for any implementation m′ of c, m and m′ are composable, and
∀ρ−
  m×m′ ∈ EnvP −       ′
                        . (m × m′ )(ρ−             +
                                     m×m′ )|Pc+ ⊑ ρc .
                   m×m


Intuitively, an environment of a contract c is then a component such that when
it is composed with an implementation of c, the composition will operate satis-
factorily with respect to the guarantee of the contract.
     We will now deﬁne the reﬁnement relation, and the conjunction and compo-
sition operations, on contracts.
Definition 7 (Contract reﬁnement). A contract c reﬁnes contract c′ , denoted
c  c′ , iff ρ−     −      +    +
              c′ ⊑ ρc and ρc ⊑ ρc′ , where ⊑ is the partial order relation defined
in Section 3.1.

The reﬁnement relation reﬂects the intention that if a contract c reﬁnes another
contract c′ , then any component implementing c should also implement c′ .
Definition 8 (Contract conjunction). The conjunction of two contracts c1 =
                                                                        def
(ρ−     +               −     +                                −     −     +     +
  c1 , ρc1 ) and c2 = (ρc2 , ρc2 ) is the contract c1 ∧ c2 = (ρc1 ⊔ ρc2 , ρc1 ⊓ ρc2 ),
where ⊔ and ⊓ are the lub and glb operations of the lattice, respectively.
This deﬁnition is consistent with the intention that any contract that reﬁnes
c1 ∧ c2 should also reﬁne c1 and c2 individually. The interface of c1 ∧ c2 is then
Ic1 ∧c2 = (Pc−1 ∪ Pc−2 , Pc+1 ∩ Pc+2 ). Note that while this is the interface in general,
conjunction of contracts is typically used to merge diﬀerent viewpoints of the
same component, and in that case Ic1 = Ic2 = Ic1 ∧c2 .
Definition 9 (Contract composability). Two contracts c1 = (ρ−                           +
                                                                                  c1 , ρc1 ) and
c2 = (ρ− c2 , ρ +
                c2 ) with interfaces  I c1  =  (P −
                                                 c1 , P +
                                                       c1 ) and Ic2 =  (P −
                                                                          c2 , P +
                                                                                c2 )  are   com-
posable if: (i) Pc+1 ∩ Pc+2 = ∅, (ii) ∀p ∈ Pc−1 ∩ Pc+2 . ρ+          c2 (p)   ⊆   ρ −
                                                                                    c1 (p),  and
 (iii) ∀p ∈ Pc−2 ∩ Pc+1 . ρ+c1 (p) ⊆ ρ −
                                       c2 (p).
The conditions for composability ensure that the mutual guarantees of the two
contracts meet each other’s assumptions.
Definition 10 (Contract composition). The composition of two composable
contracts c1 = (ρ−     +               −     +                             −     +
                 c1 , ρc1 ) and c2 = (ρc2 , ρc2 ), with interfaces Ic1 = (Pc1 , Pc1 ) and
                                                                  def
Ic2 = (Pc−2 , Pc+2 ), respectively, is the contract c1 ⊗ c2 = (ρ−         +     +
                                                                c1 ⊗c2 , ρc1 ⊔ ρc2 ), where:

                                def
                        ρ−          −     −
                         c1 ⊗c2 = (ρc1 ⊓ ρc2 )     (Pc−1 ∪Pc−2 )\(Pc+1 ∪Pc+2 )


The interface of c1 ⊗ c2 is Ic1 ⊗c2 = ((Pc−1 ∪ Pc−2 ) \ (Pc+1 ∪ Pc+2 ), Pc+1 ∪ Pc+2 ).
Theorem 2. For any composable contracts c1 and c2 , and any implementations
m1 |= c1 and m2 |= c2 , m1 and m2 are composable, and c1 ⊗ c2 is the least
contract (w.r.t. refinement order) for which the following properties hold:
  (i) m1 × m2 |= c1 ⊗ c2 ,


                                              15
 (ii) if m is an environment to c1 ⊗ c2 , then m1 × m is an environment to c2 ,
(iii) if m is an environment to c1 ⊗ c2 , then m × m2 is an environment to c1 .
Proof. Let the contracts c1 = (ρ−          +               −     +
                                     c1 , ρc1 ) and c2 = (ρc2 , ρc2 ) with interfaces Ic1 =
   −    +                −     +
(Pc1 , Pc1 ) and Ic2 = (Pc2 , Pc2 ) be composable, and let m1 |= c1 and m2 |= c2 .
Since contract composition restricts the interface in the same way as component
composition, m1 and m2 are also composable.
    Proof of (i). Since m1 |= c1 and m2 |= c2 , it must be the case that
Pc−1 ∪ Pc−2 ⊆ Pm  −
                   1
                        −
                     ∪ Pm 2
                             and Pm   +
                                        1
                                           ∪ Pm +
                                                 2
                                                   ⊆ Pc+1 ∪ Pc+2 , so Pc−1 ⊗c2 ⊆ Pm  −
                                                                                      1 ×m2
        +            +
and Pm1 ×m2 ⊆ Pc1 ⊗c2 , which are the ﬁrst two conditions from Deﬁnition 5.
                           def                                                                       def
Now, let ρ−         −         ⊤
          m1 ×m2 = ρc1 ⊗c2 ⊔ ρP −                               −                   and ρ+         +     +
                                                                                         c1 ⊗c2 = ρc1 ⊔ ρc2 . Re-
                                                       m1 ×m2 \Pc1 ⊗c2

call the deﬁnition of χ+ m1 ×m2 in Deﬁnition 3, deﬁned now in the context of
the above ρ−m1 ×m2 .  We   need to show (m1 × m2 )(ρ−              +
                                                     m1 ×m2 ) ⊑ ρc1 ⊗c2 , i.e., that
      +              +                     +                +
µρ. χm1 ×m2 (ρ) ⊑ ρc1 ⊗c2 . By using that ρc ⊗c |P +    ⊑ ρc1 ⊗c2 , this reduces to
                                                                     1      2       m1 ×m2

showing µρ. χ+             +
             m1 ×m2 (ρ) ⊑ ρc ⊗c |P +                                . This we accomplish by proving that
                                           1       2    m1 ×m2

χ+        +
 m1 ×m2 (ρc ⊗c |P +              ) ⊑ ρ+
                                      c ⊗c |P +
                                                                   , which establishes that ρ+
                                                                                             c ⊗c |P +
            1     2   m1 ×m2               1       2    m1 ×m2                                                           1    2   m1 ×m2

is a preﬁxed-point of χ+                                           +
                       m1 ×m2 , and is therefore greater than µρ. χm1 ×m2 (ρ).
                             +         +                  +
    Thus, we need to show χm1 ×m2 (ρc ⊗c |P +       ) ⊑ ρc ⊗c |P +    , i.e., that
                                                               1     2      m1 ×m2             1     2       m1 ×m2
      +
∀p ∈ Pm 1 ×m2
              . χ+        +
                 m1 ×m2 (ρc ⊗c |P +                          )(p) ⊆ ρ+
                                                                     c ⊗c |P +
                                                                                                                 +
                                                                                                   (p). Let p ∈ Pm 1
                                                                                                                     ; the
                                   1       2   m1 ×m2                           1    2   m1 ×m2
           +
case p ∈ Pm  2
                 is symmetric. Using the notation of Deﬁnition 3, we have:
                     
                      ρ+        +        (p′ )              if p′ ∈ Pm −
                                                                           ∩ Pm+
                        c1 ⊗c2 |Pm                                       1       2
       ρ−  (p ′
                ) =                1 ×m2
        m1
                      (ρ−
                         c1 ⊗c2  ⊔  ρ ⊤
                                      P −
                                                \P − )(p ′
                                                           ) if p ′
                                                                    ∈ P −
                                                                       m1  \ P +
                                                                              m2
                                                   m1 ×m2          c1 ⊗c2



Below we shall show ρ−     −     ⊤
                     m1 ⊑ ρc1 ⊔ ρP − \P − . Since m1 |= c1 , by Deﬁnition 5 we
                                                          m1        c1

have m(ρ−     ⊤             +
        c1 ⊔ ρP − \P − ) ⊑ ρc1 , and by monotonicity of m1 and transitivity of ⊑,
                      m1    c1
                                                       +        +
we obtain m(ρ−       +                   +
             m1 ) ⊑ ρc1 . Then, for p ∈ Pm1 , we have χm1 ×m2 (ρc ⊗c |P +                                                             )(p) =
                                                                                                             1       2       m1 ×m2
                            +
m1 (ρ−           +
     m1 )(p) ⊆ (ρc1 )(p) = ρc ⊗c |P +                           (p), which is what we wanted to prove.
                                       1       2       m1 ×m2

   And ﬁnally, we need to show ρ−          −
                                  m1 ⊑ ρc1 ⊔ ρPm
                                                ⊤
                                                 −
                                                    \Pc−1
                                                          . There are altogether ﬁve
                                                  1
                                              ′    −       +
cases that need to be considered. First, let p ∈ Pc1 ∩Pm    2
                                                                                   −
                                                              (recall that Pc−1 ⊆ Pm 1
                                                                                       ,
since m1 |= c1 ). Since c1 and c2 are composable, by Deﬁnition 9 we have
                                                               +
∀p ∈ Pc−1 ∩ Pc+2 . ρ+         −                     −    ′
                    c2 (p) ⊆ ρc1 (p). Then we have ρm1 (p ) = ρc ⊗c |P + (p′ ) =
                                                                                                         1       2   m1 ×m2

ρ+    ′     −    ′      −     ⊤           ′              ′    −     −       +
 c2 (p ) ⊆ ρc1 (p ) = (ρc1 ⊔ ρP − \P − )(p ). Next, let p ∈ (Pm1 \ Pc1 ) ∩ Pm2 .
                                               m1       c1

This case is similar to the ﬁrst one, but now ρ+    ′     ⊤          ′      −
                                               c2 (p ) ⊆ ρP − \P − (p ) = (ρc1 ⊔                    m1        c1

ρ⊤
 P − \P −
                                           +
          )(p′ ). Third, let p′ ∈ (Pc−1 \ Pm 2
                                               ) \ Pc−2 . Then we have ρ−    ′
                                                                        m1 (p ) =
  m1   c1

(ρ−         ⊤
  c1 ⊗c2 ⊔ ρP −          −         )(p′ ) = ρ−    ′      −     ⊤           ′                ′
                                             c1 (p ) = (ρc1 ⊔ ρP − \P − )(p ). Fourth, let p ∈
                m1 ×m2 \Pc1 ⊗c2                                                          m1   c1
  −
(Pm 1
         +
      \ Pm 2
             ) \ Pc−1 . This case is similar to the third one, but now (ρ−
                                                                         c1 ⊗c2 ⊔


                                                              16
ρ⊤
 P−          −        )(p′ ) ⊆ ρ⊤
                                P − \P −
                                         (p′ ) = (ρ−     ⊤           ′                  ′
                                                   c1 ⊔ ρP − \P − )(p ). And last, let p ∈
    m1 ×m2 \Pc1 ⊗c2              m1   c1                  m1    c1

Pc−1 ∩ Pc−2 . This case is also similar to the third one, but now, by Deﬁnition 10,
we have (ρ−             ⊤
              c1 ⊗c2 ⊔ ρP −     \P −
                                       )(p′ ) = (ρ−      −     ′     −    ′      −
                                                   c1 ⊓ ρc2 )(p ) ⊆ ρc1 (p ) = (ρc1 ⊔
                             m1 ×m2   c1 ⊗c2

ρ⊤
 P − \P −
          )(p′ ). This concludes the proof of (i).
    m1   c1

    Proof of (ii). Let m be an environment to c1 ⊗c2 . Then, Pm     +
                                                                      ∩Pc+1 ⊗c2 = ∅ and
                  +     +
consequently Pm ∩ Pc1 = ∅, so m and m1 are composable. Furthermore, since
  +                                            +
Pm  ∩Pc+2 = ∅ and Pm  +
                       1
                         ∩Pc+2 = ∅ we have Pm   1 ×m
                                                     ∩Pc+2 = ∅, thus the condition on
                              +
the interfaces hold. Since ρc1 ×c2 is the lub of ρc1 and ρ−
                                                   −                  +     +
                                                           c2 , and Pc1 ∩Pc2 = ∅, then
                           +                      +        +
denotations for all p ∈ Pc2 are the same in ρc2 and ρc1 ⊗c2 . Thus, we have that
∀ρ−
  m1 ×m×m2 ∈ EnvP −             . ∀p ∈ Pc+2 . (m1 ×m×m2 )(ρ−                       +
                                                                m1 ×m×m2 )(p) ⊆ ρc2 (p)
                           m1 ×m×m2
                                       +
must hold, which it does since ρ+
                                c2 = ρ                        and m is an environment to
                                                c1 ⊗c2 Pc+2
c1 ⊗ c2 . So m1 × m is an environment to c2 .
    The proof of (iii) is analogous.
    Finally, c1 ⊗c2 is the least contract for which the above properties hold, since
weakening ρ−                            +
              c1 ⊗c2 or strengthening ρc1 ⊗c2 would immediately falsify (i).



5        Connection to Meta-Theory
In this section we show that the abstract contract theory presented in Section 4
instantiates the meta-theory described in Section 2.2.
    In our instantiation of the meta-theory, we consider as the abstract compo-
nent universe M the same universe of components M as deﬁned in Section 4.1.
To distinguish the contracts of the meta-theory from those of the abstract the-
ory, we shall always denote the former by C and the latter by c. Recall that a
contract C is a pair (E, M ), where E, M ⊆ M. The formal connection between
the two notions is established with the following deﬁnition.
Definition 11 (Induced contract). Let c be a denotational contract. It induces
                                       def
the contract Cc = (Ec , Mc ), where Ec = {m ∈ M | m is an environment for c}
           def
and Mc = {m ∈ M | m |= c}.
Since contract implementation requires that the implementing component’s pro-
vided functions are a subset of the contract’s provided functions, every compo-
                      +
nent m such that Pm     ∩ Pc+ = ∅ is composable with every component in Mc .
    The deﬁnitions of implementation, reﬁnement and conjunction of denota-
tional contracts make this straightforward deﬁnition of induced contracts possi-
ble, so that it directly results in reﬁnement as set membership and conjunction
as lub w.r.t. the reﬁnement order.
Theorem 3. The contract theory of Section 4 instantiates the meta-theory of
Benveniste et al. [5], in the sense that composition of components is associative
and commutative, and for any two contracts c1 and c2 :
    (i) c1  c2 iff Cc1 refines Cc2 according to the definition of the meta-theory,

                                               17
 (ii) Cc1 ∧c2 is the conjunction of Cc1 and Cc2 as defined in the meta-theory, and
(iii) Cc1 ⊗c2 is the composition of Cc1 and Cc2 as defined in the meta-theory.
Proof. Statement (i) holds since c1  c2 means that for all components m, if
m |= c1 then m |= c2 . Equivalently, if m |=M Cc1 then m |=M Cc2 , which means
that Mc1 ⊆ Mc2 . Now, c1  c2 also means that all components m′ composable
with components in Mc2 are also composable with all components in Mc1 , and
thus Ec2 ⊆ Ec1 . So c1  c2 iﬀ Cc1  Cc2 .
    Statement (ii) clearly holds: any component implementing c1 ∧ c2 also im-
plements c1 and c2 . Thus, every component in Mc1 ∧c2 is also in Mc1 and Mc2 .
Similarly, all components that are environments of c1 or c2 , are also environ-
ments of c1 ∧ c2 . So Mc1 ∧c2 is the greatest lower bound of Mc1 and Mc2 with
respect to reﬁnement.
    We will now show that Statement (iii) holds. Recall Theorem 2, and say
that we have components and contracts such that m1 |= c1 and m2 |= c2 , or, by
Deﬁnition 11, that m1 |=M Cc1 and m2 |=M Cc2 . From Theorem 2 we then have
that m1 × m2 |= c1 ⊗ c2 , or m1 × m2 |=M Cc1 ⊗c2 . This trivially holds in the other
direction as well. Say that we also have m such that m is an environment to
c1 ⊗ c2 , or, in other words, that m |=E Cc1 ⊗c2 . By Theorem 2 we then have that
m1 × m is an environment to c2 , or m1 × m |=E Cc2 . Again, this trivially holds
in the other direction, and by symmetry we also have that m × m2 |=E Cc1 .
   Let us now return to our example from Section 3. When applying Contract
Based Design, contracts at the more abstract level will be decomposed into
contracts at the more concrete level. So, for our example, we might have at the
top level a contract c = (ρ−    +                                              −
                           c , ρc ) with interface (∅, {even, odd}), where ρc = ∅,
             +                                                ′
and where ρc ∈ EnvPc+ maps even to the set of pairs (s, s ) such that whenever
s(n) is non-negative and even, then s′ (r) = 1, and when s(n) is non-negative
and odd, then s′ (r) = 0, and maps odd in a dual manner. This contract could
                                                                                   def
then be decomposed into two contracts ceven and codd , so that ρ+     ceven (even) =
                            def
ρ+              −              +
 c (even) and ρceven (odd ) = ρc (odd ), and codd is analogous. Then, we would
have ceven ⊗ codd  c, and for any two components meven and modd such that
meven |= ceven and modd |= codd , it would hold that meven × modd |= c.


6    Connection to Programs with Procedures
In this section we discuss how our abstract contract theory from Section 4 relates
to programs with procedures as presented in Section 3.1, and how it relates to
Hoare logic and procedure-modular veriﬁcation as presented in Section 3.2.
    First, we deﬁne how to abstract the denotational notion of procedures into
components in the abstract theory, based on the function ξ from Section 3.1.
Definition 12 (From procedure sets to components). For any set of proce-
dures P + , calling procedures P ′ , we define the component m : EnvPm
                                                                     − →




                                         18
                −   ′ def
                        +      +    +          def
                                                 −
    + , where P
EnvPm          m = P \ Pm and Pm = P , so that ∀ρm ∈ EnvPm
                                                         − . ∀p ∈

 +              def
Pm . m(ρ−
        m )(p) = [[Sp ]]ρ−
                         m
                           .
     As the next result shows, procedure set abstraction and component compo-
sition commute. Together with commutativity and associativity of component
composition, this means that the initial grouping of procedures into components
is irrelevant, and that one can start with abstracting each individual procedure
into a component.
Theorem 4. For any two disjoint sets of procedures P1+ and P2+ , abstracted
individually into components m1 and m2 , respectively, and P1+ ∪ P2+ abstracted
into component m, it holds that m1 × m2 = m.
Proof. Let the set of procedures P1+ , calling but not providing P1− , and the
disjoint set P2+ , calling but not providing P2− , be abstracted into components
m1 and m2 , respectively, and let the set P + = P1+ ∪ P2+ be abstracted into
component m, all following Deﬁnition 12. The interfaces of components m
                                                         +
and m1 × m2 are equal, since Pm    +
                                      = Pm+
                                           1
                                                +
                                             ∪ Pm 2
                                                    = Pm   1 ×m2
                                                                 , and if P2− and P2−
                                                +          +
are the procedures called by (but not in) P1 and P2 , respectively, then the
procedures called by (but not in) P + are Pm   −
                                                 = (Pm  −
                                                         1
                                                            ∪ Pm−
                                                                  2
                                                                          +
                                                                    ) \ (Pm 1
                                                                                 +
                                                                              ∪ Pm 2
                                                                                     )=
  −
Pm1 ×m2 .
    To show that m1 × m2 = m, we have also to show that for all procedures
p ∈ P1+ ∪ P2+ , ∀ρ ∈ EnvPm   − . m(ρ)(p) = (m1 × m2 )(ρ)(p). It is enough to show

that ∀p ∈ P1+ . ∀ρ ∈ EnvPm   − . m(ρ)(p) = (m1 × m2 )(ρ)(p). By symmetry it then
                          +                         +
also holds for all p ∈ P2 , and thus for all p ∈ Pm   .
                                                                        ρ+
   For any p ∈ P1+ and ρ− ∈ EnvPm               −
                                                               ρ           ρ
                                                                            0    +
                                         − , m(ρ )(p) = [[Sp ]] − = [[Sp ]] − = ρ (p) =
                                                                                 0
(µρ. ξ(ρ))(p), where ξ : EnvP + → EnvP + is relativised on ρ− , as we recall
from Section 3.1. However, we could view this as taking the simultaneuos least
ﬁxed-point of two functions ξ1 : EnvP + × EnvP + → EnvP + and ξ2 : EnvP + ×
                                            1       2             1                 1
EnvP + → EnvP + , both also relative to ρ− , and then taking the union of the
      2             2
resulting procedure environments as the result.
   The well-known Bekić’s Lemma [3] states that, for a complete lattice L,
and monotone f, g such that f : Lp+q → Lp , g : Lp+q → Lq , it holds that
µx, y. (f (x, y), g(x, y)) = (x0 , y0 ), where x0 = µx. f (x, µy. g(x, y)) and y0 =
µy. g(x0 , y), meaning that for two interdependent monotone functions, taking
the simultaneous least ﬁxed-points gives the same results as iteratively ﬁnding
them one function at a time. Using the special case when p = q = 1, we
have that the lemma also holds for f, g : L × L → L. Furthermore, in our
case, for any complete lattice (EnvP , ⊑) and function h′ : EnvP → EnvP ,
                                                                       def
we can deﬁne the equivalent function h : Env → Env by h(ρ) = h′ (ρ ⊓ ρ⊤     P ),
essentially ignoring denotations for all procedures not in P . We then get that
Bekić’s Lemma also holds for monotone f : EnvP1 × EnvP2 → EnvP1 and
g : EnvP1 × EnvP2 → EnvP2 , for any two sets of procedures P1 and P2 .
    Again relativised on ρ− , for p ∈ P1+ and χ+m1 ×m2 : EnvP + → EnvP + we
                        −               +
have that (m1 × m2 )(ρ )(p) = (µρ. χm1 ×m2 (ρ))(p), according to Deﬁnition 3.

                                          19
Here, χ+m1 ×m2 is the simultaneous ﬁxed-point of two functions, for which we
already have partial ﬁxed-points, of the function ξ from Section 3.1. For the
procedures in P1+ in particular, and for each ρ−  1 ∈ EnvP1− , we have the ﬁxed-
points of the function ξ1 : EnvP + → EnvP + . Recall ξ1 from above. When ρ− ∪
                        ′
                                1            1
ρ−      −               −        ′                  −     −
 2 = ρ1 , we have ξ1 (ρ2 , x) = ξ1 (x) relative to ρ and ρ1 , respectively. Since
these functions are all monotone, when taking the least ﬁxed-point of χ+  m1 ×m2 ,
using the already computed ﬁxed-points, we will then by Bekić’s Lemma get
the same result as the least ﬁxed-point of ξ above, and thus m = m1 × m2 .

Component abstraction example. Let us illustrate the theorem on our
even-odd example (however, the example does not really illustrate Bekić’s Lemma,
since the two procedures do not call themselves).
    By Deﬁnition 12, the procedure set {even} is abstracted into component
meven : Env{odd} → Env{even} with interface ({odd}, {even}), so that ∀ρ− ∈
Env{odd} . m(ρ− )(even) = [[Seven ]]ρ− . By deﬁnition, [[Seven ]]ρ− is equal to
         ρ+
[[Seven ]]ρ0− , where ρ+
                       0 is the least ﬁxed point of ξ : Env{even} → Env{even}
                             def            +
deﬁned by ξ(ρ+ )(even) = [[Seven ]]ρρ− for any ρ+ ∈ Env{even} . Notice, however,
                                                                              ρ+
that procedure even does not have any calls to itself, so [[Seven ]]ρ0− does not
really depend on ρ+ . Then, for any ρ− ∈ Env{odd} , (s, s′ ) ∈ m(ρ− )(even) if
either s(n) = 0 and s′ = s[r 7→ 1], or else if s(n) > 0 and (s[n 7→ s(n) − 1], s′ ) ∈
ρ− (odd ).
    Similarly, the procedure set {odd } is abstracted into component modd :
Env{even} → Env{odd} with interface ({even}, {odd}), so that ∀ρ− ∈ Env{even} .
m(ρ− )(odd ) = [[Sodd ]]ρ− . Then, for any ρ− ∈ Env{even} , (s, s′ ) ∈ m(ρ− )(odd ) if
either s(n) = 0 and s′ = s[r 7→ 0], or else if s(n) > 0 and (s[n 7→ s(n) − 1], s′ ) ∈
ρ− (even).
    Now, applying Deﬁnition 12 to the whole (closed) program yields a com-
ponent m : Env∅ → Env{even,odd} with interface (∅, {even, odd }), so that
∀ρ− ∈ Env∅ . ∀p ∈ {even, odd } . m(ρ− )(p) = [[Sp ]]ρ− . Recall the denotations
[[Seven ]]ρ− and [[Sodd ]]ρ− from the end of Section 3.1.
    Components meven and modd are composable, and by Deﬁnition 3, their
composition has (the same) interface (∅, {even, odd }), and is (also) a mapping
meven × modd : Env∅ → Env{even,odd} .
    Finally, note that function χ+   meven ×modd : Env{even,odd} → Env{even,odd} is
exactly the function ξ in the context of the interface (∅, {even, odd }). This
can be seen by ﬁrst noting that since Env∅ = ∅, we have that χ+           meven ×modd
only depends on its arguments. Furthermore, for all ρ+ ∈ Env{even,odd} , if
       def                         def
ρ+
 odd = ρ
         +
                      and ρ+
                           even = ρ
                                    +                                        −
                                                  we have that, since odd ∈ Peven    +
                                                                                  ∩ Podd ,
              {odd}                      {even}
                                                                                     ρ+
then χ+             +                  +
      meven ×modd (ρ )(even) = meven (ρodd )(even) = [[Seven ]]ρ+ = [[Seven ]]            =
                                                                        odd
   +
ξ(ρ )(even).     Similarly χ+             +             +
                            meven ×modd (ρ )(odd ) = ξ(ρ )(odd ).       We therefore have
meven × modd = m.



                                                  20
   We now deﬁne how to abstract Hoare logic contracts into denotational con-
tracts, in terms of the contract environment ρc deﬁned in Section 3.2.
Definition 13 (From Hoare logic contracts to denotational contracts). For
a procedure p with Hoare logic contract Cp , calling other procedures P − , we
                                                                              def
define the denotational contract cp = (ρ−     +                    +
                                        cp , ρcp ) with interface Pcp = {p} and
    def                       def
Pc−p = P − , so that ρ+                      ′   −   −    ′         ′
                      cp (p) = ρc (p), and ∀p ∈ P . ρcp (p ) = ρc (p ).

    In this way, conceptually, denotational contracts become assume/guarantee-
style speciﬁcations over Hoare logic procedure contracts: assuming that all (ex-
ternal) procedures called by a procedure p transform the state according to their
Hoare logic contracts, procedure p obliges itself to do so as well.
    We now show that if a procedure implements a Hoare logic contract, then the
abstracted component will implement the abstracted contract, and vice versa.
Together with Theorem 4, this result allows the procedure-modular verification
of abstract components.

Theorem 5. For any procedure p with procedure contract Cp , abstracted into
component mp with contract cp , we have Sp |=cr
                                             par Cp iff mp |= cp .
                                                   +
Proof. First, the interfaces will agree: Pm         p
                                                      = {p} = Pc+p , and Pm−
                                                                            p
                                                                              = Pc−p since
they are both the set of called procedures.
    Next, [[Sp ]]cr = [[Sp ]]ρc by deﬁnition (see Section 3.2), i.e., the contract-
relative denotation of Sp is relativised on the contract environment ρc , and so
is ρ−                                                              cr
     cp according to Deﬁnition 13. If we have that Sp |=par Cp , then [[Sp ]]ρc ⊆
[[Cp ]], and since ρ+                                  +                        −
                    cp (p) = [[Cp ]] then [[Sp ]]ρc ⊆ ρcp (p). Because ρc and ρcp agree on
                                            −
all denotations for procedures in Pcp , and because only the denotations of the
procedures in Pc−p aﬀect the denotation of p, then we also have [[Sp ]]ρ−     c
                                                                                  ⊆ ρ+
                                                                                     cp (p).
                                                                               p
   Since m(ρ−
            cp )(p) = [[Sp ]]ρ−
                              c
                                     +
                                and Pm p
                                         = {p}, then m(ρ−       +
                                                        cp ) ⊑ ρcp . Finally, since
                                p
 −
Pm p
     = Pc−p , we have m(ρ−     ⊤               −
                         cp ⊔ ρP − \P − ) = m(ρcp ) and therefore m |= c. The
                                      mp   cp
same argument holds in the other direction.
    Returning to the example from Sections 3 and 5, we can abstract the pro-
cedure set {even} into component meven , with interface ({odd}, {even}), which
would be a function Env{odd} → Env{even} , and ∀ρ− ∈ Env{odd} . m(ρ− )(even) =
[[Seven ]]ρ− . The denotational contracts ceven and codd resulting from the decom-
position shown in Section 5, would be exactly the abstraction of the Hoare Logic
contracts Ceven and Codd shown in Section 3.2. They would both be part of the
contract environment used in procedure-modular veriﬁcation, for example when
verifying that Seven |=crpar Ceven , which would entail meven |= ceven . Thus, by
applying standard procedure-modular veriﬁcation at the source code level, we
prove the top-level contract c proposed in Section 5.




                                            21
7    Conclusion
We presented an abstract contract theory for procedural languages, based on de-
notational semantics. The theory is shown to be an instance of the meta-theory
of [5], and at the same time an abstraction of the standard denotational seman-
tics of procedural languages. We believe that our contract theory can be used to
support the development of cyber-physical and embedded systems by the design
methodology supported by the meta-theory, allowing the individual procedures
of the embedded software to be treated as any other system component. The
work also strengthens the claims of the meta-theory of distilling the notion of
contracts to its essence, by showing that it is applicable also in the context of
procedural programs and deductive veriﬁcation. Finally, this work serves as
a preparation for combining our contract theory for procedural programs with
other instantiations of the meta-theory. In future work we plan to investigate
the utility of our contract theory on real embedded systems taken from the au-
tomotive industry, where not all components are procedural programs, or even
software (cf. our previous work, e.g., [11]). We also plan to extend our toy im-
perative language with additional features, such as procedure parameters and
return values. Furthermore, we plan to extend the contract theory to capture
program traces by developing a ﬁnite-trace semantics, to enable its use in the
speciﬁcation and veriﬁcation of temporal properties. Lastly, we plan to combine
our contract theory with a contract theory for hybrid systems [20].


References
 [1] Abadi, M., Lamport, L.: Composing speciﬁcations. ACM Trans. Program.
     Lang. Syst. 15(1), 73–132 (Jan 1993)
 [2] Bauer, S., David, A., Hennicker, R., Larsen, K., Legay, A., Nyman, U.,
     Wasowski, A.: Moving from speciﬁcations to contracts in component-based
     design. In: Fundamental Approaches to Software Engineering. pp. 43–58
     (2012)
 [3] Bekić, H.: Deﬁnable operation in general algebras, and the theory of au-
     tomata and ﬂowcharts. In: Programming Languages and Their Deﬁnition -
     Hans Bekić (1936-1982). Lecture Notes in Computer Science, vol. 177, pp.
     30–55. Springer (1984)
 [4] Benveniste, A., Caillaud, B., Ferrari, A., Mangeruca, L., Passerone, R.,
     Sofronis, C.: Multiple viewpoint contract-based speciﬁcation and design.
     In: Formal Methods for Components and Objects. vol. 5382, pp. 200–225
     (10 2007)

 [5] Benveniste, A., Caillaud, B., Nickovic, D., Passerone, R., Raclet, J.B.,
     Reinkemeier, P., Sangiovanni-Vincentelli, A., Damm, W., Henzinger, T.A.,
     Larsen, K.G.: Contracts for System Design, vol. 12. Now Publishers (2018)



                                       22
 [6] Benvenuti, L., Ferrari, A., Mangeruca, L., Mazzi, E., Passerone, R., Sofro-
     nis, C.: A contract-based formalism for the speciﬁcation of heterogeneous
     systems. In: 2008 Forum on Speciﬁcation, Veriﬁcation and Design Lan-
     guages. pp. 142–147 (09 2008)
 [7] Bubel, R., Hähnle, R., Pelevina, M.: Fully abstract operation contracts. In:
     Leveraging Applications of Formal Methods, Veriﬁcation and Validation.
     Specialized Techniques and Applications. pp. 120–134 (2014)
 [8] Chen, T., Chilton, C., Jonsson, B., Kwiatkowska, M.: A compositional
     speciﬁcation theory for component behaviours. In: Programming Lan-
     guages and Systems. pp. 148–168. Springer Berlin Heidelberg (2012)
 [9] Cimatti, A., Tonetta, S.: Contracts-reﬁnement proof system for
     component-based embedded systems. Science of Computer Programming
     97 (2015)
[10] Floyd, R.W.: Assigning meanings to programs. Mathematical aspects of
     computer science 19, 19–32 (1967)

[11] Gurov, D., Lidström, C., Nyberg, M., Westman, J.: Deductive functional
     veriﬁcation of safety-critical embedded c-code: An experience report. In:
     Proceedings of FMICS-AVoCS 2017. Lecture Notes in Computer Science,
     vol. 10471, pp. 3–18. Springer (2017)
[12] Gurov, D., Westman, J.: A Hoare Logic Contract Theory: An Exercise in
     Denotational Semantics, pp. 119–127. Springer International Publishing,
     Cham (2018)
[13] Hähnle, R., Schaefer, I., Bubel, R.: Reuse in software veriﬁcation by ab-
     stract method calls. In: Automated Deduction – CADE-24. vol. 7898, pp.
     300–314 (06 2013)
[14] Hatcliﬀ, J., Leavens, G.T., Leino, K.R.M., Müller, P., Parkinson, M.: Be-
     havioral interface speciﬁcation languages. ACM Comput. Surv. 44(3) (Jun
     2012)
[15] Hoare, C.A.R.: An axiomatic basis for computer programming. Commun.
     ACM 12(10), 576–580 (Oct 1969)
[16] Jones, C.: Speciﬁcation and design of (parallel) programs. In: Proceedings
     Of IFIP’83. vol. 83, pp. 321–332 (01 1983)
[17] Lidström, C., Gurov, D.: An abstract contract theory for programs with
     procedures. In: Guerra, E., Stoelinga, M. (eds.) Fundamental Approaches
     to Software Engineering. pp. 152–171. Springer International Publishing,
     Cham (2021)
[18] Meyer, B.: Applying "design by contract". IEEE Computer 25(10), 40–51
     (1992)

                                       23
[19] Nielson, H.R., Nielson, F.: Semantics with Applications: An Appetizer.
     Springer-Verlag, Berlin, Heidelberg (2007)
[20] Nyberg, M., Westman, J., Gurov, D.: Formally proving compositionality
     in industrial systems with informal speciﬁcations. In: Margaria, T., Stef-
     fen, B. (eds.) Leveraging Applications of Formal Methods, Veriﬁcation and
     Validation: Applications. pp. 348–365. Springer International Publishing,
     Cham (2020)
[21] Owe, O., Ramezanifarkhani, T., Fazeldehkordi, E.: Hoare-style reason-
     ing from multiple contracts. In: Integrated Formal Methods - 13th Inter-
     national Conference. Lecture Notes in Computer Science, vol. 10510, pp.
     263–278. Springer (2017)
[22] van Staden, S.: On rely-guarantee reasoning. In: Mathematics of Program
     Construction. pp. 30–49. Springer International Publishing, Cham (2015)
[23] Winskel, G.: The Formal Semantics of Programming Languages: An In-
     troduction. MIT Press, Cambridge, MA, USA (1993)




                                      24
