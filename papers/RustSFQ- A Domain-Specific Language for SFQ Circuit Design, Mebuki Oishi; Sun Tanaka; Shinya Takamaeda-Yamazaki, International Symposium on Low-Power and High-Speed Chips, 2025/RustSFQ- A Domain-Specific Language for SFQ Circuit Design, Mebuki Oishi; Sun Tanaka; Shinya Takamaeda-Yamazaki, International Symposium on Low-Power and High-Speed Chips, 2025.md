                                                        RustSFQ: A Domain-Specific Language
                                                               for SFQ Circuit Design
                                                                          Mebuki Oishi, Sun Tanaka, Shinya Takamaeda-Yamazaki
                                                                                              The University of Tokyo
                                                                                       {mebuki, st, shinya}@is.s.u-tokyo.ac.jp


                                            Abstract—Cell-based design of a single-flux-quantum (SFQ)         quires careful consideration of how clock signals are supplied
                                         digital circuit requires input–output consistency; every output      to each logic gate [2], [3].
                                         signal must be consumed only once by the input of the following         For higher productivity in SFQ circuit development, cell-
                                         component, which is a unique constraint, unlike the traditional
arXiv:2502.11848v1 [cs.PL] 17 Feb 2025




                                         CMOS digital circuit design. While there are some cell libraries     based design [4] is preferred over full custom design using
                                         and simulation tools for SFQ circuit development, they do            primitive circuit elements like resistors and inductors, as is
                                         not verify the input–output consistency, and designers have          done in CMOS circuit development. However, due to the
                                         significant responsibilities to ensure it manually. Additionally,    pulse-driven nature, designers must ensure that the SFQ circuit
                                         designers have to carefully manage net names without unintended      satisfies input–output consistency.
                                         duplication and correct connectivity among nets in a netlist for
                                         simulations.                                                            There is an analog circuit simulator [5] tailored to SFQ
                                            We propose RustSFQ, a domain-specific language (DSL)              circuit evaluation, and such analog simulator requires a netlist
                                         embedded in Rust that automatically ensures the input–output         of an SFQ circuit described in the SPICE format as the input.
                                         consistency in the SFQ circuit by leveraging the ownership           However, directly describing a netlist is a significant burden
                                         system of Rust. Each SFQ circuit element is represented as a         for designers because a unique net name without unintended
                                         function while wires are represented as instances, and the Rust
                                                                                                              duplication should be assigned manually to each signal, and
                                         compiler verifies that multiple elements do not share a single
                                         wire through the ownership system. Circuit descriptions in the       careful connectivity management is required.
                                         RustSFQ are successfully compiled into low-level netlists for both      To address these problems in SFQ circuit design, we pro-
                                         analog and digital circuit simulations, and the DSL provides         pose a domain-specific language (DSL) enbedded in Rust.
                                         higher productivity than the conventional design flow.               Rather than other programming languages, we specifically
                                            Using the RustSFQ, we developed an SFQ-based Reed–                use Rust to leverage its ownership system to facilitate static
                                         Solomon encoder with a 4-bit width for the first time as a case
                                         study. We confirmed that the circuit operated correctly at 10 GHz    checking of input–output consistency. Since designing a high-
                                         through circuit simulations.                                         performance SFQ circuit requires fine-tuning of clock timings,
                                            Index Terms—single-flux-quantum (SFQ), superconducting in-        this DSL is designed to describe a circuit at the gate level,
                                         tegrated circuits, domain specific language, hardware description    close to the netlist. Moreover, the DSL contributes to efficient
                                         language, Reed-Solomon codes                                         circuit design because it can generate netlists for both digital
                                                                                                              and analog simulations with proper net names automatically
                                                               I. I NTRODUCTION                               assigned.
                                                                                                                 As a case study using the RustSFQ, we developed a Reed–
                                            Single-flux-quantum (SFQ) circuits are superconducting            Solomon encoder. Reed–Solomon codes are a type of error
                                         circuits operating at cryogenic temperatures. Due to their           correction code and have been applied in various fields such
                                         extremely high-speed operation and low power consumption,            as QR codes and wireless communications, taking advantage
                                         they attract significant interest as next-generation computing       of their high error correction capability [6], [7].
                                         devices [1].
                                                                                                                                      II. RUST SFQ
                                            SFQ circuits are driven by voltage pulses unlike CMOS
                                         circuits, which are driven by voltage levels. Each pulse             A. Implementation and Basic Design
                                         corresponds to a single magnetic flux quantum, implying it              RustSFQ is provided as a Rust crate, enabling circuit
                                         does not spontaneously split or disappear. Thus, SFQ digital         descriptions to be written as fully valid Rust code. The primary
                                         circuits must satisfy input–output consistency, a one-to-one         data types are Wire and Circuit. Methods on Circuit
                                         correspondence between inputs and outputs. In other words,           instantiate logic gates, and Wire is used to connect gates.
                                         every output signal must be consumed only once by the input          Each Wire can only be used only once by leveraging Rust’s
                                         of the following component, which is a unique constraint,            ownership system.
                                         unlike the traditional CMOS digital circuit design.                     The Wire struct internally holds only a single String.
                                            Another characteristic of SFQ circuits is that logic gates,       By wrapping it in a struct, constructor calls and cloning are
                                         such as AND or NOT, are clock-synchronous, as well as flip-          restricted. The Circuit struct has a list of gate instances;
                                         flops. Consequently, while SFQ circuits can achieve extremely        when a gate function is invoked, a new gate instance is added
                                         high clock frequency through deep gate-level pipelining, it re-      to this list (Listing 1).
           Listing 1: SFQ component abstraction                   in this manner. These include circuits with feedback loops and
pub struct Wire {name: String}                                    circuits employing counter-flow clocking, in which the clock
enum Gates {                                                      signal travels in the opposite direction of the data flow.
  And {name: String, a: String, b: String, clk:
      String, q: String},                                            To describe a circuit with loops, Wires at the upper end
  Split {name: String, a: String, q0: String, q1:                 of the loop are created along with the Circuit. The Wires
      String},                                                    at the lower end are identified as the upper end using the
  ...
}                                                                 set_loops() function.
impl<const N: usize, ... > Circuit<N, M, L, O, P> {                  The CounterWire type is introduced to describe counter-
  pub fn and(&mut self, a: Wire, b: Wire, clk: Wire,              flow clocking circuits. The DSL provides only BUFF and
       q: Option<&str>) -> Wire {
    let gate = Gates::And { ... };
                                                                  SPLIT gate functions for CounterWire, which are used
    self.gates.push(gate);                                        in clock lines. In contrast to standard gate functions, these
    return Wire::new( ... );                                      functions receive the output CounterWire and return the
  }
  ...
                                                                  input CounterWire. Listing 3 and Fig. 2 illustrate these
}                                                                 descriptions and show the resulting circuit structures.
                                                                       Listing 3: DSL description for the circuit in Fig. 2
     Listing 2: DSL description for the circuit in Fig. 1         let (mut c, [din], [loop0], [clkout]) = Circuit::
let inputs = ["a", "b", "clk"];                                       create(
let outputs = ["c", "s"];                                             ["din"], ["dout"], ["loop0"], ["clkout"],
let (mut circuit, [a, b, clk], [], []) =                              ["clkin"], "Advanced");
    Circuit::create(inputs, outputs, [], [], [],
    "HalfAdder");                                                 let (clk, clk0) = c.counter_split(clkout,None,None);
let [clk1, clk2] = circuit.split(clk, None, None);                let d = c.or(din, loop0, clk0, None);
let [a1, a2] = circuit.split(a, None, None);                      let (clk, clk0) = c.counter_split(clk, None, None);
let [b1, b2] = circuit.split(b, None, None);                      let d = c.dff(d, clk0, None);
let c = circuit.and(a1, b1, clk1, Some("c"));                     let (clkin, clk0) = c.counter_split(clk,
let s = circuit.xor(a2, b2, clk2, Some("s"));                         Some("clkin"), None);
circuit.set_outputs([c, s]);                                      let d = c.dff(d, clk0, None);
println!("{}", circuit.to_spice().join("\n"));                    let [dout, loop0] = c.split(d, Some("dout"),
                                                                      Some("loop0"));
                                                                  c.set_outputs([dout]);
   As a primary example, an SFQ-based half-adder circuit          c.set_loops([loop0]);
and its DSL description are shown in Fig. 1 and Listing 2,        c.set_counter_inputs([clkin]);
respectively.
                                                                     The DSL enables circuits to be parametrized, which is
   A Circuit instance, which corresponds a subcircuit in
                                                                  difficult in netlists. For example, a delay circuit comprising
SPICE and a module in Verilog, is created by invoking the
                                                                  a specified number of BUFF gates is described in Listing 4.
Circuit::create() function with its input and output
                                                                  Here, Rust’s ownership system is sufficiently strong to know
ports specified. At the time, Wire instances for the inputs (a,
                                                                  that the Wire instance in variable a is consumed and created
b, and clk in Listing 2) are also created.
                                                                  in every iteration; thus, the input–output consistency is still
   Logic gates are instantiated by invoking dedicated functions
                                                                  ensured.
on the Circuit. Each function takes the Wires for the gate’s
                                                                     A Circuit can be reused multiple times in another
inputs and takes ownership of them. Consequently, the Wire
                                                                  Circuit using the subcircuit() function. The function
cannot be used again. The gate function then returns a newly
                                                                  takes the reused Circuit and Wires for inputs, then returns
generated Wire for its output, which is used as an input for
                                                                  Wires for outputs. The number of inputs and outputs is
the subsequent gate.
                                                                  statically checked with the circuit type, which includes the
   A Wire can only be obtained from the circuit’s input port
                                                                  port counts.
or the gates’ output, and can only be used exactly once.
This mechanism ensures the input–output consistency required      C. Static Checking of Defective Circuits
in SFQ circuits. The Wires corresponding to the circuit’s            The pulse-driven nature of SFQ circuits requires that a pulse
output port are passed to the set_output() function, which        generated by one gate be received by exactly one gate. Circuits
consumes their ownership.                                         violating this restriction, such as those with more than one
   The Circuit has two functions to_spice() and                   receiver or no receiver, are defective as SFQ circuits. RustDSL
to_verilog(), which generate netlists in SPICE or Verilog         enables static detection of these problems, leveraging Rust’s
format as strings. Conversion of the DSL code into netlists is    ownership system and static code analyses.
completed by compiling and executing the code as a Rust              First, the circuit description in Listing 5 is defective because
code.                                                             wire a is received by multiple gates, AND and XOR. When
                                                                  you try to compile this code, the Rust compiler gives an error
B. Advanced Design                                                about ownership. The variable a loses ownership at the first
  In the RustSFQ, circuits are described from upstream to         function call of AND, and its second use in the XOR function
downstream, but certain types of circuits cannot be described     is prohibited.
    Fig. 1: Half adder circuit       Fig. 2: Counter-flow clocking circuit with a loop         Fig. 3: Parametrized delay circuit


                                                                    D. Automation of Net Name Assignment
 Listing 4: DSL description for the circuit in Fig. 3 (n = 5)
fn delay_circuit(n: u32) -> Circuit<1, 1, 0, 0, 0> {                   When writing a netlist, the assignment of net names and
  let name = format!("delay{}", n);                                 their error-free writing constitute a significant burden for
  let (mut c, [mut a], [], []) =                                    circuit designers. Although it is easy to number each net
  Circuit::create(["a"], ["q"], [], [], [], &name);
  for i in 0..n {                                                   in order, it increases the cost of circuit modification and
    let name = if i == n - 1 { Some("q") } else {                   debugging. On the other hand, naming everything with a
        None };                                                     meaningful name helps debugging but increases the cost of
    a = c.buff(a, name);
  }                                                                 naming. RustDSL provides a solution to this problem: when
  c.set_outputs([a]);                                               creating a Wire, i.e., when creating a Circuit or placing a
  return c;                                                         gate, the wire can be optionally named.
}
fn main() {                                                            Signals for I/O or those important for debugging can be
  let delay5 = delay_circuit(5);                                    explicitly named. If the net name is omitted, the name is au-
  let (mut c, [d, clk], [], []) = Circuit::create(                  tomatically assigned at compile time. Since the automatically
    ["din", "clk"], ["dout"], [], [], [], "main");
  let ([clk], []) = c.subcircuit(&delay5, [clk],                    generated names start with an underscore and are numbered
      [],[None],[]);                                                consecutively, there is no conflict unless the user dares to break
  let [clk, clk1] = c.split(clk, None, None);                       the naming rule. Listing 7 shows the netlist output from the
  let d = c.dff(d, clk1, None);
  let ([clk], []) = c.subcircuit(&delay5, [clk],                    description of listing 2.
      [],[None],[]);
  let d = c.dff(d, clk, Some("dout"));                                Listing 7: Netlist in SPICE format output from Listing 2
  c.set_outputs([d]);
                                                                    .subckt HalfAdder a b clk c s
  println!("{}", delay5.to_spice().join("\n"));
                                                                    XSPLIT1 clk _clk_0 _clk_1 THmitll_SPLIT
  println!("{}", c.to_spice().join("\n"));
                                                                    XSPLIT2 a _a_0 _a_1 THmitll_SPLIT
}
                                                                    XSPLIT3 b _b_0 _b_1 THmitll_SPLIT
                                                                    XAND4 _a_0 _b_0 _clk_0 c THmitll_AND2
                                                                    XXOR5 _a_1 _b_1 _clk_1 s THmitll_XOR
                                                                    .ends

   Second, the circuit description in Listing 6 is also defective
because no gates receive the wire a3 after it is split. When         III. A C ASE S TUDY ON SFQ R EED –S OLOMON E NCODER
you try to compile this code, the Rust compiler warns about            We demonstrated the practicality of the RustSFQ by devel-
an unused variable.                                                 oping a Reed–Solomon (RS) encoder circuit. It encoded an
   On the contrary, a description without errors or warnings        RS(12, 8) with a 4-bit width. The process was pipelined in
will guarantee that the circuit is valid as an SFQ circuit that     four stages. It had four input buffers with eight depths, and
satisfies input–output consistency.                                 its pipeline was filled by sequentially placing data from the
                                                                    buffers at every clock. It operated at a frequency of 10 GHz,
   Listing 5: Defective description with multiple receivers         as verified by digital and analog simulations.
...
let c = circuit.and(a, b1, clk1, Some("c"));                        A. Reed–Solomon Code
let s = circuit.xor(a, b2, clk2, Some("s"));                           RS codes are error-correcting codes that are widely used
circuit.set_outputs([c, s]);
                                                                    in various applications, such as QR codes and wireless com-
                                                                    munications [6], [7]. Since SFQ circuits use magnetic flux to
                                                                    perform calculations, it has been reported that electromagnetic
      Listing 6: Defective description with no receiver             noise can cause errors in operation [8]. RS codes and other
...                                                                 error-correcting codes may be utilized to improve the noise
let [a1, a2] = circuit.split(a, None, None);
let [a2, a3] = circuit.split(a2, None, None);
                                                                    tolerance of communication and memory in SFQ circuits.
let c = circuit.and(a1, b1, clk1, Some("c"));                          RS codes vary depending on the bit width, message length,
let s = circuit.xor(a2, b2, clk2, Some("s"));                       and error correction code length. An RS code is notated as
circuit.set_outputs([c, s]);
                                                                    RS(n, k) if a message of k words is encoded into n words,
                                                                    with n − k additional error-correcting words. Let n − k = 2t,
                                                                                Power              Polynomial         Binary
where t represents the error correction capability. This implies             Representation       Representation   Representation
that errors affecting up to t words can be corrected.                              0          0                        0000
   Let a be the bit width. Each word in an a-bit RS code is an                     1          1                        1000
element of the Galois field GF(2a ). The field GF(2a ) is a set                    α                α                  0100
                                                                                  α2                     α2            0010
consisting of 2a elements, each of which can be represented in                    α3                       α3          0001
multiple forms: power, polynomial, and binary. For example,                       α4          1+α                      1100
in GF(24 ) with generator polynomial p(x) = 1 + x + x4 , the                      α5              α + α2               0110
                                                                                  α6                  α2 + α3          0011
elements can be expressed as listed in Table I. Here, α satisfies                 α7          1+α        + α3          1101
p(α) = 0 and is referred to as the primitive element.                             α8          1     + α2               1010
   In the polynomial representation, the coefficients are ele-                    α9              α      + α3          0101
ments of GF(2), which is the set {0, 1}. The binary repre-                        α10         1 + α + α2               1110
                                                                                  α11             α + α2 + α3          0111
sentation corresponds to the sequence of these coefficients.                      α12         1 + α + α2 + α3          1111
Addition in GF(2a ) is performed as an XOR operation on the                       α13         1     + α2 + α3          1011
binary representations, whereas multiplication is performed as                    α14         1          + α3          1001
the product of the power representations. For multiplication,       TABLE I: Representations of elements in GF(24 ) (adapted
the exponents are considered modulo 2a − 1.                         from [9])
   In    the        RS(n, k)   code,  a    k-word       message
(m0 , m1 , . . . , mk−1 ), where mi ∈ GF(2a ) for all i,
can be represented as a (k − 1)th-degree polynomial:
    m(x) = m0 + m1 x + · · · + mk−1 xk−1 ∈ GF(2a )[x].
  Here, a generator polynomial g(x) ∈ GF(2a )[x] of degree
n − k is used, and the parity polynomial p(x) ∈ GF(2a )[x]
of degree n − k − 1 is computed as the remainder when
m(x) · xn−k is divided by g(x).
  Let p(x) be expressed as
          p(x) = p0 + p1 x + · · · + pn−k−1 xn−k−1 ,
where (p0 , p1 , . . . , pn−k−1 ) represents the error-correcting
code. The codeword is then formed by concatenating the                    Fig. 4: A CMOS implementation of RS encoder
message and the error-correcting code.
   For example, consider a 4-bit RS(12, 8) code with a gener-
ator polynomial                                                     words. At this point, the gate is shut down, which means that
                                                                    zeros are input into the multipliers. The results can then be
          g(x) = α10 + α3 x + α6 x2 + α13 x3 + x4 .                 obtained in the subsequent n − k cycles.
Suppose the message is (0010, 0101, 0011, 0101, 0110, 0100,
0001, 0101). This corresponds to the following polynomial:          C. Designed SFQ Implementation of RS Encoder
                                                                       Owing to the differences in the behavior of logic gates,
m(x) = α2 +α9 x+α6 x2 +α9 x3 +α5 x4 +α1 x5 +α3 x6 +α9 x7 .
                                                                    circuits designed for CMOS circuits cannot be directly applied
The remainder of dividing m(x) · x4 by g(x) is                      to SFQ circuits. we developed an RS encoder that operates
                                                                    efficiently in SFQ circuits based on the circuit shown in Fig. 4.
               p(x) = 0 + α2 x + αx2 + α11 x3 .                        Fig. 5 shows the designed RS encoder for RS(12,8) with a
Thus, the error-correcting code is calculated as                    4-bit width, which, to the best of our knowledge, is the first
(0000, 0010, 0100, 0111).                                           implementation of an RS encoder in SFQ circuits.
   The error detection and correction processes of the RS codes        1) Constant Multipliers: The RS encoder utilizes Galois
are omitted in this paper.                                          field multipliers, but only specific constant multiplications are
                                                                    necessary, rather than general multiplication. The RS(12, 8)
B. Existing CMOS Implementation of RS Encoder                       encoder requires multiplications by four constants: α3 , α6 ,
   A typical hardware RS encoder [9] can be implemented             α10 , and α13 . Each of these constant multipliers was designed
as shown in Fig. 4. The registers are initialized to zero. The      as a separate circuit.
message is entered sequentially from the highest to lowest             Fig. 5. (c), (d), and (e) show the constant multipliers that
coefficient. Multipliers and adders are combinational circuits      consist of XOR gates and DFFs for timing adjustment. These
that perform computations in the Galois field. The control gate     circuits were manually optimized to reduce the number of
manages the feedback signals and initially allows them to pass.     logic-gate stages. Although the α3 multiplier can complete its
After k words are input, the registers contain error-correcting     computation in a single stage, an additional DFF stage is added
Fig. 5: (a) Overall designed SFQ Reed–Solomon encoder, (b) Clockless gating circuit with an NDRO in Control Gate,
(c), (d), (e) Galois field constant multipliers


to match its stage count with that of the other multipliers. The    waiting, pipeline execution can be performed using four input
α6 multiplier comprises two α3 multipliers.                         sets. The implemented RS encoder has four 8-depth shift
   2) Pulse Gating: In CMOS circuits, the gating of a data          registers as input buffers, sequentially feeding the input value
signal with a control signal can be easily realized using only      into the calculation circuit to maximize circuit utilization.
an AND gate. However, in SFQ circuits, an AND gate requires            4) Clocking: In SFQ circuits that include feedback loops,
a clock, which is unfavorable in some cases.                        it is known that higher operating frequency can be achieved
   A clockless gating circuit is realized using a non-destructive   by using counter-flow clocking, in which the clock delay can
readout (NDRO) gate. The internal states of an NDRO gate            hide the data delay in the loop section [2]. Therefore, we
are similar to those of an RS flip-flop. Its state is updated       employed counter-flow clocking in the RS encoder. The clock
whenever a set or reset input occurs. When a clock is given,        takes 500 ps from the farthest downstream to the farthest
it outputs a pulse if its internal state is “1”. An NDRO gate       upstream, but the encoder operates with a clock period of
differs from other SFQ gates in that its internal state is not      100 ps. Appropriate delays must be inserted into the feedback
changed by clocks.                                                  section to ensure the correct operation. These delays must not
   To use an NDRO gate as a gating circuit, the controlled          be too small or too large because the data and clocks must
data line is connected to its clock input (Fig. 5. (b)). When       arrive in the correct order.
the gate’s internal state is “1”, it outputs a pulse every time a
data pulse comes, which looks like the gate passes the input               IV. S IMULATION R ESULTS AND E VALUATION
pulses. When its internal state is “0”, it outputs no pulse even
when a data pulse comes.                                               The designed RS encoder circuit’s operation was verified
   3) Pipelining: After inputting a word into the encoder, the      through digital simulation using Icarus Verilog and analog
output value of the adder next to the α13 multiplier is added       simulation using JoSIM. The input consisted of the following
to the following input value to be feedbacked. Because two          four messages:
adders requires one cycle each, the constant multiplier requires      1) (0100, 1110, 0111, 1111, 0100, 0010, 0001, 1100)
two cycles, and the control gate requires no cycle, a set of data     2) (0001, 0010, 0011, 0100, 0101, 0110, 0111, 1000)
must be input every four cycles.                                      3) (1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000)
   However, because independent data can be input without             4) (0010, 0101, 0011, 0101, 0110, 0100, 0001, 0101)
   The expected error-correcting codes for these messages are                  identified during the compilation stage. Moreover, in most
as follows:                                                                    cases, these errors can be identified in real time without
   1) (1000, 0011, 0011, 1101)                                                 compilation thanks to the Rust language server integrated into
   2) (1010, 1010, 0001, 0001)                                                 the editors.
   3) (0101, 0001, 0110, 0010)                                                                           Code       File Size (bytes)
   4) (0000, 0010, 0100, 0111)                                                                         RustSFQ           24,885
   Fig. 6 shows some of the results of the analog simulation.                                           SPICE            29,837
                                                                                                        Verilog          49,256
This illustrates that the four sets of results were correctly
output in sequence from the highest-order value. Excluding                       TABLE II: File sizes of codes to describe the RS encoder
the time required to store data into the input buffer, the
computation takes 48 cycles. Since the clock period was 100
                                                                                                    Name Assignment           Count
ps, the calculation completed in 4.8 ns.                                                                Manual             218 (27.4 %)
   The digital simulation also confirmed that the circuit oper-                                        Automatic           578 (72.6 %)
ated correctly.
                                                                                   TABLE III: Net name assignments of the RS encoder


                                                                                                           V. C ONCLUSION
                                                                                  RustSFQ, a DSL for SFQ circuit design that is embedded
                                                                               in Rust, was proposed. It enables a higher level of abstraction
                                                                               while maintaining fine-grained descriptions as conventional
                                                                               netlists. It can fill the lack of tools for efficient SFQ circuit
                                                                               design. The key feature of RustSFQ is that it ensures the input–
                                                                               output consistency by leveraging Rust’s ownership system.
                                                                               Other features, such as automatic assignment of net names
                                                                               and compatibility for both analog and digital simulations,
                                                                               contribute to effective SFQ circuit design.
                                                                                                       ACKNOWLEDGEMENTS
                                                                                 This work is supported in part by JSPS KAKENHI Grant
                                                                               Number 23H00467.
                                                                                                              R EFERENCES
                                                                               [1] K. K. Likharev and V. K. Semenov, “RSFQ logic/memory family: A new
                                                                                   Josephson-junction technology for sub-terahertz-clock-frequency digital
                                                                                   systems,” IEEE Transactions on Applied Superconductivity, vol. 1, no. 1,
                                                                                   pp. 3–28, 1991.
                                                                               [2] K. Ishida, I. Byun, I. Nagaoka, K. Fukumitsu, M. Tanaka, S. Kawakami,
   Fig. 6: Result of analog simulation of the RS encoder.                          T. Tanimoto, T. Ono, J. Kim, and K. Inoue, “SuperNPU: An extremely
The four colors correspond to each set of outputs. The results are output in       fast neural processing unit using superconducting logic devices,” in 2020
                 order from the highest-order coefficient.                         53rd Annual IEEE/ACM International Symposium on Microarchitecture
                                                                                   (MICRO). IEEE, 2020, pp. 58–72.
   The circuit of the RS encoder was described using the                       [3] K. TAKAGI, N. KITO, and N. TAKAGI, “Circuit Description and Design
                                                                                   Flow of Superconducting SFQ Logic Circuits,” IEICE Transactions on
RustSFQ. The DSL code consisted of two files with a total file                     Electronics, vol. E97.C, no. 3, pp. 149–156, 2014.
size of 24,885 bytes. After compiling the DSL code, the size                   [4] L. Schindler, J. A. Delport, and C. J. Fourie, “The ColdFlux RSFQ Cell
of the resulting SPICE file was 29,837 bytes and that of the                       Library for MIT-LL SFQ5ee Fabrication Process,” IEEE Transactions on
                                                                                   Applied Superconductivity, vol. 32, no. 2, pp. 1–7, 2022.
Verilog file was 49,256 bytes (TABLE II). Compared with the                    [5] J. A. Delport, K. Jackman, P. l. Roux, and C. J. Fourie,
combined size of the output files, the DSL source code size                        “JoSIM—Superconductor SPICE Simulator,” IEEE Transactions on Ap-
was less than one-third, indicating a reduction in the amount                      plied Superconductivity, vol. 29, no. 5, pp. 1–5, 2019.
                                                                               [6] T. V. Bui, N. K. Vu, T. T. Nguyen, I. Echizen, and T. D. Nguyen, “Robust
of code required for the description.                                              Message Hiding for QR Code,” in 2014 Tenth International Conference on
   Furthermore, one of the burdens of writing netlists, as-                        Intelligent Information Hiding and Multimedia Signal Processing, 2014,
signing net names, was notably eased. This circuit contained                       pp. 520–523.
796 net names, of which only 218 were specified explicitly                     [7] P. Dayal and R. Patial, “FPGA Implementation of Reed-Solomon Encoder
                                                                                   and Decoder for Wireless Network 802. 16,” International Journal of
(TABLE III). Over 70 % of the net names were automatically                         Computer Applications, vol. 68, pp. 42–45, 04 2013.
assigned during compilation, relieving designers of the need                   [8] Y. YAMANASHI, “Design and Implementation of a Pipelined Bit-
to assign them manually.                                                           Serial SFQ Microprocessor, CORE1β,” IEEE Trans. Appl. Supercond.,
                                                                                   vol. 17, pp. 474–477, 2007. [Online]. Available: https://cir.nii.ac.jp/crid/
   Another advantage of using the DSL is its ability to detect                     1571980075515449344
errors earlier. In addition to syntax and spelling mistakes, any               [9] J. Sylvester, “Reed Solomon Codes,” Elektrobit, January, 2001.
input–output inconsistencies specific to SFQ circuits can be
