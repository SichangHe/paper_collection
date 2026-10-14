                                                     Towards Reliable AI-Assisted Analog Design:
                                              Template-Constrained LLM Agents for SAR ADC Generation
                                                      Dimple Vijay Kochar                                        Hae-Seung Lee*                         Anantha P. Chandrakasan*
                                             Massachusetts Institute of Technology                  Massachusetts Institute of Technology           Massachusetts Institute of Technology
                                                    Cambridge, MA, USA                                     Cambridge, MA, USA                              Cambridge, MA, USA

                                         Abstract                                                                                                                           Grounded Expert
                                                                                                                                 Input Specs                                Knowledge/Plan
                                         While Large Language Models (LLMs) have demonstrated signif-
                                         icant capability in software code generation, their application to
                                         analog Electronic Design Automation (EDA) is bottlenecked. Owing
                                         to limited circuit topology understanding and data, directly prompt-
                                         ing LLMs and multimodal models leads to hallucinations and failure                                          Stage 1: Grounding
                                                                                                                                                    In Expert Knowledge
                                         to produce schematics capable of passing rigorous SPICE simula-
                                         tions, as we show in our work. Instead, we propose an end-to-end,
                                                                                                                                                            Final
                                         multi-step LLM agentic framework ATLAS, capable of generating
                                                                                                                                                            Circuit
                                         a functional Successive Approximation Register (SAR) Analog-to-
                                         Digital Converter (ADC) that successfully passes simulation valida-
arXiv:2607.14165v1 [cs.SE] 15 Jul 2026




                                         tion. To adhere to the rigid constraints of analog design, we utilize
                                         expert knowledge to ground the LLM in its planning, selection,
                                                                                                                              Stage 3: Netlist Sizing                        Stage 2: Netlist
                                         parameterization, and iterative modification. As part of ATLAS, we                     And Optimization                               Generation
                                         introduce Template-Constrained Generation - which unlike other
                                         template-based works - builds towards a more generalized SAR                        Figure 1: High-level workflow of our proposed multi-step
                                         ADC generation flow. We demonstrate a strong proof-of-concept                       LLM-based agentic framework ATLAS for creating SAR ADCs
                                         of our framework by developing SAR ADCs across technology                           from user-defined input specifications in an end-to-end au-
                                         nodes and input specs. Overall, our expert-knowledge grounded                       tomated manner.1
                                         multi-step agentic ATLAS establishes a pragmatic foundation for
                                         integrating LLMs into reliable analog design methodologies.

                                         Keywords                                                                            models for designing analog schematics from scratch. Our study
                                                                                                                             demonstrates that directly prompting LLMs in an unconstrained
                                         Analog-to-Digital Converter, ADC, SAR ADC, LLMs, Large Lan-                         manner frequently results in hallucinations, producing physically
                                         guage Models, Agents, Template                                                      unviable schematics with connectivity errors.
                                                                                                                                To address these critical limitations, this work shifts the para-
                                         1     Introduction                                                                  digm from unconstrained circuit generation to grounded, feedback-
                                         Continuous scaling of technology nodes and ever-increasing de-                      based synthesis. Rather than forcing the LLM to generate com-
                                         mand for mixed-signal Integrated Circuits (ICs) necessitate efficient,              plex analog topologies from scratch, we propose an end-to-end,
                                         scalable design methodologies. Within these, Analog-to-Digital                      multi-step LLM agentic framework ATLAS - Agentic Template-
                                         Converters (ADCs) - particularly Successive Approximation Regis-                    constrained LLM-based ADC Synthesizer (illustrated in Figure 1).
                                         ter (SAR) ADCs - are critical components that bridge the physical                   The core distinction of our framework lies in the grounding with ex-
                                         and digital domains. However, while digital Electronic Design Au-                   pert knowledge across various components for planning, selection,
                                         tomation (EDA) workflows have achieved high levels of abstraction                   stitching, re-configuration, testbench generation, etc., designed
                                         and automation [1], analog design remains largely manual, iterative,                specifically for reliable analog circuit synthesis. We also introduce
                                         and heavily intuition-driven [2]. This lack of scalable automated                   a generalized Template-Constrained generation that enables AT-
                                         synthesis for analog circuits creates a severe bottleneck in modern                 LAS to select component-wise expert templates and structurally
                                         System-on-Chip development.                                                         modify them to meet the target specifications. Feedback from our
                                            Recently, Large Language Models (LLMs) have demonstrated                         rule-based verification and simulation engines allows ATLAS to
                                         transformative capabilities in automated software engineering,                      self-debug and improve the circuit. Overall, by constraining the
                                         logic synthesis, and hardware description language (HDL) genera-                    generative search space, our agentic framework prevents the LLM
                                         tion and verification [1, 3–5]. However, its utility for analog EDA                 from diverging into physically impossible configurations while still
                                         has been restrictive, owing to the rigid, continuous-domain physical                harnessing its capacity for rapid iteration and code generation.
                                         constraints in analog EDA that differ fundamentally from discrete                      To demonstrate the efficacy of our framework, we utilize it to
                                         digital logic or software code. To this end, we conduct a deep qual-                synthesize a low-power 8-bit SAR ADC on Cadence GPDK-45nm
                                         itative study to explore the utility of existing LLMs/multimodal                    technology node. Our agentic framework generated ADC success-
                                         1We acknowledge the utilization of Generative AI - specifically Nano Banana - for   fully meets the input specs with an ENOB of 7.59. We further show
                                         creating illustrations and figures in our paper.                                    ATLAS’s generalizability by generating three additional SAR ADCs:
                                                                                                                                             Kochar et al.


         * Double-Tail Dynamic Comparator                                                              ...
                                                                                                       * Intermediate coupling transistors
         .SUBCKT DoubleTail INP INN VDD GND OUT CLK                                                    M_c1 node_latchP node_preP
         * First tail: Differential input stage                                                        node_tail2 VDD pmos_model W=2u
         M1 INP NODE1 VDD VDD PMOS L=0.18u W=15u                                                       L=0.18u
         M2 INN NODE1 VDD VDD PMOS L=0.18u W=15u                                                       M_c2 node_latchN node_preN
                                                                                                       node_tail2 VDD pmos_model W=2u
         * Second tail: Regenerative latch stage                                                       L=0.18u
         M3 NODE1 NODE2 GND GND NMOS L=0.18u W=10u                                                     ...
         M4 NODE1 NODE2 GND GND NMOS L=0.18u W=10u

         * Biasing transistor for second tail                                                          ...
         (clocked)                                                                                     * Cross-coupled latch
         M5 NODE1 GND CLK GND NMOS L=0.18u W=5u                                                        M3 outp outn vdd vdd PMOS L=45n W=2u
                                                                                                       M4 outn outp vdd vdd PMOS L=45n W=2u
         * Output stage                                                                                M5 outp outn 0 0 NMOS L=45n W=1u
         M6 NODE2 OUT GND GND NMOS L=0.18u W=8u                                                        M6 outn outp 0 0 NMOS L=45n W=1u
         .ENDS DoubleTail                                                                              ...


                           (a) Prompting GPT-4o for Double-Tail Dynamic Comparator                    (b) Prompting Gemini 3.1 and ChatGPT-Plus
                                                                                                               for Miyahara Comparator


Figure 2: Highlighting several limitations of directly prompting LLMs for netlist generation. On the left (a), we highlight several
severe issues like shorted gates, input to drains, etc. in the GPT-4o created netlist. On the right (b), we highlight issues like
missing connections and missing intermediate cross-coupling when prompting frontier LLMs.


(1) the original 8-bit SAR ADC transferred to TSMC 65nm (gen-                  digital standard cells [13] to create synthesizable analog building
eralization across technology nodes), (2) a 4-bit SAR ADC (gen-                blocks. On the algorithmic sizing front, recent optimization tech-
eralization across input specifications), and (3) a 10-bit SAR ADC             niques explicitly targeting SAR ADCs include multi-agent reinforce-
(capability of bit modification).                                              ment learning [14], global-local optimization [15], and automated
   In conclusion, our work makes the following contributions: (1)              sizing via analytical equations [16]. Despite achieving high opti-
we qualitatively showcase the limitations of direct prompting of               mization efficiency, these approaches inherently function as sizing
LLMs and multimodal models for analog circuit generation, (2) we               algorithms for a single, fixed SAR ADC, lacking the flexibility to
propose a multi-step LLM agentic framework ATLAS to reliably                   easily generalize across varied architectural design spaces.
ground the circuit generation, and (3) we demonstrate the efficacy of
our framework by synthesizing four SAR ADCs across technology                     LLMs for Circuit Design. Several works [17–19] have utilized
nodes and input specs. Overall, our work serves as a strong proof-             LLMs plugged with external optimizers for analog circuits sizing.
of-concept for reliable LLM-assisted analog design.                            Specific to analog circuit design, several works [20, 21] have demon-
   The remainder of the paper is organized as follows. Section 2               strated that general-purpose LLMs can not design even simple ana-
discusses the past works in this direction. Section 3 shows various            log circuits, as we also concur through our case study of designing
qualitative results highlighting the limitations of directly prompting         simple ADC components in Section 3. AnalogXpert [22] utilizes
LLMs for ADC netlist generation. Section 4 provides a detailed                 in-context examples for topology utilizing sub-circuit connections,
description of our proposed multi-step LLM agentic framework                   but demonstrates poor LLM performance. Owing to lack of strong
ATLAS. Section 5 demonstrates the efficacy of our framework to                 analog principles in mainstream LLMs, works like Artisan [23] pro-
generate a low-power 8-bit SAR ADC end-to-end, while Section 6                 pose niche task-specific fine-tuning of LLMs to boost performance
highlights the generalizability of our work. We conclude and discuss           on simple and specialized circuits. In a similar direction, ChipNeMo
future work in Section 7.                                                      [4] and AnalogSeeker [24] propose data curation and train foun-
                                                                               dation models for digital and analog design, respectively. In other
                                                                               directions, AnalogCoder [25], AmpAgent [26] and LADAC [27]
2   Related Works
                                                                               develop agentic LLM frameworks for schematic design of simpler
Here, we briefly discuss various works in the domain of automating             circuits like amplifiers, oscillators, etc. Majorly, most of these works
analog design and utilizing LLMs/AI in circuit design.                         have explored LLMs for simpler analog circuits, while we focus our
                                                                               work on designing SAR ADCs.
   Computer-Aided Design (CAD) for Analog Circuits. Recent re-
search has been dedicated to automating analog circuit sizing, with
methodologies spanning from analytical equation derivations to                 3     Direct LLM Prompting Limitations
Bayesian Optimization (BO) [6, 7]. Recently, there has also been               In this section, we evaluate the capability of LLMs and multimodal
a surge of works utilizing reinforcement learning (RL) methods                 LLMs to understand circuit specifications and create netlists for
[8, 9]. Within the specific domain of Successive Approximation                 analog design when prompted directly in an end-to-end fashion.
Register (SAR) ADCs, automation efforts have largely bifurcated                By highlighting the limitations of existing LLMs, we motivate our
into topology generation frameworks and algorithmic sizing. Gen-               agentic framework in Section 4. Compared to other works [17, 18],
eration frameworks frequently rely on template-based compilers                 we note that our work is not an exhaustive benchmark/evaluation
[10–12] that use pre-defined topologies to automate layout assem-              of LLMs, but rather provides qualitative case studies to highlight
bly. Alternatively, macro-based SAR ADC generation leverages                   some limitations of direct prompting.
                  M5 NODE1 GND CLK GND NMOS L=0.18u W=5u
       * Output stage                                                                                                      M4 outnM5 outp
                                                                                                                                   outp vdd outn  0 0 L=45n
                                                                                                                                             vdd PMOS  NMOS
              * Output
       M6 NODE2        stage
                 OUT GND  GND NMOS L=0.18u W=8u                                                                            M5 outpM6 outn
                                                                                                                                   outn 0 0 outp
                                                                                                                                             NMOS 0 0 NMOS
                                                                                                                                                  L=45n W=1
              M6 NODE2 OUT GND GND NMOS L=0.18u W=8u
       .ENDS DoubleTail                                                                                                    M6 outn...
                                                                                                                                   outp 0 0 NMOS L=45n W=1
                  .ENDS DoubleTail                                                                                         ...

                                    (a) Prompting   GPT-4o  forforDouble-Tail  Dynamic  Comparator                                (b) Prompting
                                                                                                                          (b) Prompting  Gemini 3.1Gemini 3.1
                                                                                                                                                    and ChatG
                                         (a) Prompting GPT-4o      Double-Tail Dynamic Comparator
                                                                                                                                    for Miyahara ComparatorCo
                                                                                                                                             for Miyahara
Towards Reliable AI-Assisted Analog Design




                  * Low-offset Design Netlist

                  M7 Vrefp N1 Vdd Vdd PMOS W=Wp7 L=Lp7                    Figure 4: Highlighting the limitations and lack of general-
       * Low-offset
              M8 VrefnDesign
                       N2 Vdd Netlist
                              Vdd PMOS W=Wp8 L=Lp8                        ization of utilizing existing fine-tuned models for netlist
                  M3 Vinp N1 Voutp Vss NMOS W=Wn3 L=Ln3
              M4 N1
                 VinnVdd
                       N2 Vdd
                           VoutnPMOS
                                  Vss NMOS  W=Wn4 L=Ln4
                                                                          generation. (left) Original circuit, (right) Fine-tuned model
       M7 Vrefp                        W=Wp7   L=Lp7
              M5 N2
       M8 Vrefn  Voutp
                     VddN3Vdd
                            N1 Vss  NMOS
                                 PMOS     W=Wn5L=Lp8
                                       W=Wp8    L=Ln5                     generated incorrect circuit.
       M3 VinpM6N1
                 Voutn N3 N2 Vss NMOS W=Wn6 L=Ln6
                    Voutp Vss NMOS W=Wn3 L=Ln3
              M1 N1 N3 Clk Vss NMOS W=Wn1 L=Ln1
       M4 VinnM2N2
                 N2 Voutn
                     N3 Clk Vss
                              Vss NMOS   W=Wn4L=Ln2
                                  NMOS W=Wn2    L=Ln4
       M5 Voutp
              M9 N3  N1 Clk
                 Voutp   VssVssNMOS
                                  Vss W=Wn5  L=Ln5
                                       NMOS W=Wn9 L=Ln9
       M6 Voutn
              M10N3  N2 Vss
                   Voutn       NMOS
                          Clk Vss  VssW=Wn6  L=Ln6 L=Ln10
                                        NMOS W=Wn10                          Under a higher compute budget, we also survey frontier models
              M11Clk
       M1 N1 N3    Vdd Vss
                       N3 Clk   VddW=Wn1
                             NMOS   PMOS W=Wp11
                                           L=Ln1 L=Lp11                   like Gemini 3.1 and ChatGPT Plus. These models are much better at
              ClpClk
       M2 N2 N3    Voutp
                       VssVssNMOS
                               C1 W=Wn2 L=Ln2
              Cln Voutn Vss C1
                                                                          analog design fundamentals and avoid the basic mistakes made by
       M9 Voutp  Clk Vss Vss NMOS W=Wn9 L=Ln9                             the smaller models. However, they also exhibit various errors when
              Vclk Clk Vss PULSE(0 1 0 1n 1n 10n 20n)
       M10 Voutn Clk Vss Vss NMOS W=Wn10 L=Ln10
                                                                          asked to generate the simpler comparator from Miyahara [32], as
       M11 Vdd N3 Clk Vdd PMOS W=Wp11 L=Lp11
       Clp Voutp Vss C1                                                   shown in Figure 2 (b). For Gemini-Pro (top in (b)), we note that the
       Cln Voutn Vss C1                                                   generated netlist has nodes (node_latchP and node_latchN) that
       Vclk Clk Vss PULSE(0 1 0 1n 1n 10n 20n)                            are not connected. On the other hand, ChatGPT Plus (bottom in
                                                                          (b)) misses creating intermediate nodes and merges them to output
                                                                          nodes creating incorrect circuit logic. We attribute some of these
Figure 3: Highlighting the limitations of utilizing multi-                errors to failure in reasoning and reduced confidence, leading to
modal LLMs for netlist generation. In red, we highlight the               hallucinations and incorrect connections. Overall, we note that
wrong connections and incorrectly identify transistors.                   LLMs are getting better at understanding analog circuits and can be
                                                                          utilized for simpler circuits; their utility through direct prompting
                                                                          for creating SAR ADCs remains limited.

3.1     Prompting LLMs                                                    3.2    Prompting Multimodal LLM
Synthesizing a SAR ADC from scratch is a formidable challenge             Recently, LLMs have improved on various image understanding
even for human experts, making end-to-end generation by an LLM            tasks and reasoning tasks [33]. [34] have explored the use of mul-
highly impractical. Instead, as part of this case study, we prompt sev-   timodal models for reasoning over simpler circuit images. To this
eral LLMs to generate netlists for simpler components - specifically      end, we conduct a small case study to study the capability of multi-
comparator - of the SAR ADC. We present qualitative results from          modal LLMs (specifically GPT-4o) to generate netlists from images
the LLM outputs in Figure 2, highlighting errors and hallucinations.      of a low-offset comparator circuit from [35]. We attempted direct
   First, we prompt GPT-4o [28] to generate a double-tail dynamic         prompting as well as detailed step-by-step prompting to guide the
comparator [29]. As shown in Figure 2 (a), there are multitudes of        generation of the netlist. We show the circuit and the best generated
errors in the created netlist. Some of them include: (1) The gates        netlist by GPT-4o in Figure 3.
of the input transistors are tied together at NODE1, completely              Even in this best generation, the multimodal LLM makes several
negating any differential sensing capability, (2) The differential        errors. While it correctly identifies the number of transistors, it in-
input signals (INP and INN) are incorrectly connected to the drain        correctly classifies them. It creates 3 PMOS and 8 NMOS transistors
terminals of M1 and M2, (3) This netlist contains its OUT at the gate     in the netlist; whereas the original circuit image has 7 PMOS and 4
of a transistor, (4) The gate of the "clocked" biasing transistor (M5)    NMOS transistors. Secondly, there are issues in the actual connec-
is permanently tied to GND. Under standard conditions, this NMOS          tions as well, specially for nodes M3 and M4 where the Vin+ and
transistor will never turn on. Inspection of the post-generation          Vin- are connected to the gates in the original circuit; while the mul-
rationale reveals a severe lack of analog design knowledge, leading       timodal model connects them to the drain. Overall, the multimodal
to hallucinations and incorrect assumptions, in turn causing the          model have good image detection capabilities to identify the num-
fundamental errors above. We observe similar behaviors with same-         ber of components and connections, but lack deeper recognition
sized LLMs from DeepSeek [30] and Gemini [31].                            and reasoning capabilities to make correct circuit connections.
                                                                                                                                   LLM
                                   Curation


Input Specs                                                                                             Simulation

                                       Wing 2: Template-Constrained                                     Integration and Testbench Creation
                                                                                                                                         Kochar et al.

Final                                                           Circuit
    3.3
Circuit    Prompting Fine-tuned models
                                                            Parameters




                                                                                   Aggregation
                                                                                   Information
   To overcome the issues of base multimodal LLMs, [34] propose
                                                            Anda Ranges
   fine-tuning recipe comprising a large dataset of simple schematic
   images and netlists. They fine-tune a lightweight YOLO vision
   model [36] specifically to detect non-standardized analog circuit
                                                                    External                Open-source          LLM-based
   symbols across varying image qualities. They pass the detected
                                                                   Optimizer
   components to an LLM to create the final netlist. We evaluate their
                                                                                         Scientific Papers    Summarization
   fine-tuned model + direct prompting of GPT-4o on 30 different




                                                                                  Retrieval-Augmented
                      Sizerrelated
   test images of circuits    LLM to SAR ADCs. Simultaneously, we
   also fine-tune a GPT-4o model on >700 datapoints from [37] and




                                                                                       Generation
   evaluate on this test set.
      Through our study, we conclude that both these fine-tuned mod-
   els fail to generate correct netlists reliably. We demonstrate an
   example of a failure case when generating a circuit image from [38]                   Text and Metric-
   in Figure 4, where we compare the original circuit (left) with the                    Based Retriever         Planner LLM
   model-created circuit rendered into an image (right). Firstly, the
   generated netlist completely removes one transistor M9. Further-
   more, the cross-coupled connections for M5-M6 and M2-M3 are
   incorrect. The connections for M7-M8 are also shorted which is not
   the case in the original circuit One of the major reasons we hypoth-
   esize for this poor performance is the distributional shift between
   the training and the testing data. These models have been trained                                            Grounded Expert
   on simpler circuits from textbooks [39, 40] with high-quality im-                        Input Specs
                                                                                                                Knowledge/Plan
   ages. When tested on complex circuits with varying image quality,
   the model fails to generalize. Largely, fine-tuned models also fail
                                                                           Figure 5: High-level illustration of stage 1 of our proposed
   to incorporate extra rounds of text-based feedback owing to their
                                                                           ATLAS involving information aggregation (top) from open-
   training procedure; thus, it’s difficult to correct the mistakes of
                                                                           source scientific papers and a RAG-based Planner (bottom)
   these models without external models.
                                                                           for generating grounded plans for SAR ADC creation.

   4      Proposed Methodology - ATLAS
   To circumvent the limitations of open-ended unconstrained gener-         4.1.1 Information Aggregation. In order to ground the LLM, we
   ation, we propose our multi-step LLM agentic framework ATLAS.            first need to aggregate information from the analog design experts
   Essentially, ATLAS enhances the reliability and reduces LLM hallu-       that we can share with the LLM. Since we can not access and share
   cinations by breaking down the complex analog design process into        proprietary company-specific information with LLMs, we rely on
   three smaller stages: (1) Grounding in Expert Knowledge, (2) Netlist     utilizing open-source data, specifically open-source scientific pa-
   Generation, and (3) Netlist Sizing and Optimization. For the scope       pers. We start with the open-source survey and database from [41],
   of this work, we do not consider layout, as all our experiments are      comprising a large database of papers that have created scientific
   schematic-based. For all the different agentic components we devel-      artifacts in the form of ADCs. This database has information about
   oped, a human expert tests them qualitatively to ensure reliability.     the paper titles and links, as well as circuit-specific details like the
   We provide an illustration of our agentic framework in Figure 1          technology node, signal-to-noise distortion ratio (SNDR), power,
   and provide a detailed overview below.                                   sampling frequency (𝑓𝑠 ), etc. Next, a human expert surveys and
                                                                            filters the papers and database entries related to SAR ADCs. Finally,
   4.1     Grounding in Expert Knowledge                                    an LLM surveys the filtered papers and creates a small summary
                                                                            of the major findings for the circuits developed from each paper.
   One of the major flaws and limitations of using LLMs for analog
                                                                            Overall, this aggregation of expert information serves as the main
   design is hallucinations. When the model is not as confident, it uses
                                                                            source of expert-grounded knowledge for the next steps in ATLAS.
   its best judgment and assumptions to fill the gaps. While this is not
   as big an issue for other tasks, a wrong assumption at any stage of      4.1.2 Retrieval-Augmented Generation. To utilize the aggregated
   circuit design is highly costly and can have ripple effects, rendering   information from the previous step, we utilize retrieval-augmented
   the entire circuit incorrect. We provided various illustrations of       generation (RAG) with LLMs. Specifically, based on the input de-
   such hallucinations in Figure 2 and 3.                                   scription and specifications from the user, a heuristic retriever is
       In order to reduce hallucinations, we propose to ground the LLM      used to match it to the best circuits from our database (based on
   with expert analog design knowledge - specifically, scientific papers    proximity of metrics). We then select the top 𝑘 circuits and pro-
   and findings. We provide an illustrative workflow of this stage in       vide its summary to the Planner LLM along with the target input
   Figure 5. The workflow for this stage comprises two main steps: (1)      specs and descriptions. The Planner LLM then formulates a high-
   Information Aggregation, and (2) Retrieval-Augmented Generation          level plan for creating the SAR ADC and its individual components,
   (RAG). We describe each of these steps in more detail below.             grounded in the expert knowledge of the retrieved scientific papers.
Towards Reliable AI-Assisted Analog Design



                                             Generator LLM                                                       Integrator LLM
                                                                                                                                    Bit Modifier
                                                                                                                                        LLM

                                                                     Rule-based
      Grounded Expert                                                Verification
                                                                                                                   Testbench
      Knowledge/Plan
                                               Wing 1: Grounded Zero-shot                Fallback                 Creator LLM
                                                                                                                                     Debugger
                                             Template             Selector LLM                                                         LLM
                                             Curation


         Input Specs                                                                                            Simulation

                                                Wing 2: Template-Constrained                                    Integration and Testbench Creation

Figure Final                                                       Circuit
       6: High-level illustration of stage 2 of our agentic framework ATLAS which coordinates the creation of the ADC netlist
based Circuit                                                    Parameters
      on the initial grounded expert knowledge and the user-specified    input specs.




                                                                                         Aggregation
                                                                                         Information
                                                                 And Ranges
This grounded expert knowledge/plan is passed to the next stage              same time, such unconstrained generation can amplify the possi-
for the actual netlist generation. We provide an illustration of the         bility of errors. We believe that this wing ofLLM-based
                                                                                                     Open-source              netlist generation is
generated grounded plan in Figure 8.                                        External
                                                                             futuristic and will improve netlist generation  as the LLMs’ inherent
                                                                            Optimizer              Scientific Papers Summarization
                                                                             analog circuit-specific capabilities improve. However, to reliably
                                                                             generate ADCs, we create a second fallback wing, which is triggered
                                                                                          Retrieval-Augmented
4.2                     Sizer LLM
        Netlist Generation                                                   if we detect issues in the netlist from this first wing. We describe
Based on the grounded expert knowledge and plan for the SAR ADC                                Generation
                                                                             this fallback generation method below.
generation from stage 1, the next and most important stage is to
create the netlist. At a high level, any netlist has several strongly in-     4.2.2 Template-constrained Netlist Generation. Unconstrained gen-
tertwined components of the comparator, capdac, and the SAR logic             eration through LLMs can lead to hallucinations and logical errors;
- and our proposed workflow creates and combines them accord-                 thus, we provide an Text   and Metric-
                                                                                                   alternate  way to generate ADCs via template-
ingly. Overall, we have a two-winged netlist generation workflow:                                 Based
                                                                              constrained generation.    ToRetriever         Planner
                                                                                                            this end, we first  curate LLM
                                                                                                                                       a variety of
(1) the first wing constructs the netlist through an iterative gen-           different templates for the components of the SAR ADC, includ-
eration loop constrained by the expert literature from stage 1 and            ing the StrongArm latch [32], the Miyahara comparator [42], the
a rule-based verification engine, and (2) the second wing utilizes            standard binary-weighted capacitive DAC array [43, 44], and the
template-constrained generation, where the LLM chooses and mod-               split-capacitor DAC array [45, 46]. Currently, we populate these
ifies one among the different templates based on the grounded                 templates using available open-source data and human effort; how-
expert data. We present the high-level illustrative overview of this          ever, they can be easily populated    with larger proprietary data as
                                                                                                              Grounded     Expert
stage in Figure 6 and provide a detailed description below.                   needed. For each template, apartKnowledge/Plan we utilize hu-
                                                                                                                   from  the netlist,
                                                                              man experts / expert LLMs to curate a textual summary and the
4.2.1 Grounded Zero-shot Netlist Generation. We highlighted some              pros/cons.
limitations of LLM-based netlist generation in Section 3. To counter             Next, we move to the Selector LLM. We provide the Selector
some of these limitations, we ground the LLM generations through              with the templates for each component along with the grounded
expert data and rule-based feedback mechanisms. Specifically, we              expert knowledge from Stage 1, and ask it to select the best template
prompt the Generator LLM with the grounded expert knowledge                   that would meet the input specs. The meta-information about the
from stage 1, along with input specs, and component-specific in-              templates proves crucial for the selection, especially for complex
formation. Based on this contextual information, the Generator is             circuits where it is difficult for the LLM to directly understand
tasked with generating a netlist for the specified component from             the code. Optionally, the LLM can also be prompted to update the
scratch. Since LLMs lack niche analog design expertise, we create a           netlist with minor modifications to the templates to cater to the
rule-based verification engine that can study a netlist and provide           input specs and grounded expert knowledge from stage 1. Overall,
feedback based on simple heuristics and rule violations. Some of              this wing can be highly effective with a wide range of templates,
these rules include parameter matching across connections and                 but only provides little flexibility to customize the circuit to user
singular-node warnings. The Generator then updates the netlist                inputs/needs.
based on the feedback provided from the rule-based verification
engine, and the loop continues for a fixed number of iterations.              4.2.3 Integration and Testbench Creation. Once the netlists for
   This wing of netlist generation is extremely liberal, as the LLM           each comparator are created (via the direct or template-constrained
can add custom components and write logic accordingly. At the                 wings), the final step remains to combine them and generate the
                                                                                                 Debugger
                            Template         Selector LLM                                          LLM
                            Curation


Input Specs                                                                 Simulation

                               Wing 2: Template-Constrained                 Integration and Testbench Creation                            Kochar et al.


      Final                                                   Circuit                           ENOB      SINAD      SFDR      THD       Power
      Circuit                                               Parameters
                                                            And Ranges               Target       7.5       45db     50db      -50db      8uW
                                                                                     Achieved    7.59     47.5db     55.6db   -51.5db     6uW
                                                              External         Table 1: Main results comparing ATLAS’s achieved specs
                                                              Optimizer        against the target specs for the low-power 8-bit SAR ADC on
                                                                               the Cadence GPDK-45nm technology node.
                        Sizer LLM

    Figure 7: High-level illustration of stage 3 of our agentic
    framework ATLAS - responsible for selecting and sizing the
    parameters of the final netlist.                                           multiplicity (𝑚), number of fingers (𝑛𝑓 ), as well as unit capacitance
                                                                               (𝑐𝑐) for capacitors.
                                                                                  Based on the selected parameters, the Sizer writes a full-loop of
    higher-level logic. Here, we prompt the Integrator LLM with the            optimization script, where it supplies these parameters and their
    high-level parameters and the meta-information about the input             expected ranges (from prior expert knowledge) to an external multi-
    and outputs of each component, as well as the original input specs         objective optimizer, which is then run across a wide range of itera-
    and the grounded expert knowledge. The Integrator is tasked to             tions. After the optimization run, the results and logs are presented
    create the higher-level SAR ADC netlist which connects each of             to the Sizer, which then updates the parameter set along with the
    these components, adds additional gates/switches if needed, and            range of search - an updated version of a previous work LEDRO
    provides the higher-level abstraction. This step is relatively easier      [17]. We conduct this iterative loop a few times and the final sized
    than direct netlist generation, as the LLM does not have to reason         netlist constitutes the final SAR ADC developed by the LLM.
    about the low-level SAR logic and transistor connections.
       Since the templates/generated netlists can be for different num-        5     Synthesis of 8-bit SAR ADC
    ber of bits relative to the input specs, the Bit-Modifier LLM updates      Here, we demonstrate the efficacy of ATLAS by developing a low-
    the netlist to meet the specs. Specifically, provided with the entire      power 8-bit SAR ADC end-to-end using our framework. First, we
    netlist and the target number of bits, the Modifier LLM updates the        provide the experimental setup and some details about the imple-
    netlist across the different components to meet the target specs.          mentation details. Later, we present our main simulated results of
       Next, we pass this netlist to the Testbench Creator LLM. The Test-      the synthesized SAR ADC from our framework.
    bench Creator reads the higher-level SAR ADC netlist and creates
    a testbench to simulate the ADC. Since unconstrained testbench             5.1     Experimental Setup
    creation can be noisy, we ground this LLM with a testbench tem-             Our major experiments are conducted on the Cadence GPDK-45nm
    plate, which the LLM modifies based on the generated SAR ADC                technology node, simulated through Cadence Spectre. To be fair
    and the input specs. Largely, the testbench utilizes an ideal DAC          with our studies of limitation analysis in Section 3, we utilize GPT-
    to convert the digital signals back to analog, and the evaluation          4o as the main LLM for our experiments. Our input specifications
    is measured using the reconstruction quality. Apart from this, a            comprise the number of input bits (# bits), sampling frequency (𝑓𝑠 ),
    human expert also rectifies the testbench to validate the correctness       Effective Number of Bits (ENOB), Signal-to-Noise and Distortion
    of the reported metrics.                                                   (SINAD), Spurious-Free Dynamic Range (SFDR), Total Harmonic
       Finally, we loop this testbench with a simulation engine to exe-         Distortion (THD), power, as well as an optional text description of
    cute the created netlist. If there are any errors/warnings as part of       the SAR ADC for human-in-the-loop guidance/steering. For power
    the simulation, this is passed to the Debugger LLM for modification         calculations, we average the DAC, comparator, and the SAR logic
    and correction of the netlist. This loop is run multiple times until        powers.
    the simulation succeeds to complete without any errors.                        For our retriever in stage 1, we utilize a simple k-Nearest Neigh-
                                                                                bors (k-NN) retrieval based on Euclidean distance in a min-max
    4.3    Netlist Sizing and Optimization                                      normalized feature space using 𝑘 = 5. This ensures that our se-
    The final component after netlist generation remains sizing the             lected papers for grounding the LLMs are similar to the target user
    different transistors and capacitors in the circuit. Various recent         specs. For our template-constrained netlist generation in stage 2,
    works [14–16, 19] have studied sizing in-depth with and without            we create templates for three components of the SAR ADC pipeline
    LLMs and can be readily plugged in for this component. In our              - specifically the comparator, the SAR logic, and the capacitor DAC
    work, we introduce this third stage of automated sizing using an            array (capdac). These components are populated with the open-
    LLM agent with an existing multi-objective optimizer, as illustrated        source and human expert curated templates as detailed in Sec-
    in Figure 7. Specifically, given the final netlist from Stage 2, the        tion 4.2.2. For our testbench template, we set VDD to 1 or 1.2 V
    Sizer LLM extracts the parameters that can be sized from the netlist        depending on specification. For the optimizer in stage 3, we use
    based on the chosen templates. These parameters have variable               multi-objective Bayesian optimization featuring Sobol-initialized
    sharing where similar transistors/capacitors are assigned the same          designs, independent Gaussian-process surrogates (BoTorch) [47],
    parameter variable. Some set of parameters usually extracted by             and qParEGO-style batch expected improvement under random
    the Sizer include transistor-level and switch-level length, width,          Chebyshev scalarizations with QMC [48].
Towards Reliable AI-Assisted Analog Design



      ### Grounded  ###Papers
                          Grounded Papers                                                                 ## Comparator Selection
      1. - 'A 12nW1. Always-On
                       - 'A 12nW Acoustic
                                   Always-OnSensing andSensing
                                              Acoustic  Object Recognition
                                                                and Object Recognition
      Microsystem     using Frequency-Domain
                    Microsystem                   Feature Extraction
                                    using Frequency-Domain    Featureand SVM and SVM
                                                                      Extraction                          "confidence": "high",
      Classification’
                    Classification’                                                                       "rationale": "The Miyahara Low-Noise Dynamic Comparator is well-
      2. 'A 3.2fJ/c.-s.
                    2. 'A0.35V 10b 100KS/s
                          3.2fJ/c.-s.        SAR100KS/s
                                      0.35V 10b  ADC in SAR
                                                        90nmADCCMOS’
                                                                  in 90nm CMOS’                           suited for the low-power, high-efficiency goals of the SAR ADC design.
                                                                                                          Its very low noise and high-speed performance align with the target
      ...         ...                                                                                     SNDR and SFDR specifications. The excellent kickback isolation
                                                                                                          supports the synchronous design requirement, and its power efficiency
      ### Recommended ArchitectureArchitecture
               ### Recommended     and Sub-Blocks
                                               and Sub-Blocks                                             matches the low-power constraint. Despite its complexity, the benefits
                                                                                                          in noise reduction and speed outweigh the drawbacks, making it the
      1. Overall Architecture:
                  1. Overall Architecture:                                                                best fit for the design plan's goals.”
       - A synchronous   SAR ADC architecture
                   - A synchronous               is chosen toismeet
                                      SAR ADC architecture           the low-
                                                                chosen   to meet the low-
      power and high-speed    requirements.
                  power and high-speed        This architecture
                                           requirements.        will leveragewill
                                                          This architecture   a leverage a                ...
      combination   of innovativeofDAC
                  combination           and comparator
                                    innovative           designs to optimize
                                               DAC and comparator      designs to optimize
      power efficiency
                  powerand   performance.
                         efficiency  and performance.                                                     ## Switching Logic
      2. Sampler:2. Sampler:                                                                              "confidence": "high",
        - Design Choice:  UseChoice:
                   - Design   a low-leakage   sample-and-hold
                                      Use a low-leakage            circuit with acircuit with a
                                                            sample-and-hold                               "rationale": "The Split-Capacitor DAC Switching option aligns well with
      charge pump   to ensure
                  charge   pumpeffective sampling
                                 to ensure          at sampling
                                            effective  low voltages,   inspired
                                                                  at low         by inspired by
                                                                          voltages,                       the design plan's emphasis on low-power and compact size, as it
      the leakagethe
                  reduction
                      leakagetechniques   from matched
                               reduction techniques     frompapers.
                                                              matched papers.                             significantly reduces power consumption and die area. It also supports
        - Responsibility: Capture andCapture
                   - Responsibility:   hold theand
                                                input
                                                    holdsignal for conversion.
                                                           the input  signal for conversion.              the synchronous design goal by enabling faster settling times, which is
                                                                                                          crucial for high-speed operation. Although it requires careful layout to
      3. DAC:     3. DAC:                                                                                 mitigate parasitic effects, its benefits in power and area efficiency make
       - Design Choice:    Implement
                    - Design   Choice: aImplement
                                          split-capacitor   DAC with a minimized
                                                      a split-capacitor    DAC with a minimized           it the best fit for the specified low-power synchronous SAR ADC design.”
      capacitor size   to reduce
                  capacitor    sizepower   consumption
                                     to reduce            and improveand
                                                 power consumption       linearity,
                                                                             improveas linearity, as
      seen in the re-switching   and arbitraryand
                  seen in the re-switching        weight capacitor
                                                    arbitrary      array
                                                               weight      techniques.
                                                                      capacitor   array techniques.       ...
       - Responsibility:  Convert theConvert
                    - Responsibility:    digital output of theoutput
                                                  the digital   SAR logic
                                                                     of theback
                                                                             SARtologic
                                                                                    an back to an
      analog signal  for comparison.
                  analog    signal for comparison.
      4. Comparator:
                  4. Comparator:                                                              Figure 9: Illustrating the choices and the underlying rationale
        - Design Choice:  Utilize
                    - Design      a dynamic
                              Choice:  Utilizecomparator    with low-power
                                              a dynamic comparator       with low-power       for template selection by our Selection LLM for the genera-
      consumption,     possibly incorporating
                  consumption,                 redundancyredundancy
                                    possibly incorporating   to improve accuracy
                                                                          to improve accuracy tion of the low-power 8-bit SAR ADC.
      and reduce and
                  power,   as suggested   by the use of low-power   comparators   in
                       reduce power, as suggested by the use of low-power comparators in
      matched designs.
                  matched designs.
        - Responsibility: Compare the
                    - Responsibility:   DAC output
                                      Compare         with output
                                                 the DAC   the sampled   input
                                                                   with the sampled input
      signal and provide  a decision
                  signal and   providefor the SAR logic.
                                       a decision  for the SAR logic.
      ...         ...
                                                                                                                         ENOB        SINAD        SFDR         THD         Power
                                                                                                           Target          7.5        45dB         50dB        -50dB        8𝜇W
Figure 8: Illustration of the grounded papers and the detailed
plan generated by the Planner LLM for the 8-bit SAR ADC.                                                   Achieved        7.82      48.8dB       56.5dB      -52.5dB      5.7𝜇W
We highlight some of the key choices it recommends.                                                    Table 2: Results highlighting the generalization across tech-
                                                                                                       nology nodes by comparing the achieved specs against the
                                                                                                       target specs for the 8-bit SAR ADC on a different technology
5.2         SAR ADC Synthesis Results                                                                  node of TSMC-65nm.
For our primary demonstration, we consider developing a low-
power 8-bit SAR ADC with human-expert provided target specifi-
cations (specs), as shown in Table 1 (first row). We set the sampling
frequency (𝑓𝑠 ) to 3.33 MHz and clock frequency (𝑓𝑐𝑙𝑘 ) as 20 MHz.
We provide the input text description simply as “synchronous low
power". We present the achieved metrics of our generated 8-bit SAR                                     6.1      Technology Nodes
ADC against the target user specs in Table 1. As noted, the ATLAS’s                                    Here, we show the generalization of ATLAS’s SAR ADC across tech-
generated SAR ADC meets all the user specifications comfortably.                                       nology nodes - specifically from GPDK-45nm to TSMC-65nm node.
   To make a deeper dive into our multi-agent framework’s decision-                                    Owing to privacy and copyright concerns with sharing foundry’s
making, we study its intermediate outputs. In Figure 8, we show                                        technology node files, directly running our framework to generate
some of the retrieved grounded papers and part of the detailed                                         the SAR ADC is unfeasible (although we believe doing so will fur-
grounded plan generated by the Planner in stage 1, highlighting                                        ther improve the ADC). Instead, the LLM-generated 8-bit SAR ADC
some of its design choices. The grounded zero-shot netlist gen-                                        was migrated from Cadence GPDK-45nm to TSMC-65nm using
eration had some errors and didn’t succeed, but the fallback to                                        custom scripts developed to automatically map and substitute the
template-constrained netlist succeeded. Some of the choices are                                        technology primitives. We utilize a local optimizer for sizing instead
well-grounded and we illustrate the Selector’s rationale in Figure 9.                                  of our LLM framework to ensure no foundry data leakage. Despite
                                                                                                       no technology node-specific optimizations, the generated SAR ADC
6     Generalization Analysis                                                                          performs well out-of-the-box with the main metrics compared with
To demonstrate the generalizability of ATLAS to generate broader                                       the target user specs provided in Table 2. Overall, this demonstrates
range of SAR ADCs, we conduct various additional analytical ex-                                        the transferability and generalization of ATLAS across technology
periments - which we detail more in this section.                                                      nodes.
                                                                                                                                                         Kochar et al.



                   ENOB        SINAD      SFDR            THD      Power     the Bit Modifier Agent of ATLAS to modify the template-based
                                                                             circuit (built for a specific number of bits) to match the target user
     Target         3.7        24dB       31.5dB          -28dB    25𝜇W
                                                                             specs. For this analysis, we utilize Gemini 3.1 as the LLM for the
     Achieved      3.86        25dB       33.6dB      -29.8dB     21.1𝜇W     Bit Modifier. To test this, we use the same user specifications as the
Table 3: Results highlighting the bit modification provided                  main synthesis experiment for the 8-bit SAR ADC, but only change
input specifications by comparing the achieved specs against                 the number of bits to 10 and set the sampling frequency (𝑓𝑠 ) as 2.5
the target specs for an asynchronous                                         MHz. Noting here that the templates were originally created specif-
                                  Vdd 4-bit SAR ADC design.
                                                                             ically for 8 bits, and their performance when extrapolated to 10 bits
                                                M1                           remains unknown/sub-optimal. We report the results for the 10-bit
                                                                             SAR ADC created by ATLAS using the Bit Modifier’s capability in
                   ENOB           M2
                               SINAD      SFDR M3THD               Power     Table 4. We observe that the ADC fails to meet the target specs, but
                                                      CLK                    achieves close to 9 ENOB. Upon human expert inspection, we con-
     Target         9.5         58dB       68dB           -65dB    7.5𝜇w
                                  M5                         M4              clude that the Bit Modifier has strong pattern-matching reasoning
     Achieved      8.93        55.5dB     62.9dB      -59.9dB      6.1𝜇W
                                                                             to extrapolate the circuit, as we show an illustration of the correct
Table 4: Results highlighting the bit modification capability                extension of the capdac array in Figure 10.
of our agentic frameworkVin               Vip to modify the
                           ATLAS when asked
8-bit SAR ADC for 10 bits.
                                                                             7    Conclusion and Future Work
                                                                             In this paper, we propose a template-constrained LLM agentic
                                                                             framework ATLAS that successfully bridges the gap between un-
       C      C    2C     4C    8C          C        2C     4C    8C
                                                                             constrained text generation and the rigorous physical demands
                                                                             of analog EDA. By grounding the LLM’s generative search space
                                        (16/15)C
                                                                             in expert-defined architectural priors, our framework serves as a
                                                                             proof-of-concept for the end-to-end synthesis of functional SAR
                                                                             ADCs across multiple specifications and technology nodes. While
 C     C      2C   4C     8C    16C         C        2C     4C    8C   16C
                                                                             the current scope of this work validates the methodology on basic
                                                                             SAR ADC topologies, it establishes a reliable, non-hallucinating par-
                                        (32/31)C                             adigm for integrating LLMs into EDA workflows. Future work can
                                                                             focus on expanding the granularity and diversity of the template
Figure 10: Illustration highlighting the bit-modification ca-                libraries, as well as leveraging the evolving reasoning capabilities
pability of our framework where ATLAS extended a 8-bit                       of newer LLMs, to tackle the continuous-domain optimization of
capdac array (top) to 10 bits (bottom).                                      much more complex mixed-signal systems. Ultimately, we believe
                                                                             this structured, prior-grounded approach opens a highly promising
                                                                             avenue for reliable AI-assisted analog circuit design.
6.2     Input Specifications
Next, we conduct experiments to evaluate the adaptability of AT-
LAS to build customized SAR ADCs for varying user input specifica-
                                                                             References
                                                                              [1] L. Chen, Y. Chen, Z. Chu, W. Fang, T.-Y. Ho, R. Huang, Y. Huang, S. Khan, M. Li,
tions. Specifically, we update the new user target specs and provide              X. Li et al., “The dawn of ai-native eda: Opportunities and challenges of large
the metrics in Table 3 (top row). We set the sampling frequency                   circuit models,” arXiv preprint arXiv:2403.07257, 2024.
(𝑓𝑠 ) to 20 MHz, choose asynchronous design, and the number of                [2] I. Guven, M. Parlak, D. Lederer, and C. De Vleeschouwer, “Ai-driven integrated
                                                                                  circuit design: A survey of techniques, challenges, and opportunities,” IEEE Access,
bits to 4. For the 4-bit SAR ADC, the Selector LLM chose simpler                  2025.
templates compared to the previous 8-bit design. It selected a stan-          [3] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan, “Swe-
                                                                                  bench: Can language models resolve real-world github issues?” arXiv preprint
dard bottom-plate capdac instead of a split-capacitor array, as the               arXiv:2310.06770, 2023.
lower resolution does not require capacitance scaling. Additionally,          [4] M. Liu, T.-D. Ene, R. Kirby, C. Cheng, N. Pinckney, R. Liang, J. Alben, H. Anand,
it replaced the low-noise Miyahara comparator with a standard                     S. Banerjee, I. Bayraktaroglu et al., “Chipnemo: Domain-adapted llms for chip
                                                                                  design,” arXiv preprint arXiv:2311.00176, 2023.
StrongArm latch, since kickback noise is far less critical at 4 bits          [5] D. V. Kochar, N. Pinckney, G.-T. Liu, C.-T. Ho, C. Deng, H. Ren, and B. Khailany,
and gives higher speed. We present the performance metrics of the                 “Grpo with state mutations: Improving llm-based hardware test plan generation,”
ADC developed by our framework in Table 3 (bottom row). The                       arXiv preprint arXiv:2601.07593, 2026.
                                                                              [6] P. Mandal and V. Visvanathan, “Cmos op-amp sizing using a geometric program-
results show how it meets the specs. In fact, ATLAS removed a                     ming formulation,” IEEE Transactions on Computer-Aided Design of Integrated
transistor connected in parallel in the bootstrap switch in the tem-              circuits and systems, vol. 20, no. 1, pp. 22–38, 2002.
                                                                              [7] S. Zhang, F. Yang, D. Zhou, and X. Zeng, “An efficient asynchronous batch
plate with the rationale of reducing THD and that indeed improved                 bayesian optimization approach for analog circuit synthesis,” in 2020 57th
performance. Overall, this analysis provides a proof-of-concept for               ACM/IEEE design automation conference (DAC). IEEE, 2020, pp. 1–6.
the generalizability of ATLAS across different input specifications.          [8] K. Settaluri, A. Haj-Ali, Q. Huang, K. Hakhamaneshi, and B. Nikolic, “Au-
                                                                                  tockt: Deep reinforcement learning of analog circuit designs,” arXiv preprint
                                                                                  arXiv:2001.01808, 2020.
6.3     Bit Modification                                                      [9] H. Wang, K. Wang, J. Yang, L. Shen, N. Sun, H.-S. Lee, and S. Han, “Gcn-rl
                                                                                  circuit designer: Transferable transistor sizing with graph neural networks and
In this analysis, we study the capability of the framework to adapt               reinforcement learning,” in 2020 57th ACM/IEEE Design Automation Conference
its circuit for varying number of bits. Specifically, this is a test of           (DAC). IEEE, 2020, pp. 1–6.
Towards Reliable AI-Assisted Analog Design


[10] M. Liu, X. Tang, K. Zhu, H. Chen, N. Sun, and D. Z. Pan, “Opensar: An open                [35] Y. Sachdeva, N. Nehra, S. Bansal, and Garima, “Review of dynamic comparators
     source automated end-to-end sar adc compiler,” in 2021 IEEE/ACM International                  for adcs,” in 2021 Second International Conference on Electronics and Sustainable
     Conference On Computer Aided Design (ICCAD). IEEE, 2021, pp. 1–9.                              Communication Systems (ICESC), 2021, pp. 83–90.
[11] ——, “1-and 80-ms/s sar adcs in 40-nm cmos with end-to-end compilation,” IEEE              [36] G. Jocher, A. Chaurasia, and J. Qiu, “Ultralytics yolo,” 2023, computer software.
     Solid-State Circuits Letters, vol. 5, pp. 292–295, 2022.                                       [Online]. Available: https://github.com/ultralytics/ultralytics
[12] M. Ding, P. Harpe, G. Chen, B. Busze, Y.-H. Liu, C. Bachmann, K. Philips, and             [37] Z. Tao, Y. Shi, Y. Huo, R. Ye, Z. Li, L. Huang, C. Wu, N. Bai, Z. Yu, T.-J. Lin
     A. Van Roermund, “A hybrid design automation tool for sar adcs in iot,” IEEE                   et al., “Amsnet: Netlist dataset for ams circuits,” in 2024 IEEE LLM Aided Design
     Transactions on Very Large Scale Integration (VLSI) Systems, vol. 26, no. 12, pp.              Workshop (LAD). IEEE, 2024, pp. 1–5.
     2853–2862, 2018.                                                                          [38] N. A. Ansari, P. Jaiswal, M. Tyagi, and P. Mittal, “Design and comparative analysis
[13] M.-J. Seo, Y.-J. Roh, D.-J. Chang, W. Kim, Y.-D. Kim, and S.-T. Ryu, “A reusable               of dynamic comparators for sar adc,” in Emerging Electronics and Automation:
     code-based sar adc design with cdac compiler and synthesizable analog building                 Select Proceedings of E2A 2021. Springer, 2022, pp. 391–401.
     blocks,” IEEE Transactions on circuits and systems II: Express Briefs, vol. 65, no. 12,   [39] B. Razavi, Design of Analog CMOS Integrated Circuits. USA: McGraw-Hill, Inc.,
     pp. 1904–1908, 2018.                                                                           2000.
[14] J. Bao, J. Zhang, Z. Huang, Z. Bi, X. Feng, X. Zeng, and Y. Lu, “Multiagent based         [40] A. S. Sedra and K. C. Smith, “Microelectronic circuits pp. 263-267,” 1987.
     reinforcement learning (ma-rl): An automated designer for complex analog                  [41] B. Murmann, “ADC Performance Survey 1997-2026,” [Online]. Available: https:
     circuits,” IEEE Transactions on Computer-Aided Design of Integrated Circuits and               //github.com/bmurmann/ADC-survey.
     Systems, vol. 43, no. 12, pp. 4398–4411, 2024.                                            [42] M. Miyahara, Y. Asada, D. Paik, and A. Matsuzawa, “A low-noise self-calibrating
[15] Y. Hao, K. Li, M. Gandara, S. Li, and B. Liu, “A global-local optimization approach            dynamic comparator for high-speed adcs,” in 2008 IEEE Asian Solid-State Circuits
     for asynchronous sar adc design,” arXiv preprint arXiv:2507.19541, 2025.                       Conference. IEEE, 2008, pp. 269–272.
[16] Z. Li, Z. Tao, Y. Zhou, Y. Shi, Z. Yu, T.-J. Lin, and L. He, “Automated sar adc sizing    [43] J. L. McCreary and P. R. Gray, “All-mos charge redistribution analog-to-digital
     using analytical equations,” in 2025 International Symposium of Electronics Design             conversion techniques. i,” IEEE Journal of Solid-State Circuits, vol. 10, no. 6, pp.
     Automation (ISEDA). IEEE, 2025, pp. 214–220.                                                   371–379, 1975.
[17] D. V. Kochar, H. Wang, A. P. Chandrakasan, and X. Zhang, “Ledro: Llm-enhanced             [44] M. Aldacher, “Analog design of asynchronous sar adc,” https://github.com/
     design space reduction and optimization for analog circuits,” in 2025 IEEE Inter-              muhammadaldacher/Analog-Design-of-Asynchronous-SAR-ADC, 2020.
     national Conference on LLM-Aided Design (ICLAD). IEEE, 2025, pp. 141–148.                 [45] Y. Yee, L. Terman, and L. Heller, “A two-stage weighted capacitor network for
[18] S. Poddar, C.-T. Ho, Z. Wei, W. Cao, H. Ren, and D. Z. Pan, “Heart: A hierarchical             d/aa/d conversion,” IEEE Journal of Solid-State Circuits, vol. 14, no. 4, pp. 778–781,
     circuit reasoning tree-based agentic framework for ams design optimization,”                   2003.
     arXiv preprint arXiv:2511.19669, 2025.                                                    [46] M. Ashok, E. V. Levine, and A. P. Chandrakasan, “Randomized switching sar
[19] C. Liu and D. Chitnis, “Eesizer: Llm-based ai agent for sizing of analog and mixed             (rs-sar) adc for power and em side-channel security,” IEEE Solid-State Circuits
     signal circuit,” IEEE Transactions on Circuits and Systems I: Regular Papers, 2025.            Letters, vol. 5, pp. 247–250, 2022.
[20] C.-C. Chang, Y. Shen, S. Fan, J. Li, S. Zhang, N. Cao, Y. Chen, and X. Zhang,             [47] M. Balandat, B. Karrer, D. Jiang, S. Daulton, B. Letham, A. G. Wilson, and E. Bak-
     “Lamagic: Language-model-based topology generation for analog integrated                       shy, “Botorch: A framework for efficient monte-carlo bayesian optimization,”
     circuits,” arXiv preprint arXiv:2407.18269, 2024.                                              Advances in neural information processing systems, vol. 33, pp. 21 524–21 538,
[21] J. Shen, Z. Chen, J. Zhuang, J. Huang, F. Yang, L. Shang, Z. Bi, C. Yan, D. Zhou, and          2020.
     X. Zeng, “Atelier: An automated analog circuit design framework via multiple              [48] S. Daulton, M. Balandat, and E. Bakshy, “Differentiable expected hypervolume
     large language model-based agents,” IEEE Transactions on Computer-Aided Design                 improvement for parallel multi-objective bayesian optimization,” Advances in
     of Integrated Circuits and Systems, 2025.                                                      neural information processing systems, vol. 33, pp. 9851–9864, 2020.
[22] H. Zhang, S. Sun, Y. Lin, R. Wang, and J. Bian, “Analogxpert: Automating ana-
     log topology synthesis by incorporating circuit design expertise into large lan-
     guage models,” in 2025 International Symposium of Electronics Design Automation
     (ISEDA). IEEE, 2025, pp. 772–777.
[23] Z. Chen, J. Huang, Y. Liu, F. Yang, L. Shang, D. Zhou, and X. Zeng, “Artisan:
     Automated operational amplifier design via domain-specific large language
     model,” in Proceedings of the 61st ACM/IEEE Design Automation Conference, 2024,
     pp. 1–6.
[24] Z. Chen, J. Zhuang, J. Shen, X. Ke, X. Yang, M. Zhou, Z. Du, X. Yan, Z. Wu, Z. Xu
     et al., “Analogseeker: An open-source foundation language model for analog
     circuit design,” arXiv preprint arXiv:2508.10409, 2025.
[25] Y. Lai, S. Lee, G. Chen, S. Poddar, M. Hu, D. Z. Pan, and P. Luo, “Analogcoder:
     Analog circuit design via training-free code generation,” in Proceedings of the
     AAAI Conference on Artificial Intelligence, vol. 39, no. 1, 2025, pp. 379–387.
[26] C. Liu, W. Chen, A. Peng, Y. Du, L. Du, and J. Yang, “Ampagent: An llm-based
     multi-agent system for multi-stage amplifier schematic design from literature
     for process and performance porting,” arXiv preprint arXiv:2409.14739, 2024.
[27] C. Liu, Y. Liu, Y. Du, and L. Du, “Ladac: Large language model-driven auto-
     designer for analog circuits,” Authorea Preprints, 2024.
[28] A. Hurst, A. Lerer, A. P. Goucher, A. Perelman, A. Ramesh, A. Clark, A. Ostrow,
     A. Welihinda, A. Hayes, A. Radford et al., “Gpt-4o system card,” arXiv preprint
     arXiv:2410.21276, 2024.
[29] D. Schinkel, E. Mensink, E. Klumperink, E. Van Tuijl, and B. Nauta, “A double-tail
     latch-type voltage sense amplifier with 18ps setup+ hold time,” in 2007 IEEE
     international solid-state circuits conference. Digest of technical papers. IEEE, 2007,
     pp. 314–605.
[30] A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang,
     C. Ruan et al., “Deepseek-v3 technical report,” arXiv preprint arXiv:2412.19437,
     2024.
[31] Google DeepMind, “Gemini 3 pro model card,” https://storage.googleapis.com/
     deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf, 2026, accessed:
     2026-04-12.
[32] T. Kobayashi, K. Nogami, T. Shirotori, Y. Fujimoto, and O. Watanabe, “A current-
     mode latch sense amplifier and a static power saving input buffer for low-power
     architecture,” in 1992 symposium on VLSI circuits digest of technical papers. IEEE,
     1992, pp. 28–29.
[33] S. Yin, C. Fu, S. Zhao, K. Li, X. Sun, T. Xu, and E. Chen, “A survey on multimodal
     large language models,” National Science Review, vol. 11, no. 12, p. nwae403, 2024.
[34] J. Bhandari, V. Bhat, Y. He, H. Rahmani, S. Garg, and R. Karri, “Masala-chai:
     A large-scale spice netlist dataset for analog circuits by harnessing ai,” 2025.
     [Online]. Available: https://arxiv.org/abs/2411.14299
