                                                S TRUCTURED D ECOMPOSITION FOR LLM R EASONING :
                                                  C ROSS -D OMAIN VALIDATION AND S EMANTIC W EB
                                                                   I NTEGRATION


                                                               Albert Sadowski                                       Jarosław A. Chudziak
                                                        Warsaw University of Technology                         Warsaw University of Technology
                                                               Warsaw, Poland                                           Warsaw, Poland
arXiv:2601.01609v1 [cs.AI] 4 Jan 2026




                                                      albert.sadowski.stud@pw.edu.pl                            jaroslaw.chudziak@pw.edu.pl


                                                                                             January 6, 2026

                                                                                              A BSTRACT

                                                 Rule-based reasoning over natural language input arises in domains where decisions must be au-
                                                 ditable and justifiable: clinical protocols specify eligibility criteria in prose, evidence rules define
                                                 admissibility through textual conditions, and scientific standards dictate methodological requirements.
                                                 Applying rules to such inputs demands both interpretive flexibility and formal guarantees. Large
                                                 language models (LLMs) provide flexibility but cannot ensure consistent rule application; symbolic
                                                 systems provide guarantees but require structured input. This paper presents an integration pattern
                                                 that combines these strengths: LLMs serve as ontology population engines, translating unstructured
                                                 text into ABox assertions according to expert-authored TBox specifications, while SWRL-based
                                                 reasoners apply rules with deterministic guarantees. The framework decomposes reasoning into
                                                 entity identification, assertion extraction, and symbolic verification, with task definitions grounded
                                                 in OWL 2 ontologies. Experiments across three domains (legal hearsay determination, scientific
                                                 method-task application, clinical trial eligibility) and eleven language models validate the approach.
                                                 Structured decomposition achieves statistically significant improvements over few-shot prompting in
                                                 aggregate, with gains observed across all three domains. An ablation study confirms that symbolic
                                                 verification provides substantial benefit beyond structured prompting alone. The populated ABox
                                                 integrates with standard semantic web tooling for inspection and querying, positioning the framework
                                                 for richer inference patterns that simpler formalisms cannot express.

                                        Keywords Large Language Models · Explainable AI · Neural-Symbolic Integration · Semantic Web


                                        1   Introduction

                                        Artificial intelligence systems are increasingly deployed to support decision-making in domains governed by explicit
                                        rules: clinical protocols specify patient eligibility criteria, evidence law defines admissibility conditions, and scientific
                                        standards dictate methodological requirements [28]. These rule frameworks exist precisely because decisions in such
                                        domains must be auditable and justifiable [12]. The growing volume of unstructured text, medical records, legal filings,
                                        research literature, creates demand for systems that can apply domain rules to natural language inputs at scale.
                                        This demand exposes a fundamental tension between two computational paradigms [51, 29]. Large language models
                                        offer unprecedented interpretive flexibility: they can identify entities, extract relationships, and resolve ambiguities
                                        inherent in natural language [50]. However, they cannot provide formal guarantees, their reasoning is opaque, their rule
                                        application inconsistent across phrasings [35, 18], and their outputs unverifiable against logical specifications [8]. The
                                        persistence of hallucination, even in state-of-the-art models, compounds these concerns [33]. Symbolic systems offer
                                        the inverse profile: formal guarantees through explicit inference rules, but an inability to interpret unstructured text
                                        directly [9, 5].
                                                                                        A PREPRINT - JANUARY 6, 2026


The capabilities of modern LLMs have renewed interest in how symbolic reasoning systems can be leveraged [47, 26].
Rather than viewing neural and symbolic approaches as competing paradigms, recent work explores architectures
that exploit their complementary strengths [37, 43]. The critical insight is that LLMs excel at the interpretive work
symbolic systems cannot perform, while symbolic systems provide the verification guarantees LLMs cannot offer. This
complementarity suggests an integration strategy: use LLMs to translate unstructured text into formal representations,
then delegate reasoning to symbolic systems.
We argue that OWL 2 ontologies [38] with SWRL rules [46] provide the right abstraction for this integration. The
architecture separates concerns cleanly: expert-authored TBox specifications encode domain rules and classification
criteria; LLMs populate the ABox by extracting entities and assertions from text; SWRL-based reasoners apply rules
with deterministic guarantees. This division positions LLMs as ontology population engines, components that translate
unstructured input into formal assertions according to predefined specifications. The populated ABox integrates with
standard semantic web tooling for inspection, querying, and further inference, addressing the interoperability limitations
of ad-hoc formalisms used in prior neural-symbolic approaches.
Our prior work [41] introduced structured decomposition for rule-based reasoning, separating the process into entity
identification, assertion extraction, and symbolic verification. That work demonstrated improvements on legal hearsay
determination but was limited to a single task and relied on ad-hoc representations with SMT-based verification. This
paper extends the framework in two directions. First, we ground task definitions in OWL 2 ontologies with SWRL
rules, replacing ad-hoc representations with semantic web standards. This reformulation enables integration with
established tooling and positions the framework for richer inference patterns: class hierarchies, multi-label classification,
and composable imports from domain vocabularies. Second, we validate the approach across three domains, legal
reasoning, scientific literature analysis, and medical inference, evaluating eleven language models to assess cross-domain
generalisability.
The paper makes two primary contributions. We present a neural-symbolic integration pattern grounded in semantic
web standards, demonstrating that LLMs can serve as ontology population engines for rule-based reasoning tasks.
The architecture produces inspectable reasoning traces where every extraction decision persists as an ABox assertion,
enabling systematic review of how text was interpreted. We then validate this pattern across three domains: legal
reasoning (hearsay determination), scientific literature analysis (method-task application), and medical inference
(clinical trial eligibility). Experiments across eleven language models confirm that structured decomposition generalises
beyond legal reasoning, with improvements across all three domains and aggregate gains reaching statistical significance.
The remainder of this paper is organised as follows. Section 2 reviews related work on LLM reasoning, prompting
strategies, and neural-symbolic integration, then introduces the semantic web technologies grounding our reformulation.
Section 3 presents the structured decomposition framework. Section 4 describes task formalisation and selection criteria.
Section 5 details experimental design, and Section 6 presents results. Section 7 discusses findings and limitations, and
Section 8 concludes.


2     Background and Related Work

The promise of combining neural flexibility with symbolic guarantees has motivated decades of research, but practical
integration remains elusive. Large language models have shifted this landscape: their interpretive capabilities enable
new forms of neural-symbolic architecture, while their well-documented reasoning limitations make external verification
mechanisms newly attractive. Realising this potential requires understanding both what LLMs can and cannot do
reliably, and which symbolic formalisms offer the right abstraction for integration.


2.1   LLM Reasoning Capabilities and Limitations

Large language models have demonstrated capabilities in complex reasoning tasks [50], showing potential for applica-
tions requiring sophisticated text analysis and inference. However, despite these capabilities, LLMs face limitations
when applications require consistent rule application [35, 18], transparent reasoning processes, and verifiable out-
comes [8].
The fundamental challenge lies in the tension between neural and symbolic approaches to reasoning [51, 29]. Neural
methods offer flexibility and generalisation across diverse inputs but often struggle with consistency and verifiability. In
contrast, symbolic systems provide formal guarantees but traditionally require structured inputs and lack adaptability to
natural language [9]. This dichotomy becomes particularly apparent in rule application scenarios where both precise
logical inference and natural language understanding are essential [5].


                                                             2
                                                                                     A PREPRINT - JANUARY 6, 2026


Three specific challenges emerge in deploying LLMs for rule-based reasoning tasks [25, 7]. First, while LLMs can
recognise patterns in training data, they lack consistent mechanisms to apply rules with logical rigour across novel
situations [35]. Second, exception handling, determining when general rules do not apply due to special conditions,
presents difficulties [14] as it requires both rule comprehension and contextual awareness. Third, the auto-regressive
generation paradigm favours local coherence over global planning [7], which can lead to reasoning errors that compound
across multiple inference steps.
These limitations are particularly problematic in domains requiring formal guarantees, such as regulatory compliance,
clinical trial eligibility determination, and scientific information extraction, where decisions must be auditable and
justifiable [12]. The persistence of hallucination, generating plausible but incorrect outputs, remains a concern even in
state-of-the-art models [33], motivating approaches that provide external verification mechanisms.

2.2   Prompting Strategies for Reasoning

To improve LLM reasoning capabilities, researchers have developed various prompting techniques. Chain-of-Thought
(CoT) prompting [50] elicits intermediate reasoning steps, improving performance on tasks requiring multi-step
inference, with benefits particularly pronounced in larger models.
Beyond CoT, other specialised techniques have emerged. Program-Aided Language Models (PAL) [16] leverage LLMs
to generate executable code that solves reasoning problems, combining the flexibility of natural language with the
precision of programming languages. ReAct [52] interleaves reasoning and acting, allowing models to interact with
external environments while building coherent reasoning traces. Decomposed Prompting [13] separates complex tasks
into modular sub-problems, each handled by specialised prompts.
In domain-specific applications, Servantez et al. [43] introduced the Chain of Logic prompting method, which separates
rule-based reasoning into independent logical steps and recomposes them to form coherent conclusions. Similarly,
the InsurLE framework by Cummins et al. [11] uses controlled natural language to codify insurance contracts while
preserving syntactic nuances and exposing the underlying formal logic.
A distinction exists between prompting strategies that structure output format versus those that change the reasoning
architecture. Techniques like CoT primarily affect how models articulate their reasoning, while approaches that integrate
external verification components—such as SMT solvers or logic programming systems—introduce architectural changes
that provide formal guarantees absent from prompting alone. Our structured decomposition approach falls into the
latter category.

2.3   Neural-Symbolic Integration Approaches

Neural-symbolic approaches combine the learning capabilities of neural networks with the reasoning power of sym-
bolic systems. This integration is promising for rule-governed domains as it can combine LLMs’ natural language
understanding with the formal reasoning capabilities of logic-based systems.
Tan et al. [47] enhanced LLM reasoning through a self-driven Prolog-based CoT mechanism that iteratively refines
logical inferences. Wei et al. [51] proposed a hybrid neural-symbolic framework that synergises neural representations
with explicit logical rules for legal reasoning in automated systems. Similar integration approaches have been explored
in multi-agent contexts, where Answer Set Programming combined with graph knowledge bases enables enhanced
collaborative reasoning capabilities [26]. Subsequent work by the same authors demonstrates that augmenting such
systems with Theory of Mind mechanisms and structured critique yields synergistic improvements in reasoning
quality [27].
The work by Lalwani et al. [29] on NL2FOL demonstrates a structured, step-by-step pipeline to translate natural
language inputs into first-order logic representations using LLMs at each step (Figure 1). Their approach addresses key
challenges in this translation process, including integrating implicit background knowledge. By leveraging structured
representations, they use Satisfiability Modulo Theory (SMT) solvers to reason about the logical validity of natural
language statements.
Alonso and Chatzianastasiou [37] demonstrated that embedding logical rules into neural frameworks can enhance the
interpretability and robustness of text analysis. Calanzone et al. [9] developed an integration approach that enforces
logical consistency by incorporating external constraint sets into LLM outputs.
Table 1 provides a comparative overview of representative approaches. The existing landscape reveals a gap between
systems using custom symbolic formalisms and those leveraging established semantic web standards. Most approaches
employ ad-hoc representations or domain-specific logic programming systems, limiting interoperability and reuse. Our
prior work [41] used JSON schemas with SMT verification, which achieved strong results but lacked standardised


                                                           3
                                                                                       A PREPRINT - JANUARY 6, 2026




Figure 1: The NL2FOL pipeline for translating natural language to first-order logic (reproduced from Lalwani et al. [29]).
Module A decomposes input text through successive extraction stages, claim parsing, entity identification, relation
classification, and property extraction, before formulating FOL expressions augmented with background knowledge.
Module B compiles the logical formula to SMT format, and Module C interprets solver outputs as natural language
counterexamples. This stepwise architecture exemplifies the neural-symbolic integration pattern our framework adopts,
though we replace ad-hoc FOL translation with OWL ontology population and SMT verification with SWRL-based
reasoning.

Table 1: Comparison of neural-symbolic methods along domain, decomposition, and symbolic reasoning dimensions.

Method                                      Domain          Decomposition Strategy           Symbolic Formalism
Thought-Like-Pro [47]                       General         Explicit multi-step (CoT-        Prolog-based inference
                                                            like)
Wei et al. (2025) [51]                      Legal (civil)   Structured pipeline              FOL with custom legal rules
NL2FOL [29]                                 General         Stepwise formalisation           FOL + SMT solver
Alonso & Chatzianastasiou (2024) [37]       Legal (con-     Logic-LLM integration            Logic rule templates
                                            tracts)
Calanzone et al. (2024) [9]                 General         End-to-end constraint loss       Logical consistency con-
                                                                                             straints
Our prior work [41]                         Legal           Three-step decomposition         SMT solver (ad-hoc schema)
                                            (hearsay)
This work                                   Cross-          Three-step decomposition         OWL 2 + SWRL
                                            domain



semantics and tooling support. This observation motivates grounding structured decomposition in OWL and SWRL,
enabling integration with the broader semantic web ecosystem.


2.4   Semantic Web Technologies for Knowledge Representation

The semantic web provides a mature technology stack for formal knowledge representation and reasoning. While
originally designed for web-scale interoperability, these standards have increasingly found application in neuro-symbolic
architectures as the symbolic substrate for verification and logic injection [21]. We introduce the core technologies
relevant to our framework reformulation.
OWL 2 [38] is a W3C standard for defining ontologies, formal specifications of shared conceptualisations within a
domain. OWL ontologies consist of two components: the TBox (terminological box) defines classes, properties, and
their relationships; the ABox (assertional box) contains individuals and their property assertions. This separation, rooted
in Description Logic theory [2], maps naturally to our framework’s distinction between task definitions (TBox) and
extracted entities/predicates (ABox).


                                                            4
                                                                                         A PREPRINT - JANUARY 6, 2026


OWL provides constructs for defining class hierarchies, property domains and ranges, and logical constraints. For
example, defining Hearsay as a subclass of Statement captures the taxonomic relationship that hearsay evidence is a
specialised form of statement. Property restrictions can express necessary conditions for class membership, though
complex rule-based inference requires additional machinery.
SWRL [46] extends OWL with Horn-like rules, enabling inference patterns beyond OWL’s native expressivity. A
SWRL rule takes the form: antecedent → consequent, where both antecedent and consequent are conjunctions of atoms.
Atoms can be OWL class assertions, property assertions, or built-in predicates for comparisons and computations.
For structured decomposition, SWRL rules encode the task predicate, the logical formula determining when a classifica-
tion holds. For instance, the hearsay determination rule can be expressed as:

                                       Statement(?s) ∧ OutOfCourtStatement(?s)
                                         ∧ hasAssertion(?s, ?a)
                                         ∧ introducedForLegalIssue(?s, ?l)                                                (1)
                                         ∧ provesTruthOfAssertion(?s, ?l)
                                         → Hearsay(?s)

This rule states that if an individual ?s satisfies all antecedent conditions, it is inferred to belong to the Hearsay class.
OWL reasoning operates under the open-world assumption (OWA): the absence of a statement does not imply its
negation. This contrasts with databases and many logic programming systems that use the closed-world assumption
(CWA). Under OWA, if a property is not asserted for an individual, the reasoner cannot conclude that the property does
not hold; it may simply be unknown [20].
For the binary classification tasks in this paper, the practical impact is limited: SWRL rules with conjunctive antecedents
require all conditions to be satisfied for the rule to fire. Whether a missing assertion is treated as “unknown” (OWA) or
“false” (CWA), the rule does not fire in either case, yielding the same classification outcome. More complex inference
patterns, such as rules that reason over the absence of properties, would require explicit handling of the OWA.
Several OWL reasoners are available, including Pellet [44], HermiT [17], and FaCT++ [48]. These reasoners support
consistency checking, classification, and SWRL rule execution. We use the Pellet reasoner, which integrates with the
owlready2 library used in our implementation.

2.5     LLMs for Ontology Engineering and Population

Recent work has explored using LLMs for ontology-related tasks, reflecting a broader shift in the semantic web commu-
nity toward leveraging large language models for tasks traditionally requiring significant manual engineering [39].

2.5.1    Ontology Learning and Alignment
LLMs have been applied to ontology learning, the automatic or semi-automatic construction of ontologies from text.
The LLMs4OL paradigm [3] demonstrated that LLMs can extract taxonomic relations, identify relevant concepts, and
propose property definitions from unstructured corpora with competitive performance. Recent benchmark studies
confirm that while models excel at surface-level extraction, correctly identifying complex axioms remains challenging
without structured guidance [4]. Consequently, resulting ontologies often require expert refinement to ensure logical
consistency and domain accuracy.
Ontology alignment, mapping concepts between different ontologies, has similarly benefited from LLM capabilities.
Models can identify semantic correspondences based on contextual understanding rather than purely lexical match-
ing [22]. These capabilities position LLMs as useful tools in the ontology engineering process, though recent position
papers argue they should not replace formal verification in high-stakes contexts [19].

2.5.2    Knowledge Graph Population
Knowledge graph population involves extracting entities and relations from text to populate a knowledge base, a task
closely aligned with our framework’s entity identification and assertion extraction steps. Studies have shown LLMs can
achieve competitive performance on relation extraction benchmarks [49].
Despite progress in these individual areas, systematic frameworks that integrate LLMs as ontology population compo-
nents with formal OWL/SWRL verification remain underexplored. Most existing work either uses LLMs for ontology
construction (producing TBox definitions) or for standalone information extraction (without formal verification).


                                                              5
                                                                                       A PREPRINT - JANUARY 6, 2026




Figure 2: Structured Decomposition Framework with OWL/SWRL integration. Yellow box represents domain expert
input (task ontology defining classes, properties, and SWRL rules); blue boxes show automated processing by LLMs
(entity identification, assertion extraction) and reasoner (rule application); arrows indicate data flow. Beyond the
classification outcome, the framework yields a populated ABox that externalises every extraction decision, providing an
inspectable record of how the input text was interpreted.


Approaches like NL2FOL (Figure 1) employ ad-hoc FOL representations and custom SMT compilation, limiting
interoperability with established semantic web infrastructure.


3     Structured Decomposition Framework

The integration pattern rests on a clean separation of concerns: LLMs handle interpretation, symbolic reasoners handle
inference, and ontologies provide the interface between them. Our prior work [41] demonstrated this separation using
ad-hoc JSON schemas with SMT verification. Here we reformulate the framework around OWL 2 ontologies and SWRL
rules, replacing custom representations with semantic web standards. This grounds the architecture in established
tooling while preserving its reasoning guarantees.

3.1   Design Principles and Architecture Overview

Decomposition-based approaches have long been recognised in cognitive science and AI as effective strategies for
complex problem solving [36, 40]. Our framework applies these principles to address a fundamental challenge:
while LLMs demonstrate impressive capabilities with natural language inputs, they struggle with consistent rule
application [18, 35].
The framework rests on three design principles. First, separation of concerns divides the reasoning pipeline between
neural and symbolic components. LLMs handle language interpretation, recognising entities and evaluating assertions
from unstructured text, while ontological reasoners handle logical inference with formal guarantees. Each component
does what it does best. Second, externalised task definitions allow domain experts to specify terms, predicates, and
classification rules without modifying the framework architecture. Experts can refine definitions as interpretations
evolve, accommodating the “open texture” inherent in many domain concepts [5]. Third, inspectable intermediate state
arises naturally from the step-wise decomposition. Each extraction step populates the ABox with explicit assertions,
identified entities, extracted assertions, inferred classifications, that persist as a reviewable record. Unlike end-to-end
approaches where reasoning is opaque, here every interpretive decision is externalised and available for scrutiny.
Figure 2 illustrates the architecture. The pipeline comprises three steps: entity identification extracts individuals from
text according to class definitions; assertion extraction determines which properties hold for those individuals; rule
application uses an OWL reasoner to infer classifications based on SWRL rules encoding the task predicate. The task
definition, formalised as an OWL ontology, provides the structural scaffold for all three steps. This decomposition
mirrors the modular design of prior neural-symbolic pipelines (cf. Figure 1), but grounds extraction in ontology-defined
specifications and replaces SMT verification with SWRL-based reasoning.
This architecture positions LLMs as ontology population engines, components that translate unstructured text into
ABox assertions according to TBox definitions provided by the task ontology. The reasoner handles inference over the


                                                            6
                                                                                      A PREPRINT - JANUARY 6, 2026


populated ontology, applying SWRL rules to determine final classifications. This division exploits the complementary
strengths of each component while localizing the sources of potential error.

3.2   Entity Identification Step

The entity identification step extracts individuals from unstructured text corresponding to classes defined in the task
ontology. Given input text and entity specifications from the ontology, the LLM identifies text spans matching each
entity type, assigns extracted entities to appropriate classes, and provides explanations justifying each extraction.
The prompt structure supplies the LLM with entity specifications expressed in natural language. Each entity type
is defined with properties specifying the entity type name, a natural language description guiding extraction, and a
mapping to the corresponding OWL class. For example, an entity specification might specify: “A communicative act
(verbal, written, or non-verbal conduct) intended to assert a fact. Detectable by explicit claims (e.g., ‘Alex said...’),
written documents, or purposeful actions (e.g., nodding).” These descriptions provide the LLM with both conceptual
definitions and practical detection heuristics.
Entity identification maps directly to ABox population: each extracted entity becomes an individual in the ontology,
with class membership assertions reflecting the LLM’s determinations. The step produces structured output specifying,
for each defined entity type, the extracted text span (if any), the assigned individual identifier, and a natural language
explanation grounding the extraction in the input text.
Several challenges arise in this step. Entity boundary detection requires determining where relevant text spans begin and
end, particularly for complex or embedded references. Implicit entities, those inferable from context but not explicitly
stated, demand interpretive judgment from the LLM. The explanation requirement serves both transparency and quality
assurance: explanations that fail to coherently justify extractions signal potential errors for human review.

3.3   Assertion Extraction Step

The assertion extraction step determines which properties and relationships hold between identified entities. Given the
entities from the previous step and assertion specifications from the task ontology, the LLM evaluates each specification,
produces binary determinations (true/false), and provides justifications grounding each decision in textual evidence.
Assertion specifications define the assertion name, the entity types it relates, a natural language description, and a
mapping to either an OWL class (for unary assertions representing class membership) or an OWL object property
(for binary assertions representing relationships). The description provides guidance for evaluation; for instance, an
assertion specification determining whether a statement occurred out of court might specify: “True if the statement was
made outside the current trial/hearing. Detect via contextual cues (e.g., “told his brother” vs. “testified in court”).”
A design pattern we investigate is the use of complementary predicates, paired assertions representing opposing
determinations. This pattern addresses a practical challenge arising from OWL’s open-world assumption (OWA): absent
an assertion, the reasoner cannot conclude that a property does not hold, it may simply be unknown. Complementary
predicates force the LLM to make explicit determinations on both positive and negative conditions, converting implicit
assumptions into explicit assertions.
In our prior work [41], complementary predicates yielded substantial precision improvements on hearsay determination
by mitigating confirmation bias. This approach reduced false positives by forcing the explicit consideration of both
confirming and disconfirming factors. As it remains unclear whether this benefit extends to other domains or persists
with more capable model architectures, we treat complementary predicates as an experimental variable rather than a
default component, evaluating the framework both with and without them across all three tasks.
Assertion extraction produces structured output specifying, for each assertion specification, the entities involved, the
boolean determination, and a natural language justification citing specific textual evidence. These outputs map to class
membership or property assertions in the ontology’s ABox.

3.4   OWL Ontology Formulation

Task definitions are formalised as OWL 2 ontologies, replacing the ad-hoc JSON schemas used in our prior work.
Task specifications become editable in tools such as Protégé, and populated ABoxes conform to standards enabling
integration with domain ontologies and SPARQL-based querying.
Each task ontology comprises a TBox defining the conceptual structure and an ABox populated during inference. The
TBox includes class hierarchies defining entity types relevant to the task, with the target classification modeled as a


                                                            7
                                                                                       A PREPRINT - JANUARY 6, 2026


class (typically a subclass of a more general entity class). Object properties capture relationships between entities, with
domain and range restrictions constraining valid assertions.
Classification logic is encoded as SWRL rules. Each rule specifies when an individual belongs to the target class: the
antecedent is a conjunction of class membership tests and property assertions; the consequent asserts membership in the
target class. For example, the hearsay rule encodes the Federal Rules of Evidence definition, when all conditions are
satisfied, the individual is classified as hearsay.
Task-level metadata for LLM prompting (entity descriptions, assertion specifications, and domain context) are encoded
as annotations within the ontology, separating prompt generation concerns from OWL reasoning semantics. This
separation allows the same ontology to drive both symbolic verification and neural interpretation. Domain experts
can edit task definitions using standard ontology tooling, validate logical consistency, and refine natural language
descriptions iteratively without modifying the framework implementation. The complete ontologies for all three
evaluation tasks are provided in the supplementary materials.1

3.5       Reasoning and ABox Inspection

The rule application step invokes an OWL reasoner to evaluate SWRL rules over the populated ontology. We use
Pellet [44] for its SWRL support and integration with standard ontology APIs, though other reasoners supporting SWRL
could substitute.
Given the ABox assertions from entity identification and assertion extraction, the reasoner performs consistency
checking, classification, and SWRL rule execution. The classification outcome, whether the target individual belongs to
the target class, constitutes the framework’s prediction.
The populated ABox serves as an inspectable artifact grounding each classification decision. Every entity extracted and
every assertion evaluated persists as an explicit record. SPARQL queries can retrieve these assertions systematically;
for instance, after processing the hearsay evaluation dataset:

PREFIX : <http://example.org/hearsay#>
SELECT ?case ?statement ?assertion
WHERE {
  ?statement :belongsToCase ?case ;
             a :OutOfCourtStatement ;
             :hasAssertion ?assertion .
}

This query retrieves out-of-court statements along with their asserted content, returning instances such as “told his
brother that...,” “wrote in the letter...,” enabling systematic review of how the input text was interpreted. The natural
language justifications generated during extraction provide human-readable rationales alongside these formal records.
For regulated domains requiring audit trails, the framework produces a complete record of interpretive decisions rather
than a black-box prediction.
Because the symbolic reasoner always produces the same output for a given set of assertions, any variability in the
framework’s behaviour stems solely from the LLM-based extraction steps. This separation makes the source of
uncertainty easy to locate: reviewers can examine the extracted entities and assertions, along with their natural language
justifications, to identify where interpretive judgments were made.

4         Task Formalisation
Structured decomposition targets a specific class of problems: those where authoritative rules fully determine classifica-
tion and where the relevant predicates can be extracted from text. We formalise three such tasks spanning legal, scientific,
and medical domains. Each satisfies both criteria, enabling evaluation of whether framework benefits generalise beyond
any single domain. The complete ontologies are available in the supplementary materials.1

4.1       Task Selection and Characterization

Not all classification problems are amenable to structured decomposition. The approach requires specific properties that
distinguish rule-governed reasoning from statistical pattern matching. Our analysis identifies two necessary conditions.
      1
          https://github.com/albsadowski/structured-decomposition-swj


                                                             8
                                                                                                                                    A PREPRINT - JANUARY 6, 2026


First, the task must have a rule-expressible decision boundary: the classification must be fully determined by a logical
formula over extractable predicates. Rules must not only exist but be sufficient to determine the outcome. Second, the
domain must permit formalisable predicate structure, allowing decomposition into discrete predicates whose logical
composition captures necessary and sufficient conditions for classification. These conditions are conjunctive: violating
either renders structured decomposition inappropriate.
Table 2 summarizes task suitability across four candidate domains. The three tasks satisfying both criteria form our
evaluation set: hearsay determination from legal reasoning, method application identification from scientific text, and
clinical trial eligibility inference from the medical domain. Each involves authoritative rule sources (Federal Rules of
Evidence, relation annotation guidelines, clinical trial protocols) that provide deterministic classification criteria.

Table 2: Task suitability for structured decomposition. Tasks require both a rule-expressible decision boundary and
formalisable predicates.




                                                                                                Clinical Trial Eligibility
                                                                           Method Application
                                                                 Hearsay




                                                                                                                             URTI
                                     Rule-expressible boundary   ✓         ✓                    ✓                            ×
                                     Formalisable predicates     ✓         ✓                    ✓                            ✓


To validate these criteria empirically, we evaluated structured decomposition on Upper Respiratory Tract Infection
(URTI) classification derived from DDXPlus [15], a medical diagnosis task with formalisable predicates (symptoms,
patient history) but no rule-expressible boundary. The results confirmed our characterization: structured decomposition
achieved 0.145 F1 compared to 0.979 for few-shot prompting. The framework correctly extracted predicates according
to diagnostic criteria, but those criteria do not constitute a sufficient decision boundary. When symptom profiles are
consistent with multiple diagnoses, the true boundary is statistical, depending on distributional patterns that few-shot
learning captures but logical rules cannot express. This negative result validates the suitability criteria: structured
decomposition is a targeted approach for rule-governed domains, not a general-purpose improvement.

4.2   Hearsay Determination

The hearsay determination task, evaluated in our prior work [41], requires classifying whether a piece of evidence
constitutes inadmissible hearsay under Rule 801 of the Federal Rules of Evidence. The rule defines hearsay as an
out-of-court statement offered to prove the truth of the matter asserted. We retain the original logical formalisation:


                                    IsHearsay(s, l) ⇔ IsStatement(s)
                                                        ∧ IsOutOfCourt(s)
                                                        ∧ ∃a. HasAssertion(s, a)                                                                              (2)
                                                          ∧ IntroducedFor(s, l)
                                                                             
                                                          ∧ ProvesTruth(s, l)

where s denotes a communicative act (verbal, written, or non-verbal conduct), l the disputed legal issue, and a the
factual claim conveyed by the statement.
The ontology defines three OWL classes: Statement, OutOfCourtStatement, and Hearsay, with the latter two modeled as
subclasses of Statement. Object properties hasAssertion, introducedForLegalIssue, and provesTruthOfAssertion capture
the relational predicates. The SWRL rule implements Formula 2: if an individual satisfies all antecedent conditions, it
is inferred to belong to Hearsay.
The task uses the LegalBench hearsay dataset [30]. Consider two contrasting examples. “To prove that Tom was in town,
a witness testifies that her friend Susan told her Tom was in town” is hearsay: an out-of-court statement is introduced
to prove its truth. Conversely, “To prove that Arthur knew English, the fact that Arthur told Bill (in English) that he


                                                           9
                                                                                      A PREPRINT - JANUARY 6, 2026


thought Mary robbed the bank” is not hearsay: the statement is introduced to prove Arthur’s English proficiency, not
Mary’s guilt.

4.3   Method Application

The method application task evaluates whether a scientific text describes a computational method being applied to
a specific task. We derive this benchmark from the SciERC dataset [32], which annotates scientific abstracts with
entity and relation labels. We filter to instances involving the Used-For relation and formulate the problem as binary
classification: given a text with a marked method entity and a marked task entity, determine whether the method is
functionally applied to the task.
The challenge lies in distinguishing genuine application from superficial co-occurrence. Scientific abstracts frequently
mention methods and tasks in conjunction (“X and Y”), comparison (“X outperforms Y”), or taxonomic contexts (“X is
a type of Y”) without implying functional application. The logical formalisation captures this distinction:

                                     Applicable(m) ⇔ IsMethod(m) ∧ IsTask(t)
                                                     ∧ FunctionalConn(m, t)                                            (3)
                                                     ∧ NotExclRelation(m, t)

where m denotes the candidate method and t the candidate task. The FunctionalConn predicate is satisfied by usage
verbs (“applied to”, “enables”), purposive markers (“for the task of”), or implicit purposive constructions linking method
to goal. The NotExcludedRelation predicate filters out conjunction, comparison, part-of, hyponym, and feature-of
relationships.
The ontology defines Method and ScientificTask as disjoint classes, with MethodApplication modeled as a subclass
of Method. Object properties functionallyConnectsTo and hasValidRelationTypeWith encode the two conjuncts. The
SWRL rule infers membership in MethodApplication when both properties are satisfied.
Input instances mark entities using bracket notation inherited from dataset preprocessing: methods in double brackets
([[ ]]) and tasks in angle brackets (« »). Consider two examples. “We present an application of [[ ambiguity packing and
stochastic disambiguation techniques ]] for Lexical-Functional Grammars to the domain of «sentence condensation »”
is positive: the method is explicitly applied via purposive language. In contrast, “We examine the relationship between
the two «grammatical formalisms»: [[ Tree Adjoining Grammars ]] and Head Grammars” is negative: the relationship
is comparative, not applicative.

4.4   Clinical Trial Eligibility

The clinical trial eligibility task requires determining whether a natural language statement about patient eligibility
logically follows from stated inclusion and exclusion criteria. We derive this benchmark from the NLI4CT dataset [24],
filtering to instances where the premise contains eligibility criteria and the hypothesis makes a claim about who may or
may not participate. The task is formulated as binary classification: entailment (the statement follows from the criteria)
or contradiction (the statement conflicts with the criteria).
This task demands precise logical reasoning over medical terminology. Inclusion criteria specify conditions patients
must satisfy; exclusion criteria specify disqualifying conditions. A statement entails when its claim is a logical
consequence of these criteria, accounting for synonymy (“claustrophobia” and “fear of confined spaces” are equivalent)
and implicit exclusion (if inclusion requires lymph node status N0 or N1, then N2 patients are excluded). The logical
formalisation is:

                                    Entails(s, p) ⇔ IsEligibilityStatement(s)
                                                    ∧ IsEligibilityCriteria(p)                                         (4)
                                                    ∧ FollowsFromPremise(s, p)

where s denotes the hypothesis statement and p the premise containing trial criteria. The FollowsFromPremise predicate
requires evaluating whether the claim in s can be derived from the logical structure of p, rather than merely checking
for textual overlap.
The ontology defines EligibilityStatement and EligibilityCriteria as the primary classes, with Entailment and Contradic-
tion modeled as disjoint subclasses of EligibilityStatement. The SWRL rule infers membership in Entailment when the
statement is classified as following from the premise.


                                                           10
                                                                                        A PREPRINT - JANUARY 6, 2026


Unlike hearsay determination, where reasoning concerns evidentiary purpose, clinical eligibility requires domain
knowledge about medical terminology and clinical trial protocols. Consider two examples. Given the exclusion criterion
“Known claustrophobia, presence of pacemaker and/or ferromagnetic material in their body that would prohibit MRI
imaging”, the statement “Patients with irrational fear of confined spaces are not eligible for the primary trial” entails:
the model must recognise synonymy between “claustrophobia” and “irrational fear of confined spaces”. Conversely,
given inclusion criteria specifying organ function thresholds, the statement “xiap gene mutation” neither follows from
nor contradicts the premise, it references absent information, yielding a contradiction under the NLI4CT annotation
scheme.

4.5    Ontology Design Patterns

The three task ontologies share a common architectural pattern. Each ontology defines OWL classes representing
domain entities (statements, methods, eligibility criteria) and object properties capturing their relationships. The target
classification is modeled as class membership: an individual belongs to Hearsay, MethodApplication, or Entailment
when the SWRL rule’s antecedent conditions are satisfied. This target class is consistently defined as a subclass of the
primary entity class, reflecting that not all statements are hearsay, not all methods are applied, and not all eligibility
claims entail.
As described in Section 3.3, we include complementary predicates as an experimental condition to test whether
findings from our prior work generalise. Each task ontology defines appropriate assertion pairs: FunctionalConn with
NoFunctionalConn for method application, FollowsFromPremise with StatementConflictsWithPremise for eligibility,
and IsOutOfCourt with IsInCourt for hearsay.
Practitioners formalising new domains should begin by identifying the target classification and its necessary conditions,
then work backward to the entities and relationships those conditions presuppose. Entity and assertion specifications
require particular care, as they constitute the natural language interface between the ontology and the LLM, vague
descriptions yield inconsistent extractions. The suitability criteria from Section 4.1 should be verified before investing in
ontology development: if the task lacks deterministic semantics or authoritative rule sources, structured decomposition
will not succeed.

5     Experimental Design
The framework is evaluated across three reasoning tasks spanning legal, scientific, and medical domains, each satisfying
the suitability criteria established in Section 4: a rule-expressible decision boundary and formalisable predicate structure.
Eleven language models and six experimental conditions yield 33 model-task combinations, enabling assessment of
cross-domain generalisability, model capability requirements, and the contribution of symbolic verification through
controlled ablation. Table 3 summarises the dataset characteristics.

    Table 3: Dataset summary across evaluation tasks. All tasks use stratified sampling to preserve class distributions.
                   Task                      Source               Test Train Positive Negative
                    Hearsay                      LegalBench [30]     94       5        41          53
                    Method Application           SciERC [32]         94       5        52          42
                    Clinical Trial Eligibility   NLI4CT [24]         94       4        47          47


Hearsay Determination. We use the LegalBench hearsay determination task [30], which requires determining
whether evidence constitutes inadmissible hearsay under Rule 801 of the Federal Rules of Evidence. The dataset
provides natural language descriptions of evidentiary scenarios with binary labels (Yes/No). We use the standard
train/test split provided by LegalBench: 94 test instances and 5 training instances (used as few-shot exemplars).

Method Application. We derive this task from the SciERC dataset [32], which annotates scientific abstracts with
entity and relation labels. We filter to instances involving the Used-For relation and formulate the problem as binary
classification: given text with marked method and task entities (using bracket notation inherited from the dataset
preprocessing), determine whether the method is functionally applied to the task. Instances are sampled to yield 94 test
and 5 training examples.

Clinical Trial Eligibility. We filter the NLI4CT dataset [24] to instances where the premise contains eligibility-related
content, identified by keywords including “Eligibility”, “Inclusion”, “Exclusion”, and “DISEASE CHARACTERIS-


                                                            11
                                                                                      A PREPRINT - JANUARY 6, 2026


TICS”. The task requires determining whether a natural language statement about patient eligibility logically follows
from stated criteria. We apply stratified sampling to balance entailment and contradiction labels, yielding 94 test
instances and 4 training instances with balanced class distribution.
All datasets are processed through a unified pipeline that standardises the input format and label encoding. Text inputs
are preserved in their original form without normalisation to maintain domain-specific terminology and formatting
conventions. Labels are mapped to a consistent binary format (Yes/No) across all tasks. The preprocessing code and
dataset generation scripts are available in our supplementary repository.2
We constrain test set sizes to 94 instances per task, determined by the smallest available dataset (hearsay). This ensures
balanced evaluation across domains and enables direct comparison of framework performance without confounding
from unequal sample sizes.

5.1       Model Selection and Configuration

We evaluate our framework across eleven language models from four providers, selected to represent diverse architectural
approaches and capability levels. Table 4 summarises the models and their configurations.


                             Table 4: Models evaluated across all experimental conditions.
                    Provider             Model                 Identifier
                                           GPT-5 Nano            gpt-5-nano
                                           GPT-5 Mini            gpt-5-mini
                    OpenAI
                                           GPT-5.2               gpt-5.2
                                           o3                    o3
                                           Claude 4.5 Sonnet     claude-sonnet-4-5-20250929
                    Anthropic
                                           Claude 4.5 Haiku      claude-haiku-4-5-20251001
                                           Gemini 2.5 Flash      gemini-2.5-flash
                    Google
                                           Gemini 2.5 Pro        gemini-2.5-pro
                                           Qwen 3                qwen3-235b-a22b-instruct-2507
                    Fireworks AI           DeepSeek v3.2         deepseek-v3p2
                                           Kimi K2               kimi-k2-instruct-0905


Models were selected to provide coverage across three dimensions. First, architectural diversity: we include both
standard autoregressive models and reasoning-optimised variants to assess whether explicit reasoning mechanisms
interact with structured decomposition. Second, capability spectrum: models range from smaller, faster variants (GPT-5
Nano, Claude 4.5 Haiku, Gemini 2.5 Flash) to larger, more capable models (GPT-5.2, Claude 4.5 Sonnet, Gemini 2.5
Pro), enabling analysis of how model capability affects framework performance. Third, provider diversity: including
models from multiple providers reduces the risk that findings are artifacts of a single training methodology or model
family.
All models use deterministic settings where available (temperature 0.0) to ensure reproducibility. Responses are
structured via Pydantic (v2.x) models through the LangChain framework, ensuring consistent output parsing across all
models and conditions.

5.2       Experimental Conditions

We evaluate six experimental conditions to isolate the contributions of different framework components and assess the
effect of complementary predicates. Table 5 summarises the condition matrix.

Few-Shot Prompting (FS). The baseline condition provides models with training examples from each task followed
by a new test case. Models receive the task description, few-shot exemplars (input-output pairs from the training split),
and the test input, then generate a direct classification. This baseline represents standard practice for LLM-based
classification without explicit reasoning structure.

      2
          https://github.com/albsadowski/ruleeval-xd


                                                           12
                                                                                       A PREPRINT - JANUARY 6, 2026



Table 5: Experimental condition matrix. SD conditions use SWRL-based reasoning; SD-Direct conditions bypass
symbolic verification.
                   Condition               Symbolic Verification Complementary Predicates
                   Few-Shot (FS)                           —                            —
                   Chain-of-Thought (CoT)                  —                            —
                   SD                                      ✓                            —
                   SD-Comp                                 ✓                            ✓
                   SD-Direct                               —                            —
                   SD-Direct-Comp                          —                            ✓


Chain-of-Thought Prompting (CoT). Models are instructed to reason step-by-step before providing a final answer.
This baseline assesses whether general reasoning elicitation provides benefits comparable to our structured approach,
following the methodology established by Wei et al. [50].

Structured Decomposition (SD). The framework as described in Section 3, using standard predicate definitions
without complementary predicates. Models perform entity identification and assertion extraction according to task
ontology specifications, with extracted predicates evaluated by the Pellet reasoner using SWRL rules.

Structured Decomposition with complementary predicates (SD-Comp). Identical to SD, but with complementary
predicates included in the assertion specifications. Complementary predicates are paired assertions representing
opposing determinations (e.g., both FunctionalConn and NoFunctionalConn), designed to force the LLM to make
explicit determinations on both positive and negative conditions rather than defaulting to one option. Introduced to
address the confirmation bias of LLMs.

Structured Decomposition Direct (SD-Direct). An ablation condition that uses identical entity and assertion
specifications as SD (without complementary predicates) but bypasses the OWL/SWRL verification step. Instead, the
LLM directly determines the final classification based on extracted predicates in a single additional inference call. This
ablation isolates the contribution of symbolic verification.

Structured Decomposition Direct with complementary predicates (SD-Direct-Comp). Identical to SD-Direct, but
with complementary predicates included.
The six conditions form a 2 × 2 factorial design (symbolic verification × complementary predicates) plus two baselines.
This design enables us to assess: (1) whether structured decomposition with SWRL verification outperforms baselines;
(2) whether symbolic verification provides value beyond structured prompting alone (SD vs. SD-Direct); and (3)
whether complementary predicates improve performance, and whether this effect interacts with symbolic verification
(comparing the complementary predicate effect across SD and SD-Direct conditions).

5.3   Evaluation Metrics

We report four metrics for each model-task-condition combination. Following standard practice in binary classification
evaluation, we use the F1 score as the primary metric for comparing conditions. F1 balances precision and recall,
providing a single summary statistic that accounts for both false positives and false negatives. All statistical comparisons
use paired t-tests over F1 scores across model-task combinations.
We additionally report:

       • Accuracy: The proportion of correct classifications, providing an intuitive measure of overall performance.
       • Precision: The proportion of positive predictions that are correct, relevant for applications where false positives
         carry high costs.
       • Recall: The proportion of actual positives correctly identified, relevant for applications where false negatives
         carry high costs (e.g., compliance screening).

We assess the significance of performance differences using paired t-tests over the 33 model-task combinations (11
models × 3 tasks). Effect sizes are reported as Cohen’s d. We consider p < 0.05 as the threshold for statistical
significance.


                                                            13
                                                                                      A PREPRINT - JANUARY 6, 2026


Table 6: Average performance across all 33 model-task combinations. SD achieves the highest F1 while maintaining
notably higher recall than baseline methods. SD-C = SD with complementary predicates.

    Method        Acc.                      Prec.                     Recall                     F1
    Few-shot      78.4%                     85.3%                     69.0%                      75.2%
    CoT           77.6%                     85.7%                     68.2%                      74.1%
    SD            80.0%                     79.4%                     84.7%                      79.8%
    SD-C          77.4%                     81.2%                     74.2%                      74.8%
    SD-Direct     73.6%                     77.7%                     71.2%                      70.1%
    SD-Direct-C   76.4%                     79.8%                     73.4%                      72.5%


Results are aggregated at three levels: (1) overall averages across all model-task combinations, (2) task-level averages
across models, and (3) model-level averages across tasks. This multi-level analysis enables identification of both general
patterns and specific model-task interactions.

5.4    Implementation and Reproducibility

Task definitions are formalised as OWL 2 ontologies with SWRL rules encoding classification logic. We use the owl-
ready2 Python library (v0.45) for ontology manipulation and the Pellet reasoner [44] for SWRL rule execution. During
evaluation, a fresh OWL world is instantiated for each test instance to ensure isolation between examples. Extracted
entities and assertions are translated to ABox assertions, the reasoner performs inference, and class membership of the
target individual determines the classification outcome.
All LLM interactions use the LangChain framework (v0.3.x) with provider-specific API clients. Structured output is
enforced via Pydantic models specifying the expected response schema for entity identification and assertion extraction
steps.
Experiments were conducted using Python 3.13 on Linux systems. API calls were made to provider endpoints (OpenAI,
Anthropic, Google Gemini API, Fireworks AI) between 2025-12-01 and 2025-12-20.
We provide the following materials to support reproducibility:

        • Dataset generation code: https://github.com/albsadowski/ruleeval-xd
        • Framework implementation including ontologies, prompts, and evaluation scripts: https://github.com/
          albsadowski/structured-decomposition-swj

The OWL ontologies for all three tasks, including TBox definitions, SWRL rules, and sd: namespace annotations for
LLM prompting, are included in the framework repository.


6     Results

We evaluated structured decomposition (SD) against baselines across 11 models and 3 tasks, yielding 33 model-task
combinations. The experimental design includes four SD variants to isolate the contributions of symbolic verification
and complementary predicates. Table 6 summarises performance across all conditions; full results for each model-task
combination are provided in Table 9, with ablation comparisons in Table 7.

6.1    Overall Performance

Structured decomposition without complementary predicates achieved the highest average F1 score (79.8%) compared
to few-shot prompting (75.2%), chain-of-thought (74.1%), and the SD-Direct ablation (70.1%). The improvement over
few-shot prompting was 4.6 percentage points and statistically significant according to a paired t-test (t(32) = 2.88,
p = 0.007, Cohen’s d = 0.5). The improvement over chain-of-thought was 5.7 percentage points (t(32) = 2.84,
p = 0.008, d = 0.5). Figure 3 illustrates these performance shifts across all model-task combinations.
As shown in Figure 3, the Method Application task exhibits the most consistent improvements, with nearly all models
benefiting from structured decomposition. The Hearsay and Clinical Trial Eligibility tasks show greater variability, with
some models experiencing regression, suggesting that framework effectiveness depends on both task characteristics and
model.


                                                           14
                                                                                     A PREPRINT - JANUARY 6, 2026




Figure 3: Performance shift from few-shot baseline (blue) to structured decomposition (red) across eleven models
and three tasks. Green lines indicate improvement; red lines indicate regression. Method Application shows the most
consistent gains.




6.2   Ablation: Contribution of Symbolic Verification


To isolate the contribution of the symbolic reasoning component, we compare SD against SD-Direct, an ablation
condition that uses identical assertion specifications and extraction prompts but bypasses the OWL/SWRL verification
step, instead asking the LLM to directly determine the classification from extracted predicates. SD outperformed
SD-Direct by 9.7 percentage points (t(32) = 3.71, p = 0.001, d = 0.65), confirming that the symbolic verification
component provides substantial benefit beyond the structured predicate definitions alone. Table 7 presents the complete
ablation results.
This ablation result is notable: providing structured assertion specifications without symbolic verification actually
degrades performance compared to few-shot prompting (70.1% vs. 75.2% F1). The decomposition into predicates
appears to introduce additional opportunities for error that only pay off when coupled with formal verification. This
finding underscores that architectural decomposition with symbolic reasoning drives the observed improvements.
The contribution of symbolic verification varies by task. On Clinical Trial Eligibility, the difference was particularly
pronounced: SD achieved 74.5% F1 compared to 54.6% for SD-Direct, a gap of 19.9 percentage points. Method
Application showed a more modest but still substantial difference of 8.5 percentage points (88.9% vs. 80.4%). On
Hearsay, the difference was minimal (75.9% vs. 75.2%), suggesting that for tasks requiring nuanced interpretation, the
extraction step dominates overall performance regardless of verification method.


                                                          15
                                                                                     A PREPRINT - JANUARY 6, 2026



Table 7: Ablation study: F1 scores (%) comparing structured decomposition with SWRL verification (SD, SD-C)
against variants without symbolic reasoning (SD-D, SD-D-C). Best result per row within each task is shown in bold.
                                Hearsay                      Method Application                 Clinical Trial Eligibility
 Model               SD     SD-C   SD-D    SD-D-C     SD      SD-C   SD-D    SD-D-C      SD        SD-C     SD-D      SD-D-C
 o3                  84.8   79.1    88.6     85.1     93.3    95.2    92.2        95.1   75.9       66.7     62.2       71.4
 GPT-5.2             84.8   84.7    77.6     89.7     93.5    94.3    85.2        94.2   76.7       50.7     60.9       56.3
 GPT-5 Mini          86.4   77.1    82.2     84.4     87.4    82.1    91.7        90.7   81.8       70.0     62.2       63.0
 GPT-5 Nano          66.7   63.5    72.4     70.6     90.7    80.8    88.5        87.9   67.5       64.0     58.3       59.2
 Claude 4.5 Sonnet   76.9   76.1    79.5     78.5     94.4    87.8    49.3        77.6   76.2       55.1     36.6       45.9
 Claude 4.5 Haiku    58.3   72.9    69.0     71.3     76.9    81.4    79.2        81.5   65.8       62.2     47.1       41.3
 Gemini 2.5 Pro      79.1   72.7    87.4     84.4     90.7    91.6    76.2        84.7   80.5       71.8     70.1       69.6
 Gemini 2.5 Flash    78.4   78.0    72.2     72.1     94.5    93.7    92.6        91.7   69.9       66.7     60.4       64.4
 DeepSeek v3.2       77.6   61.5    48.1     29.2     93.3    91.7    65.8        90.2   55.9       37.3      8.2       8.2
 Kimi K2             74.1   77.2    77.6     79.1     83.8    78.3    81.5        82.5   82.1       83.0     71.4       73.2
 Qwen 3              68.3   62.9    73.1     73.3     79.7    78.7    82.2        82.9   86.8       78.0     63.0       64.9
 Average             75.9   73.2    75.2     74.3     88.9    86.9    80.4        87.1   74.4       64.1     54.5       56.1




Figure 4: Precision-recall trade-offs by prompting strategy. Dashed curves show F1 iso-lines (0.6–0.9). Structured
decomposition (triangles) achieves higher recall, with strongest performance on Method Application, supporting
generalisation beyond the legal domain.



6.3   Ablation: Effect of Complementary Predicates

Contrary to findings from our prior work [41], complementary predicates significantly degraded performance in the
current evaluation. SD without complementary predicates outperformed SD with complementary predicates (SD-C) by
5.0 percentage points (79.8% vs. 74.8%, t(32) = 3.69, p = 0.001, d = 0.64).
This effect was most pronounced on Clinical Trial Eligibility, where complementary predicates reduced F1 by 10.3
percentage points (74.5% vs. 64.1%). On Hearsay, the reduction was 2.8 percentage points (75.9% vs. 73.2%), and on
Method Application, 2.1 percentage points (88.9% vs. 86.9%).
The pattern persisted in the SD-Direct conditions: SD-Direct without complementary predicates outperformed the
variant with complementary predicates on Hearsay (75.2% vs. 74.3%) and Clinical Trial Eligibility (54.5% vs. 56.1%),
though the relationship was mixed on Method Application (80.4% vs. 87.1%).


                                                        16
                                                                                       A PREPRINT - JANUARY 6, 2026


Table 8: SD performance by task. SD > FS indicates proportion of models where SD outperformed few-shot prompting.

                                Task                          ∆ F1      p     SD > FS
                                Hearsay                       +2.8pp   .402     7/11
                                Method Application            +7.3pp   .034     8/11
                                Clinical Trial Eligibility    +3.6pp   .104     8/11


6.4   Precision-Recall Characteristics

A notable pattern emerged in the precision-recall trade-offs (Figure 4). SD achieved substantially higher recall (84.7%)
compared to few-shot (69.0%) and chain-of-thought (68.2%). This difference of 15.7 percentage points over few-shot
was highly significant (t(32) = 7.00, p < 0.001, d = 1.22). The precision trade-off was modest: SD precision (79.4%)
was lower than few-shot (85.3%), but the recall gains more than compensated in terms of overall F1, as evidenced by
SD points clustering toward higher iso-lines in Figure 4.

6.5   Task-Level Analysis

Table 8 shows the breakdown by task, including the proportion of models for which SD outperformed few-shot
prompting.
SD performed best on the method application task, achieving a 7.3 percentage point improvement over few-shot
(p = 0.008) with 8 out of 11 models showing gains.
On clinical trial eligibility, SD outperformed few-shot on 8 out of 11 models with an aggregate improvement of 3.6
percentage points, though this did not reach statistical significance. Individual results revealed high variance: SD
produced substantial gains on some models (e.g., Qwen 3 at +6.3pp, GPT-5 Mini at +15.1pp) while underperforming on
others (e.g., GPT-5.2 at −4.3pp, DeepSeek v3.2 at −6.3pp).
The hearsay task showed the most variability, with 7 out of 11 models improving and modest aggregate gains (+2.8pp).
Some models showed large regressions (e.g., Claude 4.5 Haiku at −16.1pp, Qwen 3 at −5.3pp).

6.6   Individual Model-Task Results

The largest SD improvements over few-shot on method application were GPT-5.2 (+20.6pp), Claude 4.5 Sonnet
(+19.1pp), Gemini 2.5 Pro (+14.5pp), and GPT-5 Nano (+14.1pp). On clinical trial eligibility: GPT-5 Mini (+15.1pp),
o3 (+11.9pp), and Kimi K2 (+4.5pp). On hearsay: GPT-5 Nano (+19.5pp), o3 (+17.2pp), and GPT-5 Mini (+10.7pp).
Conversely, the largest regressions appeared primarily on hearsay: Claude 4.5 Haiku (−16.1pp), Gemini 2.5 Pro
(−7.0pp), and Qwen 3 (−5.3pp).

6.7   Model-Level Patterns

Aggregating across tasks, nine of eleven models showed positive average improvement with SD. o3 showed the strongest
gains (+9.5pp average), achieving the highest overall SD performance (84.7% F1). GPT-5.2 and Claude 4.5 Sonnet
showed similarly strong improvements (+6.3pp and +7.5pp respectively). The GPT family showed consistent positive
gains across all variants.
Three models showed degradation: Claude 4.5 Haiku (−6.4pp), Qwen 3 (−2.9pp), and Gemini 2.5 Flash (−1.1pp).
Within model families, larger variants tended to show greater improvement: Gemini 2.5 Pro (+6.9pp) versus Gemini 2.5
Flash (−1.1pp), and Claude 4.5 Sonnet (+7.5pp) versus Claude 4.5 Haiku (−6.4pp).


7     Discussion

Across all 33 model-task combinations, structured decomposition achieved an average F1 of 79.8%, compared to 75.2%
for few-shot and 74.1% for chain-of-thought. The improvement of 4.6 percentage points was statistically significant
(t(32) = 2.88, p = 0.007, Cohen’s d = 0.50), with nine of eleven models showing positive gains. Method application
showed the largest gains (+7.3pp), followed by clinical trial eligibility (+3.6pp) and hearsay (+2.8pp), confirming that
the framework generalises beyond the legal domain where it was originally validated.


                                                             17
                                                                                        A PREPRINT - JANUARY 6, 2026



Table 9: F1 scores (%) for all model-task combinations. Best result per row is shown in bold. FS = few-shot, CoT =
chain-of-thought, SD = structured decomposition (without complementary predicates), SD-C = SD with complementary
predicates.
                                     Hearsay                    Method Application        Clinical Trial Eligibility
       Model                FS     CoT     SD     SD-C     FS      CoT    SD     SD-C     FS    CoT     SD     SD-C
       o3                   67.6   71.4   84.8    79.1    91.8     90.5   93.3   95.2    64.0   63.0    75.9    66.7
       GPT-5.2              81.8   77.2   84.8    84.7    72.9     70.7   93.5   94.3    81.0   76.5    76.7    50.7
       GPT-5 Mini           75.7   62.9   86.4    77.1    94.0     87.2   87.4   82.1    66.7   67.5    81.8    70.0
       GPT-5 Nano           47.2   51.4   66.7    63.5    76.6     75.2   90.7   80.8    66.7   59.2    67.5    64.0
       Claude 4.5 Sonnet    69.7   76.0   76.9    76.1    75.3     71.4   94.4   87.8    70.1   54.1    76.2    55.1
       Claude 4.5 Haiku     74.4   78.1   58.3    72.9    82.6     88.0   76.9   81.4    62.2   56.3    65.8    62.2
       Gemini 2.5 Pro       75.0   86.1   79.1    72.7    76.2     80.5   90.7   91.6    74.1   79.5    80.5    71.8
       Gemini 2.5 Flash     84.3   85.4   78.4    78.0    82.6     81.8   94.5   93.7    74.1   68.4    69.9    66.7
       DeepSeek v3.2        77.5   79.5   77.6    61.5    83.1     80.5   93.3   91.7    62.2   59.2    55.9    37.3
       Kimi K2              77.9   86.4   74.1    77.2    81.1     77.3   83.8   78.3    77.6   68.4    82.1    83.0
       Qwen 3               73.6   85.7   68.3    62.9    82.2     76.6   79.7   78.7    80.5   73.4    86.8    78.0
       Average              73.2   76.4   75.9    73.2    81.7     80.0   88.9   86.9    70.8   66.0    74.4    64.1



However, generalisability is bounded by task suitability. As demonstrated by the negative validation on URTI
classification (Section 4.1), structured decomposition requires two properties: a rule-expressible decision boundary and
formalisable predicate structure. Tasks where identical observable features can correspond to different labels, such
as medical diagnosis from symptom profiles, require statistical discrimination that logical rules cannot provide. The
framework is not a general-purpose improvement but a targeted approach for rule-governed domains.

7.1   The Contribution of Symbolic Verification

The ablation study establishes that SWRL-based reasoning provides substantial benefit beyond structured prompting
alone. SD outperformed SD-Direct by 9.7 percentage points overall, with the gap reaching 19.9 percentage points on
clinical trial eligibility. This difference confirms that the symbolic reasoner contributes meaningfully to classification
accuracy rather than serving as architectural overhead.
A notable finding is that structured prompting without symbolic verification actually degrades performance compared
to few-shot baselines (70.1% vs. 75.2% F1). Decomposing the task into entity identification and assertion extraction
introduces additional points where errors can occur. These errors compound when the LLM must also perform the final
classification. Symbolic verification appears to correct or constrain these errors, yielding net improvement. Without it,
the added complexity provides no benefit.
The contribution of symbolic verification varied by task. On clinical trial eligibility, where the reasoning involves
matching patient characteristics against explicit criteria, the reasoner’s contribution was largest. On hearsay, where
predicate extraction requires interpreting legal language with considerable ambiguity, the gap between SD and SD-Direct
was minimal. This suggests that when extraction difficulty dominates, verification cannot compensate for upstream
errors.

7.2   Rule Complexity and Framework Benefits

The task predicates in this evaluation are relatively simple logical structures. Hearsay determination is a conjunction of
five conditions; method application requires four predicates; clinical trial eligibility uses three. All are straightforward
conjunctions without disjunctions, nested quantifiers, or complex logical patterns. One might expect that such simple
rules would not benefit substantially from formal verification, as LLMs should be capable of evaluating a handful of
conjuncts directly.
Yet the results show otherwise. Method application, with only four predicates, showed the largest improvement over
few-shot (+7.3pp) and a substantial gap between SD and SD-Direct (88.9% vs. 80.4%). Clinical trial eligibility, with
only three predicates, showed the widest gap between SD and SD-Direct: 19.9 percentage points (74.5% vs. 54.6%).
The simplicity of the rules did not diminish the framework’s contribution.
This finding bears on the role of SD-Direct. One rationale for allowing the LLM to determine the final classification
from extracted predicates is that it might reconcile extraction deficiencies: seeing all predicates together, the model
could correct inconsistencies or adjust for low-confidence extractions. The results suggest this does not occur. SD-Direct


                                                            18
                                                                                     A PREPRINT - JANUARY 6, 2026


consistently underperformed SD on method application and clinical trial eligibility. Rather than correcting errors, the
additional inference step appears to introduce new ones.
The implication is that even simple logical rules benefit from external verification. The difficulty lies not in the
complexity of the rule but in the accumulation of small extraction errors across predicates. Each predicate extraction
carries some probability of error; when the LLM must also perform the final logical combination, these errors compound.
Symbolic verification eliminates one source of error entirely, yielding improvements even when the underlying logic is
trivial.

7.3   Complementary Predicates and Ontology Design

Contrary to expectations from our prior work [41], complementary predicates degraded performance by 5.0 percentage
points overall (p = 0.001), with the largest effect on clinical trial eligibility (−10.3pp). Our prior work hypothesised
that complementary predicates would improve precision by forcing explicit consideration of both positive and negative
conditions, addressing confirmation bias and grounding reasoning under OWL’s open-world assumption. However,
even in that evaluation, benefits were concentrated in specific models (o1: +14.5pp F1, o3-mini: +13.7pp) while others
showed mixed effects (Claude 3.7 Sonnet: −1.3pp). The current evaluation, using a different and more recent model
set, observes consistently negative effects across GPT-5 variants, Claude 4.5, and Gemini 2.5. Two factors likely
contribute: the benefit appears highly model-specific rather than universal, and confirmation bias may be less prevalent
in current-generation LLMs, reducing the benefit while the additional cognitive load of evaluating paired assertions
introduces extraction errors.
This finding has practical implications for ontology design in neural-symbolic systems. When LLMs handle entity and
predicate extraction, simpler ontologies with fewer assertions appear preferable. The theoretical benefits of explicit
negation under the open-world assumption do not outweigh the practical costs of increased extraction complexity.
Practitioners designing task ontologies should favour minimal predicate sets that capture necessary conditions without
redundant complementary assertions, and empirically validate any complementary predicates for their specific model
deployments rather than assuming benefit.

7.4   Precision-Recall Trade-offs

SD achieved substantially higher recall than baselines (84.7% vs. 69.0% for few-shot), with a modest reduction in
precision (79.4% vs. 85.3%). This pattern was consistent across all three tasks.
The recall advantage suggests that structured decomposition may be particularly suited to applications where false
negatives carry higher costs than false positives. Compliance screening, eligibility determination, and evidence review
are examples where missing a relevant case is more costly than flagging a borderline one for human review. The
framework’s tendency toward inclusive classification aligns with these use cases.
For applications where false positives are more costly, the framework’s precision-recall profile may be less appropriate,
or additional filtering mechanisms may be needed downstream.

7.5   Model Capability Requirements

Within model families, larger and more capable variants showed greater improvement from structured decomposition.
Gemini 2.5 Pro gained 8.3 percentage points while Gemini 2.5 Flash 0.6 percentage points. Claude 4.5 Sonnet gained
10.8 percentage points while Claude 4.5 Haiku lost 6.1 percentage points.
This pattern reflects the framework’s architecture. The decomposition approach relies on the model to correctly identify
entities and extract assertions according to ontology specifications. Models with stronger instruction-following and
reasoning capabilities perform this extraction more accurately. The symbolic verification step guarantees correct
rule application given the extracted predicates, but it cannot compensate for extraction errors in earlier steps. When
extraction quality is poor, the framework’s benefits do not materialise.
Practitioners should therefore consider model capability when deciding whether to deploy structured decomposition.
The framework is not a substitute for model quality but rather a way to leverage capable models more effectively on
rule-governed tasks.

7.6   Benefits of Semantic Web Integration

The 1 motivated our transition from SMT to OWL/SWRL on pragmatic grounds (reliability at scale) while noting
strategic advantages in inference expressivity. Here we assess these benefits in light of the experimental results.


                                                          19
                                                                                      A PREPRINT - JANUARY 6, 2026


The populated ABox provides a complete reasoning trace. Each entity extracted, each assertion evaluated, and each
justification persists as an explicit record. When a classification is incorrect, practitioners can inspect the ABox to
identify which extraction step failed. This traceability derives from the decomposition architecture itself rather than
from OWL specifically; the choice of representation affects how traces are stored and queried, not whether they exist.
However, the ABox integrates with standard semantic web tooling without requiring separate infrastructure for rule
execution and result storage. The SPARQL query in Section 3 demonstrates that extraction decisions are queryable
directly. We do not claim SPARQL provides capabilities unavailable in relational databases; the value lies in a unified
formalism spanning task definition, rule evaluation, and result inspection.
Task definitions become reusable artifacts editable in standard ontology tooling such as Protégé and validatable for
logical consistency prior to deployment. The separation between task specification (TBox) and instance data (populated
ABox) supports iterative refinement by domain experts without modifying framework code.
The OWL foundation positions the framework for inference patterns beyond those evaluated here. Class hierarchies
could enable structured multi-class output where predictions belong to multiple abstraction levels. Multiple SWRL rules
firing independently over the same ABox could support multi-label classification without combinatorial rule explosion.
Composable ontologies could import established domain vocabularies such as SNOMED-CT for medical applications or
FIBO for financial domains. Our evaluation focused on binary classification tasks, though the architectural foundation
supports these richer patterns without modification.


7.7   Limitations and Future Work

Several limitations constrain the interpretation of these results and suggest directions for future work.
All three evaluation tasks involve binary classification. The framework’s applicability to multi-class classification,
ranking, or extraction tasks remains untested. Similarly, the task predicates evaluated here are simple conjunctions;
whether benefits extend to more complex logical structures involving disjunctions, negation, or nested quantifiers is
unknown.
Ontology design required manual effort by the authors. Creating effective entity and assertion descriptions demands
domain understanding and iterative refinement. The effort required for new domains was not systematically measured.
Recent work on multi-agent frameworks for automated knowledge acquisition [42] suggests a potential path toward
reducing this burden, though such approaches introduce their own validation challenges.
We evaluated only English-language tasks; performance on other languages, where LLM capabilities may differ, is
unknown.
Finally, the interaction between model capability and framework effectiveness suggests that as LLMs continue to
improve, the optimal division of labour between neural extraction and symbolic verification may shift. Longitudinal
evaluation across model generations would help characterise this relationship.


8     Conclusion

This paper presented an integration pattern that combines LLMs with OWL/SWRL reasoning for rule-based tasks
over natural language input. The core architectural insight is that LLMs can serve as ontology population engines:
components that translate unstructured text into ABox assertions according to expert-authored TBox specifications. This
division exploits the complementary strengths of neural and symbolic approaches. LLMs handle the interpretive work of
understanding natural language, while SWRL-based reasoners apply rules with deterministic guarantees. The populated
ABox integrates with standard semantic web tooling for inspection and querying, and the formulation positions the
framework for inference patterns that simpler formalisms cannot express: class hierarchies, multi-label classification,
and composable imports from established domain vocabularies.
The paper makes two contributions. First, we demonstrate that grounding neural-symbolic integration in semantic
web standards yields a principled architecture for rule-based reasoning. The separation between expert-authored TBox
specifications and LLM-populated ABox assertions creates inspectable reasoning traces where every extraction decision
persists as a queryable record. Second, we validate this pattern empirically across three domains and a diverse set of
language models. Structured decomposition achieved statistically significant improvements over few-shot prompting in
aggregate, with gains observed across legal reasoning, scientific text analysis, and medical inference. An ablation study
confirmed that symbolic verification provides substantial benefit beyond structured prompting alone: removing the
SWRL reasoning step markedly degraded performance.


                                                           20
                                                                                     A PREPRINT - JANUARY 6, 2026


The pattern offers a principled answer to a recurring question in neural-symbolic integration: how should LLMs
and formal reasoning systems be combined? By grounding the integration in semantic web standards, the approach
inherits decades of tooling, well-defined semantics, and established practices for ontology engineering. The result is a
framework where LLMs do what they do best, interpret language, while formal systems provide the guarantees that
high-stakes domains require.

References
[1] A. Aidid, “Toward an Ethical Human-Computer Division of Labor in Law Practice,” Fordham Law Review, vol. 92,
    no. 5, pp. 1797–1813, 2024. https://fordhamlawreview.org/wp-content/uploads/2024/03/Vol.-92_
    Aidid-1797-1813.pdf.
[2] F. Baader, D. Calvanese, D. L. McGuinness, D. Nardi, and P. F. Patel-Schneider (eds.), The Description Logic
    Handbook: Theory, Implementation, and Applications, 2nd ed., Cambridge University Press, 2007, ISBN 978-0-
    521-87625-4.
[3] H. Babaei Giglou, J. D’Souza, and S. Auer, “LLMs4OL: Large Language Models for Ontology Learning,”
    arXiv:2307.16648, 2023. doi:10.48550/arXiv.2307.16648.
[4] R. M. Bakker, D. L. Di Scala, M. H. T. de Boer, and S. A. Raaijmakers, “Ontology Learning with LLMs: A
    Benchmark Study on Axiom Identification,” arXiv preprint arXiv:2512.05594 [cs.AI], 2025.
[5] T. J. M. Bench-Capon and P. R. S. Visser, “Open Texture and Ontologies in Legal Information Systems,” in Proc.
    8th Int. Conf. Database and Expert Systems Applications (DEXA ’97), Toulouse, France, pp. 192–197, 1997.
    doi:10.1109/DEXA.1997.617268.
[6] A. Blair-Stanek and B. Van Durme, “LLMs Provide Unstable Answers to Legal Questions,” arXiv:2502.05196,
    2025. doi:10.48550/arXiv.2502.05196.
[7] N. Borazjanizadeh and S. T. Piantadosi, “Reliable Reasoning Beyond Natural Language,” arXiv:2407.11373, 2024.
    doi:10.48550/arXiv.2407.11373.
[8] S. Bubeck, V. Chandrasekaran, R. Eldan, J. Gehrke, E. Horvitz, E. Kamar, P. Lee, Y. T. Lee, Y. Li, S. Lundberg, H.
    Nori, H. Palangi, M. T. Ribeiro, and Y. Zhang, “Sparks of Artificial General Intelligence: Early experiments with
    GPT-4,” arXiv:2303.12712, 2023. doi:10.48550/arXiv.2303.12712.
[9] D. Calanzone, S. Teso, and A. Vergari, “Logically Consistent Language Models via Neuro-Symbolic Integration,”
    arXiv:2409.13724, 2024. doi:10.48550/arXiv.2409.13724.
[10] M. Choinski and J. A. Chudziak, “Ontological Learning Assistant for Knowledge Discovery and Data Mining,” in
    Proc. IMCSIT, pp. 147–155, 2009. doi:10.1109/IMCSIT.2009.5352735.
[11] J. Cummins, J. Dávila, R. Kowalski, and D. Ovenden, “Computable Contracts for Insurance: Establishing an
    Insurance-Specific Controlled Natural Language – InsurLE,” 2025.
[12] M. Dahl, V. Magesh, M. Suzgun, and D. E. Ho, “Large Legal Fictions: Profiling Legal Hallucinations in Large
    Language Models,” Journal of Legal Analysis, vol. 16, no. 1, pp. 64–93, 2024. doi:10.1093/jla/laae003.
[13] T. Khot, H. Trivedi, M. Finlayson, Y. Fu, K. Richardson, P. Clark, and A. Sabharwal, “Decomposed Prompting: A
    Modular Approach for Solving Complex Tasks,” arXiv:2210.02406, 2022. doi:10.48550/arXiv.2210.02406.
[14] M. D. DiSorbo, H. Ju, and S. Aral, “Teaching AI to Handle Exceptions: Supervised Fine-Tuning with Human-
    Aligned Judgment,” arXiv:2503.02976, 2025. doi:10.48550/arXiv.2503.02976.
[15] A. Fansi Tchango, R. Goel, Z. Wen, J. Martel, and J. Ghosn, “DDXPlus: A new dataset for automatic medical
    diagnosis,” arXiv:2205.09148, 2022.
[16] L. Gao, A. Madaan, S. Zhou, U. Alon, P. Liu, Y. Yang, J. Callan, and G. Neubig, “PAL: Program-aided Language
    Models,” arXiv:2211.10435, 2022. doi:10.48550/arXiv.2211.10435.
[17] B. Glimm, I. Horrocks, B. Motik, G. Stoilos, and Z. Wang, “HermiT: An OWL 2 Reasoner,” Journal of Automated
    Reasoning, vol. 53, no. 3, pp. 245–269, 2014. doi:10.1007/s10817-014-9305-1.
[18] I. Mirzadeh, K. Alizadeh, H. Shahrokhi, O. Tuzel, S. Bengio, and M. Farajtabar, “GSM-Symbolic: Under-
    standing the Limitations of Mathematical Reasoning in Large Language Models,” arXiv:2410.05229, 2024.
    doi:10.48550/arXiv.2410.05229.
[19] D. Herron, E. Jiménez-Ruiz, and T. Weyde, “On the Potential of Logic and Reasoning in Neurosym-
    bolic Systems Using OWL-Based Knowledge Graphs,” Neurosymbolic Artificial Intelligence, vol. 1, 2025.
    doi:10.1177/29498732251320043.


                                                          21
                                                                                        A PREPRINT - JANUARY 6, 2026


[20] P. Hitzler, M. Krötzsch, and S. Rudolph, Foundations of Semantic Web Technologies, Chapman & Hall/CRC,
    2009, 455 pp., ISBN 978-1-4200-9050-5.
[21] P. Hitzler and M. K. Sarker (eds.), Neuro-Symbolic Artificial Intelligence: The State of the Art, Frontiers in Artificial
    Intelligence and Applications, vol. 342, SAGE Publications / IOS Press, 2022, 408 pp., ISBN 978-1-64368-244-0.
[22] S. Hertling and H. Paulheim, “OLaLa: Ontology Matching with Large Language Models,” in Proc. 13th Int. Conf.
    Knowledge Capture (K-CAP 2023), pp. 89–97, 2023. doi:10.1145/3587259.3627571.
[23] Y. Hu, L. Gan, W. Xiao, K. Kuang, and F. Wu, “Fine-tuning Large Language Models for Improving Factuality in
    Legal Question Answering,” arXiv:2501.06521, 2025. doi:10.48550/arXiv.2501.06521.
[24] M. Jullien, M. Valentino, H. Frost, P. O’Regan, D. Landers, and A. Freitas, “NLI4CT: Multi-evidence natural
    language inference for clinical trial reports,” arXiv:2305.03598, 2023.
[25] M. Kant, S. Nabi, M. Kant, R. Scharrer, M. Ma, and M. Nabi, “Towards Robust Legal Reasoning: Harnessing
    Logical LLMs in Law,” arXiv:2502.17638, 2025. doi:10.48550/arXiv.2502.17638.
[26] A. Kostka and J. Chudziak, “Synergizing Logical Reasoning, Knowledge Management and Collaboration in
    Multi-Agent LLM System,” in Proc. PACLIC 38, pp. 203–212, Dec. 2024. https://aclanthology.org/2024.
    paclic-1.19/.
[27] A. T. Kostka and J. A. Chudziak, “Towards Cognitive Synergy in LLM-Based Multi-Agent Systems,” in
    Proceedings of the Annual Meeting of the Cognitive Science Society, vol. 47, Cognitive Science Society, 2025.
    Available at: https://escholarship.org/uc/item/20j8628c.
[28] Vivian Lai, Chacha Chen, Alison Smith-Renner, Q. Vera Liao, and Chenhao Tan. Towards a science of human-AI
    decision making: An overview of design space in empirical human-subject studies. In Proceedings of the 2023
    ACM Conference on Fairness, Accountability, and Transparency (FAccT ’23), pages 1369–1385, Chicago, IL, USA,
    2023. Association for Computing Machinery. DOI: 10.1145/3593013.3594087.
[29] A. Lalwani, T. Kim, L. Chopra, C. Hahn, Z. Jin, and M. Sachan, “Autoformalizing Natural Language to First-Order
    Logic: A Case Study in Logical Fallacy Detection,” arXiv:2405.02318, 2024. doi:10.48550/arXiv.2405.02318.
[30] N. Guha, D. E. Ho, J. Nyarko, and C. Ré, “LegalBench: Prototyping a Collaborative Benchmark for Legal
    Reasoning,” arXiv:2209.06120, 2022. doi:10.48550/arXiv.2209.06120.
[31] G. Juneja, S. Dutta, and T. Chakraborty, “LM2 : A Simple Society of Language Models Solves Complex Reasoning,”
    arXiv:2404.02255, 2024. doi:10.48550/arXiv.2404.02255.
[32] Y. Luan, L. He, M. Ostendorf, and H. Hajishirzi, “Multi-task identification of entities, relations, and coreference
    for scientific knowledge graph construction,” in Proc. EMNLP 2018, Brussels, Belgium, pp. 3219–3232, Oct.–Nov.
    2018. doi:10.18653/v1/D18-1360.
[33] V. Magesh, F. Surani, M. Dahl, M. Suzgun, C. D. Manning, and D. E. Ho, “Hallucination-Free? Assessing the
    Reliability of Leading AI Legal Research Tools,” arXiv:2405.20362, 2024. doi:10.48550/arXiv.2405.20362.
[34] M. Matak and J. A. Chudziak, “GAIus: Combining GenAI with Legal Clauses Retrieval,” in Proc. ICAART, vol.
    3, pp. 868–875, 2025. doi:10.5220/0013191800003890.
[35] N. Mu, S. Chen, Z. Wang, S. Chen, D. Karamardian, L. Aljeraisy, B. Alomair, D. Hendrycks, and D. Wagner,
    “Can LLMs Follow Simple Rules?” arXiv:2311.04235, 2023. doi:10.48550/arXiv.2311.04235.
[36] A. Newell and H. A. Simon, Human Problem Solving. Englewood Cliffs, NJ: Prentice-Hall, 1972.
[37] M. Noguer I Alonso and F. S. Chatzianastasiou, “Automating Legal Contracts Using Logic Rules with Large
    Language Models,” SSRN, Nov. 2024. doi:10.2139/ssrn.5023212.
[38] P. Hitzler, M. Krötzsch, B. Parsia, P. F. Patel-Schneider, and S. Rudolph, “OWL 2 Web Ontology Language Primer
    (Second Edition),” W3C Recommendation, 2012. https://www.w3.org/TR/owl2-primer/.
[39] S. Pan, L. Luo, Y. Wang, C. Chen, J. Wang, and X. Wu, “Unifying Large Language Models and Knowledge
    Graphs: A Roadmap,” IEEE Transactions on Knowledge and Data Engineering, vol. 36, no. 7, pp. 3580–3599,
    Jul. 2024. doi:10.1109/TKDE.2024.3352100.
[40] E. D. Sacerdoti, “Planning in a hierarchy of abstraction spaces,” Artificial Intelligence, vol. 5, no. 2, pp. 115–135,
    1974.
[41] A. Sadowski and J. A. Chudziak, “Explainable rule application via structured prompting: A neural-symbolic
    approach,” Procedia Computer Science, vol. 270, pp. 2166–2175, 2025. doi:10.1016/j.procs.2025.09.337.
[42] A. Sadowski and J. A. Chudziak, “On Verifiable Legal Reasoning: A Multi-Agent Framework with For-
    malized Knowledge Representations,” in Proc. CIKM ’25, Seoul, Republic of Korea, pp. 2535–2545, 2025.
    doi:10.1145/3746252.3761057.


                                                             22
                                                                                  A PREPRINT - JANUARY 6, 2026


[43] S. Servantez, J. Barrow, K. Hammond, and R. Jain, “Chain of Logic: Rule-Based Reasoning with Large Language
    Models,” arXiv:2402.10400, 2024. doi:10.48550/arXiv.2402.10400.
[44] E. Sirin, B. Parsia, B. Cuenca Grau, A. Kalyanpur, and Y. Katz, “Pellet: A practical OWL-DL reasoner,” Journal
    of Web Semantics, vol. 5, no. 2, pp. 51–53, 2007. doi:10.1016/j.websem.2007.03.004.
[45] S. Harris and A. Seaborne, “SPARQL 1.1 Query Language,” W3C Recommendation, 2013. https://www.w3.
    org/TR/sparql11-query/.
[46] I. Horrocks, P. F. Patel-Schneider, H. Boley, S. Tabet, B. Grosof, and M. Dean, “SWRL: A Semantic Web Rule Lan-
    guage Combining OWL and RuleML,” W3C Member Submission, 2004. https://www.w3.org/Submission/
    SWRL/.
[47] X. Tan, Y. Deng, X. Qiu, W. Xu, C. Qu, W. Chu, Y. Xu, and Y. Qi, “Thought-Like-Pro: Enhancing Reason-
    ing of Large Language Models through Self-Driven Prolog-based Chain-of-Thought,” arXiv:2407.14562, 2024.
    doi:10.48550/arXiv.2407.14562.
[48] D. Tsarkov and I. Horrocks, “FaCT++ Description Logic Reasoner: System Description,” in Proc. IJCAR 2006,
    pp. 292–297, 2006. doi:10.1007/11814771_26.
[49] S. Wadhwa, S. Amir, and B. C. Wallace, “Revisiting Relation Extraction in the Era of Large Language Models,”
    in Proc. ACL 2023, pp. 15566–15589, 2023.
[50] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi, Q. V. Le, and D. Zhou, “Chain-of-Thought
    Prompting Elicits Reasoning in Large Language Models,” arXiv:2201.11903, 2022. doi:10.48550/arXiv.2201.11903.
[51] B. Wei, Y. Yu, L. Gan, and F. Wu, “An LLMs-based neuro-symbolic legal judgment prediction framework for civil
    cases,” Artificial Intelligence and Law, 2025. doi:10.1007/s10506-025-09433-1.
[52] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao, “ReAct: Synergizing Reasoning and Acting
    in Language Models,” arXiv:2210.03629, 2022. doi:10.48550/arXiv.2210.03629.




                                                        23
