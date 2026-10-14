                                               A Deeper Look at Depth: Stable Generation
                                                  Accounting for Quantifier Reasoning

                                             Can Cebeci1 , Nikolaj Bjørner2 , George Candea1 , and Clément Pit-Claudel1
                                                                      1
                                                                        EPFL, Lausanne, Switzerland
                                                                  2
                                                                      Microsoft Research, Redmond, USA
arXiv:2609.26345v1 [cs.LO] 22 Sep 2026




                                                 Abstract. SMT solvers make automated verification convenient. At the
                                                 same time, solvers suffer from instability, whereby seemingly inconse-
                                                 quential changes to the input may cause a previously quickly produced
                                                 proof to fail or time out. This paper addresses a common cause of out-
                                                 come instability (i.e., unsat/unknown fluctuations) in the context of pro-
                                                 gram verification. We demonstrate that the generation (i.e., depth) ac-
                                                 counting used to make quantifier instantiation practical and implemented
                                                 in multiple state-of-the-art SMT solvers is non-confluent (i.e., prone to
                                                 divergence), and that this leads to instability. We then address this de-
                                                 ficiency and develop a new accounting method that is stable. The new
                                                 method is justified using a sequence of refinements from an abstract,
                                                 confluent solver model all the way to our implementation in Z3. Our
                                                 empirical evaluation demonstrates that our implementation reduces out-
                                                 come instability by 94% in the unstable core of the Mariposa benchmark
                                                 without leading to performance regressions.

                                                 Keywords: SMT solving · instability · quantifier reasoning



                                         1     Introduction

                                         SMT solvers make automated verification convenient but brittle. They auto-
                                         matically discharge most proof obligations, significantly lowering the required
                                         effort and expertise for developing proofs. At the same time, solvers suffer from
                                         instability, whereby seemingly inconsequential changes to the input may cause
                                         a previously quickly produced proof to fail or time out [16]. Recent work [4]
                                         conjectures that the instability users encounter in practice is addressable, not
                                         fundamental. This paper addresses a common cause of outcome instability (i.e.,
                                         unsat queries turning unknown) in the context of program verification.
                                             Controlling quantifier instantiation is crucial for stability [15, 17, 9]. This
                                         is because quantifiers are heavily used to encode verification conditions, and
                                         the solver’s success depends on choosing the right instances: under-instantiation
                                         leads to unknown and over-instantiation leads to timeout.
                                             Program verifiers typically control instantiation by configuring the solver to
                                         instantiate based on E-matching [10] exclusively, and up to some form of depth
                                         threshold [8, 7, 14]. For Z3 [11], they set smt.qi_eager_threshold. For CVC5 [1],
2          Can Cebeci, Nikolaj Bjørner, George Candea, and Clément Pit-Claudel

inst-max-level. Following Z3’s terminology, we refer to measures of a term’s
instantiation depth as its generation number.
    We demonstrate that the generation accounting implemented in some of the
state-of-the-art SMT solvers is non-confluent (i.e., prone to divergence), and that
this leads to instability. More precisely, we show that in certain cases a term’s
generation number (and subsequently the solver’s success) is dependent on the
order in which the solver explores proof branches. These cases are not simple
solver bugs. Rather, the ambiguity is conceptual: to the best of our knowledge,
there is no precise definition of what generation numbers should represent. We
use the terminology confluence here in the sense of Church-Rosser [5] properties.
It is fundamental in automated deduction, where a terminating and confluent
set of rewrite rules ensures decidability [6, 3] in several settings. SMT solvers
using E-matching for quantifier instantiation ensure termination by bounding
quantifier generation. But as we observe, bounding instantiation using generation
thresholds is an important ingredient for breaking confluence.
    We address this issue with the following contributions:

    – A precise, solver-agnostic specification of generation semantics for E-matching
      with quantifier weights.
    – Id: an abstract state machine model of solver behavior with access to idealized
      generation numbers. Id is confluent, but not practically implementable. It
      serves as a reference for the generation accounting problem independently of
      a specific implementation.
    – N, T, C: a series of implementable, increasingly efficient solver models, each
      obtained by refining the previous one. We prove, through bisimulation, that
      each solver is confluent and no more permissive than Id with quantifier in-
      stantiation.
    – An efficient implementation of C in Z3, upstream as of version 5.0.
    – An empirical evaluation demonstrating that the implementation reduces out-
      come instability by 94%, while incurring 2% fewer timeouts, in the unstable
      core of the Mariposa benchmark [16], which includes program verification
      queries. We also demonstrate that our implementation does not lead to per-
      formance regressions for SMT-LIB benchmarks [13].

    In this work-in-progress paper, we present proof sketches for the refinements
N, T, and C, aiming to convey the underlying intuition rather than full rigor.
We present some of the fully formalized proofs in the appendix; the correctness
of the remaining refinements is conjectured, supported by the proof sketches.


2      Background and Motivating Examples

In this section, we provide an overview of E-matching with generation thresholds
and quantifier weights, and motivate the need to precisely define generation
semantics.
                                                  A Deeper Look at Depth         3

      We use the following query as a running example:

  forall x. f(x+1) > f(x)
  f(0) > 0
  f(3) < 0

    The query is unsatisfiable: instantiating the quantifier three times with x :=
0, 1, 2 leads to a contradiction.


2.1     E-matching

Program verifiers typically configure SMT solvers to produce quantifier instanti-
ations using E-matching, whereby the solver produces instances based on ground
terms that match a given pattern. For our running example, the pattern f (x)
would lead to the right instantiations: f (0) in the input would match f (x) with
x := 0. That instantiation would create the term f (1), which would match again
with x := 1 and so on.
    Though the pattern is productive in this scenario, it also creates a matching
loop. Had the query been satisfiable (e.g., had the last assertion been omitted),
the solver could produce infinitely many instances rather than quickly giving
up. To guard against this, most solvers expose configuration parameters that set
thresholds controlling when to give up and return unknown.


2.2     Generation thresholds

A common idea is to threshold the depth of instantiation chains as opposed to the
total number of instantiations. The latter is prone to brittleness, as a productive
instantiation may never take place depending on the order in which the solver
explores proof branches.
    One way to track instantiation depth is to associate a generation number
with each term, such that all input terms have generation 0, and terms created
through an instantiation have 1 plus the maximal generation among matching
terms [2]. We block an instantiation if the maximal generation is above the
threshold. In the example above f (0) would have generation 0, f (1) would have
1 and so on. Therefore, a generation threshold of 3 would suffice for the solver
to return unsat.


2.3     Quantifier weights

Now consider adding another quantifier to the query:

  forall x. f(f(x)) > f(x+2) > f(x) ::: pattern f(x)

   This quantifier is more expensive: it creates two fresh terms, and both terms
re-match the pattern. So it produces 2c−1 instantiations where c is the generation
4        Can Cebeci, Nikolaj Bjørner, George Candea, and Clément Pit-Claudel

threshold. We would like to keep instantiation chains involving this quantifier
shorter than others. One way to do this is to associate a larger weight with
expensive quantifiers, and increment the generation numbers of fresh terms by
the weight, instead of just by 1.
   To prevent recursive matches on the expensive quantifier while still allowing
the productive instantiations, we can configure the query as follows:

    generation threshold: 3
    forall x. f(f(x)) > f(x+2) > f(x) ::: pattern: f(x), weight: 3
    forall x. f(x+1) > f(x) ::: pattern: f(x), weight: 1
    f(0) > 0
    f(3) < 0


2.4    Generation ambiguity
Example 1 In the current state of our working example, the generation num-
ber of f (2) is ambiguous: f (0) is part of the input so it has generation 0. Then
the first quantifier can generate f (2) at generation 3. On the other hand the
second quantifier can generate f (2) at generation 2 after two rounds of instanti-
ation. This ambiguity gives rise to instability, since f (2)’s generation determines
whether the instantiation producing f (3) > f (2) is allowed, and consequently
whether the query is unsat or unknown.

Example 2 The ambiguity is not uniquely brought on by quantifier weights.
Consider the following query:

    generation threshold: 3
    forall x. g(x) == h(x) ::: pattern g(x), weight 1
    forall x. h(x) == g(x+1) ::: pattern h(x), weight 1
    forall x. f(g(x)) > g(x) ::: pattern g(x), weight 1
    forall x. f(f(x)) > f(x) ::: pattern f(x), weight 1
    forall x. f(f(x)) < 0 ::: pattern f(f(x)), weight 1
    g(0) > 0

    g(0) has generation 0. By instantiating the first two quantifiers, we can gen-
erate g(1) at generation 2, and learn g(0) = g(1). From the third quantifier, we
get f (g(0)) at generation 1.
    The fourth quantifier should either match f (g(0)) or f (g(1)), the latter
through the equality we learned. Matching both would be wasteful, since x :=
g(0) and x := g(1) are equivalent bindings. If the fourth quantifier matches
f (g(0)), we get f (f (g(0))) at generation 2, which matches the fifth quantifier and
leads to a contradiction, returning unsat. But if the fourth quantifier matches
f (g(1)), since g(1) has generation 2 , we get f (f (g(1))), an equivalent term, at
generation 3 and so give up, returning unknown, without instantiating the fifth
quantifier.
                                                                   A Deeper Look at Depth   5

3     Preliminaries
3.1   Terms and contexts
Let x, c, and f range over variables, constants, and uninterpreted function sym-
bols, respectively. Terms are given by the grammar
                                   t := x | c | f (t1 , . . . , tn ).
   A context is a term containing exactly one hole □, which is a proper subterm.
Contexts are defined recursively by
                  C := f (t1 , . . . , □, . . . , tn ) | f (t1 , . . . , C, . . . , tn ).
   For a context C and term t, we write C[t] for the term obtained by replacing
the unique occurrence of □ in C with t.

3.2   Congruence and equality
We make a central distinction between equivalence and congruence modulo the
theory of equality. Equivalence is a weaker notion: two expressions s, t, are equiv-
alent in E, written t ∼
                      =E s, if the equality between s and t can be derived from
equalities in E using any rule in the theory of equality (reflexivity, symmetry,
transitivity, congruence). On the other hand, two terms are congruent if they
are equivalent and their equivalence can be inferred using the congruence rule:
Definition 1 (Congruence between terms). We say that t and t′ are con-
gruent if they have the same function symbol and all arguments are equivalent
in E. In other words, for every function symbol f , congruence is given by
                               ∼E t′ for i = 1, . . . , n
                            ti =              i
                       congruent E (f (t1 , . . . , tn ), f (t′1 , . . . , t′n ))
The E-matching and congruence-closure literature [12] uses terminology that
can blur this distinction. For example, the statement “if two terms f (t1 , . . . , tn )
and f (t′1 , . . . , t′n ) are congruent, then it is wasteful to try to match both” [10]
is not valid under the weaker interpretation where only f (a) = f (b) is known:
matching f (x) can produce non-equivalent bindings x := a, x := b when a ̸= b.

3.3   Quantifiers and instances
Quantifiers and quantifier instances are not terms. Instead, we treat them as
distinct syntactic objects.
    For simplicity, we assume each quantifier binds a single pattern and that
quantifiers are not nested. Generalizing to multiple bound variables and nested
quantifiers is conceptually straightforward but at the cost of more involved for-
malization.
    A quantifier instance is denoted by qJθK, where q is a quantifier and θ is the
term matching its pattern (not the bound variable). We write t ∈ qJθK to mean
that the instantiated body of q with θ contains t as a subterm.
    Each quantifier q is associated with a non-negative integer weight, denoted
by w (q).
6          Can Cebeci, Nikolaj Bjørner, George Candea, and Clément Pit-Claudel

3.4     Other notation
    – For functions f, g, h and predicate P , f ′ = f [g(x) 7→ h(x) | P (g(x))] denotes
      ∀x. (P (g(x)) =⇒ f ′ (g(x)) = h(x)) ∧∀y. (¬P (y) =⇒ f ′ (y) = f (y))
    – Similarly f ′ = f [y 7→ z] denotes f ′ (y) = z ∧ ∀x. x ̸= y =⇒ f ′ (x) = f (x)

4      Defining Generation Semantics
Intuitively, we define the generation number of a term as the weighted depth
of the shallowest derivation tree, where leaves are input terms and edges are
quantifier instantiations or equality rewrites using previously-derived terms.
    For intuition, consider the following scenario. Solid lines represent instantia-
tions and dashed lines represent rewrites:

                                                     gen 0      f (0)                g(0)
      – input terms: f (0) and g(0)
                                 weight
      – quantifiers (pattern −−−−→ term):                        3
               3                5
        f (x) −
              → f (x + 1), g(x) −
                                → g(x + 1),                                            5
                 1                                   gen 3      f (1)
        f (g(x)) −
                 → h(x)
      – equality g(1) = 1
                                                                          1 = g(1)
                                                     gen 5     f (g(1))              g(1)
    The generation number of h(1) is 6,                         1
    through the derivation tree shown.               gen 6      h(1)


Definition 2 (Reachable generation). Given a set of quantifiers Q, input
terms A, and equalities E, and instantiations I, a reachable generation g of a
term t is a tuple t ⊢E,I g, that can be obtained from one of the inferences:
                                       t∈A
                                              (Input)
                                     t ⊢E,I 0

                      q∈Q         t ∈ qJθK ∈ I      θ ⊢E,I g
                                                                (Inst)
                                 t ⊢E,I w (q) + g

                s1 ∼
                   =E s2         t[s1 ] ⊢E,I g      s2 ⊢E,I g ′
                                                                (Congruence)
                           t[s2 ] ⊢E,I max(g, g ′ )
    A and Q are constant given an input query, so we assume them implicit
arguments. A is subterm-closed (i.e., ∀t. t ∈ A ∧ t′ ∈ t =⇒ t′ ∈ A)
    It is not practically feasible for solver implementations to track generation
numbers in a way that exhaustively considers all possible quantifier instantia-
tions. We therefore make a distinction between ideal and implementation gener-
ations.
Definition 3 (Implementation generation). We define the implementation
generation of a term t with respect to A, Q, E, I as
                             genE,I (t) := min{g | t ⊢E,I g}
                                                   A Deeper Look at Depth       7

Definition 4 (Universal set of instantiations).

                         I ∞ := {qJθK | q ∈ Q, θ is a term}

Definition 5 (Ideal generation). We define the ideal generation of a term t
with respect to A, Q, E as

                          genideal
                             E (t) := min{g | t ⊢E,I ∞ g}

Whenever convenient, we denote genideal  E (t) with genE,I ∞ (t)
    For a set of equalities E, genideal
                                  E     (t) is uniquely determined and independent
of instantiation history, backtracking, or internal data-structure state.


5      An Ideal Solver Model - Id
This section presents Id, a solver model with access to genidealE (t), used as a
reference for practical algorithms.
    Our method only depends on inference steps involving quantifier instantia-
tions and equalities, and the model omits preconditions and inferences that are
irrelevant to us. In particular, we do not model conflicts, instead assuming the
solver may backtrack at any point.

5.1     State representation
The ideal solver maintains a state of the form ΣId : ⟨τ ⟩ where
 – τ : Event∗ - stack of locally asserted equalities and instances
 – Event := eq(t1 ≃ t2 ) | inst(qJθK) for q ∈ Q
      The initial state is, σ init := ⟨τ := ⟨⟩⟩.
                             Id
      Beyond the current state ⟨τ ⟩ we assume the following global constants:
 – A : Set(Term) (ground terms in input query),
 – Q : Set(Quantifier) (quantifiers),
 – maxG : N (generation threshold).
      For convenience we also define a few shortcuts based on a state:
 – E(τ ) := {e | eq(e) ∈ τ } : Set(Term) - set of equalities that are asserted
   within the scope.
 – I(τ ) := {qJθK | inst(qJθK) ∈ τ } : Set(Instance) - set of active quantifier
   instantiations.
  Unless indicated otherwise, we use E as shorthand for E(τ ) and I for I(τ ).
We also use T (σ) to refer to τ where σ := ⟨τ ⟩.
Definition 6 (Enabled instances). For a set of equalities E and quantifier
instances I, define the set of instances enabled within generation threshold maxG
as
        εE (I) := {qJθK | w (q) + genE,I (θ) ≤ maxG, q ∈ Q, θ is a term}
8          Can Cebeci, Nikolaj Bjørner, George Candea, and Clément Pit-Claudel

The transition rules for Id are as follows:
           e := (t1 ≃ t2 )                                                 (PopEq)
                             (PushEq)               ⟨τ · eq(e)⟩ →Id ⟨τ ⟩
        ⟨τ ⟩ →Id ⟨τ · eq(e)⟩

         qJθK ∈ εE (I ∞ )                                                    (PopInst)
                              (PushInst)         ⟨τ · inst(qJθK)⟩ →Id ⟨τ ⟩
    ⟨τ ⟩ →Id ⟨τ · inst(qJθK)⟩

      We use ⇝Id to denote the transitive closure of →Id (i.e., reachability).

5.2     Stability and confluence
Our goal is to prove that each solver is stable, i.e., if there is some way for the
solver to return unsat, the solver will always do so. We do not model decisions
and conflicts, or returning unsat or unknown. Instead we provide a definition of
confluence and argue that a confluent solver is outcome-stable.
    A solver returns unsat if it finds a set of conflicts that suffice to prove false,
and returns unknown if no such set can be found. When the solver visits ⟨τ ⟩, it
may find a conflict between equalities in E(τ ) considering instances in I(τ ). We
define all such (potentially conflicting) contexts the solver may observe starting
at state σ as Obs(σ):
Definition 7 (Observable contexts).

          Obs(σ) := {⟨Eo , Io ⟩ | σ ⇝S σ ′ ∧ Eo ⊆ E(T (σ ′ )) ∧ Io ⊆ I(T (σ ′ ))}

    We call a solver confluent if choosing to take certain steps never shrinks the
set of observable contexts.
Definition 8 (Confluence). Solver S with initial state σSinit is confluent if for
all states σ
                  σSinit ⇝S σ =⇒ Obs(σSinit ) = Obs(σ)
    A confluent solver is outcome-stable: if the solver may return unsat, there is
a set of conflicts, each observable from the initial state, that collectively prove
unsat. Due to confluence those conflicts remain observable after every transition,
so the solver will never return unknown.

Theorem 1. Id is confluent.

Proof. Id can perfectly backtrack every step, so it is always possible to return
from σ to σSinit , and from there observe the same contexts.


6      Realizable (And Efficient) Solver Models
Here we present our algorithm through a sequence of realizable solver models that
get iteratively more efficient. §7 then describes how the last algorithm translates
into a Z3 implementation.
                                                     A Deeper Look at Depth          9

    For each solver S, we prove that S is confluent and that S is not more per-
missive with quantifier instantiation than Id. We do so by defining a simulation
relation between solvers, proving bisimulation between Id and each subsequent
solver, and proving lemmas which state that bisimulation implies the desired
properties (Lemma 1, Lemma 2).
    The state tuple of each solver model includes τ , the event trail. τ is always ini-
tially empty, and PushEq is always available. We define a notion of subsumption
between trails, which we then use to define simulation between solvers:
Definition 9 (Trail subsumption). We define subsumption between trails τ ,
τ ′ as
                  τ ⊑ τ ′ := E(τ ) ⊆ E(τ ′ ) ∧ I(τ ) ⊆ I(τ ′ )
Definition 10 (Simulation). We define simulation between solvers R,S as
                     ′                                                           ′
R ⪯ S := ∀σS , σR , σR . σSinit ⇝S σS ∧ σR
                                         init
                                              ⇝R σR ∧ T (σR ) ⊑ T (σS ) ∧ σR →R σR
                   =⇒ ∃σS′ . σS ⇝S σS′ ∧ T (σR
                                             ′
                                               ) ⊑ T (σS′ )

Lemma 1 (Simulation preserves observations). For solvers R and S, if
                           init
S ⪯ R, Obs(σSinit ) ⊆ Obs(σR    ).
Proof. Given ⟨Eo , Io ⟩ ∈ Obs(σSinit ), we know there is a σS with σSinit ⇝S σS and
Eo ⊆ E(σS ) ∧ Io ⊆ I(σS ). We have T (σSinit ) ⊑ T (σR    init
                                                               ) since both trails are
                                                        init
empty. Since S ⪯ R, we can simulate every step in σS ⇝S σS to get a σR with
 init
σR    ⇝R σR and T (σS ) ⊑ T (σR ). Then we have Eo ⊆ E(σR ) ∧ Io ⊆ I(σR ) and
                     init
so ⟨Eo , Io ⟩ ∈ Obs(σR    ).
Lemma 2 (Bisimulation with Id implies confluence). For solver S, if Id ⪯
S and S ⪯ Id, S is confluent.

          σSinit                        σS             σS+

          ∼                   σS′                    ∼                  σS′′
          =                                          =

                                ⊑                                          ⊑
          σ init                        σ+             σId
           Id                            Id
                                                   ⊑
                              σ′                                        σ ′′
                               Id                                        Id

Proof. Given σSinit ⇝S σS , and a ⟨Eo , Io ⟩ ∈ Obs(σSinit ), it suffices to show
⟨Eo , Io ⟩ ∈ Obs(σS ), since we trivially have Obs(σS ) ⊆ Obs(σ init ).
    T (σSinit ) ⊑ T (σ init ) since both stacks are empty. Then through S ⪯ Id, we
                       Id
have a σ + with σ init ⇝Id σ + and T (σS ) ⊑ T (σ + ). Since Id can fully backtrack
           Id        Id          Id                  Id
and push the same equalities with fewer instantiations, we also have a σId with
σ init ⇝Id σ + ⇝Id σId , I(σS ) = I(σId ), and E(σS ) ⊆ E(σId ). And since pushing
 Id           Id
equalities is always allowed, σS can transition to a σs+ that includes the missing
equalities, and so T (σId ) ⊑ T (σs+ )
10       Can Cebeci, Nikolaj Bjørner, George Candea, and Clément Pit-Claudel

    By the definition of Obs(), there is a σS′ with σSinit ⇝S σS′ , Eo ⊆ E(T (σS′ ))
and Io ⊆ I(T (σS′ )). Since S ⪯ Id, we have a σ ′ with σ init ⇝Id σ ′ and T (σS′ ) ⊑
                                                    Id        Id         Id
T (σ ′ ).
    Id
    Since Id is confluent, we have a σ ′′ with σId ⇝Id σ ′′ and E(T (σ ′′ )) ⊇
                                             Id                     Id           Id
E(T (σ ′ )) ⊇ Eo and similarly I(T (σ ′′ )) ⊇ Io . Then, since Id ⪯ S and T (σId ) ⊑
        Id                                Id
T (σS ), there is a σS′′ with σS ⇝S σS′′ and T (σ ′′ ) ⊑ T (σs′′ ). Then Eo ⊆ E(T (σ ′′ ))
                                                 Id                                 Id
and Io ⊆ I(T (σ ′′ )) and so ⟨Eo , Io ⟩ ∈ Obs(σS ).
                  Id


6.1   Refinement 1: A Naive Solver – N

The most straightforward (and slow) approach is to compute all generation num-
bers at matching time using I(τ ), the current instance set.
    The naive solver maintains the same state as the ideal. It uses εE (I) instead
of εE (I ∞ ):
                            qJθK ∈ εE (I)
                                               (PushInstN )
                      ⟨τ ⟩ →N ⟨τ · inst(qJθK)⟩
All other transitions remain unchanged.

Theorem 2. Id ⪯ N.

Proof. PushEq can be trivially simulated by the corresponding step in N. PopEq
and PopInst can be simulated without any transitions. PushInst can be simulated
by a sequence of PushInstN steps: one for each quantifier instance used in the
inference of the matching term’s ideal generation, starting at the leaves. We
present a detailed proof for the PushInst case in Appendix A.

Theorem 3. N ⪯ Id

Proof. PushEqN and PushInstN can each be simulated by the corresponding
step in Id. PopEqN and PopInstN can be simulated without any transitions.


6.2   Refinement 2: Generation-Tracking Solver – T

The next step is to avoid recomputing genE,I (t) from scratch at matching time.
Instead, we maintain a dynamic mapping from terms to generation numbers.
   Generation tracking states are of the form ΣT : ⟨τ, g⟩ where

 – τ, E, I have the same meaning as in ΣId
 – g : Term → N - mapping used to track generation numbers

Initially, g(t) = 0 if t ∈ A, and g(t) = ∞ otherwise.
                                                    A Deeper Look at Depth        11

Handling equivalent instances: Real-world solvers avoid creating equiva-
lent instantiations: given θ1 , θ2 with congruent E (θ1 , θ2 ), for any q, the solver
instantiates at most one of qJθ1 K or qJθ2 K, since it judges the two instances to
be equivalent. This complicates generation tracking, as the generation updates
resulting from a single quantifier instance must emulate those of the whole set
of equivalent instances it stands in for.
    Our model allows equivalent instantiations, so this requirement could be
ignored without sacrificing completeness or conservativeness. We nonetheless
reflect it in the design of the generation-tracking solver, through the definition
of tracked generation:
Definition 11 (Tracked generation). The generation for term t used by T is

             genT
                E,g (t) := max{min{g(c) | congruent E (c, s)} | s ∈ t}

Definition 12 (Enabled instances for T).

         εT                           T
          E (g) := {qJθK | w (q) + genE,g (θ) ≤ maxG, q ∈ Q, θ is a term}

Definition 13 (Generation updates). A quantifier instance qJθK causes g to
be updated as follows:

        updateT                                          T
              E (g, qJθK) := g[t 7→ min(g(t), w (q) + genE,g (θ)) | t ∈ qJθK]

    Generation updates are sticky, meaning we do not undo them when we pop
instances. Doing so would not only require additional backtracking state, but
also make the solver re-discover the same updates later, which is expensive in
practice.

Modified transitions and definitions

                            qJθK ∈ εT
                                    E (g)
                                                            (PushInst T )
            ⟨τ, g⟩ →T ⟨τ · inst(qJθK), updateT
                                             E (g, qJθK)⟩

   All other transitions remain unchanged except state augmentation with g.
Theorem 4. N ⪯ T.
Proof. Simulating PushEq, PopEq, and PopInst is trivial (see the proof of The-
orem 2). Lemma 6 in the appendix shows that PushInstN can be simulated by
a sequence of PushInstT steps.
Theorem 5. T ⪯ Id.
Proof. Since PushEqT , PopEqT , and PopInstT are unchanged, simulating them
remains trivial. By Lemma 8 in the appendix, there exists an E ′ such that
∀t. genideal         T
        E ′ (t) ≤ genE(τ ),g (t). A PushInstT step can be simulated by first pushing
all the equalities in E ′ , then taking a PushInst step.
12       Can Cebeci, Nikolaj Bjørner, George Candea, and Clément Pit-Claudel

6.3    Refinement 3: Congruence-Class-Tracking Solver – C
T is still inefficient because computing min{g(c) | congruent E (c, t)} is expensive
for large congruence classes (§8 shows this empirically). The next version avoids
iterating over congruence classes at match time by maintaining one generation
number per congruence class.
    Solver state is now a tuple ΣC : ⟨τ, κ, γ, δ⟩ where
 – E, I have the same meaning as in ΣN and ΣT
 – κ : Term → Set(Term) - maps a term to its congruence class
 – γ : Set(Term) → N - maps a congruence class to its generation number.
 – We replace eq(e) by eq(e, κ, γ) to model backtracking to a snapshot
 – δ : Set(Term × N) - cumulative set of sticky generation updates
Initially,
 – δ=∅
 – κ(t) = {t}, for all t.
 – γ({t}) = 0 if t ∈ A and γ(·) = ∞ otherwise, for all t.
   C needs to explicitly keep track of congruence classes, which SMT solvers
readily do. Congruence classes are merged, modifying κ, as a result of PushEq
and unmerged as a result of PopEq. We make sure γ is updated accordingly,
such that it always maps to the generation of the minimal term in the class.

Definition 14 (Merging congruence classes). To track merging of congru-
ence classes and updates to generations we introduce the relation ⟨κ, γ⟩ →CGC(E)
⟨κ′ , γ ′ ⟩. It can be obtained from the reflexive-transitive closure of the inference:

 congruent E (t1 , t2 )  X ∈ κ(t1 ), Y ∈ κ(t2 )  κ′ = κ[t 7→ X ∪ Y | t ∈ X ∪ Y ]
                                   ′
                 ⟨κ, γ⟩ →CGC(E) ⟨κ , γ[X ∪ Y 7→ min(γ(X), γ(Y ))]⟩

Definition 15 (Congruence-class-tracked generation). The effective gen-
eration of a term t for C is:

                         genC
                            κ,γ (t) := max{γ(κ(s)) | s ∈ t}

   γ is analogous to g in T. It is therefore updated similarly, in response to
quantifier instantiations:
Definition 16 (Generation updates for C).

      updateC                                                C
            κ (γ, qJθK) := γ[κ(t) 7→ min(γ(κ(t)), w (q) + genκ,γ (θ)) | t ∈ qJθK]

    One complication that arises is that naively backtracking congruence-class
merges may undo generation updates resulting from quantifier instantiation,
which are meant to be sticky. It is crucial to prevent this, as re-discovering lower
generations for existing terms is expensive in practice. To this end, we explicitly
store a cumulative set of generation updates, which are re-applied on PopEq.
                                                              A Deeper Look at Depth     13

Definition 17 (New sticky updates caused by an instantiation). Each
term t re-discovered at a lower generation through a quantifier instance qJθK is
tagged with a sticky update in ∆qJθK,κ (γ, γ ′ ):
       ∆qJθK,κ (γ, γ ′ ) := {⟨t, γ ′ (κ(t))⟩ | t ∈ qJθK ∧ γ ′ (κ(t)) < γ(κ(t)) < ∞}
Definition 18 (Replaying sticky updates). Applying the updates stored in
δ to ⟨τ, κ, γ, δ⟩ leads to ⟨τ, κ, γ ′ , δ⟩ if γ →replayκ (δ) γ ′ can be obtained from one
of the inferences:

                               γ →replayκ (∅) γ (ApplyNone)

                              γ →replayκ (δ) γ ′
                                                                           (ApplySome)
         γ →replayκ (δ ∪ {⟨t, n⟩}) γ ′ [(κ(t)) 7→ min(γ ′ (κ(t)), n)]
Definition 19 (Enabled instances for C).

         εC                           C
          κ (γ) := {qJθK | w (q) + genκ,γ (θ) ≤ maxG, q ∈ Q, θ is a term}

   We now present the transition rules for C:

           e := (t1 ≃ t2 )         ⟨κ, γ⟩ →CGC(E ∪ {e}) ⟨κ′ , γ ′ ⟩
                                                                          (PushEq C )
                 ⟨τ, κ, γ, δ⟩ →C ⟨τ · eq(e, κ, γ), κ′ , γ ′ , δ⟩

                               γ ′ →replayκ (δ) γ ′′
                                                                        (PopEq C )
                ⟨τ · eq(e, κ′ , γ ′ ), κ, γ, δ⟩ →C ⟨τ, κ′ , γ ′′ , δ⟩

               qJθK ∈ εC
                       κ (γ)     γ ′ = updateC    κ (γ, qJθK)
                                                                        (PushInst C )
       ⟨τ, κ, γ, δ⟩ →C ⟨τ · inst(qJθK), κ, γ ′ , δ ∪ ∆qJθK,κ (γ, γ ′ )⟩
                                                                    (PopInst C )
                 ⟨τ · inst(qJθK), κ, γ, δ⟩ →C ⟨τ, κ, γ, δ⟩


Lemma 3. Every transition sequence executable from the initial state of C is
executable from the initial state of T, and vice versa; moreover, the resulting
states satisfy
                  ∀t. γ(κ(t)) = min{g(c) | congruent E (c, t)}
Proof. By induction on the length of the transition sequence. The invariant holds
initially, since both maps assign generation 0 to input terms and ∞ to all other
terms.
    On PushEq, merging congruence classes updates γ to the minimum of the
two merged classes’ generations. This is the same as min{g(c) | congruent E (c, t)}
once the classes are merged.
    On PushInst, C updates γ(κ(t)) for every subterm t in the instance using the
same weight and, by the induction hypothesis, the same generation for θ as T
uses to update g.
14      Can Cebeci, Nikolaj Bjørner, George Candea, and Clément Pit-Claudel

    On PopEq C , symmetrically to PushEq C , unmerging congruence classes
restores the minimum over the resulting classes. The sticky-update mechanism
ensures no generation updates are lost in the process: any update to a term’s
generation, once recorded as a sticky update, survives the split and is re-applied.
    PopInst C does not affect either map. So the invariant is trivially preserved.

Theorem 6. T ⪯ C.
                                                            ′
Proof. Given σT and σC , the latter can simulate a step to σT by first replaying
                          init
the transition sequence σT ⇝T σT and then taking the same final step. The
sequence can be replayed due to Lemma 3, and the fact that the value of γ(κ(t))
                                       init
at σC is no greater than its value at σC    for all t.

Theorem 7. C ⪯ T.

Proof. The proof is symmetric to that of Theorem 6.


7    Z3 Implementation

We implemented C in Z3; our implementation has been upstream since version
5.0. This section briefly describes some of the implementation details.
    Z3 associates each internalized term with a metadata structure called an e-
node. It keeps track of congruence classes through a hash table which stores
a unique e-node per congruence class, called the congruence representative. Z3
uses this table during pattern matching to ensure it only binds congruence rep-
resentatives, in order to avoid duplicate matches. This table effectively stores κ
from C.
    One option, in line with T, would be to store the function g as an e-node field
set at internalization and updated during quantifier instantiation. At matching
time, we could walk the congruence class of each subterm of the match candidate
to determine the minimum generation. We experimented with this option but
discarded it, as it led to significant performance regression (see §8).
    Another option, in line with C, would be to forego g and instead store γ,
directly in the hash table entry. This performs much better than the prior option,
but still incurs a minor (5%) slowdown, since looking up the hash table is less
cache-friendly than reading the generation number directly off the e-node.
    Our implementation instead stores γ on the e-node of the congruence root.
When congruence classes get merged, we update the new root’s e-node and save
the old generation on the backtracking stack. This wastes some space, since the
generation field goes unused on every e-node that is not a congruence root, but
the tradeoff is worthwhile: in the common case the congruence root’s e-node is
already accessed before a generation lookup, so we avoid the extra access.
    We store δ explicitly as a list of sticky updates to be re-applied whenever
congruence classes get unmerged. This can be expensive: sticky updates survive
backtracking until the term whose generation was updated is garbage collected,
                                                   A Deeper Look at Depth        15

and re-applying all of them costs time linear in the number of updates. In prac-
tice, however, discovering an existing term at a lower generation is uncommon
enough (despite its significance for instability) that this cost is negligible.
    Propagating generation updates is another potentially expensive consequence
of our implementation. When a term whose generation previously dominated
other terms’ generations (via instantiation) is itself updated, that update must
propagate, e.g., by allowing duplicate matches with lower generation numbers.
Our implementation skips this, slightly deviating from C, yet still greatly im-
proves stability. We suspect enabling such duplicate matches would not signifi-
cantly affect performance for the same reason as above: generation updates are
rare in practice.


8   Empirical Evaluation

Experimental setup: For our evaluation, we use the Mariposa [16] framework,
and its unstable-core benchmark set. This consists of 60 queries from prior pro-
gram verification projects, mostly written in Dafny [8]. Mariposa stability-fuzzes
these queries by generating mutants through reseeding, assertion shuffling and
variable renaming.
    For each query, we generate 99 mutants and run each of them, along with
the original query, with a 60-second timeout (Mariposa’s default). We include
queries that are not outcome-unstable to ensure we do not introduce regressions
that increase timeouts. Our experiments were run on a machine with two 64-
core AMD EPYC 7763 CPUs at 2.4GHz and 503GiB of RAM. For two of the
queries, running all 100 variants in parallel allocates enough memory to crash
our infrastructure; three others produce mutants that return a solver error due
to malformed input. We discard these five queries and present results for the
remaining 55 queries, producing 5500 mutants, each of which returns unsat,
unknown, or timeout.
    We compare four versions of generation accounting: z3’s accounting prior to
our work, which we treat as a baseline, the two less efficient options outlined in
§7 (z3-T, z3-C-table), and our final implementation (z3-C-enode).


                           Outcome-unstable       Unknown
        Solver version                                          Timeouts
                                queries           mutants
        baseline                    27                489          1813
        z3-T                         6                25           2399
        z3-C-table                   4                25           1867
        z3-C-enode                   4                29           1779

Table 1. Stability and performance results on Mariposa’s unsat core benchmark across
implementation versions. Experiments include 55 queries generating 5500 mutants.
16      Can Cebeci, Nikolaj Bjørner, George Candea, and Clément Pit-Claudel

    Table 1 reports, for each version, the number of outcome-unstable queries
(i.e., queries that have at least one unknown and one unsat mutant), the total
number of unknown mutants across all queries, and the total number of timeouts.
    Stability: All three implementations substantially reduce outcome instabil-
ity relative to the baseline: z3-C-enode cuts the number of unknown mutants
by 94% and the number of outcome-unstable queries by 85%, with z3-T and
z3-C-table achieving comparable reductions; the differences are within noise.
    Performance: We also observe a performance cost, measured as the total
number of timeouts across all queries: z3-T is considerably slower, producing
32% more timeouts than the baseline, while z3-C-table incurs only a minor
regression (3% more timeouts). z3-C-enode, our final implementation, avoids
this cost and yields slightly fewer timeouts than the baseline. Additionally, for
each solver version, we manually examined the timeout count per query and
confirmed that our changes did not cause any single query to blow up.
    To ensure our changes do not introduce regressions beyond program verifi-
cation, we also ran z3-C-table and z3-C-enode on the non-incremental SMT-
LIB benchmarks [13], using a 20-second timeout. For quantified categories, all
differences fall within noise, the largest being 14 additional timeouts (1%) for
z3-C-table on ALIA. Among quantifier-free categories, the only notable dif-
ference is a 5% slowdown for z3-C-table on QF_UF, which does not cause
additional timeouts. This is expected: the same cache-locality issue affecting
Mariposa performance also slows down congruence closure in the absence of
quantifiers. z3-C-enode avoids this regression entirely.


References
 1. Barbosa, H., Barrett, C., Brain, M., Kremer, G., Lachnitt, H., Mann, M., Mo-
    hamed, A., Mohamed, M., Niemetz, A., Nötzli, A., Ozdemir, A., Preiner, M.,
    Reynolds, A., Sheng, Y., Tinelli, C., Zohar, Y.: cvc5: A versatile and industrial-
    strength SMT solver. In: TACAS (2022)
 2. Bjørner,       N.,   Eisenhofer,    C.,     Gurfinkel,     A.,     Lopes,     N.P.,
    de Moura, L., Nachmanson, L., Wintersteiger, C.: Z3 internals.
    https://github.com/Z3Prover/doc/blob/master/internals/z3internals.mdk
 3. Buchberger, B.: Gröbner bases: An algorithmic method in polynomial ideal theory.
    In: Bose, N.K. (ed.) Multidimensional Systems Theory, pp. 184–232. D. Reidel
    Publishing Company (1985). https://doi.org/10.1007/978-94-009-5225-6_6
 4. Cebeci, C., Bjørner, N., Candea, G., Pit-Claudel, C.: A conjecture regarding SMT
    instability. In: SMT (2025)
 5. Church, A., Rosser, J.B.: Some properties of conversion. Transactions of the Amer-
    ican Mathematical Society 39(3), 472–482 (1936)
 6. Knuth, D.E., Bendix, P.B.: Simple word problems in universal algebras. In: Com-
    putational Problems in Abstract Algebra, pp. 263–297 (1970)
 7. Lattuada, A., Hance, T., Bosamiya, J., Brun, M., Cho, C., LeBlanc, H., Srinivasan,
    P., Achermann, R., Chajed, T., Hawblitzel, C., Howell, J., Lorch, J.R., Padon, O.,
    Parno, B.: Verus: A practical foundation for systems verification. In: SOSP (2024)
 8. Leino, K.R.M.: Dafny: An automatic program verifier for functional correctness.
    In: LPAR (2010)
                                                          A Deeper Look at Depth             17

 9. Leino, K.R.M., Pit-Claudel, C.: Trigger selection strategies to stabilize program
    verifiers. In: CAV (2016)
10. de Moura, L., Bjørner, N.: Efficient e-matching for smt solvers. In: CADE (2007)
11. de Moura, L.M., Bjørner, N.: Z3: An efficient SMT solver. In: TACAS (2008)
12. Nieuwenhuis, R., Oliveras, A.: Fast congruence closure and extensions. In: Infor-
    mation and Computation (2007)
13. Preiner, M., Schurr, H.J., Barrett, C., Fontaine, P., Niemetz, A.,
    Tinelli,    C.:   SMT-LIB     release   2025    (non-incremental      benchmarks),
    https://doi.org/10.5281/zenodo.16740866
14. Swamy, N., Hritcu, C., Keller, C., Rastogi, A., Delignat-Lavaud, A., Forest, S.,
    Bhargavan, K., Fournet, C., Strub, P.Y., Kohlweiss, M., Zinzindohoue, J.K.,
    Zanella-Béguelin, S.: Dependent types and multi-monadic effects in F*. In: POPL
    (2016)
15. Zhou, Y., Bosamiya, J., Li, J., Heule, M.J., Parno, B.: Context pruning for more
    robust SMT-based program verification. In: FMCAD (2024)
16. Zhou, Y., Bosamiya, J., Takashima, Y., Li, J., Heule, M., Parno, B.: Mariposa:
    Measuring SMT instability in automated program verification. In: FMCAD (2023)
17. Zhou, Y., Shah, A., Lin, Z., Heule, M., Parno, B.: Cazamariposas: Automated
    instability debugging in SMT-based program verification. In: CADE (2025)


A     Proofs related to N
Lemma 4 (N can find all ideal generations within threshold).
                      ′
 genideal                     inst
    E (t) ≤ maxG =⇒ ∃τ .⟨τ ⟩ ⇝N    ⟨τ ′ ⟩ ∧ τ ⊑ τ ′ ∧ genE,I(τ ′ ) (t) ≤ genideal
                                                                            E (t)

where ⇝inst
       N    denotes reachability through exclusively PushInstN transitions.
Proof. Since genideal                                               ideal
                E (θ) ≤ G < ∞, we have an inference for t ⊢E,I ∞ genE (t).
By induction on this inference, we have three cases:
                                                                         ′
 – (Input ) t ∈ A: Then genE,I (t) = 0 = genideal        E (t). So τ := τ is a witness.
                           ′        ∼          ′
 – (Congruence ) t = t [s2 ], s1 =E s2 , t [s1 ] ⊢E,I ∞ nt′ , s2 ⊢E,I ∞ ns2 , genideal   E (t) =
   max(nt′ , ns2 ): We have nt′ ≤ maxG and ns2 ≤ maxG and so, by the induc-
   tion hypotheses, we get ⟨τ ⟩ ⇝inst  N    ⟨τ1 ⟩ ∧ genE,I(τ1 ) (t[s1 ]) ≤ nt′ and ⟨τ ⟩ ⇝instN
   ⟨τ2 ⟩ ∧ genE,I(τ2 ) (s2 ) ≤ ns2 . Since adding instances never blocks PushInstN ,
   we can replay the transitions in ⟨τ ⟩ ⇝inst        N    ⟨τ2 ⟩ from ⟨τ1 ⟩ and get a τ ′ with
   ⟨τ ⟩ ⇝N ⟨τ1 ⟩ ⇝N ⟨τ ⟩, τ1 ⊑ τ , and τ2 ⊑ τ ′ . Then genE,I(τ ′ ) (t[s1 ]) ≤
           inst          inst   ′            ′

   genE,I(τ1 ) (t[s1 ]) ≤ nt′ and similarly genE,I(τ ′ ) (s2 ) ≤ ns2 . So, through the
   Congruence rule, genE,I(τ ′ ) (t) ≤ n = genideal      E (t).
 – (Inst ) t ∈ qJθK, genideal
                            E  (t) =  w (q) +    n θ , θ ⊢E,I ∞ nθ : Since quantifier weights
   are non-negative, nθ ≤ n ≤ maxG. Then by the induction hypothesis we have
   a τ ′′ with genE,I(τ ′′ ) (θ) ≤ genideal
                                        E (θ) ∧ ⟨τ ⟩ ⇝N
                                                               inst
                                                                    ⟨τ ′ ⟩ ∧ τ ⊑ τ ′ . PushInstN
   with qJθK is enabled in ⟨τ ′′ ⟩ and leads to some ⟨τ ′ ⟩ such that τ ′ is a witness.
Lemma 5 (The PushInst case of Theorem 2). For all σN , σId , σ ′ ,
                                                              Id
                                    ′       ′          ′       ′          ′
    T (σId ) ⊑ T (σN ) ∧ σId →inst
                              Id   σId =⇒ ∃σN . σN ⇝N σN ∧ T (σId ) ⊑ T (σN )
18       Can Cebeci, Nikolaj Bjørner, George Candea, and Clément Pit-Claudel

Proof. Let E be E(T (σId )) (or equivalently E(T (σN )), since T (σId ) ⊑ T (σN )).
                    ′               ideal
From σId →inst
            Id σId we have genE (θ)+w (q) ≤ maxG, where qJθK is the instance
being pushed. By Lemma 4, we have a τ ′ with genE,I(τ ′ ) (θ) ≤ genideal      E (θ) ∧
            ′                  ′                                       ′
σN ⇝inst
      N  ⟨τ   ⟩ ∧ T  (σN ) ⊑ τ   PushInst N with qJθK is enabled in ⟨τ   ⟩ and leads to
       ′
some σN  with T (σ ′ ) ⊑ T (σN   ′
                                   ).
                      Id

B    Proofs related to T
Lemma 6 (T can find derivable generations). For all t, n, τ, g such that
 init
σT    ⇝T ⟨τ, g⟩,

              t ⊢E,I n =⇒ ∃τ ′ , g ′ . ⟨τ, g⟩ ⇝inst
                                               T    ⟨τ ′ , g ′ ⟩ ∧ genT
                                                                      E,g ′ (t) ≤ n

Proof. By induction on t ⊢E,I n, we have three cases:
 – (Input ) t ∈ A, n = 0: Since A is subterm-closed, t′ ∈ A for all subterms t′
   of t. Then we have g init (t′ ) = 0 at initialization and because g(t′ ) cannot
   increase through any transition, g(t′ ) = 0. So τ ′ := τ, g ′ := g is a witness.
 – (Inst ) t ∈ qJθK, genE,I (t) = w (q)+nθ , θ ⊢E,I nθ : By the induction hypothesis
   we have ⟨τ, g⟩ ⇝inst   T     ⟨τ ′′ , g ′′ ⟩ and genT    E,g ′′ (t) ≤ nθ . PushInstT is enabled at
   ⟨τ ′′ , g ′′ ⟩ and leads to some ⟨τ ′ , g ′ ⟩ that serves as a witness.
 – (Congruence ) t = t′ [s2 ], s1 ∼           =E s2 , t′ [s1 ] ⊢E,I nt′ , s2 ⊢E,I ns2 , genE,I (t) =
   max(nt′ , ns2 ): Similarly to the argument in the proof of Lemma 4, we can
   take the transitions described by the two inductive hypotheses to get a τ ′ , g ′
   with ⟨τ, g⟩ ⇝inst    T   ⟨τ ′ , g ′ ⟩, genT          ′                         T
                                                E,g ′ (t [s1 ]) ≤ nt′ , and genE,g ′ (s2 ) ≤ ns2 . It
                                   ′
   suffices to show min{g (c) | congruent E (c, ts )} ≤ genE,I (t) for all subterms
   ts of t′ [s2 ]. We consider three cases:
     • ts ∈ s2 : Since genT                                         ′
                                 E,g ′′ (s2 ) ≤ ns2 , min{g (c) | congruent E (c, ts )} ≤ ns2 ≤
          genE,I (t).
     • t ∈ t′ [s ]: The same argument applies with genT ′′ (t′ [s ]) ≤ n ′
          s        1                                                  E,g       1        t
      • ts = t′′ [s2 ], t′′ [s1 ] ∈ t′ [s1 ]: We have min{g ′ (c) | congruent E (c, t′′ [s1 ])} ≤
        nt′ due to genT                ′                                    ′′      ′′
                              E,g ′′ (t [s1 ]) ≤ nt′ . Since congruent E (t [s1 ], t [s2 ]), the
                                                   ′                       ′′
        same minimal c ensures min{g (c) | congruent E (c, t [s2 ])} ≤ nt′ ≤
        genE,I (t).
Lemma 7 (Mapped values for subterms). For all reachable states ⟨τ, g⟩ of
T, for all terms t, s, s ∈ t =⇒ g(s) ≤ g(t).
Proof. Since A is subterm-closed, initially either g(t) = g(s) = 0 or g(t) =
g(s) = ∞. Then, g(t) and g(s) may only decrease, via PushInstT transitions,
which never decrease g(t) further than g(s).
Lemma 8 (Tracked generations are lower-bounded by some ideal). For
all reachable states ⟨τ, g⟩ of T,

                             ∃E ′ .∀t. genideal        T
                                          E ′ (t) ≤ genE(τ ),g (t)
                                                             A Deeper Look at Depth                 19

Proof. By induction on the reachability of ⟨τ, g⟩.

 – Initially, τ is empty. We choose E ′ := ∅. Then for all t ∈ A, both generations
   are 0 (genT   E(τ ),g (t) = 0 because A is subterm-closed), and for t ̸∈ A both
   generations are ∞.
 – (PushEq) τ := τ ′ · eq(e), IH1 := ∀t. genideal                           T
                                                             E ′ (t) ≤ genE(τ ′ ),g (t): We choose
                      ′′         ′
   the witness E := E ∪ E(τ ). Proof by structural induction on t. Let n :=
   genTE(τ ),g (t).
     • If t is a constant (0-arity function), the only term congruent to t is t
       itself. Then g(t) = n and genT                                              ideal
                                               E(τ ′ ),g (t) = n. By IH1 , genE ′ (t) ≤ n. Since
       E ′ ⊆ E ′′ , genideal
                          E ′′ (t) ≤ n.
     • Otherwise t := c[a]. By the structural induction hypothesis, genideal              E ′′ (a) ≤
       n. Assume all terms congruent to t can be expressed as c[b] for some b
       with a ∼  =E(τ ) b. In reality, a congruent term can be obtained by rewriting
       more than one argument of the top-level function as well, but we ignore
       this for simplicity of presentation. For some b, g(c[b]) ≤ n. Then, by
       Lemma 7, genT                                                         ideal
                             E(τ ′ ),g (c[b]) ≤ n and so by IH1 , genE ′ (c[b]) ≤ n. Since
       E ⊆ E , genE ′′ (c[b]) ≤ n and since E(τ ) ⊆ E , a ∼
          ′       ′′       ideal                                       ′
                                                                              =E ′′ b. Then by the
       Congruence rule for deriving generations, genideal             E ′′ (c[a])    ≤ n.
                                   ′                     ideal          T
 – (PopEq) τ · eq(e) = τ , IH1 := ∀t. genE ′ (t) ≤ genE(τ ′ ),g (t): Since E(τ ) ⊆
   E(τ ′ ), for all t, genT ′ (t) ≤ genT
                             E(τ ),g             E(τ ),g    (t). Then genideal
                                                                          E   ′ (t) ≤ gen
                                                                                           T
                                                                                          E(τ ),g (t)
   so E ′ serves as a witness.
 – (PushInst) τ = τ ′ · inst(qJθK), g = updateT       ′                       ideal
                                                 E (g , qJθK), IH1 := ∀t. genE ′ (t) ≤
   genTE(τ ′ ),g ′ (t): We choose E
                                    ′′
                                       := E ′ ∪ E(τ ) as the witness. The proof is
   structurally inductive, like the PushEq case. Let n := genT           (t). E(τ ),g
     • If t is a constant, g(t) = n and g ′ (t) = genT                             ′
                                                       E(τ ′ ),g ′ (t). Since E ⊆ E ,
                                                                                         ′′

                                     ′
       genideal
           E ′′ (t) ≤ n. If g(t) = g (t) we conclude by IH1 . Otherwise, g(t) =
                    T
       w (q) + genE,g′ (θ) with t ∈ qJθK. Since E(τ ) ⊆ E ′′ , w (q) + genideal
                                                                              E ′′ (θ) ≤ n.
       Then by the Inst rule for deriving generations, genideal    E ′′ (t) ≤ n.
     • If t is a function application, we follow an identical argument to the
       second case of (PushEq). An ideal generation less than n can be derived
       for c[b] via the Inst rule, and then for c[a] via the Congruence rule.
 – (PopInst): E(τ ) = E(τ ′ ) and g = g ′ , so we conclude trivially via the induc-
   tion hypothesis.
