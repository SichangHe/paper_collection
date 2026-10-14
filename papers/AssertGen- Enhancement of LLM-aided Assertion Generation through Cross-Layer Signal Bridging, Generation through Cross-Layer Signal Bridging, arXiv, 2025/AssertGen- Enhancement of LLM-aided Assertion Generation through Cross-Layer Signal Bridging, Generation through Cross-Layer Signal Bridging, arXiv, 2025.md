                                           AssertGen: Enhancement of LLM-aided Assertion
                                           Generation through Cross-Layer Signal Bridging
                                                       Hongqin Lyu1,2 , Yonghao Wang1,2 , Yunlin Du5 , Mingyu Shi4 , Zhiteng Chao1 , Wenxing Li1 ,
                                                                               Tiancheng Wang1,2,3† and Huawei Li1,2,3†
                                                              1
                                                               State Key Lab of Processors, Institute of Computing Technology, CAS, Beijing, China
                                                                            2
                                                                              University of Chinese Academy of Sciences, Beijing, China
                                                                                             3
                                                                                               CASTEST, Beijing, China
                                                                         4
                                                                           School of Integrated Circuits, Nanjing University, Suzhou, China
                                                           5
                                                             School of Information and Physical Sciences, University of Newcastle, Newcastle, Australia
arXiv:2509.23674v1 [cs.AR] 28 Sep 2025




                                                                                                                                Bug
                                            Abstract—Assertion-based verification (ABV) serves as a cru-                        Bug hunted by assertion
                                         cial technique for ensuring that register-transfer level (RTL)                         Antecedent of assertion
                                                                                                                                Consequent of assertion
                                         designs adhere to their specifications. While Large Language                            SPEC                                              Top Module
                                         Model (LLM) aided assertion generation approaches have re-                              Top Module                                               Sub Module
                                                                                                                      Chunk 1      Signal A
                                         cently achieved remarkable progress, existing methods are still                           Signal B
                                                                                                                                      …                   Assertion(A,D)
                                                                                                                                                                           input   …                           …   output

                                         unable to effectively identify the relationship between design               Chunk i
                                                                                                                                 Sub Module
                                                                                                                                   Signal C                                            Cross-layer assertion

                                                                                                                                                                             clk
                                         specifications and RTL designs, which leads to the insufficiency                          Signal D
                                                                                                                                      …
                                         of the generated assertions. To address this issue, we propose
                                         AssertGen, an assertion generation framework that automati-               Fig. 1: Example: cross-layer assertion generation process and
                                         cally generates SystemVerilog assertions (SVA). AssertGen first           its role in bug detection
                                         extracts verification objectives from specifications using a chain-
                                         of-thought (CoT) reasoning strategy, then bridges corresponding           verification tasks, such as stimuli generation [2], [3], security
                                         signals between these objectives and the RTL code to construct
                                         a cross-layer signal chain, and finally generates SVAs based              verification [4], [5], and formal verification [6], [7]. The power
                                         on the LLM. Experimental results demonstrate that AssertGen               of LLM has also promoted research in assertion generation of
                                         outperforms the existing state-of-the-art methods across several          hardware designs.
                                         key metrics, such as pass rate of formal property verification
                                                                                                                      Existing LLM-based assertion generation methods can be
                                         (FPV), cone of influence (COI), proof core and mutation testing
                                         coverage.                                                                 categorized into two categories according to their application
                                            Index Terms—Functional Verification, Assertion Based Verifi-           stage: RTL-stage generation and Pre-RTL-stage generation.
                                         cation, Assertion Generation, Large Language Model                        The RTL-stage assertion generation focuses on guiding LLM
                                                                                                                   to analyze RTL codes and infer logical relations among signals
                                                                  I. I NTRODUCTION                                 to construct assertions [8]. However, since RTL designs may
                                            Functional verification plays a key role in the integrated             contain semantic errors or be incomplete, assertions generated
                                         circuit (IC) design process, which is essential to maintain               from RTL designs, may inherit possible errors inside the code,
                                         the correctness and reliability of the design. Assertion-based            potentially leading to mismatches with design specifications
                                         verification (ABV) has emerged as an effective verification               [9]. Pre-RTL-stage assertion generation focuses on the natural
                                         technique at register-transfer level (RTL), and been widely               language specifications, aligning specifications with Verilog
                                         adopted by IC design projects. It has been reported that [1],             codes through semantic mapping to generate assertions [10].
                                         more than 70% of ASIC design projects adopt ABV and the                   Instead of relying solely on RTL codes, this method leverages
                                         adoption percentage is still growing year by year, because                information of design specifications to reducing the impact of
                                         ABV improves observability and controllability of designs,                deficiencies of RTL designs on assertion quality.
                                         and accordingly, allows for dramatic reduction in verification              However, current methods that generate assertions only for
                                         time and debug efforts.                                                   the top-level module will lead to inaccurate bug detection
                                            However, assertion generation typically relies on manual               when a problem occurs in a sub-level module. The root
                                         efforts, which is time-consuming, error-prone, and susceptible            cause of this inadequacy lies in three gaps between the
                                         to omissions. With the growing scale and complexity of                    design specifications and the RTL code. Firstly, functional
                                         modern IC designs, the demand for automatic and high-                     descriptions in specifications are often scattered across multi
                                         quality assertion generation is becoming increasingly urgent.             semantic levels and textual chunks, creating a structural gap
                                         Fortunately, recent advances in Large language model (LLM)                that makes signal behavior extraction an inherent cross-layer
                                         have facilitated effective applications in various hardware               challenge. Secondly, a semantic gap exists between behavioral
                                           † Corresponding author.
                                                                                                                   descriptions and verification objectives [11], which is mainly
                                         This paper has been accepted by the 34th IEEE Asian Test Symposium (ATS   due to the fragmentation of information. Specifically, the
                                         2025), December 16–19, 2025, Tokyo, Japan.                                composition logic of a complete and rigorous verification
objectives is often scattered in multiple text chunks, which                       III. A SSERT G EN F RAMEWORK
spans different semantic levels. Lastly, there also have a          A. Overview
link gap from verification objectives to corresponding RTL
code segments, which makes it challenging to fully connect            To enhance the efficiency of assertion generation, we pro-
verification objectives with related code segments.                 pose AssertGen, which aims to automatically generate correct
   To address these challenges, we propose a Pre-RTL frame-         assertions by cross-level information bridging and behavioral
work—AssertGen—to bridge the above three gaps: incremen-            modeling, as shown in Fig. 2. The framework achieves its
tal context extraction strategy for the structural gap, chain-of-   functionality through a four-step process, detailed as follows:
thought (CoT) prompting strategy for the semantic gap, and            1) Contextual Entity Extraction: An incremental strategy
cross-layer signal chain strategy for the link gap. Fig. 1 shows           extracts signal behaviors and related entities from the
how AssertGen generates cross-layer assertions by combining                specification to support verification objectives genera-
signals (e.g., Signal A and Signal D) described across different           tion.
layers in the specification.                                          2) Verification Objective Generation: By leveraging a
   The main contributions of this work are as follows:                     prompt mechanism with CoT reasoning, verification
   1) Cross-layer signal chains are used to connect speci-                 objectives are generated with cross-signal behavior.
       fications and RTL designs, accurately mapping signal           3) Bridging Verification Objectives to Verilog Segments:
       behavior to code and extracting detailed information to             A hierarchical mapping strategy using cross-layer signal
       generate assertions.                                                chains is proposed to link verification objectives to their
   2) To address the problem of scattered signal behavior                  corresponding Verilog code.
       descriptions and complex semantics in specifications, we       4) SVA Generation: Structured prompts are designed to
       propose an incremental context extraction method com-               alleviate inconsistent formatting in content generation
       bined with CoT prompt to generate more comprehensive                by LLMs.
       verification objectives.                                     B. Step 1: Contextual Entity Extraction
   3) We evaluate AssertGen on five open-source benchmark
       designs. Experimental results show that AssertGen sur-          In IC designs, signal behaviors often emerge from interac-
       passes current state-of-the-art methods in formal prop-      tions among multiple signals, making their descriptions implic-
       erty verification pass rate, COI, proof-core coverage, and   itly embedded in cross-signal contexts. To extract these seman-
       bug detection rate of mutation testing.                      tic relationships, we propose to extract contextual entities from
                                                                    the specification, where entities refer to key elements such as
                     II. R ELATED WORK                              signals, bits, or registers that convey behavioral meaning in
                                                                    the specification.
A. Assertion generation based on NLP
                                                                       To effectively extract descriptions containing entities, we
   Early template-based assertion generation methods relied         introduce a retrieval-augmented generation (RAG) mechanism.
on static analysis of specifications, but their effectiveness was   The core principle of RAG is to select the most relevant
limited without HDL code [12]. To overcome this limitation,         subset from a preprocessed collection of specification chunks
subsequent work focused on extracting properties directly           (while chunks are a series of small, more easily retrievable text
from the RTL design itself [13]. However, this method was           blocks) based on relevance computations with respect to a user
unreliable when the RTL design is flawed. To address this           query q ∈ Q. The query follows a uniform template “What
issue, a later approach was proposed to generate assertions         is the description of {signal}?,” where the initial signal used
directly from the specification using subtree analysis, ensuring    in the template to start Step 1 is arbitrarily selected from the
the assertions to reflect the intended design requirements [14].    specification at the framework’s first invocation.
                                                                       Although RAG effectively yields signal-relevant descrip-
B. Assertion generation based on LLM                                tions, cross-signal information extraction remains challenging
   Leveraging LLMs is a promising direction for assertion           due to vague semantic cues. Our three-stage prompt strategy
generation, as their strong semantic comprehension addresses        addresses this by first extracting entities that directly describe
the shortcomings of traditional NLP methods.                        the target signal Etarget , and then identifying all associated ex-
   Building on their known natural language processing capa-        ternal entitiesEcontext . To isolate purely contextual information,
bilities, researchers are increasingly applying LLMs to hard-       we then remove any entities that overlap with the target set,
ware assertion generation. Early work first explored generating     yielding Efinal = Econtext − (Etarget ∩ Econtext ). This method
hardware security assertions [15]. Subsequent research has          yields a set of highly-relevant contextual ”probes,” which serve
developed frameworks for dynamic simulation [8] and used            as the basis for subsequent cross-layer information retrieval
simulation log feedback loops for iterative refinement [16]. To     and for integrating related descriptions scattered across differ-
manage hardware’s inherent complexity, strategies have been         ent text chunks. Figure 3 shows the LLM-generated response
proposed such as assertion mining based on deep-level design        for the Control Register of an I2 C design [18].
analysis [17] and decomposing complex tasks into simpler               After initializing the external entity set Efinal from the first
subtasks [10] to improve assertion quality and quantity.            query, the system iteratively removes each entity ek ∈ Efinal
                                                             Step1 Contextual Entity Extraction                                        Step2 Verification Objective Generation
                                                                                         Entity Description Storage
                                                            Signal

                                                       query                                                                                                                                 Verification objective 1

                                                                                                LLM①                                                        LLM②
                                                                                                                       Entity                                                                Verification objective 2
                              SPEC                                                                                                             Extract verification
                                             chunks          RAG                        Signal related entities        Description
                                                                                                                                               objectives from entity




                                                                                                                                                                                                        …
                                                                                        extraction                     Hub                     description hub
                                                                                                                                                                                             Verification objective m
                                                      query 𝑞𝑘
                                                                  Entity 1   Entity 2    …    Entity n

                              Verilog Files
                                                                     Step4 SVA Generation                              Step3 Bridging Signal Verification Objectives to Verilog Segments

                                                                                                                                         Signal Chain
                                                       Assertion 1
                                                                                                                                sig1            sig2               sigk
                                                                                                                                                             …
                                                                                                                                                                                                LLM③
                                                                                             LLM④
                   Model                               Assertion 2                                                                                                                 ⚫ Signal Chain Extraction
                   checker                                                                                                                     Bridging
                                                                                   Generate the SVAs                            Verification                  Verilog
                                                                                                                                                                                   ⚫ Verilog Segments Finding
                                                                                                                                objective 1
                                                            …
                                                                                                                                                            segment 1
                                                                                                                                Verification                  Verilog
                           Evaluation Metrics:          Assertion t                                                             objective 2                 segment 2




                                                                                                                                                  …
                          ⚫ FPV Pass/Fail                                                                                                                                              Signal
                                                                                                                                Verification                  Verilog
                          ⚫ COI, Proof core,                                                                                    objective m                 segment m
                            Mutation testing                                                                                                                                                             Verilog Files



                                                                                        Fig. 2: AssertGen framework


               Entity Extraction                                                                                                                            Verification Objective
                                                                                                                                                                  Generation
              Please use the following steps to extract entities from the                                                                               You are a verification engineer. I will provide you with a text describing
              message I gave you [upload chunks]:                                                                                                      a Control Register and its related behavioral descriptors.
              l Extract signal, registers, and entities related to the Control                                                                          Please do the following steps internally:
                Register itself.                                                                                                                            1. Identify and note all behavioral descriptors related (directly
              l Other bit and register unrelated to the Control Register itself but                                                                    and indirectly) to the Control Register .
                related to its behavior.                                                                                                                    2. Gather the signal's basic info (bits, bit-width, functionality,
              l Take the intersection of the entities extracted in the two steps.                                                                      Interconnection, Additional Information, Related Signals etc.).
                lf the elements in the intersection appear in the second step                                                                               3. From steps (1) and (2), generate a final list of assertion-
                of extraction, remove them from the entities in the second step                                                                        based verification objectives only, relevant to an ABV environment
                and return the final result of the second step entity.                                                                                 without modifying the design.
                                                                                                                                                            4. Return the final list of verification objectives to me.
             [Response from Entity Extraction]
                                                                                                                                                   [Response from Verification Objective Generation]
             The following are the steps and final results of entity extraction:
                                                                                                                                                       The following are the verification objectives of Control Register :
              Step1: Extract entities related to Control Register
              [Related Registers]:                                                                                                                      1. Control Register Reset Value: - Assert that the Control
              Control Register                                                                                                                          Register (CTR) resets to `0x00` after a reset.
              [Bit/Signal Registers]:
                                                                                                                                                        2. EN Bit Behavior: - As long as ctr[7] is 0, the ena signal
              Bit 7, EN, Bit 6, IEN, Bits 5:0, Reverse.
                                                                                                                                                        should not be activated.
              Step2: Extract entities not directly related to Control Register                                                                                                         …
              [Related Registers]:                                                                                                                      11. Core Hang Prevention: - Assert that the core does not hang
              Command Register                                                                                                                          the I2C bus when the `EN` bit (CTR[7]) is cleared only after a
              [Bit/Signal Registers]:                                                                                                                   STOP command or when the `STO` bit in the Command
              STO Bit, EN                                                                                                                               Register is set.
              Step3: Find the intersection and remove it from the second step
              [Intersection Entity]:
              EN
              [Final Result]:                                                                                         Fig. 4: Prompt and response of verification objective genera-
              Command Register, STO Bit
                                                                                                                      tion
      Fig. 3: Prompt and response of entity extraction                                                                   Building upon the advantages of verification objective ab-
                                                                                                                      straction, we adopt a similar strategy within the AssertGen
which serves as a new query signal to construct the corre-
                                                                                                                      framework. Specifically, we use the target signal s and the
sponding query qk , and performs RAG-based retrieval over the
                                                                                                                      retrieved specification chunks C ′ as input to the LLM to
vector database H. This iterative expansion continues until no
                                                                                                                      construct the verification objectives v:
new entities are produced, i.e., Efinal = ∅, marking the con-
vergence of the entity set. Meanwhile, all retrieved chunks ci                                                                                                              v = fLLM (s, C ′ )                                       (1)
from H are persistently stored to ensure that subsequent stages
                                                                                                                      To ensure the LLM can effectively integrate the graphical
can effectively utilize the accumulated contextual information.
                                                                                                                      descriptions, structural features, and implicit temporal depen-
C. Step 2: Verification Objective Generation                                                                          dencies scattered across different semantic levels, we designed
                                                                                                                      and applied a structured prompt as shown in Fig. 4, where
   In practical hardware development, engineers typically                                                             the blue-highlighted parts of the verification objective includes
adopt a top-down methodology to modularize circuit design,                                                            both the top-level module and sub-level module. This prompt
thereby reducing inter-module coupling and simplifying in-                                                            guides the model to generate a comprehensive and precise
tegration and debugging. However, this methodology often                                                              verification objectives set V = {v1 , v2 , . . . , vn }.
lacks explicit bridging of signal behaviors across layers in the
specification. To address this limitation, verification engineers                                                     D. Step 3: Bridging Signal Verification Objectives to Verilog
abstract signal descriptions and contextual entities into veri-                                                       Segments
fication objectives, enabling precise cross-layer bug detection                                                         Requirement traceability, which provides bidirectional map-
and module-level attribution.                                                                                         ping between specifications, RTL designs, and verification
                       Signal Chain                                                                                  Objectives-Verilog
                        Generation                                                                                   Segments Bridging
             [Upload the RTL files]: You are a skilled hardware verification engineer                        [Upload verification objectives, signal chain, RTL files]: Your task is
             who is good at reading and analyzing RTL code (Verilog/VHDL).                                   to:
             Your task is to:                                                                                Step 1: Carefully read the objectives to be verified and its
             Step 1: Carefully read the objectives to be verified and the description                        Description provided in 'Description' to understand its logical
             provided in its description to understand its logical function and related                      function and related signals.
             Control Register.                                                                               Step 2: Step by step analysis 'RTL Code' and 'Signal chain' for
             Step 2: Extract the signal related to the authentication entry from                             every item, extract all potentially relevant segments of code for
             the RTL code files provided.                                                                    each item to be verified, including:
             Step 3: Extract the signal chain related to signal extracted in step 2.                         State Machine (FSM) logic, Assignment/update of key signals ,
                                                                                                             Register operation, Conditional judgment logic and Other
             [Response from Signal Chain Generation]                                                         codes directly related to the logic of the objectives to be verified
              To extract the signal chain for each verification objectives, I will
              carefully analyze the provided RTL code and trace the relevant signals                        [Response from Objectives-Verilog Segments Bridging]
              step by step. Below is the detailed signal chain for each verification                         The following is the Verilog segments corresponding to the
              item:
                1. Verification objective 1: Control Register Reset Value                                    verification objectives:
                  [signal]: 1. ‘ctr’ -defined in `i2c_master_top.v`                                          1. Verification objective 1:
              2. Verification objective 2: Assert that the core is enabled only                                  always @(posedge wb_clk_i or negedge rst_i)
              when the `EN` bit (CTR[7]) is set to `1`, and disabled when `EN`                                       if (!rst_i)
              is `0`.                                                                                                 ctr <= #1 8'h0;
                  [signal]: 1. ctr[7]` (EN bit) - Defined in `i2c_master_top.v`.                                     else if (wb_rst_i)
                            2. `ena` - Signal in `i2c_master_byte_ctrl.v`.                                            ctr <= #1 8’h0;
                                                   ...                                                       2. Verification objective 2:
                                                  …                                                              .ena (core_en)- `i2c_master_byte_ctrl`
              11. Verification objective 11: Assert that the core does not hang                                  .ena (ena)- `i2c_master_bit_ctrl`
              the I2C bus when the `EN` bit (CTR[7])...                                                                                     ...
                  [signal]: 1. ctr[7]` (EN bit) - Defined in `i2c_master_top.v`.                                                            ...
                            2. `ena` - Signal in `i2c_master_byte_ctrl.v`.                                   11. Verification objective 11:
                            3. `ena` - Signal in `i2c_master_bit_ctrl.v`.                                         .ena (core_en)
              Signal Chain: ’ctr’->’ena’->’ena’                                                                   wire sto = cr[6];



                                                                                                Fig. 6: Prompt and response of bridging verification objectives
         Fig. 5: Prompt and response of signal chain
                                                                                                to verilog segments
objectives, is critical for ensuring every requirement is fully
implemented and verified. However, the hierarchical nature                                      to perform document scanning and matching operations. We
of SoC designs and cross-layer signal propagation make this                                     define the bridging function as:
process highly complex.                                                                                                  M : (V, SC, D) → RV                                           (4)
   To address this challenge, we propose a two-stage struc-
tured reverse bridging approach comprising: (1) Signal Chain                                    where Rv ⊆ D denotes the set of verilog code segments
Extraction, and (2) Bridging Verification objectives to Verilog                                 semantically related to the verification objectives V. The
Segments. This approach incrementally bridges each signal in                                    matching process compares the signal semantics in vi with
a verification intent to its definition in the RTL hierarchy.                                   the defined locations of each signal si ∈ SC in the design
   Signal Chain Extraction: In hierarchical RTL designs,                                        files, establishing a structural alignment between verification
signals often form complex cross-layer propagation paths                                        requirements and RTL designs, the prompt of this process is
through various modules. Traditional language models struggle                                   shown in Fig. 6.
to accurately capture these structural dependencies. To this
end, we define the concept of signal chain (SC), as detailed                                    E. Step 4: SVA Generation
below:                                                                                             In this stage, we used GPT-4o with verification objectives,
   Definition 1 (Signal Chain). Given a signal s0 ∈ Module0 ,                                   verilog segments, and signal chain context to generate SVAs.
where Module0 denotes the highest-level module in the design                                    However, initial evaluations revealed that despite correct in-
hierarchy where s0 appears, and s0 is included in the verifica-                                 tent, the outputs suffered from inconsistent formatting. These
tion objectives, its cross-layer propagation path is represented                                flaws made the code unreliable and required significant man-
as an ordered sequence:                                                                         ual correction, indicating that the model needs fine-grained
                                                                                                guidance to ensure structural consistency.
         SC(s0 ) = {s0 , s1 , . . . , sn },                           si ∈ Modulei        (2)
                                                                                                   To address this issue, we design a fine-grained prompt
where any adjacent signal pair satisfies the semantic propaga-                                  strategy to guide the generation process and enforce format
tion constraint:                                                                                alignment. Specifically, for each signal or functional behavior
                                                              semantic
                                                                                                to be verified, we incorporate the following constraints into
                    ∀i ∈ [1, n],                 si−1 −−−−→ si                            (3)   the prompt:
                                                                                                   1) Signal Binding: Signals are explicitly referenced and
That is, each signal si is semantically derived from its prede-                                        bound using the format:
cessor si−1 .
   Based on this definition, we design a recursive method                                                    source_module_name.signal_name
grounded in CoT Prompting, which guides the LLM to con-
                                                                                                  2) Unified Output Format: All generated assertions follow a
struct signal dependencies across layers. This serves as a                                           consistent template:
structural prior for the subsequent bridging phase, as illustrated
                                                                                                          assert property
in Fig. 5.
                                                                                                          @(posedge {source_module_name}.{signal_name})
   Bridging Verification Objectives to Verilog Segments:
After completing the extraction of the signal chain SC(s0 ),                                      By adopting this format, we effectively constrain the LLM’s
we input the verification objectives V, signal chain SC and                                     generation behavior to enhance the reliability of GPT-4o’s
design file collection D = {d1 , d2 , . . . , dm } into the LLM                                 assertion outputs.
                      IV. EXPERIMENTS                                               TABLE II: Benchmarks information
                                                                        Design Name     Cell number     FF     Primary inputs (bits)   LOC
A. Experimental Setup                                                        I2 C            756         11             33             1282
   The benchmarks employed in this study are derived from                   ECG            59084       7443            932             1635
                                                                          Pairing         228287       31380          1943             2145
open-source datasets [18] [19]. The external inputs for the                SHA3            22228       2211            585             618
framework consist of initial specification documents in PDF              PicoRV32          17075       1969           2788             3049
format, signal definition files, and RTL designs in Verilog
format.                                                                D. Experimental Results
   To evaluate the effectiveness of AssertGen against SOTA ap-            To comprehensively evaluate the effectiveness of the As-
proaches, three assertion generation frameworks—AssertLLM              sertGen, we experimentally compare it with baseline methods
[10], SPEC2Assertion [20], and AssertGen—are compared,                 on the five benchmark designs of different sizes. The detailed
with their correctness and quality assessed using the commer-          results are shown in Table III. AssertGen delivers acceptable
cial formal verification tool Cadence JasperGold (v21.12.002).         performance on smaller and medium-sized design modules.
Moreover, all experiments are run on a server with an Intel(R)         For the I2 C design, AssertGen achieves an FPR of 84.85%,
Xeon(R) Gold 6148 CPU @ 2.40GHz.                                       significantly outperforming both AssertLLM (58.47%) and
                                                                       SPEC2Assertion (32.58%). In terms of COI coverage, Assert-
B. Evaluation Metrics                                                  Gen provides a modest improvement over SPEC2Assertion
                                                                       (98.41%) and AssertLLM (86.71%). More importantly, for
   Our evaluation protocol is designed for objectivity and rigor.
                                                                       PC coverage, AssertGen reaches 98.35%. This increase is
All SVAs generated by the LLM are used directly without
                                                                       mainly due to the I2 C module’s structure, where functionality
post-processing, and their quality is assessed using metrics
                                                                       centers around a few key registers, making high coverage
from JasperGold, with the mutation testing (MT) as well.
                                                                       on critical components more feasible. For the SHA3 module,
Unlike simpler structural metrics such as Cone of Influence
                                                                       AssertGen demonstrates equally comprehensive performance.
(COI) or Proof Core (PC) provided by Jaspergold, MT directly
                                                                       It not only surpasses all baseline methods in FPR (82.61%) and
evaluates an assertion’s quality with its capability to detect
                                                                       PC coverage (60.79%), but also matches the top-performing
injected mutation errors. It verifies that an SVA is not merely
                                                                       baseline in COI coverage at 89.61%, ensuring both the breadth
valid, but also capable of detecting injected design faults,
                                                                       and depth of verification. On the mid-scale PicoRV32 design,
making it the most stringent evaluation of an assertion’s
                                                                       AssertGen still shows some advantages, achieving roughly
verification power. In line with the methodology from [10],
                                                                       twice the PC coverage of the comparative algorithms.
our protocol for determining metrics like F P R conservatively
                                                                          When applied to larger and more complex designs, Assert-
treated any proof that timed out after 5 hours as a pass. The
                                                                       Gen continues to demonstrate its effectiveness. For Pairing,
detailed evaluation criteria are shown in Table I.
                                                                       AssertGen’s FPR is 75.96%, slightly lower than AssertLLM’s
           TABLE I: Summary of Evaluation Metrics
                                                                       76.67%. This difference may result from the complex temporal
    Evaluation Metrics                       Summary                   and logical relationships among cross-layer signals in Pairing,
   FPV pass rate (F P R)     Rate of SVAs passing FV
                                                                       which make accurate assertion localization difficult. Regarding
  Cone of influence (COI)    All logic driving a property
     Proof core (P C)        Minimal logic to prove property           PC coverage, the baseline methods are nearly ineffective,
 Bug Detection Rate (BDR)    Design error detection capability in MT   yielding only 0.05% and 0.08% respectively, whereas Assert-
                                                                       Gen boosts this coverage to 5.32%. On another large-scale
                                                                       design, ECG, AssertGen demonstrates improvements across
C. Benchmarks                                                          all three metrics compared to the other two methods, achieving
   To evaluate the effectiveness and scalability of AssertGen,         an FPR of 76.92%, COI of 99.73%, and PC of 23.55%.
we select benchmark designs with varying complexities, pri-
marily determined by the number of flip-flops (FFs) and                E. Extended Experiment on Mutation Testing
primary inputs (bits), causing exponential growth in state and            In the previous subsection, the effectiveness of the assertions
search spaces, respectively [21]. As detailed in Table II, our         generated by AssertGen is evaluated from the two dimen-
benchmark suite rigorously evaluates AssertGen by covering             sions of breadth and depth of structural coverage through the
small-scale, control-intensive I2 C core (approximately 1282           analysis of COI and PC. However, these two metrics cannot
lines of code (LOC)), as well as medium-scale designs like the         directly evaluate the ability of assertions to detect actual design
compute-focused SHA3 and the size-optimized RISC-V CPU                 errors. Therefore, in this subsection, we use mutation testing to
PicoRV32. To further test its capability, the suite includes the       evaluate the ability of generated assertions to detect mutation
medium-to-large, mixed-signal ECG module. Finally, to push             errors.
the limits of scalability, the suite is anchored by the large-            The mutation testing results of AssertGen, Assertllm, and
scale Pairing cryptographic accelerator, which contains over           SPEC2Assertion are shown in Fig. 7. AssertGen demonstrats
31,000 FFs. All post-synthesis metrics are obtained using the          certain bug detection capabilities on I2 C and SHA3 modules.
open-source tool Yosys-STA [22] under a 45nm process node,             For I2 C design, its BDR reaches 31.14%, while the two
ensuring a consistent basis for our evaluation.                        baseline methods are both below 2%, which makes it almost
                         TABLE III: Performance comparison of AssertLLM, SPEC2Assertion and AssertGen
                             AssertLLM                                   SPEC2Assertion                                         AssertGen
  Metric
            I2 C     ECG      Pairing SHA3 PicoRV32           I2 C     ECG Pairing SHA3 PicoRV32               I2 C     ECG      Pairing SHA3 PicoRV32
F P R(%)   58.47     54.55     76.67     78.05     32.91     32.58     65.52    36.59     66.67     39.74     84.85     76.92     75.96     82.61     81.44
COI(%)     86.71     99.52     33.19     89.56     33.37     98.41     98.37    51.08     70.45     42.38     98.80     99.73     54.48     89.61     62.49
  P C(%)   4.43       0.22     0.05      58.90     12.18      0.26      3.58    0.08        0       13.27     98.35     23.55      5.32     60.79     32.21



                                                                                 [2] Ma R, Yang Y, Liu Z, et al. VerilogReader: LLM-Aided Hardware Test
                                                                                     Generation[C]//2024 IEEE LLM Aided Design Workshop (LAD). IEEE,
                                                                                     2024: 1-5.
                                                                                 [3] Deng Y, Chen R, Xiao C, et al. LLM-TG: Towards Automated Test Case
                                                                                     Generation for Processors Using Large Language Models[C]//2024 IEEE
                                                                                     42nd International Conference on Computer Design (ICCD). IEEE,
                                                                                     2024: 389-396.
                                                                                 [4] Akyash M, Kamali H M. Self-HWDebug: Automation of LLM self-
                                                                                     instructing for hardware security verification[C]//2024 IEEE Computer
                                                                                     Society Annual Symposium on VLSI (ISVLSI). IEEE, 2024: 391-396.
                                                                                 [5] Saha D, Yahyaei K, Saha S K, et al. Empowering hardware security with
                                                                                     LLM: The development of a vulnerable hardware database[C]//2024
                                                                                     IEEE International Symposium on Hardware Oriented Security and Trust
                                                                                     (HOST). IEEE, 2024: 233-243.
Fig. 7: Bug Detection Rates of AssertLLM, SPEC2Assertion,                        [6] Liu Y, Xue Y, Wu D, et al. Propertygpt: LLM-driven formal verification
and AssertGen Across Four Designs                                                    of smart contracts through retrieval-augmented property generation[J].
                                                                                     arXiv preprint arXiv:2405.02580, 2024.
impossible to detect bugs. On the SHA3 module, AssertGen’s                       [7] Hassan M, Ahmadi-Pour S, Qayyum K, et al. LLM-guided formal
detection rate reaches 15.35%, which is nearly 4 percentage                          verification coupled with mutation testing[C]//2024 Design, Automation
                                                                                     & Test in Europe Conference & Exhibition (DATE). IEEE, 2024: 1-2.
points higher than the best performing baseline method As-                       [8] Maddala K, Mali B, Karfa C. LAAG-RV: LLM Assisted Assertion
sertLLM (11.36%).                                                                    Generation for RTL Design Verification[C]//2024 IEEE 8th International
   AssertGen still has some effect on the more complex designs                       Test Conference India (ITC India). IEEE, 2024: 1-6.
                                                                                 [9] Xie J, Liu C C. Multi-agent systems and their applications[J]. Journal
of PicoRV32 and EGC. On the PicoRV32 core, its BDR                                   of International Council on Electrical Engineering, 2017, 7(1): 188-197.
(23.20%) is twice as high as the baseline, which demon-                         [10] Yan Z, Fang W, Li M, et al. AssertLLM: Generating Hard-
strates that AssertGen has scalability. Meanwhile, on the ECG                        ware Verification Assertions from Design Specifications via Multi-
                                                                                     LLMs[C]//Proceedings of the 30th Asia and South Pacific Design
module, AssertGen achieves rates of 8.12%, outperforming                             Automation Conference (ASP-DAC). 2025: 614-621.
the baseline methods (with only 1.34% and 0.81% respec-                         [11] Sang Y, Liu B, Zhao R, et al. SoC Verification Quantitative Closed-loop
tively). The largest module, Pairing, is excluded from this                          Management Based on Automation and DPI-C Library[J].
                                                                                [12] Hekmatpour A, Salehi A. Block-based shema-driven assertion genera-
experimental evaluation due to its prohibitive computational                         tion for functional verification[C]//14th Asian Test Symposium (ATS).
cost, with an estimated runtime for mutation testing exceeding                       IEEE, 2005: 34-39.
120 hours. As SVAs are usually designed for coverage of                         [13] Yamada T. Assertion generating system, program thereof, circuit verify-
                                                                                     ing system, and assertion generating method: U.S. Patent 7,603,636[P].
certain important design properties, it is not necessary to has                      2009-10-13.
high detection rates of mutation test. But the improvement of                   [14] Zhao J, Harris I G. Automatic assertion generation from natural language
BDR of AssertGen on the baseline methods still shows its                             specifications using subtree analysis[C]//2019 Design, Automation &
                                                                                     Test in Europe Conference & Exhibition (DATE). IEEE, 2019: 598-601.
capabilities on capturing bugs difficult to catch.                              [15] Kande R, Pearce H, Tan B, et al. (Security) assertions by large language
                                                                                     models[J]. IEEE Transactions on Information Forensics and Security,
                             V. C ONCLUSION                                          2024.
                                                                                [16] Mali B, Maddala K, Gupta V, et al. Chiraag: Chatgpt informed rapid
   This paper presents AssertGen, a framework that automati-                         and automated assertion generation[C]//2024 IEEE Computer Society
                                                                                     Annual Symposium on VLSI (ISVLSI). IEEE, 2024: 680-683.
cally generates SVAs from natural language specifications and                   [17] Wang Y, Zhou J, Lyu H, et al. DeepAssert: An LLM-Aided Verification
RTL design codes. Through a multi-stage modeling approach                            Framework with Fine-Grained Assertion Generation for Modules with
that aligns verification objectives, signal traces, and design                       Extracted Module Specifications[J]. arXiv preprint arXiv:2509.14668,
                                                                                     2025.
codes, AssertGen outperforms SOTA methods like AssertLLM                        [18] IWLS 2005 Benchmaeks. https://iwls.org/iwls2005/benchmarks.html
and SPEC2Assertion in several key metrics, showing im-                          [19] A Size-Optimized RISC-V CPU https://github.com/YosysHQ/picorv32
provements in terms of formal correctness (FPR), structural                     [20] Wu F, Pan E, Kande R, et al. Spec2Assertion: Automatic pre-RTL
                                                                                     assertion generation using large language models with progressive
coverage (COI and proof core), and bug detection in mutation                         regularization[J]. arXiv preprint arXiv:2505.07995, 2025.
testing. Future work will explore and enhance the corner case                   [21] Barrett C W. ” Decision Procedures: An Algorithmic Point of View,”
bug detection capability of generated assertions.                                    by Daniel Kroening and Ofer Strichman, Springer-Verlag, 2008[J]. J.
                                                                                     Autom. Reason., 2013, 51(4): 453-456.
                                                                                [22] Xingquan Li, Simin Tao, Zengrong Huang, et al. An Open-Source
                              R EFERENCES                                            Intelligent Physical Implementation Toolkit and Library[C]. International
                                                                                     Symposium of EDA (ISEDA), 2023.
 [1] Harry Foster. 2024 Wilson Research Group IC/ASIC functional verifica-
     tion trend report. https://resources.sw.siemens.com/zh-TW/white-paper-
     2024-wilson-research-group-ic-asic-functional-verification-trend-report/
