                                          Proving Cutoff Bounds for Safety Properties in
                                                        First-Order Logic

                                                       Raz Lotan , Eden Frenkel , and Sharon Shoham

                                                                  Tel Aviv University, Tel Aviv, Israel
                                                                       lotanraz@tauex.tau.ac.il
arXiv:2408.10685v1 [cs.LO] 20 Aug 2024




                                               Abstract. First-order logic has been established as an important tool
                                               for modeling and verifying intricate systems such as distributed protocols
                                               and concurrent systems. These systems are parametric in the number of
                                               nodes in the network or the number of threads, which is finite in any
                                               system instance, but unbounded. One disadvantage of first-order logic is
                                               that it cannot distinguish between finite and infinite structures, leading
                                               to spurious counterexamples. To mitigate this, we offer a verification
                                               approach that captures only finite system instances. Our approach is an
                                               adaptation of the cutoff method to systems modeled in first-order logic.
                                               The idea is to show that any safety violation in a system instance of
                                               size larger than some bound can be simulated by a safety violation in a
                                               system of a smaller size. The simulation provides an inductive argument
                                               for correctness in finite instances, reducing the problem to showing safety
                                               of instances with bounded size. To this end, we develop a framework to
                                               (i) encode such simulation relations in first-order logic and to (ii) validate
                                               the simulation relation by a set of verification conditions given to an SMT
                                               solver. We apply our approach to verify safety of a set of examples, some
                                               of which cannot be proven by a first-order inductive invariant.


                                         1   Introduction

                                         Many recent works [2,4,5,15,24,25,33,34,43,44] have used first-order logic for de-
                                         ductive or automatic verification of distributed protocols, concurrent programs,
                                         and other systems that operate over unbounded domains. Most of these works
                                         are based on the notion of an inductive invariant as a way of verifying safety
                                         properties — properties of all reachable states of a system. An inductive invari-
                                         ant is a property that holds in the initial states of the system and is preserved by
                                         the steps of the system. The system, its properties and its inductive invariants
                                         are all specified using first-order formulas, which allows to build on the success of
                                         first-order provers and SMT solvers, with or without theories, for automatically
                                         discharging the verification conditions that establish correctness of the system.
                                             Using first-order logic for modeling and verifying systems and their induc-
                                         tive invariants has significant benefits. First, first-order logic provides a natural
                                         and expressive specification language that, thanks to uninterpreted relation and
                                         function symbols as well as quantifiers, is able to model unbounded domains,
                                         such as network topologies, sets of messages, quorums of processes, and so on.
2       Raz Lotan, Eden Frenkel and Sharon Shoham

In fact, first-order logic is Turing-complete as a specification language for sys-
tems [33]. Second, first-order logic benefits from a plethora of automatic solvers
that already exhibit impressive performance and continue to improve rapidly.
    Unfortunately, using first-order logic for encoding and verifying systems and
their inductive invariants also has several crucial downsides. One obstacle is that
it is not always possible to express a suitable inductive invariant in first-order
logic. Another problem arises from the inability of first-order logic to distin-
guish between finite and infinite structures. This may lead to spurious infinite
counterexamples to induction [9], or even to spurious violations of the property,
in cases where all finite instances of the system satisfy a desired property, but
some infinite instances do not (see Example 1). Because we are usually only in-
terested in finite, albeit unbounded, instances (e.g., a finite number of processes),
violations caused by infinite instances are spurious.
    In this work, we mitigate the aforementioned obstacles by (i) considering a
finite-domain semantics for first-order transition systems that only includes the
finite instances of the system (of any size), and (ii) devising a deductive approach
for establishing a cutoff for a first-order transition system and a safety property
under the finite-domain semantics via a size-reducing simulation between in-
stances of the system. The simulation relation is encoded and validated using
first-order logic. This allows us to take the finite-domain semantics into account
in the verification process, while still using first-order solvers to discharge the
resulting verification conditions.
    Cutoffs are widely used in the context of parameterized systems. A parame-
terized system is a family of transition systems T = {Tn }n , one for each natural
number n ∈ N. The parameter n can represent the number of nodes in a dis-
tributed network, the number of threads running a concurrent program, the
length of an array or a linked list, etc. The parameterized system T satisfies a
property P if Tn satisfies P for all n. A number k is a cutoff for the system T
and the property P if, to verify that T satisfies P , it suffices to verify that Tn
satisfies P for all n ≤ k. Cutoffs therefore allow to reduce the verification of the
unbounded system T to verification of a system where n is bounded by k. The
cutoff method, introduced by [11], proposes to establish that k is a cutoff for T
by proving that for every n > k, Tn is simulated by Tn′ for some n′ < n.
    Much like a parameterized system, a first-order specification of a transition
system induces a family of transition systems, except that instead of a numeric
parameter, the instances are defined by the domain of their states. We can
therefore adapt the cutoff method to verify all the finite instances of a first-order
transition system (i.e., instances obtained by fixing a finite domain): instead of
a simulation between any Tn for n > k and some Tn′ with n′ < n, we need to
show a simulation between any instance with a finite domain of size > k and
some instance with a strictly smaller domain.
    The key technical contribution of our work is a realization of the cutoff
method for first-order transition systems using a size-reducing simulation re-
lation between finite instances of the system. A size-reducing simulation relation
can be understood as proving the induction step in a proof by induction on
           Proving Cutoff Bounds for Safety Properties in First-Order Logic        3

the size of the domain. It therefore lifts correctness of instances of size at most
k to all finite instances, but not to infinite instances. As a result, it may suc-
ceed to verify first-order specifications that only satisfy their property w.r.t. the
finite-domain semantics and not w.r.t. the first-order semantics. Moreover, as
already demonstrated in previous work [19], verification by simulation (akin to
induction on domain size) may sometimes be easier than verification based on
inductive invariants (akin to induction on time), and can succeed in cases where
an inductive invariant cannot be expressed in first-order logic.
    We propose a first-order encoding of a size-reducing simulation relation for
a first-order transition system. We further show how to verify the correctness
of such a (user-provided) encoding by a set of verification conditions that are
encoded as first-order formulas and discharged by an automatic solver.
    Our first challenge is to ensure that the simulation relation is size-reducing
in finite domains. While first-order logic can express the property that the size
of a set is exactly k, at most k or at least k, for any specific number k, it cannot
directly compare the sizes of sets of arbitrary sizes. Our solution is to obtain
size reduction by defining the smaller domain as a subset of the larger domain
obtained by deleting one element. The element to be deleted is specified by a
(user-provided) formula. For finite instances, this ensures that the size of the
domain decreases.
    The next challenge arises from the definition of a simulation relation, which
involves quantification over states: every successor state of the larger state must
be simulated by some successor state of the smaller state. When states are
modeled using uninterpreted functions and relations, this leads to higher-order
quantification. To facilitate a first-order encoding of the verification conditions,
we strengthen the definition of the simulation relation. Namely, we replace the
existential quantification over a simulating successor state of the smaller state
by universal quantification, stating that every state that simulates the larger
successor state is a successor of the smaller state. To ensure that the universal
quantification is not satisfied vacuously, we require the (inductive) totality of
the simulation relation.

Contributions. The main contributions of this paper are:

 – We define the finite-domain semantics of first-order specifications of transi-
   tion systems, formulate the notion of cutoffs, and define size-reducing sim-
   ulations as a way of proving cutoffs for finite-domain first-order transition
   systems (Section 3).
 – We develop an approach for defining and validating size-reducing simulation
   relations in first-order logic (Section 4).
 – We implement a tool that receives as input a first-order specification of a
   transition system and a safety property, as well as a first-order encoding of a
   size-reducing simulation relation, and validates the simulation relation using
   the Z3 [28] SMT solver (Section 5).
 – We demonstrate the applicability of the approach by verifying a set of ex-
   amples of distributed protocols and concurrent systems, including some that
4        Raz Lotan, Eden Frenkel and Sharon Shoham

     cannot be verified by classical techniques based on inductive invariants (Sec-
     tion 5).

The rest of the paper is organized as follows: Section 2 provides the necessary
background on transition systems in first-order logic, Sections 3 to 5 present the
above contributions, Section 6 discusses related work and Section 7 concludes
the paper. We defer all proofs to Appendix A.


2     Preliminaries

This section provides a brief background on transition systems, first-order logic
and first-order specifications of transition systems and properties.

Transition Systems. a transition system T is given by T = (S, I, R), where S is
the set of states, I ⊆ S is the set of initial states, and R ⊆ S × S is the transition
relation. A trace of T is a sequence of states (si )ti=0 such that s0 ∈ I and for
every 0 ≤ i < t we have (si , si+1 ) ∈ R. We denote by R⋆ the reflexive transitive
closure of R. A state s is reachable if there exists a trace (si )ti=0 such that st = s.
A safety property is given by a set of states P ⊆ S. We say that T satisfies P ,
denoted T |= P , if every reachable state of T is in P . A set of states J ⊆ S is
an inductive invariant of T if for any state s ∈ I we have s ∈ J and for any two
states (s, s′ ) ∈ R such that s ∈ J we have s′ ∈ J. Note that if J is an inductive
invariant and J ⊆ P then T |= P .

First-Order Logic. We consider first-order logic with equality. For simplicity
of the presentation, we consider the single-sorted, uninterpreted version of first-
order logic, i.e., without background theories. However, in practice, we use many-
sorted first-order logic and allow some sorts and symbols to be interpreted by
arbitrary background theories. See Section 4.5 for more details.
    A first-order vocabulary Σ consists of relation and function symbols, where
function symbols with arity zero are also called constant symbols. Terms t over Σ
are either variables x or function applications f (t1 , . . . , tm ). Formulas are defined
recursively, where atomic formulas are either t1 = t2 or r(t1 , . . . , tm ) where r is a
relation symbol. Non-atomic formulas are built using connectives ¬, ∧, ∨, → and
quantifiers ∀, ∃. We denote by Vars(α) the variables of a formula α, by FV(α)
the free variables of α, and write α(x1 , . . . , xm ) when FV(α) ⊆ {x1 , . . . , xm }.
We denote a sequence x1 , . . . , xm by x when m is clear from context.
    A structure for Σ is a pair s = (D, I) where D is a domain (a nonempty set
of elements), denoted dom(s), and I is an interpretation that maps each relation
and function symbol to an appropriate construct over the domain. We denote by
struct(Σ) the set1 of all structures for Σ. We define the cardinality (size) of s,
denoted |s|, to be |dom(s)|. For two structures s = (D, I) and s× = (D× , I× ), we
1
    Technically, struct(Σ) is not a well-defined set in the sense of set theory (since we
    allow the domain of a structure to be an arbitrary set). However, for the sake of this
    paper we can restrict the domains to be subsets of N without loss of generality.
            Proving Cutoff Bounds for Safety Properties in First-Order Logic             5

say that s× is a substructure of s if D× ⊆ D, for every relation r ∈ Σ with arity
                                m
m we have I× (r) = I(r) ∩ D×       and for every function f ∈ Σ with arity m we
have I× (f ) = I(f )|D×m . For a formula α with free variables FV(α), a structure

s = (D, I) and an assignment v : FV(α) → D mapping each free variable in α
to an element from the domain, we write s, v |= α to denote that the pair (s, v)
satisfies α, defined as usual. For a variable x and a domain element d, we write
[x → d] for the assignment v : {x} → D with v(x) = d. For two formulas α, β
(not necessarily closed), we write α =⇒ β to denote the validity of α → β.
    For a vocabulary Σ and an identifier o, we denote by Σ o the vocabulary
{a | a ∈ Σ}. We assume that Σ ∩ Σ o = ∅. For a formula (or term) α over Σ we
  o

denote by αo the formula (respectively, term) over Σ o obtained by substituting
each symbol a ∈ Σ by ao ∈ Σ o . With abuse of notation, we sometimes consider
an interpretation I for Σ as an interpretation for Σ o where I(ao ) = I(a), or,
similarly, an interpretation I o of Σ o as an interpretation for Σ.

First-Order Specifications of Transition Systems. We consider transition systems
given by a first-order logic specification T = (Σ, Γ, ι, τ ) where Σ is a vocabulary,
Γ is a closed formula over Σ that acts as a finitely-axiomatizable background
theory, ι is a closed formula over Σ that specifies initial states, and τ is a closed
formula defined over vocabulary Σ ⊎ Σ ′ that specifies the transition relation.
Intuitively, the unprimed copy of Σ specifies the pre-state of a transition, while
the primed copy specifies the post-state. Some symbols in Σ may be declared
immutable, in which case τ preserves their interpretation.
    Any domain D defines a transition system TD = (SD , ID , RD ) where SD is
the set of structures s ∈ struct(Σ) with dom(s) = D that satisfy the axioms, i.e.,
s |= Γ ; ID is the set of states s ∈ SD that satisfy ι; and the transition relation
RD is the set of all pairs of states ((D, I), (D, I ′ )) where, when we identify I as
an interpretation of Σ and I ′ as an interpretation of Σ ′ we have (D, I ⊎ I ′ ) |= τ .
    The standard first-order semantics of T is then given by the transition sys-
tem Tfol = (Sfol , Ifol , Rfol ) where Sfol , Ifol , Rfol are the (disjoint) union of their
counterparts in TD over all domains D (see footnote 1 for well-definedness of the
union). Note that every trace of Tfol is a trace of TD for some domain D. This
is because (s, s′ ) ∈ Rfol implies dom(s) = dom(s′ ). We refer to TD as a system
instance of Tfol .
    Safety properties and inductive invariants are also specified by closed first-
order formulas over Σ. A safety specification φ induces a safety property P =
{s ∈ Sfol | s |= φ} for Tfol . With abuse of notation we will also consider P as a
safety property of TD for any domain D instead of writing P ∩ SD .


3    The Cutoff Method for First-Order Transition Systems

The standard first-order semantics Tfol of a transition system specification T is
often an abstraction of the intended semantics in the sense that it considers as
a state any first-order structure (that satisfies Γ ), whereas in many cases the
intended semantics only considers finite structures. In this section we define a
    6       Raz Lotan, Eden Frenkel and Sharon Shoham

1   sort node                                   9   relation termd(node)
2   immutable constant root : node             10   relation ack(node,node)
3   immutable relation leq(node,node)          11   init ¬termd(X)
4   axiom ∀X. leq(root,X) ∧ leq(X,X)           12   init ¬ack(X,Y)
5   axiom ∀X,Y. leq(X,Y) ∧ leq(Y,X) → X=Y      13
6   axiom ∀X,Y,Z. leq(X,Y) ∧ leq(Y,Z)          14   transition terminate(n: node)
                → leq(X,Z)                     15     assume ∀X. child(X,n) → ack(X,n)
7   axiom ∀X,Y,Z. leq(Y,X) ∧ leq(Z,X)          16     ∀X. termd’(X) = termd(X) ∨ (X = n)
                → leq(Y,Z) ∨ leq(Z,Y)          17     ∀X,Y. ack’(X,Y) = ack(X,Y) ∨ child(n,Y)
8   def child(Y,X) := leq(X,Y) ∧ X̸=Y ∧        18
               ∀Z.leq(Z,Y) ∧ Z̸=Y →leq(Z,X)    19   safety termd(root) → ∀X. termd(X)


              Fig. 1. First-order specification of the TreeTermination protocol.


    finite-domain semantics Tfin for T , where the size of states (structures) is finite
    but unbounded. The finite-domain semantics induces a parameterized system,
    where the parameter is the size of the (finite) domain. We then formulate the
    cutoff method, based on the notion of a size-reducing simulation, in the context
    of first-order transition systems, as a way of reducing safety verification of Tfin
    to safety verification of a bounded transition system, whose states are of size at
    most k.

    3.1    Finite-Domain Semantics of a First-Order Transition System
    The finite-domain semantics of a first-order specification of a transition system
    T is given by the transition system Tfin = (Sfin , Ifin , Rfin ) where Sfin , Ifin , Rfin are
    defined similarly to the corresponding definitions in Tfol , except that only finite
    domains are included. Note that a semantics that bounds the domain size by
    some k ∈ N can be captured with the standard first-order semantics by adding
    to Γ the formula size≤k := ∃x1 , . . . , xk .∀x. ∨i (x = xi ) as an axiom. However,
    the same cannot be done to capture the finite-domain semantics since finiteness
    of the domain is not definable in first-order logic.
        Every trace of Tfin is also a trace of Tfol . Hence, every safety property that
    is satisfied by Tfol is also satisfied by Tfin , but the converse need not hold, as
    demonstrated by the following example.

    Example 1 (TreeTermination). Consider a simple termination detection proto-
    col for nodes arranged in a rooted tree (which captures the second phase of a
    simple broadcast protocol [37]). Upon receiving an ack from all its children, a
    node terminates and sends an ack to its parent, except for the root, which does
    not have a parent. The protocol satisfies the safety property that if the root has
    declared termination then all nodes have terminated as well.
        A first-order specification of this protocol is given in Figure 1. The tree
    structure is modeled as proposed in [31], by a relation leq, axiomatized to induce
    a tree, with the intention that leq(X, Y) indicates that Y is a descendant of X
    in the tree. The axioms in example 1 ensure that leq is a partial order with the
    root as its minimum and example 1 guarantees the tree structure. The formula
    child(Y, X) indicates that Y is a child of X by asserting that X is a predecessor
    of Y in the order.
            Proving Cutoff Bounds for Safety Properties in First-Order Logic             7

                                       terminate(root)
   root ≤        ··· ≤      ≤                            root ≤       ··· ≤      ≤
            ∞                                                     ∞


Fig. 2. A counterexample to safety of TreeTermination over infinite structures, depicted
as a trace of two states related by the transition relation: the first is an initial state,
and the second violates safety. The order of nodes is depicted by ≤ and terminated
nodes are depicted by shading.


    For finite instances, the specification satisifies safety: any node X in the tree
is connected to the root by a finite sequence of predecessor steps. It follows by
induction on the length of this sequence that if the root terminated, so did X.
The induction step follows from the precondition of terminate, which ensures that
a node terminates only after its children sent it acks, and so already terminated.
    While this proof is correct, it uses induction on the length of tree paths,
and as a consequence, relies on the finiteness of the tree. In fact, if we allow
infinite structures, the safety property may be violated. A counterexample trace
for an infinite instance of the protocol is given in Figure 2. In the example, the
partial order is in fact a total order that consists of infinitely many nodes, all
of which are larger than the root, but for none the root is a predecessor. The
counterexample consists of a single step, where the root, which has no children
and therefore satisfies the pre-condition of the termination transition vacuously,
terminates, even though all the other nodes did not terminate.
    In the sequel, we develop an approach that mimics induction over the state
size and is able to verify the protocol for all finite instances by showing that
every instance with more than 2 nodes is simulated by an instance where some
node other than the root is deleted.


3.2   Establishing Cutoffs by Size-Reducing Simulations

To verify first-order transition systems under the finite-domain semantics, we
adapt the cutoff method to fit the first-order setting. Fix a first order specification
T , its corresponding transition systems {TD }D , its finite-domain semantics Tfin ,
a safety specification φ, and the induced safety property P . We define the notion
of a cutoff for Tfin and P as an adaptation of the standard definition [30].

Definition 1. A natural number k is a cutoff for Tfin and P if
                Tfin |= P       ⇐⇒      TD |= P for all D with |D| ≤ k.

    Generally speaking, cutoffs allow to reduce verification of parameterized sys-
tems to verification of bounded systems: if k is a cutoff, then it suffices to verify
TD for domains D with |D| ≤ k in order to deduce that Tfin |= P . Traditionally
(e.g., in [11]), cutoffs are investigated for classes of transition systems and proper-
ties. Since Definition 1 considers cutoffs for a specific specification of a transition
system and a specific safety property, a cutoff always exists: if Tfin |= P , then
TD |= P for any finite D, making any k a cutoff. Similarly, if Tfin ̸|= P , then there
8       Raz Lotan, Eden Frenkel and Sharon Shoham

exists a violating trace with some finite domain D, making k = |D| a cutoff. The
challenge our work addresses, and what makes cutoffs useful for verification, is
to establish a cutoff without checking whether Tfin |= P . To do so, we use the
notion of a size-reducing simulation.

Definition 2. A size-reducing simulation for Tfin , P and a bound k is a relation
H ⊆ Sfin × Sfin such that:

1. Size Reduction: For every pair (sh , sℓ ) ∈ H we have |sℓ | < |sh |.
2. Initiation: For every state sh ∈ Ifin with |sh | > k there exists sℓ ∈ Ifin such
   that (sh , sℓ ) ∈ H.
3. Simulation: For every pair (sh , sℓ ) ∈ H and sh′ ∈ Sfin such that (sh , sh′ ) ∈
   Rfin there exists sℓ′ ∈ Sfin such that (sh′ , sℓ′ ) ∈ H and (sℓ , sℓ′ ) ∈ Rfin
                                                                              ⋆
                                                                                  .
4. Fault Preservation: For every pair (sh , sℓ ) ∈ H, if sh ∈ / P then sℓ ∈   / P.

Usually (e.g., in [11,30]) simulation relations for showing cutoffs are defined
between different instances of the parameterized system. Instead, a size-reducing
simulation is a self-simulation of Tfin , which is more natural in this context.

Theorem 1. If H is a size-reducing simulation for Tfin , P and k, then k is a
cutoff for Tfin and P .

     Intuitively, the theorem holds because we can use H to translate a trace
violating P in system instances of (finite) size larger than k to a (perhaps short-
er/longer) trace violating P in a system instance with a smaller domain. Then,
continuing by induction, we get a violating trace of size smaller than k. Thus if
no counterexample to safety exists for system instances whose domain size is at
most k, no counterexample exists for Tfin , making k a cutoff.
     Our goal is to encode size-reducing simulations in first-order logic. As written,
items 2 and 3 involve alternation between universal and existential quantifica-
tion over states. Since states are first-order structures, explicitly quantifying over
them requires higher-order quantification. Note, however, that if a claim only in-
volves universal quantification over states, the quantification can remain implicit
by checking (first-order) validity. We use this observation to strengthen Defini-
tion 2 to a strong size-reducing simulation, by over-approximating the existential
quantification using universal quantification together with a totality requirement
that guarantees the universal quantification is not vacuous.
     Namely, the existential quantification specifies the existence of a state sℓ′
that simulates sh′ and is a successor of sℓ . When turning it into universal quan-
tification, we can either quantify over all successor states and require that they
are all simulating, or vice versa. We choose the latter option. We also strengthen
the requirement (sℓ , sℓ′ ) ∈ Rfin
                                 ⋆
                                    to (sℓ , sℓ′ ) ∈ Rfin or sℓ = sℓ′ , hence removing
the existential quantification on intermediate states. This is illustrated in Fig-
ure 3. The totality check then requires that a simulating state exists initially and
that it continues to hold inductively. These still involve existential quantification
over states, and we will see in the next section how to reduce them to first-order
quantification for the specific class of size-reducing relations that we use.
            Proving Cutoff Bounds for Safety Properties in First-Order Logic             9

                           R                                               R
 Definition 2      sh             sh′            Definition 3      sh              sh′

                 H                  H                            H                   H
                              ⋆                                               =
                          R                                               R
                     sℓ           sℓ′ ∃                              sℓ            sℓ′

Fig. 3. Strengthening of simulation to strong simulation: solid nodes are universally
quantified while the dashed node is existentially quantified; solid edges represent as-
sumptions and dashed edges represent conclusions. R= is a shorthand for R ∪ idS .


Definition 3. A strong size-reducing simulation for Tfin , P and k is a relation
H ⊆ Sfin × Sfin such that:
1. Size Reduction: For every pair (sh , sℓ ) ∈ H we have |sℓ | < |sh |.
2. Strong Initiation: For every pair (sh , sℓ ) ∈ H, if sh ∈ Ifin then sℓ ∈ Ifin .
3. Strong Simulation: For all pairs (sh , sℓ ) ∈ H and (sh′ , sℓ′ ) ∈ H, if (sh , sh′ ) ∈
   Rfin and dom(sℓ ) = dom(sℓ′ ) then (sℓ , sℓ′ ) ∈ Rfin or sℓ = sℓ′ .
4. Fault Preservation: For every pair (sh , sℓ ) ∈ H, if sh ∈ / P then sℓ ∈  / P.
5. Inductive Totality:
    – For every sh ∈ Ifin with |sh | > k there exists sℓ ∈ Sfin s.t. (sh , sℓ ) ∈ H.
    – For every pair (sh , sh′ ) ∈ Rfin , if there exists sℓ s.t. (sh , sℓ ) ∈ H then
       there exists sℓ′ ∈ Sfin s.t. (sh′ , sℓ′ ) ∈ H and dom(sℓ ) = dom(sℓ′ ).
    Note that in the strong simulation requirement we do not consider all states
sℓ′ that simulate sℓ but only those that have dom(sℓ ) = dom(sℓ′ ), since each
trace is confined to one system instance. As a result, we also need to require the
domain equality in the totality of item 5.
Lemma 1. A strong size-reducing simulation is a size-reducing simulation.
    The converse of Lemma 1 does not hold. In fact, a transition system may
have a size-reducing simulation but no strong size-reducing simulation. Moreover,
while size-reducing simulations are as powerful as inductive invariants as a proof
rule [30], the proof does not carry over to strong size-reducing simulations.

4    First-Order Encoding of Size-Reducing Simulations
In this section we show how to encode and validate a strong size-reducing sim-
ulation in first-order logic. To circumvent the need to express and verify size
reduction in first-order logic, we consider a certain class of strong size-reducing
simulations, where the pairs (sh , sℓ ) in the relation are such that sℓ is obtained
from sh by deleting an element in its domain and updating the interpretation of
all symbols. We propose a first-order encoding of such relations and show how
to validate that the relation defined by this encoding is a strong size-reducing
simulation using a set of verification conditions expressible in first-order logic.
    For the remainder of the section, fix a first-order specification T = (Σ, Γ, ι, τ ),
a safety specification φ and a natural number k. Let Tfin be the finite-domain
semantics associated with T and P the safety property associated with φ.
10      Raz Lotan, Eden Frenkel and Sharon Shoham

4.1    Encoding Size-Reducing Relations Using Substructures
A strong size-reducing simulation is a relation between states that satisfies cer-
tain requirements. To specify a relation between states (structures) we rely on
the standard approach of using a formula over a double vocabulary Σ h ⊎ Σ ℓ ,
where the interpretation of Σ h represents the “high” state sh , and the interpre-
tation of Σ ℓ represents the “low” state sℓ . However, since a model of a formula
(even when it is a two-vocabulary formula) has a single domain, such an encod-
ing does not account for size reduction of the domain. Our observation is that
we can enforce size reduction by deleting an element from the domain. Thus,
we use a formula η(z) over Σ h ⊎ Σ ℓ to specify a size-reducing relation, where
the deleted element is specified using the free variable z. In a model of η(z),
the interpretation of Σ h represents sh and the state sℓ is a substructure of the
interpretation of Σ ℓ with the same domain elements as sh , excluding the element
assigned to z. We formalize this by the following definition.
Definition 4. Let η(z) be a formula over Σ h ⊎ Σ ℓ , (D, I h ⊎ I ℓ ) a structure over
Σ h ⊎ Σ ℓ and d0 ∈ D such that (D, I h ⊎ I ℓ ), [z 7→ d0 ] |= η(z). Then for D× =
                                              ℓ                  ℓ
D \{d0 }, if there exists an interpretation I×  such that (D× , I× ) is a substructure
of (D, I ℓ ), we say that sℓ = (D× , I×
                                      ℓ
                                        ) is an η-substructure of sh = (D, I h ). The
size-reducing relation of η is the relation
    Hη = (sh , sℓ ) ∈ struct(Σ) × struct(Σ) | sℓ is an η-substructure of sh .
            

An example of a pair (sh , sℓ ) ∈ Hη is depicted in Figure 4 along with the
structure (D, I h ⊎ I ℓ ) and the element d0 ∈ D that induces them, assuming
that (D, I h ⊎ I ℓ ), [z 7→ d0 ] |= η(z). In the example: D = {1, 2, 3, 4}, d0 =
3, I h = {leq : {(1, 2), (1, 3), (3, 4), (1, 4)}, root : 1, ack : {(4, 3)}, termd : {4}} and
I ℓ = {leq : {(1, 2), (1, 3), (3, 4), (1, 4)}, root : 1, ack : {(4, 1)}, termd : {4}}. This
induces the pair (sh , sℓ ) ∈ Hη where sh = (D, I h ), sℓ = (D× , I×      ℓ
                                                                            ), D× = {1, 2, 4}
       ℓ
and I× = {leq : {(1, 2), (1, 4)}, root : 1, ack : {(4, 1)}, termd : {4}}. The choice
d0 = 4 would give a different pair in Hη .
Lemma 2. For a formula η(z) over Σ h ⊎ Σ ℓ , and a pair (sh , sℓ ) ∈ Hη such that
sh is finite, we have |sℓ | < |sh |.
    Lemma 2 states that, when restricting to finite structures, Hη is size-reducing.
This holds by construction. In the sequel, we define a set of verification conditions
that guarantee the rest of the required properties of Definition 3.
    In order to encode the verification conditions, we need to be able to reason
about the states (sh , sℓ ) ∈ Hη . The state sh is captured by η(z) directly. However,
sℓ is defined by a substructure that excludes the element assigned to z from the
domain of η(z). As a result, we need to exclude z when reasoning about sℓ .
For this purpose, we define, for a formula α and a variable z ∈        / Vars(α), the
z-excluded representation, denoted [α]\z . The z-excluded representation is the
formula obtained from α by adding to each quantifier a guard that excludes z.
This ensures that the evaluation of [α]\z on a structure with domain D with z
assigned to d0 ∈ D is the same as the evaluation of α on a substructure with
domain D \ {d0 } (if such a substructure exists, see Section 4.3).
              Proving Cutoff Bounds for Safety Properties in First-Order Logic            11


                                                    sh                        ack
                                                                       3              4


                                                     root   1
  s
              z            ackh
                     3              4                                  2


  root    1                ackℓ
                                                    sℓ
                     2                                                                4


                                                     root   1                  ack

                                                                       2


Fig. 4. Left: a structure s = (D, I h ⊎ I ℓ ) and an assignment [z 7→ d0 ] that satisfy
η(z). The h and ℓ copies of root, leq and termd are interpreted in the same way, so
these interpretations are depicted jointly. leq(·, ·) is depicted by solid lines and termd(·)
is depicted by shading. The interpretation of the two copies of ack(·, ·) are depicted by
dashed and dotted arrows. Right: the derived high and low structures: sh = (D, I h )
and sℓ = (D× , I×ℓ
                   ), with the relations and constants depicted in the same way.


Definition 5. For a formula α and a variable z ∈    / Vars(α), the z-excluded rep-
resentation of α, denoted [α]\z , is a formula defined inductively as follows:
 – [α]\z = α if α = r(t1 , . . . , tm ) or α = (t1 = t2 )
 – [¬β]\z = ¬[β]\z
 – [β1 ▷◁ β2 ]\z = [β1 ]\z ▷◁ [β2 ]\z for ▷◁ ∈ {∧, ∨, →}
 – [∀x.β]\z = ∀x.(x ̸= z) → [β]\z
 – [∃x.β]\z = ∃x.(x ̸= z) ∧ [β]\z
    The following lemma formalizes the aforementioned relation between the
value of the z-excluded representation of α in a structure and the value of α
in its substructure that excludes the value of z.
Lemma 3. Let α be a closed formula over Σ and z ∈     / Vars(α) a variable. Let
(D, I) be a structure for Σ, d0 ∈ D and (D× , I× ) a substructure of (D, I) such
that D× = D \ {d0 }. Then (D× , I× ) |= α ⇐⇒ (D, I), [z 7→ d0 ] |= [α]\z .

4.2    Validating Simulation
Given a formula η(z) over Σ h ⊎ Σ ℓ , we now go on to define a set of verification
conditions for T , φ, k and η(z) that ensure that Hη ∩ (Sfin × Sfin ) is a strong
12      Raz Lotan, Eden Frenkel and Sharon Shoham

       (1)     Γ h ∧ ιh ∧ η(z) =⇒ [ι]ℓ\z                            [ι-preservation]
       (2)     Γ h ∧ Γ h′ ∧ η(z) ∧ η ′ (z) ∧ τ h =⇒ [τ ∨ idΣ ]ℓ\z   [τ -preservation]
       (3)     Γ h ∧ ¬φh ∧ η(z) =⇒ [¬φ]ℓ\z                          [¬φ-preservation]
       (4)     Γ h ∧ η(z) =⇒ closureΣ (z)ℓ                          [projectability]
       (5)     Γ h ∧ η(z) =⇒ [Γ ]ℓ\z                                [Γ -preservation]
       (6)     Γ h ∧ ιh ∧ size>k =⇒ ∃z.θ(z)                         [θ-initation]
       (7)     Γ h ∧ Γ h′ ∧ θ(z) ∧ τ h =⇒ θ′ (z)                    [θ-consecution]

Fig. 5. Verification conditions establishing strong size-reducing simulation for a high-
low update η(z) with precondition θ(z), T = (Σ, Γ, ι, τ ), φ and k.


size-reducing simulation for Tfin , P and k. The full set of verification conditions
is listed in Figure 5. In this subsection we introduce three of them, which guar-
antee strong initiation, strong simulation and fault preservation (items 2 to 4 of
Definition 3). Having already ensured size reduction (item 1) in Lemma 2, the
next subsection addresses the final requirement: inductive totality (item 5).
     In all verification conditions, we use the appropriate copies of the vocabulary
to refer to high states (Σ h ) and low states (Σ ℓ ) and to pre-states (unprimed) and
post-states (primed). We use η(z) to encode pairs of states related by simulation
and the z-excluded representation to encode properties of the low state in a pair.
For this purpose, we assume w.l.o.g. that the variable z does not appear in the
system and safety specification Γ, ι, τ, φ (this can be achieved by renaming).
     Verification conditions (1) and (3) are straight forward encodings of strong
initiation and fault preservation, respectively.
     Verification condition (2) establishes strong simulation. It requires that any
transition between high-states is reflected by a transition between their simu-
lating low states or by a stutter, provided that the low states have the same
domain. The assumption that the high and low states are related by the simula-
tion relation is encoded by asserting η(z) (for the pre-states) and η ′ (z) (for the
post-states). Crucially, we use the same variable z to ensure that we refer to low
states with
         V the same domain. We encode         a stutter by the formula idΣ given by
idΣ := r∈Σ (∀x. r′ (x) ↔ r(x)) ∧ f ∈Σ (∀x. f ′ (x) = f (x)).
                                       V

Lemma 4. Let η(z) be a formula over Σ h ⊎Σ ℓ . If verification conditions (1)–(3)
of Figure 5 are valid then Hη ∩ (Sfin × Sfin ) satisfies items 2 to 4 of Definition 3.

4.3   Guaranteeing and Validating Totality
So far, we have considered an arbitrary formula η(z). We now define a syntactic
restriction on η(z), that, along with four verification conditions, guarantees that
the induced size-reducing relation Hη ∩ (Sfin × Sfin ) is inductively total (item 5 of
Definition 3). Namely, we consider formulas η(z) that consist of a precondition
θ(z) and update formulas for all the symbols in the vocabulary. For such formu-
las, called high-low updates, we show how to encode the remaining existential
quantification over states in the definition of inductive totality by first-order
quantification.
            Proving Cutoff Bounds for Safety Properties in First-Order Logic         13

Definition 6. A formula η(z) over the vocabulary Σ h ⊎Σ ℓ is a high-low update
if it has the form:
                    ^                        ^
                      ∀x. rℓ (x) ↔ αr (x, z) ∧      ∀x. f ℓ (x) = tf (x, z)
                                                                           
      η(z) = θ(z) ∧
                    r∈Σ                              f ∈Σ


where θ(z) is a formula over Σ h , for every relation symbol r ∈ Σ of arity m, αr
is a formula over Σ h with m + 1 free variables, and for every function symbol
f ∈ Σ with arity m, tf is a term over Σ h with m + 1 free variables. We call θ
the precondition for η, each αr the update formula for r and each tf the update
term for f .

    Intuitively, for a high-low update η(z) with precondition θ(z), to any high
state and assignment to z that satisfies the precondition θ(z), η(z) defines the
low state as a deterministic update from the high state, according to the formu-
las αr and terms tf . For example, we can use θ(z) to specify that the deleted
element must be different from all constants, and we can update all relation and
function symbols to their values in the high state (we refer to this as a trivial
update). However, since the low state is obtained by deleting an element, we still
need to make sure that, after the deletion, the updates result in a well-defined
substructure, and, furthermore, that the structure is in fact a state (satisfies Γ ).
This is done by additional verification conditions. First, we formalize the precise
guarantee of a high-low update:

Lemma 5. Let η(z) be a high-low update with precondition θ(z) and (D, I h ) a
structure with d0 ∈ D such that (D, I h ), [z 7→ d0 ] |= θ(z). Then there exists an
interpretation I ℓ such that (D, I h ⊎ I ℓ ), [z 7→ d0 ] |= η(z).

    The lemma states that whenever the high-state satisfies θ(z) for some value of
z, there exists I ℓ such that η(z) holds. By Definition 4, to obtain the simulating
state of the high-state, we then take a substructure which excludes the assigned
value of z. To ensure that a substructure can be obtained in this way, we must
verify that for any function symbol f , its interpretation remains a total function
when we restrict its domain and range by discarding the assigned value of z.
To ensure that a state is obtained, we further need to verify that the resulting
substructure satisfies the axioms. These properties V     are guaranteed by verification
conditions (4) and (5), where closureΣ (z) := f ∈Σ closedf (z) and closedf (z) :=
∀x. (∧m i=1 xi ̸= z) → f (x) ̸= z.
    If the aforementioned verification conditions hold, we know that any high
state that satisfies θ(z) has a corresponding low state in Hη ∩ (Sfin × Sfin ).
To guarantee inductively totality it remains to ensure that the precondition
θ(z) holds over appropriate high states. Verification condition (6) requires that
for all initial high states with size larger than k there exists z such that θ(z)
holds (note the existential quantification). The size constraint is encoded by
size>k := ∃x1 , . . . , xk+1 . ∧i,j xi ̸= xj . Verification condition (7) ensures that
totality is maintained over transitions between high states by requiring that
θ(z) is maintained, i.e., if θ(z) holds, then so does θ′ (z). To ensure that the low
14      Raz Lotan, Eden Frenkel and Sharon Shoham

states corresponding to the high pre-state and the high post-state have the same
domain, we use the same variable z in θ(z) and θ′ (z). This ensures that we can
delete the same element that is deleted in the pre-state in the post state, leading
to the same domain.
Lemma 6. Let η(z) be a high-low update with precondition θ(z), if verification
conditions (4)–(7) of Figure 5 are valid, then Hη ∩ (Sfin × Sfin ) satisfies item 5
of Definition 3.
Remark 1. The main role of θ(z) is to specify the deleted element in a high state
in a simulation pair. However, it can also be used to restrict the high states, which
may be necessary to make verification conditions (2)–(5) valid. This can be done
by conjoining to the deletion condition in θ(z) a closed formula over Σ h that
serves as an invariant. In this case, the inductive totality checks verify that the
invariant is inductive, ensuring soundness of the restriction.

4.4   Putting It All Together
The following theorem summarizes the soundness of the first-order encoding of
a strong size-reducing simulation by a high-low update.
Theorem 2. If all the verification conditions for a high-low update η(z), T ,
φ and k (Figure 5) are valid, then Hη ∩ (Sfin × Sfin ) is a strong size-reducing
simulation for Tfin , P and k. Consequently, k is a cutoff for Tfin and P .

Back to Example 1. Figure 6 encodes a high-low update that induces a size-
reducing simulation for establishing a cutoff of 2 for the TreeTermination proto-
col (Example 1). In this example, violation of safety is witnessed by a node that
did not terminate even though the root terminated. To allow the high-low update
to refer to the node inspected by the property, we first Skolemize the negated
safety property into termd(root) ∧ ¬termd(nsk ), where nsk is a fresh immutable
constant that is added to the first-order specification of the transition system.
The original transition system violates the universally quantified safety property
if and only if the transition system augmented with nsk violates the Skolemized
property. (A similar Skolemization is performed in all of our examples.) The
precondition of the high-low update is then: θ(z) = (z ̸= nsk h ∧ z ̸= rooth ), i.e.,
the deleted element z is required to be different than both the root and the vio-
lating node nsk , which ensures fault preservation. The update of the ack relation
is specified by the formula αack , which says that messages bypass the deleted
node. The other updates are trivial and thus not specified in Figure 6. αack and
the resulting high-low update are given below.

αack (x, y, z) = (ackh (x, y) ∧ x ̸= z ∧ y ̸= z)
              ∨ (ackh (x, z) ∧ childh (z, y)) ∨ (childh (x, z) ∧ ackh (z, y))
 η(z) = θ(z) ∧ (∀x, y. leqℓ (x, y) ↔ leqh (x, y)) ∧ (∀x. termdℓ (x) ↔ termdh (x))
              ∧ (∀x, y. ackℓ (x, y) ↔ αack (x, y, z)) ∧ (rootℓ = rooth ) ∧ (nsk ℓ = nsk h )
                 Proving Cutoff Bounds for Safety Properties in First-Order Logic          15


1   bound node 2       # default value
2   condition(z: node) = z ̸= nsk ∧ z ̸= root        # default formula
3   update ack(x: node, y: node, z: node) =
4       (ack(x,y) ∧ x ̸= z ∧ y ̸= z) ∨ (ack(x,z) ∧ child(z,y)) ∨ (child(x,z) ∧ ack(z,y))
5   hint terminate(nh : node, nℓ : node, z: node) = (nℓ = nh )



                     Fig. 6. Encoding of a high-low update for Example 1.



        The structure in the left of Figure 4 is an example of a model for η(z) (the
    Skolem constant, which is omitted from Figure 4, can be interpreted to any
    node other than node 3). With this definition of a high-low update, all the
    verification conditions are valid. To see that τ -preservation holds, consider a
    transition terminate(n) in the high state. If n is equal to the deleted node z,
    all changes made by the transition are lost in the projection, so the transition
    is simulated by a stutter in the low state. If n ̸= z, the transition is simulated
    by terminate(n) in the low states: if z is a child of n, then the updates to ack
    guarantee that the precondition for the transition still holds in the low state; if
    z is the parent of n, the updates to ack guarantee that the updated post-state is
    indeed the post-state of the transition; finally, if z is not a child nor a parent of n,
    the simulation is clear. We emphasize that when using our approach, validating
    the verification conditions for the given high-low update is delegated to an SMT
    solver (see Section 5.1 for explanation of the hint in Figure 6).


    4.5    Extension to a Many-Sorted Vocabulary

    We considered a single sort in the vocabulary used to specify T , which the finite-
    domain semantics treats as finite but unbounded. Our approach generalizes to
    transition systems specified using many-sorted first-order logic, including inter-
    preted sorts and symbols. In this case, the finite-domain semantics affects only
    the sorts that are designated as finite. The finite sorts and corresponding symbols
    are required to be uninterpreted, which means that they may only be restricted
    by a finitely-axiomatizable background theory (e.g., the theory of rooted trees
    as in Example 1). Other sorts and symbols may be interpreted, i.e., defined by
    arbitrary background theories, including ones that are not finitely-axiomatizable
    (e.g., linear integer arithmetic).
        To handle multiple finite sorts, we apply our approach iteratively, each time
    establishing a cutoff for a single finite sort s by finding a size-reducing simulation
    for that sort. When proving a cutoff for s, we define the cardinality of a structure
    as the cardinality of D(s), and replace D with D(s) in the definition of a cutoff
    and size-reducing simulation. The variable z used as a free variable in a high-low
    update is of sort s, and in the definition of Hη we define D× (s) = D(s) \ {d0 }.
    Finally, in the definition of a z-excluded representation and closedf (z) we add the
    guard x ̸= z only for variables x of the sort s. Then, when moving on to establish
    a cutoff for the next sort we restrict the cardinality of s to the established cutoff
    bound using the axiom size≤k . In some cases, the order in which we apply our
16      Raz Lotan, Eden Frenkel and Sharon Shoham

method matters. Specifically, when we have a function f from finite sort s1 to
finite sort s2 , it is natural to first show a cutoff for s1 .


5     Implementation and Evaluation

5.1   Implementation

The implementation of our method, which is available at [26], is built on top of
the open-source verification tool mypyvy [42]. mypyvy allows a user to provide a
first-order specification of a transition system T and a safety property φ. To run
our tool, the user additionally provides a cutoff bound for one of the system’s
sorts, as well as a high-low update specified as a deletion condition for θ(z) along
with update formulas and terms for relation and function symbols (Definition  V     6).
When omitted, the deletion condition is assigned the default formula c z ̸= c
where c ranges over the immutable constants, including Skolem constants, and
the cutoff bound is assigned the number of immutable constants. Similarly, for
an update term the default is αr (xh , z) = rh (xh ) and for an update formula the
default is tf (xh , z) = f h (xh ). Invariants of the system can also be provided, and
are conjoined to θ(z) as described in Remark 1. For instance, the user input for
Example 1 is given in Figure 6. Our tool generates the verification conditions
described in Figure 5 and validates them using the SMT solver Z3 [28]. If Z3
establishes that some verification condition is invalid, it generates a counterex-
ample, which is a model of the negated verification condition. In such cases, the
counterexample can point the user towards finding an appropriate fix for the
high-low update.

Optimizations. Of the verification conditions in Figure 5, item (2) is the most
challenging for the solver. This is because τ often has an ∃∗ prefix (quantifying
over transition arguments) followed by nested quantifiers, as can be seen in Ex-
ample 1. Since τ appears on both sides of the implication in verification condition
(2), quantifier alternations are introduced, which are difficult for SMT solvers to
handle. To expedite this check, we split it into a separate check for each transi-
tion (disjunct) of τ , strengthening the simulation requirement. Furthermore, we
let the user provide hints for the existential quantifiers (arguments) on the right-
hand side of the implication, as described next. Generally speaking, the queries
of verification condition (2) have the form (∃xh .α(xh , z)) =⇒ (∃xℓ .β(xℓ , z)),
where α and β are potentially complicated formulas with nested quantifiers. We
propose verifying the above using a user-provided hint γ(xh , xℓ , z) that satisifies
  – totality: α(xh , z) =⇒ ∃xℓ .γ(xh , xℓ , z),
  – sufficiency: α(xh , z) ∧ γ(xh , xℓ , z) =⇒ β(xℓ , z).
In this way we break the query into two, eliminating the existential quantification
over β(xℓ , z), and introducing one over γ(xh , xℓ , z). The idea is for γ(xh , xℓ , z)
to be much simpler than β(xh , z), which reduces the number of quantifier al-
ternations and significantly improves performance. In some cases we use hints
of the form γ(xh , xℓ , z) = (xℓ = t(xh , z)), where t(xh , z) are terms. In such
           Proving Cutoff Bounds for Safety Properties in First-Order Logic       17

                           Table 1. Summary of Results.

Example         Sorts & Semantics                  Cutoff    Updates Inv. Hints
TreeTermination node: fin                          node: 2     1/3    ✓ 1/1
EchoMachine     round: fin, value: fin             round: 3    0/3    ✓ 0/2
                round: 3, value: fin               value: 2    0/3    × 0/2
ToyConsensus    value: fin, quorum: fin, node: fin value: 2    1/3    ✓ 0/2
                value: 2, quorum: fin, node: fin quorum: 2 0/3        × 0/2
                value: 2, quorum: 2, node: fin     node: 4     0/3    × 1/2
LockServer      node: fin                          node: 2     1/5    ✓ 0/5
ListToken       node: fin                          node: 3     2/7    ✓ 1/3
PlusMinus       thread: fin, int                   thread: 1   1/3    ✓ 0/2
EqualSum        thread: fin, index: fin, int       thread: 2   0/8    × 0/1
                thread: 2, index: fin, int         index: 2    3/8    ✓ 0/1
EqualSumOrders thread: fin, index: fin, int        thread: 2   0/8    × 0/1
                thread: 2, index: fin, int         index: 4    3/8    ✓ 0/1


cases, totality is trivial and we have completely eliminated the existential quan-
tification. In the TreeTermination example we give a hint of this form for the
transition terminate, see Figure 6. The hint says that the transition terminate in
high states with argument nh is simulated in low states by the same argument,
nℓ = nh (or by a stutter).

5.2   Results
We evaluate our approach on examples from various previous works, listed in Ta-
ble 1. We use mypyvy with Z3 version 4.12.2.0, run on a laptop running Windows,
with a Core-i7 2.8 GHz CPU. All run-times are under 10 seconds.
    Table 1 summarizes our results. Each row describes one example. As de-
scribed in Section 4.5, for transition systems with multiple finite sorts we apply
our approach iteratively, in which case each iteration is described using a sepa-
rate row in the order of application. For each example, the columns list its sorts
and their semantics, the sort for which we show a cutoff together with the cutoff
bound, how many relation and function symbols are given update terms and
formulas (instead of using default values), whether an invariant is given, and
how many transitions are given hints. For all examples the default formula for
the deletion condition is used. In the sorts column, “s : fin” indicates that s is an
uninterpreted sort with the finite-domain semantics, “s : k” indicates that s is
an uninterpreted sort with the bounded semantics with bound k (this is encoded
by the axiom size≤k ), and “int” stands for the interpreted integer sort.
     Next, we briefly describe each of the examples.
     TreeTermination. Our motivating example from Example 1, originally from [37].
Crucially, this example cannot be proved by means of an inductive invariant as
it is only safe under the finite-domain semantics.
     EchoMachine. Taken from [9]. A simple distributed protocol where values
are echoed in rounds which are linearly ordered. A value may be echoed in some
18      Raz Lotan, Eden Frenkel and Sharon Shoham

round if there exists some previous round that echoed it. The safety property is
that the value echoed in all rounds is unique. [9] shows a simple inductive invari-
ant that implies safety over finite structures but not in the first-order semantics;
we use the same invariant in a high-low update to establish safety.
     ToyConsensus. Taken from [39]. A simple consensus protocol with three finite
sorts, including sort quorum, which is axiomatized to ensure a nonempty inter-
section for any two quorums. We highlight this example as an example where
the order of application on sorts matters. Specifically, after we show a cutoff of
2 for the sort quorum, we can instantiate the quorum intersection axiom and
Skolemize the node in the intersection of any pair of quorums, giving 4 Skolem
constants. We can then freely delete any other node.
     LockServer. Taken from [33]. A simple mutual exclusion protocol. In this
example, our approach does not simplify the proof since to prove simulation the
high-low update must include an invariant that suffices to prove safety directly.
     ListToken. A custom example where a token travels along a linked list, mod-
eled with a next relation. An invariant that proves safety would require talking
about the transitive closure of next, which cannot be done in FOL. Instead, our
approach based on simulation avoids the need to reason about the transitive
closure. The high-low update changes the next relation to skip over the deleted
node, and moves the token accordingly.
     PlusMinus. Taken from [18]. A simple concurrent program where any number
of threads each move between two program locations, incrementing and then
decrementing a shared counter, which must always remain non-negative. In [18],
it is shown that no Ashcroft invariant proves its safety. Intuitively, an inductive
invariant would need to count the number of threads in some program location,
which is problematic in FOL. Instead, the high-low update undoes increments
to the counter by the deleted thread.
     EqualSum. Taken from [14]. A simple concurrent program where threads
sum over elements of an array. The safety property is that any two threads that
terminate hold the same sum. An inductive invariant would need to record sums
of array segments of unbounded length, which is not clear how to express in FOL.
Our approach easily establishes a cutoff of 2 for sort thread. Then, to establish a
cutoff for sort index, the high-low update deletes an array element and subtracts
it from the sum of any thread pointing to a higher index.
     EqualSumOrders. A variant of EqualSum where every thread holds a different
order on the indices of the array. Unlike EqualSum, in this variant the order of
application of our method on the sorts matters. To prove the cutoff for sort index
we use a similar Skolemization to the one used in ToyConsensus.

Limitations. While our approach is applicable to some examples that cannot be
verified by previous approaches, it has limitations. The definition of a high-low
update does not specify how the state should be updated to obtain a simulation
relation. In our examples, we used the high-low update to undo all changes that
involved the deleted element z in all transitions so far. In this way, transitions
that are completely undone are simulated by stutters. For some examples, it is
hard to keep track of the changes that need to be undone, and it requires some
           Proving Cutoff Bounds for Safety Properties in First-Order Logic       19

instrumentation. For example, in the ToyConsensus example, when a value is
chosen by some quorum we change the model to keep track of the quorum that
chose it, and not only the fact that it was chosen. In some cases, undoing the
changes that involved z causes transitions of other elements to be impossible
to simulate, for example, if the transition has a guard on some global variable,
affected by z.

6   Related Work
Parameterized verification of safety properties is a widely-researched problem.
Many works [12,16,17,18,25,35,43] have developed techniques to infer inductive
invariants for parameterized systems in first-order logic. Such techniques are
bound to fail if no satisfactory invariant exists in the language considered, or if
the system is only safe in the finite instances. Our approach is deductive and
based on the notion of cutoffs [1,3,10,11,21,22,23,27,30,40,41]. Most cutoff results
guarantee that a cutoff always exists for a class of systems and properties. In turn,
the system specification is much more limited. Our work proposes a framework
for establishing cutoffs for a specific first-order transition system and property.
Next we focus on the works closest to ours.

Cutoffs by Simulation Relations. In [5], the cutoff method is utilized for safety
verification of distributed protocols specified in FOL. They automatically gen-
erate and check a simulation relation between an arbitrary system instance and
a cutoff instance.We, on the other hand, encode a simulation relation between
system instances that differ in size by 1, and not directly to the cutoff instance.
In this way, our work captures an inductive argument over the state size, which
lets it capture the finite-domain semantics. In contrast, [5] cannot verify exam-
ples such as Example 1 that are only correct in finite instances. Additionally, the
simulation relation in [5] is defined by mapping all elements in any instance to
the elements of the cutoff instance such that transitions are preserved, while we
use a partial mapping of elements with updates that allow to undo transitions.
Relying on a fixed total mapping of elements is bound to fail in examples such
as PlusMinus, where threads move between program locations. In [8], a cutoff
result is given for a parameterized mutual-exclusion protocol by giving a simu-
lation relation between system instances that differ in size by 1. Their proof of
simulation is manual, and uses an unbounded number of steps, which cannot be
automated by an SMT solver. [19] formulates the notion of a simulation-inducing
squeezer for safety properties, which is essentially a deterministic size-reducing
simulation with a slightly weaker notion of stuttering. This work is evaluated
only on deterministic sequential array programs and cannot capture transition
systems defined in FOL. Other works [6,7] automatically generate proofs for
program assertions by induction on some size parameter. These methods are
currently limited to programs manipulating arrays.

Mitigating Limitations of FOL. [4,20,31,32,39,38] use the Effectively Proposi-
tional (EPR) [36] decidable logic of FOL to model and verify transition systems.
20     Raz Lotan, Eden Frenkel and Sharon Shoham

EPR has the finite-model property: any satisfiable formula has a finite model. In
the case of safety verification, this has the effect of capturing the finite-domain
semantics. However, it is not always clear how to ensure that the verification con-
ditions are in EPR. When the verification conditions are outside of EPR, as in
Example 1, infinite models may arise. [9] finds such models and shows that they
can sometimes be eliminated by induction axioms. [29] develops an approach
for automatically generating induction axioms for systems modeled using alge-
braic data-types. [2] takes an alternative approach to modeling systems in FOL,
separating the specification of topology from the specification of the protocol.

Mitigating Limitations of Inductive Invariants. In [14], programs whose induc-
tive invariants are not expressible in FOL (or are too complex) are verified by
finding an inductive invariant for a reduction of the program obtained by re-
ordering execution steps, relying on commutativity. Counting Proofs [13] create
proofs that keep track of the number of threads that satisfy some properties,
akin to examples like PlusMinus.


7    Conclusion
We have presented a framework for specifying and validating size-reducing sim-
ulations in first-order logic as a way to establish cutoffs for the finite-domain
semantics of first-order transition systems. Size-reducing simulations mimic in-
duction over the domain size, which is sometimes simpler than induction over
time, and, notably, leverages the finite-domain semantics.
    As our evaluation shows, our framework manages to verify some examples
that cannot be verified by previous approaches. We leave automating the search
for a high-low update to future work. In this context we note that without hints
our verification conditions are not in EPR, and therefore SMT solvers sometimes
struggle to find models when a query is not valid, which might be an obstacle
for automation.
    It is possible to extend our approach to a larger class of size-reducing sim-
ulations, e.g., by allowing to delete more than one domain element, or relax-
ing the deterministic updates to other syntactic restrictions that still guarantee
Lemma 5. We did not find such extensions necessary in the examples we con-
sidered. Another interesting direction for future research is to consider a wider
range of properties, including liveness properties. While the definition of a size-
reducing simulation can be extended naturally, the more intricate structure of
traces that satisfy liveness properties seems to be a challenge.

Acknowledgement We thank Neta Elad, Shachar Itzhaky and Orna Grumberg
for helpful advice. The research leading to these results has received funding
from the European Research Council under the European Union’s Horizon 2020
research and innovation programme (grant agreement No [759102-SVIS]). This
research was partially supported by the Israeli Science Foundation (ISF) grant
No. 2117/23.
            Proving Cutoff Bounds for Safety Properties in First-Order Logic           21

References
 1. Abdulla, P., Haziza, F., Holík, L.: Parameterized verification through view ab-
    straction. Int. J. Softw. Tools Technol. Transf. 18(5), 495–516 (oct 2016). https:
    //doi.org/10.1007/s10009-015-0406-x
 2. Ashmore, R., Gurfinkel, A., Trefler, R.J.: Local reasoning for parameterized first or-
    der protocols. In: NASA Formal Methods - 11th International Symposium, NFM
    2019, Houston, TX, USA, May 7-9, 2019, Proceedings. Lecture Notes in Com-
    puter Science, vol. 11460, pp. 36–53. Springer (2019). https://doi.org/10.1007/
    978-3-030-20652-9_3
 3. Außerlechner, S., Jacobs, S., Khalimov, A.: Tight cutoffs for guarded protocols
    with fairness. In: Verification, Model Checking, and Abstract Interpretation - 17th
    International Conference, VMCAI 2016, St. Petersburg, FL, USA, January 17-19,
    2016. Proceedings. Lecture Notes in Computer Science, vol. 9583, pp. 476–494.
    Springer (2016). https://doi.org/10.1007/978-3-662-49122-5_23
 4. Ball, T., Bjørner, N., Gember, A., Itzhaky, S., Karbyshev, A., Sagiv, M., Schapira,
    M., Valadarsky, A.: Vericon: towards verifying controller programs in software-
    defined networks. SIGPLAN Not. 49(6), 282–293 (jun 2014). https://doi.org/
    10.1145/2666356.2594317
 5. Bhat, S.G., Nagar, K.: Automating cutoff-based verification of distributed proto-
    cols. In: 2023 Formal Methods in Computer-Aided Design (FMCAD). pp. 75–85
    (2023). https://doi.org/10.34727/2023/isbn.978-3-85448-060-0{_}15
 6. Chakraborty, S., Gupta, A., Unadkat, D.: Diffy: Inductive reasoning of array pro-
    grams using difference invariants. In: Computer Aided Verification - 33rd Interna-
    tional Conference, CAV 2021, Virtual Event, July 20-23, 2021, Proceedings, Part
    II. Lecture Notes in Computer Science, vol. 12760, pp. 911–935. Springer (2021).
    https://doi.org/10.1007/978-3-030-81688-9_42
 7. Chakraborty, S., Gupta, A., Unadkat, D.: Full-program induction: verifying array
    programs sans loop invariants. Int. J. Softw. Tools Technol. Transf. 24(5), 843–888
    (2022). https://doi.org/10.1007/S10009-022-00676-W
 8. Clarke, E.M., Grumberg, O., Browne, M.C.: Reasoning about networks with many
    identical finite-state processes. In: Proceedings of the Fifth Annual ACM Sym-
    posium on Principles of Distributed Computing. p. 240–248. PODC ’86, Associ-
    ation for Computing Machinery, New York, NY, USA (1986). https://doi.org/
    10.1145/10590.10611
 9. Elad, N., Padon, O., Shoham, S.: An infinite needle in a finite haystack: Find-
    ing infinite counter-models in deductive verification. Proc. ACM Program. Lang.
    8(POPL) (jan 2024). https://doi.org/10.1145/3632875
10. Emerson, E.A., Kahlon, V.: Reducing model checking of the many to the few. In:
    Automated Deduction - CADE-17, 17th International Conference on Automated
    Deduction, Pittsburgh, PA, USA, June 17-20, 2000, Proceedings. Lecture Notes in
    Computer Science, vol. 1831, pp. 236–254. Springer (2000). https://doi.org/10.
    1007/10721959_19
11. Emerson, E.A., Namjoshi, K.S.: Reasoning about rings. In: Proceedings of the 22nd
    ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages.
    p. 85–94. POPL ’95, Association for Computing Machinery, New York, NY, USA
    (1995). https://doi.org/10.1145/199448.199468
12. Fang, Y., McMillan, K.L., Pnueli, A., Zuck, L.D.: Liveness by invisible invariants.
    In: Formal Techniques for Networked and Distributed Systems - FORTE 2006,
    26th IFIP WG 6.1 International Conference, Paris, France, September 26-29, 2006.
22       Raz Lotan, Eden Frenkel and Sharon Shoham

     Lecture Notes in Computer Science, vol. 4229, pp. 356–371. Springer (2006). https:
     //doi.org/10.1007/11888116_26
13. Farzan, A., Kincaid, Z., Podelski, A.: Proofs that count. SIGPLAN Not. 49(1),
    151–164 (jan 2014). https://doi.org/10.1145/2578855.2535885
14. Farzan, A., Klumpp, D., Podelski, A.: Commutativity simplifies proofs of pa-
    rameterized programs. Proc. ACM Program. Lang. 8(POPL) (jan 2024). https:
     //doi.org/10.1145/3632925
15. Feldman, Y.M.Y., Wilcox, J.R., Shoham, S., Sagiv, M.: Inferring inductive in-
    variants from phase structures. In: Dillig, I., Tasiran, S. (eds.) Computer Aided
    Verification. pp. 405–425. Springer International Publishing, Cham (2019). https:
     //doi.org/10.1007/978-3-030-25543-5_23
16. Gurfinkel, A., Shoham, S., Meshman, Y.: SMT-based verification of parameterized
    systems. In: Proceedings of the 2016 24th ACM SIGSOFT International Sym-
    posium on Foundations of Software Engineering. p. 338–348. FSE 2016, Associa-
    tion for Computing Machinery, New York, NY, USA (2016). https://doi.org/10.
     1145/2950290.2950330
17. Hance, T., Heule, M., Martins, R., Parno, B.: Finding invariants of distributed
    systems: It’s a small (enough) world after all. In: 18th USENIX Symposium
    on Networked Systems Design and Implementation (NSDI 21). pp. 115–131.
    USENIX Association (Apr 2021), https://www.usenix.org/conference/nsdi21/
     presentation/hance
18. Hoenicke, J., Majumdar, R., Podelski, A.: Thread modularity at many levels:
    a pearl in compositional verification. In: Proceedings of the 44th ACM SIG-
    PLAN Symposium on Principles of Programming Languages. p. 473–485. POPL
    ’17, Association for Computing Machinery, New York, NY, USA (2017). https:
     //doi.org/10.1145/3009837.3009893
19. Ish-Shalom, O., Itzhaky, S., Rinetzky, N., Shoham, S.: Putting the squeeze on
    array programs: Loop verification via inductive rank reduction. In: Verification,
    Model Checking, and Abstract Interpretation. pp. 112–135. Springer International
    Publishing, Cham (2020). https://doi.org/10.1007/978-3-030-39322-{_}6
20. Itzhaky, S., Banerjee, A., Immerman, N., Lahav, O., Nanevski, A., Sagiv, M.:
    Modular reasoning about heap paths via effectively propositional formulas. In: The
    41st Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming
    Languages, POPL ’14, San Diego, CA, USA, January 20-21, 2014. pp. 385–396.
    ACM (2014). https://doi.org/10.1145/2535838.2535854
21. Jaber, N., Wagner, C., Jacobs, S., Kulkarni, M., Samanta, R.: Quicksilver: model-
    ing and parameterized verification for distributed agreement-based systems. Proc.
    ACM Program. Lang. 5(OOPSLA) (oct 2021). https://doi.org/10.1145/3485534
22. Jacobs, S., Sakr, M.: Analyzing guarded protocols: Better cutoffs, more systems,
    more expressivity. In: Verification, Model Checking, and Abstract Interpretation -
    19th International Conference, VMCAI 2018, Los Angeles, CA, USA, January 7-9,
    2018, Proceedings. Lecture Notes in Computer Science, vol. 10747, pp. 247–268.
    Springer (2018). https://doi.org/10.1007/978-3-319-73721-8_12
23. Kaiser, A., Kroening, D., Wahl, T.: Dynamic cutoff detection in parameterized
    concurrent programs. In: Computer Aided Verification, 22nd International Confer-
    ence, CAV 2010, Edinburgh, UK, July 15-19, 2010. Proceedings. Lecture Notes in
    Computer Science, vol. 6174, pp. 645–659. Springer (2010). https://doi.org/10.
     1007/978-3-642-14295-6_55
24. Karbyshev, A., Bjørner, N., Itzhaky, S., Rinetzky, N., Shoham, S.: Property-
    directed inference of universal invariants or proving their absence. J. ACM 64(1)
    (mar 2017). https://doi.org/10.1145/3022187
            Proving Cutoff Bounds for Safety Properties in First-Order Logic         23

25. Koenig, J.R., Padon, O., Shoham, S., Aiken, A.: Inferring invariants with quantifier
    alternations: Taming the search space explosion. In: Tools and Algorithms for the
    Construction and Analysis of Systems - 28th International Conference, TACAS
    2022, Munich, Germany, April 2-7, 2022, Proceedings, Part I. Lecture Notes in
    Computer Science, vol. 13243, pp. 338–356. Springer (2022). https://doi.org/
    10.1007/978-3-030-99524-9_18
26. Lotan, R., Frenkel, E., Shoham, S.: Proving cutoff bounds for safety-properties
    in first-order logic (artifact). Zenodo (2024). https://doi.org/10.5281/zenodo.
    12664114
27. Maric, O., Sprenger, C., Basin, D.A.: Cutoff bounds for consensus algorithms. In:
    Computer Aided Verification - 29th International Conference, CAV 2017, Heidel-
    berg, Germany, July 24-28, 2017, Proceedings, Part II. Lecture Notes in Com-
    puter Science, vol. 10427, pp. 217–237. Springer (2017). https://doi.org/10.
    1007/978-3-319-63390-9_12
28. de Moura, L.M., Bjørner, N.S.: Z3: an efficient SMT solver. In: Tools and Al-
    gorithms for the Construction and Analysis of Systems, 14th International Con-
    ference, TACAS 2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings.
    Lecture Notes in Computer Science, vol. 4963, pp. 337–340. Springer (2008).
    https://doi.org/10.1007/978-3-540-78800-3_24
29. Murali, A., Peña, L., Blanchard, E., Löding, C., Madhusudan, P.: Model-guided
    synthesis of inductive lemmas for FOL with least fixpoints. Proc. ACM Program.
    Lang. 6(OOPSLA2), 1873–1902 (2022). https://doi.org/10.1145/3563354
30. Namjoshi, K.S.: Symmetry and completeness in the analysis of parameterized sys-
    tems. In: Verification, Model Checking, and Abstract Interpretation, 8th Inter-
    national Conference, VMCAI 2007, Nice, France, January 14-16, 2007, Proceed-
    ings. Lecture Notes in Computer Science, vol. 4349, pp. 299–313. Springer (2007).
    https://doi.org/10.1007/978-3-540-69738-1_22
31. Padon, O.: Deductive Verification of Distributed Protocols in First-Order
    Logic. Ph.D. thesis, Tel Aviv University, Israel (2018), https://tau.primo.
    exlibrisgroup.com/permalink/972TAU_INST/bai57q/alma9932991300004146
32. Padon, O., Losa, G., Sagiv, M., Shoham, S.: Paxos made epr: decidable reasoning
    about distributed protocols. Proc. ACM Program. Lang. 1(OOPSLA) (oct 2017).
    https://doi.org/10.1145/3140568
33. Padon, O., McMillan, K.L., Panda, A., Sagiv, M., Shoham, S.: Ivy: Safety verifi-
    cation by interactive generalization. In: PLDI ’16: Proceedings of the 37th ACM
    SIGPLAN Conference on Programming Language Design and Implementation. pp.
    614–630 (Jun 2016). https://doi.org/10.1145/2908080.2908118
34. Padon, O., Wilcox, J.R., Koenig, J.R., McMillan, K.L., Aiken, A.: Induction dual-
    ity: primal-dual search for invariants. Proc. ACM Program. Lang. 6(POPL) (jan
    2022). https://doi.org/10.1145/3498712
35. Pani, T., Weissenbacher, G., Zuleger, F.: Thread-modular counter abstraction:
    automated safety and termination proofs of parameterized software by reduction
    to sequential program verification. Formal Methods in System Design pp. 1–38 (10
    2023). https://doi.org/10.1007/s10703-023-00439-6
36. Ramsey, F.P.: On a Problem of Formal Logic, pp. 1–24. Birkhäuser Boston, Boston,
    MA (1987). https://doi.org/10.1007/978-0-8176-4842-8_1
37. Segall, A.: Distributed network protocols. IEEE Transactions on Information The-
    ory 29(1), 23–35 (1983). https://doi.org/10.1109/TIT.1983.1056620
38. Tamir, O., Taube, M., McMillan, K.L., Shoham, S., Howell, J., Gueta, G., Sa-
    giv, M.: Counterexample driven quantifier instantiations with applications to dis-
24      Raz Lotan, Eden Frenkel and Sharon Shoham

     tributed protocols. Proc. ACM Program. Lang. 7(OOPSLA2) (oct 2023). https:
     //doi.org/10.1145/3622864
39. Taube, M., Losa, G., McMillan, K.L., Padon, O., Sagiv, M., Shoham, S., Wilcox,
    J.R., Woos, D.: Modularity for decidability of deductive verification with ap-
    plications to distributed systems. SIGPLAN Not. 53(4), 662–677 (jun 2018).
     https://doi.org/10.1145/3296979.3192414
40. Tran, T., Konnov, I., Widder, J.: Cutoffs for symmetric point-to-point distributed
    algorithms. In: Networked Systems - 8th International Conference, NETYS 2020,
    Marrakech, Morocco, June 3-5, 2020, Proceedings. Lecture Notes in Computer
    Science, vol. 12129, pp. 329–346. Springer (2020). https://doi.org/10.1007/
     978-3-030-67087-0_21
41. Wagner, C., Jaber, N., Samanta, R.: Enabling bounded verification of doubly-
    unbounded distributed agreement-based systems via bounded regions. Proc. ACM
    Program. Lang. 7(OOPSLA1) (apr 2023). https://doi.org/10.1145/3586033
42. Wilcox, J.R., Feldman, Y.M.Y., Padon, O., Shoham, S.: mypyvy: A research
    platform for verification of transition systems in first-order logic. In: Computer
    Aided Verification. pp. 71–85. Springer Nature Switzerland, Cham (2024). https:
     //doi.org/10.1007/978-3-031-65630-9_4
43. Yao, J., Tao, R., Gu, R., Nieh, J.: DuoAI: Fast, automated inference of inductive in-
    variants for verifying distributed protocols. In: 16th USENIX Symposium on Oper-
    ating Systems Design and Implementation (OSDI 22). pp. 485–501. USENIX Asso-
    ciation, Carlsbad, CA (Jul 2022), https://www.usenix.org/conference/osdi22/
     presentation/yao
44. Yao, J., Tao, R., Gu, R., Nieh, J., Jana, S., Ryan, G.: DistAI: Data-Driven au-
    tomated invariant learning for distributed protocols. In: 15th USENIX Sympo-
    sium on Operating Systems Design and Implementation (OSDI 21). pp. 405–421.
    USENIX Association (Jul 2021), https://www.usenix.org/conference/osdi21/
     presentation/yao
             Proving Cutoff Bounds for Safety Properties in First-Order Logic              25

A     Proofs

Theorem 1. If H is a size-reducing simulation for Tfin , P and k, then k is a
cutoff for Tfin and P .

Proof. We show that Tfin |= P if and only if TD |= P for every D with |D| ≤ k.
The direction from left to right follows directly from the definition of Tfin . For
the opposite direction, suppose TD |= P for every D with |D| ≤ k and assume
towards a contradiction that Tfin ̸|= P . Then there is a reachable state s of
Tfin with s ∈   / P . Take such a reachable state sh such that sh ∈   / P with minimal
           h
n = |s | (since all the states in Tfin are finite, minimality is well-defined). Denote
D = dom(sh ). The trace showing sh is reachable is a trace of TD . If n ≤ k we
get a contradiction to TD being safe.
     Otherwise, |sh | = n > k, sh is reachable so we have a trace (shi )ti=0 with
st = sh . We will construct, by induction on i, a reachable state sℓi such that
 h

(shi , sℓi ) ∈ H. For i = 0 we have sh0 ∈ Ifin , by item 2 we have a state sℓ0 ∈ Ifin such
that (sh0 , sℓ0 ) ∈ H and initial states are reachable. Assume we’ve constructed a
reachable state sℓi such that (shi , sℓi ) ∈ H, for i + 1 we have (shi , shi+1 ) ∈ Rfin . By
item 3 we have a state sℓi+1 such that (shi+1 , sℓi+1 ) ∈ H and (sℓi , sℓi+1 ) ∈ Rfin ⋆
                                                                                          , it
                  ℓ                            ℓ     ℓ   ℓ                      h ℓ
follows that si+1 is reachable. Denote s = st , s is reachable and (s , s ) ∈ H.
We have sh ∈     / P so by item 4, we have sℓ ∈   / P . By item 1, we have |sℓ | < |sh |, in
                                      h
contradiction to minimality of |s |.                                                        ⊔
                                                                                            ⊓

Lemma 1. A strong size-reducing simulation is a size-reducing simulation.

Proof. The properties of size-reduction and fault-preservation are the same in
both definitions. We will show that inductive totality along with strong initiation
and strong simulation imply initiation and simulation of Definition 2.

Initiation. Let sh ∈ Ifin with |sh | > k. By inductive totality we have a state
sℓ ∈ Sfin such that (sh , sℓ ) ∈ H. By strong initiation we get that sℓ ∈ Ifin .

Simulation. Let (sh , sℓ ) ∈ H and sh′ such that (sh , sh′ ) ∈ Rfin . By inductive
totality we have a state sℓ′ ∈ Sfin such that (sh′ , sℓ′ ) ∈ H and dom(sℓ ) =
dom(sℓ′ ). By strong simulation it follows that (sℓ , sℓ′ ) ∈ Rfin or sℓ = sℓ′ , and in
either case (sℓ , sℓ′ ) ∈ Rfin
                           ⋆
                               .                                                      ⊔
                                                                                      ⊓

Lemma 2. For a formula η(z) over Σ h ⊎ Σ ℓ , and a pair (sh , sℓ ) ∈ Hη such that
sh is finite, we have |sh | > |sℓ |.

Proof. sℓ is an η-substructure of sh , therefore there exists d0 ∈ dom(sh ) such
that dom(sℓ ) = dom(sh ) \ {d0 }. Thus, |sℓ | = |sh | − 1 < |sh |.             ⊔
                                                                               ⊓
26      Raz Lotan, Eden Frenkel and Sharon Shoham

For the next proofs we need some notation: for a structure s = (D, I), a term
t with free variables Vars(t) and an assignment v : Vars(t) → D we denote by
ts,v the interpretation of t in s under v. For variables x1 , . . . , xm and domain
elements d1 , . . . , dm we denote by [x 7→ d] the assignment v with v(xi ) = di
for 1 ≤ i ≤ m. For an assignment v, a variable x, and a domain element d, we
denote by v[x 7→ d] the assignment that agrees with v on all variables except for
x, which is mapped to d.

Lemma 3. Let α be a closed formula over Σ and z ∈     / Vars(α) a variable. Let
(D, I) be a structure for Σ, d0 ∈ D and (D× , I× ) a substructure of (D, I) such
that D× = D \ {d0 }. Then (D× , I× ) |= α ⇐⇒ (D, I), [z 7→ d0 ] |= [α]\z .

Proof. We first strengthen the lemma and allow α to be any formula (not nec-
essarily closed). In the same setting, for any assignment v of FV(α) to D× we
claim that (D× , I× ), v |= α ⇐⇒ (D, I), v[z 7→ d0 ] |= [α]\z .
    The proof goes by induction on the structure of α. First, we notice that if
t is a term with z ∈    / Vars(t) and v is an of assignment of Vars(t) to D× then
t(D,I),v[z7→d0 ] = t(D× ,I× ),v ∈ D× , which can be shown by induction on the
structure of the term, relying on the property that (D× , I× ) is a substructure of
(D, I), and hence interpretations of constant and function symbols coincide. All
terms that appear in α never have z as a free variable, so it follows that they
are interpreted in (D, I), v[z 7→ d0 ] to elements of D× .
    The case where α = (t1 = t2 ) follows easily. We use this as well for the case
where α = r(t1 , . . . , tm ):

                                         (D× , I× ), v |= r(t1 , . . . , tm ) ⇐⇒
                                (D× ,I× ),v
                          (t1                 , . . . , tm (D× ,I× ),v ) ∈ I× (r) ⇐⇒
             (t1 (D,I),v[z7→d0 ] , . . . , tm (D,I),v[z7→d0 ] ) ∈ I(r) ∩ D×
                                                                          m
                                                                            ⇐⇒
                    (t1 (D,I),v[z7→d0 ] , . . . , tm (D,I),v[z7→d0 ] ) ∈ I(r) ⇐⇒
                                    (D, I), [z 7→ d0 ] |= r(t1 , . . . , tm )

First equivalence is the semantics of relations, the second is definition of a sub-
structure and the observation above, the third is the observation above, and the
last equivalence is again the semantics of relations.
    For the case where α = ∀x.β, then [α]\z = ∀x. (x ̸= z) → [β]\z .

                                                       (D× , I× ), v |= ∀x.β ⇐⇒
                                    ∀d ∈ D× .(D× , I× ), v[x 7→ d] |= β ⇐⇒
                       ∀d ∈ D× .(D, I), v[x 7→ d, z 7→ d0 ] |= [β]\z ⇐⇒
            ∀d ∈ D.(D, I), v[z 7→ d0 , x 7→ d] |= (x ̸= z) → [β]\z ⇐⇒
                         (D, I), v[z 7→ d0 ] |= ∀x.(x ̸= z) → [β]\z

First equivalence is the semantics of universal quantification, the second is the
induction hypothesis, the third is seen to be true by dividing into the cases
d = d0 and d ̸= d0 , and noticing v[x 7→ d, z 7→ d0 ] = v[z 7→ d0 , x 7→ d], as x and
              Proving Cutoff Bounds for Safety Properties in First-Order Logic                      27

z are different variables by the assumption z ∈/ Vars(α). The last equivalence is
again the semantics of universal quantification.
    The cases for negation and conjunction are trivial. Disjunction and Existen-
tial quantification follow from the previous cases.
                                                                               ⊔
                                                                               ⊓

    Throughout the following proofs we use abuse of notation thinking of inter-
pretations of states such as sh , sℓ , which are interpretations of Σ as interpreta-
tions of Σ h , Σ ℓ and so on, when necessary, as discussed in Section 2. We also
freely use the fact that if α is a formula over vocabulary Σ h and and I h , I ℓ are
interpretations for domain D and vocabularies Σ h , Σ ℓ respectively, such that
(D, I h ⊎ I ℓ ) |= α then (D, I h ) |= α.

Lemma 4. Let η(z) be a formula over Σ h ⊎Σ ℓ . If verification conditions (1)–(3)
of Figure 5 are valid then Hη ∩ (Sfin × Sfin ) satisfies items 2 to 4 of Definition 3.

Proof. We prove strong initiation and strong simulation, fault preservation is
similar to strong initiation.

Strong Initiation: Let (sh , sℓ ) ∈ Hη ∩ (Sfin × Sfin ) such that sh ∈ Ifin , we show
that sℓ ∈ Ifin . From Definition 4 we have sh = (D, I h ), sℓ = (D× , I×        ℓ
                                                                                  ) and
                                                               ℓ                   ℓ
d0 ∈ D such that D× = D \ {d0 } and an interpretation I such that (D× , I×           ) is
                              ℓ          h   ℓ                      h
a substructure of (D, I ) and (D, I ⊎ I ), [z 7→ d0 ] |= η(z). s is an initial state
so we have (D, I h ) |= Γ h ∧ ιh . By validity of verification condition (1), we have
(D, I ℓ ), [z 7→ d0 ] |= [ι]ℓ\z . From Lemma 3 we get (D× , I×
                                                             ℓ
                                                                ) |= ιℓ and so sℓ ∈ Ifin
as required.

Strong Simulation: Let (sh , sℓ ), (sh′ , sℓ′ ) ∈ Hη ∩ (Sfin × Sfin ) such that (sh , sh′ ) ∈
Rfin and dom(sℓ ) = dom(sℓ′ ). We show that (sℓ , sℓ′ ) ∈ Rfin or sℓ = sℓ′ . From
(sh , sh′ ) ∈ Rfin it follows that dom(sh ) = dom(sh′ ). Along with dom(sℓ ) =
dom(sℓ′ ), unfolding Definition 4 gives: a high domain D and low domain D×
with d0 ∈ D such that D× = D \{d0 }, and interpretations: I h , I ℓ , I×         ℓ
                                                                                    , I h′ , I ℓ′ , I×
                                                                                                     ℓ′
                      ℓ                                 ℓ                 ℓ′
such that: (D× , I× ) is a substructure of (D, I ) and (D× , I× ) is a substructure
of (D, I ℓ′ ) and (D, I h ⊎ I ℓ ), [z 7→ d0 ] |= η(z), (D, I h ⊎ I ℓ′ ), [z 7→ d0 ] |= η ′ (z). By
definition of states and transitions we have: (D, I h ) |= Γ h , (D, I h′ ) |= Γ h′ and
(D, I h ⊎ I h′ ) |= τ h . By verification condition (2) we have: (D, I ℓ ⊎ I ℓ′ ), [z 7→
d0 ] |= [(τ ∨ idΣ )ℓ ]\z . By Lemma 3 we get: (D× , I×    ℓ
                                                            ⊎ I×ℓ′
                                                                   ) |= (τ ∨ idΣ )ℓ . It follows
          ℓ ℓ′               ℓ     ℓ′
that (s , s ) ∈ Rfin or s = s .                                                                      ⊔
                                                                                                     ⊓

Lemma 5. Let η(z) be a high-low update with precondition θ(z) and (D, I h ) a
structure with d0 ∈ D such that (D, I h ), [z 7→ d0 ] |= θ(z). Then there exists an
interpretation I ℓ such that (D, I h ⊎ I ℓ ), [z 7→ d0 ] |= η(z).

Proof. We define the interpretation I ℓ by: for every relation r ∈ Σ define
I ℓ (rℓ ) = {d | (D, I h ), [z 7→ d0 , x 7→ d] |= αr (x, z)}, and for every function
                                       (D,I h ),[z7→d0 ,x7→d]
f ∈ Σ define: I ℓ (f ℓ )(d) = (tf )                             . That we have (D, I h ⊎ I ℓ ), [z 7→
d0 ] |= η(z) is now trivial.                                                                        ⊔
                                                                                                    ⊓
28      Raz Lotan, Eden Frenkel and Sharon Shoham

Lemma 6. Let η(z) be a high-low update with precondition θ(z). If verification
conditions (4)–(7) of Figure 5 are valid, then Hη ∩ (Sfin × Sfin ) satisfies item 5
of Definition 3.

Proof. We show inductive totality.

Initial States. For an initial state sh ∈ Ifin with |sh | > k, we show the existence
of sℓ such that (sh , sℓ ) ∈ Hη ∩ (Sfin × Sfin ). We have sh |= Γ h ∧ ιh ∧ size>k . From
verification condition (6) we get sh |= ∃z.θ(z). Denote sh = (D, I h ), then there is
d0 ∈ D such that sh , [z 7→ d0 ] |= θ(z). From Lemma 5 there is an interpretation
I ℓ such that (D, I h ⊎ I ℓ ), [z 7→ d0 ] |= η(z). Define the domain D× = D \ {d0 }
                                ℓ
and the interpretation I×          by: for every relation symbol r ∈ Σ with arity m:
  ℓ   ℓ          ℓ ℓ         m
I× (r ) = I (r ) ∩ D× and for every function symbol f ∈ Σ with arity m:
  ℓ
I×  (f ℓ ) = I ℓ (f ℓ )|D×                                                 ℓ
                         m . By verification condition (4), we have (D, I ) |= closedf (z)

            ℓ                           m
and so I×     (f ) is a function to D×     for all f ∈ Σ so sℓ = (D× , I×
                                                                        ℓ
                                                                          ) is well-defined
                                                    h ℓ
as a structure. From the above we get (s , s ) ∈ Hη . By verification condition
(5) we have (D, I ℓ ) |= [Γ ]ℓ\z . From Lemma 3 we get (D× , I×         ℓ
                                                                          ) |= Γ ℓ , and so
 ℓ                              h ℓ
s ∈ Sfin , and we have (s , s ) ∈ Hη ∩ (Sfin × Sfin ).

Transitions. Assume (sh , sh′ ) ∈ Rfin and sℓ such that (sh , sℓ ) ∈ Hη ∩(Sfin ×Sfin ).
We show the existence of sℓ′ such that (sh′ , sℓ′ ) ∈ Hη ∩ (Sfin × Sfin ). Denote
sh = (D, I h ), sℓ = (D× , I×   ℓ
                                  ). From Definition 4, we get d0 ∈ D such that D× =
D \ {d0 } and an interpretation I ℓ such that (D, I h ⊎ I ℓ ), [z 7→ d0 ], |= η(z). It
follows that (D, I h ), [z 7→ d0 ] |= θ(z). Denote sh′ = (D, I h′ ), we then have
(D, I h ⊎ I h′ ), [z 7→ d0 ] |= Γ h ∧ Γ h′ ∧ τ h ∧ θ(z). From verification condition (7) we
have (D, I h′ ), [z 7→ d0 ] |= θ′ (z). From Lemma 5 we get an interpretation I ℓ′ such
that (D, I h′ ⊎I ℓ′ ), [z 7→ d0 ] |= η(z), from which we construct an interpretation I×   ℓ′
                                                          ℓ′          ℓ′               ℓ
similarly to the previous item. We then have s = (D× , I× ) ∈ Sfin , dom(s ) =
dom(sℓ′ ) = D× and finally (sh′ , sℓ′ ) ∈ Hη ∩ (Sfin × Sfin ).                            ⊔
                                                                                          ⊓

Theorem 2. If all the verification conditions for a high-low update η(z), T ,
φ and k (Figure 5) are valid, then Hη ∩ (Sfin × Sfin ) is a strong size-reducing
simulation for Tfin , P and k. Consequently, k is a cutoff for Tfin and P .

Proof. Corollary of Theorem 1 and lemmas 2, 4 and 6.                                      ⊔
                                                                                          ⊓
