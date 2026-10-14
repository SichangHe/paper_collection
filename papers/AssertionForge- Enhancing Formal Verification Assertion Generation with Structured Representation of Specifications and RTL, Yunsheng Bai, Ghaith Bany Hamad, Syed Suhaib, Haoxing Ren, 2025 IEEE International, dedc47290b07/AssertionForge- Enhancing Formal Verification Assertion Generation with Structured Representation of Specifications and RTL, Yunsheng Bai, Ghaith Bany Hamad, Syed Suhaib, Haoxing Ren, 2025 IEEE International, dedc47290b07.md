                                                AssertionForge: Enhancing Formal Verification
                                                    Assertion Generation with Structured
                                                  Representation of Specifications and RTL
                                                                   Yunsheng Bai, Ghaith Bany Hamad, Syed Suhaib, Haoxing Ren
                                                                                            NVIDIA
                                                                yunshengb, gbanyhamad, ssuhaib, haoxingr@nvidia.com
arXiv:2503.19174v2 [cs.AI] 14 May 2025




                                            Abstract—Generating SystemVerilog Assertions (SVAs) from            SVA generation task into phases, using customized LLMs to
                                         natural language specifications remains a major challenge in           extract structural specifications, map signal definitions, and
                                         formal verification (FV) due to the inherent ambiguity and incom-      generate assertions by prompting the LLM with contextual
                                         pleteness of specifications. Existing LLM-based approaches, such
                                         as A SSERT LLM, focus on extracting information solely from            information from specifications about relevant signals. These
                                         specification documents, often failing to capture essential internal   approaches demonstrate the feasibility of using LLMs for
                                         signal interactions and design details present in the RTL code,        generating SVAs, but they remain fundamentally limited in
                                         leading to incomplete or incorrect assertions. We propose a novel      their ability to capture the full design context.
                                         approach that constructs a Knowledge Graph (KG) from both                 The limitations stem from their approach to utilizing sources
                                         specifications and RTL, using a hardware-specific schema with
                                         domain-specific entity and relation types. We create an initial        of verification information. Specification-focused approaches
                                         KG from the specification and then systematically fuse it with         like A SSERT LLM extract design intent from the often ambigu-
                                         information extracted from the RTL code, resulting in a unified,       ous and incomplete specifications [3], [16], [19], [21], [52],
                                         comprehensive KG. This combined representation enables a more          and thus miss crucial implementation details found exclusively
                                         thorough understanding of the design and allows for a multi-           in the RTL, leading to plausible but functionally incorrect
                                         resolution context synthesis process which is designed to extract
                                         diverse verification contexts from the KG. Experiments on five         assertions. Conversely, RTL-focused approaches can capture
                                         designs demonstrate that our method significantly enhances SVA         implementation details but lack understanding of original
                                         quality over prior methods. This structured representation not         design intent and high-level functionality, producing assertions
                                         only improves FV but also paves the way for future research in         that verify implementation without validating adherence to
                                         tasks like code generation and design understanding.                   specifications.
                                            Index Terms—Formal Verification, Large Language Model,
                                         SystemVerilog Assertion, Knowledge Graph                                  We hypothesize that explicitly constructing a structured,
                                                                                                                interconnected mental model of the design—one that links
                                                                                                                design intent with RTL behavior—will provide a more ro-
                                                                I. I NTRODUCTION
                                                                                                                bust foundation for assertion generation. This mirrors how
                                            Formal Verification (FV) is a critical process in the VLSI de-      verification engineers manually synthesize information from
                                         sign flow, ensuring that increasingly complex hardware designs         multiple sources to write meaningful assertions. Compared
                                         conform to their specifications [11]. Among FV techniques,             to unstructured retrieval-based approaches [18], [33]. such
                                         Assertion-Based Verification (ABV) uses SystemVerilog As-              a mental model enables more precise tracing of intent to
                                         sertions (SVAs), which are formal properties that describe             implementation and facilitates deeper reasoning, allowing the
                                         expected design behavior, to verify functional correctness [58].       LLM to identify signal dependencies and complex interactions.
                                         To be effective, these assertions must encapsulate both the            However, building such a model is challenging, requiring
                                         high-level design intent, as described (often ambiguously)             structured knowledge extraction from specifications, analysis
                                         in natural language specifications [19], and the low-level             of RTL control flows, and alignment between abstract require-
                                         implementation details codified in Register-Transfer Level             ments and implementation details.
                                         (RTL) code. Verification engineers traditionally bridge this              In this paper, we present A SSERTION F ORGE, a novel ap-
                                         gap by mentally synthesizing information from both sources, a          proach that constructs a unified Knowledge Graph (KG) from
                                         process that is difficult to automate yet essential for producing      specifications and RTL, thereby actively “forging” assertions
                                         high-quality SVAs—assertions that are syntactically correct,           by bridging the semantic gap between high-level specifications
                                         functionally accurate, and provide comprehensive coverage of           and RTL implementation, enabling discovery of complex
                                         critical design properties.                                            multi-signal interactions often obscured in linear text. The
                                            Recently, Large Language Models (LLMs) have shown                   KG is built in two stages: entity-relation extraction from the
                                         promise in generating SVAs from natural language specifica-            specification via an LLM and structural parsing of RTL via a
                                         tions, thanks to their advanced text comprehension and coding          Verilog parser.
                                         capabilities. Methods like A SSERT LLM [18] decompose the                 With the unified KG constructed, the next step is crafting
effective prompts for LLMs to generate high-quality test           [60] by improving knowledge-grounded responses and contex-
plans and SVAs. We propose a multi-resolution context              tual understanding. Our approach adapts these advancements
synthesis process that progressively narrows focus from broad      to hardware verification by integrating specifications and RTL
design overviews to fine-grained signal interactions: (1) LLM-     code into a knowledge-rich graph.
based global summarization provides a high-level view of the
specification and RTL; (2) Signal-specific retriever extracts                           III. M ETHODOLOGY
relevant snippets from the specification and RTL; (3) Guided         In this section, we introduce our novel approach, A S -
Random Walk with Adaptive Sampling (GRW-AS) explores               SERTION F ORGE (Figure 1), for generating high-quality Sys-
the KG, tracing structured paths that connect the target signal    temVerilog Assertions (SVAs) from both natural language
to critical design elements. To ensure concise yet informative     specifications and RTL code.
prompts, an LLM-based pruning mechanism filters and refines
the retrieved text and graph-derived paths, balancing diversity    A. Problem Setup and Overview of A SSERTION F ORGE
and relevance before guiding final SVA generation.                    We formalize the problem as follows: Given a hardware de-
   Our contributions are summarized as follows:                    sign specification S and RTL code R, we generate SystemVer-
   • We propose a novel KG-based approach, A SSERTION -            ilog Assertions A = {A1 , . . . , An } evaluated for syntactic
     F ORGE, that integrates information from both natural         correctness and functional accuracy. To emulate verification
     language specifications and RTL code into a unified           engineers’ cognitive process [19] — a workflow rooted in cog-
     structured representation for SVA generation.                 nitive science’s concept of mental model (internal representa-
   • We develop a multi-resolution context synthesis process,      tions humans construct to understand complex systems [26])
     which constructs verification-critical prompts by provid-     — we develop a computational approach integrating S (design
     ing context as global summaries, signal-specific snippets,    intent) and R (implementation details).
     and structured paths from the KG.                                To computationally realize this mental model, we construct
   • We demonstrate that our method significantly enhances         a Knowledge Graph (KG), G = (V, E), where V represents
     SVA quality through experiments on five designs, achiev-      nodes (entities) and E represents edges (relationships). Entities
     ing superior results compared to existing LLM-based           V are derived from both S and R, and edges E capture re-
     methods.                                                      lationships defined by our domain-specific schema. Formally,
                                                                   G = F(S, R), where F is the KG generation function. In
                     II. R ELATED W ORK                            our approach, the complete mental model comprises both
                                                                   this structured KG representation alongside the raw specifi-
A. Formal Verification and SVA Generation
                                                                   cation and RTL texts, enabling context-aware SVA generation
   LLM-based approaches for SystemVerilog Assertion (SVA)          through dynamically constructed LLM prompts.
generation have gained traction [2], [4], [28], [29], [31],
[36]–[38], [44], [47], with A SSERT LLM [18] automating            B. Knowledge Graph Construction with GraphRAG
assertion extraction from specifications. Non-LLM methods             GraphRAG [17] is a framework for generating knowledge
include GOLDMINE [57], HARM [20], A-Team [15], and                 graphs from textual documents through a process of chunking
AutoSVA [43], which use data mining, static analysis, tem-         source text, LLM-based extraction of entities and relation-
plates, etc. for assertion generation. However, these approaches   ships, summarization of node/edge descriptions, and graph
often struggle with complex specifications, suffer from limited    assembly. While GraphRAG’s default extraction focuses on
coverage, or depend heavily on simulation stimuli quality. Re-     general-purpose entities, hardware verification demands spe-
cent RTL-guided SVA works include [27] and [54]. Our work          cialized entity and relationship types.
focuses on advancing LLM-based SVA generation, exploring              We propose an effective procedure to customize GraphRAG
how structured representation and context-aware prompting          for hardware verification. First, we leverage automated LLM-
can improve assertion quality.                                     based schema discovery by presenting a small representative
                                                                   set of hardware specification excerpts to the LLM, prompting
B. LLM for Knowledge Graph Construction and Understand-            it to identify domain-specific entity types (e.g., “registers”,
ing                                                                “clocks”) and relation types (e.g., “triggers”, “connects to”).
   Traditional methods for Knowledge Graph (KG) [1], [25]          This is followed by schema review, where we manually refine
construction rely on non-LLM approaches requiring manual           the LLM-generated schema by merging redundant or overlap-
effort and domain-specific ontologies [9], [39], [62], [63].       ping concepts (e.g., combining “Reset Signal” and “Reset”).
Recent advancements leverage LLMs for KG construction,             Finally, through prompt update and indexing, we modify
automatically inferring entities and relationships [7], [45],      only GraphRAG’s entity extraction prompt to incorporate our
[56], [64]. LLM-based graphs and KGs have gained popu-             hardware-specific schema while keeping all other GraphRAG
larity across domains [30], [46], with Microsoft’s GraphRAG        indexing components unchanged.
demonstrating their application in question answering [17].           The schema Σ is formally defined as a tuple (Et , Rt )
KGs enhance LLM-based NLP tasks including question an-             consisting of entity types Et representing key hardware design
swering, dialogue systems, and reasoning [35], [49], [53], [59],   components (e.g., “design specification”, “module”, “signal”,
                                                                                       Global
                                                                                    Summarization        Design Overview                                                          Design Overview:
                                                                                                                                                                   Prompt                                          Test
                                                                                                                 …                                                                …                                Plan
                                                                                                       All Signals Summary:                                      Construction
                                                                                                                 …
                                                                                                                                        RAG Context from spec:                    All Signals Summary:
                                                                                                                                 pwrite should be low. And
                                                                                                                                 lastly writing logger                            …
                                                                                                                                 conﬁguration in which PADDR
                                                                                                                                                                                  Relevant Context:
                            …                                                                                                    should be set at 8h and
                                                                                                                                 pwrite
                                                                                                                                               ...
                                                                                                                                                                                  Contexts relevant to
                                                                                                                                                                                  signal 'PADDR’:
                Design Specification                                                Signal-Specific                                                                               RAG Context:
                                                                                                            RAG                        RAG Context from RTL:
                                                                                    Retrieval (SSR)        Context
                                                                                                                                 assign PRDATA = (PADDR ==
                                                                                                                                                                                  …
                                                                                                                                 32'd4)?
                                                                                                                                 READ_DATA_ON_RX:READ_DATA_ON                     GUIDED_RANDOM_
                                                     + RTL Parser                                                     RAG        _RX;
                                                                                                                     Context                  ...                                 WALK Context:
                                                                                                                                                                   Context        …
           module apb(...);                                                                                                                                                                                       SVA
           ...
           always@(posedge PCLK)
                                                                                                                                                                   Pruner         FINAL
           begin
               if(!PRESETn)                                                         Guided Random                                                                                 INSTRUCTIONS AND
               begin                                                                                                                                                              REMINDER:
                   INTERNAL_I2C_REGISTER_CONFIG <=                                     Walk with       Path Context
           14'd0;                                                                                                                                                                 …
                   INTERNAL_I2C_REGISTER_TIMEOUT                                   Adaptive Sampling                                                               Filters out
           <= 14'd0;
           …
                                                             A Unified Knowledge      (GRW-AS)                 Path Context                                      redundant/low-
                   end
               end
                                                                 Graph (KG)                                                                                          quality       Example Prompt
           end
           endmodule                                                                                                                                                contexts                     Verifier (e.g. Jasper)
                                                                                   Multi-Resolution
                                                     Mental Model                                       Candidate Contexts (for a target signal)
                          RTL                                                      Context Synthesis                                                                                      Repeat for all target signals

Fig. 1. Overview of A SSERTION F ORGE. Our method is structured into a three-stage process: First, we construct a domain-specific Knowledge Graph (KG)
that captures the essential entities and relationships in the design. Together with the raw specifications and RTL, we build a mental model for the design
under verification. Second, we generate three types of candidate contexts for each signal. Lastly, we use these contexts to dynamically construct prompts for
a Large Language Model (LLM) to generate accurate SVAs.

“port”, “register”, “clock”) and relation types Rt representing                                                (RAG) [18], [33]. While RAG can effectively retrieve doc-
relationships (e.g., “hasSection”, “contains”, “defines”, “con-                                                umentation snippets and code fragments using signal names
nectsTo”, “operatesAt”).                                                                                       as queries, the retrieved context often contains noise, and
   Our customized entity extraction prompt ensures that nodes                                                  important behavioral patterns may be scattered across multiple
and edges in G0 contain detailed attributes such as type,                                                      documents and not captured in a single retrieval.
description, source ID, and relationships. Node attributes                                                        To address these challenges, we propose a dynamic context
include fields like entity type, description, level, and degree,                                               synthesis framework that unifies multiple context genera-
while edge attributes capture weight, description, and source                                                  tors with an intelligent LLM-based pruning mechanism. Our
IDs of connected nodes. These attributes are crucial for                                                       framework consists of a suite of context generators where
accurately representing both high-level and low-level design                                                   each generator leverages distinct heuristics to capture different
aspects. We will publicly release the exact prompt used                                                        aspects of the design:
for entity extraction and our entire source code to enable                                                       (i) Global Summarization: (broadest level) An LLM-based
reproducibility.                                                                                                     summarizer extracts high-level design intent from spec-
C. Refinement with RTL Information                                                                                   ifications and RTL, forming a cohesive system-level
                                                                                                                     overview.
   To enhance the completeness and accuracy of the KG, we
                                                                                                                (ii) Signal-Specific Retrieval (SSR): Given a target archi-
further refine G0 using information extracted from the RTL
                                                                                                                     tectural signal, a RAG-based retriever extracts localized,
code R. We utilize a specialized Verilog parser based on
                                                                                                                     functionally relevant snippets from the specification and
[55] to extract detailed information from RTL design files,
                                                                                                                     RTL, ensuring precise contextual grounding.
including modules, ports, signals, control flow structures, and
                                                                                                               (iii) Guided Random Walk with Adaptive Sampling
signal assignments. This process, denoted as G = ψ(G0 , R),
                                                                                                                     (GRW-AS): Given a node in the KG corresponding to
analyzes Verilog files to augment the initial KG with RTL-
                                                                                                                     a target signal, a novel graph-based traversal algorithm
specific elements. New nodes are added for internal signals,
                                                                                                                     (detailed in Section III-E) explores the KG, generating
control flow constructs, and module instances, while existing
                                                                                                                     paths that connect the target signal to other key design
nodes are enriched with attributes like signal width and type
                                                                                                                     elements.
information. Edges represent both structural relationships (e.g.,
                                                                                                                  Since naively combining all contexts would overwhelm
“has port”) and behavioral relationships (e.g., “assigns to”).
                                                                                                               downstream processing, we introduce an LLM-as-Pruner. This
Our analysis also identifies finite state machines by recogniz-
                                                                                                               pruner evaluates each candidate context generated by SSR and
ing clocked always blocks with case statements, creating FSM
                                                                                                               GRW-AS — evaluating relevance, diversity, and verification
nodes that capture state transition logic.
   Correspondences between specification and RTL nodes are                                                     potential — and filters out redundant or low-quality contexts.
identified via string matching of signal and module names. We                                                  The pruner considers both the individual merit of each con-
use exact matching for direct references and a fuzzy matching                                                  text and its complementarity with other selected contexts to
algorithm to handle minor variations in naming conventions.                                                    ensure comprehensive coverage of verification properties. Due
This linking process establishes traceability between require-                                                 to space constraints, we omit the full LLM-pruner prompt;
ments and implementation.                                                                                      however, it will be released upon paper acceptance.
                                                                                                                  The pruned contexts are then packed into dynamic
D. Multi-Resolution Context Synthesis for SVA Generation                                                       prompts—up to the maximum token limit—to provide the
   Current approaches to LLM-based hardware verifica-                                                          LLM with comprehensive yet focused information. This en-
tion predominantly rely on Retrieval-Augmented Generation                                                      sures that the LLM does not just process more data, but pro-
                                                                                                                      (
cesses better-selected data. By dynamically adapting context                                                             1.0 if c ∈/ visited
                                                                                          Quantified as N (c) =                              , where
selection based on verification needs, our approach enables                                                              0.0 otherwise
the LLM to generate test plans and SystemVerilog Assertions                                visited is the set of already visited nodes in the current
(SVAs) that capture complex behavioral patterns that are                                   walk, which is dynamically updated during each walk,
missed by traditional RAG-only methods.                                                    making the sampling adaptive.
   Following A SSERT LLM, we define architectural signals as                            These factors are combined to compute transition probabil-
input/output ports and architectural-level registers explicitly                      ities at each step according to the formula: P (c) = α · I(c) +
mentioned in the specification, excluding internal signals fur-                      β · D(c) + γ · N (c) where α, β, and γ are configurable weights
ther implemented in RTL. For each architectural signal, we                           controlling the influence of each factor. The probabilities are
construct a dedicated prompt by combining the global sum-                            normalized to sum to 1 before node selection. Walks terminate
maries with the LLM-pruned contexts from SSR and GRW-                                either upon reaching another architectural signal or exceeding
AS. These contexts are packed across multiple prompts, each                          a predefined step budget.
varying in content but constrained by the LLM’s maximum
token limit, ensuring diverse yet focused verification inputs.                                            IV. E XPERIMENTS
Each enriched prompt is then used to generate natural language                         We evaluate our approach, A SSERTION F ORGE, on five
(NL) test plans and actual SystemVerilog Assertions (SVAs).                          designs. All of the datasets and model implementation will
The generated test plans and SVAs for all architectural signals                      be released upon paper acceptance.
are combined for final evaluation.
                                                                                     A. Dataset and Knowledge Graph Statistics
E. Guided Random Walk with Adaptive Sampling (GRW-AS)                                   We evaluate our approach on five diverse hardware designs.
   To efficiently explore the KG’s structural and behavioral                         These designs represent a range of complexities and function-
relationships, we introduce the Guided Random Walk with                              alities in hardware systems, from communication protocols to
Adaptive Sampling (GRW-AS) algorithm. Inspired by biased                             microcontrollers and cryptographic modules. For each design,
random walk techniques [61] used in recommendation sys-                              our focus is on generating SVAs for a specific module within
tems [12], knowledge discovery [5], network analysis [13],                           the design. Since Verilog allows modules to reference or
and graph representation learning [22], [23], GRW-AS per-                            import other modules, we consider the total number of RTL
forms targeted exploration of the design, prioritizing paths                         files associated with each design, as shown in Table I.
likely to be relevant for verification. Starting from the target                     B. Baselines and Implementation Details
architectural signal’s corresponding node, GRW-AS performs
                                                                                        For all methods, we use GPT-4o [40] as the LLM backend.
multiple, guided random walks through the KG. Each walk is
                                                                                     KG construction follows the GraphRAG framework [17] with
biased by a combination of:
                                                                                     default settings, customizing only the prompt for entity and
  (i) Local Node Importance: Prioritizing structurally signif-                       relation extraction. RTL parsing utilizes ‘pyverilog’ [55]. For
      icant nodes (e.g., modules, key registers), thus guiding                       SSR, we adopt a multi-scale hierarchical chunking strategy
      the walk toward verification-critical regions of the KG.                       following [8], [33], with chunk sizes of 50, 100, 200, 800,
      The importance score is computed as I(n) = 0.4 ·                               and 3200 tokens and overlap ratios of 0.2 and 0.4. We retrieve
          deg(n)
      max degree + 0.6 · T (n), where deg(n) is the degree of                        the top 20 ranked chunks per signal-name query using a
      node n, max degree is the maximum degree of any                                hybrid similarity model combining TF-IDF [51] and Sentence
      node in the KG, and T (n) represents a mapping from                            Transformers [48]. The GRW-AS algorithm runs 70 walks per
      a node type to its semantic significance which can be                          signal with a budget of 100 steps, using α = 0.3, β = 0.5,
      manually adjusted using domain knowledge of the design                         and γ = 0.2. The LLM-based pruner retains a maximum of
      under verification. In our current implementation, we use                      50 contexts per type and 100 in total.
      a uniform weight for all nodes.                                                   To ensure a fair comparison and simulate a realistic ver-
 (ii) Directional Guidance: Favoring paths that lead towards                         ification scenario, we limit each method to a maximum of
      other known architectural signals. In the initialization                       3 prompts per architectural signal. Global summaries and
      phase, we compute shortest paths between all pairs of                          pruned contexts from SSR and GRW-AS are grouped by
      architectural signals and store the “next hop” for each                        type, and then distributed across these prompts, maximizing
      signal-to-signal path. For a candidate node c during                           context inclusion while respecting the GPT-4o’s token limit
      P walk, the direction score is calculated as D(c) =
      the                                                                            per prompt.
         t∈architectural signals I(c is next hop to t)
                  |architectural signals|              , where the indicator func-      We compare A SSERTION F ORGE against three baselines: (1)
      tion equals 1 if c is the first node along the shortest path                   A SSERT LLM [18]: An LLM-based approach that generates
      from the current node to target architectural signal t. This                   SVAs directly from natural language specifications without
      effectively biases the walk towards nodes that serve as                        constructing a KG. (2) A SSERTION F ORGE W / O RTL: This
      “stepping stones” to reach other architectural signals.                        baseline is similar to our full A SSERTION F ORGE, but it
(iii) Exploration novelty: Encouraging exploration of less-                          does not perform RTL refinement, relying solely on the
      visited areas of the graph by prioritizing unvisited nodes.                    initial KG G0 constructed from the design specification. (3)
                                                             TABLE I
OVERVIEW OF THE HARDWARE DESIGNS AND K NOWLEDGE G RAPH STATISTICS USED IN OUR EVALUATION . T OKEN COUNTS ARE OBTAINED USING THE
                      CL 100 K BASE TOKENIZER [41]. T IME REFERS TO THE KG CONSTRUCTION TIME IN MINUTES .

 Design          Source             Description            Spec Pages     Spec Tokens     RTL Files    RTL Tokens   # Nodes   # Edges   Time
 APB              [42]          APB to I2C interface           12            2,634           1            1,116        128      225     4.25
 ETHMAC           [42]     Ethernet MAC transmit control      102           33,754           4            6,262       1332     2502     8.10
 OPEN MSP430      [18]        MSP430 microcontroller          129           34,133           29         116,093       4636     5800     6.67
 SOCKIT           [18]       FPGA-based 1-wire master          29           13,102           4           11,547        678     1400     4.41
 UART             [18]         UART to Bus interface           10            3,103           6            9,235       1490     1815     1.60


                                                                TABLE II
     E VALUATION RESULTS . (#SVA: TOTAL ASSERTIONS GENERATED ; #S YN C: SYNTACTICALLY CORRECT; #P ROVEN : PROVEN OR PASSING ; COI
                 S TATEMENT /B RANCH /F UNCTIONAL /T OGGLE : COVERAGE METRICS FOR EACH COVERAGE MODEL UNDER COI.)

                                                                                              COI Coverage (%)
                   Model                           #SVA    #SynC    #Proven
                                                                                 Statement    Branch   Functional   Toggle
                                                                    APB
                   A SSERT LLM                      221      170        56        100.00       86.67       84.79     84.16
                   A SSERTION F ORGE W / O RTL      188      128        22        100.00       86.67       70.05     68.32
                   A SSERTION F ORGE O RIG KG       551      412        92        100.00      100.00      100.00    100.00
                   A SSERTION F ORGE                615      549        220       100.00      100.00      100.00    100.00
                                                                   ETHMAC
                   A SSERT LLM                      520      106       15          45.10       44.83      49.01     50.29
                   A SSERTION F ORGE W / O RTL     1345      331       42          50.98       51.72      71.21     77.46
                   A SSERTION F ORGE O RIG KG      1365      428       74          94.12       93.10      77.80     72.83
                   A SSERTION F ORGE               1673      960      208         100.00      100.00      99.12     98.84
                                                                OPEN MSP430
                   A SSERT LLM                      409      128       55          94.70       95.05      87.32     85.81
                   A SSERTION F ORGE W / O RTL     1123      216      106          99.08       98.91      88.94     86.95
                   A SSERTION F ORGE O RIG KG      1202      323      153          99.54       99.52      89.87     87.96
                   A SSERTION F ORGE               1600      698      327         100.00       99.76      90.09     88.16
                                                                   SOCKIT
                   A SSERT LLM                      118       49        13         85.71       82.35      88.54     90.46
                   A SSERTION F ORGE W / O RTL      393      131        41        100.00      100.00      99.33     99.08
                   A SSERTION F ORGE O RIG KG       429      156        32        100.00      100.00      99.78     99.69
                   A SSERTION F ORGE                448      136        49        100.00      100.00      99.78     99.69
                                                                    UART
                   A SSERT LLM                      249      83         29        74.36        78.26      66.78     63.01
                   A SSERTION F ORGE W / O RTL      233      93         28        74.36        78.26      70.72     68.49
                   A SSERTION F ORGE O RIG KG       279      174        50        84.62        84.78      83.88     83.56
                   A SSERTION F ORGE                253      132        27        84.62        84.78      88.82     90.41



A SSERTION F ORGE O RIG KG: This baseline uses the full                  assertion’s influence. COI coverage is obtained using the
A SSERTION F ORGE pipeline but uses the vanilla GraphRAG                 check_cov command in Jasper.
prompt for KG construction instead of our domain-customized
prompt with hardware-specific schema and examples.                       D. Results and Analysis
                                                                            Table II presents the evaluation results across five hardware
                                                                         designs, where A SSERTION F ORGE consistently outperforms
C. Evaluation Protocol
                                                                         the baselines in both proven assertions and coverage. The gains
   We use Cadence JASPER (version 2023.12) to evaluate our               are especially notable for more complex designs, achieving
generated SystemVerilog Assertions (SVAs). We measure the                near-perfect coverage across multiple metrics. Although A S -
total number of SVAs generated (#SVA), the number of syntac-             SERTION F ORGE O RIG KG generally surpasses A SSERT LLM,
tically correct SVAs (#SynC), and the number of SVAs proven              it still falls short of the full A SSERTION F ORGE pipeline, un-
without counterexamples (#Proven). Assuming a golden RTL                 derscoring the impact of our domain-specific KG construction.
implementation, this work focuses on generating high-quality             These results highlight not just the quantity but the quality of
SVAs; debugging counterexamples to determine root cause                  our generated assertions — a critical distinction since plausible
(RTL bug versus assertion error) is left for future work.                but incorrect assertions waste computational resources.
Coverage is evaluated only for proven assertions using Jasper’s
cone-of-influence (COI) coverage [10], [34] models. We report            E. Ablation Study
COI Functional Coverage, COI Branch Coverage, COI                          To analyze the contribution of each component in A S -
Statement Coverage, and COI Toggle Coverage, measuring                   SERTION F ORGE , we conduct an ablation study on the UART
coverage of high-level functionality, conditional branches,              design as in Table III. Removing the guided random walk
statements, and signal transitions, respectively, within the             algorithm (No GRW) significantly reduces the number of
                                                             TABLE III
     A BLATION STUDY RESULTS ON THE UART DESIGN , SHOWING THE IMPACT OF REMOVING INDIVIDUAL COMPONENTS FROM OUR FRAMEWORK .

                                                                                                                 COI Coverage (%)
               Model Variant                                       #SVA      #SynC      #Proven
                                                                                                    Statement    Branch   Functional      Toggle
               Full A SSERTION F ORGE (all components)              253       132          27         84.62       84.78     88.82         90.41
               No Summaries (w/o global summarization)              236        76          31         84.62       84.78     78.29         75.80
               No RAG (w/o retrieval-augmented generation)          311       128          38         84.62       84.78     83.55         83.11
               No GRW-AS (w/o guided random walk)                   243       115          26         84.62       84.78     83.55         83.11
               No Pruner (w/o LLM-based context pruning)            281       144          20         84.62       84.78     83.88         83.56
               Spec-RTL Concatenation                                91        36           9         74.36       78.26     70.39         68.04


proven assertions, highlighting its importance in exploring rel-                      Selected SVAs Generated for ETHMAC
evant design paths. The global summarization component (No
                                                                                      Plan: Validate that when ‘ResetByteCnt’ and ‘xReset’ are active,
Summaries) drastically reduces syntactically correct assertions                       ‘ByteCnt’ is set to zero and ‘TxFlow’ halts within the next clock cycle.
while producing mixed effects on coverage metrics. The base-                          SVA:
line approach that simply concatenates specification and RTL                          @(posedge MTxClk)
text (Spec-RTL Concat) performs worst across all metrics,                               (ResetByteCnt == 1 && TxReset == 1)
demonstrating that naively combining all available information                          |-> (ByteCnt == 0 && TxFlow == 0);
overwhelms the LLM and is impractical for industry-scale                              Plan: Ensure that ‘WillSendControlFrame’ is asserted just before ‘TxS-
designs with substantially larger specifications and RTL.                             tartFrmIn’ is asserted and remains asserted until ‘TxEndFrmIn’ is as-
                                                                                      serted. SVA:
F. Case Study: Knowledge Graph Visualization                                          @(posedge MTxClk)
                                                                                        ((WillSendControlFrame && TxStartFrmIn)
  Figure 2 visualizes KGs constructed from the OPEN-                                     && !TxEndFrmIn)
MSP430 design specification, contrasting the impact of our                              |-> WillSendControlFrame;
domain-specific schema.

                                                                                           Fig. 3. Examples of SVAs generated by A SSERTION F ORGE.

                            …
                                                                                    tx_busy (port) → uart_tx (module) →
                                                                                    uart_top (module) → new_tx_data (port) →
                                                                                    data_stability (verification_point)
                                                                                    Together with global summaries and signal-specific context,
                                                                                    A SSERTION F ORGE synthesized this path information to gen-
                                                                                    erate this key SVA:
Fig. 2. Visualization of the KGs from OPEN MSP430 using [6]. Node colors            @(posedge clock) (!tx_busy && new_tx_data)
represent different types of entities, such as modules and signals. Node colors         |-> ##1 tx_busy
indicate the type attribute of each entity. Left: KG generated via the original
entity extraction prompt of GraphRAG. Middle: KG generated via our domain-             Path 2: APB Interrupt Generation. This subpath exposes
customized prompt. Right: Two zoomed-in views of the KG, highlighting key           interrupt control flow:
entities with their labels.
                                                                                    INT_TX (assignment) → apb (module) →
                                                                                    TX_EMPTY (port) → data_stability (point) →
G. Case Study: SVAs Generated for ETHMAC                                            reset_behavior (point) → PRESETn (port)
   We illustrate that A SSERTION F ORGE generates high-quality                      These KG-derived insights, combined with specification snip-
SVAs capturing essential design properties on the ETHMAC                            pets and global design context, led to critical SVAs for FIFO
design in Figure 3, an Ethernet MAC transmit control module.                        status and reset behavior:
The first SVA ensures ‘ByteCnt’ resets and ‘TxFlow’ halts                           @(posedge PCLK) TX_EMPTY |=> INT_TX
during reset, which is crucial for maintaining transmission                         @(posedge PCLK) (!PRESETn) |-> TX_EMPTY
integrity, while the second verifies the correct assertion of                                     V. C ONCLUSION AND F UTURE W ORK
‘WillSendControlFrame’ during the transmission of control
frames, ensuring proper data transmission.                                             We introduced A SSERTION F ORGE, a novel approach for
                                                                                    generating SystemVerilog Assertions (SVAs) that integrates
H. Case Study: Paths Extracted by GRW-AS Algorithm                                  Knowledge Graph (KG) and Register-Transfer Level (RTL)
   To illustrate the effectiveness of our GRW-AS algorithm,                         information. Experimental results on five designs demonstrate
we examine key paths extracted from two designs’ KGs that                           significant improvements over baseline methods. While our
may have contributed to generating high-quality SVAs. Due to                        approach shows promising results, future work could explore
space constraints, we show selected subpaths that capture the                       more sophisticated KG construction techniques, methods to
essential signal relationships.                                                     further improve functional coverage, and extensions to other
   Path 1: UART Transmission Control. This path reveals                             hardware design automation tasks such as automatic code
critical dependencies:                                                              generation and design error detection.
                               R EFERENCES                                         [22] Aditya Grover and Jure Leskovec. node2vec: Scalable feature learning
                                                                                        for networks. In Proceedings of the 22nd ACM SIGKDD international
                                                                                        conference on Knowledge discovery and data mining, pages 855–864,
 [1] Bilal Abu-Salih. Domain-specific knowledge graphs: A survey. Journal               2016.
     of Network and Computer Applications, 185:103076, 2021.
                                                                                   [23] Will Hamilton, Zhitao Ying, and Jure Leskovec. Inductive representation
 [2] Mohammad Akyash and Hadi Mardani Kamali. Self-hwdebug: Automa-                     learning on large graphs. Advances in neural information processing
     tion of llm self-instructing for hardware security verification. arXiv             systems, 30, 2017.
     preprint arXiv:2405.12347, 2024.
                                                                                   [24] Marti A Hearst. TextTiling: Segmenting text into multi-paragraph
 [3] Amira A Alshazly, Ahmed M Elfatatry, and Mohamed S Abougabal.                      subtopic passages. Computational Linguistics, 23(1):33–64, 1997.
     Detecting defects in software requirements specification. Alexandria          [25] Shaoxiong Ji, Shirui Pan, Erik Cambria, Pekka Marttinen, and S Yu
     Engineering Journal, 53(3):513–527, 2014.                                          Philip. A survey on knowledge graphs: Representation, acquisition,
 [4] Avinash Ayalasomayajula, Rui Guo, Jingbo Zhou, Sujan Kumar Saha,                   and applications. IEEE transactions on neural networks and learning
     and Farimah Farahmandi. Lasp: Llm assisted security property gen-                  systems, 33(2):494–514, 2021.
     eration for soc verification. In Proceedings of the 2024 ACM/IEEE             [26] Philip Nicholas Johnson-Laird. Mental models: Towards a cognitive
     International Symposium on Machine Learning for CAD, pages 1–7,                    science of language, inference, and consciousness. Number 6. Harvard
     2024.                                                                              University Press, 1983.
 [5] Lars Backstrom and Jure Leskovec. Supervised random walks: predict-           [27] Rahul Kande, Hammond Pearce, Benjamin Tan, Brendan Dolan-Gavitt,
     ing and recommending links in social networks. In Proceedings of the               Shailja Thakur, Ramesh Karri, and Jeyavijayan Rajendran. Llm-assisted
     fourth ACM international conference on Web search and data mining,                 generation of hardware assertions. arXiv preprint arXiv:2306.14027,
     pages 635–644, 2011.                                                               2023.
 [6] Mathieu Bastian, Sebastien Heymann, and Mathieu Jacomy. Gephi: An             [28] Rahul Kande, Hammond Pearce, Benjamin Tan, Brendan Dolan-Gavitt,
     open source software for exploring and manipulating networks, 2009.                Shailja Thakur, Ramesh Karri, and Jeyavijayan Rajendran. (security)
 [7] Zhen Bi, Jing Chen, Yinuo Jiang, Feiyu Xiong, Wei Guo, Huajun Chen,                assertions by large language models. IEEE Transactions on Information
     and Ningyu Zhang. Codekgc: Code language model for generative                      Forensics and Security, 2024.
     knowledge graph construction. ACM Transactions on Asian and Low-              [29] Minwoo Kang, Mingjie Liu, Ghaith Bany Hamad, Syed Suhaib, and
     Resource Language Information Processing, 23(3):1–16, 2024.                        Haoxing Ren. Fveval: Understanding language model capabilities in for-
 [8] Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann, Trevor Cai,                    mal verification of digital hardware. arXiv preprint arXiv:2410.23299,
     Eliza Rutherford, Katie Millican, George Bm Van Den Driessche, Jean-               2024.
     Baptiste Lespiau, Bogdan Damoc, Aidan Clark, et al. Improving                 [30] Amanda Kau, Xuzeng He, Aishwarya Nambissan, Aland Astudillo, Hui
     language models by retrieving from trillions of tokens. In International           Yin, and Amir Aryani. Combining knowledge graphs and large language
     conference on machine learning, pages 2206–2240. PMLR, 2022.                       models. arXiv preprint arXiv:2407.06564, 2024.
 [9] Antoine Bosselut, Hannah Rashkin, Maarten Sap, Chaitanya Malaviya,            [31] Aman Kumar and Deepak Narayan Gadde. Generative ai augmented
     Asli Celikyilmaz, and Yejin Choi. Comet: Commonsense transformers                  induction-based formal verification. arXiv preprint arXiv:2407.18965,
     for automatic knowledge graph construction. ACL, 2019.                             2024.
[10] Hana Chockler, Orna Kupferman, and Moshe Y Vardi. Coverage metrics            [32] Chankyu Lee, Rajarshi Roy, Mengyao Xu, Jonathan Raiman, Moham-
     for formal verification. In Correct Hardware Design and Verification               mad Shoeybi, Bryan Catanzaro, and Wei Ping. Nv-embed: Improved
     Methods: 12th IFIP WG 10.5 Advanced Research Working Conference,                   techniques for training llms as generalist embedding models. arXiv
     CHARME 2003, L’Aquila, Italy, October 21-24, 2003. Proceedings 12,                 preprint arXiv:2405.17428, 2024.
     pages 111–125. Springer, 2003.                                                [33] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir
[11] Edmund M Clarke, Thomas A Henzinger, Helmut Veith, and Roderick                    Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih,
     Bloem. Model checking. MIT press, 2018.                                            Tim Rocktäschel, et al. Retrieval-augmented generation for knowledge-
[12] Colin Cooper, Sang Hyuk Lee, Tomasz Radzik, and Yiannis Siantos.                   intensive nlp tasks. Advances in Neural Information Processing Systems,
     Random walks in recommender systems: exact computation and simu-                   33:9459–9474, 2020.
     lations. In Proceedings of the 23rd international conference on world         [34] Ang Li, Hao Chen, JK Yu, Ee Loon Teoh, and Iswerya Prem Anand.
     wide web, pages 811–816, 2014.                                                     A coverage-driven formal methodology for verification sign-off. In
[13] Luciano da Fontoura Costa and Gonzalo Travieso. Exploring complex                  Design and Verification Conference and Exhibition (DVCon) United
     networks through random walks. Physical Review E—Statistical, Non-                 States, 2019.
     linear, and Soft Matter Physics, 75(1):016102, 2007.                          [35] Ke Liang, Lingyuan Meng, Meng Liu, Yue Liu, Wenxuan Tu, Siwei
[14] Zhuyun Dai and Jamie Callan. Deeper text understanding for IR with                 Wang, Sihang Zhou, Xinwang Liu, Fuchun Sun, and Kunlun He. A
     contextual neural language modeling. In Proceedings of the 42nd                    survey of knowledge graph reasoning on graph types: Static, dynamic,
     International ACM SIGIR Conference on Research and Development                     and multi-modal. IEEE Transactions on Pattern Analysis and Machine
     in Information Retrieval, pages 985–988, 2019.                                     Intelligence, 2024.
[15] Alessandro Danese, Nicolò Dalla Riva, and Graziano Pravadelli. A-            [36] Mingjie Liu, Minwoo Kang, Ghaith Bany Hamad, Syed Suhaib, and
     team: Automatic template-based assertion miner. In Proceedings of the              Haoxing Ren. Domain-adapted llms for vlsi design and verification:
     54th Annual Design Automation Conference 2017, pages 1–6, 2017.                    A case study on formal verification. In 2024 IEEE 42nd VLSI Test
[16] Ashish Darbari. Specifications: The hidden bargain for formal verifica-            Symposium (VTS), pages 1–4. IEEE, 2024.
     tion. EDN Network, September 2022.                                            [37] Karthik Maddala, Bhabesh Mali, and Chandan Karfa. Laag-rv: Llm
[17] Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao,                    assisted assertion generation for rtl design verification. In 2024 IEEE
     Apurva Mody, Steven Truitt, and Jonathan Larson. From local to global:             8th International Test Conference India (ITC India), pages 1–6. IEEE,
     A graph rag approach to query-focused summarization. arXiv preprint                2024.
     arXiv:2404.16130, 2024.                                                       [38] Bhabesh Mali, Karthik Maddala, Sweeya Reddy, Vatsal Gupta, Chandan
[18] Wenji Fang, Mengming Li, Min Li, Zhiyuan Yan, Shang Liu, Hongce                    Karfa, and Ramesh Karri. Chiraag: Chatgpt informed rapid and auto-
     Zhang, and Zhiyao Xie. Assertllm: Generating and evaluating hardware               mated assertion generation. arXiv preprint arXiv:2402.00093, 2024.
     verification assertions from design specifications via multi-llms. arXiv      [39] Jose L Martinez-Rodriguez, Ivan Lopez-Arevalo, and Ana B Rios-
     preprint arXiv:2402.00386, 2024.                                                   Alvarado. Openie-based approach for knowledge graph construction
[19] Harry D Foster, Adam C Krolnik, and David J Lacey. Assertion-based                 from text. Expert Systems with Applications, 113:339–355, 2018.
     verification: Industry myths to realities (invited tutorial). International   [40] OpenAI. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023.
     Conference on Computer Aided Verification, pages 5–10, 2008.                  [41] OpenAI. Tokenizer. https://platform.openai.com/tokenizer, 2023. Ac-
[20] Samuele Germiniani and Graziano Pravadelli. Harm: a hint-based                     cessed: 2024-09-18.
     assertion miner. IEEE Transactions on Computer-Aided Design of                [42] OpenCores. Opencores: Open source hardware designs. OpenCores
     Integrated Circuits and Systems, 41(11):4277–4288, 2022.                           Website, 2024. Accessed: June 28, 2024.
[21] Eugene Goldberg. Generation of A complete set of properties. CoRR,            [43] Marcelo Orenes-Vera, Aninda Manocha, David Wentzlaff, and Margaret
     abs/2004.05853, 2020.                                                              Martonosi. Autosva: Democratizing formal verification of rtl module
     interactions. In 2021 58th ACM/IEEE Design Automation Conference                                    A PPENDIX A
     (DAC), pages 535–540. IEEE, 2021.                                                            I MPLEMENTATION D ETAILS
[44] Marcelo Orenes-Vera, Margaret Martonosi, and David Wentzlaff. Us-
     ing llms to facilitate formal verification of rtl.       arXiv preprint    A. Overall Process
     arXiv:2309.08604, 2023.
[45] Shirui Pan, Linhao Luo, Yufei Wang, Chen Chen, Jiapu Wang, and
                                                                                   Algorithm 1 outlines the core workflow of A SSERTION -
     Xindong Wu. Unifying large language models and knowledge graphs:           F ORGE, integrating specification analysis, RTL parsing, and
     A roadmap. IEEE Transactions on Knowledge and Data Engineering,            multi-resolution context synthesis.
     2024.
[46] Boci Peng, Yun Zhu, Yongchao Liu, Xiaohe Bo, Haizhou Shi, Chuntao
     Hong, Yan Zhang, and Siliang Tang. Graph retrieval-augmented gener-
                                                                                Algorithm 1 A SSERTION F ORGE Main Process
     ation: A survey. arXiv preprint arXiv:2408.08921, 2024.                    Require: Design specification S, RTL code R
[47] Vaishnavi Pulavarthi, Deeksha Nandal, Soham Dan, and Debjit Pal. Are       Ensure: Generated SVAs A
     llms ready for practical adoption for assertion generation?, 2025.          1: Parse specification: S ← PDFParser(S)
[48] Nils Reimers and Iryna Gurevych. Sentence-bert: Sentence embeddings         2: Build initial KG: G0 ← F (S) {Sec. III-B}
     using siamese bert-networks. arXiv preprint arXiv:1908.10084, 2019.         3: Refine KG with RTL: G ← ψ(G0 , R) {Sec. A-C}
[49] Xuhui Ren, Tong Chen, Quoc Viet Hung Nguyen, Lizhen Cui, Zi Huang,          4: Extract valid architectural signals: V ← RTLSignalExtractor(R)
     and Hongzhi Yin. Explicit knowledge graph reasoning for conversa-
     tional recommendation. ACM Transactions on Intelligent Systems and          5: Generate global summary: Cg ← DesignSummarizer(S, R, V)
     Technology, 15(4):1–21, 2024.                                               6: for each signal vi ∈ V do
[50] Stephen Robertson and Hugo Zaragoza. The probabilistic relevance            7:    Retrieve signal context: Cr ← SSR(vi , S, R)
     framework: BM25 and beyond. Foundations and Trends in Information           8:    Extract KG paths: Ck ← GRW-AS(G, vi , V) {Sec. III-E}
     Retrieval, 3(4):333–389, 2009.                                              9:    Prune contexts: Cp ← P(Cg ∪ Cr ∪ Ck )
[51] Gerard Salton and Christopher Buckley. Term-weighting approaches           10:    Initialize prompt budget: B ← 3 {Max prompts per signal}
     in automatic text retrieval. Information processing & management,          11:    for j ← 1 to B do
     24(5):513–523, 1988.                                                       12:       Construct dynamic prompt: Di,j ← Ω(Cp , vi , j) {Sec. A-J}
[52] Kalpesh Sanghvi. From specification to chip: A holistic design approach.
     SemiEngineering, 2014.                                                     13:      Generate NL plans: Pi,j ← Lplan (Di,j )
[53] Bhaskarjit Sarmah, Benika Hall, Rohan Rao, Sunil Patel, Stefano            14:      Synthesize SVAs: Ai,j ← Lsva (Pi,j , Di,j )
     Pasquali, and Dhagash Mehta. Hybridrag: Integrating knowledge graphs       15:      Verify assertions: Jasper(Ai,j )
     and vector retrieval augmented generation for efficient information        16:   end for
     extraction. arXiv preprint arXiv:2408.04948, 2024.                         17: end for
[54] Cunxi Sun, Christoph Hahn, and Caroline Trippel. Towards improving
                                                                                                                                 S
                                                                                18: Aggregate coverage metrics: AnalyzeResults( i,j Ai,j )
     verification productivity with circuit-aware translation of natural lan-
     guage to systemverilog assertions. In First International Workshop on
     Deep Learning-aided Verification (DAV), 2023.
[55] Shinya Takamaeda-Yamazaki. Pyverilog: A python-based hardware              B. Knowledge Graph Construction from Specifications
     design processing toolkit for verilog hdl. In Applied Reconfigurable
     Computing, volume 9040 of Lecture Notes in Computer Science, pages            The creation of a comprehensive Knowledge Graph (KG)
     451–460. Springer International Publishing, Apr 2015.                      from design specifications is a critical first step in our ap-
[56] Milena Trajanoska, Riste Stojanov, and Dimitar Trajanov. Enhancing
     knowledge graph construction using large language models. arXiv
                                                                                proach. We leverage a customized version of GraphRAG [17]
     preprint arXiv:2305.04676, 2023.                                           for this purpose, adapting it specifically for hardware veri-
[57] Shobha Vasudevan, David Sheridan, Sanjay Patel, David Tcheng, Bill         fication domain knowledge. The entity extraction process is
     Tuohy, and Daniel Johnson. Goldmine: Automatic assertion generation        guided by a detailed prompt that defines the domain-specific
     using data mining and static analysis. In 2010 Design, Automation &
     Test in Europe Conference & Exhibition (DATE 2010), pages 626–629.
                                                                                schema (Figure 4). This prompt is crucial for ensuring that
     IEEE, 2010.                                                                the LLM extracts relevant entities and relationships from the
[58] Srikanth Vijayaraghavan and Meyyappan Ramanathan. A practical guide        hardware specifications.
     for SystemVerilog assertions. Springer Science & Business Media, 2005.        A key advantage of our approach is the adaptability of the
[59] Hong Wang, Jin Liu, Mingyang Duan, Peizhu Gong, Zhongdai Wu,               knowledge graph schema. Formal verification engineers can
     Junxiang Wang, and Bing Han. Cross-modal knowledge guided
     model for abstractive summarization. Complex & Intelligent Systems,        modify the entity and relation types based on their domain
     10(1):577–594, 2024.                                                       knowledge and the specific design under verification. For
[60] Yu Wang, Nedim Lipka, Ryan A Rossi, Alexa Siu, Ruiyi Zhang, and            example, when verifying a processor design, additional entity
     Tyler Derr. Knowledge graph prompting for multi-document question
     answering. In Proceedings of the AAAI Conference on Artificial
                                                                                types like ”Pipeline Stage,” ”Execution Unit,” or ”Branch
     Intelligence, volume 38, pages 19206–19214, 2024.                          Predictor” could be added to the schema. Similarly, when
[61] George H Weiss and Robert J Rubin. Random walks: theory and selected       verifying a memory controller, types like ”Memory Channel,”
     applications. Adv. Chem. Phys, 52:363–505, 1983.                           ”Timing Parameter,” or ”Refresh Cycle” might be more rele-
[62] Hongbin Ye, Ningyu Zhang, Hui Chen, and Huajun Chen. Generative            vant.
     knowledge graph construction: A review. EMNLP, 2022.
[63] Lingfeng Zhong, Jia Wu, Qian Li, Hao Peng, and Xindong Wu. A               C. RTL Parsing and Knowledge Graph Refinement
     comprehensive survey on automatic knowledge graph construction. ACM
     Computing Surveys, 56(4):1–62, 2023.                                         The initial knowledge graph, G0 , constructed from the
[64] Yuqi Zhu, Xiaohan Wang, Jing Chen, Shuofei Qiao, Yixin Ou, Yunzhi          design specification, is refined by integrating structural and
     Yao, Shumin Deng, Huajun Chen, and Ningyu Zhang. Llms for
     knowledge graph construction and reasoning: Recent capabilities and        behavioral information extracted from the RTL code, R. This
     future opportunities. World Wide Web, 27(5):58, 2024.                      process, denoted as G = ψ(G0 , R), is crucial for bridging the
  Prompt for Entity Extraction                                                   The parsing process begins by preprocessing the RTL files
                                                                              to handle include directives, inlining the contents of included
  [The following content is summarized or omitted for brevity: - Goal,        files to create a self-contained representation. We extract key
  Steps, and Additional instructions for hardware design specifications.
  For the full prompt, please refer to the GraphRAG repository.]              structural and behavioral information through several special-
  Entity Types:                                                               ized methods.
  Design Specification, Section, Subsection, Table, Figure, Author, Mod-         For structural information, we leverage PyVerilog’s parser
  ule, Submodule, Protocol, Signal, Port, Register, FIFO, Clock, Interrupt,
  Operation, Frequency, Standard, Reference, Component, Version, Date,        to extract hierarchical component information. Module defi-
  Comment, Pin, Configuration, Constraint/Rule, Address, Document,            nitions are identified by traversing the Abstract Syntax Tree
  Block                                                                       (AST) and locating “ModuleDef” nodes. For each module, we
  Relation Types:
  hasSection, hasSubsection, contains, authoredBy, defines, imple-            extract port declarations (“Input”, “Output”, “Inout” nodes)
  ments, uses, connectsTo, configures, generatesInterrupt, operate-           from the AST, capturing direction (input/output/inout) and
  sAt, compliesWith, referencedIn, inputTo, outputFrom, partOf, in-           width details (using the “Width” node in the AST). This
  terfacesWith, triggersOperation, dependsOn, transmitsData, receives-
  Data, has input, has output, has register, performs, uses protocol,         process determines whether a port is an input or output and
  has constraint, has rule, describes, references, modifies, creates, clos-   extracts its bit width through direct AST analysis. Module
  es/fixes, HasSubModule, HasSignal, HasPort, UsesProtocol, UsesClock,        instantiations are identified within the parent module’s defini-
  UsesAddress, DescribesOperation, TriggersInterrupt, RevisionHistory,
  belongsToSection, illustrates, hasAuthor, has port, connected to, de-       tion via “Instance” nodes, along with their port connections
  scribed in                                                                  by examining the “portlist” attribute.
  Examples:                                                                      For behavioral information, we leverage a multi-strategy
  [Example outputs and entity-relationship formats demonstrated in mul-
  tiple contexts, including hardware design specifications and narrative      approach to identify FSMs. The primary method examines
  texts.]                                                                     always blocks with clock sensitivity lists that contain case
  -Real Data-                                                                 statements, a common FSM implementation pattern. We sup-
  Entity types: {entity types}
  Text: {input text}                                                          plement this with pattern matching to identify state vari-
                                                                              ables, looking for signals named with common patterns like
                                                                              ”state”, ”st ”, or ”current”. For instance, when we encounter
Fig.   4.           Example  prompt  for entity  extrac-                      code patterns like ”always @(posedge clk)” followed by
tion   (abbreviated).    For   the  full prompt,    see:
https://github.com/microsoft/graphrag/blob/main/                              ”case(current state)”, we recognize a potential FSM. Within
graphrag/index/graph/extractors/graph/prompts.py                              these “always” blocks, we look for “case” statements (rep-
                                                                              resented by “Case” nodes in the AST). We supplement this
                                                                              AST-based approach with pattern matching on signal and
gap between high-level design intent and low-level implemen-                  parameter names, looking for common FSM-related identifiers
tation details. We achieve this using a custom RTL analysis                   like “state”, “current state”, “next state”, “st ”, or “fsm”. This
pipeline built upon the PyVerilog library [55]. Algorithm 2                   helps identify FSMs even when coding styles deviate from the
provides an overview of the RTL parsing procedure.                            strict “always @(posedge clk)” and “case(state)” pattern.
                                                                                 Control flow structures are another critical aspect of RTL
   The RTL parsing and knowledge graph refinement were
                                                                              behavior. We extract conditional statements (if/else), case
implemented using Python 3.10.14 and PyVerilog version
                                                                              statements, and loops using a combination of AST traversal
1.3.0.
                                                                              and pattern matching. For example, a regex pattern identi-
                                                                              fies case statement conditions, which often represent state-
Algorithm 2 RTL Parsing and KG Refinement                                     dependent behavior. Similarly, we analyze assignments, distin-
Require: Initial KG G0 , RTL code R                                           guishing between continuous assignments (assign statements)
Ensure: Refined KG G
 1: G ← G0 {Initialize with specification KG}
                                                                              and procedural assignments in always blocks.
 2: R ← preprocess includes(R) {Inline included files}                           Signal assignments are extracted from both “Assign” nodes
 3: rtl elements ← parse rtl(R) {Extract modules, ports, signals,             (for continuous assignments) and from within “always” blocks
    etc.}                                                                     (for procedural assignments). For each assignment, the left-
 4: dataflow ← analyze dataflow(R) {Extract signal dependencies}              hand side (LHS) signal (the target of the assignment) and
 5: for each module m ∈ rtl elements.modules do
 6:    Add module node to G
                                                                              the right-hand side (RHS) expression are recorded. The RHS
 7:    Add nodes for module ports, signals, instances, FSMs                   expression is further analyzed to identify the signals involved,
 8:    Add edges for structural relationships (containment, connec-           establishing dependencies. We distinguish between blocking
       tions)                                                                 and non-blocking assignments, which is crucial for correctly
 9:    Add nodes and edges for behavioral relationships (assign-              modeling Verilog semantics.
       ments, control flow)
10: end for
                                                                                 PyVerilog’s “VerilogDataflowAnalyzer” is used to construct
11: Link specification nodes in G0 to corresponding RTL nodes in G            a dataflow graph. The analyzer’s “getBindings” method is used
                                                                              to obtain the dataflow bindings for each signal, revealing its
12: Add root node connecting all components if needed for graph               dependencies. We add this dataflow information directly to our
    connectivity                                                              knowledge graph by creating edges between signal nodes.
13: return G
                                                                                 After extracting this RTL information, we refine the knowl-
 edge graph as shown in Algorithm 2. New nodes are added           edit-distance-based matches with scores decreasing as distance
 for RTL elements, including modules, ports, signals, module       increases. We require a minimum match score of 0.6 and
 instances, FSMs, control flow structures, and assignments.        prioritize the highest-scoring match when multiple candidates
 Existing nodes from the initial specification KG (G0 ) are        exist.
 preserved. Edges are created to represent:                           For example, given an RTL signal ”tx data valid”, our
   (i) Containment: Modules contain ports, signals, instances,     algorithm would successfully match specification mentions
       FSMs, and control structures.                               of ”transmit data valid”, ”TX DATA VALID”, or ”tx data
  (ii) Instantiation: A module instantiates another module.        valid signal”. This fuzzy matching is particularly valuable
 (iii) Port Connections: Signals are connected to ports in         for signals with domain-specific naming, where conventional
       module instances.                                           string similarity metrics alone would fail to establish correct
 (iv) Dataflow: Signals drive other signals through assign-        correspondence.
       ments.
                                                                   E. RTL Signal Extractor
  (v) Control Flow: Control structures (if, case, loops) influ-
       ence signals/assignments.                                      In the A SSERTION F ORGE framework, the RTL Signal Ex-
 (vi) FSM Structure: An edge goes from FSM to module.              tractor is essential for identifying and extracting valid sig-
(vii) Assignment: An edge goes from assignment to lhs and          nals from the RTL code. This process begins by parsing
       rhs.                                                        the RTL code to locate module declarations and their inter-
                                                                   faces, typically encompassing input, output, and inout
    Finally, a linking process, detailed in Section A-D, estab-
                                                                   signals. Using regular expressions, the extractor identifies
 lishes connections between nodes in the specification KG (G0 )
                                                                   signal declarations, capturing details such as signal direc-
 and the RTL-derived KG (G). The result is a unified KG
                                                                   tion (input, output, inout), data type (reg, wire),
 representing both design intent and implementation details.
                                                                   and bit-width specifications. For instance, a signal declared
D. Fuzzy Signal Name Matching                                      as input [7:0] data_in indicates an 8-bit wide input
                                                                   signal named data_in. Once extracted, these signal names
   A critical aspect of bridging the specification and RTL
                                                                   are compiled into a set of valid signals, serving as a reference
domains is establishing correspondence between entity names
                                                                   for subsequent stages in the workflow as in Algorithm 1.
that may differ due to naming conventions or abbreviations.
Our approach leverages a combination of exact and fuzzy            F. Global Summarization
matching techniques to link entities between the specification
                                                                      The Design Summarizer (Global Summarization) compo-
and RTL knowledge graphs.
                                                                   nent, denoted as Cg ← DesignSummarizer(S, R, V) in Algo-
   For exact matching, we identify direct name references in       rithm 1, plays a pivotal role in distilling complex hardware
the specification text using regular expressions, seeking word     design specifications and RTL code into concise, verification-
boundary-anchored occurrences of signal and module names           focused summaries. This step is essential for providing the
from the RTL. However, hardware specifications often refer         language model with a comprehensive understanding of the de-
to signals using variants of their RTL names. For example, a       sign context prior to assertion generation. Our implementation
specification might mention ”reset signal” while the RTL uses      leverages a multi-faceted summarization approach that targets
”rst n” or ”PRESETn”.                                              different aspects of the design through specialized prompts.
   To address this, we implement a specialized fuzzy matching         The Design Summarizer generates several complementary
algorithm that considers:                                          views of the design. First, it creates a high-level design
  (i) Common hardware abbreviations: We maintain a dic-            specification summary (Figure 5) that captures the main func-
      tionary mapping between full terms and common hard-          tionality and architectural components in 3-5 sentences. This
      ware abbreviations (e.g., ”reset” → ”rst”, ”clock” →         is complemented by an RTL architecture summary (Figure 6)
      ”clk”).                                                      that focuses on module hierarchy and interfaces. Additionally,
 (ii) Case and separator variations: We normalize names            it produces a comprehensive signals summary (Figure 7)
      by converting to lowercase and removing separators           that provides detailed information about each valid signal,
      like underscores, allowing matches between variants like     including type, bit width, functionality, and interactions with
      ”data valid” and ”DataValid”.                                other signals. Finally, it identifies key design patterns and
(iii) Active-low signal conventions: We detect common pat-         protocols (Figure 8) that have verification implications.
      terns for active-low signals (e.g., ” n”, ” b” suffixes or      Beyond these global summaries, the Design Summarizer
      negation prefixes like ”n” or ”not ”).                       also generates signal-specific descriptions for each target
(iv) Levenshtein distance: For remaining candidates, we            signal during the assertion generation process. This focused
      calculate edit distance with thresholds proportional to      analysis, shown in Figure 9, provides detailed context about
      name length, capturing minor typographical variations.       the specific signal for which assertions are being generated.
   The matching process uses a scoring system where exact             The Design Summarizer implements an efficient caching
matches receive the highest score (1.0), followed by abbre-        mechanism to avoid redundant LLM calls. The global design
viation expansions (0.9), case/separator variations (0.8), and     summary is generated once and reused across all assertion
  Prompt for Design Specification Summary                                       Prompt for Signal-Specific Description

  You are an expert hardware design engineer. Please provide a concise          You are an expert hardware verification engineer. Please provide a
  summary (3-5 sentences) of the following hardware design specification.       detailed description of the signal ’{signal name}’ based on the following
  Focus on the main functionality, key components, and architecture. The        specification and RTL.
  summary should give a clear high-level understanding of what this design      Design Specification: {spec text}
  does.                                                                         RTL Code: {rtl text}
  Design Specification: {spec text}                                             Include in your description:
  Provide only the summary, with no additional commentary or introduc-          The precise function of this signal Its type (input, output, inout, internal,
  tion.                                                                         etc.) and bit width Its timing characteristics (synchronous/asynchronous,
                                                                                edge-triggered, etc.) Key relationships with other signals How it affects
                                                                                or is affected by the overall system behavior Any special conditions or
                                                                                corner cases related to this signal Write 3-5 sentences with comprehen-
Fig. 5. Prompt for generating a high-level design specification summary.        sive, verification-focused details.
The prompt emphasizes conciseness while focusing on functionality, key
components, and architecture.
                                                                              Fig. 9. Prompt for generating a detailed description of a specific signal,
                                                                              focusing on its function, characteristics, and interactions.
  Prompt for RTL Architecture Summary
  You are an expert hardware design engineer. Please provide a concise
  summary (3-5 sentences) of the following RTL code. Focus on the             generation tasks, while signal-specific descriptions are cached
  module hierarchy, interfaces, and key architectural features.               individually. This approach significantly reduces the overall
  RTL Code: {rtl text}
  Provide only the RTL architecture summary, with no additional com-
                                                                              LLM query cost while maintaining comprehensive context for
  mentary or introduction.                                                    assertion generation.
                                                                                 When constructing the final context for assertion generation,
                                                                              the summarizer combines these various summary components
Fig. 6. Prompt for generating an RTL architecture summary, focusing on        in a hierarchical manner, starting with the global design
module hierarchy and interfaces.
                                                                              overview, followed by the RTL architecture summary, the
                                                                              target signal description, the comprehensive signals summary,
  Prompt for Comprehensive Signals Summary                                    and finally the design patterns summary. This layered approach
                                                                              provides the assertion generation model with both broad de-
  You are an expert hardware verification engineer. Please analyze the
  following design specification and RTL code to provide a comprehensive
                                                                              sign context and signal-specific details, enabling it to generate
  summary of the signals in the design. For each signal, include details      more accurate and relevant SystemVerilog assertions.
  about:
  Signal name                                                                 G. Signal-Specific Retrieval (SSR)
  Signal type (input, output, inout, internal, clock, reset, etc.)
  Bit width (e.g., 1-bit, 8-bit, 32-bit)                                         The Signal-Specific Retrieval (SSR) component, represented
  Functionality and purpose                                                   as Cr ← SSR(vi , S, R) in Algorithm 1, is responsible for
  Key interactions with other signals
  Valid Signals: signals str
                                                                              retrieving relevant contextual information from both specifica-
  Design Specification: {spec text}                                           tion documents and RTL code based on signal-specific queries.
  RTL Code: {rtl text}                                                           Our SSR implementation serves as a critical middle-
  Focus on the signals listed above. If the RTL/spec doesn’t provide
  information for a signal, make your best inference. Format your response    resolution layer in our multi-level context synthesis frame-
  as a list with each signal having its own paragraph that includes all the   work, bridging the gap between the high-level global sum-
  details mentioned above. Be concise yet complete.                           marization and the fine-grained graph traversal of GRW-AS.
                                                                              While global summarization captures design-wide architec-
Fig. 7. Prompt for generating a comprehensive summary of all signals in the
                                                                              tural intent and GRW-AS explores detailed signal-to-signal
design, including detailed technical characteristics.                         relationships, SSR provides essential functional context at the
                                                                              module and subsystem level. This intermediate resolution is
                                                                              crucial for hardware verification, as many behavioral specifi-
  Prompt for Design Patterns Summary                                          cations and protocol sequences exist precisely at this middle
  You are an expert hardware design engineer. Please analyze the following    level of abstraction.
  design specification and RTL code to identify and summarize key design         To effectively capture this intermediate information, we
  patterns, protocols, or verification-critical structures. Examples might    adopt a multi-scale hierarchical chunking strategy inspired
  include handshaking protocols, state machines, pipelines, arbiters, or
  clock domain crossings.                                                     by the work of Lewis et al. [33] and Borgeaud et al. [8],
  Design Specification: {spec text}                                           dividing documents into chunks of varying granularities that
  RTL Code: {rtl text}                                                        form what Robertson and Callan [50] refer to as a ”resolution
  Provide a concise summary (5-10 sentences) of the key design patterns
  and their verification implications.                                        pyramid.” At the finest resolution (50 tokens), the system
                                                                              captures precise signal definitions and immediate interactions.
                                                                              The middle resolutions (100-200 tokens) capture functional
Fig. 8. Prompt for identifying and summarizing key design patterns and        behaviors and protocol sequences that typically span multiple
protocols with verification implications.
                                                                              sentences or paragraphs. The coarsest resolutions (800-3200
tokens) preserve architectural relationships and system-level          An example of a generated path description is shown in
behaviors that might be missed in smaller chunks.                   Figure 10. This example shows a path starting from the
   To ensure coherent context across chunk boundaries, we           “baud limit” port in the UART module, traversing through
implement overlapping chunks with ratios of 0.2 and 0.4,            transmit and receive logic, and discovering critical signals
following the approach proposed by Dai and Callan [14]. This        through diverse relationship types. The description includes
overlapping strategy addresses the ”boundary fragmentation          the type of each node (e.g., “port”, “module”, “verifica-
problem” identified by Hearst [24], where critical information      tion point”, “protocol pattern”) and the module it belongs to,
can be split across adjacent chunks. By creating strategic          along with the varied relationships between consecutive nodes
overlaps, we ensure that semantically coherent units (like          (e.g., “drives”, “input to”, “involves”, “includes”). While our
descriptions of protocol sequences that might span multiple         current work focuses on representing paths as human-readable
paragraphs) remain intact in at least some retrieved chunks.        text, which we hypothesize is more natural for the LLM, future
   Our retrieval framework uses two complementary meth-             work could explore extracting subgraphs or motifs from the
ods for finding relevant context. First, we use TF-IDF to           knowledge graph.
convert text chunks into sparse vectors that emphasize rare,
                                                                    I. LLM-based Context Pruner
distinguishing terms. Second, we use Sentence Transformers
to generate dense semantic vectors that capture contextual             The pruner analyzes each context’s relevance, information
meaning. For retrieval, we use the signal name (e.g., “tx valid”    density, and complementarity with other selected contexts,
or “data ready”) as the query term. We compute cosine               considering factors like explicit mentions of the target signal,
similarity between this query and each chunk using both vector      descriptions of related signals, protocol specifications, and
representations independently, then combine the scores with         timing/behavioral constraints. As shown in Figure 11, the
an average. This dual approach balances exact signal name           LLM is prompted to act as an expert verification engineer,
matching with semantic relevance, allowing us to retrieve           receiving the original query, target signal name, and a set
context even when signal names are referenced indirectly.           of contexts with metadata (source type, retrieval score, etc.).
   To further refine the retrieval process, future enhancements     Crucially, the prompt instructs the LLM to select between a
could involve developing specialized embedding models fine-         minimum and maximum number of contexts of the given type,
tuned on hardware design corpora. Such models would be              explicitly encouraging the inclusion of even partially relevant
adept at capturing the unique linguistic patterns and termi-        information. The LLM outputs a list of indices indicating the
nologies prevalent in hardware design documents, thereby            selected contexts (e.g., “Selected contexts: [0, 2, 5]”). Our
improving retrieval accuracy. For instance, NV-Embed [32],          implementation defaults to a maximum of 50 contexts per type
a generalist embedding model, has demonstrated significant          and 100 total contexts, with a minimum of 2 contexts per type
improvements in embedding tasks by incorporating architec-          enforced whenever possible, promoting diversity.
tural innovations and specialized training procedures. Adapting
                                                                    J. Multi-Resolution Context Synthesis
similar techniques to create embeddings tailored for hardware
design verification could substantially enhance the perfor-            After pruning the contexts from various sources, the next
mance of the SSR component.                                         critical step is generating effective verification plans and
                                                                    assertions through Multi-Resolution Context Synthesis. This
H. Guided Random Walk with Adaptive Sampling (GRW-AS)               process, denoted as Di,j ← Ω(Cp , vi , j) in Algorithm 1, dy-
                                                                    namically constructs prompts that harmonize different context
   GRW-AS discovers semantically relevant paths through             types across multiple resolution levels.
the knowledge graph using biased random walks guided by                Our implementation assembles relevant contexts from SSR
verification priorities. Algorithm 3 outlines the core procedure,   (middle resolution) and GRW-AS (fine-grained resolution),
implementing the three key biases defined in Section III-E.         along with global design summaries (coarse resolution). For
                                                                    each signal, the system generates up to three distinct prompts
Algorithm 3 GRW-AS Path Discovery                                   (B = 3 in our implementation), each containing complemen-
Require: Knowledge graph G, Start node vs , signals V               tary context combinations to maximize coverage of verification
Ensure: Natural language path description L                         scenarios. These prompts respect a maximum token limit of
 1: P ← [vs ], v ← vs {Initialize path}
 2: while step ≤ budget and V ̸= ∅ do                               75% of the LLM’s context window, reserving space for the
 3:    N ← {u|(v, u) ∈ E} {Neighbor nodes}                          model’s response.
 4:    P ← [αI(u) + βD(u) + γN (u) ∀u ∈ N ]                            The two-stage verification process begins with natural lan-
 5:    v ′ ← sample(N , P) {Biased selection}                       guage (NL) plan generation, followed by SystemVerilog Asser-
 6:    P .append(v ′ ), v ← v ′                                     tion (SVA) synthesis. Figure 12 illustrates the prompt structure
 7:    if v ′ ∈ V then
 8:        V ← V \ {v ′ }                                           used for NL plan generation.
 9:    end if                                                          After generating NL plans, the system synthesizes formal
10: end while                                                       SVAs as shown in Figure 13. This stage uses the same context
11: L ← ConvertToNL(P ) {Natural Language (NL) description}         synthesis approach but adds signal-specific context and in-
12: return L
                                                                    context learning examples to guide correct assertion syntax.
                                                                     Prompt for LLM Context Pruner
 GUIDED RANDOM WALK FROM baud_limit (port)
 Located in module: baud_gen                                         You are an expert hardware verification engineer evaluating contexts to
 Path length: 57 nodes, discovered signals:                          be used in generating verification plans for signal ’{signal name}’.
 tx_busy, ce_16, new_rx_data, rx_data,                               QUERY: {query}
     new_tx_data, baud_clk, baud_freq, clock                         YOUR TASK: Select between {min selection} and {max selection}
                                                                     contexts of type ’{context type}’ that could help with verification.
                                                                     IMPORTANT NOTES:
 Signal flow path:                                                   - Select at least {min selection} contexts even if they seem only
   baud_limit (port in baud_gen) drives                              indirectly relevant
       baud_limit (port in uart_top)                                 - Consider both explicit mentions of ’{signal name}’ and general system
   baud_limit (port in uart_top) input to                            information
       uart_top (module)                                             - Partial information about interfaces, protocols, and system behavior is
   uart_top (module) part of                                         still valuable
       new_tx_data_assignment (assignment in                         - When in doubt, include rather than exclude contexts
       uart_top)                                                     CONTEXTS TO EVALUATE:
                                                                     [CONTEXT 0] {context 0}
   new_tx_data_assignment (assignment in
                                                                     —-
       uart_top) assigns to new_tx_data (port                        [CONTEXT 1] {context 1}
       in uart_top)                                                  —-
   new_tx_data (port in uart_top) involves                           ...
       data_stability (verification_point in                         SELECTION INSTRUCTIONS:
       uart_top)                                                     1. SELECT AT LEAST {min selection} CONTEXTS, even if only
   data_stability (verification_point in                             partially relevant
       uart_top) involves baud_clk (port in                          2. Focus on contexts that might help verify {signal name}
       uart_top)                                                     3. Output your selection using ONLY the format ”Selected contexts: [list
                                                                     of indices]”
   baud_clk (port in uart_top) includes
                                                                     For hardware verification, we need information about:
       rtl_111 (protocol_pattern in uart_top)                        - Signal connections and dependencies
   rtl_111 (protocol_pattern in uart_top)                            - Timing requirements
       found in uart_top (module)                                    - Protocol details
   ...                                                               - State transitions
   data_buf_assignment (assignment in                                - Interfaces
       uart_top) used in tx_data (port in
       uart_top)
   tx_data (port in uart_top) drives tx_data                       Fig. 11. Prompt template for the LLM-based Context Pruner, showing how
       (port in uart_tx)                                           contexts from different sources are presented for evaluation.
   tx_data (port in uart_tx) involves
       data_stability (verification_point in
       uart_tx)
                                                                     Prompt for NL Test Plan Generation
   data_stability (verification_point in                             Generate natural language test plans for signal ’{signal name}’.
       uart_tx) involves clock (port in                              Relevant Context: {global summary}
       uart_tx)                                                      RAG Context: {rag context}
   clock (port in uart_tx) drives clock (port                        GRW-AS Context: {grw context}
        in uart_rx)                                                  CRITICAL - Valid Signal Names (USE ONLY THESE SIGNALS):
   ...                                                               {valid signals}
   rx_data (port in uart_rx) includes rtl_108                        Examples:
        (protocol_pattern in uart_rx)                                {examples}
   rtl_108 (protocol_pattern in uart_rx)                             Generate diverse test plans based on the given information. Each test
                                                                     plan should be on a new line and start with ’Plan: ’.
       includes new_rx_data (port in uart_rx)
   ... [truncated]
                                                                   Fig. 12. Prompt template for natural language verification plan generation,
                                                                   showing how multi-resolution contexts are integrated to guide the generation
     Fig. 10. Example of a path description generated by GRW-AS.   of signal-specific test plans.



                          A PPENDIX B                              the subsequent KG refinement from RTL is remarkably effi-
                    E FFICIENCY A NALYSIS                          cient at less than 0.4% of total runtime for all designs.
                                                                      The LLM-based components show good scalability. The
   We analyze A SSERTION F ORGE’s computational efficiency         dominant computational factor remains Jasper formal ver-
across the four designs. Table IV summarizes the time dis-         ification (57-78% of runtime), which is an inherent cost
tribution across major workflow stages, demonstrating our          in any verification approach. This verification phase could
framework’s practical scalability.                                 be parallelized in future implementations to further reduce
   Our analysis reveals that A SSERTION F ORGE introduces rea-     overall time, though our current implementation evaluates each
sonable computational overhead while enabling comprehen-           assertion sequentially.
sive verification. While the initial Knowledge Graph construc-        It’s worth noting that actual running times may vary based
tion from specifications varies across designs (2.72-10.65%),      on factors such as the LLM backend engine speed, server
                                                                 TABLE IV
                               T IME DISTRIBUTION ACROSS VERIFICATION STAGES FOR DIFFERENT HARDWARE DESIGNS

                              Component                        APB       ETHMAC     OPEN MSP430     SOCKIT     UART
                              KG Construction from Spec       4.08%        10.65%       2.72%        0.62%     3.15%
                              KG Refinement from RTL          0.01%         0.07%       0.33%        0.01%     0.07%
                              Context Summarization           1.34%         0.00%       3.35%        1.17%     3.65%
                              NL Plan Generation              8.73%         5.12%       9.97%        3.97%    14.41%
                              SVA Synthesis                  12.14%         5.83%      14.03%        4.48%    20.42%
                              Jasper Verification            73.26%        77.82%      69.31%       90.34%    57.00%
                              Other Operations                0.44%         0.51%       0.29%        0.41%     1.30%
                              Total Runtime                  1h 47m        1h 25m      4h 12m       4h 14m    52m 20s



  Prompt for SVA Generation                                                       COI Toggle Coverage adds another dimension by tracking
                                                                               signal transitions within the assertion’s reach, helping us find
  Generate SystemVerilog Assertions based on the following information:        static logic that other metrics might overlook. These four
  Relevant Context: {global summary}
  {signal specific summary}                                                    metrics together give us a balanced view of assertion quality
  RAG Context: {rag context}                                                   since each looks at different verification aspects. For example,
  GRW-AS Context: {grw context}                                                an assertion might hit most statements but miss important
  Natural Language Test Plans for signal ’{signal name}’:
  Plan 1: {plan 1}                                                             branching logic, or it might check branches without exercising
  Plan 2: {plan 2}                                                             key signals.
  Plan 3: {plan 3}
  Examples:
  {examples}                                                                   B. Impact of Prompt Count Parameter
  Generate one SVA for each of the provided natural language test plans.
  Enclose each SVA in triple backticks (“‘) and prefix it with ’SVA:’.            We conducted a parameter sensitivity study on the max-
                                                                               imum prompt count parameter B, which controls how many
                                                                               distinct prompts are generated per architectural signal. Table V
Fig. 13. Prompt template for SVA generation, including multi-resolution        shows the results of varying B from our baseline value of 3
contexts, signal-specific natural language plans, and examples demonstrating
the expected SVA format.
                                                                               to higher values of 6 and 9 for the UART design.
                                                                                  Our results demonstrate that increasing the maximum
                                                                               prompt count B generally leads to more proven assertions,
load, and hardware configuration used for verification. The                    with the total count rising from 27 at B = 3 to 61 at
figures presented here represent typical performance observed                  B = 9. This improvement is expected, as each additional
in our experimental setup and are intended to illustrate the rel-              prompt contains complementary context combinations that can
ative distribution of computational effort rather than absolute                capture different verification scenarios. However, we observe
benchmarks. In practice, users may observe faster or slower                    that the relationship is not linear, with diminishing returns as
performance depending on their specific environment and the                    B increases.
optimizations applied to each component.                                          Interestingly, we observe that coverage metrics do not
                                                                               consistently improve with increasing B. For example, COI
                          A PPENDIX C                                          Functional Coverage actually decreases slightly from 88.82%
                M ORE D ETAILS ON E XPERIMENTS                                 at B = 3 to 83.93% at B = 6 before recovering to 89.14% at
                                                                               B = 9. This non-monotonic behavior suggests that while more
A. Cone-of-Influence Coverage Metrics                                          prompts generally lead to more assertions, the quality and
   When measuring verification quality, we need to look be-                    diversity of those assertions depend on complex interactions
yond just counting assertions to examine how well they actu-                   between the contexts selected for each prompt.
ally test the design’s behavior. We chose Cadence JASPER’s                        In practice, the choice of B represents a trade-off between
cone-of-influence (COI) coverage metrics as our quality indi-                  verification thoroughness and computational resources. Larger
cator because they offer deeper insights into each assertion’s                 values yield more comprehensive verification but incur higher
effectiveness [10].                                                            computational costs for both LLM inference and assertion
   We use four complementary COI metrics to capture different                  verification. Based on our experiments, B = 3 offers a rea-
verification aspects. COI Statement Coverage shows what                        sonable balance for practical applications, while higher values
percentage of RTL statements within the assertion’s influence                  may be justified for critical components requiring exhaustive
are tested, giving us basic code coverage. COI Branch Cov-                     verification.
erage reveals how well the assertion tests conditional paths
                                                                               C. Testbench SVAs Generated by LLM on the OPEN MSP430
in the logic, which is essential for verifying how the design
                                                                               Design
makes decisions. COI Functional Coverage gauges whether
the assertion truly verifies high-level requirements rather than                  Figure 14 demonstrates SVAs generated by A SSERTION -
just checking implementation details.                                          F ORGE for the OPEN MSP430 microcontroller, spanning clock
                                                           TABLE V
                            E FFECT OF VARYING MAXIMUM PROMPT COUNT PARAMETER B ON THE UART DESIGN .

                                                                                COI Coverage (%)
                         B Value           #SVA   #SynC   #Proven
                                                                    Statement   Branch   Functional   Toggle
                         B = 3 (default)   253     132      27        84.62      84.78     88.82      90.41
                         B=6               394     255      53        84.62      84.78     83.93      83.64
                         B=9               397     197      61        84.62      84.78     89.14      90.87


domains, DMA behavior, interrupt handling, and debug in-
terfaces. These automatically synthesized assertions exhibit
three key characteristics: temporal correctness (sequencing
requirements), protocol compliance (interface adherence), and
data integrity (preventing unknown states).
   These SVAs exhibit several features including multi-clock
checks (A0), protocol timing requirements (A49), error propa-
gation (A110), and cross-domain triggers (A23). This compre-
hensive coverage stems from the KG’s unified representation
of both specification requirements and RTL implementation
details.
   The guided random walks (GRW-AS) algorithm was partic-
ularly effective at discovering relationships between seemingly
unrelated signals like “cpu en” and “dco wkup” by traversing
the “openMSP430.v” connectivity paths. Additionally, exam-
ining the RTL implementation revealed critical behaviors not
explicitly documented in the specification, such as the timing
relationship between “reset n” and “puc rst” (A283) and the
exact power management protocol between “dco enable” and
“dco wkup” (A23).
   Despite the improvements in assertion quality and coverage
achieved by A SSERTION F ORGE, Table II shows coverage is
still not 100% complete. Future work includes leveraging
existing assertion libraries and learning from well-verified de-
signs via RAG or in-context learning techniques. Additionally,
iterative KG refinement, hardware-specific LLM fine-tuning,
and implementing verification feedback loops could further
enhance coverage.
Selected SVAs for OPEN MSP430 Generated by A SSERTION F ORGE
Clock Domain Validation:                                                  Memory Access Validation:
// A0: ACLK/SMCLK synchronization                                         // A110: DMA address bounds
@property p0                                                              @property p110
@(posedge smclk or aclk)                                                  @(posedge mclk) (dma_en &&
((smclk_en && !aclk_en) |-> (aclk == smclk));                             (dma_addr > ’hFFFF)) |-> (dma_resp == 1’b1);
Reset Behavior:                                                           Debug Interface Protocol:
// A22: Reset propagation                                                 // A49: I²C SDA hold time
@property p22                                                             @property p49
@(posedge mclk) (puc_rst) |-> ##1 !aclk_en;                               @(posedge dbg_i2c_scl)
                                                                          (dbg_en && dbg_i2c_sda_in |-> dbg_i2c_sda_out);
DMA Transaction Safety:
                                                                          Power Management:
// A109: Valid DMA input data
@property p109                                                            // A23: DCO wakeup trigger
@(posedge mclk) (dma_en && dma_we)                                        @property p23
|-> (dma_din !== ’hX);                                                    @(posedge mclk)
                                                                          (!dco_enable && cpu_en) |-> dco_wkup;
Interrupt Handling:
                                                                          Asynchronous Event Handling:
// A180: IRQ-ACK consistency
@property p180                                                            // A231: NMI to handler mapping
@(posedge mclk) (irq == 0) |-> irq_acc == 0;                              @property p231
                                                                          @(posedge mclk)
Clock Gating:                                                             disable iff (puc_rst) $rose(nmi)
// A307: SMCLK stability                                                  |-> $rose(cpu.NMI_handler);
@property p307                                                            Reset Assertion:
@(posedge mclk) (smclk_en && cpu_en)
|-> $isunknown(smclk) == 0;                                               // A283: Reset pin behavior
                                                                          @property p283
                                                                          @(posedge mclk)
                                                                          (reset_n == 1’b0) |-> (puc_rst == 1’b1);


       Fig. 14. Representative SVAs for OPEN MSP430 demonstrating A SSERTION F ORGE’s ability to capture diverse verification concerns..
