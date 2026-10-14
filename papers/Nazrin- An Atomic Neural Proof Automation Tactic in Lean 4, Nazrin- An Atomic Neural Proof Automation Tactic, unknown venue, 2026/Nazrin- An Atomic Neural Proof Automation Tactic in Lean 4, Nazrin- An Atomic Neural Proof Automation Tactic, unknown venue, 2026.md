                                                                                      Formal Methods in Computer-Aided Design 2021



                                         Nazrin: An Atomic Neural Proof Automation Tactic
                                                            in Lean 4
                                                     Leni Aniva                                    Iori Oikawa                          David Dill             Clark Barrett
                                         Stanford University, Stanford, U.S. Northeastern University, Massachusetts, U.S. Stanford University Stanford University
                                                 aniva@stanford.edu                 wang.fengk@northeastern.edu           dill@cs.stanford.edu barrettc@stanford.edu



                                            Abstract—In Machine-Assisted Theorem Proving, a theorem               learn heuristics from the extensive library of existing proofs,
                                         proving agent searches for a sequence of expressions and tactics         instead of hand coding them.
                                         that can prove a statement in a proof assistant. In this work,              A natural approach is to train an agent on human-written
arXiv:2602.18767v3 [cs.LO] 30 Jun 2026




                                         we introduce several novel concepts and capabilities to address
                                         obstacles faced by machine-assisted theorem proving. We first            proofs. However, this approach has several drawbacks. First of
                                         present a set of atomic tactics, a small finite set of tactics capable   all, Lean has an unbounded space of tactics that can be used
                                         of proving any provable statement in Lean. We then introduce a           to prove the same thing in many different ways, and existing
                                         transposing atomization algorithm which turns arbitrary proof            proofs use arbitrary collections of these tactics. This leads to
                                         expressions into a series of atomic tactics. We next introduce           a noisy data set, where it is unclear whether the choice of
                                         the ExprGraph data structure, which provides a succinct rep-
                                         resentation for Lean expressions. Finally, we present the Nazrin         the next tactic is because it’s the obvious right thing to do, or
                                         Prover, short for Neural Atomizer for Inhabitation Problems, a           because that’s what the author happened to prefer. We would
                                         graph neural network-based theorem proving agent using atomic            expect this to confuse or slow down training. Second, the final
                                         tactics and ExprGraph. Nazrin circumvents many challenges                version of a proof written by a human typically emphasizes
                                         faced by existing proving agents by exclusively dispatching atomic       conciseness and ease of checking, and does not provide
                                         tactics, and it is robust enough to both train and evaluate on
                                         consumer-grade hardware. We demonstrate the potential of tools           much insight about how to find a proof. Third, expressions
                                         like Nazrin using theorems from Lean’s standard library and              in Lean contain type-theoretically immaterial information to
                                         from Mathlib.                                                            the mathematical argument which could be elided without
                                                                                                                  modifying the validity of a proof.
                                                                  I. I NTRODUCTION                                   In this paper, we introduce a novel proof search approach
                                            Most modern mathematical proofs are still written in natural          which addresses these drawbacks. We have five main contri-
                                         language, a representation susceptible to ambiguity, errors, and         butions:
                                         logic gaps. A proof assistant is a computer program that                    1) Atomic Tactics: We introduce a small set of simple
                                         implements a formal proof system for foundational mathemat-                     tactics with a bounded parameter space, which can be
                                         ical reasoning. Using a proof assistant, we can write formal                    used to incrementally construct a proof expression in
                                         mathematical proofs that are precise and are guaranteed to                      Lean. This provides a small, finite action space for
                                         have no gaps or errors. Lean 4 (referred to simply as Lean                      theorem proving agents, reducing the number of choices
                                         below, for brevity) is a widely used proof assistant [15] based                 that have to be made at each step of proof search.
                                         on the Calculus of Inductive Constructions. Its Mathlib [11]                2) Transposing Atomization: We present an algorithm
                                         library is one of the largest corpora of formalized mathematics                 that can translate a proof term into a series of atomic
                                         ever built. In Lean, the type of a theorem is its statement,                    tactics. This can be used to generate a large amount of
                                         and the value of a theorem is its proof. This Curry-Howard                      training data from existing formalized mathematics. The
                                         correspondence between theorems and functions means that                        generated data trains the system how to find proofs, not
                                         the problem of finding a proof is equivalent to the problem of                  how to present them. The method of atomization could
                                         inhabitation: finding a member of a type. Proofs in Lean are                    in principle be implemented in any proof assistant.
                                         typically written manually as a series of tactics and expressions           3) ExprGraph: We design a reduced graph-based repre-
                                         that decompose and discharge proof obligations.                                 sentation of expressions in Lean that exploits the funda-
                                            Interactive theorem proving is laborious and can be te-                      mental symmetries of mathematics, while preserving a
                                         dious because the user must deal with every single detail                       necessary amount of information for search to proceed.
                                         of lengthy formal proofs. To mitigate this, modern proof                        We explicitly construct variable reference edges in the
                                         assistants incorporate a collection of automated proof methods                  ExprGraph to mimic attention mechanisms present in
                                         to do much of the work, especially low-level “obvious” proofs.                  language models.
                                         These methods include decision procedures for fragments                     4) Nazrin Prover: We introduce Nazrin, short for Neural
                                         of logic [16] [12], resolution theorem provers, hand-coded                      Atomizer for Inhabitation Problems, a low-resource
                                         heuristic search [10], or the Hammer-like Grind tactic in Lean                  graph neural network-based theorem proving agent
                                         [15]. There is a clear opportunity to apply machine learning to                 which is trained, using atomized data and reinforcement



                                               https://doi.org/                                                                           This article is licensed under a Creative
                                                                                                                                          Commons Attribution 4.0 International License
      learning, to output atomized tactics. Nazrin has similar      motivated proofs [13], where a proof is written in a way which
      aims to proof automation methods like Sledgehammer            follows the author’s trajectory of thinking rather than for easy
      [4] (in Isabelle/HOL) and Aesop [10] in Lean.                 verification and mathematical beauty. We exploit this similarity
   5) Evaluation: We evaluate Nazrin on Lean’s standard             to reduce the search space of tactic agents. We use Pantograph
      library and on its power to generalize on Mathlib. This       to interact with Lean 4 in this work, leveraging its expressive
      mimics the use case of developing a new theory in             goal management and representation system.
      Mathlib, which requires the prover agent to generalize           MiniLang [20] provides a reduced set of tactics for theorem
      on Mathlib itself.                                            proving in Isabelle for language models. This set reduces the
   The remainder of the paper is organized as follows. We           size of the action space for a theorem proving agent. However,
start with related work (II) and background (III). We then          the size of an individual tactic can still be arbitrarily large, as
introduce our atomic tactics and atomization algorithm (IV).        the choose tactic in MiniLang can provide an arbitrarily-
We next explain our graph-based representations of Lean             sized witness. In contrast, our atomic tactics always provide a
expressions and how they are used as core building blocks           finite action space.
for the Nazrin prover (V). Finally, we present our evaluation
                                                                                          III. BACKGROUND
(VI) and conclude (VII).
                                                                       We provide some background on the setting of mechanical
                     II. R ELATED W ORK                             theorem proving in Lean. Lean and Mathlib have large corpora
   Tree search, e.g., MCTS [1], is a common paradigm for            of formally proved theorems, and these theorems have been
tasks involving decisions (e.g., Board games, path planning,        extensively used in training of machine learning agents. The
theorem proving, etc). Previous work on using tree search for       primary driver of theorem proving in Lean is the proof state,
theorem proving includes [8], BFS-Prover [19], and DT-Solver        which contains an environment of already-defined functions
[17]. Hypertree Proof Search in particular pioneered the use        and lemmata, and a set of goals to prove. Dispatching a
of product rewards for determining the estimated reward for         tactic in this proof environment modifies the set of goals. The
multiple goals. It uses an And-Or tree structure to represent       mission of theorem proving is to discharge all goals in a proof
the search tree. BFS-Prover [19] uses a language model to           environment.
estimate the value of a goal. DT-Solver [17] likewise uses a           A newly discovered proof may be written in a different order
LLM but also estimates the viability of a goal by comparing it      than it was conceived. For example, in a common ϵ-δ style
against its ancestors, which uses LLMs to perform tree search.      convergence proof, one is usually not able to come up with
Alternatively, an LLM can interact with a proof assistant           a correct δ before conducting further exploration. Consider
directly via text [18]. LeanDojo and ReProver [21] involve          proving that the sum of limits â, b̂ of real functions f and g
using a language model as a reinforcement learning agent            at 0 is equal to the limit of the sum f (x) + g(x). To come
whose objective is to discharge all goals with tactics.             up with this proof, we may opt initially to leave δ empty, i.e.,
   Previous work on using graphs to represent expressions           δ := □δ . Then, we invoke the triangle inequality on |f (x) +
includes [14], in which GNNs are used to perform premise            g(x) − â − b̂| < ϵ to find that we need to prove |f (x) − â| +
selection in HOL, which is similar to Lean. Graphs can also         |g(x) − b̂| < ϵ. This backward style of reasoning is common
be used for premise selection, e.g., in [9]. Other methods          in proof assistants such as Lean 4. We apply the definition
for exploiting symmetries in mathematics include de Bruijn          of convergence to arrive at |f (x) − â| < □f when |x| <
indices [3].                                                        δf , where δf is dependent on the yet uninstantiated □f , and
   Aesop [10], which is a proof automation tool, introduced the     likewise for □g . Substituting, we find □f + □g ≤ ϵ, and
concept of metavariable coupling, which is discussed further        □δ ≤ min{δx , δy }. At this point, we can solve for all the
in Section III. Metavariable coupling refers to the mutual          uninstantiated variables using basic arithmetic. A prover agent
interference between goals in a proof, which complicates proof      following a similar proof trajectory does not have to conjure
search.                                                             complicated witnesses at the beginning and can instead rely
   More generally, a variety of hammers have been developed         on incremental construction, finding witnesses at the end or
for interactive theorem provers. These are generally based on       along the way.
automated reasoning (rather than machine learning) techniques
and include Isabelle’s Sledgehammer [4], SMTCoq [6] and             A. Metavariables and Coupling
other hammers [5] for Rocq, and various hammers [12], [16],            Informally, a goal is a placeholder for an expression we
[22] and the Grind tactic in Lean.                                  are trying to find of a particular type. These placeholders are
   Pantograph [2] affirmed the importance of the critical ob-       called metavariables in Lean. Each metavariable also has a
servation that a proof may presented in a final form that           context consisting of a set of hypotheses, free variables of
differs significantly from the structure of the proof as it was     particular types that function as assumptions associated with
discovered and built a technical toolkit in Lean to support these   the metavariable. We write ?g[v1 , . . . , vm ] for a metavariable
two different views of a proof. This is the distinction between     ?g with an associated context v1 , . . . , vm . Formally, a goal
the search view and presentation view, which we discuss more        is a metavariable without an assigned value. In general,
below. The concept of search view is related to the idea of         however, metavariables can also have values assigned. The
type of a metavariable is an expression. For example, a goal                Search View
corresponding to the statement p ∧ q is ?g : p ∧ q. We write
                                                                                                                   Tra
Γ?g for the context of a goal ?g and T?g for the type of ?g,                                                           nsp
also called the target.                                                                                             Art ositio
                                                                                                                       icu
                                                                                                                           lati n




                                                                            Contextualization

                                                                                                Essentialization
   A tactic is a Lean program that acts on one or more goals,                                                                  on
assigns values to these goals, and in the process may add new
goals. A collection of goals is called a goal state or just state.                                                                   Presentation View
The constructor tactic for instance, when applied to ?g,
generates an assignment for ?g and descendant goals ?hp and
                                                                                                                              tion
?hq .                                                                                                                   b ora         n
                                                                                                                    Ela           atio
                                                                                                                              bor
                                          (
                                            ?hp : p                                                                        la
           ?g := ∧.intro(?hp , ?hq ),                                                                                  De
                                            ?hq : q
                                                                            Kernel View
In other words, one way to prove p ∧ q is to prove p and q
                                                                     Fig. 1: The Three Views of a Proof and their relations. We
individually.
                                                                     discuss Transposition in Section IV-B and Essentialization and
   Metavariables are allowed to refer to each other. For in-
                                                                     Contextualization in Section V. We do not dicsuss Articula-
stance, to prove ?g : ∃x ∈ N, x − 2 = 0, we can again use the
                                                                     tion.
constructor tactic, generating two new goals:
                                   (
                                     ?x : N
        ?g := ∃.intro(?x, ?p),                                       B. Proof Search
                                     ?p : ?x − 2 = 0
                                                                        Given the (mostly) tree structure of proofs, a natural way
The first goal requires us to find a witness for the existential     to search for a proof is to use Monte-Carlo Tree Search [1].
quantifier in the original goal. Notice that ?p mentions ?x          There are two types of nodes in the search tree: goal nodes
as part of its type. Whenever one goal refers to another,            and goal state nodes. A goal state node has a collection of
we follow the notation introduced by Aesop [10] and call             goals. The decision that must be made at a goal state node is
them coupled metavariables. Because of the possibility of            which goal to attempt to solve next. We call this the guidance
coupling, proof search is not a simple tree search but is rather     generation problem. Once a particular goal is selected, this
a search on a directed acyclic graph (DAG). Given coupled            represents a transition from a goal state node to a goal node,
goals ?g 1 , . . . , ?g n , we must make a choice about which goal   in which a single goal is present. The decision that must be
to make progress on first, and the solution of one goal may          made at a goal node is which tactic to apply to attempt to
impact the solution (or indeed the provability) of a coupled         solve the goal. We call this the tactic generation problem.
goal.                                                                Applying a tactic to a goal may either solve the goal, which
   For any goal ?g, we define the cross-section to be the            closes the current search branch, or it may generate new goals
number of goals coupled to ?g and its ancestors. Intuitively,        to solve, representing a transition from a goal node to another
the maximum cross-section encountered during a proof can be          goal state node.
seen as one measure of the difficulty of a proof. As a general       C. Proof Views
rule, tactics that produce lower cross-sections are preferable
to those that produce higher cross-sections. For example, the           In Lean, there are many different ways to prove a theorem.
problem of {?x : N, ?p : ?x − 2 = 0} has a cross-section of          Any theorem proving agent or human operator interacting with
2, but {?hp : P, ?hq : Q}, has a cross-section of only 1. The        Lean must pick a method for receiving goals from Lean and
solutions of the goals ?hp and ?hq do not interfere with each        sending tactics into Lean. For language models and people,
other.                                                               the default choice is strings, provided by Lean’s delaborator.
                                                                     Conversely, human and machine written tactics produce Lean
   In a given goal state, later goals provide cues for solving
                                                                     expressions by executing arbirary Lean code.
earlier goals. For example, consider the goals
                                                                        We adopt the terminology of Pantograph [2] in distinguish-
  1) ?x : N                                                          ing between three broad categories of proof representation
  2) ?1 : ?x is odd                                                  styles (see Figure 1). Internally, Lean stores proofs and goals
  3) ?2 : ?x is a perfect number                                     in the kernel view, as a set of assigned and unassigned
It would be easy to close the goal ?x by providing an arbitrary      metavariables, and delaborates them to the presentation view
natural number, but it could then be impossible to close the         on demand, which is a string-based representation that pri-
other two goals. It is sometimes possible to close a coupled         oritizes ease of understanding and verification. Presentation
goal without explicit action. If we are proving {?x : N, ?p :        view is concise and typically has no coupling. However, a
?x ≥ 2}, using the reflexivity property of ≥ to prove ?p would       proof written for presentation often includes mysterious and
imply that ?x := 2. This solves ?x in passing. We will exploit       unintuitive jumps, especially when introducing new expres-
this mechanism in Section IV.                                        sions. This motivates the concept of a proof in search view,
        Atomic          Constructors   Meaning
        Invalid         .bvar          Bound Variable
                                                                     tactic has only a finite number of parameter possibilities. This
        Invalid         .mvar          Metavariable                  means in particular that no tactic takes an arbitrary number
        inhabit         .sort          Type Sort                     or string, as that would make its action space infinite. For
        intro           λ x.y          Lambda function
        exact/apply     .fvar          Free variable
                                                                     example, the inhabit tactic does not take an argument—
        inhabit         .lit           Literal                       instead it generates some default value for an inhabited type.
        exact/apply     .const         Constant                      The apply tactic takes exactly one lemma argument, and in any
        pi              ∀x.y           Function Signature
        tailArg         .app           Function Application
                                                                     proof state, only a finite number of lemmas are available in the
        Unfold          .letE          Let-In binder                 environment. Note, however, that it is still possible for a proof
        Unfold          .mdata         Expression Metadata           using atomic tactics to assign arbitrary string or number literal
        apply/cases     .proj          Projection
                                                                     values to a goal. This can happen, for example, by applying
                                                                     a lemma that assigns a specific solution value.
TABLE I: Correspondence between atomic tactics and el-                  To ensure completeness, we include at least one atomic
ementary expression constructors. The constructors labeled           tactic corresponding to each top-level expression constructor
“Invalid” cannot appear at the top-level of a proof term. The        that could appear in a proof term in Lean. Table I shows
constructors labeled “Unfold” can be transformed into another        the different constructors that can appear in a proof term
case.                                                                and the corresponding atomic tactic. Those marked “Invalid”
a representation corresponding to the proof tree structure           cannot occur as the top-level constructor of a proof term, and
mentioned above. A search view proof tracks the path of              those marked “Unfold” can be transformed into a equivalent
an agent searching for a proof and may contain coupling              expression which has a different constructor.
and backtracking. More importantly, there may be information            There is one more desirable feature for a set of atomic
present in the kernel and presentation views that is elided in the   tactics. They should be chosen to minimize the cross-sections
search view, since it is not relevant for a particular goal. For     of proofs. Proofs with large cross-sections pose a greater
example, for goals ?g : P, ?h : 2 = ?x, the solution of ?h has       challenge for a theorem proving agent, as it must somehow
no impact on the solution of ?g and therefore is irrelevant to       choose which of many coupled goals to try to make progress
?g in the search view. In Section V, we describe the process         on.
of converting a goal into search view. The ϵ-δ convergence              With these objectives in mind, we now explain the chosen
proof mentioned above also illusrates the difference between         set of atomic tactics.1 We rely on the following properties
presentation and search views.                                       of our atomic tactics. These properties are necessary for the
                                                                     atomization and agent training steps we describe next.
         IV. ATOMIC TACTICS AND ATOMIZATION                             1) Invariance: No tactic ever changes the value of an
   A tactic generation agent faces the problem of the immense               assigned metavariable, i.e., once a goal is assigned, its
number of possible tactics available for constructing proofs.               assignment never changes without backtracking.
In this section, we propose one possible mitigation for this            2) Completeness: If a tactic removes a goal, it must assign
difficulty by introducing the notion of an atomic set of tactics            the goal.
and an algorithm called atomization for generating atomic               3) Progress: It is not possible for a tactic to make no
proofs from arbitrary proofs.                                               progress, i.e., a tactic never produces a goal state con-
                                                                            taining only the goal it was applied to.
A. Atomic Tactics
                                                                        4) Determinism: The atomic tactics yield the same result
   A set of tactics is atomic if it has two key features. First             for the same input goal.
of all, it must only permit a finite number of actions (for
parametric tactics, we require the number of actions to be finite    B. Transposing Atomization
even when considering all possible values of the parameters).           Recall that our motivation for creating a set of atomic tactics
In contrast, tactics used in standard Lean proofs are often non-     is to ease the burden on an agent tasked with solving the tactic
atomic in this sense. For instance, the simp tactic takes an         generation problem. But if we are to train such an agent, we
arbitrarily long parameter list, and the conv tactic environment     need training data in the form of successful search view proofs
allows for arbitrarily long navigation sequences. The use tactic     made up of atomic tactics. We next show how to obtain such
in Lean is especially non-atomic, since the witness expression       proofs via a novel transposing atomization algorithm. This
could be arbitrarily long. Atomic tactics are designed to avoid      algorithm has two important goals. The first goal is to convert
such situations. As a result, an agent that is trained to pick       arbitrarily large or complex tactics and expressions into atomic
from a set of atomic tactics need only consider a finite number      tactics. We call this atomization. The second goal is to convert
of possibilities, greatly simplifying the task. The other key        presentation view proofs into search view proofs. We call this
feature is that a set of atomic tactics should be complete in        transposition. The algorithm takes as input the ground truth
the sense that it should be sufficiently expressive to prove any     proof term of a theorem, eroot , and outputs a sequence of goal
valid Lean theorem.                                                  tactic pairs indicating the actions on individual goals.
   In Figures 9 and 10, we present a concrete set of atomic tac-
tics. The first feature is ensured by construction—each atomic         1 The full list of tactics can be found in Appendix A.
   The starting point for atomization is a ground-truth proof                          Listing 1: Nazrin’s Transposing Atomization
term proofexpr : T which proves T , also called a solution                    function atomize(proofexpr)
                                                                                 goal := Goal(infer_type(proofexpr))
for T . We use proofexpr to guide the construction of a new                      pending := [(goal, proofexpr)]
proof for T constructed using only atomic tactics. Pseudocode                    while (goal, solution) := pending.pop()
for the algorithm is shown in Listing 1. We start by creating                       if let Some((tactic, goals, solutions))
                                                                                          := atomize_step(goal, solution)
a goal for T , and inserting it and its solution into a list of                        yield (goal, tactic)
pending goals. Then, for each pair in the list, we apply the
atomize step function, which tries to find an atomic tactic that                        descendants := order_predecessor(goals,
                                                                                            solutions)
can be used on the goal. If successful, it returns the tactic, a                        for (g, s) in (goals, solutions)
set of new goals produced by the tactic when applied to the                                 pending.push(g, s)
goal, and, crucially, corresponding solutions for each new goal.                    else
                                                                                        yield (goal, :defer)
The new goals and solutions are then inserted back into the                         end
list, and the process repeats until the pending list is empty. If                end
no atomic tactic can be found, the goal is deferred, hopefully                end
becoming solvable later.                                                      # If we can create an atomic step on this goal,
   The atomize function returns a list of pairs, each containing                  return a tactic and
a goal and the corresponding atomic tactic computed for that                  # solutions to descendant goals.
                                                                              function atomize_step(goal, solution)
goal. This gives us a recipe for proving T . We simply start                     if (tactic, solutions) := try_semigrade(goal,
with the goal ?g : T , look up which atomic tactic is paired                          solution)
with ?g, and apply that tactic to get new goals. We then pick                       return (tactic, solutions)
                                                                                 else if (tactic, solutions) := try_holograde(goal
one of the new goals ?g ′ , look up which atomic tactic is paired                     , solution)
with ?g ′ , and continue until no goals are left.                                   return (tactic, solutions)
   Atomization is easy in the vast majority of cases. For                        else
                                                                                    return :defer
example, if the goal: ?g : ∀(x : X), Y has the solution:                         end
λ x 7→ y, the natural step is to associate this goal with the                 end
intro tactic. Applying the tactic to the goal produces a new
goal ?g ′ : Y whose corresponding solution is just y. We do
not have space to go into details for every atomization step,
                                                                                 In the transposing atomization algorithm, we maintain an
but the code is available with all of the details.2
                                                                              invariant that every goal will eventually acquire a unique
   By stretching out expressions into many tactics, we can
                                                                              assignment. We define the closure ?g of ?g to be the goal
generate a large amount of training data from Lean’s standard
                                                                              formed by instantiating all predecessors of ?g.
library and Mathlib. Nazrin is designed in conjunction with a
set of atomic tactics using 3 key principles:                                    During atomization, each generated goal ?g is paired with
                                                                              an expression e?g , called the solution, with the invariant Γ?g ⊢
   1) Minimization of Cross-section: Atomization should not
                                                                              e?g : T?g maintained at all times. i.e. the solution solves the
       generate a large amount of coupled goals, which pose a
                                                                              completed version of goal. We dispatch the next tactic based
       immense challenge to guidance generation discussed in
                                                                              on e?g , and if no tactics can dispatch on ?g, we defer to another
       Section V.
                                                                              goal. In this case ?g becomes dormant.
   2) Completeness: Atomic tactics should be able to repeat
                                                                                 During atomization, Lean’s usually helpful type unification
       proofs written in non-atomic tactics.
                                                                              algorithm works against us. If used naively, type unification
   3) Non-Volatility: The solution must be replay-able.
                                                                              algorithm may assign incorrect solutions to goals and back the
   There are a few more features of the algorithm worth                       atomization algorithm into an impossible corner. To avoid this
explaining. The first is the question of what order to process                problem, we rely in such cases on the synthetic tactics tailArg
the goals in. Define a goal ?h to be an immediate predecessor                 and motivatedApply, which do not do type unification. The
of goal ?g (and ?g is the immediate successor of ?h), denoted                 cost of running these tactics is that they generate large cross-
?h ≺ ?g, if an expression in ?g’s target or context contains                  sections.
?h.3 ?g ′ is a successor to ?g if there is a chain of successors
                                                                                 Within the process of proving a goal, the execution order
?g ≺ · · · ≺ ?g ′ . When we have a choice of goals to atomize,
                                                                              of tactics can often be rearranged. We call this goal-level
we preferentially choose successor goals over predecessor
                                                                              transposition and leverage it to avoid dead ends that our
goals. The solution of these goals hopefully sheds light on
                                                                              limited set of tactics would otherwise encounter. We divide
the solutions of their predecessors or solves the predecessors
                                                                              the set of atomic tactics into 7 categories, based on their
in passing. We call this process state-level transposition. A
                                                                              area of effect, which is the smallest subexpression a tactic
visualization is in Figure 2.
                                                                              modifies: a holograde tactic acts on an entire free variable
  2 Code will be released after the anonymous review period.                  or target; a semigrade tactic acts on parts of a free variable
  3 As a subtle exception to this rule, we don’t include cases where ?h has   or target; a prograde tactic acts on a free variable; and a
any parent expression whose type is a Prop.                                   retrograde tactic acts on the target. Evidently, two semigrade
       ?1                                                                 ?1

       ?2                                                                 ?2

       ?3                                                                 ?3

                                                           Time                                                            Time
                 (a) Tactic dispatch order of a proof                   (b) Tactic dispatch order of a state-level transposed proof
Fig. 2: Blue arrows represent tactic applications. State-level transposition changes the dispatch order of tactics, but does not
change the ordering of tactics on a particular goal.

            Category          Examples
            Terminal          decide
                                                                    many tactic parameters. Note that our transposing atomization
            Holo-prograde     cases                                 algorithm could be implemented in other proof assistants,
            Holo-retrograde   apply, intro                          including Rocq and Isabelle.
            Holo-bigrade      revert, induction
            Semi-prograde     rewrite (on free variable)
            Semi-retrograde   rewrite (on target)                       V. E XPR G RAPH AND G RAPH N EURAL N ETWORKS
            Semi-bigrade      unfold
                                                                       We expect atomic tactics and atomization to be useful for a
                                                                    variety of applications, but one main motivation is to provide
        TABLE II: Examples of each grade of tactics.                training data for a theorem proving agent. In this section,
                                                                    we explain the design of such an agent based on Graph
tactics can be dispatched in arbitrary order as long as their       Neural Networks (GNNs). We selected this architecture since
areas of effect do not collide. For example, rewriting a = b        a graph can compactly represent many symmetries inherent in
and c = d can dispatch in any order on a = c. Finally, a            mathematics, and we hypothesize that GNNs will thus be an
bigrade tactic acts on both the target and a free variable. In      efficient mechanism for theorem proving.
Figure 3, we show an example where the execution order of
two semi-retrograde rewrite tactics are swapped due to non-         A. ExprGraphs
conflicting acting areas. Since the coupled goal ?x has not
                                                                       The first problem we address is how to represent Lean
been instantiated at the beginning, this goal-level transposition
                                                                    expressions and goals in a format which is suitable for
allows 2 tactics to dispatch instead of 1. We use goal-level
                                                                    consumption for a machine learning agent, a GNN in our
transposition to dispatch as many tactics as possible on a
                                                                    case. We call the process of converting an expression to a
goal before deferring to a predecessor goal. A prograde and
                                                                    graph Essentialization. In the process of essentialization, we
a retrograde tactic can likewise swap without interfering with
                                                                    carefully discard irrelevant information in the solution of the
the validity of a proof. A terminal tactic closes a goal.
                                                                    current goal. For example, an expression List.head a h queries
   Note that the extra goals generated by a tactic are not
                                                                    the first element of a list, and this query requires a certificate
considered. For semigrade tactics such as rewrite, the main
                                                                    h that the list is non-empty. However, exactly how h was
goal (with its target/local assumption modified by the rewrite)
                                                                    generated is irrelevant to any goal containing this expression.
is semi-retrograde or semi-prograde, but the tactic generates
                                                                    For this reason, h should be removed from the expression in
extra goals on the side. Since the further processing of these
                                                                    question.
goals is not hindered by the main goal, they do not contribute
                                                                       Essentialization erases some technical distinctions that are
to the grade system. An example is a rewrite lemma that is
                                                                    irrelevant to searches. For example, consider ?g and ?g ′ under
gated by some condition h : p(a) → f (a) = b. Applying this
                                                                    two different contextes:
lemma to ⊢ f (a) = f (c) generates two goals, ⊢ ?1 : b = f (c)          (
and ⊢ ?2 : p(a). We can dispatch another semigrade tactic                    ⊢ ?g : f (?1)            n
on f (a) = f (c) without interfering with the operation of this                                           ⊢ ?g ′ : f (λ x 7→ ?2[x])
                                                                             ?1 := λ x 7→ ?2[x]
lemma, but any holo-retrograde tactic would not be able to
dispatch ahead of this rewrite due to conflict with the rewrite.    In the search view, ?g and ?g ′ are identical—the same se-
   Atomization also provides a metric for the difficulty of         quence of tactics that proves ?g will lead to the proof of ?g ′
a proof. A proof whose atomization trace contains large             and vice versa—but they are different in the kernel view since
cross sections requires the simultaneous consideration of many      the former involves an additional metavariable ?1. We say ?g
factors. A proof whose atomization is long requires more steps.     and ?g ′ are search-view equivalent. If goal ?h is not coupled
The benefit of this measurement compared to number of lines         to ?g, then ?h would not participate in the ExprGraph for
or number of tactics is that proofs with few but arbitrarily        ?g. This is in contrast to Lean’s infoview which displays all
long tactics cannot hide their difficulty by simply having          unsolved goals.
                                                 1+𝑑 =𝑏+𝑎
                                           𝑎+𝑏 =1+𝑑    𝑎+𝑏 =𝑏+𝑎
                           ?𝑥 ≔ 1                                                        𝑎+𝑏 =𝑏+𝑎
                                                                                                                    …
               𝑎 + 𝑏 =?𝑥 + 𝑑                                                                  𝑏+𝑎=𝑏+𝑎

                   𝑎+𝑏 =𝑏+𝑎                                                              1+𝑑 =𝑏+𝑎
                                           𝑏 + 𝑎 =?𝑥 + 𝑑            𝑏+𝑎=1+𝑑
                                                           ?𝑥 ≔ 1                                                       ,
Fig. 3: Goal-level transposition switches orders of tactics on the same goal. Although ?x is not assigned, we can dispatch a
rewrite tactic if we rearrange the order of semigrade tactics.


                   Kind                                intro, abandon                                        Exit

                                Apply                                   apply

                               Induction       Major                      induction

                                Rewrite        Locus        Direction                rewrite
Fig. 4: Neural Probabilistic Automaton for Tactic Generation. Green states perform premise selection, Blue states perform
free variable selection. Yellow states perform locus selection. White states perform fixed-length categorical selection. Tactics
without parameters are dispatched directly by the Kind state and hence do not show up as states of the NPA.


   Each essentialized expression and goal is represented as                            Prop          𝑝        𝑞
an ExprGraph, a heterogeneous graph whose nodes are the
syntactic elements and whose edges represent relationships                      Prop          Prop
between them. This allows graph message passing to transmit                                                   𝑞         𝑝

information between related parts of the graph and between                       𝑝             𝑞         ∨          ∨
coupled goals. A simple example is shown in Figure 5. An
ExprGraph G(e) of an expression e is designed to have several                                                Or

desirable properties:
                                                                  Fig. 5: ExprGraph of ∀(p q : Prop), p ∨ q → q ∨ p. Notice
   1) Symmetry: If two expressions are α-equivalent or
                                                                  that every subexpression corresponds to a locus (grey vertex)
      search-view equivalent, they have the same ExprGraph.
                                                                  in this graph.
      This erases immaterial
                      R        distinctions
                                      R     in the kernel view.
      For example, f (x) dx and f (y) dy have identical
      meanings and produce the same ExprGraph.
   2) Self-Similarity: If e1 is a subexpression of e2 , then      eration of tactics with parameters is slightly more complicated.
      G(e1 ) is a subgraph of G(e2 ).                             Since a graph neural network is not a generative model, it
   3) Locus Conservation: Every rewritable subexpression          cannot easily generate parameterized tactics. However, armed
      (locus) of e corresponds uniquely to a vertex in G(e).      with atomic tactics, we can use the GNN to condition the
   4) Condensation: All references to the same constant, sort,    probabilities inside a non-deterministic automaton. We call
      or literal in an expression are connected with a single     this architecture a neural probabilistic automaton (NPA).
      shared vertex.                                              The transition probability from one state to the next is defined
Figure 6 visualizes essential aspects of ExprGraphs.              by the neural network with a categorical distributional output.
                                                                  An NPA is a highly specialized heterogeneous autoregressive
B. Tactic Generation from Graph Neural Networks                   model that can create finite length tactics.
   The set of atomic tactics effectively makes the proof search      The first state (called “Kind”) of the NPA selects which tac-
action space finite. This finiteness reopens many toolboxes       tic to use. Then, depending on the tactic, additional specialized
from classical reinforcement learning and makes the model         GNN heads generate arguments to the tactic in descendant
more diagnosable. If none of our tactics had parameters, our      states. For instance, the Kind state can pick the intro tactic,
model could simply output a probability distribution. The gen-    which leads to the termination of the NPA. On the other hand,
                                                                    the seconds-level tactic generation speed of language models,
                                                                    Nazrin and other GNN-based models can generate thousands
                       [1] 𝑎          :ℕ                            of tactics per minute, enabling highly parallelized proof
                       [2] 𝑏          : ℕ Nat                       searches. Since Nazrin is trained from scratch on atomization
                                                                    data, we can ensure the absence of data leakage from the
                       [3] 𝑓          :ℕ→ℕ
                                                                    training set to the test set. We train Nazrin Prover with
                       [4] ℎ=         : 𝑎=𝑏                         exclusively supervised learning data and no online data. This
                        ⊢ 𝑓 𝑎=𝑓 𝑏                                   is in contrast to Q-function learning where the model learns
                                          Eq                        to estimate the reward of actions.
                                                                       In Nazrin, we use a mechanical form of guidance generation
            (a) Essentialization erases variable names              known as rainbow guidance: If ?g ≺ ?h, then the agent
                           Nat
                                                                    assigns a higher priority to ?h. This encourages an agent to
                         𝑥:ℕ
                                                                    first explore successors rather than predecessors. If there is
                      ⊢? 𝑦 : ℕ                                      a tie, we use the ordering of goals within a state as the tie-
                                                                    breaker. On any goal ?g, the tactic agent can emit a special
                         𝑥:ℕ
                      ⊢ ?1 : gcd(𝑥 ,? 𝑦[𝑥]) = 0   0                 abandon action, indicating that no more progress can be made.
                            gcd            Eq                       This abandon semantics is used for two cases: If the search
                                                                    agent believes it is futile to continue searching on a goal, and
     (b) Essentialization cross-references variables in coupled     if the current goal’s predecessors need further progress and
     goals                                                          information before any tactic can make progress on a goal.
Fig. 6: We visualize key aspects of goals and the corresponding                               VI. E VALUATION
ExprGraph. Colored lines highlight edges which replaces
variable names. Circles represent nodes that consolidate all           We evaluate Nazrin using Lean v4.25.2 and Julia v1.12.4
references to a constant.                                           for running Graph Neural Networks. We first atomized 170180
                                                                    user-defined theorems in Lean’s standard library and Mathlib.
                                                                       Atomized theorems generally have low cross-sections as
if the Kind state picks the apply tactic, we then consult the       shown in Figure 7. The success rate of atomization is about
apply state to pick a constant. This is a retrieval problem where   58%. We set a limit of 3000 maximum steps due to compu-
the query is an embedding vector, the keys are embedding            tation time limits. The atomization algorithm can fail if this
vectors for all usable constants, and the values are Lean           maximum is exceeded or if the current heuristics fail to find
constant names. A subset of our NPA is shown in Figure 4.           a transposition.
                                                                       We then sorted the atomized theorems topologically to
   The generated tactic has to be contextualized into a form
                                                                    ensure that all dependencies of a theorem precede the the-
Lean can understand. This includes translating locus indices
                                                                    orem. This ensures the absence of information leakage during
into subexpression positions and translating free variable in-
                                                                    training. Our evaluation setup mimics a real use case, where
dices to free variable names. The contextualized tactic then
                                                                    a user is trying to develop a new formalized theory based on
dispatches in Lean.
                                                                    Mathlib. We divided the theorems in the standard library into
   We construct the GNN out of 4 components: an embedding           2 slices and those in Mathlib into 10 slices. We measure the
layer which contains embeddings of individual constants, a          generalizability of Nazrin Prover by training it on slice i and
core equivariant GNN which is responsible for in-depth under-       evaluating it on slice i+1. The metric for evaluation is the rate
standing of an expression, a fixed-point invariant GNN which        of successful proofs within a 15-second time limit. With our
generates embeddings from unseen constants, and individual          atomized dataset, we trained Nazrin Prover on the standard
tactic heads to control probability distributions on each state.    library slice 1 for 100 epochs. Each segment has about 10000
The fixed-point invariant GNN is used to generate embeddings        theorems. After training on stdlib slice 1, we evaluate Nazrin
for unseen new functions and theorems, which allows the GNN         Prover on stdlib slice 2, achieving an accuracy of 57% percent
to operate on symbols that are not in its training set.             on a random subset (Appendix C). We then trained Nazrin
   We use an embedding dimension of 32, a core GNN using            Prover on Mathlib slice 3, and mesaured its proof completion
5 attention convolution layers of 4 heads each, and the gelu        rate on slice 4. This reached 34%. We compare with Aesop
activation function [7]. It has a total of 1.5 million parameters   [10] and Grind [15] automation tactics in Figure 8.4 Observe
when running on standard library and 11 million parameters          that Nazrin Prover is capable of proving theorems that other
on Mathlib, most of which are in the embedding layer. We            automation tactics cannot discharge.
execute intro and terminal tactics with mechanical assistance:
these tactics are automatically tried before consulting the graph      4 For Aesop and Nazrin, we use perfect premise selection, both to ensure

neural network.                                                     fairness and to prevent Aesop from proving a theorem using itself. Nazrin
                                                                    does not have to operate with perfect premise selection in production. There
   The Nazrin Prover is small enough to train and evaluate          is no easy way to do this for Grind, so Nazrin is at a disadvantage in this
on a consumer-grade CPU-only machine. In comparison to              experiment.
                       (a) Standard Library                                                   (b) Mathlib
                             Fig. 7: Maximum cross-section and proof length in atomized proofs.




         (a) Runtime/Completion Comparison with Aesop                      (b) Runtime/Completion Comparison with Grind
Fig. 8: Comparison of Nazrin Prover with Aesop and Grind on a sample of slice 4 of Mathlib. Both provers are allotted 15
seconds. The bottom-right data points represent theorems that Nazrin Prover can prove but aesop/grind cannot.


                     VII. C ONCLUSION                              refine its architecture and boost performance. In particular,
   We introduce atomic tactics which provide a finite action       a neural network could replace the existing mechanically
space for prover agents. We describe a transposing atomiza-        generated rainbow guidance. Moreover, in tactics with multiple
tion algorithm, which converts existing proofs into atomized       parameters, the later parameters are not conditioned on the
proofs. We introduce Nazrin Prover, a GNN-based high-              former parameters. We made this simplification to accelerate
throughput and high-performance theorem proving agent. We          training and inference. This may make it difficult for the NPA
evaluate the agent on generalization tasks on Lean’s standard      to generate such tactics. Our results with Nazrin Prover could
library and Mathlib, demonstrating complementary capabilities      also likely be improved with more training.
with other proof automation tactics.                                  The GNN does not process numbers and strings. In future
   Atomization does not yet work for all theorems. Future          work, another model or a mechanical method could take
work could improve the coverage for atomization in Mathlib.        over to resolve these problems. We work around this issue
The atomization algorithm sometimes generates proofs of high       by assigning goals in passing using Lean’s type unification
cross sections. This places a burden on the prover agent to find   system.
one goal out of many to make progress on. Future work could
focus on obtaining lower cross-sections.                                                     R EFERENCES
   The architecture of Nazrin Prover has not been carefully        [1] Bruce Abramson and Richard Korf. A model of two-player evaluation
tuned to maximize performance. Future work could further               functions. pages 90–94, 01 1987.
 [2] Leni Aniva, Chuyue Sun, Brando Miranda, Clark Barrett, and Sanmi           [19] Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang Wu, Xia Xiao,
     Koyejo. Pantograph: A machine-to-machine interaction interface for              Yifan Sun, Shen Zheng, and Kai Shen. Bfs-prover: Scalable best-first
     advanced theorem proving, high level reasoning, and data extraction in          tree search for llm-based automatic theorem proving, 2025. URL: https:
     lean 4, 2025. URL: https://arxiv.org/abs/2410.16429, arXiv:2410.                //arxiv.org/abs/2502.03438, arXiv:2502.03438.
     16429.                                                                     [20] Qiyuan Xu, Renxi Wang, Peixin Wang, Haonan Li, and Conrad Watt. A
 [3] Stefan Berghofer and Christian Urban. A head-to-head comparison of de           minimalist proof language for neural theorem proving over isabelle/hol,
     bruijn indices and names. Electronic Notes in Theoretical Computer Sci-         2025. URL: https://arxiv.org/abs/2507.18885, arXiv:2507.18885.
     ence, 174(5):53–67, 2007. Proceedings of the First International Work-     [21] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song,
     shop on Logical Frameworks and Meta-Languages: Theory and Practice              Shixing Yu, Saad Godil, Ryan J Prenger, and Animashree Anandkumar.
     (LFMTP 2006). URL: https://www.sciencedirect.com/science/article/pii/           Leandojo: Theorem proving with retrieval-augmented language models.
     S1571066107002319, doi:10.1016/j.entcs.2007.01.018.                             Advances in Neural Information Processing Systems, 36:21573–21612,
 [4] Sascha Böhme and Tobias Nipkow. Sledgehammer: judgement day. In                2023.
     International Joint Conference on Automated Reasoning, pages 107–          [22] Thomas Zhu, Joshua Clune, Jeremy Avigad, Albert Qiaochu Jiang, and
     121. Springer, 2010.                                                            Sean Welleck. Premise selection for a lean hammer, 2026. URL: https:
 [5] Łukasz Czajka and Cezary Kaliszyk. Hammer for coq: Automation for               //arxiv.org/abs/2506.07477, arXiv:2506.07477.
     dependent type theory. Journal of Automated Reasoning, 61(1):423–453,
     2018. doi:10.1007/s10817-018-9458-4.                                                                      A PPENDIX
 [6] Burak Ekici, Alain Mebsout, Cesare Tinelli, Chantal Keller, Guy Katz,
     Andrew Reynolds, and Clark Barrett. SMTCoq: A plug-in for integrating
                                                                                A. Atomic Tactics
     SMT solvers into Coq. In Rupak Majumdar and Viktor Kuncak, editors,           Below is the list of all atomic tactics. x ≪ y means
     Proceedings of the 29th International Conference on Computer Aided
     Verification (CAV ’17), volume 10426 of Lecture Notes in Computer
                                                                                y is type-dependent on x. unify(x, y) holds if x and y’s
     Science, pages 126–136. Springer, July 2017. Heidelberg, Germany.          types can be unified, and transform(x, f ) transforms every
     URL: http://theory.stanford.edu/∼barrett/pubs/EMT+17.pdf.                  subexpression of x using the operation described by f . We
 [7] Dan Hendrycks and Kevin Gimpel. Bridging nonlinearities and stochas-       first consider the tactics in Figure 9. These are tactics already
     tic regularizers with gaussian error linear units. CoRR, abs/1606.08415,
     2016. URL: http://arxiv.org/abs/1606.08415, arXiv:1606.08415.              present in Lean, with a few small modifications. The value of
 [8] Guillaume Lample, Marie-Anne Lachaux, Thibaut Lavril, Xavier Mar-          x supplied to the exact tactic is only allowed to be a constant
     tinet, Amaury Hayat, Gabriel Ebner, Aurélien Rodriguez, and Timothée     or free variable that already appears in the goal (including its
     Lacroix. Hypertree proof search for neural theorem proving, 2022.
     arXiv:2205.11491.                                                          context), thus limiting the choice to a finite set of possibilities.
 [9] Yutong Li, Yitian Zhou, Xudong Wang, GuoChen, and Caiyan Qin.                 We create the following synthetic atomic tactics to handle
     Graphmind: Theorem selection and conclusion generation framework           edge cases:
     with dynamic gnn for llm reasoning, 2025. URL: https://arxiv.org/abs/
     2511.19078, arXiv:2511.19078.                                                 Figure 10 describes a set of hand-crafted tactics which,
[10] Jannis Limperg and Asta Halkjær From. Aesop: White-box best-first          together with those in Figure 9 and the two positional tactics
     proof search for lean. In Proceedings of the 12th ACM SIGPLAN              below, complete our set of atomic tactics. These are crafted to
     International Conference on Certified Programs and Proofs, CPP 2023,
     page 253–266, New York, NY, USA, 2023. Association for Computing           help meet our objectives of completeness and limited cross-
     Machinery. doi:10.1145/3573105.3575671.                                    section. Each rule has a finite number of parameters, each
[11] mathlib. The lean mathematical library. CoRR, abs/1910.09336, 2019.        of which has a finite number of choices. This provides a
     URL: http://arxiv.org/abs/1910.09336, arXiv:1910.09336.
[12] Abdalrhman Mohamed, Tomaz Mascarenhas, Harun Khan, Haniel Bar-             finite action space for any agent using these atomic tactics.
     bosa, Andrew Reynolds, Yicheng Qian, Cesare Tinelli, and Clark Barrett.    pi generates a raw ∀ binder; inhabit generates a default value
     Lean-smt: An smt tactic for discharging proof goals in lean, 2025. URL:    for a target which is a known inhabited type; reduceBeta
     https://arxiv.org/abs/2505.15796, arXiv:2505.15796.
[13] REBECCA LEA MORRIS. Motivated proofs: what they are, why                   β-reduces all subexpressions in the current goal; normalize
     they matter and how to write them.             The Review of Symbolic      unfolds type class function calls in Lean, which is a mech-
     Logic, 13(1):23–46, November 2019. URL: http://dx.doi.org/10.1017/         anism for handling arithmetic operators; motivatedApply is
     S1755020319000583, doi:10.1017/s1755020319000583.
[14] Aditya Paliwal, Sarah Loos, Markus Rabe, Kshitij Bansal, and Christian     an apply-like tactic which enforces type equality not via
     Szegedy. Graph representations for higher-order logic and theorem          aggressive unification but rather via a conduit ?c; This is
     proving. Proceedings of the AAAI Conference on Artificial Intelli-         used as a last-resort mechanism when converting a proof to
     gence, 34(03):2967–2974, Apr. 2020. URL: https://ojs.aaai.org/index.
     php/AAAI/article/view/5689, doi:10.1609/aaai.v34i03.5689.                  atomic tactics, if the apply tactic is unusable because of its
[15] André Platzer and Geoff Sutcliffe, editors. The Lean 4 Theorem            reliance on unification. tailArg introduces a raw unary function
     Prover and Programming Language, Cham, 2021. Springer International        application; congruenceArg and congruenceFun are last-resort
     Publishing.
[16] Yicheng Qian, Joshua Clune, Clark Barrett, and Jeremy Avigad. Lean-
                                                                                tactics for handling congruences that cannot be written as
     auto: An interface between lean 4 and automated theorem provers, 2025.     rewrites.
     URL: https://arxiv.org/abs/2505.14929, arXiv:2505.14929.                      There are two last rules in our atomic set, which are more
[17] Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao Shen, Yichun Yin,
     Jing Xiong, Enze Xie, Han Shi, Yujun Li, Lin Li, Jian Yin, Zhen-
                                                                                easily explained using examples. rewritePos(heq, locus,
     guo Li, and Xiaodan Liang. Dt-solver: Automated theorem prov-              symm) is a rewrite tactic using a lemma h which acts on a
     ing with dynamic-tree sampling guided by proof-level value func-           subexpression position called a locus rather than the nth match
     tion. In Proceedings of the 61st Annual Meeting of the Associa-
     tion for Computational Linguistics (Volume 1: Long Papers), page
                                                                                of h. For example,
     12632–12646, Toronto, Canada, Jul 2023. Association for Compu-                                          ⊢ g(b + 1) = f (a), h : a = b + 1
     tational Linguistics. URL: https://aclanthology.org/2023.acl-long.706,          rewritePos(h, p, ←)
     doi:10.18653/v1/2023.acl-long.706.                                                                               ⊢ g(a) = f (a)
[18] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu,               Here, p points to the expression b + 1, and ← indicates that
     Bo Liu, Chong Ruan, Wenda Li, and Xiaodan Liang. Deepseek-prover:
     Advancing theorem proving in llms through large-scale synthetic data,      the equation a = b + 1 is used as a rewrite rule from right to
     2024. URL: https://arxiv.org/abs/2405.14333, arXiv:2405.14333.             left.
                                   ?g : ∀x : X.Y                                   ?g : X, x : X, x is a constant or free
                  intro                                                 exact(x)
                          ?g := λx.?h[x]; {x : X} ⊢ ?h : Y                                        ?g := x
                          ?g : X, X is decidable                            {xi } ⊢ ?g : X, ¬?g contains of contradiction
                decide                                      contradiction
                             ?g := decide(X)                                             ?g := contradict(?g)
                                  ?g : X = Y, unify(X, Y )                      {xi : Xi } ⊢ ?g : X, ∃i.Xi = X
                            rfl                                    assumption
                                        ?g := Eq.refl                                       ?g := xi
                                              ?g : Y, f : X1 → · · · → Xn ; ∃i.unify(Xi+1 → · · · → Xn , Y )
                                  apply(f )
                                                             ?g := f ?g 1 , . . . , ?g i ; ?g j : Xj
                                                                  {m : M } ⊢ ?g : X
                      cases(m)
                                      ?g := X.rec(λ xc .?g c (xC ) | c); {xc ⊢ ?g c : X|c is a constructor of M }
                                                                     {m : M } ⊢ ?g : Xm
                induction(m, r)
                                      ?g := r(λ x λ Xc(x) .?g c (xc ) | c); {xc , h : Xc(x) ⊢ ?g c : X|c is a minor of r}
                                                {x1 : X1 , . . . , xn : Xn }?g : Y, xi ≪ xj for j > i
                            revert(i)
                                        ?g := ?h xi , . . . , xn ; {x1 , . . . , xi−1 } ⊢ ?h : Xi → · · · → Xn → Y


                                                 Fig. 9: Built-in Lean tactics as atomic tactics


                                            ?y : Type                                             ?g : X, g ∈ Inhabited
                    pi                                                                  inhabit
                          ?y := ∀x : ?X.?z, ?X : Type, ?z[x : ?X] : Type                            ?g := default(X)
                                                             ?g has a β-reducible subexpression
                                                reduceBeta
                                                                  transform(?g, β-reduce)
                                                                  ?g has type class calls
                                                  normalize
                                                              transform(?g, unfold type class)
                                                                       ?y : Y
                                         tailArg
                                                    ?y := ?f ?x, ?X : Type, ?f : ?X → Y, ?x : ?X
                                                                ?g : Y, f : (X1 , . . . , Xn ) → B
                            motivatedApply(f )
                                                      ?g := Eq.mp ?c (f ?x1 , . . . , ?xn ), ?xi : Xi , ?c : B = Y
                                                               ?g : b1 = b2 , b1 , b2 : β
                congruenceArg
                                      ?g := congrArg?α ?a1 ?a2 ?f ?h; ?a1 , ?a2 : ?α, ?f : ?α → β, ?h : ?a1 = ?a2
                                                                ?g : b1 = b2 , b1 , b2 : β
                 congruenceFun
                                       ?g := congrFun?α ?a ?f1 ?f2 ?h; ?a : ?α, ?f1 , ?f2 : ?α → β, ?h : ?f1 = ?f2


                                        Fig. 10: Synthetic atomic tactics for handling edge cases


  A similar rule using positions is generalizeAt(locus),                    skip over the difficult problem of expression navigation using
which replaces some subexpression with a fresh variable. For                conv or congr.
example,
                                                                            B. Example of Transposing Atomization
                             ⊢ f ′ (2x + 3) = 0
            generalizeAt(p)                                                   In Figure 11, we show an example of an atomized proof.
                            {y : R} ⊢ f ′ (y) = 0                           The atomized proof contains rewrite tactics that have exactly
Here, we replace the subexpression 2x+3 with a fresh variable               one operand and applies to a single locus.
y.
   The positional tactics rewritePos and generalizeAt act di-               C. Evaluation Result on Stdlib
rectly on a specific subtree. This enables neural networks to                 Evaluation result of Nazrin on Lean’s standard library is
focus on a subexpression using attention-like mechanisms and                in Figure 13. We train Nazrin on successive slices of Lean
        example (n m k : Nat) (ih : n + m = n + k → m = k) :
        (n + 1) + m = (n + 1) + k → m = k :=
          let h1 := Nat.succ.injEq (n + m) (n + k)
          let h2 := Eq.trans (congr (congrArg Eq
        (Nat.succ_add n m)) (Nat.succ_add n k)) h1
          let h3 := implies_congr h2 (Eq.refl (m = k))
          Eq.mpr h3 ih




                       (a) Before atomization

        example (n m k : Nat) (ih : n + m = n + k → m = k) :
        (n + 1) + m = (n + 1) + k → m = k := by
          rewrite [Nat.succ_add]
          rewrite [Nat.succ_add]
          rewrite [Nat.succ.injEq]
          exact ih




                       (b) After atomization
  Fig. 11: Example of a proof before and after atomization




                                                                   Fig. 13: Search evaluation of the model on epoch 100 on slice
Fig. 12: Training history of Nazrin prover on slices of Mathlib.   2 with a time limit of 15 seconds per theorem; Blue dots
After training on slice 1, we evaluate it on slice 2               indicate successes, and orange dots indicate failures.


Standard Library and Mathlib 4, using topological ordering to
ensure the absence of information leakage.
