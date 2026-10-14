                                            P ROVE -RT: Generating Mechanized Theorem
                                          Prover Scripts for Real-Time Systems using LLMs
                                                                          Sadat Shahriyar∗ , Shareef Ahmed† , Abdullah Al Arafat∗
                                                                          ∗ Florida International University, † University of South Florida

                                                                            Email: {sshahriy, aarafat}@fiu.edu, shareefahmed@usf.edu


                                            Abstract—Schedulability analysis is essential for certifying     results. By building on ROCQ, P ROSA enables schedulability
                                         real-time systems, but existing tests are often developed through   analyses to be stated and checked with precision, thereby
                                         pen-and-paper proofs that are difficult to scale, validate, and     increasing confidence in the correctness of real-time systems
                                         maintain. Mechanized verification in P ROSA/ROCQ offers a
                                         rigorous alternative, yet manually constructing such proofs re-     theory.
                                         quires substantial domain expertise and proof-engineering effort.      Unfortunately, mechanized verification does not eliminate
                                         Recent successes of large language models (LLMs) across a wide      the human effort required to construct formal proofs. This
                                         range of tasks make them promising candidates for generating        is evident from previous works. For example, CertiCAN, a
                                         P ROSA/ROCQ scripts for mechanized theorem provers. However,
                                         state-of-the-art LLMs often lack the P ROSA-specific knowledge
                                                                                                             P ROSA-based ROCQ tool for certifying CAN schedulability-
                                         required to correctly use its modeling abstractions and proof       analysis results, required 18,852 lines of ROCQ code, exclud-
arXiv:2608.12762v1 [cs.AI] 13 Aug 2026




                                         patterns.                                                           ing the P ROSA proofs that it reused [7]. Similarly, integrating
                                            This paper introduces P ROVE -RT, an LLM-assisted frame-         P ROSA’s verified schedulability analysis into the RT-CertiKOS
                                         work for generating P ROSA/ROCQ scripts to mechanize schedu-        verified operating-system kernel required 4,135 lines of ROCQ
                                         lability analyses in real-time systems literature. P ROVE -RT
                                                                                                             for the connection alone, including 1,900 lines for the transla-
                                         guides generation through dependency-aware informal sketches,
                                         retrieval from processed P ROSA documentation, staged skeleton      tion interface to P ROSA [8]. Beyond initial development costs,
                                         generation, and proof completion. We construct a mechanization-     mechanized proofs also incur maintenance costs: for instance,
                                         oriented corpus from 1, 191 real-time systems papers, containing    Bozhko and Brandenburg [9] observed that even conceptually
                                         13, 134 informal sketches with dependency information. On           simple changes to the underlying model can invalidate existing
                                         a curated evaluation set, direct prompting of state-of-the-art
                                                                                                             mechanized proofs and require dozens of person-hours of
                                         LLMs fails to reliably generate valid P ROSA mechanizations,
                                         whereas P ROVE -RT achieves a success rate of 44.7%. These          proof maintenance. These examples suggest that although
                                         results show that retrieval-guided and staged LLM assistance        P ROSA provides a reusable foundation for machine-checkable
                                         can improve automated mechanization of schedulability analysis      schedulability analysis, manual development and maintenance
                                         in P ROSA/ROCQ.                                                     remain a substantial barrier to widespread adoption.
                                                               I. I NTRODUCTION                                 To reduce the burden of script preparation for mechanized
                                                                                                             theorem provers [6, 10, 11, 12] in general cases, a growing
                                            Safety-critical real-time systems (RTS) must undergo an          body of work has explored automated theorem proving and
                                         offline certification process (typically in the form of a schedu-   proof automation using machine learning [13, 14, 15, 16,
                                         lability analysis) to ensure timing correctness at runtime. Tra-    17, 18, 19]. However, to the best of our knowledge, there
                                         ditionally, schedulability analyses have been devised through       has been no prior work on the automated mechanization of
                                         pen-and-paper proofs. Although this approach has enabled a          schedulability analyses for real-time systems. In this work, we
                                         rich body of real-time scheduling theory, it is increasingly        introduce P ROVE -RT, a novel large-language-model (LLM)-
                                         difficult to sustain as systems become more complex.                assisted framework for generating mechanized P ROSA proofs
                                            Moreover, manual proofs require careful validation, as sub-      for schedulability analyses whose correctness can be verified
                                         tle mistakes in intermediate lemmas or bounds can affect the        mechanically. It is noteworthy that, beyond mechanizing ex-
                                         final schedulability result and subsequent analyses that build      isting schedulability analyses, P ROVE -RT may also facilitate
                                         upon it (e.g., [1, 2, 3, 4] are a few papers among many others      the trustworthy use of generative AI for developing new
                                         that identify and address issues in earlier analyses).              schedulability analyses. As generative AI has shown promise
                                            An alternative approach is to verify correctness through         across many scientific disciplines [20, 21, 22], P ROVE -RT can
                                         mechanized proofs. Cerqueira et al. [5] developed the first         serve as a verification layer for validating AI-assisted or AI-
                                         mechanized theorem prover, P ROSA, for real-time systems.           generated schedulability results through mechanized checking.
                                         P ROSA provides a ROCQ [6]-based foundation for mechanized
                                         schedulability analysis, offering a more rigorous approach for      Challenges and Contributions. Although schedulability anal-
                                         verifying the correctness of pen-and-paper proofs. P ROSA is        yses are mathematically rigorous, they are typically expressed
                                         a repository of definitions and proofs for machine-checkable        in a non-mechanized form that lacks the explicit structure
                                         real-time scheduling theory, including task models, schedules,      required by theorem provers. Therefore, generating P ROSA
                                         workload functions, interference notions, and schedulability        scripts for schedulability analyses differs fundamentally from
conventional mathematical proof generation which is more             [23, 24, 25, 26, 27, 28], which provide many examples of
widely studied in the literature. This introduces three key          theorem statements, proof scripts, and reusable mathematical
challenges: (i) limited mechanized RTS corpora, restricting          libraries. In contrast, public data for mechanized schedulability
LLM understanding of P ROSA abstractions and proof patterns;         analysis is very limited. The P ROSA library is the main
(ii) a formalization gap between structurally non-mechanized         available resource, but its scale is much smaller than mature
schedulability analyses and P ROSA’s explicit proof structure;       mathematical proof libraries. This data scarcity limits the abil-
and (iii) the complexity in the structure of schedulability          ity of LLMs to learn P ROSA-specific abstractions, scheduling
lemmas/theorems compared to mathematical theorem-proving             terminology, type-class assumptions, and proof patterns.
tasks. These challenges are elaborated in Section II. To                Another challenge is the formalization gap between schedu-
overcome them, P ROVE -RT incrementally mechanizes schedu-           lability analyses as written in the real-time systems literature
lability analyses through staged formalization, dependency-          and the explicit proof structure required by P ROSA. Schedu-
aware proof construction, and retrieval-augmented grounding          lability analyses are usually presented through mathematical
using RTS knowledge and P ROSA documentation.                        notation, prose explanations, assumptions, definitions, interme-
   In summary, this paper makes the following contributions:         diate bounds, and proof sketches. Although these presentations
   • We introduce P ROVE -RT, a framework for assist-                are rigorous for human readers, they are not directly mecha-
      ing the mechanization of schedulability analyses in            nizable. A P ROSA/ROCQ development must explicitly declare
      P ROSA/ROCQ. To the best of our knowledge, P ROVE -RT          variables, hypotheses, type-class instances, section contexts,
      is the first LLM-assisted framework targeting the P ROSA-      dependencies, and proof obligations. Therefore, an automated
      based mechanization of RTS analysis.                           system must first identify the mechanization-relevant con-
   • We develop a benchmark from 1, 191 real-time systems            structs, recover their dependencies, normalize notation, and
      papers, comprising 13, 134 mechanization-oriented in-          map the extracted concepts to existing P ROSA abstractions
      formal sketches and corresponding P ROSA/ROCQ script           before proof generation can even begin.
      artifacts. The benchmark is intended to support future            Schedulability-analysis lemmas are also structurally com-
      work on LLM-assisted theorem proving and formalization         plex. They are often built on a hierarchy of task models, job
      for real-time systems.                                         parameters, arrival constraints, scheduling policies, workload
   • We analyze the key challenges, recurring failure                definitions, interference bounds, and response-time properties.
      modes, and corner cases encountered when generating            These definitions may depend on one another across multiple
      P ROSA/ROCQ scripts with LLMs. This study provides             levels and are usually accompanied by many hypotheses. As
      practical insights for improving future automated mech-        a result, the complete formal context needed to state and
      anization tools for real-time systems analysis.                prove a schedulability lemma in P ROSA can span hundreds of
Paper Organization. The remainder of the paper is organized          lines. This creates a substantial burden on the LLM’s context
as follows. Section II elaborates on the core challenges while       handling and reasoning capabilities.
mechanizing schedulability analysis with P ROSA. Section III            Beyond the complexity of individual lemmas, P ROSA is
provides background on P ROSA and reviews related work.              designed around reusable abstractions and lemmas that apply
Section IV introduces the notation used throughout the paper         across different task models and scheduling policies. Whether
and formalizes the problem statement. Section V presents the         an existing lemma can be used to prove a target result
design of P ROVE -RT. Section VII describes the construction         depends on whether its preconditions hold in the current proof
of the system invariant dataset, the evaluation baselines and        context. Thus, proof generation requires more than selecting
metrics, and the implementation details. Section VI provides         tactics: it requires constructing the right context, preserving
an example on how the framework works. Section VIII                  dependency order, and ensuring that all required assumptions
presents the evaluation of P ROVE -RT. Finally, Section IX           are available. These factors make automated mechanization of
concludes the paper by discussing the limitations of P ROVE -        schedulability analysis substantially more difficult than direct
RT and outlining directions for future work.                         proof generation for an already formalized theorem statement.
  II. C HALLENGES IN M ECHANIZING S CHEDULABILITY                             III. P RELIMINARIES AND R ELATED W ORK
                      A NALYSIS
   Automated theorem proving for real-time schedulability              In this section, we will discuss the necessary P ROSA back-
analysis introduces challenges that differ from the more com-        ground and the related works on mechanized theorem provers
monly studied setting of LLM-based theorem proving for pure          and script generation.
mathematics. In particular, the difficulty is not only to generate
                                                                     A. Background on P ROSA
a proof script for a given theorem, but also to recover the
formal structure needed to express schedulability analyses in           P ROSA [5] is a ROCQ library for mechanized schedulability
P ROSA/ROCQ.                                                         analysis of RTS. It formalizes real-time scheduling concepts
   A key limitation is the scarcity of mechanized training           as Gallina (i.e., ROCQ specification language) definitions and
data for real-time schedulability analysis. Recent LLM-based         establishes schedulability results as machine-checked lemmas
theorem-proving systems benefit from large formal corpora            and theorems. Since P ROSA is built in ROCQ, a P ROSA script
follows the standard ROCQ development model: required mod-             • Proof obligation is a statement that must be proved
ules are imported, assumptions are introduced through sections           before a development is complete. Lemmas, theorems,
and contexts, definitions are stated, and proof obligations are          and corollaries introduce proof obligations, whereas def-
discharged using tactics.                                                initions mainly introduce formal objects.
   A key feature of P ROSA developments is their reliance on           • Compilation is the process of checking a ROCQ /P ROSA
explicit proof context. A Section groups together variables,             file. A file compiles only if all referenced objects are
hypotheses, and type-class constraints that are shared by the            available, all statements are well typed, all type-class
definitions and lemmas inside it. P ROSA uses ROCQ type                  requirements are resolved, and all proof obligations are
classes to represent reusable modeling assumptions, such as              completed or explicitly admitted. A compilation error
task parameters, job parameters, scheduling policies, and sys-           occurs when any of these conditions is violated, for
tem properties. Although these assumptions may be inferred               example, due to missing imports, undefined variables,
automatically by ROCQ via type-class resolution, the required            unresolved type-class instances, type mismatches, or in-
instances must be available in the current context or imported           complete proofs. Such errors indicate that the script is
environment for the script to type-check.                                not yet a valid mechanized development.
   ROCQ follows a forward-referencing discipline: every def-
inition, hypothesis, lemma, theorem, and imported module             B. Related Works
must be introduced before it is used. Thus, a valid P ROSA
development must be ordered so that all prerequisites of a              Mechanized verification provides a rigorous way to validate
proof are already available when the proof is checked. This          mathematical and software artifacts by encoding definitions,
makes dependency ordering and context construction central           assumptions, lemmas, and theorems in an interactive theo-
to writing correct P ROSA scripts.                                   rem prover (ITP), where each proof is checked by a small
   We briefly summarize the ROCQ/P ROSA notions that are             trusted kernel. Several ITPs, such as ROCQ [6] (commonly
needed to follow the rest of the paper.                              known as Coq), Isabelle [10], Agda [12], and Lean [11], have
   • Proof script is the ROCQ source code used to express            been widely used in the verification community. These proof
      a formal development. In P ROSA, a proof script contains       assistants have supported the verification of a broad range
      imports, definitions, assumptions, lemmas, theorems, and       of software systems. For example, ROCQ has been used to
      tactic-based proofs for schedulability analysis.               verify the CompCert C compiler [29], a lightweight relational
   • Proof environment refers to the collection of formal            database management system [30], and distributed systems
      objects available during proof development. This includes      through the Verdi framework [31]. Isabelle/HOL has been used
      imported libraries, previously defined concepts, declared      to verify the seL4 operating-system kernel [32]. More recently,
      assumptions, and already-proved lemmas or theorems.            Lean has been used to formalize and verify neural networks
   • Proof context refers to the local information available         through TorchLean [33].
      at a particular point in a proof. In P ROSA, this often           In real-time systems, P ROSA provides a ROCQ-based foun-
      includes variables, hypotheses, task and job parameters,       dation for mechanized schedulability analysis [5]. It for-
      scheduling assumptions, and type-class instances intro-        malizes core real-time scheduling concepts including task
      duced inside a section.                                        models, schedules, workload functions, interference notions,
   • Proof goal is the proposition that remains to be proved.        and schedulability results. Building on this foundation, prior
      A schedulability theorem in P ROSA may generate one or         work has used P ROSA to mechanize and validate several
      more proof goals involving task assumptions, workload          schedulability-analysis results including response-time analy-
      bounds, interference bounds, or response-time guarantees.      sis, CAN schedulability certification, FIFO scheduling, busy-
   • Proof tactic is a command used to advance a proof by            window reasoning, and connections between response-time
      transforming the current goal into simpler subgoals or         analysis and network calculus [9, 7, 34, 35, 36]. These
      by solving it directly. Common ROCQ tactics include            works demonstrate the value of mechanized verification for
      intros, apply, rewrite, simpl, and lia.                        increasing confidence in real-time systems theory. However,
   • Proof step is one application of a proof tactic. Each proof     they still require substantial manual proof engineering and
      step changes the current proof state and moves the proof       domain expertise.
      closer to completion.                                             To reduce the burden of manual proof development, prior
   • Proof state is the complete status of an interactive proof      approaches have proposed various methods for generating
      at a given point, including the current goals and the          proof tactics, selecting relevant premises, and guiding proof
      local context. During proof construction, the proof state      search using learned models [13, 14, 15, 16, 17, 18, 19]. More
      changes after each tactic is applied.                          recently, large language models (LLMs) have shown promise
   • Type-class resolution is ROCQ ’s mechanism for auto-            in generating formal proofs and assisting interactive theorem
      matically finding required instances of abstract interfaces.   proving [37, 38, 39, 40, 41, 42]. However, these efforts
      P ROSA uses type classes to represent reusable modeling        have largely focused on general-purpose theorem proving or
      assumptions, such as job costs, task parameters, arrival       domains such as mathematics and software verification. To
      information, and scheduling properties.                        the best of our knowledge, there has been no prior effort to
automatically generate P ROSA proofs for mechanized schedu-              anizes the schedulability analysis and compiles under the
lability analysis from real-time systems papers.                         P ROSA/ROCQ environment as:

   IV. F RAMEWORK M ODEL AND P ROBLEM S TATEMENT                                                M : (A, P ) → S,

A. Framework Model                                                       where M denotes the P ROVE -RT generation pipeline and S =
                                                                         {s1 , s2 , . . . , sn } is the generated P ROSA/ROCQ script. Each
   We first define the main objects used throughout the P ROVE -         code block sj ∈ S is intended to formalize the corresponding
RT pipeline.                                                             system invariant ij ∈ I.
Schedulability Analysis (A). Let A be a schedulability anal-                A successful output must satisfy three requirements. First,
ysis for an RTS scheduling problem. Such an analysis is typ-             each generated code block sj must correctly represent the
ically presented using mathematical definitions, assumptions,            corresponding extracted invariant ij . Second, the ordering
lemmas, theorems, corollaries, and proof arguments. Unlike               of code blocks in S must respect the dependency graph
standard ROCQ tactic-generation tasks, A is not given as a               GD = (I, D), so that every prerequisite invariant is introduced
proof goal inside an existing proof environment. Instead, it             before any invariant that depends on it. Third, the final script
is a schedulability test whose formal constructs, dependency             S must compile under the P ROSA/ROCQ environment.
structure, and proof obligations must be recovered before
                                                                            We decompose this objective into two subproblems.
mechanization.
                                                                         Skeleton Generation (via Mskel ). The first subproblem
System Invariant (I). We use the term system invariant to
                                                                         is skeleton generation. For each invariant ij , the skeleton-
refer to any mechanization-relevant construct in A that must be
                                                                         generation module uses the informal sketch Kj , the retrieved
represented in the final P ROSA/ROCQ development. A system
                                                                         P ROSA context Rj , the dependency graph GD , and the partial
invariant may be a definition, hypothesis, assumption, lemma,
                                                                         P ROSA/ROCQ script already generated for earlier invariants,
theorem, corollary, fix-point, or other formal claim required to
                                                                         denoted by S<j , to produce a structurally valid P ROSA/ROCQ
establish the correctness of the schedulability test. We denote
                                                                         code block:
the set of extracted system invariants by I = {i1 , i2 , . . . , in }.
Informal Sketch ({Kj }). An informal sketch Kj describes the                           Mskel : (Kj , Rj , GD , S<j ) → sj .
statement of the invariant ij , the intuition behind it, and the
intended proof outline. These sketches serve as the intermedi-              After the skeleton-generation stage, some generated
ate representation between the natural-language schedulability           P ROSA/ROCQ fragments contain proof-bearing constructs,
analysis and the generated P ROSA/ROCQ script. Each invariant            such as lemmas, theorems, or corollaries, whose proof bodies
ij ∈ I is associated with an informal sketch Kj .                        were intentionally left as Admitted. We refer to these
Dependency Structure (GD ). The extracted invariants form a              unfinished proof bodies as deferred proof obligations. The
dependency structure. We represent this structure as a directed          proof-completion stage attempts to replace each Admitted.
acyclic graph (DAG) GD = (I, D), where each node corre-                  placeholder with a valid ROCQ proof.
sponds to a system invariant and each directed edge represents              For each deferred proof associated with sj , the proof-
a dependency, e.g., an edge (ip , ij ) ∈ D means that invariant          completion module takes the current partial script S<j , the
ij depends on ip . Thus, ip must appear earlier than ij in the           corresponding informal sketch Kj , and the retrieved P ROSA
generated P ROSA/ROCQ script. The DAG, therefore, defines                context as input Rj , and generates a proof fragment πj
the order in which invariants should be formalized. This                 intended to replace the Admitted. placeholder.
ordering is required because ROCQ is forward-referencing: all            Proof Completion (via Mproof ). The second subproblem is
definitions, assumptions, lemmas, theorems, and imports must             proof completion. For each deferred proof in sj , the proof-
be introduced before they are used.                                      completion module uses the current partial script S<j , the
P ROSA Documentation Corpus (P ). Let P be the processed                 informal sketch Kj , and the retrieved P ROSA context Rj to
P ROSA documentation corpus. P contains documentation frag-              generate a proof fragment πj :
ments, definitions, assumptions, reusable lemmas, and example
proof structures extracted from the P ROSA library. For each                           Mproof : (S<j , sj , Kj , Rj ) → πj .
invariant ij , the retrieval module selects a relevant subset
                                                                            The generated proof fragment πj is intended to replace the
Rj ⊆ P to provide the library-specific context needed for
                                                                         corresponding Admitted placeholder. It is accepted only if
script generation.
                                                                         the resulting P ROSA/ROCQ script is checked successfully by
   The generated script is built incrementally according to the
                                                                         the ROCQ compiler. If compilation fails, compiler feedback or
dependency order induced by GD .
                                                                         proof-state information is used to guide repair.
                                                                            Thus, the problem addressed by P ROVE -RT is broader
B. Problem Statement
                                                                         than next-tactic prediction. It requires transforming a real-time
   Given a schedulability analysis A and a processed P ROSA              systems schedulability analysis into a dependency-ordered
documentation corpus P , the goal of P ROVE -RT is to gener-             P ROSA/ROCQ script that can be mechanically checked by the
ate a dependency-ordered P ROSA/ROCQ script S that mech-                 proof assistant.
         Prosa Documentation             RTS Research Papers
                                                                          To facilitate this process, P ROVE -RT first prompts an LLM
                                                                       to identify candidate system invariants from schedulability test
                                                                       A. The LLM is guided using carefully designed prompts that
           Structure-aware                     Invariant
           chunking                            extraction
                                                                       include practical examples and detailed guardrails to ensure
                                                                       consistency and accuracy in the output.
          Outputs: Retrieval           Outputs: Invariants, Informal      For each extracted invariant ij ∈ I, the LLM generates an
          ready corpus                 sketches, dependency            informal sketch Kj . Informal sketches provide a structured,
                                                                       step-by-step description of each system invariant in plain
                                                                       text, capturing both the logical flow and the intended proof
                        Retrieval Operation
                                                                       outline. An example informal sketch is outlined in Listing 4
                                                                       in Appendix A1.
                                Prosa Docs    Prosa Examples
                                                                       Construction of Dependency Graph. The extracted depen-
                        Documents Reranking
                                                                       dency information is used to construct the dependency graph
                                                                       GD = (I, D). For each invariant ij , the LLM identifies
                      Skeleton Prompt Generator                        other invariants that must be established before ij can be
                                                                       formalized. Each such relation is represented as an edge in
                      Prosa Skeleton Generation                        D. The extracted invariants are then ordered according to this
                                                                       graph so that, when the P ROSA/ROCQ script is generated,
                                                                       prerequisites are introduced before the constructs that depend
                      Completed skeleton code
                                                                       on them. The resulting unit-level informal sketches, ordered
                                                                       by GD , form the primary input to the subsequent stages of
                Skeleton completion Prompt Generator                   P ROVE -RT.
                                                                       B. P ROSA Documentation Processing
                 Batch full proof completion + Repair
                                                                          The second stage of P ROVE -RT constructs the processed
                                                                       P ROSA documentation corpus P used for retrieval. This
                    Generated Prosa Script
                                                                       stage is necessary because direct LLM-based generation of
                                                                       P ROSA/ROCQ scripts is difficult without library-specific con-
Fig. 1: Overview of the proposed P ROSA/ROCQ proof-
                                                                       text. The P ROSA library relies on domain-specific abstrac-
generation pipeline.
                                                                       tions, type-class assumptions, reusable lemmas, and proof
                                                                       conventions that are often not available to a pretrained model.
                 V. P ROVE -RT F RAMEWORK                              Thus, the P ROSA documentation is processed into retrieval-
   P ROVE -RT consists of five stages: (1) Extracting system           ready fragments so that later stages can retrieve relevant proof
invariants, informal sketches, and dependency graph from               constructs for each invariant ij .
formally written schedulability analysis; (2) Processing the              The P ROSA documentation is organized into six main
P ROSA documentation into retrieval-ready fragments; (3) re-           modules: Analysis, Behavior, Implementation, Model, Results,
trieving relevant documentation and examples, with depen-              and Util. These modules are used to guide the construction
dency recovery for proof-oriented modules; (4) generating and          of P . In particular, the Results module is used primarily as a
validating a structurally correct proof skeleton with deferred         source of complete proof examples, since it contains formally
obligations; and (5) completing the deferred proofs using              verified schedulability results. The remaining modules provide
iterative repair. We explain these stages in the following             supporting context, including system definitions, modeling as-
subsections. Fig. 1 illustrates an overview of the P ROVE -RT.         sumptions, formal definitions, reusable lemmas, and auxiliary
                                                                       proof components.
A. System Invariant Extraction                                            As the modules differ in both structure and purpose, they
                                                                       are processed using two chunking strategies.
Extraction of Invariants and Sketches. The first stage of
P ROVE -RT transforms the input, schedulability analysis A,            Proof-Oriented Chunking. For the Analysis and Results
into the intermediate representation required for mechaniza-           modules, proof-oriented chunks are used which pairs each
tion, consisting of a set of system invariants I, their corre-         formal code block with its corresponding descriptive text.
sponding informal sketches {Kj }, and a dependency graph               This preserves the connection between a proof component
GD = (I, D). This stage is necessary as schedulability analy-          and the explanation that motivates it, allowing retrieval to
ses in the RTS literature are usually written for mathematical         operate over meaningful proof-level units such as definitions,
presentation rather than direct mechanization. As a result, the        lemmas, and theorems. During retrieval, the retrieved proof-
constructs needed for P ROSA/ROCQ generation may appear                level units are augmented with their relevant dependencies, so
in different forms, including prose explanations, equations,           that lemmas, theorems, and definitions are provided together
definitions, lemmas, theorems, claims, or corollaries.                 with the supporting constructs required for script generation.
This dependency reconstruction step is described in the next        maximum weight is kept to preserve the strongest dependency
section V-C.                                                        signal without double counting.
                                                                       After extracting candidate identifiers from the three zones,
Section-Level Chunking. For the remaining modules, section-
                                                                    each identifier is assigned a weight
level chunks are used, since these modules are typically                                                                         
organized around smaller and more self-contained concepts,          w(x) = max α · F[x ∈ ZA ], β · F[x ∈ ZB ], γ · F[x ∈ ZC ] ,
assumptions, or helper components.
   The resulting set of documentation fragments forms the           Here, ZA , ZB , and ZC denote the sets of identifiers extracted
processed corpus P . During retrieval, P ROVE -RT selects a         from the type-level zone, the explicit-reference zone, and the
relevant subset Rj ⊆ P for each invariant ij , which provides       remaining proof-token zone, respectively. The parameters α, β,
the LLM with P ROSA-specific context for generating the             and γ are weighting coefficients assigned to these zones, with
corresponding P ROSA/ROCQ code block sj .                           α > β > γ to reflect the relative strength of the dependency
                                                                    signal provided by each syntactic context. To improve robust-
C. Retrieval Process                                                ness, tokens are filtered out that are unlikely to correspond to
Query Construction. The retrieval stage constructs the con-         meaningful local dependencies, such as grammar keywords,
text Rj ⊆ P for each invariant ij . Given the informal sketch       logical connectives, single-character tokens, self-references,
Kj , the goal is to retrieve the most relevant fragments from       and proof-local names introduced during tactics.
the processed P ROSA documentation corpus P so that the                After extracting identifiers, they are matched against decla-
skeleton-generation module has access to library-specific def-      rations in earlier sections of the same file. A section receives
initions, assumptions, lemmas, and example proof structures.        a score when it defines a matched identifier, weighted by the
   Each informal sketch may contain information about mul-          identifier’s dependency score; sections with nonzero scores
tiple invariants, including a target invariant and the prerequi-    are treated as likely direct dependencies. Unmatched identi-
sites on which it depends. To preserve the dependency order         fiers contribute a small score to the imports file to prevent
induced by GD , we process the sketches one invariant at a          external-library references from being ignored. Because direct
time. For each invariant ij , its corresponding sketch Kj is        dependencies may themselves depend on earlier constructs, the
used as the retrieval unit.                                         procedure is applied recursively and arranges the recovered
   For each informal sketch unit Kj , three components are          sections in their original order so that each construct appears
used as retrieval queries: the statement of the invariant, the      before it is used.
intuition underlying it, and the conclusion it establishes. To-        The recovered dependencies are assembled with the re-
gether, these components capture both the formal objective          trieved section before being included in Rj . Imports are placed
and the supporting reasoning of the target proof step.              at the top level, code fragments are ordered for compilation,
   Retrieval is performed independently for the statement,          and unicode operators are normalized when needed. A lean
intuition, and conclusion queries, producing a ranked top-k list    version is first compiled containing only the recovered depen-
for each component. The retrieved candidates are then merged,       dencies to reduce context size and noise. If this fails, a full-
and the highest-scoring documentation sections are selected as      context version is used that includes all predecessor sections
the retrieval context Rj .                                          from the same file, which helps capture implicit dependencies
                                                                    such as typeclass requirements.
Dependency Recovery for Proof-Oriented Modules. For                    For the remaining modules, the documentation is more
candidates retrieved from the Analysis or Results modules, an       naturally organized into self-contained sections. Therefore,
additional syntax-aware dependency recovery step is applied         each section is treated as a single retrieval unit, the top-
before adding them to Rj . These modules contain proof-             k matching sections are retrieved, and used directly without
oriented files in which later sections often rely on earlier        additional dependency recovery.
definitions, hypotheses, lemmas, or typeclass contexts. Since
ROCQ follows a forward-referencing discipline, a section with       D. Skeleton Code Generation
index N can depend only on preceding sections with indices             The skeleton-generation stage addresses the first subproblem
from 0 to N − 1 within the same file. P ROVE -RT exploits this      defined in Section IV. For each invariant ij , it generates
ordering to recover the earlier sections needed to make the         a structurally valid P ROSA/ROCQ code block sj using the
retrieved proof fragment usable in downstream generation.           invariant’s informal sketch Kj , the retrieved context Rj , the
   The dependency recovery step assigns different weights to        dependency graph GD , and the partial script S<j generated
occurrences of identifiers based on their syntactic context.        for earlier invariants.
Identifiers before the Proof. keyword are treated as the               This stage deliberately separates structure generation from
strongest signals because they appear in the type-level state-      proof generation. Generating the correct type signature of a
ment of the declaration. Explicit references following tactics      P ROSA/ROCQ construct, including its name, variable bind-
such as apply and rewrite are treated as medium-strength            ings, typeclass constraints, and statement, is generally more
signals, while other proof-level tokens receive lower weight        tractable for a language model than simultaneously discovering
because they are more likely to include tactic noise or external-   a valid proof strategy. Therefore, the skeleton stage focuses
library names. If an identifier appears in multiple contexts, its   on producing well-typed declarations and statements, while
proof bodies are deferred to the proof-completion stage. This      Prosa Docs, Examples        Informal Sketch               Prior Script
decomposition provides an intermediate artifact that can be
checked by coqc, allowing P ROVE -RT to detect structural
errors before attempting proof synthesis.                                                      Build Prompt                     Retry
                                                                                   Skeleton and Assumption Integrity Rules
Prompt Construction. For each invariant ij , we construct
the skeleton-generation prompt from four inputs: the informal                           Generate Skeleton Block
sketch Kj , the retrieved P ROSA context Rj , the dependency                    LLM produces skeleton code, then Normalize
graph GD , and the partial script S<j . These components pro-
vide the model with the relevant library context, examples of                                     Validate
P ROSA structure, and the current proof context. The informal          Admitted only, Assumption Integrity, Compilation check with Rocq
sketch Kj for the target section is appended last so that it                                             Pass
remains the immediate generation objective.                                               Generated Skeleton code
   In addition to this contextual information, the prompt
includes two generation rules to ensure that the generated                         Fig. 2: Skeleton code generation
block sj is structurally meaningful. First, PROOF - SKELETON
RULE is enforced where every proof-bearing construct must be       fails, the section is regenerated; sections that repeatedly fail
generated with a deferred proof obligation using Admitted.,        are logged and skipped so that the pipeline can continue.
and no proof tactics are allowed at this stage. Thus, the model
may generate either of the following forms:                        E. Skeleton Code Completion
               Lemma foo : <statement>.                               After skeleton generation, each code block sj may contain
               Proof.                                              proof-bearing constructs whose proof bodies are deferred
                 Admitted.
or                                                                 using Admitted. The goal of the completion stage is to
                                                                   generate a proof fragment πj that replaces each deferred proof
               Lemma foo : <statement>.
               Admitted.                                           and makes the resulting P ROSA/ROCQ script compile. For each
Non-proof-bearing constructs, such as definitions, declara-        deferred proof, the completion module uses the current partial
tions, and type-level specifications, must instead be generated    script S<j , the corresponding informal sketch Kj , and the
in full because they do not create deferred proof obligations      retrieved P ROSA context Rj as input. In this way, the system
and are required for the skeleton to type-check.                   builds directly on the previous stage: the skeleton provides
   Second, ASSUMPTION - INTEGRITY RULES are enforced. In           the formal statement and context, while the completion stage
preliminary experiments, a common failure mode was that the        focuses only on filling in the missing proofs.
model made the proof artificially easy by turning claims that      Batch Completion with Iterative Repair. P ROVE -RT
should be proven into unsupported assumptions. To prevent          prompts LLM to generate the full proof body for a deferred
this, the prompt explicitly prohibits introducing unsupported      proof in one response. The generated proof fragment πj
hypotheses, restating the target claim as an assumption, or        replaces the corresponding Admitted. placeholder in sj ,
encoding the proof obligation in a vacuous way. Claims             and the resulting partial script is then checked with the
from Kj must remain proof-bearing constructs, while genuine        ROCQ compiler. Furthermore, to ensure that the generated
preconditions must be encoded as part of the corresponding         script proves the intended target lemma rather than circum-
formal statement.                                                  venting it, we include a proof-integrity checker. The checker
   These rules make skeleton checking more reliable. If the        validates the LLM-generated proof and detects whether the
generated block sj fails to compile, the error is more likely      model has modified the original problem, introduced unsup-
to indicate a structural problem, such as an incorrect type,       ported auxiliary facts, or shifted the main proof obligation
undefined identifier, or missing import, rather than a failed      into a separate construct. Edits outside the intended proof
or misleading proof attempt. They also prevent the model           region are treated as invalid. Concretely, the checker flags
from producing speculative proof bodies that may appear            constructs such as Axiom, Parameter, Parameters,
syntactically valid but are semantically incorrect and difficult   Conjecture, Conjectures, Admitted, admit, and
to repair later.                                                   Abort. It also detects whether the LLM introduces new global
Validation and Retry. After each generation attempt, the           lemmas or definitions outside the proof region that effectively
produced skeleton sj is validated in two steps. First, it is       carry the main proof burden. Such modifications are rejected
checked that all proof-bearing constructs follow the admitted-     because they may allow the script to compile without actually
only rule and contain no completed or partial proof bodies.        proving the original lemma. At the same time, the checker
Second, sj is appended to the current partial script S<j and the   permits harmless changes that do not alter the meaning of the
resulting script is compiled with coqc. This verifies structural   theorem, such as importing additional trusted libraries from
validity and type correctness.                                     P ROSA or MathComp etc. If the script compiles successfully
   Non-proof-bearing constructs are accepted directly because      and the proof-integrity checker reports no violations, the script
they do not open a Proof. block. If validation or compilation      is accepted.
             Skeleton Section
                                                                          These results are automatically extracted and structured using
                                                                          LLM. The extraction process identifies the formal statement,
                                                                          variables, assumptions, and conclusions associated with each
              Has Admittted?                                              invariant. In addition, it also produced an informal sketch. We
       no


                      yes                                                 provide the complete JSON extraction and the corresponding
            Generate Full Proof                                           informal sketch in Appendix A1.
            Replace all admitted                                             A notable property of the extraction is that it is dependency-
                                   Error
                                                                          aware. For each invariant, we identify the previously in-
              Compile Script                     Repair proof             troduced invariants on which it depends; this information
                 Rocq                         From compiler error
                                   Retry                                  is recorded explicitly in the extracted representation. These
                                           same error or
                      compiles             budget spent                   dependencies induce a partial order that governs the subse-
              Accept section                      Roll back
                                                                          quent formalization pipeline: an invariant is formalized only
               Append to P                       Mark as failed           after all of its dependencies have been processed. In this
                                                                          example, Claim 1 depends on Definition 1, so the definition
       Fig. 3: Batch Completion with Iterative Repair                     must first be formalized. Since P ROSA follows an interpreted
                                                                          execution model in ROCQ, all prerequisite definitions and con-
   If compilation fails or any violation is reported by the proof-
                                                                          structs must be available before they are referenced, making
integrity checker, P ROVE -RT enters an iterative repair loop in
                                                                          dependency-aware ordering essential for correct compilation.
which compiler feedback guides corrections. At each iteration,
the error message and its location are extracted from the                 B. Retrieval-Augmented Generation
compiler output and incorporated into a repair prompt together               Given the informal sketch of an invariant, the next step is
with the informal sketch Kj and the retrieved context Rj . The            to translate it into a P ROSA script. To support this translation,
LLM then proposes a revised proof fragment, which is inserted             we employ retrieval-augmented generation (RAG) over the
into the section and checked again.                                       P ROSA codebase. We use the statement, conclusion, and
   This process is attractive because it allows the model to              intuition fields from the informal sketch as query, retrieve
generate an entire proof in one step, while still benefiting from         their independent results and keep the top-k results from two
compiler-guided repair when the initial attempt is incorrect.             complementary sources: (i) example scripts that demonstrate
                                                                          similar constructs or proof patterns, and (ii) documentation
                 VI. I LLUSTRATIVE E XAMPLE                               fragments describing the syntax, semantics, and usage conven-
   We illustrate the end-to-end workflow of P ROVE -RT using a            tions of relevant P ROSA modules. Together, these provide the
concrete schedulability analysis drawn from the RTS literature,           LLM with sufficient context to generate correct and idiomatic
starting with the extraction of intermediate representations and          P ROSA script.
leading to the final machine-verified P ROSA script.                      C. Skeleton Code Generation
A. Source Material and Extraction                                            Using the retrieved context, we prompt the LLM to gen-
   We consider the paper “Worst-Case Timing Requirements                  erate skeleton code—a structurally complete, type-checkable
of Real-Time Tasks with Time Redundancy” [43] as a repre-                 P ROSA script in which all imports, section boundaries, type-
sentative example. From this paper, we extract the following              class contexts, variable declarations, and definition bodies are
definition and claim, which characterize the worst-case timing            fully specified, while every proof obligation is replaced by
requirements of a task under fault-tolerant execution. The                Admitted. Listing 1 shows the skeleton code generated for
formal notations introduced in the paper are as follows:                  the motivating example.
W ORST-C ASE T IMING R EQUIREMENT: Let ai (ki ) denote the                Listing 1: Skeleton code generated from the informal sketch.
additional processing time and runtime overhead required to               All structural elements are fully elaborated; the proof body is
tolerate ki faults during the mission time of a task T̃i . The            deferred via Admitted.
worst-case timing requirement Wi (ki ) of T̃i is given by                 Require Export prosa.util.all.
                                                                          Require Export prosa.behavior.time.
                    Wi (ki ) = Wi (0) + Ai (ki ),                   (1)   Require Export prosa.model.task.concept.
                                                                          Require Export prosa.model.aggregate.workload.
where Ai (ki ) denotes the worst-case value of ai (ki ) and
Wi (0) represents the failure-free worst-case execution time              Section WorstCaseTimingRequirement.
(WCET).                                                                     Context {Task : TaskType}.
R ETRY-BASED R EDUNDANCY: Assume that a task restarts                       Context ‘{TaskCost Task}.
from the beginning after each fault, with no rollback recovery.
                                                                            Context {Job : JobType}.
Let R∗ denote the constant restart overhead. Then the worst-                Context ‘{JobTask Job Task}.
case timing requirement under the retry mechanism is                        Context ‘{JobCost Job}.

             Wi (ki ) = ki · (R∗ + Wi (0)) + Wi (0).                (2)     Variable W_i_0 : work.
  Variable k_i : nat.                                            discharges it automatically. The completed script compiles
  Variable R_star : work.                                        under ROCQ and confirms that the retry-based worst-case
  Definition W_i_k_i (A_i_k_i : work) : work :=                  timing requirement is a valid instantiation of the general fault-
    W_i_0 + A_i_k_i.                                             tolerant WCET model formalized in P ROSA.
  Lemma W_i_k_i_retry :                                          This example demonstrates how our pipeline systematically
    W_i_k_i (k_i * (R_star + W_i_0))                             transforms informal real-time scheduling results into machine-
    = k_i * (R_star + W_i_0) + W_i_0.
  Proof.                                                         verified P ROSA proofs through a structured sequence of ex-
  Admitted.                                                      traction, retrieval-augmented skeleton generation, and targeted
                                                                 proof completion. A second illustrative example can also be
End WorstCaseTimingRequirement.
                                                                 found in Appendix F.
   The skeleton faithfully encodes the structure of both in-
                                                                                 VII. E XPERIMENTAL S ETUP
variants. Definition 1 is realized as the function W_i_k_i,
which takes the fault-tolerance overhead A_i_k_i as an              We evaluate P ROVE -RT by investigating the following
argument and returns its sum with the failure-free WCET          research questions (RQs).
W_i_0. The P ROSA type work, defined as nat, represents          RQ1: To what extent can P ROVE -RT formalize schedulability
discrete units of processor service. Claim 1 is stated as        tests as P ROSA/ROCQ scripts?
Lemma W_i_k_i_retry, which asserts that instantiating            RQ2: How does the dependency depth of informal sketches
W_i_k_i with the retry-specific overhead yields exactly          influence the success of mechanization?
Equation (2). The type-class contexts (TaskType, JobType,        RQ3: How does the choice of retrieval method affect the
TaskCost, etc.) anchor the formalization within P ROSA’s         effectiveness of P ROVE -RT?
modeling framework and ensure that the definitions are com-      A. System Invariant Dataset Construction
patible with the library’s broader infrastructure.
                                                                    As one of the main artifacts of this work, P ROVE -RT
   The Admitted. directive instructs ROCQ to accept the
                                                                 System Invariant Dataset is constructed, which is a large-
lemma statement without proof, allowing the entire file to
                                                                 scale collection of schedulability-analysis invariants designed
type-check successfully. This confirms that the formalization
                                                                 to support and evaluate LLM-assisted P ROSA/ROCQ mech-
structure—imports, scoping, type-class resolution, and the
                                                                 anization. The dataset provides instances of the framework
lemma statement itself—is sound before any proof synthesis
                                                                 objects introduced earlier: schedulability analyses A, extracted
is attempted.
                                                                 invariant sets I, informal sketches Kj , and dependency graphs
D. Proof Completion                                              GD = (I, D). Figure 4 presents a high-level overview of the
   In the final phase, we prompt the LLM a second time           system invariant corpus collection process.
to discharge the Admitted obligations. This two-phase de-           To construct the source corpus for system-invariant extrac-
composition is deliberate: by supplying the complete skeleton    tion, schedulability-analysis papers were collected from estab-
as context, the LLM gains visibility into the surrounding        lished real-time systems and embedded systems venues. The
definitions, type-class instances, and any auxiliary lemmas,     IEEE Xplore API was used to retrieve paper metadata. The
enabling it to generate proof tactics that are consistent with   search was restricted to major venues, including RTSS, RTAS,
the broader formalization. The prompt includes the retrieved     ECRTS, EMSOFT, RTCSA, RTNS, RSS, and IROS. The full
context from the RAG step, the full skeleton code, and an        search query and venue list are provided in Appendix B.
instruction to complete a specific Admitted block. For this         The API returned 1,991 paper records. For each record, the
example, the LLM produces the following proof:                   metadata was extracted to locate the corresponding full-text
                                                                 PDF. Since the IEEE Xplore API does not directly support
Listing 2: Completed proof of the retry-based worst-case         bulk full-text PDF downloads, a semi-automated browser-
timing requirement                                               assisted workflow was used with personal access credentials.
  Lemma W_i_k_i_retry :                                          For each paper, the PDF URL was extracted from the retrieved
    W_i_k_i (k_i * (R_star + W_i_0))                             metadata and was opened in an authenticated browser session
    = k_i * (R_star + W_i_0) + W_i_0.
  Proof.                                                         using Selenium. Then Selenium was used to interact with
    unfold W_i_k_i.                                              the Chrome PDF viewer and trigger the download action au-
    lia.                                                         tomatically. Because authenticated sessions may expire during
  Qed.
                                                                 long download runs, the workflow also included a session-
   The proof proceeds in two steps. First, unfold W_i_k_i        recovery mechanism that restored access through automated
δ-reduces the definition, exposing the underlying goal:          browser interactions. After retrieval, duplicate files caused
                                                                 by overlapping searches or repeated download sessions were
W_i_0 + ki × (R∗ + W_i_0) = ki × (R∗ + W_i_0) + W_i_0.
                                                                 removed, resulting in approximately 1,870 unique papers.
This is an equality over natural numbers that follows directly      Each collected PDF was then converted into a structured
from the commutativity of addition. The lia tactic, which        XML representation using GROBID. The XML format pre-
implements a decision procedure for linear integer arithmetic,   serves document structure, making it more suitable for LLM-
based extraction than raw PDF text. This structured repre-
                                                                          Paper
sentation was used as input to the invariant extraction stage           Constraints
                                                                                                    Title
of P ROVE -RT. In our implementation, we used Gemini-2.5-                                          Author                     Paper
Flash as the LLM and prompted it to identify candidate                    Target
                                                                                                    DOI                        PDF
                                                                                                  Metadata
                                                                         Venues                              Semi-automated
system invariants I from each schedulability analysis and to
                                                                                                               Download
extract their summaries, informal sketches Kj , and depen-
dency information for constructing GD . The prompts included                                                     Informal
                                                                                                                 Sketches
examples and guardrails to encourage consistent output and
                                                                         Corpus        Dependency Analysis                    LLM
to distinguish mechanization-relevant constructs from general
explanatory text.                                                               Fig. 4: System Invariant Dataset Collection
    After Gemini extraction, a deterministic validation pass was
applied to filter structurally invalid outputs before constructing   potheses, lemmas, theorems, corollaries, and fixpoints. The
the final dataset. The validator constructed an inter-invariant      complete fine-grained mapping from raw sketch kinds to
dependency graph from the extracted identifier and                   ROCQ keywords is provided in Appendix H. Overall, the
dependencies fields, where each invariant is represented as          extraction process produced 13,134 normalized system invari-
a node, and each resolved dependency is represented as a di-         ants, including their dependency information. Table I reports
rected edge from the dependent invariant to its prerequisite. To     the distribution of invariants across the normalized categories.
resolve dependency references, the validator uses a three-stage         We further analyze the number of invariants appearing
matching process: exact, normalized, and fuzzy matching.             in each unit-level informal sketch. Each sketch contains a
Exact matching requires the dependency string to match an            target invariant together with the dependencies that must be
extracted identifier character-for-character. Normalized match-      established before the target can be mechanized.
ing canonicalizes both dependency strings and candidate iden-           The resulting corpus is both an input to P ROVE -RT and a
tifiers by lowercasing text, replacing formatting artifacts such     reusable artifact for studying LLM-assisted mechanization of
as backticks and underscores with spaces, removing non-              real-time systems schedulability analyses. The distribution is
alphanumeric punctuation, and collapsing repeated whitespace.        described in Appendix G.
If both exact and normalized matching fail, fuzzy matching
compares the normalized dependency string against all nor-           B. Baselines
malized candidate identifiers using a character-level similarity
score and links it only to the highest-scoring candidate when           P ROVE -RT is compared against direct LLM-based gen-
the score exceeds 0.88. This step is intended to recover near-       eration of P ROSA/ROCQ scripts. Since recent LLMs have
duplicate identifiers with minor residual formatting differences     shown strong capability in proof synthesis and ROCQ code
while avoiding spurious dependency edges.                            generation, and since P ROSA is built on top of ROCQ, these
    Using the resolved dependency graph, the validator checks        baselines evaluate whether LLMs can mechanize real-time sys-
for unresolved dependencies, self-dependencies, forward ref-         tems schedulability analyses without the additional guidance
erences, and dependency cycles. Papers are labeled as keep,          introduced by PROVE-RT.
review, or reject: papers with dependency cycles or an                  We consider two baseline settings. First, the LLM is
unresolved-dependency ratio above 0.15 are rejected, papers          prompted to mechanize a target invariant using only the
with weaker structural issues are marked for review, and struc-      corresponding text from the original schedulability-analysis
turally valid papers are retained. After this filtering step, the    paper, without external P ROSA documentation or skeleton-
retained corpus contained 1, 191 papers and 13, 134 informal         code generation. Second, the LLM is provided with the ex-
sketches.                                                            tracted informal sketch for the target invariant, but receives no
    Another important characteristic of the retained system          retrieval support and does not use the skeleton-code generation
invariant dataset is the distribution of extracted constructs by     stage. These baselines measure how far direct LLM generation
type. As discussed earlier, each unit-level informal sketch          can go without dependency-aware retrieval, skeleton genera-
contains a target invariant together with the dependencies           tion, and proof-repair mechanisms.
required to establish it. Consequently, a single sketch may
include multiple system invariants that must be introduced           C. Evaluation Metrics
and proved sequentially before the final target invariant can           P ROVE -RT counts a generated script as successful only
be mechanized. We therefore analyze the full set of system           if it is accepted by the ROCQ proof checker; that is, the
invariants appearing across all collected sketches.                  completed proof must compile without errors, contain no
    This analysis reveals substantial variation in how authors       remaining deferred proof obligations, and pass the proof-
formulate and name system invariants. Across the collected           integrity checker without any reported violations. This follows
papers, 73 distinct raw invariant types were identified. To          the standard proof-assistant acceptance criterion used in prior
make these invariants compatible with ROCQ-based proof               ROCQ proof-generation work, where generated proofs are
development, they were normalized into six broader categories        considered correct only when they lead the theorem prover
corresponding to supported proof constructs: definitions, hy-        to proof termination with Qed [19, 42].
  TABLE I: Distribution of extracted elements by category          TABLE II: Overall mechanization success across generation
                                                                   modes.
   Category     Invariant Count Percentage # Raw Kinds
   Definition             6817        51.9%             17          Mode                                Formalized Success Rate
   Lemma                  4144        31.6%             38          Paper Statements + GPT-5               0/300          0.0%
   Theorem                1822        13.9%              1          Informal Sketch + GPT-5                0/300          0.0%
   Corollary               228         1.7%              1          Informal Sketch + Claude-Opus-4.6      1/300         0.33%
   Fixpoint                115         0.9%             14          PROVE-RT- HYBRID                      123/300        41.0%
   Hypothesis                8         0.1%              2          PROVE-RT- BM 25                       126/300        42.0%
   TOTAL                 13134      100.0%              73          PROVE-RT- DENSE                       134/300        44.7%

   To measure the effectiveness of P ROVE -RT, we use success                           VIII. E VALUATION
rate, a standard metric used in prior work to evaluate ROCQ           We evaluate P ROVE -RT according to the three research
code and proof generation [26, 44, 45].                            questions introduced in Section VII.
   Success rate is measured as the fraction of proof constructs    Evaluation of RQ1. To evaluate the effectiveness of P ROVE -
for which the tool generates a successful proof script:            RT, we compare it against direct P ROSA/ROCQ script genera-
                                     NS                            tion using state-of-the-art LLMs, including GPT and Claude.
                    Success Rate =      ,                    (3)   Although these models have demonstrated strong general
                                     NT
                                                                   capabilities in generating ROCQ code, their ability to gen-
where NS denotes the number of successfully mechanized             erate P ROSA scripts for mechanizing schedulability analyses
sketches with successful proof scripts, and NT denotes the         remains unclear. We therefore conduct a pilot study to assess
total number of evaluated sketches.                                how well these models perform in this domain-specific setting.
                                                                   We then evaluate how P ROVE -RT guides these models for
D. Implementation Details
                                                                   producing mechanically checkable P ROSA/ROCQ scripts.
   For the system invariant extraction stage, G EMINI -2.5-           For this evaluation, we performed a human-in-the-loop
F LASH was employed as the backbone large language model.          curation step to select a representative subset from the retained
The model is prompted with structured, guardrailed instruc-        invariant corpus. The selection focused on scheduling-analysis
tions alongside few-shot examples to ensure consistent XML         categories that are well aligned with existing P ROSA abstrac-
parsing.                                                           tions while still spanning different levels of mechanization
   For the retrieval-augmented generation (RAG) component,         difficulty. These categories include uniprocessor fixed-priority
the retrieval corpus was constructed from the CoqDoc-              response-time analysis, uniprocessor EDF response-time or
generated HTML documentation of P ROSA, yielding 5, 097            demand-bound analysis, FIFO/FCFS response-time analysis,
documentation fragments from 356 source files. Three retrieval     non-preemptive and limited-preemptive analyses, blocking
strategies were evaluated: BM25, dense retrieval, and hybrid       and resource-sharing analyses, self-suspending task analyses,
retrieval. For dense retrieval, the nomic-embed-code-7b            multiprocessor global EDF/global fixed-priority analysis, and
was used to generate vector embeddings and store them              multiprocessor partitioned scheduling analysis. After curation,
in a FAISS vector index. For each query, the top-K most            the final evaluation corpus contained 109 papers and 1, 904
relevant documentation chunks were selected, with K = 5,           unit-level informal sketches.
and they were provided as context to the LLM during skeleton          From this curated evaluation corpus, we further selected a
generation.                                                        smaller evaluation subset of 300 unit-level informal sketches
   The proof completion pipeline uses Claude-Opus-4.6.             using proportional stratified sampling over dependency-depth
It is executed in two phases. In the first phase, the skeleton     categories. Let nc denote the number of sketches in category
code is synthesized with Admitted. directives to verify            c, and let N denote the total number of sketches in the curated
type-checking and type-class resolution. In the second phase,      corpus. For each category, we computed the sampling quota
the LLM is prompted to discharge individual proof obligations      as
using automation tactics for linear integer arithmetic. All                                             nc
                                                                                             qc = 300 · .
interaction with the interactive theorem prover is managed via                                           N
an automated script running ROCQ version 9.1.0.                    We first selected ⌊qc ⌋ sketches from each category and then
   The dataset construction and semi-automated PDF collec-         assigned the remaining slots to the categories with the largest
tion workflows are executed via Selenium driving an authenti-      fractional remainders. Within each category, sketches were
cated Chrome browser session. Text extraction and document         sampled uniformly at random using a fixed seed of 42 for
structuring are processed using GROBID to convert raw PDFs         reproducibility.
into structured XML. The entire pipeline is implemented in            P ROVE -RT achieves the best performance among the eval-
Python 3.10 and evaluated on an Ubuntu 24.04 LTS server            uated approaches when used with dense RAG, mechanizing
equipped with an Intel Xeon w5-3423 processor with 12 cores        134 informal sketches and achieving a success rate of 44.7%.
and 24 hardware threads, and 64GB of system RAM.                   This result is encouraging because automated formalization
remains challenging even in more established proof-assistant          Evaluation of RQ2. To evaluate how the structural complexity
settings; prior neural theorem-proving systems such as Rango          of an informal sketch affects mechanization, we group the
and GPass report success rates of approximately 32% and               300 sampled informal sketches by the number of sections
35%, respectively [42, 19]. Although these results are not            they contain. In our dataset, each sketch is decomposed into
directly comparable due to differences in benchmarks and              a sequence of sections, where later sections may depend on
proof domains, they provide useful context for interpreting           definitions, assumptions, or intermediate results introduced
the difficulty of the task. Given that P ROVE -RT operates in         earlier in the sketch. Thus, the number of sections serves as a
the specialized and low-resource setting of P ROSA-based real-        proxy for the dependency depth and mechanization complexity
time systems mechanization, a 44.7% success rate indicates            of the sketch. For each group, we compare the total number
substantial progress.                                                 of sketches against the number of sketches that P ROVE -RT
   Other retrieval methods also perform competitively within          successfully formalizes as compilable P ROSA/ROCQ scripts.
P ROVE -RT: BM25 mechanizes 126 sketches with a success                  Figure 5 shows the distribution of total and successfully
rate of 42.0%, while hybrid retrieval mechanizes 123 sketches         formalized sketches across different section counts. Each pair
with a success rate of 41.0%. In contrast, direct generation          of bars corresponds to sketches with the same number of
with GPT fails to mechanize any construct, whether prompted           sections: the first bar shows the total number of sketches in
with paper statements or informal sketches. Claude mecha-             that group, while the second bar shows how many of them
nizes only 1 sketch from the informal sketches, correspond-           were successfully mechanized by P ROVE -RT.
ing to a success rate of 0.33%. These results suggest that               The trend suggests that section count is a useful indica-
direct prompting, even with structured informal sketches, is          tor of mechanization difficulty. Sketches with fewer sections
insufficient for reliable P ROSA/ROCQ generation. The detailed        typically correspond to simpler formalization tasks, such as
comparison is shown in Table II.                                      isolated definitions or short proof obligations, where the gen-
   An interesting observation from the direct-generation base-        erated P ROSA/ROCQ code depends on limited prior context.
lines is that both GPT and Claude often produce compilable            In contrast, sketches with many sections require P ROVE -RT
ROCQ scripts without actually using P ROSA. In these cases,           to preserve a longer chain of definitions, assumptions, and
the generated scripts may type-check in ROCQ, but they do not         intermediate results. This increases the likelihood that an error
rely on the definitions, abstractions, or verified results provided   in an earlier generated code block propagates to later blocks
by the P ROSA library. Since our goal is to mechanize real-time       and causes the final script to fail compilation. Consequently,
systems schedulability analyses within P ROSA, we count such          failures in high-section-count sketches often reflect compound
outputs as failures.                                                  challenges, such as missing or incorrect prerequisites, mis-
   In our study, Claude produced compilable scripts for 39 of         matched identifiers, or insufficient retrieved context. At the
the 300 informal sketches. However, only 1 of these scripts           same time, successful cases among multi-section sketches
used P ROSA; the remaining 38 were generic compilable ROCQ            show that P ROVE -RT can mechanize nontrivial dependency
scripts and were therefore discarded. The behavior was even           structures rather than only isolated constructs or single-step
more pronounced for GPT, it generated 148 compilable ROCQ             proof obligations.
scripts out of 300 attempts, but none of them used P ROSA.               It is important to note that the number of sections is only
These results further highlight the limitation of direct LLM          an approximate measure of complexity. Some short sketches
prompting, even when the generated output is syntactically            may contain difficult proof obligations, while some longer
valid and type-correct in ROCQ, it may fail to mechanize the          sketches may consist mostly of definitions or straightforward
target schedulability analysis in the intended P ROSA frame-          intermediate claims. Nevertheless, section count provides a
work.                                                                 useful aggregate view of how dependency depth affects end-
   This confirms that decomposing the task into sketch-guided         to-end mechanization success.
retrieval, skeleton generation, and proof completion improves
the reliability of LLM-assisted P ROSA mechanization.                   Observation II. The success of P ROVE -RT decreases as
                                                                        sketches contain more sections, suggesting that deeper
  Observation I. P ROVE -RT is substantially more effective             dependency chains make mechanization harder. Never-
  than direct LLM prompting for P ROSA/ROCQ mecha-                      theless, P ROVE -RT succeeds on several multi-section
  nization. On the 300 sampled informal sketches, P ROVE -              sketches, indicating that its dependency-aware extraction,
  RT- DENSE achieves the best result, mechanizing 134                   retrieval, and staged generation strategy can support non-
  sketches with a success rate of 44.7%. By contrast,                   trivial schedulability-analysis mechanization.
  direct generation with GPT-5 produces no valid P ROSA
  mechanizations, and Claude-Opus-4.6 succeeds on only 1
  sketch (0.33%). This demonstrates that successful mech-             Evaluation of RQ3. Prior work such as [42] uses BM25-
  anization requires more than general ROCQ generation                style sparse retrieval to retrieve relevant proof context. Sparse
  ability; it requires P ROSA-aware retrieval, dependency-            retrieval is a natural baseline because it is effective when
  aware structuring, and staged proof generation.                     the query and target documents share exact identifiers, the-
                                                                      orem names, library symbols, or domain-specific terminology.
                                            BM25 Retrieval                                                                                          Hybrid Retrieval                                                                          Dense Retrieval
                     80                                                                                                       80                                                                                         80
                                                                     Total                                                                                                    Total                                                                               Total
Number of Sketches




                                                                                                         Number of Sketches




                                                                                                                                                                                                    Number of Sketches
                          63                                                                                                       63                                                                                         63
                     60
                                50                                   Formalized                                               60
                                                                                                                                         50                                   Formalized                                 60
                                                                                                                                                                                                                               47 50
                                                                                                                                                                                                                                                                  Formalized
                           46         45                                                                                            46         45                                                                                       45
                     40                                                                                                       40          33                                                                             40        34
                                 29         27                                                                                                       27                                                                                       27
                                       23         22       23                                                                                              22       23                                                                              22       23
                     20                                             13                                                        20                14                           13                                          20              18
                                             10                              12
                                                                                      7       8                                                       10                              12
                                                                                                                                                                                                8                                              11             10 13       12
                                                                                                                                                                                                                                                                                           8
                                                       6        5        5        2                                                                             5        5        3        4 71 1                                                        6            3        1
                                                                                                                                                                                                                                                                                   7
                                                                                                                                                                                                                                                                                       1       2
                                                                                          0       0
                      0    1     2     3     4     5        6        7        8       9 10                                     0    1     2     3     4     5        6        7        8     9 10                         0    1   2     3     4     5        6   7        8       9 10
                                       Number of Sections                                                                                       Number of Sections                                                                       Number of Sections
                                            (a) BM25                                                                                                (b) Hybrid                                                                                (c) Dense
    Fig. 5: Mechanization success by dependency depth for different retrieval methods. For readability, the plot shows sketches
    with at most 10 sections. For each dependency depth, the blue bar shows the total number of sketches and the orange bar
    shows the number successfully formalized by P ROVE -RT.
                     TABLE III: Effect of retrieval method on P ROVE -RT.                                                                                           TABLE IV: Retrieval performance by target construct kind.

                          Retrieval         All Sections Proven                                       Sections Compiled                                             Kind                        Hybrid                                  BM25                              Dense
                          Hybrid                 123/300 (41.0%)                                      608/1393 (43.6%)                                              Definition 112/278 (40.3%) 114/278 (41.0%) 125/278 (45.0%)
                          BM25                   126/300 (42.0%)                                      559/1393 (40.1%)                                              Lemma        8/19 (42.1%)    9/19 (47.4%)    8/19 (42.1%)
                          Dense                  134/300 (44.7%)                                      597/1393 (42.9%)                                              Theorem      3/3 (100.0%)    3/3 (100.0%)     1/3 (33.3%)

                                                                                                                                                                that local section-level compilation does not always translate
    However, the retrieval setting in P ROVE -RT is different. The                                                                                              into full-sketch mechanization, since a sketch is counted as
    P ROSA documentation contains both formal code blocks and                                                                                                   fully mechanized only if all of its sections compile together
    descriptive text explaining the logical role of definitions,                                                                                                in dependency order.
    lemmas, assumptions, and proof patterns. Moreover, for each                                                                                                    Table IV further breaks down performance by target
    code block, we generate an additional LLM-based description                                                                                                 construct kind. Dense retrieval performs best on definition
    so that the retrieval corpus captures not only the surface syntax                                                                                           sketches, proving 125 out of 278 cases (45.0%), suggesting
    of the code but also its intended semantic role.                                                                                                            that semantic retrieval is effective for matching informal
       This motivates our evaluation of different retrieval methods.                                                                                            descriptions to P ROSA definitions. However, for proof-bearing
    In P ROVE -RT, retrieval queries are derived from the informal                                                                                              constructs, the trend is different. Combining lemmas and
    sketch Kj , which describes the statement, intuition, and con-                                                                                              theorems, BM25 proves 12 out of 22 proof-bearing sketches
    clusion of a target invariant in natural language. These queries                                                                                            (54.5%), Hybrid proves 11 out of 22 (50.0%), and Dense
    often do not share exact tokens with the corresponding P ROSA                                                                                               proves 9 out of 22 (40.9%). This suggests that sparse and
    documentation or code identifiers, even when they refer to                                                                                                  hybrid retrieval are particularly useful when proof completion
    the same concept. Dense retrieval is therefore useful because                                                                                               depends on exact lemma names, theorem identifiers, or library-
    it maps both sketch-derived queries and documentation de-                                                                                                   specific proof patterns. Thus, while dense retrieval gives
    scriptions into a shared semantic embedding space. At the                                                                                                   the strongest end-to-end performance overall, lexical retrieval
    same time, sparse retrieval may still be useful for recovering                                                                                              remains important for proof-bearing constructs where exact
    exact P ROSA identifiers, theorem names, and library-specific                                                                                               P ROSA references are often needed.
    terminology.                                                                                                                                                   Overall, dense retrieval is most effective for semantic align-
       Table III compares retrieval methods using two complemen-                                                                                                ment, whereas sparse and hybrid retrieval remain valuable
    tary metrics. The first metric, All Sections Proven, measures                                                                                               for proof-bearing constructs that depend on exact P ROSA
    end-to-end mechanization success: a sketch is counted as                                                                                                    references.
    successful only when all of its sections are formalized and
    compiled in dependency order. The second metric, Sections                                                                                                        Observation III. The choice of retrieval method affects
    Compiled, measures local section-level success across all                                                                                                        both section-level compilation and end-to-end mechaniza-
    generated sections.                                                                                                                                              tion. Dense retrieval achieves the best overall result, fully
       Dense retrieval achieves the best end-to-end mechanization                                                                                                    mechanizing 134/300 sketches (44.7%), while Hybrid
    performance, proving all sections for 134 out of 300 sketches                                                                                                    compiles the most individual sections, with 608/1393
    (44.7%). BM25 and Hybrid also perform competitively, prov-                                                                                                       compiled sections (43.6%). This suggests that semantic
    ing 126 and 123 sketches, respectively. At the section level,                                                                                                    retrieval is especially useful for completing full depen-
    however, Hybrid compiles the largest number of individual                                                                                                        dency chains, while sparse retrieval remains useful for
    sections, with 608 compiled sections out of 1393 (43.6%),                                                                                                        exact identifier and lemma-name matches.
    slightly higher than Dense with 597/1393 (42.9%). This shows
                       IX. C ONCLUSION                                   [9] S. Bozhko and B. B. Brandenburg, “Abstract response-time
                                                                             analysis: A formal foundation for the busy-window principle
   This paper introduced P ROVE -RT, an LLM-assisted frame-                  (artifact),” Dagstuhl Artifacts Ser., vol. 6, pp. 03:1–03:2, 2020.
work for generating mechanized P ROSA/ROCQ scripts for                       [Online]. Available: https://api.semanticscholar.org/CorpusID:
schedulability analyses in real-time systems literature. P ROVE -            220275236
RT combines dependency-aware informal sketch extraction,                [10] T. Nipkow, M. Wenzel, and L. C. Paulson, Isabelle/HOL: a
                                                                             proof assistant for higher-order logic.        Berlin, Heidelberg:
retrieval from processed P ROSA documentation, staged skele-                 Springer-Verlag, 2002.
ton generation, and proof completion to guide LLMs toward               [11] L. de Moura, S. Kong, J. Avigad, F. van Doorn, and J. von
P ROSA-aware mechanization. Our evaluation shows that di-                    Raumer, “The lean theorem prover (system description),” in Au-
rect prompting of state-of-the-art LLMs is insufficient for                  tomated Deduction - CADE-25, A. P. Felty and A. Middeldorp,
reliable P ROSA generation, while P ROVE -RT achieves a suc-                 Eds. Cham: Springer International Publishing, 2015, pp. 378–
                                                                             388.
cess rate of 44.7% with dense retrieval. We also construct              [12] “Towards a practical programming language based
a mechanization-oriented corpus of informal sketches with                    on dependent type theory,” 2007. [Online]. Available:
dependency information. The corpus can facilitate future                     https://api.semanticscholar.org/CorpusID:118357515
research on LLM-assisted mechanization of schedulability                [13] L. Blaauwbroek, M. Olšák, J. Rute, F. I. Schaposnik Massolo,
analyses, as domain-specific datasets for P ROSA/ROCQ-based                  J. Piepenbrock, and V. Pestun, “Graph2Tac: Online repre-
                                                                             sentation learning of formal math concepts,” in Proceedings
schedulability analysis are currently lacking and remain a                   of the 41st International Conference on Machine Learning,
major bottleneck for automated script generation.                            ser. Proceedings of Machine Learning Research, vol. 235.
   As a research prototype, P ROVE -RT still faces challenges                PMLR, 21–27 Jul 2024, pp. 4046–4076. [Online]. Available:
with deeper dependency chains and proof-bearing constructs                   https://proceedings.mlr.press/v235/blaauwbroek24a.html
that require precise P ROSA context. Future work will improve           [14] E. First and Y. Brun, “Diversity-driven automated formal
                                                                             verification,” in Proceedings of the 44th International
retrieval, incorporate richer proof-state feedback, and extend               Conference on Software Engineering, ser. ICSE ’22.
the framework to broader classes of schedulability analyses.                 New York, NY, USA: Association for Computing
Moreover, we will study the capabilities of LLMs to generate                 Machinery, 2022, p. 749–761. [Online]. Available:
schedulability constraints for new scheduling problems, for                  https://doi.org/10.1145/3510003.3510138
which P ROVE -RT can be used to mechanically verify the                 [15] L. Blaauwbroek, J. Urban, and H. Geuvers, “The
                                                                             tactician: A seamless, interactive tactic learner and
correctness of LLM-generated schedulability results.                         prover for coq,” in Intelligent Computer Mathematics:
                                                                             13th International Conference, CICM 2020, Bertinoro,
                          R EFERENCES                                        Italy, July 26–31, 2020, Proceedings. Berlin, Heidelberg:
 [1] R. Devillers and J. Goossens, “Liu and layland’s schedulability         Springer-Verlag, 2020, p. 271–277. [Online]. Available:
     test revisited,” Inf. Process. Lett., vol. 73, no. 5–6, p.              https://doi.org/10.1007/978-3-030-53518-6 17
     157–161, Mar. 2000. [Online]. Available: https://doi.org/10.       [16] E. First, Y. Brun, and A. Guha, “Tactok: semantics-aware
     1016/S0020-0190(00)00016-8                                              proof synthesis,” vol. 4, no. OOPSLA, Nov. 2020. [Online].
 [2] R. J. Bril, J. J. Lukkien, R. I. Davis, and A. Burns,                   Available: https://doi.org/10.1145/3428299
     “Message response time analysis for ideal controller area          [17] A. Sanchez-Stern, Y. Alhessi, L. Saul, and S. Lerner,
     network (can) refuted,” 2006. [Online]. Available: https:               “Generating correctness proofs with neural networks,” in
     //api.semanticscholar.org/CorpusID:9850815                              Proceedings of the 4th ACM SIGPLAN International Workshop
 [3] G. Nelissen, J. Fonseca, G. Raravi, and V. Nélis, “Timing              on Machine Learning and Programming Languages, ser.
     analysis of fixed priority self-suspending sporadic tasks,” in          MAPL 2020. New York, NY, USA: Association for
     2015 27th Euromicro Conference on Real-Time Systems, 2015,              Computing Machinery, 2020, p. 1–10. [Online]. Available:
     pp. 80–89.                                                              https://doi.org/10.1145/3394450.3397466
 [4] J.-J. Chen, G. Nelissen, W.-H. Huang, M. Yang,                     [18] A. Sanchez-Stern, E. First, T. Zhou, Z. Kaufman, Y. Brun,
     B. Brandenburg, K. Bletsas, C. Liu, P. Richard, F. Ridouard,            and T. Ringer, “Passport: Improving automated formal
     N. Audsley, R. Rajkumar, D. Niz, and G. Brüggen,                       verification using identifiers,” ACM Trans. Program. Lang.
     “Many suspensions, many problems: a review of self-                     Syst., vol. 45, no. 2, Jun. 2023. [Online]. Available:
     suspending tasks in real-time systems,” Real-Time Syst.,                https://doi.org/10.1145/3593374
     vol. 55, no. 1, p. 144–207, Jan. 2019. [Online]. Available:        [19] Y. Chen, Z. Sun, G. Wang, and D. Hao, “Gpass: A goal-
     https://doi.org/10.1007/s11241-018-9316-9                               adaptive neural theorem prover based on coq for automated
 [5] F. Cerqueira, F. Stutz, and B. B. Brandenburg, “Prosa: A case           formal verification,” in Proceedings of the IEEE/ACM 47th
     for readable mechanized schedulability analysis,” in 2016 28th          International Conference on Software Engineering, ser. ICSE
     Euromicro Conference on Real-Time Systems (ECRTS), 2016,                ’25. IEEE Press, 2025, p. 29–41. [Online]. Available:
     pp. 273–284.                                                            https://doi.org/10.1109/ICSE55347.2025.00116
 [6] The Rocq Prover, 2026, available at https://rocq-prover.org/doc/   [20] R. Xin, C. Xi, J. Yang, F. Chen, H. Wu, X. Xiao, Y. Sun,
     V9.2.0/refman/index.html. Last accessed: 2026-05-21.                    S. Zheng, and K. Shen, “Bfs-prover: Scalable best-first
 [7] P. Fradet, X. Guo, and S. Quinton, “Certican certifying                 tree search for llm-based automatic theorem proving,” 2025.
     can analyses and their results,” Real-Time Syst., vol. 59,              [Online]. Available: https://arxiv.org/abs/2502.03438
     no. 2, p. 160–198, Mar. 2023. [Online]. Available: https:          [21] Z. Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao,
     //doi.org/10.1007/s11241-023-09393-2                                    L. Zhang, Z. Fu, Q. Zhu, D. Yang, Z. F. Wu, Z. Gou, S. Ma,
 [8] X. Guo, M. Lesourd, M. Liu, L. Rieg, and Z. Shao, “Integrating          H. Tang, Y. Liu, W. Gao, D. Guo, and C. Ruan, “Deepseek-
     formal schedulability analysis into a verified os kernel,” in           prover-v2: Advancing formal mathematical reasoning via
     Computer Aided Verification, I. Dillig and S. Tasiran, Eds.             reinforcement learning for subgoal decomposition,” 2025.
     Cham: Springer International Publishing, 2019, pp. 496–514.             [Online]. Available: https://arxiv.org/abs/2504.21801
[22] Z. Shen, N. Huang, F. Yang, Y. Wang, G. Gao, T. Xu,                        Dagstuhl Artifacts Series, vol. 8, no. 1, pp. 3:1–3:3, 2022.
     J. Jiang, W. He, P. Yang, M. Sun, H. Ju, P. Wu,                            [Online]. Available: https://drops.dagstuhl.de/entities/document/
     B. Dai, and B. Dong, “Real-prover: Retrieval augmented lean                10.4230/DARTS.8.1.3
     prover for mathematical reasoning,” 2025. [Online]. Available:        [37] J. M. Han, J. Rute, Y. Wu, E. Ayers, and S. Polu, “Proof
     https://arxiv.org/abs/2505.20613                                           artifact co-training for theorem proving with language models,”
[23] “The lean mathematical library,” CoRR, vol. abs/1910.09336,                in International Conference on Learning Representations,
     2019. [Online]. Available: http://arxiv.org/abs/1910.09336                 2022. [Online]. Available: https://openreview.net/forum?id=
[24] K. Zheng, J. M. Han, and S. Polu, “Minif2f: a cross-system                 rpxJc9j04U
     benchmark for formal olympiad-level mathematics,” arXiv               [38] A. Q. Jiang, W. Li, S. Tworkowski, K. Czechowski,
     preprint arXiv:2109.00110, 2021.                                           T. Odrzygóźdź, P. Mił oś, Y. Wu, and M. Jamnik,
[25] Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers,                   “Thor: Wielding hammers to integrate language models
     D. Radev, and J. Avigad, “Proofnet: Autoformalizing and                    and automated theorem provers,” in Advances in
     formally proving undergraduate-level mathematics,” 2023.                   Neural Information Processing Systems, vol. 35. Curran
     [Online]. Available: https://arxiv.org/abs/2302.12433                      Associates, Inc., 2022, pp. 8360–8373. [Online]. Avail-
[26] K. Yang and J. Deng, “Learning to prove theorems via                       able: https://proceedings.neurips.cc/paper files/paper/2022/file/
     interacting with proof assistants,” CoRR, vol. abs/1905.09381,             377c25312668e48f2e531e2f2c422483-Paper-Conference.pdf
     2019. [Online]. Available: http://arxiv.org/abs/1905.09381            [39] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song,
[27] K. Bansal, S. Loos, M. Rabe, C. Szegedy, and S. J. Wilcox,                 S. Yu, S. Godil, R. J. Prenger, and A. Anandkumar,
     “Holist: An environment for machine learning of higher                     “Leandojo: Theorem proving with retrieval-augmented
     order logic theorem proving,” in Thirty-sixth International                language models,” in Advances in Neural Information
     Conference on Machine Learning (ICML), 2019. [Online].                     Processing Systems, vol. 36.               Curran Associates,
     Available: https://arxiv.org/abs/1904.03241                                Inc., 2023, pp. 21 573–21 612. [Online]. Available:
[28] G. Tsoukalas, J. Lee, J. Jennings, J. Xin, M. Ding, M. Jennings,           https://proceedings.neurips.cc/paper files/paper/2023/file/
     A. Thakur, and S. Chaudhuri, “Putnambench: Evaluating neural               4441469427094f8873d0fecb0c4e1cee-Paper-Datasets and
     theorem-provers on the putnam mathematical competition,”                   Benchmarks.pdf
     2024. [Online]. Available: https://arxiv.org/abs/2407.11214           [40] A. Q. Jiang, W. Li, J. M. Han, and Y. Wu, “LISA:
[29] X. Leroy, “Formal verification of a realistic compiler,”                   Language models of ISAbelle proofs,” in 6th Conference
     Commun. ACM, vol. 52, no. 7, p. 107–115, Jul. 2009. [Online].              on Artificial Intelligence and Theorem Proving (AITP),
     Available: https://doi.org/10.1145/1538788.1538814                         Aussois, France, Sep. 2021, pp. 17:1–17:3. [Online]. Available:
[30] G. Malecha, G. Morrisett, A. Shinnar, and R. Wisnesky,                     https://aitp-conference.org/2021/abstract/paper 17.pdf
     “Toward a verified relational database management system,”            [41] S. Polu and I. Sutskever, “Generative language modeling for
     in Proceedings of the 37th Annual ACM SIGPLAN-SIGACT                       automated theorem proving,” ArXiv, vol. abs/2009.03393, 2020.
     Symposium on Principles of Programming Languages, ser.                     [Online]. Available: https://api.semanticscholar.org/CorpusID:
     POPL ’10. New York, NY, USA: Association for Computing                     221535103
     Machinery, 2010, p. 237–248. [Online]. Available: https:              [42] K. Thompson, N. Saavedra, P. Carrott, K. Fisher, A. Sanchez-
     //doi.org/10.1145/1706299.1706329                                          Stern, Y. Brun, J. a. F. Ferreira, S. Lerner, and E. First,
[31] J. R. Wilcox, D. Woos, P. Panchekha, Z. Tatlock, X. Wang,                  “Rango: Adaptive retrieval-augmented proving for automated
     M. D. Ernst, and T. Anderson, “Verdi: a framework for                      software verification,” in Proceedings of the IEEE/ACM 47th
     implementing and formally verifying distributed systems,”                  International Conference on Software Engineering, ser. ICSE
     in Proceedings of the 36th ACM SIGPLAN Conference                          ’25. IEEE Press, 2025, p. 347–359. [Online]. Available:
     on Programming Language Design and Implementation,                         https://doi.org/10.1109/ICSE55347.2025.00161
     ser. PLDI ’15. New York, NY, USA: Association for                     [43] H. Lee, H. Shin, and S.-L. Min, “Worst case timing requirement
     Computing Machinery, 2015, p. 357–368. [Online]. Available:                of real-time tasks with time redundancy,” in Proceedings Sixth
     https://doi.org/10.1145/2737924.2737958                                    International Conference on Real-Time Computing Systems and
[32] G. Klein, K. Elphinstone, G. Heiser, J. Andronick, D. Cock,                Applications. RTCSA’99 (Cat. No.PR00306), 1999, pp. 410–
     P. Derrin, D. Elkaduwe, K. Engelhardt, R. Kolanski,                        414.
     M. Norrish, T. Sewell, H. Tuch, and S. Winwood, “sel4: formal         [44] E. First and Y. Brun, “Diversity-driven automated formal
     verification of an os kernel,” in Proceedings of the ACM                   verification,” in Proceedings of the 44th International
     SIGOPS 22nd Symposium on Operating Systems Principles,                     Conference on Software Engineering, ser. ICSE ’22.
     ser. SOSP ’09. New York, NY, USA: Association for                          New York, NY, USA: Association for Computing
     Computing Machinery, 2009, p. 207–220. [Online]. Available:                Machinery, 2022, p. 749–761. [Online]. Available:
     https://doi.org/10.1145/1629575.1629596                                    https://doi.org/10.1145/3510003.3510138
[33] R. J. George, J. Cruden, X. Zhong, H. Zhang, and                      [45] E. First, Y. Brun, and A. Guha, “Tactok: semantics-aware
     A. Anandkumar, “Torchlean: Formalizing neural networks                     proof synthesis,” vol. 4, no. OOPSLA, Nov. 2020. [Online].
     in lean,” 2026. [Online]. Available: https://arxiv.org/abs/2602.           Available: https://doi.org/10.1145/3428299
     22631                                                                 [46] S. Baruah, A. Mok, and L. Rosier, “Preemptively scheduling
[34] K. Bedarkar, M. Vardishvili, S. Bozhko, M. Maida, and B. B.                hard-real-time sporadic tasks on one processor,” in [1990]
     Brandenburg, “From intuition to coq: A case study in verified              Proceedings 11th Real-Time Systems Symposium, 1990, pp.
     response-time analysis 1 of fifo scheduling,” in 2022 IEEE Real-           182–190.
     Time Systems Symposium (RTSS), 2022, pp. 197–210.
[35] M. Maida, S. Bozhko, and B. B. Brandenburg, “Foundational
     Response-Time Analysis as Explainable Evidence of Timeliness
     (Artifact),” Dagstuhl Artifacts Series, vol. 8, no. 1, pp. 7:1–7:2,
     2022. [Online]. Available: https://drops.dagstuhl.de/entities/
     document/10.4230/DARTS.8.1.7
[36] P. Roux, S. Quinton, and M. Boyer, “A Formal Link Between
     Response Time Analysis and Network Calculus (Artifact),”
                                                        A PPENDIX
A. Illustrative Example with W ORST-C ASE T IMING R EQUIREMENTS OF R EAL -T IME TASKS WITH T IME R EDUNDANCY
  1) Extracted JSON and Informal Sketch for Illustrative Example: Listing 3 presents the extracted json that is used for the
Section VI.

                                Listing 3: Structured extraction of Definition 1 and Claim 1
[
    {
      "type": "definition",
      "identifier": "Definition 1",
      "formal_description": {
         "statement": "W_i_k_i = W_i_0 + A_i_k_i",
         "variables": {
            "W_i_k_i": "Worst case timing requirement of task
                         tau_i in the presence of k_i faults",
            "W_i_0": "Failure-free computational requirement
                       (WCET) of task tau_i",
            "A_i_k_i": "Worst case value of additional
                         reprocessing time and overhead to
                         tolerate k_i faults"
         },
         "assumptions": [
            "Faults are transient or intermittent",
            "Faults are detected immediately upon occurrence"
         ],
         "conclusion": "Defines the total time a task requires
                         to complete its execution and recovery
                         actions."
      },
      "informal_sketch": {
         "intuition": "The total time a task needs is its
                        normal execution time plus the maximum
                        possible time spent on fault detection,
                        recovery, and re-execution.",
         "steps": [
            "Identify the base execution time without faults
             W_i_0",
            "Calculate the maximum overhead A_i_k_i based on
             the specific redundancy technique used",
            "Sum them to find the total timing requirement"
         ],
         "key_insights": [
            "Separates the functional execution time from the
             fault-tolerance overhead"
         ]
      },
      "dependencies": []
    },
    {
      "type": "claim",
      "identifier": "Claim 1",
      "formal_description": {
         "statement": "W_i_k_i = k_i * (R_star + W_i_0)
                        + W_i_0",
         "variables": {
            "W_i_k_i": "Worst case timing requirement for
                         retry",
            "k_i": "Number of faults",
            "R_star": "Task restart overhead (constant)",
            "W_i_0": "Failure-free WCET"
         },
         "assumptions": [
            "Task must restart from the very beginning after
             every fault"
         ],
          "conclusion": "Calculates the WCTR for the Retry
                         redundancy technique."
        },
        "informal_sketch": {
           "intuition": "If a fault occurs, the task loses all
                          progress and must restart. In the worst
                          case, a fault occurs just before
                          completion, requiring a full re-execution
                          plus restart overhead for every fault.",
           "steps": [
              "For each of the k_i faults, add the cost of a
               full restart (R_star) and a full re-execution
               (W_i_0)",
              "Add the final successful execution time (W_i_0)"
           ],
           "key_insights": [
              "Retry is the most expensive technique because it
               discards all work done prior to the fault"
           ]
        },
        "dependencies": ["Definition 1"]
    }
]
Listing 4 presents the informal sketch that is used for the Section VI. This sketch is formatted as structured ROCQ comments
and serves as the direct input to the skeleton code generation phase.
                            Listing 4: Informal sketch used as input to skeleton code generation
(*
====section====
definition Definition 1

Statement:
W_i_k_i = W_i_0 + A_i_k_i

Variables:
W_i_k_i: Worst case timing requirement of task
           tau_i in the presence of k_i faults
W_i_0: Failure-free computational requirement
        (WCET) of task tau_i
A_i_k_i: Worst case value of additional
           reprocessing time and overhead to
           tolerate k_i faults

Assumptions:
1. Faults are transient or intermittent
2. Faults are detected immediately upon occurrence

Conclusion:
Defines the total time a task requires to complete
its execution and recovery actions.

Intuition for generating code:
The total time a task needs is its normal execution
time plus the maximum possible time spent on fault
detection, recovery, and re-execution.

Steps for generating code:
1. Identify the base execution time without faults
   W_i_0
2. Calculate the maximum overhead A_i_k_i based on
   the specific redundancy technique used
3. Sum them to find the total timing requirement

Key Insights:
1. Separates the functional execution time from the
   fault-tolerance overhead
*)

(*
====section====
claim Claim 1

Statement:
W_i_k_i = k_i * (R_star + W_i_0) + W_i_0

Variables:
W_i_k_i: Worst case timing requirement for retry
k_i: Number of faults
R_star: Task restart overhead (constant)
W_i_0: Failure-free WCET

Assumptions:
1. Task must restart from the very beginning after
   every fault

Conclusion:
Calculates the WCTR for the Retry redundancy
technique.

Intuition for generating code:
If a fault occurs, the task loses all progress and
must restart. In the worst case, a fault occurs
just before completion, requiring a full
re-execution plus restart overhead for every fault.

Steps for generating code:
1. For each of the k_i faults, add the cost of a
   full restart (R_star) and a full re-execution
   (W_i_0)
2. Add the final successful execution time (W_i_0)

Key Insights:
1. Retry is the most expensive technique because it
   discards all work done prior to the fault
*)

B. IEEE Xplore API query
  We queried IEEE Xplore using schedulability-analysis and real-time-systems keywords.
     ("schedulability analysis" OR "schedulability" OR "response time analysis" OR
     "response-time analysis")
     AND ("real-time system" OR "real-time systems" OR "real-time task" OR "real-time
     scheduling" OR "worst-case execution time")
   The API also allows us to restrict the search to specific conferences. For this purpose, we selected leading conferences in
real-time systems and system automation. The conferences specified in our search are as follows:
     ("Real-Time Systems Symposium", "RTSS"), ("Real-Time and Embedded Technology and
     Applications Symposium", "RTAS"), ("Euromicro Conference on Real-Time Systems", "ECRTS"),
     ("Embedded Software", "EMSOFT"), ("Real-Time Computing Systems and Applications",
     "RTCSA"), ("Real-Time Networks and Systems", "RTNS"), ("Robotics: Science and Systems",
     "RSS"), ("Intelligent Robots and Systems", "IROS"),
C. Prosa Documentation Details
                                  TABLE V: Role of major P ROSA documentation modules.

 Module           Role in Documentation Processing
 Behavior         Core system semantics and basic concepts
 Model            Task, processor, priority, and scheduler assumptions
 Analysis         Reusable lemmas and intermediate proof developments
 Results          Complete verified schedulability theorems and proof examples
 Implementation   Executable instances and concrete schedulers
 Util             Mathematical lemmas, helper functions, and tactics
D. Pseudocode for skeleton code generation
  The pseudocode is presented in Algorithm 1

Algorithm 1 Phase 1: Skeleton Code Generation
Require: Sketch sections S, retry budget Ms
Ensure: Skeleton script P
 1: P ← ∅                                                                                                       ▷ accumulated script
 2: for each section si ∈ S do
 3:     Ci ← R ETRIEVE C ONTEXT(si )
 4:     ki ← I NFER K IND(si )
 5:     success ← f alse
 6:     for a ← 1 to Ms do
 7:         πi ← B UILD P ROMPT(si , Ci , P, ki )
 8:         bi ← G ENERATE B LOCK(πi )
 9:         bi ← N ORMALIZE(bi )
10:         if ¬C HECK S KELETON RULES(bi ) then
11:             continue
12:         end if
13:         if ¬C HECK A SSUMPTIONS(bi , si ) then
14:             continue
15:         end if
16:         P ′ ← C ONCAT(P, bi )
17:         if C OMPILE(P ′ ) then
18:             P ← P′
19:             U PDATE C ONTEXT(P, bi )
20:             success ← true
21:             break
22:         end if
23:     end for
24:     if success = f alse then
25:         return FAILURE(si )
26:     end if
27: end for
28: return P


E. Pseudocode for Batch Completion with Iterative Repair
  The pseudocode is presented in Algorithm 2
F. Illustrative Example with “Preemptively Scheduling Hard-Real-Time Sporadic Tasks on One Processor” [46]
   We illustrate another workflow of P ROVE -RT using a concrete schedulability analysis drawn from the RTS literature, starting
with the extraction of intermediate representations and leading to the final machine-verified P ROSA script.
   1) Source Material and Extraction: We consider the paper “Preemptively Scheduling Hard-Real-Time Sporadic Tasks on
One Processor” [46] as a representative example. From this paper, we extract the following definitions and lemma. In particular,
the lemma Optimality of the Deadline Algorithm. serves as the main target, as it establishes the optimality of
the deadline algorithm for sporadic task systems. This lemma relies on several preceding modeling definitions.
Definition 1 (Sporadic Task Model). A sporadic task is defined as
                                                         Ti = (ei , di , pi ),
where ei is the execution time, di the relative deadline, and pi the minimum separation between consecutive requests, with
ei ≤ di and ei ≤ pi . A task system is a finite set τ = {T1 , . . . , Tn }.
Definition 2 (Request Model). A request of task Ti released at time t0 is represented as (i, t0 ). It requires ei units of processor
time in the interval
                                                          [t0 , t0 + di ),
so its absolute deadline is t0 + di .
Definition 3 (Legal Request Sets and Feasibility). A request set is legal if two requests of the same task are separated by
at least pi :
                                                    |t1 − t2 | ≥ pi .
A task system is feasible if every legal request set can be scheduled without missing deadlines. Thus, feasibility is a universal
property over all legal sporadic arrivals.
Algorithm 2 Phase 2a: Batch Completion with Compiler-Guided Repair
Require: Skeleton sections B, retry budget Mb
Ensure: Completed script P
 1: P ← ∅                                                                                                      ▷ completed script
 2: for each section Bi ∈ B do
 3:     if ¬H AS A DMITTED(Bi ) then
 4:         P ← C ONCAT(P, Bi )
 5:         continue
 6:     end if
 7:     Ci ← R ETRIEVE C ONTEXT(Bi )
 8:     πi ← B UILD C OMPLETION P ROMPT(Bi , Ci , P )
 9:     pi ← G ENERATE P ROOF(πi )
10:     Bi′ ← R EPLACE A DMITTED(Bi , pi )
11:     P ′ ← C ONCAT(P, Bi′ )
12:     success ← C OMPILE(P ′ )
13:     for a ← 1 to Mb do
14:         if success then
15:             break
16:         end if
17:         ei ← E XTRACT E RROR(P ′ )
18:         ρi ← B UILD R EPAIR P ROMPT(Bi′ , Ci , ei )
19:         pi ← R EPAIR P ROOF(ρi )
20:         Bi′ ← A PPLY R EPAIR(Bi′ , pi )
21:         P ′ ← C ONCAT(P, Bi′ )
22:         success ← C OMPILE(P ′ )
23:     end for
24:     if success then
25:         P ← P′
26:         M ARK C OMPLETED(Bi′ )
27:     else
28:         P ← C ONCAT(P, Bi )
29:         M ARK FAILED(Bi )
30:     end if
31: end for
32: return P



Definition 4 (Online Scheduling and Failure). An online scheduler decides at each time which active request executes. A
request (i, t0 ) is active at time t if
                                                  t0 ≤ t < t 0 + d i
and it has not yet received ei units of execution. The scheduler reports failure when a request reaches its deadline without
receiving enough execution.
Definition 5 (Deadline Algorithm). The deadline algorithm selects, at each time, the active request with the earliest absolute
deadline. For two active requests (i, t1 ) and (j, t2 ), it chooses (i, t1 ) if
                                                          t1 + di < t2 + dj .
Ties are resolved using a fixed task-index order.
Lemma 1 (Optimality of the Deadline Algorithm). The lemma states that the deadline algorithm is optimal for sporadic
task systems. For any request set, if some feasible schedule exists, then the deadline algorithm also constructs one; otherwise,
it reports failure. Therefore,
                                       τ is feasible ⇐⇒ the deadline algorithm succeeds
                                                            for every legal request set.

These results are automatically extracted and structured using LLM. Besides identifying the formal statement, variables,
assumptions, and conclusion of each invariant, the extraction also produces an informal sketch. The Informal Sketch 5
was extracted for this proof construct

                         Listing 5: Extracted Informal Sketch for Optimality of the Deadline Algorithm.

(*
====section====
definition Definition 1

Statement:
A sporadic task task_i is a triple task_i = e_i, d_i, p_i where e_i, d_i, and p_i are positive
    integers, e_i <= d_i, and e_i <= p_i. A sporadic task system task_system is a finite set
    task_system = task_1, task_2, ..., task_n.

Variables:
task_i: sporadic task i
task_system: set of sporadic tasks
e_i: execution time of task_i
d_i: relative deadline of task_i
p_i: minimum separation between successive requests of task_i
n: number of tasks

Assumptions:
1. single processor
2. preemptive scheduling
3. discrete time model
4. e_i, d_i, p_i are positive integers
5. e_i <= d_i
6. e_i <= p_i

Conclusion:
Defines the sporadic task model and the task-system model.

Intuition for generating code:
Each sporadic task can release jobs at arbitrary times, but not too frequently. The parameter
    p_i prevents infinitely dense releases, while e_i and d_i describe how much processor time
    each released job needs and when it must complete.

Steps for generating code:
1. Represent each task task_i by execution time e_i, deadline d_i, and minimum separation p_i.
2. Require e_i <= d_i so that each individual job can fit inside its own deadline window.
3. Require e_i <= p_i so that the task does not request more execution than its minimum
    inter-arrival spacing can plausibly support.
4. Collect all tasks into task_system.

Key Insights:
1. The minimum separation p_i is the key distinction between sporadic and arbitrary aperiodic
    arrivals.
2. The model allows d_i > p_i, so jobs of the same task may have overlapping deadline windows.

*)

(*
====section====
definition Definition 2

Statement:
Let P = lcm(p_1, p_2, ..., p_n). A request of task_i at time t_0 is represented by
    request_i_t_0 = i, t_0. The request requires e_i units of processor allocation in interval
    [t_0, t_0 + d_i).

Variables:
P: least common multiple of all minimum separations p_i
request_i_t_0: request of task_i released at time t_0
t_0: release time of a request
e_i: execution requirement of task_i
d_i: relative deadline of task_i
p_i: minimum separation of task_i

Assumptions:
1. task_i belongs to task_system
2. t_0 >= 0
3. time is discrete
Conclusion:
Defines task requests and their execution windows.

Intuition for generating code:
A sporadic task generates individual requests or jobs. A request released at t_0 must receive
    e_i units of service before its absolute deadline t_0 + d_i.

Steps for generating code:
1. Take a task task_i and release time t_0.
2. Construct request_i_t_0.
3. Set the absolute deadline to t_0 + d_i.
4. Require the scheduler to allocate e_i time units inside [t_0, t_0 + d_i).

Key Insights:
1. Schedulability is checked over requests, not just over task parameters.
2. The absolute deadline is release_time plus relative deadline.

*)

(*
====section====
definition Definition 3

Statement:
A set of requests request_set is schedulable iff there exists a processor schedule that
    allocates e_i time units to every request request_i_t_0 in request_set within [t_0, t_0 +
    d_i). A set request_set is legal iff for any two requests request_i_t_1 and request_i_t_2
    of the same task, abs(t_1 - t_2) >= p_i. The task_system is feasible iff every legal
    request_set is schedulable.

Variables:
request_set: set of task requests
request_i_t_0: request of task_i released at t_0
t_1: release time of one request
t_2: release time of another request
p_i: minimum separation of task_i
task_system: sporadic task system

Assumptions:
1. single processor
2. preemptive scheduling
3. all requests satisfy their task parameters

Conclusion:
Defines schedulability of a request set, legality of arrivals, and feasibility of a sporadic
    task system.

Intuition for generating code:
A request set is legal if it respects the sporadic separation constraints. A task system is
    feasible only if every possible legal arrival pattern can be scheduled without missing
    deadlines.

Steps for generating code:
1. Check all pairs of requests of the same task.
2. If any two releases are closer than p_i, the request set is illegal.
3. If the request set is legal, ask whether a valid preemptive single-processor schedule
    exists.
4. The task system is feasible only when every legal request set has such a schedule.

Key Insights:
1. Feasibility is a universal property over all legal arrival sequences.
2. The difficulty comes from the unbounded number of possible legal sporadic request sets.

*)

(*
====section====
definition Definition 4

Statement:
An online scheduling algorithm U maps each request_set and time t to either a selected active
    request request_i_t_0, an idle decision, and optionally failure. A request request_i_t_0
    is active at time t iff t_0 <= t < t_0 + d_i and the request has not yet received e_i
    units of processor allocation in [t_0, t). U reports failure at time t iff there exists
    request_i_t_0 such that t_0 + d_i = t and the request has received less than e_i units in
    [t_0, t).

Variables:
U: online scheduling algorithm
request_set: set of requests presented to U
t: current time
request_i_t_0: request of task_i released at t_0
active: predicate indicating that a request is pending and before its deadline
failure: event indicating a missed deadline

Assumptions:
1. requests are presented to U at their release times
2. U is online and iterative
3. preemption is allowed at integer time boundaries

Conclusion:
Defines online scheduling, active requests, and failure.

Intuition for generating code:
At each time, the scheduler either runs one active request or idles. Failure occurs exactly
    when a request reaches its deadline without having received enough execution.

Steps for generating code:
1. At each time t, identify all active requests.
2. Choose one active request to execute or leave the processor idle.
3. Update the amount of service received by the chosen request.
4. If any request reaches its deadline without receiving e_i service, report failure.

Key Insights:
1. Failure is defined at the deadline boundary.
2. The active-request definition captures unfinished jobs that are still eligible to execute.

*)

(*
====section====
definition Definition 5

Statement:
The deadline algorithm U allocates the processor at time t to the active request with the
    nearest absolute deadline. For active requests request_i_t_1 and request_j_t_2, U chooses
    request_i_t_1 over request_j_t_2 if t_1 + d_i < t_2 + d_j, or if t_1 + d_i = t_2 + d_j and
    i < j.

Variables:
U: deadline algorithm
request_i_t_1: active request of task_i released at t_1
request_j_t_2: active request of task_j released at t_2
t_1_plus_d_i: absolute deadline of request_i_t_1
t_2_plus_d_j: absolute deadline of request_j_t_2

Assumptions:
1. preemptive scheduling
2. single processor
3. ties are broken by lower task index

Conclusion:
Defines the deadline-driven scheduling algorithm used throughout the paper.
Intuition for generating code:
The deadline algorithm is earliest-deadline-first with a deterministic tie-breaking rule. The
    request whose deadline is closest gets the processor.

Steps for generating code:
1. At time t, collect all active requests.
2. Compute each active request’s absolute deadline.
3. Select the request with the smallest absolute deadline.
4. If two requests have the same absolute deadline, choose the one with smaller task index.

Key Insights:
1. The algorithm is EDF specialized to the paper’s request model.
2. Tie-breaking does not affect whether failure occurs, but makes the schedule deterministic.

*)

(*
====section====
lemma Lemma 1

Statement:
The deadline_algorithm_U is optimal for sporadic task systems. Given any request_set, U
    constructs a schedule for request_set if one exists; otherwise U reports failure at some
    time. Therefore task_system is feasible iff U constructs a schedule for every legal
    request_set.

Variables:
deadline_algorithm_U: earliest-deadline scheduling algorithm
request_set: set of requests
task_system: sporadic task system

Assumptions:
1. single processor
2. preemptive scheduling
3. sporadic request model
4. legal request sets respect minimum separations

Conclusion:
EDF-style deadline scheduling is sufficient to decide feasibility over legal request sets.

Intuition for generating code:
For preemptive uniprocessor scheduling, always running the active job with the earliest
    deadline is optimal: if any schedule can meet all deadlines, the deadline algorithm can
    also meet them.

Steps for generating code:
1. Consider any legal request set.
2. Run the deadline algorithm on that request set.
3. If any feasible schedule exists, the deadline algorithm also succeeds.
4. If the deadline algorithm fails, no feasible schedule exists for that request set.
5. Thus task_system is feasible exactly when the deadline algorithm never fails on any legal
    request set.

Key Insights:
1. This lemma lets the paper focus on one canonical scheduler rather than all possible
    schedules.
2. It converts feasibility into absence of failure under the deadline algorithm.

*)
   The extraction is also dependency-aware. For each invariant, we record its dependencies on previously introduced invariants,
inducing a partial order for formalization. An invariant is formalized only after all dependencies have been processed. For
example, Lemma 1 depends on Definitions 1–5, which must therefore be formalized first. Since P ROSA/ROCQ requires all
referenced constructs to be defined before use, dependency-aware ordering is necessary for successful compilation.
   2) Retrieval-Augmented Generation: Given the informal sketch of an invariant, the next step is to translate it into a P ROSA
script. To support this translation, we employ retrieval-augmented generation (RAG) over the P ROSA codebase. We use the
statement, conclusion, and intuition fields from the informal sketch as a joint query and retrieve the top-k results from two
complementary sources: (i) example scripts that demonstrate similar constructs or proof patterns, and (ii) documentation
fragments describing the syntax, semantics, and usage conventions of relevant P ROSA modules. Together, these provide the
LLM with sufficient context to generate correct and idiomatic code.
   3) Skeleton Code Generation: Using the retrieved context, we prompt the LLM to generate skeleton code—a structurally
complete, type-checkable P ROSA script in which all imports, section boundaries, type-class contexts, variable declarations, and
definition bodies are fully specified, while every proof obligation is replaced by Admitted. Listing 6 shows the skeleton
code generated for the motivating example.
Listing 6: Skeleton code generated from the informal sketch. All structural elements are fully elaborated; the proof body is
deferred via Admitted.


From mathcomp Require Import all_ssreflect.
Require Import prosa.model.task.concept.
Require Import prosa.model.task.arrival.sporadic.
Require Import prosa.model.priority.edf.
Require Import prosa.model.processor.ideal.
Require Import prosa.model.readiness.basic.
Require Import prosa.analysis.definitions.schedulability.
Require Import prosa.analysis.facts.behavior.completion.
Require Export prosa.results.edf.optimality.

Section SporadicEDFOptimality.

  Context {Task : TaskType} ‘{TaskCost Task} ‘{TaskDeadline Task} ‘{SporadicModel Task}.
  Context {Job : JobType} ‘{JobTask Job Task} ‘{JobArrival Job} ‘{JobCost Job} ‘{JobDeadline Job}.
  Variable ts : seq Task.   (* the sporadic task system tau = {T_1,...,T_n} *)
  Hypothesis H_job_deadline_def :
    forall j, job_deadline j = job_arrival j + task_deadline (job_task j).

  Definition valid_sporadic_task (tsk : Task) : Prop :=
    [/\ 0 < task_cost tsk,
        0 < task_deadline tsk,
        0 < task_min_inter_arrival_time tsk,
        task_cost tsk <= task_deadline tsk &
        task_cost tsk <= task_min_inter_arrival_time tsk ].

  Definition request_absolute_deadline (j : Job) : instant :=
    job_arrival j + task_deadline (job_task j).   (* = job_deadline j, by H_job_deadline_def *)

  Definition feasible : Prop :=
    forall arr_seq : arrival_sequence Job,
      valid_arrival_sequence arr_seq ->
      (forall tsk, tsk \in ts -> respects_sporadic_task_model arr_seq tsk) ->
      exists sched : schedule (ideal.processor_state Job),
        valid_schedule sched arr_seq /\ all_deadlines_of_arrivals_met arr_seq sched.

  Definition online_failure_at
      (arr_seq : arrival_sequence Job)
      (sched : schedule (ideal.processor_state Job)) (t : instant) : Prop :=
    exists j, arrives_in arr_seq j /\ job_deadline j = t /\ ˜˜ completed_by sched j t.

  Definition deadline_algorithm_U (sched : schedule (ideal.processor_state Job)) : Prop :=
    EDF_schedule sched.

  Lemma deadline_algorithm_optimal :
    feasible <->
    (forall arr_seq : arrival_sequence Job,
       valid_arrival_sequence arr_seq ->
       (forall tsk, tsk \in ts -> respects_sporadic_task_model arr_seq tsk) ->
       exists sched : schedule (ideal.processor_state Job),
         valid_schedule sched arr_seq /\
         all_deadlines_of_arrivals_met arr_seq sched /\
         deadline_algorithm_U sched).
  Proof. Admitted.

End SporadicEDFOptimality.

  The skeleton maps each extracted section to a corresponding P ROSA construct. Definition 1 is encoded as
valid_sporadic_task, using task_cost, task_deadline, and task_min_inter_arrival_time for ei ,
di , and pi . Definition 2 is encoded as request_absolute_deadline, representing the absolute deadline t0 + di .
Definition 3 is encoded as feasible, which quantifies over all legal arrival sequences. Definition 4 is encoded as
online_failure_at, capturing missed deadlines, and Definition 5 is encoded as deadline_algorithm_U, identified
with P ROSA’s EDF_schedule. Lemma 1 is encoded as deadline_algorithm_optimal, stating that feasibility is
equivalent to success of the deadline algorithm on every legal request set.
    The surrounding type-class context, including TaskType, JobType, and TaskCost, connects these constructs to P ROSA’s
scheduling framework. The Admitted. directive is used only as a temporary placeholder, allowing the skeleton to type-check
before the proof is synthesized, with the final proof expected to rely on P ROSA’s EDF_optimality theorem.
    4) Proof Completion: In the final phase, we prompt the LLM to discharge the Admitted obligations using the complete
skeleton, retrieved RAG context, and an instruction to complete a specific proof block. Providing the full skeleton gives the
model access to surrounding definitions, instances, and auxiliary lemmas, improving proof generation. For this example, the
LLM produces the following proof in Listing 7:

                           Listing 7: Completed proof for the Optimality of the Deadline Algorithm
    Lemma deadline_algorithm_optimal :
    feasible <->
    (forall arr_seq : arrival_sequence Job,
        valid_arrival_sequence arr_seq ->
        (forall tsk, tsk \in ts -> respects_sporadic_task_model arr_seq tsk) ->
        exists sched : schedule (ideal.processor_state Job),
          valid_schedule sched arr_seq /\
          all_deadlines_of_arrivals_met arr_seq sched /\
          deadline_algorithm_U sched).
  Proof.
    rewrite /feasible /deadline_algorithm_U.
    split.
    - move=> FEAS arr_seq VALID SPORADIC.
       apply: EDF_optimality.
       have [sched [VALID_SCHED DEADLINES_MET]] :=
         FEAS arr_seq VALID SPORADIC.
       by exists sched.
    - move=> EDF_FEAS arr_seq VALID SPORADIC.
       have [sched [VALID_SCHED [DEADLINES_MET EDF_SCHED]]] :=
         EDF_FEAS arr_seq VALID SPORADIC.
       by exists sched.
  Qed.

   The proof follows the two directions of the equivalence. First, rewrite /feasible /deadline_algorithm_U
unfolds the extracted definitions, reducing the statement to the relationship between general feasibility and existence of an
EDF schedule. In the forward direction, the assumption FEAS provides some valid schedule that meets all deadlines for any
legal arrival sequence. The proof then applies EDF_optimality, which states that if such a feasible schedule exists, then
an EDF schedule also exists.
   In the reverse direction, the assumption already provides a valid schedule that meets all deadlines and additionally satisfies
EDF_schedule. Since feasibility only requires the existence of some valid schedule meeting all deadlines, the EDF-specific
condition is discarded. Thus, the completed proof shows that the extracted lemma deadline_algorithm_optimal is a
valid P ROSA formalization of the paper’s claim that the deadline algorithm is optimal for preemptive uniprocessor sporadic
task systems. This example demonstrates how our pipeline systematically transforms informal real-time scheduling results
into machine-verified P ROSA proofs through a structured sequence of extraction, retrieval-augmented skeleton generation, and
targeted proof completion.
G. Distribution of system invariants and their number of dependencies in the generated System Invariant Dataset
   Figure 6 shows the distribution of the total number of invariants per sketch, defined as the target invariant plus its associated
dependencies. The frequency decreases as the number of dependencies increases, indicating that highly dependent invariants
are less common in the extracted corpus.
H. Fine-Grained Mapping from Raw Sketch Kinds to ROCQ Keywords
   Table VI presents the complete mapping from raw sketch kinds to their corresponding ROCQ keywords, along with the
rationale used in our normalization process.
                              Fig. 6: Distribution of system invariants and their dependencies.

                       TABLE VI: Fine-grained mapping from raw sketch kinds to ROCQ keywords.

Raw Sketch Kind                     ROCQ Keyword           Reason
Definition family
definition                          Definition             Direct equivalent
formula                             Definition             A named mathematical formula = constant definition
equation                            Definition             A named equation = defined constant/relation
implicit definition                 Definition             Implicitly defined concept
derived definition                  Definition             Derived from other definitions
foundational equation               Definition             Named base equation = constant
rta equation                        Definition             Response-time analysis equation = named bound constant
calculation formula                 Definition             A formula used in calculation = named constant
derived formula                     Definition             Derived formula = defined constant
resource planning formula           Definition             Formula for planning = named constant
objective function                  Definition             Optimization objective = a function definition
optimization objective              Definition             Same as objective function
derived function                    Definition             Derived non-recursively (not Fixpoint)
function                            Definition             Non-recursive function
formulation                         Definition             Mathematical formulation = a definition
task set definition                 Definition             Explicit definition of a task set
informal definition                 Definition             Informal but definitional in nature
Fixpoint family
algorithm                           Fixpoint               Algorithms are recursive = Fixpoint
algorithmic sketch                  Fixpoint               Sketch of a recursive algorithm
informal algorithmic sketch         Fixpoint               Informal version of algorithmic sketch
algorithm sketch                    Fixpoint               Same as algorithmic sketch
algorithm component                 Fixpoint               Part of a recursive algorithm
algorithm definition                Fixpoint               Defines a recursive algorithm
algorithm description               Fixpoint               Describes an algorithm
algorithmic derivation              Fixpoint               Algorithmically derived result
algorithmic definition              Fixpoint               Formally defined algorithm
transformation algorithm            Fixpoint               An algorithm that transforms its input
method                              Fixpoint               Computational method = procedure
procedure                           Fixpoint               Explicit computational procedure
heuristic                           Fixpoint               Iterative/recursive computational procedure
recurrence                          Fixpoint               Recurrence relation = recursive definition
Lemma family
lemma                               Lemma                  Direct equivalent
claim                               Lemma                  A claim is an auxiliary provable fact
                TABLE VI: Fine-grained mapping from raw sketch kinds to ROCQ keywords (continued).

Raw Sketch Kind                    ROCQ Keyword       Reason
proposition                        Lemma              Proposition = Lemma in ROCQ convention
observation                        Lemma              An observation is an informal lemma
property                           Lemma              A provable proposition
statement                          Lemma              A mathematical statement to be proved
formal statement                   Lemma              Formal version of a statement
condition                          Lemma              A provable condition/predicate
constraint                         Lemma              Proved inequality or bound
calculation                        Lemma              Result of a calculation = proved equality
schedulability test                Lemma              Decidable test = proved as lemma
derived test                       Lemma              A test derived from other results
optimization constraint            Lemma              Proved inequality/bound
optimization claim                 Lemma              Claim about an optimisation
application                        Lemma              Instantiation of a result
invariant                          Lemma              System/loop invariants proved as lemmas
remark                             Lemma              Remarks are informal lemmas
fact                               Lemma              A mathematical fact
result                             Lemma              A proved result
restriction                        Lemma              A restriction = conditional lemma
conjecture                         Lemma              Unproved; placeholder with Admitted
property/constraint                Lemma              Combined property/constraint
problem                            Lemma              Decision/optimisation problem
rule                               Lemma              Inference rule = proved as lemma
optimization problem               Lemma              Proved bound/property
schedulability condition           Lemma              Schedulability condition = proved predicate
problem statement                  Lemma              Problem stated formally
inequality                         Lemma              A proved inequality
known result                       Lemma              Existing proved result
principle                          Lemma              e.g. scheduling principle = proved property
derived rta                        Lemma              Response-time bounds are proved, not defined
extension                          Lemma              Extends an existing lemma
transformation                     Lemma              Proved equivalence under transformation
refinement                         Lemma              Proved relationship between specifications
informal sketch                    Lemma              Informal sketch of a proof obligation
informal                           Lemma              Generic informal mathematical statement
policy                             Lemma              Scheduling policy property = provable proposition
incomplete malformed statement     Lemma              Safe fallback
Theorem / Corollary / Hypothesis families
theorem                            Theorem            Direct equivalent
corollary                          Corollary          Direct equivalent
hypothesis                         Hypothesis         Direct equivalent
assumption                         Hypothesis         Explicit assumption in a ROCQ Section context
