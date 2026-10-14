                                        Under consideration for publication in Theory and Practice of Logic Programming                  1




                                         (Quantified) Horn Constraint Solving for Program
                                                     Verification and Synthesis
arXiv:1405.7739v1 [cs.LO] 29 May 2014




                                                                             Andrey Rybalchenko
                                                                               Microsoft Research
                                                                          (e-mail: rybal@microsoft.com)

                                                    submitted 1 January 2003; revised 1 January 2003; accepted 1 January 2003



                                                                                   Abstract

                                        We show how automatic tools for the verification of linear and branching time properties of pro-
                                        cedural, multi-threaded, and functional programs as well as program synthesis can be naturally
                                        and uniformly seen as solvers of constraints in form of (quantified) Horn clauses over background
                                        logical theories. Such a perspective can offer various advantages, e. g., a logical separation of
                                        concerns between constraint generation (also known as generation of proof obligations) and
                                        constraint solving (also known as proof discovery), reuse of solvers across different verifications
                                        tasks, and liberation of proof designers from low level algorithmic concerns and vice versa.
                                        To appear in Theory and Practice of Logic Programming (TPLP)

                                        KEYWORDS: Horn constraints, program verification, program synthesis




                                                                               1 Introduction
                                        A variety of interesting and important verification and synthesis questions about pro-
                                        grams can be formulated as constraint satisfaction problems in form of implication/Horn
                                        constraints over a suitable background theory (Gupta et al. 2011a; Gupta et al. 2011c;
                                        Grebenshchikov et al. 2012;      Popeea and Rybalchenko 2012;       Bjørner et al. 2012;
                                        Beyene et al. 2014). Verification of temporal properties and program synthesis are
                                        particularly relevant examples of such questions. Then, given an efficient constraint
                                        solver we can obtain a program verifier or synthesizer by composing it with a constraint
                                        generator. As a result we achieve a separation of concerns such that deduction rules for
                                        reasoning about programs can be developed independently and interact compositionally
                                        with inference engines (that automate the deduction process).



                                                                         2 Constraint generation
                                        We illustrate the constraint based approach using the following example. Let a program
                                        be represented by an assertion init (v) that describes a set of initial states, and an assertion
                                        next(v, v ′ ) that describes a binary transition relation.
2   Andrey Rybalchenko        Microsoft Research          (e-mail: rybal@microsoft.com)

Safety To prove that each state that is reachable from an initial state by following the
transition relation satisfies an assertion safe(v) we generate the following constraint.
                     ∃inv :
                              (∀v : init (v) → inv (v))
                          ∧ (∀v ∀v ′ : inv (v) ∧ next(v, v ′ ) → inv (v ′ ))
                          ∧ (∀v : inv (v) → safe(v))
Here we rely on second order existential quantifier to model the search for a safe (forward-
)inductive invariant. Any model of inv is such an invariant.
   Note that by using the following constraint system (but not the solver/inference engine)
we can change the proof rule from forward invariance to backward invariance.
                    ∃binv :
                            (∀v : ¬safe(v) → binv (v))
                         ∧ (∀v ∀v ′ : binv (v ′ ) ∧ next(v, v ′ ) → binv (v))
                         ∧ (∀v : binv (v) ∧ safe(v) → false)
Furthermore, we can combine forward and backward reasoning in the same constraint
system:
                    ∃inv ∃binv :
                            (∀v : init (v) → inv (v))
                         ∧ (∀v ∀v ′ : inv (v) ∧ next(v, v ′ ) → inv (v ′ ))
                         ∧ (∀v : ¬safe(v) → binv (v))
                         ∧ (∀v ∀v ′ : binv (v ′ ) ∧ next(v, v ′ ) → binv (v))
                         ∧ (∀v : inv (v) ∧ binv (v) → false)
All these reasoning approaches can be automated by the same solver, which can be made
highly beneficial through consolidation of heuristics, optimizations, and improvements.

Termination To prove program termination, i.e., absence of infinite sequences of states
that start in an initial state and follow the transition relation, we can resort to the
following constraint.
                   ∃inv ∃round :
                          (∀v : init (v) → inv (v))
                        ∧ (∀v ∀v ′ : inv (v) ∧ next(v, v ′ ) → inv (v ′ ))
                        ∧ (∀v : ¬safe(v) → binv (v))
                        ∧ (∀v ∀v ′ : inv (v) ∧ next(v, v ′ ) → round(v, v ′ ))
                        ∧ wf (round )
Note that we rely on a second order predicate wf that holds for well-founded relations.
Each solver can rely on a specific way of proving well-foundedness, e.g., using abstract
interpretation (Cousot and Cousot 2012), ranking functions (Turing 1949) or transition
invariants (Podelski and Rybalchenko 2004b; Rybalchenko 2005).
   Instead of using forward invariance to keep track of reachable states, we can use alter-
     (Quantified) Horn Constraint Solving for Program Verification and Synthesis                            3

native approaches, as exemplified by the constraint systems for reasoning about program
safety.

Information flow property Security properties often require proving that any alternation
of a (secret) program input is undetected by observing its (public) output. Let final (v)
be an assertion that describes the set of all states where computation can stop. The
program satisfies the non-interference property if the following constraint is satisfiable.

  ∃io :
            (∀v : init (v)next (v, v ′ ) → io(v, v ′ ))
          ∧ (∀v ∀v ′ ∀v ′′ : io(v, v ′ ) ∧ next(v ′ , v ′′ ) → io(v, v ′′ ))
          ∧ (∀v ∀v ′ ∀w ∀w′ : v 6= w ∧ io(v, v ′ ) ∧ io(w, w′ ) ∧ final(v) ∧ final (w′ ) → w = w′ )
This constraint captures reasoning about pairs of computations through self-composition
of input/output relation of the program, instead of performing a source-to-source trans-
formation (Barthe et al. 2004) or a specialized inference procedure (Backes et al. 2009).

Temporal property For proving properties expressed in temporal logics we can rely on
existing proof systems that reduce temporal reasoning to first-order reasoning (with aux-
iliary assertions), e.g., the proof system for CTL* (Kesten and Pnueli 2005). For example,
to prove that there exists a computation that visits states satisfying an assertion p(v)
until finally it reaches a state satisfying an assertion q(v), i.e., (init (v), next(v, v ′ )) |=
E (p(v)U q(v)), we need to solve the following constraint.

             ∃inv ∃round :
                      (∀v : init (v) → inv (v))
                   ∧ (∀v : inv (v) ∧ ¬q(v) → ∃v ′ : next(v, v ′ ) ∧ inv (v ′ ) ∧ round(v, v ′ ))
                   ∧ (∀v : inv (v) → p(v))
                   ∧ wf (round )
Note that we model the existence of a computation by relying on existential quantification
in the constraints together with a recursive dependency (Beyene et al. 2013).

Reactive synthesis We formulate the reactive synthesis problem as constraint solving by
turning this problem into a game solving problem (Beyene et al. 2014). For example,
consider the synthesis of a system with an unknown transition relation sys(v, v ′ ) that
is executed in an adversarial environment with a given transition relation env (v, v ′ ).
The system’s objective is to reach a state satisfying an assertion goal (v) regardless of
environment’s behavior. The following constraint characterizes the synthesis problem.

          ∃inv ∃round :
                   (∀v : init (v) → inv (v))
                ∧ (∀v ∀v ′ : inv (v) ∧ ¬goal (v) ∧ env (v, v ′ ) → ∃v ′′ : sys(v ′ , v ′′ ) ∧ inv (v ′′ )
                                                                               ∧ round(v, v ′′ ))
                ∧ wf (round )
4   Andrey Rybalchenko       Microsoft Research      (e-mail: rybal@microsoft.com)

Other temporal objectives can be satisfied by relying on a temporal proof system, akin
to temporal verification.


                                 3 Constraint solving
In the previous section we illustrated how program verification and synthesis question can
be formalized as second-order constraint solving problems in form of recursive implication
constraints with well-foundedness conditions, and quantifier alternation.
   Solving (various sub-classes of) such constraints is a thriving area of research. Solvers
often take advantage of the fact that constraints have Horn-like structure, which enables
iterative, abstraction based solving approaches.
   Important        classes    include     recursion-only      case     (Hoder et al. 2011;
Grebenshchikov et al. 2012; McMillan and Rybalchenko 2012; Rümmer et al. 2013)
that is facilitates reasoning about safety properties, extension with well-foundedness for
reasoning about liveness properties (Grebenshchikov et al. 2012), extension with uni-
versal quantification for inferring universally quantified invariants (Bjørner et al. 2013),
and extension with existential quantification for dealing with synthesis and branching
time questions (Beyene et al. 2013). Often such solvers rely on recursion-free fragments
of implication constrains (McMillan 2005; Gupta et al. 2011b; Gurfinkel et al. 2013;
Blanc et al. 2013) and ranking function synthesis (Podelski and Rybalchenko 2004a) as
a basic inference components.
   Constraint logic programming offers an effective tool for implementing solvers for quan-
tified (Horn) implication constraints with well-foundedness, e.g., the HSF solver and its
extensions (Grebenshchikov et al. 2012; Beyene et al. 2013; Bjørner et al. 2013) is imple-
mented using ideas of blending meta-logic programming and constraint logic program-
ming (Podelski and Rybalchenko 2007).


                                       References
Backes, M., Köpf, B., and Rybalchenko, A. 2009. Automatic discovery and quantification
  of information leaks. In Security and Privacy. IEEE Computer Society.
Barthe, G., D’Argenio, P., and Rezk, T. 2004. Secure information flow by self-composition.
  In CSF: Computer Security Foundations. IEEE.
Beyene, T., Chaudhuri, S., Popeea, C., and Rybalchenko, A. 2014. A constraint-based
  approach to solving games on infinite graphs. In POPL: Principles of Programming Languages.
  ACM.
Beyene, T., Popeea, C., and Rybalchenko, A. 2013. Solving existentially quantified Horn
  clauses. In CAV: Computer Aided Verification. Springer.
Bjørner, N., McMillan, K. L., and Rybalchenko, A. 2012. Program verification as satis-
  fiability modulo theories. In SMT@IJCAR:Satisfiability Modulo Theories. EasyChair.
Bjørner, N., McMillan, K. L., and Rybalchenko, A. 2013. On solving universally quan-
  tified Horn clauses. In SAS: Static Analysis. Springer.
Blanc, R., Gupta, A., Kovács, L., and Kragl, B. 2013. Tree interpolation in Vampire. In
  LPAR: Logic for Programming, Artificial Intelligence, and Reasoning. Springer.
Cousot, P. and Cousot, R. 2012. An abstract interpretation framework for termination. In
  POPL: Principles of Programming Languages. ACM.
Grebenshchikov, S., Gupta, A., Lopes, N. P., Popeea, C., and Rybalchenko, A. 2012.
     (Quantified) Horn Constraint Solving for Program Verification and Synthesis          5

  HSF(C): A software verifier based on Horn clauses - (competition contribution). In TACAS:
  Tools and Algorithms for the Construction and Analysis of Systems. Springer.
Grebenshchikov, S., Lopes, N. P., Popeea, C., and Rybalchenko, A. 2012. Synthesizing
  software verifiers from proof rules. In PLDI: Programming Language Design and Implemen-
  tation. ACM.
Gupta, A., Popeea, C., and Rybalchenko, A. 2011a. Predicate abstraction and refine-
  ment for verifying multi-threaded programs. In POPL: Principles of Programming Languages.
  ACM.
Gupta, A., Popeea, C., and Rybalchenko, A. 2011b. Solving recursion-free Horn clauses
  over LI+UIF. In APLAS: Programming Languages and Systems. Springer.
Gupta, A., Popeea, C., and Rybalchenko, A. 2011c. Threader: A constraint-based verifier
  for multi-threaded programs. In CAV: Computer Aided Verification. Springer.
Gurfinkel, A., Rollini, S. F., and Sharygina, N. 2013. Interpolation properties and
  SAT-based model checking. In ATVA: Automated Technology for Verification and Analy-
  sis. Springer.
Hoder, K., Bjørner, N., and de Moura, L. M. 2011. µZ - an efficient engine for fixed points
  with constraints. In CAV: Computer Aided Verification. Springer.
Kesten, Y. and Pnueli, A. 2005. A compositional approach to CTL∗ verification. Theor.
  Comput. Sci. 331, 2-3.
McMillan, K. L. 2005. An interpolating theorem prover. Theor. Comput. Sci. 345, 1.
McMillan, K. L. and Rybalchenko, A. 2012. Computing relational fixed points using in-
  terpolation. Tech. rep., Microsoft Research. MSR-TR-2013-6.
Podelski, A. and Rybalchenko, A. 2004a. A complete method for the synthesis of linear
  ranking functions. In VMCAI: Verification, Model Checking, and Abstract Interpretation.
  Springer.
Podelski, A. and Rybalchenko, A. 2004b. Transition invariants. In LICS: Logic in Computer
  Science. IEEE.
Podelski, A. and Rybalchenko, A. 2007. ARMC: The logical choice for software model
  checking with abstraction refinement. In PADL: Practical Aspects of Declarative Languages.
  Springer.
Popeea, C. and Rybalchenko, A. 2012. Compositional termination proofs for multi-threaded
  programs. In TACAS: Tools and Algorithms for the Construction and Analysis. Springer.
Rümmer, P., Hojjat, H., and Kuncak, V. 2013. Disjunctive interpolants for Horn-clause
  verification. In CAV: Computer Aided Verification. Springer.
Rybalchenko, A. 2005. Temporal verification with transition invariants. Ph.D. thesis.
Turing, A. M. 1949. Checking a large routine. In Conf. on High Speed Automatic Calculating
  machines.
