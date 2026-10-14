                                                                                    Gradual Exact Logic
                                               Unifying Hoare Logic and Incorrectness Logic via Gradual Verification
                                                              Conrad Zimmerman                                                     Jenna DiVincenzo
                                                         zimmerman.co@northeastern.edu                                             jennad@purdue.edu
                                                             Northeastern University                                                Purdue University
                                                               Boston, MA, USA                                                    West Lafayette, IN, USA

                                         Abstract                                                             1.1    Hoare logic
                                         Previously, gradual verification has been developed using            A triple in Hoare logic (HL) [Hoare 1969] is denoted {𝑃 } 𝐶 {𝑄 }.
                                         overapproximating logics such as Hoare logic. We show that           (𝑃, 𝑄 refer to logical specifications; 𝐶 refers to a program
arXiv:2412.00339v1 [cs.LO] 30 Nov 2024




                                         the static verification component of gradual verification is         statement.) Semantically, the triple is valid if, for every state
                                                                                                                                                               𝐶
                                         also connected to underapproximating logics like incorrect-          𝜎 ∈ 𝑃 (i.e., 𝑃 is true of 𝜎), when 𝜎 → 𝜎 ′ (i.e., executing 𝐶
                                         ness logic. To do this, we use a novel definition of gradual         results in 𝜎 ′ ), then 𝜎 ′ ∈ 𝑄:
                                         verification and a novel gradualization of exact logic [Maksi-
                                         movic et al. 2023] which we call gradual exact logic. Further,                               𝑃                             𝑄
                                         we show that Hoare logic, incorrectness logic, and gradual                                                 𝐶
                                         verification can be defined in terms of gradual exact logic.                                             −→
                                            We hope that this connection can be used to develop tools
                                                                                                                 Thus HL is an overapproximating (OX) logic—the postcon-
                                         and techniques that apply to both gradual verification and
                                                                                                              dition 𝑄 overapproximates the states that are reachable from
                                         bug-finding. For example, we envision that techniques de-                                                              𝐶
                                         fined in terms of exact logic can be directly applied to ver-        𝑃; precisely, 𝑄 ⊇ {𝜎 ′ | ∃𝜎 ∈ 𝑃 : 𝜎 → 𝜎 ′ }. HL is a formal
                                         ification, bug-finding, and gradual verification, using the          foundation for program verification precisely because the
                                         principles of gradual typing [Garcia et al. 2016].                   postcondition is true in all ending states.

                                         1    Overview                                                        1.2    Incorrectness logic
                                         Incorrectness logic [O’Hearn 2020] has been recently de-             A triple in incorrectness logic (IL) [O’Hearn 2020] is denoted
                                         veloped as a formal basis for “true bug-finding” and has             [𝑃] 𝐶 [𝑄] 1 . Semantically, the triple is valid if, for every 𝜎 ′ ∈
                                                                                                                                                            𝐶
                                         been applied in industrial-strength tools [Le et al. 2022].          𝑄, there is some 𝜎 ∈ 𝑃 such that 𝜎 → 𝜎 ′ :
                                         Deductions in this logic prove reachability, which enables
                                         bug-finding tools to prove the existence of an invalid state                                 𝑃                             𝑄
                                         while selectively exploring the possible paths.                                                            𝐶
                                                                                                                                                  −→
                                            At the same time, gradual verification (GV) [Bader et al.
                                         2018] addresses the complexity of traditional static verifi-         Thus IL is an underapproximating (UX) logic—the postcondi-
                                         cation. Gradually verified programs may contain imprecise            tion 𝑄 underapproximates the states that are reachable from
                                         specifications—logical formulas annotated to indicate that                                                        𝐶
                                         they contain only a partial specification of behavior. A grad-       𝑃; precisely, 𝑄 ⊆ {𝜎 ′ | ∃𝜎 ∈ 𝑃 : 𝜎 → 𝜎 ′ }. Interpreting 𝑄 as
                                         ual verifier checks the imprecise specifications using static        a specification of a bug, IL is a logic for finding bugs since a
                                         verification where it can and run-time checks (i.e. dynamic          valid triple indicates that the bug is reachable.
                                         verification) elsewhere. These run-time checks can be exer-          1.3    Gradual verification
                                         cised, e.g. with testing, giving the programmer confidence
                                         that their code will not enter a state that violates their partial   Gradual verification (GV) [Bader et al. 2018] reduces the
                                         specifications. Using gradual verification, programmers can          burden of static verification by allowing incomplete (impre-
                                         incrementally verify a program, incrementally learn verifi-          cise) specifications. A gradual verifier may make optimistic
                                         cation constructs, and safely guard unverified components.           assumptions when verifying imprecisely-specified code. Typ-
                                            More recent work [Lööw et al. 2024; Maksimovic et al.             ically, the final program is elaborated to check these assump-
                                         2023; Zilberstein et al. 2023] has produced logics and tools         tions at run-time. However, in this work we focus solely
                                         that unify over-approximating (OX) logic, often used in veri-        on the static verification component of GV so that we can
                                         fication, and under-approximating (UX) logics including IL.          compare its logic with HL and IL.
                                         In this paper, we propose another unification of OX and UX              We denote imprecise triples by {? ∧ 𝑃 } 𝐶 {𝑄 }. Intuitively,
                                         logics that we derive using the principles of gradual verifi-        this triple is valid if there is some 𝑃 ′ ⇒ 𝑃 such that {𝑃 ′ } 𝐶 {𝑄 }
                                         cation. The resulting characterization of IL demonstrates a          1 IL triples often include a specification for error states, but we omit error

                                         previously unexplored connection between GV and IL.                  handling to simplify the comparison with other logics.
                                                                                                     Conrad Zimmerman and Jenna DiVincenzo


is valid in HL. One can think of ? as representing the addi-             First, some definitions: Formula denotes all formulas in
tional assumptions introduced by 𝑃 ′ .                                FOL with arithmetic; we call these precise. SatFormula de-
   For example, the following imprecise triple is valid:              notes all satisfiable formulas. An imprecise formula is of
                  {? ∧ ⊤} 𝑥 ≔ 𝑥 + 1 {𝑥 > 0}                           the form ? ∧ 𝑃 where 𝑃 ∈ Formula. A gradual formula
                                                                      𝑃e ∈ e
                                                                           Formula can be either precise or imprecise.
This follows from the validity of                                        The concretization 𝛾 : e Formula → P (Formula) inter-
               {𝑥 ≥ 0 ∧ ⊤} 𝑥 ≔ 𝑥 + 1 {𝑥 > 0}.                         prets a gradual formulas as sets of precise formulas:
That is, the postcondition is ensured when assuming 𝑥 ≥ 0.              𝛾 (? ∧ 𝑃) = {𝑃 ′ ∈ SatFormula | 𝑃 ′ ⇒ 𝑃 },            𝛾 (𝑃) = {𝑃 }
   However, the assumptions must be plausible; formally, 𝑃 ′
                                                                      Let ⊢ (𝑃) 𝐶 (𝑄) denote a valid EL triple. Deductions in EL,
                                                                                                                               f
(and thus 𝑃) must be satisfiable (i.e., 𝑃 ′ . ⊥). Otherwise,
                                                                              ⊢ (𝑃)
                                                                      denoted e  e 𝐶 (𝑄),
                                                                                       e are defined as a consistent lifting of EL
all imprecise triples would be vacuously valid by taking
                                                                      deductions (Appendix E.2):
𝑃 ′ ≡ ⊥. With this in mind, GV can be stated as a reachability
problem—semantically, {? ∧ 𝑃 } 𝐶 {𝑄 } is valid if there exists        ⊢ (𝑃)
                                                                      e  e 𝐶 (𝑄) def
                                                                              e ⇐⇒   ⊢ (𝑃) 𝐶 (𝑄) for some 𝑃 ∈ 𝛾 (𝑃),
                                                                                                                 e 𝑄 ∈ 𝛾 (𝑄)
                                                                                                                          e
                                             𝐶
some states 𝜎 and 𝜎 ′ such that 𝜎 ∈ 𝑃, 𝜎 → 𝜎 ′ , and 𝜎 ′ ∈ 𝑄:
                                                                      2.3    Strongest postconditions
                    𝑃                       𝑄
                                𝐶                                     sp(𝑃, 𝐶) denotes the strongest (WRT ⇒) 𝑄 for which {𝑃 } 𝐶 {𝑄 }
                               −→
                                                                      is valid (calculated as usual; see Appendix B.2). Strongest
                                                                      postconditions are related to HL, IL, and EL as follows:
By contrapositive, the triple is invalid (i.e., static verification         ⊢ {𝑃 } 𝐶 {𝑄 } ⇐⇒ sp(𝑃, 𝐶) ⇒ 𝑄                  Theorem 2
will error) if it is never possible for 𝐶 to ensure 𝑄, given 𝑃.
  By comparing this diagram with those in §1.1 and §1.2, we                  ⊢ [𝑃] 𝐶 [𝑄] ⇐⇒ sp(𝑃, 𝐶) ⇐ 𝑄                   Theorem 3
can deduce that HL and IL triples are valid imprecise triples,               ⊢ (𝑃) 𝐶 (𝑄) ⇐⇒ sp(𝑃, 𝐶) ≡ 𝑄                   Theorem 4
except for vacuous cases where 𝑃 ≡ ⊥ in HL or 𝑄 ≡ ⊥ in IL.
  Our semantic definition of validity is equivalent to the            2.4    HL and IL via EL
                                                                                           f
previous definition which uses Hoare triples: Let 𝑃 ′ be a            We can characterize valid HL triples as EL
                                                                                                               f triples where the
formula that represents 𝜎 as specifically as possible, then           postcondition is made imprecise. Assuming that 𝑃 . ⊥ and
                                             𝐶
(intuitively) {𝑃 ′ } 𝐶 {𝑄 } is valid since 𝜎 → 𝜎 ′ and 𝜎 ′ ∈ 𝑄.       𝐶 terminates (in either of these cases {𝑃 } 𝐶 {𝑄 } is vacuous),
   But, we can also define valid imprecise triples in terms           we have 𝑃, 𝑄, sp(𝑃, 𝐶) ∈ SatFormula and thus (Theorem 5)
of IL—{? ∧ 𝑃 } 𝐶 {𝑄 } is valid if [𝑃] 𝐶 [𝑄 ′ ] is valid for some                  ⊢ {𝑃 } 𝐶 {𝑄 } ⇐⇒ sp(𝑃, 𝐶) ⇒ 𝑄
𝑄 ′ ⇒ 𝑄. In §2.5 we will prove these definitions equivalent.
                                                                                                    ⇐⇒ sp(𝑃, 𝐶) ∈ 𝛾 (? ∧ 𝑄)
2     Formal foundations                                                                            ⇐⇒ e
                                                                                                       ⊢ (𝑃) 𝐶 (? ∧ 𝑄).
We will now sketch our formal definitions and results. See               Likewise, we can characterize valid IL triples as EL
                                                                                                                           f triples
the appendices for the full statements and proofs.                    where the precondition is made imprecise. Weakest precondi-
    1. We define gradual exact logic—a consistent lifting [Gar-       tions are not always defined for IL [O’Hearn 2020], however,
       cia et al. 2016] of exact logic [Maksimovic et al. 2023].      we can reuse weakest preconditions for HL to witness the
    2. We show that HL, IL, and GV can be characterized by            necessary formula (see Appendix B.3). Assuming 𝑄 . ⊥
       gradual exact logic.                                           (otherwise [𝑃] 𝐶 [𝑄] is vacuous), we have (Theorem 6)
    3. We show that GV contains OX and UX deductions.
    4. We show that, for imprecise specifications, GV can be                   ⊢ [𝑃] 𝐶 [𝑄] ⇐⇒ 𝑄 ⇒ sp(𝑃, 𝐶)
       equivalently defined using OX or UX logics.                                              ⇐⇒ 𝑄 ≡ sp(wp(𝑄, 𝐶) ∧ 𝑃, 𝐶)
                                                                                                ⇐⇒ ⊢ (𝑃 ∧ wp(𝑄, 𝐶)) 𝐶 (𝑄)
2.1   Exact logic
                                                                                                ⇐⇒ e
                                                                                                   ⊢ (? ∧ 𝑃) 𝐶 (𝑄).
Exact logic (EL) [Maksimovic et al. 2023] is the intersection
of HL and IL: an EL triple (𝑃) 𝐶 (𝑄) is valid if {𝑃 } 𝐶 {𝑄 }
                                                                      2.5    GV via HL, EL,
                                                                                        f and IL
and [𝑃] 𝐶 [𝑄] are both valid. Deductions are thus exact—
they can neither under- or overapproximate behavior (see              We can now give a precise definition of GV in terms of HL, as
Appendix E for rules).                                                                                                  ⊢ {𝑃e} 𝐶 {𝑄 }.
                                                                      sketched in §1.32 . We denote valid GV triples as e
                                                                                           def
2.2   Gradual exact logic                                                   ⊢ {𝑃e} 𝐶 {𝑄 } ⇐⇒ ⊢ {𝑃 } 𝐶 {𝑄 } for some 𝑃 ∈ 𝛾 (𝑃)
                                                                            e                                              e
We further define gradual exact logic (EL)
                                       f as a consistent              2 Here we define GV more generally for all gradual preconditions, whereas

lifting [Garcia et al. 2016] of EL.                                   in §1.3 we defined it for imprecise preconditions.
Gradual Exact Logic


Using this definition and applying the characterization of        developed in the context of an exact logic, and then their
HL from §2.4 to characterize GV in terms of EL:                   applications to OX, UX, and GV logics could be derived using
            ⊢ {𝑃e} 𝐶 {𝑄 } ⇐⇒ e
            e                 ⊢ (𝑃)
                                 e 𝐶 (? ∧ 𝑄)                      AGT-style techniques [Garcia et al. 2016].

  For sake of comparison, we can define IL
                                        e as a lifting of IL,     4    Caveats and future work
the same way we have lifted HL to GV.                             While we have proven the results described, we have done
                 def                                              so only for a very restrictive language, and thus our results
     ⊢ [𝑃] 𝐶 [𝑄]
     e        e ⇐⇒   ⊢ [𝑃] 𝐶 [𝑄] for some 𝑄 ∈ 𝛾 (𝑄)
                                                 e
                                                                  should be considered preliminary. In particular, we do not
But, in the case of imprecision this is equivalent to GV. We      consider heaps, method calls, or loops. We expect our results
can see this using the characterization of IL given in §2.4:      extend to these constructs, but showing this will require
         ⊢ [𝑃] 𝐶 [? ∧ 𝑄] ⇐⇒ e
         e                  ⊢ (? ∧ 𝑃) 𝐶 (? ∧ 𝑄)                   significant work.
                                                                     Our definition of GV differs from previous definitions
                           ⇐⇒ e
                              ⊢ {? ∧ 𝑃 } 𝐶 {𝑄 }.
                                                                  [Bader et al. 2018; Wise et al. 2020; Zimmerman et al. 2024].
   Note: GV and ILe differ on precise formulas—e  ⊢ [𝑃] 𝐶 [𝑄]     Our novel definition more clearly demonstrates the connec-
                     ⊢ {𝑃 } 𝐶 {𝑄 }. Also, we do not gradualize
is not equivalent to e                                            tion with IL, and we believe it captures the essence of GV.
postconditions in HL or preconditions in IL because we can        However, this definition only considers static verification,
arbitrarily weaken these specifications already.                  and thus does not consider run-time assertions. We expect
   While verification of precise formulas is a key aspect of      this could be added, and we have hopes that we may be able
GV, this demonstrates that verification of imprecise formu-       to model run-time assertions using an evidence-based cal-
las can be accomplished using IL, and moreover that GV,           culus similar to that of gradual typing Garcia et al. [2016].
when verifying imprecisely-specified code, is proving an IL       In addition, further work is necessary to elucidate how the
deduction. Finally, we can make precise our claim from §1.3       “gradual guarantees” [Garcia et al. 2016] affect the relation
that both OX and UX deductions are valid in (the imprecise        of GV to IL. In particular, the static gradual guarantee seems
fragment of) GV. Assuming 𝑃 . ⊥, we have (immediate from          to prohibit arbitrarily dropping paths, which IL can do.
definition of GV)                                                    Finally, our work is (to our knowledge) the first to explore
                                                                  a gradualization of exact logic. It remains to be seen whether
              ⊢ {𝑃 } 𝐶 {𝑄 } =⇒ e
                               ⊢ {? ∧ 𝑃 } 𝐶 {𝑄 }.
                                                                  this is useful its own right. For example, if library developers
Also, assuming 𝑄 . ⊥, we have                                     write exact specifications, a gradual exact logic could be used
            ⊢ [𝑃] 𝐶 [𝑄] =⇒ e
                           ⊢ (? ∧ 𝑃) 𝐶 (𝑄)                        to aid development of these specifications, similar to how
                                                                  GV aids OX verification. But significantly more work would
                             ⊢ (? ∧ 𝑃) 𝐶 (? ∧ 𝑄)
                          =⇒ e                                    be necessary for this.
                             ⊢ {? ∧ 𝑃 } 𝐶 {𝑄 }.
                          =⇒ e
                                                                  5    Conclusion
Thus GV (and EL)
              f represents the union of HL and IL, while
                                                                  We have demonstrated the similarities and differences of
EL represents the intersection.
                                                                  GV and IL. Specifically, the relation between IL deductions
3    Applications                                                 and EL
                                                                       f deductions with imprecise preconditions shows that
                                                                  the notion of assumptions used in GV is equivalent to the
GV and IL verifiers in practice operate quite similarly; for      consequence rule (and path pruning) in IL. We also have
example, compare the core consume operation of Zimmer-            shown that GV with imprecise specifications is equivalent
man et al. [2024] for a gradual verifier and of Lööw et al.       to IL. Furthermore, we have defined gradual exact logic and
[2024] for an IL verifier. Both types of verifiers make assump-   used this to formally compare IL, HL, and GV. While much
tions, including pruning paths, when establishing a postcon-      work remains before it is widely applicable, we hope that this
dition. This work formalizes the connection between these         framework can be used to develop techniques that uniformly
methods of verification; in particular, gradual verification of   target all three methods of verification.
imprecisely-specified code is equivalent to IL deductions. We
hope that this will allow verifiers that already incorporate      Acknowledgments
both OX and UX logics, for example Lööw et al. [2024], to
                                                                  We thank Devin Singh for his contributions to this work.
be easily extended to GV.
   Similarly, we hope our approach can be used as a frame-
work for unifying techniques across static verification, GV,
and bug-finding. For example, bi-abduction has been de-
veloped in OX logics [Calcagno et al. 2011], applied to UX
verification [Lööw et al. 2024], and is related to GV [DiVin-
cenzo 2023]. We expect that techniques like this could be
                                                                                  Conrad Zimmerman and Jenna DiVincenzo


References
Johannes Bader, Jonathan Aldrich, and Éric Tanter. 2018. Gradual Program
   Verification. In Verification, Model Checking, and Abstract Interpretation -
   19th International Conference, VMCAI 2018, Los Angeles, CA, USA, January
   7-9, 2018, Proceedings (Lecture Notes in Computer Science, Vol. 10747), Isil
   Dillig and Jens Palsberg (Eds.). Springer, 25–46. https://doi.org/10.1007/
   978-3-319-73721-8_2
Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang.
   2011. Compositional Shape Analysis by Means of Bi-Abduction. J. ACM
   58, 6, Article 26 (Dec. 2011), 66 pages. https://doi.org/10.1145/2049697.
   2049700
Jenna Wise DiVincenzo. 2023. Gradual Verification of Recursive Heap Data
   Structures. Ph. D. Dissertation. Carnegie Mellon University.
Ronald Garcia, Alison M. Clark, and Éric Tanter. 2016. Abstracting gradual
   typing. In Proceedings of the 43rd Annual ACM SIGPLAN-SIGACT Sympo-
   sium on Principles of Programming Languages, POPL 2016, St. Petersburg,
   FL, USA, January 20 - 22, 2016, Rastislav Bodík and Rupak Majumdar
   (Eds.). ACM, 429–442. https://doi.org/10.1145/2837614.2837670
C. A. R. Hoare. 1969. An Axiomatic Basis for Computer Programming.
   Commun. ACM 12, 10 (1969), 576–580. https://doi.org/10.1145/363235.
   363259
Quang Loc Le, Azalea Raad, Jules Villard, Josh Berdine, Derek Dreyer, and
   Peter W. O’Hearn. 2022. Finding real bugs in big programs with in-
   correctness logic. Proc. ACM Program. Lang. 6, OOPSLA1 (2022), 1–27.
   https://doi.org/10.1145/3527325
Andreas Lööw, Daniele Nantes-Sobrinho, Sacha-Élie Ayoun, Caroline Cron-
   jäger, Petar Maksimovic, and Philippa Gardner. 2024. Compositional
   Symbolic Execution for Correctness and Incorrectness Reasoning. In
   38th European Conference on Object-Oriented Programming, ECOOP 2024,
   September 16-20, 2024, Vienna, Austria (LIPIcs, Vol. 313), Jonathan Aldrich
   and Guido Salvaneschi (Eds.). Schloss Dagstuhl - Leibniz-Zentrum für
   Informatik, 25:1–25:28. https://doi.org/10.4230/LIPICS.ECOOP.2024.25
Petar Maksimovic, Caroline Cronjäger, Andreas Lööw, Julian Sutherland,
   and Philippa Gardner. 2023. Exact Separation Logic: Towards Bridging
   the Gap Between Verification and Bug-Finding. In 37th European Con-
   ference on Object-Oriented Programming, ECOOP 2023, July 17-21, 2023,
   Seattle, Washington, United States (LIPIcs, Vol. 263), Karim Ali and Guido
   Salvaneschi (Eds.). Schloss Dagstuhl - Leibniz-Zentrum für Informatik,
   19:1–19:27. https://doi.org/10.4230/LIPICS.ECOOP.2023.19
Peter W. O’Hearn. 2020. Incorrectness logic. Proc. ACM Program. Lang. 4,
   POPL (2020), 10:1–10:32. https://doi.org/10.1145/3371078
Jenna Wise, Johannes Bader, Cameron Wong, Jonathan Aldrich, Éric Tanter,
   and Joshua Sunshine. 2020. Gradual verification of recursive heap data
   structures. Proc. ACM Program. Lang. 4, OOPSLA (2020), 228:1–228:28.
   https://doi.org/10.1145/3428296
Noam Zilberstein, Derek Dreyer, and Alexandra Silva. 2023. Outcome Logic:
   A Unifying Foundation for Correctness and Incorrectness Reasoning.
   Proc. ACM Program. Lang. 7, OOPSLA1 (2023), 522–550. https://doi.org/
   10.1145/3586045
Conrad Zimmerman, Jenna DiVincenzo, and Jonathan Aldrich. 2024. Sound
   Gradual Verification with Symbolic Execution. Proc. ACM Program. Lang.
   8, POPL (2024), 2547–2576. https://doi.org/10.1145/3632927
Gradual Exact Logic


A      Grammar                                                      The following explicit calculations correspond to the pre-
We define a basic language that includes mutable variables       vious definition (proved in Theorem 1):
and conditionals. Note that we do not include while loops                   wp(skip, 𝑄) = 𝑄
or functions; these constructs are left for future work.                    wp(𝑥 ≔ 𝐸, 𝑄) = 𝑄 [𝑥/𝐸]
                                                                            wp(𝐶 1 ; 𝐶 2, 𝑄) = wp(𝐶 1, wp(𝐶 2, 𝑄))
       Expr ∋ 𝐸 F 𝑛 | ⊥ | ⊤ | 𝑥 | 𝐸 ∨ 𝐸 | 𝐸 ∧ 𝐸 |
                                                                            wp(if 𝐸 then 𝐶 1 else 𝐶 2, 𝑄) =
                      𝐸 = 𝐸 | 𝐸 < 𝐸 | ¬𝐸
                                                                               (wp(𝐶 1, 𝑄) ∧ 𝐸) ∨ (wp(𝐶 2, 𝑄) ∧ ¬𝐸)
       Cmd ∋ 𝐶 F skip | 𝑥 ≔ 𝐸 | if 𝐸 then 𝐶 else 𝐶 | 𝐶; 𝐶
                                                                 Lemma 1 (Stronger postcondition). If 𝑄 ⇒ 𝑄 ′ then
Asrt ∋ 𝑃, 𝑄, 𝑅 F 𝐸 | ¬𝑃 | 𝑃 ∧ 𝑃 | 𝑃 ∨ 𝑃 | ∃𝑥 𝑃
                                                                 wp(𝐶, 𝑄) ⇒ wp(𝐶, 𝑄 ′ ).
where 𝑛 ∈ Z and 𝑥 a variable name.
   We assume that programs are typed correctly; for example,     Proof. By induction on 𝐶:
expressions 𝐸 in if 𝐸 then 𝐶 1 else 𝐶 2 will always evaluate        skip:
to a boolean value.                                                         wp(skip, 𝑄) ≡ 𝑄 ⇒ 𝑄 ′ ≡ wp(skip, 𝑄 ′ )
Definition 1 (Implication). 𝑃 ⇒ 𝑄 if all states that satisfy        𝑥 ≔ 𝐸:
𝑃 also satisfy 𝑄.                                                  wp(𝑥 ≔ 𝐸, 𝑄) ≡ 𝑄 [𝐸/𝑥] ⇒ 𝑄 ′ [𝐸/𝑥] ≡ wp(𝑥 ≔ 𝐸, 𝑄 ′ )
   Note: we do not formalize states or the semantics of asser-      𝐶1 ; 𝐶2 :
tions; we assume that our logic is close enough to first-order           (1) wp(𝐶 2, 𝑄) ⇒ wp(𝐶 2, 𝑄 ′ ) by induction
logic and thus use FOL deductions to reason about assertions.            (2) wp(𝐶 1, wp(𝐶 2, 𝑄)) ⇒ wp(𝐶 1, wp(𝐶 2, 𝑄 ′ )) by in-
   Note: We use · ⇒ · to denote implication between formu-                    duction using (1)
las in first-order logic with booleans and arithmetic. · =⇒ ·            (3) wp(𝐶 1 ; 𝐶 2, 𝑄) ⇒ wp(𝐶 1 ; 𝐶 2, 𝑄 ′ ) by (2) and defi-
denotes “if-then” in our metatheory.                                          nition of wp
Definition 2 (Equivalence of propositions). 𝑃 ≡ 𝑄 denotes           if 𝐸 then 𝐶 1 else 𝐶 2 :
that 𝑃 and 𝑄 are logically equivalent; that is,                          (1) wp(𝐶 1, 𝑄) ⇒ wp(𝐶 1, 𝑄 ′ ) by induction
                         def                                             (2) wp(𝐶 2, 𝑄) ⇒ wp(𝐶 2, 𝑄 ′ ) by induction
             𝑃 ≡ 𝑄 ⇐⇒ 𝑃 ⇒ 𝑄 and 𝑄 ⇒ 𝑃 .                                  (3) By (1) and (2)
Throughout this paper, we assume that identity of propo-                 (wp(𝐶 1, 𝑄) ∧ 𝐸) ∨ (wp(𝐶 2, 𝑄) ∧ ¬𝐸)
sitions coincides with equivalence; that is, when we write
                                                                            ⇒ (wp(𝐶 1, 𝑄 ′ ) ∧ 𝐸) ∨ (wp(𝐶 2, 𝑄 ′ ) ∧ ¬𝐸)
an individual proposition, technically we are denoting the
equivalence class that contains that proposition. For example,           (4) By (3) and definition of wp
{⊤, ⊥} = {1 = 1, 1 = 2}.                                                     wp(if 𝐸 then 𝐶 1 else 𝐶 2, 𝑄)
Definition 3 (Replacement). 𝑃 [𝑥/𝐸] denotes 𝑃 with all free                      ⇒ wp(if 𝐸 then 𝐶 1 else 𝐶 2, 𝑄 ′ )              □
occurrences of 𝑥 replaced by 𝐸.
                                                                 B.2   Strongest postconditions
Definition 4. fv(𝑃) denotes the free variables in the asser-     Definition 8. 𝑄 is the strongest postcondition for precondi-
tion 𝑃.                                                          tion 𝑃 and statement 𝐶, denoted sp(𝑃, 𝐶), if it is the strongest
Definition 5. fv(𝐶) denotes all variables referenced or as-      predicate (WRT ⇒) that ensures that if a state satisfies 𝑃,
signed in 𝐶.                                                     then after executing 𝐶, 𝑄 holds.
Definition 6. mod(𝐶) denotes all variables assigned in 𝐶.           The following explicit calculations correspond to the pre-
Explicitly,                                                      vious definition (proved in Theorem 2):
                 mod(skip) ≔ ∅                                             sp(𝑃, skip) = 𝑃
                       mod(𝑥 ≔ 𝐸) ≔ 𝑥                                      sp(𝑃, 𝑥 ≔ 𝐸) = ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣])
                       mod(𝐶 1 ; 𝐶 2 ) ≔ mod(𝐶 1 ) ∪ mod(𝐶 2 )               where 𝑣 ∉ fv(𝑃)
      mod(if 𝐸 then 𝐶 1 else 𝐶 2 ) ≔ mod(𝐶 1 ) ∪ mod(𝐶 2 )                 sp(𝑃, 𝐶 1 ; 𝐶 2 ) = sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )
                                                                           sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 ) =
B      Predicate transformers                                                 sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ ¬𝐸, 𝐶 2 )
B.1     Weakest preconditions
                                                                 Lemma 2 (Stronger precondition). If 𝑃 ⇒ 𝑃 ′ then
Definition 7. 𝑃 is the weakest precondition for a statement      sp(𝑃, 𝐶) ⇒ sp(𝑃 ′, 𝐶).
𝐶 and postcondition 𝑄, denoted wp(𝐶, 𝑄), if it is the weakest
predicate (WRT ⇒) that ensures that if a state satisfies 𝑃,      Proof. By induction on 𝐶:
then after executing 𝐶, 𝑄 holds.                                    skip: sp(𝑃, skip) ≡ 𝑃 ⇒ 𝑃 ′ ≡ sp(𝑃 ′, skip).
                                                                                                        Conrad Zimmerman and Jenna DiVincenzo


    𝑥 ≔ 𝐸: Note that 𝑃 [𝑥/𝑣] ⇒ 𝑃 ′ [𝑥/𝑣] by logic. Then:                             (2) sp(𝑃, 𝑥 ≔ 𝐸) ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣])
   sp(𝑃, 𝑥 ≔ 𝐸) ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣])     defn sp                             (3) ⊤ ≡ ∀𝑣 (𝑥 ≠ 𝐸 [𝑥/𝑣] ∨ ¬𝑃 [𝑥/𝑣]) by logic using
                                                                                        (1) and (2)
                   ⇒ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 ′ [𝑥/𝑣])                logic
                           ′
                                                                                     (4) ⊤ ≡ ∀𝑣¬𝑃 [𝑥/𝑣] by logic using (3)
                   ≡ sp(𝑃 , 𝑥 ≔ 𝐸)                            defn sp                   We prove this using a semantic argument (assum-
   𝐶1 ; 𝐶2 :                                                                            ing standard Kripke semantics for FOL):
        (1) sp(𝑃, 𝐶 1 ) ⇒ sp(𝑃 ′, 𝐶 1 ) by induction                                    Let M be a model and y ∈ |M |. By (3) we have
        (2) sp(sp(𝑃, 𝐶 1 ), 𝐶 2 ) ⇒ sp(sp(𝑃 ′, 𝐶 1 ), 𝐶 2 ) by induc-                   M ⊨ ∀𝑣 (𝑥 ≠ 𝐸 [𝑥/𝑣]∨¬𝑃 [𝑥/𝑣]), and thus M [𝑣 ↦→
             tion using (1)                                                             y] ⊨ 𝑥 ≠ 𝐸 [𝑥/𝑣] ∨ ¬𝑃 [𝑥/𝑣].
        (3) By (2) and definition of sp,                                                Let z = J𝐸 [𝑥/𝑣]K M [𝑣↦→y] . Then we have M [𝑣 ↦→
                sp(𝑃, 𝐶 1 ; 𝐶 2 ) ≡ sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )                               y, 𝑥 ↦→ z] ⊭ 𝑥 ≠ 𝐸 [𝑥/𝑣].
                               ⇒ sp(sp(𝑃 ′, 𝐶 1 ), 𝐶 2 )                                Thus we have M [𝑣 ↦→ y, 𝑥 ↦→ z] ⊨ ¬𝑃 [𝑥/𝑣]. Since
                                                                                        𝑥 ∉ fv(𝑃 [𝑥/𝑣]), we have M [𝑣 ↦→ y] ⊨ ¬𝑃 [𝑥/𝑣].
                               ≡ sp(𝑃 ′, 𝐶 1 ; 𝐶 2 )                                    Thus we can conclude that M ⊨ ∀𝑣¬𝑃 [𝑥/𝑣].
   if 𝐸 then 𝐶 1 else 𝐶 2 :                                                          (5) ⊤ ≡ ¬𝑃 [𝑥/𝑣] ≡ ¬𝑃 by logic using (4) and since
       (1) 𝑃 ∧ 𝐸 ⇒ 𝑃 ′ ∧ 𝐸 by logic                                                     𝑣 ∉ fv(𝑃)
       (2) sp(𝑃 ∧𝐸, 𝐶 1 ) ⇒ sp(𝑃 ′ ∧𝐸, 𝐶 1 ) by induction using                      (6) ⊥ ≡ 𝑃 by logic using (5)
          (1)                                                                   𝐶1 ; 𝐶2
       (3) 𝑃 ∧ ¬𝐸 ⇒ 𝑃 ′ ∧ ¬𝐸 by logic                                                (1) ⊥ ≡ sp(𝑃, 𝐶 1 ; 𝐶 2 ) by assumption
       (4) sp(𝑃 ∧ ¬𝐸, 𝐶 2 ) ⇒ sp(𝑃 ′ ∧ ¬𝐸, 𝐶 2 ) by induction                        (2) sp(𝑃, 𝐶 1 ; 𝐶 2 ) ≡ sp(sp(𝑃, 𝐶 1 ), 𝐶 2 ) by definition
           using (3)                                                                 (3) ⊥ ≡ sp(sp(𝑃, 𝐶 1 ), 𝐶 2 ) by logic using (1) and (2)
       (5)                                                                           (4) ⊥ ≡ sp(𝑃, 𝐶 1 ) by induction using (3)
  sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 )                                                     (5) ⊥ ≡ 𝑃 by induction using (4)
     ≡ sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ ¬𝐸, 𝐶 2 )                    defn sp                [if 𝐸 then 𝐶 1 else 𝐶 2 ]
                                                                                     (1) ⊥ ≡ sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 ) by assumption
     ⇒ sp(𝑃 ′ ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ′ ∧ ¬𝐸, 𝐶 2 )          (2), (4), logic
                                                                                     (2) sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 ) ≡ sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨
     ≡ sp(𝑃 ′, if 𝐸 then 𝐶 1 else 𝐶 2 )                      defn sp □                  sp(𝑃 ∧ ¬𝐸, 𝐶 2 ) by definition
                                                                                     (3) ⊥ ≡ sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ ¬𝐸, 𝐶 2 ) by (1) and (2)
Lemma 3. sp(⊥, 𝐶) ≡ ⊥                                                                (4) ⊥ ≡ sp(𝑃 ∧ 𝐸, 𝐶 1 ) by logic using (3)
Proof. By induction on 𝐶:                                                            (5) ⊥ ≡ sp(𝑃 ∧ ¬𝐸, 𝐶 2 ) by logic using (3)
   skip: sp(⊥, skip) ≡ ⊥ by definition.                                              (6) ⊥ ≡ 𝑃 ∧ 𝐸 by induction using (4)
   𝑥 ≔ 𝐸: sp(⊥, 𝑥 ≔ 𝐸) ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ ⊥) ≡ ⊥ by                                 (7) ⊥ ≡ 𝑃 ∧ ¬𝐸 by induction using (5)
       logic.                                                                        (8) ⊥ ≡ (𝑃 ∧ 𝐸) ∨ (𝑃 ∧ ¬𝐸) ≡ 𝑃 ∧ (𝐸 ∨ ¬𝐸) ≡ 𝑃 by
   if 𝐸 then 𝐶 1 else 𝐶 2 :                                                             logic using (6) and (7)                                  □
     sp(⊥, if 𝐸 then 𝐶 1 else 𝐶 2 )
       ≡ sp(⊥ ∧ 𝐸, 𝐶 1 ) ∨ sp(⊥ ∧ ¬𝐸, 𝐶 2 )                 defn sp          Lemma 5. If 𝑃 ∈ SatFormula then sp(𝑃, 𝐶) ∈ SatFormula.
       ≡ sp(⊥, 𝐶 1 ) ∨ sp(⊥, 𝐶 2 )                             logic         Proof. We prove the contrapositive: assume sp(𝑃, 𝐶) ∉
       ≡⊥∨⊥                                              induction           SatFormula, then sp(𝑃, 𝐶) ≡ ⊥, and thus by Lemma 4 𝑃 ≡
        ≡⊥                                                     logic         ⊥. Therefore 𝑃 ∉ SatFormula.                          □
   𝐶1 ; 𝐶2 :
     sp(⊥, 𝐶 1 ; 𝐶 2 ) ≡ sp(sp(⊥, 𝐶 1 ), 𝐶 2 )            defn sp            Lemma 6. If 𝑦 ∉ fv(𝐶) then sp(∃𝑦 𝑃, 𝐶) ≡ ∃𝑦 sp(𝑃, 𝐶).
                      ≡ sp(⊥, 𝐶 2 )                     induction
                                                                             Proof. By induction on 𝐶:
                      ≡⊥                                induction        □
                                                                                skip: sp(∃𝑦 𝑃, skip) ≡ ∃𝑦 𝑃 ≡ ∃𝑦 sp(𝑃, skip)
Lemma 4. sp(𝑃, 𝐶) ≡ ⊥ =⇒ 𝑃 ≡ ⊥                                                  𝑥 ≔ 𝐸: Assuming 𝑦 . 𝑣,
   Note: for a more expressive language, we would also need
                                                                              sp(∃𝑦 𝑃, 𝑥 ≔ 𝐸)
termination for this to hold.
                                                                                 ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ (∃𝑦 𝑃) [𝑥/𝑣])                     defn sp
Proof. By induction on 𝐶:                                                        ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ (∃𝑦 𝑃 [𝑥/𝑣])) 𝑦 . 𝑥 ∈ fv(𝑥 ≔ 𝐸)
   skip: ⊥ ≡ sp(𝑃, skip) ≡ 𝑃 by definition.                                      ≡ ∃𝑦∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣])               𝑦 ∉ fv(𝐸 [𝑥/𝑣])
   𝑥 ≔ 𝐸:
       (1) ⊥ ≡ sp(𝑃, 𝑥 ≔ 𝐸) by assumption                                        ≡ ∃𝑦 sp(𝑃, 𝑥 ≔ 𝐸)                                     defn sp
Gradual Exact Logic


    𝐶1 ; 𝐶2 :                                                                Lemma 8 (Frame rule). If mod(𝐶) ∩ fv(𝑃) = ∅ then
    sp(∃𝑦 𝑃, 𝐶 1 ; 𝐶 2 ) ≡ sp(sp(∃𝑦 𝑃, 𝐶 1 ), 𝐶 2 )          defn sp         sp(𝑃 ∧ 𝑅, 𝐶) ≡ 𝑃 ∧ sp(𝑅, 𝐶).
                        ≡ sp(∃𝑦 sp(𝑃, 𝐶 1 ), 𝐶 2 )         induction         Proof. By induction on 𝐶:
                        ≡ ∃𝑦 sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )         induction            skip: sp(𝑃 ∧ 𝑅, skip) ≡ 𝑃 ∧ 𝑅 ≡ 𝑃 ∧ sp(𝑅, skip)
                   ≡ ∃𝑦 sp(𝑃, 𝐶 1 ; 𝐶 2 )                    defn sp            𝑥 ≔ 𝐸: Let 𝑣 ∉ fv(𝑃). Note that 𝑥 ∈ fv(𝑥 ≔ 𝐸), thus
                                                                                    from our assumptions 𝑥 ∉ fv(𝑃) Then,
   if 𝐸 then 𝐶 1 else 𝐶 2 :
                                                                                sp(𝑃 ∧ 𝑅, 𝑥 ≔ 𝐸)
sp(∃𝑦 𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 )
                                                                                     ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣] ∧ 𝑅 [𝑥/𝑣])             defn sp
   ≡ sp((∃𝑦 𝑃) ∧ 𝐸, 𝐶 1 ) ∨ sp((∃𝑦 𝑃) ∧ ¬𝐸, 𝐶 2 )               defn sp
                                                                                     ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 ∧ 𝑅 [𝑥/𝑣])                 𝑥 ∉ fv(𝑃)
   ≡ sp(∃𝑦 (𝑃 ∧ 𝐸), 𝐶 1 ) ∨ sp(∃𝑦 (𝑃 ∧ ¬𝐸), 𝐶 2 )             𝑦 ∉ fv(𝐸)
                                                                                     ≡ 𝑃 ∧ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑅 [𝑥/𝑣])                 𝑣 ∉ fv(𝑃)
   ≡ (∃𝑦 sp(𝑃 ∧ 𝐸, 𝐶 1 )) ∨ (∃𝑦 sp(𝑃 ∧ ¬𝐸, 𝐶 2 ))             induction
                                                                                    ≡ 𝑃 ∧ sp(𝑅, 𝑥 ≔ 𝐸)                            defn sp
   ≡ ∃𝑦 (sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ ¬𝐸, 𝐶 2 ))                      logic
                                                                                𝐶 1 ; 𝐶 2 : Note that 𝑥 ∉ mod(𝐶 1 ; 𝐶 2 ) thus 𝑥 ∉ mod(𝐶 1 )
   ≡ ∃𝑦 sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 )                          defn sp □            and 𝑥 mod(𝐶 2 ). Then,
Lemma 7. sp(𝑃1 ∨ 𝑃2, 𝐶) ≡ sp(𝑃1, 𝐶) ∨ sp(𝑃2, 𝐶)                                 sp(𝑃 ∧ 𝑅, 𝐶 1 ; 𝐶 2 ) ≡ sp(sp(𝑃 ∧ 𝑅, 𝐶 1 ), 𝐶 2 ) defn sp
                                                                                                        ≡ sp(𝑃 ∧ sp(𝑅, 𝐶 1 ), 𝐶 2 )   induction
Proof. By induction on 𝐶:
                                                                                                        ≡ 𝑃 ∧ sp(sp(𝑅, 𝐶 1 ), 𝐶 2 )   induction
    skip: sp(𝑃1 ∨ 𝑃2, skip) ≡ 𝑃 1 ∨ 𝑃 2 ≡
      sp(𝑃1, skip) ∨ sp(𝑃2, skip).                                                               ≡ 𝑃 ∧ sp(𝑅, 𝐶 1 ; 𝐶 2 )     defn sp
    𝑥 ≔ 𝐸:                                                                      if 𝐸 then 𝐶 1 else 𝐶 2 : Note that by assumption
   sp(𝑃1 ∨ 𝑃2, 𝑥 ≔ 𝐸)                                                              𝑥 ∉ mod(if 𝐸 then 𝐶 1 else 𝐶 2 ) thus 𝑥 ∉ mod(𝐶 1 )
                                                                                   and 𝑥 ∉ mod(𝐶 2 ). Then,
      ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ (𝑃 1 ∨ 𝑃 2 ) [𝑥/𝑣])                 defn sp
                                                                              sp(𝑃 ∧ 𝑅, if 𝐸 then 𝐶 1 else 𝐶 2 )
      ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ (𝑃 1 [𝑥/𝑣] ∨ 𝑃2 [𝑥/𝑣]))              subst.
                                                                                   ≡ sp(𝑃 ∧ 𝑅 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ 𝑅 ∧ ¬𝐸, 𝐶 2 )           defn sp
      ≡ ∃𝑣 ((𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 1 [𝑥/𝑣]) ∨
                                                                                   ≡ (𝑃 ∧ sp(𝑅 ∧ 𝐸, 𝐶 1 )) ∨ (𝑃 ∧ sp(𝑅 ∧ ¬𝐸, 𝐶 2 ))          ind.
              (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃2 [𝑥/𝑣]))                         logic
                                                                                   ≡ 𝑃 ∧ (sp(𝑅 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑅 ∧ ¬𝐸, 𝐶 2 ))               logic
      ≡ (∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 1 [𝑥/𝑣])) ∨
                                                                                   ≡ 𝑃 ∧ sp(𝑅, if 𝐸 then 𝐶 1 else 𝐶 2 )                   defn sp □
          (∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃2 [𝑥/𝑣]))                         logic
                                                                             Lemma 9.
      ≡ sp(𝑃 1, 𝑥 ≔ 𝐸) ∨ sp(𝑃2, 𝑥 ≔ 𝐸)                        defn sp
                                                                                sp(𝑃 ∧ 𝐸, if 𝐸 then 𝐶 1 else 𝐶 2 ) ≡ sp(𝑃 ∧ 𝐸, 𝐶 1 )
    𝐶1 ; 𝐶2 :
                                                                                   sp(𝑃 ∧ ¬𝐸, if 𝐸 then 𝐶 1 else 𝐶 2 ) ≡ sp(𝑃 ∧ ¬𝐸, 𝐶 2 )
   sp(𝑃1 ∨ 𝑃2, 𝐶 1 ; 𝐶 2 )
      ≡ sp(sp(𝑃 1 ∨ 𝑃 2, 𝐶 1 ), 𝐶 2 )                         defn sp        Proof.
                                                                               sp(𝑃 ∧ 𝐸, if 𝐸 then 𝐶 1 else 𝐶 2 )
      ≡ sp(sp(𝑃 1, 𝐶 1 ) ∨ sp(𝑃2, 𝐶 1 ), 𝐶 2 )              induction
                                                                                    ≡ sp(𝑃 ∧ 𝐸 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ 𝐸 ∧ ¬𝐸, 𝐶 2 )         defn sp
      ≡ sp(sp(𝑃 1, 𝐶 1 ), 𝐶 2 ) ∨ sp(sp(𝑃2, 𝐶 1 ), 𝐶 2 )    induction
                                                                                    ≡ sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨ sp(⊥, 𝐶 2 )                        logic
     ≡ sp(𝑃1, 𝐶 1 ; 𝐶 2 ) ∨ sp(𝑃 2, 𝐶 1 ; 𝐶 2 )               defn sp
    if 𝐸 then 𝐶 1 else 𝐶 2 :                                                        ≡ sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨ ⊥                              Lemma 3
  sp(𝑃 1 ∨ 𝑃 2, if 𝐸 then 𝐶 1 else 𝐶 2 )                                            ≡ sp(𝑃 ∧ 𝐸, 𝐶 1 )                                      logic
     ≡ sp(𝐸 ∧ (𝑃1 ∨ 𝑃2 ), 𝐶 1 ) ∨                                            sp(𝑃 ∧ ¬𝐸, if 𝐸 then 𝐶 1 else 𝐶 2 )
         sp(¬𝐸 ∧ (𝑃1 ∨ 𝑃2 ), 𝐶 2 )                            defn sp           ≡ sp(𝑃 ∧ 𝐸 ∧ ¬𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ ¬𝐸 ∧ ¬𝐸, 𝐶 2 )            defn sp
     ≡ sp((𝐸 ∧ 𝑃1 ) ∨ (𝐸 ∧ 𝑃2 ), 𝐶 1 ) ∨                                        ≡ sp(⊥, 𝐶 1 ) ∨ sp(𝑃 ∧ ¬𝐸, 𝐶 2 )                             logic
         sp((¬𝐸 ∧ 𝑃1 ) ∨ (¬𝐸 ∧ 𝑃2 ), 𝐶 2 )                       logic          ≡ ⊥ ∨ sp(𝑃 ∧ ¬𝐸, 𝐶 2 )                                   Lemma 3
     ≡ sp(𝐸 ∧ 𝑃1, 𝐶 1 ) ∨ sp(𝐸 ∧ 𝑃2, 𝐶 1 ) ∨                                    ≡ sp(𝑃 ∧ ¬𝐸, 𝐶 2 )                                       logic □
         sp(¬𝐸 ∧ 𝑃1, 𝐶 2 ) ∨ sp(¬𝐸 ∧ 𝑃2, 𝐶 2 )               Lemma 7
                                                                             B.3     Fixpoint
     ≡ (sp(𝐸 ∧ 𝑃1, 𝐶 1 ) ∨ sp(¬𝐸 ∧ 𝑃1, 𝐶 2 )) ∨
                                                                             We can define a function 𝑄 ↦→ sp(wp(𝐶, 𝑄), 𝐶). We demon-
         (sp(𝐸 ∧ 𝑃2, 𝐶 1 ) ∨ sp(¬𝐸 ∧ 𝑃2, 𝐶 2 ))                  logic
                                                                             strate that this function reaches a fixpoint.
     ≡ sp(𝑃1, if 𝐸 then 𝐶 1 else 𝐶 2 ) ∨
                                                                             Lemma 10. sp(wp(𝐶, 𝑄) ∧ 𝑃, 𝐶) ≡ 𝑄 ∧ sp(𝑃, 𝐶)
         sp(𝑃2, if 𝐸 then 𝐶 1 else 𝐶 2 )                      defn sp
                                                                         □   Proof. By induction on 𝐶:
                                                                                                   Conrad Zimmerman and Jenna DiVincenzo


   skip: sp(wp(skip, 𝑄) ∧ 𝑃, skip) ≡ 𝑄 ∧ 𝑃 ≡                         Lemma 11 (Fixpoint property). If 𝑄 ⇒ sp(⊤, 𝐶) then
     𝑄 ∧ sp(𝑃, skip)                                                 𝑄 ≡ sp(wp(𝐶, 𝑄), 𝐶).
   𝑥 ≔ 𝐸: Let 𝑣 ∉ fv(𝑄). Then,
                                                                     Proof. Immediate from Lemma 10, noting that 𝑄 ≡ 𝑄 ∧
sp(wp(𝑥 ≔ 𝐸, 𝑄) ∧ 𝑃, 𝑥 ≔ 𝐸)
                                                                     sp(⊤, 𝐶) in this case.                            □
  ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧
         (wp(𝑥 ≔ 𝐸, 𝑄) ∧ 𝑃) [𝑥/𝑣])                        defn sp    Lemma 12. If 𝑄 ⇒ sp(𝑃, 𝐶) then 𝑄 ≡ sp(𝑃 ∧ wp(𝐶, 𝑄), 𝐶).
  ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ (𝑄 [𝑥/𝐸] ∧ 𝑃) [𝑥/𝑣])               defn wp
                                                                     Proof.
  ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑄 [𝑥/𝐸 [𝑥/𝑣]] ∧ 𝑃 [𝑥/𝑣])               subst            𝑄 ≡ 𝑄 ∧ sp(𝑃, 𝐶)                       𝑄 ⇒ sp(𝑃, 𝐶)
  ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑄 [𝑥/𝑥] ∧ 𝑃 [𝑥/𝑣])                  subst =                ≡ sp(𝑃 ∧ wp(𝐶, 𝑄), 𝐶)                  Lemma 10         □
  ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑄 ∧ 𝑃 [𝑥/𝑣])                     redundant
  ≡ 𝑄 ∧ (∃𝑣 𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣])                      𝑣 ∉ fv(𝑄)    C      Hoare logic
 ≡ 𝑄 ∧ sp(𝑃, 𝑥 ≔ 𝐸)                                  defn sp         Hoare triples are denoted by ⊢ {𝑃 } 𝐶 {𝑄 }. Deductions in
  if 𝐸 then 𝐶 1 else 𝐶 2 :                                           Hoare logic are characterized by the following rules:
      (1) 𝑄 ∧ sp(𝑃 ∧ 𝐸, 𝐶 1 ) ≡ sp(wp(𝐶 1, 𝑄) ∧ 𝑃 ∧ 𝐸, 𝐶 1 ) by
                                                                              OX-Skip                      OX-Assign
          induction using 𝐶 1
      (2) 𝑄 ∧ sp(𝑃 ∧ ¬𝐸, 𝐶 2 ) ≡ sp(wp(𝐶 2, 𝑄) ∧ 𝑃 ∧ ¬𝐸, 𝐶 2 )                ⊢ {𝑃 } skip {𝑃 }             ⊢ {𝑃 [𝑥/𝐸]} 𝑥 ≔ 𝐸 {𝑃 }
          by induction using 𝐶 2                                      OX-Seq                       OX-If
      (3)                                                                  ⊢ {𝑃 } 𝐶 1 {𝑅}                    ⊢ {𝐸 ∧ 𝑃 } 𝐶 1 {𝑄 }
 𝑄 ∧ sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 )                                        ⊢ {𝑅} 𝐶 2 {𝑄 }                   ⊢ {¬𝐸 ∧ 𝑃 } 𝐶 2 {𝑄 }
     ≡ 𝑄 ∧ (sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ ¬𝐸, 𝐶 2 ))        defn sp         ⊢ {𝑃 } 𝐶 1 ; 𝐶 2 {𝑄 }        ⊢ {𝑃 } if 𝐸 then 𝐶 1 else 𝐶 2 {𝑄 }
                                                                                 OX-Cons
     ≡ (𝑄 ∧ sp(𝑃 ∧ 𝐸, 𝐶 1 )) ∨
                                                                                 𝑃 ⇒ 𝑃′          ⊢ {𝑃 ′ } 𝐶 {𝑄 ′ }     𝑄′ ⇒ 𝑄
        (𝑄 ∧ sp(𝑃 ∧ ¬𝐸, 𝐶 2 ))                            logic
                                                                                                  ⊢ {𝑃 } 𝐶 {𝑄 }
     ≡ sp(wp(𝐶 1, 𝑄) ∧ 𝑃 ∧ 𝐸, 𝐶 1 ) ∨
        sp(wp(𝐶 2, 𝑄) ∧ 𝑃 ∧ ¬𝐸, 𝐶 2 )                   (1), (2)     C.1      Weakest preconditions
     ≡ sp(wp(𝐶 1, 𝑄) ∧ 𝑃 ∧ 𝐸,                                        Lemma 13. If ⊢ {𝑃 } 𝐶 {𝑄 } then 𝑃 ⇒ wp(𝐶, 𝑄).
           if 𝐸 then 𝐶 1 else 𝐶 2 ) ∨                                Proof. By induction on the derivation of ⊢ {𝑃 } 𝐶 {𝑄 }:
        sp(wp(𝐶 2, 𝑄) ∧ 𝑃 ∧ ¬𝐸,                                            OX-Skip:
           if 𝐸 then 𝐶 1 else 𝐶 2 )                  Lemma 9                 (1) 𝑃 ≡ 𝑄 by inversion
     ≡ sp(((wp(𝐶 1, 𝑄) ∧ 𝐸) ∨                                                (2) 𝑃 ≡ 𝑄 ≡ wp(skip, 𝑄) by definition
             (wp(𝐶 2, 𝑄) ∧ ¬𝐸)) ∧ 𝑃,                                       OX-Assign:
                                                                             (1) 𝑃 ≡ 𝑄 [𝐸/𝑥] by inversion
            if 𝐸 then 𝐶 1 else 𝐶 2 )                 Lemma 7                 (2) 𝑃 ≡ 𝑄 [𝐸/𝑥] ≡ wp(𝑥 ≔ 𝐸, 𝑄) by definition
     ≡ sp(wp(if 𝐸 then 𝐶 1 else 𝐶 2, 𝑄) ∧ 𝑃,                               OX-Seq:
             if 𝐸 then 𝐶 1 else 𝐶 2 )                    defn wp             (1) ⊢ {𝑃 } 𝐶 1 {𝑅} for some 𝑅 by inversion
  𝐶1 ; 𝐶2 :                                                                  (2) 𝑃 ⇒ sp(𝐶 1, 𝑅) by induction using (1)
       (1) wp(𝐶 2, 𝑄) ∧ sp(𝑃, 𝐶 1 ) ≡ sp(wp(𝐶 1,                             (3) ⊢ {𝑅} 𝐶 2 {𝑄 } by inversion
            wp(𝐶 2, 𝑄)) ∧ 𝑃, 𝐶 1 ) by induction using 𝐶 1                    (4) 𝑅 ⇒ wp(𝐶 2, 𝑄) by induction using (3)
       (2) 𝑄 ∧ sp(sp(𝑃, 𝐶 1 ), 𝐶 2 ) ≡ sp(wp(𝐶 2, 𝑄) ∧                       (5) wp(𝐶 1, 𝑅) ⇒ wp(𝐶 1, wp(𝐶 2, 𝑄)) by Lemma 1 us-
            sp(𝑃, 𝐶 1 ), 𝐶 2 ) by induction using 𝐶 2 . Then,                   ing (4)
                                                                             (6) By (4), (5), and definition of wp,
 𝑄 ∧ sp(𝑃, 𝐶 1 ; 𝐶 2 )
                                                                                        𝑃 ⇒ wp(𝐶 1, 𝑅)
    ≡ 𝑄 ∧ sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )                       defn sp
                                                                                               ⇒ wp(𝐶 1, wp(𝐶 2, 𝑄))
    ≡ sp(wp(𝐶 2, 𝑄) ∧ sp(𝑃, 𝐶 1 ), 𝐶 2 )                   (2)
                                                                                         ≡ wp(𝐶 1 ; 𝐶 2, 𝑄)
    ≡ sp(sp(wp(𝐶 1, wp(𝐶 2, 𝑄)) ∧ 𝑃, 𝐶 1 ), 𝐶 2 )          (1)
                                                                           OX-If:
    ≡ sp(sp(wp(𝐶 1 ; 𝐶 2, 𝑄) ∧ 𝑃, 𝐶 1 ), 𝐶 2 )       defn wp                 (1) ⊢ {𝐸 ∧ 𝑃 } 𝐶 1 {𝑄 } by inversion
    ≡ sp(wp(𝐶 1 ; 𝐶 2, 𝑄) ∧ 𝑃, 𝐶 1 ; 𝐶 2 )            defn sp □              (2) 𝐸 ∧ 𝑃 ⇒ wp(𝐶 1, 𝑄) by induction using (1)
                                                                             (3) ⊢ {¬𝐸 ∧ 𝑃 } 𝐶 2 {𝑄 } by inversion
                                                                             (4) ¬𝐸 ∧ 𝑃 ⇒ wp(𝐶 2, 𝑄) by induction using (3)
Gradual Exact Logic


       (5)                                                          Proof. By induction on ⊢ {𝑃 } 𝐶 {𝑄 }:
  𝑃 ≡ (𝑃 ∧ 𝐸) ∨ (𝑃 ∧ ¬𝐸)                               logic            OX-Skip: Then 𝑃 ≡ 𝑄 and 𝐶 ≡ skip, thus
      ⇒ (wp(𝐶 1, 𝑄) ∧ 𝐸) ∨ (wp(𝐶 2, 𝑄) ∧ ¬𝐸)      (2) and (4)              sp(𝑃, skip) ≡ 𝑃 ≡ 𝑄.
                                                                        OX-Assign: Then 𝑃 ≡ 𝑄 [𝑥/𝐸] and 𝐶 ≡ 𝑥 ≔ 𝐸. Assum-
      ⇒ wp(if 𝐸 then 𝐶 1 else 𝐶 2, 𝑄)             defn wp
                                                                           ing 𝑣 ∉ fv(𝑄):
      OX-Cons:
                                                                       sp(𝑄 [𝑥/𝐸], 𝑥 ≔ 𝐸)
        (1) 𝑃 ⇒ 𝑃 ′ for some 𝑃 ′ by inversion
        (2) 𝑄 ′ ⇒ 𝑄 for some 𝑄 ′ by inversion                            ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑄 [𝑥/𝐸] [𝑥/𝑣])              defn
        (3) ⊢ {𝑃 ′ } 𝐶 {𝑄 ′ } by inversion                               ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑄 [𝑥/𝐸 [𝑥/𝑣]))      substitution
        (4) 𝑃 ′ ⇒ wp(𝐶, 𝑄 ′ ) by induction using (3)                     ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑄 [𝑥/𝑥])          subst. equality
        (5) wp(𝐶, 𝑄 ′ ) ⇒ wp(𝐶, 𝑄) by Lemma 1 using (4)
                                                                         ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑄)                    redundant
        (6) 𝑃 ⇒ 𝑃 ′ ⇒ wp(𝐶, 𝑄 ′ ) ⇒ wp(𝐶, 𝑄) by (1), (4),
           and (5)                                        □             ⇒𝑄                                            𝑣 ∉ fv(𝑄)
                                                                       OX-Seq:
Lemma 14. ⊢ {wp(𝐶, 𝑄)} 𝐶 {𝑄 }                                            (1) 𝐶 ≡ 𝐶 1 ; 𝐶 2 for some 𝐶 1, 𝐶 2 by inversion
Proof. By induction on 𝐶:                                                (2) ⊢ {𝑃 } 𝐶 1 {𝑅} for some 𝑅 by inversion
                                                                         (3) ⊢ {𝑅} 𝐶 2 {𝑄 } by inversion
   skip: wp(skip, 𝑄) ≡ 𝑄 by definition; ⊢ (𝑄) skip (𝑄)
                                                                         (4) sp(𝑃, 𝐶 1 ) ⇒ 𝑅 by induction using (2)
       by OX-Skip.
                                                                         (5) sp(sp(𝑃, 𝐶 1 ), 𝐶 2 ) ⇒ sp(𝑅, 𝐶 2 ) by Lemma 2 using
   𝑥 ≔ 𝐸:
                                                                            (4)
        (1) wp(𝑥 ≔ 𝐸, 𝑄) ≡ 𝑄 [𝑥/𝐸] by definition
                                                                         (6) sp(𝑅, 𝐶 2 ) ⇒ 𝑄 by induction using (3)
        (2) ⊢ {𝑄 [𝑥/𝐸]} 𝑥 ≔ 𝐸 {𝑄 } by OX-Assign using (1)
                                                                         (7) sp(sp(𝑃, 𝐶 1 ), 𝐶 2 ) ⇒ 𝑄 by (5) and (6)
   𝐶1 ; 𝐶2 :
                                                                         (8) sp(𝑃, 𝐶) ≡ sp(𝑃, 𝐶 1 ; 𝐶 2 ) ⇒ 𝑄 by (1), (7), and
        (1) ⊢ {wp(𝐶 1, wp(𝐶 2, 𝑄))} 𝐶 1 {wp(𝐶 2, 𝑄)} by induc-
                                                                            definition of sp
             tion
                                                                       OX-If:
        (2) ⊢ {wp(𝐶 2, 𝑄)} 𝐶 2 {𝑄 } by induction
                                                                         (1) 𝐶 ≡ if 𝐸 then 𝐶 1 else 𝐶 2 for some 𝐸, 𝐶 1, 𝐶 2 by
        (3) ⊢ {wp(𝐶 1, wp(𝐶 2, 𝑄))} 𝐶 1 ; 𝐶 2 {𝑄 } by OX-Seq us-
                                                                            inversion
             ing (1) and (2)
                                                                         (2) ⊢ {𝐸 ∧ 𝑃 } 𝐶 1 {𝑄 } by inversion
        (4) wp(𝐶 1 ; 𝐶 2, 𝑄) ≡ wp(𝐶 1, wp(𝐶 2, 𝑄)) by definition
                                                                         (3) ⊢ {¬𝐸 ∧ 𝑃 } 𝐶 2 {𝑄 } by inversion
        (5) ⊢ {wp(𝐶 1 ; 𝐶 2, 𝑄)} 𝐶 1 ; 𝐶 2 {𝑄 } by (3) and (4)
                                                                         (4) sp(𝐸 ∧ 𝑃, 𝐶 1 ) ⇒ 𝑄 by induction using (2)
   if 𝐸 then 𝐶 1 else 𝐶 2 :
                                                                         (5) sp(¬𝐸 ∧ 𝑃, 𝐶 2 ) ⇒ 𝑄 by induction using (3)
        (1) Let 𝑃 ≡ (wp(𝐶 1, 𝑄) ∧ 𝐸) ∨ (wp(𝐶 2, 𝑄) ∧ ¬𝐸)
                                                                         (6) sp(𝐸 ∧𝑃, 𝐶 1 ) ∨sp(¬𝐸 ∧𝑃, 𝐶 2 ) ⇒ 𝑄 by logic using
        (2) ⊢ {wp(𝐶 1, 𝑄)} 𝐶 1 {𝑄 } by induction
                                                                            (4) and (5)
        (3) 𝑃 ∧ 𝐸 ⇒ wp(𝐶 1, 𝑄) by logic
                                                                         (7) sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 ) ⇒ 𝑄 by (6) and
        (4) ⊢ {𝑃 ∧ 𝐸} 𝐶 1 {𝑄 } by OX-Cons using (2) and (3)
                                                                            definition of sp
        (5) ⊢ {wp(𝐶 2, 𝑄)} 𝐶 2 {𝑄 } by induction
                                                                       OX-Cons:
        (6) 𝑃 ∧ ¬𝐸 ⇒ wp(𝐶 2, 𝑄) by logic
                                                                         (1) 𝑃 ⇒ 𝑃 ′ for some 𝑃 ′ by inversion
        (7) ⊢ {𝑃 ∧ ¬𝐸} 𝐶 2 {𝑄 } by OX-Cons using (5) and (6)
                                                                         (2) 𝑄 ′ ⇒ 𝑄 for some 𝑄 ′ by inversion
        (8) ⊢ {𝑃 } if 𝐸 then 𝐶 1 else 𝐶 2 {𝑄 } by OX-If using
                                                                         (3) ⊢ {𝑃 ′ } 𝐶 {𝑄 ′ } by inversion
             (4) and (7)
                                                                         (4) sp(𝑃, 𝐶) ⇒ sp(𝑃 ′, 𝐶) by Lemma 2 and (1)
        (9) 𝑃 ≡ wp(if 𝐸 then 𝐶 1 else 𝐶 2, 𝑄) by (1) and
                                                                         (5) sp(𝑃 ′, 𝐶) ⇒ 𝑄 ′ by induction using (3)
             definition of wp
                                                                         (6) sp(𝑃, 𝐶) ⇒ 𝑄 by (4), (5), and (2)                  □
        (10) ⊢ {wp(if 𝐸 then 𝐶 1 else 𝐶 2 )}
             if 𝐸 then 𝐶 1 else 𝐶 2 {𝑄 } by (8) and (9)        □    Lemma 17. ⊢ {𝑃 } 𝐶 {sp(𝑃, 𝐶)}

Lemma 15. If 𝑃 ⇒ wp(𝐶, 𝑄) then ⊢ {𝑃 } 𝐶 {𝑄 }.                       Proof. By induction on 𝐶:
                                                                       skip:
Proof. By Lemma 14, ⊢ {wp(𝐶, 𝑄)} 𝐶 {𝑄 }, thus by OX-Cons                   (1) ⊢ {𝑃 } skip {𝑃 } by OX-Skip
⊢ {𝑃 } 𝐶 {𝑄 }.                                         □                   (2) 𝑃 ≡ sp(𝑃, skip) by OX-Skip
Theorem 1. 𝑃 ⇒ wp(𝐶, 𝑄) ⇐⇒ ⊢ {𝑃 } 𝐶 {𝑄 }.                                  (3) ⊢ {𝑃 } skip {sp(𝑃, skip)} by OX-Cons using (1)
                                                                              and (2)
Proof. =⇒: Lemma 15; ⇐=: Lemma 13.                              □      𝑥 ≔ 𝐸:
                                                                           (1) Let 𝑄 ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣]) where 𝑣 ∉
C.2     Strongest postconditions                                              fv(𝑃).
Lemma 16. If ⊢ {𝑃 } 𝐶 {𝑄 } then sp(𝑃, 𝐶) ⇒ 𝑄.                              (2) ⊢ {𝑄 [𝐸/𝑥]} 𝑥 ≔ 𝐸 {𝑄 } by OX-Assign
                                                                                                    Conrad Zimmerman and Jenna DiVincenzo


         (3) 𝑃 ⇒ ∃𝑣 (𝐸 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣]) ≡ 𝑄 [𝑥/𝐸] by                 D.1   Strongest postconditions
              logic (witnessed by letting 𝑣 = 𝑥).                        Lemma 19. ⊢ [𝑃] 𝐶 [sp(𝑃, 𝐶)]
         (4) ⊢ {𝑃 } 𝑥 ≔ 𝐸 {𝑄 } by OX-Cons using (2) and (3)
         (5) ⊢ {𝑃 } 𝑥 ≔ 𝐸 {sp(𝑃, 𝑥 ≔ 𝐸)} by (1), (4), and                Proof. By induction on 𝐶:
              definition of sp                                              skip: By UX-Skip ⊢ [𝑃] skip [𝑃] and 𝑃 ≡ sp(𝑃, skip)
    𝐶1 ; 𝐶2 :                                                                   by definition.
         (1) ⊢ {𝑃 } 𝐶 1 {sp(𝑃, 𝐶 1 )} by induction                          𝑥 ≔ 𝐸:
         (2) ⊢ {sp(𝑃, 𝐶 1 )} 𝐶 2 {sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )} by induction            (1) ⊢ [𝑃] 𝑥 ≔ 𝐸 [∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣])] by UX-
         (3) ⊢ {𝑃 } 𝐶 1 ; 𝐶 2 {sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )} by OX-Seq using                 Assign
              (1) and (2)                                                        (2) sp(𝑃, 𝑥 ≔ 𝐸) ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣]) by
         (4) sp(𝑃, 𝐶 1 ; 𝐶 2 ) ≡ sp(sp(𝑃, 𝐶 1 ), 𝐶 2 ) by definition                  definition of sp
         (5) ⊢ {𝑃 } 𝐶 1 ; 𝐶 2 {sp(𝑃, 𝐶 1 ; 𝐶 2 )} by (3) and (4)                 (3) ⊢ [𝑃] 𝑥 ≔ 𝐸 [𝑠𝑝 (𝑃, 𝑥 ≔ 𝐸)] by (1) and (2)
    if 𝐸 then 𝐶 1 else 𝐶 2 :                                                𝐶1 ; 𝐶2 :
         (1) ⊢ {𝑃 ∧ 𝐸} 𝐶 1 {sp(𝑃 ∧ 𝐸, 𝐶 1 )} by induction                        (1) ⊢ [𝑃] 𝐶 1 [sp(𝑃, 𝐶 1 )] by induction
         (2) ⊢ {𝑃 ∧ ¬𝐸} 𝐶 2 {sp(𝑃 ∧ ¬𝐸, 𝐶 2 )} by induction                      (2) ⊢ [sp(𝑃, 𝐶 1 )] 𝐶 2 [sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )] by induction
         (3) ⊢ {𝑃 ∧ 𝐸} 𝐶 1 {sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ ¬𝐸, 𝐶 2 )} by               (3) ⊢ [𝑃] 𝐶 1 ; 𝐶 2 [sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )] by UX-Seq using
              OX-Cons using (1)                                                       (1), (2)
         (4) ⊢ {𝑃 ∧ ¬𝐸} 𝐶 2 {sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ ¬𝐸, 𝐶 2 )}                 (4) sp(𝑃, 𝐶 1 ; 𝐶 2 ) ≡ sp(sp(𝑃, 𝐶 1 ), 𝐶 2 ) by definition
              by OX-Cons using (2)                                               (5) ⊢ [𝑃] 𝐶 1 ; 𝐶 2 [sp(𝑃, 𝐶 1 ; 𝐶 2 )] by (3), (4)
         (5) ⊢ {𝑃 } if 𝐸 then 𝐶 1 else 𝐶 2 {sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨               if 𝐸 then 𝐶 1 else 𝐶 2 :
              sp(𝑃 ∧ ¬𝐸, 𝐶 2 )} by OX-If using (3) and (4)                       (1) ⊢ [𝐸 ∧ 𝑃] 𝐶 1 [sp(𝐸 ∧ 𝑃, 𝐶 1 )] by induction
         (6) ⊢ {𝑃 } if 𝐸 then 𝐶 1 else 𝐶 2                                       (2) ⊢ [¬𝐸 ∧ 𝑃] 𝐶 2 [sp(¬𝐸 ∧ 𝑃, 𝐶 2 )] by induction
              {sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 )} by (5) and defini-                (3) ⊢ [𝐸 ∧ 𝑃] if 𝐸 then 𝐶 1 else 𝐶 2 [sp(𝐸 ∧ 𝑃, 𝐶 1 )]
              tion of sp                                             □                by UX-IfThen using (1)
                                                                                 (4) ⊢ [¬𝐸 ∧𝑃] if 𝐸 then 𝐶 1 else 𝐶 2 [sp(¬𝐸 ∧𝑃, 𝐶 2 )]
                                                                                      by UX-IfElse using (2)
Lemma 18. If sp(𝑃, 𝐶) ⇒ 𝑄 then ⊢ {𝑃 } 𝐶 {𝑄 }.
                                                                                 (5) ⊢ [𝑃] if 𝐸 then 𝐶 1 else 𝐶 2 [sp(𝐸 ∧ 𝑃, 𝐶 1 ) ∨
Proof. Immediate from Lemma 17, applying OX-Cons.                   □                 sp(¬𝐸 ∧ 𝑃, 𝐶 2 )] by UX-Disj using (3) and (4)
                                                                                 (6) sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 ) ≡ sp(𝐸 ∧ 𝑃, 𝐶 1 ) ∨
                                                                                      sp(¬𝐸 ∧ 𝑃, 𝐶 2 ) by definition
Theorem 2. sp(𝑃, 𝐶) ⇒ 𝑄 ⇐⇒ ⊢ {𝑃 } 𝐶 {𝑄 }
                                                                                 (7) ⊢ [𝑃] if 𝐸 then 𝐶 1 else 𝐶 2
Proof. =⇒: Lemma 18; ⇐=: Lemma 16                                   □                 [sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 )] by (5) and (6) □
                                                                         Lemma 20. If 𝑄 ⇒ sp(𝑃, 𝐶) then ⊢ [𝑃] 𝐶 [𝑄].
D    Incorrectness logic                                                 Proof. Immediate from Lemma 19 and UX-Cons.                      □
Incorrectness logic triples are denoted ⊢ [𝑃] 𝐶 [𝑄]. Deduc-
tions in incorrectness logic are defined as follows:                     Lemma 21. If ⊢ [𝑃] 𝐶 [𝑄] then 𝑄 ⇒ sp(𝑃, 𝐶).
                               UX-Seq                                    Proof. By induction on the derivation ⊢ [𝑃] 𝐶 [𝑄]:
    UX-Skip                    ⊢ [𝑃] 𝐶 1 [𝑄]        ⊢ [𝑄] 𝐶 2 [𝑅]           UX-Skip:
    ⊢ [𝑃] skip [𝑃]                      ⊢ [𝑃] 𝐶 1 ; 𝐶 2 [𝑅]                     (1) 𝑄 ≡ 𝑃 by inversion
          UX-Assign                                                             (2) sp(𝑃, skip) ≡ 𝑃 by definition
                                                                                (3) 𝑄 ≡ sp(𝑃, skip) by (1) and (2)
           ⊢ [𝑃] 𝑥 ≔ 𝐸 [∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣])]
                                                                            UX-Assign:
              UX-IfThen
                           ⊢ [𝐸 ∧ 𝑃] 𝐶 1 [𝑄]                                    (1) 𝑄 ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣]) by inversion
                                                                                (2) sp(𝑃, 𝑥 ≔ 𝐸) ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣]) by
              ⊢ [𝐸 ∧ 𝑃] if 𝐸 then 𝐶 1 else 𝐶 2 [𝑄]                                 definition
            UX-IfElse                                                           (3) 𝑄 ≡ sp(𝑃, 𝑥 ≔ 𝐸) by (1) and (2)
                           ⊢ [¬𝐸 ∧ 𝑃] 𝐶 2 [𝑄]
                                                                            UX-Seq:
              ⊢ [¬𝐸 ∧ 𝑃] if 𝐸 then 𝐶 1 else 𝐶 2 [𝑄]                             (1) ⊢ [𝑃] 𝐶 1 [𝑅] for some 𝑅 by inversion
       UX-Cons                                                                  (2) ⊢ [𝑅] 𝐶 2 [𝑄] by inversion
          𝑃′ ⇒ 𝑃                  UX-Disj                                       (3) 𝑄 ⇒ sp(𝑅, 𝐶 2 ) by induction using (2)
       ⊢ [𝑃 ′ ] 𝐶 [𝑄 ′ ]                 ⊢ [𝑃1 ] 𝐶 [𝑄 1 ]                       (4) 𝑅 ⇒ sp(𝑃, 𝐶 1 ) by induction using (1)
          𝑄 ⇒ 𝑄′                         ⊢ [𝑃2 ] 𝐶 [𝑄 2 ]                       (5) sp(𝑅, 𝐶 2 ) ⇒ sp(sp(𝑃, 𝐶 1 ), 𝐶 2 ) by Lemma 2 using
        ⊢ [𝑃] 𝐶 [𝑄]                ⊢ [𝑃1 ∨ 𝑃2 ] 𝐶 [𝑄 1 ∨ 𝑄 2 ]                     (4)
Gradual Exact Logic


        (6)                                                        Theorem 3. ⊢ [𝑃] 𝐶 [𝑄] ⇐⇒ 𝑄 ⇒ sp(𝑃, 𝐶)
           𝑄 ⇒ sp(𝑅, 𝐶 2 )                         (3)             Proof. =⇒: Lemma 21; ⇐=: Lemma 20.                                  □
              ⇒ sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )              (5)
            ≡ sp(𝑃, 𝐶 1 ; 𝐶 2 )              defn sp               D.2   Satisfiability
    UX-IfThen:                                                     Lemma 22. If ⊢ [⊥] 𝐶 [𝑄] then 𝑄 ≡ ⊥.
      (1) 𝐶 ≡ if 𝐸 then 𝐶 1 else 𝐶 2 for some 𝐸, 𝐶 1, 𝐶 2 by       Proof.
          inversion
                                                                      (1) 𝑄 ⇒ sp(⊥, 𝐶) by Theorem 2
      (2) 𝑃 ≡ 𝐸 ∧ 𝑃 ′ for some 𝑃 ′ by inversion
                                                                      (2) sp(⊥, 𝐶) ≡ ⊥ by Lemma 3
      (3) ⊢ [𝐸 ∧ 𝑃 ′ ] 𝐶 1 [𝑄] by inversion
                                                                      (3) 𝑄 ⇒ ⊥ logic using (1) and (2)
      (4) 𝑄 ⇒ sp(𝐸 ∧ 𝑃 ′, 𝐶 1 ) by induction using (3)
                                                                      (4) 𝑄 ≡ ⊥ by logic using (3)                                     □
      (5) sp(𝐸 ∧𝑃 ′, 𝐶 1 ) ≡ sp(𝐸 ∧𝑃 ′, if 𝐸 then 𝐶 1 else 𝐶 2 )
          by Lemma 9                                               Lemma 23. If ⊢ [𝑃] 𝐶 [𝑄] and 𝑄 ∈ SatFormula then 𝑃 ∈
      (6)                                                          SatFormula.
     𝑄 ⇒ sp(𝐸 ∧ 𝑃 ′, 𝐶 1 )                            (4)
                                                                   Proof. Assume ⊢ [𝑃] 𝐶 [𝑄], then we prove the contraposi-
          ≡ sp(𝐸 ∧ 𝑃 ′, if 𝐸 then 𝐶 1 else 𝐶 2 )         (5)       tive; that is, 𝑃 ∉ SatFormula =⇒ 𝑄 ∉ SatFormula.
        ≡ sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 )          (2)                 Assuming 𝑃 ∉ SatFormula, since 𝑃 ∈ Formula we get
    UX-IfElse:                                                     𝑃 ≡ ⊥, and thus ⊢ [⊥] 𝐶 [𝑄] by assumption. Then by
      (1) 𝐶 ≡ if 𝐸 then 𝐶 1 else 𝐶 2 for some 𝐸, 𝐶 1, 𝐶 2 by       Lemma 22, 𝑄 ≡ ⊥ thus 𝑄 ∉ SatFormula.                  □
          inversion                                                Lemma 24. If ⊢ [𝑃] 𝐶 [𝑄] and 𝑄 ∈ SatFormula then 𝑃 ∧
      (2) 𝑃 ≡ ¬𝐸 ∧ 𝑃 ′ for some 𝑃 ′ by inversion                   wp(𝑃, 𝐶) ∈ SatFormula.
      (3) ⊢ [¬𝐸 ∧ 𝑃 ′ ] 𝐶 2 [𝑄] by inversion
      (4) 𝑄 ⇒ sp(¬𝐸 ∧ 𝑃 ′, 𝐶 2 ) by induction using (3)            Proof.
      (5) sp(¬𝐸 ∧ 𝑃 ′, 𝐶 2 ) ≡ sp(¬𝐸 ∧ 𝑃 ′,                           (1) ⊢ [𝑃] 𝐶 [𝑄] by assumption
          if 𝐸 then 𝐶 1 else 𝐶 2 ) by Lemma 9                         (2) 𝑄 ∈ SatFormula by assumption
      (6)                                                             (3) 𝑄 ⇒ sp(𝑃, 𝐶) by Lemma 21 using (1)
     𝑄 ⇒ sp(¬𝐸 ∧ 𝑃 ′, 𝐶 2 )                        (4)                (4) sp(𝑃 ∧ wp(𝑃, 𝐶), 𝐶) ≡ 𝑄 by Lemma 12 using (3)
         ≡ sp(¬𝐸 ∧ 𝑃 ′, if 𝐸 then 𝐶 1 else 𝐶 2 )         (5)          (5) ⊢ [𝑃 ∧ wp(𝑃, 𝐶)] 𝐶 [𝑄] by Lemma 20 using (4)
                                                                      (6) 𝑃 ∧ wp(𝐶, 𝑄) ∈ SatFormula by Lemma 23 using (2)
       ≡ sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 )                 (2)               and (5)                                       □
    UX-Cons:
      (1) ⊢ [𝑃 ′ ] 𝐶 [𝑄 ′ ] for some 𝑃 ′, 𝑄 ′ by inversion         E     Exact logic
      (2) 𝑃 ′ ⇒ 𝑃 by inversion                                     Exact logic triples are denoted by ⊢ (𝑃) 𝐶 (𝑄). Deductions
      (3) 𝑄 ⇒ 𝑄 ′ by inversion                                     in exact logic are characterized by the following rules:
      (4) 𝑄 ′ ⇒ sp(𝑃 ′, 𝐶) by induction using (1)                                                  EX-Assign
      (5) sp(𝑃 ′, 𝐶) ⇒ sp(𝑃, 𝐶) by Lemma 2 using (2)               EX-Skip                                     𝑥 ∉ fv(𝐸 ′ )
      (6) 𝑄 ⇒ 𝑄 ′ ⇒ sp(𝑃 ′, 𝐶) ⇒ sp(𝑃, 𝐶) by (3), (4), and
                                                                   ⊢ (⊤) skip (⊤)                  ⊢ (𝑥 = 𝐸 ′ ) 𝑥 ≔ 𝐸 (𝑥 = 𝐸 [𝑥/𝐸 ′ ])
         (5)
                                                                                                                     EX-Seq
    UX-Disj:
                                                                   EX-IfThen                                           ⊢ (𝑃) 𝐶 1 (𝑅)
      (1) ⊢ [𝑃1 ] 𝐶 [𝑄 1 ] for some 𝑃1, 𝑄 1 by inversion
                                                                               ⊢ (𝑃 ∧ 𝐸) 𝐶 1 (𝑄)                       ⊢ (𝑅) 𝐶 2 (𝑄)
      (2) ⊢ [𝑃2 ] 𝐶 [𝑄 2 ] for some 𝑃2, 𝑄 2 by inversion
      (3) 𝑃 ≡ 𝑃1 ∨ 𝑃2 by inversion                                 ⊢ (𝑃 ∧ 𝐸) if 𝐸 then 𝐶 1 else 𝐶 2 (𝑄)              ⊢ (𝑃) 𝐶 1 ; 𝐶 2 (𝑄)
      (4) 𝑄 ≡ 𝑄 1 ∨ 𝑄 2 by inversion                                                                           EX-Frame
      (5) 𝑄 1 ⇒ sp(𝑃1, 𝐶) by induction using (1)                   EX-IfElse                                   mod(𝐶) ∩ fv(𝑅) = ∅
      (6) 𝑄 2 ⇒ sp(𝑃2, 𝐶) by induction using (2)                               ⊢ (𝑃 ∧ ¬𝐸) 𝐶 2 (𝑄)                 ⊢ (𝑃) 𝐶 (𝑄)
      (7) 𝑄 1 ∨ 𝑄 2 ⇒ sp(𝑃1, 𝐶) ∨ sp(𝑃2, 𝐶) by logic using         ⊢ (𝑃 ∧ ¬𝐸) if 𝐸 then 𝐶 1 else 𝐶 2 (𝑄) ⊢ (𝑃 ∧ 𝑅) 𝐶 (𝑄 ∧ 𝑅)
         (5) and (6)                                               EX-Exists                               EX-Disj
      (8)                                                              ⊢ (𝑃) 𝐶 (𝑄)                               ⊢ (𝑃1 ) 𝐶 (𝑄 1 )
       𝑄 ≡ 𝑄1 ∨ 𝑄2                                   (4)                𝑥 ∉ fv(𝐶)                                ⊢ (𝑃2 ) 𝐶 (𝑄 2 )
            ⇒ sp(𝑃1, 𝐶) ∨ sp(𝑃2, 𝐶)                  (7)           ⊢ (∃𝑥 𝑃) 𝐶 (∃𝑥 𝑄)                   ⊢ (𝑃1 ∨ 𝑃2 ) 𝐶 (𝑄 1 ∨ 𝑄 2 )
            ≡ sp(𝑃1 ∨ 𝑃2, 𝐶)                  Lemma 7                 Note: We drop the equivalence rule, since it is immediately
                                                                   valid by our characterization of formulas by equivalence
            ≡ sp(𝑃, 𝐶)                               (3)       □   classes.
                                                                                                    Conrad Zimmerman and Jenna DiVincenzo


E.1     Strongest postconditions                                               (4) 𝑥 ∉ fv(𝐸 ′ ) by inversion
Lemma 25. ⊢ (𝑃) 𝐶 (sp(𝑃, 𝐶))                                                   (5)
                                                                             sp(𝑃, 𝐶)
Proof. By induction on 𝐶:
                                                                                ≡ sp(𝑥 = 𝐸 ′, 𝑥 ≔ 𝐸)                         (1), (2)
    skip: By EX-Skip ⊢ (𝑃) skip (𝑃) and 𝑃 ≡ sp(𝑃, skip)
                                                                                                                   ′
       by definition.                                                           ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ (𝑥 = 𝐸 ) [𝑥/𝑣])         defn sp
    𝐶 ≡ 𝑥 ≔ 𝐸:                                                                                                ′
                                                                                ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑣 = 𝐸 )                        (4)
        (1) 𝑃 ≡ ∃𝑦 (𝑥 = 𝑦∧𝑃 ′ ) for some 𝑃 ′ since ∃𝑦 (𝑥 = 𝑦) is                                    ′              ′
                                                                                ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝐸 ] ∧ 𝑣 = 𝐸 )                  logic
            a tautology. WLOG assume 𝑥 ∉ fv(𝑃 ′ ) (instances                                   ′               ′
            of 𝑥 can be replaced with 𝑦).                                       ≡ 𝑥 = 𝐸 [𝑥/𝐸 ] ∧ ∃𝑣 𝑣 = 𝐸                          (4)
        (2) ⊢ (𝑥 = 𝑦) 𝑥 ≔ 𝐸 (𝑥 = 𝐸 [𝑥/𝑦]) by EX-Assign.                                        ′
                                                                                ≡ 𝑥 = 𝐸 [𝑥/𝐸 ]                                logic
        (3) ⊢ (𝑥 = 𝑦 ∧ 𝑃 ′ ) 𝑥 ≔ 𝐸 (𝑥 = 𝐸 [𝑥/𝑦] ∧ 𝑃 ′ ) by                      ≡𝑄                                            (3)
            EX-Frame and (2).
                                                                            EX-IfThen:
        (4) ⊢ (∃𝑦 (𝑥 = 𝑦 ∧ 𝑃 ′ )) 𝑥 ≔ 𝐸 (∃𝑦 (𝑥 = 𝐸 [𝑥/𝑦] ∧ 𝑃 ′ ))
                                                                               (1) 𝐶 ≡ if 𝐸 then 𝐶 1 else 𝐶 2 by inversion
            by EX-Exists and (3).
                                                                               (2) 𝑃 ≡ 𝑃 ′ ∧ 𝐸 for some 𝑃 ′ by inversion
        (5)
                                                                               (3) ⊢ (𝑃 ′ ∧ 𝐸) 𝐶 1 (𝑄) by inversion
 sp(𝑃, 𝑥 ≔ 𝐸) ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ 𝑃 [𝑥/𝑣])                defn                 (4) 𝑄 ≡ sp(𝑃 ′ ∧ 𝐸, 𝐶 1 ) by induction using (3)
                  ≡ ∃𝑣 (𝑥 = 𝐸 [𝑥/𝑣] ∧ (∃𝑦 (𝑣 = 𝑦 ∧ 𝑃 ′ )))          (1)        (5)
                                            ′
                     ≡ ∃𝑦 (𝑥 = 𝐸 [𝑥/𝑦] ∧ 𝑃 )                        logic   sp(𝑃, 𝐶)
           (6) ⊢ (𝑃) 𝑥 ≔ 𝐸 (sp(𝑃, 𝑥 ≔ 𝐸)) by (1), (4), and (5).                ≡ sp(𝑃 ′ ∧ 𝐸, if 𝐸 then 𝐶 1 else 𝐶 2 )         (1), (2)
      𝐶1 ; 𝐶2 :                                                                        ′
                                                                               ≡ sp(𝑃 ∧ 𝐸, 𝐶 1 )                           Lemma 9
           (1) ⊢ (𝑃) 𝐶 (sp(𝑃, 𝐶 1 )) by induction
                                                                               ≡𝑄                                             (4)
           (2) ⊢ (sp(𝑃, 𝐶 1 )) 𝐶 2 (sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )) by induction
           (3) ⊢ (𝑃) 𝐶 1 ; 𝐶 2 (sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )) by EX-Seq using      EX-IfElse:
                (1), (2)                                                       (1) 𝐶 ≡ if 𝐸 then 𝐶 1 else 𝐶 2 by inversion
           (4) sp(sp(𝑃, 𝐶 1 ), 𝐶 2 ) ≡ sp(𝑃, 𝐶 1 ; 𝐶 2 ) by definition         (2) 𝑃 ≡ 𝑃 ′ ∧ ¬𝐸 for some 𝑃 ′ by inversion
           (5) ⊢ (𝑃) 𝐶 1 ; 𝐶 2 (sp(𝑃, 𝐶 1 ; 𝐶 2 )) by (3) and (4)              (3) ⊢ (𝑃 ′ ∧ ¬𝐸) 𝐶 2 (𝑄) by inversion
      if 𝐸 then 𝐶 1 else 𝐶 2 :                                                 (4) 𝑄 ≡ sp(𝑃 ′ ∧ ¬𝐸, 𝐶 2 ) by induction using (3)
           (1) ⊢ (𝑃 ∧ 𝐸) 𝐶 1 (sp(𝑃 ∧ 𝐸, 𝐶 1 )) by induction                    (5)
           (2) ⊢ (𝑃 ∧ ¬𝐸) 𝐶 2 (sp(𝑃 ∧ ¬𝐸, 𝐶 2 )) by induction               sp(𝑃, 𝐶)
           (3) ⊢ (𝑃 ∧ 𝐸) if 𝐸 then 𝐶 1 else 𝐶 2 (sp(𝑃 ∧ 𝐸, 𝐶 1 ))              ≡ sp(𝑃 ′ ∧ ¬𝐸, if 𝐸 then 𝐶 1 else 𝐶 2 )        (1), (2)
                by EX-IfThen using (1)                                                ′
                                                                               ≡ sp(𝑃 ∧ ¬𝐸, 𝐶 2 )                          Lemma 9
           (4) ⊢ (𝑃 ∧¬𝐸) if 𝐸 then 𝐶 1 else 𝐶 2 (sp(𝑃 ∧¬𝐸, 𝐶 2 ))
                by EX-IfElse using (2)                                        ≡𝑄                                                 (4)
           (5) ⊢ ((𝑃 ∧ 𝐸) ∨ (𝑃 ∧ ¬𝐸)) if 𝐸 then 𝐶 1 else 𝐶 2                EX-Seq:
                (sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ ¬𝐸, 𝐶 2 )) by EX-Disj using          (1) 𝐶 ≡ 𝐶 1 ; 𝐶 2 for some 𝐶 1, 𝐶 2 by inversion
                (3), (4)                                                       (2) ⊢ (𝑃) 𝐶 1 (𝑅) for some 𝑅 by inversion
           (6) (𝑃 ∧ 𝐸) ∨ (𝑃 ∧ ¬𝐸) ≡ 𝑃 by logic                                 (3) ⊢ (𝑅) 𝐶 2 (𝑄) by inversion
           (7) sp(𝑃 ∧ 𝐸, 𝐶 1 ) ∨ sp(𝑃 ∧ ¬𝐸, 𝐶 2 ) ≡                            (4) 𝑅 ≡ sp(𝑃, 𝐶 1 ) by induction using (2)
                sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 ) by definition                   (5) 𝑄 ≡ sp(𝑅, 𝐶 2 ) by induction using (3)
           (8) ⊢ (𝑃) if 𝐸 then 𝐶 1 else 𝐶 2                                    (6)
                (sp(𝑃, if 𝐸 then 𝐶 1 else 𝐶 2 )) by (5), (6), and (7)           sp(𝑃, 𝐶) ≡ sp(𝑃, 𝐶 1 ; 𝐶 2 )                 (1)
                                                                        □                  ≡ sp(sp(𝑃, 𝐶 1 ), 𝐶 2 )       defn sp
Lemma 26. If ⊢ (𝑃) 𝐶 (𝑄) then 𝑄 ≡ sp(𝑃, 𝐶).                                                ≡ sp(𝑅, 𝐶 2 )                     (4)
Proof. By induction on the derivation ⊢ (𝑃) 𝐶 (𝑄):                                         ≡𝑄                              (5)
   EX-Skip: By inversion 𝐶 ≡ skip and 𝑄 ≡ 𝑃, and by def-                    EX-Exists:
       inition sp(𝑃, skip) ≡ 𝑃. Thus sp(𝑃, 𝐶) ≡ sp(𝑃, skip)                    (1) 𝑃 ≡ ∃𝑥 𝑃 ′ for some 𝑃 ′ by inversion
       ≡ 𝑃 ≡ 𝑄.                                                                (2) 𝑄 ≡ ∃𝑥 𝑄 ′ for some 𝑄 ′ by inversion
   EX-Assign:                                                                  (3) ⊢ (𝑃 ′ ) 𝐶 (𝑄 ′ ) by inversion
        (1) 𝐶 ≡ 𝑥 ≔ 𝐸 for some 𝑥, 𝐸 by inversion                               (4) 𝑥 ∉ fv(𝐶) by inversion
        (2) 𝑃 ≡ 𝑥 = 𝐸 ′ for some 𝐸 ′ by inversion                              (5) 𝑄 ′ ≡ sp(𝑃 ′, 𝐶) by induction using (3)
        (3) 𝑄 ≡ 𝑥 = 𝐸 [𝑥/𝐸 ′ ] by inversion
Gradual Exact Logic


         (6)                                                      That is, except for the vacuous case where 𝑃 ≡ ⊥, gradualizing
           sp(𝑃, 𝐶) ≡ sp(∃𝑥 𝑃 ′, 𝐶)                  (2)          the postcondition exactly characterizes deductions in Hoare
                                                                  logic.
                      ≡ ∃𝑥 sp(𝑃 ′, 𝐶)         Lemma 6
                      ≡ ∃𝑥 𝑄   ′
                                                     (5)          Proof. =⇒:
                    ≡𝑄                              (2)              (1) e⊢ (𝑃) 𝐶 (? ∧ 𝑄) by assumptino
                                                                     (2) ⊢ (𝑃) 𝐶 (𝑄 ′ ) for some 𝑄 ′ ∈ 𝛾 (? ∧ 𝑄) by (1)
      EX-Disj:
                                                                     (3) sp(𝑃, 𝐶) ≡ 𝑄 ′ by Lemma 26 using (2)
         (1) 𝑃 ≡ 𝑃1 ∨ 𝑃2 for some 𝑃1, 𝑃2 by inversion
                                                                     (4) 𝑄 ′ ⇒ 𝑄 by definition of 𝛾 and (2)
         (2) 𝑄 ≡ 𝑄 1 ∨ 𝑄 2 for some 𝑄 1, 𝑄 2 by inversion
                                                                     (5) sp(𝑃, 𝐶) ⇒ 𝑄 by (3) and (4)
         (3) ⊢ (𝑃1 ) 𝐶 (𝑄 1 ) by inversion
                                                                     (6) ⊢ {𝑃 } 𝐶 {𝑄 } by Lemma 18 using (5)
         (4) ⊢ (𝑃2 ) 𝐶 (𝑄 2 ) by inversion
         (5) 𝑄 1 ≡ sp(𝑃1, 𝐶) by induction using (3)                 ⇐=:
         (6) 𝑄 2 ≡ sp(𝑃2, 𝐶) by induction using (4)                  (1) ⊢ {𝑃 } 𝐶 {𝑄 } by assumption
         (7)                                                         (2) 𝑃 ∈ SatFormula by assumption
        sp(𝑃, 𝐶) ≡ sp(𝑃1 ∨ 𝑃2, 𝐶)                       (1)          (3) sp(𝑃, 𝐶) ⇒ 𝑄 by Lemma 16 using (1)
                                                                     (4) sp(𝑃, 𝐶) ∈ SatFormula by Lemma 5 using (2)
                  ≡ sp(𝑃1, 𝐶) ∨ sp(𝑃2, 𝐶)       Lemma 7              (5) sp(𝑃, 𝐶) ∈ 𝛾 (? ∧ 𝑄) by definition of 𝛾 using (3) and
                  ≡ 𝑄1 ∨ 𝑄2                        (5), (6)              (4)
                 ≡𝑄                                   (2)            (6) ⊢ (𝑃) 𝐶 (sp(𝑃, 𝐶)) by Lemma 25
      EX-Frame:                                                      (7) e⊢ (𝑃) 𝐶 (? ∧ 𝑄) by definition using (5) and (6)    □
         (1) 𝑃 ≡ 𝑃 ′ ∧ 𝑅 for some 𝑃 ′, 𝑅 by inversion             Theorem 6. If 𝑄 ∈ SatFormula,
         (2) 𝑄 ≡ 𝑄 ′ ∧ 𝑅 for some 𝑄 ′ by inversion                             e⊢ (? ∧ 𝑃) 𝐶 (𝑄) ⇐⇒ ⊢ [𝑃] 𝐶 [𝑄]
         (3) mod(𝐶) ∩ fv(𝑅) = ∅ by inversion
                                                                  That is, except in the vacuous case where 𝑄 ≡ ⊥, gradualizing
         (4) ⊢ (𝑃 ′ ) 𝐶 (𝑄 ′ ) by inversion
                                                                  the precondition exactly characterizes deductions in incorrect-
         (5) sp(𝑃 ′, 𝐶) ≡ 𝑄 by induction using (4)
                                                                  ness logic.
         (6) sp(𝑃 ′ ∧ 𝑅, 𝐶) ≡ 𝑅 ∧ sp(𝑃 ′, 𝐶) by Lemma 8 using
            (3)                                                   Proof. =⇒:
         (7)                                                         (1) e⊢ (? ∧ 𝑃) 𝐶 (𝑄) by assumption
             sp(𝑃, 𝐶) ≡ sp(𝑃 ′ ∧ 𝑅, 𝐶)           (1)                 (2) ⊢ (𝑃 ′ ) 𝐶 (𝑄) for some 𝑃 ′ ∈ 𝛾 (? ∧ 𝑃) by definition
                        ≡ 𝑅 ∧ sp(𝑃 ′, 𝐶)          (6)                    using (1)
                                   ′                                 (3) 𝑃 ′ ⇒ 𝑃 by definition of 𝛾 using (2)
                        ≡ 𝑅 ∧𝑄                    (5)
                                                                     (4) 𝑄 ≡ sp(𝑃 ′, 𝐶) by Lemma 26 using (2)
                        ≡𝑄                        (2)         □      (5) sp(𝑃 ′, 𝐶) ⇒ sp(𝑃, 𝐶) by Lemma 2 using (3)
                                                                     (6) 𝑄 ⇒ sp(𝑃, 𝐶) by (4) and (5)
Theorem 4. ⊢ (𝑃) 𝐶 (𝑄) ⇐⇒ 𝑄 ≡ sp(𝑃, 𝐶)
                                                                     (7) ⊢ [𝑃] 𝐶 [𝑄] by Theorem 2 using (6)
Proof. =⇒: Lemma 26; ⇐=: Lemma 25                             □     ⇐=:
                                                                     (1) ⊢ [𝑃] 𝐶 [𝑄] by assumption
E.2     Gradual exact logic
                                                                     (2) 𝑄 ∈ SatFormula by assumption
                                                 ⊢ (𝑃)
Valid triples in gradual exact logic are denoted e  e 𝐶 (𝑄).
                                                         e           (3) 𝑃 ∧ wp(𝐶, 𝑄) ∈ SatFormula by Lemma 24 using (1)
Definition 9. The concretization 𝛾 : e
                                     Formula →                           and (2)
P (Formula) maps a gradual formula to the set of all formu-          (4) 𝑃 ∧ wp(𝐶, 𝑄) ⇒ 𝑃 by logic
las it can represent:                                                (5) 𝑃 ∧ wp(𝐶, 𝑄) ∈ 𝛾 (? ∧ 𝑃) by definition of 𝛾 using (3)
                                                                         and (4)
              𝛾 (𝑃) ≔ {𝑃 }
                                                                     (6) 𝑄 ⇒ sp(𝑃, 𝐶) by Theorem 2 using (1)
           𝛾 (? ∧ 𝑃) ≔ {𝑃 ′ ∈ SatFormula | 𝑃 ′ ⇒ 𝑃 }                 (7) sp(𝑃 ∧ wp(𝐶, 𝑄), 𝐶) ≡ 𝑄 by Lemma 12 using (6)
Definition 10. Deductions in gradual exact logic directly            (8) ⊢ (𝑃 ∧ wp(𝐶, 𝑄)) 𝐶 (𝑄) by Theorem 4 using (7)
are lifted deductions in exact logic:                                (9) e⊢ (? ∧ 𝑃) 𝐶 (𝑄) by (5) and (8)                     □
                         def
              ⊢ (𝑃)
              e  e 𝐶 (𝑄)
                      e ⇐⇒   ⊢ (𝑃) 𝐶 (𝑄)
                  for some 𝑃 ∈ 𝛾 (𝑃)
                                  e and 𝑄 ∈ 𝛾 (𝑄)
                                               e

Theorem 5. For 𝑃 ∈ SatFormula,
         ⊢ (𝑃) 𝐶 (? ∧ 𝑄) ⇐⇒ ⊢ {𝑃 } 𝐶 {𝑄 }.
         e
