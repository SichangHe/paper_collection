                                                            Theory-Scale Auto-Formalization of
                                                               Logics for Computer Science


                                                            Yuming Feng                                  Frederick Pu
                                                       Johns Hopkins University                       University of Toronto
                                                        yfeng97@cs.jhu.edu                      frederick.pu@mail.utoronto.ca
arXiv:2606.26525v1 [cs.LG] 25 Jun 2026




                                                      One An                         Osbert Bastani                      Li Zhang
                                             University of Pennsylvania         University of Pennsylvania            Drexel University
                                              onean@sas.upenn.edu              obastani@seas.upenn.edu            harry.Zhang@drexel.edu

                                                     Jiani Huang                           Xujie Si                       Ziyang Li
                                               University of Pennsylvania            University of Toronto         Johns Hopkins University
                                               jianih@seas.upenn.edu                six@cs.toronto.edu               ziyang@cs.jhu.edu



                                                                                         Abstract
                                                     Auto-formalization is critical for scalable formal verification, but existing progress
                                                     largely focuses on isolated statements, while theory-scale auto-formalization,
                                                     which coherently translates hundreds of interdependent definitions, lemmas, and
                                                     theorems, remains open due to challenges in consistency, faithfulness, scalability,
                                                     and correctness. In this paper, we introduce LCS-Bench, a stand-alone, theory-scale
                                                     benchmark based on Logics for Computer Science. LCS-Bench is built through
                                                     a novel semi-automated agentic pipeline that leverages concept graphs, formal
                                                     signature planning, issue tracking, sorry-filling with counter-example search, com-
                                                     plemented by faithfulness review from human experts. The resulting artifact covers
                                                     327 textbook items, over 4,076 Lean declarations, and more than 85K lines of Lean
                                                     code. The dataset supports broad evaluation through a data engine that automati-
                                                     cally derives five tracks of evaluation benchmarks, measuring different aspects of
                                                     auto-formalization and theorem-proving capabilities. We also introduce a novel
                                                     evaluation protocol featuring definitional equivalence checkers, enabling more
                                                     fine-grained and faithful assessment. Through extensive evaluation on 14 models,
                                                     we demonstrate that (1) LCS-Bench is of high quality, consistent, and faithful; (2)
                                                     the benchmark is challenging, with state-of-the-art models achieving only 20.1%
                                                     on auto-formalization tasks; and (3) our analysis reveals key findings regarding
                                                     theory-scale auto-formalization and suggests promising directions for future work.


                                         1    Introduction
                                         Auto-formalization, the translation of informal mathematics and logic into machine-verifiable state-
                                         ments and proofs, has become a central problem at the intersection of AI and formal methods [1–4].
                                         Despite recent progress, theory-scale auto-formalization remains largely unsolved: real mathematical
                                         theories require hundreds of interdependent definitions, lemmas, and theorems to be formalized as
                                         a coherent whole. This setting raises fundamental challenges in maintaining global consistency,
                                         preserving faithfulness to the source text, and producing artifacts that are not only syntactically
                                         valid but also formally provable. Progress is further limited by the lack of tailored benchmarks and
                                         evaluation protocols, as many existing evaluations rely heavily on mature libraries such as Mathlib [5],
                                         obscuring the difficulty of building theories from first principles.

                                         Preprint.
                                                                                                IAF Track: Item-Level Auto-Formalization
                                                           LCS                                   Textbook Item         Context     Skeleton   Answer
                              CutElim                ...
                                                     397 @[lcsitem chap7__theorem_7_4_2]
                              FirstOrder             398 theorem sharpenedHauptsatz_G2nnfEq
                              Herbrand               399   {L: Language} [DecidableEq (Formul          …                 …           …             …
                                                     400   (seq : Set (FormulaN L) × Set (For   SSAF Track: Subsection-Level Auto-Formalization
                                HerbrandTheorem      401   (hAllNNF : allFormulaeNNF seq)        Textbook Subsection     Context   Skeleton   Answer
                                NNFHauptsaz          402   (hProv : G1nnfEqProvable seq) :              …                  …         …             …
                                                     403   ∃ (T : G2nnfEqProofTree L)           ITP Track: Item-Level Theorem Proving
                                    Equality.lean    404     (mid : Set (FormulaN L) × Set (F
                                                                                                  Textbook Item & Proof             Lean Context
                                    Soundness.lean   405     T.conclusion = seq ∧ T.WellForme
                                                     406     IsPureVariableProof_G2nnfEq T ∧
                              SLD                    407     hasNoEssentialCuts_G2nnfEq T ∧ …
                        ,,,                          ...                                                   …                             …
      Textbook                                         Lean Repository                                        Benchmark Datasets

Figure 1: An overview of LCS-Bench. Tracks of datasets are generated from the Lean repository
derived from the textbook, covering a wide range of auto-formalization and theorem-proving tasks.

Existing auto-formalization benchmarks fall short of this setting in scope, coverage, and self-
containment. Most focus on isolated statements rather than full developments with heterogeneous
artifacts, such as definitions, lemmas, theorems, proofs, algorithms, and exercises [6–11]. Others
either do not require formally verified proofs, as in PutnamBench [12], or are built on substantial
pre-existing infrastructure, as in LeanDojo [13] and miniCTX [14]. As a result, current evaluations
do not adequately capture theory-scale auto-formalization. We therefore seek a benchmark for Lean
that is theory-scale, stand-alone, and heterogeneous, covering a broad spectrum of formalization tasks
within a single coherent development.
Figure 1 illustrates the overall design of LCS-Bench, where we turn the textbook into a Lean repository
and then derive evaluation tracks from it. To realize this goal, we start constructing our benchmark
from Logics for Computer Science: Foundations of Automatic Theorem Proving, Second Edition
[15]. We choose this text because it is self-contained, comprehensive, and centered on core topics
in logic for computer science, spanning propositional logic, first-order logic, theorem proving, and
logic programming including Prolog. Beyond theorems and proofs, it contains rich structural content
such as domain-specific languages, deeply embedded proof trees, algorithms, and meta-theory, which
are largely absent from prior auto-formalization benchmarks. LCS-Bench therefore broadens auto-
formalization from isolated mathematical statements to heterogeneous, theory-scale developments
common in computer science.
From this source, we build a large-scale Lean repository through a semi-automated, expert-in-the-loop
formalization pipeline. The pipeline combines concept graph construction, formal signature planning,
automated sorry-filling with counter-example search, and issue tracking, with expert intervention
resolving unfaithfulness and formalization gaps. The resulting repository formalizes essentially the
full technical content of the textbook, covering eight chapters, yielding 341 textbook items, 4,076
Lean declarations, and 85K lines of Lean code, including 28K lines of proof; of which 327 items
enter the benchmark. We aim to prove every theorem and lemma, and achieve this for 55% of them;
the remaining cases are primarily mechanically demanding meta-theorems, such as termination and
completeness results, whose formalizations are validated by human experts.
Operating on the codebase, we build a data engine that automatically derives five evaluation tracks:
three auto-formalization (AF) tracks, Item-level AF (IAF), Subsection-level AF (SSAF), and IAF
with Distractors (IAF-D), and two theorem-proving (TP) tracks, Declaration-level TP (DTP) and
Item-level TP (ITP), totaling 1,271 benchmark instances. Each instance provides sufficient context for
theory-scale reasoning and is designed to test coherence across related declarations rather than isolated
statement translation. For evaluation, we introduce a novel definitional equivalence checker, which
supports fine-grained assessment of type definitions and declarations beyond logical equivalence
alone. The resulting dataset is challenging: even item-level instances require formalizing multiple
heterogeneous declarations within a rich theory-scale context. In summary, our contributions are:
1. We introduce and responsibly release LCS-Bench1 , a comprehensive, stand-alone, and challenging
   benchmark for theory-scale auto-formalization based on Logics for Computer Science [15].
2. We develop a semi-automated agentic pipeline for benchmark construction, leveraging concept
   graph construction, formal signature planning, sorry-filling with counter-example search, and
   issue tracking, complemented by human expert review.
3. We implement a data engine that generates five evaluation tracks comprising 1,271 data points,
   together with a definitional equivalence checker for fine-grained and faithful assessment.
  1 The anonymous artifact is submitted along with the paper.




                                                                     2
Implicit Assumptions                        @[lcsitem chap3__definition_3_4_a]
                                            inductive PropNorm where
                                             | var : Nat → PropNorm | neg : PropNorm → PropNorm
                                             | conj : PropNorm → PropNorm → PropNorm | disj : ... | impl : ...

Textbook Definition
                                            @[lcsitem chap3__definition_3_4_2]
                                            inductive GentzenStep1 : Sequent → Sequent → Type where
                                             | andLeft (Γ Δ Λ : List PropNorm) (A B : PropNorm) : GentzenStep1
                                                 (Sequent.mk (Γ ++ [A, B] ++ Δ) Λ) (Sequent.mk (Γ ++ [.conj A B] ++ Δ) Λ)
                                             | ...


Textbook Lemma                              @[lcsitem chap3__lemma_3_4_3]
                                            theorem soundness_G (s : Sequent) (h : sequentProvable s) : sequentValid s :=
                                             by obtain ⟨t⟩ := h ↵ exact proofTree_valid t




Figure 2: Illustrative examples in the textbook about Gentzen system G′ (Left) and its formalization
in LCS-Bench (Right). We show one staged implicit assumption in the textbook (“In the rest of this
section, it will be assumed. . . ”), one graphical illustration for Gentzen system definition (horizontal
line-based inference rules), and one soundness theorem about the Gentzen system.

4. By evaluating 14 models in zero-shot, thinking, and agentic modes, we demonstrate the quality
   and difficulty of LCS-Bench and uncover key findings for theory-scale auto-formalization.

2    Illustrative Examples
We start by presenting a few illustrative examples in LCS-Bench (Figure 2). The examples are drawn
from Chap. 3 of the textbook, which formalizes propositional logic and the Gentzen sequent calculus
G′ . Definition 3.4.2 introduces the eight inference rules of G′ , which are presented in the textbook
entirely as a typeset diagram of inference rules, and Lemma 3.4.3 states the soundness of G′ .
Each numbered textbook item is linked to its Lean formalization via the @[lcsitem] attribute,
providing a stable identifier used throughout the pipeline and benchmark. One textbook item typ-
ically corresponds to multiple Lean declarations. Definition 3.4.2 maps to two inductive types
(GentzenStep1, GentzenStep2), and Lemma 3.4.3 maps to a single theorem soundness_G. Sev-
eral features make this example representative of the challenges in LCS-Bench:
1) Theory-scale context. Lemma 3.4.3 transitively depends on 79 Lean declarations across 11
   textbook items, including propositional semantics, sequents, axioms, and proof trees.
2) Graphical definitions. Definition 3.4.2 exists in the textbook only as a diagram of horizontal-line
   inference rules, which must be translated into inductive types forming a deeply embedded DSL.
3) Implicit assumptions. Formalizing sequents requires a separate type PropNorm (full name
   PropFormulaNormalized, shortened here for brevity) than the formal definition of proposi-
   tional formulas, yet this restriction appears only as a prose convention with no labeled definition.
4) Heterogeneous items. Definition 3.4.2 is an inductive type (a DSL); Lemma 3.4.3 is a theorem—
   two fundamentally different Lean constructs arising from the same chapter.
5) Formally proved. soundness_G is fully proved, reducing to case analyses over all eight inference
   rules. LCS-Bench contains proofs of individual declarations reaching up to 1,600 lines.
These examples yield tasks for two tracks. In the auto-formalization track, a model receives the
textbook text for Definition 3.4.2 (including the graphical rules) together with all dependency context,
and must produce the two inductive types that faithfully embed the rule system. In the theorem-
proving track, a model receives the statement of soundness_G and the full Lean context, and must
fill in the proof, which requires reasoning about valuations, sequent validity, and all eight rule cases.
Notably, these examples are drawn from Chap. 3, the first technical chapter after mathematical
background. The textbook subsequently covers proof search algorithms, first-order logic, Herbrand’s
theorem, resolution, and SLD resolution for Prolog, each introducing new DSLs, meta-theorems, and
algorithmic content of increasing complexity.

3    Methodology
We now describe the semi-automated agentic pipeline for converting the textbook into a validated,
high-quality Lean library, which we call the LCS-Bench Lean artifact. The pipeline consists of four
stages illustrated in Figure 3: pre-processing, formalization planning, Lean implementation, and


                                                     3
   Preprocessing     Formalization Planning           Lean Implementation                 Formal Correctness Review
                            Concept Graph            Inductive Type Definitions                      Sorry Filling
                                                 @[lcsitem chap3__definition_3_2_2]
                      Literal                    inductive PropForm where                     …   by -- BEGIN PROOF
                                       Sequent                                                     injection h with        …
                                                  | var : Nat → PropFormula
                                                                                                   h1 h2; exact ⟨h1, h2⟩
                         Clause                   | fls : PropFormula | ...


                        …       clause_valid      Concept Definition & Examples           Completeness           Triage &
                                                 @[lcsitem chap3__example_3_2_1]          Preservation          Decompose
                                                 def exNegEquivImplFls : PropFormula :=
    chap3/            Formal Signature Graph      PropFormula.equiv_
                                                   (PropFormula.neg (.var 1)) (....fls)
    chap4/
                       PropForm                                                                    Counter-example
     4.2.1.Def…md                                        Theorem & Lemma                  …                                 …
                        kind: inductive          @[lcsitem chap3__theorem_3_2_1]
                                                                                                      Searching
     4.2.2.Sou…md       constructors             theorem prop_neg_inj (A B: PropForm)
                                                  (h : PropForm.neg A = PropForm.neg B)              ∀        ∃¬
    chap5/                name: var; type: …      : A = B := by sorry



Figure 3: Overview of the LCS-Bench formalization pipeline, which consists of four stages from
preprocessing to planning, implementation, and formal correctness review.

formal correctness review. The primary models used in the pipeline are Claude Opus 4.6 [16] and
GPT 5.3 [17], accessed via Claude Code and Codex CLI respectively, used in conjunction with each
other in agentic mode. Further details are provided in Appendix A.
Pre-Processing. To ensure each formalization target is explainable and precisely traceable, we
preprocess the textbook into a structured, item-level representation. We convert the textbook from
PDF to Markdown with Marker [18], one file per subsection, and manually redraw eligible graphics,
such as proof trees, inference rules, and directed acyclic graphs, as ASCII diagrams embedded in
the Markdown. Each textbook item is wrapped in a typed XML tag, such as <theorem>, <lemma>,
<definition>, <example>, or <proof>. We also manually annotate implicit formal statements
expressed in prose, including scope restrictions, standing assumptions, and informal lemmas.
Formalization Planning. Before any Lean code is implemented, an agent analyzes the textbook’s
mathematical structure and generates a two-layer intermediate representation (IR) blueprint for
faithful, self-contained formalization. First, we generate a textbook-self-consistent concept graph:
nodes are keywords or sub-clauses from the text (e.g., “propositional formula”, “left parenthesis
count”, “disjoint antecedent and succedent”), and edges encode textbook-level relationships such as
IS - A, HAS - A, RELIES - ON, and DEFINED - BY. Second, we generate a formal signature graph that maps
each concept node to its Lean realization, including its lean_kind, constructors, fields, companion
definitions, and embedding level. The embedding level is deep for syntactic DSLs encoded as
inductive types, shallow for semantic properties over deep syntax using Lean’s Prop layer, and mixed
for meta-theorems connecting the two, such as soundness, completeness, and termination. Critically,
the embedding level must be assigned correctly so that deep syntactic constructs are available as
first-class inductive types when the agent later states meta-theorems about them.
Lean Implementation. Given the informal concept graph and the formal signature graph, an agentic
implementer translates each module into Lean code, proceeding in three rounds that respect the
dependency order established in the planning stage. After each round, lake build is run and a
review script verifies correctness and faithfulness to the signature graph.
• Round 1: Structures and inductive types. The agent first defines all inductive types and
  structures, which form the backbone for later definitions and theorems. Each Lean declaration
  is tagged with @[lcsitem] encoding the stable item ID; the lcsmain flag marks the primary
  authored declaration, distinguishing it from companion definitions and elaboration byproducts.
• Round 2: Definitions, functions, and examples. Given the type scaffolding, the agent defines
  functions, abbreviations, instances, and examples, including computational content (e.g., evaluators,
  normalizers, search procedures) and semantic predicates (e.g., validity, satisfiability, tautology).
• Round 3: Theorems and lemmas. The agent writes theorem and lemma statements drawn directly
  from the formal signature graph, leaving all proof bodies as sorry placeholders. The goal is theory-
  scale coherence: all statements type-check, all dependencies compile, and the overall structure
  faithfully mirrors the textbook. An implementation validator flags vacuous theorem statements,
  missing inductive cases, identity-function stubs, and dead @[lcsitem] declarations.
Formal Correctness Review. This stage fills sorry placeholders and checks that proofs are both
formally correct and faithful to the textbook. When proof search stalls, the pipeline performs
counterexample search by attempting to prove the negation of the statement, distinguishing difficult


                                                       4
                                            Initial Formalization                     After Intervention
                                       | allRight (y : Nat)                   | allRight (y : Nat)
                                          (Γ Δ Λ : List (FormulaN L))            (Γ Δ Λ : List (FormulaN L))
              (… Many other rules …)      (x : Nat) (A : FormulaN L) :           (x : Nat) (A : FormulaN L)
               …                                                                 (hfresh : ∀ F ∈
                                                                                   (Sequent.mk Γ (Δ ++ [all x A]
                                                                                     ++ Λ)).antecedent ++
                                             Missing side                          (Sequent.mk Γ (Δ ++ [all x A]
               …                              condition                              ++ Λ)).succedent,
                                                                                   y ∉ formulaFVN F)
                                                                                 (hfreeFor: isFreeForN (var y) x A) :
                                       GentzenStep1                              GentzenStep1
                                        (Sequent.mk Γ (Δ ++                       (Sequent.mk Γ (Δ ++
                                         [formulaSubstN A (var y) x] ++ Λ))        [formulaSubstN A (var y) x] ++ Λ))
                                        (Sequent.mk Γ (Δ ++                       (Sequent.mk Γ (Δ ++
                                         [FormulaN.all x A] ++ Λ))                 [FormulaN.all x A] ++ Λ))



Figure 4: A concrete example of human expert intervention. The (∀:right) constructor is initially
formalized without the textbook’s two side conditions (the eigenvariable condition and the free-for
condition), yielding a rule that Lean accepts but that admits unsound inferences.

true statements from subtly incorrect ones. A high-level orchestrator tracks remaining issues, triages
them by severity, decomposes stuck proofs into subgoals, and triggers a mandatory three-way review
once a theorem is claimed resolved, comparing the final Lean declaration against the textbook, the
formal signature graph, and the implementation history.
Human Expert Intervention. The automated pipeline handles the bulk of formalization, but human
expert intervention is essential for issues requiring global judgment or resolution of genuine ambiguity.
Human experts invested approximately six person-months, contributing 190K tokens of feedback
across 600+ tracked issues, alongside significant direct rewrite of roughly 30% of major definitions,
implicit assumptions, and core theorems. To further alleviate code-smells from few driving models,
the main naming and stylistic conventions are all set by human experts. Other than these, the primary
categories of failures demanding interventions are:
1. Missing standing assumptions. Textbook assumptions may be introduced far from where they are
   used, with either broad or local scope. Agents relying on immediate context often miss or dismiss
   them, producing theorems that become unprovable only in later proof attempts.
2. Vacuous formalization. The Lean statement may diverge from the textbook even when its type-
   level spec appears correct. A common failure is signature drift toward an overly loose statement,
   admitting unintended witnesses and making downstream lemmas trivially provable but unfaithful.
3. Accumulated workarounds on a false foundation. When an agent inherits a declaration whose
   statement is already wrong, subsequent agents patch around it rather than fixing it, trading
   faithfulness for the effort of a proper rewrite. Over time this compounds into rippling unfaithful
   statements built on top of a false claim, requiring a full revert of the dependent chain.
Figure 4 shows a false foundation that triggers accumulated workarounds. Due to the length of
Definition 5.4.1, one side condition (eigenvariable) appears at the very end, so the agent omitted it in
the initial formalization, and earlier checks failed to catch the error. During the proof of a subsequent
theorem, the agent repeatedly failed to close the cases generated by this rule, unable to tell whether
the proof was hard or the definition was wrong. At this point, a human expert can step in and use
dependency analysis to identify and correct the missing side condition.
In all cases, the human expert’s role is to review, identify, and resolve the issue at the source. Human
experts often significantly rewrite the statement and channel it back to re-implement and re-prove
downstream from stage 2 or 3, ensuring that the fixes are properly propagated.


4   Benchmark and Datasets

LCS-Bench organizes evaluation datasets into five tracks spanning two task families: auto-
formalization (AF) and theorem-proving (TP). Across all tracks, there are 1,271 data points in
total. Table 1 and Table 2 summarize the track statistics including the lines-of-code (LoC) and
number of Lean declarations (#Decls). Further details are provided in the Appendix B.
Auto-formalization tracks. Each AF data point provides a context of existing Lean code and
textbook content and asks the model to produce a submission.lean containing the formalized


                                                            5
                                      Input LoC           #Output Decls                                                     Input LoC        GT Output LoC
  Track             #Points                                                              Track      #Points
                                      Mean         Max    Mean       Max                                                    Mean      Max     Mean         Max
  IAF                    327         359.37       1559     6.49           57             DTP             420               383.26     1799    38.57         480
  SSAF                   116         428.05       1551    18.21           93             ITP              81               300.96      845   138.85         608
  IAF-D                  327        1383.30       4951     6.49           57             –                 –                    –        –        –           –

Table 1: Dataset statistics for the three AF tracks.                                    Table 2: Dataset statistics for the two TP tracks.

   100                                   Formalized       180            Formalized     Non-formalized
                         89                                                                                               103
                                         Non-formalized




                                                                                                          GT output LoC
         80    71
                                                          150      129
#Items




         60                         54
                                                          120                           109
                               41                          90                                  87                         102
         40                               29
                                               35 32
                    25                                     60                  51
         20                                                30
                                                                                                                          101
          0                                                 0
               3     4   5     6     7     8   9 10                Def       Thm        Lem    Ex                               101          102           103
                                                                                                                                       Input context LoC
              (a) Count by chapter.                             (b) Count by item type.                   (c) Distribution of output/input LoC.
Figure 5: IAF track statistics. We show the number of textbook items by chapter, item type, and by
input or output sizes (LoC). The bars are stacked to show the portion of formalized items (darker) vs.
non-formalized items from the textbook (faded).

declarations. IAF (Item-level Auto-Formalization) is the atomic unit: one textbook item per data
point. SSAF (Subsection-level) scales up the output, requiring the model to jointly formalize all items
in a subsection. IAF-D (IAF with Distractors) injects semantically related but irrelevant declarations
into the context to test robustness to redundant information.
Each AF data point is a quadruplet (Q, C, Ty , y): a textbook quote Q, a context C of dependent
Lean declarations, a starter template Ty with declaration skeletons, and a ground-truth y. A model
receives (Q, C, Ty ) and produces ŷ, a Submission.lean file. For evaluation, we propose a novel
DefEq Checker, a Lean program that checks definitional equivalence between y and ŷ. No existing
metric handles the heterogeneous declaration kinds present in our dataset (constants, definitions,
theorems, inductives, and constructors). Table 3 summarizes the checker’s coverage, with full details
and checker algorithm in Appendix C.
Figure 5 provides detailed per-chapter, per-type, and input/output LoC-distribution breakdowns for
the IAF track. We focus on IAF because it is the most fine-grained AF track and thus the most
representative lens into the distribution; the other AF tracks are scaled-up composites built from the
same atomic items. Notably, Figure 5a shows that LCS-Bench covers a vast majority of the textbook:
86% of all textbook items across chapters 3–10 are formalized and included in the benchmark.
Theorem-proving tracks. Each TP data point provides Lean source with sorry placeholders and
asks the model to fill them within an interactive budget. DTP (Declaration-level Theorem Proving)
targets a single sorry-bearing declaration. ITP (Item-level Theorem Proving) scopes to a full
textbook theorem or lemma and requires all its sorrys to be filled jointly, with helper declarations
left unconstrained. As shown in Table 2, of the 145 formalized theorems and lemmas, 81 have fully
machine-verified proofs and constitute the TP tracks’ data-points. The size of the ground truth proofs
is illustrated in Figure 6 as a measurement of the TP tracks’ difficulty distribution.
Each TP data point is also a tuple (Q, C, Ty , y): a textbook item Q, a context C, a target Ty containing
the declaration(s) to prove with their theorem bodies replaced by sorry, and a ground-truth y with
complete proofs. For DTP, Ty is a single sorry-stubbed declaration, often a decomposed helper not
directly corresponding to Q, so the model receives only (C, Ty ). For ITP, Ty spans every declaration
of the textbook item with all theorem bodies sorry-stubbed (other declarations kept intact), and
the model receives (Q, C, Ty ). In both cases, the model produces ŷ, accepted when all expected
declarations are present, no sorry remains, and no new axiom is introduced.
Data Engine. We develop a data engine that performs systematic dependency analysis and Lean
code modification to automatically generate all evaluation tracks from the LCS-Bench artifact. This
process is AI-free: whatever is stabilized in the artifact is faithfully used to derive the datasets. For AF
tracks, the engine fetches all dependencies, strips proofs, and composes them into a compact context
C while generating Ty and y. IAF-D is produced by additionally injecting distractor declarations. For


                                                                                    6
     Kind                   Compared                       Criterion                                    20                   20
                                                                                                                                        18
                                                                                                                                              20




                                                                                                   #Items
     Definition             Body expr.                     IS D EF E Q or GRIND                                                                     13
     Theorem                Statement type                 IS D EF E Q or GRIND                         10
                                                                                                                                                             6
     Inductive              Constructor names              Same set (order-independent)                                4

     Constructor            Constructor type               IS D EF E Q only                                 0
                                                                                                                 <25 25–49 50–99 0–199 0–399 ≥400
                                                                                                                               10    20
Table 3: Equivalence criteria used by the DefEq Checker.                                          Figure 6: #ITP items by GT output LoC.
                30
                        Zero-shot        Thinking              Agentic
                25
Pass rate (%)




                                                                                                                            20.1
                20     16.8                                               17.917.6                                                 18
                           15.4 15                                                16.315.5                                              16.115.3
                                     13.9                                                 14.4                                                  14.7
                15                                                                                                                                  12.1
                                         11.1
                                                9.5   9   8.4 7.6                                9.1
                10
                                                                                                       5.4 4.2                                             5.5
                5                                                   3.1                                          2.5                                             2.1
                0
                      G 6
                          54

                      G 6
                            5
                          45

                           2
                          25

                                                           2
                                                                 L4
                                                                3C



                                                                                46

                                                                                46

                                                                          G 54
                                                                               SS

                                                                           M 5

                                                                           G 5
                                                                                 5

                                                                                 1
                                                                               32



                                                                                                                               46

                                                                                                                           G 6
                                                                                                                               54

                                                                                                                                                25

                                                                                                                                             M 5
                                                                                                                                                25

                                                                                                                                                      PT 2
                                                                                                                                                         SS
                          4



                          4
                        LM



                         S3



                                                          D




                                                                               2

                                                                                2
                                                                             LM

                                                                              SR




                                                                                                                               4




                                                                                                                                              LM



                                                                                                                                                          3
                       CO

                       PT
                       CS


                       CH



                        K




                                                                            CS
                                                                            CO

                                                                            PT



                                                                              K
                                                                             M




                                                                              Q


                                                                                                                            CO

                                                                                                                            CS

                                                                                                                            PT

                                                                                                                                              K


                                                                                                                                              M

                                                                                                                                                        Q
                                                                             O




                                                                                                                                                        O
                                                               Q
                       D




                                                                            D
                                                                           PT




                                                                                                                                              G
                                                                           G




                                                                                                                                                         G
Figure 7: IAF pass rate (%) per model, averaged over three runs, grouped by evaluation mode (zero-
shot, thinking, agentic). Error bars show ±1 standard error of the mean (SEM) across timestamps.

TP tracks, the engine removes proof bodies to produce C and generates a data point only when the
full dependency tree is proved, so partially-proved declarations in the current artifact are excluded.


5                Evaluation

5.1                  Evaluation Setup

Models. We evaluate 14 models spanning both proprietary and open-sourced families. The proprietary
models are Claude Opus 4.6 (CO46), Claude Sonnet 4.6 (CS46), Claude Haiku 4.5 (CH45) [16],
and GPT-5.4 (GPT54) [17]. The open-sourced models are DeepSeek R1 [19] (DSR1), DeepSeek
V3.2 [20] (DS32), Kimi K2.5 [21] (K25), Devstral 2-123B [22] (D2), Llama 4 [23] (L4), Qwen 3
Coder [24] (Q3C), Qwen V3.2 [25] (Q32), MiniMax-M2.5 [26] (MM25), GLM-5 [27] (GLM5), and
GPT-OSS-120B [28] (GPTOSS).
Modes. Depending on each model’s capabilities, we apply it in up to three modes: (i) zero-shot,
direct output without thinking; (ii) thinking, with extended reasoning enabled; and (iii) agentic,
running within an agent loop under a fixed budget on the number of turns. The agentic framework is a
lightweight SWE-agent-style scaffold based on mini-swe-agent [29], with three custom tools exposed
to the model: file read/write, lake build (for compilation checking, optionally also verifying the
absence of sorry), and a submit action that finalizes the model’s output. We allow up to 20 turns
for IAF and IAF-D, 64 for SSAF, and 20 for DTP and ITP.
Track coverage. As LCS-Bench is primarily an auto-formalization benchmark, we focus our
evaluation on the IAF track, running all 14 models across all three applicable modes; results for the
remaining tracks are reported alongside. For IAF-D, we adopt the same setup as IAF. For SSAF, DTP,
and ITP, the excessive context length and per-item difficulty render zero-shot and single-turn thinking
modes ineffective, so we report agentic-mode results only.

5.2                  Research Questions and Findings

RQ1: Can current LLMs auto-formalize Logics for Computer Science? Current models fall well
short of saturation on every track. As shown in Figure 7, the best IAF pass rate is 20.1%, achieved by
Claude Opus 4.6 in agentic mode; the weakest model scores only 2.1%. Because we repeat each IAF
evaluation three times, the standard errors are consistently small (error bars in Figure 7), confirming
that the rankings faithfully reflect model capability. Enabling extended thinking or an agentic loop
provides a modest but consistent lift over zero-shot, yet the absolute numbers remain low. We further
note that, as shown in the evaluation, circular evaluation is not a big concern as Claude Opus 4.6
and GPT 5.4 are only outperforming the other models by a small margin, and the models’ correct
outcomes are mostly overlapping, as detailed in the Appendix B.


                                                                                   7
                          30                        Zero-shot   30         Zero-shot         Thinking                                                  DTP / CO46              ITP / CO46
                                                    Thinking               Agentic                                                                     DTP / CS46              ITP / CS46




                                                                                                                          Proof rate (%)
                                                                                                                                           100

Pass rate (%)
                                                    Agentic                                                                                            DTP / K25               ITP / K25
                          20                                    20                                                                         80
                                                                                                                                           60
                          10                                    10                                                                         40
                                                                                                                                           20
                           0                                    0                                                                           0
                                3   4   5   6   7   8   9 10         Def       Ex      Lem                   Thm                                 1      5          10          15          20
                          (a) Pass rate by chapter.              (b) Pass rate by item kind.                              Figure 9: Cumulative proof rate vs. #
Figure 8: IAF pass-rate breakdowns by chapter and item kind                                                               turns for DTP and ITP, across three
across three inference modes.                                                                                             models: CO46, CS46, and K25.

                          100
Pass / Compile rate (%)




                                    Zero-shot        Thinking                                                20     −2.7                                                 IAF         IAF-D
                          80        Agentic                                                                                   −2.2
                                                                                                                                             −3.2




                                                                                             Pass rate (%)
                                                                                                             15
                          60                                                                                                                         −1.3
                                                                                                                                                            −2.2 −2.0
                                                                                                             10                                                         −0.8 −1.2
                          40
                                                                                                              5                                                                     +0.3
                          20
                           0                                                                                  0
                            CO46
                            CH46
                              K5
                             D 25
                                 2
                            G D2
                                 5
                              Q 4
                               3C

                            CO25
                             CS46
                            M 46
                              Q5
                            D 32
                            G SR1
                                 5
                            G 46
                              K5
                             C 25
                            M S46
                              Q5
                               32




                                                                                                                     46


                                                                                                                                      6

                                                                                                                                      5

                                                                                                                                     45


                                                                                                                                                           2

                                                                                                                                                                 25


                                                                                                                                                                         2

                                                                                                                                                                               L4

                                                                                                                                                                                     3C
                                4
                              S3
                             LM
                               L




                                2

                             LM


                             LM



                                2




                                                                                                                             4

                                                                                                                                   LM




                                                                                                                                                        S3




                                                                                                                                                                        D
                             CS




                              K


                              M




                            CO



                              M




                                                                                                                   CO

                                                                                                                          CS




                                                                                                                                  CH




                                                                                                                                                                K




                                                                                                                                                                                    Q
                                                                                                                                                        D
                                                                                                                                  G
Figure 10: SSAF results per model-mode. Each Figure 11: IAF vs. IAF-D pass rates per model
stacked bar shows the pass rate (bottom, solid) under zero-shot mode. Injecting distractors con-
and the additional compile-only rate (top, faded). sistently degrades pass rate.

RQ2: How does performance vary with textbook difficulty? Figure 8 decomposes IAF pass rates
by chapter and by item kind. Chapter-wise (Figure 8a), models perform best on Chapters 3 and 5, the
foundational chapters on propositional and first-order logic. Performance drops sharply to near 0%
on Chapters 7–8, which cover Gentzen’s Sharpened Hauptsatz, Herbrand’s theorem, and resolution,
demanding much deeper abstract reasoning. By item kind (Figure 8b), definitions are one of the
easier categories, while examples and theorems lag behind, consistent with the intuition that theorems
require more nuanced reasoning to construct a logically valid statement.
RQ3: Can LLMs do theorem proving for LCS? As shown in Figure 9, Claude Opus 4.6 reaches a
74.5% proof rate on DTP within 20 agentic turns. While a strong result, it is partly attributable to
DTP’s design: each goal is a bite-sized sub-problem decomposed from larger proofs, and the proof
steps are largely mechanical. ITP is harder, demanding long-context reasoning over full proof states,
yet Opus 4.6 still reaches 33.3% at T =20 with no clear plateau, suggesting further gains are likely.
RQ4: How does performance react to theory-scale setups? Scaling up the formalization context
exposes a sharp capability gap. Figure 10 reports results on SSAF, where each item is a full textbook
sub-section averaging 2.82 items. Pass rates collapse to single digits for all models. While adopting
an agentic framework raises the compilation rate, it does not translate into a pass-rate gain, suggesting
the agentic loop helps surface syntax errors but cannot fix semantic mismatches. On IAF-D, adding
distractors consistently degrades pass rates across all models (Figure 11), even though the intrinsic
difficulty of the target item is unchanged. This reveals that current models struggle to identify the
critical information within a longer context, which is a prerequisite for theory-scale auto-formalization
where relevant definitions are always embedded in the surrounding material.
RQ5: Does test-time compute drive better formalization? Figure 12a shows that, in thinking
mode, incorrect outputs are associated with substantially more reasoning tokens than correct ones.
Models that fail tend to “overthink” rather than converging. High-performing models (Claude Opus
4.6, Sonnet 4.6, GPT-5.4) consistently use fewer reasoning tokens than lower-performing ones, yet
produce better results. The same pattern holds in agentic mode (Figure 12b): top models succeed
or fail decisively in fewer turns, while weaker models burn more interactions. Together, these
observations suggest that scaling test-time compute alone is not a viable path to auto-formalization
and that progress demands deeper innate capability.
RQ6: What causes formalization failures? Figure 13 breaks down error types. Even in agentic
mode, only the strongest model eliminates compilation failures; weaker models still struggle with
compilation. Among compiled-but-failed submissions, the overwhelming category is NMExpr (non-


                                                                                        8
                                      Correct Answers       Incorrect Answers                                    Correct Answers             Incorrect Answers
                     30k                                                                           20

# Reasoning Tokens
                     10k
                      5k                                                                           15




                                                                                         # Turns
                      1k                                                                           10
                     500
                     100                                                                            5
                                                                                                    1
                                6     46  54 SS K25 M25 LM5 SR1 Q32                                         46     46  54   SS           5      25 LM5         2
                             O4     CS GPT PTO                                                          CO       CS GPT PTO            K2                    Q3
                            C
                                          G        M   G   D
                                                                                                                       G                     MM   G
                           (a) Thinking: reasoning tokens per attempt.                                       (b) Agentic: turns per attempt.
Figure 12: Violin plots showing the relationship between test-time compute vs. correctness on IAF.

   CO46 (AG)                                                            References a figure                −0.161
   GLM5 (AG)
                                                                Contains informal notation                 −0.159
   MM25 (AG)
   GLM5 (ZS)
                                                               Presents a concrete instance                  −0.136

    CO46 (ZS)                                                          Uses a metavariable                                                        +0.081
                                                                  Short item (<25 tokens)                                                            +0.125
                      Pass           NMExpr       CMiss
                      NMKind         CompFail     Timeout                                           -0.3         -0.2   -0.1       0           0.1     0.2         0.3

Figure 13: IAF error-type break- Figure 14: Pass-rate difference (items with tag minus without) for
down for representative models. selected feature tags on IAF evaluation results with CO46.


matching expression): the generated term compiles and has the right syntactic shape, but is not
semantically equivalent. Missing constants (CMiss) and kind mismatches (NMKind) occur very
rarely, indicating that models generally follow the structural template.
To understand what makes an item semantically hard, we annotate items along many feature axes and
measure the per-tag pass-rate difference (with selected features shown in Figure 14). Notably, items
that reference a figure or use informal notation are the hardest to formalize: their intended semantics
must be inferred from heterogeneous presentation. Conversely, short items and those that introduce
a named object are easier, consistent with models being most reliable on self-contained, concisely
stated definitions. A full per-dimension breakdown is given in Appendix D.


6                     Related Works
Autoformalization and Theorem-Proving Benchmarks. Existing Lean-based benchmarks target
isolated mathematical statements: competition-math [6, 12, 8], textbook and domain-specific suites [7,
9–11, 30], and repo-scale proof-search benchmarks [13, 14]. Most rely on Mathlib as prebuilt
infrastructure and treat libraries as fixed context. Autoformalization datasets and methods [1, 31–
37, 2–4] similarly focus on single-statement or definition-level translation. LCS-Bench differs by
mechanizing an entire CS textbook as a stand-alone Lean 4 repository covering heterogeneous
declaration kinds completely independent from Mathlib.
Formalizing Computer Science. Prior human-written CS formalizations span verified compilers [38,
39], OS kernels [40, 41], distributed systems [42, 43], and the DeepSpec expedition [44, 45]. Machine-
checked textbooks [46–48] show theory-scale CS formalization is feasible but requires years of expert
effort. Logic-specific mechanizations [49–52] are closely related to LCS-Bench’s content. LCS-
Bench repositions this tradition as an ML-evaluable task.
Neurosymbolic and Agentic Approaches. LCS-Bench is motivated by neurosymbolic program-
ming [53–57], in which neural agents produce structured symbolic artifacts that can be formally
verified. NL-to-formal-specification work for planning and probabilistic programs [58–62] provides
evidence that LLMs can translate informal descriptions into verifiable representations. Code-oriented
agentic frameworks [63, 29, 64] establish the tool-equipped-agent design pattern. LLM-based
provers [65–73] supply natural baselines for our TP tracks.
Evaluation Metrics for Autoformalization. Standard metrics use type-checking (pass@k) or logical-
equivalence checks. BEq+ [74] and related approaches [75–78] address statement-level semantic
consistency but cannot handle inductive types, structures, or constructor-bearing definitions. Our
definitional equivalence checker fills this gap.

                                                                                   9
7   Limitations and Conclusion
We present LCS-Bench, a Lean 4 benchmark derived from Logics for Computer Science for evaluating
LLM and agent capabilities on auto-formalization and theorem proving, independent of any existing
Lean library. Our evaluations show that current models struggle to solve the benchmark, with
performance degrading sharply as difficulty increases.
Limitations. A few textbook theorems resisted both human and LLM-agent proof attempts; at the
current level of deep embedding, we cannot fully capture the textbook’s complexity, and future
work may adopt mature libraries to reach more advanced results. LCS-Bench is also scoped to
a single textbook; extending it across multiple CS textbooks and domains would strengthen the
generalizability of our semi-automated pipeline and experimental findings.

References
 [1] Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N. Rabe, Charles Staats, Mateja Jamnik, and
     Christian Szegedy. Autoformalization with large language models. In Advances in Neural
     Information Processing Systems (NeurIPS), 2022.
 [2] Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li, Kristin Lauter, Swarat Chaudhuri, and
     Dawn Song. Formal mathematical reasoning: A new frontier in AI. arXiv preprint, 2024.
 [3] Zhaoyu Li, Jialiang Sun, Logan Murphy, Qidong Su, Zenan Li, Xian Zhang, Kaiyu Yang, and
     Xujie Si. A survey on deep learning for theorem proving. arXiv preprint, 2024.
 [4] Ke Weng, Lun Du, Sirui Li, Wangyue Lu, Haozhe Sun, Hengyu Liu, and Tiancheng Zhang.
     Autoformalization in the era of large language models: A survey. arXiv preprint, 2025.
 [5] The mathlib Community. The lean mathematical library. In Proceedings of the 9th ACM
     SIGPLAN International Conference on Certified Programs and Proofs, CPP 2020, pages 367–
     381, New York, NY, USA, 2020. Association for Computing Machinery. ISBN 9781450370974.
     doi: 10.1145/3372885.3373824. URL https://doi.org/10.1145/3372885.3373824.
 [6] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. MiniF2F: a cross-system benchmark for
     formal Olympiad-level mathematics. In International Conference on Learning Representations
     (ICLR), 2022.
 [7] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir Radev,
     and Jeremy Avigad. ProofNet: Autoformalizing and formally proving undergraduate-level
     mathematics. arXiv preprint, 2023.
 [8] Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengying Liu, Ye Yuan, Haiming Wang, Wei Ju,
     Chuanyang Zheng, Yichun Yin, Lin Li, Ming Zhang, and Qun Liu. FIMO: A challenge formal
     dataset for automated theorem proving. arXiv preprint, 2023.
 [9] Jiedong Jiang, Wanyi He, Yuefeng Wang, Guoxiong Gao, Yongle Hu, Jingting Wang, Nailin
     Guan, Peihao Wu, Chunbo Dai, Liang Xiao, and Bin Dong. FATE: A formal benchmark series
     for frontier algebra of multiple difficulty levels. arXiv preprint, 2025.
[10] Junqi Liu, Xiaohan Lin, Jonas Bayer, Yaël Dillies, Weijie Jiang, Xiaodan Liang, Roman
     Soletskyi, Haiming Wang, Yunzhou Xie, Beibei Xiong, Zhengfeng Yang, Jujian Zhang, Lihong
     Zhi, Jia Li, and Zhengying Liu. CombiBench: Benchmarking LLM capability for combinatorial
     mathematics. arXiv preprint, 2025.
[11] Rongge Xu, Hui Dai, Yiming Fu, Jiedong Jiang, Tianjiao Nie, Junkai Wang, Holiverse Yang,
     and Zhi-Hao Zhang. LeanCat: A benchmark suite for formal category theory in Lean (part I:
     1-categories). arXiv preprint, 2025.
[12] George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings,
     Amitayush Thakur, and Swarat Chaudhuri. PUTNAMBENCH: evaluating neural theorem-
     provers on the putnam mathematical competition. In Proceedings of the 38th International
     Conference on Neural Information Processing Systems, NIPS ’24, Red Hook, NY, USA, 2024.
     Curran Associates Inc. ISBN 9798331314385.
[13] Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
     Godil, Ryan Prenger, and Anima Anandkumar. LeanDojo: Theorem proving with retrieval-
     augmented language models. In Advances in Neural Information Processing Systems (NeurIPS)
     Datasets and Benchmarks Track, 2023.


                                               10
[14] Jiewen Hu, Thomas Zhu, and Sean Welleck. miniCTX: Neural theorem proving with (long-
     )contexts. arXiv preprint, 2024.
[15] Jean Gallier. Logic for Computer Science: Foundations of Automatic Theorem Proving. Dover
     Publications, second edition, 2015. A corrected version of the original Wiley edition (pp. 511,
     1986).
[16] Anthropic. Claude opus 4 system card. Technical report, Anthropic, 2025. URL https:
     //www.anthropic.com/claude-opus-4-system-card.
[17] OpenAI. GPT-5 system card. Technical report, OpenAI, 2025. URL https://openai.com/
     research/gpt-5-system-card.
[18] Vikas Subramanian and Datalab. Marker: Convert pdf to markdown, 2024. URL https:
     //github.com/datalab-to/marker.
[19] DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu,
     Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu, et al.
     DeepSeek-R1: Incentivizing reasoning capability in LLMs via reinforcement learning, 2025.
[20] DeepSeek-AI, Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu,
     Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, Damai Dai, Daya Guo, Dejian
     Yang, Deli Chen, et al. DeepSeek-V3 technical report, 2024.
[21] Kimi Team, Yifan Bai, Yiping Bao, Cheng Chen, Guanduo Chen, et al. Kimi K2: Open agentic
     intelligence, 2025.
[22] Abhinav Rastogi, Adam Yang, Albert Q. Jiang, Alexander H. Liu, Alexandre Sablayrolles, et al.
     Devstral: Fine-tuning language models for coding agent applications, 2025.
[23] Meta AI. The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation.
     https://ai.meta.com/blog/llama-4-multimodal-intelligence/, 2025. Blog post,
     April 2025.
[24] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu,
     Chang Gao, Chengen Huang, et al. Qwen3 technical report, 2025.
[25] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun
     Zhang, Bowen Yu, Keming Lu, Kai Dang, Yang Fan, Yichang Zhang, An Yang, Rui Men, Fei
     Huang, Bo Zheng, Yibo Miao, Shanghaoran Quan, Yunlong Feng, Xingzhang Ren, Xuancheng
     Ren, Jingren Zhou, and Junyang Lin. Qwen2.5-Coder technical report, 2024.
[26] MiniMax, Aili Chen, Aonian Li, Bangwei Gong, et al. MiniMax-M1: Scaling test-time compute
     efficiently with lightning attention, 2025.
[27] Team GLM, Aohan Zeng, Bin Xu, Bowen Wang, Chenhui Zhang, Da Yin, Dan Zhang, Diego
     Rojas, Guanyu Feng, Hanlin Zhao, Hanyu Lai, Hao Yu, Hongning Wang, Jiadai Sun, Jiajie
     Zhang, Jiale Cheng, Jiayi Gui, Jie Tang, Jing Zhang, Jingyu Sun, Juanzi Li, Lei Zhao, Lindong
     Wu, Lucen Zhong, Mingdao Liu, et al. ChatGLM: A family of large language models from
     GLM-130B to GLM-4 all tools, 2024.
[28] OpenAI. gpt-oss-120b & gpt-oss-20b model card, 2025.
[29] John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik
     Narasimhan, and Ofir Press. SWE-agent: Agent-computer interfaces enable automated software
     engineering. In Advances in Neural Information Processing Systems (NeurIPS), 2024.
[30] Xiao-Wen Yang, Zihao Zhang, Jianuo Cao, Zhi Zhou, Zenan Li, Lan-Zhe Guo, Yuan Yao, Taolue
     Chen, Yu-Feng Li, and Xiaoxing Ma. Formalml: A benchmark for evaluating formal subgoal
     completion in machine learning theory, 2025. URL https://arxiv.org/abs/2510.02335.
[31] Xiaoyang Liu, Kangjie Bao, Jiashuo Zhang, Yunqi Liu, Yu Chen, Yuntian Liu, Yang Jiao, and
     Tao Luo. ATLAS: Autoformalizing theorems through lifting, augmentation, and synthesis of
     data. arXiv preprint, 2025.
[32] Hanyu Wang, Ruohan Xie, Yutong Wang, Guoxiong Gao, Xintao Yu, and Bin Dong. Aria: An
     agent for retrieval and iterative auto-formalization via dependency graph. arXiv preprint, 2025.
[33] Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang, Jing Xiong, Chengwu Liu, Jianhao
     Shen, Hui Jin, Jipeng Zhang, Haiming Wang, Zhicheng Yang, Jing Tang, and Zhijiang Guo.
     Process-driven autoformalization in Lean 4. arXiv preprint, 2024.


                                                 11
[34] Meiru Zhang, Philipp Borchert, Milan Gritta, and Gerasimos Lampouras. DRIFT: Decompose,
     retrieve, illustrate, then formalize theorems. arXiv preprint, 2025.
[35] Qi Guo, Jianing Wang, Jianfei Zhang, Deyang Kong, Xiangzhou Huang, Xiangyu Xi, Wei
     Wang, Jingang Wang, Xunliang Cai, Shikun Zhang, and Wei Ye. Autoformalizer with tool
     feedback. arXiv preprint, 2025.
[36] Lan Zhang, Xin Quan, and Andre Freitas. Consistent autoformalization for constructing
     mathematical libraries. In Proceedings of the 2024 Conference on Empirical Methods in
     Natural Language Processing, page 4020–4033. Association for Computational Linguistics,
     2024. doi: 10.18653/v1/2024.emnlp-main.233. URL http://dx.doi.org/10.18653/v1/
     2024.emnlp-main.233.
[37] Marcus J. Min, Yeqi Gao, Wilson Sy, Zhaoyu Li, Xujie Si, and Osbert Bastani. Divide and
     abstract: Autoformalization via decomposition and abstraction learning. In The Fourteenth
     International Conference on Learning Representations, 2026. URL https://openreview.
     net/forum?id=NjgaeXNit3.
[38] Xavier Leroy. Formal verification of a realistic compiler. Communications of the ACM, 52(7):
     107–115, 2009.
[39] Jianzhou Zhao, Santosh Nagarakatte, Milo M. K. Martin, and Steve Zdancewic. Formal
     verification of SSA-based optimizations for LLVM. In Proceedings of the ACM SIGPLAN
     Conference on Programming Language Design and Implementation (PLDI), 2013.
[40] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock, Philip Derrin,
     Dhammika Elkaduwe, Kai Engelhardt, Rafal Kolanski, Michael Norrish, Thomas Sewell,
     Harvey Tuch, and Simon Winwood. seL4: formal verification of an OS kernel. In Proceedings
     of the ACM SIGOPS Symposium on Operating Systems Principles (SOSP), pages 207–220,
     2009.
[41] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan (Newman) Wu, Jieung Kim, Vilhelm Sjöberg,
     and David Costanzo. CertiKOS: An extensible architecture for building certified concurrent
     OS kernels. In USENIX Symposium on Operating Systems Design and Implementation (OSDI),
     2016.
[42] Chris Hawblitzel, Jon Howell, Manos Kapritsos, Jacob R. Lorch, Bryan Parno, Michael L.
     Roberts, Srinath Setty, and Brian Zill. IronFleet: Proving practical distributed systems correct.
     In Proceedings of the ACM Symposium on Operating Systems Principles (SOSP), 2015.
[43] James R. Wilcox, Doug Woos, Pavel Panchekha, Zachary Tatlock, Xi Wang, Michael D. Ernst,
     and Thomas Anderson. Verdi: A framework for implementing and formally verifying distributed
     systems. In Proceedings of the ACM SIGPLAN Conference on Programming Language Design
     and Implementation (PLDI), 2015.
[44] Andrew W. Appel, Lennart Beringer, Adam Chlipala, Greg Morrisett, Benjamin C. Pierce, et al.
     The DeepSpec project: The science of deep specification. NSF Expedition in Computing, 2017.
     https://deepspec.org/.
[45] Andrew W. Appel. Program Logics for Certified Compilers. Cambridge University Press, 2014.
[46] Benjamin C. Pierce, Andrew W. Appel, Adam Chlipala, Stephanie Weirich, Chris Casinghino,
     Arthur Azevedo de Amorim, Lennart Beringer, Brent Yorgey, et al. Software foundations.
     Electronic textbook series, 2010. https://softwarefoundations.cis.upenn.edu/.
[47] Tobias Nipkow and Gerwin Klein. Concrete Semantics with Isabelle/HOL. Springer, 2014.
[48] Adam Chlipala. Certified Programming with Dependent Types. MIT Press, 2013.
[49] Asta Halkjær From, Frederik Krogsdal Jacobsen, and Jørgen Villadsen. SeCaV: A sequent
     calculus verifier in Isabelle/HOL. arXiv preprint, 2022.
[50] Asta Halkjær From, Alexander Birch Jensen, Anders Schlichtkrull, and Jørgen Villadsen.
     Teaching a formalized logical calculus. arXiv preprint, 2020.
[51] Hugo Herbelin and Danko Ilik. An analysis of the constructive content of Henkin’s proof of
     Gödel’s completeness theorem. arXiv preprint, 2024.
[52] Brian E. Aydemir, Aaron Bohannon, Matthew Fairbairn, J. Nathan Foster, Benjamin C. Pierce,
     Peter Sewell, Dimitrios Vytiniotis, Geoffrey Washburn, Stephanie Weirich, and Steve Zdancewic.
     Mechanized metatheory for the masses: The POPLmark challenge. In International Conference
     on Theorem Proving in Higher Order Logics (TPHOLs), 2005.


                                                 12
[53] Ziyang Li, Jiani Huang, and Mayur Naik. Scallop: A language for neurosymbolic programming.
     Proceedings of the ACM on Programming Languages (PLDI), 7, 2023. doi: 10.1145/3591280.
[54] Jiani Huang, Ziyang Li, Binghong Chen, Karan Samel, Mayur Naik, Le Song, and Xujie
     Si. Scallop: From probabilistic deductive databases to scalable differentiable reasoning. In
     Advances in Neural Information Processing Systems (NeurIPS), 2021.
[55] Ziyang Li, Jiani Huang, Jason Liu, and Mayur Naik. Neurosymbolic programming in Scallop:
     Principles and practice. Foundations and Trends in Programming Languages, 2024. doi:
     10.1561/2500000059.
[56] Robin Manhaeve, Sebastijan Dumancic, Angelika Kimmig, Thomas Demeester, and Luc
     De Raedt. DeepProbLog: Neural probabilistic logic programming. In Advances in Neural
     Information Processing Systems (NeurIPS), 2018.
[57] Zhun Yang, Adam Ishay, and Joohyung Lee. NeurASP: Embracing neural networks into answer
     set programming. In International Joint Conference on Artificial Intelligence (IJCAI), 2020.
[58] Tianyi Zhang, Li Zhang, Zhaoyi Hou, Ziyu Wang, Yuling Gu, Peter Clark, Chris Callison-
     Burch, and Niket Tandon. PROC2PDDL: Open-domain planning representations from texts. In
     Workshop on Natural Language Reasoning and Structured Explanations (NLRSE) at NAACL,
     2024.
[59] Cassie Huang and Li Zhang. On the limit of language models as planning formalizers. In
     Annual Meeting of the Association for Computational Linguistics (ACL), 2025.
[60] Eli Bingham, Jonathan P. Chen, Martin Jankowiak, Fritz Obermeyer, Neeraj Pradhan, Theofanis
     Karaletsos, Rohit Singh, Paul Szerlip, Paul Horsfall, and Noah D. Goodman. Pyro: Deep
     universal probabilistic programming. Journal of Machine Learning Research, 2019.
[61] Bob Carpenter, Andrew Gelman, Matthew D. Hoffman, Daniel Lee, Ben Goodrich, Michael
     Betancourt, Marcus A. Brubaker, Jiqiang Guo, Peter Li, and Allen Riddell. Stan: A probabilistic
     programming language. Journal of Statistical Software, 76(1), 2017.
[62] Luc De Raedt, Angelika Kimmig, and Hannu Toivonen. ProbLog: A probabilistic Prolog and
     its application in link discovery. In International Joint Conference on Artificial Intelligence
     (IJCAI), 2007.
[63] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and
     Karthik R Narasimhan. SWE-bench: Can language models resolve real-world github issues?
     In The Twelfth International Conference on Learning Representations, 2024. URL https:
     //openreview.net/forum?id=VTF8yNQM66.
[64] Xingyao Wang, Boxuan Li, Yufan Song, Frank F. Xu, Xiangru Tang, Mingchen Zhuge, Jiayi
     Pan, Yueqi Song, Bowen Li, Jaskirat Singh, Hoang H. Tran, Fuqiang Li, Ren Ma, Mingzhang
     Zheng, Bill Qian, Yanjun Shao, Niklas Muennighoff, Yizhe Zhang, Binyuan Hui, Junyang Lin,
     Robert Brennan, Hao Peng, Heng Ji, and Graham Neubig. OpenHands: An open platform
     for AI software developers as generalist agents. In International Conference on Learning
     Representations (ICLR), 2025.
[65] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda
     Li, and Xiaodan Liang. DeepSeek-Prover: Advancing theorem proving in LLMs through
     large-scale synthetic data. arXiv preprint, 2024.
[66] Huajian Xin, Z.Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu,
     Liyue Zhang, Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, Dejian Yang, Zhibin Gou, Z.F.
     Wu, Fuli Luo, and Chong Ruan. DeepSeek-Prover-V1.5: Harnessing proof assistant feedback
     for reinforcement learning and monte-carlo tree search. arXiv preprint, 2024.
[67] Z.Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue
     Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, Z.F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang,
     Yuxuan Liu, Wenjun Gao, Daya Guo, and Chong Ruan. DeepSeek-Prover-V2: Advancing
     formal mathematical reasoning via reinforcement learning for subgoal decomposition. arXiv
     preprint, 2025.
[68] Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
     Xia, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-Prover: A frontier model for open-source
     automated theorem proving. arXiv preprint, 2025.


                                                13
[69] Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood
     Sung, Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jianqiao Lu, Hugues de Saxcé, Bolton Bailey,
     Chendong Song, Chenjun Xiao, Dehao Zhang, Ebony Zhang, Frederick Pu, Han Zhu, et al.
     Kimina-Prover preview: Towards large formal reasoning models with reinforcement learning.
     arXiv preprint, 2025.
[70] Albert Q. Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik,
     Timothée Lacroix, Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding formal
     theorem provers with informal proofs. In International Conference on Learning Representations
     (ICLR), 2023.
[71] Haiming Wang, Huajian Xin, Chuanyang Zheng, Lin Li, Zhengying Liu, Qingxing Cao, Yinya
     Huang, Jing Xiong, Han Shi, Enze Xie, Jian Yin, Zhenguo Li, Heng Liao, and Xiaodan Liang.
     LEGO-Prover: Neural theorem proving with growing libraries. arXiv preprint, 2023.
[72] Amitayush Thakur, George Tsoukalas, Yeming Wen, Jimmy Xin, and Swarat Chaudhuri. An
     in-context learning agent for formal theorem-proving. arXiv preprint, 2023.
[73] Guillaume Lample, Marie-Anne Lachaux, Thibaut Lavril, Xavier Martinet, Amaury Hayat,
     Gabriel Ebner, Aurélien Rodriguez, and Timothée Lacroix. HyperTree proof search for neural
     theorem proving. arXiv preprint, 2022.
[74] Auguste Poiroux, Gail Weiss, Viktor Kunčak, and Antoine Bosselut. Reliable evaluation and
     benchmarks for statement autoformalization. In Conference on Empirical Methods in Natural
     Language Processing (EMNLP), 2025.
[75] Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Xian Zhang, Fan Yang, and Xiaoxing Ma.
     Autoformalize mathematical statements by symbolic equivalence and semantic consistency. In
     Advances in Neural Information Processing Systems (NeurIPS), 2024.
[76] Lan Zhang, Marco Valentino, and Andre Freitas. Autoformalization in the wild: Assessing
     LLMs on real-world mathematical definitions. arXiv preprint, 2025.
[77] Hayden Moore and Asfahan Shah. Evaluating autoformalization robustness via semantically
     similar paraphrasing. arXiv preprint, 2025.
[78] Jianqiao Lu, Yingjia Wan, Yinya Huang, Jing Xiong, Zhengying Liu, and Zhijiang Guo.
     FormalAlign: Automated alignment evaluation for autoformalization. arXiv preprint, 2024.


A     Details of the Automated Formalization Pipeline
This appendix gives a detailed account of the four-stage automated pipeline summarized in Section 3.

A.1   Pre-Processing

The textbook PDF is converted to Markdown using Marker [18], producing one file per subsection
under a strict formatting guide so that every numbered item carries a stable label. Graphics such
as inference rules, proof trees, and directed acyclic graphs are redrawn by hand as ASCII diagrams
embedded in the Markdown, giving the downstream agent parseable structured content. Each textbook
item is then wrapped in a typed XML tag: <theorem>, <lemma>, <corollary>, <definition>,
<example>, <proof>, and <problem>. Many untagged statements carry formal weight—scope
restrictions, standing assumptions, and informal lemmas stated in prose—and these are also annotated
manually. The result is a set of per-subsection Markdown files in which every item is a discrete,
labeled unit with a stable ID of the form chap3::definition-3.2.1.

A.2   Formalization Planning

Planning is divided into two sub-stages corresponding to the two intermediate representations.
L1 annotation (concept graph). A formalize-annotator subagent reads each section and extracts,
sentence by sentence, every keyword, sub-clause, and concept. Each extracted node must be a concrete
noun phrase (e.g., “propositional formula”, “left parenthesis count”). Edges encode textbook-level
relationships: IS - A, HAS - A, RELIES - ON, and DEFINED - BY. A sentence-coverage validator requires
every sentence to contribute at least one node, and every concept node must be realizable from within
the textbook itself with no delegation to external libraries.


                                                 14
L2 annotation (formal signature graph). A formalize-specifier subagent then annotates each L1
node with its Lean realization: lean_kind (∈ {inductive, structure, def, abbrev, notation,
theorem, lemma, instance}), constructor names, field names, companion definitions, and an em-
bedding level: deep (syntax DSLs as inductive types), shallow (semantic properties over deep syntax
using Lean’s Prop layer), or mixed (meta-theorems connecting the two layers, such as soundness,
completeness, and termination results). The embedding level determines whether a concept must be a
first-class inductive type or may live purely in Prop. A structural-completeness validator checks that
every textbook sentence maps to at least one L2 node and that HAS - A decompositions respect the
dependency order of the L1 graph. This stage is also where implicit standing assumptions must be
resolved: for instance, §3.4.2’s connective restriction requires a separate PropFormNorm type rather
than re-using PropForm.

A.3   Lean Implementation

A formalize-implementer subagent translates each module in three rounds, mirroring the dependency
order of the L2 graph.
Round 1 (L2 → L3): Structures and inductive types. All inductive types and structures are
defined first. Each declaration receives an @[lcsitem id] attribute encoding the stable textbook
item ID, and @[lcsmain] marks the primary authored declaration to distinguish it from companion
definitions and elaboration byproducts. After this round lake build is run and a review script
verifies that the declared types match the L2 signature graph.
Round 2 (L3 → L4a): Definitions, functions, and examples. Building on the type scaffolding, the
agent defines functions, abbreviations, instances, and examples, covering both computational content
(evaluation functions, normal-form transformers, search procedures) and semantic predicates (validity,
satisfiability, tautology). A review script checks that the definitions preserve textbook semantics.
Round 3 (L4a → L4): Theorem and lemma statements. The agent writes theorem and lemma
statements from the L2 graph, leaving proof bodies as sorry placeholders. An implementation
validator flags vacuous theorem statements, missing inductive cases, identity-function stubs, and
dead @[lcsitem] declarations. The goal of this round is theory-scale coherence, which requires all
statements to type-check, all dependencies to compile, and the overall structure to faithfully mirror
the textbook, without requiring complete formal proofs.

A.4   Formal Correctness Review

The formal correctness review focuses on reviewing the faithfulness and mathematical correctness of
the Lean statement by filling the sorry placeholders or compiling a counter-example. The central
design principle is that sorry-count is not a quality metric: a sorry-preserved-but-faithful statement is
progress; a proved-but-unfaithful statement requires revert.
Proof search loop. For each sorry-bearing theorem, an automated proving agent operates in an
iterative LSP-driven loop. At each step, it reads the current proof state from LSP diagnostics and
attempts tactics in a fixed priority order: terminal tactics (rfl, decide, omega), followed by simp
and ring, with grind and aesop used as fallbacks. The agent reports PROVED when it successfully
produces a proof that compiles without sorry, PARTIAL when it discharges some but not all goals in
a larger proof, and FALSE when it finds evidence that the theorem is not provable under the current
formalization. Successful fills are committed atomically in an isolated git worktree to be reviewed.
Counter-example search. When proof search stalls (e.g. multiple agents report FALSE), the pipeline
attempts to prove the negation of the statement: for ∀x, P (x), it constructs x with ¬P (x). A
successful counter-example immediately reclassifies the item as incorrect and routes it to faithfulness
review to investigate the root cause rather than further proof attempts.
Triage, decomposition, and review gate. A high-level orchestrator manages the loop through an
issue-tracking system (600+ YAML issue files). Issues are triaged by severity (faithfulness failures
first, then blocking dependencies, then sorry density). Stuck tasks are decomposed into sub-goals
with hard caps (≤3 sorries, ≤2 files per sub-issue). Before any worktree is merged, a mandatory
multi-phase mathematical review is triggered. The review compares the current Lean declaration
against (1) the original textbook text, (2) the L2 formal signature graph, (3) the initial auto-formalized
implementation at a pinned commit, and (4) the current state. Any spurious divergence at any layer


                                                   15
              Quote.md

                                                                             GroundTruth.lean
            Context.lean                Model         Submission.lean
                                                                           Against DefEq Checker     ✓/ ✗


           Starter.lean.in

(a) AF tracks: the model receives Quote.md, Context.lean, and Starter.lean.in, and produces
Submission.lean, which is checked against GroundTruth.lean by the DefEq Checker.


                  Quote.md

                                                         Submission.lean         Lean type-checker
               Context.lean                Model            (no sorry)                               ✓/ ✗
                                                                                   + cheat scan

               Starter.lean.in
           (theorems sorry-stubbed)

(b) TP tracks: the model receives Context.lean, Starter.lean.in (theorem bodies replaced by sorry),
and, for ITP only, Quote.md; it produces Submission.lean, accepted iff all target declarations are present, the
file builds, no sorry remains, and no cheat patterns (new axiom, opaque, @[implemented_by], . . . ) appear.
                                      Figure 15: Evaluation protocol diagrams.


results in a REJECT verdict; if a downstream review later discovers that an upstream FAITHFUL
verdict was erroneous, the entire dependent chain is reverted.
Loophole catalog. Over the course of the project, 13 classes of faithfulness failure (L1–L13) were
identified from real committed-then-reverted work, each with a detection signature and a prescribed
fix. Representative examples include: L1 (existential-over-state-record, replacing a concrete witness
with ∃w), L4 (trivial existential of a reflexively-true predicate), L8 (path-disconnected Hintikka set),
L12 (unwritten invariant: the signature admits X, the proof needs Y ⊂ X, and an adversary lives
in X \ Y ), and L13 (silent strengthening, the dual of L1–L12, where a hypothesis added to defeat
an adversary narrows the textbook claim). The loophole catalog serves as a mandatory checklist for
regression-testing review quality throughout the project, and is continuously expanded as new failure
modes are uncovered during formalization and proof repair.

B     Dataset Details
B.1     Evaluation Protocol

Figure 15 illustrates the evaluation protocol for the AF and TP tracks.

B.1.1    Model I/O
For non-agentic modes (zero-shot and thinking), the prompt is the concatenation of a mode-specific
template with fenced blocks for Context.lean, Starter.lean.in, and (when present) Quote.md.
The response is parsed by taking the last fenced lean4/lean block. If no fenced block is recovered,
the model response to the item is recorded with status=missing.
For agentic mode, the model writes its submission directly to Submission.lean over successive
turns; the initial Submission.lean is seeded from the starter with target bodies initialized to sorry.
When the loop exits, the final on-disk Submission.lean is taken as ŷ.

B.1.2    Modes and Agent Tools
Thinking variants enable the provider-native extended-reasoning channel. For models with a
binary on/off toggle, we enable thinking; for models that expose graded effort levels, we set
reasoning_effort=high. For non-Anthropic models, reasoning tokens and visible-answer to-


                                                        16
                              Pass   NMExpr    CMiss       NMKind          CompileFail   Timeout




        CO46 (AG)
        CS46 (AG)
    GPT54 (AG)
         K25 (AG)
     GLM5 (AG)
     MM25 (AG)
         Q32 (AG)
   GPTOSS (AG)
        CS46 (TH)
        CO46 (TH)
     GPT54 (TH)
   GPTOSS (TH)
         K25 (TH)
     MM25 (TH)
     GLM5 (TH)
        DSR1 (TH)
         Q32 (TH)
        CO46 (ZS)
     GPT54 (ZS)
        CS46 (ZS)
     GLM5 (ZS)
        CH45 (ZS)
        DS32 (ZS)
         K25 (ZS)
          D2 (ZS)
          L4 (ZS)
         Q3C (ZS)




                    0   10     20      30      40         50          60         70       80       90   100
                                                     Item share (%)

Figure 16: IAF error-type breakdown per (model, mode) cell. Each bar is a 100% stacked compo-
sition: Pass; NMExpr / CMiss / NMKind (compiled but checker-failed, resolved by precedence
NMExpr > NMKind > CMiss so the three are mutually exclusive); CompileFail (submission did
not elaborate); Timeout (no submission produced within the time/token budget).


kens share a single budget, which we set to max_tokens=32,768. Opus and Sonnet expose the
thinking budget and the visible-output budget as separate caps, which we both set to 16,384.
The agentic scaffold is a lightweight SWE-agent-style loop based on mini-swe-agent [29]. In place
of the single bash tool of the original scaffold, we expose four custom tools tailored to Lean editing:

• read_file(which) — reads one of context, quote, or submission.
• edit_submission(old_str, new_str) — string-replacement edit on Submission.lean that
  must match old_str exactly once.
• lake_build() — runs lake env lean on the current Submission.lean and returns the com-
  piler output.
• done(reason?) — exits the loop.

B.1.3     Scoring

AF tracks. The DefEq checker emits a per-target triple of flags: CMiss (constant missing: expected
constant not declared), NMkind (Not matching kind: kind mismatch such as def vs. theorem), and


                                                    17
                                   IAF                                               SSAF                               IAF-D
Model
           Pass      Compile      CMiss      NMExpr      NMKind Pass Compile CMiss NMExpr NMKind Pass Compile CMiss NMExpr NMKind
                                                                       Zero-shot
D2        8.4±0.37   27.9±1.24 2.7±0.41      19.4±0.97   0.1±0.10   1.7     7.8     0.9      6.0   0.0   7.6    18.0   2.1      10.1   0.0
DS32      9.5±0.61   39.8±0.81 6.3±0.10      29.9±0.54   0.2±0.10   1.7    18.1      5.2    16.4   0.0   7.3    33.0   4.0      25.4   0.0
GLM5     13.9±0.62   41.0±0.71 4.6±0.31      26.8±1.18   0.0±0.00   0.9    10.3      1.7     9.5   0.0   10.7   36.4   3.1      25.4   0.3
GPT54    15.4±0.41   58.5±1.35 7.6±0.77      42.5±1.07   0.0±0.00    –       –        –       –     –     –      –      –        –      –
CH45     11.1±0.27   44.2±1.64 6.7±0.64      32.7±1.79   0.0±0.00   2.6    19.8      2.6    17.2   0.0   9.8    36.4   4.9      26.3   0.0
K25       9.0±0.67   37.6±0.77 5.0±0.71      27.7±0.37   0.0±0.00   2.6    13.8      2.6    11.2   0.0   7.0    33.0   3.7      26.0   0.3
L4        7.6±0.18   24.3±0.62 2.1±0.31      16.6±0.74   0.0±0.00   0.9    12.9      0.9    12.1   0.0   6.4    21.7   1.5      15.0   0.0
CO46     16.8±0.47   70.5±0.87 12.8±0.64     52.9±1.33   0.9±0.18   2.6    50.0     16.4    47.4   1.7   14.1   64.5   8.9      48.6   0.9
Q3C       3.1±0.31   12.3±0.74 2.3±0.27       9.0±0.57   0.0±0.00   0.0     0.0     0.0      0.0   0.0   3.4    8.3    0.6      4.6    0.3
CS46     15.0±0.31   57.4±0.44 8.9±0.53      41.2±0.51   0.0±0.00   5.2    40.5      9.5    35.3   0.0   12.8   55.4   7.6      41.9   0.0
                                                                      Thinking
DSR1      4.2±0.10   18.7±0.18    2.9±0.10   14.0±0.10   0.0±0.00 0.9      4.3      0.9      3.4   0.0    2.8    8.9    2.1      6.1   0.0
GLM5      5.4±0.71   20.8±0.81    2.8±0.18   15.3±0.35   0.2±0.20 0.9      9.5      3.4      8.6   0.0    4.3   18.7    2.4     14.4   0.0
GPT54    16.3±0.57   73.9±0.97   12.5±0.92   55.9±1.43   0.2±0.10  –        –        –        –     –      –      –      –        –     –
GPTOSS   15.5±0.44   60.9±0.61   11.4±1.33   44.8±0.10   0.0±0.00  –        –        –        –     –      –      –      –        –     –
K25      14.4±0.35   53.0±0.41    7.5±0.20   37.3±0.81   0.3±0.18 6.9     31.9      6.0     25.0   0.0   11.0   45.6    6.7     33.6   0.0
MM25      9.1±0.51   35.7±1.06    5.0±0.71   25.1±0.64   0.5±0.20 1.7      5.2      0.9      2.6   0.0   10.1   40.4    7.0     28.7   0.0
CO46     17.6±0.27   77.1±1.70   14.1±0.47   58.3±1.58   1.0±0.27 4.3     56.9      14.7    52.6   1.7   16.2   76.5   13.8     59.3   1.2
Q32       2.5±0.10   11.5±0.27    1.8±0.53    8.7±0.37   0.0±0.00 1.7      6.0      0.9      4.3   0.9    5.2   13.5    1.5      8.0   0.0
CS46     17.9±0.82   66.9±0.97   10.1±1.27   48.5±1.12   0.3±0.18 2.6     42.2      11.2    39.7   0.0   15.6   67.0    9.8     50.2   0.3
                                                                          Agentic
GLM5     14.7±0.35 61.0±1.25     10.0±0.87   44.2±0.83   2.7±0.44   4.3     96.6    46.6    91.4   9.5    –      –      –        –     –
GPT54    16.1±0.37 73.4±0.64     13.0±0.44   55.0±0.47   0.1±0.10    –        –       –       –     –     –      –      –        –     –
GPTOSS    2.1±0.31 14.4±0.61      3.9±0.62   12.2±0.31   0.5±0.10    –        –       –       –     –     –      –      –        –     –
K25      15.3±0.88 73.3±1.87     14.8±1.68   56.1±0.97   3.0±0.20   3.4      92.2   41.4    88.8   6.9    –      –      –        –     –
MM25     12.1±0.10 78.7±1.12     25.7±0.77   61.3±0.71   3.3±0.62   2.6      85.3   44.8    81.0   7.8    –      –      –        –     –
CO46     20.1±0.67 99.4±0.47     21.1±0.18   76.1±0.61   4.1±0.54   5.2     96.6    38.8    91.4   3.4    –      –      –        –     –
Q32         5.5      29.4           5.2         22.0        0.3     0.0      0.9     0.9     0.9   0.0    –      –      –        –     –
CS46     18.0±0.53 98.5±0.18     23.4±0.37   77.5±0.67   3.9±0.20   3.4     96.6    41.4    93.1   6.9    –      –      –        –     –

Table 4: Per-cell performance across three AF tracks. Pass = strict binary pass rate (%) — submission
passes Algorithm 1. Compile = fraction of items whose submission elaborates as valid Lean (header
success, regardless of constant matching). CMiss / NMExpr / NMKind report the percentage of items
whose grader output contains at least one constmissing, notmatchexpr, or notmatchconstkind
error. An item can contribute to multiple error columns if it triggers several types. Rows are grouped
by inference mode using shaded separator bars. Dashes indicate no curated run for that cell. IAF
values are mean ± SEM across three independent runs; SSAF and IAF-D are single runs reported
without variance.




NMExpr (Not matching expression: body or statement not definitionally equivalent). An item is
recorded as status=pass iff it passes Algorithm 1. When the submission fails to elaborate, the item
is assigned CompileFail (compilation failure). A more detailed error type breakdown of the IAF track
evaluation is shown in Figure 16. A more comprehensive table showing the evaluation results of all
three AF tracks is in Table 4.
TP tracks. A TP submission is accepted as pass iff all four of the following hold:
1. Declarations present. Every target in Ty appears in ŷ with a type signature whitespace-equivalent
   to its ground-truth signature.
2. Build succeeds. lake env lean on ŷ returns exit code zero; warnings are permitted.
3. No sorry. After stripping comments and string literals, no sorry keyword remains.
4. No cheats. The stripped source contains none of: axiom <name>, opaque <name>, unsafe
   declarations, @[extern], @[implemented_by], or direct uses of sorryAx.
Any condition failing yields status=fail.
Benchmark fairness. Because the LCS-Bench artifact was constructed with the assistance of Claude
Opus, one might worry that it encodes implicit biases favouring Anthropic models. Figure 17 shows
the overlap of passing IAF items among Claude Opus 4.6, GLM-5, and GPT-5.4. Of all items solved
by at least one model, 29 are solved by all three, while only 8, 7, and 5 items are solved exclusively
by Opus, GLM-5, and GPT-5.4 respectively. The large shared core and small model-exclusive tails
indicate that item difficulty is governed by the formalization content, not by model-specific familiarity
with the artifact.


                                                                           18
                                        Passing items per model (IAF track)
                              Claude Opus 4.6                           GLM-5

                                                               9
                                          8
                                                                           7

                                                          29

                                              11
                                                                    4


                                                      5

                                                    GPT-5.4

Figure 17: Three-way Venn diagram of passing IAF items for Claude Opus 4.6 (57 pass), GLM-5
(49), and GPT-5.4 (49). The large shared region (29 items) shows that model performance is driven
by item difficulty rather than any bias introduced by the construction process.


B.2     Data Engine

We develop a deterministic, artifact-grounded data engine that performs systematic dependency
analysis and Lean code modification to automatically generate all evaluation tracks from the LCS-
Bench Lean artifact. This process is AI-free and fully reproducible: whatever is stabilized in the
artifact is faithfully used to derive the evaluation datasets without any model intervention.
For AF targets, we specify which Lean declarations to include as targets, and the engine fetches all
transitive dependencies, removes unwanted proof bodies, and composes them into a compact context
C while generating the starter template Ty and ground-truth y ∗ . IAF-D is generated in the same way,
with the addition of distractor declarations injected beyond the minimal dependency set; specifically,
for each instance, we add distractors amounting to half the number of real context dependencies.
For TP targets, the engine replaces proof bodies with sorry to produce C. A TP data point
is generated only when the entire dependency tree is well-formed and fully proved; unproved
declarations in the current artifact are therefore excluded from the TP tracks.
By adjusting the engine’s configuration, it is straightforward to generate further scaled-up variants
such as CAF (chapter-level auto-formalization) or SSTP (subsection-level theorem-proving). Through
our evaluation, however, we find these variants too difficult for current models and leave them for
future work.


C      Equivalence Checker

To evaluate the faithfulness of each submission, we developed Check.lean, a program that verifies
every constant declared in Groundtruth.lean appears in Submission.lean in a semantically
equivalent form, and that both files share the same imports. Equivalence is defined differently
depending on the kind of constant, as summarised in Table 5.


      Kind          What is compared      Equivalence criterion
      Definition    Body expression       Definitionally equal (IS D EF E Q) or congruence closure (GRIND)
      Theorem       Statement type        Definitionally equal (IS D EF E Q) or congruence closure (GRIND)
      Inductive     Constructor names     Same set of constructors, order-independent (structural check)
      Constructor   Constructor type      Definitionally equal (IS D EF E Q only, no GRIND)
          Table 5: Equivalence criteria used by Equivalence Checker for each constant kind.



                                                      19
Definition: Two definitions are considered equivalent if the Lean expressions corresponding to their
bodies are equal after full reduction, so different but computationally equivalent implementations are
treated as equal.

 Groundtruth                                            Submission (✓ accepted)

  def double ( n : Nat ) : Nat :=                        def double ( n : Nat ) : Nat :=
    n + n                                                  2 * n



Theorem: For theorems (which are effectively prop-typed non computable definitions), comparing
types alone is too loose: since under proposition extensionality all true propositions are provably
equal, meaning any two true theorems would be considered equivalent. We therefore require the
statement types to be definitionally equal (IS D EF E Q) or equal under congruence closure (GRIND),
which captures the notion that two theorems are talking about the same idea but just phrased slightly
differently.

 Groundtruth                                            Submission (✓ accepted)

  theorem add_zero ( n : Nat )                           theorem add_zero ( n : Nat ) :
      : n + 0 = n := by simp                               n + 0 = n := Nat . add_zero n



Inductive: Two inductive definitions are equivalent if they share the same set of constructor names (up
to permutation). Each constructor is then checked independently: the constructor from the submission
must have the same type as the corresponding constructor in the groundtruth (by IS D EF E Q).

 Groundtruth                                            Submission (✓ accepted)

  inductive Shape where                                  inductive Shape where
    | circle ( r : Float )                                 | rect   ( w h : Float )
    | rect   ( w h : Float )                               | circle ( r : Float )


Binder renaming resilience. Moreover, by using Lean’s definitional equality instead of structural
equality of the underlying expressions, our checker is resilient to renaming of locally bound variable
names, since changing binder names preserves definitional equality.

 Groundtruth                                            Submission (✓ accepted)

  def comp ( f g : Nat -> Nat )                          def comp ( f g : Nat -> Nat )
    ( x : Nat ) : Nat := f ( g x )                         ( n : Nat ) : Nat := f ( g n )


Sandboxing. The constants of the Groundtruth and Submission are elaborated in their respective
environments, and each constant’s body is fully reduced in its own environment before comparison
using reduceFully, which runs Lean’s kernel reducer at full transparency. This means all definitions
are unfolded, including typeclass projections and instance fields that would otherwise be opaque at
lower transparency levels. As a result, any semantic pollution introduced in the Submission is inlined
away during reduction, exposing the underlying kernel primitives rather than the Submission’s local
definitions. The comparison itself is then run in the Groundtruth environment elaborated only up to
(but not including) c, ensuring that the Submission’s local definitions are not in scope and that c itself
is not in scope during its own check.
The algorithm for the Check.lean program is summarized below:




                                                   20
Algorithm 1 Check(Groundtruth, Submission)
 1: Elaborate both files; abort on errors. Flag passed ← false if imports differ.
 2: for each constant c in Groundtruth (excluding auto-generated recursors) do
 3:          / Submission or kind(c) differs then record failure; continue
        if c ∈
 4:     end if
 5:     Let e1 , e2 be the fully reduced relevant expressions of c in each file
 6:     Definition / Theorem: E QUIV(e1 , e2 , grind = true)                    ▷ body / statement type
 7:     Inductive: success iff constructors of c are the same set in both files
 8:     Constructor: E QUIV(e1 , e2 , grind = false)                                 ▷ constructor type
 9: end for
10: return passed ∧ all checks succeeded

11: function E QUIV(e1 , e2 , grind)
12:    if IS D EF E Q(e1 , e2 ) then return S UCCESS
13:    end if
14:    if grind ∧ GRIND(e1 = e2 ) succeeds then return S UCCESS
15:    end if
16:    return M ISMATCH
17: end function



D     Feature Tagging and Analysis
D.1   Tagging schema

Each benchmark item is annotated with tags drawn from five orthogonal categories, capturing different
dimensions along which auto-formalization difficulty may vary. Surface features (Table 6) describe the
natural-language presentation of the textbook item, such as whether it uses schematic metavariables,
ellipsis notation, enumerated clauses, or refers to a figure—properties that affect how readily the prose
transcribes into Lean syntax. Subject matter (Table 7) categorizes the mathematical content of the
item along the syntax–semantics axis, distinguishing claims about derivations and formulas (syntactic)
from claims about models and truth (semantic), with further tags for meta-theorems, object-level
claims, and algorithmic content. Logical shape (Table 8) records the high-level logical form of the
statement, including its dominant quantifier (universal, existential, mixed-quantifier, quantifier-free),
connective structure (conjunctive, disjunctive, conditional, iff, negative-claim), and whether it is
multi-part or asserts an equality-claim. Vocabulary (Table 9) tags the mathematical machinery the
item relies on, ranging from set-theoretic and higher-order constructions to binders-substitution,
numeric-arithmetic, string-level, and infinitary reasoning. Finally, definition shape (Table 10) applies
to definitional items and identifies their structural form: whether the item introduces a type-definition,
inductive-definition, function-definition, predicate-definition, or recursive-definition, and whether it is
parametric, notational, uses mutual-recursion, or defines-multiple concepts at once. Tags within each
category are non-exclusive, since a single item may exhibit several features simultaneously (e.g., a
universally quantified meta-theorem that bridges syntax and semantics).
Tag assignments are produced by the pre-processing stage of the LCS-Bench pipeline: a model
proposes tags from a fixed controlled vocabulary, every assignment is reviewed by human experts,
and disagreements are reconciled before the item is admitted to the released artifact. The five tables
below report the absolute count and percentage of items in N =554 tagged items carrying each tag.

D.2   Tag distributions

Figure 18 shows the distribution of the number of tags assigned per item, summed across all five
categories. The median item carries roughly a dozen tags and the distribution is unimodal; no
item is left untagged on every axis, and only a handful of items concentrate more than 20 tags.
Two regularities are worth noting. First, surface-feature tags fire densely (almost every item has a
non-trivial length tag, and most have at least one of uses-metavariable, enumerated-clauses,
or uses-ellipsis); this is a property of the textbook’s discursive style rather than of our scheme.
Second, definition-shape tags fire only on the ∼30% of items whose role is to introduce a new
declaration, which explains the long lower tail in the per-axis cardinality. Together, the figure shows


                                                   21
      Tag                     Description                                                        Items         %
      uses-metavariable       Uses schematic letters (e.g. A, B for arbitrary formulas;           432      78.0
                              M , N for models).
      uses-ellipsis           Uses “. . . ” or \dots for continuation, as in a1 , . . . , an .    165      29.8
      enumerated-clauses      Body lists items as (i)(ii)(iii) or (a)(b)(c).                      134      24.2
      name-introducing        Uses “we call X a Y ”, “X is said to be Y ”, “we say”.               95      17.1
      concrete-instance       Claim about a specific object or example rather than a               88      15.9
                              schema.
      informal-notation       Visibly informal or typographic notation that will not               40          7.2
                              transcribe verbatim.
      references-figure       Refers to a figure, diagram, or tree picture.                        34          6.1
Table 6: Natural-language surface features tagged on benchmark items (N =554). Tags are non-
exclusive, so column sums exceed 100%.


 Tag                              Description                                                       Items            %
 syntactic                        Talks about derivations, formulas, or strings only.                    464     83.8
 meta-theorem                     Claim about the proof system itself (soundness, com-                   219     39.5
                                  pleteness, cut-elimination, . . . ).
 semantic                         Talks about models, satisfaction, or truth.                            184     33.2
 bridges-syntax-semantics         Relates syntactic ⊢ to semantic ⊨.                                     132     23.8
 object-level                     Claim about a derivation, sequent, or formula inside a                  80     14.4
                                  system.
 algorithm                        Describes a procedure or algorithm.                                     56     10.1
Table 7: Subject-matter tags on benchmark items (N =554). Tags are non-exclusive, so column sums
exceed 100%.



that the schema partitions the benchmark finely enough to support the per-tag pass-rate analysis that
follows without leaving large untagged subsets.

D.3    Per-tag pass-rate analysis

Setup. For each tag t, we compare the pass rate of items carrying t against the pass rate of
items not carrying t on Track 1 (IAF). To maximise statistical power, we aggregate the six curated
claude-opus-4-6 runs (three zero-shot and three thinking-mode) and treat every (item, run) pair as
an independent trial, yielding N =1, 950 trials over 325 items. We then compute rwith (t), rwithout (t),
and the difference ∆(t) = rwith (t) − rwithout (t) in percentage points. Significance is assessed with
a two-proportion z-test; bars in Figures 20–23 are annotated with ∗ , ∗∗ , ∗∗∗ for p < 0.05, 0.01,
and 0.001 respectively. We restrict to tags with nwith ≥ 20, dropping a handful of singleton tags
(tfae, existence-and-uniqueness, equational-chain). Wilson 95 % confidence intervals on
the per-tag rates are reported in tag_analysis_out/opus_aggregate/per_tag.csv; we omit
them from the bar plots for legibility. Treating runs as independent slightly inflates significance under
within-item correlation, but the sign and ordering of effects is robust: re-running the analysis on
each individual run separately reproduces the qualitative ranking on every axis. We report Opus 4.6
here because it is the strongest model in our suite and has the most curated runs; the per-tag effects
are qualitatively preserved across the four largest models we evaluated (Sonnet 4.6, Kimi-K2.5,
Qwen3-Coder), as confirmed by the cross-model overlay we omit here for space.

Surface features (Fig. 19). The surface-feature axis shows the cleanest length effect on the
benchmark: len-short items pass at +12.5 pp, len-medium at −6.1 pp, and len-long at
−10.9 pp, monotone across all three buckets. Beyond raw length, the strongest negative ef-
fects come from informal or visually-anchored phrasings: items that references-figure
(−16.1 pp), informal-notation (−15.9 pp), embed a concrete-instance (−13.6 pp),
enumerated-clauses (−10.2 pp), or uses-ellipsis (−7.7 pp). The two positive non-length
tags are uses-metavariable (+8.1 pp) and name-introducing (+6.1 pp); both indicate that the
prose is already abstract and close to a definition. Read as a whole, the figure suggests that the
auto-formalizer struggles much more with rendering semi-formal mathematical English (figures,


                                                      22
      Tag                    Description                                                    Items         %
      universal              Top-level shape is ∀x. φ(x) (one or more universally            159         28.7
                             quantified variables, no leading existential).
      conditional            Statement is an implication φ → ψ at the top level.              82         14.8
      multi-part             Prose enumerates several sub-claims that must all hold           66         11.9
                             (“(i) . . . (ii) . . . ”).
      conjunctive            Top-level conjunction φ ∧ ψ (after stripping outer quan-         46          8.3
                             tifiers).
      existential            Top-level shape is ∃x. φ(x), requiring witness construc-         39          7.0
                             tion.
      iff                    Biconditional φ ↔ ψ, typically a characterisation                37          6.7
                             lemma.
      equality-claim         Asserts equality of two terms, sets, or derivations.             25          4.5
      mixed-quantifier       Alternating quantifier prefix such as ∀∃ or ∃∀.                  23          4.2
      quantifier-free        Propositional or open-formula claim with no quantifier           20          3.6
                             in scope.
      negative-claim         Asserts a negation ¬φ or non-existence.                          10          1.8
      disjunctive            Top-level disjunction φ ∨ ψ (case-split shape).                   6          1.1
Table 8: Logical-shape tags on benchmark items (N =554). Tags classify the top-level connective /
quantifier pattern of the statement to be formalized; they are non-exclusive, so column sums exceed
100%. Two long-tail tags (existence-and-uniquen ess, tfae) with n=1 are omitted.


    Tag                        Description                                                    Items             %
    binders-substitution       Reasons about bound variables, free-variable sets, α-            207        37.4
                               renaming, or capture-avoiding substitution.
    set-theoretic              Manipulates sets, relations, functions-as-graphs, or car-        158        28.5
                               dinality at the meta-level.
    string-level               Operates on raw symbol strings, lists of tokens, or con-             48      8.7
                               catenations (e.g. string parses, length lemmas).
    numeric-arithmetic         Uses N / Z, induction on naturals, counting, or arithmetic           40      7.2
                               inequalities.
    infinitary                 Mentions infinite sets, sequences, Kőnig’s lemma, or                33      6.0
                               compactness — i.e. requires non-finitary reasoning.
    higher-order               Quantifies over predicates, formulas, or other higher-               25      4.5
                               order objects.
    equational-chain           Proof or statement is a chain of equalities/equivalences             11      2.0
                               (a = b = c = . . .).
Table 9: Vocabulary tags on benchmark items (N =554). Tags classify the kinds of mathematical
objects the item manipulates; they are non-exclusive, so column sums exceed 100%.



ellipses, case lists, worked examples) into Lean than with translating prose that is already sym-
bolic. The implication is methodological: a substantial fraction of benchmark difficulty lives in the
prose-to-symbol translation, not in the underlying mathematics.

Subject matter (Fig. 20). This axis shows by far the largest spread of any dimension on the
benchmark, ≈ 40 pp from worst to best. Semantic items, which talk about models, satisfaction, and
truth, gain +19.6 pp, and bridges-syntax-semantics items (soundness/completeness-style statements)
gain +16.4 pp. By contrast, algorithm items, which prescribe procedural behaviour, lose −19.3 pp;
syntactic items, which manipulate proof-system machinery directly, lose −16.4 pp; and object-level
arithmetic / string formalizations lose −9.7 pp. meta-theorem items sit near zero (the dimension
nominally distinguishes about-the-system from inside-the-system content, and meta-theorems straddle
that boundary). Read together with the surface-feature analysis, the pattern is striking: models are
reliable at the semantic core of logic—well-understood, math-shaped, nameable abstractions—and
unreliable on the syntactic infrastructure the textbook spends most of its space building. Because that
infrastructure (sequent syntax, derivability, substitution lemmas, etc.) is exactly what theory-scale
formalization has to get right first, this single dimension explains a large share of why the absolute
pass rate on Track 1 stays below 20 %.


                                                   23
        Tag                                    Description                                                                         Items                %
        parametric                             Definition is parameterised by a type, signature, or ear-                             99            17.9
                                               lier structure (e.g. a proof system parameterised by its
                                               rules).
        defines-multiple                       Single textbook item introduces several mutually related                              62            11.2
                                               declarations (e.g. a syntactic class plus its constructors).
        predicate-definition                   Introduces a new Prop-valued relation or judgement                                    60            10.8
                                               (e.g. “Γ ⊢ φ”).
        function-definition                    Introduces a new total function over already-defined                                  53                9.6
                                               data.
        type-definition                        Introduces a new type, structure, or class (non-recursive                             40                7.2
                                               carrier).
        inductive-definition                   Introduces an inductive type or inductively-defined pred-                             31                5.6
                                               icate with explicit constructors.
        recursive-definition                   Definition is by structural recursion on one of its argu-                             25                4.5
                                               ments.
        notational                             Item is essentially syntactic sugar / a notation declaration                          11                2.0
                                               with no new computational content.
        mutual-recursion                       Two or more declarations defined in a single mutual                                        5            0.9
                                               block, each referring to the other.
Table 10: Definition-shape tags on benchmark items (N =554). Tags fire only on items whose role is
to introduce a new declaration; they are non-exclusive, so column sums exceed 100%.

#items

  414                              312                                      223                                   197                      259

                                                                      176                                   154
                                                                                                                        124          174


                                                                                                                                                  101
                                              96                                       69              62
                                         75                                       54
              54 53                                43
                      19                                21       17                         15                                17                        19
         7                 6   1                             7                                     0                                                         1
    0    1    2   3   4    5   6    0    1    2    3    4    5    0    1     2    3    4    5      0   1    2      3     4    5       0       1    2    3    4

   (a) definition_shape            (b) logical_shape             (c) subject_matter              (d) surface_features                (e) vocabulary

Figure 18: Per-item tag cardinality across the five tagging dimensions (N =554 items). Each panel
shows how many tags an item carries within the named dimension; bar heights are item counts
(also printed above each bar). Cardinality 0 means the item has no tag in that dimension. Counts:
definition_shape max 414 (zero-tag), logical_shape max 312, subject_matter max 223,
surface_features max 197, vocabulary max 259. Y-scales are panel-specific so the shape of
each distribution is visible.


Logical shape (Fig. 21). The logical-shape axis isolates the effect of the statement’s top-level con-
nective and quantifier structure, holding subject matter fixed. Items with single-clause, well-quantified
shape pass more often: negative-claim (+12.7 pp), iff (+8.2 pp), conjunctive (+7.2 pp),
universal (+6.0 pp), and conditional (+3.1 pp) all help. Items that involve case-splitting
or witness-construction underperform: disjunctive (−17.6 pp), existential (−12.0 pp), and
mixed-quantifier (−4.0 pp). quantifier-free items, which in this benchmark almost exclu-
sively appear inside syntactic lemmas operating on raw formulas, also lose −16.2 pp. multi-part
statements lose −5.2 pp, consistent with a model that handles a single conditional fluently but de-
grades when the prose enumerates several sub-claims. The pattern is consistent with what one would
expect of a translator that is fluent in standard mathematical phrasing but struggles to invent witnesses
or manage case splits at the type level.

Vocabulary (Fig. 22). The vocabulary axis shows the single largest negative effect on the en-
tire benchmark: binders-substitution, −12.9 pp at n=674 trials. Any item whose statement
requires reasoning about variable capture, α-renaming, or substitution machinery is formalized
substantially less reliably, and because LCS-Bench is derived from a logic textbook, 37 % of items are
tagged this way. numeric-arithmetic (−8.2 pp) and string-level (−6.5 pp) reasoning, both
of which typically require fixing a concrete representation, also hurt. The positive end is dominated


                                                                       24
                                                   pass-rate difference (with − without)

                                                -0.2      -0.1        0        0.1         0.2




                  references-figure (n=131)                                                            −0.161 ***

                 informal-notation (n=149)                                                             −0.159 ***

                 concrete-instance (n=451)                                                             −0.136 ***

                         len-long (n=266)                                                              −0.109 ***

               enumerated-clauses (n=418)                                                              −0.102 ***

                      uses-ellipsis (n=484)                                                            −0.077 ***

                     len-medium (n=1020)                                                               −0.061 ***

                 name-introducing (n=455)                                                              +0.061 **

               uses-metavariable (n=1515)                                                              +0.081 ***

                         len-short (n=664)                                                             +0.125 ***


Figure 19: Per-tag pass-rate difference for surface_features. Length buckets (len-short,
len-medium, len-long) are included and show a monotone effect: shorter items pass at +12.5 pp
while longer items lose −10.9 pp. Same conventions as Fig. 20.

                                                       pass-rate difference (with − without)

                                                   -0.2      -0.1         0          0.1         0.2




                           algorithm (n=198)                                                             −0.193 ***

                          syntactic (n=1645)                                                             −0.164 ***

                         object-level (n=379)                                                            −0.097 ***

                       meta-theorem (n=562)                                                              +0.006

             bridges-syntax-semantics (n=369)                                                            +0.164 ***

                           semantic (n=603)                                                              +0.196 ***


Figure 20: Per-tag pass-rate difference for subject_matter, aggregated over six runs of Opus 4.6 on
track1_v3 (N =1950 item–run trials). Bar = rate(items with tag) − rate(items without tag). Stars: *
p<.05, ** p<.01, *** p<.001 (two-proportion z-test). Tags with nwith <20 or nwithout <20 omitted.


by abstract, mathlib-shaped vocabulary: higher-order (+17.9 pp) and set-theoretic (+7.5 pp)
items pass much more often, presumably because abstract operators are easier to map to Lean’s
standard library and to predicate definitions than concrete encodings are. The take-away is concrete:
if substitution and binder-correctness reasoning could be brought up to the pass rate of the rest of the
benchmark, the overall Track 1 pass rate would rise by an estimated 4–5 pp—which would be the
single largest absolute gain available from any tag-conditioned intervention.

Definition shape (Fig. 23). Definition-shape tags fire only on the ∼30% of items whose role
is to introduce a new construct, so the absolute counts are smaller. predicate-definition
items pass at +12.2 pp, the largest definitional gain on the axis—introducing a new Prop-
valued judgement is mostly a syntactic exercise that maps cleanly onto Lean inductive predi-
cates. The negatives are all data-type-shaped: mutual-recursion (−17.5 pp; n=24, the worst
offender on the axis), inductive-definition (−7.5 pp), and type-definition (−6.3 pp). Plain
function-definition, recursive-definition, and parametric items are near zero. The
asymmetry mirrors a practitioner-known pain point: defining a new Prop is straightforward, but
defining a recursive datatype that must satisfy Lean’s structural-recursion checker—especially within


                                                            25
                                                pass-rate difference (with − without)

                                             -0.2        -0.1       0        0.1        0.2



                      disjunctive (n=30)                                                          −0.176 *
                  quantifier-free (n=102)                                                         −0.162 ***
                     existential (n=198)                                                          −0.120 ***
                     multi-part (n=250)                                                           −0.052 *
                 equality-claim (n=118)                                                           −0.040
                mixed-quantifier (n=125)                                                          −0.040
                    conditional (n=389)                                                           +0.031
                      universal (n=752)                                                           +0.060 ***
                    conjunctive (n=245)                                                           +0.072 **
                             iff (n=132)                                                          +0.082 *
                  negative-claim (n=54)                                                           +0.127 *


      Figure 21: Per-tag pass-rate difference for logical_shape. Same conventions as Fig. 20.


                                                    pass-rate difference (with − without)

                                              -0.2        -0.1          0      0.1          0.2




              binders-substitution (n=674)                                                         −0.129 ***

               numeric-arithmetic (n=114)                                                          −0.082 *

                      string-level (n=167)                                                         −0.065 *

                        infinitary (n=108)                                                         −0.056

                     set-theoretic (n=613)                                                         +0.075 ***

                      higher-order (n=90)                                                          +0.179 ***


       Figure 22: Per-tag pass-rate difference for vocabulary. Same conventions as Fig. 20.



a mutual block—is a frequent source of hand-tuning even for human formalizers, and the auto-
formalizer reproduces that gap.


D.4   Reasoning effort vs. outcome

Figure 24 reports the distribution of reasoning tokens per attempt, conditioned on outcome (pass vs.
fail) and broken down by tag. The data are pooled from the three thinking-mode Opus 4.6 runs that
emit reasoning traces; the metric is approximate (#chars/4, the standard Anthropic-API conversion)
and the y-axis is on a log scale. Two patterns are visible across every dimension. First, the fail-side
median is consistently 4–6× higher than the pass-side median: when the model gets an item right
it does so quickly, and when it gets an item wrong it spends an order of magnitude more reasoning
tokens on it. This is a strong signal that test-time compute is not the binding constraint on the hard
items in LCS-Bench—budgeting is not the issue, the model is failing after sustained deliberation.
Second, the spread is wider on the fail side than on the pass side, which is consistent with the model
exploring multiple unsuccessful strategies before timing out or emitting a malformed submission.
Read together with the per-tag pass-rate analysis above, the violins suggest that the gains available
from purely scaling reasoning length are limited; the high-leverage interventions are the structural
ones identified in Sec. D.3, in particular better handling of binder/substitution reasoning and of
mutual / inductive type definitions.


                                                            26
                                                                            pass-rate difference (with − without)

                                                                       -0.2       -0.1       0         0.1          0.2




                                   mutual-recursion (n=24)                                                                      −0.175 *

                               inductive-definition (n=144)                                                                     −0.075 *
                                    type-definition (n=197)                                                                     −0.063 *

                                             notational (n=48)                                                                  −0.050

                                        parametric (n=424)                                                                      −0.011

                               recursive-definition (n=102)                                                                     −0.007

                               function-definition (n=228)                                                                      +0.027

                                  defines-multiple (n=323)                                                                      +0.033

                               predicate-definition (n=281)                                                                     +0.122 ***


                     Figure 23: Per-tag pass-rate difference for definition_shape. Same conventions as Fig. 20.

                     5000
# Reasoning Tokens




                                 Correct Answers
                                 Incorrect Answers
                     1000
                      500
                      100
                       50
                             concrete-instance uses-metavariable references-figure name-introducing informal-notation         uses-ellipsis enumerated-clauses

                                                     (a) Reasoning tokens by surface_features.

                     5000
# Reasoning Tokens




                                 Correct Answers
                                 Incorrect Answers
                     1000
                      500
                      100
                       50
                                  semantic       bridges-syntax-semantics     syntactic          meta-theorem             object-level         algorithm

                                                       (b) Reasoning tokens by subject_matter.
 Figure 24: IAF reasoning-token distribution per attempt, split by correctness (left half / green: items
 the model passed; right half / red: items it did not), aggregated over three Opus 4.6 thinking-mode
 runs (694 item–trials with non-zero thinking content). Within each tag, the violin’s left half is the
 distribution over correct attempts and the right half over incorrect attempts; horizontal bars mark
 the medians. The y-axis is on a log scale. (a) Grouped by surface_features tag (length buckets
 len-short/len-medium/len-long omitted). (b) Grouped by subject_matter tag. Tags with
 fewer than two items on either side are dropped; tags are ordered left-to-right by overall median.


 D.5                  Take-aways

Three patterns recur across the five tagging dimensions. (i) Form matters as much as content.
Surface features alone (length, ellipses, figure references) move the pass rate by 10–16 pp, before
any mathematical structure is considered. (ii) Semantic content is easy; syntactic infrastructure
is hard. Items about models and truth pass at roughly 2–3× the rate of items about derivations
and formulas, even though the textbook spends most of its pages building exactly that syntactic
infrastructure. (iii) Within the syntactic side, the dominant single difficulty is binder/substitution


                                                                                    27
reasoning, which together with mutual / inductive type-definitions accounts for the largest absolute
gaps on the benchmark and points to the most actionable direction for future work on theory-scale
auto-formalization.




                                                28
