                                                             Towards a Proof System for
                                                             Probabilistic Dynamic Logic

                                              Einar Broch Johnsen1 , Eduard Kamburjan1 , Raul Pardo2                      ,
                                                         Erik Voogd1 , and Andrzej Wąsowski2
                                                   1
                                                       Department of Informatics, University of Oslo, Oslo, Norway
arXiv:2412.00906v1 [cs.LO] 1 Dec 2024




                                                                 {einarj,eduard,erikvoogd}@ifi.uio.no
                                                        2
                                                            IT University of Copenhagen, Copenhagen, Denmark
                                                                        {raup,wasowski}@itu.dk




                                              Abstract. Whereas the semantics of probabilistic languages has been
                                              extensively studied, specification languages for their properties have
                                              received less attention—with the notable exception of recent and on-
                                              going efforts by Joost-Pieter Katoen and collaborators. In this paper, we
                                              revisit probabilistic dynamic logic (pDL), a specification logic for programs
                                              in the probabilistic guarded command language (pGCL) of McIver and
                                              Morgan. Building on dynamic logic, pDL can express both first-order state
                                              properties and probabilistic reachability properties. In this paper, we
                                              report on work in progress towards a deductive proof system for pDL. This
                                              proof system, in line with verification systems for dynamic logic such as
                                              KeY, is based on forward reasoning by means of symbolic execution.


                                        Keywords: Deductive verification · Probabilistic programs · Dynamic logic


                                        1   Introduction

                                        Joost-Pieter Katoen has pioneered techniques for the verification of probabilistic
                                        systems, including numerous contributions on model-checking algorithms (e.g.,
                                        [2, 4, 16]), including tools such as the probabilistic model checker Storm [10, 14],
                                        as well as proof systems for deductive verification (e.g., [5–7, 11, 19, 22, 28]).
                                        Whereas this line of work is rooted in Hoare logics and weakest precondition
                                        calculi, we here consider a specification language for probabilistic systems based
                                        on dynamic logic [13]: probabilistic dynamic logic (pDL for short) [25]. We believe
                                        it is interesting to study specification languages and deductive verification based
                                        on dynamic logic because dynamic logic is strictly more expressive than Hoare
                                        logic and weakest precondition calculi; in fact, both can be embedded in dynamic
                                        logic [12]. In contrast to these calculi, dynamic logics are closed under logical
                                        operators such as first-order connectives and quantifiers; for example, program
                                        equivalence, relative to state formulae φ and ψ, can be expressed by the dynamic
                                        logic formula φ → [s1 ]ψ ⇐⇒ φ → [s2 ]ψ. Consequently, specification languages
                                        based on dynamic logic, including pDL, have classical model-theoretic semantics
                                        known from logics: a satisfaction semantics.
2       E. B. Johnsen et al.


                 1   prize := 0 ⊓ (prize := 1 ⊓ prize := 2);
                 2   choice := 0 1/3 ⊕ (choice:=1 1/2 ⊕ choice:=2);
                 3   if (prize = choice)
                 4      open := (prize+1)%3 ⊓ open := (prize+2)%3;
                 5   else
                 6      open := (2*prize-choice)%3;
                 7   if (switch)
                 8      choice := (2*choice-open)%3
                 9   else
                10      skip


               Fig. 1. The Monty Hall Program in pGCL (Monty_Hall).



    This paper revisits pDL and its model-theoretic semantics, and its main con-
tribution is a deductive verification system for pDL based on forward reasoning
about pDL judgments, in contrast to the backwards reasoning used in weakest-
precondition-based approaches. To this aim, we sketch a proof system for pDL
based on symbolic execution rules that collect constraints about probabilities, and
a prototype implementation of this proof system using Crowbar [17], a modular
symbolic execution engine, and the SMT solver Z3 [23] to solve probabilistic
constraints.


2    Motivating Example

As an example of a probabilistic program in pGCL, consider the Monty Hall game,
in which a host presents three doors to a player. The first door contains a prize
and the other doors are empty. The player needs to decide (or guess) the door
behind which the prize is hidden. The game proceeds as follows. First, the location
of the prize is non-deterministically selected by the host. Then, the player selects
a door. The host opens an empty door that was not selected by the player, who
is asked whether she would like to switch doors. We determine, using pDL, what
option increases the chances of winning the prize (switching or not).
    Figure 1 shows a pGCL program, Monty_Hall, modeling the behavior of host and
player. The program contains four variables: prize (the door hiding the prize),
choice (the door selected by the player), open (the door opened by the host),
switch (a Boolean indicating whether the user switches door in the last step).
Note that the variable switch is undefined in the program, and will encode the
strategy of the player. Line 1 models the host’s non-deterministic choice of the
door for the prize. Line 2 models the player’s choice of door (uniformly over
the three doors). Lines 3–6 model the selection of the door to open, from the
doors that were not selected by the player. Lines 7–10 model whether the player
switches door or not. For simplicity, we use a slight shortcut to compute the door
to open and to switch in Lines 6 and 8, respectively. Note that for x, y ∈ {0, 1, 2},
the expression z = (2x − y) mod 3 simply returns z ∈ {0, 1, 2} such that z ̸= x
                    Towards a Proof System for Probabilistic Dynamic Logic          3

and z =
      ̸ y. Similarly, the expressions y = (x + 1) mod 3, z = (x + 2) mod 3 in
Line 4 ensure that y ̸= x, z =
                             ̸ x and y ̸= z. This shortcut computes the doors
that the host may open when the player chose the door with the prize in Line 2.
   An example of pDL specification of the Monty Hall game is the following
formula:
                switch = true → [Monty_Hall]p (choice = prize).            (1)
This formula expresses that if the player’s strategy is to change door (i.e., the
program’s precondition is given by the state formula switch = true), then the
probability of reaching a state characterized by the postcondition choice = prize
after successfully executing Monty_Hall, is p. But what should be the value of p? We
will show in Section 6 that we can prove this specification for p = min(p0 , p1 , p2 )
where each pi is the probability for the different locations of the prize.


3     Preliminaries
We briefly introduce the programming language pGCL [21], but first we recall
Markov Decision Processes [3, 26], which we use to define the semantics of pGCL.

3.1   Markov Decision Processes
Markov decision processes are computational structures that feature both prob-
abilistic and nondeterministic choice. We start from the following definition
(e.g., [3, 26]):
Definition 1 (Markov Decision Process). A Markov Decision Process
(MDP) is a tuple M = (State, Act, P) where (i) State is a countable set of states,
(ii) Act is a countable set of actions, and (iii) P : State × Act → Dist(State) is a
partial transition probability function.
    Let σ denote the states and a the actions of an MDP. A state σ is final if no
further transitions are possible from it, i.e. (σ, a) ̸∈ dom(P) for any a. A path,
denoted σ, is a sequence of states σ1 , . . . , σn such that σn is final and there are
actions a1 , . . . , an−1 such that P(σi , ai )(σi+1 ) ≥ 0 for 1 ≤ i < n. Let final(σ)
denote the final state of a path σ. To resolve non-deterministic choice, a positional
policy π maps states to actions, so π : State → Act. Given a policy π, we define
                           ·
a transition relation →   − π ⊆ State × [0, 1] × State on states that resolves all the
demonic choices in P and write
                             pi
                          σ −→π σ ′ iff P(σ, π(σ))(σ ′ ) = pi .
                                                                               p
Similarly, the reflexive and transitive closure of the transition relation, −
                                                                            →∗π ⊆
State × [0, 1] × State, defines the probability of a path as
                                                        p1        pn
              p = Pr(σ) = 1 · p1 · · · pn   where σ1 −→π · · · −→π σn .            (2)

   Thus, a path with no transitions consists of a single state σ, and Pr(σ) = 1.
Let pathsπ (σ) denote the set of all paths with policy π from σ to final states.
4       E. B. Johnsen et al.

    An MDP may have an associated reward function r : State → [0, 1] that
assigns a real value r(σ) to any state σ ∈ State. (In this paper we assume that
rewards are zero everywhere but in the final states.) We define the expectation
of the reward starting in a state σ as the greatest lower bound on the expected
value of the reward over all policies; so the real valued function defined as
                                             X
              Eσ (r) = inf Eσ,π (r) = inf          Pr(σ) r(final(σ)) ,        (3)
                          π              π
                                             σ∈pathsπ (σ)


where Eσ,π (r) stands for the expected value of the random variable induced by
the reward function under the given policy, known as the expected reward.
    In this paper, we assume that MDPs (and the programs we derive them from)
arrive at final states with probability 1 under all policies. This means that the
logic pDL that we will be defining and interpreting over these MDPs can only talk
about properties of almost surely terminating programs, so in general it cannot
be used to reason about termination without adaptation.

3.2    pGCL: A Probabilistic Guarded Command Language
As programming language, we consider the probabilistic guarded command
language (pGCL) of McIver and Morgan [21], a core language which features both
probabilistic and non-deterministic choice. We briefly recall the syntax of pGCL
and it semantics, formulated as a probabilistic transition system.

Syntax of pGCL. Let X be a set of program variables and x ∈ X, the syntax of
pGCL is defined as follows:

      v ::= true | false | 0 | 1 | . . .
      e ::= v | x | op e | e op e
      op ::= + | − | ∗ | / | > | == | ≥
      s ::= s ⊓ s | s e ⊕ s | s; s | skip | x := e | if e {s} else {s} | while e {s}

Statements s include the non-deterministic (or demonic) choice s1 ⊓ s2 between
branches s1 and s2 , and s e ⊕ s′ for the probabilistic choice between s and s′ . A
non-deterministic program s1 ⊓ s2 will arbitrarily select a branch for execution,
whereas in a probabilistic program s e ⊕ s′ , if the expression e evaluates to a value
p ∈ [0, 1] given the current values for the program variables, then s and s′ have
probability p and 1 − p of being selected, respectively. Binary operators and the
remaining statements have the usual meaning.

Semantics of pGCL. The semantics of a pGCL program s can now be defined
as an MDP Ms . A state σ of Ms is a pair of a valuation and a program, so
σ = ⟨ε, s⟩ where the valuation ε is a mapping from all the program variables in s
to concrete values (we may omit the program from this pair, if it is unambiguous
in the context). The state ⟨ε, s⟩ represents an initial state of the program s given
                           Towards a Proof System for Probabilistic Dynamic Logic                            5


              (Assign)                        (Composition1)                     (Composition2)
                                                       p                                  p
          ε′ = ε[x 7→ ε(e)]                            →π ⟨ε′ , s⟩
                                              ⟨ε, s2 ⟩ −                                  →π ⟨ε′ , s⟩
                                                                                 ⟨ε, s1 ⟩ −
                   1                                     p                               p
                →π ⟨ε′ , skip⟩
    ⟨ε, x := e⟩ −                                         →π ⟨ε′ , s⟩
                                           ⟨ε, skip; s2 ⟩ −                               →π ⟨ε′ , s; s2 ⟩
                                                                            ⟨ε, s1 ; s2 ⟩ −

          (DemChoice)                              (If1)                              (If2)
             i ∈ {1, 2}                         ε(e) = true                        ε(e) = false
         π⟨ε, s1 ⊓ s2 ⟩ = si
                                          ⟨ε, if e {s1 } else {s2 }⟩        ⟨ε, if e {s1 } else {s2 }⟩
                       1                          1                                 1
                    →π ⟨ε′ , si ⟩
      ⟨ε, s1 ⊓ s2 ⟩ −                             −
                                                  →π ⟨ε, s1 ⟩                       −
                                                                                    →π ⟨ε, s2 ⟩

                  (ProbChoice1)                                   (While1)
                ε(e) = p 0 ≤ p ≤ 1                               ε(e) = true
                               p                                        1
              ⟨ε, s1 e ⊕ s2 ⟩ −
                              →π ⟨ε, s1 ⟩         ⟨ε, while e {s}⟩ −
                                                                   →π ⟨ε, s; while e {s}⟩

                         (ProbChoice2)                             (While2)
                       ε(e) = p 0 ≤ p ≤ 1                         ε(e) = false
                                    1−p                                      1
                  ⟨ε, s1 e ⊕ s2 ⟩ −−→π ⟨ε, s2 ⟩          ⟨ε, while e {s}⟩ −
                                                                          →π ⟨ε, skip⟩


                               Fig. 2. An MDP-semantics for pGCL.


some initial valuation ε and the state ⟨ε, skip⟩ represents a final state in which
the program has terminated with the valuation ε. For a concrete program, the
policy π is a function that determines how non-deterministic choice is resolved
for a given valuation of the program variables; i.e., π⟨ε, s1 ⊓ s2 ⟩ = si for either
i = 1 or i = 2. The rules defining the partial transition probability function for a
given policy π are shown in Figure 2.


4      PDL: Probabilistic Dynamic Logic

The probabilistic dynamic logic pDL was introduced by Pardo et al. [25] as a
specification language for probabilistic programs in pGCL. pDL builds on dynamic
logic [13], a modal logic in which logical formulae with programs in the modalities
can be used to express reachability properties. Our formulation of pDL here differs
from our previous work [25] by incorporating symbolic updates [8], a technique
for representing state change in forward symbolic execution that is well-known
from the KeY verification system [1].


4.1     Syntax of pDL

Given sets X of program variables and L of logical variables disjoint from X, let
ATF denote the well-formed atomic formulae built using constants, program and
logical variables. For every l ∈ L, let dom l denote the domain of l. Let x range
6      E. B. Johnsen et al.

over X and t over well-formed terms, which for our purposes are pGCL expressions
where also logical variables are allowed.
   The formulae φ of probabilistic dynamic logic (pDL) are defined inductively as
the smallest set generated by the following grammar.

            φ   ::= ATF | ¬φ | φ1 ∧ φ2 | ∀l · φ | [s]p φ | {U }φ
           U    ::= empty | x 7→ t

where φ ranges over pDL formulae, l ∈ L over logical variables, s is a pGCL program
with variables in X, and p : State → [0, 1] is an expectation assigning values in
[0, 1] to initial states of the program s. The logical operators →, ∨ and ∃ are
derived in terms of ¬, ∧ and ∀ as usual. As usual, state formulae are pDL formulae
without the box-modality; we denote state formulae by FOL.
     A formula can be constructed by applying symbolic updates U to formulae φ;
i.e., {U }φ is a well-formed formula. Note that formulae that include symbolic
updates are typically used in intermediate steps in a proof system based on
forward symbolic execution; symbolic updates are typically not part of user-
provided specifications. Symbolic updates are syntactic representations of term
substitutions for program variables, which keep track of symbolic state changes
within a proof branch. The empty update empty denotes no change, the update
x 7→ t denotes a state change (or substitution [1]) where the program variable
x has the value of t. The update application {U }φ applies the update U to φ.


4.2   Semantics of pDL

We extend valuations to also map logical variables l ∈ L to values in dom l and let
ε |=ATF φ denote standard satisfaction, expressing that φ ∈ ATF holds in valuation
ε. From now on, we equate valuations and states, writing, for instance, ε ∈ State.
Though states consist not only of valuations, but also of program locations, the
locations are not relevant for interpreting pDL formulae.
    First, we define the semantics of updates as a function from program state to
program state. Let ε(t) be the evaluation of a term t in a state ε. The updated
states JU K(ε) for a given substitution U and state ε are given by

                              JemptyK(ε) = ε
                              Jx 7→ tK(ε) = ε[x 7→ ε(t)]

We define satisfiability of well-formed formulae in pDL as follows:

Definition 2 (Satisfiability of pDL Formulae). Let φ be a well-formed pDL
formula, π range over policies, l ∈ L, p : State → [0, 1] be an expectation
lower bound, and ε be a valuation defined for all variables mentioned in φ. The
satisfiability of a formula φ in a model ε, denoted ε |= φ, is defined inductively
                       Towards a Proof System for Probabilistic Dynamic Logic              7

  as follows:

      ε |= φ            iff   φ ∈ ATF   and    ε |=ATF φ
      ε |= φ1 ∧ φ2      iff   ε |= φ1   and   ε |= φ2
      ε |= ¬φ           iff   not ε |= φ
      ε |= ∀l · φ       iff   ε |= φ[l := v] for each v ∈ dom l
      ε |= {U }φ        iff   JU K(ε) |= φ
      ε |= [s]p φ       iff   p(ε) ≤ Eε [[φ]] where the expectation is taken in Ms

  For φ ∈ ATF, |=ATF can be used to check satisfaction just against the valuation of
  program variables since φ is well-formed. In the case of universal quantification,
  the substitution replaces logical variables with constants. The last case (p-box) is
  implicitly recursive, since the characteristic function [[φ]] refers to the satisfaction
  of φ in the final states of s. We use the characteristic function [[φ]] as the reward
  function on the final state of Ms . In other words, the satisfaction of a p-box
  formula [s]p φ captures a lower bound on the probability of φ holding after
  the program s. Consequently, pDL supports specification and reasoning about
  probabilistic reachability properties in almost surely terminating programs. We
  use |= [s]p φ to denote that a formula is valid, i.e., ε |= [s]p φ for all valuations ε.
  Proposition 1 (Properties of pDL [25]).             Let s, s1 , s2 be pGCL programs, φ a
  pDL formula, and ε a valuation.
    (i) (termination) ε |= [skip]1 φ if and only if ε |= φ;
   (ii) (inaction) ε |= [s]p φ if and only if ε |= [skip; s]p φ;
  (iii) (assign) ε |= [x := e; s]p φ if and only if ε[x 7→ ε(e)] |= [s]p φ;
  (iv) (universal lower bound) ε |= [s]0 φ;
   (v) (quantitative weakening) if ε |= [s]p φ and p′ ≤ p then ε |= [s]p′ φ;
  (vi) (demonic choice) ε |= [s1 ]p φ and ε |= [s2 ]p φ if and only if ε |= [s1 ⊓ s2 ]p φ;
 (vii) (probabilistic choice) if ε |= [s1 ]p1 φ and ε |= [s2 ]p2 φ then ε |= [s1 e ⊕ s2 ]p φ,
        where p = ε(e)p1 + (1 − ε(e))p2 ;
(viii) (if true) if ε |= e ∧ [s1 ]p φ then ε |= [if (e) {s1 } else {s2 }]p φ;
  (ix) (if false) if ε |= ¬e ∧ [s2 ]p φ then ε |= [if (e) {s1 } else {s2 }]p φ; and
   (x) (loop unfold) ε |= [if (e) {s; while (e) {s}} else {skip}]p φ if and only if
        ε |= [while (e) {s}]p φ.
  Note that in the above, arithmetic operations are lifted point-wise when applied
  to expectation lower bounds (functions p, p’).


  5    A Proof System for pDL
  Judgments. Let Γ be a set of formulae and V     φ a singular formula. We write a
  judgment    Γ    ⊢ φ  to state that the formula   Γ → φ is valid, i.e., that ε |=
    Γ → φ for every ε. When defining rules, we denote with U a nested sequence of
  V
  update applications of any depth, for example the schematic formula Uφ matches
  {U1 }{U2 } . . . {Un }φ for some natural n and updates U1 , . . . , Un .
8       E. B. Johnsen et al.

Probabilistic constraints. Our proof system is going to work with constraints on
probabilities. Let Φ be a set of pDL-formulae, U a symbolic update and eq an
(in)equality over probability variables. A pDL-constraint ⟨eq⟩Φ
                                                              U expresses that U(eq)
must hold in any state represented by the symbolic update U such that U(Φ).
In the sequel, we introduce the simplifying assumption that that probabilistic
expressions in pDL do not depend on state variables, in which case we can simplify
constraints to simple (in)equalities, e.g., p ≤ 1.

A probabilistic dynamic logic calculus for pGCL. We now introduce the inference
rules for dynamic logic formulae of the form Γ ⇒ U[s]p φ, expressing that if Γ
holds in the initial state of some program execution, the probability of reaching
a state in which φ holds from a state described by the symbolic update U by
executing s, is at least p (as before applied to the initial state). Thus, if the
symbolic update U is empty, we are in the initial state and s is the entire program
to be analyzed. The application of the inference rules creates a proof tree in
which pDL-constraints are generated as side conditions to rule applications. In the
end, the proof-tree can be closed if its pDL-constraints are satisfiable.
    Figure 3 shows the inference rules for pGCL—we omit inference rules for FOL
connectives as they are standard, see [8] for details. The rules in Figure 3 are
the syntax-driven, aiming to eliminate the weakening rule. Instead weakening
is implicitly applied in the rules that add a pDL-constraint. Let us first consider
the rule for skip, to explain the rule format. The rules symbolically execute the
first statement of the box-modality, generating a premise that must hold for the
symbolic execution of the remaining program s. Note that skip does not add any
probabilistic constraint. In the rules empty1 and empty0, the empty program is
denoted by a skip-statement without a continuation s. In these rules, our aim
is to check that the postcondition φ holds in the current state, represented by
the symbolic update U with a given probability p. If p ≤ 0, we leave the proof
tree open in rule empty0. If p ≥ 1, we close the tree if the formula holds in rule
empty1.
    Branching is expressed through probabilistic and demonic choice. Rule demon-
Choice captures the demonic choice by taking the worst case of the two branches,
where p1 and p2 capture the probability of the postcondition φ holding for each
of the branches. The pDL-constraint ⟨p ≤ min(p1 , p2 )⟩ captures this worst-case
assumption. Rule probChoice similarly captures the probabilistic choice, here the
pDL-constrain combines the probability f selecting a branch with the probability
of reaching the postcondition in that branch. Conditional branching over an
if-statement is captured by the rule if, which is standard and simply adds the
condition for selecting each branch in the state captured by the symbolic update
U to the precondition of each premise.
    Loops are captured by rule loopUnroll which simply unfolds a while-
statement into a conditional statement.
    Asserting Γ ⊢ φ expresses existence of a proof tree with root Γ ⊢ φ whose
set of side conditions is satisfiable.
                                                                     V
Theorem 1 (Soundness). For all Γ and φ, if Γ ⊢ φ then |= ( Γ ) → φ.
                       Towards a Proof System for Probabilistic Dynamic Logic                   9

Proof. By induction on the height of the proof tree that justifies the judgment
Γ ⊢ φ, with an analysis of the rule that justifies the root of the proof tree. All rules
except if are of the form where the premise is Γ ⊢ φ1 and the conclusion is Γ ⊢ φ2 .
In such cases, it suffices to prove that if φ1 holds then φ2 holds. Throughout the
proof, we use U = {U1 }{U2 } . . . {Un } for some n and symbolic updates U1 , . . . , Un .
Then, using Definition 2, ε |= Uφ if and only if (JUn K ◦ JUn−1 K ◦ · · · ◦ JU1 K)(ε) |= φ.
We will write ρU for the state transformation JUn K ◦ JUn−1 K ◦ · · · ◦ JU1 K

 – For rule empty1 ε |= U(φ) iff ρU (ε) |= φ iff ρU (ε) |= [skip]1 φ iff ε |= U[skip]1 φ.
   Here, we use Prop. 1(i).
 – For rule skip, ε |= U[s]p φ iff ρU (ε) |= [s]p φ iff ρU (ε) |= [skip; s]p φ iff ε |=
   U[skip; s]p φ. Here, we use Prop. 1(ii).
 – For rule assign, ε |= U{x 7→ e}[s]p φ iff ρU (ε) |= {x 7→ e}[s]p φ. Now write
   ε′ := ρU (ε). Then ε′ |= {x 7→ e}[s]p φ iff ε′ [x 7→ ε′ (e)] |= [s]p φ iff ε′ |= [x :=
   e; s]p φ, using Prop. 1(iii).
 – For rule empty0, p = 0 is a universal lower bound for any formula: ρU (ε) |=
   [skip]0 φ, by Prop. 1 (universal lower bound).
 – For rule demonChoice, let ε′ be arbitrary. By assumption, ε′ |= U[s1 ; s]p1 φ
   and ε′ |= U[s2 ; s]p2 φ. That is, with ε := ρU (ε′ ), ε |= [s1 ; s]p1 φ and ε |=
   [s2 ; s]p2 . Put p := min(p1 , p2 ). By Prop. 1(vi), ε |= [s1 ; s ⊓ s2 ; s]p φ, meaning
   p ≤ Eε [[φ]], taken in Ms′ where s′ = s1 ; s ⊓ s2 ; s. Analyzing the rules in Fig-
   ure 2 and using the definition of expectation, this means that both p ≤ Eε [[φ]]
   taken in Ms1 ;s and p ≤ Eε [[φ]] taken in Ms2 ;s . Now assume for contradiction
   that p > Eε [[φ]] taken in M(s1 ⊓s2 );s . Then there is a policy π such that
   p > Eε,π [[φ]] in M(s1 ⊓s2 );s . Using Rules DemChoice and Composition2,
   then, depending on the policy but without loss of generality, p > Eε,π [[φ]]
   also in Ms1 ;s . But this contradicts what we claimed before, that p ≤ Eε [[φ]]
   in Ms1 ;s . Conclude that ε |= [(s1 ⊓ s2 ); s]p φ and so ε′ |= U[(s1 ⊓ s2 ); s]p φ.
   By Prop. 1(v), this is true for any p ≤ min(p1 , p2 ), so we are done.
 – For rule probChoice, let ε′ be arbitrary. By assumption, ε′ |= U[s1 ; s]p1 φ and
   ε′ |= U[s2 ; s]p2 φ, meaning ε |= [s1 ; s]p1 φ and ε |= [s2 ; s]p2 φ with ε = ρU (ε′ ).
   With p := e · p1 + (1 − e) · p2 , by Prop. 1(vii), ε |= [s1 ; s e ⊕ s2 ; s]p φ.
   This means that p ≤ Eε [[φ]] in the MDP of s1 ; s e ⊕ s2 ; s, and analyzing
   Rules ProbChoice1, ProbChoice2, and Composition2, we know that

                 Eε [[φ]]        = ε(e) · Eε [[φ]] +(1 − ε(e)) · Eε [[φ]] =      Eε [[φ]]
                 | {z }                   | {z }                 | {z }          | {z }
              in s1 ;s e⊕s2 ;s            in s1 ;s               in s2 ;s     in (s1 e⊕s2 );s


   we conclude that also ε |= [(s1 e⊕ s2 ); s]p φ, and hence, ε′ |= U[(s1 e⊕ s2 ); s]p φ.
   The argument is generalizable to any p ≤ e · p1 + (1 − e) · p2 (Prop. 1(v)), so
   we are done.
 – For rule if, let ε′ be arbitrary and assume the premises of the rule hold.
   If ε′ ̸|= Γ there is nothing to prove. Otherwise, w.l.o.g., ε′ |= U(e) and
   therefore ε′ |= U[s1 ; s]p φ. Hence, writing ε = ρU (ε), we have ε |= e ∧
   [s1 ; s]p φ. By Prop. 1(viii), then, ε |= [if (e){s1 ; s} else {s2 ; s}]p φ. This means
   that p ≤ Eε [[φ]] in the MDP of if (e){s1 ; s} else {s2 ; s}. Using Rules If1
10       E. B. Johnsen et al.

                                       (demonChoice)
           (skip)                     Γ ⊢ U [s1 ; s ]p1 φ
       Γ ⊢ U [s]p φ                   Γ ⊢ U [s2 ; s]p2 φ
                                                              ⟨p ≤ min(p1 , p2 )⟩
     Γ ⊢ U[skip; s]p φ             Γ ⊢ U [(s1 ⊓ s2 ); s]p φ

                                        (probChoice)
           (assign)                  Γ ⊢ U[s1 ; s]p1 φ
     Γ ⊢ U{x 7→ e}[s]p φ             Γ ⊢ U[s2 ; s]p2 φ
                                                              ⟨p ≤ e · p1 + (1 − e) · p2 ⟩
     Γ ⊢ U [x := e; s]p φ          Γ ⊢ U [s1 e ⊕ s2 ; s]p φ

                                                    (if)
        (empty1)                          Γ, U(e) ⊢ U [s1 ; s]p φ
       Γ ⊢ U (φ)          .              Γ, ¬U(e) ⊢ U [s2 ; s]p φ
                       ⟨p = 1⟩
     Γ ⊢ U[skip]p φ                Γ ⊢ U [if (e){s1 } else {s2 }; s]p φ

        (empty0)                                       (loopUnroll)
                          .        Γ ⊢ U [if (e) {sb ; while (e) {sb }; s} else s}]p φ
                       ⟨p = 0⟩
     Γ ⊢ U[skip]p φ                           Γ ⊢ U [while (e) {sb }; s]p φ

                             Fig. 3. Symbolic execution rules.



   and Composition2 and the fact that ε |= e, also p ≤ Eε [[φ]] for s1 ; s. Then,
   using Rule If1 and ε |= e again, p ≤ Eε [[φ]] in (if (e){s1 } else {s2 }); s, so that
   ε |= [(if (e){s1 } else {s2 }); s]p φ, and so ε′ |= U[(if (e){s1 } else {s2 }); s]p φ.
 – Finally, for rule loopUnroll, let ε′ be arbitrary and let ε = ρU (ε′ ). There
   are two cases to consider:
       • If ε |= e (meaning ε(e) = true) then: ε |= [while (e) {sb }; s]p φ iff ε |=
         [sb ; while (e) {sb }; s]p φ (using Rules While1 and Composition2 and
         definition of expectation) iff ε |= [if (e) {sb ; while (e) {sb }; s} else s]p φ
         (using Rules If1 and Composition2).
       • Otherwise, if ε ̸|= e, similar reasoning with Rules While2, If2, and Com-
         position1 show that ε |= [while (e) {sb }; s]p φ if and only if ε |=
         [if (e) {sb ; while (e) {sb }; s} else s]p φ
     In either case, we have shown that ε′ |= U[while (e) {sb }; s]p φ if and only if
     ε′ |= U[if (e) {sb ; while (e) {sb }; s} else s]p φ



Example. We illustrate the use of the inference rules in Fig. 3 by considering
one of the branches of the proof tree for property Eq. (1) of the Monty Hall
game (Sect. 2). In Sect. 6, we use our prototype implementation to automatically
generate the complete proof. The property we are interested in proving is as
follows (the code for Monty_Hall is in Fig. 1):

                      switch = true ⊢ [Monty_Hall]p (choice = prize)
                    Towards a Proof System for Probabilistic Dynamic Logic           11

First, we apply the rule for non-deterministic choice. For convenience, we use
φ ≜ (choice = prize).


             switch = true ⊢ [prize:=0; ...]p0 φ
             switch = true ⊢ [prize:=1; ...]p1 φ
             switch = true ⊢ [prize:=2; ...]p2 φ
                                                    p ≤ min(p0 , p1 , p2 )
               switch = true ⊢ [Monty_Hall]p φ

The rule adds 3 different premises, one for each path of the non-deterministic
choice. In what follows, we focus on the proof branch for p0 . The next program
statement is an assignment, thus we apply the rule Assign.


 switch = true ⊢ {prize 7→ 0}[choice:=0 1/3 ⊕ (choice:=1 1/2 ⊕ choice:=2);...]p0 φ
                        switch = true ⊢ [prize:=0; ...]p0 φ

This rule simply added the update {prize 7→ 0}. In the following, we use Γ and
U to denote, at a point in the proof tree, the set of formulae in the precedent
of a judgment and the set of updates, respectively. Next we apply the rule to
resolve the probabilistic choice:


              Γ ⊢ U[choice:=0; ...]p00 φ
        Γ ⊢ U[(choice:=1 1/2 ⊕ choice:=2);...]p01 φ
                                                              p0 ≤ 1/3p00 + 2/3p01
 Γ ⊢ U[choice:=0 1/3 ⊕ (choice:=1 1/2 ⊕ choice:=2);...]p0 φ
We continue the example with the proof tree for the p00 premise. We apply Assign
so that we add the assignment as a symbolic update U = {prize 7→ 0, choice 7→ 0}.
Then, we apply the rule for if-statements:


             0=0                                      0̸=0
      z      }|       {                       z       }|        {
   Γ, U(prize = choice) ⊢ [s0 ;...]p00 φ   Γ, ¬ U(prize = choice) ⊢ [s1 ;...]p00 φ
                Γ ⊢ [if (prize = choice) {s0 } else {s1 };...]p00 φ

The branch for the right premise above can be closed as we have derived false
(0 ̸= 0). For the left premise, we apply the rule for resolving the non-deterministic
choice [open := (prize+1)%3 ⊓ open := (prize+1)%3; ...]p00 . This step generates a
new constraint p00 ≤ min(p000 , p001 ). We continue discussing the left branch
(open := (prize+1)%3). In this case, we include a new update {open 7→ 1}, as
U((prize + 1)%3) = (0 + 1)%3 = 1. Since we have switch = true, for the
final if-statement (if (switch) choice := (2*choice - open)%3 else skip), the right
premise (¬ U(e)) of If can be trivially closed, and the left premise produces a
final assignment {choice 7→ 2}—as U((2choice − open)%3) = (2 · 0 − 1)%3 = 2.
All in all, we get Γ ⊢ {prize 7→ 0, open 7→ 1, choice 7→ 2}(prize = choice). Since,
12         E. B. Johnsen et al.

given this update, the property does not hold, we close the branch by applying
Empty0, i.e., p000 = 0.
    In summary, this proof branch has produced the following set of constraints:
p ≤ min(p0 , p1 , p2 ), p0 ≤ 1/3p00 + 2/3p01 , p00 ≤ min(p000 , p001 ) and p000 = 0.
Similar reasoning can be applied in the remaining branches, which will produce
additional sets of constraints. In Sect. 6, we use Crowbar to automatically generate
the complete proof and constraints. Furthermore, Crowbar outsources the set
of constraints to an SMT solver to determine whether there are values for the
different pi that satisfy all constraints.

Discussion. The above proof system exploits the results of our earlier work [25]
to build an automated deduction system. In this system, we have placed a
rather simple instrument for reasoning about loops. We recall that a classic,
non-probabilistic loop-invariant rule for partial correctness has the following
structure (cast in a dynamic logic flavor [1]):

                                          (loopInvariant)
                Γ ⊢U I     Γ, U ′ (¬e ∧ I) ⊢ U ′ [s] φ    Γ, U ′ (e ∧ I) ⊢ U ′ [sb ] I)
                                  Γ ⊢ U[while (e) {sb }; s] φ
where U denotes some symbolic update such that the invariant holds (thus
            ′

abstracting from the number of iterations of the loop). Using our syntax (and
exploiting the probability lower bound of one to encode a qualitative box formula),
this rule corresponds to:
                                            (loopQual)
                Γ ⊢U I    Γ, U ′ (¬e ∧ I) ⊢ U ′ [s]1 φ    Γ, U ′ (e ∧ I) ⊢ U ′ [sb ]1 I)
                                  Γ ⊢ U[while (e) {sb }; s]1 φ
The key aspect is to invent both an invariant and the substitution at termination,
which (roughly) correspond to proposing a loop invariant in Hoare logics. This
rule generalizes in a straightforward way to the case when the loop body itself
is non-probabilistic. Then, it suffices to show that the expectation of the loop
successor s is preserved by the loop, obtaining:
                                         (loopPreserving)
                Γ ⊢U I    Γ, U ′ (¬e ∧ I) ⊢ U ′ [s]p φ    Γ, U ′ (e ∧ I) ⊢ U ′ [sb ]1 I)
                                  Γ ⊢ U[while (e) {sb }; s]p φ
In general, weakest-precondition style rules can be encoded, and as our next step,
we intend to experiment with existing rules from that space in actual proofs [18].

6      Implementation
We have implemented the above proof procedure3 in Crowbar [17], a modular
symbolic execution engine which uses the SMT-solver Z3 [23] under the hood to
3
     The sources for our prototype are available at https://github.com/Edkamb/crowbar-tool/tree/PDL.
                       Towards a Proof System for Probabilistic Dynamic Logic   13


 1   [Spec: Ensures(choice == prize)]
 2   [Spec: Prob(2/3)]
 3   {
 4   Int prize = -1; Int choice = -1; Int open = -1;
 5   Int sw = 1;
 6
 7   [Spec: Demonic]
 8 if( True ) { prize = 0; }
 9 else { [Spec: Demonic] if( True ) { prize = 1; }
10                        else { prize = 2; } }
11
12   [Spec: Prob(1/3)]
13 if( True ) { choice = 0; }
14 else { [Spec: Prob(1/2)] if( True ) { choice = 1; }
15                          else { choice = 2; } }
16
17   if(prize==choice){
18       [Spec: Demonic] if( True ) { open = (prize + 1 ) % 3; }
19                        else { open = (prize + 2) % 3; }}
20   else {open = ((2 * prize) - choice) % 3;}
21
22   if(sw==1){choice = ((2 * choice) - open) % 3;} else { skip; }
23   }



            Fig. 4. The Monty Hall game in the ABS encoding for Crowbar.



solve arithmetic constraints: Crowbar performs the symbolic execution and uses
Z3 to discharge formulas without modalities. Crowbar was originally developed to
experiment with deductive proof systems for the active object modeling language
ABS [15]. For rapid prototyping, we have therefore used the Crowbar front-end
for ABS and encoded pGCL into the main block of ABS programs; we use the
general annotation format [27] for ABS programs to capture probabilistic aspects
of pDL as annotations of ABS programs. The probabilistic constraints accumulated
during the symbolic execution of the pGCL program are then passed to Z3 if the
proof can otherwise be closed.
    The main block itself is annotated with two specification elements: first the
annotation [Spec: Ensures(e)] captures the post-condition and the annotation
[Spec: Prob(e)] captures its probability. Furthermore, we use annotations of
statements to encode probabilistic and demonic choice-operators of pGCL using an
ABS branching statement. Demonic choice is expressed with a [Spec: Demonic]
annotation on the branching statement, whose guard is then ignored. Probabilistic
choice is similarly expressed with a [Spec: Prob(e)] annotation.
   To illustrate the encoding of pGCL and pDL into the ABS representation of
Crowbar, Figure 4 shows the encoding of the Monty Hall game introduced in
Section 2. If sw is set to 1, denoting that the player always switches, the proof
14      E. B. Johnsen et al.

obligation can be discharged, as expected. If sw is set to 0, denoting that the
player never switches, the proof attempt fails.


7    Related and Future Work
The symbolic execution proof system for probabilistic dynamic logic presented
in this paper formulated in the style of KeY [1], and its symbolic execution
proof system for sequential Java. We specifically use their technique for symbolic
updates [8] in the formulation of our symbolic execution proof system. In contrast
to their work, our deductive verification system addresses probabilistic programs
by accumulating probabilistic constraints, which are then resolved using Z3.
    Voogd et al. [29] developed a symbolic execution framework for probabilistic
programs, building on Kozen’s work on the semantics of probabilistic programs
with random variables [20]. However, this work, inspired by de Boer and Bon-
sangue’s work on formalized symbolic execution [9], does not extend into a
deductive proof system as discussed in this paper. It further focuses on proba-
bilistic programs with random variables rather than probabilistic and demonic
choice as introduced in pGCL. In future work, we aim to integrate ideas from this
paper into our reasoning framework; in particular, it would be interesting to
add support for observe-statements. We refer to Voogd et al. [29] for a detailed
discussion of how different semantics for probabilistic programs relate to symbolic
execution.
    Katoen et al. [28] developed a generic deductive proof system for probabilistic
programs. Their work uses an encoding into a dedicated verification engine
for probabilistic reasoning, called Caesar. In line with systems like Viper [24],
they develop a intermediate representation language. To address probabilistic
reasoning, their intermediate language is probabilistic and generates verification
conditions for an SMT solver. Our work uses Crowbar, which is also a modular
verification system. However, Caesar is tailored for weakest-precondition-style
backwards reasoning, while our work targets forward reasoning by means of
symbolic execution.
    Our investigation shows that invariant based reasoning for loops is surprisingly
subtle for probabilistic programs. Here, Joost-Pieter Katoen and his collaborators
have again led the way (e.g., [22]). We hope some of his work on probabilistic loops
can carry over to backwards reasoning in a weakest pre-expectation framework
to forward reasoning in a symbolic execution setting, but it is an open question
today—an open question that we aim to understand—exactly how forward and
backwards reasoning about probabilistic loops relate.


8    Conclusion
This paper reports on work in progress towards a proof system for pDL, a prob-
abilistic dynamic logic for specifying properties about probabilistic programs.
A nice feature of pDL is that it is closed under logical operators such as first-
order connectives and quantifiers, and that it has a model-theoretic semantics
                     Towards a Proof System for Probabilistic Dynamic Logic              15

in terms of a satisfiability-relation. Our approach to a proof system for pDL uses
forward reasoning by combining symbolic execution with a constraint solver.
We have outlined a proof system for deductive verification based on symbolic
execution which collects constraints about probabilities as side conditions. These
are then forwarded to the constraint solver. For our prototype implementation,
we have used Crowbar, a modular deductive verification engine based on symbolic
execution, and the SMT-solver Z3 to solve constraints on probabilities.
    We would like to end this paper by thanking Joost-Pieter Katoen not only
for all his outstanding work on deductive verification of probabilistic programs,
but also for interesting discussions on the relationship between backwards and
forwards reasoning in this setting. A next step for us will be to understand if
(and hopefully, how) some of the work conducted by Katoen and colleagues on
reasoning about loops can adapted to a forward-reasoning framework.
Acknowledgments. This work was partly funded by the EU project SM4RTENANCE
(grant no. 101123423). We are grateful to Asmae Heydari Tabar for discussions
on symbolic execution and Crowbar.

References
 1. Ahrendt, W., Beckert, B., Bubel, R., Hähnle, R., Schmitt, P.H., Ulbrich, M. (eds.):
    Deductive Software Verification - The KeY Book - From Theory to Practice,
    Lecture Notes in Computer Science, vol. 10001. Springer (2016), https://doi.org/10.1007/
    978-3-319-49812-6
 2. Baier, C., Haverkort, B.R., Hermanns, H., Katoen, J.-P.: Model-checking algorithms
    for continuous-time Markov chains. IEEE Trans. Software Eng. 29(6), 524–541
    (2003), https://doi.org/10.1109/TSE.2003.1205180
 3. Baier, C., Katoen, J.-P.: Principles of model checking. MIT Press (2008)
 4. Baier, C., Katoen, J.-P., Hermanns, H.: Approximate symbolic model checking of
    continuous-time Markov chains. In: Baeten, J.C.M., Mauw, S. (eds.) Proc. 10th
    International Conference on Concurrency Theory (CONCUR’99). Lecture Notes
    in Computer Science, vol. 1664, pp. 146–161. Springer (1999), https://doi.org/10.1007/
    3-540-48320-9_12
 5. Batz, K., Biskup, T.J., Katoen, J.-P., Winkler, T.: Programmatic strategy synthesis:
    Resolving nondeterminism in probabilistic programs. Proc. ACM Program. Lang.
    8(POPL), 2792–2820 (2024), https://doi.org/10.1145/3632935
 6. Batz, K., Chen, M., Junges, S., Kaminski, B.L., Katoen, J.-P., Matheja, C.: Prob-
    abilistic program verification via inductive synthesis of inductive invariants. In:
    Sankaranarayanan, S., Sharygina, N. (eds.) Proc. 29th International Conference
    on Tools and Algorithms for the Construction and Analysis of Systems (TACAS
    2023). Lecture Notes in Computer Science, vol. 13994, pp. 410–429. Springer (2023),
    https://doi.org/10.1007/978-3-031-30820-8_25
 7. Batz, K., Kaminski, B.L., Katoen, J.-P., Matheja, C.: Relatively complete verifica-
    tion of probabilistic programs: an expressive language for expectation-based reason-
    ing. Proc. ACM Program. Lang. 5(POPL), 1–30 (2021), https://doi.org/10.1145/3434320
 8. Beckert, B., Klebanov, V., Weiß, B.: Dynamic logic for Java. In: Ahrendt et al. [1],
    pp. 49–106, https://doi.org/10.1007/978-3-319-49812-6_3
 9. de Boer, F.S., Bonsangue, M.: Symbolic execution formally explained. Formal
    Aspects of Computing 33(4), 617–636 (2021), https://doi.org/10.1007/s00165-020-00527-y
16       E. B. Johnsen et al.

10. Dehnert, C., Junges, S., Katoen, J.-P., Volk, M.: A Storm is coming: A modern
    probabilistic model checker. In: Majumdar, R., Kuncak, V. (eds.) Proc. 29th
    International Conference on Computer Aided Verification (CAV 2017). Lecture
    Notes in Computer Science, vol. 10427, pp. 592–600. Springer (2017), https://doi.org/10.
    1007/978-3-319-63390-9_31
11. Feng, S., Chen, M., Su, H., Kaminski, B.L., Katoen, J.-P., Zhan, N.: Lower
    bounds for possibly divergent probabilistic programs. Proc. ACM Program. Lang.
    7(OOPSLA1), 696–726 (2023), https://doi.org/10.1145/3586051
12. Hähnle, R.: Dijkstra’s legacy on program verification. In: Apt, K.R., Hoare, T.
    (eds.) Edsger Wybe Dijkstra: His Life, Work, and Legacy, pp. 105–140. ACM /
    Morgan & Claypool (2022), https://doi.org/10.1145/3544585.3544593
13. Harel, D., Kozen, D., Tiuryn, J.: Dynamic Logic. Foundations of Computing, MIT
    Press (Oct 2000)
14. Hensel, C., Junges, S., Katoen, J.-P., Quatmann, T., Volk, M.: The probabilistic
    model checker Storm. Int. J. Softw. Tools Technol. Transf. 24(4), 589–610 (2022),
    https://doi.org/10.1007/s10009-021-00633-z
15. Johnsen, E.B., Hähnle, R., Schäfer, J., Schlatte, R., Steffen, M.: ABS: A core
    language for abstract behavioral specification. In: Aichernig, B.K., de Boer, F.S.,
    Bonsangue, M.M. (eds.) Proc. 9th International Symposium on Formal Methods
    for Components and Objects (FMCO 2010). Lecture Notes in Computer Science,
    vol. 6957, pp. 142–164. Springer (2010), https://doi.org/10.1007/978-3-642-25271-6_8
16. Junges, S., Ábrahám, E., Hensel, C., Jansen, N., Katoen, J.-P., Quatmann, T., Volk,
    M.: Parameter synthesis for Markov models: covering the parameter space. Formal
    Methods Syst. Des. 62(1), 181–259 (2024), https://doi.org/10.1007/s10703-023-00442-x
17. Kamburjan, E., Scaletta, M., Rollshausen, N.: Deductive verification of active
    objects with Crowbar. Sci. Comput. Program. 226, 102928 (2023), https://doi.org/10.
    1016/j.scico.2023.102928
18. Kaminski, B.L.: Advanced weakest precondition calculi for probabilistic programs.
    Ph.D. thesis, RWTH Aachen University, Germany (2019), http://publications.rwth-aachen.
    de/record/755408
19. Kaminski, B.L., Katoen, J.-P., Matheja, C., Olmedo, F.: Weakest precondition
    reasoning for expected runtimes of randomized algorithms. J. ACM 65(5), 30:1–
    30:68 (2018), https://doi.org/10.1145/3208102
20. Kozen, D.: Semantics of probabilistic programs. In: Proc. 20th Annual Symposium
    on Foundations of Computer Science. pp. 101–114. IEEE Computer Society (1979),
    https://doi.org/10.1109/SFCS.1979.38
21. McIver, A., Morgan, C.: Abstraction, Refinement and Proof for Probabilistic
    Systems. Monographs in Computer Science, Springer (2005), https://doi.org/10.1007/
    b138392
22. McIver, A., Morgan, C., Kaminski, B.L., Katoen, J.-P.: A new proof rule for
    almost-sure termination. Proc. ACM Program. Lang. 2(POPL), 33:1–33:28 (2018),
    https://doi.org/10.1145/3158121
23. de Moura, L., Bjørner, N.: Z3: An efficient SMT solver. In: Ramakrishnan, C.R.,
    Rehof, J. (eds.) Proc. 14th International Conference on Tools and Algorithms for the
    Construction and Analysis of Systems (TACAS 2008). Lecture Notes in Computer
    Science, vol. 4963, pp. 337–340. Springer (2008), https://doi.org/10.1007/978-3-540-78800-3_
    24
24. Müller, P., Schwerhoff, M., Summers, A.J.: Viper: A verification infrastructure
    for permission-based reasoning. In: Jobstmann, B., Leino, K.R.M. (eds.) Proc.
    17th International Conference on Verification, Model Checking, and Abstract
                      Towards a Proof System for Probabilistic Dynamic Logic               17

    Interpretation (VMCAI 2016). Lecture Notes in Computer Science, vol. 9583, pp.
    41–62. Springer (2016), https://doi.org/10.1007/978-3-662-49122-5_2
25. Pardo, R., Johnsen, E.B., Schaefer, I., Wąsowski, A.: A specification logic for
    programs in the probabilistic guarded command language. In: Proc. 19th In-
    ternational Colloquium on Theoretical Aspects of Computing (ICTAC’22). Lec-
    ture Notes in Computer Science, vol. 13572, pp. 369–387. Springer (2022),
    https://doi.org/10.1007/978-3-031-17715-6_24
26. Puterman, M.L.: Markov Decision Processes. Wiley (2005)
27. Schlatte, R., Johnsen, E.B., Kamburjan, E., Tapia Tarifa, S.L.: The ABS simulator
    toolchain. Sci. Comput. Program. 223, 102861 (2022), https://doi.org/10.1016/j.scico.2022.
    102861
28. Schröer, P., Batz, K., Kaminski, B.L., Katoen, J.-P., Matheja, C.: A deductive
    verification infrastructure for probabilistic programs. Proc. ACM Program. Lang.
    7(OOPSLA2), 2052–2082 (2023), https://doi.org/10.1145/3622870
29. Voogd, E., Johnsen, E.B., Silva, A., Susag, Z.J., Wąsowski, A.: Symbolic seman-
    tics for probabilistic programs. In: Jansen, N., Tribastone, M. (eds.) Proc. 20th
    International Conference on Quantitative Evaluation of Systems (QEST 2023).
    Lecture Notes in Computer Science, vol. 14287, pp. 329–345. Springer (2023),
    https://doi.org/10.1007/978-3-031-43835-6_23
