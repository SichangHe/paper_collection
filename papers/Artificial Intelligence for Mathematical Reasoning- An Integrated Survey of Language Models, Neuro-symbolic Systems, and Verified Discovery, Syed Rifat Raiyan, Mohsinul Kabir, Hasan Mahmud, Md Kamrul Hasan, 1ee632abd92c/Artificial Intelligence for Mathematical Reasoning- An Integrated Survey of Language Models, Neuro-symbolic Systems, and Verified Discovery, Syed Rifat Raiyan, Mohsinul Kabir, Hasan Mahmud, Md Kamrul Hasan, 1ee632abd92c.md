                                          Artificial Intelligence for Mathematical Reasoning:
                                              An Integrated Survey of Language Models,
                                           Neuro-symbolic Systems, and Verified Discovery
                                               Syed Rifat Raiyan1 , Mohsinul Kabir2† , Hasan Mahmud1 , Md Kamrul Hasan1 , and Sophia Ananiadou2
                                                             1
                                                               Systems and Software Lab (SSL), Department of Computer Science and Engineering,
                                                                            Islamic University of Technology, Gazipur, Bangladesh
                                                                               Email: {rifatraiyan, hasan, hasank}@iut-dhaka.edu
                                                           2
                                                             Department of Computer Science, University of Manchester, Manchester, United Kingdom
                                                            Email: {mdmohsinul.kabir, sophia.ananiadou}@manchester.ac.uk † Corresponding author



                                            Abstract — Mathematical reasoning has long served as a strin-                            I. I NTRODUCTION
                                         gent test of machine intelligence; over the past decade, it has
                                         moved from a niche problem within natural language processing
                                                                                                                 The automation of mathematical reasoning has been a defin-
                                         to one of the most consequential artificial intelligence (AI)        ing ambition of artificial intelligence since its inception [1],
                                         frontiers. This survey provides a unified account of the field’s     [2]. What began in the mid-1960s as brittle pattern-matching
arXiv:2606.08728v4 [cs.AI] 26 Jul 2026




                                         evolution, from early rule-based math word problem (MWP)             programs for templated arithmetic has, within the past four
                                         solvers and template-driven geometry systems, through neural         years alone, expanded into a landscape of systems that solve
                                         expression generation and large language model prompting, to
                                         contemporary reasoning models, multi-agent systems, neuro-
                                                                                                              Olympiad-level problems, formally verify mathematical argu-
                                         symbolic theorem provers, and verified discovery workflows. We       ments in Lean 4, and contribute to the resolution of selected
                                         organize the landscape along four axes: (i) informal reasoning       open problems posed by Paul Erdős. This survey provides an
                                         over text and diagrams, spanning MWP solving, multimodal             integrated account of that arc, connecting the classical MWP
                                         geometry, and vision–language models; (ii) formal reasoning in       lineage, multimodal geometry, formal theorem proving, and
                                         proof assistants, including autoformalization, tactic prediction,
                                         compiler-guided repair, and proof search; (iii) mathematical
                                                                                                              verified mathematical discovery through what we will call the
                                         discovery, where systems propose constructions, improve bounds,      reasoning-model era — the period beginning with OpenAI o1
                                         or assist attacks on open problems; and (iv) the inference- and      in late 2024 and continuing through DeepSeek-R1, Kimi k1.5,
                                         training-time techniques, including chain-of-thought prompting,      and Gemini Deep Think in 2025–2026, during which long-
                                         tool use, process reward models, and reinforcement learning          horizon chain-of-thought generation, reinforcement learning
                                         with verifiable rewards, that increasingly connect generation with
                                         verification. We catalog major benchmarks across grade-school
                                                                                                              from verifiable rewards (RLVR), and test-time scaling became
                                         arithmetic, competition mathematics, geometry, formal proving,       the dominant levers of progress on mathematical benchmarks.
                                         multimodal and multilingual reasoning, and expert evaluation,
                                         and we examine benchmark saturation, contamination, reporting        A. Why Mathematical Reasoning?
                                         mismatches, and the distinction between pass@1, majority voting,        Mathematics occupies a privileged place within AI research
                                         and verifier-assisted pass@k. We critically assess failure modes:    for three intertwined reasons. First, it is verifiable: unlike open-
                                         brittleness under perturbation, reward hacking, multimodal
                                         grounding failures, fragile formalization, and the energy cost       ended dialogue or summarization, the correctness of a solution
                                         of reasoning-scale inference. Drawing on recent perspectives         can in principle be decided mechanically, either by arithmetic
                                         from working mathematicians, we identify future directions           or by a proof assistant. Second, it is compositional: mastering
                                         centered on verified-discovery workflows, reasoning efficiency,      mathematics demands not simply pattern recognition but the
                                         and infrastructure to make AI-assisted formalization broadly         disciplined combination of definitions, lemmas, and logical
                                         usable. Companion materials: https://github.com/Starscream-
                                         11813/awesome-AI4Math.                                               steps, a capability that has historically eluded purely statistical
                                                                                                              approaches. Third, it is a core cognitive benchmark: mathemat-
                                            Index Terms — mathematical reasoning, large language models,      ical aptitude has long been used to gauge human intellectual
                                         multi-agent systems, math word problems, geometry problem            development [3], [4] and serves as a natural yardstick for
                                         solving, autoformalization, theorem proving, Lean 4, neuro-          machine cognition. The convergence of these three properties
                                         symbolic systems, chain-of-thought, reinforcement learning, rea-     makes mathematical reasoning, prima facie, both a technical
                                         soning models, survey                                                challenge and a proving ground for claims about what LLMs
                                                                                                              can and cannot truly do.
                                                  “Have you reason? I have. Why don’t you use it? When
                                                  it performs its proper office, what more do you require?”   B. Canonical Tasks and Running Examples
                                                           — Marcus Aurelius, Meditations (Book IV, §13)         Throughout this survey we distinguish four canonical fam-
                                                                                                              ilies of tasks:
 MWP Example                                                         Informal (natural language)
 Problem: 69 handbags are sold for $23 each. There are a total        Theorem (Euclid). There are infinitely many prime numbers.
 of 420 handbags in a boutique and the remaining handbags are
 sold for $17 each. How much did the boutique earn after selling      Proof sketch. Given any finite list of primes p1 , . . . , pk , the
 all the handbags?                                                    number N = p1 · · · pk + 1 has a prime factor not in the list.
 Expression: x = 69 × 23 + (420 − 69) × 17                            □
 Solution: 7554
                                                                                                      type-check            autoformalization
TABLE I: A prototypical Math Word Problem (MWP). Shad-                                             (Lean kernel)            (LLM-assisted)
                                                                   Formal + proof (Lean 4)
ing separates the problem statement, the induced expression,
and the final answer.                                               -- Lean 4 (mathlib)
                                                                    import Mathlib.Data.Nat.Prime.Infinite
                                                                    theorem infinitude_of_primes :
                                                                       ∀ N : Nat, ∃ p : Nat,
                                                                         N ≤ p ∧ Nat.Prime p := by
                                                                      intro N
                                                                      exact Nat.exists_infinite_primes N

                                                                   Fig. 2: Autoformalization and formal theorem proving illus-
                                                                   trated on Euclid’s theorem. The downward arrow represents
                                                                   autoformalization: an LLM translates the informal statement
                                                                   into a Lean 4 statement and proof. The upward arrow repre-
                                                                   sents verification: the Lean kernel mechanically checks every
                                                                   inference step, providing a trust guarantee that no informal
                                                                   argument can match. This two-way pipeline — generate infor-
  Fig. 1: An example from the G EOMETRY 3K [5] dataset.            mally, verify formally — is the central architecture of modern
                                                                   AI-assisted theorem proving [9], [10].

  • Math Word Problems (MWPs). A textual narrative
    describes a scenario involving one or more unknown nu-
    merical quantities and poses a question. The solver must
    recover a valid mathematical expression that evaluates         (1) associate quantities with the entities they modify; (2) han-
    to the correct numeric answer. Table I shows a classical       dle the ambiguity of natural language, including chronological
    example.                                                       and temporal relations; (3) recognize when information is irrel-
  • Geometry problem solving. A problem consists of a              evant or missing; and (4) generalize across problem structures
    textual description together with one or more diagrams.        that differ substantially from its training distribution [12], [13].
    The solver must perform joint reasoning over text and          In the problem of Table I, for example, a solver must link the
    image, apply axiomatic knowledge, and produce either a         quantity 69 to its price attribute $23, derive the residual count
    numeric answer or a rigorous proof. Figure 1 illustrates       420 − 69 before introducing the second price attribute $17,
    an example from G EOMETRY 3K [5].                              and correctly order the operations.
  • Formal theorem proving and autoformalization. Given
    a mathematical statement, often originally expressed in           For geometry, the additional challenges are (1) diagram
    natural language, the system must produce a proof that         parsing, i.e. extracting the relative configuration of points,
    is mechanically verified by a proof assistant such as          edges, and vertices; (2) cross-modal reference resolution, since
    Lean 4 [6] or Isabelle. Autoformalization refers to the        the textual description frequently leaves implicit relationships
    prerequisite task of translating informal mathematical text    expressed only in the diagram; and (3) theorem retrieval and
    into formal statements.                                        application. To solve Figure 1, a system must parse a right
  • Open-ended mathematical discovery. The system is               triangle from the diagram, identify AD = 3, BD = 14,
    asked to improve known bounds, generate counterexam-           and either apply a trigonometric identity or the altitude-on-
    ples, or solve problems with no published solution. This       hypotenuse theorem to recover CD.
    class encompasses the recent wave of AI-assisted attacks
                                                                      For formal theorem proving and autoformalization, the
    on Erdős problems and the algorithmic discoveries of
                                                                   difficulty is compounded by the scarcity of parallel informal/-
    F UN S EARCH [7] and A LPHA E VOLVE [8].
                                                                   formal corpora, the compositional nature of proof tactics, and
                                                                   the sheer size of modern libraries such as mathlib [14]. For
C. Challenges                                                      open-ended discovery, finally, the challenge is conceptual: how
   While these problems are routinely solved by humans with a      does one design a search procedure capable of producing gen-
reasonable mathematical education, their automation exposes        uinely novel mathematical constructions rather than rehashing
several deep challenges. For MWPs, a capable solver must           examples from the training set?
 Discovery Example: Erdős Minimum Overlap Problem                  of AI in actual research mathematics, informed by the public
 Problem (Erdős, 1955). Let A ∪ B = [2n] be a partition with       writings and interviews of mathematicians such as Terence
 |A| = |B| = n. For each integer −2n < k < 2n, define Mk as         Tao [28]–[30].
 the number of solutions (a, b) ∈ A × B to a − b = k. Estimate        The contributions of this survey are as follows.
              M (n) =      min        max      Mk .                   1) We chronologically trace the methodology stack for
                         A∪B=[2n] −2n<k<2n
                                                                         mathematical reasoning, from rule-based and statistical
 The minimum overlap constant µ = limn→∞ M (n)/n is known                MWP solvers of the 1980s–2010s to the large-scale
 to satisfy 0.3564 ≤ µ ≤ 0.3810 [11].
                                                                         reasoning and proving systems of 2024–2026 (Figure 5).
 AI contribution. The problem appears in the A LPHA E VOLVE
 repository of open problems [8]. Discovery systems attack it         2) We introduce the supervision-ladder framework, orga-
 by evolving partition-construction programs and using M (n)             nizing the field’s progression from hand-coded schemata
 as an automated fitness function. The task is open-ended: no            through formal proof-assistant kernels as a sequence of
 fixed answer set exists, and any improvement to either bound            increasingly informative external verifiers, and propose
 constitutes a novel mathematical result.
                                                                         an updated taxonomy of mathematical reasoning sys-
 Verification. Unlike MWPs, the “answer” is a construction (an
 explicit partition) whose quality is machine-checkable but whose        tems that integrates formal, informal, multimodal, multi-
 optimality requires proof, increasingly, in Lean 4.                     agent, and discovery-oriented approaches (Figure 4).
                                                                      3) We compile a comprehensive catalog of benchmarks,
TABLE II: A prototypical open-ended mathematical discovery               both classical (AI2, MAWPS, M ATH 23K) and
problem. The solver must produce an explicit construction (a             contemporary (PARA MAWPS, GSM8K, MATH,
partition of [2n]) that improves a known bound, not merely               MGSM,          HRM8K,         PATI G ONIT,      PGPS9K,
match a reference answer. Verification requires evaluating the           M ATH V ISTA,         O LYMPIAD B ENCH,         M INI F2F,
construction’s fitness and, for a definitive result, a formal            P ROOF N ET,      P UTNAM B ENCH,       F RONTIER M ATH,
proof of the bound. This problem class is the target of                  HLE, L IVE B ENCH), with particular attention to
evolutionary program-search systems such as F UN S EARCH [7]             multilinguality, saturation, and contamination dynamics.
and A LPHA E VOLVE [8].                                               4) We report and synthesize performance results across
                                                                         these benchmarks, documenting the shift from < 70%
                                                                         MWP accuracy in 2018 to effectively saturated grade-
D. Scope and Contributions                                               school arithmetic and Olympiad geometry by 2025.
                                                                      5) We provide a measured discussion of failure modes,
   Earlier surveys of this domain [15]–[18] focus predomi-
                                                                         drawing on probing studies such as SVAMP [12] and
nantly on pre-LLM work on arithmetic MWPs. Two more
                                                                         GSM-S YMBOLIC [13], and on recent assessments by
recent surveys [19], [20] begin to cover LLM-based methods
                                                                         working mathematicians.
but stop short of the reasoning-model era inaugurated by
                                                                      6) We articulate future directions, highlighting the human–
OpenAI o1 [21] in late 2024. Very recent ACM Computing
                                                                         AI collaborative workflows emerging around Lean 4, the
Surveys articles provide useful LLM-centric lenses: [22] orga-
                                                                         division of labor between discovery and verification, and
nizes mathematical language models by tasks, methods, and
                                                                         the open problems that remain stubbornly out of reach.
datasets, while [23] frames LLM mathematical reasoning as
the interaction of mathematical comprehension and answer                  a) What this survey does not cover: In return for
generation. The 2025 ACL Findings survey of multimodal              the breadth above, we deliberately set aside several adja-
mathematical reasoning [24] offers a valuable benchmark–            cent topics. First, we exclude general code generation and
method–challenge taxonomy for MLLMs, but naturally con-             programming-language benchmarks (H UMAN E VAL, MBPP,
centrates on visual and multimodal settings. In parallel, LLM-      SWE-B ENCH) unless their problems are explicitly mathemat-
based multi-agent surveys [25] analyze agent profiling, com-        ical; surveys such as [22] already treat the code-reasoning
munication, and capability growth across domains, leaving           axis in depth. Second, we do not cover end-to-end mathe-
room for a math-specific synthesis of debate, verification, and     matics education and intelligent tutoring systems, a sizeable
proof-oriented collaboration. A very recent survey on formal        literature with its own pedagogical desiderata, restricting our
mathematical reasoning [26] focuses narrowly on the formal          attention instead to solver capabilities that an educational
side, and a parallel survey on deep learning for theorem prov-      system might use. Third, scientific reasoning at large (chem-
ing [27] covers that sub-area in depth. Table III summarizes        istry, physics, biology, and engineering QA suites such as
how these adjacent surveys motivate our scope. Our goal is to       GPQA, S CI B ENCH, and S CI E VAL) is referenced only where
provide an integrated perspective that (i) preserves the histori-   it intersects mathematical reasoning, since dedicated surveys
cal development of MWP and geometry solvers for continuity          of that frontier are already emerging. Fourth, we touch on but
with the earlier literature, (ii) gives a current account of LLM-   do not systematically review hardware, inference-system, or
based mathematical reasoning including chain-of-thought, tool       serving-stack optimizations for long-horizon reasoning, which
use, multi-agent collaboration, and test-time scaling, (iii) cov-   lie outside our methodological remit. Finally, while we do
ers autoformalization and proof search in Lean 4 in parallel        report results from proprietary frontier systems (OpenAI o-
with the informal track, and (iv) reflects on the emerging role     series, Gemini Deep Think, Claude reasoning models) for
                                    LL M




                                           al
                                       o/M




                                           .
                               P




                                           t
                                          .




                                      lng
                                       rm
                                        M



                                      Ag



                                         .
                                       as
                            W




                                      sc
                                   Ge



                                    Re



                                    Fo

                                    Di
                           M




                                    M




                                    M
Survey                                                          Distinctive strength                      What this survey adds beyond it

 Pre-LLM MWP surveys
Zhang et al. [17]          ●       ●    ❍   ❍   ❍   ❍   ❍   ❍   First comprehensive MWP survey;           LLM, formal, multimodal, and discovery axes; reasoning-model
                                                                semantic-gap taxonomy                     era
Sundaram et al. [18]       ●       ❍    ❍   ❍   ❍   ❍   ❍   ❍   Deep-learning        MWP       methods:   Prompting, RL, formal, post-2023 LLM era, multimodal,
                                                                S EQ 2S EQ, trees, graph-based            discovery
 Broad reasoning surveys
Lu et al. [19]             ●       ●    ●   ❍   ❍   ●   ❍   ❍   Task taxonomy across MWPs, geome-         Reasoning models, RLVR, recent provers, discovery, supervision
                                                                try, proving, and math QA                 ladder
Ahn et al. [20]            ●       ❍    ●   ❍   ❍   ❍   ❍   ❍   Concise account of LLM math progress      Neuro-symbolic geometry, Lean-based proving, post-2024
                                                                and open challenges                       systems
 LLM-centric surveys
Liu et al. [22]            ●       ●    ●   ●   ●   ●   ❍   ●   Task / method / dataset map, incl. aug- Classical-MWP history, verification pipelines, open-problem
                                                                mented data                             discovery
Wang et al. [23]           ●       ❍    ●   ●   ●   ❍   ❍   ❍   Comprehension–generation       framing; Formal proving and discovery as co-equal axes; CGV triad
                                                                long CoT, RL, test-time scaling
 Domain-specific surveys
Yan et al. [24]            ❍       ●    ●   ●   ❍   ❍   ❍   ❍   Post-2021 map of MLLM benchmarks,         MWP lineage; 2026 formal–informal–discovery convergence
                                                                methods, failure modes
Guo et al. [25]            ❍       ❍    ●   ❍   ●   ❍   ❍   ❍   Agent profiles, communication, and co-    Math-specific synthesis of debate, verification, proof
                                                                ordination mechanisms                     collaboration
Yang et al. [26]; Li et    ❍       ❍    ●   ❍   ❍   ●   ❍   ❍   Deep coverage of proof assistants, tac-   Integrates informal MWPs, multimodal geometry, contamination
al. [27]                                                        tics, and formal benchmarks               debates

This survey                ●       ●    ●   ●   ●   ●   ●   ●   Unifies informal, multimodal, for- Positions mathematical reasoning as a progression from
                                                                mal, and discovery-oriented systems answer prediction to verified discovery
                                                                through 2026

TABLE III: Positioning of the present survey against the recent literature on AI for mathematical reasoning. The eight middle
columns form a coverage matrix over the axes this survey treats as co-equal: math word problems (MWP), geometry and
multimodal reasoning (Geo/MM), prompted / tool-augmented LLMs (LLM), reasoning-model era (Reas.), multi-agent systems
(MAgt), formal theorem proving (Formal), mathematical discovery (Disc.), and multilingual evaluation (Mlng.). Symbols:
● = comprehensive coverage; ● = partial or peripheral coverage; ❍ = not in scope. Violet sub-headers group surveys by editorial
focus. The magenta-shaded final row marks the present survey, whose distinguishing feature is being the only entry in the
table to fill every axis: by design, the paper sits at the intersection rather than within any single sub-literature.


completeness, we do not attempt independent replication,                              2) Search, Screening, and Coding: We searched Scopus,
and we flag throughout where reported numbers are vendor-                          Web of Science, ACL Anthology, IEEE Xplore, and arXiv
supplied rather than independently audited.                                        (cs.CL, cs.AI, cs.LG, and cs.SC) between January 2023 and
                                                                                   April 2026. Search strings combined task terms (e.g., “math
E. Survey Methodology                                                              word problem,” “geometry solving,” “theorem proving,” “auto-
   We followed a structured literature-review process adapted                      formalization,” “mathematical discovery”), method terms (e.g.,
from established SLR guidelines [31]. The goal was not                             “large language model,” “chain-of-thought,” “reinforcement
a statistical meta-analysis, since evaluation protocols differ                     learning,” “multi-agent,” “neuro-symbolic”), and artifact terms
sharply across MWPs, multimodal geometry, informal LLM                             (e.g., “Lean,” “proof assistant,” “benchmark,” “process reward
reasoning, and formal proof assistants. Instead, we constructed                    model”). We supplemented database search with backward
a systematic map of the field and used the map to organize                         and forward snowballing from recent surveys [15], [17]–[20],
the narrative, tables, and taxonomy.                                               [22]–[27], targeted inclusion of seminal pre-LLM papers for
   1) Research Questions: The review is guided by five ques-                       historical continuity, and arXiv monitoring through April 2026
tions. RQ1 asks how informal mathematical reasoning evolved                        for late-breaking systems.
from rule-based MWP solvers to RL-trained reasoning models.                           The initial search yielded 1,847 candidate records. After
RQ2 asks how multimodal systems use diagrams, figures,                             removing 312 duplicates, 1,535 records remained for title and
and visual tokens as mathematical evidence. RQ3 asks how                           abstract screening. We excluded 1,089 records outside the
formal theorem proving and autoformalization have progressed                       mathematical-reasoning scope, primarily general NLP, pure
toward Olympiad- and research-level mathematics. RQ4 asks                          code generation, education technology, or scientific QA with-
what counts as genuine AI-assisted mathematical discovery, as                      out an explicit mathematical-reasoning component. Full-text
distinct from rediscovery or literature retrieval. RQ5 asks how                    review of the remaining 446 records excluded a further 208
benchmarks should be designed, maintained, and reported to                         for scope mismatch, insufficient technical detail, superseded
resist saturation, contamination, and metric mismatch across                       versions, or lack of quantitative evaluation. The final corpus
languages and modalities.                                                          contains 238 included records.
             ID   Criterion                                                                       program [32], [33] or a sequence of tool calls [34]; the
             I1   Proposes, evaluates, or analyzes a method, model, dataset, benchmark, or        evaluation is delegated to a deterministic interpreter.
                  evaluation protocol for mathematical reasoning                                     Geometry Problem. A geometry instance is a tuple
             I2   Covers at least one focus area: MWPs, geometry or multimodal math,
                  theorem proving, autoformalization, discovery, or benchmark design              ⟨t, d, c⟩, where t is the problem text, d is a diagram image, and
 Inclusion




             I3   Appears in a peer-reviewed venue, workshop, technical report, or arXiv          c = {c0 , . . . , ck } is either a set of multiple-choice numerical
                  preprint with public artifacts, substantial uptake, or clear relevance to the
                  2024–2026 frontier
                                                                                                  candidates or a free-form numerical answer space. The solver
             I4   Reports quantitative results, introduces a dataset or benchmark, or provides    must predict ci ∈ c. In more recent work, the solver may also
                  a survey/theoretical framework central to the taxonomy                          be required to return a structured proof or an interpretable
             I5   Is publicly accessible by April 2026; older seminal works are retained
                  when needed for historical continuity                                           program [35], [36].
             E1   Addresses general NLP, code generation, scientific QA, or education
                                                                                                     Autoformalization and Formal Theorem Proving. Given
                  without a specific mathematical-reasoning component                             a natural language statement sNL , the autoformalization task
 Exclusion




             E2   Duplicates or is superseded by a more complete version of the same work         is to produce a formal statement sF in a target proof assistant
             E3   Provides only abstracts, slides, editorials, or non-archival commentary,
                  except official system reports needed to document frontier model releases
                                                                                                  language (Lean 4, Isabelle, Coq) that is type-checkable and
             E4   Lacks accessible full text or sufficient methodological detail for extraction   faithful to sNL [9]. The theorem-proving task, given sF , is
                                                                                                  to produce a proof term π such that the kernel of the proof
TABLE IV: Eligibility criteria used during screening and                                          assistant accepts (sF , π). Modern systems may interleave these
full-text review. The arXiv allowance reflects the rapid pace                                     two tasks [10], [37].
of AI-for-mathematics research: several influential systems                                          Mathematical Discovery. Given an underspecified math-
first appeared as preprints or official technical reports before                                  ematical problem, for instance, to establish a new lower
journal or conference publication.                                                                bound for a combinatorial quantity, or to produce an explicit
                                                                                                  counterexample, the system must output either a construction
                                                                                                  ω along with a verification certificate, or a program p whose
   Each included record was coded by primary contribution,                                        execution produces such a construction. Frameworks such
task family, method family, modality, supervision signal,                                         as F UN S EARCH [7] and A LPHA E VOLVE [8] instantiate this
evaluation benchmark, and reported performance. For visual                                        setting by having the LLM evolve a program that maximizes
clarity, Figure 3 assigns each record to one primary Sankey                                       an automated fitness function.
category; papers with multiple roles were noted during ex-                                           Boundary Tasks: Arithmetic Representation and Calcu-
traction and cross-referenced in the relevant sections, but not                                   lation. Recent mathematical-LM surveys separate mathemati-
double-counted in the figure. This keeps the corpus distribution                                  cal calculation from higher-level reasoning [22]. This category
interpretable while preserving the paper’s integrated treatment                                   includes numerical representation, digit-level arithmetic, unit
of systems that span categories.                                                                  conversion, and expression evaluation. We treat these not as
   The remainder of the paper is organized as follows. Sec-                                       separate end goals but as enabling skills: failure at arithmetic
tion II formalizes the canonical tasks. Section III surveys                                       representation can corrupt an otherwise correct MWP parse,
MWP solvers from rule-based methods through the modern                                            while reliable calculation is often best delegated to tools once
pre-training era. Section IV examines the LLM and reasoning-                                      the model has inferred the correct expression. The literature
model era. Section V covers multimodal and geometry sys-                                          covered in this survey has a cutoff of April 2026. Systems
tems. Section VI treats formal theorem proving and autofor-                                       released or published after this date are not systematically
malization. Section VII discusses mathematical discovery and                                      reviewed.
its engagement with open problems. Section VIII catalogs
benchmarks and performance. Section IX synthesizes the                                            A. Outputs, Supervision, and Grading
methodological lessons shared across these tracks. Section X                                         The four task families above differ not only in their in-
reviews failure modes and critiques. Section XI outlines future                                   put modality but also in the kind of artifact expected from
directions. Section XIII concludes.                                                               the model. This distinction matters because mathematical
                                                                                                  reasoning systems improve fastest when the artifact can be
                          II. P ROBLEM F ORMULATION                                               automatically checked. A final numerical answer gives only
                                                                                                  weak supervision; an executable program permits deterministic
   We formalize the four canonical tasks treated in this survey.                                  evaluation; a formal proof supplies a kernel-checked certifi-
   Math Word Problem. An MWP instance is a sequence                                               cate; and an open-ended construction requires a task-specific
P of word tokens VP = {v1 , . . . , vm } and numeric values                                       verifier. Table V summarizes this progression.
nP = {n1 , . . . , nl }, the former comprising entities (names,                                      This artifact-level view also clarifies why the field has
objects, units, rates) and the latter the numerical amounts                                       repeatedly moved from unstructured text toward structured in-
relevant to those entities. The goal of an MWP solver is                                          termediates. Equation trees, operation programs, Python snip-
to map P to a valid mathematical expression EP composed                                           pets, theorem-prover tactics, and Lean proof terms all reduce
from nP , a set of auxiliary constants C (e.g. π), and operators                                  ambiguity at the cost of greater annotation or search burden.
O = {+, −, ×, ÷, . . . }, such that JEP K equals the reference                                    Much of the current research frontier can be interpreted
answer. In many modern systems, EP is replaced by a Python                                        as a search for the most useful intermediate representation:
        Search and screening                                         Included set             Taxonomy axis                        Primary sub-category

                                                                                                                                             45 Classical MWP solvers
                                                                                                        105                                  12 Math foundation models
                               312                                                                      Informal
                                                                                                        text-only                            15 Prompting & tools
                               Duplicate
                               records removed
                                                                                                                                             15 Reasoning models & RL
                                                 1089                                                                                        12 Multi-agent systems
                                                 Title/abstract
                                                 excluded                                                                                    6 Verifiers & PRMs
                                                                                                        35
                                                                                                        Multimodal                           18 Classical & neural GPS
     1847                                                                                               & geometry
    Candidate
      records
                               1535                                                                                                          17 Vision-language models
                               Records after
                               deduplication                                  238                       30
                                                                              Included
                                                                              corpus
                                                                                                        Formal
                                                                                                        reasoning                            15 Neural provers
                                                 446                                                                                         15 Autoformalization & libraries
                                                 Full-text
                                                 review                                                 8
                                                                  208                                   Discovery                            3 Program search
                                                                  Full-text
                                                                  excluded                                                                   5 Open-problem workflows
                                                                                                        60                                   25 Benchmarks & evaluation
                                                                                                        Cross-cutting
                                                                                                                                             20 Multilingual resources
                                                                                                                                             15 Adjacent surveys

Fig. 3: Search, screening, and taxonomy coding pipeline for the survey corpus. The left side shows the record-selection flow
from 1,847 candidate records to 238 included records after duplicate removal, title/abstract screening, and full-text review. The
right side assigns each included record to one primary taxonomy category for counting: informal text-only reasoning dominates
because of the long MWP lineage, while discovery remains small in volume but unusually consequential for the field’s frontier.
Cross-cutting records include benchmark, multilingual-resource, and adjacent-survey papers used to structure the dataset and
evaluation discussion.


expressive enough to capture human mathematical intent, but                              templates for new problems. We provide a brief overview here;
formal enough for machines to check and learn from.                                      interested readers may consult [15] for detailed descriptions.

                III. M ATH W ORD P ROBLEM S OLVING
                                                                                         B. Statistical Methods
  The dawn of research on MWP solving was in the mid-
1960s [1], [2]. Since then, a rich succession of approaches                                 Statistical methods use generic machine-learning models
has been developed. Following and extending earlier sur-                                 such as support vector machines and Bayes classifiers to
veys [16]–[18], we organize the literature into seven cat-                               extract entities, quantities, and operators from the problem
egories: rule-based, statistical, tree-based, semantic-parsing-                          statement, and to infer the numeric answer with simple logic.
based, similarity-based, template-based, and deep-learning-                              [40] proposed an algorithm that reasoned across sentence
based methods. The deep-learning family is further decom-                                boundaries and defined a joint log-linear distribution over
posed into S EQ 2S EQ, reinforcement-learning, graph-based,                              systems of equations, employing a two-step process that first
and complex encoder/decoder sub-families.                                                selects an equation template and then instantiates it with
                                                                                         quantities from the problem. This method laid the groundwork
A. Rule-based Methods                                                                    for incorporating semantic interpretation and information ex-
   Rule-based methods are chronologically the earliest ap-                               traction into MWP solving, but it falters on problems with new
proaches. They leverage manually hard-coded schemata about                               compositional language because it lacks sufficient background
the language being analyzed to identify regularities. The author                         knowledge.
of [38] proposed W ORD P RO, coded in Interlisp-D, which                                     [96] proposed a Quantity Entailment scheme employing a
could solve one-step arithmetic problems with four predefined                            cascade of three classifiers: a Quantity Pair Classifier outputs
schemata. The author of [94] later proposed ROBUST, which                                the pair of quantities required, an Operation Classifier selects
conceptualized free-format multi-step MWPs with extraneous                               one of {+, −, ×, ÷}, and an Order Classifier (relevant for −
information using six predefined schemata. In 2010, M SW-                                and ÷) determines the most likely order of quantities. This
PAS [95] solved multi-step addition and subtraction problems                             scheme is, however, limited to single-operator expressions.
by converting the problem statements into Problem Frames                                 [39] proposed A RIS, an early attempt at more advanced
containing the whole semantic information of the problem. The                            logic templates for multi-step problems. A RIS represents the
principal drawbacks of these methods are (i) high dependency                             problem text as a world-state tuple ⟨E, C, R⟩ of Entities,
on manual features, and (ii) an inability to generate novel                              Containers, and Relations, and introduces a seven-category
                                                                                                     e    rt
                                                                                                    r




                                                                                                 xp
                                                                                                  el
                                                                                                lve
                                                                                                 h

                                                                                                  .



                                                                                              ern

                                                                                               /e
                                                                                               ec
                                                                                             atc




                                                                                             so
                                                                                            ex




                                                                                           fk

                                                                                           an
                                                                                     m




                                                                                          b.
                                                                                         de




                                                                                         m
                                                                                        oo
                                                                                  s.




                                                                                        m
                                                                                An




                                                                                     Hu
                                                                                     Co

                                                                                     Sy
Task family                      Typical output                                                          Main supervision signal




                                                                                     Pr
 MWP & competition QA            Numeric answer, symbolic expression, or         ●       ❍   ❍   ❍   ❍   Worked solutions, CoT traces, outcome rewards
                                 short rationale
 Tool-integrated math            Python or calculator calls; mixed               ❍       ●   ❍   ❍   ❍   Program-of-thought demonstrations, execution feedback
                                 NL + program traces
 Geometry & multimodal math      Numeric answer, construction, diagram           ●       ❍   ●   ❍   ●   Diagram labels, formal-language parses, theorem-application
                                 annotations, or proof sketch                                            traces
 Formal theorem proving          Lean / Isabelle / Coq statement + proof term    ❍       ❍   ❍   ●   ❍   Tactic traces, synthetic proof corpora, type-check and
                                 or tactic script                                                        proof-state feedback
 Discovery & open problems       Construction, counterexample,                   ❍       ●   ❍   ●   ●   Evolutionary fitness, verifier feedback, literature audit, formal
                                 bound-improving program, or formalized                                  certificates
                                 theorem

TABLE V: Evaluation interfaces for mathematical reasoning. The five middle columns form a coverage matrix over the grader
types each task family relies on: Ans. match (exact match, algebraic equivalence, or answer parser), Code exec. (Python
interpreter, unit tests), Symb. solver (symbolic geometry or algebra engines), Proof kernel (Lean / Isabelle / Coq), and
Human / expert review. ● = used; ❍ = not used. Colored stripes follow the paradigm palette of Figure 5 and saturate from
light to deep as the supervision constraint strengthens, mirroring the ladder argument of Section IX. Geometry and the magenta-
shaded Discovery row are the only task families whose verification requires three distinct grader types operating in combination,
the visual signature of the multi-checker turn that the survey argues defines the 2024–2026 frontier.


verb categorization. It was accompanied by the A I 3 dataset                             where I RR(q) scores the probability that quantity q is irrel-
of 395 problems, but it handles only + and −.                                            evant to the solution, PAIR(qi , qj , ⊙) scores the likelihood
    [97] considered all possible equation systems in the hy-                             that quantities qi , qj should be combined by operator ⊙, and
pothesis space and obtained a robust decision hyperplane using                           ⊙LCA (qi , qj , T ) retrieves the operator at the lowest common
support vector machines trained with quadratic programming;                              ancestor of qi and qj in expression tree T . Inference selects
it outperformed [40] but was still unable to resolve MWPs with                           the highest-scoring expression E ∗ = argmaxE∈C Score(E).
complex noun phrases and lexical features. [98] proposed a                               The concept of a quantity schema parses out the information
system that learns to apply formulae categorized as part-whole,                          relevant to each quantity. The system was evaluated on A I 2,
change, and comparison, scored against the A DD S UB dataset,                            I L, and C OMMON C ORE, with an online version implemented
but still restricted to additive operators. [99], [100] transformed                      in [102].
problem scenarios and questions into tag-based logic forms for                              A LGES [103] generates equation trees from multi-sentence
inference.                                                                               MWPs using Integer Linear Programming and scores them
   Two major drawbacks characterize this family: (i) they                                via local and global discriminative models using a compact
require manual annotation that is costly to scale, and (ii) they                         Quantified-Set (Qset) representation, selecting the tree that
rely on pre-defined templates that are inflexible with respect                           maximizes the product of local subtree likelihoods and a global
to multiplication and division.                                                          coherence factor conditioned on the problem text.
                                                                                              [104] efficiently parses problem text into projective equa-
C. Tree-based Methods                                                                    tions, assuming at most two variables and using each quantity
   Algebraic and arithmetic expressions have an inherent                                 at most once. [105] built on [101] by introducing Unit De-
binary-tree structure, which motivates tree-based solvers. In                            pendency Graphs (UDGs) that capture relationships between
these trees, leaf nodes represent constants or variables while                           the units of quantities. Each vertex in the UDG corresponds
internal nodes represent operators; operators with lower prior-                          to a quantity and is scored by its unit role (e.g., rate vs. raw
ity occupy positions higher in the tree.                                                 count), while edges encode pairwise compatibility; rate–count
    [101] pioneered the use of expression trees for MWP                                  pairs, for instance, signal multiplication rather than addition.
solving by first applying a binary classifier to discard irrelevant                      The best graph is selected by maximizing the sum of vertex
quantities, then aggregating simple prediction problems to                               and edge scores, weighted by a hyperparameter λ.
determine the Lowest Common Ancestor (LCA) of quantity                                        [106], [107] used implicit tree structures and S EQ 2S EQ
pairs. The score of an expression E represented by the tree T                            models; M ATH EN [106] introduced an equation-normalization
is                                                                                       method combined with an ensemble of Bi-LSTM [108],
                       X                                                                 C ONV S2S [109], and Transformer [110] components. These
   Score(E) = wI RR        I RR(q)                                                       tree-based models advantageously do not require addi-
                            q∈I(E)                                                       tional manual annotations such as templates, tags, or logic
                             X                                                   (1)
                        +            PAIR(qi , qj , ⊙LCA (qi , qj , T )),                forms, and directly informed the subsequent G TS [42] and
                          qi ,qj ∈I(E)
                                 /                                                       G RAPH 2T REE [43] lines.
                                                                           Rule / statistical               W ORD P RO, A RIS, template solvers [38]–[40]
                                                        Classical MWP      Seq2Seq / Seq2Tree               DNS, GTS [41], [42]
                                                                           Graph-based (Graph2Tree)         G RAPH 2T REE, M ULTI E&D [43], [44]
                                                                           Math-specific PLMs               MWP-BERT, D EDUCT R EASONER [45], [46]
                                                        Pre-trained LMs    Math foundation models           M INERVA, D EEP S EEK M ATH, Q WEN 2.5-M ATH [47]–[49]
                                   Informal text-only                      Self-improvement / bootstrap     STA R, R S TAR -M ATH, LIMO [50]–[52]
                                                                           Chain-of-thought & tools         CoT, self-consistency, PAL, T O RA [32], [34], [53], [54]
                                                        Prompting era      Semantic understanding           DUP, ToT, least-to-most [55]–[57]
                                                                           Problem decomposition            ToT, GoT, least-to-most [56]–[58]
                                                                           Reasoning models / RLVR          OpenAI o1/o3, DeepSeek-R1, Kimi k1.5, s1 [21], [59]–[61]
                                                        Scaling & agents
                                                                           Multi-agent collaboration        Debate, R E C ONCILE, MAG IC O R E, G OA [62]–[65]
                                                                           Distilled reasoning              DMAD, latent-agent distillation, debate-to-SFT
                                                                           Symbolic / neuro-symbolic        I NTER GPS, AUTO GPS, FG EO -H YPER GN ET [5], [66], [67]
                                                        Geometry solvers
  Mathematical Reasoning Systems




                                                                           Olympiad geometry                A LPHAG EOMETRY, A LPHAG EOMETRY 2 [68], [69]


                                   Multimodal                              Visual math benchmarks           M ATH V ISTA, M ATH V ERSE, MATH-V ISION [70]–[72]
                                                        Vision–language    Multimodal math models           G-LL AVA, MAVIS, M ATH -LL AVA [36], [73]
                                                                           Visual chain-of-thought          MINT-C OT, Visual Sketchpad [74]
                                                                           Tactic prediction                GPT-f , L EAN D OJO, L EAN C OPILOT [14], [75], [76]
                                                        Proving            Compiler-guided repair           APOLLO, BALDUR [77], [78]
                                                                           Large-scale provers              D EEP S EEK -P ROVER v1/v1.5/v2, K IMINA [37], [79], [80]


                                                                           Autoformalization                DSP, L EAN W ORKBOOK, PDA/FORML4 [10], [81], [82]
                                   Formal
                                                        Data & ecosystem   Library generation               M ATHLIB L EMMA, mathlib community [83], [84]
                                                                           Proof search + assistants        A LPHA P ROOF, L EAN -STA R, HTPS [85]–[87]


                                                                           Program search                   F UN S EARCH, A LPHA E VOLVE [7], [8]
                                                        Search
                                                                           Open-problem attacks             Erdős-problem workflows [88], [89]

                                                                           Process reward models            PRMs, M ATH -S HEPHERD, O MEGA PRM [90]–[92]
                                   Discovery            Supervision
                                                                           Outcome / execution              Exact-match [93], PAL [32], Lean kernel
                                                                           verifiers



Fig. 4: A taxonomy of mathematical reasoning systems. The four main axes (informal text-only, multimodal, formal, discovery)
are subdivided into thematic clusters and specific method families, with representative systems cited for each leaf. The tree
reads left-to-right: root → axis → subfield → method → examples.


D. Semantic Parsing-based Methods                                                                E. Similarity-based Methods
   [111] presented S IGMA D OLPHIN, using a newly designed                                          S IM [115] computes similarity between a test sample and
Dolphin Language (DOL) meaning-representation. DOL trees                                         training examples via weighted Jaccard coefficients of TF–
are produced by a CFG [112], [113] parser imbued with 9,600                                      IDF vectors, applies the equation system of the most similar
grammar rules, scored by                                                                         training sample, and fills its slots from the test problem. It
                      Pk                                                                         also introduced D OLPHIN 18K, a large-scale dataset of 18,460
                           L(Ti ) · Score(Ti )                                                   annotated MWPs. Similarity-based methods fail on problems
        Score(T ) = i=1 Pk                     · p(T ),  (2)
                             i=1 L(Ti )                                                          whose structural templates do not appear in the training set.
and passed to a reasoning module to produce the final answer.
                                                                                                 F. Template-based Methods
It introduced a 1,878-problem dataset from algebra.com
and answers.yahoo.com. T EXT 2M ATH [114] performs                                                 Template-based approaches identify a candidate equation
end-to-end latent-variable prediction without a priori knowl-                                    template from a pre-defined corpus and fill numeric and
edge of operators. Such parsing-based methods tend to be                                         variable slots with quantities extracted from the problem.
limited to narrow classes of number word problems.                                               Several works discussed under statistical methods adopt this
                              symbolic /                                                          prompted / tool-augmented LLMs          reasoning models, multi-agent, formal proving, verified discovery
                                                  statistical             neural MWP
                              rule-based

                            S TUDENT,            A RIS, log-
            Symbolic &
                            W ORD P RO,            linear,
       Statistical MWP       ROBUST              K USHMAN

          Neural MWP                                               M ATH 23K,        G TS,
       (Seq2Seq, Trees)                                            S EQ 2S EQ    G RAPH 2T REE


            Prompted /                                                                               G SM 8 K, CoT,
                                                                                                                           PAL/P OT,
                                                                                                      M INERVA,
  Tool-augmented LLMs                                                                                                    T O RA, PRMs
                                                                                                        verifiers

      Reasoning Models                                                                                                                        OpenAI o1,          DeepSeek-R1,       Gemini DT ⋆
           (RLVR-trained)                                                                                                                       MoA                Kimi k1.5           o3, GoA


       Formal Theorem                                                                                                     L EAN D OJO,         DSP-V1,               DSP-V2,           APOLLO,
       Provers (Lean 4)                                                                                                     MINI F2F         AlphaProof ⋆          Gödel-Prover    P UTNAM B ENCH


           Geometry &                                                                                                      G-LLaVA,         AlphaGeometry,        AlphaGeom. 2,       MARS-GPS,
           Multimodal                                                                                                     M ATH V ISTA          M AVIS             MINT-CoT           M ATH V ERSE


               Verified                                                                                                                                                                 Erdős
                                                                                                                          F UN S EARCH                            A LPHA E VOLVE
              Discovery                                                                                                                                                                workflows


                                      ≈ 50 year gap

                               1965                   2014            2017           2019          2021         2022          2023               2024                  2025                   2026
                                 ⋆ = IMO-medal milestone, AlphaProof: silver tier, 28/42 with the rarely-solved P6 (IMO 2024) · Gemini Deep Think & OpenAI reasoning: gold tier, 35/42 (IMO 2025)


Fig. 5: Chronology of AI systems for mathematical reasoning, organized as paradigm swimlanes. Early symbolic and statistical
MWP solvers (1965–2016, shown on a compressed axis) yield to neural expression generators (2017–2020), prompted and
tool-augmented LLMs (2021–2023), and the 2024–2026 convergence of RLVR-trained reasoning models, Lean-based proof
assistants, multimodal geometers, and verified-discovery systems. The seven lanes are color-coded to match Figure 4’s four-
axis taxonomy. Stars (⋆) mark IMO-medal milestones. Abbreviations: MWP = math word problem; CoT = chain-of-thought;
PAL/P OT = program-aided / program-of-thoughts prompting; PRM = process reward model; RLVR = reinforcement learning from
verifiable rewards; MoA = mixture-of-agents; GoA = graph-of-agents; DSP = DeepSeek-Prover; DT = Deep Think.


                                           +                                                                                                                    =


                        ÷                                    ×                                                                                        ÷                    n3


                n1           n2                −                     n5                                                                   +                      n2


                                          n3           n4                                                                            x           n1

Fig. 6: Expression Tree representing n1 ÷ n2 + (n3 − n4 ) × n5 .                                          Fig. 7: Equation Tree representing (x + n1 ) ÷ n2 = n3 .


scheme [40], [97], [104]. Because the search space is expo-
                                                                                                           Seq2Seq methods: [41] introduced D NS, an RNN-based
nential in the number of slots, beam-search is typically used.
                                                                                                     S EQ 2S EQ with a similarity-based retrieval component. The
M IXED SP [116] uses both explicit (equations) and implicit
                                                                                                     encoder uses GRUs [119], the decoder uses LSTM [120],
(solutions) supervision via structured-output perceptrons [117]
                                                                                                     and a Significant Number Identification (SNI) model iden-
and introduced S OL 2 K. FGE XPRESSION [118] captures rich
                                                                                                     tifies relevant numbers in the problem text. It released
information from templates by parsing them into tree struc-
                                                                                                     the landmark M ATH 23K corpus of 23,161 Chinese MWPs.
tures and defining template fragments, yielding a fine-grained
                                                                                                     E QU G ENER [121] employs a memory-network encoder with
mapping based on Longest Common Substring.
                                                                                                     an LSTM decoder and supports all four fundamental operators
G. Deep Learning-based Methods                                                                       using G LOV E [122] and learned embeddings.
  Deep-learning methods learn representations directly from                                              Deep reinforcement learning methods: M ATH DQN [123]
data, avoiding hand-designed features.                                                               was the first application of deep RL to MWPs. It formulates
expression generation as a Markov decision process in which        embedding, which is then fed to a tree decoder resembling
the agent sequentially selects quantities and operators, trained   G TS. The training loss is the standard token-level cross-
via standard DQN with an ϵ-greedy exploration strategy. Its        entropy over the decoder’s prefix-order output:
principal contribution was to show that RL could avoid the                                    E
                                                                                              X
exposure-bias problem of teacher-forced S EQ 2S EQ training,                   L(T, P ) = −         log P (yt |qt , Gc , P ).   (3)
but its accuracy gains over supervised baselines were modest.                                 t=1
      Improved Seq2Seq methods: C ASS [124] added a copy-          A parallel G RAPH 2T REE [132] uses hierarchical tree decoders
and-align mechanism and an RL objective, finding empiri-           with parent- and sibling-feeding. RODA [133] introduces a
cally that RL is preferable to maximum-likelihood estimation       reversion-based data-augmentation scheme that rewrites a
for this task. G ROUPATT [125] proposed a group-attention          problem with its inferred answer substituted for a known
mechanism that partitions the encoder’s self-attention into        quantity. S MART [134] draws on the Situation Model [135]
four parallel modules, global, quantity-related, quantity-pair,    from cognitive psychology, using attributed grammar over a
and question-related, before aggregating them into a unified       hierarchical parse graph; it was accompanied by the A SP 6.6K
representation; this decomposition lets the encoder attend to      dataset and an OOD evaluation protocol.
different functional roles of the input simultaneously, im-              Complex encoder-decoder methods: E PT [136] is an
proving quantity–operator alignment. T-R NN [126] uses a           Expression-Pointer Transformer built on ALBERT [137] that
recursive neural network to predict a tree-structured template,    addresses expression fragmentation and operand-context sep-
composing left- and right-child representations bottom-up and      aration. M ULTI E/D [138] uses both sequence- and graph-
selecting operators at each internal node via softmax; the key     based encoders (the latter based on G RAPH SAGE [139]) and
idea is that tree structure is predicted before numeric slot-      sequence- and tree-based decoders. K A -S2T [140] integrates
filling, separating structural reasoning from quantity assign-     external knowledge via a Graph Attention Network over an en-
ment. S-A LIGNED [107] is a neural symbolic model whose            tity graph. T SN -M D [141] derives multiple correct expressions
decoder generates equations by stack operations mimicking          per problem via a teacher–student ensemble with knowledge
human reasoning; it introduces operator-specific “Semantic         distillation [142]. R PKHS [143] combines a pre-trained knowl-
Transformers” that apply distinct learned nonlinear projections    edge encoder with a hierarchical-reasoning encoder, reaching
per arithmetic operator, enabling the model to learn operator-     89.8% on M AWPS. L BF [144] introduces a Learning-by-fixing
dependent composition rules rather than a single generic           framework with tree regularization. H MS [145] uses a hierar-
combination function.                                              chical word–clause–problem encoder. N S -S OLVER [146] com-
      Graph-based methods: G TS [42] imitates human                bines a problem encoder, a symbolic equation-generator de-
problem-solving with a goal-driven recursive tree-expansion        coder, and a symbolic executor with four auxiliary objectives,
decoder. It improves upon pure S EQ 2S EQ by avoiding math-        also releasing the C M 17K benchmark. R EAL [147] emulates
ematically invalid equations but cannot generate multiple          human analogical learning via memory-augmented retrieval.
valid solutions. A ST-D EC [127] is a hierarchical S EQ 2T REE     Diverging from the generative sequence-to-tree paradigm, D E -
model with an auxiliary-stack decoder producing prefix-            DUCT R EASONER [46] frames MWP solving as a complex
notation equations. D-D ECODER [128] pioneered Transformer         relation extraction task. By iteratively predicting primitive
decoders for math equations with two decoders operating in         operations over pairs of quantities, it produces explainable
opposite directions, improving BERT-style training [129].          deductive reasoning steps while achieving strong performance
    G RAPH 2T REE       [43]      fuses     Graph-Transformer      across classical benchmarks.
encoders [130], [131] with tree decoders, using two                   Before the LLM era, the strongest systems were MWP-
complementary graphs: a Quantity Cell Graph, whose edges           B ERT [45], which uses a BERT-based encoder further pre-
connect quantities that co-occur in the same sentence or share     trained on A PE 210K with a tree decoder and achieved
a syntactic dependency, and a Quantity Comparison Graph,           84.4% on M ATH 23K and 84.3% on A PE 210K; G ENER -
whose edges encode magnitude or unit-type comparisons              ATE &R ANK [44], a BART-based [148] multi-task frame-
between quantities. The reason this graph structure helps is       work reaching 85.4% on M ATH 23K; and OpenAI’s verifier-
concrete: in a problem that mentions a rate (“$23 each”)           incorporated GPT-3 [93], [149], which introduced the G SM 8K
and a count (“69 handbags”), a sequential encoder can              benchmark and demonstrated that sampling many high-
learn the rate-times-count pattern only from word-order            temperature solutions and scoring them with a trained verifier
proximity, which breaks under paraphrase or reordering; a          could yield performance gains equivalent to a 30× increase
graph encoder encodes this relationship as an explicit edge,       in model size. This last result is in some sense the seed from
making the representation invariant to surface permutation.        which the entire reasoning-model research program of 2024–
This is precisely the “quantity attachment” failure mode that      2026 would grow.
perturbation benchmarks later diagnosed (Section X).
    Architecturally, each of the K graph-convolution heads         H. Feature Engineering in the Pre-LLM Era
applies two layers of message-passing over one adjacency view         A distinguishing characteristic of pre-deep-learning work
Ak , the K outputs are concatenated, and a feed-forward block      was the explicit design of hand-crafted features. Quantity-
with residuals and layer-normalization produces the graph          related features determine whether a number is a rate versus
                                Problem: “Tom has 5 marbles. Sara gives him 3 more. How many marbles does Tom have?”



      S EQ 2T REE     token sequence → linear hidden state → tree
                                                                                                                                                                     +
                                                                                                               encodes everything
                                                 gives            more                     Sequential                hseq                  Tree
         Tom   has    5    marbles      Sara               3
                                                                                            encoder                                       decoder
                                                                                                                                                                5         3
                          processed by Bi-LSTM

                            token sequence + explicit quantity-relation graph → tree                                                                                          +
      G RAPH 2T REE                                                                                                                  encodes relations
                                                                                                                   Graph-aware            hgph            Tree
         Tom   has    5    marbles      Sara     gives     3      more                 5   same-unit    3
                                                                                                                  encoder (GNN)                          decoder
                                                                           marbles, Tom-owned marbles, given by Sara                                                      5         3


Fig. 8: A worked-example comparison of S EQ 2T REE (top) and G RAPH 2T REE (bottom) on the same problem; yellow-
highlighted tokens are extracted quantities. S EQ 2T REE must infer from the LSTM’s hidden state that the two numbers share
the unit “marbles”; G RAPH 2T REE receives this fact explicitly through a quantity-relation graph encoding “5 same-unit 3”, so
the GNN’s hidden state separates which quantities can combine arithmetically from how they appear in surface text, a structural
prior that helps most on multi-sentence problems with distractor quantities. Both pipelines share a tree decoder and produce
the same expression tree.


 Model                    Seq-Enc.       Graph-Enc.            Seq-Dec.      Tree-Dec.          Era                       Innovation (why it helped)                Bottleneck            that
                                                                                                                                                                    triggered     the     next
 DNS [41]                    ✓                                    ✓
                                                                                                                                                                    era
 Math-EN [106]               ✓                                    ✓
 T-RNN [126]                 ✓                                    ✓                               Rule-based              Verb categories & problem frames          Fixed schema vocabulary
 S-Aligned [107]             ✓                                    ✓                                                       (make implicit semantics explicit)
 Group-ATT [125]             ✓                                    ✓
                                                                                                  Statistical / parsing   Equation templates, log-linear            New compositional lan-
 D-Decoder [128]             ✓                                    ✓                                                       scoring, logical forms                    guage
 AST-Dec [127]               ✓                                                    ✓                                       (cross-sentence information;
 GTS [42]                    ✓                                                    ✓                                       interpretable slots)
 Graph2Tree [43]             ✓                  ✓                                 ✓
                                                                                                  Tree-based              Expression trees as the output space      Multi-solution problems
 Graph2Tree [132]            ✓                  ✓                                 ✓                                       (grammar-constrained valid
 Multi-E/D [138]             ✓                  ✓                 ✓               ✓                                       equations)
 MWP-BERT [45]            ✓(BERT)                                                 ✓
                                                                                                  Seq2Seq                 End-to-end neural mapping                 Fragile under perturba-
 Generate&Rank [44]       ✓(BART)                                 ✓
                                                                                                                          (removes many hand-crafted                tion; invalid equations
                                                                                                                          features)
TABLE VI: Architectural breakdown of representative pre-                                          Graph-based             Quantity-cell graphs + tree               Multi-step commonsense
LLM neural MWP solvers. Cyan shading marks systems that                                                                   decoders (captures inter-quantity         reasoning
                                                                                                                          relational structure)
add graph, pretraining, or reranking structure beyond the
                                                                                                  PLM-based               BERT/BART pretraining +                   Dataset-specific shortcuts;
earlier sequence-only pattern; magenta marks the fully hybrid                                                             decoders / rerankers (transfer            transition to LLMs
encoder–decoder design.                                                                                                   learning, stronger representations)
                                                                                                  Verifier-aug. LLMs      Sample many traces, then rank or          Reliable graders required;
                                                                                                                          check candidates (generation              semantic errors can sur-
                                                                                                                          becomes search-and-selection)             vive execution
a raw count [97], [101], [105], [116], [123]; context-related
features leverage POS tags and dependency types within a text                                   TABLE VII: Methodological progression of MWP solving,
window [101], [105], [123]; quantity-pair features distinguish                                  read as a ladder. Each row’s right column lists the failure mode
same-unit quantities (typically combined by +/−) from rate–                                     that the next row’s innovation was specifically designed to
unit pairs (typically combined by ×/÷) [101], [103], [105],                                     dissolve, so the chain runs as bottleneck → resolution → new
[123]. Question-related features identify the unit or noun                                      bottleneck through seven generations. Colored stripes follow
phrase referenced by the question [40], [96], [101], [103],                                     the paradigm palette of Figure 5 and saturate from light to
[105], [123]. Verb-related features include the dependent verb                                  deep as the supervision constraint strengthens, an in-table
of a quantity [39], [99], [101], [103], [105], [123]. Global                                    miniature of the supervision-ladder argument developed in
features capture document-level properties, including n-gram                                    Section IX. The magenta-shaded final row marks the current
statistics [40], [96], [104], [105], [123]. The transition to                                   frontier, which is also the only generation whose bottleneck
neural models obviated most of these features, although sev-                                    has not yet been resolved by a successor era.
eral reappear implicitly in the attention patterns of modern
architectures.
                                                                                                linguistic phenomena that still cause failures: quantity attach-
I. Legacy of Classical MWP Work                                                                 ment, rate interpretation, unit conversion, comparison phrases,
  Although the benchmark leaderboards have moved far be-                                        temporal order, and irrelevant clauses. Modern LLMs often
yond hand-engineered MWP systems, the classical literature                                      solve such cases without exposing a symbolic representation,
remains important for three reasons. First, it made explicit the                                but perturbation benchmarks such as SVAMP [12] and GSM-
S YMBOLIC [13] show that these same phenomena remain                 Stage           Category      Typical mechanisms          Common failure modes
diagnostic.                                                                          Linguistic    Math-heavy pretraining,     Misreading quantities or
                                                                     Comprehension
   Second, the pre-LLM systems anticipated the current em-                                         numeric representation      notation
                                                                                     Contextual    Multimodal encoders, re-    Missing hidden assump-
phasis on intermediate structure. A S EQ 2S EQ model that                                          trieval, diagram parsing    tions or geometric con-
directly maps a paragraph to a prefix expression differs in scale                                                              straints
from an o-series reasoning model, but both are asked to emit a                       Single-path   CoT, PoT/PAL, least-to-     Logically invalid or
                                                                     Generation
latent computation trace. The difference is that older systems                                     most, long CoT              needlessly       verbose
                                                                                                                               derivations
constrained the trace by grammar and templates, while current                        Multi-path    Multi-agent debate, self-   Consensus on incorrect
systems learn longer free-form traces and rely on verifiers,                                       consistency                 paths, mode collapse
rerankers, or tools to select among them.                                            Lightweight   Exact-match     graders,    Checker mismatch, brit-
   Third, classical MWP work provides a useful warning               Verification                  Python execution            tle parsing
                                                                                     Learned       Process reward models       Reward hacking, false
about overfitting to benchmark form. Many systems achieved                                         (PRMs), agent reviewers     positive signals
strong accuracy on MAWPS or M ATH 23K but failed under                               Rigorous      Theorem provers, expert     High formalization and
small paraphrases or quantity perturbations. This pattern recurs                                   human audit                 annotation costs

at every scale: whenever the dataset distribution is narrow,         TABLE VIII: A three-component view of LLM mathematical
models learn shortcuts; whenever the evaluation is refreshed,        reasoning. The table separates comprehension, generation, and
adversarial, or mechanically generated, the same models ex-          verification mechanisms and lists common failure modes for
pose gaps between answer accuracy and robust mathematical            each component.
understanding.
J. Why Structured Representations Helped: A Retrospective
                                                                     benchmark against which the reasoning capability of general-
   Viewed from the vantage point of 2026, the pre-LLM                purpose large language models would be measured. The subse-
MWP literature reveals a clear pattern: each successful method       quent five years have transformed the landscape more radically
gained its edge by making an implicit linguistic structure           than the preceding five decades. To navigate this dense enu-
explicit. Rule-based systems made verb categories and problem        meration of systems, we organize the section around what we
frames explicit; statistical methods made equation templates         call the comprehension–generation–verification (CGV) triad:
explicit; and the decisive leap came when G RAPH 2T REE [43]         the three irreducible competences a mathematical reasoner
made inter-quantity relational structure explicit through graph      must exhibit, parsing the problem (comprehension), producing
encoders. The reason graph encoders improved over sequential         a candidate solution path (generation), and certifying that the
encoders was not simply architectural fashion: quantity-cell         path is in fact valid (verification). The CGV triad refines
graphs captured cross-quantity dependencies (e.g., that a rate       the two-stage comprehension–generation framing of recent
and a count should be multiplied, not added) that a left-to-right    LLM-centric surveys [22], [23] by promoting verification
encoder could only learn indirectly from word order. This is         from an optional post-hoc filter to a co-equal component that
precisely the “quantity attachment” failure mode identified in       participates both at inference time and during training. As
Section X and the perturbation studies of SVAMP [12]: when           detailed later in Section IX, this triad maps directly onto
surface order is changed but relational structure is preserved,      the supervision ladder that drove the era’s progression: from
graph-aware models degrade less.                                     mimicking generation, to learning verification, to verifiable
   The pattern also explains what broke each era. Tem-               search.
plates broke when problem language exceeded the template
vocabulary. Supervised expression generation broke when              A. Comprehension, Generation, and Verification
evaluation moved beyond in-distribution test sets. And even             Recent LLM-centric surveys usefully distinguish between
G RAPH 2T REE broke when the problems required multi-step            mathematical comprehension, the ability to parse notation,
common-sense reasoning that no graph over explicit quantities        quantities, diagrams, definitions, and problem intent, and an-
could capture, a gap that only the implicit world knowledge of       swer generation, the ability to synthesize a valid solution path
large pretrained models would begin to close. The transition         and final answer [23]. We extend this framing with a third
to Section IV is therefore not merely chronological; it reflects     component: verification. For mathematical reasoning, compre-
a shift from designing the right intermediate structure by hand      hension and generation are necessary but insufficient, because
to learning it from data and then verifying it externally, a shift   a fluent derivation is not ipso facto a valid one. The decisive
whose consequences pervade the remainder of this survey.             shift of 2024–2026 is that verification increasingly enters both
                                                                     inference and training, through executable programs, PRMs,
       IV. T HE LLM AND R EASONING -M ODEL E RA                      symbolic geometry solvers, and proof-assistant kernels.
   Systems discussed in this section correspond to the “LLMs            This triad also clarifies the role of long chain-of-thought.
& Agents” and “Reasoning & Verification” bands in Figure 5.          Compared with short CoT, long CoT gives the model room
The publication of GSM8K [93] in late 2021 marked a pivot            for planning, exploration, backtracking, and reflection [23].
point: grade-school math word problems ceased to be a task           Its benefit, however, depends on whether search is coupled to
researchers tried to solve ad hoc and became a standard              a reliable selector. Long reasoning traces can improve Pass@k
                             parsed intent                                (PoT) [33] have the LLM translate a math problem into
      Comprehension                             Generation
                                                                          executable Python code, delegating the actual computation
• Math pretraining
• Multimodal enc.
                             Math reasoning               • CoT / PoT     to a deterministic interpreter. On GSM8K, PAL with Codex
                                quality       candidate •• Multi-agent
• Retrieval
              error                             soln.      Self-improve   achieved 72.0% top-1 accuracy, surpassing PaLM-540B with
             signal                                   reward              CoT by 15 absolute points. A recent survey of code-enhanced
                            Verification                                  reasoning usefully separates this family into single-execution
                                                                          code generation, dynamic code–language interleaving, non-
                      • Exact match / exec.
                      • PRM / ORM                                         executable program representations, and training-time code
                      • Lean kernel
                                                                          supervision [151]. This taxonomy matters for mathematics
Fig. 9: The comprehension–generation–verification triad. Solid            because code is not merely a calculator: its structured syn-
arrows show forward reasoning; dashed arrows show verifi-                 tax, modular decomposition, executable semantics, and error
cation feedback. This extends the two-stage view of recent                feedback make it an intermediate representation that is both
surveys [23] with an explicit verification loop.                          generative and partially verifiable. T O RA [34] interleaves
                                                                          natural-language reasoning with tool invocation in a single
                                                                          loop, supervised by trajectories distilled from GPT-4 and
and self-correction, but they can also amplify verbosity, hide            refined via output-space shaping. Tool-integrated reasoning has
local mistakes, and spend unnecessary compute. Consequently,              become the de facto choice for any LLM-based math system
the strongest systems increasingly pair longer generation with            when calculator-like precision is required.
stronger verification, rather than treating length itself as a                  Semantic understanding and error reduction: While CoT
proxy for reasoning quality.                                              and tool-integrated methods address calculation errors, a com-
                                                                          plementary failure mode, semantic misunderstanding of the
B. Prompting-era Innovations                                              problem statement, persists even when arithmetic is correct.
   This subsection concerns the generation and comprehension              DUP (Deeply Understanding the Problems) [55] directly tar-
components of the triad.                                                  gets this class of errors through a three-stage prompting pro-
      Chain-of-Thought prompting: [53] demonstrated that,                 tocol: (i) extract the core question from the problem text, fil-
when prompted with a handful of exemplars containing in-                  tering irrelevant background; (ii) identify only the information
termediate reasoning steps (“chains of thought”), sufficiently            relevant to that core question; and (iii) generate the solution
large language models exhibit emergent multi-step reason-                 conditioned on both. On GSM8K, DUP achieves 97.1% zero-
ing capability. On GSM8K, prompting PaLM-540B with                        shot accuracy, substantially outperforming standard CoT, and
eight chain-of-thought (CoT) exemplars yielded state-of-the-              ablations confirm that the gains arise specifically from reduced
art performance, outperforming task-specific fine-tuned sys-              semantic misinterpretation rather than improved calculation.
tems. [150] further showed that a simple zero-shot trigger                This result is important for the survey’s verification emphasis
phrase, “Let’s think step by step”, suffices to elicit similar            (see §IV-H): semantic errors are precisely the class that
behavior in sufficiently capable models.                                  execution-based verifiers cannot catch, because a program that
      Self-consistency:   [54] introduced a decoding strat-               faithfully encodes a misunderstood problem will execute cor-
egy that samples a diverse set of reasoning paths from a                  rectly but produce the wrong answer. Methods like DUP thus
CoT-prompted model and selects the most consistent final                  complement tool-integrated reasoning by operating upstream
answer by majority vote. Self-consistency yielded double-                 of the computation.
digit percentage-point gains on GSM8K (+17.9%), SVAMP                           The code–mathematics overlap: PAL, PoT, and T O RA
(+11.0%), and AQuA (+12.2%), establishing a simple but                    are presented in this survey as tool-use strategies, but they
foundational result: reasoning quality scales with the budget             also represent the convergence of mathematical reasoning
allocated to inference-time sampling.                                     with code generation. Models trained on code (e.g., Codex,
      Problem decomposition: [57] proposed least-to-most                  Code Llama, L LEMMA) consistently outperform text-only
prompting, in which an LLM first decomposes a complex                     models of similar size on math benchmarks, even without ex-
problem into a sequence of simpler sub-problems and then                  plicit math fine-tuning. This is not coincidental: programming
solves them in order. Tree of Thoughts [56] generalizes CoT               and mathematics share a requirement for precise symbolic
to a search over a tree of intermediate states, using the LM              manipulation, state tracking, compositional reasoning, and
itself as both thought generator and state evaluator, and com-            executable checking. The same properties also explain the
bining with breadth-first or depth-first search. More elaborate           failure mode of code-aided reasoning: execution can certify
scaffolds couple LLMs with Monte Carlo Tree Search over                   that a program ran correctly, but not that it formalized the
reasoning steps, drawing an explicit analogy with AlphaGo-                intended problem. The overlap implies that code-generation
style game-tree search.                                                   benchmarks (H UMAN E VAL, MBPP, L IVE C ODE B ENCH) and
      Tool-integrated reasoning: A parallel line of work ad-              mathematical benchmarks are not independent evaluations but
dresses a fundamental limitation of pure LLM reasoning:                   partially redundant measures of a shared underlying capability.
LLMs are unreliable numerical calculators. Program-Aided                  Future work should clarify whether strong performance on
Language Models (PAL) [32] and Program of Thoughts                        one reliably predicts strong performance on the other, and
                                 Wei et al., Jan 2022 [53]          Wang et al., Mar 2022 [54]     Yao et al., May 2023 [56]                 Besta et al., Aug 2023 [58]


              I–O                            CoT                                SC                           ToT                                        GoT


                                                                                 P
                                                                                                                                                         P
                                                                                                              P

                                              P




                                                                              majority
                                                                               vote
              P



              A                               A                                  A                                      A                                       A

    (a) Input–Output            (b) Chain-of-Thought                (c) Self-Consistency          (d) Tree-of-Thoughts                     (e) Graph-of-Thoughts
    neutral         promising     negative              discarded           aggregated              reason                     backtrack / refine                    aggregate


Fig. 10: Evolution of prompting topologies for mathematical reasoning. The upper timeline sketches the shift from direct
input–output prompting to chain-based, self-consistent, tree-structured, and graph-structured reasoning. The subfigures below
use a unified visual language: the problem is represented by the circular node P , the final answer by A, and intermediate
reasoning states by smaller circular nodes. Cyan nodes indicate promising or aggregated states; magenta/red nodes indicate
negatively scored or discarded states.


whether joint training on code and mathematical proofs yields                      model in successive rounds, all without distilling traces from a
synergies beyond what either domain provides alone.                                larger teacher. Together, these methods bridge prompting, SFT,
      Self-improvement and bootstrapping: A complementary                          verification, and RL: they treat the model’s own attempts as
line of work asks whether models can improve their own                             a renewable training source, but their success still depends
reasoning traces rather than merely consume human-written                          on reliable filters such as exact answers, verifiers, or external
rationales. STA R bootstraps reasoning by generating rationales                    rewards.
from a few examples, retaining or rationalizing those that
lead to correct answers, and then fine-tuning on the resulting                     C. Multi-Agent and Agentic Mathematical Reasoning
traces [50]. Q UIET-STA R generalizes this idea beyond ques-                          This subsection concerns the generation and verification
tion answering by training models to infer latent rationales                       components of the triad. A distinct inference-time strand
inside arbitrary text before predicting difficult tokens [152].                    treats mathematical reasoning not as a single trace but as
V-STA R observes that failed self-generated solutions are also                     a collaborative process among multiple LLM agents. Early
informative: it uses both correct and incorrect candidates to                      multi-agent debate work [62] asked several model instances
train a verifier, which then selects among many proposed                           to propose answers, exchange arguments over multiple rounds,
solutions at inference time [153]. R E FT combines SFT warm-                       and converge on a common final answer; it reported gains on
up with online reinforcement learning over automatically                           mathematical and strategic reasoning while reducing halluci-
sampled reasoning paths, using ground-truth answers as task                        nated factual claims. The MAD framework [156] sharpened
rewards for mathematical reasoning [154]. LIMO pushes the                          this idea into adversarial “tit-for-tat” debate with a judge,
data-efficiency side of the same agenda, arguing that carefully                    motivated by the observation that self-reflection can degenerate
selected “cognitive templates” can elicit strong mathematical                      when a model becomes overconfident in an initially wrong
reasoning from a sufficiently knowledgeable foundation model                       solution.
with surprisingly little SFT data [52]. SC O R E shifts from ra-                      For mathematics, the central benefit of multi-agent systems
tionale generation to self-correction, training a model through                    is diversity: agents can explore different solution paths, check
multi-turn reinforcement learning to improve its own second                        each other’s arithmetic, and expose hidden assumptions. R E C-
attempt after an initial answer [155]. A particularly striking                     ONCILE [63] made this explicit through a round-table proto-
result in this vein is R S TAR -M ATH [51], which demonstrates                     col in which diverse LLM agents discuss grouped answers,
that small language models (1.5B–7B parameters) can rival                          confidence scores, and answer-rectifying explanations before
frontier models on competition-level mathematics by itera-                         a confidence-weighted vote; the paper reports an 8% gain on
tively self-evolving through Monte Carlo Tree Search: the                          MATH and finds model diversity to be a key driver of im-
model generates solution candidates, a co-trained process                          provement. DY LAN [157] introduced dynamic team optimiza-
reward model scores each reasoning step, and the verified                          tion, selecting agents by an unsupervised Agent Importance
rollouts are used to improve both the policy and the reward                        Score and then allowing the selected team to communicate
Method                 Model              Settings                        GSM8K GSM-H SVAMP ASDiv SingleEq AddSub MultiArith MATH AQuA
Direct / Chain-of-Thought prompting
Direct                  Codex             Few-shot direct prompting         19.7       5.0   69.9   74.0   86.8   90.9      44.0      –   29.5
                        PaLM-540B         Few-shot CoT                      56.9         –   79.0   73.9   92.3   91.9      94.7    8.8   35.8
CoT                     GPT-4             Few-shot CoT                      92.0         –   97.0      –      –      –         –   42.5   72.4
                        GPT-4o-mini       0-shot CoT                           –         –      –      –      –      –         –   50.6      –
                        GPT-3.5           0-shot CoT                        81.6         –   78.2      –   93.1   86.1      96.7      –      –
DUP [55]                GPT-4             0-shot semantic decomposition     97.1         –   94.2      –   96.0   95.1      98.1      –   77.1
Program-aided / tool-integrated reasoning
PAL                     Codex             Few-shot program-aided LM         72.0      61.2   79.4   79.6   96.1   92.5      99.2      –      –
                        GPT-3.5           Few-shot program-aided LM         80.6         –   79.5      –   97.6   89.1      97.0      –      –
                        GPT-4o-mini       0-shot program-aided LM              –         –      –      –      –      –         –   36.6      –
PoT                     Codex             Few-shot program of thought       71.6      61.8   85.2   85.2      –   92.2      99.5      –   54.1
                        Codex             Program of thought + SC           80.0         –   89.1      –      –      –         –      –   58.6
                        GPT-4             Few-shot program of thought       97.2         –   97.4      –      –      –         –      –   84.4
T O RA                  Llama2-70B        0-shot tool-integrated            84.3      67.2   82.7   86.8      –      –         –   49.7      –
Code interleaving / program representations
MathCoder               Llama2-70B        0-shot code interleaving          83.9         –   84.9     –      –       –        –    45.1     –
MathCoder2              CodeLlama-34B 0-shot code interleaving              81.7         –   82.5     –      –       –        –    45.2     –
CodePlan                Mistral-7B        Few-shot code-form planning       59.5         –   61.4     –      –       –        –    34.3     –
INC-Math                GPT-4o-mini       0-shot code prompting                –         –      –     –      –       –        –    51.4     –
CoC                     text-davinci-003  Chain of Code                     71.0         –      –     –      –       –        –       –     –
CodePrompt              GPT-3.5           Few-shot code prompting           80.6         –   79.6     –      –       –        –       –     –

TABLE IX: Performance of representative prompting and code-aided reasoning methods on classical MWP and competition
benchmarks. Scores are reported accuracies (%) from the corresponding source papers. Dashes indicate that a result was not
reported under the matching model and prompting/tool-use setting. GSM-H abbreviates GSM-HARD.


through a task-specific dynamic network, improving arithmetic                ative samples, raising Llama3.1-8B-Instruct on MATH from
reasoning with moderate compute.                                             50.38% to 57.82%. MALT [161] divides reasoning into het-
   The next wave moves from discussion to structured or-                     erogeneous generation, verification, and refinement roles, then
chestration. M IXTURE - OF -AGENTS [158] stacks layers of                    propagates rewards through a multi-agent search tree; it reports
LLM agents, where each layer conditions on the outputs of                    relative improvements of 15.66% on MATH and 7.42% on
the previous one, demonstrating that heterogeneous model                     GSM8K. Finally, MATTRL [162] injects test-time experi-
collaboration can outperform a single strong model but at                    ences into multi-expert deliberation and consensus, reporting
substantial token and latency cost. G RAPH - OF -AGENTS [65]                 gains over both single-agent and multi-agent baselines across
addresses this cost by selecting only the most relevant agents               medicine, math, and education.
from model-card metadata, constructing directed edges from                      Reading across Table X, a clear pattern emerges: proto-
peer relevance scores, passing messages from high-relevance                  cols that rely solely on dialogue, debate, consensus voting,
to lower-relevance agents and back, and then pooling the                     are vulnerable to correlated errors whenever agents share a
refined responses. On the MATH benchmark, G OA-M EAN                         training distribution, because majority voting cannot correct
reaches 73.12% with three selected agents, compared with                     a mistake that all voters reproduce. Protocols that introduce
71.60% for six-agent Refine and 65.80% for six-agent M OA;                   external verification into the loop (role pipelines with PRM
on MMLU-Pro it also reduces calls and tokens relative to                     scoring, solver–reviewer–refiner workflows) trade communi-
M OA. A complementary hierarchical-orchestrator topology, a                  cation cost for reliability, but their gains plateau when the
project-coordinator agent supervising workstream-coordinator                 reviewer itself lacks the domain-specific knowledge to catch
agents that in turn dispatch specialised sub-agents and reviewer             subtle mathematical errors. The strongest emerging results
agents, is used by the AI co-mathematician of Zheng et                       come from systems that combine both agent diversity and a
al. [159] to scale to multi-day open-ended research workflows                verifiable checkpoint, such as MAG IC O R E’s reward-model-
rather than single-problem solves. The lesson across these de-               guided refinement or MALT’s multi-agent search tree with
signs is not simply “more agents,” but better routing, relevance             propagated rewards. This analysis suggests a practical guide-
scoring, and aggregation.                                                    line: multi-agent collaboration is cost-effective when (i) agents
   Math-specific multi-agent systems increasingly combine                    bring genuinely different capabilities or training data rather
collaboration with verifiers. MAG IC O R E [64] uses Solver,                 than being copies of the same model, (ii) the task decomposes
Reviewer, and Refiner agents, with step-wise reward-model                    into independently verifiable subtasks, and (iii) routing or
scores guiding targeted feedback; it beats self-consistency by               relevance scoring controls communication cost. When these
3.4%, Best-of-k by 3.2%, and Self-Refine by 4.0% across five                 conditions are not met, single-agent sampling with a strong
math datasets while using fewer samples. M ARS -PO [160]                     verifier typically achieves the same diversity benefits at lower
turns multi-agent outputs into preference-optimization data                  token cost (see §IV-H).
by building shared positive samples and agent-specific neg-                        A natural next question is whether the benefits of multi-
Protocol            Representative   Mathematical role        Main risk                 M INERVA [47] continued pretraining PaLM (8B/62B/540B)
                    systems
                                                                                     on a carefully curated mixture of arXiv papers, web mathe-
 Debate / consen- Debate, MAD,       Diverse attempts with    Judge bias or          matics, and math-related code, demonstrating that a moderate
sus               R E C ONCILE       confidence-weighted      consensus on a
                                     voting                   shared error           amount of domain-specific pretraining dramatically improves
 Dynamic            DY LAN, G OA     Select task-relevant     Bad agent selection    performance on MATH and MMLU-STEM without requiring
routing                              specialists and route    or noisy relevance     external tools.
                                     messages                 scores
 Role pipelines     MAG IC O R E,    Solver–reviewer–         Reviewers may miss        L LEMMA [163] extended this recipe in open-source form.
                    MALT             refiner or               subtle mathematical    By continuing Code Llama on P ROOF -P ILE -2, a 55B-token
                                     generator–verifier–      errors
                                     refiner workflows                               mixture including A LGEBRAIC S TACK, O PEN W EB M ATH, and
  Training   from   M ARS -PO,       Convert multi-agent      Preference pairs may   the arXiv subset of RedPajama, the 7B and 34B models match
teams               MALT             traces into preference   encode correlated      or exceed the unreleased Minerva models on an equi-parameter
                                     or SFT data              flaws
 Test-time RL       MATTRL           Reuse turn-level         Credit assignment
                                                                                     basis. Crucially, Llemma displays emergent tool-use and few-
                                     experience during        and cost remain open   shot theorem-proving abilities in Lean 4 without any further
                                     deliberation             problems
                                                                                     fine-tuning, foreshadowing the unification of informal and
TABLE X: Multi-agent protocols for mathematical reasoning,                           formal tracks.
with each row paired against its dominant failure mode. The                             D EEP S EEK M ATH [48] introduced a 120B-token high-
cyan-tinted column collects the architectural benefit of each                        quality math pretraining corpus mined from Common
protocol; the magenta-tinted column collects the correspond-                         Crawl via an iteratively-retrained fastText classifier.
ing risk, so any row reads as a single trade-off. Colored                            D EEP S EEK M ATH -BASE 7B reaches 64.2% on GSM8K
stripes on the Protocol column follow the paradigm palette                           and 36.2% on MATH, surpassing the closed-source Minerva
of Figure 5. The final row marks the emerging test-time-                             540B with roughly 1/77 the parameter count. The paper
learning frontier, whose benefit and risk are still the least well                   also introduced Group Relative Policy Optimization (GRPO),
understood empirically.                                                              a critic-free RL algorithm that became the standard fine-
                                                                                     tuning recipe for reasoning training in 2024–2025 (though
                                                                                     subsequent systems including Kimi k1.5 and o3 moved
agent debate can be internalized into a single model, avoiding                       toward DAPO and PPO variants).
the token and latency cost of explicit inter-agent communica-                           Q WEN 2-M ATH and Q WEN 2.5-M ATH [49] refined the self-
tion at inference time. Recent work on debate distillation pur-                      improvement pipeline further, using iteratively bootstrapped
sues exactly this idea: complete multi-agent debate transcripts                      problem-solution pairs to train process reward models that
are used as supervised training data, or diverse multi-agent                         supervise subsequent policy rounds. I NTERN LM-M ATH [164]
trajectories are converted into preference pairs for DPO/GRPO                        and M ETA M ATH [165] pushed synthetic data generation,
fine-tuning, so that the student model learns to reproduce                           with MetaMath in particular showing that simple backward-
the self-correcting, multi-perspective reasoning pattern of the                      question rewriting augmentation substantially boosts competi-
teacher ensemble in a single forward pass. Frameworks such as                        tion math performance. MA MMOTH [166] unifies chain-of-
DMAD (Diverse Multi-Agent Debate) break the “mental set”                             thought and program-of-thought training data, arguing that
of a single model by forcing agents to adopt distinct reasoning                      exposure to both formats is necessary for robust math general-
strategies during the distillation process, and interaction-graph-                   ization. W IZARD M ATH [167] applies Reinforced Evol-Instruct
based methods compress the agent communication structure                             to amplify problem difficulty iteratively.
into compact representations for student training. Complemen-
tary mechanistic work on “latent agents” investigates whether                        E. Verifiers and Process Reward Models
reasoning models trained via RLVR already develop internal
agent-like subspaces, functionally distinct reasoning modes                             This subsection concerns the verification component of the
that activate on different problem types, suggesting that long                       triad. The verifier idea introduced by [93] was dramatically
chain-of-thought models may be performing implicit multi-                            extended by “Let’s Verify Step by Step” [90], which showed
agent debate without explicit orchestration. These findings                          that process reward models (PRMs), trained to score each
have implications for both efficiency (debate-distilled single                       intermediate step in a chain of thought, significantly out-
models can match multi-agent accuracy at a fraction of the                           perform outcome reward models (ORMs) that score only
token cost) and safety (internalized debate is harder to audit                       the final answer, reaching 78% on a representative MATH
than explicit inter-agent transcripts, raising questions about                       subset. OpenAI released the PRM800K dataset of 800,000
oversight and interpretability in high-stakes mathematical ver-                      step-level correctness labels. M ATH -S HEPHERD [91] removed
ification).                                                                          the dependence on costly human annotation by estimating
                                                                                     step correctness via Monte Carlo rollouts: a step is judged
D. Math-specialized Foundation Models                                                correct if the expected accuracy of completions starting from
  This subsection primarily concerns the generation compo-                           it is high. O MEGA PRM [92] accelerated this process via a
nent of the triad. Beyond prompting, a second strand of work                         divide-and-conquer MCTS algorithm, producing over 1.5M
adapts the LLM pretraining pipeline itself to mathematics.                           process annotations without human effort. These PRMs serve
                                                                                                                                    Rt
                                                                                      A1        A2          A3
     A1                          A2       S

                                                      draft
                                                                                                                     A1                             A3
                                                              R                       B1        B2          B3
                                        refine                                                                                     A2
                 A3                                                 critique

                                                                         F                       Ag                 A4
                  J                                                                                                                 Pl


          All-to-all exchange;                    Solver→Reviewer→                         Layered DAG;                   Router selects relevant
             judge selects                         Refiner + feedback                 each layer reads all prior           subset; sparse msgs


           (a) Debate                            (b) Pipeline                              (c) MoA                   (d) Graph-of-Agents
Fig. 11: Four multi-agent topologies for mathematical reasoning. (a) Debate: fully connected rounds with a judge [62], [63].
(b) Role pipeline: Solver–Reviewer–Refiner chain with feedback [64], [161]. (c) Mixture-of-Agents: layered DAG [158].
(d) Graph-of-Agents: router selects relevant agents; grayed nodes are unselected [65]. The progression reflects the shift from
“more agents” toward routing and verification-aware orchestration.


both as rerankers at inference time and as reward models for                   the default configuration for deployed mathematical reasoning
subsequent reinforcement-learning fine-tuning.                                 systems.
      Process vs. outcome supervision: a direct comparison:
The PRM–ORM distinction deserves explicit attention because                    F. The Reasoning-Model Era (2024–2026)
it maps directly onto the survey’s central thesis that stronger                   This subsection concerns the synthesis of generation and
verification yields better systems. Uesato et al. [168] provided               verification through RL. In September 2024, OpenAI released
the earliest controlled comparison, showing that process-based                 O 1 [21], a model explicitly trained to produce long, reflective
feedback produces more reliable solvers than outcome-based                     chains of thought before answering. OpenAI reported two
feedback on GSM8K, particularly when the generator is strong                   scaling laws that would define the subsequent eighteen months
enough that most errors are subtle single-step mistakes rather                 of research: performance improves with train-time compute
than wholesale misunderstanding. Lightman et al. [90] scaled                   dedicated to RL on verifiable rewards, and it improves further
this finding, demonstrating that a PRM selecting among 1,860                   with test-time compute spent generating and evaluating inter-
sampled solutions outperforms a best-of-N ORM by a sig-                        mediate reasoning. On AIME 2024, GPT-4o averaged 12%,
nificant margin on MATH. The intuition is straightforward:                     while O 1 averaged 74% with single-sample greedy decoding,
an ORM can distinguish correct from incorrect final answers                    83% with 64-sample majority voting, and 93% when reranking
but cannot localize where the reasoning went wrong; a PRM                      1,000 samples with a learned scoring function, placing it above
can, and this localization enables both better reranking and                   the USAMO cutoff.
more targeted RL credit assignment. However, PRMs incur                           In January 2025, DeepSeek released R1 [59], which demon-
higher annotation cost (human or rollout-based), and recent                    strated that comparable reasoning behavior could be elicited in
work on O MEGA PRM and Math-Shepherd suggests that the                         an open-weights base model via pure reinforcement learning
gap narrows when rollout-based PRM labels are abundant                         on verifiable rewards, with no supervised fine-tuning on human
and cheap. The practical implication is a cost–accuracy trade-                 reasoning traces. Notably, R1-Zero exhibited emergent “aha
off: for budget-constrained deployments, ORM reranking with                    moments” and self-correction patterns purely from reward
many samples may suffice; for high-stakes applications re-                     signal. Kimi k1.5 [60] achieved similar results with outcome-
quiring traceable reasoning, PRM scoring or execution-based                    based and generative reward models, and S 1 [61] showed
checking is essential.                                                         that test-time scaling could be elicited with as little as 1,000
      Lightweight inference-time verification: A growing fam-                  curated reasoning traces. Snell et al. [169] formalized the
ily of practical systems combines CoT and PoT reasoning with                   theoretical underpinning, showing that optimal test-time com-
lightweight verifiers that require neither human annotation nor                pute allocation can be more effective than scaling model
formal proof assistants. The simplest recipe pairs a CoT gener-                parameters.
ator with a Python executor that checks numerical consistency:                    By mid-2026 the frontier had moved into the next generation
the model generates both a natural-language derivation and ex-                 of closed-weights reasoning systems, GPT-5.5 H IGH and
ecutable code, and the system accepts the answer only if both                  G EMINI 3.1 P RO T HINKING, and a matching wave of open-
agree. More sophisticated variants use a small PRM or a fine-                  weights efforts. SU-01 [170] is a representative open release:
tuned verifier to score intermediate steps, reject solutions with              a 30B activated-3B MoE backbone trained with SFT on
low-confidence transitions, and trigger re-generation. These                   ∼340K sub-8K-token trajectories followed by 200 RL steps,
lightweight verification pipelines occupy a middle ground                      but capable of stable reasoning over trajectories exceeding
between pure sampling (cheap but unreliable) and full formal                   100K tokens at inference. With test-time scaling, SU-01
verification (reliable but expensive), and they are increasingly               reaches gold-medal-level scores on IMO 2025 (35/42) and
USAMO 2026 (35/42), and clears the gold line on IPhO 2024          18 months earlier, required problem-by-problem formalization
and IPhO 2025, while GPT-5.5 H IGH reports 92.5%/92.9% on          and multi-day compute to breach.
AIME 25/26 and 80.7% overall on IMO-P ROOF B ENCH [171],             Table XI summarizes key results across representative rea-
a recent benchmark that grades proof writing rather than final     soning models.
answers, on which G EMINI 3.1 P RO T HINKING scores 72.6%
and D EEP S EEK -V3.2-S PECIALE 45.7%. The persistent rank-        G. Inference-Time Scaling as Search
ing on IMO-P ROOF B ENCH’s advanced split (64.8%, 50.0%,              This subsection concerns test-time scaling for genera-
28.6% respectively) confirms that even at the 2026 frontier,       tion and verification. The central conceptual change of the
proof-grade reasoning remains a distinguishing axis, not yet       reasoning-model era is that inference is no longer a single
saturated by either training scale or test-time compute.           forward pass. Instead, a difficult problem is treated as a search
   The RL algorithms underlying these reasoning models             problem over possible derivations. Chain-of-thought prompt-
have evolved rapidly, and recent ACM survey work frames            ing expands the state space; self-consistency samples mul-
the progression as a move from critic-based RLHF toward            tiple trajectories; multi-agent systems distribute exploration
increasingly lightweight critic-free online optimization [23].     across solvers, reviewers, verifiers, and routers; process reward
PPO, the workhorse of ChatGPT-era RLHF, uses a learned             models score partial states; tool-integrated systems externalize
value or critic model to estimate advantages, which improves       arithmetic or symbolic manipulation; and formal provers use
stability but substantially increases memory, compute, and         the proof assistant itself to prune invalid branches. This does
tuning cost [172]. ReMax removes this learned critic by using      not make neural systems equivalent to classical search engines,
a greedy response as a REINFORCE-style baseline, exploiting        but it moves them closer to the long-standing AI view of
the trajectory-level reward structure of LLM alignment [173].      problem solving as guided exploration.
RLOO further improves baseline estimation by sampling mul-            This perspective explains why test-time compute has be-
tiple responses to the same prompt and using a leave-one-out       come a first-class variable. If a model can generate many
reward mean for each candidate [174]. GRPO, introduced with        partially independent solution attempts, then selection quality
D EEP S EEK M ATH, samples a group of completions and nor-         becomes almost as important as generation quality. Majority
malizes each reward relative to the group’s mean and standard      voting helps when errors are uncorrelated; multi-agent delib-
deviation, which made critic-free RLVR especially attractive       eration helps when agents bring genuinely different priors or
for mathematical reasoning [48]. REINFORCE++ revisits the          roles; PRM reranking helps when local step quality predicts
same critic-free family with global advantage normalization,       final correctness; execution helps when the desired output is
aiming to reduce the bias and instability introduced by prompt-    a program; and Lean checking helps when the desired output
local normalization [175]. DAPO then specializes the recipe        is a proof. The open question is how to allocate the reasoning
for long-CoT reasoning at scale by combining decoupled             budget adaptively: trivial arithmetic should not consume thou-
clipping, dynamic sampling, token-level policy-gradient loss,      sands of tokens, while a hard olympiad inequality may require
and overlong-response shaping; its Clip-Higher component           many failed approaches before a useful invariant appears.
relaxes the upper clipping bound to encourage exploration and         Snell et al. [169] showed that optimal test-time compute
delay entropy collapse [176]. Offline methods such as DPO          allocation can be more effective than scaling model param-
and Step-DPO provide simpler preference-optimization alter-        eters, but this result is stated as a general principle rather
natives, including step-wise variants for long-chain reasoning,    than a quantitative law. The open question is whether mathe-
but they do not collect new rollouts during optimization           matical reasoning admits scaling exponents analogous to the
and therefore give up part of the exploration that makes           Chinchilla laws for pretraining: does doubling the number of
online RLVR useful under distribution shift [177], [178]. The      sampled reasoning traces yield a predictable reduction in error
practical consensus by mid-2025 was consequently not that          rate, and does this exponent depend on problem difficulty, do-
one optimizer had solved reasoning training, but that online       main, or verification quality? Preliminary evidence from self-
RL with verifiable rewards had become the dominant path            consistency experiments (where accuracy scales roughly as
for pushing mathematical reasoning beyond SFT and static           1 − e−αk with sample count k under mild error-independence
preference data.                                                   assumptions) and from the PRM reranking literature (where
   In April 2025, OpenAI released O 3 and O 4- MINI, with O 3      gains plateau once the best-of-k ceiling is reached) suggests
reaching 91.6% on AIME 2024, 88.9% on AIME 2025, 86.8%             that such laws exist but are domain-dependent and verifier-
on MathVista, and approximately 25.2% on FrontierMath              dependent. A first analytical step toward such laws is taken
(versus < 2% for previous frontier models). At IMO 2025, an        by Levi [182], who shows that when per-problem failure
advanced version of Gemini with Deep Think [179] operated          probabilities follow a heavy-tailed (Beta) difficulty distribu-
end-to-end in natural language on the official problem state-      tion, the residual pass@k failure rate decays as a power law
ments within the 4.5-hour competition time limit and solved        in k whose exponent is governed by the concentration of
five out of six problems for 35/42 points, achieving gold-         hard problems — a functional form that closely matches the
medal performance in the first such officially graded evaluation   empirical coverage curves of Brown et al. [183] on MATH.
of an AI system. OpenAI’s experimental system achieved a           On this account, inference-scaling exponents exist but are
comparable result. These milestones closed a gap that, only        properties of the model–benchmark pair, pace any hope for
                       PPO                      ReMax                   RLOO                     GRPO                     REINFORCE            DAPO
        Online RL                                                                                                             ++
                    Schulman ’17               Li et al. ’24         Ahmadian ’24             DeepSeekMath                                   Yu et al. ’25
         (RLVR)                                                                                                              Hu ’25
                        [172]                      [173]                  [174]                    [48]                       [175]              [176]

                     Critic-based             Greedy baseline       Leave-one-out MC         Group-normalized            Global advantage    Clip-Higher




                                                      DPO                Step-DPO                   Offline methods sacrifice exploration.
                                    Offline
                                                   Rafailov ’23          Lai et al. ’24              Online RLVR dominates for math
                                    (pref.)                                                              reasoning by mid-2025 [23].
                                                       [177]                  [178]

                                                  Implicit reward        Step-wise pref.


Fig. 12: Evolution of RL algorithms for reasoning-model training. The main track (top) shows the progression from critic-based
PPO to critic-free online methods. The offline DPO branch (bottom, dashed) provides simpler preference-based alternatives.
Cyan boxes mark the most widely adopted algorithms for reasoning training.


a universal constant. Formalizing these relationships would                           some of these errors but remained vulnerable to correlated
enable principled compute budgeting: allocating more search                           mistakes among agents sharing the same training distribution.
to harder problems and less to easier ones, rather than applying                         The decisive response was to bring in an external judge
a uniform inference budget.                                                           whose correctness criterion is independent of the generator’s
      Reporting standards: pass@k vs. greedy vs. majority                             training objective. For arithmetic, this judge is a Python
vote: A recurring source of confusion in the literature is                            interpreter. For symbolic geometry, it is a deductive database
that reported accuracies conflate fundamentally different infer-                      like DDAR. For formal mathematics, it is the Lean kernel. In
ence regimes. Three distinct metrics should be distinguished:                         each case, the judge converts mathematical reasoning from a
(i) greedy / pass@1, the accuracy of a single deterministic                           language-modeling problem into a search-and-verify problem,
forward pass, which measures the policy’s modal behavior;                             fundamentally changing the scaling dynamics: more inference
(ii) majority vote @k (self-consistency), which samples k                             compute yields more candidates, and a reliable judge ensures
independent traces and returns the plurality answer, measuring                        that at least one correct candidate is selected.
whether correct solutions are more probable than any single                              This analysis also clarifies the conditions under which multi-
incorrect one; and (iii) pass@k, the probability that at least                        agent systems are preferable to single-agent scaling. Table X
one of k samples is correct, which measures the generator’s                           lists risks for each protocol but does not synthesize them.
coverage and is relevant when a reliable verifier is available.                       The emerging consensus is that multi-agent collaboration helps
The distinction matters enormously: O 1’s AIME 2024 accu-                             when (i) agents bring genuinely different priors or capabilities
racy rises from 74% (greedy) to 83% (majority@64) to 93%                              (e.g., a symbolic solver and a neural proposer), (ii) the
(best-of-1000 + learned scorer), and D EEP S EEK -P ROVER -                           task decomposes into subtasks with independently checkable
V2’s MiniF2F score rises from ∼60% (pass@1) to 88.9%                                  outputs, and (iii) communication cost is controlled by routing
(pass@8192). These numbers reflect qualitatively different ca-                        or relevance scoring rather than all-to-all exchange [64], [65].
pabilities, policy quality, output diversity, and verifier strength,                  When these conditions are not met, for instance, when all
respectively, and comparing them across systems without con-                          agents are instances of the same model, single-agent sampling
trolling for the sampling budget and selection mechanism is                           with a strong verifier (PRM reranking or execution) is typically
misleading. We recommend that future benchmarking reports                             more cost-effective than debate [158], [169].
include, at minimum, pass@1 (greedy), majority@k for a                                   V. M ULTIMODAL AND G EOMETRY P ROBLEM S OLVING
standardized k (e.g., 64), and the total token budget per
                                                                                         Systems discussed in this section correspond to the “Geome-
problem.
                                                                                      try & Multimodal” band in Figure 5. Geometry problems have,
                                                                                      from the beginning of the field, occupied a special position as
H. Why Verification Entered the Mainstream                                            the paradigmatic multimodal mathematical task. We cover both
                                                                                      the classical symbolic tradition and the new wave of vision–
   The progression from prompting to tool use to multi-                               language systems.
agent orchestration to formal verification is not a sequence
of independent inventions; it is driven by a single recurring                         A. Classical Geometry Problem Solving
failure. Each generation of informal reasoning systems reached                          Early work on geometry understanding dates back to the
a performance ceiling at which generation quality alone could                         1980s with efficient pattern-detection methods on geometric
no longer be distinguished from generation fluency. Chain-                            diagrams [184] and engines such as G EO R EP [185] for spatial
of-thought prompting produced plausible but arithmetically                            descriptions of line drawings. B EATRIX [186], [187] was an
wrong derivations; tool integration fixed arithmetic but intro-                       early multimodal system able to parse both English text and
duced program faithfulness errors; multi-agent debate filtered                        diagrams. The authors of [188] pioneered the combination of
Model                                    Params MATH-500 GSM8K AIME’24 AIME’25 FMath GPQA-D
General-purpose frontier LLMs
GPT-4o                            –                         76.6        94.6         12.0             –         –         53.6
Claude 3.5 Sonnet                 –                         78.3        96.4            –             –         –         59.4
Gemini 1.5 Pro                    –                         67.7           –            –             –         –         59.1
Math-specialized open-weight LLMs
DeepSeekMath-RL 7B                7B                        51.7        88.2            –             –         –            –
Qwen2.5-Math 72B-Inst             72B                       85.1        95.9         30.0             –         –            –
InternLM2-Math-Plus 7B            7B                        53.0        87.2            –             –         –            –
Reasoning models (long CoT + RLVR)
OpenAI o1                         –                         94.8        97.1         83.0          79.2       <2          78.0
DeepSeek-R1                       671B                      97.3           –         79.8          70.0         –         71.5
Kimi k1.5                         –                         96.2           –         77.5             –         –            –
s1 (32B, 1K traces)               32B                       93.0           –            –             –         –         59.6
QwQ-32B-Preview                   32B                       90.6           –         50.0             –         –         65.2
Grok 3 Beta                       –                            –           –         83.9          77.3         –         80.2
OpenAI o3                         –                            –           –         91.6          88.9      25.2         83.3
OpenAI o4-mini (high)             –                            –           –        91.7†          92.7         –         81.4
Gemini 2.5 Pro                    –                         98.8           –        87.5†          86.7         –         84.0
Qwen3 (235B-A22B, thinking)       235B                      98.0           –         85.7          81.5         –         71.1
Live leaderboard snapshots (accessed May 2026)
Gemini 3 Pro§                     –                            –           –             –       100.0          –         91.9
GPT-5.2 Pro§                      –                            –           –             –       100.0          –         93.2
                      §
Claude Mythos Preview             –                            –           –             –           –          –         94.6
LongCat-Flash-Thinking§           560B                      99.2           –             –        90.6          –            –
                 §
Kimi K2 Instruct                  1.0T                      97.4        97.3             –           –          –            –
Distilled reasoning models
DeepSeek-R1-Distill-Qwen-32B      32B                       94.3           –         72.6             –         –         62.1
DeepSeek-R1-Distill-Qwen-7B       7B                        92.8           –         55.5             –         –         49.1
DeepScaleR 1.5B                   1.5B                         –           –         43.1             –         –            –
LIMO 32B                          32B                       95.6           –         63.3             –         –         70.7

TABLE XI: Comparison of frontier, math-specialized, reasoning, and distilled models. GPQA-D = GPQA-Diamond; FMath
= FrontierMath; MATH-500 is the 500-problem subset of MATH commonly used in recent leaderboards. Dashes indicate
unreported numbers; self-reported single-shot accuracy except where noted. † M ATH A RENA pass@1 scores [180]. § Rows marked
this way are live leaderboard snapshots from LLM Stats, accessed May 10, 2026, and should be read as provisional self-reported
comparisons rather than controlled paper evaluations [181].


text and diagrams for geometry problem solving by maximiz-       where A measures affinity between the question text and literal
ing the agreement between the two modalities, a design choice    set L, and H measures coherence. G EOS could solve SAT
that anticipated subsequent multimodal fusion schemes. [189]     plane-geometry problems but was limited by its 186-problem
organized a SemEval shared task on math question answering;      dataset. G EOS ++ [190], [192] extended the formalism by
[190] examined the multimedia nature of geometry textbooks.      incorporating 293 axiomatic theorems as horn-clause rules.
   G EOS [191] was the first system to introduce a formal-       G EO S HADER [193] and G EOS -OS [194] contributed further
language description for geometry questions. It over-generates   datasets and models.
a set of relations, scores them, and chooses a subset maximiz-      I NTER GPS [5] introduced the large G EOMETRY 3K dataset
ing the combined text-and-diagram score, solving                 (3,002 problems with dense formal-language annotations) and
                                                                 combines rule-based text parsing with neural object detec-
        L∗ = argmax λ · A(L′ , t, d) + H(L′ , t, d) ,
                                                   
                                                           (4)   tion, a Transformer-based Theorem Predictor, and a Symbolic
  Selection signal        Artifact scored            Main advantage                                        Typical failure mode

  Majority vote           Final answer               Simple, model-agnostic selector; effective when       Correlated wrong traces can dominate the vote
                                                     correct traces form the plurality
  Agent consensus         Multiple agent responses   Exploits model, prompt, or role diversity across      Irrelevant or redundant agents add noise and cost
                                                     independent attempts
  ORM                     Completed solution         Cheap final-answer scoring; easy to pair with best-   Misses locally invalid steps that happen to end in
                                                     of-k sampling                                         a plausible answer
  PRM                     Intermediate steps         Localizes errors and supports targeted reranking or   Requires step-level human labels or reliable rollout-
                                                     reinforcement learning                                based annotations
  Execution               Program trace              Provides deterministic arithmetic, symbolic, or       The program may faithfully solve a misunderstood
                                                     unit-test checking                                    problem
  Lean kernel             Formal proof               Supplies kernel-level proof verification and          Formalization, premise retrieval, and proof search
                                                     reusable certificates                                 remain costly

TABLE XII: Common inference-time selection mechanisms for mathematical reasoning systems. The rows progress from weak
final-answer selectors to process-, execution-, and kernel-level checkers. Stronger checkers make generated traces more useful
for training and auditing, but they also require more structured interfaces and higher verification cost.


Geometry Problem Solver applying theorems to compute the                 MLLM baseline. The result is important because it demon-
final answer. It set the state of the art on G EOS, G EOS ++,            strates that geometry, unlike free-form MWP solving, already
and G EOMETRY 3K. N GS [35] introduced the G EO QA dataset               admits end-to-end verifiable reasoning without a full proof
of 5,010 problems with interpretable programs and multi-                 assistant: the symbolic engine serves as a lightweight kernel,
ple auxiliary tasks to enhance cross-modal representation.               and the neural component handles the perceptual and search-
G EOMETRY QA [195] re-annotated a geometry subset of                     planning tasks that symbolic systems do poorly alone.
M ATH 23K [106] with associated formulas.
                                                                         B. Neural Olympiad-Level Geometry
   The 2023–2026 plane-geometry literature sharpened the
                                                                           The most striking geometry result of the decade was A L -
lesson that diagram grounding, not just theorem search, is the
                                                                         PHAG EOMETRY [68], published in Nature in January 2024.
bottleneck. PGPSN ET [196] introduced PGPS9K, a 9,022-
                                                                         It is a neuro-symbolic system in which a symbolic deduction
problem dataset with fine-grained diagram annotations and
                                                                         engine (Deductive Database Arithmetic Reasoning, DDAR) is
interpretable solution programs, and converted diagrams into
                                                                         guided by a neural language model trained from scratch on 100
structural and semantic textual clauses for multimodal fusion.
                                                                         million synthesized theorems and proofs. On IMO-AG-30, a
G EO DRL [197] framed theorem application as a Markov
                                                                         benchmark of thirty IMO geometry problems from 2000–2022,
decision process over a geometry logic graph, using reinforce-
                                                                         A LPHAG EOMETRY solved 25, approaching the 25.9 average
ment learning while a symbolic system maintained deductive
                                                                         of human gold medalists, and substantially exceeding Wu’s
correctness. LANS [198] added layout-aware pretraining and
                                                                         method (10 problems). A LPHAG EOMETRY 2 [69], published
point-guided fusion, showing that geometric layout carries in-
                                                                         in early 2025, extended the domain language to handle move-
formation missed by image-level features alone. P I -GPS [199]
                                                                         ments of objects, locus-type theorems, and non-constructive
pushed this further by using an MLLM rectifier plus a geomet-
                                                                         problems, lifting coverage of IMO 2000–2024 geometry prob-
ric verifier to resolve underspecified points, shapes, and shaded
                                                                         lems from 66% to 88%, and solving 42 of 50 (exceeding
areas in the text before theorem prediction, achieving a nearly
                                                                         the average gold medalist). A LPHAG EOMETRY 2 was one
10% improvement over prior neural-symbolic approaches on
                                                                         component of the combined system that achieved silver-medal
G EOMETRY 3K. In parallel, FG EO -H YPER GN ET [67] inte-
                                                                         standard at IMO 2024 alongside A LPHA P ROOF [85]; the entire
grates the F ORMAL G EO symbolic system with a hypergraph
                                                                         pipeline relied on human-assisted translation of problems into
neural theorem predictor, making the predict–apply loop read-
                                                                         a domain-specific language.
able and traceable.
   AUTO GPS [66] synthesizes several of these threads into               C. Vision–Language Models for Math
a unified neuro-symbolic framework that produces verifiable                 A parallel trajectory emerged from the vision–language
stepwise proofs. Its Multimodal Problem Formalizer (MPF)                 community. M ATH V ISTA [70] introduced a 6,141-example
uses neural cross-modal comprehension to translate diagram–              benchmark drawn from 31 source datasets, spanning figure
text pairs into structured formal representations, and a De-             QA, geometry problem solving, MWPs with visuals, textbook
ductive Symbolic Reasoner (DSR) expands a hypergraph                     QA, and visual QA, and covering algebraic, arithmetic, geo-
of derivations to produce minimal, human-readable solution               metric, logical, numeric, scientific, and statistical reasoning.
steps. A feedback loop between the MPF and DSR corrects                  On M ATH V ISTA testmini, GPT-4V reached 49.9%, signif-
formalization errors during derivation, and the symbolic engine          icantly above Bard (34.8%) but 10.4 points below human
guarantees that each step is logically sound. On PGPS9K                  average.
completion tasks, AUTO GPS improves over prior SOTA by                      M ATH V ERSE [71] specialized further into plane geometry,
9.2%, and human evaluators judge 99% of its derivation steps             solid geometry, and functions (2,612 problems across six
logically correct, compared to 71% for the best-performing               variant versions totalling 15K test samples) and introduced
a step-wise CoT evaluation protocol. A key finding was that                VI. F ORMAL M ATHEMATICAL R EASONING
several MLLMs achieved higher accuracy when visual input
                                                                      Systems discussed in this section correspond to the “Formal
was removed, indicating that they relied primarily on textual
                                                                   Provers” band in Figure 5. A fundamental limitation of the in-
features. MATH-V ISION [72] collected 3,040 problems from
                                                                   formal reasoning systems discussed so far is that their outputs,
real math competitions across 16 disciplines and five difficulty
                                                                   however fluent, carry no guarantee of correctness. Sections IV
levels. MV-MATH extends these benchmarks to multi-visual
                                                                   and V documented a recurring pattern: each advance in
contexts, with leading models (Claude 3.5 Sonnet) reaching
                                                                   generation quality, longer chains of thought, tool-augmented
only 33.9% compared to 76.5% for humans.
                                                                   programs, multi-agent debate, vision-language interleaving,
   On the model side, G-LL AVA [36] bootstrapped a geometry        solved progressively harder problems while simultaneously
corpus (Geo170K) for vision-language fine-tuning, achieving        revealing new failure modes that no amount of sampling
strong performance on GPS tasks. M ATH -LL AVA introduces          or voting could reliably eliminate. Arithmetic hallucinations
the MathV360K dataset; MAVIS [73] further optimizes math-          survive self-consistency; logically invalid steps survive PRM
specific visual encoding and provides auto-generated CoT           scoring when the PRM itself lacks domain coverage; and
rationales. Reasoning-enabled multimodal models such as O 3        multimodal models sometimes achieve higher accuracy when
and Gemini Deep Think further integrate visual reasoning with      the diagram is removed, indicating that the visual modality
image manipulation tools, retaining the raw image throughout       introduces as many failure modes as it resolves. These observa-
the reasoning trace and zooming or rotating as needed.             tions converge on a single insight: for mathematical claims that
   The related-work map in MINT-C OT [74] clarifies a newer        must be trusted, theorem statements, verified conjectures, com-
split inside multimodal mathematical reasoning. One branch         petition proofs, an external mechanical guarantee is needed,
adapts text-only visual reasoning methods, such as R1-V-           one that does not depend on the same learned distribution that
style long rationales, to images; another explicitly inserts       generated the claim. This has motivated a parallel research
visual material into the rationale through crops, highlighted      agenda centered on formal proof assistants, most prominently
regions, or external sketching tools, as in Visual CoT, Chain-     Lean 4 [6], [201], that mechanically verify each inference
of-Spot, Chain-of-Image, Visual SKETCHPAD, and ICoT.               step. Working mathematicians increasingly regard this formal
MINT-C OT argues that these mechanisms are often too coarse        track as the essential complement to LLM-based informal
for diagrams because mathematical evidence may be a line           reasoning [26]–[28], [30].
segment, an angle, a label, or a non-rectangular configuration.
Its central device is an Interleave Token: before each reasoning   A. From Computer-Assisted to Machine-Assisted Proof
step, the model selects fine-grained visual tokens from the           Tao’s 2024 account of machine-assisted proof usefully sit-
original image and reasons over those tokens together with         uates modern LLM provers within a much older tradition of
text. The accompanying 54K-example dataset is built from           mathematical computation [202]. Long before proof assistants,
Mulberry-260K by pairing reasoning steps with grid-indexed         mathematicians used computation to generate data, test con-
visual regions using OCR and GPT-4o-assisted keyword align-        jectures, carry out symbolic manipulation, and certify large
ment, and the resulting 7B model is trained through text-          finite searches. Contemporary examples include SAT/SMT
only CoT SFT, interleaved-CoT SFT, and interleaved-CoT             solvers that emit proof certificates, rigorous numerical methods
RL. On the reported math-focused evaluations, it reaches           such as interval arithmetic, and computer algebra systems that
73.70 on M ATH V ISTA -M ATH, 64.72 on G EO QA, and 69.60          perform symbolic reductions under human supervision. The
on MMS TAR -M ATH; the ablation shows that text-only CoT           point is not merely historical: machine-assisted proof is best
SFT supplies much of the initial lift, while token-level visual    understood as a spectrum from heuristic exploration to kernel-
interleaving and RL add further gains. The larger lesson is        checked certification, with different trust assumptions at each
conceptual: visual math systems are beginning to expose not        level.
only whether a model uses a diagram, but which parts of the           This genealogy also clarifies why formal proof assistants
diagram each reasoning step depends on.                            have become central. Earlier computer-assisted proofs, such
   An especially recent trend imports test-time scaling into       as the four-color theorem and the Kepler conjecture, depended
geometry. MARS-GPS [200], a 2026 preprint, generates mul-          on substantial custom computation; later formalization projects
tiple parallel reasoning rollouts, checks numerical subclaims      reduced the trusted surface by rebuilding the argument inside a
with Python, ranks candidates using token-level entropy, and       proof assistant. Tao highlights several scale markers: the four-
aggregates them through voting and self-verification. It reports   color theorem was formalized in Coq; the Flyspeck verification
88.8% accuracy on G EOMETRY 3K with eight rollouts and             of Kepler’s conjecture required an eleven-year collaboration;
77.48% on PGPS9K. The result should be read cautiously             Scholze’s liquid tensor experiment took about eighteen months
until peer review, but it is conceptually important: geomet-       in Lean; and Tao’s own polynomial Freiman–Ruzsa formaliza-
ric problem solving is beginning to resemble the broader           tion converted a 33-page human proof into Lean in roughly
reasoning-model paradigm in which a strong generator is            three weeks with about twenty collaborators. These cases show
valuable mainly when coupled to systematic search and veri-        that formalization is not just post hoc checking. It uncovers
fication.                                                          hidden assumptions, creates reusable library material, and
makes unusually large mathematical collaborations possible          duces a 121K-example dataset of IMO-level informal theorems
because subtasks can be specified and independently verified.       with step-by-step proofs generated by o3-mini, annotated for
                                                                    correctness, difficulty (levels 5–10), and topic domain, and
B. Tactic Prediction and Neural Theorem Proving                     rigorously decontaminated against 18 standard benchmarks.
   Early neural theorem provers treated proving as a tactic-        Its key methodological contribution is an RL-Zero training
prediction problem: given the current proof state, predict the      protocol for informal proving: each theorem is expanded
next tactic to apply. GPT-f [75] demonstrated that a GPT-style      into logically entailing and contradictory variants, enabling a
model trained on Metamath proofs could recover non-trivial          binary reward signal (proved vs. disproved) that is verifiable
proofs via expert iteration. L EAN D OJO [14] released a large-     without a proof assistant. A 7B model trained with GRPO
scale Lean environment with premise retrieval via R E P ROVER,      on these variants outperforms substantially larger systems,
enabling retrieval-augmented tactic prediction over mathlib.        including DeepSeek-R1-Distill-70B, QwQ-32B, and Qwen2.5-
L EAN C OPILOT [76] integrates LLM-based tactic suggestion          Math-72B-Instruct, on the FIMO, HMMT, and PutnamBench
directly into the Lean 4 editor, operating as an inline co-pilot    informal-proving benchmarks, reaching an average outcome
for human mathematicians.                                           accuracy of 47.2% versus 21.5% for R1-Distill-70B. The
   The literature reviewed around A LPHA P ROOF suggests a          accompanying process evaluation framework scores generated
useful subdivision of modern provers. Search-first systems          proofs on logical validity (40%), completeness (30%), correct-
such as GPT-f and H YPERT REE P ROOF S EARCH [75], [87]             ness (20%), and clarity (10%), providing a richer signal than
pair a proof-state model with tree or hyper-tree search, often      binary outcome accuracy alone.
learning from failed proof attempts through expert iteration           The DeepTheorem result is important for three reasons.
or online training. Retrieval-centered systems such as L E -        First, it demonstrates that RL-Zero can be extended from
AN D OJO/R E P ROVER make premise selection an explicit part        closed-form QA to open-ended proof generation by construct-
of tactic prediction [14]. Whole-proof systems such as BAL -        ing verifiable theorem variants, addressing the reward-design
DUR [78] instead ask a model to emit a full Isabelle/HOL proof      bottleneck that has limited RLVR to answer-graded tasks.
script and then use proof-assistant errors for repair. The newest   Second, its process evaluation framework offers a concrete
high-performing systems blur these categories: DSP uses             operationalization of the “reasoning quality vs. answer ac-
informal sketches to guide formal proof search [10], L EAN -        curacy” distinction that recent surveys have called for but
STA R and K IMINA -P ROVER interleave natural-language rea-         not resolved [22], [23]. Third, by showing that a 7B model
soning with Lean proof generation [80], [86], and D EEP S EEK -     can match or exceed 70B-class reasoning models on informal
P ROVER -V2 and A LPHA P ROOF combine decomposition, ver-           proving, it reinforces the finding from the broader reasoning-
ification feedback, and reinforcement learning at scale [79],       model literature that data quality and training protocol often
[85].                                                               matter more than raw parameter count.
   A key efficiency innovation is APOLLO (Automated Proof
repair via LLM and Lean cOllaboration) [77], which treats           C. Autoformalization
the Lean 4 compiler not as a binary pass/fail oracle but as            Autoformalization, translating natural-language mathemat-
a diagnostic tool. When an LLM-generated proof attempt              ics into formal statements, was shown to be feasible via
fails, APOLLO’s agentic pipeline analyzes the compiler’s            few-shot prompting of Codex by [9]. DSP (Draft, Sketch,
error messages to fix syntax issues, isolates failing sub-          Prove) [10] interleaves informal and formal reasoning, having
lemmas, and recursively invokes the LLM on each remaining           the model first produce an informal proof sketch, autofor-
subgoal with a minimal sampling budget. The repaired sub-           malize it into Isabelle, and discharge the remaining subgoals
proofs are recombined and re-verified, and the process repeats      via a hammer. P ROOF N ET [204] provided 371 paired in-
for multiple attempts. This compiler-guided repair loop re-         formal/formal statements from undergraduate textbooks. The
duces the sampling budget by orders of magnitude compared           L EAN W ORKBOOK [81] formalized hundreds of thousands
to brute-force generation: for Goedel-Prover-SFT, APOLLO            of natural-language math competition problems into Lean 4
raises MiniF2F accuracy to 65.6% while reducing the required        statements. Type-checking-based filtering [205] has become
samples from ∼25,600 to a few hundred, and it enables               standard: autoformalized statements that fail to type-check are
general-purpose models such as o3-mini to jump from single-         rejected, and iterative refinement substantially improves yield.
digit accuracy (3–7%) to over 40% on formal proofs. Among              A more recent line of work uses the Lean 4 compiler not just
models with 8B parameters or fewer, it establishes a state-         as a binary type-checker but as a source of process-level super-
of-the-art MiniF2F accuracy of 84.9%. The broader lesson is         vision for autoformalization training. The FORML4 dataset
that structured repair, using the proof assistant’s feedback to     and PDA (Process-Driven Autoformalization) framework [82]
guide targeted fixes rather than regenerating entire proofs, is a   pair natural-language theorems and proofs with their Lean 4
scalable paradigm that complements both expert iteration and        formalizations, then train a Process-Supervised Verifier (PSV)
whole-proof generation.                                             on the compiler’s fine-grained error messages, including error
   A complementary line of work asks whether LLMs can               locations, type mismatches, and unresolved goals. The PSV
prove theorems without formal proof assistants, operating en-       provides step-level feedback to the autoformalization model
tirely in natural-language LATEX. D EEP T HEOREM [203] intro-       during fine-tuning, creating an iterative loop: the autoformal-
izer generates a candidate, the compiler diagnoses specific         problems, and a specialist prover is trained around the target
failures, and the PSV guides the next training round toward         instance before final search.
higher compiler acceptance rates with less filtered data. This         During IMO 2024, with the five non-geometry problems
process-driven approach parallels the PRM/ORM distinction in        manually translated into Lean by experts, A LPHA P ROOF
informal reasoning (§IV-H): outcome-level feedback (“does it        solved P1, P2, and P6; P6 was the hardest problem of
type-check?”) is cheap but coarse, while process-level feed-        the competition and was fully solved by only five of 609
back (“which step fails and why?”) enables more targeted            human contestants. A LPHAG EOMETRY 2 solved the geometry
learning. Together with APOLLO’s compiler-guided repair,            problem P4, so the combined system scored 28/42 points,
PDA illustrates a broader trend in which the proof assistant’s      equivalent to a silver medalist. This result is methodologically
feedback channel, long treated as a binary gate, is being           important but should be interpreted carefully: the competition
elevated to a rich supervision signal.                              pipeline used expert formalization, answer-guessing assistance
                                                                    for “find all” problems, and 2–3 days of TTRL for the
D. Large-Scale LLM-Based Provers                                    solved non-geometry problems. At IMO 2025, an advanced
   The D EEP S EEK -P ROVER series illustrates the rapid matura-    version of Gemini Deep Think [179], operating end-to-end in
tion of this area. D EEP S EEK -P ROVER [37] synthesized 8 mil-     natural language within the 4.5-hour time limit, achieved the
lion Lean 4 statement–proof pairs by (i) autoformalizing 870K       gold-medal threshold (35/42, five problems solved perfectly),
natural-language competition problems using DeepSeekMath-           closing the formal-vs-informal gap that had characterized the
7B; (ii) filtering low-quality statements with chain-of-thought     2024 result.
scoring and negation-based hypothesis rejection; and (iii)
iteratively expert-iterating the model on successful proofs. This   F. Ecosystem, Libraries, and Human Workflow
established that expert iteration with high-quality synthetic
data could substantially improve theorem-proving ability in            Formal mathematical reasoning is as much an infrastruc-
Lean.                                                               ture problem as a modeling problem. Proof assistants are
   D EEP S EEK -P ROVER -V1.5 [206] added RLHF using proof-         useful because they reduce correctness to kernel checking,
assistant feedback and integrated Monte Carlo Tree Search to        but the cost of reaching the kernel is paid through library
guide tactic selection. D EEP S EEK -P ROVER -V2 [79], released     coverage, notation alignment, premise retrieval, and proof-
in April 2025, took a recursive decomposition approach:             state interaction. Lean 4 has become especially influential
DeepSeek-V3 produces a natural-language proof sketch to-            because mathlib supplies a rapidly expanding shared cor-
gether with a Lean template containing sorry placeholders,          pus and because the surrounding tool ecosystem increasingly
and a 7B prover recursively solves each subgoal; the resulting      resembles modern software development: editor integration,
verified proofs serve as training data for a 671B RL-fine-tuned     continuous integration, search tools, package management, and
CoT prover. On M INI F2F- TEST [207], D EEP S EEK -P ROVER -        proof suggestions.
V2-671B reaches 88.9% pass rate at Pass@8192, solves 49                Tao frames the central practical barrier as the de Bruijn
of 658 PutnamBench problems, and correctly proves 6 of              factor: the ratio between the effort required to write a correct
15 AIME problems in ProverBench. Complementary systems              formal proof and the effort required to write a correct informal
include L EAN -STA R [86], which interleaves natural-language       proof [202]. His estimate of this ratio is still well above one,
thoughts with tactic choices trained via STaR [50], and             but falling as proof assistants, libraries, tactics, SMT solvers,
community projects such as Goedel-Prover, Kimina-Prover,            and LLM-based copilots become better integrated. This is an
and Harmonic’s A RISTOTLE which have pushed the frontier            important lens for AI-for-mathematics: the decisive threshold
further.                                                            is not whether a model can occasionally solve an isolated
                                                                    Lean benchmark, but whether the combined human–AI–proof-
E. AlphaProof and IMO 2024                                          assistant workflow makes formalization cheaper than informal
   The landmark result of the formal track in 2024 was              proof maintenance, error checking, and referee labor.
A LPHA P ROOF [85], a reinforcement-learning system trained            This matters for survey-level comparison because a
in a Lean 4 environment using an AlphaZero-inspired algo-           theorem-proving benchmark does not only measure the model.
rithm. Its proof network is a 3B-parameter encoder–decoder          It also measures whether the relevant definitions already exist
transformer that predicts both a tactic policy and a value          in the library, whether the theorem is stated with the same
estimate for the current proof state; search is organized as an     conventions as mathlib, whether useful lemmas can be
AND–OR proof tree so that decomposed subgoals must all be           retrieved, and whether the model receives proof-state feedback.
solved. Training begins with broad code/math pretraining and        A problem that is easy for a human mathematician may
Mathlib state–tactic supervision, but the central phase is RL       be difficult for Lean if the background theory has not been
over roughly 80 million Lean statements produced from about         formalized, while a problem that looks advanced may become
one million natural-language problems by an autoformaliza-          easy once an existing library theorem exactly matches it. For
tion system. For the hardest targets, A LPHA P ROOF uses test-      this reason, future evaluations should report library version,
time reinforcement learning (TTRL): a Gemini-based variant          allowed imports, premise-retrieval access, search budget, and
generator creates a large local curriculum of related Lean          whether any human formalization assistance was used.
System                             Params Approach                                            Pass@N        MiniF2F-test PutnamBench Formal-IMO
Search-first tactic prediction
GPT-f [75]                         774M     Expert iteration over Metamath                    @8              36.6%          –           –
HyperTree Proof Search [87]        600M     Online hyper-tree proof search                    @64             41.0%          –           –
Retrieval-augmented proving
LeanDojo ReProver [14]             300M     Retrieval-augmented tactic prediction             –               48.4%          –           –
InternLM2-Math-Plus [164]          7B       Open math LLM, verifiable reasoning               @32             43.4%          –           –
Thought-interleaved and whole-proof generation
Lean-STaR [86]                     7B       NL thoughts interleaved with tactics              @64             46.3%          –           –
Goedel-Prover V1 [208]             7B       Iterative SFT on autoformalized proofs            @32             57.6%        7/658         –
Expert iteration + RL provers
DeepSeek-Prover V1 [37]            7B       Synthetic Lean data + expert iteration            @65536           50.0%          –          –
DeepSeek-Prover V1.5 [206]         7B       RLHF + MCTS over proof-assistant feedback         RMaxTS           63.5%          –          –
Kimina-Prover Preview [80]         72B      Large-scale RL + formal reasoning traces          @32              80.7%       1.6%⋆         –
DeepSeek-Prover V2 (7B) [79]       7B       Recursive subgoal decomposition                   @8192            82.0%       23/658        –
Goedel-Prover V2 [209]             8B       Scaffolded synthesis + self-correction            @32              84.6%          –          –
Goedel-Prover V2 [209]             32B      Scaffolded synthesis + self-correction            @32             90.4%‡      86/658‡        –
DeepSeek-Prover V2 [79]            671B     Large CoT prover from verified subproofs          @8192            88.9%       49/658        –
Compiler-guided repair
APOLLO+Goedel-Prover-SFT [77] –             Lean compiler diagnostics for proof repair        few hundred     65.6%          –           –
APOLLO (best ≤8B) [77]             ≤8B      Recursive subgoal repair with compiler feedback   –               84.9%          –           –
Neuro-symbolic RL + formal search
AlphaProof + TTRL† [85]            3B       AlphaZero-style Lean RL, AND–OR proof tree        TTRL            99.6%†      56.1%†      58.3%†

TABLE XIII: Performance of representative neural theorem provers on formal benchmarks, grouped by approach. Pass@N
reports the search budget: “@k” = k samples, RMaxTS = reward-MaxTS, TTRL = test-time RL, and “–” = unreported.
PutnamBench entries are full-benchmark counts unless ⋆ marks PutnamBench-test percentage; ‡ denotes two rounds of compiler-
guided self-correction. † AlphaProof uses expert Lean formalizations and large TTRL budgets, so it is not directly comparable
with fully automatic systems. The table shows rapid open-prover catch-up alongside a still distinct expert-assisted TTRL regime.


   An emerging direction addresses the library-coverage bot-                A. Program Search: F UN S EARCH and A LPHA E VOLVE
tleneck directly: rather than waiting for human contributors
to formalize missing intermediate results, LLMs can proac-                     F UN S EARCH [7] introduced the paradigm of evolutionary
tively generate them. M ATHLIB L EMMA [83] employs a multi-                 program search guided by an LLM, in which a pre-trained
agent architecture, Discovery, Judge, and Formalizer agents, to             code LLM proposes variations of a Python function and an
identify “folklore lemmas”: mathematical facts widely known                 automated evaluator selects the highest-scoring programs. In
to practitioners but absent from mathlib. The system uses                   Nature 2024, the authors demonstrated its application to the
mathlib entries as seeds, proposes candidate lemmas, fil-                   cap-set problem in additive combinatorics (producing new
ters them for mathematical soundness, and generates type-                   lower bounds for cap-set sizes in several dimensions) and to
checked Lean 4 code. The accompanying benchmark com-                        online bin packing (discovering novel heuristics).
prises 4,028 type-checked Lean 4 statements, and an LLM-                       A LPHA E VOLVE [8], released in 2025, generalized F UN -
assisted human audit finds 78% mathematically sound. A                      S EARCH by evolving entire programs (hundreds of lines)
subset of the generated lemmas has been merged into the                     rather than single functions, combining Gemini Flash (breadth)
official mathlib repository, demonstrating that LLMs can                    with Gemini Pro (depth), and using richer natural-language
transition from passive consumers to active contributors of                 feedback. Its most publicized result was the discovery of an
formal library material. This is a concrete step toward reducing            algorithm for multiplying two 4 × 4 complex-valued matrices
the de Bruijn factor: if the “connective tissue” of routine                 using 48 scalar multiplications, the first improvement over
lemmas can be automatically generated and verified, human                   Strassen’s 1969 algorithm for complex matrices. The larger
mathematicians can focus on the creative steps.                             arXiv study by Georgiev, Gómez-Serrano, Tao, and Wag-
                                                                            ner [210] evaluates this paradigm on 67 problems spanning
                                                                            analysis, combinatorics, geometry, and number theory. A L -
VII. M ATHEMATICAL D ISCOVERY AND O PEN P ROBLEMS                           PHA E VOLVE rediscovered best-known solutions in most cases
                                                                            and improved them in about 20%, including the finite-field
   Systems discussed in this section correspond to the “Dis-                Kakeya problem, the kissing-number problem in 11 dimen-
covery Systems” band in Figure 5. A third and arguably most                 sions (593-sphere construction), and the Nikodym problem. In
consequential axis concerns the use of LLMs to produce new                  some cases it also extrapolated finite computational evidence
mathematical knowledge, improved bounds, explicit construc-                 into formulas valid for all input sizes, making the system
tions, counterexamples to conjectures, and, in the limit, novel             closer to a conjecture-and-construction engine than a mere
proofs of open problems.                                                    optimizer. The study further combines A LPHA E VOLVE with
Gemini Deep Think for proof generation and A LPHA P ROOF            System            Target problem        Primary verifier        Novelty guarantee
                                                                                      class                 type
for formal verification in Lean, illustrating a broader pipeline
from search over constructions to machine-assisted proof.           F UN S EARCH      Combinatorial         Python execution        Exceeds best known
                                                                                      optimization (e.g.,   (fitness evaluation)    numerical bounds
                                                                                      cap sets, bin
B. Erdős Problems and the AI-Assisted Attack Surface                                 packing)
                                                                    A LPHA E VOLVE    Open-ended            Distributed sandbox     Exceeds known
   Paul Erdős (1913–1996) left behind over a thousand con-                           algorithmic           execution               bounds; generalizes
                                                                                      discovery                                     to full programs
jectures; the erdosproblems.com database [88] currently cata-       Erdős Workflow   Open mathematical     Lean 4 kernel           Resolves unproved
logs 1,133 of them, of which roughly 680 remained open as of                          conjectures           (formal verification)   conjecture listed in
                                                                                                                                    database
early 2026. Beginning in late 2025 and accelerating through
early 2026, a succession of these problems has been solved          TABLE XIV: Comparison of recent mathematical discovery
with non-trivial AI contribution [89].                              systems across their target problem classes, verification mech-
   An early claim from OpenAI in October 2025 that GPT-             anisms, and the standards used to guarantee that a discovery
5 had autonomously solved ten Erdős problems was quickly           is genuinely novel.
rebutted by T. Bloom, who pointed out that these were in
fact literature lookups: the system had located existing papers
that the database curator was unaware of. The subsequent            whereas proof assistants, symbolic solvers, and rigorous com-
bona fide solves reflect a much more rigorous division of           putation are strong at rejecting invalid outputs [202].
labor. In December 2025, Erdős problem #1026 was solved:              This workflow paradigm is most visible in evolutionary
the A RISTOTLE system [211] (operated by B. Alexeev) gen-           program search. F UN S EARCH [7] pioneered the approach by
erated the proof sketch and autonomously formalized it in           using an LLM to mutate a single target function (e.g., a priority
Lean 4 with minimal human steering. Between January and             function for bin packing), evaluating the new function’s fitness,
March 2026, problems #728, #729, and #397 were solved               and feeding successful mutations back into a prompt pool.
using a collaborative pipeline: GPT-5.2 Pro generated the           However, this single-function restriction limits the complexity
informal proof strategies, the A RISTOTLE system was used           of the algorithms it can discover. A LPHA E VOLVE [8] extends
to formalize the resulting arguments into Lean, and human           this by implementing whole-program evolution: the LLM
experts orchestrated the translation and lemma decomposition.       mutates not just one function, but an entire multi-file Python
Across all four cases, T. Tao independently verified the proofs     repository representing an arbitrary computational workflow,
and documented them as legitimate examples of AI-assisted           allowing it to invent new data structures, helper functions,
mathematics rather than literature search. As of April 2026, 22     and optimization loops simultaneously. This architectural shift
of 279 proved Erdős problems carry formal Lean verification.       enables A LPHA E VOLVE to attack a broader class of problems,
Tao himself [29] stresses that these solves involve “lowest         as summarized in Table XIV.
hanging fruit”, problems amenable to standard techniques
                                                                       The AlphaEvolve-scale study makes the same point op-
once the right retrieval and connection is made, but notes
                                                                    erationally: evolutionary program search proposes construc-
the qualitative shift: “compression matters”, and problems that
                                                                    tions, Deep Think supplies mathematical argumentation, and
might have taken hours or days of expert effort now fall in
                                                                    AlphaProof or Lean supplies the final correctness filter [210].
minutes.
                                                                    The current bottleneck is no longer any single capability in
   A separate episode of genuine human–AI collaboration             isolation but rather the interfaces between them, a theme we
is documented in Tao’s March 2026 paper Local Bernstein             return to in Section XI.
theory, and lower bounds for Lebesgue constants, where one
                                                                       A fourth, distinct mode emerged with the AI co-
inequality was first suggested numerically by A LPHA E VOLVE,
                                                                    mathematician [159] in May 2026: an asynchronous, stateful
then proved by ChatGPT via a duality argument drawing on
                                                                    workbench in which a mathematician orchestrates a hierar-
approximation theory, which Tao verified and formalized in
                                                                    chy of agents (project coordinator, workstream coordinators,
Lean, with the resulting 1,125-line Lean proof accepted into
                                                                    specialised sub-agents for literature retrieval, code execution,
his repository. The episode illustrates the emerging modus
                                                                    and proof drafting via Gemini Deep Think, and reviewer
operandi: AI as a cross-domain search-and-connection engine,
                                                                    agents) under continuous human steering rather than au-
coupled with formal verification to guarantee correctness.
                                                                    tonomous end-to-end execution. The system reports 48% on
                                                                    F RONTIER M ATH Tier 4, the hardest, research-grade tier [212],
C. Discovery as a Workflow
                                                                    and is credited with non-trivial contributions to three open
   What is striking about the 2025–2026 discovery work is           problems: Kourovka 21.10 on just-finite group presentations
that it consistently instantiates a workflow, not a single model,   (Lackenby), two log-concavity conjectures on Stirling coef-
combining four specialized capabilities: (i) neural search or       ficients (Bérczi), and a perturbation lemma in Hamiltonian
proposal, (ii) informal proof drafting, (iii) autoformalization     systems (Rezchikov). The co-mathematician thus comple-
into Lean, and (iv) formal verification. Tao’s machine-assisted-    ments the program-search (F UN S EARCH, A LPHA E VOLVE)
proof framing explains why this architecture is plausible:          and autoformalisation-pipeline (Erdős workflow, A RISTOTLE)
LLMs are strong at generating candidate directions and code,        modes already discussed: rather than chasing fixed bench-
marks, it targets the exploratory, iterative reality of mathe-     MA1 into 831 problems with near-duplicate removal, along
matical research itself. A parallel “autonomous mathematics        with the subset P ERTURB in which quantity perturbations are
research” agent, A LETHEIA [213], was released in Febru-           introduced.
ary 2026 with similar ambitions but a different orchestration         Algebra datasets were constructed to evaluate parameter-
strategy; the convergence of two industrial labs on this work-     ized templates. A LG 514 [40] contains 514 algebra problems
bench paradigm within three months suggests it is becoming         crawled from algebra.com. D OLPHIN 1878 [111] is a
the default deployment mode for research-assistance mathe-         number-word-problem corpus with 1,878 problems and 1,183
matics.                                                            equation templates. D RAW 1K [236] contains 1,000 algebra
                                                                   problems with a 774/226 train/test split. D OLPHIN 18K [115]
    VIII. DATASET R EPOSITORY AND P ERFORMANCE                     is a large-scale dataset of 18,460 problems with 5,871 tem-
                      A NALYSIS                                    plates. AQ UA [216] provides 100,949 algebraic problems with
   Understanding the arc of progress requires a panoramic view     rationales, the first corpus large enough for end-to-end neural
of the datasets on which progress is measured. We preserve the     training. M ATH QA [237] augments a subset of AQuA with
comprehensive catalog of MWP and geometry datasets from            structured formal representations.
the earlier literature and extend it with the new benchmarks          Multi-operator benchmarks include H MWP [146], with
that have defined the 2023–2026 period.                            5,491 problems covering linear, nonlinear, and simultane-
                                                                   ous equations; C M 17K [146] with 17,659 problems across
A. Training, Benchmark, and Augmentation Corpora
                                                                   arithmetic, linear-system, non-linear-system, and equation-
   Recent surveys emphasize that the dataset ecosystem should      set subsets; M AWPS [214] unifying six earlier datasets into
not be viewed only as a list of test benchmarks [22], [23].        3,320 problems; A SDIV [215] with 2,305 problems across 25
Mathematical datasets now play at least four distinct roles:       problem types for measuring lexical and syntactic diversity;
they supply pretraining text, provide supervised reasoning         and S VAMP [12], a 1,000-problem stress test in which minor
traces, evaluate models, and create augmented feedback for         variations of M AWPS problems (question reordering, adding an
verifiers or self-improvement. This distinction is important be-   irrelevant quantity, swapping object names) dramatically drop
cause benchmark saturation can coexist with genuine progress       the accuracy of previously state-of-the-art systems, revealing
in training data, and conversely a larger training corpus does     their reliance on spurious surface cues.
not guarantee robustness on fresh evaluations.                        PARA MAWPS [218], [238] extends this robustness line in a
   We return to the cross-cutting design principles implied by     complementary direction. Instead of only applying controlled
this functional view in Section IX.                                template perturbations, it augments selected M AWPS problems
   The practical lesson is that future papers should report not    with paraphrased, adversarial, and inverse variants, then eval-
only benchmark scores but also the data path that produced         uates whether solvers preserve the underlying equation under
them: whether the model was math-pretrained, whether CoT           linguistic change. This makes it especially useful for sepa-
or program traces were used for SFT, whether synthetic data        rating true mathematical invariance from memorized surface-
came from a stronger model, whether formal data were type-         to-equation mappings. The accompanying voting framework
checked, and whether augmented data encode wrong steps             also anticipates the later LLM-era pattern of solving multiple
as well as correct ones. These details determine whether           transformed versions of the same problem and aggregating the
a reported gain reflects better mathematical comprehension,        answer.
better generation style, stronger verification, or simply closer      Large-scale Chinese MWP datasets have played a central
overlap with the evaluation distribution.                          role. M ATH 23K [41] crawled 60,000 problems from Chinese
   Tables XVI and XVII condense the long catalog into              K-12 websites and retained 23,161 for which templates could
two survey-level maps. They are intentionally organized by         be automatically extracted; it became the central benchmark
function rather than chronology: the most useful question for      for Chinese MWP research. A PE 210K [217] contains 210,488
a reader is often not “which benchmark is newest?” but “what       problems with 56,532 templates, spanning both elementary
failure mode or modeling choice does this resource expose?”        and middle-school levels. D OLPHINS [111] (a small English
                                                                   subset, 7K problems) and derivatives complete the picture.
B. Math Word Problem Datasets
                                                                      The watershed G SM 8K benchmark [93] comprises 8,500
   Early MWP corpora are small and topic-restricted.               high-quality, linguistically diverse grade-school problems re-
A I 2 [39] contains 395 addition-and-subtraction problems          quiring 2 to 8 reasoning steps. Its unique role stems from
crawled from math-aids.com and ixl.com, divided                    the explicit chain-of-thought annotations, which enabled the
into three subsets: mixed problems (M AR, 196 prob-                supervised verifier training that would later seed the entire
lems), irrelevant-information problems (I R, 121), and multi-      reasoning-model paradigm.
step problems (M S, 78). I L [96] contains 562 single-
operator problems from k5learning.com (I L -A DDSUB,
                                                                   C. Multilingual and Non-English Math Benchmarks
395) and dadsworksheets.com (I L -M ULDIV, 167). S IN -
GLE EQ [103] consists of 508 grade-school problems with one          The English-centric view of mathematical reasoning is
unknown. A LL A RITH [105] unifies A I 2, I L, S INGLE EQ, and     increasingly inadequate. Classical MWP solvers often failed
                                      reward / fitness                                    type / proof errors                                     counterexamples



               Neural proposer                                Informal reasoning                                    Formalization                                     Verification
     LLM · F UN S EARCH · A LPHA E VOLVE                 proof sketch · program · construction           Lean statement · tactics · proof terms            execution · expert audit · Lean kernel



     Erdős #729 walkthrough (Feb – Mar 2026)                    natural-language draft                         Aristotle: Lean 4 tactic script                        kernel verdict

          GPT-5.2 Pro proposes a                              Proof skeleton, 3 lemmas:                         theorem erdos_729 :                            ✓ mathlib kernel checks
          proof strategy: induction on                          L1: base case n ≤ 5                               ∀ n, P n := by                                type-check OK
          n with a 4-case partition                             L2: inductive step                                  induction n                                 unsolved goals: 0
          and a slice-rank bound.                               L3: union over cases                                apply Cauchy...                             Human verified


Fig. 13: The verified-discovery pipeline. Top row: four abstract stages, neural proposer (cyan), informal reasoning (yellow),
formalization (pink), and verification (purple), each with its representative artifacts. Bottom row: a concrete instantiation by the
GPT-5.2 Pro + A RISTOTLE team that produced a Lean-checked proof of Erdős problem #729 in early 2026, with one panel per
stage showing the actual artifact it produced. The dashed orange feedback loop carries three signal types — counterexamples,
type / proof errors, and reward / fitness — back to the proposer, closing the iterative search.

Dataset role                    Representative resources (with scale)                                            Typical artifact                           Primary function

 Training-side resources
 Math pretraining               AMPS (23B tok), P ROOF P ILE 2 (55B tok), O PEN W EB M ATH                       Raw arXiv, textbooks, web math,            Notation fluency, theorem familiarity;
                                (14.7B tok), M ATH P ILE (9.5B tok), AUTO M ATH T EXT (200B+                     code                                       powers M INERVA, L LEMMA,
                                tok), A LGEBRAIC S TACK                                                                                                     D EEP S EEK M ATH
 SFT / instruction              M ETA M ATH QA (395K), M ATH I NSTRUCT (260K), N UMINA M ATH                     CoT, PoT, tactic traces                    Solution format, tool use, competition
                                (860K+), O PEN M ATH I NSTRUCT-2 (14M), L EAN W ORKBOOK                                                                     patterns; formal subsets enable Lean
                                (57K, formal)                                                                                                               SFT
 Augmented / verifier           PRM800K (800K step labels), M ATH -S HEPHERD (MC rollouts),                      Step labels, programs, informal /          Train PRMs, program generators,
                                O MEGA PRM (1.5M+ labels), M ATH QA-P YTHON (23.9K), L ILA                       formal alignments                          autoformalizers, self-improvement
                                (134K), NATURAL P ROOFS -G EN (14.5K)                                                                                       loops
 Evaluation-side resources
 Evaluation                     GSM8K (8.8K), MATH (12.5K), O LYMPIAD B ENCH (8.5K),                             Answers, diagrams, formal                  Grade-school through research-level
                                M ATH V ISTA (6.1K), M INI F2F (488), P UTNAM B ENCH (658),                      statements, private checks                 generalization; live benchmarks resist
                                F RONTIER M ATH (∼350), M ATH A RENA (149+, live)                                                                           contamination
 Multilingual                   M ATH 23K (23K, ZH), A PE 210K (210K, ZH), MGSM (2.5K, 10                        Native or parallel problems;               Language shift, morphology, script,
                                langs), HAWP (2.3K, HI), A R MATH (6K, AR), PATI G ONIT (10K,                    equations, answers, diagrams               low-resource robustness
                                BN), BMWP (8.7K, BN), P OLY M ATH (9K, 18 langs), M3K ANG
                                (108K, 108 langs)
 General expert suites          MMLU (15.9K, 57 subj.), MMLU-P RO (12K), GPQA (448,                              MCQ, exact match, live-scored              Cross-domain quantitative transfer;
                                grad-level), L IVE B ENCH (monthly), HLE (2.5K, Nature 2026),                    tasks                                      calibration under
                                S UPER GPQA (285 disciplines)                                                                                               contamination-resistant protocols

TABLE XV: Functional taxonomy of mathematical datasets by lifecycle position. Training-side resources support pretraining,
instruction tuning, and verifier construction; evaluation-side resources test held-out reasoning, multilingual robustness, and
cross-domain transfer. Resource scales are shown in parentheses.


because of surface linguistic variation; in multilingual set-                                        primary-school MWPs and showed that transfer from a high-
tings, the same issue becomes more severe because number                                             resource Chinese solver improved Arabic performance. Turk-
words, units, morphology, word order, honorifics, and script                                         ish MWP corpora [239] were constructed by translating
conventions all interact with the mathematical parse. Chinese                                        and manually correcting MAWPS, ASD IV-A, SVAMP, and
benchmarks were the earliest large non-English success story:                                        M ATH QA, yielding 4,163 elementary problems and a filtered
M ATH 23K and A PE 210K supplied enough scale for neural                                             19,555-problem Turkish MathQA subset. Early Korean work
equation generation, while CMATH [225] later reframed                                                translated C OMMON C ORE and Illinois arithmetic datasets into
Chinese MWPs as an LLM evaluation problem using 1.7K                                                 CC KO and IL KO for KOTAB [240], while HRM8K [226]
elementary-school problems from actual workbooks and ex-                                             scales this line to 8,011 English–Korean parallel math prob-
ams, organized across six grade levels and augmented with                                            lems and finds that the gap is mostly in understanding Korean
distractor variants.                                                                                 inputs rather than in the underlying reasoning once the prob-
                                                                                                     lem is correctly represented.
   Low-resource and regional-language datasets reveal a dif-
ferent set of bottlenecks. HAWP [223] introduced 2,336                                                 Bangla/Bengali resources have also emerged rapidly.
Hindi arithmetic word problems and emphasized equation-                                              PATI G ONIT [227] contains 10,000 Bengali math problems and
equivalence evaluation rather than raw string matching. A R -                                        evaluates transformer models including Basic Transformer,
MATH [224] contributed 6,000 Modern Standard Arabic                                                  mT5, BanglaT5, and mBART50 for equation generation,
Resource                 Year    #Train      #Test    #Total Language Task      Solution Level   Modality Diagnostic focus

Classical and large-scale MWP benchmarks
AI2 [39]                    2014          –       395       395 EN      MWP     Eq       E       T        Additive reasoning, verb categories
S INGLE EQ [103]            2015          –       508       508 EN      MWP     Eq       E       T        Single-unknown algebraic parsing
A LG 514 [40]               2014          –       514       514 EN      MWP     Eq       M       T        Equation-template induction
D OLPHIN 18K [115]          2016    14,768      3,692    18,460 EN      MWP     Eq       M       T        Large-scale template diversity
MAWPS [214]                 2016          –     3,320     3,320 EN      MWP     Eq       E       T        Unified multi-dataset evaluation
ASD IV [215]                2020          –     2,305     2,305 EN      MWP     Eq       E       T        Lexical and syntactic diversity
AQ UA [216]                 2017    97,467        254    97,975 EN      MWP     Rat      U       T        End-to-end rationale training
Large-scale Chinese MWP
M ATH 23K [41]              2017    22,162      1,000    23,162 ZH      MWP     Eq       E       T        Central Chinese MWP benchmark
A PE 210K [217]             2020 200,488        5,000   210,488 ZH      MWP     Eq       E–M     T        Largest template-rich Chinese corpus
Robustness and perturbation benchmarks
SVAMP [12]                  2021       700        300     1,000 EN      MWP     Eq       E       T        Paraphrase, distractor, reordering
PARA MAWPS [218]            2023    13,023      3,255    16,278 EN      MWP     Eq       E       T        Linguistic variants and voting
GSM-S YMBOLIC [13]          2024          –     5,000     5,000 EN      MWP     Ans      E       T        Name/number substitution variance
Chain-of-thought and competition benchmarks
GSM8K [93]                  2021     7,473      1,319     8,792 EN      MWP     CoT      E       T        Grade-school multi-step reasoning
MATH [219]                  2021     7,500      5,000    12,500 EN      MWP     CoT      H–C     T        7 subjects, 5 difficulty tiers
O LYMPIAD B ENCH [220]      2024          –     8,476     8,476 EN/ZH   MWP     Ans      C       M        Bilingual multimodal olympiad
O MNI -MATH [221]           2024          –     4,428     4,428 EN      MWP     Ans      C       T        33 domains, 10+ difficulty levels
F RONTIER M ATH [212]       2024          –    ∼350      ∼350 EN        MWP     Ans      R       T        Research-grade, private solutions
M ATH A RENA [180]          2025          –   149+/yr   149+/yr EN      Mixed   Mixed    C       T        Live competitions, contamination-free
IMO-P ROOF B ENCH [171] 2025              –         60        60 EN     Proof   Proof    C       T        Proof-grading (basic / advanced splits)
Multilingual and regional-language MWP
MGSM [222]                  2022          –     2,500     2,500 10      MWP     CoT      E       T        Multilingual CoT emergence
HAWP [223]                  2022          –     2,336     2,336 HI      MWP     Eq       E       T        Hindi equation equivalence
A R MATH [224]              2022     4,800      1,200     6,000 AR      MWP     Eq       E       T        Arabic primary school, transfer
CMATH [225]                 2023          –     1,700     1,700 ZH      MWP     CoT      E       T        Chinese grade-level robustness
HRM8K [226]                 2025     7,011      1,000     8,011 KO/EN   MWP     CoT      M       T        Korean comprehension gap
PATI G ONIT [227]           2025     8,000      2,000    10,000 BN      MWP     Eq       E       T        Bengali transformer baselines
BMWP [228]                  2025     6,922      1,731     8,653 BN      MWP     Eq       E       T        Bengali textbook, operations
P OLY M ATH [229]           2025          –     ∼9K       ∼9K 18        MWP     CoT      E–C     T        Cross-lingual consistency
M3K ANG [230]               2026          – 108K var. 108K var. 108     MWP     MCQ      E–H     M        Multilingual + multimodal
Geometry and multimodal math
G EOMETRY 3K [5]            2021     2,101        601     3,002 EN      GPS     FL       H       M        Formal-language diagram parsing
G EO QA [35]                2021     3,499        754     4,998 ZH      GPS     Prog     M       M        Multimodal geometric programs
PGPS9K [196]                2023     8,022      1,000     9,022 EN      GPS     Prog     H       M        Fine-grained diagram annotations
M ATH V ISTA [70]           2024          –     6,141     6,141 EN      Vis     Ans      E–C     M        31-source visual math meta-bench
M ATH V ERSE [71]           2024          –     2,612    15,672 EN      Vis     CoT      H       M        Diagram ablation, 6 variants
MATH-V ISION [72]           2024          –     3,040     3,040 EN      Vis     Ans      H–C     M        16-discipline competition
Process, instruction, and augmented data
PRM800K [90]                2023 800K lbl            – 800K lbl EN      PRM     Step     H–C     T        Step-level correctness labels
M ATH -S HEPHERD [91]       2024 rollouts            –  rollouts EN     PRM     Step     H–C     T        Annotation-free step estimation
M ETA M ATH QA [165]        2024     395K            –    395K EN       SFT     CoT      H       T        Backward question rewriting
N UMINA M ATH               2024    860K+            –   860K+ EN       SFT     Mixed    H–C     T        Multi-source competition SFT
Formal theorem proving
M INI F2F [207]             2022          –       244       488 Multi   TP      Proof    H–C     T        Cross-system formal olympiad
P ROOF N ET [204]           2023          –       371       371 EN      TP      Proof    U       T        Informal/formal statement pairs
P UTNAM B ENCH [231]        2024          –       658       658 Multi   TP      Proof    C       T        Hardest public formal benchmark
L EAN W ORKBOOK [81]        2024    57,231           –   57,231 EN      TP      Proof    C       T        Large-scale autoformalized
D EEP T HEOREM [203]        2025     121K            –    121K EN       TP      CoT      C       T        Informal proving + RL-Zero
General expert and live evaluation suites
MMLU [232]                  2021          –    14,042    15,908 EN      MCQ     MCQ      U       T        57-subject academic breadth
GPQA [233]                  2023          –       448       448 EN      MCQ     MCQ      G       T        Graduate-level, Google-proof
L IVE B ENCH [234]          2025          –       live      live EN     Multi   Mixed    H–C     T        Contamination-free, auto-scored
HLE [235]                   2026          –     2,500     2,500 EN      Multi   Mixed    R       M        Expert-authored, Nature 2026

TABLE XVI: Dataset and benchmark landscape with concrete scales and structured metadata. Solution: Eq = equation, Ans =
numeric answer, CoT = chain-of-thought, Prog = program, FL = formal language, Proof = formal proof, Rat = rationale, MCQ =
multiple choice, Step = step labels, Mixed = multiple. Level badges: E =elementary, M =middle, H =high school, U =undergraduate,
C =competition, R =research-grade, G =graduate. Modality badges: T =text, M =multimodal.
Track                 Representative systems                           Core idea                                   Supv.           Main benchmarks                        Current lesson

 Rule/stat MWPs       W ORD P RO, A RIS, Kushman et al.                Problem frames & log-linear templates       S E             AI2, A LG 514                          Brittle coverage; high interpretability
 Neural MWPs          Seq2Seq, GTS, G RAPH 2T REE, MWP-BERT            Tree / expression decoding from text        E               MAWPS, M ATH 23K, ASD IV               Strong in-domain; fragile under perturbation
 Prompted LLMs        CoT, self-cons., ToT, least-to-most              Sample natural-language reasoning           A               GSM8K, MATH                            Fluent traces ̸= valid ones; external checks required
                                                                       traces
 Tool-int. LLMs       PAL, P OT, T O RA, calc. agents                  NL reasoning interleaved with exe-          C A             GSM8K, MATH, tabular QA                Best for arithmetic precision once the problem is parsed
                                                                       cutable code
 Math-spec. LMs       M INERVA, L LEMMA, DSM ATH, Q WEN 2.5-           Math-heavy pretraining + CoT/PoT            E C P           GSM8K,      MATH,   AIME,              Data curation often rivals parameter count
                      M ATH, MA MMOTH                                  SFT                                                         MMLU-STEM
 Multilingual LMs     M ATH O CTOPUS, mCoT, UST                        Parallel SFT; English-as-anchor reason-     A               MGSM, MSVAMP, HRM8K,                   Source-language comprehension is the bottleneck
                                                                       ing                                                         P OLY M ATH
 Reasoning models     OpenAI o1/o3, D EEP S EEK -R1, Kimi k1.5         Long internal search trained with RLVR      R P             AIME, MATH, F RONTIER -                Inference budget becomes a first-class variable
                                                                                                                                   M ATH, HLE, GPQA
 Multi-agent          Debate, R E C ONCILE, DY LAN, M OA, G OA,        Propose, critique, route, verify, refine    A P             GSM8K, MATH, MMLU-Pro,                 Diversity pays only with routing and verifiers
                      MALT                                                                                                         GPQA
 Plane-geom solvers   I NTER GPS, PGPSN ET, G EO DRL, LANS, P I -      Diagram → formal clauses; theorem           S V C           G EOMETRY 3K, PGPS9K                   Diagram grounding + multi-rollout voting drive gains
                      GPS, MARS-GPS                                    search
 Visual-CoT MLLMs     Visual CoT, Chain-of-Spot, S KETCHPAD, ICoT,     Anchor each reasoning step to image         V P             M ATH V ISTA -M ATH, G EO QA,          Visual evidence enters the rationale, not just the input
                      MINT-C OT                                        regions                                                     MMS TAR -M ATH
 Olympiad geom.       A LPHAG EOMETRY, A LPHAG EOMETRY 2               Neural proposer + symbolic DDAR en-         S               IMO-AG-30, IMO geometry                Domain-specific symbolic engines outpace general MLLMs
                                                                       gine
 Formal provers       L EAN D OJO, DSP ROVER, A LPHA P ROOF, L EAN -   Retrieve premises, decompose goals,         K R             M INI F2F,            P ROOF N ET,     Correctness is free; autoformalization is the bottleneck
                      STA R                                            gen. tactics                                                P UTNAM B ENCH
 Discovery systems    F UN S EARCH, A LPHA E VOLVE, Erdős workflows   Programs/constructions filtered by objec-   C K H           cap-set, bin-pack, live open prob-     Needs novelty checks and human/formal validation
                                                                       tive                                                        lems


TABLE XVII: Representative model families across the mathematical-reasoning literature, compressed into a single visual scan.
Colored stripes in the Track column group rows by paradigm family, following Figure 5. The Supv. column uses badges in
place of prose: A = final-answer grader; E = equation/expression labels; C = code execution; P = process reward model; R = RLVR
/ verifiable reward; K = proof-assistant kernel; S = symbolic solver; V = visual-region grounding; H = human audit.


with mT5 reported as the strongest model. BMWP [228]                                                                   Resource                          Lang           Scale              Survey-level lesson


provides 8,653 Bengali arithmetic problems drawn largely                                                                Sinitic web crawls
                                                                                                                       M ATH 23K, A PE 210K              ZH             23K / 210K         Scale enabled neural non-EN MWPs; template bias
from Bengali-medium textbooks, annotated with equations,                                                                                                                                   persists
                                                                                                                       CMATH                            ZH              1.7K               Grade-level + distractor analysis for Chinese LLMs
solutions, and operation classes; it highlights pronoun resolu-                                                         Indic native corpora
                                                                                                                       HAWP                             HI              2.3K               Equation-equivalence beats raw string match
tion, compound sentences, irrelevant information, and object-                                                          PATI G ONIT, BMWP                BN              10K / 8.7K         Local curriculum cannot be replaced by EN-only tests
keyword identification as Bengali-specific obstacles. These                                                             Other low-resource native & translated
                                                                                                                       A R MATH                         AR              6K                 Cross-lingual ZH → AR transfer helps
resources matter for Bangla-language educational AI because                                                            Turkish MWP corpora              TR              4.2K + 19.6K       Agglutinative morphology breaks seq2seq transfer

direct translation from English does not preserve local curricu-                                                       KOTAB, HRM8K
                                                                                                                        Parallel multilingual
                                                                                                                                                        KO              1.2K / 8K          Korean comprehension dominates the reasoning gap

lum, units, names, or the syntactic phenomena that determine                                                           MGSM, M ATH O CTOPUS, mCoT 10–11                 2.5K–73K           Multilingual CoT emerges with scale, but stays uneven
                                                                                                                       M ATH M IST, P OLY M ATH         13 / 18         30K / 9K           Reasoning models still show language inconsistency
the equation.                                                                                                           Multilingual multimodal
   Parallel multilingual benchmarks make controlled cross-                                                             M3K ANG                          108             1.7K × 108         Multilingual math must be tested jointly with diagrams

language comparison possible. MGSM [222] manually trans-                                                               TABLE XVIII: Non-English and multilingual mathematical-
lates 250 GSM8K problems into ten typologically diverse lan-                                                           reasoning datasets at a glance. Resources are grouped by
guages, including Bengali and Swahili, and shows that multi-                                                           construction strategy in the violet sub-headers. Lang = ISO-
lingual CoT ability emerges with scale. M ATH O CTOPUS [241]                                                           style code, or the number of languages for parallel and
extends this into training data with MGSM8KI NSTRUCT                                                                   multilingual-multimodal resources.
(about 73.6K examples across ten languages) and MSVAMP
(10K out-of-domain test examples). mCoT-MATH [242] cov-
ers eleven languages for multilingual CoT instruction tuning
and focuses on reasoning consistency across languages. More                                                            seven subject areas, fundamentally shifted the community’s
recent resources raise the ceiling: P OLY M ATH [229] covers 18                                                        expectation of what “hard” meant. Accuracies on MATH
languages and four difficulty levels, revealing large language-                                                        climbed from 6.9% (GPT-3, 2020) to > 95% (reasoning
to-language variation and input-output language inconsistency                                                          models, 2025).
even for advanced reasoning models; M ATH M IST [243] builds                                                              O LYMPIAD B ENCH [220] extends this frontier with 8,476
approximately 30K aligned question–answer pairs across                                                                 Olympiad-level problems in mathematics and physics, in-
thirteen languages from Bangla-English gold artifacts; and                                                             cluding bilingual (English/Chinese) and multimodal variants.
M3K ANG [230] brings the same question to multimodal rea-                                                              O MNI -MATH [221] collects 4,428 competition problems cov-
soning with 1,747 Kangaroo competition problems translated                                                             ering 33 domains and over 10 difficulty levels, constructed
into 108 languages, many with diagrams, plus human student                                                             specifically to evade leakage concerns. AIME 2024 and
baselines.                                                                                                             AIME 2025 (30 problems each) are the natural continuation:
                                                                                                                       short, difficult, and not-yet-memorized at the time of release,
D. Competition-level and Olympiad Benchmarks                                                                           they became the standard measure by which o1, o3, DeepSeek-
   The 2021 release of MATH [219], 12,500 problems drawn                                                               R1, and Kimi k1.5 were compared.
from AMC, AIME, and other US mathematics competitions,                                                                    F RONTIER M ATH [212], released in late 2024, represents a
with step-by-step solutions and five difficulty tiers across                                                           deliberate effort to outrun the cycle of benchmark saturation.
It consists of several hundred problems (exact count withheld;      ized exams, including SAT Math, math competitions, and
“several hundred” verified, approximately 350 in tier 1–3 and       college-entrance examinations, thereby measuring mathemat-
a smaller tier 4) authored by expert mathematicians across          ical reasoning as part of a broader human-test-taking pro-
all major branches of modern mathematics, with a research-          file. GPQA [233] is a 448-question graduate-level bench-
grade difficulty tier (tier 4) whose problems require novel ideas   mark in biology, physics, and chemistry; although not a
rather than application of standard techniques. Solutions are       mathematics benchmark, it stresses the same skills needed
held privately; only numerical final answers are submitted          for scientific mathematical reasoning: quantitative inference,
for grading. At release, leading models scored < 2%; by             symbolic manipulation, and resistance to quick web lookup.
April 2025, GPT-5’s predecessor o3 reached ∼ 25.2%; by late         L IVE B ENCH [234] explicitly targets contamination by releas-
2025, o4 and Gemini reach higher on tiers 1–2 but remain at         ing fresh, automatically scored tasks from recent sources, in-
single digits on tier 4.                                            cluding math competitions and arXiv papers, across math, cod-
     Live competition evaluation: A complementary response          ing, reasoning, language, instruction following, and data anal-
to the contamination problem is dynamic benchmarking via            ysis. S UPER GPQA [248] extends the broad-expert paradigm
live competitions. M ATH A RENA [180] evaluates models on           to 285 graduate disciplines and notes that existing evaluations
newly released math competitions, including AIME, HMMT,             overrepresent mainstream areas such as mathematics, physics,
BRUMO, SMT, and USAMO, within days of problem release,              and computer science relative to the full breadth of specialized
effectively eliminating memorization. Across 149 problems           human knowledge.
from five 2025 competitions, o3 (high), o4-mini (high), and            The most visible recent example is HLE (Humanity’s Last
Gemini 2.5 Pro each exceed 86% average accuracy on final-           Exam) [235], published online in Nature on 28 January 2026.
answer competitions, outperforming the top 1% of human              HLE contains 2,500 expert-authored, closed-ended questions
participants. However, on the proof-based USAMO 2025 (6             across dozens of subjects, including mathematics, the natural
problems, 42 points maximum), even the best model (Gem-             sciences, humanities, and social sciences. Questions may be
ini 2.5 Pro, 10.1/42) scores far below the human median of          text-only or multimodal, are either multiple-choice or short-
15/42, exposing a persistent gap between answer production          answer for automated grading, and are designed to have unam-
and rigorous proof writing.                                         biguous, verifiable answers that cannot be quickly recovered
   The M ATH A RENA framework also provides direct evi-             by internet retrieval. For mathematical reasoning, HLE’s role
dence of contamination in older benchmarks. By comparing            is complementary to F RONTIER M ATH: F RONTIER M ATH asks
model scores on AIME 2024 vs. AIME 2025 against human-              whether models can solve deep mathematics, whereas HLE
performance quantiles, the authors find that most models            asks whether mathematical skill transfers into a broad frontier-
score 10–20 percentage points higher on the 2024 version            of-knowledge exam where calibration, domain recognition,
than their 2025 performance would predict, with one model           and tool-independent reasoning all matter.
(QwQ-Preview-32B) inflated by nearly 60%. This confirms the            A related question is how scientific-reasoning benchmarks,
concern, raised in Section X, that reported AIME 2024 scores        suites that test mathematics in service of a scientific argu-
should be interpreted with caution.                                 ment rather than as an end in itself, bear on the picture
                                                                    surveyed here. We treat them as adjacent rather than central:
E. General-Purpose Expert and Live Benchmarks                       S CI B ENCH [249] aggregates 869 open-ended college-level
   Not all mathematically informative benchmarks are math-          problems in physics, chemistry, and calculus that demand
only. Broad academic suites have become important because           multi-step quantitative derivation; S CI E VAL [250] adds 18K
frontier systems are now evaluated as general problem solvers:      objective and subjective items spanning research-paper com-
a model that can solve AIME-style algebra but fails at              prehension, experimental reasoning, and formula application;
quantitative chemistry, formal logic, or data-analysis questions    and S CIENCE QA [251] provides 21K multimodal grade-
has not acquired robust mathematical reasoning in the wider         school science questions with stepwise lecture and explana-
sense. MMLU [232] initiated this style of evaluation with           tion annotations. P HYSICS E VAL [252] sharpens the physics
57 academic and professional subjects, including elementary         slice by pairing 19,609 textbook-sourced physics problems
mathematics, computer science, law, and history. MMLU-              with solutions scraped from physics forums and educational
P RO [244] raises the difficulty by adding more reasoning-          websites, then evaluating inference-time strategies, including
focused questions, expanding the answer set from four to ten        multi-agent verification, on both mathematical and descriptive
options, and filtering noisy items; the paper reports a 16–         physics questions. These suites are most informative for our
33% accuracy drop relative to MMLU and finds that CoT               purposes when the underlying reasoning is mathematical,
helps more on the harder benchmark. BBH [245], a 23-task            a kinematics problem reduces to algebra; a stoichiometry
subset of BIG-B ENCH [246], is less explicitly mathematical         question, to rational arithmetic; an experimental-design ques-
but includes algorithmic, logical, and multi-step reasoning         tion, to combinatorics. For that reason, we report scientific-
tasks for which CoT was shown to substantially change model         reasoning numbers only when they expose a failure mode also
performance.                                                        visible on mathematical benchmarks (e.g., calibration under
   Several newer benchmarks make the connection to math-            contamination-resistant evaluation, or the brittleness of multi-
ematics more direct. AGIE VAL [247] uses human standard-            step derivations under surface paraphrase), and otherwise refer
the reader to dedicated scientific-reasoning surveys for a            Tabular math is methodologically important for three rea-
complete treatment. The boundary is admittedly porous, and         sons. First, it isolates the retrieval-plus-arithmetic sub-skill:
the convergence of mathematical, scientific, and engineering       the model can only get the answer right if it locates the
reasoning into a single “quantitative reasoning” construct is an   correct cells and composes the right operations, separating
open empirical question that we revisit in Section XI.             comprehension failures from arithmetic failures more cleanly
                                                                   than narrative MWPs allow. Second, it is a natural target for
F. Geometry and Visual-Math Datasets                               tool-augmented reasoning, PoT/PAL approaches that compile
                                                                   the question to a Python or SQL program achieve gains here
   Classical geometry datasets include G EOS [191], 186 SAT
                                                                   that are larger than on text-only MWPs, because table ground-
plane-geometry problems; G EOS ++ [192], 1,406 problems
                                                                   ing maps cleanly onto a structured indexing operation. Third,
from Grade 6–10 geometry textbooks; G EO S HADER [193],
                                                                   financial and scientific tabular benchmarks (F IN QA, TAT-QA,
102 shaded-area problems; G EOS -OS [194], 2,235 problems;
                                                                   M ULTI H IERTT) are now standard slices in agentic-reasoning
G EOMETRY 3K [5], 3,002 problems with formal-language
                                                                   evaluations: their gold programs serve simultaneously as su-
ground truth; G EO QA [35], 5,010 multiple-choice problems
                                                                   pervision for code-generating agents and as verifiable rewards
with annotated operation programs; G EOMETRY QA [195],
                                                                   for RLVR-style training. We mention tabular math as a coequal
1,398 re-annotated problems from a geometry subset of
                                                                   task family alongside textual MWPs, geometry, and formal
M ATH 23K; and PGPS9K [196], 9,022 plane-geometry prob-
                                                                   proving, but defer a fuller treatment to the dedicated table-
lems with fine-grained diagram annotations and interpretable
                                                                   reasoning surveys; its principal interest here is as evidence
solution programs.
                                                                   that the comprehension–generation–verification triad applies
   The vision-language era introduced broader multimodal
                                                                   cleanly even when the comprehension stage is dominated by
benchmarks: M ATH V ISTA [70] with 6,141 examples across 31
                                                                   structured-evidence retrieval rather than diagram parsing.
source datasets; M ATH V ERSE [71] with 2,612 problems ren-
dered in six variants (15K total) for step-wise CoT evaluation;
MATH-V ISION [72] with 3,040 competition problems across           H. Formal-Proof and Autoformalization Datasets
16 disciplines; MV-MATH with multi-visual-context prob-
                                                                      M INI F2F [207] provides 488 high-school and early-
lems; and W E -M ATH targeting fine-grained mathematical-
                                                                   undergraduate problems formalized in Lean, Metamath, Is-
knowledge evaluation. A common finding across these bench-
                                                                   abelle, and HOL Light. P ROOF N ET [204] pairs 371 un-
marks is that current multimodal LLMs rely heavily on tex-
                                                                   dergraduate math theorems with informal/formal statements
tual cues: M ATH V ERSE reports cases where several MLLMs
                                                                   and proofs in Lean. P UTNAM B ENCH [231] formalizes 658
improve when the diagram is removed [71]. MINT-C OT [74]
                                                                   Putnam Competition problems across Lean 4, Isabelle, and
extends this diagnostic direction from benchmark construction
                                                                   Coq, establishing a new high-water mark for difficulty in
to supervision, adding a 54K-example visual-interleaved CoT
                                                                   formal evaluation. L EAN W ORKBOOK [81] contains 57,231
dataset in which individual reasoning steps are aligned with
                                                                   math competition problems formalized from natural-language
selected image tokens. This makes step-level grounding a
                                                                   sources, of which 21,197 have been verified and carry proofs.
trainable object rather than an a posteriori explanation of a
                                                                   P ROVER B ENCH [79] adds 325 problems including 15 from
completed answer.
                                                                   AIME 24/25. The mathlib [84] library itself, now exceeding
                                                                   1.6M lines of Lean 4 formalization, serves both as a training
G. Tabular Mathematical Reasoning
                                                                   corpus and as the premise pool against which retrievers are
   A distinctive strand of mathematical reasoning that is          evaluated.
neither purely textual nor diagrammatic operates over semi-
structured tables: numerical inference must traverse rows,         I. Probing and Functional Benchmarks
columns, and hierarchical headers before any arithmetic can
begin. TAB MWP [253] contains 38,431 grade-school prob-               A complementary class of benchmarks attempts not to
lems each paired with a table; solutions are expressed ei-         raise the ceiling but to probe the floor. S VAMP [12], men-
ther as free-text answers or as multi-step programs, and           tioned above, was the first to systematically demonstrate
the dataset becomes a standard test of whether models can          that surface perturbations could collapse performance. GSM-
ground numerical references in tabular evidence. In the finan-     S YMBOLIC [13] extends this idea to the reasoning-model era:
cial domain, F IN QA [254] provides 8,281 expert-annotated         by rendering G SM 8K problems as templates and systemati-
question–answer pairs over earnings reports in which the           cally varying surface features, it shows that even state-of-the-
gold rationale is a small executable arithmetic program, while     art LLMs exhibit significant accuracy variance under name
TAT-QA [255] (16,552 questions) and M ULTI H IERTT [256]           and number substitutions, and that performance degrades more
(10,440 questions over multi-hierarchy tables) raise the diffi-    sharply than humans’ when additional clauses are appended.
culty by requiring joint reasoning over text and several nested    P UTNAM -AXIOM provides an auto-generated perturbation
tables. The more recent TABULAR B ENCH [257]-style suites          suite for the Putnam problems. The functional benchmarks
and M ULTI TAB QA [258] push the frontier toward multi-table       of [259] generate unbounded problem variants to defeat mem-
aggregation and cross-table joins.                                 orization.
Benchmark        Pre-DL      Seq2Tree       LLM era         Reasoning era       System                            IMO-AG-30      IMO-AG-50   IMOSL-AG-
                                                                                                                                                30
 M AWPS          ∼60%       92.0% [46]        >95%              >99%
 M ATH 23K       ∼60%       85.4% [44]        >90%              >95%             Purely symbolic baselines
 G SM 8K           –         55% [93]      94.6% (GPT-4o)   97.3% (Kimi K2)     Wu’s method† [260], [261]            15/30†          –           –
 MATH-500          –        6.9% (GPT-3)    52% (GPT-4)     99.2% (LongCat)     DD+AR (DDAR alone) [68]               14/30        14/50         –
 AIME 2024         –             –         12% (GPT-4o)       91.6% (o3)        Wu + DD+AR ensemble [261]             21/30          –           –
 AIME 2025         –             –               –            94.6% (SU-         Neuro-symbolic geometry solvers
                                                             01 / GPT-5.5 H)    A LPHAG EOMETRY (AG1) [68]            25/30        27/50         –
 GPQA-D            –             –         53.6% (GPT-4o)    94.6% (Claude      A LPHAG EOMETRY + Wu [261]            27/30          –           –
                                                                 Mythos)        T ONG G EOMETRY [262]                 30/30          –           –
 F RONTIER -       –             –         <2% (GPT-4o)     48% (co-math. T4)   A LPHAG EOMETRY 2 (AG1 setup) [69]    28/30        38/50         –
M ATH‡                                                                          A LPHAG EOMETRY 2 (full) [69]         30/30        42/50       20/30
                                                                                 General reasoning LLMs (formal IMO 2024 eval)
TABLE XIX: Illustrative performance trajectory on canonical                     OpenAI o1 [21]                          –           0/50         –
MWP, competition, and expert-reasoning benchmarks. Cell                         Gemini Deep Think [179]                 –           0/50         –
shading is a five-step green heatmap of accuracy (<25 %,                         Human reference
25–60 %, 60–90 %, 90–98 %, ≥98 %); gray “–” cells indicate                      Avg. human gold medalist             25.9/30       40.9/50       –
the benchmark did not exist or was not evaluated in that era.
Stripes follow the paradigm palette of Figure 5. The 2025–                      TABLE XX: Performance on IMO geometry benchmarks.
2026 entries draw on the LLM Stats live leaderboard [181],                      IMO-AG-30: 30 IMO 2000–2022 problems formalizable
accessed May 10, 2026, and should be treated as provisional                     in AG1 [68]; IMO-AG-50: broader 2000–2024 set [69];
self-reported frontier indicators. ‡ The 48 % F RONTIER M ATH                   IMOSL-AG-30: 30 hard IMO shortlist problems never se-
figure is the AI co-mathematician’s Tier-4 score [159]; the o3                  lected for the contest. †Wu’s method was originally reported
number to its left is the Tier 1–3 average, so the two are not                  as 10/30; Sinha et al. [261] found a JGEX reimplementation
directly comparable.                                                            solves 15/30. o1 and Gemini Deep Think score 0/50 on the
                                                                                formal eval (no symbolic engine); their natural-language IMO
                                                                                performance is much higher. The magenta-shaded row marks
J. Performance Across Eras                                                      the overall state of the art.

    Figure 14 traces the trajectory of best-reported single-
model performance on nine canonical benchmarks from 2021                        new constraint narrows the search space and supplies a training
through early 2026, partitioned into the three families that                    signal that a pure next-token objective cannot provide.
organize the rest of this section: textual MWP and compe-
                                                                                A. From Representation Engineering to Verifier Engineering
tition tasks, multimodal and frontier evaluations, and formal
theorem proving. Three patterns are immediately visible. First,                    The earliest systems invested most of their effort in repre-
GSM8K and MATH have effectively saturated, both clear                           sentation engineering: problem frames, templates, quantified
95% by 2025, confirming that grade-school and high-school                       sets, semantic parses, equation trees, and unit graphs. Con-
mathematics no longer discriminate between frontier systems.                    temporary systems invest more in verifier engineering: exact-
Second, the curves for AIME 2024, F RONTIER M ATH, and                          answer graders, PRMs, symbolic solvers, execution harnesses,
P UTNAM B ENCH all exhibit a discontinuity at the onset of                      and Lean kernels. The difference is not absolute. Modern
the reasoning-model era (shaded band), with single-month                        systems still need representations, and old systems still used
jumps that exceed the entire 2021–2024 trajectory. Third,                       checks. The shift is one of emphasis: instead of hand-designing
formal proving, long thought to be the slowest-moving axis,                     a representation that will always be correct, researchers in-
has in fact moved fastest in relative terms: M INI F2F- TEST                    creasingly allow large models to propose many candidate
rose from roughly 25% in 2022 to 93% by early 2026, and                         representations and rely on external verifiers to keep only the
P UTNAM B ENCH from near-zero to over 60% in a little over                      useful ones.
a year. Table XIX provides the matching numerical summary;                      B. The Supervision Ladder
Tables XX and XXI focus on Olympiad geometry and plane-
                                                                                   Mathematical reasoning has advanced by climbing a super-
geometry solvers, respectively.
                                                                                vision ladder. At the bottom are final answers; above them are
                                                                                equations and programs; above those are step-level rationales
   IX. C ROSS -C UTTING M ETHODOLOGICAL S YNTHESIS
                                                                                and proof sketches; at the top are mechanically checked proofs.
   Across the literature reviewed above, progress is best under-                Each rung is more expensive to obtain but more informative
stood less as a sequence of isolated model architectures and                    when available. This ladder also explains why mathematics is
more as a repeated pattern: systems become powerful when                        unusually attractive for AI research: unlike many open-ended
they combine expressive generation with a strong external                       language tasks, it offers natural sources of objective feedback.
constraint. The constraint may be an equation grammar, a unit-                  The long-term opportunity is to make the top rungs cheaper by
dependency graph, a Python interpreter, a geometry theorem                      using models to generate candidate formalizations and proof
database, a process reward model, or a proof assistant. Each                    attempts, and then using the proof assistant to filter them.
                                                                                                                                                                                    % H Q F K P D U N  V D W X U D W L R Q              E H V W  U H S R U W H G  V L Q J O H  P R G H O  S H U I R U P D Q F H
                                                                                                                                        7 H [ W  0 : 3  	  F R P S H W L W L R Q                                                        0 X O W L P R G D O  	  I U R Q W L H U                                                                              ) R U P D O  W K H R U H P  S U R Y L Q J
                                                                                           
                                                                                                   K X P D Q  F H L O L Q J   J U D G H  V F K R R O                                                                                 0 D W K 9 L V W D
  E H V W  U H S R U W H G  D F F X U D F \    S U R R I  V X F F H V V    


                                                                                                                                                                                                                                          ) U R Q W L H U 0 D W K
                                                                                                                                                                                                                                          + / (                                                                              H [ S H U W  K X P D Q  R Q  0 L Q L )  )   L Q I R U P D O 
                                                                                                                                                                                                                                        , 0 2  3 U R R I % H Q F K


                                                                                           


                                                                                           


                                                                                                                                                                                                   * 6 0  .                                                                                                                                                                                                                   0 L Q L )  )  W H V W
                                                                                                                                                                                                     0 $ 7 +                                                                                                                                                                                                                     3 X W Q D P % H Q F K
                                                                                                                                                                                                      $ , 0 (     
                                                                                                                                                                                      U H D V R Q L Q J  P R G H O  H U D                                                                                                                                                                                                      3 U R R I 1 H W
                                                                                            
                                                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                    \ H D U                                                                                                         \ H D U                                                                                                         \ H D U

Fig. 14: Benchmark saturation, 2021–2026: best-reported single-model performance on nine canonical mathematical-reasoning
benchmarks, grouped by task family. Pass@1 (or proof-success rate, for formal benchmarks) is plotted against publication year.
The lavender band marks the reasoning-model era inaugurated by OpenAI o1 in late 2024 (Section IV); dashed horizontal
lines indicate informal human-performance reference points. Numbers are collected from the system reports and benchmark
papers cited throughout the survey; where multiple inference protocols were reported (greedy, majority vote, tool-augmented,
expert-formalized), we plot the higher number and discuss caveats in the body text.


C. Design Principles for Future Benchmarks                                                                                                                                                                                                                                         stage, the resolution was to bring in a stronger external
   The benchmark literature suggests five design principles.                                                                                                                                                                                                                       constraint, and the ultimate constraint, a mechanically checked
First, benchmarks should separate reasoning difficulty from                                                                                                                                                                                                                        proof, is precisely what the formal track provides.
notation difficulty, because failure to parse a diagram or an-                                                                                                                                                                                                                        This pattern has two important implications for practition-
swer format is different from failure to solve the mathematical                                                                                                                                                                                                                    ers. First, no single architectural innovation is likely to be
core. Second, they should report robustness under paraphrase,                                                                                                                                                                                                                      sufficient in isolation; the history of mathematical reasoning is
number substitution, distractor insertion, and diagram ablation.                                                                                                                                                                                                                   a history of combining generation with progressively stronger
Third, they should distinguish public training benchmarks                                                                                                                                                                                                                          verification, and systems that skip the verification step consis-
from private or live evaluation sets, since leakage becomes                                                                                                                                                                                                                        tently overfit to benchmark form. Second, the pattern predicts
more likely as models train on broad web corpora. Fourth,                                                                                                                                                                                                                          where diminishing returns will emerge next: once formal
they should record the full evaluation protocol: sample count,                                                                                                                                                                                                                     verification of competition-level proofs becomes routine, the
tool access, time budget, verifier access, human intervention,                                                                                                                                                                                                                     bottleneck will shift to autoformalization of research-level
and library version. Fifth, they should pair math-specific                                                                                                                                                                                                                         mathematics, library scaling, and the sociological challenge
leaderboards with broad expert suites such as HLE, GPQA,                                                                                                                                                                                                                           of integrating AI-assisted proofs into the human mathematical
and L IVE B ENCH; this reveals whether apparent mathematical                                                                                                                                                                                                                       community.
competence transfers to scientific and cross-domain tasks
rather than remaining a competition-math specialty. Without                                                                                                                                                                                                                        E. The Convergence Hypothesis
these details, comparisons across models can reward inference-
budget differences more than genuine reasoning differences.                                                                                                                                                                                                                           A central question for the field is whether the four research
                                                                                                                                                                                                                                                                                   axes reviewed in this survey, informal reasoning, multimodal
D. Cross-Era Patterns                                                                                                                                                                                                                                                              reasoning, formal proving, and mathematical discovery, are
   Reading Table XXII as a narrative rather than a catalog                                                                                                                                                                                                                         converging into a single unified pipeline or whether they
reveals a recurrent pattern: each generation’s key innovation                                                                                                                                                                                                                      will remain distinct specialties requiring different models and
becomes the next generation’s baseline assumption, and each                                                                                                                                                                                                                        architectures.
generation’s bottleneck is precisely what the successor is                                                                                                                                                                                                                            Evidence for convergence is accumulating. The Gem-
designed to eliminate. Templates were revolutionary when                                                                                                                                                                                                                           ini Deep Think result at IMO 2025, scoring 35/42 in natural
they replaced hand-coded schemata, but became a liability                                                                                                                                                                                                                          language, with officially certified gold-medal performance,
when problem language exceeded the template vocabulary.                                                                                                                                                                                                                            demonstrates that a single end-to-end system can combine
Supervised expression generation was revolutionary when                                                                                                                                                                                                                            informal intuition, visual diagram interpretation (for geometry
it replaced templates, but became a liability when evalua-                                                                                                                                                                                                                         problems), and multi-step deductive reasoning without requir-
tion moved beyond in-distribution test sets. Chain-of-thought                                                                                                                                                                                                                      ing a separate formalization step. Similarly, the Erdős-problem
prompting was revolutionary when it elicited multi-step rea-                                                                                                                                                                                                                       workflow of early 2026, in which GPT-5.2 Pro generated con-
soning from frozen LLMs, but became a liability when fluent                                                                                                                                                                                                                        jectures that Harmonic’s Aristotle system then formalized and
traces proved unreliable without external checking. At every                                                                                                                                                                                                                       verified in Lean, shows informal and formal tracks operating
 System                                         Type        Geo3K       PGPS9K      GeoQA MathVista-Math MMStar-Math
 Symbolic and neural-symbolic solvers
 I NTER GPS [5]                            Sym.               57.5          –           –              –                   –
 G EO DRL [197]                          Sym.+RL              68.4         66.7         –              –                   –
 LANS [198]                             Sym.+NN               82.3         74.0         –              –                   –
 P I -GPS [199]                        Sym.+MLLM              77.8         69.8         –              –                   –
 General-purpose MLLMs (zero-/few-shot)
 GPT-4o [263]                             MLLM                58.6         51.0         –            66.67                –
 Claude 3.5 Sonnet                        MLLM                56.4         45.9         –            67.41                –
 Gemini 1.5 Pro                           MLLM                 –            –           –            63.33               52.4
 Qwen2-VL-7B-Instruct [264]               MLLM                 –            –         37.80          41.11               46.4
 Qwen2.5-VL-7B-Instruct [265]             MLLM                 –            –         43.50          66.66               66.8
 InternVL2.5-8B                           MLLM                 –            –         34.60          49.63               54.8
 Reasoning and math-specialized MLLMs
 R-CoT                                 MLLM+CoT                –            –         45.78          55.93               44.0
 Math-LLaVA                            MLLM+SFT                –            –         47.32          54.81               55.6
 MAVIS-7B                              MLLM+SFT                –            –         52.66          65.19               54.8
 R1-V-7B [266]                          MLLM+RL                –            –         59.00          53.33               54.0
 MM-Eureka-Qw-7B [267]                  MLLM+RL                –            –         40.40          70.37               63.2
 MINT-C OT-7B (SFT) [74]               MLLM+SFT                –            –         60.96          70.37               66.4
 G EO GRPO-Q W-7B [268]                 MLLM+RL               53.2         50.6        80.6           73.4                –
 MINT-C OT-7B [74]                      MLLM+RL                –            –         64.72          73.70               69.6
 Multi-rollout / test-time scaling GPS
 MARS-GPS [200]                        MLLM+TTS               88.8        77.48         –              –                   –

TABLE XXI: Comparison of plane-geometry and visual-math solvers across five benchmarks. “Type” abbreviates the system
category: Sym. = symbolic, NN = neural network, MLLM = multimodal LLM, RL = reinforcement learning, SFT = supervised
fine-tuning, and TTS = test-time scaling. Dashes indicate unreported results. Values are aggregated across sources and protocols,
so the table should be read as a cross-source comparison rather than a controlled leaderboard; all figures are accuracy (%).


as complementary stages within a single discovery pipeline           closest existing approximation to this vision.
rather than as isolated research programs.
                                                                     X. FAILURE M ODES , C RITIQUES , AND O PEN Q UESTIONS
   However, strong evidence also counsels against premature
                                                                        Enthusiasm for recent progress has been balanced by a
claims of convergence. The MathArena live evaluation shows
                                                                     growing body of critique, which we survey honestly before
that even the best reasoning models score roughly 10/42 on
                                                                     turning to future directions.
USAMO-style proof problems that require sustained multi-
page arguments, compared to a human competition median of            A. Robustness and Spurious Correlations
15/42. FrontierMath problems that require novel insight rather
                                                                        The legacy of classical MWP work in Section III already
than pattern-matching still defeat most models. And the gap
                                                                     foreshadowed this failure mode: quantity attachment, unit
between answer-level accuracy (high on AIME, AMC) and
                                                                     interpretation, irrelevant clauses, and template overfitting re-
proof-level completeness (low on USAMO, PutnamBench)
                                                                     mained diagnostic long after explicit templates disappeared.
reveals that answer generation and proof generation remain
                                                                     [12] showed that a seq2seq solver reaching 87% on M AWPS
fundamentally different competencies: a model may “know”
                                                                     dropped to 37% on its own minor perturbations. [13] extended
the answer without being able to justify it formally, or may
                                                                     this critique to the LLM era: on GSM-S YMBOLIC, models
construct a fluent justification that a proof assistant rejects.
                                                                     exhibit variance of several percentage points across renderings,
   The practical resolution may be architectural pluralism           and introducing an irrelevant clause (“GSM-NoOp”) causes
within a shared infrastructure: a generator that proposes con-       accuracy drops of up to 65% even for the strongest models,
jectures and solution sketches in natural language, a verifier       which frequently change their answer under name and number
that checks them against a formal kernel, a search controller        substitutions. These results suggest that much of the improve-
that allocates compute between exploration and exploitation,         ment visible in benchmark accuracies is accompanied by only
and domain-specific modules (geometry solvers, code inter-           partial gains in genuine robustness.
preters, retrieval systems) that plug in as needed. The emerging        The deeper question raised by GSM-S YMBOLIC is what
“verified-discovery workflow” discussed in Section XI is the         kind of failure the observed variance represents. Three hy-
Era                       Dominant constraint (what makes it             Typical bottleneck (what limits it)         Representative artifacts
                          tractable)

Rule / statistical MWP    Hand-coded schemata and templates              Coverage and brittleness                    Problem frames, equation templates
Neural MWP                Supervised expression generation               Generalization outside dataset form         Prefix equations, expression trees
Prompted LLMs             Natural-language reasoning traces              Arithmetic errors and hallucinated steps    CoT, self-consistency samples
Tool-integrated LLMs      Executable interpreters and calculators        Program faithfulness to the problem text    Python snippets, tool traces
Multi-agent systems       Debate, routing, role-specialized critique     Correlated errors and communication cost    Agent transcripts, confidence votes, graph
                                                                                                                     messages
Distilled reasoning       Internalized debate + RLVR on verifiable       Token cost; oversight of latent reasoning   Long CoT traces, distilled trajectories
                          rewards
Formal provers            Proof-assistant kernels and libraries          Autoformalization and search cost           Lean statements, tactic scripts, proof terms
Discovery systems         Domain-specific evaluators + expert / formal   Novelty, literature audit, and proof        Programs, constructions, verified theorems
                          verification                                   certification

TABLE XXII: The field as a supervision ladder. Each row pairs an era with the external constraint that made it tractable, the
bottleneck that motivated the next transition, and the artifacts it produced. Column tints distinguish constraints from bottlenecks,
while era stripes follow the paradigm palette of Figure 5.


potheses compete. The training-data hypothesis holds that                         be concise, checkable, and faithful to the mathematical de-
models memorize problem–answer associations from web-                             pendencies actually used. We therefore recommend reporting
scale corpora and degrade when surface features shift;                            answer accuracy together with at least one process-sensitive
contamination-controlled benchmarks such as F RONTIER -                           measure, such as verifier pass rate, step-level PRM score,
M ATH [212] support this reading. The architectural hypothe-                      average reasoning tokens per solved problem, or the fraction
sis, advanced by Apple researchers [13], holds that autoregres-                   of solutions accepted by an external proof checker.
sive next-token prediction is fundamentally misaligned with                          The emerging literature on step-level evaluation offers par-
the compositional, non-monotonic structure of mathematical                        tial solutions. PRM scores provide a continuous proxy for step
reasoning: the model must commit to early tokens before “see-                     quality but are themselves trained on data that may conflate
ing” later constraints. The emergent but incomplete hypothesis,                   fluency with validity. D EEP T HEOREM [203] operationalizes
favored by the reasoning-model community, holds that long                         a four-dimensional rubric (logical validity 40%, completeness
CoT and RLVR do produce genuine compositional reasoning,                          30%, correctness 20%, clarity 10%) and shows that process
but that this capability is shallow, reliable on well-represented                 scores and outcome scores can diverge substantially: a model
problem types and brittle under rare structural variations.                       may produce a correct final judgment (proved/disproved) via
Distinguishing these hypotheses experimentally would require                      an incomplete or locally invalid argument. More ambitiously,
two methodological commitments that are not yet standard                          proof economy, the ratio of useful reasoning steps to total
practice: distribution-controlled evaluations that hold problem                   generated tokens, is beginning to be tracked, motivated by
structure fixed while varying surface features [12], [13], and                    the observation that long-CoT models often spend thousands
causal interventions on intermediate reasoning steps that test                    of tokens on exploration that contributes nothing to the final
whether each step is functionally necessary for the final                         answer. For educational and collaborative applications, these
answer.                                                                           process-sensitive metrics matter more than Pass@1: a student
                                                                                  or mathematician working with an AI assistant needs not just
B. Metric Mismatch and Path Optimality                                            the right answer but a derivation they can trust, extend, and
   Recent surveys also stress that final-answer accuracy is a                     learn from.
lossy proxy for mathematical reasoning quality [22], [23].
Pass@1 rewards the first sampled answer; Pass@k rewards                           C. Benchmark Contamination and the Race to Saturation
diversity and search; majority voting rewards agreement; and                         A second class of concerns relates to training-set
proof compilation rewards formal validity. These metrics                          contamination. The sheer scale of LLM pretraining
can disagree. A model may improve Pass@1 while leaving                            makes it plausible that test-problem formulations (and,
Pass@k nearly unchanged, suggesting better selection rather                       in some cases, solutions) appear in the training corpus.
than broader reasoning capacity; conversely, long-CoT or RL                       Cautious researchers now publish benchmarks with
systems may improve Pass@k by producing more diverse                              delayed release schedules (F RONTIER M ATH), live versions
traces while still generating inefficient or locally invalid deriva-              (L IVE M ATHEMATICIAN B ENCH, R EAL M ATH), functional
tions.                                                                            generators [259], expert-written retrieval-resistant suites
   This creates a path-optimality problem. Outcome-based                          (HLE, GPQA), or monthly refreshed objective tasks
training often treats a verbose, circuitous, or partially mis-                    (L IVE B ENCH). Empirical evidence for contamination
taken derivation as acceptable if the final answer is correct.                    is strongest on classical benchmarks; results on newly-
For educational applications, theorem proving, and human-AI                       constructed olympiad and research-level benchmarks are
collaboration, this is insufficient: the reasoning path should                    more difficult to explain by contamination alone.
   The community’s methodological response to contamination             mark tables that aggregate results from multiple papers,
has developed along five lines, each with trade-offs. Delayed           authors should explicitly flag which figures come from
release (e.g., F RONTIER M ATH holding solutions privately)             the original paper and which are reproduced under con-
prevents direct leakage but limits reproducibility and commu-           trolled conditions, since minor differences in prompting,
nity auditing. Live benchmarks (L IVE B ENCH, L IVE M ATHE -            sampling temperature, and evaluation harness can shift
MATICIAN B ENCH) refresh tasks periodically, defeating mem-             scores by several points.
orization but requiring continuous curation effort. Functional
generators [259] produce unlimited problem variants from          D. Reward Hacking in RLVR Training
parameterized templates, ensuring that no specific instance can      The RLVR paradigm that underwrites reasoning mod-
be memorized, but they risk testing only the narrow structural    els [48], [59] assumes that the verifiable reward, typically
family captured by the template. Expert-authored suites (HLE,     exact-match comparison of a final numerical answer, faithfully
GPQA) rely on the obscurity and difficulty of the questions       represents the training objective. In practice, this assumption
to make web-lookup infeasible, but they are expensive to          fails in several documented ways. First, rule-based verifiers
produce and may themselves leak over time. Embedding-based        are surprisingly inaccurate: a recent analysis of a standard
decontamination (as used by D EEP T HEOREM [203], which           empirical reports suggest that a substantial fraction (up to
removed ∼199K contaminated samples via cosine-similarity          38%) of responses flagged as incorrect by a rule-based grader
recall and LLM-based justification) addresses training-data       were in fact correct, because the grader could not handle
hygiene rather than benchmark design. No single strategy          equivalent but differently formatted answers (e.g., 12        1
                                                                                                                         36 vs. 3 ).
is sufficient; the strongest evaluations combine at least two     This false-negative rate deprives the model of informative
(e.g., live tasks with functional variants, or expert-authored    gradients and slows convergence. Conversely, false positives,
questions with delayed solutions).                                in which a lucky final answer receives reward despite an
   M ATH A RENA’s contamination analysis provides the             invalid derivation, reinforce hackable surface patterns.
strongest empirical evidence to date that AIME 2024 scores           Second, models trained with outcome-only RLVR can learn
are inflated by data leakage. The study also reveals a subtler    to exploit format cues: revealing the answer early in the
form of contamination: 8 of 30 AIME 2025 problems and             reasoning trace, generating repetitive or templated padding to
1 of 30 HMMT 2025 problems appeared online in similar             reach the expected length, or producing correct-looking LATEX
form before the competition, even though the competitions         that embeds the answer without genuine derivation. Third,
themselves were new. This “prior-problem leakage” is distinct     when model-based verifiers (e.g., learned PRMs) replace rule-
from training-data contamination and is harder to detect,         based graders, a subtler failure emerges: the policy model
since the leaked problems may come from online forums or          learns to produce traces that score highly on the verifier
earlier competitions rather than from the benchmark itself.       without being mathematically valid, a classical Goodhart’s-law
The implication is that even live evaluation is not fully         dynamic. Empirical work shows that more accurate verifiers do
contamination-proof; the strongest protocol combines live         not always produce better RL outcomes; in some cases, higher-
timing with cross-competition correlation analysis to identify    accuracy verifiers are more susceptible to hacking during
anomalously easy problems.                                        training because the policy has a richer signal to exploit.
   1) Recommendations for Survey-Level Reporting: The dis-           These findings have practical implications for the survey’s
cussion above implies several standards that future surveys       central claim that verification drives progress. Verification
and leaderboards should adopt when compiling results across       improves reasoning only when the verifier is (i) accurate,
systems:                                                          (ii) resistant to adversarial exploitation by the generator, and
   1) Decontamination audits: These should be reported for        (iii) rich enough to provide gradient signal on partial progress.
       every training-data pipeline. At minimum, this involves    Kernel-checked formal proofs satisfy all three conditions,
       n-gram overlap (n ≥ 13) between the training cor-          which is one reason the formal track has advanced so rapidly.
       pus and each benchmark’s test split, supplemented by       Rule-based answer graders satisfy (iii) cheaply but fail on (i)
       embedding-based cosine-similarity recall (as used by       and (ii), which explains why outcome-only RLVR produces
       D EEP T HEOREM [203], which removed ∼199K con-             models that are strong on benchmarks but fragile under
       taminated samples) and, where feasible, LLM-based          perturbation.
       justification for flagged near-matches.
   2) Inference budget reporting: Every accuracy figure           E. Multimodal-Specific Failure Modes
       should be accompanied by its inference budget: the num-       The M ATH V ERSE finding that some MLLMs improve when
       ber of sampled solutions (k), the selection mechanism      diagrams are removed [71] is the best-known multimodal
       (greedy, majority vote, ORM, PRM, execution, or Lean       failure, but it is not the only one. At least three additional
       checking), and an approximate token cost per problem.      failure classes deserve attention. First, diagram hallucination:
       Without these annotations, a “90% on MATH” claim is        models sometimes “see” geometric elements that are not
       ambiguous by at least 20 percentage points depending on    present in the image, or misidentify which angle or segment a
       whether it reflects pass@1 or best-of-256 with a PRM.      label refers to; this is especially common when diagrams are
   3) Cross-paper comparison flags: For compiled bench-           low-resolution, contain overlapping labels, or use non-standard
notation. Second, modality shortcutting: when the textual              effort that remains prohibitive for most mathematical commu-
problem statement contains enough information to solve the             nication.
problem without the diagram, models learn to ignore visual
input entirely; this is not a “bug” but a rational response to         G. Language Transfer and Localization
training distributions in which text is more reliably informative         Multilingual evaluations show that mathematical reasoning
than images. MINT-C OT’s interleave-token mechanism [74]               is not language-neutral in practice. A model may possess the
is explicitly designed to counter this shortcut by forcing the         algebraic skill needed to solve a problem but fail to parse the
model to select image regions before each reasoning step.              problem statement in Korean, Bangla, Arabic, Hindi, Turkish,
Third, cross-modal grounding failure: the model correctly              or Swahili. Translation-based benchmarks such as MGSM
parses both text and image but fails to align them, for instance,      and P OLY M ATH are valuable because they hold mathematical
identifying ∠ABC in the text but measuring ∠ABD in the                 content approximately constant across languages; native or
diagram. This failure is diagnostic of a deeper architectural          localized datasets such as HAWP, A R MATH, BMWP, and
limitation: current multimodal encoders fuse text and image            PATI G ONIT are valuable because they expose curriculum,
at a global level rather than maintaining fine-grained corre-          names, units, discourse patterns, and morphology that transla-
spondence between symbolic names and spatial locations.                tions often erase. For this reason, multilingual results should
                                                                       report the problem language, reasoning language, answer
F. Hallucination in Mathematical Derivations and Proofs                language, and whether the model was allowed to translate
   A failure mode that cuts across informal and formal tracks is       internally. Otherwise, an English-anchored system can appear
mathematical hallucination: the generation of derivation steps         mathematically stronger than it is for users who actually need
that are syntactically well-formed and superficially plausible         reliable non-English educational support.
but logically invalid. Unlike factual hallucination in open-
domain QA, mathematical hallucination is dangerous precisely           H. The “Genuine Reasoning” Question
because it is difficult to detect without line-by-line verification.      A third, and more philosophical, question concerns whether
Common patterns include: (i) citing a theorem that does not            reasoning models are actually reasoning or are very effec-
exist or does not apply to the given hypotheses; (ii) intro-           tive pattern-matchers over reasoning trajectories. Apple re-
ducing an unjustified inequality or bound that happens to              searchers [13] have argued for the latter. Tao [28], [29] has
yield the correct final answer; (iii) silently dropping a case         taken a more nuanced position: he observes that reasoning
in a case analysis; and (iv) circular reasoning in which the           models are now extremely strong at the “discovery mod-
conclusion is assumed in a disguised form. The D EEP T HE -            ulo expertise” regime, connecting a problem to an existing
OREM process evaluation framework [203], which separately              technique, recalling the relevant literature, and producing a
scores logical validity, completeness, correctness, and clarity,       candidate proof, but remain weak at introducing genuinely
provides one operational response to this problem. However,            novel ideas. This is consistent with both the AlphaEvolve
such evaluations currently rely on LLM judges (GPT-4o in               results (improvements of ∼ 20% on the 67-problem bench-
that work), which are themselves susceptible to the same               mark, mostly via clever application of known techniques) and
hallucination patterns they are asked to detect. To quantify           the Erdős-problem solves (which, in Tao’s phrasing, involve
this, the D EEP T HEOREM audit revealed that among logically           “lowest hanging fruit”).
flawed informal proofs generated by state-of-the-art models,
roughly 40% suffer from unjustified inferential leaps, 35%             I. Formal vs. Informal and the Cost of Verification
from calculation or algebraic errors, and 25% from circular               The formal track exists precisely to counter the fluency-
or logically invalid structural assumptions. Furthermore, the          correctness gap. However, the practical question is whether the
nature of these hallucinations has evolved: whereas older              formalization bottleneck is shrinking fast enough to make the
prompted models typically failed by abandoning the logical             formal track useful at scale within the 12–24 month horizon
thread entirely (generating non-sequiturs), modern long-CoT            considered by this survey. The evidence is mixed. On the pos-
reasoning models are far more likely to produce coherent but           itive side, L EAN W ORKBOOK’s first-attempt type-check rate
circular arguments or subtly drop inconvenient cases deep              of 36.5% can be raised substantially with iterative refinement
within a 5,000-token trace.                                            and type-checking feedback [205]; Tao’s experience suggests
   This evolution directly connects back to the supervision            that the human–AI collaborative de Bruijn factor is already
ladder discussed in Section IX. Outcome supervision (the               below the solo-human factor for some problem classes [202];
lowest rung) is blind to these long-trace structural errors, as        and the D EEP S EEK -P ROVER -V2 pipeline demonstrates that
it only checks the final answer. Step-level process reward             decomposition and verified subproofs can scale formal prov-
models (PRMs, the middle rung) can catch algebraic slips               ing to problems previously considered out of reach. On the
and local non-sequiturs, but often fail to detect circular rea-        negative side, the set of mathematical domains covered by
soning that spans multiple paragraphs. Consequently, the only          mathlib remains a small fraction of research mathematics;
hallucination-proof verification mechanism available today is          autoformalization of novel definitions, as opposed to textbook
a proof-assistant kernel (the highest rung), which is precisely        theorems, remains unreliable; and the compute cost of formal
why the formal track exists, but at the cost of formalization          proof search is orders of magnitude higher than informal
generation, which limits the technique to high-value targets. A      mathematics risks becoming the exclusive purview of well-
realistic assessment is that formal verification will be routinely   funded institutions, widening the gap between research uni-
available for competition-level problems and well-formalized         versities in wealthy countries and the rest of the world.
domains (real analysis, group theory, basic combinatorics)           The open-weights movement (DeepSeek-R1, Qwen-Math,
within two years, but that research-level formalization across       Gemma-Math) partially addresses this by enabling local de-
the full breadth of mathematics will require at least a fur-         ployment, but even local deployment of a 671B model requires
ther generation of library expansion and autoformalization           hardware that is unavailable to most research groups in the
improvement.                                                         Global South. Distilled models at the 1.5B–7B scale offer
                                                                     the most realistic path to broad access, and their performance
J. Multi-Agent Coordination and Correlated Errors                    on benchmarks like AIME (e.g., D EEP S CALE R’s 43.1% at
                                                                     1.5B) suggests that strong mathematical reasoning need not
   Multi-agent mathematical reasoning introduces its own fail-
                                                                     be confined to frontier-scale parameters. Nevertheless, the
ure modes. A debate protocol can converge on the wrong
                                                                     community should be explicit about the compute assumptions
answer if all agents share the same misconception; a judge
                                                                     underlying reported results: a system that achieves 91.6%
model can favor eloquent but invalid explanations; and adding
                                                                     on AIME with 1,000-sample reranking at $10 per sample
irrelevant specialist agents can actively degrade performance,
                                                                     occupies a fundamentally different point on the Pareto frontier
as G RAPH - OF -AGENTS demonstrates when comparing full-
                                                                     from one that achieves 79.8% with greedy single-sample
pool aggregation against relevance-aware node sampling [65].
                                                                     decoding.
Communication cost is also non-trivial: naive all-to-all dis-
cussion grows with the number of agents and the length of            L. The October 2025 Erdős Incident
their traces. The AI co-mathematician deployment of Zheng
                                                                        A recent cautionary tale is the October 2025 OpenAI claim,
et al. [159] adds two further failure modes specific to research-
                                                                     rapidly retracted, that GPT-5 had autonomously solved ten
assistant pipelines: reviewer-pleasing bias, in which reviewer
                                                                     open Erdős problems. T. Bloom, the curator of erdosprob-
agents converge on a flawed argument because they share the
                                                                     lems.com, pointed out that all ten were in fact literature
inductive biases of the proposer agents that produced it, and
                                                                     lookups: the system had located existing papers that the
non-termination death spirals, in which iterative review loops
                                                                     database had marked as open due to incomplete cataloging.
fail to converge and degrade into hallucinated reasoning that a
                                                                     The incident is doubly instructive. First, it underscores the
human must recognise and break out of. A related observation
                                                                     importance of careful benchmark auditing by domain experts
from the same deployment: high-quality LaTeX typesetting
                                                                     before accepting model claims. Second, and more positively,
can create a false impression of rigor when the underlying
                                                                     it prompted the development of clear protocols for what
argument is broken, a presentation-layer phenomenon to which
                                                                     constitutes an “AI solve” of an open problem, including the
formal verifiers are immune but human readers are not. For
                                                                     requirement of autonomous discovery, independent verifica-
mathematics, the most promising designs therefore combine
                                                                     tion, and (increasingly) formal verification in Lean. The four
agent diversity with external checks, Python execution, PRM
                                                                     subsequent bona fide Erdős-problem solves (#1026, #728,
scores, symbolic solvers, or Lean kernels, rather than relying
                                                                     #729, #397) in late 2025 and early 2026, each accompanied by
on dialogue alone.
                                                                     Lean formalization, suggest that the community has absorbed
                                                                     this lesson quickly.
K. Energy, Carbon, and Access
   Reasoning-model inference is dramatically more expensive                            XI. F UTURE D IRECTIONS
than single-forward-pass inference, and the cost is growing             Synthesizing across the four axes, we identify ten directions
with each generation. The Arc Prize Foundation’s revised             in which the field appears most likely to advance over the next
estimates place the cost of solving a single ARC-AGI problem         12–24 months.
with o3-high at approximately $30,000 per task, reflecting
the combinatorial search over 1,024 candidate solutions of           A. Verified-Discovery Workflows
roughly 137 pages each. At the API level, o3 is priced at $10           The most consequential architectural shift of the past eigh-
per million input tokens and $40 per million output tokens;          teen months has been the emergence of a canonical four-
a single hard mathematical problem that requires 50,000–             stage pipeline: (i) an LLM proposes a candidate answer or
100,000 reasoning tokens thus costs $2–$4, and budget-               proof sketch; (ii) an informal LLM proof fills in the steps
uncapped search can push this orders of magnitude higher.            in natural language; (iii) an autoformalizer translates the
By contrast, o4-mini and distilled models such as DeepSeek-          proof into Lean 4; (iv) Lean mechanically verifies the result.
R1-Distill-7B operate at roughly 1/10–1/100 of this cost,            Each stage has improved rapidly, but the interfaces between
demonstrating that the trade-off between reasoning depth and         stages remain brittle: autoformalization still fails on many
compute budget is already a design variable.                         mathematically natural statements, and type-checking errors
   The distributional consequences are significant. If the           rarely propagate useful information back into proof revision. A
strongest mathematical reasoning requires frontier-lab APIs          natural research agenda is to train these stages jointly with end-
and multi-thousand-dollar inference budgets, then AI-assisted        to-end reward from the final verification step, in the same spirit
that AlphaZero learned policy and value through a unified           and M3K ANG make it possible to study these questions sys-
training loop.                                                      tematically, including for Bangla and other languages that have
                                                                    historically been absent from math-reasoning leaderboards.
B. Research Assistance Beyond Competitions
   The IMO-gold result of mid-2025 and the Erdős solves            F. Neuro-Symbolic Integration Beyond Geometry
of early 2026 suggest that competition-style evaluation is            A LPHAG EOMETRY demonstrated the power of coupling
approaching saturation. The next frontier is research-level         a neural proposer with a specialized symbolic engine for
mathematics: improvements to existing theorems, counterex-          geometry. The natural generalization, coupling LLMs with
amples to standing conjectures, and explicit constants or           decision procedures, SMT solvers, and computer-algebra sys-
bounds in results that were previously only asymptotic. Bench-      tems across domains, remains comparatively underexplored.
marks such as R EAL M ATH, L IVE M ATHEMATICIAN B ENCH,             Early work on LLM + Z3, LLM + SageMath, and LLM +
and R ESEARCH B ENCH have begun to operationalize this              Lean-hammer pipelines indicates substantial gains over pure-
shift by measuring not single-problem accuracy but end-to-          LLM baselines. We expect this line of work to expand sharply,
end productivity in tasks drawn from the actual research            particularly for inequality proving, real analysis, and algebraic
workflow. Specifically, R EAL M ATH draws problems directly         geometry.
from newly published mathematics papers to evaluate frontier
capabilities on unmemorized concepts, while L IVE M ATHE -          G. The Verifiable-Reward Frontier
MATICIAN B ENCH tests proof-generation models against live,
                                                                       The          reinforcement-learning-from-verifiable-rewards
frequently refreshed theorems.                                      (RLVR) paradigm, introduced in [21], [48], [59], currently
                                                                    relies on exact-match graders for final answers (G SM 8K,
C. Reasoning Efficiency and Open Models
                                                                    M ATH, A IME) and for formal-proof completion (Lean).
   Frontier reasoning models today require tens of thousands        Extending this paradigm to proof quality, generalizability of
of output tokens per non-trivial problem. Substantial academic      a solution strategy, and economy of argument remains an
and industrial effort is therefore directed at reasoning effi-      important open problem. The PRM literature [90]–[92] offers
ciency: distilled models that retain most of the capability at a    partial answers, but a principled theory of step-level reward
fraction of the compute; methods for adaptive reasoning bud-        modeling is still lacking.
gets that deliberate only as long as necessary; and open-weight           Curriculum and difficulty scheduling: The effectiveness
models that democratize research access. The DeepSeek-R1-           of RLVR depends not only on the reward signal but also on
Distill series, Gemma-Math, and Qwen-Math-RL lines demon-           the distribution of training problems. W IZARD M ATH [167]
strate that strong reasoning need not be confined to frontier-lab   applies iterative difficulty amplification; M ETA M ATH [165]
APIs; this is likely to become a central axis of competition.       uses backward question rewriting; D EEP T HEOREM [203] fil-
                                                                    ters for difficulty ≥ 5 and constructs entailing/contradictory
D. Multi-Agent Orchestration                                        theorem variants to ensure non-trivial binary rewards. More
   The next generation of multi-agent mathematical systems          systematic curriculum design, scheduling problem difficulty to
should move beyond generic debate toward role- and domain-          match the model’s current capability, progressively introducing
aware orchestration: one agent searches for invariants, another     formal constraints, and balancing domain coverage, remains
writes executable checks, another attempts a formalization,         underexplored. The RL literature outside NLP offers relevant
another critiques hidden assumptions, and a router allocates        frameworks (self-paced learning, automatic curriculum genera-
budget dynamically. G RAPH - OF -AGENTS suggests that select-       tion, regret-based task selection), but their adaptation to mathe-
ing a small, relevant subgraph can outperform using every           matical reasoning training at the scale of millions of problems
available agent [65]; MAG IC O R E and MALT suggest that            is an open engineering and research challenge. Getting this
reviewer and verifier roles can be converted into training          right could substantially reduce the compute required for
signal [64], [161]. The open problem is credit assignment:          reasoning-model training, which is itself a significant access
when a multi-agent solve succeeds, which agent, message, or         and sustainability concern (Section X).
verification step deserves the learning signal?
                                                                    H. Reasoning Robustness and Uncertainty
E. Multilingual and Localized Reasoning                                The GSM-Symbolic results highlight the continued lack of
   The next wave of mathematical-reasoning benchmarks               robust reasoning under surface perturbation, particularly under
should be multilingual by design rather than translated only        the introduction of irrelevant information. Work on calibrated
after English saturation. The key research questions are            uncertainty for reasoning models, abstention under ambiguity,
whether models can reason in the user’s language, whether           and adversarial robustness via data augmentation represents an
they silently translate through English, whether code-switched      essential complement to raw-accuracy scaling. The emergence
rationales improve or damage reliability, and whether local         of benchmarks like MathCheck and Putnam-AXIOM [259]
textbook distributions are represented. Resources such as           gives the community the measurement instruments required
HRM8K, PATI G ONIT, BMWP, M ATH M IST, P OLY M ATH,                 to track this axis.
I. Community Infrastructure for Formalization                         mutandis to Isabelle, Coq/Rocq, and emerging assistants; we
   Finally, as Tao [29], [202] has repeatedly emphasized, the         expect that the specific systems will be displaced more rapidly
bottleneck for AI-assisted formalization is no longer model           than the structural picture, and that future iterations of this
capability alone but community infrastructure: the formal             survey will rename the actors without significantly altering
libraries required to state and prove research-level results,         the script.
the lightweight tooling that makes Lean approachable for
early-career mathematicians, and the cultural acceptance of                                XIII. C ONCLUSION
formalization as a legitimate mode of mathematical work.
Reducing the de Bruijn factor below one would change                     The six decades of research surveyed here take us from
formalization from a costly after-the-fact certificate into a         W ORD P RO’s four hand-crafted schemata for single-step arith-
productivity multiplier. Initiatives such as the Lean FRO,            metic in Interlisp-D [38] to an advanced version of Gemini
the Lean Focused Research Organization, and the mathlib               Deep Think producing five perfect IMO 2025 solutions in
community’s expansion to undergraduate curricula represent            natural language within the competition’s own 4.5-hour time
the kind of investment that will determine whether AI-for-            limit [179]. We have organized this progression along four
mathematics becomes a narrow technical specialty or a broadly         axes, informal text, multimodal, formal, and discovery, each
transformative tool. Microgrants for postdocs and graduate            with its own characteristic methods, datasets, and triumphs.
students in formalization, structured visiting programs at for-          If there is a single thread running through this history,
malization hubs, and teaching material integrating Lean with          it is that every expansion of AI mathematical reasoning
standard curricula are concrete levers for the community to           capability has been made possible by a corresponding ex-
pull.                                                                 pansion of supervision. Rule-based systems were supervised
J. Evaluation Protocols for Assisted Mathematics                      by grammarians. Statistical MWP solvers were supervised by
                                                                      equation templates. Seq2Tree neural networks were supervised
   The next generation of evaluations should measure not only         by prefix-notation expressions. LLM-based reasoners were su-
whether a model can answer a fixed problem, but whether it            pervised first by chain-of-thought exemplars, then by process
improves the productivity of a mathematically competent user.         reward models, and most recently by the deterministic grader
Such protocols should record the division of labor between            of Lean 4. Each successive supervisor is richer than the last:
human and model, the number of failed attempts, whether               Lean does not merely tell the model that an answer is correct,
the model searched the literature, whether the final proof was        it certifies why.
formalized, and how much expert editing was required. This
                                                                         In this light, the near-term future seems clear. The supervi-
is especially important for open-problem claims, where the
                                                                      sor of tomorrow is not a single model but a pipeline — often a
distinction between rediscovery, literature retrieval, heuristic
                                                                      small team of specialized agents, in which LLMs propose,
suggestion, and autonomous proof generation determines the
                                                                      critics and tools filter, autoformalizers translate, and Lean
scientific meaning of the result.
                                                                      verifies. The mathematician’s role is neither to be replaced
                      XII. L IMITATIONS                               by this pipeline nor to operate beside it as a passive equal, but
   This survey covers a rapidly moving field in which frontier        to direct it: choosing problems, deciding which angles deserve
results are often first reported through technical reports, bench-    pursuit, and, crucially, integrating the formal output back into
mark websites, public demonstrations, or project repositories         the informal discourse that remains the medium of mathemat-
rather than peer-reviewed publications. We therefore annotate         ical understanding. The primetime that Tao [29] forecast in
source status where possible, but some post-2024 results              early 2026 is not one in which AI replaces mathematicians,
remain difficult to compare because complete model details,           but one in which the distance between a good research idea
inference budgets, tool access, and verifier settings are not         and a verified theorem becomes substantially shorter, and in
always public. The performance tables aggregate numbers               which open problems that once required decades of sustained
reported under heterogeneous protocols, greedy decoding,              effort may, in some cases, yield to weeks of human-AI
majority voting, pass@k, tool-augmented inference, learned            collaboration. The practical, philosophical, and infrastructural
reranking, expert formalization, and proof-assistant feedback,        questions raised by this shift deserve the community’s best
so they should be read as a structured map of the literature          attention over the coming years.
rather than as a strictly controlled leaderboard. Similarly,
open-problem and discovery claims require special care: a                                ACKNOWLEDGEMENTS
reported AI contribution may range from literature retrieval or
candidate generation to fully formalized proof production, and           We convey our heartfelt gratitude, in advance, to the anony-
only the latter provides a strong correctness certificate. Finally,   mous reviewers for their constructive criticisms and insightful
although the survey emphasizes Lean 4 because of its current          feedback, which will surely be conducive to the improvement
centrality in AI-for-mathematics, the supervision-ladder anal-        of the research work outlined in this paper. Syed Rifat Raiyan,
ysis, the comprehension–generation–verification triad, and the        in particular, wishes to thank his parents, Syed Sirajul Islam
discovery-vs-verification division of labor all apply mutatis         and Kazi Shahana Begum, for everything.
                             R EFERENCES                                          [23] P.-Y. Wang, T.-S. Liu, C. Wang, Z. Li, Y. Wang, S. Yan, C. Jia, X.-H.
                                                                                       Liu, X. Chen, J. Xu, and Y. Yu, “A survey on large language models
 [1] E. A. Feigenbaum, J. Feldman, et al., Computers and thought. New                  for mathematical reasoning,” ACM Computing Surveys, vol. 58, no. 8,
     York: McGraw-Hill, 1963.                                                          2026.
 [2] D. G. Bobrow, Natural Language Input for a Computer Problem                  [24] Y. Yan, J. Su, J. He, F. Fu, X. Zheng, Y. Lyu, K. Wang, S. Wang,
     Solving System. PhD thesis, Massachusetts Institute of Technology,                Q. Wen, and X. Hu, “A survey of mathematical reasoning in the era of
     Cambridge, MA, 1964.                                                              multimodal large language model: Benchmark, method & challenges,”
 [3] J. Peterson, R. Pihl, D. Higgins, J. Séguin, and R. Tremblay, “Neu-              in Findings of the Association for Computational Linguistics: ACL
     ropsychological performance, iq, personality, and grades in a longi-              2025, pp. 11798–11827, 2025.
     tudinal grade-school male sample,” Individual Differences Research,          [25] T. Guo, X. Chen, Y. Wang, R. Chang, S. Pei, N. V. Chawla, O. Wiest,
     vol. 1, pp. 159–172, 2003.                                                        and X. Zhang, “Large language model based multi-agents: A survey
 [4] S. Kingsdorf and J. Krawec, “A broad look at the literature on                    of progress and challenges,” arXiv preprint arXiv:2402.01680, 2024.
     math word problem-solving interventions for third graders,” Cogent           [26] K. Yang, G. Poesia, J. He, W. Li, K. Lauter, S. Chaudhuri, and D. Song,
     Education, vol. 3, no. 1, p. 1135770, 2016.                                       “Formal mathematical reasoning: A new frontier in AI,” arXiv preprint
 [5] P. Lu, R. Gong, S. Jiang, L. Qiu, S. Huang, X. Liang, and S.-C.                   arXiv:2412.16075, 2024.
     Zhu, “Inter-GPS: Interpretable geometry problem solving with formal          [27] Z. Li, J. Sun, L. Murphy, Q. Su, Z. Li, X. Zhang, K. Yang, and X. Si, “A
     language and symbolic reasoning,” arXiv preprint arXiv:2105.04165,                survey on deep learning for theorem proving,” Conference on Language
     2021.                                                                             Modeling (COLM), 2024.
 [6] L. d. Moura and S. Ullrich, “The lean 4 theorem prover and pro-              [28] T. Tao, “AI will become mathematicians’ co-pilot.” Scientific American
     gramming language,” in Automated Deduction – CADE 28 (A. Platzer                  Interview, 2024.
     and G. Sutcliffe, eds.), (Cham), pp. 625–635, Springer International         [29] T. Tao, “AI is ready for primetime in math and theoretical physics.”
     Publishing, 2021.                                                                 IPAM talk, reported by OpenAI Academy, 2026.
 [7] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P.                [30] T. Klowden and T. Tao, “Mathematical methods and human thought
     Kumar, E. Dupont, F. J. Ruiz, J. S. Ellenberg, P. Wang, O. Fawzi, et al.,         in the age of AI,” arXiv preprint, 2026. To appear in Blackwell
     “Mathematical discoveries from program search with large language                 Companion to the Philosophy of Mathematics.
     models,” Nature, vol. 625, pp. 468–475, 2024.                                [31] B. Kitchenham and S. Charters, “Guidelines for performing systematic
 [8] A. Novikov, N. Vũ, M. Eisenberger, E. Dupont, P.-S. Huang, A. Z.                 literature reviews in software engineering,” Tech. Rep. EBSE-2007-01,
     Wagner, S. Shirobokov, B. Kozlovskii, et al., “AlphaEvolve: A cod-                Keele University and Durham University, 2007.
     ing agent for scientific and algorithmic discovery,” arXiv preprint          [32] L. Gao, A. Madaan, S. Zhou, U. Alon, P. Liu, Y. Yang, J. Callan, and
     arXiv:2506.13131, 2025.                                                           G. Neubig, “PAL: Program-aided language models,” in ICML, 2023.
 [9] Y. Wu, A. Q. Jiang, W. Li, M. Rabe, C. Staats, M. Jamnik, and                [33] W. Chen, X. Ma, X. Wang, and W. W. Cohen, “Program of thoughts
     C. Szegedy, “Autoformalization with large language models,” NeurIPS,              prompting: Disentangling computation from reasoning for numerical
     vol. 35, pp. 32353–32368, 2022.                                                   reasoning tasks,” TMLR, 2023.
[10] A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix,   [34] Z. Gou, Z. Shao, Y. Gong, Y. Shen, Y. Yang, M. Huang, N. Duan, and
     Y. Wu, and G. Lample, “Draft, sketch, and prove: Guiding formal                   W. Chen, “ToRA: A tool-integrated reasoning agent for mathematical
     theorem provers with informal proofs,” ICLR, 2023.                                problem solving,” in ICLR, 2024.
[11] E. P. White, “Erd\h {o} s’ minimum overlap problem,” arXiv preprint          [35] J. Chen, J. Tang, J. Qin, X. Liang, L. Liu, E. P. Xing, and L. Lin,
     arXiv:2201.05704, 2022.                                                           “GeoQA: A geometric question answering benchmark towards multi-
[12] A. Patel, S. Bhattamishra, and N. Goyal, “Are nlp models really able to           modal numerical reasoning,” arXiv preprint arXiv:2105.14517, 2021.
     solve simple math word problems?,” arXiv preprint arXiv:2103.07191,          [36] J. Gao, R. Pi, J. Zhang, J. Ye, W. Zhong, Y. Wang, L. Hong, J. Han,
     2021.                                                                             H. Xu, Z. Li, and L. Kong, “G-LLaVA: Solving geometric problem with
[13] I. Mirzadeh, K. Alizadeh, H. Shahrokhi, O. Tuzel, S. Bengio, and                  multi-modal large language model,” arXiv preprint arXiv:2312.11370,
     M. Farajtabar, “GSM-Symbolic: Understanding the limitations of                    2023.
     mathematical reasoning in large language models,” arXiv preprint             [37] H. Xin, D. Guo, Z. Shao, Z. Ren, Q. Zhu, B. Liu, C. Ruan, W. Li,
     arXiv:2410.05229, 2024.                                                           and X. Liang, “DeepSeek-Prover: Advancing theorem proving in LLMs
[14] K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song, S. Yu,                        through large-scale synthetic data,” arXiv preprint arXiv:2405.14333,
     S. Godil, R. Prenger, and A. Anandkumar, “LeanDojo: Theorem prov-                 2024.
     ing with retrieval-augmented language models,” in NeurIPS Datasets           [38] C. R. Fletcher, “Understanding and solving arithmetic word problems:
     and Benchmarks Track, 2023.                                                       A computer simulation,” Behavior Research Methods, Instruments, &
[15] A. Mukherjee and U. Garain, “A review of methods for automatic                    Computers, vol. 17, no. 5, pp. 565–571, 1985.
     understanding of natural language mathematical problems,” Artificial         [39] M. J. Hosseini, H. Hajishirzi, O. Etzioni, and N. Kushman, “Learning to
     Intelligence Review, vol. 29, no. 2, pp. 93–122, 2008.                            solve arithmetic word problems with verb categorization,” in EMNLP,
[16] S. Mandal and S. K. Naskar, “Solving arithmetic mathematical word                 2014.
     problems: A review and recent advancements,” in Information Tech-            [40] N. Kushman, Y. Artzi, L. Zettlemoyer, and R. Barzilay, “Learning
     nology and Applied Mathematics (P. Chandra, D. Giri, F. Li, S. Kar,               to automatically solve algebra word problems,” in Proceedings of the
     and D. K. Jana, eds.), (Singapore), pp. 95–114, Springer Singapore,               52nd Annual Meeting of the Association for Computational Linguistics
     2019.                                                                             (Volume 1: Long Papers), pp. 271–281, 2014.
[17] D. Zhang, L. Wang, L. Zhang, B. T. Dai, and H. T. Shen, “The gap of          [41] Y. Wang, X. Liu, and S. Shi, “Deep neural solver for math word
     semantic parsing: A survey on automatic math word problem solvers,”               problems,” in EMNLP, pp. 845–854, 2017.
     IEEE Transactions on Pattern Analysis and Machine Intelligence,              [42] Z. Xie and S. Sun, “A goal-driven tree-structured neural model for
     vol. 42, no. 9, pp. 2287–2305, 2020.                                              math word problems,” in IJCAI, pp. 5299–5305, 2019.
[18] S. S. Sundaram, S. Gurajada, M. Fisichella, S. S. Abraham, et al., “Why      [43] J. Zhang, L. Wang, R. K.-W. Lee, Y. Bin, Y. Wang, J. Shao, and E.-
     are nlp models fumbling at elementary math? a survey of deep learning             P. Lim, “Graph-to-tree learning for solving math word problems,” in
     based word problem solvers,” arXiv preprint arXiv:2205.15683, 2022.               ACL, 2020.
[19] P. Lu, L. Qiu, W. Yu, S. Welleck, and K.-W. Chang, “A survey of deep         [44] J. Shen, Y. Yin, L. Li, L. Shang, X. Jiang, M. Zhang, and Q. Liu,
     learning for mathematical reasoning,” ACL, 2023.                                  “Generate & rank: A multi-task framework for math word problems,”
[20] J. Ahn, R. Verma, R. Lou, D. Liu, R. Zhang, and W. Yin, “Large lan-               arXiv preprint arXiv:2109.03034, 2021.
     guage models for mathematical reasoning: Progresses and challenges,”         [45] Z. Liang, J. Zhang, J. Shao, and X. Zhang, “MWP-BERT: A strong
     in EACL Student Research Workshop, 2024.                                          baseline for math word problems,” arXiv preprint arXiv:2107.13435,
[21] OpenAI, “Learning to reason with LLMs,” tech. rep., OpenAI, 2024.                 2021.
     https://openai.com/index/learning-to-reason-with-llms/.                      [46] Z. Jie, J. Li, and W. Lu, “Learning to reason deductively: Math word
[22] W. Liu, H. Hu, J. Zhou, Y. Ding, J. Li, J. Zeng, M. He, Q. Chen,                  problem solving as complex relation extraction,” in Proceedings of the
     B. Jiang, A. Zhou, and L. He, “Mathematical language models: A                    60th Annual Meeting of the Association for Computational Linguistics
     survey,” ACM Computing Surveys, vol. 58, no. 6, 2025.                             (Volume 1: Long Papers), pp. 5944–5955, 2022.
[47] A. Lewkowycz, A. Andreassen, D. Dohan, E. Dyer, H. Michalewski,            [68] T. H. Trinh, Y. Wu, Q. V. Le, H. He, and T. Luong, “Solving olympiad
     V. Ramasesh, A. Slone, C. Anil, I. Schlag, T. Gutman-Solo, et al.,              geometry without human demonstrations,” Nature, vol. 625, pp. 476–
     “Solving quantitative reasoning problems with language models,”                 482, 2024.
     NeurIPS, vol. 35, pp. 3843–3857, 2022.                                     [69] Y. Chervonyi, T. H. Trinh, M. Olšák, X. Yang, H. H. Nguyen, M. Mene-
[48] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang,                      gali, J. Jung, J. Kim, V. Verma, Q. V. Le, and T. Luong, “Gold-medalist
     M. Zhang, Y. Li, Y. Wu, et al., “DeepSeekMath: Pushing the limits               performance in solving olympiad geometry with alphageometry2,”
     of mathematical reasoning in open language models,” arXiv preprint              Journal of Machine Learning Research, vol. 26, no. 241, pp. 1–39,
     arXiv:2402.03300, 2024.                                                         2025.
[49] A. Yang, B. Zhang, B. Hui, B. Gao, B. Yu, C. Li, D. Liu, J. Tu, J. Zhou,   [70] P. Lu, H. Bansal, T. Xia, J. Liu, C. Li, H. Hajishirzi, H. Cheng, K.-W.
     J. Lin, et al., “Qwen2.5-math technical report: Toward mathematical             Chang, M. Galley, and J. Gao, “MathVista: Evaluating mathematical
     expert model via self-improvement,” arXiv preprint arXiv:2409.12122,            reasoning of foundation models in visual contexts,” in ICLR, 2024.
     2024.                                                                      [71] R. Zhang, D. Jiang, Y. Zhang, H. Lin, Z. Guo, P. Qiu, A. Zhou, P. Lu,
[50] E. Zelikman, Y. Wu, J. Mu, and N. D. Goodman, “STaR: Bootstrapping              K.-W. Chang, Y. Qiao, and H. Li, “MathVerse: Does your multi-modal
     reasoning with reasoning,” NeurIPS, vol. 35, pp. 15476–15488, 2022.             LLM truly see the diagrams in visual math problems?,” in ECCV, 2024.
[51] X. Guan, L. L. Zhang, Y. Liu, N. Shang, Y. Sun, Y. Zhu, F. Yang, and       [72] K. Wang, J. Pan, W. Shi, Z. Lu, M. Zhan, and H. Li, “Measuring
     M. Yang, “rStar-Math: Small LLMs can master math reasoning with                 multimodal mathematical reasoning with MATH-vision dataset,” in
     self-evolved deep thinking,” in Proceedings of the 42nd International           NeurIPS Datasets and Benchmarks Track, 2024.
     Conference on Machine Learning, vol. 267 of Proceedings of Machine         [73] R. Zhang, X. Wei, D. Jiang, Y. Zhang, Z. Guo, C. Tong, J. Liu, A. Zhou,
     Learning Research, PMLR, 2025.                                                  B. Wei, S. Zhang, et al., “MAVIS: Mathematical visual instruction
                                                                                     tuning,” arXiv preprint arXiv:2407.08739, 2024.
[52] Y. Ye, Z. Huang, Y. Xiao, E. Chern, S. Xia, and P. Liu, “LIMO: Less
                                                                                [74] X. Chen, R. Zhang, D. Jiang, A. Zhou, S. Yan, W. Lin, and H. Li,
     is more for reasoning,” arXiv preprint arXiv:2502.03387, 2025.
                                                                                     “MINT-CoT: Enabling interleaved visual tokens in mathematical chain-
[53] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi,            of-thought reasoning,” arXiv preprint arXiv:2506.05331, 2025.
     Q. Le, and D. Zhou, “Chain-of-thought prompting elicits reasoning in       [75] S. Polu and I. Sutskever, “Generative language modeling for automated
     large language models,” NeurIPS, vol. 35, pp. 24824–24837, 2022.                theorem proving,” arXiv preprint arXiv:2009.03393, 2020.
[54] X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowd-        [76] P. Song, K. Yang, and A. Anandkumar, “Lean Copilot: Large language
     hery, and D. Zhou, “Self-consistency improves chain of thought rea-             models as copilots for theorem proving in Lean,” arXiv preprint
     soning in language models,” in ICLR, 2023.                                      arXiv:2404.12534, 2024.
[55] Q. Zhong, K. Wang, Z. Xu, J. Liu, L. Ding, B. Du, and D. Tao,              [77] A. Ospanov, F. Farnia, and R. Mohit, “APOLLO: Automated LLM and
     “Achieving >97% on GSM8K: Deeply understanding the problems                     Lean collaboration for advanced formal reasoning,” Advances in Neural
     makes LLMs better solvers for math word problems,” arXiv preprint               Information Processing Systems, vol. 38, pp. 41599–41633, 2026.
     arXiv:2404.14963, 2024.                                                    [78] E. First, M. N. Rabe, T. Ringer, and Y. Brun, “Baldur: Whole-proof
[56] S. Yao, D. Yu, J. Zhao, I. Shafran, T. L. Griffiths, Y. Cao, and                generation and repair with large language models,” in Proceedings of
     K. Narasimhan, “Tree of thoughts: Deliberate problem solving with               the 31st ACM Joint European Software Engineering Conference and
     large language models,” NeurIPS, vol. 36, 2023.                                 Symposium on the Foundations of Software Engineering, (New York,
[57] D. Zhou, N. Schärli, L. Hou, J. Wei, N. Scales, X. Wang, D. Schu-              NY, USA), pp. 1229–1241, Association for Computing Machinery,
     urmans, C. Cui, O. Bousquet, Q. Le, and E. Chi, “Least-to-most                  2023.
     prompting enables complex reasoning in large language models,” in          [79] Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao, L. Zhang,
     ICLR, 2023.                                                                     Z. Fu, Q. Zhu, D. Yang, et al., “DeepSeek-Prover-V2: Advancing
[58] M. Besta, N. Blach, A. Kubicek, R. Gerstenberger, M. Podstawski,                formal mathematical reasoning via reinforcement learning for subgoal
     L. Gianinazzi, J. Gajda, T. Lehmann, H. Niewiadomski, P. Nyczyk,                decomposition,” arXiv preprint arXiv:2504.21801, 2025.
     et al., “Graph of thoughts: Solving elaborate problems with large          [80] H. Wang et al., “Kimina-Prover Preview: Towards large for-
     language models,” in Proceedings of the AAAI conference on artificial           mal reasoning models with reinforcement learning,” arXiv preprint
     intelligence, vol. 38, pp. 17682–17690, 2024.                                   arXiv:2504.11354, 2025.
[59] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu,               [81] H. Ying, Z. Wu, Y. Geng, J. Wang, D. Lin, and K. Chen, “Lean
     S. Ma, P. Wang, X. Bi, et al., “DeepSeek-R1: Incentivizing reason-              Workbook: A large-scale Lean problem set formalized from natural
     ing capability in LLMs via reinforcement learning,” arXiv preprint              language math problems,” NeurIPS Datasets and Benchmarks Track,
     arXiv:2501.12948, 2025.                                                         2024.
[60] Kimi Team, “Kimi k1.5: Scaling reinforcement learning with LLMs,”          [82] J. Lu, Y. Wan, Z. Liu, Y. Huang, J. Xiong, C. Liu, J. Shen, H. Jin,
     arXiv preprint arXiv:2501.12599, 2025.                                          J. Zhang, H. Wang, et al., “Process-driven autoformalization in Lean
[61] N. Muennighoff, Z. Yang, W. Shi, X. L. Li, L. Fei-Fei, H. Hajishirzi,           4,” arXiv preprint arXiv:2406.01940, 2024.
     L. Zettlemoyer, P. Liang, E. Candès, and T. Hashimoto, “s1: Simple        [83] X. Liu, Z. Xie, A. Moeini, C. Chen, S. D. Liu, Y. Meng, A. Zhang, and
     test-time scaling,” arXiv preprint arXiv:2501.19393, 2025.                      S. Zhang, “MathlibLemma: Folklore lemma generation and benchmark
                                                                                     for formal mathematics,” arXiv preprint arXiv:2602.02561, 2026.
[62] Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch, “Improv-
                                                                                [84] The mathlib Community, “The Lean mathematical library.” https://
     ing factuality and reasoning in language models through multiagent
                                                                                     leanprover-community.github.io/mathlib4 docs/, 2020. Accessed April
     debate,” arXiv preprint arXiv:2305.14325, 2023.
                                                                                     2026.
[63] J. C.-Y. Chen, S. Saha, and M. Bansal, “ReConcile: Round-table             [85] T. Hubert, R. Mehta, L. Sartran, M. Z. Horvath, G. Zuzic, et al.,
     conference improves reasoning via consensus among diverse LLMs,”                “Olympiad-level formal mathematical reasoning with reinforcement
     in ACL, 2024.                                                                   learning,” Nature, vol. 651, pp. 607–613, 2026.
[64] J. C.-Y. Chen, A. Prasad, S. Saha, E. Stengel-Eskin, and M. Bansal,        [86] H. Lin, Z. Sun, Y. Yang, and S. Welleck, “Lean-STaR: Learning to
     “MAgICoRe: Multi-agent, iterative, coarse-to-fine refinement for rea-           interleave thinking and proving,” in ICLR, 2025.
     soning,” in EMNLP, 2025.                                                   [87] G. Lample, T. Lacroix, M.-A. Lachaux, A. Rodriguez, A. Hayat,
[65] S. Yun, J. Peng, P. Li, W. Fan, J. Chen, J. Zou, G. Li, and T. Chen,            T. Lavril, G. Ebner, and X. Martinet, “Hypertree proof search for
     “Graph-of-agents: A graph-based framework for multi-agent LLM                   neural theorem proving,” in Advances in Neural Information Processing
     collaboration,” in ICLR, 2026.                                                  Systems, vol. 35, pp. 26337–26349, 2022.
[66] B. Ping, M. Luo, Z. Dang, C. Wang, and C. Jia, “Autogps: Automated         [88] T.     Bloom,      “The    Erdős    problems     website.”   https : / /
     geometry problem solving via multimodal formalization and deductive             www.erdosproblems.com/, 2024.
     reasoning,” arXiv preprint arXiv:2505.23381, 2025.                         [89] B. Alexeev et al., “AI contributions to Erdős problems (community
[67] X. Zhang, Y. Li, N. Zhu, C. Qin, Z. Zeng, and T. Leng, “FGeo-                   wiki).” https://github.com/teorth/erdosproblems/wiki/AI-contributions-
     HyperGNet: Geometric problem solving integrating FormalGeo sym-                 to-Erd%C5%91s-problems, 2026.
     bolic system and hypergraph neural network,” in Proceedings of the         [90] H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee,
     Thirty-Fourth International Joint Conference on Artificial Intelligence,        J. Leike, J. Schulman, I. Sutskever, and K. Cobbe, “Let’s verify step
     pp. 4733–4741, 2025.                                                            by step,” ICLR, 2024.
 [91] P. Wang, L. Li, Z. Shao, R. Xu, D. Dai, Y. Li, D. Chen, Y. Wu,             [116] S. Upadhyay, M.-W. Chang, K.-W. Chang, and W.-t. Yih, “Learning
      and Z. Sui, “Math-Shepherd: Verify and reinforce LLMs step-by-step               from explicit and implicit supervision jointly for algebra word prob-
      without human annotations,” in ACL, 2024.                                        lems,” in EMNLP, pp. 297–306, 2016.
 [92] L. Luo, Y. Liu, R. Liu, S. Phatale, H. Lara, Y. Li, L. Shu, Y. Zhu,        [117] M. Collins, “Discriminative training methods for hidden markov mod-
      L. Meng, J. Sun, and A. Rastogi, “Improve mathematical reasoning                 els: Theory and experiments with perceptron algorithms,” in EMNLP,
      in language models by automated process supervision,” arXiv preprint             pp. 1–8, 2002.
      arXiv:2406.06592, 2024.                                                    [118] D. Huang, S. Shi, C.-Y. Lin, and J. Yin, “Learning fine-grained
 [93] K. Cobbe, V. Kosaraju, M. Bavarian, J. Hilton, R. Nakano, C. Hesse,              expressions to solve math word problems,” in EMNLP, pp. 805–814,
      and J. Schulman, “Training verifiers to solve math word problems,”               2017.
      arXiv preprint arXiv:2110.14168, 2021.                                     [119] J. Chung, C. Gulcehre, K. Cho, and Y. Bengio, “Empirical evaluation of
 [94] Y. Bakman, “Robust understanding of word problems with extraneous                gated recurrent neural networks on sequence modeling,” arXiv preprint
      information,” arXiv preprint math/0701393, 2007.                                 arXiv:1412.3555, 2014.
 [95] M. Yuhui, Z. Ying, C. Guangzuo, R. Yun, and H. Ronghuai, “Frame-           [120] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural
      based calculus of solving arithmetic multi-step addition and subtraction         Computation, vol. 9, no. 8, pp. 1735–1780, 1997.
      word problems,” in 2010 Second International Workshop on Education         [121] P. Mishra, L. J. Kurisinkel, D. M. Sharma, and V. Varma, “Equgener: A
      Technology and Computer Science, vol. 2, pp. 476–479, IEEE, 2010.                reasoning network for word problem solving by generating arithmetic
 [96] S. Roy, T. Vieira, and D. Roth, “Reasoning about quantities in natural           equations,” in PACLIC, 2018.
      language,” Transactions of the Association for Computational Linguis-      [122] J. Pennington, R. Socher, and C. D. Manning, “Glove: Global vectors
      tics, vol. 3, pp. 1–13, 2015.                                                    for word representation,” in EMNLP, pp. 1532–1543, 2014.
 [97] L. Zhou, S. Dai, and L. Chen, “Learn to solve algebra word problems        [123] L. Wang, D. Zhang, L. Gao, J. Song, L. Guo, and H. T. Shen,
      using quadratic programming,” in Proceedings of the 2015 Conference              “MathDQN: Solving arithmetic word problems via deep reinforcement
      on Empirical Methods in Natural Language Processing, pp. 817–822,                learning,” in AAAI, 2018.
      2015.                                                                      [124] D. Huang, J. Liu, C.-Y. Lin, and J. Yin, “Neural math word problem
 [98] A. Mitra and C. Baral, “Learning to use formulas to solve simple                 solver with reinforcement learning,” in COLING, pp. 213–223, 2018.
      arithmetic problems,” in Proceedings of the 54th Annual Meeting of the     [125] J. Li, L. Wang, J. Zhang, Y. Wang, B. T. Dai, and D. Zhang, “Modeling
      Association for Computational Linguistics (Volume 1: Long Papers),               intra-relation in math word problems with different functional multi-
      pp. 2144–2153, 2016.                                                             head attentions,” in ACL, pp. 6162–6167, 2019.
 [99] C.-C. Liang, K.-Y. Hsu, C.-T. Huang, C.-M. Li, S.-Y. Miao, and K.-Y.       [126] L. Wang, D. Zhang, J. Zhang, X. Xu, L. Gao, B. T. Dai, and H. T. Shen,
      Su, “A tag-based english math word problem solver with understanding,            “Template-based math word problem solvers with recursive neural
      reasoning and explanation,” in NAACL Demonstrations, pp. 67–71,                  networks,” in AAAI, vol. 33, pp. 7144–7151, 2019.
      2016.                                                                      [127] Q. Liu, W. Guan, S. Li, and D. Kawahara, “Tree-structured decoding
[100] C.-C. Liang, S.-H. Tsai, T.-Y. Chang, Y.-C. Lin, and K.-Y. Su, “A                for solving math word problems,” in EMNLP-IJCNLP, pp. 2370–2379,
      meaning-based English math word problem solver with understanding,               2019.
      reasoning and explanation,” in COLING 2016 Demonstrations, 2016.           [128] Y. Meng and A. Rumshisky, “Solving math word problems with
[101] S. Roy and D. Roth, “Solving general arithmetic word problems,” arXiv            double-decoder transformer,” arXiv preprint arXiv:1908.10924, 2019.
      preprint arXiv:1608.01413, 2016.                                           [129] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “BERT: Pre-
[102] S. Roy and D. Roth, “Illinois math solver: Math reasoning on the web,”           training of deep bidirectional transformers for language understanding,”
      in NAACL Demonstrations, pp. 52–56, 2016.                                        in NAACL-HLT, 2019.
[103] R. Koncel-Kedziorski, H. Hajishirzi, A. Sabharwal, O. Etzioni, and         [130] S. Yun, M. Jeong, R. Kim, J. Kang, and H. J. Kim, “Graph transformer
      S. D. Ang, “Parsing algebraic word problems into equations,” Transac-            networks,” NeurIPS, vol. 32, 2019.
      tions of the Association for Computational Linguistics, vol. 3, pp. 585–   [131] D. Cai and W. Lam, “Graph transformer for graph-to-sequence learn-
      597, 2015.                                                                       ing,” in AAAI, vol. 34, pp. 7464–7471, 2020.
[104] S. Roy, S. Upadhyay, and D. Roth, “Equation parsing: Mapping               [132] S. Li, L. Wu, S. Feng, F. Xu, F. Xu, and S. Zhong, “Graph-to-
      sentences to grounded equations,” arXiv preprint arXiv:1609.08824,               tree neural networks for learning structured input-output translation
      2016.                                                                            with applications to semantic parsing and math word problem,” arXiv
[105] S. Roy and D. Roth, “Unit dependency graph and its application to                preprint arXiv:2004.13781, 2020.
      arithmetic word problem solving,” in AAAI, 2017.                           [133] Q. Liu, W. Guan, S. Li, F. Cheng, D. Kawahara, and S. Kurohashi,
[106] L. Wang, Y. Wang, D. Cai, D. Zhang, and X. Liu, “Translating a math              “Reverse operation based data augmentation for solving math word
      word problem to an expression tree,” arXiv preprint arXiv:1811.05632,            problems,” arXiv preprint arXiv:2010.01556, 2020.
      2018.                                                                      [134] Y. Hong, Q. Li, R. Gong, D. Ciao, S. Huang, and S.-C. Zhu, “Smart:
[107] T.-R. Chiang and Y.-N. Chen, “Semantically-aligned equation gener-               A situation model for algebra story problems via attributed grammar,”
      ation for solving and reasoning math word problems,” arXiv preprint              in AAAI, vol. 35, pp. 13009–13017, 2021.
      arXiv:1811.00720, 2018.                                                    [135] W. Kintsch and J. G. Greeno, “Understanding and solving word
[108] Y. Wu et al., “Google’s neural machine translation system: Bridging              arithmetic problems,” Psychological Review, vol. 92, no. 1, p. 109,
      the gap between human and machine translation,” arXiv preprint                   1985.
      arXiv:1609.08144, 2016.                                                    [136] B. Kim, K. S. Ki, D. Lee, and G. Gweon, “Point to the expression:
[109] J. Gehring, M. Auli, D. Grangier, D. Yarats, and Y. N. Dauphin,                  Solving algebraic word problems using the expression-pointer trans-
      “Convolutional sequence to sequence learning,” in ICML, 2017.                    former model,” in EMNLP, pp. 3768–3779, 2020.
[110] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N.           [137] Z. Lan, M. Chen, S. Goodman, K. Gimpel, P. Sharma, and R. Soricut,
      Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,”                “Albert: A lite bert for self-supervised learning of language represen-
      NeurIPS, vol. 30, 2017.                                                          tations,” arXiv preprint arXiv:1909.11942, 2019.
[111] S. Shi, Y. Wang, C.-Y. Lin, X. Liu, and Y. Rui, “Automatically solving     [138] Y. Shen and C. Jin, “Solving math word problems with multi-encoders
      number word problems by semantic parsing and reasoning,” in EMNLP,               and multi-decoders,” in COLING, pp. 2924–2934, 2020.
      pp. 1132–1142, 2015.                                                       [139] W. Hamilton, Z. Ying, and J. Leskovec, “Inductive representation
[112] N. Chomsky, “Three models for the description of language,” IRE                  learning on large graphs,” NeurIPS, vol. 30, 2017.
      Transactions on Information Theory, vol. 2, no. 3, pp. 113–124, 1956.      [140] Q. Wu, Q. Zhang, J. Fu, and X.-J. Huang, “A knowledge-aware
[113] D. Gildea and D. Jurafsky, “Automatic labeling of semantic roles,”               sequence-to-tree network for math word problem solving,” in EMNLP,
      Computational Linguistics, vol. 28, no. 3, pp. 245–288, 2002.                    pp. 7137–7146, 2020.
[114] Y. Zou and W. Lu, “Text2math: End-to-end parsing text into math            [141] J. Zhang, R. K.-W. Lee, E.-P. Lim, W. Qin, L. Wang, J. Shao, and
      expressions,” arXiv preprint arXiv:1910.06571, 2019.                             Q. Sun, “Teacher-student networks with multiple decoders for solving
[115] D. Huang, S. Shi, C.-Y. Lin, J. Yin, and W.-Y. Ma, “How well do                  math word problem,” in IJCAI, 2020.
      computers solve math word problems? large-scale dataset construction       [142] G. Hinton, O. Vinyals, J. Dean, et al., “Distilling the knowledge in a
      and evaluation,” in ACL, pp. 887–896, 2016.                                      neural network,” arXiv preprint arXiv:1503.02531, 2015.
[143] W. Yu, Y. Wen, F. Zheng, and N. Xiao, “Improving math word problems          [165] L. Yu, W. Jiang, H. Shi, J. Yu, Z. Liu, Y. Zhang, J. T. Kwok, Z. Li,
      with pre-trained knowledge and hierarchical reasoning,” in EMNLP,                  A. Weller, and W. Liu, “MetaMath: Bootstrap your own mathematical
      pp. 3384–3394, 2021.                                                               questions for large language models,” ICLR, 2024.
[144] Y. Hong, Q. Li, D. Ciao, S. Huang, and S.-C. Zhu, “Learning by fixing:       [166] X. Yue, X. Qu, G. Zhang, Y. Fu, W. Huang, H. Sun, Y. Su, and
      Solving math word problems with weak supervision,” in AAAI, 2021.                  W. Chen, “MAmmoTH: Building math generalist models through
[145] X. Lin, Z. Huang, H. Zhao, E. Chen, Q. Liu, H. Wang, and S. Wang,                  hybrid instruction tuning,” ICLR, 2024.
      “HMS: A hierarchical solver with dependency-enhanced understanding           [167] H. Luo, Q. Sun, C. Xu, P. Zhao, J. Lou, C. Tao, X. Geng, Q. Lin,
      for math word problem,” in AAAI, pp. 4232–4240, 2021.                              S. Chen, and D. Zhang, “WizardMath: Empowering mathematical
[146] J. Qin, X. Liang, Y. Hong, J. Tang, and L. Lin, “Neural-symbolic                   reasoning for large language models via reinforced evol-instruct,” arXiv
      solver for math word problems with auxiliary tasks,” arXiv preprint                preprint arXiv:2308.09583, 2023.
      arXiv:2107.01431, 2021.                                                      [168] J. Uesato, N. Kushman, R. Kumar, F. Song, N. Siegel, L. Wang,
[147] S. Huang, J. Wang, J. Xu, D. Cao, and M. Yang, “Recall and learn:                  A. Creswell, G. Irving, and I. Higgins, “Solving math word prob-
      A memory-augmented solver for math word problems,” arXiv preprint                  lems with process- and outcome-based feedback,” arXiv preprint
      arXiv:2109.13112, 2021.                                                            arXiv:2211.14275, 2022.
[148] M. Lewis, Y. Liu, N. Goyal, M. Ghazvininejad, A. Mohamed, O. Levy,           [169] C. Snell, J. Lee, K. Xu, and A. Kumar, “Scaling LLM test-time compute
      V. Stoyanov, and L. Zettlemoyer, “BART: Denoising sequence-to-                     optimally can be more effective than scaling model parameters,” arXiv
      sequence pre-training for natural language generation, translation, and            preprint arXiv:2408.03314, 2024.
      comprehension,” arXiv preprint arXiv:1910.13461, 2019.                       [170] Y. Li, R. Zhan, H. Zhang, et al., “Achieving gold-medal-level
[149] T. Brown et al., “Language models are few-shot learners,” NeurIPS,                 olympiad reasoning via simple and unified scaling,” arXiv preprint
      vol. 33, pp. 1877–1901, 2020.                                                      arXiv:2605.13301, 2026.
[150] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa, “Large              [171] T. Luong et al., “IMO-ProofBench: Towards Robust Mathematical
      language models are zero-shot reasoners,” NeurIPS, vol. 35, pp. 22199–             Reasoning,” arXiv preprint arXiv:2511.01846, 2025.
      22213, 2022.                                                                 [172] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Prox-
[151] D. Yang, T. Liu, D. Zhang, A. Simoulin, X. Liu, Y. Cao, Z. Teng,                   imal policy optimization algorithms,” arXiv preprint arXiv:1707.06347,
      X. Qian, G. Yang, J. Luo, and J. McAuley, “Code to think, think to                 2017.
      code: A survey on code-enhanced reasoning and reasoning-driven code          [173] Z. Li, T. Xu, Y. Zhang, Z. Lin, Y. Yu, R. Sun, and Z.-Q. Luo, “ReMax:
      intelligence in LLMs,” arXiv preprint arXiv:2502.19411, 2025.                      A simple, effective, and efficient reinforcement learning method for
[152] E. Zelikman, G. Harik, Y. Shao, V. Jayasiri, N. Haber, and N. D.                   aligning large language models,” in Proceedings of the 41st Interna-
      Goodman, “Quiet-STaR: Language models can teach themselves to                      tional Conference on Machine Learning (R. Salakhutdinov, Z. Kolter,
      think before speaking,” arXiv preprint arXiv:2403.09629, 2024.                     K. Heller, A. Weller, N. Oliver, J. Scarlett, and F. Berkenkamp, eds.),
[153] A. Hosseini, X. Yuan, N. Malkin, A. Courville, A. Sordoni, and                     vol. 235 of Proceedings of Machine Learning Research, (Vienna,
      R. Agarwal, “V-STaR: Training verifiers for self-taught reasoners,” in             Austria), pp. 29128–29163, PMLR, 2024.
      Proceedings of the 2024 Conference on Language Modeling, 2024.               [174] A. Ahmadian, C. Cremer, M. Gallé, M. Fadaee, J. Kreutzer, O. Pietquin,
[154] T. Q. Luong, X. Zhang, Z. Jie, P. Sun, X. Jin, and H. Li, “ReFT:                   A. Üstün, and S. Hooker, “Back to basics: Revisiting REINFORCE-
      Reasoning with reinforced fine-tuning,” in Proceedings of the 62nd                 style optimization for learning from human feedback in LLMs,” in
      Annual Meeting of the Association for Computational Linguistics                    Proceedings of the 62nd Annual Meeting of the Association for
      (Volume 1: Long Papers), pp. 7611–7633, 2024.                                      Computational Linguistics (Volume 1: Long Papers), pp. 12248–12267,
[155] A. Kumar, V. Zhuang, R. Agarwal, Y. Su, J. D. Co-Reyes, A. Singh,                  2024.
      K. Baumli, S. Iqbal, C. Bishop, R. Roelofs, L. M. Zhang, K. McKinney,        [175] J. Hu, J. K. Liu, H. Xu, and W. Shen, “REINFORCE++: An efficient
      D. Shrivastava, C. Paduraru, G. Tucker, D. Precup, F. Behbahani, and               RLHF algorithm with robustness to both prompt and reward models,”
      A. Faust, “Training language models to self-correct via reinforcement              arXiv preprint arXiv:2501.03262, 2025.
      learning,” arXiv preprint arXiv:2409.12917, 2024.                            [176] Q. Yu, Z. Zhang, R. Zhu, Y. Yuan, X. Zuo, Y. Yue, W. Dai, T. Fan,
[156] T. Liang, Z. He, W. Jiao, X. Wang, Y. Wang, R. Wang, Y. Yang, S. Shi,              G. Liu, L. Liu, X. Liu, H. Lin, Z. Lin, B. Ma, G. Sheng, Y. Tong,
      and Z. Tu, “Encouraging divergent thinking in large language models                C. Zhang, M. Zhang, W. Zhang, H. Zhu, J. Zhu, J. Chen, J. Chen,
      through multi-agent debate,” in EMNLP, 2024.                                       C. Wang, H. Yu, Y. Song, X. Wei, H. Zhou, J. Liu, W.-Y. Ma, Y.-Q.
[157] Z. Liu, Y. Zhang, P. Li, Y. Liu, and D. Yang, “A dynamic LLM-powered               Zhang, L. Yan, M. Qiao, Y. Wu, and M. Wang, “DAPO: An open-
      agent network for task-oriented agent collaboration,” Conference on                source LLM reinforcement learning system at scale,” in NeurIPS, 2025.
      Language Modeling (COLM), 2024.                                              [177] R. Rafailov, A. Sharma, E. Mitchell, S. Ermon, C. D. Manning, and
[158] J. Wang, J. Wang, B. Athiwaratkun, C. Zhang, and J. Zou, “Mixture-                 C. Finn, “Direct preference optimization: Your language model is
      of-agents enhances large language model capabilities,” arXiv preprint              secretly a reward model,” in NeurIPS, 2023.
      arXiv:2406.04692, 2024.                                                      [178] X. Lai, Z. Tian, Y. Chen, S. Yang, X. Peng, and J. Jia, “Step-DPO:
[159] D. Zheng, I. von Glehn, Y. Zwols, I. Beloshapka, L. Buesing, D. M.                 Step-wise preference optimization for long-chain reasoning of LLMs,”
      Roy, M. Wattenberg, B. Georgiev, T. Schmidt, A. Cowie, F. Viegas,                  arXiv preprint arXiv:2406.18629, 2024.
      D. Kanevsky, V. Kahlon, H. Maennel, S. Alj, G. Holland, A. Davies,           [179] Google DeepMind, “Advanced version of Gemini with Deep Think
      and P. Kohli, “AI co-mathematician: Accelerating mathematicians with               officially achieves gold-medal standard at the international mathemat-
      agentic AI,” arXiv preprint arXiv:2605.06651, 2026.                                ical olympiad.” https://deepmind.google/blog/advanced- version- of-
[160] X. Lou, C. Wang, and B. An, “Mars-PO: Multi-agent reasoning system                 gemini- with- deep- think- officially- achieves- gold- medal- standard- at-
      preference optimization,” arXiv preprint arXiv:2411.19039, 2024.                   the-international-mathematical-olympiad/, 2025.
[161] S. R. Motwani, C. Smith, R. J. Das, R. Rafailov, I. Laptev, P. H. S. Torr,   [180] M. Balunovic, J. Dekoninck, I. Petrov, N. Jovanović, and M. Vechev,
      F. Pizzati, R. Clark, and C. S. de Witt, “MALT: Improving reasoning                “MathArena: Evaluating LLMs on uncontaminated math competitions,”
      with multi-agent LLM training,” Conference on Language Modeling                    Advances in Neural Information Processing Systems, vol. 38, 2026.
      (COLM), 2025.                                                                [181] LLM Stats, “Math benchmark leaderboards.” https://llm- stats.com/
[162] Z. Hu, Y. Hu, J. Liu, S. S. Li, Y. Wang, Z. Xu, S.-K. Ng, A. T. Luu,               benchmarks?category=math, 2026. Accessed May 10, 2026.
      X. Xu, B. Hooi, C. Breazeal, and H. W. Park, “Collaborative multi-           [182] N. I. Levi, “A simple model of inference scaling laws,” in Proceedings
      agent test-time reinforcement learning for reasoning,” arXiv preprint              of the 42nd International Conference on Machine Learning, vol. 267 of
      arXiv:2601.09667, 2026.                                                            Proceedings of Machine Learning Research, pp. 33984–33998, PMLR,
[163] Z. Azerbayev, H. Schoelkopf, K. Paster, M. D. Santos, S. McAleer,                  2025.
      A. Q. Jiang, J. Deng, S. Biderman, and S. Welleck, “Llemma: An               [183] B. Brown, J. Juravsky, R. Ehrlich, R. Clark, Q. V. Le, C. Ré, and
      open language model for mathematics,” in ICLR, 2024.                               A. Mirhoseini, “Large language monkeys: Scaling inference compute
[164] H. Ying, S. Zhang, L. Li, Z. Zhou, Y. Shao, Z. Fei, Y. Ma, J. Hong,                with repeated sampling,” 2024.
      K. Liu, Z. Wang, et al., “InternLM-Math: Open math large language            [184] X. Lin, S. Shimotsuji, M. Minoh, and T. Sakai, “Efficient diagram
      models toward verifiable reasoning,” arXiv preprint arXiv:2402.06332,              understanding with characteristic pattern detection,” Computer Vision,
      2024.                                                                              Graphics, and Image Processing, vol. 30, no. 1, pp. 84–106, 1985.
[185] R. W. Ferguson and K. D. Forbus, “GeoRep: A flexible tool for spatial      [209] Y. Lin et al., “Goedel-prover-v2: Scaling formal theorem proving
      representation of line drawings,” in AAAI/IAAI, pp. 510–516, 2000.               with scaffolded data synthesis and self-correction,” arXiv preprint
[186] W. C. Bulko, “Understanding text with an accompanying diagram,” in               arXiv:2508.03613, 2025.
      IEA/AIE, pp. 894–898, 1988.                                                [210] B. Georgiev, J. Gómez-Serrano, T. Tao, and A. Z. Wagner,
[187] G. S. Novak and W. C. Bulko, “Understanding natural language with                “Mathematical exploration and discovery at scale,” arXiv preprint
      diagrams,” in AAAI, pp. 465–470, 1990.                                           arXiv:2511.02864, 2025.
[188] M. J. Seo, H. Hajishirzi, A. Farhadi, and O. Etzioni, “Diagram             [211] T. Achim et al., “Aristotle: IMO-level automated theorem proving,”
      understanding in geometry questions,” in AAAI, 2014.                             arXiv preprint arXiv:2510.01346, 2025.
[189] M. Hopkins, R. Le Bras, C. Petrescu-Prahova, G. Stanovsky, H. Ha-          [212] E. Glazer, E. Erdil, T. Besiroglu, D. Chicharro, E. Chen, A. Gunning,
      jishirzi, and R. Koncel-Kedziorski, “SemEval-2019 task 10: Math                  C. F. Olsson, J.-S. Denain, A. Ho, E. d. O. Santos, et al., “FrontierMath:
      question answering,” in SemEval, pp. 893–899, 2019.                              A benchmark for evaluating advanced mathematical reasoning in ai,”
[190] M. Sachan, A. Dubey, E. H. Hovy, T. M. Mitchell, D. Roth, and E. P.              arXiv preprint arXiv:2411.04872, 2024.
      Xing, “Discourse in multimedia: A case study in extracting geometry        [213] Y. Feng et al., “Aletheia: Towards autonomous mathematics research,”
      knowledge from textbooks,” Computational Linguistics, vol. 45, no. 4,            arXiv preprint arXiv:2602.10177, 2026.
      pp. 627–665, 2020.                                                         [214] R. Koncel-Kedziorski, S. Roy, A. Amini, N. Kushman, and H. Ha-
[191] M. J. Seo, H. Hajishirzi, A. Farhadi, O. Etzioni, and C. Malcolm, “Solv-         jishirzi, “MAWPS: A math word problem repository,” in NAACL-HLT,
      ing geometry problems: Combining text and diagram interpretation,”               pp. 1152–1157, 2016.
      in EMNLP, 2015.                                                            [215] S.-y. Miao, C.-C. Liang, and K.-Y. Su, “A diverse corpus for evaluating
[192] M. Sachan, K. Dubey, and E. Xing, “From textbooks to knowledge: A                and developing English math word problem solvers,” in Proceedings
      case study in harvesting axiomatic knowledge from textbooks to solve             of the 58th Annual Meeting of the Association for Computational
      geometry problems,” in EMNLP, pp. 773–784, 2017.                                 Linguistics (D. Jurafsky, J. Chai, N. Schluter, and J. Tetreault, eds.),
[193] C. Alvin, S. Gulwani, R. Majumdar, and S. Mukhopadhyay, “Synthesis               (Online), pp. 975–984, Association for Computational Linguistics, July
      of solutions for shaded area geometry problems,” in FLAIRS, 2017.                2020.
[194] M. Sachan and E. Xing, “Learning to solve geometry problems from           [216] W. Ling, D. Yogatama, C. Dyer, and P. Blunsom, “Program induction
      natural language demonstrations in textbooks,” in *SEM, pp. 251–261,             by rationale generation: Learning to solve and explain algebraic word
      2017.                                                                            problems,” arXiv preprint arXiv:1705.04146, 2017.
[195] S.-h. Tsai, C.-C. Liang, H.-M. Wang, and K.-Y. Su, “Sequence to            [217] W. Zhao, M. Shang, Y. Liu, L. Wang, and J. Liu, “Ape210K: A large-
      general tree: Knowledge-guided geometry word problem solving.”                   scale and template-rich dataset of math word problems,” arXiv preprint
      2021.                                                                            arXiv:2009.11506, 2020.
[196] M.-L. Zhang, F. Yin, and C.-L. Liu, “A multi-modal neural geometric        [218] S. R. Raiyan, M. N. Faiyaz, S. M. J. Kabir, M. Kabir, H. Mahmud, and
      solver with textual clauses parsed from diagram,” in Proceedings of the          M. K. Hasan, “Math word problem solving by generating linguistic
      Thirty-Second International Joint Conference on Artificial Intelligence,         variants of problem statements,” in Proceedings of the 61st Annual
      pp. 3374–3382, 2023.                                                             Meeting of the Association for Computational Linguistics (Volume 4:
[197] S. Peng, D. Fu, Y. Liang, L. Gao, and Z. Tang, “GeoDRL: A self-                  Student Research Workshop), pp. 362–378, 2023.
      learning framework for geometry problem solving using reinforcement        [219] D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang,
      learning in deductive reasoning,” in Findings of the Association for             D. Song, and J. Steinhardt, “Measuring mathematical problem solving
      Computational Linguistics: ACL 2023, pp. 13468–13480, 2023.                      with the MATH dataset,” in NeurIPS Datasets and Benchmarks Track,
[198] Z.-Z. Li, M.-L. Zhang, F. Yin, and C.-L. Liu, “LANS: A layout-                   2021.
      aware neural solver for plane geometry problem,” in Findings of the        [220] C. He, R. Luo, Y. Bai, S. Hu, Z. L. Thai, J. Shen, J. Hu, X. Han,
      Association for Computational Linguistics: ACL 2024, pp. 2596–2608,              Y. Huang, Y. Zhang, et al., “OlympiadBench: A challenging benchmark
      2024.                                                                            for promoting AGI with olympiad-level bilingual multimodal scientific
[199] J. Zhao, T. Zhang, J. Sun, M. Tian, and H. Huang, “Pi-GPS: Enhancing             problems,” in ACL, 2024.
      geometry problem solving by unleashing the power of diagrammatic           [221] B. Gao, F. Song, Z. Yang, Z. Cai, Y. Miao, Q. Dong, L. Li, C. Ma,
      information,” in Proceedings of the IEEE/CVF International Confer-               L. Chen, R. Xu, et al., “Omni-MATH: A universal olympiad level
      ence on Computer Vision, pp. 1526–1536, 2025.                                    mathematic benchmark for large language models,” arXiv preprint
[200] M. A. B. Siddique, S. Hossain, S. A. Siam, S. R. Raiyan, H. Mahmud,              arXiv:2410.07985, 2024.
      and M. K. Hasan, “Beyond symbolic solving: Multi chain-of-thought          [222] F. Shi, M. Suzgun, M. Freitag, X. Wang, S. Srivats, S. Vosoughi, H. W.
      voting for geometric reasoning in large language models,” arXiv                  Chung, Y. Tay, S. Ruder, D. Zhou, D. Das, and J. Wei, “Language
      preprint arXiv:2604.00890, 2026.                                                 models are multilingual chain-of-thought reasoners,” arXiv preprint
[201] L. De Moura, S. Kong, J. Avigad, F. Van Doorn, and J. von Raumer,                arXiv:2210.03057, 2022.
      “The lean theorem prover (system description),” in International Con-      [223] H. Sharma, P. Mishra, and D. Sharma, “HAWP: a dataset for Hindi
      ference on Automated Deduction, pp. 378–388, Springer, 2015.                     arithmetic word problem solving,” in Proceedings of the Thirteenth
[202] T. Tao, “Machine assisted proof.” https://par.nsf.gov/servlets/purl/             Language Resources and Evaluation Conference, pp. 3479–3490, 2022.
      10576323, 2024.                                                            [224] R. Alghamdi, Z. Liang, and X. Zhang, “ArMATH: A dataset for
[203] Z. Zhang, J. Xu, Z. He, T. Liang, Q. Liu, Y. Li, L. Song, Z. Liang,              solving Arabic math word problems,” in Proceedings of the Thirteenth
      Z. Zhang, R. Wang, Z. Tu, H. Mi, and D. Yu, “DeepTheorem: Ad-                    Language Resources and Evaluation Conference, pp. 351–362, 2022.
      vancing LLM reasoning for theorem proving through natural language         [225] T. Wei, J. Luan, W. Liu, S. Dong, and B. Wang, “CMATH: Can your
      and reinforcement learning,” arXiv preprint arXiv:2505.23754, 2025.              language model pass Chinese elementary school math test?,” arXiv
[204] Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev,               preprint arXiv:2306.16636, 2023.
      and J. Avigad, “ProofNet: Autoformalizing and formally proving             [226] H. Ko, G. Son, and D. Choi, “Understand, solve and translate:
      undergraduate-level mathematics,” arXiv preprint arXiv:2302.12433,               Bridging the multilingual mathematical reasoning gap,” arXiv preprint
      2023.                                                                            arXiv:2501.02448, 2025.
[205] A. Poiroux, G. Weiss, V. Kunčak, and A. Bosselut, “Improving auto-        [227] J. J. Era, B. Paul, T. S. Aothoi, M. R. Zim, and F. M. Shah, “Empow-
      formalization using type checking,” arXiv preprint arXiv:2406.07222,             ering Bengali education with AI: Solving Bengali math word problems
      2024.                                                                            through transformer models,” arXiv preprint arXiv:2501.02599, 2025.
[206] H. Xin, Z. Ren, J. Song, Z. Shao, W. Zhao, H. Wang, B. Liu,                [228] S. Mondal, D. Khatua, S. Mandal, D. K. Prasad, and A. A. Sekh,
      L. Zhang, X. Lu, Q. Du, et al., “DeepSeek-Prover-V1.5: Harnessing                “BMWP: the first Bengali math word problems dataset for operation
      proof assistant feedback for reinforcement learning and monte-carlo              prediction and solving,” Discover Artificial Intelligence, vol. 5, no. 25,
      tree search,” in ICLR, 2025.                                                     2025.
[207] K. Zheng, J. M. Han, and S. Polu, “MiniF2F: A cross-system                 [229] Y. Wang, P. Zhang, J. Tang, H. Wei, B. Yang, R. Wang, C. Sun, F. Sun,
      benchmark for formal olympiad-level mathematics,” arXiv preprint                 J. Zhang, J. Wu, et al., “PolyMath: Evaluating mathematical reasoning
      arXiv:2109.00110, 2022.                                                          in multilingual contexts,” in NeurIPS, 2025.
[208] Y. Lin et al., “Goedel-prover: A frontier model for open-source            [230] A. Torres-Camps, N. M. Hadida, V. C. Vendrell, A. B. Casellas,
      automated theorem proving,” arXiv preprint arXiv:2502.07640, 2025.               A. P. Masdemont, and J. Ros-Giralt, “M3Kang: Evaluating multilingual
      multimodal mathematical reasoning in vision-language models,” arXiv       [252] O. Siddique, J. M. A. U. Alam, M. J. R. Rafy, S. R. Raiyan,
      preprint arXiv:2601.16218, 2026.                                                H. Mahmud, and M. K. Hasan, “PhysicsEval: Inference-time tech-
[231] G. Tsoukalas, J. Lee, J. Jennings, J. Xin, M. Ding, M. Jennings,                niques to improve the reasoning proficiency of large language models
      A. Thakur, and S. Chaudhuri, “PutnamBench: Evaluating neural                    on physics problems,” in Proceedings of the 14th International Joint
      theorem-provers on the putnam mathematical competition,” NeurIPS                Conference on Natural Language Processing and the 4th Conference
      Datasets and Benchmarks Track, 2024.                                            of the Asia-Pacific Chapter of the Association for Computational
[232] D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and             Linguistics, (Mumbai, India), pp. 738–760, The Asian Federation of
      J. Steinhardt, “Measuring massive multitask language understanding,”            Natural Language Processing and The Association for Computational
      in ICLR, 2021.                                                                  Linguistics, 2025.
[233] D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani,     [253] P. Lu, L. Qiu, K.-W. Chang, Y. N. Wu, S.-C. Zhu, T. Rajpurohit,
      J. Michael, and S. R. Bowman, “GPQA: A graduate-level google-proof              P. Clark, and A. Kalyan, “Dynamic prompt learning via policy gradient
      Q&A benchmark,” arXiv preprint arXiv:2311.12022, 2023.                          for semi-structured mathematical reasoning,” in ICLR, 2023.
[234] C. White, S. Dooley, M. Roberts, A. Pal, B. Feuer, S. Jain, R. Shwartz-   [254] Z. Chen, W. Chen, C. Smiley, S. Shah, I. Borova, D. Langdon,
      Ziv, N. Jain, K. Saifullah, S. Dey, et al., “LiveBench: A challenging,          R. Moussa, M. Beane, T.-H. Huang, B. Routledge, and W. Y. Wang,
      contamination-limited LLM benchmark,” in ICLR, 2025.                            “FinQA: A dataset of numerical reasoning over financial data,” in
[235] Center for AI Safety, Scale AI, and HLE Contributors Consortium, “A             EMNLP, 2021.
      benchmark of expert-level academic questions to assess AI capabili-       [255] F. Zhu, W. Lei, Y. Huang, C. Wang, S. Zhang, J. Lv, F. Feng, and
      ties,” Nature, vol. 649, pp. 1139–1146, 2026.                                   T.-S. Chua, “TAT-QA: A question answering benchmark on a hybrid
[236] S. Upadhyay and M.-W. Chang, “DRAW: A challenging and diverse                   of tabular and textual content in finance,” in ACL, 2021.
      algebra word problem set,” Technical Report, Microsoft Research MSR-      [256] Y. Zhao, Y. Li, C. Li, and R. Zhang, “MultiHiertt: Numerical reasoning
      TR-2015-78, 2015.                                                               over multi hierarchical tabular and textual data,” in ACL, 2022.
[237] A. Amini, S. Gabriel, P. Lin, R. Koncel-Kedziorski, Y. Choi, and H. Ha-   [257] P. Lu, B. Peng, H. Cheng, M. Galley, K.-W. Chang, Y. N. Wu, S.-C.
      jishirzi, “MathQA: Towards interpretable math word problem solving              Zhu, and J. Gao, “Chameleon: Plug-and-play compositional reasoning
      with operation-based formalisms,” arXiv preprint arXiv:1905.13319,              with large language models,” in NeurIPS, 2024.
      2019.                                                                     [258] V. Pal, A. Yates, E. Kanoulas, and M. de Rijke, “MultiTabQA:
[238] S. R. Raiyan, M. N. Faiyaz, and S. M. J. Kabir, Variational Mathemati-          Generating tabular answers for multi-table question answering,” in
      cal Reasoning: Enhancing Math Word Problem Solvers with Linguistic              ACL, 2023.
      Variants and Disentangled Attention. Bachelor’s thesis, Department        [259] S. Srivastava, Annarose M B, Anto P V, S. Menon, A. Sukumar,
      of Computer Science and Engineering (CSE), Islamic University of                Adwaith Samod T, A. Philipose, S. Prince, and S. Thomas, “Functional
      Technology (IUT), Board Bazar, Gazipur-1704, Bangladesh, 2023.                  benchmarks for robust evaluation of reasoning performance, and the
[239] E. Gedik and T. Gungor, “Solving Turkish math word problems by                  reasoning gap,” arXiv preprint arXiv:2402.19450, 2024.
      sequence-to-sequence encoder-decoder models,” Turkish Journal of          [260] W.-T. Wu, “On the decision problem and the mechanization of theorem-
      Electrical Engineering and Computer Sciences, vol. 31, no. 2, pp. 431–          proving in elementary geometry,” Scientia Sinica, vol. 21, no. 2,
      447, 2023.                                                                      pp. 159–172, 1978.
[240] K. Ki, D. Lee, and G. Gweon, “KoTAB: Korean template-based                [261] S. Sinha, A. Prabhu, P. Kumaraguru, S. Bhat, and M. Bethge, “Wu’s
      arithmetic solver with BERT,” in IEEE International Conference on               method can boost symbolic AI to rival silver medalists and Alpha-
      Big Data and Smart Computing, pp. 279–282, 2020.                                Geometry to outperform gold medalists at IMO geometry,” arXiv
[241] N. Chen, Z. Zheng, N. Wu, M. Gong, D. Zhang, and J. Li, “Breaking               preprint arXiv:2404.06405, 2024. NeurIPS 2024 MATH-AI Workshop.
      language barriers in multilingual mathematical reasoning: Insights and    [262] C. Zhang, J. Song, S. Li, Y. Liang, Y. Ma, W. Wang, Y. Zhu, and S.-
      observations,” arXiv preprint arXiv:2310.20246, 2023.                           C. Zhu, “Proposing and solving olympiad geometry with guided tree
[242] H. Lai and M. Nissim, “mCoT: Multilingual instruction tuning for                search,” Nature Machine Intelligence, vol. 8, pp. 84–95, 2026.
      reasoning consistency in language models,” ACL, 2024.                     [263] J. Achiam et al., “GPT-4 technical report,” arXiv preprint
[243] M. E. Sobhani, M. F. A. Sayeedi, T. Mohiuddin, M. M. Islam, and                 arXiv:2303.08774, 2023.
      S. Shatabda, “MathMist: A parallel multilingual benchmark dataset for     [264] P. Wang, S. Bai, S. Tan, S. Wang, Z. Fan, J. Bai, K. Chen, X. Liu,
      mathematical problem solving and reasoning,” Findings of EACL, 2026.            J. Wang, W. Ge, et al., “Qwen2-VL: Enhancing vision-language
[244] Y. Wang, X. Ma, G. Zhang, Y. Ni, A. Chandra, S. Guo, W. Ren,                    model’s perception of the world at any resolution,” arXiv preprint
      A. Arulraj, X. He, Z. Jiang, et al., “MMLU-Pro: A more robust and               arXiv:2409.12191, 2024.
      challenging multi-task language understanding benchmark,” in NeurIPS      [265] S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang,
      Datasets and Benchmarks Track, 2024.                                            S. Wang, J. Tang, et al., “Qwen2.5-VL technical report,” arXiv preprint
[245] M. Suzgun, N. Scales, N. Scharli, S. Gehrmann, Y. Tay, H. W. Chung,             arXiv:2502.13923, 2025.
      A. Chowdhery, Q. V. Le, E. H. Chi, D. Zhou, and J. Wei, “Challenging      [266] L. Chen, L. Li, H. Zhao, Y. Song, and Vinci, “R1-V: Reinforcing
      BIG-Bench tasks and whether chain-of-thought can solve them,” in                super generalization ability in vision-language models with less than
      Findings of ACL, 2023.                                                          $3.” https://github.com/Deep-Agent/R1-V, 2025. Accessed 2025.
[246] A. Srivastava, A. Rastogi, A. Rao, A. A. M. Shoeb, A. Abid, et al.,       [267] F. Meng et al., “MM-Eureka: Exploring visual aha moment
      “Beyond the imitation game: Quantifying and extrapolating the capabil-          with rule-based large-scale reinforcement learning,” arXiv preprint
      ities of language models,” Transactions on Machine Learning Research,           arXiv:2503.07365, 2025.
      2023.                                                                     [268] K. Liang, X. Li, W. Chen, and Y. Liu, “GeoGRPO: Investigating
[247] W. Zhong, R. Cui, Y. Guo, Y. Liang, S. Lu, Y. Wang, A. Saied,                   the stepwise-GRPO enhancement in RLHF framework,” in Document
      W. Chen, and N. Duan, “AGIEval: A human-centric benchmark for                   Analysis and Recognition – ICDAR 2025 Workshops (L. Jin, R. Zanibbi,
      evaluating foundation models,” arXiv preprint arXiv:2304.06364, 2023.           and V. Eglin, eds.), (Cham), pp. 344–361, Springer Nature Switzerland,
[248] M-A-P Team, X. Du, Y. Yao, K. Ma, B. Wang, T. Zheng, K. Zhu,                    2026.
      M. Liu, Y. Liang, X. Jin, et al., “SuperGPQA: Scaling LLM evaluation
      across 285 graduate disciplines,” arXiv preprint arXiv:2502.14739,
      2025.
[249] X. Wang, Z. Hu, P. Lu, Y. Zhu, J. Zhang, S. Subramaniam, A. R.
      Loomba, S. Zhang, Y. Sun, and W. Wang, “SciBench: Evaluating
      college-level scientific problem-solving abilities of large language
      models,” in ICML, 2024.
[250] L. Sun, Y. Han, Z. Zhao, D. Ma, Z. Shen, B. Chen, L. Chen, and K. Yu,
      “SciEval: A multi-level large language model evaluation benchmark for
      scientific research,” in AAAI, 2024.
[251] P. Lu, S. Mishra, T. Xia, L. Qiu, K.-W. Chang, S.-C. Zhu, O. Tafjord,
      P. Clark, and A. Kalyan, “Learn to explain: Multimodal reasoning via
      thought chains for science question answering,” in NeurIPS, 2022.
