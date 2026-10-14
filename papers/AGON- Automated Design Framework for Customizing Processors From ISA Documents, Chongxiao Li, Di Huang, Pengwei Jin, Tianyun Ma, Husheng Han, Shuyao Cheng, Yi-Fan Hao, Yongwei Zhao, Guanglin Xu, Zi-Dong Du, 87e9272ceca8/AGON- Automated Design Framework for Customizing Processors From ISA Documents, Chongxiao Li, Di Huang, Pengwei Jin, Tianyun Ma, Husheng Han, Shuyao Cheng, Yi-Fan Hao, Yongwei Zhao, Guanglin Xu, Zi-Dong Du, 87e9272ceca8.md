                                                                                                                                                                                                                                               1




                                                   AGON: Automated Design Framework for
                                                  Customizing Processors from ISA Documents
                                          Chongxiao Li, Di Huang, Pengwei Jin, Tianyun Ma, Husheng Han, Shuyao Cheng, Yifan Hao, Yongwei Zhao,
                                                      Guanglin Xu, Zidong Du, Rui Zhang, Xiaqing Li, Yuanbo Wen, Xing Hu, Qi Guo



                                            Abstract—Customized processors are attractive solutions for
                                         vast domain-specific applications due to their high energy ef-
                                         ficiency. However, designing a processor in traditional flows
arXiv:2412.20954v2 [cs.AR] 21 Jan 2025




                                         is time-consuming and expensive. To address this, researchers




                                                                                                                         Expert effort
                                                                                                                                                                         [25] BOOM
                                         have explored methods including the use of agile development                                                    [24] FINN
                                                                                                                                                                      [26] Rocket-chip
                                                                                                                                                                                                                         Natural    Natural
                                                                                                                                                                       Agile-based                                      language   language
                                         tools like Chisel or SpinalHDL, high-level synthesis (HLS) from                                                [23] ENIAD
                                                                                                                                                       HLS-based
                                         programming languages like C or SystemC, and more recently,                                                                                                     C code                       nOP
                                         leveraging large language models (LLMs) to generate hard-                                                                                       Hardware packages                          function
                                                                                                                                         LLM-assisted                      AGON
                                         ware description language (HDL) code from natural language                                      RTL generation
                                         descriptions. However, each method has limitations in terms                                                                                           RTL        RTL             RTL         RTL
                                                                                                                                              102     103   104      105    106
                                                                                                                                           (Adder) (ALU)                   (CPU)
                                         of expressiveness, correctness, and performance, leading to a                                                                                        Agile      HLS        LLM-Synth       AGON
                                                                                                                                                 Complexity (# cells)
                                         persistent contradiction between the level of automation and the                                              (a)                                                        (b)
                                         effectiveness of the design. Overall, how to automatically design
                                         highly efficient and practical processors with minimal human                    Fig. 1. Comparing AGON with existing synthesis work in terms of needed
                                         effort remains a challenge.                                                     expert effort and (a) complexity, (b) automation level.
                                            In this paper, we propose AGON, a novel framework designed
                                         to leverage LLMs for the efficient design of out-of-order (OoO)
                                         customized processors with minimal human effort. Central to
                                         AGON is the nano-operator function (nOP function) based                         Processing Units (CPUs) and application-specific accelerators
                                         Intermediate Representation (IR), which bridges high-level de-                  offers both high flexibility and efficiency, this approach still
                                         scriptions and hardware implementations while decoupling func-                  relies heavily on manual efforts and incurs high manual costs
                                         tionality from performance optimization, thereby providing an                   due to massive demands for diverse customized scenarios.
                                         automatic design framework that is expressive and efficient, has
                                                                                                                         For example, the construction of a high-performance RISC-
                                         correctness guarantees, and enables PPA (Power, Performance,
                                         and Area) optimization.                                                         V CPU using the widely recognized Chisel language requires
                                            Experimental results show that superior to previous LLM-                     approximately 60,000 lines of code [7], indicating a substantial
                                         assisted automatic design flows, AGON facilitates designing a                   investment in the design process.
                                         series of customized OoO processors that achieve on average                        To reduce the design efforts for customized processors
                                         2.35 × speedup compared with BOOM, a general-purpose CPU
                                                                                                                         with instruction extensions, researchers and designers have
                                         designed by experts, with minimal design effort.
                                                                                                                         dedicated significant efforts to simplifying or automating the
                                           Index Terms—CPU, design framework, automatic design,                          design flow:
                                         computer-aided design.
                                                                                                                          • Design on encapsulated hardware abstraction: Agile de-
                                                                                                                            velopment tools simplify the design flow with encapsulated
                                                                   I. I NTRODUCTION                                         hardware design abstractions. Prominent examples include
                                               USTOMIZED processors achieve prominent efficiency                            leveraging Chisel or SpinalHDL in developing hardware
                                         C     and are widely adopted in diverse domain-specific appli-
                                         cations, such as the Internet of Things (IoT) and multi-media
                                                                                                                            systems [8], [9]. However, it still demands massive expert
                                                                                                                            programming for various customized applications. For in-
                                         embedded systems [1]–[6]. Though the combination of Central                        stance, constructing a high-performance RISC-V CPU in
                                                                                                                            Chisel necessitates approximately 60k lines of code [7],
                                           Chongxiao Li, Pengwei Jin, and Husheng Han are with the State Key                representing a significant design effort.
                                         Lab (SKL) of Processors, Institute of Computing Technology (ICT), Chinese
                                         Academy of Sciences (CAS), Beijing, China, the University of Chinese             • Synthesis from high-level programming language: High-
                                         Academy of Sciences, Beijing, China, and also with Cambricon Technologies.         level synthesis (HLS) tools can automatically synthesize
                                           Di Huang, Shuyao Cheng, Yifan Hao, Yongwei Zhao, Guanglin Xu, Rui                register-transfer level (RTL) hardware codes from high-
                                         Zhang, Yuanbo Wen, and Qi Guo are with the SKL of Processors, ICT, CAS,
                                         Beijing, China.                                                                    level languages (C or SystemC) to reduce human effort
                                           Tianyun Ma is with the University of Science and Technology of China,            further. However, the coarse-grained synthesized circuit
                                         Hefei, China, the SKL of Processors, ICT, CAS, Beijing, China, and also with       suffers from sub-optimal performance [10]. Moreover, HLS
                                         Cambricon Technologies.
                                           Zidong Du and Xing Hu are with the SKL of Processors, ICT, CAS, Beijing,         does not automate the entire process from specifications to
                                         China, and Shanghai Innovation Center for Processor Technologies, Shanghai,        circuits. Manually writing high-level language code remains
                                         China.                                                                             a significant burden.
                                           Xiaqing Li is with the Key Laboratory of Big Data and Artificial Intelli-
                                         gence in Transportation (Beijing Jiaotong University), Ministry of Education,    • Synthesis from natural language: Recently, researchers
                                         Beijing, China.                                                                    have explored the attempts to utilize large language mod-
                                                                                                                                     2



  els (LLMs) to generate RTL code directly from natural               processor RTL from natural language for prototyping, facilitat-
  language specifications. However, these methods are far             ing rapid evaluation and verification, and serves as a basis for
  from practical use. For example, in RTLLM [11], no                  further development. AGON offers the following advantages:
  LLM-based methods successes in generating a simple 407-             ❶ Being expressive and efficient: AGON abstracts basic
  cell reduced instruction set computer (RISC) CPU circuits           operations in instructions into nOPs, and through the combi-
  (syntax checking all failed in five trials), including GPT-         nation of nOPs, it can implement diverse instruction functions.
  4. This is caused by the following reasons: ❶ The gap               Unlike HDL-based methods, AGON minimizes descriptive
  between LLMs’ strength in high-level tasks and processors’          code while preserving generality, enhancing LLM generation
  low-level hardware implementation. Hardware Description             efficiency. ❷ Ensuring correctness: AGON, through data
  Languages (HDLs) have a significant gap with other high-            flow graph representation and bit width inference of nOPs,
  level programming languages such as Python or C++, due              hides explicit port connection, sequential structures, and bit
  to their explicit control of port connections, sequential           width management in hardware design from LLMs, enhancing
  structures, and signal bit widths. The scarcity of high-            LLM generation accuracy and simplifying manual debugging,
  quality HDL data (˜1GB in HDLs v.s. ˜800GB in all                   thereby minimizing manual intervention. With nOP functions
  programming languages [12]) results in LLMs being sig-              accurately representing instruction functionalities, AGON’s
  nificantly weaker in HDL generation tasks compared to               primitives employ rule-based functional equivalence transfor-
  high-level programming tasks. Additionally, LLMs struggle           mations to guarantee processor implementation correctness.
  with large-scale projects [13]–[15], which are exacerbated          Additionally, AGON offers multi-level verification primitives
  in processor design due to the extensive code required              to validate the implementation. ❸ Enabling PPA optimiza-
  for managing low-level RTL details. ❷ The gap between               tion: AGON decouples functionality and optimization, only
  LLMs’ lack of inherent verification capability and the              requiring that LLM generate correct functional descriptions
  stringent correctness demands in processor design. Since            while leveraging multi-level primitives for processor opti-
  LLMs generate outputs by predicting the next token based            mization. Among these primitives, AGON also provides PPA-
  on probability distributions learned from training data, they       aware auto-tuning, reducing human intervention and achieving
  inherently lack mechanisms to verify the correctness of their       optimized design.
  generation. However, the hardware design for processors                The main contributions of this paper are as follows:
  requires high correctness and strict verification. Without             • We introduce AGON, an automated framework developed
  efficient verification mechanisms, LLMs cannot generate                  for rapid RTL generation from ISA documents to proces-
  practical processors correctly, hindering their application in           sors. AGON introduces nOP functions IR to assist LLMs
  design flows. ❸ The gap between functionality description                efficiently and expressively translating ISA requirements
  and performance optimization. Beyond accurate design gen-                to formal functionality definitions. AGON offers multi-
  eration, performance optimization is even more challenging               level verification mechanisms for correctness validation.
  for LLMs. Unlike design generation, performance optimiza-              • AGON decouples functionality and performance opti-
  tion requires a good understanding of functional equivalence             mization. During transforming nOP functions to RTL
  and the relationship between HDL code and performance,                   design, AGON proposes scheduling primitives and PPA-
  power, and area (PPA), which is currently unattainable due               aware auto-tuning methods for design optimization.
  to the scarcity of training data [16].                                   AGON offers compiler and simulation tools for automat-
                                                                           ically generating high-performance processor RTL proto-
   In summary, we are trapped in the contradiction between
                                                                           types.
the level of automation and design effectiveness. As shown
                                                                         • We perform comprehensive evaluations on AGON. The
in Figure 1, the higher the level of automation, the simpler,
                                                                           results show that, compared to other LLM-assisted meth-
slower, and less efficient the designed circuits. It is challenging
                                                                           ods, AGON is able to design practical-level processors
for the automation framework to meet all these three require-
                                                                           with minimal human intervention. We showcase design-
ments: ❶ design complex processors for various applications
                                                                           ing a series of high-performance out-of-order processors
efficiently, ❷ achieve functional correctness with minimal
                                                                           based on AGON. Compared with an expert-designed
human intervention, and ❸ empower hardware optimization to
                                                                           general-purpose CPU, our processor achieves an average
attain comparable performance with human-crafted processors.
                                                                           of 2.35 × speedup on specific tasks.
   To this end, we introduce AGON, a framework designed
for LLM-based design flows, facilitating efficient out-of-order
                                                                                  II. BACKGROUND AND M OTIVATION
(OoO) customized processor RTL prototyping with minimal
human intervention. The key insight of AGON is a nano-                A. Customized Processors
operator function (nOP function) based Intermediate Repre-               Customized processors have been widely used in scenarios
sentation (IR) to not only bridge the gap between high-level          demanding highly optimized performance for specific tasks,
descriptions and the hardware-level implementation but also           especially with area or power constraints such as embedded
decouple the functionality and the performance optimization.          systems [6], signal processing [4], [5], networking [1]–[3].
AGON is not intended to replace existing processor design             Compared to out-of-core accelerators, customized processors
flows but to offer an infrastructure for processor development        offer the advantages of minimal area overhead, low data trans-
in the era of LLMs. It enables the generation of customized           fer overhead, and ease of programming, making them an at-
                                                                                                                                                               3



                                                  1   import agon                                                3.39. sha512sum0
            ISA Extension                         2   # other nOP functions... (omitted)                         Synopsis
            Documents                             3   def sha512sum0(rs1, rd, pc):                               Implements the Sum0 transformation
                                                  4       op1 = REG_READ(rs1)                                    function as used in the SHA2-512 hash
            LLM-based Generation (§6)             5       rot1 = OR(SRL(op1, 28), SLL(op1, 64 - 28))             function [49] (Section 4.1.3).
                                                  6       rot2 = OR(SRL(op1, 34), SLL(op1, 64 - 34))             Mnemonic
            Functionality (§4)                    7       rot3 = OR(SRL(op1, 39), SLL(op1, 64 - 39))             sha512sum0 rd, rs1
        nOP functions                             8       result = XOR(XOR(rot1, rot2), rot3)                    Description
                                                  9       REG_WRITE(rd, result)             LLM-generated        This instruction is supported for the RV64
                                  Verification   10       INC_PC(pc)                                             base architecture. It implements the Sum0
      instruction (§5.1)                                                                      nOP functions
                                   (§5.4)        11                                                              transform of the SHA2-512 hash function.
                                                 12   # initialize variables... (omitted)                        [49]. This instruction must always be
                                   test IO &     13   sum0 = agon.instruction(sha512sum0, encoding)              implemented such that its execution latency
          isa (§5.2)
                                   programs      14   sum0.fuse(pattern)                                         does not depend on the data being operated
                                                 15   I = agon.isa([..., sum0])     # construct ISA              on.
    processor (§5.3)                             16   P = agon.processor(I, config) # configure processors       Operation
 AGON                                            17   ppa = P.simulate(benchmark_program)                        function clause execute
         Optimization (§5)
                                                 18   # verification                                                (SHA512SUM0(rs1, rd)) = {
            Synthesis (§5.5)                     19   sum0.verify(sum0_test_io)                                     X(rd) = ror64(X(rs1), 28) ^
                                                 20   I.verify(test_program)                                                 ror64(X(rs1), 34) ^
                                                 21   P.verify(test_program)                                                 ror64(X(rs1) ,39);
            RTL design                           22   # synthesize to RTL design                optimization        RETIRE_SUCCESS
                                                 23   P.synthesize()                           & verification    }

                       (a)                                                     (b)                                                  (c)

Fig. 2. The overview of AGON. (a) AGON decouples optimization from functionality, using nOP functions to describe the processor functionality, and
then instantiates, optimizes, and verifies designs at different levels through a set of primitives. (b) An example of using AGON for design. The functional
descriptions are generated with LLM. (c) The ISA document provided to LLM for the sha512sum0 instruction in (b). This snippet is taken from [17],
which originally contains natural language descriptions and pseudo code.



tractive choice [18]. The key is to utilize instruction set exten-             of code. Automated processor design with Chisel still faces
sions to combine the flexibility of general-purpose processors                 considerable challenges and requires further development to
and the high performance of application-specific integrated                    streamline the process.
circuits. These extensions encompass a range of functionali-
ties, including vector extensions [19], security extensions [17],              C. LLM-based Attempts on Hardware Generation
[20], [21], virtualization extensions [22]. However, supporting                   Recent researches [11], [28]–[33] have explored the po-
customized instruction extensions entails meticulous design                    tential of LLMs for directly generating RTL code from
and modification of the processor architecture. It demands                     natural language description. These studies can be divided
intensive coordination among architecture design, circuit de-                  into two categories: how to utilize existing LLMs to assist
velopment, and verification teams, which incurs significant                    in generating circuits without training, and how to fine-tune
time and human efforts, making customization costly.                           open-source LLMs for better module-level HDL generation.
                                                                               For the former, Chip-Chat [28] and Chip-GPT [29] employ
                                                                               ChatGPT to generate circuits in a conversational manner which
B. Automated Processor Design Techniques
                                                                               requires interactive human feedback. RTLLM [11] utilizes a
   High-level synthesis tools enable designers to describe cir-                self-planning technique, where LLM first gives out a high-
cuit functionality at a high level of abstraction using languages              level plan and then generates the HDL code. However, even
like C, C++, or System C [23], [24]. These tools automati-                     equipped with GPT-4, RTLLM fails to generate functionally
cally generate hardware description languages from high-level                  correct HDL code for simple designs, such as a 32-bit adder.
specifications, accelerating the design process and enabling                   For fine-tuning LLMs, Thakur et al. [30] and Liu et al. [31]
rapid exploration of design alternatives. HLS techniques first                 fine-tune different LLMs with up to 16B parameters for HDL
analyze the algorithm described in high-level code written by                  generation and presented an evaluation suite, respectively.
experts then partition it into hardware-friendly components,                   Chang et al. [32] and BetterV [33] present data augmentation
and perform data flow analysis to identify opportunities for                   methods to collect high-quality Verilog datasets, and fine-
parallel execution and optimization, such as pipelining and                    tune different open-sourced models. None of these methods
parallelized loops. Although HLS techniques significantly re-                  have demonstrated accuracy that fully exceeds GPT-4 and they
duce development time, the PPA from HLS is typically inferior                  can generate module-level HDL only, which is still far from
to those from traditional RTL design flow [10].                                assisting in designing chips.
   In more practical usages, designers leverage Chisel [8]                        There are mainly three gaps that prevent LLM from design-
for agile processor developing [7], [25], [26]. Chisel, a                      ing practical-level processors using HDLs:
hardware construction language embedded in Scala, leverage                        The gap between the long code processing ability of
an intermediate representation called FIRRTL [27], which                       LLMs and the scale of processor design projects. LLMs
can be optimized and synthesized into RTL. This results in                     struggle to process information within long contexts effec-
hardware designs that can achieve comparable performance to                    tively, especially when their length exceeds their training
those developed in Verilog. However, utilizing Chisel requires                 data [34]. The average length of Verilog code in the RTL-
designers to possess expertise and write substantial amounts                   Coder [35] fine-tuning dataset is 451.9 tokens, while the
                                                                                                                                  4



main part of open-source in-order CPU core cv32e40p [36]          Figure 2 illustrates the overall framework of AGON and show-
comprises 28 SystemVerilog files totaling 243,013 tokens.         cases an example using AGON to design a customized proces-
Evaluations in RTL-Repo [15] show that as the input context       sor. AGON decouples functionality from optimization. From
length increases from 2k to 64k tokens, the accuracy of           the functionality aspects (Section IV), it utilizes nOP functions
GPT3.5 and RTLCoder-Deepseek generating the next Verilog          generated by LLM to define the functionality of instructions
code line drops by 54.0% and 50.1%, respectively. Also,           in the processor. From the optimization aspects (Section V),
for complex code projects, LLMs struggle with complicated         it contains three levels of implementation: instruction (Sec-
cross-file dependencies [13]–[15]. Designing processors using     tion V-A), ISA (Section V-B), and processor (Section V-C). It
HDLs necessitates exhaustive files with complex inter-module      utilizes a set of primitives for instantiation, optimization, and
calling relationships. These gaps in LLM capabilities hinder      verification(Section V-D), keeping the functionality described
the application of LLMs in processor design using HDL.            in nOP functions unchanged, and eventually implements the
   The gap between HDLs and other software languages.             processor to an RTL design (Section V-E). By leveraging
LLMs leverage code as part of their training data to enhance      LLMs to generate nOP functions from the ISA documents
their logical and coding capabilities. However, HDLs focus on     (Section VI) and utilizing AGON’s auto-tuning primitives,
describing circuit structures, which is distinct from software    designers can efficiently design customized processors with
languages that focus on program control-data flow. Moreover,      extended instructions, requiring minimal human intervention.
high-quality HDL codes typically belong to integrated circuit        Figure 2 (b) illustrates a simplified example of using AGON
companies, making training data less. HDLs account for only       to design a customized processor. AGON is embedded in
about 1/800 of all programming languages [12]. Consequently,      Python, and the design starts with LLM-generated nOP func-
LLM’s generation capabilities in HDL are significantly inferior   tions (lines 2-10), which are used to define the functionalities
to those in software programming languages, with respective       of the instructions. The nOP function and its encoding are
state-of-the-art methods scoring 46.1 [33] on VerilogEval [31]    instantiated as a single instruction (line 13), followed
compared to 96.9 [37] on HumanEval [38], a Python gen-            by optimizations at the instruction level (lines 14). A set
eration benchmark. HDLdebugger [39] identifies the frequent       of instructions is then combined into an isa (line 15) and
reasons for LLM’s errors in generating Verilog, most of which     configured as a processor (line 16). We can simulate
are related to port connections, sequential structures, and       (line 17) and synthesize (line 23) the processor. We
bit width management. This highlights a clear semantic gap        verify at multiple levels based on test IO and programs
between HDL and software languages in these aspects, where        (lines 19-21).
LLMs face challenges in bridging the gap.                            We will then elaborate in the following sections how
   The gap between HDL code to hardware PPA. The                  AGON, through its unique design of nOP functions and
chain from HDL code to PPA evaluation for hardware is             the decoupling of functionality and optimization, achieves ❶
lengthy, requiring complex and time-consuming simulation          expressive and efficient, ❷ correctness assurance, and ❸ PPA
and synthesis to obtain architectural or circuit-level PPA        optimization capabilities.
evaluations [16]. Accurately predicting PPA in the early stages
of the EDA flow is extremely challenging [40]. Additionally,
                                                                        IV. F UNCTIONALITY D ESCRIPTIONS IN AGON
the downstream optimization goals from HDL code to physical
design are diverse, usually requiring multiple iterative cycles      To bridge the gap between natural language-based specifi-
to refine the design in industrial workflows [33]. LLMs lack      cations and hardware implementation, we propose a novel in-
an understanding of the relationship between HDL code and         termediate representation (IR) named nOP functions in AGON
PPA metrics due to a lack of code-metric data pairs as training   for processor functionality definitions.
data [16], and they also cannot foresee diverse downstream           nOP function is expressive in describing instruction
optimization goals, impeding the optimization of HDL code.        functionalities. nOPs are derived from natural language de-
   In summary, to achieve efficient automated processor           scriptions in ISA documents, and considering common hard-
design, we should ❶ achieve design efficiency across diverse      ware modules. Figure 3 (a), (b), and (c) illustrate the relation-
customized applications, ❷ guarantee functional correctness       ship between ISA documents, nOPs, and nOP functions, with
with minimal human intervention, and ❸ empower hardware           the dataflow shown in Figure 3 (d), using the addi instruc-
optimization to attain comparable performance with human-         tion as an example. As shown in Table I, AGON provides
crafted processors. LLM-assisted methods unveil the glimmer       three categories of nOPs: storage-related, program counter
of automated processor design from natural language specifi-      (PC)-related, and arithmetic logic (AL)-related. Generally, the
cations to hardware implementations, while still maintaining      storage-related nOPs are used to access general registers and
some fundamental gaps. By effectively solving the problems,       memory; the PC-related nOPs are used to update the PC; and
AGON provides a feasible infrastructure for automated pro-        the AL-related nOPs include arithmetic operations, bit oper-
cessor design prototyping in the era of LLMs.                     ations, shift operations, comparison operations, interception
                                                                  and concatenation operations, and conditional assignments.
                                                                  For instructions in von Neumann architectures, these three
                   III. AGON OVERVIEW
                                                                  types of nOP cover the overall functional space of instructions,
  AGON is a comprehensive framework designed for LLM-             thus enabling combining nOPs into nOP functions to define
based processor design, addressing the aforementioned issues.     various instruction functionalities. nOPs are plug-and-play for
                                                                                                                                                                    5



 (a) ISA doc                                                                                                         TABLE I
                                                                                   N OP S IN AGON AND THEIR DESCRIPTIONS , CATEGORIZED INTO THREE
      ADDI: adds the sign-extended 12-bit immediate to register rs1.
                                                                                                               TYPES .
      Arithmetic overflow is ignored and the result is simply the low XLEN
      bits of the result.                                                          nOPs                           Descriptions
                                                                                                               Storage Related
 (b) nOP                                        (d) Dataflow representation
                                                                                   REG_READ(X)                    Returns the value of register X.
      Storage-related            REG_READ                                          REG_WRITE(X, Y)                Writes value Y to the register X.
                                 REG_WRITE               rs1           imm         MEM_READ(X, Y)                 Reads Y-bytes from memory address X.
      Arithmetic Logic-related   ADD                                               MEM_WRITE(X, Y, Z)             Writes Y-bytes Z to memory address X.
                                 SIGN_EXTEND                                                              Program Counter Related
      Program Counter-related    INC_PC                                            INC_PC(PC)                     Increases PC by 4.
                                                       reg         sign            UPDATE_PC(X)                   Updates PC to X.
                                                      read        extend           COND_UPDATE_PC(C, X, PC)       If C is 1, updates PC to X, otherwise increases
 (c) nOP function                                                                                                 PC by 4.
                                                                                                          Arithmetic Logic Related
  1    def inst_addi(rs1, imm, rd, pc):             rd                       pc    AND/OR/XOR(X, Y)               Bitwise AND/OR/XOR of X and Y.
                                                                add
  2        ext_imm =                                                               NOT(X)                         Bitwise NOT of X.
  3            SIGN_EXTEND(imm, 12, 64)                                            ADD/SUB(X, Y)                  Returns X+Y / X−Y.
  4        op1 = REG_READ(rs1)                                                     SIGNED_MUL(X, Y)               Returns Xs × Ys .
  5        result = ADD(op1, ext_imm)                           reg                SLL/SRL(X, Y)                  Logical left/right shifts X by Y bits.
                                                                         inc_pc
  6        REG_WRITE(rd, result)                               write               SRA(X, Y)                      Arithmetic right shifts X by Y bits.
  7        INC_PC(pc)                                                              SLICE(X, Y, Z)                 Returns X[Y:Z].
                                                                                   CONCAT(X, Y, Z, W)             Concatenates the Y-bits X and W-bits Z.
                                                                                   SIGN_EXTEND(X, Y, Z)           Sign-extends the Y-bits X to Z bits.
                                                                                   UNSIGN_EXTEND(X, Y, Z)         Zero-extends the Y-bits X to Z bits.
Fig. 3. Concepts and examples about nOPs, nOP functions and nOP dataflow           CMP_GE_S/U(X, Y)               If X≥s/u Y returns 1, otherwise 0.
graphs. The nOPs in (b) correspond to the operations described in the natural      CMP_GT_S/U(X, Y)               If X>s/u Y returns 1, otherwise 0.
language document in (a), and can be combined to form the nOP function in          CMP_LT_S/U(X, Y)               If X<s/u Y returns 1, otherwise 0.
(c), and the dataflow is shown in (d).                                             CMP_LE_S/U(X, Y)               If X≤s/u Y returns 1, otherwise 0.
                                                                                   CMP_NE(X, Y)                   If X̸=Y returns 1, otherwise 0.
                                                                                   CMP_EQ(X, Y)                   If X=Y returns 1, otherwise 0.
                                                                                   COND_ASSIGN(C, X, Y)           If C is 1, returns X, otherwise Y.

AGON and can be easily extended by simply providing the
function of the new nOP and its corresponding circuit module.
                                                                                                        V. P RIMITIVES IN AGON
nOP functions are written in a Pythonic manner, and an nOP
function compiler is developed to support various syntaxes,                          AGON decouples functionality and optimization, gradually
including fix-count for-loops, nested nOP calls, and built-in                     implements the nOP functions into the processor RTL design
operations on constants like +, -, and <<, etc. These features                    through a set of primitives (listed in Table II), and performs
enhance the expressiveness of using nOP functions to describe                     optimization and verification during the process. AGON ap-
instruction functionalities. nOP functions serve as an effi-                      plies rule-based transformations to implement and optimize
cient IR. When designing processors using HDL, the tight                          the processor, ensuring that the functionality of the instructions
coupling of instruction functionality design and the processor                    defined in the nOP functions remains unchanged, and only de-
architecture design results in complex HDL codes. By using                        termines how these instructions are executed on the processor,
nOP functions, one can focus on the functionality of individual                   guaranteeing process correctness. Different combinations of
instructions. These nOP functions are also executable and can                     primitives yield different processor implementations, enabling
then be combined to define the execution model of a processor                     designers to explore the design space at multiple levels. AGON
at the ISA level.                                                                 employs analytical models and cycle-accurate simulators to
                                                                                  estimate the processor’s PPA and provides PPA-aware cross-
   Moreover, nOP functions bridge the gap between HDL
                                                                                  level auto-tuning methods for automatic optimization. The
and high-level programming languages. ❶ Combining all
                                                                                  following of this section will detail the implementation of the
nOPs in a data-flow manner, nOP functions efficiently avoid
                                                                                  AGON primitives.
the need for explicit interface management between circuit
modules. Module ports are automatically connected during
the AGON synthesis stage, based on the data flow in the                           A. Instruction-level Primitives
nOP function. This also eliminates the need for HDL’s                                To perform subsequent optimizations and synthesis, we
unique sequential features, such as the blocking assignment                       first instantiate the nOP function using agon.instruction
and unique driver requirements for registers and finite state                     primitive. AGON’s built-in compiler constructs a data flow
machine definition, among others. ❷ nOPs only expose bit                          graph from the nOP function. It unrolls all fixed-count for-
width information if necessary, such as performing signal                         loops, flattens nested nOP calls, and pre-computes operations
interception (SLICE), concatenation (CONCAT), and extension                       with constants, converting variable-related operations into nOP
(SIGN/UNSIGN_EXTEND), etc. For other nOPs, input and                              calls. The instruction’s encoding format is also specified. If
output bit widths are inferred implicitly through a type system.                  the compiler encounters issues it cannot resolve, it will raise
   In summary, the above-mentioned features enhance the                           an error at this stage to help designers debug. After the
expressiveness and efficiency of nOP functions, minimize                          instantiation, with a complete data flow graph, the instructions
their usage overhead in design, and make them more suit-                          are already executable. Repeated calls can be merged using
able for LLM generation. As detailed in Section VI, LLMs                          instruction.merge primitive if specified.
can accurately generate nOP functions with minimal human                             nOPs are expressive and efficient when describing instruc-
intervention.                                                                     tion functionality; however, complexities arise when mapping
                                                                                                                                                                                       6



                           TABLE II                                                                            TABLE III
    AGON’ S SCHEDULING PRIMITIVES , INCLUDING INSTANTIATION ,                              S YNTHESIS RESULTS OF SELECTED AL- RELATED N OP S .
                OPTIMIZATION , AND VERIFICATION .
                                                                                nOP                                   area (um2 )             arrival time (ns)        slack (ns)
 Primitives                   Descriptions
                                                                                UNSIGN_EXTEND                            1037.5                      0.09                 0.41
 agon.instruction(n, e)       Instantiate the nOP function n with its           COND_ASSIGN                              1931.8                      0.18                 0.32
                              corresponding encoding format e.
 instruction.merge(c)         Merge redundant nOP call c.                       CONCAT                                   2061.4                      0.27                 0.23
 instruction.fuse(p)          Fuse nOPs into one based on pattern p.            AND                                      1805.8                      0.12                 0.38
 instruction.verify(t)        Verify the instruction based on test IO t.        OR                                       1968.1                      0.12                 0.38
 agon.isa([i_0, i_1,...])     Instantiate an ISA with a list of instructions    NOT                                      1257.5                      0.09                 0.41
                              [i_0, i_1,...].
 isa.extend(i)                Extend the ISA to support instruction i.
                                                                                XOR                                      2309.0                      0.16                 0.34
 isa.simulate(b)              Simulate the execution of benchmark
                              program b at ISA level.                                                                       rs
 isa.auto_fuse(g)             Automatically fuse nOPs across the ISA
                              with a gain of no less than threshold g.
                                                                                                                            reg
 isa.verify(t)                Verify the ISA using the test program t.
                                                                                                                           read
 agon.processor(I, c)         Instantiate a processor with ISA I and                                                                                            rs
                              configuration c.
 processor.config(c)          Configure the processor with configuration c.     1 cycle      srl         sll         srl          sll   srl        sll
                                                                                                                                                                reg
 processor.simulate(b)        Simulate the execution of benchmark
                                                                                                                                                               read
                              program b at processor level.                        1 cycle          or                      or                or
 processor.auto_config(f)     Explore the design space with target function
                              f and configure the processor.                                                                                             ror   ror     ror   1 cycle
 processor.verify(t)          Verify the processor using the test program t.              1 cycle              xor
 processor.synthesize()       Synthesize the processor to RTL design.
                                                                                                                                                         rd
                                                                                             1 cycle rd                    xor
                                                                                                                                                               xor3      1 cycle


                                                                                                Total 4 cycles              reg                                 reg  Total 2 cycles
nOPs to hardware. We focus on mapping AL-related nOPs to                                                                   write                               write

the processor’s arithmetic logic units (ALUs). Implementing a                                                              (a)                                  (b)
functional unit (FU) for each nOP type can enhance hardware
reuse: given the limited types of nOPs, complex instruction                    Fig. 4. Fusing nOPs with instruction.fuse primitive. (a) The original
functionalities can also be realized by scheduling a small range               nOP dataflow graph of instruction sha512sum0. The minimum instruction
                                                                               execution cycle delay is 4 cycles. (b) After fusing with two patterns ror and
of FUs, where the number of FU types remains independent                       xor3, the delay is reduced to 2 cycles.
of the number of instructions. However, this approach requires
allocating at least one clock cycle for each nOP and may
cause timing waste. We synthesize all AL-related nOPs using                    B. ISA-level Primitives
the 65nm technology to estimate their PPA. When setting the                       We use a set of instructions to instantiate an agon.isa,
target frequency as 2 GHz with the clock cycle being 0.5 ns,                   and we can additionally extend support for new instructions
most nOPs have too much positive timing slack, with the most                   using isa.extend primitive.
affected ones listed in Table III. This will result in excessive                  The difference between an agon.isa and a simple collec-
cycle delay in instruction execution.                                          tion of agon.instructions lies in its capability to simulate
   We design instruction.fuse primitive to fuse common                         program execution at this level. The isa.simulate primi-
nOP calling patterns into a single OP and implement it as one                  tive simulates executing one instruction at a time, determining
FU, thus the instruction execution cycle delay is shortened. We                the next instruction to execute based on the PC value after
can estimate the cycle delay optimized by only considering the                 execution. This facilitates analyzing the execution results and
total arrival time of the critical path in the pattern, as shown by            reporting the dynamic instruction counts of a program.
Equation 1, where cp(g) stands for critical path in the pattern,                  As mentioned above, fusing nOPs requires appropriate
Tarr stands for arrival time of the nOP, and Tclk stands for                   patterns, while identifying all these patterns is challenging. We
cycle time. Figure 4 illustrates an example when fusing nOPs                   propose an automatic pattern searching and fusion primitive
in an extended instruction sha512sum0. The cycle delay of                      at the ISA level. We develop a greedy PPA-aware pattern
the whole instruction before fusion is 4 cycles and is optimized               search strategy to collect patterns across the ISA, outlined
to 2 cycles when applying two fusion patterns.                                 in Algorithm 1. We traverse all subgraphs (reflecting local
   However, the fusion of nOPs creates dedicated FUs, poten-                   nOP calling relationships) in the nOP data flow graph across
tially reducing hardware reuse and increasing the processor’s                  all instructions supported by the ISA, estimating the cycle
area. Therefore, designers need to comprehensively consider                    delay after fusing with Equation 1, and identify subgraphs
the benefits of nOP fusion. In the next section, we will intro-                that bring at least gainT hreshold timing optimizations. We
duce a primitive that performs PPA-aware automatic pattern                     merge isomorphic subgraphs into a single pattern and then use
search and fusion at the ISA level.                                            a greedy approach to apply these patterns according to their
                                                                               sizes to all instructions that are supported by the ISA.
                              &P                       '                       C. Processor-level Primitives
                                   o∈cp(g) Tarr (o)
               Dcycle (g) =                                              (1)      AGON instantiates an out-of-order(OoO) processor based
                                        Tclk
                                                                               on the ISA and configures it with a set of hardware param-
                                                                               eters (as shown in Table IV). We take the nOPs within the
                                                                                                                                                     7



Algorithm 1 Collecting patterns when using the                                                   TABLE IV
isa.auto_fuse primitive.                                               T HE DESIGN SPACE FOR P R O C E S S O R . A U T O _ C O N F I G PRIMITIVE .
Input: all nOPGraphs, gain threshold gainThreshold                           Module             Parameter              Candidate value
Output: patternSet                                                           Branch             BTB size              [128, 256, 512] B
 1: subgraphs ← SUBGRAPH T RAVERSE (nOPGraphs)                              Prediction       replace policy        [lfu, fifo, random, lru]
 2: patternSet = ()                                                           Fetch            fetch width                  [4, 6, 8]
                                                                                           fetch buffer entry             [16, 32, 48]
 3: for subg in subgraphs do
                                                                             Decode          decoder width               [1, 2, 3, 4, 5]
 4:     nOPs = CRITICAL PATH(subg)                                           Execute           ROB entry              [32, 64, 128, 256]
 5:     nOPLats = { L ATENCY(nOP) for nOP in nOPs }                                        load queue entry                [8, 16, 32]
 6:     nOPCycles = { C EIL(nOPLat / cycleTime)                                            store queue entry               [8, 16, 32]
                                                                                              BJU number                      [1, 2]
 7:                              for nOPLat in nOPLats }                                     AGU number                       [1, 2]
 8:     initCycle = S UM(nOPCycles)                                                          ALU number                    [1, 2, 3, 4]
 9:     optCycle = C EIL(S UM(nOPLats) / cycleTime)                                           EXT number                   [1, 2, 3, 4]
                                                                              Cache             cache way                     [4, 8]
10:     gain ← 1 - optCycle / initCycle                                                         block size                 [32, 64] B
11:     if gain ≥ gainThreshold then                                                             L1D size               [8, 16, 32] KB
12:         patternSet.add(subg)                                                                 L2D size            [128, 256, 512] KB
                                                                                                 L3D size              [1, 2, 4, 8] MB
13:     end if
14: end for
15: return patternSet
                                                                    It is worth noting that since the instructions involve memory-
                                                                    related operations, we use initial states that can simulate
                                                                    register and memory access traces as inputs, and use the
instructions as the basic dynamic scheduling unit for the OoO       transition states after instruction execution as outputs, rather
processor. The processor dynamically executes the nOPs based        than merely passing values.
on the nOP dependencies. Compared to scheduling based on
                                                                       When instructions are instantiated to an agon.isa, AGON
instructions, this implementation better reuses FUs. AGON
                                                                    provides ISA-level simulation of a program, thereby also
supports a comprehensive OoO processor microarchitecture
                                                                    supporting verifying the design with a test program. Verifi-
design at the processor level, including a decoupled frontend, a
                                                                    cation at the ISA model level does not involve the processor’s
branch prediction mechanism, and a memory hierarchy includ-
                                                                    microarchitecture; it only verifies the functionality of the
ing multi-level caches. AGON provides a cycle-accurate OoO
                                                                    instructions in the ISA, without involving architectural details,
processor simulator that simulates the execution of benchmark
                                                                    such as branch prediction, memory hierarchy, etc.
programs, reports dynamic cycle counts, and estimates the
                                                                       After the agon.processor is instantiated, the microar-
area and power of the processor using McPAT. Designers can
                                                                    chitecture is introduced via configuration. We utilize AGON’s
explore different optimized configurations based on the PPA
                                                                    built-in simulator to fully simulate the execution of the test
reported by the simulator.
                                                                    programs on the processor, and verify the correctness at the
   However, Table IV defines a space containing over 179
                                                                    processor level, including ISA definitions and microarchitec-
million design points, making manual exploration difficult.
                                                                    ture implementations.
We further provide a processor.auto_config primitive
for automatic optimization of the configurations. This design
space exploration (DSE) process can be formally represented         E. Synthesize to RTL
as Equation 2, where x denotes a design point in the design            After the optimization and verification, we synthesize
space, represented by an array of hardware parameters, and f        the design to RTL implementations on top of the BOOM
signifies the cost function. To facilitate efficient exploration,   project [25]. We integrate nOP FUs into multifunctional units
AGON employs a parallelized Bayesian optimization algo-             to reduce register ports. For ease of implementation, we
rithm for searching.                                                temporarily only support fusing all AL-related nOPs within
        x∗ = arg min f (cycle(x), area(x), power(x))         (2)    each instruction when synthesis. The fused OPs are then au-
                 x                                                  tomatically converted to Chisel functions and integrated with
                                                                    BOOM. While instructions with more than two inputs execute
                                                                    coherently in AGON simulator, implementing them requires
D. Multi-level Verification
                                                                    significant modifications to BOOM. We defer the hardware
   Verification is crucial to the processor design. In AGON,        implementation of other fusing strategies and instructions with
we offer multi-level verification mechanisms from instruction       three or more inputs for future work.
to ISA model and down to architectural levels, utilizing test
IOs or test programs to verify the design.
   As mentioned above, after instantiating the nOP function                     VI. LLM- BASED AGON G ENERATION
into an agon.instruction, it becomes executable. Design-              AGON, through its functionality optimization decoupling
ers use instruction.verify to validate the correctness of           and nOP design, is suitable for LLMs in generating instruction
the nOP function by providing standard inputs and outputs and       descriptions. Nonetheless, since the training set of LLMs
comparing them with the execution results of the instruction.       contains no AGON-related data, we develop a framework
                                                                                                                                                             8



that employs few-shot learning, self-debugging, and sampling-        method can guarantee the correctness of LLM generation,
selection techniques to generate accurate nOP functions while        our approach avoids modifying complex HDL codes. This
minimizing the need for human effort.                                significantly reduces the need for expert involvement com-
   Figure 5 illustrates our framework for generating the nOP         pared to other LLM-assisted circuit generation methods. The
functions based on the natural language ISA documents. The           instruction set nOP functions generated through the above
starting point of this framework is the natural language spec-       steps are then sent to AGON for scheduling.
ifications of the instructions. These specifications are taken
directly from real-world ISA documents [17], [41]. These
                                                                              Inputs                  Generation                   Clustering
informal specifications have various formats and styles. Some                                                                 ×n
                                                                                                    Syntax checker
only describe the purpose of the instruction, while others




                                                                                                                          …
                                                                              ISA doc.
provide detailed information about the operations. Some may                  nOP spec.
also use pseudocode to aid in explaining functionality.                                              nOP
                                                                              3-shot                 funcs                     Select
                                                                             Examples                                                  nOP
A. Few-shot Learning                                                                                           Feedback              function
                                                                                                         LLM
   We first provide the nOP specifications (Figure 6 (a)) and                                                                                       …
nOP function regulations as prompts to the LLM. We then
require the LLM to generate the corresponding nOP function                                        AGON scheduling
according to the instruction specification, following the pro-
vided regulations. Brown et al. [42] demonstrate that LLMs           Fig. 5. The AGON’s nOP function generation method. After the nOP
are capable of few-shot learning using examples provided             functions are generated, they are sent for AGON’s scheduling.
in the prompt. Therefore, we provide the natural language
specifications of three instructions from the MIPS instruction
set, along with their corresponding hand-crafted nOP func-            You are an expert CPU designer tasked with translating instruction
                                                                      specifications from an ISA (Instruction Set Architecture) document into
tions, as examples for LLMs to perform few-shot learning,             functions using a set of predefined operators. Below is the list of allowed
one of which is presented in Figure 6 (b). We select three            operators and their descriptions:
                                                                        (1) REG_READ(X) -- Returns the 64-bits value of the register with number X.
MIPS instructions as examples to prevent overlap with RISC-             (2) …
V instructions in the target generation task, thereby ensuring        Guidelines:
a fair evaluation of our method’s generalization abilities.             1. Focus only on operations involving general registers, PC, and immediate
                                                                      values.
                                                                        2. …
B. Self-debugging                                                     Next, please translate the following specifications into functions.
                                                                                                 (a) nOP specfications
   We utilize the compiler provided in AGON to check the
syntax of nOP functions generated by LLMs and provide                 SPECIFICATION:
                                                                        Doubleword Shift Left Logical DSLL
feedback when syntax errors occur [43]. If the nOP function             …
fails the syntax check, the erroneous nOP function and the              The 64-bit doubleword contents of GPR rt are shifted left, inserting zeros
syntax check feedback are provided back to the LLM for                into the emptied bits; the result is placed in GPR rd. The bit shift count in the
                                                                      range 0 to 31 is specified by sa.
regeneration. Repeat the above process until the generated              …
nOP function passes the syntax check or the iteration times           FUNCTION:
                                                                        The value in register rt is logically left shifted by the number of bits specified
threshold is reached.                                                 by the immediate value, and the result is still 64-bit. This result is then written
                                                                      into register rd.
                                                                        def dsll(rt, imm, rd, pc):
C. Sampling and Selection                                                 op1 = REG_READ(rt)
                                                                          op2 = SLL(op1, imm)
   The output of LLMs is stochastic. To enhance the quality               REG_WRITE(rd, op2)
of the nOP functions generated by the LLM, we apply a                     INC_PC(pc)

sampling-clustering-selection mechanism proposed by Li et                                     (b) One few-shot example
al. [44]. We repeat the aforementioned generation and self-
debugging processes n times to obtain n nOP functions.               Fig. 6. Illustration of nOP specifications and few-shot examples. nOP
Subsequently, due to the nOP functions executable feature,           specifications are provided to LLM along with 3-shot examples to conduct
                                                                     few-shot learning.
we generate multiple random input states, execute each nOP
function with all initial states and obtain the transfer states as
the outputs. We cluster nOP functions based on their output
                                                                                                 VII. E XPERIMENTS
states. nOP functions that have the same output states are
grouped into the same cluster. Eventually, an nOP function           A. Experimental Setup
from the largest cluster is selected as the final output. We            We conduct detailed experiments to evaluate AGON. We
provide this clustering method instead of simply filtering           select RV64I as the base ISA and eight domain-specific appli-
nOP functions using instruction.verify primitive as                  cations as benchmarks, two of which are from the test suite
comprehensive testing IOs may not always be available.               of the RISC-V Zknh extension [17], while the remaining six
   Finally, if the nOP function generated by the above frame-        are from Nuclei-Software [45], which is a business software
work still contains errors, we correct it manually. While no         based on the RISC-V P extension [41]. The SHA256 and
                                                                                                                                                            9



                            TABLE V                                                           TABLE VI
                 AGON’ S TARGETING BENCHMARKS .                      PASS RATE COMPARISON FOR LLM- BASED GENERATION ( IN 3 TRIALS ).

                name                extended instructions              instruction       AGON        Chisel        instruction      AGON          Chisel
       k0      SHA256       sha256{sig0, sig1, sum0, sum1}                             pass@1(%)   pass@1(%)                      pass@1(%)     pass@1(%)
       k1      SHA512       sha512{sig0, sig1, sum0, sum1}                                                  RV64I
       p0     Fast Math                   clz32                      49 instructions     95.9          -
       p1   Complex Math       mulsr64, smtt32, smbt32,                                                 Zknh extension
                              smdrs32, kmxda32, pkbb32,              sha256sig0          100           0         sha256sig1          100              0
                            kwmmul, kstsa32, ksubw, clz32            sha256sum0          100           0         sha256sum1          100              0
       p2    Matrix Mult             smmul, smar64                   sha512sig0          67.7          0         sha512sig1           0               0
       p3    Matrix Add              kadd32, kaddw                   sha512sum0          100           0         sha512sum1          100              0
       p4    Matrix Sub              ksub32, ksubw                                                       P extension
       p5    Matrix Scale       pkbb32, kslra32, smmul                 kadd32             100          0             kaddw          100              67.7
                                                                       kslra32             0           0            ksub32          100               0
                                                                        ksubw             100          0            pkbb32          100              67.7
                                                                       smar64             100          0             smmul          100               0
                                                                        clz32              0           0           mulsr64          100              67.7
SHA512 benchmarks are mostly adopted hash functions in                 smtt32             100          0            smbt32          100               0
                                                                       smdrs32            100          0           kmxda32          67.7              0
cryptography. Fast Math benchmark provides a set of fast               kwmmul              0           0           kstsa32          100               0
approximation functions to sine, cosine, and square root,
and the Complex Math benchmark performs operations on                                         TABLE VII
complex data vectors. The last four benchmarks are designed         P ROCESSOR COMPLEXITY AND DEVELOPMENT EFFORT COMPARED WITH
for matrix calculations. The involved extended instructions for             OTHER LLM- ASSISTED PROCESSOR DESIGN METHODS .

these benchmarks can be found in Table V.                                           design              area (µm2 )     #instructions      debug LoC
   We utilize GPT-4 as the embedded LLM in our generation                      tiny-scale CPUs
method (Section VI) with 3-shot examples. The temperature                       Chip-Chat [28]              -                24               1896
                                                                                ChipGPT [29]              3240.8             10                9
for generation is set to 0.3. In each generation process, we              our customized processors
allow up to 3 rounds of syntax check feedback and generate                         SHA256                  9.63e6            57                 2
up to 9 samples for clustering. We evaluate the accuracy of                        SHA512                  6.47e6            57               4.67
                                                                                  Fast Math               6.42e6             53                 4
AGON generation using the pass@1 [38] metric, as shown in                       Complex Math              9.60e6             62               9.67
Equation 3, where n stands for total generation times and c                      Matrix Mult              11.61e6            54                 2
                                                                                  Matrix Add               9.96e6            54                 2
stands for the number of correct generations.                                     Matrix Sub               9.59e6            54                 2
                                        hci                                      Matrix Scale              8.54e6            55               7.33
                   pass@1 := Eproblems                      (3)
                                         n
We calculate the number of lines of code (LoC) required in          high as 0.96. Analyzing the generation of RV64I instructions,
modifying nOP functions for all instructions in a processor         we find that the LLM fails only when generating the lui
to be correctly implemented, to evaluate the minimum human          and auipc instructions, and successes in generating all other
intervention needed when using AGON.                                instructions. This proves that with the nOP function acting
   We      utilize     AGON’s       auto-tuning      primitives     as an efficient IR, AGON can correctly generate almost all
(isa.auto_fuse and processor.auto_config ) in our                   basic instructions without human intervention. For compli-
experiments to demonstrate AGON’s optimization capabilities         cated extended instructions, AGON succeeds in generating 18
and its ability to minimize human effort in processor design.       instructions without human intervention. The pass rate of nOP
The dynamic execution statistics are reported by simulating         functions also significantly surpasses that of Chisel ALU codes
the execution of the benchmarks in the AGON embedded                in all instructions except sha512sig1, where both methods fail
simulator. Based on the optimal architecture obtained from          to generate without human modification.
AGON’s auto-tuning, we implement our processor and                     We further evaluate the human effort required to modify
synthesize the generated circuit to report its accurate area.       erroneous nOP functions. The result is reported in Table VII.
All syntheses are done using a commercial EDA tool with a           We compare our results with two other works that utilize
65nm technology.                                                    LLMs to generate CPUs. We annotate the area and the
                                                                    number of supported instructions for each generated processor
B. AGON Provides Efficiency                                         to illustrate their complexity. For our design, the average
   To illustrate the efficiency of using AGON for processor         debugging line-of-code across 3 trials is reported to show de-
design, we evaluate the pass rate of LLM generating AGON            velopment effort. Chip-Chat [28] designs a CPU that supports
for describing each extended instruction, and compare it with       24 instructions through conversations with ChatGPT. The CPU
generating corresponding dedicated ALUs in Chisel, both with        area is not reported. In order to design such a tiny-scale CPU,
3-shot examples and providing the same ISA documents as in-         they require the user to interactively provide 1896 lines of
put. We also report an average pass rate for 49 RV64I standard      natural language prompts, which results in significant human
instructions. Since RV64I instructions involve memory access        overhead. In ChipGPT [29], after modifying 9 lines of the
or branch operations, their functionality cannot be described       generated Verilog code, a CPU that only supports 10 instruc-
using a single ALU; therefore, comparing them with Chisel’s         tions is designed, and unable to run real-world applications.
pass rate is not feasible.                                          Compared with their work, equipped with AGON, LLMs are
   Table VI illustrates the results. The experimental results       able to design processors that have significant advantages in
show that for the RV64I instructions, our average pass rate is as   complexity and the number of supported instructions, with
                                                                                                                                                                                                                                                       10



 lower or equivalent human interventions, and can be evaluated                                                                                  take the area of BOOM estimated by McPAT as the
 on real-world benchmarks, demonstrating AGON’s efficiency                                                                                      limitation, utilizing isa.auto_fuse(gain_th=0) and
 when designing complex processors.                                                                                                             processor.auto_config primitives to optimize the per-
                                                                                                                                                formance of ASIPs with a smaller area than BOOM. Applying
                                                                                                                                                BOOM configurations, we use our simulator to report the
 C. AGON Enables Optimization
                                                                                                                                                performance of benchmark applications compiled to RV64I
    Figure 7 shows the optimization provided by                                                                                                 running on BOOM as the baseline. Figure 8 reports the
 our     auto-tuning    primitives    (isa.auto_fuse         and                                                                                cycles and area of optimized ASIPs and BOOM under three
 processor.auto_config). We use area efficiency                                                                                                 BOOM configurations: small, large, and giga. As illustrated,
 as the optimization goal, minimizing Equation 4. The dots                                                                                      our approach surpasses BOOM’s performance in 23 out of
 represent designs that have been explored by AGON’s built-in                                                                                   24 scenarios. The average performance across all benchmarks
 DSE engine, while the darker dots indicate that they are                                                                                       is 2.35× faster than BOOM, while the average area is only
 on the Pareto front. As analyzed previously, the choice of                                                                                     79.5% that of BOOM. In scenarios with the smallest area
 different nOP fusing strategies will affect the performance                                                                                    budget (use small-BOOM’s area as the limitation), we achieve
 and area of the processors. Performing isa.auto_fuse                                                                                           an average performance improvement of 3.84× compared to
 optimization with no gain threshold requirements (i.e. all                                                                                     BOOM and a maximum improvement of 17.40× in the pro-
 nOPs are fused into one OP) makes it easier to obtain better                                                                                   cessor customized for Matrix Multiplication Benchmark (p2).
 performance by reducing cycle delays and register pressure,                                                                                    The experimental results demonstrate that utilizing AGON
 but it also leads to a larger area due to fewer hardware reuse                                                                                 achieves an end-to-end design and optimization process from
 opportunities, so the blue points tend to be distributed in                                                                                    ISA documents to processors with minimal human effort.
 the upper left of the scope. Applying no isa.auto_fuse
 design does not require excessive dedicated computational                                                                                                          Cycles BOOM          Cycles AGON          Area BOOM         Area AGON
 components, so it can achieve a smaller area. However,                                                                                                       250                                                                             28
 problems of long cycle latency and register pressure will                                                                                                                                                                                    26

 lead to lower performance, thus the red points tend to be                                                                                                    200                                                                             24

 distributed in the lower right part of the chart. Specifying a                                                                                                                                                                               22




                                                                                                                                                                                                                                                   Area (mm²)
                                                                                                                                                 Cycles (k)




                                                                                                                                                              150
                                                                                                                                                                                                                                              20
 gain threshold with a 50% cycle reduction is a compromise,
                                                                                                                                                                                                                                              18
 so the green points tend to be distributed in the middle. These                                                                                              100
                                                                                                                                                                                                                                              16
 observations are prominent in SHA512, Complex Math, and                                                                                                                                                                                      14
                                                                                                                                                               50
 Matrix Scale benchmarks.                                                                                                                                                                                                                     12
                                                                                                                                                                0                                                                             10
                                                                                                                                                                    k0 k1 p0 p1 p2 p3 p4 p5 k0 k1 p0 p1 p2 p3 p4 p5 k0 k1 p0 p1 p2 p3 p4 p5
                                           f : = cycle(x) × area(x)                                                                     (4)                                 Small                   Large                   Giga


    In summary, the results prove that the scheduling primitives                                                                                Fig. 8. The cycles and area of customized processors designed with AGON
 in AGON provide a large optimization space, and with auto-                                                                                     and BOOM under three BOOM configurations: small, large, and giga.
 tuning primitives, the designers can effectively explore the
 design space with minimal human effort.
                                                                                                                                                                                     VIII. R ELATED W ORK
                       SHA256                   SHA512                     Fast Math                           Complex Math                     A. Architecture Description Language
         13.8                           12.9                     14.7                              12.9

                                                                                                                                                   Architectural description language (ADL) is an abstraction
area (mm2)




         12.9                           12.2                     13.6                              12.2
                                                                                                                                                of hardware description language (HDL) in processor design.
         12.0                           11.6                     12.4                              11.6
                                                                                                                                                Based on the level of abstraction, it can be divided into two
         11.1                           11.0                     11.2                              11.0
                       100        125             30        45      80.0          80.8      81.6                27.5        30.0         32.5
                                                                                                                                                categories. 1) ADLs bounding to microarchitecture, including
                   cycles (k)                  cycles (k)                  cycles (k)                           cycles (k)                      nML [46], Lisa [47], etc.; 2) ADLs focusing on the description
                   Matrix Mult                 Matrix Add                  Matrix Sub                          Matrix Scale
         12.9                           12.8                     11.9                              11.9                                         of the instruction set, including ViDL [48], ASSIST [49], etc.
area (mm2)




         12.3                           12.2                     11.6                              11.6                                         Due to the absence of microarchitecture specifications in the
         11.6                           11.6                     11.3                              11.3
                                                                                                                                                description, it brings challenges to hardware mapping. Further,
         11.0                           11.0                     10.9                              11.0
                                                                                                                                                both categories require manual coding from designers, pre-
                   5         10                 33.0   34.5                33.0          34.5             32           34          36           venting the realization of fully automated design processes. To
                    cycles (k)                 cycles (k)          cycles (k)                            cycles (k)
                without auto_fuse()               auto_fuse(gain_th=0.5)                           auto_fuse(gain_th=0)                         the best of our knowledge, no previous work has synthesized
                                                                                                                                                complex out-of-order processors from ADLs.
 Fig. 7. The results of the auto-tuning for our 8 benchmark applications.
 Different colors represent different settings in isa.auto_fuse primitive,
 leading to different preferences in the Pareto front.
                                                                                                                                                B. Assisting EDA Processes with LLM
                                                                                                                                                   In addition to the aforementioned LLM-based circuit gener-
   We further compare the performance of customized                                                                                             ation works, some researchers explored employing LLM to as-
 processors designed using AGON with BOOM in area-                                                                                              sist the EDA process [50]–[52]. For example, ChipNemo [50]
 constrained scenarios. To enable a fair comparison, we                                                                                         is an engineering assistant chatbot that can generate EDA
                                                                                                                                                            11



scripts or analyze bugs. ChatEDA [51] generates code for ma-                     [11] Y. Lu, S. Liu, Q. Zhang, and Z. Xie, “Rtllm: An open-source benchmark
nipulating EDA tools based on natural language instructions.                          for design rtl generation with large language model,” arXiv preprint
                                                                                      arXiv:2308.05345, 2023.
Kande et al. [52] utilize LLM to generate security assertions to                 [12] R. Li, L. Allal, Y. Zi, N. Muennighoff, D. Kocetkov, C. Mou, M. Marone,
assist in hardware verification. These works do not involve the                       C. Akiki, J. Li, J. Chim et al., “Starcoder: May the source be with you!”
logical design of the processors and are therefore orthogonal                         Transactions on machine learning research, 2023.
                                                                                 [13] F. Zhang, B. Chen, Y. Zhang, J. Keung, J. Liu, D. Zan, Y. Mao, J.-G.
to our work.                                                                          Lou, and W. Chen, “RepoCoder: Repository-level code completion
                                                                                      through iterative retrieval and generation,” in Proceedings of the 2023
                                                                                      Conference on Empirical Methods in Natural Language Processing,
                           IX. C ONCLUSION                                            H. Bouamor, J. Pino, and K. Bali, Eds. Singapore: Association
   We propose AGON, a framework for LLM-based cus-                                    for Computational Linguistics, Dec. 2023, pp. 2471–2484. [Online].
                                                                                      Available: https://aclanthology.org/2023.emnlp-main.151
tomized processor design. AGON decouples optimization from                       [14] T. Liu, C. Xu, and J. McAuley, “Repobench: Benchmarking repository-
functionality, utilizes LLM-generated nOP functions to define                         level code auto-completion systems,” in The Twelfth International
the processor functionality, and provides a series of primitives                      Conference on Learning Representations, 2024. [Online]. Available:
                                                                                      https://openreview.net/forum?id=pPjZIOuQuF
to implement, optimize, and verify the design. We evaluate the                   [15] A. Allam and M. Shalan, “Rtl-repo: A benchmark for evaluating llms on
effectiveness of AGON by automatically designing a series of                          large-scale rtl design projects,” arXiv preprint arXiv:2405.17378, 2024.
Out-of-Order processors, customized for different applications,                  [16] R. Zhong, X. Du, S. Kai, Z. Tang, S. Xu, H.-L. Zhen, J. Hao,
                                                                                      Q. Xu, M. Yuan, and J. Yan, “Llm4eda: Emerging progress in large
with minimal human intervention. The designed processors                              language models for electronic design automation,” arXiv preprint
reach an average of 2.35 × performance improvement com-                               arXiv:2401.12224, 2023.
pared to the baseline.                                                           [17] (2023) riscv/riscv-crypto: RISC-v cryptography extensions standardi-
                                                                                      sation work. [Online]. Available: https://github.com/riscv/riscv-crypto/
   AGON aims to act as an infrastructure for processor design                         tree/main
in the era of LLMs. In the future, we plan to support: ❶ Other                   [18] C. Li, Y. Wang, H. Li, and Y. Han, “Append: Rethinking asip synthesis
parallelized architectures, such as single-instruction-multi-data                     in the era of ai,” in 2023 60th ACM/IEEE Design Automation Conference
(SIMD) and multi-core processing. ❷ More comprehensive                                (DAC). IEEE, 2023, pp. 1–6.
                                                                                 [19] (2022) riscv/riscv-v-spec: RISC-v v vector extension. [Online].
synthesis flow to support diverse target architectures. ❸ More                        Available: https://github.com/riscv/riscv-v-spec/tree/master
primitives to enhance optimization. ❹ Open-sourced AGON                          [20] A. Harris, T. Verma, S. Wei, L. Biernacki, A. Kisil, M. T. Aga,
generation benchmarks to facilitate the research in the com-                          V. Bertacco, B. Kasikci, M. Tiwari, and T. Austin, “Morpheus ii: A risc-
                                                                                      v security extension for protecting vulnerable software and hardware,”
munity.                                                                               in 2021 IEEE International Symposium on Hardware Oriented Security
                                                                                      and Trust (HOST). IEEE, 2021, pp. 226–238.
                                                                                 [21] A. Menon, S. Murugan, C. Rebeiro, N. Gala, and K. Veezhinathan,
                              R EFERENCES                                             “Shakti-t: A risc-v processor with light weight security extensions,” in
 [1] S. Shahabuddin, A. Mämmelä, M. Juntti, and O. Silvén, “Asip for 5g            Proceedings of the Hardware and Architectural Support for Security and
     and beyond: Opportunities and vision,” IEEE Transactions on Circuits             Privacy, 2017, pp. 1–8.
     and Systems II: Express Briefs, vol. 68, no. 3, pp. 851–857, 2021.          [22] J. Chen, D. Li, Z. Mi, Y. Liu, B. Zang, H. Guan, and H. Chen, “Duvisor:
 [2] K. Van Renterghem, D. Verhulst, S. Verschuere, P. Demuytere, J. Van-             a user-level hypervisor through delegated virtualization,” arXiv preprint
     dewege, and X.-Z. Qiu, “A scalable network asip enabling flow aware-             arXiv:2201.09652, 2022.
     ness in ethernet access,” in 2006 International Conference on Field         [23] J. Zhang and J. Li, “Eniad: A reconfigurable near-data processing
     Programmable Logic and Applications. IEEE, 2006, pp. 1–4.                        architecture for web-scale ai-enriched big data service,” in 2021 IEEE
 [3] M. De Nil, L. Yseboodt, F. Bouwens, J. Hulzink, M. Berekovic,                    Hot Chips 33 Symposium (HCS). IEEE, 2021, pp. 1–8.
     J. Huisken, and J. van Meerbergen, “Ultra low power asip design for         [24] M. Blott, T. B. Preußer, N. J. Fraser, G. Gambardella, K. O’brien,
     wireless sensor nodes,” in 2007 14th IEEE International Conference on            Y. Umuroglu, M. Leeser, and K. Vissers, “Finn-r: An end-to-end deep-
     Electronics, Circuits and Systems. IEEE, 2007, pp. 1352–1355.                    learning framework for fast exploration of quantized neural networks,”
 [4] H.-C. Liao, M. Asri, T. Isshiki, D. Li, and H. Kunieda, “A high level            ACM Transactions on Reconfigurable Technology and Systems (TRETS),
     design of reconfigurable and high-performance asip engine for image              vol. 11, no. 3, pp. 1–23, 2018.
     signal processing,” IEICE Transactions on Fundamentals of Electronics,      [25] J. Zhao, B. Korpan, A. Gonzalez, and K. Asanovic, “Sonicboom: The
     Communications and Computer Sciences, vol. 95, no. 12, pp. 2373–                 3rd generation berkeley out-of-order machine,” in Fourth Workshop on
     2383, 2012.                                                                      Computer Architecture Research with RISC-V, vol. 5, 2020, pp. 1–7.
 [5] Z. Liu, K. Dickson, and J. V. McCanny, “Application-specific instruction    [26] K. Asanović, R. Avizienis, J. Bachrach, S. Beamer, D. Biancolin,
     set processor for soc implementation of modern signal processing                 C. Celio, H. Cook, D. Dabbelt, J. Hauser, A. Izraelevitz, S. Karandikar,
     algorithms,” IEEE Transactions on Circuits and Systems I: Regular                B. Keller, D. Kim, J. Koenig, Y. Lee, E. Love, M. Maas, A. Magyar,
     Papers, vol. 52, no. 4, pp. 755–765, 2005.                                       H. Mao, M. Moreto, A. Ou, D. A. Patterson, B. Richards, C. Schmidt,
 [6] J. F. Eusse, R. Leupers, G. Ascheid, P. Sudowe, B. Leibe, and T. Sadasue,        S. Twigg, H. Vo, and A. Waterman, “The rocket chip generator,”
     “A flexible asip architecture for connected components labeling in               Tech. Rep. UCB/EECS-2016-17, Apr 2016. [Online]. Available: http:
     embedded vision applications,” in 2014 Design, Automation & Test in              //www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-17.html
     Europe Conference & Exhibition (DATE). IEEE, 2014, pp. 1–6.                 [27] A. Izraelevitz, J. Koenig, P. Li, R. Lin, A. Wang, A. Magyar, D. Kim,
 [7] Y. Xu, Z. Yu, D. Tang, G. Chen, L. Chen, L. Gou, Y. Jin, Q. Li, X. Li,           C. Schmidt, C. Markley, J. Lawson et al., “Reusability is firrtl ground:
     Z. Li et al., “Towards developing high performance risc-v processors             Hardware construction languages, compiler frameworks, and transforma-
     using agile methodology,” in 2022 55th IEEE/ACM International Sym-               tions,” in 2017 IEEE/ACM International Conference on Computer-Aided
     posium on Microarchitecture (MICRO). IEEE, 2022, pp. 1178–1199.                  Design (ICCAD). IEEE, 2017, pp. 209–216.
 [8] J. Bachrach, H. Vo, B. Richards, Y. Lee, A. Waterman, R. Avižienis,        [28] J. Blocklove, S. Garg, R. Karri, and H. Pearce, “Chip-chat:
     J. Wawrzynek, and K. Asanović, “Chisel: constructing hardware in a              Challenges and opportunities in conversational hardware design,”
     scala embedded language,” in Proceedings of the 49th Annual Design               in 2023 ACM/IEEE 5th Workshop on Machine Learning for
     Automation Conference, 2012, pp. 1216–1225.                                      CAD (MLCAD). IEEE, sep 2023. [Online]. Available: https:
 [9] (2024) Spinalhdl/spinalhdl: Scala based hdl. [Online]. Available:                //doi.org/10.1109%2Fmlcad58807.2023.10299874
     https://github.com/SpinalHDL/SpinalHDL                                      [29] K. Chang, Y. Wang, H. Ren, M. Wang, S. Liang, Y. Han, H. Li,
[10] S. Lahti, P. Sjövall, J. Vanne, and T. D. Hämäläinen, “Are we there          and X. Li, “Chipgpt: How far are we from natural language hardware
     yet? a study on the state of high-level synthesis,” IEEE Transactions            design,” 2023.
     on Computer-Aided Design of Integrated Circuits and Systems, vol. 38,       [30] S. Thakur, B. Ahmad, Z. Fan, H. Pearce, B. Tan, R. Karri, B. Dolan-
     no. 5, pp. 898–911, 2019.                                                        Gavitt, and S. Garg, “Benchmarking large language models for auto-
                                                                                                                                                          12



     mated verilog rtl code generation,” in 2023 Design, Automation & Test        [52] R. Kande, H. Pearce, B. Tan, B. Dolan-Gavitt, S. Thakur, R. Karri, and
     in Europe Conference & Exhibition (DATE). IEEE, 2023, pp. 1–6.                    J. Rajendran, “Llm-assisted generation of hardware assertions,” arXiv
[31] M. Liu, N. Pinckney, B. Khailany, and H. Ren, “Verilogeval: Evaluating            preprint arXiv:2306.14027, 2023.
     large language models for verilog code generation,” in 2023 IEEE/ACM
     International Conference on Computer Aided Design (ICCAD). IEEE,
     2023, pp. 1–8.
[32] K. Chang, K. Wang, N. Yang, Y. Wang, D. Jin, W. Zhu, Z. Chen, C. Li,
     H. Yan, Y. Zhou et al., “Data is all you need: Finetuning llms for chip
     design via an automated design-data augmentation framework,” arXiv
     preprint arXiv:2403.11202, 2024.
[33] Z. PEI, H. Zhen, M. Yuan, Y. Huang, and B. Yu, “Betterv:
     Controlled verilog generation with discriminative guidance,” in Forty-
     first International Conference on Machine Learning, 2024. [Online].
     Available: https://openreview.net/forum?id=jKnW7r7de1
[34] N. F. Liu, K. Lin, J. Hewitt, A. Paranjape, M. Bevilacqua, F. Petroni, and
     P. Liang, “Lost in the middle: How language models use long contexts,”
     Transactions of the Association for Computational Linguistics, vol. 12,
     pp. 157–173, 2024.
[35] S. Liu, W. Fang, Y. Lu, Q. Zhang, H. Zhang, and Z. Xie, “Rtlcoder:
     Outperforming gpt-3.5 in design rtl generation with our open-source
     dataset and lightweight solution,” arXiv preprint arXiv:2312.08617,
     2023.
[36] M. Gautschi, P. D. Schiavone, A. Traber, I. Loi, A. Pullini, D. Rossi,
     E. Flamand, F. K. Gürkaynak, and L. Benini, “Near-threshold risc-v core
     with dsp extensions for scalable iot endpoint devices,” IEEE transactions
     on very large scale integration (VLSI) systems, vol. 25, no. 10, pp. 2700–
     2713, 2017.
[37] L. Zhong, Z. Wang, and J. Shang, “Ldb: A large language model
     debugger via verifying runtime execution step-by-step,” arXiv preprint
     arXiv:2402.16906, 2024.
[38] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan,
     H. Edwards, Y. Burda, N. Joseph, G. Brockman et al., “Evaluating large
     language models trained on code,” arXiv preprint arXiv:2107.03374,
     2021.
[39] X. Yao, H. Li, T. H. Chan, W. Xiao, M. Yuan, Y. Huang, L. Chen, and
     B. Yu, “Hdldebugger: Streamlining hdl debugging with large language
     models,” arXiv preprint arXiv:2403.11671, 2024.
[40] N. Wu and Y. Xie, “A survey of machine learning for computer
     architecture and systems,” ACM Computing Surveys (CSUR), vol. 55,
     no. 3, pp. 1–39, 2022.
[41] (2022) riscv/riscv-p-spec: RISC-v packed SIMD extension. [Online].
     Available: https://github.com/riscv/riscv-p-spec/tree/master
[42] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal,
     A. Neelakantan, P. Shyam, G. Sastry, A. Askell et al., “Language mod-
     els are few-shot learners,” Advances in neural information processing
     systems, vol. 33, pp. 1877–1901, 2020.
[43] X. Chen, M. Lin, N. Schärli, and D. Zhou, “Teaching large language
     models to self-debug,” arXiv preprint arXiv:2304.05128, 2023.
[44] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond,
     T. Eccles, J. Keeling, F. Gimeno, A. Dal Lago et al., “Competition-
     level code generation with alphacode,” Science, vol. 378, no. 6624, pp.
     1092–1097, 2022.
[45] (2023) Nuclei microcontroller software interface standard. [Online].
     Available: https://github.com/Nuclei-Software/NMSIS
[46] J. Van Praet, D. Lanneer, W. Geurts, and G. Goossens, “nml: A
     structural processor modeling language for retargetable compilation and
     asip design,” in Processor Description Languages. Elsevier, 2008, pp.
     65–93.
[47] O. Schliebusch, A. Hoffmann, A. Nohl, G. Braun, and H. Meyr,
     “Architecture implementation using the machine description language
     lisa,” in Proceedings of ASP-DAC/VLSI Design 2002. 7th Asia and
     South Pacific Design Automation Conference and 15h International
     Conference on VLSI Design. IEEE, 2002, pp. 239–244.
[48] R. Dreesen, “Vidl: A versatile isa description language,” in 2012
     IEEE 19th International Conference and Workshops on Engineering of
     Computer-Based Systems. IEEE, 2012, pp. 222–231.
[49] G. Liu, J. Primmer, and Z. Zhang, “Rapid generation of high-quality
     risc-v processors from functional instruction set specifications,” in 2019
     56th ACM/IEEE Design Automation Conference (DAC), 2019, pp. 1–6.
[50] M. Liu, T.-D. Ene, R. Kirby, C. Cheng, N. Pinckney, R. Liang, J. Alben,
     H. Anand, S. Banerjee, I. Bayraktaroglu et al., “Chipnemo: Domain-
     adapted llms for chip design,” arXiv preprint arXiv:2311.00176, 2023.
[51] H. Wu, Z. He, X. Zhang, X. Yao, S. Zheng, H. Zheng, and B. Yu,
     “Chateda: A large language model powered autonomous agent for eda,”
     IEEE Transactions on Computer-Aided Design of Integrated Circuits
     and Systems, 2024.
