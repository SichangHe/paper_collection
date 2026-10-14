                                             SecGoal: A Benchmark for Extracting Formalizable Security Goals from
                                                                    Protocol Documents

                                            Dawei Huang, Hui Li* , Bo Jia, Haonan Feng, Jingjing Guan, Yueshuang Jiao, Xiangdong Li
                                                              Beijing University of Posts and Telecommunications
                                         {fengchen666, lihuill, q st, fenghaonan222, guaner, yueshuang, lxd dong}@bupt.edu.cn



                                                                     Abstract
arXiv:2604.27601v2 [cs.CR] 28 May 2026




                                                  Formal verification provides rigorous guaran-
                                                  tees for cryptographic security, yet extract-
                                                  ing formalizable security goals from natural-
                                                  language protocol documents remains largely        Figure 1: Protocol formal verification workflow from
                                                  manual. We introduce SecGoal, a dedicated          natural-language specification review to security goal
                                                  expert-annotated dataset and benchmark for ex-     identification and formal analysis.
                                                  tracting formalizable security goal statements
                                                  from protocol documents, covering 15 widely        models, and security goals—such as confidential-
                                                  deployed protocols, together with AIFG, a          ity and authentication—into code for tools like
                                                  schema- and flow-conditioned framework for         Tamarin (Meier et al., 2013) and ProVerif (Blanchet
                                                  structured formal security property generation.    et al., 2018). Upon execution, these tools can au-
                                                  Our evaluation shows that frontier and large       tomatically generate attack traces for subtle flaws
                                                  LLMs achieve high property recall but low ex-      that evade conventional testing, or conversely, pro-
                                                  traction precision because they often fail to
                                                  distinguish formalizable security goals from
                                                                                                     vide mathematical proofs that the protocol satisfies
                                                  non-goal protocol content. In contrast, Sec-       its intended security properties. Crucially, the ef-
                                                  Goal fine-tuning makes smaller open-source         fectiveness of formal verification depends on an
                                                  LLMs substantially more selective extractors       intermediate step that remains largely manual: ex-
                                                  of formalizable security goals. On the held-out    tracting security goal statements from protocol doc-
                                                  test protocols, Gemma2-9B-FT improves ex-          uments and mapping them into precise symbolic
                                                  traction precision from 24.0% to 66.6% and         security property descriptions.
                                                  reaches 97.6% property recall, outperforming
                                                  larger prompted LLMs and encoder baselines.           This step is challenging because protocol doc-
                                                  In a controlled setting, AIFG shows that con-      uments, such as IETF RFCs, are written in long-
                                                  cise goal inputs can support high-recall struc-    form, unstructured natural language, while verifi-
                                                  tured property generation, while expert-vetted     cation tools operate on precise security properties.
                                                  extracted inputs reveal over-generation as the     However, security goals are rarely stated explic-
                                                  main remaining bottleneck. Together, SecGoal       itly; instead, they are dispersed across descriptive
                                                  and AIFG provide a dataset, benchmark, and
                                                                                                     text, threat discussions, and design rationales. Even
                                                  framework for specification-grounded security
                                                  goal extraction and property generation.           when identified, translating these goals into formal,
                                                                                                     tool-checkable property statements remains largely
                                             1    Introduction                                       unsystematic, creating a persistent specification-
                                                                                                     to-model gap that limits the scalability of formal
                                             Formal verification is critical for cryptographic se-   protocol analysis.
                                             curity, providing rigorous guarantees for widely de-       Recent advances in large language
                                             ployed protocols such as TLS 1.3 (Bhargavan et al.,     models (LLMs) have sparked interest in
                                             2017; Cremers et al., 2017) and 5G-AKA (Basin           autoformalization—the automated translation of
                                             et al., 2018; Cremers and Dehnel-Wild, 2019).           natural language into formal specifications (Wu
                                             As illustrated in Figure 1, formal verification typ-    et al., 2022)—and formal specification inference
                                             ically requires domain experts to manually cu-          for programs (Le-Cong et al., 2025). LLMs
                                             rate documents and encode protocol logic, threat        have demonstrated strong capabilities in code
                                                 * Corresponding author.                             generation (Chen et al., 2021), mathematical
proof synthesis (Jiang et al., 2022), and assertion       sistent high-recall, low-precision failure mode
generation (Cosler et al., 2023), suggesting their        across the benchmark.
potential to assist in automating security goal         • We show that fine-tuning smaller open-source
statement extraction and formalization.                   LLMs on SecGoal substantially improves this
    However, security protocols pose a particularly       precision–recall trade-off, and provide AIFG, a
difficult setting: documents often extend over hun-       schema- and flow-conditioned framework for se-
dreds of pages, embed goals implicitly, and require       curity property generation from extracted goals.
long-context semantic reasoning, where errors can
lead to incomplete or unsound formal analyses.          2   Related Work
These observations raise a more focused question:
                                                        LLMs for Autoformalization. A growing body
can LLMs reliably extract formalizable security
                                                        of research leverages LLMs to translate natural lan-
goals from long protocol documents, and to what
                                                        guage constraints into formal artifacts for general
extent can such extracted goals support structured
                                                        software and hardware verification. Tools such
formal security-property generation under a given
                                                        as NL2Spec (Cosler et al., 2023) and recent ap-
protocol flow and formal schema?
                                                        proaches by Beg et al. (Beg et al., 2025) focus
    Existing work on LLMs for formal methods pri-
                                                        on generating code-level assertions (e.g., Dafny,
marily focuses on code-level annotations or state-
                                                        JML) or function contracts (Pearce et al., 2023).
machine inference (Wael et al., 2025), while pub-
                                                        Similarly, in hardware, AssertLLM (Yan et al.,
licly available datasets aligning natural-language
                                                        2025) automates the generation of SystemVerilog
protocol documents with formal security properties
                                                        Assertions. However, as highlighted by Formal-
are absent. This data gap and lack of benchmarks
                                                        Bench (Le-Cong et al., 2025), general-purpose
prevents systematic evaluation of LLM capabilities
                                                        models struggle with the logical rigor required for
in this high-stakes setting and hinders the develop-
                                                        verification. Crucially, these approaches operate
ment of LLM-based methods for automatic formal
                                                        in deterministic contexts (e.g., source code or lo-
analysis of security protocols.
                                                        calized comments). They do not address the lin-
    To address this gap, we formulate formalizable
                                                        guistic challenge of extracting global security goals
security-goal extraction as a benchmark task and
                                                        from unstructured, ambiguous protocol documents,
introduce SecGoal, a dedicated expert-annotated
                                                        where the “code” does not yet exist.
dataset for this setting, together with AIFG, a
schema- and flow-conditioned framework for struc-       Automated Protocol Modeling. Prior work on
tured formal security property generation from ex-      protocol analysis typically assumes structured in-
tracted goals. Our study asks whether LLMs can          puts or focuses on operational flows rather than
distinguish formalizable goals from surrounding         security logic. One stream translates semi-formal
protocol text, and how extraction quality affects       notations (e.g., Alice & Bob) into verification
downstream formalization. We find a clear gap be-       models using compilers (Keller and Basin, 2014)
tween promise and practice: frontier LLMs such          or LLMs (Li et al., 2025). Regarding opera-
as GPT-5.4, Claude-Sonnet-4-6, and Gemini-3-Pro-        tional extraction, RFCNLP (Pacheco et al., 2022)
Preview achieve high recall but lack the precision      and PROSPER (Sharma and Yegneswaran, 2023)
needed for formal analysis, while instruction tun-      utilize BERT-based architectures to extract Fi-
ing on SecGoal substantially improves extraction        nite State Machines (FSMs). More recently, Au-
and enables accurate security property generation.      toSM (Mao et al., 2025) leveraged LLMs and inter-
    Our main contributions are as follows:              mediate lambda calculus to synthesize executable
• We introduce SecGoal, an expert-annotated             symbolic models. However, these methods face a
   benchmark for extracting formalizable security       dual limitation: they either require manual inter-
   goals from 15 widely deployed protocols, where       mediate translation or overlook the extraction of
   goals are sparse and often implicitly embedded       formalizable security goals.
   in real, heterogeneous specifications rather than
   always being stated explicitly.                      Datasets and Benchmarks. Existing resources
• We define cross-granularity metrics that jointly      largely bypass the extraction challenge. Crypto-
   measure extraction precision and security prop-      FormalEval (Curaba et al., 2024) benchmarks the
   erty coverage, and use them to systematically        translation of pre-defined properties into Tamarin
   evaluate frontier and large LLMs, revealing a con-   code, assuming the extraction is already done. In
the smart contract domain, PropertyGPT (Liu et al.,      selection achieves 0.844 F1 and 0.737 Jaccard
2024b) relies on source code structure and com-          similarity, while property labeling achieves 0.956
piler feedback, which are unavailable in natural         micro-F1 and 0.947 Cohen’s κ. Per-protocol results
language documents.                                      are provided in Appendix B.5.
   To our knowledge, SecGoal is the first expert-
annotated benchmark specifically targeting the ex-       3.3   Dataset Statistics and Split
traction of formalizable security goal evidence          SecGoal contains 391 annotated security goal state-
from protocol documents. Complementing this              ments and 131 formal security properties across
resource, AIFG serves as a schema- and flow-             15 protocols. These statements occupy only 2.5%
conditioned framework for structured security prop-      of the source text on average, creating a sparse
erty generation from extracted goals.                    and challenging extraction setting. Table 6 in the
                                                         appendix reports per-protocol statistics. For evalu-
3     The SecGoal Dataset                                ation, we use protocol-level splits, ensuring that all
                                                         text from a protocol appears in only one split.
3.1    Protocol Coverage and Sources
SecGoal covers 15 widely deployed protocols              4     AIFG Framework
across critical domains—telecommunications (5G-          AIFG is a schema- and flow-conditioned frame-
AKA), industrial IoT (OPC-UA, SPDM), and web             work for structured security property generation. It
security (TLS 1.3, FIDO2)—whose specifications           extracts formalizable security goal statements and
are drawn from heterogeneous sources, ranging            generates structured property descriptions using re-
from structured IETF RFCs to industrial standards        trieved context, an available protocol flow, and a
and academic literature. Unlike synthetic datasets,      formal schema, but does not synthesize executable
SecGoal reflects real-world complexity: security         formalization tool code from raw documents.
goals are rarely stated explicitly but instead implic-
itly embedded in verbose, domain-specific prose.         4.1   Overview
                                                         AIFG bridges protocol documents and formal secu-
3.2    Human-in-the-Loop Annotation
                                                         rity properties by extracting security goals from D
We employed a three-phase HITL pipeline. First,          and mapping them, conditioned on a selected pro-
an LLM with multiple queries generated broad can-        tocol flow F and schema S, to a set of canonical
didate security goal statements to maximize cover-       formal property descriptions P = {p1 , . . . , pm }.
age, shifting human effort from raw extraction to           Rather than attempting end-to-end translation,
precise verification.                                    AIFG decomposes the pipeline into two stages: ex-
   Second, two doctoral researchers specializing in      traction and formalization. As illustrated in Fig-
cryptographic protocol analysis and formal verifi-       ure 2, Stage I (Mext ) extracts security goal state-
cation independently reviewed the candidate secu-        ments G from D, filtering out operational content.
rity goals, removing unsupported candidates and          Stage II (Mform ) performs retrieval-augmented for-
adding omitted ones. We treated protocol specifica-      malization: it first uses each extracted goal g ∈ G
tions as the annotation ground truth, using formal-      to retrieve relevant contextual chunks Cret , and then
analysis literature only as a secondary reference.       synthesizes structured formal properties P condi-
This is necessary because the two sources may dif-       tioned on Cret , the protocol flow F, and the formal
fer in scope: Basin et al. (2018) identify 5G-AKA        template schema S.
goals and assumptions not explicit in the 3GPP
specification, while some security goals stated in       4.2   Stage I: Security Goal Extraction
the EDHOC specification (Selander et al., 2021)          Security-goal statements are sparse in protocol doc-
fall outside the properties explicitly analyzed by Ja-   uments, covering only 2.5% of annotated document
comme et al. (2023). Thus, formal analyses guided        text on average. Directly mapping a full document
and validated our annotations but did not override       to formal properties is prone to context dilution, as
the specifications.                                      operational descriptions dominate the input while
   Finally, a senior professor with domain expertise     formalizable goals remain rare. Stage I therefore
adjudicated disagreements and edge cases to ensure       uses the extractor Mext to extract security goal
consistency across all 15 protocols.                     statements from D and produce the goal set G for
   Inter-annotator agreement is strong: statement        security formalization.
                                 Figure 2: An overview of the AIFG framework.

Document Preprocessing. We first remove struc-               role references or agreement variables, such as
tural boilerplate, such as tables of contents, bib-          which nonces or transcript hashes constitute the
liographies, and copyright notices, to reduce ir-            authentication agreementValues. These details
relevant noise. The remaining document text is               must be grounded using the protocol context.
then segmented to mitigate context window lim-             • Symbolic mismatch: Natural-language terms
itations (Liu et al., 2024a) and retain sufficient           do not necessarily align with the variable names,
local context for extraction. This preprocessing             role names, and message fields used in the target
step yields a sequence of chunks C = {c1 , . . . , cn },     formal model.
which serve as input to the extractor.                     • Mapping complexity: The mapping is many-to-
                                                             many: a single goal statement may imply multi-
Model Fine-Tuning. AIFG is model-agnostic,                   ple formal properties, while multiple goal state-
but we instantiate Mext with a model fine-tuned              ments may support the same property.
on SecGoal to improve extraction accuracy. Since
security goal statements are rare, the training data       Contextual Retrieval. Because entity definitions
is highly imbalanced and can bias the model toward         and variable bindings are scattered across D, trans-
non-goal protocol content. We therefore adopt              lating each goal in isolation can cause symbolic
Randomized Negative Downsampling (Liu et al.,              mismatches. For each extracted goal g ∈ G, we
2008), sampling negative examples to maintain a            retrieve the top-k relevant chunks Cret using g as a
controlled positive-to-negative ratio (e.g., 1:3) and      semantic query. The retrieved context helps ground
improve discrimination between formalizable goals          underspecified roles, entities, and protocol terms,
and non-goal text.                                         and is combined with the protocol variable struc-
                                                           ture described next.
Goal Extraction. During extraction, the extrac-
tor Mext is applied to each chunk ci ∈ C. If               Flow and Schema Inputs. AIFG treats the pro-
no security goal statement is detected, the extrac-        tocol flow F as a model-conditioned input rather
tor returns an empty list; otherwise, it generates         than an artifact automatically inferred from raw
a structured list of the formalizable security goal        documents, because symbolic protocol models may
statements in ci . The extracted statements are then       vary across experts and configurations. Here, F is
aggregated and deduplicated to form the protocol-          a structured representation of a selected complete
level candidate goal set G.                                formal protocol-flow model, including the roles, or-
                                                           dered message exchanges, and flow-level variables
4.3   Stage II: Security Goal Formalization
                                                           used to align document terms with formal-model
Translating the security goal statements G into for-       notation. The schema S is a protocol-independent
mal security properties that are accurate and consis-      structured representation of formal security prop-
tent with the formal protocol model is non-trivial,        erties. It summarizes common property specifica-
due to several linguistic and logical challenges:          tions into typed slots, providing a canonical space
• Ambiguity: Narrative goals often omit explicit           for property generation, evaluation, and many-to-
many deduplication. The full template definitions      goal statements and property-level coverage via
are provided in Appendix D.                            three complementary metrics:
Formal Property Synthesis. To ground retrieved
goals in the target formal model, we combine Cret      • Extraction Precision (Pext ): Pext = T PT+F  P
                                                                                                         P,
with F and S. For each goal g ∈ G, the model             where T P counts extracted statements that are
generates each candidate property p according to         valid security goal statements and F P counts
p ∼ P(· | g, Cret , F, S). Guided by S, the model        extracted statements that are not, measuring the
instantiates structured security property templates      signal-to-noise ratio of the extraction.
and maps natural-language terms to canonical vari-                                                   |Phit |
                                                       • Property-level Recall (Rprop ): Rprop = |P    GT |
                                                                                                             ,
ables in F; for example, a phrase such as “shared        where Phit denotes the set of ground-truth for-
secret” may be grounded to KAB and placed in the         mal properties whose evidential statements are
secretData slot. Finally, all generated properties       present in the extracted output, and PGT is the
are canonicalized and deduplicated to obtain the         complete ground-truth property set. This mea-
final security property set P.                           sures the fraction of formal properties recover-
                                                         able downstream.
5     Evaluation
                                                       • Extraction-Coverage F1 (EC-F1): EC-F1 =
                                                         2·Pext ·Rprop
We evaluate LLMs and AIFG on SecGoal, guided              Pext +Rprop , a cross-granularity harmonic mean
by three research questions:                             grounded in the requirements of formal verifica-
• RQ1: What limitations do contemporary LLMs             tion: Pext minimizes the noise that propagates
   exhibit when extracting security goals from pro-      into the formalization pipeline, while Rprop en-
   tocol documents?                                      sures no critical security properties are missed
• RQ2: How effectively does SecGoal fine-tuning          during formal analysis. We adopt EC-F1 as the
   improve security goal extraction, and can fine-       primary extraction metric.
   tuned small generative models outperform en-
   coder baselines and frontier LLMs?
• RQ3: How reliably can AIFG generate struc-           Metrics for Formalization (RQ3). We assess
   tured formal security-property descriptions from    formal property generation along two complemen-
   extracted security goals?                           tary dimensions:
    We use LlamaFactory (Zheng et al., 2024) for the
RQ2 fine-tuning experiments and RAGFlow (In-           • Property-level Precision/Recall/F1: Measures
finiFlow, 2024) for the RQ3 formalization pipeline.      whether the generated property set recovers the
For RQ1 and RQ2, all LLMs are evaluated with             gold formal security properties. A generated
provider-recommended default settings, with tem-         property is counted as a match only when it has
perature fixed to 0 for determinism and repro-           the same property type and subtype as a gold
ducibility. Detailed configurations for all exper-       property and is sufficiently aligned in its roles
iments are provided in Appendix A. The formal            and core security data. Precision penalizes spuri-
template schema and prompt templates are pre-            ous properties, while recall measures how many
sented in Appendices D and E, respectively.              gold properties are recovered.
5.1    Evaluation Metrics                              • Slot-level Precision/Recall/F1:         Measures
                                                         whether the internal fields of matched proper-
We employ a specialized metric suite that extends
                                                         ties are grounded correctly. We flatten each
PropertyGPT (Liu et al., 2024b) to address the
                                                         property into slot tokens such as asserter=R
non-bijective mapping inherent to our task: a sin-
                                                         or agreementValues=TH 2, then compare the
gle textual statement may encode multiple proper-
                                                         generated and gold slot-token sets. This captures
ties, and one property may be supported by several
                                                         errors in roles, attacker assumptions, keys,
statements, rendering standard statement-level or
                                                         nonces, transcript hashes, and other formal
property-level metrics insufficient alone for this
                                                         arguments even when the property type is correct.
task. Detailed definitions and a worked example
                                                         Slot scores are computed over matched property
are provided in Appendix C.
                                                         pairs; unmatched generated and gold properties
Metrics for Extraction (RQ1 & RQ2). We                   are reflected by property-level precision and
jointly evaluate the precision of extracted security     recall. Full details are provided in Appendix C.
Figure 3: Zero-shot and few-shot extraction performance across models, averaged over all 15 SecGoal protocols.
Models are ordered by few-shot EC-F1. Few-shot prompting improves precision substantially while property recall
remains largely saturated, yielding higher EC-F1 overall.

5.2   RQ1: LLM Performance on Goal                       Few-shot prompting only partially mitigates the
      Extraction                                         gap. Few-shot prompting improves Pext and EC-
                                                         F1 for several models, with the largest EC-F1 gain
To answer RQ1, we evaluate several frontier and          observed for Qwen3.5-Plus (+7.08 points). How-
large open-source LLMs, together with two com-           ever, the improvement remains limited and some-
pact instruction-tuned models, under zero-shot and       times trades recall for precision: GLM-5 decreases
few-shot prompting. Figure 3 reports property-           from 95.90% to 89.99% in Rprop , and Qwen2.5-
level recall (Rprop ), extraction precision (Pext ),     7B-Instruct drops from 81.45% to 66.31%.
and EC-F1 averaged over all 15 SecGoal protocols.           Model scale alone also does not guarantee
                                                         better extraction. GPT-5.4 and Claude-Sonnet-
Off-the-shelf LLMs achieve high recall but low           4-6 achieve very high few-shot recall, 97.60%
precision. Among frontier and large prompted             and 98.43%, respectively, but their precision re-
LLMs, Rprop is consistently high: zero-shot re-          mains only 23.88% and 21.31%. Conversely,
call ranges from 94.24% to 98.43%, indicating            Qwen3.5-Plus obtains the highest few-shot preci-
that these models can usually locate regions con-        sion, 36.44%, but still trails Gemini-3-Pro-Preview
taining recoverable security goals. The compact          and GLM-5 in EC-F1. Overall, the best EC-F1
instruction-tuned baselines are less recall-stable,      scores come from models with a better precision–
but the same precision bottleneck remains across         recall balance rather than from models maximizing
the benchmark. Zero-shot Pext ranges only from           either dimension alone.
20.25% to 31.57% among the stronger prompted             Answer to RQ1. Contemporary LLMs are not
models, and even few-shot prompting raises the           reliable standalone extractors for security protocol
best precision only to 36.44% for Qwen3.5-Plus.          formalization. Frontier and large prompted mod-
Consequently, no prompted model reaches 50%              els often achieve high property coverage, but all
EC-F1; the strongest few-shot results are 49.65%         prompted models systematically over-extract non-
for Gemini-3-Pro-Preview, 49.59% for GLM-5,              goal text. Few-shot prompting improves selectivity
and 48.97% for Qwen3.5-Plus.                             only marginally, indicating that domain-specific
   This gap reveals the central failure mode of cur-     adaptation is necessary.
rent LLMs: they are good at detecting broadly
security-related content, but poor at separating         5.3   RQ2: Effectiveness of SecGoal
formalizable security goals from protocol mecha-         To answer RQ2, we evaluate whether SecGoal fine-
nisms, implementation constraints, and explanatory       tuning improves smaller open-source LLMs as se-
text. For formal verification, such low precision is     curity goal extractors. We compare Gemma2-9B
costly, because each spurious extraction must be         and Qwen2.5-7B before and after fine-tuning, and
manually filtered before formalization.                  benchmark the fine-tuned models against encoder
            (a) Instruct vs. fine-tuned models                     (b) Fine-tuned models vs. prompted LLMs
Figure 4: RQ2 held-out test results: (a) instruction-tuned models versus SecGoal fine-tuned models; (b) fine-tuned
small models versus few-shot LLMs, with bubble area denoting EC-F1.

                                                             Chunking           Downsamp. Pext Rprop EC-F1
baselines and strong few-shot prompted LLMs. All
                                                                                None         63.1    83.4    70.3
RQ2 results are computed on the held-out test pro-           Sentence-window
                                                                                1:3          65.7    90.4    74.6
tocols after training on the SecGoal training split.
                                                                                None         61.2    86.0    70.5
Accordingly, the prompted baselines in Figure 4(b)           Section-level
                                                                                1:3          66.6    97.6    77.8
are re-evaluated on the same test subset rather than
                                                           Table 1: Ablation results on held-out test protocols with
using the all-protocol averages from RQ1.
                                                           Gemma2-9B-FT under the same train/test split.
Fine-tuning corrects the precision–recall imbal-
                                                              Family    Model             Rprop     Pext    EC-F1
ance. Figure 4(a) shows that SecGoal fine-tuning
                                                              Encoder RoBERTa      62.25 57.91              56.21
improves both smaller open-source LLMs. For
                                                              Encoder SecureBERT   79.75 59.97              66.32
Gemma2-9B, Pext rises from 24.0% to 66.6% on                  LLM     Gemma2-9B-FT 97.65 66.61              77.78
the held-out test set, while Rprop increases from
                                                           Table 2: Encoder results on held-out test protocols using
87.9% to 97.6%, raising EC-F1 from 35.9% to
                                                           the same train/test split as the fine-tuned LLMs.
77.8%. Qwen2.5-7B shows the same pattern: Pext
improves from 32.6% to 58.5%, Rprop from 84.1%             Fine-tuned compact LLMs outperform encoder
to 87.8%, and EC-F1 from 45.3% to 68.2%.                   and prompted LLM baselines. Table 2 shows
   These gains suggest that SecGoal fine-tuning            that Gemma2-9B-FT outperforms encoder base-
primarily helps models draw a clearer and more             lines trained on the same split, achieving 77.78%
reliable boundary between formalizable security            EC-F1 versus 56.21% for RoBERTa (Liu et al.,
goals and related but non-goal protocol text. While        2019) and 66.32% for SecureBERT (Aghaei et al.,
prompted LLMs often retrieve broadly relevant pas-         2022). The gain over SecureBERT is mainly recall-
sages, fine-tuning provides the domain-specific su-        driven, while precision also improves modestly.
pervision needed to filter out operational descrip-           The fine-tuned LLMs also surpass much larger
tions that should not be formalized, yielding more         prompted models in Figure 4(b). Gemma2-9B-FT
selective and trustworthy extraction behavior.             exceeds the strongest prompted baseline, GLM-
                                                           5, by 20.7 EC-F1 points, while Qwen2.5-7B-FT
Context and negative-example downsampling                  also outperforms all prompted baselines. The main
both matter. Table 1 shows that section-level              advantage is precision: Gemma2-9B-FT reaches
context and randomized negative-example down-              66.6% Pext , whereas prompted models remain be-
sampling are complementary. Fixing the chunk-              low 45% on the same test split.
ing strategy at section-level, downsampling im-
proves EC-F1 from 70.5% (no downsampling) to               Answer to RQ2. SecGoal fine-tuning improves
77.8% (1:3 ratio); fixing the downsampling ratio at        extraction by teaching models to distinguish for-
1:3, section-level chunking outperforms sentence-          malizable security goals from non-goal protocol
window chunking by 3.2 points (77.8% vs. 74.6%).           text. Compact fine-tuned LLMs outperform both
This indicates that effective extraction requires both     encoder specialists and larger prompted LLMs, in-
contextual continuity and balanced exposure to             dicating that task-specific supervision matters more
goal and non-goal examples.                                than scale alone for this task.
Protocol Input      Level     P         R         F1
                                                           Expert-vetted inputs expose over-generation
NSSK     gold-min. Prop. 0.71±0.00 1.00±0.00 0.83±0.00     and coverage gaps. Under expert-vetted inputs,
                     Slot 0.93±0.09 1.00±0.00 0.96±0.05
NSSK     expert-vet. Prop. 0.58±0.06 1.00±0.00 0.74±0.05   AIFG often retains useful coverage but generates
                     Slot 1.00±0.00 1.00±0.00 1.00±0.00    a larger property set. NSSK and Kao-Chow v1 re-
KC-v1    gold-min. Prop. 0.73±0.19 0.73±0.19 0.73±0.19     cover all gold properties, yet over-generation low-
                     Slot 0.89±0.08 1.00±0.00 0.94±0.04    ers property F1 to 0.74 and 0.55, respectively. ED-
KC-v1    expert-vet. Prop. 0.38±0.03 1.00±0.00 0.55±0.03
                     Slot 1.00±0.00 1.00±0.00 1.00±0.00    HOC and SPDM are harder: recall falls to 0.76
                                                           and 0.71, while additional generated properties re-
EDHOC gold-min. Prop. 0.73±0.02 0.86±0.03 0.79±0.03
                  Slot 0.85±0.00 0.89±0.00 0.87±0.00       duce F1 to 0.51 and 0.39. This contrast suggests
EDHOC expert-vet. Prop. 0.38±0.03 0.76±0.00 0.51±0.02      a complexity effect. For compact protocols, the
                  Slot 0.83±0.01 0.89±0.00 0.85±0.01
                                                           flow and schema expose fewer canonical distinc-
SPDM     gold-min. Prop. 0.55±0.08 0.92±0.12 0.69±0.09     tions, so AIFG mainly needs to suppress redundant
                     Slot 0.77±0.08 0.98±0.02 0.84±0.06
SPDM     expert-vet. Prop. 0.27±0.03 0.71±0.06 0.39±0.04   properties after coverage is achieved. By contrast,
                     Slot 0.73±0.06 0.95±0.01 0.81±0.05    EDHOC and SPDM involve variable-rich proper-
Table 3: RQ3 property- and slot-level formalization
                                                           ties spanning state, session binding, negotiation,
results (mean ± std., three runs); full TP/FP/FN counts    measurements, and authentication. Their errors
are in Appendix Table 11. KC-v1: Kao-Chow v1; gold-        therefore combine over-generation, missed canoni-
min./expert-vet.: gold-minimal/expert-vetted.              cal properties, and incomplete variable grounding,
5.4    RQ3: Formal Property Generation                     which lowers slot F1 on matched pairs (0.85 and
                                                           0.81 under expert-vetted inputs) relative to NSSK
To answer RQ3, we evaluate AIFG as a flow-
                                                           and Kao-Chow v1 (1.00). EDHOC further shows
conditioned property-generation task: given ex-
                                                           an upstream coverage effect: its expert-vetted goals
tracted goals, a protocol flow, and a schema,
                                                           cover fewer gold properties, reducing generated
AIFG generates canonical property descriptions
                                                           recall; the gold-minimal rows also show that com-
and grounds their slots. We instantiate AIFG
                                                           plete goal coverage does not guarantee complete
with GPT-5.4 (OpenAI, 2026) and text-embedding-
                                                           structured property generation.
large (OpenAI, 2024) retrieval; details are in Ap-
pendix A. For each protocol, the flow F is derived         Answer to RQ3. With concise, well-covered in-
from formal-analysis papers and implementations            puts, AIFG can recover many target properties and
and normalized into AIFG’s flow format; gold prop-         ground matched slots reliably. Its main remain-
erties are written relative to this flow and schema S.     ing bottleneck is selecting the minimal canonical
We test four protocols spanning compact academic           property set: realistic extractions amplify over-
and industrial settings (NSSK, Kao-Chow v1, ED-            generation, and complex protocols such as EDHOC
HOC, and SPDM) under two input variants: gold-             and SPDM also expose coverage gaps.
minimal, concise gold statements covering all gold
properties, and expert-vetted, reviewed Gemma2-            6   Conclusion
9B-FT extractions with false positives removed.
                                                           We introduced SecGoal, a dedicated expert-
This setting evaluates intermediate structured prop-
                                                           annotated benchmark for security goal extraction
erty generation, not end-to-end formal verification
                                                           from protocol documents, and AIFG, a schema-
or executable model synthesis.
                                                           and flow-conditioned framework for generating
Concise inputs improve coverage but not exact              structured formal security properties from extracted
selection. Gold-minimal inputs give AIFG con-              goals. Our evaluation shows that frontier and large
cise statements that cover the target property set,        LLMs can often identify security-relevant passages
improving property recall on most protocols (Ta-           but struggle to filter formalizable goals, making
ble 3). NSSK reaches full recall with 0.83 property        precision the main bottleneck. SecGoal fine-tuning
F1, while EDHOC and SPDM reach 0.86 and 0.92               substantially improves this boundary judgment, en-
recall, respectively. However, property precision          abling smaller open-source LLMs to outperform
remains limited by extra generated properties and          larger prompted models and encoder baselines.
strict canonical matching, yielding 0.79 F1 on ED-         AIFG further demonstrates that concise goal inputs
HOC and 0.69 on SPDM; Kao-Chow v1 reaches                  support high-recall structured property generation,
0.73 F1 despite strong slot grounding, reflecting          while expert-vetted extracted inputs expose over-
property-level matching sensitivity.                       generation as the key obstacle to scaling.
7   Limitations                                          and focuses on protocol-level security requirements
                                                         rather than information about individual users or
Specification-grounded scope. SecGoal and
                                                         organizations. When releasing the dataset and code,
AIFG extract and formalize security goals that are
                                                         we will respect the redistribution terms of the origi-
stated or supported by the protocol specification.
                                                         nal source documents and provide documentation
They do not synthesize additional security assump-
                                                         of protocol coverage, annotation criteria, and in-
tions or expert-derived properties that may be re-
                                                         tended use.
quired for a complete security analysis (Basin et al.,
                                                         Annotation process. All annotation and adjudi-
2018). The output should therefore be viewed as a
                                                         cation were conducted internally by members of
specification-grounded goal set, not as a proof of
                                                         the research team. Two doctoral researchers with
full protocol security.
                                                         experience in cryptographic protocol analysis and
Gap to end-to-end verification. AIFG focuses             symbolic verification independently reviewed the
on the goal side of formal verification: extract-        candidate security goals, while a senior domain
ing security goals and generating structured for-        expert, also a member of the research team, adju-
mal property descriptions. It assumes an available       dicated disagreements and edge cases. No crowd-
protocol flow and variable namespace, and does           workers, external paid annotators, or vulnerable
not automatically synthesize executable Tamarin          populations were involved. The task required ex-
or ProVerif models from raw documents. Although          pert judgments about specification-grounded, for-
these tools can automate reasoning over a specified      malizable security goals, rather than subjective or
model, completing a proof often requires expert-         personal information from annotators.
written auxiliary lemmas, suitable proof strategies,     Security impact and dual use. Because this work
and iterative model or query refinements. Thus,          concerns security protocols, we acknowledge po-
fully automating the path from raw protocol docu-        tential dual-use and over-reliance risks. The pro-
ments to completed formal verification remains an        posed methods may help analysts identify formal-
open challenge in both research and practice.            izable security goals more efficiently, but their out-
                                                         puts should not be interpreted as a proof of proto-
Limited formalization scale. Our RQ3 evalua-
                                                         col security. SecGoal and AIFG are specification-
tion covers NSSK, Kao-Chow v1, EDHOC, and
                                                         grounded: they extract and formalize goals that are
SPDM, extending the controlled setting from com-
                                                         stated in or supported by the source documents, but
pact academic protocols to a more realistic indus-
                                                         they do not synthesize all expert-derived assump-
trial protocol. Even so, the evaluation remains lim-
                                                         tions needed for complete security analysis.
ited by the need to construct expert-validated flows,
                                                         Intended use. This benchmark is intended to sup-
variable namespaces, and gold structured proper-
                                                         port research on specification-grounded security
ties with high confidence. We do not include OPC-
                                                         goal extraction and structured security-property
UA in RQ3 because its security behavior is spread
                                                         generation. We discourage using the system as a
across multiple specifications and deployment pro-
                                                         standalone security certification tool, as a substitute
files; even before threat-model dimensions, OPC-
                                                         for expert formal verification, or as the sole basis
UA yields 216 protocol configurations, making a
                                                         for security-critical deployment decisions. Out-
single gold flow difficult to define without introduc-
                                                         puts produced by models trained or evaluated on
ing strong manual modeling assumptions. Includ-
                                                         SecGoal should be reviewed by qualified domain
ing it would make the evaluation depend heavily
                                                         experts before being used in formal analysis work-
on the completeness of an OPC-UA-specific model
                                                         flows or other security-sensitive settings.
rather than isolating AIFG’s property-generation
ability. We therefore treat RQ3 as a controlled
property-generation study rather than a coverage         References
study over all SecGoal protocols.
                                                         Ehsan Aghaei, Xi Niu, Waseem Shadid, and Ehab Al-
Ethical Considerations                                     Shaer. 2022. Securebert: A domain-specific lan-
                                                           guage model for cybersecurity. In international con-
Data and privacy. SecGoal is constructed from              ference on security and privacy in communication
                                                           systems, pages 39–56. Springer.
publicly available protocol specifications, stan-
dards, and academic materials. It does not contain       David Basin, Jannik Dreier, Lucca Hirschi, Saša
personal, sensitive, or user-generated private data,       Radomirovic, Ralf Sasse, and Vincent Stettler. 2018.
  A formal analysis of 5g authentication. In Pro-         Katriel Cohn-Gordon, Cas Cremers, and Luke Gar-
  ceedings of the 2018 ACM SIGSAC conference on             ratt. 2016. On post-compromise security. In 2016
  computer and communications security, pages 1383–         IEEE 29th Computer Security Foundations Sympo-
  1396.                                                     sium (CSF), pages 164–178. IEEE.

Arshad Beg, Diarmuid O’Donoghue, and Rosemary             Matthias Cosler, Christopher Hahn, Daniel Men-
  Monahan. 2025. A short survey on formalising             doza, Frederik Schmitt, and Caroline Trippel. 2023.
  software requirements using large language models.       nl2spec: Interactively translating unstructured natu-
  arXiv preprint arXiv:2506.11874.                         ral language to temporal logics with large language
                                                           models. In International Conference on Computer
Karthikeyan Bhargavan, Bruno Blanchet, and Nadim           Aided Verification, pages 383–396. Springer.
  Kobeissi. 2017. Verified models and reference im-
  plementations for the tls 1.3 standard candidate. In    Cas Cremers. 2011. Key exchange in ipsec revisited:
  2017 IEEE Symposium on Security and Privacy (SP),         Formal analysis of ikev1 and ikev2. In European
  pages 483–502. IEEE.                                      Symposium on Research in Computer Security, pages
                                                            315–334. Springer.
Karthikeyan Bhargavan, Christina Brzuska, Cédric Four-   Cas Cremers, Alexander Dax, and Aurora Naska. 2023.
  net, Matthew Green, Markulf Kohlweiss, and Santi-         Formal analysis of {SPDM}: Security protocol and
  ago Zanella-Béguelin. 2016. Downgrade resilience         data model version 1.2. In 32nd USENIX Security
  in key-exchange protocols. In 2016 IEEE Symposium         Symposium (USENIX Security 23), pages 6611–6628.
  on Security and Privacy (SP), pages 506–525. IEEE.
                                                          Cas Cremers and Martin Dehnel-Wild. 2019.
Karthikeyan Bhargavan, Charlie Jacomme, Franziskus          Component-based formal analysis of 5g-aka:
  Kiefer, and Rolfe Schmidt. 2024. Formal verifica-         Channel assumptions and session confusion. In
  tion of the {PQXDH}{Post-Quantum} key agree-              Network and Distributed System Security Symposium
  ment protocol for end-to-end secure messaging. In         (NDSS). Internet Society.
  33rd USENIX Security Symposium (USENIX Security
  24), pages 469–486.                                     Cas Cremers, Marko Horvat, Jonathan Hoyland, Sam
                                                            Scott, and Thyla Van Der Merwe. 2017. A compre-
Bruno Blanchet. 2004. Automatic proof of strong se-         hensive symbolic analysis of tls 1.3. In Proceedings
  crecy for security protocols. In IEEE Symposium           of the 2017 ACM SIGSAC conference on computer
  on Security and Privacy, 2004. Proceedings. 2004,         and communications security, pages 1773–1788.
  pages 86–100. IEEE.
                                                          Cristian Curaba, Denis D’Ambrosi, Alessandro Min-
Bruno Blanchet, Ben Smyth, Vincent Cheval, and Marc         isini, and Natalia Pérez-Campanero Antolı́n. 2024.
  Sylvestre. 2018. Proverif 2.00: automatic crypto-         Cryptoformaleval: Integrating llms and formal verifi-
  graphic protocol verifier, user manual and tutorial.      cation for automated cryptographic protocol vulnera-
  Version from, 16:05–16.                                   bility detection. arXiv preprint arXiv:2411.13627.

Colin Boyd, Anish Mathuria, and Douglas Stebila. 2003.    Vincent Diemunsch, Lucca Hirschi, and Steve Kremer.
  Protocols for authentication and key establishment,       2025. A comprehensive formal security analysis of
  volume 1. Springer.                                       {OPC}{UA}. In 34th USENIX Security Symposium
                                                            (USENIX Security 25), pages 7077–7096.
Simone Bussa, Riccardo Sisto, and Fulvio Valenza.
  2023. Formal verification of the fdo protocol. In       Haonan Feng, Hui Li, Xuesong Pan, Ziming Zhao, and
  2023 IEEE Conference on Standards for Commu-              T Cactilab. 2021. A formal analysis of the fido uaf
  nications and Networking (CSCN), pages 290–295.           protocol. In NDSS.
  IEEE.                                                   Daniel Fett, Ralf Küsters, and Guido Schmitz. 2016. A
                                                            comprehensive formal security analysis of oauth 2.0.
Frederick Butler, Iliano Cervesato, Aaron D Jaggard,        In Proceedings of the 2016 ACM SIGSAC conference
  Andre Scedrov, and Christopher Walstad. 2006. For-        on computer and communications security, pages
  mal analysis of kerberos 5. Theoretical Computer          1204–1215.
  Science, 367(1-2):57–87.
                                                          Stefan-Lukas Gazdag, Sophia Grundner-Culemann, To-
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,            bias Guggemos, Tobias Heider, and Daniel Loeben-
 Henrique Ponde De Oliveira Pinto, Jared Kaplan,             berger. 2021. A formal analysis of ikev2’s post-
 Harri Edwards, Yuri Burda, Nicholas Joseph, Greg            quantum extension. In Proceedings of the 37th An-
 Brockman, and 1 others. 2021. Evaluating large              nual Computer Security Applications Conference,
 language models trained on code. arXiv preprint             pages 91–105.
 arXiv:2107.03374.
                                                          Jingjing Guan, Hui Li, Haisong Ye, and Ziming Zhao.
John Andrew Clark and Jeremy Lawrence Jacob. 1997.           2022. A formal analysis of the fido2 protocols. In
  A survey of authentication protocol literature: Ver-       European Symposium on Research in Computer Se-
  sion 1.0.                                                  curity, pages 3–21. Springer.
InfiniFlow. 2024. Ragflow: An open-source rag engine      Simon Meier, Benedikt Schmidt, Cas Cremers, and
   based on deep document understanding. https://           David Basin. 2013. The tamarin prover for the sym-
   github.com/infiniflow/ragflow.                           bolic analysis of security protocols. In International
                                                            conference on computer aided verification, pages
Charlie Jacomme, Elise Klein, Steve Kremer, and             696–701. Springer.
  Maı̈wenn Racouchot. 2023. A comprehensive, for-
  mal and automated analysis of the {EDHOC} proto-        OpenAI. 2024.      New embedding models and
  col. In 32nd USENIX Security Symposium (USENIX            API updates.       https://openai.com/index/
  Security 23), pages 5881–5898.                            new-embedding-models-and-api-updates/.
                                                            Accessed: 2026-05-25.
Albert Q Jiang, Sean Welleck, Jin Peng Zhou,
  Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée        OpenAI. 2026. Introducing GPT-5.4. https://
  Lacroix, Yuhuai Wu, and Guillaume Lample. 2022.           openai.com/index/introducing-gpt-5-4/. Ac-
  Draft, sketch, and prove: Guiding formal theo-            cessed: 2026-05-25.
  rem provers with informal proofs. arXiv preprint
  arXiv:2210.12283.                                       Maria Leonor Pacheco, Max von Hippel, Ben Wein-
                                                           traub, Dan Goldwasser, and Cristina Nita-Rotaru.
Michel Keller and Prof Dr David Basin. 2014. Con-          2022. Automated attack synthesis by extracting fi-
  verting alice&bob protocol specifications to tamarin.    nite state machines from protocol specification doc-
  ETH Zurich.                                              uments. In 2022 IEEE Symposium on Security and
                                                           Privacy (SP), pages 51–68. IEEE.
Thanh Le-Cong, Bach Le, and Toby Murray. 2025. Can
  llms reason about program semantics? a compre-          Hammond Pearce, Benjamin Tan, Baleegh Ahmad,
  hensive evaluation of llms on formal specification        Ramesh Karri, and Brendan Dolan-Gavitt. 2023. Ex-
  inference. In Proceedings of the 63rd Annual Meet-        amining zero-shot vulnerability repair with large lan-
  ing of the Association for Computational Linguistics      guage models. In 2023 IEEE symposium on security
  (Volume 1: Long Papers), pages 21991–22014.               and privacy (SP), pages 2339–2356. IEEE.

Qiang Li, Jihong Han, Lin Yuan, Xiangcheng Li, and        Andreas Pfitzmann and Marit Hansen. 2010. A termi-
  Xiaoyu Wang. 2025. Constructing formal models of          nology for talking about privacy by data minimiza-
  cryptographic protocols from alice&bob style speci-       tion: Anonymity, unlinkability, undetectability, unob-
  fications via llm. Scientific Reports, 15(1):11866.       servability, pseudonymity, and identity management.

Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paran-       Göran Selander, John Preuß Mattsson, and Francesca
  jape, Michele Bevilacqua, Fabio Petroni, and Percy        Palombini. 2021. Ephemeral Diffie-Hellman Over
  Liang. 2024a. Lost in the middle: How language            COSE (EDHOC). Internet-Draft draft-ietf-lake-
  models use long contexts. Transactions of the associ-     edhoc-12, Internet Engineering Task Force. Work
  ation for computational linguistics, 12:157–173.          in Progress.

Xu-Ying Liu, Jianxin Wu, and Zhi-Hua Zhou. 2008. Ex-      Prakhar Sharma and Vinod Yegneswaran. 2023. Pros-
  ploratory undersampling for class-imbalance learn-        per: Extracting protocol specifications using large
  ing. IEEE Transactions on Systems, Man, and Cyber-        language models. In Proceedings of the 22nd ACM
  netics, Part B (Cybernetics), 39(2):539–550.              workshop on hot topics in networks, pages 41–47.

Ye Liu, Yue Xue, Daoyuan Wu, Yuqiang Sun, Yi Li,          Fares Wael, Youssef Maklad, Ali Hamdi, and Wael
  Miaolei Shi, and Yang Liu. 2024b. Propertygpt: Llm-       Elsersy. 2025. An agentic flow for finite state ma-
  driven formal verification of smart contracts through     chine extraction using prompt chaining. In 2025 In-
  retrieval-augmented property generation. arXiv            telligent Methods, Systems, and Applications(IMSA),
  preprint arXiv:2405.02580.                                pages 328–333. IEEE.

Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-       Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus
  dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,             Rabe, Charles Staats, Mateja Jamnik, and Christian
  Luke Zettlemoyer, and Veselin Stoyanov. 2019.             Szegedy. 2022. Autoformalization with large lan-
  Roberta: A robustly optimized bert pretraining ap-        guage models. Advances in neural information pro-
  proach. arXiv preprint arXiv:1907.11692.                  cessing systems, 35:32353–32368.

Gavin Lowe. 1997. A hierarchy of authentication spec-     Zhiyuan Yan, Wenji Fang, Mengming Li, Min Li, Shang
  ifications. In Proceedings 10th computer security         Liu, Zhiyao Xie, and Hongce Zhang. 2025. As-
  foundations workshop, pages 31–43. IEEE.                  sertllm: Generating hardware verification assertions
                                                            from design specifications via multi-llms. In Pro-
Ziyu Mao, Jingyi Wang, Jun Sun, Shengchao Qin, and          ceedings of the 30th Asia and South Pacific Design
  Jiawen Xiong. 2025. Llm-aided automatic modeling          Automation Conference, pages 614–621.
  for security protocol verification. In 2025 IEEE/ACM
  47th International Conference on Software Engineer-     Tatu Ylonen. 2006. Rfc 4251: The secure shell (ssh)
  ing (ICSE), pages 642–654. IEEE.                          protocol architecture.
Jingjing Zhang, Lin Yang, Xianming Gao, Gaigai Tang,
   Jiyong Zhang, and Qiang Wang. 2021. Formal analy-
   sis of quic handshake protocol using symbolic model
   checking. IEEE Access, 9:14836–14848.
Yaowei Zheng, Richong Zhang, Junhao Zhang, Yanhan
  Ye, and Zheyan Luo. 2024. Llamafactory: Unified
  efficient fine-tuning of 100+ language models. In
  Proceedings of the 62nd annual meeting of the as-
  sociation for computational linguistics (volume 3:
  system demonstrations), pages 400–410.
A     Experimental Setup and                            A.3    Encoder and Prompting
      Hyperparameters                                   Encoder baselines. We compared against
                                                        RoBERTa (Liu et al., 2019) and Secure-
A.1    Hardware and Software                            BERT (Aghaei et al., 2022) as segment-level
All local fine-tuning experiments were conducted        encoder baselines. We reformulate extraction as
on a server equipped with 1 × NVIDIA A800               binary classification: given a candidate statement
80GB PCIe GPU, an Intel Xeon Gold 6348 CPU              and its section context, formatted as candidate
with 112 logical cores, and 1.0 TiB system mem-         statement [SEP] section context, the encoder
ory. The operating system was Ubuntu 22.04.5 LTS.       predicts whether the candidate is a formalizable
The NVIDIA driver version was 580.82.07, and the        security goal. Candidate statements are generated
CUDA runtime version reported by nvidia-smi             from annotated protocol chunks by splitting sen-
was 13.0. We used LlamaFactory (Zheng et al.,           tences, bullet items, table rows, and local sentence
2024) for fine-tuning the open-source LLM extrac-       combinations. Candidates aligned with gold goals
tors.                                                   are labeled positive, and unmatched candidates are
                                                        labeled negative. During inference, all candidates
   Prompting-based evaluations of proprietary
                                                        are scored, thresholded, and deduplicated to obtain
LLMs were conducted through their official hosted
                                                        the final extracted goal set. The two baselines use
interfaces or APIs. To improve reproducibility, we
                                                        the same pipeline and differ only in the pretrained
fixed the temperature to 0 for all prompting experi-
                                                        checkpoint.
ments, while keeping all other inference parameters
at the officially recommended default settings. For     Hyperparameter            RoBERTa       SecureBERT
models that provide optional thinking or extended-                                              ehsanaghaei/
reasoning modes, we disabled these modes in all         Base model               roberta-base
                                                                                                 SecureBERT
experiments and used standard prompted inference.       Max length                    512            512
                                                        Batch size                    16             16
The hardware configuration above applies only to
                                                        Learning rate              2 × 10−5       1 × 10−5
local fine-tuning experiments.                          Epochs                         10             12
                                                        Weight decay                 0.01           0.01
                                                        Warmup ratio                  0.1            0.1
A.2    Fine-tuning and Hyperparameters                  Focal γ                       2.0            2.0
                                                        Focal α                      0.25           0.25
We fine-tuned Qwen2.5-7B-Instruct and Gemma2-           Inference threshold          0.25           0.25
9B-Instruct using LoRA-based supervised fine-           Model-selection metric       F0.5           F1.5
tuning in LlamaFactory (Zheng et al., 2024). For
each model, we used the same fine-tuning con-           Table 5: Core hyperparameters for the encoder base-
figuration across its corresponding experimental        lines.
variants, while changing only the training data con-       We used focal loss for both encoders and fixed
struction when needed for ablation analysis.            the random seed to 42. For each baseline, we se-
                                                        lected the checkpoint with the best validation score
Hyperparameter                Qwen2.5-7B Gemma2-9B
                                                        according to the model-selection metric in Table 5.
Learning rate                  5 × 10−6     8 × 10−6
Training epochs                    10           20      Prompting setup. We evaluated prompting-
Max sequence length               2500         2500
Per-device batch size               4            4      based LLMs under zero-shot and few-shot settings.
Gradient accumulation steps         4            4      In zero-shot prompting, the model received only
LR scheduler                     Cosine       Cosine    the task instruction and the input protocol chunk.
Warmup                         0.05 ratio    20 steps
                                                        In few-shot prompting, we prepended three manu-
Optimizer                       AdamW        AdamW
Precision                       bfloat16     bfloat16   ally constructed demonstration examples to specify
LoRA rank                           8           16      the output format and clarify the boundary between
LoRA alpha                         16           32      formalizable security goals and non-goal protocol
LoRA dropout                      0.05         0.10
                                                        text. The few-shot demonstrations include brief
LoRA target modules                all          all
                                                        exclusion rationales, but the model was always
Table 4: Core fine-tuning hyperparameters for the two   instructed to return JSON-only outputs. These ex-
open-source LLM extractors.                             amples were synthetic and were not taken from any
                                                        SecGoal benchmark document or fine-tuning data.
All prompting-based LLMs were evaluated on the              statements, associated formal properties, the ap-
full SecGoal benchmark.                                     proximate share of protocol document text anno-
                                                            tated as security goal statements, and source refer-
A.4      Retrieval and Formalization Setup                  ences. We use these statistics to track annotation
We implemented the formalization stage using                coverage.
RAGFlow (InfiniFlow, 2024). The chat model
was GPT-5.4, and the embedding model was                    B.2   Train-Test Split
text-embedding-large. The knowledge base
contained the formal property taxonomy, template            We used a protocol-level train–test split to evalu-
schema, protocol flow definitions, and supporting           ate cross-protocol generalization. All annotated
protocol context. Documents were processed using            statements from the same protocol were assigned
RAGFlow’s default “General” parsing mode.                   to the same split, avoiding leakage from protocol-
   We enabled Reasoning Flow and Keyword Anal-              specific terminology, message names, and security
ysis and kept the remaining RAGFlow parameters              assumptions across training and testing. The test
at their default settings. The same retrieval and           set consists of five held-out protocols: Kao-Chow
generation configuration was used for all protocols         v1, NSSK, SPDM, EDHOC, and OPC-UA. The
in the formalization evaluation.                            remaining ten protocols were used for training and
                                                            validation.
                Goal         Goal
    Protocol          Props.                Ref.
               Stmts.        Share
TLS 1.3         29     12     2.3% (Bhargavan et al.,       B.3   Three-Phase Annotation Pipeline
                                   2017; Cremers et al.,
                                   2017)
IKEv2           20      8     1.3% (Gazdag et al., 2021;    Section 3.2 describes the three-phase annotation
                                   Cremers, 2011)           pipeline; here, we report the additional per-phase
Kerberos5       33     9      2.2% (Butler et al., 2006)    statistics omitted there. We used frontier LLMs
OAuth2.0        51     7      3.6% (Fett et al., 2016)
5G-AKA          46     11     1.8% (Basin et al., 2018;     to generate broad preliminary candidate pools
                                   Cremers and              for expert annotation. After pooling and de-
                                   Dehnel-Wild, 2019)
PQXDH           16      7     8.9% (Bhargavan et al.,       duplicating candidates within each document, the
                                   2024)                    recall-oriented generation stage yielded two candi-
FIDO2           23     15     7.2% (Feng et al., 2021;      date pools containing 1,980 and 2,054 candidate
                                   Guan et al., 2022)
QUIC            25      7     0.9% (Zhang et al., 2021)     security goal statements, respectively, for human
SSH             10      8     2.7% (Ylonen, 2006)           review.
OPC-UA          28      6     3.5% (Diemunsch et al.,
                                   2025)                       During independent review, each annotator con-
FDO             23     6     10.7% (Bussa et al., 2023)     firmed or rejected every candidate, added goal state-
EDHOC           33     17     4.8% (Jacomme et al.,
                                   2023)                    ments missed by the generator, and assigned one or
SPDM            20      8     1.1% (Cremers et al., 2023)   more property types. Annotators worked from the
NSSK            19      5    17.4% (Clark and Jacob,
                                   1997)
                                                            protocol specification and the references in Table 6,
Kao-Chow v1     15      5    13.2% (Clark and Jacob,        with no access to each other’s labels. Across the
                                   1997)                    two independent reviews, annotators recovered 87
Total           391    131   2.5% –                         omitted goal statements that were absent from the
                                                            LLM-generated candidate pools. Before arbitra-
Table 6: SecGoal dataset statistics across 15 protocols     tion, the two annotators selected 317 and 305 state-
before document-level splitting. Goal Share denotes the
approximate share of protocol document text annotated
                                                            ments, respectively, with 263 shared statements
as security goal statements.                                and a union of 359 statements; see Table 7.
                                                               The senior professor adjudicated the 96 non-
                                                            shared statements and all uncertain cases under the
B       Dataset Construction and                            same specification-grounded inclusion rule, recon-
        Documentation                                       ciled boundary and label differences, and recov-
                                                            ered 29 additional omitted goal statements after
B.1      Coverage and Sources
                                                            the two annotators completed their reviews. The
Table 6 provides the protocol-level documenta-              final dataset contains 391 goal statements and 131
tion for SecGoal, including annotated security goal         formal security properties.
B.4     Annotation Guidelines                                  C    Metric Definitions and a Worked
A security goal statement is an intended security                   Example
property that the protocol guarantees, that is, the            Why extraction uses cross-granularity metrics.
what, and must be expressible as a trace constraint            Security-goal extraction in SecGoal is not ordinary
in a symbolic model. We exclude operational logic,             sentence retrieval: it is the upstream filtering step
namely the how: parsing, encoding, and interoper-              for formal verification. Two failure modes there-
ability requirements.                                          fore matter at the same time. First, false-positive
   Modal verbs such as “must” and “shall” are not              extractions increase expert review cost and may
sufficient evidence of security relevance. We also             induce spurious formal properties. Second, false
exclude non-formalizable requirements, such as                 negatives can make a downstream security prop-
UI mandates and physical constraints, as well as               erty unrecoverable, even if many other sentences
over-inferred goals. For example, the TLS 1.3                  are correctly extracted. Standard statement-level F1
legacy version check serves middlebox interop-                 does not capture this behavior because the relation
erability rather than downgrade protection.                    between natural-language statements and formal
   Each statement maps to one or more property                 properties is many-to-many: one statement may
types under a many-to-many relation.                           encode multiple formal properties, while several
                                           Prop.               different statements may support the same property.
Protocol      A1 A2 Shr. Stmt. F1 Jacc.          Cohen′ sκ
                                           µ-F1                We therefore score extraction at two granularities.
5G-AKA         31   33   24   0.750   0.600 0.873   0.859      Pext measures whether the extracted statements are
EDHOC          30   29   28   0.949   0.903 0.976   0.973      clean security goal evidence, whereas Rprop mea-
FDO            19   15   13   0.765   0.619 1.000   1.000
FIDO2          20   20   17   0.850   0.739 1.000   1.000      sures whether the extracted evidence still covers
IKEv2          16   18   14   0.824   0.700 0.902   0.877      the formal properties needed for downstream anal-
Kao-Chow v1    11   13   10   0.833   0.714 1.000   1.000
Kerberos5      27   25   22   0.846   0.733 0.894   0.882      ysis. EC-F1 combines these two requirements and
NSSK           17   17   16   0.941   0.889 1.000   1.000      is used as the primary extraction metric.
OAuth2.0       40   37   32   0.831   0.711 0.965   0.959
OPC-UA         27   21   21   0.875   0.778 0.951   0.938      Extraction metrics. For a protocol, let PGT be
PQXDH          11   12   10   0.870   0.769 0.966   0.957
QUIC           17   15   11   0.688   0.524 1.000   1.000      the set of ground-truth formal properties and let
SPDM           18   15   13   0.788   0.650 0.917   0.895      E(p) denote the gold security goal statements that
SSH             8   10    8   0.889   0.800 0.903   0.872
TLS 1.3        25   25   24   0.960   0.923 1.000   1.000      provide evidence for property p ∈ PGT . Let Ĝ be
Mean            – –     – 0.844 0.737 0.956 0.947              the normalized and deduplicated set of extracted
Total         317 305 263 Jaccard= 73.26%, F1= 84.57%          statements. An extracted statement is counted as a
                                                               true positive if it is a valid, specification-grounded
Table 7: Inter-annotator agreement over the SecGoal an-        security goal statement and matches a gold eviden-
notation set, reported by protocol before final arbitration.
                                                               tial statement; otherwise it is counted as a false
Statement F1 and Jaccard measure statement-selection
agreement; Prop. µ-F1 and κ measure property-label             positive. Thus,
agreement.                                                                                TP
                                                                               Pext =           .
                                                                                        TP + FP
B.5     Annotator Qualifications and IAA
                                                               We mark a ground-truth property as hit when its
Both annotators are PhD researchers with experi-               required evidential statement(s) are present in the
ence in cryptographic protocol analysis and sym-               true-positive extraction set; for properties with al-
bolic verification tools. A senior professor per-              ternative evidential statements, recovering any suf-
formed final arbitration. Inter-annotator agreement            ficient evidence counts as a hit. Let Phit be the set
was computed before arbitration on normalized se-              of hit properties. Property-level recall is
lected statements, with duplicates removed within
each protocol. Annotator 1 selected 317 statements                                          |Phit |
                                                                                Rprop =             .
and Annotator 2 selected 305 statements; 263 were                                           |PGT |
shared, yielding 84.57% Statement Selection F1
                                                               Finally, extraction-coverage F1 is the harmonic
and 73.26% Jaccard similarity. On shared state-
                                                               mean of these two quantities:
ments, property-label agreement reached 0.956
Prop. µ-F1 and 0.947 Cohen’s κ. Detailed protocol-                                      2 · Pext · Rprop
level results are reported in Table 7.                                     EC-F1 =                       .
                                                                                         Pext + Rprop
Worked extraction example. Assume a protocol              ber of unmatched gold properties. We compute
has six ground-truth formal properties, |PGT | = 6.
A model extracts eight statements. Five are valid                                  TP
                                                                        Pprop =           ,
security goal statements and three are operational                              TP + FP
requirements, such as message encoding rules or                                    TP
                                                                       Rprop =             ,
abort conditions. Thus T P = 5, F P = 3, and                                    TP + FN
Pext = 5/(5 + 3) = 0.625. The five true-positive                                 2Pprop Rprop
                                                                      F 1prop =               .
statements cover only five distinct formal prop-                                Pprop + Rprop
erties: one statement covers two authentication
                                                          For NSSK and Kao-Chow v1, core-field overlap is
properties, two statements redundantly support the
                                                          evaluated by strict symbolic equality: terms must
same secrecy property, and one remaining ground-
                                                          match exactly, so dec(X) is not automatically nor-
truth property is missed. Hence #Hit = 5 and
                                                          malized to X, and both core-field precision and re-
Rprop = 5/6 = 0.833. The resulting score is
                                                          call must reach τ . For EDHOC, whose properties
                                                          have more complex internal structure, the same one-
                                                          to-one matching protocol uses a coverage-based
                  2 · 0.625 · 0.833                       core-data criterion: if type, subtype, and roles
       EC-F1 =                      = 0.714.
                   0.625 + 0.833                          match, a generated property is counted as cover-
                                                          ing a gold property when it covers the gold core
                                                          data. In all protocols, unmatched generated and
This example illustrates why both dimensions are
                                                          gold properties affect property-level precision and
necessary. A model can recover most formal prop-
                                                          recall, respectively.
erties while still producing many false positives, or
                                                             Slot-level scoring. Slot-level metrics eval-
it can be precise but miss a property required for
                                                          uate whether the fields inside matched proper-
verification. EC-F1 rewards extractors that main-
                                                          ties are filled correctly. We flatten each prop-
tain downstream property coverage without flood-
                                                          erty into a set of slot tokens. For example,
ing the formalization stage with non-goal text.
                                                          an Authentication property with asserter=R,
                                                          subject=I, and agreement values TH 2, TH 3,
                                                          and TH 4 yields asserter=R, subject=I, and
Formalization metrics. For RQ3, we evaluate               one agreementValues=TH i token for each i ∈
the generated formal-property set P̂ against the          {2, 3, 4}. For a matched pair, slot true positives are
gold set PGT at two levels.                               the shared tokens, slot false positives are generated-
   Property-level matching. Each generated prop-          only tokens, and slot false negatives are gold-only
erty can be matched to at most one gold property. A       tokens:
match requires identical type and subtype, agree-                                   T Pslot
ment on the property-specific role fields, and suf-                    Pslot =                   ,
                                                                               T Pslot + F Pslot
ficient overlap on the core data fields. The default                                 T Pslot
core-field threshold is τ = 0.8. Role fields are                      Rslot =                     ,
                                                                               T Pslot + F Nslot
selected by property family: authentication proper-
                                                                                2Pslot Rslot
ties compare the two participant roles and attacker                  F 1slot =               .
                                                                               Pslot + Rslot
type; secrecy and privacy properties compare the
relevant role sets and attacker type; and special         Slot scores are computed over matched property
properties compare the subtype-specific actor or          pairs for all protocols. Unmatched generated and
role fields. Core data fields are also family-specific:   gold properties are captured by property-level pre-
authentication compares agreement values, secrecy         cision and recall, respectively, rather than being
compares secret or session data, privacy compares         double-counted as slot-level errors.
protected identity data, and special properties com-
pare the relevant parameters, compromised keys,           D   Formal Property Taxonomy and
session keys, or evidence fields.                             Templates
  Let T P be the number of generated properties           The AIFG formalization stage uses a structured
that are successfully matched, F P the number of          knowledge base to bridge natural-language proto-
unmatched generated properties, and F N the num-          col specifications and symbolic security-property
descriptions. This appendix summarizes the sup-                               Compact Formal Property Schema Skeleton
ported property taxonomy and the JSON schema
used to instantiate formalized goals.                                         [
                                                                                  {
                                                                                       "property": {
                                                                                         "type": "Secrecy",
D.1       Property Taxonomy                                                              "subtype": "[registered_secrecy_subtype]",
                                                                                         "secretData": "[Variable_Name_From_Flow]",
                                                                                         "sharedBetween": ["[RoleA]", "[RoleB]"],
The current schema covers four families of formal-                                       "attacker_type": "[passive | active]"
izable security properties:                                                            }
                                                                                  },
• Secrecy: Covers standard confidentiality, strong                                {
                                                                                       "property": {
  secrecy (indistinguishability), forward and back-                                      "type": "Authentication",
                                                                                         "subtype": "[registered_authentication_subtype
  ward secrecy, and post-compromise security vari-                                       ]",
  ants (Blanchet, 2004; Boyd et al., 2003; Cohn-                                         "asserter": "[Role_Who_Verifies]",
                                                                                         "subject": "[Role_Being_Authenticated]",
  Gordon et al., 2016).                                                                  "agreementValues": ["[Nonce_or_Key_From_Flow]"],
• Authentication:       Supports the hierarchy                                             "attacker_type": "active"
  of authentication specifications defined by                                          }
                                                                                  },
  Lowe (Lowe, 1997), including Aliveness, Weak                                    {
                                                                                       "property": {
  Agreement, Non-injective Agreement, and                                                "type": "Privacy",
                                                                                         "subtype": "[registered_privacy_subtype]",
  Injective Agreement.                                                                   "identity": "[Identity_or_Pseudonym_From_Flow]",
• Privacy: Addresses user-centric protections such
                                                                                           "sessionIdentifiers": ["[
  as Identity Protection, Anonymity, and Unlinka-                                          Session_Value_From_Flow]"],
                                                                                           "attacker_type": "[passive | active]"
  bility (Pfitzmann and Hansen, 2010).                                                 }
• Special Properties: Includes other properties                                   },
                                                                                  {
  such as Downgrade Prevention (Bhargavan et al.,                                      "property": {
                                                                                         "type": "Special",
  2016), Key Compromise Impersonation (KCI)                                              "subtype": "[registered_special_subtype]",
  protection, session independence, and Non-                                             "target": "[Negotiated_or_Evidence_Value]",
                                                                                         "dependsOn": ["[Protocol_State_or_Key]"],
  Repudiation (Boyd et al., 2003).                                                       "attacker_type": "active"
                                                                                       }
                                                                                  },
                                                                                  {
D.2       Formal Property Schema                                                       "property": {
                                                                                         "type": "Secrecy",
To avoid turning the appendix into a prompt dump,                                        "subtype": "forward_secrecy",
                                                                                         "compromisedKey": "[LongTermKey_Variable]",
we summarize the executable schema in Table 8                                            "protectedSessionData": "[
                                                                                         SessionKey_or_Message_Variable]",
and show a compact JSON skeleton below. The                                              "recoveryMechanism": "[ephemeral_key_exchange]",
complete JSON schema, including all subtype-                                               "roles": ["[RoleA]", "[RoleB]"],
specific usage guide fields, is included in the                                            "attacker_type": "active"
                                                                                       }
released artifact.                                                                },
                                                                                  {
                                                                                       "property": {
Family           Schema Summary                                                          "type": "Privacy",
                                                                                         "subtype": "unlinkability",
Secrecy          Subtypes: standard secrecy, strong secrecy,                             "unlinkableData": "[
                 forward secrecy, backward secrecy, weak pcs,                            Pseudonym_or_SessionID_Variable]",
                 full pcs.                                                               "attacker_type": "[passive | active]"
                 Core slots: protected/compromised data, roles, recovery or            }
                 healing mechanism.                                               },
                 Attacker: passive or active, subtype-dependent.                  {
Authentication   Subtypes: aliveness, weak agreement,                                  "property": {
                 non injective agreement, injective agreement.                           "type": "Special",
                 Core slots: asserter, subject, agreementValues.                         "subtype": "downgrade_protection",
                 Attacker: active.                                                       "negotiatedParams": ["[Param]"],
Privacy          Subtypes: low level privacy, anonymity,                                 "strongestMode": "[Highest_Security_Mode]",
                 unlinkability.                                                          "attacker_type": "active"
                 Core slots: identity variables, pseudonyms, session                   }
                 identifiers, compared identities.                                },
                 Attacker: passive or active.                                     {
Special          Subtypes: downgrade protection, kci protection,                       "property": {
                 session independence, non repudiation.                                  "type": "Special",
                 Core slots: negotiated parameters, compromised keys,                    "subtype": "kci_protection",
                 session keys, signature evidence.                                       "victimRole": "[Role_Being_Tricked]",
                 Attacker: active.                                                       "compromisedKey": "[LongTermKey_Variable]",
                                                                                         "attacker_type": "active"
                                                                                       }
 Table 8: Summary of the formal property schema used by                           }
                         AIFG.                                                ]
E      Prompt Templates
                                                                   Task:
We report compact prompt skeletons for readability.                Translate one natural-language security goal into
                                                                         strictly formatted JSON
The full executable prompts used in experiments,                   security properties.
including the complete few-shot demonstrations                     Inputs:
and all field-filling rules, are included in the re-               <formal_templates>{formal_templates}</
                                                                         formal_templates>
leased artifact.                                                   <output_schema>{output_schema}</output_schema>
                                                                   <protocol_flow>{protocol_flow}</protocol_flow>
                                                                   <symbol_inventory>{symbol_inventory}</
E.1      Stage I: Security Goal Extraction                               symbol_inventory>
                                                                   <role_alias_map>{role_alias_map}</role_alias_map>
The extraction prompt defines a security goal as                   <retrieved_context>{retrieved_context}</
                                                                         retrieved_context>
a protection guarantee rather than a mechanical                    <security_goal>{security_goal}</security_goal>
protocol step. The zero-shot setting uses only the                 Procedure:
task definition and input text. The few-shot setting               1. Objective identification:
                                                                      Identify the concrete security objective(s)
inserts three synthetic demonstrations with brief                        expressed or clearly entailed by
                                                                      {security_goal}, using {retrieved_context} only as
exclusion rationales before the final JSON-only                           supporting evidence.
output instruction.
                                                                   2. Protocol grounding:
                                                                      Resolve roles through {role_alias_map}. Ground all
      Extraction Prompt Skeleton                                          protocol data using exact
                                                                      symbols from {symbol_inventory} or {protocol_flow}.

      You are a formal verification expert. Extract
            verbatim sentences that express SECURITY GOALS         3. Template instantiation:
            from protocol specification text.                         Select the closest template from {formal_templates
                                                                         } for each distinct
      A security goal states a protection guarantee: what             objective and fill only fields defined in {
            asset is protected, which entity is                          output_schema}.
            authenticated, what attack is prevented, or
            what state must hold after a session.                  Key constraints:
                                                                   - Return only a valid JSON array. If no template
      Do not extract sentences that only describe message                applies, return [].
            flow, encoding, field formats, abort conditions,       - Do not invent, rename, translate, or normalize
             algorithm selection, interoperability, UI/                  protocol variables beyond
            storage requirements, physical policies, or              {symbol_inventory}.
            hardness assumptions.                                  - Use canonical role names in all role fields; do not
                                                                          place role names inside
      If a sentence mixes a security guarantee with                  agreementValues.
            mechanism details, keep it only when the               - If one goal implies multiple distinct objectives,
            guarantee is explicit and independently                      output one JSON object per
            meaningful.                                              objective.
                                                                   - For Authentication, asserter is the party receiving
      Extract complete original sentences without rewriting,              the assurance and subject
             merging, or splitting them. Remove duplicate            is the authenticated peer. agreementValues contain
            sentences while preserving document order.                   only protocol data relevant
                                                                     to the agreement objective.
      Judge by semantic intent, not by MUST/SHALL keywords.        - For Secrecy, use the concrete protocol variable
                                                                         that represents the protected
      {few_shot_demonstrations_if_any}                               data or established secret. sharedBetween lists
                                                                         legitimate holders.
      Input Text:                                                  - For Privacy, use the privacy template when the
      {input_text}                                                       protected data is an identity,
                                                                     credential identifier, endpoint identifier,
      Output only a JSON array of extracted sentences. If                metadata, or other private
            none qualify, output [].                                 identifier.
                                                                   - Use only fields defined in {output_schema}; omit
                                                                         helper or explanatory fields.

                                                                   Return only the JSON array.
E.2      Stage II: Security Goal Formalization
The formalization prompt combines the extracted
goal, retrieved protocol context, protocol-flow defi-          F    Detailed Results and Error Analysis
nitions, and the formal schema from Appendix D.
It asks the model to discover the security intent,             The main evaluation reports aggregate answers to
ground abstract concepts to exact flow variables,              the three research questions. This appendix uses
and instantiate the matching schema template.                  the complete result tables to explain where those
                                                               aggregate trends come from. We focus on protocol-
      Formalization Prompt Skeleton
                                                               level heterogeneity, calibration effects that are hid-
                                                               den by averages, and the concrete error mech-
      You are an expert Security Protocol Formalization
            Assistant.                                         anisms that connect extraction quality to down-
                                                               stream property generation.
F.1   RQ1 Complete Extraction Results                  that prompted LLMs select. Thus the main effect
Protocol difficulty is highly uneven. Table 9          of SecGoal supervision is not simply to make the
shows that the extraction problem is not uniformly     model extract more, but to change which non-goal
difficult across SecGoal. Prompted models perform      statements it rejects.
best on compact protocol descriptions whose se-        Fine-tuning does not guarantee complete goal
curity goals are close to the message-flow logic,      coverage. The EDHOC rows expose a residual
such as Kao-Chow v1, NSSK, PQXDH, SSH, and             recall limitation that is hidden by the high aver-
EDHOC. In these cases, the text contains relatively    age Rprop . Gemma2-9B-FT with section-level
little implementation or deployment material, so       chunks and 1:3 downsampling reaches high pre-
high property recall is less often accompanied by      cision, but still misses two gold properties. Man-
large volumes of irrelevant extractions. By con-       ual inspection shows that these misses trace to a
trast, QUIC, 5G-AKA, Kerberos5, FDO, OAuth2.0,         subtle EDHOC goal statement: transcript hashes
OPC-UA, and TLS 1.3 remain difficult even for          (TH 2, TH 3, and TH 4) are used for key deriva-
stronger prompted models. Their specifications         tion and as additional authenticated data. None
contain extensive interoperability, state-machine,     of the evaluated prompted or fine-tuned extractors
configuration, and implementation requirements,        selected this statement. This failure reflects two
which are security-adjacent but usually not formal-    related challenges. First, even strong LLMs still
izable goals.                                          lack sufficient formal-analysis expertise to reliably
                                                       recognize all security goal statements described in
Few-shot prompting acts as local calibration,
                                                       protocol specifications. Second, this statement is
not task learning. The per-protocol rows also
                                                       phrased through a concrete cryptographic mecha-
show that few-shot examples do not produce a sta-
                                                       nism rather than a declarative security claim. Al-
ble global decision boundary. They often improve
                                                       though this mechanism-level wording makes the
precision on verbose protocols such as TLS 1.3, but
                                                       statement look like operational protocol logic, it
can reduce property recall on protocols where the
                                                       is in fact a formalizable security goal statement
gold goals are sparse or expressed through protocol-
                                                       because it specifies the binding material that un-
specific mechanisms. For example, several models
                                                       derpins the intended authentication properties. Be-
become more selective after prompting while los-
                                                       cause all evaluated LLM extractors miss this state-
ing hits on Kerberos5, PQXDH, or SPDM. This pat-
                                                       ment, the case shows that current LLMs remain
tern suggests that in-context examples mainly tune
                                                       insufficient for complete security-goal extraction
the model’s extraction conservativeness; they do
                                                       from protocol specifications: fine-tuning improves
not provide the protocol-specific formal-analysis
                                                       selectivity, but it does not fully close coverage gaps
knowledge needed to reliably distinguish formaliz-
                                                       for mechanism-framed security goal statements.
able security goals from security-relevant mecha-
nisms. Consistent with this interpretation, a small    The remaining errors are protocol-specific.
number of few-shot outputs exhibit demonstration       The held-out protocols also reveal different resid-
leakage, where the model copies or paraphrases         ual precision failures. On OPC-UA, the best fine-
goals from the examples into the target-protocol       tuned model reaches full property recall but still
extraction; we treat these as false positives when     produces many false positives, reflecting the den-
they are not supported by the target specification.    sity of configuration, negotiation, and deployment
                                                       constraints in the specification. SPDM lies between
F.2   RQ2 Complete Fine-tuning Results                 these cases: the model recovers all properties un-
Fine-tuning changes the type of error. Table 10        der the best setting, but still includes redundant
gives a more diagnostic view of the fine-tuning        security-adjacent statements. These differences
gains reported in the main text. Encoder base-         matter because downstream formalization is af-
lines are often conservative: RoBERTa extracts         fected differently by missed goals and by redundant
few candidates and achieves perfect precision on       goals.
EDHOC, but misses many gold properties. Secure-
BERT improves coverage but extracts more false         F.3   RQ3 Complete Formalization Results
positives. The fine-tuned LLMs occupy a different      Input concision, not only correctness, affects
regime: they retain broad property coverage while      property generation. Table 11 separates two fac-
learning to suppress many operational statements       tors that are conflated in end-to-end use: whether
the required goals are present, and whether the
corresponding goal statements are concise. Under           Generated:
                                                           {
gold-minimal inputs, AIFG receives concise goal              "type": "Authentication",
                                                             "subtype": "non_injective_agreement",
statements aligned with the target property set and          "asserter": "Requester",
therefore improves coverage, especially on NSSK              "subject": "Responder",
                                                             "agreementValues": [
and SPDM, though precision remains sensitive to                 "pkR",
                                                                "nonceChallengeI",
additional generated properties and strict symbolic             "TVCA",
matching. Under expert-vetted inputs, false posi-            ],
                                                                "Tchallenge"

tives have already been removed, but the remain-             "attacker_type": "active"
                                                           }
ing extracted goal statements are longer and less          Difference: missing "digestR" (under-grounding).
canonical. The resulting drop in precision shows           EDHOC explicit key confirmation (slot P/R/F1 =
that correctness alone is insufficient: redundant or             0.800/1.000/0.889)
                                                           Gold:
over-broad goal wording can still lead AIFG to             {
                                                             "type": "Authentication",
generate additional plausible structured properties.         "subtype": "non_injective_agreement",
These additional properties are not necessarily se-          "asserter": "Responder",
                                                             "subject": "Initiator",
mantically wrong; in many cases, they reflect small          "agreementValues": [
                                                               "method",
deviations from the minimal gold property set or               "pkI",
from the canonical slot choices used for evaluation.           "pkR",
                                                               "G_X",
                                                               "G_Y",
Over-generation propagates differently at prop-                "PRK_4x3m"
                                                             ]
erty and slot levels. The expert-vetted settings           }
illustrate this distinction. AIFG generates more           Generated:
properties than in the gold-minimal setting, low-          {
                                                             "type": "Authentication",
ering property precision across all four protocols.          "subtype": "non_injective_agreement",
                                                             "asserter": "Responder",
However, the matched property pairs often retain             "subject": "Initiator",
stronger slot-level scores: NSSK and Kao-Chow                "agreementValues": [
                                                                "PRK_4x3m",
v1 reach perfect slot F1, while EDHOC and SPDM                  "pkI",
                                                                "pkR",
retain 0.85 and 0.81 slot F1, respectively. This                "G_X",
                                                                "G_Y",
suggests that AIFG can often ground roles, secrets,             "method",
and agreement values accurately once a generated                "suitesI",
                                                                "TH_4"
property is matched to a gold property, even when            ],
                                                             "attacker_type": "active"
it generates too many structured properties overall.       }
Manual inspection shows that non-perfect slot F1           Difference: extra "suitesI" and "TH_4" (over-
                                                                  grounding).
often reflects boundary errors within such matched
properties. The compact examples below illustrate
both under-grounding and over-grounding after
property-level matching. These patterns motivate
treating input concision as an important objective,
not only extraction correctness.

   Slot-Level Error Examples in Matched Properties

   SPDM authentication (slot P/R/F1 = 1.000/0.875/0.933)
   Gold:
   {
     "type": "Authentication",
     "subtype": "non_injective_agreement",
     "asserter": "Requester",
     "subject": "Responder",
     "agreementValues": [
        "pkR",
        "digestR",
        "nonceChallengeI",
        "TVCA",
        "Tchallenge"
     ],
     "attacker_type": "active"
   }
Table 9: Complete RQ1 extraction results by model and protocol. ZS and FS denote zero-shot and few-shot
prompting.

            Model                    Protocol      GT ZS-Pext ZS-Rprop ZS-EC-F1 FS-Pext FS-Rprop FS-EC-F1
            Claude-Sonnet-4-6        5G-AKA        11    0.099   1.000   0.180    0.105   1.000    0.191
            Claude-Sonnet-4-6        EDHOC         17    0.270   0.765   0.399    0.287   0.765    0.418
            Claude-Sonnet-4-6        FDO             6   0.125   1.000   0.222    0.138   1.000    0.243
            Claude-Sonnet-4-6        FIDO2         15    0.182   1.000   0.309    0.194   1.000    0.324
            Claude-Sonnet-4-6        IKEv2           8   0.131   1.000   0.232    0.131   1.000    0.232
            Claude-Sonnet-4-6        Kao-Chow v1     5   0.394   1.000   0.565    0.429   1.000    0.600
            Claude-Sonnet-4-6        Kerberos5       9   0.116   1.000   0.208    0.123   1.000    0.219
            Claude-Sonnet-4-6        NSSK            5   0.343   1.000   0.511    0.361   1.000    0.531
            Claude-Sonnet-4-6        OAuth2.0        7   0.133   1.000   0.235    0.141   1.000    0.248
            Claude-Sonnet-4-6        OPC-UA          6   0.101   1.000   0.183    0.129   1.000    0.229
            Claude-Sonnet-4-6        PQXDH           7   0.293   1.000   0.453    0.333   1.000    0.500
            Claude-Sonnet-4-6        QUIC            7   0.076   1.000   0.140    0.076   1.000    0.141
            Claude-Sonnet-4-6        SPDM            8   0.214   1.000   0.353    0.185   1.000    0.312
            Claude-Sonnet-4-6        SSH             8   0.414   1.000   0.585    0.400   1.000    0.571
            Claude-Sonnet-4-6        TLS 1.3       12    0.147   1.000   0.257    0.163   1.000    0.280
            Claude-Sonnet-4-6        Average       8.7   0.203   0.984   0.322    0.213   0.984    0.336
            DeepSeek-V4-Flash        5G-AKA         11   0.114   1.000   0.204    0.138   1.000    0.243
            DeepSeek-V4-Flash        EDHOC          17   0.309   0.765   0.440    0.382   0.647    0.481
            DeepSeek-V4-Flash        FDO             6   0.118   1.000   0.211    0.134   1.000    0.237
            DeepSeek-V4-Flash        FIDO2          15   0.353   1.000   0.522    0.492   1.000    0.659
            DeepSeek-V4-Flash        IKEv2           8   0.179   1.000   0.304    0.173   1.000    0.295
            DeepSeek-V4-Flash        Kao-Chow v1     5   0.471   1.000   0.640    0.421   1.000    0.593
            DeepSeek-V4-Flash        Kerberos5       9   0.131   1.000   0.231    0.156   1.000    0.270
            DeepSeek-V4-Flash        NSSK            5   0.385   1.000   0.556    0.385   1.000    0.556
            DeepSeek-V4-Flash        OAuth2.0        7   0.145   1.000   0.254    0.161   1.000    0.277
            DeepSeek-V4-Flash        OPC-UA          6   0.131   1.000   0.232    0.137   1.000    0.241
            DeepSeek-V4-Flash        PQXDH           7   0.474   0.857   0.610    0.643   0.857    0.735
            DeepSeek-V4-Flash        QUIC            7   0.080   1.000   0.148    0.110   1.000    0.199
            DeepSeek-V4-Flash        SPDM            8   0.165   0.875   0.277    0.218   0.875    0.349
            DeepSeek-V4-Flash        SSH             8   0.280   0.875   0.424    0.364   0.875    0.514
            DeepSeek-V4-Flash        TLS 1.3       12    0.142   0.833   0.243    0.217   1.000    0.357
            DeepSeek-V4-Flash        Average       8.7   0.232   0.947   0.353    0.275   0.950    0.400
            DeepSeek-V4-Pro          5G-AKA         11   0.124   1.000   0.220    0.141   1.000    0.247
            DeepSeek-V4-Pro          EDHOC          17   0.338   0.765   0.468    0.448   0.765    0.565
            DeepSeek-V4-Pro          FDO             6   0.137   1.000   0.242    0.143   1.000    0.250
            DeepSeek-V4-Pro          FIDO2          15   0.545   1.000   0.706    0.480   1.000    0.649
            DeepSeek-V4-Pro          IKEv2           8   0.126   1.000   0.224    0.156   1.000    0.269
            DeepSeek-V4-Pro          Kao-Chow v1     5   0.458   1.000   0.629    0.550   1.000    0.710
            DeepSeek-V4-Pro          Kerberos5       9   0.133   1.000   0.235    0.138   0.889    0.239
            DeepSeek-V4-Pro          NSSK            5   0.385   1.000   0.556    0.429   1.000    0.600
            DeepSeek-V4-Pro          OAuth2.0        7   0.165   1.000   0.283    0.162   0.857    0.272
            DeepSeek-V4-Pro          OPC-UA          6   0.130   1.000   0.230    0.157   1.000    0.271
            DeepSeek-V4-Pro          PQXDH           7   0.429   0.857   0.571    0.643   0.857    0.735
            DeepSeek-V4-Pro          QUIC            7   0.070   1.000   0.131    0.087   1.000    0.161
            DeepSeek-V4-Pro          SPDM            8   0.133   0.875   0.230    0.188   1.000    0.316
            DeepSeek-V4-Pro          SSH             8   0.296   0.875   0.443    0.320   0.875    0.469
            DeepSeek-V4-Pro          TLS 1.3       12    0.146   1.000   0.255    0.186   1.000    0.313
            DeepSeek-V4-Pro          Average       8.7   0.241   0.958   0.361    0.282   0.950    0.404
            Gemini-3-Flash-Preview   5G-AKA         11   0.125   1.000   0.222    0.183   1.000    0.309
            Gemini-3-Flash-Preview   EDHOC          17   0.349   0.765   0.480    0.441   0.765    0.559
            Gemini-3-Flash-Preview   FDO             6   0.142   1.000   0.248    0.161   1.000    0.277
            Gemini-3-Flash-Preview   FIDO2          15   0.283   1.000   0.441    0.381   1.000    0.552
            Gemini-3-Flash-Preview   IKEv2           8   0.148   1.000   0.257    0.189   1.000    0.318
            Gemini-3-Flash-Preview   Kao-Chow v1     5   0.480   1.000   0.649    0.400   1.000    0.571
            Gemini-3-Flash-Preview   Kerberos5       9   0.133   1.000   0.235    0.162   0.778    0.269
            Gemini-3-Flash-Preview   NSSK            5   0.414   1.000   0.585    0.500   1.000    0.667
            Gemini-3-Flash-Preview   OAuth2.0        7   0.176   1.000   0.299    0.168   1.000    0.288
            Gemini-3-Flash-Preview   OPC-UA          6   0.121   1.000   0.216    0.198   1.000    0.331
            Gemini-3-Flash-Preview   PQXDH           7   0.476   0.857   0.612    0.538   0.857    0.661
            Gemini-3-Flash-Preview   QUIC            7   0.096   1.000   0.175    0.099   1.000    0.180
            Gemini-3-Flash-Preview   SPDM            8   0.193   0.875   0.316    0.260   0.875    0.401
            Gemini-3-Flash-Preview   SSH             8   0.435   0.875   0.581    0.625   0.875    0.729
            Gemini-3-Flash-Preview   TLS 1.3        12   0.216   1.000   0.356    0.229   1.000    0.372
            Gemini-3-Flash-Preview   Average       8.7   0.252   0.958   0.378    0.302   0.943    0.432
            Gemini-3-Pro-Preview     5G-AKA         11   0.160   0.909   0.272    0.209   1.000    0.345
            Gemini-3-Pro-Preview     EDHOC          17   0.464   0.765   0.578    0.581   0.765    0.661
            Gemini-3-Pro-Preview     FDO             6   0.189   1.000   0.319    0.210   1.000    0.347
            Gemini-3-Pro-Preview     FIDO2          15   0.439   1.000   0.610    0.521   1.000    0.685
            Gemini-3-Pro-Preview     IKEv2           8   0.280   1.000   0.438    0.282   1.000    0.440
            Gemini-3-Pro-Preview     Kao-Chow v1     5   0.500   1.000   0.667    0.526   1.000    0.690
            Gemini-3-Pro-Preview     Kerberos5       9   0.179   0.889   0.299    0.241   0.778    0.368
            Gemini-3-Pro-Preview     NSSK            5   0.435   1.000   0.606    0.435   1.000    0.606
            Gemini-3-Pro-Preview     OAuth2.0        7   0.183   1.000   0.310    0.214   1.000    0.353
            Gemini-3-Pro-Preview     OPC-UA          6   0.180   1.000   0.306    0.222   1.000    0.364
            Gemini-3-Pro-Preview     PQXDH           7   0.500   0.857   0.632    0.636   0.857    0.730
            Gemini-3-Pro-Preview     QUIC            7   0.112   1.000   0.201    0.148   1.000    0.257
            Gemini-3-Pro-Preview     SPDM            8   0.317   0.875   0.465    0.286   0.875    0.431
            Gemini-3-Pro-Preview     SSH             8   0.529   0.875   0.660    0.563   0.875    0.685
            Gemini-3-Pro-Preview     TLS 1.3        12   0.267   1.000   0.421    0.321   1.000    0.486
            Gemini-3-Pro-Preview     Average       8.7   0.316   0.945   0.452    0.360   0.943    0.496
            GLM-5                    5G-AKA        11    0.169   1.000   0.289    0.225   1.000    0.367
            Continued on next page
                  Table 9: Complete RQ1 extraction results (continued).

Model                 Protocol      GT ZS-Pext ZS-Rprop ZS-EC-F1 FS-Pext FS-Rprop FS-EC-F1
GLM-5                 EDHOC          17   0.468   0.765   0.580    0.628   0.765    0.690
GLM-5                 FDO             6   0.167   1.000   0.286    0.243   1.000    0.391
GLM-5                 FIDO2          15   0.440   1.000   0.611    0.485   1.000    0.653
GLM-5                 IKEv2           8   0.218   1.000   0.358    0.360   1.000    0.529
GLM-5                 Kao-Chow v1     5   0.455   1.000   0.625    0.600   1.000    0.750
GLM-5                 Kerberos5       9   0.177   0.889   0.295    0.278   0.556    0.370
GLM-5                 NSSK            5   0.400   1.000   0.571    0.385   1.000    0.556
GLM-5                 OAuth2.0        7   0.214   1.000   0.352    0.211   0.857    0.339
GLM-5                 OPC-UA          6   0.156   1.000   0.270    0.247   1.000    0.396
GLM-5                 PQXDH           7   0.524   0.857   0.650    0.300   0.571    0.393
GLM-5                 QUIC            7   0.139   1.000   0.244    0.161   1.000    0.278
GLM-5                 SPDM            8   0.292   1.000   0.452    0.316   0.875    0.464
GLM-5                 SSH             8   0.563   0.875   0.685    0.636   0.875    0.737
GLM-5                 TLS 1.3        12   0.246   1.000   0.395    0.356   1.000    0.525
GLM-5                 Average       8.7   0.308   0.959   0.444    0.362   0.900    0.496
GPT-5.4               5G-AKA         11   0.112   1.000   0.202    0.119   1.000    0.212
GPT-5.4               EDHOC          17   0.270   0.765   0.399    0.370   0.765    0.499
GPT-5.4               FDO             6   0.142   1.000   0.248    0.168   1.000    0.288
GPT-5.4               FIDO2          15   0.277   1.000   0.434    0.304   1.000    0.467
GPT-5.4               IKEv2           8   0.133   1.000   0.235    0.151   1.000    0.262
GPT-5.4               Kao-Chow v1     5   0.407   1.000   0.579    0.435   1.000    0.606
GPT-5.4               Kerberos5       9   0.123   1.000   0.220    0.124   1.000    0.220
GPT-5.4               NSSK            5   0.361   1.000   0.531    0.353   1.000    0.522
GPT-5.4               OAuth2.0        7   0.152   1.000   0.264    0.145   1.000    0.254
GPT-5.4               OPC-UA          6   0.118   1.000   0.211    0.128   1.000    0.227
GPT-5.4               PQXDH           7   0.323   1.000   0.488    0.333   1.000    0.500
GPT-5.4               QUIC            7   0.072   1.000   0.135    0.077   1.000    0.143
GPT-5.4               SPDM            8   0.136   0.875   0.236    0.261   0.875    0.402
GPT-5.4               SSH             8   0.316   1.000   0.480    0.429   1.000    0.600
GPT-5.4               TLS 1.3        12   0.160   1.000   0.276    0.186   1.000    0.313
GPT-5.4               Average       8.7   0.207   0.976   0.329    0.239   0.976    0.368
Qwen3.5-Plus          5G-AKA         11   0.137   1.000   0.241    0.184   0.909    0.306
Qwen3.5-Plus          EDHOC          17   0.475   0.765   0.586    0.596   0.765    0.670
Qwen3.5-Plus          FDO             6   0.139   1.000   0.245    0.189   1.000    0.318
Qwen3.5-Plus          FIDO2          15   0.366   1.000   0.536    0.512   1.000    0.677
Qwen3.5-Plus          IKEv2           8   0.158   0.875   0.268    0.250   0.875    0.389
Qwen3.5-Plus          Kao-Chow v1     5   0.480   1.000   0.649    0.500   1.000    0.667
Qwen3.5-Plus          Kerberos5       9   0.175   0.889   0.292    0.227   0.667    0.338
Qwen3.5-Plus          NSSK            5   0.435   1.000   0.606    0.417   1.000    0.588
Qwen3.5-Plus          OAuth2.0        7   0.183   1.000   0.310    0.179   1.000    0.303
Qwen3.5-Plus          OPC-UA          6   0.176   1.000   0.300    0.237   1.000    0.383
Qwen3.5-Plus          PQXDH           7   0.588   0.857   0.698    0.875   0.857    0.866
Qwen3.5-Plus          QUIC            7   0.124   1.000   0.220    0.127   1.000    0.225
Qwen3.5-Plus          SPDM            8   0.250   0.875   0.389    0.345   0.875    0.495
Qwen3.5-Plus          SSH             8   0.474   0.875   0.615    0.533   0.875    0.663
Qwen3.5-Plus          TLS 1.3       12    0.197   1.000   0.330    0.297   1.000    0.458
Qwen3.5-Plus          Average       8.7   0.291   0.942   0.419    0.364   0.922    0.490
Gemma2-9B-Instruct    5G-AKA         11   0.063   0.455   0.110    0.064   0.455    0.112
Gemma2-9B-Instruct    EDHOC          17   0.259   0.647   0.370    0.291   0.647    0.402
Gemma2-9B-Instruct    FDO             6   0.053   0.833   0.100    0.068   0.833    0.126
Gemma2-9B-Instruct    FIDO2          15   0.078   0.800   0.142    0.096   0.867    0.173
Gemma2-9B-Instruct    IKEv2           8   0.057   1.000   0.109    0.060   0.875    0.112
Gemma2-9B-Instruct    Kao-Chow v1     5   0.350   1.000   0.519    0.320   1.000    0.485
Gemma2-9B-Instruct    Kerberos5       9   0.082   0.667   0.146    0.087   0.667    0.153
Gemma2-9B-Instruct    NSSK            5   0.345   1.000   0.513    0.406   1.000    0.578
Gemma2-9B-Instruct    OAuth2.0        7   0.087   1.000   0.161    0.091   1.000    0.167
Gemma2-9B-Instruct    OPC-UA          6   0.082   1.000   0.151    0.077   1.000    0.143
Gemma2-9B-Instruct    PQXDH           7   0.200   0.857   0.324    0.214   0.571    0.312
Gemma2-9B-Instruct    QUIC            7   0.030   0.571   0.058    0.036   0.857    0.069
Gemma2-9B-Instruct    SPDM            8   0.078   0.750   0.141    0.107   0.750    0.188
Gemma2-9B-Instruct    SSH             8   0.100   0.625   0.172    0.129   0.500    0.205
Gemma2-9B-Instruct    TLS 1.3        12   0.047   0.500   0.086    0.089   0.750    0.159
Gemma2-9B-Instruct    Average       8.7   0.127   0.780   0.207    0.142   0.785    0.226
Qwen2.5-7B-Instruct   5G-AKA         11   0.162   0.818   0.270    0.216   0.364    0.271
Qwen2.5-7B-Instruct   EDHOC          17   0.477   0.765   0.588    0.424   0.706    0.530
Qwen2.5-7B-Instruct   FDO             6   0.194   1.000   0.325    0.200   0.667    0.308
Qwen2.5-7B-Instruct   FIDO2          15   0.149   0.800   0.252    0.189   0.800    0.305
Qwen2.5-7B-Instruct   IKEv2           8   0.048   0.625   0.090    0.051   0.250    0.085
Qwen2.5-7B-Instruct   Kao-Chow v1     5   0.500   1.000   0.667    0.333   1.000    0.500
Qwen2.5-7B-Instruct   Kerberos5       9   0.141   0.556   0.225    0.167   0.333    0.222
Qwen2.5-7B-Instruct   NSSK            5   0.348   1.000   0.516    0.545   1.000    0.706
Qwen2.5-7B-Instruct   OAuth2.0        7   0.141   1.000   0.247    0.198   1.000    0.330
Qwen2.5-7B-Instruct   OPC-UA          6   0.185   1.000   0.313    0.182   1.000    0.308
Qwen2.5-7B-Instruct   PQXDH           7   0.300   0.714   0.423    0.200   0.571    0.296
Qwen2.5-7B-Instruct   QUIC            7   0.030   0.857   0.057    0.131   0.714    0.222
Qwen2.5-7B-Instruct   SPDM            8   0.154   0.750   0.255    0.143   0.500    0.222
Qwen2.5-7B-Instruct   SSH             8   0.250   0.500   0.333    0.300   0.375    0.333
Qwen2.5-7B-Instruct   TLS 1.3       12    0.085   0.833   0.154    0.153   0.667    0.248
Qwen2.5-7B-Instruct   Average       8.7   0.211   0.815   0.314    0.229   0.663    0.326
Table 10: Complete RQ2 test-set extraction results. In Gemma2-9B-FT variants, sent. denotes sentence-window
chunking and sect. denotes section-level chunking.

                         Model                         Protocol        GT Ext.     TP    FP #Hit Pext Rprop EC-F1
                         RoBERTa                       EDHOC            17     7     7     0     8   1.000     0.471     0.640
                         RoBERTa                       Kao-Chow v1       5    10     6     4     4   0.600     0.800     0.686
                         RoBERTa                       NSSK              5    11     6     5     4   0.545     0.800     0.649
                         RoBERTa                       OPC-UA            6     4     1     3     1   0.250     0.167     0.200
                         RoBERTa                       SPDM              8     6     3     3     7   0.500     0.875     0.636
                         RoBERTa                       Average         8.2   7.6   4.6   3.0   4.8   0.579     0.622     0.562
                         SecureBERT                    EDHOC            17   16   11       5     9   0.688     0.529     0.598
                         SecureBERT                    Kao-Chow v1       5   21   13       8     5   0.619     1.000     0.765
                         SecureBERT                    NSSK              5   22   14       8     5   0.636     1.000     0.778
                         SecureBERT                    OPC-UA            6   18    7      11     5   0.389     0.833     0.530
                         SecureBERT                    SPDM              8   12    8       4     5   0.667     0.625     0.645
                         SecureBERT                    Average         8.2 17.8 10.6     7.2   5.8   0.600     0.798     0.663
                         Qwen2.5-7B-FT                 EDHOC            17   32   19   13       13   0.594     0.765     0.668
                         Qwen2.5-7B-FT                 Kao-Chow v1       5   13   10    3        5   0.769     1.000     0.870
                         Qwen2.5-7B-FT                 NSSK              5   11    8    3        5   0.727     1.000     0.842
                         Qwen2.5-7B-FT                 OPC-UA            6   52   15   37        6   0.288     1.000     0.448
                         Qwen2.5-7B-FT                 SPDM              8   11    6    5        5   0.545     0.625     0.583
                         Qwen2.5-7B-FT                 Average         8.2 23.8 11.6 12.2      6.8   0.585     0.878     0.682
                         Gemma2-9B-FT (sent., none)    EDHOC            17   25   19       6    10   0.760     0.588     0.663
                         Gemma2-9B-FT (sent., none)    Kao-Chow v1       5   11    8       3     5   0.727     1.000     0.842
                         Gemma2-9B-FT (sent., none)    NSSK              5   15    8       7     5   0.533     1.000     0.696
                         Gemma2-9B-FT (sent., none)    OPC-UA            6   30   15      15     5   0.500     0.833     0.625
                         Gemma2-9B-FT (sent., none)    SPDM              8   11    7       4     6   0.636     0.750     0.689
                         Gemma2-9B-FT (sent., none)    Average         8.2 18.4 11.4     7.0   6.2   0.631     0.834     0.703
                         Gemma2-9B-FT (sent., 1:3)     EDHOC            17   31   23       8    11   0.742     0.647     0.691
                         Gemma2-9B-FT (sent., 1:3)     Kao-Chow v1       5   13    8       5     5   0.615     1.000     0.762
                         Gemma2-9B-FT (sent., 1:3)     NSSK              5   14    9       5     5   0.643     1.000     0.783
                         Gemma2-9B-FT (sent., 1:3)     OPC-UA            6   38   19      19     6   0.500     1.000     0.667
                         Gemma2-9B-FT (sent., 1:3)     SPDM              8   14   11       3     7   0.786     0.875     0.828
                         Gemma2-9B-FT (sent., 1:3)     Average         8.2 22.0 14.0     8.0   6.8   0.657     0.904     0.746
                         Gemma2-9B-FT (sect., none)    EDHOC            17   30   22       8    14   0.733     0.824     0.776
                         Gemma2-9B-FT (sect., none)    Kao-Chow v1       5   10    7       3     5   0.700     1.000     0.824
                         Gemma2-9B-FT (sect., none)    NSSK              5    9    5       4     3   0.556     0.600     0.577
                         Gemma2-9B-FT (sect., none)    OPC-UA            6   32   15      17     6   0.469     1.000     0.638
                         Gemma2-9B-FT (sect., none)    SPDM              8   10    6       4     7   0.600     0.875     0.712
                         Gemma2-9B-FT (sect., none)    Average         8.2 18.2 11.0     7.2   7.0   0.612     0.860     0.705
                         Gemma2-9B-FT (sect., 1:3)     EDHOC            17   33   27       6    15   0.818     0.882     0.849
                         Gemma2-9B-FT (sect., 1:3)     Kao-Chow v1       5    9    8       1     5   0.889     1.000     0.941
                         Gemma2-9B-FT (sect., 1:3)     NSSK              5   10    6       4     5   0.600     1.000     0.750
                         Gemma2-9B-FT (sect., 1:3)     OPC-UA            6   36   16      20     6   0.444     1.000     0.615
                         Gemma2-9B-FT (sect., 1:3)     SPDM              8   19   11       8     8   0.579     1.000     0.733
                         Gemma2-9B-FT (sect., 1:3)     Average         8.2 21.4 13.6     7.8   7.8   0.666     0.976     0.778


Protocol      Input          Gold       Gen.          TP          FP         FN                Property                                Slot
                                                                                         P           R          F1          P           R           F1

NSSK          gold-minimal 5.00±0.00 6.33±0.94 5.00±0.00 2.00±0.00 0.00±0.00 0.71±0.00         1.00±0.00     0.83±0.00   0.93±0.09   1.00±0.00   0.96±0.05
NSSK          expert-vetted 5.00±0.00 8.67±0.94 5.00±0.00 3.67±0.94 0.00±0.00 0.58±0.06        1.00±0.00     0.74±0.05   1.00±0.00   1.00±0.00   1.00±0.00
Kao-Chow v1   gold-minimal 5.00±0.00 5.00±0.00 3.67±0.94 1.33±0.94 1.33±0.94 0.73±0.19         0.73±0.19     0.73±0.19   0.89±0.08   1.00±0.00   0.94±0.04
Kao-Chow v1   expert-vetted 5.00±0.00 13.33±0.94 5.00±0.00 8.33±0.94 0.00±0.00 0.38±0.03       1.00±0.00     0.55±0.03   1.00±0.00   1.00±0.00   1.00±0.00
EDHOC         gold-minimal 17.00±0.00 20.00±0.00 14.67±0.47 5.33±0.47 2.33±0.47 0.73±0.02      0.86±0.03     0.79±0.03   0.85±0.00   0.89±0.00   0.87±0.00
EDHOC         expert-vetted 17.00±0.00 34.33±2.36 13.00±0.00 21.33±2.36 4.00±0.00 0.38±0.03    0.76±0.00     0.51±0.02   0.83±0.01   0.89±0.00   0.85±0.01
SPDM          gold-minimal 8.00±0.00 12.33±1.70 7.33±0.94 6.00±1.41 0.67±0.94 0.55±0.08        0.92±0.12     0.69±0.09   0.77±0.08   0.98±0.02   0.84±0.06
SPDM          expert-vetted 8.00±0.00 21.00±0.82 5.67±0.47 15.67±0.94 2.33±0.47 0.27±0.03      0.71±0.06     0.39±0.04   0.73±0.06   0.95±0.01   0.81±0.05


Table 11: Complete RQ3 formalization results under the property-level and slot-level evaluation, reported as mean
± standard deviation over three runs.
