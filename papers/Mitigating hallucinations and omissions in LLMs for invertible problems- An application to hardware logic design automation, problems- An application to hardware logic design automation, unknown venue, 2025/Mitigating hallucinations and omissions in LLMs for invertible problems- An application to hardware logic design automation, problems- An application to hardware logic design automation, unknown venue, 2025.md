                                             Mitigating hallucinations and omissions in LLMs for invertible
                                             problems: An application to hardware logic design automation
                                                    Andrew S. Cassidy, Guillaume Garreau, Jay Sivagnaname, Mike Grassi, Bernard Brezzo,
                                                                           John V. Arthur, Dharmendra S. Modha
                                                                                                          IBM Research
                                         Abstract                                                                                        Input LCT specification
                                         We show for invertible problems that transform data from a source                                               !!"#$!%
                                         domain (for example, Logic Condition Tables (LCTs)) to a destina-
                                         tion domain (for example, Hardware Description Language (HDL)                             Encode LLM        !
arXiv:2512.03053v2 [cs.LG] 16 Apr 2026




                                         code), an approach of using Large Language Models (LLMs) as a
                                         lossless encoder from source to destination followed by as a lossless                                           !"&'!#('&
                                         decoder back to the source, comparable to lossless compression in               Output
                                         information theory, can mitigate most of the LLM drawbacks of                    Logic                Verilog HDL
                                         hallucinations and omissions. Specifically, using LCTs as inputs,               Design
                                                                                                                                                         !!"#$!%
                                         we generate the full HDL for a two-dimensional network-on-chip                                                                  Comparison:
                                         router (13 units, 1500-2000 lines of code) using seven different LLMs,                    Decode LLM       ! !"                 ✅ Match /
                                         reconstruct the LCTs from the auto-generated HDL, and compare                                                                   ❌ No Match
                                         the original and reconstructed LCTs. This approach yields signif-                                               !"&'!#('&
                                         icant productivity improvements, not only confirming correctly
                                         generated LLM logic and detecting incorrectly generated LLM logic                          Reconstructed LCT specification
                                         but also assisting developers in finding design specification errors.
                                                                                                                   Figure 1: View of an LLM as an invertible transform T from
                                         1    Introduction                                                         an input token sequence S𝑝𝑟𝑜𝑚𝑝𝑡 to an output token sequence
                                         Large Language Models (LLMs) suffer from the fundamental chal-            S𝑟𝑒𝑠𝑝𝑜𝑛𝑠𝑒 . The input prompt sequence is a specification. The
                                         lenges of false positives (hallucinations) and false negatives (omitted   output sequence contains the completed HDL code. By reap-
                                         information). Recent research shows that hallucination is inevitable      plying the LLM transform T −1 in the reverse direction, the
                                         [36] and LLMs have difficulty with omissions [10]. We demonstrate         input specification can be reconstructed from the output
                                         that it is possible to mitigate these challenges for invertible prob-     HDL code and checked versus the original specification.
                                         lems consisting of essentially translating the same information into
                                         different semantic contexts. Without directly combating intrinsic
                                         false positives and false negatives inherent in the LLMs, we pro-
                                         pose a direction whereby it is possible to spot and correct these            As an illustrative example, we demonstrate that this approach
                                         extrinsically. Eschewing the fundamental scientific and philosophi-       can correctly translate Logic Condition Tables (LCTs) to Hardware
                                         cal questions about whether LLMs understand semantic meaning              Description Language (HDL) code, while detecting both LLM en-
                                         or operate syntactically on form [4], we adopt an utilitarian and         coding/decoding errors and assisting developers in finding inherent
                                         engineering approach of focusing on how to direct LLMs to produce         design specification errors, thus significantly increasing designer
                                         correct, complete, and concise output for invertible problems.            productivity.
                                            Comparable to lossless compression in information theory, we              Precise specification using LCTs ensures all design information
                                         propose using LLMs as an encoder (from a source context into a des-       is completely and correctly defined. An LCT succinctly specifies
                                         tination) followed by as a decoder (from the destination context back     system input conditions and corresponding output results in ta-
                                         into the source), and then verifying that this results in an identity     ble columns for each case of values in table rows (see Section 3).
                                         map. The input itself becomes the ground truth for axiomatically          The closed loop solution using LLMs as an invertible transform to
                                         asserting correctness [16]. Note that while this approach mitigates       verify the implementation is shown in Fig. 1. An LLM performs
                                         hallucinations and omissions, it does not mathematically eliminate        a transform T from an input token sequence S𝑝𝑟𝑜𝑚𝑝𝑡 to an out-
                                         them because either the encoder phase, the decoder phase, or both         put token sequence S𝑟𝑒𝑠𝑝𝑜𝑛𝑠𝑒 . Mathematically, the transform is
                                         might introduce self-cancelling hallucinations producing a match.         defined as: S𝑟𝑒𝑠𝑝𝑜𝑛𝑠𝑒 = T (S𝑝𝑟𝑜𝑚𝑝𝑡 ) where the transform input
                                         Therefore, formal verification is still necessary. Many classes of        and output are token sequences: S𝑝𝑟𝑜𝑚𝑝𝑡 = {𝑠 0, 𝑠 1, 𝑠 2, ..., 𝑠𝑛−1 } and
                                         such practical problems exist, for example, translating COBOL into        S𝑟𝑒𝑠𝑝𝑜𝑛𝑠𝑒 = {𝑠 0, 𝑠 1, 𝑠 2, ..., 𝑠𝑚−1 } respectively. The LLM transform T
                                         Java/C++, translating English into Spanish, and translating JSON          can be applied in the forward or encode direction to generate Ver-
                                         into XML/YAML/CSV formats. This approach is grounded in recent            ilog HDL from a specification. Or the LLM transform T −1 can be
                                         results that language models are injective and hence invertible [21]      applied in the inverse or decode direction to reconstruct the original
                                         and is inspired by well studied autoencoders for lossy compression        LCT specification from the Verilog HDL. Applying these encoder /
                                         [15].                                                                     decoder transforms forms an autoencoder.
                                                                        Andrew S. Cassidy, Guillaume Garreau, Jay Sivagnaname, Mike Grassi, Bernard Brezzo,
                                                                                                                       John V. Arthur, Dharmendra S. Modha


Table 1: Example combinational LCT: 4-input MUX. Table                     Table 2: Example sequential LCT: registered 2-input MUX
columns contain input conditions (blue) and output results                 with data valid and backpressure (ready).
(green). Table rows contain cases.
                                                                                           Inputs                          Outputs               Comments
    Case                 Inputs            Outputs    Comments               rst_n    ready valid_in       select    valid_out data_out
                enable            select   data_out                            0        X         X          X           0          0            Reset
      0           0                 X          0      Disabled                 1        0         X          X       valid_out data_out          Backpress
      1           1                 0       data0     output 1𝑠𝑡 data          1        1         0          X           0          0            No input
      2           1                 1       data1     output 2𝑛𝑑 data          1        1         1          0           1        data0          Select 0
      3           1                 2       data2     output 3𝑟𝑑 data          1        1         1          1           1        data1          Select 1
      4           1                 3       data3     output 4𝑡ℎ data
                                                                           Table 3: Example Finite State Machine LCT with four states,
                                                                           two outgoing transitions per state—selected by cond0 and
                                                                           cond1, and three output results.

   Using the autoencoder as a verification method, the original                             Inputs                                 Outputs
input LCT specification and the reconstructed output LCT speci-               rst_n    state cond0       cond1      next_state      out0 out1       out2
fication are compared. If the input and output LCTs don’t match,                0        X        X        X            0            0     0         0
one of three cases is true:                                                     1        X        0        0          state         out0 out1       out2
                                                                                1        0        1        0            0            1     0         0
    (1) an error in the encode/forward transform (LLM error),                   1        0        0        1            2            1     0         0
    (2) error in the decode/inverse transform (LLM error),                      1        1        1        0            2            0     0         1
    (3) or inadequate original specification (designer error).                  1        1        0        1            3            0     0         1
                                                                                1        2        1        0            3            0     1         1
As a result, our approach is a verification method primarily for                1        2        0        1            0            0     1         1
checking the LLM’s work and only secondarily the LCT specifi-                   1        3        1        0            1            1     1         0
cation. Note that our approach’s ability to check the input LCT                 1        3        0        1            1            1     1         0
specification itself is limited. If the designer defines the wrong
function with a complete, well-formed input LCT specification,             Table 4: Hierarchical Connectivity Table: The lower row is
our approach will correctly implement the wrong function. Thus,            repeated for all ports in a module instantiation.
functional verification of the input specification and overall design
is still necessary, as well as to cover the case of self-cancelling
                                                                             Port Direc-   Port Name      Net Name               Size (bits)   Net Context
hallucinations.                                                              tion
                                                                             {input,       module         interconnection        {# bits}      {internal, ex-
2   Background                                                               output}       signal         signal                               ternal}

Boolean Truth Tables [35, 28] form the basis of digital logic design.
Programmable digital computing circuits, such as EDVAC [33] and            3 Approach
ENIAC [14], followed closely after. As succeeding decades brought
innovations in programming these computing machines, Decision              3.1 Logic Condition Tables (LCTs)
Tables [26, 27, 9, 32] were developed as a means for specifying            LCTs are an efficient representation of logic design blocks, including
programatic thinking. They concisely specify the actions to take for       both combinational and sequential circuits. Derived from Decision
any given input condition to the system in a table format. Boolean         Tables and their cousins, the Boolean Truth Table, examples of the
Truth Tables and Decision Tables are the foundation of the LCTs            basic LCT structure are shown in Table 1 (combinational 4-input
described in Section 3. LCTs were first applied to auditing the logic      MUX), Table 2 (registered 2-input MUX), and Table 3 (4-state Finite
of a 22B transistor Neural Inference Processor [20, 7] prior to tape-      State Machine). Table columns contain the set of input conditions
out. Used as a formal verification methodology, over 160 LCTs were         to the design and the set of output results/actions produced by
manually constructed from the Verilog source code, one per process         the design. Table rows contain the set of cases, which define the
statement on selected logic units. The tables, representing the un-        result to produce (or action to take), given the specific set of input
derlying logic, were then checked for correctness and completeness.        conditions. The first column, “Case,” is not required, it is just shown
As a result, the processor was successful in first pass silicon.           for illustration. The last column, “Comments,” is optional, however,
   A wide variety of approaches containing natural language de-            it is useful for human table designers (and potentially for the LLM
scriptions of logic designs, have been developed to test LLM ap-           as well—but that hypothesis is untested in this paper). Observe that
proaches for automated logic generation. Examples include: model           neither conditions nor outputs are required to be binary valued.
fine tuning [31], data augmentation [11, 19, 6, 29], instruction tun-      Condition headers may be a signal name, or may be an actual logical
ing [37], feedback-directed refinement [34, 5], and extracting logic       or arithmetic condition (for example: 𝐴&∼𝐵 or 𝐶 ≤ 10). The “don’t
equations from natural language [30].                                      care” symbol is “X.” In most logic designs there are many “don’t
Mitigating hallucinations and omissions in LLMs for invertible problems: An application to hardware logic design automation


                  Table 5: LLM Model Comparison                                           3.2     Closed Loop Design Flow
                                                                                          The closed loop design flow follows Fig. 1. The automation of steps
 Model               Developer      Ref.   Release       Parameters     Context           2, 3, and 4 drive developer productivity improvement.
                                                                        (tokens)
                                                                                                (1) (Human) designer specifies the logic as an LCT.
 Claude Sonnet-      Anthropic      [1]    Sep-2025      “frontier”     200K
 4.5
                                                                                                (2) Apply the LLM transform T to the LCT to generate the
 Gemini2.5-Pro       Google         [12]   Mar-2025      “large”        1M                          Verilog HDL.
 Gemini2.5-          Google         [12]   Jun-2025      “small”        1M                      (3) Apply the LLM inverse transform T −1 to the generated
 Flash                                                   est.17B                                    Verilog HDL to reconstruct the original LCT specification.
 ChatGPT-5           OpenAI         [23]   Aug-2025      “frontier”     400K                    (4) Compare the original LCT specification with the recon-
 ChatGPT-5-          OpenAI         [23]   Aug-2025      “small”        400K                        structed LCT specification.
 mini                                                                                           (5) Fix any errors (and repeat from 2. if necessary).
 Llama-4-            Meta           [17]   Apr-2025      17B active,    128K
 maverick17b-                                            400B total
 128e-instruct                                                                            3.3     Forward Transform Prompt
 Llama-3-405b-       Meta           [13]   Jul-2024      405B           128K              For the forward transform, the prompt is simple, using the LCT as
 instruct                                                                                 the specification together with the Verilog port map. The prompt
                                                                                          consisted of the following:
                                                                                                (1) Specify clocked or combinational Verilog.
                                                                                                (2) Specify the LCT columns (# input condition columns and #
                                                                                                    output result columns).
                                                                                                (3) List the LCT in CSV format.
care” cases, leading to a significant compression of rows relative                              (4) Define the Verilog port map, including the module input
to the possible number of cases. The table rows display a natural                                   and output signals.
hierarchy of nested ‘if’ and/or ‘case’ statements.
    Table 2 defines a simple registered 2-input multiplexor, with a                       3.4     Inverse Transform Prompt
data valid signal and backpressure (ready) signal. In the backpres-                       For the inverse transform, the prompt is more involved, as LCTs
sure case, the 𝑣𝑎𝑙𝑖𝑑_𝑜𝑢𝑡 and 𝑑𝑎𝑡𝑎_𝑜𝑢𝑡 registers should hold their                         are unknown to LLMs and thus LLMs have not been trained to
value (do not update), denoted by entering the output signal name                         generate LCTs. The prompt consisted of the following:
into the corresponding table cell. Table 3 defines an example four                              (1) Short natural language definition of an LCT.
state Finite State Machine (FSM), where each state has two possible                             (2) List a full example of a Verilog HDL (MUX2 design).
outgoing transitions, selected by input conditions 0 and 1.                                     (3) List a full example of the corresponding LCT (MUX2 de-
    LCTs are particularly well suited for specifying the parallelism                                sign).
of logic circuits, as many output signals can be driven by the same                             (4) List the Verilog to evaluate.
input condition set. In addition, logic circuits can be partitioned                             (5) Define the input condition and output result column head-
into multiple LCTs, subdividing the complexity, similar to parallel                                 ers for the LCT to be reconstructed.
process blocks in HDL. As the LCT itself does not specify clock-
ing, we specify in the prompt whether each LCT is “clocked” or                            3.5     LLM Models
“combinational” to direct the LLM to implement a clocked process
(sequential) circuit or unclocked (combinational) circuit. The tim-                       Table 5 summarizes the LLM Models used in this paper. All models
ing semantics are the same as standard logic design. Clocked LCTs                         are publicly available and used “off-the-shelf,” without retraining,
are state holding and retain their state from the prior clock cycle.                      fine tuning, augmentation, or any other modification.
Unclocked LCTs do not retain state from the prior clock cycle.
    One significant advantage of the LCTs is that they compel human                       4     Experiment: 2D Network-on-Chip Router
logic designers into a disciplined and structured design methodol-                        We tested our approach on a 2D Mesh Network-on-Chip (NoC)
ogy. In constructing the LCT, human designers must think through                          Router design, comprised of 13 hierarchical design units, and rep-
both the conditions and the results of each case. All condition cases                     resentative in complexity of an industry design. The router design
should be enumerated. Checks, transforms, and optimizations can                           was specified via LCTs by a human logic designer. The LCTs were
be applied to LCTs, however, full treatment of these subjects is                          given to an LLM to generate Verilog HDL in the forward transform.
outside the scope of this paper.                                                          The generated Verilog HDL was then given to an LLM to regenerate
    An example connectivity table definition for hierarchical design                      the original LCT specification in the inverse transform.
is shown in Table 4. A simple definition, similar to a standard HDL                          The 2D NoC Router design is depicted in Fig. 2. In the context of
port map, it defines the connectivity for all ports of a module. Net                      a 2D core array, adjacent cores in the North, South, East, and West
context defines whether a signal interconnects to other modules or                        directions are interconnected via a 2D router (RTR). The router also
to the external ports (up a level of hierarchy). Connectivity tables                      has a Local connection from the 2D network to a local Processing
are not the focus of this paper, however, they also proved to be an                       Element (PE) in the same core. All links are bidirectional and the TX
effective specification for LLMs.                                                         link from one core connects to the RX link of the adjacent core. The
                                                                                             Andrew S. Cassidy, Guillaume Garreau, Jay Sivagnaname, Mike Grassi, Bernard Brezzo,
                                                                                                                                            John V. Arthur, Dharmendra S. Modha


        Inputs (RX)                   Router (RTR)                       Outputs (TX)

        N                                                                             N              (3,0)               (3,1)            (3,2)             (3,3)
                                                                                              RTR                RTR               RTR               RTR
        S                                                                             S
                                                     Crossbar
        E                                                                             E              PE                  PE               PE                PE
                                                      Switch
        W                                                                             W                              N
        L                                                                             L
                                                                                                     (2,0)   W           (2,1)            (2,2)             (2,3)
                                                                                              RTR                RTR               RTR               RTR
                 Input Buffers (FIFOs)                                                                                    E
                                                                                                     PE          S     L PE               PE                PE

             Head/      Flow      North
            Tail Gen   Control   Request
                                                                                                     (1,0)               (1,1)            (1,2)             (1,3)
             Head/      Flow      South                                                       RTR                RTR               RTR               RTR
            Tail Gen   Control   Request

             Head/      Flow       East                                                              PE                  PE               PE                PE
            Tail Gen   Control   Request

             Head/      Flow      West
            Tail Gen   Control   Request
                                                                                                     (0,0)               (0,1)            (0,2)             (0,3)
             Head/      Flow      Local                                                       RTR                RTR               RTR               RTR
            Tail Gen   Control   Request

                                           Merge     Merge     Merge     Merge     Merge
                                                                                                     PE                  PE               PE                PE
                                           Arbiter   Arbiter   Arbiter   Arbiter   Arbiter
                   Crossbar
                    Switch                 MUX 4     MUX 4     MUX 4      MUX 4    MUX 4

                                             N         S         E         W         L              Router Core Processing Element


Figure 2: 2D NoC Router Design: (Right) Two dimensions array of cores, each core contains a router (RTR) and a processing
element (PE). Each core connects to neighboring cores via North (N) and South (S) connections in the Y-dimension, East (E)
and West (W) connections in the X-dimension, as well as from the core router to the core processing element via the Local
(L) connection. (Upper Left) The Router is comprised of five input channels with input buffers and five output channels,
interconnected via a crossbar switch. (Lower Left) The crossbar switch contains the logic for routing the packets.


router is composed of five input FIFOs and a non-blocking cross-                                unit meters the flow of input packets into the crossbar based on
bar switch. We divided the router into eleven logic design units                                the grant signals. All units use 𝑣𝑎𝑙𝑖𝑑 and 𝑟𝑒𝑎𝑑𝑦 signaling for packet
(𝐹 𝐼 𝐹𝑂, 𝑟𝑒𝑔_𝑠𝑡𝑎𝑔𝑒, 𝑓 𝑙𝑜𝑤_𝑐𝑜𝑛𝑡𝑟𝑜𝑙, ℎ𝑒𝑎𝑑_𝑡𝑎𝑖𝑙_𝑔𝑒𝑛, 𝑚𝑟𝑔_𝑎𝑟𝑏, 𝑚𝑢𝑥4,                                flow control within the router unit and on {N,S,E,W,L} routing links.
𝑟𝑒𝑞𝑢𝑒𝑠𝑡_𝑁 , 𝑟𝑒𝑞𝑢𝑒𝑠𝑡_𝑆, 𝑟𝑒𝑞𝑢𝑒𝑠𝑡_𝐸, 𝑟𝑒𝑞𝑢𝑒𝑠𝑡_𝑊 , 𝑟𝑒𝑞𝑢𝑒𝑠𝑡_𝐿), and two                               5    Results
hierarchical connectivity units (𝑟𝑒𝑞𝑢𝑒𝑠𝑡_𝑡𝑜𝑝, 𝑟𝑡𝑟 _𝑡𝑜𝑝). The function
of each logic design unit is specified by an LCT. The specification                             The results for LLM logic generation using seven different models
of each connectivity unit, which contains no logic, is a mapping                                are summarized in Table 6, using functional simulation to check the
table from source unit and signal to destination unit and signal.                               logic. There are 11 logic units and 2 connectivity units. Using only
    The 2D NoC is designed to support variable length packets and a                             the Pass@1 metric [8] for both syntax and functionality, two LLM
dimension-ordered X-Y routing protocol, which routes horizontally,                              models correctly designed all 13 units with 100% success. Two LLM
followed by vertically, followed by locally. The first word of the                              models had only single compile errors (requiring only 2 lines of
packet is the header word, comprised of three fields: the X-address                             code each to be fixed). Two additional LLM models had insufficient
for East-West routing, the Y-address for North-South routing, and                               context length to generate the largest design unit. Aside from the
the length field which specifies the packet payload size in words.                              insufficient context length, all units were fully functional with
The FIFO is a standard synchronous, dual-port FIFO. Using the                                   less than 15 lines of code modified (out of 1500-2000 lines of code
length field, the ℎ𝑒𝑎𝑑_𝑡𝑎𝑖𝑙_𝑔𝑒𝑛 unit generates a single-cycle “head”                            generated, depending on the LLM model).
signal that aligns with the first word in the packet, and a single-                                The inverse transform from HDL to LCT was performed by the
cycle “tail” signal that aligns with the last word in the packet. The                           Gemini2.5-Pro model for all units, across all HDL generating (for-
request units perform X-Y address comparisons with the core X-Y                                 ward transform) models. Using different LLMs in the forward and
IDs to implement the routing rules and generate requests to the                                 inverse transforms separates the design and the check, similar to
arbiter. The 𝑚𝑟𝑔_𝑎𝑟𝑏 unit arbitrates between incoming requests                                  separate human designers and verifiers in traditional logic design
to a given output channel and issues a grant based on a round-                                  and verification methodology. The 𝑟𝑒𝑔_𝑠𝑡𝑔 and 𝑓 𝑖 𝑓 𝑜 units were
robin policy. Arbitration is only performed on the head word of                                 split into multiple LCTs for recreation by process statement, match-
packets, and maintained until the tail word is received. Based on                               ing the generation LCT structure. The inverse transform results are
the selected incoming request, the 𝑚𝑢𝑥4 unit outputs the correct                                summarized in Table 7, demonstrating not only the ability to recon-
packet. In conjunction with the 𝑟𝑒𝑔_𝑠𝑡𝑎𝑔𝑒 unit, the 𝑓 𝑙𝑜𝑤_𝑐𝑜𝑛𝑡𝑟𝑜𝑙                               struct the LCT specification from the LLM generated HDL logic,
                                                                                                but also the ability to detect errors of hallucination and omission.
Mitigating hallucinations and omissions in LLMs for invertible problems: An application to hardware logic design automation


Table 6: Router Experiment Results: Syntax errors in generated logic are denoted as S. Functional errors in generated logic are
denoted as F. The number of errors is denoted as #E and the number of lines of code to fix the errors are denoted as #L. DNF is
Did Not Finish, due to insufficient context length.

 Forward Model           reg_stg     flow_ctrl    head_tail     mrg_arb      mux4      req_N     req_S      req_E      req_W      req_L      fifo     req_top    rtr_top
 ClaudeSonnet-4.5         PASS         PASS         PASS         PASS        PASS      PASS      PASS       PASS        PASS      PASS      PASS       PASS       PASS
 Gemini2.5-Pro            PASS         PASS         PASS         PASS        PASS      PASS      PASS       PASS        PASS      PASS      PASS       PASS       PASS
 Gemini2.5-Flash          PASS         PASS         PASS         PASS        PASS      PASS      PASS       PASS        PASS     S:1E,2L    PASS       PASS       PASS
 ChatGPT-5                PASS         PASS         PASS         PASS        PASS      PASS      PASS       PASS        PASS     S:1E,2L    PASS       PASS       PASS
                                                   S:2E,6L,                                                                                S:1E,1L,
 ChatGPT-5-mini           PASS         PASS                      F:1E,1L     PASS      PASS      PASS       PASS       PASS       PASS                 PASS      PASS
                                                   F:1E,2L                                                                                 F:3E,4L
 Llama-4-maverick         PASS         PASS        F:2E,2L        PASS       PASS      PASS      PASS       PASS        PASS      PASS     F:3E,4L     PASS       DNF
 Llama-3-405b             PASS         PASS         PASS          PASS       PASS      PASS      PASS      F:2E,2L     F:2E,2L   F:3E,3L    PASS       PASS       DNF


Table 7: Comparison results between input LCT specification and reconstructed LCT specification (generated by Gemini2.5-Pro
LLM). Table key: green = all correct, orange = forward transform error, blue = inverse transform error, yellow = designer
specification error. Notation: M = correctly identified LCT match, M SP = correctly identified LCT match—functional fail due to
incomplete designer specification, X EQ = correctly identified LCT mismatch but functionally equivalent, X FW = correctly
identified LCT mismatch in the forward transform, X FW∼S = correctly identified LCT mismatch in the forward transform that
was not caught by functional simulation test cases, and X INV = correctly identified LCT mismatch in the inverse transform.

 Forward Model           reg_stg     flow_ctrl head_tail      mrg_arb      mux4      req_N     req_S     req_E       req_W     req_L                  fifo
 Claude-Sonnet-4.5       M M            M         M              M          M          M         M         M           M         M      M       M         M        M
 Gemini2.5-Pro           M M            M         M              M          M          M       X EQ        M           M         M      M       M         M        M
 Gemini2.5-Flash         M M            M         M              M          M          M       X EQ        M           M         M      M       M         M     X FW∼S
 ChatGPT-5               M M            M         M              M          M          M         M         M           M       X INV    M       M         M        M
 ChatGPT-5-mini          M M            M       X FW           M SP         M          M       X EQ        M           M         M     M SP    M SP       M        M
 Llama-4-maverick        M M            M       X FW          X FW∼S        M          M       X EQ        M           M         M     M SP    M SP       M        M
 Llama-3-405b            M M            M         M           X FW∼S        M          M         M       X FW        X FW      X FW     M       M         M        M


Both types of error, hallucination and omission, can occur in the                                  HDL generation, the unused output was dropped from the
forward transform, inverse transform, and/or designer specifica-                                   HDL, and thus not included in the reconstructed LCT.
tion. An example hallucination in the forward transform: invalid                                     • Yellow = Designer specification error.
routing rules (model Llama-3, unit 𝑟𝑒𝑞_𝐸). An example omission in                              (4) MISMATCH: X FW = mismatching comparison between
the forward transform: priority encoder cases dropped during HDL                                   LCTs correctly caught the functional error in the forward
generation (model Llama-4 unit 𝑚𝑟𝑔_𝑎𝑟𝑏) .                                                          transform generating the HDL.
   Comparing the original and reconstructed LCTs in Table 7, with                                    • Orange = Forward transform error.
respect to Table 6, the following cases emerge:                                                (5) MISMATCH: X FW∼S = mismatching comparison between
                                                                                                   LCTs correctly caught errors not caught in functional sim-
                                                                                                   ulation, due to missing testbench test cases.
    (1) MATCH: M = 100% match between original LCT and recon-                                        • Orange = Forward transform error.
        structed LCT, indicating correctly generated logic.                                    (6) MISMATCH: X INV = mismatching comparison between
           • Green = Forward transform correct, inverse transform                                  LCTs due to INV transform error. The specific case found
              correct, and designer specification correct.                                         corresponds to a forward transform syntax error, which
    (2) MATCH: M SP = 100% match between original LCT and re-                                      may have hindered the performance of the inverse trans-
        constructed LCT, however, functional simulation indicated                                  form.
        a failure (Table 6). Closer inspection revealed subtle errors                                • Blue = Inverse transform error.
        in the specification, not defined by the LCT (for example, a
        bitwidth mismatch). If the original LCT does not contain                          Note that when comparing Table 7 versus Table 6, the focus is on
        the information, the HDL cannot be reliably generated, nor                        correctly identifying the functional errors (F), ignoring the syntax
        the LCT reliably reconstructed.                                                   errors (S) in the forward transform. In addition, the units 𝑟𝑒𝑞_𝑡𝑜𝑝
           • Yellow = Designer specification error.                                       and 𝑟𝑡𝑟 _𝑡𝑜𝑝 are connectivity tables, as opposed to LCTs, and were
    (3) MISMATCH: X EQ = mismatching comparison between                                   not checked, but there is nothing fundamentally blocking their
        LCTs, however, closer inspection revealed logically and                           evaluation with the same flow.
        functionally equivalent tables. This particular case was due                         The following additional results did not affect the MATCH /
        to an unused output specified in the original LCT. During                         MISMATCH comparison and were not annotated in Table 7:
                                                                         Andrew S. Cassidy, Guillaume Garreau, Jay Sivagnaname, Mike Grassi, Bernard Brezzo,
                                                                                                                       John V. Arthur, Dharmendra S. Modha


     • Reordering (permuting) the rows and/or columns of an                      (5) Reproducibility: By precisely defining logical function,
       LCT is a valid table transformation that does not change                      LCTs are a reproducible specification, invariant across mod-
       the functional specification of the LCT.                                      els, runs, and design styles.
     • Another valid LCT transform is to expand “don’t care” cases             We learned two general lessons for generating useable logic with
       into enumerated cases. This changes the LCT contents, but            LLMs. First, it is crucial for designers to be complete and precise
       generates a functionally equivalent LCT.                             in specification. Anything left unspecified or ambiguously speci-
     • Minor specification gaps in the original LCTs were identi-           fied is open to misinterpretation and misimplementation. Second,
       fied (e.g. missing reset case), but did not affect the results.      breaking down designs into sufficiently small levels of complex-
     • Minor differences in signal names, such as abbreviations             ity contributed to successful LLM logic generation. The larger the
       or suffixes were inconsequential and ignored. Similarly,             complexity of the design unit, the higher the chance of generation
       differences in numerical types, such as 3′𝑑5 and 3′𝑏101,             mistakes. In our experimental 2D NoC Router design, the size of
       that are logically equivalent are also ignored.                      the LCTs generally comprised tens of table cells (rows × columns),
     • Additional default cases for fully specified case statements         ranging up to several hundred table cells for the merge arbiter.
       were inserted by the LLMs to cover uninitialized signals             Separate experiments demonstrated successful logic generation
       (𝑋 ′𝑠), but have no bearing on functional logic.                     (forward transform, checked by functional simulation) of synthetic
                                                                            FSM LCTs into the range of thousands of table cells.
While these issues prevent direct one-to-one comparison of LCTs,
we do not see any significant technical hurdles blocking automa-            7    Conclusion
tion of the LCT comparison step to determine logical equivalence,           The primary impact of this work is the demonstration of an invert-
completing the closed-loop methodology (Section 3.2).                       ible design flow using LLMs. By encoding a specification from a
   Note that it is possible that an error in the forward transform          source context into a destination context using an LLM, and then
could be cancelled out by the opposite error in the inverse transform,      decoding from the destination context back into the source context,
leading to an undetected forward transform error. While unlikely,           also using an LLM, the reconstructed specification can be directly
using different LLM models for the forward and inverse transforms           compared with the original specification to assert the veracity of the
(as done in Table 7) reduces this possibility even further.                 results. We used this approach to successfully detect both matching
                                                                            and mismatching LCTs, corresponding to functionally correct and
6   Discussion                                                              functionally erroneous HDL respectively. This development rep-
                                                                            resents an important catalyst for integrating LLMs in EDA design
Summarizing the results, we applied an LLM forward transform to             flows to accelerate the development and verification time of logic
LCTs, generating Verilog HDL to design a fully functional 2D NoC            hardware designs. The forward (encoder) pass adds a new tool in
Router. Then, after sufficiently augmenting the prompt to teach             accelerating design. The inverse (decoder) pass adds a new tool in
LLMs about LCTs by example, we successfully used the LLM in-                aiding correctness. Together, they form a closed-loop design flow
verse transform to reconstruct the LCT specifications. Comparing            with built-in checking for errors due to LLM hallucinations and
original and reconstructed LCTs successfully detected all five func-        omissions. In addition, the LCT specification itself is an important
tional errors in the forward transform found by simulation, while           contribution to high-quality automated logic generation through
also detecting three more forward transform errors, not found by            complete, concise, and correct specification.
simulation. The reconstruction step only introduced one inverse                We demonstrated our results using 100% publicly available, off-
transform error for additional review. The final three functional           the-shelf LLMs. We note that the top three performing models:
errors were due to incomplete or ambiguous specification. Our ap-           Claude Sonnet4.5, Gemini2.5-Pro, and ChatGPT5 are models that
proach cannot be faulted for missing these, as it can only create           use multi-step “thinking” and perform well on coding and complex
and reconstruct based on the information that it has. No penalty            reasoning tasks. Going forward, we expect that LLM approaches
for information it does not have.                                           that combine logic compilation, synthesis engines, simulations, and
   Using LCTs for specification addresses five challenges for gener-        boolean logic reasoning with pure LLM will outperform in logic
ating logic HDL using LLMs.                                                 generation. Moreover, LLMs can be co-trained and fine-tuning to
                                                                            improve task performance on logic generation using LCT specifica-
    (1) Scale: LCTs are inherently modular. They can be composed            tions for further task performance gains.
        using connectivity tables. Hierarchy demonstrated with the             While the large, frontier LLMs performed the best, we note
        2D NoC Router design.                                               the trend towards medium/small models, for example, the 17B
    (2) Complexity: LCTs concisely capture a large number of in-            parameter Gemini2.5-Flash and the Llama4-maverick mixture-of-
        put conditions and output results. Complex forward-backward         experts with 17B active parameters performed reasonably well
        flow control demonstrated with the 2D NoC Router design             for a significantly smaller computational footprint. We expect to
        and scaling complexity into tables with hundreds of cells.          see in the future more smaller models [3, 24] trained for domain
    (3) Completeness: An LCT with full coverage of all cases,               specific tasks for optimized computational performance [18]. This
        conditions, and results is a completely specified design.           bodes well for sustaining the energy costs of computation [22, 25,
    (4) Specificity: LCT cases (table rows) precisely define logi-          2] brought about by the demand for the latest AI capabilities.
        cal relationships from input conditions to output results,
        leaving no room for ambiguous interpretation of function.
Mitigating hallucinations and omissions in LLMs for invertible problems: An application to hardware logic design automation


References                                                                                [20]   Dharmendra S Modha et al. 2023. Neural inference at the frontier of energy,
 [1]   Anthropic, PBC. 2025. Claude. Retrieved Oct. 30, 2025 from https://claude.ai/.            space, and time. Science, 382, 6668, 329–335.
 [2]   Rathinakumar Appuswamy et al. 2024. Breakthrough low-latency, high-energy-         [21]   Giorgos Nikolaou, Tommaso Mencattini, Donato Crisostomi, Andrea Santilli,
       efficiency LLM inference performance using NorthPole. In 2024 IEEE High                   Yannis Panagakis, and Emanuele Rodolà. 2025. Language models are injective
       Performance Extreme Computing Conference (HPEC), 1–8. doi:10.1109/HPEC628                 and hence invertible. (2025). https://arxiv.org/abs/2510.15511 arXiv: 2510.15511
       36.2024.10938418.                                                                         [cs.LG].
 [3]   Peter Belcak, Greg Heinrich, Shizhe Diao, Yonggan Fu, Xin Dong, Saurav             [22]   Jesse Noffsinger, Mark Patel, Pankaj Sachdeva, Arjita Bhan, Haley Chang, and
       Muralidharan, Yingyan Celine Lin, and Pavlo Molchanov. 2025. Small language               Maria Goodpaster. 2025. The cost of compute: a $7 trillion race to scale data
       models are the future of agentic AI. (2025). https://arxiv.org/abs/2506.02153             centers. McKinsey & Company Insights, (Apr. 2025). https://www.mckinsey.co
       arXiv: 2506.02153 [cs.AI].                                                                m/industries/technology-media-and-telecommunications/our-insights/the-c
 [4]   Emily M Bender and Alexander Koller. 2020. Climbing towards nlu: on meaning,              ost-of-compute-a-7-trillion-dollar-race-to-scale-data-centers.
       form, and understanding in the age of data. In Proceedings of the 58th annual      [23]   OpenAI. 2025. GPT-5 is here. Retrieved Nov. 8, 2025 from https://openai.com/g
       meeting of the association for computational linguistics, 5185–5198.                      pt-5/.
 [5]   Jason Blocklove, Shailja Thakur, Benjamin Tan, Hammond Pearce, Siddharth           [24]   Aldo Pareja et al. 2024. Unveiling the secret recipe: a guide for supervised
       Garg, and Ramesh Karri. 2025. Automatically Improving LLM-based Verilog                   fine-tuning small LLMs. (2024). https : / / arxiv . org / abs / 2412 . 13337 arXiv:
       Generation using EDA Tool Feedback. ACM Trans. Des. Autom. Electron. Syst.,               2412.13337 [cs.LG].
       30, 6, Article 100, (Oct. 2025), 26 pages. doi:10.1145/3723876.                    [25]   Konstantin F. Pilz, Yusuf Mahmood, and Lennart Heim. 2025. AI’s Power Re-
 [6]   Paul E. Calzada, Zahin Ibnat, Tanvir Rahman, Kamal Kandula, Danyu Lu, Sujan               quirements Under Exponential Growth: Extrapolating AI Data Center Power
       Kumar Saha, Farimah Farahmandi, and Mark Tehranipoor. 2025. VerilogDB:                    Demand and Assessing Its Potential Impact on U.S. Competitiveness. Tech. rep.
       The Largest, Highest-Quality Dataset with a Preprocessing Framework for                   RR-A3572-1. RAND Corporation. doi:10.7249/RRA3572-1.
                                                                                          [26]   Solomon L Pollack. 1963. Analysis of the decision rules in decision tables. Tech.
       LLM-based RTL Generation. (2025). https://arxiv.org/abs/2507.13369 arXiv:
                                                                                                 rep.
       2507.13369 [cs.AR].
                                                                                          [27]   Udo W Pooch. 1974. Translation of decision tables. ACM Computing Surveys
 [7]   Andrew S Cassidy et al. 2024. IBM NorthPole: an architecture for neural net-
                                                                                                 (CSUR), 6, 2, 125–151.
       work inference with a 12nm chip. In 2024 IEEE International Solid-State Circuits
                                                                                          [28]   Emil L Post. 1921. Introduction to a general theory of elementary propositions.
       Conference (ISSCC). Vol. 67. IEEE, 214–215.
                                                                                                 American journal of mathematics, 43, 3, 163–185.
 [8]   Mark Chen et al. 2021. Evaluating large language models trained on code. CoRR,
                                                                                          [29]   Brendan Roberts. 2025. Improving LLM Performance in Generating Verilog by
       abs/2107.03374. https://arxiv.org/abs/2107.03374 arXiv: 2107.03374.
                                                                                                 Fine Tuning with a Translated Code Dataset. (May 2025). https://www2.eecs.b
 [9]   CODDASYL. 1982. A modern appraisal of decision tables. Report of the Decision
                                                                                                 erkeley.edu/Pubs/TechRpts/2025/EECS-2025-104.pdf.
       Table Task Group, 230–232.
                                                                                          [30]   Prithwish Basu Roy, Akashdeep Saha, Manaar Alam, Johann Knechtel, Michail
[10]   Harvey Yiyun Fu, Aryan Shrivastava, Jared Moore, Peter West, Chenhao Tan,
                                                                                                 Maniatakos, Ozgur Sinanoglu, and Ramesh Karri. 2025. Veritas: Deterministic
       and Ari Holtzman. 2025. Absencebench: language models can’t tell what’s
                                                                                                 Verilog Code Synthesis from LLM-Generated Conjunctive Normal Form. (2025).
       missing. (2025). https://arxiv.org/abs/2506.11440 arXiv: 2506.11440 [cs.CL].
                                                                                                 https://arxiv.org/abs/2506.00005 arXiv: 2506.00005 [cs.AR].
[11]   Mingzhe Gao, Jieru Zhao, Zhe Lin, Wenchao Ding, Xiaofeng Hou, Yu Feng, Chao
                                                                                          [31]   Shailja Thakur, Baleegh Ahmad, Hammond Pearce, Benjamin Tan, Brendan
       Li, and Minyi Guo. 2024. AutoVCoder: A Systematic Framework for Automated
                                                                                                 Dolan-Gavitt, Ramesh Karri, and Siddharth Garg. 2023. VeriGen: A Large
       Verilog Code Generation using LLMs. (2024). https://arxiv.org/abs/2407.18333
                                                                                                 Language Model for Verilog Code Generation. (2023). https://arxiv.org/abs/230
       arXiv: 2407.18333 [cs.AR].
                                                                                                 8.00708 arXiv: 2308.00708 [cs.PL].
[12]   Google, Inc. 2025. Google Gemini. Retrieved Oct. 30, 2025 from https://gemini
                                                                                          [32]   J Vanthienen and E Dries. 1997. Decision tables: refining the concept and a
       .google.com.
                                                                                                 proposed standard. Communications of the ACM.
[13]   Aaron Grattafiori et al. 2024. The Llama 3 Herd of Models. (2024). https://arxiv
                                                                                          [33]   John von Neumann. 1945. First Draft of a Report on the EDVAC. Tech. rep. Con-
       .org/abs/2407.21783 arXiv: 2407.21783 [cs.AI].
                                                                                                 tract No. W-670-ORD-4926. Moore School of Electrical Engineering, University
[14]   Douglas Rayner Hartree. 1946. The ENIAC, an electronic computing machine.
                                                                                                 of Pennsylvania, Philadelphia, PA, USA, (June 1945).
       Nature, 158, 4015, 500–506.
                                                                                          [34]   Anjiang Wei, Huanmi Tan, Tarun Suresh, Daniel Mendoza, Thiago S. F. X. Teix-
[15]   Robert Hecht-Nielsen. 1995. Replicator neural networks for universal optimal
                                                                                                 eira, Ke Wang, Caroline Trippel, and Alex Aiken. 2025. VeriCoder: Enhancing
       source coding. Science, 269, 5232, 1860–1863.
                                                                                                 LLM-Based RTL Code Generation through Functional Correctness Validation.
[16]   Charles Antony Richard Hoare. 1969. An axiomatic basis for computer pro-
                                                                                                 (2025). https://arxiv.org/abs/2504.15659 arXiv: 2504.15659 [cs.AR].
       gramming. Communications of the ACM, 12, 10, 576–580.
                                                                                          [35]   Ludwig Wittgenstein. 2010. Tractatus Logico-Philosophicus. Trans. by C.K. Og-
[17]   Meta AI. 2025. meta-llama/Llama-4-Maverick-17B-128E-Original.
                                                                                                 den. Original work published 1922. Project Gutenberg.
       url https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Original.
                                                                                          [36]   Ziwei Xu, Sanjay Jain, and Mohan Kankanhalli. 2025. Hallucination is inevitable:
       Accessed: 2024-11-07. (Apr. 2025).
                                                                                                 an innate limitation of large language models. (2025). https://arxiv.org/abs/240
[18]   Christopher Mims. 2025. Large language models get all the hype, but small
                                                                                                 1.11817 arXiv: 2401.11817 [cs.CL].
       models do the real work. The Wall Street Journal, (Oct. 2025). https://www.wsj
                                                                                          [37]   Yang Zhao et al. 2025. CodeV: Empowering LLMs with HDL Generation through
       .com/tech/ai/large-language-models-get-all-the-hype-but-small-models-do-
                                                                                                 Multi-Level Summarization. (2025). https://arxiv.org/abs/2407.10424 arXiv:
       the-real-work-225d3145.
                                                                                                 2407.10424 [cs.PL].
[19]   Kyungjun Min, Seonghyeon Park, Hyeonwoo Park, Jinoh Cho, and Seokhyeong
       Kang. 2025. Improving LLM-Based Verilog Code Generation with Data Aug-
       mentation and RL. In 2025 Design, Automation & Test in Europe Conference
       (DATE), 1–7. doi:10.23919/DATE64628.2025.10992897.
