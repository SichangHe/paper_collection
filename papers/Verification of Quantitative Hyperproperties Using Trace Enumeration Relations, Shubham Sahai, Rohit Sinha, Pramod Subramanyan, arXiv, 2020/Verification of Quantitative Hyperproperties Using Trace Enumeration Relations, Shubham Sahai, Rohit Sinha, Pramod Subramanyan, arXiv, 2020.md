                                              Verification of Quantitative Hyperproperties
                                                 Using Trace Enumeration Relations ⋆

                                                    Shubham Sahai1 , Pramod Subramanyan1 , and Rohit Sinha2
arXiv:2005.04606v2 [cs.CR] 14 May 2020




                                                                1
                                                                    Indian Institute of Technology, Kanpur
                                                                              2
                                                                                 Visa Research



                                                 Abstract. Many important cryptographic primitives offer probabilistic
                                                 guarantees of security that can be specified as quantitative hyperprop-
                                                 erties; these are specifications that stipulate the existence of a certain
                                                 number of traces in the system satisfying certain constraints. Verifica-
                                                 tion of such hyperproperties is extremely challenging because they in-
                                                 volve simultaneous reasoning about an unbounded number of different
                                                 traces. In this paper, we introduce a technique for verification of quan-
                                                 titative hyperproperties based on the notion of trace enumeration rela-
                                                 tions. These relations allow us to reduce the problem of trace-counting
                                                 into one of model-counting of formulas in first-order logic. We also in-
                                                 troduce a set of inference rules for machine-checked reasoning about the
                                                 number of satisfying solutions to first-order formulas (aka model count-
                                                 ing). Putting these two components together enables semi-automated
                                                 verification of quantitative hyperproperties on infinite state systems.
                                                 We use our methodology to prove confidentiality of access patterns in
                                                 Path ORAMs of unbounded size, soundness of a simple interactive zero-
                                                 knowledge proof protocol as well as other applications of quantitative
                                                 hyperproperties studied in past work.


                                         1     Introduction

                                         Recent years have seen significant progress in automated and semi-automated
                                         techniques for the verification of security requirements of computer systems [4,
                                         10, 16, 20, 32, 50, 53, 58]. Much of this progress has built on the theory of hyper-
                                         properties [22], and these have been used extensively in analysis of whether sys-
                                         tems satisfy secure information flow properties [1, 2, 6, 8, 15, 30, 37, 39, 41, 52, 60]
                                         such as observational determinism [44, 58] and non-interference [34]. Unfortu-
                                         nately, the security specification of several important security primitives cannot
                                         be captured by secure information flow properties like observational determin-
                                         ism. In particular, observational determinism and non-interference are not appli-
                                         cable when reasoning about algorithms that offer probabilistic – as opposed to
                                         deterministic – guarantees of confidentiality and integrity. Prominent examples
                                         of security primitives offering probabilistic guarantees include Path ORAM [51]
                                         and various zero-knowledge proof protocols.
                                         ⋆
                                             This is an extended version of a paper with the same title that appears at CAV 2020.
2             Shubham Sahai, Pramod Subramanyan, and Rohit Sinha

    A promising direction for the verification of such protocols are the class of
quantitative hyperproperties [31], one example of which is deniability [12, 14].
Deniability states that for every infinitely-long sequence of observations that an
adversary makes, there are (exponentially) many different secrets that could have
resulted in exactly these observations. Therefore, the adversary learns very little
about the secrets in an execution from a particular sequence of observations.
    How does one prove a quantitative hyperproperty like deniability? Suppose
our goal is to show that for every trace of adversary observations, there exist 2n
traces with the same observations but different secrets. Here n is a parameter
of the system, e.g., the length of a password in bits. One option, first suggested
by Yasuoka and Terauchi [57] and recently revisited by Finkbeiner, Hahn, and
Torfah [31], is to consider the following k-trace property, where k = 2n + 1.
    ∀π0 . ∃π1 , π2 , . . . , π2n .
      2n
     ^                             2n ^
                                  ^  2n                                      
              obs(π0 ) = obs(πj ) ∧       (j 6= k) ⇒ secret(πj ) 6= secret(πk )
        j=1                          j=1 k=1

    The property states that for every trace of the system, there must exist
2n other traces with identical observations and pairwise different secrets. In
the above, π0 , π1 , . . . represent trace variables, obs(πj ) refers to the trace of
adversary observations projected from the trace πj , while secret(πj ) refers to
the trace of secret values in the trace πj . There are at least three problems
with the verification of the above property. First, the size of this property grows
exponentially with n; verification needs to reason about 2n traces simultaneously
and is not scalable. The second problem is quantifier alternation. Even if we could
somehow reason about 2n traces, we have to show that for every trace π0 , there
exist 2n other traces satisfying the above condition. The third problem is that
the above technique does not work for symbolic bounds. While it is possible – at
least in principle – to use the above construction by picking a specific value of
n, say 16, to show that 216 traces exist that satisfy deniability, we would like to
show that the property holds for all n, where n is a state variable or parameter
of the transition system. Capturing the dependence of the trace-count bound on
parameters, such as n, is important because it shows that the attacker has to
work exponentially harder as n increases. Such general proofs are not possible by
reduction to a k-trace property because the construction requires k be bounded.
    Recent work by Finkbeiner, Hahn, and Torfah [31] has made significant
progress in addressing the first two problems by showing a reduction from k-trace
property checking into the problem of maximum model counting [33]. However,
their technique still produces a propositional formula whose size grows expo-
nentially in the size of the quantitative hyperproperty. Further, model counting
itself is a computationally hard problem that is known to be #P -complete, and
maximum model counting is even harder. As a result, their technique does not
scale well and times out on the verification of an 8-bit leakage bound for an 8-bit
password. Finally, their method does not support symbolic bounds, and there-
fore cannot be used to verify parametric systems; we verify several examples of
such systems in this paper (e.g., Path ORAM [51] of symbolic size).
                    Verification of QHPs Using Trace Enumeration Relations         3

    In this work, we propose a new technique for quantitative hyperproperty
verification that addresses each of the above problems. Our approach is based
on the following insights. First, instead of trying to count the number of traces
that have the same observations and different inputs, we instead show injectiv-
ity/surjectivity from satisfying assignments of a first-order formula to traces of
a transition system. This allows us to bound the number of traces satisfying
the quantitative hyperproperty by the number of satisfying solutions to this for-
mula. We introduce the notion of a trace enumeration relation to formalize this
relation between the first-order formula and traces of the transition system. An
important advantage of the above reduction is that proving the validity of a trace
enumeration relation is only a hyperproperty – not a quantitative hyperproperty.
    Next, we develop a novel technique to bound the number of satisfiable solu-
tions to a first-order logic formula, which is of independent interest. While this is
a hard problem, we exploit the fact that our formulas have a significant amount
of structure. We introduce a set of inference rules inspired by ideas from enu-
merative combinatorics [13, 55, 59]. These rules allow us to bound the number
of satisfying assignments to a formula by making only satisfiability queries.
    In summary, our techniques can prove quantitative hyperproperties with sym-
bolic bounds on parametric infinite-state systems. We demonstrate their utility
by verifying representative quantitative hyperproperties of diverse applications.

Contributions
 1. We introduce a specification language for quantitative hyperproperties (QHPs)
    over symbolic transition systems and define formal satisfaction semantics for
    this language. Our specification language is more expressive than past work
    on QHP specification because it allows the bound to be a first-order formula
    over the state variables of the transition system.
 2. We provide several examples of QHPs relevant to security verification. We
    identify a new class of QHPs, referred to as soundness hyperproperties, ap-
    plicable to protocols that provide statistical guarantees of integrity.
 3. We propose a novel semi-automated verification methodology for proving
    that a system satisfies a QHP. Our methodology applies to properties that
    involve a single instance of quantifier alternation and works by reducing
    the problem of QHP verification to that of checking non-quantitative hyper-
    properties over two and three traces of the system and counting satisfiable
    solutions to a formula in first-order logic.
 4. We introduce a set of inference rules for bounding the number of satisfiable
    solutions to a first-order logic formula, using only satisfiability queries.
 5. We demonstrate the applicability of our specification language and verifica-
    tion methodology by providing proofs of security for Path ORAM, soundness
    of a simple zero-knowledge protocol, as well as examples taken from prior
    work on quantitative security specifications. We show that our verification
    methodology scales to larger systems than could be handled in prior work.
    To the best of our knowledge, our work is the first machine-checked proof of
    confidentiality of the access patterns in Path ORAM.
4         Shubham Sahai, Pramod Subramanyan, and Rohit Sinha

2     Motivating Example
In this section, we first introduce the model of transition systems used in this
paper. We then discuss quantitative hyperproperty (QHP) specification and ver-
ification for our running example – a simple zero-knowledge puzzle.

2.1    Preliminaries
Let FOL(T ) denote first-order logic modulo a theory T . The theory T is assumed
to be multi-sorted, includes the theory of linear integer arithmetic (LIA), and
contains the = relation. Let ΣT be the theory T ’s signature: the set consisting
of the constant, function, and predicate symbols in the theory. We say that a
formula is a ΣT -formula if it consists of the symbols in ΣT along with variables,
logical connectives, and quantifiers. We only consider theories which are such
that the set of satisfying assignments for any ΣT -formula is a countable set.3
    For every variable x, we will assume there exists a unique variable x′ , which
we refer to as the primed version of x. We will use X, Y , and Z to denote
sets of variables. Given a set of variables X, we will use X ′ to refer to the set
consisting of the primed version of each variable in X, that is X ′ = {x′ | x ∈ X}.
Similarly X1 , X2 , etc. are sets consisting of new variables defined as follows:
X1 = {x1 | x ∈ X} and X2 = {x2 | x ∈ X}. We will use F (X) to denote the
application of a function or predicate symbol F on the variables in the set X.
A satisfying assignment σ to the formula F (X) is written as σ |= F (X). Given
a formula F (X) and a satisfying assignment σ to this formula, we will denote
the valuation of the variable x ∈ X in the assignment σ as σ(x). We will abuse
notation in two ways and also write σ(X) to refer to a map from the variables
x ∈ X to their assignments in σ. We will also write σ(G(X)) to denote the
valuation of the term G(X) under the assignment σ.
    The number of satisfiable assignments for the variables in the set X to a for-
mula F (X, Y ) as a function of the variables Y will be denoted by #X. F (X, Y ).
#X. F (X, Y ) is the function λY . |{σ(X) | σ |= F (X, Y)}| evaluated at Y ; |S| is
                                                                             .
the cardinality of the set S. For example, consider the predicate f (i, n) = (0 ≤
i < 2n). In this case, #i. f (i, n) = max (0, 2n), meaning that for a given value
of n > 0, there are 2n satisfying assignments to i.

Definition 1 (Transition System). A transition system M is defined as the
tuple M = hX, Init(X), Tx (X, X ′ )i. X is a finite set of (uninterpreted) constants
that represents the state variables of the transition system. Init and Tx are ΣT -
formulas representing the initial states and the transition relation, respectively.
Init is defined over the signature ΣT ∪ X. Tx is over the signature ΣT ∪ X ∪ X ′ ;
X represents the pre-state of the transition and X ′ represents its post-state.

    A state of the system is an assignment to the variables in X. We use σ 0 , σ 1 , σ 2
etc. to represent states. A trace of the system M is an infinite sequence of states
3
    Our experiments mostly use the AUFLIA theory which allows arrays, uninterpreted
    functions, and linear integer arithmetic.
                       Verification of QHPs Using Trace Enumeration Relations                      5

τ = σ 0 σ 1 σ 2 . . . σ i . . . such that Init(σ 0 ) is valid and for all i ≥ 0, Tx (σ i , σ i+1 ) is
valid; in order to keep notation uncluttered, we will often drop the ≥ 0 qualifier
when referring to trace indices. We assume that every state of the transition
system has a successor: for all σ there exists some σ ′ such that Tx (σ, σ ′ ) is valid,
ensuring every run of the system is infinite. We will represent traces by τ, τ1 , τ2 ,
etc. Given a trace τ , we refer to its ith element by τ i . If τ = σ 0 σ 1 . . . , then
τ 0 = σ 0 and τ 1 = σ 1 . The notation τ [i,∞] refers to the suffix of trace τ starting
at index i. The set of all traces of the system M is denoted by ΦM . Given a state
σ and a variable x ∈ X, σ(x) is the valuation of x in the state σ.


2.2    Motivating Example: Zero-Knowledge Hats

Zero-knowledge (Z-K) proofs are constructions involving two parties: a prover
and a verifier, where the prover’s goal is to convince the verifier about the
veracity of a given statement without revealing any additional information. We
motivate the need for quantitative hyperproperty verification using a Z-K puzzle.


Puzzle Overview: Consider the following scenario. Peggy has a pair of oth-
erwise identical hats of different colors (say, yellow and green). She wants to
convince Victor, who is yellow-green color blind, that the hats are of different
colors, without revealing the colors of the hats. This problem can be solved using
the following interactive protocol. Peggy gives both hats to Victor, and Victor
randomly chooses a hat behind a curtain and shows it to Peggy. Next, he goes
back behind the curtain and uniformly randomly chooses if he wants to switch
the hat or not. He now appears in front of Peggy and asks: “Did I switch?”
    If the hats are really of different colors, Peggy will be able to answer correctly
with probability 1. If Peggy is cheating – the hats are in fact of the same color –
her best strategy is to guess, and with probability 0.5 she will answer incorrectly.
If the interaction is repeated k-times, Peggy will be caught with probability 1 −
2−k . The interaction between Peggy and Victor only reveals the fact that Peggy
can detect a switch and not the color of the hat, making this zero-knowledge.


Verification Objectives: A zero-knowledge proof must satisfy three proper-
ties: completeness (an honest prover should be able to convince an honest verifier
of a true statement), soundness (a cheating prover can convince an honest veri-
fier with negligible probability) and zero-knowledge (no information apart from
the veracity of the statement should be revealed). Completeness is a standard
trace property, while zero-knowledge is the 2-safety property of indistinguisha-
bility. Consequently, the main challenge in automated verification of the zero-
knowledge protocol described above is that of soundness. In this section, we
discuss its specification and verification using quantitative hyperproperties.


Soundness as a Quantitative Hyperproperty: Consider the transition sys-
tem M = hX, Init (X), Tx (X, X ′ )i, shown in Figure 1, representing this protocol.
6        Shubham Sahai, Pramod Subramanyan, and Rohit Sinha


                   .
    X              = {C, P, S, i, R}
                   .
    Init(X)        = (∀i. 0 ≤ C[i] ≤ 1) ∧ (∀i. 0 ≤ P[i] ≤ 1) ∧ S ∧ (i = 1) ∧ (R > 0)
                   .
    Tx (X, X ′ )   = (C′ = C) ∧ (P′ = P) ∧ (R′ = R) ∧ S′ = S ∧ (C[i] = P[i]) ∧
                                                                                

                      i′ = min (i + 1, R)


              Fig. 1: Transition system model of the example protocol.


The variable R is a parameter of the system and refers to the number of rounds
of the protocol. C and P are boolean arrays representing the challenges from
the verifier to the prover, and the responses from the prover to the verifier, re-
spectively. i is the current round, and S is a boolean flag which corresponds to
whether the zero-knowledge proof has succeeded. C and P are initialized non-
deterministically to model the fact that the verifier chooses their challenges ran-
domly, and a cheating prover’s best strategy is guessing. While a cheating prover
can use any strategy, if the challenges are indistinguishable to her, then the best
strategy is to sample responses from a uniform distribution.
    Soundness is captured by the following quantitative hyperproperty (QHP):

                     ∀π0 .#π1: F (δπj ,πk ). G (ψπ0 ,π1 ) ≥ 2R − 1                     (1)

We will provide formal satisfaction semantics for QHPs in Section 3. For now, we
informally describe its meaning. The term #π1: F (δπj ,πk ). G (ψπ0 ,π1 ) ≥ 2R − 1
introduces a counting quantifier which stipulates the existence of at least 2R − 1
traces satisfying certain conditions: (i) these traces must all be pairwise-different,
where difference is defined by satisfaction of the formula F (δπj ,πk ) and (ii) all
of these traces must be related to trace π0 by the relation G (ψπ0 ,π1 ).
    The state predicates δ and ψ are defined as follows.
                    .
        δ(σ1 , σ2 ) = σ1 (P[i]) 6= σ2 (P[i])
                    .                                     
        ψ(σ1 , σ2 ) = σ1 ((i = R) ⇒ S) ⇒ σ2 ((i = R) ⇒ ¬S)           ∧
                                                        
                       σ1 (C) = σ2 (C) ∧ σ1 (R) = σ2 (R)

    The requirement imposed by δ is that Peggy’s responses be different at some
step i for every pair of traces captured by the counting quantifier. ψ says that if
trace π0 is a trace where Peggy’s cheating succeeds (i.e., S = true when i = R),
then in all traces captured by π1 , the challenges and number of rounds are the
same as π0 but Peggy’s cheating is detected by Victor (i.e., S = false when
i = R). These requirements are illustrated in Figure 2(b).
    The QHP requires that for every trace in which a cheating prover succeeds
in tricking the verifier for a given trace of challenges, there are 2R − 1 other
traces with the same challenges in which the prover’s cheating is detected. Even
though soundness is a probabilistic property over the distribution of the system’s
traces, it can be reduced to counting (and thus specified as a QHP) because each
                                 Verification of QHPs Using Trace Enumeration Relations                                 7

                                                                                                           success
                                                          τ0      τ00             τ01         τ02    ...       τ0k    ...
                   U(Y1 , τ0 , τ1 )                                                                            fail   =C
      Y1            U (Y 2       , τ0 , τ2 )              τ1      τ10             τ11         τ12    ...       τ1k    ...
           Y2                                                                                                  fail   =C
                                    C)
      V(Y, R)           C,
                             τ 0, τ                       τ2      τ20             τ21         τ22    ...       τ2k    ...
                 U (Y
                                                                   ..                                                 =C
                                                                    .
           YC                                                                                                  fail
                                                          τC      τC0             τC1         τC2    ...       τCk    ...


(a) Trace enumeration predicates.                                       (b) Traces in the soundness QHP.


      Fig. 2: Using trace enumeration predicates to verify the soundness QHP.


execution trace is sampled uniformly from a finite set. Therefore, if the QHP is
satisfied, Peggy’s probability of successful cheating is upper-bounded by 2−R .


2.3        Solution Outline



                                Construct Transition System Model                               Definition 1



                                     Construct Enumeration: V, U                                Definitions 4 and 5
                                                                  ⊳
                                                  }
                                               ,=




                                                                        ∈
                                                                         {≤
                                             {≥




                                                                            ,=
                                         ∈




                                                                              }
                                         ⊳




                Injective Enumeration                             Surjective Enumeration
      Properties 2 and 3                                                                Properties 6 and 7

                                                      Counting
                                                      Section 5


                Fig. 3: Overview of the complete verification methodology.


    To prove a QHP of the form ∀π0 . #π1 : ∆πj ,πk . ϕ ⊳ N (Z), we construct a
trace enumeration predicate V(Y, Z) and show an injective/bijective mapping
8        Shubham Sahai, Pramod Subramanyan, and Rohit Sinha

from assignments to Y in V(Y, Z) and traces of the system. This allows us to
prove ∀π0 . #π1 : ∆πj ,πk . ϕ ⊳ #Y. V(Y, Z). This part of the proof relies on the
notion of a trace enumeration relation (§ 4). In the next step, we show that
#Y. V(Y, Z) ⊳ N (Z) using the inference rules presented in § 5. Figure 3 shows
an overview of the complete methodology and a roadmap for the rest of the
paper. We now describe these steps in the context of the motivating example.

Verification of Soundness for the Z-K Hats Puzzle: Property 1 is illustrated in
Figure 2(b). τ0 is a trace where the Z-K proof succeeds, while the proof fails for
the set of traces ΦC = {τ1 , τ2 , . . . , τC }. The red states show the particular step
of the proof in which an incorrect response is given by the prover, and each of
these steps as well as their associated prover responses are pairwise different.
The QHP is satisfied if |ΦC | ≥ 2R − 1 for every τ0 ∈ ΦM , where R = τ00 (R).
     The first step in our methodology is to construct a parameterized relation,
called a trace enumeration relation, U(Y, τ0 , τ1 ). This relates τ0 to each trace in
the set ΦC and is parameterized by Y. For every value of the parameter Y, U
relates a trace in which the proof succeeds (τ0 ) to a trace in which the proof fails
(τ1 ). For every trace τ0 in which the proof succeeds, the set {τ1 | ∃Y. U(Y, τ0 , τ1 )}
corresponds to the set of traces with the same challenges and the same number
of rounds, but with failed proofs of knowledge. Note this is a subset of ΦC .
     Next, we construct a predicate V(Y, R) which defines valid assignments to
Y for a particular value of R. For a particular R, consider the set: {σ(Y) | σ |=
V(Y, R)}. Suppose we are able to show that the relation U is injective in Y and
τ0 for assignments to Y drawn from this set, then we can lower-bound the size of
ΦC by the size of this set. In other words, we have reduced the problem of trace
counting to the problem of counting assignments to V(Y, R).
     Precisely stated, using V and U, we show the following.

 1. For every trace τ0 , and every assignment Yi satisfying V(Yi , τ00 (R)), there
    exists a corresponding trace τi that satisfies both U(Yi , τ0 , τi ) and ψ(τ0 , τi ).
    (Note τ00 (R) refers to the valuation of R in the initial state of τ0 .)
 2. Given two different satisfying assignments to V for a particular value of R,
    say Yj and Yk , the corresponding traces τj and τk are guaranteed to have
    different prover responses; in other words, the traces satisfy δ(τj , τk ).

    The above two properties, illustrated in Figure 2(a), imply there is an injec-
tive mapping from satisfying assignments of V(Y, R) to traces in ΦC . Therefore,
the number of traces in ΦC can be lower bounded by the number of satisfy-
ing assignments to Y in V(Y, R), i.e. #Y. V(Y, R). We have reduced the difficult
problem of counting traces into a slightly easier problem of counting satisfying
assignments to a FOL(T ) formula.
    The final step is to bound #Y. V(Y, R). For example, one well-known idea
from enumerative combinatorics is that if a set A is the union of disjoint sets B
and C, then |A| = |B| + |C|. Translated to model counting, the above can be
written as #X. F (X, Y ) = #X. G(X, Y )+#X. H(X, Y ) if F (X, Y ) ⇔ G(X, Y )∨
                    Verification of QHPs Using Trace Enumeration Relations              9

H(X, Y ) is valid and G(X, Y ) ∧ H(X, Y ) is unsat.4 We present a set of inference
rules in Section 5 that build on this and related ideas. These inference rules
allow us derive a machine-checked proof of the bound #Y. V(Y, R) ≥ 2R − 1,
thus completing the proof of Property 1 for the Z-K hats puzzle.


3     Overview of Quantitative Hyperproperties
This section introduces a logic for the specification of quantitative hyperproper-
ties over symbolic transition systems. We present satisfaction semantics for this
logic and then discuss its applications in security verification.


       ψ      ::= ∀π. ψ | #π: ∆πj ,πk . ψ ⊳ N (Z) | ϕ
       ϕ      ::= Pπ1 ,π2 ,...,πk | ¬ϕ | ϕ ∨ ϕ | ϕ U ϕ | X ϕ
       ⊳      ::= ≤ | = | ≥


                   Fig. 4: Grammar of Quantitative HyperLTL.




3.1   Quantitative Hyperproperties
Figure 4 shows the syntax of Quantitative HyperLTL, our extension of Hyper-
LTL [32] that allows specification of quantitative hyperproperties over symbolic
transition systems. There are two noteworthy differences from the presentation
of HyperLTL in [32]. The first is the predicate Pπ1 ,π2 ,...,πk . This refers to a k-
ary state predicate P that is applied to the first element of each trace in the
subscript. These are analogous to atomic propositions in presentations that use
Kripke structures and are defined as k-ary state predicates to capture relational
properties over traces of the transition system. For example, consider the predi-
                  .
cate P(σ0 , σ1 ) = (input(σ0 ) = input (σ1 )). Given this definition, a system M with
exactly two traces ΦM = {τ1 , τ2 } satisfies the HyperLTL formula ∀π1 , π2 . Pπ1 ,π2
iff input (τ10 ) = input (τ20 ). This hyperproperty requires that the input in the
initial state of the system be deterministically initialized.
     The second difference is the new counting quantifier : #π: ∆πj ,πk . ψ ⊳ N (Z).5
∆πj ,πk is an unquantified HyperLTL formula over two “fresh” trace variables πj
and πk that encodes when two traces are considered different.6 ψ is another
4
  We note there is an implied universal quantifier here. To be precise, we must write
  ∀Y. #X. F (X, Y ) = #X. G(X, Y ) + #X. H(X, Y ).
5
  A counting quantifier over Kripke structures was introduced by Finkbeiner et al. [31].
  Our definition is slightly different and a detailed comparison is deferred to Section 7.
6
  We say that an unquantified HyperLTL formula is over the set of trace variables V
  iff every variable that appears in the subscript of some predicate P in the formula
  belongs the set V .
10         Shubham Sahai, Pramod Subramanyan, and Rohit Sinha



Π |=Φ ∀π. ψ                         iff for all τ ∈ Φ : Π[π 7→ τ ] |=Φ ψ
Π |=Φ #π: ∆πj ,πk . ψ ⊳ N (Z)       iff |ΦC | = 0 ⇒ 0 ⊳ N (Z) is valid, and
                                       |ΦC | > 0 ⇒ ∀τ ∈ ΦC . |ΦC | ⊳ τ 0 (N (Z)), where,
                                       ΦC ⊆ Φ is a maximally large set such that:
                                        ∀τj , τk ∈ ΦC .
                                               τj 6= τk ⇔ {πj 7→ τj , πk 7→ τk } |= ∆πj ,πk
                                       and, ∀τ ∈ ΦC . Π[π 7→ τ ] |=Φ ψ
Π |=Φ Pπ1 ,...,πk                   iff P(Π(π1 )0 , . . . , Π(πk )0 ) is valid
Π |=Φ ¬ψ                            iff Π 6|=Φ ψ
Π |=Φ ψ ∨ ϕ                         iff Π |=Φ ψ or Π |=Φ ϕ
Π |=Φ X ϕ                           iff Π [1,∞] |=Φ ϕ
Π |=Φ ϕ U ψ                         iff there exists j ≥ 0 : Π [j,∞] |=Φ ψ
                                        and for all 0 ≤ i < j : Π [i,∞] |=Φ ϕ


Fig. 5: Satisfaction semantics for Quantitative HyperLTL formulas over symbolic
transition systems.


(possibly-quantified) HyperLTL formula. The operator ⊳ can be ≤, =, or ≥.
N (Z) is an integer-sorted term in FOL(T ) over the variables in the set Z, Z ⊂ X
where X is the set of state variables of the transition system under consideration.
Z typically refers to the subset of the state variables that define the parameters
of the transition system; e.g. Z = {R} for the Z-K proof transition system
in Figure 1, the number of blocks in a model of Path ORAM, the size of an
array, etc. Typically, the variables in the set Z do not change after initialization.
Informally stated, the counting quantifier is satisfied if a maximally large set
ΦC ⊆ Φ satisfying the following two conditions: (i) each of the traces in ΦC are
pairwise different as defined by satisfaction of ∆πj ,πk , and (ii) every trace in this
set satisfies the HyperLTL formula ψ, has cardinality ⊳ count where count is the
valuation of N (Z) in the initial state of every trace in ΦC .
    The remaining operators are standard, so we do not discuss them further and
instead provide formal satisfaction semantics.


Satisfaction Semantics of Quantitative HyperLTL The validity judge-
ment of a property ϕ by a set of traces Φ is defined with respect to a trace
assignment Π : Vars → Φ. Here, Vars is the set of trace variables. We use
π, π1 , π2 , . . . to refer to trace variables.7 The partial function Π is a mapping
from trace variables to traces. We use the notation Π[π 7→ τ ] to refer to a trace
7
     Note the distinction between trace variables denoted by π1 , π2 , etc. and traces which
     are denoted by τ1 , τ2 , etc.
                    Verification of QHPs Using Trace Enumeration Relations        11

assignment that is identical to Π except for the trace variable π which now maps
to the trace τ . We write Π |=Φ ψ if the set of traces Φ satisfies the property
ψ under the trace assignment Π. We will drop the subscript Φ from |=Φ if it
is clear from the context or irrelevant. The notation Π [i,∞] is an abbreviation
for the new trace assignment obtained by taking the suffix starting from index
i of every trace in Π: Π [i,∞] (π) = Π(π)[i,∞] for every trace π ∈ dom(Π) where
dom(Π) is the domain of Π. We write Π 6|=Φ ψ when Π |=Φ ψ is not satisfied.
Satisfaction rules for HyperLTL formulas are shown in Figure 5.
Definition 2 (Quantitative HyperLTL Satisfaction). We say that the tran-
sition system M satisfies the property ψ, denoted by M |= ψ if the empty trace
assignment ∅ satisfies formula ψ for the set of traces ΦM , that is ∅ |=ΦM ψ.

Additional Operators: The above showed the minimal set of operators required
in Quantitative HyperLTL. The rest of this paper will use the other standard
operators such as ∧ (conjunction), ⇒ (implication), F (future/eventually) and
G (globally/always) which can be defined in terms of the operators in Figure 4.

Well-defined Formulas: In order for the semantics of Quantified HyperLTL to
be meaningful, we need certain semantic restrictions on the structure of QHPs.
Definition 3 (Well-defined QHPs). An instance of a counting quantifier #π:
∆πj ,πk . ϕ ⊳ N (Z) is said to be well-defined if:
1. ¬∆πj ,πk is an equivalence relation over the set of all traces Φ, and
2. In every set of the traces ΦC captured by the counting quantifier in the se-
   mantics shown in Figure 5, the term N (Z) has the same valuation for all
   initial states: ∀τi , τj ∈ ΦC . τi0 (N (Z)) = τj0 (N (Z)).
    A Quantified HyperLTL formula is said to be well-defined if every instance
of a counting quantifier in the formula is well-defined.

Example 1 (Well-defined QHPs). The QHPs presented in the rest of this paper
are all well-defined, so here we give an example of a QHP that is not well-defined.
Consider this variant of Property 1: ∀π0 .#π1 : true. G (ψπ0 ,π1 ) ≥ 2R − 1. This
is not a well-defined QHP because ∆πj ,πk in the counting quantifier is simply
true, and its negation is not an equivalence relation over the set of traces.

    Note that condition (1) in the definition above affects ∆πj ,πk while condition
(2) places a restriction on ϕ. The former condition prevents double-counting of
traces, while the latter ensures that the trace count is unambiguous.
    The properties in our experiments require only syntactic checks to verify
well-definedness. Specifically, ∆πj ,πk is always of the form F (Pπj ,πk ) where P
                           .
is of the form P(σ1 , σ2 ) = f (σ1 ) 6= f (σ2 ). The negation of this is obviously an
equivalence relation over the set of all traces. Secondly, our QHPs are of the
form ∀π0 . #π1: ∆πj ,πk . ϕ ⊳ N (Z) where ϕ enforces equality of the variables in
Z between the traces π0 and π1 . These two features guarantee well-definedness.
In the rest of this paper, we only consider well-defined QHPs.
12       Shubham Sahai, Pramod Subramanyan, and Rohit Sinha

3.2    Applications of QHPs in Security Specification
Deniability: Our first example of a quantitative hyperproperty is deniability.
Suppose obs(σ) is a term that corresponds to the adversary observable part of
the state σ, while secret(σ) corresponds to the secret component of the state
σ. Deniability is satisfied when every trace of adversary observations can be
                                                                               .
generated by at least N (Z) different secrets. For this, we define δ(σ1 , σ2 ) =
                                               .
secret (σ1 ) 6= secret (σ2 ) and ≈O (σ1 , σ2 ) = obs(σ1 ) = obs(σ2 ).

                      ∀π0 .#π1: F (δπj ,πk ). G (≈O
                                                  π0 ,π1 ) ≥ N (Z)




               τ1   τ10       τ11      τ12       τ13    ...      τ1k      ...

                    ≈O       ≈O        ≈O       ≈O               ≈O

               τ2   τ20       τ21      τ22       τ23    ...      τ2k      ...

                    ≈O       ≈O        ≈O       ≈O               ≈O

               τ3   τ30       τ31      τ32       τ33    ...      τ3k      ...

                .
                .
                .   ≈O       ≈O        ≈O       ≈O               ≈O

               τC   τC0       τC1      τC2       τC3    ...      τCk      ...




                             Fig. 6: Illustrating deniability.


    Figure 6 illustrates deniability. It shows a set of traces ΦC := {τ1 , τ2 , . . . , τC };
the circles represent the states in each trace and the secret values are shown
by color of the circle. For these traces, every pair of corresponding states have
the same observations: represented by ≈O , and every distinct pair of traces
differ in the secrets. Deniability is satisfied if |ΦC | ≥ N (Z). Satisfaction implies
that every trace of adversary observations has at least N (Z) counterparts with
identical observations but different values of secret (σ). If we can show in a system
satisfying deniability that each trace of secrets is equiprobable and N (Z) grows
exponentially in some parameters of the system, then we can conclude that
the system satisfies computational indistinguishability. Deniability can capture
probabilistic notions of confidentiality, such as confidentiality of Path ORAM.

Soundness: While deniability encodes a form of confidentiality, soundness is its
dual in the context of integrity. One example of soundness was given in § 2.2
for the Z-K hats puzzle. Soundness is generally applicable to protocols that of-
fer probabilistic integrity guarantees. For instance, many interactive challenge-
response protocols which consist of repeated rounds such that if the prover suc-
ceeds in all rounds, the verifier can be convinced with high probability that the
prover is not cheating. This can be viewed as a QHP stating that for every trace
                      Verification of QHPs Using Trace Enumeration Relations     13

in which a dishonest prover tricks a verifier into accepting an invalid proof, there
are at least N (Z) other traces with different prover responses in which the cheat-
ing is detected. As usual, we require that traces be uniformly sampled from a
finite set in order to state soundness as a QHP.
    Soundness is stated as ∀π0 .#π1 : F (δπj ,πk ). G (ψπ0 ,π1 ) ≥ N (Z). The rela-
tion δ is defined as two states having different prover responses. ψ requires the
challenge-response protocol to fail in π1 if it succeeded in π0 and also that the
system parameters (the variables in Z) be identical between π0 and π1 .


              τ1     τ10      τ11      τ12      τ13    ...    τ1i      ...
                     ≈I


                              ≈I


                                       ≈I


                                                ≈I




                                                              ≈I
              τ2     τ20      τ21      τ22      τ23    ...    τ2i      ...
                     ≈I


                              ≈I


                                       ≈I


                                                ≈I




                                                              ≈I
              τ3     τ30      τ31      τ32      τ33    ...    τ3i      ...

              ..


                                                              ≈I
                     ≈I


                              ≈I


                                       ≈I


                                                ≈I



               .

             τC      τn0      τn1      τn2      τn3   ...     τni      ...



                   Fig. 7: Illustrating quantitative non-interference.



Quantitative Non-interference: In contrast to the above examples, which lower-
bounded the number of traces, quantitative non-interference [49, 57] upper-
bounds the amount of information that an attacker can gain from any single
trace of attacker-supplied inputs. It is shown in Figure 7 and stated as follows:

                       ∀π0 .#π1: F (δπj ,πk ). G (≈Iπ0 ,π1 ) ≤ N (Z)

    In the above, the condition ≈I encodes the fact that the traces π0 and π1
                                                         .
have the same set of attacker inputs: ≈I (σ1 , σ2 ) = inp(σ1 ) = inp(σ2 ). The
relation δ requires the states σ1 and σ2 have different attacker observations:
            .
δ(σ1 , σ2 ) = obs(σ1 ) 6= obs(σ2 ). The property is counting the number of different
attacker observable outputs for any given input. Assuming that attacker inputs
are equiprobable, quantitative non-interference implies that the maximum infor-
mation an attacker can learn from any single trace is lg(N (Z)) bits.

Summarizing QHP Specification: These examples demonstrate that QHPs
have important applications in security verification. They capture probabilistic
14      Shubham Sahai, Pramod Subramanyan, and Rohit Sinha

notions of both confidentiality and integrity. In particular, the following form
of QHPs consisting of a single quantifier alternation seems especially relevant
for security verification: ∀π0 . #π1 : ∆πj ,πk . ϕ ⊳ N (Z). Each of the examples
of quantitative hyperproperties discussed in the previous subsection – deniabil-
ity, soundness, and quantitative non-interference [49, 57] fit in this template.
Therefore, in the rest of this paper, we focus on developing scalable verification
techniques for QHPs that follow this template.


4     Trace Enumerations

This section introduces the notion of a trace enumeration, which is a technique
that allows us to reduce the problem of counting traces to that of counting
satisfiable assignments to a formula in FOL(T ).


4.1   Trace Enumeration Relations

We now formalize injective trace enumerations which allows us to lower-bound
the number of traces captured by a counting quantifier in a QHP.

Definition 4 (Injective Trace Enumeration). Let us consider a transition
system M = hX, Init(X), Tx (X, X ′ )i and the relation U(Y, τ1 , τ2 ) where Y is a
set of variables disjoint from X, τ1 and τ2 are traces of this transition system.
Let ∀π0 . #π1 : ∆πj ,πk . ϕ ≥ N (Z) be a QHP where Z ⊂ X. Suppose V(Y, Z)
is a predicate over the variables in Y and Z. We say that the pair V(Y, Z) and
U(Y, τ1 , τ2 ) form an injective trace enumeration of the system M for the QHP
∀π0 . #π1: ∆πj ,πk . ϕ ≥ N (Z) iff the following conditions are satisfied:

1. For every trace τ0 in ΦM and every satisfying assignment (Y, Z) for the pred-
   icate V(Y, Z), there exists a trace τ1 ∈ ΦM which is related to the trace τ0 as
   per the relation U via this same assignment to Y . Further, the pair τ0 and
   τ1 satisfy the property ϕ and the valuation of the variables in Z in the initial
   state of τ1 is equal to Z.

       ∀τ0 ∈ ΦM , Y, Z. V(Y, Z) ⇒                                                     (2)
          ∃τ1 ∈ ΦM . U(Y, τ0 , τ1 ) ∧ {π0 7→ τ0 , π1 7→ τ1 } |= ϕ ∧ τ10 (Z) = Z
                                                                                  


2. Different assignments to the variables in Y for the formula V(Y, Z) enumer-
   ate different traces in U(Y, τ0 , τ1 ), where “different” means satisfaction of
   ∆πj ,πk .

          ∀τ0 , τ1 , τ2 ∈ ΦM , Y1 , Y2 , Z.                                           (3)
             V(Y1 , Z) ∧ V(Y2 , Z) ∧ Y1 6= Y2                                  ⇒
             U(Y1 , τ0 , τ1 ) ∧ U(Y2 , τ0 , τ2 ) ∧ τ10 (Z) = Z ∧ τ20 (Z) = Z   ⇒
             {πj 7→ τ1 , πk 7→ τ2 } |= ∆πj ,πk
                       Verification of QHPs Using Trace Enumeration Relations               15

    If V and U form an injective trace enumeration M for the property ∀π0 . #π1:
∆πj ,πk . ϕ ≥ N (Z), then for every trace τ0 , there exist at least as many traces
satisfying the counting quantifier as there are satisfying assignments to Y in
V(Y, Z). This is made precise in the following lemma.

Lemma 1. [Trace Count Lower-Bound] If V(Y, Z) and U(Y, τ1 , τ2 ) form an in-
jective trace enumeration of the system M for the QHP ∀π0 . #π1: ∆πj ,πk . ϕ ≥
N (Z) and if #Y. V(Y, Z) is finite for all assignments to Z, then M |= ∀π0 .#π1:
∆πj ,πk . ϕ ≥ #Y. V(Y, Z).

Example 2 (Injective Trace Enumeration). Let P0 [1], . . . , P0 [R] be a trace of cor-
rect responses for some particular sequence of challenges for our running ex-
ample. Consider the array Y[1], Y[2], . . . , Y[R] where each Y[j] ∈ {0, 1}. Y is a
boolean array of size R, and Y[i] = 1 means that the prover gives an incorrect
response to the challenge in round i. We can define the predicate V as follows.
            .                                                                
   V(Y, R) = ∃i. 1 ≤ i ≤ R ∧ Y[i] 6= 0 ∧ ∀i. (i < 1 ∨ i > R) ⇒ Y[i] = 0            (4)

    The above definition ensures that at least one response is incorrect. Notice
that for every assignment to Y except the assignment of all zeros, the trace of
responses defined by ∀j. P1 [j] = P0 [j]⊕Y[j] (where ⊕ is exclusive or) corresponds
to a valid trace of the system and satisfies the counting quantifier in Property 1.
Specifically, every such response from the prover is incorrect and will result in the
protocol failing. We can use the above facts to define the relation U as follows:
                  .
   U(Y, τ1 , τ2 ) = ∀j. τ10 (P[j]) = τ20 (P[j]) ⊕ Y[j]
                                                      
                                                                            ∧ (5)
                  τ10 (C) = τ20 (C) ∧ τ10 (R) = τ20 (R) ∧ (τ1R (S) ⇒ ¬τ2R (S))

The pair V and U form an injective trace enumeration for the system M (defined
in Figure 1) for the Property 1. This is because different Y’s will result in different
prover responses for the same challenges. By Lemma 1, we can conclude that
Property 1 is satisfied if #Y. V(Y, R) ≥ 2R − 1

   We now define the notion of a surjective trace enumeration, which makes it
possible to upper bound the number of traces captured by a counting quantifier.

Definition 5 (Surjective Trace Enumeration). A trace enumeration of the
system M consisting of the pair of predicates V(Y, Z) and U(Y, τ1 , τ2 ) is said to
be surjective for the QHP ∀π0 . #π1: ∆πj ,πk . ϕ ≤ N (Z) on the system M if the
following conditions are satisfied.

1. Every pair of traces of M which satisfy the formula ϕ can be related via the
   relation U for some values (Y, Z) satisfying V(Y, Z) such that the valuation
   of the variables in Z in the initial state of τ1 is equal to Z.

     ∀τ0 , τ1 ∈ ΦM .                                                                        (6)
                                        ∃Y, Z. V(Y, Z) ∧ U(Y, τ0 , τ1 ) ∧ τ10 (Z) = Z
                                                                                        
        {π0 7→ τ0 , π1 7→ τ1 } |= ϕ ⇒
16      Shubham Sahai, Pramod Subramanyan, and Rohit Sinha

2. Distinct traces, as defined by satisfaction of ∆πj ,πk , must result in different
   assignments to Y satisfying V(Y, Z).

          ∀τ0 , τ1 , τ2 ∈ ΦM , Y1 , Y2 , Z.                                     (7)
              {πj 7→ τ1 , πk 7→ τ2 } |= ∆πj ,πk ∧ τ10 (Z) = τ20 (Z) = Z     ⇒
              {π0 7→ τ0 , π1 7→ τ1 } |= ϕ ∧ {π0 7→ τ0 , π1 7→ τ2 } |= ϕ     ⇒
              U(Y1 , τ0 , τ1 ) ∧ U(Y2 , τ0 , τ2 ) ∧ V(Y1 , Z) ∧ V(Y2 , Z)   ⇒
              Y1 6= Y2

   Analogous to injective trace enumerations, surjective enumerations can be
used to upper-bound the number of traces satisfying the counting quantifier.

Lemma 2. [Trace Count Upper-Bound] If the pair V(Y, Z) and U(Y, τ1 , τ2 ) form
a surjective trace enumeration of the system M for the QHP formula
∀π0 . #π1: ∆πj ,πk . ϕ ≤ N (Z) and if #Y. V(Y, Z) is finite for every assignment
to Z, then M |= ∀π0 .#π1: ∆πj ,πk . ϕ ≤ #Y. V(Y, Z).

Example 3 (Surjective Trace Enumeration). The definitions of V and U provided
in Equations 4 and 5 are also surjective trace enumerations, for the transition
system shown in Figure 1, with respect to Property 1. As a result, Lemmas 1
and 2 together give us a tight bound of #Y. V(Y, R), and therefore a tight bound
on the number of satisfying traces for the counting quantifier in Property 1.


5     Model Counting

As discussed in the previous section, trace enumeration relations can bound the
number of satisfying traces in a QHP. Given a QHP ∀π0 . #π1 : ∆πj ,πk . ϕ ⊳
N (Z), appropriate trace enumeration predicates V(Y, Z) and U can be used to
derive that ∀π0 . #π1: ∆πj ,πk . ϕ ⊳ #Y. V(Y, Z). The final step in our verification
methodology is to show validity of #Y. V(Y, Z) ⊳ N (Z). To that end, this section
discusses our novel technique for model counting.


5.1   Model Counting via SMT Solving

Our approach borrows ideas from enumerative combinatorics [13, 55, 59] and
introduces the inference rules shown in Figure 8 to reason about model counts for
formulas in FOL(T ). Each of the conclusions in the inference rules is a statement
involving model counts of FOL(T ) formulas, while each of the premises is a
formula in FOL(T ) that does not involve model counts and can, therefore, be
checked using SAT/SMT solvers. We describe these inference rules next.

Range: This rule states that the number of satisfying assignments in the variable
i to a formula of the form a ≤ i < b is b − a if b ≥ a and zero otherwise. This
rule forms one of the “base cases” in our derivations.
                    Verification of QHPs Using Trace Enumeration Relations         17

Positive: This rule states that the number of satisfying assignments is always
greater than or equal to zero. We will use this in conjunction with other rules
which upper bound the number of satisfying solutions to formulas.

ConstLB and ConstUB: If a formula f (X) has c distinct solutions, we can con-
clude that the #X. f (X) is lower-bounded by c. ConstUB is the converse of
ConstLB . It states that if a formula does not have c distinct solutions, f (X)
definitely has fewer than c satisfying assignments in X.

UB: If we have two formulas f (X) and g(X) such that f (X) ⇒ g(X), this
means that g(X) has at least as many satisfying solutions as f (X).

Injectivity: This rule is based on the following idea from enumerative combina-
torics. Suppose we have two sets A and B. We can show that |A| ≤ |B| if there
exists an injective function from A to B. Translating this to model counts, the
set A in the rule corresponds to satisfying assignments to f (X), B corresponds
to satisfying assignments to g(Y ) and F is the injective witness function.

Ind≥ and Ind≤ : Suppose the formulas f (X, n) and g(Y, n) are parameterized by
the integer variable n. If an injective witness function G (X, Y, n) is able to “lift”
satisfying assignments of f (Xn , n) and g(Yn , n) into a satisfying assignment of
f (Xn+1 , n + 1), then we can conclude that the number of satisfying assignments
to f (X, n + 1) are at least as many as the product of the number of satisfying
assignments to f (X, n) and g(Y, n). Ind ≤ is the surjective version of this rule.
It applies when a satisfying assignment to f (Xn+1 , n + 1) can be “lowered” into
satisfying assignments to f (Xn , n) and g(Yn , n) where the values of Xn and Yn
are given by the witness functions Hx and Hy respectively.


5.2   Model Counting in the Motivating Example

The definition of the predicate V in the motivating example is shown below.
            .                                                            
  V(Y, R) = ∃i. 1 ≤ i ≤ R ∧ Y[i] 6= 0 ∧ ∀i. ((i < 1 ∨ i > R) ⇒ Y[i] = 0)

    Our task is to show #Y. V(Y, R) = 2R − 1. Recall that Y is an array of
binary values (i.e. the integers 0 and 1) and consider the following predicates:
          .                                                .               
Vf (Y, R) = ∀i. (i < 1 ∨ i > R) ⇒ Y[i] = 0 , V1 (Y, R) = ∀i. Y[i] = 0 and
       .
W(i) = 0 ≤ i < 2. Using these definitions, the proof is as follows.

 1. (ConstUB , Positive) #Y. Vf (Y, R) ∧ V1 (Y, R) = 1.
 2. (Or ) #Y. Vf (Y, R) = #Y. V(Y, R) + #Y. V1 (Y, R).
 3. (ConstLB , ConstUB ) #Y. V1 (Y, R) = 1.
 4. (ConstLB , ConstUB ) #Y. Vf (Y, 1) = 2.
 5. (Ind ≤ ): #Y. Vf (Y, R) ≤ #i. W(i) × #Y. Vf (Y, R − 1).
 6. (Ind ≥ ): #Y. Vf (Y, R) ≥ #i. W(i) × #Y. Vf (Y, R − 1).
 7. (Range): #i. W(i) = 2.
18         Shubham Sahai, Pramod Subramanyan, and Rohit Sinha


                                                   Range                          Positive
           (#i. a ≤ i < b) = max (b − a, 0)                       #Y. f (X) ≥ 0
                     Vc
                       i=1 f (Xi ) ∧ distinct (X1 , . . . , Xc ) is sat
                                                                         ConstLB
                                   #X. f (X) ≥ c
                   Vc
                      i=1 f (Xi ) ∧ distinct (X1 , . . . , Xc ) is unsat
                                                                          ConstUB
                                   #X. f (X) < c
                                  f (X, Y ) ⇒ g(X, Y )
                                                           UB
                              #X. f (X, Y ) ≤ #X. g(X, Y )
                             h(X, Y ) ⇔ f (X) ∧ g(Y )
                                                              AndUB
                    #X ∪ Y . h(X, Y ) ≤ #X. f (X) × #Y. g(Y )
                                  f (X) ⇒ g(F (X))
                                             
                 f (X1 ) ∧ f (X2 ) ∧ X1 6= X2 ⇒ F (X1 ) 6= F (X2 )
                                                                         Injectivity
                              #X. f (X) ≤ #Y. g(Y )
                      h(X, Y ) ⇔ f (X) ∧ g(Y ) X ∩ Y = ∅
                                                              Disjoint
                    #X ∪ Y . h(X, Y ) = #X. f (X) × #Y. g(Y )
                               f (X, Y ) ⇔ g(X, Y ) ∨ h(X, Y )
                                                                                     Or
      #X. f (X, Y ) = #X. g(X, Y ) + #X. h(X, Y ) − #X. g(X, Y ) ∧ h(X, Y )
                                        
                      f (X, n) ∧ g(Y, n) ⇒ f (G (X, Y, n), n + 1)
                (X1 6= X2 ∨ Y1 6= Y2 ) ⇒ G (X1 , Y1 , n) 6= G (X2 , Y2 , n)
                                                                            Ind≥
                   #X. f (X, n + 1) ≥ #X. f (X, n) × #Y. g(Y, n)
                                                                            
             f (X, n + 1) ⇒ f (Hx (X, n + 1), n) ∧ g(Hy (X, n + 1), n)
                                                                               
        X1 6= X2 ⇒ Hx (X1 , n) 6= Hx (X2 , n) ∨ Hy (Y1 , n) 6= Hy (Y2 , n)
                                                                                 Ind≤
                   #X. f (X, n + 1) ≤ #X. f (X, n) × #Y. g(Y, n)


Fig. 8: Model counting proof rules. Unless otherwise specified, premises are satis-
fied when the formula is valid. Conclusions have an implicit universal quantifier.



 8. (4 – 7) imply that #Y. Vf (Y, R) = 2 × #Y. Vf (Y, R − 1), #Y. Vf (Y, 1) = 2,
    this means #Y. Vf (Y, R) = 2R .
 9. (2, 3, 8) imply that #Y. V(Y, R) = 2R − 1.

                                                  .
   In step 5, the witness function is G (Y, R, i) = Y[R + 1 7→ i], while in step 6,
                           .                                        .
they are HhY,Ri (Y, R + 1) = hY[R + 1 7→ 0], Ri and Hi (Y, R + 1) = (Y[R + 1]).8
Note steps 8 and 9 are automatically discharged by the SMT solver.


8
     The notation arr [i 7→ v] denotes an array that is identical to arr except for index i
     which contains v.
                   Verification of QHPs Using Trace Enumeration Relations        19

6     Experimental Results and Discussion

In this section, we present an experimental evaluation of the use of trace enu-
merations for the verification of quantitative hyperproperties.


6.1   Methodology

We studied five systems with varying complexity and QHPs. These were modeled
in the Uclid5 modeling and verification framework [46, 54], which uses the Z3
SMT solver (v4.8.6) [24] to discharge the proof obligations. The experiments
were run on an Intel i7-4770 CPU @ 3.40GHz with 8 cores and 32 GB RAM.
    The verification conditions are currently manually generated from the mod-
els, but automation of this is straightforward and ongoing. The k-trace properties
were proven using self-composition [9, 10] and induction. A number of strength-
ening invariants had to be specified manually for the inductive proofs. Many
of the invariants are relational and quantified and, therefore, difficult to infer
algorithmically. We note that recent work has made progress toward automated
inference of quantified invariants [29, 38].


Implementation Issues: In addition to the techniques in Sections 4 and 5,
we must address two additional practical challenges. The first challenge is the
definition of U(Y, τ1 , τ2 ) as some general relation over traces. This poses dif-
ficulties in our proofs which rely on induction. Hence, we impose a syntactic
restriction on the relation U by constraining it to be a relational hyperinvariant
                                                                                   .
of the transition system. In other words, U has the following form: U(Y, τ1 , τ2 ) =
∀i. E(Y, τ1i (X), τ2i (X)). This allows using induction and self-composition [9, 10,
53] to verify that a relation is indeed a trace enumeration predicate.
    The second challenge is the quantifier alternation. Definitions 4 and 5 involve
quantifier alternation over trace variables and verification of such hyperproper-
ties is challenging. We address this problem by manually specifying Skolem wit-
ness functions for the existential quantifiers [48]. Note that utilizing a Skolem
function in this context is not straightforward because we need to construct
a witness function for an infinitely long trace. We side-step the issue by con-
structing a witness function for the initial state of the corresponding trace and
imposing an additional condition requiring that if the initial states of two traces
are related via the relation E, then all subsequent states must also be related.


6.2   Overview of Results

Due to limited space, we only provide a brief description of our benchmarks for
evaluation and refer the interested reader to Appendix B for a more detailed
discussion. We have also made the models and associated proof scripts available
at [27]. A brief overview of the case studies follows.
20      Shubham Sahai, Pramod Subramanyan, and Rohit Sinha


                     Table 1: Verification Results of Models.

Benchmark               Hyperproperty                Model Proof    Num. Verif.
                                                     LoC   LoC      Annot. Time
Electronic Purse [7]    Deniability                   46     93     9       3.92s
Password checker [31]   Quantitative non-interference 59     100    10      4.69s
F-Y Array Shuffle       Quantitative information flow 86     195    96      7.38s
ZK Hats (Sec. 2.2)      Soundness                     91     191    36      6.34s
Path ORAM [51]          Deniability                   587    209    142     9.74s




 1. Electronic Purse. We model an electronic purse, with a secret initial bal-
    ance, proposed by Backes et al. [7]. A fixed amount is debited from the purse
    until the balance is insufficient for the next transaction. We prove a denia-
    bility property: there is a sufficient number of traces with identical attacker
    observations but different initial balances.
 2. Password Checker. We model the password checker from Finkbeiner et
    al. [31], but we allow passwords of unbounded length n. We prove quantita-
    tive non-interference: information leakage to an attacker is ≤ n bits.
 3. Array Shuffle. We implement a variant of the Fisher-Yates shuffle. We
    chose this because producing random permutations of an array is an impor-
    tant component of certain cryptographic protocols (e.g., Ring ORAM [43]).
    We prove a quantitative information flow property stating that all possible
    permutations are indeed generated by the shuffling algorithm.
 4. ZK Hats. We prove soundness of the zero-knowledge protocol in Section 2.
 5. Path ORAM. Discussed in Section 6.3.
The properties we prove on these models and the results of our evaluation are pre-
sented in Table 1 which shows the size of each model, the number of lines of proof
code (this is the code for self-composition, property specification, etc.), the num-
ber of verification annotations (invariants and procedure pre-/post-conditions)
and the verification time for each example. Once the auxiliary strengthening
invariants are specified, the verification completes within a few seconds. This
suggests that the methodology can scale to larger models, and even implemen-
tations. The main challenge in the application of the methodology is the con-
struction of the trace enumeration relations, associated witness functions, and
the specification of strengthening invariants. Each of these requires application-
specific insight. Since most of our enumerations and invariants are quantified,
some of the proofs also required tweaking the SMT solver’s configuration options
(e.g. turning off model-based quantifier instantiation in Z3).

6.3   Deniability of Path ORAM
In this section, we discuss our main case study: the application of trace enumer-
ations for verifying deniability of server access patterns in Path ORAM [51], a
                    Verification of QHPs Using Trace Enumeration Relations       21

practical variant of Oblivious RAM (ORAM) [35]. ORAMs refer to a class of
algorithms that allow a client with a small amount of storage to store/load a
large amount of data on an untrusted server while concealing the client access
pattern from the server. Path ORAM stores encrypted data on the server in an
augmented binary tree format. Each node stores Z data blocks, referred to as
buckets of size Z. Additionally, the client has a small amount of local storage
called the stash. The client maintains a secret mapping called the position map
to keep track of the path where a data block is stored on the server. Each entry
in the position map maps a client address to a leaf on the server. Path ORAM
maintains the invariant that every block is stored somewhere along the path
from the root to the leaf node that the block is mapped to by the position map.
The position map is initialized randomly, and an entry of the position map is
updated after every access to that location.


 Algorithm 1: Oram Access Protocol
     Secret Input : OP, request, data∗
     Public Output : leaf                                   /* Accessed Leaf */
 1 leaf ← pMap[request]
 2 pMap[request] ← UniformRandom(1, numBlks)                 /* remap */
 3 stash ← stash ∪ ReadPath(leaf)
 4 if OP = WRITE then
 5      UpdateData(stash, request, data∗ )
 6   WritePath(leaf, stash)



    The Path ORAM access function shown in Algorithm 1 can be logically
divided into 5 steps: (1) getting the mapped leaf corresponding to the requested
data block, (2) updating the position map entry for the accessed data block, (3)
reading the path on the server corresponding to the leaf, (4) updating the data
in case of a write operation, and (5) writing the data blocks back from stash to
the path read from ORAM.
    Our model of Path ORAM is a transition system where each step corresponds
to a single execution of the access function for an arbitrary operation and address.
The model has an unbounded size tree and stash. Each bucket contains four
nodes – this is the recommended configuration for Path ORAM [51]. The model
makes uses of various uninterpreted functions for abstraction, e.g. modeling the
path from the root of the tree to a leaf.

Deniability of Server Access Patterns in Path ORAM: Intuitively, the
security of path ORAM requires that the adversary (untrusted server) learns
nothing about the access pattern of the client by observing server accesses. In
Path ORAM, the position map is initialized randomly and every subsequent up-
date to the position is also done by sampling from a uniform random distribution.
Hence every secret position map is equally likely to be chosen. We formulate
22            Shubham Sahai, Pramod Subramanyan, and Rohit Sinha


    (a)               3                             4                        2

              1                             1                        1               4
                                                                                             ...
                  4       2                     3       2                3
          0       1       2     3       0       1       2   3    0       1       2       3
      p= [0, 2, 1, 1] r= 4             p= [0, 2, 1, 3] r= 2     p= [0, 3, 1, 3] r= 1

    (b)               4                             2                        2

              3                             3                        3               1
                                                                                             ...
                  2       1                     4       1                4
          0       1       2     3       0       1       2   3    0       1       2       3
      p= [2, 1, 0, 1] r= 2             p= [2, 3, 0, 1] r= 1     p= [3, 3, 0, 1] r= 3


 Fig. 9: Path ORAM systems satisfying the counting quantifier of Equation 8.


security of access patterns in Path ORAM as a deniability property stating that
for every infinitely-long trace of server accesses, there are (numBlks − 1)! traces
of client accesses with identical server observations but different client requests.

                          ∀π0 . #π1 : F (δ πj ,πk ). G (ψπ0 ,π1 ) ≥ (numBlks − 1)!            (8)

The binary predicate δ imposes the requirement that the client’s request are
different in each of the traces captured by the counting quantifier, and the con-
dition in ψ states that all the traces captured by the counting quantifier have
the same observable access pattern as π0 .


Verification of Deniability in Path ORAM: To verify the QHP stated in
Equation 8, for every trace of server accesses we need to generate (numBlks − 1)!
traces of client requests that produce the same server access.
   Suppose we have Path ORAM (a) that is initialized with some position map.
Now consider the Path ORAM (b) with the same number of blocks, but with
an initial position map that is a derangement of the position map of (a).9 The
key insight is that ORAM (b) can simulate an identical server access pattern
as ORAM (a) by appropriately choosing a different client request that maps to
the same leaf that is being accessed by (a) and then updating the position map
identically as (a). This is shown in Figure 9, which shows two Path ORAMs that
produce identical server access patterns but service different client requests.
9
     A derangement of a set is a permutation of the elements of the set such that no
     element appears in its original position.
                    Verification of QHPs Using Trace Enumeration Relations          23

   The above insight leads to the following trace enumeration. V(Y, W, numBlks)
captures the notion of a valid derangement:
                     .
  V(Y, W, numBlks) =
                                                
    ∀i. 1 ≤ i ≤ numBlks . Y[i] 6= i ∧ W[i] 6= i                            ∧
    ∀i. 1 ≤ i ≤ numBlks =⇒ 1 ≤ Y[i] ≤ numBlks ∧ 1 ≤ W[i] ≤ numBlks         ∧
    ∀i, j. (1 ≤ i ≤ numBlks ∧ 1 ≤ j ≤ numBlks ∧ i 6= j) =⇒
                                                              
                               (Y[i] 6= Y[j]) ∧ (W[i] 6= W[j])         ∧
                                                            
    ∀i. i < 0 ∨ i > numBlks =⇒ (Y[i] = 0) ∧ (W[i] = 0)                 ∧
                                                                   
    ∀i. 1 ≤ i ≤ numBlks . ∃j. 1 ≤ j ≤ numBlks. W[i] = j =⇒ Y[j] = i     (9)
Every satisfying assignment to the above is a derangement Y and its inverse W.
These can be used to permute the client’s accesses in ORAM (a) so that the
server accesses made by ORAM (b) are identical to those of ORAM (a).
    Next we define the relation U.
                    .
U({Y, W}, τ1 , τ2 ) = τ10 (numBlks) = τ20 (numBlks) ∧ τ10 (stashSz) = τ20 (stashSz) ∧
                       ∀i. ∀j. τ2i (pMap[j]) = τ1i (pMap[Y[j]])
                                                               
                                                                                     ∧
                             i                i
                                                           
                       ∀i. τ2 (request) = τ1 (W[request])                            ∧
                             i           i
                                                
                       ∀i. τ1 (leaf) = τ2 (leaf)                                     ∧
                             i              i
                                                     
                       ∀i. τ1 (remap) = τ2 (remap)                                 (10)
    U relates two traces which are such that the position map of one is a permu-
tation of the other, their client requests are appropriately permuted, and have
identical access patterns and position map updates.

Discussion: It is important to note that deniability of the access pattern is
just one aspect of the security of Path ORAM. Path ORAM also requires that
the data stored on the server be encrypted and authenticated using randomized
authenticated encryption algorithm. Verifying these aspects of Path ORAM is
unrelated to quantitative hyperproperties, so we do not incorporate them in our
model.

7    Related Work
Hyperproperties: Research into secure information flow started with the semi-
nal work of Denning and Denning [25], Goguen and Meseguer [34] and Rushby [45].
The self-composition construction for the verification of secure information flow
was introduced by Barthe et al. [10]. Terauchi and Aiken identified the class
of k-safety properties [53], which is an important subset of the class of hy-
perproperties. Clarkson and Schneider [22] introduced the class of specifica-
tions called hyperpropertiesand showed that both noninterference and observa-
tional determinism [44, 58], as well many other security specifications were in-
stances of hyperproperties. Clarkson and colleagues also introduced HyperLTL
24      Shubham Sahai, Pramod Subramanyan, and Rohit Sinha

and HyperCTL∗ [20], which are temporal logics for specifying hyperproperties,
while verification algorithms for these were introduced by Finkbeiner and col-
leagues in [32]. Cartesian Hoare Logic [50] was introduced by Sousa and Dillig
and enables the specification and verification of hyperproperties over programs
as opposed to transition systems. A number of subsequent efforts have studied
hyperproperties in the context of program verification [5, 28, 47, 56].
Quantitative Information Flow: Quantitative hyperproperties build on the
rich literature of quantitative information flow (QIF) [3, 18, 21, 36, 49]. The QIF
problem is to quantify (or bound) the number of bits of secret information that
is attacker-observable. Certain notions of QIF can be expressed as QHPs. It is
important to note QHPs can express security specifications (e.g., soundness) that
are not QIF. Yasuoka and Terauchi studied QIF from a theoretical perspective
and showed that it could be expressed as hypersafety and hyperliveness [57].
They have the first construction to show that QIF with a constant bound of b
bits can be expressed as a k-safety property where k = 2b + 1. In principle, this
means that QIF can be expressed as HyperLTL/HyperCTL [20] formulas and
verified using the self composition-based algorithm in [32] assuming the bound is
static. Approaches based on QIF measures such as min-entropy [49], Shannon
entropy [19] etc. have also been applied in the context of static analysis [40].
QIF has been studied for specific applications; e.g. cache-based side-channel
attacks [26, 40] and web applications [17, 42, 61]. These stand in contrast to our
approach, which permits verification of a large and generic class of QHPs.
Quantitative Hyperproperties: Quantitative Cartesian Hoare Logic (QCHL)
enables verification of certain quantitative properties of programs [16]. QHPs are
more expressive than QCHL, the latter counts events within a trace (e.g. memory
accesses), while QHPs count the number of traces satisfying certain conditions.
    The most closely related work to ours is of Finkbeiner et al. [31] who intro-
duced Quantitative HyperLTL over Kripke structures. They also introduced a
verification algorithm for this logic that is based on maximum model counting.
However, their algorithm does not scale to reasonable-sized systems, and exper-
iments from their paper show that the approach times out when checking an
8-bit leak in a password checker (using 8-bit passwords). We differ from their
work in three important ways. First, our properties are defined over symbolic
transition systems rather than Kripke structures. This allows modeling and ver-
ification of QHPs over infinite-state systems. Second, our bounds are symbolic,
which enables us to express bounds as functions of transition system parameters.
Finally, our definition of Quantitative HyperLTL is also more expressive. It is
not possible to convert our QHPs into (non-quantitative) HyperLTL formulas
with k-traces for any fixed value of k.
Verification of ORAMs: In concurrent work with ours, Barthe et al. [11] and
Darais et al. [23] have introduced specialized mechanisms to prove security of
ORAMs. Barthe et al. [11] introduced a probabilistic separation logic (PSL) that
(among other things) can be used to reason about the security of ORAMs. Unlike
QHPs, PSL does not permit quantitative reasoning about probabilities of events
and also does not (yet) support machine-checked reasoning. Darais et al. [23]
                   Verification of QHPs Using Trace Enumeration Relations      25

introduce a type system that enforces obliviousness; they use this type system
to implement a tree-based ORAM. Note that QHPs can express specifications
other than obliviousness, and obliviousness need not necessarily be a QHP.


8   Conclusion
Quantitative hyperproperties are a powerful class of specifications that stipu-
late the existence of a certain number of traces satisfying certain constraints.
Many important security guarantees, especially those involving probabilistic
guarantees of security, can be expressed as quantitative hyperproperties. Un-
fortunately, verification of quantitative hyperproperties is a challenging problem
because these specifications require simultaneous reasoning about a large num-
ber of traces of a system. In this paper, we introduced a specification language,
satisfaction semantics, and a verification methodology for quantitative hyper-
properties. Our verification methodology is based on reducing the problem of
counting traces into that of counting the number of assignments that satisfy a
first-order logic formula. Our methodology enables security verification of many
interesting security protocols that were previously out of reach, including confi-
dentiality of access pattern accesses in Path ORAM.


Acknowledgements
We sincerely thank the anonymous reviewers for their insightful comments which
helped improve this paper. This work was supported in part by the Semicon-
ductor Research Corporation under Task 2854 and the Science and Engineering
Research Board of India, a unit of the Department of Science and Technology,
Government of India.
                             Bibliography


 [1] José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, and François Du-
     pressoir. Verifiable side-channel security of cryptographic implementations:
     constant-time mee-cbc. In International Conference on Fast Software En-
     cryption, pages 163–184. Springer, 2016.
 [2] José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, François Dupres-
     soir, and Michael Emmi. Verifying constant-time implementations. In 25th
     USENIX Security Symposium, USENIX Security., pages 53–70, 2016.
 [3] Mário S Alvim, Miguel E Andrés, and Catuscia Palamidessi. Quantita-
     tive information flow in interactive systems. Journal of Computer Security,
     20(1):3–50, 2012.
 [4] Timos Antonopoulos, Paul Gazzillo, Michael Hicks, Eric Koskinen, Tachio
     Terauchi, and Shiyi Wei. Decomposition instead of self-composition for
     proving the absence of timing channels. In PLDI, pages 362–375, 2017.
 [5] Timos Antonopoulos, Paul Gazzillo, Michael Hicks, Eric Koskinen, Tachio
     Terauchi, and Shiyi Wei. Decomposition instead of self-composition for
     proving the absence of timing channels. In Proceedings of the 38th ACM
     SIGPLAN Conference on Programming Language Design and Implementa-
     tion, PLDI 2017, pages 362–375, New York, NY, USA, 2017. ACM.
 [6] J. Bacelar Almeida, Manuel Barbosa, Jorge S. Pinto, and Bárbara Vieira.
     Formal verification of side-channel countermeasures using self-composition.
     Sci. Comput. Program., 78(7):796–812, July 2013.
 [7] Michael Backes, Boris Kopf, and Andrey Rybalchenko. Automatic Discov-
     ery and Quantification of Information Leaks. In Proceedings of the 2009
     30th IEEE Symposium on Security and Privacy, SP ’09, pages 141–153,
     Washington, DC, USA, 2009. IEEE Computer Society.
 [8] Gilles Barthe, Gustavo Betarte, Juan Campo, Carlos Luna, and David
     Pichardie. System-level non-interference for constant-time cryptography.
     In Proceedings of the 2014 ACM SIGSAC Conference on Computer and
     Communications Security, pages 1267–1279. ACM, 2014.
 [9] Gilles Barthe, Juan Manuel Crespo, and César Kunz. Relational verifica-
     tion using product programs. In Michael Butler and Wolfram Schulte, ed-
     itors, FM 2011: Formal Methods, pages 200–214, Berlin, Heidelberg, 2011.
     Springer Berlin Heidelberg.
[10] Gilles Barthe, Pedro R. D’Argenio, and Tamara Rezk. Secure information
     flow by self-composition. In 17th IEEE Computer Security Foundations
     Workshop, (CSFW-17), pages 100–114, 2004.
[11] Gilles Barthe, Justin Hsu, and Kevin Liao. A probabilistic separation logic.
     Proc. ACM Program. Lang., 4(POPL), December 2019.
[12] Vincent Bindschaedler, Reza Shokri, and Carl A Gunter. Plausible de-
     niability for privacy-preserving data synthesis. Proceedings of the VLDB
     Endowment, 10(5):481–492, 2017.
                   Verification of QHPs Using Trace Enumeration Relations     27

[13] Anders Björner and Richard P. Stanley. A Combinatorial Miscellany.
     L’Enseignement mathématique, 2010.
[14] Anrin Chakraborti, Chen Chen, and Radu Sion. Datalair: Efficient block
     storage with plausible deniability against multi-snapshot adversaries. Pro-
     ceedings on Privacy Enhancing Technologies, 2017(3):179–197, 2017.
[15] Kevin Cheang, Cameron Rasmussen, Sanjit Seshia, and Pramod Subra-
     manyan. A formal approach to secure speculation. In 2019 IEEE 32nd
     Computer Security Foundations Symposium (CSF), pages 288–28815, June
     2019.
[16] Jia Chen, Yu Feng, and Isil Dillig. Precise detection of side-channel vul-
     nerabilities using quantitative cartesian hoare logic. In Proceedings of the
     2017 ACM SIGSAC Conference on Computer and Communications Secu-
     rity, CCS ’17, pages 875–890, New York, NY, USA, 2017. ACM.
[17] Shuo Chen, Rui Wang, XiaoFeng Wang, and Kehuan Zhang. Side-channel
     leaks in web applications: A reality today, a challenge tomorrow. In 2010
     IEEE Symposium on Security and Privacy, pages 191–206. IEEE, 2010.
[18] David Clark, Sebastian Hunt, and Pasquale Malacaria. Quantitative infor-
     mation flow, relations and polymorphic types. Journal of Logic and Com-
     putation, 15(2):181–199, 2005.
[19] David Clark, Sebastian Hunt, and Pasquale Malacaria. A static analysis for
     quantifying information flow in a simple imperative language. Journal of
     Computer Security, 15(3):321–371, 2007.
[20] Michael R Clarkson, Bernd Finkbeiner, Masoud Koleini, Kristopher K
     Micinski, Markus N Rabe, and César Sánchez. Temporal logics for hy-
     perproperties. In International Conference on Principles of Security and
     Trust, pages 265–284. Springer, 2014.
[21] Michael R Clarkson, Andrew C Myers, and Fred B Schneider. Belief in
     information flow. In 18th IEEE Computer Security Foundations Workshop
     (CSFW’05), pages 31–45. IEEE, 2005.
[22] Michael R. Clarkson and Fred B. Schneider. Hyperproperties. Journal of
     Computer Security, 18(6):1157–1210, 2010.
[23] David Darais, Ian Sweet, Chang Liu, and Michael Hicks. A language
     for probabilistically oblivious computation. Proc. ACM Program. Lang.,
     4(POPL), December 2019.
[24] L. De Moura and N. Bjørner. Z3: An Efficient SMT Solver. In Tools and
     Algorithms for the Construction and Analysis of Systems, 2008.
[25] Dorothy E. Denning and Peter J. Denning. Certification of programs for
     secure information flow. Commun. ACM, 20(7):504–513, July 1977.
[26] Goran Doychev, Boris Köpf, Laurent Mauborgne, and Jan Reineke.
     Cacheaudit: A tool for the static analysis of cache side channels. ACM
     Transactions on Information and System Security (TISSEC), 18(1):4, 2015.
[27] Experiments: Models and Proof Scripts for the paper “Verification of Quan-
     titative Hyperproperties Using Trace Enumeration Relations”. Available at
     https://github.com/ssahai/CAV-2020-benchmarks, 2020.
[28] Azadeh Farzan and Anthony Vandikas. Automated hypersafety verification.
     In Computer Aided Verification - 31st International Conference, CAV 2019,
28      Shubham Sahai, Pramod Subramanyan, and Rohit Sinha

     New York City, NY, USA, July 15-18, 2019, Proceedings, Part I, pages 200–
     218, 2019.
[29] Grigory Fedyukovich, Sumanth Prabhu, Kumar Madhukar, and Aarti
     Gupta. Quantified invariants via syntax-guided synthesis. In International
     Conference on Computer Aided Verification, pages 259–277. Springer, 2019.
[30] Andrew Ferraiuolo, Rui Xu, Danfeng Zhang, Andrew C. Myers, and G. Ed-
     ward Suh. Verification of a Practical Hardware Security Architecture
     Through Static Information Flow Analysis. In Proceedings of the Twenty-
     Second International Conference on Architectural Support for Programming
     Languages and Operating Systems, ASPLOS 2017, Xi’an, China, April 8-
     12, 2017, pages 555–568, 2017.
[31] Bernd Finkbeiner, Christopher Hahn, and Hazem Torfah. Model check-
     ing quantitative hyperproperties. In Computer Aided Verification - 30th
     International Conference, CAV 2018, Held as Part of the Federated Logic
     Conference, FloC 2018, Oxford, UK, July 14-17, 2018, Proceedings, Part I,
     pages 144–163, 2018.
[32] Bernd Finkbeiner, Markus N Rabe, and César Sánchez. Algorithms for
     model checking hyperltl and hyperctl ∗ . In International Conference on
     Computer Aided Verification, pages 30–48. Springer, 2015.
[33] Daniel J Fremont, Markus N Rabe, and Sanjit A Seshia. Maximum model
     counting. In Thirty-First AAAI Conference on Artificial Intelligence, 2017.
[34] Joseph A. Goguen and José Meseguer. Security Policies and Security Mod-
     els. In 1982 IEEE Symposium on Security and Privacy, Oakland, CA, USA,
     April 26-28, 1982, pages 11–20, 1982.
[35] Oded Goldreich and Rafail Ostrovsky. Software protection and simulation
     on oblivious rams. J. ACM, 43(3):431–473, May 1996.
[36] James W Gray III. Toward a mathematical foundation for information flow
     security. Journal of Computer Security, 1(3-4):255–294, 1992.
[37] Marco Guarnieri, Boris Köpf, José F. Morales, Jan Reineke, and Andrés
     Sánchez. SPECTECTOR: principled detection of speculative information
     flows. CoRR, abs/1812.08639, 2018.
[38] Arie Gurfinkel, Sharon Shoham, and Yakir Vizel. Quantifiers on demand.
     In International Symposium on Automated Technology for Verification and
     Analysis, pages 248–266. Springer, 2018.
[39] Chris Hawblitzel, Jon Howell, Jacob R Lorch, Arjun Narayan, Bryan Parno,
     Danfeng Zhang, and Brian Zill. Ironclad Apps: End-to-End Security via
     Automated Full-System Verification. In Proceedings of the 11th USENIX
     conference on Operating Systems Design and Implementation, pages 165–
     181, 2014.
[40] Boris Köpf, Laurent Mauborgne, and Martı́n Ochoa. Automatic quantifica-
     tion of cache side-channels. In International Conference on Computer Aided
     Verification, pages 564–580. Springer, 2012.
[41] Sujit Kumar Muduli, Pramod Subramanyan, and Sayak Ray. Verification
     of Authenticated Firmware Loaders. In Proceedings of Formal Methods in
     Computer-Aided Design. IEEE, 2019.
                   Verification of QHPs Using Trace Enumeration Relations     29

[42] Quoc-Sang Phan and Pasquale Malacaria. Abstract model counting: a novel
     approach for quantification of information leaks. In Proceedings of the 9th
     ACM symposium on Information, computer and communications security,
     pages 283–292. ACM, 2014.
[43] Ling Ren, Christopher Fletcher, Albert Kwon, Emil Stefanov, Elaine Shi,
     Marten van Dijk, and Srinivas Devadas. Constants count: Practical improve-
     ments to oblivious RAM. In 24th USENIX Security Symposium (USENIX
     Security 15), pages 415–430, Washington, D.C., August 2015. USENIX As-
     sociation.
[44] A. W. Roscoe. CSP and determinism in security modelling. In Proceedings
     of the 1995 IEEE Symposium on Security and Privacy, Oakland, California,
     USA, May 8-10, 1995, pages 114–127, 1995.
[45] John M. Rushby. Proof of separability: A verification technique for a class
     of a security kernels. In International Symposium on Programming, 5th Col-
     loquium, Torino, Italy, April 6-8, 1982, Proceedings, pages 352–367, 1982.
[46] Sanjit A. Seshia and Pramod Subramanyan. Uclid5: Integrating modeling,
     verification, synthesis and learning. In Proceedings of the 16th ACM-IEEE
     International Conference on Formal Methods and Models for System Design
     (MEMOCODE), October 2018.
[47] Ron Shemer, Arie Gurfinkel, Sharon Shoham, and Yakir Vizel. Property
     directed self composition. In Isil Dillig and Serdar Tasiran, editors, Com-
     puter Aided Verification, pages 161–179, Cham, 2019. Springer International
     Publishing.
[48] Thoralf Skolem. Logico-combinatorial investigations in the satisfiability or
     provability of mathematical propositions: a simplified proof of a theorem by
     L. Löwenheim and generalizations of the theorem. From Frege to Gödel. A
     Source Book in Mathematical Logic, 1879-1931, pages 252–263, 1967.
[49] Geoffrey Smith. On the foundations of quantitative information flow. In
     International Conference on Foundations of Software Science and Compu-
     tational Structures, pages 288–302. Springer, 2009.
[50] Marcelo Sousa and Isil Dillig. Cartesian Hoare Logic for verifying k-safety
     properties. In Proceedings of the 37th ACM SIGPLAN Conference on Pro-
     gramming Language Design and Implementation, PLDI ’16, pages 57–69,
     New York, NY, USA, 2016. ACM.
[51] Emil Stefanov, Marten van Dijk, Elaine Shi, Christopher W. Fletcher, Ling
     Ren, Xiangyao Yu, and Srinivas Devadas. Path ORAM: an extremely simple
     oblivious RAM protocol. In 2013 ACM SIGSAC Conference on Computer
     and Communications Security, CCS’13, Berlin, Germany, November 4-8,
     2013, pages 299–310, 2013.
[52] Pramod Subramanyan, Rohit Sinha, Ilia A. Lebedev, Srinivas Devadas, and
     Sanjit A. Seshia. A formal foundation for secure remote execution of en-
     claves. In Proceedings of the 2017 ACM SIGSAC Conference on Computer
     and Communications Security, CCS 2017, Dallas, TX, USA, October 30 -
     November 03, 2017, pages 2435–2450, 2017.
30        Shubham Sahai, Pramod Subramanyan, and Rohit Sinha

[53] Tachio Terauchi and Alexander Aiken. Secure information flow as a safety
     problem. In Static Analysis, 12th International Symposium, SAS, Proceed-
     ings, pages 352–367, 2005.
[54] UCLID5 Verification and Synthesis System.                    Available at
     http://github.com/uclid-org/uclid/, 2019.
[55] Herbert S. Wilf. generatingfunctionology. AK Peters/CRC Press, 2005.
[56] Weikun Yang, Pramod Subramanyan, Yakir Vizel, Aarti Gupta, and Sharad
     Malik. Lazy Self-Composition for Security Verification. In Computer Aided
     Verification - 30th International Conference, CAV 2018, Oxford, UK, July
     14-17, 2018, Proceedings, 2018.
[57] Hirotoshi Yasuoka and Tachio Terauchi. Quantitative information flow as
     safety and liveness hyperproperties. Theoretical Computer Science, 538:167–
     182, 2014.
[58] Steve Zdancewic and Andrew C Myers. Observational determinism for con-
     current program security. In Proceedings of the 16th IEEE Computer Secu-
     rity Foundations Workshop, pages 29–43. IEEE, 2003.
[59] Doron Zeilberger. Enumerative and algebraic combinatorics. In The Prince-
     ton Companion to Mathematics, pages 550–561. Princeton University Press,
     2010.
[60] Danfeng Zhang, Yao Wang, G. Edward Suh, and Andrew C. Myers. A
     Hardware Design Language for Timing-Sensitive Information-Flow Security.
     In Proceedings of the Twentieth International Conference on Architectural
     Support for Programming Languages and Operating Systems, ASPLOS ’15,
     Istanbul, Turkey, March 14-18, 2015, pages 503–516, 2015.
[61] Kehuan Zhang, Zhou Li, Rui Wang, XiaoFeng Wang, and Shuo Chen. Side-
     buster: automated detection and quantification of side-channel leaks in web
     application development. In Proceedings of the 17th ACM conference on
     Computer and communications security, pages 595–606. ACM, 2010.


Appendix A            Proofs
Lemma 3 (Equivalence Class Characterization).
    Let M = hX, Init (X), Tx (X, X ′ )i be a transition system and ΦM be the set of
traces of this transition system. Consider the quantitative hyperproperty: ∀π0 . #π1:
∆πj ,πk . ϕπ0 ,π1 ⊳ N (Z) for this system where Z ⊂ X. We assume the property
is well-defined. Further suppose:
    ≃ is the equivalence relation over traces corresponding to ¬∆πj ,πk .
                      τj ≃ τk iff {πj 7→ τj , πk 7→ τk } |= ¬∆πj ,πk
     Let Φϕ (τ0 ) be the function defined as follows.
                            .
                              n                                        o
                   Φϕ (τ0 ) = τ1 | {π0 7→ τ0 , π1 7→ τ1 } |=ΦM ϕτ0 ,τ1

    Let C(τ0 ) be the number of equivalence classes in Φϕ (τ0 ) induced by ≃ .
    Separately, let ΦC (τ0 ) be a function that constructs the maximally large set
satisfying the following conditions:
                     Verification of QHPs Using Trace Enumeration Relations         31

1. ∀τj , τk ∈ ΦC (τ0n). τj 6= τk ⇔ {πj 7→
                                        o τj , πk 7→ τk } |= ∆πj ,πk , and
2. ∀τ1 ∈ ΦC (τ0 ).   π0 7→ τ0 , π1 7→ τ1 |=ΦM ϕπ0 ,π1 .

   Then for every τ0 ∈ ΦM , C(τ0 ) = |ΦC (τ0 )|.
Proof Sketch. For every set ΦC (τ0 ) defined as above, every pair of distinct mem-
bers τj and τk , satisfy ∆πj ,πk . This means they are in different equivalence classes
for the relation ≃ . If ΦC (τ0 ) is maximally large, then the number of equivalence
classes must be equal to C(τ0 ).                                                     ⊓
                                                                                     ⊔
    A consequence of Lemma 3 is that one can prove satisfiability of a Quantita-
tive HyperLTL formula by counting the number of equivalence classes induced
by ≃ over Φϕ (τ0 ) instead of using the definition shown in Figure 5.
Lemma 1. [Trace Count Lower-Bound] If V(Y, Z) and U(Y, τ1 , τ2 ) form an
injective trace enumeration of the system M for the QHP ∀π0 . #π1: ∆πj ,πk . ϕ ≥
N (Z) and if #Y. V(Y, Z) is finite for all assignments to Z, then M |= ∀π0 .#π1:
∆πj ,πk . ϕ ≥ #Y. V(Y, Z).
Proof Sketch. The proof is by induction on the number of satisfying assignments
to Y in the formula V(Y, Z). We will consider the degenerate case when V(Y, Z)
is unsatisfiable separately and then use the case with one satisfying solution as
the base case for the induction.
     If #Y. V(Y, Z) is zero, then the lemma is trivially satisfied.
     Base case: If #Y. V(Y, Z) = 1, then by the definition of injective trace
enumerations, for every trace τ0 , we have at least one trace τ1 which satisfies ϕ.
This means the number of equivalence classes for Φϕ (τ0 ) as defined in Lemma 3
is at least one. Thus the QHP is satisfied.
     Induction hypothesis: Suppose the lemma holds for all formulas F (Y, Z)
such that #Y. F (Y, Z) = n; F (Y, Z) and U form an injective trace enumera-
tion for the system M . By assumption, V and U also form an injective trace
enumeration for M .
     Inductive step: We now have to show that the lemma holds for an arbitrary
formula V(Y, Z) such that #Y. V(Y, Z) = n + 1 with V and U constituting an
injective trace enumeration for the QHP on M .
     To do this, let us consider y which is a satisfying assignment to V(Y, Z). The
                  .
formula V ′ (Y ) = V(Y, Z) ∧ Y 6= y has n satisfying assignments to Y for the same
value of Z. Further, V ′ (Y ) and U are also an injective trace enumeration for
the QHP on the system M . By the induction hypothesis, the lemma holds for
V ′ (Y ). This means M |= ∀π0 . #π1: ∆πj ,πk . ϕ ≥ #Y. V ′ (Y, Z) and by Lemma 3
the set Φϕ (τ0 ) has at least n equivalence classes for every τ0 ∈ ΦM , each class
corresponding to the satisfying assignments to Y in V ′ (Y, Z) for Z = τ00 (Z). If
Φϕ (τ0 ) has more than n equivalence classes, the lemma holds.
     Instead, suppose that Φϕ (τ0 ) has exactly n equivalence classes. Now consider
the assignment y and its corresponding trace τy in Property 2. By Property 3,
τy is in a different equivalence class from all of the traces corresponding to
assignments to Y in V ′ (Y, Z). Contradiction! Therefore, Φϕ (τ0 ) has at least n+ 1
equivalence classes and so the inductive step holds.                              ⊓
                                                                                  ⊔
32       Shubham Sahai, Pramod Subramanyan, and Rohit Sinha

Lemma 2. [Trace Count Upper-Bound] If the pair V(Y, Z) and U(Y, τ1 , τ2 )
form a surjective trace enumeration of the system M for the QHP formula
∀π0 . #π1: ∆πj ,πk . ϕ ≤ N (Z) and if #Y. V(Y, Z) is finite for every assignment
to Z, then M |= ∀π0 .#π1: ∆πj ,πk . ϕ ≤ #Y. V(Y, Z).
Proof Sketch. The proof is similar in structure to Lemma 1 and is also by in-
duction on the number of satisfying assignments to Y in V(Y, Z).
    As before, we will treat the degenerate case when #Y. V(Y, Z) = 0 separately.
In this case, then Property 6 must hold vacuously and there are no traces that
satisfy ϕ. Φϕ (τ0 ) is the empty set for at least one τ0 ∈ ΦM . The QHP is satisfied.
    Base Case: Since #Y. V(Y, Z) = 1, Y1 6= Y2 is false and so Property 7 holds
vacuously. This means there is only one equivalence class of traces, and so the
lemma is true for the base case.
    Induction hypothesis: As in the previous proof, suppose the lemma holds
for all formulas F (Y, Z) such that #Y. F (Y, Z) = n; F (Y, Z) and U form a
surjective trace enumeration for the system M . By assumption, V and U form a
surjective trace enumeration for M .
    Inductive step: We now have to show that the lemma holds for an ar-
bitrary formula V(Y, Z) such that #Y. V(Y, Z) = n + 1 when V and U con-
stitute a surjective trace enumeration for the QHP on the transition system
M . We will again consider y, a satisfying assignment to V(Y, Z) and construct
                        .
the formula V ′ (Y ) = V(Y, Z) ∧ Y 6= y. V ′ has n satisfying assignments to Y
for this value of Z. Consider the set ΦM ′ constructed by removing all traces
from ΦM which are related to some trace τ0 in the relation U for Y = y:
ΦM ′ = ΦM − {τ1 | ∃τ0 . U(y, τ0 , τ1 )}. For every Φϕ ′ (τ0 ) constructed analogously
to Φϕ (τ0 ) from this set ΦM ′ , the set Φϕ ′ (τ0 ) has at least one less equivalence class
(for the relation ≃ ) than Φϕ (M ). By the induction hypothesis, the lemma holds
for the bound #Y. V ′ (Y, Z) for set of traces ΦM ′ . However, Φϕ (τ0 ) has at most
one more equivalence class than Φϕ ′ (τ0 ) and #Y. V(Y, Z) = #Y. V ′ (Y, Z) + 1.
Therefore, the inductive step holds.                                                     ⊓
                                                                                         ⊔


Appendix B            Experiments
This section provides more detail on the benchmarks used in our experimental
evaluation.

Electronic Purse: This example models an electronic purse, which was also
studied by Backes et al. [7], where a fixed amount (decr), modeled as an in-
teger, is debited from the purse, with secret initial balance (also modeled as
an integer), until the balance is insufficient for this transaction. The adversary-
observable state consists of each debit and the number of debits from the purse.
We show a deniability property which states that the number of traces with
identical observations but different initial balances are at least decr: ∀π0 .#π1 :
F (δ πj ,πk ). G (ψπ0 ,π1 ) ≥ decr. The binary predicate δ captures the fact that the
traces have different balances, and ψ ensures that they have identical adversary
observations.
                    Verification of QHPs Using Trace Enumeration Relations        33

Password Checker: This example models a program that checks a password.
This example is interesting because Finkbeiner et al. [31] studied the same
problem and found their technique times out when checking for 8-bit leakage
for an 8-bit password. We are able to provide a proof of quantitative non-
interference (QNI) for a password of unbounded length (at the cost of manual
construction of the trace enumeration relation). The QNI property states that
the maximum information leaked to the attacker is n bits, where n is a state
variable/parameter of the system representing the bit-length of the password:
∀π0 .#π1: F (δ πj ,πk ). G (ψπ0 ,π1 ) ≤ 2n − 1. δ requires the adversary observations
to be different while ψ ensures adversary inputs are the same in the two traces.
In other words, we prove that nothing besides the password is leaked to the
attacker even if the adversary can make unlimited login attempts.

Array Shuffle: This implements a variant of the Fisher-Yates shuffle. We chose
this example because producing random permutations of an array is an impor-
tant component of several cryptographic protocols (e.g., Ring ORAM [43]) and
a buggy shuffle algorithm that does not produce all permutations would result
in vulnerabilities in these protocols. We prove a quantitative information flow
property stating that all possible permutations are indeed generated by the al-
gorithm: ∀π0 .#π1 : F (δ πj ,πk ). G (ψπ0 ,π1 ) ≥ n!. As usual, δ requires the output
of the shuffle to be different, while ψ ensures that the input arrays are the same.
This example is interesting because we are able to prove for unbounded-length
input arrays that the shuffle does indeed produce all permutations. Note such an
unbounded proof is not possible with techniques based solely on model count-
ing.
