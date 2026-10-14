                                                    A Specification Logic for Programs in the
                                                   Probabilistic Guarded Command Language
                                                                            (Extended Version)

                                              Raúl Pardo1 , Einar Broch Johnsen2 , Ina Schaefer3 , and Andrzej Wasowski
                                                                                                                ˛      1
arXiv:2205.04822v2 [cs.LO] 19 Aug 2022




                                                            1
                                                              IT University of Copenhagen, Copenhagen, Denmark,
                                                                      2
                                                                        University of Oslo, Oslo, Norway
                                                            3
                                                              Karlsruhe Institute of Technology, Karlsruhe, Germany



                                                Abstract. The semantics of probabilistic languages has been extensively studied,
                                                but specification languages for their properties have received little attention. This
                                                paper introduces the probabilistic dynamic logic pDL, a specification logic for
                                                programs in the probabilistic guarded command language (pGCL) of McIver and
                                                Morgan. The proposed logic pDL can express both first-order state properties and
                                                probabilistic reachability properties, addressing both the non-deterministic and
                                                probabilistic choice operators of pGCL. In order to precisely explain the meaning
                                                of specifications, we formally define the satisfaction relation for pDL. Since pDL
                                                embeds pGCL programs in its box-modality operator, pDL satisfiability builds on a
                                                formal MDP semantics for pGCL programs. The satisfaction relation is modeled
                                                after PCTL, but extended from propositional to first-order setting of dynamic logic,
                                                and also embedding program fragments. We study basic properties of pDL, such
                                                as weakening and distribution, that can support reasoning systems. Finally, we
                                                demonstrate the use of pDL to reason about program behavior.


                                         1   Introduction

                                         This paper introduces a specification language for probabilistic programs. Probabilistic
                                         programming techniques and systems are becoming increasingly important not only for
                                         machine-learning applications but also for, e.g., random algorithms, symmetry breaking
                                         in distributed algorithms and in the modelling of fault tolerance. The semantics of
                                         probabilistic languages has been extensively studied, from Kozen’s seminal work [1] to
                                         recent research [2–5], but specification languages for their properties have received little
                                         attention (but see, e.g., [6]).
                                             The specification language we define in this paper is the probabilistic dynamic logic
                                         pDL, a specification logic for programs in the probabilistic guarded command language
                                         pGCL of McIver and Morgan [7]. This programming language combines the guarded
                                         command language of Dijkstra [8], in which the non-deterministic scheduling of threads
                                         is guarded by Boolean assertions, with state-dependent probabilistic choice. Whereas
                                         guarded commands can be seen as a core language for concurrent execution, pGCL can be
                                         seen as a core language for probabilistic and non-deterministic execution.
                                             The proposed logic pDL can express both first-order state properties and reachability
                                         properties, addressing the non-deterministic as well as the probabilistic choice operators
of pGCL. Technically, pDL is a probabilistic extension of (first-order) dynamic logic [9], a
modal logic in which programs can occur within the modalities of logical formulae. The
semantics of dynamic logic is defined as a Kripke-structure over the set of valuations
of program variables. Dynamic logic allows reachability properties to be expressed for
given (non-probabilistic) programs by means of modalities. The probabilistic extension
pDL allows probabilistic reachability properties to be similarly expressed.
    In order to precisely explain the meaning of specifications expressed in pDL, we for-
mally define the semantics of this logic in terms of a satisfaction relation for pDL formulae
(a model-theoretic semantics). The satisfaction relation is modeled after PCTL [10],
but extended from a propositional to a first-order setting of dynamic logic, embedding
program fragments in the modalities. Since pDL embeds pGCL programs in its formulae,
the formalization of pDL satisfiability builds on a formal semantics for pGCL programs,
which is defined by Markov Decision Processes (MDP) [11]. The formalization of pDL
satisfiability allows us to study basic properties of specifications, such as weakening and
distribution. Finally, we demonstrate how pDL can be used to specify and reason about
program behavior. The main contributions of this paper are:
    – The specification logic pDL to syntactically express probabilistic properties of stochas-
      tic non-deterministic programs written in pGCL;
    – A model-theoretic semantics for pDL over a simple MDP semantics for pGCL pro-
      grams; the satisfaction relation is modeled after PCTL, but extended from a propo-
      sitional to a first-order setting of dynamic logics with embedded pGCL programs;
      and
    – A study of basic properties of pDL and a demonstration of how pDL can be used to
      specify and reason about pGCL programs.
Our motivation for this work is ultimately to define a proof system which allows us
to mechanically verify high-level properties for programs written in probabilistic pro-
gramming languages. Dynamic logic has proven to be a particularly successful logic
for such verification systems in the case of regular (non-probabilistic) programs; in
particular, KeY [12], which is based on forward reasoning over DL formulae, has been
used for breakthrough results such as the verification of the TimSort algorithm [13].
The specification language introduced in this paper constitutes a step in this direction,
especially by embedding probabilistic programs into the modalities of the specification
language. Further, the semantic properties of pDL form a semantic basis for proof rules,
to be formalized, proven correct, and implemented in future work.


2     State of The Art
Verification of probabilistic algorithms has been addressed with abstract interpreta-
tion [14], symbolic execution [15], or probabilistic model checking [16]. Here, we focus
on logical reasoning about probabilistic algorithms using dynamic logic. Existing dy-
namic logics for probabilistic programs are Kozen’s PPDL and PrDL of Feldman and
Harel. Kozen introduces probability by drawing variable values from distributions, while
propositions are measurable real-valued functions [17]. The program semantics is purely
probabilistic; PPDL does not include demonic choice. Probabilistic Dynamic Logic


                                               2
(PrDL) relies on the same notion of state, but introduces probabilistic transitions using
a random choice operator [18]. Since neither PPDL nor PrDL include non-determinism,
to reason about non-deterministic stochastic programs in a program logic we need a
new specification language. We aim to develop a first-order dynamic logic for programs
(PPDL was propositional) with demonic and probabilistic choice.
     The main alternative for logical reasoning about probabilistic programs is the weakest
pre-expectation calculus, proposed by McIver and Morgan for the probabilistic guarded
command language (pGCL) [7]. The language contains explicit probabilistic and demonic
choice. Program states are modeled by classical (non-probabilistic) variable assignments,
and probabilities are introduced by an explicit probabilistic choice. Assertions are real-
valued functions over program state capturing expectations, where a Boolean embedding
is used to derive expectations from logical assertions. Reasoning in pGCL follows a
backwards expectation transformer semantics. McIver and Morgan define an axiomatic
semantics given by the weakest pre-expectation calculus over pGCL programs, but do
not introduce an operational semantics for the language. Also they do not provide
a specification language for pGCL assertions, i.e., real-valued functions, beyond the
Boolean embedding (cf. [19]). In this work, we want to build on this tradition. However,
we think there is a need for a specification language with classical model-theoretical
semantics known from logics—a satisfaction semantics. Dynamic logics is a good basis
for such a development, since it is strictly more expressive than Hoare logic and weakest
precondition calculi—both can be embedded in dynamic logic [20]. In contrast to these
calculi, dynamic logics are closed under logical operators such as first-order connectives
and quantifiers; for example, program equivalence, relative to state formulae ϕ and ψ,
can be expressed by the formula ϕ ⇒ [s1 ]ψ ⇐⇒ ϕ ⇒ [s2 ]ψ.
     As mentioned, the original pGCL lacked operational semantics. Since semantics is
needed for a traditional definition of satisfaction in a modal logic, we propose to use the
MDP semantics similar to the one of Gretz et al. [21], where post-expectations are re-
wards in final states. An alternative could be Kaminski’s computation tree semantics [3],
but we find it more complex and less standard for our purpose (deviating further from
traditions of simpler logics like PCTL).
     Termination analysis of probabilistic programs [2, 22] considers probabilistic reacha-
bility properties. This and other directions of related work, such as separation logic for
probabilistic programs [23], expected run-time analysis for probabilistic programs [24]
and relational reasoning over probabilistic programs for sensitivity analysis [25], are
orthogonal to the goal of defining a specification language for programs, and thus outside
of scope of interest for this particular paper. Generally all these approaches rely on the
backwards pre-expectation transformer semantics of McIver and Morgan [7].


3   Preliminaries
We review the basic semantic notions used in the main part of the paper.
Definition 1 (Markov Decision Process). A Markov Decision Process (MDP) is a
tuple M = (State, Act, P) where (i) State is a countable set of states, (ii) Act is a count-
able set of actions, (iii) P : State×Act * Dist(State) is a partial transition probability
function.


                                             3
Let σ denote the states and a the actions of an MDP. A state σ is final if no further
transitions are possible from it, i.e. (σ, a) 6∈ dom(P) for any a. A path, denoted σ, is a se-
quence of states σ1 , . . . , σn such that σn is final and there are actions a1 , . . . , an−1 such
that P(σi , ai )(σi+1 ) ≥ 0 for 1 ≤ i < n. Let final(σ) denote the final state of a path σ.
    For a given state, the set of applicable actions of P defines the demonic choices
between successor state distributions. A positional policy π is a function that maps states
to actions, so π : State → Act. We assume π to be consistent with P, so P(σ, π(σ)) is
                                                                ·
defined. Given a policy π, we define a transition relation →   − π ⊆ State × [0, 1] × State on
states that resolves all the demonic choices in P and write:
                              p
                            →π σ 0
                           σ−            iff   P(σ, π(σ))(σ 0 ) = p.                           (1)
                                 p
For a given policy π, we let −
                             →∗π ⊆ State×[0, 1]×State denote the reflexive and transitive
closure of the transition relation, and define the probability of a path σ = σ1 , . . . , σn by
                                                                  p1    pn
                p = Pr(σ) = 1 · p1 · · · pn        where σ1 −→π · · · −→π σn .                 (2)

Thus, a path with no transitions consists of a single state σ, and Pr(σ) = 1. Let pathsπ (σ)
denote the set of all paths with policy π from σ to final states.
    In this paper we assume that MDPs (and the programs we derive them from) arrive at
final states with probability 1 under all policies. This means that the logic pDL that we will
be defining and interpreting over these MDPs can only talk about properties of almost
surely terminating programs, so in general it cannot be used to reason about termination
without adaptation. This is what corresponds to the notion of partial correctness in
non-probabilistic proof systems.
    An MDP may have an associated reward function r : State → [0, 1] that assigns a
real value r(σ) to any final state σ ∈ State. (In this paper we assume that rewards are
zero everywhere but in the final states.) We define the expectation of the reward starting
in a state σ as the greatest lower bound on the expected value of the reward over all
policies; so the real valued function defined as
                                                    X
                  Eσ (r) = inf Eσ,π (r) = inf            Pr(σ) r(final(σ)) ,               (3)
                             π                 π
                                                   σ∈pathsπ (σ)

where Eσ,π (r) stands for the expected value of the random variable induced by the reward
function under the given policy, known as the expected reward. Note that the expectation
Eσ (r) always exists and it is well defined. First, for a given policy the expected value
Eσ,π (r) is guaranteed to exist, as we only consider terminating executions and our
reward functions are bounded, non-negative, and non-zero in final states only. The set of
possible positional policies that we are minimizing over might be infinite, but the values
we are minimizing over are bounded from below by zero, so the set of expected values
has a well defined infimum. Finally, because the MDPs considered here almost surely
arrive at a final state, we do not need to condition the expectations on terminating paths to
re-normalize probability distributions, which greatly simplifies the technical machinery.
    To avoid confusing expectations and scalar values, we use bold font for expectations
in the sequel. For instance, p represents an unknown expectation from the state space
into [0, 1], and 0 represents a constant expectation function, equal to zero everywhere.


                                                   4
         v ::= true | false | 0 | 1 | . . .
         e ::= v | x | op e | e op e
         op ::= + | − | ∗ | / | > | == | ≥
         s ::= s u s | s e ⊕ s | s; s | skip | x := e | if e {s} else {s} | while e {s}

           Fig. 1. The syntax of the probabilistic guarded command language pGCL


    We use characteristic functions to define rewards for the semantics of pGCL pro-
grams, consistently with McIver & Morgan [7]. For a formula ϕ in some logic with
the corresponding satisfaction relation, a characteristic function [[ϕ]], also known as
a Boolean embedding or an indicator function, assigns 1 to states satisfying ϕ and 0
otherwise. In this paper, models will be program states, and also states of an MDP. In
general, characteristic functions can be replaced by arbitrary real-valued functions [3],
but this is not needed to interpret logical specifications, so we leave this to future work.
    Finally, given a formula ϕ that can be interpreted over a state space of an MDP, we
define the truncation of a reward function p as the function (p ↓ ϕ)(σ) = p(σ) · [[ϕ]](σ).
The truncation of p to ϕ maintains the original value of p for states satisfying ϕ and
gives zero otherwise. Note that p ↓ ϕ remains a valid reward function if p was.

4    pGCL: A Probabilistic Guarded Command Language
The probabilistic guarded command language pGCL [7], extends Dijkstra’s guarded
command language [8] with probabilistic choice. Figure 1 gives the syntax of pGCL. We
let x range over the set X of program variables, v over primitive values, and e over
expressions Exp. Expressions e are constructed over program variables x and primitive
values v by means of unary and binary operators op (including logical operators ¬, ∧, ∨
and arithmetic operators +, −, ∗, /). Expressions are assumed to be well-formed.
    Statements s include the non-deterministic (or demonic) choice s1 u s2 between the
branches s1 and s2 . We write s e ⊕ s0 for the probabilistic choice between the branches s
and s0 ; if the expression e evaluates to a value p given the current values for the program
variables, then s and s0 have probability p and 1 − p of being selected, respectively. In
many cases e will be a constant, but in general it can be an expression over the state
variables (i.e., e ∈ Exp), so its semantics will be an real-valued function. Sequential
composition, skip, assignment, if-then-else and while are standard (e.g., [8]).
    The semantics of pGCL programs s is defined as an MDP Ms (cf. [21]), and its
executions are captured by the partial transition probability function for a given policy
                                  p
π, which induces the relation −  →π for some probability p, (Eq. (1)). A state σ of Ms is
a pair of a valuation and a program, so σ = hε, si where the valuation ε is a mapping
from all the program variables in s to concrete values (sometimes we omit the program
part, if it is unambiguous in the context). The state hε, si represents an initial state of the
program s given some initial valuation ε and the state hε, skipi represents a final state in
which the program has terminated with the valuation ε.
    The rules defining the partial transition probability function for a given policy π are
                                          p
shown in Fig. 2. We denote by hε, si −   →π hε0 , s0 i the transition from hε, si to hε0 , s0 i by


                                                5
                                               (P ROB C HOICE 1)
                                             ε(e) = p 0 ≤ p ≤ 1                  (D EM C HOICE )
          (A SSIGN )
         0                                                 p                        i ∈ {1, 2}
       ε = ε[x 7→ ε(e)]                    hε, s1 e ⊕ s2 i −
                                                           →π hε, s1 i
                                                                                πhε, s1 u s2 i = si
                 1
            →π hε0 , skipi
hε, x := ei −                                  (P ROB C HOICE 2)                           1
                                                                                           →π hε0 , si i
                                                                             hε, s1 u s2 i −
                                             ε(e) = p 0 ≤ p ≤ 1
                                                                                      (I F 1)
       (C OMPOSITION 1)                                   1−p
                                          hε, s1 e ⊕ s2 i −−→π hε, s2 i
               p                                                                   ε(e) = true
               →π hε0 , s2 i
      hε, s1 i −
                     p                             (W HILE 1)                hε, if e {s1 } else {s2 }i
                →π hε0 , s2 i
 hε, skip; s1 i −                                                                    1
                                                  ε(e) = true                       −
                                                                                    →π hε, s1 i
                                                     1
                                   hε, while e {s}i −
                                                    →π hε, s; while e {s}i             (I F 2)
       (C OMPOSITION 2)
               p                                                                   ε(e) = false
               →π hε0 , s2 i
      hε, s1 i −                                   (W HILE 2)
               p                                  ε(e) = false               hε, if e {s1 } else {s2 }i
                →π hε0 , s2 ; si
    hε, s1 ; si −                                                                    1
                                                           1                        −
                                                                                    →π hε, s2 i
                                        hε, while e {s}i −
                                                         →π hε, skipi


                                     Fig. 2. An MDP-semantics for pGCL.


action α = π(hε, si), where p is the resulting probability. Note that for demonic choice,
the policy π fixes the action choice between the distributions 0, 1 and 1, 0; for all other
statements, there is already a single successor distribution. The transitive closure of this
                            p
relation, denoted hε0 , s0 i−
                            →∗π hεn , sn i, expresses that there is a sequence of zero or more
such transitions from hε0 , s0 i to hεn , sn i with corresponding actions αi = π(εi , si ) and
probability pi for 0 < i ≤ n, such that p = 1 · p1 · · · pn .
    Remark that the rules in Fig. 2 allow programs to get stuck, for instance if an ex-
pression e evaluates to a value outside [0, 1] (P ROB C HOICE). Since we are interested
in partial correctness, we henceforth rule out such programs and only consider programs
that successfully reduce to a single skip statement under all policies with probability 1.


5      Probabilistic Dynamic Logic

Formulae & Satisfiability. Given sets X of program variables and L of logical variables
disjoint from X, let ATF denote the well-formed atomic formulae built using constants,
program and logical variables. For every l ∈ L, let dom l denote the domain of l. We
extend valuations to also map logical variables l ∈ L to values in dom l and let ε |=ATF ϕ
denote standard satisfaction, expressing that ϕ ∈ ATF holds in valuation ε.
    The formulae of probabilistic dynamic logic (pDL) are defined inductively as the
smallest set generated by the following grammar:

                         ϕ     ::=     ATF | ¬ϕ | ϕ1 ∧ ϕ2 | ∀l · ϕ | [s]p ϕ                           (4)


                                                      6
where ϕ ranges over pDL formulae, l ∈ L over logical variables, s is a pGCL program with
variables in X, and p is an expectation assigning values in [0, 1] to initial states of the
program s. The logical operators →, ∨ and ∃ are derived in terms of ¬, ∧ and ∀ as usual.
    The last operator in Eq. (4) is known as the box-operator in dynamic logics, but now
we give it a probabilistic interpretation along with the name “p-box.” Given a pGCL
program s, we write [s]p ϕ to express that the expectation that a formula ϕ holds after
successfully executing s is at least p; i.e., the function p represents the expectation for ϕ
in the current state of Ms using [[ϕ]] as the reward function (see Sect. 3). For the reader
familiar with the CTL/PCTL terminology, the p-box formulae are path formulae, and all
other formulae are state formulae.
    We define semantics of well-formed formulae in pDL, so formulae with no free logical
variables—all occurrences of logical variables are captured by a quantifier. The definition
extends the standard satisfaction relation of dynamic logic [9] to the probabilistic case:
Definition 2 (Satisfaction of pDL Formulae). Let ϕ be a well-formed pDL formula, π
range over policies, l ∈ L, p : State → [0, 1] be an expectation lower bound, and ε be a
valuation defined for all variables mentioned in ϕ. The satisfiability of a formula ϕ in a
model ε, denoted ε |= ϕ, is defined inductively as follows:

      ε |= ϕ              iff ε |=ATF ϕ for          ϕ ∈ ATF
      ε |= ϕ1 ∧ ϕ2        iff ε |= ϕ1      and       ε |= ϕ2
      ε |= ¬ϕ             iff   not ε |= ϕ
      ε |= ∀l · ϕ         iff ε |= ϕ[l := v] for each v ∈ dom l
      ε |= [s]p ϕ         iff p(ε) ≤ Eε [[ϕ]] where the expectation is taken in Ms

For ϕ ∈ ATF, |=ATF can be used to check satisfaction just against the valuation of program
variables since ϕ is well-formed. In the case of universal quantification, the substitution
replaces logical variables with constants. The last case (p-box) is implicitly recursive,
since the characteristic function [[ϕ]] refers to the satisfaction of ϕ in the final states of s.
    The satisfaction of a p-box formula [s]p ϕ captures a lower bound on the probability
of ϕ holding after the program s. Consequently, pDL supports specification and reasoning
about probabilistic reachability properties in almost surely terminating programs.
    It is convenient to omit the valuation ε from the satisfaction judgement, meaning that
the judgement holds for all valuations (validity):

                     |= [s]p ϕ iff     ε |= [s]p ϕ for all valuations ε                      (5)



6    The p-box Modality and Logical Connectives
We begin our investigation of pDL by exploring how the p-box operator interacts with
different expectations and the other connectives of pDL.
     In a proof system, weakening is useful to allow adjusting proven facts to a format of
a syntactic proof rule. Since all operators of pDL, with the exception of p-box, behave like
in first order logic, the usual qualitative weakening properties apply for these operators


                                                 7
at the top-level. For instance, ϕ1 ∧ ϕ2 can be weakened to ϕ1 . These properties follow
directly from Def. 2. The following proposition states the key properties for p-box:

Proposition 3 (Weakening). Let ε stand for a valuation, p, 0 ∈ State → [0, 1] be
expectation lower bounds, s a pGCL program, and ϕ ∈ pDL. Then:

 1. Universal lower bound: ε |= [s]0 ϕ
 2. Quantitative weakening: ε |= [s]p1 ϕ then ε |= [s]p2 ϕ if p2 ≤ p1 everywhere
 3. Weakening conjunctions: ε |= [s]p (ϕ1 ∧ ϕ2 ) then ε |= [s]p ϕi for i = 1, 2
 4. Qualitative weakening: ε |= [s]p ϕ1 and |= ϕ1 → ϕ2 then ε |= [s]p ϕ2 .

The first point states that there is a limit to the usefulness of weakening the expectation:
if you cannot guarantee that the lower bound is positive, then you do not have any
information at all. A zero lower-bound would hold for any property. The second property
is a probabilistic variant of weakening, which follows directly from the last case of
Def. 2; the lower bound on an expectation can always be lowered. The last two properties
are the probabilistic counterparts of weakening in standard (non-probabilistic) dynamic
logic; the third property is syntactic for conjunction, the last one is general.
    When building proofs with pDL, the other direction of reasoning seems more useful:
we would like to be able to derive a conjunction from two independently concluded facts.
For state formulae, this holds naturally, like in first-order logic. For p-box formulae, we
would like to use the expectations pi of two formulae ϕi to draw conclusions about the
expectation that their conjunction holds. It seems tempting to translate the intuitions from
the Boolean lattice to real numbers, and to suggest that a minimum of the expectations
for both formulae is a lower bound for their conjunction. To develop some intuition, let
us first consider an incorrect proposal using the following counterexample:

Example 4. Consider the program 3, modeling a six-sided fair die:

       3     ::=    x:=1 1/6 ⊕ (x:=2 1/5 ⊕ (x:=3 1/4 ⊕ (x:=4 1/3 ⊕ (x:=5 1/2 ⊕ x:=6 ))))    (6)

Let ‘odd’ be an atomic formula stating that a value is odd, and ‘prime’ an atomic formula
stating that it is prime. Since the die is fair, the expectations for each of these after 3 are:

                       |= [3]1/2 odd(x)        |= [3]1/2 prime(x)                           (7)

The minimum of the two expectations is a constant function which equals 1/2 everywhere,
but the expectation bound in [s]p (odd(x) ∧ prime(x)) can be at most 1/3 since only two
outcomes (x 7→ 3 and x 7→ 5) satisfy both predicates. Effectively, even if ε |= [s]p1 ϕ1
and ε |= [s]p2 ϕ2 hold, we do not necessarily have ε |= [s]min(p1 ,p2 ) ϕ1 ∧ ϕ2 . The
reason is that the expectation bounds measure what is the lower bound on satisfaction
of a property, but not where in the execution space this probability mass is placed. There
is not enough information to see to what extent the two properties are overlapping. t   u

Similarly, p(ε) = p1 (ε)p2 (ε) is not a good candidate in Ex. 4, since it is only guaranteed
to be a lower bound for a conjunction when ϕi are independent events. Unless p1 = p2 =
1, combining proven facts with conjunction (or disjunction) weakens the expectation:


                                               8
Theorem 5. Let ε be a valuation, p, p1 , p2 ∈ State → [0, 1] expectation lower bounds,
s a pGCL program, and ϕ1 , ϕ2 ∈ pDL. Then:

 1. p-box conjunction: if ε |= [s]p1 ϕ1 and ε |= [s]p2 ϕ2 , then ε |= [s]p (ϕ1 ∧ ϕ2 ) where
    p = max(p1 +p2 − 1, 0) everywhere.
 2. p-box disjunction: if ε |= [s]p1 ϕ1 or ε |= [s]p2 ϕ2 , then ε |= [s]p (ϕ1 ∨ ϕ2 ) where
    p = min(p1 , p2 ) everywhere.

Note the asymmetry between these cases: reasoning about conjunctions of low proba-
bility properties using Thm. 5.1 is inefficient, and quickly arrives at the lower bound
expectation 0, which, as observed in Prop. 3, holds vacuously. If both properties have
an expected probability lower than 1/2, then pDL cannot really see (in a compositional
manner) whether there is any chance that they can be satisfied simultaneously. In con-
trast, compositional reasoning about disjunctions makes sense both for low and high
probability events. This is a consequence of using lower bounds on expectations. The
bounds in Thm. 5 are consistent with prior work by Baier et al. on LTL verification of
probabilistic systems [26].
    The qualitative non-probabilistic specialization of Thm. 5.1 behaves reasonably:
when ϕ1 or ϕ2 hold almost surely, then the theorem reduces to a familiar format:

                 if ε |= [s]p ϕ1 and ε |= [s]1 ϕ2 then ε |= [s]p (ϕ1 ∧ ϕ2 )             (8)

Theorem 6. Let ε be a valuation, p ∈ State → [0, 1] an expectation lower bound, s a
pGCL program, and ϕ ∈ pDL a well-formed formula.
 1. If ε |= [s]p ∀l · ϕ then ε |= ∀l · [s]p ϕ, but not the other way around in general.
 2. If ε |= ∃l · [s]p ϕ then ε |= [s]p ∃l · ϕ but not the other way around in general.

The essence of the above two properties lies in the fact that quantifiers in pDL only
affect logical variables, programs cannot access logical variables, and we do not allow
quantification over expectation variables.
    In a deductive proof system, one works with abstract states, not just concrete states.
A state abstraction can be introduced as a precondition, a pDL property that captures
the essence of an abstraction, and is satisfied by all the abstracted states sharing the
property. If an abstract property is a precondition for a proof, it is naturally introduced
using implication. However, implication is unwieldy in an expectation calculus, so it
is practical to be able to eliminate it in the proof machinery. The following theorem
explains how a precondition can be folded into an expectation function:
Theorem 7 (Implication Elimination). Let s be a pGCL program, ϕi be pDL formulae,
and p a lower-bound function for expectations. Then:

                         |= ϕ1 → ([s]p ϕ2 ) iff      |= [s]p↓ϕ1 ϕ2

Note that we use validity naturally when working with abstract states, as the state is
replaced by the precondition in the formula.
    Finally, negation in pDL is difficult to push over boxes. This is due to non-determinism
and the lower bound semantics of expectations it enforces. A p-box property expresses


                                             9
a lower bound on probability of a post-condition holding after a program. Naturally, a
negation of a p-box property will express an upper-bound on a property, but pDL has no
upper-bound modality first-class. We return to this problem in Sect. 8, where we discuss
reasoning about upper-bounds in non-deterministic and in purely probabilistic programs.


7   Expectations for Program Constructs

This section investigates how expectations are transformed by pGCL program constructs,
as opposed to logical constructs discussed above. We begin by looking at the composite
statements, which build the structure of the underlying MDP. The probabilistic choice
introduces a small expectation update, consistent with an expectation of a Bernoulli
variable (item 1). The demonic choice (item 2), requires that both sides provide the same
guarantee, which is consistent with worst-case reasoning.
Theorem 8 (Expectation and Choices). Let si be programs, ϕ a PDL formula, pi
lower bound functions for expectations into [0, 1], and ε a valuation of variables. Then:

 1. If ε |= [s1 ]p1 ϕ and ε |= [s2 ]p2 ϕ then ε |= [s1 e ⊕ s2 ]p ϕ
    with p = ε(e)p1 +(1−ε(e))p2
 2. ε |= [s1 ]p ϕ and ε |= [s2 ]p ϕ if and only if ε |= [s1 u s2 ]p ϕ

Note that in the second case, demonic, we can always use weakening (Prop. 3.2) to
equalize the left-hand-side expectation lower-bounds using a point-wise minimum, if the
premises are established earlier for different lower bound functions.

Example 9. This example shows that a non-deterministic assignment is less informative
than a probabilistic assignment. It shows that pDL can be used to make statements that
compare programs directly in the formal system—one of its distinctive features in com-
parison with prior works (cf. Sect. 2). We check satisfaction of the following pDL formula
for any expectation lower bound p:

    |= ∀δ · ∀p · 0 ≤ p ≤ 1 → ([x:=0 u x:=1]p (x ≥ δ) → [x:=0 p ⊕ x:=1]p (x ≥ δ)) .

For simplicity, we use the logical variable p directly in the rightmost program (this can
easily be encoded as an additional assumption equating a fresh logical variable to a
program variable). For the proof, we first simplify the formula using equivalence rewrites:

|= ∀δ · ∀p · 0 ≤ p ≤ 1 → ([x:=0 u x:=1]p (x ≥ δ) → [x:=0 p ⊕ x:=1]p (x ≥ δ))
iff for ε, δ, p we have
ε |= 0 ≤ p ≤ 1 → ([x:=0 u x:=1]p (x ≥ δ) → [x:=0 p ⊕ x:=1]p (x ≥ δ)) (Sect. 5, Def. 2 ∀)
iff for ε, δ, p we have
ε |= ¬0 ≤ p ≤ 1∨¬[x:=0 u x:=1]p (x ≥ δ) ∨ [x:=0 p ⊕ x:=1]p (x ≥ δ)        (syntactic sugar)
iff for ε, δ, p we have
¬0 ≤ p ≤ 1 ∨ ¬p(ε) ≤ Eε (x ≥ δ) ∨ p(ε) ≤ Eε (x ≥ δ)                       (Def. 2, the box)


                                              10
In the last line above the left expectation is taken in MDP Mx:=0ux:=1 and the right
one is taken in Mx:=0 p⊕x:=1 .
    Now the property is a disjunction of three cases. If the first or second disjunct hold
the formula holds vacuously (the assumptions in the statement are violated). We focus
on the last case, when the first two disjuncts are violated (so the assumptions hold). We
need to show that the last disjunct holds. We split the reasoning in two cases:

 1. δ ≤ 0: Consider the right expectation Eε (x ≥ δ). In the right program this expec-
    tation is equal to 1 because the formula always holds (both possible values of x are
    greater or equal to δ). Consequently, any expectation lower bound p is correct for
    this formula: p(ε) ≤ Eε (x ≥ δ) in the right program.
 2. δ > 0: Consider the left expectation Eε (x ≥ δ). By Eq. (3) this expectation is equal
    to zero (the policy that chooses the left branch in the program violates the property
    as x = 0 < δ). Since p(ε) ≤ Eε (x ≥ δ) = 0, it must be that p(ε) = 0 in the left
    program. By the universal lower bound property (Prop. 3.1), all properties hold after
    any program with the expectation lower bound p, including the post-condition of
    the right program.                                                                 t
                                                                                       u

For any program logic, it is essential that we can reason about composition of consecutive
statements; allowing the post-condition of one to be used as a pre-condition for the other.
The following theorem demonstrates that sequencing in pGCL corresponds to composition
of expectations in the MDP domain. It uses implication elimination (Thm. 7) to compute
a post-condition for a sequence of programs. Crucially, the new lower bound is computed
using an expectation operation in the MDP of the first program, using the lower-bound
of the second program as a reward function. Here, the expectation operation acts as a
way to explore the program graph and accumulate values in final states.

Theorem 10 (Expectation and Sequencing). Let si be pGCL programs, ϕi be pDL
formulae, ε be a valuation, and p an expectation lower bound function.
               If |= ϕ1 → ([s2 ]p ϕ2 ) then ε |= [s1 ; s2 ]Ehε,s1 i (p↓ϕ1 ) ϕ2 ,

where the expectation Ehε,s1 i (p ↓ ϕ1 ) is taken in Ms1 with p ↓ ϕ1 as the reward function.

For a piece of intuition, note that the above theorem captures the basic step of a backwards
reachability algorithm for MDPs, but expressed in pDL; it accumulates expectations
backwards over s1 from what is already known for s2 .
    We now move to investigating how simple statements translate expectations:
Theorem 11 (Unfolding Simple Statements). Let s be a pGCL program, ϕ a pDL for-
mula, p a function into [0, 1], a lower bound on expectations, and ε a valuation. Then

 1. ε |= [skip]1 ϕ iff ε |= ϕ
 2. ε |= [s]p ϕ iff ε |= [skip; s]p ϕ
 3. ε |= [x:=e; s]p ϕ iff ε[x 7→ ε(e)] |= [s]p ϕ

The case of if-conditions below is rather classic (Thm. 12.3). For any given state, we can
evaluate the head condition and inherit the expectation from the selected branch. For this


                                             11
to work we assume that the atomic formulae (ATF) satisfaction semantics in pDL is consis-
tent with the expression evaluation semantics in pGCL. The case of while loops is much
more interesting—indeed a plethora of works have emerged recently on proposing sound
reasoning rules for while loop invariants, post-conditions and termination (see Sect. 2). In
this paper, we show the simplest possible reasoning rule for loops that performs a single
unrolling, exactly along the operational semantics. Of course, we are confident that many
other rules for reasoning about while loops (involving invariants, prefixes, or converging
chains of probabilities) can also be proven sound in pDL—left as future work.

Theorem 12 (Unfolding Loops and Conditionals). Let e be a program expression
(also an atomic pDL formula over program variables in X), ϕ be a pDL atomic formula,
si be pGCL programs, p an expectation lower bound function, and ε a valuation. Then:

 1. If ε |= e ∧ [s1 ]p ϕ then ε |= [if e { s1 } else { s2 } ]p ϕ
 2. If ε |= ¬e ∧ [s2 ]p ϕ then ε |= [if e { s1 } else { s2 } ]p ϕ
 3. ε |= [if e { s; while e { s }} else {skip} ]p ϕ iff ε |= [ while e { s } ]p ϕ


8      Purely Probabilistic and Deterministic Programs

The main reason for the lower-bound expectation semantics in pDL (inherited from
McIver&Morgan) is the presence of demonic choice in pGCL. With non-determinism in the
language, calculating precise probabilities is not possible. However, this does not mean
that pDL cannot be used to reason about upper-bounds. The following theorem explains:4

Theorem 13 (Joni’s Theorem). For a policy π, property ϕ, program s, and state ε: if
ε |= [s]p1 ϕ and ε |= [s]p2 ¬ϕ then Eπ,ε [[ϕ]] ∈ [p1 , 1 − p2 ].

The theorem means that for a purely probabilistic program derived by fixing a policy
for a pGCL program s, the expected reward is bounded from below by the expectation of
this reward in s, and from above by the expectation of its negation in s. The theorem
follows directly from Eq. (3) and the negation case in Def. 2.
    For deterministic programs, some surprising properties, follow from interaction of
probability and logics. For instance, we can conclude a conjunction of expectations from
an expectation of a disjunction.

Theorem 14. Let s be a purely probabilistic pGCL program (a program that does not
use the demonic choice), let ε stand for a valuation, p ∈ State → [0, 1] be an expectation
function, and ϕi ∈ pDL properties. Then if ε |= [s]p (ϕ1 ∨ ϕ2 ) then there exist p1 , p2 ,
p1 + p2 ≥ p everywhere, such that ε |= [s]p1 ϕ1 and ε |= [s]p2 ϕ2 .

Intuitively, the property holds, because each of the measure of the space of final states of
the disjointed properties can be separated between the disjuncts. This separation would
not be possible with non-determinism, as shown in the following counterexample.
 4
     The theorem is named as a tribute to the song Both sides now by Joni Mitchell.


                                                12
Example 15. Consider the program ::= x := H u x := T. The following holds for any
initial valuation ε:
                            ε |= [ ]1 (x = H ∨ x = T)
This happens because disjunction is weakening and a weaker property is harder to
avoid, here impossible to avoid, for an adversary minimizing an expectation satisfaction.
However, at the same time: ε |= [ ]0 (x = H) and ε |= [ ]0 (x = T) and 0 + 0 < 1.
Importantly, zero is the tightest expectation lower bound possible here.               t
                                                                                       u


9     Program Analysis with pDL

In this section, we apply pDL to reason about two illustrative examples: the Monty Hall
game (Sect. 9.1), and convergence of a Bernoulli random variable (Sect. 9.2).


9.1   Monty Hall Game

In this section, we use pDL to compute the probability of winning the Monty Hall game.
In this game, a host presents 3 doors, one of which contains a prize and the others are
empty, and a contestant must figure out the door behind which the prize is hidden. To
this end, the host and contestant follow a peculiar sequence of steps. First, the location of
the prize is non-deterministically selected by the host. Secondly, the contestant chooses
a door. Then, the host opens an empty door from those that the contestant did not choose.
Finally, the contestant is asked whether she would like to switch doors. We determine,
using pDL, what option increases the chances of winning the prize (switching or not).
     Listing 1.1 shows a pGCL program, Monty_Hall, modeling the behavior of host and
contestant. There are 4 variables in this program: prize (door containing the prize),
choice (door selected by the contestant), open (door opened by the host), switch (Boolean
indicating whether the user switches in the last step). Note that the variable switch is
undefined in the program. The value of switch encodes the strategy of the contestant,
so its value will be part of a pDL specification that we study below. Line 1 models
the hosts’s non-deterministic choice of the door for the prize. Line 2 models the door
choice of the contestant (uniformly over the 3 doors). Lines 3-6 model the selection
of the door to open, from the non-selected doors by the contestant. Lines 7-10 model
whether the contestant switches door or not. For clarity and to reduce the size of the
program, in lines 6 and 8, we use a shortcut to compute the door to open and to switch,
respectively. Note that for x, y ∈ {0, 1, 2} the expression z = (2x − y) mod 3 simply
returns z ∈ {0, 1, 2} such that z 6= x and z 6= y. Similarly, in line 4, the expressions
y = (x + 1) mod 3, z = (x + 2) mod 3 ensure that y 6= x, z 6= x and y 6= z. This
shortcut computes the doors that the host may open when the contestant’s choice (line 2)
is the door with the prize.

                       Listing 1.1. Monty Hall Program (Monty_Hall)
                   1   prize := 0 u (prize := 1 u prize := 2);
                   2   choice := 0 1/3 ⊕ (choice:=1 1/2 ⊕ choice:=2);
                   3   if (prize = choice)
                   4      open := (prize+1)%3 u open := (prize+2)%3;



                                            13
                   5    else
                   6        open := (2*prize-choice)%3;
                   7    if (switch)
                   8        choice := (2*choice-open)%3
                   9    else
                  10        skip

We use pDL to find out the probability of the contestant selecting the door with the prize.
To this end, we check satisfaction of the following formula, and solve it for p.

                  ε[switch 7→ true] |= [Monty_Hall]p (choice = prize).                   (9)

First, we show that p = min(p0 , p1 , p2 ) where each pi is the probability for the different
locations of the prize. Formally, we use Thm. 8.2 (twice) as follows

                       ε |= [prize:=0;...]p0 (choice = prize) and
                       ε |= [prize:=1;...]p1 (choice = prize) and
                       ε |= [prize:=2;...]p2 (choice = prize) imply
                       ε |= [Monty_Hall]min(p0 ,p1 ,p2 ) (choice = prize)

For each pi , we compute the probability for each branch of the probabilistic choice. To
this end, we use Thm. 8.1 as follows:

ε |= [choice:=0;...]pi0 (choice = prize) and
ε |= [(choice:=1 1/2 ⊕ choice:=2);...]pi1 (choice = prize) imply
ε |= [choice:=0 1/3 ⊕ (choice:=1 1/2 ⊕ choice:=2);...]1/3·pi0 +2/3·pi1 (choice = prize).

and apply it again for pi1 to resolve the inner probabilistic choice:

        ε |= [choice:=1;...]pi10 (choice = prize) and
        ε |= [choice:=2;...]pi11 (choice = prize), implies
        ε |= [(choice:=1 1/2 ⊕ choice:=2);...]1/2·pi10 +1/2·pi11 (choice = prize)

These steps show that pi = 1/3 · pi0 + 2/3 · 1/2 · pi10 + 2/3 · 1/2 · pi11 where pi0 , pi10
and pi11 are the probabilities for the paths with choice equals to 0, 1 and 2, respectively.
    Let us focus on the case p1 . This is the case when the prize is behind door 1,
ε[prize 7→ 1]. In what follows, we explore the three possible branches of the probabilistic
choice. Consider the case where the user chooses door 1, i.e., ε[choice 7→ 1] and

          ε |= [if (prize = choice) {s0 } else {s1 };...]p110 (choice = prize)

where s0 and s1 correspond to lines 4 and 6 in Listing 1.1, respectively. Since ε |=
prize = choice holds and by Thm. 12.1 we derive that

                               ε |= [s0 ;...]p110 (choice = prize).

Note that p110 remains unchanged. Statement s1 contains a non-deterministic choice, so
we apply Thm. 8.2 to derive p110 = min(p1100 , p1101 ) where each p110i correspond to


                                               14
the cases where ε[open 7→ 2] and ε[open 7→ 0], respectively. Since switch = true both
branches execute line 8, and the probabilities remain the same (Thm. 12.1). A simple
calculation shows that after executing line 8 ε 6|= (prize = choice) for both cases. For
instance, consider
         ε[open 7→ 0] |= [choice := (2*choice-open)%3]p1100 (prize = choice).
By Thm. 11.3 ε[choice 7→ (2 ∗ 1 − 0)%3 = 2], which results in prize 6= choice. By the
universal lower bound rule (Prop. 3.1) we derive p1100 = 0. The same derivations show
that p1101 = 0, and, consequently, p110 = 0.
    The same reasoning shows that prize = choice holds for the cases where choice 6= 1
in line 2, i.e., pi0 and pi11 —we omit the details as they are analogous to the steps
above. In these cases, by Thm. 11.1 we derive that pi0 = 1 and pi11 = 1. Recall that
p110 = 0 (see above), then we derive that p1 = 1/3 · 1 + 2/3 · 1/2 · 0 + 2/3 · 1/2 · 1.
Consequently, p1 = 1/3 + 1/3 = 2/3. Analogous reasoning shows that all pi = 2/3.
    To summarize, the probability of choosing the door with the prize when switching
is at most 2/3. In other words, we have proven that switching door maximizes the
probability of winning the prize.

9.2   Convergence of a Bernoulli random variable
We use pDL to study the convergence of a program that estimates the expectation of a
Bernoulli random variable. To this end, we compute the probability that an estimated
expectation is above an error threshold δ > 0. This type of analysis may be of practical
value for verifying the implementation of estimators for statistical models.
     Consider the following pGCL program for estimating the expected value of a Bernoulli
random variable (Technically the program computes the number of successes out of n
trials, and we will put the estimation into the post-condition):
                          Listing 1.2. Bernoulli Program (Bernoulli)
                  1   i := 0; c := 0;
                  2   while (i < n) {
                  3       s := 0 µ ⊕ s := 1;
                  4       c := c + s;
                  5       i := i + 1
                  6   }

Intuitively,
        P Bernoulli computes the average of n Bernoulli trials Xi with mean µ, i.e.,
X =       i Xi /n. It is well-known that E[X] = µ (e.g., [27]). Each Xi can be seen
as a sample or measurement to estimate µ. A common way to study convergence is
to check the probability that the estimated mean X is within some distance δ > 0 of
µ, i.e., Pr(|X − µ| > δ). In Bernoulli, a sample Xi corresponds to the execution of
the probabilistic choice µ⊕ in line 3 of Listing 1.2. After
                                                         P running all loop iterations,
variable c contains the sum of all the samples, i.e., c = i Xi . Thus, X is equivalent
to c/n and the specification of convergence can be written as Pr(|c/n − µ| > δ). Note
that this specification is independent of the implementation of the program. The same
specification can be used for any program estimating µ—by simply replacing X with
the term estimating µ in the program.


                                             15
    In pDL, we can study the convergence of this estimator by checking

                            ε |= [Bernoulli]p (|c/n − µ| > δ)

for some value of µ ∈ [0, 1], δ > 0 and n ∈ N. Note that, since the program contains no
non-determinism, p = Pr(|X − µ| > δ). We describe the reasoning to compute p.
     First, note that the while-loop in Bernoulli is bounded. Therefore, we can replace it
with a sequence of n iterations of the loop body. Let si denote the ith iteration of the loop
(lines 3-4 in Listing 1.2). We omit for brevity the assignments in line 1 of Listing 1.2
and directly proceed with a state ε[c 7→ 0, i 7→ 0]. Consider the first iteration of the loop,
i.e., i = 0. By Thm. 12.3 we can derive

     ε |= [if (0 < n) {s0 ; while (i < n) {s1 }} else {skip}}]p (|c/n − µ| > δ).

Assume ε |= 0 < n holds, then by Thm. 12.1 we derive

                    ε |= [s0 ; while (i < n) {s1 }]p (|c/n − µ| > δ).

By applying the above rules repeatedly we can rewrite Bernoulli as

                        ε |= [s0 ;...;sn−1 ;skip]p (|c/n − µ| > δ)

with the skip added in the last iteration of the loop by Thm. 12.3 and 12.2.
    Second, we compute the value of p for a possible path of Bernoulli. Consider the
case when c = 0 after executing the program. That is,

                            ε |= [s0 ;...;sn−1 ;skip]p (c = 0).

This only happens for the path where the probabilistic choice is resolved as c:=0 for all
loop iterations. Applying Thm. 10 we derive

   If |= (c = 0) → [s1 ;. . .;sn−1 ;skip]p0 (c = 0), then
                                            ε |= [s0 ; . . . ; sn−1 ; skip]Eε p0 ↓(c=0) (c = 0).

Here Eε is computed over Ms0 (cf. Thm. 10). For Bernoulli, this expectation is com-
puted over the two paths resulting from the probabilistic choice in Listing 1.2, line 3.
Since only the left branch satisfies c = 0 and it is executed with probability µ, then
Eε p0 = µp0 . Applying this argument for each iteration of the loop we derive that
ε |= [s0 ;...;sn−1 ;skip;]p (c = 0) holds for p = µn . Similarly, consider the case where
c = 1 after running all iterations of the loop, due to the first iteration resulting in c:=1
and the rest c:=0. Then, we apply Thm. 10 as follows

   If |= (c = 1) → [s1 ;. . .;sn−1 ;skip]p0 (c = 1), then
                                            ε |= [s0 ; . . . ; sn−1 ; skip]Eε p0 ↓(c=1) (c = 1).

In this case, Eε p0 = (1 − µ)p0 , as the probability of c = 1 is (1 − µ) (cf. Listing 1.2 line
3). Since, in this case, the remaining iterations of the loop result in c:=0, and from our
reasoning above, we derive that p0 = µn−1 . Hence, p = (1 − µ)µn−1 . In general, by


                                             16
                                  1.0                                                  δ = 0.1
                                                                                       δ = 0.2
                                  0.8                                                  δ = 0.4




                   Pr(|c/n − 0.5| > δ )
                                  0.6


                                  0.4


                                  0.2


                                  0.0

                                          3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
                                             Number of loop iterations (number of samples)


               Fig. 3. Convergence of Bernoulli random variable with µ = 0.5.


repeatedly applying these properties, we can derive that the probability of a path is
µi (1 − µ)j where i is the number loop iterations resulting in c:=0 and j the number of
loop iterations resulting in c:=1.
    Now we return to our original problem ε |= [Bernoulli]p (|c/n − µ| > δ). Recall
from Def. 2 that p is the sum of the probabilities over all the paths that satisfy the
post-condition. BernoulliP has zeros(i)
                                 2n paths (two branches per loop iteration). Therefore,
we conclude that p = i∈Φ µ              (1 − µ)ones(i) where zeros(·), ones(·) are functions
returning the number of zeros and ones in the binary representation of the parameter,
respectively, and Φ = { i ∈ 2n | |ones(i)/n − µ| > δ } enumerates all paths in the
program satisfying the post-condition. Note that the binary representation of 0, . . . , 2n
conveniently captures each of the possible executions of Bernoulli.
    The result above is useful to examine the convergence of Bernoulli. It allows us to
evaluate the probability of convergence for increasing number of samples and different
values of µ and δ. As an example, Fig. 3 shows the results for µ = 0.5, δ ∈ {0.1, 0.2, 0.4}
and up to n = 20 iterations of the loop. The dotted and dashed lines in the figure show
that with 20 iterations the probability of having an error δ > 0.2 is less than 5%. However,
for an error δ > 0.1 the probability increases to more than 20%.


10    Conclusion
This paper has proposed pDL, a specification language for probabilistic programs—the
first dynamic logic for probabilistic programs written in pGCL. Like pGCL, pDL contains
probabilistic and demonic choice. Unlike pGCL, it includes programs as first-order entities
in specifications and allows forward reasoning capabilities as usual in dynamic logic.
We have defined the model-theoretic semantics of pDL and shown basic properties of
the newly introduced p-box modality. We demonstrated the reasoning capabilities on
two well-known examples of probabilistic programs. In the future, we plan to develop
a deductive proof system for pDL supported by tools for (semi-)automated reasoning
about pGCL programs. Furthermore, the current definition of pDL gives no syntax to the
expectations. Batz et al. propose a specification language for real-valued functions that


                                                                17
is closed under the construction of weakest pre-expectations [19]; such a language could
be used to express assertions for pGCL programs. It would be interesting to integrate these
advances into pDL.

Acknowledgments This work was supported by the Research Council of Norway via
SIRIUS (project no. 237898).

References
 1. Kozen, D.: Semantics of probabilistic programs. In: Proc. 20th Annual Symposium on
    Foundations of Computer Science, IEEE Computer Society (1979) 101–114
 2. Hark, M., Kaminski, B.L., Giesl, J., Katoen, J.: Aiming low is harder: induction for lower
    bounds in probabilistic program verification. Proc. ACM Program. Lang. 4(POPL) (2020)
    37:1–37:28
 3. Kaminski, B.L.: Advanced weakest precondition calculi for probabilistic programs. PhD
    thesis, RWTH Aachen University, Germany (2019)
 4. Stein, D., Staton, S.: Compositional semantics for probabilistic programs with exact condi-
    tioning. In: Proc. 36th Annual ACM/IEEE Symposium on Logic in Computer Science (LICS
    2021), IEEE (2021) 1–13
 5. Smolka, S., Kumar, P., Foster, N., Kozen, D., Silva, A.: Cantor meets Scott: semantic
    foundations for probabilistic networks. In Castagna, G., Gordon, A.D., eds.: Proc. 44th ACM
    SIGPLAN Symposium on Principles of Programming Languages (POPL 2017), ACM (2017)
    557–571
 6. Batz, K., Fesefeldt, I., Jansen, M., Katoen, J., Keßler, F., Matheja, C., Noll, T.: Foundations
    for entailment checking in quantitative separation logic. In Sergey, I., ed.: Proc. 31st European
    Symposium on Programming (ESOP 2022). Volume 13240 of Lecture Notes in Computer
    Science., Springer (2022) 57–84
 7. McIver, A., Morgan, C.: Abstraction, Refinement and Proof for Probabilistic Systems.
    Monographs in Computer Science. Springer (2005)
 8. Dijkstra, E.W.: A Discipline of Programming. Prentice-Hall (1976)
 9. Harel, D., Kozen, D., Tiuryn, J.: Dynamic Logic. Foundations of Computing. MIT Press
    (October 2000)
10. Hansson, H., Jonsson, B.: A logic for reasoning about time and reliability. Formal Aspects
    Comput. 6(5) (1994) 512–535
11. Puterman, M.L.: Markov Decision Processes. Wiley (2005)
12. Ahrendt, W., Beckert, B., Bubel, R., Hähnle, R., Schmitt, P.H., Ulbrich, M., eds.: Deductive
    Software Verification - The KeY Book - From Theory to Practice. Volume 10001 of Lecture
    Notes in Computer Science. Springer (2016)
13. de Gouw, S., Rot, J., de Boer, F.S., Bubel, R., Hähnle, R.:                           OpenJDK’s
    Java.utils.Collection.sort() is broken: The good, the bad and the worst case. In Kroening, D.,
    Pasareanu, C.S., eds.: Proc. 27th International Conference on Computer Aided Verification
    (CAV 2015). Volume 9206 of Lecture Notes in Computer Science., Springer (2015) 273–289
14. Cousot, P., Monerau, M.: Probabilistic abstract interpretation. In: Programming Languages
    and Systems, Springer (2012) 169–193
15. Filieri, A., Pasareanu, C.S., Visser, W.: Reliability analysis in symbolic pathfinder. In: 35th
    International Conference on Software Engineering (ICSE’13), IEEE Computer Society (2013)
    622–631
16. Kwiatkowska, M.Z., Norman, G., Parker, D.: The PRISM benchmark suite. In: Ninth Inter-
    national Conference on Quantitative Evaluation of Systems (QEST 2012), IEEE Computer
    Society (2012) 203–204


                                                18
17. Kozen, D.: A probabilistic PDL. J. Comput. Syst. Sci. 30(2) (1985) 162–178
18. Feldman, Y.A., Harel, D.: A probabilistic dynamic logic. In: Proceedings of the 14th Annual
    ACM Symposium on Theory of Computing (STOC), ACM (1982) 181–195
19. Batz, K., Kaminski, B.L., Katoen, J., Matheja, C.: Relatively complete verification of
    probabilistic programs: an expressive language for expectation-based reasoning. Proc. ACM
    Program. Lang. 5(POPL) (2021) 1–30
20. Hähnle, R.: Dijkstra’s legacy on program verification. In Apt, K.R., Hoare, T., eds.: Edsger
    Wybe Dijkstra: His Life, Work, and Legacy. ACM / Morgan & Claypool (2022) 105–140
21. Gretz, F., Katoen, J., McIver, A.: Operational versus weakest pre-expectation semantics for
    the probabilistic guarded command language. Perform. Evaluation 73 (2014) 110–132
22. McIver, A., Morgan, C., Kaminski, B.L., Katoen, J.: A new proof rule for almost-sure
    termination. Proc. ACM Program. Lang. 2(POPL) (2018) 33:1–33:28
23. Batz, K., Kaminski, B.L., Katoen, J., Matheja, C., Noll, T.: Quantitative separation logic: a
    logic for reasoning about probabilistic pointer programs. Proc. ACM Program. Lang. 3(POPL)
    (2019) 34:1–34:29
24. Kaminski, B.L., Katoen, J., Matheja, C., Olmedo, F.: Weakest precondition reasoning for
    expected run-times of probabilistic programs. In Thiemann, P., ed.: Programming Languages
    and Systems - 25th European Symposium on Programming, ESOP 2016. Volume 9632 of
    Lecture Notes in Computer Science., Springer (2016) 364–389
25. Aguirre, A., Barthe, G., Hsu, J., Kaminski, B.L., Katoen, J., Matheja, C.: A pre-expectation
    calculus for probabilistic sensitivity. Proc. ACM Program. Lang. 5(POPL) (2021) 1–28
26. Baier, C., Kwiatkowska, M.Z., Norman, G.: Computing probability bounds for linear time
    formulas over concurrent probabilistic systems. Electron. Notes Theor. Comput. Sci. 22
    (1999) 29
27. Dekking, F.M., Kraaikamp, C., Lopuhaä, H.P., Meester, L.E.: A modern introduction to
    probability and statistics: understanding why and how. Springer texts in statistics. Springer
    (2005)




                                               19
 A     Proofs

 A.1   Proofs and Auxiliary Properties for Sect. 3

 Expectations in an MDP. We start with a few basic order and distribution properties of
 expectations that are useful in later proofs.

 Lemma 16. Given a program s, the MDP Ms representing its semantics, its state σ,
 and reward functions r, r 1 , r 2 (into [0, 1] we have that

  1. Eσ (r) is a non-negative function for any non-negative reward function r.
  2. If r 1 ≤ r 2 everywhere then Eσ (r 1 ) ≤ Eσ (r 2 ) everywhere.
  3. Eσ (r 1 ) + Eσ (r 2 ) ≤ Eσ (r 1 + r 2 ) everywhere.
  4. For a constant c ∈ R we have that max[Eσ (r) + c, 0] ≤ Eσ [max(r + c, 0)]
  5. For a constant c ∈ [0, 1] we have that cEσ (r) = Eσ [cr]
  6. (1 − inf π r) = supπ (1 − r) and (1 − supπ r) = inf π (1 − r)
  7. Eσ,π (λσ 0 · Eπ,σ0 (r)) = Eσ,π (r)
  8. Eσ (λσ 0 · Eσ0 (r)) ≤ Eσ (r)

 Proof (Lemma 16).

16.3 We have equality in this property if there is no non-determinism (a Markov Chain
     instead of an MDP). Then the property is just a regular property of expected value
     of random variables. For an MDP we have:
                            h               i h               i
     Eσ (r 1 ) + Eσ (r 2 ) = inf Eσ,π (r 1 ) + inf Eσ,π (r 2 ) (def. of expectation, Eq. (3))
                                 π                 π
                         ≤ inf [Eσ,π (r 1 ) + Eσ,π (r 2 )]       (inf f + inf g ≤ inf(f + g))
                             π
                         = inf Eσ,π (r 1 + r 2 )                        (E distributes with +)
                             π
                         = Eσ (r 1 + r 2 )                                           (Eq. (3))

16.4 We have equality if c is non-negative.
                                  h                  i
     max (Eσ (r) + c, 0) = max inf Eσ,π (r) + c, 0                                    (Eq. (3))
                                     π
                                  h                   i
                          = max inf (Eσ,π (r) + c) , 0                   (shift inf by a const.)
                                      π
                           = inf max [Eσ,π (r) + c, 0]                 (argue by cases of max)
                                 π
                           = inf max[Eσ,π (r + c), 0]              (shift random variable by c)
                                 π
                           ≤ inf max {Eσ,π [max(r + c, 0)], 0}           (truncate random var)
                                 π
                           = inf Eσ,π [max(r + c, 0)]          (Eσ,π [max(r + c, 0)] nonneg.)
                                 π
                           = Eσ [max(r + c, 0)]                                       (Eq. (3))



                                              20
16.5 The equality follows from the fact that infimum and expected value both commute
     with a multiplication by a non-negative constant.
16.7 First a comment what the lambda notation in parentheses means: we mean that the
     random variable in the outer expected value is itself an expected value in final states
     of the outer Markov Chain (which are the initial states of the inner Markov Chain).
     As usual a random variable in a Markov Chain (or a reward in a Markov Chain) is
     a function that takes as an argument the state it is calculated from. We explicitly
     name this argument σ. Alternatively, we could have put a dot (·) instead of σ in the
     subscript of the inner expected value: λσ · Eπ,σ (r) means the same as Eπ,· (r).
     Now that the notation is out of the way, let’s prove the lemma by a sequence of
     equalities:

      Eσ,π (λσ 0 · Eσ0 ,π (r))                                                              (assumption LHS)
             X
      =              Pr(σ 1 )Efinal(σ1 ),π (r)                                                        (Eq. (3))
           σ 1 ∈paths(σ)
                                                                             
               X                            X
       =              Pr(σ 1 )                      Pr(σ 2 )r(final(σ 2 ))                          (Eq. (3))
           σ 1 ∈paths(σ)            σ 2 ∈paths(final(σ 1 ))
               X                  X
       =                                     Pr(σ 1 ) Pr(σ 2 )r(final(σ 2 ))        (distribute multiplication)
           σ 1 ∈paths(σ) σ 2 ∈paths(final(σ 1 ))
                 X
       =                   Pr(σ 1 σ 2 )r(final(σ 1 σ 2 ))                 (concatenate paths, now in Ms1 ;s2 )
           σ 1 σ 2 ∈paths(σ)

       = Eσ,π (r)                                                                                     (Eq. (3))

     Note that when we expand expected values using Eq. (3) the policy π disappears in
     the notation—it is implicitly included in the probability mass function Pr. We chose
     not to subscript it for readability. Also the paths set starting in σ in the penultimate
     row refer to the paths in Ms1 ;s2 (so the set of the longer paths).
16.8 The use of the lambda notation is the same as in the previous point, so see above.

           Eσ (λσ 0 · Eσ0 (r))                                                          (assumption LHS)
                                             
           = inf Eσ,π λσ 0 · inf0 Eσ0 ,π0 (r)                                               (Eq. (3) twice)
                 π                    π
            ≤ inf Eσ,π (λσ 0 · Eσ0 ,π (r))                     (infimum over a smaller set of policy pairs)
                 π
            ≤ inf Eσ,π (r)                                                           (Lemma 16.7 above)
                 π
            = Eσ (r)                                                                              (Eq. (3))
                                                                                                              t
                                                                                                              u

 Boolean embeddings (characteristic functions). For these properties it is useful to equate
 Boolean formulae with sets of states satisfying them (since these properties make sense
 for any classical logic, not necessarily PDL). The logical connectives then translate to
 set algebra in standard manner (conjunction is a intersection, etc.)


                                                              21
Lemma 17. Consider formulae (sets of states), ϕ, ϕ1 and ϕ2 . Then
 1. [[ϕ1 ]] + [[ϕ2 ]] − 1 ≤ [[ϕ1 ∧ ϕ2 ]] everywhere
 2. [[¬ϕ]] = 1 − [[ϕ]] and [[ϕ]] = 1 − [[¬ϕ]] everywhere
Proof (Lemma 17).
 1. Consider an element of State which is both in ϕ1 and in ϕ2 . Then the left hand side
    is 1, and so is the right hand side. The left hand side decreases by 1 or 2 for all other
    classes of elements, while the right hand side decreases by 1, so the inequality holds.
 2. [[ϕ]] is a zero-one function, and the construction just inverts the assignment of zeroes
    and ones, which is exactly what a negation does.
                                                                                          t
                                                                                          u

A.2     Proofs for Sect. 6
Proof (Proposition 3).
3.1. By Lemma 16.1 and the last case of Def. 2.
3.2. By assumption p2 (ε) ≤ p1 (ε) ≤ Ehε,si [[ϕ]] for any state (the latter by the last case
     in Def. 2). Thus, by Def. 2, the last case again, ε |= [s]p2 ϕ.
3.3. Note that |= ϕ1 ∧ ϕ2 → ϕi and see the next point.
3.4. Note that [[ϕ1 ]] ≤ [[ϕ2 ]] everywhere. By the last case in Def. 2 and Lemma 16.2 we
     have p(ε) ≤ Ehε,si [[ϕ1 ]] ≤ Ehε,si [[ϕ2 ]], hence ε |= [s]p ϕ2 .
                                                                                        t
                                                                                        u
Proof (Theorem 5).
5.1. We show that satisfaction can be concluded with the last case of Def. 2:
       p(ε) = max(p1 (ε) + p2 (ε) − 1, 0)
            ≤ max(Ehε,si [[ϕ1 ]] + Ehε,si [[ϕ2 ]] − 1, 0)                      (pi lowerbounds)
            ≤ max(Ehε,si ([[ϕ1 ]] + [[ϕ2 ]]) − 1, 0)                               (Lemma 16.3)
            ≤ Ehε,si (max([[ϕ1 ]] + [[ϕ2 ]] − 1, 0))                               (Lemma 16.4)
            ≤ Ehε,si (max([[ϕ1 ∧ ϕ2 ]], 0))                     (Lemma 17.1 and Lemma 16.2)
            = Ehε,si [[ϕ1 ∧ ϕ2 ]]                            (max([[ϕ1 ∧ ϕ2]], 0) = [[ϕ1 ∧ ϕ2 ]])
      The max operator is used to ensure that the obtained reward function is non-negative,
      which we wanted because we only work with rewards created by Boolean embed-
      dings. This way the resulting expectation always has values in [0, 1].
5.2. Assume, without loss of generality, that ε |= [s]p1 ϕ1 holds. We show that satisfac-
     tion can be concluded with the last case of Def. 2.
             p(ε) = min(p1 (ε), p2 (ε)) ≤ p1 (ε)                               (minimum)
                                          ≤ Ehε,si [[ϕ1 ]]          (Def. 2, ε |= [s]p1 ϕ1 )
                                          ≤ Ehε,si [[ϕ1 ∨ ϕ2 ]]                 (Prop. 3.4)


                                              22
                                                                                            t
                                                                                            u

Proof (Theorem 6).

6.1 First observe that for any value v ∈ dom l of a logical variable l ∈ L we have the
    following syntactic equality:

                          ([s]p ϕ) [l := v]    ≡     [s]p (ϕ[l := v])

    The two formulae are identical because the program s cannot refer to logical vari-
    ables (l). Now we build the argument using this fact:

     ε |= [s]p (∀l · ϕ)                                                         (assumption)
     implies ε |= [s]p (ϕ[l := v]) (pick v ∈ dom l, Lemma 16.2 as [[∀l · ϕ]] ≤ [[ϕ[l := v]]])
     iff ε |= ([s]p ϕ) [l := v]                                   (syntactic equality, above)

    Now observe that we have shown that ε |= [s]p (∀l · ϕ) implies ε |= ([s]p ϕ) [l := v]
    for arbitrary v ∈ dom l. By Def. 2 this means that it also implies ε |= ∀l · [s]p ϕ.
    Consider a counter example for the opposite direction. Let be a program modeling
    a fair coin: ::= x := H 1/2 ⊕ x := T and let dom l = {H, T}, and the following two
    properties. The first property ϕ1 holds in any environment, the second property ϕ2
    holds in no environment.

                  ϕ1 ≡ ∀l · [ ]1/2 (x = l)           ϕ2 ≡ [ ]1/2 (∀l · x = l)             (10)




                                              23
6.2 We first prove the positive case of the theorem:
     ε |= ∃l · [s]p ϕ                                                                 (assumption)
     iff ε |= ¬∀l · ¬[s]p ϕ                                                        (syntactic sugar)
     iff not ε |= ∀l · ¬[s]p ϕ                                                              (Def. 2)
     iff not for all v ∈ dom l: ε |= ¬[s]p (ϕ[l := v])               (Def. 2, synt. equality above)
     iff not for all v ∈ dom l not: ε |= [s]p (ϕ[l := v])                                   (Def. 2)
     iff exists v ∈ dom l: p(ε) ≤ inf Ehε,si,π [[ϕ[l := v]]]                  (Def. 2, meta-exists)
                                       π
     iff exists v ∈ dom l: p(ε) ≤ 1 − (1 − inf Ehε,si,π [[ϕ[l := v]]])                     (algebra)
                                            π
     iff exists v ∈ dom l: p(ε) ≤ 1 − sup 1 − Ehε,si,π [[ϕ[l := v]]]                 (Lemma 16.6)
                                                                      
                                            π
     iff exists v ∈ dom l: p(ε) ≤ 1 − sup Ehε,si,π (1 − [[ϕ[l := v]]]) (sum expected vals)
                                            π
     iff exists v ∈ dom l: p(ε) ≤ 1 − sup Ehε,si,π [[¬ϕ[l := v]]]                    (Lemma 17.2)
                                            π
     implies exists v ∈ dom l: p(ε) ≤ 1 − sup Ehε,si,π [[∀l · ¬ϕ]]
                                                 π
                                                          (as [[∀l · ¬ϕ]] ≤ [[¬ϕ[l := v]]] for any v)
     iff p(ε) ≤ 1 − sup Ehε,si,π [[∀l · ¬ϕ]]                                  (drop free quantifier)
                        π
     iff p(ε) ≤ inf Ehε,si,π (1 − [[∀l · ¬ϕ]])                                       (Lemma 16.6)
                  π
     iff p(ε) ≤ inf Ehε,si,π [[¬∀l · ¬ϕ]]                                            (Lemma 17.2)
                  π
     iff p(ε) ≤ Ehε,si [[∃l · ϕ]]                                         (syntactic sugar, Eq. (3))
     iff ε |= [s]p (∃l · ϕ)                                                                 (Def. 2)
    Consider a counter example for the opposite direction. Recall the program mod-
    eling a “non-deterministic coin:“ ::= x: = H t x := T and dom l = {H, T}, and
    the following two properties. The first property ϕ1 holds in any environment, the
    second property ϕ2 holds in no environment.
                      ϕ1 ≡ [ ]1 (∃l · x = l)             ϕ2 ≡ ∃l · [ ]1 (x = l)                  (11)
                                                                                                   t
                                                                                                   u
Proof (Theorem 7). We prove the co-occurrence of the two validities by splitting in
cases, based on whether a particular valuation ε satisfies the precondition or not.
Case 1: ε |= ϕ1 (works in both directions):
                        ε |= ϕ1 → ([s]p ϕ2 )             (thm assumption)
                        ε |= [s]p ϕ2                                 (case)
                        ε |= [s]p↓ϕ1 ϕ2              ((p ↓ ϕ1 )(ε) = p(ε))
Case 2: not ε |= ϕ1 then the left-hand-side holds vacuously. The right-hand-side also
holds because the expectation is zero (p ↓ ϕ1 )(ε) = p(ε) · ([[ϕ1 ]](ε)) = p(ε) · 0 = 0
which means the formula holds by Prop. 3.1.                                          t
                                                                                     u


                                                24
A.3     Proofs for Sect. 7
Proof (Theorem 8).

8.1 Let i denote the program s1 e ⊕ s2 . From left to right, we need to show that
    ε(e)p1 (ε) +(1−ε(e))p2 (ε) ≤ Ehε,ii [[ϕ]] where the expectation is taken in Ms1 e ⊕s2 .

      ε(e)p1 (ε) + (1 − ε(e))p2 (ε)
      ≤ ε(e)Ehε,s1 i [[ϕ]] + (1 − ε(e))Ehε,s2 i [[ϕ]] (left in Ms1 , right in Ms2 by assumption)
      = Ehε,s1 i [ε(e)[[ϕ]]] + Ehε,s2 i [(1 − ε(e))[[ϕ]]]                       (Lemma 16.5 twice)
              h                                    i
                          (1)                  (2)
      ≤ Ehε,ii ε(e)[[ϕ]] + (1−ε(e))[[ϕ]]            (Lemma 16.3, [[ϕ]](k)positive only for sk states)
      = Ehε,ii [[ϕ]]              (now in Ms1 e⊕s2 extending expected value as per P ROB C HOICE 1/2)

8.2 Let i denote the program s1 u s2 . For the proof from left to right, we need to show
    that p(ε) ≤ Eε [[ϕ]] where the expectation is taken in the Ms1 us2 :

      p(ε)
       ≤ min{Ehε,s1 i [[ϕ]], Ehε,s2 i [[ϕ]]}                  (left in Ms1 , right in Ms2 by assumption)
       = min{inf Ehε,s1 i,π1 [[ϕ]], inf Ehε,s2 i,π2 [[ϕ]]}        (left in Ms1 , right in Ms2 by Eq. (3))
                  π1                     π2
       = inf{inf Ehε,s1 i,π1 [[ϕ]], inf Ehε,s2 i,π2 [[ϕ]]}                  (inf is minimum in a finite set)
                 π1                     π2
       = inf Ehε,ii,π [[ϕ]]                  (inf of infima, D EM C HOICE has two policies, no ε change)
           π
       = Ehε,ii [[ϕ]]                                                                (in Ms1 us2 , Eq. (3))

      The argument in the opposite direction follows by the same equalities backwards,
      and then the fact that a lower bound of a minimum is small than each element in a set.
                                                                                         t
                                                                                         u
Proof (Theorem 10). Let i denote the program s1 ; s2 . To show that

                                       ε |= [s1 ; s2 ]Ehε,s1 i (p↓ϕ1 ) ϕ2

we need to demonstrate that

                                     Ehε,s1 i (p ↓ ϕ1 ) ≤ Ehε,ii [[ϕ2 ]] ,

where the left expectation is taken in Ms1 and the right expectation is taken in Ms1 ;s2 .
We use the theorem’s assumption |= ϕ1 → ([s2 ]p ϕ2 ) to get |= [s2 ]p↓ϕ1 ϕ2 by Thm. 7.
This in turn means that (p ↓ ϕ1 )(ε0 ) ≤ Ehε0 ,s2 i [[ϕ2 ]] for all ε0 (with the latter expectation
taken in Ms2 ).

               Ehε,s1 i (p ↓ ϕ1 )
               ≤ Ehε,s1 i λε0 · Ehε0 ,s2 i [[ϕ2 ]]        (because |= [s2 ]p↓ϕ1 ϕ2 and Def. 2)
                                                     

               ≤ Ehε,ii [[ϕ2 ]]                                                  (Lemma 16.8)

                                                                                                          t
                                                                                                          u


                                                         25
 Proof (Theorem 11).

11.1 Let us start from the left hand side, so assume that ε |= [skip]1 ϕ. Then

      1 = 1(ε)
        ≤ Ehε,skipi [[ϕ]]                                                                    (Def. 2)
        = inf Ehε,skipi,π [[ϕ]]                                                             (Eq. (3))
             π
        = Ehε,skipi [[ϕ]]                                        (skip deterministic, single policy)
                X
        =               Pr(σ) · ([[ϕ]](final(σ)))                                           (Eq. (3))
            σ∈paths(hε,skipi)
                  X
        =                Pr(σ) · ([[ϕ]](ε)) (definition of final, for pDL [[ϕ]](hε, skipi) = [[ϕ]](ε))
            σ∈paths(hε,skipi)

        = 1 · [[ϕ]](ε)                                          (only one final path, singleton size)

     We have shown that 1 ≤ [[ϕ]](ε), which by definition of characteristic functions
     means that ε |= ϕ. For the opposite direction, take ε |= ϕ and use the above
     six equalities from the bottom to show that 1(ε) = Ehε,skipi [[ϕ]], which means
     ε |= [skip]1 ϕ.

11.2 One could argue from Thm. 10, but this is cumbersome, as it requires weakening
     the left-hand side to validity, which is not needed for skip, a special deterministic
     case. Thus it is better to prove directly from definition. The key step is that the
     infimum over all policies π for s is the same for skip; s, because skip does not
     change valuation and the set of policies, see rule C OMPOSITION 1; so in this case
     neither the reward valuation or the policy can be chosen differently. The argument
     works in both directions.

11.3 To prove this case we observe that executing a single assignment statement (see
     A SSIGN) does not change the probability of final paths in the MDP associated with
     the program, so it does not change the expectation of the formula as long as the
     program is executed in the same valuation that the assignment creates. This argument
     works in both directions:

             ε |= [x:=e; s]p ϕ
         iff ε[x 7→ ε(e)] |= [skip; s]p ϕ (A SSIGN does not change probability of paths)
         iff ε[x 7→ ε(e)] |= [s]p ϕ                                                  (Thm. 11.2)


                                                                                                    t
                                                                                                    u

 Proof (Theorem 12).

12.1 Let’s write i for the program i = if e { s1 } else { s2 } . We want to show that
     p(ε) ≤ Ehε,ii [[ϕ]] where the expectation is taken in the MDP Mi . To do this we


                                                 26
       will reduce the calculation of the expectation to the MDPs Ms1 and Ms2 with the
       prefix for resolving the condition:

       p(ε)
       ≤ Ehε,s1 i [[ϕ]]                                          (in Ms1 , assumption and Def. 2 twice)
       = inf Ehε,s1 i [[ϕ]]                                                               (in Ms1 , Eq. (3))
          π
                  X
       = inf                      Pr(σ) · [[ϕ]](final(σ))               (Eq. (3), path prob. taken under π)
           π
               σ∈paths(hε,s1 i)
                                                           
                          X
       = inf 1 ·                 Pr(σ) · [[ϕ]](final(σ))                              (trivial, also below)
           π
                   σ∈paths(hε,s1 i)
                                                                                                          
                        X                                              X
       = inf 1 ·                     Pr(σ) · [[ϕ]](final(σ)) + 0 ·                Pr(σ) · [[ϕ]](final(σ))
           π
                   σ∈paths(hε,s1 i)                             σ∈paths(hε,s2 i)
                     X
       = inf                    Pr(σ) · [[ϕ]](final(σ))               (I F 1, assumption that ε |= e, Def. 2)
           π
               σ∈paths(hε,ii)

       = Ehε,ii [[ϕ]]                                                                               (in Mi )

       Notice the shift of the MDP in the penultimate line to Mi in the sum index. A
       line above, the assumption that the atomic formula e holds allows us to extend the
       expectation by the suitable choice of the if-branch. Since the if condition evaluates
       to true, the rule IF 1 creates an MDP prefix advancing with probability one to state
       hε, s1 i and with probability zero to the other state (we assume the same evaluation
       semantics for ATFin the logic and for expressions in pGCL). Afterwards we just observe
       that this is the same as calculating expected values directly from the if head.
12.2 The proof is symmetric to the previous case, just with the other I F rule.
12.3 This simple rule follows directly from operational semantics rules W HILE -1 and
     W HILE -2:
                               p ≤ Ehε,i1 i [[ϕ]] = Ehε,i2 i [[ϕ]]               (12)
       where i1 = if e { s; while e { s }} else {skip} and i2 = while e { s } . The equality
       of expectations holds because the two MDPs are identical—represent the same tree
       of terminating expectations over the same states, with the same branching structure,
       and final states. (Recall we only reason about almost surely terminating programs.)
       The I F -1 rule on the first program has exactly the same effect (and successors) as
       W HILE -1 rule on the second program. Similarly both I F -2 on the first and W HILE -2
       on the second program reduce to skip with the same valuation.
                                                                                            t
                                                                                            u

 A.4     Proofs for Sect. 8
 Proof (Theorem 14). Let s be a pGCL program, ε stand for a valuation, p ∈ State →
 [0, 1] be an expectation function, π a policy resolving non-determinism in s, and ϕi ∈ pDL


                                                       27
properties. The expected reward p after s for [[ϕ1 ∨ ϕ2 ]] under the scheduler π is a lower-
bound for the sum of the separate expectations of ϕ1 and ϕ2 , formally:

                p = Ehε,si,π [[ϕ1 ∨ ϕ2 ]] ≤ Ehε,si,π [[ϕ1 ]] + Ehε,si,π [[ϕ2 ]] .      (13)

This is because in the rightmost sum, some of the states can be counted twice: once for
ϕ1 and once for ϕ2 .
     Note that, if s is purely probabilistic (does not use the demonic choice operator) then
the above can be written equivalently as follows: If ε |= [s]p (ϕ1 ∨ ϕ2 ) then there exist
p1 , p2 such that ε |= [s]p1 ϕ1 and ε |= [s]p2 ϕ2 and p1 + p2 ≥ p everywhere.              t
                                                                                           u




                                               28
