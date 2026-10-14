                                                           To appear at the IEEE International Conference on IC Design and Technology 2026 (ICICDT),
                                                                                      June 22 - 24, 2026, Dresden, Germany


                                               Knowledge Graphs, the Missing Link in Agentic
                                                       AI-based Formal Verification
                                          Vaisakh Naduvodi Viswambharan1 , Keerthan Kopparam Radhakrishna1 , Deepak Narayan Gadde1 , Aman Kumar2
                                                                                      1 Infineon Technologies Dresden AG & Co. KG, Germany
                                                                               2 Infineon Technologies Semiconductor India Private Limited, India



                                           Abstract—Recent advances in Large Language Models (LLMs)                         processing, staged prompting [2], [7] and RTL-derived prompt
                                        have enabled workflows that generate SystemVerilog Assertions                       enrichment [8], [9]. Common strategies include schema-guided
                                        (SVAs) from natural-language specifications, with the potential                     normalization [3] and retrieval-augmented context selection
                                        to accelerate Formal Verification (FV). However, high-quality
arXiv:2605.06434v1 [cs.AI] 7 May 2026




                                        assertion synthesis remains challenging because specifications are                  [10], [11]. However, studies report that these assertions show
                                        often ambiguous or incomplete and critical micro-architectural                      syntax and semantic errors requiring iterative correction and
                                        details reside in the Register Transfer Level (RTL). Many existing                  manual triage [3], [12], motivating representations with explicit,
                                        approaches treat the specification and RTL as loosely structured                    persistent links across requirements, RTL semantics, generated
                                        text, which weakens specification-to-RTL grounding and leads to                     properties, and verification outcomes.
                                        semantic mismatches and frequent syntax failures during formal
                                        parsing and elaboration. This work addresses these limitations                         KG-based structuring offers more explicit grounding. Asser-
                                        with a verification-centric Knowledge Graph (KG) constructed                        tionForge [6] builds a KG linking specification artifacts to the
                                        from structured Intermediate Representations (IRs) extracted from                   RTL hierarchy and signals for structured context Yet, formal-
                                        the specification, RTL, and formal-tool feedback, including syntax                  tool outcomes, including CEXs, and coverage gaps, are typically
                                        diagnostics, Counterexamples (CEXs), and coverage reports. The                      not represented as queryable KG content, limiting traceability
                                        KG links requirements, design hierarchy, signals, assumptions,
                                        and properties to provide traceable, design-grounded context for                    and hindering systematic closed-loop refinement.
                                        generation. A multi-agent workflow queries and updates this KG                         To address these limitations, this work proposes a verification-
                                        to generate SVAs and to drive three refinement loops: syntax repair                 centric methodology that builds a KG from structured IRs
                                        guided by tool diagnostics, CEX-guided correction using trace                       extracted from the specification, RTL, and formal-tool feedback.
                                        links, and coverage-directed property augmentation. Evaluation                      LLM agents query and update the KG to support design-
                                        across seven benchmark designs indicates that KG-based context
                                        retrieval improves specification-to-RTL grounding and consistently                  grounded property generation and three refinement loops: syntax
                                        produces compilable SVAs with low syntax-repair overhead. The                       repair guided by parser and elaboration diagnostics, CEX-
                                        approach achieves formal coverage ranging from 78.5% to 99.4%,                      guided correction using traces, and coverage-directed augmen-
                                        though convergence exhibits design dependence with complex tem-                     tation from tool-reported gaps.
                                        poral and arithmetic reasoning remaining challenging for current
                                                                                                                               The main contributions of this paper are as follows:
                                        LLM capabilities.
                                           Index Terms—Formal Verification, Knowledge Graphs, Agentic                          • A verification-centric KG construction based on structured
                                        AI, LLMs                                                                                 IRs, integrating specification intent, RTL structure, gener-
                                                                                                                                 ated properties, and formal-tool results.
                                                                I. I NTRODUCTION
                                                                                                                               • A multi-agent workflow that uses KG-grounded context to
                                           FV offers strong correctness for RTL designs by proving that                          generate and refine SVAs with traceability across require-
                                        key behaviors hold across all reachable states, including corner                         ments, design elements, properties, and results.
                                        cases that are difficult to cover with simulation. Central to FV                       • An evaluation on open-source designs quantifying the
                                        is using SVAs to encode intended behavior as formal properties.                          impact of KG-grounded context on property generation
                                        However, writing accurate assertions requires deep understand-                           effectiveness, syntactic validity, and CEX refinement.
                                        ing of both the specification and RTL implementation, making
                                        assertions time-consuming and error-prone.                                                                     II. R ELATED W ORK
                                           Advances in LLMs enable automated synthesis of SVAs from
                                                                                                                               In LLM-assisted SVA generation, prior works differ in rep-
                                        natural-language specifications [1], [2], [3], [4], [5]. To produce
                                                                                                                            resenting specification intent and design context; key challenge
                                        semantically correct SVAs, models need context linking to the
                                                                                                                            is grounding requirements and RTL semantics, while enabling
                                        relevant RTL hierarchy, and signal interactions [6]. Accord-
                                                                                                                            iterative refinement from formal verification outcomes.
                                        ingly, prior work builds context through structured specification
                                                                                                                               Specification-driven approaches synthesize SVAs from
                                           Under grant 101194371, Rigoletto is supported by Chips Joint Undertaking         natural-language specifications, but are limited by ambiguous
                                        and its members, including top-up funding by the National Funding Authorities       and missing behavioral constraints [1], [2]. To improve reli-
                                        from involved countries. Rigoletto is also funded by the Federal Ministry of
                                        Research, Technology and Space under the funding code 16MEE0548S. The               ability, many systems structure specifications before genera-
                                        responsibility for the content of this publication lies with the author.            tion: ChIRAAG [3] uses JSON schema-guided representations,



                                        ©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
                                        reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                                                                       reuse of any copyrighted component of this work in other works.
                            Inputs                                                  Intermediate                      Requirement-based Knowledge Graph                                      Multi-agent systems                                                                     Multi-agent systems                                                                              Requirement-based Knowledge Graph
                                                                                 Representations (IRs)                   for property generation agents                                    for property generation                                                                for syntax error correction                                                                          after initial formal verification run
                      Specification
                                                                                    run_context.json
   # FIFO Specification
                                                                                                                                                                                                     sva_lead_agent             code_extractor                      syntax_validator                                    syntax_fixer               syntax_analyzer
   ## 1. Overview
   ---------------------------------------------------------
   ## 2. Parameters                                                                  spec_doc.json                                                                                                                                     Properties that cannot be fixed after three correction attempts are commented out
   ---------------------------------------------------------                                                                                                                                            spec_analyst
   ## 3. Interface Signals
   ---------------------------------------------------------                                                                                                                                                                                               Update
   ## 4. Internal Architecture
   ---------------------------------------------------------     Processed          spec_chunks.json                          Knowledge graph                                                                                                                                                                                          Yes
                                                                                                                               Knowledge graph                    Prompt per
   ## 5. Functional Requirements
                                                                 specification                                                                                                                                                                             SystemVerilog Assertions
   ---------------------------------------------------------                                                                                                      requirement                            sva_author           Properties per
                                                                 for IR                                                                                                                                                                        module fifo_sva ();
                                                                                                                                                                                                                                                                                                                                       Syntax error(s)         No
   ## 6. Timing Requirements
                                                                                                         nodes.csv,                                                                                                           requirement
   ---------------------------------------------------------                                                                                                                                                                                   //---------------------------------macros---------------------------                                                                                 Knowledge graph
   ## 7. Assumptions & Environment                                                 requirements.json     edges.csv                                                                                                                             property no_operations_during_reset;                                                                                                                  Knowledge graph
   ---------------------------------------------------------                                                                                                                                                                                   @(posedge `clk) (!`reset_n) |-> (!`wr_en && !`rd_en);
                                                                                                                                                                                                                                               endproperty
                                                                                                                                                                                                       sva_reviewer                            assert property(no_operations_during_reset);
                                                                                                                                                                                                                                               //---------------------------------properties-----------------------                                               Update
              RTL implementation                                                      testplan.json
                                                                                                                                                                                                                                               endmodule
                                                                                                                                                                                                                                                                                                                                        Formal tool
  module fifo #(
   WIDTH = 8,                                                                                                                                                                                                                                  bind fifo fifo_sva inst_fifo_sva (.*);
   DEPTH = 32,
                                                                                                                                                                                                                                                                                                                            Intermediate Representations (IRs)
     LOG2DEPTH = $clog2(DEPTH)
                                                                                     scenarios.json                                                                                                     sva_patcher
  )(                                                             Processed                                                                                                                                                             Update
     clk, reset_n, wr_en, wr_data, full,
     rd_en, rd_data, empty                                       using RTL                                                                                                                                                                                              coverage_metrics                               cex_cases              formal_results
  );                                                             parser
                                                                                   design_model.json
  //--------------------------logic---------------------------
  endmodule                                                                                                                       Rulebooks                                                           code_extractor
                                                                                                                                                                                                                                          properties                    updated scenarios                               tracelinks
                                                                    RTL metadata extracted from parser
                                                                                                                                                                                                                                                                                                                                                                                    nodes.csv, edges.csv



                                                                                       (a) Knowledge Graphs and multi-agent systems used for property generation and syntax error correction
             Requirement-based Knowledge Graph                                                       Multi-agent systems for                                                                Multi-agent systems                                                                                                                                                                                                Multi-agent systems
                                                                                                                                                                                                                                                                                                                       Formal tool                       SystemVerilog Assertions
              after initial formal verification run                                              counterexample (CEX) correction                                                         for syntax error correction                                                                                                                                                                                        for coverage improvement
                                                                                                                                                                                                                                                                                                                                                      module fifo_sva ();

                                                                                                                                                                                                                                                                                                                                                      //--------------macros-------------
                                                                                                             vcd_parser              code_extractor                        syntax_validator                             syntax_fixer                syntax_analyzer                                 Yes                                                                                        Properties          cov_lead_agent
                                                                                                                                                                                                                                                                                                                                                      //------------properties-----------
                                                                                      Prompt per                                                                                                                                                                                                                      Syntax error(s)
                                                                                      requirement                                                                                                                                                                                                                                                     endmodule
                                                                                                                                                  Properties that cannot be fixed after three correction attempts are commented out                                                                                              No                   bind fifo fifo_sva inst_fifo_sva (.*);
                                                                                                                                                                                                                                                                                                                                                                                                                       cov_analyzer
                                                                                                           spec_assertion
                                                                                                             _analyzer                                         Update                                                          Yes
                                       Knowledge graph
                                        Knowledge graph
                                                                                                                                                          SystemVerilog Assertions                                                                                      No
                                                                                                                                                 module fifo_sva ();                                                            Syntax error(s)
                                                                                                                                                 //---------------------------------macros---------------------------
                                                                                                                                Properties per                                                                                                                                                                                                                                                                         cov_processor
                                                                                                            rtl_analyzer                         property no_operations_during_reset;
                                                                                                                                                 @(posedge `clk) (!`reset_n) |-> (!`wr_en && !`rd_en);
                                                                                                                                requirement                                                                                                    Update
                                                                                                                                                 endproperty                                                                                                                               Update
                                                                                                                                                 assert property(no_operations_during_reset);
                                                                                                                                                 //---------------------------------properties-----------------------              Formal tool                                                                                                                                                 Prompt
                                                                                                                                                 endmodule
                                                                                                                                                 bind fifo fifo_sva inst_fifo_sva (.*);
                                                                                                              cex_fixer                                                                                                           Intermediate Representations (IRs)                                                                                                                                                   cov_improver
                                                                                                                                                    Update
                                                                                                                                                                                             coverage_metrics                 cex_cases                 formal_results

                                                  Rulebooks                                                                                                                                                                                                                                          nodes.csv
                                                                                                           code_extractor                                         properties                       updated scenarios              tracelinks                                                                                                                                                                       code_extractor
                                                                                                                                                                                                                                                                                                     edges.csv

                                                                                                                                                                                                                                                                                                                                             Final Knowledge Graph



                                                                 (b) Knowledge Graphs and multi-agent systems used for CEX correction, coverage improvement and syntax error correction
                    Fig. 1. End-to-end workflow of the proposed approach. NetworkX is used for KG construction, and PyVis provides interactive HTML visualization.

AssertLLM [2] decomposes extraction and synthesis while                                                                                                                                                                     ification planning, assertion generation, formal proving, and
Spec2Assertion [7] improves functional correctness via pro-                                                                                                                                                                 coverage evaluation, yet formal-tool outputs remain transient
gressive regularization and structured reasoning yet remaining                                                                                                                                                              rather than persistent, queryable artifacts.
largely pre-RTL. These approaches improve consistency but                                                                                                                                                                      Overall, prior work improves SVA generation via structured
struggle when micro-architectural details are absent.                                                                                                                                                                       prompting, retrieval, and agentic decomposition but traceability
   In contrast, RTL-driven approaches use static analysis of im-                                                                                                                                                            remains weak without structured, queryable tool outputs. Thus,
plementation artifacts to guide assertion generation, improving                                                                                                                                                             this work introduces a verification- centric KG constructed
signal relevance but risking intent drift without explicit code                                                                                                                                                             from structured IRs spanning specification intent, RTL structure,
links [8], [9]. Hybrid approaches connect intent and implementa-                                                                                                                                                            generated properties, and formal-tool feedback. This founda-
tion more explicitly: AssertionForge [6] constructs a KG linking                                                                                                                                                            tion enables multi-agent generation and closed-loop refinement
specification artifacts to the RTL hierarchy and signals for struc-                                                                                                                                                         driven by syntax diagnostics, CEXs, and coverage gaps, with
tured context. Retrieval augmentation and structured prompting                                                                                                                                                              traceability from requirements to assertions and formal out-
further focus models on relevant context: Retrieval Augmented                                                                                                                                                               comes.
Generation (RAG)-based approaches retrieve targeted fragments
to reduce hallucinations [10], and LISA [11] combines retrieval                                                                                                                                                                                                                                                       III. M ETHODOLOGY
with structured reasoning to improve temporal correctness and                                                                                                                                                                    The workflow is organized into four layers:
reduce retries. While effective, these methods rely on complete                                                                                                                                                                  (i) Inputs: specification, RTL, configuration, and agents
cross-artifact links between requirements, signals, and behav-                                                                                                                                                                  (ii) Typed JSON IRs: normalize requirements, RTL structure,
iors.                                                                                                                                                                                                                                properties, and verification outcomes
   Despite these advances, studies still report recurring syntax                                                                                                                                                               (iii) Runtime KGs: retrieves localized context neighborhoods
errors and semantic mismatches requiring iterative fixes [12].                                                                                                                                                                       bounded by task relevance and provides traceable, design-
Some systems add limited feedback loops, such as simulation-                                                                                                                                                                         grounded context
or test-driven repair prompting [3], [13]. Saarthi [4] advances                                                                                                                                                                (iv) Agent orchestration: routes property generation,
with an agentic, end-to-end formal workflow coordinating ver-                                                                                                                                                                        syntax/CEX repair, and coverage improvement loops



©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                               reuse of any copyrighted component of this work in other works.
                                                                             TABLE I
                                         Intermediate Representation artifacts and their roles in the verification workflow

 IR Artifact           Purpose
 spec_chunks.json      Hierarchical specification decomposition with heading structure, semantic tags, enabling targeted context retrieval
 requirements.json     Extracted requirements with identifiers, natural language text, categories, priorities, traceability to specification chunks
 testplan.json         Per-requirement verification plans, observable signals, stimulus-response behaviors, timing constraints
 design_model.json     RTL metadata from formal tool analysis: module hierarchies, ports (direction, bit-width), signals, FSM encodings, parameters
 properties.json       Generated SVA code with property identifiers, requirement traceability, type classification, line mappings
 tracelinks.json       Mappings encoding requirement-to-specification, property-to-requirement, property-to-coverage relationships for bidirectional
                       traceability
 formal_results.json   Per-property outcomes with formal status (proven, CEX, vacuous), proof depth, runtime, diagnostic artifacts (VCD)
 cex_cases.json        Counterexample tracking with property identifiers, VCD paths, failure line numbers, correction attempt history for iterative
                       debugging
 coverage_metrics.json Aggregated statistics: reachability percentages, proof core ratio, vacuity counts, dead code classifications driving coverage
                       iterations
 run_context.json      Execution snapshot with run identifiers, file paths, iteration counts, tool versions, timestamps, configuration
 nodes.csv             Graph node export with unique IDs, type labels (spec_chunk, requirement, property, formal_result), run IDs, JSON attributes
 edges.csv             Graph edge export with source/destination IDs, relationship types (derives_from, validates, proves, fails, covers), run IDs,
                       JSON attributes

      while preserving traceability from requirements to                            also includes tool outputs such as compilation diagnostics, CEX
      properties and outcomes                                                       traces, and coverage gap reports. RTL metadata is indexed by
   In each run, requirements and RTL metadata are extracted                         hierarchical signal identifiers, enabling automatic mapping from
into typed JSON IRs, followed by property generation and                            specification-level signal mentions to RTL hierarchical paths.
formal verification. Syntax and CEX correction along with                           B. Multi-Agent Orchestration
coverage improvement are triggered based on tool outputs and
                                                                                       Verification is decomposed into specialized agents to separate
updated IR artifacts as shown in Fig. 1.
                                                                                    concerns that would be difficult for a single monolithic prompt:
               Listing 1: IR core entity types and relationships                    specification interpretation, RTL signal grounding, temporal
     Entities:                                                                      logic synthesis, and tool-driven debugging. Each agent operates
     SpecChunk        - specification fragments                                     with a KG-bundled context neighborhood appropriate to its
     Requirement      - functional requirements
     Property         - generated SVA code                                          task, emits structured updates to IR objects and property code,
     FormalResult     - verification outcomes                                       and hands off to the next agent through explicit coordination
     CoverageMetrics - RTL coverage tracking
     Relationships:                                                                 protocols. This enables deterministic routing and complete au-
     Requirement     --> SpecChunk (provenance)                                     ditability of the verification workflow. Fig. 1a illustrates the
     Property        --> Requirement (validation)
     Property        --> FormalResult (outcomes)                                    agent interactions during property generation, while Fig. 1b
     Property/RTL    --> CoverageMetrics (coverage)                                 shows the CEX correction and coverage improvement systems.
                                                                                       1) Property Generation Agents: Requirements are trans-
A. Intermediate Representations and Knowledge Graphs                                lated into SVA properties through a multi-agent workflow.
   Verification artifacts are stored as typed JSON IRs to enable                    The sva_lead oversees the property generation process by
deterministic orchestration and cross-iteration comparison. Ta-                     coordinating agents and ensuring verification strategy alignment
ble I enumerates the IR artifacts, and Listing 1 summarizes the                     with requirements. RTL metadata extracted from the parser pop-
core entity types and trace links used for requirement-centric,                     ulates the design_model IR artifact with module hierarchies,
property-centric, and coverage-centric retrieval.                                   ports, signals, and parameters. For each requirement, the KG
   The runtime KG is constructed from nodes.csv and                                 provides a neighborhood containing the requirements, parent
edges.csv exported from the IR artifacts. The KG acts                               specification fragment, RTL signals, and rulebook guidelines.
as an artifact registry with property-granular updates: when                        The spec_analyst decomposes requirements into testable
a property is regenerated or corrected, only its downstream                         conditions: trigger events, responses, timing constraints, and
evidence (for example, formal results, CEXs, and coverage                           exceptions. The sva_author translates these into SVA syntax
records) is invalidated and recomputed, enabling focused re-                        using assertions, temporal operators, and assume directives.
verification while preserving end-to-end traceability.                              The sva_reviewer validates against specification adherence
   The runtime KG constructs bounded context by traversing                          and rulebooks. The sva_patcher corrects properties based
from a task anchor node, typically a requirement or a property.                     on sva_reviewer feedback. The code_extractor as-
For property generation, the neighborhood includes the target                       sembles approved properties into a SVA file with macros and
requirement, its parent specification fragment, relevant RTL                        property declarations.
objects (module scope and signals), and related properties vali-                       2) Syntax Correction Agents: LLM-generated syntax errors
dating sibling requirements. For repair tasks, the neighborhood                     in properties are addressed through a multi-agent correction



©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                               reuse of any copyrighted component of this work in other works.
                                                                                TABLE II
                                                                 Evaluation of the proposed methodology
    Evaluation Category           Evaluation Metric          FIFO [14]     Lemming [15]       ALU [15]     CICD [15]       BST [15]      TTC Counter [15]       CSR [15]
                             #Properties (T | P | F)         26 | 17 | 9     51 | 50 | 1       2|1|1       15 | 12 | 3    34 | 18 | 16     41 | 30 | 11        42 | 26 | 16
   Property generation       #Vacuous properties                  0               0               0             0               7                2                   5
                             %Reachable RTL coverage            88.2            94.7            95.8          72.6            73.1             59.0                33.8
   Syntax correction         #Fix attempts                        1               0               3             1               1                1                   1
   CEX correction            #Properties (C | NC)               8|1             0|1             0|1           0|3            0 | 16           0 | 11              0 | 16
                             #Properties (T | P | F)         26 | 25 | 1     51 | 50 | 1       2|1|1       15 | 12 | 3    37 | 20 | 17     41 | 30 | 11        42 | 32 | 10
   Coverage improvement      #Vacuous properties                  1               0               0             0               7                2                   5
                             %Reachable RTL coverage            88.2            94.7            95.8          71.8            73.1             59.0                84.6
   End-to-end results        %Formal coverage                   93.8           97.32            99.41        90.83           86.46            82.98               93.82
   Knowledge Graph size      #Nodes | #Edges                 231 | 1054     402 | 2157        116 | 396    165 | 688      299 | 1107        302 | 1522         338 | 1397

T - Total, P - Passed, F - Failed, C - Corrected, NC - Not Corrected, FIFO - First In First Out, ALU - Arithmetic Logic Unit, CICD - Cascaded Integrator-Comb Decimator, BST -
Binary Search Tree, TTC Counter - Time-to-Completion Counter, CSR (CSR APB Interface Design) - Control and Status Register Advanced Peripheral Bus Interface


strategy. After compilation, the syntax_analyzer parses                                 The cov_improver generates targeted properties using cover
error messages and attributes them to specific properties. The                          directives for reachability and assertions for correctness. The
syntax_fixer applies deterministic repairs for well-known                               code_extractor assembles coverage properties for iterative
patterns (undeclared identifiers wrapped with backtick macro                            formal runs.
syntax or hierarchical paths, undefined macros auto-resolved
by adding definitions) and handles complex errors (temporal                                                              IV. E VALUATION
operators, sequence expressions, type mismatches) using com-
pilation diagnostics, property context, requirement text, and                              The system was evaluated on seven benchmark designs:
RTL signal declarations. The syntax_validator performs                                  FIFO, Lemming, ALU, CIC Decimator, Binary Search Tree
isolated testing in a temporary wrapper to prevent cascading                            (BST), TTC Counter, and CSR APB Interface, using the multi-
errors before reintegration. The code_extractor extracts                                agent flow with the GPT-5.2 model and Cadence JasperGold for
the corrected code. Properties receive maximum three attempts;                          FV, as shown in Table II. Overall, the workflow consistently
persistent failures are disabled and logged for manual review.                          produces runnable SVA at scale. Syntax correction remains low
                                                                                        effort across the completed designs, which indicates that KG-
   3) Counterexample Correction Agents: Properties failing                              grounded context, especially deterministic signal and hierarchy
FV produce CEXs indicating RTL bugs or property is-                                     resolution via the design_model IR, reduces common front-
sues. VCD waveforms, failure timestamps, and signals are                                end issues such as undeclared identifiers, macro mismatches,
extracted and stored as FormalResult IR entities. The                                   and incorrect hierarchical references.
vcd_parser extracts temporal behavior at failure points.                                   The main differences across designs appear after compilation,
The spec_assertion_analyzer classifies root causes:                                     during CEX-based refinement and coverage improvement. FIFO
RTL bugs, over-specification, missing assumptions, or under-                            and CIC Decimator benefit from iterative refinement, with
specification. The rtl_analyzer examines RTL source code                                improved pass rates and higher end-to-end formal coverage after
and traces logic paths; genuine bugs are documented for RTL                             the correction loops. This suggests that many initial failures
correction. The cex_fixer corrects property issues by ad-                               are caused by local issues such as missing guards, overly
justing constraints, adding assumptions, or strengthening asser-                        strong assumptions, or boundary-condition constraints, which
tions. The code_extractor assembles corrected properties                                can be corrected using retrieved context and CEX evidence.
for isolated verification before reintegration. Properties receive                      TTC Counter shows moderate convergence: a non-trivial frac-
maximum three attempts, with persistent failures flagged for                            tion of initially failing properties become provable after CEX
manual analysis.                                                                        correction, but overall coverage remains lower than the strongest
   4) Coverage Improvement Agents: Syntactically correct                                benchmarks, consistent with limited reachable-state coverage in
properties may still achieve inadequate coverage. Formal tool                           the design. CSR APB Interface shows a different pattern: initial
reports are parsed to extract coverage metrics: unreachable                             property quality is lower, but the coverage loop yields a clear
RTL statements, dead code regions and vacuous properties,                               improvement in passing properties, indicating that additional
stored as CoverageMetrics IR entities. The cov_lead_agent                               targeted properties help exercise previously uncovered behavior.
coordinates coverage improvement by prioritizing gaps in func-                             In contrast, Lemming and ALU show limited benefit from
tional paths and distinguishing intentionally unreachable de-                           automated correction. Most properties pass early, and the re-
fensive code. The cov_analyzer performs root cause anal-                                maining failures do not improve significantly, suggesting that the
ysis, examining RTL implementation to identify conditions                               unresolved cases require complex temporal reasoning such as
for unreachable code and querying the KG to determine if                                reset behavior, FSM transition intent, or multi-cycle arithmetic
existing properties or assumptions prevent those combinations.                          meaning. BST remains the most difficult: many properties
The cov_processor links gaps to requirements through                                    are generated, but a large fraction remain failing and CEX
KG traversal, identifying under-verified requirement aspects.                           correction does not converge, which is consistent with the need



©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                               reuse of any copyrighted component of this work in other works.
for global data-structure invariants and inductive reasoning that                   [11]    S. Paul et al., “LISA: LLM Informed Systemverilog Assertion generation
exceed local patching strategies.                                                           with RAG and Chain-of-Thought,” in IEEE ISVLSI, 2025.
                                                                                    [12]    V. Pulavarthi et al., “Are LLMs Ready for Practical Adoption for
   Vacuous-property behavior further separates the benchmarks.                              Assertion Generation?” In DATE Conference, 2025.
CIC Decimator and BST exhibit more vacuous properties,                              [13]    K. Maddala et al., “LAAG-RV: LLM Assisted Assertion Generation for
indicating some checks can pass without strongly constraining                               RTL Design Verification,” in IEEE 8th ITC India, 2024.
                                                                                    [14]    OpenCores, https://opencores.org.
behavior under the default environment. This motivates stronger                     [15]    N. Pinckney et al., CVDP: A Next-Generation Benchmark Dataset for
environment modeling or non-vacuity constraints earlier in the                              Evaluating LLMs and Agents on RTL Design and Verification, 2025.
loop so coverage improvements reflect exercised behavior rather
than trivially satisfied properties.
   KG size grows with design complexity and trace link density,
but it does not directly predict verification success. Overall, the
KG improves reliability and repeatability of artifact management
and context retrieval, particularly for property generation and
syntax stabilization, while semantic debugging remains the main
limiting factor on harder benchmarks.
                             V. C ONCLUSION
   This paper presented a KG-centric, multi-agent workflow for
LLM-assisted FV that addresses specification-to-RTL grounding
through structured IRs and bounded context retrieval. Specifi-
cations, RTL metadata, properties, tool outcomes, and coverage
evidence are represented as typed JSON artifacts and exported
as nodes and edges for constructing a requirement-based runtime
KG that supports property generation and post-run refinement
loops. Across the evaluated benchmarks, the approach consis-
tently produces compilable, traceable SVAs with low syntax-
fix overhead, while the largest remaining challenge is semantic
correction for properties that require deeper temporal reasoning
or global invariants. Importantly, as LLMs improve, they can
better leverage the KG’s structured context and traces to improve
property generation and downstream formal verification. Future
work will focus on improving CEX correction with richer tem-
poral reasoning patterns and inductive invariant generation for
stateful designs, and on refining coverage-gap classification to
better separate unreachable code from true verification targets.
                               R EFERENCES
 [1]   R. Kande et al., “(Security) Assertions by Large Language Models,”
       IEEE Transactions on Information Forensics and Security, 2024.
 [2]   Z. Yan et al., “AssertLLM: Generating Hardware Verification Assertions
       from Design Specifications via Multi-LLMs,” in Proceedings of the 30th
       ASPDAC Conference, ACM, 2025.
 [3]   B. Mali et al., “ChIRAAG: ChatGPT Informed Rapid and Automated
       Assertion Generation,” in IEEE ISVLSI, 2024.
 [4]   A. Kumar et al., “Saarthi: The First AI Formal Verification Engineer,”
       in DVCon US, 2025.
 [5]   D. N. Gadde et al., “Hey AI, Generate Me a Hardware Code! Agentic
       AI-based Hardware Design & Verification,” in 38th SBCCI, 2025.
 [6]   Y. Bai et al., “AssertionForge: Enhancing Formal Verification Assertion
       Generation with Structured Representation of Specifications and RTL,”
       in IEEE ICLAD, 2025.
 [7]   F. Wu et al., “Spec2Assertion: Automatic Pre-RTL Assertion Generation
       using LLMs with Progressive Regularization,” arXiv, 2025.
 [8]   A. Ayalasomayajula et al., “LASP: LLM Assisted Security Property
       Generation for SoC Verification,” in ACM/IEEE 6th MLCAD, 2024.
 [9]   H. Lyu et al., “AssertMiner: Module-Level Spec Generation and Asser-
       tion Mining using Static Analysis Guided LLMs,” arXiv, 2025.
[10]   H. A. Quddus et al., “Enhanced VLSI Assertion Generation: Conforming
       to High-Level Specifications and Reducing LLM Hallucinations with
       RAG,” in DVCon Europe, 2024.




©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                               reuse of any copyrighted component of this work in other works.
