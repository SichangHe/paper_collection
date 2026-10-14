                                                STLSat—An Improved Tableau for Satisfiability
                                                  Checking of Signal Temporal Logic Formulas
                                         Marco Zamponi1               , Florian Lammel2 , Ezio Bartocci2         , and Michele Chiari2,3
                                                                  1
                                                                IMT Lucca, Lucca, Italy, name.surname@imtlucca.it
                                                              2
                                                               TU Wien, Vienna, Austria, name.surname@tuwien.ac.at
                                                  3
                                                    AIT Austrian Institute of Technology, Vienna, Austria, name.surname@ait.ac.at
arXiv:2607.21081v2 [cs.LO] 17 Sep 2026




                                                                                        Abstract
                                                   Signal Temporal Logic (STL) is a formalism used to describe temporal properties of
                                               real-valued signals in cyber-physical systems. In mission- and safety-critical domains, spec-
                                               ifications often consist of large collections of STL formulas, making consistency checking
                                               and requirement analysis a major engineering bottleneck. Tableau-based satisfiability pro-
                                               cedures are a natural way to address this problem. Two of the authors of this paper
                                               contributed to the only existing tree-shaped tableau for bounded discrete-time STL, but
                                               we have recently found out that the procedure can return incorrect verdicts for some STL
                                               formulas. In this paper, we pinpoint the flaw in that procedure and present a new tree-
                                               shaped tableau that we prove to be sound and complete for bounded discrete-time STL.
                                                   On top of this theoretical foundation, we introduce STLSat, an open-source Rust
                                               tool that decides the satisfiability of STL formulas, synthesizes concrete witness signals,
                                               and extracts unsatisfiable cores with its tableau engine, allowing users to identify incon-
                                               sistent subsets of requirements for more effective specification debugging. STLSat also
                                               implements enhanced first-order logic and satisfiability modulo theories encodings for STL,
                                               which allow it to act as a portfolio solver.
                                                   We evaluate STLSat on an extended benchmark suite (including STL and Mission-time
                                               Linear Temporal Logic formulas) that we release publicly. Across the whole benchmark, the
                                               portfolio solver matches or outperforms state-of-the-art tools while preserving correctness.


                                         1    Introduction
                                         Signal Temporal Logic (STL) [30] is a well-established specification language for describing the
                                         temporal properties of real-valued signals in mission- and safety-critical cyber-physical systems
                                         (CPS). STL underpins a broad spectrum of verification tasks, ranging from runtime monitor-
                                         ing [25] and mutation testing [9] to falsification [38], parameter synthesis [4], fault localization [6]
                                         and debugging [7]. During the design of a CPS, engineers typically collect a large number of
                                         STL requirements. In this context, the following two situations can be problematic:
                                         Inconsistency. A set of STL Vn formulas Φ = {φ1 , . . . , φn } is consistent
                                                                                                                Vn iff there exists at least
                                         one signal s such that s |= i=1 φi . Equivalently, the conjunction i=1 φi must be satisfiable;
                                         if it is not, the requirements are mutually contradictory.
                                         Redundancy. A formula ψ ∈ ΦVis redundant w.r.t. the remaining requirements iff those
                                         requirements already entail ψ, i.e., φ∈Φ\{ψ} |=E ψ. By definition, this holds exactly when the
                                         formula       φ∈Φ\{ψ} ∧ ¬ψ is unsatisfiable.
                                                    V          

                                              Moreover, manual analysis of large CPS requirement sets is error-prone and demanding in
                                         terms of time, expertise, and cognitive effort, especially when expressed in a formal language
                                         such as STL. Thus, automated requirement engineering tools are highly desirable to support
                                         engineers in these tasks. Luckily, both notions of consistency and redundancy can be reduced to
                                         a single STL-satisfiability query: for any pair of formulas φ, ψ, the implication φ → ψ holds iff
STLSat                                                           Zamponi, Lammel, Bartocci and Chiari


φ ∧ ¬ψ is unsatisfiable, and equivalence follows from mutual implication. Hence, in this paper
we tackle the problem of checking STL satisfiability.
     These reductions are especially valuable in specification mining [8], where automatically ex-
tracted temporal-logic specifications may contain noise, redundancies, or inconsistencies. Sat-
isfiability checking can detect inconsistent subsets, eliminate redundancies, and cluster seman-
tically equivalent specifications, yielding a more concise and traceable requirement model.
Example. Consider an autonomous crop-irrigation controller whose water-flow signal f is
measured along the irrigation line. The following three STL requirements have been elicited:

                         φ1 := G[0,100] F[10,40] (f ≥ 50)
                                                                           
                         φ2 := G[0,120] f ≥ 50 ⇒ F[0,10] G[0,30] (f < 5)
                         φ3 := G[0,120] (f < 100)

    • φ1 requires that, at every time in [0, 100], the flow reaches at least 50 l/min within the
      following 10–40 time units.
    • φ2 states that whenever the flow reaches this irrigation value, it must be reduced below
      5 l/min within the next 10 time units and stay low for another 30 time units, in order to
      avoid over-watering.
    • φ3 is a safety bound that forbids flows equal to or above 100 l/min at any time in the
      interval 0-120 units, preventing flooding of the field.
    The three formulas together form the specification Φw = {φ1 , φ2 , φ3 }. Before Φw can be
used for modelV3 checking or falsification, we must verify that it is consistent, i.e. that the
conjunction i=1 φi is satisfiable. Intuitively, φ2 forces a drop from f ≥ 50 to f < 5, which
might conflict with φ1 ; however, turning this intuition into a rigorous proof requires exploring
all possible signal behaviors over [0, 140]. Manual reasoning is error-prone, whereas automated
STL satisfiability tools decide consistency in seconds; if the set is satisfiable they may synthesize
a concrete witness signal, and if it is unsatisfiable they may extract an unsatisfiable core that
pinpoints the conflicting requirements, enabling their immediate refinement.
    Although STL has become the de facto standard specification language for CPS require-
ments, it is still lacking mature, high-performance, and dedicated satisfiability solvers. Existing
approaches either target different logics—e.g., MLTLSAT [28]—or exist only as research proto-
types such as the tableau implementation described in Melani et al. [31]. Moreover, these tools
do not integrate smoothly into verification pipelines, which limits their usefulness for practical
requirement-engineering workflows that require automated debugging and traceability.
    The most prominent tableau-based solver for bounded discrete-time STL is STLTree [31],
also co-developed by two of the authors of this paper. Its construction accelerates reasoning by
“jumping” over intervals, but a careful analysis reveals a soundness flaw: in formulas with nested
temporal operators, the old jump rules may skip instants where conflicts would be introduced,
causing the tableau to miss rejecting branches. Consider the following unsatisfiable formula:
                                                          
                                 φS := G[0,5] p ∨ G[2,2] p ∧ G[3,5] q,

where p and q are inconsistent atomic predicates, for example p = x ≥ 0 and q = x < 0. At
time 3, the second conjunct requires q; hence, the first conjunct cannot be satisfied by choosing
p and instead generates the obligation G[5,5] p. The second conjunct also requires q at time
5, making φS unsatisfiable. However, STLTree jumps from time 3 to time 5 and incorrectly
shifts the obligation from G[5,5] p to G[7,7] p. The resulting tableau avoids the conflict between
p and q at time 5 and accepts φS with a signal that is not actually a model of φS .

2
STLSat                                                         Zamponi, Lammel, Bartocci and Chiari


    This motivates our first contribution: a corrected tableau algorithm with formally proved
soundness and completeness. Our approach inspects proposition-appearance intervals to guar-
antee that no conflicts can be introduced in skipped time steps.
    Building on this foundation we introduce STLSat, an open-source Rust tool implementing
three complementary decision procedures that can be executed in parallel to speed up the
solving process: our correct tableau, an optimized first-order-logic encoding, and a qualitative-
semantics SMT encoding. The tableau supports unsatisfiable-core extraction for debugging,
and can synthesize witness signals for satisfiable formulas by extracting them from the tableau.
To foster reproducibility, we also release an extensive STL benchmark suite [40].
    STLSat determines in under one second that the φ1 –φ3 irrigation requirements are mutu-
ally inconsistent and the tableau engine also returns the subset of constraints {φ1 , φ2 } respon-
sible for the conflict as an unsatisfiable core, thus providing immediate debugging support.
    We conduct an extensive empirical evaluation on the released benchmark set of STL for-
mulas, as well as its close relative MLTL coming from related works, comparing each STL-
Sat engine against state-of-the-art STL solvers and against a dedicated MLTL satisfiability
checker [28]. The results show that no single technique dominates across all instances; however,
the portfolio approach combining the three STLSat solving engines achieves the best overall
performance in terms of runtime and scalability.
In summary, our contributions are:
   1. a sound and complete tree-shaped tableau algorithm with a novel set of rules;
   2. STLSat, a high-performance Rust portfolio solver with tableau, FOL, and SMT engines;
   3. a novel unsat-core extraction method for the tableau engine;
   4. an open benchmark suite covering STL formulas; and
   5. a thorough experimental study demonstrating superior performance over existing tools.
    The remainder of the paper is organized as follows. Section 2 surveys related work on
temporal logic satisfiability. Section 3 recalls the syntax and semantics of STL and MLTL. Sec-
tion 4 details the flaws in the existing tableau [31] and presents our corrected tableau algorithm
together with its soundness and completeness proofs. Section 5 details the implementation of
STLSat’s three solving engines. Section 6 describes our experimental methodology and reports
the results. Finally, Section 7 draws conclusions and outlines future research directions.


2    Related Work
Originally proposed for CPS monitoring and testing [30], STL has primarily been studied for
runtime verification [5], while consistency checking, redundancy removal, and implication anal-
ysis remain less explored.
Validity, vacuity, and redundancy. These issues were firstly addressed by Dokhanchi et al.
[19], who reduced validity, vacuity, and redundancy questions for STL to satisfiability problems
in Metric Interval Temporal Logic (MITL) [1]. Their approach leverages existing MITL solvers
[10] to obtain counterexamples or proofs of equivalence. While effective, this pipeline incurs the
overhead of translating STL into a different logic and does not directly support the extraction
of minimal conflicting subsets.
Debugging tools. In the same spirit, Roehm et al. [37] proposed STLInspector, a debugging
aid that generates concrete witness signals by mutating candidate models and querying an SMT
encoding of the STL formula. The tool is useful for pinpointing why a specification holds or
fails on a given trace, but it does not provide a systematic analysis of the logical relationships
among multiple requirements.

                                                                                                 3
STLSat                                                                 Zamponi, Lammel, Bartocci and Chiari


Satisfiability/Model checking. The close relationship between satisfiability and bounded
model checking has motivated several encodings of STL into first-order logic (FOL) or Sat-
isfiability Modulo Theories (SMT). Bae and Lee [3] presented a refutationally complete SMT
encoding for bounded model checking of continuous-time STL against hybrid system models; an
improved variant was later shown to be suitable for satisfiability checking [27]. For discrete-time
settings, Raman et al. [34] introduced an SMT formulation aimed at model predictive control
that can also serve as a decision procedure for STL satisfiability [31].
Tableau-based approaches. The only dedicated tableau method for bounded discrete-time
STL prior to our work is the one-pass tree-shaped construction proposed by Melani et al. [31].
They proved that STL satisfiability is EXPSPACE-complete and implemented their algorithm,
inspired by tableau techniques for other temporal logics [36, 21], in a prototype Python tool.
In the course of our investigation we discovered a soundness flaw in their original jump opti-
mization; we therefore revisited the mathematical definition, and proved both soundness and
completeness for the corrected rule.
Related temporal logics. Several works have studied satisfiability for logics closely related
to STL. Bersani et al. [11, 12] offered SMT encodings for MITL and Quantified Temporal Logic
(QTL) [23], but these frameworks admit only Boolean signals, limiting their applicability to
the quantitative nature of STL. Mission-time Linear Temporal Logic (MLTL) [35] shares many
syntactic constructs with STL; a systematic comparison of encodings for MLTL—including
translations to LTL on finite traces, SMV specifications, and FOL—was carried out by Li
et al. [29], who identified the FOL encoding as the best performing. Our tool incorporates an
improved version of this FOL translation and demonstrates better empirical performance on
both STL and MLTL benchmarks.
Unsatisfiable-core extraction. The extraction of minimal unsatisfiable cores has been ex-
tensively investigated for propositional SAT and SMT solving [14]. Within temporal logics,
similar techniques have been explored mainly for Linear Temporal Logic (LTL) [39, 22], but
to the best of our knowledge no existing framework provides unsat-core extraction for STL
formulas. By integrating a dedicated core extraction mechanism into our tableau engine we fill
this gap and enable direct debugging of inconsistent requirement sets.


3     Background
Signal Temporal Logic (STL). We define bounded discrete-time STL [30] on the temporal
domain of natural numbers N. A signal is a function w : N → Rn that associates time instants
with valuations of a finite set of signal variables S = {x1 , . . . , xn }. We define the projection wR
of a signal w on a set R ⊆ S in the usual way. STL formulas have the following syntax:
                             φ := ⊤ | f (R) ▷◁ k | ¬φ | φ1 ∨ φ2 | φ1 UI φ2
where ▷◁ ∈ {<, =, >}, R ⊆ S is a set of signal variables, f : R|R| → R is a linear function of
signal values, k ∈ Q is a rational constant, and I = [a, b] with a, b ∈ N and a ≤ b.
    We define the semantics on a signal w and a time instant t ∈ N as follows:
    (w, t) |= ⊤                   (always true)
    (w, t) |= f (R) ▷◁ k      iff f (wR (t)) ▷◁ k, with ▷◁ ∈ {<, =, >}
    (w, t) |= ¬φ              iff (w, t) ̸|= φ
    (w, t) |= φ1 ∨ φ2         iff (w, t) |= φ1 or (w, t) |= φ2
    (w, t) |= φ1 U[a,b] φ2    iff ∃t′ ∈ [t + a, t + b] : (w, t′ ) |= φ2 and ∀t′′ ∈ [t, t′ ] : (w, t′′ ) |= φ1


4
STLSat                                                                 Zamponi, Lammel, Bartocci and Chiari


Boolean signals can be encoded by defining a real variable xp for each atomic proposition p,
and asserting p as xp = 1 and ¬p as xp ̸= 1.
   We also use propositional operators (∧, →), and temporal operators eventually (or finally) FI
and always (or globally) GI as shortcuts for FI φ ≡ ⊤ UI φ and GI φ ≡ ¬ FI ¬φ. We also employ
the release operator R, defined as the dual of until under negation, i.e., φ1 RI φ2 ≡ ¬(¬φ1 UI ¬φ2 ).
Given φ1 UI φ2 and φ2 RI φ1 , we refer to φ1 as the invariant, and to φ2 as the target.

Mission-Time Linear Temporal Logic (MLTL). MLTL [35] can be seen as a fragment
of bounded discrete-time STL that only allows for Boolean signals. It also differs from STL in
the semantics of the until operator, which we denote as strict until (sU) for MLTL:

(w, t) |= φ1 sU[a,b] φ2 iff ∃t′ ∈ [t + a, t + b] : (w, t′ ) |= φ2 and ∀t′′ ∈ [t + a, t′ − 1] : (w, t′′ ) |= φ1

The strict release operator is defined as φ1 sRI φ2 ≡ ¬(¬φ1 sUI ¬φ2 ).
   Indeed, MLTL’s until operator is expressible in terms of STL’s, and vice versa:
                                                                                             
φ1 sU[a,b] φ2 ≡ F[a,a] (φ1 ∨ φ2 ) U[0,b−a] φ2   φ1 sR[a,b] φ2 ≡ F[a,a] (φ1 ∧ φ2 ) R[0,b−a] φ2
φ1 U[a,b] φ2 ≡ G[0,a] φ1 ∧ φ1 sU[a,b] (φ1 ∧ φ2 )       φ1 R[a,b] φ2 ≡ F[0,a] φ1 ∨ φ2 sU[a,b] φ1 ∨ G[a,b] φ2

The equivalences in the second row, together with common propositional and temporal logic
equivalences, allow for rewriting all STL formulas in strict normal form, i.e., by using only
strict operators in positive form, with negation only applied to atomic propositions.


4     Tree-Shaped Tableau
Building upon the tree-shaped tableau introduced in [31], we propose an alternative definition
of the JUMP rule, an optimization that skips sequences of redundant time steps during tableau
exploration while fixing the soundness and completeness problems of the original rule.
    We begin by reviewing the original basic tableau, i.e., without the JUMP rule, whose sound-
ness and completeness results still hold. We then introduce the new JUMP rule and, finally,
present its correctness theorems.


4.1    Basic Tableau
A tableau is a tree in which each node u is labeled with a set of formula occurrences Γ(u)
required to hold conjunctively, and a time counter t(u) ∈ N. The root u0 is labeled with the
formula ϕ to be checked, assumed to be in strict normal form. Besides a formula, elements of
Γ(u) may carry auxiliary metadata recording the temporal formula occurrence that generated
them—i.e., their parent. We write ⟨φ⟩ψ for the occurrence whose underlying formula is φ and
whose parent occurrence is ψ, and ⟨φ⟩⊥ when no parent is present (e.g., for operators in the
input formula). For instance, in ⟨a⟩GI a , the occurrence GI a is the parent of a, meaning that
unfolding it generated that occurrence of a. Parent annotations are only needed by the JUMP
rule, hence we omit them whenever not strictly relevant, and we identify occurrences in Γ(u)
by their underlying formula.
    The tableau is built incrementally by applying the expansion rules in Table 1, which decom-
pose formulas in a node’s label into simpler ones according to their semantics generating child
nodes. Decomposing temporal operators introduces marked operators denoted by a bar (e.g.,

                                                                                                             5
STLSat                                                                              Zamponi, Lammel, Bartocci and Chiari


Table 1: Expansion rules. A node u with ϕ ∈ Γ(u) that satisfies the condition is expanded into
one child up or two children us and up such that t(us ) = t(up ) = t(u), Γ(us ) = (Γ(u) \ {ϕ}) ∪
Γϕ (us ) and Γ(up ) = (Γ(u) \ {ϕ}) ∪ Γϕ (up ).

    Cat.        ϕ ∈ Γ(u)              condition      Γϕ (us )                              Γϕ (up )
                ⟨φ1 ∨ φ2 ⟩ψ                          ⟨φ1 ⟩ψ                                ⟨φ2 ⟩ψ
    Prop.
                ⟨φ1 ∧ φ2 ⟩ψ                          ⟨φ1 ⟩ψ , ⟨φ2 ⟩ψ

                ⟨F[a,b] φ⟩ψ           a ≤ t(u) < b   ⟨text(u) (φ)⟩⊥                        ⟨F[a,b] φ⟩ψ
                                      t(u) = b       ⟨text(u) (φ)⟩⊥
     Temporal




                ⟨G[a,b] φ⟩ψ           a ≤ t(u) < b                                         ⟨G[a,b] φ⟩ψ , ⟨text(u) (φ)⟩ϕ
                                      t(u) = b                                             ⟨text(u) (φ)⟩ϕ

                ⟨φ1 sU[a,b] φ2 ⟩ψ     a ≤ t(u) < b   ⟨text(u) (φ2 )⟩⊥                      ⟨φ1 sU[a,b] φ2 ⟩ψ , ⟨text(u) (φ1 )⟩ϕ
                                      t(u) = b       ⟨text(u) (φ2 )⟩⊥

                ⟨φ1 sR[a,b] φ2 ⟩ψ     a ≤ t(u) < b   ⟨text(u) (φ1 )⟩⊥ , ⟨text(u) (φ2 )⟩⊥   ⟨φ1 sR[a,b] φ2 ⟩ψ , ⟨text(u) (φ2 )⟩ϕ
                                      t(u) = b                                             ⟨text(u) (φ2 )⟩ϕ



F), which represent operators whose satisfaction is postponed to the next time step. Further-
more, temporal operator decomposition employs a temporal expansion function text mapping
formulas inside nested temporal operators to their realizations when unfolded at time t.
    which updates intervals when nested temporal operators are unfolded:

                   text (⊤) = ⊤            text (f (R) ▷◁ k) = f (R) ▷◁ k           text (¬φ1 ) = ¬ text (φ1 )
                              text (φ1 ◦ φ2 ) = text (φ1 ) ◦ text (φ2 )           with ◦ ∈ {∧, ∨}
                                 t
                              tex (A[a,b] φ) = A[a+t,b+t] φ                       with A ∈ {F, G}
                                 t
                              tex (φ1 B[a,b] φ2 ) = φ1 B[a+t,b+t] φ2              with B ∈ {sU, sR}.

    During tableau construction, nodes are checked for local inconsistencies. Formally, a node
u is rejected (and closed) if either ¬⊤ ∈ Γ(u) or the set of propositions {f (R) ▷◁ k ∈ Γ(u)} ∪
{¬(f (R) ▷◁ k) ∈ Γ(u)} is inconsistent. Rejected nodes are leaves.
    When no further decomposition rule is applicable to a node, i.e., all temporal operators
in its label are marked or not active, the node is said to be poised. In this case, the tableau
advances time through the STEP rule:

STEP Let u be a poised node. If Γ(u) contains any temporal operators, then u has one child
    u′ with t(u′ ) = t(u) + 1, and

                        Γ(u′ ) = {AI φ ∈ Γ(u) | A ∈ {F, G}} ∪ {φ1 BI φ2 ∈ Γ(u) | B ∈ {sU, sR}}
                                     ∪ {A[a,b] φ | A[a,b] φ ∈ Γ(u) ∧ A ∈ {F, G} ∧ t(u) < b}
                                     ∪ {φ1 B[a,b] φ2 | φ1 B[a,b] φ2 ∈ Γ(u) ∧ B ∈ {sU, sR} ∧ t(u) < b}

    If u is poised, not rejected, and its STEP successor label is empty, then the corresponding
branch is accepted and witnesses the satisfiability of the input formula. If the tableau frontier
consists of only rejected nodes, the input formula is unsatisfiable.
    Fig. 1 shows an example of the basic tableau for formula G[0,4] a ∧ b sU[4,7] ¬a. The tableau
starts with the expansion rule for the ∧ operator, and proceeds with the one for the G operator,
which creates a marked instance of G[0,4] a and extracts its argument a. The interval of the sU

6
STLSat                                                                                   Zamponi, Lammel, Bartocci and Chiari

                                                                                        
                                                                u0 : G[0,5] p ∨ G[2,2] p ∧ G[3,5] q | 0
                                                                                   ...
      u0 : G[0,4] a ∧ b sU[4,7] ¬a | 0
                                                                                      [0,5]
                    ∧                                  u1 : G[0,5] p ∨ G[2,2] p , p ∨ G[5,5] p, G[3,5] q | 3
      u1 : G[0,4] a, b sU[4,7] ¬a | 0                                           G, G
                    G                                                                [0,5]
                                                      u2 : G[0,5] p ∨ G[2,2] p , p ∨ G[5,5] p, G[3,5] q, q | 3
    u2 : G[0,4] a, a, b sU[4,7] ¬a | 0
                                                                            ∨              ∨
                STEP                                                                                                 [0,5]
      u3 : G[0,4] a, b sU[4,7] ¬a | 1              u3 : . . . , p, q | 3        u4 : G[0,5] p ∨ G[2,2] p , G[3,5] q, G[5,5] p, q | 3

                     ...                                    ✗                                          JUMP
      u4 : G[0,4] a, b sU[4,7] ¬a | 4                                                                                 [0,5]
                                                                                 u5 : G[0,5] p ∨ G[2,2] p , G[3,5] q, G[7,7] p | 5
                    G
                                                                                                         G, G
           u5 : a, b sU[4,7] ¬a | 4                                                                     [0,5]             [0,5]
                                                                                          u6 :     p ∨ G[7,7] p,   q, G[7,7] p | 5
                     sU
                                                                                                          ∨        ∨
u6 : a, ¬a | 4          u7 : a, b sU[4,7] ¬a, b | 4
                                                                                                                                   [0,5]
       ✗                       STEP                                                u7 : . . . , p, q | 5           u8 : q, G[7,7] p | 5
                           u8 : b sU[4,7] ¬a | 5                                               ✗                        JUMP
                                  sU                                                                                              [0,5]
                                                                                                                       u9 : G[7,7] p | 7
              ✓ u9 : ¬a | 5           u10 : b sU[4,7] ¬a, b | 5
                                                                                                                             G

                                                                                                                   ✓ u10 : p | 7

Figure 1: Basic tableau for G[0,4] a ∧ b sU[4,7] ¬a.                       Figure 2: STLTree tableau for φS .



operator starts at 4, so no more expansion rules can be applied and u2 is poised, and the STEP
rule advances time by creating node u3 . This process goes on until time 4, creating many nodes
identical to u1 and u2 , which we omit from the figure. At time 4, the sU operator is expanded,
creating two nodes us = u6 and up = u7 . In u6 , we try to satisfy it by extracting ¬a, which
conflicts with a extracted by the G operator and leads to a rejected node. In u7 , we postpone
the satisfaction of the sU operator by marking it and extracting b, which does not conflict with
any other proposition. Since G[0,4] a ends at time 4, the step rule does not propagate it to u8 .
Thus, the sU can finally be satisfied in u9 . Since u9 has no temporal operators and no conflicts
between atomic propositions, it is accepted, witnessing the satisfiability of the input formula.
    Soundness and completeness of the basic tableau were established in [31]:
Theorem 1 ([31, Theorem 4.4 and Lemma 3]). A formula φ is satisfiable iff the basic tableau
rooted in it has an accepting branch.


4.2      The JUMPOld rule and its unsoundness
As an optimization to the basic tableau, Melani et al. [31] introduced the JUMPOld rule to skip
repetitive parts of the tableau by jumping directly to a later point in time. For instance, for
formula G[0,20] x > 0 ∧ F[0,5] x > 5, the tableau need not explore every time instant, as checking
consistency only at interval bounds 0, 5, and 20 is sufficient to determine satisfiability. Formulas
with nested operators are trickier: the tableau by [31] waits until the end of the time interval of

                                                                                                                                           7
STLSat                                                               Zamponi, Lammel, Bartocci and Chiari


the first extracted instance of the inner operator. For instance, with formula G[5,20] F[0,5] x > 0,
the tableau proceeds with the STEP rule until time 5 + 5 = 10, after which it may jump to time
20.
    We found out, however, that this precaution is not enough to preserve the soundness of the
tableau. As we mentioned in §1, formula φS witnesses this flaw. Fig. 2 shows part of the tableau
rooted in φS that uses the JUMPOld rule. The figure omits the prefix up to time 3, in which
the first conjunct is satisfied by choosing p and the STEP rule is applied. At time 3, expanding
                                                                  [0,5]
the two outer G operators produces q and the disjunction p ∨ G[5,5] p (here, the superscript [0, 5]
indicates that the formula is extracted from an operator with interval [0, 5]). The branch that
                                                                                             [0,5]
chooses p is locally inconsistent with q and is rejected. The other branch chooses G[5,5] p.
    Since its current time is greater than 0 + 2 = 2, the poised node u4 satisfies the conditions of
                                                                                 [0,5]
the JUMPOld rule, which jumps from time 3 to time 5. Since the parent of G[5,5] p is still active
at time 3, the rule treats this formula as a derived obligation and shifts both interval bounds by
                                                   [0,5]                               [0,5]
the jump length 2. Consequently, u6 contains G[7,7] p instead of the required G[5,5] p. At time
5, the first conjunct can again select its nested G disjunct, which yields the same obligation at
time 7; after q expires, the tableau satisfies p at time 7 and accepts the branch. The branch
therefore never checks the inconsistent pair p, q at time 5.
    The JUMPOld rule compromises both soundness and completeness of the tableau. We de-
scribe this flaw in more detail in Appendix A.

4.3    A new, correct JUMP rule
To speed up tableau construction, we introduce the JUMP rule, which can be used to compress
a sequence of STEP rule applications. Intuitively, a jump from a poised node u to a node u′ has
the same effect as postponing all active temporal operators until time t(u′ ) by always choosing
the expansion rule Γϕ (up ).
    To describe the JUMP rule, we introduce new notation, then discuss the jump-size com-
putation, and finally describe the resulting node. To simplify notation, we omit the G and F
operators, which we replace by the standard equivalences GI φ ≡ ¬⊤ sRI φ and FI φ ≡ ⊤ sUI φ.
    The JUMP rule needs parent annotations, which are created by expansion rules. When the
JUMP rule is enabled, the STEP rule propagates parent annotations on all formulas that it
inserts in the new node. They are accessed through the parent-active predicate P , which we
define over a formula occurrence and a node as follows:

             P (ϕ, u)    iff   ϕ = ⟨φ⟩ψ for some φ, ψ ∈ Γ(u) s.t. ψ ̸= ⊥ and ψ ∈ Γ(u).

Proposition Validity Intervals. We define the proposition validity intervals T (φ) of a
formula φ as the time intervals in which its atomic propositions may appear, allowing us to
identify potential conflicts. Formally:

                        T (f (R) ▷◁ k) = T (⊤) = {(0, 0)}         T (¬φ) = T (φ)
                        T (φ1 ◦ φ2 ) = T (φ1 ) ∪ T (φ2 )          with ◦ ∈ {∧, ∨}
         T (φ1 sU[a,b] φ2 ) = T (φ1 sR[a,b] φ2 ) = {(l + a, r + b − 1) | (l, r) ∈ T (φ1 ), a < b}
                                                   ∪ {(l + a, r + b) | (l, r) ∈ T (φ2 )}

    To distinguish different occurrences of the same proposition, we associate a unique identifier
to every occurrence. For instance, in φ = p sU[0,5] q ∧ p sU[0,10] r, the two occurrences of p are

8
STLSat                                                           Zamponi, Lammel, Bartocci and Chiari


treated as distinct because they are governed by different temporal constraints. Formally, the
formula is viewed as a syntax tree whose leaves carry unique identifiers. Two propositions are
considered the same only if they share the same syntactic structure and identifier. Identifiers
are preserved by expansion rules and by the temporal expansion operator tex. Such identifiers
are used only for validity intervals: for local consistency checking, propositions are compared
solely based on their syntactic structure.
    Function T is defined so that each occurrence of an atomic proposition ρ in a formula
contributes exactly one pair (l, r). Hence, we may unambiguously refer to a pair i = (l, r) ∈
T (φ) deriving from ρ, meaning the specific occurrence identified via its identifier rather than
merely its syntactic structure. We denote as id(i) such an identifier.
    The following lemma, whose proof is in Appendix B, relates validity intervals computed
from a formula φ to the time instants at which occurrences of a proposition produced by
decompositions of φ may appear in the tableau:
Lemma 2. Let u be a node of the basic tableau, φ ∈ Γ(u) be a formula in the label of the node,
and ρ be an atomic proposition appearing in φ. Let (l, r) ∈ T (φ) be the proposition validity
interval deriving from ρ. Then, in the subtree rooted at u, any occurrence of ρ derived from
the expansion of φ can only appear in nodes v such that l ≤ t(v) ≤ r if ρ is nested within a
temporal operator in φ, and such that t(v) = t(u) otherwise.

4.3.1    Jump Size Calculation
To guarantee that the JUMP rule preserves the correctness of the algorithm, we compute the
jump size k ∗ as the minimum of two bounds.

Bounds Limit (k) The first limit ensures that the jump does not cross a time instant at
which an operator becomes active or expires. It is defined as

                             k(u) = min{t ∈ K(u) | t > t(u)} − t(u),

where the set K(u) collects bounds of temporal operators in u:

                     K(u) = {a, b | φ1 B[a,b] φ2 ∈ Γ(u), B ∈ {sU, sU, sR, sR}}

   We illustrate the computation of the bounds on node u2 from the tableau in Fig. 1. We
have K(u2 ) = {0, 4, 7}, and thus k(u2 ) = 4.

Soundness Limit (ksound∗
                             ) Consider a temporal operator φ = φ1 sU[a,b] φ2 or φ = φ2 sR[a,b] φ1
in a poised node u. The basic tableau would emit the invariant part φ1 at every intermediate
time instant t(u)+j, with 1 ≤ j < k, before reaching the jump destination t(u)+k. To guarantee
the soundness of the approach, we need to be sure that such invariants do not generate conflicts
with other formulas in the node.
    We first collect the validity intervals of atomic propositions that may be generated by the
invariant part of active postponed temporal operators:
              [
    N (u) =        {(t(u) + l, t(u) + r) | (l, r) ∈ T (φ1 ), φ = φ1 sU[a,b] φ2 ∨ φ = φ2 sR[a,b] φ1 }.
            φ∈Γ(u)

An element (ln , rn ) ∈ N (u) describes the validity interval of an invariant emitted at time instant
t(u) by an active temporal operator φ, i.e., text(u) (φ1 ). If the same invariant is emitted at a
skipped time t(u) + j, its interval is shifted to (ln + j, rn + j).

                                                                                                   9
STLSat                                                             Zamponi, Lammel, Bartocci and Chiari


   We then collect the validity intervals of atomic propositions that may be generated by
temporal operators in Γ(u) whose parent is not active:
               [
     O(u) =        {(l, r) | (l, r) ∈ T (φ), φ = φ1 B[a,b] φ2 , B ∈ {sU, sU, sR, sR}, ¬P (φ, u)}
               φ∈Γ(u)


   If an interval in N (u) intersects one in O(u), we cannot exclude that the skipped invariant
conflicts with other formulas. Since we do not know which propositions will eventually form an
inconsistent core, we perform a STEP as a safe choice: the JUMP rule is disabled whenever

                        ∃(n, o) ∈ N (u) × O(u) s.t. id(n) ̸= id(o) ∧ n ∩ o ̸= ∅                      (1)

    If no intersection exists, for every n = (ln , rn ) ∈ N (u) and o = (lo , ro ) ∈ O(u), either rn < lo
or ro < ln . The case ro < ln is always safe: delaying the emitted invariants moves the interval
to the future, so other proposition intervals will never intersect with it. In case rn < lo instead,
shifting the invariant to the future might cause the intersection of the intervals. We define the
sound jump limit as the earliest distance at which propositions may appear together:
        ∗
             (u) = min {lo − rn | (n, o) ∈ N (u) × O(u) ∧ id(n) ̸= id(o) ∧ rn < lo } ∪ {+∞}
                                                                                                   
      ksound

   Let us evaluate the soundness bounds on node u2 in Fig. 1: we have N (u2 ) = {(0, 0)} and
O(u2 ) = {(0, 4), (4, 6), (4, 7)}, hence ksound
                                          ∗
                                                (u2 ) = 4.

Completeness Guard Consider a temporal operator φ = φ1 sU[a,b] φ2 or φ = φ2 sR[a,b] φ1 in
a poised node u. The JUMP rule reconstructs the branch in which this temporal obligation is
postponed until the jump destination t(u) + k. In the basic tableau, an accepting branch may
satisfy the temporal obligation (i.e., select the Γφ (us ) expansion rule) at some intermediate
time t(u) + j, with 1 ≤ j < k. If time step t(u) + j is skipped, the JUMP rule may reach a
node rejected due to the postponed obligation, even though the basic tableau had an accepting
branch rooted at t(u) + j.
    We first collect the validity intervals of atomic propositions that may be generated by the
target (i.e., φ2 ) part of active temporal operators:
               [
    M (u) =          {(t(u) + l, t(u) + r) | (l, r) ∈ T (φ2 ), φ = φ1 sU[a,b] φ2 ∨ φ = φ2 sR[a,b] φ1 }.
             φ∈Γ(u)


An element (lm , rm ) ∈ M (u) describes the validity interval of a proposition generated by the
formula emitted at time t(u), namely text(u) (φ2 ). If the same target is emitted at some time
t(u) + j with 1 ≤ j < k, its interval is shifted to (lm + j, rm + j).
   We then collect the validity intervals of propositions that may generate conflicts with a target
extraction. These consist of propositions already present in the node and the ones generated
by non-expired temporal operators without an active parent:

     S(u) = O(u) ∪ {(t(u), t(u)) | φ ∈ Γ(u), φ = f (R) ▷◁ k ∨ φ = ¬(f (R) ▷◁ k), ¬P (φ, u)}.

   If an interval in M (u) intersects one in S(u), then we cannot determine when the invariant
stops conflicting with the target. Since the extraction might be satisfiable at the next instant,
we perform a STEP, and disable the JUMP rule whenever:

                        ∃m ∈ M (u), ∃s ∈ S(u) s.t. id(m) ̸= id(s) ∧ m ∩ s ̸= ∅                       (2)

10
STLSat                                                           Zamponi, Lammel, Bartocci and Chiari


    If no such intersection exists, then for every m = (lm , rm ) ∈ M (u) and s = (ls , rs ) ∈ S(u),
either rm < ls or rs < lm . Case rs < lm is safe, as the potentially conflicting interval is before
the target one, and delaying extraction would move the latter to the future. Otherwise, when
rm < ls , extracting the target at a later time can cause the two intervals to intersect, leading
to a possible conflict. However, if the JUMP rule is enabled, then no two intervals m and s
intersect, and all currently active temporal formulas can be satisfied by extracting their targets
at the current time. Thus, there is no need for a jump limit to ensure completeness.
    In the running example of Fig. 1, we have M (u2 ) = {(0, 0)} and S(u2 ) = {(0, 4), (4, 7)}.
Note that proposition a has been extracted from the active operator G[0,4] a, so it is marked
with ⟨a⟩G[0,4] a , and its validity interval is excluded from S(u2 ).

4.3.2    Rule Application
Let u be a poised node in which (1) and (2) do not hold. The JUMP rule creates one child u′
with t(u′ ) = t(u) + k ∗ (u), where the jump size k ∗ (u) and node label Γ(u′ ) are defined as
                                   k ∗ (u) = min(k(u), ksound
                                                        ∗
                                                              (u))
         Γ(u′ ) = {⟨φ1 sU[a,b] φ2 ⟩ψ | ⟨φ1 B[a,b] φ2 ⟩ψ ∈ Γ(u), B ∈ {sU, sU}, t(u′ ) ≤ b}
                   ∪ {⟨φ1 sR[a,b] φ2 ⟩ψ | ⟨φ1 B[a,b] φ2 ⟩ψ ∈ Γ(u), B ∈ {sR, sR}, t(u′ ) ≤ b}
    The label Γ(u′ ) omits real-valued constraints and unmarks operators, so that expansion
rules can build nodes for the next time instants. The bound ksound
                                                                 ∗
                                                                       (u) guarantees that the
JUMP rule preserves remaining temporal obligations while avoiding redundant checks.
    Finally, we can evaluate the JUMP bounds on node u2 of Fig. 1. We have k(u2 ) = 4 and
 ∗
ksound (u2 ) = 4; hence, the JUMP rule can be applied with a jump size of 4, skipping time
instants 1 to 3. With the JUMP rule, node u4 is the (only) child of u2 .

Shared-Variable Optimization For a set of atomic constraints to be inconsistent, at least
two of them have to share a variable. Moreover, two occurrences of a Boolean variable cannot
conflict if they have the same polarity. From this observation we can derive a simple optimization
that allows for applying the JUMP rule more often: in (1) and (2) we consider only pairs of
intervals that come either from two opposite occurrences of the same Boolean variable (such as
a and ¬a) or from two atomic constraints such that at least one variable occurs in both.

4.3.3    Correctness
We prove soundness and completeness of the JUMP rule by showing, respectively, that an
accepted branch in the JUMP tableau implies one in the basic tableau, and vice versa.
Lemma 3. Let u be a poised node. Let u′ be the node obtained by applying the JUMP rule to
u, or the STEP rule if JUMP conditions are not satisfied. If the subtree rooted at u′ contains
an accepted branch, then the subtree of the basic tableau rooted at u also contains one.
Theorem 4 (Soundness). If the tableau built by using the JUMP rule has an accepted branch,
then the basic tableau for a formula ϕ also has an accepted branch
Theorem 5 (Completeness). If the basic tableau for a formula ϕ has an accepted branch, then
the tableau built by using the JUMP rule also has an accepted branch.
   We report manually written proofs of these results in Appendix B. Moreover, we have
formalized the above claims and their proofs with the Lean 4 proof assistant [18], with the help
of GPT 5.6 Sol [33]. The Lean formalization is publicly available in [40].

                                                                                                  11
STLSat                                                                Zamponi, Lammel, Bartocci and Chiari


5      STLSat Tool
STLSat [41] is a modular tool for satisfiability checking of bounded discrete-time STL formulas.
The full implementation, including source code, benchmarks, and reproducibility scripts, is
publicly available1 . Given a formula φ, STLSat determines whether there exists a discrete-
time signal w : N → Rn such that (w, 0) |= φ. STLSat implements three different solving
engines working over the same formula representation:
   • the tableau-based method described in §4;
   • a FOL engine for STL inspired by [29];
   • a quantifier-free encoding inspired by MPC [34] and bounded model checking [15] methods.

5.1      Tableau Method
STLSat features an efficient implementation of the tableau methodology described in §4.
    It introduces a lightweight syntactic simplification phase before tableau construction. This
pre-processing step applies common rewriting rules, including nested conjunction and disjunc-
tion flattening, redundant operand removal (e.g., φ ∧ ⊤ ≡ φ), and merging of temporal operator
intervals (e.g., G[0,3] φ ∧ G[2,5] φ ≡ G[0,5] φ). These simplifications reduce formula complexity
and, consequently, the depth of tableau expansion without affecting satisfiability.
    Furthermore, STLSat replaces the tableau expansion of [31], which relies on the program
call stack for node exploration, with an explicit stack-based implementation. This design enables
finer control over memory allocation and improves performance when exploring deep tableaux.
    STLSat performs local consistency checks of atomic propositions by invoking the Z3 solver
[17]. We also implemented a custom solver for systems of difference constraints by reducing
them to negative-cycle detection in graphs [16, 2, 20]. This optimization improves performance
by eliminating the external Z3 calls for supported formulas.

Witness Signals STLSat is able to extract witness signals for satisfiable STL formulas.
The witness signal is constructed by traversing the accepting branch of the basic tableau and
collecting the atomic propositions extracted at each time instant. The resulting signal is then
represented as a piecewise function over the time domain, with values determined by the ex-
tracted propositions.

Unsat-Core Extraction Whenever a formula is determined to be unsatisfiable, STLSat
performs a lightweight unsatisfiable-core extraction to identify the source of inconsistency. We
represent the input formula φ as a conjunction of subformulas after repeatedly applying   Vm the
∧-expansion rule, so that at the root node u0 we have Γ(u0 ) = {φ1 , . . . , φm }, and φ = i=1 φi .
Let A be the set of atomic predicates f (R) ▷◁ k occurring in φ. We associate each atomic
predicate a ∈ A to its originating subformula φi through a mapping M : A → {1, . . . , m}.
   During tableau expansion, every node contains a set of atomic predicates A(u) ⊆ A extracted
from the input formula φ. When a node is rejected by the underlying theory solver, the solver
provides the subset of conflicting atomic predicates responsible for the inconsistency:

                                 Cu = {au,1 , au,2 , . . . , au,k } ⊆ A(u).

    When all branches ofSthe tableau are rejected, the local unsatisfiable cores are aggregated
into a single set C = u rejected Cu and mapped back to their originating formulas in the

     1 https://github.com/ZamponiMarco/stlsat/



12
STLSat                                                         Zamponi, Lammel, Bartocci and Chiari


root node, producing a high-level unsatisfiable core U ⊆ Γ(u0 ) that identifies a subset of
subformulas responsible for the inconsistency, with U = {φi | ∃a ∈ C : M (a) = i}. The
returned core is unsatisfiable, but not necessarily irreducible or minimal. Its further evaluation
and minimization, as well as solver-native core extraction for the remaining engines, are left to
future work.

5.2    First-Order Logic Encoding
An almost out-of-the-box solution for STL satisfiability is to translate a formula φ into First-
Order Logic (FOL) by recursively replacing each operator with its semantics definition, and then
check the resulting formula with a theorem prover or an SMT solver with quantifier support.
    Li et al. [29] applies this idea to MLTL. They encode signals as functions from non-negative
integers (representing time) to Boolean values: for each atomic proposition p, they define a
function p : N → {⊤, ⊥}, such that p(t) = ⊤ iff p holds at time t. Moreover, they define a
Boolean function f taking two integers k and len, which returns ⊤ iff the FOL translation of φ
is true at time k for a signal of length len.
    We implement an optimized STL encoding where signals are integer-to-real functions (for
real values) or integer-to-Boolean functions (for Boolean signals). The translation follows the
semantics in §3. To reduce formula size, we employ the usual ad hoc FOL translations for the
F and G operators, rather than translating them to U.

5.3    Quantifier-Free SMT Encoding
Closely related to the FOL approach, STL satisfiability can also be encoded as a quantifier-
free SMT problem over linear real arithmetic, similarly to SMT encodings used for optimal
control [34] and bounded model checking [15].
    The encoding first computes the formula horizon and creates symbolic variables for each
signal variable at every time instant. The encoding recursively unfolds the semantics of STL op-
erators. Boolean operators are translated directly into their SMT counterparts, while temporal
operators are expanded over their intervals. The resulting quantifier-free linear real arithmetic
formula can be solved by an SMT solver.


6     Experiments
We compare the three STLSat engines against state-of-the-art STL and MLTL satisfiability
tools. For both logics, we include STLTree [32], the original Python implementation of [31];
for MLTL, we also compare with the best-performing technique for MLTL satisfiability analyzed
by Li et al. [29], namely their FOL encoding which we call MLTLSAT, obtained by running the
tool made available by the authors [28]. MLTLSAT translates MLTL formulas into SMTLIB
files, which we feed to Z3 4.15.8 [17]. We ran all experiments on a server equipped with an AMD
EPYC 9654 CPU and 755 GB of RAM running Ubuntu 24.04. The parallel configuration runs
all three engines concurrently and reports the wall-clock time until the first engine terminates,
thus representing a portfolio result. A replication package can be found in [40].

6.1    Benchmarks
We evaluate STLSat on MLTL and STL benchmark suites, whose descriptive statistics are
reported in Table 2.

                                                                                                13
STLSat                                                                                                                                                                         Zamponi, Lammel, Bartocci and Chiari


Table 2: Descriptive statistics of the MLTL and STL benchmark suites. Values show median
(95th percentile) for depth, temporal depth and horizon, and mean for branching factor (i.e.,
number of node children). The last four columns show the frequency (%) of each operator.

     Bench. suite                                                     Depth                     T. Depth                                          Horizon                                                    B. F.         F           G             U            R
                                          NASA-Boeing            8.0 (11.0)                        1.0 (1.9)                               100000.0 (100001.8)                                               1.80        12.8        87.2       0.0             0.0
     MLTL




                                          Random                 10.0 (20.0)                       6.0 (18.0)                                 461.0 (1374.0)                                                 1.46        36.8        37.1      15.9            10.3
                                          Random0                10.0 (20.0)                       6.0 (18.0)                                 316.0 (943.0)                                                  1.46        37.0        36.8      15.6            10.6
                                          Random-STL             10.0 (21.0)                        4.0 (8.0)                               1000.0 (10000.0)                                                 1.65        33.4        33.4      16.6            16.6
     STL




                                          Random0-STL            11.0 (25.0)                       5.0 (12.0)                                205.5 (4234.1)                                                  1.54        33.3        33.0      16.9            16.7



                                                  (a) NASA-Boeing suite                                                               (b) Random suite                                                                (c) Random0 suite
                                                                                                                         4000                                                                           4000
                                   60
            Number of benchmarks solved




                                                                                                Number of benchmarks solved




                                                                                                                                                                               Number of benchmarks solved
                                   50
                                                                                                                         3000                                                                           3000

                                   40

                                                                      STLSat parallel                                                                STLSat parallel                                                                    STLSat parallel
                                   30                                                                                    2000                                                                           2000
                                                                      STLSat JUMP tableau                                                            STLSat JUMP tableau                                                                STLSat JUMP tableau
                                                                      STLSat basic tableau                                                           STLSat basic tableau                                                               STLSat basic tableau
                                   20
                                                                      STLSat FOL                                                                     STLSat FOL                                                                         STLSat FOL
                                                                                                                         1000                                                                           1000
                                                                      STLSat SMT                                                                     STLSat SMT                                                                         STLSat SMT
                                   10
                                                                      STLTree unsound tableau                                                        STLTree unsound tableau                                                            STLTree unsound tableau
                                                                      MLTLSAT                                                                        MLTLSAT                                                                            MLTLSAT
                                          0                                                                                   0                                                                               0

                                              0            50                      100                                            0          50                    100                                            0             50                    100
                                                           Time (s)                                                                           Time (s)                                                                          Time (s)


                                                      Figure 3: Survival plots for MLTL benchmarks [29]. Higher is better.


MLTL. The first benchmark suite in Li et al. [29] contains three subsets of MLTL formulas:
    • NASA-Boeing: 63 satisfiable formulas extracted from real-world avionics systems;
    • Random: 4,000 randomly generated formulas with realistic patterns and random integer
      time intervals;
    • Random0 : 4,000 randomly generated formulas whose time intervals all start at 0.
All MLTL formulas use only Boolean variables, stressing temporal operators over large horizons
without linear real arithmetic.
STL. The second benchmark suite comprises three groups of STL formulas:
    • nine requirements collected by Melani et al. [31] plus the running example Φw ;
    • Random-STL: 2,000 randomly generated formulas of varying length;
    • Random0-STL: 2,000 random formulas of varying length with all intervals starting at 0.
Note that the satisfiability of all generated formulas is not controlled beforehand and is ulti-
mately determined by the solving engines. The generation process for the random STL bench-
mark suites is detailed in Appendix C.


6.2                                       Results
MLTL. We compare STLSat with STLTree and the FOL encoding of [29] (MLTLSAT). We
show the results as survival plots in Fig. 3, with a 120 s timeout. In Table 3 we present the
number of instances in which each STLSat solving engine was strictly the fastest, grouped by
benchmark and formula satisfiability for both MLTL and STL suites. On the NASA-Boeing
suite, the FOL encoding (§ 5.2) dominates: it solved 62 benchmarks within 80 s, reporting

14
STLSat                                                             Zamponi, Lammel, Bartocci and Chiari


Table 3: Fastest STLSat engine by benchmark and satisfiability class. Upper rows report
counts and lower rows percentages among instances solved by at least one engine (n); ties are
counted separately.

                                         sat                                    unsat
         benchmark     tableau   FOL      SMT     tie      n    tableau   FOL     SMT     tie     n
                          27       35       0       0      62      –        –       –      –       0
         nasa-boeing
                        43.5%    56.5%    0.0%    0.0%             –        –       –      –
  MLTL




                        3166      226      14      17    3423    153        23      3      0     179
         random
                       92.5%     6.6%     0.4%    0.5%          85.5%     12.8%   1.7%   0.0%
                        3278      190       3      16    3487    217        41      0      3     261
         random0
                       94.0%     5.4%     0.1%    0.5%          83.1%     15.7%   0.0%   1.2%
                        702       143      146     25    1016    227       121     22      43    413
         random
                       69.1%     14.1%    14.4%   2.4%          55.0%     29.3%   5.3%   10.4%
  STL




                        682       36       81      19    818     284       108     40     22     454
         random0
                       83.4%     4.4%     9.9%    2.3%          62.6%     23.8%   8.8%   4.8%



a parsing error on one. MLTLSAT solved 46 benchmarks within 108 s and timed out on 14
launching parsing errors on 3. This advantage comes from a smaller generated encoding with
fewer quantifiers: these formulas—derived from manually written requirement sets—contain
only F and G rather than U operators, and can benefit from our ad hoc encoding of F and G.
    On the other hand, tableau-based tools perform better on randomly generated formulas, with
STLSat outperforming STLTree despite using stricter jumping rules, thanks to the efficient
algorithm implementation. In fact, formulas in these suites contain many temporal operators
with wide time intervals, which can greatly benefit from the tableau’s JUMP rule. The SMT
encoding (§ 5.3) performed worst on average, consistent with the findings of [31], although it
was the only STLSat engine able to solve the Aerospace benchmark within the time limit.
    Executing STLSat’s three solving engines in parallel brings a slight benefit in random
benchmarks, because there are some formulas for which one particular engine performs better
than the others. In the NASA-Boeing set, instead, the FOL encoding terminates first on the
large majority of instances (although by a small margin), and parallel execution offsets the
overhead of running all engines.
STL. Table 4 shows our comparison on benchmarks from [31], plus the running example Φw .
STLSat outperforms STLTree in some benchmarks, but times out in the largest ones; on the
other hand, the FOL encoding quickly solves CPS, and the SMT encoding solves Aerospace
without timing out.
    Fig. 4 shows survival plots for randomly generated STL formulas. STLSat’s tableau per-
forms slightly worse than STLTree, but much better than the FOL and SMT encodings.
Table 3 suggests that the tableau is the fastest engine on most instances, while FOL and SMT
are each fastest on smaller subsets of formulas. In particular, FOL wins on most of the NASA-
Boeing benchmarks, and wins more frequently in unsatisfiable instances than satisfiable ones.
Consequently, parallel execution of the STLSat engines yields further computational gains.

Ablation Study Our JUMP rule is a sound and complete alternative to the JUMPOld rule [31],
although it is generally applicable in fewer cases. To assess its practical impact, we compare
the STLSat tableau against the basic tableau with JUMP disabled (where only STEP rules
execute) across all benchmarks from §6.1.
    Fig. 5 compares their solving times: most points lie below the bisector, showing that JUMP

                                                                                                       15
STLSat                                                                                                                                                Zamponi, Lammel, Bartocci and Chiari


Table 4: Results on STL benchmarks from [31]. Columns 2 to 4 contain, respectively, number
of requirements, maximum time Horizon, and temporal operators. Column R gives the result,
shared by all approaches (⊤ = “satisfiable”, ⊥ = “unsatisfiable”). The remaining columns give
the solution time (s) for each approach, where TO denotes a timeout at 120 s. Bold marks the
fastest solver per row.

 Benchmark            #                                        H   Op.            R            STLTree                                          STLSat       STLSat                     STLSat      STLSat
                                                                                                tableau                                           SMT           FOL                      basic t.   JUMP t.
 Car [3]               4                                  100      G,F,U          ⊤                  0.5328                                       0.0238           0.0212                  0.0114    0.0050
 Thermostat [3]        4                                   40      G,F,U,R        ⊤                  0.4930                                       0.0186           0.0310                  0.0060    0.0044
 Watertank [3]         4                                   50      G,F            ⊤                  0.5044                                       0.0174           0.0194                 0.0116      0.0146
 Railroad [3]          4                                  100      G,F            ⊥                  5.4144                                      0.0186            0.0582                  0.0538     0.0258
 Battery [3]           4                                   64      G,F,U          ⊤                  0.5940                                       0.0240           0.0852                  0.0158    0.0088
 PCV [26]              9                                1,250      G,F            ⊤                  2.2950                                       1.0698          0.0190                  22.1564    25.0328
 MTL [24]             10                                2,020      G,F            ⊥                  1.4636                                       0.1914          0.0178                   0.2798     0.2834
 CPS [13]             37                               13,799      G,F,U          ⊥                  3.1226                                          TO           0.0198                      TO         TO
 Aerospace [31]       31                                1,010      G,F            ⊤                 8.7816                                       37.5802              TO                      TO         TO
 Irrigation Φw , §1    3                                  160      G,F            ⊥                  0.6774                                      0.0306               TO                   0.0698     0.0404



                                                               (a) Random suite                                                                (b) Random0 suite
                                                2000                                                                            2000
                       Number of benchmarks solved




                                                                                                       Number of benchmarks solved




                                                1500                                                                            1500



                                                1000                                                                            1000
                                                                             STLSat parallel                                                                  STLSat parallel
                                                                             STLSat JUMP tableau                                                              STLSat JUMP tableau
                                                                             STLSat basic tableau                                                             STLSat basic tableau
                                                     500                                                                             500
                                                                             STLSat FOL                                                                       STLSat FOL
                                                                             STLSat SMT                                                                       STLSat SMT
                                                                             STLTree unsound tableau                                                          STLTree unsound tableau
                                                       0                                                                               0

                                                           0          50                   100                                             0          50                    100
                                                                      Time (s)                                                                         Time (s)


             Figure 4: Survival plots for random STL benchmarks. Higher is better.


generally improves performance. Furthermore, instances where jumping provides no benefit
from the optimization remain close to the bisector, indicating that computing and checking the
jump conditions introduces negligible overhead.


7     Conclusions
We presented STLSat, an open-source Rust tool for satisfiability checking of bounded discrete-
time STL. We identified an unsound optimization in the tableau of Melani et al. [31] and
replaced it with a sound and complete rule. STLSat combines this tableau with two alternative
encodings: a FOL translation and a quantifier-free SMT encoding, which can be executed in
parallel as a portfolio solver.
   Our extensive benchmark suite (covering both STL and MLTL, with real-world and ran-
domly generated instances) shows that STLSat performs comparably to STLTree, and often
outperforms state-of-the-art SMT encodings such as MLTLSAT. Furthermore, running all STL-
Sat solving engines in parallel yields the best overall performance. Moreover, we argued how

16
STLSat                                                                                                                                                                                                                Zamponi, Lammel, Bartocci and Chiari



                                   (a) NASA-Boeing (MLTL)                                                                                      (b) Random (MLTL)                                                                                            (c) Random0 (MLTL)
                                   100                                                                                                   100                                                                                                          100
                                     5                                                                                                     5                                                                                                            5

                                     2                                                                                                     2                                                                                                            2
    STLSat JUMP tableau time (s)




                                                                                                          STLSat JUMP tableau time (s)




                                                                                                                                                                                                                       STLSat JUMP tableau time (s)
                                   10                                                                                                    10                                                                                                           10
                                     5                                                                                                     5                                                                                                            5

                                     2                                                                                                     2                                                                                                            2

                                     1                                                                                                     1                                                                                                            1
                                     5                                                                                                     5                                                                                                            5

                                     2                                                                                                     2                                                                                                            2

                                   0.1                                                                                                   0.1                                                                                                          0.1
                                     5                                                                                                     5                                                                                                            5

                                     2                                                                                                     2                                                                                                            2

                             0.01                                                                                                  0.01                                                                                                         0.01
                                0.01      0.1                            1                10                                          0.01             0.1                            1                10                                          0.01             0.1         1          10
                                         STLSat basic tableau time (s)                                                                                STLSat basic tableau time (s)                                                                                STLSat basic tableau time (s)

                                                                                         (d) Random (STL)                                                                                             (e) Random0 (STL)
                                                                                   100                                                                                                          100
                                                                                     5                                                                                                            5

                                                                                     2                                                                                                            2
                                                    STLSat JUMP tableau time (s)




                                                                                                                                                                 STLSat JUMP tableau time (s)
                                                                                   10                                                                                                           10
                                                                                     5                                                                                                            5

                                                                                     2                                                                                                            2

                                                                                     1                                                                                                            1
                                                                                     5                                                                                                            5

                                                                                     2                                                                                                            2

                                                                                   0.1                                                                                                          0.1
                                                                                     5                                                                                                            5

                                                                                     2                                                                                                            2

                                                                             0.01                                                                                                         0.01
                                                                                0.01            0.1                            1                 10                                          0.01            0.1                            1                 10
                                                                                               STLSat basic tableau time (s)                                                                                STLSat basic tableau time (s)


   Figure 5: Scatter plots for the STLSat ablation study on MLTL and STL benchmarks.


unsat core extraction facilitates specification mining, redundancy elimination, and traceability
in CPS development.
    Future work will focus on temporal analysis for unsat cores, support for unbounded STL
operators and continuous-time semantics, tighter integration with model-checking, falsification,
and specification mining, and the development of visual debugging interfaces that display coun-
terexample signals and core constraints.


Acknowledgements
Partially funded by the European Union. Views and opinions expressed are those of the authors
only and do not necessarily reflect those of the European Union or the European Health and
Digital Executive Agency (HADEA). Neither the European Union nor the granting authority
can be held responsible for them. RobustifAI project, ID 101212818; VASSAL project, ID
101160022; MoSaiC project, ID 101103010. Partially funded by WWTF project ICT22-023
(TAIGER).


References
 [1] Rajeev Alur, Tomás Feder, and Thomas A. Henzinger. The benefits of relaxing punctuality.
     J. ACM, 43(1):116–146, 1996. doi:10.1145/227595.227602.

                                                                                                                                                                                                                                                                                                   17
STLSat                                                      Zamponi, Lammel, Bartocci and Chiari


 [2] Alessandro Armando, Claudio Castellini, Enrico Giunchiglia, and Marco Maratea. A SAT-
     based decision procedure for the Boolean combination of difference constraints. In SAT
     2004, 2004. URL http://www.satisfiability.org/SAT04/programme/71.pdf.

 [3] Kyungmin Bae and Jia Lee. Bounded model checking of signal temporal logic properties
     using syntactic separation. Proc. ACM Program. Lang., 3:1–30, 2019. doi:10.1145/3290364.

 [4] Ezio Bartocci, Luca Bortolussi, Laura Nenzi, and Guido Sanguinetti. System design of
     stochastic models using robustness of temporal properties. Theor. Comput. Sci., 587:3–25,
     2015. doi:10.1016/J.TCS.2015.02.046.

 [5] Ezio Bartocci, Jyotirmoy V. Deshmukh, Alexandre Donzé, Georgios Fainekos, Oded Maler,
     Dejan Nickovic, and Sriram Sankaranarayanan. Specification-based monitoring of cyber-
     physical systems: A survey on theory, tools and applications. In Lectures on Runtime
     Verification - Introductory and Advanced Topics, volume 10457 of LNCS, pages 135–175.
     Springer, 2018. doi:10.1007/978-3-319-75632-5_5.

 [6] Ezio Bartocci, Thomas Ferrère, Niveditha Manjunath, and Dejan Nickovic. Localizing
     faults in Simulink/Stateflow models with STL. In HSCC ’18, pages 197–206. ACM, 2018.
     doi:10.1145/3178126.3178131.

 [7] Ezio Bartocci, Niveditha Manjunath, Leonardo Mariani, Cristinel Mateis, and Dejan Nick-
     ovic. Cpsdebug: Automatic failure explanation in CPS models. Int. J. Softw. Tools Tech-
     nol. Transf., 23(5):783–796, 2021. doi:10.1007/S10009-020-00599-4.

 [8] Ezio Bartocci, Cristinel Mateis, Eleonora Nesterini, and Dejan Nickovic. Survey on
     mining signal temporal logic specifications. Inf. Comput., 289(Part):104957, 2022.
     doi:10.1016/J.IC.2022.104957.

 [9] Ezio Bartocci,    Leonardo Mariani,  Dejan Nickovic, and Drishti Yadav.
     Property-based mutation testing.  In ICST ’23, pages 222–233. IEEE, 2023.
     doi:10.1109/ICST57152.2023.00029.

[10] Marcello M. Bersani, Matteo Rossi, and Pierluigi San Pietro. A tool for deciding the
     satisfiability of continuous-time metric temporal logic. In TIME’13, pages 99–106. IEEE
     Computer Society, 2013. doi:10.1109/TIME.2013.20.

[11] Marcello M. Bersani, Matteo Rossi, and Pierluigi San Pietro.   An SMT-based
     approach to satisfiability checking of MITL.   Inf. Comput., 245:72–97, 2015.
     doi:10.1016/J.IC.2015.06.007.

[12] Marcello M. Bersani, Matteo Rossi, and Pierluigi San Pietro. A tool for deciding the
     satisfiability of continuous-time metric temporal logic. Acta Informatica, 53(2):171–206,
     2016. doi:10.1007/S00236-015-0229-Y.

[13] Chaima Boufaied, Maris Jukss, Domenico Bianculli, Lionel C. Briand, and Yago Isasi
     Parache. Signal-based properties of cyber-physical systems: Taxonomy and logic-based
     characterization. J. Syst. Softw., 174:110881, 2021. doi:10.1016/J.JSS.2020.110881.

[14] Alessandro Cimatti, Alberto Griggio, and Roberto Sebastiani. A simple and flexible way
     of computing small unsatisfiable cores in SAT modulo theories. In SAT’07, volume 4501
     of LNCS, pages 334–339. Springer, 2007. doi:10.1007/978-3-540-72788-0_32.

18
STLSat                                                       Zamponi, Lammel, Bartocci and Chiari


[15] Edmund M. Clarke, Armin Biere, Richard Raimi, and Yunshan Zhu. Bounded model
     checking using satisfiability solving. Formal Methods Syst. Des., 19(1):7–34, 2001.
     doi:10.1023/A:1011276507260.

[16] Thomas H Cormen, Charles E Leiserson, Ronald L Rivest, and Clifford Stein. Introduction
     to algorithms. MIT press, 2022.

[17] Leonardo de Moura and Nicolaj Bjørner. Z3: An efficient SMT solver. In TACAS’08.,
     volume 4963 of LNCS. Springer, 2008. doi:https://doi.org/10.1007/978-3-540-78800-3_24.

[18] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming
     language. In CADE’21, LNCS, page 625–635, Berlin, Heidelberg, 2021. Springer-Verlag.
     doi:10.1007/978-3-030-79876-5_37.

[19] Adel Dokhanchi, Bardh Hoxha, and Georgios Fainekos. Formal requirement debugging for
     testing and verification of cyber-physical systems. ACM Trans. Embed. Comput. Syst., 17
     (2), 2017. ISSN 1539-9087. doi:10.1145/3147451.

[20] Bruno Dutertre and Leonardo M. de Moura. A fast linear-arithmetic solver for DPLL(T). In
     CAV 2006, volume 4144 of LNCS, pages 81–94. Springer, 2006. doi:10.1007/11817963_11.

[21] Luca Geatti, Nicola Gigante, Angelo Montanari, and Mark Reynolds. One-pass and tree-
     shaped tableau systems for TPTL and TPTLb +past. Inf. Comput., 278:104599, 2021.
     doi:10.1016/J.IC.2020.104599.

[22] Luca Geatti, Nicola Gigante, Angelo Montanari, and Gabriele Venturato. SAT meets
     tableaux for linear temporal logic satisfiability. J. Autom. Reason., 68(2):6, 2024.
     doi:10.1007/S10817-023-09691-1.

[23] Yoram Hirshfeld and Alexander Moshe Rabinovich. Timer formulas and decidable metric
     temporal logic. Inf. Comput., 198(2):148–178, 2005. doi:10.1016/J.IC.2004.12.002.

[24] Bardh Hoxha, Houssam Abbas, and Georgios Fainekos. Benchmarks for temporal logic
     requirements for automotive systems. In ARCH14-15, volume 34 of EPiC Series in Com-
     puting, pages 25–30. EasyChair, 2015. doi:10.29007/xwrs.

[25] Stefan Jaksic, Ezio Bartocci, Radu Grosu, Reinhard Kloibhofer, Thang Nguyen, and Dejan
     Nickovic. From signal temporal logic to FPGA monitors. In MEMOCODE ’15, pages 218–
     227. IEEE, 2015. doi:10.1109/MEMCOD.2015.7340489.

[26] Xiaoqing Jin, Jyotirmoy V. Deshmukh, James Kapinski, Koichi Ueda, and Ken Butts.
     Powertrain control verification benchmark. In HSCC’14, page 253–262, New York, USA,
     2014. ACM. ISBN 9781450327329. doi:10.1145/2562059.2562140.

[27] Jia Lee, Geunyeol Yu, and Kyungmin Bae.                     Efficient SMT-based model
     checking for signal temporal logic. In ASE’21,             pages 343–354. IEEE, 2021.
     doi:10.1109/ASE51524.2021.9678719.

[28] Jianwen Li.   mltlsat.   GitHub.com, 2019.      URL https://github.com/lijwen2748/
     mltlsat.

[29] Jianwen Li, Moshe Y. Vardi, and Kristin Y. Rozier. Satisfiability checking for mission-time
     LTL (MLTL). Inf. Comput., 289(Part):104923, 2022. doi:10.1016/J.IC.2022.104923.

                                                                                              19
STLSat                                                      Zamponi, Lammel, Bartocci and Chiari


[30] Oded Maler and Dejan Nickovic. Monitoring temporal properties of continuous sig-
     nals. In FORMATS/FTRTFT’04, volume 3253 of LNCS, pages 152–166. Springer, 2004.
     doi:10.1007/978-3-540-30206-3_12.

[31] Beatrice Melani, Ezio Bartocci, and Michele Chiari. A tree-shaped tableau for checking
     the satisfiability of signal temporal logic with bounded temporal operators. ACM Trans.
     Embed. Comput. Syst., 24(5s):1–26, 2025. doi:10.1145/3759917.

[32] Beatrice Melani, Ezio Bartocci, and Michele Chiari. Stltree, 2025. URL https://github.
     com/beamelani/Consistency_Check.

[33] OpenAI. GPT-5.6: Frontier intelligence that scales with your ambition. https://openai.
     com/index/gpt-5-6/, 2026. Accessed: 2026-08-28.

[34] Vasumathi Raman, Alexandre Donzé, Mehdi Maasoumy, Richard M. Murray, Al-
     berto L. Sangiovanni-Vincentelli, and Sanjit A. Seshia. Model predictive control
     with signal temporal logic specifications.  In CDC’14, pages 81–87. IEEE, 2014.
     doi:10.1109/CDC.2014.7039363.

[35] Thomas Reinbacher, Kristin Y. Rozier, and Johann Schumann. Temporal-logic based
     runtime observer pairs for system health management of real-time systems. In TACAS’14,
     volume 8413 of LNCS, pages 357–372. Springer, 2014. doi:10.1007/978-3-642-54862-8_24.

[36] Mark Reynolds. A new rule for LTL tableaux. In GandALF’16, volume 26 of EPCTS,
     pages 287–301, 2016. doi:10.4204/EPTCS.226.20.

[37] Hendrik Roehm, Thomas Heinz, and Eva Charlotte Mayer. Stlinspector: STL validation
     with guarantees. In CAV’17, volume 10426 of LNCS, pages 225–232. Springer, 2017.
     doi:10.1007/978-3-319-63387-9_11.

[38] Sriram Sankaranarayanan and Georgios Fainekos. Falsification of temporal properties of
     hybrid systems using the cross-entropy method. In HSCC’12, pages 125–134. ACM, 2012.
     doi:10.1145/2185632.2185653.

[39] Viktor Schuppan. Extracting unsatisfiable cores for LTL via temporal resolution. Acta
     Informatica, 53(3):247–299, 2016. doi:10.1007/S00236-015-0242-1.

[40] Marco Zamponi, Michele Chiari, and Ezio Bartocci. Replication package for the paper
     “STLSat—an improved tableau for satisfiability checking of Signal Temporal Logic formu-
     las”, 2026. URL https://doi.org/10.5281/zenodo.22746464.

[41] Marco Zamponi, Michele Chiari, and Florian Lammel. STLSat. GitHub.com, 2026. URL
     https://github.com/ZamponiMarco/stlsat.



A     Flaws in the JUMPOld rule
In this section, we show that the JUMPOld rule proposed by Melani et al. [31] undermines both
soundness and completeness of the tableau. We report the definition of the JUMPOld rule almost
verbatim from [31] below.

20
STLSat                                                                 Zamponi, Lammel, Bartocci and Chiari


   Melani et al. [31] manage formula superscripts in a slightly different way: nested operators
extracted by expansion rules are annotated with the interval of the parent formula, rather than
the formula itself:

               textI (φ1 B[a,b] φ2 ) = φ1 BI[a+t,b+t] φ2                 with B ∈ {sU, sR}

where I is the interval [a, b] in Table 1, and textI replaces textψ in that table. Note that, since
such superscripts are not used in the basic tableau, this change does not interfere with its
correctness.
                                                                                         J
   The JUMPOld rule can be applied to a poised node u if all marked operators φ1 sU[a,b] φ2 or
     J
φ2 sR[a,b] φ1 in Γ(u), with J = [aJ , bJ ] and t(u) ≥ bJ , are such that
   i. t(u) < b, and
  ii. for all temporal operators ψ in φ1 that are not nested in any other temporal operator we
      have t(u) ≥ a + Iu (ψ),
where Iu (ψ) is the upper endpoint of the interval of ψ (e.g., Iu (G[a,b] ψ ′ ) = b). Otherwise, only
the STEP rule can be applied.
   If the conditions above are met, then u has one child u′ such that t(u′ ) = min{t ∈ K(u) |
t > t(u)}, where

              K(u) = {a, b | φ1 BJ[a,b] φ2 ∈ Γ(u) ∧ B ∈ {sU, sR, sU, sR} ∧ t(u) ≥ bJ },

and, setting k = t(u′ ) − t(u), we have

    Γ(u′ ) = {φ1 BJI φ2 ∈ Γ(u) | B ∈ {sU, sR} ∧ t(u) ≥ bJ }
             ∪ {φ1 BJ[a+k,b+k] φ2 | φ1 BJ[a,b] φ2 ∈ Γ(u) ∧ B ∈ {sU, sR} ∧ t(u) < bJ }
                                      J
             ∪ {φ1 BJ[a,b] φ2 | φ1 B[a,b] φ2 ∈ Γ(u) ∧ B ∈ {sU, sR} ∧ t(u) ≥ bJ ∧ t(u) < b}
                                            J
             ∪ {φ1 BJ[a+k,b+k] φ2 | φ1 B[a,b] φ2 ∈ Γ(u) ∧ B ∈ {sU, sR} ∧ t(u) < bJ ∧ t(u) < b}

   The JUMPOld rule has two main issues:
   1. condition ii. only takes into account one level of nesting of temporal operators, and only
      in the right-hand-side operand; and
   2. the set Γ(u′ ) does not faithfully re-create the label that node u′ would have if it had been
      reached by repeatedly applying the STEP rule until reaching a node with t = t(u) + k,
      dropping formulas that can reveal inconsistencies.
   As shown in Section 4.2, formula φS witnesses the unsoundness of the JUMPOld rule mainly
because of the second issue above. The following formula illustrates the first issue:

                      φ′S = (G[0,0] G[5,5] a) sU[0,4] (G[5,5] ¬c) ∧ G[5,8] c ∧ G[8,8] ¬a

    Fig. 6 shows part of the tableau rooted in φ′S that uses the JUMPOld rule. First, the tableau
tries to satisfy the U operator at time 0 by expanding it to G[5,5] ¬c in node u2 , but this leads to
a contradiction with G[5,8] c. It thus tries extracting ψ = G[0,0] G[5,5] a in node u3 , and since here
Iu (ψ) = 0, the conditions for the JUMPOld rule apply. Thus, the tableau jumps to u8 which, as
noted in Section 4.2, does not contain G[8,8] ¬c, allowing the satisfaction of all operators.

                                                                                                        21
STLSat                                                                       Zamponi, Lammel, Bartocci and Chiari


                     u0 : (G[0,0] G[5,5] a) U[0,4] (G[5,5] ¬c) ∧ G[5,8] c ∧ G[8,8] ¬a | 0



                     u1 : (G[0,0] G[5,5] a) U[0,4] (G[5,5] ¬c), G[5,8] c, G[8,8] ¬a | 0

                                                  U

                                                                                                                     [0,4]
u2 : G[5,5] ¬c, G[5,8] c, G[8,8] ¬a | 0        u3 : (G[0,0] G[5,5] a) sU[0,4] (G[5,5] ¬c), G[5,8] c, G[8,8] ¬a, G[0,0] G[5,5] a | 0

             JUMP                                                                     G

u4 : G[8,8] ¬a, G[5,5] ¬c, G[5,8] c | 5                                                                                 [0,0]
                                                  u7 : (G[0,0] G[5,5] a) sU[0,4] (G[5,5] ¬c), G[5,8] c, G[8,8] ¬a, G[5,5] a | 0
                 G
                                                                                  JUMP

  u5 : G[8,8] ¬a, G[5,8] c, ¬c, c | 5                                                                        [0,0]
                                                  u8 : (G[0,0] G[5,5] a) U[4,4] (G[5,5] ¬c), G[8,8] ¬a, G[5,5] a, G[5,8] c | 4
           ✗ LOC-UNSAT
                                                                                       U

                                                                  [0,0]
                                               u9 : G[8,8] ¬a, G[5,5] a, G[5,8] c, G[9,9] ¬c | 4       ...

                                                                  STEP
                                                                      ...



                                                                 u18 : ¬c | 9
                                                                  ✓ EMPTY


                       Figure 6: Tableau with the JUMPOld rule for formula φ′S .


    The new JUMP rule that we present in Section 4.3 does not suffer from the same issue thanks
to the soundness limit (cf. Section 4.3.1). In fact, due to the U operator we have (0, 5) ∈ N (u)
and due to G[8,8] ¬a we have (8, 8) ∈ O(u). Thus, we have ksound     ∗
                                                                          (u) ≤ lo − rn = 8 − 5 = 3:
the tableau may jump at most to a node u with t(u ) = 3, in which either we try to satisfy
                                                ′          ′

the U operator, encountering the contradiction between G[8,8] ¬c and G[5,8] c, or we postpone
its satisfaction, revealing the contradiction between G[3,3] G[5,5] a and G[8,8] ¬a.
    The JUMPOld rule also undermines the completeness of the tableau. Consider the following
formula:
                       φC = a sU[0,10] (b ∧ G[20,30] c) ∧ G[0,27] ¬c ∧ G[10,10] ¬b

This formula is satisfiable, as shown by an accepting branch of the basic tableau in Fig. 7. In
satisfying signals, the sU operator must have its right-hand operand satisfied at times 8 or 9.
In fact, formula G[20,30] c conflicts with G[0,27] ¬c if it is extracted at a time in between 0 and 7,
while b conflicts with G[10,10] ¬b at time 10.
    Thus, the tableau branch that tries to satisfy the sU operator at time 0 is rejected, while
the one that postpones its satisfaction remains. The JUMPOld rule then jumps directly to time
10, where the sU operator must be satisfied, but it cannot: by skipping nodes with times 8 and
9, the JUMPOld rule prevents the tableau from finding two possible accepting branches. Thus,

22
STLSat                                                            Zamponi, Lammel, Bartocci and Chiari


                         u0 : a sU[0,10] (b ∧ G[20,30] c) ∧ G[0,27] ¬c ∧ G[10,10] ¬b | 0

                                                       ...
                                                    STEP

                           u1 : G[10,10] ¬b, G[8,27] ¬c, a sU[8,10] b ∧ G[20,30] c | 8


                         u2 : G[10,10] ¬b, G[8,27] ¬c, a sU[8,10] b ∧ G[20,30] c, ¬c | 8


              u3 : G[10,10] ¬b, G[8,27] ¬c, b ∧ G[28,38] c, ¬c | 8     ...

                                      ...
                                  STEP

                             u4 : G[38,38] c | 38


                                 u5 : c | 38
                                  ✓ EMPTY

          Figure 7: Part of an accepting branch of the basic tableau for formula φC .


the JUMPOld rule makes the tableau incomplete, as it may declare unsatisfiable formulas that
are actually satisfiable.
    By contrast, with our JUMP rule, in each node u with a sU[0,10] (b ∧ G[20,30] c) ∈ Γ(u) we
have (t(u) + 20, t(u) + 30) ∈ M (u), and (0, 27) ∈ S(u), due to G[0,27] ¬c. Since for all t ∈ [0, 7]
we have (t + 20, t + 30) ∩ (0, 27) ̸= ∅, the JUMP rule cannot be applied until a node with time
8 is reached. In such a node the expansion rule for the sU operator is applied, generating an
accepting branch.


B     Theorem Proofs
Proof of Lemma 2. If ρ does not appear within a temporal operator, then it may appear only in
the labels of descendants v of u generated by the expansion rules for the ∧ and ∨ operators. Such
rules generate children nodes with the same time as the parent, hence t(v) = t(u). Moreover,
the STEP rule drops all non-temporal operators and propositions, hence none of the nodes it
produces may contain ρ.
    We prove the case in which ρ appears within a temporal operator only for the t(v) ≤ r side,
the other one (l ≤ t(v)) being analogous. The computation of T (φ) is recursive on the syntactic
structure of φ, and (l, r) ∈ T (φ) results from a sequence of nested formulas terminating in ρ.
We denote this sequence as π = ⟨θn , θn−1 , . . . , θ0 ⟩, where:
    • θn = φ;
    • θi is the subformula of θi+1 selected by the recursive application of T (φ) that yields (l, r);
    • θ0 = ρ.
For each θi in the path, let (li , ri ) ∈ T (θi ) denote the element contributed by θi to (l, r) along
the recursive computation, so that (ln , rn ) = (l, r) and (l0 , r0 ) = (0, 0). Furthermore, let m be

                                                                                                   23
STLSat                                                                     Zamponi, Lammel, Bartocci and Chiari


the index of the last temporal operator in the sequence: θm = θm,1 BI θm,2 , with B ∈ {sU, sR},
and for m < i ≤ n, we have θi = θi,1 ◦ θi,2 with ◦ ∈ {∧, ∨}2 .
    We now prove the claim that for each formula θi with 0 ≤ i < m, and any node ui such
that text(ui ) (θi ) ∈ Γ(ui ), and any node u′i in the subtree rooted at ui , if we have ρ ∈ Γ(u′i ) that
is an occurrence derived from the expansion of θi along π, then t(u′i ) ≤ t(ui ) + ri . We proceed
by induction on i, with cases on the shape of θi .
    For the base case we have θ0 = ρ, and T (θ0 ) = {(0, 0)}, so r0 = 0. Since no expansion rules
can be applied to ρ, and the STEP rule does not propagate ρ to its child, ρ may only appear
in descendants of u0 that do not result from an application of STEP, thus only in u0 itself or
nodes u′0 such that t(u′0 ) = t(u0 ). Hence, t(u′0 ) = t(u0 ) ≤ t(u0 ) + r0 , and the claim holds.
    The inductive step is by cases on the shape of θi :

     • If θi = ¬θi−1
                 ′
                     , then T (θi ) = T (θi−1
                                          ′
                                              ), so ri = ri−1 , and the claim follows by the induction
       hypothesis.
     • Let θi = θi,1 ∨ θi,2 and, w.l.o.g., θi−1 = θi,1 (the other case is analogous). Since T (θi ) =
       T (θi,1 ) ∪ T (θi,2 ), we have ri = ri−1 . According to Table 1, the root ui of the subtree in
       which θi appears has two children ui,1 = ui−1 and ui,2 such that text(ui ) (θi,1 ) ∈ Γ(ui,1 )
       and θi ̸∈ Γ(ui,1 ); text(ui ) (θi,2 ) ∈ Γ(ui,2 ) and θi ̸∈ Γ(ui,2 ); and t(ui−1 ) = t(ui,1 ) = t(ui,2 ) =
       t(ui ). Node u′i may only appear in the subtree rooted in ui,1 . Hence, by the induction
       hypothesis, t(u′i ) ≤ t(ui,1 ) + ri−1 = t(ui ) + ri , and the claim holds.
     • The case for θi = θi,1 ∧ θi,2 is analogous.

     • Let θi = θi,1 sU[a,b] θi,2 . According to the operator semantics and Table 1, since text(ui ) (θi ) ∈
       Γ(ui ), any branch that contains ui must contain3 a node ui,2 such that t(ui,2 ) ∈ [a +
       t(ui ), b+t(ui )] and text(ui,2 ) (θi,2 ) ∈ Γ(ui,2 ), and for all time instants t′ with a+t(ui ) ≤ t′ <
       t(ui,2 ) there must be a node ut′ such that t(ut′ ) = t′ and text(ut′ ) (θi,1 ) ∈ Γ(ut′ ). Assume
       w.l.o.g. that θi−1 = θi,1 (the other case is analogous). Consider any such node ut′ . By
       the induction hypothesis, for all nodes v in the subtree rooted in ut′ , if we have ρ ∈ Γ(v),
       then t(v) ≤ t(ut′ ) + ri−1 = t′ + ri−1 . By the definition of T (θi ), we have ri = ri−1 + b − 1,
       and since t′ < b + t(ui ) we have t(v) ≤ t′ + ri−1 < b + t(ui ) + ri−1 = t(ui ) + ri , and the
       claim holds.
        The sR operator can be treated analogously.

    We now come to θi with m ≤ i ≤ n, for which we prove that for any node ui such that
θi ∈ Γ(ui ), and any node u′i in the subtree rooted at ui , if we have ρ ∈ Γ(u′i ) that is an
occurrence derived from the expansion of θi along π, then t(u′i ) ≤ ri .
    Let θm = θm,1 sU[a,b] θm,2 (the case for sR is analogous). The argument is similar to the
inductive step of the previous claim, except θm ∈ Γ(um ), instead of text(um ) (θm ) ∈ Γ(um ).
Thus, any branch that contains um must contain a node um,2 such that t(um,2 ) ∈ [a, b] and
text(um,2 ) (θm,2 ) ∈ Γ(um,2 ), and for all time instants t′ with a ≤ t′ < t(um,2 ) there must be a
node ut′ such that t(ut′ ) = t′ and text(ut′ ) (θm,1 ) ∈ Γ(ut′ ). We assume w.l.o.g. that θm−1 = θm,1 :
our previous claim holds for it. Hence, consider any such node ut′ . For all nodes v in the subtree
rooted in ut′ , if we have ρ ∈ Γ(v), then t(v) ≤ t(ut′ ) + rm−1 = t′ + rm−1 . By the definition of
T (θm ), we have rm = rm−1 +b−1, and since t′ < b we have t(v) ≤ t′ +rm−1 ≤ b−1+rm−1 = rm ,
and the claim holds.

     2 We assume φ to be in strict normal form, so temporal operators cannot be nested in a negation.
     3 Unless the branch is rejected before u
                                             i,2 appears. In this case, however, the claim is trivially true.



24
STLSat                                                            Zamponi, Lammel, Bartocci and Chiari


    To conclude the proof, it suffices to notice that for m < i ≤ n, the top-level operator in θi
is ∧ or ∨. Hence, ri = rm , and ρ appears in descendants v of um such that t(v) ≤ rm = ri .

Proof of Lemma 3. We proceed by contradiction. Assume that no branch below u in the basic
tableau is accepted, while the subtree rooted at u′ contains an accepted branch.
    If the STEP rule is applied, then u′ is also the successor of u in the basic tableau, so the
accepted branch below u′ is already a branch below u in the basic tableau, contradicting the
assumption. Hence, in the following we assume that u′ is obtained by applying the JUMP rule.
Let k = k ∗ (u) be the jump size, so that t(u′ ) = t(u) + k.
    Since Γ(u) is consistent (otherwise u would be rejected by the local inconsistency check),
any rejection in the basic tableau must arise from further expansions along branches below u.
    We focus on the branch of the basic tableau where we postpone the satisfaction of temporal
operators—i.e., obtained by always following the postponement child Γφ (up ) whenever an active
temporal operator is expanded—and apply the STEP rule until we reach a poised node v with
time t(u) + j. Since no branch below u is accepted by assumption, this branch must be rejected.
    The only structural difference between the basic tableau below u and the jump tableau
below u′ is that the basic tableau explicitly generates intermediate nodes at time instants
t(u) + 1, . . . , t(u′ ) − 1, while the jump tableau skips them. Since k ≤ k(u), no temporal operator
becomes active or expires at a skipped instant. Hence, divergence in satisfiability between the
two trees can only occur if extracting an invariant from some active temporal operator at an
intermediate time step t(u) + j, for 1 ≤ j < k, introduces atomic constraints that become
inconsistent with constraints derived from some formula in Γ(u). We now show that no such
new contradictions arise.
    Let ρ denote an atomic proposition arising from the extraction of an invariant of some
marked temporal operator at an intermediate time, and let σ denote an atomic proposition
from another formula ψ in Γ(u).
    Let (ln , rn ) ∈ N (u) be the validity interval (from T (text(u) (φ1 ))) of the invariant producing
ρ, and let (lo , ro ) ∈ O(u) be the validity interval of T (ψ) terminating on the atomic proposition
σ. Note that formulas with an active parent are excluded from O(u) because the validity
intervals of any derived proposition σ are contained in those of their active parent. This
redundancy is a consequence of Lemma 2, which indirectly shows that the validity intervals of
propositions in nested subformulas are always included in the ones of their active ancestors.
    The soundness condition of the JUMP rule, namely (1), guarantees that for all such pairs,
either rn < lo or ro < ln .

Case rn < lo First, suppose that ρ is nested into a temporal operator within φ1 . Since j <
          ∗
    k ≤ ksound (u) ≤ lo − rn , we have rn + j < lo , where rn + j is the upper validity bound of
    text(u)+j
              (φ1 ). Applying Lemma 2 to text(u)+j (φ1 ), any occurrence of ρ can only appear
    in a node wρ with t(wρ ) ≤ rn + j. Applying Lemma 2 to ψ, any occurrence of σ derived
    from the expansion of ψ can only appear in a node wσ with t(wσ ) ≥ lo . Hence t(wρ ) ≤
    rn + j < lo ≤ t(wσ ), so ρ and σ cannot occur together in any node and no inconsistency
    can arise.
      If ρ is not nested into any temporal operator in φ1 , then by Lemma 2 we have t(wρ ) =
      t(u) + j ≤ rn + j < lo ≤ t(wσ ). Note that, by the definition of O(u), σ is always nested
      into at least one temporal operator.

Case ro < ln Note that ρ must be nested into a temporal operator within φ1 . Otherwise, we
    would have ln = t(u) > ro , meaning that σ could only occur in the past.

                                                                                                    25
STLSat                                                               Zamponi, Lammel, Bartocci and Chiari


      Applying Lemma 2 to ψ, any occurrence of σ derived from the expansion of ψ can only
      appear in a node wσ with t(wσ ) ≤ ro . Applying Lemma 2 to text(u)+j (φ1 ), any occurrence
      of ρ derived from its expansion can only appear in a node wρ with t(wρ ) ≥ ln + j. Hence
      t(wσ ) ≤ ro < ln < ln + j ≤ t(wρ ), so ρ and σ cannot co-occur in any node and no
      inconsistency can arise.

    We have shown that no inconsistency can be triggered by invariant extractions at any
skipped time t(u) + j. Consequently, the postponement branch of the basic tableau cannot
be rejected before time t(u) + k. At time t(u) + k, this branch preserves the same temporal
obligations as u′ . Since the subtree rooted at u′ contains an accepted branch, the basic tableau
rooted at u admits an accepted branch too, contradicting the initial assumptions.

Proof of Theorem 4. Let TJ be the tableau constructed using the JUMP rule, and assume it
contains an accepted branch u = u0 , . . . , un . We consider the poised nodes in the accepted
branch p ⊆ u.
    Take a poised node pi where the JUMP rule is applied, resulting in a node v, so that
t(v) = t(pi ) + k ∗ (pi ). By Lemma 3, if k ∗ (pi ) < ksound
                                                       ∗
                                                             (pi ), the basic tableau subtree rooted at pi
must also contain an accepted branch. In the case where k ∗ (pi ) = ksound     ∗
                                                                                    (pi ), time instant t(v)
will be the first potential time instant where a conflict could arise, but this node is checked via
the standard consistency checks both in the basic tableau and the one using the JUMP rule.

Proof of Theorem 5. Consider a poised node u such that the JUMP rule is applied to it, and
denote the resulting node as u′ .
    Let us prove the claim by contradiction. Assume that the basic tableau contains an accepting
branch, but all branches originating from u in the tableau with the JUMP rule are rejected.
This means that every branch generated from the temporal obligations in Γ(u′ ) is eventually
rejected.
    If a step condition is triggered, then u′ is the successor of u in the basic tableau as well,
so the tableau with the JUMP rule would be accepted as well, contradicting the hypothesis.
Hence, in the following, we assume that u′ is obtained by applying the JUMP with a jump size
k = k ∗ (u), so that t(u′ ) = t(u) + k.
    The only possibility for the basic tableau to contain an accepted branch is that, at some
intermediate node w with t(u) < t(w) < t(u′ ), the accepting branch selected the satisfaction
of a temporal formula ψ ∈ Γ(w) (through expansion rule Γψ (w1 )) that, if postponed, would
otherwise be propagated to Γ(u′ ), with ψ = φ1 sU[a,b] φ2 or ψ = φ2 sR[a,b] φ1 . Let j = t(w)−t(u)
and note that 1 ≤ j < k.
    Since k ≤ k(u), ψ must be already active in u. Consider node label ΓA := (Γ(u) \ {ψ}) ∪
{text(u) (φ2 )}, obtained by satisfying ψ already at u, and node label ΓjB := (Γ(w) \ {ψ}) ∪
{text(u)+j (φ2 )}, obtained by satisfying ψ at w. We show that if the subtree rooted at node la-
beled ΓA is rejected, then the subtree rooted at node labeled ΓjB is rejected as well, contradicting
that node w is part of an accepting branch.
    Since the subtree rooted at ΓA is rejected (as it is explored also by the jump tableau),
every branch terminates in a nodes that contains a contradiction, or ¬⊤. Let V be the set of
rejected leaf nodes. For each v ∈ V, let C v ⊆ Γ(v) be a minimal inconsistent subset of atomic
constraints, with C v ̸= ∅.
    Partition C v into Cm   v
                              ∪ Csv , where Cm
                                             v
                                                contains propositions derived from the extracted
target φ2 and Cs those derived from Γ(u) \ {ψ}.
                  v

    If Cmv
           = ∅ the conflict lies entirely within propositions in Γ(u) \ {ψ}, while if Csv = ∅ it lies
entirely within the extracted target propositions. In both cases, conflict would be independent

26
STLSat                                                           Zamponi, Lammel, Bartocci and Chiari


of the time at which the target is extracted, thus would arise in ΓjB as well, and the claim holds.
The case in which rejection is due to ¬⊤ being in Cm   v
                                                          or Csv is also analogous.
     We focus on the remaining case Cm ̸= ∅ and Cs ̸= ∅, and ¬⊤ ̸∈ Cm
                                        v            v                     v
                                                                             ∪ Csv . Choose σ ∈ Csv
and ρ ∈ Cm . Note that the constraints σ and ρ belong to the same minimal inconsistent set
            v

C v , but they are not necessarily pairwise inconsistent.
     We analyze the source of the obstacle proposition σ:

  (i) If σ ∈ Γ(u) has no active parent, then s = (t(u), t(u)) ∈ S(u).
     If ρ ∈ Γ(u), then by Lemma 2 there exists (lρ , rρ ) ∈ T (text(u) (φ2 )) such that lρ = t(u)
     and m = (t(u), rρ ) ∈ M (u). If ρ is not nested into any temporal operator, then m =
     (t(u), t(u)) ∈ M (u).
     Hence the intersection between m and s contains t(u), enforcing a STEP rule due to (2).

 (ii) If σ ∈ Γ(u) has an active parent, we again show that if propositions ρ and σ occur in the
      same leaf v, by Lemma 2 their validity intervals intersect.
     In fact, if ρ is nested into a temporal operator in φ2 , we have m = (lρ , rρ ) ∈ M (u) with
     lρ ≤ t(v) ≤ rρ . If ρ is not nested into any temporal operator in φ2 , then we must have
     t(v) = t(u), and m = (t(u) + 0, t(u) + 0) = (t(v), t(v)) ∈ M (u).
     Moreover, Γ(u) must contain a formula θ such that θ has no active parent, and σ appears in
     θ (considering its identifier). Since θ has no active parent, its validity intervals are included
     in S(u), and by applying Lemma 2 we have s = (lσ , rσ ) ∈ S(u) such that lσ ≤ t(v) ≤ rσ .
     Then {t(v)} ∈ m∩s ̸= ∅, and a STEP rule would be executed, contradicting the possibility
     of making a jump in the first place.

    Since the node labeled with ΓA is also explored by the jump tableau, and by the premise it
is rejected, the node labeled with ΓjB will be rejected too contradicting the assumption that w
is part of an accepting branch of the basic tableau and proving the theorem.

Corollary 6. The JUMP rule with the distinct-variable optimization (§4.3.2) is sound and
complete.

Proof (sketch). The claim follows from the proofs of Theorems 4 and 5 and the following ob-
servations:

   • Local inconsistencies in node labels are checked only among literals, i.e., atomic propo-
     sitions in positive or negated form. If such propositions are Boolean variables, their
     conjunction may only be unsatisfiable if the same variable appears both in positive and
     negated form. Thus, two such literals that contain different variables or are the same
     literal may never cause a node to be rejected by the local consistency check.

   • If a node contains real-valued constraints, it might be the case that, although two con-
     straints do not share any variables, their conjunction with a larger set of constraints is
     unsatisfiable. In this case we use the fact that, if a set of constraints is unsatisfiable, then
     at least two of them must share a variable.
     Suppose, by contradiction, that the tableau that uses the optimization has an accepting
     branch, and the one without it has none. Let v be a node that appears only in the unopti-
     mized tableau and is rejected due to a contradiction. Node v must descend from a poised
     node u in which the guard (1) allows the JUMP rule only when using the optimization,
     or the ksound
             ∗
                   (u) limit is larger when using the optimization, thus allowing for a longer

                                                                                                   27
STLSat                                                            Zamponi, Lammel, Bartocci and Chiari


       jump. However, since v is rejected, Γ(v) must contain two real-valued constraints ρ and
       σ that share the same variable. Let φ, ψ ∈ Γ(u) be the two formulas from which ρ and σ
       respectively derive. By Lemma 2, both T (φ) and T (ψ) must contain a validity interval
       that includes t(v). This can be easily shown to contradict the fact that the optimized
       tableau jumps when the unoptimized does not, or that it makes a longer jump.
       A similar argument can be made for completeness along the lines of the proof of Theorem 5.




C       Random Benchmark Generation
The Random-STL and Random0-STL benchmark suites were generated using a stochastic re-
cursive expansion algorithm. The generator is implemented in Rust using the set of functions
provided by the formula module of the STLSat tool.

C.1      Generation Algorithm
The generator produces formulas whose satisfiability is not known beforehand and is ultimately
determined by the solving engines. A formula is created as the conjunction of j independently
generated sub-formulas. Each of these sub-formulas is produced by a recursive function.

Recursive Generation The generation of a branch is terminated once an atomic proposition
is selected (as it has no children). The average formula depth is controlled by a parameter
pstop_base , representing the probability of selecting an atomic proposition. This probability
grows linearly with the current tree depth d such that Pstop = min(1, pstop_base × d).

Temporal Operator Whenever the recursion continues, the algorithm selects between a
temporal or a non-temporal operator based on a parameter ptemp . Whenever a temporal oper-
ator is selected, the operator is chosen uniformly from the set {F, G, U, R}. The corresponding
interval I = [a, b] is computed to ensure the global temporal horizon is not exceeded. Let h
denote the current accumulated horizon at the given tree depth, l the maximum global horizon
parameter, and i the maximum allowable interval length parameter. The maximum permissible
time interval length is ∆max = min(i, l − h).
    For the Random-STL benchmark, the interval I is generated by selecting one of three modes
with equal probability:
     • a = 0, and b ∼ U(0, ∆max ).
     • a ∼ U(0, ∆max ), and b ∼ U(a, ∆max ).
     • a ∼ U(0, ∆max ), and b = l − h.
For the Random0-STL benchmark, the generation enforces the first mode (with a = 0 for all
temporal operators).

Atomic Proposition When an atomic proposition is selected, it is sampled from a pre-
generated pool of c constraints. These constraints operate over the real variables S = {x1 , . . . , xr }
and can take three forms, which are selected uniformly:
     1. Simple Bounds: xi ▷◁ k.

28
STLSat                                                         Zamponi, Lammel, Bartocci and Chiari


  2. Difference Logic: xi − xj ▷◁ k for i ̸= j.
  3. Linear Constraints:    x∈S ′ x ▷◁ k, where S ⊆ S is a randomly selected subset.
                                                 ′
                          P

The relation ▷◁ is sampled from {<, ≤, >, ≥, =, ̸=}, while the constant k is a randomly generated
rational number.

C.2      Parameter Space and Suite Configuration
The Random-STL suite was generated by sweeping across all combinations of the parameter
space. Table 5 presents the set of possible parameter values for each defined parameter. For
each combination of parameters, 5 formulas have been generated, for a total of 2000 formulas.
The Random0-STL variation uses identical parameter space value combinations but restricts
all generated temporal operator intervals to the form [0, b], as detailed in the previous section.

                Parameter                        Values Sampled
                Real Variables (r)             {5}
                Real Constraints (c)           { 10 }
                Max Horizon (l)                { 100, 500, 1000, 5000, 10000 }
                Max Interval Length (i)        { 50, 1000 }
                Stop Probability (pstop_base ) { 0.05, 0.1, 0.15, 0.2, 0.25 }
                Temporal Probability (ptemp ) { 0.33, 0.5, 0.75, 0.95 }
                Conjunctions (j)               { 5, 10 }

                     Table 5: Parameter space for STL benchmark suites.




                                                                                                29
