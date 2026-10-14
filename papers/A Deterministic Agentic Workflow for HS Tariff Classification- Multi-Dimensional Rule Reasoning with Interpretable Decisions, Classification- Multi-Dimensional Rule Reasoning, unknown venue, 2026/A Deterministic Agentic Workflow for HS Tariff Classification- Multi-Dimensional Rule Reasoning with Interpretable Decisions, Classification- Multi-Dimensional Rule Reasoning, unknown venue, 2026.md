                                            A Deterministic Agentic Workflow for HS Tariff
                                            Classification: Multi-Dimensional Rule Reasoning
                                                        with Interpretable Decisions
                                                     Yu Zhang∗ , Dongjiang Zhuang¶ , Qu Zhou‡ , Zheng Huang§ , Junhe Wu† , Jing Cao† , Kai Chen∗
                                                       ∗ School of Information and Electronic Engineering, Shanghai Jiao Tong University, Shanghai, China
                                                                       † Customs National Supervision Bureau for Duty Collection (Shanghai),

                                                                     General Administration of Customs of the P.R.C. (GACC), Shanghai, China
                                                                          ‡ Nanjing Jiyun Information Technology Co., Ltd., Nanjing, China
                                                                   § School of Computer Science, Shanghai Jiao Tong University, Shanghai, China
arXiv:2605.14857v1 [cs.AI] 14 May 2026




                                                                                 ¶ Department of Science and Technology (Shanghai),

                                                                     General Administration of Customs of the P.R.C. (GACC), Shanghai, China



                                            Abstract—Harmonized System (HS) tariff classification is a          system organizes roughly 5,000 commodity groups under a
                                         high-stakes, expert-level task in which a free-form product            hierarchical structure of 21 sections, 99 chapters, approxi-
                                         description must be mapped to a specific six- or eight-digit           mately 1,200 four-digit headings, and several thousand six-
                                         code under the General Interpretive Rules (GIR), section notes,
                                         chapter notes, and Explanatory Notes. The difficulty lies not          digit subheadings; many national administrations, including
                                         in knowledge volume but in multi-dimensional rule reasoning: a         China’s General Administration of Customs (GACC) and the
                                         correct classification must satisfy competing priority rules along     United States International Trade Commission, further extend
                                         several axes simultaneously, including material, form, function,       the six-digit international codes to eight or ten national digits
                                         essential character, the part–versus–whole boundary, and specific      for duty and statistical purposes. Classification of a given
                                         listing versus residual headings. End-to-end prompting of large
                                         language models fails characteristically by resolving one axis         product to a specific code is the legal basis on which import
                                         while ignoring the priority constraints on the others. We present a    duties, value-added tax, anti-dumping levies, dual-use export
                                         deterministic agentic workflow in contrast to self-planning agents:    controls, and a wide range of regulatory permissions are
                                         the control flow is fixed, language model calls are confined to        assigned. The economic stakes are correspondingly high: mis-
                                         narrow stages, and reflection and verification are retained as local   classification can trigger post-entry duty adjustments, shipment
                                         mechanisms. This design yields interpretability by construction—
                                         each decision is decomposed into stage-wise structured outputs         holds, civil penalties, and—in cross border e-commerce—
                                         with verbatim citation of the chapter or section notes that bear       temporary suspensions of postal corridors. Classification is
                                         on it. The architecture combines offline knowledge-engineering         performed every day at industrial scale by customs officers,
                                         of the Chinese HS tariff with an online six-stage pipeline.            brokers, and trade-compliance teams; the WCO reports that
                                         Evaluated on HSCodeComp at the six-digit level, the workflow           more than one billion customs declarations are processed
                                         reaches 75.0% top-1 and 91.5% top-3 at four digits, and 64.2%
                                         top-1 and 78.3% top-3 at six digits with Qwen3.6-plus; an              worldwide each year.
                                         open-weight Qwen3.6-27B-FP8 backbone in non-thinking mode                 The challenge of HS classification is, surprisingly, not one
                                         achieves 84.2% four-digit and 77.4% six-digit top-1 agreement          of knowledge volume. The tariff itself is a finite, public
                                         with the frontier model. A two-stage manual audit of 226               document; the section notes, chapter notes, and Explanatory
                                         six-digit disagreements suggests that a non-trivial fraction of        Notes maintained by the WCO together with national customs
                                         HSCodeComp ground-truth labels may deviate from HS general
                                         rules; full adjudication records are released in the appendix as       administrations occupy at most a few thousand pages. The
                                         preliminary findings for community review.                             difficulty lies in what we call multi-dimensional rule reason-
                                            Index Terms—Harmonized System, tariff classification, large         ing: a correct classification must satisfy competing priority
                                         language models, agentic workflow, retrieval-augmented genera-         rules along several axes simultaneously. At least six such
                                         tion, regulatory reasoning, interpretability, customs compliance.      axes recur across the tariff: (i) material, distinguishing for
                                                                                                                instance plastic from rubber, textile from leather, or steel
                                                                 I. I NTRODUCTION                               from aluminum; (ii) form and processing state, distinguishing
                                                                                                                primary forms (granules, powders, liquids) from intermediate
                                            The Harmonized Commodity Description and Coding Sys-
                                                                                                                forms (rods, profiles, monofilaments), from finished articles,
                                         tem, commonly known as the Harmonized System (HS), is
                                                                                                                from parts; (iii) function and end-use, distinguishing general-
                                         the global nomenclature for traded goods, established and
                                                                                                                purpose articles from those dedicated to a specific machine,
                                         maintained by the World Customs Organization (WCO) and
                                                                                                                vehicle, or medical procedure; (iv) essential character under
                                         implemented in more than 200 customs administrations. The
                                                                                                                GIR 3(b), which arbitrates the classification of composite
                                           Corresponding author: Kai Chen (kchen@sjtu.edu.cn).                  articles by identifying the component that gives the article its
essential character; (v) the part-versus-whole boundary under         tic difficulty of HS classification and explain why end-to-
Section XVI Note 2 and Section XVII Note 2, which decides             end LLM prompting fails on it. We present a deterministic
whether a component is classified with the parent machine or          agentic workflow—combining offline knowledge-engineering
as a separate article in its own right; and (vi) specific listing     of the Chinese HS tariff with an online six-stage pipeline—
versus residual headings under GIR 1 and GIR 3(a), which              and discuss its position relative to self-planning agents. We
mandates that named goods take priority over generic basket           evaluate on HSCodeComp [1], a recent expert-level benchmark
headings.                                                             of 632 product entries, reporting six-digit accuracy as the
   These axes are not independent. The chapter notes them-            primary metric for reasons discussed in Section V. We further
selves embed cross-references and exclusions that re-route            conduct a two-stage manual audit of disagreements between
a candidate classification from one chapter to another; for           our predictions and HSCodeComp ground-truth labels, the
example, the chapter notes of Chapter 39 specify a strict form-       results of which suggest that a non-trivial fraction of the labels
priority architecture in which a finished article in plastic (e.g.,   may deviate from HS general rules; full adjudication records
a 1.75 mm-diameter monofilament made of PLA) must be                  are released as preliminary findings.
classified by its form (heading 39.16, plastic monofilaments)
rather than by its underlying polymer (subheading 3907.70,                                 II. R ELATED W ORK
polylactic acid). A practitioner classifying the same item            A. Datasets and benchmarks for HS classification
without this rule will land on the polymer subheading—a                  Public datasets and benchmarks for HS or HTS classifica-
defensible choice on the material axis but an incorrect one           tion have remained scarce relative to the practical importance
once form priority is taken into account.                             of the task. The most directly relevant recent contribution is
   End-to-end prompting of large language models (LLMs)               HSCodeComp [1], an expert-level benchmark of 632 prod-
on HS classification exhibits exactly this failure pattern. The       uct entries drawn from a large-scale e-commerce platform,
model resolves one axis correctly—most often material, occa-          annotated by multiple e-commerce domain experts at the
sionally function—and produces a fluent, rule-citing rationale        ten-digit level and spanning 27 chapters and 32 first-level
that nonetheless ignores the priority constraints on the other        categories. HSCodeComp is the benchmark on which we
axes. The problem is compounded by the fact that six- and             evaluate in Section V. ATLAS [2], released roughly con-
eight-digit codes are valid-looking integer strings: a model that     temporaneously, contributes a larger-scale dataset of 18,731
has not been grounded in the actual tariff index will readily         rulings processed from the U.S. Customs Rulings Online
fabricate codes that do not exist in the schedule at all. Chain-      Search System (CROSS), with a held-out test split intended for
of-thought prompting alone does not fix this. The underlying          benchmarking large-model classification on U.S. HTS codes.
problem is not insufficient reasoning but the absence of the          An earlier benchmark study by Judy [4] evaluates four com-
right slice of the corpus from the model’s context, together          mercial HTS classification tools—Zonos, Tarifflo, Avalara, and
with the absence of any structural commitment about where             the WCO BACUDA prototype—on 100 CROSS rulings, with
in the corpus the next constraint should be loaded.                   metrics covering accuracy, speed, rationality, and HTS-code
   We report on a production-grade system for Chinese HS              alignment; this work is, to our knowledge, the only published
classification designed around this observation. Rather than          characterization of the commercial landscape on U.S. data.
treat the task as a single generation problem, we decompose           Beyond these, the public dataset situation for non-U.S. tariff
it into a deterministic agentic workflow: a directed sequence         regimes remains thin: we are not aware of an analogously
of narrow, retrieval-grounded LLM stages organized along              sized, expert-annotated, publicly available benchmark for the
the hierarchical structure of the tariff itself (chapter, heading,    Chinese HS regime in the English-language literature.
subheading), with each stage emitting a structured, individu-
ally testable artifact. Reflection, verification, and recovery are    B. Methods for HS classification
retained as local mechanisms within stages, but the control              Methods reported in the English-language literature fall
flow itself is fixed by engineers rather than discovered by           into three broad families. The first family treats the task as
the model. The design has two practical consequences. First,          supervised text classification or retrieval over heading text.
interpretability arises by construction: every classification de-     The most developed entry in this family is Lee et al. [3],
cision is decomposed into stage-wise structured outputs with          who, in collaboration with the Korea Customs Service, propose
verbatim citation of the chapter or section notes that bear on        an explainable decision-supporting model based on Sentence-
the decision, allowing customs officers and declarants to audit       BERT with supervised contrastive learning and a multiple-
each step independently. Second, the workflow is moderate in          negative- ranking loss; the model retrieves precedent rulings
its compute footprint: an open-weight 27B-class backbone in           as explanations and reports 93.9% top-3 accuracy on 925
non-thinking mode produces predictions closely aligned with           challenging subheadings, validated by a 32-expert user study.
a frontier model on the same workflow, indicating that the            Similar contrastive-learning approaches over trade transactions
architecture does not rest on the reasoning capacity of any           have been explored for other national tariff regimes. These sys-
single state-of-the-art LLM.                                          tems are highly competitive within their training distribution
   The contributions of this paper are as follows. We ar-             but, by construction, do not perform multi-step rule reasoning
ticulate multi-dimensional rule reasoning as the characteris-         over GIR clauses or chapter notes.
   The second family fine-tunes large language models on tariff      distinguishes correctness (whether the answer is factually
data. ATLAS [2] is the most recent representative work: a            right) from groundedness (whether the cited authority actually
LLaMA-3.3-70B model supervised-fine-tuned on the 18,731-             supports the claim made). This distinction maps cleanly onto
ruling CROSS training split, reporting 40% ten-digit and             our setting: an HS prediction can be wrong, or it can be right
57.5% six-digit accuracy on held-out CROSS test data and             by accident in the sense that the predicted code is correct while
outperforming several leading proprietary reasoning models           the cited rule does not actually support it. The latter mode
on the same task. Gholamian et al. [5] study LLM in-context          is largely invisible without structured citation output, and we
learning for product classification under realistic data pertur-     will return to this distinction when motivating the design of
bations (abbreviations, deletions), comparing flat, hierarchical-    our final-scoring stage.
prompting, and few-shot LLM configurations against fine-
                                                                     D. Agentic LLM workflows: from self-planning to determinis-
tuned Sentence-Transformer classifiers on e-commerce tax-
                                                                     tic pipelines
onomies; they find LLMs to be substantially more robust to
noisy and abbreviated descriptions than supervised baselines,           The agentic-LLM literature can be read along an axis of
motivating the use of LLMs over noisy small-importer descrip-        how much planning autonomy is granted to the model. At the
tions.                                                               autonomous end, ReAct [10] interleaves reasoning “thoughts”
   The third family targets the agentic setting explicitly, treat-   with environment “actions” in an open-ended loop and has
ing classification as a multi-step reasoning task with tool          become the canonical reference for tool-using LLM agents.
use. HSCodeComp [1] evaluates fourteen foundation models,            Reflexion [11] augments such agents with verbal self-reflection
six open-source agent frameworks instantiated with GPT-5             over previous attempts, stored as episodic memory, to sup-
backbones, and three closed-source deep-search agents; the           port iterative self-improvement. A large family of subsequent
strongest baseline reaches 46.8% ten-digit accuracy on the           frameworks (AutoGen, LangGraph, SmolAgents, and others,
HSCodeComp test set, well below the 95% accuracy reported            surveyed in recent literature) has explored variations on this
for experienced human experts, with the gap not closing              autonomy theme.
under test-time scaling. Collectively, these three families differ      At the lower-autonomy end of the same axis sit workflow-
markedly in their assumptions about where the difficulty of HS       style designs in which the stages are fixed and the LLM is
classification lies—in representation learning, in parametric        invoked only within narrow, well-scoped sub-tasks. Recent
knowledge, or in stepwise rule application—and no consensus          practitioner-facing discussions have sharpened the distinc-
architecture has emerged.                                            tion between “agents” (autonomously orchestrating a plan to
                                                                     achieve a goal) and “workflows” (executing a predefined se-
C. Retrieval-augmented LLMs and reasoning over regulated             quence of LLM calls), arguing that for tasks whose stage struc-
corpora                                                              ture is stable and known in advance, the workflow style offers
   Hybrid retrieval that combines lexical scoring with dense         lower variance, easier debugging, and tighter cost control with-
neural retrieval is now standard in production information-          out sacrificing the use of LLMs as reasoning components. The
retrieval pipelines. ColBERT [7] introduced fine-grained dense       system reported here sits at the lower-autonomy end: the stages
retrieval via late interaction, and the family has continued to      are dictated by the structure of the HS tariff (chapter, heading,
evolve; reciprocal rank fusion [8] provides a calibration-free       subheading) rather than discovered at run time, and reflection,
method for combining rankings from heterogeneous retrievers          verification, and recovery are retained as local mechanisms
and has become a default choice in hybrid search systems.            within individual stages rather than as global planning loops.
On the reranking side, listwise LLM rerankers introduced             We adopt the term deterministic agentic workflow to make this
by RankGPT [9] demonstrated that permutation-generation              position explicit, and the design’s implications for accuracy,
prompts over candidate passages with a sliding-window strat-         interpretability, and operational predictability are discussed in
egy can outperform supervised cross-encoder rerankers in             Section IV.
zero-shot regimes; subsequent open-source variants have es-                                  III. M ETHOD
tablished this as a standard component of retrieval-augmented           This section describes the system. Section III-A states
pipelines.                                                           the design philosophy that shapes everything that follows.
   Retrieval-augmented reasoning over regulated corpora, in-         Section III-B describes the offline knowledge-engineering tier
cluding legal and medical materials, is a closely related            that structures the Chinese HS tariff into queryable artifacts.
research area. Of particular relevance to our work, Magesh           Section III-C walks through the online six-stage classification
et al. [6], in a preregistered empirical evaluation published        pipeline. Figure 1 gives the overall architecture; we annotate
in the Journal of Empirical Legal Studies, examine com-              it as we proceed. Section III-D presents a worked example—a
mercial legal-research products that advertise themselves as         TPU mobile-phone screen protector—tracing the input through
“hallucination-free” through retrieval-augmented generation.         all six stages.
They find that Lexis+ AI hallucinates on approximately 17%
of queries and Westlaw AI-Assisted Research on approxi-              A. Design philosophy: deterministic agentic workflow
mately 33%, even in a setting where retrieval is technically           The control flow of the system is fixed in advance and is
functional. The authors introduce a two-axis taxonomy that           not subject to LLM-side planning at run time. Each stage
                 Offline tier · knowledge engineering


                       Chapter notes                      Section notes                    Hierarchy index                    GIR rules
                    inclusions, exclusions              cross-chapter rules              chapter to subheading               priority logic



                                       BM25 lexical index                                          Dense embedding index
                                     over heading and note text                                     over heading and note text


                                                                                  queried per stage


                 Online tier · six-stage pipeline

                        Input                        1. Attribute extraction                             2. Candidate retrieval
                    free-form text                    material, form, function                           BM25 + dense, RRF, ~40



                                                    4. L2 ranking + confirm                                 3. L1 shortlisting
                                                      notes, exclusions, top-3                             attribute scoring, ~10



                                                   5. Subheading resolution                            6. Final scoring + citation
                                                            six-digit code                               pros, cons, GIR, verbatim




Fig. 1. System architecture. The offline tier (top) decomposes the Chinese HS tariff into structured artifacts: chapter notes, section notes, the chapter-to-
subheading hierarchy index, the General Interpretive Rules, and parallel BM25 and dense embedding indices over heading and note text. The online tier
(bottom) is a six-stage pipeline that queries the offline artifacts at each stage. Candidate counts narrow from approximately forty retrieved headings (Stage 2)
to ten four-digit candidates (Stage 3) to a shortlist of three (Stage 4), with subheading resolution and cited final scoring on top.



is a separate model call with a strict input schema, a strict                    (failures are localizable to specific stages without re-running
output schema, and a stage-local prompt; the output of one                       the pipeline).
stage is the input of the next. Reflection, verification, and
                                                                                 B. Offline tier: HS tariff knowledge engineering
recovery are retained, but as local mechanisms within stages.
For instance, the L2 stage discussed below may re-rank or                           The Chinese HS tariff is published as a structured document
demote a candidate when a chapter-note exclusion is detected;                    with section notes (one per section, of which there are 21),
this is reflection inside the stage, not a global re-plan of the                 chapter notes (one or more per chapter, of which there are
pipeline.                                                                        99), explanatory notes from the WCO adapted by national
                                                                                 customs, and the heading and subheading texts themselves. We
   This is a deliberate counter-position to deep-search agents                   decompose this corpus offline into five families of artifacts.
of the ReAct–Reflexion lineage. We do not claim that plan-                          Note artifacts. Each section note and chapter note is parsed
ning autonomy is bad in general; we claim that for tariff                        into typed clauses: inclusion clauses that admit named goods
classification, the stage structure is dictated by the tariff itself             into a chapter, exclusion clauses that explicitly route named
(chapter, heading, subheading) and is not something the model                    goods out of the chapter (typically into a named alternative
needs to discover. Trading planning autonomy for determinism                     heading), and priority clauses that establish form-priority
in this setting buys three concrete properties: interpretability                 or part-versus-whole disciplines internal to the chapter. The
by construction (every stage emits an inspectable artifact),                     chapter-note exclusions are particularly load-bearing: many of
variance reduction (the same input traverses the same stages                     them encode cross-chapter redirections that an LLM would
in the same order on every call), and operational legibility                     not otherwise see in a single retrieval pass.
   Hierarchy index. The tariff hierarchy is materialized as a         structured pros, cons, and the applicable GIR clauses. The
queryable index from chapter to heading to subheading, with           output is three four-digit candidates.
each level linked to its applicable notes. Given a candidate             Stage 5 (subheading resolution) descends from the chosen
heading, the system can retrieve in O(1) time the full set of         four-digit heading to its six-digit subheadings, applying GIR 6
notes that constrain its classification.                              (the subheading analogue of GIR 1 and GIR 3) together with
   GIR rules. The six General Interpretive Rules are encoded as       subheading-level notes. Where the description unambiguously
priority statements that the online stages can invoke explicitly.     implies a national eight-digit subdivision, the eight-digit code
GIR 1 (headings, then notes), GIR 3(a) (specific over generic),       is also emitted; otherwise the system stops at six digits and
GIR 3(b) (essential character for composite goods), and GIR 6         flags the ambiguity.
(subheading-level analogues of GIR 1 and GIR 3) carry most               Stage 6 (final scoring with structured citation) produces
of the weight in practice.                                            the final output: the top three candidate codes, each annotated
   Retrieval indices. Two parallel indices are built over head-       with a confidence score, supporting points (pro), opposing
ing and note text. A BM25 index handles lexical matches               points (con), the GIR clause(s) applied, and verbatim citations
on rare and concrete nouns (“polyurethane”, “centrifugal”,            from the chapter or section notes that bear on the decision.
“thermosetting”). A dense embedding index handles functional          Citation strings are post-processed to annotate which subset
paraphrases (“for vehicle cooling”, “anti-corrosion coating”).        of the cited rule was load-bearing. The two-axis evaluability
They are combined at retrieval time by Reciprocal Rank                that this output schema enables is discussed in Section IV;
Fusion [8], chosen because it requires no score calibration           the structure also maps directly onto the correctness–versus–
between the two retrievers.                                           groundedness distinction of Magesh et al. [6].
   The offline tier is built once per tariff version. When the
tariff is revised (in China typically annually, with mid-year         D. A worked example
notices), only the affected chapters and headings are re-                To make the pipeline concrete, consider a typical small-
indexed.                                                              importer description: “50 pcs HD hydrogel film for all
                                                                      phones, matte / anti-blue-ray / UV / privacy, TPU material.”
C. Online tier: six-stage classification pipeline                     This is a real entry from the HSCodeComp benchmark.
   Stage 1 (attribute extraction) converts the free-form prod-        Stage      1    extracts    material = thermoplastic
uct description into a structured set of attributes: material, form   polyurethane (TPU),                form = self-adhesive
and processing state, function and intended end-use, salient          thin film,           function = screen protection,
distinguishing features, and—where reliably inferable from            end-use = mobile phone screen, and notes the
the description—origin or brand-name disambiguation. This             marketing terms (matte, anti-blue-ray) as non-classifying
externalizes the implicit pre-reading that a human classifier         decorations. Stage 2 retrieves a mix of plastic-film headings
performs before opening the tariff. The schema is fixed; the          (39.19, 39.20, 39.26) and electronics-related headings (85.17
model is not asked to invent attribute keys.                          parts).
   Stage 2 (candidate retrieval) queries the BM25 and dense              At Stage 3, the L1 ranker reads the heading texts alone
indices in parallel using both the original description and the       and shortlists 39.19 (“self-adhesive plates, sheets, film, and
Stage 1 attributes, and fuses the two ranked lists by RRF.            other flat shapes”, plastics), 39.20 (“other plates, sheets, film,
The output is roughly forty heading candidates. Recall, not           plastics”), and 39.26 (“other articles of plastics”), among
precision, is the goal here; later stages discriminate. Tuning        others. At Stage 4, loading the Chapter 39 chapter notes makes
the BM25/dense weighting by hand was consistently less                the form priority explicit: GIR 3(a) and the named specificity
productive than refining the prompts of the subsequent ranker         of heading 39.19 establish that any self-adhesive plastic flat
stages, and we therefore retain the unweighted RRF fusion.            shape goes to 39.19 ahead of the generic 39.20 and the residual
   Stage 3 (L1 shortlisting) scores each of the forty candidates      39.26. The confirmation sub-step records this as the load-
against the Stage 1 attributes via an LLM ranker prompted             bearing clause and commits to 39.19. Stage 5 descends to
with the heading text alone (no notes yet). The output is             subheading 3919.90 (“other”, as the film is not in rolls of width
approximately ten four-digit candidates. The intent is to do          ≤ 20 cm, which would have indicated 3919.10). Stage 6 emits
cheap discrimination before loading the expensive chapter-note        the final scored output with the verbatim text of heading 39.19,
context.                                                              the GIR 3(a) specificity clause, and the chapter-note text that
   Stage 4 (L2 ranking with note-triggered confirmation)              confirms self-adhesion is sufficient for 39.19 regardless of any
loads the chapter notes and section notes that bear on the            printed pattern.
surviving candidates and performs a second, deeper rank. This            The example also illustrates a failure mode that the pipeline
stage is given explicit permission to demote a candidate purely       is designed to prevent. A model prompted end-to-end on the
on the strength of an exclusion clause—a pattern that mirrors         same description will often land on 3926.90, “other articles of
expert reasoning, in which an apparently strong heading is            plastics”. The underlying mistake is that the model resolves
sometimes ruled out by a single note in the chapter to which          the material axis correctly (plastic) but does not apply the
the candidate belongs. A note-triggered confirmation sub-             form-priority architecture of Chapter 39—which is precisely
step then forces a commitment at the four-digit level, with           the constraint loaded by Stage 4.
                      IV. E XPERIMENTS                                                             TABLE I
                                                                             E ND - TO - END ACCURACY ON HSC ODE C OMP (n=632).
A. Setup
   Benchmark. We evaluate on HSCodeComp [1], an expert-                              Metric                  top-1       top-3
level dataset of 632 product entries collected from a large-scale                    Four-digit accuracy    75.0%     91.5%
e-commerce platform and annotated with ten-digit HS codes                            Six-digit accuracy     64.2%     78.3%
by multiple e-commerce domain experts. Although HSCode-
Comp’s ten-digit codes follow the U.S. Harmonized Tariff
                                                                                                TABLE II
Schedule, the upper levels of the hierarchy (chapter, four-             S TAGE ATTRIBUTION OF FOUR - DIGIT TOP -1 ERRORS (158 CASES ).
digit heading, six-digit subheading) are part of the international
Harmonized System and are directly applicable to the Chinese                     Stage at which the gold heading is lost     Cases
regime. We therefore report results at the four-digit and six-                   Recall miss (Stage 2)                            35
digit levels, and treat the ten-digit level as outside the scope                 L1 drop (Stage 3)                                 3
of a Chinese-tariff system.                                                      L2 not in keep final (Stage 4)                   16
   Backbones. We evaluate two backbones: Qwen3.6-plus, a                         L2 keeps gold but not top-1 (Stage 4)           102
frontier proprietary model accessed via API, used in non-                        Final ranking override (Stage 6)                  2
thinking mode; and Qwen3.6-27B-FP8, an open-weight 27B-                          Total                                           158
class model in FP8 quantization, deployed locally, also in non-
thinking mode. Both backbones are used through the same
workflow; no per-backbone prompt tuning is performed. The            Table II summarizes the result for the 158 four-digit top-1
intent is to test whether the workflow itself, rather than a         errors observed under v7.
particular backbone’s reasoning capacity, drives the result.            Recall failures account for 22% of all four-digit errors; in
   Metrics. We report top-1 and top-3 accuracy at the four-          the overwhelming majority of cases (102 out of 158, 65%) the
digit and six-digit levels: a prediction is correct if any of the    gold heading is retrieved, retained through L1, and kept by L2,
top-3 candidate codes emitted by Stage 6 matches the ground-         but not placed first at the L2 ranking step. This is the failure
truth code at the relevant granularity. We additionally report       mode the L2 stage is most exposed to: the gold heading is
cross-backbone agreement: for the same input, the fraction           correctly recognized as a candidate, but the ranker prefers a
of cases on which Qwen3.6-27B-FP8 emits the same top-                sibling on grounds that, in retrospect, miss a priority constraint
1 prediction as Qwen3.6-plus. Stage attribution counts the           such as form priority or specific-over-generic.
number of cases in which the gold heading is discarded at
each pipeline stage.                                                 D. Backbone substitutability
   Versioning. The system has been iterated over multiple              Table III reports the prediction agreement between the
production releases. We report results for the v7 release, which     Qwen3.6-27B-FP8 backbone and Qwen3.6-plus on the same
introduced expanded recall vocabulary in Stage 2, L1 retention       632 inputs under the same workflow. For top-1 predictions, the
of note-tagged candidates, a self-exclusion rule in Stage 6          two backbones agree on 84.2% of four-digit codes and 77.4%
ranking, and broadened triggers in the L2 confirmation sub-          of six-digit codes.
step.                                                                  The result is consistent with the design hypothesis: when the
                                                                     workflow fixes the control flow and curates the context enter-
B. End-to-end accuracy
                                                                     ing each LLM call, the choice of backbone within a reasonable
   Table I reports end-to-end accuracy on the 632-sample             capability tier becomes less load-bearing than it is for end-to-
HSCodeComp evaluation. With Qwen3.6-plus as the back-                end prompting. A smaller open-weight 27B-class backbone in
bone, the workflow reaches 75.0% top-1 and 91.5% top-3               FP8, run in non-thinking mode on modest hardware, produces
at the four-digit level, and 64.2% top-1 and 78.3% top-3 at          predictions that align with the frontier model on roughly four
the six-digit level. The four-digit top-3 figure, in particular,     out of five four-digit decisions, indicating the workflow can be
indicates that for over nine out of ten queries the gold heading     operated without dependence on a frontier proprietary model.
is contained in the system’s emitted shortlist. The gap between
top-1 and top-3 at four digits (75.0% to 91.5%, i.e., 16.5 pp)       E. Manual audit of disagreements
suggests that the residual error at top-1 is concentrated in            The accuracy numbers in Table I compare predictions
borderline four-digit decisions where multiple headings are          against HSCodeComp’s published ground-truth labels and as-
individually defensible, an observation we revisit in the manual     sume those labels are correct. To examine that assumption, we
audit below.                                                         manually audit the 226 six-digit top-1 disagreements between
                                                                     Qwen3.6-plus predictions and HSCodeComp ground-truth.
C. Stage attribution of four-digit errors                               The audit follows a two-stage protocol. First, each disagree-
   For each query whose top-1 four-digit code does not match         ment is assessed by an external large language model (distinct
the gold heading, we trace the pipeline output to identify the       from the classification backbone) prompted with the HS Ex-
stage at which the gold heading was lost or down-weighted.           planatory Note text, the applicable chapter and section notes,
                            TABLE III                               L2 stage, so that material-named subheadings (e.g., 3907.70
  T OP -1 PREDICTION AGREEMENT BETWEEN Q WEN 3.6-27B-FP8 AND        for PLA) occasionally beat form-named subheadings (e.g.,
 Q WEN 3.6- PLUS ON THE SAME 632 INPUTS AND THE SAME WORKFLOW.
                                                                    39.16 for monofilaments above 1 mm); (iv) parts mistakenly
                 Level                Agreement
                                                                    classified to a generic parts chapter rather than to the functional
                                                                    chapter of the parent machine, in violation of Section XVI
                 Top-1 four-digit   84.2% (532/632)                 and Section XVII Note 2; (v) inconsistent application of
                 Top-1 six-digit    77.4% (489/632)
                                                                    GIR 3(a) specific-over-generic when the candidate set contains
                                                                    a residual basket heading. The five patterns suggest where the
                           TABLE IV                                 offline knowledge base, in particular the encoding of chapter-
         M ANUAL AUDIT OF 226 SIX - DIGIT DISAGREEMENTS .
                                                                    internal priority architectures and the cross-chapter exclusion
                                                                    graph, can be strengthened in subsequent releases.
     Bucket                                       Cases     Share
     A. Agent better supported by HS rules             96   42.5%                              V. C ONCLUSION
     B. Ground truth better supported (agent           34   15.0%
     wrong)                                                            We presented a deterministic agentic workflow for HS
     C. HS boundary, professional disagreement         83   36.7%   tariff classification. The architectural commitment is to fix
     plausible
                                                                    the control flow in advance, confine the LLM to narrow
     D. Data-quality issue in query or label           13   5.8%
                                                                    stages with structured inputs and outputs, and treat reflection
     Total                                            226   100%    and verification as stage-local mechanisms rather than global
                                                                    planning loops. The system combines an offline knowledge-
                                                                    engineering tier that decomposes the Chinese HS tariff into
and a strict instruction to base its judgment only on the rule      typed rule artifacts with an online six-stage pipeline that
text rather than on case analogy. Second, each disagreement         traverses the tariff hierarchy and emits decisions with verbatim
is reviewed by a human expert with customs-classification           rule citations.
training, who confirms or overrides the model’s judgment. The          On HSCodeComp, the workflow reaches 75.0% top-1 and
expert also assigns each disagreement to one of four buckets:       91.5% top-3 four-digit accuracy and 64.2% top-1 and 78.3%
(A) the agent’s prediction appears better supported by the rule     top-3 six-digit accuracy with a frontier backbone; an open-
text; (B) the published ground truth appears better supported       weight 27B-class backbone in non-thinking mode produces
(the agent is wrong); (C) the case is a genuine HS boundary         top-1 predictions that agree with the frontier backbone on
where professional classifiers could reasonably disagree; or        84.2% of four-digit and 77.4% of six-digit cases, indicating
(D) the query text or label exhibits data-quality issues (e.g.,     that the workflow does not depend on the reasoning capacity
the product description and the ground-truth code are mutually      of any single state-of-the-art model. A manual audit of 226
inconsistent).                                                      six-digit disagreements, following an external-LLM-assisted,
   Table IV summarizes the bucket distribution. We emphasize        expert-reviewed protocol, suggests that a non-trivial fraction
that the audit is preliminary. Annotation noise and the inherent    of the published ground-truth labels on this benchmark may
subjectivity of boundary cases mean that the absolute propor-       deviate from HS general rules; we report this finding as
tions should not be taken as definitive; the most defensible        preliminary and release the adjudication record for community
reading is that the proportions in buckets A and D are large        review.
enough that headline accuracy numbers computed against the             Several directions remain open. We are fine-tuning a 9B-
unaudited labels are likely to underestimate the true perfor-       class model on the intermediate artifacts produced by the
mance.                                                              workflow; the training is ongoing and early results are encour-
   Treating bucket A and bucket D as “agent-not-incorrect”          aging, to be reported separately. The cross-chapter exclusion
yields a corrected six-digit top-1 accuracy of approximately        graph implied by the chapter notes is currently exploited
85.8% on this benchmark, with the caveat above. A more ag-          heuristically through Stage 4 retrieval; a more systematic
gressive accounting that also credits boundary cases (bucket C)     graph-based treatment is a natural next step. Finally, the overall
yields approximately 96.2%; we report the conservative figure       template—a deterministic workflow over a hierarchically or-
as the one we are willing to defend without case-by-case            ganized regulatory corpus, with structured rule-cited output—
verification by a second expert.                                    generalizes to adjacent tasks such as sanitary classification,
F. Failure mode analysis                                            dual-use export control, and drug schedule classification,
                                                                    where the answer is constrained by a fixed corpus and the
   Among the 34 bucket-B cases (cases on which the system
                                                                    reasoning must be auditable.
is, on audit, genuinely wrong), we identify five recurring
patterns: (i) semantic confusion in Chapter 71 between cu-                                       R EFERENCES
bic zirconia, rhinestone, synthetic stones, and reconstructed
stones; (ii) boundary between watch-case bodies (9111.x) and         [1] Y. Yang, T. Lan, Q. Jia, L. Zhu, H. Jiang, H. Zhu, L. Wang, W. Luo,
                                                                         and K. Zhang, “HSCodeComp: A realistic and expert-level benchmark
other clock or watch parts (9114.x) in Chapter 91; (iii) in-             for deep search agents in hierarchical rule application,” arXiv preprint
sufficient surfacing of form priority in Chapter 39 at the               arXiv:2510.19631, 2025.
 [2] P. Yuvraj and S. Devarakonda, “ATLAS: Benchmarking and adapting
     LLMs for global trade via harmonized tariff code classification,” arXiv
     preprint arXiv:2509.18400, 2025.
 [3] E. Lee, S. Kim, S. Kim, S. Jung, H. Kim, and M. Cha, “Explainable
     product classification for customs,” ACM Trans. Intell. Syst. Technol.,
     vol. 15, no. 2, art. 25, pp. 1–24, 2024.
 [4] B. Judy, “Benchmarking harmonized tariff schedule classification mod-
     els,” arXiv preprint arXiv:2412.14179, 2024.
 [5] S. Gholamian, G. Romani, B. Rudnikowicz, and S. Skylaki, “LLM-
     based robust product classification in commerce and compliance,” in
     Proc. 1st Workshop on Customizable NLP (CustomNLP4U) at EMNLP,
     2024, pp. 26–36.
 [6] V. Magesh, F. Surani, M. Dahl, M. Suzgun, C. D. Manning, and D. E.
     Ho, “Hallucination-free? Assessing the reliability of leading AI legal
     research tools,” J. Empir. Legal Studies, vol. 22, pp. 216–242, 2025.
 [7] O. Khattab and M. Zaharia, “ColBERT: Efficient and effective passage
     search via contextualized late interaction over BERT,” in Proc. SIGIR,
     2020, pp. 39–48.
 [8] G. V. Cormack, C. L. A. Clarke, and S. Büttcher, “Reciprocal rank
     fusion outperforms Condorcet and individual rank learning methods,” in
     Proc. SIGIR, 2009, pp. 758–759.
 [9] W. Sun, L. Yan, X. Ma, S. Wang, P. Ren, Z. Chen, D. Yin, and Z. Ren,
     “Is ChatGPT good at search? Investigating large language models as
     re-ranking agents,” in Proc. EMNLP, 2023, pp. 14918–14937.
[10] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao,
     “ReAct: Synergizing reasoning and acting in language models,” in Proc.
     ICLR, 2023.
[11] N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan, and
     S. Yao, “Reflexion: Language agents with verbal reinforcement learn-
     ing,” in Proc. NeurIPS, 2023.
Appendix: Manual audit of 226 six-digit disagreements
The table below shows 26 representative cases from the manual audit of 226 six-digit top-1 disagreements between system
predictions and HSCodeComp ground-truth labels (Section IV-E). Columns: HSCodeComp task ID; product; published ground-
truth six-digit code (GT); system prediction (Agent); expert-assigned bucket; one-line rule-based rationale citing HS Explanatory
Notes or chapter or section notes. Buckets: A—system better supported by HS rules than the published GT (GT may deviate);
B—published GT better supported, system is wrong; C—genuine HS boundary; D—data-quality issue in query or label. The
complete record, per-case citations, and full nine-stage traces are available from the corresponding author on request.
ID        Product                                  GT           Agent         Bk       Rule-based rationale
    Bucket A — system’s prediction better supported by HS rules (GT may deviate)
350       TPU self-adhesive screen film            3926.90      3919.90       A        Heading 39.19 names self-adhesive plastic flat shapes specifically; GIR 3(a) places it ahead of the
                                                                                       residual basket 39.26.
287       ANNKE 8CH network video                  8522.90      8521.90       A        A network video recorder is a complete recording apparatus directly listed in 85.21; it is not a
          recorder                                                                     part within the scope of 85.22.
7         Zinc-alloy with rhinestone jewelry       7116.20      7117.19       A        Rhinestones are glass imitations of gemstones (not natural, synthetic, or reconstructed stones per
          set                                                                          Chapter 71 Note 1); jewelry with glass imitations falls in 71.17.
608       99.8% high-concentration tattoo          3304.99      3004.90       A        High-concentration anesthetic for permanent makeup is a medicament; 30.04 names this use
          anesthetic cream                                                             specifically, ahead of cosmetic heading 33.04.
316       Untreated natural human hair, bulk       6704.20      0501.00       A        Heading 05.01 covers human hair, unworked; 67.04 covers wigs and false eyelashes (worked
                                                                                       articles), to which the product has not yet been processed.
391       Transparent PVC ankle rain boots         6402.19      6401.92       A        Heading 64.01 specifically names waterproof footwear of rubber or plastics; PVC waterproof boots
                                                                                       are therefore precluded from 64.02.
117       Nike Air Max running shoes               6404.19      6404.11       A        Subheading 6404.11 specifically names sports footwear, including training and running shoes;
                                                                                       6404.19 is the residual subheading.
558       Polar-fleece neck gaiter / scarf         6307.90      6117.10       A        Heading 61.17 specifically names knitted scarves and similar articles; 63.07 is a residual heading
                                                                                       for other made-up textile articles.
31        GPS dog-fence wireless collar            8543.70      8526.91       A        The principal function is radio-navigation positioning, specifically named in 85.26.91, ahead of
                                                                                       the residual heading 85.43 for unnamed electrical apparatus.
32        Fractional CO2 laser skin device         8543.70      9018.90       A        A professional medical / aesthetic laser instrument is more specifically classified in 90.18 than in
                                                                                       the residual heading 85.43.
472       Activated-carbon replacement filter      8421.21      8421.99       A        A replacement consumable for a filtration apparatus is a part, classified in 8421.99, not in the
          cartridge                                                                    integrated-apparatus subheading 8421.21.
46        Xiaomi Redmi K40 OLED display            8517.79      8524.92       A        The 2022 HS introduced 85.24 to specifically cover flat panel display modules; an OLED display
          assembly                                                                     assembly falls under 8524.92, more specific than 8517.79 (parts of phones).
233       Loose freshwater pearls for DIY          7116.10      7101.22       A        Loose pearls not strung into jewelry are classified in 71.01; heading 71.16 covers articles of pearls
                                                                                       (i.e., finished jewelry).
    Bucket B — system is wrong; GT is better supported (failure modes identified in Section IV-F)
137       PLA 3D-printer filament, 1.75 mm         3916.90      3907.70       B        Chapter 39 imposes a form-priority architecture: monofilaments above 1 mm in cross-section
                                                                                       belong to heading 39.16, regardless of the underlying polymer; 3907.70 names PLA in primary
                                                                                       form.
480       Car air-conditioning filter element      8421.39      4823.20       B        A finished filter element is a complete filtering apparatus and is classified in 84.21 regardless of
          (Mercedes)                                                                   the substrate material (paper, fabric, or metal); the system mistakenly took the paper-substrate
                                                                                       path.
52        Arduino UNO R3 development               8542.31      8543.70       B        A general-purpose microcontroller-on-carrier without dedicated end-function is admissible under
          board                                                                        85.42 as a packaged assembly of integrated circuits; the system over-applied the 8542 exclusion
                                                                                       clause and landed in the residual 85.43.
606       Stainless-steel cleaning filter basket   7326.90      7326.20       B        Subheading 7326.20 specifically names articles of iron or steel wire, to which a wire-mesh basket
          (wire mesh)                                                                  conforms; the system selected the residual 7326.90 unnecessarily.
569       Anti-theft bicycle padlock (alloy        8301.40      8301.10       B        Subheading 8301.10 specifically names padlocks; 8301.40 covers other locks.
          steel)
    Bucket C — HS boundary, professional classifiers may disagree
20        DIATONE BLHeli 32 brushless              8503.00      8504.40       C        An electronic speed controller for a brushless motor sits between motor-part heading 85.03 and
          ESC                                                                          static-converter heading 85.04; both are defensible in current practice.
295       LG washing-machine MCU control           8537.10      8450.90       C        The application of Section XVI Note 2(a) vs. Note 2(b) is contested for MCU-bearing appliance
          board                                                                        control boards; both 85.37 and 8450.90 have precedent.
113       Halter-neck  strappy  bodysuit           6211.43      6204.33       C        Heading 62.11 (casual / sportswear) and heading 62.04 (women’s upper garments) overlap for
          (polyester)                                                                  halter-neck strappy tops; national practice varies.
274       UGREEN HDMI-compatible video             8544.20      8544.42       C        HDMI cables are technically shielded multi-conductor, between coaxial-cable 8544.20 and 8544.42
          cable                                                                        (other conductors with connectors); current administrative practice differs by country.
    Bucket D — data-quality issue in query or label
108       “Korean luxury denim distressed          6103.42      6203.42       D        The query describes denim trousers (woven by construction); the GT records a knitted subheading
          jeans”                                                                       (6103), inconsistent with the product.
543       Confederate flag, 100D polyester,        4911.91      6304.93       D        The query self-annotates that the item is a printed-and-dyed polyester flag; the GT codes it as
          3×5 ft                                                                       printed matter (49.11), inconsistent with textile flag products.
627       USB car charger with cigarette-          9613.80      8504.40       D        The GT records 96.13 (lighters), incompatible with the product, which is a static converter for
          lighter plug                                                                 in-vehicle charging.
