                                                                                                                                           (Special Session)
                                                                                      This paper will be presented at IEEE VLSI Test Symposium (VTS) 2026.

                                         From Language to Logic: Bridging LLMs & Formal
                                            Representations for RTL Assertion Generation
                                                                                Nowfel Mashnoor, Hadi Kamali, Kimia Azar
                                            Department of Electrical and Computer Engineering (ECE), University of Central Florida, Orlando, FL 32816, USA
                                                                                    {nowfel, kamali, azar}@ucf.edu


                                            Abstract—SystemVerilog Assertions (SVA) are essential for (RAG) [23] has improved LLM grounding in other domains,
                                         formal verification of digital hardware, yet their manual creation and recent work has applied it to RTL code generation [24], its
                                         demands significant expertise in both the design under verifica- potential for assertion generation, particularly when combined
                                         tion and temporal logic. Recent studies have explored using large
                                         language models (LLMs) to automate SVA generation, but exist- with formal-tool structural queries remains largely unexplored.
arXiv:2604.23100v1 [cs.CR] 25 Apr 2026




                                         ing approaches suffer from incorrect signal references, missing       To address these challenges, we present ProofLoop, a
                                         timing constraints, and lack of formal correctness guarantees. tool-augmented ReAct agent for automated SVA generation
                                         This paper presents ProofLoop, a tool-augmented ReAct agent that integrates Cadence JasperGold as a solver-in-the-loop.
                                         that generates SVA from natural-language specifications using a
                                                                                                             This agentic approach allows the model to dynamically decide
                                         solver-in-the-loop approach. The agent operates in two phases:
                                         Phase A autonomously gathers design context by invoking EDA what information it needs, rather than following a fixed
                                         and formal tools, including semantic search over an AST-indexed pipeline. The key contributions are:
                                         vector database and JasperGold structural queries, while Phase B (1) Agentic context synthesis. We propose a ReAct-based
                                         generates SVA and iteratively refines it using JasperGold formal
                                         proof feedback over up to fixed (here 3) verification rounds. We       agent that autonomously gathers verification-relevant con-
                                         evaluate ProofLoop on FVEval Design2SVA design benchmarks              text via semantic retrieval over an AST-indexed RTL rep-
                                         and demonstrate that this framework can achieve 93.7% syn-             resentation and structural queries to a formal tool.
                                         tax correctness and 82.0% functional correctness. An ablation (2) Solver-in-the-loop refinement. We introduce an iterative
                                         study confirms that each component, i.e., retrieval-augmented          verification loop that leverages formal proof feedback to
                                         generation (RAG), JasperGold tools, and the verification loop
                                         contributes significantly (and orthogonally).                          correct generated assertions, enabling targeted repair of
                                            Index Terms—SystemVerilog Assertions, Formal Verification,          syntax errors, signal mismatches, and inconsistencies.
                                         LLM, ReAct Agent, Solver-in-the-Loop, RAG.                         (3) Scalable assertion generation. We demonstrate that tool-
                                                                                                              augmented context and iterative refinement significantly
                                                               I. I NTRODUCTION
                                                                                                              improve both syntactic and functional correctness, with
                                         Assertion-based verification (ABV) is a cornerstone of modern        robustness that scales to complex, multi-module designs.
                                         hardware verification, enabling engineers to express design (4) Comprehensive empirical study. We evaluate on the FVE-
                                         intent as SystemVerilog Assertions (SVA) that can be formally        val benchmark [25] and present ablation analyses that quan-
                                         proven or monitored during simulation [1]–[3]. However,              tify the impact of retrieval, structural analysis, and verifi-
                                         writing quality SVA remains computation- and labor-intensive         cation feedback, highlighting the role of tool augmentation
                                         that requires deep understanding of both register-transfer level     in bridging natural language and formal specifications.
                                         (RTL) semantics and temporal logic [4]. Prior automated
                                         approaches based on data mining [5]–[7] or template matching                          II. R ELATED W ORK
                                         [8], [9] have shown promise but remain limited in expressive- Traditional approaches to automated assertion generation in-
                                         ness and require design-specific configuration. As hardware clude GoldMine [5], which uses data mining over simulation
                                         complexity continues to grow, particularly at system-on-chip traces; HARM [6], a hint-based assertion miner; and AutoSVA
                                         (SoC) scale, the cost of non-automated assertion authoring has [8], which generates formal testbenches from interface anno-
                                         become a bottleneck in verification.                             tations. While effective for specific patterns, these methods do
                                            Large language models (LLMs) have shown promise in au- not generalize from natural-language specifications.
                                         tomating SVA generation [10]–[12], building on their success        Table I summarizes key differences among recent LLM-
                                         in RTL code generation [13]–[18] and verification [19], [20]. based SVA generation approaches. ChIRAAG [26] uses GPT-
                                         However, directly prompting an LLM with raw RTL and a 4 with simulation log feedback. AssertLLM [27] introduces a
                                         specification often produces assertions with incorrect signal three-phase multi-LLM pipeline, but operates without formal
                                         names, wrong clock/reset assumptions, and mismatched tem- feedback. SANGAM [28] applies Monte Carlo Tree Self-
                                         poral sequences (w.r.t. actual hardware behavior) [21], [22]. Refine (MCTSr) with JasperGold syntax checking in the
                                         These errors persist because LLMs lack access to the structural search loop; however, its MCTSr-based search is computa-
                                         metadata that verification engineers rely on, e.g., flip-flop tionally expensive and does not leverage JG metadata for
                                         clocking, reset values, signal fanin/fanout relationships, and context enrichment. Saarthi [29] proposes an agentic multi-
                                         FSM state encodings. While retrieval-augmented generation agent system with formal proof analysis but lacks a large-
   TABLE I: Comparison of LLM-Based SVA Generation Approaches.
                                                                                 JasperGold formal verification in Phase B (see Alg. 1).
Method                RAG JG Meta. Agentic Tools Solver Loop Bench. Eval.
                                                                                 B. AST Indexing and Knowledge Base
ChIRAAG [26]           ✗         ✗              ✗       Sim.       ✗
AssertLLM [27]         ✗         ✗              ✗         ✗        ✗             The RTL design is parsed using a SystemVerilog compiler [37]
SANGAM [28]           ✓          ✗              ✗        JG        ✗             to produce an verifiable AST. The AST is decomposed into
Saarthi [29]           ✗         ✗              ✓        FV        ✗
AssertionForge [30]   KG         ✗              ✗         ✗        ✗
                                                                                 four semantic chunk types:
SVAgent [31]           ✗         ✗              ✗         ✗        ✗             1) Module Interface: ports, parameters, and localparams.
ChatSVA [32]          ✓          ✗              ✗         ✗        ✗             2) Always Block: capturing sequential/combinational logic.
ProofLoop (Ours)       ✓         ✓              ✓          JG     ✓              3) Instance: sub-module instantiations with port connections.
                                                                                 4) Assign: continuous assignment groups.
scale benchmark evaluation. AssertionForge [30] constructs                       Each chunk is embedded using an embedding model and
a knowledge graph for multi-resolution context synthesis but                     stored in a vector database, creating a per-design knowledge
does not include iterative formal refinement. SVAgent [31]                       base that supports semantic similarity search. This modular
uses fine-grained prompting for security-oriented assertions                     decomposition ensures that the LLM context window is pop-
without RAG or iterative formal refinement. ChatSVA [32]                         ulated only with the most relevant design fragments rather
combines task-specific fine-tuned LLMs with data augmenta-                       than the entire RTL, which is critical for multi-module designs
tion, complementing our tool-augmented approach. Menon et                        where the full source can exceed context limits.
al. [33] contribute a curated SVA dataset that supports fine-
                                                                                 C. Phase A: Context Gathering
tuning-based methods. FVEval [25] establishes the benchmark
and evaluation methodology we adopt. RTLFixer [34] and                           The tool autonomously gathers design context through an
Blocklove et al. [35] demonstrate that iterative EDA tool                        interleaved Thought → Action → Observation loop for up
feedback can correct LLM-generated RTL, a concept we                             to 6 rounds. The system has access to two categories of tools:
extend to assertion generation. Hassan et al. [36] combine                       (1) Retrieval tools provide lightweight access to the vector
LLM-guided formal verification with mutation testing, high-                      database. They enable semantic search over the AST-indexed
lighting the synergy between LLMs and formal tools. As                           chunks, module interface queries (ports, parameters), hierarchy
shown in Table I, ProofLoop differs from prior work in                           traversal across the dependency tree, parameter/localparam
two key ways: (i) the agent autonomously decides which                           resolution, and signal-specific always-block retrieval.
tools to invoke through a reasoning loop, dynamically adapt-                        Structural analysis tools interface with JasperGold to
ing its information-gathering strategy per specification; and                    extract hardware-level metadata that cannot be inferred from
(ii) JasperGold is integrated both for structural queries during                 RTL text alone. These include signal fan-in and fan-out cone
context gathering (signal dependency and register analysis)                      extraction, which reveals datapath dependencies, and flip-flop
and for formal proof during iterative verification.                              property inspection, which reports clock domains, reset be-
                                                                                 havior, and data-input connections. The system autonomously
              III. P ROPOSED M ETHOD : P R O O F L O O P                         decides which tools to call based on the specification. This
A. Overview                                                                      approach skips extra queries for simple cases while allowing
                                                                                 deeper exploration for complex designs.
Fig. 1 shows the ProofLoop framework. Given an RTL
design and a natural-language assertion specification, the                       D. Phase B: SVA Generation and Verification Loop
system operates in 3 stages: (1) AST indexing builds a                           After context gathering, the agent generates candidate SVA
semantic knowledge base from the RTL, (2) a ReAct agent                          conditioned on the retrieved design context and the natural-
gathers design context via tool calls in Phase A, and (3) the                    language specification. The generated assertions are embedded
agent generates SVA, followed by iteratively refining it using                   into the RTL and passed to JasperGold for bounded formal

    Input Data                     AST Indexing &                        SVA Generation with ProofLoop         SVA Verification and Refinement Loop
    Collection              Knowledge Base Preprocessing
                                                                                                                 assert
                                 AST Parser         Embedding                              VectorDB Tools         (...)                         Verified SVA
                                                                                           Semantic Search                        JG Results
                           Chunk Types Extracted
                                                                                           Module Interface     SVA to JG
                               Module Interface                   Large Language                                  Ver.
                                                                      Model                Module Interface                           Refinement Loop
                              (ports, parameters)
    RTL Desing                                                         Agent Loop                                                       (Falsified/SE)
                                 Always Block                                             Desing Hierarchy           Agent Loop
       (SV)
                               (seq/comb logic)                                              Parameters
                                   Instance                                                  Signal Logic                                 Refine SVA and
                              (sub-module inst.)                                                                                            Re-submit
                                                     VectorDB                             JasperGold Tools
                                    Assign            Design                                                         Observe
       Spec                                                                                   Fan-in/Out
                              (cont. assignment)    Knowledge          Observe
                                                       Base                                   Flip-Flop        1/5        2/5       3/5        4/5    5/5


Fig. 1: ProofLoop framework (Tool-augmented ReAct agent). In Phase A, the agent autonomously queries retrieval and structural analysis tools to gather
design context. In Phase B, the agent generates SVA assertions and iteratively refines them using JasperGold formal verification feedback.
Algorithm 1 Tool-in-the-Loop Calls in ProofLoop.                     B. Assertion Verification results
Require: RTL design D, NL specification s, LLM L, tools T            Table II presents the main comparison across 192 designs. The
Ensure: Verified SVA assertion
 1: AST Indexing:                                                    tool-augmented pipeline substantially outperforms the direct
 2: chunks ← pyslang parse(D) {4 chunk types}                        prompting baseline in both syntax and functional correctness,
 3: VectorDB.store(embed(chunks))
 4: Phase A: Context Gathering (up to 6 rounds)                      nearly doubling the functionality score with Qwen3.5-35B. A
 5: conv ← [system prompt, spec(s), design context(D)]               cross-model evaluation with Mistral confirms that the improve-
 6: for r = 1 to 6 do
 7:     msg ← L(conv, tools = T ) {ReAct: Thought+Action}            ment generalizes: the pipeline yields a comparable relative
 8:     if no tool calls in msg then                                 gain despite the smaller model’s lower capability.
 9:          break {Agent has enough context}
10:      end if                                                            TABLE II: Assertion Verification results: Pipeline vs. Baseline
11:      for each tool call t in msg do
12:          obs ← T .execute(t) {Observation}                        Model                Method     Syntax       Functionality     Proven     Falsified
13:          conv.append(obs)
                                                                      Qwen3.5-35B          Baseline     78.3           43.2           445         246
14:      end for
15: end for                                                           Qwen3.5-35B          Pipeline     93.7           82.0           790         260
16: Phase B: Generation + Verification (up to 3 rounds)               Mistral-Small-24B    Baseline     65.8           31.1           249         200
17: sva ← L.generate sva(conv)
18: for v = 1 to 3 do                                                 Mistral-Small-24B    Pipeline     85.5           53.3           419         724
19:      result ← JG.prove(sva, D)
20:      if result.status ∈ {proven, undetermined} then              C. Component-Wise Ablation Analysis
21:          vacuity ← JG.vacuity check(sva, D)
22:          break                                                   To isolate each component’s contribution, we conduct an
23:      end if
                                                                     ablation study on a 36-design subset, progressively removing
24:      sva ← L.fix(sva, result.feedback)
25: end for                                                          pipeline components. Table III presents the results.
26: return sva, result
                                                                        Stripping away all tools reduces the pipeline to baseline-
verification. The solver attempts to prove all properties within     level performance, confirming that the agentic tool augmen-
a bounded time limit, classifying each as proven, falsified,         tation is the primary driver of improvement. Among indi-
or undetermined. For proven or undetermined properties, we           vidual components, the iterative verification loop provides
perform an additional vacuity analysis to ensure that the proof      the largest single contribution by enabling the agent to cor-
is non-trivial (i.e., not satisfied due to unreachable antecedents   rect syntax errors and temporal mismatches through solver
or inactive triggering conditions). Otherwise, the solver’s error    feedback. Structural analysis tools offer the next-largest gain,
messages and counterexample traces are fed back to the               as they supply authoritative signal dependency and register
agent, enabling targeted repair of the failing assertions rather     information that the LLM cannot infer from RTL text alone.
than blind regeneration. This feedback is programmatically           RAG retrieval provides a more modest but consistent benefit,
parsed and incorporated into the agent’s context for targeted        primarily helping the agent resolve signal names and module
refinement. Rather than regenerating assertions from scratch,        interfaces accurately.
the agent performs localized edits, e.g., correcting signal          D. Design Complexity Analysis
references, aligning clock/reset domains, refining temporal          Fig. 2 reveals that the pipeline’s advantage scales with design
operators, or restructuring antecedent/consequent conditions         complexity. For single-module designs, the baseline achieves
to match observed behavior. This solver-in-the-loop is a key         66.1% functionality since the full RTL fits within the LLM’s
differentiator from prior work: the system receives concrete,        context window. However, as designs grow to include multiple
machine-generated feedback about why an assertion fails,             interconnected modules, the baseline’s performance degrades
syntax errors, signal mismatches, or temporal violations, and        for large designs while the pipeline maintains relatively stable
can surgically correct the issue.                                    accuracy. This shows that AST-based retrieval and structural
                                                                     analysis are most effective for complex, multi-module designs.
                   IV. E XPERIMENTAL R ESULTS                        The pipeline’s modular decomposition ensures bounded con-
A. Experimental Setup                                                text per query, regardless of total design size.
We evaluate ProofLoop on the FVEval benchmark [25],                  E. Design2SVA Benchmark Comparison
which comprises 96 pipeline and 96 FSM designs of varying            We evaluated the ProofLoop framework on the Design2SVA
complexity. We measure and report two primary metrics: (i)           task from FVEval [25]. For each design, we perform 5
Syntax, where 1.0 denotes if JasperGold reports no compi-            independent trials per design with nucleus sampling. Table IV
lation errors; and (ii) Functionality, which determines the          compares against the FVEval baselines.
ratio of proven to total number of assertions. Our primary              Despite using a smaller model, our pipeline substantially
model is Qwen3.5-35B with native tool-calling capabilities.          TABLE III: Ablation Study for Tool Augmentation and Solver Feedback.
To assess generality, we additionally evaluate Mistral-Small-         Configuration                   Syntax (%)      Functionality (%)       ∆ vs. Full
3.1-24B under the same pipeline configuration. The baseline
                                                                      Full Pipeline                      93.7                 82.0               —
corresponds to direct prompting, where the LLM is provided              − RAG retrieval                  90.9                 70.9             −13.5%
with raw RTL and the natural-language specification without             − Verification loop              82.9                 64.7             −21.1%
access to retrieval, structural tools, or verification feedback.        − Structural analysis tools      80.0                 58.4             −28.8%
                                                                        − All tools (baseline)           70.3                 36.1             −56.0%
All experiments are conducted on NVIDIA H100 GPUs.
                    100                                                                                  80                                                            71.1
                                                                        Pipeline                                                               64.8
                     80                                                 Baseline
Functionality (%)

                                                                                                         60




                                                                                       Correctness (%)
                                                                                                                   52.7
                     60                                                                                                  Syntax
                                                                                                         40              Functionality
                     40
                     20                                                                                                                                                18.2
                                                                                                         20                                    11.8
                      0                                                                                            2.0
                             Small                Medium             Large                                0
                          (1 module)           (2-6 modules)      (7+ modules)                                V1                          V2                      V3
    Fig. 2: Functionality by design complexity. The pipeline’s advantage grows             Fig. 3: Syntax and functional correctness improvement across verification
    substantially with design size, as the baseline struggles with multi-module            rounds for the multi-iteration specs. Each round of solver feedback progres-
    designs that exceed LLM context capacity.                                              sively improves both metrics, with syntax recovery.

    outperforms in both design categories. The improvement is                              vs. asynchronous reset from the raw RTL alone.
    particularly pronounced on pipeline designs, where multi-                                 In Phase A, the framework issues 22 tool calls across 6
    module structural complexity makes tool-augmented con-                                 reasoning rounds: it queries module interfaces and parameters
    text gathering essential; the FVEval baselines rely on direct                          for all five units, performs semantic searches for register
    prompting and lack access to structural metadata or iterative                          behavior and reset semantics, and retrieves specific always-
    solver feedback. The strong pass@5 scores indicate that with                           block code to confirm clocking. In Phase B, the first SVA
    multiple trials, the agent reliably produces at least one formally                     attempt uses array-slice notation (ready[1:3] == ’d0),
    provable assertion, suggesting robust performance even when                            which JasperGold rejects as a compilation error. The
    individual attempts may vary. This shows that the combination                          solver feedback identifies the invalid syntax, and the agent
    of structured context and solver-guided refinement constrains                          corrects it by expanding to individual element comparisons
    the search space, enabling convergence to formally provable                            (ready[1] == ’d0 && ready[2] == ’d0 && ...).             The
    assertions even when individual generations may vary.                                  corrected assertions are formally proven in the second round
    F. Verification Loop Analysis                                                          (5 proven, 0 falsified). This example highlights how the
    Fig. 3 analyzes the iterative verification loop across all spec-                       tool-augmented context gathering resolves cross-module
    ifications. Two-thirds of specs (384) succeed on the first                             structural questions and the verification loop catches and
    verification attempt. Of the remaining specs converge after                            corrects SVA syntax errors that would otherwise persist.
    two rounds and 114 require all three rounds. The agent is                                                      V. C ONCLUSION
    most effective at recovering from syntax and compilation
                                                                                           This paper presented a tool-augmented framework for auto-
    errors: 59.3% of syntax failures are corrected through solver
                                                                                           mated SVA generation that integrates JasperGold as a solver-
    feedback. Falsification recovery is harder; only 20 of 101 specs
                                                                                           in-the-loop. The agent autonomously gathers design context
    with initially falsified properties fully recover. This asymmetry
                                                                                           through a suite of retrieval and structural analysis tools,
    suggests that LLMs are more capable of fixing structural
                                                                                           then generates and iteratively refines SVA using formal proof
    mistakes given explicit error messages than of correcting
                                                                                           feedback. The pipeline achieves 93.7% syntax and 82.0%
    temporal logic errors, which require deeper reasoning about
                                                                                           functional correctness, outperforming the baseline on 66.1%
    hardware behavior.
                                                                                           of designs with gains that scale with design complexity reach-
    G. Case Study                                                                          ing significant relative improvement on large multi-module
    We illustrate the pipeline on a 6-module FSM design with                               designs. On the Design2SVA benchmark, the pipeline achieves
    a top-level module instantiating five execution units. The                             a combined pass@1 of 0.636, substantially outperforming
    specification requires verifying that all pipeline stage registers                     baselines. The results suggest that the agentic tool-augmented
    clear correctly on reset: synchronous register must clear on                           approach addresses the fundamental limitation of prompt-
    the next clock edge, while asynchronous registers must clear                           only methods: the inability to access the structural metadata
    immediately. The baseline produces syntactically invalid SVA                           that verification engineers routinely rely on. Future work will
    because it cannot determine which registers use synchronous                            explore domain-specific fine-tuning on curated SVA datasets,
                          TABLE IV: FVEval Design2SVA Comparison.                          extension to SoC-scale multi-file designs, integration with
                                         Pipeline Designs        FSM Designs               open-source formal engines to broaden accessibility, and inves-
    Method                         Func@1           Func@5     Func@1      Func@5          tigate multi-agent collaboration, where agents handle distinct
    GPT-4o [25]                        0.104          0.427     0.373          0.900       verification subtasks, enabling more comprehensive assertion
    Gemini-1.5-Pro [25]                0.175          0.500     0.427          0.906       suites for industrial-scale designs.
    Gemini-1.5-Flash [25]              0.025          0.125     0.079          0.281
    Mixtral-8x22B [25]                 0.119          0.472     0.054          0.167                                                R EFERENCES
    Llama-3.1-70B [25]                 0.167          0.615     0.231          0.719
    Llama-3.1-8B [25]                  0.150          0.552     0.121          0.521           [1] H. Witharana, Y. Lyu, S. Charles, and P. Mishra, “A survey on assertion-
    Ours (Qwen3.5-35B)                 0.412          0.896     0.860          0.958
                                                                                                   based hardware verification,” ACM Computing Surveys, vol. 54, no. 11s,
                                                                                                   pp. 1–33, 2022.
 [2] S. Vijayaraghavan and M. Ramanathan, A Practical Guide for Sys-              [21] V. Pulavarthi, D. Nandal, S. Dan, and D. Pal, “AssertionBench: A
     temVerilog Assertions. Springer, 2005.                                            benchmark to evaluate large-language models for assertion generation,”
 [3] E. M. Clarke, T. A. Henzinger, H. Veith, and R. Bloem, Handbook of                in Findings of the Association for Computational Linguistics: NAACL
     Model Checking. Springer, 2018.                                                   2025, 2025.
 [4] S. Aftabjahani, R. Kastner, M. Tehranipoor, F. Farahmandi, J. Oberg,         [22] M. Kang, M. Liu, G. Bany Hamad, S. Suhaib, and H. Ren, “Domain-
     A. Nordstrom, N. Fern, and A. Althoff, “Special session: CAD for                  adapted LLMs for VLSI design and verification: A case study on formal
     hardware security—automation is key to adoption of solutions,” in 2021            verification,” in 2024 IEEE 42nd VLSI Test Symposium (VTS). IEEE,
     IEEE 39th VLSI Test Symposium (VTS). IEEE, 2021, pp. 1–10.                        2024.
 [5] S. Vasudevan, D. Sheridan, S. Patel, D. Tcheng, B. Tuohy, and D. John-       [23] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal,
     son, “GoldMine: Automatic assertion generation using data mining                  H. Küttler, M. Lewis, W.-t. Yih, T. Rocktäschel et al., “Retrieval-
     and static analysis,” in 2010 Design, Automation & Test in Europe                 augmented generation for knowledge-intensive NLP tasks,” in Advances
     Conference & Exhibition (DATE). IEEE, 2010, pp. 626–629.                          in Neural Information Processing Systems (NeurIPS), 2020.
 [6] S. Germiniani and G. Pravadelli, “HARM: A hint-based assertion miner,”       [24] Z. Ibnat, P. E. Calzada, R. M. Ihtemam, S. K. Saha, J. Zhou, F. Farah-
     IEEE Transactions on Computer-Aided Design of Integrated Circuits                 mandi, and M. Tehranipoor, “DeepV: A model-agnostic retrieval-
     and Systems, vol. 41, no. 11, pp. 4277–4288, 2022.                                augmented framework for Verilog code generation with a high-quality
 [7] A. Danese, N. Dalla Riva, and G. Pravadelli, “A-Team: Automatic                   knowledge base,” arXiv preprint arXiv:2510.05327, 2025.
     template-based assertion miner,” in Proceedings of the 54th Annual           [25] M. Kang, M. Liu, G. Bany Hamad, S. Suhaib, and H. Ren, “FVEval:
     Design Automation Conference (DAC). ACM, 2017, pp. 1–6.                           Understanding language model capabilities in formal verification of
 [8] M. Orenes-Vera, A. Manocha, D. Wentzlaff, and M. Martonosi, “Au-                  digital hardware,” arXiv preprint arXiv:2410.23299, 2024.
     toSVA: Democratizing formal verification of RTL module interactions,”        [26] B. Mali, K. Maddala, V. Gupta, S. Reddy, C. Karfa, and R. Karri, “ChI-
     in Proceedings of the 58th ACM/IEEE Design Automation Conference                  RAAG: ChatGPT informed rapid and automated assertion generation,”
     (DAC). ACM/IEEE, 2021, pp. 535–540.                                               in 2024 IEEE Computer Society Annual Symposium on VLSI (ISVLSI).
 [9] N. Farzana, F. Rahman, M. Tehranipoor, and F. Farahmandi, “SoC se-                IEEE, 2024, pp. 680–683.
     curity verification using property checking,” in 2019 IEEE International     [27] W. Fang, M. Li, M. Li, Z. Yan, S. Liu, H. Zhang, and Z. Xie,
     Test Conference (ITC). IEEE, 2019, pp. 1–10.                                      “AssertLLM: Generating and evaluating hardware verification asser-
[10] R. Kande, H. Pearce, B. Tan, B. Dolan-Gavitt, S. Thakur, R. Karri, and            tions from design specifications via multi-LLMs,” arXiv preprint
     J. Rajendran, “(security) assertions by large language models,” IEEE              arXiv:2402.00386, 2024.
     Transactions on Information Forensics and Security, 2024.                    [28] A. Gupta, B. Mali, and C. Karfa, “SANGAM: SystemVerilog as-
[11] M. Orenes-Vera, M. Martonosi, and D. Wentzlaff, “Using LLMs to                    sertion generation via Monte Carlo tree self-refine,” arXiv preprint
     facilitate formal verification of RTL,” arXiv preprint arXiv:2309.09437,          arXiv:2506.13983, 2025.
     2023.                                                                        [29] A. Kumar, D. N. Gadde, K. K. Radhakrishna, and D. Lettnin,
[12] C. Sun, C. Hahn, and C. Trippel, “Towards improving verification                  “Saarthi: The first AI formal verification engineer,” arXiv preprint
     productivity with circuit-aware translation of natural language to Sys-           arXiv:2502.16662, 2025.
     temVerilog assertions,” in Proceedings of the DAV Workshop, 2023.            [30] Y. Bai, G. Bany Hamad, S. Suhaib, and H. Ren, “AssertionForge:
[13] S. Thakur, B. Ahmad, H. Pearce, B. Tan, B. Dolan-Gavitt, R. Karri, and            Enhancing formal verification assertion generation with structured rep-
     S. Garg, “VeriGen: A large language model for Verilog code generation,”           resentation of specifications and RTL,” in 2025 IEEE International
     arXiv preprint arXiv:2308.00708, 2023.                                            Conference on LLM-Aided Design (ICLAD). IEEE, 2025.
[14] M. Akyash, K. Azar, and H. Kamali, “Decortl: A run-time decoding             [31] R. Guo, A. Ayalasomayajula, H. Li, J. Zhou, S. K. Saha, and F. Farah-
     framework for rtl code generation with llms,” in 2025 IEEE/ACM                    mandi, “SVAgent: AI agent for hardware security verification assertion,”
     International Conference On Computer Aided Design (ICCAD). IEEE,                  arXiv preprint arXiv:2507.16203, 2025.
     2025, pp. 1–9.                                                               [32] L. T. Fu, J. Zhou, S. Ren, M. Zhang, J. Xiong, H. Jiang,
[15] S. Liu, W. Fang, Y. Lu, J. Wang, Q. Zhang, H. Zhang, and Z. Xie, “Rtl-            N. Guan, X. Wang, and J. Yang, “ChatSVA: Bridging SVA genera-
     coder: Fully open-source and efficient llm-assisted rtl code generation           tion for hardware verification via task-specific LLMs,” arXiv preprint
     technique,” IEEE Transactions on Computer-Aided Design of Integrated              arXiv:2604.02811, 2026.
     Circuits and Systems, vol. 44, no. 4, pp. 1448–1461, 2024.                   [33] A. Menon et al., “Enhancing large language models for hardware ver-
[16] M. Akyash, K. Azar, and H. Kamali, “Rtl++: Graph-enhanced llm for rtl             ification: A novel SystemVerilog assertion dataset,” ACM Transactions
     code generation,” in 2025 IEEE International Conference on LLM-Aided              on Design Automation of Electronic Systems, 2025.
     Design (ICLAD). IEEE, 2025, pp. 44–50.                                       [34] Y.-D. Tsai, M. Liu, and H. Ren, “RTLFixer: Automatically fix-
[17] Y. Zhao, D. Huang, C. Li, P. Jin, M. Song, Y. Xu, Z. Nan, M. Gao,                 ing RTL syntax errors with large language models,” arXiv preprint
     T. Ma, L. Qi et al., “Codev: Empowering llms with hdl generation                  arXiv:2311.16543, 2023.
     through multi-level summarization,” IEEE Transactions on Computer-           [35] J. Blocklove, S. Thakur, B. Tan, H. Pearce, S. Garg, and R. Karri,
     Aided Design of Integrated Circuits and Systems, 2025.                            “Automatically improving LLM-based Verilog generation using EDA
[18] N. Mashnoor, M. Akyash, H. Kamali, and K. Azar, “Meltrtl: Multi-                  tool feedback,” ACM Transactions on Design Automation of Electronic
     expert llms with inference-time intervention for rtl code generation,”            Systems, 2025.
     arXiv preprint arXiv:2601.13015, 2026.                                       [36] M. Hassan, S. Ahmadi-Pour, K. Qayyum, C. K. Jha, and R. Drechsler,
[19] H. Huang, Z. Lin, Z. Wang, X. Chen, K. Ding, and J. Zhao, “Towards                “LLM-guided formal verification coupled with mutation testing,” in
     llm-powered verilog rtl assistant: Self-verification and self-correction,”        2024 Design, Automation & Test in Europe Conference & Exhibition
     arXiv preprint arXiv:2406.00115, 2024.                                            (DATE). IEEE, 2024, pp. 1–6.
[20] N. Mashnoor, M. Akyash, H. Kamali, and K. Azar, “Llm-ift: Llm-               [37] C. Wolf, J. Glaser, and J. Kepler, “Yosys—a free Verilog synthesis
     powered information flow tracking for secure hardware,” in 2025 IEEE              suite,” in Proceedings of the 21st Austrian Workshop on Microelectronics
     43rd VLSI Test Symposium (VTS). IEEE, 2025, pp. 1–5.                              (Austrochip), vol. 97, 2013.
