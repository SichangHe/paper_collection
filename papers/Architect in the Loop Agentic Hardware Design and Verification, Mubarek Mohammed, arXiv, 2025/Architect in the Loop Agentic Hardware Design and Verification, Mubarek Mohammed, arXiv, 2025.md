                                                  Architect in the Loop Agentic Hardware
                                                          Design and Verification
                                                                                         Mubarek Mohammed
                                                                                    Western Washington University
                                                                                         Bellingham, WA USA
                                                                                        mohammm6@wwu.edu
arXiv:2512.00016v1 [cs.AR] 19 Oct 2025




                                            Abstract—The ever increasing complexity of the hard-        barrier to entry for hardware design, and accelerate the
                                         ware design process demands improved hardware design           critical design verification loop.
                                         and verification methodologies. With the advent of gen-
                                         erative AI various attempts have been made to automate            However, moving from single file code generation
                                         parts of the design and verification process. Large language
                                                                                                        to agentic, system-level design introduces significant
                                         models (LLMs) as well as specialized models generate hdl
                                         and testbenches for small components, having a few leaf        challenges related to maintaining architectural integrity,
                                         level components. However, there are only a few attempts       managing complex dependencies, and ensuring semantic
                                         to automate the entire processor design process. Hard-         consistency across dozens of files. Recent work such as
                                         ware design demands hierarchical and modular design            AutoChip [2] and other end-to-end synthesis frameworks
                                         processes. We utilized this best practice systematically and
                                                                                                        [3] have made significant strides, particularly in high-
                                         effectively. We propose agentic automated processor design
                                         and verification with engineers in the loop. The agent         level synthesis (HLS) and domain-specific accelerator
                                         with optional specification tries to break down the design     design. Yet, a gap remains in understanding the prac-
                                         into sub-components, generate HDL and cocotb tests,            tical capabilities and limitations of agentic systems for
                                         and verifies the components involving engineer guidance,       general-purpose, register-transfer level (RTL) CPU de-
                                         especially during debugging and synthesis. We designed
                                                                                                        sign, a domain that demands attention to detail, from
                                         various digital systems using this approach. However, we
                                         selected two simple processors for demonstration purposes      instruction set architecture (ISA) to microarchitectural
                                         in this work. The first one is a LEGv8 like a simple           data paths.
                                         processor verified, synthesized and programmed for the
                                         DE-10 Lite FPGA. The second one is a RISC-V like 32-              This case study investigates a practical application of
                                         bit processor designed and verified in similar manner          this emerging technology through a framework we term
                                         and synthesized. However, it is not programmed into the        the ”Blueprint-Driven Agent”. We tasked an AI agent
                                         DE-10 Lite. This process is accomplished usually using
                                         around a million inference tokens per processor, using         with several complete design challenges of increasing
                                         a combination of reasoning (e.g gemini-pro) and non-           complexity: a simple single-cycle LEGv8-style proces-
                                         reasoning models (eg. gpt-5-mini) based on the complexity      sor, a synthesizable 32-bit RISC-V core, a pipelined
                                         of the task. This indicates that hardware design and           LEGv8 processor, and others(not reported in this work).
                                         verification experimentation can be done cost effectively      The methodology was rooted in a blueprint-driven ap-
                                         without using any specialized hardware. The approach is
                                         scalable, we even attempted system-on-chip, which we want      proach, where the AI first generates a high-level JSON
                                         to experiment in our future work.                              specification, defining the system’s architecture, which it
                                            Index Terms—Agentic Design, Hardware Description            then uses to create, verify, and self-correct the necessary
                                         Language, Architecture, RISC-V, SystemVerilog, LLM,            HDL components by using cocotb testing.
                                         FPGA, Design Automation
                                                                                                           The objective was to rigorously assess the AI’s effi-
                                                            I. I NTRODUCTION                            cacy not just in localized code generation, but in its abil-
                                            The domain of digital systems design, traditionally         ity to compose a complex, functional, and synthesizable
                                         characterized by long development cycles, extensive            system. While initial results in component generation
                                         manual effort, and a high barrier to entry, is poised          and verification were impressive, system-level verifica-
                                         for transformation by advances in Artificial Intelligence      tion invariably revealed critical failures. This paper doc-
                                         [1]. Large Language Model (LLM) based AI agents                uments the collaborative human-AI debugging journey,
                                         now possess the capability to understand natural lan-          providing a granular analysis of the agent’s limitations,
                                         guage specifications and generate hardware description         and offers a refined ”Architect-in-the-Loop” workflow as
                                         languages (HDLs) like SystemVerilog and VHDL. This             a powerful and economically viable paradigm for future
                                         promises to automate tedious coding tasks, lower the           hardware design.
                  II. R ELATED W ORKS                              III. T HE AI-D RIVEN D ESIGN M ETHODOLOGY
                                                                  Our framework is designed to emulate and enhance
  In this section we discuss the major works in this area.     a modern, specification-driven workflow. It leverages
                                                               an AI agent for code generation, verification, and self-
A. Verilog Generation and Evaluation                           correction, all under the strategic supervision of a human
                                                               architect. The core components of this methodology are
   There are several attempts to fine tune LLMs to better      outlined below.
generate Verilog hdl code. Some of them are BetterV
[4], VerilogEval [6], and RTL coder [5]. The focus of
these works is to evaluate the models capability for small
modules. This is close to the leaf level components or
components with few subcomponents. Even though we
use LLMs to generate SystemVerilog code components,
the strength of our work comes from how we hierarchi-
cally build complex digital systems including processors.
   In our work, we mainly use LLMs with a combination
of reasoning models (for planning, debugging/fix, and
integration) and non-reasoning models (for code and
testbench generation).

B. AI Assisted Digital Systems Design
   The work very close to ours conceptually is Chip-
Chat [1]. They tried to build a small processor from
scratch by chatting with LLMs. An experienced engineer
(the author) prompted the LLM to give the required
modules, debugged it, and iteratively improved it to
generate a working processor. Chip-Chat purely involves
the engineer and chat bot, with parts of the code being
broken up into separate chats.They even continued to the
tiny-tapeout process for manufacturing. In our case, we
automate the hierarchical and modular design process.
Another work, AutoChip [2] used LLMs to build small
digital circuits by incorporating self-feedback loop, very
similar to ours at the component level. However, Au-
toChip does not create more complicated components
and hierarchical components.
   Our work partially or completely automates the pro-         Fig. 1: Agentic Digital Design Flow with Human-in-the-
cess through agentic digital systems design. The ex-           Loop Feedback and Approval at Each Stage
periment in this work is done considering the human
engineer playing a critical role in the digital systems           For sample code look at the appendix. The details are
design process such as a simple processor development          also hosted on github. 1
process. The engineer/architect can provide specification      A. Phase 1: The Blueprint as a Formal Specification
in terms of JSON blueprint as well as a text prompt.
                                                                  The foundation of each project is a JSON blueprint,
Once the agent starts, if a component fails the agent
                                                               which can either be provided by a human architect
initiates a self-correction loop. However, it waits for the
                                                               or generated by the agent from a high-level natural
engineer to provide feedback and approves the fix. The
                                                               language prompt. This document serves as the formal,
engineer at this stage can edit the failed hdl or test files
                                                               machine-readable specification, defining:
and let the agent continue. In a separate work of ours
                                                                  • Global project parameters (e.g., data widths, mem-
for experimental purposes, not published, we even let
                                                                    ory depths).
the agent run end-to-end without human intervention just
                                                                  • An optional SystemVerilog package for defining a
starting from blueprint or prompt specification. However,
                                                                    shared Instruction Set Architecture (ISA).
even in this case the engineer has the option to edit code
especially if the agent is struggling to fix some issues.        1 https://github.com/mmubarek/eda/tree/main/paper1
  •  A hierarchical list of all required system compo-              agent then re-verifies the edited design to ensure
     nents, their individual interfaces (ports and param-           correctness before allowing it to proceed.
     eters), and their inter-dependencies.                        This iterative, human-in-the-loop process ensures that
A key observation, which became central to later debug-        every component is both structurally correct and func-
ging efforts, was that initial agent-generated blueprints      tionally validated before integration.
often omitted a formal ISA definition or created con-             Once all sub-modules pass their unit tests, the orches-
tradictory parameterizations. Our refined methodology          trator enters the integration phase, generating a top-level
(Figure 2) now employs a highly structured prompt that         module that instantiates and interconnects the verified
explicitly guides the agent to produce a complete and          components. This step is itself subject to the same
non-contradictory blueprint as the first step.                 linting, verification, and human approval loops, since
TABLE I: Key Parameters Defined in an Example AI-              interface mismatches or wiring errors commonly arise
Generated Blueprint                                            during integration.

                  Parameter                                    C. Phase 3: System-Level Verification
                  DATA_WIDTH
                  ADDRESS_WIDTH                                   With all components integrated, the agent generates
                  INSTRUCTION_WIDTH                            a cycle-accurate top-level cocotb testbench. The ver-
                  OPCODE_WIDTH
                  REG_ADDR_WIDTH
                                                               ification strategy follows a golden model approach: a
                                                               Python implementation of the ISA maintains an internal
                                                               model of the processor’s architectural state (registers
   In additon to these parameters, ISA related parameters
                                                               and memory). For each executed instruction, the golden
are defined in the blueprint.
                                                               model predicts the expected state updates, which are
B. Phase 2: Component Generation, Integration, and             then compared against the DUT’s debug outputs at every
Self-Correction                                                cycle.
   Using the blueprint, the agent’s orchestrator processes        This strategy uncovers subtle, cross-module issues
each component according to its dependency graph. For          such as pipeline hazards, bus arbitration errors, or timing
each sub-module, the following workflow is applied:            mismatches that are not visible at the unit-test level. Fail-
  1) HDL and Testbench Generation: The agent gen-              ures again trigger the same AI self-correction loop with
     erates a synthesizable SystemVerilog module and a         mandatory human approval, ensuring both automation
     corresponding cocotb testbench.                           and accountability.
  2) Pre-Flight Linting (Verilator): A lightweight com-           Only after passing system-level verification is the
     pilation check using Verilator in linting mode is         design returned to the engineer for FPGA synthesis,
     performed first to efficiently detect syntax and struc-   hardware debugging, and physical validation. This final
     tural errors.                                             step ensures that ultimate responsibility and fine-grained
     • If the linting passes, the workflow proceeds to
                                                               optimization remain in human hands, even as the agent
        functional verification.                               automates the majority of the design flow.
     • If the linting fails, the agent analyzes the error
        log, proposes a fix, and submits it for human              IV. D EBUGGING AND ROOT C AUSE A NALYSIS
        approval. Upon approval, the design is retried.
                                                                 Debugging and analysis continues for the top level
  3) Functional Verification (cocotb): If linting suc-         module if there is failure. This initiates an iterative
     ceeds, the sub-module is tested against its cocotb        debugging process that reveals a pattern of agent failure
     unit testbench. Failures here typically expose be-        modes. This process was repeated across other designs,
     havioral or semantic errors.                              confirming our analysis. Table II provides a detailed log
     • As with linting, testbench failures trigger a self-     of representative bugs discovered, their root cause, and
        correction loop: error analysis → candidate fix        the corresponding solution, which often involved refining
        → human approval → re-verification.                    the agent’s underlying prompting strategies.
     • The number of retry attempts is bounded by
        a configurable limit (e.g., three attempts per
                                                                   V. A NALYSIS OF AGENTIC C APABILITIES AND
        component). If the limit is reached, the human
                                                                                  L IMITATIONS
        engineer may step in directly to provide manual
        edits.                                                    This case study, in our view, provides a snapshot of the
  4) Human Overrides: At any stage, the engineer               current capabilities and, more importantly, the systemic
     can manually modify the HDL or testbench. The             limitations of LLM agents in digital design.
TABLE II: Summary of observed errors, root causes, and           understanding of how components must interact. This
applied solutions in LLM-assisted hardware design.               ”semantic gap” is a known challenge in AI-driven code
 Error                Cause                Solution              generation and is particularly acute in hardware design
 Inconsistent ISA     LLM generated        Refined prompting     due to the tight, bit-level coupling between modules.
 implementations      mismatched           with explicit ISA     This manifested in several critical ways, summarized in
                      instruction          tables; enforced      Table III.
                      encodings across     consistency via
                      modules              shared JSON
                                           blueprint
                                                                 TABLE III: Critical Errors Encountered in Final Phases
 Parameter            Uncoordinated        Centralized            Error Category        Description of Is-      Resolution / Fix
 propagation errors   parameter            parameter file and                           sue
                      definitions across   enforced               Missing Initializa-   Instruction memory      Created          and
                      modules              inheritance through    tion File             lacked a proper         integrated          a
                                           JSON schema                                  .hex file, leading      correctly formatted
 Incorrect handling   Agent omitted or     Prompted agent to                            to failed instruction   .hex file, then
 of SystemVerilog     mismatched           generate package                             fetch.                  re-ran verification.
 packages             imports in           stubs first, then      Cascading   Data      Fixing the missing      Performed
                      integrated designs   ensured imports        Width Mismatches      .hex file exposed       systematic width
                                           during integration.                          hidden inconsisten-     alignment across
                                           Later, used only                             cies in data widths     modules, updated
                                           centeralized                                 across modules.         bus     connections,
                                           parameters.                                                          and         extended
 Misaligned           Agent-generated      Human-in-the loop                                                    testbench coverage.
 memory interfaces    load/store modules   debugging and          Inconsistent   ISA    ISA instruction en-     Standardized
                      had width            prompt                 Encoding              codings were in-        instruction
                      mismatches           improvement                                  consistently imple-     encodings      using
 Clock related        Agent failed to      Human-in-the-loop                            mented across de-       a single JSON
 errors               insert               correction                                   coder and execu-        ISA specification,
                      synchronization                                                   tion modules.           regenerated RTL
                      logic for signals                                                                         and testbenches.



A. Strengths                                                          VI. E CONOMIC AND F UTURE I MPLICATIONS
  • Syntactic Correctness and Boilerplate Genera-                A. A Highly Cost-Effective Collaboration
    tion: The agent excelled at generating syntactically            A remarkable aspect of this project was its economic
    correct SystemVerilog and Python. It handled the             efficiency. The whole design, verification, and the de-
    boilerplate of module definitions, port lists, and           bugging process for multiple complex processors was
    testbench structure well, saving significant manual          completed by utilizing reasoning models for planning
    effort.                                                      and integration, and non-reasoning model for test code
  • Blueprint Adherence: It correctly parsed the JSON            generation at component level, a simple processor can
    blueprint to define module names, parameters, and            be completed in less than a million tokens. For context,
    port widths, demonstrating a strong grasp of struc-          this stands in stark contrast to the significant engineering
    tured input and the ability to follow a formal               man-hours and associated costs typically required for
    specification. In some cases, the blueprint (JSON)           such tasks. In this framework, the AI agent plays the role
    is more than 1300 lines of code.                             of a junior engineer, automating more than 80% of the
  • Modular Decomposition and Localized Reason-                  repetitive coding and first-pass verification. Meanwhile,
    ing: The initial design breakdown into standard,             the human architect remains central—providing high-
    single-responsibility components was excellent en-           level guidance, validating decisions, and ensuring that
    gineering practice. Within the context of a single           the design intent is faithfully captured. The result is not
    module, the agent demonstrated a strong ability to           only cost-effective but also aligned with democratizing
    implement the required logic based on its descrip-           access to sophisticated hardware design workflows.
    tion.
                                                                 B. The Path Forward: The Architect-in-the-Loop
B. Limitations: The Semantic Cohesion Gap                          This work strongly suggests that the most promising
   The core failures of the agent, across all tested designs,    near-term trajectory for AI in hardware design is not
stemmed from a single, profound limitation: a lack of            complete autonomy, but a sophisticated Architect-in-the-
holistic semantic cohesion. While capable of reasoning           Loop model. In this paradigm, the human engineer is
about a task in isolation (e.g., ”write an ALU”), the            not simply a reviewer of the AI’s output but an active
agent struggles to maintain a consistent, system-wide            collaborator from the earliest stages of design.
                                                                                   VII. C ONCLUSION
                                                                The experiment of designing multiple complex proces-
                                                             sors using a blueprint-driven AI agent was a qualified
                                                             success. It demonstrated the immense potential of this
                                                             approach to dramatically accelerate hardware develop-
                                                             ment by automating the most labor-intensive aspects
                                                             of RTL and testbench generation. The agent proved
                                                             capable of creating complex, synthesizable designs that
                                                             successfully targetted FPGA hardware.
                                                                However, it also starkly highlighted the ”semantic
                                                             cohesion gap” that prevents current models from reliably
                                                             composing complex systems without human oversight.
                                                             The agent, while proficient at localized tasks, lacks the
                                                             holistic, system-wide reasoning that is the hallmark of
                                                             an experienced engineer.
                                                                The most valuable takeaway is the demonstrated vi-
                                                             ability and economic efficiency of the human-AI col-
Fig. 2: Refined Agentic Digital Design Flow with
                                                             laborative model. The AI acts as a tireless, fast, and
Human-in-the- Loop
                                                             exceptionally low-cost junior engineer, while the human
                                                             provides the architectural wisdom and strategic debug-
   Crucially, human oversight begins at the specification    ging insight that is currently irreplaceable. The future of
level: ambiguous or incomplete ISAs, architectural pa-       AI in digital design is not about replacing the architect,
rameters, or high-level constraints must be clarified by     but about providing them with the most powerful co-
the architect before the agent proceeds. This ensures that   pilot, turning weeks of work into days, and days into
the agent operates with a complete and unambiguous           hours.
blueprint. The human architect also provides strategic de-
bugging insight, approves or rejects AI-generated fixes,
and may directly modify RTL when necessary, with the                                   R EFERENCES
agent handling re-verification.
   Looking ahead, realizing this vision requires next-        [1] H. Fu, H. G. Gerez, et al. (2024). Chip-Chat: A Large Language
                                                                  Model for Conversational Hardware Design. arXiv:2402.13324.
generation agents to evolve in three key directions:
                                                              [2] Z. Liu, H. G. Gerez, et al. (2023). AutoChip: A LLaMA-based
  1) Demand Complete Specifications: Agents must be               Agent for Chip Design. arXiv:2311.09228.
     trained to detect missing or contradictory elements      [3] B. Li, Y. G. Gerez, et al. (2024). Towards Automatic and
                                                                  Agile AI/ML Accelerator Design with End-to-End Synthesis. In
     in high-level specifications and formally request            Proceedings of the 2024 ACM/SIGDA International Symposium
     clarification, rather than making assumptions that           on Field-Programmable Gate Arrays.
     can cascade into architectural flaws.                    [4] Z. Pei, et al., ”BetterV: Controlled Verilog Generation with Dis-
                                                                  criminative Guidance,” arXiv preprint arXiv:2402.03375, 2024.
  2) Perform Cross-Module Semantic Analysis:                  [5] S. Liu, et al., ”RTLCoder: Outperforming GPT-3.5 in Design
     Agents should employ lightweight static and                  RTL Generation with Our Open-Source Dataset and Lightweight
     semantic checks to ensure interface compatibility,           Solution,” arXiv preprint arXiv:2312.08617, 2023.
                                                              [6] M. Liu, N. Pinckney, B. Khailany, and H. Ren, ”VerilogEval:
     parameter consistency, and adherence to design               Evaluating Large Language Models for Verilog Code Genera-
     rules across the codebase before running expensive           tion,” arXiv preprint arXiv:2309.07544, 2023.
     simulations.                                             [7] Cocotb Contributors, cocotb documentation, [Online]. Available:
  3) Integrate with Formal Methods: Beyond simu-                  https://docs.cocotb.org/. (Accessed: Aug. 26, 2025).
                                                              [8] W.           Snyder,         Verilator,[Online].       Available:
     lation, agents should be capable of generating Sys-          https://github.com/verilator/verilator, 2023 (Accessed: August
     temVerilog Assertions (SVA) or formal properties to          26, 2025)
     express inferred design intent, enabling exhaustive
     verification with formal tools.                                                     A PPENDIX
   Taken together, these directions position the human ar-
                                                                           C OMPLETE S UPPORTING DATA
chitect as the source of design intent, while empowering
the AI agent to act as a capable, efficient, and verifi-       You will find the complete blueprint, hdl files,
able collaborator. This balance preserves accountability,    cocotb test, scripts to simulate the digital system
reduces cost barriers, and opens a path toward broader       at https://github.com/mmubarek/eda/tree/main/paper1.
participation in advanced hardware design.                   Sample code is provided in the next appendices.
          A PPENDIX : T OOLS AND D EBUGGING P ROCESS            19         "dependencies": [],
                                                                20         "status": "Validating",
     A. Tools                                                   21         "interface": [
        For simulation, we utilized cocotb together with 22                  {
                                                             23                 "name": "clk",
     verilator. We developed both component-level and 24                        "direction": "input",
     top-level cocotb tests to ensure functionality and cor- 25                 "width": 1
     rectness across the design hierarchy.                   26              },
                                                                27           {
     B. Debugging Process: Synthesis and Experimentation 28                     "name": "rst",
                                                                29              "direction": "input",
        One of the major issues encountered was the absence 30                  "width": 1
     of a hex file for the instruction memory. To resolve this, 31           },
                                                                32           {
     we created the required hex file, integrated it into the 33                "name": "pc_next_addr",
     design, and retested the code.                             34              "direction": "input",
        When compiling for the FPGA, we also needed to 35                       "width": "ADDRESS_WIDTH"
                                                                36           },
     provide a dedicated top-level module that wired the 37                  {
     design components to the FPGA peripherals. This modi- 38                   "name": "pc_out",
     fication introduced cascading issues, primarily related to 39              "direction": "output",
                                                                40              "width": "ADDRESS_WIDTH"
     mismatched data widths across modules, which required 41                }
     significant debugging. After carefully resolving these 42             ]
     mismatches, both verification and synthesis completed 43          },
                                                                44 .
     successfully.                                              45 .
        The updated design was then iteratively tested using 46 .
     cocotb: each modification was rerun, verified, and 47 {
                                                                48         "name": "Legv8SingleCycleProcessor",
     debugged through simulation until stable results were 49              "file": "legv8_single_cycle_processor.sv"
     achieved.                                                         ,
                                                                50       "description": "Top-level module for the
     C. Processor Development Notes                                    simple single-cycle Legv8 processor,
                                                                       integrating all sub-components.",
        Using our HDL generation tool, we created a 32- 51               "dependencies": [
     bit RISC-V processor. During early debugging stages, 52                "ProgramCounter",
     we noticed recurring issues. Both the RISC-V and 53                    "InstructionMemory",
                                                              54            "ControlUnit",
     LEGv8 implementations successfully passed cocotb 55                    "RegisterFile",
     tests; however, neither included a preloaded hex file 56               "ALU",
     in their instruction memory. Instead, cocotb injected 57               "DataMemory",
                                                              58            "SignExtender",
     instructions directly at the top-level testbench.        59            "Mux2to1",
        To enable standalone execution, we manually added an 60             "Mux3to1",
     instruction.hex file for the RISC-V design. With 61                    "Adder"
                                                              62         ],
     this addition, the RISC-V processor ran without errors, 63          "status": "Pending",
     though the synthesis tool still reported minor warnings. 64         "interface": [
                                                                65          {
                            B LUEPRINT                          66             "name": "clk",
                                                                67             "direction": "input",
 1   {                                                          68             "width": 1
 2       "projectName": "Legv8SingleCycleProcessor",    69                  },
 3       "parameters": {                                70                  {
 4          "DATA_WIDTH": 8,                            71                     "name": "rst",
 5          "ADDRESS_WIDTH": 8,                         72                     "direction": "input",
 6          "INSTRUCTION_WIDTH": 16,                    73                     "width": 1
 7          "REG_ADDR_WIDTH": 3,                        74                  },
 8          "OPCODE_WIDTH": 4,                          75                  {
 9          "ALU_OP_WIDTH": 3,                          76                     "name": "debug_pc_out",
10         "IMMEDIATE_WIDTH": 6,                        77                     "direction": "output",
11         "JUMP_ADDR_WIDTH": 12,                       78                     "width": "ADDRESS_WIDTH"
12         "PC_INCREMENT_VAL": 2                        79                  },
13       },                                             80                  {
14       "components": [                                81                     "name": "debug_instruction_out",
15         {                                            82                     "direction": "output",
16            "name": "ProgramCounter",                 83                     "width": "INSTRUCTION_WIDTH"
17            "file": "program_counter.sv",             84                  },
18            "description": "Holds the address of the 85                   {
            current instruction and updates it based on 86                     "name": "debug_alu_result",
             control signals.",
87                       "direction": "output",               4   import random
88                             "width": "DATA_WIDTH"          5
89                   },                                       6 @cocotb.test()
90                   {                                        7 async def register_file_test(dut):
91                       "name": "debug_reg_write_data",      8     """Test the RegisterFile module thoroughly.
92                       "direction": "output",                     """
93                       "width": "DATA_WIDTH"                9
94                   }                                       10      # Parameters derived from the HDL module
95               ]                                           11      DATA_WIDTH = 8
96           }                                               12      REG_ADDR_WIDTH = 3
97       ]                                                   13      NUM_REGISTERS = 1 << REG_ADDR_WIDTH # 2ˆ3 =
98   }                                                                8 registers
                                                             14
                 Listing 1: Simple Legv8 Like Blueprint      15      # Create a clock instance and start it
                                                             16      clock = Clock(dut.clk, 10, units="ns") # 10
                                                                     ns period = 100MHz clock
     D. RegisterFile.sv                                      17      cocotb.start_soon(clock.start())
                                                             18
 1 module RegisterFile (
                                                             19      # Keep a shadow model of the register file
 2    input logic clk,
                                                                     for verification
 3    input logic rst,
                                                             20      # Initialize all shadow registers to 0,
 4    input logic [2:0] read_addr1,
                                                                     matching the reset behavior
 5    input logic [2:0] read_addr2,
                                                             21      shadow_registers = [0] * NUM_REGISTERS
 6    input logic [2:0] write_addr,
                                                             22
 7    input logic [7:0] write_data,
                                                             23      cocotb.log.info("Starting RegisterFile test
 8    input logic write_en,
                                                                     ")
 9    output logic [7:0] read_data1,
                                                             24
10    output logic [7:0] read_data2
                                                             25      # 1. Reset the DUT
11 );
                                                             26      cocotb.log.info("Applying reset and
12
                                                                     verifying initial state.")
13       localparam DATA_WIDTH = 8;
                                                             27      dut.rst.value = 1
14       localparam REG_ADDR_WIDTH = 3;
                                                             28      dut.write_en.value = 0
15       localparam NUM_REGISTERS = (1 <<
                                                             29      dut.write_addr.value = 0
           REG_ADDR_WIDTH);
                                                             30      dut.write_data.value = 0
16
                                                             31      dut.read_addr1.value = 0
17       logic [DATA_WIDTH-1:0] registers [
                                                             32      dut.read_addr2.value = 0
           NUM_REGISTERS-1:0];
                                                             33
18
                                                             34      await ClockCycles(dut.clk, 5) # Hold reset
19       // Synchronous write, preventing writes to R0
                                                                     for a few clock cycles
20       always_ff @(posedge clk or posedge rst) begin
                                                        35           dut.rst.value = 0
21         if (rst) begin
                                                        36           await RisingEdge(dut.clk) # Wait for reset
22            for (int i = 0; i < NUM_REGISTERS; i++)
                                                                     to de-assert and first clock edge
           begin
                                                        37
23              registers[i] <= {DATA_WIDTH{1’b0}};
                                                        38           # Verify all registers are 0 after reset
24            end
                                                        39           for i in range(NUM_REGISTERS):
25         end else begin
                                                        40               dut.read_addr1.value = i
26            // Only write if write_en is high AND the
                                                        41               dut.read_addr2.value = i # Check both
             destination is not R0
                                                                     read ports
27            if (write_en && (write_addr != 0)) begin
                                                        42               await Timer(1, units="ns") # Allow
28              registers[write_addr] <= write_data;
                                                                     combinatorial logic to settle
29                end
                                                        43               assert dut.read_data1.value == 0, \
30         end
                                                        44                   f"ERROR: Register {i} (read_data1)
31       end
                                                                     not 0 after reset. Got {dut.read_data1.
32
                                                                     value}"
33       // Asynchronous read, forcing R0 to be 0
                                                             45          assert dut.read_data2.value == 0, \
34       // If reading address 0, output 0, otherwise
                                                             46              f"ERROR: Register {i} (read_data2)
           output the register value.
                                                                     not 0 after reset. Got {dut.read_data2.
35       assign read_data1 = (read_addr1 == 0) ? {
                                                                     value}"
           DATA_WIDTH{1’b0}} : registers[read_addr1];
                                                             47          shadow_registers[i] = 0 # Ensure shadow
36       assign read_data2 = (read_addr2 == 0) ? {
                                                                      model is also reset to 0
           DATA_WIDTH{1’b0}} : registers[read_addr2];
                                                             48
37
                                                             49      cocotb.log.info("Initial state verified:
38   endmodule
                                                                     All registers are 0.")
                         Listing 2: Corrected RegisterFile   50
                                                             51
                                                             52
     E. test RegisterFile.sv                                 53      # 2. Basic Write and Read Test
                                                             54      cocotb.log.info("Performing basic write and
 1 import cocotb                                                      read test.")
 2 from cocotb.clock import Clock                            55      test_addr = 1
 3 from cocotb.triggers import RisingEdge,                   56      test_data = 0xAA
       FallingEdge, Timer, ClockCycles
57    dut.write_en.value = 1                             .read_data1.value)}"
58    dut.write_addr.value = test_addr            106    assert dut.read_data2.value == write_data2,
59    dut.write_data.value = test_data                    \
60    await RisingEdge(dut.clk) # Write occurs on 107        f"ERROR: Concurrent read data2 mismatch
       this rising edge                                  . Expected {hex(write_data2)}, got {hex(dut
61    shadow_registers[test_addr] = test_data #          .read_data2.value)}"
      Shadow model updated *after* the clock edge 108    cocotb.log.info(f"Concurrent writes to R{
62                                                       write_addr1} ({hex(write_data1)}) and R{
63    # Read immediately after write (within the         write_addr2} ({hex(write_data2)}) and reads
      same clock cycle)                                   verified.")
64    dut.read_addr1.value = test_addr            109
65    dut.read_addr2.value = test_addr            110    # 4. Overwriting a Register
66    await Timer(1, units="ns") # Allow          111    cocotb.log.info("Testing overwriting a
      combinatorial read outputs to settle               register.")
67    assert dut.read_data1.value == test_data, \ 112    overwrite_addr = 2
68        f"ERROR: Read data1 mismatch after      113    overwrite_data = 0xCC
      write. Expected {hex(test_data)}, got {hex( 114    dut.write_en.value = 1
      dut.read_data1.value)}"                     115    dut.write_addr.value = overwrite_addr
69    assert dut.read_data2.value == test_data, \ 116    dut.write_data.value = overwrite_data
70        f"ERROR: Read data2 mismatch after      117    await RisingEdge(dut.clk)
      write. Expected {hex(test_data)}, got {hex( 118    shadow_registers[overwrite_addr] =
      dut.read_data2.value)}"                            overwrite_data
71                                                 119
72    # Read from an unwritten address (should    120    dut.read_addr1.value = overwrite_addr
      still be 0)                                 121    await Timer(1, units="ns")
73    unwritten_addr = (test_addr + 1) %          122    assert dut.read_data1.value ==
      NUM_REGISTERS                                      overwrite_data, \
74    dut.read_addr1.value = unwritten_addr       123        f"ERROR: Overwrite failed for R{
75    await Timer(1, units="ns")                         overwrite_addr}. Expected {hex(
76    assert dut.read_data1.value ==                     overwrite_data)}, got {hex(dut.read_data1.
      shadow_registers[unwritten_addr], \                value)}"
77        f"ERROR: Read data from unwritten       124    cocotb.log.info(f"Overwrite of R{
      register {unwritten_addr} mismatch.                overwrite_addr} with {hex(overwrite_data)}
      Expected {hex(shadow_registers[                    verified.")
      unwritten_addr])}, got {hex(dut.read_data1. 125
      value)}"                                    126    # 5. No Write when write_en is low
78    cocotb.log.info(f"Basic write to R{         127    cocotb.log.info("Testing no write when
      test_addr} ({hex(test_data)}) and read             write_en is low.")
      verified.")                                 128    no_write_addr = 3
79     # 3. Concurrent Writes and Reads (         129    no_write_data = 0xFF
      different addresses)                        130    original_value = shadow_registers[
80    cocotb.log.info("Testing concurrent writes         no_write_addr] # Should be 0 from reset
      and reads.")                                131    dut.write_en.value = 0 # Crucial: write_en
81    write_addr1 = 1                                    is low
82    write_data1 = 0x11                          132    dut.write_addr.value = no_write_addr
83    write_addr2 = 2                             133    dut.write_data.value = no_write_data
84    write_data2 = 0x22                          134    await RisingEdge(dut.clk) # Clock edge, but
85                                                        no write should occur
86    # Write to addr1                            135
87    dut.write_en.value = 1                      136    dut.read_addr1.value = no_write_addr
88    dut.write_addr.value = write_addr1          137    await Timer(1, units="ns")
89    dut.write_data.value = write_data1          138    assert dut.read_data1.value ==
90    await RisingEdge(dut.clk)                          original_value, \
91    shadow_registers[write_addr1] = write_data1 139        f"ERROR: Write occurred when write_en
92                                                       was low for R{no_write_addr}. Expected {hex
93    # Write to addr2                                   (original_value)}, got {hex(dut.read_data1.
94    dut.write_en.value = 1                             value)}"
95    dut.write_addr.value = write_addr2          140    assert dut.read_data1.value !=
96    dut.write_data.value = write_data2                 no_write_data, \
97    await RisingEdge(dut.clk)                   141        "ERROR: Data was written despite
98    shadow_registers[write_addr2] = write_data2        write_en being low!"
99                                                 142   cocotb.log.info(f"No write to R{
100   # Read both concurrently using different           no_write_addr} when write_en is low
      read ports                                         verified.")
101   dut.read_addr1.value = write_addr1          143
102   dut.read_addr2.value = write_addr2          144    # 6. Fill all registers and verify
103   await Timer(1, units="ns")                  145    cocotb.log.info("Filling all registers and
104   assert dut.read_data1.value == write_data1,        verifying their contents.")
       \                                          146    dut.write_en.value = 1
105       f"ERROR: Concurrent read data1 mismatch 147    for i in range(NUM_REGISTERS):
      . Expected {hex(write_data1)}, got {hex(dut 148        data_to_write = (i * 17 + 5) & ((1 <<
      DATA_WIDTH) - 1)                            191            dut.write_en.value = 0 # No write
149       dut.write_addr.value = i                       this cycle
150       dut.write_data.value = data_to_write    192            cocotb.log.debug(f"Cycle {cycle}:
151       dut.write_en.value = 1 if i != 0 else 0        No write this cycle.")
        # Don’t write to R0                       193
152                                                194       # 2. Set read addresses for the *
153       await RisingEdge(dut.clk)                      current* cycle’s verification.
154                                                195       # These reads will reflect the state *
155       # Update shadow model only if not R0           after* the upcoming clock edge.
156       if i != 0:                              196        read_addr1 = random.randint(0,
157           shadow_registers[i] = data_to_write        NUM_REGISTERS - 1)
158       else:                                   197        read_addr2 = random.randint(0,
159           shadow_registers[i] = 0 # R0               NUM_REGISTERS - 1)
      always stays 0                              198        dut.read_addr1.value = read_addr1
160                                                199       dut.read_addr2.value = read_addr2
161   # Verify all registers by reading them back 200
162   for i in range(NUM_REGISTERS):              201        # 3. Wait for the clock edge. This is
163       dut.read_addr1.value = i                       when the DUT’s write (if enabled) happens.
164       dut.read_addr2.value = (i + 1) %        202        await RisingEdge(dut.clk)
      NUM_REGISTERS # Read another one            203
      concurrently                                204        # 4. Update shadow model *after* the
165       await Timer(1, units="ns")                     clock edge if a write was enabled
166       assert dut.read_data1.value ==          205        if write_this_cycle:
      shadow_registers[i], \                      206            shadow_registers[write_addr_val] =
167           f"ERROR: Verification failed for R{        write_data_val
      i} (read_data1). Expected {hex(             207
      shadow_registers[i])}, got {hex(dut.        208        # 5. Allow combinatorial logic for
      read_data1.value)}"                                reads to settle *after* the clock edge
168       assert dut.read_data2.value ==          209        await Timer(1, units="ns")
      shadow_registers[(i + 1) % NUM_REGISTERS], 210
      \                                           211        # 6. Now verify the reads
169           f"ERROR: Verification failed for R 212         expected_data1 = shadow_registers[
      {(i + 1) % NUM_REGISTERS} (read_data2).            read_addr1]
      Expected {hex(shadow_registers[(i + 1) %    213        expected_data2 = shadow_registers[
      NUM_REGISTERS])}, got {hex(dut.read_data2.         read_addr2]
      value)}"                                    214        actual_data1 = dut.read_data1.value
170       cocotb.log.debug(f"Verified R{i} ({hex( 215        actual_data2 = dut.read_data2.value
      shadow_registers[i])}) and R{(i + 1) %      216
      NUM_REGISTERS} ({hex(shadow_registers[(i + 217         assert actual_data1 == expected_data1,
      1) % NUM_REGISTERS])})")                           \
171   cocotb.log.info("All registers filled and   218            f"ERROR: Cycle {cycle}: Random
      verified successfully.")                           Read1 mismatch at addr {read_addr1}.
172                                                      Expected {hex(expected_data1)}, got {hex(
173   # 7. Randomized Test                               actual_data1)}"
174   cocotb.log.info("Starting randomized test    219       assert actual_data2 == expected_data2,
      (100 cycles).")                                    \
175                                                220           f"ERROR: Cycle {cycle}: Random
176   for cycle in range(100):                           Read2 mismatch at addr {read_addr2}.
177       # 1. Determine write operation for the         Expected {hex(expected_data2)}, got {hex(
      *upcoming* clock edge                              actual_data2)}"
178       write_this_cycle = False                 221       cocotb.log.debug(f"Cycle {cycle}:
179       write_addr_val = 1                             Random Read: addr1={read_addr1}, data1={hex
180       write_data_val = 0                             (actual_data1)} (expected {hex(
181                                                      expected_data1)}) | "
182       if random.random() < 0.6: # 60% chance 222                           f"addr2={read_addr2},
      to write                                            data2={hex(actual_data2)} (expected {hex(
183           write_this_cycle = True                    expected_data2)})")
184           write_addr_val = random.randint(1, 223
      NUM_REGISTERS - 1)                          224    cocotb.log.info("Randomized test completed.
185           write_data_val = random.randint(1,         ")
      (1 << DATA_WIDTH) - 1)                      225    cocotb.log.info("RegisterFile test finished
186           dut.write_en.value = 1                      successfully!")
187           dut.write_addr.value =
      write_addr_val                                         Listing 3: Corrected test RegisterFile
188           dut.write_data.value =
      write_data_val
189           cocotb.log.debug(f"Cycle {cycle}:
      Setting inputs for write: addr={
      write_addr_val}, data={hex(write_data_val)}
      ")
190       else:
