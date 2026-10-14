                                        Solver-Aided Constant-Time Circuit Verification

                                        Rami Gökhan Kıcı1 , Klaus v. Gleissenthall2 , Deian Stefan1 , and Ranjit Jhala1
                                                                1
                                                                    University of California San Diego
                                                                    2
                                                                      Vrije Universiteit Amsterdam
arXiv:2104.00461v1 [cs.CR] 1 Apr 2021




                                        Abstract. We present Xenon, a solver-aided method for formally verifying that
                                        Verilog hardware executes in constant-time. Xenon scales to realistic hardware
                                        designs by drastically reducing the effort needed to localize the root cause of
                                        verification failures via a new notion of constant-time counterexamples, which
                                        Xenon uses to automatically synthesize a minimal set of secrecy assumptions.
                                        Xenon further exploits modularity in Verilog code via a notion of module
                                        summaries, thereby avoiding duplicate work across multiple module instantia-
                                        tions. We show how Xenon’s assumption synthesis and summaries enable the
                                        verification of a variety of circuits including AES, a highly modular AES-256
                                        implementation where modularity cuts verification from six hours to under three
                                        seconds, and ScarV, a timing channel hardened RISC-V micro-controller whose
                                        size exceeds previously verified designs by an order of magnitude.


                                        1   Introduction
                                        Timing side-channel attacks are no longer theoretical curiosities. Over the last
                                        two decades, they have been used to break implementations of cryptographic
                                        primitives ranging from public-key encryption algorithms [25, 53, 77], to block
                                        ciphers [22, 61], digital signature schemes [60], zero-knowledge proofs [33], and
                                        pseudorandom generators [32]. This, in turn, has allowed attackers to break
                                        systems that rely on these primitives for security—for example, to steal TLS keys
                                        used to encrypt web traffic [25,32,77], to snoop and forge virtual private network
                                        traffic [60], and to extract information from trusted execution environments [24,
                                        32, 33, 76].
                                            The gold standard for preventing timing side-channel attacks is to follow a
                                        discipline of constant-time or data-oblivious programming [1, 15, 21, 28, 34, 78].
                                        At its core, this discipline ensures that (1) secret data is not used as an operand
                                        to variable-time instructions (e.g., floating point operations like division [18, 19,
                                        54, 64]) and (2) the program’s control flow and memory access patterns do not
                                        depend on secrets.
                                            But for the constant-time discipline to be effective, it is crucial that the
                                        constant-time property be preserved by the underlying hardware. For example,
                                        an instruction that is deemed constant-time needs to indeed produce its outputs
                                        after the same number of clock cycles, irrespective of operands or internal state.
                                        Similarly, given that control-flow and memory access patterns are public, i.e.,
                                        free of secrets, a CPU’s timing must indeed be secret-independent.
                                            Unfortunately, simply assuming that hardware preserves constant-time doesn’t
                                        work. Incorrect assumptions about the timing-variability of floating-point in-
2                         Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

structions, for example, allowed attackers to break the differentially private Fuzz
database [49]. Attempts to address these attacks (e.g., [65]) were also foiled:
they relied on yet other incorrect microarchitectural assumptions (e.g., about
the timing-variability of SIMD instructions) [54]. Yet more recently, hardware
crypto co-processors (e.g., Intel and STMicroelectronics’s trusted platform mod-
ules) turned out to exhibit similar secret-dependent timing variability [60].
    A promising path towards eliminating such attacks is to formally verify that
our hardware preserves the constant-time property of the software it is exe-
cuting. Such verification efforts, however, require tool support. Unfortunately,
unlike software verification of constant-time, which has had a long history [20],
constant-time hardware verification is still in its infancy [27, 46, 78]. As a result,
existing verification approaches like Iodine [46] fail to scale to realistic hard-
ware. This has two fundamental reasons. First, existing tools do not help when
verification fails, as is inevitable, since hardware circuits only preserve constant-
time execution under very specific secrecy assumptions that describe which port
and wire values are public or secret. Currently, upon failure, the user must un-
dertake the tedious and time consuming task of determining, whether the circuit
is indeed leaky (i.e., variable-time), or whether it is missing additional secrecy
assumptions, which the user then has to explicate. In our experience, this process
takes up the overwhelming majority of time spent on the verification effort. Sec-
ond, current methods fail to exploit the modularity that is already explicit at the
register transfer level. Hence, they duplicate verification effort across replicated
modules which leads to a blow up in verification time.
    In this paper, we present Xenon, a solver-aided method for formally verifying
that Verilog hardware executes in constant-time. We develop Xenon via four
contributions.
1. Counterexamples. To help users understand verification failures, we in-
troduce the notion of constant-time counterexamples (§ 4.1). A counterexample
highlights the earliest point in the circuit where timing variability is introduced;
this simplifies the task of understanding whether a circuit is variable-time by
narrowing the user’s attention to the root cause of the verification failure (and
a thereby small fraction of the circuit). To compute counterexamples, Xenon
leverages information extracted from the failed proof attempt. In particular, the
solver communicates (1) for which variables (i.e., registers and wires) it was
able to prove the constant-time property and (2) in which order the remaining
variables became non-constant time. This allows Xenon to break cyclic data-
dependencies which cause a chicken-and-egg problem that is hard to resolve when
assigning blame manually.
2. Assumption Synthesis. To help the user resolve the verification failure,
Xenon uses the counterexample to synthesize a suggested fix. For example,
Xenon may find a constant-time counterexample for a processor pipeline where
the two different runs may execute two different ISA instructions (say, addition
and division) which take different numbers of clock cycles. Yet, the execution of
each instruction (for any inputs) may be constant-time. Xenon uses the coun-
terexample to synthesize a minimal candidate set of secrecy assumptions (e.g.,
                            Solver-Aided Constant-Time Circuit Verification      3

that any two executions have the same, publicly visible sequence of instructions)
which address the root cause of the verification failure (§ 4.2). The user then
decides either to accept the candidate assumption, or, if they do not match their
intuition for the intended usage of the circuit, reject them, in which case Xenon
computes an alternative. Internally, Xenon computes candidate assumptions,
via a reduction to integer linear programming [63].
3. Modular Verification. Finally, in order to scale both verification and coun-
terexample generation to larger and more complex hardware, we introduce a
notion of module summaries (§ 3). Module summaries succinctly capture the
timing properties of a module’s input and output ports at a given usage site. By
abstracting inessential details about the exact computations performed by the
module and focusing solely on its timing behavior, Xenon produces fewer and
more compact constraints.
4. Evaluation. We implement Xenon and evaluate the impact of counterexam-
ples, assumption synthesis and modularity on the verification of different kinds
of hardware modules (§ 6). We find that Xenon’s counterexample synthesis dra-
matically reduces the number of potential error locations a user has to inspect
in order to understand the root-cause of the violation (to 6% of its original size)
and that Xenon is highly effective at suggesting useful assumptions—on average
81.67% are accepted by the user. Similarly, our evaluation shows that module
summaries are key to reducing verification times for certain hardware designs
(e.g., for AES-256 crypto core summaries reduced the verification time from six
hours to a three seconds). Overall, we find that Xenon’s solver-aided verifica-
tion process drastically reduces verification effort (e.g., manually verifying the
largest benchmark of [46] took us several minutes instead of days) and is key
to scaling verification to realistic hardware: the SCARV side-channel hardened
RISC-V core [4] we verify is an order of magnitude larger than the RISC-V cores
verified by previous state-of-the-art tools.


2     Overview

We start by reviewing how to specify and verify the absence of timing channels
in Verilog hardware designs (§ 2.1), show how existing techniques fail to scale on
real-world hardware designs, as these designs are often only constant-time under
additional secrecy assumptions which are tedious to derive by hand (§ 2.2),
sketch how Xenon helps finding secrecy assumptions automatically (§ 2.3), and
finally discuss how Xenon exploits modularity (§ 2.4).


2.1   Verifying Constant-Time Execution of Hardware

Lookup Circuit. Figure 1 shows the code for a Verilog module, which imple-
ments a lookup table by case-splitting over the 8-bit input value. This module
executes in constant-time: even if input in contains a secret value, producing
output out takes the same amount of time (one clock cycle), irrespective of the
4                             Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

                                  in      out    in• out•
                         time
                                 L R L R L R L R
                          1     h00 hff X X ⋆ ⋆ • •
                          2     h00 hff h63 h2c • • ⋆ ⋆

Fig. 2: Two runs of Figure 1 showing values and liveness-bits input (in) and output
(out). X represents an undefined value.



value of in, and therefore, an attacker cannot make any inference about the
value of in by observing the timing of the computation.
Specifying Constant-Time Execution. Figure 2 makes this intuition more
precise, using a recent definition of constant-time execution for hardware [46].
Instead of tracking timing
indirectly through informa-
tion flow [57,71,80] the def-          1  module S ( clk , in , out );
inition uses a direct no-              2      input clk ; [ 7 : 0] in ;
tion of timing.3 The Fig-              3      output reg [ 7 : 0] out ;
ure shows two runs of mod-             4      always @ ( posedge clk )
ule S: one for input 8'h00             5        case ( in )
                                       6            8’ h00 : out <= 8’ h63 ;
and one for input 8'hff.               7            ...
We want to track how long              8            8’ hff : out <= 8’ h2c ;
it takes for the two in-               9        endcase
puts, issued at cycle 1 to            10  endmodule
pass through the circuit
and produce their respec- Fig. 1: A simple, constant-time lookup-table in Ver-
                               ilog, taken from [10].
tive outputs. For this, we put a “tracer” on the inputs by assigning a liveness-bit
to each register. For some register x, we set its liveness-bit x• to ⋆, if x has been
influenced by the input at initial cycle 1 (we say x is 1-live) and •, otherwise.
Figure 2 shows how liveness-bits are propagated through the circuit. Initially, in
both executions, the input is 1-live and the output is not. In cycle 2, both outputs
1-live due to the case-split on the value of in. Assuming that an attacker can
observe the liveness-bits of all outputs, here, register out, the attacker cannot
distinguish the two executions, and we can conclude that the pair of executions
is indeed constant-time.
Verifying Constant-Time Execution. In order to show constant-time exe-
cution, not only for the two runs in Figure 2, but for the whole circuit, Xenon
proves that for any pair of runs, that is, for any pair of inputs, and any initial
cycle, the constant-time property holds. Xenon’s solver achieves this by con-
structing a product circuit [46] whose runs correspond to pairs of runs—called
left and right —of the original circuit. In this product, each original variable x
has two copies xL and xR that hold the values of x in the left and right runs, re-
3
    This definition has the advantage of being more precise. In fact, indirect techniques
    would not be able to prove constant-time execution of this simple example, since
    there is an information flow from the potentially sensitive input to the output.
                                  Solver-Aided Constant-Time Circuit Verification      5

     spectively. Following [46], Xenon’s solver uses the product circuit to synthesize
     invariant properties of the circuit. For example, let’s define that a variable x is
     constant time (and write ct(x)), if for any pair of executions, its liveness-bit in
     the left execution x•L is always the same as its liveness-bit in the right execution
     x•L , i.e., x•L = x•R always holds, for all initial cycles t. Xenon synthesizes the
     following invariant on the module which proves constant-time execution, under
     the condition that module inputs are constant-time: ct(in) ⇒ ct(out).


     2.2   Real World Hardware is Not Constant-Time

                                                 Unfortunately, unlike the simple lookup-
1    // source ( IF_pc ); sink ( WB_reg );       table from Figure 1, real world circuits
2    module mips_pipeline ( clk , rst );
                                                 are typically not constant-time, in an
3    input clk , rst ;                           absolute sense. Instead, when care-
4                                                fully designed, they are constant-time
5    assign IF_pc4 = IF_pc + 32 ’ d4 ;           under specific secrecy assumptions de-
6    assign IF_pcj = ID_Jmp                      tailing which circuit inputs are sup-
     ? ID_jaddr : IF_pc4 ;                       posed to be public (visible to the at-
7    assign IF_pcn = M_PCSrc ? M_btgt            tacker) or secret (unknown to the at-
     : IF_pcj ;                                  tacker). Thus, verification requires the
8

9    assign ID_rs = ID_instr [ 25 : 21 ] ;       user to painstakingly discover secrecy
10   assign ID_rt = ID_instr [ 20 : 16 ] ;       assumptions through manual code in-
11   rom32 IMEM ( IF_pc , IF_instr );            spection, which can be prohibitively
12
                                                 difficult in real world circuits.
13   always @ (*)
14     Stall = EX_MemRead &&                     A Pipelined MIPS Processor. We
15                ( EX_rt == ID_rs ||            illustrate the importance of these as-
16                  EX_rt == ID_rt );
17   always @ ( posedge clk )
                                                 sumptions using the program in Fig-
18     if ( rst )                                ure 3 which shows a a code-fragment
19       ID_instr      <= 0; ...                 taken from one of our benchmarks—
20     else                                      a pipelined MIPS processor [8]. If
21       if ( Stall == 1) begin
22          ID_instr <= ID_instr ;               the reset bit rst is set, the proces-
23          IF_pc      <= IF_pc ;                sor sets a number of registers to zero
24          EX_rt      <= EX_rt ;                (Line 18). Otherwise, the processor
            ...
25
                                                 checks whether the pipeline is stalled
26          WB_reg <= WB_reg ;
27       end else begin                          (Line 21) and either forwards the cur-
28          ID_instr <= IF_instr ;               rent instruction from the instruction-
29          IF_pc      <= IF_pcn ;               fetch stage to the instruction-decode
            EX_rt      <= ID_rt ;
30
                                                 stage (Line 28) and advances the pro-
31          ...
32          WB_reg <= WB_wd ;                    gram counter (Line 29), or stalls by re-
33       end                                     assigning the current values (Line 22).
34     end
                                                 The Pipeline is not Constant-
          Fig. 3: MIPS Pipeline Fragment.        Time. When using the processor in
                                                 a security critical context, we want to
                                                 make sure that it avoids leaking se-
     crets through timing, i.e., that it is constant-time. Unfortunately, our example
6                          Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

               stall      ID jmp    IF inst•    ID inst•     EX rt•     WB reg•
      time
              L    R      L    R     L    R      L    R      L    R     L    R
        1     0     1     1    0     ⋆   ⋆       •    •      •    •      •   •
        2     0     0     0    1     •   ⋆       ⋆    •      •    •      •   •
        3     0     0     0    0     ⋆    •      ⋆   ⋆       ⋆    •     ⋆    •

Fig. 4: Two runs of Figure 3, where the right run stalls in cycle 1. The liveness bits of
sink wb reg differ in cycle 3 and therefore the circuit is not constant-time.



pipeline is not constant-time without any further restrictions on its usage. For
example, the execution time for a given instruction depends on whether or not
the pipeline is stalled before the instruction is retired. This is illustrated in Fig-
ure 4. We model an attacker that can measure how long an instruction takes
to move through the pipeline, i.e., from source IF pc to sink WB reg (this is
specified through the annotation in Line 1 of Figure 3). Such an attacker can dis-
tinguish the two runs in Figure 4, as the liveness-bits of WB reg differ in cycle 3.
This timing difference lets the attacker make inferences about the control-flow
of the program which is executed on the processor, and therefore any attempt
to verify constant-time execution results in a failure.


2.3   Automatically Finding Secrecy Assumptions

We may, however, still be able to use this processor safely, if we can find a
suitable set of secrecy assumptions. For example, we could assume that register
Stall is public (i.e., free of secrets, which can be formally expressed by the as-
sumption that StallL = StallR always holds). In this case, the timing difference
in Figure 4 would only leak information that the attacker is already aware of.
However, Stall is defined deep inside the pipeline and therefore, it is hard to
translate this assumption into a restriction on the kind of software i.e., code we
are allowed to execute on the processor. Instead, we want to phrase our assump-
tions in terms of externally visible computation inputs. For example, restricting
program counter IF pc to be public directly translates into the obligation that
the executed program’s control-flow be independent of secrets.
    To achieve this using existing technology, the engineer first has to manu-
ally identify that the timing variability is first introduced in variable ID instr
(Line 28) due to a control dependency on Stall. They then need to inspect
how Stall is set (Line 13) and painstakingly trace the definitions which may
involve complex combinatorial logic (excerpt starting in line Line 5) and circular
data-flows in order to identify a promising candidate register, such that marking
the register as public will render the circuit constant-time. Counterexamples like
Figure 4 are often of little help as they are hard to interpret, and fail to focus
attention on the relevant parts of the circuit.
Solver Aided Verification:         Xenon
                                       ’s Interactive Loop. Xenon drastically
simplifies this time consuming process through a solver-aided workflow that helps
finding secrecy assumptions automatically.
                            Solver-Aided Constant-Time Circuit Verification      7

Step 1. First, we start with an empty set of secrecy assumptions and run Xenon
on the pipeline. The verification fails, as the pipeline is not constant-time, how-
ever, Xenon displays the following prompt to guide the user towards a solution.
> Mark 'reset' as PUBLIC? [Y/n]
The user either says Y indicating that reset should indeed be considered pub-
lic, or else responds N which tells Xenon to exclude the variable from future
consideration (i.e., not suggest it in future). Suppose that we follow Xenon’s
advice, and click Y: this marks reset public and re-starts Xenon for another
verification attempt.
Step 2. Next, Xenon suggests marking M PCSrc as public. M PCSrc acts as a
flag that indicates whether the current instruction in the memory stage contains
an indirect jump. But since M PCSrc’s value depends on register values (i.e.,
M PCSrc is set depending on whether the output of the execute phase is zero)
assuming that M PCSrc is public would lead to assumptions about the data-
memory which we wish to avoid. We therefore tell Xenon to exclude it in future
verification attempts and restart verification.
Step 3. Restarting verification causes Xenon to suggest candidate variables
IF pc and IF pcn, the program counter of the fetch stage and its value in
the next cycle, respectively. We mark IF pc as public as this directly encodes
the assumption that the program’s control flow does not depend on secrets. In
addition, Xenon infers a second set of usage assumptions which details the parts
of the pipeline that have to be flushed on context switches. These assumptions
would otherwise have to be supplied by the user as well. Finally, Xenon proves
that the resulting program executes in constant-time and therefore concludes
the verification process.
Counterexamples. While synthesizing candidate assumptions, Xenon inter-
nally computes a constant-time counterexample which consists of the set of vari-
ables that have lost the constant-time property earliest. While the user can
simply follow Xenon’s suggestions without further investigating the root cause
of the violation, we find that—if the user chooses to do so—the counterexample
often helps to further understand why the circuit has become non constant-time.
For example in our simple pipeline, Xenon returns a counterexample consisting
only of variable ID instr for all three interactions. Indeed, inspecting the parts
of the circuit where ID instr is assigned focuses our attention on the relevant
parts of the circuit, that is, the conditional assignment of ID instr under rst
(Line 18) and under Stall (Line 21). We discuss how Xenon computes coun-
terexamples using an artifact extracted from the failed proof attempt in § 4.1,
and how Xenon synthesizes secrecy assumptions via a reduction to integer linear
programming in § 4.2.

2.4   Real World Circuits Aren’t Not Small
While Xenon’s solver-aided verification loop significantly reduces the time the
user has to spend on verification efforts, large real world circuits often also
8                          Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

          1   module S4 ( clk , in , out );
          2      input clk ;
          3      input [ 31 : 0 ] in ;
          4      output [ 31 : 0] out ;
          5        wire [ 7 : 0 ]      out_0 ,    out_1 , out_2 , out_3 ;
          6      S S_0 ( clk , in [ 31 : 24 ] ,   out_3 ),
          7        S_1 ( clk , in [ 23 : 16 ] ,   out_2 ),
          8        S_2 ( clk , in [ 15 :8 ] ,     out_1 ),
          9        S_3 ( clk , in [ 7 : 0] ,      out_0 );
         10        assign out = { out_3 ,         out_2 , out_1 , out_0 };
         11   endmodule

                     Fig. 6: Module from the AES benchmark.

present a challenge for to solver. This is because computing invariants requires a
whole program analysis. Hence, the efficiency of our solver crucially depends of
the size of the circuit we are analyzing, and therefore verification might become
prohibitively slow on large designs.
    Consider, for example, the AES-256 benchmark from [10]. Fig. 5 depicts
the dependency graph of its modules, where each node m represents a Verilog
module, and we draw an edge between modules m and n, if m instantiates n.
Each edge is annotated with the number of instantiations. Even though there are
only ten modules, the total number of module instantiations is 789. This, in turn,
causes a blowup in the size of code Xenon has to verify. Even though the sum of
#LOC of the modules is only 856, inlining module instances causes this number
to skyrocket to 135194 rendering verification all but intractable. (In fact, Xenon
does manage to verify the naive, inlined circuit, however, verification takes over
6 hours to complete).
    Fortunately, we can avoid this
blowup by exploiting the modularity
that is already apparent at the Ver-                 exp  A
                                                7           1
ilog level. We illustrate this process           6   exp   1      4
                                                          B   S4      S
using module S from Figure 1.               aes
                                                   1     4

                                                       final
                                              13                         1
Module Summaries. Since the                            4           4       1
                                                  one       lookup     T       xS
value of out only depends on in, we
can characterize its timing behavior
as follows: the module output out is
                                         Fig. 5: Module dependency graph of the
constant-time, if module input in is AES-256 benchmark.
constant-time.
    We can formalize this in the fol-
lowing module summary, which we Xenon computes automatically: ct(in) ⇒
ct(out). Instead of inlining the module, we can now use its summary thereby
eschewing the code explosion and enabling efficient verification. The code in Fig-
ure 6 shows an instantiaton of module S in module S4. Instead of inlining S at
its four instantiaton sites S_0 to S_3, Xenon uses the single module summary
to compute a correctness proof, which only takes 3 seconds.
                               Solver-Aided Constant-Time Circuit Verification              9

3     Modular Constant-Time Verification

We now formalize the concepts introduced in the overview. We first review a
formal definition of constant-time execution for hardware circuits (§ 3.1) and its
translation to Horn-clause verification conditions (§ 3.2). We then show how to
modularize this naive encoding via summaries (§ 3.3).


3.1    Defining Constant-Time Execution

Configurations. Configurations represent the state of a Verilog computation.
A configuration Σ , (P, σ, θ, c, t, Src) is made up of a Verilog program P (say,
the processor in Figure 3), a store σ, a liveness map θ, current clock cycle c ∈ N,
initial clock cycle t ∈ N and, finally, a set of sources Src ⊆ Vars. Store σ ∈
Vars → Z maps variables Vars (registers and wires) to their current values;
map θ ∈ Vars → {⋆, •} maps variables to liveness-bits; cycle t marks the
starting-cycle of the computation we want to track and finally Src identifies the
inputs of the computation we are interested in.
Transition relation. Transition relation ∈ (Σ × Σ) encodes a standard Ver-
ilog semantics which defines how a configuration is updated from one clock-cycle
to the next. We omit its definition, as it is not needed for our purposes, but for-
mal accounts can be found in [46, 47, 80]. In addition to updating the store and
current cycle, the transition relation updates the liveness map θ by tracking
which variables are currently influenced by the computation started in t. At
initial cycle t, our transition relation starts a new computation by setting the
liveness-bits of all variables in Src to ⋆, and those of all others variables to •.
Runs. We call a sequence of configurations π , Σ0 Σ1 . . . Σn−1 a run, if each
consecutive pair of configurations is related by the transition relation, i.e., if
Σi       Σi+1 , for i ∈ {0, . . . , n − 2}. We call Σ0 , (P, σ0 , θ0 , 0, t, Src) initial
state, and require that θ0 maps all variables to •. Finally, for a run π ,
(P, σ0 , θ0 , c0 , t, Src) . . . (P, σn−1 , θn−1 , cn−1 , t, Src), we say that π is a run of P
of length n with respect to t and Src and let store(π, i) = σi and live(π, i) , θi ,
for i ∈ {0, . . . , n − 1}.
Example. Consider again Figure 2. The Figure depicts two runs πL and πR
of length 3 with respect to initial cycle 1 and source {in} of the program in
Figure 1. Columns in and out show store(π, i)(in) and store(π, i)(out), for π ∈
{πL , πR } and i ∈ {1, 2}. Similarly, columns in• and out• show live(π, i)(in) and
live(π, i)(out), for π ∈ {πL , πR }, and i ∈ {1, 2}. The Figure omits the initial state
at cycle 0, where all liveness-bits are set to •.
Flushed, Constant-Time, Public. For two runs πL and πR of length n, we
say that variable v is flushed, if store(πL , 0) = store(πR , 0), we call v public, if
store(πL , i) = store(πR , i), for i ∈ {0, . . . , n − 1} and finally, we call v constant-
time, if live(πL , i) = live(πR , i), for i ∈ {0, . . . , n − 1}.
Secrecy Assumptions. A set of secrecy assumptions A , (Flush, Pub) con-
sists of a set of variables Flush ⊆ Vars that are assumed to be flushed in
10                              Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

the initial state, and a set of variables Pub ⊆ Vars, that are assumed equal
throughout. A pair of runs πL and πR of length n, satisfy a set of assumptions
A, if, for each v ∈ Flush, v is flushed, and for each v in Pub, v is public. We
describe how Xenon synthesizes secrecy assumptions in § 4.
Constant-Time Execution. We now define constant-time execution with re-
spect to a set of sinks Snk ⊆ Vars, sources Src, and assumptions A. We say
that a program P is constant-time, if for any initial cycle t and any pair of runs
πL and πR of P with respect to t and Src of length n that satisfy A, and any
sink o ∈ Snk, o is constant-time.
Example. Consider again Figure 2. If we assume that variables in cycle 0 have
the same value as in cycle 1, then out is flushed while in is not. Neither in,
nor out are public, but both are constant-time. As out is constant-time in all
runs, the program in Figure 1 is constant-time with respect to the empty set
of assumptions and sink {out}. In Figure 4, none of the variables are public or
constant-time, however, the program in Figure 3 can be shown to be constant-
time with Pub = {IF pc, reset}.



  init(vsL , vsR ) ∧ flush ∧ pub → inv (vsL , vsR , 0, t)                                         (init)

  inv (vsL , vsR , c, t) ∧ next (vsL , vsR , vsL′ , vsR′ , t) ∧ pub → inv (vsL′ , vsR′ , c + 1, t) (cons)

  inv (vsL , vsR , c, t) ∧ pub → o•L = o•R , for o ∈ Snk                                            (ct)


Fig. 7: Horn clause encoding of the verification conditions for constant-time execution.



3.2    Verifying Constant-Time Execution via Horn Constraints
To verify constant-time execution of a circuit, we mirror the formal definition of
constant-time execution in a set of Horn clauses [23]. We start with the naive,
monolithic encoding and discuss how to make it modular in § 3.3. At high level,
the constraints i) issue a new live instruction at a non-deterministically cho-
sen initial cycle t, and ii) ensure constant-time execution by verifying that the
liveness-bits for each sink are always the same, in any two runs. The clauses—
shown in Figure 7—encode standard verification conditions over an invariant
inv (vsL , vsR , c, t) of the product circuit, where vs ranges over all variables in the
circuit and their respective liveness bits, and c and t are the current and initial
cycles, respectively. We now describe the verification conditions in more detail.
Initial States and Transition Relation. Formula init (vsL , vsR ) describes
the product circuit’s initial states and requires all liveness-bits to be set to •. To
ensure that the proof holds for any initial cycle, init does not constrain t. Formula
next encodes the transition relation of the product circuit. Like , next sets
liveness-bits of all sources to ⋆ at clock cycle t. Importantly, constructing next
                            Solver-Aided Constant-Time Circuit Verification      11

requires inlining all modules and therefore can lead to large constraints that are
beyond the abilities of the solver.
Assumptions. For a set of assumptions A , (Flush, Pub), we construct
formulas flush and pub, both of which require the variables in their respec-
tive sets to be equal in the two runs. We let flush , (∧x∈Flush xL = xR ) and
pub , (∧x∈Pub xL = xR ).
Horn Constraints & Solutions. We then require that the invariant holds,initially
(init ), assuming all variables in Flush and Pub are equal in both runs; that
the invariant is preserved under the transition relation of the product circuit,
assuming that public variables are equal in both runs (cons), and finally, that
the liveness-bits of any sink are the same in both runs (ct ). These constraints
are then passed to an off-the-shelf solver [9] yielding a formula which, when
substituted for inv , makes all implications valid and thus proves constant-time
execution.
Proof Artifacts. While attempting to construct the invariant, the solver’s in-
ternal representation keeps track of i) the set of variables which it was able to
prove to be constant-time and public and ii) the order in which the remain-
ing variables lost the respective properties. In case of a failed proof attempt, the
prover communicates these artifacts to the assumption synthesis part of Xenon,
which in turn uses them to identify the verification failure, as we will discuss in
the next section.


3.3   Finding Modular Invariants

Naively, constructing next requires all the code to be in a single module. How-
ever, this can yield gigantic circuits whose Horn clauses are too large to analyze
efficiently. To avoid instantiating the entire module at each usage site, Xenon
constructs module summaries which concisely describe the timing relevant prop-
erties of the module’s input and output ports.
Per-Module Invariants and Summaries. Instead of a single whole program
invariant inv , the modular analysis constructs a per-module invariant inv m , and
an additional summary sum m , for each module m. The summary only ranges
over module inputs and outputs, and respective liveness-bits (io) and needs to be
implied by the invariant, i.e., we add a clause stating that inv m (vsL , vsR , t) ⇒
sum m (ioL , ioR , t). The analysis produces the same constraints as before, but
now on a per-module basis, that is, we require module invariants to hold on
initial states (init ), and be preserved under the transition relation (cons), but,
instead of using the overall transition relation next we use a per-module transi-
tion relation next m . It may now happen that next m makes use of a module n,
but instead of inlining the transition relation of n as before, we substitute it
by its module summary sum n , thereby avoiding the blowup in constraint size.
Finally, we restrict sources and sinks to occur at the top-level module, and add
a clause requiring that any sink has the same liveness-bits in both runs (ct ). The
summaries are also used to modularize our assumption synthesis algorithm § 4.3.
12                             Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

4      Counterexamples & Assumption Synthesis
We now explain how Xenon uses the proof artifacts to help the user understand
and explicate secrecy assumptions when verification fails. We first describe how
Xenon analyzes the artifacts from the failed proof attempt in order to compute a
counterexample consisting of the set of variables that—according to the informa-
tion communicated by the prover—lost the constant-time property first (§ 4.1).
Next, we discuss how Xenon uses the counterexample to synthesize a set of se-
crecy assumptions that eliminate the root cause of the verification failure (§ 4.2).
This is done by computing a blame-set which contains the set of variables that
likely caused the loss of constant-time for the variables in the counterexample
via a control dependency. This blame set is then used to encode an optimization
problem whose solution determines a minimal set of assumptions required to
remove the timing violation. Finally, we briefly discuss how Xenon uses mod-
ule summaries to speed up counterexample generation and secrecy assumption
synthesis (§ 4.3).

4.1      Computing Counterexamples

Dependency Graph. To compute the counterexample from a failed proof at-
tempt, Xenon first creates a dependency graph G , (V, D ∪ C) which encodes
data-, and control dependencies between program variables. G consists of vari-
ables V ⊆ Vars, data-dependencies D ⊆ (Vars × Vars), where (v, w) ∈ D
if v’s value is used to compute w directly through an assignment, and control-
dependencies C ⊆ (Vars×Vars) where (v, w) ∈ C, if v’s value is used indirectly,
i.e., w’s value is computed under a branch whose condition depends on v.
Variable-Time Map. Next, Xenon extracts an artifact from the failed proof
attempt: a partial map varTime ∈ (Vars ⇀ N) which records the temporal
order in which variables started to exhibit timing variability. Importantly, if for
some v, varTime is undefined (we write varTime(v) = ⊥), the solver was able to
prove that v is constant-time. For any other variables v and w, if varTime(v) <
varTime(w), then v started to exhibit timing variability before w.4 Xenon uses
this map to break cyclic data-flow dependencies.
Computing the Counterexample. Using the data-flow graph, and varTime,
Xenon computes a reduced graph. Xenon removes from the dependency graph,
all nodes that are constant-time and all edges (w, v) such that varTime(w) >
varTime(v). Intuitively, if variable w has started to exhibit timing variability
after variable v, it cannot be the cause for v losing the constant-time prop-
erty. Finally, Xenon removes all nodes that cannot reach a sink node using the
remaining edges. This leaves us with a set of variables Cex ⊆ Vars without
4
     More formally, for variables v, w if varTime(v) < varTime(w), then there exist two
     runs πL and πR of some length n, and two numbers 0 6 i, j < n such that i is the
     smallest number such that live(πL , i)(v) 6= live(πR , i)(v) and similarly j is the smallest
     number such that live(πL , j)(w) 6= live(πR , j)(w) and i < j. This information can e.g.,
     be extracted from a concrete counterexample trace, like the one shown in Figure 4.
                            Solver-Aided Constant-Time Circuit Verification      13

incoming edges, which we identify as the root cause of the violation, and which
we present—as counterexample—to the user. We now define the reduced graph
in more detail.
Reachability. For dependency graph G , (V, D ∪ C) and nodes v, w ∈ V we
write v → w, if (v, w) ∈ (D ∪ C), v →n w, if there is a sequence v0 v1 . . . vn−1 ,
such that v0 = v and vn−1 = w, and vi → vi+1 for i ∈ {0, . . . , n − 2}. Finally, we
say w is reachable from v, if there exists n such that v →n w.
Reduced Graph. For a data-flow graph G , (V, D ∪ C), and map varTime,
we define the reduced graph with respect to varTime as the largest subgraph
G ′ , (V ′ , D ′ ∪ C ′ ) such that V ′ ⊆ V, D ′ ⊆ D, C ′ ⊆ C and
 1. No node is constant-time, i.e., for all v ∈ V ′ , varTime(v) 6= ⊥.
 2. All edges respect the causal order given by vartime, i.e., for all (v, w) ∈
    (D ′ ∪ C ′ ), we have varTime(v) 6 varTime(w).
 3. All nodes can reach a sink, i.e., for all v ∈ V ′ , there is o ∈ Snk such that o
    is reachable from v.
For variable v, and graph G , (V, D∪C), let pre(v, G) be the set of its immediate
predecessors in G, that is pre(v, G) , {w | (w, v) ∈ (D ∪ C)}. We define the
counterexample Cex of a graph G with map varTime as the set of nodes in
the reduced graph G ′ (wrt. varTime), that have no predecessors, i.e., Cex ,
{v | pre(v, G ′ ) = ∅}.
Example: Simplified Pipeline. The code in Figure 8 shows a simplified version
of        the           pipelined        processor   from        Figure         3.
                                                    Like in Figure 3, the pipeline
                                                    either stalls (Line 10) if
       1 assign ID_rt = ID_instr [ 20 : 16 ] ;      flag Stall is set (Line 9),
       2                                            or else forwards values to
       3 rom32 IMEM ( IF_pc , IF_instr );           the next stage (Line 13).
       4

       5 always @ (*)
                                                    To avoid a write-after-write
       6    stall = ( ID_rt == EX_rt )              data-hazard, the Stall flag
       7                                            is set, if the instructions
         always @ ( posedge clk ) begin
       8
                                                    in the execute and de-
       9    if ( Stall == 1) begin
      10          ID_instr <= ID_instr ;            code stage have the same
      11          EX_rt       <= EX_rt ;            target registers (Line 6).
      12    end else begin                          The target register is cal-
      13          ID_instr <= IF_instr ;
      14          EX_rt       <= ID_rt ;
                                                    culated from the current
      15    end                                     instruction (Line 1), and
      16 end                                        the instruction is, in turn,
                                                    fetched from memory us-
     Fig. 8: MIPS Pipeline Fragment in Verilog.     ing the current program
                                                    counter (Line 3). Note the
cyclic dependency between ID instr and Stall that turns comprehending the
root cause into a “chicken-and-egg” problem.
Dependency Graph. To check if the pipeline fragment executes in constant-
time, we mark IF pc as source, and ID instr as sink and run Xenon. Since the
14                                  Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

                                              Stall (X, 3)                                                 Stall (X, 3)

       IF inst (X, ⊥)    ID instr (X, 1)                       EX rt (X, 3)              ID instr (X, 1)                  EX rt (X, 3)

                                              ID rt (X, 2)                                                 ID rt (X, 2)
       IF pc (X, ⊥)




                   (a) Dependency Graph.                                          (b) Dependency Graph after
                                                                                  eliminating constant-time nodes
                                                                                  and edges violating the order
                                                                                  given by varTime.

                                                     Summary Graph

                                                                               Stall (X, 3)

                            IF instr (X, ⊥)                  ID instr (X, 1)


                                                                               Stall (X, 3)


                             IF inst (X, ⊥)                  ID instr (X, 1)                    EX rt (X, 3)


                                                                               ID rt (X, 2)
                              IF pc (X, ⊥)


                        (c) Dependency Graph with Module Summary.

Fig. 9: Figure 9a shows the dependency graph for Figure 8. Data-dependencies are
shown as solid edges, and control-dependencies are shown dashed. Each node is la-
beled with its varTime-value and marked (X) if Xenon was able to prove the vari-
able constant-time and (X) otherwise. Figure 9b shows the dependency graph after
eliminating constant-time nodes from Figure 9a, and removing edges that violate the
variable-time map. Removing the edge between Stall and ID instr breaks the cyclic
dependency in the original graph. Figure 9c shows the variable dependency graph with
a summary-graph extracted from the module summary.



pipeline is variable-time, the verification fails. To compute a minimal counterex-
ample, Xenon creates the dependency graph shown in Figure 9a. Each node is
annotated with information extracted from the failed proof attempt: the node
is labeled with its value under varTime, and is marked with (X) if Xenon was
able to verify that the variable is constant-time and (X) otherwise. Solid edges
represent data-, and dashed edges represent control dependencies. The ordering
induced by varTime allows us to break the cyclic dependency between variables
Stall and ID instr, thereby resolving the chicken-and-egg problem.
Reduced Dependency Graph. Figure 9b shows the dependency graph af-
ter removing all constant-time nodes and edges that violate the causal order-
ing. Xenon erases all nodes that cannot reach sink ID instr. This only leaves
ID instr which we return as counterexample.
Remark. In case the proof artifact only partially resolves the cyclic depen-
dencies, that is, vartime only defines a partial order over non-constant-time
variables, the reduced graph may still contain cycles, and therefore there may
be no nodes without predecessor. We can however still apply our technique by
computing the graph’s strongly connected components, and including all nodes
in the respective component in the counterexample.
                               Solver-Aided Constant-Time Circuit Verification      15

4.2   Assumption Synthesis
The previous step leaves us with a set of nodes Cex, which lost the constant-
time property first. Since these nodes must have lost the constant-time property
through a control dependency on a secret value, we can compute a set of vari-
ables Blame that are directly responsible: the immediate predecessors of Cex
in the dependency graph with respect to a control dependency. Formally, for
dependency graph G = (V, D ∪ C), we let Blame , {w | v ∈ Cex ∧ (w, v) ∈ C}.
To synthesize secrecy assumptions that remove the constant-time violation, we
could directly assume that all nodes in Blame are public. But this is often a
poor choice: variables in Blame can be defined deep inside the circuit, whereas
we would like to phrase our assumptions in terms of externally visible input
sources.
Finding Secrecy Assumptions via ILP. Instead, we compute a minimal
set of assumptions close to the input sources via a reduction to Integer Linear
Programming (ILP). To this end, we use a second proof artifact, a map secret
that—similar to varTime—describes the temporal order in which the verifier
determines variables have become secret, i.e., ceased being public. Let G ′ =
(V ′ , D ′ ∪ C ′ ) be the reduced dependency graph with respect to secret, and let
No ⊆ V ′ be a set of variables that the user chose to exclude from consideration.
Xenon produces constraints on a new set of variables: two constraint variables
mv ∈ {0, 1} and pv ∈ {0, 1}, for each program variable v, such that mv = 1, if
program variable v is marked public by an assumption, and pv = 1, if v can be
shown to be public, that is, it is either marked public, or all its predecessors are
public. Then, Xenon produces the following set of constraints.
          mv > pv ,                            if v ∈ V ′ , pre(v, G ′ ) = ∅ (1)
               P                    
                    w∈pre(v,G ′ ) pw
          mv +      #pre(v,G ′ )       > pv    if v ∈ V ′ , pre(v, G ′ ) 6= ∅ (2)

          pv = 1                               if v ∈ (Blame \ No)           (3)

          mv = 0                               if v ∈ No                     (4)
Constraints (1) and (2) ensure that a variable is public, if either it is marked
public, or all its predecessors in G ′ are public. Constraint (3) ensures that all
blamed variables that have not been excluded can be shown to be public, and
finally, constraint (4) ensures that all excluded constraints are not marked. Let
d(v, w) be a distance metric, i.e., a function that maps pairs of nodes to the
natural numbers. Then we want to solve the constraints using the following
objective function that we wish to minimize, where for v ∈ V ′ , we define as weight
the minimal distance from one of the source nodes wv = (arg minin∈Src d(in, v)):
                                     X
                                          wv mv .                        (objective)
                                       v∈V ′

A solution to the constraints defines a set of assumptions A = (Flush, Pub),
where we let Flush , {v ∈ V ′ | mv = 0, pv = 0} and Pub , {v ∈ V ′ | mv = 1}.
The constraints can be solved efficiently by an off-the-shelf ILP solver.
16                          Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

Example: Simplified Pipeline. Consider again the simplified pipeline in Fig-
ure 8. As we identified ID instr as the root cause in the previous step, we need to
ensure that its blame-set consisting of all indirect influences is public. ID instr
only depends on Stall, and therefore we add constraint pStall = 1. Since, all vari-
ables are secret (i.e., we didn’t make any public-assumptions yet), the reduced
graph is equal to the original graph. For variables IF instr and ID instr, we
                                                       p     +p
get: mIF instr + pIF pc > pIF instr and mID Instr + IF instr2 Stall > pID Instr . We
obtain the following objective function: mIF pc + 2mIF instr + 3mID instr +. . . .
Sending the constraints to an ILP solver produces a solution, where mIF pc = 1,
mv = 0, for all variables v 6= IF PC, and pv = 1, for all v. This corresponds
to the following assumption set A , (Flush, {IF PC}), where Flush includes all
variables except IF PC. This corresponds exactly to the desired minimal solution
where we only mark IF pc as public. Note that our method does not necessarily
result in all variables becoming public. We give an example in Appendix A.


4.3     Modular Assumption Synthesis

To avoid a blowup in constraint size, we want to avoid inlining instantiated
modules. We therefore extract a dependency graph from the module summary:
whenever the summary requires an input in to be public for an output out to
be constant-time, we draw a control dependency between in and out. Whenever
the summary requires an input in needs to be constant-time for an output
out to be constant-time, we draw a data dependency. Finally, we insert the
computed summary graph into the top level dependency graph, and connect the
instantiation parameters to the graph’s inputs and outputs.
Example. We modify Figure 8 to factor out the updates to ID instr into a sep-
arate module. Xenon computes the following summary invariant, from which we
create the graph in Figure 9c: ct(IF instr) ∧ pub(Stall) ⇒ pub(ID instr).
Since connecting the instantiated variables to the summary graph is equivalent
to the original graph (Figure 9a), our analysis returns the same result.


5      Implementation

Xenon is split into front-end and back-end. Our front-end translates Verilog
to the Iodine intermediate representation (IR) [46] and associates secrecy as-
sumptions with input and output wires. Our back-end translates this annotated
IR into verification conditions (Horn clauses); when verification fails, we gen-
erate counter examples and secrecy assumptions and present them to the user
for feedback. We implement the back-end in roughly 9KLOC Haskell, using the
liquid-fixpoint (0.8.0.2) [9] and Z3 (4.8.1) [35] libraries for verification, and
the GLPK (4.65) [7] library for synthesizing assumptions by solving the ILP
problem of § 4. Our tool and evaluation data sets (described next) are open
source and available on GitHub.5
5
     We omit the link for the double-blind review process.
                                     Solver-Aided Constant-Time Circuit Verification               17

                               #Assum         Check (H:M:S)          CEX Sugg Accept
    Name           #LOC                    CT                 # Iter
                            #flush #public    Inlined Modular        Ratio Ratio Ratio
    MIPS [8]         447        28        3   X     2.42     3.13     3 2.50%     1.73% 83.33%
    RISC-V [6]       514        10       11   X    13.21    10.23     5 16.24%    3.98% 46.90%
    SHA-256 [11]     563         4        3   X     7.21     8.90     2 4.28%     3.57% 100.00%
    FPU [2]         1108         3        1   X     9.10    11.54     1 0.33%     0.26% 100.00%
    ALU [5]         1327         1        3   X     2.01     2.29     2 0.88%     1.38% 75.00%
    FPU2 [3]         272        24        4   ✗     1.31     3.65     -       -        -       -
    RSA [12]         855        29        4   ✗     2.87     1.51     -       -        -       -
    AES-256 [10]     800         0        0 X 6:05:01.82      2.74    -      -     -      -
    SCARV [4]       8468        73       54 X   14:20.93   8:35.46   34 9.08% 5.68% 84.80%

    Total           14354      159       89 - 6:20:00.88   9:19.45   47 5.55%* 2.77%* 81.67%*
Table 1: #LOC is the number of lines of Verilog code (without comments or empty
lines), #Assum is the number of assumptions; flush and public are sizes of the sets
Flush and Pub respectively, CT shows if the program is constant-time, Check is
the time Xenon took to check the program; Inlined and Modular represent inlining
module instances and using module summaries respectively. # Iter is the number of
times the user has to invoke Xenon to verify the benchmark starting with an empty
set of assumptions; CEX Ratio is the average ratio of the number of identifiers in
the counterexample to all variable-time identifiers in a given iteration; Sugg Ratio
is the average ratio of the number of secrecy assumptions that Xenon suggests to all
secret variables in a given iteration, and Accept Ratio is the average ratio of the
suggested assumptions accepted by the user. In the Total row, we use * to denote
averages instead of sums. We do not run error localization on FPU2 and RSA because
they are variable-time; AES-256 does not need any assumptions.




6     Evaluation

We evaluate Xenon by asking the following questions:
 ◮ Q1: Are constant-time counterexamples effective at localizing the cause of
    verification failures?
 ◮ Q2: Are the secrecy assumptions suggested by Xenon useful?
 ◮ Q3: What is the combined effect of counterexamples and secrecy assumption
    generation on the verification effort?
 ◮ Q4: Do module summaries improve scalability?
To answer questions Q1 and Q2, we use Xenon to recover the assumptions for
the benchmark suite from [46]. These benchmarks include a MIPS and RISC-
V core, ALU and FPU modules, and RSA and SHA-256 crypto modules. To
evaluate questions Q3 and Q4, we evaluate Xenon on two challenging new
benchmarks, the SCARV “side-channel hardened RISC-V” processor [4] whose
size exceeds the largest benchmark from [46] by a factor of 10, and a highly
modular AES-256 implementation [10].
Summary. Xenon’s counterexample synthesis dramatically reduces the num-
ber of potential error locations users have to manually inspect (6% of its original
size) and most of Xenon’s assumption suggestions are accepted by the user (on
18                       Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

average 81.67%). Module summaries are key to reducing verification times for
certain hardware designs (e.g., for AES-256 crypto core summaries reduced the
verification time from six hours to a three seconds). We find the counterexam-
ples and secrecy assumptions suggested by Xenon to be crucial to reducing the
human-in-the-loop time from days to (at worst) hours.
Experimental Setup. We run all experiments on a 1.9GHz Intel Core i7-8650U
machine with 16 GB of RAM, running Ubuntu 20.04 with Linux kernel 5.4.
Methodology. For every benchmark, we start with an empty set of secrecy as-
sumptions and run Xenon repeatedly to recover the missing assumptions needed
to verify the benchmark. We collect the following information after every invo-
cation of the tool: the total number of variables that are variable-time and se-
cret; the size of the counterexamples measured by the number of variables they
contain; the number of assumptions Xenon suggests, and the number of as-
sumptions we reject during each iteration; finally, we record the number of times
we invoke Xenon to complete each verification task. With all the assumptions
in place, we measure the time it takes for the tool to verify each benchmark;
we report the median of thirty runs for all but the non-modular (inlined) AES
benchmark, for which—due to its size—we report the median of three runs.
Q1: Error Localization. To understand whether our counterexample gener-
ation is effective at localizing the cause of verification failures, we compare the
number of variables in the counterexample to the total number of non-constant-
time variables. The CEX Ratio column Table 1 reports the average ratio per it-
eration. On average, we observe that less than 6% of non-constant-time variables
are included in the counterexample. Since the total number of non-constant-time
variables is typically on the order of hundreds (e.g., the median (and geomean)
number of non-constant-time variables across all benchmarks and iteration is
97 (94)), this dramatically reduces the number of variables the developer has
to inspect in order to understand the violation. For the benchmarks that were
variable time, the counterexamples also precisely pinpointed where in the cir-
cuit the constant-time property was violated. For example, in the FPU2 bench-
mark Xenon included the state register in its third iteration counterexample.
This register indicates when the FPU’s output is ready. Inspecting the register’s
blame-set (similar to the process described in § 2.3) revealed that its value is set
depending on whether one of the operands to the division operation is NaN and
thus the FPU clearly leaks information about its operands.
Q2: Identifying Secrecy Assumptions. To assess the quality of secrecy as-
sumptions suggested by Xenon, we record the number of suggestions that the
user accepts (useful suggestions) and the ratio of suggestions to the total number
of secret variables the user would otherwise have to inspect manually. We find
that most (on average 81.67%) of Xenon’s suggestions are useful, reported in
the Accept Ratio column of Table 1. Moreover, we observe that the number
of variables included in the counterexamples is relatively small (Sugg Ratio
column); on average, we only had to inspect 2.77% of the secret variables.
Q3: Verification Effort. Finally, as a rough measure of the overall verification
effort, we count the number of user interactions, i.e., the number of times we
                           Solver-Aided Constant-Time Circuit Verification    19

invoked Xenon after modifying our set of secrecy assumptions. Verifying the
largest benchmark from [46], the Yarvi RISC-V core [6] took five invocations
over several minutes. The final assumptions we arrived at were the same as the
assumptions manually identified by the authors of Iodine in [46]; they, however,
took multiple days to identify these assumptions and verify this core [52]. Veri-
fying the SCARV core took thirty four iterations and roughly three hours; this
core is considerably larger (roughly 10×) than the Yarvi RISC-V core and, we
think, beyond what would possible with tools like Iodine, which rely on manual
annotations and error localization. Indeed, we found the error localization and
assumption inference to be especially useful in narrowing our focus and under-
standing to small parts of the core and avoid the need to understand complex
implementation details irrelevant to the analysis.
Q4: Scalability. To evaluate how module summaries affect the scalability, we
compare the time it takes to verify (or show variable-time) a program with and
without module summaries. Columns Inlined and Modular of Table 1 gives the
run times of Xenon with inlining (no summaries) and module summaries, re-
spectively. On the Iodine benchmarks (the first seven benchmarks), we observe
that module summaries don’t meaningfully speed up verification. Indeed, on av-
erage, module summaries only reduce the size of the query sent to our solver by
roughly 5% on these benchmarks. On the more complex AES-256 and SCARV
benchmarks, however, we see the benefit of module summaries. For AES-256, us-
ing module summaries reduces the query size by 99.7%, from 391.3MB to 1.2MB,
which, in turn, reduces the verification time by three orders of magnitude—from
six hours to three seconds. Module summaries allow Xenon to exploit the core’s
modular design, i.e., AES-256’s multiple and nested instantiations of the same
modules (see Figure 5). For SCARV, summaries reduce the query size by 41%,
and speed up the verification time by 40%. Though this reduction is not as
dramatic as the AES-256 case, the speedup did improve Xenon’s interactivity.


7   Related Work

Verifying Leakage Freedom. There are various techniques, such as ct-verif [16],
[21], and CT-Wasm [74], that verify constant-time execution of software, and
quantify leakage through timing and cache side-channels [13, 14, 39, 56, 68, 79].
However, their analyses do not directly apply to our setting: They consider
straight-line, sequential code, unlike the highly parallel nature of hardware.
There are many techniques for verifying information flow properties of hard-
ware. Kwon et al. [55] prove information flow safety of hardware for policies
that allow explicit declassification and are expressed over streams of input data.
SecVerilog [80] and Caisson [57] use information flow types to ensure that gen-
erated circuits are secure. GLIFT [71, 72] tracks the flow of information at the
gate level to eliminate timing channels. Other techniques such as HyperFlow [41],
GhostRider [58] and Zhang et al. [79] take the hardware and software co-design
approach to obtain end-to-end guarantees. dudect [66], detects end-to-end tim-
ing variabilities across the stack via a black-box technique based on statistical
20                       Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

measurements. Iodine [46], like Xenon, focuses on clock-precise constant-time
execution, not information flow. Unlike Xenon, none of these methods provides
help in elucidating secrecy assumptions, in case the verification fails—a feature
we found essential in scaling our analysis to larger benchmarks. We see the tech-
niques presented in this paper as complementary and would like to explore their
potential for scaling existing verification methods for hardware and software.
Fault Localization. There are several approaches to help developers localize
the root causes of software bugs [75]. Logic-based fault localization techniques
[30, 40, 50, 51] are the closest line of work to ours. For example, BugAssist [50]
uses a MAXSAT solver to compute the maximal set of statements that may
cause the failure given a failed error trace of a C program. Xenon is similar in
that we phrase localization as an optimization problem, allowing the use of ILP
to locate the possible cause of a non-constant-time variable. However, Xenon
focuses on constant-time, which is a relational property, and hardware which has
a substantially different execution model.
Synthesizing Assumptions. Our approach to synthesizing secrecy assump-
tions is related to work on precondition synthesis for memory safety. Data-driven
precondition inference techniques such as [43, 44, 62, 69, 70], unlike Xenon, re-
quire positive and negative examples to infer preconditions. Xenon’s synthesis
technique is an instance of abductive inference, which has been previously used
to triage analysis reports by allowing the user to interactively determine the
preconditions under which a program is safe or unsafe [36] or to identify the
most general assumptions or context under which a given module can be veri-
fied safe [26,37,38,45]. Unlike the above, our abduction strategy is tailored to the
relational constant-time property. Furthermore, Xenon uses information from
the verifier to ensure that the user interaction loop only invokes the ILP solver
(not the slower Horn-clause verifier), yielding a rapid cycle that pinpoints the
assumptions under which a circuit is constant-time. In future work, we would like
to see, if ideas introduced in Xenon can be applied to localization, explanation
and verification of other classes of correctness or security properties.
Modular Verification of Software and Hardware. Xenon exploits modu-
larity to verify large circuits by composing summaries of the behaviors of smaller
sub-components of those circuits. This is a well-know idea in verification; for
example, [67] shows how to perform dataflow analysis of large programs by com-
puting procedure summaries, and Houdini [42] shows how to verify programs by
automatically synthesizing pre- and post- conditions summarizing the behaviors
of individual procedures. On the hardware side, model checkers like Mocha [17]
and SMV [59] use rely-guarantee reasoning to perform modular verification.
Kami [29] and [73] develops a compositional hardware verification methodology
using the Coq proof assistant. However, the above require the user to provide
module interface abstractions. There are some approaches that synthesize such
abstractions in an counterexample guided fashion [48,81]. All focus on functional
verification of properties of a single run, and do not support abstractions needed
to reason about timing-channels which require relational hyperproperties [31].
                            Solver-Aided Constant-Time Circuit Verification     21

References

 1. BearSSL - constant-time crypto. https://www.bearssl.org/constanttime.html.
    (Accessed on 08/19/2020).
 2. fpga mc/fpu         at     master      ·      monajalal/fpga mc         ·    github.
    https://github.com/monajalal/fpga mc/tree/master/fpu.                (Accessed on
    08/16/2020).
 3. Github - dawsonjon/fpu: synthesiseable ieee 754 floating point library in verilog.
    https://github.com/dawsonjon/fpu. (Accessed on 08/16/2020).
 4. Github - scarv/scarv-cpu: Scarv: a side-channel hardened risc-v platform.
    https://github.com/scarv/scarv-cpu. (Accessed on 08/16/2020).
 5. Github - scarv/xcrypto: Xcrypto: a cryptographic ise for risc-v.
    https://github.com/scarv/xcrypto. (Accessed on 08/19/2020).
 6. Github       -   tommythorn/yarvi:      Yet    another    risc-v    implementation.
    https://github.com/tommythorn/yarvi. (Accessed on 08/16/2020).
 7. Glpk       -     gnu     project    -     free    software      foundation     (fsf).
    https://www.gnu.org/software/glpk/. (Accessed on 08/10/2020).
 8. iodine/benchmarks/472-mips-pipelined at master · gokhankici/iodine · github.
    https://github.com/gokhankici/iodine/tree/master/benchmarks/472-mips-pipelined.
    (Accessed on 08/16/2020).
 9. liquid-fixpoint:    Horn    clause    constraint   solving     for   liquid   types.
    https://github.com/ucsd-progsys/liquid-fixpoint. Accessed: 2018-08-29.
10. Overview :: AES :: OpenCores. https://opencores.org/projects/tiny aes. (Ac-
    cessed on 08/05/2020).
11. Overview :: Sha cores :: Opencores. https://opencores.org/projects/sha core.
    (Accessed on 08/16/2020).
12. Rsa4096/modexp 2.0 at master · fatestudio/rsa4096 · github. . (Accessed on
    08/16/2020).
13. TIS-CT. http://trust-in-soft.com/tis-ct/.
14. J Bacelar Almeida, Manuel Barbosa, Jorge S Pinto, and Bárbara Vieira. Formal
    verification of side-channel countermeasures using self-composition. In Science of
    Computer Programming, 2013.
15. José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, François Dupressoir, and
    Michael Emmi. Verifying constant-time implementations. In USENIX Security
    Symposium, 2016.
16. José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, François Dupressoir, and
    Michael Emmi. Verifying constant-time implementations. In USENIX Security,
    2016.
17. Rajeev Alur and Thomas A. Henzinger. Reactive modules. Formal Methods Syst.
    Des., 15(1):7–48, 1999.
18. Marc Andrysco, David Kohlbrenner, Keaton Mowery, Ranjit Jhala, Sorin Lerner,
    and Hovav Shacham. On subnormal floating point and abnormal timing. In S&P,
    2015.
19. Marc Andrysco, Andres Nötzli, Fraser Brown, Ranjit Jhala, and Deian Stefan. To-
    wards verified, constant-time floating point operations. In Proceedings of the ACM
    SIGSAC Conference on Computer and Communications Security. ACM, 2018.
20. Manuel Barbosa, Gilles Barthe, Karthikeyan Bhargavan, Bruno Blanchet, Cas Cre-
    mers, Kevin Liao, and Bryan Parno. SoK: Computer-aided cryptography. In IEEE
    Symposium on Security and Privacy, 2021.
22                        Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

21. Gilles Barthe, Gustavo Betarte, Juan Campo, Carlos Luna, and David Pichardie.
    System-level non-interference for constant-time cryptography. In Proceedings of
    the ACM SIGSAC Conference on Computer and Communications Security. ACM,
    2014.
22. Daniel J. Bernstein. Cache-timing attacks on AES. Technical report, 2005.
23. Nikolaj Bjørner, Arie Gurfinkel, Ken McMillan, and Andrey Rybalchenko. Horn
    clause solvers for program verification. In Fields of Logic and Computation. 2015.
24. Ferdinand Brasser, Urs Müller, Alexandra Dmitrienko, Kari Kostiainen, Srdjan
    Capkun, and Ahmad-Reza Sadeghi. Software grand exposure:SGX cache attacks
    are practical. In Workshop on Offensive Technologies, 2017.
25. David Brumley and Dan Boneh. Remote timing attacks are practical. Computer
    Networks, 2005.
26. Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. Com-
    positional Shape Analysis by Means of Bi-Abduction. 58(6):26:1–26:66.
27. Sunjay Cauligi, Craig Disselkoen, Klaus von Gleissenthall, Dean Tullsen, Deian
    Stefan, Tamara Rzk, and Gilles Barthe. Constant-time foundations for the new
    Spectre era. In Programming Language Design and Implementation (PLDI). ACM
    SIGPLAN, 2020.
28. Sunjay Cauligi, Gary Soeller, Brian Johannesmeyer, Fraser Brown, Riad S. Wahby,
    John Renner, Benjamin Gregoire, Gilles Barthe, Ranjit Jhala, and Deian Stefan.
    FaCT: A dsl for timing-sensitive computation. In Programming Language Design
    and Implementation (PLDI). ACM SIGPLAN, 2019.
29. Joonwon Choi, Muralidaran Vijayaraghavan, Benjamin Sherman, Adam Chlipala,
    and Arvind. Kami: A Platform for High-Level Parametric Hardware Specification
    and Its Modular Verification. In International Conference on Functional Program-
    ming (ICFP). ACM SIGPLAN, 2017.
30. Jürgen Christ, Evren Ermis, Martin Schäf, and Thomas Wies. Flow-sensitive fault
    localization. Lecture Notes in Computer Science Verification, Model Checking, and
    Abstract Interpretation, pages 189–208, 2013.
31. Michael R. Clarkson and Fred B. Schneider. Hyperproperties. Journal of Computer
    Security, 2010.
32. Shaanan Cohney, Andrew Kwong, Shahar Paz, Daniel Genkin, Nadia Heninger,
    Eyal Ronen, and Yuval Yarom. Pseudorandom black swans: Cache attacks on
    CTR DRBG. In 2020 IEEE Symposium on Security and Privacy (SP). IEEE,
    2020.
33. Fergus Dall, Gabrielle De Micheli, Thomas Eisenbarth, Daniel Genkin, Nadia
    Heninger, Ahmad Moghimi, and Yuval Yarom. CacheQuote: Efficiently recov-
    ering long-term secrets of SGX EPID via cache attacks. IACR Transactions on
    Cryptographic Hardware and Embedded Systems, 2018(2), May 2018.
34. Lesly-Ann Daniel, Sébastien Bardin, and Tamara Rezk. BINSEC/REL: Efficient
    relational symbolic execution for constant-time at binary-level. In IEEE Sympo-
    sium on Security and Privacy, 2020.
35. Leonardo de Moura and Nikolaj Bjørner. Z3: An efficient SMT solver. In TACAS,
    2008.
36. Isil Dillig, Thomas Dillig, and Alex Aiken. Automated error diagnosis using abduc-
    tive inference. In Proceedings of the 33rd ACM SIGPLAN Conference on Program-
    ming Language Design and Implementation, PLDI ’12, pages 181–192. Association
    for Computing Machinery.
37. Isil Dillig, Thomas Dillig, Boyang Li, and Ken McMillan. Inductive invariant
    generation via abductive inference. SIGPLAN Not., 48(10):443–456, October 2013.
                             Solver-Aided Constant-Time Circuit Verification        23

38. Isil Dillig, Thomas Dillig, Boyang Li, Ken McMillan, and Mooly Sagiv. Synthesis
    of circular compositional program proofs via abduction. 19(5):535–547.
39. Goran Doychev, Dominik Feld, Boris Köpf, Laurent Mauborgne, and Jan Reineke.
    Cacheaudit: A tool for the static analysis of cache side channels. In USENIX
    Security, 2013.
40. Evren Ermis, Martin Schäf, and Thomas Wies. Error invariants. FM 2012: Formal
    Methods Lecture Notes in Computer Science, pages 187–201, Aug 2012.
41. Andrew Ferraiuolo, Mark Zhao, Andrew C Myers, and G Edward Suh. Hyperflow:
    A processor architecture for nonmalleable, timing-safe information flow security.
    In SIGSAC, 2018.
42. Cormac Flanagan and K Rustan M Leino. Houdini, an Annotation Assistant for
    ESC/Java. pages 500–517. Springer, Berlin, Heidelberg.
43. Pranav Garg, Christof Löding, P. Madhusudan, and Daniel Neider. Ice: A robust
    framework for learning invariants. Computer Aided Verification Lecture Notes in
    Computer Science, pages 69–87, 2014.
44. Pranav Garg, Daniel Neider, P. Madhusudan, and Dan Roth. Learning invariants
    using decision trees and implication counterexamples. In Principles of Program-
    ming Languages, POPL ’16. ACM.
45. Roberto Giacobazzi. Abductive analysis of modular logic programs. In Proceedings
    of the 1994 International Symposium on Logic Programming, ILPS ’94, pages 377–
    391. MIT Press.
46. Klaus V. Gleissenthall, Rami Gökhan Kici, Deian Stefan, and Ranjit Jhala. IO-
    DINE: Verifying constant-time execution of hardware. In USENIX Conference on
    Security Symposium, 2019.
47. Michael J. C. Gordon. The semantic challenge of verilog hdl. In LICS, 1995.
48. Anubhav Gupta, Kenneth L. McMillan, and Zhaohui Fu. Automated assumption
    generation for compositional verification. Formal Methods Syst. Des., 32(3):285–
    301, 2008.
49. Andreas Haeberlen, Benjamin C. Pierce, and Arjun Narayan. Differential privacy
    under fire. In David Wagner, editor, USENIX Security, 2011.
50. Manu Jose and Rupak Majumdar. Bug-assist: Assisting fault localization in ANSI-
    c programs. In Ganesh Gopalakrishnan and Shaz Qadeer, editors, Computer Aided
    Verification, Lecture Notes in Computer Science, pages 504–509. Springer.
51. Manu Jose and Rupak Majumdar. Cause clue clauses. Proceedings of the 32nd
    ACM SIGPLAN conference on Programming language design and implementation
    - PLDI 11, 2011.
52. Rami Gökhan Kici. Personal communication, August 2020.
53. Paul C Kocher. Timing attacks on implementations of Diffie-Hellman, RSA, DSS,
    and other systems. In CRYPTO, 1996.
54. David Kohlbrenner and Hovav Shacham. On the effectiveness of mitigations against
    floating-point timing channels. In USENIX Security, 2017.
55. Hyoukjun Kwon, William Harris, and Hadi Esameilzadeh. Proving flow security of
    sequential logic via automatically-synthesized relational invariants. In CSF, 2017.
56. Adam Langley. ctgrind: Checking that functions are constant time with valgrind.
    https://github.com/agl/ctgrind/.
57. Xun Li, Mohit Tiwari, Jason K Oberg, Vineeth Kashyap, Frederic T Chong, Tim-
    othy Sherwood, and Ben Hardekopf. Caisson: a hardware description language for
    secure information flow. In PLDI, 2011.
58. Chang Liu, Austin Harris, Martin Maas, Michael Hicks, Mohit Tiwari, and Elaine
    Shi. Ghostrider: A hardware-software system for memory trace oblivious compu-
    tation. SIGPLAN Notices, 2015.
24                        Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

59. Kenneth L. McMillan. A compositional rule for hardware design refinement. In
    Orna Grumberg, editor, Computer Aided Verification, 9th International Confer-
    ence, CAV ’97, Haifa, Israel, June 22-25, 1997, Proceedings, volume 1254 of Lecture
    Notes in Computer Science, pages 24–35. Springer, 1997.
60. Daniel Moghimi, Berk Sunar, Thomas Eisenbarth, and Nadia Heninger. TPM-
    FAIL:TPM meets timing and lattice attacks. In USENIX Security, 2020.
61. Dag Arne Osvik, Adi Shamir, and Eran Tromer. Cache attacks and countermea-
    sures: the case of AES. In Cryptographers’ Track at the RSA Conference. Springer,
    2006.
62. Saswat Padhi, Rahul Sharma, and Todd Millstein. Data-driven precondition infer-
    ence with learned features. In Proceedings of the 37th ACM SIGPLAN Conference
    on Programming Language Design and Implementation, PLDI ’16, pages 42–56.
    Association for Computing Machinery.
63. Christos H. Papadimitriou and Kenneth Steiglitz. Combinatorial Optimization:
    Algorithms and Complexity. Prentice-Hall, Inc., USA, 1982.
64. Ashay Rane, Calvin Lin, and Mohit Tiwari. Raccoon: Closing digital side-channels
    through obfuscated execution. In USENIX Security, 2015.
65. Ashay Rane, Calvin Lin, and Mohit Tiwari. Secure, precise, and fast floating-point
    operations on x86 processors. In USENIX Security, 2016.
66. Oscar Reparaz, Joseph Balasch, and Ingrid Verbauwhede. Dude, is my code con-
    stant time? In DATE, 2017.
67. Thomas W. Reps, Susan Horwitz, and Shmuel Sagiv. Precise interprocedural
    dataflow analysis via graph reachability. In Ron K. Cytron and Peter Lee, edi-
    tors, Conference Record of POPL’95: 22nd ACM SIGPLAN-SIGACT Symposium
    on Principles of Programming Languages, San Francisco, California, USA, Jan-
    uary 23-25, 1995, pages 49–61. ACM Press, 1995.
68. Bruno Rodrigues, Fernando Magno Quintão Pereira, and Diego F Aranha. Sparse
    representation of implicit flows with applications to side-channel detection. In
    CCC, 2016.
69. Xujie Si, Hanjun Dai, Mukund Raghothaman, Mayur Naik, and Le Song. Learning
    loop invariants for program verification. In S. Bengio, H. Wallach, H. Larochelle,
    K. Grauman, N. Cesa-Bianchi, and R. Garnett, editors, Advances in Neural Infor-
    mation Processing Systems 31, pages 7751–7762. Curran Associates, Inc.
70. Xujie Si, Aaditya Naik, Hanjun Dai, Mayur Naik, and Le Song. Code2Inv: A Deep
    Learning Framework for Program Verification. In Shuvendu K. Lahiri and Chao
    Wang, editors, Computer Aided Verification, Lecture Notes in Computer Science,
    pages 151–164. Springer International Publishing.
71. Mohit Tiwari, Jason K Oberg, Xun Li, Jonathan Valamehr, Timothy Levin, Ben
    Hardekopf, Ryan Kastner, Frederic T. Chong, and Timothy Sherwood. Crafting a
    usable microkernel, processor, and i/o system with strict and provable information
    flow security. In ISCA, 2011.
72. Mohit Tiwari, Hassan MG Wassel, Bita Mazloom, Shashidhar Mysore, Frederic T
    Chong, and Timothy Sherwood. Complete information flow tracking from the gates
    up. In Sigplan Notices, 2009.
73. Muralidaran Vijayaraghavan, Adam Chlipala, Arvind, and Nirav Dave. Modular
    Deductive Verification of Multiprocessor Hardware Designs. In Daniel Kroening
    and Corina S. Păsăreanu, editors, Computer Aided Verification, Lecture Notes in
    Computer Science, pages 109–127. Springer International Publishing.
74. Conrad Watt, John Renner, Natalie Popescu, Sunjay Cauligi, and Deian Stefan.
    CT-Wasm: Type-driven secure cryptography for the web ecosystem. 2019.
                             Solver-Aided Constant-Time Circuit Verification       25

75. W. Eric Wong, Ruizhi Gao, Yihao Li, Rui Abreu, and Franz Wotawa. A survey on
    software fault localization. IEEE Transactions on Software Engineering, 42(8):707–
    740, 2016.



76. Yuan Xiao, Mengyuan Li, Sanchuan Chen, and Yinqian Zhang. STACCO: Dif-
    ferentially analyzing side-channel traces for detecting SSL/TLS vulnerabilities in
    secure enclaves. In Proceedings of the 2017 ACM SIGSAC Conference on Computer
    and Communications Security, pages 859–874, 2017.



77. Yuval Yarom, Daniel Genkin, and Nadia Heninger. CacheBleed: a timing attack
    on openssl constant-time rsa. Journal of Cryptographic Engineering, 7(2):99–112,
    2017.



78. Jiyong Yu, Lucas Hsiung, Mohamad El Hajj, and Christopher W Fletcher. Data
    oblivious ISA extensions for side channel-resistant and high performance comput-
    ing. In NDSS, 2019.



79. Danfeng Zhang, Aslan Askarov, and Andrew C. Myers. Language-based control
    and mitigation of timing channels. In PLDI, 2012.



80. Danfeng Zhang, Yao Wang, G. Edward Suh, and Andrew C. Myers. A hardware
    design language for timing-sensitive information-flow security. In ASPLOS, 2015.



81. Hongce Zhang, Weikun Yang, Grigory Fedyukovich, Aarti Gupta, and Sharad Ma-
    lik. Synthesizing Environment Invariants for Modular Hardware Verification. In
    Dirk Beyer and Damien Zufferey, editors, Verification, Model Checking, and Ab-
    stract Interpretation, Lecture Notes in Computer Science, pages 202–225. Springer
    International Publishing.
26                        Rami Gökhan Kıcı , Klaus v. Gleissenthall , Deian Stefan, and Ranjit Jhala

A    Example: Not all Variables Become Public

Example 3. One might think that Xenon requires all variables occurring in
branch conditions to be annotated as public, however, this is not the case. Ap-
pendix A shows an example of such a program. Running Xenon produces the
dependency graph shown in Figure 10. Xenon computes root-cause candidates
by eliminating constant-time nodes and edges violating the precedence order.
The result is shown in Figure 11. Removing all nodes that cannot reach source
out leaves only nodes r3 and out, and since r3 has no predecessors, we identify
it as the earliest node that became non-constant time, and therefore the root
cause of the problem. Solving the ILP constraints yields stall as candidate as-
sumption, and marking stall as public and restarting Xenon verifies constant
time execution without the need to mark cond as public. This is possible because
Xenon is able to prove that tmp1 and tmp2 have the same colors, irrespective of
the value of cond, i.e., that tmp1• =tmp2• holds irrespective of cond.
 1   module test ( clk , in , cond , bubble , out );
 2     input wire clk , in , cond , bubble ;
 3     output reg out ;
 4     reg tmp1 , tmp2 , r2 , r3 ;
 5

 6     always @ ( posedge clk ) begin
 7       tmp1 <= in | r3 ;
 8       tmp2 <= in & r3 ;
 9

10       if ( cond )
11         r2 <= tmp1 ;
12       else
13         r2 <= tmp2 ;
14

15       if ( stall )
16         r3 <= r3 ;
17       else
18         r3 <= r2 ;
19

20       out <= r3 ;
21     end
22   endmodule



                       cond (X, ⊥)                  stall (X, ⊥)


                                     tmp1 (X, 10)    r3 (X, 7)


                       r2 (X, 13)                                  out (X, 10)


                                     tmp2 (X, 10)    in (X, ⊥)



                 Fig. 10: Example 3: Variable dependency graph.
                               Solver-Aided Constant-Time Circuit Verification   27

                                   tmp1 (X, 10)   r3 (X, 7)


                      r2 (X, 13)                              out (X, 10)


                                   tmp2 (X, 10)



Fig. 11: Example 3: Variable dependency graph after eliminating non-ct nodes and
edges that violate the precedence relation.
