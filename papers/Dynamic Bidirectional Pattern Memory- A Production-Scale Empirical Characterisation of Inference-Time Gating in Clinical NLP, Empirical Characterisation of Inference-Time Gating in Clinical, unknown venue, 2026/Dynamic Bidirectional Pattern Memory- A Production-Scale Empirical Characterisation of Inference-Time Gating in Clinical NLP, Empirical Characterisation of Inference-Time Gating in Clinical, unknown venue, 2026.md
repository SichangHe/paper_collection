                                        Dynamic Bidirectional Pattern Memory: A Production-Scale
                                        Empirical Characterisation of Inference-Time Gating in Clinical
                                        NLP⋆
                                        Ali H. Lazema,b,∗ (Corresponding Author), William Teahana (Co-Author)
                                        a School of Computer Science and Engineering, Bangor University, Bangor, Gwynedd, LL57 2DG, United Kingdom
                                        b University of Thi-Qar, Nasiriyah, 64001, Iraq



                                        ARTICLE INFO                                      ABSTRACT
                                                                                          We study inference-time pattern-memory gating in a production-scale clinical natural language
arXiv:2607.00870v1 [cs.CL] 1 Jul 2026




                                        Keywords:
                                        multi-agent pattern memory                        processing (NLP) pipeline. The pipeline pairs a generator (Llama-3.3 70B) that proposes
                                        inference-time gating                             extractions with a verifier (MMed-Llama-3.1 70B) that accepts or rejects them, over 167,034
                                        clinical natural language processing              PMC-Patients narratives, and we add a lightweight memory that learns at deployment time
                                        large language model verification                 which extractions to filter, so the verifier need not re-examine candidates already seen to fail.
                                        generator-verifier architecture                   We report four findings. First, learning these filtering rules directly from the verifier’s rejections
                                                                                          did not work at full scale: the relation-extraction filter ended up empty even though the pipeline
                                                                                          logged 785,797 rejected candidates, because the rejections were spread too thinly across too
                                                                                          many distinct forms to accumulate. Second, a simpler rule based on a fixed clinical ontology
                                                                                          produced the same filtering without relying on the verifier at all, capturing 49,734 ontology-
                                                                                          violating relations on a held-out 5,000-patient set. Third, we tested five versions of the question-
                                                                                          answering filter; four failed for distinct and instructive reasons, and the fifth succeeded by
                                                                                          checking whether a patient’s extracted clinical entities actually support the question being asked;
                                                                                          on the categories where it applies, it was 1.84 times more likely to flag an answer the verifier
                                                                                          would reject than one it would accept. Fourth, across all five versions one pattern held: a filter
                                                                                          is selective only when it tests the same evidence the verifier itself weighs, not when it tries to
                                                                                          imitate the verifier’s output. Taken together, these findings give a practical, transferable result for
                                                                                          any generator-verifier pipeline: the most natural memory design can fail silently at deployment
                                                                                          scale, and whether a pre-generation gate is selective is decided before any engineering effort, by
                                                                                          whether its signal probes the question the verifier itself answers. Throughout, the system flags
                                                                                          suspect extractions rather than deleting them, so every decision stays visible for clinical review.
                                                                                          All code and test artefacts are released openly.




                                        1. Introduction
                                            Large language models have transformed clinical natural language processing, enabling extraction of named
                                        entities, relations, and question–answer pairs from clinical narratives at scales unattainable with prior rule-based or
                                        fine-tuned-classifier pipelines. A growing body of work pairs a generator model with a verifier model that scores or
                                        accepts the generator’s outputs (Madaan et al., 2023; Shinn et al., 2023; Yao et al., 2023), adding an inference-time
                                        correctness check on top of instruction tuning and retrieval. This pattern is attractive in clinical settings, where an
                                        unverified extraction can carry a factual error into a patient record. At the scale of clinical informatics corpora, however,
                                        where hundreds of thousands of narratives are processed without model retraining, inference-time verification becomes
                                        the dominant computational expense. This motivates a mechanism that avoids invoking the verifier on candidates the
                                        pipeline has, in effect, already seen fail: an inference-time memory that accumulates verdict evidence as the pipeline
                                        runs and gates future candidates accordingly, without retraining either model.
                                            The design space for such a memory is large, and which choices actually yield selective gating, gating that flags the
                                        candidates a verifier would reject while leaving those it would accept, is not established. A memory can be configured
                                        and yet remain empirically inactive at deployment scale; a gating signal can be sophisticated and yet fail to separate
                                            ⋆
                                              This work was supported by the Ministry of Higher Education and Scientific Research in Iraq and conducted on the Supercomputing Wales
                                        Falcon (SCWF00175) platform.
                                            ∗ Corresponding author

                                                lhl23prg@bangor.ac.uk (A.H. Lazem); w.j.teahan@bangor.ac.uk (W. Teahan)
                                              ORCID (s): 0000-0002-8677-9689 (A.H. Lazem); 0000-0003-3640-6750 (W. Teahan)




                                        A.H. Lazem et al.: Preprint submitted to Elsevier                                                                                        Page 1 of 39
                                            Dynamic Bidirectional Pattern Memory

the candidates the verifier distinguishes. The central open question is therefore not how to build such a memory, but
which signal sources make its gates selective, and which do not.
    This paper addresses that question through the design, deployment, and empirical characterisation of Dynamic
Bidirectional Pattern Memory (DBPM), an inference-time pattern memory embedded in a multi-agent clinical-NLP
pipeline. The pipeline processes the 167,034-patient PMC-Patients corpus (Zhao et al., 2023) with Llama-3.3 70B
as generator and MMed-Llama-3.1 70B (Qiu et al., 2024) as verifier. DBPM consumes the verifier’s verdict stream
and gates the generator’s future candidates at three pipeline stages (named-entity recognition, relation extraction,
and question answering with reasoning), modifying no parameters of either model. We characterise its behaviour at
production scale, where failure modes become visible that benchmark-scale evaluation does not expose.
    The characterisation yields a single structural regularity that organises the paper:a pre-generation gating signal is
selective for verifier rejection only when it directly tests the same evidence the verifier itself weighs. A signal that probes
a different quantity, however sophisticated its aggregation, does not separate the candidates the verifier distinguishes.
This regularity is practical: a practitioner can assess a candidate signal source by asking whether it probes the same
question the verifier answers, before committing engineering effort to it. It emerges from a controlled dissection of five
gating-signal sources, four of which fail to produce selective gating and one of which succeeds, and it is consistent
with a second, independent finding about how such a memory populates at scale.

Contributions
    This paper makes four contributions, unified by the question of what makes inference-time pattern-memory gating
selective in a production clinical pipeline.

(C1) Production-scale evidence that the natural verifier-fed design fails. The most natural design, accumulating
the verifier’s own rejections by candidate type and gating on the accumulated evidence, does not populate at 167,034-
patient scale: the relation-extraction blocklist remains empty despite hundreds of thousands of logged rejection events.
We show the cause is structural, an interaction between evidence accumulation, time-decay, and pruning under
a rejection stream that is diffuse rather than concentrated, and that it generalises to any inference-time memory
accumulating statistics over free-form LLM output.

(C2) A working verifier-independent signal source for the same channel. Replacing the diffuse verifier-fed
signal with a deterministic ontology-violation predicate, which maps free-form relation labels to a bounded canonical
space, populates the same downstream gate where the verifier-fed pathway did not. The signal source, not the
persistence mechanism, is what determines whether the channel populates.

(C3) A five-source empirical dissection of gating-signal selectivity. We test five distinct signal sources for the
question-answering gate. Four fail to produce selective gating, each for a structurally distinct reason, aggregation-level
mismatch, signal absence, counting asymmetry, and cross-task orthogonality, and one succeeds. The dissection isolates
why each failure occurs, rather than reporting only the design that worked.

(C4) A structural regularity for selective inference-time gating. The successful signal source is the one that tests
whether a patient’s extracted clinical entities support the question being asked, the same grounding question the verifier
implicitly resolves. Across the five sources, selectivity tracks this alignment and nothing else, yielding the regularity
above as an empirical, operationalisable guide for gate design in any generator–verifier architecture.
    We deploy and measure DBPM under a measurement-instrumented discipline that flags suspect candidates rather
than deleting them, so every gating decision remains visible for clinical review, and we disclose the operating-envelope
bounds within which the selective gate applies. All gating code and evaluation artefacts are released openly.

Paper organisation
    Section 2 positions DBPM against related work. Section 3 formalises the multi-agent pipeline and the inference-
time-memory problem, and defines the candidate signature on which the memory is keyed. Section 4 specifies the
DBPM design, including the early design decisions that motivated it, the persistence layer, three-tier gating, the
ontology-violation signal source, and the five gating-signal sources evaluated for the question-answering gate. Section 5
describes the experimental setup and the stratified 5,000-patient evaluation cohort. Section 6 reports the empirical
findings, from the verifier-fed-channel failure at production scale through the signal-source dissection and its per-
category operating envelope. Section 7 synthesises the structural regularity and its clinical implications; Section 8

A.H. Lazem et al.: Preprint submitted to Elsevier                                                                 Page 2 of 39
                                            Dynamic Bidirectional Pattern Memory

discloses the operating-envelope and construct-overlap bounds; and Section 9 identifies schema closure, dataset-quality
evaluation, and held-out validation as future work. Section 10 concludes.


2. Related Work
   DBPM sits at the intersection of seven research threads in modern NLP and machine learning. We position it
against the closest neighbour in each, drawing distinctions in mechanism, deployment scope, and what the framework
explicitly does not do.

2.1. Multi-Agent Pipelines and Verifier-Driven Generation
    The generator–verifier separation underpins much recent inference-time work on LLM reliability. Self-Refine
(Madaan et al., 2023) uses the same LLM to generate, critique, and refine outputs across multiple self-iterations on
a single input. Reflexion (Shinn et al., 2023) extends this with verbal self-reflection persisted in an episodic memory
buffer between trials, reinforcing the agent through linguistic feedback rather than gradient updates. ReAct (Yao et al.,
2023) interleaves reasoning traces with tool use actions in a single trajectory. AutoGen (Wu et al., 2024) and MetaGPT
(Hong et al., 2024) frame the verifier generator separation as multi-agent conversation with role specialization and
standardized operating procedures, respectively. Generative Agents (Park et al., 2023) extends the memory-trace
concept to long-running interactive simulations. LLM-as-a-judge frameworks (Zheng et al., 2023) systematize the
use of strong LLMs as evaluators of weaker generators.
    These systems share with DBPM the principle that an inference-time critic can improve output quality without
retraining. They differ from DBPM in two structural ways. First, with the exception of Reflexion’s episodic buffer,
the critic state in these systems either does not persist across inputs (Self-Refine, ReAct) or persists as natural
language reflections that the generator must re-interpret each call (Reflexion). DBPM persists categorical evidence
about candidate signatures in a structured store consulted by the gate at decision time, with amortised (1) lookup:
gate queries reduce to hash-set membership over precomputed per-task block, downgrade, and whitelist indices, and
writes to in-place dictionary updates keyed on the signature. This is required as design constraint C1 (Section 3.3) and
detailed in Appendix A.1. Second, none of these systems publishes empirical evidence that the natural verifier-fed-
memory design fails at production scale; DBPM does (Section 6.1), motivating the verifier independent signal sources
that follow.

2.2. Knowledge Sharing Between Agents
    A line of work in multi-agent systems formalised structured information exchange between cooperating agents
long before the LLM era. Tambe’s STEAM model (Tambe, 1997) framed teamwork as agents maintaining shared joint
intentions, monitoring team-member performance, and selectively communicating evidence under decision theoretic
constraints an early operationalisation of the principle that cooperating agents need shared structured state, not only
message-passing, to coordinate reliably. Teahan and Tuff (2006) subsequently proposed a framework for knowledge
sharing between autonomous agents operating in a shared environment, addressing how candidate evidence should be
exchanged and consolidated.
    DBPM operationalises the same problem for the generator–verifier setting: the generator and the verifier are two
agents that share a structured memory consulted at gate time, with the verifier’s verdict statistics supplemented by a
verifier independent ontology signal forming the shared representation. The question these earlier frameworks raised,
“How should autonomous agents share evidence about candidate decisions?”, is the same question DBPM answers in
the modern setting. We view this lineage as a relevant predecessor to the present paper’s framing; the contribution of our
work is the empirical characterisation of which signal sources actually populate such a shared memory at deployment
scale.

2.3. Retrieval and Memory-Augmented Generation
     Retrieval-augmented generation (Lewis et al., 2020) and the trillion-token RETRO architecture (Borgeaud et al.,
2022) maintain a deployment-time store consulted at inference, but the store contains information (documents,
embeddings, factual chunks) used to augment the generator’s input. End-to-end Memory Networks (Sukhbaatar et al.,
2015), Memory-Augmented Neural Networks (Santoro et al., 2016), and the Differentiable Neural Computer (Graves
et al., 2016) introduce learned external memories used as read/write substrate during training; the store evolves through
gradient updates and persists across episodes within a single trained model.


A.H. Lazem et al.: Preprint submitted to Elsevier                                                             Page 3 of 39
                                            Dynamic Bidirectional Pattern Memory

    The closest published cousin to DBPM in this lineage is Agentic Context Engineering (Zhang et al., 2026).
ACE treats context as an evolving playbook accumulated through a generator–reflector–curator loop, with structured
incremental updates that preserve detailed strategy knowledge across many interactions. ACE and DBPM share the
principle of inference-time-evolving deployment state that informs future generations without weight modification.
They differ in mechanism layer: ACE updates a context document that the agent reads (a prompt-side intervention);
DBPM updates a gate that filters the agent’s output (a verification-side intervention). Both operate downstream of a
frozen generator; neither requires retraining. We see ACE as the closest concurrent work in evolving deployment state;
DBPM addresses a different question (“Which signals make a verification-gate selective?”) than ACE (“How to grow
a structured context?”).

2.4. Continual Learning and Test-Time Adaptation
     A separate line of work studies how trained models can adapt without forgetting prior knowledge. Elastic Weight
Consolidation (Kirkpatrick et al., 2017) selectively slows learning on weights important for prior tasks to mitigate
catastrophic forgetting. Gradient Episodic Memory (Lopez-Paz and Ranzato, 2017) stores past examples and constrains
updates to avoid increasing loss on stored data. TENT (Wang et al., 2021) adapts batch-normalization affine parameters
at test time via entropy minimization. SHOT (Liang et al., 2020) freezes the source classifier and learns target features
through information maximization plus pseudo-labels. Parisi et al. (2019) review the broader continual-learning
landscape.
     DBPM is orthogonal to all of these. EWC, GEM, TENT, and SHOT all modify model parameters either selectively
(EWC, GEM) or via self-supervised test-time objectives during deployment (TENT, SHOT). DBPM modifies no
parameters of either the generator or the verifier; it adds an external gate consulted at inference. We cite this cluster to
position DBPM in the design space, not as direct competitor.

2.5. Clinical NLP and Biomedical Extraction
    End-to-end clinical NLP pipelines have evolved from rule-based systems through neural and now generative archi-
tectures. MetaMap (Aronson, 2001) and cTAKES (Savova et al., 2010) established the modern pipeline structure with
deterministic ontology mapping over UMLS. Domain-specific BERTs, BioBERT (Lee et al., 2020), PubMedBERT
(Gu et al., 2021) and ClinicalBERT (Alsentzer et al., 2019)—improved entity recognition through pretraining on
biomedical corpora. The 2018 n2c2 shared task on adverse drug events (Henry et al., 2020) crystallized the relation-
classification benchmark for clinical extraction. The verifier model in our pipeline, MMed-Llama-3.1 70B (Qiu et al.,
2024), continues this trajectory with multilingual medical pretraining.
    Most recent clinical NLP systems emphasize the generator side (model size, instruction tuning, domain pretraining)
and treat the pipeline as feed-forward: extraction stages produce candidates that are scored or filtered downstream.
DBPM adds an orthogonal component, a deployment-time gate, that maintains structured evidence about candidate
signatures across patients and consults this evidence at each stage. The ontology-based mechanism in our pipeline
(the Ontology-Violation Filter; M3-RE in the codebase) explicitly returns to the deterministic-ontology tradition of
MetaMap and cTAKES, but applies it as a runtime gate alongside LLM-driven extraction rather than as the primary
extraction method.

2.6. Inference-Time Adaptation and Weak Supervision
    Methods that adapt LLMs at inference without gradient updates include few-shot in context learning (Brown et al.,
2020), chain-of-thought prompting (Wei et al., 2022), and self-consistency (Wang et al., 2023). These operate within
a single forward pass or a small number of self-iterations on a single input. They are complementary to DBPM: a
DBPM-gated pipeline can use any of these at the generator stage. Weak-supervision frameworks (Ratner et al., 2019)
combine multiple noisy label sources at training time without ground truth; DBPM combines multiple signal sources
(verifier verdicts, ontology violations) at deployment time. Self-training methods such as Pseudo-Label (Lee, 2013)
and Noisy Student (Xie et al., 2020) use model predictions as training signals; DBPM does not train, but its memory
store does accumulate verdict statistics that could in principle feed downstream training (we do not pursue this in the
present paper).

2.7. Knowledge Distillation and Data Curation
    DBPM’s output verified, gated extraction results is a candidate substrate for downstream model training. Knowledge
distillation (Hinton et al., 2015) compresses an ensemble’s predictions into a single model. Stanford Alpaca (Taori


A.H. Lazem et al.: Preprint submitted to Elsevier                                                               Page 4 of 39
                                              Dynamic Bidirectional Pattern Memory


Table 1
Positioning of DBPM against the closest system in each related thread. A filled circle (●) marks a property the system
has; an open circle (❍) marks its absence. Columns are: inference-time state that persists across inputs; a verifier distinct
from the generator; a deterministic ontology constraint; published evidence of a production-scale population failure; and
treatment of which signal makes a gate selective. DBPM is distinguished not by any single column but by the last two:
it is the only entry documenting the verifier-fed failure at deployment scale and isolating the signal property that governs
selectivity.

                                                                  Persistent     Verifier    Ontology      Scale-fail.     Signal
   System                                                            state       distinct   constraint      evidence     selectivity

   Self-Refine (Madaan et al., 2023)                                   ❍            ●            ❍             ❍             ❍
   Reflexion (Shinn et al., 2023)                                     ●†            ●            ❍             ❍             ❍
   ReAct (Yao et al., 2023)                                            ❍            ❍            ❍             ❍             ❍
   RAG / RETRO (Lewis et al., 2020; Borgeaud et al., 2022)             ●            ❍            ❍             ❍             ❍
   ACE (Zhang et al., 2026)                                            ●            ●            ❍             ❍             ❍
   MetaMap / cTAKES (Aronson, 2001; Savova et al., 2010)               ❍            ❍            ●             ❍             ❍
   LLM-as-judge (Zheng et al., 2023)                                   ❍            ●            ❍             ❍             ❍

   DBPM (this work)                                                    ●            ●            ●             ●              ●
    † Reflexion persists natural-language reflections in an episodic buffer, re-interpreted by the generator each call, rather than

                                        structured categorical evidence consulted by a gate.


et al., 2023) and Vicuna (Chiang et al., 2023) demonstrated that instruction tuning data from strong generators can
produce competitive smaller models. LIMA (Zhou et al., 2023) showed that surprisingly little high quality alignment
data suffices for strong instruction following. QuRating (Wettig et al., 2024) systematizes quality-based selection of
pretraining data via LLM judgments on writing style, expertise, and educational value.
    DBPM is positioned relative to this cluster as an upstream quality-control layer for data-generation pipelines. The
framework does not perform distillation or selection itself; it provides structured provenance for downstream curators
to use. The dataset quality evaluation of DBPM’s outputs (true-positive rates on individual suppressions, downstream
training-utility studies) is outside the scope of this paper and is reserved for future work on the resulting corpus.

    Summary of positioning: DBPM is not the first system to maintain inference-time state (RAG, RETRO, Reflexion,
ACE), not the first to use a verifier distinct from a generator (Self-Refine, AutoGen, LLM-as-judge), and not the first to
apply ontology constraints in clinical extraction (MetaMap, cTAKES). Its contribution is empirical: a characterization
of which signal sources actually populate inference-time pattern memory at production scale, what failure modes
prevent the naïve verifier-fed design from working, and what structural property a working signal source must
satisfy. The five-iteration M1 dissection (Section 6.3) and the Ontology-Violation Filter verifier-independent pathway
(Section 6.2) jointly answer the question of what makes inference-time pattern-memory gating selective in this regime.
Table 1 summarises this positioning against the closest system in each thread.


3. Background and Problem Formulation
   This section formalises the deployment setting in which DBPM operates. The objective is to specify the multi-
agent pipeline, the verdict feedback signal it produces, and the constraints any inference-time memory mechanism
must satisfy. Mechanism details are deferred to Section 4.

3.1. Multi-Agent Clinical NLP Pipeline
    Let 𝐷 = {𝑥1 , … , 𝑥𝑁 } denote a corpus of 𝑁 clinical narratives, where each 𝑥𝑖 is a single patient narrative. The
pipeline produces structured outputs across a finite task set 𝑇 with cardinality |𝑇 | = 11, indexed by a task identifier
𝑡 ∈ 𝑇 . In our deployment, 𝑁 = 167,034, the PMC-Patients narrative corpus (Zhao et al., 2023). The eleven task buckets
per patient record are named entity recognition (NER), relation extraction (RE), question–answer pairs with four-layer




A.H. Lazem et al.: Preprint submitted to Elsevier                                                                         Page 5 of 39
                                              Dynamic Bidirectional Pattern Memory

reasoning schemas (QAR), clinical-fidelity summarisation, medication extraction, temporal-event extraction, active-
risk identification, risk-state-machine derivation, risk-based recommendations, risk-grounded QA, and a visualisation-
payload assembly stage. Each task emits its own output stream: NER, RE, and QAR share the enriched multi-task
output file, while the other eight buckets each produce a dedicated .jsonl output.
    DBPM’s active consumer gates are defined for three of these tasks: NER, RE, and QAR. This reflects the deployed
worker’s gate implementation; the remaining buckets are not gated at the candidate level. NER is the upstream
entity extractor, and its output feeds downstream relation extraction, temporal-event extraction, and the deterministic
intelligence-layer components that depend on extracted entities. RE and QAR carry their own gates because they emit
candidate-level verdict streams that DBPM consumes alongside NER. Throughout the rest of this paper, all DBPM-
gating claims refer to these three gates.
    Each narrative is processed by two LLM agents:

    • A generator agent 𝐺 that produces, for each narrative-task pair (𝑥𝑖 , 𝑡), a set of task-specific candidate outputs
                (𝑘)                             (𝑘)
      𝐶𝑖,𝑡 = {𝑐𝑖,𝑡  ∶ 𝑘 = 1, … , 𝐾𝑖,𝑡 }, where 𝑐𝑖,𝑡 is the 𝑘-th candidate and 𝐾𝑖,𝑡 is the number of candidates emitted for
      that pair. The generator is Llama-3.3 70B, served via vLLM continuous batching on two tensor-parallel H200
      GPUs.
                                                           (𝑘)
    • A verifier agent 𝑉 that assigns each candidate 𝑐𝑖,𝑡      a categorical verdict 𝑣(𝑘)
                                                                                       𝑖,𝑡 ∈ 𝑉𝑡 , where 𝑉𝑡 denotes the
      verdict space for task 𝑡. (The verdict space 𝑉𝑡 is a set of categorical labels and is notationally distinct from
      the verifier agent 𝑉 , which is a model; the two share a letter but not a referent.) The verdict space is task-
      specific: 𝑉𝑡 = {PASS, FAIL} for the binary verification tasks (NER, QAR, medications, summary), and
      𝑉𝑡 = {PASS_STRONG, PASS_WEAK, FAIL} for relation extraction. The graded form on RE reflects clinical
      relations of varying support strength. The remaining non-gated tasks use verdict structures that DBPM does not
      consume and that we do not specify here. The verifier emits no continuous confidence; the pipeline derives any
      post-hoc multiplier from the categorical verdict and internal rule-based signals. The verifier is MMed-Llama-3.1
      70B (Qiu et al., 2024), served on the remaining two H200 GPUs.

    The QAR task produces question–answer pairs together with a four-layer reasoning schema. A single DBPM gate
(denoted gate_qa in the codebase, for historical reasons) handles both the minimal-context QA case and the full-
reasoning QAR case. The deployed runs reported throughout this paper use the QAR configuration, and all selectivity
claims (Sections 6.3 and 6.4) are measured against QAR outputs.
                      (𝑘)                                     (𝑘)
    Each candidate 𝑐𝑖,𝑡   admits an extractable signature 𝜎(𝑐𝑖,𝑡  ) ∈ Σ𝑡 . We define a signature as the canonical key under
which candidates are grouped in memory: a deterministic, normalised identifier computed from the candidate, such
that two candidates occurring in different narratives are treated as the same pattern if and only if they share a signature.
                                                                                                           ⨆
Here Σ𝑡 is the task-specific signature space, the set of all signatures admissible for task 𝑡, and Σ = 𝑡∈𝑇 Σ𝑡 is their
disjoint union across tasks. The signature is the unit of memory: the memory stores and retrieves evidence keyed on 𝜎,
not on the raw candidate. Throughout, a signature is the unique key under which evidence is grouped, and a pattern is
the stored record (severity, count, timestamp) that this evidence accumulates into; many events may share one signature
and therefore update one pattern, but a signature identifies at most one pattern per task. Across the three gated tasks,
the signatures are defined as follows.

    • NER signatures are the lowercase-normalised entity string.

    • RE signatures are the uppercase-normalised triple (h_type, 𝑟, t_type) of head category, relation label 𝑟, and tail
      category. For RE we additionally retain the raw head and tail entity strings as auxiliary fields, used only by the
      NER-coverage gate (Section 4.8); these auxiliary fields are not part of the RE signature.
    • QAR signatures are the lowercase-normalised question template plus an error-class disambiguator, introduced
      in the first iteration of the QAR gate (Section 4.8).

3.2. The Verdict Stream
    As the pipeline processes the documents in 𝐷, it emits a stream of verdict events:

      𝑆 = {(𝜎𝑗 , 𝑡𝑗 , 𝑣𝑗 , 𝜏𝑗 , 𝑠𝑗 ) ∶ 𝑗 = 1, … , 𝑀}                                                                    (1)


A.H. Lazem et al.: Preprint submitted to Elsevier                                                               Page 6 of 39
                                                 Dynamic Bidirectional Pattern Memory

where, for the 𝑗-th event, 𝜎𝑗 ∈ Σ𝑡𝑗 is the candidate signature, 𝑡𝑗 ∈ 𝑇 is the task that produced the event, 𝑣𝑗 ∈ 𝑉𝑡𝑗 is the
verdict the verifier (or a rule-based source) assigned, 𝜏𝑗 is the wall-clock timestamp at which the event was recorded,
and 𝑠𝑗 is the signal source label identifying the subsystem that produced the event (for example, the direct verifier, a
rule-based ontology check, or a cross-task propagation path). The source label 𝑠𝑗 selects the source weight 𝑤𝑠 applied
during the memory update (Section 4). The total number of events in the stream is 𝑀. Each rejection event is persisted
to universal_rejections.jsonl as the tuple (uid, stage, entity, reason, conf ): the patient identifier, the pipeline
stage at which the rejection occurred, the rejected entity or candidate, a categorical rejection reason, and the associated
confidence. The exact event counts by stage and reason at production scale are reported in Section 6.1 (Table 7).
    In a static pipeline, each verdict 𝑣𝑗 is consumed once its candidate is accepted or rejected, and the stream 𝑆 is then
discarded. The central design question for DBPM is whether 𝑆 instead contains exploitable structure. Two questions
follow. First, does the verdict distribution conditioned on a signature concentrate as evidence accumulates? Second,
can a memory that estimates this distribution online convert it into gating decisions for future candidates with the same
signature? Section 6 addresses both empirically across several signal sources; the answer differs by source.

3.3. The Inference-Time Memory Problem
    A solution to the inference-time pattern-memory problem maintains, after the 𝑗-th event, a memory state that is
queried at gate time. We require the state to yield, for any signature-task pair (𝜎, 𝑡), a quantitative estimate of how
strongly accumulated evidence opposes a candidate and, optionally, how strongly it supports one. We capture this with
two real-valued functions, indexed by the event count 𝑗:

    • 𝐵𝑗 ∶ Σ × 𝑇 → [0, 1], the blocklist severity: the value 𝐵𝑗 (𝜎, 𝑡) is the severity accumulated against signature 𝜎
      on task 𝑡 after 𝑗 events, with higher values indicating stronger evidence for rejection.

    • 𝑊𝑗 ∶ Σ × 𝑇 → [0, 1], the whitelist confidence: the value 𝑊𝑗 (𝜎, 𝑡) is the confidence accumulated for signature
      𝜎 on task 𝑡 after 𝑗 events, with higher values indicating stronger evidence for acceptance.

    The memory begins with no prior beliefs, 𝐵0 (𝜎, 𝑡) = 𝑊0 (𝜎, 𝑡) = 0 for all (𝜎, 𝑡), and is updated after each event by
an update operator 𝑈 :

      (𝐵𝑗 , 𝑊𝑗 ) = 𝑈 (𝐵𝑗−1 , 𝑊𝑗−1 , 𝜎𝑗 , 𝑡𝑗 , 𝑣𝑗 , 𝜏𝑗 , 𝑠𝑗 )                                                              (2)

where (𝐵𝑗−1 , 𝑊𝑗−1 ) is the memory state before the event, (𝜎𝑗 , 𝑡𝑗 , 𝑣𝑗 , 𝜏𝑗 , 𝑠𝑗 ) is the 𝑗-th verdict event defined in
Equation (1), and (𝐵𝑗 , 𝑊𝑗 ) is the updated state. The choice of 𝑈 , together with the gating policy that consumes (𝐵𝑗 , 𝑊𝑗 ),
must satisfy four practical constraints imposed by the deployment setting.

(C1) Constant-time gating. Querying 𝐵𝑗 (𝜎, 𝑡) and 𝑊𝑗 (𝜎, 𝑡) must complete in (1) amortised time. Gates are queried
      at every candidate-generation event and cannot become a pipeline bottleneck at production throughput.
(C2) Bounded memory size. The signature space |Σ| is unbounded in principle, since NER signatures are arbitrary
      normalised strings; the number of stored signatures must nonetheless remain tractable, and the storage policy
      must admit eviction.
(C3) Bounded values. 𝐵𝑗 (𝜎, 𝑡), 𝑊𝑗 (𝜎, 𝑡) ∈ [0, 1] for all (𝜎, 𝑡) and all 𝑗. Boundedness prevents a single high-frequency
      signature from dominating gating over long deployment horizons.
(C4) Stability under non-stationarity. Clinical documentation conventions evolve across specialties, time periods,
      and institutional sources, so the memory must admit recovery: evidence must attenuate once it ceases to be
      reinforced. As we note here and substantiate in Section 6.1, the choice of decay parameters interacts with the
      distributional shape of the rejection stream. When rejections are diffuse across many signatures, the decay
      window can exhaust an individual signature’s severity before it accumulates to threshold. This interaction is
      the central empirical finding of Section 6.1.

    Together, (C1)–(C4) carve out the design space. The remaining choices, how 𝑈 aggregates evidence, how it
forgets, which signal sources contribute, and how the gating policy converts (𝐵𝑗 , 𝑊𝑗 ) into a decision, are the subject
of Section 4.


A.H. Lazem et al.: Preprint submitted to Elsevier                                                                Page 7 of 39
                                              Dynamic Bidirectional Pattern Memory


Table 2
Notation used throughout Sections 3 and 4. Additional notation (learning rates 𝜂𝑣,𝑡 , source weights 𝑤𝑠 , decay parameters
𝜌𝑣 and ℎ𝑡 , gating thresholds 𝜃𝑡block and 𝜃𝑡down ) is introduced at the points it is needed in Section 4.
                      Symbol                 Meaning
                      𝑥𝑖 , 𝐷, 𝑁              Narrative, corpus, corpus size (𝑁 = 167,034)
                      𝑇 , |𝑇 |               Task set; |𝑇 | = 11 in this deployment
                      𝑡∈𝑇                    Task index
                      𝐺, 𝑉                   Generator (Llama-3.3 70B), verifier (MMed-Llama-3.1 70B)
                       (𝑘)
                      𝑐𝑖,𝑡 , 𝐶𝑖,𝑡 , 𝐾𝑖,𝑡     Candidate, candidate set, count per (𝑖, 𝑡)
                      𝜎 ∈ Σ𝑡 , Σ             Signature, per-task and disjoint-union signature space
                      𝑣(𝑘)
                       𝑖,𝑡 , 𝑉𝑡              Verdict, verdict space for task 𝑡
                      𝜏𝑗                     Wall-clock timestamp of the 𝑗-th event
                      𝑠𝑗                     Signal source label of the 𝑗-th event (selects weight 𝑤𝑠 , §4)
                      𝑆, 𝑀                   Verdict event stream, total event count
                      𝐵𝑗 (𝜎, 𝑡), 𝑊𝑗 (𝜎, 𝑡)   Blocklist severity, whitelist confidence
                      𝑈                      Memory update operator (§4)
                      𝜎0 (𝑣)                 Initial severity for a new signature (§4.2)


3.4. Notation Summary
   Table 2 summarises the notation used throughout Sections 3 and 4. Each symbol is also defined in the text at the
point of first use; the table is provided as a consolidated reference.


4. DBPM Design
    This section specifies the design of DBPM. We organise it around four questions a reader can hold in mind
throughout: how a single verdict updates the memory (Section 4.3), how evidence about one task informs another
(Section 4.4), how the accumulated evidence becomes a gating decision (Section 4.5), and how the memory forgets so
that it tracks changing clinical language (Section 4.6). Two further components follow: a verifier-independent signal
source that populates the relation-extraction channel where the verifier-fed signal does not (Section 4.7), and the
question-answering gate, whose five design iterations are the empirical core of the paper (Section 4.8). Figure 1 shows
where DBPM sits between the generator and verifier, and Algorithm 1 gives the update operator in full.
    The parameter values quoted throughout are read directly from the deployed worker. To keep the body readable, the
in-code identifiers for flags, thresholds, and methods are confined to Appendix A.1; the body names each mechanism
by what it does.

4.1. Early Design Decisions
    DBPM began from the most natural design for an inference-time memory: let the verifier’s own rejections
accumulate by signature, and gate any future candidate whose signature has accumulated enough rejection evidence.
The intuition is direct. If the verifier has rejected a given kind of candidate often enough, the pipeline should stop paying
to re-verify it and should instead flag it on sight. This design has three moving parts, each independently reasonable: an
additive rule that raises a signature’s severity on each rejection, a decay that lowers severity over time so the memory
can recover when clinical language shifts, and a pruning step that discards signatures whose severity has fallen to
negligible levels.
    We deployed this design first and expected it to populate the blocklist at production scale. It did so for two of the
three gated tasks but not for the third, relation extraction, and the reason it failed there (Section 6.1) shaped every
design choice that follows. The verifier-independent signal source of Section 4.7 exists because the verifier-fed source
did not populate the relation-extraction channel; the five iterations of the question-answering gate (Section 4.8) exist
because selectivity, not population, was the binding constraint there. We present the mechanism as deployed, but the
order in which its parts were added was driven by these two empirical failures, and we return to that narrative when
the evidence for it is in hand (Section 6).


A.H. Lazem et al.: Preprint submitted to Elsevier                                                               Page 8 of 39
                                            Dynamic Bidirectional Pattern Memory


Table 3
Per-task verdict learning rates 𝜂𝑣,𝑡 for the three DBPM-gated tasks. The values are fixed at worker initialisation and are
not tuned to the empirical results of Section 6.
                                          Verdict            NER      RE    QAR
                                          hard_fail           0.15   0.20    0.15
                                          soft_downgrade      0.05   0.08    0.05
                                          success             0.03   0.05    0.04


4.2. Parameters
    The mechanism is governed by a small set of constants, all fixed at worker initialisation and none tuned to the
empirical results of Section 6. We introduce each here so that the equations of the following subsections can refer to it
directly. Table 3 and Table 4 collect the two multi-valued sets; the remaining scalars are stated inline.

Learning rates 𝜂𝑣,𝑡 . The learning rate 𝜂𝑣,𝑡 sets how much a single verdict of type 𝑣 on task 𝑡 raises a signature’s
severity (Equation 3). The values appear in Table 3. Relation extraction carries higher rates than the other two tasks
because its verifier emits a graded verdict (PASS_STRONG, PASS_WEAK, FAIL) rather than a binary one, so each relation
verdict carries more information.

Source weights 𝑤𝑠 . Each verdict is scaled by a weight reflecting how much the subsystem that produced it should
be trusted. A direct verifier verdict carries full weight (1.0); a rule-based ontology check carries half (0.5); cross-task
signals, which are indirect by construction, carry less (0.2 to 0.4, by direction). The full set is in Table 4. One source,
a generator self-critique weighted 0.7, is reserved in the code but inactive in every run reported here.

Decay and recovery. Two distinct decay mechanisms operate on different clocks. An in-run multiplicative factor
𝜌𝑣 damps repeated firing of the same signature within a run (𝜌hard_fail = 0.99, 𝜌sof t_downgrade = 0.985). A wall-clock
half-life ℎ𝑡 governs how fast an un-reinforced signature fades across days (ℎNER = 5, ℎRE = ℎQAR = 10 days). The two
are kept separate deliberately: one tracks the event sequence, the other elapsed time. A third constant 𝜌success = 0.998
exists but is never reached on the severity path, since success events update the whitelist and return before the severity
update.

Initial severity 𝜎0 (𝑣). A first-time rejection initialises severity to 𝜎0 (hard_fail) = 0.50 or 𝜎0 (sof t_downgrade) =
0.25, scaled by the source weight.

Gating thresholds. A signature is blocked once its severity exceeds the per-task block threshold 𝜃𝑡block (0.65 NER,
0.70 RE, 0.60 QAR) and it has been seen at least 𝑛min
                                                  𝑡   times (3, 2, 3 respectively). It is downgraded, rather than blocked,
when severity lies in the band between the downgrade threshold 𝜃𝑡down = 0.40 (all tasks) and the block threshold, with
a single observation sufficient.

Storage caps 𝐶𝑡 . At most 𝐶𝑡 signatures are retained per task (200 NER, 300 RE, 150 QAR); when the count is
exceeded, the lowest-severity entries are evicted. The caps were set so the working set fits in process memory at the
deployed throughput.

4.3. Severity Update
    For each signature 𝜎 on task 𝑡, the blocklist stores its current severity 𝜎sev ∈ [0, 1], an observation count 𝑐, the
timestamp 𝜏last of its most recent update, and a cross-task hit counter 𝜅 used in Section 4.4. The whitelist stores a
confidence 𝜎conf ∈ [0, 1] in place of severity.
    A verdict event is routed by its verdict type. A success takes the whitelist path, raising the signature’s confidence
toward a ceiling of 0.99 (initialised at 0.90 on first sighting) and returning without touching severity. A hard_fail or
soft_downgrade takes the blocklist path. For a signature seen for the first time, severity is initialised to the source-
weighted base 𝑤𝑠 ⋅ 𝜎0 (𝑣). For a signature already in memory, the update applies the in-run decay before adding the
new evidence:
                  {                        }
      𝜎sev ← min 1, 𝜌𝑣 ⋅ 𝜎sev + 𝑤𝑠 ⋅ 𝜂𝑣,𝑡 ,        𝑐 ← 𝑐 + 1, 𝜏last ← 𝜏.                                              (3)

A.H. Lazem et al.: Preprint submitted to Elsevier                                                              Page 9 of 39
                                            Dynamic Bidirectional Pattern Memory

    Equation (3) carries the substance of the update rule, and each term earns its place. The decay factor 𝜌𝑣 < 1 stops
a single signature from saturating at the ceiling under repeated firing, which is what purely additive updates would do.
The additive term scales the base learning rate 𝜂𝑣,𝑡 by the source weight 𝑤𝑠 , so an indirect signal moves severity less
than a direct verifier verdict. The outer clip to [0, 1] enforces boundedness (constraint C3 of Section 3.3).

4.4. Cross-Task Propagation
     A rejection on one task is often evidence about another. If the verifier rejects a relation, the entities it joins are
themselves suspect; if it rejects an entity, no relation built on that entity can be sound. DBPM acts on this through
pattern-level cross-task propagation: a rejection on one task records derived evidence on a related task’s memory.
Three directions are active, and their asymmetry is deliberate.
     When a relation is hard-failed, DBPM records a downgrade against each of its head and tail entity strings in the
NER memory, at the cross-task weight and with the increment further halved, because the evidence is twice removed
from a direct NER verdict. A hard-failed question-answer pair propagates the same way to the entities named in its
answer text, at the lowest weight in the system, since long-form answers mix genuine entities with prose. These two
directions are graded: they nudge severity upward without ever, on their own, blocking a candidate. The third direction
is categorical. When an entity is hard-failed at the NER stage, it is added to a preemption set, and any future relation
candidate built on that entity is dropped before the verifier sees it. This direction is all-or-nothing rather than graded
because an entity the verifier has already rejected cannot meaningfully take part in any relation, so a partial signal
would be wasted.
     Four invariants keep propagation safe. Whitelist protection: a signature the verifier has directly confirmed receives
no propagated evidence, so direct confirmation always dominates indirect inference. Propagation cap: once a signature
has received propagated evidence three times (𝜅 ≥ 3), further propagation is suppressed, with 𝜅 itself decaying so the
suppression lifts after sustained quiet. Severity-zone guard: once a signature’s severity reaches 0.55, cross-task evidence
can no longer raise it; indirect evidence may push a signature into the downgrade band but never into the block band on
its own. Recursion prevention: a propagated update is itself ineligible to propagate, which rules out cycles. Together
the last two invariants give the structural guarantee made precise in Section 4.5: cross-task evidence alone cannot block
a candidate.
     These pattern-level directions are distinct from the decision-time cross-task signals used by the difficulty gate and
the NER-coverage gate (Section 4.8), which read cross-task state without writing to it. Pattern-level propagation is
active in every run reported in Section 6; its isolated effect is below the pipeline’s noise floor and is quantified in
Appendix A.7.

4.5. Three-Tier Gating
    The accumulated evidence becomes a decision at three gate sites, one per gated task. For each candidate, the gate
returns one of three verdicts:

                     ⎧ALLOW     if 𝜎 ∈ 𝑊𝑗𝑡
                     ⎪
                     ⎪BLOCK     if 𝑐(𝜎, 𝑡) ≥ 𝑛min and 𝐵𝑗 (𝜎, 𝑡) > 𝜃𝑡block
      gate𝑗 (𝜎, 𝑡) = ⎨                        𝑡                                                                        (4)
                     ⎪DOWNGRADE if 𝑐(𝜎, 𝑡) ≥ 1 and 𝜃𝑡
                                                    down < 𝐵 (𝜎, 𝑡) ≤ 𝜃 block
                                                               𝑗          𝑡
                     ⎪ALLOW     otherwise.
                     ⎩

     The decision is read top to bottom. A signature on the whitelist exits immediately as ALLOW, never reaching the
severity checks; this early exit is why verifier-confirmed candidates are never downgraded (Section 6.5). Otherwise the
signature is blocked if its severity clears the block threshold and it has enough corroborating observations, downgraded
if its severity falls in the band below that threshold, and allowed by default. A blocked candidate is dropped before
the verifier is called. A downgraded candidate proceeds, but its confidence is multiplied by 0.7, a reduction that flows
through relation filtering and graph weighting without removing the candidate. An allowed candidate is untouched.
     Four properties of this policy are worth stating plainly. Whitelist precedence is unconditional: no amount of
accumulated indirect evidence can override a direct success. Minimum support on the block clause means no single
event can block a signature; at least 𝑛min 𝑡    observations must agree, whereas a single observation suffices to flag a
borderline candidate for downgrade. Threshold separation (𝜃𝑡down < 𝜃𝑡block ) leaves a non-empty downgrade band on
every task, so the gate degrades gracefully rather than flipping between block and allow. Direct-evidence requirement


A.H. Lazem et al.: Preprint submitted to Elsevier                                                            Page 10 of 39
                                            Dynamic Bidirectional Pattern Memory

for block follows from the severity-zone guard of Section 4.4: cross-task-only severity is capped at 0.55, below every
task’s block threshold of 0.60 or more, so a candidate reaches BLOCK only if its history includes at least one direct
verifier or rule-based verdict. This is a structural separation, not a tuned heuristic.

4.6. Decay and Pruning
     The in-run decay of Equation (3) handles repeated firing within a run. A second mechanism handles the passage
of time. At each save, every blocklist severity is multiplied by a wall-clock decay term:

      𝜎sev ← 𝜎sev ⋅ 2−Δ𝜏∕ℎ𝑡 ,       Δ𝜏 = 𝜏now − 𝜏last (days).                                                            (5)

A signature that stops being reinforced loses half its severity every ℎ𝑡 days, so the gate follows shifts in clinical
documentation over a long deployment. Equation (5) is the operational form of the recovery constraint (C4 of
Section 3.3). Once a severity falls below 0.01, the signature is pruned. The cross-task counter 𝜅 also decays at each
prune, so a signature that once hit the propagation cap is not quarantined permanently. A per-task storage cap then
evicts the lowest-severity survivors if the count exceeds 𝐶𝑡 .
    This is where the natural design meets its binding condition, and the outcome turns on an interaction between
mechanisms rather than on any single part. Whether a channel populates depends on a race between reinforcement and
decay. If a signature is reinforced faster than it decays, it clears threshold; if it is reinforced more slowly, it is pruned
before it accumulates. Section 6.1 shows that at production scale the relation-extraction channel loses this race, and
that the cause is the distributional shape of the rejection stream rather than its volume.

4.7. The Ontology-Violation Filter
    Section 6.1 establishes that the verifier-fed relation-extraction channel produces no usable patterns at production
scale. The fix is not to change the memory but to change the signal that feeds it. The Ontology-Violation Filter (hereafter
“the Filter") is a deterministic check that fires on every relation candidate, independent of the verifier, flagging any
relation whose head-type, relation, tail-type triple is not admissible under the worker’s clinical ontology:

      ontology_violation(ℎtype , 𝑟, 𝑡type ) ↔
                                                        [                ]                                               (6)
         (ℎtype , 𝑡type ) ∈ PRIORS and alias(𝑟) ∉ PRIORS (ℎtype , 𝑡type ) ,

where PRIORS is a static table of 29 admissible type-triples encoding the ontology, and alias(⋅) is a 32-entry map that
canonicalises verbal variants of a relation (for example, MAY_REVEAL and REVEALS collapse to one label). Both are
fixed at load time, and the comparison is case-normalised.
    A flagged candidate is recorded as a hard failure keyed on its type-triple, with the rule-based source weight, and
persisted through the same decay and pruning machinery as any other blocklist entry. The Ontology-Violation Filter
introduces no new gate: it populates the same relation-extraction blocklist that the existing relation gate already queries,
so the verifier-fed pathway and the Ontology-Violation Filter feed one channel from two independent sources. The
reason it succeeds where the verifier-fed pathway fails is the reason developed in Section 4.6. Because the predicate fires
on a fixed alphabet of type-triples rather than on the open vocabulary of natural-language relation labels, its evidence
concentrates on a handful of signatures and wins the reinforcement-versus-decay race that the diffuse verifier-fed signal
loses.

4.8. The Question-Answering Gate: Five Iterations
    The question-answering gate is the most heavily worked component of DBPM and the empirical heart of the paper.
Here the binding problem was never whether the channel would populate, it did, but whether the gate would be selective:
whether it would flag the candidates the verifier rejects while leaving the rest alone. We tested five signal sources in
turn. Four were not selective, each failing for a structurally different reason; the fifth was. We present them in the order
we tried them, because the sequence is itself the argument: the failures are not a catalogue of mistakes but a map of
which kinds of signal can possibly make such a gate selective.
    The gate fires once per question-answer pair, keyed on the pair’s QAR category (one of eleven QAR categories,
comprising seven general clinical categories, diagnosis, treatment, symptoms, tests, history, observation,
and risk_factor, and four outcome-related categories, outcome_clinicalstatus, outcome_disposition,
outcome_mortality, and adverse_event). The five sources differ only in what they read to make that decision.


A.H. Lazem et al.: Preprint submitted to Elsevier                                                              Page 11 of 39
                                            Dynamic Bidirectional Pattern Memory

First: category-aggregate fail-mass (within-task). The first source totals, per category, the accumulated rejection
mass and flags categories above a threshold. It is anti-selective: the categories it flags are the high-volume ones, not
the error-prone ones, and the verifier does not decide category by category. The failure mode is an aggregation-level
mismatch: the gate decides at the category level while the verifier decides at the pair level.

Second: verifier uncertainty (within-task). The second source reads a per-pair field the verifier sets when its text
output fails to parse, on the hypothesis that this marks uncertainty. The field is almost never set: modern instruction-
tuned models reliably produce parseable output, so the signal is effectively empty at scale. The failure mode is signal
absence: the hoped-for signal does not exist in the data.

Third: per-category fail-rate (within-task). The third source estimates each category’s true fail-rate by dividing
its rejection count by its total:
                                      count FAIL [cat]
      𝑃̂ (FAIL ∣ cat) =                                          ,                                                       (7)
                          count FAIL [cat] + count SUCCESS [cat]

firing a downgrade above a category fail-rate threshold. The fail-rate varies across categories, so the signal is not
degenerate, yet the gate is still anti-selective. The cause is subtle: failures are counted per pair while successes are
counted per question template (roughly eleven templates total), so the denominator and numerator are aggregated at
different units and the estimate overstates the true rate for high-volume categories. The failure mode is a counting
asymmetry: numerator and denominator are tallied at mismatched granularities.

Fourth: per-patient difficulty (cross-task). The fourth source is the first to read cross-task state at decision time. It
combines the category fail-rate with a per-patient difficulty score built from upstream rejection density:

                                                rejections_upstream(patient)
      dif f iculty(patient) =       (                                                   ),                               (8)
                                max rejections_upstream(patient) + ner_yield(patient), 1

where rejections_upstream counts the patient’s NER- and RE-stage verifier rejections and ner_yield counts its verifier-
passed entities. The gate fires a downgrade only when both the category fail-rate and the patient difficulty exceed
their thresholds. It produces no measurable selectivity: the difficulty distributions for verifier-passed and verifier-failed
pairs are statistically indistinguishable. The failure mode is cross-task orthogonality: upstream extraction difficulty
is unrelated to what the verifier judges at the answer stage, which turns on answer content such as hallucination or
over-specification.

Fifth: NER-coverage intersection (cross-task). The fifth source asks a different question, the one the verifier itself
implicitly answers: does the patient have the extracted clinical entities that an answer in this category would need
to be grounded? It checks whether the QAR category being asked about appears among the patient’s accepted NER
categories:

      ner_cats(patient) = { fact.category ∶ fact ∈ accepted_facts(patient) },

and gates accordingly:

                     ⎧ALLOW                          if cat ∈ ner_cats(patient)
                     ⎪
gate(cat, patient) = ⎨DOWNGRADE                      if cat ∉ ner_cats(patient) and the category has a matching NER bucket
                     ⎪fall back to the fourth source otherwise.
                     ⎩
                                                                                                                         (9)

A patient with matching coverage passes; a patient without it is flagged. Nine of the eleven categories have a matching
NER bucket; the two that do not (adverse_event, outcome_mortality) fall back to the fourth source.
    This source was motivated by a read-only test on the development cohort: across qualified categories, a patient
lacking the relevant NER coverage was substantially more likely to have its answer rejected than a patient with it. We


A.H. Lazem et al.: Preprint submitted to Elsevier                                                              Page 12 of 39
                                             Dynamic Bidirectional Pattern Memory


Table 4
Source weights 𝑤𝑠 applied in the severity update (Equation 3). Each weight scales a verdict event by the reliability of
the subsystem that produced it: a direct verifier verdict carries full weight, indirect and cross-task signals carry less. The
self-critique source is reserved in the code but inactive in all runs reported here.

                             Source                 Signal origin                        Weight 𝑤𝑠

                             verifier_mmed          Direct MMed-Llama verdict               1.0
                             rule_based             Ontology / regex check                  0.5
                             cross_task_ner         NER-to-RE preemption                    0.4
                             cross_task_re          RE-to-NER propagation                   0.3
                             cross_task_qa          QAR-to-NER propagation                  0.2
                             cross_task             Generic cross-task fallback             0.5

                             verifier_self          Generator self-critique (inactive)     (0.7)


measure the deployed gate’s selectivity by its lift, the ratio of its flagging rate on verifier-rejected pairs to its flagging
rate on verifier-accepted pairs:
                𝑃 (gate f lags ∣ verif ier = FAIL)
      lif t =                                      ,                                                                     (10)
                𝑃 (gate f lags ∣ verif ier = PASS)
where flagging means a DOWNGRADE or BLOCK verdict. A lift above one means the gate is more likely to flag a
pair the verifier rejects than one it accepts. Section 6.3 reports this lift on both cohorts, along with the per-category
operating envelope and a structural-correctness check; the fifth source is the working design, and the principle that
explains why it works and the other four fail is the subject of Section 7.

4.9. DOWNGRADE-First Measurement Discipline
    Throughout the measurements of this paper, the gate runs in a measurement-instrumented mode that tags suspect
candidates rather than removing them. A class-level flag controls whether the policy emits BLOCK verdicts at all;
when it is off, the BLOCK tier of Equation (4) is suppressed and a candidate that would otherwise be blocked is instead
tagged in its per-pair output without being removed from the pipeline stream. This is the default in every measurement
reported here. The gate therefore records which candidates would be blocked under a hard-blocking configuration,
without committing to the removal.
    The discipline has a direct empirical consequence, developed in Section 6.5: because the NER-coverage gate tags
rather than removes, its ON-versus-OFF ablation arm comparisons produce near-zero pair-count deltas even when
the gate tags thousands of pairs. Selectivity must therefore be read at the gate-tagging level, through the lift ratio of
Equation (10), not from output-volume change. A production deployment that wishes to act on the gate’s verdicts
would enable the hard-blocking configuration, converting each tag into a BLOCK; the in-code flag for this is given in
Appendix A.1.

5. Experimental Setup
    This section specifies the dataset, the evaluation cohort, and the ablation protocol used to evaluate DBPM. The
design goal of the protocol is to isolate the contribution of each DBPM component through controlled paired ablations
on a single locked 5,000-patient cohort, and to separately characterise the verifier-fed channel at full 167,034-patient
production scale. Hardware and software configuration, the resume protocol, and the in-code flag mappings are given
in Appendix A.1; a single consolidated summary of every fixed setting appears in Table 14.

5.1. Dataset
    Evaluation uses the multi-task derivative of the PMC-Patients corpus that the pipeline produces. The source corpus
is PMC-Patients (Zhao et al., 2023), a publicly released collection of 𝑁 = 167,034 patient case reports drawn from
PubMed Central full-text articles. The pipeline loads and processes the corpus end to end, converting each narrative
into a structured record carrying the eleven task-bucket outputs of Section 3.1, of which three (NER, RE, QAR) are
DBPM-gated and feed the analysis of this paper.

A.H. Lazem et al.: Preprint submitted to Elsevier                                                               Page 13 of 39
                                             Dynamic Bidirectional Pattern Memory


Table 5
Full-run production characterisation on the 167,034-patient corpus, with all values aggregated from the deployed run’s
per-patient metrics and final memory state. The run spanned approximately twelve days (4–16 May 2026). The relation
rejection count (785,797) and the empty relation blocklist are analysed in Section 6.1; the high relation precision (0.994)
reflects the permissive-verifier regime discussed in Section 8.2.
                                  Quantity                                              Value
                                  Corpus and throughput
                                  Patient narratives processed                         167,034
                                    human / veterinary                        163,400 / 3,634
                                  Elapsed wall-clock duration                         ∼12 days
                                  Mean end-to-end time per patient                      102.9 s
                                    NER / RE / QAR stage means             24.6 / 14.7 / 43.1 s
                                  Extraction yield (corpus totals)
                                  Named entities                                     4,471,110
                                  Candidate relations                                4,915,334
                                  Relations accepted to enriched output              4,129,537
                                  Question–answer pairs                              1,035,199
                                  Verifier rejections and persistence
                                  Relation rejections (classifier stage)               785,797
                                  Persisted relation blocklist patterns                      0
                                  Persisted NER / QA patterns                       5,860 / 11
                                  Precision (corpus means)
                                  Relation precision                                     0.994
                                  Verifier precision                                     0.945
                                  Final-output precision                                 0.888
                                  Mean entity coverage                                   0.773



The held-out 5,000-patient cohort. The three paired ablations of Section 5.2 share a single 5,000-patient subsample,
drawn once from the full corpus by stratified random sampling and then fixed across every ablation arm so that ON-
versus-OFF comparisons are patient-aligned. The cohort is stratified along three dimensions: age bucket (0–17, 18–39,
40–64, 65+, plus an explicit unknown bucket for missing or unparseable ages), gender (F, M, unknown), and document-
length tertile computed from the full corpus, with cut points T1 ≤ 1,931 characters < T2 ≤ 3,121 characters < T3. The
three-dimensional grid yields 24 non-empty strata.
     The deployed pipeline processed the entire 167,034-patient corpus end to end over approximately twelve days;
Table 5 characterises this full production run, the aggregate yields, throughput, and precision against which the ablation
cohort below is drawn. Of these narratives, 163,400 are human case reports and 3,634 are veterinary; we retain both,
since the gating mechanism operates on extraction structure rather than on any species-specific content, but note that
the corpus is not exclusively human.
     Sampling proceeds in two stages. Let 𝑛target = 5,000 be the target cohort size and 𝑛strata = 24 the number of non-
empty strata. Each non-empty stratum first receives a minimum floor allocation of min(10, max(1, 𝑛target ∕(2 𝑛strata )))
patients, capped by the stratum’s population, so that rare strata remain visible. The remaining sample size is then
distributed proportionally to each stratum’s residual population above its floor, with rounding remainders assigned to
the largest-deficit strata so the total reaches exactly 𝑛target = 5,000. Selection within a stratum is uniform random
without replacement, seeded for reproducibility, and the final identifier list is shuffled to randomise processing order.
     The resulting cohort mirrors the demographic skew of the source corpus: the five largest strata all fall in the 40–64
age bucket and together contribute roughly a third of the cohort, with the 18–39 female bucket dominating the next tier.
Because the same cohort is reused across all arms, this skew is held constant and does not confound the paired com-
parisons. The full stratum allocations, tertile cut points, and identifier list are released as ablation_5k_uids.json.
     Every gated-task output is verifier-attested: candidates that fail verification are logged to universal_rejections
.jsonl with stage and reason metadata, so the dataset records the complete candidate-and-verdict stream that
drives DBPM. At production scale, this stream contains 1,367,615 events; the per-stage breakdown (Table 7) and
its interaction with the persistence layer are reported in Section 6.1.



A.H. Lazem et al.: Preprint submitted to Elsevier                                                            Page 14 of 39
                                            Dynamic Bidirectional Pattern Memory


Table 6
The four evaluation configurations. Rows 1–3 are paired ablations on the held-out 5,000-patient cohort, each isolating one
DBPM component. Row 4 is a production-scale cross-check on the full 167,034-patient corpus, not a paired comparison.
Flag names are the literal switches toggled, given here for reproducibility; their concept mapping is in Appendix A.1.
            #       Configuration                   What is tested                What is held constant
            1       Ontology Filter ON vs           The     Ontology-Violation    Held-out cohort; NER-coverage
                    OFF (BPM_DISABLE_M3)            Filter (Section 4.7)          gate ON in both arms; pattern-
                                                                                  level propagation active in both
                                                                                  arms
            2       NER-coverage gate ON vs         The NER-coverage inter-       Held-out cohort; Ontology Fil-
                    OFF (M1V7_ENABLE)               section gate (Section 4.8)    ter ON in both arms; difficulty
                                                                                  gate as fallback in both arms
            3       DBPM full ON vs full            All new DBPM compo-           Held-out cohort; legacy _ner_-
                    OFF (BPM_DISABLE mas-           nents simultaneously          block / _re_block checks ac-
                    ter switch)                                                   tive in both arms
            4       167K production       cross-    Population of the verifier-   Full 167,034-patient corpus;
                    check                           fed RE channel at deploy-     deployed DBPM-full configura-
                                                    ment scale                    tion


5.2. Ablation Protocol
    We evaluate DBPM through four configurations, summarised in Table 6. The first three are paired ablations on
the held-out 5,000-patient cohort, each isolating one component by toggling a single flag while holding the rest of
the system fixed. The fourth is a production-scale cross-check on the full corpus, not a paired comparison: it exists
to characterise whether the verifier-fed relation-extraction channel populates at deployment scale, which is a property
only visible at full volume.
    Each paired ablation records three families of measurement per arm: task-level pair counts (per-stage candidate
counts and verifier pass/fail counts for NER, RE, and QAR); DBPM-specific metrics (per-task BLOCK / DOWN-
GRADE / ALLOW counts, pattern-level cross-task propagation count, and whitelist and blocklist sizes by severity
bucket); and system metrics (per-stage runtime, candidate-rejection rate by stage, and end-to-end patient-processing
time).
    All four configurations run under the DOWNGRADE-first measurement discipline of Section 4.9: the gate tags
candidates in the output without removing them from the stream. Selectivity is therefore measured at the tagging level,
via the lift ratio of Equation (10), and provenance is measured by the count of gate-tagging events relative to total
pipeline pair throughput, rather than by output-volume change.
    One further component, pattern-level cross-task propagation (Section 4.4), is active in the deployed configuration
but is not among the four configurations above. Its isolated effect is measured by a separate paired ablation (cross-
task propagation ON vs OFF) reported in Appendix A.7. We keep it out of the main protocol because its measured
contribution, a pair-count delta of 0.098% of pipeline throughput, falls below the pipeline’s per-stage non-determinism
floor and so carries no main-results weight.


6. Results
    This section reports what the data supports and discusses its limitations. The paper is a methodological characteri-
sation of DBPM as an inference-time pattern-memory gating mechanism: which signal sources populate its channels,
which gate designs are selective and which fail, and what structural pattern emerges across the design space. Dataset-
quality evaluation of DBPM’s outputs (human-rated true-positive rates, downstream clinical-correctness scoring) is
the subject of separate forthcoming work on the resulting corpus and is excluded from this paper’s claims.
    The findings rest on four empirical anchors: a production-scale run revealing the structural absence of verifier-
fed signal accumulation (Section 6.1); a paired ablation of the Ontology-Violation Filter on the held-out cohort
(Section 6.2); a dissection of the five question-answering gate signal sources, with development-cohort replication
(Sections 6.3 and 6.4); and a confirmation that DBPM operates by tagging rather than suppression (Section 6.5).


A.H. Lazem et al.: Preprint submitted to Elsevier                                                                Page 15 of 39
                                              Dynamic Bidirectional Pattern Memory


Table 7
Rejection-stream composition at 167,034-patient production scale. Each event is persisted to universal_-
rejections.jsonl as the tuple (uid, stage, entity, reason, conf). The Stage-3 classifier and Stage-4 QA verifier dominate;
the Stage-1 gatekeeper rejections are ontology-mismatch events across clinical categories. The 785,797 Stage-3 classifier
rejections are the relation-pathway events that, despite their volume, did not persist into the verifier-fed blocklist channel.

                         Stage                      Rejection reason                          Events

                         Stage 3 (Classifier)       SOTA_Classify_None                       785,797
                         Stage 4 (QA verifier)      QA_Verifier_Reject                       548,093

                         Stage 1 (Gatekeeper)       Ontology_Mismatch_Diagnosis               20,246
                                                    Ontology_Mismatch_Tests                   10,105
                                                    Ontology_Mismatch_Risk_Factor              2,061
                                                    Ontology_Mismatch_History                  1,244
                                                    Ontology_Mismatch_Observation                 21
                                                    Ontology_Mismatch_Outcome                      1

                         Stage 1 (Verifier)         NER_Verifier_Reject                            33
                         Stage 1 (Rescue)           Rescued_By_Confidence                          14

                         Total                                                             1,367,615



6.1. Production-Scale Failure of the Verifier-Fed Channel
    The most natural design, accumulating the verifier’s own rejections by relation signature and gating on the
accumulated evidence, did not populate at production scale. The deployed run processed the full 167,034-patient corpus
over approximately twelve days of elapsed wall-clock time (4–16 May 2026), spanning several resubmitted SLURM
allocations (Appendix A.4), and its full characterisation is given in Table 5. At the end of the run, the verifier-fed
relation-extraction blocklist held no patterns at all: the relation channel was absent from the persisted memory state,
not merely below its threshold of count ≥ 2 and severity > 0.70. The named-entity and question-answering channels,
by contrast, populated normally over the same run, holding 5,860 and 11 patterns respectively in the final state.
    This empty channel is the more striking because the same run produced a large volume of relation rejections. Of
the 4,915,334 candidate relations the generator emitted, 785,797 were rejected, logged as Stage-3 classifier events on
the relation-extraction pathway (Table 7). The channel that should have accumulated these rejections recorded none of
them.

Two senses of “rejection,” and why the distinction is the finding. The reconciliation of 785,797 rejections with
zero persisted patterns is not a discrepancy; it is the mechanism. The 785,797 figure counts classifier-stage rejection
events on the candidate stream. These are distinct from memory-fail events, the rejections that the persistence layer
actually consolidates into a stored signature. In the deployed run the relation memory’s fail counter remained at zero: no
rejection was ever consolidated, so no signature was ever created, so the channel stayed empty. The rejections existed
in abundance on the stream; they simply never became persistable memory.
     The cause is the interaction of three persistence-layer mechanisms, each individually sensible (Section 4.6): per-
signature aggregation under the head-type, relation, tail-type key; wall-clock severity decay with a ten-day half-life
on relation patterns (Equation 5); and prune-on-save below a severity floor of 0.01. Because DBPM state persists
across the resubmitted allocations and the decay advances on real UTC time rather than compute time (Appendix A.4),
the relevant clock is the run’s full twelve-day span, over which the ten-day half-life fires roughly once. Across that
window, relation rejections recurred too infrequently per signature relative to the decay: each signature’s severity
decayed between save events faster than reinforcement arrived, so signatures fell below the floor and were pruned
before they could accumulate. A signature reinforced rarely never survives long enough to clear threshold, no matter
how many rejections occur in total, because they are spread across too many distinct signatures.
     The other two gated channels received more concentrated per-signature traffic and populated normally at the same
final snapshot, the question-answering channel holding 11 records and the named-entity channel 5,860. The collapse
is therefore specific to the relation channel’s rejection distribution, not a property of the persistence layer in general:

A.H. Lazem et al.: Preprint submitted to Elsevier                                                                Page 16 of 39
                                            Dynamic Bidirectional Pattern Memory

the identical decay-and-prune machinery that emptied the relation channel left the other two intact. Figure 2 contrasts
the input volume against the persisted output state.
    The finding generalises beyond this pipeline. Any inference-time memory that accumulates per-signature statistics
over free-form LLM output is exposed to the same diffusion: when the output vocabulary is open, rejections spread
across too many distinct signatures for any one to be reinforced faster than it decays, and the channel stays empty
regardless of total volume. The mitigation is to change the signal source so that events concentrate on a bounded
alphabet, which is exactly what the Ontology-Violation Filter of Section 4.7 (evaluated next) does.

6.2. The Ontology-Violation Filter: A Verifier-Independent Source
   We evaluate the Ontology-Violation Filter on the held-out cohort under a paired ON/OFF ablation, with the NER-
coverage gate held ON in both arms and the system in DOWNGRADE-first mode.

Suppression magnitude. The Filter silently suppressed 𝑁 = 1,207 relation candidates (0.98% of total): the ON arm
carried 122,253 relations against 123,460 in the OFF arm, all 1,207 removed through the verifier-independent pathway.
Where the verifier-fed pathway produced zero usable patterns at production scale (Section 6.1), the Filter populates
the same downstream blocklist through an independent signal source that sidesteps the persistence-decay interaction.
Figure 3 shows the six threshold-clearing patterns.

Mechanism stability. The same six type-triple patterns recur on the held-out cohort with the same rank-
ordering and proportional frequencies as on the development cohort (tests-associated_with-diagnosis,
symptoms-manifests-diagnosis,                symptoms-causes-diagnosis,              treatment-prevents-symptoms,
history-associated_with-diagnosis, diagnosis-associated_with-history). The total event count
grows from 2,486 on the development cohort to 49,734 on the held-out cohort, a 20.0× increase over a 25× increase
in patients. This sub-linear growth is the signature of a signal concentrating on a fixed type-triple alphabet rather than
dispersing. Each pattern is, by construction, a type-triple the ontology disallows; whether individual suppressions
improve dataset quality is a downstream question outside this paper’s scope.

No precision-proxy or runtime delta. The verifier passed essentially every relation reaching enriched output in both
arms (precision proxy 1.0000 in each), and the wall-time difference was 26 seconds across runs of roughly nine hours
(0.08%, within noise). The Filter’s contribution is therefore upstream candidate suppression through an independent
signal source, not a downstream precision gain, in a regime where the verifier itself is permissive.

A note on provenance. The 1,207 suppressions here are the Filter’s isolated contribution, measured against an
OFF arm that kept the NER-coverage gate ON. The combined ablation of Section 6.5 reports a smaller figure of
913 because its OFF arm disables every DBPM mechanism, including the NER-coverage gate. Both are correct; they
answer different questions, and we return to the distinction in Section 6.5.

6.3. Five Signal Sources for the Question-Answering Gate
     We tested five candidate signals for the question-answering gate, that is, five different quantities the gate could read
to make its decision, in the order introduced in Section 4.8. Four are not selective, each failing for a structurally distinct
reason; the fifth, the NER-coverage gate, is selective within its operating envelope. Figure 4 plots the selectivity lift of
all five.

Category-aggregate fail-mass. The first source totals each category’s accumulated rejection mass and flags
categories above a threshold. On the development cohort, its lift was 0.006 across 𝑁 = 2000 pairs: not merely non-
selective but anti-selective, tagging categories roughly 170× less likely to be verifier-rejected than untagged ones. The
cause is an aggregation-level mismatch: the signal decides at the category level whereas the verifier decides per pair,
so it flags whichever categories accumulate volume rather than those that are error-prone.

Verifier uncertainty. The second source reads the per-pair field the verifier sets when its output fails to parse,
hypothesised to mark uncertainty. Across 1,283 development-cohort pairs, no event carried an ambiguous value:
the signal does not exist at this scale. This is a case of signal absence: the field is a parse-failure flag, and modern
instruction-tuned models almost never produce unparseable output, so it is left unset.



A.H. Lazem et al.: Preprint submitted to Elsevier                                                               Page 17 of 39
                                                    Dynamic Bidirectional Pattern Memory

Per-category fail-rate. The third source estimates each category’s true fail-rate (Equation 7) by joining rejection
and success records, firing a downgrade above a fail-rate threshold. The fail-rate genuinely varies across categories
(spread 0.52 on the held-out cohort, 0.58 on the development cohort, so the signal is non-degenerate), yet the gate’s
instance-level lift was only 0.05. The cause is a counting asymmetry: failures are counted per pair while successes are
counted per question template (about eleven templates total), so the estimate overstates the true rate for high-volume
categories and the gate tags categories whose individual pairs mostly pass.

Per-patient difficulty. The fourth signal, the first to read cross-task state at decision time, combines the category
fail-rate with a per-patient upstream-difficulty score (Equation 8) and fires only when both exceed threshold. Its lift
was 0.00, a failure we attribute to cross-task orthogonality: the PASS-side and FAIL-side difficulty distributions are
statistically indistinguishable (medians 0.179 versus 0.174, means 0.188 versus 0.191, third quartiles 0.290 versus
0.294). Upstream extraction difficulty simply does not predict verifier rejection at the answer stage, which turns on
answer content such as hallucination or over-specification.

NER-coverage intersection. The fifth source asks whether the patient has the extracted entities an answer in the
asked category would need (Section 4.8). It was motivated by a read-only test on the development cohort: across
six qualified categories, a patient lacking the relevant coverage was a median 3.43× more likely to have its answer
rejected than a patient with it. The deployed gate allows covered patients and downgrades uncovered ones, across the
nine categories with a matching NER bucket; the two without a bucket (adverse_event, outcome_mortality) fall
through to the difficulty gate.
    On the development cohort, the gate’s path lift across the nine mapped categories was 1.89 (tagging 0.386 of FAIL
pairs against 0.205 of PASS pairs); the two unmapped categories contributed a fallback lift of 0.00, giving a global lift
of 1.59. On the held-out cohort, the path lift was 1.84 (0.360 of FAIL against 0.196 of PASS, over 𝑛FAIL = 3,868 and
𝑛PASS = 31,135 mapped-category pairs),1 with the same 0.00 fallback giving a global lift of 1.52. The path lift therefore
holds across the 25× scale-up to within roughly 4% (1.89 to 1.84), although the underlying tagging probabilities move
somewhat more, which we note rather than overclaim.
    The held-out path lift is statistically significant. We obtain its 95% confidence interval from the delta-method
variance for the log of a risk ratio,
                             1 − 𝑃tag|FAIL            1 − 𝑃tag|PASS
       ̂
       Var[log lif t] =                         +                        ,
                           𝑛FAIL ⋅ 𝑃tag|FAIL        𝑛PASS ⋅ 𝑃tag|PASS

which gives [1.75, 1.93]; the null hypothesis of no selectivity (lif t = 1) is rejected decisively (𝑝 < 10−15 ). This interval
captures within-run sampling precision only; run-to-run and configuration-dependent variation is reported separately
in Section 8.3.
    Mechanism integrity. Of the 17,703 covered-PASS pairs in mapped categories on the held-out cohort, zero were
tagged, a structural-correctness check confirming that covered pairs hit the early-ALLOW exit and never reach the
downgrade branch. The development-cohort check (726 covered-PASS pairs, zero tagged) replicates this at 25× smaller
scale.

Why the fifth source succeeds where the first four fail. The four failures are not a ladder of increasing
sophistication that eventually works; the second and fourth sources are more elaborate than the first and fail more
conclusively. They fail because each reads the wrong input. The first and third base their decision on category-level
statistics, but the verifier decides per pair. The second reads a signal that does not exist at scale. The fourth reads
upstream difficulty, which is orthogonal to what the verifier judges. The fifth reads whether the patient has the entities
an answer would need to be grounded, which is the same question the verifier implicitly resolves. The structural pattern
is the subject of Section 7.1: a pre-generation signal is selective for verifier rejection only when it directly probes the
answer-grounding question the verifier itself evaluates.

6.4. Per-Category Operating Envelope
    The headline path lift of 1.84 averages over substantial per-category variation; selectivity is far from uniform across
the eleven categories. Table 8 gives the full breakdown and Figure 5 visualises it. Four operating regimes emerge.
    1 The lift uses 𝑛
                     PASS = 31,135, every PASS pair evaluated by the gate. A second count, 17,703 covered-PASS pairs, appears later in this section
and restricts to PASS pairs whose patient-level NER set covers the category; the two are not interchangeable.


A.H. Lazem et al.: Preprint submitted to Elsevier                                                                                  Page 18 of 39
                                            Dynamic Bidirectional Pattern Memory


Table 8
Per-category selectivity of the NER-coverage gate on the held-out cohort (single-run measurement; per-category lifts for
categories with small 𝑛FAIL are subject to run-to-run variance, discussed at the end of this subsection). The coverage
column is the percentage of PASS pairs whose patient-level NER set covers the category. Categories with no NER bucket
fall through to the difficulty gate. “Regime” is the operating-envelope classification described in the body.
      Category                        𝑛PASS    𝑛FAIL           cov%    𝑃 (𝑡 ∣ 𝑃 )   𝑃 (𝑡 ∣ 𝐹 )          lift   regime
      diagnosis                       4,764     105             95.7      0.043        0.733        17.13      selective
      risk_factor                       564     448             53.7      0.463        1.000          2.16     selective
      outcome_clinicalstatus          3,191     448              4.4      0.956        1.000          1.05     categorical
      outcome_disposition             2,235     419              1.7      0.983        1.000          1.02     categorical
      outcome_mortality                 697     351    0.0 (no-NER)       0.149        0.000          0.00     fallback
      adverse_event                   2,517     443    0.0 (no-NER)       0.113        0.000          0.00     fallback
      history                         1,971     433             42.8      0.000        0.000     undefined     no tagging
      observation                     2,979     416              1.3      0.000        0.000     undefined     no tagging
      symptoms                        3,944     303             96.8      0.000        0.000     undefined     saturated
      treatment                       4,143     260             97.7      0.000        0.000     undefined     saturated
      tests                           4,130     242             94.8      0.000        0.000     undefined     saturated


Selective (lift > 1.5). Two categories separate PASS from FAIL. diagnosis (lift 17.13) is the strongest: at 95.7%
coverage the gate tags 73.3% of FAIL pairs against only 4.3% of PASS pairs, a clean separation driven by a small,
well-separated FAIL stratum (105 FAIL against 4,764 PASS). risk_factor (lift 2.16) sits in the mid-coverage regime
the gate was designed for: at 53.7% coverage it tags every FAIL pair and 46% of PASS pairs. Notably, diagnosis is
anti-selective when the fifth source is ablated in isolation but becomes the most selective category under full DBPM,
because the Ontology-Violation Filter removes ontology-violating relations that would otherwise inflate the coverage
signal for diagnosis questions; cleaning the upstream relations sharpens the signal. We examine this interaction in
Section 7.1.

Categorical (lift ≈ 1.0). Two outcome categories, outcome_clinicalstatus (coverage 4.4%, lift 1.05) and
outcome_disposition (coverage 1.7%, lift 1.02), tag nearly all PASS and all FAIL pairs at near-zero coverage,
behaving as coarse always-on category filters rather than per-patient gates. They are not selective, but their behaviour
is predictable.

No tagging or saturated. Five of the general clinical categories, history, observation, symptoms, treatment,
and tests, tag nothing. For symptoms, treatment, and tests, coverage is saturated (95–98%), so nearly every
patient is covered and the gate allows almost everyone. For history (coverage 42.8%) and observation (coverage
1.3%), the gate simply does not fire on this cohort. The mechanism operates correctly but rarely activates.

Fallback (no NER bucket). adverse_event and outcome_mortality have no matching NER bucket, so the fifth
source cannot apply and the difficulty gate runs, tagging PASS pairs only (𝑃 (𝑡 ∣ 𝐹 ) = 0).
    The net picture is an operating envelope rather than a uniform effect: strong per-patient selectivity in two categories,
coarse categorical filtering in two, no measurable tagging in five, and no application in two. The gate is selective in
the mid-to-high-coverage regime where the coverage signal separates the PASS and FAIL strata, and degenerates
predictably outside it. Identifying these conditions is itself a methodological contribution.

Per-category instability for small FAIL strata. The per-category lifts for categories with small FAIL strata
(diagnosis, 𝑛FAIL = 105; the outcome categories, 𝑛FAIL ≤ 451; adverse_event, 𝑛FAIL = 447) are subject to run-to-
run noise. An independent replication under the full-DBPM configuration (the cross-task ablation arm, Appendix A.7)
gave a path lift of 1.71, within the 1.52–1.84 band, but the per-category diagnosis lift swung between near-zero
and large positive values across runs and configurations of the same gate. We caution against drawing per-category
conclusions from any single run: the aggregate path lift is stable, the per-category lifts on small strata are not. The
regime-level classification (selective, categorical, saturated, fallback) is robust across runs even where the precise
within-regime lifts vary.

A.H. Lazem et al.: Preprint submitted to Elsevier                                                                  Page 19 of 39
                                            Dynamic Bidirectional Pattern Memory


Table 9
Pair-count deltas between the full-DBPM ON and OFF arms on the held-out cohort. The named-entity (+0.19%) and QA
(−0.03%) deltas are within the per-stage non-determinism floor, confirming that the NER-coverage gate tags QA candidates
without removing them. The relation delta (−913, −0.74%) is the Ontology-Violation Filter’s genuine suppression, the only
above-noise pair-count change.
                                       Stage            ON         OFF       𝚫         𝚫%
                                       NER          133,790     133,533   +257     +0.19%
                                       RE           122,425     123,338   −913     −0.74%
                                       QAR           31,135      31,143     −8     −0.03%


Table 10
Tagging summary on the held-out cohort (DBPM-full ablation) across all eleven QA categories. Rows are the verifier’s
verdict; columns are the gate’s tag (DOWNGRADE collapsed with BLOCK as tagged ). Percentages are within-row, the
fraction of each verdict class that the gate tags, so each row sums to 100%. The table reports selectivity, not classification
accuracy: the gate is a selective tagger on a single grounding signal, not a verifier surrogate, so the relevant quantity is
the ratio of the two tag rates (the lift), not precision, recall, or F1. The gate tags 36.0% of verifier-FAIL pairs against
19.6% of verifier-PASS pairs, a lift of 0.360∕0.196 = 1.84 (95% CI [1.75, 1.93]). Tagging in the nine mapped categories is
produced by the NER-coverage gate; the two no-bucket categories (adverse_event, outcome_mortality) are tagged by
the difficulty gate, which contributes no FAIL-side tags, so the all-category ratio equals the mapped-category path lift, an
equality specific to these data, not a general identity.
                             Verifier verdict                 Tagged      Not tagged      Row total
                             FAIL                   1,392 (36.0%)       2,476 (64.0%)         3,868
                             PASS                   6,101 (19.6%)      25,034 (80.4%)        31,135
                             Column total                      7,493             27,510     35,003


6.5. Tagging, Not Suppression: Measurement Discipline and Provenance
    Under the DOWNGRADE-first discipline, the NER-coverage gate tags pairs without removing them, so the gate
produces almost no change in pair counts even while tagging thousands of pairs. Table 9 shows the pair-count deltas
and Figure 6 contrasts them against the tagging volume.
    The gate tagged 6,101 verifier-PASS QA pairs in the ON arm against zero in the OFF arm (where the master switch
deactivates every mechanism), so all 6,101 PASS-side tags are attributable to DBPM. With the 1,392 FAIL-side tags,
7,493 QA pairs are tagged in total, the basis of the confusion summary in Table 10. Against this tagging volume,
the near-zero pair-count deltas confirm the design intent: selectivity must be read from tagging behaviour, not output
volume.

Aggregate DBPM provenance (single combined ablation). A single paired ablation toggles all new DBPM
mechanisms together via the master switch. On the same held-out cohort it produced 913 silent relation suppressions by
the Ontology-Violation Filter (ON arm 122,425 relations against 123,338 in the OFF arm) and 6,101 attributable QA
downgrade-tags by the NER-coverage gate (against zero when the switch is off). Together these are 7,014 gating events
across the 287,350 pipeline pairs of the ON arm, or 2.44% of pipeline pairs touched by the new DBPM mechanisms.
    The combined-ablation suppression count of 913 differs from the isolated count of 1,207 (Section 6.2) because
the two ablations differ in both arms, not only the OFF arm: the isolated ablation holds the NER-coverage gate ON
in both arms and measures only the Filter, whereas the combined ablation turns every mechanism off together, which
shifts the relation pair counts in both arms as well. The two numbers are not in conflict; each is the right answer to a
different question. The combined figure of 913 answers “What is DBPM’s aggregate contribution against an ungated
baseline?”; the isolated figure of 1,207 answers “What is the Filter’s contribution holding everything else constant?”
    At this scale, the allow-set dominates the blocklist: the named-entity channel holds 96,708 whitelisted signatures
against 2,991 blocklist patterns, and the QA channel holds 11 whitelisted signatures against 34 blocklist patterns. This
dominance is consistent with the early-ALLOW exit of Equation (4): most candidates match a known-safe signature
and bypass belief-based gating.



A.H. Lazem et al.: Preprint submitted to Elsevier                                                               Page 20 of 39
                                             Dynamic Bidirectional Pattern Memory


Table 11
The five signal sources tested for the question-answering gate, characterised by what each read, its granularity, the empirical
outcome, and the failure mode where applicable. The NER-coverage gate is the working design; its path lift band of 1.52–
1.84 is measured across four independent replications (Section 8.3).
     Source                 Signal read                Granularity      Outcome                 Failure mode
     Category-              category-aggregate         category-level   anti-selective (lift    aggregation-level
     aggregate      fail-   verifier fail-mass                          0.006)                  mismatch
     mass
     Verifier               verifier   parse-failure   per-pair         signal absent           signal absence
     uncertainty            flag
     Per-category fail-     per-category fail-rate     category-level   anti-selective (lift    counting asymmetry
     rate                   (dual-bucket)                               0.05)
     Per-patient diffi-     per-patient upstream       per-patient,     no signal       (lift   cross-task orthogonality
     culty                  difficulty                 cross-task       0.00)
     NER-coverage in-       per-patient     NER-       per-patient,     selective (path lift    working design
     tersection             category coverage          cross-task       1.52–1.84 across
                                                                        four replications)


Runtime overhead. The ON arm ran in 8h48m10s (6.34 s/patient) and the OFF arm in 8h48m50s (6.35 s/patient), a
difference of 40 seconds across 31,690, or 0.13%. This is below the pipeline’s per-patient variance floor (expected noise
on the mean across 𝑛 = 5000 is roughly ±140 seconds; continuous batching, the dual-model verifier, and network jitter
contribute 1–3 seconds of per-patient standard deviation). We therefore claim only that the gate’s per-patient overhead
is below the variance floor, not that it produces a speed-up.
    Two consequences follow for downstream consumers. First, DBPM’s gate is measurement-instrumented rather
than production-suppressive: it records which pairs would be blocked under hard-BLOCK mode without committing
to the removal, and a deployment wishing to act on its verdicts would enable hard-BLOCK mode (Section 4.9). Second,
in Table 9 the named-entity and QA deltas are within non-determinism, and the relation delta of −913 is the Filter’s
suppression, not a gate effect; the gate itself, in DOWNGRADE-first mode, removes no pairs. Conclusions from DBPM
ablations must therefore be drawn at the tagging level, not from pair-count deltas.

Provenance scope. The 2.44% figure comes from a single master-switch ablation on the locked cohort, measuring the
aggregate contribution of the two new mechanisms against an ungated baseline on identical input. Pattern-level cross-
task propagation is disabled in both arms by the master switch; its independent contribution is measured separately in
Appendix A.7 at 0.098% of pipeline throughput, below the per-stage non-determinism floor.


7. Discussion
    This section sets out what the results of Section 6 establish about inference-time pattern-memory gating in LLM-
grounded clinical NLP. We organise it around three questions: what the five-source dissection of the question-answering
gate reveals as a structural principle (Section 7.1); how the production-scale failure of the verifier-fed channel changes
the design problem for downstream pipelines (Section 7.2); and what follows for the safe deployment of LLM-driven
extraction at scale (Section 7.3).

7.1. A Structural Principle for Selective Pre-Generation Gating
     The five-signal dissection of the question-answering gate (Sections 4.8 and 6.3) is enough to state a structural
principle about which signals can make inference-time gating selective in a generator-verifier architecture. In each of
the first four gate variants, the gate read a structurally distinct signal and failed for a structurally distinct reason; the
fifth succeeded by reading a signal none of the others did. Table 11 lays out the progression.
     Read across the five, the pattern is not that more sophisticated mechanisms win. The second and fourth sources are
more elaborate than the first, and they fail more conclusively. The pattern is that a pre-generation signal is selective
for verifier rejection only when it directly probes the answer-grounding question the verifier itself evaluates. The first
and third gate variants test a category-level statistic, the accumulated fail-mass or fail-rate of the whole category, but

A.H. Lazem et al.: Preprint submitted to Elsevier                                                                   Page 21 of 39
                                            Dynamic Bidirectional Pattern Memory

the verifier accepts or rejects each pair individually, so a category-level signal cannot separate the pairs the verifier
distinguishes within that category. The second variant checks a parse-failure flag, on the assumption that unparseable
output marks an uncertain verdict, but modern instruction-tuned models almost always produce parseable output, so
the flag is essentially never set and carries no information. The fourth variant checks how much upstream extraction
the patient required, on the assumption that hard-to-extract patients yield worse answers; but the verifier judges the
answer’s own content, whether it is hallucinated, over-specified, or unsupported by the source text, and this is unrelated
to upstream extraction difficulty. We confirmed the two are unrelated directly: the upstream-difficulty scores of verifier-
passed and verifier-failed pairs are statistically indistinguishable (Section 6.3). The fifth variant checks whether the
patient has the extracted clinical entities that an answer in the asked category would need, which is the same question
the verifier resolves when it decides whether an answer is grounded. That alignment between the gate’s signal and the
verifier’s decision criterion is what makes the fifth variant selective.
    The principle is directly usable. A practitioner designing an inference-time gate for a generator-verifier pipeline can
test a candidate signal by asking whether it probes the same question the verifier answers. If it does, the gate may be
selective; if it does not, the gate will not be, however sophisticated its aggregation. The five sources give one positive
and four negative instances of exactly this test.
    Alignment is necessary for selectivity but does not guarantee it. The four failed variants establish the necessary
half: none was selective, and none probed the verifier’s grounding question. But alignment alone is not sufficient,
a signal can probe the right question and still fail to separate PASS from FAIL when its values do not vary across
patients. The per-category operating envelope (Section 6.4) shows this: even the well-aligned NER-coverage signal
degenerates under coverage saturation, where nearly every patient has the relevant entities and the gate rarely fires,
and under coverage sparsity, where nearly no patient has them and the gate fires categorically rather than per patient.
Signal-distributional properties bound the operating regime beyond the alignment requirement.
    The principle also explains an interaction between the Ontology-Violation Filter and the NER-coverage gate. In
isolation, the diagnosis category is anti-selective, but under full DBPM it becomes the most selective category (lift
17.13, Section 6.4). The Filter removes ontology-violating relations that would otherwise enter the coverage signal the
gate reads; with those spurious relations gone, the coverage signal aligns more closely with the verifier’s grounding
decision for diagnosis questions. This is the principle operating one level up: cleaning an upstream signal makes a
downstream signal more aligned with the verifier’s question, and so more selective.

7.2. Verifier-Fed Memory as a Production-Scale Failure Mode
    The empty verifier-fed relation-extraction channel at production scale (Section 6.1), zero persisted patterns against
785,797 logged classifier rejections, is a production-scale failure of the most natural design for an inference-time pattern
memory. That design accumulates per-signature rejection statistics through a source-weighted update (Equation 3),
applies time-decay so the memory can recover as documentation conventions shift (Equation 5), and prunes signatures
whose decayed severity falls below a floor. Each mechanism is individually sensible; their interaction at production
scale is not.
    What determines the outcome is the distributional shape of the rejection stream, not its volume. When rejections
concentrate, many failures sharing a few signatures, each signature is reinforced faster than it decays and clears
threshold. When rejections disperse, many failures spread thinly across many signatures, each signature decays between
save events faster than reinforcement arrives, and nothing clears threshold no matter how high the total volume. Across
the full 167,034-patient run, the relation rejection stream was dispersed: its 785,797 rejections spread across the open
natural-language vocabulary of relation labels the model emits, with no single signature reinforced fast enough to
survive.
    The Ontology-Violation Filter (Section 4.7) avoids this failure by changing the source of the signal that feeds
the channel, not the persistence mechanism. Its predicate fires per candidate against a fixed set of 29 type-triples, so
events concentrate on those triples regardless of how the relation label is phrased. The concentrated distribution clears
threshold where the dispersed one did not, and it does so through the same persistence machinery; only the input signal
differs. The contribution here is the empirical demonstration that the choice of input signal, the verifier’s verdicts versus
the ontology predicate, not the design of the memory, can be the difference between an empty channel and a populated
one across the full 167,034-patient run.
    The implication reaches past this pipeline. Any inference-time memory that accumulates per-signature statistics
over free-form LLM output, whether relation labels, classification tags, or intent labels, is exposed to the same



A.H. Lazem et al.: Preprint submitted to Elsevier                                                              Page 22 of 39
                                            Dynamic Bidirectional Pattern Memory

dispersion. The remedy is to define signal sources that map that free-form output onto a bounded canonical space,
so the channel concentrates rather than disperses.

7.3. Clinical Implications
    Three findings of this paper carry directly into clinical deployment practice: a pattern-memory blocklist can
be configured yet empirically empty at scale, an ontology signal and a verifier catch different error classes and so
complement rather than replace each other, and tagging suspect candidates rather than deleting them keeps every
gating decision in the clinical audit trail. We state each as an implication for practitioners adopting inference-time
pattern-memory gating in LLM-grounded extraction pipelines.

(i) A blocklist that appears configured may be empirically inactive. Section 6.1 documents a verifier-fed relation
blocklist that was empty at production scale even though the pipeline generated nearly 800,000 rejections that should,
in principle, have filled it. A pipeline that relied on this blocklist for a safety guarantee would have shipped without
that guarantee being enforceable on its full corpus. The lesson is that a deployment using a pattern-memory gate
needs observability for whether the memory actually populates at scale, not merely confirmation that the mechanism
is configured to populate it. We release the crosscheck_F1_167k_blocklist.py script as one such check.

(ii) Verifier-independent signal sources complement rather than replace the verifier. The Ontology-Violation
Filter fills the relation blocklist where the verifier-fed pathway did not, but the two are not redundant. The verifier rejects
relations on content grounds (hallucinated pairs, unsupported relations); the Filter rejects them on structural grounds
(type-triple violations against the ontology). On the held-out cohort, the Filter flagged 49,734 ontology violations while
the verifier continued to reject content errors on a separate set of candidates. A deployment seeking coverage of both
error classes should run both sources.

(iii) Tagging rather than blocking preserves auditability. Automated removal of model output is contentious in
clinical settings, because a wrongly removed candidate is invisible by construction and therefore impossible to audit.
The DOWNGRADE-first discipline (Section 4.9) tags suspect candidates in the output stream instead of removing
them, so downstream consumers, clinicians, auditors, and training pipelines alike, see exactly what the gate flagged
and decide for themselves whether to act. A hard-blocking configuration is available for deployments that prefer the
gate’s verdict to be final. We recommend the tagging default in clinical contexts because a flagged candidate stays in
the audit trail whereas a blocked one disappears from it. This is an interpretive recommendation following from the
measurement discipline; the present work does not directly compare the costs of a false block against those of a false
allow in clinical use.

8. Limitations
    The empirical claims face four principal threats to validity, which we address in turn: the narrow operating
envelope of the NER-coverage gate (Section 8.1); the absence of a measured downstream precision lift (Section 8.2);
construct overlap between the gate’s design hypothesis test and its deployment evaluation (Section 8.3); and single-
corpus evaluation on PMC-Patients (Appendix A.8, consolidated in Section 8.4). We disclose each so that readers and
reviewers can locate the bounds of the claims.

8.1. Operating-Envelope Bounds of the NER-Coverage Gate
   The NER-coverage gate is selective in one operating regime, mid-spectrum coverage, and degenerates in others.
The per-category breakdown on the held-out cohort (Section 6.4) identifies four regimes.

    • Selective (diagnosis, risk_factor): the gate separates PASS from FAIL pairs. diagnosis (lift 17.13 at
      95.7% coverage) tags 73% of FAIL pairs against 4% of PASS pairs; risk_factor (lift 2.16 at 53.7% coverage)
      tags all FAIL pairs and 46% of PASS pairs. diagnosis is selective only under full DBPM, where the Ontology-
      Violation Filter cleans the upstream coverage signal (Section 7.1).
    • Categorical (outcome_clinicalstatus, outcome_disposition): at sparse coverage (4.4% and 1.7%) the
      gate tags nearly uniformly (lift 1.05 and 1.02), behaving as a category-level filter rather than a per-patient gate.



A.H. Lazem et al.: Preprint submitted to Elsevier                                                                Page 23 of 39
                                                    Dynamic Bidirectional Pattern Memory

    • Saturated or no-tagging (history, observation, symptoms, treatment, tests): for symptoms, treat-
      ment, and tests, coverage above 95% means nearly every patient is covered and the gate allows almost everyone;
      for history and observation, the gate does not fire on this cohort. In both sub-regimes, the mechanism
      operates correctly but rarely activates.

    • No NER bucket (adverse_event, outcome_mortality): the worker has no matching bucket, so the gate
      cannot apply and the difficulty-gate fallback tags PASS pairs only.

    The headline path lift of 1.84 therefore averages behaviour across these regimes. A deployment seeking uniform
selectivity across all eleven categories would need to address the saturated, sparse, and no-bucket regimes through
schema closure (Section 9.1) and category-specific configuration.

8.2. No Downstream Precision Lift Measured
    The verifier is permissive at the scale tested: it passes essentially every relation reaching the enriched output stage
in both arms of both ablations. The precision proxy delta on the held-out cohort is therefore 1.0000∕1.0000, and we
cannot claim that DBPM reduces downstream hallucinations as measured by the verifier’s decisions on enriched output.
    What DBPM demonstrably does is upstream candidate suppression (the Ontology-Violation Filter removes 913
relation candidates on the held-out cohort) and per-pair selectivity tagging (the NER-coverage gate tags 6,101 PASS-
side QA pairs against a fully ungated baseline; Section 6.5). These are measurable effects on the pipeline’s intermediate
state, not measured improvements to the final dataset’s clinical correctness. Establishing that the algorithmic effects
translate into clinical-correctness gains requires human-rated true-positive evaluation on a stratified sample of
suppressed and tagged candidates, which is outside this paper’s scope (Section 9.2) and reserved for separate dataset-
quality work.

8.3. Construct Overlap in the Gate’s Hypothesis Test
    The development-cohort hypothesis test that motivated the NER-coverage gate used the same construct, per-patient
NER coverage against per-patient QA failure, that the deployed gate now reads as its decision signal. The lift measured
on that cohort is therefore not a held-out estimate of the gate’s generalisation.
    We partially mitigate this by triangulating the path lift across four measurements under different configurations and
runs: the component-isolated ablation on the held-out cohort gives 1.52, the cross-task full-configuration ablation gives
1.71, the full-DBPM held-out ablation gives 1.84, and the development cohort gives a global blended lift of 1.59.2 The
three path-lift measurements span 1.52–1.84, and every figure exceeds the 1.5 selectivity threshold. The full-DBPM
configuration, which we adopt as the primary result, sits at the top of this band because the Ontology-Violation Filter
removes ontology-violating relations that would otherwise inflate the coverage signal, sharpening it when the full stack
is active (the diagnosis category, for instance, rises from anti-selective in isolation to a lift of 17.1 under full DBPM;
Section 6.3). Replication across scales, configurations, and runs is not the same as held-out generalisation, but the
consistency of the path lift above threshold across every measurement strengthens the mitigation. A genuine held-out
validation would require a fresh cohort drawn from a population the hypothesis test did not consume; we identify this
as future work (Section 9.3).

8.4. Further Limitations in Appendix A.10
   Two further limitations are retained in Appendix A.10 so the body stays focused on the three principal bounds
above:

    • Pattern-level cross-task propagation (Section 4.4), previously flagged as not independently ablated, is now
      measured at 0.098% of pipeline throughput, below the per-stage non-determinism floor (Appendix A.7).

    • Single-corpus evaluation: all results are measured on PMC-Patients; extension to electronic health record (EHR)
      corpora is reserved for future work (Section 9.3), with the structural expectations under EHR distribution shift
      discussed in Appendix A.8.
    2 The development-cohort entry is the global blended lift (1.59), not the path lift (1.89 on the nine mapped categories, Section 6.3); we list it

here because it is the figure the hypothesis test reported, and we mark it as global to avoid conflating it with the three path-lift measurements.




A.H. Lazem et al.: Preprint submitted to Elsevier                                                                                      Page 24 of 39
                                            Dynamic Bidirectional Pattern Memory

8.5. Scope of the Methodological Contribution
   This paper makes claims about DBPM’s algorithmic behaviour: which signal sources populate which channels,
which gate designs are selective, and which integrity checks pass at scale. It does not claim that DBPM’s outputs
improve the clinical correctness of the resulting dataset, that the suppressed relations are genuinely wrong in the clinical
context of their source text, or that models trained on DBPM-gated output outperform those trained on ungated output.
These are downstream-quality questions for separate evaluation work, deferred explicitly to keep the present scope
coherent.

9. Future Work
   We identify three future-work directions, ordered by how directly they extend the paper’s contributions. Each
addresses a specific limitation from Section 8.

9.1. Schema Closure for No-Bucket Categories
     Two categories (adverse_event, outcome_mortality) have no matching NER bucket, so the NER-coverage
gate cannot fire and the difficulty-gate fallback tags PASS pairs only (Sections 6.4 and 8.1). Extending the NER stage
to emit Adverse_Event and Outcome_Mortality entity types would let the gate operate on these two categories
on the same terms as the other nine. Closing the schema this way would raise the global blended lift toward the path
lift, since the two fallback categories would begin contributing selective tags rather than zero-lift fallback tags; the
realised gain depends on the NER yield in these categories and the verifier’s rejection distribution within them, and
is an empirical question for the closed-schema deployment. Schema closure is an engineering extension that does not
change the methodological contribution, but it is the most direct path to broadening the gate’s operating envelope.

9.2. Dataset-Quality Evaluation
    This paper makes no claim that DBPM’s suppressions and tags improve dataset quality (Section 8.5). Establishing
that would require a separate programme on the pipeline’s multi-task derivative of PMC-Patients: stratified human
review of suppressed relations and tagged QA pairs against clinical-correctness criteria, together with downstream
model-training studies on gated versus ungated output. A stratified sample of suppressed relations across the six
ontology-violation patterns has been prepared as a release artefact; its evaluation is reserved for a separate dataset-
quality paper.

9.3. Held-Out and EHR Validation
    The construct-overlap caveat (Section 8.3) is addressable by validating the gate on a held-out PMC-Patients cohort
drawn from a population the hypothesis test did not consume. The single-corpus caveat (Appendix A.8) is addressable
by extending evaluation to EHR-derived narratives, subject to the data-access constraints typical of EHR research. The
two validations are complementary: the first establishes that the gate generalises on a similar distribution, the second
that it generalises across a documentation-style shift. Each warrants its own publication.


10. Conclusion
     DBPM is an inference-time pattern-memory gating mechanism for a clinical NLP pipeline, and this paper
characterises its empirical behaviour at production scale rather than its theoretical properties. The characterisation
yielded four findings: a verifier-fed accumulation pathway that fails at 167,034-patient production scale (Section 6.1); a
verifier-independent ontology pathway that succeeds where the verifier-fed pathway did not (Section 6.2); a five-source
dissection of the question-answering gate in which four sources fail for structurally distinct reasons and one succeeds
by aligning its signal with the verifier’s grounding criterion (Sections 6.3 and 6.4); and the structural principle that
follows from the dissection (Section 7.1).
     The gate’s operating envelope is bounded. We characterise the bounds, saturated coverage, sparse coverage,
categorical regimes, and no-bucket categories (Section 8.1), and identify the extensions that would expand them.
We do not claim improvements to downstream clinical correctness: the effects we measure are upstream candidate
suppression and per-pair selectivity tagging, and whether these translate into clinically correct dataset improvements
is reserved for separate dataset-quality work (Section 9.2).
     The five-source dissection is the contribution we expect to travel beyond this pipeline. Practitioners designing
inference-time gates for generator-verifier architectures in any domain, clinical NLP, code generation, scientific

A.H. Lazem et al.: Preprint submitted to Elsevier                                                             Page 25 of 39
                                            Dynamic Bidirectional Pattern Memory

extraction, agentic tool use, can apply the structural principle to test a candidate signal source before investing
engineering effort in a mechanism that the four negative results here suggest will not generalise. The principle is
necessary, not sufficient: signal-distributional properties further bound the operating regime. Both the principle and
the bounds emerge from work at production scale, where the failure modes the paper documents become visible in a
way they do not at benchmark scale.
    We release the DBPM gating module, the ablation runner, the gate-decision graders, and the held-out cohort
identifier list. The release lets any reader reproduce the source-by-source outcomes and the production-scale channel
finding from the same underlying data; the five signal sources are documented as a repository changelog.


A. Implementation, Operational, and Extension Details
    This appendix collects implementation engineering, operational configuration, and extension-direction material
referenced from the body of the paper. Section A.1 also serves as the in-code identifier reference for the mechanisms
that Section 4 names by function: the body names each flag, threshold, and method by what it does, and the mapping
to source-level identifiers is given here.

A.1. Implementation and In-Code Identifier Reference
    DBPM is realised as a single Python class with (1) amortised gate cost. Read-side data structures are precomputed
once per save into per-task hash sets _block, _downgrade, _whitelist, indexed by signature; gate queries
(Equation 4) are constant-time set membership with at most three lookups (whitelist, block, downgrade) plus a
count comparison. Write-side updates (Equations 2 and 3) use a _write_index mapping signature keys to pattern
dictionaries for (1) in-place modification.
    State is persisted to a single JSON file (bpm_production.json) under a FileLock-protected atomic-write protocol:
the in-memory state is serialised to a temporary file and renamed over the canonical path under exclusive lock. To bound
I/O contention at the deployment’s 64-way effective concurrency, saves are batched: each worker process accumulates
record events and triggers a save after every 200 such events, then merges the on-disk state with its own using max
for severity and sum for counts. With 16 worker processes, this places save frequency at roughly one merge per 12.5
events globally, below the FileLock acquisition rate threshold for serialisation stalls.

Gate methods and signal sources. The three gate sites of the three-tier policy (Section 4.5) are exposed as
gate_ner(𝜎, NER), gate_relation(𝜎, RE), and gate_qa(category, ...). The question-answering method
retains the legacy name gate_qa for backward compatibility; the deployed configuration runs on QAR-category inputs,
and all selectivity claims are measured against QAR outputs (Section 3.1). The Ontology-Violation Filter (Section 4.7)
is M3-RE in the codebase: it records through bpm.record("re", payload, failure_type="hard_fail") with
payload field onto_violation=True, and populates the same _re_block cache that gate_relation() queries,
introducing no new gate.

Ablation flags. Six flags expose the design choices for ablation (Table 12). The four core flags toggle individual
mechanisms; the gate-level flag M1_QA_GATE_HARD_BLOCK controls whether the question-answering gate emits
BLOCK at all and defaults to 0 (DOWNGRADE-first) in every measurement of this paper (Section 4.9); and the
master switch BPM_DISABLE disables all DBPM gating and recording by flipping the four core flags to OFF at worker
initialisation. Because the master switch operates at gate-invocation time rather than at configuration-serialisation
time, the persisted configuration block is byte-identical between a BPM_DISABLE=0 run and a BPM_DISABLE=1 run;
the architectural consequences of this are discussed in Section A.6.

Thresholds and constants. Table 13 maps the concept names used in Section 4.2 to their in-code identifiers and
deployed values. The learning rates and decay factors are given in Table 3 and the body of Section 4.2; the source
weights are in Table 4. The question-answering fail-rate threshold of the third and fourth signal sources (Equations 7
and 8) is M1V5_FAIL_THRESHOLD, set to 0.30 on the development cohort and 0.60 on the held-out 5,000-patient cohort;
the difficulty threshold of the fourth source is M1V6_DIFFICULTY_THRESHOLD = 0.30.

Memory state and persistence fields Each blocklist entry stores the tuple (𝜎sev , 𝑐, 𝜏last , 𝜅) of Section 4.3 under
tasks[t].patterns in bpm_production.json, with the cross-task hit counter 𝜅 held in the field cross_-
task_hits; whitelist entries are stored under whitelist[t] as (𝜎conf , 𝑐, 𝜏last ). Rejection events are logged to

A.H. Lazem et al.: Preprint submitted to Elsevier                                                          Page 26 of 39
                                            Dynamic Bidirectional Pattern Memory


Table 12
Module-level ablation flags and their effect. The default column gives the value used in the deployed full-DBPM
configuration; the master switch BPM_DISABLE overrides the four core flags when set.

               Flag                                  Effect when OFF                                       Default

               BPM_ENABLE_CROSS_TASK                 No pattern-level cross-task propagation               ON
               BPM_ENABLE_THREE_TIER                 Gate collapses to BLOCK / ALLOW                       ON
               BPM_ENABLE_UNCERTAINTY                Ambiguous QAR verdicts treated as success             ON
               BPM_ENABLE_SOURCE_WEIGHTS             All source weights set to 𝑤𝑠 = 1                      ON

               M1_QA_GATE_HARD_BLOCK                 QAR gate emits DOWNGRADE, never BLOCK                 0
               BPM_DISABLE                           All DBPM gating and recording active                  0


Table 13
Concept-to-identifier mapping for the thresholds and constants of Section 4.2. Per-task values are given as (NER, RE,
QAR).

       Concept (body)                               In-code identifier                         Deployed value

       Block threshold 𝜃𝑡block                      BLOCK_THRESHOLDS[t].min_severity           (0.65, 0.70, 0.60)
       Minimum support 𝑛min
                        𝑡
                            (block)                 BLOCK_THRESHOLDS[t].min_count              (3, 2, 3)
       Downgrade threshold 𝜃𝑡down                   downgrade band lower bound                 0.40 (all tasks)
       Minimum support (downgrade)                  –                                          1 (all tasks)
       Storage cap 𝐶𝑡                               per-task pattern cap                       (200, 300, 150)
       Severity-zone guard                          cross-task severity ceiling                0.55
       Propagation cap                              cross_task_hits ceiling                    3
       QAR fail-rate threshold                      M1V5_FAIL_THRESHOLD                        0.30 dev / 0.60 held-out
       QAR difficulty threshold                     M1V6_DIFFICULTY_THRESHOLD                  0.30
       DOWNGRADE confidence multiplier              calibrated-confidence scale                0.70



universal_rejections.jsonl as the tuple (uid, stage, entity, reason, conf ) of Section 3.2. The deterministic
question-to-category map consulted by the NER-coverage gate is QA_TEMPLATES_GEN; the ontology and alias tables
of Equation (6) are ENTITY_RELATION_PRIORS (29 admissible type-triples) and RELATION_ALIAS (32 normalisation
entries), both fixed at worker load time. The per-pair gate verdict is written to the output field dbpm_gate, the cross-task
recursion guard of Algorithm 1 is the parameter is_cross_task, and the inactive self-critique source of Table 4 is
gated by SELFVERIF_ENABLE, which defaults to OFF.

A.2. Verifier Verdict Semantics
    A design choice of the surrounding pipeline is worth noting because it shapes the verdict distribution DBPM
consumes. The verifier is conservative-pass on binary tasks: for NER, only an explicit “NO” yields FAIL, and
ambiguous outputs default to PASS. For RE, ambiguous outputs default to PASS_WEAK, the middle of the graded
scale. For QAR, a single ambiguous output triggers a three-vote ensemble with tie-break to PASS.
    These conservative defaults reduce false-rejection on borderline candidates and produce a verdict distribution
skewed toward acceptance, which is the appropriate prior in clinical extraction where over-rejection systematically
loses recall on rare entities. DBPM’s gating policy (Equation 4) compensates by requiring 𝑛min
                                                                                           𝑡   corroborating failures
before a BLOCK fires, so the conservative-pass verifier and the support-count threshold work together rather than at
cross-purposes.




A.H. Lazem et al.: Preprint submitted to Elsevier                                                                    Page 27 of 39
                                            Dynamic Bidirectional Pattern Memory


Table 14
Complete experimental configuration. All settings were fixed before analysis and are reported here so the measurement
and downstream experiments can be reproduced exactly. The gating constants summarised below are stated in full, with
their in-code identifiers, in Tables 12 and 13; learning rates and source weights are in Tables 3 and 4.
           Component                                Setting
           Pipeline and corpus
           Source corpus                            PMC-Patients (167,034 patient narratives)
           Generator model                          Llama-3.3-70B (instruction-tuned)
           Verifier model                           MMed-Llama-3.1-70B
           Task buckets                             11 total; 3 DBPM-gated (NER, RE, QAR)
           Serving framework                        vLLM, continuous batching, tensor parallelism TP = 2 per model
           Decoding (generator and verifier)
           Context window                           8192 tokens (–max-model-len)
           Max concurrent sequences                 256 (–max-num-seqs)
           GPU memory utilisation                   0.90 (–gpu-memory-utilization)
           Precision                                bfloat16 (–dtype bfloat16); chunked prefill enabled
           Sampling temperature                     0.0 (greedy) for all gated-task generation and verification
           Top-𝑝 / top-𝑘                            Not applicable at temperature 0 (top-𝑝 0.9 engaged only if temper-
                                                    ature > 0); no top-𝑘
           Max generation tokens                    Per stage: 1500 (RE/JSON extraction), 160 (QAR), 60 (verifier
                                                    verdict)
           DBPM gating
           Block thresholds 𝜃𝑡block                 0.65 / 0.70 / 0.60 (NER / RE / QAR)
           Downgrade threshold 𝜃𝑡down               0.40 (all tasks)
           Minimum support 𝑛min 𝑡   (block)         3 / 2 / 3 (NER / RE / QAR); 1 for downgrade
           Storage caps 𝐶𝑡                          200 / 300 / 150 (NER / RE / QAR)
           Wall-clock half-lives ℎ𝑡                 5 / 10 / 10 days (NER / RE / QAR)
           In-run decay 𝜌𝑣                          0.99 (hard_fail), 0.985 (soft_downgrade)
           Severity-zone guard                      0.55 (cross-task severity ceiling)
           Propagation cap                          3 cross-task hits per signature
           DOWNGRADE confidence multiplier          0.70
           QAR fail-rate threshold                  0.30 (development) / 0.60 (held-out)
           QAR difficulty threshold                 0.30
           Measurement mode                         DOWNGRADE-first (M1_QA_GATE_HARD_BLOCK = 0)
           Evaluation cohort
           Held-out cohort                          5,000 patients, stratified random subsample
           Stratification                           Age bucket × gender × document-length tertile (24 non-empty strata)
           Tertile cut points                       T1 ≤ 1,931 < T2 ≤ 3,121 < T3 characters
           Sampling                                 Floor allocation then proportional residual; uniform random without
                                                    replacement
           Seed                                     Fixed (random.Random(42))
           Production cross-check                   Full corpus, 167,034 patients, deployed DBPM-full configuration
           Ablation protocol
           Paired ablations                         3 (Ontology Filter; NER-coverage gate; full DBPM master switch)
           Cross-task ablation                      1 separate paired ablation (reported in Appendix A.7)
           Selectivity metric                       Lift = 𝑃 (tag ∣ FAIL)∕𝑃 (tag ∣ PASS)
           Significance                             Delta-method 95% CI on log lift; 𝐻0 ∶ lif t = 1
           Hardware
           GPU                                      4 × NVIDIA H200 (141 GB HBM3e each)
           System                                   64 CPU cores, 900 GB system memory
           Scheduler                                SLURM (Supercomputing Wales Falcon)
           Persistence                              Single JSON file, FileLock atomic writes, 200-event save batches



A.3. Hardware and Software Configuration
   Table 14 consolidates every fixed setting of the measurement, the models and their decoding parameters, the gating
constants, the evaluation cohort, the ablation protocol, and the hardware, in a single reference; the remainder of this
subsection expands the serving and concurrency configuration in detail.
   Experiments run on a single SLURM-managed compute node: 4× NVIDIA H200 GPUs (141 GB HBM3e each),
64 CPU cores, 900 GB system memory. SLURM allocations are 72-hour wall-clock with a 70-hour Python-side budget
and a 2-hour grace window for graceful shutdown.

A.H. Lazem et al.: Preprint submitted to Elsevier                                                                      Page 28 of 39
                                            Dynamic Bidirectional Pattern Memory

   The pipeline is deployed as two independent vLLM OpenAI-compatible API servers, the generator on port 8000
and the verifier on port 8001, each occupying two GPUs under tensor parallelism TP = 2:

    • Generator 𝐺. Llama-3.3 70B (instruction-tuned) on GPUs 0–1, configured with –max-model-len 8192,
      –max-num-seqs 256, –gpu-memory-utilization 0.90, –dtype bfloat16, and –enable-chunked-
      prefill.
    • Verifier 𝑉 . MMed-Llama-3.1 70B (Qiu et al., 2024) on GPUs 2–3, with identical vLLM parameters.

     The orchestrator spawns 16 worker processes via Python multiprocessing. Each worker maintains four
concurrent patient coroutines, giving 64-way effective concurrency that vLLM’s continuous batching aggregates into
efficient GPU batches. HTTP traffic between worker coroutines and the two vLLM servers is asynchronous (aiohttp),
with per-call timeouts of 180 s and three retry attempts. Running independent generator and verifier servers, rather than
tensor-parallelising a single model across all four GPUs, avoids the larger cross-GPU synchronisation that a four-way
split would incur. When one model is split across GPUs, the partial results each GPU computes must be summed and
redistributed to every GPU before computation continues, an AllReduce collective operation that fires on every token;
keeping each model within its own pair of GPUs confines this synchronisation to two GPUs rather than four. This
is the configuration used for the production runs. The save-batching and FileLock protocol that bounds persistence
contention at this concurrency is described in Section A.1.

A.4. Checkpoint-and-Resume Protocol
    Because the full 167,034-patient corpus exceeds a single SLURM allocation, the pipeline implements a checkpoint-
and-resume protocol. The orchestrator detects pre-existing multitask_data_enriched.jsonl output and skips
already-processed UIDs, opening output files in append mode so no record is overwritten. The SLURM script monitors
Python’s exit code and treats codes 124 (timeout fired with SIGTERM), 130 (SIGINT-handled), 137 (SIGKILL
escalation), and 143 (clean SIGTERM exit) as resubmit-eligible, computing the remaining patient count and re-
sbatch-ing the job automatically.
    DBPM state survives across job submissions because its JSON file is written to the shared output directory
(OUTPUT_DIR/bpm_production.json), not to node-local /tmp.

A.5. Reproducibility
    The DBPM gating module and the analysis artefacts required to reproduce the paper’s quantitative claims are
released under an open-source license (see Code availability). The release includes:

    • the standalone DBPM gating module (dbpm.py), with all numeric constants stated in Section 4.2 as class
      attributes;
    • the selectivity grader (grade_m1v7_selectivity.py), the aggregate-provenance script (aggregate_dbpm_-
      provenance.py), and the 167K cross-check (crosscheck_F1_167k_blocklist.py);
    • the genericised ablation runner (run_ablation.sh), which documents the full-ON vs full-OFF protocol; and
    • the held-out 5,000-patient and development-cohort identifier lists.

    The surrounding extraction pipeline (the worker, orchestration, and model-serving layers) is not included; the
released module is the gating logic the paper characterises, and the cohort lists plus aggregate counts permit
reproduction of the reported selectivity, lift, and production-scale channel findings. The five question-answering signal
sources are documented as a changelog in the repository rather than shipped as patch scripts against the withheld
worker.

A.6. Architectural Disclosures
    DBPM gates three of the eleven pipeline task buckets (NER, RE, QAR; Section 3.1). The summary task has a
reserved threshold in BLOCK_THRESHOLDS["summary"] but no consumer gate. Medication extraction, temporal-event
extraction, active-risk identification, risk-state-machine derivation, risk-based recommendations, risk-grounded QAR,
and visualisation-payload assembly are entirely outside the DBPM gating system. Extension to these tasks is reserved
for future work.

A.H. Lazem et al.: Preprint submitted to Elsevier                                                           Page 29 of 39
                                            Dynamic Bidirectional Pattern Memory

    DOWNGRADE-first measurement discipline (Section 4.9) is applied to new, untested signal channels: the third
signal source onward of the question-answering gate, and the Ontology-Violation Filter channel. Legacy production-
validated channels (the named-entity gate over _ner_block, and the legacy _re_block check in gate_relation)
retain hard-BLOCK semantics as a deliberate design choice, since they have empirical support from the project’s
deployment history.
    The byte-identical configuration footprint of the BPM_DISABLE master switch, noted in Section A.1, has one
useful empirical consequence: because the switch acts at gate-invocation time, the OFF arm of the combined ablation
(Section 6.5) records zero DOWNGRADE tags across the full 5,000-patient cohort, confirming that the switch produces
the expected gate inactivity rather than a silently altered configuration.

A.7. Pattern-Level Cross-Task Propagation: Measured Contribution
     The pattern-level cross-task propagation mechanism described in Section 4.4 is a persistence-layer component
active in all DBPM runs reported in Section 6. We isolate its independent contribution via a single paired ablation: ON
arm BPM_ENABLE_CROSS_TASK = 1 (the deployed default) versus OFF arm BPM_ENABLE_CROSS_TASK = 0, with
all other DBPM mechanisms (Ontology-Violation Filter, NER-coverage gate, three-tier gating, source weights) held at
their default ON settings. Both arms use the held-out 5,000-patient cohort.

Result. The cross-task ablation produces a combined pair-count delta of 280 across the three gated tasks (NER Δ =
−232, RE Δ = +41, QAR Δ = −7) against 287,350 total pipeline pairs in the ON arm, yielding a contribution
of 0.098% of pipeline throughput. This is below the 0.5% per-stage non-determinism floor of the pipeline (vLLM
continuous batching plus the dual-model verifier introduce ∼ 0.1–0.3% per-stage run-to-run variance on identical-
cohort runs; see Appendix A.4). The path lift in the ON arm is 1.71, within the 1.52–1.84 empirical band documented
in Section 8.3.

Instrumentation note. The worker’s _event_counters["cross_task_propagations"] global counter reported
zero events in this ablation, while 24 NER patterns in the persisted bpm_production.json recorded cross_task_-
hits > 0. The discrepancy reflects an instrumentation gap in the worker’s event-counter update paths: cross-task
propagation through new-signature creation increments the per-pattern counter but not the global event counter. The
per-pattern evidence confirms the mechanism fired, and the pair-count delta is the authoritative measurement of
mechanism contribution at the pipeline-output level. We disclose this for transparency; the substantive claim is the
0.098% pair-delta, which is independent of the global event-counter discrepancy.

Interpretation. The mechanism’s safeguards (severity-zone guard at 0.55, propagation cap 𝜅 ≥ 3, source weights
𝑤 ∈ [0.2, 0.4]) bound its impact below the per-stage non-determinism floor at the held-out 5K scale. This is consistent
with the architectural intent of the mechanism: pattern-level cross-task propagation is designed to push severity into
the DOWNGRADE band without crossing into BLOCK on cross-task evidence alone (Section 4.5, invariant 3), and
at this scale the safeguards bind before any output-level effect accumulates. The result closes the independent-ablation
limitation flagged in earlier drafts of this paper.

A.8. Single-Corpus Evaluation
    All evaluation in this paper uses PMC-Patients (Zhao et al., 2023) as the source corpus. PMC-Patients is the
established public benchmark for clinical narrative extraction at the sub-100K-patient-record scale, and using it permits
direct comparison to prior LLM-driven clinical NLP work. However, the corpus consists of case reports from PubMed
Central full-text articles, which differ in documentation style from electronic health records (EHRs) used in real clinical
settings: case reports are authored for academic publication, are typically reviewed by peers before release, and are
written with denotative precision intended to support reproducibility. EHR narratives are authored under clinical time
pressure, contain abbreviations and shorthand specific to local institutional cultures, and reflect dictation artefacts not
present in published case reports.
    The empirical findings of Section 6, specifically the diffuse-rejection distributional shape that produced the
production-scale channel finding (Section 6.1) and the per-category operating envelope of the NER-coverage gate
(Section 6.4), may shift on EHR-derived corpora. Extension to EHR data is identified as future work (Section 9.3).




A.H. Lazem et al.: Preprint submitted to Elsevier                                                            Page 30 of 39
                                                   Dynamic Bidirectional Pattern Memory

A.9. Answerability Cascade for Saturated and Sparse-Coverage Categories
    Five QAR categories on the held-out cohort exhibit saturated NER coverage (symptoms, treatment, tests,
observation, history); the NER-coverage gate rarely fires for these because nearly every patient is covered. One
category (outcome_clinicalstatus) exhibits sparse NER coverage, so the gate fires categorically rather than
per-patient. A complementary signal source, for example a distilled small-language-model answerability check that
fires when NER coverage is uninformative, could extend the working operating envelope to these categories while
preserving the deterministic predicate structure of the present design.
    This extension is conditional on its own evaluation establishing that the additional signal is selective; we do not
commit to it working at this stage. We identify it as the most natural next-step extension for deployments seeking
uniform per-pair selectivity across all categories.

A.10. Limitations Addressed in This Appendix
    This section consolidates the appendix-resident limitation disclosures referenced from Section 8.4:
    • Pattern-level cross-task propagation (Appendix A.7): measured contribution 0.098% of pipeline throughput,
      below the per-stage non-determinism floor.
    • Single-corpus evaluation (Appendix A.8): all empirical findings are measured on PMC-Patients; EHR distribution-
      shift is addressed in Section 9.3.

CRediT authorship contribution statement
    Ali H. Lazem: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data
curation, Writing – original draft, Writing – review & editing, Visualization. William Teahan: Conceptualization,
Methodology, Supervision, Writing – review & editing, Project administration.


Code availability
    The DBPM gating module, the grader scripts that reproduce the reported selectivity and lift figures, and the cohort
identifier lists are openly available on GitHub at https://github.com/Ali-Lazem/DBPM and permanently archived
on Zenodo at https://doi.org/10.5281/zenodo.21038023. The surrounding extraction pipeline is not included;
the repository provides the gating logic and the artefacts required to reproduce the paper’s quantitative claims.


Data availability
    The cohort identifier lists used for the reported ablations are included in the code repository and index the publicly
available PMC-Patients corpus (Zhao et al., 2023). The aggregate gating-outcome counts that reproduce the reported
figures are provided in the repository (counts and rates only; no clinical text). The derived extraction corpus is not
released.

Acknowledgements
   We acknowledge the services of Supercomputing Wales and the Bangor eResearch Team, including the support
provided by Dr. Ade Fewings.


References
Alsentzer, E., Murphy, J., Boag, W., Weng, W.H., Jindi, D., Naumann, T., McDermott, M., 2019. Publicly available clinical bert embeddings, in:
   Proceedings of the 2nd Clinical Natural Language Processing Workshop, pp. 72–78.
Aronson, A.R., 2001. Effective mapping of biomedical text to the umls metathesaurus: The metamap program, in: Proceedings of the AMIA
   Symposium, pp. 17–21.
Borgeaud, S., Mensch, A., Hoffmann, J., Cai, T., Rutherford, E., Millican, K., van den Driessche, G., Lespiau, J.B., Damoc, B., Clark, A., et al.,
   2022. Improving language models by retrieving from trillions of tokens, in: International Conference on Machine Learning, pp. 2206–2240.
Brown, T.B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Neelakantan, A., et al., 2020. Language models are few-shot learners, in:
   Advances in Neural Information Processing Systems, pp. 1877–1901.
Chiang, W.L., Li, Z., Lin, Z., Sheng, Y., Wu, Z., Zhang, H., Zheng, L., Zhuang, S., Zhuang, Y., Gonzalez, J.E., Stoica, I., Xing, E.P., 2023. Vicuna:
   An open-source chatbot impressing gpt-4 with 90%* chatgpt quality. URL: https://vicuna.lmsys.org.


A.H. Lazem et al.: Preprint submitted to Elsevier                                                                                    Page 31 of 39
                                                     Dynamic Bidirectional Pattern Memory

Graves, A., Wayne, G., Reynolds, M., Harley, T., Danihelka, I., Grabska-Barwińska, A., Colmenarejo, S.G., Grefenstette, E., Ramalho, T., Agapiou,
   J., et al., 2016. Hybrid computing using a neural network with dynamic external memory. Nature 538, 471–476.
Gu, Y., Tinn, R., Cheng, H., Lucas, M., Usuyama, N., Liu, X., Naumann, T., Gao, J., Poon, H., 2021. Domain-specific language model pretraining
   for biomedical natural language processing. ACM Transactions on Computing for Healthcare 3, 1–23.
Henry, S., Buchan, K., Filannino, M., Stubbs, A., Uzuner, O., 2020. 2018 n2c2 shared task on adverse drug events and medication extraction in
   electronic health records. Journal of the American Medical Informatics Association 27, 3–12. doi:10.1093/jamia/ocz166.
Hinton, G., Vinyals, O., Dean, J., 2015. Distilling the knowledge in a neural network. arXiv preprint arXiv:1503.02531 .
Hong, S., Zhuge, M., Chen, J., Zheng, X., Cheng, Y., Wang, J., Zhang, C., Wang, Z., Yau, S.K.S., Lin, Z., et al., 2024. Metagpt: Meta programming
   for a multi-agent collaborative framework, in: International Conference on Learning Representations.
Kirkpatrick, J., Pascanu, R., Rabinowitz, N., Veness, J., Desjardins, G., Rusu, A.A., Milan, K., Quan, J., Ramalho, T., Grabska-Barwinska, A.,
   Hassabis, D., Clopath, C., Kumaran, D., Hadsell, R., 2017. Overcoming catastrophic forgetting in neural networks. Proceedings of the National
   Academy of Sciences 114, 3521–3526. doi:10.1073/pnas.1611835114.
Lee, D.H., 2013. Pseudo-label: The simple and efficient semi-supervised learning method for deep neural networks, in: Workshop on Challenges
   in Representation Learning, ICML, p. 896.
Lee, J., Yoon, W., Kim, S., Kim, D., Kim, S., So, C.H., Kang, J., 2020. Biobert: A pre-trained biomedical language representation model for
   biomedical text mining. Bioinformatics 36, 1234–1240.
Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.t., Rocktäschel, T., Riedel, S., Kiela, D., 2020.
   Retrieval-augmented generation for knowledge-intensive nlp tasks, in: Advances in Neural Information Processing Systems, pp. 9459–9474.
Liang, J., Hu, D., Feng, J., 2020. Do we really need to access the source data? source hypothesis transfer for unsupervised domain adaptation, in:
   International Conference on Machine Learning, pp. 6028–6039.
Lopez-Paz, D., Ranzato, M., 2017. Gradient episodic memory for continual learning, in: Advances in Neural Information Processing Systems.
Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang, Y., Gupta, S., Majumder,
   B.P., Hermann, K., Welleck, S., Yazdanbakhsh, A., Clark, P., 2023. Self-refine: Iterative refinement with self-feedback, in: Advances in Neural
   Information Processing Systems. URL: https://arxiv.org/abs/2303.17651.
Parisi, G.I., Kemker, R., Part, J.L., Kanan, C., Wermter, S., 2019. Continual lifelong learning with neural networks: A review. Neural Networks
   113, 54–71.
Park, J.S., O’Brien, J.C., Cai, C.J., Morris, M.R., Liang, P., Bernstein, M.S., 2023. Generative agents: Interactive simulacra of human behavior, in:
   Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST), pp. 1–22.
Qiu, P., Wu, C., Zhang, X., Lin, W., Wang, H., Zhang, Y., Wang, Y., Xie, W., 2024. Towards building multilingual language model for medicine.
   Nature Communications 15, 8384.
Ratner, A., Hancock, B., Dunnmon, J., Sala, F., Pandey, S., Ré, C., 2019. Training complex models with multi-task weak supervision, in: Proceedings
   of the AAAI Conference on Artificial Intelligence, pp. 4763–4771.
Santoro, A., Bartunov, S., Botvinick, M., Wierstra, D., Lillicrap, T., 2016. Meta-learning with memory-augmented neural networks, in: International
   Conference on Machine Learning, pp. 1842–1850.
Savova, G.K., Masanz, J.J., Ogren, P.V., Zheng, J., Sohn, S., Kipper-Schuler, K.C., Chute, C.G., 2010. Mayo clinical text analysis and knowledge
   extraction system (ctakes): Architecture, component evaluation and applications. Journal of the American Medical Informatics Association 17,
   507–513.
Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., Yao, S., 2023. Reflexion: Language agents with verbal reinforcement learning,
   in: Advances in Neural Information Processing Systems. URL: https://arxiv.org/abs/2303.11366.
Sukhbaatar, S., Szlam, A., Weston, J., Fergus, R., 2015. End-to-end memory networks, in: Advances in Neural Information Processing Systems.
Tambe, M., 1997. Towards flexible teamwork. Journal of Artificial Intelligence Research 7, 83–124. doi:10.1613/jair.433.
Taori, R., Gulrajani, I., Zhang, T., Dubois, Y., Li, X., Guestrin, C., Liang, P., Hashimoto, T.B., 2023. Stanford alpaca: An instruction-following
   llama model. GitHub repository. URL: https://github.com/tatsu-lab/stanford_alpaca.
Teahan, W.J., Tuff, P.G., 2006. A framework for knowledge sharing between autonomous agents, in: Proceedings of the 5th WSEAS International
   Conference on System Science and Simulation in Engineering, pp. 219–227.
Wang, D., Shelhamer, E., Liu, S., Olshausen, B., Darrell, T., 2021. Tent: Fully test-time adaptation by entropy minimization, in: International
   Conference on Learning Representations. URL: https://openreview.net/forum?id=uXl3bZLkr3c.
Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., Zhou, D., 2023. Self-consistency improves chain-of-thought
   reasoning in language models, in: International Conference on Learning Representations.
Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E.H., Le, Q.V., Zhou, D., 2022. Chain-of-thought prompting elicits reasoning
   in large language models, in: Advances in Neural Information Processing Systems, pp. 24824–24837.
Wettig, A., Gupta, A., Malik, S., Chen, D., 2024. Qurating: Selecting high-quality data for training language models, in: Proceedings of the 41st
   International Conference on Machine Learning, pp. 52915–52971.
Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., et al., 2024. Autogen: Enabling next-gen llm
   applications via multi-agent conversation, in: First Conference on Language Modeling.
Xie, Q., Luong, M.T., Hovy, E., Le, Q.V., 2020. Self-training with noisy student improves imagenet classification, in: Proceedings of the IEEE/CVF
   Conference on Computer Vision and Pattern Recognition, pp. 10687–10698.
Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y., 2023. React: Synergizing reasoning and acting in language models, in:
   International Conference on Learning Representations. URL: https://arxiv.org/abs/2210.03629.
Zhang, Q., Hu, C., Upasani, S., Ma, B., Hong, F., Kamanuru, V., Rainton, J., Wu, C., Ji, M., Li, H., Thakker, U., Zou, J., Olukotun, K., 2026. Agentic
   context engineering: Evolving contexts for self-improving language models, in: International Conference on Learning Representations. URL:
   https://arxiv.org/abs/2510.04618.




A.H. Lazem et al.: Preprint submitted to Elsevier                                                                                       Page 32 of 39
                                                    Dynamic Bidirectional Pattern Memory

Zhao, Z., Jin, Q., Chen, F., Peng, T., Yu, S., 2023. A large-scale dataset of patient summaries for retrieval-based clinical decision support systems.
  Scientific data 10, 909.
Zheng, L., Chiang, W.L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E., Zhang, H., Gonzalez, J.E., Stoica, I., 2023.
  Judging llm-as-a-judge with mt-bench and chatbot arena, in: Advances in Neural Information Processing Systems.
Zhou, C., Liu, P., Xu, P., Iyer, S., Sun, J., Mao, Y., Ma, X., et al., 2023. Lima: Less is more for alignment, in: Advances in Neural Information
  Processing Systems.

Ali Hussein Lazem received the B.Sc. in Computer Science from the University of Thi-Qar, Iraq, and the M.Sc. in Artificial Intelligence from Troy
University, Alabama, USA. He is currently a Ph.D. candidate in the School of Computer Science and Engineering at Bangor University, United
Kingdom. His research focuses on the production-scale deployment of large language models for clinical natural language processing, with broader
interests in generative AI, computer vision, and machine learning.




William J. Teahan is a Senior Lecturer and Postgraduate Research Director in the School of Computer Science and Engineering at Bangor
University, United Kingdom. His research spans natural language processing, text compression, machine learning, and agent-based systems, with
a long-standing interest in statistical models of language and structured knowledge representation. He has contributed to multidisciplinary projects
across computer science, biological sciences, and environmental sciences, with collaborations spanning multiple countries. His roles at Bangor
include postgraduate supervision, curriculum development, and the coordination of research programmes within the School. He has supervised
numerous doctoral students whose work has informed computational approaches to language modelling and applied artificial intelligence.




A.H. Lazem et al.: Preprint submitted to Elsevier                                                                                     Page 33 of 39
                                             Dynamic Bidirectional Pattern Memory




                                                        Generator G
     generator zone                                      Llama-3.3 70B
                                                        (vLLM, TP=2)



                                                                  candidates 𝐶𝑖,𝑡
                                                                  signatures 𝜎



                                                        DBPM Gate
                                                 gated tasks: NER, RE, QAR

                                     gate function: BLOCK / DOWNGRADE / ALLOW




      inference-time                    Blocklist 𝐵𝑗                      Whitelist 𝑊𝑗
    pattern memory                     severity per 𝜎                    confidence per 𝜎




                                       Ontology-Violation Filter (verifier-independent)


                                                                                             Feedback Loop:
                                                                                             verdict stream {(𝜎, 𝑡, 𝑣, 𝜏, 𝑠)}
                                                                                             (no gradient updates)
                                                                  BLOCK ⇒ dropped
                                                                  DOWNGRADE ⇒ tagged
                                                                  ALLOW ⇒ passes



                                                         Verifier V
       verifier zone                                MMed-Llama-3.1 70B
                                                     (vLLM, TP=2)


Figure 1: Architecture and locus of DBPM. The pattern memory sits between the generator (𝐺, Llama-3.3 70B) and
the verifier (𝑉 , MMed-Llama-3.1 70B). It gates candidate outputs before 𝑉 is called (forward path, solid arrows)
and accumulates evidence from 𝑉 ’s verdicts after each call (feedback loop, dashed arrow). The gate returns BLOCK,
DOWNGRADE, or ALLOW for each candidate signature 𝜎 (Equation 4): a BLOCK’ed candidate is dropped before 𝑉 is
called, a DOWNGRADE’ed candidate passes through with a tag in its output metadata, and an ALLOW’ed candidate
is unchanged. The dual store is the heart of the persistence layer (Section 4.3): the blocklist 𝐵𝑗 accumulates severity
evidence, while the whitelist 𝑊𝑗 records direct verifier confirmation and takes precedence over indirect evidence. The
Ontology-Violation Filter (Section 4.7) provides a verifier-independent signal source feeding the same blocklist. DBPM
updates no parameters of 𝐺 or 𝑉 .




A.H. Lazem et al.: Preprint submitted to Elsevier                                                               Page 34 of 39
                                              Dynamic Bidirectional Pattern Memory




Algorithm 1 DBPM update operator 𝑈 (per verdict event)
Require: verdict event (𝜎, 𝑡, 𝑣, 𝜏, 𝑠); memory state (𝐵𝑗−1 , 𝑊𝑗−1 ); recursion guard is_cross_task (default FALSE)
Ensure: updated memory state (𝐵𝑗 , 𝑊𝑗 )

 1: if 𝑣 = SUCCESS then
 2:    update 𝑊𝑗−1 (𝜎, 𝑡) via the whitelist path                                                 ⊳ whitelist path, Sec. 4.3
 3:    return (𝐵𝑗−1 , 𝑊𝑗 )
 4: end if

 5: 𝜂 ← 𝜂𝑣,𝑡 ;   𝑤 ← 𝑤𝑠                                                                     ⊳ learning rate, source weight
 6: if entry 𝑒 for (𝜎, 𝑡) exists in 𝐵𝑗−1 then
                      (                   )
 7:     𝑒.sev ← min 1, 𝜌𝑣 𝑒.sev + 𝑤 𝜂                                                          ⊳ severity update, Sec. 4.3
 8:     𝑒.count ← 𝑒.count + 1; 𝑒.𝜏 ← 𝜏
 9: else
10:     initialise 𝑒 with sev = 𝑤 𝜎0 (𝑣), count = 1, 𝜅 = 0, 𝜏 = 𝜏
11:     insert 𝑒 into 𝐵𝑗
12: end if

13: if is_cross_task or 𝑣 ≠ HARD _ FAIL then
14:      return (𝐵𝑗 , 𝑊𝑗−1 )                                                             ⊳ guards rule out cycles, Sec. 4.4
15: end if


16: if 𝑡 = RE then
17:      for 𝑒str ∈ {head, tail} with 4 < |𝑒str | < 60 do
18:          PROPAGATE(𝑒str , 𝑤cross_task_re , 𝜏)                                                  ⊳ RE → NER, Sec. 4.4
19:      end for
20: else if 𝑡 = QAR then
21:      for 𝑒str ∈ split(answer, ",") do
22:          PROPAGATE(𝑒str , 𝑤cross_task_qa , 𝜏)                                                ⊳ QAR → NER, Sec. 4.4
23:     end for
24: else if 𝑡 = NER then
25:     𝑃 ← 𝑃 ∪ {𝜎}                                                                  ⊳ NER → RE preemption set, Sec. 4.4
26: end if


27: return (𝐵𝑗 , 𝑊𝑗−1 )

28: procedure P ROPAGATE (𝑒str , 𝑤, 𝜏)                                                ⊳ graded cross-task update, Sec. 4.4
29:    if 𝑒str ∈ 𝑊 NER or 𝜅(𝑒str ) ≥ 3 or 𝐵𝑗 (𝑒str , NER) ≥ 0.55 then
                    𝑗−1
30:        return                                                      ⊳ whitelist, cap, and severity-zone guards
31:    end if
32:    𝑠before ← 𝐵𝑗 (𝑒str , NER)
33:    recurse: 𝑈 (𝑒str , NER, SOFT_DOWNGRADE, 𝜏, 𝑤) with is_cross_task = T RUE
34:    Δ ← 𝐵𝑗 (𝑒str , NER) − 𝑠before
35:    𝐵𝑗 (𝑒str , NER) ← 𝑠before + 12 Δ                                                ⊳ half-weight propagation
36:    𝜅(𝑒str ) ← 𝜅(𝑒str ) + 1
37: end procedure




A.H. Lazem et al.: Preprint submitted to Elsevier                                                             Page 35 of 39
                                                               Dynamic Bidirectional Pattern Memory


                 Production-scale finding: verifier-fed RE blocklist channel empty at 167K despite 785,797 Stage-3 rejections
                                      (a) Input signal: stage rejections                         (b) Output state: persisted patterns

    Stage 3 - RE classifier                                                                785,797                                               104                                      5,860




                                                                                                        Persisted patterns at 167K (log scale)
    Stage 4 - QAR verifier                                              548,093
                                                                                                                                                 103


 Stage 1 - NER gatekeeper         33,678
                                                                                                                                                 102


    Stage 1 - NER verifier 33                                                                                                                                               11
                                                                                                                                                 101
                                                                                                                                                              0
     Stage 1 - NER rescue 14                                                                                                                               (channel
                                                                                                                                                            empty)
                                                                                                                                                 100
                              0            200000        400000         600000          800000                                                               RE             QAR            NER
                                                    Rejection events logged at 167K


Figure 2: The verifier-fed relation-extraction persistence channel at 167,034-patient deployment scale. (a) Input signal:
1.37M rejection events logged across the five verifier stages, dominated by Stage 3 (relation classifier, 785,797 events,
reason SOTA_Classify_None) and Stage 4 (QA verifier, 548,093 events). (b) Output state: persisted patterns at threshold
in the relation, QA, and named-entity channels after the run (log scale). The relation channel is empty despite consuming
785,797 input events; the named-entity channel populates with 5,860 patterns and the QA channel with 11. This asymmetry
is the central production-scale finding and motivates the verifier-independent Ontology-Violation Filter (Section 4.7).




                                                              Ontology-Violation Filter: type-triples populating the RE blocklist
    tests -> associated_with -> diagnosis                                                                                                                                                13,749


        symptoms -> manifests -> diagnosis                                                                                                                                    11,813


             symptoms -> causes -> diagnosis                                                                                                                                  11,811


         treatment -> prevents -> symptoms                                                                 6,635


 history -> associated_with -> diagnosis                                                4,085


 diagnosis -> associated_with -> history                               1,641
                                                                                                                                                       6 patterns, 49,734 events on held-out cohort

                                                          0          2000         4000           6000                                             8000         10000       12000       14000
                                                                                      Ontology-violation events on held-out cohort

Figure 3: Type-triple patterns populating the relation blocklist through the Ontology-Violation Filter (Section 4.7) on the
held-out cohort. Six threshold-clearing patterns aggregate 49,734 ontology-violation events. The Filter is a deterministic
predicate (Equation 6) over head-type, relation, tail-type triples against a 29-entry clinical ontology, independent of the
verifier-fed pathway whose collapse is documented in Figure 2.



A.H. Lazem et al.: Preprint submitted to Elsevier                                                                                                                                      Page 36 of 39
                                                         Dynamic Bidirectional Pattern Memory




                                               Five candidate signals for the question-answering gate
                                     lift 0.006 (not selective)
 Category-aggregate fail-mass
                                     aggregation-level mismatch


                                  no signal (not selective)
          Verifier uncertainty
                                  signal absence (flag unpopulated)


                                       lift 0.050 (not selective)
         Per-category fail-rate
                                       counting asymmetry


                                  lift 0.000 (not selective)                                                   selectivity
         Per-patient difficulty                                                                                threshold (1.5)
                                  cross-task orthogonality


                                                                                                                                 lift 1.84 (SELECTIVE)
    NER-coverage intersection
                                                                                                                                 structurally aligned (selective)

                              0.00           0.25           0.50          0.75       1.00       1.25        1.50       1.75          2.00
                                                                   Selectivity lift = P(tag | FAIL) / P(tag | PASS)

Figure 4: Selectivity lift of the five candidate signals for the question-answering gate on the held-out 5,000-patient cohort.
Lift is defined in Equation (10) as 𝑃 (tag ∣ FAIL)∕𝑃 (tag ∣ PASS); values ≥ 1.5 (dashed line) indicate selectivity. Four of the
five signals fall below the threshold, each for the distinct reason labelled; the NER-coverage signal reaches a path lift of 1.84
in the full-DBPM configuration, within the 1.52–1.84 empirical band across four independent replications (Section 8.3).




A.H. Lazem et al.: Preprint submitted to Elsevier                                                                                              Page 37 of 39
                                                      Dynamic Bidirectional Pattern Memory




                    Per-category behaviour of the NER-coverage gate (the working signal), held-out cohort
              diagnosis                                                                                                                               lift 17.13 cov 96%

            risk_factor                                                                                      lift 2.16 cov 54%

 outcome_clinicalstatus                                                                         lift 1.05 cov 4%

    outcome_disposition                                                                         lift 1.02 cov 2%

               symptoms            no tagging cov 97%

              treatment            no tagging cov 98%
                                                                                                     selectivity
                                                                                                     threshold 1.5
                  tests            no tagging cov 95%

                history            no tagging cov 43%

            observation            no tagging cov 1%

          adverse_event            fallback (lift 0.00) cov 0%                                                            selective (lift > 1.5)
                                                                                                                          categorical (lift ~ 1.0, sparse coverage)
      outcome_mortality            fallback (lift 0.00) cov 0%                                                            saturated / no tagging
                                                                                                                          difficulty-gate fallback (no NER bucket)
                                              0.1                            0.5          1.0      1.5 2.0                 5           10             20
                                                        Selectivity lift = P(tag | FAIL) / P(tag | PASS) (log scale)
                 cov = coverage: fraction of PASS pairs whose patient NER set contains the asked category. Selectivity requires mid-range coverage.


Figure 5: Per-category behaviour of the NER-coverage gate on the held-out cohort, the working signal of Section 6.3.
Bars give the selectivity lift per QAR category on a log scale; coverage (the fraction of PASS pairs whose patient-level
NER set contains the asked category) is annotated on each. The categories fall into four regimes: selective (diagnosis
17.13, risk_factor 2.16, both above the 1.5 threshold); categorical at sparse coverage (outcome_clinicalstatus 1.05,
outcome_disposition 1.02); saturated or no-tagging at high or very low coverage (five categories); and difficulty-gate
fallback where no NER bucket exists (adverse_event, outcome_mortality). Selectivity requires mid-range coverage:
diagnosis is anti-selective in isolation but becomes the most selective category under full DBPM, as the Ontology-
Violation Filter removes ontology-violating relations that inflate its coverage signal (Section 6.3).




A.H. Lazem et al.: Preprint submitted to Elsevier                                                                                                          Page 38 of 39
                                                                Dynamic Bidirectional Pattern Memory




                                     DOWNGRADE-first: the gate tags candidates without removing them
                            7000            Pairs Modified (Full-DBPM ON vs OFF)                                                   Candidates Tagged

                                                                                                                                           6,101
                            6000
Events on held-out cohort




                            5000

                            4000

                            3000

                            2000

                            1000                                 913
                                        257
                                                                                            8
                               0
                                          NER                     RE                      QAR                                               QAR
                                   (Pairs Changed)         (Pairs Changed)          (Pairs Changed)                                     (Gate Tagged)
                                   Note: The RE delta represents the deterministic Ontology-Violation Filter's suppression, not the QAR gate.


Figure 6: Pair-count deltas (left) versus gate-tag counts (right) on the held-out cohort under the full-DBPM ablation. The
named-entity and QA pair-count deltas are within run-to-run noise (+257 and −8), confirming the DOWNGRADE-first
discipline: the gate tags QA candidates without removing them. The relation delta of −913 is the Ontology-Violation
Filter’s genuine suppression, not a gate effect. The gate tags 6,101 PASS-side and 1,392 FAIL-side QA pairs (7,493 total),
establishing selectivity at the tagging level rather than through output-volume change.




A.H. Lazem et al.: Preprint submitted to Elsevier                                                                                                  Page 39 of 39
