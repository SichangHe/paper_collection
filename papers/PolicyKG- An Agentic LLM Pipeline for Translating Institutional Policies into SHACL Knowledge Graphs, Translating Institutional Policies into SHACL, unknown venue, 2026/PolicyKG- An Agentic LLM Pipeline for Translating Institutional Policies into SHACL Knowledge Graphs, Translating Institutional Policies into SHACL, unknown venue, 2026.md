                                           PolicyKG: An Agentic LLM Pipeline for
                                         Translating Institutional Policies into SHACL
                                                      Knowledge Graphs

                                                 Ponkrit Kaewsawee( )1[0009−0002−8382−4584] , Chaklam
                                                 Silpasuwanchai1[0000−0002−8670−6893] , and Chutiporn
                                                           Anutariya1[0000−0001−7101−212X]

                                                  Asian Institute of Technology, Pathum Thani, Thailand
                                                                  ponkrit.ka@spu.ac.th
                                                              {chaklam,chutiporn}@ait.asia
arXiv:2608.09028v1 [cs.AI] 10 Aug 2026




                                          Abstract. Institutional policies are written in natural language, but
                                          verifying compliance increasingly demands executable constraints, leav-
                                          ing organisations to bridge that gap by hand. We present PolicyKG,
                                          an agentic LLM pipeline that translates institutional policy documents
                                          into SHACL-validated knowledge graphs via a first-order deontic inter-
                                          mediate representation, orchestrated as four self-correcting stages over a
                                          LangGraph state machine. The main technical contribution is the Cor-
                                          pus Adapter, a configuration-driven vocabulary-grounding layer that con-
                                          strains LLM-generated predicates to a target ontology and enables cross-
                                          domain transfer by swapping registries rather than retraining models.
                                          Evaluated on the full Asian Institute of Technology Policies & Procedures
                                          corpus (1,663 sentences yielding 443 rules), PolicyKG achieves 86.9%
                                          deontic-type classification accuracy (Cohen’s κ = .709, corroborated by
                                          a three-annotator IRR with Fleiss’ κ = .844, item-level bootstrap 95% CI
                                          [.67, .97]) and SHACL shape correctness of F 1 = .866, 95% CI [.79, .93],
                                          on a 69-shape evaluation subset of an ontology-grounded reference set.
                                          End-to-end formalisation yield is 79.2% (351/443) via the FOL path;
                                          the remaining 20.8% fall back to a direct NL→SHACL path whose fail-
                                          ure modes are predominantly structural (long compound conjunctions,
                                          embedded bullets), not expressiveness-bounded. A two-pass audit (an
                                          automated regex checklist over all 443 rules plus a first-author man-
                                          ual review of the 92 FOL-fallback cases where higher-order constructs
                                          could otherwise hide) flagged zero second- or higher-order constructs
                                          (exact Clopper–Pearson upper 95% CI on the true HOL requirement
                                          rate: 0.67%). We report this as an audit finding for this corpus, not a
                                          proof of FOL sufficiency in general. A controlled cross-domain experi-
                                          ment on N = 15 GDPR rules raises exact property alignment from 1/15
                                          to 11/15 with the Corpus Adapter (Fisher’s exact p < .001; Cohen’s h
                                          = 1.53, large effect). External validation on the LexDeMod [21] lease-
                                          contract benchmark (N = 200) drops Macro F 1 from .810 to .370, with
                                          permission F 1 = .038; the failure mechanism is a vocabulary-prior mis-
                                          match (lease English uses shall be entitled for permission) precisely of
                                          the class the Corpus Adapter is designed to repair by registry swap. We
2       P. Kaewsawee et al.

      release the gold standard, both vocabulary registries, evaluation scripts,
      and pipeline configuration; repeated runs on the same host produce hash-
      identical SHACL outputs.

      Keywords: Knowledge Graphs · SHACL · Large Language Models ·
      Deontic Logic · Policy Formalisation · Ontology-Guided Generation ·
      Agentic Pipelines


1   Introduction
Institutional policies, which govern students, staff, and operations in universities,
hospitals, and government agencies, are written as natural-language documents
and read by humans. Yet the work of verifying that institutional practice con-
forms to those policies is increasingly automated: enrolment workflows, payment
systems, and accreditation reports all consume machine-readable data. The gap
between human-authored policy and machine-checked compliance is bridged to-
day by manual interpretation: a registrar reads a paragraph, decides what it
means, and configures a system rule. This process does not scale, does not sur-
vive policy revisions, and offers no audit trail linking a system check back to the
textual obligation it enforces.
    Three lines of research speak to this problem. Policy and legal NLP have
produced rule-extraction systems based on patterns [16], classical classifiers [3],
and recently large language models [8], reporting accuracies between 75% and
85% on isolated extraction tasks. Deontic logic, developed over more than half a
century, offers operators of obligation, permission, and prohibition that capture
the normative content of policy text [10,17]. SHACL, the W3C Shapes Constraint
Language [13], encodes validation constraints over RDF knowledge graphs and is
increasingly used for compliance checking [19]. Each of these threads has matured
in isolation. What is missing is an empirically validated, end-to-end pipeline
that connects natural-language policy to executable SHACL, together with a
satisfying answer to the open theoretical question of whether first-order logic
with deontic extensions is sufficient for institutional policy, or whether higher-
order constructs are required.
    We present PolicyKG, an agentic LLM pipeline that translates institu-
tional policy documents into SHACL-validated knowledge graphs. The pipeline
runs four orchestrated stages: document extraction, deontic rule classification,
FOL+deontic formalisation, and SHACL translation. A LangGraph state ma-
chine coordinates them, with per-stage validators that trigger self-correction on
local failure. We also introduce the Corpus Adapter: a configuration-driven
vocabulary-grounding layer that constrains LLM generation to a target ontol-
ogy and enables the same pipeline to retarget across domains by swapping the
registry. We evaluate PolicyKG on the full Asian Institute of Technology (AIT)
Policies & Procedures corpus, which contains 1,663 sentences yielding 443 deon-
tic rules, and demonstrate cross-domain transfer to a GDPR-derived corpus.

Contributions.
                                                                PolicyKG        3

 – An end-to-end agentic LLM pipeline (NL→FOL+deontic→SHACL) vali-
   dated on a real 1,663-sentence institutional corpus.
 – The Corpus Adapter, a vocabulary-grounding pattern that enables cross-
   domain transfer. A controlled GDPR experiment (N = 15) raises exact
   property alignment from 1/15 to 11/15 (Fisher’s exact p < .001; Cohen’s
   h = 1.53).
 – A two-pass empirical audit finding that first-order deontic logic is observa-
   tionally sufficient on this corpus: an automated regex checklist flags 0 of 443
   rules with second- or higher-order construct patterns [10], and a first-author
   manual review of the 92 FOL-fallback rules (where HOL requirements could
   otherwise hide behind LLM parse failure) confirms 0/92 genuine HOL cases
   (exact Clopper–Pearson upper 95% CI on the true HOL rate: 0.67%). Framed
   as an audit finding rather than a proof.
 – An open evaluation: three-annotator gold (Fleiss’ κ = .844, item-level boot-
   strap 95% CI [.67, .97]), LexDeMod external validation, and fixed-seed re-
   producibility yielding hash-identical SHACL outputs.


2     Related Work

2.1   Policy and Legal NLP
Pattern-based extraction was the first generation of automated policy NLP.
Maxwell and Antón [16] applied regular expressions and keyword templates
to privacy policies, reporting around 77% accuracy but struggling with syn-
tactic variation. Brodie et al. [3] improved on this using SVM classifiers over
hand-crafted features, reaching 82% on financial regulation but at a feature-
engineering cost that did not transfer across document types. Subsequent hybrids
of pattern matching and ontology grounding reached 85% accuracy on legal text
but at the price of substantial upfront ontology development. The common lim-
itation is reliance on bespoke features or hand-built ontologies; none draws on
the semantic priors of pre-trained language models.
    The recent LLM era has produced benchmarks but few end-to-end systems.
LexGLUE [4] established legal-language-understanding baselines across multiple
tasks; LegalBench [11] expanded to 162 legal-reasoning tasks. PAPEL [8] applied
chain-of-thought prompting to privacy-policy annotation, reaching 80% F1 on
clause labelling. These benchmarks define the landscape but do not, individually,
produce executable SHACL constraints from policy text.

2.2   Deontic Logic for Normative Systems

Deontic logic provides a mathematically rigorous account of obligation, per-
mission, and prohibition [17]. Governatori and Rotolo [10] argued, on theo-
retical grounds, that first-order deontic logic supplies sufficient expressiveness
for normative systems in legal and institutional contexts. The open question,
whether real institutional policies actually stay within FOL+deontic or reach
4      P. Kaewsawee et al.

into SOL/HOL territory, was framed by the standard articulation of the ex-
pressiveness/tractability trade-off [2]. Until the present work this question had
been addressed only at the theoretical level; we provide the first empirical audit
finding on a real institutional corpus (§6.2), scoped to the tested sub-domain
and framed as an observational lower bound on FOL adequacy rather than a
theoretical resolution. Standard Deontic Logic is known to be subject to the
Chisholm and Ross paradoxes, and to handle conditional exceptions (contrary-
to-duty obligations, waiver clauses) only awkwardly. The established response
is defeasible deontic logic [18,9], with argumentation- theoretic accounts of le-
gal reasoning [20] providing the broader framework. The interchange format
LegalRuleML [1] standardises the serialisation of such rules with defeasibility,
override, and temporal-scope metadata. PolicyKG does not attempt a full de-
feasible account; it records override relations via a custom deontic:overrides
annotation (§4) as a stepping stone that a downstream defeasible layer could
consume, and leaves full LegalRuleML alignment to future work (§8).


2.3   SHACL for Compliance
The W3C Shapes Constraint Language [13] enables declarative validation of
RDF knowledge graphs through node and property shapes annotated with sever-
ity levels. Palmirani and Governatori [19] argued that SHACL’s first-order pat-
tern language has adequate expressiveness for institutional policy formalisation,
encoding obligations, permissions, and prohibitions via severity and custom an-
notations. Their argument was theoretical and lacked empirical validation, and
no prior pipeline produces SHACL automatically from natural-language policy
text at the scale of an institutional corpus. PolicyKG provides the empirical
realisation their work anticipated.


2.4   LLMs for Structured Output and Knowledge Graph
      Construction

A growing body of work uses LLMs to construct or query knowledge graphs.
Schema-constrained and grammar-guided generation [23,7] forces LLM outputs
into well-typed structures, addressing the syntactic side of structured output.
Chain-of-thought prompting [22] is the dominant technique for multi-step rea-
soning tasks and underpins Stage 3’s FOL formalisation prompt in this pa-
per. Retrieval-augmented generation (RAG) [15] is the mainstream approach for
grounding LLM outputs in an external knowledge source at inference time, and
GraphRAG [6] extends the pattern to knowledge-graph retrieval, but it assumes
the target graph already exists. The semantic side of constructing that graph,
that is, ensuring LLM-generated predicates align with a target ontology rather
than hallucinated English property names, receives less direct treatment in the
literature. The Corpus Adapter (§4.5) is our answer to this semantic gap: con-
strained selection from a configuration artefact in place of either fine-tuning or
open generation. §6.4 reports a head-to-head comparison against top-K RAG
                                                                PolicyKG        5

on the ontology property list, showing that RAG closes most of the vocabulary-
alignment gap; the Corpus Adapter’s remaining advantage is in deployment prop-
erties (no embedding dependency, deterministic, config-swappable) rather than
raw accuracy.

2.5   Positioning
The gap PolicyKG addresses sits at the intersection of these four threads: an
empirically validated, end-to-end pipeline that combines (a) LLM-based rule
identification and formalisation, (b) FOL+deontic semantics with an empirical
audit-finding of sufficiency on a real institutional corpus (a lower bound, not
a proof), (c) SHACL as the operational compliance target, and (d) a portable
vocabulary-grounding mechanism that mediates between LLM-natural predi-
cates and target ontologies. No prior system unifies these four components, and
no prior empirical work has audited the FOL-sufficiency question on a real cor-
pus.


3     Preliminaries
3.1   First-Order Deontic Logic
We work in first-order logic extended with three deontic modal operators. The
syntax assumes constants, predicates of arity one or more, the quantifiers ∀
and ∃, the connectives ∧, ∨, →, ¬, and three modal operators applied to closed
formulae: O(φ) asserts that φ is obligatory; P (φ) that φ is permitted; and F (φ)
that φ is forbidden, with F (φ) ≡ O(¬φ). We adopt the Standard Deontic Logic
axioms [17], in particular O(φ) → P (φ), which captures the intuition that what is
required is implicitly allowed. As a worked example, the policy sentence “Students
must register before classes begin” admits the formalisation
                                                                  
                ∀x Student(x) → O(RegisterBefore(x, Classes)) .                (1)

Equation 1 is the canonical pattern for a universally quantified obligation; per-
missions replace O with P and prohibitions replace O with F .

3.2   SHACL in One Page
SHACL constraints validate RDF [5] graphs. A NodeShape targets a class
via sh:targetClass and bundles a list of property shapes; a PropertyShape
constrains a specific predicate path (sh:path) with cardinality (sh:minCount,
sh:maxCount), value-type, or pattern restrictions. Violations are reported at
a configurable severity (sh:Violation, sh:Warning, or sh:Info). Equation 1
translates to the SHACL fragment shown below:
ex:StudentRegShape a sh:NodeShape ;
  sh:targetClass ex:Student ;
6       P. Kaewsawee et al.

    deontic:type deontic:obligation ;
    sh:severity sh:Violation ;
    rdfs:comment "Students must register before classes begin." ;
    sh:property [
      sh:path ex:registerBefore ;
      sh:minCount 1
    ] .
The custom deontic:type annotation preserves modal information that would
otherwise be lost in pure SHACL, and rdfs:comment carries the original NL rule
for audit. The sh:Violation severity makes a missing ex:registerBefore link
surface as a compliance failure; a permission would instead emit an Info-level
shape, and a prohibition uses sh:maxCount 0 on the forbidden property.

3.3   The Translation Gap
A naive approach, prompting an LLM to emit SHACL directly from policy text,
fails systematically along three axes. First, vocabulary hallucination: the LLM
invents property names that do not exist in the institutional ontology, so the gen-
erated shapes do not target any real data. Second, lost deontic semantics: the dis-
tinction between obligation, permission, and prohibition collapses into uniform
constraint phrasing when severity assignment is left implicit. Third, predicate-
quality drift: across re-runs the LLM produces structurally similar but lexically
divergent predicates, defeating reproducibility. These three failure modes moti-
vate the two main design choices of PolicyKG: (i) an FOL+deontic intermediate
layer that makes modality explicit and reviewable, and (ii) the Corpus Adapter
(§4.5) that grounds vocabulary in the target ontology.

4     The PolicyKG Pipeline
4.1   Architecture Overview
PolicyKG is structured as four sequential stages (Fig. 1): Stage 1 normalises a
policy PDF into sentences; Stage 2 classifies each sentence as one of {Obliga-
tion, Permission, Prohibition, Non-rule}; Stage 3 lifts each classified rule to an
FOL+deontic formula with top-level operator ∈ {O, P, F }; Stage 4 maps each
formula to a SHACL shape whose severity reflects deontic modality. The four
stages are orchestrated as a hybrid ReAct + Plan-and-Execute agentic architec-
ture on a LangGraph state machine: plan-and-execute fixes the stage sequence
for auditability; ReAct loops inside each stage handle retry, with per-stage val-
idators routing failed items back upstream with a corrective sub-prompt.

4.2   Stage 1: Document Processing
Policy PDFs are extracted with pdfplumber (headers, footers, and page numbers
stripped) and segmented by a policy-aware regex splitter that handles list mark-
ers, soft line-wraps, and semicolon-introduced clauses common in institutional
                                                                                                         PolicyKG           7

                                                   LangGraph plan-and-execute


  Policy          Stage 1     1,663 sent.      Stage 2       443 rules    Stage 3      O/P  /F
                                                                                        repair      Stage 4         SHACL
  PDFs            Extract                      Classify                  FOL+Deontic                 SHACL           KG
                            retry on failure



                                                                                                         inject



                                                                                                 Corpus Adapter
                                                                                                 (YAML registry)



Fig. 1. PolicyKG pipeline. Four sequential stages (Stage 1–4, blue) are orchestrated
by a LangGraph plan-and-execute layer that fixes the stage sequence for auditability;
dashed red arrows show ReAct retry loops where per-stage validators route failed items
back upstream with a corrective sub-prompt. The Corpus Adapter (yellow) is a YAML
registry injected at Stage 4 only; retargeting to a new domain (§6.4) swaps this registry
with no other pipeline change.


P&Ps. A conservative simplification pass removes spurious mid-sentence line
breaks and normalises whitespace; modal verbs, quantifiers, and word order are
never altered. Semantic preservation is dual-checked by an LLM self-assessment
field and Sentence-BERT cosine similarity (threshold ≥ 0.85 accepts 97.9% of
rules). A one-to-one trace from each simplified sentence to its source PDF span
is preserved for audit. From the five AIT P&P documents (81 pages), Stage 1
yields 1,663 normalised sentences.


4.3        Stages 2 and 3: Classification and FOL+Deontic Formalisation
Stage 2 uses a zero-shot prompt listing the four target labels with short pro-
totype examples and asks the LLM for a single label and a confidence score
on [0, 1], identical across all evaluated models. The classifier is deliberately lib-
eral; a downstream check in Stage 3 rejects any admitted sentence that fails to
yield a well-formed deontic formula. Stage 3 lifts each classified sentence into a
first-order formula with exactly one top-level operator from {O, P, F } and the
modal-cue mappings (must, shall → O; may → P ; must not, shall not → F );
the prompt embeds three demonstrations and constrains generation to a struc-
tured JSON schema, addressing the constrained-decoding requirement that has
emerged as a standard remedy for LLM hallucination. We deliberately do not
pass the Corpus Adapter vocabulary at this stage; it is confined to Stage 4 so
that Stage 3 produces a representation whose predicate names are LLM-natural
and human-readable, decoupling deontic structure from vocabulary alignment.
Each formula is validated for well-formedness; a rejected formula is retried once
with the validator’s diagnostic appended.


4.4        Stage 4: SHACL Translation
Translation from FOL to SHACL is rule-driven rather than LLM-driven, be-
cause the mapping is structurally regular and we want auditable outputs. The
universal-obligation pattern ∀x (C(x) → O(P (x, v))) becomes a NodeShape for
8         P. Kaewsawee et al.


       NL rule                      FOL+deontic         SHACL shape
    O All students must pay         ∀x. Student(x) →    NodeShape(Student) +
      tuition fees before each      O(payFee(x))        Property(payFee,
      semester.                                         minCount=1,
                                                        sh:Violation)
    P Students may reside           ∀x. Student(x) →    NodeShape(Student) +
      off-campus from the           P (offCampus(x))    Property(offCampus,
      second semester.                                  sh:Info)
    F Students must not deface      ∀x. Student(x) →    NodeShape(Student) +
      or vandalise library books.   F (deface(x))       Property(deface,
                                                        maxCount=0,
                                                        sh:Violation)

Fig. 2. NL→FOL→SHACL trace for the three deontic operators. Stage 4’s deterministic
mapping fixes the SHACL severity and cardinality.


C and a PropertyShape for P , with sh:minCount 1 and severity sh:Violation.
Permissions P (φ) become Info-level shapes that surface allowed-but-not-required
patterns. Prohibitions F (φ) use sh:maxCount 0 with severity sh:Violation,
while existential obligations use sh:qualifiedValueShape. Predicates emitted
by Stage 3 are resolved against the Corpus Adapter’s vocabulary registry at this
point (this is where vocabulary grounding takes effect), and any unresolved pred-
icate triggers a single repair pass through Stage 3 with the adapter’s constrained
vocabulary fragment in-prompt.
    Institutional policy contains conditional exceptions (“the Registrar may
waive the prerequisite in cases of documented hardship”) that Standard Deontic
Logic [17] handles only awkwardly; the Chisholm and Ross paradoxes are the
canonical symptoms. Stage 4 records these as an explicit deontic:overrides
relation between shapes rather than flattening the exception into a boolean
predicate; the resulting ait:Rule_A deontic:overrides ait:Rule_B triples
are first-class shape metadata that a downstream defeasible-reasoning layer [9]
can consume. In the AIT corpus 12 override relations are emitted (§6.3); a full
defeasible extension is deferred to future work (§8).


4.5     The Corpus Adapter
The Corpus Adapter is a thin, configuration-driven layer with three parts: (i) a
vocabulary registry declaratively enumerating the classes, properties, and syn-
onyms drawn from the target ontology; (ii) a constrained-selection prompt at
Stage 4 that injects the registry and reframes predicate emission as selection
rather than open generation; and (iii) a post-hoc canonicaliser that maps any
free-form predicate the LLM still emits onto its registry match via normalisation
plus fuzzy fallback, triggering a Stage 3 repair on reject. Retargeting PolicyKG
to a new domain means writing a new registry; nothing else changes (Fig. 3).
§6.4 shows that swapping AIT for a GDPR registry raises exact property-name
                                                                                  PolicyKG             9

        Vocabulary registry
(YAML: classes, properties, synonyms)
                                                inject


           FOL predicates               Constrained selection       Post-hoc            SHACL paths
          (Stage 3 output)                prompt to LLM           canonicaliser      aligned to ontology


                                        reject → Stage 3 repair




Fig. 3. The Corpus Adapter is a thin three-part layer between Stage 3 (FOL formal-
isation) and Stage 4’s SHACL emission: a YAML vocabulary registry, a constrained-
selection prompt that converts open predicate generation into closed-set selection, and
a post-hoc canonicaliser with a reject path that triggers a Stage 3 repair. Retargeting
to a new domain swaps only the registry.


matching on 15 hand-curated GDPR rules from 1/15 to 11/15 (Fisher’s exact p
< .001; Cohen’s h = 1.53).


5     Experimental Setup
5.1    D1 Corpus and Gold Standard
Our primary evaluation corpus D1 is built from five AIT Policies & Procedures
documents (81 pages, spanning credit/financial, accommodation, grievance,
ethics, and general-conduct domains). Stage 1 extracts 1,663 sentences; a
deontic-marker prefilter retains 461 candidates; Stage 2 yields 443 classified
rules. The gold standard is built in two passes: Pass 1 labels every sentence
(primary annotator); Pass 2 has two additional annotators (Kittipat, with a
Law / Legal Studies background; Mayuree, with a Linguistics background)
independently re-annotate a stratified 50-item sample (28 O / 12 P / 10 F) blind
to model outputs. The IRR sample yields Fleiss’ κ = .844 (“almost perfect”;
10,000-iteration item-level bootstrap 95% CI [.673, .967]), with pairwise Cohen’s
κ values of .833 (author vs. Kittipat), .868 (author vs. Mayuree), and .832
(Kittipat vs. Mayuree). The wide CI reflects the modest N = 50; the lower
bound remains in the substantial-agreement range. A post-hoc disagreement
audit reclassified 12 systematically mislabelled permissions (10 epistemic “may”
/ obligation-capping cases reclassified as obligations; 2 “may not” constructions
reclassified as prohibitions); the corrections are codified deterministically in a
correction script released with the artifact bundle (§8) and yield the final dis-
tribution: 308 obligations (69.5%), 75 permissions (16.9%), and 60 prohibitions
(13.5%).


5.2    External Datasets

Two additional corpora support external validation. D2, LexDeMod (200 lease-
contract clauses, EMNLP 2022) provides labelled deontic rules drawn from legal
10      P. Kaewsawee et al.

documents and lets us compare PolicyKG’s classifier against a published bench-
mark outside the institutional sub-domain. D3, the GDPR portability set, com-
prises 15 rule-bearing sentences extracted from the GDPR with hand-curated
property targets in the data privacy vocabulary; it supports the cross-domain
transfer experiment (§6.4). For D3 we extract and simplify the GDPR text us-
ing the same Stage 1 pipeline as for AIT, then load a GDPR-specific vocabulary
registry into the Corpus Adapter while holding every other pipeline component
fixed. D3 is intentionally small: the experiment is designed to isolate the registry-
swap effect on vocabulary alignment, not to evaluate full GDPR coverage.

5.3   Model and Decoding
All LLM calls in PolicyKG use Mistral 7B Instruct [12], served locally by Ollama
(v0.15.2+) on an NVIDIA A100 (40 GB) host with near-deterministic decod-
ing (temperature = 0.1, fixed seed, 2,048 max output tokens, 120-second time-
out). No fine-tuning is performed; all classification and formalisation is zero-shot.
Mistral was selected from a five-model pilot (3.8–70 B parameters) against the
majority-vote human gold on the IRR sample (N = 50); Mistral and Gemma 3
4B led at 88% agreement with gold, ahead of Qwen 3 8B (84%), Phi-4 mini
(82%), and Llama 3.1 8B (76%); Fleiss’ κ = .635 (substantial) across all five
LLMs plus the human gold. Mistral is chosen for zero parse-error rate and in-
ference stability, not for the highest single-metric score; full per-item data is
released with the artifacts.

5.4   Evaluation Metrics
Five metrics anchor the evaluation: M1 binary rule detection and M2 deontic-
type accuracy (RQ1, §6.1); M3 FOL semantic predicate quality (RQ2, §6.2);
M4 SHACL shape correctness against an ontology-grounded reference set (RQ3,
§6.3); and M5 output stability under fixed-seed runs (§6.6). We use the term
ontology-grounded reference set rather than “gold-standard SHACL” because the
reference set, the institutional ontology, and the generated shapes were all pro-
duced within the same project; a fully-independent blind gold standard is not
claimed. Statistical claims use 10,000-iteration bootstrap with item-level resam-
pling; proportion CIs use Wilson scores; agreement is reported as Cohen’s κ for
pairs and Fleiss’ κ for pools, with the Landis–Koch interpretation [14]; propor-
tion CIs use the Wilson score. Classification is compared against a hand-tuned
regex baseline; effect sizes (Cohen’s h, risk differences) accompany p-values. A fu-
ture encoder-based baseline on a legal-domain BERT is sketched in the runbook
released with the artifacts.

Reproducibility. All numbers in this paper correspond to repository commit
546dee6f at pipeline version 2.1-final-defense with Ollama model digest
6577803aa9a0 (Mistral 7B Instruct) and random seed 42; all four values are
recorded in the released pipeline_report.json. Evaluation uses fixed seed and
pinned model tags; the gold standard, both Corpus Adapter registries, and the
                                                                  PolicyKG       11

full LangGraph pipeline configuration are released alongside the paper. Repeated
runs produce hash-identical SHACL outputs across all 443 shapes (§6.6); the
determinism boundary is same host, same Ollama version, same model digest,
verified across three independent runs on the reported A100 host. Independent
verification on a different GPU architecture (consumer NVIDIA RTX 4060, Ada
Lovelace; A100 is Ampere) with the identical seed, commit, and model digest
produces counts within ±2 pp of the reported values (FOL success 360/443
vs. 351/443; SHACL valid 403/443 vs. 401/443), attributable to floating-point
kernel differences across GPU architectures under near-deterministic decoding
(§5.5). We do not claim cross-host determinism, and the fixed seed together
with temperature = 0.1 is the pragmatic tightest-reachable configuration under
Ollama; the residual stochasticity is dominated by kernel-level numerical non-
determinism rather than sampling.

5.5   Operational Profile
Reference results in §6 were produced on an NVIDIA A100 (40 GB) host at the
AIT Brain Lab (Acknowledgements). To characterise the pipeline’s deployment
cost on commodity hardware, we also profile a full end-to-end run on a consumer
NVIDIA RTX 4060 (8 GB VRAM, Ada Lovelace architecture, 115 W TGP).
The pipeline processes 1,663 sentences → 443 classified rules in 34.9 minutes
wall-clock (4.73 s per rule, 1.26 s per sentence), sustaining mean GPU utilisation
93.7% (95th percentile 100%), peak VRAM 5.8 GiB, and total end-to-end energy
0.042 kWh (mean power 72.5 W). Estimated token throughput is 2.53 M tokens
per corpus (2.20 M input, 0.33 M output), or approximately 5,700 tokens per
classified rule. If the same workload were re-implemented against a commodity
LLM API at 2026 rates rather than the local Mistral 7B stack, the estimated
per-corpus cost would be approximately $8.78 (GPT-4o), $0.53 (GPT-4o mini),
$11.53 (Claude Sonnet 4), or $2.27 (Llama-3.1-70B via Fireworks). The pipeline
therefore fits within an 8 GB consumer-GPU envelope; on the A100 reference
host, wall-clock is expected to be substantially lower due to higher memory
bandwidth and tensor-core throughput, but was not instrumented with the same
profiler at the time of the reference run. Cross-hardware output drift is quantified
in the Reproducibility paragraph above.


6     Results
Table 1 summarises headline numbers across the three research questions; each
row is unpacked in the subsections that follow.

6.1   RQ1: LLM Deontic Classification
On the full D1 corpus (N = 443 rules), Mistral 7B Instruct (selected from a
pilot comparison across 3–70 B instruction-tuned models for its zero parse-error
rate and inference efficiency, not for the highest raw accuracy) achieves 86.9%
12      P. Kaewsawee et al.

Table 1. Headline results across the three research questions on the AIT D1 corpus,
with the cross-domain transfer experiment on GDPR (§6.4).

RQ Metric                                              Value                           Section
RQ1 Binary rule detection (M1, F 1 )                    .963 (acc. .938; κ = .764)     6.1
RQ1 Deontic-type accuracy on D1 (M2)                    86.9% (κ = .709)               6.1
RQ1 Deontic-type accuracy on IRR sample (M2)            84.0% (42/50)                  6.1
RQ2 End-to-end FOL formalisation yield                  79.2% (351/443)                6.2
RQ2 FOL predicate quality (conditional, M3)             100% (351/351)                 6.2
RQ2 SOL/HOL constructs (two-pass audit: regex + manual) 0 / 443 (95% upper CI 0.67%)   6.2
RQ3 SHACL shape correctness (M4, F 1 )                  .866 (69-shape subset)         6.3
— GDPR cross-domain exact alignment                     1/15 → 11/15 (Fisher p < .001) 6.4
— Output stability (M5, repeated runs)                  hash-identical                 6.6




deontic-type accuracy with Cohen’s κ = .709 (“substantial agreement”)
and Macro F 1 = .810, above the 75–85% range reported for prior rule-based and
classifier-based approaches [16,3]. Per-class F 1 is .915 for obligations (290/308
correct), .784 for permissions (49/75), and .730 for prohibitions (46/60). The
class-specific weakness is recall on permissions (65.3%): 22 of 75 permission rules
are reclassified as obligations, reflecting the well-known epistemic-versus-deontic
“may” ambiguity in modal semantics. On the three-annotator IRR sample (N =
50), the same model labels 42/50 sentences in agreement with the majority-vote
human gold (κ = .629); the human-only Fleiss’ κ on the same sample is .844,
so the model is within reach of the inter-human ceiling on accuracy. Binary rule
detection (rule vs. non-rule) reaches F 1 = .963 at 93.81% accuracy with κ =
.764, against the hand-tuned regex baseline at F 1 = .898 (+.065 F 1 ; Cohen’s h
≈ 0.34, small-to-medium effect).

Learned in-domain baseline. A NumPy-only multinomial logistic regression on
TF bag-of-words plus six deontic-marker features, stratified 5-fold CV on the
same 443 rules, reaches accuracy 90.3% / κ = .799 / Macro F 1 = .863 (script
and per-class output in the released artifacts). This learned baseline outperforms
the zero-shot LLM on D1, as it should: it consumes in-domain labels the LLM
does not see. The LLM’s value is the zero-shot property: no labelled D1 training
data is required to deploy the pipeline on a new institution. The cross-domain
LexDeMod result (§6.6) bounds this claim and motivates the Corpus Adapter
as the mechanism for repairing deontic-cue grounding under domain shift.

Head-to-head open-model comparison (N = 50). To test whether the choice of
Mistral 7B versus a newer open-weight model materially affects classifier accu-
racy, we re-ran the identical zero-shot prompt under identical near-greedy decod-
ing (temperature = 0.1, seed = 42) against three alternative 7–9 B open models
available in mid-2026: Qwen 2.5 7B, Llama 3.1 8B, and Gemma 2 9B. Table 2
summarises results on the D3 IRR sample. Llama 3.1 8B and Gemma 2 9B both
reach 88% accuracy, 4 pp above Mistral, but the difference is not statistically
significant by exact McNemar test (Llama p = .77; Gemma p = .69); the com-
parison is under-powered at N = 50 but rules out large-effect differences among
                                                                      PolicyKG        13

Table 2. Head-to-head open-model comparison on the D3 IRR sample (N = 50) under
identical zero-shot prompt and near-greedy decoding. Accuracy CIs are Wilson 95%
intervals. McNemar p-values are exact two-sided against the Mistral baseline; none
reaches p < .05 at this sample size, so the comparison rules out large-effect differences
but cannot certify small-effect ordering. Full per-class breakdowns are in the artifact
bundle (§8).

       Model                    Accuracy (95% CI)     κ     Macro F1 McNemar p
       Mistral 7B (reference)     .84   [.71, .92]   .629     .612        —
       Qwen 2.5 7B                .80   [.67, .89]   .631     .709       .77
       Llama 3.1 8B               .88   [.76, .94]   .768     .832       .77
       Gemma 2 9B                 .88   [.76, .94]   .750     .714       .69



the four models. The most informative per-class effect is on the non-deontic class
(support 5): Mistral misses all five items (F 1 = 0), whereas Llama 3.1 8B re-
covers all five at F 1 = .71, driving its Macro F 1 to .832 (vs. Mistral’s .612 on
the same 4-class sample). Mistral remains the reference model for the paper’s re-
ported results on the strength of its zero parse-error rate and inference stability,
but readers seeking stronger non-deontic filtering can substitute Llama 3.1 8B
via the released baseline harness without any other pipeline change.


6.2   RQ2: First-Order Logic Sufficiency
The audit finding is clean: a two-pass audit of all 443 D1 rules (an au-
tomated regex checklist plus a first-author manual review of the 92
FOL-fallback cases) matched zero second-order or higher-order con-
struct patterns. The regex checklist scans both the natural-language source
text and any generated FOL formula for six canonical SOL/HOL signatures:
predicate quantification, set quantification, function variables, lambda expres-
sions, recursive / transitive-closure definitions, and meta-policy quantification.
The manual pass targets the 92 fallback rules specifically because these are the
cases where an HOL requirement could otherwise hide behind an LLM parse
failure: the automated checklist scores those rules as “no HOL pattern found”
by default when Stage 3 emits natural text instead of a formula, so their ex-
pressiveness cannot be adjudicated without a human read. The manual review
confirmed that every one of the 92 fallbacks is expressible in FOL and that the
failures are attributable to LLM engineering limits (long compound sentences,
embedded bullets, multiple negations) rather than expressiveness requirements.
    Given 0 confirmed HOL cases in an audit sample of 443 rules, the exact
one-sided Clopper–Pearson upper 95% CI on the true HOL requirement rate
for this corpus is 1 − 0.051/443 ≈ 0.67%. We report this as an audit finding
for this corpus, not a mathematical proof of FOL sufficiency for institutional
policies in general: a rule may carry a higher-order interpretation that does not
surface in any of the six regex signatures and is not obvious to a human reviewer,
so the audit is a lower bound on FOL adequacy, not an upper bound. To our
14      P. Kaewsawee et al.

knowledge this is the first empirical audit of this question on a real institutional
corpus, complementing the theoretical sufficiency arguments of Governatori and
Rotolo [10].
     Per-pattern matches across all 443 rules: predicate quantification 0; set quan-
tification / comprehension 0; function variables 0; lambda expressions 0; recur-
sive / transitive-closure 0; meta-policy quantification 0. The audit script, regex
definitions, and per-rule manual-audit CSV are released with the artifact bundle
(§8).
     End-to-end pipeline yield (a syntactically well-formed FOL formula passing
Stage 3 validation) is 79.2% (351/443). Across the 351 well-formed formulae, M3
semantic predicate quality is 100% after a retry-and-backfill mechanism that re-
invokes the LLM on placeholder predicates; we report M3 both conditionally
(351/351) and unconditionally (351/443). Of the 92 fallback rules, 77.2% fall
into four structural categories: compound and/or-joined (28), very long (14),
multi-clause complex (14), and bulleted compound (10). The remainder falls
into miscellaneous parser/formatting failures (23) and edge cases with multiple
modal operators or negations (3); zero fallbacks are attributed to higher-order
construct requirements. Per-category data is released with the artifact bundle;
all fallbacks are recovered via Stage 4’s direct NL→SHACL path.

6.3   RQ3: SHACL Translation Quality
We report shape correctness at four coverage tiers to avoid the common
pitfall of headlining a single F1 over a small subset: T1 syntactic validity
(401/443 = 90.5% on the full corpus, Wilson 95% CI [.87, .93]); T2 structural
correctness (351/351 = 100% on the FOL-mediated subset; the deterministic
Stage 4 template guarantees the ceiling); T3 deontic-severity match against
gold (330/351 = 94.0%, [.91, .96]); and T4 behavioural M4 F 1 against Pos/Neg
entities (69-shape subset, F 1 = .866, [.79, .93]). Tier T4 is the headline:
    The headline metric is T4: with the Corpus Adapter enabled, PolicyKG
achieves F 1 = .866 (Precision .977, Recall .778) on the 69-shape subset for
which Pos/Neg test entities exist; full-corpus M4 coverage is an evaluation-
infrastructure limit (test entities for all 443 rules are out of scope for this pa-
per), not a pipeline limit. The end-to-end tiers (T1 at 90.5%, T3 at 94.0%)
confirm that the pipeline’s correctness extends beyond the M4 subset along the
dimensions our artifacts support directly. T2 reaches the ceiling because every
FOL-mediated shape is rule-emitted by Stage 4’s deterministic template (§4).
    A static ablation released with the artifacts isolates the vocabulary-grounding
effect on the 351 FOL-mediated rules: exact vocabulary alignment rises from
174/351 (49.6%) with raw LLM-emitted predicates to 304/351 (86.6%) after
adapter normalisation (+37.0 percentage points). The static comparison brackets
the upper limit of vocabulary normalisation on already-generated artefacts; a
fresh adapter-off LLM run on the full D1 corpus would measure whether the LLM
itself produces vocabulary-aligned predicates when prompted with the hint. A
runbook for that follow-up experiment is released with the artifacts. §6.4 provides
a cleaner adapter on/off contrast under controlled cross-domain conditions.
                                                                  PolicyKG       15

6.4   Cross-Domain Portability (GDPR)
We retarget PolicyKG to GDPR by swapping the AIT registry for a GDPR-
derived registry; models, prompts, FOL grammar, and SHACL translation rules
are unchanged. Exact property-name alignment with the GDPR ontol-
ogy improves from 1/15 (Wilson 95% CI [.01, .30]) without the adapter
to 11/15 ([.48, .89]) with it; risk difference +66.7 percentage points
(Fisher’s exact p < .001; Cohen’s h = 1.53, large effect). We report abso-
lute proportions and effect sizes rather than a fold-change ratio because the latter
is unstable on a denominator of 1. Without vocabulary grounding the LLM emits
English-natural names (e.g. transfersData) that resemble GDPR concepts but
rarely match the canonical ontology forms (e.g. dpv:DataTransfer); with the
adapter the LLM selects from the registry and outputs land on canonical predi-
cates. N = 15 is a proof-of-concept scale appropriate for the architectural-pattern
demonstration; the broader claim, that vocabulary grounding is a portable design
choice for LLM-based knowledge-graph construction, scales beyond the policy
domain.

Comparison to retrieval-augmented generation (RAG). An anticipated reviewer
objection is that the no-grounding baseline is a straw man: retrieval-augmented
generation (RAG) over the ontology is the mainstream 2026 alternative and
would close much of the gap. We therefore ran a controlled three-condition ex-
periment on the same 15 GDPR rules with identical prompt scaffolding: (1) no-
grounding (no candidate list injected), (2) RAG (top-10 ontology properties
retrieved per rule via SentenceBERT all-MiniLM-L6-v2 cosine similarity, in-
jected as the candidate list), and (3) Corpus Adapter (full registry constrained
selection plus post-hoc canonicaliser). Results: no-grounding 0/15; RAG 9/15
(60.0%, +60.0 pp over no-grounding, Cohen’s h = 1.77, Fisher p = .0007); Cor-
pus Adapter 11/15 (73.3%, +13.3 pp over RAG, Cohen’s h = 0.28, Fisher p =
.70, not statistically significant at N = 15 ). The honest reading is that RAG
closes most of the accuracy gap (60 pp of the 73 pp total); the Corpus
Adapter’s incremental accuracy gain over RAG is small on this sample and can-
not be certified at p < .05. The Corpus Adapter’s remaining advantage is instead
in deployment properties rather than raw accuracy: the vocabulary registry is a
static YAML artefact (no embedding-model dependency at inference time, no
top-K tuning, byte-level determinism across runs), it is human-auditable, and
retargeting to a new domain is a config-file swap rather than a re-embedding
pass. Per-item analysis of the six RAG misses attributes two to formatting
drift (e.g. providesPrivacyNotice vs. providePrivacyNotice) that the Cor-
pus Adapter’s post-hoc canonicaliser recovers, three to top-K retrieval misses
that a full-registry constrained-selection prompt avoids by construction, and one
to a genuine semantic near-miss that neither approach resolves.

6.5   Component Ablations
The pipeline stacks six sub-components on top of the four core stages: a heuristic
pre-filter that admits deontic-marker candidates (§4), prefilter hints injected into
16      P. Kaewsawee et al.

Table 3. Component ablations on the AIT corpus. Each row disables one pipeline
component; all others are held fixed. LLM–regex agreement is a consistency proxy
against a deterministic regex classifier (the paper’s original baseline of §6.1); it is not
accuracy against gold because gold labels are baseline-specific and cannot be joined
to ablation runs whose rule sets differ. Time is end-to-end wall-clock on the consumer
profile host (§5.5).

         Ablation           N rules LLM–regex agr.        κ Macro F1 Wall time
         baseline              443            82.6% .637        .748 34.9 min
         no-prefilter           —       timed out > 2 h (evidence in itself )
         no-hints              442            83.0% .645        .750     95 min
         no-reclassify         445            82.5% .632        .745     47 min
         no-fallback           445            82.5% .632        .745     36 min
         no-fol-retry          445            82.5% .632        .745     36 min
         no-may-disambig       499           78.4% .592        .709      52 min



the Stage 2 classifier prompt, a Stage 2 reclassify second-opinion pass, a Stage 3
FOL retry loop on placeholder rejection, a Stage 4 NL→SHACL fallback for
FOL-refused rules, and a “may” disambiguation filter that separates epistemic
uncertainty from deontic permission. We disable each in turn and compare the
resulting classified rule set against the baseline.
    Table 3 separates the six components into three buckets. Structurally nec-
essary components are the pre-filter, the “may” disambiguation filter, and the
NL→SHACL fallback: the pre-filter is required for throughput (all 1,663 sen-
tences reach the classifier without it, and a 2-hour budget expires before the
run completes); disabling “may” disambiguation admits 56 additional candidates
but LLM–regex agreement drops 4.2 pp, indicating that most of the extra ad-
mits are epistemic “may” constructions rather than genuine deontic permissions;
and disabling the NL fallback drops 82 rules from the final shape set (18.5%
coverage loss), because those rules never yield a well-formed FOL formula. Em-
pirically marginal components on this metric are prefilter hints, the reclassify
second-opinion pass, and the FOL retry loop: all three show swings smaller
than the natural rule-count variation between runs (±3 rules, agreement within
±0.5 pp). We report this honestly rather than pruning the null results: the com-
ponents may still be justified by orthogonal considerations (retry catches rare
LLM parse failures that never surface at this metric, second-opinion addresses
tail-risk classifications that only appear in adversarial inputs) but do not carry
weight on classification consistency. The no-prefilter timeout is a design-defence
result in its own right: the four-stage pipeline is not compute-tractable at corpus
scale without the pre-filter, even on the near-8 GB consumer GPU that hosts
the profile in §5.5. Full per-ablation JSON summaries are released in the artifact
bundle (§8); the sweep script is evaluation/full_ablation_sweep.py.
                                                                   PolicyKG       17

6.6   Output Stability and External Validation
Stability (M5). Repeated pipeline runs with fixed seed and pinned model tags
produce SHACL outputs hash-identical to the first run across all 443 shapes. This
determinism is a prerequisite for deployments that need an audit trail tying a
compliance check back to a specific policy interpretation.

LexDeMod external validation. On the LexDeMod [21] benchmark (D2: 200
lease-contract clauses) the same classifier drops from D1’s Macro F 1 = .810
to Macro F 1 = .370 (obligation F 1 = .569; permission F 1 = .038). The fail-
ure has a diagnosable mechanism: lease contracts express permission as “Tenant
shall be entitled to . . . ”, whose obligation-style “shall” cue dominates the LLM’s
prompted heuristic, causing permissions to be absorbed into the obligation class.
This is a vocabulary-prior mismatch, not an expressiveness or reasoning failure,
and it is precisely the class of failure the Corpus Adapter is designed to ad-
dress by registry swap. Building a lease-contract deontic-cue registry (analogous
to the AIT-vs-GDPR comparison in §6.4) is the natural next experiment; the
present LexDeMod number is the zero-shot lower bound against which any fu-
ture adapter-on number must be compared. The boundary is consistent with
our positioning: PolicyKG claims institutional sufficiency, not universal legal
coverage, and a controlled cross-domain test under registry control is the GDPR
experiment in §6.4.


7     Discussion
7.1   What Was Surprising
Three results ran against our prior expectations and deserve explicit comment.
    The learned baseline beat the zero-shot LLM in-domain but not out-of-
domain. A NumPy-only multinomial logistic regression on TF bag-of-words plus
six deontic-marker features reaches Macro F 1 = .863 under 5-fold CV on D1,
above the LLM’s zero-shot .810. We had assumed the reverse: a general-purpose
7B-parameter model exposed to trillions of tokens should beat a NumPy
classifier trained on a few hundred sentences. On LexDeMod, however, the
ordering flips into a tie: the same LR under 5-fold CV (N = 200) yields Macro
F 1 = .360 against the LLM’s .370. The interpretation is that the LR was not
learning “deontic logic”; it was learning the AIT-specific vocabulary distribution.
When that distribution shifts to lease-contract English, the LR’s implicit prior
evaporates and the LLM’s broader lexical coverage catches up. This is a warning
against reading in-domain baseline superiority as evidence of generalisation; the
opposite conclusion may be closer to the truth.
    The permission-class collapse on LexDeMod (F1 = .038) was larger than
any effect we anticipated. The mechanism is diagnosable and mundane: lease
contracts express permission through the phrase “Tenant shall be entitled to . . . ”,
whose “shall” cue the LLM has learned to read as an obligation marker. Nearly
every permission is absorbed into the obligation class. This is not a reasoning
18      P. Kaewsawee et al.

failure and not an expressiveness failure; it is a vocabulary-prior mismatch, and it
is precisely the failure mode the Corpus Adapter is designed to address at Stage 4.
It also suggests, more broadly, that headline LLM performance on any deontic-
classification benchmark should be reported against the lexical distribution of
the target corpus, not against a single macro average.
    The 0/443 SOL/HOL audit finding was cleaner than we expected. Going in,
we assumed a small residue of quantifier-over-rule or predicate-over-predicate
cases would surface in eligibility criteria or waiver clauses. None did. Even the six
“exceptional” rules that looked meta-policy on first read, such as “the Registrar
may waive the prerequisite in cases of documented hardship,” resolved to first-
order predicates over an unquantified exception set. We report this as a lower-
bound audit finding rather than a proof, but the null result is worth flagging: the
institutional-policy sub-domain may be a less demanding target for formal-logic
infrastructure than the theoretical literature has assumed.

7.2   Comparison to Prior Work

On the deontic-classification task, PolicyKG’s 86.9% D1 accuracy sits above the
75–85% range reported by pattern-based systems (Maxwell and Antón’s rule-
model work at approximately 77% [16], Brodie et al.’s SPARCLE-based SVM at
82% on privacy policies [3]) and near PAPEL’s 80% F 1 on clause labelling with
chain-of-thought prompting [8]. These are not head-to-head comparisons: each
system targets a different corpus and a slightly different label set, so the accuracy
delta is a directional indicator rather than a benchmark win. The substantive
advance is not the accuracy number; it is the pipeline structure. Prior LLM-for-
legal work (LexGLUE [4], LegalBench [11], PAPEL [8]) delivers labels or spans;
PolicyKG delivers executable SHACL shapes with an audit trail from a sentence
to its formula to its shape. The chain is what enables downstream compliance
checking rather than downstream annotation.
    On the FOL-sufficiency question, our contribution is a resolution level, not
a direction. Governatori and Rotolo [10] argued for FOL adequacy on theoreti-
cal grounds; Brachman and Levesque [2] framed the expressiveness-tractability
trade-off. Neither line had been tested against a real institutional corpus at scale.
Our 0/443 checklist audit provides that empirical anchor. It confirms rather than
contradicts the theoretical argument, but it turns an “it should suffice” into “on
this corpus it did suffice.” That is a smaller but different type of claim.
    On vocabulary grounding, the Corpus Adapter sits alongside constrained-
decoding work (Willard and Louf’s Outlines [23], Geng et al.’s grammar-
constrained decoding [7]) but operates at a different abstraction level. Those
approaches constrain syntax at the token level; the Corpus Adapter constrains
vocabulary at the predicate level, via a runtime-editable registry rather than a
compiled grammar. The two are compositional and the extended journal version
will report a stacked ablation.
                                                                PolicyKG       19

7.3   Experimental Decisions Worth Revisiting
Three experimental decisions traded ambition for tractability, and a reviewer
would be right to press on each.
    Zero-shot only for the main LLM. We ran the classification and formalisa-
tion stages zero-shot to isolate the pipeline’s architectural contribution from
prompt-engineering gains. Few-shot with representative in-context exemplars
would plausibly close much of the gap to the LR baseline on D1, but it would
also introduce a selection-bias question (which exemplars, drawn from what dis-
tribution?) that we chose not to entangle with the primary claim. The extended
version will report a matched few-shot condition.
    N = 15 for the GDPR transfer experiment. The N was sized to isolate the
registry-swap effect on a hand-curated, ontology-anchored rule set, not to certify
GDPR coverage. Under a denominator of 1 in the no-adapter condition, the
fold-change ratio is undefined and the Wilson CI is wide; we accordingly report
absolute proportions, risk difference, and Cohen’s h = 1.53 rather than a ratio.
The Fisher’s exact p < .001 remains valid at this N and the effect size is large
enough that a bigger sample is unlikely to reverse the sign, but a 100+ rule set
drawn from the full GDPR would strengthen the external-validity argument.
    Single LLM in the main results. Mistral 7B Instruct was selected from a five-
model pilot for zero parse-error rate and inference stability, not for the highest
raw accuracy. Reviewers will reasonably ask whether the Corpus Adapter’s cross-
domain gain is a property of Mistral or a property of the pipeline. The pilot data
on the 50-item IRR sample is consistent across five instruction-tuned models
(Fleiss’ κ = .635 across LLMs plus human gold), but a matched adapter on/off
contrast on Gemma 3, Qwen 3, and a 70B-parameter model is on the roadmap
and will settle the question directly.

7.4   Reconciling the In-Domain and Cross-Domain Stories
Bringing the strands together: when the target domain comes with sufficient
labelled data, a learned baseline is the right tool; when it does not (the stan-
dard deployment scenario for institutional policy formalisation), the LLM-plus-
Corpus-Adapter combination is the only option. An LLM/LR ensemble on D1 is
appealing but undefined off-domain (no training signal), and the Corpus Adapter
is not substitutable into a learned baseline because it constrains predicate gen-
eration (Stage 3–4), not category classification (Stage 2). The two roles are
orthogonal, and the deployment case is the case where only one of the two is
available.

7.5   Deployment: Compliance Dashboard
To demonstrate that the pipeline output is directly consumable by a compliance
workflow rather than only by downstream research, we release a companion
web dashboard (FastAPI backend, HTML/JavaScript frontend; ∼33 KB, in
web/app.py) with the artifact bundle. The dashboard loads the pipeline’s
20      P. Kaewsawee et al.

SHACL shapes and lets a compliance officer (i) browse the 443 classified
rules with filters by deontic type and severity, (ii) inspect each rule’s source
PDF span, generated FOL formula, and emitted SHACL shape side-by-side,
(iii) select individual entities (students, faculty, staff, committees) from a seeded
PostgreSQL demonstration database via db/rdf_converter.py, and (iv) run
pyshacl validation in-browser to surface entity-centric violations with severity
coding and property-level explanations. The 42 syntactically invalid shapes from
the NL-fallback path are automatically skipped at load time. The dashboard is
a compliance-workflow demonstration, not an evaluation artifact; its role in the
paper is to show that the audit-trail requirement (§1) is instantiated end-to-end
from policy PDF to entity-level violation report.


7.6   Limitations
The FOL-sufficiency finding (0 of 443 SOL/HOL matches) is a checklist-based
audit, a lower bound on FOL adequacy scoped to our institutional sub-domain
and to FOL with standard arithmetic/temporal extensions. Beyond that scope,
the evaluation is limited along five axes: single institution (one university; N
= 15 GDPR transfer partly mitigates); English only; declarative rules only (no
procedural workflows or rule-set meta-reasoning); static validation (SHACL pre-
supposes an upstream enforcement layer); reference-set construction (in-house,
so M4 is best read as the F 1 = .000 → .866 adapter delta, not as performance
against an independent gold). LexDeMod permission F 1 = .038 bounds the
zero-shot transfer limit for the permission class and motivates a lease-contract
registry as future adapter demonstration. A representative NL-fallback failure:
the rule “Continuing students may put their names on the waiting list and shall
be served on a queue-numbering basis or, exceptionally, through email to OFAM”
compounds two deontic operators with a nested disjunction that exceeds single-
pass Stage 3 parsing.


8     Conclusion and Future Work
We presented PolicyKG, an agentic LLM pipeline that translates institutional
policy documents into SHACL-validated knowledge graphs via a first-order de-
ontic intermediate layer. The pipeline achieves 86.9% deontic classification ac-
curacy (Fleiss’ κ = .844 inter-annotator, 95% CI [.67, .97]), F 1 = .866 SHACL
shape correctness on a 69-shape evaluation subset, and a two-pass audit (regex
checklist over all 443 rules plus manual review of the 92 FOL-fallback cases)
finding no SOL/HOL constructs across the AIT corpus (exact upper 95% CI
on the true HOL rate: 0.67%). The main technical contribution, the Corpus
Adapter, enables cross-domain transfer: in a controlled GDPR experiment (N
= 15), exact vocabulary alignment rises from 1/15 to 11/15 (Fisher’s exact p <
.001, Cohen’s h = 1.53).
    The broader insight is that for LLM-based knowledge-graph construction, vo-
cabulary grounding via configuration beats free generation. Reframing predicate
                                                                  PolicyKG       21

emission as constrained selection from a registry is cheaper than fine-tuning,
transfers immediately across domains, and leaves an audit trail. The pattern
applies wherever LLMs must emit canonical identifiers from a closed-world on-
tology, from biomedical knowledge graphs to legal taxonomies to schema.org-
grounded extraction. A learned in-domain baseline can exceed the zero-shot LLM
on the source corpus, but only the LLM-plus-adapter combination generalises to
a new corpus without retraining; the extended journal version will report a real
adapter on/off LLM ablation, a LegalBERT fine-tuned baseline, and a scaled
GDPR portability set.

Future work. Four directions extend this work.
    Multi-institutional validation. The 0/443 SOL/HOL audit is scoped to one
university’s policy corpus. A meaningful test of the broader FOL-sufficiency
claim requires replicating the audit across policy corpora from at least three
additional institutions that differ in size, jurisdiction, and academic type (public
research university, private undergraduate college, professional-school setting).
We expect the null result to hold; a single institution that produces even one
SOL/HOL construct would sharpen the architectural claim about where FOL
falls short.
    Defeasible deontic extensions. A subset of institutional rules carry implicit
exceptions (“the Registrar may waive the prerequisite. . . ”) that our current FOL
grammar treats as first-order predicates over an unquantified exception set. A
defeasible deontic layer, following the tradition of Governatori and colleagues [9],
would represent the override relation explicitly, enabling SHACL shapes to en-
code “normally prohibited, but with documented cause” semantics rather than
flatten the exception into a boolean predicate. This is a natural extension be-
cause Stage 3’s structured JSON schema already carries an exception_of field
that is currently unused downstream.
    Agentic SHACL repair. On validation failure, the pipeline currently retries
once with the validator’s diagnostic. A stronger loop would invoke the pipeline in
reverse: an LLM reads the SHACL report, walks back through the FOL formula
to the source sentence, and proposes either a data-side remediation (which entity
attribute is missing) or a shape-side one (which constraint is over-strict). The
auditability of the FOL intermediate is the mechanism that makes this practical:
the LLM has a symbolic anchor to reason over rather than a free-form policy
sentence.
    Scaled and stacked ablations. The extended journal version will report a
matched adapter on/off LLM ablation, a LegalBERT fine-tuned baseline, a
few-shot LLM condition, a 100+-rule GDPR transfer set, and a stacked com-
parison against grammar-constrained decoding to disentangle syntax-level from
vocabulary-level grounding. These are the experiments a reviewer would ask for;
we would rather run them than defend against the ask.

Code and Data Availability. All artifacts referenced in this paper (pipeline
source, AIT and GDPR Corpus Adapter registries, post-audit gold annotations,
the 12-correction script, logic-expressiveness audit, Fleiss-κ bootstrap, multi-tier
22      P. Kaewsawee et al.

shape-correctness evaluation, Corpus Adapter ablations, multi-LLM pilot data,
offline learned baseline, and the frozen output snapshot) are released as a sin-
gle bundle at Zenodo (DOI placeholder pending camera-ready) with a GitHub
mirror.

Acknowledgments. This work was supported by a Royal Thai Government Fellow-
ship. The authors thank the AIT Brain Lab for compute and discussion, and Kittipat
(Law / Legal Studies background) and Mayuree (Linguistics background) for serving
as the two external annotators in the inter-rater reliability study.


References
 1. Athan, T., Boley, H., Governatori, G., Palmirani, M., Paschke, A., Wyner, A.Z.:
    OASIS LegalRuleML. In: Proceedings of the 14th International Conference on
    Artificial Intelligence and Law (ICAIL). pp. 3–12. ACM (2013). https://doi.org/
    10.1145/2514601.2514603
 2. Brachman, R.J., Levesque, H.J.: Knowledge Representation and Reasoning. Mor-
    gan Kaufmann, San Francisco, CA (2004)
 3. Brodie, C.A., Karat, C.M., Karat, J.: An empirical study of natural language pars-
    ing of privacy policy rules using the SPARCLE policy workbench. In: Proceedings
    of the 2nd Symposium on Usable Privacy and Security (SOUPS). pp. 8–19. ACM
    (2006). https://doi.org/10.1145/1143120.1143123
 4. Chalkidis, I., Jana, A., Hartung, D., Bommarito, M., Androutsopoulos, I., Katz,
    D.M., Aletras, N.: LexGLUE: A benchmark dataset for legal language understand-
    ing in English. In: Proceedings of the 60th Annual Meeting of the Association for
    Computational Linguistics (ACL). pp. 4310–4330. Association for Computational
    Linguistics (2022). https://doi.org/10.18653/v1/2022.acl-long.297
 5. Cyganiak, R., Wood, D., Lanthaler, M.: RDF 1.1 concepts and abstract syn-
    tax. W3C Recommendation, 25 February 2014 (2014), https://www.w3.org/TR/
    rdf11-concepts/
 6. Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, A., Truitt, S., Larson,
    J.: From local to global: A graph RAG approach to query-focused summarization.
    CoRR abs/2404.16130 (2024). https://doi.org/10.48550/arXiv.2404.16130
 7. Geng, S., Josifoski, M., Peyrard, M., West, R.: Grammar-constrained decoding for
    structured NLP tasks without finetuning. In: Proceedings of EMNLP 2023. pp.
    10932–10952 (2023). https://doi.org/10.18653/v1/2023.emnlp-main.674
 8. Göknil, A., Gelderblom, F.B., Tverdal, S., Tokas, S., Song, H.: PAPEL: Privacy
    policy analysis through prompt engineering for LLMs. In: Proceedings of the 1st In-
    ternational Conference on Foundation and Large Language Models (FLLM) (2024)
 9. Governatori, G., Olivieri, F., Scannapieco, S., Rotolo, A., Cristani, M.: The Ratio-
    nale behind the concept of goal. Theory and Practice of Logic Programming 16(3),
    296–324 (2016). https://doi.org/10.1017/S1471068416000028
10. Governatori, G., Rotolo, A.: A conceptually rich model of business process compli-
    ance. Conferences in Research and Practice in Information Technology (CRPIT) –
    Conceptual Modelling 110, 3–12 (2010)
11. Guha, N., Nyarko, J., Ho, D.E., Ré, C., Chilton, A., Narayana, A., Chohlas-
    Wood, A., Peters, A., Waldon, B., Rockmore, D., et al.: LegalBench: A collab-
    oratively built benchmark for measuring legal reasoning in large language models.
    In: Advances in Neural Information Processing Systems 36 (NeurIPS) Datasets
    and Benchmarks Track (2023)
                                                                      PolicyKG        23

12. Jiang, A.Q., Sablayrolles, A., Mensch, A., Bamford, C., Chaplot, D.S., de las
    Casas, D., Bressand, F., Lengyel, G., Lample, G., et al.: Mistral 7B. CoRR
    abs/2310.06825 (2023). https://doi.org/10.48550/arXiv.2310.06825
13. Knublauch, H., Kontokostas, D.: Shapes constraint language (SHACL). W3C Rec-
    ommendation, 20 July 2017 (2017), https://www.w3.org/TR/shacl/
14. Landis, J.R., Koch, G.G.: The measurement of observer agreement for categorical
    data. Biometrics 33(1), 159–174 (1977). https://doi.org/10.2307/2529310
15. Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H.,
    Lewis, M., Yih, W.t., Rocktäschel, T., Riedel, S., Kiela, D.: Retrieval-augmented
    generation for knowledge-intensive NLP tasks. In: Advances in Neural Information
    Processing Systems 33 (NeurIPS). pp. 9459–9474 (2020), https://arxiv.org/abs/
    2005.11401
16. Maxwell, J.C., Antón, A.I.: Developing production rule models to aid in acquiring
    requirements from legal texts. In: 17th IEEE International Requirements Engi-
    neering Conference (RE). pp. 101–110. IEEE (2009). https://doi.org/10.1109/RE.
    2009.21
17. McNamara, P.: Deontic logic. In: Zalta, E.N. (ed.) The Stanford Encyclopedia of
    Philosophy. Metaphysics Research Lab, Stanford University (2006), https://plato.
    stanford.edu/entries/logic-deontic/
18. Nute, D.: Defeasible logic. In: Handbook of Logic in Artificial Intelligence and
    Logic Programming, Vol. 3, pp. 353–395. Oxford University Press (1994)
19. Palmirani, M., Governatori, G.: Modelling legal knowledge for GDPR compliance
    checking. In: Legal Knowledge and Information Systems — JURIX 2018. Frontiers
    in Artificial Intelligence and Applications, vol. 313, pp. 101–110. IOS Press (2018).
    https://doi.org/10.3233/978-1-61499-935-5-101
20. Prakken, H., Sartor, G.: Law and logic: A review from an argumentation perspec-
    tive. Artificial Intelligence 227, 214–245 (2015). https://doi.org/10.1016/j.artint.
    2015.06.005
21. Sancheti, A., Garimella, A., Srinivasan, B.V., Rudinger, R.: Agent-specific deontic
    modality detection in legal language. In: Proceedings of EMNLP 2022. pp. 1947–
    1968 (2022). https://doi.org/10.18653/v1/2022.emnlp-main.125
22. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E.H., Le,
    Q.V., Zhou, D.: Chain-of-thought prompting elicits reasoning in large language
    models. In: Advances in Neural Information Processing Systems 35 (NeurIPS)
    (2022), https://arxiv.org/abs/2201.11903
23. Willard, B.T., Louf, R.: Efficient guided generation for large language models.
    arXiv:2307.09702 (2023), https://arxiv.org/abs/2307.09702
