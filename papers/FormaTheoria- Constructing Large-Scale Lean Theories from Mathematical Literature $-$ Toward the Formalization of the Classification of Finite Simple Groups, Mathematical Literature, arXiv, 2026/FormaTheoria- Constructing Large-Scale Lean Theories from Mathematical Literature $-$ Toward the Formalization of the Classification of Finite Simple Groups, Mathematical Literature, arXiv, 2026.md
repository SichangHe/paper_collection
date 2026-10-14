                                           F ORMAT HEORIA: Constructing Large-Scale Lean Theories from
                                                            Mathematical Literature
                                               Toward the Formalization of the Classification of Finite Simple Groups


                                                         Tianjiao Nie                      Ao Zhang                        Yusen Tang
                                                      Qiuzhen College                  Qiuzhen College                  Qiuzhen College
                                                     Tsinghua University              Tsinghua University              Tsinghua University
                                                              Damiano Testa                                Shing-Tung Yau*
                                                        Department of Mathematics                  Yau Mathematical Sciences Center
arXiv:2608.10894v1 [cs.LO] 11 Aug 2026




                                                          University of Warwick                         Tsinghua University
                                                                  Peng Li∗                                         Yuan Zhou∗
                                                 Institute for AI Industry Research (AIR)                 Yau Mathematical Sciences Center
                                                            Tsinghua University                                Tsinghua University



                                                                                              Abstract
                                                   Large-scale formalization of advanced mathematics requires more than translating individual state-
                                              ments: it must reconstruct a coherent theory distributed across heterogeneous sources. This process
                                              raises four challenges: discovering implicit dependencies, correcting source defects, preserving seman-
                                              tic fidelity, and reconciling cross-source misalignments. We present F ORMAT HEORIA, an end-to-end,
                                              AI-assisted workflow that coordinates source acquisition, formalization, proof construction, recursive de-
                                              pendency discovery, independent review, and reconciliation, while preserving provenance and protecting
                                              approved declarations. A shared agent framework supports long-horizon execution through tool use, con-
                                              text compaction, review-gated termination, section-level source context, and dependency-aware batch
                                              parallelization. Applying F ORMAT HEORIA to major components of the Classification of Finite Simple
                                              Groups (CFSG), we construct a machine-checked Lean development extending through the Bender–
                                              Suzuki theorem and encompassing the Feit–Thompson Odd Order Theorem, Glauberman’s Z ∗ theorem,
                                              and the Brauer–Suzuki theorem. This development verifies an extensive body of deeply interdependent
                                              finite-group theory while providing a foundation for continuing the CFSG formalization. An empirical
                                              analysis of the code and recorded construction process supports the practical relevance of the identified
                                              challenges and illustrates the roles of the corresponding workflow components. Together, these results
                                              demonstrate how AI-assisted workflows can reconstruct mathematically significant formal theories from
                                              distributed literature by combining language-model agents with formal verification, structured review,
                                              and explicit dependency management.




                                            * Correspondence to: Shing-Tung Yau <styau@tsinghua.edu.cn>, Peng Li <lipeng@air.tsinghua.edu.cn>

                                         and Yuan Zhou <yuan-zhou@tsinghua.edu.cn>.
Contents
1   Introduction                                                                                            3
    1.1 Challenges of Large-Scale Source-Based Formalization . . . . . . . . . . . . . . . . . . . .        6
    1.2 Our Contributions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   7
    1.3 Empirical Observations and Design Implications . . . . . . . . . . . . . . . . . . . . . . .        8

2   F ORMAT HEORIA: Formalization Model and Workflow                                                     9
    2.1 Source Items and Formalizations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
    2.2 Classification of the Issues in Autoformalization Process . . . . . . . . . . . . . . . . . . . 11
    2.3 Workflow Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12

3   Agent Components and Review Procedures                                                                  15
    3.1 Shared Agent Framework . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      15
    3.2 P ROVER . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   17
    3.3 T RANSLATOR AGENT . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       20
    3.4 R ECONCILER AGENT . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       21

4   Implementation Considerations                                                                       23
    4.1 Section-Level Context Sharing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
    4.2 Dependency-Aware Batch Parallelization . . . . . . . . . . . . . . . . . . . . . . . . . . . 23

5   Empirical Findings from Large-Scale Formalization                                                       24
    5.1 Distributed Sources and Deep Dependencies . . . . . . . . . . . . . . . . . . . . . . . . . .       24
        5.1.1 Distributed Source Discovery . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        24
        5.1.2 Source Length and Formalization Burden . . . . . . . . . . . . . . . . . . . . . . .          25
        5.1.3 Depth and Connectivity of the Declaration Dependency Graph . . . . . . . . . . . .            27
    5.2 Source Defects and Misalignments Identified during the Formalization Process . . . . . . .          30
    5.3 Examples of Automatically Fixed Translation Mistakes . . . . . . . . . . . . . . . . . . . .        32
    5.4 Reconciliation Hotspots and Repair Boundaries . . . . . . . . . . . . . . . . . . . . . . . .       33
    5.5 Review as an Iterative Quality Gate . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     37
    5.6 Comparison with Existing Rocq Formalization . . . . . . . . . . . . . . . . . . . . . . . .         37

6   Ablation Studies                                                                                        40
    6.1 Parallel versus Sequential Proof Construction . . . . . . . . . . . . . . . . . . . . . . . . .     40
    6.2 Effect of Section-Level Context Sharing . . . . . . . . . . . . . . . . . . . . . . . . . . . .     41
    6.3 Diagnostic Feedback in Translation Review . . . . . . . . . . . . . . . . . . . . . . . . . .       42

7   Conclusion                                                                                              43

A Formalized Theorems                                                                                       49

B Prompts                                                                                                   51




                                                      2
1    Introduction
Formal mathematics represents definitions, statements, and proofs in languages whose declarations can be
checked by a small trusted kernel. It has enabled machine-checked proofs of major results and the construc-
tion of increasingly extensive libraries of verified mathematics. Proof assistants such as Rocq (formerly
Coq) [8], Lean [39], Isabelle/HOL [40], and HOL Light [27] have enabled landmark human-driven formal-
ization projects, while recent language-model and search-based systems have made substantial progress in
statement formalization and theorem proving. These developments demonstrate the growing capacity of
formal methods to verify sophisticated mathematics, but most existing projects and AI systems begin with a
designated theorem, a curated proof plan, or an already constructed formal environment.
    The Classification of Finite Simple Groups (CFSG) presents a different challenge. Its proof is dis-
tributed across a large and historically layered literature whose dependencies, definitions, conventions,
and representations must be recovered and aligned during formalization. We introduce F ORMAT HEORIA,
an AI-assisted workflow for reconstructing the required mathematics from this literature as a coherent,
dependency-connected Lean theory. Starting from target results in the literature, the workflow discovers and
formalizes required dependencies, reconciles incompatible mathematical interfaces, and integrates approved
declarations into an evolving formal development. The literature provides the mathematical basis for this
construction but does not prescribe a literal reproduction of its organization or presentation. F ORMAT H -
EORIA normally preserves the mathematical content of each source item, while permitting corrections or
reconciliations when the literature contains defects or cross-source misalignments.

Importance and difficulty of formalizing CFSG. The Classification of Finite Simple Groups (CFSG)
is one of the defining achievements of modern mathematics. By the Jordan–Hölder theorem, the simple
composition factors of a finite group are determined, up to isomorphism and reordering, by the group it-
self. Finite simple groups therefore serve as the irreducible building blocks of finite-group theory. CFSG
identifies all such groups: cyclic groups of prime order, alternating groups, groups of Lie type, and the
sporadic groups. The classification consequently provides fundamental structural infrastructure for finite-
group theory and supports applications in number theory, algebraic and arithmetic geometry, combinatorics,
and related areas [44, 43]. A formal development of CFSG would make this infrastructure available as a
mechanically checked and reusable foundation for subsequent formal mathematics.
     The scale and organization of the proof make CFSG an exceptionally difficult target for formalization.
Its first-generation proof emerged over several decades through contributions from approximately one hun-
dred mathematicians and remains dispersed across hundreds of papers and books [44, 17]. These sources
were written independently, at different times, and for different purposes; they frequently leave dependencies
implicit and may employ different definitions, conventions, representations, and assumptions. The history of
CFSG also illustrates the difficulty of verifying such an extensive and distributed argument. After the clas-
sification had been announced, the quasithin case remained a gap for more than two decades and ultimately
required the two-volume work of Aschbacher and Smith [3]. Harada and Solomon later repaired another
omitted case involving a standard component of type M    c22 [26]. The continuing second-generation program
seeks to reorganize the proof into a more coherent account, but this program itself spans many volumes
and remains a major undertaking. Formalizing CFSG therefore requires the reconstruction of a coherent,
dependency-connected theory from a historically layered body of literature. A machine-checked devel-
opment would make dependencies and hypotheses explicit, document cross-source identifications, expose
defects or incompatibilities encountered during construction, and provide stable formal interfaces through
which later results could invoke the classification. It would thereby turn one of the most extensive collective


                                                      3
achievements in mathematical history into an auditable and reusable formal theory.

Comparison with major formalization projects. Major formalization projects have demonstrated that
proof assistants can verify mathematical arguments whose length, computational content, or structural com-
plexity extends far beyond the scale of an ordinary paper. Human-led projects have produced machine-
checked proofs of the Four Color Theorem, the Feit–Thompson Odd Order Theorem, and the Kepler con-
jecture [13, 14, 24]. More recently, the Liquid Tensor Experiment showed that Lean and Mathlib can support
rapid, collaborative formalization at the frontier of contemporary mathematical research [10]. In parallel,
general-purpose libraries such as Mizar, the Archive of Formal Proofs, and Mathlib have accumulated ex-
tensive bodies of reusable formal mathematics across a broad range of subjects [48, 5].
     These developments exhibit different forms of scale. General-purpose libraries derive their scale from
the breadth of the mathematics accumulated across many areas and contributors. Theorem-centered projects
derive theirs from the depth and complexity of formalizing a designated result, typically using a curated
blueprint or a small number of systematic expositions. Our development presents a third setting: con-
structing a dependency-connected theory whose constituent results and mathematical interfaces must be
recovered from a large and heterogeneous literature. Table 1 compares representative projects along three
dimensions: approximate code volume, mathematical scope, and the organization of their source material.
Because proof assistants, repository boundaries, and counting conventions differ, the reported figures pro-
vide order-of-magnitude context rather than normalized measurements.
     By raw code volume, our development comprises more than 994,000 lines.1 As a rough indication of
codebase size, this exceeds half of the 1.9 million lines reported for Mathlib in 2025. The more consequential
distinction concerns the organization and scope of the formalized mathematics. Unlike a general-purpose
library, our development is directed toward a connected sequence of structural results in finite-group theory.
Unlike a theorem-centered project, it does not begin with a single curated formalization blueprint. It instead
integrates results recovered from independently written books and papers into a coherent Lean theory while
preserving consistency across their formal interfaces. The project’s scale therefore reflects both the volume
of its formal development and the breadth and depth of the dependency-connected theory that it reconstructs.
Section 5 examines this latter dimension more closely through the declaration-dependency graph and a
section-by-section comparison with the Rocq formalization of the Odd Order Theorem.

Comparison with AI-assisted proof construction. Recent AI-assisted theorem-proving systems have
substantially expanded the range of formal proof obligations that can be addressed automatically. Pretrain-
ing on mathematical text, source code, and formal proofs supports the interpretation of informal mathematics
and the generation of proof-assistant syntax [4]. Reasoning-oriented post-training, inference-time search,
and proof-assistant feedback further support the decomposition, verification, and iterative repair of multi-
step arguments [49, 50, 32]. These techniques provide complementary capabilities for translating mathe-
matical content and constructing mechanically checked proofs. Benchmarks and theorem-proving systems
demonstrate substantial progress on individual formalization and proof tasks. miniF2F comprises 488 in-
dependently posed competition-level statements, while LeanDojo extracts 98,734 theorem–proof pairs from
Mathlib [53, 51]. DeepSeek-Prover, AlphaProof, and Aristotle employ different combinations of synthetic
data, learned reasoning, verifier feedback, and inference-time proof search [49, 50, 32, 1]. Autoformalization
benchmarks extend the task to translating natural-language statements, but typically treat these statements
as separate inputs [52]. miniCTX incorporates repository context spanning tens of thousands of tokens,
    1
      Unless otherwise stated, all quantitative figures reported for our development refer to a snapshot taken when the proofs were
first completed, before subsequent cleanup and additions; Section 5 analyzes this snapshot.


                                                                4
 Development         Formal system and        Reported scale: code volume       Organization of the mathematical
                     scope                    and effort                        source
 Mathlib [5]         Lean; broad commu-       1.9 million lines (2025); ongo-   General-purpose library spanning
                     nity library             ing since 2017                    many mathematical subjects and
                                                                                contributors
 Odd Order [14]      Rocq;          Feit–     ∼150,000 lines with libraries     One theorem reconstructed princi-
                     Thompson theorem         (∼40,000 for the theorem it-      pally from two systematic exposi-
                                              self); 6 years                    tions
 Flyspeck [24, 23]   HOL Light & Is-          ∼500,000 lines; eleven years      One proof, including its com-
                     abelle; Kepler conjec-   (2003–2014); ∼20 work-years       putational components, organized
                     ture                                                       around a project-specific revised
                                                                                blueprint
 Liquid   Tensor     Lean; one research       ∼90,000 lines [9];        ∼18     One designated theorem devel-
 Experiment [10]     theorem                  months (2020–2022)                oped through a shared blueprint
                                                                                and specification-driven collabo-
                                                                                ration, by about a dozen math-
                                                                                ematicians and several computer
                                                                                scientists
 F ORMAT HEORIA      Lean; several CFSG       More than 994,000 lines in        A heterogeneous literature whose
 (this work)         components forming       more than 850 files, and          sources, dependencies, defini-
                     one      dependency-     30,298 declarations reachable     tions, and conventions must be
                     connected theory         from Bender–Suzuki1 ; ∼7          discovered and aligned during for-
                                              months                            malization

Table 1: A comparison of the scope and scale of representative formal-mathematics developments. Each
row reports the code volume and the effort as the project itself reports them; the figures are not normalized
across formal systems, and line counts in particular are not comparable between them.


thereby accounting for definitions, lemmas, notation, and file-level information beyond the immediate proof
state [30].
     Despite their methodological differences, these settings generally assume that the target theorem and
its surrounding formal environment have already been specified. In conventional theorem proving, a formal
context Γ and target type τ are given, and the task is to construct a proof term p such that Γ ⊢ p : τ . Statement
autoformalization additionally constructs τ from a supplied natural-language statement, but usually does so
relative to an existing formal context. The principal challenge is therefore to translate or prove an individual
target using definitions, notation, and supporting results that are already available.
     F ORMAT HEORIA addresses a different task: constructing and extending the formal context required
to state and prove the target results. Starting from a source item and an existing approved Lean context,
the workflow must determine which additional definitions and theorems are required, locate and interpret
their sources, formalize newly discovered dependencies, reconcile incompatible mathematical interfaces,
and integrate the resulting declarations without altering approved mathematical content. These activities
are interdependent: proof attempts may expose missing dependencies, source inspection may reveal defects
or misalignments, and reconciliation may create new proof obligations. Because this process can span
many agent interactions and exceed a single model context, F ORMAT HEORIA maintains persistent structured
project state, retrieves task-relevant information, and compacts earlier interactions while preserving essential


                                                        5
mathematical decisions.
    The distinction therefore lies in the unit of construction and evaluation. Existing AI-assisted proving
systems generally construct an individual statement or proof relative to a specified target and formal project.
F ORMAT HEORIA instead produces the elaborated, dependency-resolved, and internally coherent Lean the-
ory required to state and establish the target results without unsupported axioms. Semantic review therefore
evaluates whether each formalization is mathematically supported by its sources and whether any departures
are justified, rather than requiring literal fidelity to the source presentation.

1.1   Challenges of Large-Scale Source-Based Formalization
Large-scale source-based formalization must recover the required mathematical statements and dependen-
cies as formalization proceeds. Proof construction must therefore be coordinated with source acquisition,
dependency discovery, cross-source alignment, semantic translation, and source validation. This setting
gives rise to four interdependent challenges, denoted C1–C4.

C1: Distributed sources and deep dependencies. The source corpus comprises numerous books and
papers rather than a single self-contained exposition. Dependencies frequently cross source boundaries,
and a cited result may itself depend on a substantial chain of earlier results. Moreover, an individual proof
in the literature may extend over many pages and invoke intermediate results whose relevance becomes
apparent only during formalization. Formalizing a target theorem therefore requires the system to discover
and reconstruct a large, evolving dependency context. An omitted or incorrectly identified dependency may
prevent subsequent formalization even when the local proof argument is otherwise valid.

C2: Misalignments across mathematical sources. Because the source corpus is distributed across inde-
pendently written books and papers, its constituent sources need not adopt a common system of definitions,
conventions, notation, or representations. Two sources may define the same object under different con-
ventions, introduce extensionally equivalent formulations through distinct mathematical constructions, or
use the same name for different objects. A downstream source may also move between such formulations
without explicitly specifying the required identification. Consequently, formalizations that are individually
faithful to their respective sources may not be directly composable in Lean. Addressing these cross-source
misalignments may require bridging equivalences, conversion constructions, or permitted revisions to can-
didate formalizations.

C3: Semantically incorrect Lean translations. Natural-language definitions and theorem statements
must be interpreted in their documented mathematical context, since standing assumptions and conventions
may be left implicit. A Lean declaration may nevertheless elaborate successfully while misrepresenting
the source, for example, by omitting or altering an assumption, mistranslating a quantifier, encoding a
different mathematical object, or strengthening or weakening a conclusion. Lean’s elaborator establishes
well-typedness, not semantic fidelity. Such errors may therefore remain undetected by Lean and propagate
to subsequent formalizations. Semantic fidelity must accordingly be assessed independently of elaboration
and provability, against both the source item and its surrounding context.

C4: Defects in the mathematical sources. The mathematical sources may themselves contain typograph-
ical errors, missing conditions, ambiguous formulations, incomplete arguments, or incorrect statements.



                                                      6
Such defects may initially be difficult to distinguish from errors introduced during source transcription, de-
pendency reconstruction, translation, or proof construction. In particular, the failure to prove a faithfully
translated statement may reflect a defect in the source rather than a limitation of the proof procedure. The
formalization workflow must therefore retain sufficient source context to diagnose the discrepancy and must
report cases that cannot be resolved without mathematical judgment for human investigation.
    These challenges arise at distinct interfaces but interact closely. A missing dependency may make a
correct translation appear unprovable, a cross-source misalignment may resemble a translation error, and
either a semantic translation error or a source defect may become apparent only during downstream proof
construction. The workflow introduced in Section 2 therefore addresses these challenges through distinct
but coordinated mechanisms.

1.2     Our Contributions
To address these challenges, we introduce F ORMAT HEORIA. The principal contributions of this paper are
as follows.

      • We develop an end-to-end workflow that coordinates source acquisition, formalization, proof con-
        struction, dependency discovery, review, and reconciliation at scale. The workflow preserves prove-
        nance, protects approved declarations in a persistent library, and records unresolved issues for hu-
        man investigation. It is implemented through a shared agent framework designed for long-horizon
        formalization, combining multi-turn language-model interaction with Lean and other tools, context
        compaction, review-gated termination, section-level source context, and dependency-aware batch par-
        allelization. Sections 2, 3 and 4 describe the overall workflow, its constituent components, and the
        associated implementation considerations, respectively.

      • We construct a large-scale Lean formalization of major components of the CFSG program, extend-
        ing through the Bender–Suzuki theorem and encompassing the Feit–Thompson Odd Order Theo-
        rem, Glauberman’s Z ∗ theorem, and the Brauer–Suzuki theorem. The resulting development ver-
        ifies an extensive body of deeply interdependent finite-group theory and establishes a foundation
        for continuing the formalization of the CFSG. The Lean code for this development is available at
        https://github.com/Qiuzhen-CFSG/CFSG.

      • We conduct an empirical analysis of the resulting Lean code and its recorded construction process.
        The analysis examines the expansion and structure of source dependencies, the distribution of source
        defects and cross-source reconciliations, semantic-review outcomes, and the development’s scale and
        construction time in comparison with the human-developed Rocq formalization. These observations
        support the practical relevance of the challenges identified above and illustrate how the corresponding
        workflow components address them. Section 1.3 summarizes the principal observations and design
        implications, while Section 5 presents the detailed analysis.

      • We experimentally evaluate three core workflow mechanisms through controlled ablation studies. On
        the evaluated targets, dependency-aware parallelism reduced proof-construction wall time by 76.1%
        (4.2×), whereas section-level context sharing reduced wall time by 26.5% and total token consump-
        tion by 18.0%. A pilot study of ten source items further found 6/10 correct translations without review,
        9/10 with diagnostic review feedback, and 10/10 with a self-improved review rubric. These results
        quantify the tradeoff between elapsed time and inference cost and provide evidence that context reuse


                                                        7
      and source-grounded review feedback contribute to construction efficiency and translation fidelity.
      Section 6 presents these studies.

1.3   Empirical Observations and Design Implications
At the completion-time snapshot analyzed in Section 5, our workflow had completed Lean formalizations of
the Feit–Thompson Odd Order Theorem, Glauberman’s Z ∗ theorem, the Brauer–Suzuki theorem, and the
Bender–Suzuki theorem (Appendix A). These results form a connected theoretical progression rather than
four interchangeable targets: Odd Order excludes nonabelian finite simple groups of odd order; Glauber-
man’s Z ∗ and Brauer–Suzuki convert information about involutions and Sylow 2-subgroups into global
restrictions; and Bender–Suzuki culminates in the classification of finite simple groups with strongly em-
bedded subgroups. The Odd Order development was independently reconstructed principally from Bender–
Glauberman and Peterfalvi [7, 42], rather than translated or ported from the existing Rocq formalization
[14]; a shared source decomposition did not determine the same proof route or declaration structure. Extend-
ing this chain through Bender–Suzuki required a broader and more heterogeneous literature. The resulting
repository contained more than 994,000 lines of Lean in more than 850 files.
    Taken together, the resulting formalization and its recorded construction process yield four empirical
observations and associated design implications for large-scale formalization. The first three support the
practical relevance of Challenges C1–C4 and illustrate the roles of dependency discovery, source correction
and reconciliation, and layered semantic review in addressing them. The fourth concerns the quality of the
resulting formal artifact.

The scope and difficulty of a large formalization emerge through dependency discovery. The results
support the practical relevance of Challenge C1: the required source corpus and mathematical infrastructure
cannot necessarily be specified in advance. The three human-supplied sources served only as entry points,
while recursive dependency discovery added twelve further sources, accounting for 680 consulted pages, or
65.6% of the total. Moreover, the resulting dependency graph combines a broad, shallow base with a narrow
but exceptionally deep backbone. In the Bender–Suzuki project-only closure, 29.4% of declarations have
depth zero and the median depth is two, whereas the root has depth 458. These findings indicate that source
page count alone is a poor measure of formalization difficulty; the discovered dependency structure also
determines the required infrastructure, the critical proof paths, and the opportunities for parallel construc-
tion. They therefore motivate the workflow’s recursive dependency-discovery and dependency-management
components (Section 5.1).

Source defects and cross-source misalignments require distinct but coordinated responses. The de-
velopment provides evidence for Challenges C2 and C4. It exposed hidden assumptions, missing hypothe-
ses, an incorrect divisibility condition, and an indexing error, while also encountering incompatible defini-
tions and representations across sources. These two classes of problems require different responses: source
defects must be corrected or explicitly justified against the relevant mathematical context, whereas cross-
source misalignments require conversion lemmas, compatibility bridges, or reconciled interfaces. The ob-
served modifications were concentrated at representation-heavy interfaces rather than distributed uniformly
by source size or declaration count, suggesting that a relatively small number of carefully designed rec-
onciliations can stabilize many downstream declarations. When no source-supported correction or bridge
is available, however, the issue must be preserved and escalated for mathematical judgment. These ob-
servations motivate the workflow’s separation of source correction, cross-source reconciliation, and human


                                                      8
intervention (Sections 5.2 and 5.4)

Semantic fidelity requires review beyond kernel verification. The review outcomes illustrate Chal-
lenge C3: Lean elaboration establishes that a term has its stated type, but does not establish that the type
represents the source result in its documented context. Eleven of the fourteen PF Part I sections were re-
turned after their first review, showing that mechanically valid formalizations may still require semantic revi-
sion. The workflow therefore combines elaboration and axiom checks with independent review of translated
declarations and root theorem statements. This review must also distinguish mistranslation from missing
dependencies, source defects, and cross-source misalignments, since these failure modes can produce simi-
lar symptoms during proof construction. Automation can perform much of the checking and revision, while
human judgment remains necessary when the intended interpretation is ambiguous or a repair lacks clear
source support. The evidence thus illustrates the value of layered review that concentrates human attention
at unresolved semantic boundaries (Sections 5.3 and 5.5).

Construction efficiency and artifact quality are distinct objectives. In the comparison considered here,
the automatically constructed Lean development was completed over a shorter wall-clock period but con-
tains substantially more code than the human-developed Rocq formalization. These figures are not normal-
ized measures of effort, readability, or quality, but they indicate that rapid construction does not by itself
produce a concise and reusable library. Large-scale autoformalization should therefore be evaluated not only
by the amount of verified mathematics produced, but also by the stability of its abstractions, the transparency
of its proofs, and its potential for integration into reusable mathematical libraries (Section 5.6). This obser-
vation also motivates the future direction, discussed in Section 7, of improving the quality and reusability of
AI-generated formalization code.


2     F ORMAT HEORIA: Formalization Model and Workflow
This section presents the formalization model and high-level workflow through which F ORMAT HEORIA
constructs approved Lean formalizations of natural-language source items. Figure 1 provides an overview
of F ORMAT HEORIA, showing how its principal workflow components address the four challenges and how
the underlying agents are executed through a shared agent framework. The remainder of this section de-
scribes the workflow in greater detail. Section 2.1 defines source items and their formalizations, together
with the approval rules that protect completed mathematical content. Section 2.2 classifies the principal
issues arising from Challenges C2–C4 that we encountered during autoformalization. Finally, Section 2.3
explains how F ORMAT HEORIA coordinates source retrieval and transcription, semantic translation, graph-
based proof construction, and on-demand dependency discovery; how the P ROVER procedure and R EC -
ONCILER AGENT address source defects and cross-source misalignments, respectively; and how unresolved
ambiguities, errors, and conflicts are escalated for human investigation.

2.1   Source Items and Formalizations
A source item is a pointer to a mathematical definition or theorem stated in natural language in mathematical
literature supplied by the user or discovered automatically. Here and throughout the paper, the term theo-
rem also encompasses results labeled as lemmas, propositions, or corollaries in the source. A source item
identifies both the source document and the relevant result, for example, by the document title and theorem
number. It thereby specifies what is to be formalized without reproducing the source text itself.


                                                       9
   PROJECT CHALLENGES & OUR SOLUTIONS

     C1
             Distributed dependencies                                                                  C2
                                                                                                             Cross-source misalignment
             Retain evidence; discover prerequisites recursively                                             Compare sources and formalizations; construct a local
             and on demand.                                                                                  compatibility repair.



     C3
             Semantic fidelity                                                                         C4
                                                                                                             Defective source material
             Lean checks + independent semantic review against                                               Proof-driven diagnosis + escalation for unsupported
             the original source material.                                                                   source material.


   WORKFLOW MECHANISMS
          FormaTheoria

       C1     Source item                               Search & OCR                              C3   TranslatorAgent                                                  Approval
                                                                                                  Construct candidate Lean declaration
                                                           SearchAgent                                                                           Definition
                                                      locate and retrieve literature
                                                                                                                   candidate fs
                                                                                                             Definition: type + term
                                                             OCRAgent                                        Theorem: type + sorry
                                                        reconstruct transcription                                                                                  Global persistent
               root item s                                                                                  ReviewAgent Gate                                            library
            definition or theorem
            in source document                          Sraw                Stex                       ✓ Lean elaboration                                           state = approved
                                                   pages/images         transcription                  ✓ Statement immutability
                                                                                                                                                   Failure
                                                                                                       ✓ Independent semantic review
                                                                                                                                                                        Definition
                                                                                                                                                                    type + term fixed
                                                                           MissingDependency(s′)
                       Recursive dependency                                                                         Theorem
                  C1
                       discovery                                                                                                                                          Theorem
                                                                                        C4    Prover                                     Proof                           type fixed
                  invoke FormaTheoria(s′)                                                    Graph-based proof construction
                        → approve f                                                                                                                                     except during
                                   s′                                                                                                                              authorized reconciliation
                       → resume current translation/proof                                                   root
                                                                                                              s

                                                                      repaired
                            C2      ReconcilerAgent                  candidate                                                prune
                                                                                                                                                              C2      Human
                           Compare sources + Lean
                                                                                                                                                                      Investigation
                                        formalizations               Conflict(s′)        ProveAgent
                                                                                         ProveAgent↔↔RefineAgent                                              C4
                                                                                                                                         Failure
                           Local compatibility repair                                   Review: elaboration • protected statements
                                                                                                • no unauthorized axioms




       Shared agent framework
       Used by TranslatorAgent, ProveAgent, RefineAgent, ReconcilerAgent

              Multi-turn LLM + tools                                      Context compaction                                           Review-gated termination




Figure 1: Overview of F ORMAT HEORIA. Starting from a root source item, the system retrieves and tran-
scribes the relevant source material, constructs a candidate Lean declaration, and, for a theorem, performs
graph-based proof construction before independent review and approval. Newly discovered dependencies
are formalized recursively, cross-source conflicts are handled by R ECONCILER AGENT, and unresolved de-
pendencies, source defects, and incompatibilities are escalated for human investigation. Approved formal-
izations are committed to the global persistent library under the stated immutability rules. The upper panel
maps the four principal challenges to their corresponding workflow components, while the lower panel sum-
marizes the shared agent framework through which the agents underlying these components are executed.



                                                                                               10
        For a source item s, a formalization is a tuple

                                           fs = (types , terms , Γs , states ),

  where Γs is a Lean context, types is a Lean type, and terms is a Lean term satisfying

                                                 Γs ⊢ terms : types .

  If s is a definition, then terms is the body of the definition, while types specifies the kind of mathematical
  object being defined. If s is a theorem, then types expresses its assumptions and conclusion, and terms is a
  proof of that statement under the Curry–Howard correspondence.
      The state of a formalization is

                                          states ∈ {candidate, approved}.

  A candidate formalization is still being constructed or repaired by the T RANSLATOR AGENT, P ROVE AGENT,
  or R ECONCILER AGENT. An approved formalization is regarded as complete. For a definition, approval
  means that its Lean body faithfully represents the mathematical definition in the source. For a theorem,
  approval means that its Lean type has the same mathematical meaning as the theorem statement and that
  its Lean term proves this type. Note that the mathematical content of a source item is interpreted in its
  documented context, including any standing hypotheses, local conventions, or preceding definitions needed
  to understand it. Accordingly, assumptions omitted from the displayed statement may be made explicit
  in Lean when they are unambiguously supplied by the surrounding text; doing so does not constitute a
  departure from the source.

  Global library and the approval rule. All source items and their formalizations are maintained in a
  global persistent library. Once a formalization fs is approved, both the type and term of a definition are
  fixed. For a theorem, the type is fixed, although its proof term may be replaced provided that the resulting
  code still elaborates. The only exception is that the R ECONCILER AGENT, as introduced later, may perform
  an authorized revision of an approved formalization when necessary to resolve incompatibilities among
  source-item formalizations.

  2.2     Classification of the Issues in Autoformalization Process
  In this section, we classify the principal issues encountered during the autoformalization process. These
  issues arise from Challenges C2–C4, and F ORMAT HEORIA incorporates corresponding mechanisms that
  attempt to address them automatically. This classification may not be exhaustive. Issues that the workflow
  cannot resolve automatically are escalated for human investigation.

  Source defects. As noted in Challenge C4, natural-language mathematical literature may contain errors
  that compromise the correctness of its mathematical content. We distinguish the following two types of
  source defect:

[D EF 1] A source item s contains a typographical or mathematical error in a definition or theorem statement,
         resulting in an incorrect definition, hypothesis, or conclusion.

[D EF 2] A source item s contains a typographical or mathematical error in the proof of a theorem, rendering
         one or more steps of the proof invalid.

                                                           11
   Source misalignments. As noted in Challenge C2, natural-language mathematical sources may leave
   conventions implicit, use the same terminology for different objects, or present equivalent concepts in for-
   mulations that are not directly interchangeable in Lean. We distinguish the following two types of source
   misalignment:

[M AL 1] Source items s1 and s2 give mathematically equivalent definitions of the same object, but the corre-
         sponding formalizations f1 and f2 are not definitionally equal in Lean.

[M AL 2] Source items s1 and s2 use the same name for distinct mathematical objects, while a downstream
         source item s3 implicitly treats these objects as identical.

   Incorrect Lean translations. This class of issues corresponds to Challenge C3 and concerns the semantic
   fidelity of T RANSLATOR AGENT when translating source definitions and theorem statements into Lean.
   An incorrectly translated theorem statement may render the intended theorem unprovable. An incorrectly
   translated definition or theorem statement may also prevent a formalized result from being applied to a
   downstream source item. We distinguish the following two types:

 [I N T1] A theorem source item s is translated into f , but the statement in f cannot be proved in Lean because
          the translation is incorrect.

 [I N T2] A source item s2 invokes s1 , but f1 cannot be applied directly in f2 because f1 incorrectly translates
          s1 .

       Section 5.2 presents representative source defects and misalignments identified in the literature during
   our project. Section5.3 presents representative examples of incorrect Lean translations produced by T RANS -
   LATOR AGENT.


   Addressing the issues identified above. We adopt different strategies for the types of issues identified
   above. A source defect of type [D EF 2] is typically detected and corrected during the P ROVER procedure
   introduced in Section 2.3. If P ROVER cannot resolve the defect while preserving the formalized statement,
   it escalates the issue for human investigation. Section 3.2 describes this procedure in detail. Some defects
   of type [D EF 1] can also be detected and corrected through this procedure. The remaining cases manifest in
   Lean as issues of type [I N T1] or [I N T2] and are handled using the corresponding procedures.
        A misalignment of type [M AL 1] can generally be addressed by introducing a helper lemma relating f1
   and f2 , for example, by establishing the equivalence of the two formalized definitions. A misalignment of
   type [M AL 2] manifests operationally as an issue of type [I N T2] when a downstream formalization attempts
   to use f1 in a context where f2 is expected. Such cases are therefore handled in the same manner as issues
   of type [I N T2]. To address issues of types [I N T1] and [I N T2], we introduce R ECONCILER AGENT, which
   diagnoses their underlying causes and constructs local, source-based repairs. Section 2.3 situates this agent
   within the overall workflow, while Section 3.4 describes its operation in detail.

   2.3   Workflow Overview
   F ORMAT HEORIA constructs an approved Lean formalization of a root source item together with the relevant
   source items on which it depends. This process extends beyond the translation of an isolated passage. As
   shown in Figure 1, the system retrieves and transcribes the relevant source material, constructs the Lean
   statement or definition, proves the statement when the source item is a theorem, and checks the resulting


                                                        12
artifacts. During translation and proof construction, the system discovers additional source items that are
required to state or prove the current item. It recursively formalizes these dependencies and then resumes
the interrupted task in the enlarged Lean context.
     Dependencies are therefore discovered on demand. The system does not require a complete dependency
structure to be supplied in advance. A dependency may be identified while translating the mathematical
statement or while constructing its proof. In either case, the F ORMAT HEORIA suspends the current task,
invokes itself on the missing source item, and restarts or resumes the current task after the dependency has
been approved.
     Previously formalized material may rely on definitions, assumptions, notation, or representations that
are incompatible with the source item currently under consideration. Such incompatibilities may arise from
source defects, source misalignments, or translation errors and manifest as issues of type [I N T2], as defined
in Section 2.2. When such an incompatibility is detected, R ECONCILER AGENT compares the relevant
sources and Lean formalizations and attempts to construct a repair. R ECONCILER AGENT may also address
issues of type [I N T1]. In such cases, P ROVER may determine that the current theorem s is unprovable
as translated and identify a potential conflict involving a previously formalized source item s′ that invokes
s. R ECONCILER AGENT then compares the statement of s with the context in which s′ invokes it and
seeks an appropriate repair. In either case, the repair may revise the current candidate, introduce a justified
compatibility construction, replace the proof term of an approved theorem without changing its statement,
or revise explicitly authorized theorem statements. The system does not make unauthorized changes to the
protected mathematical content of an approved formalization merely to achieve successful Lean elaboration.
     The workflow escalates a task when the agents cannot produce a supported translation, proof, or rec-
onciliation. Human investigation may then examine the sources and Lean code, edit the formalization,
provide additional instructions to an agent, or invoke the F ORMAT HEORIA on another source item. Thus,
human intervention is reserved for cases in which the automated workflow cannot determine a source-based
continuation.
     Algorithm 1 summarizes this recursive process. The return value r indicates whether an agent has
completed its task, found a missing dependency, detected a conflict, or encountered a failure. The value f
denotes the current formalization.
   The F ORMAT HEORIA workflow may invoke the following agents and procedures. Their roles are sum-
marized below, with detailed descriptions provided in Section 3.

Search and OCR Agents. The S EARCH AGENT locates and retrieves the literature identified by the source
item. Its output Sraw contains the relevant source material in its retrieved form, such as document pages
or page images. The OCRAGENT converts the retrieved material into the transcription Stex used by the
subsequent agents. The original material Sraw is retained alongside the transcription so that the subsequent
agents can consult the source evidence when the transcription is ambiguous.

Translator Agent. T RANSLATOR AGENT converts each source item into a candidate Lean formalization,
preserving the complete mathematical meaning. For a definition, it constructs the declaration type and
body; for a theorem, it translates the full statement and leaves the proof to the P ROVER. The agent may use
approved formalizations and existing library declarations, and it reports any additional source item required
for the translation as a missing dependency to F ORMAT HEORIA. Each candidate must pass both mechanical
Lean checks and an independent semantic review that compares the declaration with the original source
materials. If the available materials are ambiguous or insufficient to support a faithful translation, the agent
reports a failure for human investigation.

                                                      13
Algorithm 1 F ORMAT HEORIA
Require: source item s
Ensure: formalization fs of s
 1: Sraw ← S EARCH AGENT(s)
 2: Stex ← OCRAGENT(Sraw )
 3: (r, f ) ← T RANSLATOR AGENT(s, Sraw , Stex )
 4: f.state ← candidate
 5: if r = MissingDependency(s′ ) then
 6:      F ORMAT HEORIA(s′ )                              ▷ Workflow halts and human intervenes if formalization of s′ fails
 7:      return F ORMAT HEORIA(s)                                                                           ▷ restart translation
 8: else if r = Failure(e) then
 9:      return R EPORT T O H UMAN(e)
10: if s is a definition then
11:      f.state ← approved
12:      return f
13: while true do                                                               ▷ additional procedure when s is a theorem
14:      (r, f ) ← P ROVER(s, Sraw , Stex , f )
15:      if r = MissingDependency(s′ ) then
16:           F ORMAT HEORIA(s′ )                         ▷ Workflow halts and human intervenes if formalization of s′ fails
17:           continue                                                      ▷ restart proof after completing the dependency
18:      else if r = Conflict(s′ ) then
                          ′            ′
19:           Retrieve Sraw   , and Stex  for s′ via S EARCH AGENT and OCRAGENT
20:           Let fs′ denote the existing formalization for s′
21:           (rR ECONCILE , f, fs′ ) ← R ECONCILER AGENT(s, Sraw , Stex , f, s′ , Sraw
                                                                                     ′      ′
                                                                                         , Stex , fs′ )
22:           if rR ECONCILE = Failure(e) then
23:               return R EPORT T O H UMAN(e)
24:           else                                                                                      ▷ rR ECONCILE = Success
25:               continue                                                             ▷ continue with the repaired candidate
26:      else if r = Failure(e) then
27:           return R EPORT T O H UMAN(e)
28:      else                                                                                                    ▷ r = Success
29:           f.state ← approved
30:           return f


Prover Procedure. The P ROVER constructs a proof of a candidate theorem formalization through an
iterative, graph-based procedure. It maintains a proof graph whose nodes represent the target theorem
and any helper lemmas introduced during proof construction. P ROVE AGENT first attempts to discharge
the active proof obligation directly. If the obligation is too difficult, R EFINE AGENT decomposes it into
simpler helper lemmas; if a proposed obligation is determined to be nonviable, the corresponding branch
is pruned and the procedure explores another decomposition. Each successful proof must pass mechanical
review, including project elaboration, statement immutability, and the absence of unauthorized axioms. The
procedure continues until the root theorem is proved or it reports a missing dependency, incompatibility, or
unresolved failure to F ORMAT HEORIA.

Reconciler Agent. R ECONCILER AGENT resolves incompatibilities between a source item under formal-
ization and a previously formalized dependency, corresponding to issues of types [M AL 1] and [M AL 2]
introduced in Section 2.2. It compares the relevant source materials and Lean formalizations to identify the
cause of the conflict and construct a local, source-based repair. Depending on the conflict, the agent may

                                                              14
revise the current candidate formalization, introduce a justified compatibility definition or lemma, replace
the proof term of an approved theorem while preserving its statement, or revise explicitly authorized the-
orem statements. Each proposed repair must satisfy the applicable approval rules, remain confined to the
authorized scope, and preserve the elaboration of all existing downstream formalizations. If no supported re-
pair can satisfy these requirements, the agent reports the unresolved conflict to F ORMAT HEORIA for human
investigation.


3     Agent Components and Review Procedures
This section details the principal components invoked by the F ORMAT HEORIA workflow and the review
procedures governing their execution. Section 3.1 introduces the shared agent framework, which supports
multi-turn tool use, persistent artifacts, context compaction, and review-gated termination. Section 3.2
presents the graph-based P ROVER, in which P ROVE AGENT and R EFINE AGENT iteratively construct and de-
compose proofs while enforcing elaboration and statement immutability. Section 3.3 describes how T RANS -
LATOR AGENT produces source-faithful Lean declarations and subjects them to both mechanical checks and
independent semantic review. Finally, Section 3.4 explains how R ECONCILER AGENT constructs local,
source-based repairs for incompatibilities between formalizations while preserving approved mathematical
content and existing downstream developments.

3.1   Shared Agent Framework
The agents introduced below instantiate a common framework to perform different tasks within the main
workflow. The framework supports tool-based interaction with persistent files, allows agents to operate
across multiple large language model turns, and permits termination only after an independent review pro-
cedure accepts the proposed output. It thereby separates task-specific agent behavior from the underlying
mechanisms for tool execution, context management, and output validation.

Input and output. The agent framework takes as input a task prompt p and a review agent R. The prompt
specifies the task, available artifacts, expected output, and permitted tools, while the review agent defines
the conditions under which the task is considered complete.
    During execution, the agent may modify designated persistent files through tool calls. At a termination
attempt, the framework parses the proposed output o from the files specified by the task contract and returns
it only after R accepts it. We therefore model the agent framework as a function with side effects:

                                     AGENT F RAMEWORK(p, R) −→ o.

The files modified during execution constitute its side effects and serve as persistent, structured artifacts for
subsequent use by other agents or external tools.

Framework Description. Algorithm 2 gives the conceptual execution procedure. Specifically, the agent
first constructs the initial context C0 from the task prompt. At turn k, it invokes a large language model,
which produces a response hk and a finite sequence of tool calls ak . If ak ̸= ∅, the framework executes
the permitted calls, obtains their results rk , appends the response, tool calls, and results to the context, and
invokes the model again.
     A stop point is a turn at which ak = ∅. At a stop point, the framework parses the proposed output
from the files specified by the task contract. Reaching a stop point does not by itself indicate successful

                                                       15
Algorithm 2 Shared Agent Framework
Require: task prompt p and review agent R
Ensure: reviewed output o and modified persistent files
 1: C0 ← [p]
 2: for k = 1, 2, . . . do
 3:     (hk , ak ) ← LargeLanguageModel(Ck−1 )
 4:     if ak = ∅ then
 5:         o ← PARSE O UTPUT(p)
 6:         (v, d) ← R(p, o)
 7:         if v = accept then
 8:              return o
 9:         else
10:              Ck ← Ck−1 :: [hk , d]                                          ▷ continue with review findings
11:     else
12:         Execute ak and obtain results rk
13:         Ck ← Ck−1 :: [hk , ak , rk ]


completion, because the model may stop prematurely or incorrectly claim that the task is complete. The
framework therefore invokes the review agent R. If R rejects the output, the framework adds its findings to
the context and resumes execution. The framework terminates and returns the output only when R accepts
it.

Review agent. The review agent returns either accept or reject. A rejection is accompanied by diagnostic
feedback d, which explains the failed checks and guides the next model turn. Each task-specific agent
supplies its own review agent, allowing the same runtime to enforce different completion requirements. The
review procedures used by P ROVE AGENT and R EFINE AGENT are described in Section 3.2.

Context compaction. Formalizing long proofs may require an agent to sustain a reasoning trajectory
across many model turns. We denote by Ck the model context supplied at iteration k, including the task
specification, output contract, and interaction history accumulated through that iteration, such as relevant
model responses and tool outputs. This model context is distinct from the Lean context Γs .
     To keep the execution within the model’s finite context window, the framework monitors the token length
of Ck . When this length exceeds a configured threshold Bctx , the framework replaces the earlier portion
of the interaction history with a compact representation, generated either through an explicit summarization
prompt or through the model provider’s native compaction mechanism. The compacted context preserves
the task specification, output contract, established results, unresolved work, and references to persistent
artifacts needed to continue the task. The agent then resumes execution under the same loop using the
compacted context. Algorithm 2 omits this compaction operation for clarity.

Tool calls.   The common tool allowlist contains the following operations:

read Read a designated file or range without modifying it.

edit Apply a localized modification to a designated existing file and return the resulting diff or an error.

write Create a designated file or replace its contents when the agent is authorized to do so.


                                                          16
bash Execute a shell command and return its standard output, standard error, and exit status. This operation
    supports repository search, Lean compilation, audits, and tests.

Each component may impose further restrictions on this common allowlist. In particular, access to bash
does not allow an agent to bypass its file permissions or acceptance conditions.

3.2    P ROVER
The proof of a substantial mathematical theorem may span many pages in the source and require tens of
thousands of lines of Lean code. Such a task typically exceeds what a current language-model agent can
complete reliably within a single uninterrupted trajectory. The P ROVER addresses this long-horizon dif-
ficulty by alternating between two agents. P ROVE AGENT attempts to prove one active theorem or helper
lemma, while R EFINE AGENT decomposes a proof obligation that is too difficult to solve directly. A per-
sistent directed acyclic graph records this decomposition and the progress made across successive agent
runs.2

Input and output.        The P ROVER has the interface

                                              (s, Sraw , Stex , f ) −→ (r, f ′ ),

where s is the source item, Sraw is the corresponding raw literature file, Stex is its reconstructed LATEX
source, and f is a candidate formalization containing the fixed statement to be proved. The output f ′ is the
resulting formalization, and the return status belongs to

                     r ∈ Success, Failure(e), MissingDependency(s′ ), Conflict(s′ ) .
                          


    The status Success indicates that the proof has been completed and has passed the review procedure.
A missing dependency or conflict is returned to F ORMAT HEORIA, which formalizes the dependency or
invokes R ECONCILER AGENT, respectively. A failure records an error e that requires human investigation,
as specified in Algorithm 1.

Procedure description. Algorithm 3 describes the P ROVER. Its state is represented by a directed acyclic
graph Gs , an active path p, and an active node a, as defined below. Each node a of Gs represents either the
target formalization f or a helper lemma introduced to support its proof, and has a (prover) state

                                   a.prover_state ∈ {proposed, proved, pruned}.

A proposed node remains to be proved, a proved node has passed the applicable review procedure, and a
pruned node records a proof obligation that P ROVE AGENT has judged not viable.
    The root of Gs is the target formalization f . An edge u → v indicates that v was introduced as a simpler
proof obligation intended to support the proof of u. The active path p is a selected path from the root to the
node currently being processed, and its final node is the active node a.
    P ROVE AGENT first attempts to prove a directly. If it succeeds, the algorithm marks a as proved and
returns to its preceding node on the active path. If the agent returns TooHard(e), R EFINE AGENT augments
Gs with one or more helper lemmas and extends the active path to a newly selected node. If the active node
   2
    A lemma-graph mechanism implemented in AIM after the release of its initial report provided one point of reference for this
design. For the broader natural-language proof workflow and pessimistic verification methodology, see [38, 31].


                                                              17
Algorithm 3 P ROVER
Require: source item s, source files Sraw and Stex , and candidate formalization f
Ensure: return status r and resulting formalization f ′
 1: Gs ← ({f }, ∅), f.prover_state ← proposed, p ← [f ]
 2: while f.prover_state ̸= proved do
 3:     a ← last element of p
 4:     r ← P ROVE AGENT(s, Sraw , Stex , f, a)
 5:     if r = Success then
 6:          a.prover_state ← proved
 7:          Remove a from the end of p
 8:     else if r = NotProvable(e) then
 9:          a.prover_state ← pruned
10:          Remove a from the end of p
11:          if a = f then
12:              return (Failure(e), f )
13:     else if r = MissingDependency(s′ ) then
14:          return (MissingDependency(s′ ), f )
15:     else if r = Conflict(s′ ) then
16:          return (Conflict(s′ ), f )
17:     else
18:          e ← FAILURE M ESSAGE(r)                                                      ▷ r = TooHard(e)
19:          (Gs , p) ← R EFINE AGENT(s, Sraw , Stex , f, Gs , p, a, e)
20:          if |Gs | > Bgraph then
21:              return (Failure(graph size limit exceeded), f )
     ′
22: f ← R EAD F ORMALIZATION(f )
23: return (Success, f ′ )



is pruned, the algorithm also returns to the preceding node and may pursue a different decomposition. This
process continues until the root is proved or the P ROVER returns a condition to F ORMAT HEORIA.
    The graph serves both as a proof plan and as a record of earlier attempts. In particular, pruned nodes
help prevent P ROVE AGENT from repeatedly following the same unsuccessful decomposition. Whenever the
model context is compacted, the current graph, active path, and active node are retained in the compacted
context. Section 5.1.3 quantifies the execution horizons that this mechanism must support.

P ROVE AGENT.      P ROVE AGENT runs under the common agent framework described in Section 3.1. It takes

                                               (s, Sraw , Stex , f, a)

as input, where a is the currently active formalization, and may modify the authorized Lean source files. It
returns one of

               Success, TooHard(e), NotProvable(e), MissingDependency(s′ ), Conflict(s′ ) .
             


Its task prompt instructs it to replace the proof placeholder in a with a Lean proof supported by the sup-
plied sources, without changing any existing theorem statement or definition. The review agent used by
P ROVE AGENT, together with the implementation of its review checks, is specified later in this subsection.
     The status TooHard(e) indicates that the active obligation should be decomposed into simpler helper
lemmas. By contrast, NotProvable(e) indicates that P ROVE AGENT does not regard the current node as a

                                                         18
viable proof obligation, for example, because it appears mathematically false or because the agent cannot
identify a valid proof.
    P ROVE AGENT returns MissingDependency(s′ ) when proving the active node requires a source item s′
whose formalization is not yet available. It returns Conflict(s′ ) when it detects either of the following cases:

   1. The formalization of s′ is available but cannot be used consistently in the formalization of s. This
      case corresponds to an issue of type [I N T2] introduced in Section 2.2.

   2. Sufficient evidence suggests that s, as translated, may be unprovable, and the agent identifies a down-
      stream source item s′ that invokes s. The agent proposes this conflict so that the statement of s can be
      compared with the context in which s′ invokes it. This case corresponds to an issue of type [I N T1].

When Conflict(s′ ) is returned, F ORMAT HEORIA invokes R ECONCILER AGENT to investigate the potential
incompatibility and construct an appropriate repair.

R EFINE AGENT. R EFINE AGENT is invoked when P ROVE AGENT returns TooHard(e). It receives the
source materials, the target formalization, the current graph Gs , the active path p, the active node a, and the
explanation e:
                                         (s, Sraw , Stex , f, Gs , p, a, e).
Its output is an updated graph and active path:

                                                   (G′s , p′ ).

   R EFINE AGENT analyzes why the current obligation is too difficult, proposes simpler helper lemmas,
and adds the corresponding nodes and edges to Gs . It then extends the active path and selects its final
node as the next active node. R EFINE AGENT also runs under the common agent framework described in
Section 3.1, but it uses the distinct review procedure specified below.

Review procedures. At every stop point, the common agent framework described in Section 3.1 invokes
the review agent associated with the current task. The review agent for P ROVE AGENT performs the follow-
ing mechanical checks:

   1. the Lean project elaborates successfully;

   2. no existing theorem statement or definition has been modified, as detailed under “Immutable state-
      ments” later in this subsection; and

   3. if the return status is Success, the resulting formalization does not depend on any additional axioms
      beyond Lean’s fundamental axioms.

If any check fails, the review agent returns reject, together with a description of the failure. The common
agent framework adds this feedback to the context and resumes P ROVE AGENT.
    The review agent for R EFINE AGENT follows the same procedure except that it omits the first check:
the Lean project is not required to elaborate at a R EFINE AGENT stop point. It retains the second and third
checks above. This distinction allows R EFINE AGENT to construct an intermediate proof decomposition
before all newly proposed obligations have been completed.



                                                       19
Immutable statements. The second review condition requires a stronger safeguard than an instruction
in the agent prompt. A language-model agent may inadvertently modify an existing statement, and Lean’s
metaprogramming facilities make source-level audits alone insufficient for reliably detecting such changes.
The review procedure therefore uses kernel-level declaration information to enforce statement immutability.
    Before P ROVE AGENT or R EFINE AGENT begins, the agent snapshots the current Lean repository and
records a statement hash for every existing top-level Lean declaration. At each stop point, it computes the
hashes again and compares them with the snapshot. If any hash differs, the review agent rejects the output
and reports the modified declarations. The agent loop then resumes with an explicit instruction to restore
the affected statements and definitions. This check restricts the agents to constructing proofs and permitted
helper declarations without altering existing mathematical statements.

3.3   T RANSLATOR AGENT
Translating a mathematical definition or theorem statement into Lean requires preserving its mathematical
meaning while expressing it through Lean’s type system and the APIs available in the project. An incorrect
translation may make the intended theorem unprovable or cause downstream formalizations to rely on a
statement that differs from the source. The principal challenge is therefore semantic fidelity rather than
syntactic correctness alone. The T RANSLATOR AGENT addresses this challenge by combining Lean-based
mechanical checks with an independent, LLM-based semantic review.

Input and output.     The T RANSLATOR AGENT has the interface

                                          (s, Sraw , Stex ) −→ (r, f ),

where s is the source item, Sraw is the corresponding raw literature file, and Stex is its reconstructed LATEX
source. The output f is the candidate formalization of s, and the return status belongs to

                           r ∈ Success, Failure(e), MissingDependency(s′ ) .
                               


The status Success indicates that f has passed the applicable Lean checks and has been accepted by the
semantic review as representing the same mathematical content as s. The status MissingDependency(s′ )
indicates that the formalization of another source item s′ is required to express s. The F ORMAT HEORIA first
formalizes s′ and then restarts the translation of s. The status Failure(e) records an unresolved error e and
causes the task to be reported for human investigation, as in Section 3.2.

Procedure description. The T RANSLATOR AGENT instantiates the common agent framework described
in Section 3.1. Its task prompt instructs it to inspect both Sraw and Stex , identify the mathematical content
associated with s, and construct the corresponding Lean declaration.
    If s is a definition, the type and body of f must faithfully represent the definition in the source. If s is
a theorem, the type of f must faithfully represent the complete theorem statement, including its parameters,
assumptions, quantifiers, and conclusion, while its proof term is left as sorry for subsequent construction
by the P ROVER. During translation, the agent may invoke Lean to diagnose and repair elaboration errors.
It may use existing library declarations and approved formalizations, but it may not modify them. If an
additional source item is required to state the current item, the agent returns MissingDependency(s′ ). If the
source material is insufficient or ambiguous and the agent cannot establish a supported translation, it returns
Failure(e) rather than selecting an unsupported interpretation.


                                                       20
Review procedure. The review procedure for T RANSLATOR AGENT is particularly important because an
incorrect translation can propagate errors to downstream formalizations.
    At each stop point, the common agent framework invokes the review procedure associated with T RANS -
LATOR AGENT. The procedure first performs the following mechanical checks:

   1. the Lean project elaborates successfully; and

   2. no existing theorem statement or definition has been modified.

The second condition is enforced by the statement-immutability mechanism described in Section 3.2.
    These checks establish that Lean accepts the proposed declaration and that previously formalized math-
ematical content remains unchanged. However, they do not establish that f has the same mathematical
meaning as s. The review procedure therefore also invokes an independent R EVIEWAGENT to assess the
semantic fidelity of the translation.
    The R EVIEWAGENT receives s, Sraw , Stex , and the proposed formalization f . Its prompt instructs it to
compare the source with the Lean declaration and identify any semantic discrepancies. The prompt includes
a checklist of recurrent translation errors, including:

   1. moving part of a theorem’s conclusion into its assumptions;

   2. omitting conditions stated or implicitly required by the source;

   3. confusing existential and universal quantification;

   4. using a Mathlib declaration whose semantics differ subtly from the intended mathematical concept;
      and

   5. replacing a specific typeclass assumption required by the source with a different or unjustifiably gen-
      eral assumption.

    The checklist is initially authored by humans based in part on recurrent semantic errors identified during
the early stages of the project. After a batch of T RANSLATOR AGENT trajectories and the corresponding
human interventions has been collected, a S ELF I MPROVE AGENT updates the checklist to incorporate addi-
tional recurrent failure patterns. The prompt templates used by these agents are provided in the appendix.
    At each stop point, the R EVIEWAGENT is invoked with a fresh context. It receives neither findings
from previous reviews nor the internal reasoning trajectory of T RANSLATOR AGENT. This separation helps
ensure that the semantic review remains independent of the process that produced the candidate formaliza-
tion. If either a mechanical check or the semantic review fails, the review procedure returns reject with
concrete findings. The common agent framework adds these findings to the context and resumes T RANS -
LATOR AGENT. The translation terminates successfully only after all applicable checks accept the proposed
formalization.

3.4   R ECONCILER AGENT
R ECONCILER AGENT addresses incompatibilities between a source item under formalization and previously
formalized material, corresponding to issues of types [M AL 1] and [M AL 2] in Section 2.2. When such an
incompatibility is detected, the agent compares the relevant source materials and Lean formalizations and
attempts to construct a source-based repair.



                                                      21
Input and output.     R ECONCILER AGENT has the interface
                             (s, Sraw , Stex , f, s′ , Sraw
                                                        ′      ′
                                                            , Stex , f ′ ) −→ (r, fe, fe′ ),
where s is the source item currently being formalized and s′ is a source item on which s depends. The objects
Sraw and Stex are, respectively, the raw literature file containing s and its reconstructed LATEX source; the
primed objects provide the corresponding materials for s′ . Finally, f and f ′ are the current formalizations
of s and s′ .
    The agent is invoked under the following two cases, corresponding to Conflict cases returned by
P ROVE AGENT, as described in Section 3.2:
   1. f cannot use f ′ as required by the dependency of s on s′ ; for example, some arguments required by
      f ′ may not be constructible in the context of f , or the type or term obtained from f ′ may differ from
      what f expects.
   2. P ROVER determines that theorem s is unprovable as translated and identifies a potential conflict in-
      volving a previously formalized source item s′ that invokes s.
    The outputs fe and fe′ are the formalizations resulting from the attempted reconciliation, and
                                           r ∈ {Success, Failure(e)} .
The status Success indicates that the incompatibility has been resolved and that the resulting Lean project
has passed the applicable review procedure. The status Failure(e) records an unresolved conflict together
with an explanation e. F ORMAT HEORIA reports such a failure for human investigation.

Reconciliation procedure and authorized revisions. R ECONCILER AGENT instantiates the common agent
framework described in Section 3.1. Its task prompt instructs it to inspect both source items, their surround-
ing source materials, and their Lean formalizations before determining the cause of the incompatibility.
Depending on the conflict, the agent may revise the current candidate formalization, introduce a justified
compatibility definition or lemma, or replace the proof term of an approved theorem while preserving its
statement. All modifications must comply with the approval rules, under which the R ECONCILER AGENT is
additionally authorized to revise the statements (or definition bodies) of both f and f ′ .
    No uniform repair rule suffices for all conflicts. The agent is therefore instructed to seek a best-effort,
source-based resolution subject to two principles:
   1. the repair should be local and minimal, avoiding unnecessary changes to the surrounding formaliza-
      tion; and
   2. all existing downstream uses of the affected formalizations must continue to elaborate.
If the available sources do not support a repair satisfying these requirements, the agent returns Failure(e)
rather than altering protected mathematical content merely to make the project elaborate.

Review procedure. At each stop point, the common agent framework invokes the review procedure asso-
ciated with R ECONCILER AGENT. The procedure performs the following mechanical checks:
   1. the Lean project elaborates successfully, and all existing downstream formalizations continue to elab-
      orate without modification to definitions or theorem statements; and
   2. all changes are confined to the declarations and auxiliary constructions authorized by the reconcilia-
      tion task, and every approved formalization continues to satisfy the applicable immutability rules.

                                                          22
4     Implementation Considerations
This section describes implementation choices that improve the efficiency of the F ORMAT HEORIA workflow
without changing its formalization model or approval rules.

4.1   Section-Level Context Sharing
Context sharing allows information accumulated during one agent execution to be carried forward to sub-
sequent executions on related tasks. This mechanism is particularly useful in source-based formalization
because related source items often rely on the same mathematical background, literature dependencies, and
Mathlib declarations. Reusing this information reduces the token and time cost of reconstructing the relevant
context for each source item independently.
    To avoid confusion with the Lean context Γs , we use model context to refer to the information supplied
to an agent during its execution. Instances of T RANSLATOR AGENT and P ROVER AGENT that process related
source items reuse a common, evolving model context. We define relatedness at the section level: source
items are treated as related when they occur in the same section of a book or paper. This boundary reflects
the organization of mathematical literature, where items within a section typically share notation, standing
assumptions, definitions, intermediate results, and relevant external dependencies. At the same time, it limits
the inclusion of information from unrelated parts of the source corpus.
    Accordingly, when Algorithm 2 is invoked for a source item, its initial context C0 is initialized from the
most recent model context available for that section at the time of invocation. The resulting section-level
model context retains information accumulated while processing earlier source items, including relevant
source passages, previously identified literature dependencies, and useful Mathlib declarations. Discov-
eries made during one agent execution can therefore be reused by subsequent T RANSLATOR AGENT and
P ROVE AGENT instances working within the same section. Section-level context sharing thus amortizes the
token cost of reconstructing mathematical background and discovering literature and Mathlib dependencies
across multiple translation and proof-construction tasks.

4.2   Dependency-Aware Batch Parallelization
Independent source items can be formalized concurrently, thereby reducing the wall-clock time required to
process a large source corpus. Parallel execution must, however, respect dependencies discovered during
formalization and coordinate modifications to the shared persistent library. We therefore combine batch-
level parallelism with dependency-aware synchronization and globally serialized reconciliation.
     In our implementation, source items are organized into batches, each typically corresponding to a section
of a book or paper. Subject to the dependencies known at the time of scheduling, F ORMAT HEORIA is
invoked in parallel for all source items in a batch. Because the complete dependency structure is generally
unavailable in advance, an invocation may discover during statement construction or proof construction that
its source item depends on another item currently being processed by a concurrent invocation.
     To coordinate such cases, the system records the active F ORMAT HEORIA invocation, if any, associated
with each source item. When an invocation discovers a dependency, it first checks this record. If the depen-
dency is already being processed, the invocation does not launch a duplicate task. Instead, it waits for the
existing invocation to complete and then resumes using the resulting formalization. If the dependency is not
being processed and has not yet been formalized, the system invokes F ORMAT HEORIA for that dependency
through the ordinary recursive workflow. This mechanism allows independent tasks to proceed concurrently
while ensuring that each newly discovered dependency is formalized only once.


                                                      23
    Parallel execution also creates potential write conflicts in the shared persistent library. In particular,
R ECONCILER AGENT may modify existing Lean declarations, including definitions, theorem statements,
and proofs, subject to the approval rules described in Section 2.1. We therefore treat reconciliation as a
globally exclusive operation. At most one R ECONCILER AGENT may be active at any time. Before it begins,
all other formalization processes are paused and remain suspended until the reconciliation has completed
and its changes have been committed to the persistent library. The suspended processes then resume against
the updated library state. This serialization prevents other processes from reading or modifying declarations
while they are being reconciled.


5       Empirical Findings from Large-Scale Formalization
This section analyzes a completion-time snapshot of the formalization. The snapshot contains more than
994,000 lines of Lean in more than 850 files. More than 10% of these lines lie outside the combined depen-
dency closures of the Odd Order theorem and the Bender–Suzuki theorem. Repository size should therefore
not be identified with the size of either proof: the repository also contains declarations supporting other
results and intermediate developments that are not used by either root theorem. Unless stated otherwise,
all counts below refer to this snapshot and do not include later edits. We use these measurements to iden-
tify structural phenomena, but avoid treating lines of code, tokens, or elapsed time as direct measures of
mathematical difficulty.

5.1     Distributed Sources and Deep Dependencies
This subsection provides empirical evidence for Challenge C1 (Section 1.1). We examine the challenge at
three levels: the expansion of the external source corpus, the weak relationship between source length and
formalization burden, and the depth and connectivity of the resulting formal dependency graph.

5.1.1    Distributed Source Discovery
The formalization draws on 15 books and papers, covering 1,037 consulted pages (Table 2). The three
sources supplied by a human collaborator—the books of Bender–Glauberman and Peterfalvi [7, 42], together
with the fourth volume of Gorenstein–Lyons–Solomon [19]—account for 357 pages (34.4%). Following de-
pendencies led the workflow to twelve additional sources covering 680 pages (65.6%). Thus, dependency
discovery expanded the corpus fivefold, from three entry points to fifteen sources, and added about 1.9 times
as much consulted material by page count as was initially supplied.3 The significance for Challenge C1 is
not merely that the corpus became larger. Almost two-thirds of the consulted pages lay outside the ini-
tially supplied sources, so the boundary of the formalization task was not known in advance. The workflow
had to discover the source corpus while simultaneously constructing the formal dependency graph: when
a proof reached a dependency across a source boundary, progress could require locating the relevant pas-
sage, identifying and reconstructing its own prerequisites, and inserting the resulting declarations before the
downstream item could resume. A single omitted or misidentified dependency could therefore block a long
chain even when the local argument at its endpoint was otherwise valid. The human-supplied books served
as entry points rather than a closed specification; empirically, the challenge was the open-ended coupling of
source discovery and proof construction.
    3
   Page density varies across books and papers, so these totals are a coarse measure of source coverage rather than a normalized
measure of mathematical content.



                                                              24
 No. Authors                           Source                                                  Pages Consulted

  1     Helmut Bender and George       Local Analysis for the Odd Order Theorem [7]            1–152
        Glauberman
  2     Thomas Peterfalvi              Character Theory for the Odd Order Theorem [42]         1–150
  3     Daniel Gorenstein, Richard     The Classification of the Finite Simple Groups, Number 4 19–64, 245–253
        Lyons, and Ronald Solomon      [19]
  4     Marshall Hall, Jr.             The Theory of Groups [25]                               200–217
  5     I. Martin Isaacs               Character Theory of Finite Groups [35]                  1–11, 78–121, 262–285
  6     Daniel Gorenstein              Finite Groups [15]                                      102–112, 217–238,
                                                                                               270–280
  7     Graham Higman                  Suzuki 2-Groups [29]                                    79–96
  8     Bertram Huppert                Endliche Gruppen I [33]                                 135–142, 153–273,
                                                                                               448–465, 526–539
  9     Bertram Huppert and Norman     Finite Groups III [34]                                  28–35, 172–195,
        Blackburn                                                                              219–227, 246–291
 10     Michio Suzuki                  Group Theory II [46]                                    120–166, 266–286
 11     Daniel Gorenstein, Richard     The Classification of the Finite Simple Groups, Number 2 53–61, 72–78, 96–106,
        Lyons, and Ronald Solomon      [18]                                                     140–147
 12     Christoph Hering               On Finite Groups Operating Doubly Transitively on Their 456–458
                                       Involutions [28]
 13     Walter Feit                    The Representation Theory of Finite Groups [11]         140–247, 450–475
 14     Thomas Peterfalvi              Le théorème de Bender–Suzuki I [41]                     193–197
 15     Helmut Bender                  Transitive Gruppen gerader Ordnung, in denen jede       527–554
                                       Involution genau einen Punkt festläßt [6]

                             Table 2: Source literature consulted in the formalization.


    These corpus-level counts capture the breadth of Challenge C1 across sources, but source discovery also
exposes a second layer of dependency reconstruction within individual texts. Mathematical sources differ
substantially in their expository organization. Some (e.g. [7]) adopt a declaration-oriented style, in which
definitions, lemmas, and theorems are presented as locally self-contained units with explicit hypotheses and
conclusions. Others (e.g. [42]) use a running-context style, in which a section develops a mathematical
configuration through consecutively numbered items whose roles may vary: some state results, while others
introduce notation, record intermediate observations, or continue the surrounding discussion. Later results
can consequently inherit objects, assumptions, and intermediate facts from an extended preceding context.
Locating the relevant source passage is then only the first step: before that passage can be formalized, the
workflow must recover the evolving local context that gives it complete logical content and determine which
parts of that context belong in the formal dependency graph. Thus, a newly discovered source may enlarge
not only the document corpus but also a dependency context whose boundary becomes visible only as the
downstream formalization proceeds.

5.1.2    Source Length and Formalization Burden
Table 3 and Figure 2 show that page count has a conditional, rather than universal, relationship with for-
malization size. Across all 46 sections, source pages and local Lean lines of code (LOC) have Pearson


                                                            25
                       Bender–Glauberman (BG)                                    Peterfalvi (PF) Part I                          Peterfalvi (PF) Part II and appendices
                  Section      Local Pages Library                         Section Local Pages Library                          Section         Local Pages Library
                  Sec. 1      4,009                 8        19,528        Sec. 1    12,236             2        58,913         II.1.1        6,510           3 15,362
                  Sec. 2        174                 8        19,531        Sec. 2     7,639             5        28,363         II.1.2        5,654           1 97,918
                  Sec. 3     24,842                16        48,636        Sec. 3    19,287             5        56,918         II.1.3       13,885           4 66,484
                  Sec. 4     14,140                11        38,973        Sec. 4    11,882             6        56,833         II.2         29,261           7 106,715
                  Sec. 5      6,838                 5        38,473        Sec. 5    19,119             5        48,272         II.3.1       11,115           3 108,413
                  Sec. 6      6,605                 6        39,408        Sec. 6    25,513             8        59,113         II.3.2        2,573           1 54,696
                  Sec. 7      5,287                 6        42,270        Sec. 7     6,648             6        29,574         II.3.3        4,699           3 67,181
                  Sec. 8      7,176                 3        42,432        Sec. 8    19,291             6        75,104         II.4.1        2,743           1   2,291
                  Sec. 9      6,425                 5        42,657        Sec. 9    73,314             8        69,647         II.4.2        8,397           6 39,994
                  Sec. 10    16,858                11        51,573        Sec. 10   42,717             6        78,319         II.4.3        5,507           3 53,663
                  Sec. 11     5,005                 3        51,547        Sec. 11   24,995             5        78,431         II.4.4        3,122           3 58,562
                  Sec. 12    30,374                14        52,153        Sec. 12   19,884             6        78,663         Appendix I    2,572           2 97,270
                  Sec. 13    11,952                 8        51,954        Sec. 13   54,809            12        80,029         Appendix II   3,230           2 98,308
                  Sec. 14    20,985                12        52,595        Sec. 14   32,388             6        97,151         Appendix III 2,953            5 48,436
                  Sec. 15    23,516                 6        52,850                                                             Appendix IV 11,862            6 58,787
                  Sec. 16    11,074                12        52,931
                  Appendix C 8,068                  6        50,178

Table 3: Lean lines of code (LOC) and recorded source pages by section. “Local” denotes project LOC and
“Library” the relevant Mathlib dependency footprint.

                                                                                     BG (n = 17)                        PF (n = 29)
                        (a) Local LOC                                        (b) Relevant Mathlib LOC                                  (c) Local + relevant Mathlib LOC
                 160k
                                        Pearson r: BG 0.70 · PF 0.74                               Pearson r: BG 0.21 · PF 0.11                          Pearson r: BG 0.48 · PF 0.44

                 120k
 Lines of code




                  80k


                  40k


                   0
                           2    4   6   8     10        12     14     16        2    4     6       8        10     12      14    16       2    4    6    8     10     12     14    16
                                                                                      Textbook length (pages)

Figure 2: Lean lines of code (LOC) against the number of source pages for all 46 rows in Table 3. The three
panels separate local project code, the relevant Mathlib dependency footprint, and their sum.


correlation r = 0.47. Within each principal source family the association is stronger (r = 0.70 for BG and
r = 0.74 for PF), yet the two families occupy visibly different vertical ranges in the left panel. Source iden-
tity therefore changes the baseline cost against which page length is informative. The eight-page rows make
this concrete: BG Section 1 has 4,009 local LOC, whereas PF Section 9 has 73,314, more than eighteen
times as many. Page count records how much space an author devotes to an argument, but not how much
context is implicit, how much infrastructure the formal representation requires, or how finely the workflow
decomposes the argument.
     The tabular aggregates quantify the separation visible in the scatter plot. The BG rows contain 203,328
local LOC for 140 source pages, approximately 1,452 LOC per page. The PF rows, including Part II and
the appendices, contain 483,805 local LOC for 136 pages, approximately 3,557 LOC per page. Thus PF has


                                                                                           26
about 2.45 times the observed formalization density of BG despite nearly equal page totals. This difference
is not introduced by Peterfalvi Part II: Part I alone contains 369,722 local LOC for 86 pages, approximately
4,299 LOC per page. The comparison therefore points to a source-family effect, not simply to one unusually
long auxiliary development.
    The other two panels show why even this local-code relationship should not be interpreted as a predictor
of total dependency footprint. Source pages have correlation r = −0.12 with relevant Mathlib LOC and
only r = 0.12 with local and relevant Mathlib LOC combined. Among the one-page PF sections, for exam-
ple, Part II Section 4.1 has 5,034 combined LOC, whereas Part II Section 1.2 has 103,572—a factor of more
than twenty. The relevant-Mathlib median is 48,636 LOC for BG and 59,113 for PF; the respective ranges
are 19,528–52,931 and 2,291–108,413. A larger footprint can indicate broader reuse, heavier prerequisites,
or both, and is not a direct count of missing lemmas. Taken together, the higher PF local density and much
wider library footprint are consistent with the working hypothesis that BG draws on a more concentrated
body of theory while PF crosses more varied interfaces. A direct audit of project-local foundational decla-
rations would still be required to conclude that Mathlib support is intrinsically better for BG; proof style,
agent decomposition, and source presentation remain potential confounders.
    Section-level code volume measures the size of the formalization, but not the dependency structure that
makes the task long-horizon. We therefore turn from source and code volume to the depth and connectivity
of the declaration graph.

5.1.3   Depth and Connectivity of the Declaration Dependency Graph
Graph definition and scope. The formalized development induces a dependency graph over its Lean
declarations. Here a declaration is a theorem or a definition. Let G = (V, E) denote this graph, where each
node in V is a declaration and an edge u → v records that the declaration u uses v. Thus, edges point from a
declaration to one of its prerequisites. Lean’s declaration discipline makes this dependency relation acyclic.
    We analyze the induced subgraph whose nodes satisfy both of the following conditions: they are reach-
able from the declaration of the Bender–Suzuki theorem, and they belong to the formalization project rather
than Mathlib. This subgraph contains 30,298 nodes and 186,187 edges.

Dependency depth and structural profile. To quantify dependency depth, for each node u ∈ V we
compute the length of a longest directed path beginning at u:
                         d(u) = max{k : there exists u = u0 → u1 → · · · → uk }.
The resulting distribution is shown in Figure 3. In the Bender–Suzuki project-only closure, the root theorem
has depth 458. A corresponding root-specific computation for the Feit–Thompson theorem gives depth 430.
These root depths place the final results at the end of exceptionally long chains of project declarations. For
Challenge C1, they quantify the long dependency horizon that must be maintained while composing the
formalization.
    The distribution is strongly skewed. Of the 30,298 project declarations, 8,916 (29.4%) have depth zero,
and the median depth is only two. Yet the 90th, 95th, and 99th percentiles are 38, 169, and 378, respectively.
In particular, the depth increases by 209 between the 95th and 99th percentiles, even though half of the
declarations have depth at most two. This contrast is a notable feature of the graph: the development is
not uniformly deep, but has a broad shallow base together with a small, exceptionally deep backbone. The
shape is more informative than the maximum alone. It localizes the long-horizon aspect of Challenge C1
to a relatively small upper tail of declarations that carries the long-range composition needed by the root
theorem.

                                                     27
                                                Length 0: 8,916 nodes (29.4%)
         Number of nodes (log scale)   104


                                       103
                                                                                                                                Maximum observed length: 458
                                            2
                                       10


                                       101


                                       100

                      100%
                       90%
Cumulative share




                       75%
                                50%
                                25%
                                                                                                                     Median 2   90th 38   95th 169   99th 378
                                       0% 0          50           100           150     200             250         300         350          400          450
                                                                                      Longest path length (edges)

Figure 3: Distribution of the maximum path length starting from each project declaration in the Bender–
Suzuki dependency closure.


     The histogram also contains narrow high-depth regions. In the interval [342, 360], for example, exactly
one declaration occurs at each depth. The run records associate these declarations with the development
around equations (13.6)–(13.12) of [42]. The one-per-level pattern is consistent with a narrow logical bridge:
at these depths the graph has little visible width, so progress toward the root may depend on a nearly serial
piece of formal development.4

Reuse hubs and integration points. For a declaration v, its in-degree is the number of declarations that
reference v, while its out-degree is the number of declarations referenced by v. The five declarations with
the largest values of each quantity are listed in Tables 4 and 5.
    The in-degree ranking measures how widely a declaration is reused by the development. All five leading
entries are definitions. Four expose recurring character-theoretic or group-theoretic interfaces: Section1
.ClassFunction, Section1.IsIrreducibleCharacterOnGroup, ambientDerivedSu
bgroup, and subgroupCentralizerIn. The remaining entry, section9MaximalSubgroups,
packages the maximal-subgroup structure used in the Feit–Thompson proof. Their concentration at the top
of the ranking shows that a small set of definitions provides interfaces on which a large fraction of the
development depends. The concentration is especially pronounced at the first rank: Section1.Class
Function is referenced by 6,016 declarations, more than three times the in-degree of the second-ranked
entry.
                       4
    The depth histogram alone, however, does not prove that the declarations form one adjacent path; that stronger statement
requires direct inspection of the intervening edges.



                                                                                             28
  Rank    Declaration                                                      Category                 In-degree
    1     Section1.ClassFunction                                           Definition                   6,016
    2     Section1.IsIrreducibleCharacterOnGroup                           Definition                   1,834
    3     section9MaximalSubgroups                                         Definition                   1,792
    4     ambientDerivedSubgroup                                           Definition                   1,787
    5     subgroupCentralizerIn                                            Definition                   1,549

                                Table 4: Top-five declarations by in-degree.

  Rank    Declaration                                                      Category               Out-degree
    1     BenderSuzuki.External.Higman.lemma12_disti                       Theorem                        536
          nct_pair_gap_classify_basic
    2     FeitThompson.PFsection9.theorem_9_11_case_                       Theorem                        351
          a_step_9_11_8_sourceData_of_noPairStep_sec9
    3     BenderSuzuki.PFchapter3section1.theorem_c_                       Theorem                        239
          of_Q1_ne_bot
    4     Section12.theorem_12_17_lowerBoundData_sou                       Theorem                        223
          rce_leaf
    5     BenderSuzuki.External.Higman.lemma12_chain                       Theorem                        147
          _typeBCD_with_isomorphic_criterion

                                Table 5: Top-five declarations by out-degree.


    The out-degree ranking measures the breadth of the prerequisite context needed to establish a declara-
tion. All five leading entries are theorems, and their large out-degrees identify proof or source-data packages
that assemble many earlier results. These declarations are therefore integration points in the formal depen-
dency structure, rather than the widely reused foundational interfaces identified by the in-degree ranking.
The clean separation between the two top-five lists is not built into the degree definitions: high in-degree
selects definitions that broadcast a shared vocabulary across the project, whereas high out-degree selects
theorems that gather many prerequisites at difficult proof boundaries. Although the top five do not deter-
mine the full degree distribution, they expose two complementary forms of concentration that a long-horizon
workflow must manage: stable reusable interfaces and localized integration points.

Project structure versus library substrate. The project-only Bender–Suzuki closure contains 30,298
nodes and 186,187 edges. If Mathlib declarations are retained, the same root-specific closure contains
74,922 nodes and 1,444,499 edges. Including the library therefore multiplies the node count by about 2.5
and the edge count by about 7.8. Equivalently, the number of edges per node rises from about 6.1 in
the project-only graph to about 19.3 in the library-inclusive graph. The disproportionate increase in edges is
important: Mathlib contributes not merely additional prerequisite nodes, but a much more densely connected
substrate. Much of the graph’s raw connectivity therefore belongs to the library, whereas the project-only
view isolates the structure introduced by this formalization. Reporting both views prevents a deep library
dependency closure from being mistaken for an equally large body of newly formalized mathematics, while
still recording the library structure on which the project relies.

Operational manifestation of the long dependency horizon. The declaration graph measures the static
depth of the formalized theory, while the execution traces expose the corresponding operational horizon of

                                                      29
the workflow. Across all recorded trajectories, the workflow consumed 64B tokens in total. The longest ob-
served trajectory spanned 9.17 days, consumed 3.5 billion tokens, and underwent 606 context compactions.
These measurements show that the largest formalization tasks extend far beyond a single model context or an
uninterrupted proof attempt. Progress must instead survive repeated compression of the interaction history
while preserving the current proof state, the relevant section-level context, and decisions accumulated over
earlier stages. This provides an operational counterpart to the depth of the declaration DAG and motivates
the graph-based state tracking mechanism for P ROVER described in Section 3.2.
Taken together, these measurements expose two complementary dimensions of Challenge C1. Source dis-
covery makes the boundary of the task open-ended, while the declaration dependency graph makes its inter-
nal horizon exceptionally deep but highly concentrated. The difficulty lies not simply in formalizing many
source pages, but in discovering and composing the small set of long dependency chains that connect a broad
base of local declarations to the root theorems. The degree rankings further suggest where this composition
is organized: reusable definitions stabilize shared interfaces, while a small number of theorems integrate
unusually broad prerequisite contexts.

5.2   Source Defects and Misalignments Identified during the Formalization Process
In this section, we present representative mathematical issues identified in the literature during our project
and classify each issue according to the source defects and misalignments defined in Section 2.2. Most
of these issues were resolved automatically by the workflow, either through the P ROVER procedure or by
R ECONCILER AGENT. Because such automatically resolved issues are recorded only in execution logs and
are not reported separately by the workflow, our retrospective review may not have recovered every instance.
A smaller number of issues could not be resolved automatically and were escalated for human investigation;
we report all such cases encountered in the project.
    The first two examples arose while formalizing the proof of the Odd Order Theorem based on [7, 42].
The existing Rocq formalization [14] may also have encountered these issues. Our workflow nevertheless
identified them independently. Moreover, for one of these issues, namely the incompatibility between the
definitions of type I maximal subgroup, we adopted a different resolution, as described below.

Incompatibility between definitions of type I maximal subgroups [M AL 1]. The proof of the Odd Order
Theorem proceeds by choosing a minimal counterexample G and analyzing the structure of its maximal
subgroups. These maximal subgroups are divided into five classes, called types I–V. However, [7] and [42]
give different definitions of type I maximal subgroups. Condition (Iii) in [7, Section 16] requires that

      each complement E to H in M contains a normal abelian subgroup A such that CE (x) ⊂ A
      for all x ∈ H # ,

whereas [42, Definition 8.1] requires only that

      there is a complement U of H containing a normal abelian subgroup U1 such that CU (x) ⊂ U1
      for all x ∈ H # .

Thus, the definition in [7] is formally stronger than that in [42]: the former quantifies over all complements,
whereas the latter requires only the existence of one such complement. Nevertheless, the two conditions are
equivalent by the Schur–Zassenhaus theorem, since complements to H in M exist and are conjugate.
    This case was resolved automatically by the P ROVER procedure and was identified through a retrospec-
tive examination of the execution logs. In particular, the P ROVER procedure resolves this incompatibility

                                                      30
by establishing a lemma that bridges the two definitions. By contrast, the existing Rocq formalization of
the Odd Order Theorem [14] adopts the latter condition as its definition of type I maximal subgroups and
formalizes the results from [7] using the formulation in [42].

Typographical errors in the definitions of type I maximal subgroups [D EF 1].           Condition (Iv)(c) in the
definition of type I maximal subgroups in [7] states

      for every p ∈ π(H), p ∈ π ∗ and the exponent of M/H divides p − 1; for some such prime p,
      we have Op′ (M ) is cyclic.

While attempting to prove Proposition 16.1 of [7] under this definition, the autoformalization workflow
stalled. After repeated attempts, P ROVER returned Failure to F ORMAT HEORIA, triggering an escalation for
human investigation. Manual examination of the proof of Proposition 16.1 revealed that the final condition
should instead read:

      for every p ∈ π(H), p ∈ π ∗ and the exponent of M/H divides p − 1; for some such prime p,
      we have Op′ (H) is cyclic.

Thus, Op′ (M ) in the stated definition appears to be a typographical error for Op′ (H). The corresponding
definition in [42, Definition 8.3] contains the same error.

Missing condition in Peterfalvi [D EF 1]. The proof of Appendix IV, Lemma 2(c) in [42] requires the
additional condition that |Q1 | is odd, but this condition is omitted from the lemma statement. In Peterfalvi’s
application of the lemma, however, |Q1 | is already known to be odd from the earlier decomposition in
[42, Part II, Chapter 1]. The application can therefore be justified by supplying this hypothesis implicitly
in that context. The condition must nevertheless be added to the lemma statement for the lemma itself to
hold. This issue was resolved automatically by R ECONCILER AGENT and identified through a retrospective
examination of the execution logs.

Error in Theorem 8.27 in Huppert I [D EF 1].        The statement of Dickson’s theorem in [33, Satz II.8.27]
includes

      semidirect products of elementary abelian groups of order pm with cyclic groups of order t,
                 m
      where t | p d−1 and t | pf − 1.

The P ROVER procedure found counterexamples to this statement and escalated the issue for human investi-
gation. Manual examination determined that the correct statement is

      semidirect products of elementary abelian groups of order pm with cyclic groups of order t,
                                f
      where t | pm − 1 and t | p d−1 .

Thus, the factor d appears in the wrong divisibility condition in the stated theorem.

Error in Lemma 11 of Higman [D EF 2]. In the proof of Lemma 11 in [29, p. 88], the basis u0 , . . . , um
should instead be u0 , . . . , um−1 . This indexing error was corrected automatically by the P ROVER procedure
and identified through a retrospective examination of the execution logs.



                                                      31
Inconsistent definitions of Suzuki 2-groups [M AL 1].         In the definition of Suzuki 2-groups, Peterfalvi
[42] requires the action to be regular:

      A Suzuki 2-group is a 2-group P such that P is non-abelian, P has at least two involutions and
      there is a cyclic group K which acts faithfully on P and regularly on the set of involutions of
      P.

In contrast, Higman [29] only assumes that the action is transitive. The P ROVER automatically derives
transitivity from regularity and therefore can invoke the relevant results in [29]. Note that Higman later
proved the non-trivial result that transitivity in this setting actually implies regularity; however, this theorem
has not been formalized by the P ROVER. This issue was identified through a retrospective examination of
the execution logs.

5.3   Examples of Automatically Fixed Translation Mistakes
The initial translation of a source item may fail to preserve its intended mathematical content, particularly
when the source relies on implicit context or when hypotheses and conclusions are incorrectly organized
in the formal statement. Such errors may be exposed either by a failed proof attempt or by the failure of a
proved theorem to support a downstream argument. In these cases, the R ECONCILER AGENT compares the
translation with the relevant source context and downstream uses, identifies the discrepancy, and repairs the
formal statement. The following examples illustrate two translation mistakes detected and corrected through
this process.

Implicit source context omitted in translation [I N T1]. Part I of [42] is written in a style that leaves
many standing assumptions implicit. For example, (13.18) states:

      Let j be such that 0 < j < p and let βj = IndSP W1 1P W1 − µ0j . (a) supp(βj ) ⊂ P # ∪ (W −
      (W1 ∪ W2 ))S ⊂ A0 (S). (b) ∥βj ∥2 = u−1                     τ
                                                q + 2. (c) Γ = βj − 1G + η0j is independent of j,
      orthogonal to 1G and real. (d) Set Γ = X + Y where X is a linear combination of the functions
      ηik and Y is orthogonal to the functions ηik . Then ∥Y ∥2 ≤ u−1
                                                                    q .

Here, G is a chosen minimal counterexample to the Odd Order Theorem, and S ≤ G is a particular sub-
group selected in (13.1) on Page 75, nine pages before (13.18) on Page 84. Similarly, µ is a class function
introduced in (13.1), which in turn refers back to (4.3) for its construction and relevant properties. The initial
translation of (13.18) omitted the context associated with these particular choices of S and µ. Consequently,
the P ROVER could not establish the translated statement because the formal context lacked properties of S
and µ required by the proof. The R ECONCILER AGENT repaired the translation by comparing (13.18) with
(13.1) and making the required context explicit.

Translation weakened theorem statement [I N T2]. The initial translation of Peterfalvi’s (12.6) [42] was
incorrect: the conclusions of theorem_12_6_statement were mistakenly included in
theorem_12_6_source_data, which appears as an assumption of theorem_12_6_statement.
The resulting theorem therefore admitted a trivial proof but was unusable in downstream arguments, such as
Peterfalvi’s (12.16) and (14.2), because constructing theorem_12_6_source_data already required
establishing the intended conclusions. Accordingly, the P ROVER initially proved theorem_12_6 trivially
but later failed to apply it while proving Peterfalvi’s (12.16). This failure triggered the R ECONCILER AGENT,
which corrected the statement of theorem_12_6 by comparing it with its use in (12.16).

                                                       32
5.4   Reconciliation Hotspots and Repair Boundaries
Reconciliation addresses theory-integration failures arising from cross-source misalignment (Challenge C2),
incorrect Lean translation (Challenge C3), and source defects (Challenge C4). Such failures typically sur-
face as an unprovable translation or downstream application conflict of type [I N T1] or [I N T2], although
diagnosis may reveal an underlying [M AL 1], [M AL 2], [D EF 1], or [D EF 2] issue, as illustrated in Sec-
tion 5.2. Table 6 reports the exact modification counts and declaration populations, while Figure 4 normal-
izes these counts by source-group size and orders the groups by modification share. The normalized view
distinguishes absolute modification volume from the relative extent of the affected code surface. Because
one reconciliation may modify several declarations, whereas an unresolved case may be escalated without
modifying any, these measurements describe the affected code surface rather than agent invocations, distinct
incompatibilities, successful repairs, or error rates.

Where reconciliation concentrates. Table 6 reports the number of declarations modified during reconcil-
iation together with the total declaration population of each audited source group, while Figure 4 normalizes
these counts by source-group size. These quantities measure the formal code surface affected by reconcili-
ation. They do not directly measure the number of reconciliation invocations, distinct incompatibilities, or
source errors, because a single incompatibility may require coordinated changes to several declarations.
     The modifications are highly concentrated. Across the source groups represented in Table 6, 284 of
10,417 declarations were modified, giving an aggregate share of 2.7%. PF Part I accounts for 255 of these
284 modifications. Within PF Part I, Sections 9, 10, and 13 alone account for 219 modifications, or 77.1% of
all modifications in the table, although they contain only 3,633 of the 10,417 declarations. The concentration
remains visible after normalization. Sections 10 and 13 have modification shares of 8.97% and 8.50%,
respectively, and together contain 192 modified declarations among 2,208 declarations, for a combined
share of 8.7%. More broadly, Sections 9–14 have a modification share of 242/5,246 = 4.6%, compared
with 13/1,626 = 0.8% for Sections 6–8. Thus, the later PF Part I sections exhibit a modification share
approximately 5.8 times as large.
     Section size alone does not account for this pattern. For example, Section 9 contains 1,425 declarations,
more than either Section 10 or Section 13, but its modification share is only 1.89%. To explore whether the
concentration is instead associated with cross-section integration, we analyze the declaration-dependency
graph. Let Vs denote the declarations owned by Section s. Because an edge u → v indicates that u depends
on v, define                                                                 X
                       d+s (u) = |{v : u → v, owner(v) ̸= s}|,         Cs =      d+s (u).
                                                                           u∈Vs

Here, Cs counts the dependency edges from declarations in Section s to declarations owned by other sec-
tions. It therefore measures the extent to which the formalization of Section s relies on interfaces with
previously formalized material.
    Table 7 provides supporting evidence for an association between such cross-section dependencies and
reconciliation concentration. Sections 10 and 13 have the two largest cross-section dependency counts,
10,203 and 11,631, as well as the two highest modification shares. Across the fourteen PF Part I sections,
the modification share has Pearson correlation r = 0.861 and Spearman correlation ρ = 0.820 with Cs ,
both with p < 0.001. Its association with section size is weaker: the corresponding correlations are r =
0.607 (p = 0.021) and ρ = 0.483 (p = 0.080). These exploratory comparisons suggest that the observed
concentration is more closely associated with cross-section integration than with the number of declarations
alone.


                                                     33
                           Declarations Total                                                       Declarations Total
Source Group                                                              Source Group
                            Modified Declarations                                                    Modified Declarations
BG Section 5                            4              127                PF Part I Section 14                    21                722
BG Section 6                            1              114                PF Part II Chapter 1.1                   2                209
BG Section 13                           2              259                PF Part II Chapter 1.2                   1                 86
BG Section 16                           1              356                PF Part II Chapter 1.3                   1                130
PF Part I Section 6                     1              711                PF Part II Chapter 2                     1                434
PF Part I Section 7                     4              378                PF Part II Chapter 4.2                   2                 64
PF Part I Section 8                     8              537                PF Part II Appendix III                  1                 47
PF Part I Section 9                    27            1,425                PF Part II Appendix IV                   3                200
PF Part I Section 10                   82              914                Huppert Chapter II                       2                120
PF Part I Section 11                    1              467                Huppert Chapter IV                       1                268
PF Part I Section 12                    1              424                Huppert Chapter XI                       5                697
PF Part I Section 13                  110            1,294                Higman                                   2                434
                                                                          Total                                  284            10,417

Table 6: Declarations modified by R ECONCILER AGENT relative to the total declaration count in each source
group.
                                                      aggregate among listed groups = 2.7%

    PF Part I Section 10                                                                                             82/914
    PF Part I Section 13                                                                                         110/1,294
           BG Section 5                                     4/127
  PF Part II Chapter 4.2                                    2/64
    PF Part I Section 14                                  21/722
 PF Part II Appendix III                         1/47
     PF Part I Section 9                       27/1,425
     Huppert Chapter II                      2/120
 PF Part II Appendix IV                    3/200
     PF Part I Section 8                   8/537
  PF Part II Chapter 1.2                1/86
     PF Part I Section 7               4/378
  PF Part II Chapter 1.1              2/209
           BG Section 6              1/114
          BG Section 13            2/259
  PF Part II Chapter 1.3           1/130
    Huppert Chapter XI             5/697
                Higman          2/434
    Huppert Chapter IV         1/268
          BG Section 16       1/356
    PF Part I Section 12     1/424
    PF Part II Chapter 2     1/434
    PF Part I Section 11     1/467                                                                          BG                Huppert
     PF Part I Section 6    1/711                                                                           PF                Higman

                       0%                   2%                      4%              6%                 8%                     10%
                                                          Declarations modified / total declarations

Figure 4: Source groups ordered by the share of declarations modified by R ECONCILER AGENT. Bar lengths
show the number of modified declarations divided by the total declaration count in the corresponding source
group; labels report the underlying counts, and colors distinguish source families. The dashed line marks
the aggregate modification share across the source groups listed in Table 6.


                                                                     34
                                                            R ECONCILER AGENT
                           PF Section      |Vs |      Cs
                                                             modification share
                           1               737        106                     0%
                           2               329        163                     0%
                           3               682      1,715                     0%
                           4               432      1,767                     0%
                           5               619      2,967                     0%
                           6               711      4,070                  0.14%
                           7               378      1,038                  1.06%
                           8               537      4,026                  1.49%
                           9             1,425      6,308                  1.89%
                           10              914     10,203                  8.97%
                           11              467      5,365                  0.21%
                           12              424      3,942                  0.24%
                           13            1,294     11,631                  8.50%
                           14              722      8,442                  2.91%

                     Table 7: Cross-section dependency counts for PF Part I sections.


     Inspection of the corresponding Lean development further suggests a plausible structural explanation
for this association. In PF Part I Section 10, the file PFsection10/Basic.lean organizes source hy-
potheses and their carrier data through section10FullFourSixSourceNotation,
section10FourSixSupportedPackage, and section10SupportedFourSixData. The first
declaration records the source-notation layer, whereas the latter two package the supported assumptions
and carrier data. The file PFsection10/PFsection10_11.lean expands these packages into fam-
ilies of source-data and supported-data declarations, together with bridge lemmas that project fields from
bundled hypotheses or transport existing results into the supported representation. For example, the odd-
order, vanishing, and parity fields of Hypothesis (10.4) are extracted through separate theorem interfaces
whose proof terms directly select the corresponding fields. PF Part I Section 13 exhibits the same pat-
tern across a larger module boundary: its 21 source files combine material from Sections 3, 5, 6, 8, 9,
10, and 11. In PFsection13/PFsection13_2.lean, separate source, rank-choice, and branch-data
predicates are connected by conversion lemmas, while PFsection13/PFsection13_Common.lean
stages the numerical argument of Theorem (13.10) through raw-source, total-norm, cardinal-formula, and
strict-comparison data, with bridge lemmas between successive representations. These intermediate decla-
rations generally expose source contexts or transport existing results rather than express independent math-
ematical conclusions. Consequently, a mismatch at one representation boundary may require coordinated
revisions to several packages, projections, and transport lemmas. Thus, integration across formal inter-
faces may expand the reconciliation footprint of a single conceptual incompatibility, requiring coordinated
modifications to multiple packages, projections, conversion lemmas, and transport lemmas.

Why local reconciliation can succeed. Many conflicts are repairable because the two sides already con-
tain enough source evidence to justify a mathematical bridge. For a type [M AL 1] mismatch, the definitions
may be mathematically equivalent even though Lean does not identify them definitionally; an equivalence
lemma or conversion construction can make the identification explicit. For a conflict manifesting as [I N T2],


                                                      35
the current candidate can often be revised to use the approved dependency through an adapter, without
changing either source-level statement. The package and projection layers in PF Sections 10 and 13 make
these boundaries verbose, but they also localize the required transports and provide named intermediate
invariants against which a repair can be checked.
     The approval rule is central to this capability. R ECONCILER AGENT may modify the current candidate,
add justified compatibility declarations, replace the proof term of an approved theorem while preserving its
type, or revise explicitly authorized theorem statements. It may not silently weaken an un-authorized ap-
proved hypothesis, strengthen an un-authorized approved conclusion, or identify two objects merely because
doing so makes elaboration succeed. The reconciliation is accepted only if the sources support the bridge
and all existing downstream declarations continue to elaborate. In this sense, reconciliation is constrained
theory integration rather than unrestricted refactoring.
     Section 5.2 provides concrete examples of this boundary. The two formulations of type I maximal sub-
groups constitute a type [M AL 1] misalignment: a source-supported equivalence bridge is possible because
Schur–Zassenhaus supplies the missing mathematical identification. The omitted odd-order condition in Pe-
terfalvi is a type [D EF 1] defect that R ECONCILER AGENT could repair because the required hypothesis was
already established in the surrounding source context. Likewise, the regular formulation of Suzuki 2-groups
is sufficient for using a result stated under transitivity, because the needed implication has a supported direc-
tion. These cases are repairable not because reconciliation tolerates inconsistency, but because the available
sources establish a local path from the stronger or differently packaged context to the interface required
downstream.

Limits and escalation boundary. Reconciliation cannot manufacture mathematical evidence that is ab-
sent from the sources. A type [M AL 2] conflict may involve genuinely distinct objects sharing a name;
identifying them would be unsound, while separating them may require a nonlocal redesign of the formal
theory. A type [D EF 1] or [D EF 2] defect may require deciding what the author intended, supplying a missing
theorem, or making unauthorized correction to an approved theorem statement. Similarly, an [I N T1] error
in the type of an already approved declaration cannot be repaired merely by replacing its proof term. These
cases exceed the local authority of R ECONCILER AGENT and must be escalated or returned to an upstream
translation and approval step.
    The examples in Section 5.2 again show the distinction. The misplaced divisibility factor in Huppert’s
statement required human examination, whereas the indexing error in Higman’s proof could be corrected
during proof construction without changing the theorem statement. For Suzuki 2-groups, the workflow uses
the supported implication from regularity to transitivity, but it does not claim the unformalized converse.
The operative criterion is therefore not whether a conflict is small syntactically, but whether a local repair is
justified by available evidence, respects approved interfaces, and preserves every downstream use.
    Finally, the aggregate does not measure the success rate or cost of reconciliation. A high modification
share may reflect one broad interface repair rather than many independent failures, and a difficult unsuc-
cessful reconciliation may leave no modified declaration at all. This distinction is operationally important
because reconciliation is globally exclusive in the parallel workflow of Section 4.2; repeated calls at a hotspot
may pause otherwise independent workers, but declaration counts cannot quantify that delay. Establishing
operational effectiveness would require call-level traces recording the diagnosed issue type, attempted repair,
review outcome, human escalation, downstream declarations rechecked, and time spent at the reconciliation
barrier. The present data instead support a structural conclusion: reconciliation work is concentrated where
source boundaries are exposed as formal interfaces, and automatic repair is effective only when those inter-
faces can be connected by a local, source-supported construction.


                                                       36
                       Section     Review Rejects          Section      Review Rejects
                       PF Sec. 1         3                 PF Sec. 8          1
                       PF Sec. 2         0                 PF Sec. 9          1
                       PF Sec. 3         1                 PF Sec. 10         0
                       PF Sec. 4         2                 PF Sec. 11         2
                       PF Sec. 5         2                 PF Sec. 12         1
                       PF Sec. 6         1                 PF Sec. 13         1
                       PF Sec. 7         0                 PF Sec. 14         1
                                                                Total         16

                    Table 8: Rejected review outcomes for translation work in PF Part I.


5.5   Review as an Iterative Quality Gate
Each section-level translation was reviewed repeatedly until it was accepted. Consequently, a section with
r rejected outcomes required r + 1 review rounds. As shown in Table 8, the fourteen PF Part I sections
generated 16 rejected outcomes and therefore required 30 review rounds in total. Only three sections were
accepted on the first review; the other eleven, or 78.6%, were returned for revision at least once. Seven
sections were accepted in the second round, three in the third, and one in the fourth.
     These results provide direct operational evidence that the review agent affected the translation process.
For most sections, it did not simply confirm the first candidate: it identified sufficient problems to prevent
that candidate from advancing past the review stage and triggered another translation attempt. At the same
time, the varying number of rounds shows that review did not impose a fixed rejection cycle. Some trans-
lations passed immediately, whereas others required up to three revisions. All sections were eventually
accepted within four rounds, suggesting that the feedback was actionable enough for the translation process
to converge rather than repeatedly producing unresolved candidates.
     The data establish the usefulness of review as an active quality gate, but not its semantic accuracy in
isolation. A rejected outcome may contain one or several findings, and repeated rejections may concern
the same underlying issue. Moreover, eventual acceptance does not by itself prove that every remaining
translation choice is correct. A stronger evaluation would require issue-level review records and an inde-
pendent assessment of accepted candidates. The present evidence nevertheless shows that the review agent
made consequential decisions: it intervened in most section-level translations and converted a single-pass
generation process into an iterative generate–check–revise workflow.

5.6   Comparison with Existing Rocq Formalization
A machine-checked proof of the Odd Order theorem, constructed in the Coq Proof Assistant using the
Mathematical Components library, was announced in September 2012 by Gonthier and collaborators [14].
The Coq project was renamed The Rocq Prover in 2025 [47]; we use the current name below. At repository
level, our Lean formalization contains substantially more lines of code than the Rocq formalization. This
is a descriptive difference in code volume. It does not, by itself, measure development effort, mathematical
difficulty, or proof quality. The comparison here is deliberately restricted to the Odd Order development.
At the source level, that proof is organized around BG and PF Part I; PF Part II supports the Bender–Suzuki
development and is not used by the Rocq Odd Order development. Accordingly, Table 9 compares the shared
BG and PF Part I section breakdown, while the root-closure totals below additionally include every project
declaration—that is, every named theorem or definition—needed by the root theorem, including declarations

                                                     37
outside that breakdown. Neither quantity represents all Lean code in our repository. We therefore compare
the two developments along three dimensions: their organization and proof routes over the shared sources,
their code volume, and their checks on the final theorem and its logical assumptions.

Shared source structure, different proof routes. Both developments replace the original 255-page proof
of Feit and Thompson [12] with the same later two-volume route: the BG volume on local analysis [7] and
PF Part I on character theory [42]. Both also preserve the section structure of those sources. The Rocq
development consists of the files BGsection1.v to BGsection16.v, then BGappendixAB.v and
BGappendixC.v, then PFsection1.v to PFsection14.v. Our directories carry the same names,
with no counterpart to BGappendixAB.v. A section-by-section comparison is therefore possible, and we
report one in Table 9. The unusually close alignment of source boundaries makes this comparison more
informative than a repository-wide line count, while the remaining differences in libraries and proof style
still preclude a direct effort comparison.
     The shared decomposition comes from the shared sources, but the developments diverge in four aspects:

   1. Proof route through BG’s appendices. For the principal proof-route divergence, our development
      departs from BG. BG’s Appendix B proves Puig’s theorem, presenting it as the analogue of [15,
      Theorem 8.2.11] on Z(J(S)), and the Rocq development follows this route: it formalizes BG’s Ap-
      pendices A and B in BGappendixAB.v and uses the Puig subgroup in four further files. We instead
      prove Glauberman’s theorem on Z(J(S)) itself, following [15, Chapter 8]. No subgroup of Puig’s
      kind occurs under any name in our formalization: every subgroup we define as a supremum of a
      family of subgroups is a p-core, a π-core, the Fitting subgroup, or Thompson’s J.

   2. Use of analysis. The Rocq proof is free of analysis by construction and uses only the field algC of
      algebraic numbers containing character values. Our development, by contrast, uses both the complex
      numbers of Mathlib and real analysis.

   3. Division into declarations. The declaration counts are likewise not in section-by-section correspon-
      dence: our development has fewer declarations than the Rocq development in five sections, but eighty
      times as many in PF Part I Section 6. Such a spread is consistent with an autoformalized devel-
      opment in which many additional declarations are helper lemmas and their number depends on the
      decomposition found by R EFINE AGENT, rather than directly on the source structure.

   4. Type-I maximal subgroups. The developments resolve the discrepancy between the definitions of
      type I maximal subgroups discussed in Section 5.2 in opposite ways. The Rocq formalization adopts
      the existential formulation in [42, Definition 8.3], whereas ours adopts the universal formulation in [7,
      Section 16]. Because the two formulations are equivalent, this representational choice does not affect
      the downstream mathematics.


Lean code volume is substantially larger, but line counts do not measure effort. The repository-level
difference is large. The Rocq development is 34 files and 40,549 lines, whereas the root-specific part of
our Lean repository that proves the same theorem is 537 files and 626,021 lines, a ratio of about fifteen to
one. Within the shared BG and PF Part I section breakdown, Table 9 records 573,050 Lean lines and 39,163
Rocq lines. These figures describe final code volume, but they are not a normalized comparison of the work
or mathematical content represented by each line. Four factors limit their interpretation.


                                                      38
        BG             Lean            Rocq                     PF Part I       Lean            Rocq
                                                   Ratio                                                    Ratio
      Section      Lines of Code   Lines of Code                Section     Lines of Code   Lines of Code
        1                4,009           1,334      3.0            1             12,236             755     16.2
        2                  174           1,154      0.2            2              7,639             830      9.2
        3               24,842           1,829     13.6            3             19,287           1,874     10.3
        4               14,140           1,411     10.0            4             11,882             995     11.9
        5                6,838             531     12.9            5             19,119           1,611     11.9
        6                6,605             317     20.8            6             25,513           1,347     18.9
        7                5,287             972      5.4            7              6,648             835      8.0
        8                7,176             398     18.0            8             19,291           1,133     17.0
        9                6,425             470     13.7            9             73,314           2,230     32.9
       10               16,858           1,500     11.2            10            42,717           1,225     34.9
       11                5,005             440     11.4            11            24,995           1,200     20.8
       12               30,374           2,680     11.3            12            19,884           1,363     14.6
       13               11,952           1,119     10.7            13            54,809           2,190     25.0
       14               20,985           2,511      8.4            14            32,388           1,261     25.7
       15               23,516           1,508     15.6
       16               11,074           1,362      8.1
    Appendix C           8,068             778     10.4
       Total           203,328          20,314     10.0          Total          369,722          18,849     19.6

                 Table 9: Lines of code by source section in the Lean and Rocq formalizations.


   1. The base libraries differ. A base library supplies reusable definitions and proved theorems on which
      a project can build. The Rocq development uses Mathematical Components, which contains extensive
      finite-group theory developed in large part for the Odd Order proof. The accounting boundary there-
      fore differs between the projects: material counted as project code on one side may already be library
      code on the other. Subtracting the shared BG and PF Part I section totals from the corresponding de-
      velopment totals leaves 52,971 Lean lines and 1,386 Rocq lines outside the shared section breakdown;
      the Rocq remainder comprises Appendices A and B, the Wielandt fixed-point file, and the stripped
      statement. A normalized comparison would also count the relevant group-theoretic portions of both
      base libraries. We do not have those measurements.

   2. The proof languages differ. Lean and Rocq use different formal languages and proof styles. In
      particular, SSREFLECT, the proof language used throughout Mathematical Components, is designed
      for concise proof scripts. A line of Lean and a line of Rocq are therefore not equivalent units of
      expression or work.

   3. Generated proofs may have a different internal structure. Automatically generated Lean proofs
      may introduce many local helper lemmas or miss refactorings that a human-maintained project would
      make. The present counts cannot distinguish necessary formal infrastructure from code that later
      refactoring might reduce.

   4. Lines of code measure volume, not quality or effort. Line counts record the amount and verbosity
      of the final code. They do not directly measure correctness, mathematical difficulty, development
      time, or project quality.

   Within these limits, the data support three descriptive conclusions. First, the Lean code volume for the
Odd Order theorem is substantially larger. Second, the difference is distributed across the source: Lean has

                                                           39
more lines in 16 of the 17 BG rows and all 14 PF Part I rows, so the aggregate is not produced by one ex-
ceptional section. Third, the section-level ratios vary from 0.2 to 34.9, with book-level ratios of 10.0 for BG
and 19.6 for PF Part I. There is therefore no stable line-count conversion factor between the developments,
and source length alone does not determine formalization volume, consistent with Section 5.1. These mea-
surements do not show that Lean or automatic formalization required fifteen times as much labor, that the
Lean proof was mathematically harder, or that the generated proof is of lower quality than the Rocq proof.

Both developments check the root theorem and its logical assumptions. A root-theorem check asks
two basic questions: (i) whether the formal statement expresses the theorem that the project claims to prove;
and (ii) whether its proof uses only the intended logical foundations. Both developments address these
questions, although they do so differently.
    The Rocq development includes stripped_odd_order_theorem.v, which gives a minimal, self-
contained formulation of the Odd Order theorem using bare Rocq logic, without notation, coercions, or
implicit arguments. The file does not merely display this formulation: it proves the stripped theorem by
connecting it to PFsection14.Feit_Thompson, with the resulting proof checked by the Rocq kernel.
The Rocq formalization also avoids additional postulated axioms.
    Our development uses comparator for a corresponding root-level check. It takes a statement written
independently of the development, using only Mathlib constants, and verifies that the theorem proved here
has the same type. It then replays the proof through the kernel and checks that its dependency closure
contains no axioms beyond the three permitted by Lean’s logic, namely propext, Classical.choice
and Quot.sound. Thus, both developments guard against two important failure modes: unintentionally
proving a different theorem and proving the intended theorem using unexpected assumptions.
    These root-level checks do not assess the source-level justification of intermediate declarations. Transla-
tion review and reconciliation provide a separate safeguard against mistranslated statements and unsupported
cross-source connections, without requiring the Lean development to reproduce the books’ organization or
proof routes.


6       Ablation Studies
We conduct ablation studies of three workflow components: dependency-aware parallelism, section-level
context sharing, and review-guided translation. For each component, we compare alternative configurations
on a fixed target and report their effects on wall time, token consumption, or translation accuracy, as appli-
cable. Unless stated otherwise, the experiments run on a Dell PowerEdge R750xa with Ubuntu 22.04.1, use
gpt-5.6-sol with the reasoning-effort setting max, and execute through the Pi agent harness5 with the
four tools described in Section 3.1. Network access is disabled, and the agents can access only the supplied
Lean repository. Reported wall time includes Lean compilation: individual files can require several minutes
to build, a full rebuild takes more than 30 minutes, and the agents invoke the compiler repeatedly while
constructing proofs.

6.1      Parallel versus Sequential Proof Construction
We compare the dependency-aware parallel execution of Section 4.2 with a sequential schedule on the proof
of Glauberman’s Z ∗ theorem. Since network access is blocked during execution, both conditions are sup-
plied in advance with correct translations of all definitions and theorem statements; the comparison therefore
    5
        https://github.com/earendil-works/pi


                                                      40
isolates proof construction rather than source retrieval or statement translation. The parallel condition per-
mits at most ten concurrent P ROVER instances; individual instances run for between 0.13 and 7.6 hours.
Section-level context sharing is enabled in this experiment.

             Execution Mode                              Wall Time      Total Tokens   Output Tokens
             Sequential                                       51.4 h   2,085,361,637          7,645,079
             Parallel                                         12.3 h   3,038,587,634          9,077,309
             Relative change (parallel vs. sequential)       −76.1%         +45.7%             +18.7%

Table 10: Parallel and sequential proof construction for Glauberman’s Z ∗ theorem. Wall time includes Lean
compilation.

    Table 10 exhibits a direct time–compute tradeoff. Parallel execution reduces wall time from 51.4 to 12.3
hours, a 76.1% reduction or a 4.2× speedup, while increasing total token consumption by 45.7%. Output-
token consumption increases more modestly, from 7,645,079 to 9,077,309, or 18.7%. Aggregate total-token
consumption per wall-clock hour consequently rises from approximately 40.6 million to 247.4 million,
reflecting the simultaneous activity of multiple P ROVER instances. Parallelization is therefore effective at
converting additional inference capacity into shorter elapsed time, but it is not a token-saving mechanism.
The relevant benefit is critical-path compression: independent proof obligations advance concurrently, so
overall completion is governed more by the slowest active branches than by the sum of all branch durations.

6.2   Effect of Section-Level Context Sharing
We evaluate the section-level reuse mechanism of Section 4.1 on PF Part II, Chapter 4, Section 3. In the
sharing condition, a single P ROVER trajectory processes the theorems in sequence: after a theorem is proved,
the agent session is not terminated, and the instruction for the next theorem is appended to the accumulated
model context. Thus, the interaction history records source-specific notation and assumptions, earlier proof
attempts, relevant local declarations, and discovered Mathlib interfaces. This model context is distinct from
the Lean proof context and persists across theorem boundaries. In the no-sharing condition, each theorem
instead begins in a fresh session, for 21 sessions in total. In both conditions, the theorems are proved
sequentially without dependency-aware batch parallelization.

                       Condition                Wall Time      Total Tokens   Output Tokens
                       No sharing                   23.6 h     520,807,040         923,108
                       Section-level sharing        17.3 h     426,810,415         730,462
                       Relative reduction           26.7%           18.0%           20.9%

Table 11: Context-sharing ablation on PF Part II, Chapter 4, Section 3. Wall time includes Lean compilation.

    As shown in Table 11, section-level sharing reduces total token consumption by 18.0%, output tokens
by 20.9%, and wall time by 26.5%. In the no-sharing condition, the mathematical and formal environment
of the section must be reconstructed across 21 independent sessions. The shared trajectory amortizes this
discovery cost: once notation, standing assumptions, local declarations, and usable library interfaces have
been established, they remain available for subsequent theorems. The consistent reductions across all three
measures show that section-level context sharing is effective for this target.


                                                         41
6.3   Diagnostic Feedback in Translation Review
T RANSLATOR AGENT uses an LLM-based R EVIEWAGENT as a semantic judge because Lean elaboration
verifies that a proposed declaration is well typed, but not that it faithfully expresses the source statement.
The judge independently compares the source material with the candidate Lean declaration; when it rejects a
candidate, its feedback is returned to T RANSLATOR AGENT for another attempt. We conduct a pilot ablation
to distinguish the effect of this review step from the effect of the information contained in its feedback.
Source items were randomly sampled from the literature corpus, translated under one of four conditions,
and then judged manually for fidelity to the source:
   1. No review: T RANSLATOR AGENT returns its initial translation without an LLM review step.
   2. Binary decision: R EVIEWAGENT returns only Accept or Reject.
   3. Decision with diagnostics: R EVIEWAGENT returns the binary decision together with concrete find-
      ings for the next translation attempt.
   4. Self-improved review rubrics: R EVIEWAGENT’s checklist are updated by the self-improvement
      process.


                       Review Feedback             Manually Judged Correct      Tokens
                       No review                                     6/10    22,545,626
                       Binary decision                               7/10    36,060,479
                       Decision with diagnostics                     9/10    64,415,452
                       Self-improved                                10/10    59,764,652

                   Table 12: Pilot ablation of review feedback for T RANSLATOR AGENT.

     The ten problems are sampled randomly from the sources and fixed for the four runs. Table 12 reports
six correct translations among ten items without review, seven with a binary decision, nine when diagnostics
accompany the decision, and ten under the self-improved review rubric. A binary rejection prevents an
unsupported candidate from advancing, but provides no direction for revision. Diagnostics additionally
generate an explanation of the rejection, e.g. which part of the translation drifts from the source. Relative
to the fixed diagnostic condition, the self-improved rubric raises the observed count from nine to ten correct
translations while reducing token consumption from 64,415,452 to 59,764,652, a 7.2% reduction. Rather
than merely adding another review pass, the self-improvement process converts failures observed in earlier
attempts into reusable review criteria. In this sample, the simultaneous increase in observed translation
accuracy and reduction in token consumption suggests that the resulting rubric made subsequent reviews
more targeted. Together with the repeated review outcomes in Section 5.5, these results show that translation
review serves two distinct functions—candidate selection and source-grounded revision guidance—and that
the quality of the rubric affects both. The learned rubrics and their model-generated examples are shown
below.
  The learned checklist
      1. Recover inherited context. When a target occurs inside a long-running section, standing setup,
         or case analysis, verify all still-active hypotheses and previously fixed structural data. Do not
         assume that only conditions repeated beside the target remain in force.


                                                      42
     2. Preserve canonical data. If the source refers to maps, actions, subgroups, quotient actions, repre-
        sentatives, decompositions, or other objects defined earlier, ensure that the Lean declaration uses
        those canonical objects or explicitly ties parameters to them. Do not silently replace canonical
        data with arbitrary functions, actions, or instances.
        Example. For quotient group G / H, ensure the MulDistribMulAction is induced by the
        action on G. Reuse the induced quotient-action APIs rather than inventing arbitrary instances.

     3. Preserve complete structured data. When the source treats a decomposition, model, configura-
        tion, or reconstruction datum as one mathematical object, verify that every distinguished compo-
        nent relevant to its meaning is represented and preserved.

     4. Do not strengthen for implementation convenience. Reject unnecessary assumptions, type-
        classes, stronger action formulas, extra finiteness assumptions, or proof-derived properties that
        are not part of the source statement.
        Example. Conclusions of theorems should not appear in assumptions.

     5. Audit bundled interfaces for hidden strengthening. When reusing an existing project predicate,
        structure, or bundled interface, check that its hypotheses and mathematical generality match the
        source.


7   Conclusion
Large-scale source-based formalization is not only a problem of proving statements that have already been
expressed in a formal language. It requires the construction of the surrounding theory from distributed
sources whose dependencies, conventions, and occasional defects become visible only as formalization
proceeds. We introduced F ORMAT HEORIA to support this process end to end. The workflow combines
source retrieval, semantic translation, graph-based proof construction, on-demand dependency discovery,
independent review, constrained reconciliation, and human escalation, while maintaining provenance and
protecting approved declarations from unsupported downstream changes.
     The completed formalizations of the Feit–Thompson, Glauberman Z ∗ , Brauer–Suzuki, and Bender–
Suzuki theorems demonstrate the scale at which these mechanisms can operate. The analysis reveals two dis-
tinct forms of long-range structure. Source discovery leaves the boundary of the task open-ended, whereas
the declaration graph contains a broad shallow base connected to the root theorems through a narrow but
exceptionally deep backbone. The execution traces provide an operational counterpart: the largest trajec-
tories span repeated context compactions and therefore require proof state and earlier decisions to survive
well beyond a single model context. Together, these observations explain why persistent graph-based state
is a central workflow mechanism rather than merely a representation of the final proof.
     The results also show that quality control and theory integration cannot be reduced to kernel checking
alone. Review rejected the first candidate for most PF Part I sections and turned translation into an itera-
tive generate–check–revise process. Reconciliation modifications were concentrated at a small number of
representation-heavy interfaces rather than distributed in proportion to source-group size. The source cases
in Section 5.2 further distinguish repairs supported by an explicit mathematical bridge from conflicts that
require human judgment. These findings support a division of responsibility in which Lean certifies formal
correctness, review checks source fidelity, reconciliation performs only source-justified local repairs, and
unresolved semantic questions remain visible for escalation.


                                                     43
Future work. The present study remains a case study of a single large-scale formalization in finite-
group theory. Our primary direction for future work is to continue formalizing the remaining compo-
nents of the CFSG. Possible next targets include the Gorenstein–Walter theorem [20, 22, 21], the Alperin–
Brauer–Gorenstein theorem [2], followed by the Gorenstein–Harada theorem [16] and the Aschbacher–
Smith work [3], which comprises more than one thousand pages of technically demanding mathematics.
The Gorenstein–Walter theorem is already posed as a LeanEval problem [37], so a formalization of it can
be checked against a statement fixed by the benchmark rather than by us. Although the current work-
flow provides core capabilities for dependency discovery and reconciliation, scaling to these larger targets
may require more robust automated handling of source defects and cross-source misalignments. It may
also require extending the batch parallelism of Section 4.2 to dynamic scheduling, accelerating the project
by dynamically assigning independent branches, promptly propagating approved prerequisites, prioritizing
critical-path tasks, and detecting interface conflicts during branch integration.
     Two broader directions also merit investigation. One is the development of models and workflows for
improving code quality and reusability by refactoring Lean developments into stable, well-documented ab-
stractions, reducing duplicated and ad hoc constructions, and aligning reusable components with Mathlib.
Because AI-generated code can be difficult for human readers to follow, such efforts would need to empha-
size clear naming, transparent proof structures, and explanatory documentation. Another direction is the
construction of a formalization-backed knowledge base and interactive interfaces exposing the definitions,
source provenance, dependencies, and proof structure of the CFSG. The present formal library and its de-
pendency graph could provide the underlying verified content, but realizing this possibility would require
semantic annotations, links between formal declarations and their mathematical explanations, and effec-
tive tools for search, visualization, and proof navigation. Such resources could help junior mathematicians
navigate the extensive prerequisites of the CFSG, enable senior mathematicians to examine its global struc-
ture more effectively, and potentially reveal alternative proof paths, reusable intermediate results, or other
opportunities for new mathematical discoveries.


Acknowledgments
We are sincerely grateful to Richard Lyons and Ronald Solomon for their valuable discussions.


References
 [1] Tudor Achim, Alex Best, Alberto Bietti, Kevin Der, Mathïs Fédérico, Sergei Gukov, Daniel Halpern-
     Leistner, Kirsten Henningsgard, Yury Kudryashov, Alexander Meiburg, et al. Aristotle: IMO-Level
     Automated Theorem Proving. arXiv preprint arXiv:2510.01346, 2025.

 [2] Jonathan L Alperin, Richard Brauer, and Daniel Gorenstein. Finite Groups with Quasi-Dihedral and
     Wreathed Sylow 2-Subgroups. Transactions of the American Mathematical Society, 151(1):1–261,
     1970.

 [3] Michael Aschbacher and Stephen D Smith. The Classification of Quasithin Groups. American Math-
     ematical Society, 2004.

 [4] Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen McAleer, Qiaochu
     Jiang, Jia Deng, Stella R Biderman, and Sean Welleck. Llemma: An Open Language Model for


                                                     44
     Mathematics. In Proceedings of The Twelfth International Conference on Learning Representations
     (ICLR 2024), pages 40622–40649, 2024.

 [5] Anne Baanen, Matthew Robert Ballard, Johan Commelin, Bryan Gin-ge Chen, Michael Rothgang,
     and Damiano Testa. Growing Mathlib: Maintenance of a Large Scale Mathematical Library. In
     Proceedings of The 18th Conference on Intelligent Computer Mathematics (CICM 2025), pages 51–
     70. Springer, 2025.

 [6] Helmut Bender. Transitive gruppen gerader ordnung, in denen jede involution genau einen punkt
     festläßt. Journal of Algebra, 17(4):527–554, 1971.

 [7] Helmut Bender and George Glauberman. Local Analysis for the Odd Order Theorem, volume 188.
     Cambridge University Press, 1994.

 [8] Yves Bertot and Pierre Castéran. Interactive Theorem Proving and Program Development: Coq’Art:
     The Calculus of Inductive Constructions. Springer Science & Business Media, 2013.

 [9] Kevin Buzzard. Beyond the Liquid Tensor Experiment. Xena Project blog, 2022. https://xenapr
     oject.wordpress.com/2022/09/12/beyond-the-liquid-tensor-experiment/.

[10] Johan Commelin and Adam Topaz. Abstraction Boundaries and Spec Driven Development in Pure
     Mathematics. Bulletin of the American Mathematical Society, 61(2):241–255, 2024.

[11] Walter Feit. The Representation Theory of Finite Groups, volume 25 of North-Holland Mathematical
     Library. North-Holland, Amsterdam, 1982.

[12] Walter Feit and John G. Thompson. Solvability of Groups of Odd Order. Pacific Journal of Mathe-
     matics, 13(3):775–1029, 1963.

[13] Georges Gonthier. Formal Proof--The Four-Color Theorem. Notices of the AMS, 55(11):1382–1393,
     2008.

[14] Georges Gonthier, Andrea Asperti, Jeremy Avigad, Yves Bertot, Cyril Cohen, François Garillot,
     Stéphane Le Roux, Assia Mahboubi, Russell O’Connor, Sidi Ould Biha, Ioana Pasca, Laurence
     Rideau, Alexey Solovyev, Enrico Tassi, and Laurent Théry. A Machine-Checked Proof of the Odd
     Order Theorem. In Proceedings of 4th International Conference on Interactive Theorem Proving (ITP
     2013), volume 7998 of Lecture Notes in Computer Science, pages 163–179. Springer, 2013.

[15] Daniel Gorenstein. Finite Groups. Harper & Row, 1968.

[16] Daniel Gorenstein and Koichiro Harada. Finite Groups Whose 2-Subgroups Are Generated by at Most
     4 Elements, volume 147. American Mathematical Society, 1974.

[17] Daniel Gorenstein, Richard Lyons, and Ronald Solomon. The Classification of the Finite Simple
     Groups, Number 1, volume 40.1 of Mathematical Surveys and Monographs. American Mathematical
     Society, Providence, RI, 1994.

[18] Daniel Gorenstein, Richard Lyons, and Ronald Solomon. The Classification of the Finite Simple
     Groups, Number 2, volume 40.2 of Mathematical Surveys and Monographs. American Mathematical
     Society, Providence, RI, 1996.


                                                 45
[19] Daniel Gorenstein, Richard Lyons, and Ronald Solomon. The Classification of the Finite Simple
     Groups, Number 4: Part II, Chapters 1--4: Uniqueness Theorems, volume 40.4 of Mathematical
     Surveys and Monographs. American Mathematical Society, Providence, RI, 1999.

[20] Daniel Gorenstein and John H Walter. The Characterization of Finite Groups with Dihedral Sylow
     2-Subgroups. I. Journal of Algebra, 2(1):85–151, 1965.

[21] Daniel Gorenstein and John H Walter. The Characterization of Finite Groups with Dihedral Sylow
     2-Subgroups. III. Journal of Algebra, 2(3):354–393, 1965.

[22] Daniel Gorenstein and John H Walter. The Characterization of Finite Groups with Dihedral Sylow
     2-Subgroups—II. Journal of Algebra, 2(2):218–270, 1965.

[23] Thomas Hales. The Formal Proof of the Kepler Conjecture: A Critical Retrospective. arXiv preprint
     arXiv:2402.08032, 2024.

[24] Thomas Hales, Mark Adams, Gertrud Bauer, Tat Dat Dang, John Harrison, Le Truong Hoang, Cezary
     Kaliszyk, Victor Magron, Sean McLaughlin, Tat Thang Nguyen, et al. A Formal Proof of the Kepler
     Conjecture. In Forum of mathematics, Pi, volume 5, page e2. Cambridge University Press, 2017.

[25] Jr. Hall, Marshall. The Theory of Groups. Macmillan, New York, 1959.

[26] Koichiro Harada and Ronald Solomon. Finite Groups Having a Standard Component L of Type M
                                                                                             c12
     or M22 . Journal of Algebra, 319(2):621–628, 2008.
        c

[27] John Harrison. HOL Light: An Overview. In Proceedings of the 22nd International Conference on
     Theorem Proving in Higher Order Logics (TPHOLs ’09), pages 60–66. Springer, 2009.

[28] Christoph Hering. On Finite Groups Operating Doubly Transitively on Their Involutions. Archiv der
     Mathematik, 22(1):456–458, 1971.

[29] Graham Higman. Suzuki 2-Groups. Illinois Journal of Mathematics, 7(1):79–96, 1963.

[30] Jiewen Hu, Thomas Zhu, and Sean Welleck. MiniCTX: Neural Theorem Proving with (Long-) Con-
     texts. In Proceedings of The Thirteenth International Conference on Learning Representations (ICLR
     2025), volume 2025, pages 10106–10130, 2025.

[31] Yanxing Huang, Zihan Tang, Zejin Lin, Peng Li, and Yang Liu. Pessimistic Verification for Open
     Ended Math Questions. In Proceedings of the Forty-Third International Conference on Machine Learn-
     ing (ICML 2026), 2026.

[32] Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z Horváth, Goran Žužić, Eric Wieser, Aja
     Huang, Julian Schrittwieser, Yannick Schroecker, Hussain Masoom, et al. Olympiad-Level Formal
     Mathematical Reasoning with Reinforcement Learning. Nature, 651:607–613, 2026.

[33] Bertram Huppert. Endliche Gruppen I, volume 134 of Die Grundlehren der mathematischen Wis-
     senschaften. Springer, 1967.

[34] Bertram Huppert and Norman Blackburn. Finite Groups III, volume 243 of Grundlehren der mathe-
     matischen Wissenschaften. Springer, Berlin, Heidelberg, 1982.


                                                  46
[35] I. Martin Isaacs. Character Theory of Finite Groups, volume 69 of Pure and Applied Mathematics.
     Academic Press, New York, 1976.

[36] Lean FRO. Comparator. https://github.com/leanprover/comparator. Accessed
     2026-08-11.

[37] Lean FRO. LeanEval. https://github.com/leanprover/lean-eval. Accessed 2026-
     08-05.

[38] Yuanhang Liu, Yanxing Huang, Yanqiao Wang, Peng Li, and Yang Liu. AI Mathematician: Towards
     Fully Automated Frontier Mathematical Research. arXiv preprint arXiv:2505.22451, 2025.

[39] Leonardo de Moura and Sebastian Ullrich. The Lean 4 Theorem Prover and Programming Language.
     In Proceedings of the 28th International Conference on Automated Deduction (CADE-28), pages 625–
     635, Cham, 2021. Springer International Publishing.

[40] Tobias Nipkow, Markus Wenzel, and Lawrence C. Paulson. Isabelle/HOL: A Proof Assistant for
     Higher-Order Logic. Springer, 2002.

[41] Thomas Peterfalvi. Le théorème de Bender–Suzuki I. In Révision dans les groupes finis: groupes
     du type de Lie de rang 1, number 142–143 in Astérisque, pages 141–233. Société mathématique de
     France, 1986.

[42] Thomas Peterfalvi. Character Theory for the Odd Order Theorem, volume 272. Cambridge University
     Press, 2000.

[43] Stephen D. Smith. Applying the Classification of Finite Simple Groups, volume 230. American Math-
     ematical Society, 2018.

[44] Ronald Solomon. A Brief History of the Classification of the Finite Simple Groups. Bulletin of the
     American Mathematical Society, 38(3):315–352, 2001.

[45] Michio Suzuki. A New Type of Simple Groups of Finite Order. Proceedings of the National Academy
     of Sciences, 46(6):868–870, 1960.

[46] Michio Suzuki. Group Theory II, volume 248 of Grundlehren der mathematischen Wissenschaften.
     Springer, Berlin, Heidelberg, 1986.

[47] Rocq Development Team. Release of Rocq 9.0. https://rocq-prover.org/changelog/
     2025-03-12-rocq-9.0, March 2025. Accessed 2026-08-07.

[48] The mathlib Community. The Lean Mathematical Library. In Proceedings of the 9th ACM SIGPLAN
     International Conference on Certified Programs and Proofs (CPP 2020), pages 367–381, New York,
     NY, USA, 2020. Association for Computing Machinery.

[49] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li,
     and Xiaodan Liang. DeepSeek-Prover: Advancing Theorem Proving in LLMs Through Large-Scale
     Synthetic Data. arXiv preprint arXiv:2405.14333, 2024.




                                                  47
[50] Huajian Xin, Z.Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue
     Zhang, Xuan Lu, Qiushi Du, Wenjun Gao, Haowei Zhang, Qihao Zhu, Dejian Yang, Zhibin Gou, Z.F.
     Wu, Fuli Luo, and Chong Ruan. DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for
     Reinforcement Learning and Monte-Carlo Tree Search. In Proceedings of The Thirteenth International
     Conference on Learning Representations (ICLR 2025), volume 2025, pages 72274–72303, 2025.

[51] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
     Prenger, and Animashree Anandkumar. LeanDojo: Theorem Proving with Retrieval-Augmented Lan-
     guage Models. In Advances in Neural Information Processing Systems, volume 36, pages 21573–
     21612. Curran Associates, Inc., 2023.

[52] Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li, Zhongyuan Peng, Minghao Liu, Yifan Zhang,
     Zheng Yuan, Huajian Xin, Wenhao Huang, et al. FormalMATH: Benchmarking Formal Mathematical
     Reasoning of Large Language Models. arXiv preprint arXiv:2505.02735, 2025.

[53] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. MiniF2F: A Cross-System Benchmark for For-
     mal Olympiad-Level Mathematics. In Proceedings of The Tenth International Conference on Learning
     Representations (ICLR 2022), 2022.




                                                  48
A    Formalized Theorems
In this section we state the theorems formalized by the workflow. The theorems are printed here in the form
in which a reader can verify them directly against the Lean code, which is a constraint on how a statement is
written and not only on how it is proved. Three of the four need little defending on that score. Theorems 1,
2 and 3 are targets of LeanEval [37]: the statement of each is posed by the benchmark, fixed in a file a
participant is forbidden to modify, and settled before any proof is attempted. Theorem 3 is displayed below
in a simplified but equivalent form, as explained there. It was therefore not written by the same hands that
discharged it, and could not drift towards whatever turned out to be provable. Two of the three are moreover
stated over Mathlib and nothing else: Theorem 1 needs a finite group, the parity of its order, and solvability,
and this is also, verbatim, the endpoint of our own odd order library. Only Theorem 3 adds a notion of its
own, the odd core — the supremum of the normal subgroups of odd order — and that is one line long.
    Theorem 5 has neither advantage. Its statement is ours, and one side of it must name the groups be-
ing classified, which no amount of care will reduce to Mathlib’s current vocabulary. Definition 4 and the
discussion after the theorem are what we do about that.

Theorem 1 (Feit–Thompson). Let G be a finite group. If |G| is odd, then G is solvable.

Theorem 2 (Glauberman’s Z ∗ theorem). Let G be a finite group with an isolated involution t (i.e. the only
conjugate of t commuting with t is itself). Then there is a normal subgroup N ⊴ G of odd order such that
[g, t] ∈ N for all g ∈ G.

Theorem 3 (Brauer–Suzuki). Let G be a finite group whose Sylow 2-subgroups are generalized quaternion
groups of order 2n with n ≥ 3, and let t be an involution of G. Write O(G) for the odd core of G, the largest
normal subgroup of odd order. Then the image of t in G/O(G) is central.

    Theorem 3 is not the benchmark statement verbatim. What LeanEval poses, at commit ff6a35e, is the
following.
theorem brauer_suzuki {G : Type*} [Group G] [Finite G]
    (n : N) (hn : 3 ≤ n)
    (P : Sylow 2 G)
    (hquat : Nonempty ((P : Subgroup G) ≃* QuaternionGroup (2 ^ (n - 2))))
    (t : G) (ht_mem : t ∈ (P : Subgroup G)) (ht_ord : orderOf t = 2) :
    (QuotientGroup.mk t : G / oddCore G) ∈ Subgroup.center (G / oddCore G)

     Theorem 3 is this statement with ht_mem, the requirement that t lies in the named Sylow 2-subgroup
P , left out, i.e. our proof of this statement does not use the ht_mem hypothesis. The two are equivalent,
and in the direction that matters ours is the stronger: an involution lies in some Sylow 2-subgroup, all of
them are conjugate, and the conclusion never mentions the one chosen, so the hypothesis is recovered by
replacing P with a conjugate. The statement is equivalent to the more familiar one that Z(G/O(G)) has
order exactly two. The equivalence is straightforward. The center of G/O(G) has no non-trivial subgroup
of odd order, since such a subgroup would be a normal subgroup of odd order in a group with none. Thus,
the center is a 2-group and it lies inside every Sylow 2-subgroup; being central it lies in that subgroup’s
own center, which has order two because the subgroup is generalized quaternion. The image of t is then its
non-trivial element. Conversely, a center of order two visibly contains a central involution.
     The last of the four theorems is stated in terms of the notion of a strongly embedded subgroup. We set
it out on its own because it carries the weight of everything said after it. The notion is built from Mathlib
primitives alone — subgroups, conjugation, and whether an element is an involution — so a reader can

                                                      49
satisfy themselves that the Lean code matches what the literature says without leaving Mathlib’s vocabulary.
That is what makes it useful here: it is the connective between a statement that is easy to vet as correctly
formalized and the harder one, in terms of matrix groups, that the classification actually delivers.

Definition 4 (Strongly embedded subgroup). A subgroup M of a finite group X is strongly embedded if M
is proper, M contains an involution, and M ∩ M g contains no involution for every g ∈ X \ M .

    In Lean this is the whole of it:
def IsInvolution {G : Type*} [Group G] (x : G) : Prop := x ̸= 1 ∧ x ^ 2 = 1

def IsStronglyEmbedded {X : Type*} [Group X] (M : Subgroup X) : Prop :=
  M ̸= ⊤ ∧ (∃ x ∈ M, IsInvolution x) ∧
    ∀ g ∈/ M, ∀ x ∈ M ⊓ M.map (MulAut.conj g).toMonoidHom, ¬ IsInvolution x

Theorem 5 (Bender–Suzuki). For a finite simple group X the following are equivalent:

   1. X has a strongly embedded subgroup;

   2. X is isomorphic to PSL2 (2n ) with n ≥ 2, to the Suzuki group Sz(22n+1 ) with n ≥ 1, or to PSU3 (2n )
      with n ≥ 2.

     Two features of this statement are included primarily for the benefit of the reader. They illustrate what a
formalization of a theorem of this scale can provide beyond the bare fact that Lean accepts its proof.
     The first feature is that the statement is an equivalence, rather than only the classification implication
from Side 1 to Side 2 of Theorem 5. The two sides differ considerably in how readily a human reader can
inspect them. Side 2 names three families of matrix groups, two of them constructed here. Fully checking
this side requires examining the underlying constructions, particularly that of Sz(22n+1 ), which is elaborate
and has no existing counterpart in Mathlib. Side 1, by contrast, is Definition 4. It fits on three lines and can
be compared directly with the standard definition in the group-theory literature.
     The reverse implication from Side 2 to Side 1 therefore serves as a reader-facing sanity check on the
formalization. It verifies that every group belonging to one of the three explicitly constructed families has
a strongly embedded subgroup: respectively, a Borel subgroup, the stabilizer of a point of the ovoid, or the
stabilizer of an isotropic point. This direction is not needed to state the classification, and proving it directly
is itself highly nontrivial. Its formal proof consequently establishes a substantial and readily intelligible
mathematical consequence of the constructions, even for readers who do not inspect every detail of their
matrix representations. Together with the classification direction, it also shows that the three constructed
families collectively coincide with the finite simple groups possessing a strongly embedded subgroup.
     This sanity check supplements the identification of the constructions. Our PSL2 (2n ) is
ProjectiveSpecialLinearGroup (Fin 2) (GaloisField 2 n), namely Mathlib’s projec-
tive special linear group over its field of order 2n . Our PSU3 (2n ) is defined, using Mathlib’s matrix vocab-
ulary, as the group of determinant-one isometries of the Hermitian form with antidiagonal Gram matrix,
modulo scalars. Our construction of Sz(22n+1 ) is based directly on Suzuki’s original construction in [45].
Following that construction, we define it as the subgroup of GL4 (22n+1 ) generated by three explicit families
of matrices. The correspondence is therefore grounded in the published matrix construction itself. Because
this construction is substantially more involved than those of the other two families, however, checking ev-
ery detail requires considerable effort from a human reader. The equivalence provides an additional check
by formally establishing that these explicitly constructed groups possess the highly nontrivial structural
property required by the Bender–Suzuki theorem.

                                                        50
    The second feature is that Side 1 contains essentially no project-specific group-theoretic machinery. It
is stated using Mathlib’s notions of subgroups, conjugation, and lattice operations, together with a one-
line definition of an involution given four lines earlier in the same file. In the development, this side
is represented by IsStronglyEmbedded in BenderSuzuki/FinalTheorem.lean. This is the
same predicate that appears as the hypothesis of bender_suzuki, and the equivalence is formalized as
isSimpleBenderGroup_iff_exists_stronglyEmbedded, in the file Classification.lean.
Thus, the readily inspectable side of the equivalence is stated almost entirely in standard Mathlib vocabulary
and can be compared directly with the conventional mathematical formulation.
    Reading a statement is one check; the other is mechanical. Lean accepts any file that compiles, and
macros, custom tactics and new axioms give an author many tricks to compile something that does not
prove what its name suggests. The comparator [36] closes that gap: it checks that the theorem proved here
has the same type as the statement written independently of this development, then replays the proof through
the kernel, admitting no axioms beyond the three permitted ones. Section 5.6 describes how we use it.


B    Prompts
  P ROVE AGENT
    Using Lean compiler
    The following instructions focus on how to use the Lean compiler to test Lean interfaces and write
    test snippets.

  Use a disposable Lean file as the scratch surface for an investigation. Prefer a uniquely named direc-
  tory under /tmp, created with mktemp -d, so probing does not pollute the repository. If the user
  designates an existing probe file, inspect it before editing and preserve unrelated work.

  Probe loop.

     1. Import the narrowest module that exposes the declarations under study.

     2. Keep related checks and small examples together while the investigation is active.

     3. Run the probe from the repository root:
             lake env lean /tmp/<probe-directory>/Probe.lean

     4. Read the complete diagnostic, revise one uncertainty, and rerun.

     5. Put the final proof or definition in its owning module. Remove only temporary artifacts that you
        created.

  A successful probe establishes elaboration in the probe environment; it does not replace building the
  edited source module.

  Inspect declarations.   Use exact qualified names when possible:




                                                    51
import BenderSuzuki.PFchapter4section1.lemma_a

#check Subgroup.map_normalClosure
#check @Subgroup.map_normalClosure
#print Subgroup.map_normalClosure
#print axioms BenderSuzuki.PFchapter4section1.lemma_a

set_option pp.all true in
#check Subgroup.map_normalClosure

   • Use #check for the elaborated type.

   • Add @ to expose implicit arguments.

   • Use #print for the declaration body or theorem statement available through the environment.

   • Use #print axioms only after rebuilding edited source. Treat sorryAx as unresolved proof
     debt.

   • Scope set_option pp.all true with in to expose coercions, universes, reducible wrap-
     pers, and synthesized arguments without flooding the entire probe.

Inspect proof states.   Write a small example with the same imports, variables, hypotheses, and
target:
example {G : Type*} [Group G] (H : Subgroup G) : H ≤ H := by
  intro x hx
  trace_state
  exact hx
Use trace_state at the point of interest. Deliberately leaving a disposable example incomplete is
also useful because the CLI prints the remaining context and goal. A temporary sorry is permitted
only in the disposable probe; never count it as progress or copy it into finished source.
Test candidate terms in separate labeled examples or one at a time. Preserve the exact type mismatch
from a failed candidate instead of retrying it without a new reason.

Diagnose source and freshness.
   • Run lake env lean path/to/Target.lean for direct source diagnostics.

   • Convert a source path to its build target by dropping .lean and replacing / with ., then run
     lake build <Target.Module>.

   • Remember that importing ‘Target‘ loads its last built .olean; it does not expose unbuilt edits to
     Target.lean.

   • After changing source, rebuild the owning module before checking an exported declaration or its
     axioms through a probe.

   • Capture long output under /tmp and scan it with


                                                 52
                 rg "error:|warning:|sorry|unsolved goals"

      while retaining the full log for context.

When an error appears only in a downstream module, compare the exported declaration’s visibility,
import boundary, and exact elaborated type before changing the proof itself.
  Finding a proof
  The following instructions focus on how to find a proof of a theorem directly.


Establish the proof contract.

   1. Restate the target in plain mathematical language: inputs, typeclass assumptions, hypotheses, and
      conclusion.

   2. Inspect the surrounding namespace, variables, imports, visibility, and neighboring proof style.

   3. Do not silently weaken, strengthen, or replace the claim.

   4. Build the owning module before editing when a clean baseline is important.

Loop for a proof.

   1. Normalize only enough to expose the mathematical shape with dsimp, simp, or carefully chosen
      rewrites.

   2. Search the local repository, then Mathlib, before proving reusable infrastructure from scratch.

   3. Confirm promising declarations with #check or a small probe using the target imports.

   4. Decompose the proof into the smallest useful helpers. Keep theorem-local facts local or
      private; promote a helper to public API only when a real downstream consumer justifies it.

   5. Make a small source edit and run lake build <Target.Module>.

   6. Read the complete first error, inspect the local goal in a probe when needed, and fix one cause at
      a time.

   7. Once the owner builds, run the narrowest relevant downstream build. Use a full lake build
      for final integration when the change crosses libraries or build configuration.

Prefer disposable example declarations over inserting exploratory placeholders into production source.
If a top-down skeleton in source is genuinely useful, keep every sorry short-lived and explicitly
tracked, and remove all new placeholders before completion.




                                                  53
Proof construction priorities.      Use tactics in roughly this order, choosing the clearest fit rather than
forcing a fixed script:

    • Simplification: simp, simp?, dsimp, simp only, or simpa.

    • Structure: intro, refine, constructor, use, rcases, obtain, and cases.

    • Rewriting and transport: rw, nth_rw, simp_rw, change, show, convert, and calc.

    • Domain automation: ring, nlinarith, linarith, omega, or other imported tactics when
      the goal matches their domain.

    • Search automation: exact?, apply?, aesop?, and grind for exploration; retain them when
      stable and readable, otherwise use their suggestions to write explicit steps.

Prefer a short calc or named intermediate fact when it exposes the mathematical reason for a trans-
formation. Avoid large undirected automation when a few deterministic steps make dependencies and
failure modes clearer.

Decompose hard proofs.       Before a new difficult route, write a 3–8 line sketch naming:

    • the reduction from the main goal;

    • the helper declarations or local facts;

    • the key project or Mathlib dependencies;

    • the highest-risk inference.

Discharge easy normality, containment, equality, and impossible branches early. Isolate the hard core as
an explicit lemma with the weakest useful statement. Make the main theorem typecheck against helper
statements when that clarifies the architecture, then prove helpers from easiest to hardest.
If an informal source makes an unsupported jump, isolate the exact implication and try to falsify it under
weaker assumptions. Repair the hypothesis or route, prove a narrow transfer lemma, or record a blocker;
do not encode the missing inference as an axiom, opaque declaration, or unexplained sorry.

Debug common failures.

    • If simplification stalls, use simp?, inspect the suggested lemmas, then prefer a focused simp
      only [...] when stability matters.

    • If unification fails, inspect #check @name, make key arguments explicit, and check coercions
      or orientation.

    • If typeclass search fails or loops, identify the missing instance. Add it as a hypothesis or local
      haveI when mathematically justified; avoid an unnecessary global instance.

    • If the goal looks unrelated, unfold only the relevant definitions with dsimp, change, or simp
      [definition] and confirm that the statement has not drifted.


                                                     54
    • If a definition in a module file cannot unfold, add @[expose] only when unfolding is part of
      its intended interface; otherwise prove and use an exposed helper theorem.
    • If a downstream file cannot see a declaration, check public visibility and whether the depen-
      dency requires public import.
    • If a proof works only with a broader import, locate the actual dependency and decide whether the
      target should import it or the helper belongs in a lower module.

Verify completion.
   1. Build the owning module and relevant downstream target.
   2. Inspect logs for error:, warning:, sorry, and unsolved goals; explain any pre-
      existing warning that remains relevant.
   3. Scan changed Lean source for unintended sorry, axiom, and opaque declarations.
   4. Rebuild before using #print axioms Fully.Qualified.name on exported theorems.
   5. Confirm intended names, namespace, visibility, imports, and statement meaning.
   6. Run git diff -check and preserve unrelated working-tree changes.
Do not declare the task complete merely because a scratch example elaborates or one local theorem
closes; satisfy the user’s full requested scope and integration boundary.
  Long-horizon management
  The following instructions focus on how to manage the proof task using a DAG.

Since proving the targe theorem is likely to span multiple context window and sessions, maintain files
for tracking states. Update live task state incrementally during the task.

Proof state management.           In state.md, record the following information:
    • active target, the theorem being proved;
    • progress, the actions taken by the agent;
    • lessons, reusable experience for next steps;
    • validation, the acceptance gate of the target.
Keep the state file up to date.

Proof graph management. A node is a theorem, or definition whose statement is formalized or in-
troduced as a helper. A route is a tentative proof decomposition that may be refined, or pruned. Node
states are only proposed, proved, and pruned. If no usable route exists, inspect the Lean state-
ment, source theorem/proof, and dependencies, then write a short Lean-oriented proof sketch and helper
plan. If the route is blocked, choose one: split the current subnode, replace a helper, or prune the route
and create a new one.


                                                     55
R EFINE AGENT
The task is to refine the node graph and the active route. A node is a theorem, or definition whose
statement is formalized or introduced as a helper. A route is a tentative proof decomposition that may
be refined, or pruned. Node states are only proposed, proved, and pruned.
The current active target {{lean target}} is too hard to be proved directly. Please decompose it into
several helper lemmas and build a new route.

    • Isolate the exact inference, list the available hypotheses, and try to falsify the bare implication in
      a smaller setting.

    • Before a new route, write a proof sketch: goal, helpers, dependencies, and risk.

    • Prune easy branches early. Discharge normal, containment, and impossible branches first, then
      isolate the hard branch.

T RANSLATOR AGENT
Your task is to translate all definitions and theorem statements in {{source item}} in {{Lean
file}}.

Requirements.

    • You only need to formalize the statements of definitions and theorems etc., and fill the proof
      bodies with sorry.

    • Every definition and theorem must be exactly the same as the natural language version in the
      source. In particular, you should make sure the Lean version doesn’t omit assumptions in the
      source.

R EVIEWAGENT for T RANSLATOR AGENT
The task is to review {{lean file}} for whether it is a source faithful translation of {{source item}}.
The original task instruction is
‘‘‘
{{TranslatorAgent instructions}}
‘‘‘
Common pitfalls. The following is a list of common mistakes one usually makes when translating
definitions and statements to Lean. Pay attention to the list: {{learned checklist}}

R ECONCILER AGENT
Currently we need to invoke {{lean target}} in {{lean source}} as describe by the natural-language
{{source items}}. Please investigate the situation and

    • fix without changing downstream definitions or theorem statements;

    • request human investigation.

Rules for fixing.   When attempting to fix the given lean code, follow the rules:


                                                    56
   • You may change the given lean code, definitions, theorem statements, or proofs.

   • The final Lean repository must build. In particular, if you changed a given lean declaration, all
     downstream usage of the declaration must be updated.

   • You’re not allowed to modify any definitions or statements except the two given to you.

   • If you fails to fix the lean code, report to human immediately.

Common patterns.

   • If the theorem statement asserts existence, try to make the statement constructive, i.e. write down
     the concrete construction in the statement. Consider this rule in particular when downstream
     needs uniqueness of the existence.

   • The universe level parameters should be as general as possible.

   • If the desired Lean theorem cannot be invoked due to mismatched type, first write down a separate
     bridge lemma deriving the desired property from the existing assumptions.




                                                  57
