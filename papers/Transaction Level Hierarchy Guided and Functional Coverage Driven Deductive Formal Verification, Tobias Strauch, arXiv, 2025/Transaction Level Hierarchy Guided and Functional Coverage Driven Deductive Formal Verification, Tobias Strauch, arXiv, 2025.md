                                        To appear in the proc. of the 35th Intern. IEEE Workshop on Rapid System Prototyping, 3rd Oct. 2024, Raleigh, NC, USA



                                         Transaction Level Hierarchy Guided and Functional
                                           Coverage Driven Deductive Formal Verification
                                                                                                   Tobias Strauch
                                                                                                        R&D
                                                                                                   EDAptix e.K.
                                                                                                Munich, Germany
                                                                                             Email: tobias@edaptix.com

                                           Abstract—We demonstrate how dynamic verification (e.g. sim-             is also supported. The paper finishes with related work, results,
                                        ulation) can be replaced by deductive formal verification and              and the concluding Section IX.
                                        how to benefit from the advantages of symbolic verification and
                                        the reuse of verification proofs. To do this, we swap the well-                    II. F UNCTIONAL COVERAGE AND ASSERTIONS
                                        known module-hierarchy based concept with a transaction-level
arXiv:2501.01534v1 [cs.AR] 2 Jan 2025




                                                                                                                      Today, FC comes in two flavors in SystemVerilog. One type
                                        (TL) based alternative, which still allows us to describe the design
                                        as precisely as on RTL. We enhance the aspect-oriented and TL              of FC is sample-based coverage provided by a covergroup.
                                        oriented language PDVL to support the definition of functional             Covergroups record the number of occurrences of various
                                        coverage (FC) and assertions at all levels of a TL-hierarchy.              values specified as coverpoints. These coverpoints can be hier-
                                           We then show how to use a deductive formal verification (DFV)           archically referenced by testcases and testbenches so that it can
                                        flow which compiles PDVL code into Gallina code to be used by              be verified whether certain values or scenarios have occurred.
                                        the Coq theorem prover. It can be argued that FC can be converted
                                        into proof obligations and that proving them is equivalent to 100%         They also provide a means for creating cross coverage. Unlike
                                        coverage. We also demonstrate how lower-level proofs can be                assertion-based cover properties, covergroups may be used in
                                        reused when verifying aspects at higher-levels of a TL-hierarchy.          both class-based objects or structural code.
                                        We argue that the traditional assertion-based verification (ABV)              The second type of FC is assertion based. Assertions became
                                        methodology is still supported and SVA can be proven using DFV.            very popular at a time when individual IP modules had to
                                           Index Terms—Transaction level design and verification, deduc-
                                        tive formal verification, coverage driven verification, ABV                be connected to an SoC. Despite the introduction of an SoC
                                                                                                                   module interconnect specification (e.g. AMBA from ARM),
                                                                                                                   IP providers wanted to ensure that the bus interface of their
                                                               I. I NTRODUCTION
                                                                                                                   encrypted IP block was functioning properly and was stimu-
                                           Verification can generally be divided into dynamic and static           lated correctly. Since then, assertion-based verification (ABV)
                                        verification methods. Dynamic methods such as simulation are               has gained greater acceptance and is now used for FC and the
                                        usually associated with a testbench (TB) that stimulates and               definition of lower-level assertions of various design aspects.
                                        monitors the design behavior. If the guidelines of the Portable               Temporal logic is widely used in property checking based
                                        Stimulus Specification (PSS) and the Universal Verification                formal verification as well as ABV. To express different types of
                                        Methodology (UVM) are followed, then the functional cover-                 properties, a variety of temporal logics have been proposed. For
                                        age (FC) is defined and checked within testbenches. SystemVer-             example, Linear-time Temporal Logic (LTL) is able to describe
                                        ilog Assertions (SVA) and their automatically derived coverage             a property along with a single execution. However, it lacks the
                                        are typically defined within the Design Under Verification                 ability to express other possible executions and Computation
                                        (DUV) and can be (dynamically) verified during simulation.                 Tree Logic (CTL) is proposed to solve the problem. The
                                        Alternatively, static verification methods such as an SMT solver           assertion definitions are used to (auto-)generate assertion-based
                                        are used to statically verify SVA.                                         FC points.
                                           We exploit the aspect-oriented and transaction-level (TL) lan-             The relevant type of coverage comes from a cover property,
                                        guage PDVL [1], which allows the definition of TL-hierarchies.             which uses the same temporal syntax as defined by SVA. Since
                                        We associate FC and assertions with virtual transactions on                cover properties use the same properties as asserts, the same
                                        individual hierarchy levels. Then we convert the DUV and                   work in creating the properties can be reused in both checking
                                        verification code into Gallina [2] code to be used for deductive           and coverage gathering. Cover properties are typically used
                                        formal verification (DFV). We argue that FC can be converted               for protocol coverage since the temporal syntax is ideal for
                                        into theorems and that proving them is equivalent to 100% FC.              describing sequences of events over time, such as those required
                                           In Section II FC as well as assertions and their coverage are           for bus interfaces.
                                        discussed. Our work is described in Section III. Then PDVL                    However, cover properties can only be placed in structural
                                        is reintroduced briefly and the conversion to Gallina code is              code (i.e., modules, programs, or interfaces) and cannot be used
                                        outlined in Section V. TL-hierarchy guided and functional                  in class-based objects. Likewise, their coverage information
                                        coverage driven DFV is discussed in Section VI, followed by                is not easily accessible in SystemVerilog (SV) for use in a
                                        the presentation that the traditional SVA based ABV approach               testbench (e.g. steering stimulus generation).



                                                                                                               1
To appear in the proc. of the 35th Intern. IEEE Workshop on Rapid System Prototyping, 3rd Oct. 2024, Raleigh, NC, USA




           Fig. 1. Comparing status quo and transaction-level-hierarchy guided and functional coverage driven deductive formal verification.



  Fig. 1 shows that SVAs are defined at the module level                         3) Verifying FC and assertions from lower-level up to
according to the current state of the art. Dynamic ABV can                    system-level: System-level coverage is primarily captured using
be based on simulation, emulation or FPGA based prototyping.                  simulation techniques. As symbolic simulation is still lim-
All of them face the challenge of activating an assertion. When               ited, many simulation runs must be executed by directed or
dynamic ABV is combined with constraint random or directed                    constraint random tests. Additionally, the possibility to reuse
verification, the runtime can be very high to activate coverage               verification throughout the module hierarchy is limited. Veri-
points of corner cases. HW-based dynamic ABV solutions                        fying system-level coverage using static methods such as DFV
have the problem of collecting relevant assertion coverage                    continues to pose significant challenges, and its usage cannot
data. Static ABV uses predominantly SMT solver to verify the                  be considered mainstream today.
correctness of assertions.                                                       In our work we enable VTRs to define coverage. VTRs
                                                                              can be used to assert behavior seamlessly throughout the
                         III. O UR WORK                                       complete hierarchy, from lower-level up to the system-level.
   Our work enables the definition of FC and assertions from the              Therefore, coverage can be defined and verified throughout the
lower-level up to the system-level and supports their coverage-               TL-hierarchy as well. We demonstrate how these VTRs and
driven DFV. It is set in contrast to the status quo in Fig. 1.                their associated coverage can be converted into Gallina code
   1) Adding relevant language constructs to PDVL: PDVL is                    and how the individual coverage points can be proven. We argue
an aspect-oriented and transaction-level Programming Design                   that individual coverage points of VTRs can be associated with
and Verification Language, which itself adds language con-                    individual proofs. Subsequently, VTRs which are built on other
structs on top of SystemVerilog (SV).                                         VTRs can define coverage that can be proven by reusing proofs
   In our work we demonstrate further improvements to PDVL                    of their lower-level VTRs.
to enable DFV from lower-level up to the system-level. We refer                  4) Using lower-level assertion definition and associated
to code that asserts expected behavior as virtual transactions                coverage: Lower-level assertion definitions (such as SVA) are
(VTRs) in PDVL. VTRs are not meant to be synthesizable                        very well established for lower-level logic such as finite state
unless explicitly specified.                                                  machines (FSMs) and interface protocols. Usually, assertion
   2) Defining FC and assertions from lower-level up to system-               coverage definition is automatically derived from these lower-
level: When using SV, system-level coverage points can be                     level assertions and can be verified statically by SMT solvers
defined to capture complex system behavior. To make optimal                   or during dynamic verification (e.g. simulation).
use of this possibility and to support a certain level of reuse,                 Our work demonstrates how to reuse SVA in PDVL and
the UVM and the PSS were defined. Using SVA at the system                     discusses the conversion of the design and the lower-level
level to assert complex system behavior remains challenging.                  assertion definitions into Gallina code. Combined with the
   In our work we demonstrate the use of VTRs that can                        compiled design behavior, the assertions can then be verified
bundle a set of less complex VTRs. This allows the definition                 by proving using a DFV tool like the Coq proof assistant [3].
of a hierarchy of VTRs which asserts behavior from system-                       5) Proof by symbolic simulation: In our work we focus on
level all the way down to lower-level. Higher-level VTRs can                  DFV based on symbolic simulation, as demonstrated in [4].
therefore also assert system behavior that spans over DUV and                 Theorems can be proven that for a given initial state and a
TB behavior alike. This reusable TL-hierarchy based on VTRs                   given stimulation sequence, where state and sequence values
seamlessly fills the gap which exists between lower-level SVA                 can have a symbolic type, all possible resulting states and state
and the expected behavior defined by the UVM.                                 transitions match the expected behavior.



                                                                          2
To appear in the proc. of the 35th Intern. IEEE Workshop on Rapid System Prototyping, 3rd Oct. 2024, Raleigh, NC, USA


                           IV. PDVL                                        Algorithm 1 PDVL: RISC-V instruction example (ADDI)
                                                                            1: cl instr addi {                              (* cluster *)
   PDVL was introduced in 2017 [5]. We therefore only give
                                                                            2: c instr i addi { if (opcode i == 7’h13    (* condition *)
a very brief overview. PDVL is based on SV and encapsulates
conditions and assignments. The latter are then called datap-               3:   & funct3i == 3’h0) this; }
                                                                            4: d addi { dp out = rs1 dato+instr[31:20]; } (* datapath *)
aths. Transactions (TRs) determine the conditions under which
individual datapaths are valid. PDVL is not limited to CPUs,
                                                                            5: tr rv32i addi {                         (* transaction *)
but an example of a RISC-V instruction is given in Alg. 1.
                                                                            6:   unique @c instr i addi { d rs1i addr; d addi;
   Aforementioned elements are stored in clusters. The aspect-
                                                                            7:     d rd dp out; d rd addr; c rf write; d pc4; } } }
oriented paradigm of PDVL becomes obvious, when looking at
the hardware generation process (Alg. 2). A hardware module
hierarchy is built, and clusters are then joined into the individual
                                                                           Algorithm 2 PDVL: Generating a module hierarchy, joining
modules. The merging and signal routing must be handled by
                                                                           a cluster into a submodule and defining clock input and edge
the compiler. More information can be found in the PDVL
                                                                           sensitivity for registers.
specification [1].
                                                                            1: build TB {
   In this paper, we introduce the concept of VTRs which allows
                                                                            2: build i duv DUV;                    (* build hierarchy *)
us to define a TL-hierarchy (Fig. 2). We also show by examples,
                                                                            3: join cl rv32i cl rv32imc;                    (* joining *)
which SV constructs are reused in PDVL for FC and assertion
                                                                            4: join { tr reg { @e clk { tr rv32i addi; }}} cl rv32imc;
definition.

              V. PDVL TO G ALLINA COMPILER                                  5:   join cl rv32imc i duv; }
   The tool “MRPHS” compiles PDVL code into synthesizable
SV code. MRPHS’ PDVL to Gallina compiler extension was
introduced in [6]. We therefore only give a very brief overview.              MRPHS generates Gallina definitions to support symbolic
   The design “DUV” must be generated by using the relevant                simulation techniques. The definition sim update (Alg. 5, line
PDVL build commands (Alg. 2) before PDVL code is com-                      1) walks through the complete design and updates all possible
piled into a Gallina representation (Alg. 3). Once the logic is            non-sequential signals. Assuming the DUV has only one single
joined, all sequential and combinatorial signals of the DUV are            clock, then the definition sim cycle (Alg. 5, line 1) simulates
identified.                                                                a complete cycle, which includes an update of all sequential
   We mention the standard Boolean type ”bool” for signal bits             elements, followed by an update of all non-sequential signals.
in this paper, but any user-defined type can be used instead. Alg.         For more complex clock domain structures, the sim cycle
3 shows that all signals are added to an inductively defined type          definition is adapted accordingly. Alg. 5, line 3 demonstrates,
t item and that a dynamic list t state can be generated based              how two cycles of the design can be simulated.
on t item members.
   Only signals with a defined value are added to the t state list.
A signal can be removed from the list once its value becomes
                                                                           Algorithm 3 Gallina: Signal definition examples, the design
undefined. This applies to both sequential and combinatorial
                                                                           state list and a boolean function example
signals. The t state list therefore contains all sequential ele-
                                                                             1: Inductive t item : Type :=
ments and combinatorial signals that are defined at a given
                                                                             2:   | i nil
point of time.
                                                                             3:   | instr ( l : t bus32 )
   Alg. 3, line 12 shows that design-specific functions are
                                                                             4:   | ...
defined, which are subsequently used in the generated Gallina
                                                                             5:   | pc ( l : t bus20 )
code. MRPHS also generates a set of more general functions
                                                                             6:   | reg file ( l : t arr32x32 ) .
which, for instance, assign a given value to an item in the t state
                                                                            7:
list (e.g. f set) or extract the value of a specific item in the
                                                                            8: Inductive t state : Type :=
t state list (e.g. f get). The generated Gallina code mentioned
                                                                            9:   | st nil
so far is stored as a DUV specific library.
                                                                           10:  | st cons ( s : t item ) ( l : t state ) .
   For each condition in the PDVL source code, a Boolean
                                                                           11:
signal is generated and added to the item list as well. The
                                                                           12: Definition f equal32 ( a b : t bus32 ) : bool := ...
condition body is converted into a Gallina definition.
   All condition, datapath, and transaction definitions in PDVL
are compiled into Gallina code and stored as a second DUV-                 Algorithm 4 Gallina: Compiled condition, datapath and trans-
specific library, which is used by the final proof scripts. Alg. 4         action definitions (ADDI example)
gives an example related to the aforementioned RISC-V ADDI
                                                                            1: Definition c instr i addi ( st : t state ) : t state := ...
instruction. We will see in the following section, that theorems
                                                                            2: Definition d addi ( st : t state ) : t state := ...
can be proven based on the automatically generated Gallina
                                                                            3: Definition tr rv32i addi ( st : t state ) : t state := ...
code mentioned so far.



                                                                       3
To appear in the proc. of the 35th Intern. IEEE Workshop on Rapid System Prototyping, 3rd Oct. 2024, Raleigh, NC, USA


Algorithm 5 Gallina: Helper definitions for symbolic simula-            Algorithm 6 PDVL: VTR UART TX-RX Transfer
tion                                                                     1: cluster tb axi uart {
  1: Definition sim update ( st : t state ) : t state := ...             2:    c tx rx data eq {
  2: Definition sim cycle ( st : t state ) : t state := ...              3:       if (uart rx data == axi tx data) this; }
  3: Definition two cycles ( st : t state ) : t state :=                 4:    vtr tx rx transfer {
  4:  sim cycle (sim cycle st).                                          5:       sequence tx rx transfer {
                                                                         6:          init: {
                                                                         7:             random axi tx data;
  VI. TL- HIERARCHY GUIDED COVERAGE DRIVEN DFV                           8:             c axi trans;
A. Introducing virtual transactions                                      9:             finish; }
                                                                        10:          finish: {
   In this section we introduce virtual transactions (VTRs)             11:             @c uart rx valid {
which allow us to define a TL-hierarchy and ultimately the              12:                  cover cp tx rx eq { c rx tx data eq; }
reuse of lower-level verification results on higher-level. VTRs         13:                  exit; } } } } }
can define testbench related functionality such as sequences,
randomness, coverage points, etc.. A VTR can bundle a set of
TRs and VTRs. This generates a TL-hierarchy that can have               of a function written in a sequential programming language.
multiple top-level VTRs, whereas each of the top-level VTRs             The called VTR starts at the “init” state of the sequence. The
groups a specific set of TRs and VTRs for a specific verification       called VTR finishes when the “exit” keyword is reached. At this
goal. VTRs are not meant to be synthesizable unless explicitly          timepoint, the calling VTR continues processing its sequence.
specified.                                                                 The execution of the resulting VTR tree becomes time con-
   One of the key ideas behind PDVL is that it extends the              suming when a VTR calls a cycle-timed VTR. Our enhanced
SV language by only a limited number of new constructs.                 PDVL version supports the fork-join and other known mecha-
It is therefore intended that VTRs in PDVL reuse many of                nisms to run multiple time-consuming sequences in parallel.
the testbench related language constructs known from SV. We                An example of an untimed VTR is an instruction gen-
mention some keywords by providing examples.                            erator for an UART TX driver shown in Alg. 7 called
B. VTRs and testbench related language constructs                       “vtr cpu uart tx driver”. It is also outlined in Fig. 2 in the
                                                                        sequencer block, indicating that it calls the CPU multiple times
   Fig. 2 gives an overview of the design example we use                to force the CPU to issue individual bus master writes.
to demonstrate our methodology. The synthesizable UART                     After assigning a symbolic value to “axi tx data”, the
transmit (TX) module in the DUV provides standard UART TX               VTR successively calls a list of VTRs. The goal is that the
capabilities. The outgoing datastream is captured by an UART            UART TX Enable Bit is set (“vtr cpu uart tx enable”) and
monitor. We now show how a VTR (Alg. 6) can be defined,                 that the “axi tx data” value is written into the UART TX
which creates a verification environment for these two entities.        register (“vtr cpu uart tx data”) which starts the transmission.
   A VTR can define time consuming behavior by using the                Finally, the CPU should constantly loop over a NOP instruction
keyword sequence (Alg. 6, line 5). A sequence always starts             (“vtr cpu loop nop”). The called VTRs force the CPU in the
at the “init” state, can traverse a finite number of user defined       given system to execute individual instructions, which results
states (here “finish”) and becomes redundant when reaching the          in individual AXI bus-writes.
keyword “exit” (Alg. 6, line 13). A sequence can therefore also            The VTR “vtr cpu uart tx data” (Alg. 7, line 10) shows
be considered as an FSM.                                                how the CPU can be forced to execute a sequence of instruc-
   In our example (Alg. 6, line 6), a random “symbolic” value           tions to issue the relevant AXI master data write command.
is assigned to the byte “axi tx data” during the “init” state and          VTRs can be untimed, timed and cycle-timed. When a VTR
the condition “c axi trans” is set valid. The sequence then tran-       is called by a VTR outside an edge sensitive block, the VTR is
sitions to the finish state. Once the condition “c uart rx valid”       untimed and the VTRs interact by an calling-init-exit-continue
is true, it is checked whether the coverage point “cp tx rx eq”         process. Multiple VTRs can also interact using a fork-join or
is covered and the sequence is exited.                                  alternative mechanisms.
   If the VTR “vtr tx rx transfer” is called within a VTR that
defines the clock for the registers involved, then the sequence         D. VTRs and coverage related constructs
is clocked by the specified clock (e.g. UART clock). In this               PDVL supports the concept of SV to assign a random value
case we are talking about a cycle-timed VTR.                            to a signal. This is the case, for example, if the payload of a
   A cycle-timed VTR checks signal values and condition states          data transmission is generic. PDVL uses the keyword “random”
in the respective cycle. It also assigns condition states and           to indicate, that any valid value within the given range of a
signal values to the relevant signal at the given clock edge.           signal must be considered during verification (Alg. 6, line 7
                                                                        and Alg. 7, line 5). In the remainder of the paper we use the
C. VTRs as instruction code generator                                   term ”symbolic” value for such an assignment.
  A VTR can call other VTRs. The calling VTR can then be                   We also introduce a coverage definition for individual VTRs.
considered as an untimed VTR, which has more the character              A coverage point is defined by the keyword “cover”, followed



                                                                    4
To appear in the proc. of the 35th Intern. IEEE Workshop on Rapid System Prototyping, 3rd Oct. 2024, Raleigh, NC, USA




Fig. 2. Transaction level hierarchy example, showing the design under verification (DUV) and transactions as well as the testbench (TB) and virtual transactions.


Algorithm 7 PDVL: CPU UART Driver Instruction Generator                            VTRs which give an abstract view of local behavior such as a
 1: cluster tb cpu uart driver {                                                   CPU sequence and a UART TX-RX data transfer.
 2:    vtr cpu uart tx driver {                                                       We now broaden the perspective and introduce a VTR
 3:       sequence cpu uart driver {                                               which produces a system-wide sequence, shown in Fig. 2. In
 4:         init: {                                                                our example, the top-level sequence “vtr cpu uart sequence”
 5:            random axi tx data;                                                 forces the CPU to generate a set of instructions which enable
 6:            vtr cpu uart tx enable;                                             the UART to transmit data. The CPU then writes a symbolic
 7:            vtr cpu uart tx data;                                               value into the UART, which is then transmitted and captured
 8:            vtr cpu loop nop;                                                   by the UART monitor. Fig. 2 illustrates that it can be seen as
 9:            exit; } } }                                                         a top-level VTR covering previously mentioned VTRs so far.
10:    vtr cpu uart tx enable { ... }                                              We will see how our approach to use DFV will benefit from
11:    vtr cpu uart tx data {                                                      such a TL-hierarchy.
12:       sequence cpu tx data {
                                                                                   F. VTRs and deductive formal verification
13:         init: { instr2;
14:            ... /* code executing ”lui s0, 0x80030;” */ }                          We now show how VTRs and the resulting TL-hierarchy can
15:         instr2: { instr3;                                                      be used for DFV. We improved the PDVL to Gallina compiler
16:            ... /* code executing ”li a5, axi tx data;” */ }                    (“MRPHS”, Section V) to support VTRs.
17:         instr3: {                                                                 1) Proving theorems based on combined transactions:
18:            ... /* code executing ”sw a5, 4(s0);” */ }                          Alg. 8 shows a simplified code of the example VTR (Alg.
19:            exit; } } }                                                         6) compiled into Gallina code. The theorem lists a sym-
20:    vtr cpu loop nop { ... }}                                                   bolic value as a hypothesis. Coverage properties are compiled
                                                                                   into definitions, which check that the defined conditions are
                                                                                   true (“cp uart tx rx”). The sequence “vtr tx rx transfer” is
                                                                                   also compiled into a definition, which modifies the list of
by a property name and a body that, for example, checks
                                                                                   the given design states. The compiled and provable theo-
whether a certain condition is true at a given cycle (Alg. 6,
                                                                                   rem “th tx rx transfer” executes the “vtr tx rx transfer” and
line 12).
                                                                                   checks whether the property “cp uart tx rx” is covered.
                                                                                      2) Proving theorems based on sequences: In this sub-
E. TL-hierarchy
                                                                                   section, we refer to the CPU UART driver code generator
   So far we have discussed the CPU and the UART section of                        described in Alg. 7. To prove that each of the code generation
our example design. We need to mention the AXI arbiter block,                      sequences (vtr cpu uart tx enable and vtr cpu uart tx data)
which basically converts AXI master writes to the relevant AXI                     initiates correct AXI master writes, individual cover properties
slave writes. A VTR can also be defined for an AXI master-                         can be defined similar to the coverage property in Alg. 6.
slave transfer, such as “”vtr axi mst slv transfer” in Fig. 2.                        Alg. 9 lists the compiled and provable theorem for the
   There are additional TRs and VTRs which connect the design                      “cpu uart driver” sequence listed in Alg. 7. After the individual
modules and testbench elements. Fig. 2 illustrates that all TRs                    sequences have been executed, it is checked whether the
are part of the synthesizable design. We have also discussed                       relevant properties are covered (“true”).



                                                                               5
To appear in the proc. of the 35th Intern. IEEE Workshop on Rapid System Prototyping, 3rd Oct. 2024, Raleigh, NC, USA


Algorithm 8 Gallina: Coverage theorem (simplified)                     converted into PDVL items. The Boolean layer is compiled
 1: Theorem th tx rx transfer :                                        into condition and datapath logic as defined by PDVL. SVA
 2:    foreach axi tx data : t bus,                                    sequences and properties are converted into VTR sequences
 3:    cp uart tx rx (                                                 as defined in this paper. Here multiple VTR sequences can
 4:    vtr tx rx transfer ( reset st )).                               result from this conversion process and the possibility to use
                                                                       fork-join methods becomes relevant. SVA local variables can
Algorithm 9 Gallina: CPU UART driver sequence                          also be compiled into registers within the IR. Assumptions and
 1: Theorem th cpu uart driver :                                       coverage goals are converted into coverage properties.
 2:    foreach axi tx data : t bus,                                       At the current state, our work does not support the full
 3:    cp cpu tx data (                                                range of SVAs. There are limitations in aspects like liveliness,
 4:    cp cpu tx enable (                                              overlapping transactions, etc.. However, it is not our goal to
 5:    vtr cpu loop nop (                                              fully support this specific methodology. Let’s assume there are
 6:    vtr cpu uart tx data ( axi tx data                              SVAs in a sender and a receiver of an interface. We argue that
 7:    vtr cpu uart tx enable ( reset st ))))).                        our approach of a TL-hierarchy covers both sides with VTRs
                                                                       spanning over sender and receiver functionality, so that local
                                                                       SVAs become redundant.
G. Reuse of proofs                                                                          VII. R ELATED WORK
   The ability to define more abstract VTRs to build a TL-                BSV: Bluespec SystemVerilog (BSV) [8] is a high-level
hierarchy can be particularly useful when proofs of lower-level        hardware description language of guarded atomic actions. The
theorems derived from lower-level TRs or VTRs can be reused.           BSV concept is based on BSV rules and a term rewriting
We start with a top-level VTR.                                         system, whereas each rule can be viewed as a declarative
   1) Top-level VTR reuses lower level proofs: We can see              assertion expressing a potential atomic state transition. In [9] it
in Fig. 2 how the top-level VTR “vtr cpu uart sequence”                is discussed, how the modular concept of BSV generates new
functionally extends over all VTRs mentioned so far. We want           challenges for predicting the compiler output. The sequential
to prove that the symbolic value which is programmed by the            behavior of the hardware defined by PDVL is exact and the
CPU is transmitted from the UART TX module to the UART                 cycle behavior of the compiler’s SV and Gallina code is
monitor. This can be asserted within a VTR similar to the              therefore predictable since no scheduling is involved.
“cp uart tx rx” cover property in Alg. 6, line 12. The top-level          KAMI: According to [10], KAMI is a framework to support
VTR “vtr cpu uart sequence” needs to call the same sequence            implementing, specifying, formally verifying, and compiling
as defined in Alg. 7, lines 6-8.                                       hardware designs based on BSV and the Coq theorem prover.
   After compiling the VTR “vtr cpu uart sequence” to the              It emphasizes modular verification of digital hardware. In
relevant theorem, the proof can reuse proven theorems of lower-        contrast, using PDVL provides a TL design paradigm and a TL
level theorems such as the one of “th tx rx transfer” etc..            formal verification paradigm. TRs can span multiple modules,
   2) Mid-level VTR reuses lower level proofs: When proving            creating a TL-hierarchy that can range from low-level cycle-
mid-level theorems such as “th tx rx transfer”, reusing lower-         accurate TRs to approximately-timed or untimed VTRs. The
level theorems (not previously mentioned) is also advantageous.        concept of a module becomes only relevant when the final SV
   In the given UART example, it can be argued that a finite           code is generated.
state machine (FSM) controlling the UART TX has its coun-                 Rules rewriting: The work in [11] describes the proving and
terpart in the FSM of the UART receiver (RX) in the testbench          disproving of assertion rewrite rules with automated theorem
monitor. For simplicity, let’s assume that the transmission is         provers. The work is based on the assertion language PSL and
based on a synchronous single-bit protocol.                            concentrates on rule rewriting. We outlined our flow to convert
   The TR in the TX-FSM that defines the transmission of a             SVA into an IR of FSMs, datapath and checker logic, which is
single bit is combined with the TR in the RX-FSM to form               then compiled into Gallina code and used for DFV. We do not
a new VTR that defines the entire transmission process of a            use rewriting as such, but benefit greatly from reusing proofs
single bit value. This abstract VTR in PDVL is compiled into           through applying proven theorems.
Gallina code which can be used for proving. A theorem is                  RTL to TLM: The main intent of the work in [12] is to
proven stating that the transmitted data bit value is correct.         automatically build a dynamic ABV environment for a TLM
   The same mechanism is applied for the transfer of a byte            model, with no restrictions on the abstraction level, by starting
and a full packet, while using the previously formally verified        from a set of properties initially defined for a corresponding
theorem of transmitting a bit (or byte respectively).                  RTL implementation. First, cycle-accurate RTL properties are
                                                                       automatically rewritten into a set of properties suited to be
H. SVA in PDVL and intermediate representation                         checked on an event-based TLM model. Secondly, an approach
   The work in [7] shows how SVAs can be converted into                is defined to synthesize TLM properties into checkers to be
synthesizable code by extracting FSMs, datapath and checker            adopted for dynamic ABV of the TLM model. In our work,
logic. We follow these guidelines and generate an IR that is           we use a TL language to define TL assertions throughout a
in-line with PDVL representations. Local SVA variables are             user defined TL-hierarchy.



                                                                   6
To appear in the proc. of the 35th Intern. IEEE Workshop on Rapid System Prototyping, 3rd Oct. 2024, Raleigh, NC, USA


   TL assertion language: In [13] an assertion specification             which enables the definition and verification of functional
language is presented which is based on formal definitions that          coverage and assertions from lower-level to system-level.
allows the specification of TL properties and their execution in            This hierarchical verification approach allows us to focus on
simulation. It derives the language from known ABV languages             level specific verification challenges and enables incremental
and extends these by the required TL functionality. It also              updates when behavior only changes locally. It fills the gap that
explains how simulation traces of finite length can be checked           exists today between low-level SVA-based verification and the
against properties. Our work, on the other hand, is optimized for        state-of-the-art coverage-based verification defined in UVM and
DFV. Nevertheless, the work in [13] was a great inspiration for          PSS. At the same time, lower-level SW routines (e.g. peripheral
our work, especially because it is based on industry experience.         drivers) become an integral part of the system verification at
                                                                         the same time.
                        VIII. R ESULTS
   The SoC design was written in PDVL. The number of                                                     TABLE I
synthesizable TRs and VTRs are listed in Tab I for each                                    R ESULTS FOR REFERENCE S O C DESIGN .
individual core and the complete SoC. MRPHS was used to                                   TR     VTR     Theorems       Coq      Coq      Verilator
compile the design into synthesizable SV code. The design                                                              CCET      MIRT       SRT
and the VTRs are compiled into Gallina code. The compilation                                                           [sec]     [sec]     [sec]
                                                                           RV32IMC       107     144        219         52.4     5.01       27.8
process of the SoC is completed within less than 10 seconds                 SDRAM        93      160        197         55.9     3.49       27.0
for each of the two outputs. For compilation and runtime                    Ethernet     72      89         106         18.3     2.48       14.0
evaluation, we use an i7, 2.6GHz CPU.                                        AES         64      76         111         13.7     2.92       8.03
   The number of resulting theorems is listed in Tab. I. It also              SoC        445     813        1048        186      6.26       125
shows the complete consecutive execution time (CCET) of all
proofs on a single thread for each individual core and the entire
SoC. We introduce a maximal incremental runtime (MIRT),                                                R EFERENCES
which is the worst case runtime to prove all relevant proofs              [1] T. Strauch. PDVL Specification v0.1. [Online]. Available:
based on an incremental change in the source code.                            https://github.com/cloudxcc/PDVL
                                                                          [2] Gallina Development Team. The Gallina specification language. [On-
   We developed a testbench in SV with the same coverage                      line]. Available: https://coq.github.io/doc/v8.9/refman/language/gallina-
we achieve by the DFV flow. We use Verilator to run the                       specification-language.html
regression suite. Tab I lists the simulation runtime (SRT) for            [3] Coq Development Team. The coq proof assistant. [Online]. Available:
                                                                              http://coq.inria.fr/
each individual core and the entire SoC.                                  [4] Y. Morihiro, and T. Toneda, “Formal verification of Data-path Circuits
   The execution time of a simulation based regression suite                  Based on Symbolic Simulation”, Proc. of the Ninth Asian Test Sympo-
(SRT) is faster than the complete execution time of the DFV                   sium, 2000, 6th Dec, Taipei, Taiwan, pp. 1-8.
                                                                          [5] T. Strauch, ”An Aspect and Transaction Oriented Programming, Design
flow (CCET). This is mainly due to Coq theorem prover                         and Verification Language”, IEEE Euromicro DSD 2017, 30 Aug. - 1
runtime issues. Nevertheless, DFV-based tests can be run in                   Sep., Vienna, Austria, pp. 30 - 39.
parallel to reduce this disadvantage, just like simulation-based          [6] T. Strauch, ”Deductive Formal Verification of Synthesizable, Transaction-
                                                                              level Hardware Designs Using Coq”, Design, Automation & Test in
regression suites. Alternatively, a faster theorem prover might               Europe Conference & Exhibition (DATE), 25-27 March 2024, Valencia,
eventually be used as our DFV is not limited to the Coq theorem               Spain, pp. 1-6.
prover.                                                                   [7] J. Long, and A. Seawright, ”Synthesizing SVA Local Variables for Formal
                                                                              Verification”, 44th ACM/IEEE Design Automation Conf (DAC), 4-8 June
   The runtime of the DFV flow when only an incremental                       2007, San Diego, CA, USA. pp. 75-80.
update needs to be verified (MIRT), looks promising compared              [8] R. Nikhil, “Bluespec SystemVerilog: Efficient, correct RTL from high
to the individual simulation runtime (SRT) of individual core                 level specifications,” Proc. 2nd ACM and IEEE Int. Conf. Formal Meth-
                                                                              ods and Models for Co-Design, MEMOCODE’04, 23-25 June 2004, San
related tests.                                                                Diego, CA, USA, pp. 69–70.
   We see one of the most important advantages at the system              [9] M. Vijayaraghavan, N. Dave, and Arvind, “Modular Compilation of
level. While it is becoming increasingly difficult to write                   Guarded Atomic Actions”, ACM/IEEE Intern. Conf. on Formal Meth-
                                                                              ods and Models for Codesign, MEMOCODE 2013, 18-20 Oct. 2013,
efficient system-level tests in simulation, we have found that                Portland, OR, USA, pp. 177-188.
it is very inviting to write top-level tests for our DFV flow.           [10] J. Choi, M. Vijayaraghavan, B. Sherman, A. Chlipala, and Arvind.
The possibility to reuse lower level proof is particularly helpful            “Kami: A Platform for High-Level Parametric Hardware Specification
                                                                              and Its Modular Verification”, Proceedings of the ACM on Programming
when solving software driver related issues. In this respect, we              Languages, Volume 1, Issue ICFP, Article No.: 24, pp 1–30.
see a clear advantage of our demonstrated DFV flow over a                [11] K. Morin-Allory, M. Boulé, D. Borrione, and Zeljko Zilic, ”Proving and
simulation-based verification approach.                                       Disproving Assertion Rewrite Rules with Automated Theorem Provers”,
                                                                              IEEE Intern. High Level Design Validation and Test Workshop, 19-21
                       IX. C ONCLUSION                                        November 2008, Incline Village, NV, USA, pp. 56-63.
                                                                         [12] Nicola Bombieri, Riccardo Filippozzi, Graziano Pravadelli and Francesco
  We have demonstrated the use of deductive formal verifi-                    Stefanni, ”RTL property abstraction for TLM assertion-based verifica-
cation (DFV) to prove functional coverage and assertions as                   tion”, Design, Automation & Test in Europe Conference & Exhibition
                                                                              (DATE), 9-13 March 2015, Grenoble, France, pp. 85-90.
an alternative to simulation-based verification. One key contri-         [13] W. Ecker, V. Esen, T. Steininger, M. Velten, and M. Hull, ”Specification
bution of DFV is the ability to symbolically verify complete                  Language for Transaction Level Assertions”, IEEE Intern. High Level
coverage areas in a deductive manner. In order to benefit from                Design Validation and Test Workshop, 8-10 November 2006, Monterey,
                                                                              CA, USA, pp. 77-84.
verification reuse, we introduce a transaction level hierarchy,



                                                                     7
