                                         Lean on Vampire Proofs (Short Paper)
                                         Jonas Bodingbauer #
                                         TU Wien, Austria
                                         Márton Hajdu #
                                         TU Wien, Austria
                                         Laura Kovács #
                                         TU Wien, Austria
                                         Axel Polaczek #
                                         TU Wien, Austria
                                         Michael Rawson #
                                         University of Southampton, UK
arXiv:2603.26342v1 [cs.LO] 27 Mar 2026




                                               Abstract
                                         VAMPIRE proves theorems completely automatically in first- and higher-order logic extended with theories.
                                         Proof checking is increasingly demanded to consolidate user trust in VAMPIRE’s output. We describe ongoing
                                         efforts in reconstructing VAMPIRE proofs as trusted proofs in L EAN.

                                         2012 ACM Subject Classification Theory of computation → Automated reasoning

                                         Keywords and phrases Interactive Theorem Provers, Automated Theorem Provers, Lean, Vampire, Proof
                                         Reconstruction

                                         Acknowledgements We thank Henrik Böving for providing helpful insights on L EAN. This research was
                                         funded in whole or in part by the ERC Consolidator Grant ARTIST 101002685, the ERC Proof of Concept
                                         Grant LEARN 101213411, and by SBA Research (SBA-K1 NGC), a COMET Center within the COMET –
                                         Competence Centers for Excellent Technologies Programme, and funded by BMIMI, BMWET, and the federal
                                         state of Vienna. The COMET Programme is managed by FFG .


                                          1     Introduction
                                         Computer-assisted proofs are indispensable in applications of mathematics [24, 35, 9], cybersecur-
                                         ity [32, 17, 22], software analysis [7, 1, 16], neural networks [5, 14], and many other areas. Automated
                                         reasoners, such as automated theorem provers (ATPs) and satisfiability modulo theory (SMT) solvers,
                                         provide push-button solutions to machine-based proof generation. Proofs returned by automated
                                         reasoners are can be checked by e.g. using an external ATP/SMT solver to reprove each step of
                                         the generated proof [30, 21, 2]. Alternatively, one can rely on interactive theorem proving (ITP) to
                                         replay the proof inference-by-inference [25, 26]. Unfortunately, proof-checking efforts struggle to
                                         accommodate advanced reasoning features: for example, quantifier elimination cannot be checked by
                                         SMT solvers, inductive proofs are often not supported by existing proof standards, and equational
                                         reasoning modulo associativity and commutativity (AC) is very difficult to recover in ITPs. There is a
                                         constant tension between advances in ATP [4, 37, 28, 33, 15, 19] and proof checking.
                                         Our contributions. This paper addresses proof checking for the VAMPIRE theorem prover [6], making
                                         proof checking feasible and adjustable. We enhance VAMPIRE with trusted proofs: proofs generated
                                         by VAMPIRE are reconstructed in, and checked by, the L EAN interactive theorem prover [12]. We
                                         describe our ongoing efforts in extending VAMPIRE with L EAN-based proof formats (Section 3),
                                         allowing us to use L EAN for increasing user trust in VAMPIRE proofs. Our experiments showcase
                                         scalability of using L EAN for trusting VAMPIRE (Section 4).
                                         Related methods have emerged from both ATP and ITP communities. We complement the interfacing
                                         efforts of Lean-auto [29] by providing tactics for validating VAMPIRE proofs in L EAN. Compared
                                         to [30], trust in VAMPIRE proofs is handed off to L EAN, rather than an SMT solver, significantly
2   Lean on Vampire Proofs (Short Paper)



    1. mul(x, mul(y, z)) =             Input             19. id = mul(x, mul(y, mul(x, y))) Sup 4,1
                 mul(mul(x, y), z)                       22. mul(x, mul(x, y)) = y           FwDem 15,2
    2. mul(id, x) = x                  Input             25. mul(x, id) = x                  Sup 22,4
    4. id = mul(x, x)                  Input             80. mul(y, mul(x, y)) = mul(x, id) Sup 22,19
    6. ¬∀x, y : mul(x, y) = mul(y, x) Neg. Goal          85. mul(y, mul(x, y)) = x           FwDem 80,25
    7. ∃x, y : mul(x, y) ̸= mul(y, x) ENNF 6             160. mul(x, y) = mul(y, x)          Sup 22,85
    8. mul(σ0 , σ1 ) ̸= mul(σ1 , σ0 )  Skolem 7          249. mul(σ0 , σ1 ) ̸= mul(σ0 , σ1 ) Sup 8,160
    15. mul(x, mul(x, y)) = mul(id, y) Sup 1,4           250. false                          Resolve 249
        Figure 1 Simplified VAMPIRE proof showing that if every element of a group has order two, the group
    is commutative. Here, mul denotes the group operator and id the group’s identity element. The variables x, y
    are implicitly universally quantified, whereas σ0 and σ1 are Skolem constants. The proof steps Sup, FwDem
    respectively denote superposition and its variant forward demodulation.


    reducing the trusted computing base. Work with SMT solvers [26] is similar, but here we consider
    superposition-based theorem proving. This is the first step towards a long-term vision turning
    VAMPIRE into a hammer for L EAN, complementing existing efforts in ATP/ITP integration [38, 18]
    and continuing a long tradition of VAMPIRE service in hammer systems [13].



     2     Illustrative Example and Scope

    Saturation and VAMPIRE. Proof automation with VAMPIRE is performed via saturation [20]: given
    a conjecture F in (extensions of) first-order logic, VAMPIRE negates and clausifies ¬F and tries to
    derive falsum from the resulting clause set by saturating the set with respect to the the superposition
    calculus [3, 27]. During proof search, clauses may be removed if they are determined to be redundant.
    Whenever the empty clause false is derived as a consequence of ¬F , (classical) validity of F is
    established and a proof is generated as part of the VAMPIRE output. Figure 1 shows a sample proof in
    which VAMPIRE applies specializations of superposition inferences, such as forward demodulation.

    Checking VAMPIRE proofs for soundness. To improve efficiency of proof search VAMPIRE
    implements dedicated inference rules for equality reasoning, redundancy checking, arithmetic, and
    induction [6], among others. These advances increase the number of inference rules in VAMPIRE to
    around 200. Our work identifies a core set of inference rules (Section 3) from which trusted proofs of
    VAMPIRE are generated. Trust in VAMPIRE proofs is achieved by the help of L EAN: (i) we extend
    VAMPIRE to output proofs as L EAN theorems proven using lemmas corresponding to inferences.
    Once VAMPIRE finds a proof, a L EAN input file is generated where tactics are used to (ii) reconstruct
    VAMPIRE inferences in L EAN, demonstrating soundness for each step. A final combination of these
    steps results in a full VAMPIRE proof from assumptions to conclusions trusted by L EAN. For example,
    each VAMPIRE rule from Figure 1 is converted to a L EAN theorem and proven by a collection of
    dedicated tactics, such as the superposition tactic in Listing 3.



     3     L EAN Trust on VAMPIRE Proofs

    We produce L EAN-checkable proofs for problems solved by VAMPIRE (Section 3.1). We report on
    our efforts in reconstructing the preprocessing steps (Section 3.2) and the most important inference
    rules (Section 3.3) of VAMPIRE in L EAN. While this paper focuses on standard first-order logic with
    equality, extending our work to multi-sorted first-order logic is an immediate step for future work.
Bodingbauer, Hajdu, Kovács, Polaczek, and Rawson                                                                   3


3.1      Implementation
Our approach for generating trusted VAMPIRE proofs is implemented1 as a shared effort between
VAMPIRE and L EAN: once a VAMPIRE proof is generated, we output a L EAN file in which we
construct proof terms in L EAN using tactics provided by L EAN and mathlib[23]. Generating proof
terms can be assisted by additional information gained through proof replay in VAMPIRE, for
example in the case of unification or matching. For the frequently used inference rules in saturation
(Section 3.3), clauses are instantiated via the most general unifiers (mgu) computed by VAMPIRE and
passed to the grind tactic in L EAN.
General structure of trusted VAMPIRE proofs. A L EAN file representing a trusted VAMPIRE proof
is structured in three parts. After the preamble that declares all required symbols, the second (typically
largest) section includes all individual inference steps as theorems. Each theorem is proven using a
collection of L EAN tactics, or in very simple cases directly by providing suitable proof terms. Tactics
are often needed, because VAMPIRE inferences do not keep the ordering of clauses and hence require
suitable AC rule applications. The third part is a proof of the input conjecture, which shows that the
set of axioms imply the conclusion. This is done by using the previously proven lemmas to reconstruct
the proof found by VAMPIRE and also includes symbol introduction, such as Skolemization and
Tseitin transformation, which are part of VAMPIRE’s preprocessing (see Figure 1). Formulas are
encoded in a natural way in L EAN: the primitives of first-order formulas are used as defined by L EAN
core and mathlib [23]. Since VAMPIRE treats all domains as inhabited, this must be taken into account
in L EAN, which allows empty sorts.
    -- inference steps above
    theorem fullProof :
    (∀ v0 v1 v2 : ι, ((mul (mul v0 v1) v2)=(mul v0 (mul v1 v2)))) →
    (∀ v0 : ι, ((mul id v0)=v0)) → (∀ v0 : ι, (id=(mul v0 v0))) →
    (∀ v0 v1 : ι, ((mul v0 v1)=(mul v1 v0))) := by
      intros step1 step2 step3
      apply Classical.byContradiction; intro step5
      ...
      have step160 := inf_s160 step22 step85
      have step249 := inf_s249 step8 step160

     Listing 1 Third part of a L EAN input file, representing a trusted VAMPIRE proof corresponding to Figure 1.
It is combining the previously proven lemmas corresponding to inference steps for the full proof of Figure 1.



3.2      Preprocessing
Several preprocessing steps are used in VAMPIRE. To transform a first-order formula F (i.e. con-
jecture) into clausal normal form (CNF), the formula F is (typically) rectified, simplified, flattened,
transformed to equivalence negation normal form (ENNF),2 named, converted to NNF, Skolemized,
and finally transformed to conjunctive normal form [31]. For ENNF transformation as well as flatten-
ing and simplification, we use the L EAN simp tactic, with suitable theorems.3 For the transformation
from ENNF to CNF, our implementation currently uses either duper [11] or grind.
Skolemization. After the input conjecture F has been transformed to NNF, the existential quantifiers
are replaced with Skolem functions of suitable arity. The default implementation of VAMPIRE replaces
existentially-quantified variables by functions that are dependent on free variables of the immediate


1
  Our implementation is open-source and available on GitHub: https://github.com/vprover/vampire/tree/leancheck,
  Lean library https://github.com/vprover/vamplean
2
  Equivalence NNF allows ↔ and ⊕, with negations in front of atoms.
3
  In (E)NNF transformation, VAMPIRE by default uses non-confluent rewrite rules, however its outermost reduction
  strategy can be replicated using the ↓ annotation.
4   Lean on Vampire Proofs (Short Paper)


    subformulas. Automating this behavior in proof reconstruction is challenging; we therefore implemen-
    ted an option to change VAMPIRE Skolemization to use all currently bound variables (which is always
    a superset of the previously bound variables). For showing correctness of the employed Skolemization
    mechanism, we prenex the existential quantifiers using the theorem Classical.skolem of type:


                     (∀(x : α), ∃(y : b x), p x y) ↔ ∃(f : (x : α → b x), ∀(x : α), p x (f x)).

    Additional theorems that allow prenexing an existential from both ∨ and ∧ are also used. For the
    formula in existential prenex form, each of the quantifiers can then be assigned a new function name.
    Special care needs to be taken to match the ordering of Skolem functions assigned to variables as
    well as the orientation of equalities which is handled by custom tactics. The Skolemization step 8 of
    the running example shown in Figure 1 is given in Listing 2.

         -- step8 skolemisation
         exists_prenex at step7
         let ⟨sK0,sK1,step8’⟩ := step7
         have step8 : (¬((mult sK0 sK1)=(mult sK1 sK0))) := by symm_match using step8’

        Listing 2 Skolemization of the two existentially quantified variables in step 8. This snippet is from the third
    part of a trusted proof and assembles all inferences. symm_match and exists_prenex are custom tactics
    which take care of the orientation of equalities and prenexing.


    Predicate and function definitions. VAMPIRE may introduce predicates naming subformulas. These
    are declared globally as implicit variables, later defined in the final part of the L EAN input. Addition-
    ally, a suitable equivalence theorem is added and used by later inference steps from VAMPIRE.



    3.3       Inference Rules within Saturation

    Saturation-based proof search in VAMPIRE implements the superposition calculus and uses the
    following core rules: resolution, factoring, paramodulation, equality resolution, and equality factoring.
    Many rules applied in VAMPIRE, such as superposition and (forward) demodulation, can be described
    as a restricted instance of paramodulation.
        Listing 3 demonstrates superposition used by VAMPIRE at step 160 of Figure 1. It is translated as
    a L EAN theorem that takes two premises and gives a conclusion. At the beginning of the theorem, all
    premises are introduced as well as the variables of the conclusion. The most general unifier (mgu)
    found by VAMPIRE is instantiated via the have statements. After that, the grind tactic is called,
    which is well-suited for ground reasoning and can effectively reconstruct proof terms.4
        Other inference rules of VAMPIRE follow the same steps: introduce premises and conclusion
    variables, instantiate them according to the unifier found by VAMPIRE, and then dispatch it to grind.
    When it occurs that two variables are unified, the unifier can contain a variable that is not present
    in the conclusion [30]. In this case, the default element of the inhabited sort is used. In the future,
    more specialized, custom, tactics could be employed that can use additional information provided by
    VAMPIRE such as the positions where rewrites occurred.5



    4
        This approach is inspired by [30], where ground instances are passed to an SMT solver.
    5
        VAMPIRE does not preserve literal ordering, therefore a tactic that takes into account AC of ∨ is required.
Bodingbauer, Hajdu, Kovács, Polaczek, and Rawson                                                                   5


                                                                    General paramodulation rule
theorem inf_s160 :                                               l =r∨C         L[k] ∨ D
 (∀ x0 y0 : ι, ((mul y0 (mul x0 y0 ))=x0 )) →                                             σ = mgu(l, k)
 (∀ x1 y1 : ι, ((mul x1 (mul x1 y1 ))=y1 )) →                       (L[r] ∨ C ∨ D)σ
 (∀ x y : ι, ((mul x y)=(mul y x))) := by                       instantiated with
 intros h0 h1 x y
 have i0 := h0 x y                                                l     mul(y0 , mul(x0 , y0 ))
 have i1 := h1 y (mul x y)                                        r     x0
 grind only [cases Or]                                           L[k]   mul(x1 , mul(x1 , y1 )) = y1
                                                                  σ     {x0 7→ x, y0 7→ y,
                                                                         x1 7→ y, y1 7→ mul(x, y)}
                            (a)                                                        (b)

   Listing 3 (a) L EAN theorem representing the superposition step 160 of Figure 1. (b) The instantiation of
paramodulation (i.e. more general superposition) for (a). Clauses C, D are empty for the instance of Figure 1.




3.4     AVATAR

A feature that contributes to VAMPIRE’s success is AVATAR [36], which enables efficient reasoning
over the propositional/quantifier-free structure of clauses. Simply put, AVATAR splits clauses into
variable-disjoint sub-clauses and defines propositional labels for each of the sub-clauses, as follows.

                                     ¬Q(z) ∨ P (x, f (z)) ∨ R(y)               sp1 ≡ ¬Q(z) ∨ P (x, f (z))
AVATAR splitting of a clause:                                    using
                                             sp1 ∨ sp2                         sp2 ≡ R(y)
A SAT solver in AVATAR is used to reason about the propositional structure sp1 ∨sp2 , while VAMPIRE
handles AVATAR components of the form R(x) ← sp2 , which should be understood as “R(x) if sp2 ”.
If the SAT solver finds that the propositional structure is unsatisfiable, a refutation is produced. When
the SAT solver finds a model, VAMPIRE continues reasoning using the learned knowledge from the
propositional model and derives new contradictions using first-order reasoning, that can in turn be
used to define new propositional clauses to be passed to the SAT solver. When a VAMPIRE proof is
found with AVATAR, the final contradiction (false) is derived by the SAT solver.

AVATAR in L EAN. To reconstruct and check AVATAR steps in L EAN, the propositional names are
declared and defined in the first and last parts of VAMPIRE proofs (Section 3.1). When a proof step
involves an AVATAR component, the propositional labels of the conclusions are introduced before
introducing the propositional variables (e.g. sp1 ); these labels are used to instantiate premises, as
shown in Listing 4. The other rules are treated as normal inference rules, where the splitting clauses
is treated using rewrites as well as grind, which only needs to handle AC reordering as well as
removing potentially duplicate literals. The final SAT refutation is handled using the bv_decide
tactic, which calls a SAT solver and then verifies the received proof within L EAN [10].

theorem inf_s160_avatar : (sP1→(∀ x0 y0 : ι, ((mul y0 (mul x0 y0 ))=x0 ))) →
 (∀ x1 y1 : ι, ((mul x1 (mul x1 y1 ))=y1 )) →
 (sP1→(∀ x y : ι, ((mul x y)=(mul y x)))) := by
 intros h0 h1 sp1 x y
 have i0 := h0 sp1 x y
 ...
theorem avatarRefutation’ (sP1’ sP2’ sP3’ : Bool) : (sP1’ || sP2’ || sP3’) →
     (!sP2’) → (!sP3’) → (!sP1’) → False := by bv_decide

   Listing 4 Variant of the inference rule of Listing 3 if it were part of an AVATAR proof. The final SAT proof,
which is reconstructed using bv_decide, is also listed.
6   Lean on Vampire Proofs (Short Paper)


     4                        Experiments
    Our experiments used benchmarks from version
    9.2.1 of the TPTP library [34]. We relied on         TPTP VAMPIRE
                                                                                        L EAN
    B ENCH E XEC [8] for conducting experiments,                             Success Timeout Error
                                                         CNF        3860       3785        53        22
    using an AMD Epyc 7502 2.5GHz processors             FOF        3897       3296        482       119
    and 1TB RAM. Each benchmark ran with a
    single core and 16GB of memory. Our bench-             Figure 2 Number of proofs found by baseline VAM -
                                                       PIRE (column 2) vs our L EAN proof reconstructions
    mark set consists of all CNF and FOF problems
                                                      (columns 3–5), sorted for success/failure reasons. Suc-
    from TPTP, overall 17,603 problem instances.
                                                       cess means trusted VAMPIRE proofs, validated by L EAN.
    Our VAMPIRE runs used VAMPIRE version 5.0.1
    with the Discount saturation loop and a 20-giga-
    instruction (roughly 5-10 seconds) resource limit (-sa discount -i 20000); we refer to this
    VAMPIRE version as baseline VAMPIRE. For L EAN, we used a 300-second timeout.
        We compare (i) baseline VAMPIRE without proof output (-proof off) and (ii) our work
    (Section 3.1) enhancing VAMPIRE (Git tag: Leancheck2026) with output of proofs checkable by
    L EAN. Figure 2 summarizes our results, showcasing 98% success rate of trusted proof generation on
    CNF problems and 85% of FOF examples. We note that CNF proof reconstruction reduces the load
    of reconstructing preprocessing steps. For problems whose VAMPIRE proofs cannot yet be checked
    by L EAN, the reasons stem from large L EAN files (column 4) or hard to reconstruct inferences and
    lacking support of some specific VAMPIRE inference, implementation bugs or running into L EAN
    tactic timeout (column 5).
        Figure 3(a) indicates that proof replay has a non-negligible influence on proofs that have been
    in generated in less time (shorter proving process). Rerunning few proof inferences for a shorter
    proof search is comparatively more costly when less inferences are made during proof search. Proof
    replay may take long time when there are lots of possible inferences from two premises. Figure 3(b)
    shows that there is only minimal correlation between VAMPIRE proof search and L EAN proof
    reconstruction and checking. Finally, Figure 3(c) hints that longer proofs yield longer processes
    for proof reconstruction and checking times in L EAN as one would expect. This is likely not only
    because the amount of theorem increase but also because longer proofs yield longer formulas to be
    checked via VAMPIRE-specific L EAN tactics that are not necessarily needed/optimized.

                                                (a)                      (b)                    (c)
                            100        with proof generation
                                       without proof generation
      Vampire runtime [s]




                             10



                              1



                             0.1



                            0.01
                                   0   2000      4000     6000    8000
                                         Proved instances


        Figure 3 (a) Comparing baseline VAMPIRE and our VAMPIRE version outputting a L EAN file; here, we
    include only CNF and FOF problems where baseline VAMPIRE found a proof by contradiction. This plot only
    accounts for the overhead in VAMPIRE, not for L EAN proof reconstruction and checking time. Notice the
    logarithmic y-axis. (b) A scatter plot comparing the L EAN proof reconstruction and checking runtime vs the
    VAMPIRE runtime. (c) A scatter plot of L EAN runtime vs number of theorems in a L EAN input file.
Bodingbauer, Hajdu, Kovács, Polaczek, and Rawson                                                                 7


 5     Conclusions and Future Work
We describe ongoing efforts on reconstructing VAMPIRE proofs in L EAN, allowing us to trust VAM -
PIRE proofs thanks to L EAN ’s kernel (alongside a trusted SAT proof-checker [10]). Our experiments
show scalability of generating trusted VAMPIRE proofs. We so far handle only a small fraction of the
inference steps implemented by VAMPIRE. To remedy this, the proof-producing Duper ATP [11] is
invoked if no specialized set of tactics is available. Further work plans addressing various efficiency
limits of proof reconstruction in L EAN. Notably, the current implementation of CNF transformation
requires parsing and analyzing the same (possibly large) formula multiple times. Saturation steps
would also benefit by further information available within VAMPIRE; these steps could be utilized
through specialized tactics in L EAN.


 6     Use of Generative AI Tools
Generative AI tools were not used in the writing of this paper. GitHub Copilot suggestions (that
mainly rely on GPT5- mini) in VS Code have been used in our implementation.


      References
 1    Wolfgang Ahrendt, Thomas Baar, Bernhard Beckert, Martin Giese, Elmar Habermalz, Reiner Hähnle,
      Wolfram Menzel, and Peter H. Schmitt. The KeY Approach: Integrating Object Oriented Design and
      Formal Verification. In JELIA, 2000. doi:10.1007/3-540-40006-0_3.
 2    Michael Armand, Germain Faure, Benjamin Grégoire, Chantal Keller, Laurent Théry, and Benjamin
      Werner. A Modular Integration of SAT/SMT Solvers to Coq through Proof Witnesses. In CPP, 2011.
      doi:10.1007/978-3-642-25379-9_12.
 3    Leo Bachmair and Harald Ganzinger. Resolution Theorem Proving. In Handbook of Automated Reasoning.
      North-Holland, 2001. doi:10.1016/B978-044450813-3/50004-7.
 4    Haniel Barbosa, Clark W. Barrett, Martin Brain, Gereon Kremer, Hanna Lachnitt, Makai Mann, Ab-
      dalrhman Mohamed, Mudathir Mohamed, Aina Niemetz, Andres Nötzli, Alex Ozdemir, Mathias Preiner,
      Andrew Reynolds, Ying Sheng, Cesare Tinelli, and Yoni Zohar. cvc5: A Versatile and Industrial-Strength
      SMT Solver. In TACAS, 2022. doi:10.1007/978-3-030-99524-9_24.
 5    Clark W. Barrett, Thomas A. Henzinger, and Sanjit A. Seshia. Certificates in AI: Learn but Verify.
      Communications of ACM, 2026. doi:10.1145/3737447.
 6    Filip Bártek, Ahmed Bhayat, Robin Coutelier, Márton Hajdú, Matthias Hetzenberger, Petra Hozzová,
      Laura Kovács, Jakob Rath, Michael Rawson, Giles Reger, Martin Suda, Johannes Schoisswohl, and
      Andrei Voronkov. The Vampire Diary. In CAV, 2025. doi:10.1007/978-3-031-98682-6_4.
 7    Raven Beutner and Bernd Finkbeiner. Checking Satisfiability of Hyperproperties Using First-Order Logic.
      In ATVA, 2024. doi:10.1007/978-3-031-78750-8_10.
 8    Dirk Beyer. Reliable and Reproducible Competition Results with BenchExec and Witnesses Report on
      SV-COMP 2016. In TACAS, 2016. doi:10.1007/978-3-662-49674-9_55.
 9    Matthew Bolan, Joachim Breitner, Jose Brox, Nicholas Carlini, Mario Carneiro, Floris van Doorn, Martin
      Dvorak, Andrés Goens, Aaron Hill, Harald Husum, Hernán Ibarra Mejia, Zoltan A. Kocsis, Bruno Le
      Floch, Amir Livne Bar-on, Lorenzo Luccioli, Douglas McNeil, Alex Meiburg, Pietro Monticone, Pace P.
      Nielsen, Emmanuel Osalotioman Osazuwa, Giovanni Paolini, Marco Petracci, Bernhard Reinke, David
      Renshaw, Marcus Rossel, Cody Roux, Jérémy Scanvic, Shreyas Srinivas, Anand Rao Tadipatri, Terence
      Tao, Vlad Tsyrklevich, Fernando Vaquerizo-Villar, Daniel Weber, and Fan Zheng. The Equational Theories
      Project: Advancing Collaborative Mathematical Research at Scale, 2025. arXiv:2512.07087.
10    Henrik Böving, Siddharth Bhat, Luisa Cicolini, Alex Keizer, Léon Frenot, Abdalrhman Mohamed, Léo
      Stefanesco, Harun Khan, Joshua Clune, Clark Barrett, and Tobias Grosser. Interactive Bitvector Reasoning
      using Verified Bit-Blasting. Proceedings of the ACM on Programming Languages (OOPSLA), 2025.
      doi:10.1145/3763167.
8   Lean on Vampire Proofs (Short Paper)


    11   Joshua Clune, Yicheng Qian, Alexander Bentkamp, and Jeremy Avigad. Duper: A Proof-Producing
         Superposition Theorem Prover for Dependent Type Theory. In ITP, 2024. doi:10.4230/LIPIcs.
         ITP.2024.10.
    12   Leonardo de Moura and Sebastian Ullrich. The Lean 4 Theorem Prover and Programming Language. In
         CADE, 2021. doi:10.1007/978-3-030-79876-5_37.
    13   Martin Desharnais, Petar Vukmirovic, Jasmin Blanchette, and Makarius Wenzel. Seventeen Provers Under
         the Hammer. In ITP, 2022. doi:10.4230/LIPIcs.ITP.2022.8.
    14   Remi Desmartin, Omri Isac, Grant O. Passmore, Ekaterina Komendantskaya, Kathrin Stark, and Guy
         Katz. A Certified Proof Checker for Deep Neural Network Verification in Imandra. In ITP, 2025.
         doi:10.4230/LIPICS.ITP.2025.1.
    15   André Duarte and Konstantin Korovin. Implementing Superposition in iProver (System Description). In
         IJCAR, 2020. doi:10.1007/978-3-030-51054-1_24.
    16   Pamina Georgiou, Bernhard Gleiss, Ahmed Bhayat, Michael Rawson, Laura Kovács, and Giles Reger.
         The Rapid Software Verification Framework. In FMCAD, 2022. doi:10.34727/2022/ISBN.
         978-3-85448-053-2_32.
    17   Simon Jeanteur, Laura Kovács, Matteo Maffei, and Michael Rawson. CryptoVampire: Automated
         Reasoning for the Complete Symbolic Attacker Cryptographic Model. In IEEE SP, 2024. doi:10.
         1109/SP54263.2024.00246.
    18   Anja Petkovic Komel, Michael Rawson, and Martin Suda. Case Study: Verified Vampire Proofs in the
         LambdaPi-calculus Modulo. CoRR, 2025. doi:10.48550/ARXIV.2503.15541.
    19   Laura Kovács, Petra Hozzová, Márton Hajdú, and Andrei Voronkov. Induction in Saturation. In IJCAR,
         2024. doi:10.1007/978-3-031-63498-7_2.
    20   Laura Kovács and Andrei Voronkov. First-Order Theorem Proving and Vampire. In CAV, 2013. doi:
         10.1007/978-3-642-39799-8_1.
    21   Hanna Lachnitt, Mathias Fleury, Leni Aniva, Andrew Reynolds, Haniel Barbosa, Andres Nötzli, Clark W.
         Barrett, and Cesare Tinelli. IsaRare: Automatic Verification of SMT Rewrites in Isabelle/HOL. In TACAS,
         2024. doi:10.1007/978-3-031-57246-3_17.
    22   Evan Laufer, Alex Ozdemir, and Dan Boneh. zkPi: Proving Lean Theorems in Zero-Knowledge. In CCS,
         2024. doi:10.1145/3658644.3670322.
    23   The mathlib Community. The lean mathematical library. In CPP, 2020. doi:10.1145/3372885.
         3373824.
    24   William McCune. Solution of the Robbins Problem. Journal of Automated Reasoning, 1997. doi:
         10.1023/A:1005843212881.
    25   Jia Meng and Lawrence C. Paulson. Translating Higher-Order Clauses to First-Order Clauses. Journal of
         Automated Reasoning, 2008. doi:10.1007/s10817-007-9085-y.
    26   Abdalrhman Mohamed, Tomaz Mascarenhas, Harun Khan, Haniel Barbosa, Andrew Reynolds, Yicheng
         Qian, Cesare Tinelli, and Clark W. Barrett. lean-smt: An SMT Tactic for Discharging Proof Goals in
         Lean. In CAV, 2025. doi:10.1007/978-3-031-98682-6_11.
    27   Robert Nieuwenhuis, Thomas Hillenbrand, Alexandre Riazanov, and Andrei Voronkov. On the Evaluation
         of Indexing Techniques for Theorem Proving. In IJCAR, 2001. doi:10.1007/3-540-45744-5_
         19.
    28   Grant Olney Passmore. Some Lessons Learned in the Industrialization of Formal Methods for Financial
         Algorithms. In FM, 2021. doi:10.1007/978-3-030-90870-6_39.
    29   Yicheng Qian, Joshua Clune, Clark W. Barrett, and Jeremy Avigad. Lean-Auto: An Interface Between
         Lean 4 and Automated Theorem Provers. In CAV, 2025. doi:10.1007/978-3-031-98682-6_10.
    30   Michael Rawson, Andrei Voronkov, Johannes Schoisswohl, and Anja Petkovic Komel. Ground Truth:
         Checking Vampire Proofs via Satisfiability Modulo Theories. In CADE, 2025. doi:10.1007/
         978-3-031-99984-0_8.
    31   Giles Reger, Martin Suda, and Andrei Voronkov. New Techniques in Clausal Form Generation. In GCAI,
         2016. doi:10.29007/dzfz.
    32   Neha Rungta. A Billion SMT Queries a Day (Invited Paper). In CAV, 2022. doi:10.1007/
         978-3-031-13185-1_1.
Bodingbauer, Hajdu, Kovács, Polaczek, and Rawson                                                            9


33   Stephan Schulz, Simon Cruanes, and Petar Vukmirovic. Faster, Higher, Stronger: E 2.3. In CADE, 2019.
     doi:10.1007/978-3-030-29436-6_29.
34   Geoff Sutcliffe. Stepping Stones in the TPTP World. In IJCAR, 2024. doi:10.1007/
     978-3-031-63498-7_3.
35   Josef Urban and Geoff Sutcliffe. Automated Reasoning and Presentation Support for Formalizing
     Mathematics in Mizar. In AISC, 2010. doi:10.1007/978-3-642-14128-7_12.
36   Andrei Voronkov. AVATAR: The Architecture for First-Order Theorem Provers. In CAV, 2014. doi:
     10.1007/978-3-319-08867-9_46.
37   Christoph Weidenbach, Dilyana Dimova, Arnaud Fietzke, Rohit Kumar, Martin Suda, and Patrick
     Wischnewski. SPASS version 3.5. In CADE, 2009. doi:10.1007/978-3-642-02959-2_10.
38   Thomas Zhu, Joshua Clune, Jeremy Avigad, Albert Qiaochu Jiang, and Sean Welleck. Premise Se-
     lection for a Lean Hammer, 2025. URL: https://arxiv.org/abs/2506.07477, arXiv:
     2506.07477.
