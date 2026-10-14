                                         DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA


                                                    Pinaki Prasad Guha Neogi * 1 Ahmad Mohammadshirazi * 1 Ser-Nam Lim 2 Rajiv Ramnath 1


                                                                     Abstract                               1. Introduction
                                               Document visual question answering requires                  Answering questions over documents such as invoices, re-
                                               models not only to answer questions correctly, but           ceipts, forms, and scanned records requires models to reason
arXiv:2511.22521v3 [cs.CV] 22 May 2026




                                               also to precisely localize answers within complex            jointly over textual content and spatial layout. Beyond pre-
                                               document layouts. While large vision-language                dicting correct answers, practical document understanding
                                               models (VLMs) achieve strong spatial ground-                 systems must also precisely localize answers within the
                                               ing, their inference cost and latency limit real-            document, enabling trust, interpretability, and human verifi-
                                               world deployment; on the other hand, compact                 cation in high-stakes domains such as finance, healthcare,
                                               VLMs are efficient but suffer substantial local-             and legal processing (Mathew et al., 2021; Park et al., 2019;
                                               ization degradation under standard fine-tuning or            Jaume et al., 2019).
                                               distillation. To address this gap, we propose Doc-
                                                                                                            Recent vision-language models (VLMs) have demonstrated
                                               VAL, a validated chain-of-thought (CoT) distil-
                                                                                                            strong performance on document understanding benchmarks
                                               lation framework that transfers explicit spatial
                                                                                                            that evaluate answer accuracy and layout reasoning (Huang
                                               reasoning from large teacher models to compact,
                                                                                                            et al., 2022; Luo et al., 2024; Liao et al., 2024). However,
                                               deployable student VLMs. DocVAL combines
                                                                                                            this progress exposes a fundamental deployment dilemma.
                                               (1) teacher-generated spatial CoT supervision,
                                                                                                            Large VLMs achieve robust answer accuracy and spatial
                                               (2) a rule-based dual-mode validator that filters
                                                                                                            grounding, but incur high inference latency, large mem-
                                               low-quality training signals and provides fine-
                                                                                                            ory footprints, and reliance on cloud APIs, making them
                                               grained, pixel-level corrective feedback, and (3)
                                                                                                            impractical for large-scale or on-device deployment. In con-
                                               a validation-driven two-stage training procedure
                                                                                                            trast, compact VLMs are efficient and deployable, yet suffer
                                               with iterative refinement. Text detection is used
                                                                                                            severe degradation in spatial reasoning, particularly when
                                               only as training-time scaffolding for supervision
                                                                                                            precise bounding box localization is required.
                                               and validation, enabling the final student to oper-
                                               ate as a pure VLM without OCR or detection at in-            This gap persists because current training paradigms are
                                               ference. Across multiple document understanding              misaligned with the requirements of spatial grounding. Stan-
                                               benchmarks, the proposed DocVAL yields consis-               dard fine-tuning and knowledge distillation approaches
                                               tent improvements of up to 6-7 ANLS points over              transfer output distributions or intermediate representa-
                                               comparable compact VLMs. We further introduce                tions (Ahn et al., 2019; Gou et al., 2021), but do not teach
                                               mean Average Precision (mAP) as a localization               how localization decisions are made. As a result, com-
                                               metric for document question answering and re-               pact models often produce plausible answers without reli-
                                               port strong spatial grounding performance under              ably grounding them in the document. This issue is further
                                               this new evaluation. We release 95K validator-               compounded by commonly used evaluation metrics such as
                                               verified CoT traces and show that high-quality,              ANLS (Li & Liu, 2007), which emphasize textual correct-
                                               validated supervision is more effective than scal-           ness while largely ignoring spatial precision. The outcome
                                               ing unfiltered data, enabling efficient and trustwor-        is a growing trust gap: models appear accurate, yet fail
                                               thy document grounding. Code/Data: GitHub.                   to provide verifiable, location-aware predictions, which is
                                                                                                            particularly problematic in safety-critical domains such as
                                           *
                                            Equal contribution 1 Department of Computer Science and         healthcare, law, and finance, where hallucinated or weakly
                                         Engineering, Ohio State University, Ohio, US 2 Department          grounded outputs limit the reliability and practical adoption
                                         of Computer Science, University of Central Florida, Florida,       of such systems.
                                         US. Correspondence to: Pinaki Prasad Guha Neogi <guha-
                                         neogi.2@osu.edu>.                                                  In this work, we argue that closing this gap requires trans-
                                                                rd                                          ferring not just answers or coordinates, but explicit spatial
                                         Proceedings of the 43 International Conference on Machine
                                         Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026       reasoning processes. We introduce DocVAL, a validated
                                         by the author(s).                                                  chain-of-thought (CoT) distillation framework that enables

                                                                                                        1
                        DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA




Figure 1. Overview of the DocVAL Framework. A three-phase pipeline for validated chain-of-thought (CoT) distillation.
 Phase A: Teacher Data Generation —The teacher VLM (Gemini 2.5 Pro) generates CoT traces from raw documents, which are
filtered by DocVAL for quality assurance. Phase B1: Student Fine-Tuning —A smaller VLM (Gemma3-12B) is fine-tuned on the
validated CoT dataset. Phase B2: Instruction Tuning —The student model iteratively refines its reasoning with DocVAL feedback
until convergence. Phase C: Evaluation —The final model generates stepwise reasoning to produce the answer and bounding boxes.


compact VLMs to acquire strong document grounding ca-                  Figure 1 illustrates the DocVAL pipeline. In Phase A, a large
pabilities by explicitly supervising intermediate spatial rea-         teacher VLM generates spatial CoT traces that are validated
soning steps through quality-controlled reasoning transfer.            using text detection solely as training-time scaffolding for
Unlike generic visual reasoning, document spatial ground-              supervision and filtering. In Phase B, a compact student
ing is inherently compositional: models must identify rel-             is trained in two stages: first through supervised learning
evant text regions, reason about their relative layout, and            on validated CoT traces, and then through validation-driven
translate this reasoning into precise pixel-level coordinates.         iterative refinement using structured feedback. In Phase
Chain-of-thought reasoning is particularly well-suited to              C, the final student performs document question answering
this setting because it externalizes intermediate spatial deci-        with spatial grounding as a pure VLM, requiring no auxiliary
sions—such as locating candidate regions, verifying seman-             models at inference.
tic alignment, and refining boundaries—that are otherwise
                                                                       Beyond the training framework, DocVAL introduces a new
implicit in end-to-end coordinate regression. Prior work has
                                                                       dataset of 95K high-quality, validator-verified CoT traces,
shown that CoT improves structured reasoning by exposing
                                                                       each aligned with answer text and bounding box annotations.
intermediate steps (Wei et al., 2022; Shao et al., 2025); in
                                                                       To our knowledge, this is the first large-scale dataset that
the document domain, these steps naturally correspond to
                                                                       couples document-level chain-of-thought reasoning with
spatial operations over layout and geometry. By supervis-
                                                                       explicit spatial supervision. Importantly, our experiments
ing these intermediate spatial descriptions, rather than only
                                                                       across multiple benchmark datasets demonstrate that data
final answers or bounding boxes, DocVAL provides a princi-
                                                                       quality outweighs data quantity: training on larger but un-
pled mechanism for transferring spatial reasoning processes
                                                                       validated reasoning data degrades localization performance,
from large teacher models to compact, deployable students.
                                                                       while a smaller set of validated examples yields substan-
DocVAL further draws inspiration from validation-driven
                                                                       tially higher accuracy and efficiency. This finding highlights
learning (Madaan et al., 2023), adapting it to the unique
                                                                       the importance of validation-aware dataset construction for
challenges of spatial reasoning in document understanding.
                                                                       reasoning-based fine-tuning.
Key insight. Spatial grounding can be effectively distilled
                                                                       Our main contributions are:
when four conditions are met: (1) teacher models express
reasoning as explicit spatial descriptions rather than opaque             • We propose DocVAL, a validated chain-of-thought
coordinate predictions; (2) training data is rigorously filtered            distillation framework that transfers spatial reason-
to remove hallucinated boxes and inconsistent reasoning;                    ing from large teacher models to compact, deployable
(3) student errors are corrected through actionable, pixel-                 VLMs.
level feedback rather than binary scores; and (4) students
are trained to predict bounding boxes directly from visual                • We incorporate VAL, a rule-based dual-mode validator,
inputs, without relying on detection or OCR at inference                    to adapt validation-driven learning to document spatial
time. DocVAL is explicitly designed to satisfy all four                     grounding by filtering low-quality supervision and pro-
conditions.                                                                 viding fine-grained, pixel-level feedback for iterative
                                                                            refinement.

                                                                   2
                        DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

   • We present a new dataset of 95K validator-verified                2.2. Reasoning, Distillation, and Validation
     CoT traces for document question answering with
                                                                       Chain-of-thought (CoT) prompting (Wei et al., 2022) and
     spatial grounding.
                                                                       its extensions to vision-language models (Xu et al., 2025;
                                                                       Zheng et al., 2023) demonstrate that explicit step-by-step
   • Through extensive ablations across multiple bench-                reasoning can improve model performance. However, exist-
     marks and data scales, we show that validation-driven,            ing approaches primarily focus on semantic or logical rea-
     high-quality supervision is substantially more data-              soning and provide limited support for document-specific
     efficient than unvalidated training, enabling strong              spatial reasoning. Moreover, CoT traces are typically treated
     spatial localization with significantly fewer training            as supervision without verification, which is particularly
     examples and without OCR or detection at inference.               problematic in document understanding, where unvalidated
                                                                       reasoning can include hallucinated regions, inconsistent spa-
The remainder of this paper is organized as follows: Sec-              tial relations, or incorrect coordinate references that propa-
tion 2 reviews related work; Section 3 details the DocVAL              gate noise during training.
framework; Section 4 describes experimental setup and                  This limitation is compounded in knowledge distillation
datasets; Section 5 presents results and ablations; and Sec-           settings. Traditional distillation methods (Gou et al., 2021;
tion 6 presents the conclusion.                                        Ji et al., 2021; Lei & Tao, 2023) and recent VLM distilla-
                                                                       tion approaches (Li et al., 2024; 2023) focus on transferring
                                                                       representations or output distributions, but do not explicitly
2. Related Work                                                        teach how spatial localization decisions are made. Rationale
2.1. Document Understanding and Spatial Grounding                      distillation (Gupta et al., 2023) incorporates explanations,
                                                                       yet typically lacks mechanisms to ensure the correctness or
Early document understanding models such as Lay-                       consistency of those explanations. Concurrent document
outLM (Xu et al., 2020a) and its successors (Xu et al.,                VQA distillation efforts have explored compiling agentic
2020b; Huang et al., 2022) introduced layout-aware rep-                reasoning pipelines into smaller models, but DocVAL dif-
resentation learning through joint text, image, and layout             fers by making validation central to the supervision loop and
pre-training. More recent approaches follow either OCR-                by explicitly correcting spatial grounding errors through de-
free or OCR-based paradigms. OCR-free models (Kim                      terministic pixel-level feedback. As a result, both reasoning-
et al., 2022; Lee et al., 2023; Mohammadshirazi et al., 2024)          based supervision & distillation pipelines remain vulnerable
integrate text recognition end-to-end but often require high-          to low-quality or misleading training signals.
resolution inputs and incur substantial computational cost.
                                                                       Validation-driven learning offers a promising direction for
OCR-based methods achieve richer spatial integration by
                                                                       addressing these issues. Prior work has explored validation-
encoding bounding boxes or layout tokens (Lu et al., 2024;
                                                                       based feedback in domains such as planning (Verma et al.,
Liao et al., 2024; Luo et al., 2024), but typically rely on ex-
                                                                       2025), but such approaches operate with discrete action
ternal OCR or detection pipelines at inference time. Recent
                                                                       spaces and binary correctness signals, limiting their appli-
agentic and graph-augmented document VQA systems fur-
                                                                       cability to continuous spatial reasoning. DocVAL adapts
ther improve interpretability by decomposing document rea-
                                                                       validation-driven learning to document spatial grounding by
soning into specialized modules or explicitly modeling spa-
                                                                       combining textual accuracy, geometric consistency, and rea-
tial relations, but they typically retain additional inference-
                                                                       soning coherence into a rule-based validator that provides
time components for tool orchestration, graph reasoning, or
                                                                       deterministic filtering and fine-grained corrective feedback.
memory access (Mohammadshirazi et al., 2025a;b).
                                                                       This formulation enables iterative refinement in continuous
Despite strong answer accuracy, most existing systems pro-             spatial domains while avoiding hallucinated supervision and
vide limited support for explicit, interpretable spatial ground-       external grounding dependencies.
ing. Localization decisions are often implicit or tightly cou-
pled to preprocessing modules, making verification difficult
                                                                       3. Methodology
and introducing brittle inference dependencies. In contrast,
our paper demonstrates that compact vision-language mod-               We present DocVAL, a validation-driven reasoning distil-
els can learn end-to-end document grounding when trained               lation framework for learning reliable spatial grounding in
with appropriate reasoning supervision, without relying on             document understanding. Figure 1 provides an overview of
detection at inference. We provide a detailed conceptual               the three-phase training and deployment pipeline. Concep-
comparison of DocVAL relative to grounding-focused work                tually, DocVAL addresses the following challenge: “How
such as DOGR (Zhou et al., 2025) and TRIG (Li et al., 2025)            can a compact vision-language model learn verifiable,
in Appendix F.1.                                                       location-aware reasoning from large teachers, without


                                                                   3
                       DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

inheriting their inference cost or relying on auxiliary                grounded in explicit metrics (e.g., ANLS, IoU), ensures
modules at test time?” DocVAL resolves this by (i) dis-                consistency across iterations, and allows fine-grained, au-
tilling explicit spatial reasoning from a large teacher, (ii)          ditable feedback without introducing an additional learning
rigorously validating and filtering this supervision using             problem. We do not claim that rule-based validation is uni-
a rule-based validator, and (iii) iteratively refining a com-          versally superior; rather, it is well-suited to VAL’s role as
pact student model through validation-driven feedback. We              a training-time assessor providing reliable supervision for
describe each component below.                                         spatial grounding. A sensitivity analysis of VAL’s thresh-
                                                                       olds and component weights is provided in Appendix G.
3.1. Overview of the DocVAL Framework                                  Details about formulation of validation criteria appear in
                                                                       Appendix B.2.
DocVAL operates in three phases:
Phase A (Validated Teacher Trace Generation). A large                  Uses of VAL. Because VAL functions as a validator and
teacher model generates spatial CoT reasoning traces for               assessor rather than a predictive model, we employ it for
document-question pairs. These traces are validated and                two complementary purposes within DocVAL:
filtered using a rule-based validator (VAL) to ensure correct-
ness, grounding fidelity, and reasoning consistency.                     1. Training data curation (Phase A): VAL filters
Phase B (Validation-Driven Student Learning). A com-                        teacher-generated reasoning traces, retaining only high-
pact student model is trained in two stages: (B1) supervised                quality examples for supervised learning.
learning on validated teacher traces, and (B2) iterative re-
                                                                         2. Validation-driven refinement (Phase B2): VAL an-
finement using fine-grained corrective feedback produced
                                                                            alyzes student predictions and generates fine-grained
by VAL.
                                                                            diagnostic feedback to guide iterative correction.
Phase C (Pure VLM Deployment). After training, only
the student model is retained. Inference requires a single             Both uses rely on the same underlying validation architec-
forward pass over the document image and question, with                ture but differ in output granularity, as illustrated in Figure 2.
no OCR, detection, or external validation modules.                     Appendix D illustrates this with the help of an example.
Throughout training, auxiliary tools such as text detection
are used only as scaffolding for validation and supervision.           Asymmetric Validation Design. VAL is permitted to ac-
The final model performs end-to-end spatial reasoning di-              cess detected text regions during training-time validation,
rectly from visual inputs.                                             while the student model never receives region-level inputs.
                                                                       This intentional asymmetry allows VAL to perform pre-
3.2. VAL: Rule-Based Validator for Answer                              cise error diagnostics—such as identifying semantic region
     Localization                                                      mismatches (e.g., Subtotal vs. Total)—while forcing the
                                                                       student to learn spatial grounding purely from visual repre-
At the core of DocVAL is VAL, a rule-based validator de-               sentations. As a result, region information serves only as
signed to enforce quality control over spatial reasoning su-           temporary supervision scaffolding and is fully removed at
pervision and to provide structured, actionable feedback for           inference time.
student refinement. VAL plays a supervisory role during
training: it assesses the correctness of answers, bounding             3.2.1. VALIDATION M ODULES
boxes, and reasoning traces, and identifies specific failure
modes that require correction.                                         VAL consists of five specialized modules:
                                                                       Module 1: OCR Grounding Engine. Matches predicted
Why rule-based validation? VAL is intentionally not im-                bounding boxes to detected text regions using IoU, enabling
plemented as a learned critic. Our goal is not to approximate          semantic verification (e.g., detecting “Subtotal” vs. “Total”
human judgment or to learn an implicit notion of correctness,          confusions) independent of geometric accuracy.
but to provide stable, verifiable, and reproducible supervi-
sion signals during training. In this setting, a learned valida-       Module 2: Answer Validator. Computes textual correct-
tor introduces several challenges: (i) non-deterministic feed-         ness using a weighted combination of ANLS and OCR
back that can vary across training iterations, (ii) susceptibil-       presence:
ity to hallucinated or inconsistent critiques, (iii) difficulty
in providing precise geometric corrections (e.g., pixel-level            Qans = 0.7 · ANLS(ap , agt ) + 0.3 · ⊮[ap ∈ OCR(R)].
bounding box adjustments), and (iv) the risk of compound-
ing errors when a learned validator itself is imperfect. By            Module 3: Bounding Box Validator. Evaluates spatial
contrast, rule-based validation enables deterministic checks           accuracy using IoU and region agreement, and computes a

                                                                   4
                         DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA




Figure 2. VAL Dual-Mode Architecture Comparison. VAL operates in two distinct modes sharing the same 5-module architecture but
differing in output granularity. Left (Filter): Phase A processes teacher outputs (D2 ) at 50 examples/sec, producing binary Accept/Reject
decisions to curate 95K high-quality training examples from 102K raw outputs. Right (Verifier): Phase B2 processes student outputs
(D4 ) at 12 examples/sec during iterative refinement, generating detailed rule-based feedback including specific error messages, pixel-level
corrections (δ), priority-ordered fixes, and corrected outputs. Both modes compute identical quality scores (Q) but Filter uses Q only for
thresholding while Verifier generates comprehensive diagnostic feedback to guide student learning. Refer Appendix D for examples.


pixel-level correction vector                                            0.85 are retained, yielding 95K validated traces (92.7% re-
                                                T                        tention). This curated dataset is split into training, refine-
                δ = [∆x1 , ∆y1 , ∆x2 , ∆y2 ] .
                                                                         ment, and test sets (80/10/10). Complete data flow details
                                                                         appear in Appendix D.
Module 4: Reasoning Validator. Assesses reasoning qual-
ity via three checks: structural completeness, coordinate
                                                                         3.4. Phase B: Validation-Driven Student Learning
consistency, and spatial-language alignment.
Module 5: Feedback Generator. In filtering mode, outputs                 3.4.1. S TAGE B1: S UPERVISED S PATIAL R EASONING
binary accept/reject decisions. In verification mode, gener-                    L EARNING
ates structured natural-language feedback with prioritized               The student model (Gemma3-12B) is trained via supervised
corrections and suggested fixes.                                         fine-tuning on the validated dataset. Given only (I, q) as
                                                                         input, the student learns to generate the full output tuple
3.3. Phase A: Validated Teacher Trace Generation                         (CoT, a, b), where b = [x1 , y1 , x2 , y2 ].
We begin with a dataset D1 of 102,447 document images                    The training objective is standard autoregressive likelihood:
paired with questions and ground-truth answer bounding                                           T
boxes. A large teacher VLM (Gemini 2.5 Pro by default)
                                                                                                 X
                                                                                     LSFT = −           log Pθ (ct | I, q, c<t ),
generates spatial CoT traces conditioned on the document                                          t=1
image, question, and ground truth annotations.
                                                                         —where c denotes the serialized reasoning, answer, and
                                                                         bounding box tokens.
Text Detection for Validation. Text detection (DB-
ResNet (Liao et al., 2020)) is applied solely to enable vali-            This stage teaches student to internalize spatial structure &
dation. Detected regions allow VAL to verify that predicted              reasoning patterns w/o relying on explicit region anchors.
boxes correspond to meaningful text and to generate region-
level semantic feedback. These regions are never used as                 3.4.2. S TAGE B2: I TERATIVE R EFINEMENT WITH VAL
student inputs.                                                                 F EEDBACK
Quality-Based Curation. Each teacher-generated exam-                     To further improve grounding fidelity, we perform
ple is scored by VAL. Examples with quality score Q >                    validation-driven instruction tuning. At each iteration, the

                                                                     5
                       DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

student generates predictions, which are evaluated by VAL             a step size of 0.05. We additionally report IoU@0.5 and
in verification mode. VAL produces structured natural-                IoU@0.75 for interpretability. Since several prior models
language feedback describing errors and pixel-level cor-              do not expose localization outputs, mAP is reported only
rections.                                                             when available. Metric definitions appear in Appendix B.2.
These feedback-augmented examples are added to the train-
ing set, and the student is fine-tuned to incorporate the             4.2. Implementation Details
corrections. This process repeats until convergence or a              Teacher Models. We evaluate both closed-source and
maximum of ηmax = 20 iterations. Unlike prompt-based                  open-source teachers. Closed-source models include Gem-
refinement, this procedure updates model weights, enabling            ini 2.5 Pro (default), GPT-5, Claude 4.5 Sonnet, Gemini 2.5
durable improvements in spatial reasoning. A detailed                 Flash, and GPT-4o. Open-source teachers include Qwen3-
wall-clock and example-pass breakdown comparing Stage                 VL-235B-Thinking and Llama4-400B.
B1, Stage B2, and standard distillation is provided in Ap-
pendix H.                                                             Student Model. Our primary student is Gemma3-12B,
                                                                      with additional experiments on Gemma3-4B. All students
3.5. Phase C: Deployment                                              are fully fine-tuned using AdamW. Training is performed on
                                                                      2×H100 80GB GPUs. Full hyperparameters are provided
At inference time, the trained student model processes a              in Appendix B and Table 5.
document image and question in a single forward pass, pro-
ducing reasoning, answer text, and bounding box predic-               Text Detection. Text detection is performed using DB-
tions. No OCR, detection, teacher, or validator is required.          ResNet (Liao et al., 2020) and is used only during
This yields a compact, efficient, and verifiable document             teacher generation and validation. Alternative detectors
understanding system suitable for real-world deployment.              (CRAFT (Baek et al., 2019), PSENet (Wang et al., 2019),
                                                                      EasyOCR) are evaluated in ablations. No detection is used
                                                                      during student inference.
4. Experiments
Our experimental evaluation is designed to answer three               Baselines. We compare against recent OCR-based and
questions:                                                            OCR-free document understanding models, including Do-
                                                                      cLayLLM (Liao et al., 2024), LayoutLLM (Luo et al., 2024),
  1. Does DocVAL improve both answer accuracy and spa-                LayTextLLM (Lu et al., 2024), DLaVA (Mohammadshi-
     tial grounding compared to existing VLMs?                        razi et al., 2024), and ARIAL (Mohammadshirazi et al.,
                                                                      2025a), together with strong general-purpose VLMs such
  2. Which components of DocVAL are responsible for
                                                                      as InternVL3.5, Qwen3-VL, and Llama-Vision variants.
     these gains?
                                                                      These baselines were selected to cover the main competing
  3. How do data quality, data scale, and model capacity              paradigms for document VQA: OCR-based layout-aware
     affect spatial reasoning performance?                            models, OCR-free end-to-end VLMs, document-specific
                                                                      localization systems, and recent general VLMs with strong
                                                                      multimodal reasoning capability. This provides a balanced
4.1. Datasets and Evaluation Metrics
                                                                      comparison across models that differ in their use of OCR,
Datasets. We evaluate on five widely used document un-                layout tokens, localization modules, and model scale. We
derstanding benchmarks: DocVQA (Mathew et al., 2021),                 also include controlled ablations that remove key DocVAL
VisualMRC (Tanaka et al., 2021), FUNSD (Jaume et al.,                 components to isolate the effect of validated reasoning su-
2019), CORD (Park et al., 2019), and SROIE (Huang et al.,             pervision, VAL filtering, and iterative feedback-based re-
2019). Together, these datasets cover diverse document                finement.
types including scanned forms, receipts, invoices, and web-
based documents. Across all datasets, we construct an initial         5. Results
pool of 102,447 examples (D1 ). After teacher generation
and validation filtering (Section 3.2), 95K examples remain           5.1. Main Results
and are split into training (D3 , 76K), refinement (D4 , 9.5K),
                                                                      Table 1 summarizes performance across all benchmarks.
and held-out test sets (Dtest , 9.5K).
                                                                      DocVAL consistently improves both answer accuracy
                                                                      and spatial grounding, establishing state-of-the-art results
Evaluation Metrics. We report answer accuracy using                   among compact, end-to-end, OCR-free-at-inference VLMs,
ANLS (Li & Liu, 2007). To evaluate spatial grounding, we              while also outperforming strong modular grounding base-
introduce mean Average Precision (mAP) over bounding                  lines on overlapping benchmarks (see Appendix F for a
boxes, computed across IoU thresholds from 0.5 to 0.95 with           detailed breakdown).

                                                                  6
                        DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

Table 1. Performance comparison on Document VQA benchmarks. DocVAL operates as pure VLM without text detection at inference.
†
  Uses OCR at inference; not directly comparable to compact OCR-free VLMs. Best results per size category in bold.

                                                            DocVQA             VisualMRC        FUNSD            CORD           SROIE
 Method                    Model Size     OCR@Inf
                                                           ANLS mAP           ANLS mAP        ANLS mAP         ANLS mAP       ANLS mAP
 Prior Work
 DocLayLLM                 Llama3-7B            ✗          78.4       -        55.0     -     84.1     -       71.3    -       84.3     -
 LayoutLLM                Vicuna1.5-7B          ✗          74.3       -        55.8     -     80.0     -       63.1    -       72.1     -
 LayTextLLM                Llama2-7B            ✗          77.2       -        41.7     -     81.0     -       82.5    -       96.1     -
 DLaVA                     Pixtral-12B          ✗          85.9      46.2      52.1     -     87.6    45.5     84.4   57.9     91.4     -
 ARIAL                    Gemma3-27B            ✓          88.7      50.1       -       -     90.0    50.3     85.5   60.2     93.1     -
 VLMs (4B-8B)
 Qwen3-VL-8B-Thinking          8B               ✗          80.4       -        53.8     -     84.1     -       80.7    -       86.3    -
 InternVL3.5-8B                8B               ✗          79.9       -        52.6     -     85.3     -       82.9    -       90.8    -
 Gemma3-4B                     4B               ✗          78.6       -        51.1     -     81.9     -       78.3    -       87.4    -
 DocVAL (Gemma3-4B)            4B               ✗          88.7      69.1      58.4    50.1   86.0    72.3     85.6   70.2     93.1   71.8
 VLMs (11B-14B)
 Llama-3.2-11B-Vision         11B               ✗          83.2       -        54.4     -     86.4     -       81.6    -       90.7    -
 InternVL3.5-14B              14B               ✗          84.7       -        57.1     -     85.9     -       84.1    -       91.6    -
 Gemma3-12B                   12B               ✗          84.6       -        56.1     -     86.9     -       85.3    -       92.4    -
 DocVAL (Gemma3-12B)          12B               ✗          91.4      82.4      73.7    68.8   92.2    81.8     88.8   78.1     95.2   79.6

                                         Table 2. Validation strategy ablation across datasets.

                                          DocVQA              VisualMRC                 FUNSD            CORD                  SROIE
  Validation Mode
                                        ANLS mAP             ANLS mAP                 ANLS mAP         ANLS mAP              ANLS mAP
  No validation (102K data)              88.1       63.7          70.4       53.3     89.1     64.2     85.6      66.4       92.2     65.1
  VAL Filter only (binary)               89.5       76.1          71.6       64.7     90.3     69.9     86.9      71.3       93.4     70.9
  VAL Filter & Verifier (detailed)       91.4       82.4          73.7       68.8     92.2     81.8     88.8      78.1       95.2     79.6


On DocVQA, DocVAL with Gemma3-12B achieves 91.4%                             Efficiency at Smaller Scales. The 4B DocVAL variant
ANLS and 82.4% mAP, improving over the base Gemma3-                          achieves 88.7% ANLS and 69.1% mAP on DocVQA, out-
12B by +6.8 ANLS points and introducing strong spatial                       performing larger 8B models by a wide margin. Relative
grounding where prior models do not report mAP. Compared                     to the base Gemma3-4B, DocVAL improves accuracy by
to InternVL3.5-14B (84.7% ANLS), DocVAL improves                             +10.1 ANLS points, demonstrating that validated reasoning
accuracy by +6.7 points while additionally providing precise                 transfer can compensate for reduced model capacity.
localization.
These gains generalize across datasets, including +17.6                      5.2. Ablation Studies
mAP on FUNSD and +20.2 mAP on VisualMRC rela-                                The ablations in Tables 2, 3, and 7 together cover the key
tive to the strongest available baselines. Notably, DocVAL                   standard distillation baselines. Specifically, “w/o teacher
achieves these improvements without relying on OCR or                        CoT” corresponds to direct answer/box supervision; “No
detection at inference time.                                                 validation” to unfiltered teacher-output distillation; and
ARIAL (Mohammadshirazi et al., 2025a) is the strongest di-                   “Phase B1 only” to one-shot rationale distillation without
rectly comparable grounding-focused baseline, explicitly op-                 iterative refinement. This allows us to isolate the gains
timizing answer localization via an agentic modular pipeline                 from validated, iterative reasoning transfer rather than from
with OCR at inference. Despite using a 2.3× larger back-                     additional supervision alone.
bone (Gemma3-27B + TrOCR) and a hard OCR dependency
at inference, ARIAL achieves 88.7 ANLS and 50.1 mAP                          5.2.1. T EXT D ETECTION A NALYSIS
on DocVQA. DocVAL (Gemma3-12B) surpasses this with                           Text detection is used only during training for teacher gen-
91.4 ANLS and 82.4 mAP—a +32.3 mAP gain—while                                eration & validation, and is never provided to the student
operating as a pure VLM with no OCR at inference. This                       at inference. As shown in Table 6 & Appendix E.1, re-
confirms that validated spatial CoT distillation is a more ef-               moving detection from Phase A causes a substantial drop
fective path to precise answer localization than OCR-based                   in localization performance (DocVQA mAP: 82.4 → 74.1,
region matching, even at a fraction of the model size (see                   –8.3), confirming that detection-guided teacher reasoning &
Appendix F for the per-benchmark breakdown).                                 region-based VAL feedback are critical for curating high-


                                                                         7
                        DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

                                          Table 3. Training strategy ablation across datasets.

                                      DocVQA             VisualMRC                  FUNSD               CORD               SROIE
     Training Config
                                    ANLS mAP            ANLS mAP                  ANLS mAP            ANLS mAP           ANLS mAP
     Phase B1 only (no iteration)      88.3      72.7      72.2          60.4      90.1      70.8      86.1      69.2     92.3   70.4
     B1 + B2 (5 iterations)            88.8      74.3      72.2          62.6      89.9      74.7      86.5      72.3     93.1   73.8
     B1 + B2 (10 iterations)           90.3      78.9      72.6          66.4      91.4      79.2      88.0      76.2     94.5   78.1
     B1 + B2 (converged)               91.4      82.4      73.7          68.8      92.2      81.8      88.8      78.1     95.2   79.6
       (iterations)                    (14)      (14)      (16)          (16)      (13)      (13)      (12)      (12)     (11)   (11)

Table 4. Data scale ablation across datasets. Performance of DocVAL (Gemma3-12B) trained on varying proportions of the validated CoT
dataset D3 . All configurations use full iterative refinement on D4 (9.5K). Best results in bold.

                                              DocVQA              VisualMRC                FUNSD                CORD
                  Data Scale    Size     ANLS       mAP       ANLS              mAP    ANLS         mAP       ANLS      mAP
                  25%           19K       86.2      64.8          68.4          54.2      87.8      66.3      83.7      62.1
                  50%           38K       88.9      73.6          71.1          61.7      89.9      74.1      86.3      70.8
                  75%           57K       90.4      78.9          72.8          65.9      91.4      78.6      87.9      75.3
                  100%          76K       91.4      82.4          73.7          68.8      92.2      81.8      88.8      78.1


quality supervision. Based on the analysis of the results in               date the effectiveness of the dual-mode VAL architecture.
Table 6, we use DB-ResNet for all reported experiments,
while the final student remains a pure VLM at inference.                   5.2.4. T RAINING S TRATEGY
                                                                           Table 3 analyzes training configurations. Stage B1 only
5.2.2. T EACHER M ODEL A NALYSIS                                           (supervised learning without iteration) achieves 88.3 ANLS
                                                                           and 72.7 mAP on DocVQA—establishing baseline spatial
Teacher model choice strongly impacts student ground-
                                                                           reasoning capabilities but leaving substantial room for im-
ing quality. As summarized in Table 7 (Appendix E.2),
                                                                           provement. Adding iterative refinement yields progressive
reasoning-capable teachers consistently outperform non-
                                                                           gains: 5 iterations reach 74.3 mAP (+1.6), 10 iterations 78.9
reasoning variants. Gemini 2.5 Pro yields the strongest
                                                                           mAP (+6.2), and convergence at 14 iterations reaches 82.4
results (91.4 ANLS, 82.4 mAP on DocVQA), while remov-
                                                                           mAP (+9.7).
ing explicit teacher reasoning traces during distillation re-
sults in a large localization drop (–17.0 mAP). These results
                                                                           5.2.5. DATA S CALE A NALYSIS
indicate that explicit reasoning traces are essential for trans-
ferring spatial grounding, beyond what answer or coordinate                Table 4 examines how training data volume affects DocVAL
supervision alone can provide.                                             performance. We train the student model on 25%, 50%,
                                                                           75%, and 100% of D3 (corresponding to 19K, 38K, 57K,
5.2.3. VALIDATION S TRATEGY A NALYSIS                                      and 76K validated CoT traces respectively), while maintain-
                                                                           ing the full iterative refinement procedure on D4 . This setup
Table 2 evaluates the impact of validation strategy. Training
                                                                           isolates the impact of supervised learning data quantity from
on unfiltered teacher outputs (102K examples without VAL
                                                                           the effects of validation-driven refinement.
Filter) yields 88.1 ANLS and 63.7 mAP on DocVQA—18.7
mAP below full DocVAL. This substantial gap demonstrates                   The results reveal a consistent positive correlation between
that low-quality traces containing coordinate hallucinations               data scale and performance across all benchmarks. On
or reasoning inconsistencies significantly impair learning.                DocVQA, scaling from 25% to 100% yields substantial
                                                                           gains: +5.2 ANLS points (86.2→91.4) and +17.6 mAP
Applying VAL Filter in binary mode improves performance
                                                                           (64.8→82.4). Notably, spatial grounding (mAP) benefits
to 89.5 ANLS and 76.1 mAP by removing problematic
                                                                           more dramatically from increased data than textual accu-
examples. Further incorporating the VAL Verifier with de-
                                                                           racy (ANLS), suggesting that learning precise coordinate
tailed feedback achieves 91.4 ANLS and 82.4 mAP, adding
                                                                           regression requires more diverse training examples than se-
+6.3 mAP over binary filtering alone. These gains confirm
                                                                           mantic understanding. While the 25% configuration (19K
that actionable, pixel-level corrections and priority-ordered
                                                                           examples) achieves reasonable ANLS (86.2%), it struggles
fixes enable substantially more effective learning than coarse
                                                                           significantly with localization (64.8 mAP), indicating that
quality filtering. The consistent improvements across all
                                                                           spatial reasoning requires sufficient training diversity to
datasets (4.1–11.9 mAP gains from detailed feedback) vali-

                                                                     8
                          DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

generalize effectively.                                               is OCR-free at inference), detector failures affect supervi-
                                                                      sion quality rather than the deployed inference pipeline. We
Cross-dataset analysis reveals distinct scaling dynamics.
                                                                      expand on this scope and on VAL’s robustness to its own
VisualMRC shows the steepest improvement curve (+14.6
                                                                      design choices in Appendix G and Appendix H.
mAP from 25% to 100%), likely because its web-based
documents exhibit greater layout diversity that benefits from
larger training sets. FUNSD and CORD demonstrate more                 6. Conclusion
gradual improvements (+15.5 and +16.0 mAP respectively),              We introduced DocVAL, a validated chain-of-thought dis-
suggesting that form-based documents contain more regular             tillation framework that enables compact vision-language
spatial patterns that can be learned from fewer examples.             models to perform precise spatial grounding in document un-
Importantly, even at 50% data (38K examples), DocVAL                  derstanding tasks. By combining reasoning-focused teacher
achieves 73.6 mAP on DocVQA—already surpassing the                    supervision, rule-based multi-aspect validation, and iterative
unvalidated baseline’s 63.7 mAP (Table 2) trained on the              refinement, DocVAL transfers spatial reasoning capabilities
full 102K examples.                                                   without introducing inference-time dependencies. Our re-
                                                                      sults demonstrate that explicit, quality-controlled reasoning
Finally, a marginal returns analysis shows diminishing but
                                                                      transfer outperforms implicit feature distillation and unfil-
consistent gains as data increases. The 25%→50% jump
                                                                      tered scaling. DocVAL establishes a general template for
provides +8.8 mAP on DocVQA, 50%→75% adds +5.3
                                                                      distilling structured reasoning from large models into ef-
mAP, and 75%→100% contributes +3.5 mAP. This pattern
                                                                      ficient, deployable systems, with implications extending
indicates that while performance continues to improve with
                                                                      beyond documents to grounded vision-language reasoning
scale, the validated CoT approach extracts substantial value
                                                                      more broadly. As future work, we plan to extend validation-
from limited data—a critical property for domains where
                                                                      driven distillation to more complex document reasoning set-
annotation is expensive. The interaction between data scale
                                                                      tings, such as multi-hop questions and long-form documents,
and iterative refinement merits further investigation: prelim-
                                                                      while exploring hybrid validators that retain the reliability
inary experiments suggest that refinement partially compen-
                                                                      of rule-based supervision with greater flexibility. An orthog-
sates for limited initial data, though this effect saturates at
                                                                      onal direction is to combine validated reasoning transfer
very low data scales (<25%).
                                                                      with model-compression and routing-aware specialization
                                                                      techniques, including expert pruning in mixture-of-experts
5.3. Discussion
                                                                      models, to further reduce inference cost while preserving
Validated Reasoning as the Core Driver. Across all ab-                grounded reasoning quality (Neogi et al., 2025a).
lations, the largest gains arise from explicit, validated rea-
soning transfer. The combination of CoT supervision and               Impact Statement
multi-aspect validation prevents error propagation and en-
ables precise spatial learning.                                       This paper presents DocVAL, a validated chain-of-thought
                                                                      distillation framework for grounded Document VQA. By
Why Pure VLMs Can Work. Our results challenge the                     encouraging both answer correctness and spatial consis-
assumption that document understanding requires perma-                tency during training, DocVAL aims to reduce ungrounded
nent OCR or layout modules. With appropriate supervision,             outputs and make document understanding models more
VLMs can internalize spatial representations sufficient for           verifiable and practical in deployment, including settings
pixel-level localization.                                             where OCR-based pipelines may be brittle or unavailable.
Implications Beyond Documents. The DocVAL                             DocVAL may have positive societal impact by supporting
paradigm generalizes to tasks requiring grounded and                  human verification and auditability in high-stakes workflows
decision-centric reasoning, including referring expressions,          (Neogi et al., 2025c) such as finance, healthcare, and legal
embodied perception, robotic manipulation, and high-stakes            document processing, where errors can be costly. At the
multimodal forecasting where calibrated evidence and                  same time, document understanding models may be misused
confidence is important (Neogi et al., 2025b). The key                for privacy-invasive information extraction or relied upon
insight—validated reasoning transfer—extends beyond                   for automated decision-making without appropriate over-
document understanding.                                               sight. We encourage responsible deployment with human-
Scope and Limitations. DocVAL’s benchmarks span                       in-the-loop review, access controls, and privacy-aware data
scanned forms, receipts, invoices, and web documents, but             handling. Overall, we believe the primary impact of this
do not fully cover handwriting-heavy pages, severely de-              work is to advance reliable and interpretable machine learn-
graded scans, or chart-dominant layouts where both detector           ing for grounded document understanding.
quality and teacher reasoning degrade. Because text detec-
tion serves only as training-time scaffolding (the student

                                                                  9
                       DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

References                                                            Lee, K., Joshi, M., Turc, I. R., Hu, H., Liu, F., Eisensch-
                                                                        los, J. M., Khandelwal, U., Shaw, P., Chang, M.-W.,
Ahn, S., Hu, S. X., Damianou, A., Lawrence, N. D., and
                                                                        and Toutanova, K. Pix2struct: Screenshot parsing as
  Dai, Z. Variational information distillation for knowledge
                                                                        pretraining for visual language understanding. In Inter-
  transfer. In Proceedings of the IEEE/CVF conference on
                                                                        national Conference on Machine Learning, pp. 18893–
  computer vision and pattern recognition, pp. 9163–9171,
                                                                        18912. PMLR, 2023.
  2019.
                                                                      Lei, S. and Tao, D. A comprehensive survey of dataset
Baek, Y., Lee, B., Han, D., Yun, S., and Lee, H. Character
                                                                        distillation. IEEE Transactions on Pattern Analysis and
  region awareness for text detection. In Proceedings of the
                                                                        Machine Intelligence, 46(1):17–32, 2023.
  IEEE/CVF conference on computer vision and pattern
  recognition, pp. 9365–9374, 2019.                                   Li, M., Zhang, R., Chen, J., Gu, J., Zhou, Y., Dernoncourt,
                                                                        F., Zhu, W., Zhou, T., and Sun, T. Towards visual text
Gou, J., Yu, B., Maybank, S. J., and Tao, D. Knowledge                  grounding of multimodal large language model. arXiv
  distillation: A survey. International journal of computer             preprint arXiv:2504.04974, 2025.
  vision, 129(6):1789–1819, 2021.
                                                                      Li, X., Fang, Y., Liu, M., Ling, Z., Tu, Z., and Su, H. Distill-
Guha Neogi, P. P. Edge–texture-based characteristic at-                  ing large vision-language model with out-of-distribution
  tribute on local radius of gyration face for human face                generalizability. In Proceedings of the IEEE/CVF Inter-
  recognition. In Proceedings of the Global AI Congress                  national Conference on Computer Vision, pp. 2492–2503,
 2019, pp. 263–273. Springer, 2020.                                      2023.
Gupta, A., Saini, S., and Narayanan, P. Concept distillation:         Li, Y. and Liu, B. A normalized Levenshtein distance
  leveraging human-centered explanations for model im-                  metric. IEEE Transactions on Pattern Analysis and
  provement. Advances in Neural Information Processing                  Machine Intelligence, 29(6):1091–1095, 2007. doi:
  Systems, 36:63724–63737, 2023.                                        10.1109/TPAMI.2007.1078.
Huang, Y., Lv, T., Cui, L., Lu, Y., and Wei, F. Layoutlmv3:           Li, Z., Li, X., Fu, X., Zhang, X., Wang, W., Chen, S., and
  Pre-training for document ai with unified text and image              Yang, J. Promptkd: Unsupervised prompt distillation for
  masking. In Proceedings of the 30th ACM International                 vision-language models. In Proceedings of the IEEE/CVF
 Conference on Multimedia, pp. 4083–4091, 2022.                         Conference on Computer Vision and Pattern Recognition,
                                                                        pp. 26617–26626, 2024.
Huang, Z., Chen, K., He, J., Bai, X., Karatzas, D., Lu,
  S., and Jawahar, C. Icdar2019 competition on scanned                Liao, M., Wan, Z., Yao, C., Chen, K., and Bai, X. Real-time
  receipt ocr and information extraction. In 2019 Interna-              scene text detection with differentiable binarization. In
  tional Conference on Document Analysis and Recognition                Proceedings of the AAAI conference on artificial intelli-
 (ICDAR), pp. 1516–1520. IEEE, 2019.                                    gence, volume 34, pp. 11474–11481, 2020.
Jaume, G., Ekenel, H. K., and Thiran, J.-P. Funsd: A dataset          Liao, W., Wang, J., Li, H., Wang, C., Huang, J., and Jin,
  for form understanding in noisy scanned documents. In                 L. Doclayllm: An efficient and effective multi-modal ex-
  2019 International Conference on Document Analysis                    tension of large language models for text-rich document
  and Recognition Workshops (ICDARW), volume 2, pp.                     understanding. arXiv preprint arXiv:2408.15045, 2024.
  1–6. IEEE, 2019.
                                                                      Lu, J., Yu, H., Wang, Y., Ye, Y., Tang, J., Yang, Z., Wu,
Ji, M., Heo, B., and Park, S. Show, attend and distill: Knowl-          B., Liu, Q., Feng, H., Wang, H., et al. A bounding box
   edge distillation via attention-based feature matching. In           is worth one token: Interleaving layout and text in a
   Proceedings of the AAAI conference on artificial intelli-            large language model for document understanding. arXiv
   gence, volume 35, pp. 7945–7952, 2021.                               preprint arXiv:2407.01976, 2024.

Kar, A. and Neogi, P. P. G. Triangular coil pattern of local          Luo, C., Shen, Y., Zhu, Z., Zheng, Q., Yu, Z., and Yao, C.
  radius of gyration face for heterogeneous face recognition.           Layoutllm: Layout instruction tuning with large language
 Applied Intelligence, 50(3):698–716, 2020.                             models for document understanding. In Proceedings
                                                                        of the IEEE/CVF Conference on Computer Vision and
Kim, G., Hong, T., Yim, M., Nam, J., Park, J., Yim, J.,                 Pattern Recognition, pp. 15630–15640, 2024.
  Hwang, W., Yun, S., Han, D., and Park, S. Ocr-free docu-
  ment understanding transformer. In European Conference              Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao,
  on Computer Vision, pp. 498–517. Springer, 2022.                     L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S.,

                                                                 10
                       DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

  Yang, Y., et al. Self-refine: Iterative refinement with self-          Workshop on Computational Optimization of Buildings,
  feedback. Advances in Neural Information Processing                    2025.
  Systems, 36:46534–46594, 2023.
                                                                       Neogi, P. P. G., Goswami, S., and Mustafi, J. Intelligent
Mathew, M., Karatzas, D., and Jawahar, C. V. Docvqa:                     water drops-based image steganography. In Proceedings
 A dataset for vqa on document images. In Proceedings                    of the Global AI Congress 2019, pp. 363–375. Springer,
 of the IEEE/CVF Winter Conference on Applications of                    2020.
 Computer Vision (WACV), pp. 2200–2209, 2021.
                                                                       Neogi, P. P. G., Mohammadshirazi, A., Kulshrestha, D., and
Mohammadshirazi, A., Neogi, P. P. G., Lim, S.-N., and
                                                                         Ramnath, R. Exploiting the experts: Unauthorized com-
 Ramnath, R. Dlava: Document language and vision assis-
                                                                         pression in moe-llms. arXiv preprint arXiv:2511.19480,
 tant for answer localization with enhanced interpretability
                                                                         2025a.
 and trustworthiness. arXiv preprint arXiv:2412.00151,
 2024.
                                                                       Neogi, P. P. G., Mohammadshirazi, A., and Ramnath, R.
Mohammadshirazi, A., Neogi, P. P. G., Kulshrestha, D.,                   Alco-fm: Adaptive long-context foundation model for
 and Ramnath, R. Arial: An agentic framework for docu-                   accident prediction. arXiv preprint arXiv:2507.08153,
 ment vqa with precise answer localization. arXiv preprint               2025b.
 arXiv:2511.18192, 2025a.
                                                                       Neogi, P. P. G., Mohammadshirazi, A., and Ramnath, R. In-
Mohammadshirazi, A., Neogi, P. P. G., Kulshrestha, D., and               sightbuild: Llm-powered causal reasoning in smart build-
 Ramnath, R. Mga-vqa: Secure and interpretable graph-                    ing systems. arXiv preprint arXiv:2507.08235, 2025c.
 augmented visual question answering with memory-
 guided protection against unauthorized knowledge use.                 Park, S., Shin, S., Lee, B., Lee, J., Surh, J., Seo, M., and
 arXiv preprint arXiv:2511.17881, 2025b.                                 Lee, H. Cord: A consolidated receipt dataset for post-
                                                                         ocr parsing. In Workshop on Document Intelligence at
Mohammadshirazi, A., Neogi, P. P. G., and Ramnath, R.                    NeurIPS, 2019.
 Piad-srnn: Physics-informed adaptive decomposition in
 state-space rnn. In International Conference on Machine               Shao, H., Qian, S., Xiao, H., Song, G., Zong, Z., Wang,
 Learning, 2025c.                                                        L., Liu, Y., and Li, H. Visual cot: Advancing multi-
Nath, S., Neogi, P. P. G., Sing, J. K., and Sarkar, S. K.                modal language models with a comprehensive dataset and
  Vlsi routing optimization based on modified constricted                benchmark for chain-of-thought reasoning. Advances in
  pso with iterative rlc delay model. In 2018 International              Neural Information Processing Systems, 37:8612–8642,
  Conference on Current Trends towards Converging Tech-                  2025.
  nologies, 2018.
                                                                       Tanaka, R., Nishida, K., and Yoshida, S. Visualmrc: Ma-
Neogi, P. P. G. Novel approach for steiner nodes filtration              chine reading comprehension on document images. In
  in vlsi global routing. In 2019 International Conference               Proceedings of the AAAI Conference on Artificial Intelli-
  on Intelligent Computing and Remote Sensing, 2019a.                    gence, volume 35, pp. 13878–13888, 2021.

Neogi, P. P. G. Cost-effective dynamic workflow scheduling             Verma, P., La, N., Favier, A., Mishra, S., and Shah, J. A.
  in iaas cloud environment. In 2019 International Con-                  Teaching llms to plan: Logical chain-of-thought in-
  ference on Intelligent Computing and Remote Sensing,                   struction tuning for symbolic planning. arXiv preprint
  2019b.                                                                 arXiv:2509.13351, 2025.
Neogi, P. P. G. Iwd-based mobile sink route determination              Wang, W., Xie, E., Li, X., Hou, W., Lu, T., Yu, G., and Shao,
  for wsn under non-uniform data constraints. In 2019                   S. Shape robust text detection with progressive scale
  International Conference on Computer Communication                    expansion network. In Proceedings of the IEEE/CVF
  and Informatics, 2019c.                                               Conference on Computer Vision and Pattern Recognition,
Neogi, P. P. G. Deep learning based solar radiation predic-             pp. 9336–9345, 2019.
  tion models for the pacific northwest. Master’s thesis,
 Washington State University, 2023.                                    Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi,
                                                                        E., Le, Q. V., Zhou, D., et al. Chain-of-thought prompting
Neogi, P. P. G. Multi-scale lstm networks for long-term                 elicits reasoning in large language models. Advances in
  building temperature prediction: A simplified approach                neural information processing systems, 35:24824–24837,
  to complex thermal dynamics. In ICML 2025 CO-BUILD                    2022.

                                                                  11
                       DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

Xu, G., Jin, P., Wu, Z., Li, H., Song, Y., Sun, L., and Yuan,
  L. Llava-cot: Let vision language models reason step-
  by-step. In Proceedings of the IEEE/CVF International
 Conference on Computer Vision, pp. 2087–2098, 2025.
Xu, Y., Li, M., Cui, L., Huang, S., Wei, F., and Zhou, M.
  Layoutlm: Pre-training of text and layout for document
  image understanding. In Proceedings of the 26th ACM
 SIGKDD Conference on Knowledge Discovery & Data
 Mining (KDD), pp. 1192–1200, 2020a. doi: 10.1145/
  3394486.3403172.
Xu, Y., Xu, Y., Lv, T., Cui, L., Wei, F., Wang, G., Lu, Y.,
  Florencio, D., Zhang, C., Che, W., et al. Layoutlmv2:
  Multi-modal pre-training for visually-rich document un-
  derstanding. arXiv preprint arXiv:2012.14740, 2020b.
Zheng, G., Yang, B., Tang, J., Zhou, H.-Y., and Yang, S. Dd-
  cot: Duty-distinct chain-of-thought prompting for multi-
  modal reasoning in language models. Advances in Neural
  Information Processing Systems, 36:5168–5191, 2023.
Zhou, Y., Chen, Y., Lin, H., Wu, Y., Yang, S., Qi, Z., Ma, C.,
  Zhu, L., and Shan, Y. DOGR: Towards versatile visual
  document grounding and referring. In Proceedings of the
  IEEE/CVF International Conference on Computer Vision
  (ICCV), pp. 3596–3606, 2025.




                                                                 12
                      DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

A. Terminology and Design Decisions
CoT Output. Throughout the paper, ”CoT Output” refers to the complete tuple (CoT, a, b) where CoT is step-by-step
spatial reasoning, a is the extracted answer, and b is the predicted bounding box. VAL validates all three components.

Instruction Tuning. Stage B2 employs instruction tuning which updates model weights through gradient descent on
feedback-augmented examples (student mistakes + VAL feedback → corrections). This differs from prompt tuning which
freezes weights and only trains soft embeddings. Spatial reasoning requires modifying visual encoders and coordinate
regression heads, necessitating full weight updates.

Validation-Driven Learning. Stage B2 implements an iterative loop: predict → validate → feedback → retrain. VAL
actively guides improvement through actionable corrections rather than passive scoring, creating dynamic training datasets
that evolve with model capabilities.

Text Region. A detected text instance ri = (bi , ti , i) where bi ∈ R4 are bounding box coordinates, ti is OCR-extracted text,
and i is the region index. Text detection (DB-ResNet) extracts region set R = {r1 , ..., rn } with n ≈ 15-20 per document.
Regions enable VAL’s semantic validation (”Region #7 Subtotal vs Region #2 Total”) but are never given to students, who
must learn text localization through pure visual reasoning.

Detection as Scaffolding. Text detection serves training-time only purposes: (1) guiding teacher CoT generation, (2)
enabling VAL’s semantic validation. Students receive only (I, q) and must develop internal spatial representations. This
asymmetry enables quality supervision while maintaining deployment simplicity.

Design Rationale. We use rule-based VAL for: (1) deterministic consistency across iterations, (2) precise pixel-level
feedback, (3) zero computational cost, (4) objective metrics that cannot hallucinate, and (5) avoiding validation-of-validator
recursion. Iterative refinement enables progressive error correction through feedback targeting actual mistakes. Full fine-
tuning rather than LoRA is necessary as spatial reasoning requires modifying core visual encoders (preliminary experiments
showed 8-12 mAP degradation with parameter-efficient methods).


Broader Applicability Across Constrained Domains. The same principle may be useful in other constrained prediction
settings, including biometric recognition, where geometric and texture cues support verification (Guha Neogi, 2020; Kar &
Neogi, 2020); secure visual communication, where image transformations must preserve hidden-message recoverability
(Neogi et al., 2020); and optimization problems such as VLSI routing, workflow scheduling, and wireless sensor-network
routing, where predictions must satisfy resource, latency, or connectivity constraints (Neogi, 2019a;b;c; Nath et al.,
2018). It may also benefit time-series prediction systems, where reliable forecasts often require models to account for
temporal structure, domain constraints, and interpretable evidence rather than producing black-box predictions (Neogi, 2025;
Mohammadshirazi et al., 2025c; Neogi, 2023). These domains differ from document VQA, but they share a common need
for models whose outputs can be checked against explicit structural, temporal, or domain-specific constraints.

B. Experimental Configuration
B.1. Complete Hyperparameters
Key Configurations. Phase A: Teacher (Gemini 2.5 Pro, temp 0.7) generates 102K CoT traces; DB-ResNet detection
provides 15-20 regions/image for validation only (never given to student). Stage B1: Student (Gemma3-12B) receives
only (I, q) and produces (CoT, a, b); learning rate 2e − 4, effective batch 128, 3 epochs over D3 (76K). Stage B2; 2
                                                                                 ¯ < 0.2 mAP over 3 iterations. Phase C:
epochs/iteration over D4 (9.5K); convergence at 12-16 iterations (avg 13.2) when ∆
Pure VLM inference on consumer GPUs.
Table 5 provides complete configuration across all phases.


B.2. VAL Scoring Formulas
Complete mathematical formulations for VAL. All formulas use detected regions R for validation but regions are never
provided to students.

                                                             13
                       DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

                                    Table 5. Complete hyperparameter configuration for DocVAL

        Parameter                               Phase A              Stage B1             Stage B2        Phase C
        Student Training
        Model                                     N/A            Gemma3-12B          Gemma3-12B          Gemma3-12B
        Learning Rate                             N/A              2e − 4              2e − 4               N/A
        Batch Size (effective)                    N/A               128                  128                  1
        Sequence Length                           N/A               2048                2048                2048
        Epochs                                    N/A                 3                 2/iter              N/A
        Optimizer                                 N/A              AdamW               AdamW                N/A
        Weight Decay                              N/A               0.01                0.01                N/A
        Warmup Steps                              N/A               500                  200                N/A
        VAL Configuration
        Mode                                 Filter (binary)           N/A         Verifier (detailed)      N/A
        Qmin                                      0.85                 0.85               0.85              N/A
        Weights (αans , αbbox , αreason )     0.4, 0.4, 0.2              -           0.4, 0.4, 0.2          N/A
        Throughput                             50 ex/sec               N/A             12 ex/sec            N/A
        Retention                            92.7% (95K)               N/A                N/A               N/A
        Data Splits
        D3 (Training)                            76,000               76,000                 -                -
        D4 (Validation)                           9,500                  -                 9,500              -
        Dtest (Test)                              9,500                  -                   -              9,500
        Computational Resources
        GPU                                 CPU only (VAL)        H100 80GB              H100 80GB       A100 40GB
        Memory                                64GB RAM              78GB                   72GB            28GB



Quality Scores:

                                      Qans = 0.7 · ANLS(ap , agt ) + 0.3 · ⊮[ap ∈ OCR(R)]                                (1)
                                     Qbbox = 0.8 · IoU(bp , bgt ) + 0.2 · ⊮[rp = rgt ]                                   (2)
                                              Sstruct + Scoord + Sspatial
                                    Qreason =                                                                            (3)
                                                          3
                                         Q = 0.4Qans + 0.4Qbbox + 0.2Qreason                                             (4)


Convergence Detection:

                                                           k
                                            ¯ (k) = 1
                                                           X
                                            ∆                     (mAPj − mAPj−1 )                                       (5)
                                                    w
                                                        j=k−w+1

                                                    ¯ (k) < 0.2 and max ∆(k) < 0.4
                                       Converged ⇐⇒ ∆                                                                    (6)
                                                                         j
                                                                               j


where w = 3 iterations.

B.3. Complete Algorithm
Algorithm 1 provides complete pseudocode with three key design principles: (1) Detection for validation only (line 9), (2)
Student receives only (I, q) without regions (line 35), (3) VAL uses regions for feedback but student learns visually (lines
46-49).

                                                                14
                        DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

Algorithm 1 DocVAL: Validated CoT Distillation
                              gt   gt
 1: Input: D1 = {(Ii , qi , ai , bi )}102447
                                          i=1    , Teacher T , Detector D, Student Mθ0
 2: Output: Fine-tuned student Mθ∗
 3: // Phase A: Teacher Generation + VAL Filter
                          gt gt
 4: for each (Ii , qi , ai , bi ) ∈ D1 do
 5:    Ri ← D(Ii ) {Detection for validation only}
 6:    (CoTTi , aTi , bTi ) ← T (Ii , Ri , qi , agt   gt
                                                 i , bi )
                                        T   T T       gt gt
 7:    if VAL-Filter(Ii , Ri , CoTi , ai , bi , ai , bi ) > 0.85 then
 8:       Dfiltered ← Dfiltered ∪ {(Ii , Ri , qi , CoTTi , aTi , bTi )}
 9:    end if
10: end for
11: Split Dfiltered → D3 (76K), D4 (9.5K), Dtest (9.5K)
12: // Stage B1: Supervised Learning
13: for epoch e = 1 to 3 do
14:    for each (Ii , qi , CoTgt      gt gt
                                i , ai , bi ) ∈ D3 do
15:       // CRITICAL:
                    P         Student gets only (Ii , qi ), no regions
16:       L ← − t log Pθ (ct |Ii , qi , c<t ) where c = [CoT, a, b]
17:       Update θ with AdamW
18:    end for
19: end for
20: // Stage B2: Iterative Refinement
21: for iteration k = 1 to 20 do
22:    for each (Ii , Ri , qi , agt    gt
                                 i , bi ) ∈ D4 do
            (k)   (k)   (k)
23:      (ci , ai , bi ) ← Mθk−1 (Ii , qi ) {No regions to student}
                                          (k) (k) (k)
24:      Fi ← VAL-Verifier(Ii , Ri , ci , ai , bi , agt        gt
                                                          i , bi )
           (k)     (k)                     gt gt gt
25:      Dcorr ← Dcorr ∪ {(Ii , qi , Fi , ci , ai , bi )}
26:   end for
                       (k)
27:   Fine-tune θ on Dcorr for 2 epochs
28:   Evaluate: mAPk on D4
29:   if Converged (Eq. 6) then
30:      break
31:   end if
32: end for
33: return Mθ∗ {Pure VLM}




C. Qualitative Examples
Success: Complex Receipt. Multiple similar amounts (Subtotal: $87.50, Tax: $7.88, Total: $108.51). Student correctly
distinguished ”TOTAL” field, predicted [542,876,618,904]. Result: ANLS=1.0, IoU=1.0 (perfect). Demonstrates semantic
understanding and pixel-accurate localization.
Failure: Multi-Line Address. Three-line address spanning disconnected regions. Student correctly extracted full text
(ANLS=1.0) but bbox covered only first line (IoU=0.31). Single-bbox architectural limitation, not reasoning failure.
Failure: Handwritten Text. Student read handwriting correctly (ANLS=1.0) but bbox imprecise (IoU=0.68 vs. typical
> 0.9 for print). VAL validation during training missed handwritten regions, affecting feedback quality.
Near-Perfect: Structured Form. Tax form with clear grid layout. Student identified ”EIN” label and predicted
[384,187,496,214] vs. GT [385,188,495,213]. ANLS=1.0, IoU=0.98 (1-2px offset). Represents typical performance
on well-structured documents where DocVAL excels.


                                                                 15
                       DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

D. Sample Outputs
D.1. Teacher, Student, and VAL Interaction

  Teacher Generation (Phase A):
  Input: Receipt image, Q: ”What is the total?”
  Regions (for teacher/VAL): 15 detected, including Region #2 [510,800,570,830] → ”$45.99”, Region #14 [445,795,505,825] →
  ”TOTAL:”
  Teacher Output: Step-by-step reasoning referencing regions → Answer: $45.99, BBox: [510,800,570,830]
  VAL Filter: Q = 1.0 > 0.85 → ACCEPT




  Student Prediction (Iteration 3, Stage B2):
  Input (Pure VLM): Same receipt image, Q: ”What is the total?” (NO regions)
  Output: Steps 1-5 (identifies ”SUBTOTAL” instead of ”TOTAL”) → Answer: $42.50, BBox: [760,650,840,680]




  VAL Verifier Feedback:
  Validation: Answer: ANLS=0.167, BBox: IoU=0.0, Reasoning: 0.73, Overall: Q=0.313 → INVALID
  Detailed Feedback:

     • Answer Error: Got ”$42.50” (SUBTOTAL), Expected ”$45.99” (TOTAL). Wrong semantic field.

     • BBox Error: IoU=0.0. Move 250px LEFT, 150px DOWN. Targets Subtotal (middle) instead of Total (lower).

     • Reasoning Issue: Step 3 identified ”SUBTOTAL” when question asks for ”total”. Look for ”TOTAL” label specifically.
     • Priority Fixes: (1) Distinguish Subtotal vs Total fields, (2) Locate ”TOTAL” label in lower section, (3) Adjust bbox position




E. Ablation Studies Experiments
E.1. Text Detection Analysis
Table 6 analyzes the role of text detection during teacher data generation and VAL validation. Removing detection from
Phase A (teacher generation and validation filtering) significantly degrades performance: DocVQA mAP drops from 82.4 to
74.1 (–8.3). This confirms that detection-guided teacher CoT generation and region-based VAL feedback are critical for
maintaining high training data quality. Notably, the student model operates without detection at inference, demonstrating
that high-quality supervision—rather than inference-time dependencies—enables pure VLM spatial reasoning.
Among detection methods, DB-ResNet achieves the best overall performance (82.4 mAP on DocVQA), likely due to its
strong recall for small text regions and efficient processing. CRAFT (80.6 mAP) and PSENet (79.3 mAP) show slightly
lower performance, while EasyOCR (78.7 mAP) struggles with dense text layouts. Removing region references from teacher
CoT while retaining detection for VAL (76.8 mAP) further shows that region-aware reasoning generation contributes beyond
validation alone, highlighting detection’s dual role as both supervision scaffolding and reasoning guide.

                                                                 16
                       DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

       Table 6. Text detection ablation across datasets. Detection used only in Phase A (teacher+VAL), not student inference.

                                      DocVQA             VisualMRC            FUNSD              CORD                SROIE
  Configuration
                                     ANLS mAP           ANLS mAP            ANLS mAP           ANLS mAP            ANLS mAP
  DocVAL (DB-ResNet)                  91.4      82.4     73.7        68.8    92.2      81.8     88.8      78.1      95.2        79.6
  DocVAL (CRAFT)                      90.9      80.6     73.2        67.3    91.6      79.9     88.1      76.4      94.8        78.1
  DocVAL (PSENet)                     90.5      79.3     72.8        66.1    91.1      78.5     87.7      75.2      94.4        77.3
  DocVAL (EasyOCR)                    90.1      78.7     72.3        65.4    90.8      77.8     87.2      74.6      94.1        76.8
  w/o detection (Phase A)             88.7      74.1     70.9        62.2    89.3      73.4     85.9      71.7      92.6        73.9
  w/o region refs in teacher CoT      89.8      76.8     71.8        64.1    90.4      76.2     87.0      73.9      93.5        75.4



E.2. Teacher Model Analysis
Table 7 examines how teacher model choice influences student performance. Gemini 2.5 Pro achieves the strongest results
(91.4 ANLS, 82.4 mAP on DocVQA), producing high-quality reasoning traces that transfer effectively to the student.
Reasoning-focused models (Claude 4.5 Sonnet: 90.8/81.2; GPT-5: 90.3/80.5) consistently outperform non-reasoning
variants (Gemini 2.5 Flash: 88.4/76.1; GPT-4o: 87.9/74.8), confirming that explicit step-by-step reasoning in teacher outputs
is crucial for learning spatial grounding.
Open-source teachers achieve competitive performance as well: Qwen3-VL-235B (90.6/79.8) and Llama4-400B (90.1/78.9)
generate sufficiently high-quality CoT traces for effective distillation. In contrast, the w/o teacher CoT baseline (87.7 ANLS,
65.4 mAP), which uses direct bounding box supervision without reasoning traces, exhibits a 17.0 mAP degradation. This
gap confirms that explicit reasoning transfer—not just answer or coordinate supervision—is essential for spatial grounding.

        Table 7. Teacher model ablation. Student (Gemma3-12B) performance across datasets with different teacher VLMs.

                                    DocVQA              VisualMRC             FUNSD             CORD                SROIE
  Teacher Model
                                   ANLS mAP            ANLS mAP             ANLS mAP          ANLS mAP            ANLS mAP
  Closed-source (reasoning)
  Gemini 2.5 Pro                    91.4      82.4      73.7      68.8      92.2      81.8      88.8     78.1      95.2         79.6
  Claude 4.5 Sonnet                 90.8      81.2      73.1      67.9      91.7      80.6      88.2     77.3      94.8         78.9
  GPT-5                             90.3      80.5      72.6      67.2      91.3      79.8      87.7     76.7      94.4         78.2
  Closed-source (non-reasoning)
  Gemini 2.5 Flash              88.4          76.1      71.2      64.3      89.9      76.7      86.3     73.9      93.3         75.8
  GPT-4o                        87.9          74.8      70.8      63.1      89.4      75.2      85.8     72.6      92.9         74.4
  Open-source
  Qwen3-VL-235B-A22B                90.6      79.8      72.8      66.5      91.4      79.1      88.0     76.2      94.6         77.8
  Llama4-400B-A17B                  90.1      78.9      72.3      65.8      90.9      78.3      87.5     75.4      94.2         77.1
  w/o teacher CoT (direct FT)       87.7      65.4      68.1      58.2      88.2      68.9      86.4     68.7      92.7         71.3



F. ARIAL Comparison: Detailed Breakdown
Table 1 includes ARIAL (Mohammadshirazi et al., 2025a) as a grounding-focused baseline. Here we provide the per-
benchmark breakdown of the gap between DocVAL and ARIAL. ARIAL is an agentic modular pipeline combining TrOCR
for OCR-based text extraction, a retrieval module, a fine-tuned Gemma3-27B QA backbone, and a separate text-to-region
alignment module for localization—making OCR a hard inference-time dependency.
The mAP gap is particularly large because ARIAL grounds via OCR text-region matching, which is bounded by detection
coverage and string-match precision, whereas DocVAL trains the student to perform spatial reasoning directly from visual
inputs via validated CoT distillation. Improvements to ARIAL’s components do not directly address this architectural
limitation.

                                                                17
                      DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

Table 8. Per-benchmark comparison between DocVAL (Gemma3-12B, OCR-free) and ARIAL (Gemma3-27B + TrOCR). DocVAL
outperforms ARIAL on every overlapping benchmark in both ANLS and mAP, using a 2.3× smaller backbone and no OCR at inference.

                                              DocVQA            FUNSD              CORD            SROIE
                     Method
                                            ANLS mAP          ANLS mAP           ANLS mAP          ANLS
                     ARIAL (27B+OCR)         88.7     50.1     90.0     50.3      85.5      60.2     93.1
                     DocVAL (12B)            91.4     82.4     92.2     81.8      88.8      78.1     95.2
                     ∆                       +2.7     +32.3    +2.2     +31.5     +3.3     +17.9     +2.1


F.1. Conceptual Positioning Relative to DOGR and TRIG
Direct numerical comparison with DOGR and TRIG is not feasible because they address related but fundamentally distinct
problems. DOGR targets document grounding and referring—localizing a referenced region given a referring expression—
evaluated on DOGR-Bench (charts, posters, PDFs), not on the DocVQA/FUNSD/CORD/SROIE benchmarks used here.
Its input/output specification differs from DocVAL’s: DOGR takes a region description and outputs a localized region,
whereas DocVAL takes a natural-language question and outputs both an answer and its bounding box. TRIG targets text-rich
image grounding across broader document types and evaluates on TRIG-Bench with different annotation protocols, without
reporting mAP@IoU[0.5:0.95] on our benchmarks.

                                 Table 9. Conceptual comparison: DocVAL vs. DOGR vs. TRIG.

  Dimension                                         DocVAL                             DOGR                  TRIG
  Primary task                        Answer localization in DocVQA             Document referring     Text-rich grounding
  OCR at inference                                   ✗                            Not specified           OCR-assisted
  Pixel-level iterative refinement                  ✓                                  ✗                        ✗
  Inference-time independence                       ✓                                  ✗                        ✗
  Validated CoT distillation                        ✓                                  ✗                        ✗

Neither DOGR nor TRIG targets the specific combination of validated spatial CoT distillation, OCR-free inference, and
compact deployable student training that defines DocVAL. The released 95K validator-verified CoT dataset may also benefit
future work in referring and grounding settings.

G. VAL Sensitivity Analysis
A natural concern with a rule-based validator is whether performance depends sensitively on the specific thresholds and
weights chosen in Appendix B.2. We perform two targeted sensitivity studies on DocVQA to test this.

G.1. Threshold Sensitivity
We vary the global VAL quality threshold Qmin from 0.75 to 0.95, holding all other settings fixed. Table 10 reports the
corresponding retention rate, resulting dataset size, and student performance.

Table 10. Sensitivity of DocVAL (Gemma3-12B) to the VAL quality threshold Qmin on DocVQA. Performance is stable across a broad
range (0.80–0.90); degradation appears only at the extremes.

                                     Qmin        Retention    Dataset Size      ANLS     mAP
                                      0.75          98.1%       ∼100K           90.1     79.3
                                      0.80          96.2%       ∼98K            90.6     80.8
                                   0.85 (ours)      92.7%        95K            91.4     82.4
                                      0.90          83.4%       ∼85K            90.8     81.6
                                      0.95          65.1%       ∼67K            89.2     78.9


Across the operational range (0.80–0.90), DocVQA mAP varies by only 1.6 points. Performance degrades only at the
extremes—either retaining too many noisy traces (0.75) or discarding too much useful data (0.95). This confirms that
Qmin = 0.85 is not a knife-edge optimum.

                                                              18
                       DocVAL: Validated Chain-of-Thought Distillation for Grounded Document VQA

G.2. Component Weight Sensitivity
We next vary the component weights (αans , αbbox , αreason ) in the overall quality score (Eq. 4) around the default (0.4, 0.4, 0.2)
setting.

Table 11. Sensitivity of DocVAL (Gemma3-12B) to the VAL component weights on DocVQA. Maximum mAP variation across all tested
configurations is 1.2 points.

                                              (αans , αbbox , αreason )   ANLS   mAP
                                                  (0.5, 0.3, 0.2)         91.1   81.7
                                                  (0.3, 0.5, 0.2)         91.0   82.1
                                              (0.4, 0.4, 0.2) — ours      91.4   82.4
                                                  (0.4, 0.3, 0.3)         91.2   81.9
                                                  (0.3, 0.3, 0.4)         90.8   81.2
                                                (0.33, 0.33, 0.33)        91.0   81.5


Across six weight configurations, mAP varies by at most 1.2 points. The default (0.4, 0.4, 0.2) encodes a deliberate
priority—answer correctness and box quality as primary, reasoning quality as supporting supervision—but performance is
not brittle to this choice. We attribute the stability to two factors: (i) low-quality traces typically fail on multiple dimensions
simultaneously, so the rejection decision is robust to weight perturbations; and (ii) VAL’s geometric correction vector δ is
computed independently of these scalar weights, so verifier-mode pixel-level feedback is unaffected.

H. Compute Cost and Scope
H.1. Stage B2 Compute Breakdown
Stage B2 (iterative refinement) is sometimes perceived as adding substantial training overhead beyond Stage B1. We clarify
the actual cost here. Stage B1 trains for 3 epochs over D3 (76K examples), giving ∼228K example-passes. Stage B2 runs
for 2 epochs per iteration over D4 (9.5K examples) and converges in 12–16 iterations on average (13.2), giving ∼251K
example-passes total. The two stages are therefore of the same order in example-passes; Stage B2 is not an additional
full-scale training run.
VAL verification itself is CPU-only and runs at 12 examples/sec in verifier mode, which is negligible relative to GPU student
training. The total Stage B2 wall-clock cost on our 2×H100 setup is roughly 1.0–1.2× that of Stage B1. Importantly, this is
a one-time training cost: the deployed student is a pure VLM with no OCR, detector, teacher, or validator at inference.

H.2. Scope of Current Benchmarks
DocVAL is evaluated on DocVQA, VisualMRC, FUNSD, CORD, and SROIE, covering scanned forms, receipts, invoices,
and web documents. We do not claim full coverage of all document regimes. In particular, three regimes lie outside the
current benchmark distribution and are expected to be harder:

   • Handwriting-heavy pages. As noted in Appendix C, our qualitative analysis shows the student can read handwritten
     text correctly (ANLS = 1.0 in one example) but localizes less precisely (IoU = 0.68 vs. >0.9 for print). This degradation
     traces back to training-time validation: detectors miss handwritten regions, so VAL’s region-level feedback is weaker.
   • Severely degraded scans. Heavy noise, faded ink, or skewed pages reduce detector recall, which in turn weakens
     VAL’s supervision signal.
   • Chart- and figure-dominant pages. Documents where the answer-bearing region is a non-text visual element (e.g., a
     chart axis label inside a plot) fall outside the validator’s text-detection scaffolding.

In all three cases, the failure mode affects the quality of training supervision, not the deployed inference pipeline—the
student receives only (I, q) at test time and is not affected by detector failures at inference. Extending DocVAL to these
regimes (e.g., via complementary chart/figure detectors during training, or via teacher CoTs explicitly trained on handwritten
data) is an interesting direction for future work.


                                                                    19
