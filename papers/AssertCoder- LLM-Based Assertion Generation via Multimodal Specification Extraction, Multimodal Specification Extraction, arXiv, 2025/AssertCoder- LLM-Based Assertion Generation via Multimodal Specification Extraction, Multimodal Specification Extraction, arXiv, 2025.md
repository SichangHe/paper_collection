                                          AssertCoder: LLM-Based Assertion Generation via
                                                 Multimodal Specification Extraction
                                                                  Enyuan Tian                                  Yiwei Ci, Qiusong Yang*
                                              Institute of Software, Chinese Academy of Sciences Institute of Software, Chinese Academy of Sciences
                                                  University of Chinese Academy of Sciences                         Beijing, China
                                                                 Beijing, China                              {yiwei, qiusong}@iscas.ac.cn
                                                         tianenyuan22@mails.ucas.ac.cn

                                                                    Yufeng Li                                                     Zhichao Lyu
                                                   Institute of Computing Technology, Chinese                 Institute of Software, Chinese Academy of Sciences
arXiv:2507.10338v1 [cs.SE] 14 Jul 2025




                                                                Academy of Sciences                                               Beijing, China
                                                                   Beijing, China                                         lvzhichao18@mails.ucas.ac.cn
                                                            crazybinary494@gmail.com

                                            Abstract—Assertion-Based Verification (ABV) is critical for en-    from the semantic gap between semi-structured specifica-
                                         suring functional correctness in modern hardware systems. How-        tions and the formal temporal logic required for assertions
                                         ever, manually writing high-quality SVAs remains labor-intensive      [13]. While specifications are multimodal, their translation
                                         and error-prone. To bridge this gap, we propose AssertCoder,
                                         a novel unified framework that automatically generates high-          into precise, semantically consistent SVAs lacks systematic
                                         quality SVAs directly from multimodal hardware design specifica-      methodologies, often leading to semantic mapping errors.
                                         tions. AssertCoder employs a modality-sensitive preprocessing to         With the recent advances in Large Language Model (LLM),
                                         parse heterogeneous specification formats (text, tables, diagrams,    researchers apply LLM to generate assertion from specifi-
                                         and formulas), followed by a set of dedicated semantic analyzers      cations. Some attempts [14]–[17] primarily explored few-
                                         that extract structured representations aligned with signal-level
                                         semantics. These representations are utilized to drive assertion      shot and zero-shot LLM prompting to generate SVAs from
                                         synthesis via multi-step chain-of-thought (CoT) prompting. The        high-level specifications. Although they are suitable for low-
                                         framework incorporates a mutation-based evaluation approach           complexity specifications, such methods often struggle to
                                         to assess assertion quality via model checking and further refine     generalize across the wide spectrum of specification formats,
                                         the generated assertions. Experimental evaluation across three        which include tabular structures, architectural diagrams, and
                                         real-world Register-Transfer Level (RTL) designs demonstrates
                                         AssertCoder’s superior performance, achieving an average in-          symbolic timing constraints. Other approaches, such as [18]–
                                         crease of 8.4% in functional correctness and 5.8% in mutation         [20], adopt a single generation paradigm without incorporating
                                         detection compared to existing state-of-the-art approaches.           semantic feedback, limiting their ability to handle ambiguity
                                            Index Terms—Hardware Formal Verification, Assertion Gen-           and ensure assertion completeness.
                                         eration, Large Language Models.                                          To address these limitations, we introduce AssertCoder, a
                                                                                                               unified framework for synthesizing SVAs from multimodal
                                                                I. I NTRODUCTION                               hardware design specifications. AssertCoder initiates with
                                            Modern system-on-chip (SoC) designs require rigorous               modality-aware preprocessing and dedicated analyzers that
                                         functional verification to ensure correctness under complex           extract structured, signal-level information from diverse spec-
                                         control logic, aggressive timing constraints, and highly inter-       ifications (text, tables, diagrams, and formulas). These are
                                         connected subsystems. Assertion-Based Verification (ABV),             consolidated into a unified intermediate representation, en-
                                         a cornerstone of formal verification, addresses this need by          abling assertion generation via a multi-step CoT prompting
                                         embedding behavioral specifications as SVAs [1]. These asser-         strategy [21]. To ensure the quality of SVAs, AssertCoder
                                         tions act as temporal monitors, enabling early bug detection          incorporates a mutation-guided evaluation and refinement with
                                         through both simulation and formal analysis. However, manual          model checking [22], allowing regeneration of assertions in
                                         SVA development remains a scalability bottleneck due to its           response to undetected mutation iteratively. This integration
                                         labor-intensive nature and reliance on domain expertise [2].          of semantic abstraction, structured prompting, and feedback-
                                            To address this challenge, researchers investigated methods        guided refinement enables high-quality assertion generation
                                         based on static analysis [3], [4], dynamic data mining [5]–[7]        across real-world RTL designs.
                                         and natural language processing [8]–[12], aiming to extract              Our main contributions are as follows:
                                         assertions directly from specification. A key challenge stems            1. We propose a modality-sensitive classification and anal-
                                                                                                               ysis mechanism that dispatches heterogeneous specification
                                           * Corresponding author: Qiusong Yang                                content (text, tables, diagrams, and formulas) to dedicated
                                         TABLE I: COMPARISONS OF LLM-BASED ASSERTION GENERATION METHODS
                                Framework            SPEC                           Main                              RAG                Verification   Testbench      Iterative
       Method/Citation
                                   Input            Modality                    Prompt Strategy                    Integration             Target         Scale       Refinement
         AssertLLM [14]                               Multi                                                             ✓
                                  SPEC                                      Template-based Structured                                    Functional     Mid-scale           ✗
       (Yan et al., 2024)                    (only Waveform Diagram)                                             (SVA Textbooks)
      AssertionForge [18]                                                                                               ✓
                                RTL + SPEC          Text-only                  Task Decomposition                                        Functional     Large-scale         ✗
        (Bai et al., 2025)                                                                                         (Garph RAG)
      Spec2Assertion [19]
                                  SPEC              Text-only             Progressive Regularization CoT                ✗                Functional     Mid-scale           ✗
        (Wu et al., 2025)
    Assertion by LLMs [17]                                                                                                                                                 ✓
                                RTL + SPEC          Text-only           Few-shot with Structured Examples               ✗                  Security     Mid-scale
      (Kande et al., 2024)                                                                                                                                              (Manual)
         ChIRAAG [15]                                                                                                                                                      ✓
                                RTL + SPEC          Text-only             Structured Prompting via JSON                 ✗                Functional     Mid-scale
       (Mali et al., 2024)                                                                                                                                              (Partial† )
          NL2SVA [16]                                                                                                                                                      ✓
                                RTL + SPEC          Text-only                   Circuit-aware CoT                       ✗                Functional     Small-scale
       (Sun et al., 2024)                                                                                                                                               (Manual)
      AssertionLLM [20]
                                RTL + SPEC          Text-only               Instruction-style Prompting                 ✗                Functional     Mid-scale           ✗
    (Pulavarthi et al., 2025)
          AssertCoder                                        *                                                         ✓                                                   ✓
                                  SPEC               Multi              Alignment-aware Multi-step CoT                                   Functional     Full-scale
          (Our Work)                                                                                         (Design-aware Retrieval)                                 (Automatic)
*
  Multimodal specification includes state diagrams, dataflow diagrams, architecture blocks, etc., all transferred into pseudo-code or natural language to enhance LLM understanding.
†
  ChIRAAG performs partial automated refinement, handling only syntax, basic timing, and missing signal errors; most assertion and design issues still require manual intervention.

analyzers. Each analyzer extracts structured semantic repre-                                   Compared to these methods, our approach focuses on com-
sentations, which are converted into a unified information                                  prehensive modality semantic extraction, structured prompt-
specification to support the SVA generation task.                                           ing, and mutation-guided refinement, without RTL informa-
   2. We develop a semantics-driven, retrieval-augmented as-                                tion. As summarized in Table I, it combines multimodal
sertion synthesis engine that converts structured specification                             specification extraction through alignment-aware, multi-step
into formal properties via a four-step process: unified semantic                            CoT reasoning with automatic assertion refinement.
decomposition, pattern selection, temporal binding, and SVA
syntax synthesis. The method dynamically selects and instan-                                                III. T HE A SSERT C ODER F RAMEWORK
tiates assertion templates using timing and signal semantics.                               A. Overview
   3. We adopt a mutation-based approach to evaluate the                                       The AssertCoder framework is designed to generate SVAs
functionality covered by assertions, aiming to enhance their                                from multimodal specifications. As shown in Fig. 1, Assert-
quality. To comprehensively assess assertion coverage, we                                   Coder decomposes the overall process into four stages: (1)
employ model checking. This process involves refining asser-                                SPEC Preprocessing, (2) Multimodal Information Extrac-
tions to verify functionality with undetected mutations. As a                               tion, (3) SVA Generation, and (4) Evaluation and Iteration.
result, potential bugs can be identified through these enhanced                             It integrates a modality-sensitive analysis, multi-step CoT
assertions.                                                                                 prompting, semantic alignment and retrieval-augmented gener-
   4. We implement and evaluate the framework on 3 real-                                    ation (RAG) to transform specifications into SVAs. To ensure
world RTL modules with multimodal specifications. The re-                                   high-quality assertion generation, the framework incorporates
sults show that the SVA generated by our framework, com-                                    a mutation-based mechanism that systematically evaluates the
pared to the baseline, not only generate a greater number                                   effectiveness of assertion sets through model checking and
of syntax correctness SVAs, but also increases the functional                               guides iterative refinement through feedback.
correctness by 8.4% and the mutation detection by 5.8%.
                     II. R ELATED W ORK                                                     B. SPEC Preprocessing
   Prior efforts in assertion generation span a spectrum                                       To robustly process specifications, often delivered as PDFs
of methodologies, ranging from RTL-guided methods to                                        containing text, tables, diagrams, and formulas, AssertCoder
specification-based approaches. Table I provides a comparative                              initiates with a preprocessing stage that segments the docu-
overview of representative works.                                                           ment into structurally meaningful blocks. This step is essential
   Recent works, such as AssertionForge [18], NL2SVA [16],                                  for enabling modality-sensitive analysis in later stages.
and AssertionLLM [20], rely on both RTL and specification                                      We adopt a hybrid approach combining classical document
as input. While RTL provides refined temporal semantics                                     parsing and LLM-based semantic classification. The PDF is
and signal-level observability, these methods risk semantic                                 first parsed using LayoutParser [23], a deep learning layout
drift if the design under test (DUT) contains bugs. During                                  analyzer pretrained on PubLayNet [24], to extract visual
the generation process, reliance on these error information                                 elements such as paragraphs, tables, and diagrams, along with
inevitably has an impact on SVA, leading to degraded assertion                              bounding boxes, content type hints, and position information.
quality.                                                                                       The output of this parser ensemble is a flattened token
   In contrast, Spec2Assertion [19] and AssertLLM [14] oper-                                stream composed of content blocks, each enriched with layout-
ate solely on textual or waveform-based specifications. How-                                derived information. These candidate blocks are passed to
ever, these systems do not fully leverage the multimodal                                    an LLM via prompting strategy for semantic classification.
abundance of design documents (tables, timing diagrams, and                                 For each block, the LLM outputs two key attributes: the
architectural diagrams) and thus often produce assertion with                               modality (e.g., TEXT, TABLE, FORMULA, DIAGRAM) and
limited functional coverage.                                                                the semantic category (e.g., Architecture, Timing Behavior,
                                               Fig. 1: The Overview of AssertCoder Framework
Control Logic, Reset Behavior, Module Interface, etc.). The                 extracted from the PDF block
prompt includes structured input-output examples and explic-              • modality: one type of {TEXT, TABLE, FORMULA,
itly instructs the model to reason about signal semantics,                  DIAGRAM}, as inferred by the LLM
control logic, and structural content. An example of the full            • semantic_category: one of the predefined func-
prompt structure is shown in Listing 1.                                     tional categories (e.g., Timing Behavior, Control
SYSTEM ROLE
                                                                            Logic)
You are a hardware specification analyst with expertise in               • page_number: page index of the original block
signal semantics, interface conventions, and timing
                                                                         • bounding_box: physical location of the block on the
behavior. You are assisting in classifying document blocks
extracted from layout-aware parsers.                                        page
TASK DESCRIPTION
                                                                         • layout_hints: information from the parser (e.g., font
Given a structured content block from a hardware design
specification extracted using a layout-aware parser                         size, block type, section ID)
identify:
• The modality of the block: {TEXT,TABLE,FORMULA,DIAGRAM}                This format serves as a standardized, cross-modal input for-
• Assign a semantic category from the following(including              mat for information extraction. It ensures that semantic content
but not limited to):
   - Architecture      - Module/Interface Declaration                  and structural context are jointly preserved, enabling precise
   - Timing Behavior   - Details are omitted for brevity.              mapping of specification intent to formal representations in
• Reason step-by-step before giving your answer.Use both
the text content and any available layout hints (e.g.,                 subsequent stages.
block type, section title) to make your judgment.
INPUT EXAMPLE
"The module asserts ‘valid‘ for two cycles after ‘ready‘ is
                                                                       C. Multimodal Information Extraction
 high. ‘reset‘ overrides this behavior."                                  To support assertion synthesis from heterogeneous spec-
EXPECTED OUTPUT
Modality: TEXT
                                                                       ification, AssertCoder employs modality-sensitive analyzers
Semantic category: Timing Behavior                                     specialized for the modality and semantic category labels from
                                                                       preprocessing. Each analyzer employs a tailored prompting
      Listing 1: Prompt Template for SPEC Preprocessing Agent
                                                                       strategy to extract semantically relevant content. The results
  The output of the preprocessing stage is a unified inter-            are then transformed into structured representations that sup-
mediate representation that merges the structural information          port SVAs generation across module, signal, and temporal
with LLM-predicted semantic annotations. In the intermediate           contexts.
representation, each block is encapsulated in a structured                1) Text Analyzer: Textual content blocks labeled as Inter-
JSON-like object containing the following fields:                      face Declaration, Control Logic, or Configuration Info contain
   • content: the raw content (text, table, or formula)                essential semantic information about modules, ports, and their
behavioral descriptions. The text analyzer processes these          2. If the diagram is a waveform-based timing diagram:
                                                                        - Identify all signal transitions and timing
blocks using a structured prompt template that guides LLM               annotations
to extract relevant fields, such as signal names, I/O directions,       - Describe behavior in both:
                                                                            - Natural language
widths, and associated functionality. A representative prompt               - Temporal logic using bounded operators (F, G, X)
is shown in Listing 2.                                              EXAMPLE INPUT:
                                                                    Type: Timing Diagram
SYSTEM ROLE:
                                                                    Signal Transitions:
You are an expert digital hardware design analyst.
                                                                      - ien rise at cycle 44
TASK DESCRIPTION:
                                                                      - irq_flag rise at cycle 44, descend at cycle 51
You will be given a paragraph from hardware specifications.
                                                                    EXPECTED OUTPUT:
Your job is to extract structured design information using
                                                                    Natural language:
the following YAML schema:
                                                                      After ien is asserted, irq_flag becomes high within 1
---
                                                                      cycle and remains high for 6 cycles.
name: string
                                                                    Temporal logic:
description: string
                                                                      ien => F[0:1] irq_flag && G[0:5] irq_flag
ports:
                                                                    ---
  - name: string    - I/O directions: input | output | inout
                                                                    Type: FSM Diagram
  - width: int      - description: string
                                                                    States: IDLE, REQ, GRANT
implementation:
                                                                    Transitions:
  -reset: string    - accumulation: string
                                                                      - IDLE --(start)--> REQ
  -output_behavior: string
                                                                      - REQ --(ack)--> GRANT
  -counter_operation: string
                                                                    Pseudocode:
example_usage: string
                                                                      if (state == IDLE && start) then next_state = REQ;
notes:
                                                                      if (state == REQ && ack) then next_state = GRANT;
  - string
  - ...
module_interface: string                                                       Listing 3: Prompt Template for Diagram Analyzer
---
INSTRUCTIONS:
                                                                       3) Formula and Table Analyzers: AssertCoder also includes
- Use only the information present in the paragraph.                prompt-driven analyzers for handling formulas and tables that
- Do not invent missing fields; leave them blank or as
empty lists.
                                                                    appear in hardware specifications. The prompt template is
- Maintain accurate terminology and formatting.                     omitted here for brevity.
INPUT:
[Insert any paragraph describing a hardware module,                    The formula analyzer targets symbolic expressions and
interface, or subcomponent]                                         timing conditions presented in either natural language or
OUTPUT (example):
name: [module_name]                                                 mathematical notations. The extracted semantics are expressed
description: [...]                                                  in equations that preserve both syntactic and logical structure.
ports:
  - name: [...]     - direction: [...]                                 The table analyzer focuses on structured tabular data used
  - width: [...]    - description: [...]                            to specify interfaces, configuration registers, or operational
implementation:
  reset: [...]                                                      modes. With layout-informed segmentation and structured
  ...                                                               prompt template, each table is parsed into a structured JSON
            Listing 2: Prompt Template for Text Analyzer
                                                                    object. These representations are serialized into a JSON array
                                                                    format, which integrates seamlessly with other modality out-
   2) Diagram Analyzer: Another modality supported by As-           puts and facilitates unified processing in assertion generation.
sertCoder is graphical content, which is handled by a unified          4) Merging into a unified Specification: To support down-
diagram analyzer. This component interprets both structural         stream assertion generation, AssertCoder integrates the outputs
diagrams (FSMs, control/data flow) and timing diagrams by           from all four modality-sensitive analyzers into a unified rep-
first converting them into labeled diagram representations          resentation. For every signal or register, its relevant content is
using OCR techniques [25]. The semantic category identified         grouped together by aggregating information from multiple
during preprocessing determines which prompt-driven reason-         modalities, including structural descriptions from text and
ing module is used to process each diagram accordingly.             tables, behavioral logic from diagrams, and timing constraints
   Structural diagrams are mapped to control logic using            from formulas. The following example shows the merged
pseudocode-style interpretation, while timing diagrams are          specification of signal ack_out after multimodal analysis.
converted into natural language descriptions and formal tem-
                                                                    Signal: ack_out
poral constraints using operators (F, G, and X). This unified       ATTRIBUTES:
framework ensures consistent logic abstraction across visual        - Name: ack_out       - Width: 1
                                                                    - Direction: output - Default Value: 0
modalities and supports subsequent assertion synthesis. A rep-      - Category: control signal
resentative prompt used by this analyzer is shown in Listing 3.     BEHAVIORAL SEMANTICS:
                                                                    - Control Logic: state == READ && data_valid
SYSTEM ROLE:                                                        - FSM Transition: READ --(data_valid)--> SEND_ACK
You are a digital hardware logic interpreter.                       - Timing Constraint: ##[1:2] ack_out[*2]
TASK:                                                               - Temporal Logic: F[1:2] ack_out && G[0:1] ack_out
Given a diagram parsed into a graph (with nodes and edges),         - Natural Language:
 analyze its type and produce structured logic output.                "If data_valid is asserted during READ,
1. If the diagram is a structural (FSM or control flow)                then ack_out must be asserted within 2 cycles
diagram:                                                               and held for at least 1 cycle."
    - For each edge (source --(condition)--> destination),          TEMPORAL ROLES:
    output:                                                         - responder   - bounded-delay    - stabilizer
         if (state == source && condition) then next_state =        INTENT CANDIDATE TRIPLET:
          destination;                                              - Precondition: state == READ && data_valid
- Consequence: ack_out == 1                                         "timing": "between 2 and 4 cycles, and hold for >=2
- Timing: ##[1:2] ack_out[*2]                                       cycles"
SOURCE TRACEABILITY:                                                "mutation_points": [] // leave empty during initial
- Text Segment: Section 2.1                                         generation
- FSM Diagram: Figure 3                                           }
- Timing Waveform: Figure 5                                       EXPECTED OUTPUT:
- Formal Formula: Equation (2)                                    Step 1:
- Interface Table: Table 1                                        If (read_req && !arbiter_grant), then read_valid must
                                                                  become high within 2-4 cycles and stay high for >=2 cycles.
        Listing 4: Merged Semantic Specification for ack_out      Step 2:Pattern: Implication
                                                                  Step 3:Temporal: ##[2:4] read_valid[*2]
   This integrated format provides a complete and structured      Step 4:assert property (@(posedge clk)(read_req && !
                                                                  arbiter_grant) |-> ##[2:4]read_valid[*2]);
view of each design, making it available for the subsequent
assertion generation phase.                                                   Listing 5: Prompt Template for SVA Generator

D. SVA Generation                                                 E. Evaluation and Iteration
   Given the structured specification produced in the previ-         After the initial round of assertion generation, AssertCoder
ous stage, AssertCoder generates SVAs through a multi-step        evaluates the effectiveness of the SVA set through mutation
CoT prompting strategy, which systematically decomposes the       injection and model checking. Let A = {a1 , a2 , . . . , an } be
generation task into interpretable sub-steps. For signals of      the set of generated assertions and M = {m1 , m2 , . . . , mk }
each module, the LLM-guided process performs the following        the set of injected mutations. For each assertion-mutant pair
four steps: (1) Unified Semantic Decomposition, (2) Pattern       (ai , mj ), model checking is performed, and the outcome is
Selection, (3) Temporal Binding, and (4) SVA Syntax Syn-          logged as:
thesis. The details can be found in Listing5.                                                    (
   To perform the four-step method, AssertCoder employs a                                         1 if ai fails on mj
                                                                              detect(ai , mj ) =                               (1)
prompt template that guides each reasoning step, enabling                                         0 otherwise
interpretable generation and closer alignment with formal
                                                                    We define the mutation Score for each assertion ai as:
semantics. Domain knowledge is enhanced via a RAG tool
[26], which injects relevant passages from a curated corpus of                                   k
                                                                                                 X
SVA references and hardware design literature.                                    Score(ai ) =         detect(ai , mj )        (2)
   The generation interface also supports feedback from the                                      j=1

evaluation stage through undetected mutation points. While          This score represents the number of unique mutations that
the initial synthesis is performed without feedback, subsequent   ai is able to detect. Based on this metric, to further assess
iterations incorporate mutation-specific cues (mutation points)   the overall effectiveness of the assertion set, we compute the
using the same prompting structure to improve mutation            Average Mutation Score as:
detection.                                                                                                    n
                                                                                                          1X
SYSTEM ROLE:                                                                 Avg. Mutation Score =              Score(ai )     (3)
You are a hardware verification expert specialized in SVA                                                 n i=1
generation.
TASK DESCRIPTION:                                                    This metric reflects the average number of detected muta-
Given a structured specification segment for a signal (
including precondition, consequence, and timing window),          tions per assertion, capturing the aggregate detection strength
generate a valid SVA in four steps:                               of the generated set. Assertions with Score(ai ) = 0 are
[Optional]
If mutation detection feedback is available, consider the         deemed low-quality and automatically removed from the final
following uncovered mutation conditions to guide assertion        set. To evaluate overall detection, we define the Mutation
refinement:
- mutation_points: ["read_valid never asserted", "read_req        detection Rate (MDR):
never followed by output", ...]
Step 1 | Semantic Decomposition:                                                       |{mj | ∃ai : detect(ai , mj ) = 1}|
Extract the intent into three parts:                                        MDR =                                             (4)
- Precondition: When should this assertion be triggered?                                                k
- Consequence: What signal behavior must happen?
- Timing: Within what time window must it occur?
                                                                    If MDR<1, it implies that certain mutations remain unde-
Step 2 | Pattern Selection:                                       tected by all generated assertions. In such cases, the mutation
Choose the best matching assertion pattern:
- Implication (if A then B within N cycles)
                                                                  traces and logs serve as feedback to regeneration SVA. The
- Stability (signal must remain constant)                         failed mutations’ context (e.g., affected signal, location, or
- Invariant (property must always hold)
Step 3 | Temporal Binding:
                                                                  operation) is used to promote the LLM to produce more
Translate timing into SystemVerilog syntax, e.g., ##[2:4],        relevant assertions.
[*2], etc.
Step 4 | SVA Syntax Synthesis:
                                                                      By employing model checking, each assertion is re-
Assemble the final assertion using SystemVerilog syntax.          evaluated against the unmutated DUT to identify potential
Include clock edge and proper operators.
INPUT EXAMPLE:
                                                                  false positives. Assertions that are syntactically correct but
{                                                                 semantically misaligned with the specification, producing spu-
  "precondition": "read_req is high && arbiter_grant is low
  ",
                                                                  rious counterexamples on the original DUT, are labeled as
  "consequence": "read_valid must be high",                       false positives. Those that fail due to detecting actual DUT
                            TABLE II: ASSERTION GENERATION QUALITY COMPARISONS ACROSS THREE DESIGNS
     Design            Method       #SVAs Gen.   Syntax Correctness (%)     Functional Correctness (%)   Avg. Mutation Score    MDR (%)      FPR (%)
                      AssertCoder        92           90 (97.8%)                   81 (88.0%)                    0.63              84.3        3.2
     I2C              AssertLLM         89            86 (96.6%)                   73 (82.0%)                    0.59              79.8        5.6
                        GPT-4o          112           68 (60.7%)                   22 (19.6%)                    0.17              41.0        19.3
                      AssertCoder       134           132 (98.5%)                  118 (88.1%)                   0.61              87.2        2.8
     AES              AssertLLM         130           128 (98.5%)                  102 (78.5%)                   0.57              81.5        4.9
                        GPT-4o          141            74 (52.5%)                   28 (19.9%)                   0.16              38.5        21.1
                      AssertCoder       215           209 (97.2%)                  187 (86.9%)                   0.59              85.4        3.5
     Openmsp430       AssertLLM         210           205 (97.6%)                  165 (78.6%)                   0.54              78.1        6.1
                        GPT-4o          236           101 (42.8%)                   34 (14.4%)                   0.13              34.7        24.8
     Avg.             AssertCoder      147.0         143.7 (97.8%)                128.7 (87.6%)                  0.61              85.6        3.2
                      AssertLLM        143.0         139.7 (97.7%)                113.3 (79.2%)                  0.57              79.8        5.5
                        GPT-4o         163.0          81.0 (49.7%)                 28.0 (17.2%)                  0.15              38.1        21.7

flaws are not considered false positives and may even motivate
specification updates. We define the False Positive Rate (FPR)
as:
           |{ai ∈ Afinal | fail(ai , DUT) ∧ ¬semantically_corr(ai )}|
 FPR =                                                                    (5)
                                     |Afinal |

where:
   • Afinal denotes the final set of assertions after filtering and
     regeneration;
   • fail(ai , DUT) indicates assertion ai fails in model
     checking on the DUT;
   • semantically_corr(ai ) is true if ai aligns with                            Fig. 2: Effect of component ablations on functional correctness assertions.
     specification intent.
  Since assertion failures may indicate either flawed assertions
or actual DUT bugs, we perform a post-validation step that
manually checks failed assertions.
               IV. E XPERIMENTAL E VALUATION
A. Experimental Setup
   We evaluate AssertCoder on a suite of open-source hard-
ware designs of varying complexity, including an I2C master
[27] (small-scale), an AES core [28] (medium-scale), and
Openmsp430 [29] (large-scale). Each design is accompanied
by its multimodal specification document, containing natural
language descriptions, tables, and timing diagrams.
   The proposed method is compared against two approaches:                           Fig. 3: Impact on mutation detection rate (MDR) across designs.
(1) GPT-4o [30], used in a direct zero-shot prompting man-
ner, and (2) AssertLLM, a recent multi-agent prompting
                                                                                structural guidance, yielding a low mutation detection rate and
framework for assertion synthesis. We employ AssertLLM
                                                                                high false positive rate.
as the baseline method. All methods operate on identical
specification inputs. Our framework uses the GPT-4o API for                        The advantage of AssertCoder lies in its unified semantic
generation, SymbiYosys [31] for model checking, and Mantra                      decomposition and CoT reasoning pipeline, which enables
[32] for injecting mutations based on bug-derived mutation                      precise identification of assertion intent and timing constraints.
operators. Approximately 100–300 mutants are generated per                      Importantly, the low FPR indicates that the SVA generated
DUT.                                                                            by the AssertCoder framework has high quality. These results
                                                                                demonstrate the importance of structured prompting and mul-
B. Evaluation of Assertion Quality                                              timodal signal-level abstraction in SVA generation.
   To assess assertions quality, we analyze the outputs of
AssertCoder, AssertLLM, and GPT-4o on three DUTs using                          C. Ablation Study
a set of standard metrics. Table II summarizes the results.                       To understand the contribution of each core component in
   Across all designs, AssertCoder achieves the highest asser-                  the AssertCoder pipeline, we conduct an ablation study by
tion quality. It maintains a very high accuracy rate in both syn-               incrementally disabling three major modules: (1) RAG, (2)
tax correctness and functional correctness, and generates more                  CoT prompting , and (3) mutation-guided iterative refinement.
effective assertions. While AssertLLM demonstrates strong                       We measure the impact on both the number of functional
effectiveness, it occasionally produces semantically weak as-                   correctness assertions and the MDR across all three DUTs.
sertions due to insufficient temporal grounding. In contrast,                     As shown in Figure 2, removing CoT prompting leads to
GPT-4o struggles to produce useful SVAs in the absence of                       the largest decrease in correctness SVA count, highlighting
its importance in guiding multi-step reasoning and ensuring                     [13] K. Chang, Z. Chen, Y. Zhou, W. Zhu, K. Wang, H. Xu, C. Li, M. Wang,
signal-condition alignment. Removing RAG has comparatively                           S. Liang, H. Li et al., “Natural language is not enough: Benchmarking
                                                                                     multi-modal generative ai for verilog generation,” in Proceedings of the
minimal impact, indicating that most assertion-relevant seman-                       43rd IEEE/ACM International Conference on Computer-Aided Design,
tics are already encoded within the specification. However,                          2024, pp. 1–9.
without iterative refinement, the system produces fewer high-                   [14] Z. Yan, W. Fang, M. Li, M. Li, S. Liu, Z. Xie, and H. Zhang, “Assertllm:
                                                                                     Generating hardware verification assertions from design specifications
impact assertions and achieves a lower MDR.                                          via multi-llms,” in Proceedings of the 30th Asia and South Pacific Design
   Figure 3 further confirms that iterative assertion synthesis is                   Automation Conference, 2025, pp. 614–621.
critical for maximizing mutation detection, as its removal leads                [15] B. Mali, K. Maddala, V. Gupta, S. Reddy, C. Karfa, and R. Karri,
                                                                                     “Chiraag: Chatgpt informed rapid and automated assertion generation,”
to substantial detection drops across all DUTs. These results                        in 2024 IEEE Computer Society Annual Symposium on VLSI (ISVLSI).
confirm that all three components contribute to AssertCoder’s                        IEEE, 2024, pp. 680–683.
effectiveness, with CoT enabling correctness and iteration                      [16] C. Sun, C. Hahn, and C. Trippel, “Towards improving verification pro-
                                                                                     ductivity with circuit-aware translation of natural language to systemver-
ensuring completeness.                                                               ilog assertions,” in First International Workshop on Deep Learning-aided
                                                                                     Verification, 2023.
                           V. C ONCLUSION                                       [17] R. Kande, H. Pearce, B. Tan, B. Dolan-Gavitt, S. Thakur, R. Karri, and
                                                                                     J. Rajendran, “(security) assertions by large language models,” IEEE
   In this work, we introduced AssertCoder, a unified frame-                         Transactions on Information Forensics and Security, 2024.
                                                                                [18] Y. Bai, G. B. Hamad, S. Suhaib, and H. Ren, “Assertionforge: Enhancing
work for automatic SVA generation from multimodal hard-                              formal verification assertion generation with structured representation of
ware specifications. By integrating modality-sensitive semantic                      specifications and rtl,” arXiv preprint arXiv:2503.19174, 2025.
extraction, a structured multi-step Chain-of-Thought prompt-                    [19] F. Wu, E. Pan, R. Kande, M. Quinn, A. Tyagi, D. K. Houngninou,
                                                                                     J. Rajendran, and J. Hu, “Spec2assertion: Automatic pre-rtl assertion
ing strategy, and mutation-guided iterative refinement, As-                          generation using large language models with progressive regularization,”
sertCoder significantly improves the quality of assertion-                           arXiv preprint arXiv:2505.07995, 2025.
based verification. Experimental evaluations demonstrated that                  [20] V. Pulavarthi, D. Nandal, S. Dan, and D. Pal, “Are llms ready for
                                                                                     practical adoption for assertion generation?” in 2025 Design, Automation
AssertCoder outperforms existing methods, achieving higher                           & Test in Europe Conference (DATE). IEEE, 2025, pp. 1–7.
functional correctness and mutation detection.                                  [21] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,
                                                                                     D. Zhou et al., “Chain-of-thought prompting elicits reasoning in large
                                                                                     language models,” Advances in neural information processing systems,
                             R EFERENCES                                             vol. 35, pp. 24 824–24 837, 2022.
                                                                                [22] E. M. Clarke, “Model checking,” in Foundations of Software Technology
 [1] J. Bergeron, Writing testbenches using SystemVerilog. Springer Science          and Theoretical Computer Science: 17th Conference Kharagpur, India,
     & Business Media, 2007.                                                         December 18–20, 1997 Proceedings 17. Springer, 1997, pp. 54–56.
 [2] H. Witharana, Y. Lyu, S. Charles, and P. Mishra, “A survey on assertion-   [23] Z. Shen, R. Zhang, M. Dell, B. C. G. Lee, J. Carlson, and W. Li,
     based hardware verification,” ACM Computing Surveys (CSUR), vol. 54,            “Layoutparser: A unified toolkit for deep learning based document
     no. 11s, pp. 1–33, 2022.                                                        image analysis,” in Document Analysis and Recognition–ICDAR 2021:
 [3] M. Orenes-Vera, A. Manocha, D. Wentzlaff, and M. Martonosi, “Au-                16th International Conference, Lausanne, Switzerland, September 5–10,
     tosva: Democratizing formal verification of rtl module interactions,”           2021, Proceedings, Part I 16. Springer, 2021, pp. 131–146.
     in Proceedings of the 58th ACM/IEEE Design Automation Conference           [24] X. Zhong, J. Tang, and A. J. Yepes, “Publaynet: largest dataset ever
     (DAC). IEEE, 2021, pp. 535–540.                                                 for document layout analysis,” in 2019 International conference on
 [4] W. Fang, G. Hu, and H. Zhang, “r-map: Relating implementation and               document analysis and recognition (ICDAR). IEEE, 2019, pp. 1015–
     specification in hardware refinement checking,” IEEE Transactions on            1022.
     Computer-Aided Design of Integrated Circuits and Systems, 2023.            [25] J. Memon, M. Sami, R. A. Khan, and M. Uddin, “Handwritten opti-
 [5] A. Danese, N. D. Riva, and G. Pravadelli, “A-team: Automatic template-          cal character recognition (ocr): A comprehensive systematic literature
     based assertion miner,” in Proceedings of the 54th Annual Design                review (slr),” IEEE access, vol. 8, pp. 142 642–142 668, 2020.
     Automation Conference (DAC), 2017, pp. 1–6.                                [26] Z. Guo, L. Xia, Y. Yu, T. Ao, and C. Huang, “Lightrag: Simple
 [6] S. Germiniani and G. Pravadelli, “Harm: a hint-based assertion miner,”          and fast retrieval-augmented generation,” 2025. [Online]. Available:
     IEEE Transactions on Computer-Aided Design of Integrated Circuits               https://arxiv.org/abs/2410.05779
     and Systems, vol. 41, no. 11, pp. 4277–4288, 2022.                         [27] R. Herveille, “I2c-master core specification,” svn://opencores.
 [7] S. Vasudevan, D. Sheridan, S. Patel, D. Tcheng, B. Tuohy, and D. John-          org/ocsvn/i2c@ r76, OpenCores, 2003.
     son, “Goldmine: Automatic assertion generation using data mining           [28] H. Hsing, “Aes core specification,” OpenCores, 2013.
     and static analysis,” in 2010 Design, Automation & Test in Europe          [29] O. Girard, “openmsp430,” URL: http://opencores.org, 2009.
     Conference & Exhibition (DATE). IEEE, 2010, pp. 626–629.                   [30] OpenAI, “GPT-4 Technical Report,” https://openai.com/research/gpt-4,
 [8] F. Aditi and M. S. Hsiao, “Hybrid rule-based and machine learning               Mar. 2024, accessed: Jul. 2025.
     system for assertion generation from natural language specifications,”     [31] C. Wolf, “Yosys open synthesis suite,” 2016.
     in 2022 IEEE 31st Asian Test Symposium (ATS). IEEE, 2022, pp.              [32] J. Wu, Y. Lei, Z. Zhang, X. Meng, D. Yang, P. Li, J. He, and X. Mao,
     126–131.                                                                        “Mantra: Mutation testing of hardware design code based on real bugs,”
 [9] S. J. Frederiksen, J. Aromando, and M. S. Hsiao, “Automated assertion           in 2023 60th ACM/IEEE Design Automation Conference (DAC). IEEE,
     generation from natural language specifications,” in 2020 IEEE Interna-         2023, pp. 1–6.
     tional Test Conference (ITC). IEEE, 2020, pp. 1–5.
[10] C. B. Harris and I. G. Harris, “Glast: Learning formal grammars to
     translate natural language specifications into hardware assertions,” in
     2016 Design, Automation & Test in Europe Conference & Exhibition
     (DATE). IEEE, 2016, pp. 966–971.
[11] O. Keszocze and I. G. Harris, “Chatbot-based assertion generation from
     natural language specifications,” in 2019 Forum for Specification and
     Design Languages (FDL). IEEE, 2019, pp. 1–6.
[12] G. Parthasarathy, S. Nanda, P. Choudhary, and P. Patil, “Spectosva:
     Circuit specification document to systemverilog assertion translation,”
     in 2021 Second Document Intelligence Workshop at KDD, 2021, n.d.
