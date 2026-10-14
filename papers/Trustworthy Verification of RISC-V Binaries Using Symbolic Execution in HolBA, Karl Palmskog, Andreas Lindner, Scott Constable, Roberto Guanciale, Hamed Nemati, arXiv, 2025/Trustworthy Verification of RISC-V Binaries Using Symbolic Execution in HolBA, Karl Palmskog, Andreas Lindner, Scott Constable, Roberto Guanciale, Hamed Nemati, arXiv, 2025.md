                                             Trustworthy Verification of RISC-V Binaries
                                                 Using Symbolic Execution in HolBA

                                         Karl Palmskog1 , Andreas Lindner2 , Scott Constable3 , Roberto Guanciale1 , and
                                                                       Hamed Nemati1
                                                      1
                                                          KTH Royal Institute of Technology, Stockholm, Sweden
arXiv:2503.14135v1 [cs.LO] 18 Mar 2025




                                                            {palmskog,robertog,hnemati}@kth.se
                                                               2
                                                                 Uppsala University, Uppsala, Sweden
                                                               andreas.lindner@angstrom.uu.se
                                                                          3
                                                                            Intel Labs, USA
                                                                 scott.d.constable@intel.com



                                               Abstract. Many types of formal verification establish properties about
                                               abstract high-level program representations, leaving a large gap to pro-
                                               grams at runtime. Although gaps can sometimes be narrowed by tech-
                                               niques such as refinement, a verified program’s trusted computing base
                                               may still include compilers and inlined assembly. In contrast, verification
                                               of binaries following an Instruction Set Architecture (ISA) such as RISC-
                                               V can ensure that machine code behaves as expected on real hardware.
                                               While binary analysis is useful and sometimes even necessary for ensuring
                                               trustworthiness of software systems, existing tools do not have a formal
                                               foundation or lack automation for verification. We present a workflow
                                               and toolchain based on the HOL4 theorem prover and the HolBA binary
                                               analysis library for trustworthy formal verification of RISC-V binaries.
                                               The toolchain automates proofs of binary contracts by forward symbolic
                                               execution of programs in HolBA’s intermediate language, BIR. We val-
                                               idated our toolchain by verifying correctness of RISC-V binaries with
                                               (1) an implementation of the ChaCha20 stream cipher and (2) hand-
                                               written assembly for context switching in an operating system kernel.

                                               Keywords: Binary analysis · Symbolic execution · RISC-V · HOL4.


                                         1   Introduction
                                         Many types of formal verification are based on using an abstract representation
                                         of a program, e.g., a pure function or high-level program syntax inside an inter-
                                         active theorem prover (ITP). While this approach may leave a large gap between
                                         the verified abstraction and the actual code being executed, engineers can use
                                         techniques such as step-wise refinement or extraction to extend verification down
                                         to executable source code [7]. Still, the Trusted Computing Base (TCB) for such
                                         verified programs could include unverified compilers and inlined hand-written
                                         assembly, which may undermine formal guarantees.
                                             In contrast to high-level source code, machine code (assembly) in binary
                                         format is what is typically executed directly on the underlying hardware, and
2       K. Palmskog et al.

Instruction Set Architectures (ISAs) such as RISC-V [24] have a well-defined
machine state and a limited number of simple operations. Hence, by targeting
this lower abstraction level, binary analysis tools [3,22] can ensure strong prop-
erties, e.g., by ruling out issues with compilers and inlined assembly. However,
while binary analysis is useful—and even necessary for ISA-level guarantees in
software systems tied to a proprietary unverified compiler—existing tools either
do not have a formal foundation or lack automation for verifying non-trivial high
assurance machine code, such as for cryptographic ciphers.
    We present a toolchain based on the HOL4 theorem prover [12] and the
HolBA library [16] for trustworthy formal verification of RISC-V (RV64G in-
struction set) binaries. The toolchain is based on lifting RISC-V disassembly to
the intermediate language BIR embedded in HOL4 and then performing proof-
producing forward symbolic execution of BIR programs. We express properties
of binaries to be verified using binary-level contracts [17] via the independently
developed L3 model of RISC-V [9]; when such contracts are translated to BIR
level and proved automatically using symbolic analysis, we backlift the results
to obtain RISC-V contract theorems about lifted binaries.
    Ultimately, our goal is to automate key steps of translation validation, where
binary code is demonstrated to refine the behavior of an abstract algorithmic
specification [20]. Intuitively, this means that our toolchain is not meant for prov-
ing that some assembly routine sorts a list, but instead that it refines (is simu-
lated by) a specific merge sort implementation. Hence, to validate our toolchain,
we apply it to case studies from two relevant high-assurance domains: cryptog-
raphy and operating system kernels. As with most ITP-based tools, some parts
in our toolchain are fully automated (albeit incomplete), while others require
manual interaction with HOL4, e.g., to express specifications.
    In summary, we make the following contributions:

 1. We describe a workflow for verifying RISC-V binaries, which we implemented
    by way of a toolchain on top of HOL4 and HolBA using proof-producing
    symbolic execution.
 2. We demonstrate the toolchain in two case studies: one binary implementing
    the ChaCha20 stream cipher [1], and one binary with hand-written RISC-V
    assembly from a separation kernel [13].
 3. We perform an evaluation of our symbolic execution approach to investigate
    whether it scales to large RISC-V binaries.

The toolchain components enabling our workflow are all included in the HolBA
library and available together with examples under an open source license [4].


2   Background and Related Work

In this section, we give some background on binary analysis, and contrast our
binary verification with related approaches and previous work.
                                Trustworthy Verification of RISC-V Binaries         3




Fig. 1. Binary analysis tool architecture centering on an intermediate language (IL).


Binary analysis and intermediate languages. Analysis of machine code indepen-
dent of any high-level language goes back to the 1940s [10], but received little
attention in the context of formal verification until the late 1980s [6]. Mod-
ern binary analysis tools include BitBlaze [22] and the Binary Analysis Platform
(BAP) [3]. These and similar tools, including HolBA, use the architecture shown
in Figure 1, where binaries based on many different ISAs are translated to a sin-
gle well-defined intermediate language (IL). This IL, called BIL for BAP and BIR
for HolBA, is then used for many different analyses, e.g., symbolic execution and
control flow, with results expressed in terms of the corresponding binary.

Binary verification and verified compilation. Properties of program source code
can be formally transferred to a corresponding binary by a verified compiler such
as CompCert [14] and CakeML [23]. Verified compilation (VC) is an orthogo-
nal approach to direct binary verification (BV), with different advantages and
limitations. Most directly, VC requires access to program source code, while BV
does not. ITP-based environments for program verification based on VC, such as
VST [5] and Characteristic Formulae [11], do not allow expression of ISA-level
properties, while BV permits (only) such properties. Inlined assembly in source
code must be explicitly supported for VC, while BV is unaffected. Finally, sup-
port for custom ISA extensions, e.g., for hardware acceleration of cryptographic
code, may require extensive additions to the verified compiler and its correct-
ness theorem. In contrast, BV support for ISA extensions typically only requires
minor changes to the IL and the process of converting binaries to the IL.
    Binary verification can also be achieved indirectly by decompiling the binary
into a model that resembles the source language (e.g., C) and then verifying
that model. This approach was used to extend the seL4 refinement proofs from C
source code to the compiled binary [20]. The approach’s coverage is limited by the
decompiler, which may be unable to produce models for unconventional control
flow behaviors or for ISA extensions that are not captured by the modeling
language. For example, the decompiler used by Sewell et al. [20] was unable to
generate models for several procedures that originated from assembly source.

The HolBA library. HolBA is a library for binary analysis based on the HOL4
theorem prover [21]. Initial work on HolBA defined the BIR intermediate lan-
4      K. Palmskog et al.




             Fig. 2. Binary analysis workflow using HOL4 and HolBA.


guage for low-level code and functionality for proof-producing lifting of bina-
ries [16]. Subsequent work integrated a Hoare-style logic for expressing and rea-
soning about properties of BIR programs and for ISAs supported by HolBA [17].
However, this previous work did not include domain-specific automation for ver-
ification of binary programs. That is, verification had to be done by manually
applying Hoare-style rules inside HOL4. Moreover, before the work described in
this paper, end-to-end verification of RISC-V binaries was not possible.


3   Binary Verification Workflow
The intended workflow of our toolchain consists of the steps below and is illus-
trated in Figure 2. While other workflows are possible using HolBA, e.g., for
other ISAs such as ARMv8, we focus on a highly automated workflow for verifi-
cation of functional correctness properties for RISC-V. As with most verification
approaches using ITPs, our workflow is incomplete in the sense that verification
steps can fail without a specification being false.

0. Compilation: Compile a source program to a RISC-V binary. This step is
   completely optional, but adjustments to compilation can simplify verification.
1. Disassembly: Disassemble the RV64G binary.
2. Lifting: Translate the disassembly to BIR and generate a HOL4 theorem
   connecting the BIR program to corresponding binary code.
3. RISC-V specification: Specify program boundaries inside disassembly and
   define pre- and post-conditions using the L3 model of RISC-V.
4. BIR specification: Translate RISC-V pre-conditions and post-conditions
   to BIR expressions and prove equivalence in HOL4.
5. Symbolic execution: Symbolically execute the BIR program according to
   the program boundaries and obtain a HOL4 symbolic analysis theorem.
6. Symbolic transfer: Prove a HOL4 contract theorem for the BIR program
   using the pre- and post-conditions via the symbolic analysis theorem.
7. Backlifting: Prove a RISC-V contract theorem by way of the BIR contract
   theorem and the lifting theorem.

    To explain each of the steps, we use the running example defined in Figure 3,
which shows different representations of a simple program incr that increments
its argument (a 64-bit unsigned integer) by one.
                               Trustworthy Verification of RISC-V Binaries       5

        #include <stdint.h>
        uint64_t incr(uint64_t i) { return i + 1; }

        incr:     file format elf64-littleriscv
        Disassembly of section .text:
        0000000000010488 <incr>:
           10488:       00150513                addi     a0,a0,1
           1048c:       00008067                ret

        <| bb_label := BL_Address_HC
            (Imm64 0x10488w) "00150513 (addi a0,a0,1)";
           bb_statements :=
            [BStmt_Assign (BVar "x10" (BType_Imm Bit64))
             (BExp_BinExp BIExp_Plus
              (BExp_Den (BVar "x10" (BType_Imm Bit64)))
              (BExp_Const (Imm64 1w)))];
           bb_last_statement :=
            BStmt_Jmp (BLE_Label (BL_Address (Imm64 0x1048Cw))) |>


Fig. 3. Example program that increments a 64-bit unsigned integer represented in C
(top), corresponding RISC-V disassembly (middle) and BIR abstract syntax (bottom).


Compilation. Our toolchain and workflow does not require program source code,
only a RISC-V (RV64G) binary. However, we expect many users to perform
binary analysis on programs for which they have source code, which enables
control over compiler optimizations which can affect the size of the binary.

Disassembly. We disassemble RV64G binaries using gnu-objdump to enable
further processing. The middle box in Figure 3 shows our example’s disassembly.

Lifting. Our lifting tool parses the disassembly using specifications of program
bounds (address of initial instruction and address after final instruction to lift)
and translates the indicated input into a BIR program inside HOL4. Formally, a
BIR program is a list of blocks containing statements in abstract syntax, as shown
at the bottom of Figure 3. Lifting also produces a HOL4 theorem expressing,
roughly, that the BIR program simulates the corresponding RISC-V program—
this theorem is what enables later backlifting of contracts from BIR to RISC-V.

RISC-V specification. We express RISC-V binary contracts as pairs of pre- and
postconditions in HOL4 using the machine state defined by the L3 model, as
illustrated at the top of Figure 4, where a0 is the standardized application
binary interface (ABI) name of register x10.

BIR specification. To enable symbolic execution, we (manually) translate RISC-
V pre- and postconditions to BIR, exemplified below the top box in Figure 4.

Symbolic execution, transfer, and backlifting. Once the BIR specification is set
up, we can symbolically execute the BIR program. This process uses the BIR
precondition as a path condition and produces a general symbolic execution
theorem. We then use this theorem to automatically prove a BIR contract and
finally a RISC-V contract, as shown in the lowermost parts of Figure 4.
6       K. Palmskog et al.

        Definition riscv_incr_pre_def: (* RISC-V precondition via L3 *)
         riscv_incr_pre (pre_x10:word64)(m:riscv_state) : bool =
         (m.c_gpr m.procID 10w = pre_x10)
        End
        Definition riscv_incr_post_def: (* RISC-V postcondition via L3 *)
         riscv_incr_post (pre_x10:word64) (m:riscv_state) : bool =
         (m.c_gpr m.procID 10w = pre_x10 + 1w)
        End

        Definition bir_incr_pre_def: (* BIR precondition *)
         bir_incr_pre (pre_x10:word64) : bir_exp_t = BExp_BinPred
          BIExp_Equal (BExp_Den (BVar "x10" (BType_Imm Bit64)))
           (BExp_Const (Imm64 pre_x10))
        End
        Definition bir_incr_post_def: (* BIR postcondition *)
         bir_incr_post (pre_x10:word64) : bir_exp_t = BExp_BinPred
          BIExp_Equal (BExp_Den (BVar "x10" (BType_Imm Bit64)))
            (BExp_BinExp BIExp_Plus (BExp_Const (Imm64 pre_x10))
             (BExp_Const (Imm64 1w)))
        End

        Theorem bir_cont_incr: (* BIR contract via symbolic execution*)
         bir_cont bir_incr_prog bir_exp_true
          (BL_Address (Imm64 incr_init_addr))
          {BL_Address (Imm64 incr_end_addr)} {} (bir_incr_pre pre_x10)
          (\l. if l = BL_Address (Imm64 incr_end_addr)
             then bir_incr_post pre_x10 else bir_exp_false)

        Theorem riscv_cont_incr: (* RISC-V contract via backlifting *)
         riscv_cont bir_incr_progbin incr_init_addr {incr_end_addr}
          (riscv_incr_pre pre_x10) (riscv_incr_post pre_x10)


       Fig. 4. Pre- and postconditions and theorems for program in Figure 3.

4     Techniques and Implementation

Our toolchain is implemented in the HolBA library for HOL4, i.e., it is imple-
mented in Standard ML (SML). We summarize the implemented techniques.


4.1   Architecture, lifting, and contracts

HolBA (Figure 5) is built based on the HOL4 theorem prover [12] and the L3
specification language [8] to facilitate analysis of binary code in an architecture-
agnostic manner using BIR. It ensures soundness of the analysis by formally
certifying the transpilation of binary code into BIR, which involves translating
machine code instructions into BIR snippets while preserving their semantics.
This is achieved using a proof-producing transpiler built on HOL4 ISA specifi-
cations that generates (bi)simulation theorems at the transition system level to
ensure that the binary program’s behavior is faithfully mirrored in BIR [18].
    HolBA provides both a HOL4 interface and an SML interface for most op-
erations to facilitate its integration and usage. Its backend provides tools for
symbolic execution, relational analysis, and contract verification, where con-
tracts are Hoare triples—tailored for binary programs with unstructured control
                                 Trustworthy Verification of RISC-V Binaries         7




Fig. 5. Architecture of HolBA, a theorem-prover-based binary analysis platform. The
figure illustrates HolBA’s modular design, highlighting key components.


flows, including those with multiple endpoints—to establish correctness of pro-
grams. HolBA’s weakest precondition generation automates the verification of
loop-free BIR code by deriving verification conditions that can be discharged
using SMT solvers [17]. Symbolic execution complements this by tracking pro-
gram states symbolically to explore execution paths of the given program and
propagation of path conditions [15]. These techniques are tightly integrated with
a Hoare-style logic to modularize rigorous correctness proofs.

4.2   Symbolic execution
In order to automate verification, we rely on forward symbolic execution. Com-
pared to backward techniques, like weakest precondition generation, forward
symbolic execution eases the propagation of constants and precondition con-
straints, enabling pruning of infeasible paths and optimization of context-sensitive
operations. This is especially useful in the context of binary code analysis, where
unstructured code can lead to many potential paths due to indirect jumps, and
unstructured data may lead to memory aliasing. For example, when returning
from a callee function, the caller return address is known and propagated from
the caller function; or when reading from the memory, the latest store operation
can be ignored as the two accesses are disjunct under the path condition.
    Following previous work [15], a symbolic state s̄ consists of a path condition
and a mapping from variables to symbolic expressions, which in turn refer to sym-
bols. An interpretation H maps symbols to values, and we say that a symbolic
state s̄ matches a concrete state s when its evaluation under the interpretation
H renders the path condition true and the mapped variables as the values in
s, written as H(s̄) = s. In order to deal with unstructured binary code, the
symbolic executor relies on the concept of symbolic structures, s̄ →L {s̄1 . . . s̄n },
which denotes that executions encountering only the program labels L and start-
ing from a concrete state that is matched by the initial symbolic state s̄ via an
interpretation, eventually reach a concrete state that is matched by at least one
of the symbolic states {s̄1 . . . s̄n } via the same interpretation.
    The symbolic executor exploits HOL4 meta-programming and consists of two
parts. The first component is a set of formally verified inference rules that al-
8       K. Palmskog et al.

low to establish symbolic structures for individual instructions, compose them
sequentially, do case analyses, prune infeasible states, rename symbols, intro-
duce abbreviations in the path conditions, simplify expressions in the states,
strengthen the path condition of the initial symbolic state, or weaken the path
condition of a final state. The second component is an ML procedure that uses
the inference rules to analyze a complete program fragment. This procedure uses
several heuristics to choose which rules should be applied and how parameters
should be instantiated, e.g. which expressions should be abbreviated, which cases
should be introduced. Furthermore, this process is proof producing, meaning it
uses the HOL4 system to justify the rule soundness theorems it chooses and
composes them to produce the result as theorem. To automatically prove a) in-
feasible path conditions for pruning symbolic states, b) expression simplification
conditions, and c) contractual postcondition entailment for all final states in
the symbolic structure, we produce corresponding conditions using the SMTLIB
standard and check them with an external SMT solver—currently Z3. Finally, we
use the BIR contract and lifter theorems to produce a RISC-V contract theorem.


5     Binary Verification Case Studies

To validate the usefulness of our toolchain and demonstrate that it can be used
to verify real-world binaries, we performed case studies for two high-assurance
system software domains: cryptography and operating systems.


5.1   The ChaCha20 stream cipher

ChaCha20 is a stream cipher that performs twenty rounds of the ChaCha algo-
rithm as defined by Bernstein [1]. We obtained a ChaCha20 binary by compiling
a reference implementation in C using gcc with optimization level -O1, yield-
ing RISC-V disassembly with 847 instructions. Lifting of the dissassembly and
performing symbolic execution on it took a few minutes on a modern machine.
    We focused on specifying and verifying the byte encryption loop body of the
ChaCha20 binary, taking inspiration from similar specifications in HacSpec [2].
More specifically, we define a ChaCha round as a transformation of 16 variables
holding unsigned 32-bit words (array in the source code), which is then used as
input to the next round. Figure 6 shows our definition of a ChaCha quarter round
transforming the state, which we then used as a building block to specify the
byte encryption loop body as a so-called column round followed by a diagonal
round [19]. In the figure, ?? is the HOL4 word XOR operation, <<~ is word left
shift, >>>~ is word right shift, and #<<~ is word rotation to the left.
    Note that our verification of ChaCha byte encryption only establishes the
connection between a high-level functional specification in HOL4 and how the
main loop body of the RISC-V binary behaves according to L3. That is, we did
not prove any non-functional (security) properties of the ChaCha20 binary.
                               Trustworthy Verification of RISC-V Binaries     9

        Definition chacha_line_fst_def:
         chacha_line_fst (pre_a:word32) (pre_b:word32) = pre_a + pre_b
        End
        Definition chacha_line_snd_def:
         chacha_line_snd pre_a pre_d (s:word32) : word32 =
         ((pre_a ?? pre_d) <<~ s) || ((pre_a ?? pre_d) >>>~ (32w - s))
        End (* equivalent to (pre_a ?? pre_d) #<<~ s when s <=+ 31w *)
        Definition chacha_quarter_round_def:
         chacha_quarter_round pre_a pre_b pre_c pre_d =
          let a = pre_a; b = pre_b; c = pre_c; d = pre_d;
          a = chacha_line_fst a b; d = chacha_line_snd a d 16w;
          c = chacha_line_fst c d; b = chacha_line_snd c b 12w;
          a = chacha_line_fst a b; d = chacha_line_snd a d 8w;
          c = chacha_line_fst c d; b = chacha_line_snd c b 7w
          in (a,b,c,d)
        End


         Fig. 6. High-level ChaCha20 quarter round specification in HOL4.


5.2   RISC-V separation kernel

S3K is an open source capability-based separation kernel targeting embedded
RISC-V systems [13]. Practically, S3K manages a collection of user processes
and ensures that they adhere to given restrictions on execution time (slices),
memory access, and interprocess communication. We specified and verified two
key handwritten RISC-V assembly routines from S3K:

trap_entry: Entered when the user process is interrupted or an exeception is
   encountered. Loads a pointer to the process’s process control block (PCB)
   from the special mscratch RISC-V register, then stores the user process’s
   context (general purpose registers) to the PCB.
trap_exit: Entered when the kernel resumes a user process. Loads the user
   process’s context from the PCB (pointed at by register x10), replacing reg-
   ister values with the values from the PCB.

We obtained disassembly for the routines from the S3K author, consisting of
81 instructions that takes less than a minute to lift and symbolically execute.
After adjusting lifting for special RISC-V instructions such as csrrw, we ex-
pressed routine contracts in terms of assignment of registers to memory locations
(trap_entry), and assignments of memory locations to registers (trap_exit);
Figure 7 shows a fragment of the (RISC-V) postcondition of trap_entry. The
S3K author manually validated our specifications, and we then translated them
to BIR manually and performed the verification separately for each routine.


6     Symbolic Execution Evaluation

To investigate the scalability of our proof-producing symbolic execution, we ran
it on a collection of dissassembled RISC-V binaries and measured the running
time; the results are shown in Table 1. To give an indication of the binary size,
10     K. Palmskog et al.

      Definition riscv_kernel_trap_entry_post_def:
      riscv_kernel_trap_entry_post (pre_x1:word64) (pre_mhartid:word64)
      (pre_mscratch:word64) (pre_mepc:word64) (*..*) (m:riscv_state):=
      m.c_gpr m.procID 2w = (* adjusted stack pointer in x2 register *)
       (0xFFFFFFFFFFFFFFFFw * (pre_mhartid <<~ 10w)) + 0x80006400w /\
      riscv_mem_load_dword m.MEM8 (pre_mscratch+8w) = pre_mepc /\
      riscv_mem_load_dword m.MEM8 (pre_mscratch+16w) = pre_x1 (*..*)
      End


      Fig. 7. Fragment of postcondition for trap_entry in S3K disassembly.

         Program #Instr. Description                                Time
         aes-unopt 637 AES cipher, optimization -O0                 67.65s
         aes       264 AES cipher, optimization -O1                 5.52s
         motor     120 motor driver, nested functions and branching 3.71s
         swap       8    swap memory location content               0.19s
         isqrt      15   integer square root                        0.11s
         mod2        4   modulo two                                 0.03s
         incr        4   increment variable                         0.03s

     Table 1. Evaluated programs and their symbolic execution running times.


the table lists the number of RISC-V instructions; this is close to but not the
same as the number instructions symbolically executed, e.g., we often skip ret.
    Per the table, symbolic execution of BIR programs corresponding to disas-
sembly with hundreds of instructions generally takes at most a few minutes. The
running time increases with both the number of BIR statements (corresponding
to ISA instructions) and the “store complexity” of the program. The latter refers
to how much information needs to be stored in the symbolic state during execu-
tion. In many cryptographic routines, all the output bits depend on all the input
bits, yielding a large symbolic state as in AES. In the unoptimized binary, these
expressions are replicated several times in the symbolic memory. Note that AES
is only symbolically executed from initialization until the end of the first round.


7    Conclusions and Future Work

We presented a workflow for verifying RISC-V binaries inside the HOL4 theorem
prover using the HolBA library for binary analysis [4]. The workflow is based
on orchestrating and augmenting previously disparate parts of HolBA, including
lifting of RISC-V machine code to the BIR intermediate language, Hoare-style
binary contracts, and forward symbolic execution of BIR. In particular, we auto-
mated generation of BIR contract theorems from symbolic execution theorems.
     We demonstrated the toolchain on case studies from high-assurance system
software domains, highlighting that binary verification is mainly useful for ensur-
ing that binaries follow high-level behavioral specifications. Future work includes
automated translation of (restricted) RISC-V contracts to BIR contracts, which
may also enable an interface to the toolchain outside of HOL4.
                                 Trustworthy Verification of RISC-V Binaries        11

References

 1. Bernstein, D.J.: Chacha, a variant of Salsa20. In: Workshop Record of SASC, vol.
    8. pp. 3–5 (2008), http://cr.yp.to/chacha/chacha-20080128.pdf
 2. Bhargavan, K., Kiefer, F., Strub, P.Y.: hacspec: Towards verifiable crypto stan-
    dards. In: Security Standardisation Research: 4th International Conference. pp.
    1–20 (2018). https://doi.org/10.1007/978-3-030-04762-7_1
 3. Brumley, D., Jager, I., Avgerinos, T., Schwartz, E.J.: BAP: A binary analysis plat-
    form. In: Computer Aided Verification. pp. 463–469 (2011). https://doi.org/10.
    1007/978-3-642-22110-1_37
 4. Buiras, P., Dong, N., Guanciale, R., Lacroix, T., Lindner, A., Lundberg, D., Ne-
    mati, H., Palmskog, K., Stockmayer, M., Timmerman, J., Tuerk, T., Westerberg,
    A.: Verification of RISC-V binaries using symbolic execution in HolBA (Mar 2025).
    https://doi.org/10.5281/zenodo.15043918
 5. Cao, Q., Beringer, L., Gruetter, S., Dodds, J., Appel, A.W.: VST-Floyd: A separa-
    tion logic tool to verify correctness of C programs. Journal of Automated Reasoning
    61(1), 367–422 (Jun 2018). https://doi.org/10.1007/s10817-018-9457-5
 6. Clutterbuck, D.L., Carré, B.A.: The verification of low-level code. Software Engi-
    neering Journal 3, 97–111(14) (May 1988). https://doi.org/10.1049/sej.1988.0012
 7. Cohen, C., Dénès, M., Mörtberg, A.: Refinements for free! In: Certified Programs
    and Proofs. pp. 147–162. Springer International Publishing, Cham (2013). https:
    //doi.org/10.1007/978-3-319-03545-1_10
 8. Fox, A.: L3: A Specification Language for Instruction Set Architectures, https:
    //acjf3.github.io/l3
 9. Fox, A.: Improved tool support for machine-code decompilation in HOL4. In: In-
    teractive Theorem Proving. pp. 187–202. Springer International Publishing, Cham
    (2015). https://doi.org/10.1007/978-3-319-22102-1_12
10. Goldstine, H.H., von Neumann, J.: Planning and Coding of Problems for an Elec-
    tronic Computing Instrument, Vol. 2 of Report on the Mathematical and Logical
    Aspects of an Electronic Computing Instrument. Tech. rep., U.S. Army Ord. Dept.
    (1947)
11. Guéneau, A., Myreen, M.O., Kumar, R., Norrish, M.: Verified characteristic formu-
    lae for CakeML. In: Programming Languages and Systems. pp. 584–610. Springer,
    Berlin, Heidelberg (2017). https://doi.org/10.1007/978-3-662-54434-1_22
12. HOL development team: HOL interactive theorem prover, https:
    //hol-theorem-prover.org
13. Karlsson, H.A.: S3K: Simply secure separation kernel, https://github.com/
    kth-step/s3k
14. Leroy, X.: Formal verification of a realistic compiler. Commun. ACM 52(7),
    107–115 (Jul 2009). https://doi.org/10.1145/1538788.1538814
15. Lindner, A., Guanciale, R., Dam, M.: Proof-producing symbolic execution for bi-
    nary code verification. CoRR abs/2304.08848 (2023). https://doi.org/10.48550/
    arXiv.2304.08848
16. Lindner, A., Guanciale, R., Metere, R.: TrABin: Trustworthy analyses of binaries.
    Science of Computer Programming 174, 72–89 (2019). https://doi.org/10.1016/j.
    scico.2019.01.001
17. Lundberg, D., Guanciale, R., Lindner, A., Dam, M.: Hoare-style logic for unstruc-
    tured programs. In: Software Engineering and Formal Methods: 18th International
    Conference. pp. 193–213 (2020). https://doi.org/10.1007/978-3-030-58768-0_11
12      K. Palmskog et al.

18. Metere, R., Lindner, A., Guanciale, R.: Sound transpilation from binary to
    machine-independent code. In: Formal Methods: Foundations and Applica-
    tions: 20th Brazilian Symposium. pp. 197–214 (2017). https://doi.org/10.1007/
    978-3-319-70848-5_13
19. Nir, Y., Langley, A.: ChaCha20 and Poly1305 for IETF Protocols. RFC 7539 (May
    2015). https://doi.org/10.17487/RFC7539
20. Sewell, T.A.L., Myreen, M.O., Klein, G.: Translation validation for a verified OS
    kernel. In: Conference on Programming Language Design and Implementation.
    pp. 471–482. Association for Computing Machinery, New York, NY, USA (2013).
    https://doi.org/10.1145/2491956.2462183
21. Slind, K., Norrish, M.: A brief overview of HOL4. In: Theorem Proving in Higher
    Order Logics. pp. 28–32. Springer Berlin Heidelberg, Berlin, Heidelberg (2008).
    https://doi.org/10.1007/978-3-540-71067-7_6
22. Song, D.X., Brumley, D., Yin, H., Caballero, J., Jager, I., Kang, M.G., Liang, Z.,
    Newsome, J., Poosankam, P., Saxena, P.: BitBlaze: A new approach to computer
    security via binary analysis. In: Information Systems Security, 4th International
    Conference. pp. 1–25 (2008). https://doi.org/10.1007/978-3-540-89862-7_1
23. Tan, Y.K., Myreen, M.O., Kumar, R., Fox, A., Owens, S., Norrish, M.: The verified
    CakeML compiler backend. Journal of Functional Programming 29, e2 (2019).
    https://doi.org/10.1017/S0956796818000229
24. Waterman, A., Lee, Y., Patterson, D.A., Asanović, K.: The RISC-V Instruction
    Set Manual, volume I: User-level ISA, version 2.1. Tech. Rep. UCB/EECS-2016-
    118, University of California, Berkeley (May 2016), http://www2.eecs.berkeley.
    edu/Pubs/TechRpts/2016/EECS-2016-118.html
