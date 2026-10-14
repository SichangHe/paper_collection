                                             Learning-Infused Formal Reasoning: From
                                          Contract Synthesis to Artifact Reuse and Formal
                                                             Semantics

                                         Arshad Beg1*† , Diarmuid O’Donoghue1† and Rosemary Monahan1†
                                           1*
                                                Department of Computer Science, Maynooth University, Ireland.
arXiv:2602.02881v2 [cs.SE] 16 Jun 2026




                                                   *Corresponding author(s). E-mail(s): arshad.beg@mu.ie;
                                                     Contributing authors: diarmuid.odonoghue@mu.ie;
                                                                 rosemary.monahan@mu.ie;
                                                      †
                                                        These authors contributed equally to this work.


                                                                               Abstract
                                           This paper articulates a long-term research vision for formal methods at the
                                           intersection with artificial intelligence, outlining multiple conceptual and techni-
                                           cal dimensions and reporting on our ongoing work toward realising this vision. It
                                           advances a forward-looking perspective on the next generation of formal methods
                                           based on the integration of automated contract synthesis, semantic artifact reuse,
                                           and refinement-based theory. We argue that future verification systems must
                                           builds towards individual correctness proofs toward a cumulative, knowledge-
                                           driven paradigm in which specifications, contracts, and proofs are continuously
                                           synthesised and transferred across systems. To support this shift, we outline a
                                           hybrid framework combining large language models with graph-based represen-
                                           tations to enable scalable semantic matching and principled reuse of verification
                                           artifacts. Learning-based components provide semantic guidance across heteroge-
                                           neous notations and abstraction levels, while symbolic matching ensures formal
                                           soundness. Grounded in compositional reasoning, this vision points toward veri-
                                           fication ecosystems that evolve systematically, leveraging past verification efforts
                                           to accelerate future assurance.

                                           Keywords: Formal Reasoning, Formal Verification, Contract Synthesis, Graph
                                           Construction, Graph Matching, Unifying Theory of Programming, Theory of
                                           Institutions




                                                                                    1
1 Introduction
Over the past decade, AI has advanced at an incredible pace. Deep learning and
large language models now handle language, images, and decision-making with impres-
sive fluency. Yet despite this progress, these systems remain hard to trust. They are
opaque, they can fail without warning, and they offer no clear guarantees of safety
or correctness–problems that matter deeply in high-stakes settings. Formal methods
offer something AI currently lacks: solid, mathematical guarantees about how a system
behaves. They support engineers in writing precise rules and providing proofs that a
system follows them. However, these techniques struggle with today’s large and con-
stantly changing AI systems:specifications are difficult to maintain, proofs grow quickly
in complexity, and symbolic tools alone cannot scale to modern learned components.
    Recent research hints at a way forward. Learning can speed up proof search,
propose useful specifications, and guide testing. Formal reasoning, in turn, is being
extended to handle neural networks and other learned models. However, many cur-
rent solutions target narrow problems, missing is a unified foundation. Our vision,
which we call Learning-Infused Formal Reasoning (LIFR), aims to bring these solu-
tions together, by creating a steady feedback loop where learning helps automate and
adapt formal reasoning tasks, while formal methods ensure that the results remain
sound and reliable. Techniques like automated contract synthesis and LLM-guided
discovery of verification artifacts become part of a common framework supported by
rigorous semantics. By integrating learning, reuse, and formal foundations, we will
move beyond ad hoc tool combinations toward a principled way of building intelligent
systems that are both powerful and trustworthy.
    Now we present our recent contributions. The paper Beg et al. (2025a) offers
a structured look at the challenges of turning informal, natural-language require-
ments into precise formal specifications. It highlights how ambiguity, missing domain
models, contextual gaps, and the instability of current LLMs jointly make consis-
tent and reliable formalisation difficult. A key contribution is the introduction of
the VERIFYAI research framework, which proposed to integrate LLMs with NLP
pipelines, ontology-driven modelling, and artefact-reuse mechanisms to support semi-
automated derivation of verifiable specifications. The paper also offers a focused
synthesis of early state-of-the-art approaches–such as Req2Spec, SpecGen, AssertLLM,
and nl2spec–systematically comparing how contemporary systems represent require-
ments, generate logical constraints, and interface with verification tools. Additionally,
it reports empirical evaluations across multiple SMT solvers (Alt-Ergo, Z3, CVC4,
CVC5) using Frama-C PathCrawler, providing comparative evidence on verification
success rates and solver execution times that highlight practical feasibility limits of
current formalisation pipelines.
    The more comprehensive study Beg et al. (2025b) significantly extends these con-
tributions by offering a large-scale synthesis of over one hundred studies that examine
AI-enabled approaches to requirements formalisation, traceability, and verification.
This work maps the broader landscape of LLM-based and AI-assisted techniques for
translating informal requirements into formal specifications across diverse program-
ming languages, specification notations, and verification backends, including model
checkers and theorem provers. The survey categorises the dominant methodological


                                           2
patterns used in recent tools. These patterns range from pattern-based rule extrac-
tion to logical constraint inference and hybrid neuro-symbolic pipelines. The survey
also identifies ecosystem-level challenges that remain largely unresolved. These chal-
lenges include barriers to toolchain integration, insufficient traceability mechanisms,
and limited reuse of existing specification artefacts.
    The work incorporates an expanded empirical investigation of Frama-C’s for-
mal analysis and test-generation ecosystem. The study evaluates the Runtime Error
(RTE) analyser, the Value Analysis (EVA) plugin, and the PathCrawler tool to deter-
mine their capability to infer assertions, generate ACSL annotations, detect runtime
anomalies, and produce targeted test cases for representative C programs. The find-
ings reveal persistent issues–including solver instability, path-coverage constraints,
and configuration sensitivities–that constrain automation reliability in real-world for-
malisation workflows. By proposing mitigation strategies such as dataset adaptation,
selective path-exploration heuristics, and fine-grained tool-configuration adjustments,
it proposes how coordinated, multi-tool, human-guided workflows can systematically
overcome these limitations. Together, these two contributions Beg et al. (2025a,b)
provide foundational exploration and experimental validation of AI-enabled formal
methods.
    Our research vision comprises of three threads: contract synthesis, artefact reuse,
and semantic foundations. Figure 1 presents the high-level conceptual architecture
that organises the research threads into the unified LIFR framework.




         Fig. 1: High-level conceptual architecture of the LIFR framework.


    The structure of the paper is as follows: Section 2 presents our vision of research
in the area of contract synthesis. Subsection 2.4 briefs our contribution addressing
contract synthesis. Section 3 explores the role of LLMs in graph matching for artefact
reuse. Subsection 3.3 summaries our on-going work, while Section 4 describes the
formal semantic foundations. Section 5 summarises the challenges and future directions
identified in Beg et al. (2025b). Section 6 concludes the paper.




                                           3
2 Contract Synthesis
This section articulates a research vision for contract synthesis situated within the pro-
posed VERIFYAI framework Beg et al. (2025a). Rather than presenting a completed
implementation, we outline a forward-looking architectural blueprint for how large
language models (LLMs), verification engines, and human-centred oversight could be
combined to support semantically rigorous specification workflows. The aim is to char-
acterise the methodological foundations required for transforming natural-language
requirements into verifiable program contracts while avoiding assumptions of system
maturity or deployment. In contrast to the artifact reuse setting of Section 3, which
focuses on semantic alignment between existing formal artefacts, the present section
concentrates on the initial construction of contracts from informal descriptions and
on the principles needed to ensure their correctness, traceability, and interpretability.
The following subsections develop this vision by analysing the challenges of require-
ment formalisation, motivating neuro-symbolic synthesis, and describing the intended
architectural components of VERIFYAI as a conceptual pipeline.

2.1 From Natural Language to Verifiable Contracts
The proposed VERIFYAI framework is motivated by long-standing difficulties in
converting informal requirements into precise, machine-verifiable annotations. Prior
studies Beg et al. (2025a,b) highlight that natural-language descriptions often contain
latent assumptions, contextual dependencies, and domain-specific conventions that are
not directly compatible with the rigid semantic formats required by formal verifica-
tion environments. LLMs provide new opportunities for interpreting such descriptions,
but their outputs are susceptible to ambiguity, instability, and hallucination, espe-
cially when required to produce logically constrained structures such as preconditions,
postconditions, and invariants.
    Within VERIFYAI, contract synthesis is conceived as an iterative transformation
process rather than a direct translation. The framework envisions the use of controlled
prompting strategies that scaffold LLMs to extract candidate behavioural obligations
from textual descriptions. These candidates would then be subjected to validation
and refinement steps informed by formal verification feedback. Rather than assuming
that LLMs can inherently internalise program semantics, this process emphasises the
need for explicit alignment between linguistic intent and symbolic constraints. The
intended outcome is a synthesis workflow in which LLM-generated artefacts converge
toward logical adequacy through repeated interaction with verification tools, while
maintaining fidelity to the original requirements.

2.2 Architectural Foundations of Learning-Infused Contract
    Synthesis
The architectural sketch underpinning VERIFYAI comprises three complementary
technical pillars, each grounded in insights from the literature but intentionally
presented as a conceptual proposal rather than a realised system.




                                            4
    The first pillar concerns a structured prompting architecture shaped by the empir-
ical observations summarised in Beg et al. (2025a). These observations suggest that
LLM performance in specification-related tasks is heavily influenced by prompt design,
contextual cues, and the use of domain templates. VERIFYAI extends these findings
by outlining a family of prompt patterns and transformation routines intended to nor-
malise natural-language requirements, expose implicit semantic relations, and guide
the generation of candidate program contracts. This layer establishes the linguistic
and syntactic scaffolding needed for subsequent verification-aware refinement.
    The second pillar integrates formal verification into the generative loop. Verifi-
cation tools such as Frama-C, Z3, or Alt-Ergo are envisioned as active components
that provide structured feedback on the correctness and completeness of the gen-
erated annotations. Counterexamples, proof failures, and satisfiability results would
be used to reshape and constrain subsequent LLM outputs, thereby counteracting
hallucinations and enforcing semantic discipline. This neuro-symbolic interplay con-
ceptualises contract synthesis as a convergence process driven jointly by generative
heuristics and symbolic reasoning, without presupposing that such integration is
currently automated.
    The third pillar focuses on traceability and expert oversight, drawing on the limi-
tations identified in Beg et al. (2025b). Current AI-assisted formalisation approaches
frequently lack mechanisms for documenting how generated contracts relate to initial
requirements, which complicates auditability and expert review. VERIFYAI proposes
a design in which mappings between requirements, generated annotations, and revi-
sion histories are explicitly recorded. This would support human-in-the-loop curation,
facilitate accountability, and enable engineers to understand and shape the evolution
of the specification artefacts. The purpose of this pillar is not to prescribe a fin-
ished interface, but to articulate the metadata and interaction patterns necessary for
trustworthy adoption in safety-critical domains.

2.3 Scalable and Semantically Grounded Contract Synthesis
The VERIFYAI proposal anticipates that contract synthesis must ultimately oper-
ate across diverse languages, verification platforms, and specification paradigms. This
end-points of specification distinguish contract construction from the artifact reuse
mechanisms discussed in Section 3. Here, the goal is not to discover correspondences
between pre-existing artefacts, but to ensure that newly synthesised contracts can
integrate flexibly into heterogeneous verification ecosystems.
    To this end, the conceptual architecture is intentionally language and tool-agnostic.
It is designed to accommodate ACSL-style annotations, SMT-based constraints, or
specifications for model checkers and theorem provers. This generality is informed
by limitations noted in Beg et al. (2025b), where vertically siloed toolchains hinder
interoperability and long-term maintainability. By foregrounding semantic grounding
and verifier-driven refinement, VERIFYAI aims to establish an extensible basis from
which specialised contract styles can be generated without compromising correctness.
    The long-term research direction implied by this architecture is that contract syn-
thesis may act as a foundational capability for a broader family of learning-enhanced
formal reasoning tasks. Synthesised contracts could serve downstream roles in model


                                           5
checking, symbolic execution, testing, or behavioural refinement, provided that their
semantics are precisely defined and traceable. Although VERIFYAI is presented purely
as a proposal, its envisioned integration of synthesis, verification, and expert oversight
outlines what such scalable and semantically principled workflows may eventually
require.

2.4 Empirical Advances in Contract Synthesis
Beg et al. (2026a) investigates the practical behaviour of automated contract synthesis
for C programs through the generation of ACSL annotations. The study evaluates five
approaches: our own rule-based Python script, the Frama-C RTE plugin, and three
large language models (DeepSeek, GPT-5, and OLMo3). The focus is on one-shot
annotation generation, where specifications are produced without iterative refinement.
All generated annotations are verified using the Frama-C WP plugin with multiple
SMT solvers under a controlled setup. A filtered subset of the CASP benchmark is
used to ensure consistency across experiments. The evaluation considers proof success
rates, solver timeouts, and internal processing time. This design allows a direct com-
parison between symbolic and learning-based approaches while isolating the effect of
annotation quality. The results provide a clear empirical basis for understanding the
current capabilities and limitations of automated contract generation methods.
    The findings show that rule-based approaches and the RTE plugin provide consis-
tent verification performance, particularly for safety-related properties such as runtime
checks. At the same time, LLM-based approaches demonstrate competitive effective-
ness, with verification success rates remaining in the range of 83–95% across models. In
addition to this strong baseline performance, LLMs generate a broader range of anno-
tations, including functional constraints that are not typically captured by rule-based
techniques. While some variability is observed in solver behaviour and processing time,
this reflects differences in the structure and richness of generated specifications rather
than a lack of capability. Differences across models are also evident, with DeepSeek
exhibiting relatively stable behaviour, though all evaluated models produce practically
useful annotations. Overall, the results indicate that LLM-based methods are viable
for contract generation and can be meaningfully integrated into verification workflows.
    These observations have direct implications for the contract synthesis proposed
in this paper. They support the view that synthesis should be treated as a guided
process where multiple generation strategies contribute complementary strengths.
Rule-based methods provide reliable coverage for safety properties, while LLMs extend
this coverage by introducing richer and more expressive candidate constraints. This
combination enables broader specification discovery without sacrificing verification
feasibility. Within the LIFR framework, this aligns with a neuro-symbolic loop in
which LLM-generated contracts are validated and refined through formal verification.
Practitioners can therefore adopt LLM-based annotation generation as part of their
workflow, particularly in contexts where specification effort is a bottleneck. The results
strengthen the case for integrating learning-based generation with symbolic reasoning
to build scalable and effective contract synthesis systems.




                                            6
3 LLMs and Graph Matching for Artifact Reuse
This section lays out a research vision for reuse of verification artifacts with the help of
large language models (LLMs) and graph matching. It focuses on how these techniques
can support the later stages of the verification lifecycle. In particular, it highlights
opportunities to discover, align, and adapt existing formal artefacts such as contracts,
specifications, and proofs. The goal is not to describe an implemented system, but
to articulate an architectural vision supported by empirical insights, identifying how
LLM-guided semantic inference and graph-theoretic structure could be integrated to
enable scalable reuse. Our approach is that similar implementations will have similar
specifications. Large repositories of verification artefacts already exist, yet their reuse
remains predominantly manual. Developers must search, compare, and adapt contracts
and proofs that may differ widely in syntax, abstraction level, or domain vocabulary. A
long-term research challenge is therefore to design principled mechanisms that capture
semantic correspondences between artefacts despite such variability. This section out-
lines how semantic graph representations, LLM-derived embeddings, and approximate
matching algorithms could form a unified conceptual foundation for this task.

3.1 Empirical Foundations from Knowledge-Graph and
    Ontology Research
Earlier work on graph-based representations of source code explored how formal
specifications could be propagated between implementations with similar structural
patterns Pitu et al. (2013). These studies demonstrated that graph abstractions can
support transfer of specifications and behavioural information across related programs.
More recent developments in knowledge-graph alignment, schema matching, and entity
matching provide stronger empirical support for hybrid approaches that combine
symbolic structure with neural representations. Current systems show that seman-
tic embeddings improve retrieval coverage and flexibility, while structural constraints
improve precision and reduce incorrect alignments Lippolis et al. (2023). Retrieval-
augmented reasoning over graph structures has also demonstrated that grounding
neural inference in symbolic representations can reduce hallucination and improve
consistency.
    Related evidence also comes from software engineering and ontology-engineering
workflows. Code-graph retrieval systems augmented with language models demon-
strate that neural methods are more effective when operating over structured
representations rather than raw text alone. Similarly, ontology-guided query gen-
eration and symbolic–neural hybrid pipelines show that structural grounding and
semantic interpolation are complementary capabilities Vasic et al. (2025). These obser-
vations align with our proposal that graph structure provides correctness-preserving
constraints, while neural embeddings support flexible semantic interpretation across
heterogeneous verification artefacts.




                                             7
3.2 Positioning Within the LIFR Framework
Effective reuse depends on identifying subtle semantic relationships between compo-
nents of verification artefacts. Programs, proofs, and specifications encode constraints
among variables, transitions, invariants, and obligations. These structures rarely align
through surface-level textual similarity alone, and in many cases only fragments of
behavioural intent are preserved across code refactorings, platform differences, or
architectural updates. For this reason, we view reuse as a problem of semantic match-
ing under partial equivalence and abstraction. This conceptualisation differs from
contract synthesis, where the challenge is to produce new formal artefacts; here, the
task is to uncover structural and semantic similarity within an existing ecosystem of
artefacts.
    To support a uniform treatment of diverse artefact types, we propose modelling
verification artefacts as typed, attributed graphs. Node types correspond to semantic
entities–state variables, predicates, transitions, or proof obligations–while edges encode
relations such as dataflow, control-flow, refinement, logical implication, or dependency.
This abstraction places programs, specifications, and proofs within a shared structural
representation, enabling reasoning across heterogeneous artefacts without privileging
any particular syntax. The graph formalism thus acts as the symbolic substrate upon
which semantic alignment can be explored.
    While graph structure captures the formal relations between artefact components,
it alone is insufficient for semantic matching in real-world contexts. Names, comments,
logical formulas, and auxiliary documentation contain additional meaning that cannot
be fully extracted via structural analysis. LLMs provide a mechanism for embedding
these heterogeneous linguistic and symbolic elements into a shared semantic space.
The proposal is not that LLMs determine correctness, but that they serve as seman-
tic oracles capable of suggesting correspondences between graph nodes that are not
syntactically aligned.
    Within this conceptual architecture, embeddings derived from LLMs enrich graph
nodes with semantic features reflecting linguistic descriptions, identifier conventions,
and latent domain knowledge. Approximate matching algorithms operating on these
enriched graphs could then search for candidate alignments supported both by struc-
tural consistency and by LLM-inferred similarity. This approach preserves semantic
nuance without requiring the LLM to perform global reasoning or to guarantee logical
soundness.
    Figure 2 illustrates the envisioned reuse pipeline, in which existing verification arte-
facts are first converted into typed, attributed graphs, then semantically enriched using
LLM-derived embeddings, and finally aligned through approximate graph matching
that combines structural constraints with semantic similarity. LLMs would provide
probabilistic semantic priors, while the graph layer would enforce global relational and
type constraints. This separation of roles is essential: LLMs excel at capturing contex-
tual semantics but are unreliable at enforcing formal structure, while graph algorithms
capture structure but struggle with linguistic ambiguity.
    Under this proposed architecture, reuse involves three steps: 1. Graph construction,
where artefacts are translated into typed, attributed graphs with precise relational



                                             8
  Verification Artefacts            Graph Construction              Semantic Enrichment                    Approximate Graph Matching
Programs, Specifications, Proofs   Typed & Attributed Graphs         LLM-Derived Embeddings                 Structure + Semantic Similarity




                                                                                              Refinement
                                                                                               Needed
                                                                   Graph-Based Adaptation
                                                                                                            Artefact Reuse & Retrieval
                                                                      Rewriting, Refinement




                                                                                                                            Verified




                                                                                                              Verification Completed



Fig. 2: Visionary workflow for verification artefact reuse via hybrid graph matching
and LLM-based semantic enrichment.


semantics. 2. Semantic enrichment, where each node receives an embedding, encod-
ing textual and symbolic meaning. 3. Approximate graph matching, where alignment
candidates are discovered by combining structural similarity with embedding-level
proximity.
    This process differs fundamentally from contract synthesis, which concerns gener-
ating new specifications; the reuse workflow instead emphasises structural comparison,
retrieval, and adaptation of existing artefacts. Identifying correspondences between
verification artefacts is only one stage of reuse; adaptation is equally important.
Once two specifications, proofs, or models have been aligned, portions of one artefact
may need to be transformed to fit the abstraction level or structural conventions of
the target context. Graph transformation theory provides a rigorous foundation for
such adaptations. Existing work demonstrates how graph rewriting rules can encode
insertions, deletions, refinements, and structural edits within proof assistants, pre-
serving semantic invariants during transformation steps Strecker (2007). We propose
leveraging these ideas to express modification rules for verification artefacts. Path-
expression–based views of graphs, which express relational constraints resembling
those in verification logics, offer an avenue for checking whether adaptations preserve
pre-established invariants. Integrated into a reuse pipeline, such transformations could
enable automated restructuring of specifications or proofs while maintaining the logical
relationships needed for downstream verification.
    This use of LLM within an iterative reasoning cycle is becoming an accepted
approach. General purpose frameworks like LangChain Topsakal and Akinci (2023)
and AutoGPT are gaining traction for supporting iterative development of LLM gen-
erated solutions to challenging problems. These systems support common approaches
like retrieval augment generation (RAG) and especially conversational histories in a
manner that’s agnostic of the specific LLM being used - even allowing a consortium
of multiple LLMs to be used.




                                                               9
3.3 Graph Construction and Matching for Artefact Reuse
Our on-going work Beg et al. (2026b) addresses the first step of artefact reuse, namely
the construction of uniform representations for programs and their specifications. The
study presents a pipeline that transforms imperative programs into typed, attributed
graphs. The evaluation spans multiple language and specification settings, including
C with ACSL, Java with JML, and Dafny for C#. The construction process com-
bines abstract syntax tree parsing with lightweight extraction of specification elements.
These are encoded as nodes and edges capturing control flow, data dependencies,
and contract-level information. The resulting graphs provide a consistent abstraction
across otherwise heterogeneous artefacts. This enables comparison at a structural level
while retaining key semantic elements. The work demonstrates that such graph repre-
sentations can be generated systematically and at scale, forming a practical basis for
further semantic analysis.
    A key aspect of the approach is the integration of neural embeddings with graph
structure. Node representations are enriched using models such as SentenceTrans-
former and CodeBERT, allowing semantic context to be captured alongside structural
relations. This combination supports more expressive similarity assessment, where
both program behaviour and specification intent contribute to matching. The results
show that embedding-enhanced graphs improve the identification of related artefacts
across datasets, even when surface syntax differs. Importantly, the approach remains
modular. Graph construction and semantic enrichment are treated as separate stages,
which simplifies extension and adaptation. This design also allows different embed-
ding models or domain-specific encodings to be incorporated without changing the
underlying graph structure.
    Within the LIFR framework, this work provides a concrete foundation for seman-
tic artefact reuse. It shows that reuse can be framed as a problem of alignment over
structured and enriched representations rather than direct syntactic comparison. The
constructed graphs act as a bridge between symbolic program structure and learned
semantic similarity. This aligns with the broader goal of combining formal represen-
tations with neural methods in a controlled manner. The results also support the
feasibility of approximate graph matching as a next step, where structural constraints
and embedding similarity can be jointly exploited. For practitioners, the pipeline
demonstrates that reusable representations can be derived from existing codebases
with limited manual effort. Overall, this work strengthens the case for graph-based
methods as a scalable and extensible approach to verification artefact reuse.

4 Underlying Theory Foundations
This section develops the theoretical foundations required for semantically grounded
AI assistance in specification and verification. Existing LLM-driven pipelines–such
as those surveyed in Beg et al. (2025a,b)–typically operate at the syntactic surface
of formalisms, generating constraints or predicates tied to a single verification envi-
ronment such as ACSL, Event-B, or TLA+ . In the absence of a unifying semantic
substrate, these artefacts lack principled interoperability, hindering cross-tool reason-
ing, scalable refinement, and structured reuse. Our aim is to situate LIFR workflows


                                           10
within mathematically robust semantic theories that enable language-independent
correctness reasoning and satisfaction-preserving translations.
    UTP, introduced by Hoare and He and articulated through Woodcock’s tutorial
Woodcock and Cavalcanti (2004), provides an algebraic relational calculus that unifies
diverse programming paradigms through healthiness conditions and design theories.
Its use in integrated formalisms such as Circus Woodcock and Cavalcanti (2002)
demonstrates its capacity to harmonise imperative constructs, CSP processes, and Z
schemas within a single semantic model. Complementing UTP, the Theory of Insti-
tutions Goguen and Burstall (1992) supplies an abstract account of logical systems
through signatures, sentences, models, and satisfaction, thereby enabling the compar-
ison, translation, and combination of formalisms while preserving semantic meaning.
Together, UTP and Institutions offer a rigorous, language-independent foundation for
embedding AI-generated artefacts into a sound semantic framework.

4.1 Institutions as a Basis for Interoperability
The theory of institutions, which finds its foundations in category theory, provides
a general framework for defining a logical system Goguen and Burstall (1992). Insti-
tutions are used to represent logics in terms of their vocabulary (signatures), syntax
(sentences) and semantics (models and satisfaction condition). The basic maxim of
institutions is that “Truth is invariant under change of notation” Goguen and Burstall
(1992). Institutions have been devised for a number of logics Sannella and Tarlecki
(2012) and for formal specification languages which are used for verification pur-
poses, including CASL and Event-B Mosses (2004); Farrell et al. (2017). The latter
is of particular interest since Event-B is used at an industrial-scale in the verifica-
tion of cyber-physical systems. These institutions support modular specifications as
well as interoperability between formalisms Farrell (2017). Reynolds (2023) intro-
duces a framework in Rocq that streamlines the construction of institutions and the
verification of their standard proof obligations, reducing repetitive and error-prone
manual work. The approach is demonstrated through mechanised encodings of first-
order logic, Event-B semantics, and their combination with linear temporal logic. The
thesis also develops institution-independent constructions that support generic logic
combinations and translations.

4.2 From Translation Frameworks to Unified Semantic
    Theories
Our motivation is rooted in earlier work which relates heterogeneous formalisms
through mathematically verified transformations. An example is the transformation
of state-rich process algebra Circus into the state-poor process algebra CSP. The
prototype developed in Beg (2016) demonstrated the feasibility of automatically trans-
lating LaTeX-based Circus specifications into CSPm, enabling direct analysis via the
FDR model checker. The study revealed key technical challenges—handling complex
action compositions, implementing pattern matching for behavioural normalisation,
and maintaining observable event semantics—which underscored the limitations of
imperative implementation techniques. These insights motivated the more principled


                                          11
functional formulation of translation rules later adopted. Beg (2016) also provided a
comprehensive formalisation of the Circus-to-CSP translation using Haskell, encod-
ing the refinement steps and semantic constraints as functional transformations with
explicit correctness guarantees. The resulting prototype supported the formal mod-
elling of software and hardware protocols and offered a rigorous account of how
rich state-based descriptions can be systematically mapped into process-algebraic
behaviours. Collectively, these contributions emphasised the need for mathematically
disciplined frameworks capable of expressing and verifying relationships between dis-
parate modelling languages—precisely the role addressed by the Unifying Theories of
Programming (UTP) and the Theory of Institutions.
    Model checking and theorem proving have long been central techniques for
verifying autonomous systems. Model checkers systematically explore state spaces
to identify behavioural violations, while theorem provers establish mathematical
guarantees about system correctness. Existing verification frameworks combine for-
mal behavioural models with automated reasoning to analyse timing, safety, and
interaction properties in complex autonomous systems.
    A significant line of work integrates process algebras with graphical state-machine
notations to support robotic system design and verification. These approaches are sup-
ported by tool environments capable of automatically translating high-level models
into formal representations suitable for model checking and proof-based verifica-
tion. Several frameworks also combine state-machine modelling with theorem proving
environments, enabling refinement-based reasoning and verification across different
abstraction levels. Much of this work is grounded in the Unifying Theories of Program-
ming (UTP), which provides a semantic basis for integrating heterogeneous formalisms
through relational refinement theories.
    Mechanised UTP environments now support automated reasoning for refinement
calculus, denotational semantics, and Hoare-style verification within proof assis-
tants. Related work on model-based testing and runtime verification shows that
unified semantic frameworks scale beyond theory into embedded, real-time, and
industrial systems. These developments reinforce the relevance of semantic interop-
erability and refinement-preserving translation for future LIFR workflows. In our
approach, institutional semantics extends this direction by providing a more gen-
eral mechanism for interoperability across heterogeneous verification technologies and
logical systems. Isabelle/UTP Foster et al. (2020) mechanises UTP theories within
a proof assistant, supplying automated reasoning for refinement calculus, denota-
tional models, and Hoare logic. Work on model-based testing Iyenghar et al. (2011)
demonstrates the applicability of UTP to embedded and real-time systems, while
industrial deployments—from UAS traffic management with runtime verification Ham-
mer et al. (2022) to verification of the RTEMS operating system Butterfield and Tuong
(2023)—illustrate the value of unified semantic models in large-scale settings.
    Within this landscape, LIFR workflows can be re-envisioned as operating under
semantic governance rather than merely generating syntactic artefacts. UTP and
Institution theory allow AI-generated predicates to be checked against healthiness
conditions; behavioural models to be interpreted through design theories; and spec-
ification fragments to be transported across formalisms via institution morphisms.



                                          12
Techniques for iterative prompting and context-sensitive refinement Wang et al. (2022)
complement this vision by enabling LLMs to explore and adapt within semantically
constrained spaces.
    A key advantage of embedding LIFR in these semantic theories is the ability
to articulate and mechanise interoperability across modelling languages and verifica-
tion environments. Proof-graph frameworks such as Cyclone can encode relationships
among UTP theories, Event-B machines, TLA+ behaviours, and ACSL specifications,
while satisfaction-preserving translations—e.g. between temporal logics or between
behavioural and state-based assertions—can be expressed as institution morphisms.
UTP calculi, including those mechanised in Isabelle/UTP, offer refinement, concur-
rency, and temporal reasoning operators compatible with automated proof engines.
These mechanisms open pathways for AI-assisted migrations across formalisms,
enabling structured specification reuse and multi-tool verification at scale.
    Bringing these strands together, we advocate a semantically disciplined method-
ology for AI-assisted specification and verification in which learning systems operate
within the constraints imposed by UTP and Institutional semantics. In this paradigm,
AI components act not as syntactic converters but as semantic agents that propose,
transform, and analyse artefacts in accordance with healthiness conditions, refinement
laws, and satisfaction-preserving mappings. Such an environment enables principled
cross-language verification, traceability, and scalable integration of specifications,
supporting the evolution of formal artefacts beyond the limitations of tool-specific
pipelines. This direction lays the groundwork for a new generation of trustworthy,
interoperable, and semantically grounded verification ecosystems in which AI and
formal methods co-develop in mutually reinforcing ways.

5 Discussion
The integration of large language models into formal specification and verification
pipelines exposes tightly coupled technical challenges that cannot be resolved by
incremental performance improvements alone. As identified in Beg et al. (2025b), a
primary limitation is the absence of aligned, high-fidelity datasets connecting real
industrial natural-language requirements with semantically validated specifications
and verification outcomes. Existing datasets remain synthetic, narrow, or lack veri-
fied specification-level ground truth, creating a validation gap in which LLMs may
appear effective under superficial metrics while failing to preserve behavioural seman-
tics. Future work must prioritise versioned, traceable corpora binding requirements,
code, generated specifications, solver outcomes, and human corrections into a single
source-aware structure. Without such datasets, true semantic correctness, refinement
preservation, and scalability cannot be measured.
    A second challenge is instability of specification generation under prompt varia-
tion: small phrasing differences can produce materially different ACSL or JML outputs
even for fixed requirements. This undermines reproducibility in safety-critical con-
texts. Research must shift toward formally constrained prompt templates, contract
schemas, and grammar-restricted decoding backed by tool-specific ASTs. Evaluation
across prompting strategies must correlate syntactic validity with downstream proof



                                          13
success and solver stability. Interoperability across heterogeneous verification environ-
ments remains limited. Tool-specific translators mapping LLM outputs into ACSL,
JML, or solver languages are fragile and non-scalable. A semantically typed, tool-
neutral intermediate representation is needed to express preconditions, postconditions,
invariants, and frame conditions independently of concrete syntax, while remaining
translatable across logics with differing expressivity.
    Symbolic reasoning is typically used only post hoc. Solvers detect inconsistencies
after generation but do not guide it. Closed-loop integration—feeding unsatisfiable
cores, counterexamples, and path constraints back into generation–requires machine-
interpretable representations of solver feedback and control strategies that avoid
non-terminating repair loops. Traceability across lifecycle artefacts is another bottle-
neck. Linking requirements, specifications, implementation, and verification results is
often manual or heuristic-based and does not scale to multi-version systems. Future
systems need version-aware, bidirectional trace graphs where LLMs propose candidate
links validated through proof obligations or review. Semantics-preserving traceability
requires refinement-aware propagation and delta-based specification updates, not full
regeneration.
    Handling partial, underspecified, or contradictory requirements also remains
unresolved. Industrial requirements contain implicit assumptions and conflicts, and
current LLMs either over-concretise or silently resolve contradictions. Generators
must instead model uncertainty explicitly through conditional contracts, alterna-
tive behaviours, and assumption clauses refined during verification. Trustworthiness
and certification concerns—training data provenance, memorisation, prompt injec-
tion, nondeterminism—are amplified when LLMs participate in verification pipelines.
Verifiable guarantees on bounded nondeterminism, auditable training data for safety-
relevant fine-tuning, and runtime monitoring of specification generation are essential
for regulatory acceptance in domains such as avionics or medical software.
    Scalability remains limited to small programs. Memory constraints, context-
window limits, and path-coverage explosion degrade performance for larger systems.
Hierarchical specification synthesis is required, where modules are verified indepen-
dently and composed under formally justified and minimised interface contracts. The
long-term trajectory is a shift from isolated automation to semantically grounded
co-design among LLMs, symbolic engines, and human experts. LLMs should act as
statistically guided front-ends under continuous logical supervision; symbolic tools
must constrain generation rather than merely validate it; and human experts should
curate reusable invariants, proof patterns, and failure taxonomies. The success of
LLM-assisted verification ultimately depends on disciplined integration of statistical
learning with formal semantic control, traceability, and certifiable trust models.

6 Conclusions
This paper has outlined a coherent vision for the future of formal verification centered
on three tightly integrated pillars: automated contract synthesis, semantic artifact
reuse via LLM-guided graph matching, and a unifying underlying theory of refine-
ment and compositional reasoning. Contract synthesis elevates specifications from



                                           14
static, human-authored objects to dynamic artifacts that can be inferred, repaired, and
adapted as systems evolve. At the same time, the proposed hybrid reuse framework
addresses a long-standing bottleneck in formal methods: the inability to systematically
transfer verification knowledge across projects and domains. By treating verifica-
tion artifacts as structured semantic objects rather than isolated syntactic entities,
the framework enables reuse at the level of behavioral intent rather than textual
coincidence.
    The integration of large language models with graph-based representations plays
a critical enabling role in this vision. LLMs provide expressive semantic embeddings
that bridge heterogeneous notations, languages, and abstraction levels, while graph
matching enforces global structural coherence across candidate alignments. Crucially,
this separation allows machine learning to guide discovery and search without compro-
mising the symbolic guarantees required for sound verification. Rather than replacing
formal reasoning, learning-based components function as semantic accelerators that
expose latent structure in large verification repositories. This hybridization opens the
door to verification workflows in which contracts, proofs, and counterexamples are not
merely reused opportunistically, but systematically discovered, adapted, and validated
at scale.
    Finally, the underlying theoretical framework provides the essential glue that makes
synthesis and reuse trustworthy. Refinement relations, abstraction operators, and
compositional semantics supply the formal infrastructure needed to interpret approx-
imate matches, justify reuse transformations, and ensure that transferred artifacts
preserve correctness guarantees. The resulting perspective shifts formal verification
from a static, one-off activity to a cumulative and continuously evolving discipline.
By tightly coupling synthesis, semantic reuse, and theory, we move toward verification
systems that do not merely check correctness, but actively accumulate, generalize, and
propagate formal knowledge across the software and cyber-physical system lifecycle.

Acknowledgement
This work is partly funded by the ADAPT Research Centre for AI-Driven Digital
Content Technology, which is funded by Research Ireland through the Research Ireland
Centres Programme and is co funded under the European Regional Development Fund
(ERDF) through Grant 13/RC/2106 P2.
   This publication has also emanated from research conducted with the financial
support of Science Foundation Ireland/Research Ireland under Grant number 21/FFP-
P/10118.

Use of AI-Assisted Tools
We acknowledge the use of free version of GPT-5 for refining the textual presentation
of this vision paper. The model was applied solely to improve clarity and coherence.
The text has been thoroughly reviewed and discussed by all authors to ensure accuracy
and integrity.




                                          15
References
Beg A (2016) Translating from ”state-rich” to ”state poor” process algebras. PhD
  thesis, Trinity College Dublin, Ireland, URL https://hdl.handle.net/2262/82894

Beg A, O’Donoghue D, Monahan R (2025a) Leveraging LLMs for formal software
  requirements: Challenges and prospects. In: Proc. 7th Int. Workshop OVERLAY @
  ECAI 2025, Bologna, Italy, URL https://ceur-ws.org/Vol-4142/paper11.pdf

Beg A, O’Donoghue D, Monahan R (2025b) Traceable and verifiable software require-
  ments: A synthesis of AI-enabled formal methods. J Softw Test Verif Reliab URL
  https://doi.org/10.5281/zenodo.17772835, under review; Version v1 available on
  Zenodo

Beg A, O’Donoghue D, Monahan R (2026a) Evaluating LLM-generated ACSL annota-
  tions for formal verification. In: Proc. Formal Tech. Judicious Program. Workshop at
  ECOOP 2026, Brussels, Belgium, URL https://arxiv.org/abs/2602.13851, accepted;
  to appear, June 30, 2026

Beg A, O’Donoghue D, Monahan R (2026b) Graph construction and matching for
  imperative programs using neural and structural methods. URL https://arxiv.org/
  abs/2604.26578

Butterfield A, Tuong F (2023) Applying formal verification to an open-source real-
  time operating system. In: Bowen JP, Li Q, Xu Q (eds) Theories of Programming
  and Formal Methods, Lecture Notes in Computer Science, vol 14080. Springer, pp
  348–366, https://doi.org/10.1007/978-3-031-40436-8 13

Farrell M (2017) Event-B in the institutional framework: defining a semantics, mod-
  ularisation constructs and interoperability for a specification language. PhD thesis,
  Maynooth University

Farrell M, Monahan R, Power JF (2017) An Institution for Event-B. In: Rec. Trends
  Alg. Dev. Tech., Springer, pp 104–119, https://doi.org/10.1007/978-3-319-72044-9
  8

Foster S, Baxter J, Cavalcanti A, et al (2020) Unifying semantic foundations for
  automated verification tools in Isabelle/UTP. Science of Computer Programming
  197:102510. https://doi.org/https://doi.org/10.1016/j.scico.2020.102510

Goguen JA, Burstall RM (1992) Institutions: abstract model theory for specification
 and programming. J ACM 39(1):95–146

Hammer A, Cauwels M, Hertz B, et al (2022) Integrating runtime verification into an
 automated UAS traffic management system. Innov Syst Softw Eng 18(4):567–580.
 https://doi.org/10.1007/S11334-021-00407-5




                                          16
Iyenghar P, Pulvermueller E, Westerkamp C (2011) Towards model-based test automa-
  tion for embedded systems using UML and UTP. In: ETFA2011, pp 1–9, https:
  //doi.org/10.1109/ETFA.2011.6058982

Lippolis AS, Klironomos A, Milon-Flores DF, et al (2023) Enhancing entity alignment
  between wikidata and artgraph using LLMs. In: Proc. Int. Workshop SWODCH
  at ISWC 2023, CEUR Workshop Proc., vol 3540. CEUR-WS.org, URL https://
  ceur-ws.org/Vol-3540/paper7.pdf

Mosses PD (2004) CASL reference manual: the complete documentation of the
 common algebraic specification language. Springer

Pitu M, Grijincu D, Li P, et al (2013) Arı́s: Analogical reasoning for reuse of implemen-
  tation & specification. In: Proceedings Artificial Intelligence for Formal Methods
  (AI4FM). Department of Computer Science, Heriot-Watt University

Reynolds C (2023) Machine-Assisted Proofs for Institutions. PhD thesis, National
  University of Ireland Maynooth

Sannella D, Tarlecki A (2012) Foundations of algebraic specification and formal
  software development. Springer

Strecker M (2007) Modeling and verifying graph transformations in proof assistants.
  In: Proc. TERMGRAPH@ETAPS 2007, Electron. Notes Theor. Comput. Sci., vol
  203. Elsevier, pp 135–148, URL https://doi.org/10.1016/j.entcs.2008.03.039

Topsakal O, Akinci TC (2023) Creating Large Language Model applications utilizing
  LangChain: A primer on developing LLM apps fast. In: International conference on
  applied engineering and natural sciences, pp 1050–1056

Vasic I, Fill HG, Quattrini R, et al (2025) Knowledge Graphs vs. Large Language
  Models: Competitors or Partners in Supporting Virtual Museums. ACM Journal on
  Computing and Cultural Heritage

Wang B, Deng X, Sun H (2022) Iteratively Prompt Pre-trained Language Mod-
 els for Chain of Thought. In: Proc. EMNLP 2022. Association for Computational
 Linguistics, Abu Dhabi, UAE, pp 2714–2730, https://doi.org/10.18653/v1/2022.
 emnlp-main.174

Woodcock J, Cavalcanti A (2002) The Semantics of Circus. In: Bert D, Bowen JP,
 Henson MC, et al (eds) ZB 2002: Formal Specification and Development in Z and
 B. Springer Berlin Heidelberg, Berlin, Heidelberg, pp 184–203, https://doi.org/10.
 1007/3-540-45648-1 10

Woodcock J, Cavalcanti A (2004) A Tutorial Introduction to Designs in Unifying The-
 ories of Programming. In: Boiten EA, Derrick J, Smith G (eds) Integrated Formal
 Methods. Springer Berlin Heidelberg, Berlin, Heidelberg, pp 40–66


                                           17
