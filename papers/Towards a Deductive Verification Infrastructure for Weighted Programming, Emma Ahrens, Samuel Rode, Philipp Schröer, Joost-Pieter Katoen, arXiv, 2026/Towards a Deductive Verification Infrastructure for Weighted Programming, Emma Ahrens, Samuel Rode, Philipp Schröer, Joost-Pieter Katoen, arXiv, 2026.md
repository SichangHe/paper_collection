                                         Towards a Deductive Verification Infrastructure
                                         for Weighted Programming
                                         EMMA AHRENS∗ , RWTH Aachen University, Germany
                                         SAMUEL RODE∗ , RWTH Aachen University, Germany
                                         PHILIPP SCHRÖER∗ , RWTH Aachen University, Germany
                                         JOOST-PIETER KATOEN, RWTH Aachen University, Germany
                                         Weighted programs extend guarded commands with trace weights drawn from a semiring, or more generally a
arXiv:2608.18971v1 [cs.PL] 19 Aug 2026




                                         monoid-module. Varying this algebra gives one programmatic syntax for a variety of quantitative and symbolic
                                         models. Weakest-preweighting semantics provides a compositional basis for reasoning about those programs.
                                            We present a deductive verification framework based on a weighted assertion language and an intermediate
                                         verification language. Its weight domains are ordered structures with implication and coimplication, which let
                                         verification conditions express lower- and upper-bound obligations internally. We prove sound translations
                                         of core commands and reusable encodings for various proof rules applying to procedure calls and loops. To
                                         facilitate automation, we prove soundness of a quantifier elimination procedure for our assertion language.
                                         A prototype in the Caesar verifier checks case studies for probabilistic queueing costs, recursive database
                                         provenance with cyclic dependencies, clearance bounds for networks of arbitrary size, and formal-language
                                         reasoning about lock-freedom of a compare-and-swap counter.
                                         Additional Key Words and Phrases: weighted programming, deductive verification, intermediate verification
                                         languages, semirings, Heyting algebras

                                         1   Introduction
                                         Quantitative reasoning is becoming increasingly relevant across many different branches of com-
                                         puter science. Recent work ranges from weighted transition systems and automata [16, 21] to
                                         weighted logics [11, 32] and declarative languages [7, 9, 35]. In database theory, provenance analysis
                                         uses semiring semantics to investigate why queries return the answers they do [18, 19]. Weighted
                                         semantics have also been studied for Datalog, a programming language for data reasoning [10],
                                         while [20] considers logic programming with semiring semantics. Further developments include
                                         weighted rewriting [2, 3], weighted pushdown automata [27], Guarded Kleene Algebra with Tests
                                         with semiring semantics [26], and Weighted NetKAT [1]. Overall, this amount of research raises a
                                         natural question: To what extent can we automate quantitative reasoning?
                                            Weighted Programming. This work takes a step towards semi-automatic verification of weighted
                                         programs, as introduced by Batz et al., which is a generalization of classical programs where
                                         executions accumulate weights from an algebraic domain. This domain is usually a semiring, and
                                         in the general form a monoid-module with additive aggregation ⊕ and scalar multiplication ⊗. The
                                         weights can express quantitative properties, such as costs, probabilities, and security clearances,
                                         as well as symbolic properties, such as formal trace languages. Weigh statements multiply weight
                                         along execution traces, while non-deterministic choice combines traces via the additive operation.
                                            For example, the Boolean semiring, with addition ⊕ = ∨ and scalar multiplication ⊗ = ∧,
                                         yields programs with Boolean assertions and angelic non-determinism. The tropical monoid-module
                                         Wtrop over N∞ yields programs that optimize for minimal costs (⊕ = min), where costs are additive
                                         ∗ Equal contribution.


                                         Authors’ Contact Information: Emma Ahrens, ahrens@cs.rwth-aachen.de, RWTH Aachen University, Aachen, Germany;
                                         Samuel Rode, samuel.rode@rwth-aachen.de, RWTH Aachen University, Aachen, Germany; Philipp Schröer, phisch@cs.rwth-
                                         aachen.de, RWTH Aachen University, Aachen, Germany; Joost-Pieter Katoen, katoen@cs.rwth-aachen.de, RWTH Aachen
                                         University, Aachen, Germany.
2                                                                               Ahrens, Rode, Schröer, and Katoen



           𝑐 := 1#                                         while ( true ) {
           while ( 𝑛 > 0 ) {                                     𝑁
                                                                 Ê
                                                                        { 𝑖 := 𝑗 }#
               𝑛 := 𝑛 − 1#                                        𝑗=1
                 {                                              if ( ℓ [𝑖] = 𝑣 ) {
                       ⊗𝑐                                            ⊗ 𝑆𝑖 # 𝑣 := ℓ [𝑖] + 1 # ℓ [𝑖] := 𝑣
                 }⊕{                                            } else {
                       ⊗ 𝑦 # 𝑛 := 0   }}                                ⊗ 𝐹𝑖 # ℓ [𝑖] := 𝑣                  }}
(a) Ski rental problem (tropical monoid-module). For     (b) Compare-and-swap counter with 𝑁 threads (for-
𝑛 days of skiing, the program models the choice be-      mal languages monoid-module). Each thread 𝑖 at-
tween renting skis for a day at a cost of 1, or buying   tempts to increment a shared counter ℓ [𝑖] from a
skis for a cost of 𝑦.                                    value 𝑣 to 𝑣 + 1. Failure weighs by 𝐹𝑖 , success by 𝑆𝑖 .

          Fig. 1. Weighted programs for the ski rental problem and a compare-and-swap counter.


(⊗ = +). The Ski-rental problem (Figure 1a) is a classical example of an optimization problem that
can be modeled as a weighted program over the tropical monoid-module. Given either the choice
of renting skis for a day at a cost of 1, or buying skis for a cost of 𝑦, the goal is to minimize the
total cost over 𝑛 days. We can also represent a compare-and-swap (CAS) concurrent counter as a
weighted program over the monoid-modules of formal languages, shown in Figure 1b. We want to
show lock-freedom, i.e. that there always exists a thread that makes progress.
   Weakest preweightings generalize Dijkstra’s weakest preconditions [15] and probabilistic weakest
preexpectations [29] to weighted programs [7]. The transformer wp proceeds backwards through
the program and computes a weighting that maps each program state to the aggregate weight of
all executions starting in that state. For the Boolean semiring, this states whether there exists an
execution satisfying all assertions. For the tropical monoid-module, this is the minimal cost among
all non-deterministic execution traces.
   Assertions, Assumptions, Proof Rules. To automate such reasoning, we extend weighted programs
with verification statements such as assert and assume. These statements allow us to reify proof rules
as programs: reasoning principles for loops and procedure calls become program encodings that
manipulate states and weights. In the weighted setting, verification statements must be quantitative,
i.e., they must support lower- and upper-bound reasoning. For example, procedure calls can be
represented by a program that asserts a preweighting 𝜌, forgets (“havocs”) the values of variables
𝛽 modifiable by the callee, and assumes a postweighting 𝜓 . Similarly, loop rules such as Park
induction and 𝑘-induction [6] can be encoded as programs that check quantitative invariants.
   By reifying proof rules as programs, one can use a small, reusable backend for many verification
techniques. This is the idea of an intermediate verification language (IVL), a simple programming
language with verification statements and verification-condition generation. Successful classical
IVL-based infrastructures include Boogie [5] and Why3 [17]. A program in the source language is
translated to the IVL, with the proof rules encoded in the IVL. Here, generic transformations and
optimizations can be applied to the IVL program, and then verification conditions are generated
and discharged by an SMT solver.
  Goals of this Paper. We want to build a verification infrastructure for weighted programming,
supporting a wide variety of algebraic domains and verification techniques. Weakest preweighting
Towards a Verification Infrastructure for wGCL                                                                                          3


                         semantics of                          semantics of
        𝜔 -Continuous                                                       wGCL: Weighted          reasons about
                                   Weakest Preweightings
       Monoid-Modules                                                    Programming Language
                                                                                                               Proof Rules
               adds                                                                                       (Specification Statements,
               implications                        formalisation                      encoded in
                                                                                                         local Park Induction, local
                                                                                                         𝜅 -Induction, 𝜔 -Invariants)
                                        wHeyLo: Verification                  wHeyVL: Verifi-
      Heyting Algebras                                                                                encoded in
                                          Preweightings                       cation Language



                                                                Quantifier
                                                                                                SMT Solver
                                                               Elimination


Fig. 2. Overview of our verification infrastructure for weighted programming. The left side shows the algebraic
structures and assertion language, while the right side shows the IVL and verification pipeline.


semantics exists for weighted programs, but we lack an assertion language, an IVL, and encod-
ings of proof rules for weighted programming. We therefore generalize the Caesar verification
infrastructure [33], from probabilistic to weighted programming.
   Because weighted programming is parametric over the concrete monoid-module, we need
to instantiate the assertion language and IVL for different algebraic domains. In particular, we
need notions of quantitative conjunctions and implications, with support for both lower- and
upper-bound reasoning. We address this by parameterizing wHeyLo and wHeyVL over Heyting
algebras, which provide the conjunction and implication operations,1 and further generalizing
encodings of proof rules. Another challenge is automation. The wHeyVL encodings of proof rules
introduce quantitative infimum and supremum quantifiers, which are difficult for SMT solvers to
handle directly. While complete quantifier elimination exists for restricted quantitative assertion
fragments [8], we also have structural specifications and domain-specific expressions outside of
such a fragment. We therefore provide a best-effort quantifier-elimination pass for wHeyLo that
eliminates supported quantifiers and leaves the rest unchanged.
  Overview of Our Approach. The first layer in Figure 2 is the source language: monoid-modules
are the basis for the weakest preweighting semantics for the wGCL language of weighted programs.
The second layer is our verification infrastructure: based on Heyting algebras for semantics, we
define the wHeyLo assertion language. wGCL programs are translated to wHeyVL programs, using
encodings of proof rules for procedure calls and loops. The semantics of wHeyVL is defined via
verification preweightings in wHeyLo, and approximates the original wGCL semantics (soundness).
We provide a quantifier elimination procedure for wHeyLo to enable SMT-based reasoning.
   Contributions. We develop a deductive verification infrastructure for weighted programming.
      • We introduce wHeyLo, a weighted assertion language parameterized by bi-Heyting algebras,
        and instantiate it for totally ordered and Boolean algebras, and the Why monoid-module.
      • We define wHeyVL, an intermediate verification language for lower- and upper-bound
        reasoning.
      • For proof rules, we encode specification statements, Park induction, 𝜅-induction, and 𝜔-
        invariants as wHeyVL programs and address local variables in our soundness proofs.
      • We formalize a best-effort quantifier-elimination pass for wHeyLo that preserves valid-
        ity/covalidity on arbitrary verification conditions and is complete on identified fragments.

1 Although Caesar’s HeyLo and HeyVL are named after Heyting algebras, prior work only supported the setting specific to

expected-value reasoning, not general Heyting algebras [33].
4                                                                                   Ahrens, Rode, Schröer, and Katoen


       • We prototype the approach in Caesar and evaluate it on case studies spanning expected
         costs, provenance, security clearances, and formal-language reasoning about lock-freedom.

2     Weighted Programming and Reasoning via Weakest Preweightings
We define the wGCL language of weighted programs, named for a weighted version of the proba-
bilistic pGCL language [29], in turn named after Dijkstra’s guarded command language GCL [15].
wGCL is based on monoid-modules, providing a general algebraic structure for trace weights.

2.1    Monoid-Modules
Monoid-modules consist of a monoid M and a module W over that monoid, and they generalize
semirings, which are more commonly used in the literature on weighted automata and optimization.
  Definition 2.1 (Monoid-Module). A monoid M = (𝑀, ⊙, 1) is a set 𝑀 together with an associative
multiplication ⊙ : 𝑀 × 𝑀 → 𝑀 and the corresponding neutral element 1 ∈ 𝑀.
  A module W = (𝑊 , ⊕, 0, ⊗) over the monoid M consists of a commutative monoid (𝑊 , ⊕, 0)
together with a scalar multiplication ⊗ : 𝑀 × 𝑊 → 𝑊 such that
       • multiplication is associative and distributive, hence for all 𝑣, 𝑤 ∈ 𝑀 and 𝑥, 𝑦 ∈ 𝑊 it is
         (𝑣 ⊙ 𝑤) ⊗ 𝑥 = 𝑣 ⊗ (𝑤 ⊗ 𝑥) and 𝑣 ⊗ (𝑥 ⊕ 𝑦) = (𝑣 ⊗ 𝑥) ⊕ (𝑣 ⊗ 𝑦),
       • the neutral element 1 is also neutral w.r.t. the scalar multiplication and the neutral element
         0 annihilates, hence for all 𝑣 ∈ 𝑀 and 𝑥 ∈ 𝑊 it is 1 ⊗ 𝑥 = 𝑥 and 𝑣 ⊗ 0 = 0.
  With different choices of monoid-modules, we recover classical and probabilistic programming.
For instance, the angelic Boolean monoid-module embeds Boolean best-case reasoning:
            Angelic Boolean:             Mbool = (B, ∧, true)        and     Wbool = (B, ∨, false, ∧) ,
where at least one trace (⊕ = ∨) is true (⊙ = ⊗ = ∧). We embed probabilistic reasoning via:
                 Probability:           Mprob = (R ≥0, ·, 1)      and              ≥0, +, 0, ·) ,
                                                                         Wprob = (R∞
i.e. the monoid multiplies (finite) non-negative reals via the standard multiplication and the module
adds them via the standard addition, where 1 = 1 and 0 = 02 . Each step of the execution trace may
be weighted by a finite value from R ≥0 , and the total weight may even be infinite (from R∞   ≥0 ).
   The tropical monoid-module is often used to reason about optimization problems, where different
actions are possible, choosing between actions corresponds to taking the action with the minimal
costs, and taking several actions corresponds to taking the sum of their costs.
                 Tropical:         Mtrop = (N∞, +, 0)         and    Wtrop = (N∞, min, ∞, +) ,
   One can also capture traces of program executions as words over an alphabet Γ. The formal
languages monoid-module allows scalar multiplication with (finite) words from Γ ∗ , with the module
operating on possibly infinite words from 2Γ . With · denoting concatenation of words, and 𝜖 being
                                            ∞


the empty word:
                                                                             Wlang = (2Γ , ∪, ∅, ·) .
                                                                                           ∞
              Formal languages:              Mlang = (Γ ∗, ·, 𝜖)     and
The additive operation ⊕ induces the following binary relation.
  Definition 2.2 (Natural Order). The natural order on a monoid-module W = (𝑊 , ⊕, 0, ⊗) is a
binary relation ⊑ ⊆ 𝑊 ×𝑊 , where 𝑥 ⊑ 𝑦 if and only if there exists an element 𝑧 ∈ 𝑊 with 𝑥 ⊕ 𝑧 = 𝑦.

2 Throughout this paper, we use the convention 0 · ∞ = 0 and 𝑥 · ∞ = ∞ for 𝑥 > 0.
Towards a Verification Infrastructure for wGCL                                                                     5



         𝑎 → 𝑛 | 𝑥 | 𝑎 + 𝑎 | 𝑎 · 𝑎 | 𝑎 −¤ 𝑎                     𝐶 → 𝑥 := 𝑎 | 𝐶 1 # 𝐶 2 | ⊗ 𝑚
        𝑏 → 𝑎 < 𝑎 | ¬𝑏 | 𝑏 ∧ 𝑏                                    | if ( 𝑏 ) { 𝐶 1 } else { 𝐶 2 }
        𝑚 → 𝑣 | 𝑚 ⊙ 𝑚 | ⟨𝑏⟩ · 𝑚 | 𝑚𝑎                                 |   while ( 𝑏 ) { 𝐶 1 } | { 𝐶 1 } ⊕ { 𝐶 2 }

Fig. 3. Syntax of expressions and wGCL programs, with 𝑥 ∈ Vars, 𝑛 ∈ N, 𝑣 ∈ 𝑀, 𝐶 1, 𝐶 2 ∈ wGCL, 𝑎 ∈ AExp,
𝑏 ∈ BExp, and 𝑚 ∈ MExp.


   The natural order on the probability module Wprob is the standard order on the reals, since 𝑎 ⊑ 𝑏
if and only if 𝑎 +𝑐 = 𝑏 for some 𝑐 ∈ R∞≥0 if and only if 𝑎 ≤ 𝑏 for all 𝑎, 𝑏 ∈ R ≥0 . On the tropical module
                                                                               ∞

Wtrop , the natural order ⊑ is the reversed standard order ≥ on the extended natural numbers N∞ .
For 𝑥, 𝑦 ∈ N∞ , 𝑥 ⊑ 𝑦 if and only if there exists an element 𝑧 ∈ N∞ such that 𝑥 ⊕ 𝑧 = 𝑥 min 𝑧 = 𝑦 if
and only if 𝑥 ≥ 𝑦. It follows, e.g., that ∞ ⊑ 20 ⊑ 0, ∞ is the smallest element, and 0 the largest.
 Definition 2.3 (𝜔-Continuous Monoid-Module). A module W = (𝑊 , ⊕, 0, ⊗) over the monoid
M = (𝑀, ⊙, 1) is 𝜔-continuous, if
   • the natural order is a partial order (reflexive, transitive, and antisymmetric),Ãa least element
      ⊥ ∈ 𝑊 exists, and every 𝜔-ascending chain (𝑥𝑖 )𝑖 ∈N ⊆ 𝑊 has a supremum 𝑖 ∈N 𝑥𝑖 ∈ 𝑊 ,3
   • scalar multiplication and addition are 𝜔-continuous; for every 𝜔-ascending chain (𝑥𝑖 )𝑖 ∈N ⊆
      𝑊 and element 𝑦 ∈ 𝑀, it is
                     Ä       Ä                                Ä        Ä
                 𝑦⊗     𝑥𝑖 =     (𝑦 ⊗ 𝑥𝑖 )      and      𝑦⊕       𝑥𝑖 =     (𝑦 ⊕ 𝑥𝑖 ).
                            𝑖 ∈N      𝑖 ∈N                                𝑖 ∈N       𝑖 ∈N

  We want to support both lower- and upper-bound reasoning, so we require 𝜔-bicontinuous
monoid modules, which satisfy both 𝜔-continuity and 𝜔-cocontinuity. The latter is continuity with
respect to the reversed natural order ⊒4 . All our monoid-modules are 𝜔-bicontinuous (Section F).

2.2    Syntax and Semantics of wGCL
The syntax of wGCL is standard imperative programming with a weigh statement ⊗ 𝑚 , which
weighs branches with the monoid multiplication ⊗, and a branching statement { 𝐶 1 } ⊕ { 𝐶 2 }.
  Definition 2.4 (Syntax of wGCL). For an 𝜔-continuous module W over the monoid M and a
countable set of variables Vars ranging over the natural numbers N, the set wGCL of weighted
programs is constructed by the grammar in Figure 3.
   Programs in wGCL operate on program states Σ = {𝜎 : Vars → N | supp(𝜎) is finite}, i.e.
functions mapping variables to natural numbers with finite support. The semantics J𝑎K : Σ → N for
arithmetic expressions and J𝑏K : Σ → {0, 1} for Boolean expressions are standard (c.f. Figure 14). In
particular, −¤ denotes the truncated subtraction, which is defined as J𝑎 −¤ 𝑎 ′ K(𝜎) = max{0, J𝑎K(𝜎) −
J𝑎 ′ K(𝜎)} for all 𝜎 ∈ Σ. Monoid expressions 𝑚 describe elements of monoid M and have semantics
J𝑚K : Σ → M with J𝑣K(𝜎) = 𝑣, J𝑚 ⊙ 𝑚 ′ K(𝜎) = J𝑚K(𝜎) ⊙ J𝑚 ′ K(𝜎). ⟨𝑏⟩ · 𝑚 is a conditional monoid
expression, which evaluates to J𝑚K(𝜎) if J𝑏K(𝜎) is true and to 1 otherwise. The expression 𝑚𝑎
denotes the J𝑎K(𝜎)-fold monoid multiplication of J𝑚K(𝜎).
   A program execution starts in some state 𝜎 ∈ Σ with the neutral weight 1 ∈ M. With the
assignment 𝑥 := 𝑎, we update a variable 𝑥 ∈ Vars to an arithmetic expression 𝑎 in a given program
state 𝜎 ∈ Σ by 𝜎 [𝑥 ↦→ 𝑎] = 𝜆𝑦. if 𝑦 = 𝑥 then J𝑎K(𝜎) else 𝜎 (𝑦). When weighing with ⊗ 𝑚 , the
3 This defines exactly an 𝜔-complete partial order.
4 The reversed natural order ⊒ is defined as 𝑥 ⊒ 𝑦 if and only if 𝑦 ⊑ 𝑥 for all 𝑥, 𝑦 ∈ W.
6                                                                                      Ahrens, Rode, Schröer, and Katoen


    𝐶                               wpJ𝐶K(𝑓 )                                  wlpJ𝐶K(𝑓 )
    𝑥 := 𝑎                          𝑓 [𝑥 ↦→ 𝑎]                                 𝑓 [𝑥 ↦→ 𝑎]
    𝐶1 # 𝐶2                         wpJ𝐶 1 K(wpJ𝐶 2 K(𝑓 ))                     wlpJ𝐶 1 K(wlpJ𝐶 2 K(𝑓 ))
    if ( 𝑏 ) { 𝐶 1 } else { 𝐶 2 }   [𝑏] · wpJ𝐶 1 K(𝑓 ) ⊕ [¬𝑏] · wpJ𝐶 2 K(𝑓 )   [𝑏] · wlpJ𝐶 1 K(𝑓 ) ⊕ [¬𝑏] · wlpJ𝐶 2 K(𝑓 )
    { 𝐶1 } ⊕ { 𝐶2 }                 wpJ𝐶 1 K(𝑓 ) ⊕ wpJ𝐶 2 K(𝑓 )                wlpJ𝐶 1 K(𝑓 ) ⊕ wlpJ𝐶 2 K(𝑓 )
    ⊗𝑚                              𝑚⊗𝑓                                        𝑚⊗𝑓
    while ( 𝑏 ) { 𝐶 1 }             lfp 𝑋 . [¬𝑏] · 𝑓 ⊕ [𝑏] · wpJ𝐶 1 K(𝑋 )      gfp 𝑋 . [¬𝑏] · 𝑓 ⊕ [𝑏] · wlpJ𝐶 1 K(𝑋 )
                                            |           {z             }               |             {z              }
                                                      = Φ 𝑓 (𝑋 )                                  = Ψ𝑓 (𝑋 )


Fig. 4. The iterative definition of the weakest (liberal) preweightings w(l)pJ𝐶K(𝑓 ) for 𝐶 ∈ wGCL and 𝑓 ∈ W.


previous weight is multiplied by J𝑚K(𝜎) for the program state 𝜎 ∈ Σ. The branching statement
{ 𝐶 1 } ⊕ { 𝐶 2 } combines the weights of the branches 𝐶 1 and 𝐶 2 by the module addition ⊕.
   Example 2.5. Recall the ski rental example (Figure 1a), defined on the tropical module Wtrop over
the monoid Mtrop . Each iteration of the loop in state 𝜎 and with current weight 𝑚 ∈ M chooses
the minimum cost (⊕ = min) of either renting skis for a day at a cost of 1 (left branch) or buying
skis for a cost of 𝑐 (right branch). When renting, the new weight is 1 ⊗ 𝑤 = 1 + 𝑤 and the new state
is 𝜎 [𝑥 ↦→ 𝑥 + 1]. When buying, the new weight is 𝑐 ⊗ 𝑤 = 𝑐 + 𝑤 with new state 𝜎 [𝑥 ↦→ 0].
   For the CAS counter example (Figure 1b), we use the monoid-module of formal languages Wlang
over the alphabet {𝑆𝑖 , 𝐹𝑖 | 𝑖 ∈ N}. Each of the two if-branches corresponds to either successful or
unsuccessful CAS operations, and we weigh the branches with either the success word 𝑆𝑖 or failure
word 𝐹𝑖 for thread 𝑖. Therefore, the weight of a program execution is an infinite word representing
the sequence of successful and unsuccessful CAS operations. Full operational semantics can be
found in Section A.1.

2.3     Weakest (Liberal) Preweightings
We reason about weights of program executions via weightings.
  Definition 2.6 (Weighting). For a monoid-module W and a set of variables Vars, a weighting
𝑓 ∈ W = { Σ → 𝑊 } maps each program state to an element, called weight, in the module.
    For a fixed 𝜔-bicontinuous module W over the monoid M, the set W of weightings is also an
𝜔-bicontinuous module over M, since all properties are lifted pointwise. The Iverson bracket [𝑏]
filters weightings to states satisfying the Boolean expression 𝑏. Let 𝑓 ∈ W and 𝜎 ∈ Σ. Then:
                                                    (
                                                      𝑓 (𝜎), if J𝑏K(𝜎),
                                  ( [𝑏] · 𝑓 ) (𝜎) =
                                                      0,     otherwise.
Substitution of a variable 𝑥 ∈ Vars by an arithmetic expression 𝑎 in a weighting 𝑓 ∈ W is given by
𝑓 [𝑥 ↦→ 𝑎] = 𝜆𝜎.𝑓 (𝜎 [𝑥 ↦→ 𝜎 (𝑎)]). We reason about weighted programs using weakest preweight-
ings [7], which are the generalization of classical weakest preconditions [15] and probabilistic
weakest preexpectations [29] to the setting of weighted programs. They are defined recursively
over the program structure, with both a non-liberal and liberal variant.
  Definition 2.7 (Weakest Preweightings). For an 𝜔-continuous module W over monoid M and
program 𝐶 ∈ wGCL, the weakest (liberal) preweightings wpJ𝐶K, wlpJ𝐶K : (W → W) are defined in
Figure 4.
Towards a Verification Infrastructure for wGCL                                                        7


    The rules in Figure 4 define wpJ𝐶K(𝑓 ) for a program 𝐶 ∈ wGCL and weighting 𝑓 ∈ W by
propagating 𝑓 backwards through the program. Because 𝑓 is evaluated at the end of the program,
it is called a postweighting, and wpJ𝐶K(𝑓 ) is called a preweighting.
    Assignments substitute the assigned expression into the postweighting, while sequential compo-
sition composes transformers in reverse program order, yielding wpJ𝐶 1 K(wpJ𝐶 2 K(𝑓 )) for 𝐶 1 # 𝐶 2 .
Conditionals select the corresponding branch pointwise: states satisfying 𝑏 use wpJ𝐶 1 K(𝑓 ), and
states satisfying ¬𝑏 use wpJ𝐶 2 K(𝑓 ). Branching combines the two branch preweightings by the mod-
ule addition ⊕, and a weighing statement ⊗ 𝑚 scalar-multiplies the postweighting by the monoid
expression 𝑚. Loops while ( 𝑏 ) { 𝐶 1 } are interpreted as the least fixed point of the characteristic
function Φ 𝑓 (𝑋 ) = [¬𝑏] · 𝑓 ⊕ [𝑏] · wpJ𝐶 1 K(𝑋 ), which exists by 𝜔-continuity and Kleene’s fixed-point
theorem [7]. The liberal transformer wlpJ𝐶K(𝑓 ) is analogous, except that loops use the greatest
fixed point of the function Ψ𝑓 (𝑋 ) = [¬𝑏] · 𝑓 ⊕ [𝑏] · wlpJ𝐶 1 K(𝑋 ).
    The resulting difference in both transformers is that wpJ𝐶K(𝑓 ) collects the weights of all ter-
minating executions with 𝑓 evaluated the final state, while wlpJ𝐶K(𝑓 ) additionally collects the
weights of all non-terminating executions.
  Example 2.8. Recall the Ski rental problem (Figure 1a) over the tropical monoid-module Wtrop . For
the loop body 𝐶 ′ , we obtain the weakest preweighting wpJ𝐶 ′ K(𝑓 ) = 1⊗ 𝑓 [𝑛 ↦→ 𝑛 − 1] ⊕𝑐 ⊗ 𝑓 [𝑛 ↦→ 0].
The characteristic function of the loop is Φ 𝑓 (𝑋 ) = [𝑛 = 0]·𝑓 ⊕[𝑛 > 0]·(1⊗𝑋 [𝑛 ↦→ 𝑛 − 1]⊕𝑐 ⊗𝑋 [𝑛 ↦→
0]). One can prove that the least fixed point evaluates to 𝑛 ⊕ 𝑦.
   Theorem 2.9 ([7]). The weighting transformer wpJ𝐶K(·) is a well-defined, 𝜔-continuous function.
In particular, the least fixed point of the function Φ exists for all 𝑓 ∈ W and 𝐶 ∈ wGCL.
  Analogously, we define weakest liberal preweightings for 𝜔-cocontinuous modules W, see
Definition A.7 and Theorem A.8 on Pages 30 and 31.

3     Heyting (Co-)Implications for Totally Ordered and Boolean Algebras
Central to the specifications and proofs in the weakest preweighting calculi are comparisons between
weightings. In addition, we need to express assumptions during proofs, e.g. assuming that a certain
precondition holds, or that some value is bounded by a certain threshold. We use Heyting algebras
to internalize the comparison and assumption operations in the logic, which give us quantitative
implications and dual co-implications. Although HeyLo and HeyVL of prior work [33] define
quantitative (co-)implications, they only do so for the specific setting of probabilistic programs
(corresponding to Wprob ). Here, we generalize to more general 𝜔-bicontinuous monoid-modules.
   In the following, we define instances of Heyting algebras for (1) totally ordered lattices, (2)
Boolean algebras, and (3) the specific setting of the why semiring Wwhy . Figure 5 gives an overview
of the different monoid-modules and their corresponding (co-)implications.

3.1    Heyting Algebras
In our setting, we consider monoid-modules that are bounded lattices5 and equip them with an
implication. This yields a Heyting algebra, where the implication 𝑎 → (·) : 𝐻 → 𝐻 is right adjoint
to the meet 𝑎 ⊓ (·) : 𝐻 → 𝐻 .
  Definition 3.1 (Bi-Heyting Algebra). A Heyting algebra H = (𝐻, ⊑, ⊓, ⊔, →) is a bounded lattice
(𝐻, ⊑) together with an implication →: 𝐻 × 𝐻 → 𝐻 such that for all 𝑎, 𝑏, 𝑥 ∈ 𝐻 ,
                                        (𝑎 ⊓ 𝑥) ⊑ 𝑏        iff      𝑥 ⊑ (𝑎 → 𝑏).

5 In a bounded lattice (𝐻, ⊑), for all 𝑎 ∈ 𝐻 , we have ⊥ ⊑ 𝑎 ⊑ ⊤.
8                                                                                                      Ahrens, Rode, Schröer, and Katoen




                                 trop          nats     prob           clear           bool         lang          why
       weightings W: Σ→W
        map into module W




                                                                                                     2Γ
                                                                                                           ∞
                            𝑊    N∞            N∞        R∞
                                                          ≥0       {P, C, S, TS}       {0, 1}                   pDNF
                            ⊕    min            +         +             min              ∨            ∪            ∨
                            0     ∞             0          0             TS              0            ∅             0
                            ⊗     +             ·          ·            max              ∧             ·           ∧

                                 N∞                                {P, C, S, TS}       {0, 1}         Γ∗
        weights from




                            𝑀                   N        R ≥0                                                   pDNF
         monoid M




                            ⊙     +             ·          ·            max              ∧             ·           ∧
                            1      0            1          1                 P           1            𝜀             1

                            ⊑     ≥             ≤         ≤                  ≥           ≤            ⊆            ≤
                            ⊥     ∞             0          0                             0            ∅             0
    𝜔 −bicomplete




                                                                         TS
     partial order
     bounds via




                            ⊤      0            ∞         ∞                  P           1           Γ∞             1
                            ⊓    max           min       min            max              ∧            ∩            ∧
                            ⊔    min           max       max            min              ∨            ∪            ∨
       comparison via
       Heyting algebra




                                 totally    totally      totally        totally        Boolean      Boolean       finite
                                ordered    ordered      ordered        ordered         algebra      algebra    distributive
                            →    →tot          →tot     →tot            →tot           →bool        →bool      →pDNF
                            ←    ←tot          ←tot     ←tot            ←tot           ←bool        ←bool      ←pDNF
                                           (                       )                            (                       )
                                       ⊤,             if 𝑎 ⊑ 𝑏,                             ⊥,             if 𝑏 ⊑ 𝑎,
                            𝑎 →tot 𝑏 =                                           𝑎 ←tot 𝑏 =
                                       𝑏,             otherwise                             𝑏,             otherwise
                            𝑎 →bool 𝑏 = ¬𝑎 ⊔ 𝑏                                   𝑎 ←bool 𝑏 = ¬𝑎 ⊓ 𝑏

Fig. 5. An overview over 𝜔-bicontinuous monoid-modules that are bi-Heyting algebras. All instances from
Table 1 in [7] for weighted programming reappear, though extended by the Heyting (co-)implications.
For clear, 𝑃 < 𝐶 < 𝑆 < 𝑇 𝑆 and the displayed order ≥ is the natural order induced by min. For lang,
                       ∞
Γ ∞ = Γ ∗ ∪ Γ𝜔 , 𝐿 ∈ 2Γ is a language of finite and infinite words, 𝑔 ∈ Γ ∗ is a finite word, and 𝑔 ·𝐿 = {𝑔 ·𝑙 | 𝑙 ∈ 𝐿}.
For why, pDNF denotes positive DNF formulae over a finite set of variables, ordered by semantic implication;
→pDNF and ←pDNF are the residuals of this finite distributive lattice.


For every 𝑎 ∈ 𝐻 , let ¬𝑎 := 𝑎 → ⊥ be the Heyting negation. The dual structure H = (𝐻, ⊑, ⊓, ⊔, ←)
is a co-Heyting algebra with the co-implication ←: 𝐻 × 𝐻 → 𝐻 such that for all 𝑎, 𝑏, 𝑥 ∈ 𝐻 ,
                                                    𝑏 ⊑ (𝑎 ⊔ 𝑥)        iff       (𝑎 ← 𝑏) ⊑ 𝑥 .
For every 𝑎 ∈ 𝐻 , let ∼𝑎 := 𝑎 ← ⊤ be the co-negation. A Heyting algebra which is also a co-Heyting
algebra is called a bi-Heyting algebra.
   The following algebraic form of the deduction theorem [25] allows us to internalize comparisons
in the logic via the implication → and co-implication ←.
Towards a Verification Infrastructure for wGCL                                                          9


   Theorem 3.2 (Deduction Theorem). Let H be a bi-Heyting algebra and 𝑎, 𝑏 ∈ 𝐻 . Then, we have
                    𝑎 ⊑ 𝑏      iff 𝑎 → 𝑏 = ⊤      and      𝑎 ⊒ 𝑏     iff 𝑎 ← 𝑏 = ⊥.
  With the Boolean embedding ? (·) : B → 𝐻 that maps true to ⊤ and false to ⊥, we can internalize
the Boolean comparison → and ← in the logic as well and even encode if-else statements.
   Lemma 3.3. Let H be a bi-Heyting algebra. For all 𝑏 ∈ B and 𝑥 ∈ 𝐻 , we have
                         (                                          (
                           𝑥, if 𝑏                                    𝑥, if ¬𝑏
             ? (𝑏) → 𝑥 =                       and      ? (𝑏) ← 𝑥 =
                           ⊤, otherwise                               ⊥, otherwise
   Example 3.4 (Ternary Conditionals). Let H = (𝐻, ⊑, ⊓, ⊔, →) be a Heyting algebra and 𝑐 ∈ B.
Then, for all 𝑎, 𝑏 ∈ 𝐻 , we have ( ? (𝑐) → 𝑎) ⊓ ( ? (¬𝑐) → 𝑏) = if 𝑐 then 𝑎 else 𝑏. Dually, for co-Heyting
algebra H = (𝐻, ⊑, ⊓, ⊔, ←), we have ( ? (𝑐) ← 𝑎) ⊔ ( ? (¬𝑐) ← 𝑏) = if 𝑐 then 𝑏 else 𝑎.
  Instead of using a Boolean embedding, we want to express qualitative properties directly via
our bi-Heyting algebra. To use proof rules such as Park induction, we need to check whether a
certain entailment holds. To connect the quantitative domain H with qualitative reasoning, we
define validation and covalidation operators that "booleanize" statements by mapping them to the
extreme values ⊥ and ⊤ of the bi-Heyting algebra.
  Definition 3.5 (Validation and Covalidation). Let H = (𝐻, ⊑, ⊓, ⊔, →) be a Heyting algebra with
𝑥 ∈ 𝐻 , then we define the validation △(𝑥) and covalidation ▽(𝑥) as follows:
                            (                                (
                              ⊤, if 𝑥 = ⊤                      ⊥, if 𝑥 = ⊥
                    △(𝑥) =                     and ▽(𝑥) =
                              ⊥, otherwise                     ⊤, otherwise .
   To obtain direct definitions of Heyting (co-)implications for totally ordered lattices, Boolean
algebras, and the why semiring Wwhy , the following characterization helps.
  Lemma 3.6 (Residual Characterization of (Co-)Implication). Let (𝐻, ⊑) be a bounded lattice.
Then, the following statements are equivalent:
   (1) There exists an implication → suchÃthat (𝐻, ⊑, ⊓, ⊔, →) is a Heyting algebra.
   (2) For every 𝑎, 𝑏 ∈ 𝐻 , the supremum {𝑥 ∈ 𝐻 | 𝑎 ⊓ 𝑥 ⊑ 𝑏} is well-defined.
                                                        Ã
Then, we derive that the Heyting implication is 𝑎 → 𝑏 = {𝑥 ∈ 𝐻 | 𝑎 ⊓ 𝑥 ⊑ 𝑏} for all 𝑎, 𝑏 ∈ 𝐻 .
   Dually, the Heyting co-implication can be characterized as the least element satisfying 𝑏 ⊑ 𝑎 ⊔ 𝑥.
These extrema exist since the greatest (least) element of a subset of a partially ordered set is always
its supremum (infimum).

3.2   Totally Ordered Bounded Lattices
HeyLo from [33] extends the probability module Wprob by the Gödel implications to obtain a
bi-Heyting algebra. We generalize those implications for any totally ordered bounded lattice (𝐻, ⊑),
which yields a bi-Heyting algebra with the (co-)implications →tot and ←tot .
   Lemma 3.6 provides a constructive characterization of the implications and, since 𝐻 is totally
ordered and bounded, we derive that the greatest element 𝑥 ∈ 𝐻 such that 𝑎 ⊓ 𝑥 ⊑ 𝑏 holds is either
⊤, if 𝑎 ⊑ 𝑏, or 𝑏, otherwise. A dual construction works for the co-implication.
  Theorem 3.7. For any totally ordered bounded lattice (𝐻, ⊑), we obtain a bi-Heyting algebra
H = (𝐻, ⊑, ⊓, ⊔, →tot, ←tot ), with the (co-)implications
                          (                   )                  (              )
                             ⊤, if 𝑎 ⊑ 𝑏,                          ⊥, if 𝑏 ⊑ 𝑎,
              𝑎 →tot 𝑏 =                          and 𝑎 ←tot 𝑏 =                  .
                             𝑏, otherwise                         𝑏, otherwise
10                                                                                     Ahrens, Rode, Schröer, and Katoen


 The extended naturals module Wnats , the tropical semiring Wtrop , and the probability module
Wprob are totally ordered bounded lattices, hence we use the previous implications in this work.
   Example 3.8. For the probability module Wprob , this yields the Gödel implication 𝑎 →tot 𝑏 = ∞,
if 𝑎 ≤ 𝑏, and 𝑎 →tot 𝑏 = 𝑏, otherwise. This yields, e.g., 4 →tot 5 = ∞ and 5 →tot 4 = 4. The
natural order of the tropical semiring Wtrop is reversed, hence we obtain 𝑎 →tot 𝑏 = 0 if 𝑎 ≥ 𝑏 and
𝑎 →tot 𝑏 = 𝑏, otherwise. Then, we have 4 →tot 5 = 5 and 5 →tot 4 = 0.

3.3    Boolean Algebras
A second source of Heyting algebras are Boolean algebras. Unlike general Heyting algebras, where
negation is only a pseudo-complement, Boolean algebras require that for every element 𝑎 an
additive inverse ¬𝑎 exists, satisfying 𝑎 ⊓ ¬𝑎 = ⊥ and 𝑎 ⊔ ¬𝑎 = ⊤.
  By the characterization in Lemma 3.6, 𝑎 →bool 𝑏 is the greatest element 𝑥 ∈ 𝐻 such that 𝑎 ⊓𝑥 ⊑ 𝑏.
The candidate ¬𝑎 ⊔ 𝑏 satisfies 𝑎 ⊓ (¬𝑎 ⊔ 𝑏) = (𝑎 ⊓ ¬𝑎) ⊔ (𝑎 ⊓ 𝑏) = 𝑎 ⊓ 𝑏 ⊑ 𝑏. This motivates the
material implication 𝑎 →bool 𝑏 = ¬𝑎 ⊔ 𝑏 from classical logic.
   Theorem 3.9. For any Boolean algebra (𝐻, ⊑, ¬) with ⊓ and ⊔ defined, we obtain a bi-Heyting
algebra H = (𝐻, ⊑, ⊓, ⊔, →bool, ←bool ) with 𝑎 →bool 𝑏 = ¬𝑎 ⊔ 𝑏 and 𝑎 ←bool 𝑏 = ¬𝑎 ⊓ 𝑏.
   Example 3.10. Instances of Boolean algebras are the Boolean module Wbool 6 and the formal
languages module Wlang for any alphabet Γ. For the Boolean module, the material implication is
the standard Boolean implication, e.g., (true →bool false) = false and (false →bool true) = true.
For the formal languages module, the material implication is the set-theoretic implication, e.g.,
({𝑎, 𝑏} →bool {𝑏, 𝑐}) = {𝑏, 𝑐} and ({𝑎, 𝑏} →bool {𝑎, 𝑏, 𝑐}) = {𝑎, 𝑏, 𝑐}.

3.4    The Why Module
Not all monoid-modules fall into the previous two categories. One example is the Why module
Wwhy , which tracks provenance of computations, nÔi.e., Ó
                                                        why a certain result was o obtained.
  Let 𝐴 be a finite set of variables and pDNF =    𝑗=1 𝑋 ∈𝐼 𝑗 𝑎 | 𝑛 ≥ 0, 𝐼 𝑗 ⊆ 𝐴
                                                   𝑛
                                                                                    the set of positive
                                                                                                 /≡
formulae in DNF module logical equivalence. We order pDNF by semantic entailment, i.e., 𝑃 ⊑ 𝑄 if
and only if for all 𝜌 : 𝐴 → {0, 1} it is (𝜌 |= 𝑃 implies 𝜌 |= 𝑄).
                     Why:         Mwhy = (pDNF, ∧, 1)          and     Wwhy = (pDNF, ∨, 0, ∧).
Since pDNF is defined modulo logical equivalence over the finite set 𝐴, it is itself finite and forms a
bounded distributive lattice with meet ∧, join ∨, bottom 0, and top 1. It is neither totally ordered,
nor a Boolean algebra, since positive formulae are not closed under negation. For 𝑃, 𝑄 ∈ pDNF,
                                         Ü
                           𝑃 →pDNF 𝑄 =       {𝑅 ∈ pDNF | 𝑃 ∧ 𝑅 ⊑ 𝑄 } .
Since pDNF is finite, this join is well-defined and computable; the order check is entailment over
finitely many valuations. The coimplication ←pDNF is defined dually as the residual of ∨.
 Theorem 3.11. For every finite set of variables 𝐴, the carrier pDNF of the Why monoid-module
Wwhy forms a bi-Heyting algebra (pDNF, ⊑, ∧, ∨, →pDNF, ←pDNF ).
  Indeed, 𝑃 →pDNF 𝑄 is by construction the greatest 𝑅 with 𝑃 ∧ 𝑅 ⊑ 𝑄; hence it is the Heyting
implication by Lemma 3.6, and the co-Heyting implication follows dually.
6 The Boolean module W
                      bool is both a totally ordered lattice and a Boolean algebra, and both Theorems 3.7 and 3.9 yield the
same (co-)implications.
Towards a Verification Infrastructure for wGCL                                                    11


 𝜑            J𝜑K(𝜎) ∈ W                           𝜑           J𝜑K(𝜎) ∈ W
                                                               (
 𝑤 ∈W         𝑤                                                  ⊤, if J𝜑K(𝜎)
                                                   ? (𝑏)
                                                                 ⊥, otherwise
              ÉJ𝑎K (𝜎 )
 𝑎 ·𝜑             𝑖=1     J𝜑K(𝜎)
 𝑚 ⊗𝜑         J𝑚K(𝜎) ⊗ J𝜑K(𝜎)                      𝜑 ⊕𝜓        J𝜑K(𝜎) ⊕ J𝜓 K(𝜎)
 𝜑 ⊓𝜓         J𝜑K(𝜎) ⊓ J𝜓 K(𝜎)                     𝜑 ⊔𝜓        J𝜑K(𝜎) ⊔ J𝜓 K(𝜎)
 𝜑 →𝜓         J𝜑K(𝜎) → J𝜓 K(𝜎)                     𝜑 ←𝜓        J𝜑K(𝜎) ← J𝜓 K(𝜎)
 d            d                                   Ã           Ã
   𝑥𝜑            J𝜑K(𝜎 [𝑥 ↦→ 𝑛]) | 𝑛 ∈ N             𝑥𝜑           J𝜑K(𝜎 [𝑥 ↦→ 𝑛]) | 𝑛 ∈ N
    △(𝜑)      △(𝑤) with J𝜑K(𝜎) = 𝑤                 ▽(𝜑)        ▽(𝑤) with J𝜑K(𝜎) = 𝑤
Table 1. Syntax and semantics of wHeyLo formulae. Cells colored in   and    mark order-dual formula
constructors.



4    Verification Infrastructure for Weighted Programming
In this section, we specify the quantitative assertion language wHeyLo that is parameterized over
𝜔-bicontinuous monoid-modules that are bounded lattices and admit Heyting (co-)implications.
From now on, we consider only modules W over monoids M that meet these prerequisites.
   Furthermore, we define the intermediate verification language wHeyVL which allows us to encode
wGCL programs, assumptions, and proof rules. Its semantics are wHeyLo formulae which are
computable via the verification preweighting transformer vp.
   Definition 4.1 (Quantitative Assertions). The set of wHeyLo formulae is defined by the grammar
in Table 1, where 𝑎 is an arithmetic expression AExp, 𝑏 is a Boolean expression BExp, and 𝑚 is a
monoid expression MExp. The semantics J𝜑K : Σ → W is defined in Table 1. The notation via
Iverson brackets [𝑏] · 𝜑 may be used as syntactic sugar for the wHeyLo formula ? (¬𝑏) ← 𝜑.
  The following theorem ensures that the semantics of wHeyLo formulae are well-defined. The
main challenge here are the supremum and infimum of - seemingly - arbitrary sets, even though
the
 Ã monoid-modules    are only 𝜔-bicontinuous. However, the definition of wHeyLo ensures that
J 𝑥 𝜑K = 𝑖 ∈N 𝑤𝑖 ∈ W exists for an 𝜔-ascending chain (𝑤𝑖 )𝑖 ∈N ⊆ W (and dually for the infimum).
          Ã

  Theorem 4.2. If the module W = (𝑊 , ⊕, 0, ⊗) over the monoid M = (𝑀, ⊙, 1) is 𝜔-bicontinuous
and a bi-Heyting algebra, then the semantics of the wHeyLo formulae are well-defined.
   See Section B for a proof. Two wHeyLo formulae 𝜑 and 𝜓 are equivalent, denoted 𝜑 ≡ 𝜓 , iff
J𝜑K = J𝜓 K. By lifting the natural order of the module pointwise, we obtain 𝜑 ⊑ 𝜓 iff 𝜑 → 𝜓 is valid
and 𝜑 ⊒ 𝜓 iff 𝜑 ← 𝜓 is covalid. The formula 𝜌 ∈ wHeyLo is valid iff 𝜌 ≡ ⊤ and covalid iff 𝜌 ≡ ⊥.
   The intermediate verification language wHeyVL generalizes the HeyVL language presented by
Schröer et al. [33] for probabilistic programs over the probabilistic module Wprob . Intermediate
verification languages are not designed to be executed directly, but allow intermediate represen-
tations that encode proof obligations for programs in an imperative style. wHeyVL is a weighted
language that can be instantiated for various weighted settings.
   wHeyVL statements are closely related to wGCL commands, but extend them with statements
that allow the encoding of proof rules (there are several examples in Section 5). In Table 2, we list
the syntax of wHeyVL, where the first statements have a one-on-one correspondence to statements
in wGCL. The remaining statements are the extensions that allow intermediate reasoning.
12                                                                        Ahrens, Rode, Schröer, and Katoen


 𝐶                   vpJ𝐶K(𝜑)                        𝐶                    vpJ𝐶K(𝜑)

                                                     if (+) { 𝑆 1 }
 𝑥 := 𝑎              𝜑 [𝑥 ↦→ 𝑎]                                           vpJ𝐶 1 K(𝜑) + vpJ𝐶 2 K(𝜑)
                                                     else { 𝑆 2 }
 𝐶 1; 𝐶 2            vpJ𝐶 1 K(vpJ𝐶 2 K(𝜑))           weigh 𝑚             𝑚 ⊗𝜑
 if (⊓) { 𝑆 1 }                                      if (⊔) { 𝑆 1 }
                     vpJ𝐶 1 K(𝜑) ⊓ vpJ𝐶 2 K(𝜑)                            vpJ𝐶 1 K(𝜑) ⊔ vpJ𝐶 2 K(𝜑)
 else { 𝑆 2 }                                        else { 𝑆 2 }
 assert 𝜓            𝜓 ⊓𝜑                            coassert 𝜓          𝜓 ⊔𝜑
 assume 𝜓            𝜓 →𝜑                            coassume 𝜓          𝜓 ←𝜑
                     d                                                   Ã
 havoc 𝑥               𝑥𝜑                            cohavoc 𝑥             𝑥𝜑
 validate            △(𝜑)                            covalidate           ▽(𝜑)
Table 2. Syntax and semantics of wHeyVL. Cells colored in represent primal operators needed for underap-
proximations, while cells in the complementary color represent their dual counterparts for overapproxima-
tions.




   The assignment 𝑥 := 𝑎 assigns the value of an arithmetic expression 𝑎 ∈ AExp to a variable
𝑥 ∈ Vars. Sequential composition 𝐶 1 ; 𝐶 2 executes 𝐶 1 followed by 𝐶 2 and weighted branching
if (+) {𝐶 1 } else {𝐶 2 } executed both substatements and combines them via the additive operation
⊕ of the module. The weighting weigh 𝑚 weighs 𝑚 ∈ MExp via the multiplicative operation ⊗
of the module. Demonic branching if (⊓) {𝐶 1 } else {𝐶 2 } executes either 𝐶 1 or 𝐶 2 , where the
choice is made to minimize the verification preweighting. The assertion assert 𝜓 and assumption
assume 𝜓 generalize classical assertions and assumptions, where 𝜓 is a wHeyLo formula. The havoc
statement havoc 𝑥 assigns an arbitrary value to variable 𝑥 and the validation statement validate
turn quantitative weightings into qualitative ones (c.f. Table 2).
   The previous statements are generally associated with reasoning about lower bounds of the
verification preweighting. Dually, there are the angelic branching if (⊔) {𝐶 1 } else {𝐶 2 }, coasser-
tion coassert 𝜓 , coassumption coassume 𝜓 , cohavoc cohavoc 𝑥, and covalidation covalidate
statements, which are used for over-approximations.
   We specify the semantics via the recursively defined verification preweighting transformer

                          vpJ𝐶K : wHeyLo → wHeyLo for all 𝐶 ∈ wHeyVL

that is again related to the weakest (liberal) preweighting transformers wp and wlp, see Definition 2.7.
Let 𝜑 ∈ wHeyLo be a post. For the assignment statement 𝑥 := 𝑎, the sequential composition
𝐶 1 ; 𝐶 2 , the weighted branching if (+) {𝐶 1 } else {𝐶 2 }, and the weighting weigh 𝑎, the semantics
is defined just like the wp/wlp semantics in wGCL (see Section 2).
    The non-deterministic branchings if (⊓) {𝐶 1 } else {𝐶 2 } and if (⊔) {𝐶 1 } else {𝐶 2 } take the
infimum ⊓ and supremum ⊔ of the semantics of the branches, respectively. The assertion assert 𝜓
takes the infimum ⊓ of the assertion 𝜓 and the post 𝜑, while the assumption statement assume 𝜓
is defined by the implication →. Havoc havoc 𝑥 takes the infimum ⊓ over all possible values
of 𝑥 and the validation statement validate applies the △(·) operator to the post 𝜑. Dually, the
semantics of the angelic branching if (⊔) {𝐶 1 } else {𝐶 2 }, coassert 𝜓 , coassume 𝜓 , cohavoc 𝑥,
and covalidate statements are defined by taking the supremum ⊔, the coimplication ←, the
Towards a Verification Infrastructure for wGCL                                                           13


         Procedure (𝜑 ⊑ vpJ𝐶K(𝜓 ))                               Coprocedure (𝜑 ⊒ vpJ𝐶K(𝜓 ))
       rig proc P (in : 𝜏) -> (out : 𝜏)                        rig coproc P (in : 𝜏) -> (out : 𝜏)
             pre 𝜑                                                  pre 𝜑
             post 𝜓                                                 post 𝜓
       {𝐶 }                                                    {𝐶 }

    Fig. 6. wHeyVL procedures (left) verify lower bounds and coprocedures (right) verify upper bounds.


supremum ⊔ over all possible values of 𝑥, and the ▽(·) operator, respectively. Note that the classical
if-else branching corresponds to if (+) {assume ? (𝑏); 𝐶 1 } else {assume ? (¬𝑏); 𝐶 2 }.
   wHeyVL programs are collections of procedures and coprocedures, which are again dual constructs.
Its syntax is schematically shown in Figure 6 and consists of
      • its signature specifying the weighted instance rig (e.g., trop, bool, or lang), the keyword
         proc or coproc, the name 𝑃, and typed input and output parameters in : 𝜏 and out : 𝜏,
      • its specification via a preweighting 𝜑 ∈ wHeyLo and a postweighting 𝜓 ∈ wHeyLo, and
      • its body 𝐶 ∈ wHeyVL that is a wHeyVLstatement.
Input parameters are read-only and can only be used in the pre 𝜑, post 𝜓 , and body 𝐶, while output
parameters may be written to, but cannot be used in the pre 𝜑.
   A procedure verifies if the pre 𝜑 is a lower bound of the verification preweighting of 𝐶 with
respect to the post 𝜓 . Dually, a coprocedure verifies upper bounds.
  Definition 4.3. Consider the (co)procedures from Figure 6. A procedure 𝑃 (with keyword proc)
verifies iff 𝜑 ⊑ vpJ𝐶K(𝜓 ). A coprocedure 𝑃 (with keyword coproc) verifies iff 𝜑 ⊒ vpJ𝐶K(𝜓 ).
  By the deduction theorem (Theorem 3.2), the verification conditions for procedures and coproce-
dures can be internalized in wHeyLo as ⊤ ≡ 𝜑 → vpJ𝐶K(𝜓 ) and ⊥ ≡ 𝜑 ← vpJ𝐶K(𝜓 ).

5   Proof Rules & Encodings in wHeyVL
In this section, we bridge the gap between the theoretical concept weighted programming and
our verification infrastructure from the previous section. The translation of a loop-free program
𝐶 ∈ wGCL into the verification language wHeyVL is straight-forward and depicted in Figure 7.
For this translation, the following theorem shows that the correspondence between the weakest
(liberal) preweightings and the verification preweightings is exact.
  Theorem 5.1 (Loop-Free Encodings are Exact). For a loop-free program 𝐶 ∈ wGCL and
postweighting 𝜑 ∈ wHeyLo, we have, for all 𝜎 ∈ Σ, that vpJenc(𝐶)K(𝜑) (𝜎) = wpJ𝐶K(𝜑) (𝜎).
   For loop-free wGCL constructs, wp and wlp coincide. However, there exists no direct translation
for programs with loops. We consider common proof rules, like e.g. Park induction [7] and 𝜅-
induction [6]. Furthermore, we modify Park induction and 𝜅-induction to corresponding local proof
rules that disregard variables that are not altered during the execution of the loop. With those
modified proof rules, we can use more invariants to show lower (resp. upper) bounds. Then, we
give the encoding of the premises into wHeyVL-programs, which allows the calculation of lower
(resp. upper) bounds of the weakest (liberal) preweightings. Every proof rule in this section has a
version that verifies a lower bound and uses procedures. Every rule also has a dual version that
verifies an upper bound, uses coprocedures, and dual statements, which we omit for brevity. We
write 𝜓 instead of J𝜓 K and vpJ·K(·) (𝜎) instead of JvpJ·K(·)K(𝜎) for all 𝜓 ∈ wHeyLo and 𝜎 ∈ Σ.
14                                                                        Ahrens, Rode, Schröer, and Katoen



 𝐶                            enc(𝐶)                  = encco (𝐶)         specEnc(𝛽 : [𝜌,𝜓 ])
 𝑥 := 𝐸                       𝑥 := 𝐸                                      assert 𝜌;           (filter for 𝜌)
 ⊗𝑎                           weigh 𝑎                                     havoc 𝛽;
 𝐶1 # 𝐶2                      enc(𝐶 1 ); enc(𝐶 2 )                             (quantify modified states)
 { 𝐶1 } ⊕ { 𝐶2 }              if (+) {enc(𝐶 1 )} else {enc(𝐶 2 )}
                                                                          validate;
 if (𝑏) {𝐶 1 }                if (⊓) {assume ? (𝑏); enc(𝐶 1 )}
                                                                                    (booleanize the check)
    else {𝐶 2 }                  else {assume ? (¬𝑏); enc(𝐶 2 )}
 while ( 𝑏 ) { 𝐶 1 }          (without translation)                       assume 𝜓 (entailment check)

Fig. 7. Translation of loop-free wGCL statements into wHeyVL and encoding of the specification statement
for states 𝛽 ⊆ Vars and weightings 𝜌,𝜓 ∈ wHeyLo.


5.1     Specification Statements
Before considering proof rules for loops, we look at the encoding of specification statements [30]
in wHeyVL. Intuitively, such a statement represents a block of code by specifying a preweighting,
a postweighting, and which variables are changed during the execution. Therefore, they enable
implementation abstraction; instead of a concrete implementation, specification statements describe
a program by their effects. This is key to modular verification, where we verify components of
a program separately and then analyse the derived specification statements to verify the whole
program. Furthermore, they give rise to program refinement, where we start with specification
statements and incrementally refine them into concrete implementations.
   Definition 5.2. Let 𝛽 ⊆ Vars, 𝜌,𝜓 ∈ wHeyLo. The (under-approximating) specification statement
𝛽 : [𝜌,𝜓 ] is a placeholder for the set of all wHeyVL programs 𝐶 that modify only variables in 𝛽 and
satisfy 𝜌 ⊑ vpJ𝐶K(𝜓 ).
  To achieve a desired post 𝜑 ∈ wHeyLo using the specification 𝛽 : [𝜌,𝜓 ], two conditions must be
met. First, the pre 𝜌 must hold in the initial state. Second, the specification’s post 𝜓 must be strong
enough to guarantee 𝜑 after arbitrarily changing the variables in 𝛽 while leaving all other variables
untouched. The set 𝛽 contains all local variables and, starting in an initial state 𝜎 ∈ Σ, the following
definition gives us an over-approximation of all states reachable by modifying the local variables.
     Definition 5.3 (𝛽-Reachable States). For any state 𝜎 ∈ Σ and any 𝛽 ⊆ Vars, we define
                        Reach𝛽 (𝜎) = {𝜎 ′ ∈ Σ | ∀𝑣 ∈ Vars \ 𝛽 : 𝜎 (𝑣) = 𝜎 ′ (𝑣)}.
  Now, the previous intuition translates directly into a wHeyVL encoding. We first assert that
the pre 𝜌 is a lower bound. Then, arbitrary changes to the local variables 𝛽 are mimicked by havoc
and validate booleanizes the result. Finally, we can assume that the postcondition 𝜓 holds.
   Lemma 5.4 (Semantics). For 𝛽 ⊆ Vars and 𝜌,𝜓, 𝜑 ∈ wHeyLo, and 𝜎 ∈ Σ, the specification
statement encoding specEnc(𝛽 : [𝜌,𝜓 ]) given in Figure 7 satisfies
                                          (
                                            𝜌 (𝜎), if 𝜓 (𝜎 ′ ) ⊑ 𝜑 (𝜎 ′ ) ∀𝜎 ′ ∈ Reach𝛽 (𝜎)
        vpJspecEnc(𝛽 : [𝜌,𝜓 ])K(𝜑) (𝜎) =                                                    .
                                            ⊥,     otherwise
     By applying vp sequentially, we derive
                                                                                    l
        vpJassert 𝜌K(vpJhavoc 𝛽K(vpJvalidateK(vpJassume 𝜓 K(𝜑)))) = 𝜌 ⊓                 △(𝜓 → 𝜑) ,
                                                                                    𝛽
Towards a Verification Infrastructure for wGCL                                                                         15



  specEncco (𝛽 : [𝜌,𝜓 ] ⊒ )                                                                     parkEnc(𝐶, 𝛽, 𝐼 ) =




                                                                         (𝛽 : [𝐼, 𝐼 ])
                                                                          specEnc
  coassert 𝜌; cohavoc 𝛽; covalidate; coassume 𝜓                                                 assert 𝐼 ; havoc 𝛽;
                                                                                                validate; assume 𝐼 ;
  charEnc(𝐶, 𝐼 )
                                                                                                if (𝑏) {
  if (𝑏) {




                                                                               charEnc(𝐶, 𝐼 )
                                                                                                  enc(𝐶);
      enc(𝐶);        (encoding of loop body)
                                                                                                  assert 𝐼 ;
      assert 𝐼 ;         (filter for invariant)
                                                                                                  assume ? (false);
      assume ? (false);      (establish truth)
                                                                                                } else {}
   } else {}

Fig. 8. Encoding of the specification statement, the characteristic function, and Park induction for variables
𝛽 ⊆ Vars, weightings 𝜌,𝜓 ∈ wHeyLo, loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, and invariant 𝐼 ∈ wHeyLo.


where assume evaluates to ⊤, if 𝜓 ⊑ 𝜑, and 𝜓 , otherwise. Due to validate, this yields ⊤, if
𝜓 ⊑ 𝜑, and ⊥, otherwise. The statement havoc checks this condition for all states in Reach𝛽 (𝜎)
and assert filters for 𝜌 (see Section C.1). The soundness theorem below states that the encoding
specEnc(𝛽 : [𝜌,𝜓 ]) under-approximates the semantics of any statement that satisfies the respective
specification.
  Theorem 5.5 (Soundness). Let 𝛽 ⊆ Vars, 𝜌,𝜓 ∈ wHeyLo, and 𝐶 ∈ wHeyVL be a statement
that only modifies variables in 𝛽 and satisfies 𝜌 ⊑ vpJ𝐶K(𝜓 ). Then, for all 𝜑 ∈ wHeyLo, we have
vpJspecEnc(𝛽 : [𝜌,𝜓 ])K(𝜑) ⊑ vpJ𝐶K(𝜑).
  The proof follows directly from Lemma 5.4 and the monotonicity of the wHeyVL semantics.
  We specify over-approximating specification statements 𝛽 : [𝜌,𝜓 ] ⊒ , where we consider upper
bounds and vpJ𝐶K(𝜓 ) ⊑ 𝜌 holds. The corresponding encoding specEncco (𝛽 : [𝜌,𝜓 ] ⊒ ) is obtained
by substituting all statements in specEnc(·) by their dual co-statements, see Figure 8. The semantics,
the soundness theorem, and the corresponding proofs are exactly dual.

5.2   Finite Loop Unrolling
While the encoding of loop-free programs is straightforward, we do not have an exact encoding of
programs with loops. We can, however, approximate loops by proof rules. This leads us to the first
proof rule finite loop unrolling. We can literally unroll a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL once,
twice, or more times and approximate it via
                          if ( 𝑏 ) { 𝐶 ′ },      if ( 𝑏 ) { 𝐶 ′ # if ( 𝑏 ) { 𝐶 ′ } },            ...
For an 𝑛-unrolling 𝐶 𝑛 of the loop 𝐶 and postweighting 𝜑 ∈ wHeyLo, the weakest preweighting is
wpJ𝐶 𝑛 K(𝜑) = Φ𝑛𝜑 (⊥). We know from Section 2 and Kleene’s fixed point theorem [7] that the weakest
preweightings is wpJ𝐶K(𝜑) = lfp 𝑋 . Φ𝜑 (𝑋 ) = 𝑛∈N Φ𝑛𝜑 (⊥) and hence wpJ𝐶 𝑛 K(𝜑) ⊑ wpJ𝐶K(𝜑) for
                                              Ã
all 𝑛 ∈ N. The more times we unroll the loop, the better the approximation becomes.
    Lemma 5.6 (Finite Loop Unrolling). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, weightings
𝑓 , ℎ ∈ W, and the corresponding characteristic function Φ 𝑓 , we have, for any 𝑛 ∈ N, that
                                   ℎ ⊑ Φ𝑛𝑓 (⊥)       implies ℎ ⊑ wpJ𝐶K(𝑓 ).
   The proof of the previous lemma applies Kleene’s fixed point theorem and uses the monotonicity
of the join ⊔. For the encoding and a postweighting 𝜑 ∈ wHeyLo, we translate the characteristic
16                                                                           Ahrens, Rode, Schröer, and Katoen


function Φ𝜑 (𝐼 ) = [𝑏] · wpJ𝐶 ′ K(𝐼 ) ⊕ [¬𝑏] · 𝜑 into the wHeyVL program charEnc(𝐶, 𝐼 ) in Figure 8,
where 𝐼 ∈ wHeyLo. If 𝑏 holds, this program encodes the loop body enc(𝐶 ′ ), asserts that 𝐼 holds,
and uses assume ? (false) afterwards to discard the current assertion. If 𝑏 does not hold, then the
postweighting 𝜑 holds.
   Lemma 5.7 (Semantics). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, weightings 𝜑, 𝐼 ∈ wHeyLo, an
encoding enc(𝐶 ′ ) with vpJenc(𝐶 ′ )K(𝜓 ) ⊑ wpJ𝐶 ′ K(𝜓 ) for all 𝜓 ∈ wHeyLo, and 𝜎 ∈ Σ, the encoding
of the characteristic function Φ𝜑 (𝐼 ) given in Figure 8 satisfies
                                                   (
                                                     vpJenc(𝐶 ′ )K(𝐼 ) (𝜎), if J𝑏K(𝜎)
                   vpJcharEnc(𝐶, 𝐼 )K(𝜑) (𝜎) =                                        .
                                                    𝜑 (𝜎),                  otherwise
  Hence, the translation charEnc encodes exactly the characteristic function Φ and, via applying
the program 𝑛 ∈ N times, we use Lemma 5.6 to derive the following property.
  Lemma 5.8 (Soundness). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, weightings 𝜑, 𝐼 ∈ wHeyLo,
𝑛 ∈ N, and an encoding enc(𝐶 ′ ) with vpJenc(𝐶 ′ )K(𝜓 ) ⊑ wpJ𝐶 ′ K(𝜓 ) for all 𝜓 ∈ wHeyLo, the
encoding charEnc is a sound under-approximation, thus vpJcharEnc(𝐶, ⊥)𝑛 K(𝜑) ⊑ wpJ𝐶K(𝜑).
  We use this proof rule by checking 𝜌 ⊑ vpJcharEnc(𝐶, ⊥)𝑛 K(𝜑) for some 𝑛 ∈ N and 𝜌, 𝜑 ∈
wHeyLo. If this holds, we can conclude that 𝜌 ⊑ wpJ𝐶K(𝜑) is a lower bound.
  The dual proof rule exists for the weakest liberal preweightings of loops, where we obtain an upper
bound by applying the characteristic function repeatedly. In this case, the encoding charEncco (𝐶, 𝐼 )
contains the dual co-statements (note that the dual of assume ? (false) is coassume ? (true)) and
everything follows similarly.

5.3   Local Park Induction
Park induction allows reasoning about an unbounded number of steps. Also, loop unrolling gives us
a lower bound for the weakest preweighting of a loop, while Park induction yields an upper bound
(and the dual holds for weakest liberal preweightings). Instead of applying the characteristic function
to the least or greatest weighting, we need to guess a suitable loop invariant to under-approximate
the weakest liberal preweighting of the loop (and over-approximate weakest preweightings).
    More specifically, we call 𝐼 ∈ wHeyLo a subinvariant, if 𝐼 ⊑ Ψ𝑓 (𝐼 ), and a superinvariant, if Φ 𝑓 (𝐼 ) ⊑
𝐼 . Park induction states that the invariant is a lower bound on the weakest liberal preweighting of
the loop 𝐶 ∈ wGCL for postweighting 𝜑 ∈ wHeyLo, hence 𝐼 ⊑ wlpJ𝐶 ′ K(𝜑), if 𝐼 is a subinvariant
[7]. For wpJ𝐶K(𝜑), the weighting 𝐼 is an upper bound if it is a superinvariant.
    Here, we define local Park induction on a restricted state space that depends variables that are
modified during the execution of the loop, so-called local variables (see Section 5.1). This alteration
allows us to prove more (correct) invariants than the original Park induction rule and makes the rule
more complete. In the classical setting of Boolean verification, Boogie/BoogiePL-based encodings
implement this idea as part of their encodings [28] and related loop-cutting transformations have
been validated operationally [31]. In the quantitative setting, the tool Caesar also employs this
enhanced rule, although its proof was missing.
    Suppose that Γ ⊆ Σ is a set of states that is closed under the 𝛽-reachable states, more formally,
Reach𝛽 (𝜎) ⊆ Γ for all 𝜎 ∈ Γ. Then, we alter the original proof rule to local Park induction by
considering Γ-restricted weightings 𝜑 |Γ and restricted inequalities ⊑Γ .
   Definition 5.9. For weightings 𝑓 , 𝑔 ∈ W and a set of states Γ ⊆ Σ that is closed under 𝛽-
reachability, we consider Γ-restricted weightings 𝑓 |Γ , 𝑔 |Γ : Γ → W with the Γ-restricted order
𝑓 |Γ ⊑Γ 𝑔 |Γ if and only if 𝑓 (𝜎) ⊑ 𝑔(𝜎) ∀𝜎 ∈ Γ.
Towards a Verification Infrastructure for wGCL                                                       17


  This restriction keeps all the previous properties, since the set of restricted weightings is again
an 𝜔-bicontinuous monoid-module and in particular also 𝜔-bicomplete partially ordered.
  Lemma 5.10 (Closedness under Reachability). For a program 𝐶 ∈ wGCL with local variables
𝛽 ⊆ Vars and a set Γ ⊆ Σ of states that is closed under 𝛽-reachability, wlpJ𝐶K : W → W is closed
under Γ-restricted weightings: for all 𝑓 ∈ W, there exists 𝑔 ∈ W such that wlpJ𝐶K(𝑓 |Γ ) = 𝑔 |Γ .
   Since the weighting transformer Ψ𝑓 is 𝜔-cocontinuous, we derive from the previous lemma that
its restriction to an set Γ (closed under 𝛽-reachable states) is again 𝜔-bicontinuous. Finally, we can
state and prove the local variant of Park induction. Here, we use global weightings 𝑓 , 𝐼 ∈ W but
consider only the restricted state space Γ.
    Theorem 5.11 (Local Park Induction). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL with local
variables 𝛽 ⊆ Vars, a set Γ ⊆ Σ of states that is closed under 𝛽-reachability, and weightings 𝑓 , 𝐼 ∈ W,
it is
                       𝐼 ⊑Γ Ψ𝑓 (𝐼 ) implies 𝐼 ⊑Γ wlpJwhile ( 𝑏 ) { 𝐶 ′ }K(𝑓 ).
   The Ski-rental problem as introduced in Figure 1a is a simple example where the correctness of
the invariant depends on constant variables that are not modified during the execution of the loop.
The optimal costs of the program are min{𝑛, 𝑦}, where 𝑛 is the number of days and 𝑦 is the cost of
buying skis. However, the original Park induction rule does not suffice to prove the correctness
for the invariant 𝐼 = min{𝑛, 𝑦} for postweighting 0 ∈ W, since it considers the global state space
Σ: A counterexample is 𝜎 ∈ Σ with 𝜎 (𝑛) = 4, 𝜎 (𝑦) = 6, and 𝜎 (𝑐) = 2, where the optimal costs are
min{2 · 𝑛, 𝑦} = 6 and the inequality on the left-hand side in Theorem 5.11 does not hold, since
                     𝜎 (𝐼 ) = 4 ̸⊑ Ψ𝑓 (𝐼 ) (𝜎) = 5   ⇐⇒ 𝜎 (𝐼 ) = 4 ≱ Ψ𝑓 (𝐼 ) (𝜎) = 5.
 The local proof rule considers only the restricted state space Γ = {𝜎 ∈ Σ | 𝜎 (𝑐) = 1}. Here, we can
show that 𝐼 is indeed a subinvariant and thus verify the correctness of the program.
  The encoding of local Park induction is parkEnc in Figure 8 and Lemma C.1 shows that its
semantics satisfies
                                                   (
                                                     𝐼 (𝜎), if 𝐼 ⊑Reach𝛽 (𝜎 ) Ψ𝜑 (𝐼 )
                     vpJparkEnc(𝐶, 𝐼 )K(𝜑) (𝜎) ⊑
                                                     ⊥,     otherwise .

  Theorem 5.12 (Soundness). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL with local variables
𝛽 ⊆ Vars and weightings 𝜑, 𝐼 ∈ wHeyLo, the encoding parkEnc is a sound under-approximation, thus
                                  vpJparkEnc(𝐶, 𝛽, 𝐼 )K(𝜑) ⊑ wlpJ𝐶K(𝜑).
   The dual proof rule exists for weakest preweightings of loops, where we check whether 𝐼 ∈
wHeyLo is a superinvariant and obtain an upper bound by computing the encoding parkEncco (𝐶, 𝛽, 𝐼 )
that contains the corresponding co-statements and everything follows analogously. This allows us
to prove programs where the correctness of the invariant depends on constant variables that are
not modified during the execution.

5.4   Local 𝜅-Induction
The 𝜅-induction proof rule, formalized by Batz et al. [6] for complete lattices, extends Park induction
by relaxing its strict one-step inductivity requirement. We adapt this technique to our setting of
𝜔-bicomplete partial orders and extend it to local 𝜅-induction.
  Recall that, for a loop 𝐶 and postweighting 𝜑 ∈ wHeyLo, the weakest liberal preweighing is the
greatest fixed point of the characteristic function and due to Kleene’s fixed point theorem [7] it is
18                                                                                                                                        Ahrens, Rode, Schröer, and Katoen



                                                                   𝜅-Enc(𝐶, 𝛽, 𝐼 )                                          0-unrollEnc(𝐶, 𝛽, 𝐼 ) =
                         (𝛽 : [𝐼, 𝐼 ])
                          specEnc



                                                                    assert 𝐼 ; havoc 𝛽;                                     charEnc(𝐶, 𝛽, 𝐼 )
                                                                    validate; assume 𝐼 ;
                                                                                                                            for 𝜅 > 0 :
                                                                    if (𝑏) {
                                                                                                                            𝜅-unrollEnc(𝐶, 𝛽, 𝐼 ) =
                                                                               enc(𝐶 ′ ); coassert 𝐼 ;
                                                                                                                            if (𝑏) {
                                                                               if (𝑏) {
                               (𝜅-1)-unrollEnc(𝐶, 𝛽, 𝐼 )
 𝜅-unrollEnc(𝐶, 𝛽, 𝐼 )




                                                                                                                               enc(𝐶 ′ );       (encoding of loop body)
                                                                                 enc(𝐶 ′ ); coassert 𝐼 ;
                                                                                                                               coassert 𝐼 ;             (admit invariant)
                                                           charEnc(𝐶, 𝛽, 𝐼 )




                                                                                 if (𝑏) {
                                                                                                                               (𝜅-1)-unrollEnc(𝐶, 𝛽, 𝐼 );
                                                                                    enc(𝐶 ′ ); assert 𝐼 ;
                                                                                                                            } else {}
                                                                                    assume ? (false);
                                                                                    } else {}
                                                                                 } else {}
                                                                               } else {}


Fig. 9. Encoding of 𝜅-induction for the loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, variables 𝛽 ⊆ Vars, weightings
𝜌,𝜓 ∈ wHeyLo, an invariant 𝐼 ∈ wHeyLo, and 𝜅 = 2.


wlpJ𝐶K(𝜑) = gfp 𝑋 . Ψ𝜑 (𝑋 ) = 𝑛∈N Ψ𝜑𝑛 (⊤). Via local Park induction, we can prove a lower bound
                             d
𝐼 ∈ wHeyLo and refine it by iteratively applying the characteristic function, hence
                                                                                           𝐼 ⊑Γ Ψ𝜑 (𝐼 ) ⊑Γ Ψ𝜑2 (𝐼 ) ⊑Γ · · · ⊑Γ wlpJ𝐶K(𝜑).
However, the reverse direction of Park induction does not hold in general. Even if 𝐼 is a valid upper
bound with 𝐼 ⊑Γ wlpJ𝐶K(𝜑), the weighting 𝐼 might not be inductive in the sense that 𝐼 ̸⊑Γ Ψ𝜑 (𝐼 ).
To tackle this, we create an increasing chain with the following operator.
  Definition 5.13. For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL and weightings 𝑓 , 𝐼 ∈ W, the 𝜅-
induction operator is defined as Λ : W → W, 𝑋 ↦→ 𝐼 ⊔ Ψ𝑓 (𝑋 ).
   Since we extend 𝜅-induction to local 𝜅-induction, we consider a set of states Γ ⊆ Σ that is closed
under 𝛽-reachability, where 𝛽 are the local variables of the program. Then, Γ-restricted weightings
𝜑 |Γ ,𝜓 |Γ : Γ → W consider a smaller state space and allow for a Γ-restricted order ⊑Γ (compare
with Section 5.3). We have shown in Lemma 5.10 that the characteristic function Ψ𝜑 is closed under
Γ-restricted weightings and we show the same for the 𝜅-induction operator in Lemma C.2.
   Now, even if the weighting 𝐼 ∈ wHeyLo is not inductive (𝐼 ̸⊑Γ Ψ𝜑 (𝐼 )), the operator Λ enforces
the increasing chain 𝐼 ⊑𝛽 Λ(𝐼 ) = 𝐼 ⊔ Ψ𝜑 (𝐼 ) ⊑𝛽 Λ2 (𝐼 ) = 𝐼 ⊔ Ψ𝜑 (𝐼 ⊔ Ψ𝜑 (𝐼 )) ⊑𝛽 · · ·
Applying Λ iteratively can be interpreted as searching for a inductive weighting; there exists a
𝜅 ∈ N such that (Λ𝜅 (𝐼 ) ⊑Γ Ψ𝜑 (Λ𝜅 (𝐼 )) is a local subinvariant) if and only if (𝐼 ⊑Γ Ψ𝜑 (Λ𝜅 (𝐼 ))). Then
we use local Park induction to derive that 𝐼 ⊑Γ Λ𝜅 (𝐼 ) ⊑Γ wlpJwhile ( 𝑏 ) { 𝐶 ′ }K(𝜑).
   Theorem 5.14 (𝜅-Induction). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL with local variables
𝛽 ⊆ Vars, a set Γ ⊆ Σ of states that is closed under 𝛽-reachability, weightings 𝑓 , 𝐼 ∈ W, and 𝜅 ∈ N, it
is
                    𝐼 ⊑Γ Ψ𝑓 (Λ𝜅 (𝐼 )) implies 𝐼 ⊑Γ wlpJwhile ( 𝑏 ) { 𝐶 ′ }K(𝑓 ).
Towards a Verification Infrastructure for wGCL                                                                    19



 𝜔-Enc(𝐶, 𝐼 𝑛 )                                            rig proc step (𝑥 1 : 𝜏1, . . . , 𝑥 𝑘 : 𝜏𝑘 )
 cohavoc 𝑛;                     (supremum over 𝑛)                      -> (𝑥 1 : 𝜏1, . . . , 𝑥𝑘 : 𝜏𝑘 )
 assert 𝐼 (𝑛);                         (filter for 𝐼 𝑛 )   pre 𝐼 (𝑛 + 1)
 assume ? (false)                  (establish truth)       post 𝜑
                                                           { var 𝑥 1 : 𝜏1 := 𝑥 1 ; . . . ; var 𝑥𝑘 : 𝜏𝑘 := 𝑥 𝑘 ;
 rig proc base (𝑥 1 : 𝜏1, . . . , 𝑥 𝑘 : 𝜏𝑘 ) -> ()
                                                              if (𝑏) {
  pre 𝐼 (0)
                                                                 enc(𝐶 ′ ); assert 𝐼 (𝑛); assume ? (false);
  post ? (false)
                                                              } else {} }
  {}

Fig. 10. Encoding of the 𝜔-rule for the loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, weighting 𝜑 ∈ wHeyLo, and an
𝜔-invariant 𝐼 (𝑛) ∈ wHeyLo with free variable 𝑛 ∈ Vars.


   We encode local 𝜅-induction via the encoding 𝜅-Enc(𝐶, 𝛽, 𝐼 ) = specEnc(𝛽 : [𝐼, 𝐼 ]);
𝜅-unrollEnc(𝐶, 𝛽, 𝐼 ) that modifies the variables 𝛽, applies the 𝜅-induction operator 𝜅 times, and
then computes the characteristic function Ψ𝜑 , see Figure 9. The Lemma C.3 shows that the semantics
of the encoding 𝜅-Enc satisfies
                                                    (
                                                      𝐼 (𝜎), if 𝐼 ⊑Γ Ψ𝜑 (Λ𝜅 (𝐼 ))
                     vpJ𝜅-Enc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) ⊑
                                                      ⊥,      otherwise .

The soundness of the encoding follows from the 𝜅-induction proof rule and the semantics of the en-
coding. This is formalized in Theorem C.4, which states that 𝜅-Enc is a sound under-approximation
with
                               vpJ𝜅-Enc(𝐶, 𝛽, 𝐼 )K(𝜑) ⊑ wlpJ𝐶K(𝜑).
  Again, the dual proof rule exists for proving upper bounds by replacing the encodings in Figure 9
by their dual co-statements. The corresponding proofs are completely dual.

5.5 𝜔-Invariants
Until now, loop unrolling is the only proof rule that computes lower bounds for weakest preweight-
ings (and upper bounds for weakest liberal preweightings). However, this rule considers exactly
𝑛 unrollings for a fixed 𝑛 ∈ N. The 𝜔-rule allows us to prove lower bounds for all 𝑛 ∈ N by
constructing a chain of weightings (𝐼 𝑛 )𝑛∈N ∈ wHeyLoN , where 𝐼 𝑛 lower-bounds the 𝑛-th un-
rolling, hence 𝐼 𝑛 ⊑ Φ𝑛𝜑 (⊥) for every 𝑛 ∈ N. We show that its limit is a sound lower bound of the
weakest preweighting of the loop. The dual proof rule exists for upper bounds of weakest liberal
preweightings.
  We call an 𝜔-ascending chain of weightings (𝐼 𝑛 )𝑛∈N ∈ wHeyLoN an 𝜔-subinvariant, if 𝐼 0 = ⊥
and 𝐼 𝑛+1 ⊑ Φ𝜑 (𝐼 𝑛 ) for all 𝑛 ∈ N holds. An 𝜔-descending chain (𝐼 𝑛 )𝑛∈N ∈ wHeyLoN is an 𝜔-
superinvariant, if 𝐼 0 = ⊤ and Ψ𝜑 (𝐼 𝑛 ) ⊑ 𝐼 𝑛+1 for all 𝑛 ∈ N. The 𝜔-rule states that, given an
𝜔-subinvariant (𝐼 𝑛 )𝑛∈N , its supremum is a lower bound of the weakest preweighting of the loop.
We can show by induction that every term 𝐼 𝑛 bounds the subsequent Kleene term Φ𝑛+1    𝜑 (⊥) and
prove that the limit of the sequence (𝐼 𝑛 )𝑛∈N soundly approximates the fixed point.
  Theorem 5.15 (𝜔-Rule). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, a postweighting 𝑓 ∈ W, and
an 𝜔-subinvariant (𝐼 𝑛 )𝑛∈N ∈ WN , it is sup𝑛∈N 𝐼 𝑛 ⊑ wpJwhile ( 𝑏 ) { 𝐶 ′ }K(𝑓 ).
20                                                                        Ahrens, Rode, Schröer, and Katoen


  For the encoding of the 𝜔-rule, we represent the sequence (𝐼 𝑛 )𝑛∈N by the formula 𝐼 (𝑛) ∈ wHeyLo
with free variable 𝑛 ∈ Vars. Then, we check that (𝐼 (𝑛))𝑛∈N is an 𝜔-subinvariant via the two auxiliary
programs in Figure 10 that encode the base case and the induction step of a natural induction on 𝑛.
  Lemma 5.16 (Checking 𝜔-Invariant). For a weighting 𝐼 (𝑛) ∈ wHeyLo with free variable 𝑛 ∈
Vars, the programs 𝑏𝑎𝑠𝑒 and 𝑠𝑡𝑒𝑝 in Figure 10 encode
                𝐼 (0) ⊑ vpJ𝑏𝑎𝑠𝑒K(𝜑)           if and only if     𝐼 (0) = ⊥
        and     𝐼 (𝑛 + 1) ⊑ vpJ𝑠𝑡𝑒𝑝K(𝜑)           implies        ∀𝑛 ∈ N : 𝐼 (𝑛 + 1) ⊑ Φ𝜑 (𝐼 (𝑛)).
   If the two auxiliary programs are valid, Theorem 5.15 induces that sup𝑛∈N 𝐼 𝑛 is a lower bound
of the weakest preweighting of the loop. This is encoded in 𝜔-Enc in Figure 10 and Lemma C.5
shows that                                                     Ä
                             vpJ𝜔-Enc(𝐶, (𝐼 𝑛 )𝑛∈N )K(𝜑) (𝜎) =   𝐼 (𝑛).
                                                                 𝑛∈N
  If one of the two procedures fail to verify, the proposed sequence is not a valid 𝜔-invariant and
the whole verification fails. Otherwise, the encoding guarantees a sound lower bound (Theorem C.6)
on the weakest preweighting with vpJ𝜔-Enc(𝐶, (𝐼 𝑛 )𝑛∈N )K(𝜑) ⊑ wpJ𝐶K(𝜑).

6     Case Studies
In this section, we illustrate the application of our framework to verify quantitative properties of
weighted programs. We demonstrate the use of the proof rules that we developed in Section 5 such
as Park induction and the 𝜔-rule. Moreover, we focus on the pipeline that our framework imposes.
   Take a program 𝐶 ∈ wGCL and a postweighting 𝑓 ∈ W. For each loop, pick a proof rule from
Section 5 and guess an invariant 𝐼 ∈ W. Decide whether to under- or overapproximate. Transform
𝐶 into a wHeyVL program by encoding loop-free fragments directly and loops via the encoding of
the proof rule. Encode the weightings as wHeyLo formulae. Apply the verification preweighting
transformer vp to obtain a preweighting 𝜌 ∈ wHeyLo and eliminate quantifier via the algorithm in
Section 7, before discharging to an SMT solver.

6.1    Network Security Analysis
Let us consider a (simplified) example, where an attacker needs 𝑛 steps in a network to reach
a target database with hidden information. At each step, the attacker has the nondeterministic
choice between a standard attack (which requires clearance level Clearance to succeed) and a
specific exploit of service that usually requires the high clearance level TopSecret, but has a critical
vulnerability at the last step (hence clearance level Confidential suffices).
   Many automated approaches to network security modeling, such as the attack graphs generated
by Sheyner et al. [34], require a finite-state representation of the network. These methods evaluate
fixed topologies and cannot verify properties across networks of unbounded size 𝑛. Compositional
reasoning via weakest preweightings often avoids these limitations for network topologies that are
representable as weighted programs. Instead of generating a graph of size 𝑛, we compactly encode
the rules of the topology using a while-loop.
   Our example 𝐶𝐴𝐶 is encoded in Figure 26 and uses the monoid-module
Clearance:           Mclear = ({P, C, S, TS}, max, P)   and    Wclear = ({P, C, S, TS}, min, TS, max) ,
with totally-ordered values Public < Confidential < Secret < TopSecret, the additive operation
min (choosing the path with least security clearance) and the multiplicative operation max (the
clearance of a path is the maximum clearance of its steps)
   By calculating an upper bound on the weakest preweighting wpJ𝐶𝐴𝐶 K(P) ⊑ 𝜑, corresponding to
wpJ𝐶𝐴𝐶 K(P) ≥ 𝜑, we determine the minimal clearance an attacker needs to successfully compromise
Towards a Verification Infrastructure for wGCL                                                         21


the target for an arbitrary network size 𝑛. Figure 8 and the invariant 𝐼 (𝑛) = min{[𝑛 = 0] · P, [𝑛 = 1] ·
C, [𝑛 ≥ 2] · S} gives us the encoding networkSecurity = parkEnc(𝐶𝐴𝐶 , 𝛽, 𝐼 (𝑛)) in Figure 23, where
𝛽 = {𝑛}. Using Theorem 5.12, we derive that
                         wpJnetworkSecurityK(P) ⊑ vpJnetworkSecurityK ⊑ 𝐼 (𝑛 0 ).
The minimal security clearance is hence P if the attacker is already at the target (𝑛 = 0), C if the
target is one step away (𝑛 = 1), and S, otherwise (𝑛 ≥ 2).

6.2    Lock-Freedom of the Compare-And-Swap Technique
In concurrency theory, we need guarantees on how multiple processes interact when competing
for shared resources. In [7], the authors analyse starvation-freedom of a mutual exclusion protocol
via weakest preweightings. A common non-blocking progress condition is lock-freedom [23, p. 60],
which guarantees global progress7 , but individual threads may starve [22].
   Consider a system with 𝑁 threads trying to increment a shared counter (𝑣) using the compare-
and-swap technique, where each process 𝑖 saves a local copy of the counter in ℓ [𝑖] and computes
the incremented value ℓ [𝑖] + 1. In each iteration, a process is non-deterministically chosen and
updates the variable 𝑣, if its local copy of 𝑣 is up-to-date, otherwise, it updates its local copy.
   We write infinite words 𝑤 over the alphabet Γ = {S1, F1, . . . , S𝑁 , F𝑁 } via the formal languages
module Wlang to analyse the progress of 𝑁 processes. E.g., the word S1 F2 S2 · · · depicts that process
1 successfully updated the counter 𝑣, then process 2 failed and updated its local copy, and afterwards
process 2 successfully updated the counter 𝑣. The program 𝐶𝐶𝐴𝑆 ∈ wGCL in Figure 1b encodes the
compare-and-swap technique and the corresponding language of infinite words.
   We define a descending 𝜔-chain of languages (L𝑛 )𝑛∈N , where L𝑛 contains all infinite words with
at most 𝑁 consecutive failures in the first 𝑛 steps. Then, we show that wlpJ𝐶𝐶𝐴𝑆 K(⊥) ⊑ inf 𝑛∈N L𝑛 ,
which implies that every computed word contains at most 𝑁 consecutive failures and thus the
program is lock-free. We specify auxiliary languages L𝑛𝑘 , 𝑛 ∈ N and 1 ≤ 𝑘 ≤ 𝑁 ,
                                                                Ø               Ø              
                     0
                              Ø
     L0 = Γ ,
      𝑘     𝜔
                   L𝑛+1 =          S𝑖 · L𝑛 , and
                                         𝑁              𝑘+1
                                                      L𝑛+1 =                 𝑘
                                                                      F𝑖 · L𝑛 ∪                 𝑁
                                                                                          S𝑖 · L𝑛 .
                                 1≤𝑖 ≤𝑁                                    1≤𝑖 ≤𝑁   1≤𝑖 ≤𝑁

Again, the subscript 𝑛 specifies that the prefix of length 𝑛 contains at most 𝑁 consecutive failures.
The superscript 𝑘 specifies that the word starts with at most 𝑘 consecutive failures. As an example,
we have F3 F1 S3 F3 F2 F1 F3 S1 ∈ L62 for 𝑁 = 3, which starts with exactly 2 consecutive failures and
contains at most 3 consecutive failures in the prefix of length 6. Now, we define L𝑛 = L𝑛𝑁 .
  Theorem 5.15 states that if wlp Φ⊥ (L𝑛 ) ⊑ L𝑛+1 for all 𝑛 ∈ N, then inf 𝑛∈N L𝑛 is an upper bound
on the weakest liberal preweighting. The encoding of this proof rule in wHeyVL is given by
baseCAS, stepCAS, and CAS = 𝜔-Enc(𝐶𝐶𝐴𝑆 , L𝑛 ), see Figure 23. Via Theorem C.6, we conclude that
wlpJ𝐶𝐶𝐴𝑆 K(⊥) ⊑ vpJCASK ⊑ inf 𝑛∈N L𝑛 .

6.3    Queueing Background Jobs
We consider a queue of 𝑘 background jobs (e.g. image processing, mail delivery, report generation).
Each job succeeds with probability 0.8 and fails with probability 0.2. Upon failure, the system either
performs a simple retry with costs 4 or restarts the system and performs a full retry with costs 6.
We want to obtain a bound on the expected total costs of processing the queue.
   The probability module Wprob allows us to model this problem as a program 𝐶𝑄 ∈ wGCLprob (see
Figure 24). In wGCLprob , a program { ⊗ 0.8 # 𝐶 1 } ⊕ { ⊗ 0.2 # 𝐶 2 } corresponds to the probabilistic
choice { 𝐶 1 } [0.8] { 𝐶 2 } from pGCL. Since this generalizes and all other statements of pGCL are
7 At every step, some thread will make progress within a finite number of steps.
22                                                                              Ahrens, Rode, Schröer, and Katoen


native in wGCLprob (compare with [29]), weighted programming is a conservative extension of
probabilistic programming over non-negative integer variables.
   The expected costs of processing the queue are tracked in the variable 𝑒. Hence, we compute
an upper bound of wpJ𝐶𝑄 K(𝑒) and illustrate this for 𝜅-induction with 𝜅 = 2 by upper bounding
wp
   Φ𝑒 ( wp Φ𝑒 (𝐼 ) ⊓ 𝐼 ) for some invariant 𝐼 ∈ wHeyLo. The encoding is queueing = 𝜅-Enc(𝐶𝑄 , 𝛽, 𝐼 ) ∈
wHeyVL for local variables 𝛽 = {𝑘, 𝑒, 𝑏} and invariant 𝐼 = 𝑒 + 4 · 𝑘 + 16 · [𝑏 ≠ 𝑏 0 ] (see Figure 22).
We derive that wpJ𝐶𝑄 K(𝑒) ⊑ vpJqueueingK ⊑ 𝑒 0 + 4 · 𝑘 0 , where 𝑒 0 and 𝑘 0 are the initial values of 𝑒
and 𝑘. Hence, the additional costs are bounded by 4 · 𝑘 for a queue of length 𝑘.

6.4   Database Provenance
In database theory, Why provenance [12, 14, 18, 19] analyses which entries in a data-
base determine the result of a query. As an example, we consider the organisational                     a b
hierarchy of a company, where new ideas are discussed with the direct supervisor.                       2 3
Employee 𝑎 may discuss an idea with its manager 𝑏 in the table. This is a simplified                    2 1
version of the path accessibility problem [12, 13]. Figure 11 visualises the organiation.               3 2
We consider the query: Can information travel from employee 4 to manager 1?                             3 1
   Why provenance determines why that query is correct, hence which employees                           4 2
need to know about the new idea in order to pass it on to the top manager. Or, more                     5 2
formally, which entries in the table lead to the result of the query. Here, one possible                6 3
explanation for the result are the rows 1, 2, and 5 in the table. However, there exist
other explanations (e.g. rows 1, 3, and 5 or rows 1, 2, 3, and 5) and the new idea can be passed back
and forth between employees 2 and 3 arbitrarily often, which leads to infinitely many explanations.
The Why semiring [14] provides finite representations of the infinite explanations due to the
idempotent addition ∨ and we represent that employee 𝑎 knows about an idea by the atom 𝑋𝑎 .
Figure 25 contains an implementation in wGCLwhy and computes the information flow from 4 to 1.
   To obtain the provenance, we are interested in the weakest liberal
preweighting wlpJ𝐶𝐺𝑅 K(⊤), where the postweighting 𝜑 = ⊤ means that                                1
we do not impose any additional constraints. We use Park induction to
show that 𝐼 ⊑ Ψ𝑓 (𝐼 ) for the invariant 𝐼 = [𝑒 = 1] · 𝑋 1 ∨ [𝑒 = 2] · (𝑋 1 ∧                2             3
𝑋 2 ∧ 𝑋 3 ) ∨ [𝑒 = 3] · (𝑋 1 ∧ 𝑋 2 ∧ 𝑋 3 ) ∨ [𝑒 = 4] · (𝑋 1 ∧ 𝑋 2 ∧ 𝑋 3 ∧ 𝑋 4 ). Fig-
ure 8 gives us the encoding graphReachability = parkEnc(𝐶𝐺𝑅 , {𝑒}, 𝐼 )                  4       5      6      7
in Figure 21. Using Theorem 5.12, we derive that 𝑋 1 ∧ 𝑋 2 ∧ 𝑋 3 ∧ 𝑋 4 ⊑
vpJgraphReachabilityK ⊑ wlpJ𝐶𝐺𝑅 K(⊤), which means that the informa-
                                                                                      Fig. 11. Organizational hi-
tion may travel via the employees 1, 2, 3, and 4.
                                                                                      erarchy as a graph.
   Note that reasoning via weakest preweightings and the vp calculus
elegantly avoid looking at infinitely many derivation trees (representing
infinitely many explanations), relying on complex, infinite formal power series, or implementing
specialized algorithms to prevent infinite loops, since loops are evaluted as fixed points and the
idempotent operation algebraically collapses the representation of infinite derivation trees into
finite, closed-form expressions. This captures exact provenance without requiring infinite data
structures or cycle detection.

7 Automated Reasoning
7.1 Verification via Caesar
For the verification of the case studies in the previous section, we give a translation from certain
instances of wHeyVL into the existing tool Caesar [33]. This is a first step towards full automation of
weighted programs. This is simple for the probability module Wprob , since wGCL is a conservative
Towards a Verification Infrastructure for wGCL                                                                23


                                Infimum-prefix rules                              Supremum-prefix rules
Context                                d                                                 Ã
                                        𝑥 (·)                                             𝑥 (·)

Lattice
                   d                 d        d                       Ã                Ã        Ã
                  ( 𝑥 𝜑 ) ★ 𝜓, 𝜑 ★ ( 𝑦 𝜓 ) ≡ (𝜑 ★ 𝜓 ) always         ( 𝑥 𝜑 ) ★ 𝜓, 𝜑 ★ ( 𝑦 𝜓 ) ≡ (𝜑 ★ 𝜓 ) always
Validation
                     d  d                                              Ã        Ã
                  △ 𝑥 𝜑 ≡ 𝑥 △ (𝜑 )                    always         △ ( 𝑥 𝜑 ) ≡ 𝑥 △ (𝜑 )                  uwf.
Covalidation
                    d  d                                               Ã        Ã
                  ▽ 𝑥 𝜑 ≡ 𝑥 ▽ (𝜑 )                        wf.        ▽ ( 𝑥 𝜑 ) ≡ 𝑥 ▽ (𝜑 )                always
Implication
                   Ã                   d        d                     d                  Ã        Ã
                  ( 𝑥 𝜑 ) → 𝜓, 𝜑 → ( 𝑦 𝜓 ) ≡ (𝜑 → 𝜓 ) always         ( 𝑥 𝜑 ) → 𝜓, 𝜑 → ( 𝑦 𝜓 ) ≡ (𝜑 → 𝜓 ) uwf.
Coimplication
                   Ã                   d        d                     d                  Ã        Ã
                  ( 𝑥 𝜑 ) ← 𝜓, 𝜑 ← ( 𝑦 𝜓 ) ≡ (𝜑 ← 𝜓 )     wf.        ( 𝑥 𝜑 ) ← 𝜓, 𝜑 ← ( 𝑦 𝜓 ) ≡ (𝜑 ← 𝜓 ) always
Addition
                   d                 d        d                       Ã                Ã        Ã
                  ( 𝑥 𝜑 ) ⊕ 𝜓, 𝜑 ⊕ ( 𝑦 𝜓 ) ≡ (𝜑 ⊕ 𝜓 )    W+          ( 𝑥 𝜑 ) ⊕ 𝜓, 𝜑 ⊕ ( 𝑦 𝜓 ) ≡ (𝜑 ⊕ 𝜓 )    W+
Scalar
                       d         d                                        Ã        Ã
                  𝑎 ⊗ ( 𝑥 𝜑 ) ≡ 𝑥 (𝑎 ⊗ 𝜑 )              extra        𝑎 ⊗ ( 𝑥 𝜑 ) ≡ 𝑥 (𝑎 ⊗ 𝜑 )               Wx


Fig. 12. Prenexing rules for 𝜑,𝜓 ∈ wHeyLo and 𝑎 ∈ MExp where 𝑥 is not free in 𝜓 and 𝑦 is not free in 𝜑.
Comma-separated formulas  d are separate    prenexing laws, one for each displayed position of the quantified
                                     Ã
subformula. On the right, (·) and (·) bind the same variable as the quantified subformula being moved.
In the lattice row, ★ ∈ {⊓, ⊔}. always rules hold always, W+/Wx: under extra weighted assumptions, uwf./wf.
under (upwards) well-foundedness, and extra under scalar meet preservation.


extension of pGCL, wHeyVL is also a conservative extension of HeyVL. For the Why semiring
Wwhy , we translate statements ⊗ 𝑚 into assume ? (𝑚) and statements if (+) into if (⊔) {·} else {·}
(which corresponds to booleanizing the formulae). The Clearance module is translated by replacing
⊗ 𝑚 with coassert 𝑚 and if (+) with if (⊓) {·} else {·}. And the formal languages module
considers a variable ℓ that contains the language that will be computed in the remainder of the
execution. Then, ⊗ 𝑚 translates to assert ℓ ⊆ 𝑚 · Γ ∞ , which ensures that all words in ℓ start with
𝑚. Section E contains the full translations for the instances that we consider in this work.

7.2    Quantifier Elimination
For automated verification, we want to discharge verification conditions to an SMT solver. The
quantitative quantifiers of wHeyLo are an obstacle: as they correspond to infima and suprema,
classical techniques for quantifier elimination do not apply. Hence, we develop a technique for
quantifier elimination in our setting. This also covers the previously not formalized implementation
in use by Caesar, so far limited to the probabilistic module Wprob . Quantifier elimination is
necessary in particular due to the use of havoc/cohavoc, which induces infima/suprema. For
example, the encoding    of Park induction (c.f. Section 5.3) has a verification condition of the form
⊤ ≡ 𝜌 → (𝐼 ⊓ 𝑥 △(Ψ)), where 𝐼 ∈ wHeyLo is the loop invariant and 𝜌 ∈ wHeyLo is a pre, and
                 d
Ψ ∈ wHeyLo is for the loop body.8 The key observation is that, one can first move the quantifier
(prenex) and then strip leading infima, preserving equivalence with respect to validity. We assume
𝑥 is only bound in Ψ and does not occur free in 𝜌 or 𝐼 .9
            1. Prenex:
                                         d                       d
                                𝜌 → 𝐼 ⊓ 𝑥 △(Ψ)               ≡     𝑥 (𝜌 → (𝐼 ⊓ △(Ψ)))
               2. Strip:    𝑥 (𝜌 → (𝐼 ⊓ △(Ψ))) is valid iff 𝜌 → (𝐼 ⊓ △(Ψ)) is valid .
                          d

  Figure 12 shows the landscape of prenexing rules that hold under various assumptions. Many
hold always (always). For the example above where we eliminate infima, we make use of the rules in
the second column and prenex over the validation △(·), binary meet ⊓, and implication →.
  The rules in the second column generate a prefix of infimum quantifiers, and the third column
generate suprema. Generally, we can strip leading infima with respect to validity (equivalence to
⊤), and suprema with respect to covalidity (equivalence to ⊥):
8 Instead of 𝜌 ⊑ 𝐼 ⊓
                      𝑥 △ (Ψ), we use the internalized version ⊤ ≡ 𝜌 → (𝐼 ⊓ 𝑥 △ (Ψ) ) (recall Theorem 3.2).
                       d                                                   d
9 Variables bound by quantifiers can always be renamed to satisfy this condition.
24                                                                                      Ahrens, Rode, Schröer, and Katoen


           Elimination for Validity                                        Elimination for Covalidity
          qelim↓ : wHeyLo → wHeyLo:                                        qelim↑ : wHeyLo → wHeyLo:
             𝛼 ↦→ 𝛼  for atomic 𝛼, ⊤, ⊥                                        𝛼 ↦→ 𝛼for atomic 𝛼, ⊤, ⊥
                                                                                            
          △(𝜑) ↦→ △ qelim↓ (𝜑)                                            ▽(𝜑) ↦→ ▽ qelim↑ (𝜑)
         𝜑 ★ 𝜓 ↦→ qelim↓ (𝜑) ★ qelim↓ (𝜓 )                               𝜑 ★ 𝜓 ↦→ qelim↑ (𝜑) ★ qelim↑ (𝜓 )
             for ★ ∈ {⊓, ⊔, ⊕}                                                for ★ ∈ {⊓, ⊔, ⊕}
         𝑎 ⊗ 𝜑 ↦→ 𝑎 ⊗ qelim↓ (𝜑)                                          𝑎 ⊗ 𝜑 ↦→ 𝑎 ⊗ qelim↑ (𝜑)
        𝜑 → 𝜓 ↦→ qelim↑ (𝜑) → qelim↓ (𝜓 )                               𝜑 ← 𝜓 ↦→ qelim↓ (𝜑) ← qelim↑ (𝜓 )
          d                    ↓                                          Ã                    ↑
           𝑥 𝜑 ↦→ fresh𝑥 (qelim (𝜑))                                       𝑥 𝜑 ↦→ fresh𝑥 (qelim (𝜑))

             𝜑 ↦→ 𝜑       otherwise                                            𝜑 ↦→ 𝜑       otherwise

Fig. 13. Quantifier elimination procedures qelim↓ and qelim↑ for validity and covalidity, respectively. The
function fresh𝑥 (·) : wHeyLo → wHeyLo replaces the eliminated bound variable 𝑥 by a fresh free variable.


     Theorem 7.1 (Quantifier Stripping). For every 𝜑 ∈ wHeyLo:
               l                                Ä
                  𝜑 is valid iff 𝜑 is valid,       𝜑 is covalid iff 𝜑 is covalid.
                  𝑥                                            𝑥

d In contrast to classical logic, we cannot always prenex quantifiers [4]. For example, ▽ 𝑥 𝜑 ≡
                                                                                                d 

   𝑥 ▽(𝜑) only holdsd when our monoid-module is well-founded, i.e. for all 𝜎 ∈ Σ, there exists a value
𝑣 ∈ N such that J 𝑥 𝜑K(𝜎) = J𝜑d    [𝑥 ↦→ 𝑣]K(𝜎) for all 𝜑 ∈ wHeyLo. Over the probabilistic    d module
Wprob , letd𝜑 = (1/2)𝑥 ⊗ 1. Then 𝑥 𝜑 = 0, but no 𝑥 ∈ N realizes this infimum; hence ∇( 𝑥 𝜑) = 0,
whereas 𝑥 ∇(𝜑) = ∞. By contrast, the tropical monoid-module Wtrop is upwards well-founded:
its natural order is reversed on N∞ , so suprema are ordinary minima and are always attained.
Further, all of our monoid-modules also satisfy the W+, Wx, extra assumptions, which allow prenexing
over addition and scalar multiplication (suprema and infima), respectively.10 From now on, we
focus on rules that always hold for the monoid-modules in our paper (always, W+, Wx, extra but not wf.
nor uwf.). The constructions can be easily extended for when other assumptions hold.
    In the above, we used the rules in Figure 12 to shift quantifiers bottom-up and then strip a prefix.
However, when the shifted quantifier cannot be stripped (e.g. a supremum w.r.t. validity), we want to
avoid quantifiers capturing larger formulas than before. Therefore, we present a top-down approach
in Figure 13. Starting from the root, we directly remove eliminatable quantifiers while possible and
stop recursing at quantifiers that cannot be eliminated. When a quantifier is removed, we replace
bound variables 𝑥 by fresh ones to avoid wrong capture. We have two entry points, qelim↓ and
qelim↑ , corresponding to elimination with respect to validity and covalidity, respectively. When the
pattern of the current formula matches, then we may stop, recurse, orÃ   switch to the dual procedure.
For example, qelim↓ (△ 𝑥 𝑥 ) = △ qelim↓ (𝑥) = △(𝑥) and qelim↓ ( 𝑥 𝑥 → 𝑦 𝑦) = 𝑥 → 𝑦. For
                          d                                                       d

soundness, we prove the equivalence to prenexing and stripping leading quantifiers via Theorem 7.1.


     Theorem 7.2. Assume always, W+, Wx, and extra hold. Then, for every 𝜑 ∈ wHeyLo,
           𝜑 is valid     iff qelim↓ (𝜑) is valid ,           𝜑 is covalid     iff   qelim↑ (𝜑) is covalid .
10 For W+, ⊕ must preserve binary meets and joins, and for Wx, 𝑎 ⊗ (·) must preserve binary joins, for extra, binary meets.
Towards a Verification Infrastructure for wGCL                                                                    25


   Because the procedures traverse every sub-formula at most once, they run in linear time.11 The
resulting formulas are of the same sizes as before, only with quantifiers removed and fresh variables
introduced for every bound variable. For the following fragment, all quantifiers can be eliminated.
  Theorem 7.3. Assume always, W+, Wx, and extra hold. Let wHeyLo↓, wHeyLo↑ ⊆ wHeyLo be given by
the following mutually recursive grammars, where 𝜑 qf ∈ wHeyLo is quantifier-free.
                                l
           𝜑 ↓ ::= 𝜑 qf | △ 𝜑 ↓ |  𝜑 ↓ | 𝜑 ↓ ⊓ 𝜑 ↓ | 𝜑 ↓ ⊔ 𝜑 ↓ | 𝜑 ↓ ⊕ 𝜑 ↓ | 𝑎 ⊗ 𝜑 ↓ | 𝜑 ↑ → 𝜑 ↓,
                                       𝑥
                                  Ä
             𝜑 ↑ ::= 𝜑 qf | ▽ 𝜑 ↑ |  𝜑↑ | 𝜑↑ ⊓ 𝜑↑ | 𝜑↑ ⊔ 𝜑↑ | 𝜑↑ ⊕ 𝜑↑ | 𝑎 ⊗ 𝜑↑ | 𝜑↓ ← 𝜑↑.
                                        𝑥

Let 𝜑 ∈ wHeyLo↓ . Then, qelim↓ (𝜑) ∈ wHeyLoqf . For 𝜑 ∈ wHeyLo↑, we have qelim↑ (𝜑) ∈ wHeyLoqf .
   As a consequence, we can completely eliminate the quantifiers introduced by havoc statements
in procedures for encodings of the specification statement, Park and 𝑘-induction proof rules (c.f.
Section 5). Dually, the same holds for the dual encodings using cohavoc statements in coprocedures.

8   Related Work
Because we generalize using monoid-modules and not just semirings, our work subsumes prob-
abilistic programming verification, in particular the HeyVL language [33].12 We address several
missing details, including soundness of local proof rules, and quantifier elimination. Although both
are internally used in the Caesar implementation, they were previously not formally addressed.
   We build a general deductive verification framework for weighted programs, extending weakest
preweighting semantics [7] with an assertion language and an intermediate verification language.
For proof rules, we newly generalize the proof rules for specification statements [30], 𝜅-induction [6],
and 𝜔-invariants, introducing local variants.
   Weighted NetKAT [1] provides a semiring-parametric extension of NetKAT and verifies quantita-
tive network properties by compiling policies to weighted automata. This is complementary to our
work: Weighted NetKAT exploits the finite packet model of NetKAT to obtain decision procedures,
while our framework provides a general deductive verification infrastructure for weighted programs.
However, Weighted NetKAT policies can be encoded as wGCL programs, and the corresponding
scalar properties can be stated as weakest-preweighting bounds and verified deductively. Outcome
Logic [35] is a Hoare-style logic with algebraic effects based on semirings.
   Batz et al. study quantifier elimination for piecewise-linear quantities over the extended ratio-
nals [8]. In contrast, we also support e.g. formulas with exponentials (c.f. Section 7) and other
monoid-modules. Whereas they target full logical equivalence, we only target validity/covalidity,
which is sufficient for verification conditions. For Gödel logics, Baaz and Gamsakhurdia study
prenex fragments [4] and show that prenex normal forms are not always available. In contrast to
both of the above, we also degrade gracefully when quantifiers cannot be eliminated.

9   Conclusion
We presented a deductive verification infrastructure for weighted programs, parameterized by
𝜔-bicontinuous monoid-modules whose natural orders form bi-Heyting algebras. Its assertion
language wHeyLo and intermediate language wHeyVL uniformly support lower- and upper-bound
reasoning and encode specification statements, local Park and 𝜅-induction, and 𝜔-invariants. We
11 qelim↓ (·) and qelim↑ (·) can be combined with the variable renaming of fresh to avoid redundant traversals.
12 This work only subsumes probabilistic programs without reward statements, as those are still missing in weighted

programming as well.
26                                                                                          Ahrens, Rode, Schröer, and Katoen


proved these encodings sound and presented a linear-time, best-effort quantifier-elimination proce-
dure that preserves validity or covalidity and is complete on identified fragments. Sound lowerings
to Caesar enabled the verification of expected costs, security clearances, database provenance, and
formal-language properties. Future work includes a native implementation, automated invariant
generation, and support for higher moments and multiple objectives.

References
 [1] Emmanuel Suárez Acevedo, Tiago Ferreira, Kevin Batz, Oliver Bøving, Nate Foster, and Alexandra Silva. 2026. Weighted
     NetKAT: A Programming Language For Quantitative Network Verification. Proc. ACM Program. Lang. 10, PLDI, Article
     240 (2026), 73 pages. doi:10.1145/3808318
 [2] Emma Ahrens, Jan-Christoph Kassing, Jürgen Giesl, and Joost-Pieter Katoen. 2025. Weighted Rewriting: Semiring
     Semantics for Abstract Reduction Systems. In 10th International Conference on Formal Structures for Computation and
     Deduction, FSCD 2025, Birmingham, UK, July 14-20, 2025 (LIPIcs, Vol. 337), Maribel Fernández (Ed.). Schloss Dagstuhl -
     Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 6:1–6:21. doi:10.4230/LIPICS.FSCD.2025.6
 [3] Martin Avanzini and Akihisa Yamada. 2025. Weighted Rewriting. In Frontiers of Combining Systems - 15th International
     Symposium, FroCoS 2025, Reykjavik, Iceland, September 29 - October 1, 2025, Proceedings (Lecture Notes in Computer
     Science, Vol. 15979), René Thiemann and Christoph Weidenbach (Eds.). Springer, Cham, 191–208. doi:10.1007/978-3-
     032-04167-8_11
 [4] Matthias Baaz and Mariami Gamsakhurdia. 2024. Goedel logics: Prenex fragments. arXiv:2407.16683 [cs.LO] https:
     //arxiv.org/abs/2407.16683
 [5] Michael Barnett, Bor-Yuh Evan Chang, Robert DeLine, Bart Jacobs, and K. Rustan M. Leino. 2005. Boogie: A Modular
     Reusable Verifier for Object-Oriented Programs. In Formal Methods for Components and Objects, 4th International
     Symposium, FMCO 2005, Amsterdam, The Netherlands, November 1-4, 2005, Revised Lectures (Lecture Notes in Computer
     Science, Vol. 4111), Frank S. de Boer, Marcello M. Bonsangue, Susanne Graf, and Willem P. de Roever (Eds.). Springer,
     Berlin, Heidelberg, 364–387. doi:10.1007/11804192_17
 [6] Kevin Batz, Mingshuai Chen, Benjamin Lucien Kaminski, Joost-Pieter Katoen, Christoph Matheja, and Philipp Schröer.
     2021. Latticed k-Induction with an Application to Probabilistic Programs. In Computer Aided Verification - 33rd
     International Conference, CAV 2021, Virtual Event, July 20-23, 2021, Proceedings, Part II (Lecture Notes in Computer Science,
     Vol. 12760), Alexandra Silva and K. Rustan M. Leino (Eds.). Springer, Cham, 524–549. doi:10.1007/978-3-030-81688-9_25
 [7] Kevin Batz, Adrian Gallus, Benjamin Lucien Kaminski, Joost-Pieter Katoen, and Tobias Winkler. 2022. Weighted
     programming: a programming paradigm for specifying mathematical models. Proc. ACM Program. Lang. 6, OOPSLA1
     (2022), 1–30. doi:10.1145/3527310
 [8] Kevin Batz, Joost-Pieter Katoen, and Nora Orhan. 2025. Quantifier Elimination and Craig Interpolation: The Quantitative
     Way. In Foundations of Software Science and Computation Structures - 28th International Conference, FoSSaCS 2025, Held
     as Part of the International Joint Conferences on Theory and Practice of Software, ETAPS 2025, Hamilton, ON, Canada,
     May 3-8, 2025, Proceedings (Lecture Notes in Computer Science, Vol. 15691), Parosh Aziz Abdulla and Delia Kesner (Eds.).
     Springer, Cham, 176–197. doi:10.1007/978-3-031-90897-2_9
 [9] Vaishak Belle and Luc De Raedt. 2020. Semiring programming: A semantic framework for generalized sum product
     problems. Int. J. Approx. Reason. 126 (2020), 181–201. doi:10.1016/J.IJAR.2020.08.001
[10] Stefano Bistarelli, Fabio Martinelli, and Francesco Santini. 2008. A Semantic Foundation for Trust Management
     Languages with Weights: An Application to the RTFamily. In Autonomic and Trusted Computing, 5th International
     Conference, ATC 2008, Oslo, Norway, June 23-25, 2008, Proceedings (Lecture Notes in Computer Science, Vol. 5060),
     Chunming Rong, Martin Gilje Jaatun, Frode Eika Sandnes, Laurence Tianruo Yang, and Jianhua Ma (Eds.). Springer,
     Berlin, Heidelberg, 481–495. doi:10.1007/978-3-540-69295-9_38
[11] Benedikt Bollig and Paul Gastin. 2009. Weighted versus Probabilistic Logics. In Developments in Language Theory, 13th
     International Conference, DLT 2009, Stuttgart, Germany, June 30 - July 3, 2009. Proceedings (Lecture Notes in Computer
     Science, Vol. 5583), Volker Diekert and Dirk Nowotka (Eds.). Springer, Berlin, Heidelberg, 18–38. doi:10.1007/978-3-
     642-02737-6_2
[12] Marco Calautti, Ester Livshits, Andreas Pieris, and Markus Schneider. 2024. The Complexity of Why-Provenance for
     Datalog Queries. Proc. ACM Manag. Data 2, 2, Article 83 (May 2024), 16 pages. doi:10.1145/3651146
[13] Stephen A. Cook. 1974. An Observation on Time-Storage Trade Off. J. Comput. Syst. Sci. 9, 3 (1974), 308–316.
     doi:10.1016/S0022-0000(74)80046-2
[14] Katrin M. Dannert, Erich Grädel, Matthias Naaf, and Val Tannen. 2021. Semiring Provenance for Fixed-Point Logic. In
     29th EACSL Annual Conference on Computer Science Logic (CSL 2021) (Leibniz International Proceedings in Informatics
     (LIPIcs), Vol. 183), Christel Baier and Jean Goubault-Larrecq (Eds.). Schloss Dagstuhl – Leibniz-Zentrum für Informatik,
     Dagstuhl, Germany, 17:1–17:22. doi:10.4230/LIPIcs.CSL.2021.17
Towards a Verification Infrastructure for wGCL                                                                           27


[15] Edsger W. Dijkstra. 1975. Guarded Commands, Nondeterminacy and Formal Derivation of Programs. Commun. ACM
     18, 8 (1975), 453–457. doi:10.1145/360933.360975
[16] Manfred Droste and Dietrich Kuske. 2021. Weighted automata. In Handbook of Automata Theory, Jean-Éric Pin (Ed.).
     European Mathematical Society Publishing House, Zürich, Switzerland, 113–150. doi:10.4171/AUTOMATA-1/4
[17] Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3 - Where Programs Meet Provers. In Programming
     Languages and Systems - 22nd European Symposium on Programming, ESOP 2013, Held as Part of the European Joint
     Conferences on Theory and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013. Proceedings (Lecture Notes
     in Computer Science, Vol. 7792), Matthias Felleisen and Philippa Gardner (Eds.). Springer, Berlin, Heidelberg, 125–128.
     doi:10.1007/978-3-642-37036-6_8
[18] Erich Grädel and Val Tannen. 2025. Provenance Analysis and Semiring Semantics for First-Order Logic. In Model
     Theory, Computer Science, and Graph Polynomials: Festschrift in Honor of Johann A. Makowsky, Klaus Meer, Alexander
     Rabinovich, Elena Ravve, and Andrés Villaveces (Eds.). Springer Nature Switzerland, Cham, 351–401. doi:10.1007/978-
     3-031-86319-6_21
[19] Todd J. Green, Grigoris Karvounarakis, and Val Tannen. 2007. Provenance semirings. In Proceedings of the Twenty-Sixth
     ACM SIGMOD-SIGACT-SIGART Symposium on Principles of Database Systems (Beijing, China) (PODS ’07). Association
     for Computing Machinery, New York, NY, USA, 31–40. doi:10.1145/1265530.1265535
[20] Tao Gu and Fabio Zanasi. 2021. Coalgebraic Semantics for Probabilistic Logic Programming. Log. Methods Comput. Sci.
     17, 2 (2021), 2:1–2:35. doi:10.23638/LMCS-17(2:2)2021
[21] Mikkel Hansen, Kim Guldstrand Larsen, Radu Mardare, and Mathias Ruggaard Pedersen. 2018. Reasoning About Bounds
     in Weighted Transition Systems. Log. Methods Comput. Sci. 14, 4 (2018), 19:1–19:32. doi:10.23638/LMCS-14(4:19)2018
[22] Maurice Herlihy and Nir Shavit. 2011. On the Nature of Progress. In Principles of Distributed Systems (Lecture Notes in
     Computer Science, Vol. 7109), Antonio Fernández Anta, Giuseppe Lipari, and Matthieu Roy (Eds.). Springer, Berlin,
     Heidelberg, 313–328. doi:10.1007/978-3-642-25873-2_22
[23] M. Herlihy, N. Shavit, V. Luchangco, and M. Spear. 2020. The Art of Multiprocessor Programming (2 ed.). Morgan
     Kaufmann, Cambridge, MA. doi:10.1016/C2011-0-06993-4
[24] P.T. Johnstone. 1982. Stone Spaces. Cambridge University Press, Cambridge. https://books.google.de/books?id=
     CiWwoLNbpykC
[25] Stephen Cole Kleene. 2002. Mathematical Logic (dover ed. ed.). Dover Publications, Mineola, NY. Originally published
     by Wiley in 1967.
[26] Spencer Van Koevering, Wojciech Rozowski, and Alexandra Silva. 2025. Weighted GKAT: Completeness and Complexity.
     In 52nd International Colloquium on Automata, Languages, and Programming, ICALP 2025, Aarhus, Denmark, July 8-11,
     2025 (LIPIcs, Vol. 334), Keren Censor-Hillel, Fabrizio Grandoni, Joël Ouaknine, and Gabriele Puppis (Eds.). Schloss
     Dagstuhl - Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 172:1–172:18. doi:10.4230/LIPICS.ICALP.2025.172
[27] Werner Kuich. 1997. Semirings and Formal Power Series: Their Relevance to Formal Languages and Automata. In
     Handbook of Formal Languages, Volume 1: Word, Language, Grammar, Grzegorz Rozenberg and Arto Salomaa (Eds.).
     Springer, Berlin, Heidelberg, 609–677. doi:10.1007/978-3-642-59136-5_9
[28] K. Rustan M. Leino and Wolfram Schulte. 2007. A Verifying Compiler for a Multi-Threaded Object-Oriented Lan-
     guage. In Software System Reliability and Security, Manfred Broy, Johannes Grünbauer, and Tony Hoare (Eds.).
     NATO Security through Science Series D: Information and Communication Security, Vol. 9. IOS Press, Amsterdam,
     351–416. https://www.microsoft.com/en-us/research/publication/a-verifying-compiler-for-a-multi-threaded-object-
     oriented-language/
[29] Annabelle McIver and Carroll Morgan. 2005. Abstraction, Refinement and Proof for Probabilistic Systems. Springer,
     New York, NY. doi:10.1007/B138392
[30] Carroll Morgan. 1988. The Specification Statement. ACM Trans. Program. Lang. Syst. 10, 3 (1988), 403–419. doi:10.
     1145/44501.44503
[31] Gaurav Parthasarathy, Peter Müller, and Alexander J. Summers. 2021. Formally Validating a Practical Verification
     Condition Generator. In Computer Aided Verification (Lecture Notes in Computer Science). Springer, Cham, 704–727.
     doi:10.1007/978-3-030-81688-9_33
[32] Stefan Riezler. 1997. Quantitative Constraint Logic Programming for Weighted Grammar Applications. In Logical
     Aspects of Computational Linguistics (Lecture Notes in Computer Science, Vol. 1328), Christian Retoré (Ed.). Springer,
     Berlin, Heidelberg, 346–365. doi:10.1007/BFb0052166
[33] Philipp Schröer, Kevin Batz, Benjamin Lucien Kaminski, Joost-Pieter Katoen, and Christoph Matheja. 2023. A Deductive
     Verification Infrastructure for Probabilistic Programs. Proc. ACM Program. Lang. 7, OOPSLA2 (2023), 2052–2082.
     doi:10.1145/3622870
[34] O. Sheyner, J. Haines, S. Jha, R. Lippmann, and J.M. Wing. 2002. Automated generation and analysis of attack graphs.
     In Proceedings 2002 IEEE Symposium on Security and Privacy. IEEE Computer Society, Los Alamitos, CA, 273–284.
     doi:10.1109/SECPRI.2002.1004377
28                                                                              Ahrens, Rode, Schröer, and Katoen


[35] Noam Zilberstein. 2025. Outcome Logic: A Unified Approach to the Metatheory of Program Logics with Branching
     Effects. ACM Trans. Program. Lang. Syst. 47, 3 (2025), 14:1–14:71. doi:10.1145/3743131
Towards a Verification Infrastructure for wGCL                                                              29


A    Additional Theory of Section 2: Weighted Programming and Reasoning via Weakest
     Preweightings
  Definition A.1 (Semiring). A semiring S = (𝑆, ⊕, ⊙, 0, 1) is the set 𝑆 together with two operations
and corresponding neutral elements such that
      • the structure (𝑆, ⊕, 0) is a commutative monoid,
      • the structure (𝑆, ⊙, 1) is a monoid,
      • the multiplication is distributive over the addition, hence for all 𝑎, 𝑏, 𝑐 ∈ 𝑆

                𝑎 ⊙ (𝑏 ⊕ 𝑐) = (𝑎 ⊙ 𝑏) ⊕ (𝑎 ⊙ 𝑐)         and   (𝑎 ⊕ 𝑏) ⊙ 𝑐 = (𝑎 ⊙ 𝑐) ⊕ (𝑏 ⊙ 𝑐),

      • and multiplication by zero annihilates, hence for all 𝑎 ∈ 𝑆

                                                 𝑎 ⊙ 0 = 0 ⊙ 𝑎 = 0.

  Lemma A.2. A semiring S = (𝑆, ⊕, ⊙, 0, 1) is a special instance of a module W = (𝑊 , ⊕, 0, ⊗) over
the monoid M = (𝑀, ⊙, 1), where
      • the monoid M = (𝑀, ⊙, 1) satisfies 𝑊 = 𝑆, ⊙ M = ⊙ S , and 1 M = 1 S , and
      • the module W = (𝑊 , ⊕, 0, ⊗) satisfies 𝑀 = 𝑆, ⊕ W = ⊕ S , 0 W = 0 S , and ⊗ W = ⊙.

   Proof. Due to the definition of semirings, we know that W = (𝑊 , ⊕, 0, ⊗) is a monoid and
M = (𝑀, ⊙, 1) is a commutative monoid. The scalar multiplication ⊗ : 𝑊 × 𝑀 → 𝑀 is associative,
distributive, and has the neutral element 1, since the multiplicative operation ⊙ S is associative,
distributive, and has 1 as neutral element. Furthermore, 0 annihilates, since it also annihilates in
the semiring.                                                                                      □

 Lemma A.3 (Monotonicity of Scalar Multiplication). Let W = (𝑊 , ⊕, 0, ⊗) be a monoid-
module over a monoid M. For all 𝑎 ∈ 𝑀 and 𝑝, 𝑞 ∈ 𝑊 ,

                                       𝑝 ⊑𝑞       implies 𝑎 ⊗ 𝑝 ⊑ 𝑎 ⊗ 𝑞.

    Proof.

                 𝑝 ⊑𝑞      implies     ∃𝑚 ∈ 𝑊 . 𝑝 ⊕ 𝑚 = 𝑞                     (definition of the natural order)
                           implies 𝑎 ⊗ (𝑝 ⊕ 𝑚) = 𝑎 ⊗ 𝑞                                 (scalar multiplication)
                           implies     (𝑎 ⊗ 𝑝) ⊕ (𝑎 ⊗ 𝑚) = 𝑎 ⊗ 𝑞                  (distributivity of ⊗ over ⊕)
                           implies 𝑎 ⊗ 𝑝 ⊑ 𝑎 ⊗ 𝑞.                             (definition of the natural order)

                                                                                                             □

  Lemma A.4 (Monotonicity of Weighted Addition). Let W = (𝑊 , ⊕, 0, ⊗) be a monoid-module
over a monoid M. For all 𝑐, 𝑝, 𝑞 ∈ 𝑊 ,

                                       𝑝 ⊑𝑞       implies 𝑝 ⊕ 𝑐 ⊑ 𝑞 ⊕ 𝑐.

  Proof. Assume 𝑝 ⊑ 𝑞. By definition of the natural order, there exists 𝑚 ∈ 𝑊 such that 𝑝 ⊕ 𝑚 = 𝑞.
Hence
                                     (𝑝 ⊕ 𝑐) ⊕ 𝑚 = (𝑝 ⊕ 𝑚) ⊕ 𝑐 = 𝑞 ⊕ 𝑐,
using associativity and commutativity of ⊕. Therefore 𝑝 ⊕ 𝑐 ⊑ 𝑞 ⊕ 𝑐.                                         □
30                                                                                                      Ahrens, Rode, Schröer, and Katoen



                                                                      𝑏          J𝑏K(𝜎) ∈ {0, 1}
             𝑎                  J𝑎K(𝜎) ∈ N                                       (
                                                                                   1, if J𝑎K(𝜎) < J𝑎 ′ K(𝜎)
             𝑛∈N                𝑛                                     𝑎 < 𝑎′
                                                                                   0, otherwise
             𝑥 ∈ Vars           𝜎 (𝑥)                                            (
                                                                                   1, if J𝑏K(𝜎) = 0
             𝑎 + 𝑎′             J𝑎K(𝜎) + J𝑎 ′ K(𝜎)                    ¬𝑏
                                                                                   0, otherwise
             𝑎 · 𝑎′             J𝑎K(𝜎) · J𝑎 ′ K(𝜎)                               (
                                                                                   1, if J𝑏K(𝜎) + J𝑏 ′ K(𝜎) ≥ 1
             𝑎 −¤ 𝑎 ′           J𝑎K(𝜎) −¤ J𝑎 ′ K(𝜎)                   𝑏 ∧ 𝑏′
                                                                                   0, otherwise

Fig. 14. Semantics of arithmetic and Boolean expressions AExp and BExp, where monus −¤ is subtraction
truncated at 0.

                   𝜎 ′ = 𝜎 [𝑥 ↦→ 𝜎 (𝑏 ) ]                                                       𝑢 = 𝜎 (𝑚)
                                                 (assign)                                                             (weight)
                  ⟨𝑥 := 𝑏, 𝜎 ⟩ ⊢1    ⟨↓, 𝜎 ′ ⟩                                             ⟨⊗ 𝑚 , 𝜎 ⟩ ⊢𝑢 ⟨↓, 𝜎 ⟩
                    ⟨𝐶 1 , 𝜎 ⟩ ⊢𝑢 ⟨↓, 𝜎 ′ ⟩                                          ⟨𝐶 1 , 𝜎 ⟩ ⊢𝑢 ⟨𝐶 1′ , 𝜎 ′ ⟩ and 𝐶 1′ ≠↓
                                                   (seq. 1)                                                                    (seq. 2)
                 ⟨𝐶 1 # 𝐶 2 , 𝜎 ⟩ ⊢𝑢 ⟨𝐶 2 , 𝜎 ⟩                                      ⟨𝐶 1 # 𝐶 2 , 𝜎 ⟩ ⊢𝑢 ⟨𝐶 1′ # 𝐶 2 , 𝜎 ⟩
                              𝜎 |= 𝑏                                                                𝜎 |= ¬𝑏
                                                              (if)                                                                        (else)
      ⟨if ( 𝑏 ) { 𝐶 1 } else { 𝐶 2 } , 𝜎 ⟩ ⊢1 ⟨𝐶 1 , 𝜎 ⟩                       ⟨if ( 𝑏 ) { 𝐶 1 } else { 𝐶 2 } , 𝜎 ⟩ ⊢1 ⟨𝐶 2 , 𝜎 ⟩

                                                   (left branch)                                                          (right branch)
        ⟨ { 𝐶 1 } ⊕ { 𝐶 2 }, 𝜎 ⟩ ⊢1 ⟨𝐶 1 , 𝜎 ⟩                                   ⟨ { 𝐶 1 } ⊕ { 𝐶 2 }, 𝜎 ⟩ ⊢1 ⟨𝐶 2 , 𝜎 ⟩
                            𝜎 |= 𝑏                                                                 𝜎 |= ¬𝑏
                                                                   (while)                                                     (break)
⟨while ( 𝑏 ) { 𝐶 } , 𝜎 ⟩ ⊢1 ⟨𝐶 # while ( 𝑏 ) { 𝐶 } , 𝜎 ⟩                            ⟨while ( 𝑏 ) { 𝐶 } , 𝜎 ⟩ ⊢1 ⟨↓, 𝜎 ⟩

Fig. 15. The structural operational semantics for wGCL-programs from [7] without the computation counter
and the branching history and extended by weighted expressions.


A.1    Operational Semantics
We use program states to construct configurations and define the semantics of weighted programs
via a weighted relation on the set of configurations.
   Definition A.5 (Configuration). A configuration is a tuple (𝐶, 𝜎) ∈ (wGCL ∪ {↓}) × Σ =: 𝑄, where
↓ indicates termination.
  For a specific configuration (𝐶, 𝜎), the weighted program 𝐶 contains the remaining commands
and 𝜎 is the current program state. Now, we define the semantics of a weighted program as a
weighted relation between configurations.
  Definition A.6 (Operational Semantics of wGCL). The computation relation ⊢ ⊂ 𝑄 × M × 𝑄 is
the smallest set satisfying the rules in Figure 15.

  Definition A.7 (Weakest Liberal Preweightings). For an 𝜔-cocontinuous module W over the
monoid M, we define the weakest liberal preweightings iteratively as the weighting transformer
wlp : wGCL → (W → W) via the rules in Figure 4.
   The weakest liberal preweighting of a loop is defined via the greatest fixed point of the charac-
teristic function wlp Φ : W → W, 𝑋 ↦→ [¬𝑏] 𝑓 ⊕ [𝑏]wlpJ𝐶K(𝑋 ).
Towards a Verification Infrastructure for wGCL                                                 31


  Theorem A.8. The weighting transformer wlpJ𝐶K(·) is a well-defined, 𝜔-cocontinuous function. In
particular, the greatest fixed point of the function wlp Φ exists for all 𝑤 ∈ W and 𝐶 ∈ wGCL.
   The proof of this theorem can be found in [7].
32                                                                        Ahrens, Rode, Schröer, and Katoen


B     Theory and Proofs of Section 3: Heyting (Co-)Implications for Totally Ordered and
      Boolean Algebras
     Definition B.1 (Bounded Lattice). A partially ordered set (𝑆, ⊑) is a bounded lattice, if
       • it is a lattice, hence there exist greatest lower bounds 𝑎 ⊓ 𝑏 ∈ 𝑆 and least upper bounds
          𝑎 ⊔ 𝑏 ∈ 𝑆 for all 𝑎, 𝑏 ∈ 𝑆 with regard to the order ⊑, and
       • there exists a greatest element ⊤ ∈ 𝑆 and least element ⊥ ∈ 𝑆 such that 𝑎 ⊓ ⊤ = 𝑎 and
          𝑎 ⊔ ⊥ = 𝑎 for all 𝑎 ∈ 𝑆.
  Both the meet ⊓ and join ⊔ are commutative (𝑎 ⊓𝑏 = 𝑏 ⊓ 𝑎), associative (𝑎 ⊓ (𝑏 ⊓ 𝑐) = (𝑎 ⊓𝑏) ⊓ 𝑐),
and absorbing (𝑎 ⊓ (𝑎 ⊔ 𝑏) = 𝑎 for 𝑎, 𝑏, 𝑐 ∈ 𝑆).
     Lemma B.2. Meet and join are distributive in Heyting algebras.
     Proof. See [24].                                                                                    □
  Lemma B.3. Let W be an 𝜔-bicontinuous monoid-module. If the natural order ⊑ on 𝑊 admits
binary meets and joins, then (𝑊 , ⊑) is a bounded lattice.
   Proof. By 𝜔-continuity, ⊑ is a partial order with a least element, which we denote by ⊥. By
𝜔-cocontinuity, the reversed order ⊒ has a least element. Equivalently, ⊑ has a greatest element,
which we denote by ⊤.
   By assumption, all binary meets and joins with respect to ⊑ exist. Hence (𝑊 , ⊑) is a lattice with
least element ⊥ and greatest element ⊤, and therefore a bounded lattice.                            □
     Theorem 3.2 (Deduction Theorem). Let H be a bi-Heyting algebra and 𝑎, 𝑏 ∈ 𝐻 . Then, we have
                   𝑎 ⊑ 𝑏     iff 𝑎 → 𝑏 = ⊤        and      𝑎 ⊒ 𝑏      iff 𝑎 ← 𝑏 = ⊥.
     Proof.
      (1) For the first statement, instantiate the Heyting adjunction with 𝑥 = ⊤:
                                     𝑎⊓⊤ ⊑𝑏       iff ⊤ ⊑ 𝑎 → 𝑏.
          Since 𝑎 ⊓ ⊤ = 𝑎 and ⊤ ⊑ 𝑦 holds iff 𝑦 = ⊤, this yields 𝑎 ⊑ 𝑏 iff 𝑎 → 𝑏 = ⊤.
      (2) Dually, instantiate the co-Heyting adjunction with 𝑥 = ⊥:
                                     𝑏 ⊑𝑎⊔⊥       iff 𝑎 ← 𝑏 ⊑ ⊥.
          Since 𝑎 ⊔ ⊥ = 𝑎 and 𝑦 ⊑ ⊥ holds iff 𝑦 = ⊥, this yields 𝑎 ⊒ 𝑏 iff 𝑎 ← 𝑏 = ⊥.
                                                                                                         □
     Lemma 3.3. Let H be a bi-Heyting algebra. For all 𝑏 ∈ B and 𝑥 ∈ 𝐻 , we have
                           (                                          (
                             𝑥, if 𝑏                                    𝑥, if ¬𝑏
               ? (𝑏) → 𝑥 =                       and      ? (𝑏) ← 𝑥 =
                             ⊤, otherwise                               ⊥, otherwise
     Proof. By the adjunction laws of bi-Heyting algebras (Def. 3.1), for every 𝑥 ∈ 𝐻 ,
                   ⊤ → 𝑥 = 𝑥,        ⊥ → 𝑥 = ⊤,         ⊤ ← 𝑥 = ⊥,       ⊥ ← 𝑥 = 𝑥.
This follows immediately, e.g. 𝑎 ⊑ ⊤ → 𝑥 iff 𝑎 = ⊤ ⊓ 𝑎 ⊑ 𝑥, and (⊥ ← 𝑥) ⊑ 𝑎 iff 𝑥 ⊑ ⊥ ⊔ 𝑎 = 𝑎.
The other two identities are exactly given in Theorem 3.2.                                  □
     Recall Lemma 3.6 from Page 9:
  Lemma 3.6 (Residual Characterization of (Co-)Implication). Let (𝐻, ⊑) be a bounded lattice.
Then, the following statements are equivalent:
Towards a Verification Infrastructure for wGCL                                                        33


   (1) There exists an implication → suchÃthat (𝐻, ⊑, ⊓, ⊔, →) is a Heyting algebra.
   (2) For every 𝑎, 𝑏 ∈ 𝐻 , the supremum {𝑥 ∈ 𝐻 | 𝑎 ⊓ 𝑥 ⊑ 𝑏} is well-defined.
                                                        Ã
Then, we derive that the Heyting implication is 𝑎 → 𝑏 = {𝑥 ∈ 𝐻 | 𝑎 ⊓ 𝑥 ⊑ 𝑏} for all 𝑎, 𝑏 ∈ 𝐻 .
  Proof. (⇒)
      For 𝑎, 𝑏 ∈ 𝐻 , we show 𝑎 → 𝑏 is the greatest element of 𝑆 := {𝑥 ∈ 𝐻 | 𝑎 ⊓ 𝑥 ⊑ 𝑏}.
       (1) Since 𝑎 → 𝑏 ⊑ 𝑎 → 𝑏, we have 𝑎 ⊓ (𝑎 → 𝑏) ⊑ 𝑏 by Definition 3.1: Bi-Heyting
           Algebra, hence 𝑎 → 𝑏 ∈ 𝑆.
       (2) Let 𝑥 ∈ 𝑆 be arbitrary, i.e. 𝑎 ⊓ 𝑥 ⊑ 𝑏. By Definition 3.1, this gives 𝑥 ⊑ 𝑎 → 𝑏.
      Since 𝑎 → 𝑏 ∈ 𝑆 and every 𝑥 ∈ 𝑆 satisfies 𝑥 ⊑ 𝑎 → 𝑏, we conclude that 𝑎 → 𝑏 is the
      greatest element
                   Ã of 𝑆. SinceÃa greatest element of a subset of a poset is always its
      supremum, 𝑆 exists and 𝑆 = 𝑎 → 𝑏, as claimed.
(⇐)
      For 𝑎, 𝑏 ∈ 𝐻 , define 𝑎 → 𝑏 := max{𝑥 ∈ 𝐻 | 𝑎 ⊓𝑥 ⊑ 𝑏}, which is well-defined because
      the assumption guarantees the max exists, and it is unique since ⊑ is antisymmetric.
      We check that → satisfies the defining adjunction: for all 𝑎, 𝑏, 𝑥 ∈ 𝐻 ,
                                         𝑎 ⊓ 𝑥 ⊑ 𝑏 ⇐⇒ 𝑥 ⊑ 𝑎 → 𝑏.
         (⇒) If 𝑎 ⊓ 𝑥 ⊑ 𝑏, then 𝑥 ∈ {𝑥 | 𝑎 ⊓ 𝑥 ⊑ 𝑏}, so 𝑥 ⊑ 𝑎 → 𝑏, as 𝑎 → 𝑏 is an upper
               bound of this set.
         (⇐) If 𝑥 ⊑ 𝑎 → 𝑏, then since 𝑎 → 𝑏 itself lies in {𝑥 | 𝑎 ⊓ 𝑥 ⊑ 𝑏}, we have
              𝑎 ⊓ (𝑎 → 𝑏) ⊑ 𝑏. As ⊓ is monotone, 𝑥 ⊑ 𝑎 → 𝑏 gives 𝑎 ⊓ 𝑥 ⊑ 𝑎 ⊓ (𝑎 → 𝑏) ⊑ 𝑏.
         Hence → satisfies the adjunction property, so (𝐻, ⊑, ⊓, ⊔, →) is a Heyting algebra
                                                                                                      □
  Lemma B.4 (Join Below Weighted Addition). Let W = (𝑊 , ⊕, 0, ⊗) be a monoid-module over
a monoid M whose natural order admits the binary join 𝑝 ⊔ 𝑞. Then
                                                 𝑝 ⊔ 𝑞 ⊑ 𝑝 ⊕ 𝑞.
  Proof. We have 𝑝 ⊑ 𝑝 ⊕ 𝑞 and 𝑞 ⊑ 𝑝 ⊕ 𝑞 by the definition of the natural order. Hence 𝑝 ⊕ 𝑞 is
an upper bound of 𝑝 and 𝑞, so the least upper bound must satisfy 𝑝 ⊔ 𝑞 ⊑ 𝑝 ⊕ 𝑞.              □
   Recall Theorem 3.7 from Page 9:
  Theorem 3.7. For any totally ordered bounded lattice (𝐻, ⊑), we obtain a bi-Heyting algebra
H = (𝐻, ⊑, ⊓, ⊔, →tot, ←tot ), with the (co-)implications
                          (                   )                  (              )
                             ⊤, if 𝑎 ⊑ 𝑏,                          ⊥, if 𝑏 ⊑ 𝑎,
              𝑎 →tot 𝑏 =                          and 𝑎 ←tot 𝑏 =                  .
                             𝑏, otherwise                         𝑏, otherwise
   Proof. We show that H = (𝐻, ⊑, ⊓, ⊔, →tot, ←tot ) is a bi-Heyting algebra by showing that
(𝐻, ⊑, ⊓, ⊔, →tot ) and (𝐻, ⊑, ⊓, ⊔, ←tot ) are (co-)Heyting algebras via the statement in Lemma 3.6.
   For all 𝑎, 𝑏 ∈ 𝐻 with 𝑎 ⊑ 𝑏, we observe that 𝑥 := (𝑎 →tot 𝑏) = ⊤. This is the greatest element in
𝐻 and satisfies 𝑎 ⊓ 𝑥 = 𝑎 ⊓ ⊤ = 𝑎 ⊑ 𝑏. For 𝑎 ̸⊑ 𝑏, we obtain 𝑥 := (𝑎 →tot 𝑏) = 𝑏 and the inequality
𝑎 ⊓ 𝑥 = 𝑎 ⊓ 𝑏 = 𝑏 ⊑ 𝑏 is satisfied. There exists no greater element 𝑏 ′ ∈ 𝐻 such that 𝑎 ⊓ 𝑏 ′ ⊑ 𝑏, since
then 𝑏 ′ ̸⊑ 𝑏 and 𝑏 ̸⊑ 𝑏 ′ hold, which is a contradiction. Thus (𝐻, ⊑, ⊓, ⊔, →tot ) is a Heyting algebra.
   Now we consider 𝑎, 𝑏 ∈ 𝐻 with 𝑏 ⊑ 𝑎 and observe that 𝑥 := (𝑎 ←tot 𝑏) = ⊥. This is the least
element in 𝐻 and satisfies 𝑏 ⊑ 𝑎 = 𝑎 ⊔ ⊥ = 𝑎 ⊔ 𝑥. For 𝑏 ̸⊑ 𝑎, we obtain 𝑥 := (𝑎 ←tot 𝑏) = 𝑏, which
satisfies 𝑏 ⊑ 𝑏 = 𝑎 ⊔ 𝑏 = 𝑎 ⊔ 𝑥. Assume that there exists a smaller element 𝑏 ′ ∈ 𝐻 that satisfies the
34                                                                        Ahrens, Rode, Schröer, and Katoen


inequality 𝑏 ⊑ 𝑏 ′ = 𝑎 ⊔ 𝑏 ′ . This is a contradiction with 𝑏 ̸⊑ 𝑏 ′ and hence 𝑎 ←tot 𝑏 always yields the
least element that satisfies 𝑏 ⊑ 𝑎 ⊔ 𝑥 and (𝐻, ⊑, ⊓, ⊔, ←tot ) is a co-Heyting algebra.                 □
   Theorem 3.9. For any Boolean algebra (𝐻, ⊑, ¬) with ⊓ and ⊔ defined, we obtain a bi-Heyting
algebra H = (𝐻, ⊑, ⊓, ⊔, →bool, ←bool ) with 𝑎 →bool 𝑏 = ¬𝑎 ⊔ 𝑏 and 𝑎 ←bool 𝑏 = ¬𝑎 ⊓ 𝑏.
  Proof. We verify the Heyting and co-Heyting adjunctions directly.
Implication. Define 𝑎 →bool 𝑏 := ¬𝑎 ⊔ 𝑏. We show that, for all 𝑎, 𝑏, 𝑥 ∈ 𝐻 ,
                                   𝑎 ⊓𝑥 ⊑𝑏      ⇐⇒       𝑥 ⊑ ¬𝑎 ⊔ 𝑏.
First assume 𝑎 ⊓ 𝑥 ⊑ 𝑏. Since 𝑎 ⊔ ¬𝑎 = ⊤, distributivity gives
                𝑥 = 𝑥 ⊓ ⊤ = 𝑥 ⊓ (𝑎 ⊔ ¬𝑎) = (𝑥 ⊓ 𝑎) ⊔ (𝑥 ⊓ ¬𝑎) ⊑ 𝑏 ⊔ ¬𝑎 = ¬𝑎 ⊔ 𝑏.
Conversely, assume 𝑥 ⊑ ¬𝑎 ⊔ 𝑏. Then
               𝑎 ⊓ 𝑥 ⊑ 𝑎 ⊓ (¬𝑎 ⊔ 𝑏) = (𝑎 ⊓ ¬𝑎) ⊔ (𝑎 ⊓ 𝑏) = ⊥ ⊔ (𝑎 ⊓ 𝑏) = 𝑎 ⊓ 𝑏 ⊑ 𝑏.
Hence 𝑎 →bool 𝑏 = ¬𝑎 ⊔ 𝑏 satisfies the Heyting adjunction.
Co-implication. Define 𝑎 ←bool 𝑏 := ¬𝑎 ⊓ 𝑏. We show that, for all 𝑎, 𝑏, 𝑥 ∈ 𝐻 ,
                                   𝑏 ⊑ 𝑎 ⊔𝑥     ⇐⇒       ¬𝑎 ⊓ 𝑏 ⊑ 𝑥 .
First assume 𝑏 ⊑ 𝑎 ⊔ 𝑥. Then
           ¬𝑎 ⊓ 𝑏 ⊑ ¬𝑎 ⊓ (𝑎 ⊔ 𝑥) = (¬𝑎 ⊓ 𝑎) ⊔ (¬𝑎 ⊓ 𝑥) = ⊥ ⊔ (¬𝑎 ⊓ 𝑥) = ¬𝑎 ⊓ 𝑥 ⊑ 𝑥 .
Conversely, assume ¬𝑎 ⊓ 𝑏 ⊑ 𝑥. Since 𝑎 ⊔ ¬𝑎 = ⊤, distributivity gives
                      𝑏 = 𝑏 ⊓ ⊤ = 𝑏 ⊓ (𝑎 ⊔ ¬𝑎) = (𝑏 ⊓ 𝑎) ⊔ (𝑏 ⊓ ¬𝑎) ⊑ 𝑎 ⊔ 𝑥 .
Hence 𝑎 ←bool 𝑏 = ¬𝑎 ⊓ 𝑏 satisfies the co-Heyting adjunction.
  Therefore H = (𝐻, ⊑, ⊓, ⊔, →bool, ←bool ) is a bi-Heyting algebra.                                     □
 Theorem 3.11. For every finite set of variables 𝐴, the carrier pDNF of the Why monoid-module
Wwhy forms a bi-Heyting algebra (pDNF, ⊑, ∧, ∨, →pDNF, ←pDNF ).
   Proof. Since pDNF(𝐴) is defined modulo logical equivalence over the finite atom set 𝐴, it is
finite. The propositional operations ∧ and ∨ respect logical equivalence, so they are well-defined
on pDNF(𝐴). Ordered by entailment, pDNF(𝐴) is a finite distributive lattice with meet ∧, join ∨,
bottom 0, and top 1. Ô
   In particular, 𝑋 = {𝑅 ∈ pDNF(𝐴) | 𝑃 ∧ 𝑅 ⊑ 𝑄 } exists for all 𝑃, 𝑄 ∈ pDNF(𝐴), since pDNF(𝐴)
is finite. What remains to be shown is that 𝑋 is indeed the greatest element satisfying the condition,
i.e. 𝑃 ∧ 𝑋 ⊑ 𝑄. By finite distributivity,
                                 Ü
                       𝑃 ∧𝑋 =        {𝑃 ∧ 𝑅 | 𝑅 ∈ pDNF(𝐴), 𝑃 ∧ 𝑅 ⊑ 𝑄 } ⊑ 𝑄.
Thus 𝑋 is the greatest element 𝑍 satisfying 𝑃 ∧ 𝑍 ⊑ 𝑄. This proofs that (pDNF(𝐴), ⊑, ∧, ∨, →) is a
Heyting algebra by Lemma 3.6.
   To show the dual statement, define 𝑌 = {𝑅 ∈ pDNF(𝐴) | 𝑄 ⊑ 𝑃 ∨ 𝑅} . The same argument
                                             Ó
as above shows that 𝑌 is the least element satisfying 𝑄 ⊑ 𝑃 ∨ 𝑌 , so (pDNF(𝐴), ⊑, ∧, ∨, ←) is a
co-Heyting algebra. Combining both statements, we conclude that (pDNF(𝐴), ⊑, ∧, ∨, →, ←) is a
bi-Heyting algebra.                                                                             □
   Lemma B.5. Let the 𝜔-bicontinuous module W = (𝑊 , ⊕, 0, ⊗) over the monoid
                                                                        Ã     M = (𝑀, ⊙, 1) be
also
d    a bi-Heyting algebra. Then for all countable 𝐴 ⊆ W, the supremum     𝐴 ∈ W and infimum
   𝐴 ∈ W exists.
Towards a Verification Infrastructure for wGCL                                                       35


   Proof. If 𝐴 = ∅, then 𝐴 = ⊥ and 𝐴 = ⊤ exist because the bi-Heyting algebra is bounded.
                        Ã         d
Hence assume 𝐴 is nonempty and choose an enumeration (𝑎𝑖 )𝑖 ∈N of 𝐴. We construct a sequence
(𝑏𝑖 )𝑖 ∈N ⊆ W such that          Ä       Ä       Ä
                                    𝐴=      𝑎𝑖 =   𝑏𝑖 .
                                                 𝑖 ∈N    𝑖 ∈N
    Define 𝑏 0 := 𝑎 0 and 𝑏𝑖+1 := 𝑏𝑖 ⊔ 𝑎𝑖+1 ∈ W, which is well-defined since the supremum of two
elements
     Ã exists in a Heyting algebra. We observe         that (𝑏𝑖 )𝑖 ∈N is an ascending 𝜔-chain and hence
𝐿 = 𝑖 ∈N 𝑏𝑖 ∈ W exists. This implies that 𝐴 ∈ W exists.
                                               Ã
   We further show that 𝐿 is the supremum of 𝐴. First, 𝐿 is an upper bound of all 𝑎𝑖 since 𝑎𝑖 ⊑
𝑎 0 ⊔ . . . ⊔ 𝑎𝑖 = 𝑏𝑖 ⊑ 𝐿 for all 𝑖 ∈ N. Second, 𝐿 is the least such upper bound. Let 𝐿 ′ be an upper
bound of 𝐴, so 𝑎𝑖 ⊑ 𝐿 ′ for all 𝑖 ∈ N. We show by induction that 𝑏𝑛 ⊑ 𝐿 ′ for all 𝑛 ∈ N. As a base
case, we have 𝑏 0 = 𝑎 0 ⊑ 𝐿 ′ . For the induction step, we assume that 𝑏𝑛 ⊑ 𝐿 ′ and further note that
by definition 𝑎𝑛+1 ⊑ 𝐿 ′ . Hence 𝐿 ′ is an upper bound of both 𝑏𝑛 and 𝑎𝑛+1 , so 𝑏𝑛+1 = 𝑏𝑛 ⊔ 𝑎𝑛+1 ⊑ 𝐿 ′ .
Thus, 𝐿 ′ is an upper bound of the chain (𝑏𝑖 )𝑖 ∈N . Since 𝐿 is the least upperÃ bound of this chain, we
conclude that 𝐿 ⊑ 𝐿 ′ . So 𝐿 is the least upper bound of 𝐴. Consequently, 𝑖 ∈N 𝑎𝑖 = 𝐿. The proof for
infima is analogous.                                                                                   □
   Theorem 4.2. If the module W = (𝑊 , ⊕, 0, ⊗) over the monoid M = (𝑀, ⊙, 1) is 𝜔-bicontinuous
and a bi-Heyting algebra, then the semantics of the wHeyLo formulae are well-defined.
   Proof. To show well-definedness, we need to prove that the formulae 𝑥 𝜑 (and 𝑥 𝜑) evaluate
                                                                        d          Ã
to elements in the module W for all formulae 𝜑 ∈ wHeyLo. Since the module is 𝜔-bicontinuous,
we only know that suprema (and infima) of ascending (and descending) 𝜔-chains are well-defined.
   However, Lemma B.5 states that suprema (and infima) of countable sets exist in 𝜔-bicontinuous
monoid-module that are bi-Heyting algebras. Hence we need to show that the set
                                     
                                       J𝜑K(𝜎 [𝑥 ↦→ 𝑛]) | 𝑛 ∈ N
is countable for all 𝜑 ∈ wHeyLo. This holds directly, since the natural numbers N are countable. □
   Heyting algebras can also be defined in an axiomatic way.
   Theorem B.6 (Heyting Algebra Axioms). A bounded lattice (𝐻, ⊑, ⊓, ⊔) with a binary implica-
tion →: 𝐻 × 𝐻 → 𝐻 is a Heyting algebra H = (𝐻, ⊑, ⊓, ⊔, →) if and only if the following conditions
hold for all 𝑎, 𝑏, 𝑐 ∈ 𝐻 :
    (1) (𝑎 → 𝑎) = ⊤,
    (2) 𝑎 ⊓ (𝑎 → 𝑏) = 𝑎 ⊓ 𝑏,
    (3) 𝑏 ⊓ (𝑎 → 𝑏) = 𝑏,
    (4) 𝑎 → (𝑏 ⊓ 𝑐) = (𝑎 → 𝑏) ⊓ (𝑎 → 𝑐).
   Proof. See [24].                                                                                  □

   Proposition B.7 (Properties of Bi-Heyting Algebras). Let H = (𝐻, ⊑, ⊓, ⊔, →, ←) be a
bi-Heyting algebra. Then the following properties hold for all 𝑎, 𝑏, 𝑐 ∈ 𝐻 :
    (1) 𝑎 ⊑ 𝑏 ⇐⇒ 𝑎 → 𝑏 = ⊤,                                                       (→ internalizes ⊑)
    (2) 𝑎 ⊑ 𝑏 ⇐⇒ 𝑏 ← 𝑎 = ⊥,                                                       (← internalizes ⊑)
    (3) 𝑏 ⊑ 𝑐 =⇒ 𝑎 → 𝑏 ⊑ 𝑎 → 𝑐,                                              (𝑎 → (−) is monotone)
    (4) 𝑏 ⊑ 𝑐 =⇒ 𝑎 ← 𝑏 ⊑ 𝑎 ← 𝑐,                                              (𝑎 ← (−) is monotone)
    (5) 𝑏 ⊑ 𝑐 =⇒ 𝑐 → 𝑎 ⊑ 𝑏 → 𝑎,                                                ((−) → 𝑎 is antitone)
    (6) 𝑏 ⊑ 𝑐 =⇒ 𝑐 ← 𝑎 ⊑ 𝑏 ← 𝑎,                                                ((−) ← 𝑎 is antitone)
   Proof.
36                                                                                             Ahrens, Rode, Schröer, and Katoen


Statement 1. Proof that 𝑎 ⊑ 𝑏 iff 𝑎 → 𝑏 = ⊤:
 (⇒) Assume 𝑎 ⊑ 𝑏. Then 𝑎 ⊓ ⊤ = 𝑎 ⊑ 𝑏. Using Lemma 3.6
                             𝑎 → 𝑏 = sup 𝑥 ∈ 𝐻 | 𝑎 ⊓ 𝑥 ⊑ 𝑏 = ⊤
                                        

holds, since ⊤ is in the set and is the greatest element in 𝐻 .
 (⇐) Assume 𝑎 → 𝑏 = ⊤. By the definition of the implication
                                              𝑎 ⊓ ⊤ ⊑ 𝑏 =⇒ 𝑎 ⊑ 𝑏.
The proofs for all the co-Heyting properties follow dually. As an example, we show the proof for
Statement 2, but omit the rest.
Statement 2. Proof that 𝑎 ⊑ 𝑏 iff 𝑏 ← 𝑎 = ⊥:
 (⇒) Assume 𝑎 ⊑ 𝑏. Then 𝑎 ⊑ ⊥ ⊔ 𝑏. Using the dual of Lemma 3.6:
                               𝑏 ← 𝑎 = inf 𝑥 ∈ 𝐻 | 𝑎 ⊑ 𝑥 ⊔ 𝑏 = ⊥
                                           

holds, since ⊥ is in the set and is the least element in 𝐻 .
 (⇐) Assume 𝑏 ← 𝑎 = ⊥. By definition of the co-implication:
                                𝑏 ← 𝑎 ⊑ ⊥ =⇒ 𝑎 ⊑ 𝑏 ⊔ ⊥ =⇒ 𝑎 ⊑ 𝑏.
Implications 3 and 4. Proof that 𝑏 ⊑ 𝑐 =⇒ 𝑎 → 𝑏 ⊑ 𝑎 → 𝑐:
 (⇒) Assume 𝑏 ⊑ 𝑐. Then 𝑎 ⊓ (𝑎 → 𝑏) = 𝑎 ⊓ 𝑏 ⊑ 𝑏 ⊑ 𝑐. Together with Lemma 3.6, we have:
                            𝑎 → 𝑐 = sup 𝑥 ∈ 𝐻 | 𝑎 ⊓ 𝑥 ⊑ 𝑐 ⊒ 𝑎 → 𝑏.
                                        

Implications 5 and 6. Proof that 𝑏 ⊑ 𝑐 =⇒ 𝑐 → 𝑎 ⊑ 𝑏 → 𝑎:
                                                                           Thm. B.6
 (⇒) Assume 𝑏 ⊑ 𝑐. Then 𝑏 ⊓ (𝑐 → 𝑎) ⊑ 𝑐 ⊓ (𝑐 → 𝑎) = 𝑐 → 𝑎 ⊑ 𝑎. Again, we can use Lemma 3.6:
                         𝑏 → 𝑎 = sup 𝑥 ∈ 𝐻 | 𝑏 ⊓ 𝑥 ⊑ 𝑎 ⊒ 𝑐 → 𝑎.
                                     

                                                                                                                              □

   Lemma B.8 (Order Characterization of Existing Suprema and Infima). Let (𝐻, ⊑) be a
partially
Ã          ordered set, let 𝐼 be an index set, and let {𝑎𝑖 }𝑖 ∈𝐼 be a family of elements in 𝐻 . If the supremum
  𝑖 ∈𝐼 𝑎𝑖 exists, then for every 𝑐 ∈ 𝐻 ,
                                     Ä
                                         𝑎𝑖 ⊑ 𝑐       iff      ∀𝑖 ∈ 𝐼 . 𝑎𝑖 ⊑ 𝑐.
                                    𝑖 ∈𝐼
                 d
If the infimum     𝑖 ∈𝐼 𝑎𝑖 exists, then for every 𝑐 ∈ 𝐻 ,
                                           l
                                   𝑐⊑             𝑎𝑖          iff          ∀𝑖 ∈ 𝐼 . 𝑐 ⊑ 𝑎𝑖 .
                                           𝑖 ∈𝐼

   Proof. We prove the supremum case; the infimum case is dual. Let 𝑠 := 𝑖 ∈𝐼 𝑎𝑖 and let 𝑐 ∈ 𝐻 .
                                                                                 Ã
If 𝑠 ⊑ 𝑐, then 𝑎𝑖 ⊑ 𝑠 ⊑ 𝑐 for every 𝑖 ∈ 𝐼 , because 𝑠 is an upper bound of the family. Conversely,
if 𝑎𝑖 ⊑ 𝑐 for every 𝑖 ∈ 𝐼 , then 𝑐 is an upper bound of the family. Since 𝑠 is the least upper bound,
𝑠 ⊑ 𝑐.                                                                                             □

   Lemma B.9 (Lattice Preservation of Existing Extrema). Let H = (𝐻, ⊑, ⊓, ⊔, →, ←) be a
bi-Heyting algebra. Let 𝐼 be an index set, let {𝑎𝑖 }𝑖 ∈𝐼 be a family of elements in 𝐻 , and let 𝑐 ∈ 𝐻 . If the
     Ã           Ã
joins 𝑖 ∈𝐼 𝑎𝑖 and 𝑖 ∈𝐼 (𝑐 ⊓ 𝑎𝑖 ) exist, then
                                             Ä          Ä
                                         𝑐⊓      𝑎𝑖 =      (𝑐 ⊓ 𝑎𝑖 ).
                                                       𝑖 ∈𝐼         𝑖 ∈𝐼
Towards a Verification Infrastructure for wGCL                                                               37

               d                d
If the meets    𝑖 ∈𝐼 𝑎𝑖 and     𝑖 ∈𝐼 (𝑐 ⊔ 𝑎𝑖 ) exist, then
                                                        l                l
                                                   𝑐⊔          𝑎𝑖 =             (𝑐 ⊔ 𝑎𝑖 ).
                                                        𝑖 ∈𝐼             𝑖 ∈𝐼
   Proof. We first prove preservation of existing joins by meet. For every 𝑑 ∈ 𝐻 ,
                        Ä                 Ä
                     𝑐⊓     𝑎𝑖 ⊑ 𝑑 iff        𝑎𝑖 ⊑ 𝑐 → 𝑑                        (adjunction for →)
                                𝑖 ∈𝐼                       𝑖 ∈𝐼
                                                   iff ∀𝑖 ∈ 𝐼 . 𝑎𝑖 ⊑ 𝑐 → 𝑑                        (Lemma B.8)
                                                   iff ∀𝑖 ∈ 𝐼 . 𝑐 ⊓ 𝑎𝑖 ⊑ 𝑑                   (adjunction for →)
                                                       Ä
                                                   iff     (𝑐 ⊓ 𝑎𝑖 ) ⊑ 𝑑.                         (Lemma B.8)
                                                           𝑖 ∈𝐼
We now prove preservation of existing meets by join. For every 𝑑 ∈ 𝐻 ,
                           l                     l
                   𝑑 ⊑ 𝑐 ⊔ 𝑎𝑖 iff 𝑐 ← 𝑑 ⊑            𝑎𝑖                                      (adjunction for ←)
                                       𝑖 ∈𝐼                                 𝑖 ∈𝐼
                                                   iff ∀𝑖 ∈ 𝐼 . 𝑐 ← 𝑑 ⊑ 𝑎𝑖                        (Lemma B.8)
                                                   iff ∀𝑖 ∈ 𝐼 . 𝑑 ⊑ 𝑐 ⊔ 𝑎𝑖                   (adjunction for ←)
                                                           l
                                                   iff 𝑑 ⊑ (𝑐 ⊔ 𝑎𝑖 ).                             (Lemma B.8)
                                                                  𝑖 ∈𝐼
Since both statements hold for every 𝑑 ∈ 𝐻 , reflexivity and antisymmetry yields the claim.                  □

   Lemma B.10 (Meet Preservation of Implication). Let H = (𝐻, ⊑, ⊓, ⊔, →) be a Heyting algebra.
Let 𝐼 be an arbitrary indexdset and letd{𝑏𝑖 }𝑖 ∈𝐼 be a family of elements in 𝐻 indexed by 𝐼 . For any
element 𝑎 ∈ 𝐻 , if the meet 𝑖 ∈𝐼 𝑏𝑖 and 𝑖 ∈𝐼 (𝑎 → 𝑏𝑖 ) exist, then
                                          l          l
                                      𝑎→        𝑏𝑖 = (𝑎 → 𝑏𝑖 ).
                                                        𝑖 ∈𝐼             𝑖 ∈𝐼
   Proof. For every 𝑐 ∈ 𝐻 ,
                                       l                                  l
                        𝑐 ⊑𝑎→                 𝑏𝑖   iff 𝑎 ⊓ 𝑐 ⊑                   𝑏𝑖          (adjunction for →)
                                       𝑖 ∈𝐼                               𝑖 ∈𝐼
                                                   iff ∀𝑖 ∈ 𝐼 . 𝑎 ⊓ 𝑐 ⊑ 𝑏𝑖                        (Lemma B.8)
                                                   iff ∀𝑖 ∈ 𝐼 . 𝑐 ⊑ 𝑎 → 𝑏𝑖                   (adjunction for →)
                                                           l
                                                   iff 𝑐 ⊑ (𝑎 → 𝑏𝑖 ).                             (Lemma B.8)
                                                                  𝑖 ∈𝐼
Since this holds for every 𝑐 ∈ 𝐻 , reflexivity and antisymmetry yields the claim.                            □
   Lemma B.11 (Join Preservation of Coimplication). Let H = (𝐻, ⊑, ⊓, ⊔, →, ←) be a bi-Heyting
algebra. Let 𝐼 be an index set, let {𝑏𝑖 }𝑖 ∈𝐼 be a family of elements in 𝐻 , and let 𝑎 ∈ 𝐻 . If the joins
Ã             Ã
  𝑖 ∈𝐼 𝑏𝑖 and  𝑖 ∈𝐼 (𝑎 ← 𝑏𝑖 ) exist, then
                                              Ä       Ä
                                        𝑎←       𝑏𝑖 =    (𝑎 ← 𝑏𝑖 ).
                                                        𝑖 ∈𝐼             𝑖 ∈𝐼
   Proof. For every 𝑐 ∈ 𝐻 ,
                    Ä
                        (𝑎 ← 𝑏𝑖 ) ⊑ 𝑐                iff ∀𝑖 ∈ 𝐼 . 𝑎 ← 𝑏𝑖 ⊑ 𝑐                      (Lemma B.8)
                         𝑖 ∈𝐼
                                                     iff ∀𝑖 ∈ 𝐼 . 𝑏𝑖 ⊑ 𝑎 ⊔ 𝑐                 (adjunction for ←)
38                                                                                          Ahrens, Rode, Schröer, and Katoen

                                                            Ä
                                                     iff             𝑏𝑖 ⊑ 𝑎 ⊔ 𝑐                                (Lemma B.8)
                                                             𝑖 ∈𝐼
                                                                         Ä
                                                     iff 𝑎 ←                      𝑏𝑖 ⊑ 𝑐.                (adjunction for ←)
                                                                         𝑖 ∈𝐼

Since this holds for every 𝑐 ∈ 𝐻 , reflexivity and antisymmetry yields the claim.                                          □

   Lemma B.12 (Implication Turns Joins into Meets). Let H = (𝐻, ⊑, ⊓, ⊔, →) be a Heyting
algebra.                 d index set, let {𝑎𝑖 }𝑖 ∈𝐼 be a family of elements in 𝐻 , and let 𝑏 ∈ 𝐻 . If the
     Ã Let 𝐼 be an arbitrary
join 𝑖 ∈𝐼 𝑎𝑖 and the meet 𝑖 ∈𝐼 (𝑎𝑖 → 𝑏) exist, then
                                          !
                                    Ä                l
                                        𝑎𝑖 → 𝑏 = (𝑎𝑖 → 𝑏).
                                             𝑖 ∈𝐼                           𝑖 ∈𝐼

     Proof. For every 𝑐 ∈ 𝐻 ,
                                     !                                     !
                             Ä                              Ä
                    𝑐⊑              𝑎𝑖 → 𝑏          iff              𝑎𝑖 ⊓ 𝑐 ⊑ 𝑏                          (adjunction for →)
                             𝑖 ∈𝐼                           𝑖 ∈𝐼
                                                                                   !
                                                                    Ä
                                                    iff 𝑐 ⊓                    𝑎𝑖 ⊑ 𝑏                 (commutativity of ⊓)
                                                                     𝑖 ∈𝐼
                                                           Ä
                                                    iff           𝑎𝑖 ⊑ 𝑐 → 𝑏                             (adjunction for →)
                                                           𝑖 ∈𝐼
                                                    iff ∀𝑖 ∈ 𝐼 . 𝑎𝑖 ⊑ 𝑐 → 𝑏                                    (Lemma B.8)
                                                    iff ∀𝑖 ∈ 𝐼 . 𝑐 ⊓ 𝑎𝑖 ⊑ 𝑏                              (adjunction for →)
                                                    iff ∀𝑖 ∈ 𝐼 . 𝑎𝑖 ⊓ 𝑐 ⊑ 𝑏                           (commutativity of ⊓)
                                                    iff ∀𝑖 ∈ 𝐼 . 𝑐 ⊑ 𝑎𝑖 → 𝑏                              (adjunction for →)
                                                            l
                                                    iff 𝑐 ⊑ (𝑎𝑖 → 𝑏).                                          (Lemma B.8)
                                                                  𝑖 ∈𝐼

Since 𝑐 ∈ 𝐻 was arbitrary, reflexivity and antisymmetry yields the claim.                                                  □

  Lemma B.13 (Coimplication Turns Meets into Joins). Let H = (𝐻, ⊑, ⊓, ⊔, →, ←) be a bi-
Heyting                  Ã index set, let {𝑎𝑖 }𝑖 ∈𝐼 be a family of elements in 𝐻 , and let 𝑏 ∈ 𝐻 . If the
     d algebra. Let 𝐼 be an
meet 𝑖 ∈𝐼 𝑎𝑖 and the join 𝑖 ∈𝐼 (𝑎𝑖 ← 𝑏) exist, then
                                          !
                                    l                Ä
                                       𝑎𝑖 ← 𝑏 =          (𝑎𝑖 ← 𝑏).
                                             𝑖 ∈𝐼                          𝑖 ∈𝐼

     Proof. For every 𝑐 ∈ 𝐻 ,
                     Ä
                        (𝑎𝑖 ← 𝑏) ⊑ 𝑐                iff ∀𝑖 ∈ 𝐼 . 𝑎𝑖 ← 𝑏 ⊑ 𝑐                                    (Lemma B.8)
                      𝑖 ∈𝐼
                                                    iff ∀𝑖 ∈ 𝐼 . 𝑏 ⊑ 𝑎𝑖 ⊔ 𝑐                              (adjunction for ←)
                                                            l
                                                    iff 𝑏 ⊑ (𝑎𝑖 ⊔ 𝑐)                                           (Lemma B.8)
                                                                    𝑖 ∈𝐼
                                                                                   !
                                                                     l
                                                    iff 𝑏 ⊑                    𝑎𝑖 ⊔ 𝑐                          (Lemma B.9)
                                                                     𝑖 ∈𝐼
Towards a Verification Infrastructure for wGCL                                                               39

                                                               !
                                                       l
                                                 iff          𝑎𝑖 ← 𝑏 ⊑ 𝑐.                    (adjunction for ←)
                                                       𝑖 ∈𝐼

Since this holds for every 𝑐 ∈ 𝐻 , reflexivity and antisymmetry yield the claim.                             □

B.1    An Exemplary Lightweight Encoding of Weighted NetKAT
Weighted NetKAT [1] is parametric in an 𝜔-continuous semiring. By Lemma A.2, every such
semiring induces an instance of wGCL. We represent a Weighted NetKAT packet by a wGCL
program state: each packet field becomes one program variable. Since Weighted NetKAT assumes
finite field domains, symbolic values such as switches, hosts, and ports can be encoded by natural
numbers. The following lightweight translation is not supposed to reproduce the Weighted NetKAT
automata construction. Instead, it aims to show that the scalar verification problems expressible by
their policies can be phrased as weakest-preweighting bounds of wGCL programs, which we can
verify in our framework.
   For every Weighted NetKAT test 𝑡, let 𝐵𝑡 be the corresponding Boolean expression over the
packet variables. We write T (𝑝) for the wGCL command obtained by translating the Weighted
NetKAT policy 𝑝. The structural translation is:

           wNetKAT policy         meaning                              wGCL encoding
           𝑡                      filter packets by test 𝑡             if ( 𝐵𝑡 ) { ⊗ 1 } else { ⊗ 0 }
           𝑓 ←𝑛                   update field 𝑓                       𝑓 := 𝑛
           𝑟 ⊙𝑝                   run 𝑝 with weight 𝑟                  ⊗ 𝑟 # T (𝑝)
           𝑝 ⊕𝑞                   choose between policies              { T (𝑝) } ⊕ { T (𝑞) }
           𝑝; 𝑞                   run 𝑝, then 𝑞                        T (𝑝) # T (𝑞)
           𝑝∗                     finitely many repetitions            see below
           dup                    log packet history                   ⊗1

   The only nontrivial clause next to dup is Kleene star 𝑝 ∗ . For every occurrence of 𝑝 ∗ , choose a
fresh Boolean control variable 𝑏 not used in T (𝑝) and define
           T (𝑝 ∗ ) ≜ { 𝑏 := 0 } ⊕ { 𝑏 := 1 } # while ( 𝑏 = 1 ) { T (𝑝) # { 𝑏 := 0 } ⊕ { 𝑏 := 1 } } .
   The initial branch chooses whether to execute zero iterations. After every executed copy of
T (𝑝), the program again chooses whether to stop or continue. Thus the loop encoding reproduces
the semantic role of Weighted NetKAT star: it aggregates all finite repetitions of 𝑝. By the Kleene-
iteration semantics of wGCL loops and the definition of countable sums in 𝜔-continuous modules
[7, Thm. 4.7, Def. A.15 and Eq. (6)], the resulting weakest preweighting is
                                                  Ê
                              wpJT (𝑝 ∗ )K(𝑤) =       wpJT (𝑝)𝑛 K(𝑤),
                                                              𝑛∈N

for postweightings 𝑤 independent of the fresh variable 𝑏, where T (𝑝) 0 is the empty command and
T (𝑝)𝑛+1 = T (𝑝) # T (𝑝)𝑛 .
   The table maps dup to the neutral weight because this is enough for scalar safety and reachability
properties. The role of dup in Weighted NetKAT is to record complete packet histories. To also
track the packet history in our setting, we could add a ghost history variable to the program state,
or abstractly use a monoid-module of 𝑆-weighted languages over guarded strings, i.e. functions
from guarded strings to the semiring carrier 𝑆 that assign a weight to each packet-history trace.
However, we do not need this heavier construction for scalar verification problems.
40                                                                          Ahrens, Rode, Schröer, and Katoen


   Example. Consider the first switch in Figure 2 of Weighted NetKAT [1]. The policy 𝑝 1 is the
forwarding-table policy: it chooses an outgoing port from the destination field. The policy ℓ1 is the
link policy: it follows the link attached to the chosen port. Latencies are therefore attached to ℓ1 ,
not to 𝑝 1 . For packets destined to H2 , the relevant fragment is 𝑝 1 ; ℓ1lat , where
                         𝑝 1 ≜ if dst = H2 then (pt ← 3 ⊕ pt ← 4)
                                 else if dst = H1 then pt ← 1
                                 else drop,
                        ℓ1lat ≜ if pt = 3 then 2 ms ⊙ (sw ← S3 ; pt ← 1)
                                 else if pt = 4 then 4 ms ⊙ (sw ← S4 ; pt ← 1)
                                 else pt = 1.
Writing weights in milliseconds, the translation is
                          T (𝑝 1 ; ℓ1lat ) = T (𝑝 1 ) # T (ℓ1lat )
                               T (𝑝 1 ) ≜ if dst = H2 then
                                              { pt := 3 } ⊕ { pt := 4 }
                                           else if dst = H1 then
                                              pt := 1
                                           else
                                              ⊗0
                              T (ℓ1lat ) ≜ if pt = 3 then
                                              ⊗ 2 # sw := S3 # pt := 1
                                           else if pt = 4 then
                                              ⊗ 4 # sw := S4 # pt := 1
                                           else
                                              if ( pt = 1 ) { ⊗ 1 } else { ⊗ 0 }
If a packet at switch S1 is destined for host H2 , then T (𝑝 1 ) chooses between ports 3 and 4, and
T (ℓ1lat ) contributes the corresponding link weight. Thus the translated program exposes exactly
the branch weights 2 and 4. With the tropical instantiation this yields the best-case latency
                                            2 ⊕ 4 = min{2, 4} = 2,
whereas with the arctic instantiation it yields the worst-case latency 2 ⊕ 4 = max{2, 4} = 4.
   This example illustrates that scalar Weighted NetKAT analyses can be expressed in wGCL.
Weighted NetKAT obtains decision procedures by compiling finite packet-processing policies to
finite automata [1, Sec. 3.1, Sec. 5, Thm. 1]. Our deductive infrastructure has a different scope: using
invariants, it can also reason about parameterized or infinite-state weighted programs, such as the
unbounded network-security case study.
Towards a Verification Infrastructure for wGCL                                                   41


C    Proofs of Section 5: Proof Rules & Encodings in wHeyVL
Theorem 5.1 (Loop-Free Encodings are Exact). For a loop-free program 𝐶 ∈ wGCL and post-
weighting 𝜑 ∈ wHeyLo, we have, for all 𝜎 ∈ Σ, that vpJenc(𝐶)K(𝜑) (𝜎) = wpJ𝐶K(𝜑) (𝜎).

Proof. We proceed by structural induction on 𝐶.
Base cases.
      - Case 𝐶 = 𝑥 := 𝐸.
                            JvpJenc(𝐶)K(𝜑)K
                             = JvpJ𝑥 := 𝐸K(𝜑)K                                      (Def. of enc(·))
                               = J𝜑 [𝑥 ↦→ 𝐸]K                                           (Def. of :=)
                               = 𝜆𝜎 : J𝜑K(𝜎 [𝑥 ↦→ 𝜎 (𝐸)])
                               = wpJ𝑥 := 𝐸K(J𝜑K)

      - Case 𝐶 = ⊙ 𝑎.
                         JvpJenc(𝐶)K(𝜑)K
                          = JvpJweigh 𝑎K(𝜑)K                                        (Def. of enc(·))
                          = J𝑎 · 𝜑K                                                 (Def. of weigh)
                          = 𝑎 ⊙ J𝜑K
                          = wpJ⊙ 𝑎K(J𝜑K)

Inductive cases. Assume the induction hypothesis for arbitrary but fixed 𝐶 1, 𝐶 2 ∈ wGCL.
      - Case 𝐶 = 𝐶 1 ; 𝐶 2 .
                     JvpJenc(𝐶)K(𝜑)K
                      = JvpJenc(𝐶 1 ); enc(𝐶 2 )K(𝜑)K                               (Def. of enc(·))
                      = JvpJenc(𝐶 1 )K(vpJenc(𝐶 2 )K(𝜑))K
                      = wpJ𝐶 1 K(JvpJenc(𝐶 2 )K(𝜑)K)                                          (I.H.)
                      = wpJ𝐶 1 K(wpJ𝐶 2 K(J𝜑K))
                      = wpJ𝐶K(J𝜑K)

      - Case 𝐶 = { 𝐶 1 } ⊕ { 𝐶 2 }.
                    JvpJenc(𝐶)K(𝜑)K
                     = JvpJif (+) {enc(𝐶 1 )} else {enc(𝐶 2 )}K(𝜑)K
                     = JvpJenc(𝐶 1 )K(𝜑) + vpJenc(𝐶 2 )K(𝜑)K                          (Def. if (+))
                     = JvpJenc(𝐶 1 )K(𝜑)K ⊕ JvpJencwp (𝐶 2 )K(𝜑)K
                     = wpJ𝐶 1 K(J𝜑K) ⊕ wpJ𝐶 2 K(J𝜑K)                                          (I.H.)
                     = wpJ𝐶K(J𝜑K)

      - Case 𝐶 = if (𝑏) { 𝐶 1 } else { 𝐶 2 }. For all 𝜎 ∈ Σ.
           JvpJencwp (𝐶)K(𝜑)K(𝜎)
           = JvpJif (⊓){assume ? (𝑏); encwp (𝐶 1 )}
42                                                                          Ahrens, Rode, Schröer, and Katoen


                  else {assume ? (¬𝑏); encwp (𝐶 2 )}K(𝜑)K(𝜎)
          = JvpJassume ? (𝑏); encwp (𝐶 1 )K(𝜑)
                   ⊓ vpJassume ? (¬𝑏); encwp (𝐶 2 )K(𝜑)K(𝜎)                                    (Def. if (⊓))
          = JvpJassume ? (𝑏); encwp (𝐶 1 )K(𝜑)K(𝜎)
                   ⊓ JvpJassume ? (¬𝑏); encwp (𝐶 2 )K(𝜑)K(𝜎)                                        (Def. ⊓)
          = JvpJassume ? (𝑏)K(vpJencwp (𝐶 1 )K(𝜑))K(𝜎)
                   ⊓ JvpJassume ? (¬𝑏)K(vpJencwp (𝐶 2 )K(𝜑))K(𝜎)                                    (Def. =)
          = J? (𝑏) → vpJencwp (𝐶 1 )K(𝜑)K(𝜎)
                   ⊓ J? (¬𝑏) → vpJencwp (𝐶 2 )K(𝜑)K(𝜎)                                        (Def. assume)
          = (J? (𝑏)K(𝜎) → JvpJencwp (𝐶 1 )K(𝜑)K(𝜎))
                   ⊓ (J? (¬𝑏)K(𝜎) → JvpJencwp (𝐶 2 )K(𝜑)K(𝜎))
          = (J? (𝑏)K(𝜎) → wpJ𝐶 1 K(J𝜑K) (𝜎))
                   ⊓ (J? (¬𝑏)K(𝜎) → wpJ𝐶 2 K(J𝜑K) (𝜎))                                                 (I.H.)
              (
                  ⊤ → wpJ𝐶 1 K(J𝜑K) (𝜎) ⊓ ⊥ → wpJ𝐶 2 K(J𝜑K) (𝜎),      if J𝑏K(𝜎) = true
          =
                  ⊥ → wpJ𝐶 1 K(J𝜑K) (𝜎) ⊓ ⊤ → wpJ𝐶 2 K(J𝜑K) (𝜎),      otherwise
              (
                  (⊤ → wpJ𝐶 1 K(J𝜑K) (𝜎)) ⊓ ⊤,     if J𝑏K(𝜎) = true
          =                                                                                 (Definition 3.1)
                  ⊤ ⊓ (⊤ → wpJ𝐶 2 K(J𝜑K) (𝜎)),     otherwise
              (
                  ⊤ → wpJ𝐶 1 K(J𝜑K) (𝜎),    if J𝑏K(𝜎) = true
          =                                                                                 (Definition B.1)
                  ⊤ → wpJ𝐶 2 K(J𝜑K) (𝜎),    otherwise
              (
                  wpJ𝐶 1 K(J𝜑K) (𝜎),   if J𝑏K(𝜎) = true
          =                                                                                 (Definition 3.1)
                  wpJ𝐶 2 K(J𝜑K) (𝜎),   otherwise
          = ([𝑏] wpJ𝐶 1 K(J𝜑K)) (𝜎) ⊕ ([¬𝑏] wpJ𝐶 2 K(J𝜑K)) (𝜎)
          = wpJ𝐶K(J𝜑K) (𝜎)                                                                      □

C.1   Proofs of Section 5.1: Specification Statements
Lemma 5.4 (Semantics). For 𝛽 ⊆ Vars and 𝜌,𝜓, 𝜑 ∈ wHeyLo, and 𝜎 ∈ Σ, the specification statement
encoding specEnc(𝛽 : [𝜌,𝜓 ]) given in Figure 7 satisfies
                                          (
                                            𝜌 (𝜎), if 𝜓 (𝜎 ′ ) ⊑ 𝜑 (𝜎 ′ ) ∀𝜎 ′ ∈ Reach𝛽 (𝜎)
        vpJspecEnc(𝛽 : [𝜌,𝜓 ])K(𝜑) (𝜎) =                                                    .
                                            ⊥,       otherwise

Proof. By the semantics in Table 2 and sequential composition,
                      vpJenc(𝛽 : [𝜌,𝜓 ])K(𝜑) (𝜎)
                       = vpJassert 𝜌; havoc 𝛽; validate; assume 𝜓 K(𝜑) (𝜎)
                       = vpJassert 𝜌K(vpJhavoc 𝛽; validate; assume 𝜓 K(𝜑)) (𝜎)
                       = J𝜌K(𝜎) ⊓ vpJhavoc 𝛽K(vpJvalidate; assume 𝜓 K(𝜑)) (𝜎).
The suffix validate; assume 𝜓 checks whether 𝜓 ⊑ 𝜑 holds and turns this qualitative test into a
boolean-valued weighting. Since havoc 𝛽 ranges over exactly the states in Reach𝛽 (𝜎), the resulting
Towards a Verification Infrastructure for wGCL                                                    43


value is ⊤ iff
                                    ∀𝜎 ′ ∈ Reach𝛽 (𝜎). J𝜓 K(𝜎 ′ ) ⊑ J𝜑K(𝜎 ′ ),
and ⊥ otherwise. Meeting this result with J𝜌K(𝜎) yields the claim.                                □
Theorem 5.5 (Soundness). Let 𝛽 ⊆ Vars, 𝜌,𝜓 ∈ wHeyLo, and 𝐶 ∈ wHeyVL be a statement
that only modifies variables in 𝛽 and satisfies 𝜌 ⊑ vpJ𝐶K(𝜓 ). Then, for all 𝜑 ∈ wHeyLo, we have
vpJspecEnc(𝛽 : [𝜌,𝜓 ])K(𝜑) ⊑ vpJ𝐶K(𝜑).

Proof. Let 𝜎 ∈ Σ be arbitrary.
First assume that
                                    ∀𝜎 ′ ∈ Reach𝛽 (𝜎). J𝜓 K(𝜎 ′ ) ⊑ J𝜑K(𝜎 ′ ).
By Lemma 5.4,
                                    vpJenc(𝛽 : [𝜌,𝜓 ])K(𝜑) (𝜎) = J𝜌K(𝜎).
Since 𝐶 adheres to the specification,
                                            J𝜌K(𝜎) ⊑ vpJ𝐶K(𝜓 ) (𝜎).
Moreover, because 𝐶 may modify only variables in 𝛽, every state that is relevant for evaluating
vpJ𝐶K(·) (𝜎) is contained in Reach𝛽 (𝜎). Hence the assumption above implies that replacing 𝜓 by 𝜑
can only increase the value of the verification preweighting, i.e.
                                         vpJ𝐶K(𝜓 ) (𝜎) ⊑ vpJ𝐶K(𝜑) (𝜎).
Therefore,
                                 vpJenc(𝛽 : [𝜌,𝜓 ])K(𝜑) (𝜎) ⊑ vpJ𝐶K(𝜑) (𝜎).

Otherwise, Lemma 5.4 yields
                              vpJenc(𝛽 : [𝜌,𝜓 ])K(𝜑) (𝜎) = ⊥ ⊑ vpJ𝐶K(𝜑) (𝜎).                      □

C.2    Proofs of Section 5.2: Finite Loop Unrolling
Lemma 5.6 (Finite Loop Unrolling). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, weightings 𝑓 , ℎ ∈
W, and the corresponding characteristic function Φ 𝑓 , we have, for any 𝑛 ∈ N, that
                                   ℎ ⊑ Φ𝑛𝑓 (⊥)    implies ℎ ⊑ wpJ𝐶K(𝑓 ).

Proof. Let Φ 𝑓 be the characteristic function of wpJ𝐶K(𝑓 ). By the loop semantics and Kleene’s
fixed-point theorem,                                      Ä
                           wpJ𝐶K(𝑓 ) = lfp 𝑋 . Φ 𝑓 (𝑋 ) =   Φ𝑚𝑓 (⊥).
                                                                  𝑚∈N
For every 𝑛 ∈ N, the approximant Φ𝑛𝑓 (⊥) is below this supremum. Hence ℎ ⊑ Φ𝑛𝑓 (⊥) implies
ℎ ⊑ wpJ𝐶K(𝑓 ) by transitivity.                                                          □
Lemma 5.7 (Semantics). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, weightings 𝜑, 𝐼 ∈ wHeyLo, an
encoding enc(𝐶 ′ ) with vpJenc(𝐶 ′ )K(𝜓 ) ⊑ wpJ𝐶 ′ K(𝜓 ) for all 𝜓 ∈ wHeyLo, and 𝜎 ∈ Σ, the encoding
of the characteristic function Φ𝜑 (𝐼 ) given in Figure 8 satisfies
                                                   (
                                                     vpJenc(𝐶 ′ )K(𝐼 ) (𝜎), if J𝑏K(𝜎)
                   vpJcharEnc(𝐶, 𝐼 )K(𝜑) (𝜎) =                                        .
                                                    𝜑 (𝜎),                  otherwise
44                                                                              Ahrens, Rode, Schröer, and Katoen


Proof.
     vpJcharEnc(𝐶)𝐼 K(𝜑) (𝜎)
     = vpJif (⊓){assume ? (𝑏); enc(𝐶 ′ ); assert 𝐼 ; assume ? (false)}else {assume ? (¬𝑏)}K(𝜑) (𝜎)
     = (J? (𝑏)K(𝜎) → vpJenc(𝐶 ′ ); assert 𝐼 ; assume ? (false)K(𝜑) (𝜎)) ⊓ (J? (¬𝑏)K(𝜎) → J𝜑K(𝜎))
     = (J? (𝑏)K(𝜎) → vpJenc(𝐶 ′ )K(vpJassert 𝐼 ; assume ? (false)K(𝜑)) (𝜎))
          ⊓ (J? (¬𝑏)K(𝜎) → J𝜑K(𝜎))
     = (J? (𝑏)K(𝜎) → vpJenc(𝐶 ′ )K(𝐼 ) (𝜎)) ⊓ (J? (¬𝑏)K(𝜎) → J𝜑K(𝜎))
       (
         vpJenc(𝐶 ′ )K(𝐼 ) (𝜎), if J𝑏K(𝜎) = true
     =                                                                                                         □
         J𝜑K(𝜎),                otherwise
Lemma 5.8 (Soundness). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, weightings 𝜑, 𝐼 ∈ wHeyLo,
𝑛 ∈ N, and an encoding enc(𝐶 ′ ) with vpJenc(𝐶 ′ )K(𝜓 ) ⊑ wpJ𝐶 ′ K(𝜓 ) for all 𝜓 ∈ wHeyLo, the
encoding charEnc is a sound under-approximation, thus vpJcharEnc(𝐶, ⊥)𝑛 K(𝜑) ⊑ wpJ𝐶K(𝜑).

Proof. By Lemma 5.7 and the soundness assumption on enc(𝐶 ′ ), each characteristic encoding
under-approximates the semantic characteristic function:
                                      vpJcharEnc(𝐶, 𝐼 )K(𝜑) ⊑ Φ𝜑 (𝐼 ).
Therefore, by induction on 𝑛,
                                    vpJcharEnc(𝐶, ⊥)𝑛 K(𝜑) ⊑ Φ𝑛𝜑 (⊥).
The claim follows from Lemma 5.6.                                                                              □

C.3     Proofs of Section 5.3: Local Park Induction
Lemma 5.10 (Closedness under Reachability). For a program 𝐶 ∈ wGCL with local variables
𝛽 ⊆ Vars and a set Γ ⊆ Σ of states that is closed under 𝛽-reachability, wlpJ𝐶K : W → W is closed
under Γ-restricted weightings: for all 𝑓 ∈ W, there exists 𝑔 ∈ W such that wlpJ𝐶K(𝑓 |Γ ) = 𝑔 |Γ .

Proof. We prove by structural induction on 𝐶 that for all global weightings 𝑌 , 𝑍 ∈ W with
𝑌 (𝜎) = 𝑍 (𝜎) for all 𝜎 ∈ Γ, it holds that wlpJ𝐶K(𝑌 ) (𝜎) = wlpJ𝐶K(𝑍 ) (𝜎) for all 𝜎 ∈ Γ. The
corresponding statement for wpJ𝐶K is analogous, but we concentrate on wlpJ𝐶K here.
Base cases.
        - Case 𝐶 = 𝑥 := 𝐸. Since 𝑥 ∈ 𝛽 and Γ is closed under 𝛽-reachability, every successor state
          𝜎 [𝑥 ↦→ J𝐸K(𝜎)] is also in Γ. Hence, for all 𝜎 ∈ Γ,
                                 wlpJ𝑥 := 𝐸K(𝑌 ) (𝜎) = 𝑌 (𝜎 [𝑥 ↦→ J𝐸K(𝜎)])
                                                       = 𝑍 (𝜎 [𝑥 ↦→ J𝐸K(𝜎)])
                                                       = wlpJ𝑥 := 𝐸K(𝑍 ) (𝜎).

        - Case 𝐶 = ⊗ 𝑎 . Immediate from the definition of the weight multiplication: 𝑚 ⊗ 𝑌 depends
          only on 𝑌 (𝜎), and therefore on 𝑍 (𝜎) when 𝑌 and 𝑍 agree on Γ.
Inductive cases. Assume the statement holds for 𝐶 1 and 𝐶 2 .
        - Case 𝐶 = 𝐶 1 ; 𝐶 2 . For all 𝜎 ∈ Γ, the induction hypothesis gives wlpJ𝐶 2 K(𝑌 ) (𝜎) = wlpJ𝐶 2 K(𝑍 ) (𝜎).
          Applying the induction hypothesis to 𝐶 1 then yields the desired equality for 𝐶.
Towards a Verification Infrastructure for wGCL                                                        45


      - Case 𝐶 = { 𝐶 1 } ⊕ { 𝐶 2 }. The semantics of branching is pointwise addition, so the claim
        follows directly from the induction hypothesis on both branches.
      - Case 𝐶 = if ( 𝑏 ) { 𝐶 1 } else { 𝐶 2 }. For 𝜎 ∈ Γ, either 𝑏 (𝜎) or ¬𝑏 (𝜎) holds. In the former
        case, the result is determined by 𝐶 1 ; in the latter by 𝐶 2 . The induction hypothesis therefore
        implies the desired equality for 𝐶.
      - Case 𝐶 = while ( 𝑏 ) { 𝐶 1 }. Let Ψ𝑌 (𝑋 ) = [¬𝑏] · 𝑌 ⊕ [𝑏] · wlpJ𝐶 1 K(𝑋 ) and Ψ𝑍 (𝑋 ) = [¬𝑏] ·
        𝑍 ⊕ [𝑏] · wlpJ𝐶 1 K(𝑋 ). By the induction hypothesis on 𝐶 1 , any two weightings that agree on
        Γ are mapped by wlpJ𝐶 1 K to weightings that also agree on Γ. Hence Ψ𝑌 and Ψ𝑍 agree on Γ
        whenever 𝑌 and 𝑍 do.
        Define the approximants 𝑋 0 = ⊤ and 𝑋𝑛+1 = Ψ𝑌 (𝑋𝑛 ), and analogously 𝑋 0′ = ⊤ and
          ′
        𝑋𝑛+1  = Ψ𝑍 (𝑋𝑛′ ). By induction on 𝑛, each pair 𝑋𝑛 , 𝑋𝑛′ agrees on Γ. Therefore the greatest
        fixed points gfp . Ψ𝑌 and gfp . Ψ𝑍 also agree on Γ. This proves the claim for wlpJ𝐶K.
Finally, closure under Γ-restricted weightings follows from the fact that for any restricted weighting
𝜑 |Γ and any two global extensions 𝑌 , 𝑍 of it, the values of wlpJ𝐶K(𝑌 ) on Γ agree with those of
wlpJ𝐶K(𝑍 ). Thus we may choose 𝜑 ′ = wlpJ𝐶K(𝑌 ) as a global extension of the result. The analogous
argument for wpJ𝐶K is straightforward.                                                               □
Theorem 5.11 (Local Park Induction). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL with local
variables 𝛽 ⊆ Vars, a set Γ ⊆ Σ of states that is closed under 𝛽-reachability, and weightings 𝑓 , 𝐼 ∈ W,
it is
                       𝐼 ⊑Γ Ψ𝑓 (𝐼 ) implies 𝐼 ⊑Γ wlpJwhile ( 𝑏 ) { 𝐶 ′ }K(𝑓 ).

Proof. We assume that the inequality 𝐼 |Γ ⊑Γ Ψ𝑓 (𝐼 |Γ ) holds for an invariant 𝐼 ∈ W. Due to
Lemma 5.10, the transformed weighting Ψ𝑓 (𝐼 |Γ ) : Γ → W is again Γ-restricted. Hence, we can use
monotonicity of Ψ𝑓 and obtain via natural induction on 𝑛 ∈ N that
                                                 𝐼 |Γ ⊑Γ Ψ𝑓𝑛 (𝐼 |Γ ).

Furthermore, we derive via Park induction that 𝐼 |Γ ⊑Γ gfp Ψ𝑓 . =wlpJ𝐶K(𝜑), since the set of Γ-
restricted weightings is an 𝜔-bicomplete partially ordered set and the weighting transformer Ψ𝑓 is
𝜔-bicontinuous.                                                                                 □

Lemma C.1 (Semantics of Encoding). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL with local variables
𝛽 ⊆ Vars, weightings 𝜑, 𝐼 ∈ wHeyLo, and an encoding enc(𝐶 ′ ) with vpJenc(𝐶 ′ )K(𝜓 ) ⊑ wpJ𝐶 ′ K(𝜓 )
for all 𝜓 ∈ wHeyLo, the encoding of Park induction in Figure 8 satisfies
                                                 (
                                                   𝐼 (𝜎), if 𝐼 ⊑Reach𝛽 (𝜎 ) Ψ𝑓 (𝐼 )
                   vpJparkEnc(𝐶, 𝐼 )K(𝜑) (𝜎) ⊑
                                                   ⊥,     otherwise .

Proof. Since the encoding of local Park induction is the sequential composition of the specification
statement encoding and the characteristic function encoding, we calculate the semantics using
Lemma 5.4 and Lemma 5.7 by
                             vpJparkEnc(𝐶, 𝐼 )K(𝜑) (𝜎)
                           = vpJspecEnc(𝛽 : [𝐼, 𝐼 ])K(vpJcharEnc(𝐶, 𝐼 ) (𝜑)K) (𝜎)
                             (
                               𝐼 (𝜎), if 𝐼 ⊑Reach𝛽 (𝜎 ) vpJcharEnc(𝐶, 𝐼 )K(𝜑)
                           =
                               ⊥(𝜎), otherwise
46                                                                                Ahrens, Rode, Schröer, and Katoen

                           (
                               𝐼 (𝜎),   if 𝐼 (𝜎 ′ ) ⊑Reach𝛽 (𝜎 ) Ψ𝜑 (𝐼 ) (𝜎 ′ )
                       ⊑
                               ⊥(𝜎),    otherwise.
                                                                                                                 □
Theorem 5.12 (Soundness). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL with local variables 𝛽 ⊆ Vars
and weightings 𝜑, 𝐼 ∈ wHeyLo, the encoding parkEnc is a sound under-approximation, thus
                                 vpJparkEnc(𝐶, 𝛽, 𝐼 )K(𝜑) ⊑ wlpJ𝐶K(𝜑).

Proof. For an arbitrary state 𝜎 ∈ Σ, the set Γ = Reach𝛽 (𝜎) ⊆ Σ is the smallest superset of states
that is closed under 𝛽-reachability. We distinguish two cases.
      • Assume that 𝐼 ⊑Γ Ψ𝑓 (𝐼 ) holds. Then vpJparkEnc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) ⊑ 𝐼 (𝜎) due to Lemma C.1.
        Due to local Park induction and Theorem 5.11, we know that 𝐼 ⊑Γ wlpJ𝐶K(𝜑) and hence
        also 𝐼 (𝜎) ⊑ wlpJ𝐶K(𝜑) (𝜎). Then inequality follows by
                       vpJparkEnc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) ⊑ 𝐼 (𝜎) ⊑ wlpJ𝐶K(𝜑) (𝜎).

      • Assume that 𝐼 ̸⊑Γ Ψ𝑓 (𝐼 ) holds. Then vpJparkEnc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) = ⊥ due to Lemma C.1.
        We cannot apply local Park induction and Theorem 5.11. However, the inequality follows by
                        vpJparkEnc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) = ⊥ ⊑ wlpJ𝐶K(𝜑) (𝜎).

This concludes the proof.                                                                                        □

C.4    Proofs of Section 5.4: Local 𝜅-Induction
Lemma C.2 (Closedness under Reachability). For a program 𝐶 ∈ wGCL with local variables
𝛽 ⊆ Vars and a set Γ ⊆ Σ of states that is closed under 𝛽-reachability, the 𝜅-induction operator Λ is
closed under Γ-restricted weightings, hence for all 𝑓 ∈ W exists 𝑔 ∈ W such that
                                                 Λ𝜅 (𝑓 |Γ ) = 𝑔 |Γ .

Proof. We know that Ψ𝑓 is closed under 𝛽-reachability. Furthermore, we can show by structural
induction that for all 𝑓 , 𝑔 ∈ W there exists ℎ ∈ W such that 𝑓 |Γ ⊔ 𝑔 |Γ = ℎ |Γ . This implies the
statement by induction on 𝜅.                                                                      □
Theorem 5.14 (𝜅-Induction). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL with local variables
𝛽 ⊆ Vars, a set Γ ⊆ Σ of states that is closed under 𝛽-reachability, weightings 𝑓 , 𝐼 ∈ W, and
𝜅 ∈ N, it is
                  𝐼 ⊑Γ Ψ𝑓 (Λ𝜅 (𝐼 )) implies 𝐼 ⊑Γ wlpJwhile ( 𝑏 ) { 𝐶 ′ }K(𝑓 ).

Proof. We show that Λ𝜅 (𝑔) ⊑Γ Λ𝜅+1 (𝑔) for any 𝑔 ∈ W by natural induction on 𝜅 ∈ N: It is
𝑔 ⊑Γ 𝐼 ⊔ Ψ𝑓 (𝐼 ) = Λ(𝐼 ) and Λ𝜅 (𝑔) ⊑Γ Λ𝜅+1 (𝑔) ⇐⇒ 𝐼 ⊔ Ψ𝑓 (Λ𝜅 −1 ) ⊑Γ 𝐼 ⊔ Ψ𝑓 (Λ𝜅 (𝐼 )), if we assume
that Λ𝜅 −1 (𝑔) ⊑Γ Λ𝜅 (𝐼 ) for an arbitrary but fixed 𝜅 > 0 as the induction hypothesis.
The previous statement together with the premise 𝐼 ⊑Γ Ψ𝑓 (Λ𝜅 (𝐼 )) show that Λ𝜅 (𝐼 ) is a local
subinvariant by
                         Λ𝜅 (𝐼 ) ⊑Γ Λ𝜅+1 (𝐼 ) = 𝐼 ⊔ Ψ𝑓 (Λ𝜅 (𝐼 )) ⊑Γ Ψ𝑓 (Λ𝜅 (𝐼 )).
We apply local Park induction (Theorem 5.11) to obtain that 𝐼 ⊑Γ wlpJ𝐶K(𝑓 ).                                     □
Towards a Verification Infrastructure for wGCL                                                   47


Lemma C.3 (Semantics of Encoding). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL with local variables
𝛽 ⊆ Vars, weightings 𝜑, 𝐼 ∈ wHeyLo, an encoding enc(𝐶 ′ ) with vpJenc(𝐶 ′ )K(𝜓 ) ⊑ wpJ𝐶 ′ K(𝜓 ) for
all 𝜓 ∈ wHeyVL, and 𝜎 ∈ Σ, the encoding of 𝜅-induction in Figure 9 satisfies
                                                  (
                                                    𝐼 (𝜎), if 𝐼 ⊑Γ Ψ𝑓 (Λ𝜅 (𝐼 ))
                     vpJ𝜅-Enc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) ⊑
                                                    ⊥,     otherwise .

Proof. We show by induction that for a loop 𝐶 ∈ wHeyVL with local variables 𝛽 ⊆ Σ, weightings
𝜑, 𝐼 ∈ wHeyLo, and state 𝜎 ∈ Σ, the semantics of 𝜅-unrollEnc is
                              vpJ𝜅-unrollEnc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) ⊑ Ψ𝑓 (Λ𝜅 (𝐼 )) (𝜎).

The base case is 𝜅 = 0 with 0-unrollEnc(𝐶, 𝛽, 𝐼 ) = charEnc(𝐶, 𝛽, 𝐼 ) and hence
vpJ0-unrollEnc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) ⊑ Ψ𝑓 (𝐼 ) (𝜎).
We assume that the statement holds for an arbitrary, but fixed 𝜅 ∈ N and obtain
      vpJ(𝜅+1)-unrollEnc(𝐶, 𝛽, 𝐼 )K(𝜑)
   = vpJassume ? (𝑏); enc(𝐶 ′ ); coassert 𝐼 ; 𝜅-unrollEnc(𝐶, 𝛽, 𝐼 )K(𝜑) ⊓ vpJassume ? (¬𝑏)K(𝜑)
   = ( ? (𝑏) → vpJenc(𝐶 ′ )K(vpJcoassert 𝐼 ; 𝜅-unrollEnc(𝐶, 𝛽, 𝐼 )K(𝜑))) ⊓ vpJassume ? (¬𝑏)K(𝜑)
   = ( ? (𝑏) → vpJenc(𝐶 ′ )K(𝐼 ⊔ 𝜅-unrollEnc(𝐶, 𝛽, 𝐼 ) (𝜑))) ⊓ ( ? (¬𝑏) → 𝜑)
 (IH)
   ⊑ ( ? (𝑏) → vpJenc(𝐶 )K(𝐼 ⊔ Ψ𝑓 (Λ (𝐼 )))) ⊓ ( ? (¬𝑏) → 𝜑)
                       ′            𝜅

                       ′     𝜅+1
   ⊑ ( ? (𝑏) → vpJenc(𝐶 )K(Λ           (𝐼 ))) ⊓ ( ? (¬𝑏) → 𝜑)
   ⊑ Ψ𝑓 (Λ  𝜅+1
                  (𝐼 )).
This shows the statement by induction.
We know that 𝜅-Enc(𝐶, 𝛽, 𝐼 ) = specEnc(𝐶, 𝛽, 𝐼 ); 𝜅-unrollEnc(𝐶, 𝛽, 𝐼 ) and hence
                             vpJ𝜅-Enc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎)
                           = vpJspecEnc(𝐶, 𝛽, 𝐼 ); 𝜅-unrollEnc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎)
                           = vpJspecEnc(𝐶, 𝛽, 𝐼 )K(vpJ𝜅-unrollEnc(𝐶, 𝛽, 𝐼 )K(𝜑)) (𝜎)
                             (
                               𝐼 (𝜎), if 𝐼 ⊑Γ vpJ𝜅-unrollEnc(𝐶, 𝛽, 𝐼 )K(𝜑)
                           =
                               ⊥,     otherwise,
                             (
                               𝐼 (𝜎), if 𝐼 ⊑Γ Ψ𝑓 (Λ𝜅 (𝐼 ))
                           =
                               ⊥,     otherwise.
                                                                                                  □


Theorem C.4 (Soundness). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL with local variables 𝛽 ⊆ Vars,
weightings 𝜑, 𝐼 ∈ wHeyLo, and 𝜅 ∈ N, the encoding 𝜅-Enc is a sound under-approximation, thus
                                     vpJ𝜅-Enc(𝐶, 𝛽, 𝐼 )K(𝜑) ⊑ wlpJ𝐶K(𝜑).

Proof. For an arbitrary state 𝜎 ∈ Σ, the set Γ = Reach𝛽 (𝛽) ⊆ Σ is the smallest superset of states
that is closed under 𝛽-reachability. We distinguish two cases.
48                                                                             Ahrens, Rode, Schröer, and Katoen


       • Assume that 𝐼 ⊑Γ Ψ𝑓 (Λ𝜅 (𝐼 )) holds. Then vpJ𝜅-Enc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) ⊑ 𝐼 (𝜎) due to Lemma C.3.
         Due to local 𝜅-induction and Theorem 5.14, we know that 𝐼 ⊑Γ wlpJ𝐶K(𝜑) and hence also
         𝐼 (𝜎) ⊑ wlpJ𝐶K(𝜑) (𝜎). Then inequality follows by
                             vpJ𝜅-Enc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) ⊑ 𝐼 (𝜎) ⊑ wlpJ𝐶K(𝜑) (𝜎).

       • Assume that 𝐼 ̸⊑Γ Ψ𝑓 (Λ𝜅 (𝐼 )) holds. Then vpJ𝜅-Enc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) = ⊥ due to Lemma C.3.
         We cannot apply local 𝜅-induction and Theorem 5.14. However, the inequality follows by
                               vpJ𝜅-Enc(𝐶, 𝛽, 𝐼 )K(𝜑) (𝜎) = ⊥ ⊑ wlpJ𝐶K(𝜑) (𝜎).

This concludes the proof.                                                                                     □

C.5     Proofs of Section 5.5: 𝜔-Invariants
Theorem 5.15 (𝜔-Rule). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, a postweighting 𝑓 ∈ W, and an
𝜔-subinvariant (𝐼 𝑛 )𝑛∈N ∈ WN , it is sup𝑛∈N 𝐼 𝑛 ⊑ wpJwhile ( 𝑏 ) { 𝐶 ′ }K(𝑓 ).

Proof. We show via natural induction that 𝐼𝑛 ⊑ Φ𝑛𝑓 (⊥) holds for all 𝑛 ∈ N.

       • Suppose that 𝑛 = 0. Then 𝐼 (0) = ⊥ and ⊥ ⊑ Φ0𝑓 (⊥) = ⊥.
       • Assume that 𝐼𝑛 ⊑ Φ𝑛𝑓 (⊥) holds for an arbitrary, but fixed number 𝑛 ∈ N. Then 𝐼𝑛+1 ⊑
         Φ 𝑓 (𝐼𝑛 ) ⊑ Φ 𝑓 (Φ𝑛𝑓 (⊥)) follows from the induction hypothesis, from the conditions on subin-
         variants, and from the 𝜔-continuity of the characteristic function Φ 𝑓 .
This concludes the statement via natural induction.
Since 𝐼𝑛 ⊑ Φ𝑛𝑓 (⊥) holds for all 𝑛 ∈ N, we derive that sup𝑛∈N 𝐼𝑛 ⊑          𝑛∈N Φ 𝑓 (⊥) = wpJ𝐶K(𝜑).
                                                                          Ã      𝑛                            □

Lemma 5.16 (Checking 𝜔-Invariant). For a weighting 𝐼 (𝑛) ∈ wHeyLo with free variable 𝑛 ∈ Vars,
the programs 𝑏𝑎𝑠𝑒 and 𝑠𝑡𝑒𝑝 in Figure 10 encode
                   𝐼 (0) ⊑ vpJ𝑏𝑎𝑠𝑒K(𝜑)               if and only if   𝐼 (0) = ⊥
        and        𝐼 (𝑛 + 1) ⊑ vpJ𝑠𝑡𝑒𝑝K(𝜑)               implies      ∀𝑛 ∈ N : 𝐼 (𝑛 + 1) ⊑ Φ𝜑 (𝐼 (𝑛)).

Proof. By applying the rules in Table 2, we obtain the semantics of 𝑏𝑎𝑠𝑒 and 𝑠𝑡𝑒𝑝 by
                                  𝐼 (0) ⊑ vpJ𝑏𝑎𝑠𝑒K( ? (false))                           (definition of proc)
                               iff 𝐼 (0) ⊑ ? (false) = ⊥.
and, again 𝐼 (𝑛 + 1) ⊑ vpJ𝑠𝑡𝑒𝑝K(𝜑), and
       vpJ𝑠𝑡𝑒𝑝K(𝜑)
     = vpJvar 𝑥 1 : 𝜏1 := 𝑥 1 ; . . . ; if (⊓) {assume ? (𝑏); . . .} else {assume ? (¬𝑏)}K(𝜑)
     = vpJvar 𝑥 1 : 𝜏1 := 𝑥 1 ; . . . ; var 𝑥𝑘 : 𝜏𝑘 := 𝑥 𝑘 K
         (vpJassume ? (𝑏); enc(𝐶 ′ ); assert 𝐼 (𝑛); assume ? (false)K(𝜑) ⊓ vpJassume ? (¬𝑏)K(𝜑))
     = vpJvar 𝑥 1 : 𝜏1 := 𝑥 1 ; . . . ; var 𝑥𝑘 : 𝜏𝑘 := 𝑥 𝑘 K
         (vpJassume ? (𝑏); enc(𝐶 ′ ); assert 𝐼 (𝑛)K( ? (false) → 𝜑) ⊓ ( ? (¬𝑏) → 𝜑))
     = vpJvar 𝑥 1 : 𝜏1 := 𝑥 1 ; . . . ; var 𝑥𝑘 : 𝜏𝑘 := 𝑥 𝑘 K
         (vpJassume ? (𝑏); enc(𝐶 ′ ); assert 𝐼 (𝑛)K(⊥) ⊓ ( ? (¬𝑏) → 𝜑))
     = vpJvar 𝑥 1 : 𝜏1 := 𝑥 1 ; . . . ; var 𝑥𝑘 : 𝜏𝑘 := 𝑥 𝑘 K
Towards a Verification Infrastructure for wGCL                                                  49


        (vpJassume ? (𝑏); enc(𝐶 ′ )K(𝐼 (𝑛)) ⊓ ( ? (¬𝑏) → 𝜑))
   = vpJvar 𝑥 1 : 𝜏1 := 𝑥 1 ; . . . ; var 𝑥𝑘 : 𝜏𝑘 := 𝑥 𝑘 K
        (vpJassume ? (𝑏)K(vpJenc(𝐶 ′ )K(𝐼 (𝑛))) ⊓ ( ? (¬𝑏) → 𝜑))
   = vpJvar 𝑥 1 : 𝜏1 := 𝑥 1 ; . . . ; var 𝑥𝑘 : 𝜏𝑘 := 𝑥 𝑘 K
        ( ? (𝑏) → vpJenc(𝐶 ′ )K(𝐼 (𝑛)) ⊓ ( ? (¬𝑏) → 𝜑))
   = ? (𝑏) → vpJenc(𝐶 ′ )K(𝐼 (𝑛)) ⊓ ( ? (¬𝑏) → 𝜑)
   ⊑ Φ 𝑓 (𝐼 (𝑛)),
if vpJenc(𝐶 ′ )K(𝜓 ) ⊑ wpJenc(𝐶 ′ )K(𝜓 ) for all 𝜓 ∈ wHeyLo. Hence, 𝐼 (𝑛 + 1) ⊑ vpJenc(𝐶 ′ )K(𝜑) ⊑
wpJenc(𝐶 ′ )K(𝜑) follows for all 𝑛 ∈ N.                                                          □

Lemma C.5 (Semantics of Encoding). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, a postweighting
𝜑 ∈ wHeyLo, and a weighting 𝐼 (𝑛) ∈ wHeyLo with free variable 𝑛 ∈ Vars, the encoding of the 𝜔-rule
in Figure 10 satisfies                                      Ä
                         vpJ𝜔-Enc(𝐶, (𝐼 (𝑛))𝑛∈N )K(𝜑) (𝜎) =     𝐼 (𝑛).
                                                                   𝑛∈N

Proof. By applying the rules in Table 2, we obtain the semantics of 𝜔-Enc(𝐶, 𝐼 (𝑛)) by
                           vpJ𝜔-Enc(𝐶, 𝐼 (𝑛))K(𝜑)
                        = vpJcohavoc 𝑛; assert 𝐼 (𝑛)K(vpJassume ? (false)K(𝜑))
                        = vpJcohavoc 𝑛; assert 𝐼 (𝑛)K( ? (false) → 𝜑)
                        = vpJcohavoc 𝑛; assert 𝐼 (𝑛)K(⊤)
                        = vpJcohavoc 𝑛K(vpJassert 𝐼 (𝑛)K(⊤))
                        = vpJcohavoc 𝑛K(𝐼 (𝑛) ⊓ ⊤)
                        = vpJcohavoc 𝑛K(𝐼 (𝑛))
                           Ä
                        =     𝐼 (𝑛).
                           𝑛∈N
                                                                                                 □

Theorem C.6 (Soundness). For a loop 𝐶 = while ( 𝑏 ) { 𝐶 ′ } ∈ wGCL, a postweighting 𝜑 ∈ wHeyLo,
and a weighting 𝐼 (𝑛) ∈ wHeyLo, the encoding 𝜔-Enc is a sound under-approximation, if the auxiliary
procedures 𝑏𝑎𝑠𝑒 and 𝑠𝑡𝑒𝑝 in Figure 10 are valid for an 𝑛 ∈ N. Then
                                     vpJ𝜔-Enc(𝐶, 𝐼 )K(𝜑) ⊑ wpJ𝐶K(𝜑).

Proof. Suppose that the programs 𝑏𝑎𝑠𝑒 and 𝑠𝑡𝑒𝑝 are valid, then the sequence (𝐼 (𝑛))𝑛∈N is an
𝜔-subinvariant with 𝐼 (0) = ⊥ and 𝐼𝑛+1 ⊑ Φ 𝑓 (𝐼𝑛 ) forÃ
                                                      all 𝑛 ∈ N due to Lemma 5.16. Then, we apply
Theorem 5.15 and obtain vpJ𝜔-Enc(𝐶, 𝐼 (𝑛))K(𝜑) = 𝑛∈N 𝐼 (𝑛) ⊑ wpJ𝐶K(𝜑).                         □
50                                                                                         Ahrens, Rode, Schröer, and Katoen


D     Proofs of Section 7: Automated Reasoning
     Theorem 7.1 (Quantifier Stripping). For every 𝜑 ∈ wHeyLo:
               l                                Ä
                  𝜑 is valid iff 𝜑 is valid,       𝜑 is covalid iff 𝜑 is covalid.
                  𝑥                                       𝑥

     Proof. Let 𝜎 ∈ Σ. If 𝜑 is valid, then J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) = ⊤ for all 𝑣 ∈ N, and hence
                   l
                  J 𝜑K(𝜎) = inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N = inf {⊤ | 𝑣 ∈ N} = ⊤.
                                    
                          𝑥
Thus 𝑥 𝜑 is valid.
    d
  Conversely, assume 𝑥 𝜑 is valid. Then
                    d
              l
        ⊤ = J 𝜑K(𝜎) = inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N ⊑ J𝜑K(𝜎 [𝑥 ↦→ 𝜎 (𝑥)]) = J𝜑K(𝜎).
                            
                      𝑥
Since ⊤ is greatest, J𝜑K(𝜎) = ⊤. As 𝜎 was arbitrary, 𝜑 is valid.
  If 𝜑 is covalid, then J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) = ⊥ for all 𝑣 ∈ N, and hence
                  Ä
                 J 𝜑K(𝜎) = sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N = sup {⊥ | 𝑣 ∈ N} = ⊥.
                                   
                          𝑥
Thus 𝑥 𝜑 is covalid.
    Ã
  Conversely, assume 𝑥 𝜑 is covalid. Then
                     Ã
                                                                Ä
                                      J𝜑K(𝜎 [𝑥 ↦→ 𝜎 (𝑥)]) ⊑ J       𝜑K(𝜎) = ⊥.
                                                                𝑥
Since ⊥ is least, J𝜑K(𝜎) = ⊥. As 𝜎 was arbitrary, 𝜑 is covalid.                                                           □

D.1     Prenexing Rules
We first collect the formula-level prenexing equivalences used by the quantifier-elimination proce-
dure.
D.1.1    Logical Prenexing.
  Theorem D.1 (Positive Prenexing). Let 𝜑,𝜓 ∈ wHeyLo and 𝑥, 𝑦 ∈ Vars where 𝑥 ∉ free(𝜓 ) and
𝑦 ∉ free(𝜑). Then the following equivalences hold:
         l                 l                         Ä                 Ä
             𝜑 ⊓𝜓 ≡          (𝜑 ⊓ 𝜓 )                    𝜑 ⊔𝜓 ≡           (𝜑 ⊔ 𝜓 )
             𝑥                    𝑥                                    𝑥                            𝑥
                 l                l                                        Ä                       Ä
            𝜑⊓            𝜓   ≡       (𝜑 ⊓ 𝜓 )                        𝜑⊔           𝜓          ≡         (𝜑 ⊔ 𝜓 )
                  𝑦               𝑦                                            𝑦                    𝑦

            l                     l                                    Ä                           Ä
                 𝜑 ⊔𝜓         ≡       (𝜑 ⊔ 𝜓 )                             𝜑 ⊓𝜓               ≡         (𝜑 ⊓ 𝜓 )
             𝑥                    𝑥                                    𝑥                            𝑥
                 l                l                                        Ä                       Ä
            𝜑⊔            𝜓   ≡       (𝜑 ⊔ 𝜓 )                        𝜑⊓           𝜓          ≡         (𝜑 ⊓ 𝜓 )
                  𝑦               𝑦                                            𝑦                    𝑦

                 l                l                                        Ä                       Ä
           𝜑→             𝜓   ≡       (𝜑 → 𝜓 )                       𝜑←            𝜓          ≡         (𝜑 ← 𝜓 )
                  𝑦               𝑦                                            𝑦                    𝑦
                                                                                       !
                                                                           Ä                       Ä
              ©l ª                l                                    ▽           𝜓          ≡         ▽(𝜓 )
             △­ 𝜓 ®           ≡       △(𝜓 )
                                                                           𝑦                        𝑦
              «𝑦 ¬                𝑦
Towards a Verification Infrastructure for wGCL                                                      51


  Proof. Let 𝜑,𝜓 ∈ wHeyLo and 𝑥, 𝑦 ∈ Vars where 𝑥 ∉ free(𝜓 ) and 𝑦 ∉ free(𝜑), and 𝜎 ∈ Σ.
Recall that 𝜑 ≡ 𝜓 iff J𝜑K(𝜎) = J𝜓 K(𝜎) for all 𝜎 ∈ Σ.
     - Case 𝑥 𝜑 ⊓ 𝜓 .
              d
                l
               J 𝜑 ⊓ 𝜓 K(𝜎)
                    𝑥
                             (                        )
                                 l
                  = inf J            𝜑K(𝜎), J𝜓 K(𝜎)                                  (definition of ⊓)
                                 𝑥
                  = inf inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N , J𝜓 K(𝜎)
                        
                                                                                   (definition of       𝑥)
                                                                                                    d

                  = inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]), J𝜓 K(𝜎) | 𝑣 ∈ N
                       
                                                                                         (merge inf)
                  = inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]), J𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                       
                                                                                       (𝑥 ∉ free(𝜓 ))
                  = inf inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]), J𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                        
                                                                                      (introduce inf)
                  = inf J𝜑 ⊓ 𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                       
                                                                                     (definition of ⊓)
                     l
                                                                                   (definition of 𝑥 )
                                                                                                  d
                  = J (𝜑 ⊓ 𝜓 )K(𝜎)
                         𝑥

        The case 𝜑 ⊓ 𝑦 𝜓 ≡ 𝑦 (𝜑 ⊓ 𝜓 ) is analogous.
                    d      d

      - Case 𝑥 𝜑 ⊔ 𝜓 .
             d
                l
               J 𝜑 ⊔ 𝜓 K(𝜎)
                    𝑥
                             (                        )
                                 l
                   = sup J           𝜑K(𝜎), J𝜓 K(𝜎)                                  (definition of ⊔)
                                 𝑥
                   = sup inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N , J𝜓 K(𝜎)
                          
                                                                                   (definition of       𝑥)
                                                                                                    d

                   = inf sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]), J𝜓 K(𝜎) | 𝑣 ∈ N
                            
                                                                                        (Lemma B.9)
                   = inf sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]), J𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                            
                                                                                       (𝑥 ∉ free(𝜓 ))
                   = inf J𝜑 ⊔ 𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                        
                                                                                     (definition of ⊔)
                      l
                                                                                   (definition of 𝑥 )
                                                                                                  d
                   = J (𝜑 ⊔ 𝜓 )K(𝜎)
                         𝑥

        The case 𝜑 ⊔ 𝑦 𝜓 ≡ 𝑦 (𝜑 ⊔ 𝜓 ) is analogous.
                     d    d

      - Case 𝜑 → 𝑦 𝜓 .
                   d

                       l
                 J𝜑 → 𝜓 K(𝜎)
                                 𝑦
                                    l
                        = J𝜑K(𝜎) → J 𝜓 K(𝜎)                                         (definition of →)
                                          𝑦

                        = J𝜑K(𝜎) → inf J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) | 𝑣 ∈ N
                                        
                                                                                   (definition of       𝑦)
                                                                                                    d

                        = inf J𝜑K(𝜎) → J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) | 𝑣 ∈ N
                             
                                                                                          (Lem. B.10)
                        = inf J𝜑K(𝜎 [𝑦 ↦→ 𝑣]) → J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) | 𝑣 ∈ N
                             
                                                                                        (𝑦 ∉ free(𝜑))
                           l
                                                                           (definitions of → and 𝑦 )
                                                                                                 d
                        = J (𝜑 → 𝜓 )K(𝜎)
                             𝑦
52                                                                        Ahrens, Rode, Schröer, and Katoen

                d         
     - Case △         𝑦𝜓       .

                     ©l ª
                  J△­ 𝜓 ®K(𝜎)
                     «( 𝑦 ¬
                        ⊤, if J 𝑦 𝜓 K(𝜎) = ⊤
                               d
                   =                                                                  (definition of △(−))
                        ⊥, otherwise
                      (
                        ⊤, if J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) = ⊤ for all 𝑣 ∈ N
                                                                                         (definition of       )
                                                                                                          d
                   =
                        ⊥, otherwise
                          ((                                     )
                             ⊤, if J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) = ⊤
                   = inf                                 |𝑣 ∈N                       (infimum of {⊤, ⊥})
                             ⊥, otherwise
                       l
                                                                             (definition of △(−) and         𝑦)
                                                                                                         d
                   = J △(𝜓 )K(𝜎).
                           𝑦
                                           Ã        Ã
       The covalidation case ▽                  𝑦 𝜓  ≡ 𝑦 ▽(𝜓 ) is dual.
     - Case 𝑥 𝜑 ⊔ 𝜓 .
            Ã
              Ä
             J 𝜑 ⊔ 𝜓 K(𝜎)
                 𝑥
                           (                            )
                                   Ä
                = sup J                𝜑K(𝜎), J𝜓 K(𝜎)                                     (definition of ⊔)
                                   𝑥
                = sup sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N , J𝜓 K(𝜎)
                         
                                                                                        (definition of       𝑥)
                                                                                                         Ã

                = sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]), J𝜓 K(𝜎) | 𝑣 ∈ N
                     
                                                                                        (flatten suprema)
                = sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]), J𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                     
                                                                                            (𝑥 ∉ free(𝜓 ))
                = sup sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]), J𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                         
                                                                                          (introduce sup)
                = sup J𝜑 ⊔ 𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                     
                                                                                          (definition of ⊔)
                   Ä
                = J (𝜑 ⊔ 𝜓 )K(𝜎)                                                        (definition of 𝑥 )
                                                                                                       Ã
                      𝑥
       The case
            Ã 𝜑 ⊔ 𝑦 𝜓 ≡ 𝑦 (𝜑 ⊔ 𝜓 ) is analogous.
                  Ã       Ã
     - Case 𝑥 𝜑 ⊓ 𝜓 .
                Ä
              J 𝜑 ⊓ 𝜓 K(𝜎)
                  𝑥
                           (                            )
                                   Ä
                = inf J                𝜑K(𝜎), J𝜓 K(𝜎)                                     (definition of ⊓)
                                   𝑥
                = inf sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N , J𝜓 K(𝜎)
                        
                                                                                        (definition of       𝑥)
                                                                                                         Ã

                = sup inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]), J𝜓 K(𝜎) | 𝑣 ∈ N
                       
                                                                                             (Lemma B.9)
                = sup inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]), J𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                       
                                                                                            (𝑥 ∉ free(𝜓 ))
                = sup J𝜑 ⊓ 𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                      
                                                                                          (definition of ⊓)
                   Ä
                = J (𝜑 ⊓ 𝜓 )K(𝜎)                                                        (definition of 𝑥 )
                                                                                                       Ã
                       𝑥
Towards a Verification Infrastructure for wGCL                                                                53


        The case 𝜑 Ã
                   ⊓ 𝑦 𝜓 ≡ 𝑦 (𝜑 ⊓ 𝜓 ) is analogous.
                     Ã      Ã
      - Case 𝜑 ← 𝑦 𝜓 .
                       Ä
                 J𝜑 ←    𝜓 K(𝜎)
                                     𝑦
                                             Ä
                         = J𝜑K(𝜎) ← J             𝜓 K(𝜎)                                      (definition of ←)
                                              𝑦

                         = J𝜑K(𝜎) ← sup J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) | 𝑣 ∈ N
                                         
                                                                                             (definition of       𝑦)
                                                                                                              Ã

                         = sup J𝜑K(𝜎) ← J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) | 𝑣 ∈ N
                               
                                                                                                 (Lemma B.11)
                         = sup J𝜑K(𝜎 [𝑦 ↦→ 𝑣]) ← J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) | 𝑣 ∈ N
                               
                                                                                                 (𝑦 ∉ free(𝜑))
                            Ä
                         = J (𝜑 ← 𝜓 )K(𝜎)                                           (definitions of ← and 𝑦 )
                                                                                                          Ã
                                 𝑦

                                                                                                                  □

  Theorem D.2 (Negative Prenexing). Let 𝜑,𝜓 ∈ wHeyLo and 𝑥, 𝑦 ∈ Vars where 𝑥 ∉ free(𝜓 )
and 𝑦 ∉ free(𝜑). Then the following equivalences hold:
         Ä                 l                            l           Ä
        ( 𝜑) → 𝜓 ≡             (𝜑 → 𝜓 )                ( 𝜑) ← 𝜓 ≡      (𝜑 ← 𝜓 )
           𝑥                             𝑥                        𝑥                      𝑥

                    Ä                    l                                 l            Ä
               ¬(        𝜑)          ≡       (¬𝜑)                     ∼(       𝜑)   ≡        (∼𝜑)
                    𝑥                    𝑥                                 𝑥             𝑥



   Proof. Let 𝜑,𝜓 ∈ wHeyLo and 𝑥, 𝑦 ∈ Vars where 𝑥 ∉ free(𝜓 ) and 𝑦 ∉ free(𝜑).
     - Case ( 𝑥 𝜑) → 𝜓 .
              Ã
                  Ä
                J( 𝜑) → 𝜓 K(𝜎)
                             𝑥
                                 Ä
                         =J          𝜑K(𝜎) → J𝜓 K(𝜎)                                          (definition of →)
                                 𝑥
                         = sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N → J𝜓 K(𝜎)
                               
                                                                                             (definition of       𝑥)
                                                                                                              Ã

                         = inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) → J𝜓 K(𝜎) | 𝑣 ∈ N
                              
                                                                                                 (Lemma B.12)
                         = inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) → J𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                              
                                                                                                 (𝑥 ∉ free(𝜓 ))
                            l
                         = J (𝜑 → 𝜓 )K(𝜎)
                                 𝑥

      - Case (          𝑥 𝜑) ← 𝜓 .
                    d
                             l
                        J(       𝜑) ← 𝜓 K(𝜎)
                             𝑥
                            l
                         = J 𝜑K(𝜎) ← J𝜓 K(𝜎)                                                  (definition of ←)
                                 𝑥
                         = inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N ← J𝜓 K(𝜎)
                              
                                                                                             (definition of       𝑥)
                                                                                                              d

                         = sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ← J𝜓 K(𝜎) | 𝑣 ∈ N
                               
                                                                                                 (Lemma B.13)
                         = sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ← J𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                               
                                                                                                 (𝑥 ∉ free(𝜓 ))
54                                                                      Ahrens, Rode, Schröer, and Katoen

                            Ä
                   =J           (𝜑 ← 𝜓 )K(𝜎)                                 (definitions of ← and    𝑥)
                                                                                                     Ã
                            𝑥
       - Case ¬(       𝑥 𝜑). Using ¬𝜑 ≡ 𝜑 → ⊥, we compute:
                   Ã
                            Ä                Ä
                       J¬       𝜑K(𝜎) = J(            𝜑) → ⊥K(𝜎)                        (definition of ¬)
                            𝑥                    𝑥
                                           l
                                        = J (𝜑 → ⊥)K(𝜎)                (previous proofcase with 𝜓 = ⊥)
                                             𝑥
                                           l
                                        = J ¬𝜑K(𝜎).                                     (definition of ¬)
                                             𝑥
       - Case ∼(   𝑥 𝜑). Using ∼𝜑 ≡ 𝜑 ← ⊤, we compute:
                   d
                            l                l
                       J∼       𝜑K(𝜎) = J(           𝜑) ← ⊤K(𝜎)                         (definition of ∼)
                            𝑥                𝑥
                                             Ä
                                        =J       (𝜑 ← ⊤)K(𝜎)           (previous proofcase with 𝜓 = ⊤)
                                             𝑥
                                             Ä
                                        =J           ∼𝜑K(𝜎).                            (definition of ∼)
                                             𝑥
                                                                                                         □
  The remaining prenexing directions require the relevant quantified extremum to be realized by
an actual program value.
  Definition D.3 (Well-Foundedness). wHeyLo is well-founded if, for all 𝜑 ∈ wHeyLo, 𝑥 ∈ Vars, and
𝜎 ∈ Σ,                                                        l
                             ∃𝑣 − ∈ N . J𝜑K(𝜎 [𝑥 ↦→ 𝑣 − ]) = J 𝜑K(𝜎).
                                                                   𝑥
wHeyLo is upwards well-founded if, for all 𝜑 ∈ wHeyLo, 𝑥 ∈ Vars, and 𝜎 ∈ Σ,
                                                           Ä
                          ∃𝑣 + ∈ N . J𝜑K(𝜎 [𝑥 ↦→ 𝑣 + ]) = J 𝜑K(𝜎).
                                                                   𝑥

  Finite totally ordered domains, such as the Boolean and clearance semirings, satisfy both clauses.
Domains ordered like N, such as the counting semiring, satisfy well-foundedness but not upwards
well-foundedness. Reversed natural-number orders, such as the tropical semiring over N∞ , satisfy
upwards well-foundedness but not well-foundedness. Dense orders such as Viterbi or bottleneck,
and Boolean-algebra domains such as formal languages, satisfy neither clause in general.
  Lemma D.4 (Well-Founded Quantifiers under Monotone Maps). Let 𝜑 ∈ wHeyLo, 𝑥 ∈ Vars,
and 𝜎 ∈ Σ.
  If wHeyLo is well-founded, then for every monotone map 𝐹 : 𝐻 → 𝐻 ,
                           l
                       𝐹 (J 𝜑K(𝜎)) = inf 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣])) | 𝑣 ∈ N ,
                                            
                                    𝑥
and for every antitone map 𝐹 : 𝐻 → 𝐻 ,
                            l
                        𝐹 (J 𝜑K(𝜎)) = sup 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣])) | 𝑣 ∈ N .
                                         
                                   𝑥
     Dually, if wHeyLo is upwards well-founded, then for every monotone map 𝐹 : 𝐻 → 𝐻 ,
                              Ä
                          𝐹 (J 𝜑K(𝜎)) = sup 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣])) | 𝑣 ∈ N ,
                                              
                                   𝑥
Towards a Verification Infrastructure for wGCL                                                            55


and for every antitone map 𝐹 : 𝐻 → 𝐻 ,
                            Ä
                        𝐹 (J 𝜑K(𝜎)) = inf 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣])) | 𝑣 ∈ N .
                                         
                                        𝑥

   Proof. We prove the well-founded clauses; the upwards well-founded clauses are dual.
   By well-foundedness, choose 𝑣 0 ∈ N such that
                                       l
                 J𝜑K(𝜎 [𝑥 ↦→ 𝑣 0 ]) = J 𝜑K(𝜎) = inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N .
                                                   
                                                    𝑥

Hence J𝜑K(𝜎 [𝑥 ↦→ 𝑣 0 ]) ⊑ J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) for all 𝑣 ∈ N. If 𝐹 is monotone, then 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣 0 ])) ⊑
𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣])) for all 𝑣 ∈ N. Thus 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣 0 ])) is a lower bound of 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣])) | 𝑣 ∈ N .
Since it is also an element of this set, it is its least element and hence its infimum. Therefore
                              l
                          𝐹 (J 𝜑K(𝜎)) = inf 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣])) | 𝑣 ∈ N .
                                                  
                                        𝑥

    If 𝐹 is antitone, then 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣])) ⊑ 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣 0 ])) for all 𝑣 ∈ N. Thus 𝐹 (J𝜑K(𝜎 [𝑥 ↦→
𝑣 0 ])) is an upper bound of 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣])) | 𝑣 ∈ N . Since it is also an element of this set, it is
                               

its greatest element and hence its supremum. Therefore
                                l
                            𝐹 (J 𝜑K(𝜎)) = sup 𝐹 (J𝜑K(𝜎 [𝑥 ↦→ 𝑣])) | 𝑣 ∈ N .
                                                
                                        𝑥
                                                                                                           □

  Theorem D.5 (Additional Logical Prenexing from Above). Assume wHeyLo is upwards
well-founded in the sense of Definition D.3. Let 𝜑,𝜓 ∈ wHeyLo and 𝑥, 𝑦 ∈ Vars where 𝑥 ∉ free(𝜓 )
and 𝑦 ∉ free(𝜑). Then the following additional equivalences hold:
              Ä            Ä                               Ä                 l
        𝜑→       𝜓 ≡          (𝜑 → 𝜓 )                    ( 𝜑) ← 𝜓 ≡            (𝜑 ← 𝜓 )
                    𝑦                   𝑦                        𝑥                     𝑥

                            !                                             Ä            l
               Ä                        Ä                            ∼(       𝜑)   ≡       (∼𝜑)
           △            𝜓       ≡           △(𝜓 )                         𝑥            𝑥
                𝑦                       𝑦



   Proof. Let 𝜑,𝜓 ∈ wHeyLo and 𝑥, 𝑦 ∈ Vars where 𝑥 ∉ free(𝜓 ) and 𝑦 ∉ free(𝜑).
     - Case 𝜑 → 𝑦 𝜓 .
                  Ã
                Ä
          J𝜑 →     𝜓 K(𝜎)
                            𝑦
                                    Ä
             = J𝜑K(𝜎) → J               𝜓 K(𝜎)                                              (definition of →)
                                    𝑦

             = sup J𝜑K(𝜎) → J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) | 𝑣 ∈ N
                  
                                                                      (Lemma D.4 with 𝐹 (𝑧) = J𝜑K(𝜎) → 𝑧)
             = sup J𝜑K(𝜎 [𝑦 ↦→ 𝑣]) → J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) | 𝑣 ∈ N
                  
                                                                                                (𝑦 ∉ free(𝜑))
                Ä
             = J (𝜑 → 𝜓 )K(𝜎).                                                             (definition of 𝑦 )
                                                                                                         Ã
                    𝑦

        The validation clause is obtained by the same argument with 𝐹 (𝑧) = △(𝑧).
56                                                                         Ahrens, Rode, Schröer, and Katoen


       - Case ( 𝑥 𝜑) ← 𝜓 .
               Ã
             Ä
           J( 𝜑) ← 𝜓 K(𝜎)
                 𝑥
                     Ä
               =J        𝜑K(𝜎) ← J𝜓 K(𝜎)                                                  (definition of ←)
                     𝑥
               = inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ← J𝜓 K(𝜎) | 𝑣 ∈ N
                    
                                                                    (Lemma D.4 with 𝐹 (𝑧) = 𝑧 ← J𝜓 K(𝜎))
               = inf J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ← J𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                    
                                                                                             (𝑥 ∉ free(𝜓 ))
                  l
                                                                                         (definition of 𝑥 )
                                                                                                       d
               = J (𝜑 ← 𝜓 )K(𝜎).
                     𝑥
         The co-negation clause is the special case ∼𝜑 ≡ 𝜑 ← ⊤.
                                                                                                          □
   Theorem D.6 (Additional Logical Prenexing from Below). Assume wHeyLo is well-founded
in the sense of Definition D.3. Let 𝜑,𝜓 ∈ wHeyLo and 𝑥, 𝑦 ∈ Vars where 𝑥 ∉ free(𝜓 ) and 𝑦 ∉ free(𝜑).
Then the following additional equivalences hold:
          l                     Ä                                  l           l
         ( 𝜑) → 𝜓 ≡                 (𝜑 → 𝜓 )                 𝜑← 𝜓 ≡               (𝜑 ← 𝜓 )
           𝑥                          𝑥                              𝑦              𝑦

                     l                Ä
               ¬(        𝜑)   ≡           (¬𝜑)
                                                                   ©l ª            l
                     𝑥                𝑥                           ▽­ 𝜓 ®      ≡         ▽(𝜓 )
                                                                   «𝑦 ¬             𝑦


     Proof. Let 𝜑,𝜓 ∈ wHeyLo and 𝑥, 𝑦 ∈ Vars where 𝑥 ∉ free(𝜓 ) and 𝑦 ∉ free(𝜑).
       - Case ( 𝑥 𝜑) → 𝜓 .
                d
              l
            J( 𝜑) → 𝜓 K(𝜎)
                 𝑥
                  l
               = J 𝜑K(𝜎) → J𝜓 K(𝜎)                                                        (definition of →)
                     𝑥
               = sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) → J𝜓 K(𝜎) | 𝑣 ∈ N
                    
                                                                    (Lemma D.4 with 𝐹 (𝑧) = 𝑧 → J𝜓 K(𝜎))
               = sup J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) → J𝜓 K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N
                    
                                                                                             (𝑥 ∉ free(𝜓 ))
                  Ä
               = J (𝜑 → 𝜓 )K(𝜎).                                                         (definition of 𝑥 )
                                                                                                       Ã
                     𝑥
         The negation
                   d clause is the special case ¬𝜑 ≡ 𝜑 → ⊥.
       - Case 𝜑 ← 𝑦 𝜓 .
                 l
           J𝜑 ← 𝜓 K(𝜎)
                         𝑦
                           l
               = J𝜑K(𝜎) ← J 𝜓 K(𝜎)                                                        (definition of ←)
                                  𝑦

               = inf J𝜑K(𝜎) ← J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) | 𝑣 ∈ N
                    
                                                                    (Lemma D.4 with 𝐹 (𝑧) = J𝜑K(𝜎) ← 𝑧)
               = inf J𝜑K(𝜎 [𝑦 ↦→ 𝑣]) ← J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) | 𝑣 ∈ N
                    
                                                                                             (𝑦 ∉ free(𝜑))
                  l
                                                                                         (definition of 𝑦 )
                                                                                                       d
               = J (𝜑 ← 𝜓 )K(𝜎).
                     𝑦
Towards a Verification Infrastructure for wGCL                                                                           57


        The covalidation clause is obtained by the same argument with 𝐹 (𝑧) = ▽(𝑧).
                                                                                                                          □
D.1.2 Weighted Prenexing. The weighted prenexing laws below are not consequences of the bare
monoid-module setup alone, let alone the bi-Heyting algebra structure. We first isolate the laws that
remain valid in the general 𝜔-bicontinuous monoid-module setting, and then state the additional
preservation assumptions under which they become formula equivalences.
   We first want to identify which prenexing rules hold in the general framework of 𝜔-bicontinuous
bi-Heyting algebras. The crucial observation is that the monoid-module operations ⊕ and ⊗ are
inherently tied to the bottom element ⊥ through definitions like 𝑝 ⊕ ⊥ = 𝑝 and 𝑎 ⊗ ⊥ = ⊥.
 Lemma D.7 (Bottom Facts for Weighted Addition). Let W = (𝑊 , ⊕, 0, ⊗) be a monoid-
module over a monoid M. For all 𝑝, 𝑞 ∈ 𝑊 ,
                                        𝑝 ⊕𝑞 =⊥        iff 𝑝 = ⊥ and 𝑞 = ⊥.                                              (1)
Moreover, for every family (𝑟𝑖 )𝑖 ∈𝐼 whose supremum exists,
                                     Ä
                                        𝑟𝑖 = ⊥ iff ∀𝑖 ∈ 𝐼 . 𝑟𝑖 = ⊥.                                                      (2)
                                              𝑖 ∈𝐼
Finally, for every nonempty family (𝑠𝑖 )𝑖 ∈𝐼 and every 𝑐 ∈ 𝑊 for which the displayed extrema exist,
                                    !
                              Ä                         Ä
                                  𝑠𝑖 ⊕ 𝑐 = ⊥ iff           (𝑠𝑖 ⊕ 𝑐) = ⊥,                           (3)
                                       𝑖 ∈𝐼                        𝑖 ∈𝐼
                                                 !
                                       l                           l
                                              𝑠𝑖 ⊕ 𝑐 = ⊥   iff            (𝑠𝑖 ⊕ 𝑐) = ⊥.                                  (4)
                                       𝑖 ∈𝐼                        𝑖 ∈𝐼

   Proof. For the Equation (1),
                            𝑝 ⊕𝑞 =⊥            implies 𝑝 = ⊥ and 𝑞 = ⊥                                    (𝑝, 𝑞 ⊑ 𝑝 ⊕ 𝑞 = ⊥)
                                               implies 𝑝 ⊕ 𝑞 = ⊥.                                 (⊥ = 0 is neutral for ⊕)
The converse follows, cause ⊥ = 0 is neutral for ⊕. For Equation (2),
                  Ä
                    𝑟𝑖 = ⊥ implies ∀𝑖 ∈ 𝐼 . 𝑟𝑖 ⊑ ⊥                                        (𝑟𝑖 ⊑    𝑖 ∈𝐼 𝑟 𝑖 and Lemma B.8)
                                                                                                  Ã
                     𝑖 ∈𝐼
                                       implies ∀𝑖 ∈ 𝐼 . 𝑟𝑖 = ⊥,
and the converse follows because ⊥ is the smallest upper bound if all 𝑟𝑖 are ⊥.
  The Equation (3) equivalence now follows immediately:
                               !
                          Ä                     Ä
                             𝑠𝑖 ⊕ 𝑐 = ⊥ iff         𝑠𝑖 = ⊥ and 𝑐 = ⊥                                          (Equation (1))
                                𝑖 ∈𝐼                        𝑖 ∈𝐼
                                                       iff ∀𝑖 ∈ 𝐼 . 𝑠𝑖 = ⊥ and 𝑐 = ⊥                          (Equation (2))
                                                       iff ∀𝑖 ∈ 𝐼 . 𝑠𝑖 ⊕ 𝑐 = ⊥                                (Equation (1))
                                                           Ä
                                                       iff     (𝑠𝑖 ⊕ 𝑐) = ⊥.                                  (Equation (2))
                                                            𝑖 ∈𝐼
   For infima, both sides are equivalent to 𝑖 ∈𝐼 𝑠𝑖 = ⊥ and 𝑐 = ⊥:
                                            d
                  !
            l                      l
      1.        𝑠𝑖 ⊕ 𝑐 = ⊥ iff        𝑠𝑖 = ⊥ and 𝑐 = ⊥                                                ,       (Equation (1))
              𝑖 ∈𝐼                            𝑖 ∈𝐼
58                                                                                                     Ahrens, Rode, Schröer, and Katoen

               l                                        l
         2.           (𝑠𝑖 ⊕ 𝑐) = ⊥   implies 𝑐 ⊑               (𝑠𝑖 ⊕ 𝑐)                                                 (𝑐 ⊑ 𝑠𝑖 ⊕ 𝑐 for all 𝑖)
               𝑖 ∈𝐼                                     𝑖 ∈𝐼
                                                                              l               l
                                     implies 𝑐 = ⊥              implies                𝑠𝑖 =          (𝑠𝑖 ⊕ 𝑐) = ⊥.                   (⊥ = 0)
                                                                              𝑖 ∈𝐼            𝑖 ∈𝐼
Conversely,           𝑖 ∈𝐼 𝑠𝑖 = ⊥ and 𝑐 = ⊥ implies
                     d                                  d                         d
                                                             𝑖 ∈𝐼 (𝑠𝑖 ⊕ 𝑐) =           𝑖 ∈𝐼 𝑠𝑖 = ⊥.                                        □
  For the remainder, we (still) assume the standing wHeyLo setting of an 𝜔-bicontinuous monoid-
module over a monoid whose natural-order lattice is a bi-Heyting algebra. The following scalar
lemma and prenexing laws hold in this general setting, without any additional assumptions on the
monoid-module structure.
  Lemma D.8 (Bottom Facts for Scalar Multiplication over Suprema). Let 𝑎 ∈ 𝑀. For every
family (𝑝 𝑣 )𝑣 ∈N in 𝑊 ,    Ä               Ä
                         𝑎⊗     𝑝 𝑣 = ⊥ iff    (𝑎 ⊗ 𝑝 𝑣 ) = ⊥.
                                           𝑣 ∈N                       𝑣 ∈N
     Proof.
          Ä                                                                Ä
       𝑎⊗   𝑝𝑣 = ⊥            implies ∀𝑣 ∈ N. 𝑎 ⊗ 𝑝 𝑣 ⊑ 𝑎 ⊗                       𝑝𝑣 = ⊥               (𝑝 𝑣 ⊑       𝑣 ∈N 𝑝 𝑣 and Lemma A.3)
                                                                                                                Ã
              𝑣 ∈N                                                         𝑣 ∈N
                              implies ∀𝑣 ∈ N. 𝑎 ⊗ 𝑝 𝑣 = ⊥                                                                         (def. of ⊥)
                                      Ä
                              implies     (𝑎 ⊗ 𝑝 𝑣 ) = ⊥.                                                                    (Equation (2))
                                          𝑣 ∈N
  Conversely, assume 𝑣 ∈N (𝑎 ⊗ 𝑝 𝑣 ) = ⊥. Then 𝑎 ⊗ 𝑝 𝑣 = ⊥ for all 𝑣 ∈ N by Equation (2). Enumerate
                       Ã
N as (𝑣𝑛 )𝑛∈N and define
                               𝑢 0 ≜ 𝑝 𝑣0 ,   𝑢𝑛+1 ≜ 𝑢𝑛 ⊔ 𝑝 𝑣𝑛+1 .
Then 𝑛∈N 𝑢𝑛 = 𝑣 ∈N 𝑝 𝑣 by the construction in Lemma B.5, and 𝑎 ⊗ 𝑢𝑛 = ⊥ for all 𝑛 ∈ N by
      Ã           Ã
induction:
                         Base: 𝑎 ⊗ 𝑢 0    = 𝑎 ⊗ 𝑝 𝑣0 = ⊥,
                         Step: 𝑎 ⊗ 𝑢𝑛+1 = 𝑎 ⊗ (𝑢𝑛 ⊔ 𝑝 𝑣𝑛+1 )
                                          ⊑ 𝑎 ⊗ (𝑢𝑛 ⊕ 𝑝 𝑣𝑛+1 )                                           (Lemma B.4 and Lemma A.3)
                                          = (𝑎 ⊗ 𝑢𝑛 ) ⊕ (𝑎 ⊗ 𝑝 𝑣𝑛+1 )                                       (distributivity of ⊗ over ⊕)
                                          =⊥⊕⊥                                            (induction hypothesis and assumption)
                                          = ⊥.
Hence
                                                      Ä                    Ä
                                                 𝑎⊗          𝑝𝑣 = 𝑎 ⊗             𝑢𝑛                                    (join construction)
                                                      𝑣 ∈N                 𝑛∈N
                                                                     Ä
                                                                 =         (𝑎 ⊗ 𝑢𝑛 )                                   (𝜔-continuity of ⊗)
                                                                     𝑛∈N
                                                                 = ⊥.                                                        (Equation (2))
                                                                                                                                           □
  Theorem D.9 (General Weighted Prenexing for Covalidity). Let 𝑎 ∈ 𝑀 be a constant scalar,
and let 𝜑,𝜓 ∈ wHeyLo with 𝑥 ∉ free(𝜓 ) and 𝑦 ∉ free(𝜑). Then the following covalidity equivalences
hold:
 Ä                         Ä                             Ä                       Ä
( 𝜑) ⊕ 𝜓 is covalid iff        (𝜑 ⊕ 𝜓 ) is covalid, 𝜑 ⊕ ( 𝜓 ) is covalid iff        (𝜑 ⊕ 𝜓 ) is covalid,
     𝑥                                𝑥                                            𝑦                                     𝑦
Towards a Verification Infrastructure for wGCL                                                                           59

    l                                l                                       l                          l
(       𝜑) ⊕ 𝜓 is covalid     iff         (𝜑 ⊕ 𝜓 ) is covalid,         𝜑⊕(       𝜓 ) is covalid   iff       (𝜑 ⊕ 𝜓 ) is covalid,
    𝑥                                𝑥                                       𝑦                          𝑦
        Ä                            Ä
𝑎⊗(           𝜑) is covalid   iff          (𝑎 ⊗ 𝜑) is covalid.
         𝑥                           𝑥

    Proof. For an arbitrary state 𝜎 ∈ Σ:
      - Case Addition over supremum.
                                                                         !
              Ä                                  Ä
                  𝜑) ⊕ 𝜓 K(𝜎) = ⊥        iff            J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ⊕ J𝜓 K(𝜎) = ⊥                   (definition of       𝑥)
                                                                                                                         Ã
         J(
              𝑥                                  𝑣 ∈N
                                               Ä
                                         iff          (J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ⊕ J𝜓 K(𝜎)) = ⊥                         (Lemma D.7)
                                               𝑣 ∈N
                                               Ä
                                         iff          (J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ⊕ J𝜓 K(𝜎 [𝑥 ↦→ 𝑣])) = ⊥               (𝑥 ∉ free(𝜓 ))
                                               𝑣 ∈N
                                                 Ä
                                         iff J        (𝜑 ⊕ 𝜓 )K(𝜎) = ⊥.                                 (definition of       𝑥)
                                                                                                                         Ã
                                                 𝑥
                                                                                    !
                   Ä                                         Ä
          J𝜑 ⊕ (       𝜓 )K(𝜎) = ⊥       iff J𝜑K(𝜎) ⊕               J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) = ⊥                (definition of       𝑦)
                                                                                                                         Ã
                   𝑦                                         𝑣 ∈N
                                               Ä
                                         iff          (J𝜑K(𝜎) ⊕ J𝜓 K(𝜎 [𝑦 ↦→ 𝑣])) = ⊥                         (Lemma D.7)
                                               𝑣 ∈N
                                               Ä
                                         iff          (J𝜑K(𝜎 [𝑦 ↦→ 𝑣]) ⊕ J𝜓 K(𝜎 [𝑦 ↦→ 𝑣])) = ⊥               (𝑦 ∉ free(𝜑))
                                               𝑣 ∈N
                                                 Ä
                                         iff J        (𝜑 ⊕ 𝜓 )K(𝜎) = ⊥.                                 (definition of       𝑦)
                                                                                                                         Ã
                                                 𝑦

        - Case Addition over infimum.
                                                     !
           l                        l
         J( 𝜑) ⊕ 𝜓 K(𝜎) = ⊥ iff                                                                         (definition of       𝑥)
                                                                                                                         d
                                      J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ⊕ J𝜓 K(𝜎) = ⊥
              𝑥                                  𝑣 ∈N
                                               l
                                     iff              (J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ⊕ J𝜓 K(𝜎)) = ⊥                         (Lemma D.7)
                                               𝑣 ∈N
                                               l
                                     iff              (J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ⊕ J𝜓 K(𝜎 [𝑥 ↦→ 𝑣])) = ⊥               (𝑥 ∉ free(𝜓 ))
                                               𝑣 ∈N
                                          l
                                     iff J (𝜑 ⊕ 𝜓 )K(𝜎) = ⊥.                                            (definition of       𝑥)
                                                                                                                         d

                                                 𝑥
                                                                                    !
                   l                                         l
                                     iff J𝜑K(𝜎) ⊕                                                       (definition of       𝑦)
                                                                                                                         d
          J𝜑 ⊕ (       𝜓 )K(𝜎) = ⊥                               J𝜓 K(𝜎 [𝑦 ↦→ 𝑣]) = ⊥
                   𝑦                                         𝑣 ∈N
                                               l
                                     iff              (J𝜑K(𝜎) ⊕ J𝜓 K(𝜎 [𝑦 ↦→ 𝑣])) = ⊥                         (Lemma D.7)
                                               𝑣 ∈N
                                               l
                                     iff              (J𝜑K(𝜎 [𝑦 ↦→ 𝑣]) ⊕ J𝜓 K(𝜎 [𝑦 ↦→ 𝑣])) = ⊥               (𝑦 ∉ free(𝜑))
                                               𝑣 ∈N
                                               l
                                     iff J                                                              (definition of       𝑦)
                                                                                                                         d
                                                      (𝜑 ⊕ 𝜓 )K(𝜎) = ⊥.
                                                 𝑦
60                                                                                        Ahrens, Rode, Schröer, and Katoen


        - Case Scalar multiplication over supremum.
                    Ä                          Ä
              J𝑎 ⊗ ( 𝜑)K(𝜎) = ⊥ iff 𝑎 ⊗          J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) = ⊥                                      (definition of   𝑥)
                                                                                                                           Ã
                        𝑥                               𝑣 ∈N
                                                 Ä
                                         iff            (𝑎 ⊗ J𝜑K(𝜎 [𝑥 ↦→ 𝑣])) = ⊥                              (Lemma D.8)
                                                 𝑣 ∈N
                                                 Ä
                                         iff J          (𝑎 ⊗ 𝜑)K(𝜎) = ⊥.                           (definitions of ⊗ and   𝑥)
                                                                                                                           Ã
                                                   𝑥
                                                                                                                               □
   The analogous scalar
                     d rule for infimum quantifiers is not included here: in the general monoid-
module setting, 𝑎 ⊗ 𝑥 𝜑 does not need to preserve covalidity in both directions without additional
assumptions.
   The preceding theorem gives judgment-preservation facts rather than formula equivalences.
For the goal-directed algorithm, these general covalidity-preservation facts would in principle
be enough for the weighted rules in the upper branch. However, the lower branch also moves
weighted addition across infimum quantifiers and there we need validity preservation. To obtain a
soundness statement for both branches, and to understand when the stronger formula equivalences
are available, we now demand that the monoid-module fulfills additional assumptions.
   Conceptually, the approach is based on the idea that similarly to Lemmas B.5 and D.8 we
would like to turn the family we quantify over into a countable chain to utilize the 𝜔-bicontinuity
assumptions. The current construction lets us turn a countable family (𝑝 𝑣 )𝑣 ∈N into an ascending
or descending chain 𝑢𝑛 with the same supremum orÃinfimum, e.g. Ã 𝑛 𝑢𝑛 =Ã 𝑣 ∈N 𝑝 𝑣 . However,
                                                                          Ã        Ã
by 𝜔-continuity of scalar multiplication    we get 𝑎 ⊗ 𝑣 ∈N 𝑝 𝑣 = 𝑎 ⊗ 𝑛 𝑢𝑛 = 𝑛 (𝑎 ⊗ 𝑢𝑛 ), but the
prenexed expression would be 𝑣 ∈N (𝑎 ⊗ 𝑝 𝑣 ). These are not the same unless scalar multiplication
                                 Ã
also preserves the finite joins used to build 𝑢𝑛 , i.e. unless we know 𝑎 ⊗ (𝑝 ⊔ 𝑞) = (𝑎 ⊗ 𝑝) ⊔ (𝑎 ⊗ 𝑞).
   Lemma D.10 (Countable Extrema Preservation for Weighted Maps). Let W = (𝑊 , ⊕, 0, ⊗)
be an 𝜔-bicontinuous monoid-module over a monoid M whose natural-order lattice is a bi-Heyting
algebra, and let (𝑝 𝑣 )𝑣 ∈N be a family in 𝑊 . Then:
    (i) If a fixed 𝑐 ∈ 𝑊 satisfies
                            (𝑝 ⊔ 𝑞) ⊕ 𝑐 = (𝑝 ⊕ 𝑐) ⊔ (𝑞 ⊕ 𝑐)                  for all 𝑝, 𝑞 ∈ 𝑊 ,
          then                                    !
                                         Ä                      Ä
                                                𝑝𝑣 ⊕ 𝑐 =               (𝑝 𝑣 ⊕ 𝑐).
                                         𝑣 ∈N                   𝑣 ∈N
     (ii) If a fixed 𝑐 ∈ 𝑊 satisfies
                            (𝑝 ⊓ 𝑞) ⊕ 𝑐 = (𝑝 ⊕ 𝑐) ⊓ (𝑞 ⊕ 𝑐)                  for all 𝑝, 𝑞 ∈ 𝑊 ,
          then                                    !
                                         l                      l
                                                𝑝𝑣 ⊕ 𝑐 =               (𝑝 𝑣 ⊕ 𝑐).
                                         𝑣 ∈N                   𝑣 ∈N
     (iii) If a fixed 𝑎 ∈ 𝑀 satisfies
                            𝑎 ⊗ (𝑝 ⊔ 𝑞) = (𝑎 ⊗ 𝑝) ⊔ (𝑎 ⊗ 𝑞)                   for all 𝑝, 𝑞 ∈ 𝑊 ,
          then                                  Ä              Ä
                                         𝑎⊗            𝑝𝑣 =           (𝑎 ⊗ 𝑝 𝑣 ).
                                                𝑣 ∈N           𝑣 ∈N
Towards a Verification Infrastructure for wGCL                                                                 61


   (iv) If a fixed 𝑎 ∈ 𝑀 satisfies
                           𝑎 ⊗ (𝑝 ⊓ 𝑞) = (𝑎 ⊗ 𝑝) ⊓ (𝑎 ⊗ 𝑞)                          for all 𝑝, 𝑞 ∈ 𝑊 ,
         then                                       l               l
                                             𝑎⊗              𝑝𝑣 =          (𝑎 ⊗ 𝑝 𝑣 ).
                                                    𝑣 ∈N            𝑣 ∈N

  Proof. We prove the first and fourth case; the second and third is identical, replacing ascending
chains by descending chains or addition by scalar multiplication. For (i), enumerate N as (𝑣𝑛 )𝑛∈N
and define
                                 𝑢 0 ≜ 𝑝 𝑣0 ,   𝑢𝑛+1 ≜ 𝑢𝑛 ⊔ 𝑝 𝑣𝑛+1 .
Then (𝑢𝑛 )𝑛∈N is ascending and 𝑛∈N 𝑢𝑛 = 𝑣 ∈N 𝑝 𝑣 according to the proof of Lemma B.5. To see
                                Ã             Ã
that (𝑢𝑛 ⊕ 𝑐)𝑛∈N is the corresponding chain for (𝑝 𝑣 ⊕ 𝑐)𝑣 ∈N , define
                                 𝑤 0 ≜ 𝑝 𝑣0 ⊕ 𝑐,              𝑤𝑛+1 ≜ 𝑤𝑛 ⊔ (𝑝 𝑣𝑛+1 ⊕ 𝑐).
We show by induction that 𝑤𝑛 = 𝑢𝑛 ⊕ 𝑐 for all 𝑛. The base case is immediate. For the induction
step, using the binary join-preservation assumption,
                      𝑤𝑛+1 = (𝑢𝑛 ⊕ 𝑐) ⊔ (𝑝 𝑣𝑛+1 ⊕ 𝑐) = (𝑢𝑛 ⊔ 𝑝 𝑣𝑛+1 ) ⊕ 𝑐 = 𝑢𝑛+1 ⊕ 𝑐.
Therefore, again by the construction in Lemma B.5,
                              Ä              Ä      Ä
                                  (𝑢𝑛 ⊕ 𝑐) =   𝑤𝑛 =   (𝑝 𝑣 ⊕ 𝑐).
                                       𝑛∈N                   𝑛∈N             𝑣 ∈N
Hence                            !                       !
                          Ä                   Ä                       Ä                    Ä
                                𝑝𝑣 ⊕ 𝑐 =            𝑢𝑛 ⊕ 𝑐 =                 (𝑢𝑛 ⊕ 𝑐) =           (𝑝 𝑣 ⊕ 𝑐),
                         𝑣 ∈N                 𝑛∈N                    𝑛∈N                   𝑣 ∈N
where the middle equality uses 𝜔-continuity of weighted addition.
  For (iv), enumerate N as (𝑣𝑛 )𝑛∈N and define
                                 𝑑 0 ≜ 𝑝 𝑣0 ,  𝑑𝑛+1 ≜ 𝑑𝑛 ⊓ 𝑝 𝑣𝑛+1 .
Then (𝑑𝑛 )𝑛∈N is descending and 𝑛∈N 𝑑𝑛 = 𝑣 ∈N 𝑝 𝑣 according to the proof of Lemma B.5. To
                                   d          d
identify (𝑎 ⊗ 𝑑𝑛 )𝑛∈N with the chain generated by (𝑎 ⊗ 𝑝 𝑣 )𝑣 ∈N , define
                                  𝑒 0 ≜ 𝑎 ⊗ 𝑝 𝑣0 ,            𝑒𝑛+1 ≜ 𝑒𝑛 ⊓ (𝑎 ⊗ 𝑝 𝑣𝑛+1 ).
Again 𝑒𝑛 = 𝑎 ⊗ 𝑑𝑛 follows by induction: the base case is immediate, and
                       𝑒𝑛+1 = (𝑎 ⊗ 𝑑𝑛 ) ⊓ (𝑎 ⊗ 𝑝 𝑣𝑛+1 ) = 𝑎 ⊗ (𝑑𝑛 ⊓ 𝑝 𝑣𝑛+1 ) = 𝑎 ⊗ 𝑑𝑛+1
by the binary meet-preservation assumption. Thus
                                  l              l
                                     (𝑎 ⊗ 𝑑𝑛 ) =   (𝑎 ⊗ 𝑝 𝑣 ).
                                             𝑛∈N                     𝑣 ∈N

Thus                             l                 l                l                    l
                          𝑎⊗           𝑝𝑣 = 𝑎 ⊗          𝑑𝑛 =           (𝑎 ⊗ 𝑑𝑛 ) =             (𝑎 ⊗ 𝑝 𝑣 ),
                                𝑣 ∈N               𝑛∈N          𝑛∈N                      𝑣 ∈N
where the middle equality uses 𝜔-cocontinuity of scalar multiplication.                                        □

  The next theorem brings these preservation properties into the form of the prenexing laws used
by the prenexing algorithm.
62                                                                                              Ahrens, Rode, Schröer, and Katoen


     Theorem D.11 (Weighted Prenexing). Assume that for every 𝑐 ∈ 𝑊 and every 𝑎 ∈ 𝑀,

             (𝑝 ⊔ 𝑞) ⊕ 𝑐 = (𝑝 ⊕ 𝑐) ⊔ (𝑞 ⊕ 𝑐),                                   (𝑝 ⊓ 𝑞) ⊕ 𝑐 = (𝑝 ⊕ 𝑐) ⊓ (𝑞 ⊕ 𝑐),               (5)
             𝑎 ⊗ (𝑝 ⊔ 𝑞) = (𝑎 ⊗ 𝑝) ⊔ (𝑎 ⊗ 𝑞)                                                                                   (6)

for all 𝑝, 𝑞 ∈ 𝑊 . Let 𝑎 ∈ 𝑀 be a constant scalar, and let 𝜑,𝜓 ∈ wHeyLo with 𝑥 ∉ free(𝜓 ) and
𝑦 ∉ free(𝜑). Then:
                 Ä            Ä                               Ä      Ä
                ( 𝜑) ⊕ 𝜓 ≡       (𝜑 ⊕ 𝜓 ),               𝜑 ⊕ ( 𝜓) ≡    (𝜑 ⊕ 𝜓 ),
                     𝑥                 𝑥                                                 𝑦          𝑦
                     l                 l                                                 l          l
                 (        𝜑) ⊕ 𝜓 ≡         (𝜑 ⊕ 𝜓 ),                              𝜑⊕(        𝜓) ≡       (𝜑 ⊕ 𝜓 ),
                      𝑥                𝑥                                                 𝑦          𝑦
                          Ä            Ä
                 𝑎⊗(            𝜑) ≡       (𝑎 ⊗ 𝜑).
                           𝑥           𝑥

If, additionally, this scalar 𝑎 preserves binary meets, i.e.

                               𝑎 ⊗ (𝑝 ⊓ 𝑞) = (𝑎 ⊗ 𝑝) ⊓ (𝑎 ⊗ 𝑞)                      for all 𝑝, 𝑞 ∈ 𝑊 ,

then also
                                                          l              l
                                                    𝑎⊗(       𝜑) ≡            (𝑎 ⊗ 𝜑).
                                                          𝑥               𝑥

  Proof. We show equality of denotations in an arbitrary state 𝜎 ∈ Σ. For the first addition-over-
supremum clause:
                                                  !
             Ä                 Ä
           J( 𝜑) ⊕ 𝜓 K(𝜎) =       J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ⊕ J𝜓 K(𝜎)
                  𝑥                         𝑣 ∈N
                                           Ä
                                       =            (J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ⊕ J𝜓 K(𝜎))                                     (Lemma D.10)
                                           𝑣 ∈N
                                           Ä
                                       =            (J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) ⊕ J𝜓 K(𝜎 [𝑥 ↦→ 𝑣]))                            (𝑥 ∉ free(𝜓 ))
                                           𝑣 ∈N
                                            Ä
                                       =J           (𝜑 ⊕ 𝜓 )K(𝜎).
                                                𝑥

The right-hand addition-over-supremum clause is symmetric.
  The two addition-over-infimum clauses are proved in the same way, using the meet-preservation
part of Lemma D.10.
  For scalar multiplication over supremum:
                                 Ä              Ä
                           J𝑎 ⊗ ( 𝜑)K(𝜎) = 𝑎 ⊗      J𝜑K(𝜎 [𝑥 ↦→ 𝑣])
                                            𝑥                            𝑣 ∈N
                                                                  Ä
                                                              =          (𝑎 ⊗ J𝜑K(𝜎 [𝑥 ↦→ 𝑣]))                      (Lemma D.10)
                                                                  𝑣 ∈N
                                                                   Ä
                                                              =J         (𝑎 ⊗ 𝜑)K(𝜎).
                                                                    𝑥

The scalar-over-infimum clause follows analogously from the additional binary meet-preservation
assumption for 𝑎.                                                                             □
Towards a Verification Infrastructure for wGCL                                                      63


  We now connect the preservation assumptions in Theorem D.11 to the main classes of domains
used in this paper, as summarized in Figure 5. The point is that totality, Booleanity of the natural-
order lattice, and idempotence of weighted addition are distinct assumptions: Booleanity gives the
logical connectives, whereas idempotence identifies weighted addition with lattice join.
   Corollary D.12 (Totally Ordered Weighted Prenexing). If the natural order of the monoid-
module is total, then all weighted prenexing equivalences from Theorem D.11, including scalar multi-
plication over infimum quantifiers, hold. This covers the totally ordered weighted domains considered
in Figure 5.
  Proof. Fix 𝑐 ∈ 𝑊 , 𝑎 ∈ 𝑀, and 𝑝, 𝑞 ∈ 𝑊 . Since the natural order is total, assume without loss of
generality that 𝑝 ⊑ 𝑞. Then 𝑝 ⊔ 𝑞 = 𝑞 and 𝑝 ⊓ 𝑞 = 𝑝. By Lemmas A.3 and A.4, weighted addition
and scalar multiplication are monotone, so 𝑝 ⊕ 𝑐 ⊑ 𝑞 ⊕ 𝑐 and 𝑎 ⊗ 𝑝 ⊑ 𝑎 ⊗ 𝑞. Hence
                  (𝑝 ⊔ 𝑞) ⊕ 𝑐 = (𝑝 ⊕ 𝑐) ⊔ (𝑞 ⊕ 𝑐),        (𝑝 ⊓ 𝑞) ⊕ 𝑐 = (𝑝 ⊕ 𝑐) ⊓ (𝑞 ⊕ 𝑐),
and likewise
                 𝑎 ⊗ (𝑝 ⊔ 𝑞) = (𝑎 ⊗ 𝑝) ⊔ (𝑎 ⊗ 𝑞),         𝑎 ⊗ (𝑝 ⊓ 𝑞) = (𝑎 ⊗ 𝑝) ⊓ (𝑎 ⊗ 𝑞).
Thus the addition assumptions, the scalar join assumption, and the additional scalar meet-preservation
assumption of Theorem D.11 all hold. Hence Theorem D.11 applies.                                   □

  Lemma D.13 (Idempotent Addition Is Lattice Join). Let W = (𝑊 , ⊕, 0, ⊗) be a monoid-module
whose natural order is a partial order and admits binary joins. Then
                      ∀𝑝 ∈ 𝑊 . 𝑝 ⊕ 𝑝 = 𝑝           iff       ∀𝑝, 𝑞 ∈ 𝑊 . 𝑝 ⊕ 𝑞 = 𝑝 ⊔ 𝑞.
   Proof. The ⇐ direction is immediate because 𝑝 ⊔ 𝑝 = 𝑝. For the ⇒ direction, assume that ⊕ is
idempotent. The element 𝑝 ⊕ 𝑞 is an upper bound of 𝑝 and 𝑞 by the definition of the natural order.
Let 𝑟 be any upper bound of 𝑝 and 𝑞. Then 𝑝 ⊑ 𝑟 and 𝑞 ⊑ 𝑟 , so choose 𝑚, 𝑛 ∈ 𝑊 with 𝑝 ⊕ 𝑚 = 𝑟
and 𝑞 ⊕ 𝑛 = 𝑟 . By idempotence,
                            𝑝 ⊕ 𝑟 = 𝑝 ⊕ 𝑝 ⊕ 𝑚 = 𝑟,         𝑞 ⊕ 𝑟 = 𝑞 ⊕ 𝑞 ⊕ 𝑛 = 𝑟.
Hence (𝑝 ⊕ 𝑞) ⊕ 𝑟 = 𝑝 ⊕ (𝑞 ⊕ 𝑟 ) = 𝑝 ⊕ 𝑟 = 𝑟 , and therefore 𝑝 ⊕ 𝑞 ⊑ 𝑟 . Thus 𝑝 ⊕ 𝑞 is the least upper
bound of 𝑝 and 𝑞.                                                                                   □

  Corollary D.14 (Idempotent Weighted Prenexing). If weighted addition is idempotent, then
the addition rules and the scalar-over-supremum rule from Theorem D.11 hold. This applies in particular
when ⊕ is disjunction or union, as in the Boolean semiring and the formal-language module. If,
additionally, each scalar map 𝑝 ↦→ 𝑎 ⊗ 𝑝 preserves binary meets, then scalar multiplication also
prenexes over infimum quantifiers.
   Proof. By Lemma D.13, weighted addition coincides with the lattice join. Thus 𝑝 ↦→ 𝑝 ⊕ 𝑐
is the map 𝑝 ↦→ 𝑝 ⊔ 𝑐, which preserves binary joins by associativity of ⊔ and binary meets by
distributivity of the bi-Heyting lattice:
                                        (𝑝 ⊓ 𝑞) ⊔ 𝑐 = (𝑝 ⊔ 𝑐) ⊓ (𝑞 ⊔ 𝑐).
Moreover,
                  𝑎 ⊗ (𝑝 ⊔ 𝑞) = 𝑎 ⊗ (𝑝 ⊕ 𝑞) = (𝑎 ⊗ 𝑝) ⊕ (𝑎 ⊗ 𝑞) = (𝑎 ⊗ 𝑝) ⊔ (𝑎 ⊗ 𝑞),
so every scalar map preserves binary joins. The claims follow from Theorem D.11.                     □
64                                                                          Ahrens, Rode, Schröer, and Katoen


   A Note on Boolean natural-order lattices. A Boolean natural-order lattice gives the Boolean
implication and coimplication, but it does not by itself demand the required behavior of ⊕ or ⊗.
The concrete Boolean examples in Figure 5 satisfy the stronger idempotent-addition assumption
above: in the Boolean semiring addition is disjunction, and in the formal-language module addition
is union. In these examples scalar meet preservation also holds, because Boolean multiplication
and fixed-word prefixing preserve intersections.
   Example D.15 (Counterexample: Scalar Infimum Prenexing). The previous formal-language coun-
terexample used a language such as {𝑐, 𝑐𝑐} as a scalar, but in the formal-language monoid-module
Wlang scalars are words 𝑔 ∈ Γ ∗ , not languages. Thus that construction was not a counterexample
for our monoid-module framework.
   Consider the expectation monoid-module Wprob with its componentwise natural order. Let the
scalar be 𝑎 = (1, 1), and define
                          𝜑 ≜ ( ? (𝑥 < 1) ⊓ (0, 100)) ⊔ ( ? (¬(𝑥 < 1)) ⊓ (1, 0)).
Then J𝜑K(𝜎 [𝑥 ↦→ 0]) = (0, 100) and J𝜑K(𝜎 [𝑥 ↦→ 𝑛]) = (1, 0) for all 𝑛 ≥ 1, hence
                                  l
                             𝑎 ⊗ J 𝜑K(𝜎) = (1, 1) ⊗ (0, 0) = (0, 0),
                                        𝑥

                          l
                      J       (𝑎 ⊗ 𝜑)K(𝜎) = ((1, 1) ⊗ (0, 100)) ⊓ ((1, 1) ⊗ (1, 0))
                          𝑥
                                            = (0, 100) ⊓ (1, 1)
                                            = (0, 1).

  Therefore 𝑎 ⊗ 𝑥 𝜑 . 𝑥 (𝑎 ⊗ 𝜑). Thus scalar multiplication does not prenex over infimum
                  d        d
quantifiers in the general monoid-module setting.
  Lemma D.16 (Conditional Weighted Prenexing). Let 𝑎 ∈ 𝑀 and 𝜑 ∈ wHeyLo. If 𝜑 is boolean-
valued (i.e., ImJ𝜑K ⊆ {⊥, ⊤}), then scalar multiplication distributes over the infimum:
                                                !
                                           l         l
                                      𝑎⊗      𝜑 ≡ (𝑎 ⊗ 𝜑).
                                                𝑥         𝑥

   Proof. Let 𝜎 ∈ Σ. Let 𝑆 = {J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) | 𝑣 ∈ N} be the set of values over which the infimum
is taken. Since 𝜑 is boolean-valued, 𝑆 ⊆ {⊥, ⊤}. We distinguish two cases based on the value of the
quantifier:
      - Case 1: J 𝑥 𝜑K(𝜎) = ⊥. By the definition of infimum, this implies that ⊥ ∈ 𝑆, because
                  d
        ImJ𝜑K ⊆ {⊥, ⊤}.
           – LHS: 𝑎 ⊗ ⊥ = ⊥ by the annihilation axiom of monoid-modules.
           – RHS: Since ⊥ ∈ 𝑆, the set of distributed values {𝑎 ⊗ 𝑠 | 𝑠 ∈ 𝑆 } contains the element
             𝑎 ⊗ ⊥. Since 𝑎 ⊗ ⊥ = ⊥ and ⊥ is the least element, the infimum of this set is ⊥.
        Thus, LHS d= RHS = ⊥.
      - Case 2: J 𝑥 𝜑K(𝜎) = ⊤. This implies that for all 𝑣, J𝜑K(𝜎 [𝑥 ↦→ 𝑣]) = ⊤. Thus, 𝑆 = {⊤}.
           – LHS: 𝑎 ⊗ ⊤.
           – RHS: The set of distributed values is {𝑎 ⊗ ⊤}. The infimum is trivially 𝑎 ⊗ ⊤.
        Thus, LHS = RHS = 𝑎 ⊗ ⊤.
                                                                                                           □
Towards a Verification Infrastructure for wGCL                                                                           65


   Summary of weighted prenexing assumptions. In the table below, ✓ means that the corresponding
formula equivalence is guaranteed, cov means that only the covalidity-preservation statement from
Theorem D.9 is guaranteed, and – means that the property is not forced by the assumption. The
hook arrows indicate strengthening implications between the assumptions, i.e. the second row
implies the first.
                                                                                           ⊕          ⊕d     ⊗        ⊗d
Assumption
                                                                                         over       over   over     over
                                                                                              Ã                 Ã

General 𝜔-bicontinuous module                                                                 cov    cov    cov      –
Total natural order                                                                            ✓      ✓      ✓       ✓
Boolean natural-order lattice                                                                  –      –      –       –
↩→ Idempotent weighted addition                                                                ✓      ✓      ✓       –
↩→ ↩→ Idempotent addition and scalar meet preservation                                         ✓      ✓      ✓       ✓
The total-order row covers the totally ordered examples from Figure 5, such as Wtrop , Wnats , and
Wprob . The last row covers the concrete Boolean examples there, such as Wbool and Wlang .

D.2    Goal-Directed qelim
In this subsection, we fix the standing assumptions from Sections 2 and 3 together with the wHeyLo
semantics from Table 1: the underlying domain is an 𝜔-bicontinuous monoid-module over a monoid,
together with an implication and coimplication such that the induced weighting domain forms a
bi-Heyting algebra. Thus, for every 𝜑 ∈ wHeyLo,
          𝜑 is valid    iff ∀𝜎 ∈ Σ. J𝜑K(𝜎) = ⊤,                  𝜑 is covalid            iff ∀𝜎 ∈ Σ. J𝜑K(𝜎) = ⊥.
  The proof of Theorem 7.2 proceeds in three steps. First, auxiliary procedures prenex↓ (·) and
prenex↑ (·) move quantifiers to the front while preserving formula equivalence. Second, auxiliary
procedures strip↓ (·, ·) and strip↑ (·, ·) remove the resulting leading quantifier block. Third, we show
that the displayed procedure in Figure 13 is exactly strip ◦ prenex. Completeness is then treated
separately on a syntactic fragment where the prenexed matrix is quantifier-free.


  Definition D.17 (Quantifier-Free Matrices and Prenex Outputs). We write 𝜓 ∈ wHeyLoqf iff 𝜓
contains no occurrences of 𝑥 or 𝑥 . We write 𝜖 for the empty variable list, 𝑥 𝑥® for prefixing a
                                 d     Ã
variable to a list, and 𝑥®𝑦® for concatenation.
  For a variable list 𝑥,
                       ® define iterated quantification by
                                     l             l       ll
                                        𝜓 ≜ 𝜓,        𝜓≜      𝜓,
                                           𝜖                  𝑥 𝑥®         𝑥    𝑥®

and dually
                                      Ä                   Ä               ÄÄ
                                               𝜓 ≜ 𝜓,                𝜓≜                  𝜓.
                                       𝜖                      𝑥 𝑥®         𝑥        𝑥®
   We identify lower prenex outputs with formulas by
                                                                          l
                                                ⟨®
                                                 𝑥,𝜓 ⟩ ∈ P↓          =
                                                                     b         𝜓,
                                                                          𝑥®

and dually upper prenex outputs by
                                                                         Ä
                                                ⟨®
                                                 𝑥,𝜓 ⟩ ∈ P↑          =
                                                                     b         𝜓.
                                                                          𝑥®
66                                                                         Ahrens, Rode, Schröer, and Katoen


                 Lower Branch                                         Upper Branch
              prenex↓ (·) (prenexing)                              prenex↑ (·) (prenexing)
              𝛼 ↦→ ⟨𝜖, 𝛼⟩   for atomic 𝛼, ⊤, ⊥                     𝛼 ↦→ ⟨𝜖, 𝛼⟩   for atomic 𝛼, ⊤, ⊥
                   𝑥, △(𝜓 )⟩
          △(Ψ) ↦→ ⟨®                                                   𝑥, ▽(𝜓 )⟩
                                                              ▽(Ψ) ↦→ ⟨®
           where prenex↓ (Ψ) = ⟨®
                                𝑥,𝜓 ⟩                           where prenex↑ (Ψ) = ⟨®
                                                                                     𝑥,𝜓 ⟩
        𝜑 1 ★ 𝜑 2 ↦→ ⟨® ® ★ 𝜒⟩
                      𝑥𝑦,𝜓                                  𝜑 1 ★ 𝜑 2 ↦→ ⟨® ® ★ 𝜒⟩
                                                                          𝑥𝑦,𝜓
           where prenex↓ (𝜑 1 ) = ⟨®
                                   𝑥,𝜓 ⟩                        where prenex↑ (𝜑 1 ) = ⟨®
                                                                                        𝑥,𝜓 ⟩
           and prenex↓ (𝜑 2 ) = ⟨®
                                 𝑦, 𝜒⟩                          and prenex↑ (𝜑 2 ) = ⟨®
                                                                                      𝑦, 𝜒⟩
           for ★ ∈ {⊓, ⊔, ⊕}                                    for ★ ∈ {⊓, ⊔, ⊕}
         𝑎 ⊗ Ψ ↦→ ⟨®
                   𝑥, 𝑎 ⊗ 𝜓 ⟩                                 𝑎 ⊗ Ψ ↦→ ⟨®
                                                                        𝑥, 𝑎 ⊗ 𝜓 ⟩
           where prenex↓ (Ψ) = ⟨®
                                𝑥,𝜓 ⟩                           where prenex↑ (Ψ) = ⟨®
                                                                                     𝑥,𝜓 ⟩
       𝜑 1 → 𝜑 2 ↦→ ⟨® ® → 𝜒⟩
                     𝑥𝑦,𝜓                                  𝜑 1 ← 𝜑 2 ↦→ ⟨® ® ← 𝜒⟩
                                                                         𝑥𝑦,𝜓
           where prenex↑ (𝜑 1 ) = ⟨®
                                   𝑥,𝜓 ⟩                        where prenex↓ (𝜑 1 ) = ⟨®
                                                                                        𝑥,𝜓 ⟩
           and prenex (𝜑 2 ) = ⟨®
                     ↓          𝑦, 𝜒⟩                          and prenex↑ (𝜑 2 ) = ⟨®
                                                                                     𝑦, 𝜒⟩

           𝑥 Ψ ↦→ ⟨𝑥 𝑥,𝜓                                       𝑥 Ψ ↦→ ⟨𝑥 𝑥,𝜓
          d                                                   Ã
                     ® ⟩                                                 ® ⟩
           where prenex↓ (Ψ) = ⟨®
                                𝑥,𝜓 ⟩                           where prenex↑ (Ψ) = ⟨®
                                                                                     𝑥,𝜓 ⟩
              𝜑 ↦→ ⟨𝜖, 𝜑⟩   otherwise                              𝜑 ↦→ ⟨𝜖, 𝜑⟩   otherwise

Fig. 16. Algorithm prenex. The lower branch produces a prefix of infimum quantifiers, and the upper branch
a prefix of supremum quantifiers. In binary cases, prefixes are concatenated in left-to-right order.


Accordingly, we write
                   P↓ ≜ {⟨®
                          𝑥,𝜓 ⟩ | 𝜓 ∈ wHeyLo},         P↑ ≜ {⟨®
                                                              𝑥,𝜓 ⟩ | 𝜓 ∈ wHeyLo}.


  Definition D.18 (Algorithm prenex). Figure 16 defines functions prenex↓ (·) : wHeyLo → P↓ and
    Ã (·) : wHeyLo → P↑ . If prenex (𝜑) = ⟨®   𝑥,𝜓 ⟩, then 𝜑 ≡ 𝑥® 𝜓 ; if prenex↑ (𝜑) = ⟨®
                                                                                        𝑥,𝜓 ⟩, then
       ↑                              ↓
                                                               d
prenex
𝜑 ≡ 𝑥® 𝜓 . Moreover, by Theorem D.21,
                                                   𝑥,𝜓 ⟩ with 𝜓 ∈ wHeyLoqf ,
                     𝜑 ∈ wHeyLo↓ =⇒ prenex↓ (𝜑) = ⟨®
                                                   𝑥,𝜓 ⟩ with 𝜓 ∈ wHeyLoqf .
                     𝜑 ∈ wHeyLo↑ =⇒ prenex↑ (𝜑) = ⟨®


     Lemma D.19 (Validation and Covalidation Reflection). For every 𝜑 ∈ wHeyLo:
                △(𝜑) is valid    iff 𝜑 is valid,     ▽(𝜑) is covalid    iff 𝜑 is covalid.
  Proof. Let 𝜎 ∈ Σ. By definition, J△(𝜑)K(𝜎) = ⊤ iff J𝜑K(𝜎) = ⊤. Hence △(𝜑) is valid            iff 𝜑 is valid.
Dually, J▽(𝜑)K(𝜎) = ⊥ iff J𝜑K(𝜎) = ⊥, so ▽(𝜑) is covalid iff 𝜑 is covalid.                               □


     Theorem D.20 (Soundness of prenex). Assume the hypotheses of Theorem D.11. Then:
      (i) If prenex↓ (𝜑) = ⟨®
                                           d
                            𝑥,𝜓 ⟩, then 𝜑 ≡ 𝑥® 𝜓 .
Towards a Verification Infrastructure for wGCL                                                                                      67


    (ii) If prenex↑ (𝜑) = ⟨®
                                                   Ã
                           𝑥,𝜓 ⟩, then 𝜑 ≡                  𝑥® 𝜓 .

  Proof. This is a direct mutual induction: each recursive clause of Figure 16 is justified by the
corresponding prenexing theorem stated above. We prove both clauses simultaneously by induction
on the recursive evaluation of Figure 16.
   Lower branch.
     - Case 𝛼, ⊤, or ⊥. Immediate.
     - Case △(Ψ). Let prenex↓ (Ψ) = ⟨®
                                     𝑥,𝜓 ⟩. IH: Ψ ≡ 𝑥® 𝜓 . By repeated application of the validation
                                                    d
       clause of Theorem D.1,
                                                  !
                                             l       l
                                 △(Ψ) ≡ △       𝜓 ≡      △(𝜓 ) .
                                                                     𝑥®                𝑥®

      - Case 𝜑 1 ★𝜑 2 , ★ ∈ {⊓, ⊔}. Let prenex↓ (𝜑 𝑖 ) = ⟨®
                                                          𝑥𝑖 ,𝜓𝑖 ⟩. IH: 𝜑 𝑖 ≡                          𝑥®𝑖 𝜓𝑖 . By repeated application
                                                                                                       d
         of the ★-clauses of Theorem D.1,
                                          l        l       l
                             𝜑 1 ★ 𝜑 2 ≡ ( 𝜓1 ) ★ ( 𝜓2 ) ≡   (𝜓 1 ★ 𝜓 2 ).
                                                 𝑥®1                       𝑥®2              𝑥®1 𝑥®2

      - Case 𝜑 1 ⊕ 𝜑 2 . Let prenex↓ (𝜑 𝑖 ) = ⟨®
                                               𝑥𝑖 ,𝜓𝑖 ⟩. IH: 𝜑 𝑖 ≡ 𝑥®𝑖 𝜓𝑖 . By repeated application of
                                                                   d
        Theorem D.11,
                                         l          l           l
                            𝜑 1 ⊕ 𝜑 2 ≡ ( 𝜓1 ) ⊕ ( 𝜓2 ) ≡         (𝜓 1 ⊕ 𝜓 2 ).
                                                 𝑥®1                       𝑥®2              𝑥®1 𝑥®2

      - Case 𝑎 ⊗ Ψ. Let prenex↓ (Ψ) = ⟨®
                                       𝑥,𝜓 ⟩. IH: Ψ ≡ 𝑥® 𝜓 . By repeated application of the scalar-
                                                                                      d
        infimum clause of Theorem D.11,
                                               l     l
                                 𝑎 ⊗ Ψ ≡ 𝑎 ⊗ 𝜓 ≡ (𝑎 ⊗ 𝜓 ).
                                                                      𝑥®              𝑥®

      - Case d
             𝜑 1 → 𝜑 2 . Let prenex↑ (𝜑 1 ) = ⟨®
                                               𝑥,𝜓 ⟩ and prenex↓ (𝜑 2 ) = ⟨®
                                                                           𝑦, 𝜒⟩. IH: 𝜑 1 ≡                                   𝑥® 𝜓 and
                                                                                                                           Ã
        𝜑 2 ≡ 𝑦® 𝜒. By repeated application of Theorems D.1 and D.2,
                                         Ä           l      l
                           𝜑 1 → 𝜑 2 ≡ ( 𝜓 ) → ( 𝜒) ≡ (𝜓 → 𝜒).
                                                       𝑥®                        𝑦®            𝑥® 𝑦®

      - Case 𝑥      Ψ. Let prenex↓ (Ψ) = ⟨®
                                          𝑥,𝜓 ⟩. IH: Ψ ≡
                                                     𝑥® 𝜓 . Since d𝑥 Ψ ≡ 𝑥 𝑥® 𝜓 , immediate.
               d                                                  d     d             d

      - Case otherwise. Immediate from prenex↓ (𝜑) = ⟨𝜖, 𝜑⟩ and 𝜖 𝜑 = 𝜑.
   Upper branch.
     - Case 𝛼, ⊤, or ⊥. Immediate.
     - Case ▽(Ψ). Let prenex↑ (Ψ) = ⟨®
                                     𝑥,𝜓 ⟩. IH: Ψ ≡ 𝑥® 𝜓 . By repeated application of the covali-
                                                   Ã
       dation clause of Theorem D.1,
                                                 !
                                            Ä      Ä
                                ▽(Ψ) ≡ ▽       𝜓 ≡     ▽(𝜓 ) .
                                                                     𝑥®                𝑥®

      - Case 𝜑 1 ★𝜑 2 , ★ ∈ {⊓, ⊔}. Let prenex↑ (𝜑 𝑖 ) = ⟨®
                                                          𝑥𝑖 ,𝜓𝑖 ⟩. IH: 𝜑 𝑖 ≡ 𝑥®𝑖 𝜓𝑖 . By repeated application
                                                                             Ã
         of the upper clauses of Theorem D.1,
                                         Ä        Ä       Ä
                            𝜑 1 ★ 𝜑 2 ≡ ( 𝜓1 ) ★ ( 𝜓2 ) ≡   (𝜓 1 ★ 𝜓 2 ).
                                                 𝑥®1                       𝑥®2              𝑥®1 𝑥®2
68                                                                          Ahrens, Rode, Schröer, and Katoen


     - Case 𝜑 1 ⊕ 𝜑 2 . Let prenex↑ (𝜑 𝑖 ) = ⟨®
                                              𝑥𝑖 ,𝜓𝑖 ⟩. IH: 𝜑 𝑖 ≡ 𝑥®𝑖 𝜓𝑖 . By repeated application of
                                                                  Ã
       Theorem D.11,
                                       Ä           Ä           Ä
                          𝜑 1 ⊕ 𝜑 2 ≡ ( 𝜓1 ) ⊕ ( 𝜓2 ) ≡          (𝜓 1 ⊕ 𝜓 2 ).
                                       𝑥®1          𝑥®2          𝑥®1 𝑥®2

     - Case 𝑎 ⊗ Ψ. Let prenex↑ (Ψ) = ⟨®
                                      𝑥,𝜓 ⟩. IH: Ψ ≡ 𝑥® 𝜓 . By repeated application of the scalar
                                                    Ã
       clause of Theorem D.11,
                                              Ä            Ä
                                 𝑎⊗Ψ≡𝑎⊗             𝜓≡          (𝑎 ⊗ 𝜓 ).
                                               𝑥®          𝑥®

     - Case Ã
            𝜑 1 ← 𝜑 2 . Let prenex↓ (𝜑 1 ) = ⟨®
                                              𝑥,𝜓 ⟩ and prenex↑ (𝜑 2 ) = ⟨®
                                                                          𝑦, 𝜒⟩. IH: 𝜑 1 ≡         𝑥® 𝜓 and
                                                                                                 d
       𝜑 2 ≡ 𝑦® 𝜒. By repeated application of Theorems D.1 and D.2,
                                       l           Ä       Ä
                          𝜑1 ← 𝜑2 ≡ ( 𝜓 ) ← (         𝜒) ≡    (𝜓 ← 𝜒).
                                         𝑥®           𝑦®          𝑥® 𝑦®

     - Case 𝑥 Ψ. Let prenex↑ (Ψ) = ⟨®
                                    𝑥,𝜓 ⟩. IH: Ψ ≡ 𝑥® 𝜓 . Since 𝑥 Ψ ≡ 𝑥 𝑥® 𝜓 , immediate.
             Ã                                             Ã   Ã      Ã
     - Case otherwise. Immediate from prenex↑ (𝜑) = ⟨𝜖, 𝜑⟩ and 𝜖 𝜑 = 𝜑.
                                                               Ã

                                                                                                           □


  Theorem D.21 (Prenex Completeness on the qelim Fragment). Assume the hypotheses of
Theorem D.11. Then:
    (i) If 𝜑 ∈ wHeyLo↓ , then prenex↓ (𝜑) = ⟨®
                                             𝑥,𝜓 ⟩ for some 𝑥,𝜓
                                                            ® , and every such result satisfies
        𝜓 ∈ wHeyLoqf .
   (ii) If 𝜑 ∈ wHeyLo↑ , then prenex↑ (𝜑) = ⟨®
                                             𝑥,𝜓 ⟩ for some 𝑥,𝜓
                                                            ® , and every such result satisfies
        𝜓 ∈ wHeyLoqf .
  Proof. This is again a straightforward mutual induction over the fragment grammar: every
constructor in the fragment maps quantifier-free recursive results to a quantifier-free matrix.
We prove both clauses simultaneously by induction on the derivation of 𝜑 ∈ wHeyLo↓ and 𝜑 ∈
wHeyLo↑ .
     - Case 𝜑 ∈ wHeyLoqf . Immediate, since prenex↓ (𝜑) = ⟨𝜖, 𝜑⟩ and prenex↑ (𝜑) = ⟨𝜖, 𝜑⟩.
     - Case △(Ψ) ∈ wHeyLo↓ . Let prenex↓ (Ψ) = ⟨®    𝑥,𝜓 ⟩. By IH, 𝜓 ∈ wHeyLoqf , hence △(𝜓 ) ∈
       wHeyLoqf .
     - Case ▽(Ψ) ∈ wHeyLo↑ . Dual.
     - Case 𝑥 Ψ ∈ wHeyLo↓ . Let prenex↓ (Ψ) = ⟨®   𝑥,𝜓 ⟩. By IH, 𝜓 ∈ wHeyLoqf .
             d

     - Case 𝑥 Ψ ∈ wHeyLo↑ . Dual.
             Ã

     - Case 𝜑 1 ★ 𝜑 2 ∈ wHeyLo↓ , ★ ∈ {⊓, ⊔, ⊕}. Let prenex↓ (𝜑 𝑖 ) = ⟨®  𝑥𝑖 ,𝜓𝑖 ⟩. By IH, 𝜓 1,𝜓 2 ∈
       wHeyLoqf , hence 𝜓 1 ★ 𝜓 2 ∈ wHeyLoqf .
     - Case 𝜑 1 ★ 𝜑 2 ∈ wHeyLo↑ , ★ ∈ {⊓, ⊔, ⊕}. Dual.
     - Case 𝜑 1 → 𝜑 2 ∈ wHeyLo↓ . Let prenex↑ (𝜑 1 ) = ⟨®  𝑥,𝜓 ⟩ and prenex↓ (𝜑 2 ) = ⟨®
                                                                                       𝑦, 𝜒⟩. By IH,
       𝜓, 𝜒 ∈ wHeyLoqf , hence 𝜓 → 𝜒 ∈ wHeyLoqf .
     - Case 𝑎 ⊗ Ψ ∈ wHeyLo↓ . Let prenex↓ (Ψ) = ⟨®   𝑥,𝜓 ⟩. By IH, 𝜓 ∈ wHeyLoqf , hence 𝑎 ⊗ 𝜓 ∈
       wHeyLoqf .
     - Case 𝜑 1 ← 𝜑 2 ∈ wHeyLo↑ . Let prenex↓ (𝜑 1 ) = ⟨®  𝑥,𝜓 ⟩ and prenex↑ (𝜑 2 ) = ⟨®
                                                                                       𝑦, 𝜒⟩. By IH,
       𝜓, 𝜒 ∈ wHeyLoqf , hence 𝜓 ← 𝜒 ∈ wHeyLoqf .
Towards a Verification Infrastructure for wGCL                                                                      69


      - Case 𝑎 ⊗ Ψ ∈ wHeyLo↑ . Let prenex↑ (Ψ) = ⟨®
                                                  𝑥,𝜓 ⟩. By IH, 𝜓 ∈ wHeyLoqf , hence 𝑎 ⊗ 𝜓 ∈
        wHeyLoqf .
                                                                                           □


  Definition D.22 (Algorithm strip). The functions strip↓ (·, ·) : P↓ → wHeyLo and strip↑ (·, ·) :
P↑ → wHeyLo are defined by the following recursive equations:
           strip↓ (𝑥 𝑥,𝜓
                     ® ) ≜ strip↓ (𝑥,
                                   ® fresh𝑥 (𝜓 )),                strip↑ (𝑥 𝑥,𝜓
                                                                            ® ) ≜ strip↑ (𝑥,
                                                                                          ® fresh𝑥 (𝜓 )),
            strip↓ (𝜖,𝜓 ) ≜ 𝜓,                                      strip↑ (𝜖,𝜓 ) ≜ 𝜓 .
By Lemma D.24,
    l                                                      Ä
      𝜓 is valid         iff           ® ) is valid,
                               strip↓ (𝑥,𝜓                       𝜓 is covalid    iff              ® ) is covalid;
                                                                                          strip↑ (𝑥,𝜓
      𝑥®                                                    𝑥®

if 𝜓 ∈ wHeyLoqf , then strip (𝑥,𝜓  ↓
                                          ® ) ∈ wHeyLoqf whenever the corresponding branch
                              ® ), strip (𝑥,𝜓     ↑

is defined.


   Lemma D.23 (Strip Eqations). For all variable lists 𝑥,
                                                       ® 𝑦® and formulas 𝜙,𝜓 :
                                          
                 ↓                   ↓
                   ® △(𝜓 )) = △ strip (𝑥,𝜓
            strip (𝑥,                  ® ) ,
              strip↓ (𝑥®𝑦,
                        ® 𝜙 ★ 𝜓 ) = strip↓ (𝑥,
                                            ® 𝜙) ★ strip↓ (𝑦,𝜓
                                                           ® )                         for ★ ∈ {⊓, ⊔, ⊕},
                strip↓ (𝑥,
                        ® 𝑎 ⊗ 𝜓 ) = 𝑎 ⊗ strip↓ (𝑥,𝜓
                                                ® ),
             strip↓ (𝑥®𝑦,
                       ® 𝜙 → 𝜓 ) = strip↑ (𝑥,
                                            ® 𝜙) → strip↓ (𝑦,𝜓
                                                           ® ),
                                                  
                strip↑ (𝑥,® ▽(𝜓 )) = ▽ strip↑ (𝑥,𝜓
                                               ® ) ,
              strip↑ (𝑥®𝑦,
                        ® 𝜙 ★ 𝜓 ) = strip↑ (𝑥,
                                            ® 𝜙) ★ strip↑ (𝑦,𝜓
                                                           ® )                         for ★ ∈ {⊓, ⊔, ⊕},
                     ↑                            ↑
                strip (𝑥,
                       ® 𝑎 ⊗ 𝜓 ) = 𝑎 ⊗ strip (𝑥,𝜓
                                              ® ),
             strip↑ (𝑥®𝑦,
                       ® 𝜙 ← 𝜓 ) = strip↓ (𝑥,
                                           ® 𝜙) ← strip↑ (𝑦,𝜓
                                                          ® ).
  Proof. All clauses follow by induction on the leftmost variable list, using Definition D.22 and
the freshness convention built into Figure 16.                                                  □


   Lemma D.24 (Stripping a Prenex Output). For every ⟨®
                                                      𝑥,𝜓 ⟩ ∈ P↓ ,
                           l
                             𝜓 is valid iff strip (𝑥,𝜓
                                                 ↓
                                                   ® ) is valid.
                                        𝑥®
For every ⟨®
           𝑥,𝜓 ⟩ ∈ P↑ ,           Ä
                                        𝜓 is covalid   iff strip↑ (𝑥,𝜓
                                                                   ® ) is covalid.
                                   𝑥®
If additionally 𝜓 ∈ wHeyLoqf , then
                           strip↓ (𝑥,𝜓
                                   ® ) ∈ wHeyLoqf ,              strip↑ (𝑥,𝜓
                                                                         ® ) ∈ wHeyLoqf .
  Proof. We prove both clauses simultaneously by induction on the recursive evaluation of
Definition D.22.
70                                                                                       Ahrens, Rode, Schröer, and Katoen


       - Case strip↓ (𝑥 𝑥,𝜓
                        ® ). By Theorem 7.1,
                              l                            l
                                𝜓 is valid iff                   fresh𝑥 (𝜓 ) is valid.
                                   𝑥 𝑥®                     𝑥®

         Then apply IH to (𝑥,® fresh𝑥 (𝜓 )).
       - Case strip↑ (𝑥 𝑥,𝜓
                        ® ). Dual, using Theorem 7.1.
       - Case strip↓ (𝜖,𝜓 ) or strip↑ (𝜖,𝜓 ). Immediate.
The quantifier-freeness clause follows by the same induction: the recursive equations of Defini-
tion D.22 only remove leading quantifiers, and the base case returns the unchanged matrix.    □



     Lemma D.25 (qelim Factors Through strip ◦ prenex). If prenex↓ (𝜑) = ⟨®
                                                                          𝑥,𝜓 ⟩, then

                                            qelim↓ (𝜑) = strip↓ (𝑥,𝜓
                                                                 ® ).

Dually, if prenex↑ (𝜑) = ⟨®
                          𝑥,𝜓 ⟩, then

                                            qelim↑ (𝜑) = strip↑ (𝑥,𝜓
                                                                 ® ).

  Proof. We prove both clauses simultaneously by induction on the recursive evaluation of
Figure 13.

     Lower branch.
       - Case 𝛼, ⊤, or ⊥. Immediate.
       - Case △(Ψ). Let prenex↓ (Ψ) = ⟨®
                                       𝑥,𝜓 ⟩. By IH and Lemma D.23,
                                                          
               qelim↓ (△(Ψ)) = △ qelim↓ (Ψ) = △ strip↓ (𝑥,𝜓
                                                          ® ) = strip↓ (𝑥,
                                                                        ® △(𝜓 )).

       - Case 𝜑 1 ★ 𝜑 2 , ★ ∈ {⊓, ⊔}. Let prenex↓ (𝜑 𝑖 ) = ⟨®
                                                            𝑥𝑖 ,𝜓𝑖 ⟩. By IH and Lemma D.23,

qelim↓ (𝜑 1 ★𝜑 2 ) = qelim↓ (𝜑 1 ) ★ qelim↓ (𝜑 2 ) = strip↓ (𝑥®1,𝜓 1 ) ★ strip↓ (𝑥®2,𝜓 2 ) = strip↓ (𝑥®1𝑥®2,𝜓 1 ★𝜓 2 ).

       - Case 𝜑 1 ⊕ 𝜑 2 . Let prenex↓ (𝜑 𝑖 ) = ⟨®
                                                𝑥𝑖 ,𝜓𝑖 ⟩. By IH and Lemma D.23,

qelim↓ (𝜑 1 ⊕ 𝜑 2 ) = qelim↓ (𝜑 1 ) ⊕ qelim↓ (𝜑 2 ) = strip↓ (𝑥®1,𝜓 1 ) ⊕ strip↓ (𝑥®2,𝜓 2 ) = strip↓ (𝑥®1𝑥®2,𝜓 1 ⊕𝜓 2 ).

       - Case 𝑎 ⊗ Ψ. Let prenex↓ (Ψ) = ⟨®
                                        𝑥,𝜓 ⟩. By IH and Lemma D.23,

                 qelim↓ (𝑎 ⊗ Ψ) = 𝑎 ⊗ qelim↓ (Ψ) = 𝑎 ⊗ strip↓ (𝑥,𝜓
                                                               ® ) = strip↓ (𝑥,
                                                                             ® 𝑎 ⊗ 𝜓 ).

       - Case 𝜑 1 → 𝜑 2 . Let prenex↑ (𝜑 1 ) = ⟨®
                                                𝑥,𝜓 ⟩ and prenex↓ (𝜑 2 ) = ⟨®
                                                                            𝑦, 𝜒⟩. By IH and Lemma D.23,

qelim↓ (𝜑 1 → 𝜑 2 ) = qelim↑ (𝜑 1 ) → qelim↓ (𝜑 2 ) = strip↑ (𝑥,𝜓
                                                              ® ) → strip↓ (𝑦,
                                                                            ® 𝜒) = strip↓ (𝑥®𝑦,𝜓
                                                                                             ® → 𝜒).

     - Case 𝑥 Ψ. Let prenex↓ (Ψ) = ⟨®     𝑥,𝜓 ⟩. By IH and Definition D.22,
             d

                     l
            qelim↓ ( Ψ) = fresh𝑥 (qelim↓ (Ψ)) = fresh𝑥 (strip↓ (𝑥,𝜓 ® )) = strip↓ (𝑥 𝑥,𝜓
                                                                                     ® ).
                         𝑥

       - Case otherwise. Immediate, since prenex↓ (𝜑) = ⟨𝜖, 𝜑⟩ and strip↓ (𝜖, 𝜑) = 𝜑 = qelim↓ (𝜑).
Towards a Verification Infrastructure for wGCL                                                                       71


   Upper branch.
     - Case 𝛼, ⊤, or ⊥. Immediate.
     - Case ▽(Ψ). Let prenex↑ (Ψ) = ⟨®
                                     𝑥,𝜓 ⟩. By IH and Lemma D.23,
                                                        
              qelim↑ (▽(Ψ)) = ▽ qelim↑ (Ψ) = ▽ strip↑ (𝑥,𝜓
                                                        ® ) = strip↑ (𝑥,
                                                                      ® ▽(𝜓 )).

      - Case 𝜑 1 ★ 𝜑 2 , ★ ∈ {⊓, ⊔}. Let prenex↑ (𝜑 𝑖 ) = ⟨®
                                                           𝑥𝑖 ,𝜓𝑖 ⟩. By IH and Lemma D.23,
qelim↑ (𝜑 1 ★𝜑 2 ) = qelim↑ (𝜑 1 ) ★ qelim↑ (𝜑 2 ) = strip↑ (𝑥®1,𝜓 1 ) ★ strip↑ (𝑥®2,𝜓 2 ) = strip↑ (𝑥®1𝑥®2,𝜓 1 ★𝜓 2 ).
      - Case 𝜑 1 ⊕ 𝜑 2 . Let prenex↑ (𝜑 𝑖 ) = ⟨®
                                               𝑥𝑖 ,𝜓𝑖 ⟩. By IH and Lemma D.23,
qelim↑ (𝜑 1 ⊕ 𝜑 2 ) = qelim↑ (𝜑 1 ) ⊕ qelim↑ (𝜑 2 ) = strip↑ (𝑥®1,𝜓 1 ) ⊕ strip↑ (𝑥®2,𝜓 2 ) = strip↑ (𝑥®1𝑥®2,𝜓 1 ⊕𝜓 2 ).
      - Case 𝑎 ⊗ Ψ. Let prenex↑ (Ψ) = ⟨®
                                       𝑥,𝜓 ⟩. By IH and Lemma D.23,
                 qelim↑ (𝑎 ⊗ Ψ) = 𝑎 ⊗ qelim↑ (Ψ) = 𝑎 ⊗ strip↑ (𝑥,𝜓
                                                               ® ) = strip↑ (𝑥,
                                                                             ® 𝑎 ⊗ 𝜓 ).
      - Case 𝜑 1 ← 𝜑 2 . Let prenex↓ (𝜑 1 ) = ⟨®
                                               𝑥,𝜓 ⟩ and prenex↑ (𝜑 2 ) = ⟨®
                                                                           𝑦, 𝜒⟩. By IH and Lemma D.23,
qelim↑ (𝜑 1 ← 𝜑 2 ) = qelim↓ (𝜑 1 ) ← qelim↑ (𝜑 2 ) = strip↓ (𝑥,𝜓
                                                              ® ) ← strip↑ (𝑦,
                                                                            ® 𝜒) = strip↑ (𝑥®𝑦,𝜓
                                                                                             ® ← 𝜒).
     - Case 𝑥 Ψ. Let prenex↑ (Ψ) = ⟨®     𝑥,𝜓 ⟩. By IH and Definition D.22,
             Ã
                     Ä
            qelim (↑
                         Ψ) = fresh𝑥 (qelim↑ (Ψ)) = fresh𝑥 (strip↑ (𝑥,𝜓
                                                                    ® )) = strip↑ (𝑥 𝑥,𝜓
                                                                                     ® ).
                         𝑥

      - Case otherwise. Immediate, since prenex↑ (𝜑) = ⟨𝜖, 𝜑⟩ and strip↑ (𝜖, 𝜑) = 𝜑 = qelim↑ (𝜑).
                                                                                                                      □
   Theorem 7.2. Assume always, W+, Wx, and extra hold. Then, for every 𝜑 ∈ wHeyLo,
          𝜑 is valid     iff qelim↓ (𝜑) is valid ,          𝜑 is covalid     iff   qelim↑ (𝜑) is covalid .
   Proof.     - Case qelim↓d(𝜑) = 𝜓 . Let prenex↓ (𝜑) = ⟨®
                                                         𝑥,𝜓 ⟩. By Lemma D.25, 𝜓 = strip↓ (𝑥,𝜓
                                                                                           ® ).
       By Theorem D.20, 𝜑 ≡ 𝑥® 𝜓 . Hence
                                       l
                     𝜑 is valid iff       𝜓 is valid                      (formula equivalence)
                                                   𝑥®
                                            iff strip↓ (𝑥,𝜓
                                                        ® ) is valid                                    (Lemma D.24)
                                            iff 𝜓 is valid.
      - Case qelim↑ (𝜑) = 𝜓 . Let prenex↑ (𝜑) = ⟨®
                                                 𝑥,𝜓 ⟩. By Lemma D.25, 𝜓 = strip↑ (𝑥,𝜓
                                                                                   ® ). By Theo-
        rem D.20, 𝜑 ≡ 𝑥® 𝜓 . Hence
                      Ã
                                         Ä
                     𝜑 is covalid iff        𝜓 is covalid                    (formula equivalence)
                                                   𝑥®
                                            iff strip↑ (𝑥,𝜓
                                                        ® ) is covalid                                  (Lemma D.24)
                                            iff 𝜓 is covalid.
                                                                                                                      □
  Theorem 7.3. Assume always, W+, Wx, and extra hold. Let wHeyLo↓, wHeyLo↑ ⊆ wHeyLo be given by
the following mutually recursive grammars, where 𝜑 qf ∈ wHeyLo is quantifier-free.
                                l
           𝜑 ↓ ::= 𝜑 qf | △ 𝜑 ↓ |  𝜑 ↓ | 𝜑 ↓ ⊓ 𝜑 ↓ | 𝜑 ↓ ⊔ 𝜑 ↓ | 𝜑 ↓ ⊕ 𝜑 ↓ | 𝑎 ⊗ 𝜑 ↓ | 𝜑 ↑ → 𝜑 ↓,
                                       𝑥
72                                                                    Ahrens, Rode, Schröer, and Katoen

                                 Ä
            𝜑 ↑ ::= 𝜑 qf | ▽ 𝜑 ↑ |  𝜑↑ | 𝜑↑ ⊓ 𝜑↑ | 𝜑↑ ⊔ 𝜑↑ | 𝜑↑ ⊕ 𝜑↑ | 𝑎 ⊗ 𝜑↑ | 𝜑↓ ← 𝜑↑.
                                  𝑥

Let 𝜑 ∈ wHeyLo↓ . Then, qelim (𝜑) ∈ wHeyLoqf . For 𝜑 ∈ wHeyLo↑, we have qelim↑ (𝜑) ∈ wHeyLoqf .
                              ↓


     Proof.     - Case 𝜑 ∈ wHeyLo↓ . Let prenex↓ (𝜑) = ⟨®𝑥,𝜓 ⟩. By Theorem D.21, 𝜓 ∈ wHeyLoqf .
         By Lemma D.25, qelim (𝜑) = strip (𝑥,𝜓
                             ↓           ↓
                                            ® ). Hence qelim↓ (𝜑) ∈ wHeyLoqf by Lemma D.24.
       - Case 𝜑 ∈ wHeyLo↑ . Let prenex (𝜑) = ⟨®
                                        ↑         𝑥,𝜓 ⟩. By Theorem D.21, 𝜓 ∈ wHeyLoqf . By
         Lemma D.25, qelim (𝜑) = strip (𝑥,𝜓
                          ↑           ↑
                                        ® ). Hence qelim↑ (𝜑) ∈ wHeyLoqf by Lemma D.24. □
                                                                                                                                                                             Towards a Verification Infrastructure for wGCL
                                                                                                             Formal                          Formal
Source                                           Access                        Why/
                    Tropical                                                                                 languages:                      languages:
statement                                        control                       provenance
                                                                                                             lower monitor                   upper monitor

𝑥 := 𝑒              as is                        as is                         as is                         as is                           as is
𝑆1 # 𝑆2             𝑇 (𝑆 1 ) # 𝑇 (𝑆 2 )          𝑇 (𝑆 1 ) # 𝑇 (𝑆 2 )           𝑇 (𝑆 1 ) # 𝑇 (𝑆 2 )           𝑇↓ (𝑆 1 ) # 𝑇↓ (𝑆 2 )           𝑇↑ (𝑆 1 ) # 𝑇↑ (𝑆 2 )
{𝑆 1 } ⊕ {𝑆 2 }     {𝑇 (𝑆 1 ) } ⊓ {𝑇 (𝑆 2 ) }     {𝑇 (𝑆 1 ) } ⊓ {𝑇 (𝑆 2 ) }    {𝑇 (𝑆 1 ) } ⊔ {𝑇 (𝑆 2 ) }     {𝑇↓† (𝑆 1 ) } ⊕ {𝑇↓† (𝑆 2 ) }   {𝑇↑ (𝑆 1 ) } ⊓ {𝑇↑ (𝑆 2 ) }
{𝑆 1 } ⊓ {𝑆 2 }     {𝑇 (𝑆 1 ) } ⊔ {𝑇 (𝑆 2 ) }     {𝑇 (𝑆 1 ) } ⊔ {𝑇 (𝑆 2 ) }    {𝑇 (𝑆 1 ) } ⊓ {𝑇 (𝑆 2 ) }     {𝑇↓ (𝑆 1 ) } ⊓ {𝑇↓ (𝑆 2 ) }     {𝑇↑† (𝑆 1 ) } ⊔ {𝑇↑† (𝑆 2 ) }
{𝑆 1 } ⊔ {𝑆 2 }     {𝑇 (𝑆 1 ) } ⊓ {𝑇 (𝑆 2 ) }     {𝑇 (𝑆 1 ) } ⊓ {𝑇 (𝑆 2 ) }    {𝑇 (𝑆 1 ) } ⊔ {𝑇 (𝑆 2 ) }     {𝑇↓† (𝑆 1 ) } ⊔ {𝑇↓† (𝑆 2 ) }   {𝑇↑ (𝑆 1 ) } ⊓ {𝑇↑ (𝑆 2 ) }
weigh 𝑎             reward 𝑎b                    coassert 𝑎b                   assert bool(𝑎)                assert ℓ ⊆ 𝑎 · Γ ∞ #            ℓ := 𝑎 −1 · ℓ
                                                                                                             ℓ := 𝑎 −1 · ℓ
assert 𝜓            coassert 𝜓b                  coassert 𝜓b                   assert bool(𝜓 )               assert ℓ ⊆ 𝜓                    ℓ := ℓ ∪ (Γ ∞ \ 𝜓 )
assume 𝜓            coassume 𝜓b                  coassume 𝜓b                   assume bool(𝜓 )               ℓ := ℓ ∩ 𝜓                      assert (Γ ∞ \ 𝜓 ) ⊆ ℓ
validate #          covalidate # coassume 𝜓b     covalidate # coassume 𝜓b      havoc 𝑝𝑎1 , . . . , 𝑝𝑎𝑛 #     𝑇↓ (validate) #𝑇↓ (assume 𝜓 )   𝑇↑† (validate) #
                                                                               validate # assume bool (𝜓 )                                   𝑇↑ (assume 𝜓 )
assume 𝜓
coassert 𝜓          assert 𝜓b                    assert 𝜓b                     coassert bool(𝜓 )             ℓ := ℓ \ 𝜓                      assert 𝜓 ⊆ ℓ
coassume 𝜓          assume 𝜓b                    assume 𝜓b                     —                             assert ℓ ⊆ Γ ∞ \ 𝜓              ℓ := ℓ ∪ 𝜓
havoc 𝑥             cohavoc 𝑥                    cohavoc 𝑥                     as is                         as is                           cohavoc 𝑥 †
cohavoc 𝑥           havoc 𝑥                      havoc 𝑥                       as is                         cohavoc 𝑥 †                     havoc 𝑥
validate            covalidate                   covalidate                    —                             assume ℓ ≠ ∅ #                  assert Γ ∞ ⊆ ℓ †
                                                                                                             ℓ := Γ ∞
covalidate          validate                     validate                      —                             assert ℓ ⊆ ∅ †                  coassert Γ ∞ ⊆ ℓ #
                                                                                                                                             ℓ := ∅ #
                                                                                                                                             covalidate

                  Table 3. Statement-level translations proved in Section E. Unmarked entries are exact equivalences from Theorems E.2, E.5, E.8,
                  E.10 and E.12. In the tropical and clearance columns, 𝜓b denotes the translated source formula in ordinary R∞    ≥0 . Tropical costs are
                  embedded by inclusion, while clearance levels use P = 0, C = 1, S = 2, and TS = ∞. The superscript † marks one-sided lax rules
                                                                     b       b       b           c
                  from Lemmas E.3 and E.6. A dash means that this appendix gives no compositional exact lowering for that statement form. In the
                  Why/provenance column, bool(𝜓 ) is defined only for crisp 𝜓 , i.e. 𝜓 (𝜎) ∈ {⊥, ⊤} for every state 𝜎; ordinary state transformers must
                  not write the fresh provenance variables, except that the displayed validate # assume 𝜓 block explicitly havocs them to quantify
                  over all provenance valuations.




                                                                                                                                                                             73
74                                                                              Ahrens, Rode, Schröer, and Katoen


E     Lowerings of wHeyVL
Table 3 summarizes the statement-level translations proved in this appendix.

E.1    Residual-Language Monitor Translation
We can translate (fragments of) wHeyVLlang over formal languages into wHeyVLbool over predicates
on residual languages. We present two translations, one for lower bounds and one for upper bounds.
They are based on residual languages, which we explain first.
E.1.1 Residual Languages. The translation maintains a language variable ℓ that stores the residual
language after the current execution prefix. That is, ℓ contains exactly those continuations that
would still complete the current prefix to a word in the original language.
   Formally, for a language 𝐿 ⊆ Γ ∞ and a word 𝑢 ∈ Γ ∗ , the residual language 𝑢 −1 · 𝐿 is defined by
𝑢 · 𝐿 = { 𝑤 | 𝑢𝑤 ∈ 𝐿 }. The upper- and lower-bound translations rely on Equations (7a) and (7b).
  −1

                            𝑎 ·𝜑 ⊆ ℓ    iff 𝜑 ⊆ 𝑎 −1 · ℓ                                                    (7a)
                            ℓ ⊆ 𝑎 ·𝜑    iff   (𝑎   −1
                                                        · ℓ ⊆ 𝜑) ∧ (ℓ ⊆ 𝑎 · Γ )
                                                                            ∞
                                                                                                            (7b)
Equation (7b) includes the additional condition ℓ ⊆ 𝑎 · Γ ∞ because quotienting alone is insufficient.
For example, if ℓ = {𝑏} for some 𝑏 ≠ 𝑎, then 𝑎 −1 · ℓ = ∅, and hence 𝑎 −1 · ℓ ⊆ 𝜑 holds for every 𝜑.
Nevertheless, ℓ ⊆ 𝑎 · 𝜑 is false, since the words in ℓ do not start with 𝑎.
E.1.2 Lower-Bound Translation. The translation rewrites each statement into a sequence of wHeyVLbool
statements that manipulate the residual language ℓ. The translated postcondition is assert (ℓ ⊆ 𝜑).
   The statement weigh 𝑎 now means that the next symbol must be 𝑎. To implement this, we first
check that every word in the current residual starts with 𝑎 (i.e., ℓ ⊆ 𝑎 · Γ ∞ ), and then update the
residual by taking the quotient with 𝑎 (i.e., ℓ := 𝑎 −1 · ℓ). Therefore, weigh 𝑎 is translated to
                                 assert (ℓ ⊆ 𝑎 · Γ ∞ ) # ℓ := 𝑎 −1 · ℓ .
  The statement assert 𝜓 checks that all possible continuations of the current execution (i.e., ℓ)
are included in 𝜓 . Thus, assert 𝜓 is translated to assert (ℓ ⊆ 𝜓 ).
  The statement assume 𝜓 restricts the current residual to continuations contained in 𝜓 . Thus,
assume 𝜓 is translated to ℓ := ℓ ∩ 𝜓 .
  The following definition formalizes the translation for a fragment of wHeyVLlang statements.
  Definition E.1 (Residual-language monitor translation). Let ℓ be fresh and range over languages
over Γ ∞ . For
                 𝑆 ::= 𝑥 := 𝑒 | assert 𝜓 | assume 𝜓 | coassert 𝜓 | coassume 𝜓
                     | validate | weigh 𝑎 | havoc 𝑥 | if (⊓) {𝑆 } else {𝑆 } | 𝑆 # 𝑆
define monitor(−) by
                       monitor(assert 𝜓 ) = assert (ℓ ⊆ 𝜓 )
                       monitor(assume 𝜓 ) = ℓ := ℓ ∩ 𝜓
                     monitor(coassert 𝜓 ) = ℓ := ℓ \ 𝜓
                     monitor(coassume 𝜓 ) = assert (ℓ ⊆ Γ ∞ \ 𝜓 )
                       monitor(validate) = assume (ℓ ≠ ∅) # ℓ := Γ ∞
                         monitor(weigh 𝑎) = assert (ℓ ⊆ 𝑎 · Γ ∞ ) # ℓ := 𝑎 −1 · ℓ
          monitor(if (⊓) {𝑆 1 } else {𝑆 2 }) = if (⊓) {monitor(𝑆 1 )} else {monitor(𝑆 2 )}
                           monitor(𝑆 1 # 𝑆 2 ) = monitor(𝑆 1 ) # monitor(𝑆 2 ) .
Towards a Verification Infrastructure for wGCL                                                                75


It leaves havoc 𝑥 and 𝑥 := 𝑒 unchanged. In the Boolean algebra of languages, 𝜓 ← 𝜑 = 𝜑 \ 𝜓 .
   The next theorem states that the encoding is sound for the lower-bound query (ℓ ⊆ vpJ𝑆K(𝜑)),
i.e., the monitor correctly tracks the residual language of the initial language 𝜑 after executing 𝑆.
Definition E.4 gives the dual translation for the upper-bound query (vpJ𝑆K(𝜑) ⊆ ℓ).
  Theorem E.2. Assume that ℓ is fresh, i.e., ℓ does not occur in 𝑆 or 𝜑. Then, for every statement 𝑆 in
the fragment above and language 𝜑,
                                   (ℓ ⊆ vpJ𝑆K(𝜑))      iff vcJmonitor(𝑆)K((ℓ ⊆ 𝜑)).
   Proof. We prove by structural induction on 𝑆.
     - Case 𝑆 = assert 𝜓 .
                   (ℓ ⊆ vpJassert 𝜓 K(𝜑))
                      iff         (ℓ ⊆ 𝜓 ∩ 𝜑)                                                           (Def. vp)
                      iff         (ℓ ⊆ 𝜓 ) ∧ (ℓ ⊆ 𝜑)                                  (Defs. subset/intersection)
                      iff         vcJassert (ℓ ⊆ 𝜓 )K((ℓ ⊆ 𝜑))                                          (Def. vc)
                      iff         vcJmonitor(assert 𝜓 )K((ℓ ⊆ 𝜑))                                 (Def. monitor)
      - Case 𝑆 = assume 𝜓 .
                       (ℓ ⊆ vpJassume 𝜓 K(𝜑))
                             iff    (ℓ ⊆ 𝜓 → 𝜑)                                                         (Def. vp)
                             iff ℓ ∩ 𝜓 ⊆ 𝜑                                                    (Def. implication)
                             iff    (ℓ ⊆ 𝜑) [ℓ ↦→ ℓ ∩ 𝜓 ]                                         (Def. substBy)
                             iff vcJℓ := ℓ ∩ 𝜓 K((ℓ ⊆ 𝜑))                                               (Def. vc)
                             iff vcJmonitor(assume 𝜓 )K((ℓ ⊆ 𝜑))                                  (Def. monitor)
      - Case 𝑆 = coassert 𝜓 .
                      (ℓ ⊆ vpJcoassert 𝜓 K(𝜑))
                            iff     (ℓ ⊆ 𝜓 ∪ 𝜑)                                                         (Def. vp)
                            iff ℓ \ 𝜓 ⊆ 𝜑                                                        (Set difference)
                            iff     (ℓ ⊆ 𝜑) [ℓ ↦→ ℓ \ 𝜓 ]                                         (Def. substBy)
                            iff vcJℓ := ℓ \ 𝜓 K((ℓ ⊆ 𝜑))                                                (Def. vc)
                            iff vcJmonitor(coassert 𝜓 )K((ℓ ⊆ 𝜑))                                 (Def. monitor)
      - Case 𝑆 = coassume 𝜓 .
                      (ℓ ⊆ vpJcoassume 𝜓 K(𝜑))
                            iff     (ℓ ⊆ 𝜑 \ 𝜓 )                                                        (Def. vp)
                            iff     (ℓ ⊆ Γ \ 𝜓 ) ∧ (ℓ ⊆ 𝜑)
                                           ∞
                                                                                                 (Set difference)
                            iff vcJassert (ℓ ⊆ Γ \ 𝜓 )K((ℓ ⊆ 𝜑))
                                                       ∞
                                                                                                        (Def. vc)
                            iff vcJmonitor(coassume 𝜓 )K((ℓ ⊆ 𝜑))                                 (Def. monitor)
      - Case 𝑆 = validate.
                   (ℓ ⊆ vpJvalidateK(𝜑))
                      iff         (ℓ ⊆ △(𝜑))                                                            (Def. vp)
76                                                                                        Ahrens, Rode, Schröer, and Katoen


                       iff   (ℓ = ∅) ∨ (Γ ∞ ⊆ 𝜑)                                                         (Def. validate)
                       iff   (ℓ = ∅) ∨ (ℓ ⊆ 𝜑) [ℓ ↦→ Γ ]  ∞
                                                                                                            (Def. substBy)
                       iff   (ℓ = ∅) ∨ vcJℓ := Γ ∞ K((ℓ ⊆ 𝜑))                                                     (Def. vc)
                       iff vcJassume (ℓ ≠ ∅)K vcJℓ := Γ K((ℓ ⊆ 𝜑))
                                                                 ∞
                                                                                                                  (Def. vc)
                                                                                  

                       iff vcJassume (ℓ ≠ ∅) # ℓ := Γ ∞ K((ℓ ⊆ 𝜑))                                                (Def. vc)
                       iff   vcJmonitor(validate)K((ℓ ⊆ 𝜑))                                                (Def. monitor)

       - Case 𝑆 = weigh 𝑎.
             (ℓ ⊆ vpJweigh 𝑎K(𝜑))
               iff     (ℓ ⊆ 𝑎 · 𝜑)                                                                               (Def. vp)
               iff     (ℓ ⊆ 𝑎 · Γ ∞ ) ∧ 𝑎 −1 · ℓ ⊆ 𝜑                                                       (Equation (7b))
               iff     (ℓ ⊆ 𝑎 · Γ ) ∧ (ℓ ⊆ 𝜑) [ℓ ↦→ 𝑎
                                   ∞                      −1
                                                               · ℓ]                                         (Def. substBy)
               iff     (ℓ ⊆ 𝑎 · Γ ) ∧ vcJℓ := 𝑎
                                   ∞              −1
                                                       · ℓK((ℓ ⊆ 𝜑))                                              (Def. vc)
               iff     vcJassert (ℓ ⊆ 𝑎 · Γ )K vcJℓ := 𝑎
                                              ∞                  −1
                                                                                                                  (Def. vc)
                                                                                      
                                                                      · ℓK((ℓ ⊆ 𝜑))
               iff     vcJassert (ℓ ⊆ 𝑎 · Γ ) # ℓ := 𝑎
                                              ∞            −1
                                                                · ℓK((ℓ ⊆ 𝜑))                                     (Def. vc)
               iff     vcJmonitor(weigh 𝑎)K((ℓ ⊆ 𝜑))                                                       (Def. monitor)

       - Case 𝑆 = 𝑥 := 𝑒.
                         (ℓ ⊆ vpJ𝑥 := 𝑒K(𝜑))
                             iff   (ℓ ⊆ 𝜑 [𝑥 ↦→ 𝑒])                                                              (Def. vp)
                             iff   (ℓ ⊆ 𝜑) [𝑥 ↦→ 𝑒]                                                            (Freshness)
                             iff vcJ𝑥 := 𝑒K((ℓ ⊆ 𝜑))                                                              (Def. vc)
                             iff vcJmonitor(𝑥 := 𝑒)K((ℓ ⊆ 𝜑))                                              (Def. monitor)

       - Case 𝑆 = 𝑆 1 # 𝑆 2 . Since ℓ is fresh and does not occur in 𝑆 2 or 𝜑, it also does not occur in
         vpJ𝑆 2 K(𝜑).
              (ℓ ⊆ vpJ𝑆 1 # 𝑆 2 K(𝜑))
                 iff    (ℓ ⊆ vpJ𝑆 1 K(vpJ𝑆 2 K(𝜑)))                                                              (Def. vp)
                 iff    vcJmonitor(𝑆 1 )K((ℓ ⊆ vpJ𝑆 2 K(𝜑)))                                                  (I.H. for 𝑆 1 )
                 iff                                                                                          (I.H. for 𝑆 2 )
                                                                              
                        vcJmonitor(𝑆 1 )K vcJmonitor(𝑆 2 )K((ℓ ⊆ 𝜑))
                 iff    vcJmonitor(𝑆 1 ) # monitor(𝑆 2 )K((ℓ ⊆ 𝜑))                                                (Def. vc)
                 iff    vcJmonitor(𝑆 1 # 𝑆 2 )K((ℓ ⊆ 𝜑))                                                   (Def. monitor)

       - Case 𝑆 = havoc 𝑥. This is immediate from the definition of vp, the definition of vc, and the
         fact that monitor(havoc 𝑥) = havoc 𝑥.
       - Case 𝑆 = if (⊓) {𝑆 1 } else {𝑆 2 }. This is immediate from the induction hypotheses and
         (ℓ ⊆ 𝑋 ∩ 𝑌 ) ⇐⇒ (ℓ ⊆ 𝑋 ) ∧ (ℓ ⊆ 𝑌 ).
                                                                                                                          □

     Lemma E.3 (Lax lower-bound translation). Let 𝑆 0 range over the fragment of Theorem E.2. For
        𝑆 ::= 𝑆 0 | if (+) {𝑆 } else {𝑆 } | if (⊔) {𝑆 } else {𝑆 } | cohavoc 𝑥 | covalidate | 𝑆 # 𝑆
Towards a Verification Infrastructure for wGCL                                                                             77


define monitor′ (−) by
                                     monitor′ (𝑆 0 ) = monitor(𝑆 0 )
          monitor′ (if (+) {𝑆 1 } else {𝑆 2 }) = if (+) {monitor′ (𝑆 1 )} else {monitor′ (𝑆 2 )}
          monitor′ (if (⊔) {𝑆 1 } else {𝑆 2 }) = if (⊔) {monitor′ (𝑆 1 )} else {monitor′ (𝑆 2 )}
                          monitor′ (cohavoc 𝑥) = cohavoc 𝑥
                         monitor′ (covalidate) = assert (ℓ ⊆ ∅)
                                 monitor′ (𝑆 1 # 𝑆 2 ) = monitor′ (𝑆 1 ) # monitor′ (𝑆 2 ) .
Then, for every such statement 𝑆 and every language 𝜑,
                                  vcJmonitor′ (𝑆)K((ℓ ⊆ 𝜑)) ⇒ (ℓ ⊆ vpJ𝑆K(𝜑)).
  Proof. The cases from Theorem E.2 are identical. We only show the additional lax cases and
sequencing.
     - Case 𝑆 = if (+) {𝑆 1 } else {𝑆 2 } or 𝑆 = if (⊔) {𝑆 1 } else {𝑆 2 }.
       vcJmonitor′ (𝑆)K((ℓ ⊆ 𝜑))
         iff     vcJmonitor′ (𝑆 1 )K((ℓ ⊆ 𝜑)) ∨ vcJmonitor′ (𝑆 2 )K((ℓ ⊆ 𝜑))                          (Defs. monitor’/vc)
         implies       (ℓ ⊆ vpJ𝑆 1 K(𝜑)) ∨ (ℓ ⊆ vpJ𝑆 2 K(𝜑))                                                           (I.H.)
         implies       (ℓ ⊆ vpJ𝑆 1 K(𝜑) ∪ vpJ𝑆 2 K(𝜑))                                                             (Union)
         iff     (ℓ ⊆ vpJ𝑆K(𝜑))                                                                                   (Def. vp)
      - Case 𝑆 = cohavoc 𝑥.
                      vcJmonitor′ (cohavoc 𝑥)K((ℓ ⊆ 𝜑))
                          iff vcJcohavoc 𝑥K((ℓ ⊆ 𝜑))                                                       (Def. monitor’)
                          iff ∃𝑣 . (ℓ ⊆ 𝜑 [𝑥 ↦→ 𝑣])                                                               (Def. vc)
                                          Ø
                          implies (ℓ ⊆        𝜑 [𝑥 ↦→ 𝑣])                                                        (Witness)
                                               𝑣
                          iff    (ℓ ⊆ vpJcohavoc 𝑥K(𝜑))                                                           (Def. vp)
      - Case 𝑆 = covalidate.
                       vcJmonitor′ (covalidate)K((ℓ ⊆ 𝜑))
                           iff    (ℓ ⊆ ∅) ∧ (ℓ ⊆ 𝜑)                                                   (Defs. monitor’/vc)
                           implies      (ℓ ⊆ ∅)
                           implies      (ℓ ⊆ vpJcovalidateK(𝜑))                                                    (∅ ⊆ 𝑋 )
      - Case 𝑆 = 𝑆 1 # 𝑆 2 . Since ℓ is fresh and does not occur in 𝑆 2 or 𝜑, it also does not occur in
        vpJ𝑆 2 K(𝜑).
          vcJmonitor′ (𝑆 1 # 𝑆 2 )K((ℓ ⊆ 𝜑))
               iff   vcJmonitor′ (𝑆 1 )K vcJmonitor′ (𝑆 2 )K((ℓ ⊆ 𝜑))                                 (Defs. vc/monitor’)
                                                                            

               implies                    ′
                           vcJmonitor (𝑆 1 )K((ℓ ⊆ vpJ𝑆 2 K(𝜑)))                               (I.H. for 𝑆 2 , monotonicity)
               implies     (ℓ ⊆ vpJ𝑆 1 K(vpJ𝑆 2 K(𝜑)))                                                         (I.H. for 𝑆 1 )
               iff   (ℓ ⊆ vpJ𝑆 1 # 𝑆 2 K(𝜑))                                                                      (Def. vp)
                                                                                                                           □
78                                                                         Ahrens, Rode, Schröer, and Katoen


   The left-hand side of Figure 17 shows the modified CAS livelock example 𝐶𝐿𝐹       ′ from Section 6.2,

encoded by Park induction (cf. Section 5.3) in the formal-language instance of wHeyVL, together
with its translated monitor version in the Boolean instance over residual-language predicates
according to Lemma E.3. Because a procedure precondition is implemented as an initial assume
and the monitor translation maps assume to an assignment on ℓ, the figure internalizes the origi-
nal pre/postconditions as explicit wrapper statements rather than translating them through the
procedure header. The schematic branch                  :
                                                𝑗=1 { 𝑖 = 𝑗 } on the left is rendered on the right by the
                                             É𝑁

existential explicit choice cohavoc 𝑖 # coassume ¬? (1 ≤ 𝑖 ≤ 𝑁 ). Here coassume ¬? (1 ≤ 𝑖 ≤ 𝑁 ) keeps
exactly the valid thread indices, since ¬? (𝑏) denotes the Boolean complement of the embedding of 𝑏
and coassume 𝜓 excludes the states satisfying 𝜓 . The lowered procedure verifies. Thus, by sound-
ness of local Park induction (Theorem 5.12) together with Lemma E.3, this implies 𝐼𝑘 ⊆ wlpJ𝐶𝐿𝐹     ′ K(0).

In Caesar, this example still has to be instantiated to a concrete finite nondeterministic choice.
Towards a Verification Infrastructure for wGCL                                                                     79


                             Source                                                Lowered
                           wHeyVLlang                                             wHeyVLbool

            lang proc casLivelock (𝑘 : N)                    bool proc casLivelock (𝑘 : N)
                           -> (𝑖, 𝑣 : N, 𝑙 𝑣 : Lists)                      -> (𝑖, 𝑣 : N, 𝑙 𝑣 : Lists, ℓ : lang)
                pre ⊤                                            pre ⊤
                post ⊤                                           post ⊤
            {                                                {
                assume 𝐼𝑘 #                                      ℓ := ℓ ∩ 𝐼𝑘 #
                assert 𝐼𝑘 #                                      assert (ℓ ⊆ 𝐼𝑘 )#
                havoc 𝑖, 𝑣, 𝑙 𝑣 #                                havoc 𝑖, 𝑣, 𝑙 𝑣 #
                validate#                                        assume (ℓ ≠ ∅) # ℓ := Γ ∞ #
                assume 𝐼𝑘 #                                      ℓ := ℓ ∩ 𝐼𝑘 #
                if ( true ) {                                    if ( true ) {
                   𝑁
                   Ê
                           { 𝑖 := 𝑗 }#                              cohavoc 𝑖 # coassume ¬? (1 ≤ 𝑖 ≤ 𝑁 ) #
                    𝑗=1
                   if ( 𝑙 𝑣 [𝑖] = 𝑣 ) {                             if ( 𝑙 𝑣 [𝑖] = 𝑣 ) {
                     𝑣 := 𝑣 + 1#                                      𝑣 := 𝑣 + 1#
                        weigh 𝑆𝑖 #                                       assert (ℓ ⊆ 𝑆𝑖 · Γ ∞ ) # ℓ := 𝑆𝑖−1 · ℓ#
                        𝑙 𝑣 [𝑖] := 𝑣                                     𝑙 𝑣 [𝑖] := 𝑣
                   } else {                                         } else {
                        weigh 𝐹𝑖                                         assert (ℓ ⊆ 𝐹𝑖 · Γ ∞ ) # ℓ := 𝐹𝑖−1 · ℓ
                   }#                                               }#
                   assert 𝐼𝑘 # assume ? (false)                     assert (ℓ ⊆ 𝐼𝑘 ) # ℓ := ∅
                } else { }#                                      } else { }#
                assert ∅                                         assert (ℓ ⊆ ∅)
            }                                                }

                                                                                
Fig. 17. Modified CAS livelock witness from Section 6.2 for 𝐼𝑘 ≜ [𝑙 𝑣 [𝑘] ≠ 𝑣] · 𝐹𝑘𝜔 and its monitor translation
into the Boolean instance over residual-language predicates, following Lemma E.3. Because assumptions
lower to assignments, the original pre/post are made explicit as wrapper statements, so both procedures use
the trivial outer specification. Here lang denotes languages over Γ ∞ .


E.1.3   Upper-Bound Translation.
   Definition E.4 (Residual-language upper-bound monitor translation). Let ℓ be fresh and range over
languages over Γ ∞ . For
        𝑆 ::= 𝑥 := 𝑒 | assert 𝜓 | assume 𝜓 | coassert 𝜓 | coassume 𝜓 | weigh 𝑎
                | covalidate | if (+) {𝑆 } else {𝑆 } | if (⊔) {𝑆 } else {𝑆 } | cohavoc 𝑥 | 𝑆 # 𝑆
define monitor↑ (−) by
          monitor↑ (if (+) {𝑆 1 } else {𝑆 2 }) = if (⊓) {monitor↑ (𝑆 1 )} else {monitor↑ (𝑆 2 )}
          monitor↑ (if (⊔) {𝑆 1 } else {𝑆 2 }) = if (⊓) {monitor↑ (𝑆 1 )} else {monitor↑ (𝑆 2 )}
80                                                                               Ahrens, Rode, Schröer, and Katoen


                      monitor↑ (cohavoc 𝑥) = havoc 𝑥
                             monitor↑ (𝑆 1 # 𝑆 2 ) = monitor↑ (𝑆 1 ) # monitor↑ (𝑆 2 )
                       monitor↑ (assert 𝜓 ) = ℓ := ℓ ∪ (Γ ∞ \ 𝜓 )
                       monitor↑ (assume 𝜓 ) = assert ((Γ ∞ \ 𝜓 ) ⊆ ℓ)
                    monitor↑ (coassert 𝜓 ) = assert (𝜓 ⊆ ℓ)
                    monitor↑ (coassume 𝜓 ) = ℓ := ℓ ∪ 𝜓
                            monitor↑ (weigh 𝑎) = ℓ := 𝑎 −1 · ℓ
                    monitor↑ (covalidate) = coassert (Γ ∞ ⊆ ℓ) # ℓ := ∅ # covalidate.
It leaves 𝑥 := 𝑒 unchanged.
  Theorem E.5. Assume that ℓ is fresh, i.e., it does not occur in 𝑆 or 𝜑. Then, for every statement 𝑆 in
the fragment above and language 𝜑,
                             (vpJ𝑆K(𝜑) ⊆ ℓ)         iff vcJmonitor↑ (𝑆)K((𝜑 ⊆ ℓ)) .
     Proof. The proof is by structural induction.
       - Case 𝑆 = assert 𝜓 .
                     (vpJassert 𝜓 K(𝜑) ⊆ ℓ)
                       iff     (𝜓 ∩ 𝜑 ⊆ ℓ)                                                              (Def. vp)
                       iff 𝜑 ⊆ ℓ ∪ (Γ \ 𝜓 ) ∞
                                                                                                  (Set difference)
                       iff                             ∞
                               (𝜑 ⊆ ℓ) [ℓ ↦→ ℓ ∪ (Γ \ 𝜓 )]                                         (Def. substBy)
                       iff vcJℓ := ℓ ∪ (Γ \ 𝜓 )K((𝜑 ⊆ ℓ))
                                                ∞
                                                                                                         (Def. vc)
                       iff vcJmonitor (assert 𝜓 )K((𝜑 ⊆ ℓ))
                                            ↑
                                                                                                  (Def. monitor)
       - Case 𝑆 = assume 𝜓 .
                    (vpJassume 𝜓 K(𝜑) ⊆ ℓ)
                      iff     (𝜓 → 𝜑 ⊆ ℓ)                                                               (Def. vp)
                      iff     (Γ ∞ \ 𝜓 ) ⊆ ℓ ∧ (𝜑 ⊆ ℓ)                                            (Set difference)
                      iff vcJassert ((Γ ∞ \ 𝜓 ) ⊆ ℓ)K((𝜑 ⊆ ℓ))                                           (Def. vc)
                      iff vcJmonitor↑ (assume 𝜓 )K((𝜑 ⊆ ℓ))                                       (Def. monitor)
       - Case 𝑆 = coassert 𝜓 .
                    (vpJcoassert 𝜓 K(𝜑) ⊆ ℓ)
                      iff     (𝜓 ∪ 𝜑 ⊆ ℓ)                                                               (Def. vp)
                      iff 𝜓 ⊆ ℓ ∧ (𝜑 ⊆ ℓ)                                                                (Union)
                      iff vcJassert (𝜓 ⊆ ℓ)K((𝜑 ⊆ ℓ))                                                    (Def. vc)
                      iff vcJmonitor (coassert 𝜓 )K((𝜑 ⊆ ℓ))
                                            ↑
                                                                                                  (Def. monitor)
       - Case 𝑆 = coassume 𝜓 .
                    (vpJcoassume 𝜓 K(𝜑) ⊆ ℓ)
                      iff     (𝜑 \ 𝜓 ⊆ ℓ)                                                               (Def. vp)
Towards a Verification Infrastructure for wGCL                                                                    81


                           iff 𝜑 ⊆ ℓ ∪ 𝜓                                                             (Set difference)
                           iff     (𝜑 ⊆ ℓ) [ℓ ↦→ ℓ ∪ 𝜓 ]                                              (Def. substBy)
                           iff vcJℓ := ℓ ∪ 𝜓 K((𝜑 ⊆ ℓ))                                                     (Def. vc)
                           iff vcJmonitor (coassume 𝜓 )K((𝜑 ⊆ ℓ))
                                                 ↑
                                                                                                     (Def. monitor)
      - Case 𝑆 = weigh 𝑎.
                           (vpJweigh 𝑎K(𝜑) ⊆ ℓ)
                             iff    (𝑎 · 𝜑 ⊆ ℓ)                                                            (Def. vp)
                             iff 𝜑 ⊆ 𝑎     −1
                                                ·ℓ                                                   (Equation (7a))
                             iff    (𝜑 ⊆ ℓ) [ℓ ↦→ 𝑎      −1
                                                              · ℓ]                                    (Def. substBy)
                             iff vcJℓ := 𝑎 −1 · ℓK((𝜑 ⊆ ℓ))                                                 (Def. vc)
                             iff vcJmonitor (weigh 𝑎)K((𝜑 ⊆ ℓ))
                                                     ↑
                                                                                                     (Def. monitor)
      - Case 𝑆 = covalidate.
         (vpJcovalidateK(𝜑) ⊆ ℓ)
            iff   (▽(𝜑) ⊆ ℓ)                                                                               (Def. vp)
            iff   (Γ   ∞
                           ⊆ ℓ) ∨ ▽(((𝜑 ⊆ ℓ) [ℓ ↦→ ∅]))                                           (Def. covalidate)
            iff   (Γ   ∞
                           ⊆ ℓ) ∨ vcJcovalidateK((𝜑 ⊆ ℓ) [ℓ ↦→ ∅])                                          (Def. vc)
            iff                          ∞
                                                                                                            (Def. vc)
                                                                                             
                  vcJcoassert (Γ ⊆ ℓ)K vcJcovalidateK((𝜑 ⊆ ℓ) [ℓ ↦→ ∅])
            iff vcJcoassert (Γ ⊆ ℓ)K vcJℓ := ∅ # covalidateK((𝜑 ⊆ ℓ))
                                         ∞
                                                                                                            (Def. vc)
                                                                      

            iff vcJcoassert (Γ ∞ ⊆ ℓ) # ℓ := ∅ # covalidateK((𝜑 ⊆ ℓ))                                       (Def. vc)
            iff   vcJmonitor↑ (covalidate)K((𝜑 ⊆ ℓ))                                                 (Def. monitor)
      - Case 𝑆 = if (+) {𝑆 1 } else {𝑆 2 } or 𝑆 = if (⊔) {𝑆 1 } else {𝑆 2 }. This is immediate from the
        induction hypotheses and (𝑋 ∪ 𝑌 ⊆ ℓ) ⇐⇒ (𝑋 ⊆ ℓ) ∧ (𝑌 ⊆ ℓ).
      - Case 𝑆 = cohavoc 𝑥. This is immediate from the definitions and ( 𝑣 𝑋 𝑣 ⊆ ℓ) ⇐⇒
                                                                                      Ð
        ∀𝑣. (𝑋 𝑣 ⊆ ℓ).
      - Case 𝑆 = 𝑥 := 𝑒. This follows exactly as in the proof of Theorem E.2, since the translation
        leaves 𝑥 := 𝑒 unchanged.
      - Case 𝑆 = 𝑆 1 # 𝑆 2 . This follows exactly as in the proof of Theorem E.2, using sequential
        composition and the induction hypotheses.
                                                                                                      □
   Lemma E.6 (Lax upper-bound translation). Let 𝑆 0 range over the fragment of Theorem E.5. For
                           𝑆 ::= 𝑆 0 | if (⊓) {𝑆 } else {𝑆 } | havoc 𝑥 | validate | 𝑆 # 𝑆
                  ↑′
define monitor (−) by
                                     monitor↑′ (𝑆 0 ) = monitor↑ (𝑆 0 )
        monitor↑′ (if (⊓) {𝑆 1 } else {𝑆 2 }) = if (⊔) {monitor↑′ (𝑆 1 )} else {monitor↑′ (𝑆 2 )}
                             monitor↑′ (havoc 𝑥) = cohavoc 𝑥
                           monitor↑′ (validate) = assert (Γ ∞ ⊆ ℓ)
                                 monitor↑′ (𝑆 1 # 𝑆 2 ) = monitor↑′ (𝑆 1 ) # monitor↑′ (𝑆 2 ) .
82                                                                           Ahrens, Rode, Schröer, and Katoen


Then, for every such statement 𝑆 and every language 𝜑,
                                vcJmonitor↑′ (𝑆)K((𝜑 ⊆ ℓ)) ⇒ (vpJ𝑆K(𝜑) ⊆ ℓ).
  Proof. The cases from Theorem E.5 are identical. We only show the additional lax cases and
sequencing.
      - Case 𝑆 = if (⊓) {𝑆 1 } else {𝑆 2 }.
      vcJmonitor↑′ (𝑆)K((𝜑 ⊆ ℓ))
        iff    vcJmonitor↑′ (𝑆 1 )K((𝜑 ⊆ ℓ)) ∨ vcJmonitor↑′ (𝑆 2 )K((𝜑 ⊆ ℓ))            (Defs. monitor↑′ /vc)
        implies       (vpJ𝑆 1 K(𝜑) ⊆ ℓ) ∨ (vpJ𝑆 2 K(𝜑) ⊆ ℓ)                                               (I.H.)
        implies       (vpJ𝑆 1 K(𝜑) ∩ vpJ𝑆 2 K(𝜑) ⊆ ℓ)                                          (Intersection)
        iff    (vpJ𝑆K(𝜑) ⊆ ℓ)                                                                        (Def. vp)

      - Case 𝑆 = havoc 𝑥.
                      vcJmonitor↑′ (havoc 𝑥)K((𝜑 ⊆ ℓ))
                        iff vcJcohavoc 𝑥K((𝜑 ⊆ ℓ))                                           (Def. monitor↑′ )
                        iff ∃𝑣 . (𝜑 [𝑥 ↦→ 𝑣] ⊆ ℓ)                                                    (Def. vc)
                                    Ù
                        implies ( 𝜑 [𝑥 ↦→ 𝑣] ⊆ ℓ)                                                   (Witness)
                                      𝑣
                        iff    (vpJhavoc 𝑥K(𝜑) ⊆ ℓ)                                                  (Def. vp)

      - Case 𝑆 = validate.
                      vcJmonitor↑′ (validate)K((𝜑 ⊆ ℓ))
                         iff   (Γ ∞ ⊆ ℓ) ∧ (𝜑 ⊆ ℓ)                                      (Defs. monitor↑′ /vc)
                         implies    Γ∞ ⊆ ℓ
                         implies    (vpJvalidateK(𝜑) ⊆ ℓ)                          (vpJvalidateK(𝜑) ⊆ Γ ∞ )

      - Case 𝑆 = 𝑆 1 # 𝑆 2 . Since ℓ is fresh and does not occur in 𝑆 2 or 𝜑, it also does not occur in
        vpJ𝑆 2 K(𝜑).
         vcJmonitor↑′ (𝑆 1 # 𝑆 2 )K((𝜑 ⊆ ℓ))
              iff   vcJmonitor↑′ (𝑆 1 )K vcJmonitor↑′ (𝑆 2 )K((𝜑 ⊆ ℓ))                  (Defs. vc/monitor↑′ )
                                                                         

              implies    vcJmonitor↑′ (𝑆 1 )K((vpJ𝑆 2 K(𝜑) ⊆ ℓ))                  (I.H. for 𝑆 2 , monotonicity)
              implies    (vpJ𝑆 1 K(vpJ𝑆 2 K(𝜑)) ⊆ ℓ)                                              (I.H. for 𝑆 1 )
              iff   (vpJ𝑆 1 # 𝑆 2 K(𝜑) ⊆ ℓ)                                                          (Def. vp)

                                                                                                              □

E.2   Tropical Translation
The tropical monoid-module Wtrop has weights in N∞ , with ⊕ = min and scalar multiplication +.
We embed weights into R∞  ≥0 by inclusion, so if (+) {𝑆 1 } else {𝑆 2 } maps to demonic choice and
weigh 𝑐 maps to reward 𝑐. A source lower-bound check maps to a target upper-bound check, hence
source procedures map to target coprocedures. The verification statements map as in the definition
below: assert, assume, havoc, and validate map to their co variants, and conversely.
Towards a Verification Infrastructure for wGCL                                                            83


   Definition E.7 (Tropical translation). Define a translation
                                   trop(−) : wHeyVLtrop → wHeyVLprob
recursively by
                                      trop(𝑥 := 𝑒) = 𝑥 := 𝑒
                                   trop(weigh 𝑐) = reward 𝑐
                 trop(if (+) {𝑆 1 } else {𝑆 2 }) = if (⊓) {trop(𝑆 1 )} else {trop(𝑆 2 )}
                                     trop(𝑆 1 # 𝑆 2 ) = trop(𝑆 1 ) # trop(𝑆 2 )
                 trop(if (⊓) {𝑆 1 } else {𝑆 2 }) = if (⊔) {trop(𝑆 1 )} else {trop(𝑆 2 )}
                 trop(if (⊔) {𝑆 1 } else {𝑆 2 }) = if (⊓) {trop(𝑆 1 )} else {trop(𝑆 2 )}
                                 trop(assert 𝜓 ) = coassert 𝜓b
                                 trop(assume 𝜓 ) = coassume 𝜓b
                              trop(coassert 𝜓 ) = assert 𝜓b
                              trop(coassume 𝜓 ) = assume 𝜓b
                                   trop(havoc 𝑥) = cohavoc 𝑥
                                trop(cohavoc 𝑥) = havoc 𝑥
                                 trop(validate) = covalidate
                              trop(covalidate) = validate.

On the right-hand side, each weight 𝑐 ∈ N∞ is read as an element of R∞  ≥0 . For formulae, 𝜓 embeds
                                                                                           b
constants pointwise, swaps ⊓ with ⊔, swaps → with ←, and swaps quantified infima with suprema.
In particular, Boolean embeddings are dualized as ?d
                                                   (𝑏) = ? (¬𝑏). Any derived statement is translated
after expanding it into this language.
   Theorem E.8. For every statement 𝑆 of wHeyVLtrop , every postweighting 𝑟 : Σ → N∞ , and every
state 𝜎 ∈ Σ,
                             vpJtrop(𝑆)K(b𝑟 ) (𝜎) = vctrop
                                                          (𝑆) (𝑟 ) (𝜎).
   Proof. We prove the claim by structural induction on 𝑆.
   Semiring-specific cases.
                  vctrop (if (+)
                                {𝑆 1 } else {𝑆 2 }) (𝑟 ) (𝜎)
                                                                       
                   = min vctrop
                               (𝑆 1 ) (𝑟 ) (𝜎), vctrop
                                                       (𝑆 2 ) (𝑟 ) (𝜎)                        (Def. vctrop )
                  = vpJtrop(𝑆 1 )K(b
                                   𝑟 ) (𝜎) ⊓ vpJtrop(𝑆 2 )K(b
                                                            𝑟 ) (𝜎)               (I.H., target meet is min)
                  = vpJif (⊓) {trop(𝑆 1 )} else {trop(𝑆 2 )}K(b
                                                              𝑟 ) (𝜎)                              (Def. vp)
                  = vpJtrop(if (+) {𝑆 1 } else {𝑆 2 })K(b
                                                        𝑟 ) (𝜎)                          (Def. translation)
For 𝑆 = weigh 𝑐, we calculate
                                                 (weigh 𝑐) (𝑟 ) (𝜎)
                                          vctrop 
                                           = 𝑐 + 𝑟 (𝜎)                                         (Def. vctrop )
                                                          𝑟 ) (𝜎)
                                           = vpJreward 𝑐K(b                                        (Def. vp)
                                                               𝑟 ) (𝜎)
                                           = vpJtrop(weigh 𝑐)K(b                         (Def. translation.)
84                                                                                 Ahrens, Rode, Schröer, and Katoen


                         Source                                                  Lowered
                       wHeyVLtrop                                               wHeyVLprob

       trop proc skiRental (𝑛 0 : N, 𝑐 𝐵 : N)             prob coproc skiRental (𝑛 0 : N, 𝑐 𝐵 : N)
                  -> (𝑛 : N)                                         -> (𝑛 : N)
            pre 𝐼 (𝑛 0 )                                           𝐼 (𝑛 0 )
                                                               pre b
            post 0                                             post 0
       {                                                  {
            𝑛 := 𝑛 0 # assert 𝐼 (𝑛)#
                                                               𝑛 := 𝑛 0 # coassert b
                                                                                   𝐼 (𝑛)#
            havoc 𝑛 # validate # assume 𝐼 (𝑛)#
                                                                                                 𝐼 (𝑛)#
                                                               cohavoc 𝑛 # covalidate # coassume b
            if ( 𝑛 > 0 ) {
                                                               if ( 𝑛 > 0 ) {
                 𝑛 := 𝑛 − 1#
                                                                    𝑛 := 𝑛 − 1#
                  if (+) {
                                                                     if (⊓) {
                           ⊗1
                                                                              reward 1
                  } else {
                                                                     } else {
                           ⊗ 𝑐 𝐵 # 𝑛 := 0
                                                                              reward 𝑐 𝐵 # 𝑛 := 0
                  }#
                                                                     }#
                  assert 𝐼 (𝑛) # assume ? (false)
                                                                              𝐼 (𝑛) # coassume ? (true)
                                                                     coassert b
            } else { }
                                                               } else { }
       }
                                                          }

Fig. 18. Tropical ski-rental lower-bound proof and its translation to the R∞    ≥0 instance according to Defini-
tion E.7. The source procedure is translated to a target coprocedure, so Caesar checks the source lower bound
as a target upper bound. Here 𝐼 (𝑛) ≜ offlineCost (𝑛, 𝑐 𝐵 ) and b
                                                                𝐼 is its embedded target formula.


  Remaining cases. Sequential composition and assignment follow from the induction hypotheses
and substitution commuting with b
                                −. The remaining cases use the same equations for ⊓/⊔, → /←,
quantified infima/suprema, and validation/covalidation.                                    □
     Figure 18 shows the tropical ski-rental example and its translation.

E.3     Clearance Translation
The clearance semiring Sclear = ({P, C, S, TS}, min, max, TS, P) uses levels P < C < S < TS. We
embed these levels into ordinary R∞
                                  ≥0 by

                                    P = 0,
                                    b          b = 1,
                                               C           S = 2,
                                                           b              c = ∞.
                                                                          TS
Thus the top clearance level TS maps to the top element ∞ of the R∞
                                                                  ≥0 instance. Under this embedding,
if (+) {𝑆 1 } else {𝑆 2 } maps to demonic choice and weigh 𝑐 maps to coassert b   𝑐:
                                vpJcoassert b   𝑟 ) (𝜎) = b
                                            𝑐 K(b            𝑟 (𝜎) = max(𝑐,
                                                          𝑐 ⊔b             𝑟 (𝜎)).
A source lower-bound check maps to a target upper-bound check, hence source procedures map
to target coprocedures. Dually, a source upper-bound check maps to a target lower-bound check,
Towards a Verification Infrastructure for wGCL                                                            85


hence source coprocedures map to target procedures. The verification statements map as in the
definition below: assert, assume, havoc, and validate map to their co variants, and conversely.
   Definition E.9 (Clearance translation). Define a translation
                                 clear(−) : wHeyVLclear → wHeyVLprob
recursively by
                                   clear(𝑥 := 𝑒) = 𝑥 := 𝑒
               clear(if (+) {𝑆 1 } else {𝑆 2 }) = if (⊓) {clear(𝑆 1 )} else {clear(𝑆 2 )}
                                clear(weigh 𝑐) = coassert b
                                                          𝑐
                                  clear(𝑆 1 # 𝑆 2 ) = clear(𝑆 1 ) # clear(𝑆 2 )
               clear(if (⊓) {𝑆 1 } else {𝑆 2 }) = if (⊔) {clear(𝑆 1 )} else {clear(𝑆 2 )}
               clear(if (⊔) {𝑆 1 } else {𝑆 2 }) = if (⊓) {clear(𝑆 1 )} else {clear(𝑆 2 )}
                              clear(assert 𝜓 ) = coassert 𝜓b
                              clear(assume 𝜓 ) = coassume 𝜓b
                           clear(coassert 𝜓 ) = assert 𝜓b
                           clear(coassume 𝜓 ) = assume 𝜓b
                                clear(havoc 𝑥) = cohavoc 𝑥
                             clear(cohavoc 𝑥) = havoc 𝑥
                              clear(validate) = covalidate
                           clear(covalidate) = validate.
On the right-hand side, clearance constants and formulae are read via the embedding above into R∞≥0 .
For formulae, 𝜓b embeds constants pointwise, swaps ⊓ with ⊔, swaps → with ←, and swaps
quantified infima with suprema. In particular, Boolean embeddings are dualized as ?d   (𝑏) = ? (¬𝑏).
Any derived statement is translated after expanding it into this language.
  Theorem E.10. For every statement 𝑆 of wHeyVLclear , every clearance postweighting 𝑟 : Σ →
{P, C, S, TS}, and every state 𝜎 ∈ Σ,
                                               𝑟 ) (𝜎) = vcclear
                                  vpJclear(𝑆)K(b                (𝑆) (𝑟 ) (𝜎).
   Proof. We prove the claim by structural induction on 𝑆.
   Semiring-specific cases. For 𝑆 = if (+) {𝑆 1 } else {𝑆 2 }, we calculate
                vcclear (if (+)
                               {𝑆 1 } else {𝑆 2 }) (𝑟 ) (𝜎)
                                                                      
                 = min vcclear
                              (𝑆 1 ) (𝑟 ) (𝜎), vcclear
                                                       (𝑆 2 ) (𝑟 )(𝜎)                        (Def. vcclear )
                 = vpJclear(𝑆 1 )K(b
                                   𝑟 ) (𝜎) ⊓ vpJclear(𝑆 2 )K(b
                                                             𝑟 ) (𝜎)              (I.H., target meet is min)
                 = vpJif (⊓) {clear(𝑆 1 )} else {clear(𝑆 2 )}K(b
                                                               𝑟 ) (𝜎)                             (Def. vp)
                 = vpJclear(if (+) {𝑆 1 } else {𝑆 2 })K(b
                                                        𝑟 ) (𝜎)                          (Def. translation.)
   For 𝑆 = weigh 𝑐, we calculate
                                               (weigh 𝑐) (𝑟 ) (𝜎)
                                        vcclear
                                         = max(𝑐,
                                                 𝑟 (𝜎))                                      (Def. vcclear )
86                                                                                Ahrens, Rode, Schröer, and Katoen


                             Source                                             Lowered
                           wHeyVLclear                                         wHeyVLprob

clear coproc networkSecurity (𝑛 0 : N)                      prob proc networkSecurity (𝑛 0 : N)
              -> (𝑛 : N)                                                  -> (𝑛 : N)
        pre 𝐼 (𝑛 0 )                                                 𝐼 (𝑛 0 )
                                                                 pre b
        post 𝑃                                                   post 0
{                                                            {
        𝑛 := 𝑛 0 # coassert 𝐼 (𝑛)#
                                                                 𝑛 := 𝑛 0 # assert b
                                                                                   𝐼 (𝑛)#
        cohavoc 𝑛 # covalidate # coassume 𝐼 (𝑛)#
                                                                                             𝐼 (𝑛)#
                                                                 havoc 𝑛 # validate # assume b
        if ( 𝑛 > 0 ) {
                                                                 if ( 𝑛 > 0 ) {
             𝑛 := 𝑛 − 1#
                                                                      𝑛 := 𝑛 − 1#
              if (+) {
                                                                          if (⊓) {
                       ⊗𝑆
                                                                                  coassert 2
              } else {
                                                                          } else {
                       if ( 𝑛 = 0 ) {
                                                                                  if ( 𝑛 = 0 ) {
                             ⊗𝐶
                                                                                       coassert 1
                       } else {
                                                                                  } else {
                             ⊗𝑇𝑆
                                                                                       coassert ∞
                       }
                                                                                  }
              }#
                                                                          }#
              coassert 𝐼 (𝑛) # coassume ? (true)
                                                                                 𝐼 (𝑛) # assume ? (false)
                                                                          assert b
        } else { }
                                                                     } else { }
}
                                                             }

Fig. 19. Network-security example from Section 6.1 and its translation to the R∞    ≥0 instance according to
Definition E.9. The source coprocedure is translated to a target procedure, so Caesar checks the source upper
bound as a target lower bound under the order-reversing embedding. On the right, we use the embedding
P = 0, C
b      b = 1, b
              S = 2, and TS
                         c = ∞. Here 𝐼 (𝑛) ≜ [𝑛 = 0] ⊗ 𝑃 ⊕ [𝑛 = 1] ⊗ 𝐶 ⊕ [𝑛 ≥ 2] ⊗ 𝑆.



                                          𝑐 ⊔b
                                         =b  𝑟 (𝜎)                                                 (definition of b
                                                                                                                  −)
                                         = vpJcoassert b   𝑟 ) (𝜎)
                                                       𝑐 K(b                                              (Def. vp)
                                                              𝑟 ) (𝜎)
                                         = vpJclear(weigh 𝑐)K(b                                 (Def. translation.)

  Remaining cases. Sequential composition and assignment follow from the induction hypotheses
and substitution commuting with b
                                −. The remaining cases use the same equations for ⊓/⊔, → /←,
quantified infima/suprema, and validation/covalidation.                                    □

     Figure 19 shows the network-security example and its translation.
Towards a Verification Infrastructure for wGCL                                                      87


E.4    Why-Semiring Translation
Let 𝐴 be a finite set of provenance atoms. The carrier of the Why semiring is pDNF(𝐴). Source
assertions therefore have type 𝐻 : Σ → pDNF(𝐴).
   To lower into Boolean wHeyVL, we add one fresh Boolean variable 𝑝𝑎 for each provenance atom
𝑎 ∈ 𝐴, and write bΣ ≜ Σ × (𝐴 → {false, true}) for the extended target state space. An extended state
is written b
           𝜎 = (𝜎, 𝜌), where 𝜌 (𝑎) is the value of 𝑝𝑎 .
   For a Why formula 𝑊 ∈ pDNF(𝐴), define bool(𝑊 ) to be the Boolean assertion on b        Σ obtained by
replacing each atom 𝑎 with 𝑝𝑎 , i.e., bool(𝑊 ) (𝜎, 𝜌) ≜ eval𝜌 (𝑊 ). For assertions 𝐻 : Σ → pDNF(𝐴),
define bool(𝐻 ) (𝜎, 𝜌) ≜ eval𝜌 (𝐻 (𝜎)). The target verification calculus is still the ordinary Boolean
calculus vcbool , now interpreted over assertions on b   Σ. For source wHeyVLwhy programs in this
fragment, weigh 𝑊 with 𝑊 ∈ pDNF(𝐴) maps the postweight 𝐻 to 𝜎 ↦→ 𝑊 ∧ 𝐻 (𝜎), and weighted
choice combines branches by disjunction. The pointwise Booleanization below preserves finite
conjunctions and disjunctions of provenance formulas. It does not, in general, preserve Heyting
implication, coimplication, validity, or covalidity. Thus, arbitrary assume −, coassume −, validate,
and covalidate are not part of the structural Why lowering theorem. The special fragment
validate # assume 𝑃, which is used in the proof rules, is still exact. For Why assertions 𝑃, 𝐻 :
Σ → pDNF(𝐴), the original Why-wHeyVL source validates the implication 𝑃 (𝜎) →pDNF 𝐻 (𝜎),
and therefore only checks whether this value is ⊤. In a Heyting algebra this is equivalent to an
order check, and for pDNF(𝐴) the order is entailment of the represented predicates:
               𝑃 (𝜎) →pDNF 𝐻 (𝜎) = ⊤ ⇐⇒ 𝑃 (𝜎) ⊑ 𝐻 (𝜎)
                                              ⇐⇒ ∀𝜌 : 𝐴 → B. eval𝜌 (𝑃 (𝜎)) ⇒ eval𝜌 (𝐻 (𝜎)) .
Thus, Boolean implication is used only for this entailment check, not to represent the Why implica-
tion itself.
  Definition E.11 (Why-semiring translation). Fix an enumeration 𝐴 = {𝑎 1, . . . , 𝑎𝑛 }. On the sup-
ported fragment, the statement translation tr : wHeyVLwhy → wHeyVLbool over b           Σ is defined
by
                      tr(weigh 𝑊 ) = assert bool(𝑊 ),
       tr(if (+) {𝑆 1 } else {𝑆 2 }) = if (⊔) {tr(𝑆 1 )} else {tr(𝑆 2 )},
                          tr(𝑆 1 # 𝑆 2 ) = tr(𝑆 1 ) # tr(𝑆 2 ) ,
                     tr(assert 𝐻 ) = assert bool(𝐻 ),
                  tr(coassert 𝐻 ) = coassert bool(𝐻 ),
                     tr(assume 𝐺) = assume bool(𝐺)                 if 𝐺 (𝜎) ∈ {⊥, ⊤} for all 𝜎,
        tr(validate # assume 𝑃) = havoc 𝑝𝑎1 # · · · # havoc 𝑝𝑎𝑛 # validate # assume bool(𝑃),
       tr(if (⊓) {𝑆 1 } else {𝑆 2 }) = if (⊓) {tr(𝑆 1 )} else {tr(𝑆 2 )},
       tr(if (⊔) {𝑆 1 } else {𝑆 2 }) = if (⊔) {tr(𝑆 1 )} else {tr(𝑆 2 )},
for weights 𝑊 ∈ pDNF(𝐴) and assertions 𝑃, 𝐻, 𝐺 : Σ → pDNF(𝐴). State transformers that leave
the fresh Boolean variables 𝑝𝑎 unchanged are translated unchanged.
  Theorem E.12. For every statement 𝑆 in the supported fragment of Definition E.11 and every Why
assertion 𝐻 : Σ → pDNF(𝐴),
                                                                    
                          vcJtr(𝑆)K(bool(𝐻 )) = bool vcwhy (𝑆) (𝐻 )
                         Σ.
as Boolean assertions on b
88                                                                                     Ahrens, Rode, Schröer, and Katoen


  Proof. We prove the claim pointwise by induction on the syntax of the supported fragment. Fix
an extended state b            Σ. It suffices to show
                  𝜎 = (𝜎, 𝜌) ∈ b
                                            𝜎 ) iff eval𝜌 vcwhy (𝑆) (𝐻 ) (𝜎) .
                                                                            
                     vcJtr(𝑆)K(bool(𝐻 )) (b
       - Case 𝑆 = weigh 𝑊 .
                      vcJtr(weigh 𝑊 )K(bool(𝐻 )) (b
                                                  𝜎)
                           iff   vcJassert bool(𝑊 )K(bool(𝐻 )) (b
                                                                𝜎)                                   (Def. translation)
                           iff bool(𝑊 ) (b𝜎 ) ∧ bool(𝐻 ) (b
                                                          𝜎)                                               (Def. vcbool )
                           iff eval𝜌 (𝑊 ) ∧ eval𝜌 (𝐻 (𝜎))                                        (Def. Booleanization)
                           iff eval𝜌 (𝑊 ∧ 𝐻 (𝜎))                                         (Evaluation of positive DNF)
                           iff                                                                              (Def. vcwhy )
                                                                   
                                 eval𝜌 vcwhy (weigh 𝑊 ) (𝐻 ) (𝜎)
       - Case 𝑆 = if (+) {𝑆 1 } else {𝑆 2 }.
         vcJtr(if (+) {𝑆 1 } else {𝑆 2 })K(bool(𝐻 )) (b
                                                      𝜎)
               iff     vcJif (⊔) {tr(𝑆 1 )} else {tr(𝑆 2 )}K(bool(𝐻 )) (b
                                                                        𝜎)                           (Def. translation)
               iff vcJtr(𝑆 1 )K(bool(𝐻 )) (b 𝜎 ) ∨ vcJtr(𝑆 2 )K(bool(𝐻 )) (b
                                                                           𝜎)                              (Def. vcbool )
               iff eval𝜌 vcwhy (𝑆 1 ) (𝐻 ) (𝜎) ∨ eval𝜌 vcwhy (𝑆 2 ) (𝐻 ) (𝜎)                                       (I.H.)
                                                                            

               iff eval𝜌 vcwhy (𝑆 1 ) (𝐻 ) (𝜎) ∨ vcwhy (𝑆 2 ) (𝐻 ) (𝜎)                   (Evaluation of positive DNF)
                                                                       

               iff eval𝜌 vcwhy (if (+) {𝑆 1 } else {𝑆 2 }) (𝐻 ) (𝜎)                                         (Def. vcwhy )
                                                                        

       - Case 𝑆 = assume 𝐺 with 𝐺 (𝜎) ∈ {⊥, ⊤} for all 𝜎. If 𝐺 (𝜎) = ⊤, then both sides are equivalent
         to eval𝜌 (𝐻 (𝜎)):
     bool(𝐺) (𝜎, 𝜌) ⇒ bool(𝐻 ) (𝜎, 𝜌) iff true ⇒ eval𝜌 (𝐻 (𝜎)) iff eval𝜌 ⊤ →pDNF 𝐻 (𝜎) .
                                                                                                 

         If 𝐺 (𝜎) = ⊥, then both sides are true:
                                                   iff false ⇒ eval𝜌 (𝐻 (𝜎))     iff
                                                                                                            
     bool(𝐺) (𝜎, 𝜌) ⇒ bool(𝐻 ) (𝜎, 𝜌)                                                    eval𝜌 ⊥ →pDNF 𝐻 (𝜎) .
       - Case 𝑆 = validate # assume 𝑃. The added havoc statements range over all valuations of
         the provenance variables, hence
       vcJtr(validate # assume 𝑃)K(bool(𝐻 )) (𝜎, 𝜌)
         iff ∀𝜌 ′ : 𝐴 → {false, true}. bool(𝑃) (𝜎, 𝜌 ′ ) ⇒ bool(𝐻 ) (𝜎, 𝜌 ′ )                 (Def. translation, vcbool )
         iff ∀𝜌 : 𝐴 → {false, true}. eval (𝑃 (𝜎)) ⇒ eval (𝐻 (𝜎))
                       ′
                                                     𝜌′                    𝜌′                    (Def. Booleanization)
         iff 𝑃 (𝜎) ⊑ 𝐻 (𝜎)                                                                 (Semantic order reflection)
         iff 𝑃 (𝜎) →pDNF 𝐻 (𝜎) = ⊤                                                               (Heyting implication)
         iff                                                                                          (Def. validation)
                                                    
                     eval𝜌 △ 𝑃 (𝜎) →pDNF 𝐻 (𝜎)
         iff                                                                                                (Def. vcwhy )
                                                                       
                     eval𝜌 vcwhy (validate # assume 𝑃) (𝐻 ) (𝜎)
         The cases 𝑆 1 # 𝑆 2 , if (⊓) {𝑆 1 } else {𝑆 2 }, if (⊔) {𝑆 1 } else {𝑆 2 }, assert, and coassert are
         immediate from the induction hypotheses and the fact that eval𝜌 (−) preserves conjunction
         and disjunction of positive DNF formulas. The ordinary state-transformer cases := , havoc,
         and cohavoc are immediate when they do not update the fresh Boolean variables 𝑝𝑎 .
                                                                                                                       □
Towards a Verification Infrastructure for wGCL                                                      89


                       Source                                            Translated
                      wHeyVLwhy                                          wHeyVLbool

                                                                                   0     0
     why proc graphReachability ()                   bool proc graphReachability (𝑝𝐴𝐵 , 𝑝𝐴𝐴 : B)
                -> (𝑛𝑜𝑑𝑒 : N)                                   -> (𝑛𝑜𝑑𝑒 : N, 𝑝𝐴𝐵 , 𝑝𝐴𝐴 : B)
          pre 𝑋𝐴𝐵 ∨ 𝑋𝐴𝐴                                         0     0
                                                           pre 𝑝𝐴𝐵 ∨ 𝑝𝐴𝐴
          post ⊤                                           post ⊤
     {                                               {
          𝑛𝑜𝑑𝑒 := 0 # assert 𝐼 #                                              0
                                                          𝑛𝑜𝑑𝑒 := 0 # 𝑝𝐴𝐵 := 𝑝𝐴𝐵           0
                                                                                 # 𝑝𝐴𝐴 := 𝑝𝐴𝐴 #
          havoc 𝑛𝑜𝑑𝑒 # validate # assume 𝐼 #               assert 𝐼 bool #
          if ( 𝑛𝑜𝑑𝑒 ≠ 1 ) {                                havoc 𝑛𝑜𝑑𝑒 # havoc 𝑝𝐴𝐵 , 𝑝𝐴𝐴 #
                if (+) {                                   validate # assume 𝐼 bool #
                        𝑛𝑜𝑑𝑒 := 1 # ⊗ 𝑋𝐴𝐵                  if ( 𝑛𝑜𝑑𝑒 ≠ 1 ) {
                } else {                                        if (⊔) {
                        𝑛𝑜𝑑𝑒 := 0 # ⊗ 𝑋𝐴𝐴                               𝑛𝑜𝑑𝑒 := 1 # assert 𝑝𝐴𝐵
                }#                                              } else {
                assert 𝐼 # assume ? (false)                             𝑛𝑜𝑑𝑒 := 0 # assert 𝑝𝐴𝐴
           } else { }                                           }#
     }                                                          assert 𝐼 bool # assume ? (false)
                                                           } else { }
                                                     }

Fig. 20. Graph-reachability program 𝐶𝐺𝑅 from Figure 22 and its lowering to the Boolean instance on the
extended state space. The provenance atoms 𝑋𝐴𝐵 and 𝑋𝐴𝐴 become mutable Boolean variables 𝑝𝐴𝐵 and
                                         0 and 𝑝 0 . We encode the two nodes as 0 and 1, and write 𝐼 ≜
𝑝𝐴𝐴 , initialized from read-only inputs 𝑝𝐴𝐵       𝐴𝐴
[𝑛𝑜𝑑𝑒 = 1] ⊤ ∨ [𝑛𝑜𝑑𝑒 ≠ 1] (𝑋𝐴𝐵 ∨ 𝑋𝐴𝐴 ) and 𝐼 bool ≜ bool(𝐼 ) = [𝑛𝑜𝑑𝑒 = 1] ⊤ ∨ [𝑛𝑜𝑑𝑒 ≠ 1] (𝑝𝐴𝐵 ∨ 𝑝𝐴𝐴 ).


   Figure 20 shows the graph-reachability example and its translation. The positive commands,
crisp guard assumptions, and the Park-induction check are all covered by Definition E.11 and theo-
rem E.12.
90                                                                                 Ahrens, Rode, Schröer, and Katoen


                           Source                                                Translated
                          wHeyVLwhy                                              wHeyVLbool

     why proc graphReachability ()                       bool proc graphReachability (𝑝 10, 𝑝 20, 𝑝 30, 𝑝 40 : B)
              -> (𝑒 : N)                                             -> (𝑒 : N, 𝑝 1, 𝑝 2, 𝑝 3, 𝑝 4 : B)
         pre 𝑋 1 ∧ 𝑋 2 ∧ 𝑋 3 ∧ 𝑋 4                            pre 𝑝 10 ∧ 𝑝 20 ∧ 𝑝 30 ∧ 𝑝 40
         post ⊤                                               post ⊤
     {                                                   {
         ⊗ 𝑋 4 # 𝑒 := 4 # assert 𝐼 #
                                                              𝑝 1 := 𝑝 10 # 𝑝 2 := 𝑝 20 # 𝑝 3 := 𝑝 30 # 𝑝 4 := 𝑝 40 #
         havoc 𝑒 # validate # assume 𝐼 #
                                                              assert 𝑝 4 # 𝑒 := 4 # assert 𝐼𝑏𝑜𝑜𝑙 #
         if ( 𝑒 ≠ 1 ) {                                       havoc 𝑒 # havoc 𝑝 1, 𝑝 2, 𝑝 3, 𝑝 4 #
              if ( 𝑒 = 2 ) {                                  validate # assume 𝐼𝑏𝑜𝑜𝑙 #
                      if (+) {                                if ( 𝑒 ≠ 1 ) {
                            ⊗ 𝑋 3 # 𝑒 := 3                           if ( 𝑒 = 2 ) {
                      } else {                                              if (⊔) {
                            ⊗ 𝑋 1 # 𝑒 := 1                                         assert 𝑝 3 # 𝑒 := 3
                      }#                                                    } else {
              } else {                                                             assert 𝑝 1 # 𝑒 := 1
                      if ( 𝑒 = 3 ) {                                        }#
                            if (+) {                                 } else {
                                 ⊗ 𝑋 2 # 𝑒 := 2                             if ( 𝑒 = 3 ) {
                            } else {                                               if (⊔) {
                                 ⊗ 𝑋 1 # 𝑒 := 1                                           assert 𝑝 2 # 𝑒 := 2
                            }#                                                     } else {
                      } else {                                                            assert 𝑝 1 # 𝑒 := 1
                            if ( (𝑒 = 4) ∨ (𝑒 = 5) ) {                             }#
                                 ⊗ 𝑋 2 # 𝑒 := 2                             } else {
                            } else {                                               if ( (𝑒 = 4) ∨ (𝑒 = 5) ) {
                                 ⊗ 𝑋 3 # 𝑒 := 3                                         assert 𝑝 2 # 𝑒 := 2
                            }                                                      } else {
                      }                                                                   assert 𝑝 3 # 𝑒 := 3
              }                                                                    }
              assert 𝐼 # assume ? (false)                                   }
         } else { }                                                  }
     }                                                               assert 𝐼𝑏𝑜𝑜𝑙 # assume ? (false)
                                                              } else { }
                                                         }

Fig. 21. Employee graph-reachability program from Section 6.4 and its lowering to the Boolean instance on
the extended state space. The provenance atoms 𝑋𝑖 become mutable Boolean variables 𝑝𝑖 , initialized from
read-only inputs 𝑝𝑖0 . We write 𝐼 bool ≜ bool(𝐼 ).
Towards a Verification Infrastructure for wGCL                                                             91


                      wHeyVLprob                                              wHeyVLwhy

  prob coproc queueing (𝑘 0 : N, 𝑒 0 : N, 𝑏 0 : B)              why proc graphReachability ()
               -> (𝑘 : N, 𝑒 : N, 𝑏 : B)                                       -> (𝑛𝑜𝑑𝑒 : N)
      pre 𝑒 0 + 4 · 𝑘 0                                              pre 𝑋𝐴𝐵 ∨ 𝑋𝐴𝐴
      post 𝑒                                                         post ⊤
  {                                                              {
      𝑘 := 𝑘 0 # 𝑒 := 𝑒 0 # 𝑏 := 𝑏 0 #                               𝑛𝑜𝑑𝑒 := 0#

      coassert 𝑒 + 4 · 𝑘 + 16 · [𝑏 ≠ 𝑏 0 ]#                          assert 𝐼 # havoc 𝑛𝑜𝑑𝑒#
      cohavoc 𝑘, 𝑒, 𝑏 # covalidate#                                  validate # assume 𝐼 #
      coassume 𝑒 + 4 · 𝑘 + 16 · [𝑏 ≠ 𝑏 0 ]#                          if ( 𝑛𝑜𝑑𝑒 ≠ 1 ) {
      if ( 𝑘 > 0 ) {                                                   if (+) {
         if (+) { ⊗ 0.8 }                                                𝑛𝑜𝑑𝑒 := 1 # ⊗ 𝑋𝐴𝐵
         else { ⊗ 0.2 #                                                } else {
            if ( 𝑏 ) { 𝑒 := 𝑒 + 4 }                                      𝑛𝑜𝑑𝑒 := 0 # ⊗ 𝑋𝐴𝐴
            else { 𝑒 := 𝑒 + 10 }#                                      }#
            𝑏 := ¬𝑏                                                    assert 𝐼 # assume ? (false)
         } # 𝑘 := 𝑘 − 1#                                             } else { }
         assert 𝑒 + 4 · 𝑘 + 16 · [𝑏 ≠ 𝑏 0 ]                      }

         if ( 𝑘 > 0 ) {
            if (+) { ⊗ 0.8 }
            else { ⊗ 0.2 #
               if ( 𝑏 ) { 𝑒 := 𝑒 + 4 }
               else { 𝑒 := 𝑒 + 10 }#
               𝑏 := ¬𝑏
            } # 𝑘 := 𝑘 − 1#

            coassert 𝑒 + 4 · 𝑘 + 16 · [𝑏 ≠ 𝑏 0 ]#
            coassume ? (true)
         } else { }
      } else { }
  }

Fig. 22. The job scheduling program 𝑞𝑢𝑒𝑢𝑒𝑖𝑛𝑔 uses 𝑘-induction with 𝑘 = 2 to prove wpJ𝐶𝑄 K(𝑒) ⊑ 𝑒 0 + 4 ∗ 𝑘 0 .
The program 𝑔𝑟𝑎𝑝ℎ𝑅𝑒𝑎𝑐ℎ𝑎𝑏𝑖𝑙𝑖𝑡𝑦 uses Park induction to prove wlpJ𝐶𝐺𝑅 K(⊤) ⊒ 𝑋𝐴𝐵 ∨ 𝑋𝐴𝐴 .
92                                                                                Ahrens, Rode, Schröer, and Katoen


                        wHeyVLclear                                            wHeyVLlang

     clear coproc networkSecurity (𝑛 0 : N)                 clear coproc base (ℓ0 : Lists)
                     -> (𝑛 : N)                                             -> (ℓ : Lists)
         pre min{ [𝑛 0 = 0] · P, [𝑛 0 = 1] · C,                 pre 𝐼 (0)
                       [𝑛 0 ≥ 2] · S }   = 𝐼 (𝑛 0 )             post ⊥
         post P                                             { coassert ? (true) }
     {
         𝑛 := 𝑛 0 #                                         clear coproc step (ℓ0 : Lists)
                                                                            -> (ℓ : Lists)
         coassert 𝐼 (𝑛) # cohavoc 𝑛#
                                                                pre 𝐼 (𝑛 + 1)
         covalidate # coassume 𝐼 (𝑛)#
                                                                post ⊥
         if ( 𝑛 > 0 ) {                                     {
           𝑛 := 𝑛 − 1#                                          ℓ := ℓ0 #
            if (+) {
                                                                if ( true ) {
                 ⊗S
                                                                   if (+) { 𝑖 := 1 }
            } else {
                                                                   else {if (+) { 𝑖 := 2 } . . .
                 if ( 𝑛 = 0 ) {
                                                                        . . . else { 𝑖 := 𝑁 } }#
                     ⊗C
                 } else {                                          if ( ℓ [𝑖] = 𝑣 ) {
                     ⊗ TS                                            ⊗ 𝑆𝑖 # 𝑣 := ℓ [𝑖] + 1 # ℓ [𝑖] := 𝑣
                 }                                                 } else {
            }#                                                         ⊗ 𝐹𝑖 # ℓ [𝑖] := 𝑣
                                                                   }
            coassert 𝐼 (𝑛) # coassume ? (true)
         } else { }                                                coassert 𝐼 (𝑛) # coassume ? (true)
     }                                                          } else { }
                                                            }

Fig. 23. The program 𝑛𝑒𝑡𝑤𝑜𝑟𝑘𝑆𝑒𝑐𝑢𝑟𝑖𝑡𝑦 uses Park induction to prove wpJ𝐶𝐴𝐶 K(𝑃) ≥ 𝐼 (𝑛 0 ) with 𝐼 (𝑛) =
min{[𝑛 = 0] · P, [𝑛 = 1] · C, [𝑛 ≥ 2] · S}. The programs 𝑏𝑎𝑠𝑒 and 𝑠𝑡𝑒𝑝 show wlpJ𝐶𝐶𝐴𝑆 K(⊥) ⊑ inf 𝑛∈N 𝐼 (𝑛) via
𝜔-superinvariants.
Towards a Verification Infrastructure for wGCL                                                                93


                                        𝐶𝑄 ∈ wGCLprob             (( 𝑒 + 4 · 𝑘
                                                                  ⊑

                                        while ( 𝑘 > 0 ) {
                                              {
                                                    ⊗ 0.8
                                              } ⊕ {
                                                    ⊗ 0.2 #
                                                    if ( 𝑏 ) {
                                                         𝑒 := 𝑒 + 4
                                                    } else {
                                                         𝑒 := 𝑒 + 10
                                                    }#
                                                    𝑏 := ¬𝑏
                                              }#
                                              𝑘 := 𝑘 − 1#
                                        }
                                        wp
                                            (( 𝑒

                  Fig. 24. The job scheduling program 𝐶𝑄 satisfies wpJ𝐶𝑄 K(𝑒) ⊑ 𝑒 0 + 4 ∗ 𝑘 0 .


F     Theory and Proofs of Section 6: Case Studies
F.1    Probabilities: Queueing Background Jobs
We show that the probability module Wprob over the monoid Mprob is an 𝜔-bicontinuous monoid-
module with Heyting (co-)implications.
  Lemma F.1. The probability module Wprob = (R∞
                                              ≥0, +, 0, ·) over the monoid M prob = (R ≥0, ·, 1) is
a monoid-module (see Definition 2.1).
   Proof. We observe that (R ≥0, ·, 1) and (R∞      ≥0, +, 0) are monoids, where the latter is also commuta-
tive due to the addition +. We check the properties of the scalar multiplication · : R ≥0 × R∞       ≥0 → R ≥0 ,
                                                                                                              ∞

(𝑝, 𝑐) ↦→ 𝑝 · 𝑐. It is associative ((𝑝 · 𝑞) · 𝑐 = 𝑝 · (𝑞 · 𝑐)) and distributive (𝑝 · (𝑐 + 𝑑) = 𝑝 · 𝑐 + 𝑝 · 𝑑) for
𝑝, 𝑞 ∈ R ≥0 and 𝑐 ∈ R∞   ≥0 . Furthermore, the neutral element 1 is neutral (1 · 𝑐 = 𝑐) and the neutral
element 0 is annihilating (𝑝 · 0 = 0), hence all properties are satisfied.                                     □
    Lemma F.2. The probability module Wprob over the monoid Mprob is 𝜔-bicontinuous.
   Proof. The natural order is defined as 𝑐 ⊑ 𝑑 if and only if there exists 𝑒 ∈ R∞
                                                                                 ≥0 such that 𝑐 +𝑒 = 𝑑
if and only if 𝑐 ≤ 𝑑 in the usual order of the non-negative reals. Hence, the natural order is a partial
(even total) order with least element 0, greatest element ∞, where suprema and infima of 𝜔-chains
are the usual supremum and infimum in the non-negative reals (since the non-negative reals are
complete, they always exist).
   We show that the scalar multiplication · is 𝜔-bicontinuous in the second argument and assume
that 𝑝 ∈ R ≥0 and (𝑐𝑖 )𝑖 ∈N ⊆ R∞
                               ≥0 is an ascending (descending) 𝜔-chain. Then
               𝑝 · sup 𝑐𝑖 = 𝑝 · sup 𝑐𝑖 = sup 𝑝 · 𝑐𝑖         and 𝑝 · inf 𝑐𝑖 = 𝑝 · inf 𝑐𝑖 = inf 𝑝 · 𝑐𝑖 ,
                   𝑖 ∈N          𝑖 ∈N        𝑖 ∈N                     𝑖 ∈N        𝑖 ∈N      𝑖 ∈N
94                                                                               Ahrens, Rode, Schröer, and Katoen



                           𝐶𝐺𝑅 ∈ wGCLwhy            (( 𝑋 1 ∧ 𝑋 2 ∧ 𝑋 3 ∧ 𝑋 4
                                                    ⊒

                           ⊗ 𝑋 4 # 𝑒 := 4#

                           while ( 𝑒 ≠ 1 ) {
                                  if ( 𝑒 = 2 ) {
                                       { ⊗ 𝑋 3 # 𝑒 := 3 } ⊕ { ⊗ 𝑋 1 # 𝑒 := 1 }
                                  } else {
                                       if ( 𝑒 = 3 ) {
                                             { ⊗ 𝑋 2 # 𝑒 := 2 } ⊕ { ⊗ 𝑋 1 # 𝑒 := 1 }
                                       } else {
                                             if ( (𝑒 = 4) ∨ (𝑒 = 5) ) {
                                                  ⊗ 𝑋 2 # 𝑒 := 2
                                             } else {
                                                   ⊗ 𝑋 3 # 𝑒 := 3
                                             }
                                       }
                                  }
                           }
                            wlp
                               (( ⊤

        Fig. 25. The recursive database provenance program 𝐶𝐺𝑅 satisfies wlpJ𝐶𝐺𝑅 K(⊤) ⊒ 𝑋𝐴𝐵 ∨ 𝑋𝐴𝐴 .

since the scalar multiplication is just the usual multiplication of non-negative reals, which is
continuous. The addition is also 𝜔-bicontinuous using the same argument.                      □
     Lemma F.3. The probability module Wprob over the monoid Mprob admits Heyting (co-)implications.
     Proof. Since the module Wprob is totally ordered, Theorem 3.7 states that the implications
                           (               )                    (                )
                             ∞ if 𝑐 ≤ 𝑑,                          0 if 𝑑 ≤ 𝑐,
                𝑐 →tot 𝑑 =                      and 𝑐 ←tot 𝑑 =                     .
                            𝑑 otherwise                           𝑑 otherwise
specify a bi-Heyting algebra (R∞
                               ≥0, ⊑, min, max, →tot, ←tot ) for 𝑐, 𝑑 ∈ R ≥0 .
                                                                         ∞                                      □

F.2     Why: Database Provenance
We show that the Why module Wwhy over the monoid Mwhy is an 𝜔-bicontinuous monoid-module
with Heyting (co-)implications. The set of positive disjunctive normal form propositional formulae
pDNF is the set of propositional formulae in disjunctive normal form, where all literals are positive
and we consider formulae up to logical equivalence.
  The Why module Wwhy is a semiring, hence we call it Why semiring in the main text.
 Lemma F.4. The Why module Wwhy = (pDNF, ∨, 0, ∧) over the monoid Mwhy = (pDNF, ∧, 1) is a
monoid-module (see Definition 2.1).
  Proof. We observe that (pDNF, ∧, 1) and (pDNF, ∨, 0) are monoids, where the latter is also
commutative due to the disjunction ∨. We check the properties of the scalar multiplication ∧ :
Towards a Verification Infrastructure for wGCL                                                        95


                                              𝐶𝐴𝐶 ∈ wGCLclear
                                              ⊒
                                              (( 𝐼 (𝑛)
                                              while ( 𝑛 > 0 ) {
                                                  𝑛 := 𝑛 − 1#
                                                    {
                                                         ⊗𝑆
                                                    }⊕{
                                                         if ( 𝑛 = 0 ) {
                                                              ⊗𝐶
                                                         } else {
                                                              ⊗𝑇𝑆
                                                         }
                                                    }
                                              }
                                              wlp
                                                  (( 𝑃

          Fig. 26. The program 𝐶𝐴𝐶 describes network security and satisfies wlpJ𝐶𝐴𝐶 K(𝑃) ⊒ 𝐼 (𝑛).


pDNF × pDNF → pDNF, (𝑝, 𝑞) ↦→ 𝑝 ∧ 𝑞. It is associative ((𝑝 ∧ 𝑞) ∧ 𝑟 = 𝑝 ∧ (𝑞 ∧ 𝑟 )) and distributive
(𝑝 ∧ (𝑞 ∨ 𝑟 ) = (𝑝 ∧ 𝑞) ∨ (𝑝 ∧ 𝑟 )) for 𝑝, 𝑞, 𝑟 ∈ pDNF. Furthermore, the neutral element 1 is neutral
(1 ∧𝑝 = 𝑝) and the neutral element 0 is annihilating (𝑝 ∧ 0 = 0), hence all properties are satisfied. □

   Lemma F.5. The Why module Wwhy over the monoid Mwhy is 𝜔-bicontinuous.
   Proof. The natural order is defined as 𝑝 ⊑ 𝑞 if and only if there exists 𝑟 ∈ pDNF such that
𝑝 ∨ 𝑟 = 𝑞 if and only if 𝑝 ≤ 𝑞 in the usual order of propositional formulae (where 0 is the least
element and 1 is the greatest element). Hence, the natural order is a partial order with least element
0, greatest element 1, where suprema and infima of 𝜔-chains exist, since the set of propositional
formulae is finite (up to logical equivalence).
   We show that the scalar multiplication ∧ is 𝜔-bicontinuous in the second argument and assume
that 𝑝 ∈ pDNF and (𝑞𝑖 )𝑖 ∈N ⊆ pDNF is an ascending (descending) 𝜔-chain. Since the set of
propositional formulae is finite, the 𝜔-chain is eventually constant, i.e., there exists 𝑗 ∈ N such that
𝑞𝑖 = 𝑞 𝑗 for all 𝑖 ≥ 𝑗. Hence,
                        𝑝 ∧ sup 𝑞𝑖 = sup (𝑝 ∧ 𝑞𝑖 )       and 𝑝 ∧ inf 𝑞𝑖 = inf (𝑝 ∧ 𝑞𝑖 ).
                             𝑖≤𝑗        𝑖≤𝑗                         𝑖≤𝑗     𝑖≤𝑗

The additive operation ∨ is also 𝜔-bicontinuous using the same argument.                              □

  For the Heyting (co-)implications of the Why module Wwhy over the monoid Mwhy , look at the
remark in Section 3.

F.3   Clearance: Network Security Analysis
We show that the clearance module Wclear over the monoid Mclear is an 𝜔-bicontinuous monoid-
module with Heyting (co-)implications.
96                                                                        Ahrens, Rode, Schröer, and Katoen


   Lemma F.6. The clearance module Wclear over the monoid Mclear is a monoid-module (see Defini-
tion 2.1).
   Proof. Recall that Wclear = ({P, C, S, TS}, min, TS, max) and Mclear = ({P, C, S, TS}, max, P).
We observe that ({P, C, S, TS}, max, P) and ({P, C, S, TS}, min, TS) are monoids, where the latter
is also commutative due to the minimum min. We check the properties of the scalar multiplica-
tion max : {P, C, S, TS} × {P, C, S, TS} → {P, C, S, TS}, (𝑝, 𝑞) ↦→ max{𝑝, 𝑞}. It is associative and
distributive over min, since for all 𝑝, 𝑞, 𝑟 ∈ {P, C, S, TS},
       (𝑝 max 𝑞) max 𝑟 = 𝑝 max(𝑞 max 𝑟 ),      max{𝑝, min{𝑞, 𝑟 }} = min{max{𝑝, 𝑞}, max{𝑝, 𝑟 }}.
Furthermore, the neutral element P is neutral (max{P, 𝑝} = 𝑝) and TS is annihilating (max{𝑝, TS} =
TS), hence all properties are satisfied.                                                         □
     Lemma F.7. The clearance module Wclear over the monoid Mclear is 𝜔-bicontinuous.
   Proof. The natural order is defined as 𝑝 ⊑ 𝑞 if and only if there exists 𝑟 ∈ {P, C, S, TS} such
that 𝑝 min 𝑟 = 𝑞 if and only if 𝑝 ≥ 𝑞 holds on the clearance levels. Hence, the natural order is a
partial (even total) order with least element TopSecret, greatest element Public, where all ascending
(descending) 𝜔-chains become constant after at most 4 steps and hence the supremum (infimum)
exists.
  We show that the scalar multiplication max is 𝜔-bicontinuous in the second argument and
assume that 𝑝 ∈ {P, C, S, TS} and (𝑞𝑖 )𝑖 ∈N ⊆ {P, C, S, TS} is an ascending (descending) 𝜔-chain.
Since the 𝜔-chain is eventually constant, there exists 𝑗 ∈ N such that 𝑞𝑖 = 𝑞 𝑗 for all 𝑖 ≥ 𝑗. Hence,
              max{𝑝, sup 𝑞𝑖 } = sup max{𝑝, 𝑞𝑖 }   and    max{𝑝, inf 𝑞𝑖 } = inf max{𝑝, 𝑞𝑖 }.
                      𝑖≤𝑗       𝑖≤𝑗                              𝑖≤𝑗       𝑖≤𝑗

The additive operation min is also 𝜔-bicontinuous using the same argument.                               □
   Note that the natural order ⊑ is the reverse of the semantic order ≥ on the clearance levels.
This is also the reason why we compute the upper bound wpJ𝐶𝐴𝐶 K(TS) ⊑ 𝐼 to obtain the minimal
clearance level 𝐼 ≤ wpJ𝐶𝐴𝐶 K(TS).
     Lemma F.8. The clearance module Wclear over the monoid Mclear admits Heyting (co-)implications.
     Proof. Since the module Wclear is totally ordered, Theorem 3.7 states that the implications
                          (               )                    (                  )
                            P if 𝑝 ≥ 𝑞,                          TS if 𝑞 ≥ 𝑝,
               𝑝 →tot 𝑞 =                      and 𝑝 ←tot 𝑞 =                       .
                           𝑞 otherwise                           𝑞     otherwise
specify a bi-Heyting algebra ({P, C, S, TS}, ≥, max, min, →tot, ←tot ) for 𝑝, 𝑞 ∈ {P, C, S, TS}.         □
