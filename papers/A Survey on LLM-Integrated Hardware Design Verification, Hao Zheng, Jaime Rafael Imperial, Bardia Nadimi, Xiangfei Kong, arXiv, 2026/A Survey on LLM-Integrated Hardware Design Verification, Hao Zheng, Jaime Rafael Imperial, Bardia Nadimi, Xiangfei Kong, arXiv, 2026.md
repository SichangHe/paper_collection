                                              A Survey on LLM-Integrated Hardware Design
                                                             Verification
                                                                  Hao Zheng∗ , Jaime Rafael Imperial∗ , Bardia Nadimi∗ , Xiangfei Kong∗
                                                                ∗ Bellini College of Cybersecurity, AI, and Computing, University of South Florida

                                                                                               Tampa, FL, USA
                                                                          Email: {haozheng, imperialj, bnadimi, xiangfeikong}@usf.edu


                                            Abstract—Large language models (LLMs) are increasingly                    Consequently, hardware verification has become one of
                                        being integrated into hardware verification to automate spec-              the most challenging, costly, and resource-intensive stages of
                                        ification interpretation, verification-artifact generation, debug-         the IC design process [3], aiming to establish that hardware
                                        ging, formal reasoning, and tool orchestration. This survey
arXiv:2610.10580v1 [cs.AR] 6 Oct 2026




                                        provides a systematic review of LLM-assisted hardware func-                implementations conform to their functional requirements and
                                        tional verification across SystemVerilog assertion generation,             design intent. While verification spans both pre-silicon veri-
                                        stimulus and testbench generation, bug localization and design             fication and post-silicon validation, pre-silicon verification is
                                        repair, model checking and equivalence checking, SAT/SMT                   particularly critical because defects that escape into fabrication
                                        optimization, and emerging agentic verification workflows. We              can require costly silicon re-spins, cause substantial schedule
                                        organize the literature by methodology, verification objective, tool
                                        interaction, benchmark, and evaluation criterion, and examine              delays, and incur significant financial losses [4]. Yet, growing
                                        both inference-time techniques—including prompting, retrieval,             hardware complexity has made pre-silicon verification increas-
                                        structured reasoning, and agentic workflows—and training-time              ingly difficult to scale. The 2024 Wilson Research Group
                                        adaptation. Across these areas, a common pattern emerges:                  Functional Verification Study [5] reports that peak IC/ASIC
                                        LLMs are most effective as semantic reasoning, search, and                 verification teams average over 14 engineers, compared with
                                        orchestration components embedded within verification-aware
                                        workflows, while simulators, formal engines, coverage tools, and           approximately 12 design engineers, while design engineers
                                        solvers provide executable feedback and correctness evidence.              spend about 50% of their time on verification. Overall, verifi-
                                        However, tool acceptance alone does not establish verification             cation is estimated to consume 60–70% of IC development
                                        correctness, since assertions, tests, repairs, or proofs may sat-          cost and schedule [6, 7], highlighting the need for greater
                                        isfy available checks without faithfully capturing the complete            automation and productivity in modern hardware verification.
                                        design intent. We therefore identify semantic alignment between
                                        specifications and verification evidence, scalable integration with           Large Language Models (LLMs) [8, 9, 10] are increasingly
                                        deterministic tools, generalization to unseen designs, and rigorous        used across the Electronic Design Automation (EDA) stack
                                        evaluation of correctness, cost, robustness, and human effort as           because they can interpret and generate diverse hardware ar-
                                        key challenges. Finally, we discuss emerging directions toward             tifacts, including specifications, RTL, assertions, testbenches,
                                        specification-centered, neuro-symbolic, and persistent agentic             and tool logs. Their flexible natural-language interface enables
                                        verification systems that combine LLM flexibility with indepen-
                                        dently checkable verification evidence.                                    reasoning across heterogeneous information and interaction
                                            Index Terms—Large language models, hardware verification,              with EDA tools through retrieval-augmented and agentic work-
                                        formal verification, electronic design automation.                         flows [11, 12]. Consequently, LLMs have been explored for
                                                                                                                   specification analysis [13, 14], RTL and hardware genera-
                                                               I. I NTRODUCTION                                    tion [15, 16, 17, 18], design-space exploration [19], verifi-
                                           Computing systems have become indispensable to mod-                     cation planning [20], assertion and testbench generation [21,
                                        ern society, supporting a wide range of applications with                  22, 23, 24, 25], bug localization and repair [26, 27], and
                                        increasingly stringent requirements for functionality, perfor-             autonomous verification [28]. Recent approaches increasingly
                                        mance, reliability, safety, security, and energy efficiency. At            integrate LLMs with simulators, formal verification engines,
                                        the hardware level, System-on-Chip (SoC) designs have be-                  synthesis tools, and external knowledge to ground generation
                                        come a dominant architecture, with modern chips integrating                and enable iterative refinement [28, 29]. Despite substantial
                                        tens to hundreds of billions of transistors and increasingly               progress, significant challenges remain in ensuring correctness,
                                        heterogeneous and tightly coupled functional blocks [1, 2].                mitigating hallucinations, preserving design intent, scaling to
                                        This growing hardware complexity, coupled with society’s                   industrial-scale designs, and establishing rigorous evaluation
                                        increasing reliance on computing systems in safety-, security-             methodologies tailored to hardware engineering tasks moti-
                                        , and mission-critical applications, makes ensuring hardware               vating systematic research into trustworthy and autonomous
                                        correctness and dependability increasingly challenging and                 LLM-integrate hardware verification.
                                        essential. Consequently, rigorous hardware verification is a
                                        fundamental requirement for identifying design errors and es-              A. Why a New Survey Focused on LLM-Driven Verification?
                                        tablishing confidence that hardware implementations conform                  The rapid adoption of Large Language Models (LLMs)
                                        to their intended specifications before deployment.                        has spurred a growing body of survey literature on their



                                                                                                               1
applications in Electronic Design Automation (EDA). Ex-                  repair, and autonomous verification agents. In addition, the
isting surveys consistently identify LLMs as a transforma-               survey provides a unified comparison of datasets, benchmarks,
tive technology across the chip design flow, but they differ             tools, and evaluation frameworks used throughout the field,
substantially from the scope of this survey. Pan et al. [11]             identifies common limitations such as hallucination, tool or-
provide a broad EDA-wide treatment spanning system-level                 chestration, and scalability, and highlights emerging research
design, RTL design, logic synthesis, physical design, and                directions including multimodal LLMs, agentic verification
analog design, with verification appearing as one component              systems, and human-in-the-loop verification workflows. By
of a much larger design-automation landscape. Xu et al. [12]             treating hardware verification as an integrated feedback-driven
similarly frame LLMs as a general technology across the chip             process rather than a collection of isolated applications, this
flow, including specification optimization, HDL generation,              survey establishes a comprehensive reference for researchers
testing, debugging, synthesis, and back-end task execution.              and practitioners and provides a roadmap for advancing LLM-
Consequently, they relegate functional verification to brief sub-        integrated verification from proof-of-concept demonstrations
sections, missing technical nuances like Universal Verifica-             to dependable engineering practice.
tion Methodology (UVM) infrastructure composition. Yang et
al.[30] narrow the focus to Verilog code generation, explicitly          B. Paper Organization
organizing the literature around models, datasets, metrics,
generation techniques, and alignment, but their inclusion                   The organization of this paper is as follows. Section II gives
criteria exclude studies focused solely on repair or testing             background necessary to the following sections. Section III
without generation. The recent Agentic EDA survey [28]                   surveys the latest research on SVA generations using LLMs.
targets autonomous orchestration of the RTL-to-GDSII flow                Section IV surveys the latest research on stimulus and test-
and emphasizes perception–cognition–action loops, tool ex-               bench generation usinig LLMs. Section V surveys the latest
ecution, and the sim-to-silicon gap rather than the detailed             research on bug localization and design repair using LLMs.
methodology of verification tasks. The work in [31] focuses              Section VI surveys the latest research on formal verification
primarily on vulnerability identification (e.g., Common Weak-            using LLMs. Section VII concludes the paper, offers our views
ness Enumerations) and threat modeling. While they lever-                of current challenges to LLM-based verification methods, and
age testbenches and assertions, their core metric is security            highlight promising future research directions.
compliance rather than general functional coverage closure.
A verification-specific survey by Liu et al. [32] is closest in
                                                                                               II. BACKGROUND
spirit, but it is compact and organized as a high-level overview
of assertion generation, testbench generation, debugging, and            A. Overview of Hardware Design Flow
holistic verification frameworks. Consequently, these works do
not provide comprehensive coverage of the rapidly expanding                 A typical hardware design flow, illustrated in Fig. 1, pro-
landscape of LLM-driven hardware functional verification,                gresses through increasingly concrete representations from
including emerging techniques for testbench generation, asser-           system requirements to fabricated silicon. System and architec-
tion generation, coverage closure, bug localization, debugging,          tural specifications define functional requirements, interfaces,
design repair, verification agents, benchmark development, and           and performance, power, and area (PPA) objectives, which
evaluation methodologies. This gap has become increasingly               are refined into microarchitecture and synthesizable RTL. The
pronounced as the field has grown rapidly since 2024, with               RTL is transformed through logic synthesis into a gate-level
dozens of verification-focused studies appearing in leading              netlist and subsequently through physical design, including
EDA venues. As a result, researchers and practitioners cur-              floorplanning, placement, clock-tree synthesis, and routing,
rently lack a unified and systematic understanding of how                followed by physical verification and signoff before tapeout
LLMs are being applied across the full verification workflow,            and fabrication. Fabricated devices then undergo post-silicon
the associated benchmark ecosystems, and the remaining tech-             validation for functionality, performance, and power.
nical challenges. Table I summarizes the structural coverage                Verification is a cross-cutting activity throughout this flow
gaps of existing literature across the four pillars of the pro-          rather than an isolated design stage. At the RTL and gate
posed survey paper.                                                      levels, functional verification employs simulation, constrained-
   This survey provides a comprehensive review of recent                 random testing, assertions, functional coverage, formal meth-
research on LLM-integrated hardware functional verification,             ods, and RTL-to-netlist equivalence checking. Physical imple-
a rapidly emerging research area with unique workflows, arti-            mentation is validated through static timing analysis, design-
facts, evaluation criteria, and tool-integration requirements that       rule checking (DRC), layout-versus-schematic (LVS) check-
are not adequately captured by broader LLM-for-EDA surveys.              ing, and power- and signal-integrity analysis, followed by
Unlike prior reviews that treat verification as a secondary com-         post-silicon validation. Because verification can expose design
ponent of the design flow, this survey systematically organizes          defects or specification violations at any stage, the flow is
the literature across the complete verification pipeline, in-            inherently iterative, with verification results potentially trig-
cluding SystemVerilog Assertion (SVA) generation, testbench              gering revisions to earlier design stages. This survey focuses
and stimulus generation, bug localization, debugging, design             on functional (logic) verification at the RTL and gate levels.



                                                                     2
                                                             TABLE I
  C OMPARISON OF EXISTING SURVEYS AND THE PROPOSED SURVEY. A CHECKMARK (✓) INDICATES SUBSTANTIAL COVERAGE OF A TOPIC , WHILE △
                                            DENOTES PARTIAL OR HIGH - LEVEL DISCUSSION .

 Survey             EDA-wide   RTL Gen.   SVA Gen.   Testbench    Debug   Repair   Benchmarks Verification-   Scope
                                                     / Stimulus                               Centric
 Pan et al. [11]    ✓          ✓          △          △            △       △        △          ×               Broad survey of LLM applications across EDA workflow
 Xu et al. [12]     ✓          ✓          △          △            △       △        ×          ×               Overview of LLMs in design, testing, optimization, and automation
 Yang et al. [30]   ×          ✓          ×          ×            ×       ×        ✓          ×               Focused on Verilog/RTL code generation models, datasets, and evaluation
 Zang et al. [28]   ✓          ✓          ×          ×            △       △        ×          ×               Agentic EDA and autonomous RTL-to-GDSII workflows
 Liu et al. [32]    ×          ×          ✓          ✓            ✓       △        △          ✓               Overview of LLM-assisted circuit verification
 This Survey        ×          △          ✓          ✓            ✓       ✓        ✓          ✓               Comprehensive survey of LLMs for verification, including assertion generation, testbench/stimulus generation,
                                                                                                              bug localization, debugging, RTL repair, datasets, benchmarks, evaluation methodologies, tool integration, and
                                                                                                              open challenges




                                                                                                       methods, including model checking and equivalence checking,
                                                                                                       mathematically establish specified properties or behavioral
                                                                                                       equivalence and can expose corner cases that are difficult
                                                                                                       to reach through simulation [34, 35, 36]. These techniques
                                                                                                       commonly rely on Boolean SAT [37, 38] and Satisfiability
                                                                                                       Modulo Theories (SMT) solvers [39, 40], while emulation
                                                                                                       and FPGA-based prototyping accelerate the execution of large
                                                                                                       workloads that are impractical to explore through software
                                                                                                       simulation.
                                                                                                          A typical functional-verification flow develops a testbench
                                                                                                       that generates stimulus, drives the design under test (DUT),
                                                                                                       monitors responses, and checks observed behavior against
                                                                                                       expected results. Verification engineers must also develop
                                                                                                       test scenarios, assertions, checkers, and coverage models, fol-
                                                                                                       lowed by iterative simulation, failure diagnosis, and regression
                                                                                                       testing. Coverage metrics help identify untested functionality
                                                                                                       and guide subsequent verification, but no single metric can
                                                                                                       establish verification completeness [33]. Moreover, verification
                                                                                                       remains difficult to scale because modern designs exhibit
                                                                                                       enormous input and state spaces, long temporal behaviors, and
                                                                                                       complex interactions among components and software. Simu-
                                                                                                       lation may fail to exercise difficult-to-reach behaviors, while
                                                                                                       formal methods face state-space explosion and scalability lim-
                                                                                                       itations [34, 41]. Developing verification artifacts, diagnosing
                                                                                                       failures determining whether apparent coverage gaps repre-
                                                                                                       sent genuine verification deficiencies also requires substantial
                                                                                                       hardware expertise and engineering effort. These challenges
                                                                                                       motivate increasing interest in automation, including LLM-
                                                                                                       based methods for generating verification artifacts, exploring
                                                                                                       design behavior, and assisting verification and debugging.

                                                                                                       C. Large Language Models
              Fig. 1. A simplified overview of hardware design flow.                                      Large Language Models (LLMs) are deep learning mod-
                                                                                                       els trained on large-scale text and source-code corpora to
                                                                                                       learn general-purpose representations of language, program-
B. Verification Concepts and Techniques                                                                ming constructs, and domain knowledge. Most modern LLMs
   Hardware functional verification aims to establish that an                                          are based on the Transformer architecture [42], whose self-
implementation conforms to its intended functional and tempo-                                          attention mechanism enables effective modeling of long-range
ral behavior. It primarily combines simulation-based verifica-                                         dependencies and highly parallelized training. LLMs are typ-
tion, formal methods, and hardware-assisted techniques. Sim-                                           ically developed through large-scale pre-training followed by
ulation remains the dominant approach, exercising the design                                           post-training, such as supervised fine-tuning and preference- or
with directed or constrained-random stimuli and using cover-                                           feedback-based optimization, which adapts general capabilities
age metrics to guide verification progress; methodologies such                                         toward instruction following and task-specific behavior.
as the Universal Verification Methodology (UVM) support                                                   LLMs can be adapted to downstream tasks through prompt-
reusable and modular verification environments [33]. Formal                                            ing, including few-shot and reasoning-oriented strategies such



                                                                                                   3
as chain-of-thought prompting [43]. These capabilities are par-         fication artifacts while retaining conventional simulation and
ticularly relevant to hardware verification, where an LLM may           formal-verification tools as the final validation mechanisms.
need to interpret specifications, identify relationships among             Beyond RTL generation and verification, LLMs are being
signals and modules, generate assertions or test scenarios, and         applied across the EDA optimization stack. At the HLS level,
reason about verification failures. However, LLM-generated              approaches such as C2HLSC and HLSPilot use LLMs to
reasoning and artifacts are not correctness guarantees, moti-           transform and optimize HLS code [6], [7]. At the physical-
vating the use of external knowledge and deterministic verifi-          design level, agent-based frameworks such as ChatEDA em-
cation mechanisms.                                                      ploy LLMs to decompose design tasks, generate tool scripts,
   Retrieval-Augmented Generation (RAG) [44] supplements                and orchestrate conventional EDA tools from RTL through
model knowledge with task-specific information retrieved at             physical implementation [8]. Collectively, these efforts exploit
inference time. For hardware verification, retrieved context            three capabilities of LLMs—cross-domain semantic mapping,
may include specifications, RTL modules, interface descrip-             pattern recognition, and automated reasoning—to bridge high-
tions, protocol documentation, assertions, verification plans, or       level design intent with executable artifacts, including HDL
debugging records. LLMs can also interact with external tools,          code, verification programs, and EDA scripts. Rather than
using approaches such as ReAct [45] and Toolformer [46],                replacing established EDA algorithms, LLMs increasingly
to invoke simulators, formal engines, compilers, coverage               serve as intelligent interfaces and assistants that automate
analyzers, or other EDA tools and use their outputs to refine           repetitive tasks, guide design-space exploration, and enable
subsequent actions. This tool-grounded interaction is particu-          engineers to focus on architecture, corner cases, and other
larly important for verification because deterministic tools can        tasks requiring domain expertise.
independently evaluate generated artifacts.
   Agentic LLM systems extend these capabilities by decom-                   III. S YSTEM V ERILOG A SSERTION G ENERATION
posing complex tasks into multiple steps, maintaining inter-               This section first overviews SVA generation and the moti-
mediate state, invoking tools, and iteratively refining results;        vations of using LLMs. Then, it survyes recent LLM-based
multi-agent frameworks can further assign specialized roles             SVA generation methods at inference time and training time
such as planning, generation, verification, and debugging [47].         as summarzed in Table II. Next, it reviews evaluation methods
These workflows, however, must manage the limited context               and bechmarks for SVA generation methods as summarized in
available to each model invocation. Large RTL hierarchies,              Table III. Finally, remaining challenges and future directions
specifications, testbenches, waveforms, and tool logs can ex-           are highlighted.
ceed practical context limits, motivating long-context models,
retrieval, summarization, and structured representations. To-           A. Overview and Motivation
gether, reasoning, retrieval, tool use, and agentic orchestration          Assertion-Based Verification (ABV) expresses expected
provide the foundation for applying LLMs to hardware verifi-            hardware behavior as executable properties that can be evalu-
cation, while deterministic verification tools remain essential         ated through simulation or formally proven against an imple-
for validating their outputs.                                           mentation. SystemVerilog Assertions (SVAs) are the dominant
                                                                        assertion language, used in approximately 80% of projects
D. LLMs for EDA                                                         employing ABV [5]. SVAs capture functional and temporal
   The integration of Large Language Models (LLMs) into                 requirements, such as protocol rules, request–response rela-
Electronic Design Automation (EDA) flows is enabling in-                tionships, ordering constraints, and reset behavior, thereby
creasingly autonomous and machine-augmented hardware de-                providing an explicit representation of design intent. They
sign workflows. Early efforts such as VeriGen demonstrated              improve observability and debugging and enable formal ex-
domain adaptation by fine-tuning open-source models on                  ploration of behaviors that may be difficult to exercise through
Verilog corpora [1]. Subsequent approaches have explored                simulation.
natural-language-driven RTL generation and iterative refine-               Despite these advantages, developing high-quality SVAs
ment, with frameworks such as AutoChip incorporating com-               remains knowledge-intensive and time-consuming. Verifica-
piler and simulation feedback into multi-turn generation loops          tion engineers must interpret requirements distributed across
to identify and correct syntactic and functional errors [2],            natural-language specifications, tables, diagrams, and timing
while RTLCoder demonstrated the effectiveness of domain-                descriptions; identify the behaviors that require verification;
specific training data and lightweight open-source models on            map abstract concepts to implementation signals; and encode
benchmarks such as RTLLM and VerilogEval [3].                           them using precise temporal semantics. Ambiguous or incom-
   Hardware verification is another major application area.             plete specifications further widen this semantic gap between
LLM-based approaches have been developed to automate ver-               high-level design intent and executable assertions.
ification collateral generation, including testbenches through             Accordingly, automated SVA generation must address more
frameworks such as AutoBench [4], and assertion generation              than syntactic correctness. A useful assertion must be syn-
from natural-language design specifications through systems             tactically valid, semantically consistent with the intended re-
such as AssertLLM [5]. These methods reduce the manual                  quirement, and correctly aligned with implementation signals
effort required to translate design intent into executable veri-        and cycle-level timing. These requirements are distinct: an



                                                                    4
                                                                     TABLE II
                   R EPRESENTATIVE RELATED WORK ON LLM- ASSISTED SVA GENERATION ACROSS TRAINING - AND INFERENCE - TIME TECHNIQUES

Work                  Pre- or       Technique stage Generation style                                      Feedback / evaluation                            Main contribution                                 Key limitation
                      Post-RTL

nl2sva [48]           Post-RTL      Inference           Circuit-aware few-shot prompting with editable JasperGold/model-checker feedback with            Early circuit-aware NL-to-SVA translation           Proof-of-concept evaluation; substantial human
                                                        sub-translations                                human review                                                                                         interaction
AssertLLM [23]        Pre-RTL       Inference           Multi-LLM task decomposition with structured JasperGold FPV on I2C; syntax and proof pass Full-specification multimodal generation using             Limited benchmark scope; no
                                                        text/waveform IRs                               rates                                            intermediate representations                        verifier-in-the-loop refinement
AutoSVA2 [49]         Post-RTL      Inference           GPT-4 RTL prompting with engineered             FPV counterexamples and coverage on CVA6 Integrates direct RTL-to-SVA generation with                Requires engineer auditing/refinement and
                                                        syntax/semantic rules                           PTW/TLB                                          AutoSVA                                             formal-tool access
AssertionForge [25] Post-RTL        Inference           Spec+RTL knowledge graph with RAG/SSR           JasperGold proof plus COI                        Structured spec–RTL grounding for broader           KG overhead; no verifier-in-the-loop SVA
                                                        and GRW-AS retrieval                            statement/branch/functional/toggle coverage      assertion generation                                refinement
ChiRAAG [50]          Post-RTL      Inference           Structured-spec prompting with iterative        Simulation/test-case feedback on OpenTitan       Early automatic simulator-feedback refinement       Few test cases; limited completeness/coverage
                                                        simulation-log repair                           designs                                          of generated SVAs                                   guarantees
SANGAM [24]           Post-RTL      Inference           Multimodal agents with Monte Carlo Tree         JasperGold proof/coverage feedback on I2C        Search-based self-refinement for multimodal         Two-design evaluation; compute/tool-intensive
                                                        Self-Refine (MCTSr)                             and RV-Timer                                     SVA generation                                      refinement
AssertCraft [51]      Post-RTL      Training +          Subtask-focused fine-tuning plus iterative      Custom compiler and FPV on HDLBits-derived Combines task-specific fine-tuning with                   Requires curated training data and golden RTL;
                                    Inference           compiler/FPV-guided prompting                   designs                                          automated syntax/semantic repair                    gains are coupled to refinement loop
AssertCoder [52]      Pre-RTL       Inference           Multimodal extraction plus semantic analyzers Mutation-based model checking and refinement Unified text/table/diagram/formula-to-SVA                 Extraction errors propagate; evaluation limited
                                                        and multi-step CoT                              on three designs                                 generation                                          to three designs
Spec2Assertion [53] Pre-RTL         Inference           Progressive regularization with CoT and         JasperGold FPV plus RTL-derived                  Explicit pre-RTL generation and                     Evaluation metric still requires golden RTL
                                                        property decomposition                          assertion-importance score                       assertion-quality metric
AssertGen [54]        Post-RTL      Inference           CoT objectives with cross-layer spec-to-RTL     FPV, COI/proof-core, and mutation coverage on Generates assertions over internal cross-layer         Requires RTL/signal artifacts; no closed-loop
                                                        signal bridging                                 five designs                                     signal chains                                       refinement
ChatSVA [55]          Pre-RTL       Training +          Four task-specific agents with AgentBridge data Formal verification on 24 designs; pass rate and Specialized trained agents for high-coverage        Heavy data/training pipeline; formal evaluation
                                    Inference           generation, SFT, and RAG                        coverage                                         end-to-end SVA generation                           still depends on RTL oracle
SuperSAGA [56]        Post-RTL      Inference           Supervisor–subordinate agents with RAG and      Iterative formal-tool feedback; OpenTitan        Agent hierarchy for generation, debug, and          Requires human-reviewed verification plans and
                                                        verification plan                               coverage evaluation                              refinement                                          formal tools
SVAgent [57]          Post-RTL      Inference           Security-property decomposition with            Pyverilog/TrustHUB; syntax and functional        Security-focused SVA generation with                Limited to selected threat models/vulnerability
                                                        RTL/FSM analysis                                accuracy                                         structured reasoning chains                         classes
Saarthi [58]          Post-RTL      Inference           Multi-agent vPlan-to-SVA, proof/CEX repair,     Formal proof, counterexamples, coverage, and End-to-end AI formal-verification engineer              Human intervention remains for unresolved
                                                        and coverage closure                            human escalation                                 workflow                                            agent loops
ProofLoop [59]        Post-RTL      Inference           ReAct agent with AST-RAG and JasperGold         Three-round JasperGold proof refinement on       Adaptive RTL retrieval with solver-in-the-loop      Requires retrieval infrastructure and
                                                        structural queries                              FVEval Design2SVA                                generation                                          commercial FV tooling
KG-Based Agentic      Post-RTL      Inference           Spec+RTL+feedback KG with                       Formal diagnostics, CEX, and coverage on         Persistent traceable grounding across the FV        Complex KG/agent state; design-dependent
FV [60]                                                 syntax/CEX/coverage refinement loops            seven benchmarks                                 workflow                                            convergence

Validatable           Pre-RTL       Training            Fine-tuned CodeT5/PLBART for NL-to-SVA            Back-translation/cycle-consistency similarity;   Early supervised NL-to-SVA translation with an Property-level input only; no full-specification
Generation [61]                                         with back-translation validation                  no RTL formal check                              interpretable validation loop                  extraction or RTL validation
VERT [62]             Post-RTL      Training            LoRA fine-tuning of LLaMA 3.1 and                 Syntax plus mutation, formal, and                Large domain-specific SVA dataset showing      RTL-snippet task; limited evidence for full
                                                        DeepSeek Coder on Verilog/SVA pairs               simulation-based functional checks               strong gains from local fine-tuning            specification-driven generation
Hybrid-NL2SVA         Pre-RTL       Training +          Qwen2.5-Coder supervised fine-tuning              Formal evaluation on 40 designs and 229          Demonstrates complementary gains from SFT Targets property-level translation rather than
[63]                                Inference           combined with customized HybridRetrieval          annotated SVAs                                   and retrieval for NL-to-SVA                    property extraction/full-spec generation
                                                        RAG




                                                                                        TABLE III
                                                       R EPRESENTATIVE DATASETS AND BENCHMARKS FOR LLM- ASSISTED SVA GENERATION

Dataset /              Primary use        Scale                Inputs / targets                                 Construction / source                           Evaluation / intended use                        Key limitation
benchmark

AssertLLM [23]         Evaluation         20 designs           Complete specifications + golden RTL;            Open-source IP and system-level designs         Syntax, FPV pass/fail, and COI/proof             Small design set and assumes bug-free
                                                               generated SVAs are evaluated against the         with full natural-language specifications and   coverage using formal verification               golden RTL; formal success is only a proxy
                                                               design                                           verified RTL                                                                                     for specification alignment
VERT [62]              Training           20,000 samples       RTL/code snippets → SVA                          Synthetic if-else, case, and combined-logic     Domain-specific fine-tuning of open-source       Synthetic snippet-level data does not
                                                                                                                snippets using variables extracted from         LLMs for SVA generation                          represent complete specifications, modules,
                                                                                                                open-source HDL projects; synchronous and                                                        or hierarchical design intent
                                                                                                                asynchronous cases
AssertionBench [64]    Evaluation +       100 designs          Verilog design → assertion set                   Curated OpenCores designs; assertions mined     In-context learning and fine-tuning studies;     RTL-to-SVA setting lacks natural-language
                       training                                                                                 with GoldMine/HARM and formally verified        syntax and FPV proof/counterexample              specification intent and inherits biases of
                                                                                                                with JasperGold                                 outcomes                                         mined reference assertions
FVEval [65]            Evaluation         571 cases            NL/testbench → SVA; synthetic NL →               79 expert NL2SVA cases, 300 synthetic           Syntax and formal functional/equivalence         Human subset is small; two subsets are
                                                               SVA; RTL → SVA                                   NL2SVA cases, and 192 generated RTL             checking across three assertion-generation       synthetic and do not model full
                                                                                                                cases (96 pipelines + 96 FSMs)                  settings                                         specification-driven verification
Hybrid-NL2SVA          Training +         4,070 training       Natural-language property/explanation →          Synthetic fine-tuning corpus with               Fine-tuning/RAG evaluation using syntax and      Focuses on property-level NL2SVA
[63]                   evaluation         examples; 40         SVA                                              prompt-guided SVA construction                  functional/formal matching                       translation rather than extracting properties
                                          designs / 229                                                         explanations; separate formally verified                                                         from complete specifications or RTL
                                          SVAs for                                                              annotated evaluation set
                                          evaluation
CVDP-cid14 [66]        Evaluation         98 assertion tasks   Verification prompt/context → SVA                Human-authored tasks within the                 Executable test-harness/simulation-based pass    Assertion generation is only one CVDP
                                                                                                                783-problem CVDP suite; 68 non-agentic          evaluation in realistic single- and multi-step   category and simulation/harness success does
                                                                                                                and 30 agentic assertion-generation problems    settings                                         not establish formal or semantic correctness
AssertLLM2 [67]        Evaluation         83 designs, 13       Structured specification + golden/buggy RTL      Real-world open-source designs (filtered for    Syntax, formal provability, COI/proof/formal     Still relatively small and untested among the
                                          categories           → SVA                                            > 200 RTL lines), normalized                    coverage, and mutation-based bug detection       broader LLM for SVA generation community
                                                                                                                specifications, dependency-complete RTL,        in bug-prevention and bug-hunting settings
                                                                                                                and systematic mutations




assertion may compile successfully yet express the wrong                                                                              1) Automated SVA Generation Before LLMs: Before LLMs,
behavior, while an assertion formally proven against RTL                                                                           automated assertion generation primarily relied on templates,
may still misrepresent the specification. Signal and timing                                                                        rules, static analysis, and mining of simulation traces. Gold-
alignment is particularly challenging because specifications                                                                       Mine [68] mines candidate invariants from simulation traces,
often describe behavior abstractly, whereas SVAs must iden-                                                                        maps them to predefined assertion templates, and applies for-
tify concrete signals, sampling events, delays, and temporal                                                                       mal verification to eliminate invalid candidates. A-Team [69]
relationships. Beyond individual assertions, practical genera-                                                                     combines templates with data mining and coverage-guided
tion should produce an assertion set that provides adequate                                                                        heuristics, while HARM [70] uses user-provided propositions,
specification coverage while avoiding vacuous, redundant, or                                                                       templates, and metrics to generate temporal properties.
inconsistent properties.                                                                                                              These approaches provide predictable and structured gen-
                                                                                                                                   eration, but their expressiveness is constrained by prede-



                                                                                                                               5
fined templates, propositions, or observed execution behav-              multimodal, tool-grounded, and agentic workflows that address
ior. Consequently, they can struggle with previously unseen              different stages of the specification-to-SVA transformation.
property structures, complex temporal relationships, and re-                1) Structured Decomposition and Design Grounding:
quirements expressed only at the specification level. Trace-             NL2SVA [48] is among the earliest LLM-based approaches
mining methods may also infer properties that happen to hold             and translates manually provided natural-language property
for the observed implementation rather than properties repre-            descriptions into an intermediate representation containing
senting intended behavior. More fundamentally, conventional              signal information, partial translations, and candidate SVAs.
approaches have limited capability to interpret unstructured             Model checking is subsequently used to validate the asser-
specifications and determine what properties should be veri-             tions, with human intervention when refinement is required.
fied, leaving a semantic gap between design requirements and             Although this workflow demonstrates the feasibility of com-
generated assertions.                                                    bining LLM generation with formal verification, it assumes
   2) Motivation for LLM-Based SVA Generation: LLMs offer                that relevant requirements have already been extracted from
a complementary capability by interpreting natural-language              the specification and therefore does not automate the more
requirements, generating code, and reasoning across hetero-              difficult task of identifying verification properties from com-
geneous design information. They can potentially extract                 plete design documents.
behavioral relationships from specifications, translate them                AssertLLM [23] extends this direction toward end-to-end
into temporal properties, and, when RTL is available, map                generation from complete specifications. Rather than directly
specification concepts to concrete signals and implementation            prompting an LLM with the entire document, it decom-
structures. Retrieval and multimodal techniques can further in-          poses the task into specification analysis, signal mapping,
corporate information from large documents, tables, diagrams,            and assertion generation, thereby producing structured in-
and waveforms. These capabilities make LLMs particularly                 termediate descriptions before generating SVAs. It also in-
attractive for bridging the specification-to-assertion semantic          corporates assertion-related knowledge through retrieval and
gap.                                                                     processes textual and waveform information. This decompo-
   However, LLM generation is probabilistic and provides no              sition reduces the reasoning burden of a single inference step
correctness guarantee. Generated assertions may contain syn-             and makes intermediate results more inspectable. However,
tax errors, incorrect temporal relationships, erroneous signal           because AssertLLM derives its design knowledge primarily
mappings, or properties that appear plausible but do not reflect         from the specification, implementation details absent from the
design intent. Recent approaches therefore increasingly com-             specification can remain unresolved.
bine LLM generation with structured design representations,                 AssertionForge [25] addresses this limitation by jointly
retrieval, simulation, formal verification, coverage analysis,           grounding generation in the specification and RTL. It con-
and iterative refinement. In such workflows, LLMs provide                structs a hardware-specific knowledge graph (KG) from spec-
semantic interpretation and candidate generation, while deter-           ification concepts and fuses it with RTL entities and rela-
ministic verification tools provide feedback for validation and          tionships, followed by multi-resolution context extraction for
refinement.                                                              SVA generation. Compared with the primarily specification-
   A key distinction is whether assertions are generated be-             centered decomposition of AssertLLM, this representation ex-
fore or after RTL becomes available. Pre-RTL approaches                  plicitly connects high-level requirements with implementation-
derive properties primarily from specifications and therefore            level signals and dependencies, improving the context avail-
preserve greater independence from implementation errors,                able for assertion generation. The tradeoff is increased pre-
but face difficulties in mapping abstract requirements to con-           processing complexity and greater dependence on the RTL:
crete signals and cycle-level timing. Post-RTL approaches                errors in KG construction or an incorrect implementation
use implementation information to improve signal and timing              can propagate into generated properties, potentially weakening
grounding and produce more readily executable assertions,                their independence as specification-level checks.
but risk generating properties that reproduce erroneous RTL                 AutoSVA2 [49] similarly introduces intermediate rules
behavior rather than independently checking the specification.           to constrain SVA generation. Collectively, these approaches
Thus, effective LLM-based SVA generation must balance                    show that intermediate representations—including structured
specification fidelity with implementation grounding, using              descriptions, rules, and knowledge graphs—are useful for
RTL to resolve implementation details without allowing it to             decomposing the large semantic jump from heterogeneous
override the verification intent established by the specification.       specifications to temporal logic. However, additional repre-
                                                                         sentations also create new points at which information can be
B. Inference-Time Methods                                                omitted or incorrectly transformed.
   Inference-time approaches generate SVAs using pretrained                 2) Multimodal Processing and Explicit Reasoning: Hard-
LLMs without modifying their model parameters. Compared                  ware specifications frequently encode critical behavior in
with fine-tuning-based methods, they can readily incorporate             tables, timing diagrams, waveforms, equations, and figures
new specifications, RTL designs, retrieved knowledge, and                rather than text alone. AssertLLM [23] incorporates wave-
verification-tool feedback. Existing methods have evolved                form information, while AssertCoder [52] more explicitly de-
from direct natural-language translation toward structured,              composes multimodal specification processing by converting



                                                                     6
diagrams, waveforms, tables, and formulas into structured               refinement, this approach reduces dependence on a single
representations such as pseudocode, formal expressions, LATEX,          stochastic generation and can explore alternatives involving
or JSON before assertion generation. SANGAM [24] likewise               different signal dependencies or temporal relationships. How-
employs specialized Spec Analyzer, Signal Mapper, and Wave-             ever, its effectiveness depends critically on the reward or se-
form Analyzer components to extract complementary informa-              lection criterion; optimizing primarily for formal-tool success
tion from specifications. These approaches reduce dependence            can favor assertions that are provable but weak, vacuous,
on textual descriptions and can recover timing or structural            or semantically misaligned. SANGAM therefore represents
information unavailable in prose. Their effectiveness, however,         a shift from simply repairing a generated assertion toward
depends on the accuracy of multimodal interpretation; an in-            searching the space of candidate interpretations.
correctly interpreted waveform or table can introduce semantic             AssertCoder [52] and AssertGen [54] further incorporate
errors before SVA generation begins.                                    mutation testing to evaluate whether generated assertions
   Explicit reasoning provides another mechanism for bridging           detect injected RTL faults. This provides stronger evidence
specifications and temporal properties. Spec2Assertion [53]             of verification usefulness than syntax or proof success alone
applies Chain-of-Thought (CoT) prompting and progressive                because it evaluates fault-detection capability. Nevertheless,
regularization in the pre-RTL setting, encouraging the model            mutation score remains dependent on the representativeness
to reason about antecedents, consequents, temporal relation-            of the injected faults and does not by itself establish that an
ships, and cycle dependencies before constructing an SVA.               assertion faithfully represents the specification.
AssertCoder [52] extends multi-step reasoning to structured                4) Agentic SVA Generation: The progression from task de-
multimodal inputs, whereas AssertGen [54] first extracts verifi-        composition and iterative refinement naturally leads to agentic
cation objectives from the specification and subsequently maps          workflows, in which specialized components coordinate spec-
them to RTL signals. The latter approaches therefore combine            ification analysis, retrieval, assertion generation, tool execu-
explicit reasoning with implementation grounding, addressing            tion, and repair. AssertLLM [23] and SANGAM [24] already
a major limitation of purely pre-RTL reasoning. Nevertheless,           exhibit elements of role-based decomposition, although their
a plausible reasoning trace is not evidence of semantic correct-        primary contributions are structured generation and search
ness: incorrect timing assumptions or incomplete interpretation         rather than autonomous tool orchestration.
of the requirement can still produce well-formed but incorrect             More explicit agentic approaches extend this decomposition.
assertions.                                                             ChatSVA [55] formulates SVA generation as an end-to-end
   3) Retrieval and Verification-Guided Refinement: Retrieval-          multi-agent workflow with specialized stages for specifica-
Augmented Generation (RAG) provides external knowledge                  tion processing, functional-checkpoint extraction, and asser-
without modifying the LLM. AssertLLM [23], for exam-                    tion generation, while its AgentBridge infrastructure supports
ple, retrieves SVA-related verification knowledge to improve            construction of task-specific data. SuperSAGA [56] uses a
generation, whereas AssertionForge [25] uses graph-based                supervisor–subordinate architecture combining RAG, human-
retrieval over design-specific relationships. The distinction is        reviewed verification plans, formal-tool feedback, and iterative
important: general verification knowledge primarily helps the           assertion refinement. SVAgent [57] applies agentic decomposi-
model understand how to express assertions, while design-               tion specifically to hardware-security verification by breaking
specific retrieval helps determine what behavior should be              complex security requirements into finer-grained verification
expressed. The latter is therefore more directly relevant to            tasks before SVA generation.
specification-to-RTL semantic alignment.                                   This direction also overlaps increasingly with broader agen-
   Most recent frameworks further couple generation with                tic formal-verification systems. Saarthi [58], ProofLoop [59],
iterative feedback. NL2SVA [48] introduced model-checking               and KG-based agentic formal-verification frameworks [60]
feedback with human-guided refinement, while general self-              coordinate assertion generation with mechanisms such as
refinement methods such as Self-Refine [71] demonstrated                verification rulebooks, knowledge-graph retrieval, formal-
that LLMs can critique and revise their own outputs. ChI-               tool queries, counterexample-guided refinement, and coverage
RAAG [50] applies verification-tool feedback to SVA cor-                feedback. These systems expand the role of the LLM from
rection by interpreting errors and regenerating failed asser-           an assertion generator to an orchestrator of the verification
tions. Such feedback is particularly effective for syntax and           process. However, greater autonomy also increases pipeline
tool-detectable errors because compilers and formal engines             complexity, inference and tool-execution cost, and opportu-
provide objective diagnostics. Its ability to correct semantic          nities for error propagation. Consequently, agentic decom-
errors is more limited: a property that successfully compiles           position is most useful when intermediate artifacts such as
or is proven against the RTL may still encode the wrong                 extracted requirements, signal mappings, verification plans,
requirement.                                                            and candidate assertions can themselves be independently
   SANGAM [24] extends linear self-refinement into candidate            validated rather than trusting only the final output.
search through Monte Carlo Tree Self-Refine (MCTSr). After                 5) Summary and Remaining Limitations: Overall,
multimodal specification processing, it explores multiple rea-          inference-time SVA generation has evolved along several
soning trajectories for individual signals and uses the resulting       complementary dimensions. Early methods such as NL2SVA
traces to generate assertions. Compared with one-shot or linear         focus on translating explicitly provided requirements,



                                                                    7
whereas AssertLLM expands generation to complete                       language statement. It therefore addresses property translation
specifications through task decomposition. AssertionForge              rather than the broader problem of extracting verification
and AssertGen strengthen specification-to-RTL grounding;               requirements from complete specifications. Moreover, back-
AssertCoder and SANGAM incorporate multimodal                          translation measures linguistic consistency rather than behav-
information; Spec2Assertion emphasizes explicit reasoning;             ioral correctness; an assertion can appear consistent in natural
SANGAM further introduces search over alternative reasoning            language while still containing incorrect temporal semantics
trajectories; and recent agentic frameworks coordinate these           or failing to represent the RTL behavior correctly.
capabilities with external verification tools. Thus, the                  Hybrid-NL2SVA follows a similar property-translation
field is moving from direct NL-to-SVA translation toward               formulation but combines domain-specific fine-tuning with
specification understanding, design grounding, candidate               inference-time augmentation. It fine-tunes Qwen2.5-Coder-
generation, verification, and iterative refinement.                    7B-Instruct using a synthetic dataset constructed from
   Despite this progression, three limitations remain common.          hardware-design textbooks and Verilog collected from 67
First, stronger RTL grounding improves signal mapping and              designs, containing 4,070 SVAs paired with one-sentence
executability but can compromise independence from imple-              natural-language descriptions generated using OpenAI o4-
mentation errors, whereas specification-only methods preserve          mini. The resulting model shows substantial improvement after
verification intent but struggle with implementation-level de-         fine-tuning, while retrieval-based augmentation further im-
tails. Second, tool feedback provides reliable evidence for            proves generation. Compared with the earlier CodeT5/PLBart
syntax, satisfiability, and behavior relative to the RTL, but          approach, Hybrid-NL2SVA benefits from a stronger pretrained
does not by itself establish semantic agreement with the               code model, a larger hardware-specific dataset, and a hy-
specification. Third, increasingly elaborate reasoning, search,        brid training/inference strategy. Nevertheless, both approaches
and multi-agent pipelines improve robustness at the expense of         share the same fundamental abstraction: they assume that a
latency, tool calls, computational cost, and additional opportu-       relevant property has already been extracted and expressed in
nities for intermediate errors. Future inference-time methods          natural language. Their results therefore demonstrate improved
therefore need to combine specification fidelity and implemen-         NL-to-SVA translation, but provide limited evidence for full
tation grounding while independently validating intermediate           specification-driven assertion generation. In addition, synthetic
representations and evaluating generated assertion sets using          natural-language labels and automatically collected assertions
complementary measures of semantic correctness, coverage,              make performance dependent on the semantic quality of the
non-vacuity, and realistic fault-detection capability.                 constructed training pairs.
                                                                          2) Specification-Conditioned and Hybrid Fine-Tuning: As-
C. Training-Time Methods                                               sertCraft [51] moves closer to specification-driven generation
   Training-time approaches adapt an LLM to SVA genera-                by fine-tuning an LLM using assertion-related examples ex-
tion by updating its parameters using hardware-verification-           tracted and filtered from open-source repositories together with
specific data. Unlike inference-time methods, which rely on            synthetic data. Rather than relying exclusively on the fine-
prompting, retrieval, structured context, search, or tool feed-        tuned model, AssertCraft combines task-specific adaptation
back without modifying the underlying model, fine-tuning               with an inference-time iterative refinement loop in which
attempts to internalize SVA syntax, temporal semantics, and            candidate assertions can be repaired using a non-fine-tuned
recurring hardware-property patterns. This can improve gen-            LLM. This hybrid architecture is significant because it treats
eration consistency and enable smaller open-source models              fine-tuning and inference-time reasoning as complementary:
to perform specialized verification tasks. However, because            fine-tuning provides domain-specific generation capability,
SVA generation involves multiple stages—including require-             while iterative refinement addresses errors that remain after
ment extraction, signal mapping, temporal reasoning, and               generation.
assertion construction—most existing training-time methods                This design also illustrates an important difficulty in eval-
focus on particular subtasks rather than learning the complete         uating training-time approaches. Improvements in AssertCraft
specification-to-SVA process.                                          arise from several interacting components, including dataset
   1) Property-Level Translation and Semantic Adaptation:              construction, task decomposition, the fine-tuned generator, and
Aditi and Hsiao [61] provide an early demonstration of fine-           iterative refinement. Consequently, end-to-end improvements
tuning for SVA generation by adapting CodeT5 and PLBart                cannot necessarily be attributed to fine-tuning alone without
to translate natural-language property descriptions into asser-        controlled ablation. More generally, fine-tuning can improve
tions. The generated SVA is additionally translated back into          the model’s prior knowledge of SVA patterns but does not
natural language and compared with the original description,           eliminate the need for specification grounding or external ver-
providing an interpretable consistency check between the input         ification. A model trained on high-quality assertion examples
requirement and generated property. This work demonstrates             may still generate a property that is inappropriate for the
that task-specific training can teach models the correspon-            particular design being verified.
dence between natural-language temporal behavior and SVA                  3) Domain-Specific Model Adaptation: VERT [62] further
constructs. However, it assumes that the desired property has          emphasizes the value of domain-specific training data. It con-
already been identified and expressed as a concise natural-            structs a large SVA dataset from open-source hardware designs



                                                                   8
and uses it to fine-tune DeepSeek Coder and LLaMA 3.1                   cation objectives, assertions, and verification outcomes. Train-
models, which are subsequently compared with GPT-4o across              ing objectives could similarly move beyond next-token pre-
multiple hardware designs. The results show that smaller open-          diction on individual assertions toward learning specification-
source models adapted to hardware-verification data can out-            to-property alignment, signal grounding, temporal reasoning,
perform a substantially larger general-purpose closed-source            and assertion-set construction. Importantly, fine-tuning should
model on the evaluated SVA-generation tasks. This provides              not replace deterministic verification: compilation, simulation,
important evidence that, for specialized verification tasks,            formal analysis, vacuity checking, and mutation testing remain
domain adaptation can compensate for model scale. Fine-tuned            necessary for independently evaluating generated properties.
open-source models also enable local deployment, which is               A promising direction is therefore a hybrid architecture in
attractive when proprietary RTL and specifications cannot be            which domain-specific training provides efficient hardware-
exposed to external model providers.                                    verification knowledge, while inference-time retrieval and
   VERT, however, also exposes a recurring limitation of                reasoning supply design-specific context and formal tools
current training-time methods: the granularity and provenance           provide objective feedback on correctness and verification
of training data strongly determine what the model learns. As-          effectiveness.
sertions mined from open-source repositories provide realistic
SVA syntax and recurring temporal patterns, but snippet-level           D. Evaluation Methods and Benchmarks
examples contain limited information about the complete spec-
ification and design context from which the assertions origi-              The inference- and training-time methods reviewed above
nated. Consequently, strong performance on local assertion-             employ different mechanisms to improve SVA generation,
generation tasks does not necessarily imply that the model              ranging from structured prompting, retrieval, reasoning, and
can identify appropriate verification objectives from a full            formal-tool feedback to domain-specific fine-tuning. Evalu-
specification, reason across module hierarchies, or construct           ating these methods, however, requires determining not only
a comprehensive assertion set for an unseen IP.                         whether an LLM can produce executable SVA code, but also
   4) Cross-Method Analysis and Limitations: Taken together,            whether the generated properties faithfully capture verifica-
these studies demonstrate a progression from fine-tuning for            tion intent and effectively detect incorrect behavior. Existing
direct NL-to-SVA translation toward domain-adapted mod-                 evaluations can therefore be viewed as providing increasingly
els embedded within larger verification pipelines. Aditi and            strong but complementary forms of evidence: syntactic valid-
Hsiao [61] establish the feasibility of learning mappings be-           ity, formal consistency, coverage, fault-detection capability,
tween natural-language properties and SVA; Hybrid-NL2SVA                and ultimately specification alignment.
scales this formulation using a modern code LLM, synthetic                 1) Evaluation Methodologies: Syntactic validity is the
data, and retrieval; AssertCraft [51] combines fine-tuning with         most basic and widely reported metric. It measures whether
iterative inference-time refinement; and VERT [62] demon-               generated assertions can be parsed, compiled, and accepted by
strates that sufficiently specialized training can make smaller         SystemVerilog verification tools. This metric is inexpensive,
open-source models competitive with or superior to larger               deterministic, and particularly useful for measuring whether
general-purpose models. Thus, training-time and inference-              prompting or fine-tuning improves knowledge of SVA syntax.
time techniques are increasingly complementary rather than              However, compilation establishes only that an assertion is
competing alternatives: fine-tuning internalizes recurring do-          executable; a syntactically correct property may still check
main knowledge, while retrieval, structured context, RTL                the wrong behavior, use inappropriate timing, or encode an
grounding, and verification-tool feedback provide design-               incorrect requirement.
specific information that cannot reasonably be encoded in                  Formal property verification (FPV) provides stronger
model parameters.                                                       behavioral evidence by checking generated assertions against
   Nevertheless, current training-time methods remain primar-           an RTL implementation using formal verification tools such
ily focused on learning how to express properties as SVAs,              as JasperGold or SymbiYosys. If a trusted golden RTL im-
rather than determining which properties are required to                plementation is assumed to correctly realize the specification,
adequately verify a design. Most training datasets consist of           successful proof provides evidence that the generated asser-
assertion snippets or pairs of natural-language descriptions            tion is consistent with the expected design behavior, while
and SVAs, with relatively limited representation of complete            counterexamples can identify incorrect properties. FPV is
specifications, RTL hierarchy, verification intent, and relation-       therefore widely used in benchmarks such as AssertLLM [23],
ships among multiple properties. Dataset construction also              VERT [62], AssertionBench [64], and FVEval [65]. However,
introduces risks from noisy repository assertions, automati-            FPV is not a direct semantic oracle. A weak, vacuous, or
cally generated descriptions, duplicated examples, and possible         incorrectly interpreted assertion may still be provable, and
overlap between training and evaluation designs. These issues           results depend on the RTL, assumptions, constraints, and
make data quality, provenance, and contamination control                formal environment. Proofs may also time out or remain incon-
particularly important when evaluating fine-tuned models.               clusive for complex designs. Thus, FPV primarily establishes
   Future training-time methods therefore require datasets that         consistency with the analyzed implementation, not necessarily
preserve richer relationships among specifications, RTL, verifi-        correctness with respect to the original specification.



                                                                    9
   Coverage analysis complements FPV by measuring how                    evidence than syntax-only evaluation. However, the small
generated properties relate to the implementation. Existing              number of designs limits behavioral and structural diversity
work reports metrics such as cone of influence (COI), proof              and makes broad conclusions about generalization difficult.
coverage, formal coverage, and, depending on the environ-                   VERT [62] takes a substantially different approach. Its
ment, statement, branch, or toggle coverage. AssertLLM [23]              dataset contains approximately 20,000 snippets extracted from
introduced COI-based analysis alongside FPV, while later                 open-source hardware repositories, including BOOM, Rocket
benchmarks such as VERT [62] and AssertLLM2 [67] employ                  Chip, XiangShan, and other RTL projects. Rather than em-
broader coverage measurements. Coverage can expose trivial               phasizing complete specification-to-design tasks, VERT tar-
assertions that constrain or observe little of the design and can        gets recurring SVA-generation patterns and errors, including
assess the collective reach of an assertion set. Nevertheless,           temporal and clock-cycle interpretation. Its scale makes it par-
high coverage does not imply correct verification intent: a              ticularly suitable for training and evaluating domain-adapted
property may involve many RTL signals while still encode                 models, and its combination of syntax, COI, FPV, and mu-
behavior inconsistent with the specification.                            tation testing provides multiple measures of assertion quality.
   Mutation testing evaluates a different dimension—whether              The tradeoff is granularity: snippet-level tasks provide limited
assertions can detect erroneous implementations. Mutations               evidence that a model can identify verification objectives from
are introduced into an otherwise correct RTL design, and gen-            a complete specification or reason across large hierarchical
erated assertions are evaluated according to whether they fail           designs. Thus, VERT is especially valuable for evaluating the
on the faulty versions. AssertCoder [52], VERT [62], and As-             training-time domain adaptation discussed in the previous sub-
sertLLM2 [67] use mutation-based evaluation to complement                section, whereas specification-level benchmarks better exercise
syntax, proof, and coverage metrics. Compared with proving               the inference-time reasoning and grounding pipelines reviewed
assertions only against golden RTL, mutation testing provides            earlier.
stronger evidence of practical fault-detection capability and               AssertionBench [64] occupies an intermediate position. It
assertion strength. However, its validity depends strongly on            contains 100 samples derived from OpenCores designs, with
the realism, diversity, and relevance of the injected faults.            formally proven reference assertions, English descriptions,
Easily detected or artificial mutations may inflate performance,         and corresponding Verilog designs. This construction provides
while generating representative semantic bugs at scale remains           controlled NL-to-SVA tasks while retaining executable RTL
difficult. Mutation score should therefore be interpreted as             for formal validation, making it useful for evaluating in-
a measure of fault-detection effectiveness, rather than direct           context learning and property translation. However, its em-
proof of specification correctness.                                      phasis on syntax and FPV provides limited measurement of
   These metrics evaluate complementary properties rather                assertion-set coverage, fault-detection capability, or fidelity to
than interchangeable notions of correctness. Syntax checking             complete design specifications.
establishes executability; FPV establishes consistency with                 FVEval [65] provides broader task diversity through
RTL under the verification environment; coverage measures                three complementary sub-benchmarks. NL2SVA-Human con-
interaction with or reach into the design; and mutation test-            tains 79 expert-written assertions from real-world verifica-
ing measures ability to detect selected faults. The strongest            tion environments paired with natural-language descriptions;
objective, specification alignment, asks whether an assertion            NL2SVA-Machine contains 300 machine-generated natural-
accurately captures the intended requirement. This remains the           language/SVA pairs; and Design2SVA contains 192 synthetic
most difficult dimension to evaluate automatically because nei-          RTL instances based on arithmetic pipelines and finite-state
ther the RTL nor generated mutations provide an independent              machines. This decomposition is useful because it distin-
semantic oracle when the objective is to verify the implemen-            guishes human-authored property translation, scalable syn-
tation against a natural-language specification. Consequently,           thetic translation, and direct RTL-to-SVA generation rather
no single existing metric is sufficient, motivating evaluation           than collapsing them into a single task. It therefore enables
frameworks that combine multiple complementary measures.                 analysis of how performance changes with the source and
   2) Benchmarks: Existing SVA benchmarks differ substan-                form of the input. However, its primary reliance on syntax
tially in task formulation, design scale, input context, and             checking and FPV again leaves specification coverage, realistic
evaluation methodology, reflecting the evolution from property           fault detection, and full-document semantic alignment largely
translation toward specification- and design-level assertion             unmeasured.
generation.                                                                 CVDP [66] differs from these assertion-specific benchmarks
   AssertLLM [23] introduced one of the earliest standard-               by evaluating SVA generation as one component of a broader
ized benchmarks for specification-driven SVA generation. It              suite of LLM-based EDA tasks. Its assertion subset contains
contains 20 samples drawn from open-source IP and system-                98 tasks with prompts, relevant context, design files, and
level designs, pairing specifications with corresponding RTL.            test harnesses, using checklist-based evaluation and syntax
This pairing is important because it enables evaluation of both          checking. This task-oriented formulation is valuable for as-
specification-conditioned generation and generated assertions            sessing SVA generation within a broader hardware-engineering
against executable implementations. Its evaluation combines              context rather than an isolated translation setting. However,
syntax checking, COI analysis, and FPV, providing stronger               its evaluation provides less evidence about formal correct-



                                                                    10
ness, non-vacuity, coverage, and fault-detection strength than          robustness across repeated runs, and human intervention. Such
assertion-specific benchmarks.                                          multidimensional evaluation is necessary to compare increas-
   AssertLLM2 [67] moves toward a more comprehensive                    ingly sophisticated inference- and training-time approaches
design-level evaluation. It contains 83 samples collected from          and to determine whether improvements in SVA generation
open-source Verilog/SystemVerilog repositories together with            translate into more effective hardware verification.
corresponding specifications, while filtering out designs below
200 lines of RTL to increase task complexity and normal-                E. Challenges and Future Directions
izing specification structure. More importantly, its evaluation            Despite substantial progress from direct NL-to-SVA trans-
combines syntax checking, FPV, COI, proof coverage, formal              lation toward structured, tool-guided, fine-tuned, and agentic
coverage, and mutation testing. Compared with earlier bench-            approaches, several challenges remain before LLM-generated
marks that emphasize one or two dimensions, AssertLLM2                  SVAs can be reliably used in practical verification.
therefore evaluates both whether assertions are executable and             Semantic alignment and evaluation. A fundamental chal-
provable and whether they exercise meaningful portions of               lenge is determining whether generated assertions faithfully
the design and detect injected faults. Its remaining limitation         represent the specification. Existing methods commonly rely
is shared by the broader literature: these tool-based metrics           on syntax checking, formal property verification (FPV), cov-
remain proxies for whether generated assertions faithfully and          erage, and mutation testing. These provide complementary
comprehensively represent the original specification.                   evidence of executability, consistency with RTL, design in-
   3) Cross-Benchmark Analysis and Open Challenges: Taken               teraction, and fault-detection capability, respectively, but none
together, these benchmarks reveal a progression in both task            directly establishes specification fidelity. SpecAlign [72] repre-
complexity and evaluation strength. Property-level benchmarks           sents an initial step toward explicitly evaluating the semantic
such as AssertionBench and portions of FVEval provide                   alignment between generated SVAs and their corresponding
controlled evaluation of NL-to-SVA translation, while VERT              specifications. Nevertheless, specification-level evaluation re-
emphasizes scale and is particularly suited to training-time            mains challenging, particularly when golden RTL is used for
domain adaptation. AssertLLM and AssertLLM2 move toward                 both generation and validation, since an incorrect property de-
complete specification- and design-conditioned generation,              rived from faulty RTL may still be formally proven against that
better exercising the reasoning, retrieval, signal-grounding,           RTL. Future evaluation should therefore combine complemen-
and refinement capabilities of inference-time systems. CVDP             tary metrics with independent specification-level assessment.
instead evaluates assertion generation within a broader EDA             Standardized benchmarks should also include diverse unseen
task environment. Similarly, evaluation has progressed from             designs, realistic specifications and faults, and contamination
syntax checking toward FPV, coverage, and mutation testing,             controls to enable meaningful comparison across methods.
with recent benchmarks increasingly combining these metrics.               From individual assertions to assertion sets. Existing
   However, direct comparison across reported results remains           evaluations primarily assess individual properties, whereas
difficult because benchmarks differ in design source, scale,            practical verification depends on whether the complete asser-
input information, property granularity, formal environment,            tion set adequately captures design intent. Generating many
and evaluation criteria. Training-time evaluations introduce            simple and correct assertions may produce favorable aggre-
the additional concern of contamination or repository overlap,          gate results while missing complex behaviors or interactions.
particularly when both training and evaluation examples orig-           Future evaluation should therefore consider specification cov-
inate from public RTL repositories. Inference-time methods              erage, non-vacuity, redundancy, consistency, behavioral di-
face a related concern when specifications, RTL, or reference           versity, and fault-detection effectiveness at the assertion-set
assertions may have appeared in model pretraining data.                 level. Explicit traceability between specification requirements
Evaluation on held-out designs and, where possible, previously          and generated properties would further reveal missing or
unpublished or carefully contamination-controlled benchmarks            inadequately represented requirements.
is therefore important for establishing generalization.                    Generalization, scalability, and cost. Training-time ap-
   More fundamentally, existing benchmarks still provide lim-           proaches show the benefits of domain adaptation, while
ited measurement of assertion-set quality. Evaluating asser-            inference-time methods improve design-specific reasoning
tions independently does not determine whether the generated            through retrieval, structured representations, and tool feed-
set adequately covers the specification, contains redundant or          back. However, both remain sensitive to data quality and
contradictory properties, or omits critical requirements. Future        are largely evaluated on relatively small designs or localized
benchmarks should therefore preserve explicit relationships             properties. Scaling to complex SoCs requires reasoning across
among specifications, RTL, reference verification objectives,           hierarchical RTL and specifications while selectively retrieving
assertions, and realistic faults, enabling separate measurement         relevant information across modules and abstraction levels.
of syntactic validity, semantic fidelity, specification cover-          Moreover, multimodal processing, candidate search, agentic
age, non-vacuity, consistency, behavioral diversity, and fault-         workflows, and repeated formal-tool calls increase latency
detection capability. For iterative and agentic methods, eval-          and computational cost. Future evaluations should therefore
uation should additionally report inference cost, verification-         report inference and verification runtime, tool calls, refinement
tool runtime, number of refinement iterations or tool calls,            iterations, and human intervention, together with controlled



                                                                   11
ablations that isolate the contributions of individual tech-              The literature on LLM-assisted testbench generation sep-
niques.                                                                arates into three related but distinct tasks. The first is
   Toward complete verification property sets. Another                 stimulus generation: producing input vectors, transactions,
promising direction is joint generation of assumptions, asser-         or sequences that improve code or functional coverage.
tions, and cover properties. Assumptions characterize valid            The second is testbench construction: producing executable
environmental behavior, assertions specify required design             drivers, clocks, resets, monitors, and checkers. The third is
behavior, and cover properties establish reachability of impor-        verification-environment synthesis: generating reusable UVM
tant scenarios. Generating and validating them together can            or subsystem-level verification infrastructure. These tasks dif-
reduce spurious failures, expose overconstraint and vacuity,           fer in difficulty. Stimulus generation can be judged by coverage
and provide a more complete representation of verification             and simulator output, while full testbench generation also
intent than assertions alone.                                          requires correct timing, reset handling, protocol compliance,
   Overall, future research should shift from optimizing the           and a faithful oracle. This distinction explains why many
generation of individually valid assertions toward construct-          recent systems use the LLM as a planner or repair agent, while
ing specification-aligned and independently validated verifi-          deterministic code templates, DSLs, or simulators enforce the
cation property sets. LLMs are well suited for interpreting            final executable structure [76, 77, 78, 79].
requirements, connecting information across heterogeneous                 Figure 2 summarizes this taxonomy and the feedback sig-
artifacts, and proposing candidate properties, while determin-         nals that cut across the three task levels.
istic simulation and formal tools provide essential validation
and feedback. Combining these complementary capabilities—              B. Pre-LLM Automation: Templates, Grammars, and Con-
while maintaining traceability to the specification, control-          strained Random Testing
ling cost, and preserving independence from implementation
errors—is a promising path toward reducing manual assertion-              Automatic testbench generation predates modern LLMs.
development effort and enabling reliable, review-centered              Earlier tools demonstrate two lessons that remain important.
assertion-based verification.                                          First, constraining the output space greatly improves syntac-
                                                                       tic stability. Second, simulation throughput matters because
               IV. T ESTBENCH G ENERATION                              verification requires repeated execution. AVERT, for exam-
                                                                       ple, generates Verilog testbenches for grammatical-evolution
   This section surveys recent work on automatic testbench             hardware-design workflows by using DUT port information
and stimulus generation for hardware verification, with em-            and standard test-vector files; it supports combinational and
phasis on large language model (LLM) based methods. It                 sequential circuits and improves simulation efficiency by eval-
situates LLM approaches relative to pre-LLM template and               uating multiple DUTs in a single generated testbench [80].
grammar-based tools, then reviews prompt-only generation,              Such approaches do not solve oracle discovery or semantic
EDA-feedback loops, coverage-directed stimulus generation,             adequacy, but they show that structured generation can remove
self-validating testbench construction, UVM/subsystem-level            repetitive formatting work and reduce avoidable syntax errors.
generation, training-time alignment, and benchmark design.                Other pre-LLM work includes coverage-directed test gen-
The main conclusion is that current LLMs are most useful               eration, directed testing, and RTL fuzzing. Machine-learning-
when embedded in verification-aware workflows that constrain           assisted coverage-directed generation and directed hardware
generation with scenarios, templates, simulators, coverage             validation emphasizes the same optimization problem that
reports, and functional self-checks, rather than when used as          LLM systems now revisit: selecting tests that close cov-
unconstrained SystemVerilog authors.                                   erage efficiently while preserving bug-finding power [81,
                                                                       82]. RFUZZ, DirectFuzz, and FuzzWiz show that fuzzing-
A. Motivation and Scope                                                style feedback can drive RTL exploration using coverage or
   Simulation-based functional verification remains one of the         hardware-specific guidance, making them important non-LLM
most common pre-silicon verification techniques. A useful              baselines for stimulus-generation studies [83, 84, 85].
testbench is not merely code that compiles: it instantiates               Traditional constrained-random verification similarly pro-
the design under test (DUT), drives meaningful stimuli,                vides a useful baseline for LLM work. Randomization and
observes outputs, compares behavior against an oracle or               coverage feedback can explore large input spaces, especially in
reference model, and records structural or functional cov-             UVM-style environments, but engineers still have to write con-
erage. In industrial SystemVerilog flows, this often expands           straints, monitors, scoreboards, and coverage models. LLM-
into Universal Verification Methodology (UVM) components               based methods therefore should not be evaluated only against
such as sequence items, sequencers, drivers, monitors, agents,         direct prompting; they should also be compared with ran-
scoreboards, coverage collectors, and tests [73, 74]. Python-          dom, constrained-random, template-based, fuzzing-based, and
based harnesses such as cocotb are also relevant because many          coverage-directed baselines where appropriate. This is espe-
LLM workflows exploit Python’s stronger representation in              cially important because a generated testbench that improves
pretraining corpora to implement checkers, reference models,           line coverage may still miss a functional bug if the checker is
or orchestration code [75].                                            weak or absent.



                                                                  12
                                                                     LLM-assisted hardware
                                                                      testbench generation




                           Stimulus generation                       Testbench construction                       Environment synthesis
                           vectors, transactions,                    clocks, resets, drivers,                    UVM agents, sequences,
                           coverage-bin targets                        monitors, checkers                           protocol libraries




                           Coverage feedback                             Oracle feedback                               Tool feedback
                           line, branch, FSM,                         scoreboards, mutants,                         lint, compile, sim,
                             functional bins                              bug injection                                formal checks

                         Generation should be constrained by executable verification evidence, not only by natural-language plausibility.


               Fig. 2. Taxonomy of LLM-assisted testbench generation tasks and the main verification signals used to constrain them.



C. Prompted LLM Generation with EDA Feedback                                        for uncovered branches [22]. The system’s Coverage Ex-
   The earliest LLM-based testbench studies generally prompt                        plainer and DUT Explainer modules illustrate a practical
a commercial model with RTL and a natural-language specifi-                         prompt-engineering pattern: raw Verilator output is not ideal
cation, compile or simulate the result, and feed tool output                        LLM context, so an intermediate explanation layer translates
back into subsequent prompts. Bhandari et al. study this                            simulator artifacts into natural-language goals. The method
pattern for finite-state-machine testbench generation and bug                       performs best when the design remains within the model’s
detection. Their workflow asks GPT-3.5 or GPT-4 to generate                         comprehension scope, and its degradation on larger FSMs
tests, uses commercial EDA feedback to identify uncovered                           reinforces the scalability concerns observed in FSM-focused
transitions or errors, and iteratively refines prompts until                        work.
coverage improves. The work is important because it treats                             Spec2Cov generalizes this agentic coverage-closure per-
simulator and coverage output as first-class prompt context,                        spective by driving test-stimulus generation directly from
not merely as an after-the-fact evaluation step [86].                               design specifications and iteratively coordinating compilation,
   The FSM study also exposes a recurring limitation: LLMs                          simulation, coverage-report parsing, and prompt refinement
struggle with long traces, many states, and multi-bit outputs.                      [88]. Its results show that agentic coverage closure can reach
The authors mitigate this by chunking traces, resetting after                       full coverage on simpler designs but remains significantly
groups of transitions, and decomposing multi-bit outputs into                       harder on complex designs, which is consistent with the
smaller subproblems. This suggests a broader design principle                       broader literature: coverage feedback is powerful, but it does
for testbench generation: scalable systems should avoid asking                      not eliminate the need for design understanding, good oracles,
the model to reason over an entire trace or full environment                        and scalable decomposition.
in one context window. Instead, they should decompose the                              Several newer systems frame coverage closure as part of a
task into local coverage gaps, individual protocol obligations,                     broader verification-agent loop. PRO-V-R1 combines an LLM
or smaller signal cones.                                                            with reinforcement learning and simulation feedback to im-
                                                                                    prove automatic RTL verification, while UCAgent proposes an
D. Coverage-Directed Stimulus Generation                                            end-to-end block-level verification agent that traverses states
   A second line of work uses the LLM primarily as a                                and goals toward coverage closure [89, 90]. These systems
coverage-directed stimulus generator. LLM4DV is an open-                            are not only testbench generators; they combine planning,
source framework that orchestrates LLMs for hardware test-                          test generation, execution, and refinement. They are therefore
stimuli generation across multiple DUTs. Rather than asking                         best viewed as adjacent evidence that testbench generation is
for a complete verification environment, it iteratively samples                     becoming an agentic workflow rather than a single prompt-
missed coverage bins, restarts or refines dialogue context, and                     completion task.
uses few-shot prompting to guide the generation of input stim-                         Figure 3 abstracts the recurring loop shared by these sys-
uli [87]. This narrower framing is valuable because coverage                        tems.
bins and simulator feedback provide an executable objective:
the model is rewarded for reaching untested behavior, not for                       E. Full Testbench Generation and Self-Correction
producing aesthetically plausible HDL.                                                AutoBench is a key transition from stimulus-only work to
   VerilogReader takes a related but more code-coverage-                            complete LLM-generated testbenches. It proposes a staged
oriented view. It integrates an LLM into a coverage-directed                        workflow that separates scenario specification, Verilog driver
generation loop where the model acts as a “Verilog reader”                          generation, and Python checker generation. This architecture
that interprets RTL and coverage reports, then proposes stimuli                     deliberately uses Python for checking because LLMs are



                                                                               13
                              Spec + RTL                  LLM planner                     Generator                    EDA execution
                           interfaces, resets,         scenarios, signals,             stimuli, drivers,                lint, compile,
                            protocol intent              coverage goals                    checkers                    simulate, prove




                                                      Human review                    Repair/alignment                   Evidence
                                                     oracle adequacy,                  prompt update,                  errors, traces,
                                                     signoff judgment               self-correction, DPO             coverage, mutants


                                                  Solid arrows: automated tool-feedback loop. Dashed arrows: human constraints and review.


   Fig. 3. Verification-aware feedback loop used by simulator-in-the-loop, self-correcting, coverage-directed, and agentic testbench-generation systems.



generally stronger at Python than HDL, while Verilog remains                          UVM2 demonstrates a more automated UVM workflow
necessary for driving and integrating with RTL simulation                          that generates UVM testbenches and refines stimuli with
[76]. AutoBench also introduces AutoEval, which evaluates                          coverage feedback on RTL designs up to roughly 1.6K lines of
generated testbenches at multiple levels: basic execution, func-                   code [93]. HAVEN pushes the structured-generation principle
tional behavior, and mutation-based adequacy. The mutation-                        further by preventing the LLM from writing raw UVM code
based step is particularly important because a testbench can                       directly. Instead, LLM agents extract an architectural plan,
compile and even pass the golden design while still failing to                     protocol-specific Jinja2 templates instantiate UVM compo-
reject incorrect RTL mutants.                                                      nents, and a protocol-aware sequence DSL generates bus-
   CorrectBench extends this direction by adding functional                        correct stimulus. On open-source IPs spanning Direct, Wish-
self-validation and self-correction. Its central insight is that                   bone, and AXI4-Lite interfaces, HAVEN reports complete
syntax-level debugging is insufficient: the generated checker                      compilation success and strong average code and functional
or driver may be functionally wrong even after it compiles.                        coverage [78]. This is one of the clearest examples that
CorrectBench uses scenario-based validation with imperfect                         reducing LLM freedom can improve verification trust.
RTL variants to infer whether a generated testbench can dis-                          UVMarvel extends the UVM story to subsystem-level ver-
tinguish correct and incorrect behavior, then feeds detected bug                   ification. It introduces an intermediate representation, a bus
information to an LLM-based corrector [77]. This shifts the                        protocol library, signal tracking, and a Verilog patching library
target from “does the testbench run?” to “does the testbench                       to translate heterogeneous specifications into protocol-correct
detect meaningful behavioral differences?”                                         UVM environments and refine stimuli [79]. Compared with
   ConfiBench further extends the AutoBench/CorrectBench                           module-level benchmarks, this is closer to industrial verifica-
family with confidence-based scenario masking and a multi-                         tion because subsystems involve protocol interactions, gener-
testbench ensemble. Instead of trusting a single generated                         ated interconnect, and multiple coordinated blocks. However,
testbench in all scenarios, it masks high-risk scenarios and                       it also shows that successful LLM-aided UVM generation
combines multiple generated testbenches to compensate for                          currently depends on substantial handcrafted infrastructure:
coverage loss. Reported results show a higher overall pass rate                    protocol libraries, IRs, templates, and tool-specific repair
than AutoBench and CorrectBench-style baselines, especially                        loops.
on sequential circuits [91]. The broader lesson is that ensemble                      Other UVM-oriented and end-to-end verification studies
and confidence mechanisms can be useful when individual                            support the same trend. Exploratory APB UVM case stud-
LLM outputs remain unstable.                                                       ies show that generative models can help scaffold protocol-
                                                                                   specific UVM components, but also that human review is
F. UVM and Subsystem-Level Generation                                              still needed for completeness and correctness [94]. Multi-agent
   Moving from module-level Verilog testbenches to UVM                             verification frameworks and security-verification agents extend
environments introduces a substantial jump in complexity.                          the idea beyond plain functional testbenches by combining
UVM code is class-heavy, convention-driven, and protocol-                          LLM-generated collateral with simulator execution, asser-
sensitive; a generated environment must coordinate transaction                     tion/security checks, or tool-guided debug loops [95, 96, 97].
definitions, sequences, drivers, monitors, scoreboards, con-                       These works are useful related literature even when their
figuration databases, coverage groups, and simulator-specific                      primary target is broader verification automation rather than
build rules. VerifLLMBench addresses this evaluation gap                           testbench generation alone.
by benchmarking LLM-generated UVM testbenches using
verified DUTs, generated UVM components, iterative syntax                          G. Training-Time Alignment and Execution-Aware Learning
repair, linting, compilation, simulation, and coverage analysis                       Prompting and agentic refinement improve inference-time
[92]. Its importance is methodological: UVM generation must                        behavior, but they do not directly teach the model which
be evaluated as an environment-construction problem, not                           testbench patterns produce high verification value. TB or
merely as a single-file code-generation task.                                      Not TB addresses this by fine-tuning models with Coverage-



                                                                              14
Driven Direct Preference Optimization (CD-DPO). It con-                checks are only gateway metrics. A stronger benchmark asks
structs PairaNet, a preference dataset of higher- and lower-           whether the testbench drives meaningful scenarios, reaches
quality testbenches labeled by simulation-derived coverage             structural and functional coverage targets, detects injected bugs
metrics, and trains models to prefer stimuli that improve              or RTL mutants, and avoids false passes. AutoBench and Cor-
coverage [98]. This is important because it turns coverage from        rectBench make this explicit through multi-stage evaluation
a prompt-time hint into a training signal.                             and mutant-based checks [76, 77]. CVDP broadens the bench-
   LLM4Cov similarly argues that online reinforcement learn-           mark landscape by including hardware design and verification
ing with simulators is often too slow and expensive, so it             tasks in both non-agentic and agentic forms, revealing that
builds an offline execution-aware agent-learning framework.            tool-using verification tasks remain difficult for current models
The framework uses execution-validated data curation, policy-          [101]. Benchmarking should also include fuzzing and directed-
aware synthesis, and worst-state-prioritized sampling to train         test baselines because classical CDG, RFUZZ, DirectFuzz, and
compact models for high-coverage testbench generation [99].            FuzzWiz attack the same coverage-closure objective with non-
These training-time approaches indicate a likely future di-            LLM search strategies [81, 83, 84, 85].
rection: instead of relying only on increasingly large gen-               The most useful metrics for this subfield include:
eral models, verification-specific generators may be trained             • Build success: parsing, elaboration, simulator compatibil-
on simulator-labeled examples, coverage traces, failed repair              ity, and lint cleanliness;
attempts, and tool-grounded preferences.                                 • Stimulus effectiveness: line, branch, toggle, FSM-state,
   Structured Testbench Generation (STG) takes an even                     FSM-transition, and user-defined functional coverage;
stronger stance against unconstrained LLM generation. Rather             • Oracle strength: ability to reject faulty designs, RTL
than iteratively prompting an LLM to synthesize testbenches,               mutants, or injected bugs;
STG exploits hardware structure to generate deterministic test-          • Repair convergence: number of tool-feedback iterations,
benches, reduce false passes, and curate verification-oriented             token cost, and simulator runs required;
data for model training [100]. STG’s results support a recur-            • Scalability: performance on sequential circuits, larger
ring conclusion across this section: testbench generation bene-            FSMs, bus protocols, and subsystem-level designs;
fits from deterministic structure wherever possible, with LLMs           • Portability: whether generated collateral works across
used for planning, classification, repair, or data augmentation            open-source and commercial simulators.
rather than unrestricted final-code authorship.                           Figure 4 shows why later-stage metrics provide stronger
                                                                       evidence than syntax or compilation alone. Tables IV–VI
H. Agentic Verification Workflows
                                                                       summarize representative work across these dimensions.
   The newest papers increasingly describe testbench genera-
tion as one component of an agentic verification loop. In these        J. Challenges and Future Directions
systems, the LLM may decompose a verification goal, generate              LLM-based testbench generation has evolved from generat-
or repair testbench code, execute tools, interpret compiler            ing directed tests for small RTL modules toward self-checking
or simulator output, update coverage goals, and repeat. This           testbenches, coverage-guided refinement, UVM environments,
matches the “prompt, verify, repeat” pattern articulated in            and subsystem-level verification. In parallel, workflows have
recent verification-cycle work [97]. The important distinction         progressed from one-shot generation toward iterative and
from earlier self-debugging is that the agent owns more of the         agentic approaches that incorporate simulation and coverage
verification workflow: it can select which scenario to target,         feedback. Despite this progress, unconstrained SystemVer-
which tool output to inspect, and when to revise code or               ilog and UVM generation remains unreliable for complex
stimuli.                                                               sequential and protocol-intensive designs. The strongest ap-
   This agentic framing has two consequences for a survey.             proaches therefore combine LLM reasoning with determinis-
First, related work should include papers whose output is not          tic structures such as templates, intermediate representations
only a testbench file but a verification process that includes         (IRs), domain-specific languages (DSLs), protocol libraries,
testbench generation. PRO-V-R1, UCAgent, MAVF, and SV-                 and verification-tool feedback.
LLM are examples because they use generated programs,                     A central challenge is oracle quality. Effective stimuli
tests, or verification collateral inside larger automatic RTL          provide limited value without trustworthy mechanisms for de-
verification pipelines [89, 90, 95, 96]. Second, evaluation            termining correctness. High coverage or successful execution
needs to include cost and convergence, not only final coverage:        against golden RTL does not necessarily imply strong bug-
the number of compile/simulation attempts, failed repairs,             detection capability. Mutation testing, imperfect RTL variants,
prompts, and tool calls becomes part of the method’s prac-             and controlled bug injection therefore provide important com-
ticality.                                                              plementary evaluation [76, 77, 100]. Future work should place
                                                                       greater emphasis on generating and validating scoreboards,
I. Benchmarks and Evaluation Metrics                                   reference models, assertions, and other checking mechanisms.
   A serious testbench-generation benchmark must evaluate                 Sequential and temporal reasoning remains difficult for
several layers of correctness. At minimum, the generated arti-         resets, handshakes, long-latency operations, pipelines, FSMs,
fact should compile, elaborate, and simulate. However, these           and subsystem protocols. Existing approaches mitigate this



                                                                  15
                                       1. Build                     2. Simulation                        3. Coverage                            4. Oracle                         5. Readiness
                                 parse, elaborate, lint           expected scenarios                 branches, FSMs, bins                  mutants, bugs, checks                portability, review


                                         Evidence strength increases from left to right; later stages are harder to satisfy but more meaningful for signoff.


Fig. 4. Evaluation ladder for generated testbenches. Compilation is necessary, but coverage, oracle strength, mutation resistance, and portability are stronger
indicators of verification value.

                                                                TABLE IV
         R EPRESENTATIVE RELATED WORK ON AUTOMATIC AND LLM- ASSISTED HARDWARE TESTBENCH GENERATION : CLASSICAL BASELINES AND
                                                    STIMULUS - GENERATION METHODS .

Work                   Primary target                           Generation style                             Feedback / evaluation                      Main contribution                            Key limitation

AVERT [80]             Verilog testbench construction for       Grammar/template-based generation from       Simulation throughput on benchmark         Shows that structured non-LLM generation     Requires externally supplied vectors and
                       evolutionary hardware                    ports and test vectors                       circuits                                   can reduce manual testbench setup and        does not infer semantic oracles
                                                                                                                                                        improve simulation efficiency
Bhandari et al. [86]   FSM testbench generation and bug         Prompted GPT-3.5/GPT-4 with iterative        Transition coverage and bug-detection      Demonstrates compiler/simulator feedback     Scalability limited by trace length, state
                       detection                                EDA feedback                                 traces                                     as a practical prompt-refinement signal      count, and context management
RFUZZ [83]             RTL fuzzing and coverage exploration     Coverage-guided fuzzing for RTL              Coverage feedback and bug-finding          Establishes fuzzing as a strong non-LLM      Does not generate human-readable
                                                                simulators                                   experiments                                coverage-directed baseline                   verification environments or semantic
                                                                                                                                                                                                     checkers
DirectFuzz [84]        Directed RTL test generation             Directed fuzzing with hardware-aware         Targeted coverage and bug exposure       Improves reachability of hard-to-trigger       Still needs external checking and target
                                                                guidance                                                                              RTL behaviors                                  selection
FuzzWiz [85]           RTL fuzzing with hardware-specific       Automated hardware fuzzing workflow          Coverage and crash/bug finding           Provides a recent fuzzing baseline for         Optimizes exploration more than reusable
                       feedback                                                                                                                       automated RTL stimulus generation              testbench construction
LLM4DV [87]            Hardware test-stimuli generation         Coverage-directed prompting and              Functional coverage across multiple DUTs Frames LLMs as stimulus generators             Less focused on complete reusable
                                                                missed-bin refinement                                                                 inside a DV loop                               testbench environments
VerilogReader [22]     Code-coverage-directed stimulus          LLM reads RTL plus coverage                  Verilator-style coverage and             Introduces coverage and DUT explainers         Degrades when designs exceed model
                       generation                               explanations                                 random-testing comparison                to translate tool output into LLM-readable     comprehension scope
                                                                                                                                                      goals
Spec2Cov [88]          Specification-driven coverage closure    Agentic prompt refinement with simulator     Compilation, simulation, and code        Automates iterative stimulus generation        Full coverage remains difficult for
                                                                interaction                                  coverage over varied designs             from specifications                            complex designs




                                                             TABLE V
       R EPRESENTATIVE RELATED WORK ON AUTOMATIC AND LLM- ASSISTED HARDWARE TESTBENCH GENERATION : FULL TESTBENCH , UVM, AND
                                                     SUBSYSTEM - LEVEL METHODS .

Work                   Primary target                           Generation style                             Feedback / evaluation                      Main contribution                            Key limitation

AutoBench [76]         Full Verilog/Python hybrid testbench     Scenario, driver, and checker                Eval0–Eval2 metrics with mutant RTLs       Establishes a systematic LLM                 Syntax-focused repair still leaves
                       generation                               decomposition                                                                           testbench-generation and evaluation          functional checker errors
                                                                                                                                                        framework
CorrectBench [77]      Functionally self-correcting testbench   Generator, validator, and corrector agents   Scenario validation and Eval2 pass ratio   Adds functional self-validation and          Still relies on imperfect generated variants
                       generation                                                                                                                       self-correction without golden testbenches   and benchmark-scale tasks
ConfiBench [91]        Robust testbench generation under        Scenario masking and multi-testbench         Pass rate on AutoBench-style tasks         Uses confidence and ensembles to reduce      Added complexity and cost; still
                       uncertainty                              ensemble                                                                                risky generated behavior                     task-benchmark centered
VerifLLMBench [92]     UVM testbench benchmark                  LLM-generated UVM components with            Build success, lint, simulation, and       Provides an open methodology for             Demonstration designs are relatively
                                                                iterative repair                             coverage                                   evaluating LLM-generated UVM                 simple compared with industrial
                                                                                                                                                        environments                                 subsystems
UVM2 [93]              UVM testbench and stimulus generation    Automated UVM framework with                 Code and functional coverage on larger     Moves LLM verification from simple           Requires substantial tool orchestration and
                                                                coverage-guided refinement                   RTL designs                                benches toward reusable UVM workflows        domain-specific setup
HAVEN [78]             UVM testbench and sequence synthesis     LLM planning plus protocol templates and     Compilation, code coverage, and            Avoids raw UVM generation by using           Protocol-specific engineering must be built
                                                                sequence DSL                                 functional coverage                        templates and protocol-aware DSLs            and maintained
UVMarvel [79]          Subsystem-level UVM generation           IR, protocol library, signal tracking, and   Subsystem code coverage and automated      Extends LLM-aided UVM generation to          Public evidence remains recent and
                                                                patching                                     runtime                                    subsystem-level protocols                    protocol-library dependent




challenge by decomposing behavior into scenarios, transac-                                                              ity but are generally too small and public to establish industrial
tions, DSL operations, or targeted coverage gaps [22, 78, 86].                                                          readiness and may introduce contamination concerns. CVDP
Extending such structured reasoning to longer traces and                                                                and UVM-oriented benchmarks improve realism [92, 101],
interacting protocols is important for scaling beyond small                                                             but broader evaluation is needed across hidden designs, large
designs.                                                                                                                subsystems, mixed-language repositories, multiple simulators,
   Industrial-scale UVM generation introduces additional                                                                and standardized bug suites. Richer datasets aligning specifica-
challenges because useful environments must correctly con-                                                              tions, RTL, testbenches, execution traces, coverage, and bugs
nect components, obey protocol timing, implement meaningful                                                             would further support both evaluation and verification-aware
scoreboards and coverage models, and integrate with simulator                                                           training.
workflows. HAVEN, UVM2 , UVMarvel, and VerifLLMBench                                                                       Finally, execution-driven refinement can be costly. Re-
demonstrate progress, but also indicate that UVM genera-                                                                peated LLM and simulator interactions increase inference cost,
tion benefits substantially from templates, IRs, and reusable                                                           simulator usage, and verification time. Promising directions
protocol libraries [78, 79, 92, 93]. This suggests a hybrid                                                             include learning from execution traces, deterministic structural
approach in which LLMs perform high-level planning and rea-                                                             generation, targeted repair, and agentic controllers that obtain
soning while deterministic mechanisms generate structurally                                                             more useful feedback from fewer tool runs [89, 90, 98,
constrained verification components.                                                                                    99, 100]. Evaluation should therefore report simulator runs,
   Scalability and evaluation also remain open problems.                                                                refinement iterations, inference cost, and human intervention
HDLBits- and VerilogEval-derived tasks provide reproducibil-                                                            in addition to functional results.



                                                                                                                  16
                                                             TABLE VI
       R EPRESENTATIVE RELATED WORK ON AUTOMATIC AND LLM- ASSISTED HARDWARE TESTBENCH GENERATION : TRAINING - TIME AND AGENTIC
                                                             METHODS .

Work                Primary target                           Generation style                            Feedback / evaluation                       Main contribution                            Key limitation

TB or Not TB [98]   Coverage-optimized stimulus generation   CD-DPO fine-tuning from                     CVDP CID12 coverage metrics                Uses simulator-derived coverage as a          Depends on curated paired data and
                                                             coverage-labeled preferences                                                           training-time preference signal               simulator-labeled examples
LLM4Cov [99]        High-coverage agentic testbench          Offline execution-aware agent learning      Coverage pass rate under agentic           Learns from execution-validated               Benchmark and training protocol are
                    generation                                                                           evaluation                                 trajectories without online RL cost           recent; industrial generality remains open
PRO-V-R1 [89]       Automatic RTL verification agent         LLM plus reinforcement learning and         Program/test generation and verification   Treats verification as an executable          Broader RTL-verification scope makes
                                                             simulation feedback                         outcomes                                   feedback loop rather than static generation   direct TB-only comparison difficult
UCAgent [90]        End-to-end block-level functional        Agentic state/goal exploration with tool    Coverage closure and verification progress Shows how test generation can be              Very recent preprint; benchmark generality
                    verification                             feedback                                                                               embedded in a full verification agent         remains evolving
MAVF [95]           Module-level verification automation     Multi-agent generative AI workflow          Verification artifact generation and tool  Demonstrates division of labor among          Industry-style framework with limited
                                                                                                         execution                                  agents for module-level verification          public reproducibility details
SV-LLM [96]         SoC security verification                Agentic LLM workflow for security           Security-verification outcomes             Extends LLM-generated verification            Security focus differs from general
                                                             checks and generated collateral                                                        artifacts to security-oriented SoC flows      functional testbench generation
STG [100]           Deterministic testbench generation and   Structure-driven deterministic generation   Runtime, compile success, coverage, and    Shows deterministic structure can             Less flexible when verification intent is
                    data curation                                                                        false-pass reduction                       outperform iterative LLM testbench            not recoverable from structure alone
                                                                                                                                                    synthesis in speed and reliability




   Overall, existing work suggests that progress in LLM-based                                                      property rather than the RTL implementation [26, 105, 106].
testbench generation depends less on unconstrained code-                                                           Manual execution of this loop remains a major verification
generation capability or model scale than on how effectively                                                       bottleneck [102], increasingly aggravated by design scale and
the LLM is integrated with the verification process. The field                                                     integration complexity [104].
is consequently shifting from prompt-based testbench genera-                                                          RTL concurrency and hierarchy make this process partic-
tion toward verification-aware automation, in which simulator                                                      ularly challenging. A defect may propagate across multiple
outcomes serve as validation signals, refinement feedback, or                                                      modules and clock cycles before becoming observable, making
training preferences, while deterministic structures constrain                                                     the reported failure structurally and temporally distant from its
generation. Future progress will likely depend on stronger                                                         source [102, 103]. Repair must further relate the suspected
oracle generation, improved temporal and protocol reason-                                                          logic to the specification and timing behavior, remove the
ing, richer specification–RTL–testbench datasets, simulator-                                                       failure, and preserve unaffected functionality. Errors in lo-
portable and contamination-resistant evaluation, and scalable                                                      calization or diagnosis can therefore propagate to invalid or
workflows that combine LLM planning with deterministic                                                             incomplete repairs and additional debugging iterations [104].
verification infrastructure.                                                                                          LLMs can support this workflow by jointly processing
                                                                                                                   RTL, specifications, diagnostics, simulation traces, and formal
             V. D EBUGGING AND D ESIGN R EPAIR
                                                                                                                   counterexamples to assist localization, causal diagnosis, and
   Sections III and IV examined how LLMs can assist pre-                                                           repair [26, 103, 107]. Hardware-specific methods strengthen
silicon verification by generating assertions, stimuli, test-                                                      these capabilities through RAG for external design or repair
benches, and other verification artifacts to expose incorrect                                                      knowledge [108], RTL-specific fine-tuning [103, 109], explicit
RTL behavior. Once a failure is detected, however, compiler                                                        dependency representations [107], and multi-agent coordina-
diagnostics, simulation mismatches, assertion violations, or                                                       tion of localization and repair [110, 111]. These techniques
formal counterexamples must be translated into an actionable                                                       provide complementary mechanisms for implementing the
diagnosis and a validated correction. This motivates debugging                                                     failure-to-repair workflow.
and design repair, which closes the verification loop by                                                              In this section, we survey 25 papers on LLM-assisted hard-
identifying the fault, determining its cause, correcting the RTL,                                                  ware debugging, encompassing bug detection and localization,
and re-verifying the design.                                                                                       RCA, RTL and assertion repair, and integrated debugging
   As illustrated in Fig. 5, RTL debugging is an iterative                                                         workflows. Section V-A classifies the works by their primary
failure-to-repair process. Bug localization narrows an ob-                                                         debugging methodology, while Section V-B compares their
served failure to suspicious RTL modules, blocks, expressions,                                                     coverage of the debugging pipeline. Section V-C examines
signals, or assignments using the RTL and failure evidence                                                         debugging embedded within RTL generation workflows. Sec-
such as waveforms, assertion reports, or formal counterexam-                                                       tion V-D concludes with open challenges and future directions.
ples [26, 102, 103]. Root cause analysis (RCA) determines                                                          General-purpose software-repair methods without hardware
how the localized logic produces the observed deviation,                                                           evaluation are excluded.
while RTL repair generates a corrective modification for
re-verification [104]. If the failure persists or new violations                                                   A. LLM-Based Debugging Methodologies Taxonomy
emerge, the relevant stages are repeated. These stages should                                                         LLM-assisted debugging methods span multiple stages of
not be conflated: accurate localization does not establish                                                         the debugging pipeline but differ in how they acquire and use
the root cause, a plausible diagnosis does not guarantee a                                                         information to guide localization, diagnosis, and repair. To
correct repair, and a patch that passes the available checks                                                       characterize these methodological differences, we group the
may not preserve behavior outside those checks. Source-only                                                        reviewed works into four categories according to their princi-
localization further identifies suspicious RTL without an ob-                                                      pal mechanism: (1) prompting and tool-feedback-based debug-
served failure, whereas assertion repair corrects the verification                                                 ging; (2) retrieval-augmented debugging; (3) model adaptation;



                                                                                                              17
                                                                          Re-run verification to validate fix


       Step 1: Verification              Step 2: Failure Observation               Step 3: Bug Localization        Step 4: Root Cause Analysis        Step 5: RTL Fix
  Verification detects RTL errors        Verification detects incorrect           The bug scope is narrowed         The localized RTL logic is
   and validates fixes through              RTL behavior through                    by tracking signals and          analyzed to identify the    The RTL implementation is
    simulation, assertions, or             simulation mismatches,                dependencies backward from         fundamental cause of the       modified to correct the
        formal verification.                assertion violations, or             the failure to suspicious RTL               failure.              identified root cause.
                                          formal counterexamples.                      modules or logic.

                  Original failure persists, refine bug localization                         Root cause not found, expand scope


           Fig. 5. Conventional RTL debugging process illustrating iterative bug localization, root cause analysis, RTL fixing, and re-verification.



and (4) structured and agentic reasoning. These categories                                         rates of 93% and 78%, respectively. UVLLM [114] further
capture complementary sources of knowledge and control,                                            combines UVM checking with mismatch-driven data-flow slic-
enabling comparison of their capabilities, requirements, and                                       ing and test-score-based rollback. Time-aware slicing narrows
limitations beyond the pipeline stages they address. The cat-                                      the failure context presented to the LLM, while executable
egories are not mutually exclusive or indicative of capability.                                    UVM checks guide candidate selection. Across 331 error
Many frameworks combine multiple mechanisms; each work                                             instances from 27 RTLLM-derived modules, it reports syntax
is categorized by its principal contribution, with additional                                      and functional fix rates of 86.99% and 71.92%, respectively.
mechanisms identified in Tables VII and VIII.                                                         These methods demonstrate that prompting and verification
   1) Category 1: Prompting and Tool-Feedback-Based De-                                            feedback can support both source-level detection and iterative
bugging: This category uses prompting to guide LLMs in                                             RTL repair without model adaptation. Their effectiveness,
identifying defects or generating candidate repairs. Some                                          however, depends strongly on the information exposed by the
methods regenerate RTL and analyze differences from the                                            prompt and verification tools. Ambiguous diagnostics or weak
original code to locate potential defects [105]. Others incor-                                     functional feedback may not reveal the underlying cause, caus-
porate compiler or simulation feedback to iteratively refine                                       ing repeated generation to converge slowly or fail when the
repairs [110]. These approaches primarily rely on knowledge                                        required hardware knowledge is unavailable. This limitation
encoded in the LLM and information provided in the prompt,                                         motivates retrieval-based methods that explicitly augment the
without external retrieval or model parameter updates.                                             LLM with external debugging knowledge.
   Prompting methods can inject task-specific knowledge with-                                         2) Category 2: Retrieval-Augmented Debugging: Retrieval-
out modifying model parameters. Ahmad et al. [112] in-                                             augmented methods supplement the LLM with external infor-
vestigate repair of human-introduced hardware security bugs                                        mation, such as specifications, expert repair examples, docu-
using CWE-conditioned prompts and model/prompt sampling.                                           mentation, or design context, at inference time. This provides
Across 15 bugs, every case has at least one successful repair                                      task-specific knowledge without modifying model parameters
candidate, while GPT-4 produces 3,862 correct repairs in 7,500                                     and can improve both diagnosis and repair when the required
attempts. For selected weaknesses, CWEAT is used for bug de-                                       information is not reliably encoded in the LLM.
tection and post-repair checking. Self-HWDebug [113] instead                                          Qayyum et al. [115] use RAG to retrieve specification
derives reusable repair instructions from vulnerable/secure                                        context for HDL bug identification and repair. Their method
RTL pairs. Its two-shot configuration repairs all 25 test snip-                                    combines specification retrieval with expression decomposi-
pets spanning five CWE categories. Both approaches encode                                          tion and repairs all 25 nonconstant mutations across three
vulnerability knowledge through prompts rather than external                                       OpenTitan IPs, but none of the five constant mutations. The
retrieval or model adaptation. Beyond repair, prompting can                                        failed constants are absent from the specifications, illustrating
support bug detection and localization. FLAG [105] prompts                                         that retrieval effectiveness depends on the completeness of the
an LLM to regenerate RTL and uses differences from the                                             underlying knowledge source.
original code, token confidence, and distance from comments                                           Rather than retrieving specifications, RTLFixer [108] re-
as features for defect localization. Because it does not require                                   trieves validated expert solutions associated with compiler-
a failing testbench, it can screen incomplete or non-compiling                                     error patterns and combines them with ReAct-style prompt-
designs. Its line-level method detects 38 of 120 OpenTitan                                         ing and compiler feedback. The framework reports a 98.5%
bugs, demonstrating how prompted RTL regeneration can                                              compilation-error repair rate, with ablations showing comple-
provide diagnostic features for source-level screening.                                            mentary contributions from retrieval, iterative feedback, and
   Tool-feedback-based methods close the loop by using com-                                        diagnostic quality. GROVE [116] further makes the retrieval
piler or simulation results to evaluate generated repairs and                                      corpus adaptive by organizing previously resolved cases into
guide subsequent revisions. MEIC [110] employs debugging                                           an evolving knowledge tree with applicability conditions. Can-
and scoring agents, together with candidate history, rollback,                                     didate knowledge is validated on its originating cases, while
and self-planning, to manage iterative repair. On 178 RTLLM-                                       budget-aware retrieval selects relevant entries for new fail-
derived error instances, it reports syntax and functional fix                                      ures. On a module-disjoint SVA-Eval split, GROVE improves



                                                                                              18
Llama-3.3 pass@1 from 72.7% to 84.7% and achieves 86.9%                   versus joint localization and correction.
pass@5. These results demonstrate the potential of reusable                  Adaptation can further target repair generation or constrain
repair knowledge, although validation on an originating case              its scope. AssertSolver [109] combines pretraining, supervised
does not guarantee transfer to other designs.                             fine-tuning, and direct preference optimization over correct
   Retrieval can also select relevant design structure rather than        and incorrect responses for assertion-triggering RTL faults. It
textual repair knowledge. HDLxGraph [117] combines AST                    reports repair pass@1 and pass@5 of 88.54% and 90.00%,
hierarchy with data-flow traversal to retrieve repository-level           respectively, and generates explanations alongside candidate
RTL context. Its debugging evaluation covers five mor1kx                  corrections. ARSP [121] instead trains semantic partitioning
commits and uses ROUGE rather than functionally validated                 and fragment-repair models to restrict modification to a se-
repair, so the results demonstrate context retrieval rather               lected RTL region while retaining the specification and global
than repair correctness. ViTAD [118] instead augments signal              code as context. On injected faults in 33 designs, it achieves
dependencies with timing information and retrieves repair                 77.92% pass@1 and 83.88% pass@5. These methods address
strategies conditioned on inferred causes of timing violations.           complementary aspects of repair: response-level supervision
Across 54 injected timing cases, ViTAD improves the fix rate              improves candidate generation, whereas learned partitioning
from 54.38% to 71.05%, a gain of 16.67 percentage points.                 constrains where modifications are applied.
   Overall, retrieval-augmented debugging depends on the rel-                Overall, model adaptation enables hardware-specific local-
evance and completeness of external knowledge and the ability             ization and repair knowledge to be internalized rather than re-
of the LLM to apply it correctly.                                         peatedly retrieved or supplied through prompts. The reviewed
   3) Category 3: Debugging through Model Adaptation:                     methods show that adaptation can improve localization, guide
Model adaptation encodes hardware-specific debugging                      downstream repair, and specialize models for particular defect
knowledge in model parameters through continued pretraining,              classes, while synthetic data, repository histories, and prefer-
supervised fine-tuning, preference optimization, or specialized           ence signals provide different forms of supervision. However,
training objectives. These methods aim to improve localization            performance depends strongly on the quality and represen-
and repair, but their effectiveness depends on representative             tativeness of the training data, and metrics such as exact
training data. Public datasets pairing faulty RTL with fault              patch match or textual similarity do not necessarily establish
locations, diagnostics, and validated repairs remain limited.             functional correctness. Moreover, parameter adaptation alone
   HDLdebugger [103] addresses this data limitation by con-               does not resolve failures whose causes span large RTL hierar-
structing a synthetic debugging corpus through reverse engi-              chies, multiple clock cycles, or long verification traces. These
neering. Controlled mutations of correct RTL are paired with              limitations motivate the structured representations, explicit
compiler diagnostics and reference implementations to provide             search, and agent coordination examined in the next category.
repair supervision, while code and document retrieval supplies               4) Category 4: Structured and Agentic Debugging: Prompt-
additional context at inference time. The resulting framework             ing, retrieval, and model adaptation improve the knowledge
reports an 81.93% execution pass rate on its test split drawn             available to an LLM, but complex RTL failures may still re-
from 92,143 industrial HDL instances. LLM4SecHW [119]                     quire reasoning across multiple signals, modules, clock cycles,
instead mines open-source hardware version histories for de-              and candidate repairs. Structured and agentic methods address
fect/fix pairs and descriptions and applies lightweight adapter-          this challenge by explicitly organizing failure evidence, inter-
based fine-tuning. Its evaluation uses per-case ROUGE scores              mediate hypotheses, repair search, or tool interactions. This
and qualitative examples rather than an aggregate functionally            category therefore includes graph-based reasoning, structured
validated repair rate. These approaches illustrate two com-               search, and agent coordination, with classification determined
plementary sources of adaptation data: controlled synthetic               by the principal methodological contribution rather than the
defects and naturally occurring development histories.                    use of multiple agents alone.
   Model adaptation can also specialize LLMs for fault lo-                   FVDebug [107] structures formal counterexamples as a
calization. LiK [26] combines continual pretraining, super-               directed acyclic graph that captures signal dependencies across
vised localization training, and SimPO preference optimiza-               timesteps. A Graph Scanner uses batched LLM inference with
tion, achieving 93.38% localization pass@1 compared with                  paired for-and-against prompting to identify suspicious nodes,
77.9% for GPT-4-Turbo on the same benchmark. Supplying its                after which a reasoning agent develops causal hypotheses and
predicted locations to GPT-3.5 further improves downstream                generates patches. On 38 SVA-Eval-Human cases, FVDebug
repair from 40.39% to 58.92%, demonstrating the value of lo-              reports a Quality@Best score of 0.956 under an LLM judge
calization as an intermediate debugging step. VeriDebug [120]             and repair pass@1/pass@5 of 71.1%/86.8%. Its additional
instead integrates localization and repair within a shared model          CVA6 and proprietary industrial examples primarily demon-
using contrastive representations of fault locations and bug              strate RCA on larger designs and should not be interpreted
types. It reports 67.2% top-1 localization accuracy and 64.7%             as achieving the same repair rates. VeriPilot [122] instead
top-1 repair accuracy, where repair requires an exact match               aligns RTL variables with internal variables of a supplied
to the reference corrected line. Thus, LiK and VeriDebug                  golden model and traces control- and data-flow dependencies
represent different interfaces between learned localization and           to guide iterative repair. On adapted CVDP tasks, this approach
repair: explicit localization for a downstream repair model               improves GPT-4o repair success from 54.3% to 85.71%,



                                                                     19
demonstrating the value of explicit reference alignment while           knowledge-oriented mechanisms of the preceding categories
requiring an executable golden model.                                   by explicitly controlling how debugging evidence is repre-
   VeriTrace [123] introduces Agentic Temporal Exploration,             sented, analyzed, and searched. Dependency graphs can ex-
in which an Inspector agent iteratively selects internal signals        pose spatial and temporal fault propagation, structured search
and time windows for hypothesis-driven waveform analysis                can explore alternative repairs, and specialized agents or sym-
before a separate RTL Debugger performs targeted repair. The            bolic tools can decompose and constrain complex debugging
Inspector reasons over the specification, RTL, and waveform             tasks. These mechanisms are particularly useful when failures
evidence without direct access to the testbench, while can-             cannot be resolved from a single prompt or local code context,
didate repairs are re-simulated against the supplied golden             but their effectiveness remains bounded by the quality of
testbench and retained when they reduce mismatches. On                  the available verification evidence, reference models, and tool
VerilogEval-V2, VeriTrace achieves 100% with Claude Sonnet              feedback. In practice, the four categories are complementary
4.5, with notable gains on sequential FSM tasks. However,               rather than exclusive: hybrid frameworks increasingly combine
repair acceptance is determined by the supplied testbench, so           prompting, retrieval, model adaptation, structured reasoning,
passing establishes consistency with the exercised behaviors            and verification tools to address different information and
rather than independent conformance to the complete specifi-            control requirements throughout the debugging process.
cation; behaviors, corner cases, or temporal conditions omitted
by the testbench remain unverified.                                     B. LLM-Based Debugging Works Across Pipeline Stages
   Structured reasoning can also organize the search over                  The preceding taxonomy classifies LLM-based debugging
candidate repairs. R3A [111] separates multi-agent fault lo-            methods by their primary mechanisms. We next compare the
calization from patch exploration, using ranked candidate               reviewed works by their coverage of the debugging pipeline
locations to initialize a stochastic tree-of-thoughts search. A         in Fig. 5, focusing on bug localization, RCA, repair, and
heuristic balances exploration and exploitation under a fixed           integrated re-verification. Tables VII and VIII summarize these
time budget, enabling R3A to solve 29 of 32 RTL-Repair                  capabilities and the corresponding evaluation evidence.
cases, with mean pass@1 and pass@5 of 75.0% and 86.7%,                     Bug localization. Localization methods differ in both the
respectively. Clover [124] extends this approach by dispatch-           granularity of their outputs and how directly those outputs
ing repair tasks between LLM-based editing and SMT-based                identify faulty RTL. LiK [26] predicts fault locations that guide
repair within a dialogue-state tree. It solves 31 of 32 RTL-            downstream correction, while VeriDebug [120] jointly learns
Repair cases and achieves 87.5% mean pass@1, compared                   localization and repair. In contrast, ARSP [121] identifies
with 29 of 32 cases and 75.0% for R3A. These results suggest            a candidate repair region, and HDLxGraph [117] retrieves
the potential of combining generative search with constrained           repository context relevant to diagnosis. These outputs serve
symbolic repair, although the cross-study comparison does not           related purposes but provide different levels of localization
isolate the contribution of SMT reasoning and both methods              evidence. Notably, LiK shows that its predicted locations
depend on the adequacy of the waveform checks.                          improve downstream GPT-3.5 repair from 40.39% to 58.92%,
   Agentic workflows can also target debugging outputs other            demonstrating practical value beyond localization accuracy. By
than RTL repair. MARVEL [125] coordinates a security-policy             comparison, candidate-region extraction or context retrieval
supervisor with tool-specialized executors to identify SoC              alone does not establish line-level localization accuracy or
vulnerabilities rather than generate patches. Its 51 reported           improved repair. Localization should therefore be evaluated
findings comprise 19 vulnerabilities, 14 warnings, and 18               by both the specificity of the identified region and its demon-
hallucinated findings, highlighting both the coverage and               strated contribution to subsequent debugging.
false-positive challenges of agentic security analysis. Assert-            Root cause analysis. RCA goes beyond localization by
Fix [106] targets assertion repair by retrieving relevant RTL           explaining how the suspected RTL produces the observed
and distinguishing timing from logic errors before correction.          failure. Its evaluation should therefore distinguish a causally
It achieves formal assertion-fix rates of 73.7% − −83.8%                supported diagnosis from reasoning generated only as an
across four designs, but assumes golden RTL and therefore               intermediate step toward repair. FVDebug [107] separately
addresses a different repair target from faulty-RTL correction.         evaluates generated causal hypotheses and checked repair
   LintLLM [126] illustrates structured diagnostic reasoning            outcomes, reporting a Quality@Best score of 0.956 for RCA
without an explicitly established multi-agent architecture. Its         in addition to its repair results. AssertSolver [109] also gen-
Logic-Tree prompt decomposes diagnosis into ordered steps,              erates explanations with proposed corrections, but explanation
while a Defect Tracker tentatively fixes detected defects and           generation alone does not establish causal accuracy. Similarly,
reruns LLM-based detection to identify primary defects. Be-             a successful patch validates the correction only under the
cause this feedback comes from repeated LLM detection rather            supplied checks and does not necessarily validate every step
than independent EDA-tool validation, the resulting diagnoses           of its accompanying explanation. Evaluation scale must also
still require external confirmation. Across 90 designs spanning         be associated with the pipeline stage: FVDebug’s larger CVA6
11 defect categories and three difficulty levels, it reports an         and industrial demonstrations establish RCA capability at that
83.33% correct rate and a 12.22% false-positive rate.                   scale, but not equivalent automated repair performance. RCA
   Overall, structured and agentic methods complement the               evaluation should therefore report whether causal hypotheses



                                                                   20
                                                             TABLE VII
    S UMMARY OF LLM- BASED HARDWARE DEBUGGING WORKS (PART I). C AT.: C1 = PROMPTING / MODEL GENERATION / TOOL FEEDBACK , C2 =
RETRIEVAL , C3 = PARAMETER ADAPTATION , C4 = STRUCTURED / AGENTIC REASONING . BL = BUG LOCALIZATION , RCA = ROOT CAUSE ANALYSIS , F IX
                        = RTL REPAIR , E2E = INTEGRATED FAILURE - TO - PATCH WORKFLOW WITH TOOL RECHECKING .

Paper                 Cat.    BL RCA Fix          E2E Core Technique                          Bug Types     Key Result                        Benchmark
AutoVeriFix [127]     C1       –  –  ✓             ✓ Python-assisted two-stage                Syntax,       GPT-4: 77.2% pass@1               VerilogEval-Human/Machine,
                                                      generation, iterative simulation        functional    (Human), 83.7% pass@1             RTLLM v2.0, generation
                                                      feedback                                              (Machine), 83.5% pass@5           outcomes
                                                                                                            (RTLLM v2.0)
VerilogCoder [128]    C1,4    (✓) (✓)       ✓      ✓  Graph-based planning, debug             Syntax,       GPT-4 Turbo: 94.2% workflow       VerilogEval-Human v2, 156
                                                      agent, AST-based waveform               functional    pass rate with supplied           tasks, supplied golden
                                                      tracing                                               testbench feedback                testbenches
On hardware            C1      –      –     ✓     (✓) CWE-conditioned prompts,                Hardware      15/15 cases have a successful     15 security bugs, separate
security bug code                                     model/prompt sampling, selected         security      candidate, GPT-4: 3,862/7,500     functional-repair comparison
fixes [112]                                           CWEAT integration                                     correct attempts
MEIC [110]            C1,4    (✓) (✓)       ✓      ✓ Prompt-configured debug/scorer           Syntax,       93% syntax and 78%                178 RTLLM-derived error
                                                      agents, candidate history and           functional    functional fix rates              instances
                                                      rollback
UVLLM [114]           C1,4     ✓    (✓)     ✓      ✓ UVM checking, mismatch-driven            Syntax,     86.99% syntax and 71.92%        331 error instances across 27
                                                      DFG slicing, test-score rollback        functional  functional fix rates            RTLLM-derived modules
RTLFixer [108]       C1,2,4    –    (✓)     ✓      ✓ ReAct and expert-guidance                Compilation 98.5% compilation-error repair, VerilogEval-derived syntax
                                                      retrieval with compiler feedback        errors      not a functional repair rate    errors, additional RTLLM
                                                                                                                                          evaluation
From Bugs to           C2      ✓    (✓)     ✓      –    Specification retrieval, expression   Functional 25/25 nonconstant mutations      AON Timer, UART, and EDN,
Fixes [115]                                             decomposition and patching            mutations   patched, 0/5 constant mutations 30 injected mutations
                                                        closure
GROVE [116]           C2,4    (✓) (✓)       ✓      –    Tool-validated knowledge tree,        Assertion-    Llama-3.3: 84.7% pass@1,      SVA-Eval: 732 training/183
                                                        applicability conditions,             triggering    86.9% pass@5, Jasper-checked test cases, module-disjoint
                                                        snapshot-and-zoom retrieval           RTL faults                                  split
HDLdebugger [103] C2,3        (✓) (✓)       ✓      –    Reverse-engineered error pairs,       Compiler-     81.93% execution pass rate on 92,143 industrial HDL
                                                        code/document retrieval,              oriented      the reported test split       instances, 8:2 train/test split
                                                        supervised fine-tuning                HDL errors
HDLxGraph [117]        C2     (✓)     –    (✓)     –    AST hierarchy and DFG signal          Repository    Debugging assessed by          Five mor1kx commits,
                                                        traversal for repository retrieval    defects       ROUGE overlap, no functional HDLSearch evaluates retrieval
                                                                                                            repair pass rate               separately
ViTAD [118]           C2,4     ✓     ✓      ✓      –    Timing dependency graph,              Setup/hold,   GPT-4o: 71.05% fix rate versus 54 reported injected timing
                                                        violation-path analysis,              CDC           54.38% without ViTAD           cases, Vivado-based evaluation
                                                        cause-conditioned repair
                                                        knowledge
LLM4SecHW [119]        C3      ✓    (✓)     ✓      –    Repository-history defect/fix pairs   Hardware      Per-case ROUGE and                Open-source hardware version
                                                        and descriptions, adapter-based       defects,      qualitative examples, no          histories, including OpenTitan
                                                        fine-tuning                           security      aggregate validated repair rate
✓: explicitly implemented target/output, (✓): supporting operation or restricted demonstration, –: not separately established. E2E denotes automated tool rechecking within
the declared workflow, not full-design verification, signoff, or independent proof of all unaffected behavior. An E2E dash does not mean that a paper omitted experimental
validation. Category labels identify mechanisms, not publication order. Metrics retain each paper’s evaluation definition and are not directly comparable across rows.



are independently assessed and distinguish such evidence from                            exercised by the workflow.
intermediate reasoning used to guide repair.
   Repair and closed-loop debugging. Repair methods differ
in both the artifact being corrected and the criterion used to
accept a candidate. For RTL repair, RTLFixer [108] evaluates                                Overall, the reviewed methods provide increasingly broad
compilation success, whereas VeriDebug [120] measures exact                              coverage of the debugging pipeline, ranging from source-level
agreement with a reference corrected line. These criteria differ                         localization to integrated localization, diagnosis, repair, and re-
from behavioral validation through simulation, assertions, or                            verification. However, pipeline coverage alone does not deter-
formal checking, as used by other repair frameworks [107,                                mine debugging capability or correctness. Localization outputs
114]. AssertFix [106] further targets incorrect assertions while                         vary in granularity, RCA requires evidence that generated
assuming golden RTL, and therefore addresses a different re-                             explanations reflect the observed failure, and repair results
pair problem from correcting a faulty implementation. Closed-                            depend strongly on the acceptance criterion and behavioral
loop integration adds another dimension by automatically                                 oracle. Accordingly, comparisons should distinguish which
rechecking candidate repairs and using the resulting feedback                            pipeline stages are automated from what evidence validates
for further correction. For example, UVLLM [114] combines                                the output of each stage. This distinction is particularly impor-
candidate generation with UVM-based rechecking to support                                tant for closed-loop workflows, where repeated tool feedback
iterative repair. Such re-verification strengthens the debugging                         can improve repair success without guaranteeing correctness
loop but establishes correctness only with respect to the checks                         beyond the supplied verification checks.



                                                                                    21
                                                           TABLE VIII
 S UMMARY OF LLM- BASED HARDWARE DEBUGGING WORKS (PART II). T HE COLUMN DEFINITIONS FOLLOW TABLE VII. SO DENOTES SOURCE - ONLY
SCREENING AS AN INPUT CONDITION , NOT AN ADDITIONAL CATEGORY. A SUPERSCRIPT A IDENTIFIES ASSERTION REPAIR RATHER THAN RTL REPAIR .

Paper                 Cat.    BL RCA Fix      E2E Core Technique                       Bug Types Key Result                         Benchmark
LiK [26]              C3      ✓   –   –        –  Continual pretraining,               Functional 93.38% localization pass@1,       102 RTLLM-derived cases
                                                  line-localization supervision,       RTL faults downstream GPT-3.5 repair:        spanning five injected bug
                                                  SimPO                                             40.39% to 58.92%                types
VeriDebug [120]        C3     ✓       –    ✓   –  Contrastive localization/type        Functional 67.2% location Acc@1, 64.7% Synthetic functional defects,
                                                  embeddings and guided repair with RTL faults exact-match repair Acc@1             compilable RTL, held-out
                                                  shared parameters                                                                 evaluation split
AssertSolver [109]     C3     ✓     (✓)    ✓   –  Pretraining, supervised fine-tuning, Assertion- 88.54% pass@1, 90.00%             SVA-Eval: 877 generated and
                                                  and DPO on correct/incorrect         triggering   pass@5, assertion-failure       38 human-curated cases
                                                  repair responses                     RTL faults resolution
Self-                  C1      –      –    ✓   –  Instructions synthesized from        Hardware     Two-shot setting: 25/25 test    Five CWE categories, five test
HWDebug [113]                                     vulnerable/secure pairs, no weight security       snippets mitigated              snippets per category
                                                  update
FVDebug [107]         C2,4    ✓      ✓     ✓ (✓) Signal-event causal graph,            Formal-      Quality@Best 0.956 (LLM         38 SVA-Eval-Human cases,
                                                  balanced scanning, hypothesis        verification judge), repair pass@1/pass@5: additional CVA6 and
                                                  exploration, patch generation        failures     71.1%/86.8%                     industrial RCA cases
R3A [111]              C4     ✓     (✓)    ✓   ✓ AST-segmented localization            Structural, 29/32 cases solved, mean         RTL-Repair, acceptance
                                                  agents, stochastic tree-of-thoughts functional    pass@1 75.0%, pass@5 86.7% against reference waveforms
                                                  patch search
LintLLM [126]          C4,    ✓     (✓)   (✓)  –  Logic-Tree prompting, tentative      Syntax, lin- o1-mini: 83.33% correct rate, 90 designs, 11 defect
                       SO                         fixes and LLM redetection to         t/semantic   12.22% reported false-positive categories, three difficulty
                                                  isolate primary defects              defects      rate                            levels
FLAG [105]             C1,    ✓       –    –   –  Static targeting, regeneration       Security,    Line-level detection: 51/201,   OpenTitan (120), HackAtDAC
                       SO                         differences and token probabilities, functional   token top-five: 47/201          (42), CirFix (30), CWE
                                                  line classifier                                                                   examples (9)
ARSP [121]            C3,4   (✓)      –    ✓   –  Trained semantic partitioning and Functional 77.92% pass@1, 83.88%                Injected faults in 33
                                                  fragment repair, controlled          RTL faults pass@5, testbench-checked         RTLLM/GenBen designs,
                                                  recombination                                                                     mean 219 RTL lines
VeriPilot [122]        C4     ✓     (✓)    ✓   ✓ Golden-model variable alignment, Functional GPT-4o on adapted CVDP:                Strider and adapted CVDP
                                                  CDFG tracing, reference-guided       RTL faults 54.3% to 85.71% repair success tasks, executable golden
                                                  iterative repair                                                                  models supplied
Clover [124]           C4    (✓) (✓)       ✓   ✓ Agentic dispatch to LLM/SMT           Structural, 31/32 RTL-Repair cases           RTL-Repair, additional
                                                  repair, dialogue-state tree search, functional    solved, mean pass@1 87.5%       random-logic synthetic
                                                  RTL toolbox                                                                       evaluation
MARVEL [125]          C2,4    ✓     (✓)    –   –  Security-policy supervisor and       SoC security 51 reports: 19 vulnerabilities, OpenTitan-based
                                                  tool-specialized detection                        14 warnings, 18 hallucinations Hack@DATE SoC
                                                  executors
AssertFix [106]       C2,4   (✓)     ✓    ✓A (✓)A Related-RTL retrieval, timing/logic Incorrect     Formal assertion fix rates:     I2C, ECG, Pairing, SHA3,
                                                  classification, assertion-specific   SVA          73.7%–83.8% across four         golden RTL assumed
                                                  correction                           timing/logic designs
BL includes candidate-region extraction. It does not imply measured line-level accuracy. RCA marked as supporting denotes explanatory reasoning or defect classification
without an independently evaluated causal-diagnosis task. LintLLM’s edits support internal diagnosis. FVDebug’s large-design demonstrations concern RCA and should not
inherit its small-benchmark repair rates. Assertion repair and source-only detection are included for their debugging role but remain distinct from RTL functional repair.



C. Debugging as a Component of LLM-Based RTL Genera-                                    coding and debugging agents. Its debugging agent uses simu-
tion Framework                                                                          lation mismatches and AST-based waveform tracing to revise
                                                                                        generated RTL against a supplied testbench. With GPT-4
   The preceding subsections consider debugging primarily as
                                                                                        Turbo, the complete workflow achieves a 94.2% pass rate
the diagnosis and repair of faulty RTL. Debugging also serves
                                                                                        on 156 VerilogEval-Human v2. VeriTrace [123] extends this
as an integral component of LLM-based RTL generation,
                                                                                        paradigm by allowing a dedicated Inspector agent to iteratively
where generated candidates are iteratively corrected before
                                                                                        select internal signals and temporal windows for hypothesis-
being accepted. In this setting, correction occurs at two levels:
                                                                                        driven waveform analysis before targeted RTL repair.
compilation errors can be addressed using compiler diagnos-
tics, whereas functional errors require behavioral feedback                                AutoVeriFix [127] instead constructs its own behavioral
from a testbench or reference model.                                                    reference from the natural-language specification. Its first stage
   RTLFixer [108] illustrates compilation-oriented correction                           generates a Python reference model and tests, which are
of LLM-generated Verilog. It combines compiler feedback                                 refined using Python coverage feedback. The second stage
with retrieved expert repair guidance to iteratively revise                             generates Verilog and iteratively corrects compilation errors
erroneous candidates. This improves RTL executability, but                              and behavioral mismatches against this reference. With GPT-4,
compilation alone does not establish functional correctness.                            AutoVeriFix achieves 77.2% pass@1 on VerilogEval-Human,
   Functional correction requires stronger behavioral feedback.                         83.7% pass@1 on VerilogEval-Machine, and 83.5% pass@5
VerilogCoder [128] integrates graph-based task planning with                            on RTLLM v2.0. These results characterize the complete



                                                                                   22
generation-and-correction workflow rather than repair of a                agentic methods reviewed above show that debugging perfor-
fixed set of pre-existing RTL defects.                                    mance depends on decisions about which fault hypotheses to
   Another recent work, VeriRefine [129], also integrates ver-            explore, which signal or temporal dependencies to trace, which
ification and debugging directly into RTL generation through              context to retrieve, and when to invoke simulation, formal, or
a structured intermediate representation. Unlike VerilogCoder,            symbolic tools. Future agents could adapt these policies from
which uses a supplied benchmark testbench to guide debug-                 previous validated outcomes, progressively learning which rea-
ging, VeriRefine generates its verification environment from the          soning and tool-use strategies are effective for different failure
specification, keeping both generation and correction grounded            classes. Such adaptation must be separated experimentally
in the same source of intended behavior.                                  from gains due simply to additional retrieval, repair attempts,
   Overall, debugging turns RTL generation into an iterative              or computation. Runtime, token consumption, tool calls, and
process guided by verification feedback. Its reliability depends          solver budgets should therefore accompany repair accuracy
on both the coverage of the checks and the correctness of                 when evaluating self-evolving strategies.
the expected behavior. Verification artifacts generated from                 A third challenge is maintaining independent and trust-
the specification may share interpretation errors with the                worthy verification. The preceding studies show that com-
RTL. Evaluation should therefore report feedback access and               piler success, exact patch matching, simulation tests, assertion
iteration budgets and use benchmark simulation or properties              checking, and formal verification provide different levels of
withheld during repair to assess functional correctness.                  evidence, and no single metric establishes correctness in all
                                                                          settings. Moreover, when the same testbench or reference
D. Future Research Direction: Self-Evolving Hardware De-                  model guides repair and determines acceptance, the system
bugging Systems                                                           can overfit to the available verification environment. A self-
   The reviewed methods demonstrate a progression from                    evolving agent could amplify this problem by retaining such
prompt-based correction toward retrieval, model adaptation,               locally successful but incomplete repairs as future knowledge.
structured reasoning, agentic search, and verification-guided             New experience should therefore be admitted to persistent
repair. However, most systems learn little from completed                 memory only after independent validation, preferably using
debugging tasks and restart subsequent tasks with the same                held-out tests, properties, or formal checks that are not avail-
knowledge and strategies. A promising direction is self-                  able during repair. The agent should also distinguish faults in
evolving hardware debugging, in which agents accumulate                   the RTL from errors in assertions, reference models, specifi-
validated experience across designs and revisions and use it to           cations, or environmental assumptions rather than modifying
improve bug localization, diagnosis, repair, and verification.            the artifact that defines its own acceptance criterion.
   A self-evolving system should retain more than successful                 Finally, scalability remains an open challenge because re-
patches. Each debugging episode should associate the failure              alistic failures can span modules, clock cycles, and long
and repair with its fault location, causal evidence, relevant             execution traces. Current approaches demonstrate the benefits
signal dependencies, specification assumptions, applicability             of dependency graphs, slicing, retrieval, fine-tuning, and agent
conditions, and validation results. GROVE [116] provides an               decomposition, but evidence for large-scale end-to-end repair
initial example of organizing validated repair knowledge for              remains limited. Future systems will require compact repre-
reuse, while MEIC, R3A, and Clover [110, 111, 124] maintain               sentations of spatial and temporal failure evidence, hierarchical
candidate states and feedback within individual debugging                 localization and reasoning, selective retrieval, and adaptive tool
sessions. Extending such mechanisms across tasks could allow              invocation to control context and computational cost. Human
previous experience to guide retrieval, fault localization, repair        oversight will also remain important for ambiguous specifica-
selection, and tool invocation rather than merely provide                 tions, high-impact repairs, and final acceptance criteria.
another repair example.                                                      Overall, existing work establishes that LLMs can support
   A central challenge is reliable transfer across designs and            individual stages of hardware debugging and that combin-
revisions. A repair that succeeds on one design may be-                   ing prompting, retrieval, adaptation, structured reasoning, and
come invalid when interfaces, timing behavior, implementation             verification feedback can substantially strengthen closed-loop
structure, or specifications change. Persistent knowledge must            repair. The next step is to move from isolated debugging
therefore retain the conditions under which it was learned                episodes toward systems that learn from validated experience
and be revalidated before reuse rather than treating every                while preserving independent verification. Achieving this goal
successful repair as universally applicable. Evaluation should            requires reliable cross-design transfer, persistent knowledge
correspondingly use sequences of unseen designs or design                 with explicit applicability conditions, adaptive yet resource-
revisions and compare systems with and without accumulated                efficient debugging policies, scalable reasoning over temporal
experience under equivalent resource budgets. Such experi-                and hierarchical RTL behavior, and evaluation against veri-
ments should measure whether experience reduces localiza-                 fication evidence withheld from the learning and repair pro-
tion effort and improves independently validated repair rates             cess. Addressing these challenges is essential for transforming
without increasing regressions or false positives.                        LLM-based debugging from task-specific repair automation
   A second challenge is evolving debugging strategies rather             into dependable hardware debugging systems that improve
than only accumulating repair knowledge. The structured and               across designs without accumulating incorrect or obsolete



                                                                     23
knowledge.                                                                research directions toward reliable, scalable, and increasingly
                                                                          autonomous LLM-assisted formal verification for production-
          VI. LLM S FOR F ORMAL V ERIFICATION                             grade hardware.
    Simulation-based validation remains indispensable in hard-
ware verification because of its flexibility and scalability;             A. LLM-Assisted Proof Generation and Model Checking
however, it explores only a finite set of input sequences and                Beyond formal property generation, recent research has
execution scenarios and therefore cannot guarantee the absence            increasingly employed LLMs to assist the proof process it-
of bugs. Formal verification (FV), in contrast, provides exhaus-          self. These approaches use LLMs to construct intermediate
tive mathematical guarantees by proving that a design satisfies           proof artifacts, guide proof search, optimize model-checking
specified properties over all states and inputs admitted by a for-        algorithms, and coordinate verification workflows, thereby
mal model [35, 130]. Despite these guarantees, practical adop-            moving LLMs deeper into the formal verification pipeline
tion of FV is hindered by two fundamental bottlenecks. The                while retaining conventional formal engines as the source of
first is the specification bottleneck, which requires engineers           correctness guarantees.
to translate design intent into precise properties, environmental            One important direction is incremental and hierarchical
assumptions, invariants, and verification models. The sec-                proof generation, which decomposes large verification prob-
ond is the computational bottleneck arising from state-space              lems into smaller proof obligations. Qayyum et al. [131] pro-
explosion and the complexity of SAT/SMT-based reasoning                   posed an LLM-assisted framework that partitions a design into
for large designs. Industrial FV further requires engineers               smaller modules and generates module-level invariants and
to select appropriate proof engines and strategies, analyze               interface properties. Each generated property is independently
counterexamples, diagnose root causes, and iteratively refine             validated using SAT/SMT-based formal verification before
verification models. These challenges are compounded by                   being composed into higher-level proofs. This decomposition
incomplete or ambiguous specifications, bounded-verification              reduces the reasoning burden on the LLM and improves proof
limitations, vacuous properties, multi-property interactions,             scalability by avoiding direct reasoning over the complete
and solver scalability, making formal verification both labor             flattened design.
intensive and computationally demanding.                                     A closely related direction is LLM-assisted invariant syn-
    Recent advances in large language models (LLMs) have                  thesis, where the LLM generates candidate inductive invariants
created opportunities to address both the specification and               that are subsequently validated by formal engines. Hassan et
computational bottlenecks of formal verification. By process-             al. [132] combined GPT-4-generated invariants with formal
ing natural-language specifications, RTL, assertions, source              verification and mutation testing. Mutation testing provides
code, and verification traces, LLMs can generate candidate                a stronger assessment of invariant quality than syntactic va-
properties, invariants, verification models, proof strategies, and        lidity or proof success alone because it evaluates whether
solver optimization heuristics, while also assisting with coun-           generated invariants can distinguish the original design from
terexample analysis and verification workflow orchestration.              intentionally modified implementations, thereby exposing se-
Rather than relying directly on LLM outputs, recent research              mantically weak or vacuous properties. CIll [133] further intro-
increasingly adopts a neuro-symbolic paradigm in which                    duced a counterexample-to-induction (CTI)-guided approach
LLMs perform semantic reasoning and heuristic generation,                 in which candidate invariants are checked using bounded
while model checkers, SAT/SMT solvers, and other formal                   model checking and inductiveness checking, and counterex-
engines validate the generated artifacts and provide corrective           amples are returned to the LLM to guide iterative refinement.
feedback. This separation combines the flexibility of gener-              Integration with IC3 and k-induction enabled verification of
ative models with the soundness of formal verification and                multiple RISC-V processor designs. Together, these studies
has enabled applications spanning property generation, model              demonstrate the potential of closed-loop LLM–formal-engine
checking, logic equivalence checking, solver optimization, and            interactions for synthesizing nontrivial proof artifacts, while
end-to-end verification workflow automation.                              also showing that effectiveness depends strongly on the quality
    SystemVerilog assertion generation using LLMs has been                of counterexample interpretation and the efficiency of formal
treated in Section III. This section reviews the emerging                 feedback.
landscape of LLM-driven formal verification and examines                     A complementary direction applies LLMs not to individual
how LLMs are being integrated with formal engines to address              proof artifacts but to the model-checking algorithms them-
proof construction, equivalence checking, solver optimization,            selves. IC3-Evolve [134], for example, uses an LLM offline
and workflow automation. It also analyzes the limitations that            to evolve IC3/PDR heuristics through auditable code modi-
currently constrain reliability and scalability, including hallu-         fications. Candidate changes are accepted only when SAFE
cination, limited context and reasoning depth, data scarcity,             executions produce independently verifiable proof certificates
benchmark overfitting and contamination, verification latency,            and UNSAFE executions generate replayable counterexam-
and solver scalability. By organizing existing approaches ac-             ples. The resulting optimized model checker operates with-
cording to their verification objectives, LLM roles, formal               out an LLM at runtime, separating heuristic discovery from
back ends, and evaluation methodologies, this review iden-                trusted proof reasoning. This approach illustrates an important
tifies common design patterns and limitations and highlights              distinction between LLM-assisted verification, where the LLM



                                                                     24
participates in an individual verification instance, and LLM-               A more prevalent approach treats formal equivalence check-
driven verification optimization, where the LLM searches for             ing as a correctness oracle within LLM-driven RTL generation.
improvements to the underlying formal engine.                            FormalEval [136] uses sequential equivalence checking to
   Recent work has further expanded the role of LLMs from                compare generated RTL with a reference implementation and
assisting individual verification tasks to orchestrating complete        returns either a proof result or a counterexample. The formal
formal verification workflows. Saarthi [20], for example, or-            result therefore provides an objective functional-correctness
ganizes specification analysis, verification planning, assertion         signal for evaluating and refining LLM-generated RTL. For-
generation, property proving, counterexample analysis, and               malRTL [137] extends this paradigm by coupling LLM-based
coverage closure into an integrated multi-agent workflow                 planning and RTL synthesis with formal equivalence checking
coupled with commercial formal verification tools. Although              and software reference models as executable specifications.
its reported end-to-end automation rate remains approximately            Generated RTL is accepted or revised according to formal
40%, the framework demonstrates a transition toward agentic              feedback, transforming RTL generation from a one-shot syn-
formal verification in which multiple reasoning and verifica-            thesis task into an iterative generate–verify–repair process.
tion activities are coordinated within a unified workflow.                  These studies reveal a common pattern between LLM-
   Collectively, these studies indicate an evolution from LLM-           assisted model checking and LEC: in both settings, LLMs
based generation of individual proof artifacts toward closed-            primarily perform semantic reasoning and generate or refine
loop proof refinement, model-checker optimization, and multi-            verification artifacts, while formal engines provide objective
agent verification orchestration. The current state of practice          feedback that guides subsequent iterations. The key distinction
remains fundamentally neuro-symbolic: LLMs are effective                 lies in the verification objective: model-checking approaches
as generators, heuristic search mechanisms, decomposition                use LLMs to construct invariants, decompose proof obliga-
agents, and counterexample interpreters, whereas SAT/SMT                 tions, interpret counterexamples, or guide proof search for
solvers, bounded model checkers, IC3/PDR, and commercial                 properties of a design, whereas LEC approaches use LLMs to
formal engines remain responsible for establishing correctness.          reason about correspondences between implementations and
This division of responsibility is essential because linguistic          to synthesize or repair RTL under equivalence constraints. On
plausibility cannot establish the soundness or completeness              the other hand, this common generate–formally validate–refine
required for formal hardware verification.                               paradigm suggests that techniques developed for LLM-guided
                                                                         proof refinement, counterexample interpretation, and hierar-
B. LLM-Assisted Logic Equivalence Checking                               chical decomposition could potentially be transferred to LEC,
   Compared with LLM-assisted property generation and                    particularly for correspondence identification and equivalence-
model checking, the use of LLMs for logic equivalence                    problem partitioning. It is also interesting to extend the role
checking (LEC) remains relatively immature. LEC deter-                   of LLMs toward broader proof assistance, including identifi-
mines whether two hardware implementations exhibit equiv-                cation of correspondence points, abstraction and partitioning
alent behavior and is routinely used for RTL-to-RTL com-                 strategies, and interpretation of equivalence counterexamples.
parison, RTL-to-gate verification, and validation of synthe-
sis and engineering-change-order (ECO) transformations. Be-              C. LLM-Driven SAT/SMT Solver Optimization
cause conventional LEC provides a proof or counterexample                   Modern formal verification engines, including IC3/PDR-
rather than a statistical confidence estimate, current LLM-              based model checkers, rely heavily on SAT/SMT solvers as
based approaches generally use LLMs in conjunction with                  their core reasoning engines. Their performance is therefore
formal equivalence engines rather than as replacements for               strongly influenced by solver heuristics and implementation
them. Two complementary directions have emerged: learning-               choices, including branching, clause learning and deletion, pre-
based prediction of equivalence relationships and the use of             processing and inprocessing, restarts, and theory propagation.
formal equivalence checking as a correctness oracle for LLM-             This dependency has motivated research on using LLMs to
based RTL generation and refinement.                                     automate the discovery and optimization of solver heuristics
   DeepRTL2 [135] explores RTL equivalence as a represen-                and implementations.
tation learning problem. It constructs equivalent and non-                  Non-LLM solver specialization provides an important base-
equivalent RTL pairs through a feedback-driven process in                line for this research direction. Su et al. developed Gip-
which GPT-4o generates functionality-preserving RTL trans-               SAT [138], a lightweight CDCL solver specialized for IC3
formations and a conventional Yosys LEC flow determines                  workloads by exploiting structural properties of IC3-generated
whether the resulting designs remain equivalent. The generated           SAT queries. GipSAT reduces unnecessary decisions, re-
pairs are subsequently used to train representations for equiv-          places the conventional VSIDS binary heap with a bucket-
alence classification. DeepRTL2 reports 68.1% accuracy and               based data structure, and optimizes temporary-clause manage-
72.3% F1 score, outperforming the evaluated general-purpose              ment, achieving an average 3.61× speedup over a MiniSat-
embedding baselines. However, the learned predictor serves               based IC3 implementation on HWMCC’20 and HWMCC’24
primarily as a filtering mechanism rather than a replacement             benchmarks. The subsequent rIC3 framework further com-
for formal equivalence checking because statistical classifica-          bines SAT-level optimizations with IC3 improvements such
tion cannot provide exhaustive correctness guarantees.                   as dynamic generalization and internal-signal-based reason-



                                                                    25
ing [139]. These results establish that substantial gains can            can generate useful verification artifacts, but whether they
arise from tailoring both solver and model-checking strate-              can do so reliably, efficiently, scalably, and with sufficient
gies to verification-specific workloads and motivate LLMs as             generalization across designs and verification tasks.
mechanisms for automating such optimization.                                First, correctness remains fundamentally different from
   Based on these observations, AutoSAT [140] and                        linguistic plausibility. LLM-generated assertions, invariants,
SolSearch [141] use LLMs to generate and iteratively                     proof strategies, or solver modifications may appear reasonable
refine CDCL solver heuristics or source-code modifications               while being incomplete, over-constrained, vacuous, or seman-
based on benchmark performance. AutoModSAT [142] further                 tically incorrect. Formal validation is therefore essential, but
combines prompt optimization with evolutionary search to                 validation alone does not guarantee useful verification if the
explore modular SAT solver configurations. These approaches              generated properties do not adequately capture design intent.
formulate solver optimization as an empirical search loop                Future systems should jointly address property quality and
in which the LLM proposes a modification, the resulting                  proof validity through mechanisms that detect vacuity, measure
solver is compiled and evaluated on representative instances,            specification coverage, identify missing behaviors, and use
and performance feedback guides subsequent iterations. The               counterexamples to refine both the generated artifact and its
results demonstrate that LLMs can explore a broad design                 underlying specification.
space of solver heuristics and implementation strategies that               Second, scalability remains a central limitation at both
would otherwise require substantial manual expertise.                    the LLM and formal-engine levels. Large industrial designs
   LLM-based optimization has also been explored for SMT                 exceed practical context limits and contain long-range depen-
reasoning. LLMs can generate and refine SMT constraints or               dencies that are difficult for LLMs to preserve across iterative
solver API code from high-level objectives, translating infor-           interactions. At the same time, formal engines face state-
mal requirements into SMT-LIB formulations or APIs such as               space explosion and expensive SAT/SMT reasoning. Hierar-
Z3 Optimize [143]. For solver optimization, however, syntactic           chical verification, modular context management, retrieval of
validity is insufficient: generated formulations and solver mod-         design-relevant information, and multi-agent decomposition
ifications must preserve semantic correctness while improving            are promising approaches, but their effectiveness must be
solving efficiency and avoiding unsupported or computation-              evaluated against the cost of maintaining consistency across
ally inefficient theory combinations. Consequently, the central          agents and abstraction boundaries. In particular, future systems
challenge is to jointly evaluate correctness and performance             should avoid merely shifting the scalability problem from the
rather than optimize either criterion in isolation.                      formal engine to an increasingly large LLM context.
   Overall, existing work have demonstrated the search ca-                  Third, the interaction between LLMs and formal tools
pability of LLMs for SAT/SMT solver optimization, partic-                introduces a significant latency bottleneck. Proof attempts and
ularly when candidate generation is combined with auto-                  SAT/SMT evaluations may require minutes or hours, making
mated compilation, correctness checking, and empirical perfor-           naive generate–verify–repair loops prohibitively expensive.
mance evaluation. However, current results remain vulnerable             Research should therefore investigate adaptive feedback mech-
to benchmark overfitting, unstable optimization trajectories,            anisms that determine when formal evaluation is necessary,
compilation and execution failures, and loss of generality               surrogate models that prioritize promising candidates, and
when optimizations are tuned to particular workloads. Future             compact representations of counterexamples, proof failures,
progress therefore requires evaluation across diverse formal-            and solver traces that preserve the information most useful
verification workloads and explicit measurement of both solver           for subsequent LLM reasoning.
performance and generalization, rather than reporting improve-              Fourth, generalization and evaluation remain insufficiently
ments on a single benchmark distribution.                                understood. Many existing studies rely on small benchmark
                                                                         suites or task-specific datasets, making it difficult to determine
D. Cross-Cutting Challenges and Future Directions                        whether reported gains reflect genuine reasoning improve-
   Across these research directions, the state of the art is mov-        ments or overfitting to particular designs, coding styles, solver
ing beyond one-shot LLM generation toward closed-loop, tool-             configurations, or benchmark distributions. Future evaluations
grounded, and increasingly agentic formal verification. Current          should include larger and more diverse hardware designs,
systems can generate assertions and invariants, decompose                unseen architectures, cross-benchmark testing, multiple LLMs,
verification problems, interpret counterexamples, guide proof            and controlled ablation studies that isolate the contributions of
search, optimize solver implementations, and coordinate multi-           prompting, retrieval, agentic decomposition, formal feedback,
stage verification workflows. The most reliable architectures            and solver optimization. Evaluation should also report not only
share a common pattern: the LLM performs semantic rea-                   correctness and proof success, but verification time, tool-call
soning, candidate generation, heuristic exploration, or work-            cost, coverage, robustness across repeated runs, and the degree
flow coordination, while deterministic formal tools provide              of human intervention required.
correctness feedback and ultimately establish the validity of               Finally, a major opportunity lies in developing hardware-
the generated artifacts. Nevertheless, current systems remain            aware agentic systems that jointly reason about specifications,
far from autonomous production-grade verification, and the               RTL structure, formal properties, proof strategies, and the
primary research challenge is no longer simply whether LLMs              underlying SAT/SMT infrastructure. Rather than treating these



                                                                    26
tasks as independent stages, future frameworks could establish           retrieval, multimodal reasoning, and hierarchical hardware
feedback loops in which failures at one level inform deci-               knowledge are promising mechanisms for maintaining these
sions at another—for example, counterexamples could guide                relationships across large designs.
property refinement, failed proofs could trigger abstraction                Scalability represents a second high-level challenge. Current
or decomposition, and solver-performance feedback could                  results are strongest on relatively localized tasks, whereas
influence model-checking strategies. Such systems should                 industrial verification requires reasoning across large RTL
remain grounded by independently checkable proof artifacts               hierarchies, long temporal behaviors, heterogeneous verifica-
and formal correctness oracles, enabling increasing levels               tion artifacts, and expensive EDA-tool interactions. Simply
of automation without sacrificing the soundness guarantees               increasing context length, agent count, or refinement iterations
that distinguish formal verification from statistical software           is unlikely to provide a sustainable solution because it can shift
generation.                                                              rather than eliminate the underlying complexity. Future sys-
                                                                         tems should instead selectively retrieve and compress relevant
       VII. C ONCLUSION AND F UTURE D IRECTIONS                          information, reason hierarchically across abstraction levels,
   This survey examined the emerging role of LLMs across                 decompose verification objectives, and invoke expensive tools
hardware functional verification, including assertion genera-            only when their expected information value justifies the cost.
tion, stimulus and testbench generation, bug localization and            The longer-term goal is an adaptive neuro-symbolic workflow
design repair, formal verification, equivalence checking, solver         in which LLM reasoning determines what should be ana-
optimization, and agentic verification workflows. Across these           lyzed next while deterministic verification engines determine
areas, a common pattern emerges: LLMs are most effective                 whether the resulting claims are valid.
not as replacements for established verification algorithms, but            A third challenge is establishing generalization and trust-
as semantic reasoning and orchestration layers that connect              worthy evaluation. Reported results remain difficult to com-
specifications, design artifacts, verification evidence, and de-         pare because studies differ substantially in benchmark scale,
terministic EDA tools. Prompting, retrieval, model adaptation,           available design information, verification environments, model
structured representations, and agentic reasoning improve dif-           configurations, iteration budgets, and acceptance criteria. Pub-
ferent aspects of this interaction, while simulators, formal en-         lic hardware repositories further introduce potential over-
gines, coverage tools, and SAT/SMT solvers remain essential              lap between model training data and evaluation artifacts.
for evaluating generated artifacts and establishing correctness.         Future benchmarks should therefore emphasize unseen and
   A second cross-cutting finding is the growing importance              contamination-controlled designs, diverse architectures and
of closed-loop, verification-grounded workflows. Compilation             abstraction levels, realistic specifications and defects, and
diagnostics, simulation traces, coverage reports, counterex-             evaluation across multiple models and verification tools. Eval-
amples, proof outcomes, and solver statistics increasingly               uation should measure not only final artifact success but
serve not only as acceptance signals but also as feedback                also verification effectiveness, robustness across repeated runs,
for localization, refinement, search, and tool selection. This           computational and tool cost, and required human intervention.
feedback-driven paradigm appears across assertion and test-              For iterative and agentic systems, controlled ablations are par-
bench generation, RTL debugging and repair, model check-                 ticularly important for distinguishing genuine improvements
ing, equivalence checking, and solver optimization. However,             in reasoning from gains obtained through additional search,
successful interaction with a verification tool should not be            tool calls, or computation.
confused with complete verification: an artifact may satisfy                These considerations also change how autonomy should be
the available checks while still failing to capture behaviors or         viewed in hardware verification. The emerging trajectory is
requirements that those checks do not represent. The central             from one-shot artifact generation toward persistent agents that
challenge is therefore not merely generating executable or tool-         plan verification activities, interpret heterogeneous evidence,
accepted artifacts, but preserving alignment between design              coordinate tools, and reuse validated experience across de-
intent and the verification evidence used to justify correctness.        signs and revisions. Such systems could progressively improve
   This observation motivates a broader research direction               retrieval, decomposition, debugging, and verification strate-
toward specification-centered verification intelligence. Future          gies, but persistent knowledge must retain its applicability
systems should maintain explicit relationships among require-            conditions and validation evidence so that obsolete or design-
ments, RTL, assertions, stimuli, reference models, coverage              specific conclusions are not propagated. Human engineers will
objectives, counterexamples, and repair decisions rather than            remain essential for resolving ambiguous intent, reviewing
treating these artifacts independently. Such traceability would          high-impact decisions, defining verification objectives, and es-
enable an agent to determine whether a verification failure              tablishing signoff criteria. Accordingly, the objective should be
originates from the implementation, a generated verification             dependable human–AI collaboration rather than unrestricted
artifact, an incorrect environmental assumption, or an incom-            autonomous verification.
plete specification. It would also provide a stronger basis                 Overall, the reviewed literature shows that LLMs can sub-
for measuring verification completeness and for preventing               stantially reduce the semantic and orchestration burden of
implementation-specific behavior from silently redefining the            hardware verification when coupled with deterministic veri-
intended specification. Structured intermediate representations,         fication infrastructure. The field has progressed from isolated



                                                                    27
generation of assertions, tests, and repairs toward integrated                                 R EFERENCES
workflows that reason over specifications, verification artifacts,
failure evidence, and formal engines. The next major step is               [1] Apple, “Apple Introduces M2 Ultra.” https://www.apple.
to make these workflows specification-aligned, scalable, inde-                 com/newsroom/2023/06/apple-introduces-m2-ultra/,
pendently verifiable, and demonstrably generalizable. Progress                 June 2023. Accessed: Oct. 3, 2026.
along these dimensions could transform LLM-assisted verifica-              [2] NVIDIA,          “NVIDIA          Blackwell      Platform
tion from a collection of promising task-level demonstrations                  Arrives to Power a New Era of Com-
into a dependable verification methodology in which LLMs                       puting.”             https://nvidianews.nvidia.com/news/
provide flexible reasoning and automation while established                    nvidia-blackwell-platform-arrives-to-power-a-new-era-of-computin
EDA tools and engineering judgment preserve the correctness                    Mar. 2024. Accessed: Oct. 3, 2026.
guarantees required for hardware design.                                   [3] H. Witharana, Y. Lyu, S. Charles, and P. Mishra, “A
                                                                               survey on assertion-based hardware verification,” ACM
                     ACKNOWLEDGMENT
                                                                               Comput. Surv., vol. 54, Sept. 2022.
   This work is supported by the National Science Foundation               [4] B. Moyer, “Legacy process nodes going strong: The
under Grant No. 2434247. Any opinions, findings, and conclu-                   critical, and growing, significance of mature node chips
sions or recommendations expressed in this material are those                  and processes,” Semiconductor Engineering, July 2024.
of the author(s) and do not necessarily reflect the views of the           [5] H. Foster, “2024 Wilson Research Group IC/ASIC
funding agencies.                                                              Functional Verification Trend Report,” 2024.
                                                                           [6] J. Pan, G. Zhou, C. Chang, I. Jacobson, J. Hu, and
                                                                               Y. Chen, “A Survey of Research in Large Language
                                                                               Models for Electronic Design Automation,” ACM Trans.
                                                                               Des. Autom. Electron. Syst., vol. 30, no. 3, pp. 1–21,
                                                                               2025.
                                                                           [7] D. Yu, H. Foster, and T. Fitzpatrick, “A survey of ma-
                                                                               chine learning applications in functional verification,”
                                                                               in Proc. DVCon, 2024.
                                                                           [8] OpenAI, “Gpt-5.” https://openai.com/gpt-5/, 2025. Ac-
                                                                               cessed: 2025-10-13.
                                                                           [9] Anthropic,      “Claude.”      https://claude.com/product/
                                                                               overview, 2025. Accessed: 2025-10-13.
                                                                          [10] Google DeepMind, “Gemini.” https://gemini.google.
                                                                               com/, 2025. Accessed: 2025-10-13.
                                                                          [11] J. Pan, G. Zhou, C.-C. Chang, I. Jacobson, J. Hu, and
                                                                               Y. Chen, “A survey of research in large language models
                                                                               for electronic design automation,” ACM Transactions on
                                                                               Design Automation of Electronic Systems, vol. 30, no. 3,
                                                                               2025.
                                                                          [12] K. Xu, D. Schwachhofer, J. Blocklove, I. Polian, P. Do-
                                                                               manski, D. Pfluger, S. Garg, R. Karri, O. Sinanoglu,
                                                                               J. Knechtel, Z. Zhao, U. Schlichtmann, and B. Li,
                                                                               “Large language models for electronic design automa-
                                                                               tion,” 2025.
                                                                          [13] J. Wang, X. Chen, L. Zhang, and Z. Xie, “Real-
                                                                               bench: Benchmarking llms on real-world hardware de-
                                                                               sign specifications,” in The 62nd ACM/IEEE Design
                                                                               Automation Conference (DAC), ACM/IEEE, 2025.
                                                                          [14] S. Kumar, S. Mukhopadhyay, and S. Kundu, “Enhanc-
                                                                               ing llm performance on hardware design tasks via
                                                                               structural alignment,” in Proceedings of the IEEE Inter-
                                                                               national Symposium on Circuits and Systems (ISCAS),
                                                                               IEEE, 2025.
                                                                          [15] S. Liu, W. Fang, Y. Lu, J. Wang, Z. Qijun, H. Zhang,
                                                                               and Z. Xie, “Rtlcoder: Fully open-source and efficient
                                                                               llm-assisted rtl code generation technique,” in Proceed-
                                                                               ings of the IEEE/ACM International Conference on
                                                                               Computer-Aided Design (ICCAD), IEEE, 2024.



                                                                     28
[16] C.-T. Ho, H. Ren, and B. Khailany, “Verilogcoder:                  [29] M. Liu, T.-D. Ene, R. Kirby, C. Cheng, N. Pinckney,
     Autonomous verilog coding agents with graph-based                       R. Liang, J. Alben, H. Anand, S. Banerjee, I. Bayrak-
     planning and abstract syntax tree (ast)-based waveform                  taroglu, B. Bhaskaran, B. Catanzaro, A. Chaudhuri,
     tracing tool,” in Proceedings of the AAAI Conference on                 S. Clay, B. Dally, L. Dang, P. Deshpande, S. Dhodhi,
     Artificial Intelligence, vol. 39, pp. 300–307, Association              S. Halepete, E. Hill, J. Hu, S. Jain, A. Jindal,
     for the Advancement of Artificial Intelligence (AAAI),                  B. Khailany, G. Kokai, K. Kunal, X. Li, C. Lind,
     February 2025.                                                          H. Liu, S. Oberman, S. Omar, G. Pasandi, S. Pratty,
[17] Y. Zhao, H. Zhang, H. Huang, Z. Yu, and J. Zhao,                        J. Raiman, A. Sarkar, Z. Shao, H. Sun, P. P. Suthar,
     “Mage: A multi-agent engine for automated rtl code                      V. Tej, W. Turner, K. Xu, and H. Ren, “Chipnemo:
     generation,” in Proceedings of the 62nd ACM/IEEE De-                    Domain-adapted llms for chip design,” 2024.
     sign Automation Conference (DAC), IEEE/ACM, 2025.                  [30] G. Yang, W. Zheng, D. Liang, P. Hu, Y. Yang, S. Peng,
[18] B. Nadimi and H. Zheng, “A multi-expert large lan-                      Z. Li, J. Feng, X. Wei, K. Sun, D. Ma, H. Cheng,
     guage model architecture for verilog code generation,”                  Y. Shen, X. Chen, X. Hu, T. Y. Zhuo, and D. Lo, “Large
     in Proceedings of the IEEE International Workshop on                    language model for verilog code generation: Literature
     LLM-Aided Design (LAD), April 2024.                                     review and the road ahead,” 2025.
[19] W. Sun, S. Zhou, X. Liao, and H. Yao, “Eda-copilot:                [31] Anonymous, “AI/LLM-Based Security Verification: A
     A rag-powered intelligent assistant for eda tools,” ACM                 Survey and AI Accelerator Case Study,” arXiv preprint
     Transactions on Design Automation of Electronic Sys-                    arXiv:2604.01572, 2026.
     tems (TODAES), 2026.                                               [32] H. Liu, Y. Lu, M. Wang, X. Yao, and B. Yu, “Llm-
[20] A. Kumar et al., “Saarthi: The first ai formal verification             assisted circuit verification: A comprehensive survey,”
     engineer,” in Proceedings of DVCon U.S., 2025.                          in Proceedings of the 31st Asia and South Pacific
[21] R. Qiu, G. L. Zhang, R. Drechsler, U. Schlichtmann,                     Design Automation Conference, 2026.
     and B. Li, “CorrectBench: Automatic Testbench Gen-                 [33] Accellera Systems Initiative, Universal Verification
     eration with Functional Self-Correction using LLMs                      Methodology (UVM) User’s Guide, 2015.
     for HDL Design,” in Design, Automation and Test in                 [34] A. Gupta, “Formal hardware verification methods: A
     Europe (DATE), 2025.                                                    survey,” Formal Methods in System Design, vol. 1,
[22] R. Ma, Y. Yang, Z. Liu, J. Zhang, M. Li, J. Huang,                      no. 2–3, pp. 151–238, 1992.
     and G. Luo, “Verilogreader: LLM-aided hardware test                [35] E. M. Clarke, O. Grumberg, and D. A. Peled, Model
     generation,” arXiv preprint arXiv:2406.04373, 2024.                     Checking. Cambridge, MA, USA: MIT Press, 1999.
[23] Z. Yan, W. Fang, M. Li, M. Li, S. Liu, Z. Xie, and                 [36] A. Biere, A. Cimatti, E. Clarke, and Y. Zhu, “Bounded
     H. Zhang, “Assertllm: Generating hardware verification                  Model Checking Using Satisfiability Solving,” Formal
     assertions from design specifications via multi-llms,” in               Methods in System Design, vol. 19, no. 1, pp. 7–34,
     Proceedings of the 30th Asia and South Pacific Design                   2001.
     Automation Conference, ASPDAC ’25, (New York, NY,                  [37] N. Een and N. Sörensson, “Minisat: A sat solver with
     USA), p. 614–621, Association for Computing Machin-                     conflict-clause minimization,” in Theory and Applica-
     ery, 2025.                                                              tions of Satisfiability Testing, vol. 3569 of Lecture Notes
[24] A. Gupta, B. Mali, and C. Karfa, “Sangam: Sys-                          in Computer Science, pp. 502–518, Springer, 2005.
     temverilog assertion generation via monte carlo tree               [38] A. Biere, “Cadical at the sat race 2019,” in Proceedings
     self-refine,” in 2025 IEEE International Conference on                  of SAT Race 2019: Solver and Benchmark Descriptions,
     LLM-Aided Design (ICLAD), pp. 180–187, 2025.                            vol. B-2019-1 of Department of Computer Science
[25] Y. Bai, G. B. Hamad, S. Suhaib, and H. Ren, “Assertion-                 Series of Publications B, pp. 14–15, University of
     forge: Enhancing formal verification assertion genera-                  Helsinki, 2019.
     tion with structured representation of specifications and          [39] L. de Moura and N. Bjørner, “Z3: An efficient smt
     rtl,” in 2025 IEEE International Conference on LLM-                     solver,” in Tools and Algorithms for the Construction
     Aided Design (ICLAD), pp. 85–92, 2025.                                  and Analysis of Systems, vol. 4963 of Lecture Notes in
[26] B. Yao, N. Wang, J. Zhou, X. Wang, H. Gao, Z. Jiang,                    Computer Science, pp. 337–340, Springer, 2008.
     and N. Guan, “Location is key: Leveraging large lan-               [40] H. Barbosa, C. W. Barrett, M. Brain, G. Kremer,
     guage model for functional bug localization in verilog,”                H. Lachnitt, M. Mann, A. Mohamed, M. Mohamed,
     arXiv preprint arXiv:2409.15186, 2024. Version 2.                       A. Niemetz, A. Nötzli, A. Ozdemir, M. Preiner,
[27] M.-H. Tsai et al., “RTLFixer: Automatically Fixing                      A. Reynolds, Y. Sheng, C. Tinelli, and Y. Zohar, “cvc5:
     RTL Syntax Errors with Large Language Models,” in                       A versatile and industrial-strength smt solver,” in Tools
     International Conference on VLSI Design, 2024.                          and Algorithms for the Construction and Analysis of
[28] Z. Zang, Y. Song, A. Wang, B. W.-K. Ling, Q. Sun,                       Systems, vol. 13243 of Lecture Notes in Computer
     Z. Lei, F. Yang, C. Zhuo, and J. Luo, “The dawn                         Science, pp. 415–442, Springer, 2022.
     of agentic eda: A survey of autonomous digital chip                [41] IEEE Technology Navigator, “Formal verification—
     design,” 2026.                                                          Hardware verification.” https://technav.ieee.org/topic/



                                                                   29
     formal-verification/.                                                 N. Guan, X. Wang, and J. Yang, “Chatsva: Bridging sva
[42] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit,                      generation for hardware verification via task-specific
     L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin,                  llms,” ArXiv, vol. abs/2604.02811, 2026.
     “Attention is all you need,” in Advances in Neural               [56] S. Paul, A. Banerjee, S. Ghosh, S. Surendran, and
     Information Processing Systems, vol. 30, 2017.                        R. K. Gajavelly, “Supersaga: A supervisor-subordinate
[43] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter,                  agentic workflow for the generation of assertions,” in
     F. Xia, E. Chi, Q. V. Le, and D. Zhou, “Chain-of-                     2026 31st Asia and South Pacific Design Automation
     thought prompting elicits reasoning in large language                 Conference (ASP-DAC), pp. 420–425, 2026.
     models,” in Advances in Neural Information Processing            [57] R. Guo, A. Ayalasomayajula, H. Li, J. Zhou, S. K. Saha,
     Systems, vol. 35, pp. 24824–24837, 2022.                              and F. Farahmandi, “Svagent: Ai agent for hardware
[44] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin,              security verification assertion,” 2025.
     N. Goyal, H. Küttler, M. Lewis, W.-t. Yih,                      [58] A. Kumar, D. N. Gadde, K. K. Radhakrishna, and
     T. Rocktäschel, S. Riedel, and D. Kiela, “Retrieval-                 D. Lettnin, “Saarthi: The first ai formal verification
     augmented generation for knowledge-intensive nlp                      engineer,” 2025.
     tasks,” in Advances in Neural Information Processing             [59] N. Mashnoor, H. Kamali, and K. Azar, “From language
     Systems, vol. 33, pp. 9459–9474, 2020.                                to logic: Bridging llms and formal representations for
[45] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran,                            rtl assertion generation,” in 2026 IEEE 44th VLSI Test
     K. Narasimhan, and Y. Cao, “React: Synergizing rea-                   Symposium (VTS), pp. 1–5, 2026.
     soning and acting in language models,” in International          [60] V. N. Viswambharan, K. K. Radhakrishna, D. N. Gadde,
     Conference on Learning Representations, 2023.                         and A. Kumar, “Knowledge graphs, the missing link in
[46] T. Schick, J. Dwivedi-Yu, R. Dessi, R. Raileanu,                      agentic ai-based formal verification,” 2026.
     M. Lomeli, L. Zettlemoyer, N. Cancedda, and                      [61] F. Aditi and M. S. Hsiao, “Validatable generation of
     T. Scialom, “Toolformer: Language models can teach                    system verilog assertions from natural language spec-
     themselves to use tools,” in Advances in Neural Infor-                ifications,” in 2023 Fifth International Conference on
     mation Processing Systems, vol. 36, pp. 68539–68551,                  Transdisciplinary AI (TransAI), pp. 102–109, 2023.
     2023.                                                            [62] A. Menon, S. Miftah, S. Kundu, S. Kundu, A. Srivas-
[47] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Zhu, L. Jiang,                  tava, A. Raha, G. Sonnenschien, S. Banerjee, D. Math-
     S. Zhang, A. H. Awadallah, R. W. White, D. Burger,                    aikutty, and K. Basu, “Enhancing large language models
     and C. Wang, “Autogen: Enabling next-gen llm ap-                      for hardware verification: A novel systemverilog asser-
     plications via multi-agent conversation,” arXiv preprint              tion dataset,” ACM Trans. Des. Autom. Electron. Syst.,
     arXiv:2308.08155, 2023.                                               Aug. 2025. Just Accepted.
[48] C. B. Hahn, “Towards improving verification produc-              [63] W. Xiao, D. Ekberg, S. Garg, and R. Karri, “Hybrid-
     tivity with circuit-aware translation of natural language             nl2sva: Integrating rag and finetuning for llm-based
     to systemverilog assertions,” 2023.                                   nl2sva,” 2025.
[49] F. Siddiqui et al., “AutoSVA2: An Automated Frame-               [64] V. Pulavarthi, D. Nandal, S. Dan, and D. Pal, “Are llms
     work for Formal Property Verification Using LLMs,”                    ready for practical adoption for assertion generation?,”
     arXiv preprint arXiv:2403.XXXXX, 2024.                                2025.
[50] B. Mali, K. Maddala, V. Gupta, S. Reddy, C. Karfa,               [65] M. Kang, M. Liu, G. B. Hamad, S. Suhaib, and H. Ren,
     and R. Karri, “Chiraag: Chatgpt informed rapid and                    “Fveval: Understanding language model capabilities in
     automated assertion generation,” 2024.                                formal verification of digital hardware,” 2024.
[51] M. Shahidzadeh, B. Ghavami, S. Wilton, and L. Shan-              [66] N. Pinckney, C. Deng, C.-T. Ho, Y.-D. Tsai, M. Liu,
     non, “Automatic high-quality verilog assertion genera-                W. Zhou, B. Khailany, and H. Ren, “Comprehensive
     tion through subtask-focused fine-tuned llms and itera-               verilog design problems: A next-generation benchmark
     tive prompting,” 2024.                                                dataset for evaluating large language models and agents
[52] E. Tian, Y. Ci, Q. Yang, Y. Li, and Z. Lyu, “Assert-                  on rtl design and verification,” 2025.
     coder: Llm-based assertion generation via multimodal             [67] Y. Wu, W. Fang, J. Wang, W. Li, Z. Guo, and Z. Xie,
     specification extraction,” 2025.                                      “Assertllm2: A comprehensive llm benchmark for as-
[53] F. Wu, E. Pan, R. Kande, M. Quinn, A. Tyagi, D. K.                    sertion generation from design specifications,” 2026.
     Houngninou, J. Rajendran, and J. Hu, “Spec2assertion:            [68] S. Vasudevan, D. Sheridan, S. Patel, D. Tcheng,
     Automatic pre-rtl assertion generation using large lan-               B. Tuohy, and D. Johnson, “Goldmine: Automatic asser-
     guage models with progressive regularization,” 2025.                  tion generation using data mining and static analysis,” in
[54] H. Lyu, Y. Wang, Y. Du, M. Shi, Z. Chao, W. Li,                       2010 Design, Automation & Test in Europe Conference
     T. Wang, and H. Li, “Assertgen: Enhancement of llm-                   & Exhibition (DATE 2010), pp. 626–629, 2010.
     aided assertion generation through cross-layer signal            [69] A. Danese, N. D. Riva, and G. Pravadelli, “A-team:
     bridging,” 2025.                                                      Automatic template-based assertion miner,” in 2017
[55] L. T. Fu, J. Zhou, S. Ren, M. Zhang, J. Xiong, H. Jiang,              54th ACM/EDAC/IEEE Design Automation Conference



                                                                 30
     (DAC), pp. 1–6, 2017.                                                generation for RTL designs using directed graybox
[70] S. Germiniani and G. Pravadelli, “Harm: A hint-based                 fuzzing,” in Proceedings of the 58th ACM/IEEE Design
     assertion miner,” IEEE Transactions on Computer-                     Automation Conference, pp. 529–534, 2021.
     Aided Design of Integrated Circuits and Systems,                [85] D. N. Gadde, A. Kumar, D. Lettnin, and S. Simon,
     vol. 41, no. 11, pp. 4277–4288, 2022.                                “FuzzWiz: Fuzzing framework for efficient hardware
[71] A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao,                 coverage,” arXiv preprint arXiv:2410.17732, 2024.
     S. Wiegreffe, U. Alon, N. Dziri, S. Prabhumoye,                 [86] J. Bhandari, J. Knechtel, R. Narayanaswamy, S. Garg,
     Y. Yang, S. Gupta, B. P. Majumder, K. Hermann,                       and R. Karri, “LLM-aided testbench generation and
     S. Welleck, A. Yazdanbakhsh, and P. Clark, “Self-refine:             bug detection for finite-state machines,” arXiv preprint
     Iterative refinement with self-feedback,” 2023.                      arXiv:2406.17132, 2024.
[72] J. R. Imperial and H. Zheng, “Specalign: A semantic             [87] Z. Zhang, B. Szekely, P. Gimenes, G. Chadwick, H. Mc-
     alignment framework for systemverilog assertion gen-                 Nally, J. Cheng, R. Mullins, and Y. Zhao, “LLM4DV:
     eration,” 2026.                                                      Using large language models for hardware test stimuli
[73] IEEE, “IEEE Standard for SystemVerilog–Unified                       generation,” arXiv preprint arXiv:2310.04535, 2023.
     Hardware Design, Specification, and Verification Lan-           [88] S. Lowe, E. Hilaneh, A. Babbit, N. Gopalan,
     guage.” IEEE Std 1800-2023, 2023. Official standard                  V. Chhabria, and A. Arora, “Spec2Cov: An agentic
     landing page.                                                        framework for code coverage closure of digital hard-
[74] Accellera Systems Initiative, “UVM 1.2 User’s Guide,”                ware designs,” arXiv preprint arXiv:2604.15606, 2026.
     2015.                                                           [89] Y. Zhao, Z. Wu, B. Yuan, Z. Yu, H. Zhang, W. Ni, C.-
[75] cocotb contributors, “cocotb Documentation,” 2026.                   T. Ho, H. Ren, and J. Zhao, “PRO-V-R1: Reasoning
     Accessed 2026-06-16.                                                 enhanced programming agent for RTL verification,”
[76] R. Qiu, G. L. Zhang, R. Drechsler, U. Schlichtmann,                  arXiv preprint arXiv:2506.12200, 2025.
     and B. Li, “Autobench: Automatic testbench generation           [90] J. Wang, Z. Yao, Y. Pi, X. Li, F. Song, J. Wang, Y. Xie,
     and evaluation using llms for hdl design,” in Proceed-               S. Wang, and Y. Bao, “UCAgent: An end-to-end agent
     ings of the 2024 ACM/IEEE International Symposium                    for block-level functional verification,” arXiv preprint
     on Machine Learning for CAD, 2024.                                   arXiv:2603.25768, 2026.
[77] R. Qiu, G. L. Zhang, R. Drechsler, U. Schlichtmann,             [91] R. Qiu, G. L. Zhang, R. Drechsler, T. Ho, U. Schlicht-
     and B. Li, “Correctbench: Automatic testbench gen-                   mann, and B. Li, “ConfiBench: Automatic testbench
     eration with functional self-correction using llms for               generation with confidence-based scenario mask and
     hdl design,” in Design, Automation and Test in Europe                testbench ensemble using LLMs for HDL design,”
     Conference, 2025.                                                    ACM Transactions on Design Automation of Electronic
[78] C.-C. Meng, Y.-R. Lu, G.-Y. Lin, T. T. Yeh, K.-C. Wu,                Systems, 2025.
     and I.-C. Wu, “Haven: Hybrid automated verification             [92] N. S. Murthy, E. Nelson, S. S. Sapatnekar, and J. Sar-
     engine for uvm testbench synthesis with llms,” arXiv                 tori, “VerifLLMBench: An open-source benchmark for
     preprint arXiv:2604.27643, 2026.                                     testbenches generated with large language models,”
[79] J. Ye, D. Pan, H. Liu, Y. Hu, J. Zhou, K. Xu, X. Fang,               in Design and Verification Conference (DVCon) U.S.,
     X. Wang, N. Guan, and Z. Jiang, “Uvmarvel: an auto-                  2025.
     mated llm-aided uvm machine for subsystem-level rtl             [93] J. Ye, Y. Hu, K. Xu, D. Pan, Q. Chen, J. Zhou, S. Zhao,
     verification,” arXiv preprint arXiv:2605.04704, 2026.                X. Fang, X. Wang, N. Guan, and Z. Jiang, “From con-
[80] J. McEllin, R. Conway, and C. Ryan, “AVERT: An auto-                 cept to practice: an automated llm-aided uvm machine
     matic verilog testbench generation tool for grammatical              for rtl verification,” arXiv preprint arXiv:2504.19959,
     evolution,” in 2022 33rd Irish Signals and Systems                   2025.
     Conference (ISSC), 2022.                                        [94] D. Dranga, “Trials of using generative AI for APB
[81] I. Ioannides and K. Eder, “Coverage-directed test gen-               UVM testbench generation,” Romanian Journal of In-
     eration automated by machine learning: A review,”                    formation Technology and Automatic Control, vol. 34,
     ACM Transactions on Design Automation of Electronic                  no. 2, pp. 75–84, 2024.
     Systems, vol. 17, no. 1, 2012.                                  [95] W. Liu, F. Hou, J. Zhang, H. Liu, and A. Lei, “A multi-
[82] A. A. Jayasena and P. Mishra, “Directed test generation              agent generative AI framework for IC module-level ver-
     for hardware validation: A survey,” ACM Computing                    ification automation,” arXiv preprint arXiv:2507.21694,
     Surveys, vol. 56, no. 5, pp. 1–36, 2024.                             2025.
[83] K. Laeufer, J. Koenig, D. Kim, J. Bachrach, and K. Sen,         [96] D. Saha, S. Tarek, H. A. Shaikh, K. T. Hasan,
     “RFUZZ: Coverage-directed fuzz testing of RTL on                     P. S. Nalluri, M. A. Hasan, N. Alam, J. Zhou,
     FPGAs,” in Proceedings of the 2018 IEEE/ACM Inter-                   S. K. Saha, M. Tehranipoor, and F. Farahmandi, “SV-
     national Conference on Computer-Aided Design, 2018.                  LLM: An agentic approach for SoC security verifi-
[84] S. Canakci, L. Delshadtehrani, F. Eris, M. B. Taylor,                cation using large language models,” arXiv preprint
     M. Egele, and A. Joshi, “DirectFuzz: Automated test                  arXiv:2506.20415, 2025.



                                                                31
 [97] M. Hassan, M. Nadeem, K. Qayyum, C. K. Jha, and                         X. Fang, S. Zhao, N. Guan, and Z. Jiang, “Insights from
      R. Drechsler, “Prompt. verify. repeat. LLMs in the hard-                rights and wrongs: A large language model for solving
      ware verification cycle,” in 2025 IEEE International                    assertion failures in RTL design,” in Proc. ACM/IEEE
      Conference on Omni-layer Intelligent Systems, 2025.                     Design Automation Conference (DAC), pp. 1–7, 2025.
 [98] B. Nadimi, K. Filom, D. Chen, and H. Zheng, “TB or                [110] K. Xu, J. Sun, Y. Hu, X. Fang, W. Shan, X. Wang, and
      Not TB: Coverage-driven direct preference optimiza-                     Z. Jiang, “MEIC: Re-thinking RTL debug automation
      tion for verilog stimulus generation,” arXiv preprint                   using LLMs,” in Proc. IEEE/ACM International Con-
      arXiv:2511.15767, 2025.                                                 ference on Computer-Aided Design (ICCAD), pp. 1–9,
 [99] H. Zhang, Z. Yu, C.-T. Ho, H. Ren, B. Khailany, and                     2024.
      J. Zhao, “LLM4Cov: Execution-aware agentic learning               [111] Z. Luo, F. Cui, K. Zhou, R. Guo, M. Xia, H. Hou,
      for high-coverage testbench generation,” arXiv preprint                 and Y. Liang, “R3A: Reliable RTL repair frame-
      arXiv:2602.16953, 2026.                                                 work with multi-agent fault localization and stochas-
[100] E.-M. Huang, Y.-H. Kao, R.-H. Deng, W.-P. Hsin, Y.-T.                   tic tree-of-thoughts patch generation,” arXiv preprint
      Hsieh, C. Liang, H.-Y. Tsou, M.-C. Chen, Y.-K. Hung,                    arXiv:2511.20090, 2025. Version 2.
      S.-C. Ho, P.-H. Huang, S.-H. Hung, and H. T. Kung,                [112] B. Ahmad, S. Thakur, B. Tan, R. Karri, and H. Pearce,
      “Structured testbench generation for llm-driven hdl                     “On hardware security bug code fixes by prompting
      design and verification-oriented data curation,” arXiv                  large language models,” IEEE Transactions on Infor-
      preprint arXiv:2606.12983, 2026.                                        mation Forensics and Security, vol. 19, pp. 4043–4057,
[101] N. Pinckney, C. Deng, C.-T. Ho, Y.-D. Tsai, M. Liu,                     2024.
      W. Zhou, B. Khailany, and H. Ren, “Comprehensive                  [113] M. Akyash and H. M. Kamali, “Self-HWDebug: Au-
      verilog design problems: A next-generation bench-                       tomation of LLM self-instructing for hardware security
      mark dataset for evaluating large language models and                   verification,” in Proc. IEEE Computer Society Annual
      agents on RTL design and verification,” arXiv preprint                  Symposium on VLSI (ISVLSI), pp. 391–396, 2024.
      arXiv:2506.14074, 2025.                                           [114] Y. Hu, J. Ye, K. Xu, J. Sun, S. Zhang, X. Jiao,
[102] D. Pal and S. Vasudevan, “Symptomatic bug localiza-                     D. Pan, J. Zhou, N. Wang, W. Shan, X. Fang, X. Wang,
      tion for functional debug of hardware designs,” in Proc.                N. Guan, and Z. Jiang, “UVLLM: An automated
      International Conference on VLSI Design and Inter-                      universal RTL verification framework using LLMs,”
      national Conference on Embedded Systems (VLSID),                        in Proc. ACM/IEEE Design Automation Conference
      pp. 517–522, 2016.                                                      (DAC), pp. 1–7, 2025.
[103] X. Yao, H. Li, T. H. Chan, W. Xiao, M. Yuan, Y. Huang,            [115] K. Qayyum, M. Hassan, S. Ahmadi-Pour, C. K. Jha,
      L. Chen, and B. Yu, “HDLdebugger: Streamlining HDL                      and R. Drechsler, “From bugs to fixes: HDL bug
      debugging with large language models,” ACM Trans-                       identification and patching using LLMs and RAG,” in
      actions on Design Automation of Electronic Systems,                     Proc. IEEE LLM Aided Design Workshop (LAD), pp. 1–
      vol. 30, no. 6, pp. 102:1–102:26, 2025.                                 5, 2024.
[104] H. Witharana, Y. Lyu, S. Charles, and P. Mishra, “A               [116] Y. Bai and H. Ren, “Learning to debug: LLM-organized
      survey on assertion-based hardware verification,” ACM                   knowledge trees for solving RTL assertion failures,”
      Computing Surveys, vol. 54, no. 11s, pp. 1–33, 2022.                    arXiv preprint arXiv:2511.17833, 2025. Version 2.
[105] B. Ahmad, J. Ah-Kiow, B. Tan, R. Karri, and H. Pearce,            [117] P. Zheng, J. Qin, F. Zhang, N. Chitla, Z. Wan, S. Wu,
      “FLAG: Finding line anomalies (in RTL code) with gen-                   Y. Cao, C. Ding, and Y. Zhao, “HDLxGraph: Bridging
      erative AI,” ACM Transactions on Design Automation                      large language models and HDL repositories via HDL
      of Electronic Systems, vol. 30, no. 6, pp. 103:1–103:30,                graph databases,” in Proc. Asia and South Pacific De-
      2025.                                                                   sign Automation Conference (ASP-DAC), pp. 533–540,
[106] H. Lyu, Y. Du, Y. Wang, Z. Chao, T. Wang,                               2026.
      and H. Li, “AssertFix: Empowering automated asser-                [118] W. Lv, Y. Xia, X. Chen, and L. Kuang, “ViTAD: Timing
      tion fix via large language models,” arXiv preprint                     violation-aware debugging of RTL code using large
      arXiv:2509.23972, 2025. Version 1.                                      language models,” arXiv preprint arXiv:2508.13257,
[107] Y. Bai, G. B. Hamad, C.-T. Ho, S. Suhaib, and H. Ren,                   2025. Version 1.
      “FVDebug: An LLM-driven debugging assistant for                   [119] W. Fu, K. Yang, R. G. Dutta, X. Guo, and G. Qu,
      automated root cause analysis of formal verification fail-              “LLM4SecHW: Leveraging domain-specific large lan-
      ures,” arXiv preprint arXiv:2510.15906, 2025. Version                   guage model for hardware debugging,” in Proc. Asian
      1.                                                                      Hardware Oriented Security and Trust Symposium
[108] Y. Tsai, M. Liu, and H. Ren, “RTLFixer: Automatically                   (AsianHOST), pp. 1–6, 2023.
      fixing RTL syntax errors with large language models,”             [120] N. Wang, B. Yao, J. Zhou, Y. Hu, X. Wang, Z. Jiang,
      in Proc. ACM/IEEE Design Automation Conference                          and N. Guan, “VeriDebug: A unified LLM for verilog
      (DAC), pp. 1–6, 2024.                                                   debugging via contrastive embedding and guided cor-
[109] J. Zhou, Y. Ji, N. Wang, Y. Hu, X. Jiao, B. Yao,                        rection,” in Proc. IEEE International Conference on



                                                                   32
      LLM-Aided Design (ICLAD), pp. 61–67, 2025.                             tion via llms for model checking,” arXiv preprint
[121] B. Yao, N. Wang, X. Liu, Y. Du, Y. Hu, H. Gao,                         arXiv:2602.23389, 2026.
      Z. Jiang, and N. Guan, “ARSP: Automated repair of ver-           [134] M. Miao, G. Hu, Z. Yang, and H. Zhang, “Ic3-evolve:
      ilog designs via semantic partitioning,” arXiv preprint                Proof-/witness-gated offline llm-driven heuristic evolu-
      arXiv:2508.16517, 2025. Version 1.                                     tion for ic3 hardware model checking.” arXiv preprint
[122] Y. Wang, C. Liu, J. Zhang, L. Zhang, L. Cheng, X. Li,                  arXiv:2604.03232, 2026. arXiv.
      and H. Li, “VeriPilot: An LLM-powered verilog de-                [135] Y. Liu et al., “Deeprtl2: A versatile model for rtl-related
      bugging framework,” arXiv preprint arXiv:2606.23759,                   tasks,” in Findings of the Association for Computational
      2026. Version 1.                                                       Linguistics (ACL), pp. 6485–6500, 2025.
[123] Y.-T. Liu and C. Yu, “VeriTrace: Human-like temporal             [136] J. Jiang, J. Wang, Y. Yan, Y. Liu, and J. Zhu, “For-
      exploration completes agentic action space,” in Proc.                  maleval,” ACM Trans. Design Autom. Electron. Syst.,
      IEEE International Conference on LLM-Aided Design                      vol. 30, no. 1, pp. 1–25, 2025.
      (ICLAD), 2026.                                                   [137] K. Li et al., “Formalrtl: Verified rtl synthesis at scale,”
[124] Z. Luo, Y. Xu, R. Guo, F. Cui, K. Zhou, M. Xia, H. Hou,                arXiv preprint arXiv:2603.08738, 2026.
      Y. Luo, and Y. Liang, “Clover: A neural-symbolic agen-           [138] Y. Su, Q. Yang, Y. Ci, Y. Li, T. Bu, and Z. Huang,
      tic harness with stochastic tree-of-thoughts for verified              “Deeply optimizing the sat solver for the ic3 algorithm,”
      RTL repair,” arXiv preprint arXiv:2604.17288, 2026.                    in Computer Aided Verification – 37th International
      Version 1.                                                             Conference, CAV 2025, Proceedings, Part I, vol. 15931
[125] L. Collini, B. Ahmad, J. Ah-Kiow, and R. Karri, “MAR-                  of Lecture Notes in Computer Science, pp. 237–257,
      VEL: Multi-agent RTL vulnerability extraction using                    Springer, 2025.
      large language models,” ACM Transactions on Design               [139] Y. Su, Q. Yang, Y. Ci, T. Bu, and Z. Huang, “The
      Automation of Electronic Systems, 2026.                                ric3 hardware model checker,” in Computer Aided Ver-
[126] Z. Fang, R. Chen, Z. Yang, Y. Guo, H. Dai, and                         ification – 37th International Conference, CAV 2025,
      L. Wang, “LintLLM: An open-source verilog linting                      Proceedings, Part I, vol. 15931 of Lecture Notes in
      framework based on large language models,” in Proc.                    Computer Science, pp. 167–177, Springer, 2025.
      Great Lakes Symposium on VLSI (GLSVLSI), pp. 673–                [140] Y. Sun, F. Ye, X. Zhang, S. Huang, B.-Z. Zhang, K. Wei,
      680, 2025.                                                             and S. Cai, “Autosat: Automatically optimize sat solvers
[127] Y. Tan, X. Meng, Z. Jiang, and Y. Lyu, “AutoVer-                       via large language models,” Journal of Artificial Intel-
      iFix: Automatically correcting errors and enhancing                    ligence Research, vol. 76, 2026.
      functional correctness in LLM-generated verilog code,”           [141] J. Sheng, Y. Lin, J. Wu, Y. Huang, J. Shi, M. Zhang,
      in Proc. Asia and South Pacific Design Automation                      and X. Wang, “Solsearch: An llm-driven framework
      Conference (ASP-DAC), pp. 526–532, 2026.                               for efficient sat-solving code generation,” in Proceed-
[128] C.-T. Ho, H. Ren, and B. Khailany, “VerilogCoder: Au-                  ings of the 47th International Conference on Software
      tonomous verilog coding agents with graph-based plan-                  Engineering: New Ideas and Emerging Results (ICSE-
      ning and abstract syntax tree (AST)-based waveform                     NIER), pp. 31–35, IEEE/ACM, 2025.
      tracing tool,” in Proceedings of the AAAI Conference             [142] Y. Sun, F. Ye, Z. Chen, K. Wei, and S. Cai, “Discovering
      on Artificial Intelligence, vol. 39, pp. 300–307, 2025.                heuristics in a complex sat solver with large language
[129] X. Kong, T. Tabassum, M. Abdelwahab, and H. Zheng,                     models,” arXiv preprint arXiv:2507.22876, 2025.
      “A progressive approach to synthesizable rtl design gen-         [143] T.-C. Hwang, F. Yu, and J.-H. R. Jiang, “Agentic taxa-
      eration using llms,” arXiv preprint arXiv:2607.18519,                  tion optimization via llm smt-constraint reasoning,” in
      2026.                                                                  Proceedings of the IEEE/ACM 48th International Con-
[130] A. Biere, A. Cimatti, E. M. Clarke, O. Strichman,                      ference on Software Engineering: Software Engineering
      and Y. Zhu, “Bounded model checking,” Advances in                      in Practice (ICSE-SEIP ’26), pp. 797–807, IEEE/ACM,
      Computers, vol. 58, pp. 117–148, 2003.                                 2026.
[131] K. Qayyum, M. Hassan, S. Ahmadi-Pour, C. K. Jha,
      and R. Drechsler, “Late-breaking results: Llm-assisted
      automated incremental proof generation for hardware
      verification,” in Proceedings of the 63rd ACM/IEEE
      Design Automation Conference (DAC), (New York, NY,
      USA), pp. 1–2, Association for Computing Machinery,
      2026.
[132] M. Hassan et al., “Llm-guided formal verification cou-
      pled with mutation testing,” in Proceedings of the
      Design, Automation and Test in Europe Conference
      (DATE), 2024.
[133] Y. Su et al., “Cill: Cti-guided invariant genera-



                                                                  33
