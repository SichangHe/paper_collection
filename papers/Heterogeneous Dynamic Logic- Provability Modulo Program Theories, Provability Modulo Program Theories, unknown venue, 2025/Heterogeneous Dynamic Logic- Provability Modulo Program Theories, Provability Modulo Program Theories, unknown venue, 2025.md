                                         Heterogeneous Dynamic Logic:
                                         Provability Modulo Program Theories
                                         SAMUEL TEUBER, Karlsruhe Institute of Technology (KIT), Germany
                                         MATTIAS ULBRICH, Karlsruhe Institute of Technology (KIT), Germany
                                         ANDRÉ PLATZER, Karlsruhe Institute of Technology (KIT), Germany
                                         BERNHARD BECKERT, Karlsruhe Institute of Technology (KIT), Germany
arXiv:2507.08581v2 [cs.LO] 14 Apr 2026




                                         Formally specifying, let alone verifying, properties of systems involving multiple programming languages is in-
                                         herently challenging. We introduce Heterogeneous Dynamic Logic (HDL), a framework for combining reasoning
                                         principles from distinct (dynamic) program logics in a modular and compositional way. HDL mirrors the archi-
                                         tecture of satisfiability modulo theories (SMT): Individual dynamic logics, along with their calculi, are treated as
                                         dynamic theories that can be combined to reason about heterogeneous systems whose components are verified
                                         using different program logics. HDL provides two key operations: Lifting extends an individual dynamic theory
                                         with new program constructs (e.g., the havoc operation or regular programs) and automatically augments its
                                         calculus with sound reasoning principles for the new constructs; and Combination enables cross-language rea-
                                         soning in a single modality via Heterogeneous Dynamic Theories, facilitating the reuse of existing proof infrastruc-
                                         ture. By lifting combined theories with regular programs, we obtain heterogeneous control structures that allow
                                         us to reason about intertwined cross-language behavior. We formalize dynamic theories, their lifting and combi-
                                         nation, and prove the soundness of all proof rules in Isabelle. We also introduce a proof rule combining deductive
                                         DL-based reasoning with reasoning principles from Kleene Algebras with Tests. Furthermore, we prove relative
                                         completeness theorems for lifting and combination: Under usual assumptions, reasoning about lifted or com-
                                         bined theories is no harder than reasoning about the constituent dynamic theories and their common first-order
                                         structure (i.e., the “data theory”). We demonstrate HDL’s value by verifying an automotive case study where a
                                         Java controller (formalized in Java dynamic logic) steers a plant model (formalized in differential dynamic logic).
                                         CCS Concepts: • Theory of computation → Program verification; Logic and verification; Modal and
                                         temporal logics; • Software and its engineering → Software verification.
                                         Additional Key Words and Phrases: Dynamic Logic, Theory Combination, Relative Completeness, Isabelle
                                         ACM Reference Format:
                                         Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert. 2026. Heterogeneous Dynamic Logic:
                                         Provability Modulo Program Theories. Proc. ACM Program. Lang. 10, PLDI, Article 217 (June 2026), 52 pages.
                                         https://doi.org/10.1145/3808295

                                         1    Introduction
                                         Since its origins in Hoare logic [33] and Dijkstra’s predicate transformers [20], formal verification
                                         has grown into a mature discipline, supporting a wide range of languages, from bytecode [47, 67],
                                         C [16, 38], or Java [2, 11], to modern languages like Rust [4, 41] and even to hybrid programs for
                                         cyber-physical systems [50]. While individual “worlds” enjoy robust verification infrastructures, it
                                         remains challenging to rigorously combine verification results across languages. Yet, many modern
                                         systems are inherently heterogeneous and would benefit from methodologies enabling composi-
                                         tional reasoning across program logics. This raises the fundamental questions of how semantics and
                                         Authors’ Contact Information: Samuel Teuber, Karlsruhe Institute of Technology (KIT), Karlsruhe, Germany, teuber@kit.edu;
                                         Mattias Ulbrich, Karlsruhe Institute of Technology (KIT), Karlsruhe, Germany, ulbrich@kit.edu; André Platzer, Karlsruhe
                                         Institute of Technology (KIT), Karlsruhe, Germany, platzer@kit.edu; Bernhard Beckert, Karlsruhe Institute of Technology
                                         (KIT), Karlsruhe, Germany, beckert@kit.edu.

                                         © 2026 Copyright held by the owner/author(s).
                                         This is the author’s version of the work. It is posted here for your personal use. Not for redistribution. The definitive Version
                                         of Record was published in Proceedings of the ACM on Programming Languages, https://doi.org/10.1145/3808295.



                                                                              Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:2                                             Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


proof principles of program logics can be combined to specify and verify heterogeneous systems. In
practice, heterogeneous verification today often resorts to encoding one system (e.g., a software con-
troller) in the language of another (e.g., hybrid programs) [28, 37, 39, 63]. However, such encodings
are neither seamless nor intuitive: They obscure structure and fail to reuse existing infrastructure.
   Dynamic Logic. We argue that Dynamic Logic (DL) provides a strong foundation for reasoning
about heterogeneous systems due to its expressiveness and its structural properties. DL generalizes
traditional verification techniques [20, 33] by treating programs as first-class citizens of the logic
embedded within modalities (rather than residing outside the logic). This enables DL to specify a
large variety of systems including imperative languages [31] or hybrid systems [50]. Crucially, DL’s
treatment of programs gives rise to a fully compositional logic that naturally supports properties
such as liveness [62] or incorrectness [56] as well as hyperproperties (e.g. refinement [42, 54, 68] or
secure information flow [8]) without necessitating specialized logics (as necessary for, e.g., Hoare
logic). However, prior DL frameworks are confined to a single, fixed programming language, and
are thus ill-suited for verifying heterogeneous systems that combine components from multiple
“worlds” (e.g. Java code and hybrid systems). As a lighter-weight counterpart to DL, Kleene Algebra
with Tests [40] (KAT) is an effective methodology for (automated) program verification. Our
approach also integrates with program rewriting via KAT to ease heterogeneous verification.
   Satisfiability Modulo Theories. The success of satisfiability modulo theories (SMT) has transformed
first-order reasoning across a wide range of applications. By requiring a unified set of assumptions
(e.g., stable infiniteness [46]) from first-order theories, SMT solvers can delegate theory-specific
queries, e.g., involving integers or arrays, to specialized sub-solvers. Users can freely combine
theories within a single formula while theory combination mechanisms ensure soundness and, under
suitable assumptions, even completeness. The seminal results by Shostak, Nelson and Oppen, and
their subsequent extensions [6, 44, 46, 61, 65, 66] thus paved the way for the modular combination
of first-order theories. This enables a separation of concerns between theory-specific reasoning and
the logical structure connecting the theories. Inspired by this design, we ask: Can a similar, modular
structure be applied to program logics? That is, can we reason about heterogeneous programs
while preserving the semantics and proof rules established for individual languages? This paper
answers the question in the affirmative, building on the rigorous foundations of dynamic logic.
  Contribution. This paper introduces Heterogeneous Dynamic Logic (HDL): The foundational for-
mal notions that allow DL to serve as a generalized, SMT-inspired vehicle to combine different
program logics (as dynamic theories), just like first-order logic serves as a vehicle to combine different
data logics (as first-order theories). Heterogeneous Dynamic Logic supports two key operations:
    • Lifting (Section 6) extends a given dynamic theory Δ with additional program constructs,
      such as nondeterministic choice (Δ:=∗ , Section 6.1) or the closure over regular programs (Δreg ,
      Section 6.2). Lifting also automatically extends the dynamic theory’s calculus with sound
      proof rules to reason about the extended programming language.
    • Combination (Section 7) merges two theories Δ (0) and Δ (1) (defined over programming lan-
      guages Λ𝑃(0) , Λ𝑃(1) ) into a single heterogeneous dynamic theory Δ̂. This new dynamic theory sup-
      ports heterogeneous programs in which programs from Λ𝑃(0) and Λ𝑃(1) can be composed freely
      using regular programs. Combination also merges and extends the individual proof calculi.
This enables rigorous, modular reasoning over heterogeneous programs with deeply intertwined
behavior of programs stemming from individual logics. Along with a relatively complete proof
calculus for lifted/combined dynamic theories, we also present an axiom leveraging KAT-style
equational rewriting – coupling KAT’s reasoning principles with DL’s proof system. We introduce

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                               217:3


a formalization of dynamic theories, their lifting and combination and their sound proof calculi
in Isabelle in a reusable manner via its Locale infrastructure (formalized Lemmas/Theorems are in
cyan, see Section D). This formalization directly supports interactive theorem proving for hetero-
geneous systems with proof infrastructure reuse. Simultaneously, the SMT-like architecture of our
proof calculus lays the groundwork for automated heterogeneous verification in the long term.
    Overview. The remainder of this paper is structured as follows: Section 2 motivates the challenge
of heterogeneous verification using a concrete case study. Section 3 surveys prior attempts to support
general cross-language verification. Sections 4 and 5 introduce our notion of dynamic theories, a
generalization of dynamic logic with reduced assumptions, and demonstrate that our assumptions
suffice to recover well-known properties of “DL-like” logics. In this context, we also connect DL’s
proof calculus to equational reasoning via KAT. Section 6 presents lifting, an approach to extend
a given dynamic theory with additional program features such as regular programs along with
deriving the necessary proof rules. To this end, we also prove that our regular program lifting results
in a KAT which enables tool reuse. Section 7 proves that the heterogeneous dynamic theory over two
dynamic theories is once again a dynamic theory. Corresponding additional proof rules are derived
including additional KAT-style identities which ease verification in practice. Finally, Section 8
establishes conditions under which relative completeness transfers from a dynamic theory to its
lifted and/or combined version. Section 9 showcases the utility of HDL on our automotive case study.

2   Motivation: Case Study
As example of a heterogeneous system we con- 1 int x1 = v+1;
                                                    2 int x2 = x1 x1;
sider a car steered by a software controller writ- 3 if(10000*x2*+ (amax-amin)*T*
ten in Java while driving towards a stop sign. 4 (amax*T + 200*x1) > -20000*amin*(p-1)) {
To effectively leverage existing proof infrastruc- 5 this.acc = amin;
                                                    6 } else {
tures, we wish to model the time-continuous, 7 this.acc += (p>10000) ? 10 : -10;
physical system in Differential Dynamic 8 this.acc = (this.acc > amax) ? amax :
Logic [50] (𝑑L) using KeYmaera X [25, 49, 50, 9                    (this.acc < amin) ? amin : this.acc; }

53] while verifying the controller using Java Dy-  (a) Java Controller  ctrl that can be analyzed using
namic Logic [7] (JavaDL) using the KeY tool [2].   JavaDL.
                                                                                                       
   Java Dynamic Logic. JavaDL allows reason-        env ≡ t := 0; (x′ = v, v′ = a, t′ = 1 & t ≤ T) ;
ing about Java programs [2, 7, 9] (including ex- (b) Environment model that can be analyzed in Differ-
                                                  ential Dynamic Logic (𝑑L).
ceptions, heap state etc.). Consider the method
in Figure 1a serving as controller for a car ap-                       a ← this.acc
                                                              ctrl p ← (x − s) ; v ← v env
proaching a stop sign at distance p with velocity
v. The method computes an acceleration via the (c) The heterogeneous system (← denotes some kind
stateful field this.acc and brakes in case the of assignment; semantics see Section 9).
condition in line 3 is satisfied. The method is          Fig. 1. Heterogeneous system case study
not idempotent due to this.acc and its computation also depends on static variables amax, amin
and T. While JavaDL (and KeY) is capable of verifying Java programs, JavaDL cannot reason about
physical dynamics, e.g. given as differential equations.
   Differential Dynamic Logic. Differential Dynamic Logic [50] (𝑑L) allows reasoning about hybrid
programs whose states evolve either along discrete state transitions (variable assignments) or
continuously along differential equations. Consider the hybrid program env in Figure 1b which
sets a clock variable t to 0 and evolves x, v and t along a differential equation for a maximum
time of T. The program describes the evolution of a car’s position under constant acceleration a.
Using the proof calculus implemented in the theorem prover KeYmaera X [25, 49, 50, 53], we can

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:4                                             Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


prove statements about hybrid programs. However, KeYmaera X cannot natively reason over Java
programs which, e.g., encompass integer arithmetic with overflows and heap state invariants.
  Challenge. Both of the introduced verification methodologies come with strengths and weak-
nesses. While they excel at verifying properties for their “native” domain of computation, they lack
support for their respective counterpart. However, to verify the safety of the entire heterogeneous
system, we require a formalism that allows us to reason about the looped heterogeneous system
sketched in Figure 1c. We propose a general framework that gives a formal semantics to this sketch
and provides a proof calculus that emphasizes the reuse of proof infrastructure. Our framework is
not tied to the particular combination of languages discussed in this case study.

3   Related Work
   Dynamic Logic. As summarized by Ahrendt et al. [3], DL has been instantiated for a wide range
of behavioral languages (e.g., Java [2], hybrid programs [50, 51], byte code [67, 68] or abstract state
machines [57]) allowing proofs of numerous properties (functional correctness [10, 18], safety [35,
52], liveness [62], incorrectness [56], refinement [42, 68] or information flow [8, 13]). However, the
combination of behavioral languages has not previously been studied.
  Parameterized Dynamic Logic. Parameterized Dynamic Logic [69] is a framework designed to
build a dynamic logic and a calculus for a given programming language based on symbolic execution
rules. While their approach also generalizes the concept of dynamic logic, it does not address the
challenge to reason about heterogeneous programs which is at the core of this paper.
  Satisfiability Modulo Theories. Research on SMT theory combination [6, 44, 46, 65, 66] is not
readily extensible to modal/dynamic logic: Much of the theory is limited to quantifier-free first-order
logic (which is even more restrictive than full first-order (dynamic) logic), and classic SMT theory
combination has no way of dealing with a dynamic logic’s program primitives.
   Intermediate Verification Languages. To reason about programs or state transition systems across
languages, an effective approach is to encode them into a unified intermediate representation. This
paradigm is used in systems like Boogie [5], Why3 [22] and Viper [43], which enable language-
agnostic reasoning. Similarly, in model checking, common input formats like SMV and exchange
formats such as VMT [15] and Moxi [36] facilitate analyzing heterogeneous systems.
   In contrast, heterogeneous dynamic logic deliberately avoids assuming a shared language or logic,
aiming to integrate verification systems without a clear common ground. For instance, differential
dynamic logic supports continuous value evolution through differential equations – a capability
that cannot be naturally encoded within the languages mentioned earlier.
   Fibring. In contrast to logic fibring [26, 27] (established for modal logics), Heterogeneous Dynamic
Logic goes beyond the fibring of “truth bearing” entities that one could expect from a DL with
multiple modalities. For example, fibring could produce formulas of the form 𝜙 1 → [𝛼 1 ] 1 [𝛼 2 ] 2 𝜙 2
(see Section 7.1) where [·] 1 and [·] 2 represent modalities for distinct programming languages. While
merging of truth-bearing entities can encode some behaviors observed in heterogeneous systems,
there is a large class of behaviors that cannot be modeled by merely merging truth bearing entities
since it ignores the programs. In particular, we cannot model looped execution.
   UTP and Heterogeneous Bisimulation. The Unified Theories of Programming [34] (UTP) and its
Isabelle formalization [24] provide a common framework for integrating diverse programming
languages into a common semantics with shared state. While this enables proofs on cross-language
systems, it typically requires embedding existing program semantics within UTP. In contrast, HDL
aims for modular and sound reuse of existing (external) verification infrastructure via the common

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                               217:5


interface provided by DL. For example, our case study natively leverages the existing DL-based proof
infrastructures for Java [2] and hybrid programs [25] unchanged, whereas the UTP community has
invested considerable effort (notably, Foster’s formalisation of hybrid relations [23]) to embed hybrid
programs within UTP. This highlights HDL’s orthogonal philosophy in comparison to UTP. HDL also
provides native support for a wide range of properties that can be encoded in DL (see also [3, Sec. 3]).
   The range of properties also distinguishes HDL from heterogeneous (bi)simulation [45] which
is designed for comparison of systems (e.g., a labeled transition system vs. a probabilistic system).
   Contract-based and Polyglot Verification. Our approach provides three key advantages in compar-
ison to contract-based techniques: First, in our framework all components, all communication, all
invariants, and all desired properties can be modeled in a single integral formal system and can later
be proved in a single formula. While language agnostic contract languages like Contract-LIB [21]
aim to bridge the specification gap between different PLs, they cannot model heterogeneous systems
in a single program. Instead, they require a meta-level argument on combination outside any pro-
gram logic. Secondly, in its usual formulation, contracts overapproximate functional behavior and are
hence only suitable for correctness/safety verification (box-properties) and not liveness/relational
properties supported by DL. Finally, our relative completeness results in Section 8 ensure that we
can prove all properties of interest using our calculus by reusing proofs for individual components.
   Polyglot verification, specifically PolyVer [14], advocates for a contract-based verification ap-
proach for cross-language verification. While PolyVer can alleviate the issue of requiring meta-level
arguments by providing an automaton-based semantics for the polyglot system, their approach
does not provide a relative completeness guarantee. Hence, it is a priori unclear whether their
specification language is sufficiently expressive to prove all safety properties. In contrast, PolyVer
proposes an interesting, AI-based approach to synthesize auxiliary contracts. Evaluating similar
techniques for heterogeneous dynamic logic could be an exciting direction of future work.
   Kleene Algebras. Kleene Algebra Modulo Theories [30] (KAMT) is a conceptually related approach
that proposes to turn a client theory into a Kleene Algebra with Tests (KAT). In contrast to KAMT, we
derive a dynamic logic and emphasize reuse of proof infrastructure for combined theories. Kozen [40]
motivated KAT with the observation that “many simple program manipulations [...] do not require
the full power of [propositional DL]”; indeed, dynamic logics support a wider range of properties,
including quantifiers, liveness, or properties with alternating modalities, which are typically beyond
KA(M)T’s power. While DL’s expressivity precludes decidability, we prove relative completeness
results for our calculus under theory lifting or combination (see Section 8). Moreover, as axiom (E)
demonstrates, we can also integrate KA(M)T results into our reasoning where applicable. In comple-
mentary research, Kleene Algebra with Domain [19, 58, 59] extends KAT with (anti-)domain opera-
tors to recover propositional DL expressivity, but remains in the propositional, quantifier-free setting.

4   Dynamic Theories
The foundation of our approach is the idea behind First-Order Dynamic Logic (FODL) [31, 32],
which extends first-order logic to a multi-modal logic where programs parameterize modalities.
For instance, for an integer first-order theory, the formula
                                       0 ≤ 𝑣 → [𝑤 := 𝑣 + 1], 1 ≤ 𝑤                                               (1)
                                       |{z}     | {z } |{z}
                                        atom          program       atom

states that after all execution of 𝑤 := 𝑣 + 1, 𝑤 is positive if 𝑣 was non-negative. Unlike Hoare
triples [33] or predicate transformers [20], Dynamic Logic treats programs as first-class citi-
zens of formulas, enabling compositional reasoning about richer properties such as reachability
(⟨𝑤 := 𝑣 + 1⟩ 𝑤 > 0) and hyper-properties ([𝑝] ⟨𝑞⟩ 𝐹 ).

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:6                                             Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


   Our contribution generalizes this principle: not only the first-order theory but also the underlying
program language can be chosen freely. We introduce dynamic theories as a minimal semantic
interface capturing the assumptions on programs and first-order reasoning. Concrete program logics
(existing or new) are instantiations of a dynamic theory; multiple such theories can be composed
into a heterogeneous dynamic theory that still satisfies the same interface. This composability allows
“stacking” theories while retaining derived proof rules. By parameterizing over both programs and
atoms, our framework unifies diverse program logics and provides a reusable foundation akin to
SMT theory combination — ensuring that compliant dynamic logics can interoperate and inherit
proof rules automatically.

4.1     Syntax
To focus the presentation on the modal aspects of the logic, we abstract away from the term
structure of a Dynamic Logic’s first-order fragment and instead begin our investigation directly
at the level of first-order atoms. We formalize the syntactic material of a dynamic theory in the
notion of a dynamic signature:
Definition 4.1 (Dynamic Signature). A dynamic signature Λ is given by a set of variables Λ𝑉 , a set
of first-order atoms Λ𝐴 , and the set of programs Λ𝑃 with all three sets pairwise disjoint. We denote this
as Λ = (Λ𝑉 , Λ𝐴 , Λ𝑃 )
   Given a signature Λ, we can define the structure of formulas that are part of a dynamic theory
in a manner that is similar to classical FODL while constraining programs and variables to all
syntactical constructs contained in Λ:
Definition 4.2 (Λ-formulas). Let Λ = (Λ𝑉 , Λ𝐴 , Λ𝑃 ) be a dynamic signature. Given a variable
𝑣 ∈ Λ𝑉 , an atom 𝑎 ∈ Λ𝐴 , and a program 𝑝 ∈ Λ𝑃 , Λ-formulas are defined by the following grammar:
𝐹, 𝐺 F 𝑎 | ¬𝐹 | 𝐹 ∧ 𝐺 | ∀𝑣 𝐹 | [𝑝] 𝐹
  The set of all Λ-Formulas is denoted as FmlΛ . We denote the first-order fragment (i.e. all formulas
without any box modality) as FOLΛ ⊂ FmlΛ . Further, we introduce syntactic sugar for the diamond
modality, which we denote as ⟨𝑝⟩ 𝐹 ≡ ¬ [𝑝] ¬𝐹 . Similarly, syntactic sugar can be introduced for
existential quantifiers and other logical connectives (∨, →, . . .).
Example 4.1 (Syntax for Ordered Semirings). As a running example, consider an ordered semi-ring
(R, +, ·, ≤) and an arbitrary set of variables Λ𝑉R = {𝑣 1, 𝑣 2, . . . }: We define terms as literals 𝑐 ∈ 𝐿 ⊆ R,
variables 𝑣 ∈ Λ𝑉R and any composition of terms with + and ·. Atoms are any formulas of the form
𝑡 1 ≤ 𝑡 2 and programs have the form 𝑣 := 𝑡 1 (for 𝑡 1, 𝑡 2 terms and 𝑣 ∈ Λ𝑉R ). Together, these components
form a dynamic signature containing variables, atoms and programs.

4.2     Semantics
The previous section outlined the syntactic constructs necessary to define a dynamic theory. With
formulas of our dynamic theory defined, we can now focus on the semantic constructs that are
necessary to define a dynamic theory. To this end, we require five components: First, since we
are considering a modal logic, we require a state space S over which we can evaluate Λ-formulas.
Secondly, we require functions to evaluate the values of variables (V) w.r.t. some universe (U),
the truth-value of atoms (A), and the state-transition behavior of programs (P). Each of these
components must satisfy some conditions. Once these components are defined, we can define the
evaluation of formulas. We now begin by defining state spaces and variable evaluations:
Definition 4.3 (Universes, State Spaces and Variable Evaluation). Given a dynamic signature Λ
with variables Λ𝑉 and a set U ≠ ∅ called universe, a state space S ≠ ∅ is defined as a set of states
together with a variable evaluation function V : S × Λ𝑉 → U such that S and V satisfy:

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                                 217:7


   (S Independence) For all 𝜇, 𝜎 ∈ S and 𝑉 ⊆ Λ𝑉 ,there exists an 𝜔 ∈ S such that for all 𝑣 ∈ Λ𝑉 :
                    V (𝜔, 𝑣) = V (𝜇, 𝑣) if 𝑣 ∈ 𝑉 and else V (𝜔, 𝑣) = V (𝜎, 𝑣)

   This definition of state spaces slightly deviates from popular definitions of Dynamic Logic that
often consider the state space as the set of all mappings from Λ𝑉 to U which for us corresponds
to defining V (𝜇, 𝑣) = 𝜇 (𝑣). However, our set-based definition allows for more complex state
spaces. For example, we can globally exclude the possibility of a variable 𝑣 taking on certain values
𝛿 ∈ U, which can be leveraged for typed/sorted state spaces. Similarly, we can construct state
spaces that are formed by composing states from other state spaces (an example of this can be
found in Section 7). Our approach also circumvents formalization hurdles in Isabelle/HOL that
would accompany a dependently typed mapping approach for state spaces. Importantly, the state
independence property retains a notion of well-formedness of the state space which ensures that if
a variable 𝑣 ∈ Λ𝑉 is assigned some value 𝛿 ∈ U, then any other state can also be modified so that 𝑣
has that value 𝛿. For example, this can ensure that a variable which (in a more fine-grained view of
the dynamic theory) is an integer variable can indeed be assigned all integer values independently
of the remaining state. State independence is important for proving coincidence properties for
formulas and programs which is crucial for proof rule derivation. For states 𝜇, 𝜎 ∈ S we will say 𝜇
and 𝜎 are equal on 𝑉 ⊆ Λ𝑉 (denoted 𝜇 ≡𝑉 𝜎) whenever for all 𝑣 ∈ 𝑉 it holds that V (𝜇, 𝑣) = V (𝜎, 𝑣).
   For the semiring dynamic signature from Example 4.1 we can define the universe U = R and
the state space as the set of all mappings 𝜇 : Λ𝑉 → U. The variable evaluation function then is
V R (𝜇, 𝑣) = 𝜇 (𝑣). For example, if R = Z, then a variable can take on any integer value.
   A state can also be used for the evaluation of atoms which we define as follows:

Definition 4.4 (Atom Evaluation). Given a dynamic signature Λ with variables Λ𝑉 and atoms Λ𝐴
and a state space S we define a free variable overapproximation FV𝐴 : Λ𝐴 → 2Λ𝑉 and an atom
evaluation function A : Λ𝐴 → 2 S as any functions satisfying the following properties:
       (FV𝐴 Coverage) For any atom 𝑎 ∈ Λ𝐴 and any states 𝜇, 𝜎 ∈ S
                        if 𝜇 ≡ (FV𝐴 (𝑎) ) 𝜎 then 𝜇 ∈ A (𝑎) iff 𝜎 ∈ A (𝑎)
           (FV𝐴 Finite) FV𝐴 (𝑎) is finite for all atoms 𝑎 ∈ Λ𝐴 .

   While the coverage property ensures that FV𝐴 covers all variables that influence the evaluation
of a given atom, the finiteness property ensures that atoms are well-behaved in a sense that is
classically expected in first-order logic (where only variables that syntactically occur in the finite
formula can have an impact). These two properties are once again of particular importance for
coincidence properties essential for deriving the dynamic theory proof rules.
   Continuing our semiring dynamic signature from Example 4.1, we define the atom evaluation
function that takes a state 𝜇 and evaluates an atomic formula (and its resp. terms) w.r.t. 𝜇 (i.e.
𝜇 ∈ A (𝑡 1 ≤ 𝑡 2 ) iff 𝜇 (𝑡 1 ) ≤ 𝜇 (𝑡 2 ) in Z, where 𝜇 (𝑡) evaluates the variables in term 𝑡 w.r.t. 𝜇). Concretely,
a state 𝜇 satisfies the atom 0 ≤ 𝑣 iff V Z (𝜇, 𝑣) = 𝜇 (𝑣) ≥ 𝜇 (0) = 0. The definition of FV𝐴R can then be
given via straightforward syntactical analysis of terms and formulas.
   Similarly to the semantics of atoms, the semantics of programs also have side conditions on how
their behavior is influenced by variables which is captured by a program’s free variables FV𝑃 ·. The
side conditions also provide us with an (implicit) parameterization of programs w.r.t. their variables.
Formally, we require the program evaluation function to satisfy the following constraints:

Definition 4.5 (Program Evaluation). Given a dynamic signature Λ with variables Λ𝑉 and programs
Λ𝑃 and a state space S we define a free variable overapproximation FV𝑃 : Λ𝑃 → 2Λ𝑉 and a program
evaluation function P : Λ𝑃 → 2 S as any functions satisfying the following properties:
                                   2




                                 Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:8                                             Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


      (FV𝑃 Coverage) For all programs 𝑝 ∈ Λ𝑃 , all states 𝜇, 𝜎, 𝜔 ∈ S, and any set 𝑉 ⊇ FV𝑃 (𝑝):
                       if 𝜇 ≡𝑉 𝜎 and (𝜇, 𝜔) ∈ P (𝑝), then there exists a state 𝜔˜ such that
                       (𝜎, 𝜔)
                            ˜ ∈ P (𝑝) and 𝜔 ≡𝑉 𝜔˜
          (FV𝑃 Finite) For all programs 𝑝 ∈ Λ𝑃 the result of FV𝑃 (𝑝) is finite.
    (Extensionality) For all programs 𝑝 ∈ Λ𝑃 and all states 𝜇, 𝜇,˜ 𝜎, 𝜎˜ ∈ S:
                                              ˜ then (𝜇, 𝜎) ∈ P (𝑝) iff ( 𝜇,
                       if 𝜇 ≡Λ𝑉 𝜇˜ and 𝜎 ≡Λ𝑉 𝜎,                              ˜ ∈ P (𝑝)
                                                                          ˜ 𝜎)
   The coverage property establishes that any variable possibly influencing the state transition of
a program 𝑝 must be part of FV𝑃 (𝑝). This is achieved by ensuring that if two states agree on a
superset of FV𝑃 (𝑝), then there must exist “isomorphic” state transitions, i.e. state transitions in
P (𝑝) where the resulting states equally agree on this set of variables. For the remainder of this
paper, it is paramount that this property is not just satisfied for FV𝑃 (𝑝), but also for its supersets to
ensure equivalent effects on any variables written by 𝑝. The second condition ensures that this new
set of free variables is finite, too, which is relevant for central coincidence properties. Finally, the
extensionality property ensures that program behavior is only dependent on variable assignment
and not intensional differences between states which is also relevant for coincidence.
   Recall the dynamic signature from Example 4.1, the program evaluation function for 𝑣 := 𝑡 1
induces a transition relation (𝜇, 𝜎) ∈ P R (𝑣 := 𝑡 1 ) iff 𝜎 (𝑣) = 𝜇 (𝑡 1 ) and 𝜇 ≡ {𝑣 } ∁ 𝜎 where 𝜇 (𝑡 1 ) is the
evaluation of term 𝑡 1 in state 𝜇 (going forward we denote by 𝑉 ∁ the complement set Λ𝑉 \ 𝑉 for
𝑉 ⊆ Λ𝑉 ). FV𝑃 is again obtained via syntactic analyses.
  We summarize the semantics of a dynamic theory as a domain of computation, which together
with its dynamic signature (syntax) fully specifies the theory:
Definition 4.6 (Domain of Computation). Given a dynamic signature Λ, a domain of computation
of Λ (denoted as D = (U, S, V, A, FV𝐴 , P, FV𝑃 )) consists of:
    • A universe U (see Definition 4.3)
    • A corresponding state space S (see Definition 4.3)
    • A variable evaluation function V (see Definition 4.3)
    • An atom evaluation function A and free variable overapproximation FV𝐴 (see Definition 4.4)
    • A program evaluation function P and free variable overapproximation FV𝑃 (see Definition 4.5)
Definition 4.7 (Dynamic Theory). A dynamic theory is the combination of a dynamic signature Λ
and a corresponding domain of computation D. We denote a dynamic theory as Δ = (Λ, D).
The semantics of Λ-formulas (Definition 4.2) for a dynamic theory Δ = (Λ, D) are defined as follows:
Definition 4.8 (Semantics of Formulas). Consider a dynamic theory Δ = (Λ, D). We define the
semantics of Λ-formulas as follows:
            DJ𝑎K = A (𝑎)        DJ¬𝐹 K = S \ DJ𝐹 K             DJ𝐹 ∧ 𝐺K = DJ𝐹 K ∩ DJ𝐺K
                    n                                                    o
         DJ∀𝑣 𝐹 K = 𝜇 ∈ S for all 𝜎 ∈ S : 𝜇 ≡ {𝑣 } ∁ 𝜎 implies 𝜎 ∈ DJ𝐹 K
                    
         DJ[𝑝] 𝐹 K = 𝜇 ∈ S for all 𝜎 ∈ S : (𝜇, 𝜎) ∈ P (𝑝) implies 𝜎 ∈ DJ𝐹 K
   We say 𝐹 is Δ-valid (denoted as |=Δ 𝐹 ) iff every state in S satisfies 𝐹 , i.e. S = DJ𝐹 K. If a particular
state 𝜇 ∈ S satisfies a formula 𝐹 (i.e., 𝜇 ∈ DJ𝐹 K) we denote this as 𝜇 |=Δ 𝐹 and say 𝜇 satisfies 𝐹
or that 𝐹 is Δ-satisfiable. For example, the formula 𝐹 ∧ [𝑝] 𝐺 is true in a state 𝜇 if 𝜇 |=Δ 𝐹 (i.e. 𝜇
satisfies 𝐹 ) and if for every (𝜇, 𝜎) ∈ DJ𝑝K it holds that 𝜎 |=Δ 𝐺 (i.e. every such 𝜎 satisfies 𝐺).
   By now we have instantiated the semantics for the semiring dynamic signature (R, +, ·, ≤) in
Example 4.1. Lemma 4.2 shows that our construction yields a dynamic theory Δ R satisfying all
properties of Definition 4.6. A concrete example for a formula of this theory is Equation (1). Its

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                               217:9


program 𝑤 := 𝑣 + 1 induces a state transition (𝜇, 𝜎) ∈ P Z (𝑤 := 𝑣 + 1) iff 𝜎 (𝑤) = 𝜇 (𝑣 + 1) = 𝜇 (𝑣) + 1
(and 𝜇 ≡ {𝑤 } ∁ 𝜎). It is then easy to see that Equation (1) is indeed valid in ΔZ : For any state with 𝜇 (𝑣) ≥
0 and any state transition to 𝜎 such that 𝜎 (𝑤) = 𝜇 (𝑣)+1 (and otherwise equal) it holds that 𝜎 (𝑤) ≥ 1.
  Relation to classical First-Order Dynamic Logic. The syntax and semantics of classical first-order
dynamic logic [32], are more restrictive in the supported structure of atoms and state spaces. State
spaces are assumed to be simple valuations [32, p. 293] (and not more complex constructs admitting
the evaluation of variables and atoms), and atoms are defined as predicates over terms [32, p. 103].
We demonstrate that axioms and proof rules derivable for classical, interpreted first-order dynamic
logic are equally derivable using our smaller set of assumptions; Moreover, this relaxation, in turn,
has two advantages: (1) The designer of a program logic, formalized as dynamic theory, can focus
on the particularities of the program logic at hand and obtain extensions like regular programs or
havoc operators for free (lifting, see Section 6), (2) Program logics formalized as dynamic theories
can be combined arbitrarily in a manner that admits compositional reasoning (heterogeneous
dynamic theories, see Section 7).

4.3   Static Semantics
For deriving proof rules, we need a precise notion of semantically free and bound variables,
i.e. those that affect or are affected by a formula or program. Definition 4.6 already assumes
overapproximations FV𝐴 and FV𝑃 of these sets that are typically defined syntactically. For example,
in Example 4.1, variables in expressions are considered free, and those on the left of assignments
are bound. Such approximations are not exact: For instance, 𝑥 := 𝑥 + 𝑦 − 𝑦 changes no state and
hence has syntactically, but not semantically, free or bound variables. Exact computation of these
sets is undecidable [55]. As we have no knowledge on atom and program structure, syntactic
approximations are unavailable and we instead adopt the semantic approach from Platzer [49]:
Definition 4.9 (Free and Bound Variables). Let 𝑝 be some program and 𝐹 be some formula over a
dynamic theory Δ = (Λ, D). Free variables FVΔ and bound variables BVΔ are defined as follows:
                    n                                                              o
          FVΔ (𝐹 ) = 𝑣 ∈ Λ𝑉 exists 𝜇, 𝜇˜ ∈ S s.t. 𝜇 ≡ {𝑣 } ∁ 𝜇˜ and 𝜇 ∈ DJ𝐹 K ∌ 𝜇˜
                    n
          FVΔ (𝑝) = 𝑣 ∈ Λ𝑉 exists 𝜇, 𝜇,˜ 𝜎 ∈ S s.t. 𝜇 ≡ {𝑣 } ∁ 𝜇˜ and (𝜇, 𝜎) ∈ P (𝑝)
                                                                                      o
                             but there is no 𝜎˜ s.t. 𝜎 ≡ {𝑣 } ∁ 𝜎˜ and ( 𝜇, ˜ ∈ P (𝑝)
                                                                         ˜ 𝜎)
            BVΔ (𝑝) = {𝑣 ∈ Λ𝑉 | exists 𝜇, 𝜇˜ ∈ S s.t. (𝜇, 𝜇)
                                                          ˜ ∈ P (𝑝) and V (𝜇, 𝑣) ≠ V ( 𝜇,
                                                                                       ˜ 𝑣)}
  We denote VarsΔ (𝑝) = FVΔ (𝑝) ∪ BVΔ (𝑝). Going forward we will only use BVΔ (𝑝) and VarsΔ (𝑝)
which combines both free and bound variables. The definition of free variables breaks down for
atoms depending on an infinite set of variables (e.g., consider some atom that is true iff an infinite
number of variables have value 1). However, we avoid this issue by assuming that FV𝐴 is finite for all
atoms. Note that FV𝐴 (𝑎) and FV𝑃 (𝑝) resp. overapproximate FVΔ (𝑎) and FVΔ (𝑝) (see Lemma C.1).

4.4   Instantiations of Dynamic Theories
We have now introduced an elaborate definition of dynamic theories. While the proof-theoretic value
of these definitions will become clear in the subsequent sections through the derivability of numer-
ous proof rules from the proposed assumptions, we should first examine whether these definitions
are sensible. To this end, we prove that three Dynamic Logics are instantiations of our definitions:
Lemma 4.1 (PDL as Dynamic Theory). Propositional Dynamic Logic over arbitrary atomic programs
and propositional atoms is an instantiation of a dynamic theory.

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:10                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


Lemma 4.2 (Semi-Ring First-Order Dynamic Logic as Dynamic Theory). Consider first-order atoms
(equality and less than) over terms of an ordered semi-ring (e.g. natural numbers, see Example 4.1). The
dynamic logic with programs of the form 𝑣 := 𝑡 where 𝑡 is a term of the semi-ring is an instantiation
of a dynamic theory.

  Proof Sketch. To prove that Semi-Ring First-Order Dynamic Logic is a dynamic theory, we
prove that the state space, variables, atom and program evaluation, and their respective free
variable definitions (see Example 4.1) satisfy the six requirements from Definitions 4.3 to 4.5. As
this logic’s state space is the set of all (unique) variable to universe mappings, S Independence
and Extensionality is trivially satisfied. FV𝐴 Coverage and FV𝑃 Coverage can be achieved by
constructing FV𝐴 and FV𝑃 as sound syntactical analyses. FV𝐴 Finite and FV𝑃 Finite are achieved
through the syntactic construction of atoms/programs which only touch a finite set of variables. □

Lemma 4.3 (Differential Dynamic Logic as Dynamic Theory). The variables, atoms, and programs of
Differential Dynamic Logic as formalized in the Archive of Formal Proofs [12] form a dynamic theory.

  Consequently, all proof rules and results described below hold for these three dynamic theories.
While the logic from Lemma 4.2 might at first seem overly simplistic, we show in Section 6 that we
can lift this theory to support a wider range of programs. As discussed in Section 1, this paper is
not only about existing dynamic theories, but also about the ability to construct further dynamic
theories which are, by design, interoperable with the collection of existing dynamic theories.

4.5 Proof Calculi
From a program verification perspective, the objective of dynamic logics, and dynamic theories,
is to prove that a program 𝑝 satisfies formalized (functional) properties. For example, we might
want to verify that for all inputs satisfying 𝐹 , the program 𝑝 satisfies the postcondition 𝐺. From a
proof-theoretic perspective this corresponds to proving that dynamic theory formula 𝐹 → [𝑝] 𝐺 is
Δ-valid, i.e. that |=Δ 𝐹 → [𝑝] 𝐺. This is usually achieved by proof calculi that, from axioms and
proof rules, derive that a certain formula is valid.
   For the purpose of this work, we consider a calculus to be a relation ⊢Δ ∈ 2FmlΛ × FmlΛ where
(Γ, 𝐹 ) ∈ ⊢Δ (denoted Γ ⊢Δ 𝐹 or ⊢Δ 𝐹 iff Γ = ∅) iff 𝐹 can be derived from Γ using the proof rules and
axioms of the calculus ⊢Δ . We are only interested in sound proof calculi:

Definition 4.10 (Sound Calculus). For a dynamic theory Δ a proof calculus ⊢Δ is called sound iff for
all formulas 𝐹 ∈ FmlΛ it holds that ⊢Δ 𝐹 implies |=Δ 𝐹 .

  Soundness is a compositional property, i.e. a proof calculus is sound if all proof rules are sound
and all instantiations of axioms are valid. Soundness is thus an inductive consequence of the
soundness of individual calculus steps, because the calculus iteratively generates (valid) axiom
instantiations and applies (sound) proof rules. As common in dynamic logics [9, 50, 67] and their
practical implementations [2, 25], the remainder of this work assumes that all (elementary) dynamic
theories Δ are equipped with a sound proof calculus ⊢Δ that is complete w.r.t. propositional and
uninterpreted first-order reasoning (e.g., by extending the Hilbert or Sequent calculus). Section 5
extends this calculus with additional proof rules that hold independently of a particular dynamic
theory. Sections 6 and 7 extend and combine dynamic theories and provide sound calculi building on
the given calculus for Δ. This approach guarantees compositionality. Although our theories become
more expressive as we lift and merge them with the proposed constructs, we can nonetheless reuse
the calculus ⊢Δ of the original theory.

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:11


            ⊢Δ 𝜙                             (V) 𝜙 → [𝛼] 𝜙                 (FVΔ (𝜙) ∩ BVΔ (𝛼) = ∅)
      (G)
          ⊢Δ [𝛼] 𝜙                           (B) (∀𝑣 [𝛼] 𝜙) ↔ ( [𝛼] ∀𝑣 𝜙)           (𝑣 ∉ VarsΔ (𝛼))
      (E) [𝛼] 𝜙 ↔ [𝛽] 𝜙       (𝛼  𝛽)        (K) ( [𝛼] (𝜙 → 𝜓 )) → ( [𝛼] 𝜙 → [𝛼] 𝜓 )

                      Fig. 2. Elementary axioms and proof rules for dynamic theories


  Equational Reasoning. In addition to proof rule based reasoning, our approach also supports
reasoning via a refinement [42] and an equivalence relations between programs which can be
proven via syntactic rewriting using techniques from Kleene Algebra with Tests [40] (KAT):
Definition 4.11 (Refinement and Equivalence). A program 𝑝 refines 𝑞 (denoted as 𝑝 ≲ 𝑞) iff for all
(𝜇, 𝜎) ∈ P (𝑝) it holds that (𝜇, 𝜎) ∈ P (𝑞). Programs are equivalent (𝑝  𝑞) iff 𝑝 ≲ 𝑞 and 𝑞 ≲ 𝑝.

5   Elementary Results and Proof Rules for Dynamic Theories
Concerning the semantic definitions of free and bound variables, we observe that the definitions
from Definition 4.9 exactly characterize the variables determining the valuation of a formula as well
as the variables changed by the program. All three definitions come with a minimality guarantee
that ensures we are not overly conservative in our estimation of which variables impact valuations:
Lemma 5.1 (Coincidence Lemma for Formulas & Minimality). Given a dynamic theory Δ and
formula 𝐹 define 𝑉 = FVΔ (𝐹 ). Then 𝐹 has the same truth value in any two states agreeing on 𝑉 (i.e., if
S ∋ 𝜇 ≡𝑉 𝜇˜ ∈ S then 𝜇 ∈ DJ𝐹 K iff 𝜇˜ ∈ DJ𝐹 K). 𝑉 is the smallest set with this coincidence property.
Lemma 5.2 (Coincidence Lemma for Programs & Minimality). Given a dynamic theory Δ with
program 𝑝 consider some 𝑉 ⊇ FVΔ (𝑝). If for states 𝜇, 𝜎 ∈ S only differing on a finite set of variables
(i.e., {𝑣 ∈ Λ𝑉 | V (𝜇, 𝑣) ≠ V (𝜎, 𝑣)} is finite) it holds that 𝜇 ≡𝑉 𝜎 and (𝜇, 𝜇)
                                                                              ˜ ∈ P (𝑝), then there exists
a 𝜎˜ ∈ S such that (𝜎, 𝜎)˜ ∈ P (𝑝) and 𝜇˜ ≡𝑉 𝜎. ˜ FVΔ (𝑝) is the smallest set with this property.
Lemma 5.3 (Bounded Effect & Minimality). Given a dynamic theory Δ and a program 𝑝 define
𝑉 = BVΔ (𝑝). For all (𝜇, 𝜎) ∈ P (𝑝) it holds that 𝜇 ≡𝑉 ∁ 𝜎. 𝑉 is the smallest set with this property.
   We will now derive Hilbert-style proof calculus rules (extending the usual first-order axioms)
which hold independently of any particular dynamic theory. In particular, these rules also hold
for combined, heterogeneous dynamic theories (see Section 7). Since we do not know the inner
workings of programs 𝑝 ∈ Λ𝑃 it is the obligation of the designer of a dynamic theory to provide
a suitable calculus to decompose and prove statements about such atomic programs. However, we
can nonetheless provide calculus rules that hold independently of the concrete programs. A first set
of these axioms and rules can be found in Figure 2. These rules will be extended in the subsequent
section by calculus rules for reasoning about the closure of regular programs over the programs
in Λ𝑃 . By providing our calculus rules, we propose a compositional calculus. The theory designer
can focus on proof procedures for statements about (from our perspective) atomic programs, while
our rules provide the general, compositional principles that are independent of the particular
programming language at hand. To this end, we formalize the soundness of the described axioms:
Theorem 5.1 (Soundness of Elementary Proof Rules). The proof rules and axioms in Figure 2 are
sound w.r.t. to any dynamic theory Δ.
   The proof rule (G) and the axiom (V) are akin to first-order Hilbert-calculus generalization rules
by allowing us to wrap formulas into modalities. Barcan’s axiom (B) encodes a constant domain
property for the dynamic theory’s state space that emerges from the state space properties outlined
in Section 4. (V) allows us to eliminate programs that do not affect the postcondition while axiom

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:12                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


(K) allows distributing modalities across implications. Finally, (E) allows us to swap programs in
modalities for equivalent programs. As described in Theorem 5.1, we can prove the soundness of these
axioms independently of the considered state space, atomic formulas, and programs. While Figure 2
presents the axioms as requiring semantic side conditions, these can be discharged via syntactic
algorithms. For example, the sets FVΔ and BVΔ can be over-approximated using syntactic analyses
(e.g., Definition 4.5 establishes an overapproximation of FVΔ for programs) Equivalence results (𝛼 
𝛽) can be obtained using sound KAT [40] rewriting rules or natively within dynamic logic [42, Sec. 7].

6     Lifting Dynamic Theories
In this section, we demonstrate, for the first time, the power of the concise formalization of necessary
properties for the construction of a dynamic theory. Given a dynamic theory Δ, we can extend its
functionality, e.g., by extending the structure of state spaces, atoms, or programs, with common
constructs. By proving that this extension again satisfies the properties outlined in Section 4, all
properties, proof rules, and axioms are lifted to the extended, more expressive, dynamic theory.
Similarly to conservative extensions in first-order theory, our lifting ensures that previously valid
axioms and formulas remain sound. Unlike conservative extensions, some liftings of dynamic
theories meaningfully extend the expressiveness of the logic’s programming language beyond the
original theory’s expressiveness by allowing new state transitions that were previously impossible.
The most prominent example of this is the introduction of loops in Section 6.2 which lifts a theory
to its regular closure over programs. Before discussing regular closures, we first propose a lifting
which does not increase expressivity but serves as a gentle introduction of all concepts reused later.
To this end we extend a dynamic theory by the havoc operator 𝑣 := ∗ which assigns the variable 𝑣
to an arbitrary value (Section 6.1)

6.1      Havoc Operator Lifting
On a syntactical level, lifting a dynamic theory Δ to a new dynamic theory Δ:=∗ amounts to
enhancing the original set of programs Λ𝑃 with the havoc operator on all variables in Λ𝑉 , i.e.
Λ:=∗
 𝑃 = Λ𝑃 ∪ {𝑣 = ∗ | 𝑣 ∈ Λ𝑉 }. We can similarly extend Δ’s domain of computation D. Overall, this
         ¤    :
amounts to the following lifting operation (·) :=∗ (where ∪¤ is the disjoint union):
Definition 6.1 (Havoc Lift). Given a dynamic theory Δ we define Δ:=∗ = (Λ:=∗, D :=∗ ) such that all
components of Δ and Δ:=∗ are equal except for:
      • Λ:=∗
         𝑃 = Λ𝑃 ∪ {𝑣 = ∗ | 𝑣 ∈ Λ𝑉 }
                      ¤     :                                                • FV𝑃:=∗ (𝑝) = FV𝑃 (𝑝) (for 𝑝 ∈ Λ𝑃 )
      • P :=∗ (𝑝) = P (𝑝)n (for 𝑝 ∈ Λ𝑃 )           o                         • FV𝑃:=∗ (𝑣 := ∗) = ∅ (for 𝑣 ∈ Λ𝑉 )
      • P :=∗ (𝑣 := ∗) = (𝜇, 𝜎) ∈ S 2 𝜇 ≡ {𝑣 } ∁ 𝜎            (𝑣 ∈ Λ𝑉 )

Note that 𝑣 is not free in 𝑣 := ∗ as its value does not influence the program’s reachable states. We
prove that the havoc lift Δ:=∗ of a dynamic theory Δ satisfies all properties of a dynamic theory:
Theorem 6.1 (Havoc Lifted Dynamic Theories). The havoc lift Δ:=∗ of any dynamic theory Δ is a
dynamic theory.
  For first-order atoms (Λ𝐴 ) and the state space (S), the required properties for a dynamic theory
are still satisfied, because we did not modify these components. For programs, we ensured that
our semantic definition of havoc satisfies the properties asserted in Definition 4.5. While it is
advantageous that the properties proven for arbitrary dynamic theories carry over from Δ to Δ:=∗ ,
the havoc lifting would be useless if properties of the specific theory Δ under consideration would
not carry over as well. If this were the case, all properties proven for a Δ under consideration would
have to be reproved for Δ:=∗ and the lifting operation would lose its utility. Fortunately, our new

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:13


set of formulas is a superset of the original formulas, i.e. FmlΛ ⊆ FmlΛ:=∗ . This raises the question
of whether their semantics also carry over. Indeed, we can prove a calculus rule which translates
proofs about Δ into proofs about Δ:=∗ :
Lemma 6.1 (Havoc Reduction). For any dynamic theory Δ, the following proof rule is sound:
                                            ⊢Δ 𝜙
                                    (HR)           (assuming 𝜙 ∈ FmlΛ )
                                           ⊢Δ:=∗ 𝜙
   Hence, we can reuse any decision procedure developed for determining the validity of formulas
in FmlΛ to determine the validity of formulas in the havoc-free fragment of FmlΛ:=∗ and carry these
results over using (HR). Additionally, we prove the soundness of the well-known (:=∗) axiom for
the decomposition of the havoc operator:
Lemma 6.2 (Havoc Axiom). For any dynamic theory Δ, the following axiom is sound in Δ:=∗ :
  (:=∗) ( [𝑣 := ∗] 𝜙) ↔ (∀𝑣 𝜙)
   Before we move to regular programs, let us recap what this section demonstrated. Given any
dynamic theory Δ, we can create a new dynamic theory Δ:=∗ which: (1) Has the additional program
primitive 𝑣 := ∗; (2) Inherits the dynamic theory axioms (G), (V), (B) and (K); (3) Allows reuse
of existing proof infrastructure for Δ through (HR) (as a valid formula of Δ is also valid in Δ:=∗ ).
Rule (HR) enables this reuse even when Δ’s axiom schemata may not hold for arbitrary Δ:=∗ -
instantiations, by restricting reductions to formulas from FmlΛ . The remainder of this section, as
well as Section 7, will demonstrate significantly more expressive lifting procedures with the same
properties, i.e. transfer of proof rules and validity preservation.
Example 6.1. Continuing the example of a dynamic theory over a semi-ring Δ R defined in
Example 4.1, we can lift Δ R with havoc resulting in Δ R . Beyond programs 𝑥 := 𝑡 (for semiring
                                                               :=∗

terms 𝑡) the theory Δ R
                              :=∗
                                   then also supports programs 𝑥 := ∗. While this does not increase
expressivity (see axiom   ( :=∗)), it can increase expressivity when combined with the regular closure
defined below. Δ R        also admits the application of all proof principles from Δ R via (HR).
                     :=∗

6.2   Regular Program Lifting
Given a set of (atomic) programs, it is often useful to consider their regular programs closure, i.e., any
construction of programs obtained by sequential composition, nondeterministic choice, (first-order
logic) checks, and nondeterministic loops. This is an interesting set of programs, because it allows
constructing well-known imperative constructs such as if or while, from a small set of operations.
It is also isomorphic to the program constructs considered in Kleene Algebra with Tests [40]. We
now show that any dynamic theory Δ can be lifted to this more expressive set of programs while
retaining the properties established above. To this end, we begin by defining the regular closure of
programs along with their semantics:
Definition 6.2 (Regular Closure). Given a dynamic theory Δ over programs Λ𝑃 with program
evaluation function P we define the regular closure of programs, denoted Λ𝑃 via the following
                                                                                  reg

grammar (where 𝑟 ∈ Λ𝑃 and 𝐹 FOL ∈ FOLΛ ): 𝑝, 𝑞 F 𝑟 𝑝; 𝑞 𝑝 ∪ 𝑞 ? (𝐹 FOL ) (𝑝) ∗ .
We then lift the program evaluation function to P reg as follows:
    • P reg (𝑟 ) = P (𝑟 ) (for 𝑟 ∈ Λ𝑃 )
    • P reg (𝑝; 𝑞) = (𝜇, 𝜔) ∈ S 2 there exists 𝜎 ∈ S s.t. (𝜇, 𝜎) ∈ P reg (𝑝) and (𝜎, 𝜔) ∈ P reg (𝑞)
    • P reg (𝑝 ∪ 𝑞) = P reg   (𝑝) ∪ P (𝑞)
                                       reg

    • P reg (? (𝐹 FOL )) = (𝜇, 𝜎) ∈ S 𝜇 ∈ DJ𝐹 FOL K and 𝜇 ≡Λ𝑉 𝜎
    • P reg (𝑝) ∗ = 𝑛∈N P reg (𝑝 𝑛 ) where 𝑝 0 ≡ ? (⊤) and 𝑝 𝑛+1 ≡ (𝑝; 𝑝 𝑛 )
                    Ð


                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:14                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


         (?) [? (𝜙)] 𝜓 ↔ (𝜙 → 𝜓 )                         (∪)    [𝛼 ∪ 𝛽] 𝜙 ↔ [𝛼] 𝜙 ∧ [𝛽] 𝜙
          (;) [𝛼; 𝛽] 𝜙 ↔ [𝛼] [𝛽] 𝜙                        (I)    [𝛼 ∗ ] (𝜙 → [𝛼] 𝜙) → (𝜙 → [𝛼 ∗ ] 𝜙)
         (∗ ) [𝛼 ∗ ] 𝜙 ↔ 𝜙 ∧ [𝛼] [𝛼 ∗ ] 𝜙

                      Fig. 3. Axioms for regular programs originally due to Segerberg [60]

                                                                                                       reg
   To create a new dynamic theory, it remains to define the set of free variables FV𝑃 . To this
end, the free variables for 𝑟 ∈ Λ𝑃 are defined as FV𝑃 (𝑟 ), and the free variables under sequential
composition and nondeterministic choice are defined as the union of their components. The free
variables of a looped program (𝑝) ∗ are the free variables of 𝑝. For the check ? (𝐹 FOL ) we leverage
our knowledge about the free variables of atoms (encoded in FV𝐴 ) to construct the free variables of
a first-order formula (see Definition C.1). Note that popular definitions of ? (𝐹 FOL ) often enforce
semantics where it must be the case that 𝜇 = 𝜎 while we allow transitions to equivalent states as
the usual definition breaks our extensionality assumption in Definition 4.5 (since we allow distinct
states 𝜇, 𝜎 ∈ S such that 𝜇 ≡Λ𝑉 𝜎). This particularity disappears if we assume S to be a “classical”
mapping from variables to values. We can then formally define the regular closure lift and prove
that it constructs once again a dynamic theory:
Definition 6.3 (Regular Closure Lift). For a dynamic theory Δ and its regular closure over programs
Λ𝑃 , P reg (see Definition 6.2) and FV𝑃 as defined in Definition C.2, the regular closure lift is defined as:
 reg                                  reg


                        Δreg = Λ𝑉 , Λ𝐴 , Λ𝑃 , U, S, V, A, FV𝐴 , P reg, FV𝑃
                                           reg                               reg  


Theorem 6.2 (Regular Closure over Dynamic Theory). The regular closure lift Δreg of any dynamic
theory Δ is a dynamic theory.
  Just as before, we can define a reduction rule which allows us to reuse proof results in Δreg
that have already been shown for Δ. Additionally, our lifting comes with numerous axioms on the
decomposition of regular programs which we summarize in Figure 3 and are provably sound:
Lemma 6.3 (Regular Reduction). For any dynamic theory Δ, the following proof rule is sound:
                                                ⊢Δ 𝜙
                                       (RR)            (assuming 𝜙 ∈ FmlΛ )
                                               ⊢Δreg 𝜙
Theorem 6.3 (Soundness of Proof Rules over Regular Closure). For any dynamic theory Δ the
axioms in Figure 3 are sound in Δreg .
  The proof rules provided in Figure 3 allow us to decompose checks, sequential compositions
and nondeterminstic choice programs (see axioms (?), (;), (∪)). Moreover, they allow the iterative
decomposition of loops as well as inductive invariant reasoning about loops (see axioms (∗ ), (I)).
However, the axioms are, yet, insufficient for loop termination.
    Loop Convergence. A significant strength of dynamic logics, and hence dynamic theories, is their
ability to reason about partial and total correctness via the dual diamond and box modalities. To
this end, it is sometimes necessary to not only reason about loop invariants (via (I)), but also about
loop variants to prove progress. To this end, consider a formula ⟨𝑝 ∗ ⟩ 𝐹 . In this instance, we must
prove that running program 𝑝 in a loop eventually leads to a state satisfying 𝐹 . This is usually
achieved via well-founded induction proofs. Given a formula 𝜙 (𝑁 ) that is satisfied for a sufficiently
large 𝑁 ∈ N, one iteration of 𝑝 ensures that 𝜙 (𝑁 − 1) is satisfied in the post state. If 𝜙 (0) implies
𝐹 , this proves that 𝐹 becomes satisfied after iteratively running 𝑝 for a sufficiently large number
of steps. This requires counting. However, due to the generality of our assumed state space, we

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:15


currently have no way of counting or performing well-founded induction. Hence, we now propose
a set of additional assumptions that allow us to introduce a loop termination rule:
Definition 6.4 (Inductive Expressivity). Given some dynamic theory Δ, assume some function
N : U → N mapping elements from the universe to natural numbers. We say a variable 𝑣 ∈ Λ𝑉 is
integer expressive w.r.t. N iff for all 𝑛 ∈ N there exists a state 𝜇 ∈ S such that N (V (𝜇, 𝑣)) = 𝑛. Let
Λ𝑉 N be a set of such variables. We say Δ has inductive expressivity iff for some given N there exist
two functions nat+1, nat= : Λ𝑉2 N → FOLΛ and one function nat>0 : Λ𝑉 N → FOLΛ such that:
     (Positive Sound) For any variable 𝑣 ∈ Λ𝑉 N and any state 𝜇 ∈ S:
                           𝜇 ∈ DJnat>0 (𝑣)K iff N (V (𝜇, 𝑣)) > 0
        (Eqal Sound) For variables 𝑣, 𝑤 ∈ Λ𝑉 N with 𝑣 ≠ 𝑤 and any state 𝜇 ∈ S:
                           𝜇 ∈ DJnat= (𝑣, 𝑤)K iff N (V (𝜇, 𝑣)) = N (V (𝜇, 𝑤))
    (Plus One Sound) For variables 𝑣, 𝑤 ∈ Λ𝑉 N with 𝑣 ≠ 𝑤 and any state 𝜇 ∈ S:
                           𝜇 ∈ DJnat+1 (𝑣, 𝑤)K iff N (V (𝜇, 𝑣)) + 1 = N (V (𝜇, 𝑤))
   This inductive expressivity yields all that is required to prove loop convergence, which enables us
to prove loop termination and reachability of certain states via loop iteration. To this end, dynamic
logics usually are equipped with a proof rule [31] or axiom [51] that looks something like this:
    [𝑝 ∗ ] (∀𝑣 ((𝑣 > 0 ∧ 𝜙 (𝑣)) → ⟨𝑝⟩ 𝜙 (𝑣 − 1))) → ∀𝑣 (𝜙 (𝑣) → ⟨𝑝 ∗ ⟩ 𝜙 (0))                 (𝑣 ∉ Vars (𝑝))
This axiom formalizes the well-founded induction argument outlined above: If 𝜙 (𝑣) is satisfied
and one iteration of 𝑝 allows us to reach a state satisfying 𝜙 (𝑣 − 1), then we can reach a state with
𝜙 (0) by iterating the execution of 𝑝 (assuming 𝑣 is a natural number). To prove loop reachability
properties, we also want an axiom like this one in the regular closure over our dynamic theory;
however, we lack any means to parameterize formulas with specific variables. After all, our theory
so far makes no assumptions about how atomic formulas in Λ𝐴 evaluate w.r.t. variables beyond the
definition of FV𝐴 . Hence, we derive the following axiom which can be proven independently of the
dynamic theory at hand so long as the properties from Definition 6.4 are given:
Lemma 6.4 (Loop Convergence Rule). For any inductively expressive dynamic theory Δ, the following
axiom is sound for its regular closure Δreg for any integer expressive distinct variables 𝑣, 𝑤 ∈ Λ𝑉 N
with 𝑤 ∉ FVΔ (𝜙) and 𝑣, 𝑤 ∉ Vars (𝑝):
         ( [𝑝 ∗ ] (∀𝑣 ((nat>0 (𝑣) ∧ 𝜙) → ⟨𝑝⟩ (∀𝑤 (nat+1 (𝑤, 𝑣) → ∀𝑣 (nat= (𝑣, 𝑤) → 𝜙))))))
    (C)
         → (∀𝑣 (𝜙 → ⟨𝑝 ∗ ⟩ (∃𝑣 (¬nat>0 (𝑣) ∧ 𝜙))))
   Note that once we apply nat+1, nat= or nat>0 to concrete variables, they reduce to a concrete
Δ-formula yielding a concrete instantiation of axiom (𝐶). Importantly, we cannot subtract from
𝑣 within a single predicate since any predicate (including nat+1 ) requires a reference point from
which to subtract 1. We mitigate this by employing the helper variable 𝑤. To demonstrate the utility
of the additional assumptions, we have also proven that a concrete Dynamic Logic instantiates the
properties defined in Definition 6.4:
Lemma 6.5 (Semi-Ring First-Order Dynamic Logic over Natural Numbers). The semi-ring dynamic
theory Δ R , instantiated for natural numbers or integers (resp. ΔN or ΔZ ), isinductively expressive.
                                                                             :=∗ reg            :=∗  reg
Hence, axiom (C) is a sound axiom for its havoc lifted, regular closure Δ N           (resp. ΔZ             ).

Example 6.2 (Regular Program Lifting for Ordered Semiring). We reconsider the example of a
dynamic logic over an ordered semiring (R, +, ·, ≤) for R = Z: As seen in Lemma 6.5, this dynamic
theory is inductively expressive. Hence, all axioms derived up to this
                                                                      point      (Figures 2 and 3 as well
                                                                           :=∗  reg
as (HR), (RR), (:=∗), (C)) apply to its havoc lifted, regular closure Δ Z             . From a very simple

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:16                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


definition of assignment, we have thus derived a dynamic theory with full support for regular
programs and nondeterministic assignment. For example, the following program is part of this
dynamic theory:
                                                            ∗              
   1 ≤ 𝑛 → 𝑥 := 0; 𝑖 := 0; ? (𝑖 ≤ 𝑛) ; 𝑥 := 𝑥 + 𝑖; 𝑖 := 𝑖 + 1 ; ? (¬ (𝑖 ≤ 𝑛)) 2 ∗ 𝑥 ≤ 𝑛 ∗ (𝑛 + 1) (2)
This formula asserts that x is no larger than the Gauss formula predicts after summing up the first
𝑛 integers. Based on our simple definitions in Example           4.1 we can now perform reasoning about
                                                           :=∗  reg
programs like the one in Equation (2). In fact, ΔZ                     provides the equivalent of a guarded
command language over integers and, as will be shown in Section 8, a relatively complete proof
calculus for it. In fact, our initial definition of ΔZ even could have omitted the assignment programs
(by initializing ΛZ𝑃 = ∅) by defining assignment as syntactic sugar for havoc and check [1]:
         𝑣 := 𝑡 ≡ (𝑤 := ∗; ? (𝑡 ≤ 𝑤 ∧ 𝑤 ≤ 𝑡) ; 𝑣 := ∗; ? (𝑣 ≤ 𝑤 ∧ 𝑤 ≤ 𝑣))                for 𝑤 ∈ Λ𝑉Z fresh
  Kleene Algebra with Tests. We prove that our regular closure lifting forms a Kleene Algebra with
Test [32, 40] over the theory’s programs (see Theorem C.1). In combination with axiom (E), this
enables KAT-style rewriting within dynamic logics.

7     Heterogeneous Dynamic Theories
We enhance dynamic theories further by allowing combination of multiple theories to reason about
heterogeneous systems, whose components operate on different domains of computation, but may
interact. Heterogeneous theories serve two purposes: (1) they provide a unified framework that
explicitly models both systems and their interactions, and (2) they enable rigorous reasoning about
the overall system by reusing results and proof calculi from the homogeneous component theories.
The heterogeneous proof calculus decomposes obligations to the individual theories, analogous to
how reasoning over regular programs reduces to reasoning over atomic programs.
   Given two theories Δ (0) , Δ (1) , we first construct a simple heterogeneous theory Δ (01) over Λ𝑃(0) ∪
Λ𝑃(1) , then lift it with havoc and regular closure. The resulting fully heterogeneous dynamic theory Δ̂
provides an expressive logic combining Δ (0) and Δ (1) with all axioms from Sections 5 and 6 included.

7.1      Simple Heterogeneous Dynamic Theories
We assume we are given two dynamic theories Δ (0) , Δ (1) and begin by defining the state space of
our new dynamic theory:
Definition 7.1 (Heterogeneous State Space). Given two dynamic theories Δ (0) , Δ (1) and their resp.
state spaces S (0) , S (1) we define the heterogeneous state space as Ŝ = S (0) × S (1) . For a given state
 𝜇 (0) , 𝜇 (1) ∈ Ŝ variable evaluation is defined as follows:
              
                                                    (
                                                      V (0) 𝜇 (0) , 𝑣 𝑣 ∈ Λ𝑉(0)
                                                                 
                                     (0) (1)
                              V̂ 𝜇 , 𝜇        ,𝑣 =
                                                      V (1) 𝜇 (1) , 𝑣 𝑣 ∈ Λ𝑉(1)
                                                                     

   A priori, the behavior modeled in Δ (0) and Δ (1) hence happens in isolation. However, similarly
to reasoning about concurrent systems, the appeal of reasoning about heterogeneous systems lies
precisely in the interaction of these a priori independent behaviors. Hence, to relate the behavior of
these two independent state space components, we introduce a new set of atoms (denoted Λ𝐴      ∩ ) that

allows us to constrain permissible combinations of individual states 𝜇 (0) and 𝜇 (1) :
Definition 7.2 (Heterogeneous Atoms). Given two dynamic theories Δ (0) , Δ (1) and their heteroge-
                                                                 ∩ over variables Λ∩ = Λ (0) ∪ Λ (1)
neous state space Ŝ we define a new set of heterogeneous atoms Λ𝐴                 𝑉    𝑉       𝑉

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                                      217:17


with an evaluation function A ∩ : Λ𝐴 ∩ → 2 Ŝ and a free variable function FV∩ : Λ∩ → 2Λ𝑉 such that               ∩
                                                                             𝐴    𝐴
the constructs satisfy the atom evaluation requirements from Definition 4.4.
   Heterogeneous atoms can be considered the dynamic theory counterpart to mixed terms in
first-order theory combination. Just like in the case of first-order theory combination, these terms
allow us to constrain the relation between values in both worlds. As a concrete example, Section 9
defines the heterogeneous atom round(v, w) for JavaDL integer variables v and real-valued 𝑑L
variables w. Its semantics will allow us to constrain the possible values of the Java variable v (in
state 𝜇 (0) ) based on the values of the 𝑑L variable w (in 𝜇 (1) ). In combination with havoc (𝑥 := ∗) and
checks (? (𝐹 FOL )), heterogeneous atoms serve as communication primitives between languages.
   A simple heterogeneous dynamic theory is then defined as follows:
Definition 7.3 (Simple Heterogeneous Dynamic Signature). Given two dynamic theories Δ (0) , Δ (1)
with resp. signatures Λ (0) , Λ (1) and a set of heterogeneous atoms Λ𝐴
                                                                      ∩ over Δ (0) , Δ (1) (see Definition 7.2)
                                                                                          
we define the simple heterogeneous dynamic signature as Λ (01) = Λˆ𝑉 , Λˆ𝐴 , Λ (01) with:             𝑃


            Λˆ𝑉 = Λ𝑉(0) ∪Λ
                        ¤ 𝑉(1)              Λˆ𝐴 = Λ𝐴(0) ∪Λ
                                                        ¤ 𝐴(1) ∪Λ
                                                               ¤ 𝐴∩
                                                                                          Λ𝑃(01) = Λ𝑃(0) ∪Λ
                                                                                                         ¤ 𝑃(1)
  The domain of computation, i.e. the heterogeneous theory’s semantics, naturally follows:
Definition 7.4 (Simple Heterogeneous Domain of Computation). Given two dynamic theories
Δ (0) , Δ (1) and notation as in Definition 7.3 we define the simple heterogeneous domain of computation
D (01) as follows:
    • The universe is the combination of individual universes: Û = U (0) ∪ U (1)
    • The state space is the heterogeneous state space Ŝ over Δ (0) , Δ (1) with the corresponding variable
      evaluation function V̂ (see Definition 7.1)
    • The atom evaluation function Â and program evaluation function P (01) is given as below (with
      corresponding free variable functions FVˆ 𝐴 , FV𝑃(01) as defined in Definition C.4).
                    A (0) (𝑎) × S (1)      𝑎 ∈ Λ𝐴(0)                                 (
                                                                                          P (0) (𝑝)       𝑝 ∈ Λ𝑃(0)
                   
                   
                                            𝑎 ∈ Λ𝐴(1)                  (01)
                   
                   
           Â (𝑎) = S (0) × A (1) (𝑎)                              P          (𝑝) =
                                                                                          P (1) (𝑝)       𝑝 ∈ Λ𝑃(1)
                                            𝑎 ∈ Λ𝐴
                   
                    A ∩ (𝑎)
                                                ∩
                   
    The notation of our simple heterogeneous signature Λ (01) and the simple heterogeneous dynamic
theory D (01) is already giving a hint at the components of the dynamic theory which are here to stay
for the fully heterogeneous version (denoted with (·))ˆ vs. components of the simple heterogeneous
theory that still require further refinement (denoted with (·) (01) ): While the universe, state space,
variables and atoms remain as-is, the range of admissible programs will still be extended. Before we
lift Δ (01) to a more expressive set of programs, we begin by showing that our simple heterogeneous
dynamic signature and domain of computation indeed form a dynamic theory:
Theorem 7.1 (Simple Heterogeneous Dynamic Theories). Assume two dynamic theories Δ (0) , Δ (1)
and a corresponding set of heterogeneous atoms Λ𝐴 ∩ , then Λ (01) and D (01) as defined in Definitions 7.3

and 7.4 form a dynamic theory Δ    (01) as defined in Definition 4.7. The soundness of all axioms and
proof rules from Figure 2 carries over.
This result unlocks the first four proof rules for Δ (01) . However, the range of properties we will be
able to formalize and prove with Δ (01) is still underwhelming as modalities in Δ (01) can only contain
a program from Δ (0) or a program from Δ (1) — not both. Before we lift this limitation in the next
section, we consider how this logic relates to another technique for combining logics, namely fibring.

                                 Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:18                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


   Relation to Fibring. By explicitly labeling the modalities w.r.t. the contained program (i.e. [𝑝] 𝐹
becomes [𝑝] (0) 𝐹 for 𝑝 ∈ Λ𝑃(0) and [𝑝] (1) 𝐹 otherwise), we can interpret this logic as a “multi-
dynamic logic” with two distinct modal operators. This approximately corresponds to what could
be achieved via fibring [27] of dynamic logics where we could combine the truth bearing entities of
Δ (0) and Δ (1) . As fibring does not recognize programs as first-class citizens, it cannot integrate
their respective program constructs which restricts the expressive power of analyzable systems.
In particular, it cannot capture systems involving, e.g., intricate control structures such as loops.
Instead, fibring is confined to modeling systems that can be decomposed into a (nondeterministic)
finite, sequential compositions of homogeneous subsystems. Importantly, our dynamic theory does
not have two distinct modalities. This key difference allows us to apply the lifting procedures
devised in Section 6 which naturally yields a significantly more expressive program logic.

7.2      Fully Heterogeneous Dynamic Theories
Using the lifting procedures from Section 6 we can define the fully heterogeneous dynamic theory,
supporting the composition of homogeneous programs using all regular program constructs, in a
straightforward manner:
Definition 7.5 (Fully Heterogeneous Dynamic Theories). Given two dynamic theories Δ (0) , Δ (1)
and a corresponding set of heterogeneous atoms Λ𝐴∩ forming the simple heterogeneous dynamic theory
                                                                                            :=∗  reg
Δ (01) , we define the fully heterogeneous dynamic theory over Δ (0) , Δ (1) as Δ̂ = Δ (01)             with
(·) reg and (·) :=∗ as given in Theorem 6.1 and Theorem 6.2.
  As planned, we can recover all axioms established above (with the exception of (C) for which the
requirements will be discussed below):
Theorem 7.2 (Fully Heterogeneous Dynamic Theories). Given two dynamic theories Δ (0) , Δ (1) and
a corresponding set of heterogeneous atoms Λ𝐴
                                            ∩ the fully heterogeneous dynamic theory Δ̂ is a dynamic

theory. Proof rules and axioms from Figure 3 as well as axioms (HR), (:=∗), and (RR) carry over to Δ̂.
   Just as for the regular closure over programs of one dynamic theory, the construction of a
heterogeneous dynamic theory over two theories would be entirely devoid of purpose if validity
wouldn’t carry over from the individual logics to the combined one. Fortunately, we can show that
for any pure Λ (0) /Λ (1) -formula the validity w.r.t. Δ (0) /Δ (1) entails the validity w.r.t. Δ̂:
Lemma 7.1 (Heterogeneous Reduction). For any fully heterogeneous dynamic theory Δ̂ over arbi-
trary Δ (0) , Δ (1) the following proof rules are sound:
                 ⊢ (0) 𝜙                                       ⊢ (1) 𝜙
      (HR0) Δ              (assuming 𝜙 ∈ FmlΛ (0) )      (HR1) Δ       (assuming 𝜙 ∈ FmlΛ (1) )
                   ⊢Δ̂ 𝜙                                        ⊢Δ̂ 𝜙
  Loop Convergence. In order for the loop convergence rule to carry over as well, we require that
our heterogeneous dynamic theory Δ̂ is inductively expressive. To this end, we note that whenever
one of the homogeneous dynamic theories Δ (0) , Δ (1) is inductive, then the heterogeneous dynamic
theory is inductive as well:
Lemma 7.2 (Inductive Expressivity of Δ̂). Let Δ (0) be inductively expressive, then there exists a
(constructive) adjusted function N̂ such that Δ̂ is inductively expressive w.r.t. the variables Λ𝑉(0)N . The
same holds in case Δ (1) is inductively expressive.
  Using this result, any dynamic theory can be made inductively expressive by combining it with
an already inductively expressive theory. Depending on whether we use a loop convergence rule
inherited from Δ (0) or from Δ (1) , we denote it as (C (0) ) or (C (1) ), respectively.

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:19


   Program Rewriting. While not necessary for relative completeness, axiom (E) can also be used to
rewrite homogeneous regular program constructs (here in blue and orange) into fully heterogeneous
regular program constructs (here in magenta) via the following identities (see Theorem C.2):
          ? (𝜙)  ? (𝜙)             𝛼 ∪𝛽 𝛼 ∪𝛽                   𝛼; 𝛽  𝛼; 𝛽   (𝛼) ∗  (𝛼) ∗
                                                                                 ∗
   Using these identities, we can turn a program 𝛼 mixed ≡ 𝑝 1 ;(𝑞 1 ∪ 𝑞 2 ) ∗ . into a program
                                  ∗
𝛼 unmixed ≡ 𝑝 1 ; (𝑞 1 ∪ 𝑞 2 ) ∗ by syntactically deriving that 𝛼 mixed  𝛼 unmixed . This result, in
                                
combination with axiom (E), formalizes the natural correspondence between homogeneous and
heterogeneous regular programs and enables us to decompose a homogeneous programs.

8     Relative Completeness
The expressivity of heterogeneous dynamic logic, enabling us to reason about intertwined hetero-
geneous dynamics, would equally be its downfall if the expressivity were to keep us from verifying
properties in practice. To this end, we usually desire to formalize dynamic logics in a way that
guarantees relative completeness, i.e. the property that any valid formula can also be proved valid if
we assume the availability of an oracle for first-order validity:
Definition 8.1 (Relative Completeness). A dynamic theory Δ is called relatively complete if there
exists a calculus ⊢Δ such that if for some formula 𝐹 ∈ FmlΔ it holds that |=Δ 𝐹 then also ΓΔ ⊢Δ 𝐹 where
ΓΔ = {𝐺 FOL ∈ FOLΔ | |=Δ 𝐺 FOL }.
This property is interesting, because it guarantees that, using the given calculus, proving properties
about the dynamic logic is “no harder” than proving properties about its underlying (first-order) data
theory. Section B introduces a calculus of metaproperties to reason about relative completeness and
related properties for lifted and combined dynamic logics. Due to space constraints, we focus the
exposition in the paper to central assumptions necessary to obtain relative completeness and then
present Theorem 8.1 which proves that, under common, reasonable assumptions, the heterogeneous
dynamic theory over two relatively complete dynamic theories is once again relatively complete.

8.1    Assumptions for Relative Completeness.
We begin by providing a succinct overview on properties of a dynamic theory Δ = (Λ, D) required
to prove relative completeness while deferring formal definitions to the appendix.
  Finite Support. We require that Δ has finite support (see Definition B.2), i.e. that there exists a
syntactic over-approximation BV𝑃 of semantically bound variables (i.e. BVΔ (𝑝) ⊆ BV𝑃 (𝑝) for all
programs 𝑝) and that BV𝑃 is always finite, i.e. all programs only modify a finite set of variables.
   Gödel Expressivity. Like many relative completeness proofs in dynamic logic [9, 31, 51], we require
a first-order theory which is capable of encoding finite sequences of domain values into a single value.
The first example of this mechanism is due to Gödel [29] who showed that any finite sequence of inte-
ger values can be injectively mapped to a single integer value. A more general description of this en-
coding mechanism (here predicate 𝑅) was established by Parikh (first published by Harel [31, p. 29]):
            (∀𝑥 1 . . . 𝑥𝑛 ) (∃𝑦) (∀𝑤) (∀𝑖) ((𝑖 ∈ N ∧ 1 ≤ 𝑖 ≤ 𝑛) =⇒ (𝑅(𝑤, 𝑖, 𝑦) ≡ (𝑤 = 𝑥𝑖 )))
We generalize this notion to our definition of state spaces and atoms here and call an inductively
expressive theory Gödel expressive (Definition B.5), if the domains of all its variables support this
type of sequence encoding. Assuming suitable first order theories, Gödel expressivity has previously
been shown for multiple dynamic logics including interpreted integer first-order dynamic logic [31],
differential dynamic logic over reals [51] and dynamic logic with non-rigid functions [9].

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:20                                               Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


   FOL Expressivity. An additional assumption serving as bread and butter of many meaningful
relative completeness proofs [9, 31, 51] is the notion of FOL expressivity (Definition B.3). This
property asserts that for any program 𝑝 there exists a first-order rendition formula S𝑝 that exactly
relates the pre and post state of 𝑝’s variables. In essence, this ensures that we can express the
behavior of programs in the theory’s first-order fragment. To prove FOL expressivity, one often
relies on Gödel expressiveness. For example, Lemma C.14 proves that for any FOL expressive, Gödel
expressive dynamic theory with finite support its regular closure is also FOL expressive.
   Communicating Theories. While previous assumptions constrained individual theories, we also
require an assumption about the expressivity of heterogeneous atoms in Λ𝐴    ∩ . To this end, Defini-

tion B.6 ensures that heterogeneous theories adhering to it have a common first-order structure that
is expressive enough to exchange integer values via atoms formalizing equality between integers of
both theories. Without communication, our renditions of heterogeneous programs cannot exactly
represent the progress of a heterogeneous loop as the individual theories would not be able to
synchronously count the number of loop iterations.

8.2      Relative Completeness under Combination.
We prove Theorem 8.1 which states that the fully heterogeneous dynamic theory over two relatively
complete dynamic theories is again relatively complete (proof see page 33).
Theorem 8.1 (Relative Completeness of Fully Heterogeneous Dynamic Theories). Let Δ (0) , Δ (1) be
two relatively complete (Definition 8.1), FOL expressive (Definition B.3), Gödel expressive (Definition B.5)
dynamic theories with finite support (Definition B.2) that are communicating in Δ (01) (Definition B.6).
Then the fully heterogeneous dynamic theory Δ̂ with its proof calculus ⊢Δ̂ is relatively complete.

9     Case Study
To demonstrate our approach, we apply HDL to the case study from Section 2. We first derive
results about the individual two components. Subsequently, we merge these results into a system
level guarantee. We will use the homogeneous (atomic) equality predicate 𝑡 1  𝑡 2 which states that
the values of two terms 𝑡 1, 𝑡 2 are equal as well as the homogeneous inequality predicates (≤,>,<).
   Java. For the Java component ctrl we wish to verify that once the relative distance to the stop
sign (given as p) becomes too small it must brake by choosing an appropriate acceleration. Using
JavaDL and the proof calculus implemented in the interactive theorem prover KeY [2, 7], we can then
derive the result in Lemma 9.1. We do not only prove properties on the stateful result of this.acc,
but also on the preservation of the heap structure, the correctness of (possibly overflowing) integer
arithmetic, and the field values of A, B, and T (mechanized proof in KeY). Note that these aspects
of control software would be hard to model in 𝑑L which allows only real-valued variables.
Lemma 9.1 (Correctness of ctrl). The following JavaDL formula is valid:1
               heap_assumptions ∧              heap_assumptions ∧
             ­ A > 0 ∧ A−  A ∧              ­ B ≤ this.acc ≤ A ∧
             ©                    ª          ©                               ª
                                    → [ctrl]
                                  ®                                          ®
             ­ B < 0 ∧ B−  B ∧              ­ (brake_cond → this.acc  B) ∧ ®
             ­                    ®          ­                               ®
                                  ®
             « T > 0∧T  T                   « A  A∧B  B∧T  T
                        −                       −        −        −
                                  ¬                                          ¬
             |          {z        }          |               {z              }
                          ctrlPre                                                   ctrlPost
with brake_cond abbreviating 104 (v + 1) 2 + (A − B)T(AT + 200(v + 1)) > −2 · 104 B(p − 1).
1 For the actual proof we require further assumptions which we summarize as heap_assumptions. This concerns the correct

initialization of the heap, the correct instantiation of Java objects, etc. While this paper denotes object fields as variables
(e.g. A), these values are technically obtained via a rigid function which we omit for clarity [2].

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:21


   Differential Dynamic Logic. Using the calculus implemented in the theorem prover KeYmaera X,
we can prove statements about hybrid programs. For example, we can prove the validity of the
formula in Lemma 9.2 which shows (under some assumptions) that x will always be at most s
(the stop sign’s position) and an additional invariant after execution of env (proof mechanized
in KeYmaera X). While 𝑑L provides us with an effective infrastructure to reason about the en-
vironment’s differential equations, it is unfit to reason about Java’s heap and integer arithmetic.


Lemma 9.2 (Evolution of env). The following formula is valid in 𝑑L:
                                                                                         invariant
                                                                 z      }|    {
              A>0 ∧ B>0 ∧ T>0∧                                          2          
                                                   → [env] x ≤ s ∧ x + v /(2B) ≤ s
              acc_assumptions ∧ x + v2 /(2B) ≤ s           |          {z          }
            |                {z                  }                  envPost
                                envPre

with the following abbreviation for acc_assumptions:
                                                               
  −B ≤ a ∧ a ≤ A ∧ x + v2 /2B + (A/B + 1) AT2 /2 + Tv > s → a  −B ∨ (v  0 ∧ a  0)
  Heterogeneous Safety. Both 𝑑L and JavaDL are instantiations of dynamic theories and we can
hence construct a fully heterogeneous dynamic theory Δ (𝑑JavaL ) , here called differential JavaDL,
over Δ (𝑑 L ) and Δ (JavaDL) . To this end, we add heterogeneous atoms to Λ𝐴
                                                                           ∩ with respective evaluation

A for any integer variable v in JavaDL and any real arithmetic variable w in 𝑑L:
  ∩

    • equal (v, w) with 𝜇 ∈ A ∩ (equal (v, w)) iff Z ∋ V̂ (𝜇, v) = V̂ (𝜇, w)
    • round (v, w) with 𝜇 ∈ A ∩ (round (v, w)) iff V̂ (𝜇, v) ∈ Z and V̂ (𝜇, v) − 0.5 < V̂ (𝜇, w) as
      well as V̂ (𝜇, w) ≤ V̂ (𝜇, v) + 0.5
The atoms allow us to explicitly model the communication between Δ (𝑑 L ) and Δ (JavaDL) and are
all we need to model the full heterogeneous system in Δ (𝑑JavaL ) . After executing the controller we
set the 𝑑L variable 𝑎 to an arbitrary value and then assert it has the value of the Java variable in
this.acc via a check (using the atomic formula equal). Based on the new acceleration we execute
the environment env and retrieve the position and velocity via round. This can be formalized as
    ctrl; 𝛼ˆ ≡ ctrl; (a := ∗; ? (equal (this.acc, 𝑎 ∗ 100)) ; env; p := ∗; v := ∗; ? (coupling))
where we abbreviate coupling ≡ (round (p, 100 (s − x)) ∧ round (v, 100v)). For our safety proof,
we define the following coupled precondition which defines admissible initial states of our het-
erogeneous system:
                                                                                             
  coupledPre ≡ (ctrlPre ∧ 𝜙 2 ∧ 𝜙 3 ) 𝜙 2 ≡ A > 0 ∧ B > 0 ∧ T > 0 ∧ 𝑥 + 𝑣 2 /(2 ∗ 𝐵) ≤ 𝑠
          𝜙 3 ≡ equal (A− , 100A) ∧ equal (B− , −100B) ∧ equal (T− , 100 ∗ T) ∧ coupling
                                                                                         

Note that ctrlPre ∈ FmlΔ (JavaDL) , 𝜙 2 ∈ FmlΔ (𝑑 L) , and 𝜙 3 ∈ FmlΔ (𝑑JavaL) , i.e. ctrlPre and 𝜙 2 constrain
the homogeneous states, while 𝜙 3 synchronizes them. Using our heterogeneous calculus we can
then prove that our heterogeneous system never overshoots the stop sign:
Lemma 9.3 (Safety of the Heterogeneous System). The following formula is valid in Δ (𝑑JavaL ) :
                                                   ˆ ∗ 𝑥 ≤𝑠
                                                      
                             coupledPre → (ctrl; 𝛼)                                            (3)
   Proof Sketch. We provide a sketch for the proof of Lemma 9.3 below (Proof A and B). Beyond
the heterogeneous calculus rules presented above, we use the rules from Figure 4 which are derivable
in our calculus (see Section A).

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:22                                                    Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


  ([] ∧) ( [𝛼] 𝜙 ∧ [𝛼] 𝜓 ) ↔ [𝛼] (𝜙 ∧ 𝜓 )               [𝛼] 𝜙 (𝜙 → 𝜓 )                                     𝜙 → [𝛼] 𝜙
  (𝐹 (𝑖 ) ) (𝜓 → [𝛼] 𝜉) → (𝜙 ∧ 𝜓 → [𝛼] (𝜉 ∧ 𝜙)) (MR)                                               (ind)
                                                             [𝛼] 𝜓                                         𝜙 → [𝛼 ∗ ] 𝜙
      where 𝛼 ∈ Λ𝑃(1−𝑖 ) , 𝜙 ∈ FmlΛ (𝑖 ) and 𝑖 ∈ {0, 1}

              Fig. 4. Additional proof rules derived from previously defined axioms (see Section A).

   Proof A
                        see Proof B
                                                                   ∗ (FOL)
            coupledPre → [ctrl] [ 𝛼ˆ ] coupledPre
       (;)                                             𝐵 > 0 ∧ 𝑥 + 𝑣 2 /2𝐵 ≤ 𝑠 → 𝑥 ≤ 𝑠
             coupledPre → [ctrl; 𝛼ˆ ] coupledPre                      ···
   (ind)
           coupledPre → (ctrl; 𝛼ˆ ) ∗ coupledPre
                                     
                                                            coupledPre → 𝑥 ≤ 𝑠
   (MR)
                             coupledPre → (ctrl; 𝛼ˆ ) ∗ 𝑥 ≤ 𝑠
                                                      

   Proof B
                    ∗ (KeY: Lemma 9.1)                                ∗ (FOL)
      (HR0)                                                                                            using Lemma 9.2
               ctrlPre  →  [ctrl] ctrlPost                      coupledPre   → 𝜙3
(𝐹 (𝑖 ) )                                               (V)                                            see Section C.3
          ctrlPre ∧ 𝜙 2 → [ctrl] (ctrlPost ∧ 𝜙 2 )          coupledPre → [ctrl] 𝜙 3               ( (ctrlPost ∧ 𝜙 2 ) ∧ 𝜙 3 )
([ ] ∧)
                      coupledPre → [ctrl] ( (ctrlPost ∧ 𝜙 2 ) ∧ 𝜙 3 )                             → [ 𝛼ˆ ] coupledPre
               (MR)
                                                   coupledPre → [ctrl] [ 𝛼ˆ ] coupledPre                                        □
The validity of this formula guarantees safety (𝑥 ≤ 𝑠) for any number of control-environment loop
iterations assuming coupledPre. First, note that there is no straight forward way to even specify
this desired behavior without HDL as it represents a system level guarantee only emerging from
the looped interaction of Java and the hybrid program. Secondly, note that our calculus proves
this result by decomposing proof obligations until the JavaDL and 𝑑L lemmas above are applicable.
This underscores the power of our logic to state and prove statements about systems that do not
neatly live in the world of a single dynamic theory, but require their interaction.
   Limitations. Our case study demonstrates that practical proofs reach a scale where pen-and-paper
formalization alone becomes infeasible. In future work, we plan to extend our Isabelle formalization
into a practical tool for HDL proofs. Our approach is also fundamentally limited by its definition of
a dynamic theory. For example, the validity of Barcan’s axiom (B) implies that a variable’s domain
does not grow or shrink. However, this limitation can typically be circumvented by introducing
predicates stating whether an object actually exists [48].

10    Conclusion
This work introduces Heterogeneous Dynamic Logic, a compositional framework for the verification
of heterogeneous programs. Similarly to how Satisfiability Modulo Theories modularly combines
data logics to construct more expressive, combined first-order theories, Heterogeneous Dynamic
Logic modularly combines program logics to construct more expressive, combined heterogeneous
program logics. The resulting heterogeneous dynamic theories enable not only the specification of
otherwise hard to formalize properties (see Sections 2 and 9), but also their verification by providing
a proof calculus that decomposes problems in a manner that is compatible with existing homoge-
neous verification infrastructure – including, both, classical dynamic logic calculi and KAT-based
equational reasoning. Section 8 shows, under common assumptions, that heterogeneous proof
calculi inherit not just rules and axioms but also relative completeness. This proves that verifying
heterogeneous programs is no harder than verifying properties about the homogeneous programs
and their shared first-order structure (i.e., their data logic). Our proof theory of heterogeneous
systems will not only enable the combination of existing verification methodologies, but also serves
as a vehicle for future dynamic logic or KAT-based verification techniques, which can seamlessly
integrate with the existing ecosystem through HDL.

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                                        217:23


Data Availability
We provide our extensible Isabelle formalization on Zenodo [64].

Acknowledgments
This work was supported by funding from the pilot program Core-Informatics of the Helmholtz
Association (HGF) and by an Alexander von Humboldt Professorship.

References
 [1]   Noah Abou El Wafa and André Platzer. 2025. Complete first-order game logic. CoRR, abs/2504.03495. arXiv: 2504.03495.
 [2]   Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, Reiner Hähnle, Peter H. Schmitt, and Mattias Ulbrich, (Eds.)
       2016. Deductive Software Verification - The KeY Book - From Theory to Practice. LNCS. Vol. 10001. Springer. isbn:
       978-3-319-49811-9. doi:10.1007/978-3-319-49812-6.
 [3]   Gidon Ernst, Matthias Güdemann, Alexander Knapp, Florian Nafz, Frank Ortmeier, Hella Ponsar, Gerhard Schellhorn,
       and Alexander Schiendorfer, (Eds.) 2025. The many uses of dynamic logic. Go Where the Bugs Are - Essays Dedicated to
       Wolfgang Reif on the Occasion of His 65th Birthday. LNCS. Springer, 56–82. doi:10.1007/978-3-031-92196-4_4.
 [4]   Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J. Summers. 2019. Leveraging rust types for modular
       specification and verification. Proc. ACM Program. Lang., 3, OOPSLA, 147:1–147:30. doi:10.1145/3360573.
 [5]   Michael Barnett, Bor-Yuh Evan Chang, Robert DeLine, Bart Jacobs, and K. Rustan M. Leino. 2005. Boogie: A modular
       reusable verifier for object-oriented programs. In Formal Methods for Components and Objects, 4th International
       Symposium, FMCO 2005, Amsterdam, The Netherlands, November 1-4, 2005, Revised Lectures (LNCS). Frank S. de Boer,
       Marcello M. Bonsangue, Susanne Graf, and Willem P. de Roever, (Eds.) Springer, 364–387. doi:10.1007/11804192_17.
 [6]   Clark W. Barrett and Cesare Tinelli. 2018. Satisfiability modulo theories. In Handbook of Model Checking. Edmund M.
       Clarke, Thomas A. Henzinger, Helmut Veith, and Roderick Bloem, (Eds.) Springer, 305–343. doi:10.1007/978-3-319-1
       0575-8_11.
 [7]   Bernhard Beckert. 2000. A dynamic logic for the formal verification of java card programs. In Java on Smart Cards:
       Programming and Security, First International Workshop, JavaCard 2000, Cannes, France, September 14, 2000, Revised
       Papers (LNCS). Isabelle Attali and Thomas P. Jensen, (Eds.) Springer, 6–24. doi:10.1007/3-540-45165-X_2.
 [8]   Bernhard Beckert, Daniel Bruns, Vladimir Klebanov, Christoph Scheben, Peter H. Schmitt, and Mattias Ulbrich. 2013.
       Information flow in object-oriented software. In Logic-Based Program Synthesis and Transformation, 23rd International
       Symposium, LOPSTR 2013, Madrid, Spain, September 18-19, 2013, Revised Selected Papers (LNCS). Gopal Gupta and
       Ricardo Peña, (Eds.) Springer, 19–37. doi:10.1007/978-3-319-14125-1_2.
 [9]   Bernhard Beckert and André Platzer. 2006. Dynamic logic with non-rigid functions. In Automated Reasoning, Third
       International Joint Conference, IJCAR 2006, Seattle, WA, USA, August 17-20, 2006, Proceedings (LNCS). Ulrich Furbach
       and Natarajan Shankar, (Eds.) Springer, 266–280. doi:10.1007/11814771_23.
[10]   Bernhard Beckert, Peter Sanders, Mattias Ulbrich, Julian Wiesler, and Sascha Witt. 2024. Formally verifying an
       efficient sorter. In Tools and Algorithms for the Construction and Analysis of Systems - 30th International Conference,
       TACAS 2024, Luxembourg City, Luxembourg, April 6-11, 2024, Proceedings, Part I (LNCS). Bernd Finkbeiner and Laura
       Kovács, (Eds.) Springer, 268–287. doi:10.1007/978-3-031-57246-3_15.
[11]   Stefan Blom and Marieke Huisman. 2014. The vercors tool for verification of concurrent programs. In FM 2014:
       Formal Methods - 19th International Symposium, Singapore, May 12-16, 2014. Proceedings (LNCS). Cliff B. Jones, Pekka
       Pihlajasaari, and Jun Sun, (Eds.) Springer, 127–131. doi:10.1007/978-3-319-06410-9_9.
[12]   Rose Bohrer. 2017. Differential dynamic logic. Archive of Formal Proofs, (Feb. 2017). https://isa-afp.org/entries/Differ
       ential_Dynamic_Logic.html, Formal proof development.
[13]   Rose Bohrer and André Platzer. 2018. A hybrid, dynamic logic for hybrid-dynamic information flow. In Proceedings
       of the 33rd Annual ACM/IEEE Symposium on Logic in Computer Science, LICS 2018, Oxford, UK, July 09-12, 2018.
       Anuj Dawar and Erich Grädel, (Eds.) ACM, 115–124. doi:10.1145/3209108.3209151.
[14]   Pei-Wei Chen, Shaokai Lin, Adwait Godbole, Ramneet Singh, Elizabeth Polgreen, Edward A. Lee, and Sanjit A. Seshia.
       2025. Polyver: A compositional approach for polyglot system modeling and verification. In Proceedings of the 25th
       Conference on Formal Methods in Computer-Aided Design, FMCAD 2025, Menlo Park, CA, USA, October 6-10, 2025.
       Ahmed Irfan and Daniela Kaufmann, (Eds.) TU Wien Academic Press. doi:10.34727/2025/ISBN.978-3-85448-084-6_10.
[15]   Alessandro Cimatti, Alberto Griggio, Sergio Mover, Marco Roveri, and Stefano Tonetta. 2022. Verification modulo
       theories. Formal Methods Syst. Des., 60, 3, 452–481. doi:10.1007/S10703-023-00434-X.
[16]   Edmund M. Clarke, Daniel Kroening, and Flavio Lerda. 2004. A tool for checking ANSI-C programs. In Tools and
       Algorithms for the Construction and Analysis of Systems, 10th International Conference, TACAS 2004, Barcelona,




                                    Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:24                                                 Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


         Spain, March 29 - April 2, 2004, Proceedings (LNCS). Kurt Jensen and Andreas Podelski, (Eds.) Springer, 168–176.
         doi:10.1007/978-3-540-24730-2_15.
[17]     M. J. Cresswell and G. E. Hughes. 1996. A New Introduction to Modal Logic. Routledge, New York.
[18]     Martin de Boer, Stijn de Gouw, Jonas Klamroth, Christian Jung, Mattias Ulbrich, and Alexander Weigl. 2023. Formal
         specification and verification of jdk’s identity hash map implementation. Formal Aspects Comput., 35, 3, 18:1–18:26.
         doi:10.1145/3594729.
[19]     Jules Desharnais, Bernhard Möller, and Georg Struth. 2006. Kleene algebra with domain. ACM Trans. Comput. Log., 7,
         4, 798–833. doi:10.1145/1183278.1183285.
[20]     Edsger W. Dijkstra. 1975. Guarded commands, nondeterminacy and formal derivation of programs. Commun. ACM,
         18, 8, 453–457. doi:10.1145/360933.360975.
[21]     Gidon Ernst, Wolfram Pfeifer, and Mattias Ulbrich. 2024. Contract-lib: A proposal for a common interchange format for
         software system specification. In Leveraging Applications of Formal Methods, Verification and Validation. Specification
         and Verification - 12th International Symposium, ISoLA 2024, Crete, Greece, October 27-31, 2024, Proceedings, Part III
         (LNCS). Tiziana Margaria and Bernhard Steffen, (Eds.) Springer, 79–105. doi:10.1007/978-3-031-75380-0_6.
[22]     Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3 - where programs meet provers. In Programming
         Languages and Systems - 22nd European Symposium on Programming, ESOP 2013, Rome, Italy, March 16-24, 2013.
         Proceedings (LNCS). Matthias Felleisen and Philippa Gardner, (Eds.) Springer, 125–128. doi:10.1007/978-3-642-37036-
         6_8.
[23]     Simon Foster. 2019. Hybrid relations in isabelle/utp. In Unifying Theories of Programming - 7th International Symposium,
         UTP 2019, Dedicated to Tony Hoare on the Occasion of His 85th Birthday, Porto, Portugal, October 8, 2019, Proceedings
         (LNCS). Pedro Ribeiro and Augusto Sampaio, (Eds.) Springer, 130–153. doi:10.1007/978-3-030-31038-7_7.
[24]     Simon Foster, Frank Zeyda, and Jim Woodcock. 2014. Isabelle/utp: A mechanised theory engineering framework. In
         Unifying Theories of Programming - 5th International Symposium, UTP 2014, Singapore, May 13, 2014, Revised Selected
         Papers (LNCS). David A. Naumann, (Ed.) Springer, 21–41. doi:10.1007/978-3-319-14806-9_2.
[25]     Nathan Fulton, Stefan Mitsch, Jan-David Quesel, Marcus Völp, and André Platzer. 2015. Keymaera X: an axiomatic
         tactical theorem prover for hybrid systems. In Automated Deduction - CADE-25 - 25th International Conference on
         Automated Deduction, Berlin, Germany, August 1-7, 2015, Proceedings (LNCS). Amy P. Felty and Aart Middeldorp,
         (Eds.) Springer, 527–538. doi:10.1007/978-3-319-21401-6_36.
[26]     Dov M. Gabbay. 1996. An overview of fibred semantics and the combination of logics. In Frontiers of Combining
         Systems, First International Workshop FroCoS 1996, Munich, Germany, March 26-29, 1996, Proceedings. Applied Logic
         Series. Franz Baader and Klaus U. Schulz, (Eds.) Kluwer Academic Publishers, 1–55. doi:10.1007/978-94-009-0349-4_1.
[27]     Dov M. Gabbay. 1999. Fibring Logics. Clarendon Press, New York.
[28]     Luis Garcia, Stefan Mitsch, and André Platzer. 2019. Hyplc: hybrid programmable logic controller program translation
         for verification. In Proceedings of the 10th ACM/IEEE International Conference on Cyber-Physical Systems, ICCPS 2019,
         Montreal, QC, Canada, April 16-18, 2019. Xue Liu, Paulo Tabuada, Miroslav Pajic, and Linda Bushnell, (Eds.) ACM,
         47–56. doi:10.1145/3302509.3311036.
[29]     Kurt Gödel. 1931. Über formal unentscheidbare sätze der principia mathematica und verwandter systeme i. Monat-
         shefte für Mathematik und Physik, 38, 173–198. doi:10.1007/BF01700692.
[30]     Michael Greenberg, Ryan Beckett, and Eric Hayden Campbell. 2022. Kleene algebra modulo theories: a framework
         for concrete kats. In PLDI ’22: 43rd ACM SIGPLAN International Conference on Programming Language Design and
         Implementation, San Diego, CA, USA, June 13 - 17, 2022. Ranjit Jhala and Isil Dillig, (Eds.) ACM, 594–608. doi:10.1145
         /3519939.3523722.
[31]     David Harel. 1979. First-Order Dynamic Logic. LNCS. Vol. 68. Springer. isbn: 3-540-09237-4. doi:10.1007/3-540-09237-4.
[32]     David Harel, Dexter Kozen, and Jerzy Tiuryn. 2000. Dynamic Logic. The MIT Press, (Sept. 2000). isbn: 978-0-262-
         27495-1. doi:10.7551/mitpress/2516.001.0001.
[33]     C. A. R. Hoare. 1969. An axiomatic basis for computer programming. Commun. ACM, 12, 10, 576–580. doi:10.1145/36
         3235.363259.
[34]     C. A. R. Hoare. 1997. Unified theories of programming. In Mathematical Methods in Program Development. Manfred
         Broy and Birgit Schieder, (Eds.) Springer Berlin Heidelberg, Berlin, Heidelberg, 313–367. isbn: 978-3-642-60858-2.
         doi:10.1007/978-3-642-60858-2_21.
[35]     Jean-Baptiste Jeannin, Khalil Ghorbal, Yanni Kouskoulas, Aurora C. Schmidt, Ryan W. Gardner, Stefan Mitsch, and
         André Platzer. 2017. A formally verified hybrid system for safe advisories in the next-generation airborne collision
         avoidance system. Int. J. Softw. Tools Technol. Transf., 19, 6, 717–741. doi:10.1007/S10009-016-0434-1.
[36]     Chris Johannsen, Karthik Nukala, Rohit Dureja, Ahmed Irfan, Natarajan Shankar, Cesare Tinelli, Moshe Y. Vardi, and
         Kristin Yvonne Rozier. 2024. The moxi model exchange tool suite. In Computer Aided Verification - 36th International
         Conference, CAV 2024, Montreal, QC, Canada, July 24-27, 2024, Proceedings, Part I (LNCS). Arie Gurfinkel and Vijay
         Ganesh, (Eds.) Springer, 203–218. doi:10.1007/978-3-031-65627-9_10.


Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                                        217:25


[37]   Eduard Kamburjan, Stefan Mitsch, and Reiner Hähnle. 2022. A hybrid programming language for formal modeling
       and verification of hybrid systems. Leibniz Trans. Embed. Syst., 8, 2, 04:1–04:34. doi:10.4230/LITES.8.2.4.
[38]   Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris Yakobowski. 2015. Frama-c: A
       software analysis perspective. Formal Aspects Comput., 27, 3, 573–609. doi:10.1007/S00165-014-0326-7.
[39]   Jonas Klamroth, Bernhard Beckert, Max Scheerer, and Oliver Denninger. 2023. Qin: enabling formal methods to deal
       with quantum circuits. In IEEE International Conference on Quantum Software, QSW 2023, Chicago, IL, USA, July 2-8,
       2023. Shaukat Ali et al., (Eds.) IEEE, 175–185. doi:10.1109/QSW59989.2023.00029.
[40]   Dexter Kozen. 1997. Kleene algebra with tests. ACM Trans. Program. Lang. Syst., 19, 3, 427–443. doi:10.1145/256167.25
       6195.
[41]   Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno,
       and Chris Hawblitzel. 2023. Verus: verifying rust programs using linear ghost types. Proc. ACM Program. Lang., 7,
       OOPSLA1, 286–315. doi:10.1145/3586037.
[42]   Sarah M. Loos and André Platzer. 2016. Differential refinement logic. In Proceedings of the 31st Annual ACM/IEEE
       Symposium on Logic in Computer Science, LICS ’16, New York, NY, USA, July 5-8, 2016. Martin Grohe, Eric Koskinen,
       and Natarajan Shankar, (Eds.) ACM, 505–514. doi:10.1145/2933575.2934555.
[43]   Peter Müller, Malte Schwerhoff, and Alexander J. Summers. 2016. Viper: A verification infrastructure for permission-
       based reasoning. In Verification, Model Checking, and Abstract Interpretation - 17th International Conference, VMCAI
       2016, St. Petersburg, FL, USA, January 17-19, 2016. Proceedings (LNCS). Barbara Jobstmann and K. Rustan M. Leino,
       (Eds.) Springer, 41–62. doi:10.1007/978-3-662-49122-5_2.
[44]   Greg Nelson and Derek C. Oppen. 1979. Simplification by cooperating decision procedures. ACM Trans. Program.
       Lang. Syst., 1, 2, 245–257. doi:10.1145/357073.357079.
[45]   Pedro Nora, Jurriaan Rot, Lutz Schröder, and Paul Wild. 2025. Relational connectors and heterogeneous simulations.
       In Foundations of Software Science and Computation Structures - 28th International Conference, FoSSaCS 2025, Hamilton,
       ON, Canada, May 3-8, 2025, Proceedings (LNCS). Parosh Aziz Abdulla and Delia Kesner, (Eds.) Springer, 111–132.
       doi:10.1007/978-3-031-90897-2_6.
[46]   Derek C. Oppen. 1980. Complexity, convexity and combinations of theories. Theor. Comput. Sci., 12, 291–302. doi:10.1
       016/0304-3975(80)90059-6.
[47]   Marco Paganoni and Carlo A. Furia. 2023. Verifying functional correctness properties at the level of java bytecode. In
       Formal Methods - 25th International Symposium, FM 2023, Lübeck, Germany, March 6-10, 2023, Proceedings (LNCS).
       Marsha Chechik, Joost-Pieter Katoen, and Martin Leucker, (Eds.) Springer, 343–363. doi:10.1007/978-3-031-27481-7
       _20.
[48]   André Platzer. 2012. A complete axiomatization of quantified differential dynamic logic for distributed hybrid systems.
       Log. Methods Comput. Sci., 8, 4. doi:10.2168/LMCS-8(4:17)2012.
[49]   André Platzer. 2017. A complete uniform substitution calculus for differential dynamic logic. J. Autom. Reason., 59, 2,
       219–265. doi:10.1007/S10817-016-9385-1.
[50]   André Platzer. 2008. Differential dynamic logic for hybrid systems. J. Autom. Reason., 41, 2, 143–189. doi:10.1007/S10
       817-008-9103-8.
[51]   André Platzer. 2012. The complete proof theory of hybrid systems. In Proceedings of the 27th Annual IEEE Symposium
       on Logic in Computer Science, LICS 2012, Dubrovnik, Croatia, June 25-28, 2012. IEEE Computer Society, 541–550.
       doi:10.1109/LICS.2012.64.
[52]   André Platzer and Jan-David Quesel. 2009. European train control system: A case study in formal verification. In
       Formal Methods and Software Engineering, 11th International Conference on Formal Engineering Methods, ICFEM 2009,
       Rio de Janeiro, Brazil, December 9-12, 2009. Proceedings (LNCS). Karin K. Breitman and Ana Cavalcanti, (Eds.) Springer,
       246–265. doi:10.1007/978-3-642-10373-5_13.
[53]   André Platzer and Yong Kiam Tan. 2020. Differential equation invariance axiomatization. J. ACM, 67, 1, 6:1–6:66.
       doi:10.1145/3380825.
[54]   Enguerrand Prebet and André Platzer. 2024. Uniform substitution for differential refinement logic. In Automated
       Reasoning - 12th International Joint Conference, IJCAR 2024, Nancy, France, July 3-6, 2024, Proceedings, Part II (LNCS).
       Christoph Benzmüller, Marijn J. H. Heule, and Renate A. Schmidt, (Eds.) Springer, 196–215. doi:10.1007/978-3-031-6
       3501-4_11.
[55]   H. G. Rice. 1953. Classes of recursively enumerable sets and their decision problems. Transactions of the American
       Mathematical Society, 74, 2, 358–366. doi:10.2307/1990888.
[56]   Philipp Rümmer and Muhammad Ali Shah. 2007. Proving programs incorrect using a sequent calculus for java
       dynamic logic. In Tests and Proofs - 1st International Conference, TAP 2007, Zurich, Switzerland, February 12-13, 2007.
       Revised Papers (LNCS). Yuri Gurevich and Bertrand Meyer, (Eds.) Springer, 41–60. doi:10.1007/978-3-540-73770-4_3.
[57]   Gerhard Schellhorn and Wolfgang Ahrendt. 1997. Reasoning about abstract state machines: the WAM case study. J.
       Univers. Comput. Sci., 3, 4, 377–413. doi:10.3217/JUCS-003-04-0377.


                                    Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:26                                                Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


[58]     Igor Sedlár. 2023. Kleene algebra with dynamic tests: completeness and complexity. CoRR, abs/2311.06937. arXiv:
         2311.06937.
[59]     Igor Sedlár. 2023. On the complexity of kleene algebra with domain. In Relational and Algebraic Methods in Computer
         Science - 20th International Conference, RAMiCS 2023, Augsburg, Germany, April 3-6, 2023, Proceedings (LNCS). Roland
         Glück, Luigi Santocanale, and Michael Winter, (Eds.) Springer, 208–223. doi:10.1007/978-3-031-28083-2_13.
[60]     Krister Segerberg. 1982. A completeness theorem in the modal logic of programs. Banach Center Publications, 9,
         31–46. doi:10.4064/-9-1-31-46.
[61]     Robert E. Shostak. 1978. An algorithm for reasoning about equality. Commun. ACM, 21, 7, 583–585. doi:10.1145/3595
         45.359570.
[62]     Yong Kiam Tan and André Platzer. 2021. An axiomatic approach to existence and liveness for differential equations.
         Formal Aspects Comput., 33, 4-5, 461–518. doi:10.1007/S00165-020-00525-0.
[63]     Samuel Teuber, Stefan Mitsch, and André Platzer. 2024. Provably safe neural network controllers via differential
         dynamic logic. In Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information
         Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024. Amir Globersons, Lester
         Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang, (Eds.)
[64]     [SW] Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert, Artifact for "Heterogeneous Dynamic
         Logic: Provability Modulo Program Theories" Mar. 2026. doi:10.5281/zenodo.19551156.
[65]     Cesare Tinelli and Mehdi T. Harandi. 1996. A new correctness proof of the Nelson-Oppen combination procedure.
         In Frontiers of Combining Systems, First International Workshop FroCoS 1996, Munich, Germany, March 26-29, 1996,
         Proceedings (Applied Logic Series). Franz Baader and Klaus U. Schulz, (Eds.) Kluwer Academic Publishers, 103–119.
         doi:10.1007/978-94-009-0349-4_5.
[66]     Cesare Tinelli and Calogero G. Zarba. 2004. Combining decision procedures for sorted theories. In Logics in Artificial
         Intelligence, 9th European Conference, JELIA 2004, Lisbon, Portugal, September 27-30, 2004, Proceedings (LNCS). José
         Júlio Alferes and João Alexandre Leite, (Eds.) Springer, 641–653. doi:10.1007/978-3-540-30227-8_53.
[67]     Mattias Ulbrich. 2010. A dynamic logic for unstructured programs with embedded assertions. In Formal Verification
         of Object-Oriented Software - International Conference, FoVeOOS 2010, Paris, France, June 28-30, 2010, Revised Selected
         Papers (LNCS). Bernhard Beckert and Claude Marché, (Eds.) Springer, 168–182. doi:10.1007/978-3-642-18070-5_12.
[68]     Mattias Ulbrich. 2013. Dynamic Logic for an Intermediate Language: Verification, Interaction and Refinement. Ph.D.
         Dissertation. Karlsruhe Institute of Technology. doi:10.5445/IR/1000041169.
[69]     Yuanrui Zhang. 2024. Parameterized dynamic logic - towards A cyclic logical framework for program verification via
         operational semantics. CoRR, abs/2404.18098. arXiv: 2404.18098.




Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:27


A     Additional Proof Rules
A.1    Additional Proof Rules for Dynamic Theories
Lemma A.1 (Helper Rules). The axioms ([] ∧), (𝐾 ⟨ ⟩ ), and (𝑀𝑃 ⟨⟩ ) as well as the proof rules (M) and
(MR) in Figure 5 are sound and can be derived from the proof rules of Dynamic Theories established in
Section 4.
  Proof. The proofs presented here are based on proofs for Modal Logic from the literature [17].
The rule ([] ∧) is sound and can be derived:
⇒



                                                     ∗
                                             𝜙 → 𝜓 → (𝜙 ∧ 𝜓 )
                                     (G)
                                          [𝛼] (𝜙 → 𝜓 → (𝜙 ∧ 𝜓 ))
                                   (K)
                                        [𝛼] 𝜙 → [𝛼] (𝜓 → (𝜙 ∧ 𝜓 ))
                                 (K)
                                      [𝛼] 𝜙 → ( [𝛼] 𝜓 → [𝛼] (𝜙 ∧ 𝜓 ))
Elementary logic transformations yield that this is equivalent to ( [𝛼] 𝜙 ∧ [𝛼] 𝜓 ) → [𝛼] (𝜙 ∧ 𝜓 ).
⇐
First, we show the property for 𝜙; subsequently the same proof can be repeated for 𝜓 and subse-
quently be joined:
                                                       ∗
                                                  𝜙 ∧𝜓 → 𝜙
                                          (G)
                                               [𝛼] (𝜙 ∧ 𝜓 → 𝜙)
                                        (K)
                                             [𝛼] (𝜙 ∧ 𝜓 ) → [𝛼] 𝜙
The rule (M) is sound and can be derived:

                                                    (𝜙 → 𝜓 )
                                             (G)
                                                  [𝛼] (𝜙 → 𝜓 )
                                            (K)
                                                 [𝛼] 𝜙 → [𝛼] 𝜓
The proof for (𝐾 ⟨ ⟩ ) is based on work by Platzer [51, Appendix B.4]: We first obtain [𝛼] (¬𝜓 → ¬𝜙) →
([𝛼] ¬𝜓 → [𝛼] ¬𝜙) via (K). Via propositional reasoning this can be rewritten as: [𝛼] (¬𝜓 → ¬𝜙) →
(¬ [𝛼] ¬𝜙 → ¬ [𝛼] ¬𝜓 ). Via duality this is the same as [𝛼] (¬𝜓 → ¬𝜙) → (⟨𝛼⟩ 𝜙 → ⟨𝛼⟩ 𝜓 ). Via
(𝜙 → 𝜓 ) → (¬𝜓 → ¬𝜙) and (G) with (K) we derive that [𝛼] (𝜙 → 𝜓 ) → (⟨𝛼⟩ 𝜙 → ⟨𝛼⟩ 𝜓 ).
  The rule (MR) is sound and can be derived by cutting [𝛼] 𝜙 into the proof and subsequently
applying (M) (proven sound above).

   For the proof of (𝑀𝑃 ⟨ ⟩ ) we start with the formulas ⟨𝛼⟩ 𝜓 and ∀𝑣 (𝜓 → 𝜙). Via (V) (all bound
variables of 𝛼 are not free in the formula) we get that the latter formula implies [𝛼] ∀𝑣 (𝜓 → 𝜙).
We can then instantiate the variables in 𝑣 with their respective non-bound versions which yields
[𝛼] (𝜓 → 𝜙). Via (𝐾 ⟨ ⟩ ) (proven above) we then get ⟨𝛼⟩ 𝜓 → ⟨𝛼⟩ 𝜙. Therefore, the following
formula is valid: ⟨𝛼⟩ 𝜓 ∧ (⟨𝛼⟩ 𝜓 → ⟨𝛼⟩ 𝜙) → ⟨𝛼⟩ 𝜙. This in turn implies ⟨𝛼⟩ 𝜙.
                                                                                                □
Lemma A.2 (Pullback Axiom). The following axiom is sound for any dynamic theory Δ and derivable
from the axioms and proof rules in Section 4:

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:28                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


 ([] ∧) ( [𝛼] 𝜙 ∧ [𝛼] 𝜓 ) ↔ [𝛼] (𝜙 ∧ 𝜓 )                                                            𝜙 →𝜓
                                                                                         (M)
  (𝐾 ⟨ ⟩ ) [𝛼] (𝜙 → 𝜓 ) → ⟨𝛼⟩ 𝜙 → ⟨𝛼⟩ 𝜓                                                         [𝛼] 𝜙 → [𝛼] 𝜓
(𝑀𝑃 ⟨ ⟩ ) ⟨𝛼⟩ 𝜓 ∧ ∀𝑣 (𝜓 → 𝜙) → ⟨𝛼⟩ 𝜙                                                           [𝛼] 𝜙       (𝜙 → 𝜓 )
           where 𝑣 ⊇ BVΔ (𝛼)                                                       (MR)
                                                                                                       [𝛼] 𝜓

Fig. 5. Additional proof rules for Dynamic Theories. All rules pictured here are derivable from the axioms of
Dynamic Logic established in Section 4.


                                                         𝑣       ⊇ (BVΔ (𝛼) ∪ FVΔ (⟨𝛼⟩ 𝜙))
   (PB) ∀𝑣 + (𝜓 → ⟨𝛼⟩ 𝜉) ∧ ∃𝑣 + 𝜓 ∧ ∀𝑣 (𝜉 → 𝜙) → (⟨𝛼⟩ 𝜙) +
                                              
                                                         𝑣       = FVΔ (𝜓 ∧ 𝜉) \ 𝑣
   Proof. Starting from ∀𝑣 + (𝜓 → ⟨𝛼⟩ 𝜉) and ∃𝑣 + 𝜓 ∧ ∀𝑣 (𝜉 → 𝜙) we can derive via first-
                                                                    
order reasoning that this implies ∃𝑣 + 𝜓 ∧ ∀𝑣 (𝜉 → 𝜙) ∧ (𝜓 → ⟨𝛼⟩ 𝜉)  via
                                                                        propositional recom-
bination this can be turned into ∃𝑣 + 𝜓 ∧ 𝜓 → ⟨𝛼⟩ 𝜉 ∧ ∀𝑣 (𝜉 → 𝜙) . Using (𝑀𝑃 ⟨⟩ ) this im-
plies ∃𝑣 + (𝜓 ∧ (𝜓 → ⟨𝛼⟩ 𝜙)). Via (local) Modus Ponens this implies ∃𝑣 + (⟨𝛼⟩ 𝜙). Since 𝑣 + ∉
FVΔ (⟨𝛼⟩ 𝜙) this in turn implies ⟨𝛼⟩ 𝜙                                                      □

A.2      Additional Proof Rules for Regular Programs
Lemma A.3 (Loop Induction). For any dynamic theory Δ, the following axiom is sound in Δreg and
derivable from the axioms in Section 6.2:
                                                         𝜙 → [𝛼] 𝜙
                                                 (ind)
                                                         𝜙 → [𝛼 ∗ ] 𝜙
   Proof. The proof can be performed as follows:

                                                       𝜙 → [𝛼] 𝜙
                                              (G)    ∗
                                                   [𝛼 ] (𝜙 → [𝛼] 𝜙)
                                               (I)
                                                      𝜙 → [𝛼 ∗ ] 𝜙
                                                                                                                      □

A.3      Additional Proof Rules for Heterogeneous Dynamic Theories
Lemma A.4 (Soundness of Frame Rule). For any heterogeneous dynamic theory Δ̂ over dynamic
theories Δ (0) , Δ (1) the following axiom is sound and can be derived from the rules from Section 7:
  (𝐹 (𝑖 ) ) (𝜓 → [𝛼] 𝜉) → (𝜙 ∧ 𝜓 → [𝛼] (𝜉 ∧ 𝜙))
            where 𝛼 ∈ Λ𝑃(1−𝑖 ) , 𝜙 ∈ FmlΛ (𝑖 ) and 𝑖 ∈ {0, 1}
  Proof. The proofs assume the previous derivation of the rules from Lemma A.1
After application of ([] ∧), the left side reads 𝜙 ∧ 𝜓 → [𝛼] 𝜉 ∧ [𝛼] 𝜙 which we can decompose into
two implications. Observe that 𝜓 → [𝛼] 𝜉 is our assumption on the right. For the case of 𝜙 → [𝛼] 𝜙
we can apply the (V) axiom since Λ𝑉(𝑖 ) ∩ Λ𝑉(1−𝑖 ) = ∅ and BVΔ (𝛼) ⊆ Λ𝑉(1−𝑖 ) while FVΔ (𝜙) ⊆ Λ𝑉(𝑖 ) .
                                                                                                       □
Lemma A.5 (Ghost Axiom given Equality). For any heterogeneous dynamic theory Δ̂ over dynamic
theories Δ (0) , Δ (1) , the following axiom is sound and can be derived from the rules from Section 7
under the additional assumption of the axiom 𝑣  𝑣 (for all 𝑣 ∈ Λ𝑉 ):

(ghost) [𝑣 := ∗; ? (𝑣  𝑤)] 𝜙 → 𝜙 (for 𝑣 ∉ FVΔ (𝜙))

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:29


   Proof. The rule Ghost is sound and can be derived: Resolving the program on the left using
(:=∗) and (?), we get an equivalent representation
                                    ∀𝑣 (𝑣  𝑤 → 𝜙) for 𝑣 ∉ FVΔ (𝜙)
By instantiating 𝑣 with 𝑤 we get 𝑤  𝑤 → 𝜙 (since 𝑣 ∉ Vars (𝜙)). Using Modus Ponens with the
axiom 𝑤  𝑤 this derives 𝜙.                                                                □

B   A Calculus for Reasoning about Meta-Properties of Dynamic Theories
A desirable meta property for dynamic logics is the relative completeness of their axiomatizations [9,
32, 51]: Due to Gödel [29], for most dynamic logics, one cannot hope for a complete axiomatization,
as their expressiveness allows the axiomatization of integers [32] that constitute an undecidable
first-order theory. However, it is often possible to create a finite set of axiom schemata and proof
rules that allow us to reduce any validity question over dynamic logic formulas to a validity question
over first-order theory formulas for which we then assume the availability of an oracle. This limited
notion of completeness, called relative completeness, implies that our calculus ensures that programs
are handled completely, as proving properties about the considered programs is exactly as hard
as proving properties about the underlying first-order theory (and no harder). We formalize this
notion in Definition 8.1.
   The preceding sections of this paper have proposed a highly compositional approach to the
construction of dynamic theories: Starting from a base theory Δ, we can generate lifted dynamic
theories with more program functionality (Δ:=∗ and Δreg ) or combine theories (Δ (01) and then
Δ̂). The key advantage of theory lifting and combination was the ability to reuse proof calculi
and obtain standardized additional proof rules which are valid irrespective of the lifted/combined
theory. The approach outlined above raises the question to what degree meta properties of the
calculus, in particular its relative completeness, are equally compositional: For example, given
a relatively complete dynamic theory Δ (0) , can we derive a notion of relative completeness for
 Δ (0)
        reg
             ? Or, similarly, can we derive a relative completeness result for its theory combination
w.r.t. some secondary dynamic theory Δ̂? To this end, we observe that relative completeness proofs
in the literature, implicitly or explicitly, follow a highly-compositional structure [9, 31, 51] that can
be leveraged to compositionalize results on the relative completeness of dynamic theory calculi.
Hence, in this section, we describe a number of results that allow us to lift and merge relative
completeness results when lifting and combining dynamic theories in a structured manner.
   Section 4 outlined properties/assumptions that defined what a dynamic theory is. In Section 6.2
we saw, for the first time, a case where we leveraged further assumptions (inductive expressiveness,
Definition 6.4) to derive stronger calculus rules (axiom (C)). We will begin this section by describing
a set of additional meta properties, like relative completeness (Definition 8.1), that certain dynamic
theories may satisfy (Section B.1). For these additional meta properties/assumptions, we then derive
sufficient conditions under which the meta properties are preserved under theory lifting and/or
theory combination (Section B.2). Finally, we leverage the defined meta properties and proven
preservation rules to derive relative completeness results for havoc lifting, regular program lifting,
and theory combination in (fully) heterogeneous dynamic theories.
   Notation and Admissible Variable Values. Going forward, we will use underlining of variables to
denote (syntactically!) finite vectors of variables or values (e.g., 𝑣 or 𝛿). By slight abuse of notation,
we will also use these vectors in quantifiers (e.g., ∀𝑣 . . . ), which can be reduced to a (syntactically)
finite sequence of quantifiers. By an even worse abuse of notation, we will sometimes use the
vectors in set expressions (e.g. 𝑣 ⊆ FVΔ (𝜙)), in which case we consider the set of all variables in
the vector.

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:30                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


Definition B.1 (Reasoning about admissible variable values). Given a dynamic theory Δ we de-
fine ValsΔ : Λ𝑉 → 2 U as the mapping from variables to all admissible values of a variable (i.e.
ValsΔ (𝑣) = {𝛿 ∈ U | it exists 𝜇 ∈ S such that V (𝜇, 𝑣) = 𝛿 }). We call two variables 𝑣, 𝑣˜ twin variables
iff ValsΔ (𝑣) = ValsΔ (𝑣).
                       ˜ We call two variable vectors 𝑣, 𝑣˜ twins iff the vectors are of equal length and
for every component it holds that 𝑣 𝑖 and 𝑣˜𝑖 are twin variables.

B.1      Assumptions for Relative Completeness
To transfer relative completeness across liftings and into heterogeneous theories, we must impose
one further meaningful restriction about the behavior of programs in our underlying dynamic
theory. We now require that programs not only have a finite read footprint (Definition 4.5), but
also a finite write footprint to be able to characterise their behavior:
Definition B.2 (Finite Support). Given a dynamic theory Δ. We say Δ has finite support iff for some
function BV𝑃 : Λ𝑃 → 2Λ𝑉 it holds that:
         (BV𝑃 Coverage) For all programs 𝑝 ∈ Λ𝑃 it holds that BVΔ (𝑝) ⊆ BV𝑃 (𝑝)
            (BV𝑃 Finite) For all programs 𝑝 ∈ Λ𝑃 the result of BV𝑃 (𝑝) is finite
   First Order Expressiveness. Beyond this assumption on program behavior and the assumption on
the availability of a relatively complete proof calculus (Definition 8.1), we also require further tools
that are necessary to prove relative completeness. These assumptions do not always constrain the
range of allowed programs or atomic formulas, but for relative completeness results to carry over,
the designer of a given dynamic theory must ensure these additional meta properties hold. The first
requirement of this kind is termed FOL Expressiveness and ensures that a given dynamic theory is
capable of representing the behavior of its programs in the theory’s first-order fragment. While this
requirement might seem surprising and unintuitive for someone unfamiliar with dynamic logic
relative completeness results, it is, in fact, the bread and butter of meaningful relative completeness
proofs [9, 31, 51]:
Definition B.3 (FOL Expressive). Consider a dynamic theory Δ with finite support. We say Δ is FOL
Expressive iff it satisfies the following properties:
(Infinite Variables) For any variable 𝑣 ∈ Λ𝑉 there exists an infinite number of twin variables.
      (Eq Predicate) There exists a function : Λ𝑉2 → FOLΔ such that for twin variables 𝑣, 𝑤 ∈
                     Λ𝑉 N and any state 𝜇 ∈ S:
                     𝜇 ∈ DJ (𝑣, 𝑤)K iff V (𝜇, 𝑣) = V (𝜇, 𝑤)
         (Rendition) There exists a function S such that for all programs 𝑝 ∈ Λ𝑃 and all twin
                     variable vectors 𝑣, 𝑣 + with 𝑣 ⊇ Vars (𝑝) and 𝑣 ∩𝑣 + = ∅ the function S𝑝 𝑣, 𝑣 +
                     returns a formula    in FOLΛ such that:
                     |=Δ S𝑝 𝑣, 𝑣 + ↔ ⟨𝑝⟩ 𝑣  𝑣 +
                                  

   For clarity, we will denote  (𝑣, 𝑤) as 𝑣  𝑤. For example, there exist results for rendition of
first-order dynamic logic programs [31] or hybrid programs [51] (via relative completeness w.r.t.
the discrete fragment of hybrid programs). We can then derive the following additional axiom on
the behavior of equality:
   Gödelization. Another characteristic of relative completeness proofs in dynamic logic is that they
typically rely on the ability of first-order theories to encode both program behavior (see above) and
finite sequences of domain values into a single value. The first example of this mechanism is due to
Gödel [29] who showed that any finite sequence of integer values can be injectively mapped to a
single integer value. The purpose of these encodings lies in the reasoning about loops: To prove

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:31


relative completeness, we require that the first-order fragment of our dynamic theory is capable of
expressing the strongest loop invariant.
   A more general description of this sequence encoding mechanism was established by Parikh
(and first published by Harel [31, p. 29]): Intuitively, without precisely formalizing the logic below,
we desire a total predicate 𝑅(𝑥, 𝑖, 𝑦) such that for all 𝑛 ∈ N it holds that (taken from [31]):
            (∀𝑥 1 . . . 𝑥𝑛 ) (∃𝑦) (∀𝑤) (∀𝑖) ((𝑖 ∈ N ∧ 1 ≤ 𝑖 ≤ 𝑛) =⇒ (𝑅(𝑤, 𝑖, 𝑦) ≡ (𝑤 = 𝑥𝑖 )))
This definition is w.r.t. a common domain for 𝑥 and 𝑦; however, this is not a strict requirement for
our dynamic theories where it would also suffice to encode sequences of values for variable 𝑣 in
the value set of another variable 𝑤 with ValsΔ (𝑣) ≠ ValsΔ (𝑤). Hence, we define Gödelization of
a variable 𝑣 w.r.t. a second variable 𝑤, which is a representative for the value range into which
sequences of values of 𝑣 are embedded. Given twin variables 𝑣,   ˜ 𝑤˜ for 𝑣, 𝑤, we then demand that
there exists a first-order formula G𝑣 (𝑤,
                                        ˜ 𝑛, 𝑗, 𝑣)
                                                ˜ that decodes an 𝑛-dimensional sequence of values
           ˜ extracts the 𝑗-th value, and asserts this component is “stored” in 𝑣.
stored in 𝑤,                                                                    ˜ Formally, this leads
to the following definition, which describes that the value range of 𝑣 ∈ Λ𝑉 supports Gödelization:
Definition B.4 (Gödelization Support). Let Δ be some dynamic theory that is inductively expressive
w.r.t. Λ𝑉 N . We say 𝑣 ∈ Λ𝑉 has Gödelization Support w.r.t. Λ𝑉 N iff there exists a variable 𝑤 ∈ Λ𝑉 and
some formula G𝑣 , called Gödel Formula, such that:
For any 𝑁 ∈ N and any vector of values 𝛿 ∈ ValsΔ (𝑣) 𝑁 there exists a value 𝜖 ∈ ValsΔ (𝑤) such that:
For any integer variables 𝑖, 𝑛 ∈ Λ𝑉 N and any twin variables 𝑣˜ (resp. 𝑤)
                                                                       ˜ of 𝑣 (resp. 𝑤) and any state 𝜇
with V (𝜇, 𝑤) ˜ = 𝜖 and N (V (𝜇, 𝑛)) = 𝑁 it holds that 𝜇 |=Δ G𝑣 (𝑤,      ˜ iff 1 ≤ 𝑘 = N (V (𝜇, 𝑗)) ≤ 𝑁
                                                                 ˜ 𝑛, 𝑗, 𝑣)
and V (𝜇, 𝑣) ˜ = 𝛿𝑘 .
   Some concrete examples of Gödelization would be:
    • In interpreted (integer) first-order dynamic logic, the variables support Gödelization using
       standard Gödel Numbers [29, 32]
    • In differential dynamic logic, real values have a Gödelization for a differentially expressive
       first-order structure (formalizable via our atoms) [51]
    • Under certain constraints, non-rigid functions (i.e., functions whose evaluation depends on
       the state) equally admit Gödelization [9]
For the relative completeness proofs below, we consequently demand that our underlying induc-
tively expressive dynamic theory is also Gödel Expressive:
Definition B.5 (Gödel Expressive). Consider a dynamic theory Δ that is inductively expressive w.r.t.
variables Λ𝑉 N . We say Δ is Gödel Expresive iff it satisfies the following properties:
   (Gödel Formulas) All variables 𝑣 ∈ Λ𝑉 support Gödelization w.r.t. Λ𝑉 N for a provided Gödel
                           Function G𝑣 (see Definition B.4).
     (Less Predicate) There exists a function nat< : Λ𝑉2 N → FOLΔ such that for variables 𝑣, 𝑤 ∈
                           Λ𝑉 N with 𝑣 ≠ 𝑤 and any state 𝜇 ∈ S:
                           𝜇 ∈ DJnat< (𝑣, 𝑤)K iff N (V (𝜇, 𝑣)) < N (V (𝜇, 𝑤))
   Communication in Heterogeneous Dynamic Theories. The properties described above concern a
single dynamic theory. We now discuss assumptions under which relative completeness results
can also be obtained for heterogeneous dynamic theories as described in Section 7. To this end,
one might hope that Gödelization and/or FOL expressiveness might be sufficient to prove relative
completeness of fully heterogeneous dynamic theories. Unfortunately, it turns out that this is not
quite sufficient yet: While subtle, Gödelization requires that the Gödel formulas over all variables use
the same set of integer expressive variables. However, by default, variables 𝑣 (0) ∈ Λ𝑉(0) from theory

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:32                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert



 By Definition:                                        Results for Havoc Lifting:
                      FolExp (Δ) =⇒Fin (Δ)                      Fin (Δ) =⇒Fin (Δ:=∗ )                               Lemma C.9
                                                                                              :=∗
 Theorem C.3:                                                  Göd (Δ) =⇒Göd (Δ )                                   Lemma C.9
                                                                                                       :=∗
 FolExp (Δ) ∧ FolRelCom (Δ) =⇒RelCom (Δ)                   FolExp (Δ) =⇒FolExp (Δ )                                Lemma C.10
                                                                                                             :=∗
                                                          RelCom (Δ) =⇒FolRelCom (Δ )                              Lemma C.11
 Results for Regular Program Lifting:
                                                      Fin (Δ) =⇒Fin (Δreg )                                        Lemma C.13
                                                                             reg
                                                     Göd (Δ) =⇒Göd (Δ              )                               Lemma C.13
                                                                                   reg
                                     Göd (Δ) ∧ FolExp (Δ) =⇒FolExp (Δ                    )                         Lemma C.14
                                                                                             reg
                   Göd (Δ) ∧ FolExp (Δ) ∧ RelCom (Δ) =⇒FolRelCom (Δ                                )         Lemma C.15, C.16
 Results for Heterogeneous Dynamic Theories:
                                                            
                            Fin Δ (0) ∧ Fin Δ (1) =⇒Fin Δ (01)                                                     Lemma C.8
                                                           
             Göd Δ (0) ∧ Göd Δ (1) ∧ Co Δ (01) =⇒Göd Δ (01)                                                        Lemma C.17
                                                              
        FolExp Δ (0) ∧ FolExp Δ (1) ∧ Co Δ (01) =⇒FolExp Δ (01)                                                    Lemma C.18
     FolExp Δ (0)  ∧ RelCom Δ (0)  ∧
                                                                    
                                                      =⇒FolRelCom Δ (01)                                     Lemma C.19, C.20
     FolExp Δ (1)   ∧ RelCom Δ  (1)   ∧ Co Δ (01)
                                                  


                                     Fig. 6. Results on Relative Completeness




Δ (0) and their Gödel Formulas G𝑣 (0) will be using a different set of integer expressive variables for
Gödelization (Λ𝑉(0)N ) than variables 𝑣 (1) ∈ Λ𝑉(1) from theory Δ (1) which rely on Λ𝑉(1)N . The requirement
that all Gödelizations use the same set of integer expressive variables is no definitional accident,
but indeed imperative for the derivation of loop renditions in regular programs: Without a common
“integer language” we cannot encode that both worlds evolve the loop to an equal number of
iterations and in lock-step. Hence, we must guarantee a minimal amount of information flow
between the two worlds, which must be implemented using suitable (equality) atoms in Λ𝐴                ∩ and

corresponding functions mapping variables to Λ -formulas:
                                                        (01)


Definition B.6 (Communicating Theories). Let Δ (0) , Δ (1) be two inductively expressive, FOL ex-
pressive dynamic theories with integer expressive sets Λ𝑉(0)N, Λ𝑉(1)N which together form Δ (01) . We say
Δ (0) , Δ (1) are communicating in Δ (01) iff the following properties are satisfied:

   (Z Communcation) There exists a function nat=(01) : Λ𝑉(0)N × Λ𝑉(1)N → FOLΛ (01) such that for
                      variables 𝑣 ∈ Λ𝑉(0)N, 𝑤 ∈ Λ𝑉(1)N and any state 𝜇 ∈ S:
                      𝜇 ∈ Δ (01) Jnat=(01) (𝑣, 𝑤)K iff N (0) V (01) (𝜇, 𝑣) = N (1) V (01) (𝜇, 𝑤)
                                                                                                

       (Eq Predicate) Δ (01) satisfies the Eq Predicate property from Definition B.3 on Δ (01) .



Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:33


B.2    A Calculus of Relative Completeness
To succinctly represent the property preservation and relative completeness results obtained from
our theory, we summarize and denote possible properties a dynamic theory (and its axiomatization)
may have as follows:
               Fin (Δ) Finite Support (Definition B.2)
           FolExp (Δ) FOL Expressiveness (Definition B.3)
              Göd (Δ) Gödel Expressiveness (Definition B.5)
       FolRelCom (Δ) Calculus of Dynamic Logic is relatively complete w.r.t. box and diamond
                       first-order formulas (i.e. 𝐹 FOL → [𝑝] 𝐺 FOL and 𝐹 FOL → ⟨𝑝⟩ 𝐺 FOL )
          RelCom (Δ) Relative Completeness (Definition 8.1)
               Co (Δ) Communicating heterogeneous dynamic theory (Definition B.6)
  Based on this formalization, we have derived the rules presented in Figure 6, describing under
which circumstances properties carry over from one dynamic theory to the next during lifting
and theory combination. While we defer details of these results to the Appendix, we can derive
Theorems B.1 and 8.1 from the results in Figure 6, which concern relative completeness under
regular program closure and for theory combination.
Theorem B.1 (Relative Completeness for Regular Programs). Let Δ be some FOL Expressive, Gödel
expressive, relatively complete dynamic theory with calculus ⊢Δ . Then Δreg is relatively complete with
the calculus ⊢Δreg from Section 6.2.
   Proof. Using the notation from Figure 6: We have FolExp (Δ), Göd (Δ),Fin (Δ),RelCom (Δ). Then
via Lemma C.13 get Fin (Δreg ). Via Lemma C.14 get FolExpr (Δreg ) and via Lemmas C.15 and C.16
get FolRelCom (Δreg ). Then via Theorem C.3 get RelCom (Δreg ).                                □
Theorem B.2 (Relative Completeness of Fully Heterogeneous Dynamic Theories). Let Δ (0) , Δ (1)
be two relatively complete, FOL expressive, Gödel Expressive dynamic theories with finite support that
are communicating in Δ (01) . Then the fully heterogeneous dynamic theory Δ̂ with its proof calculus
⊢Δ̂ is relatively complete.
   Proof. We use the notation and rules from Figure 6:
First, let us reconsider our assumptions: We have FolExp Δ (0) , Göd Δ (0) ,Fin Δ (0) ,RelCom Δ (0) .
                                                                                                       

We also have FolExp Δ (1) , Göd Δ (1) ,Fin Δ (1) ,RelCom Δ (1) . We further know Co Δ (01) .
                                                                                                 

   Using Lemmas C.19 and C.20 we get FolRelCom Δ (01) . Moreover have Göd Δ (01) (via Lemma C.17)
                                                                                            

and FolExp Δ (01) (via Lemma C.18). Together this yields RelCom Δ (01) via Theorem C.3.
                                                                               

   Via Lemma C.9 we moreover get Fin (Δ (01) ) :=∗ and Göd (Δ (01) ) :=∗ and we can further derive
                                                                            

FolExpr (Δ (01) ) :=∗ (Lemma C.10) and FolRelCom (Δ (01) ) :=∗ (Lemma C.11). Again, this yields
                                                                      

RelCom (Δ (01) ) :=∗ via Theorem C.3.
                      

   Based on this, Lemma C.13 yields Fin ((Δ (01) ) :=∗ ) reg and Göd ((Δ (01) ) :=∗ ) reg . Lemma C.14 then
                                                                                        

delivers FolExpr ((Δ (01) ) :=∗ ) reg and together with our relative completeness result for (Δ (01) ) :=∗
                                     

(RelCom (Δ (01) ) :=∗ ) this delivers FolRelCom ((Δ (01) ) :=∗) reg (Lemmas C.15 and C.16).
                                                                    

   Finally, this yields RelCom ((Δ (01) ) :=∗ ) reg ≡ RelCom Δ̂ (via Theorem C.3).
                                                   
                                                                                                          □

C     Proofs and Additional Definitions
C.1 Auxilliary Definitions and Lemmas
Lemma C.1 (Soundness of Free Variables). For any atom 𝑎 ∈ Λ𝐴 and 𝑝 ∈ Λ𝑃 :
                       FVΔ (𝑎) ⊆ FV𝐴 (𝑎)                             FVΔ (𝑝) ⊆ FV𝑃 (𝑝)

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:34                                               Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


Definition C.1 (Free Variables of First-Order Formulas). Given a dynamic theory Δ, we define the
syntactically free variables FVΔ over FmlΛ as follows:
    • FVΔ (𝑎) = FV𝐴 (𝑎) (for 𝑎 ∈ Λ𝐴 )
    • FVΔ (¬𝐹 ) = FVΔ (𝐹 )
    • FVΔ (𝐹 ∧ 𝐺) = FVΔ (𝐹 ) ∪ FVΔ (𝐹 )
    • FVΔ (∀𝑣 𝐹 ) = FVΔ (𝐹 ) \ {𝑣 }
    • FVΔ ( [𝑝] 𝐹 ) = FV𝑃 (𝑝) ∪ FVΔ (𝐹 )
Lemma C.2 (FVΔ is an Overapproximation). For any dynamic theory Δ and any formula 𝐹 ∈ FmlΛ
it holds that:
                                   FVΔ (𝐹 ) ⊆ FVΔ (𝐹 )
Definition C.2 (Free Variables over Regular Programs). For any dynamic theory Δ and its regular
closure over programs Λ𝑃 , we define FV𝑃 as follows:
                       reg             reg

    • FV𝑃 (𝑟 ) = FV𝑃 (𝑟 ) (for 𝑟 ∈ Λ𝑃 )
           reg
        reg             reg             reg  reg
    • FV𝑃 (𝑝; 𝑞) = FV𝑃 (𝑝 ∪ 𝑞) = FV𝑃 (𝑝) ∪ FV𝑃 (𝑞)
        reg
    • FV𝑃 (? (𝐹 FOL )) = FVΔ (𝐹 FOL )
    • FV𝑃 (𝑝) ∗ = FV𝑃 (𝑝)
        reg             reg


Theorem C.1 (Regular Closure forms KAT). The program constructs of the regular closure lifting
satisfy all axioms of a Kleene Algebra with Tests (see Definition C.3) where + is ∪, · is ;, 1 is ? (⊤), (·) ∗
is the nondeterministic loop and the boolean algebra is constructed over checks ? (·).2
Definition C.3 (Kleene Algebra with Tests). We base our definition of Kleene and Boolean Algebra
on prior literature [32, 40]. In the notation of this paper, our regular program lifting satisfies the Kleene
Algebra with Tests axioms if the following identitites hold:
    𝛼 ∪ (𝛽 ∪ 𝛾)  (𝛼 ∪ 𝛽) ∪ 𝛾               𝛼 ∪𝛽  𝛽 ∪𝛼          𝛼∪? (⊥)  𝛼                 𝛼 ∪𝛼  𝛼
         𝛼; (𝛽; 𝛾)  (𝛼; 𝛽) ; 𝛾          ? (⊤) ; 𝛼  𝛼           𝛼; ? (⊤)  𝛼            𝛼; (𝛽 ∪ 𝛾)  (𝛼; 𝛽) ∪ (𝛼; 𝛾)
? (⊤) ∪ (𝛼; 𝛼 ∗ )  𝛼 ∗                  ? (⊥) ; 𝛼 ? (⊥)        𝛼; ? (⊥) ? (⊥)         (𝛼 ∪ 𝛽) ; 𝛾  (𝛼; 𝛾) ∪ (𝛽; 𝛾)
? (⊤) ∪ (𝛼 ∗ ; 𝛼)  𝛼 ∗                             𝛼 ∪ (𝛽; 𝛾) ≲ 𝛾 → 𝛽 ∗ ; 𝛼 ≲ 𝛾
                                                    𝛼 ∪ (𝛾; 𝛽) ≲ 𝛾 → 𝛼; 𝛽 ∗ ≲ 𝛾
and if furthermore for any programs 𝛼, 𝛽, 𝛾 only containing checks as atomic programs the following
identitites hold:
𝛼 ∪ (𝛽 ∪ 𝛾)  (𝛼 ∪ 𝛽) ∪ 𝛾                    𝛼; (𝛽; 𝛾)  (𝛼; 𝛽) ; 𝛾              𝛼 ∪𝛽  𝛽 ∪𝛼              𝛼; 𝛽  𝛽; 𝛼
  𝛼 ∪ (𝛽; 𝛾)  (𝛼 ∪ 𝛽) ; (𝛼 ∪ 𝛾)           𝛼; (𝛽 ∪ 𝛾)  (𝛼; 𝛽) ∪ (𝛼; 𝛾)       𝛼∪?(⊥)  𝛼              𝛼∪?(⊤) ?(⊤)
         𝛼 ∪ 𝛼 ?(⊤)                            𝛼 ∪𝛼  𝛼                       𝛼; ?(⊤)  𝛼            𝛼; ?(⊥) ?(⊥)
          𝛼; 𝛼 ?(⊥)                                𝛼; 𝛼  𝛼
Where 𝛼 ≡? (¬F (𝛼)) and F (𝛼) is defined as follows:
                                                                                                F (𝜙) ∗ ≡ ⊤
                                                                                                       
         F (? (𝜙)) ≡ 𝜙             F (𝜙;𝜓 ) ≡ 𝜙 ∧ 𝜓              F (𝜙 ∪ 𝜓 ) ≡ 𝜙 ∨ 𝜓
Note that F (𝛼) for 𝛼 ∈ Λ𝑃 need not be defined as we assume all atomic programs to be checks
whenever F (·) is applied.
2 For negation of check constructs we introduce an additional operator which aggregates and negates a given program

consisting purely of checks (see Definition C.3).


Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:35


Lemma C.3 (Correctness of F (·)). If 𝛼 only contains checks as atomic programs then the following
identity holds:
                                         𝛼 ? (F (𝛼))
Definition C.4 (Free Variables for Simple Heterogeneous Domain of Computation). Given two
dynamic theories Δ (0) , Δ (1) and notation as in Definition 7.3, we define free variables of atoms and
programs as follows:
                        FV (0) (𝑎) 𝑎 ∈ Λ𝐴(0)                         (
                                                                        FV𝑃(0) (𝑝) 𝑎 ∈ Λ𝑃(0)
                       
                        𝐴(1)
                       
                                           (1)
          FV𝐴 (𝑎) = FV𝐴 (𝑎) 𝑎 ∈ Λ𝐴
             ˆ                                             FV𝑃 (𝑝) =
                                                            ˆ
                                                                        FV𝑃(1) (𝑝) 𝑎 ∈ Λ𝑃(1)
                                          Λ
                       
                        FV∩ (𝑎)
                       
                                     𝑎 ∈   ∩
                        𝐴                 𝐴

Theorem C.2 (Heterogeneous Rewriting). Let Δ (0) , Δ (1) be two dynamic theories and let Δ̂ be the
fully heterogeneous dynamic theory over Δ (0)       and Δ (1) . Then the following identities hold where
                                               reg

programs of Δ̂ are in magenta and programs of Δ (0)
                                                       reg
                                                            are in blue:
          ? (𝜙)  ? (𝜙)             𝛼 ∪𝛽 𝛼 ∪𝛽                   𝛼; 𝛽  𝛼; 𝛽              (𝛼) ∗  (𝛼) ∗

A corresponding result can be derived if some dynamic theory Δ (0) is combined with the regular
closure Δ (1)
               reg
                    .
Lemma C.4 (Identity Equality). For any dynamic theory Δ that is FOL Expressive or Communicating,
the following axiom holds for any 𝑣 ∈ Λ𝑉 :
                                                    𝑣  𝑣.
   Proof of Lemma C.4. Note, that 𝑣 is a twin variable of itself. Hence, by definition we know that
for all states 𝜇 ∈ DJ (𝑣, 𝑣)K iff V (𝜇, 𝑣) = V (𝜇, 𝑣) which holds in all states.                □

C.2   Definitions and Proofs for Relative Completeness Results
In order to reason more explicitly about the behavior of renditions, we require a vehicle to reason
more explicitly about renditions. To this end, note that due to the state independence property (see
Definition 4.3), a variable 𝑣 can be updated to any value from ValsΔ (𝑣) in any state. This gives rise
to the notion of twin states that allows us to selectively pull values of a twin variable from another
state:
Definition C.5 (Twin States). Let Δ be some dynamic theory and 𝑣, 𝑣 + be twin variable vectors from
                                                                 𝑣+
Λ𝑉 . For any two states 𝜇, 𝜎 ∈ S we define the twin state (𝜇, 𝜎) 𝑣 as the state that maps variables from
𝑣 + to the value of their twin 𝑣 in 𝜎 and otherwise to 𝜇, formally we require that:
                                              (
                                                V 𝜎, 𝑣 𝑖 𝑣 = 𝑣 +𝑖 for some 𝑖
                                                        
                                      𝑣+
                                         
                            V (𝜇, 𝜎) 𝑣 , 𝑣 =
                                                V (𝜇, 𝑣) else
  Note that due to the state independence property of the state space, we have for any twin variable
                                                   𝑣+
vectors 𝑣, 𝑣 + and any states 𝜇, 𝜎 ∈ S that (𝜇, 𝜎) 𝑣 ∈ S. We can then derive the following, equivalent
rendition property for a finite support dynamic theory:
Definition C.6 (Equivalent Rendition Definition). For a dynamic theory Δ with finite support we
                                                                                  𝑝 ∈ Λ𝑃 and all twin
say it supports rendition iff there exists a function S such that for all programs
variable vectors 𝑣, 𝑣 + with 𝑣 ⊇ Vars (𝑝) and 𝑣 ∩ 𝑣 + = ∅ the function S𝑝 𝑣, 𝑣 + returns a formula in
FOLΛ such that:
                          𝑣+
(𝜇, 𝜎) ∈ P (𝑝) iff (𝜇, 𝜎) 𝑣 |=Δ S𝑝 𝑣, 𝑣 + and 𝜇 ≡𝑣 ∁ 𝜎
                                         


                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:36                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


Proposition C.1. The definition in Definition C.6 is equivalent to the Rendition property as defined
in Definition B.3.
Lemma C.5 (Expressibility of Λ-formulas as first-order formulas). If a dynamic theory Δ is FOL
Expressive with finite support, then for every formula 𝐹 ∈ FmlΛ there exists a 𝐹 FOL ∈ FOLΛ such that
⊨Δ 𝐹 ↔ 𝐹 FOL .
  Proof. Proof by structural induction:
𝐹 ∈ FOLΛ In this case 𝐹 FOL ≡ 𝐹 .
𝐹 ≡ ¬𝐺    By structural induction we know there is a formula 𝐺 FOL such that ⊨Δ 𝐺 ↔ 𝐺 FOL . Then,
          it also holds that ⊨Δ 𝐹 ↔ ¬𝐺 FOL .
𝐹 ≡ [𝑝] 𝐺 By structural induction we know there is a formula 𝐺 FOL such that ⊨Δ 𝐺 ↔ 𝐺 FOL .
          Through our assumption of FOL Expressiveness, we also know that there exists a
                                                                 𝑣+
          formula S𝑝 such that (𝜇, 𝜎) ∈ P (𝑝) iff we have (𝜇, 𝜎) 𝑣 |=Δ S𝑝 𝑣, 𝑣 + and 𝜇 ≡𝑣 ∁ 𝜎.
                                                                                

          Hence, choose twin variable vectors 𝑣 ⊇ Vars (𝑝) ∪ FVΔ (𝐺 FOL ) and 𝑣 + . We then
          construct the following formula 𝐻 :
                          ∀𝑣 + S𝑝 𝑣, 𝑣 + → ∀𝑣 𝑣  𝑣 + → 𝐺 FOL .
                                                                   

              Let 𝜇 ∈ S be some state such that 𝜇 |=Δ 𝐻 . Then consider a state 𝜇˜ such that 𝜇 ≡               ˜
                                                                                                               𝜇.
                                                                                                      ( 𝑣+ ) ∁
                                                                                                   𝑣+
              Then we can interpret 𝜇˜ as a twin state for some 𝜎 such that 𝜇˜ ≡ (𝜇, 𝜎) 𝑣 and 𝜇 ≡𝑣 ∁ 𝜎.
              Then 𝜇˜ |=Δ S𝑝 𝑣, 𝑣 + iff (𝜇, 𝜎) ∈ P (𝑝). We consider the case where S𝑝 is satisfied by
                                      
               ˜ Then consider any state 𝜎˜ with 𝜇˜ ≡𝑣 ∁ 𝜎˜ and 𝜎˜ |=Δ 𝑣  𝑣 + . Then by assumption we
              𝜇.
              know that 𝜎˜ |=Δ 𝐺 FOL . However, we also know that 𝜎 ≡𝑣 𝜎,         ˜ because 𝜇˜ encodes the
              values of 𝜎 in 𝑣 + , 𝜎˜ has the same values as 𝜇˜ for 𝑣 + and 𝜎˜ has equal values for 𝑣 and 𝑣 + .
              Consequently, by coincidence we get that 𝜎 |=Δ 𝐺 FOL . Hence 𝜇 |=Δ [𝑝] 𝐺 FOL .
              Conversely, assume 𝜇 |=Δ [𝑝] 𝐺 FOL . In this case, we know that for any (𝜇, 𝜎) ∈ P (𝑝)
                                                        any 𝑉 ⊇ Vars (𝑝) we get 𝜇 ≡𝑉 𝜎. Then for any
              we get that 𝜎 |=Δ 𝐺 FOL . Importantly, for
              𝜇˜ with 𝜇 ≡𝑣 + ∁ 𝜇˜ with 𝜇˜ |=Δ S𝑝 𝑣, 𝑣 + (otherwise 𝜇˜ trivially satisfies the implication),
                                                                                         𝑣+
          we know that we can interpret 𝜇˜ as a twin state (𝜇, 𝜎)     ˜ 𝑣 with 𝜇 ≡𝑣 ∁ 𝜎.
                                                                                       ˜ We then
          know that (𝜇, 𝜎)˜ ∈ P (𝑝) and hence 𝜎˜ |=Δ 𝐺 FOL . However, just as before, we can then
          construct a state 𝜔 such that 𝜇˜ ≡𝑣 ∁ 𝜔 but 𝜔 |=Δ 𝑣  𝑣 + . Hence, 𝜎˜ ≡𝑣 𝜔 and hence by
          coincidence lemma 𝜔 |=Δ 𝐺 FOL . Hence, since 𝜔 merely represents an arbitrary state
          after instantiation of quantifiers for 𝜇, we get that 𝜇 |=Δ 𝐻 .
𝐹 ≡ ∀𝑣𝐺 By structural induction we know there is a formula 𝐺 FOL such that |=Δ 𝐺 ↔ 𝐺 FOL . Then
          it also holds that |=Δ ∀𝑣𝐺 ↔ ∀𝑣𝐺 FOL
𝐹 ≡ 𝐺 ∧ 𝐻 By structural induction we know there are formulas 𝐺 FOL and 𝐻 FOL such that ⊨Δ 𝐺 ↔
          𝐺 FOL and resp. ⊨Δ 𝐻 ↔ 𝐻 FOL . Then, it also holds that ⊨Δ 𝐹 ↔ 𝐺 FOL ∧ 𝐻 FOL .
                                                                                                □
Theorem C.3 (Relative Completeness). Let Δ be an FOL Expressive dynamic theory with finite
support. If its proof calculus ⊢Δ admits proving all valid formulas of the form 𝐹 FOL → [𝑝] 𝐺 FOL and all
valid formulas of the form 𝐹 FOL → ⟨𝑝⟩ 𝐺 FOL , then its proof calculus is relatively complete w.r.t. FOLΔ .
   Proof. While admitting more modularity through the properties outlined in Section 8, the basic
gist of the proof is structurally identical to similar proofs in prior literature [31, 51]. We assume we
are given a valid formula in conjunctive normal form (if not, perform appropriate propositional
recombination), where negations are pushed inside modalities and modalities are not pulled out
of conjunctions/disjunctions. Like [31], we perform induction over the number of modalities and

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:37


the number 𝑁 of non-trivial quantifiers, i.e. such quantifiers which have a modality inside. First,
note that the case for 𝑁 = 0 modalities and non-trivial quantifiers is covered by our assumption
of relative completeness: If the formula under consideration has no modalities, we can prove its
validity relative to FOLΔ . Next, consider the case 𝑁 + 1: We first consider the conjunctions of
formulas: Since the formula is valid, we can prove each conjunct separately. If a conjunction has 𝑁
modalities/non-trivial quantifiers, this case is already handled by the inductive hypothesis. For a
conjunct with 𝑁 + 1 modalities/non-trivial quantifiers, we must consider a disjunction. There exist
the following cases:
    𝐹 ∨ [𝑝] 𝐺 We then know that 𝐹, 𝐺 have fewer modalities than our considered formula (covered
              by case 𝑁 ). Thus, our calculus can already prove that 𝐹 ↔ 𝐹 FOL and 𝐺 ↔ 𝐺 FOL where
              𝐹 FOL, 𝐺 FOL are constructed according to Lemma C.5 (note that 𝐹 FOL, 𝐺 FOL have 𝑁 = 0
              modalities/non-trivial quantifiers). We can furthermore prove ¬𝐹 FOL → [𝑝] 𝐺 FOL
              by assumption. Via (MR) and propositional reasoning, we then derive ¬𝐹 → [𝑝] 𝐺.
              Propositional recombination then yields 𝐹 ∨ [𝑝] 𝐺.
    𝐹 ∨ ⟨𝑝⟩ 𝐺 Just as before, 𝐹, 𝐺 have fewer modalities and our proof calculus can hence prove
              𝐹 ↔ 𝐹 FOL and 𝐺 ↔ 𝐺 FOL which yields ¬𝐹 → ¬𝐹 FOL . Using 𝐺 FOL → 𝐺 with (G)
              and (𝐾 ⟨ ⟩ ) gives ⟨𝑝⟩ 𝐺 FOL → ⟨𝑝⟩ 𝐺. By assumption, we can then prove ¬𝐹 FOL →
              ⟨𝑝⟩ 𝐺 FOL . Using propositional recombination we can then derive ¬𝐹 → ⟨𝑝⟩ 𝐺 which
              then yields 𝐹 ∨ ⟨𝑝⟩ 𝐺.
     𝐹 ∨ ∀𝑣 𝐺
     𝐹 ∨ ∃𝑣 𝐺 Just as before, we know there exist first-order formulas 𝐹 FOL, 𝐺 FOL equivalent to
              𝐹, 𝐺. We leave ¬𝐹 FOL → ∀𝑣 𝐺 FOL (resp. ¬𝐹 FOL → ∃𝑣 𝐺 FOL ) as an exercise for our
              first-order oracle. It remains to prove that ¬𝐹 ↔ ¬𝐹 FOL and 𝐺 FOL ↔ 𝐺 (which
              we know to be true by construction). Importantly, these formulas have one non-
              trivial quantifier less and are hence covered by our inductive hypothesis. First-order
              recombination of these three provable formulas then yields 𝐹 ∨∀𝑣 𝐺 (resp. 𝐹 ∨ ∃𝑣 𝐺).
Overall, the induction demonstrates that any valid formula can be derived via the given calculus. □

Lemma C.6 (Bound Variables over Havoc Programs). Let Δ be a dynamic theory with finite support,
then Δ:=∗ also has finite support with the following BV𝑃:=∗ :
    • BV𝑃:=∗ (𝑟 ) = BV𝑃 (𝑟 ) (for 𝑟 ∈ Λ𝑃 )
    • BV𝑃:=∗ (𝑣 := ∗) = {𝑣 }
   Proof. First note that by construction if BV𝑃 is finite (assumed) then so is BV𝑃:=∗ . Next, we
consider the coverage property. We have proven this property via a structural induction proof in
Isabelle.                                                                                       □

Lemma C.7 (Bound Variables over Regular Programs). Let Δ be a dynamic theory with finite support,
then Δreg also has finite support with the following BV𝑃 :
                                                       reg

    • BV𝑃 (𝑟 ) = BV𝑃 (𝑟 ) (for 𝑟 ∈ Λ𝑃 )
          reg
        reg             reg             reg  reg
    • BV𝑃 (𝑝; 𝑞) = BV𝑃 (𝑝 ∪ 𝑞) = BV𝑃 (𝑝) ∪ BV𝑃 (𝑞)
        reg
    • BV𝑃 (? (𝐹 FOL )) = BV𝑃 (𝐹 FOL )
    • BV𝑃 (𝑝) ∗ = BV𝑃 (𝑝)
        reg              reg

                                                                                                    reg
   Proof. First note that by construction if BV𝑃 is finite (assumed) then so is BV𝑃 . Next, we
consider the coverage property. We have proven this property via a structural induction proof in
Isabelle.                                                                                      □


                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:38                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


Lemma C.8 (Bound Variables for Simple Heterogeneous Dynamic Theories). Let Δ (01) be the
simple heterogeneous dynamic theory over Δ (0) , Δ (1) . If both homogeneous dynamic theories have
finite support, then so has Δ (01) with the following BV𝑃(01) :
    • BV𝑃(01) (𝑟 ) = BV𝑃(0) (𝑟 ) (for 𝑟 ∈ Λ𝑃(0) )
    • BV𝑃(01) (𝑟 ) = BV𝑃(1) (𝑟 ) (for 𝑟 ∈ Λ𝑃(1) )

  Proof. First note that by construction if BV𝑃(0) and BV𝑃(1) are finite (assumed) then so is BV𝑃(01) .
Next, we consider the coverage property. We have proven this property via a structural induction
proof in Isabelle.                                                                                 □
C.2.1 Havoc and Relative Completeness. To illustrate on a simple example how relative complete-
ness results can be extended to lifted logics and heterogeneous dynamic theories, we begin by
demonstrating how relative completeness and similar properties of interest carry over when moving
from a dynamic theory Δ to its lifted version with havoc support Δ:=∗ . To this end, we recall the
axioms that we derived earlier for Δ:=∗ : (:=∗) allows us to replace a havoc operation by a first-order
quantifier, and (HR) allows us to reuse proof results for Δ. Intuitively, it is hence sensible that this
lifting would preserve relative completeness. Formally, we first observe the following:
Lemma C.9 (Trivial Liftings for Havoc). For an inductively expressive, Gödel expressive dynamic
theory Δ with finite support it holds that Δ:=∗ is inductively expressive, Gödel expressive and has finite
support
  Proof. Finite support is shown in Lemma C.6, inductive expressiveness and Gödel expressiveness
are first-order properties, i.e. they depend on the state space, the universe, the variables, and the
atoms. However, all these components of our dynamic theory are not modified by the lifting.
Consequently, Δ:=∗ is inductively expressive by the same argument as Δ.                             □
   We can next consider the property of FOL Expressiveness. We observe that FOL Expressiveness
also carries over to Δ:=∗ :
Lemma C.10 (FOL Expressiveness for Havoc Lifting). For an FOL expressive dynamic theory Δ it
holds that Δ:=∗ is also FOL expressive.
  Proof. Towards Infinite Variables and Eq Predicate note that (·) :=∗ does not modify the state
space nor the variable set. Consequently, this property automatically transfers.
  Towards Rendition we note that for all programs 𝑝 ∈ Λ𝑃 the property is already satisfied. In
addition, we propose the following encoding for the havoc operation:
                                                 Û
                                    S𝑤:=∗ 𝑣, 𝑣 + ≡     𝑣  𝑣+
                                                              𝑣 ∈𝑣
                                                              𝑣≠𝑤
Since it holds that (𝜇, 𝜎) ∈ P (𝑤 := ∗) iff 𝜇 ≡ {𝑤 } ∁ 𝜎, it naturally follows that (𝜇, 𝜎) ∈ P (𝑤 := ∗) iff
                    𝑣+
𝑣 ≡𝑣 ∁ 𝑤 and (𝜇, 𝜎) 𝑣 |=Δ:=∗ 𝑣 ∈𝑣 𝑣  𝑣 + . Consequently, Δ:=∗ is FOL Expressive.
                             Ó
                                                                                                         □
                                   𝑣≠𝑤

  By extending the calculus ⊢Δ of Δ by the axiom (:=∗) and the rule (HR), we can show that the
extended calculus ⊢Δ:=∗ can derive all valid first-order safety and diamond properties:
Lemma C.11 (Box and Diamond Properties for Havoc Lifting). Consider a dynamic theory Δ
with relatively complete proof calculus ⊢Δ . The extended proof calculus ⊢Δ:=∗ is relatively complete for
formulas of the following two forms where 𝐹 FOL, 𝐺 FOL ∈ FOLΛ:=∗ and 𝑝 ∈ Λ:=∗𝑃 :
                          𝐹 FOL → [𝑝] 𝐺 FOL                              𝐹 FOL → ⟨𝑝⟩ 𝐺 FOL

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                                   217:39


  Proof. We first consider box properties and perform a case distinction over 𝑝:
       𝑝 ∈ Λ𝑃 In this case, the formula is part of FmlΔ . Since ⊢Δ is relatively complete, there exists
               a first-order formula |=Δ 𝐻 FOL ∈ FOLΔ such that 𝐻 FOL ⊢Δ 𝐹 FOL → [𝑝] 𝐺 FOL . Using
               (HR) we can hence derive 𝐻 FOL ⊢Δ:=∗ 𝐹 FOL → [𝑝] 𝐺 FOL and furthermore |=Δ 𝐻 FOL .
   𝑝 ≡ 𝑣 := ∗ In this case, we can apply (:= ∗) and via propositional reasoning we arrive at
               the equivalent formulation 𝐹 FOL → ∀𝑣 𝐺 FOL . Since this first-order formula is
               equivalent and we assumed validity, we have that |=Δ:=∗ 𝐹 FOL → ∀𝑣 𝐺 FOL and
               𝐹 FOL → ∀𝑣 𝐺 FOL ⊢Δ:=∗ 𝐹 FOL → [𝑝] 𝐺 FOL
Next, we consider diamond properties. To this end, note that for 𝑝 ∈ Λ𝑃 we can make the structurally
same argument. For 𝑣 := ∗ we swap ∀ for ∃ and apply the same argument as above.                      □
  Using these Lemmas, we can then prove the following result:
Lemma C.12 (Relative Completeness for Havoc Lift). Let Δ be some FOL Expressive relatively
complete dynamic theory with calculus ⊢Δ . Then Δ:=∗ is relatively complete with the calculus ⊢Δ:=∗
from Section 6.1.
  Proof. This is a corollary of Theorem C.3 using Lemmas C.9 to C.11                                                    □
   The case of the havoc lifting is quite straight forward, however, we can apply similar principles
to the case of regular programs which will be discussed next.
C.2.2   Regular Programs and Relative Completeness.
Lemma C.13 (Trivial Liftings for Regular Programs). For an inductively expressive, Gödel expressive
dynamic theory Δ with finite support it holds that Δreg is inductively expressive, Gödel expressive and
has finite support
  Proof. Finite support is shown in Lemma C.7, inductive expressiveness and Gödel expressiveness
are first-order properties, i.e. they depend on the state space, the universe, the variables, and the
atoms. However, all these components of our dynamic theory are not modified by the lifting.
Consequently, Δreg is inductively expressive by the same argument as Δ.                             □
Lemma C.14 (FOL Expressiveness for Regular Lifting). For an FOL expressive, Gödel Expressive
dynamic theory Δ with finite support, it holds that Δreg is also FOL expressive.
  Proof. Towards Infinite Variables and Eq Predicate note that (·) reg does not modify the state
space nor the variable set. Consequently, this property automatically transfers.
  We will now focus on Rendition: To prove this property, we must construct a program rendition
S𝑝 for all programs 𝑝 ∈ Λ𝑃 . To this end, we first compute 𝑉 = FV𝑃 [Δreg ] (𝑝) ∪ BV𝑃 (𝑝) and then
                            reg                                                           reg

proceed as follows where 𝑣, 𝑣 +, 𝑤, 𝑣,˜ 𝑤˜ are twin variable vectors and all contain twin variables of all
variables in 𝑉 . Note that 𝑉 is finite and |𝑉 | is syntactically fixed. Hence, quantifiers over variable
vectors are to be understood as a sequence of quantifiers instantiating all |𝑉 | variables. Since we
assume Δ to be FOL Expressive, we can skip the case for 𝑝 ∈ Λ𝑃 (given by assumption) and focus
on the case 𝑝 ∈ Λ𝑃 \ Λ𝑃 :
                    reg


        S𝑝;𝑞 𝑣, 𝑣 + ≡ ∃𝑤 S𝑝 𝑣, 𝑤 ∧ S𝑞 𝑤, 𝑣 +                  for 𝑝, 𝑞 ∈ Λ𝑃
                                                                      reg


       S𝑝∪𝑞 𝑣, 𝑣 + ≡ S𝑝 𝑣, 𝑣 + ∨ S𝑞 𝑣, 𝑣 +                    for 𝑝, 𝑞 ∈ Λ𝑃
                                                                      reg
                        Û
              ˜ 𝑣+ ≡       𝑣˜  𝑣 + ∧ ∀𝑣 𝑣  𝑣˜ → 𝐹
                                                     
       S?(𝐹 ) 𝑣,                                              for 𝐹 ∈ FmlΛreg iff 𝑣˜ ≠ 𝑣 ⊇ FVΔ (𝐹 )
                                                                                       𝑃
                          𝑣 ∈𝑉
                          Û
        S?(𝐹 ) 𝑣, 𝑣 + ≡          𝑣  𝑣+ ∧ 𝐹
                     
                                                                       for 𝐹 ∈ FmlΛreg else
                                                                                       𝑃
                          𝑣 ∈𝑉


                                    Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:40                                                Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


For the case of loops, let 𝑘, 𝑛 ∈ Λ𝑉 N be integer expressive variables of Δ. Let 𝑣 be 𝑀 dimensional,
then 𝑍 1, . . . , 𝑍 𝑀 is a sequence of fresh variables such that 𝑍𝑖 is a twin variable of the variable 𝑤 that
admits Gödelization for 𝑣 𝑖 (remember that 𝑣 𝑖 may only admit Goedelization w.r.t. variables with a
different value      set represented by 𝑤). We can then construct the following first-order formula for
S (𝑝 ) ∗ 𝑣, 𝑣 + :
               
                                       
                 ∃𝑛∃𝑍 1 . . . ∃𝑍 𝑀 (0)
                    𝑀
                    Û                                               
                          G𝑣 𝑗 𝑍 𝑗 , 𝑛, 1, 𝑣 𝑗 ∧ G𝑣 𝑗 𝑍 𝑗 , 𝑛, 𝑛, 𝑣 + 𝑗 ∧
                    𝑗=1
                    ∀𝑘∃𝑤∃𝑤˜
                                                      𝑀
                                                                                                                  !
                                                     Û                                                    
                     0 < 𝑘 < 𝑛 → S𝑝 𝑤, 𝑤˜ ∧                  G𝑣 𝑗 𝑍 𝑗 , 𝑛, 𝑘, 𝑤 𝑗 ∧ G𝑣 𝑗 𝑍 𝑗 , 𝑛, 𝑘 + 1, 𝑤˜ 𝑗
                                                       𝑗=1
                


Note that 0 < 𝑘 and 𝑘 < 𝑛 can be encoded via nat< and 𝑘 + 1 can be encoded as follows:
                                                                   
                               ∃𝑘˜ nat+1 𝑘, 𝑘˜ ∧ G𝑣 𝑗 𝑍 𝑗 , 𝑛, 𝑘,
                                                               ˜ 𝑤˜
                                                                    𝑗

Further, for 𝑜,˜ 𝑧˜ ∈ Λ𝑉 N the literals 0 and 1 inside a formula 𝐹 can resp. be encoded as 𝑧,      ˜ 𝑜˜ via
∃𝑜˜ ∃𝑧˜ (¬nat>0 (𝑧) ˜ ∧ nat+1 (𝑧,   ˜ ∧ 𝐹 ).
                                 ˜ 𝑜)
   We now need to prove that S𝑝 the way defined above indeed satisfies our definition of program
renditions. To this end, we proceed via structural induction over the programs where 𝑝 ∈ Λ𝑃 is
given by assumption.
Remaining Base Case:
   ? (𝐹 ) By definition we know that (𝜇, 𝜎) ∈ P reg (? (𝐹 )) iff 𝜇 ≡Λ𝑉 𝜎 and 𝜇 |= 𝐹 . This is the case iff
                          𝑣+
          we have (𝜇, 𝜎) 𝑣˜ |=Δreg 𝑣 ∈𝑉 𝑣˜  𝑣 + ∧ ∀𝑣 𝑣  𝑣˜ → 𝐹 and 𝜇 ≡𝑣 ∁ 𝜎. Note that we require
                                     Ó                              

          the ∀ around 𝐹 since we have no infrastructure for rewriting 𝐹 with a different set of
          variables. This is due to our minimal set of assumptions about first-order atoms. For the
          case that the first argument of S?(𝐹 ) already coincides with the variables of 𝐹 , we provide
          the case without quantification.
Inductive Cases:
We assume that for 𝑝, 𝑞 ∈ Λ𝑃 there exist program renditions S𝑝 , S𝑞 .
                                reg

𝑝; 𝑞       By definition of sequential composition for any (𝜇, 𝜔) ∈ P reg (𝑝; 𝑞) there exists a state
           𝜎 ∈ S reg such that (𝜇, 𝜎) ∈ P reg (𝑝) and (𝜎, 𝜔) P reg (𝑞). By our inductive assumption, we
                                                                           𝑣+
           then know (𝜇, 𝜎) ∈ P reg (𝑝) iff we have 𝜇 ≡𝑣 ∁ 𝜎 and (𝜇, 𝜎) 𝑣 |=Δreg S𝑝 (𝑣, 𝑣 + ). Further, we
                                                                                𝑣+
          know that (𝜎, 𝜔) ∈ P reg (𝑞) iff 𝜎 ≡𝑣 ∁ 𝜔 and (𝜎, 𝜔) 𝑣 |=Δreg S𝑞 (𝑣, 𝑣 + ). It is then straight
                                                                                     𝑣+
          forward that (𝜇, 𝜔) ∈ P reg (𝑝; 𝑞) iff 𝜇 ≡𝑣 ∁ 𝜔 and (𝜎, 𝜔) 𝑣 |=Δreg S𝑝;𝑞 (𝑣, 𝑣 + ) (note we get
          𝜇 ≡𝑣 ∁ 𝜔 from the two inductive assumptions).
𝑝 ∪𝑞      By definition of nondeterministic choice we know that (𝜇, 𝜎) ∈ P reg (𝑝 ∪ 𝑞) iff (𝜇, 𝜎) ∈
          P reg (𝑝) or (𝜇, 𝜎) ∈ P reg (𝑞). Combining the inductive hypotheses, this yields that (𝜇, 𝜎) ∈
                                                             𝑣+
          P reg (𝑝 ∪ 𝑞) iff 𝜇 ≡𝑣 ∁ 𝜎 and furthermore (𝜎, 𝜔) 𝑣 |=Δreg S𝑝∪𝑞 (𝑣, 𝑣 + ).
(𝑝) ∗                                               reg (𝑝) ∗ iff for some 𝑁 ∈ N it holds that (𝜇, 𝜎) ∈
                                                             
          We know
                      definition that (𝜇, 𝜎) ∈ P
                      by
           P reg (𝑝) 𝑁 . Again, by definition this is the case iff there exist states 𝜇˜ 1, . . . , 𝜇˜ 𝑁 such that

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                               217:41


         𝜇 = 𝜇˜ 1 , 𝜇˜ 𝑁 = 𝜎 and for all 1 ≤ 𝑘 < 𝑁 it holds that ( 𝜇˜𝑘 , 𝜇˜𝑘+1 ) ∈ P reg (𝑝). We now need to
                                                   𝑣+
         show that this is the case iff (𝜇, 𝜎) 𝑣 |=Δ S (𝑝 ) ∗ 𝑣, 𝑣 + and 𝜇 ≡𝑣 ∁ 𝜎.
                                                                          

         We show this by initializing the existential variables of the formula. To this end (via state
         independence), pick a state 𝜔 that is equal to 𝜇 everywhere except for:
         – N (V reg (𝜔, 𝑛)) = 𝑁
         – For all variables 𝑣 𝑗 the variable 𝑍 𝑗 are assigned to the corresponding value for the
           sequence
                                                                              
                                      V reg 𝜇˜ 1, 𝑣 𝑗 , . . . , V reg 𝜇˜ 𝑁 , 𝑣 𝑗
          w.r.t. the Gödel-Predicate G𝑣 𝑗 . That is, we assign 𝑍 𝑗 a Gödel-Encoding of the sequence
           of values that 𝑣 𝑗 took on across all 𝑁 loop iterations.                                    
         The latter assignments of 𝑍 𝑗 ensure that 𝜔 |= 𝑀
                                                         Ó                                              +
                                                           𝑗=1 G𝑣 𝑗 𝑍 𝑗 , 𝑛, 1, 𝑣 𝑗 ∧ G𝑣 𝑗 𝑍 𝑗 , 𝑛, 𝑛, 𝑣 𝑗 as

         we previously asserted that 𝜇 = 𝜇˜ 1 and 𝜇˜𝑛reg = 𝜎. And the first/last element of 𝑍 𝑗(𝑖 ) ’s series
         evaluates to the values of 𝑣 𝑗 in 𝜇/𝜎. We also know that for all 1 ≤ 𝐾 < 𝑁 it holds that
                                                         𝑣+
         ( 𝜇˜𝐾 , 𝜇˜𝐾+1 ) ∈ P reg (𝑝) iff ( 𝜇˜𝐾 , 𝜇˜𝐾+1 ) 𝑣 |=Δ S𝑝 𝑣, 𝑣 + and 𝜇˜𝐾 ≡𝑣 ∁ 𝜇˜𝐾+1 . We still need to show
                                                                        

         that 𝜔 satisfies the remaining formula. To this end, consider any version of 𝜔 after the the
         quantifier ∀𝑘 (denoted 𝜔).    ˜ To this end, consider the case where 0 < 𝐾 = N (V reg (𝜔,          ˜ 𝑘)) <
         N (V (𝜔,  reg  ˜ 𝑛)) = 𝑁 (the other case trivially satisfies the implication). For any such 𝐾, 𝜔˜
         can be updated     for 𝑤 and 𝑤˜ such that they are (component wise) assigned to the values
         of V reg 𝜇˜𝐾 , 𝑣 and V reg 𝜇˜𝐾+1, 𝑣 . Since we know that ( 𝜇˜𝐾 , 𝜇˜𝐾+1 ) ∈ P reg (𝑝) and recalling
         the condition on S𝑝 from above, this yields that:
                                        𝑀                                               
                                       Û
              𝜔˜ |=Δreg ∃𝑤∃𝑤˜ S𝑝 𝑤, 𝑤˜ ∧   G𝑣 𝑗 𝑍 𝑗 , 𝑛, 𝑘, 𝑤 𝑗 ∧ G𝑣 𝑗 𝑍 𝑗 , 𝑛, 𝑘 + 1, 𝑤˜ 𝑗
                                               𝑗=1

         In conclusion, 𝜔 satisfies all parts of the formula of S (𝑝 ) ∗ 𝑣, 𝑣 + . Remember that 𝜔˜ only
                                                                               
         varies from 𝜔 in existentially quantified variables. Thus, by coincidence lemma we get
                     𝑣+
         that (𝜇, 𝜎) 𝑣 |=Δreg S (𝑝 ) ∗ and via the coincidence lemma and bounded effect, we also know
                                                                                     𝑣+
         that 𝜇 ≡𝑣 ∁ 𝜎. Conversely, given a state 𝜔 such that 𝜔 = (𝜇, 𝜎) 𝑣 |=Δreg S (𝑝 ) ∗ with 𝜇 ≡𝑣 ∁ 𝜎,
         we can reconstruct a program run of the loop: The existential instantiation of 𝑛 tells us the
         number of loop iterations and the sequences encoded in 𝑍 𝑗 (which by construction must
         all be sequences of length 𝑛) provide us with values for the intermediate states, where it is
         ensured that all loop steps correspond to the transition relation of 𝑝. Overall, this yields
                                                            𝑣+
         that (𝜇, 𝜎) ∈ P reg (𝑝 ∗ ) iff 𝜇 ≡𝑣 ∁ 𝜎 and (𝜇, 𝜎) 𝑣 |=Δreg S (𝑝 ) ∗
This concludes our proof which showed that for all programs 𝑝 ∈ Λ𝑃 it holds that (𝜇, 𝜎) ∈ P reg (𝑝)
                                                                               reg

         𝑣+
iff (𝜇, 𝜎) 𝑣 |=Δreg S𝑝 and 𝜇 ≡𝑣 ∁ 𝜎                                                                                 □

Lemma C.15 (Box Properties for Regular Programs). Consider an FOL expressive, Gödel expressive
dynamic theory Δ with finite support and a relatively complete proof calculus ⊢Δ . The extended proof
calculus ⊢Δreg is relatively complete for formulas of the form 𝐹 FOL → [𝑝] 𝐺 FOL with 𝐹 FOL, 𝐺 FOL ∈
FOLΛreg and 𝑝 ∈ Λ𝑃
                    reg


  Proof. Note that due to our assumptions, we know that Δreg is FOL expressive. We perform the
proof by structural induction over programs in a similar fashion to Harel et al. [31] and Platzer [51]
while obtaining the base case from assumptions:

                                Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:42                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


𝑝 ∈ Λ𝑃        In this case, the formula is in FmlΛ . Since the formula is valid and ⊢Δ is relatively
              complete, we can use (RR) do relatively completely derive the formula in Δreg using ⊢Δ .
𝑝 ≡? (𝐻 )     By applying the axiom (?) we get a formula which is equivalent and modality free,
              namely 𝐹 FOL → (𝐻 → 𝐺 FOL ).
𝑝 ≡𝑞 ∪𝑟       By applying the axiom (∪) we get a formula which is equivalent, namely (after propo-
              sitional restructuring) (𝐹 FOL → [𝑞] 𝐺 FOL ) ∧ (𝐹 FOL → [𝑟 ] 𝐺 FOL ). We can then prove
              these two parts of the conjunction separately. By inductive assumption, our calculus is
              capable of proving the two statements, as they must both be valid.
𝑝 ≡ 𝑞; 𝑟      By applying the axiom (;) we get an equivalent formula, namely 𝐹 FOL → [𝑞] [𝑟 ] 𝐺 FOL .
              Using Lemma C.5, we know there is a formula 𝐻 FOL ∈ FmlΛ such that |=Δ 𝐻 FOL ↔
              [𝑟 ] 𝐺 FOL . We then apply (MR) w.r.t. 𝐻 FOL , which yields two proof obligations. First,
              we have to prove 𝐹 FOL → [𝑝] 𝐻 FOL . By construction of 𝐻 FOL , this is equivalent to the
              original formulation. Therefore, this formula is valid and can be proven according to
              our inductive assumption. Secondly, we have to prove 𝐻 FOL → [𝑝] 𝐺 FOL .. As the two
              sides are, by construction, equivalent, this is equally a valid formula which can be
              proven according to our
                                      inductive assumption.
𝑝 ≡ (𝑞) ∗     First, note that (𝑞) ∗ 𝐺 FOL is a provable invariant: Via (∗ ) we get (𝑞) ∗ 𝐺 FOL →
                                                                                            
                    ∗
              [𝑞] (𝑞) 𝐺 FOL . Using (ind) this implies that the formula is an invariant. Using Lemma C.5,
              we construct the formula 𝐻 FOL which is equivalent to (𝑞) ∗ 𝐺 FOL . Then the formula
                                                                            

              𝐹 FOL → 𝐻 FOL is valid and first-order. Moreover, the formula (𝑞) ∗ 𝐺 FOL → 𝐺 FOL is
                                                                                    

              valid (as 𝐺 FOL must also hold after 0 iterations) which yields the validity of 𝐻 FOL →
              𝐺 FOL which is again a first-order formula. Thus, we first adjust the lefthand-side  via
              𝐹 FOL → 𝐻 FOL and then apply (MR) with 𝐻 FOL . The formula 𝐻 FOL → (𝑞) ∗ 𝐻 FOL is
                                                                                               

              then valid and provable using (ind) via the induction hypothesis and the right side
              𝐻 FOL → 𝐺 FOL is valid and a first-order provable.
                                                                                                      □
Lemma C.16 (Diamond Properties for Regular Programs). Consider an FOL expressive, Gödel
expressive dynamic theory Δ with finite support and a relatively complete proof calculus ⊢Δ . The
extended proof calculus ⊢Δreg is relatively complete for formulas of the form 𝐹 FOL → ⟨𝑝⟩ 𝐺 FOL with
𝐹 FOL, 𝐺 FOL ∈ FOLΛreg and 𝑝 ∈ Λ𝑃 .
                                reg


    Proof. Note that due to our assumptions we know that Δreg is FOL expressive. We perform the
proof by structural induction over programs in a similar fashion to Harel et al. [31] and Platzer [51]
while obtaining the base case from assumptions:
𝑝 ≡ 𝑞; 𝑟    By applying the axiom (;) we get an equivalent formula namely 𝐹 FOL → ⟨𝑞⟩ ⟨𝑟 ⟩ 𝐺 FOL .
            Then using Lemma C.5 get a formula 𝐻 FOL such that |=Δreg 𝐻 FOL ↔ ⟨𝑟 ⟩ 𝐺 FOL . Due to
            the assumed validity in combination with the inductive hypothesis we can then use
            ⊢Δreg to (relatively) prove 𝐹 FOL → ⟨𝑞⟩ 𝐻 FOL and 𝐻 FOL → ⟨𝑟 ⟩ 𝐺 FOL . From the latter via
            (G) (with 𝑞) and (𝐾 ⟨ ⟩ ) get ⟨𝑞⟩ 𝐻 FOL → ⟨𝑞⟩ ⟨𝑟 ⟩ 𝐺 FOL . Via propositional reasoning this
            yields 𝐹 FOL → ⟨𝑞⟩ ⟨𝑟 ⟩ 𝐺 FOL .
...         For checks and choice the proof follows directly from the dual version of the proof for
            Lemma C.15. For example, for check we apply the dual interpretation of (?) ⟨? (𝜙)⟩ 𝜓 ≡
            ¬ [? (𝜙)] ¬𝜓 ≡ ¬ (𝜙 → ¬𝜓 ) ≡ 𝜙 ∧ 𝜓 . Similar arguments follow for the other composi-
            tion primitives besides loops, which we will discuss now.
𝑝 ≡ (𝑞) ∗ For loops we instantiate the first-order formula for (𝑞) ∗ 𝐺 FOL (see Lemma C.5) via the
            loop construction from Lemma C.14 while dropping the outer existential quantification
            of ∃𝑛. Instead, we choose 𝑛, 𝑚 ∈ Λ𝑉 N in such a way that it is a fresh variable . We refer

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                                       217:43


               to this formula as 𝐻 FOL (𝑛). The formula
                   ∀𝑛 nat>0 (𝑛) → ⟨𝑞⟩ ∀𝑚 (nat+1 (𝑚, 𝑛) → ∀𝑛 (nat= (𝑛, 𝑚) → 𝐻 FOL (𝑛)))
               then is valid, because the reachability of a state satisfying 𝐺 after 𝑛 states implies there
               exists a state transition via 𝑞 such that after one iteration we can reach 𝐺 in 𝑛 − 1
               transitions. Thus, we can prove the formula above via inductive assumption. Via (G)
               we can then derive the precondition for (C) which yields
                               ∀𝑛 𝐻 FOL (𝑛) → ⟨𝑞 ∗ ⟩ ∃𝑛 (¬nat>0 (𝑛) ∧ 𝐻 FOL (𝑛))
               We then know that 𝐹 FOL → ∃𝑛 𝐻 FOL (𝑛) is valid (due to the validity of 𝐹 FOL →
                (𝑝) ∗ 𝐺 FOL ) which implies that we can derive it via first-order reasoning. Moreover, it is
               valid (and thus derivable via first-order reasoning) that ∃𝑛 (¬nat>0 (𝑛) ∧ 𝐻 FOL (𝑛)) →
               𝐺 FOL . Using (G) and further reasoning via (𝐾 ⟨⟩ ), this yields that:
                               (𝑝) ∗ ∃𝑣 (¬nat>0 (𝑛) ∧ 𝐻 FOL (𝑛)) → (𝑝) ∗ 𝐺 FOL .
               Via Modus Ponens, we can therefore derive that (𝑝) ∗ 𝐺 FOL
                                                                                                                           □
C.2.3    Heterogeneous Dynamic Theories and Relative Completeness.
Lemma C.17 (Gödel Encodings for Simple Heterogeneous Dynamic Theories). Let Δ (0) , Δ (1) be
two Gödel expressive dynamic theories that are communicating and together form Δ (01) . Then Δ (01) is
also Gödel expressive.

   Proof. For any variable in Λ𝑉(0) we leave the Gödel formula as is. For any variable in 𝑣 ∈ Λ𝑉(1)
(encoded in 𝑤 ∈ Λ𝑉(1) ) and 𝑛 (0) , 𝑗 (0) ∈ Λ𝑉(0)N, 𝑛 (1) , 𝑗 (1) ∈ Λ𝑉(1)N have:
                                                                                                         
G𝑣 𝑤, 𝑛 (0) , 𝑗 (0) , 𝑣 ≡ ∃𝑛 (1) ∃𝑗 (1) nat=(01) 𝑛 (0) , 𝑛 (1) ∧ nat=(01) 𝑗 (0) , 𝑗 (1) ∧ G𝑣 𝑤, 𝑛 (1) , 𝑗 (1) , 𝑣

This translates the integer indices 𝑛 (0) , 𝑗 (0) into integer expressive variables native to Δ (1) .                      □

Lemma C.18 (FOL Expressiveness). Let Δ (0) , Δ (1) be two FOL expressive dynamic theories that are
communicating in Δ (01) . Then Δ (01) is also FOL expressive.

  Proof. For Infinite Variables note that the value ranges of variables for any 𝑣 ∈ Λ𝑉(𝑖 ) has not
changed. Hence, since Δ (0) , Δ (1) have the infinite variable property, so has Δ (01) . For Eq Predicate
this is enforced via the assumption that Δ (0) , Δ (1) are communicating in Δ (01) (and thus via new
atoms in Λ𝐴 ∩ ).

  The Rendition is constructed as follows:
                                                          Û
             S𝑝 𝑣, 𝑣 + ≡ S𝑝(𝑖 ) 𝑣 | Λ (𝑖 ) , 𝑣 + | Λ (𝑖 ) ∧   𝑣  𝑣+            for 𝑝 ∈ Λ𝑃(𝑖 )
                      
                                         𝑉          𝑉
                                                               (1−𝑖 )
                                                           𝑣 ∈Λ𝑉        ∩𝑣
                                              
Where 𝑣 | Λ (𝑖 ) = 𝑣 1(𝑖 ) , . . . , 𝑣𝑚(𝑖 )(𝑖 ) with 𝑣 1(𝑖 ) , . . . , 𝑣𝑚(𝑖 )(𝑖 ) corresponding to the (syntactically created)
               𝑉

subvector of 𝑣 whose variables are in Λ𝑉(𝑖 ) and 𝑣 + | Λ (𝑖 ) contains the corresponding twin variables.
                                                                   𝑉
With our assumption about the correctness of S𝑝 in the FOL Expressive dynamic theory Δ (𝑖 ) , this
immediately implies that Δ (01) equally has the rendition property. Note that we may not assume
finite support in this proof, as we solely rely on the correctness of the FOL expressivity of the
underlying logics.                                                                              □

                                    Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:44                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


Lemma C.19 (Box Properties for Simple Heterogeneous Theories). Let Δ (0) , Δ (1) be two relatively
                                                                     are communicating in Δ .
complete, FOL expressive dynamic theories with finite support that                                (01)

Consider now the simple heterogeneous dynamic theory (i.e. Δ   (01)  ), then its proof calculus ⊢Δ (01)
is relatively complete for formulas of the form 𝐹 FOL → [𝑝] 𝐺 FOL with 𝐹 FOL, 𝐺 FOL ∈ FOLΔ (01) , 𝑝 ∈
FOLΛ (01) .
         𝑃

   Proof. In contrast to similar proofs (e.g. Harel et al. [31] and Platzer [51]), the major challenge in
deriving relative completeness is the case where 𝑝 ∈ Λ𝑃(𝑖 ) but 𝐹 FOL, 𝐺 FOL ∈ FmlΛ (01) , i.e. the formulas
may contain predicates, functions and variables from both theories. We tackle this case, which is in
fact the only one for programs 𝑝 ∈ Λ𝑃(01) , as follows:
  𝑝 ∈ Λ𝑃(𝑖 ) In this case we must discharge the reasoning about 𝑝 to the homogeneous calculus ⊢Δ (𝑖 ) .
             However, 𝐹 FOL and 𝐺 FOL are first-order formulas over Λ (01) and can therefore contain
             variables or atoms not native to Λ (𝑖 ) . Thus, we cannot simply hand the formula to ⊢Δ (𝑖 ) .
             Instead, for each 𝑣 ∈ Vars (𝑝) we apply the rule (ghost) (keeping in mind Lemma C.4)
             with 𝑣 − = 𝑣 for a fresh variable 𝑣 − . Decomposition of the introduced modalities using
             (:=∗), (;) and (?) coupled with further simplification using first-order reasoning yields
               𝐹 FOL ∧ 𝑣 −  𝑣 → [𝑝] 𝐺 FOL
             We can then derive the validity of the following formula (note that all 𝑣 − are fresh):
                            𝐹 FOL ∧ 𝑣 −  𝑣 ↔ ∀𝑣 𝑣  𝑣 − → 𝐹 FOL ∧ 𝑣 −  𝑣
                                                                              

              Using this fact, we can obtain an equivalent formula where we substitute the left
              hand-side by the right hand-side using first-order reasoning. This yields
                                ∀𝑣 𝑣  𝑣 − → 𝐹 FOL ∧ 𝑣 −  𝑣 → [𝑝] 𝐺 FOL
                                                             

              We then apply (MR) w.r.t. ∀𝑣 𝑣  𝑣 − → 𝐹 FOL ∧ S𝑝 𝑣 − , 𝑣 which yields two proof
                                                                              
              obligations. The first proof obligation reads:
               ∀𝑣 𝑣  𝑣 − → 𝐹 FOL ∧ 𝑣 −  𝑣 → [𝑝] ∀𝑣 𝑣  𝑣 − → 𝐹 FOL ∧ S𝑝 𝑣 − , 𝑣
                                                                                      

              Using ([] ∧) we decompose this formula into a proof that ∀𝑣 𝑣  𝑣 − → 𝐹 FOL is pre-
                                                                                                
              served (this immediately follows from (V)) and a proof that S𝑝 𝑣 − , 𝑣 holds after ex-
              ecution of 𝑝. To this end, we weaken the right side yielding the formula 𝑣 −  𝑣 →
              [𝑝] S𝑝 𝑣 − , 𝑣 . Note, that this formula is in Λ (𝑖 ) and is furthermore valid, as S𝑝 pre-
                            
              cisely describes the variable values of all reachable states. Thus, we can discharge this
              proof obligation to ⊢Δ (𝑖 ) which (by assumption) must relatively prove its validity w.r.t.
              first-order formulas.
              Secondly, we must prove that:
                                 ∀𝑣 𝑣  𝑣 − → 𝐹 FOL ∧ S𝑝 𝑣 − , 𝑣 → 𝐺 FOL
                                                                  

              First, note that this formula is a first-order formula over Λ (01) . Consider any state 𝜎 such
                                      −                   −
                                                              
              that 𝜎 |=Δ ∀𝑣 𝑣  𝑣 → 𝐹 FOL ∧ S𝑝 𝑣 , 𝑣 (otherwise the formula is trivially satisfied).
              Then, we construct 𝜇 ∈ S where V (01) (𝜇, 𝑣) = V (01) (𝜎, 𝑣 − ) for all 𝑣 ∈ Vars (𝑝) and
              𝜇 ≡Vars(𝑝 ) ∁ 𝜎. Then, by definition of S𝑝 it holds that (𝜇, 𝜎) ∈ P (01) (𝑝) and 𝜇 |=Δ 𝐹 FOL .
              Since we assumed the validity of the original formula, this implies that 𝜎 ⊨ 𝐺 FOL . Thus,
              the second proof obligation is valid and we therefore reduced the validity of the original
              formula to a first-order formulas.
                                                                                                                   □

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:45


Lemma C.20 (Diamond Properties for Simple Heterogeneous Theories with Havoc). Let Δ (0) , Δ (1)
be two relatively complete, FOL expressive dynamic theories with finite support that are communicating
in Δ (01) . Consider now the simple heterogeneous dynamic theory (i.e. Δ (01) ), then its proof calculus
⊢Δ (01) is relatively complete for formulas of the form 𝐹 FOL → ⟨𝑝⟩ 𝐺 FOL with 𝐹 FOL, 𝐺 FOL ∈ FOLΔ (01) , 𝑝 ∈
FOLΛ (01) .
      𝑃

   Proof. In contrast to similar proofs (e.g. Harel et al. [31] and Platzer [51]), the major challenge in
deriving relative completeness is the case where 𝑝 ∈ Λ𝑃(𝑖 ) but 𝐹 FOL, 𝐺 FOL ∈ FmlΛ (01) , i.e. the formulas
may contain predicates, functions and variables from both theories. We tackle this case, which is in
fact the only one for programs 𝑝 ∈ Λ𝑃(01) , as follows:
  𝑝 ∈ Λ𝑃(𝑖 ) We apply the (PB) rule with the two fresh formulas 𝐻 1 ≡ S𝑝 𝑣, 𝑣 + and 𝐻 2 ≡ 𝑣  𝑣 + .
                                                                                       
             This results in the formula
                    𝐹 FOL → ∀𝑣 + (𝐻 1 → ⟨𝑝⟩ 𝐻 2 ) ∧ ∃𝑣 + 𝐻 1 ∧ ∀𝑣 (𝐻 2 → 𝐺 FOL ) .
                                                                                    

            We can split this up into two separate proofs. The first proof obligation (after omitting
            𝐹 FOL ) reads ∀𝑣 + (𝐻 1 → ⟨𝑝⟩ 𝐻 2 ). Notably, this formula is entirely in Λ (𝑖 ) and can there-
            fore be discharged via the calculus ⊢Δ (𝑖 ) . Since we assumed the relative completeness
            of ⊢Δ (𝑖 ) this must succeed as 𝐻 1 is our program   rendition. The second proof obligation
            reads 𝐹 FOL → ∃𝑣 +  𝐻 1 ∧ ∀𝑣 (𝐻 2 → 𝐺 FOL ) . We assumed that 𝐹 FOL → ⟨𝑝⟩ 𝐺 FOL is valid
                                                          
            and 𝐻 1 ≡ S𝑝 𝑣, 𝑣 + exactly describes the possible state transitions starting from 𝑣 (in
            this instance in particular for a state satisfying 𝐹 FOL ). Thus, there must exists a 𝑣 + such
            that S𝑝 𝑣, 𝑣 + and that further for all 𝑣 with 𝑣  𝑣 + it holds that 𝐺 FOL is satisfied. This
            is exactly what the formula checks and the formula is thus valid. Since it is moreover
            by definition a first-order formula, we can prove it using our oracle. Thus, we can prove
            the validity of diamond formulas for 𝑝 ∈ Λ𝑃(𝑖 ) .
                                                                                                          □
Lemma C.21 (Relative Completeness: Simple Heterogeneous Dynamic Theories). Let Δ (0) , Δ (1) be
two relatively complete, FOL expressive dynamic theories with finite support that are communicating
in Δ (01) . Then the simple heterogeneous dynamic theory Δ (01) with its proof calculus ⊢Δ (01) is relatively
complete.
  Proof. This is a corollary from Theorem C.3: We know that Δ (01) is FOL expressive (Lemma C.18)
and that the diamond and box fragments are relatively complete (Lemmas C.19 and C.20). Conse-
quently ⊢Δ (01) for the full theory.                                                           □

C.3   Proof of Case Study Guarantee
Here we prove the example described in Section 9. We begin by giving a full account of the (in the
main text abbreviated) formula coupledPre:
            coupledPre ≡ ctrlPre ∧
                             A > 0 ∧ B > 0 ∧ T > 0 ∧ 𝑥 + 𝑣 2 /(2 ∗ 𝐵) ≤ 𝑠 ∧
                             equal (A− , 100A) ∧ equal (B− , −100B) ∧ equal (T− , 100 ∗ T)
                             round (p, 100 (x − s)) ∧ round (v, 100v)
We then apply (MR), introducing 𝜙 ≡ coupledPre which leaves us with the cases (A) and (B).
(A) Note that coupledPre is a large conjunction which in particular contains 𝑥 + 𝑣 2 /(2𝐵) ≤ 𝑠 We
can thus show that coupledPre → 𝑥 ≤ 𝑠.

                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:46                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


                                                  ˆ ∗ coupledPre. This allows us to apply
                                                    
(B) We now need to prove that coupledPre → (ctrl; 𝛼)
the (ind) rule leaving the proof obligation

                                     coupledPre → [ctrl; 𝛼]
                                                         ˆ coupledPre.

                                  ˆ
As a reminder we once again print 𝛼:

               (a := ∗; ? (equal (this.acc, 𝑎 ∗ 100)) ; env; p := ∗; v := ∗; ? (coupling))

We decompose ctrl; 𝛼ˆ via (;). Next we again apply (MR) w.r.t 𝜙 ≡ 𝐹 1 . (see below) which produces
(B.A) and (B.B).

                 𝐹 1 ≡ctrlPost∧
                                                                    
                        A > 0 ∧ B > 0 ∧ T > 0 ∧ 𝑥 + 𝑣 2 /(2 ∗ 𝐵) ≤ 𝑠 ∧
                        equal (A− , 100A) ∧ equal (B− , −100B) ∧ equal (T− , 100 ∗ T) ∧
                                                                
                       round (p, 100 (x − s)) ∧ round (v, 100v)

(B.A) We now need to prove that coupledPre → [ctrl] 𝐹 1 . We split this into two separate proof
obligations via application of ([] ∧): The preservation of the equal/round atoms (last part) can be
shown via (V) as these variables are not part of BVΔ (ctrl)
                                                          of JavaDL and follow from coupledPre.
The preservation of A > 0 ∧ . . . ∧ 𝑥 + 𝑣 2 /(2 ∗ 𝐵) ≤ 𝑠 can be skipped via (𝐹 (𝑖 ) ) (for 𝑖 = 𝑑L) as
this is already part of coupledPre and soley concerns 𝑑L variables. Finally, it remains to show that
coupledPre → [ctrl] ctrlPost. Via (HR0) we reduce this to JavaDL. In fact, we have already
proven this property in Lemma 9.1.
(B.B) This proof branch now reads:

    𝐹 1 → [a := ∗; ? (equal (this.acc, a ∗ 100)) ; env; p := ∗; v := ∗; ? (coupling)] coupledPre

We decompose further via (;) (:=∗) (;) (?). After further simplification, the formula then reads:

           ctrlPost∧
         ­ equal (A− , 100A) ∧
         ©                                      ª
                                                ®
         ­ equal (B− , −100B) ∧
         ­                                      ®
                                                ®
         ­ equal (T− , 100T) ∧
         ­                                      ®
                                                ®
         ­ round (p, 100 (x − s)) ∧             ® → [env; p := ∗; v := ∗; ? (coupling)] coupledPre
         ­                                      ®
         ­ round (v, 100v) ∧
         ­                                      ®
                                                ®
         ­ equal (this.acc, a ∗ 100) ∧
         ­                                      ®
                                                ®
         ­ A > 0 ∧ −B > 0 ∧
         ­                                      ®
                                                ®
         « 𝑇 > 0 ∧ 𝑥 + 𝑣 /(2𝐵) ≤ 𝑠
                           2
                                                ¬
Note, that in comparison to envPre we lack the formula acc_assumptions. To remedy this, we perform
a cut w.r.t. acc_assumptions. We can prove this formula because it follows from the equation on
the left hand-side (in particular via ctrlPost). We perform this proof via mechanized first-order
reasoning in KeYmaera X. After simplification and application of (;) this yields the following proof
situation:
              ctrlPost ∧ envPre
            ­ equal (A− , 100A) ∧
            ©                              ª
                                           ® → [env] [p := ∗; v := ∗; ? (coupling)] coupledPre
                                           ®
            ­ equal (B− , −100B) ∧
            ­
                                           ®
                      −
            « equal (T , 100T)             ¬

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:47


Once again we apply (MR) this time w.r.t. 𝜙 ≡ 𝐹 2 as follows:
                𝐹 2 ≡envPost ∧ ctrlPost ∧
                      (equal (A− , 100A) ∧ equal (B− , −100B) ∧ equal (T− , 100T)) ∧
                      (A > 0 ∧ B > 0 ∧ T > 0)
This leaves proof obligations (B.B.A) and (B.B.B).
(B.B.A) We now need to prove that the following formula is valid:
                                   ctrlPost ∧ envPre
                                 ­ equal (A− , 100A) ∧
                                 ©                         ª
                                                           ® → [env] 𝐹 2
                                                           ®
                                 ­ equal (B− , −100B) ∧
                                 ­
                                                           ®
                                           −
                                 « equal (T , 100T)        ¬
To this end, we apply ([] ∧) to factor out the equalities and inequalities of the second and third line of
𝐹 2 , which can be shown via (V) as the contained variables are not part of BVΔ (env). For the remaining
formula, we apply (𝐹 (𝑖 ) ) (for i=JavaDL), which shows the preservation of ctrlPost, meaning it only
remains to show envPost. After weakening the precondition, we thus get envPre → [env] envPost.
Fortunately, we have previously shown this with KeYmaera X in Lemma 9.2. Hence, we can reuse
this result via (HR1)
(B.B.B) It remains to show that the following formula is valid:
                            𝐹 2 → [p := ∗; v := ∗; ? (coupling)] coupledPre
After further reduction via (;) (:=∗) (;) (:=∗) (;) (?) and further simplification this yields:
                   heap_assumptions ∧
                                                ctrlPre ∧
                 ­ A  A ∧ B−  B ∧
                 © −                        ª
                                              ­ A>0 ∧ B>0 ∧ T>0∧
                                            ® ©                                                 ª
                 ­ T  T ∧ envPost ∧
                 ­ −                        ®                                                   ®
                                              ­ 𝑥 + 𝑣 2 /(2 ∗ 𝐵) ≤ 𝑠 ∧
                                            ® ­                                                 ®
                 ­ equal (A− , 100A) ∧
                 ­                          ®                                                   ®
                                              ­ equal (A− , 100A) ∧
                                            ® ­                                                 ®
                 ­ equal (B− , −100B) ∧     ®→­
                 ­                          ®                                                   ®
                                              ­ equal (B− , −100B) ∧
                                                                                                ®
                 ­ equal (T− , 100T)
                 ­                          ®                                                   ®
                                              ­ equal (T− , 100T)
                                            ® ­                                                 ®
                 ­ round (p, 100 (x − s)) ∧ ®
                 ­                          ®                                                   ®
                                              ­ round (p, 100 (x − s)) ∧
                                              ­                                                 ®
                 ­ round (v, 100v) ∧
                 ­                          ®                                                   ®
                                              « round (v, 100v) ∧
                                            ®
                 « A>0 ∧ B>0 ∧ 𝑇 >0 ¬
                                                                                                ¬
Almost all elements of the conjunction on the right (after expansion of ctrlPre and envPost) can be
shown via 𝜙 → 𝜙. The exception are the formulas A > 0, B < 0 and T > 0 which nonetheless easily
follow from A > 0, B > 0, T > 0 and the equal constraints. This concludes our proof that coupledPre
is inductive w.r.t. 𝛼ˆ and simulaneously concludes our proof on the validity of Equation (3).




                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:48                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


D     Isabelle Formalization: Overview
To obtain the same modularity of components presented in the paper in Isabelle, the formalization
is spread across several locales, which impose additional assumptions on the considered dynamic
theory in exchange for providing additional proof rules.

D.1      Basic Constructions
   FirstOrder. The underlying first-order structure is implemented in the locale folCore in the file
FirstOrder.thy. This locale demands the assumptions from Definitions 4.3 and 4.4 and constructs
first-order formulas over the provided atoms (given as type parameter ’atom).

   Dynamic Logic. Given an instantiation of the locale folCore (see above) and programs sat-
isfying the assumptions from Definition 4.5, we can instantiate the locale dynamic_theory in
DynamicLogicCore.thy, which implements the core results of a dynamic theory. Programs are
provided as the type parameter ’prog. This includes the data structures for formulas, their eval-
uation, all coincidence and bound effect lemmas, Hilbert calculus axioms (sanity check), and the
axioms (G) and (K). The file DynamicLogic.thy then proves the additional axioms (V) and (B).
When this paper states a particular structure is a dynamic theory (see Definition 4.7) this corresponds
to it being an instantiation of this locale (dynamic_theory).

D.2      Liftings
Liftings are implemented as locales whose only assumption is the instantiation of an existing locale
instantiation dynamic_theory. We have implemented Havoc lifting (see Section 6.1) and a lifting
to generate the closure over regular programs (see Section 6.2).

  Havoc. The havoc lifting is implemented in the locale havoc_lifting in HavocDynamicLogic.thy.
This locale takes a given instantiation of dynamic_theory. It then constructs an extended program-
ming language which includes the havoc operation, defines appropriate primitives for program
evaluation, and free variable computation. It then proves that the extended constructs are once
again an instantiation of dynamic_theory via Isabelle’s sublocale mechanism. Further, all axioms
presented in the paper are proven.

   Regular Programs. Similarly to the havoc lifting, the regular program closure lifting is imple-
mented as a locale regular_lifting in the file KATDynamicLogic.thy. In the same approach as
above, this locale takes as only assumptions the instantiation of the locale dynamic_theory and
proves that the regular closure over programs (with an appropriately defined program evaluation)
is once again an instantiation of the locale dynamic_theory via Isabelle’s sublocale mechanism.
Further, all axioms presented in the paper are proven.

D.3      Combination
As outlined in Section 7, the construction of a heterogeneous dynamic theory has three requirements:
Two existing dynamic theories and a set of new first-order atoms evaluating over the composed
state (i.e., S (0) × S (1) ). In Isabelle, this is implemented as the locale HeterogeneousDynLog inside
HeterogeneousDynamicLogic.thy: This locale takes as input two instantiations of dynamic_theory
and one instantiation of folCore whose state space is fixed to the combined state space of the indi-
vidual theories. The locale constructs the simple heterogeneous dynamic theory as described in Sec-
tion 7.1 and proves that it is once again an instantiation of dynamic_theory. Using havoc_lifting
and regular_lifting, this heterogeneous instantiation is then lifted to the fully heterogeneous
dynamic theory. Additionally, we prove the reduction rules (HR0), (HR1).

Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:49


D.4   Inductive Expressiveness
To additionally derive axiom (C), we require inductive expressiveness. This is formalized in the
locale nat_regular_lifting, which, in addition to an instantiation of regular_lifting (re-
quired for the availability of loops) makes the assumptions formalized in Definition 6.4. It then
proves the soundness of axiom (C) for an arbitrary given regular program lifted dynamic theory. In
HeterogeneousDynLog we also prove that if a given homogeneous dynamic theory Δ (𝑖 ) is induc-
tively expressive (i.e. instantiates nat_regular_lifting), then the fully heterogeneous dynamic
theory is also inductively expressive w.r.t Λ𝑉(𝑖N) (i.e. instantiates nat_regular_lifting).

D.5   Equational reasoning
We introduce the fundamental notions of program equivalence and refinement in the theory
DLRewriting which extends dynamic_theory. For dynamic logics with regular program closure
the theory KATRewriting introduces the locale KleeneDynLog which proves the Kleene Algebra
with Tests axioms and auxilliary lemmas. HeterogeneousRewriting formalizes the KAT rewriting
results for heterogeneous theory combination.
   Note on assumptions of KATRewriting. For clarity this paper introduces dynamic logics as requir-
ing the extensionality axiom required by KATRewriting. In reality, dynamic_theory itself requires a
slightly weaker notion of extensionality which we prove to be weaker in ExtensionalDynamicLogic.
Hence, all results of this paper are in particular derivable for the definition of dynamic theory
presented here while also holding for a slightly weaker notion of extensionality formalized in
dynamic_theory.

D.6   Instantiations
So far we have proven the following instantiations of provided locales:
    • Our formalization of Propositional Dynamic Logic is an instantiation of dynamic_theory
      (this instantiation implemented its own regular programs)
    • Our formalization of semi-ring first-order logic and DL (solely with assignment) instantiates:
      – folCore
      – dynamic_theory
      – havoc_lifting
      – regular_lifting
      – nat_regular_lifting for nat or int
    • The AFP’s formalization of differential dynamic logic [12] instantiates dynamic_theory
    • Two instantiations of semi-ring DL and a semi-ring first-order logic over corresponding state
      tuples instantiates HeterogeneousDynLog (sanity check for assumptions of HDL).

D.7   Artifact
We provide Isabelle outlines for our main project as well as our instantiation with Differential
Dynamic Logic, along with the Isabelle files in the supplementary materials.




                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:50                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


D.8 Reference to Isabelle Proofs
 Result      Isabelle Reference                                               File
             dynamic_theory.dyn_FV_fml_sound,
 Lemma C.1                                                                    DynamicLogicCore.thy
             dynamic_theory.dyn_FV_prog_sound
 Lemma 4.1   pdlDLFull                                                        PDL.thy
 Lemma 4.2   semiring_dl_full                                                 SemiRingDL.thy
 Lemma 4.3   dl_dyn_core                                                      DifferentialDL.thy
             dyn_fv_sem_coincidence,
 Lemma 5.1                                                                    DynamicLogicCore.thy
             dyn_fv_sem_coincidence_smallest
             dyn_prog_fv_sem_coincidence,
 Lemma 5.2                                                                    DynamicLogicCore.thy
             dyn_prog_fv_sem_coincidence_smallest
             dyn_prog_bv_sem_bounded,
 Lemma 5.3   dyn_prog_bv_sem_bounded_smallest1,                               DynamicLogicCore.thy
             dyn_prog_bv_sem_bounded_smallest2
 Lemma C.2   dynamic_theory.dyn_FV_fml_sound                                  DynamicLogicCore.thy
             dynamic_theory.dyn_axiom_G,                                      DynamicLogicCore.thy
             dynamic_theory.dyn_axiom_K,
 Theorem 5.1 dynamic_theory.dyn_axiom_V,                                      DynamicLogic.thy
             dynamic_theory.dyn_axiom_B
             dynamic_theory.rewriteAxiomReplace                               DLRewriting.thy
 Theorem 6.1 havoc_lifting.havoc_dl                                           HavocDynamicLogic.thy
 Lemma 6.1   havoc_lifting.dyn_axiom_HR                                       HavocDynamicLogic.thy
 Lemma 6.2   havoc_lifting.dyn_axiom_havoc                                    HavocDynamicLogic.thy
 Theorem 6.2 regular_lifting.kat_dl                                           KATDynamicLogic.thy
 Lemma 6.3   regular_lifting.dyn_axiom_RR                                     KATDynamicLogic.thy
             regular_lifting.dyn_axiom_test,
             regular_lifting.dyn_axiom_seq,
 Theorem 6.3 regular_lifting.dyn_axiom_star,                                  KATDynamicLogic.thy
             regular_lifting.dyn_axiom_choice,
             regular_lifting.dyn_axiom_I
             KleeneDynLog.kat_rule_*
 Theorem C.1                                                                  KATRewriting.thy
             KleeneDynLog.bool_rule*_general
 Lemma C.3   KleeneDynLog.eq_if_pure                                          KATRewriting
 Lemma 6.4   nat_regular_lifting.dyn_axiom_C                                  NatKATDynamicLogic.thy
             semiring_dl_full_nat,
 Lemma 6.5                                                                    SemiRingDL.thy
             semiring_dl_full_nat_int




Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
Heterogeneous Dynamic Logic: Provability Modulo Program Theories                                              217:51


    Result           Isabelle Reference                                         File
    Theorem 7.1      HeterogeneousDynLog.het_dl                                 HeterogeneousDynamicLogic.thy
                     HeterogeneousDynamicLogic.het_dl_havoc
    Theorem 7.2                                                                 HeterogeneousDynamicLogic.thy
                     HeterogeneousDynamicLogic.het_dl_kat
                     HeterogeneousDynLog.dyn_axiom_R0,
    Lemma 7.1                                                                   HeterogeneousDynamicLogic.thy
                     HeterogeneousDynLog.dyn_axiom_R1
                     inductively_expressive_1
    Lemma 7.2                                                                   HeterogeneousDynamicLogic.thy
                     inductively_expressive_2
                     HeterogeneousRewriting.choice_rewrite
                     HeterogeneousRewriting.seq_rewrite
    Theorem C.2                                                                 HeterogeneousRewriting.thy
                     HeterogeneousRewriting.check_rewrite
                     HeterogeneousRewriting.loop_rewrite
    Lemma C.6        HavocDynamicLogic.BV_overapprox                            HavocDynamicLogic.thy
    Lemma C.7        KATDynamicLogic.BV_overapprox                              KATDynamicLogic.thy
    Lemma C.8        HeterogeneousDynLog.BV_overapprox                          HeterogeneousDynamicLogic.thy




                               Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
217:52                                            Samuel Teuber, Mattias Ulbrich, André Platzer, and Bernhard Beckert


D.9 Reference to Isabelle Definitions
 Result          Isabelle Reference                                              File
                 types of folCore                                                FirstOrder.thy
 Definition 4.1
                 types of dynamic_theory                                         DynamicLogicCore.thy
                 fol_formula                                                     FirstOrder.thy
 Definition 4.2
                 dyn_formula                                                     DynamicLogicCore.thy
 Definition 4.3  folCore                                                         FirstOrder.thy
 Definition 4.4  folCore                                                         FirstOrder.thy
 Definition 4.5  dynamic_theory                                                  DynamicLogicCore.thy
 Definition 4.6  dynamic_theory                                                  DynamicLogicCore.thy
 Definition 4.7  dynamic_theory                                                  DynamicLogicCore.thy
                 folCore.fol_eval                                                FirstOrder.thy
 Definition 4.8
                 dynamic_theory.dyn_eval                                         DynamicLogicCore.thy
                 folCore.fol_fv_sem                                              FirstOrder.thy
                 dynamic_theory.dyn_fv_sem                                       DynamicLogicCore.thy
 Definition 4.9
                 dynamic_theory.dyn_prog_fv_sem                                  DynamicLogicCore.thy
                 dynamic_theory.dyn_prog_bv_sem                                  DynamicLogicCore.thy
                 dynamic_theory.progRefine
 Definition 4.11                                                                 DLRewriting.thy
                 dynamic_theory.progEquiv
                 havoc_prog
 Definition 6.1  havoc_lifting.full_prog_eval                                    HavocDynamicLogic.thy
                 havoc_lifting.full_prog_FV
                 kat_prog
 Definition 6.2  regular_lifting.full_prog_eval_int                              KATDynamicLogic.thy
                 regular_lifting.full_prog_eval
 Definition C.1 folCore.fol_fv_syn                                               FirstOrder.thy
 Definition C.2 regular_lifting.full_prog_fv_syn                                 KATDynamicLogic.thy
 Definition 6.3  regular_lifting                                                 KATDynamicLogic.thy
 Definition 6.4  nat_regular_lifting                                             NatKATDynamicLogic.thy
                 see HeterogeneousDynLog
 Definition 7.1                                                                  HeterogeneousDynamicLogic.thy
                 (’state1 × ’state2)
                 HeterogeneousDynLog.atom_eval_comm
 Definition 7.2                                                                  HeterogeneousDynamicLogic.thy
                 HeterogeneousDynLog.atom_fv_syn_comm
 Definition 7.3  HeterogeneousDynLog                                             HeterogeneousDynamicLogic.thy
                 HeterogeneousDynLog.het_atom_eval
 Definition 7.4                                                                  HeterogeneousDynamicLogic.thy
                 HeterogeneousDynLog.het_prog_eval
                 HeterogeneousDynLog.het_atom_fv_syn
 Definition C.4                                                                  HeterogeneousDynamicLogic.thy
                 HeterogeneousDynLog.het_dyn_prog_FV
 Definition 7.5  HeterogeneousDynLog.het_dl_kat                                  HeterogeneousDynamicLogic.thy

Received 2025-11-13; accepted 2026-04-03




Proc. ACM Program. Lang., Vol. 10, No. PLDI, Article 217. Publication date: June 2026.
