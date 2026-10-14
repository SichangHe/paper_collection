                                        Circuit-Based Program Verification
                                        Sequential Circuits as an Intermediate Representation for Verifying C Programs

                                        PO-CHUN CHIEN, LMU Munich, Germany
                                        NIAN-ZE LEE∗ , National Taiwan University, Taiwan
                                        ARMIN BIERE, University of Freiburg, Germany
                                        DIRK BEYER, LMU Munich, Germany
                                        Formal verification of software programs and hardware designs shares the common goal of reasoning about state-transition systems,
                                        yet the two communities have largely developed separate intermediate representations, verification algorithms, and tools. This paper
                                        investigates sequential circuits as an alternative intermediate representation for software verification, with the goal of enabling direct
                                        application of hardware-model-checking techniques. We present Circuit-Based Program Verification (CPV), a modular and extensible
                                        framework that translates C programs into sequential circuits and employs off-the-shelf hardware model checkers as verification
                                        backends. Unlike traditional software verifiers, which typically rely on path-based exploration, CPV reasons over sequential circuits,
                                        where a program’s control and data flows are folded into a monolithic transition relation that can be analyzed as a whole. The framework
arXiv:2608.07397v1 [cs.SE] 7 Aug 2026




                                        supports reachability-safety and termination analyses. For reachability safety, programs are encoded as circuits with a bad-state
                                        predicate. For termination, a liveness-to-safety transformation is applied at the circuit level, reducing non-termination detection to a
                                        state-revisit check. CPV integrates a portfolio of state-of-the-art hardware model checkers, together providing access to a diverse
                                        set of verification algorithms, including bounded model checking, k-induction, interpolation-based model checking, and IC3/PDR.
                                        Moreover, CPV further offers different circuit-encoding strategies that capture program behavior relationally or functionally, catering
                                        to different backends. Counterexamples found by hardware model checkers are automatically translated back into software-verification
                                        witnesses for users to interpret verification results. We conducted a comprehensive experimental evaluation on the SV-COMP 2026
                                        benchmark suite, covering more than 16 000 verification tasks. Our results show that CPV achieved competitive performance against
                                        five well-established software verifiers. In particular, CPV exhibited complementary strengths by uniquely solving tasks that other
                                        verifiers cannot handle and solved the second largest number of instances in both reachability-safety and termination benchmark
                                        categories. These results demonstrate that sequential circuits provide a viable intermediate representation for software verification
                                        and that hardware model-checking techniques can be applied effectively with model and witness translation.

                                        CCS Concepts: • Software and its engineering → Formal software verification; Formal methods; • Theory of computation
                                        → Verification by model checking; Program reasoning; • Hardware → Model checking.

                                        Additional Key Words and Phrases: C programs, Sequential circuits, Btor2, Intermediate representation, Verification witnesses

                                        ACM Reference Format:
                                        Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer. 2026. Circuit-Based Program Verification: Sequential Circuits as an
                                        Intermediate Representation for Verifying C Programs. 1, 1 (August 2026), 49 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn
                                        ∗ Also with LMU Munich.


                                        A preliminary version of this work was published in the proceedings of TACAS 2024 [54].
                                        Authors’ Contact Information: Po-Chun Chien, po-chun.chien@sosy.ifi.lmu.de, LMU Munich, Germany; Nian-Ze Lee, nzlee@ntu.edu.tw, National Taiwan
                                        University, Taiwan; Armin Biere, biere@cs.uni-freiburg.de, University of Freiburg, Germany; Dirk Beyer, dirk.beyer@lmu.de, LMU Munich, Germany.




                                        This work is licensed under a Creative Commons Attribution 4.0 International License.
                                        © 2026 Copyright held by the owner/author(s).
                                        Manuscript submitted to ACM


                                        Manuscript submitted to ACM                                                                                                                  1
2                                                             Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


1    Introduction
Formal verification plays an important role in ensuring the reliability of software systems. It is routinely applied to
detect property violations and establish correctness guarantees for safety-critical software. Over the past decades,
the software-verification community has developed a rich ecosystem of verification techniques and tools, including
data-flow analysis [18, 88], predicate abstraction [84, 91, 94], and symbolic execution [50, 96]. In parallel, the community
for hardware model checking has made substantial advances, leading to highly effective algorithms such as bounded
model checking [36, 38, 39], k-induction [122], interpolation-based model checking [106, 128, 129], and IC3/PDR [47, 72].
    Despite sharing the common goal of reasoning about state-transition systems, software verification and hardware
model checking have largely evolved as separate research communities. The two domains rely on different modeling
formalisms, intermediate representations, benchmark suites, and tool ecosystems. Software verifiers typically operate
on program-centric representations such as control-flow automata (CFAs) or static single-assignment form, whereas
hardware model checkers reason about transition systems represented as sequential circuits with parallel execution
semantics. As a consequence, advances in one domain might require substantial technical effort to be transferred to
the other, even when they address rather similar verification problems on an abstract level.
    Several efforts have sought to bridge this gap by translating verification tasks between software and hardware
domains [17, 71, 101, 109, 110, 115, 127] and by adopting verification algorithms across communities [16, 29, 56, 69, 97].
Prior verification approaches based on program-to-circuit translation [71, 101, 115], however, target only bit-level
circuit representations for reachability-safety verification, restricting the scope of problems that can be expressed, and
do not support the backtranslation of verification witnesses. Studies on algorithm transfer require reimplementing
hardware-verification algorithms within a software verifier rather than reusing existing hardware model checkers.
Taken together, these limitations leave the potential of sequential circuits as an intermediate representation for software
verification underexplored. This work seeks to answer the following question: Can sequential circuits serve as a practical
representation for software verification and enable effective application of hardware-model-checking techniques and tools?
    To illustrate, Fig. 1a shows the CFA representation of a simple C program (the corresponding C code is given later in
Fig. 2), where each node and edge represent a program location and a statement, respectively. The function nondet()
models an external program input by returning a nondeterministic value on each call. Figure 1b shows the schematic
structure of the sequential circuit obtained after translation. In the circuit, primary inputs model calls to nondet(), state
registers store the program location and the values of program variables, combinational logic encodes the program’s
execution semantics, and the primary output signals the verification property (e.g., whether the error location 𝑙𝑒𝑟𝑟 can
ever be reached, or whether the termination location 𝑙𝑒𝑛𝑑 is always eventually reached). The control flows and data
updates in a CFA are thus absorbed into the circuit’s next-state functions, producing a monolithic transition-system
representation on which hardware model checkers can operate directly.
    We investigate the proposed circuit-based program-verification methodology by developing CPV, a verifier for C
programs that uses sequential circuits as its intermediate representation. CPV translates programs into word-level
sequential circuits in the Btor2 format [114] and leverages off-the-shelf hardware model checkers, namely ABC [49],
AVR [83], Pono [117], and rIC3 [125], as verification backends. Unlike traditional software verifiers, which typically
explore programs path-by-path, CPV’s backends reason over the circuit as a whole, exploiting the monolithic tran-
sition relation illustrated in Fig. 1b. The framework supports both reachability-safety and termination analyses. To
increase the confidence and interpretability of the verification results, CPV additionally translates hardware-level
counterexamples [114] into standard software-verification witnesses [2, 20], making the overall process certifying [104].

Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                      3




                                        𝑙 init
                                                                   Primary inputs                             Primary output
                                              a = 1;                (nondet() calls)                      (verification property)
                                         𝑙5
                                              b = nondet();

                                         𝑙6                                       Combinational Logic
                                                                                           (program’s
                      [a <= b];                   ![a <= b];
                                                                                       control + data flow)
                             𝑙7                    𝑙 13
               a = nondet();
                                    ![a + b == 5];
                             𝑙8                   return 0;
            b = (b + 1) % 3;
                                                                                           Registers
                             𝑙9                    𝑙 end                                (program location
               [a + b == 5];                                                            and variables 𝑎, 𝑏)

                            𝑙 err                abort();

                                  (a) CFA                                              (b) Sequential circuit


                       Fig. 1. A CFA (a) and the encoded sequential circuit (b) for an example C program


  Altogether, CPV combines several techniques within a unified yet modular verification framework: property-aware
instrumentation, large-block encoding [19] to extract the program’s transition relation, transition-function synthesis to
construct the sequential circuit, portfolio-based hardware model checking, and witness reconstruction.
  In our comprehensive evaluation on over 16 000 verification tasks, we demonstrate the feasibility of the proposed
circuit-based verification methodology. More than 70 % of tasks can be successfully translated into sequential circuits. The
remaining failures were primarily due to implementation limitations in the frontend rather than inherent restrictions of
the approach, suggesting that a more robust program-to-circuit translator is a direction for making circuit-based program
verification even more effective. Subsequent experiments further show that hardware model checkers can effectively
verify the translated circuits. The circuit representation also makes it straightforward to apply transformations such as
liveness-to-safety reduction [37] and logic optimization [108]. When compared against five state-of-the-art software
verifiers, CPV exhibited complementary strengths and solved the second-most instances on both the reachability-
safety and termination benchmark sets. The performance of CPV has also been evaluated in the annual International
Competition on Software Verification (SV-COMP) [33]. CPV first participated in SV-COMP 2024 [54] and has since achieved
strong performance against other participants. For example, in SV-COMP 2025, CPV ranked third in the ReachSafety
category. These results suggest that sequential circuits constitute a viable intermediate representation for software
verification and that the proposed circuit-based verification framework is competitive with established software verifiers.

1.1   Contributions
The novelty of the proposed circuit-based program-verification methodology lies in its unified integration of pro-
gram instrumentation, circuit translation, property encoding, and witness reconstruction around sequential circuits
as an intermediate representation. Its significance stems from complementing existing program-centric intermediate
representations by establishing sequential circuits as a practical alternative, thereby enabling the direct application
                                                                                                               Manuscript submitted to ACM
4                                                                         Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


of state-of-the-art hardware model checkers to software verification. In summary, this work makes the following
contributions:
• We systematically investigate sequential circuits as an alternative intermediate representation for software verification
    and study their potential to bridge software verification and hardware model checking.
• We present CPV, a modular and extensible framework for software verification that translates C programs into
    word-level sequential circuits and reuses off-the-shelf hardware model checkers as verification backends.
• We develop relational and functional circuit-encoding strategies for constructing sequential circuits from a program’s
    transition relation, catering to different model-checking backends.
• We propose program-instrumentation and property-encoding techniques for reachability-safety and termination
    verification, which facilitate a mechanism for reconstructing software-verification witnesses from hardware-model-
    checking results.
• We perform a comprehensive experimental evaluation on the SV-COMP benchmark suite, assessing translation
    feasibility, circuit-encoding strategies, and witness validation.
• We demonstrate that the proposed circuit-based approach is competitive with state-of-the-art software verifiers,
    including CPAchecker [10], Esbmc [131], Kratos2 [85], Symbiotic [4], and Ultimate Automizer [12], while exhibiting
    complementary strengths by solving benchmark tasks that existing approaches struggle to verify.
• We release CPV as open-source software on GitLab1 and archive stable releases on Zenodo [53] to support repro-
    ducibility and long-term availability.
• As a byproduct of this work, we also contribute a large collection of sequential circuits translated from the SV-COMP
    benchmark suite to the Hardware Model Checking Competition (HWMCC) [43],2 enabling future cross-domain
    benchmarking and research.

1.2    Outline
The remainder of this paper is organized as follows. Section 2 reviews related work, covering approaches that bridge
software and hardware verification and intermediate representations used in software verification. Section 3 introduces
the necessary background on control-flow automata, sequential circuits, and the specification of safety and liveness
properties. Section 4 presents the overall architecture of CPV. Section 5 explains the translation of C programs into
sequential circuits. Sections 6 and 7 describe property encoding, program instrumentation, and witness translation for
verifying reachability-safety and termination properties, respectively. Throughout the above technical sections, we use
a running example to illustrate the presented concepts and the translation process. Section 8 covers implementation
details, including the translation pipeline and the integration of hardware model checkers. Section 9 presents the
research questions and discusses the experimental evaluation. Finally, Sect. 10 concludes the paper.

2     Related Work
Our work sits at the intersection of two active research communities, software verification and hardware model checking.
We organize the discussion of related work around four themes: efforts to bridge the two verification communities
through task translation (Sect. 2.1) and algorithm transfer (Sect. 2.2), and common intermediate representations used
in software verification (Sect. 2.3).
1 https://gitlab.com/sosy-lab/software/cpv
2 The translated sequential circuits are available at https://gitlab.com/sosy-lab/research/data/svcomp25-to-btor2. They were derived from the SV-COMP
2025 benchmark set [32] using CPV at 2b20529.
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                           5


2.1   Bridging Hardware and Software Verification Through Translation
Numerous approaches have explored translations between software and hardware representations for verification
and related applications [28]. The most closely related work also employs hardware model checkers as backends for
software verification by translating programs into circuit representations. Long [101], and Noureddine and Zaraket [115]
translated C programs into bit-level sequential circuits in the Aiger format [44]. Both approaches blast arrays into
bit-vectors since Aiger does not natively support arrays, and use ABC [49] as the sole verification backend. Edwards,
Ma, and Damiano [71] translated embedded C programs into logic netlists and verified them using the Ketchum model
checker [92], which primarily relies on automatic test pattern generation to produce assertion-violating test vectors.
Their circuit representation supports arrays, but the approach has limited support for modeling external program inputs.
   Compared with these approaches, our work extends the scope of circuit-based software verification in several respects.
We translate programs into the word-level Btor2 format [114], which natively supports arrays and serves as the standard
format in HWMCC [43], allowing multiple off-the-shelf hardware model checkers to be used as verification backends.
Beyond reachability-safety verification, CPV also supports termination analysis. It can further translate hardware-level
counterexamples into standard software-verification witnesses [2, 20], enabling independently checkable verification
results. In addition, CPV supports floating-point variables and dynamic memory allocation, features not supported by the
previous circuit-based approaches. Finally, whereas previous work evaluated either handcrafted examples [71] or a small
subset of the SV-COMP benchmark suite [101, 115], we conduct a comprehensive experimental evaluation on more than
16 000 benchmark programs using different circuit encodings, hardware model checkers, and verification algorithms.
   A complementary line of work focuses on establishing equivalence between hardware implementations and the
higher-level software specifications. Clarke and Kröning [63] use C programs as reference specifications for hardware
designs and check their equivalence via bounded model checking through exhaustive loop unrolling. Commercial tools
such as Jasper C2RTL3 pursue the same objective in industrial settings. These approaches treat C as a specification
language rather than as the primary verification target, and therefore address a different problem than our work.
   CirC [116] is a compiler framework that lowers high-level languages, including C, to existentially quantified cir-
cuits (EQCs) for applications in cryptographic proof systems. Unlike sequential circuits, EQCs are stateless and admit
nondeterminism through existential quantification. This representation is well suited to CirC’s intended applications
but is less natural for modeling the sequential semantics of imperative programs.
   In the opposite direction, several tools translate hardware circuits into software representations. v2c [109, 110]
translates Verilog circuits into C programs, while Btor2C [17] and Btor2MLIR [127] translate Btor2 circuits into C
programs and LLVM IR, respectively. These tools enable the application of software verifiers to hardware designs.

2.2   Transferring Techniques from Hardware Model Checking to Software Verification
On the algorithmic side, several works have investigated the transfer of verification algorithms from hardware to software.
Bounded model checking (BMC) [36, 38, 39], k-induction [122], interpolation-based model checking [106, 128, 129], and
IC3/PDR [47, 72] were originally developed for verifying hardware systems, where SAT solving plays a central role [45],
and have been adapted and applied to software programs. Today, BMC and k-induction are widely used in software
verification, and many software verifiers employ them as core engines [9, 65, 66]. Interpolation-based methods have
likewise been studied extensively [16, 29, 107]. IC3/PDR has also been adapted to operate on the abstract reachability tree
of an unrolled CFA [56] as well as directly on the CFA itself [97]. These works reimplement hardware-model-checking

3 https://www.cadence.com/en_US/home/tools/system-design-and-verification/formal-and-static-verification/jasper-c-formal-verification.html

                                                                                                                   Manuscript submitted to ACM
6                                                            Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


algorithms within software-verification frameworks by adapting them to operate on program-centric representations.
Our work takes a fundamentally different approach: rather than reimplementing the algorithms, we aim to reuse
hardware model checkers directly by translating programs into sequential circuits. This design choice allows CPV to
benefit immediately from advances in hardware model checking without reimplementing individual algorithms, and
enables a head-to-head comparison of hardware- and software-verification techniques on the same benchmark suite.

2.3    Intermediate Representations for Software Verification
The choice of intermediate representation (IR) is a fundamental design decision in a verification framework, as it
determines both the properties that can be expressed and the algorithms that can be applied. In software verification, a
variety of program-centric IRs have been developed, each targeting a different stage of the verification workflow.
    LLVM IR [98] is primarily used within the LLVM compiler infrastructure, but several verification tools [50, 74, 131]
also build on it. For instance Klee [50] performs symbolic execution on LLVM bitcode, and Esbmc [131] first translates
programs to LLVM IR as a frontend step before lowering them further to its goto-program representation. As a general-
purpose compiler IR, LLVM IR benefits from mature tooling and broad language-frontend support (e.g., via Clang),
but verifiers still need to encode its semantics as logic formulas to reason about it.
    Several language-agnostic verification IRs have also been proposed to decouple language frontends from verification
backends, including Boogie [67], Why3 [75], and Viper [111]. At a lower level, many software verifiers represent
programs as CFAs, in which nodes correspond to program locations and edges represent operations such as assignments
and assumptions. Cbmc [65] and Esbmc [66] use goto programs, while CPAchecker [9] and Ultimate Automizer [90] operate
on their internal CFA representations. Although many verifiers implement their own CFA variant, efforts have been
made to standardize CFA-based IR that can be consumed by multiple tools. For example, K2 [85] and SV-LIB [23] are
two SMT-LIB-like formats for describing imperative programs as CFAs. They inherit the expressions and theories of
SMT-LIB [11] while extending them with constructs for program-specific features such as loops, function calls, and
annotations for loop invariants. CPV uses K2 as a frontend IR before translating programs into sequential circuits.
    These IRs are typically lowered further to representations suitable for automated reasoning. SAT/SMT-based verifiers
commonly unroll the CFA along (syntactically) feasible control-flow paths, rename variables into static single-assignment
form, and encode the resulting verification conditions as SAT or SMT queries. Constrained Horn Clauses (CHCs) [46]
serve as another widely used logical IR. Rather than explicitly exploring execution paths, CHC-based approaches encode
program semantics and properties as a system of Horn clauses, whose satisfiability determines whether the property
holds. CHCs also provide a standardized SMT-LIB-based representation that can be consumed by many CHC solvers.
    Sequential circuits, as employed by CPV, represent another alternative. Here, control flow is encoded using a symbolic
program counter, program variables become state registers, and program execution is captured by next-state functions.
Effectively, the program’s transition behavior over control flow and data update is folded into a monolithic state-
transition system, implicitly representing common program syntactic constructs such as loops or function calls. This
representation enables the direct use of off-the-shelf hardware model checkers as verification backends.

3     Background
This section introduces the necessary background to understand the proposed verification approach. We present
control-flow automata as a representation for modeling imperative software programs (Sect. 3.1.1) and sequential
circuits as the standard representation for hardware transition systems (Sect. 3.1.2). We further describe the formulation
of safety and liveness model-checking problems in the context of each representation (Sect. 3.2) and the corresponding
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                 7


 1    extern unsigned int __VERIFIER_nondet_uint ();
 2    void reach_error () { /* error label */ abort (); }
 3    int main () {
 4      unsigned int a = 1;
 5      unsigned int b = __VERIFIER_nondet_uint ();
 6      while ( a <= b ) {
 7        a = __VERIFIER_nondet_uint ();
 8        b = ( b + 1) % 3;
 9        if ( a + b == 5) {
10          reach_error ();
11        }
12      }
13      return 0;
14    }

                                  Fig. 2. An example C program whose CFA is depicted in Fig. 1a


verification witnesses (Sect. 3.3). Throughout this paper, we use standard logical symbols such as ∧ (conjunction),
∨ (disjunction), and ¬ (negation), along with the temporal operators from linear temporal logic [118], including G
(globally), F (eventually), and U (until).

3.1    State-Transition Systems
Software and hardware systems can be modeled as symbolic state-transition systems. Such a system is defined by an
initial-state predicate Init (𝑋 ) and a transition relation TR(𝑋, 𝐼, 𝑋 ′ ), where 𝑋 is a finite set of state variables, 𝐼 is a finite
set of primary input variables, and 𝑋 ′ denotes the next-state version of 𝑋 . The predicate Init (𝑋 ) specifies the initial
states of the system, while TR(𝑋, 𝐼, 𝑋 ′ ) describes the state transitions under the given input values. Additional invariant
constraints may further restrict the reachable state space. An execution trace (or path) of the system is a sequence of
states, starting from an initial state, in which every two consecutive states are related by TR under some input values.
The two representations introduced in the following differ mainly in how the transition relation is described.

3.1.1 Software Representation: Control-Flow Automaton. We model an imperative program as a control-flow automaton
(CFA). A CFA is a directed graph 𝐴 = (L, 𝑙𝑖𝑛𝑖𝑡 , 𝐺), where L is a finite set of nodes corresponding to program locations,
𝑙𝑖𝑛𝑖𝑡 ∈ L is the initial location (i.e., program entry), and 𝐺 ⊆ (L × Ops × L) is a set of edges. Each edge (𝑙, op, 𝑙 ′ ) ∈ 𝐺 is
annotated with an operation op ∈ Ops, which is either a variable assignment or an assumption (i.e., a Boolean guard).
As we work with C programs, we assume that C operators and data types constitute the operations.
     For verification purposes, we further distinguish two special locations in the CFA: an error location 𝑙𝑒𝑟𝑟 ∈ L, which
represents assertion violations or other program locations that should not be reached, and a termination location
𝑙𝑒𝑛𝑑 ∈ L, which represents program termination (e.g., via return from main(), exit(), or abort()). These locations are
used to encode reachability-safety and termination properties.
     A CFA can be viewed as a transition system whose state variables comprise the program variables together with an
auxiliary program-counter variable 𝑝𝑐 tracking the program location. Its input variables model the nondeterministic
values supplied by the environment, its initial-state predicate constrains 𝑝𝑐 to the program entry location 𝑙𝑖𝑛𝑖𝑡 , and
its transition relation captures the effect of executing CFA edges on both 𝑝𝑐 and the program variables. Under this
interpretation, reaching a program location becomes reaching a state with the corresponding value of 𝑝𝑐. Section 5.1
details the construction used in this work.
                                                                                                          Manuscript submitted to ACM
8                                                                      Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


      Example 1. Consider the example C program in Fig. 2. The program declares two variables a and b, both of type
      unsigned int. It starts by initializing a to 1 (Sect. 3.1.1) and b to a nondeterministic value (Sect. 3.1.1; modeled by
      the return of __VERIFIER_nondet_uint()). Then, the program enters a loop with the condition a <= b, where the
      values of a and b are updated in each iteration.
        The CFA representation of this program is shown in Fig. 1a, where __VERIFIER_nondet_uint() is abbreviated
      as nondet(). Each node corresponds to a program location, and each edge is annotated with the corresponding
      operation. For instance, 𝑙𝑖𝑛𝑖𝑡 corresponds to program entry at Sect. 3.1.1, 𝑙 5 to Sect. 3.1.1, and 𝑙𝑒𝑛𝑑 to the termination
      location after returning from main() at Sect. 3.1.1; the edge from 𝑙𝑖𝑛𝑖𝑡 to 𝑙 5 represents the assignment initializing
      variable a. Assumption edges are marked with square brackets. For example, the edge from 𝑙 6 to 𝑙 7 is an assumption
      edge with guard [a <= b], indicating that the loop body (Sect. 3.1.1) is entered under this condition.


3.1.2 Hardware Representation: Sequential Circuit. A sequential circuit is a special form of a transition system in
which the transition relation can be represented explicitly by next-state functions. For each state variable 𝑥 ∈ 𝑋 ,
there exists a transition function 𝑥 ′ = 𝑓𝑥 (𝑋, 𝐼 ), thus allowing the transition relation to be represented functionally
instead of relationally. Structurally, a sequential circuit consists of registers (state variables), primary inputs, primary
outputs encoding verification properties, and combinational logic that computes the next-state functions and property
outputs. The combinational logic can be represented as a directed acyclic graph, where nodes represent state variables,
input variables, and circuit operations (e.g., bit-vector arithmetic and Boolean connectives), and edges encode the
data dependencies between nodes. The computed next-state values are fed back into the registers, thereby connecting
different time frames and making the overall graph structure cyclic. For a node in the graph, its cone of influence (CoI),
also referred to as its transitive fan-ins, is the subset of variables and operations that can transitively affect its value
through data dependencies, potentially crossing register boundaries.
    In hardware model checking, variables are finite-width and range over bit-vectors and arrays. The underlying logic is
typically quantifier-free bit-vector logic with arrays (QF_ABV), which extends quantifier-free bit-vector logic (QF_BV)
with the array theory [103] to model memories. Common interchange formats for sequential circuits include the
word-level Btor2 format [114] (supporting both QF_ABV and QF_BV) and the bit-level Aiger format [44] (supporting
QF_BV), which can be translated from higher-level hardware description languages such as SystemVerilog [124]. We
follow formal semantics of these logics (QF_BV, QF_ABV) as standardized in SMT-LIB [11].

3.2    Safety and Liveness Properties
After introducing the systems of interest we now continue to describe safety and liveness properties considered in
this work for software verification and hardware model checking.

3.2.1 Software-Verification Properties. We focus on two properties from the C verification track of SV-COMP [33]:
reachability safety (ReachSafety) and Termination. The ReachSafety property4 states that, starting from the program
entry main(), the function reach_error() must never be called during execution. A counterexample is therefore a finite
execution trace from the program entry to a call of reach_error(). The Termination property5 states that every execution
(starting from the program entry main()) must eventually reach a termination point, e.g., upon exit(), abort(), or

4 https://gitlab.com/sosy-lab/benchmarking/sv-benchmarks/-/blob/svcomp26/c/properties/unreach-call.prp
5 https://gitlab.com/sosy-lab/benchmarking/sv-benchmarks/-/blob/svcomp26/c/properties/termination.prp

Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                         9


returning from the call to main(). A counterexample is an infinite execution trace, which can be represented as a lasso,
assuming the state space to be finite, that never reaches a termination point.

3.2.2 Hardware-Model-Checking Properties. We follow the property specification of the Aiger [44] and Btor2 [114]
formats, as adopted by HWMCC [43]. A safety property is encoded using a predicate bad over state and input variables,
monitored by a primary output of the circuit. The predicate bad describes the condition under which the safety
property is violated. A counterexample is an initialized finite execution path satisfying 𝑐 U (𝑐 ∧ 𝑏𝑎𝑑), where 𝑐 denotes
the invariant constraint. Liveness properties are represented using a finite set of justice constraints 𝐽 (also known
as fairness constraints
                   Ó in some   literature). A counterexample to a liveness property is an initialized infinite path
satisfying (G 𝑐) ∧   𝑗 ∈ 𝐽 GF 𝑗 , where 𝑐 denotes the invariant constraint. That is, on this path, the invariant constraint
is always true and each justice constraint 𝑗 ∈ 𝐽 holds infinitely often. Equivalently, if the liveness property holds
(i.e., no counterexample exists), then along every execution path, either 𝑐 eventually becomes false or at least one
𝑗 ∈ 𝐽 eventually becomes false forever. In this work, we consider only a single justice constraint (i.e., |𝐽 | = 1), which
is sufficient for encoding program termination.


3.3   Verification Witnesses
A verifier that reports only a verdict asks its users to trust the verifier itself. Following the paradigm of certifying
algorithms [104], a verifier can instead accompany its verdict with a witness: an independently checkable artifact
that justifies the reported result. The process of checking such a witness, rather than repeating the verification, is
called witness validation. Two kinds of witnesses are commonly distinguished. A correctness witness documents a proof,
typically by exposing the invariants inferred by the verifier, whereas a violation witness describes an execution path
(a counterexample) that violates the property. Both SV-COMP [33] and HWMCC [43] require participating verifiers to
produce witnesses and validate them as part of their competition workflows. As generating and checking correctness
witnesses is an active research area for both software [25] and hardware [77, 78] model checking, including the discussion
of which formats are appropriate, we focus in this article on violation witnesses and leave exploring translation of
correctness witnesses to future work. For the concrete syntax of the violation witness formats, we refer the reader to
the specifications of software-verification witnesses [2, 20, 133] and Btor2 witnesses [114].

3.3.1 Software-Verification Witnesses. For reachability safety, a violation witness for a program with nondeterministic
inputs records the values assigned to those inputs along the error path, each tied to the program location at which it is
consumed. It may additionally constrain the control flow, e.g., by specifying which branch is taken or which value is
returned from a function, and finally identifies the target location at which the property violation occurs. Since the
recorded constraints need not determine every nondeterministic input or branch taken, a witness can represent a set
of execution paths. The witness is considered valid if this set contains at least one path violating the property. If the
witness describes a single execution trace, i.e., all nondeterminism is resolved, it corresponds to a test vector.
  A violation witness for termination is an infinite execution trace represented as a lasso (assuming the program’s
state space is finite). A lasso consists of a finite stem from the program entry to a recurrent location, followed by a
cycle from that location back to itself that can be repeated forever. The witness records the inputs consumed along
both the stem and the cycle and identifies the locations that every represented path must visit infinitely often. It
does not necessarily need to provide a recurrent set of program states. Instead, establishing the recurrence argument
is left to the witness validator [133].
                                                                                                  Manuscript submitted to ACM
10                                                                                 Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


                                                       Large-block                      Transition        Trans.-function   Sequential
            Specification
                                                       encoder [19]                      relation            encoder          circuit



             C program             Instrumentor               C’

                                             (a) Frontend: program instrumentation and encoding


           Sequential                         Hardware model checker                            HWMC            Witness
                                                                                                                            SV witness
             circuit                     (ABC [49], AVR [83], Pono [117], rIC3 [125])           witness        translator


                        Liveness-to-safety
                                                         Circuit’                                                             Verdict
                         transformer [37]

                                             (b) Backend: model checking and witness translation


                 Fig. 3. Verification pipeline of CPV (HWMC: hardware-model-checking; SV: software-verification)



     Two exchange formats are used in SV-COMP [33]. The GraphML-based format (v1) [20] describes violation witnesses
as protocol automata. The YAML-based format (v2) [2, 133] represents violation witnesses as sequences of waypoints,
each consisting of a source location together with an associated constraint.

3.3.2 Hardware-Model-Checking Witnesses. A violation witness for hardware model checking is represented as a
sequence of time frames, each containing the valuations of state variables and the assignments to input variables at the
corresponding time step. In the initial frame, values must be provided for all state variables that are not initialized by
the model. For subsequent frames, state valuations may be omitted, as they can be inferred from the preceding state and
the provided inputs. Don’t-care input values may be omitted as well. Such a witness is essentially a concrete test vector
over time that can be replayed by simulation. For a safety property, the witness describes a finite counterexample trace
from an initial state to a bad state. For a justice property, the infinite counterexample is likewise exported as a finite
lasso-shaped trace consisting of a stem followed by one iteration of the cycle. The successor of the state in the last
time frame, computed from its state and input assignments, is identical to one of the earlier states. Both the Aiger [44]
and Btor2 [114] formats define standardized representations for violation witnesses.

4     Verification Pipeline
The verification pipeline of the proposed circuit-based program-verification framework is depicted in Fig. 3. Its
verification workflow is divided into a frontend and backward stage.

4.1    Frontend (Fig. 3a)
An input C program with a property to be verified (reachability safety or termination) is first instrumented. This
instrumentation is essential both for encoding the verification problem and for enabling witness translation (Sects. 6.2
and 7.3). From the instrumented program, CPV extracts the transition relation using large-block encoding [19] (Sect. 5.1).
The property is encoded as a predicate over the resulting transition system. A subsequent encoding pass extracts
transition functions from the transition relation and constructs a word-level sequential circuit [114] (Sect. 5.2), yielding
a transition-function-based representation.
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                               11


4.2    Backend (Fig. 3b)
Once the frontend produces the sequential circuit, CPV invokes hardware model checkers such as AVR [83] and Pono [117]
to verify it (Sect. 8.2). For liveness properties, in addition to using checkers’ native liveness checking, CPV can apply
a liveness-to-safety transformation [37] prior to verification. If a property violation is detected, the backend model
checker may produce a violation witness [114], that is, a counterexample trace over the translated circuit. This witness
is translated into a software-verification witness [2, 20] for the original program.

4.3    Modularity and Extensibility
CPV is designed with modularity in mind: each component is clearly separated and communicates through standardized
formats for verification artifacts, e.g., Btor2 [114] for circuits and YAML format [2] for software-verification witnesses.
This clean interface makes it easy to add new encoders, alternative circuit representations, or additional backend
model checkers. The result is a flexible framework that can be easily extended and adapted for experimenting with
diverse circuit-based verification techniques.

5     Encoding Programs as Sequential Circuits
We then describe how to encode C programs represented as CFAs into sequential circuits. A CFA is first translated
into a symbolic transition system using large-block encoding (Sect. 5.1), and subsequently encoded as a sequential
circuit (Sect. 5.2) suitable for hardware model checking.

5.1    From CFA to Transition Relation via Large-Block Encoding
Large-block encoding (LBE) [19] is a technique for extracting a transition relation from a CFA by summarizing multiple
CFA edges into a single transition. LBE first identifies maximum loop-free CFA segments (referred to as blocks) and
summarizes the edges within each block into a single transition. That is, in the resulting transition system, all edges
within a block are executed atomically in one step.
    To construct the transition relation, we enumerate all syntactically feasible block-level transitions within the CFA, and
introduce an auxiliary program-counter variable 𝑝𝑐 to encode the program locations corresponding to block entries and
exits. A transition corresponding to a block is then encoded as (𝑝𝑐 = 𝑙 in ∧ 𝑝𝑐 ′ = 𝑙𝑜𝑢𝑡 ) ∧ 𝜑 (𝑌, 𝐼, 𝑌 ′ ), where 𝑙 in and 𝑙𝑜𝑢𝑡 are
the entry and exit locations of the block, respectively, and 𝜑 (𝑌, 𝐼, 𝑌 ′ ) is a quantifier-free first-order formula encoding the
semantics of executing the block. Here, 𝑌 denotes the set of program variables, while 𝐼 denotes the set of input variables
for modeling nondeterministic inputs from the environment (e.g., __VERIFIER_nondet_<type>() in SV-COMP benchmark
tasks). Accordingly, the set of state variables in the transition system is 𝑋 ≜ 𝑌 ∪ {𝑝𝑐}. The transition relation is the
disjunction over all such formulas, and the initial-state predicate is 𝑝𝑐 = 𝑙𝑖𝑛𝑖𝑡 , where 𝑙𝑖𝑛𝑖𝑡 is the program-entry location.
    Instead of encoding every CFA edge as an individual transition step (referred to as single-block encoding in the
literature [19]), LBE reduces the number of transition steps required to represent a program execution. Although
each transition becomes more complex, modern SMT solvers can typically handle the larger formulas efficiently. This
advantage is particularly pronounced for unrolling-based model-checking techniques, as larger blocks allow more
program behavior to be encoded and explored within a single transition step.




                                                                                                         Manuscript submitted to ACM
12                                                               Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


      Example 2. We demonstrate the application of LBE to the CFA in Fig. 1a. The identified blocks have entry and exit
      locations at 𝑙𝑖𝑛𝑖𝑡 , 𝑙 6 , 𝑙 err , and 𝑙 end . The CFA summarized by
      LBE is shown in Fig. 4, where each edge corresponds to a
                                                                                                    𝑙 init
      block-level transition in the original CFA and may contain                     [a <= b];
                                                                                                          a = 1; b = nondet();
      multiple program operations.                                                a = nondet();
                                                                           b = (b + 1) % 3;
         The resulting transition system is encoded by state                                         𝑙6
                                                                                                               ![a <= b];
                                                                                  ![a + b== 5];
      variables 𝑋 ≜ {𝑝𝑐, 𝑎, 𝑏} (where 𝑎 and 𝑏 correspond to                                                     return 0;
      the program variables a and b, respectively), as well as                              [a <= b];
                                                                                        a = nondet();            𝑙 end
      input variables 𝐼 ≜ {nd 5, nd 7 } (modeling return values of
                                                                                     b = (b + 1) % 3;
      nondet() at Sects. 3.1.1 and 3.1.1).
                                                                                        [a + b == 5];             abort();
         The initial-state predicate Init is 𝑝𝑐 = 𝑙𝑖𝑛𝑖𝑡 and the                                     𝑙 err
      transition relation TR(𝑋, 𝐼, 𝑋 ′ ) is the disjunction of the
      following formulas:                                                             Fig. 4. CFA summarized by LBE
          • (𝑝𝑐 = 𝑙𝑖𝑛𝑖𝑡 ∧ 𝑝𝑐 ′ = 𝑙 6 ) ∧ (𝑎 ′ = 1 ∧ 𝑏 ′ = nd 5 )
          • (𝑝𝑐 = 𝑙 6 ∧ 𝑝𝑐 ′ = 𝑙 err ) ∧ (𝑎 ≤ 𝑏 ∧ 𝑎 ′ = nd 7 ∧ 𝑏 ′ = (𝑏 + 1)%3 ∧ nd 7 + ((𝑏 + 1)%3) = 5)
          • (𝑝𝑐 = 𝑙 6 ∧ 𝑝𝑐 ′ = 𝑙 6 ) ∧ (𝑎 ≤ 𝑏 ∧ 𝑎 ′ = nd 7 ∧ 𝑏 ′ = (𝑏 + 1)%3 ∧ nd 7 + ((𝑏 + 1)%3) ≠ 5)
          • (𝑝𝑐 = 𝑙 6 ∧ 𝑝𝑐 ′ = 𝑙 end ) ∧ (𝑎 > 𝑏 ∧ 𝑎 ′ = 𝑎 ∧ 𝑏 ′ = 𝑏)
          • (𝑝𝑐 = 𝑙 err ∧ 𝑝𝑐 ′ = 𝑙 end )

5.2    Constructing Sequential Circuits from Transition Relations
Given a transition relation, we consider two alternative strategies for constructing a sequential circuit. The resulting
circuits differ in how the transition relation is represented: relational encoding treats the transition relation as a constraint
and enforces it through an auxiliary oracle (Sect. 5.2.1), whereas functional encoding derives explicit next-state functions
for each state variable (Sect. 5.2.2). We describe both encoding strategies in the following.

5.2.1 Relational Encoding. Relational encoding utilizes auxiliary variables to represent the next-state valuation. To this
end, we introduce: (1) a fresh Boolean state variable valid, initialized to ⊤, which acts as an oracle tracking whether
the current execution follows the transition relation TR; and (2) for each state variable 𝑥 ∈ 𝑋 , a fresh input variable
𝑥 in simulating the next-state value of 𝑥.
     The resulting circuit contains state variables 𝑋 ∪ {valid} and input variables 𝐼 ∪ 𝑋 in , where 𝑋 in = {𝑥 in | 𝑥 ∈ 𝑋 }.
The initial-state predicate of the circuit is Init (𝑋 ) ∧ valid, where Init (𝑋 ) is the initial-state predicate of the original
transition system. The conjunction ensures that the circuit starts from a valid initial state. The transition functions
are constructed as:

                                              valid ′ ← valid ∧ TR(𝑋, 𝐼, 𝑋 in ), and
                                                  𝑥 ′ ← 𝑥 in , for each 𝑥 ∈ 𝑋 .

     Intuitively, the circuit nondeterministically selects next-state values through the input variables 𝑋 in , while valid
monitors whether the chosen valuation satisfies the transition relation. To ensure that only valid executions are
considered during model checking, the invariant constraint valid is added to the resulting circuit.



Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                   13


    Example 3. We apply relational encoding to the transition relation TR obtained in Example 2. The resulting
    circuit has state variables {𝑝𝑐, 𝑎, 𝑏, valid}, and input variables {nd 5, nd 7, 𝑝𝑐 in, 𝑎 in, 𝑏 in }. The initial-state predicate is
    𝑝𝑐 = 𝑙𝑖𝑛𝑖𝑡 ∧ valid, and the transition functions are:

                                    valid ′ ← valid ∧ TR({𝑝𝑐, 𝑎, 𝑏}, {nd 5, nd 7 }, {𝑝𝑐 in, 𝑎 in, 𝑏 in }),
                                       𝑝𝑐 ′ ← 𝑝𝑐 in,
                                        𝑎 ′ ← 𝑎 in , and
                                        𝑏 ′ ← 𝑏 in .



5.2.2 Functional Encoding. Functional encoding derives next-state functions for each state variable directly from the
transition relation TR. The key idea is to decompose each disjunct in TR into conditions and state updates (recall that TR
is a disjunction of conjunctions of predicates, where each conjunction corresponds to a block-level transition identified
by LBE). A condition is a predicate that only involves current-state and input variables, e.g., 𝑝𝑐 = 𝑙𝑖𝑛𝑖𝑡 or 𝑎 ≤ 𝑏. It
captures the current program location and the guard for entering the next block, such as a loop condition. A state
update is a predicate of the form 𝑥 ′ = 𝑓 (𝑋, 𝐼 ) for some state variable 𝑥 ∈ 𝑋 , e.g., 𝑝𝑐 ′ = 𝑙 6 or 𝑏 ′ = (𝑏 + 1)%3.
  Intuitively, a state update summarizes the net effect of a block on a single variable. Because the execution of a block
is deterministic, i.e., fixing the current-state and input values uniquely determines the successor value of every state
variable, there exists, for every block and every state variable, a function mapping the current state and inputs to the
corresponding next-state value. In practice, the LBE process might need to skolemize the formula by introducing static
single-assignment indices for the state variables to hold the intermediate state values during a block’s execution [22].
The indexed variables can then be resolved recursively by substituting their defining equations, eventually yielding
state-update functions that depend only on the current-state and input variables.
  For each state variable 𝑥 ∈ 𝑋 , the next-state function is obtained by collecting all state updates of 𝑥 and guarding each
update with the conjunction of its corresponding conditions. The resulting function is encoded as a nested if-then-else
expression. Conceptually, it has the form
                                                           
                                                           
                                                           
                                                            𝑓1 (𝑋, 𝐼 ),   if 𝑐 1,
                                                           
                                                            𝑓2 (𝑋, 𝐼 ),   if 𝑐 2,
                                                           
                                                           
                                                           
                                                  𝑥′ ←
                                                           
                                                                           ..
                                                                            .
                                                           
                                                           
                                                           
                                                           
                                                           
                                                                           otherwise,
                                                           
                                                            ∗,
                                                           
                                                           
where ∗ denotes any value or expression, each 𝑓𝑖 (𝑋, 𝐼 ) originates from a state-update predicate and each guard 𝑐𝑖
is the conjunction of the conditions associated with that update. The guards are mutually exclusive because they
correspond to distinct transitions in the CFA.
  To account for the fact that the transition relation extracted via LBE is not right-total (e.g., the termination location
𝑝𝑐 = 𝑙 end has no successor), we introduce a dedicated sink state 𝑙 sink for the program counter. The identified conditions
form the guards of the “if” and “else-if” branches, while the “else” branch corresponds to cases not covered by TR
and thus represents invalid transitions. We handle the “else” branch as follows: for 𝑝𝑐, the next-state value is set
to 𝑙 sink ; for all other state variables, the next-state values can be assigned arbitrarily (e.g., to their current values,
as done in our implementation), since execution beyond the current state is considered invalid, making the exact
                                                                                                             Manuscript submitted to ACM
14                                                                      Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


next-state value irrelevant. Lastly, the invariant constraint 𝑝𝑐 ≠ 𝑙 sink is added to ensure that only valid executions
are considered during model checking.
      Example 4. Applying functional encoding to the transition relation from Example 2 yields the following transition
      functions:

                                      1,         if 𝑝𝑐 = 𝑙𝑖𝑛𝑖𝑡 ,
                                    
                                    
                                    
                                    
                                    
                                                 if 𝑝𝑐 = 𝑙 6 ∧ 𝑎 ≤ 𝑏,
                                    
                                     nd 7,
                                    
                                    
                               𝑎′ ←
                                    
                                    
                                    
                                    
                                     𝑎,         if 𝑝𝑐 = 𝑙 6 ∧ 𝑎 > 𝑏,
                                                 otherwise;
                                    
                                     ∗,
                                    
                                    
                                    

                                      nd 5,             if 𝑝𝑐 = 𝑙𝑖𝑛𝑖𝑡 ,
                                    
                                    
                                    
                                    
                                    
                                     (𝑏 + 1)%3,        if 𝑝𝑐 = 𝑙 6 ∧ 𝑎 ≤ 𝑏,
                                    
                                    
                                    
                               𝑏′ ←
                                    
                                    𝑏,
                                    
                                    
                                                       if 𝑝𝑐 = 𝑙 6 ∧ 𝑎 > 𝑏,
                                                        otherwise;
                                    
                                     ∗,
                                    
                                    
                                    

                                      𝑙 6,       if 𝑝𝑐 = 𝑙𝑖𝑛𝑖𝑡 or 𝑝𝑐 = 𝑙 6 ∧ 𝑎 ≤ 𝑏 ∧ nd 7 + ((𝑏 + 1)%3) ≠ 5,
                                     
                                     
                                     
                                     
                                     
                                                 if 𝑝𝑐 = 𝑙 6 ∧ 𝑎 ≤ 𝑏 ∧ nd 7 + ((𝑏 + 1)%3) = 5,
                                     
                                     𝑙 err ,
                                     
                                     
                              𝑝𝑐 ′ ←
                                     
                                     
                                     
                                     
                                     𝑙 end ,    if 𝑝𝑐 = 𝑙 6 ∧ 𝑎 > 𝑏 or 𝑝𝑐 = 𝑙 err ,
                                                 otherwise.
                                     
                                     
                                     𝑙 sink ,
                                     
                                     
      We merge the cases with the same next-state value for 𝑝𝑐 to simplify the expression above. The initial-state predicate
      remains unchanged as 𝑝𝑐 = 𝑙𝑖𝑛𝑖𝑡 .


5.2.3 Comparison. Relational and functional encoding represent two different ways of constructing sequential circuits
from a transition relation. Relational encoding represents the transition relation as a constraint over current-state,
next-state (simulated by auxiliary inputs 𝑋 in ), and input variables and monitors its validity through an oracle, whereas
functional encoding expresses the next state explicitly as a function of the current state and inputs.
     Relational encoding is more general and can be applied to arbitrary transition relations without requiring a particular
formula structure. For example, the same technique has been used to construct sequential circuits from a nondeterministic
finite automaton for string analysis [130]. This flexibility comes at the cost of introducing auxiliary variables to represent
next-state valuations and validity checks. Consequently, the generated circuits may be more difficult to verify, as the
additional variables enlarge the search space.
     Functional encoding, in contrast, relies on a specific characteristic of the transition relation by requiring that the
execution of each block is deterministic. This assumption ensures that state updates admit a functional expression
over the current-state and input variables, and is guaranteed by the transition relation induced by the CFA model.
Because next-state functions are derived directly, no auxiliary next-state variables are required, resulting in more
compact circuits. Moreover, exposing the transition structure through explicit next-state functions allows more room
for logic simplification and enables functional substitution during circuit unrolling, which propagates state information
across time frames and simplifies the resulting SAT/SMT formulas. Such simplifications can be performed during
preprocessing by SMT solvers such as Boolector [114] and Bitwuzla [112] through variable and term substitution. Hence,
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                        15


                                                                       𝑝𝑐 = 𝑙 init   𝑝𝑐 ≠ 𝑙 end                𝑝𝑐 ≠ 𝑙 end
                                                                                                      ...

                                                                                                  𝑝𝑐 ≠ 𝑙 end                𝑝𝑐 ≠ 𝑙 end
        𝑝𝑐 = 𝑙 init                         𝑝𝑐 = 𝑙 err
                              ...
                                                                                                                  ...
                                                                                                               𝑝𝑐 ≠ 𝑙 end


       (a) Finite counterexample to reachability safety               (b) Infinite, lasso-shaped counterexample to termination


                      Fig. 5. Counterexample structures for reachability-safety (a) and termination (b) properties




functional encoding is often considered more amenable to SAT/SMT-based reasoning than relational encoding, as
shown by previous studies in the context of bounded model checking [95, 121]. In practice, however, the effectiveness
of either encoding also depends on the verification algorithm employed by the backend model checker, as demonstrated
in our evaluation (Sect. 9).


6     Verifying Reachability Safety
In this section, we describe how reachability-safety properties are encoded in the sequential circuits (Sect. 6.1), and how
we instrument the program to facilitate the extraction of software-verification witnesses from hardware model-checking
results (Sect. 6.2).


6.1    Encoding Reachability-Safety Property
In SV-COMP [33], error locations in C programs are annotated with calls to the function reach_error(), and later assigned
to a designated program-counter value 𝑙 err during translation. The reachability-safety property states that error locations
are unreachable from the program entry and can therefore be encoded by asserting that the program counter never
equals 𝑙 err , captured by the bad-state predicate bad ≜ (𝑝𝑐 = 𝑙 err ).
    Given a translated circuit and a safety property, a hardware model checker automatically determines whether the
property holds. If the property is violated, the model checker produces a violation witness (counterexample), namely a
trace in the translated circuit that reaches a bad state from an initial state while satisfying all invariant constraints, as
illustrated in Fig. 5a. Such a trace corresponds to a program execution path that starts from the initial location and
reaches an error location. Section 6.2 will describe how an error trace can be reconstructed from a hardware-model-
checking witness. Conversely, if the safety property holds, no valid execution path of either the original program or the
translated circuit reaches an error location or bad state, respectively. Some hardware model checkers can additionally
produce a correctness witness, often in the form of an inductive invariant overapproximating the set of reachable states,
as a proof of safety. However, current support for exporting correctness witnesses is less mature and less uniform
than that for violation witnesses in hardware model checkers. Recent editions of HWMCC have taken steps toward
standardizing them [79]. In principle, an inductive invariant for the circuit could also be translated back into loop
invariants in the original program, but CPV currently does not support this translation.
                                                                                                                  Manuscript submitted to ACM
16                                                           Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


 1    extern unsigned int __VERIFIER_nondet_uint ();
 2    unsigned int __cpv_nondet_uint_5 () { // added by CPV
 3      static unsigned char __cpv_nondet_count_5 = 0;
 4      __cpv_nondet_count_5 = __cpv_nondet_count_5 + 1;
 5      return __VERIFIER_nondet_uint ();
 6    }
 7    unsigned int __cpv_nondet_uint_7 () { // added by CPV
 8      static unsigned char __cpv_nondet_count_7 = 0;
 9      __cpv_nondet_count_7 = __cpv_nondet_count_7 + 1;
10      return __VERIFIER_nondet_uint ();
11    }
12    void reach_error () { /* error label */ abort (); }
13    int main () {
14      unsigned int a = 1;
15      unsigned int b = __cpv_nondet_uint_5 (); // originally at line 5
16      while ( a <= b ) {
17        a = __cpv_nondet_uint_7 (); // originally at line 7
18        b = ( b + 1) % 3;
19        if ( a + b == 5) {
20          reach_error ();
21        }
22      }
23      return 0;
24    }

                                  Fig. 6. Instrumented C program for reachability analysis



6.2    Program Instrumentation and Error-Trace Reconstruction
Large-block encoding folds program statements at different locations into a single transition-system step. As a result, a
violation witness produced by a hardware model checker may contain values for input variables that are not actually
relevant to the property violation. For instance, when transitioning from 𝑙 init to 𝑙 6 in Fig. 1a, the return value of
__VERIFIER_nondet_uint() at Sect. 3.1.1 (encoded as input variable 𝑛𝑑 7 in the circuit) does not affect the transition.
Nevertheless, a hardware model checker is not able to distinguish the relevant and irrelevant input values and may
assign an arbitrary value to 𝑛𝑑 7 in the witness. Such values cannot be mapped back to the original program when
reconstructing an error trace.
     To easily identify the nondeterministic inputs that are actually consumed along a property-violating execution
path, we instrument each __VERIFIER_nondet_<type>() call with a dedicated counter whose value changes after every
invocation. These counters are translated into state variables in the resulting sequential circuit and are therefore
observable in the hardware-model-checking witness. A change in a counter value between two consecutive time
steps indicates that the corresponding nondeterministic input has been consumed during that transition. Furthermore,
the source location of each __VERIFIER_nondet_<type>() call can be encoded in the corresponding counter’s variable
name (e.g., using its line and column numbers), as illustrated in Example 5. Given a hardware violation witness, we
reconstruct the corresponding software error trace by tracking changes in the counters and extracting the associated
input values. The recovered inputs are then mapped back to the program locations containing the corresponding
__VERIFIER_nondet_<type>() calls. This allows us to discard irrelevant input assignments introduced by the hardware
model checker and produce a witness that reflects the execution of the original program.
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                             17


  The instrumentation further improves the modularity of the verification pipeline. Without it, witness reconstruction
would require additional metadata (communicated through a separate artifact) from the task translator, such as
mappings between circuit input variables and the CFA transitions that consume them, as well as the corresponding
source-code locations. By exposing the consumption of nondeterministic inputs through counters encoded directly
in the circuit, all information required for witness reconstruction becomes part of the verification task itself. As a
result, the witness translator can recover both the relevant input values and their source-code locations directly from
the hardware-model-checking witness, allowing it to operate independently of the task translator and keeping the
overall architecture modular.
    Example 5. We demonstrate the instrumentation technique using the example program in Fig. 2. The two calls
    to __VERIFIER_nondet_uint() are instrumented with counters __cpv_nondet_count_5 and __cpv_nondet_count_7,
    as shown in Fig. 6. The suffixes _5 and _7 denote the line numbers of the calls in the original program before
    instrumentation. For brevity, column numbers are omitted from the counter names shown here. Both counters are
    of type unsigned char and are initialized to 0. As we only need to observe whether a counter value changes, the
    potential overflow is not a concern. Using an unsigned type also avoids the undefined behavior associated with
    signed-integer overflow in C.
      After translation, we obtain a sequential circuit similar to those in the previous examples, with two additional state
    variables, ndcnt 5 and ndcnt 7 , corresponding to the inserted counters. The bad-state predicate is bad ≜ (𝑝𝑐 = 𝑙 err ),
    where 𝑙 err is the program-counter value assigned to the error location.
      A violation witness produced by the hardware model checker is summarized in the following table (“-” denotes a
    don’t-care value):


                                                             State                           Input
                             Time step
                                          𝑝𝑐      𝑎      𝑏           ndcnt 5   ndcnt 7     𝑛𝑑 5       𝑛𝑑 7

                                0        𝑙 init   -            -          0         0    UINT_MAX        -
                                1           𝑙6    1   UINT_MAX            1         0             -     5
                                2        𝑙 err    5           0           1         1             -      -


    The input values to be extracted are highlighted in bold. The value 𝑛𝑑 5 = UINT_MAX at time step 0 is relevant because
    ndcnt 5 changes from 0 to 1 between time steps 0 and 1. Similarly, we take the value 𝑛𝑑 7 = 5 at time step 1 because
    ndcnt 7 changes from 0 to 1 between time steps 1 and 2.
      Mapping these values back to the corresponding nondeterministic calls in the original program yields the
    following error trace:
       (1) enter main();
       (2) __VERIFIER_nondet_uint() returns UINT_MAX at Sect. 3.1.1;
       (3) enter the while loop at Sect. 3.1.1;
       (4) __VERIFIER_nondet_uint() returns 5 at Sect. 3.1.1;
       (5) reach_error() is called at Sect. 3.1.1.




                                                                                                       Manuscript submitted to ACM
18                                                                              Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


7     Verifying Program Termination
Here we explain how termination properties are encoded in the translated circuits (Sect. 7.1), how the resulting liveness
properties can be reduced to safety properties (Sect. 7.2), and how non-termination witnesses can be extracted from
hardware model-checking results (Sect. 7.3).

7.1    Encoding Termination Property
During translation, program-termination locations are assigned a designated program-counter value 𝑙 end . The ter-
mination property requires that every execution starting from the program entry eventually reaches a termination
location. Accordingly, we encode the property using a justice constraint defined as 𝑗 ≜ (𝑝𝑐 ≠ 𝑙 end ). Note, however,
that requiring 𝑝𝑐 ≠ 𝑙 end to hold only infinitely often in a counterexample is not strong enough. We must additionally
enforce that 𝑝𝑐 ≠ 𝑙 end is true at every step. Therefore, an invariant constraint 𝑝𝑐 ≠ 𝑙 end is added in conjunction with
the invariant constraint introduced during circuit encoding in Sect. 5.2.6
     Recall the semantics of justice constraints from Sect. 3.2.2. A counterexample is an infinite initialized execution
in the shape of a lasso, consisting of a finite prefix (the stem) leading to a cycle that can be traversed indefinitely, as
illustrated in Fig. 5b. Along this execution, 𝑝𝑐 ≠ 𝑙 end holds always (and thus infinitely often). The cycle portion of
the lasso represents a recurring program behavior that prevents the execution from reaching a termination location.
Thus, such a counterexample corresponds directly to a non-terminating execution of the original program. If no
counterexample exists, i.e., the termination property holds, then all executions of the original program eventually
reach a termination location.

7.2    Liveness-to-Safety Transformation
Since many hardware model checkers do not support liveness properties directly, we apply a standard liveness-to-
safety (L2S) transformation [37]. The general L2S transformation supports multiple justice constraints. In our setting,
however, only a single justice constraint is present, and it is already implied by the invariant constraint introduced
above. Consequently, the transformation can be simplified to checking whether a previously encountered state can
be revisited in the transition system.
     The L2S transformation introduces a Boolean input variable save and a Boolean state variable saved. In addition, for
each state variable 𝑥, a corresponding recording state variable 𝑥𝑟 of the same sort is introduced. The input variable save
acts as an oracle and may become ⊤ at any time step. The state variable saved is initialized to ⊥ and records whether
save has been triggered previously. Its transition function is saved ′ ← save ∨ saved. When save is triggered for the
first time, i.e., when 𝑠𝑎𝑣𝑒 ∧ ¬𝑠𝑎𝑣𝑒𝑑 holds, the recording state variables capture the current state. Thus, the transition
function of each recording state variable is defined as: 𝑥𝑟′ ← ite(save ∧ ¬saved, 𝑥, 𝑥𝑟 ). All remaining state variables are
updated according to their original transition functions, unchanged by the L2S transformation. A state revisit is then
detected by the predicate saved ∧ 𝑥 ∈𝑋 (𝑥 = 𝑥𝑟 ), which checks whether the current state matches the previously saved
                                 Ó

state. The transformed safety property is obtained by treating this predicate as the bad-state condition.
     A model checker that supports safety properties can then be used to verify the transformed circuit and property.
Besides the verification verdict, model checkers may also produce witnesses. Similar to Sect. 6, a violation witness and
a correctness witness for the transformed circuit can be translated back to a non-terminating lasso and a transition
invariant [120] for the original program, respectively. The witness translator in CPV currently supports translating

6 Since the justice constraint is implied by the invariant constraint, it can technically be omitted (i.e., set to ⊤). We retain it here for clarity.

Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                              19


violation witnesses (further described in Sect. 7.3), whereas translation of correctness witnesses [25, 78] as discussed
already in Sect. 3.3 is left for future work.
   We can further optimize the L2S transformation by excluding from the state-revisit check the auxiliary counter
variables introduced during program instrumentation for witness reconstruction (see Sect. 7.3). These variables serve
solely for bookkeeping purposes and do not influence program execution or termination, and can therefore be safely
omitted. More generally, under functional encoding, any state variable that is not contained in the cone of influence of
the justice and invariant constraints (including the instrumented counters) does not need to be included in the state
comparison. This CoI-based optimization, however, only works for functional encoding, since in relational encoding,
all state variables appear in the transition function of the state variable valid. Hence, CoI analysis cannot identify
irrelevant variables and only the instrumented counter variables can be reliably omitted.
   The optimization is particularly beneficial for the instrumented counters. With counters included in the state-revisit
check, the execution would need to revisit not only the same program state but also the same counter values. The
counters are typically set to increase by a certain value upon each invocation. Re-obtaining the same values may require
many additional transitions until wrap-around (due to overflow) occurs. As a result, the lasso-shaped witness produced
by the model checker may become substantially longer, making the verification problem unnecessarily harder. The
effectiveness of this optimization is confirmed by the evaluation results presented later in Sect. 9 (RQ3.1).

7.3    Program Instrumentation and Non-Termination Witness Extraction
As in Sect. 6.2, we instrument each __VERIFIER_nondet_<type>() call with a counter to identify the input values relevant
to a non-terminating execution.
   Moreover, in order to determine which loop is responsible for non-termination, one could inspect the program-
counter value 𝑝𝑐 at which a state saving or revisit occurs in the witness produced by the model checker and map it back
to the corresponding program location. Nevertheless, this requires understanding how program locations are encoded in
the circuit, which may vary across encoders (e.g., one-hot or binary encoding). One could for example store an explicit
mapping between circuit-level 𝑝𝑐 encodings and program locations as an auxiliary artifact produced by the encoder, and
use it during witness translation. To reduce coupling between the circuit encoder and the witness translator, we instead
introduce a dedicated counter for each loop in the program, whose value changes at the beginning of the loop body.
These counters are encoded as state variables in the resulting sequential circuit. As with the nondeterministic-input
counters, the source location of each loop can be encoded in the corresponding counter variable’s name.
   Given a violation witness produced by the hardware model checker, relevant input values can be recovered by tracking
changes in the nondeterministic-input counters. Similarly, the loop responsible for non-termination can be identified
via the loop counter that changes at the time the state saving occurs, or equivalently, via the 𝑝𝑐 value at that point.
      Example 6. In Fig. 7, we illustrate the instrumentation on the example program from Fig. 2. As in Example 5,
      the two __VERIFIER_nondet_uint() calls are instrumented with counters to track the consumption of their return
      values. In addition, a counter __cpv_loop_count_6 is introduced for the while loop at Sect. 3.1.1 to monitor loop
      entries. The counter is declared as a global variable, initialized to 0, and incremented at the beginning of the loop
      body.7 Its name encodes the source location of the while loop in the original program.



7 In CPV’s implementation, “&&   ((__cpv_loop_count_<id> = __cpv_loop_count_<id> + 1) || 1)” is appended to the original loop con-
dition, which is equivalent to incrementing the counter at the beginning of the loop body.
                                                                                                        Manuscript submitted to ACM
20                                                               Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


 1   extern unsigned int __VERIFIER_nondet_uint ();
 2   unsigned int __cpv_nondet_uint_5 () { ... }    // added by CPV
 3   unsigned int __cpv_nondet_uint_7 () { ... }    // added by CPV
 4   unsigned char __cpv_loop_count_6 = 0;          // added by CPV
 5   void reach_error () { /* error label */ abort (); }
 6   int main () {
 7     unsigned int a = 1;
 8     unsigned int b = __cpv_nondet_uint_5 ();
 9     while ( a <= b ) {                                // originally at line 6
10       __cpv_loop_count_6 = __cpv_loop_count_6 + 1; // added by CPV
11       a = __cpv_nondet_uint_7 ();
12       b = ( b + 1) % 3;
13       if ( a + b == 5) {
14         reach_error ();
15       }
16     }
17     return 0;
18   }

                                    Fig. 7. Instrumented C program for termination analysis


       After going through the translation pipeline, we obtain a sequential circuit similar to that in Example 5, with
     one additional state variable, loopcnt 6 , corresponding to the inserted loop counter. The L2S transformation is then
     applied to the circuit. For illustration, we assume the functional encoding from Example 4, though the transformation
     itself is independent of the encoding choice and applies also to circuits under relational encoding. L2S introduces
     state variables saved, 𝑎𝑟 , 𝑏𝑟 , and 𝑝𝑐𝑟 (the latter three for recording a previously visited program state), together with
     an input variable save. The liveness property is thereby reduced to checking whether saved ∧ (𝑝𝑐 = 𝑝𝑐𝑟 ) ∧ (𝑎 =
     𝑎𝑟 ) ∧ (𝑏 = 𝑏𝑟 ) can ever become ⊤ while satisfying the invariant constraint (𝑝𝑐 ≠ 𝑙 end ∧ 𝑝𝑐 ≠ 𝑙𝑠𝑖𝑛𝑘 ).
       An example violation witness for the transformed problem is shown below (“-” denotes a don’t-care value). For
     simplicity, we omit the recording state variables (𝑎𝑟 , 𝑏𝑟 , and 𝑝𝑐𝑟 ) from the table.


                                                              State                                  Input
                      Time step
                                    𝑝𝑐      𝑎   𝑏   ndcnt 5    ndcnt 7    loopcnt 6   saved   nd 5   nd 7    save

                              0    𝑙 init   -   -        0            0          0        0     1       -      0
                              1       𝒍6    1   1        1            0          0        0      -     1       1
                              2       𝑙6    1   2        1            1          1        1      -     0        -
                              3       𝑙6    0   0        1            2          2        1      -     1        -
                              4       𝒍6    1   1        1            3          3        1      -      -       -


       From the above witness, observe that the values of 𝑝𝑐, 𝑎, and 𝑏 at time step 1 are identical to those at time step 4,
     indicating a state revisit and thus the cycle portion of the lasso-shaped counterexample. These values are captured
     by the corresponding recording variables from time step 2 onward, and are subsequently used to detect the revisit
     condition at time step 4. The while loop at Sect. 3.1.1 is entered repeatedly between time steps 1 and 4, as evidenced


Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                          21


      by the 𝑝𝑐’s value and the increasing value of the loop counter loopcnt 6 . The state-saving event occurs at time step 1,
      when save is triggered for the first time. At the same time, loopcnt 6 increases from time step 1 to 2, marking the
      transition from the stem to the cycle in the lasso-shaped counterexample and indicating that this while loop is
      responsible for the non-terminating behavior. The same procedure described in Sect. 6.2 can be used to recover the
      return values of the __VERIFIER_nondet_uint() calls.
        After extracting the relevant input values and mapping them back to the original program, we reconstruct the
      non-termination witness as follows:
         (1) enter main();
         (2) __VERIFIER_nondet_uint() returns 1 at Sect. 3.1.1;
         (3) enter the while loop at Sect. 3.1.1 with program state a = 1 and b = 1;
         (4) __VERIFIER_nondet_uint() returns 1 at Sect. 3.1.1;
         (5) enter the while loop at Sect. 3.1.1 again with a = 1 and b = 2;
         (6) __VERIFIER_nondet_uint() returns 0 at Sect. 3.1.1;
         (7) enter the while loop at Sect. 3.1.1 again with a = 0 and b = 0;
         (8) __VERIFIER_nondet_uint() returns 1 at Sect. 3.1.1;
         (9) enter the while loop at Sect. 3.1.1 again with the same state as in step (3), namely a = 1 and b = 1 (state
             revisit occurs).


8     Implementation
The previous sections presented the concepts and workflow of circuit-based program verification. In this section, we
describe how they are implemented in CPV.
    CPV orchestrates the execution of the various components involved in the verification workflow. This orchestration
layer is implemented in Python, with individual components either invoked as subprocesses or integrated as libraries.
The implementation builds upon several external components, including Kratos2 [85] for frontend parsing and parts of
the program-to-circuit translation (Sect. 8.1), CoVeriTeam [27] for invoking backend hardware model checkers (Sect. 8.2),
and the hardware model checkers themselves for verifying the translated circuits. Details on the witness translator
(Sect. 8.3) and the portfolios used in SV-COMP and in our evaluation (Sect. 8.4) are also provided.


8.1    C-to-Btor2 Encoding
Depending on the verification task, CPV first instruments the input program to facilitate witness translation and property
encoding. We then use Kratos2 [85] for large-block encoding. Kratos2 parses the C program and translates it into K2,
an intermediate verification language that essentially represents the program’s control-flow automaton in textual
form. Given a program entry and a target function, it applies large-block encoding and introduces a symbolic program
counter to obtain a state-transition system, from which the corresponding 𝑝𝑐 values for the program entry and target
location can be obtained. For reachability-safety verification, this workflow can be applied directly, as the program entry
is typically main(), and, in the SV-COMP setting, the target error function is reach_error(). For termination analysis,
however, a program may terminate through multiple exit points, which cannot necessarily be represented by a single
target function. Since Kratos2 supports only one target function, CPV instruments the program with a fresh function label
__cpv_reach_exit() and uses it as the target. Calls to __cpv_reach_exit() are inserted immediately before every program
exit point except returning from main(), including calls to exit() and abort(). To handle termination through main(), a
                                                                                                    Manuscript submitted to ACM
22                                                                            Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


wrapper function __cpv_main() is introduced, which invokes the original main() first and then calls __cpv_reach_exit().
As a result, all program exits are redirected to a single target location represented by __cpv_reach_exit(), and the
wrapper function __cpv_main() serves as the new program entry for Kratos2.
     We use Btor2 [114] to represent the translated circuit because it is the prevailing format for hardware model checking
and is supported by many tools participating in HWMCC [43]. Relational encoding is implemented by Kratos2, which can
translate K2 programs directly into Btor2 circuits. For functional encoding, K2 is first encoded into a VMT-LIB transition
system [58, 61] by Kratos2 and then to Btor2 using our functional encoder. The functional encoder is implemented in
Python and uses PyVMT [81] and PySMT [80] for manipulating transition systems and SMT formulas. Two encoding
options for the program-counter variable 𝑝𝑐 are provided by the functional encoder: one-hot encoding, which uses 𝑛
bits for 𝑛 program locations, and binary encoding, which uses ⌈log2 (𝑛)⌉ bits (relational encoding in Kratos2 currently
supports only binary encoding of 𝑝𝑐). Although one-hot encoding requires more state registers, it often yields simpler
next-state logic and, consequently, more compact circuits in terms of overall gate count [52, 87]. One-hot encoding is
also argued to provide more fine-grained splitting opportunities for SAT/SMT solvers resulting in more specific learned
clauses and thus faster solving. In our case, since the number of program locations is typically small compared with the
program state space, which is dominated by the program’s data variables, the choice has little effect on the resulting
circuits. For reachability-safety verification, the generated circuit contains a bad signal asserting that 𝑝𝑐 is equal to the
program-counter value assigned to the target error function. For termination, the generated circuit contains a justice
constraint corresponding to the termination encoding described in Sect. 7. The L2S transformer in CPV takes a Btor2
circuit containing a justice constraint as input and produces a Btor2 circuit containing a bad property as output.
     During the translation to Btor2, primitive data types, including integers, floating-point numbers, and pointers, in
the input program are encoded using fixed-size bit-vectors. Floating-point values can be encoded by blasting them into
bit-vectors, which is supported by the relational encoding implemented in Kratos2. Our functional encoder currently
does not support this word-blasting procedure. Static arrays are naturally represented as Btor2 arrays. Heap memory
is modeled in K2 (and hence in Btor2) as a large global array, and pointer dereferences are translated into reads from
and writes to this array, which are subsequently encoded as Btor2 array operations. Since Btor2 represents transition
systems in QF_ABV, all input and state variables must range over finite domains. This requirement is naturally satisfied
by fixed-width machine types and the finite address space used to model heap memory. Several language features
remain only partially supported. For instance, support for library functions is limited and programs relying on functions
from libraries such as math.h may fail during the C-to-K2 translation stage. The capabilities and limitations of the
frontend translation are evaluated and discussed in Sect. 9 (RQ1). Function calls are inlined during large-block encoding.
Recursive functions are only partially supported, as CPV currently relies on Kratos2 to perform bounded unrolling with
a user-specified recursion depth,8 and support for concurrent programs is currently beyond the scope of CPV.
     While developing CPV, we uncovered several issues in Kratos2 related to the translation pipeline. We contributed
fixes and reported the issues to the development team of Kratos2. All identified problems have since been resolved,
improving the robustness of the underlying infrastructure used by CPV.

8.2    Integration of Hardware Model Checkers
CPV currently integrates four hardware model checkers: ABC [49], AVR [83], rIC3 [125], and Pono [117]. Together,
these tools provide access to a diverse set of verification algorithms, including bounded model checking (BMC) [38],

8 A possible alternative would be to encode the call stack explicitly as an array in the translated circuit, although this approach has not yet been explored.

Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                        23


𝑘-induction [122], IC3/PDR [47, 72] and its variants such as IC3IA [59] and IC3SA [82], as well as interpolation-based
model checking [106, 128, 129]. Depending on the selected model checker and engine, reasoning is performed using
SAT solvers such as MiniSat [73], CaDiCaL [40], GipSAT [126], and Kissat [41], or SMT solvers such as MathSAT5 [60],
Boolector [114], Bitwuzla [112], and Yices2 [70].
   The integrated model checkers differ in their input-language support and witness-export capabilities. While AVR,
rIC3, and Pono natively support Btor2, ABC operates on the bit-level Aiger format [44]. When using ABC, CPV invokes
Btor2Aiger [113] to bit-blast the Btor2 circuit into Aiger prior to verification, and the export of violation witnesses
in Btor2 format is thus not supported. Furthermore, ABC and rIC3 only support QF_BV and therefore cannot handle
sequential circuits involving arrays (QF_ABV).
   The execution of hardware model checkers is orchestrated through CoVeriTeam [27], a library for cooperative
verification. CoVeriTeam provides a uniform interface for invoking different verification backends and reuses the mature
execution infrastructure of the benchmarking framework BenchExec [31]. In particular, it assembles command lines
to run the backend model checkers, configures isolated containerized environments and enforces resource limits via
runexec, collects witnesses and verification results, and parses tool outputs using the so-called tool-info modules9 from
BenchExec. This design makes it straightforward to integrate additional hardware model checkers into CPV in the future,
as developers only need to provide the executable of the new verification backend and implement a tool-info module.

8.3   Witness Translation
When a hardware model checker reports a property violation, CPV translates the generated hardware-model-checking
witness into a software-verification witness. As a first step, CPV invokes BtorSim [113], a simulator for Btor2 circuits and
the official validator for violation witnesses in HWMCC [43]. This serves two purposes. First, it independently validates
the violation witness produced by the model checker. Second, it generates a complete simulation trace containing
the values of all state and input variables at every time step. This information is necessary because hardware model
checkers typically export only input assignments in a violation witness. The witness translator then analyzes the
simulation trace and identifies value changes in the counters introduced during program instrumentation. From these
changes, it determines the input values relevant to the violation and reconstructs the corresponding software-level
execution trace, as described in Sects. 6.2 and 7.3. The reconstructed witness can be exported in the GraphML-based
witness format (v1) [20] or the YAML-based witness format (v2) [2, 133].
   Translation of correctness witnesses is not yet implemented. At present, among the integrated hardware model
checkers, only rIC3 [125] is able to export correctness witnesses or inductive invariants in a standardized Btor2-based
format. Therefore, when a property is proven, CPV currently emits an empty trivial witness artifact.

8.4   Sequential Portfolios in SV-COMP
We devise sequential portfolios of hardware model checkers for CPV to participate in SV-COMP, which are also used in
the evaluation in Sect. 9. In the competition, the resource limits are 15 min of CPU time and 15 GB of memory [33]. Due
to the tight memory bound, we adopt sequential portfolios that distribute the available time budget across multiple
model-checking engines instead of running them in parallel.
   We organize the portfolios along two orthogonal dimensions: (1) the verification property (ReachSafety vs. Termi-
nation) and (2) the underlying theory that the translated circuit depends on (QF_BV vs. QF_ABV). This yields four

9 https://github.com/sosy-lab/benchexec/blob/main/doc/tool-integration.md

                                                                                                  Manuscript submitted to ACM
24                                                                 Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


                                                               Property
                                    ReachSafety                                     Termination

                               Theory                                                          Theory
                 QF_BV                        QF_ABV                            QF_BV                         QF_ABV


              rIC3 · IC3                Pono · 𝑘-ind. (w/ CEGAR)              rIC3 · IC3                Pono · 𝑘-ind. (w/ CEGAR)
                 200 s                            200 s                          200 s                            300 s

            AVR · IC3SA                      AVR · IC3SA                    AVR · IC3SA                      AVR · IC3SA
               200 s                            200 s                          200 s                            300 s

             ABC · IMC                       Pono · IC3SA                   Pono · IC3IA                  Pono · k-induction
               200 s                            200 s                          200 s                         remaining

          Pono · k-induction              Pono · k-induction              Pono · k-induction
             remaining                       remaining                       remaining


Fig. 8. Sequential portfolios used in CPV’s SV-COMP configuration, each consisting of a sequence of hardware model-checking engines
(denoted as <tool>·<engine> with an associated time budget), selected based on the verification property and whether the translated
circuit contains arrays




configurations, each with its own schedule. To construct each portfolio, we benchmark individual engines on a sampled
subset of verification tasks from SV-COMP 2025, and iteratively build a greedy selection that maximizes the number
of solved instances. The resulting schedules are then manually refined to account for complementary strengths of
different verification techniques and to mitigate overfitting to the benchmark set. The final portfolios are shown in
Fig. 8. Since ABC and rIC3 do not support QF_ABV, they are not included in the portfolios for tasks involving arrays.
Furthermore, given that ABC cannot export violation witnesses in Btor2 format, we select only one ABC engine for
the portfolios, where it is primarily used for proving safety properties.
     In addition to backend engines, the portfolio also includes alternative translation strategies, such as functional
and relational encodings, as well as variants with and without program slicing in the CFA-to-TR translation. These
strategies form additional layers above the backend engine portfolios and are applied sequentially in the order in
which they are mentioned.


9     Evaluation
We conducted a large-scale and comprehensive evaluation of CPV on the SV-COMP benchmark set [33] to demonstrate
the feasibility and effectiveness of the proposed circuit-based program-verification approach. This section first presents
the research questions (Sect. 9.1) and the experimental setup (Sect. 9.2), then answers each research question with
detailed results and analyses (Sect. 9.3), and concludes with a discussion of potential threats to validity (Sect. 9.4).


9.1    Research Questions
Our evaluation follows the structure of CPV’s verification pipeline (Sect. 4). We first study the feasibility of translating C
programs into sequential circuits (RQ1), and then examine how different circuit-encoding choices affect the resulting
circuits and the performance of downstream model checking (RQ2). We further investigate CPV’s liveness-to-safety
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                             25


transformation, evaluating both its internal design choices and how it compares to an alternative source-level trans-
former (RQ3). Moving to the backend, we assess the quality of the violation witnesses exported by CPV (RQ4). Finally,
we evaluate CPV end-to-end against state-of-the-art software verifiers on the SV-COMP benchmark suite (RQ5).
   Concretely, we aim to answer the following research questions:
RQ1: Can a significant portion of SV-COMP benchmark tasks be encoded as sequential circuits? (answer)
RQ2: What are the effects of different circuit-encoding choices (relational vs. functional)?
      2.1: How does the encoding affect the effectiveness of hardware model checkers? (answer)
      2.2: How does encoding affect the resulting circuit size and verification run time? (answer)
      2.3: What is the impact of sequential logic optimization on circuits under different encodings? (answer)
RQ3: What are the effects of optimizations and implementation choices in CPV’s L2S transformer?
      3.1: Does eliminating instrumented variables during L2S significantly improve CPV’s effectiveness? (answer)
      3.2: How does CPV’s L2S transformation compare to another source-level L2S transformer, TransVer? (answer)
RQ4: How many violation witnesses produced by CPV can be validated? (answer)
RQ5: How does CPV compare with state-of-the-art software verifiers on the SV-COMP benchmark set?
      5.1: How does CPV perform on ReachSafety benchmark tasks? (answer)
      5.2: How does CPV perform on Termination benchmark tasks? (answer)

9.2    Experimental Setup
We describe the experimental setup as follows.

9.2.1 Benchmark set. We used the benchmark set from SV-COMP 2026 [33, 34]. Each verification task consists of a C
program, a property (specification), and an expected verdict indicating whether the property holds or is violated.
   The evaluation focuses on the categories ReachSafety and Termination, which correspond to the classes of properties
currently supported by CPV. All programs in these categories are single-threaded. Programs containing recursive
functions are excluded, as recursion is not supported by CPV. After filtering, the ReachSafety category contains 14 208
tasks, and the Termination category contains 1 993 tasks. Table 1 (column “#Tasks”) summarizes the number of tasks
in each subcategory of the benchmark set.

9.2.2 Evaluated Tools. CPV version 1.1 [55] was used in the evaluation. It is bundled with the following hardware
model checkers as backends: ABC [49] at commit 474e7fb, AVR [83] at commit 82af52e (from a forked repository;
with some modifications for easier result parsing), Pono [117] at commit f7e3a6c, and rIC3 [125] version 1.5.1. CPV
utilizes Btor2Aiger to bit-blast Btor2 circuits into Aiger format for ABC, and BtorSim to simulate witnesses in order to
reconstruct full counterexample traces. Both tools are compiled from Btor2Tools at commit d33c73f.
   For RQ3.2, TransVer [26] at commit a8dfc6b was used for comparison.
   For RQ4, violation witnesses produced by CPV were validated using CPAchecker [30] version 4.2.2 [35] and Witch [7]
at commit ffc643d [8]. Both tools support the v2 witness format and were among the top two participants in the C
Validation track for the categories ReachSafety and Termination of SV-COMP 2026 [33]. For validation of v1 witnesses,
the same version of CPAchecker and Symbiotic-Witch [5], the predecessor of Witch, at commit 43ee4b7 [6] were used.10
   For RQ5, we compared CPV with several software verifiers. These include the leading tools from SV-COMP 2026 [33],
evaluated in the versions and configurations used in the competition [14]: CPAchecker [9, 10] version 4.2.2 [35],
10 Symbiotic-Witch and Witch support only v1 and v2 witness formats, respectively, whereas CPAchecker supports both.

                                                                                                                       Manuscript submitted to ACM
26                                                           Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


Esbmc [66, 131] version 7.11 [100], Symbiotic [4, 123] at commit 9866754 [3], and Ultimate Automizer [12, 90] at commit
00d4337 [68]. We selected these verifiers based on their strong performance in SV-COMP 2026. In particular, UAutomizer
ranked first overall in the C verification track and second in the Termination category, while CPAchecker, Esbmc, and
Symbiotic achieved the top three positions in the ReachSafety category. CPAchecker also ranked second overall in the C
verification track. Moreover, since CPV relies on Kratos2 in its frontend, we evaluated Kratos2 version 2.3 in combination
with the wrapper script provided in the reproduction artifact for its CAV 2023 paper [85, 86].
     The evaluated verifiers cover a broad range of verification techniques, including configurable program analysis [24],
counterexample-guided abstraction refinement [64], bounded model checking [38], k-induction [21, 69], interpolation-
based model checking [16, 29], symbolic execution [96], automata-based methods [90], and predicate abstraction [91],
reflecting both the diversity and the state of the art in software verification.

9.2.3 Benchmarking Environment. All experiments were performed on a cluster of machines running Ubuntu 24.04 (64
bit), each equipped with a 3.4 GHz Intel Xeon E3-1230 v5 CPU (8 processing units) and 33 GB of RAM. The exper-
imental environment used Python 3.12 and pycparser 2.21. For each benchmark task, 900 s of CPU time, 15 GB of
memory, and 2 CPU cores were allocated. We employed BenchExec [31] and BenchCloud [15] to ensure reliable and
scalable benchmarking.

9.3    Answers to Research Questions
In this section, we present the experiments conducted for each research question, along with the corresponding results,
analyses, and discussions. Throughout, proofs and alarms produced by a verifier refer to correct results confirming
that the specified property holds and that the property is violated, respectively. A brief summary is highlighted in
a blue box at the end of each RQ.

RQ1: Translating C Verification Tasks to Sequential Circuits. To assess the feasibility of encoding C verification tasks as
sequential circuits, we translated the ReachSafety and Termination benchmark tasks into Btor2 circuits using CPV’s
translation pipeline under both relational and functional encodings (Sect. 5.2). Since CPV’s frontend largely relies on
Kratos2, which first represents C programs as CFAs in K2 IR, the number of tasks successfully translated into K2 CFAs
was also recorded. Table 1 summarizes the translation results, showing that a substantial portion of the benchmark
tasks can be successfully translated into both K2 CFAs and Btor2 circuits under both encodings.
     Translation from C to K2 was largely possible, with over 80 % of all benchmark tasks successfully encoded as K2
CFAs. Some subcategories exhibited lower success rates. In ReachSafety-ControlFlow, most failures involved the use
of longjmp(), which is currently unsupported. In ReachSafety-Floats, a portion of failures arose from unsupported
floating-point library functions such as sin(), ceil(), fmod(), and floor(). In subcategories such as ReachSafety-Heap,
ReachSafety-Sequentialized, and Termination-MainHeap, as well as parts of ReachSafety-Floats, failures were caused
by limitations of pycparser or unsupported non-constant initializers in array declarations in Kratos2. These limitations
will be addressed in future work by contributing patches to Kratos2 and pycparser, as well as extending CPV’s frontend,
as already demonstrated in Sect. 8.1.
     In subcategories such as Arrays, BitVectors, Hardware, and Loops in ReachSafety, and BitVectors and MainControlFlow
in Termination, over 90 % of tasks were successfully translated into Btor2 circuits under both encodings. For relational
encoding, a drop in success rate was observed in some subcategories. In ReachSafety-ECA, approximately 200 tasks
failed due to out-of-memory errors. In ReachSafety-Floats and ReachSafety-Heap, Kratos2 encountered internal errors
when encoding program semantics as SMT formulas using MathSAT5. In ReachSafety-ProductLines, failures arose from
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                               27

                      Table 1. Summary of SV-COMP benchmark tasks translated into K2 CFAs and Btor2 circuits


                                                                       CFA (K2)            Relational (Btor2)          Functional (Btor2)
                       Category                       #Tasks
                                                                     #           %            #             %             #               %
                           Arrays                         440         438      99.5           432        98.2             421        95.7
                           BitVectors                      48          48     100              48       100                48       100
                           Combinations                   671         636      94.8           636        94.8             110        16.4
                           ControlFlow                     73          35      47.9            33        45.2              33        45.2
                           ECA                          1 263       1 252      99.1         1 050        83.1             784        62.1
                           Floats                       1 400         321      22.9           233        16.6              10         0.714
                           Hardness                     6 789       6 525      96.1         6 079        89.5             742        10.9
       ReachSafety
                           Hardware                     1 224       1 182      96.6         1 181        96.5           1 167        95.3
                           Heap                           237          78      32.9            53        22.4              53        22.4
                           Loops                          762         753      98.8           742        97.4             713        93.6
                           ProductLines                   597         597     100             419        70.2             419        70.2
                           Sequentialized                 585         245      41.9           217        37.1             183        31.3
                           XCSP                           119         119     100             119       100                98        82.4
                           Overall                    14 208      12 229       86.1        11 242        79.1           4 781            33.7
                           BitVectors                      34          32      94.1            32        94.1              32            94.1
                           MainControlFlow                253         243      96.0           243        96.0             242            95.7
       Termination         MainHeap                       180           0       0               0         0                 0             0
                           Other                        1 526       1 391      91.2         1 166        76.4           1 080            70.8
                           Overall                      1 993       1 666      83.6         1 441        72.3           1 354            67.9



unsupported encodings of pointers to constant string literals. The subcategory Termination-Other shares programs
with ReachSafety-Floats and ReachSafety-ProductLines and thus exhibits similar issues.
   For functional encoding, failures mirrored those of relational encoding, as both share the same large-block encoding
component.11 Additionally, the current functional encoding does not support floating-point data types, contributing to
lower success rates in subcategories such as ReachSafety-Combinations, ReachSafety-Floats, and ReachSafety-Hardness.
In ReachSafety-ECA and other subcategories, some failures were caused by reaching Python’s recursion limit when
traversing SMT formula trees. We note that this limitation stems from the current implementation rather than the
encoding technique itself. Future versions of CPV will address this issue, for example, by adopting an iterative traversal
of SMT formulas.
   The median translation time for ReachSafety tasks was 2.62 s for relational encoding and 2.88 s for functional encoding.
For Termination tasks, the median translation time was 2.50 s and 2.53 s, respectively (computed over successfully
translated tasks). Profiling revealed that importing Python libraries (including CoVeriTeam, NetworkX, PySMT, and PyVMT)
took approximately 2.2 s per run on our machines. This is because the benchmarking environment did not include all
required Python dependencies. To simplify deployment across the cluster, these packages were bundled with CPV and
imported via Python wheel files, which introduced a small startup overhead. When installed locally, the import time
can be significantly reduced. Nevertheless, given the per-task time limit of 900 s, the translation overhead remained
modest and was not a bottleneck in the overall verification pipeline, leaving sufficient time for model checking.

11 The relational encoder is more developed. All tasks translated by the functional encoder can also be handled by the relational one.

                                                                                                                         Manuscript submitted to ACM
28                                                                        Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


     Overall, translating C programs into sequential circuits is feasible. Although the frontend of CPV (via Kratos2) is
not as mature as those of long-established software verifiers, CPV nevertheless achieves remarkable effectiveness in
end-to-end verification, as further demonstrated in RQ5.1 and RQ5.2.

     A large portion (over 70 %) of 16 201 evaluated benchmark tasks can be successfully translated into sequential
     circuits. The translation overhead is low relative to the overall time budget, leaving sufficient resources for
     model checking. The remaining limitations are primarily due to implementation constraints in the frontend (e.g.,
     unsupported floating-point library functions) rather than inherent restrictions of the proposed approach.

RQ2.1: Encoding’s effect on Model-Checking Effectiveness. To study the impact of different encoding choices on model
checkers’ effectiveness, the four primary backend tools (ABC, AVR, Pono, and rIC3) in CPV were evaluated on Btor2
circuits generated under relational and functional encodings. We focused on the subset of benchmark tasks that can be
successfully translated into Btor2 circuits under both encodings. To reduce computation time while maintaining a
representative sample across subcategories, up to 150 tasks were randomly sampled from each ReachSafety subcategory,
with a balance between tasks with and without property violations, resulting in a total of 1 402 tasks for the category
ReachSafety. For Termination, all 1 354 tasks that were successfully translated under both encodings were considered,
as the total number is manageable. Since some model-checking engines only support bit-vector sorts without arrays,
we further identified 1 167 ReachSafety tasks and 1 241 Termination tasks that do not contain arrays.
     Table 2 summarizes the results of each model-checking engine on the sampled subsets, including bit-vector-only (Ta-
ble 2a) and array-manipulating tasks (Table 2b), under both relational and functional encodings. Figure 9 further
visualizes the results using cactus plots.12 A data point (𝑥, 𝑦) in the plots indicates that the respective engine correctly
solved 𝑥 tasks under the encoding shown in the legend, each within 𝑦 seconds of CPU time. In the cactus plots, results
for ReachSafety and Termination are combined.
     The results show that most model-checking engines favor the functional encoding over the relational one in terms
of the number of solved tasks, with improvements in both the number of proofs and alarms. The cactus plots further
indicate that many engines require less CPU time to solve the same number of tasks under functional encoding. There
are a few exceptions, though. ABC’s IMC engine performed slightly better on tasks using relational encoding, and Pono’s
IMC engine showed little to no difference between the two encodings. In contrast, ABC’s PDR, rIC3’s IC3, and Pono’s
IC3IA demonstrated clear improvements with functional encoding, whereas AVR’s IC3SA did not exhibit such a trend.
     These differences may be attributed to factors beyond the encoding itself, such as the implementation of the engines,
their internal representations of transition systems, and the underlying SAT/SMT solvers. We have submitted the
translated Btor2 circuits to HWMCC [42, 43] and encourage the developers of the model checkers to further investigate
the performance differences. In summary, the results suggest that offering different encoding choices in CPV is valuable,
as this caters to different model-checking engines.

     The evaluation shows that encoding choices have a noticeable impact on model-checking performance, with
     functional encoding generally yielding better results in terms of the number of tasks solved and run time.
     However, the effect is not uniform across all engines, and some tools perform similarly or even slightly better
     with relational encoding. These results highlight the value of offering multiple encoding options in CPV to better
     accommodate different model-checking backends.

12 We use a slightly modified cactus plot in which time is plotted on the 𝑦 -axis, following common practice in the SV-COMP community.

Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                              29

       Table 2. Results for hardware model checkers on translated Btor2 tasks under relational and functional encodings

                                                   (a) On bit-vector-only tasks

              HWMC                                   ReachSafety (1 167)                       Termination (1 241)
                               Results
       Tool       Config.                     Relational    Functional      Δ (%)    Relational     Functional       Δ (%)
                               #Solved             868            866      −0.23             979         950         −3.0
                   IMC           proofs            444            444       0                249         250          0.40
                                 alarms            424            422      −0.47             730         700         −4.1
       ABC
                               #Solved             696            794       14               611         674         10
                   PDR           proofs            412            433        5.1              65         109         68
                                 alarms            284            361       27               546         565          3.5
                               #Solved             798            892       12               893         935          4.7
                    IC3          proofs            445            492       11               208         241         16
                                 alarms            353            400       13               685         694          1.3
       rIC3
                               #Solved             746            833       12               796         944       19
               k-induction       proofs            332            404       22                68         217      220
                                 alarms            414            429        3.6             728         727       −0.14
                               #Solved             781            800        2.4             855         853         −0.23
       Pono        IMC           proofs            417            432        3.6             223         224          0.45
                                 alarms            364            368        1.1             632         629         −0.47

                                         (b) On tasks with both array and bit-vector sorts

              HWMC                                   ReachSafety (1 402)                       Termination (1 354)
                               Results
       Tool       Config.                     Relational    Functional      Δ (%)    Relational     Functional       Δ (%)
                               #Solved             857            852      −0.58             859         903          5.1
                  IC3SA          proofs            469            483       3.0              216         218          0.93
                                 alarms            388            369      −4.9              643         685          6.5
       AVR
                               #Solved             844            868        2.8             828         842          1.7
               k-induction       proofs            358            362        1.1             110         112          1.8
                                 alarms            486            506        4.1             718         730          1.7
                               #Solved             678            750       11               755         767          1.6
                  IC3IA          proofs            388            424        9.3             162         158         −2.5
                                 alarms            290            326       12               593         609          2.7
       Pono
                               #Solved             861            914        6.2         1 015         1 014         −0.099
               k-induction       proofs            363            405       12             312           317          1.6
                                 alarms            498            509        2.2           703           697         −0.85



RQ2.2: Encoding’s effect on Circuit Size and Run Time. In light of the performance differences observed between relational
and functional encodings in RQ2.1, we further analyzed the resulting circuit sizes under both encodings. ABC was
chosen as the subject of study because it provides circuit statistics such as the number of gates (AIG nodes).
  Figure 10a compares the number of gates in circuits translated from the same C verification task under relational and
functional encodings. A data point (𝑥, 𝑦) in the scatter plots indicates that the circuit generated under relational encoding
has 𝑥 gates while the one under functional encoding has 𝑦 gates. The color of a data point denotes the task category. A
                                                                                                        Manuscript submitted to ACM
30                                                                                Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer

  103                                                                                103
                   IMC · rel.                                                                  IC3SA · rel.
  102              IMC · func.                                                       102       IC3SA · func.
                   PDR · rel.                                                                  𝑘-ind. · rel.
                   PDR · func.                                                                 𝑘-ind. · func.
  101                                                                                101
                   scPDR · rel.
                   scPDR · func.
  100                                                                                100


 10−1                                                                               10−1


 10−2                                                                               10−2
        0                 500               1 000         1 500        2 000               0         500            1 000            1 500         2 000

                                       (a) ABC                                                                   (b) AVR
  103                                                                                103
                   IC3IA · rel.                                                                IC3 · rel.
  102              IC3IA · func.                                                     102       IC3 · func.
                   IMC · rel.                                                                  𝑘-ind. · rel.
  101              IMC. · func.                                                      101       𝑘-ind. · func.
                   𝑘-ind. · rel.
  100              𝑘-ind. · func.                                                    100


                                                                                    10−1
 10−1

                                                                                    10−2
 10−2
        0                 500               1 000         1 500        2 000               0         500            1 000            1 500         2 000

                                       (c) Pono                                                                  (d) rIC3


Fig. 9. Cactus plots comparing model-checking engines on Btor2 tasks translated from the SV-COMP benchmark set under relational
and functional encodings (𝑥: n-th fastest correct result; 𝑦: CPU time (s))


            107                                              103                                       103
                        ReachSafety                                 ReachSafety                                  ReachSafety
                        Termination                                 Termination                                  Termination


                                                             101                                       101
            104



                                                            10−1                                     10−1
            101
                  101                 104           107             10−1            101        103               10−1          101           103
                    (a) Circuit size (#gates)                      (b) IMC’s run time (s)                       (c) PDR’s run time (s)


Fig. 10. Scatter plots comparing circuit size and verification run time of ABC under relational (𝑥) and functional (𝑦) encodings (gray
lines indicate equal performance and one order-of-magnitude differences)



point below the diagonal corresponds to an instance where functional encoding yields a smaller circuit, and vice versa.
We observe that functional encoding generally resulted in smaller circuits than relational encoding, with some cases
demonstrating an order-of-magnitude reduction in the number of gates. In addition, Table 3 reports the median circuit
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                        31

Table 3. Summary of median circuit size and ABC’s run time under relational and functional encodings on ReachSafety (a) and
Termination (b) tasks, as well as the number of tasks where each encoding yielded better results

                                                  (a) On ReachSafety tasks

                           Circuit size (1 167 tasks)   IMC (857 comm. solved)     PDR (681 comm. solved)
             Encoding
                           Med. #gate     #smaller      Med. time       #faster    Med. time       #faster
             Relational      21 897             97         0.342             400       0.661          245
             Functional      13 758          1 070         0.379             457       0.233          436

                                                  (b) On Termination tasks

                           Circuit size (1 241 tasks)   IMC (947 comm. solved)     PDR (559 comm. solved)
             Encoding
                           Med. #gate     #smaller      Med. time       #faster    Med. time       #faster
             Relational      10 801             28         0.347             218       1.93            82
             Functional       8 396          1 212         0.223             729       0.377          477




sizes under both encodings, as well as the number of tasks for which each encoding yielded a more compact circuit
when applied to the same benchmark task. Functional encoding achieved smaller median sizes for both benchmark
categories, and produced smaller circuits in 91.7 % and 97.7 % of the ReachSafety and Termination tasks, respectively.
  We next compare the run time of ABC’s IMC and PDR engines on tasks solved under both encodings in Figs. 10c
and 10b, and Table 3. For IMC, functional encoding led to an increase in the median run time on the 857 commonly solved
ReachSafety tasks, despite solving a larger number of tasks in shorter CPU time (see Table 3a). On the 947 commonly
solved Termination tasks (see Table 3b), IMC exhibited slightly better run-time efficiency under functional encoding.
However, recall that IMC solved more tasks under relational encoding when considering all evaluated benchmark tasks
across both categories (see Table 2a). On the other hand, ABC’s PDR demonstrated a clearer efficiency advantage for
circuits generated by functional encoding. As illustrated in Fig. 10b, many data points lie below the diagonal, with
some showing order-of-magnitude improvements. The median verification run time was also lower under functional
encoding for both categories. On the commonly solved tasks, PDR was faster under functional encoding in 64.0 % and
85.3 % of the ReachSafety and Termination tasks, respectively. These observations are consistent with RQ2.1: ABC’s
PDR shows a clear preference for functional encoding, whereas IMC exhibits more mixed behavior.
  From the collected experimental results, we observe a positive correlation between circuit size and the run time of
both ABC’s engines. However, circuit size (and run time) is influenced not only by the encoding but also by the intrinsic
complexity of the original C verification task, for which no standard quantitative metric exists. Moreover, structural
differences introduced by the encoding may affect solver performance independently of circuit size. In summary, while
functional encoding can often produce more compact circuits, the performance improvements in subsequent verification
runs are not uniform across different backend engines.


   Functional encoding generally produces smaller circuits than relational encoding. From the analysis of ABC’s
   results, we observe that its PDR engine performs more efficiently on circuits generated by functional encoding,
   whereas its IMC engine shows less difference in run time between the two encodings.

                                                                                                  Manuscript submitted to ACM
32                                                                                      Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer

                                                                                  10 849
                             9 871                                                         9 521
             10 000                                                   10 000
                                                                                                      8 606
                                     6 835           6 784
                                                                                                                                  𝑥: Encoding
              5 000                                                    5 000                                                   𝑦: Median #gates
                                                                                                                                   w/o scorr
                                                                                                              636.5                w/ scorr
                                                               0
                 0                                                        0
                             Relational              Functional                       Relational      Functional

                              (a) ReachSafety                                          (b) Termination


Fig. 11. Bar charts comparing the median number of gates of the encoded circuits with and without scorr for commonly solved
ReachSafety (a) and Termination (b) tasks, under relational and functional encodings


                                                                                       3.47

        3                                                             3
                                                                                                                                     𝑥: Encoding
                      2.13
        2                                                             2        1.81                                               𝑦: Median time (s)
                                                                                              1.34                                            PDR
        1                                                             1                                                                scorr+ PDR
             0.520
                              0.330
                                             0.100
                                                     0.290                                           0.270 0.170                      (scorr+)PDR
                                                             0.0100                                                   0.0200
        0                                                             0
                Relational                      Functional                        Relational             Functional

                        (a) ReachSafety                                                   (b) Termination


Fig. 12. Bar charts comparing the median run time of different PDR configurations of ABC for commonly solved ReachSafety (a) and
Termination (b) tasks, under relational and functional encodings (“(scorr+)PDR” denotes the run time of PDR subsequent to scorr)



RQ2.3: Combined Effect of Encoding and Circuit Optimization. In RQ2.1 and RQ2.2, we observe that ABC’s PDR engine
was more effective and efficient on circuits generated by functional encoding. This raises an interesting research
question of whether circuit optimization can further improve PDR’s performance and whether its effects differ between
the two encodings. We continue to use ABC as the primary subject of study, as it implements several powerful sequential
logic optimization techniques such as speculative reduction [108] (referred to as scorr in ABC). We applied scorr
before running PDR and compared the results to those of PDR alone. The time limit and measurements included
both optimization and verification phases.
     Figures 11 and 12 compare the median number of gates and the run time of ABC’s PDR engine on commonly solved
tasks across all evaluated configurations (encoding and circuit optimization). In Table 4, the mean values and the
corresponding reduction rates are reported. The number of solved tasks is further listed in Table 5. The run time
reported here is measured internally by ABC, which provides separate timings for scorr and PDR, rather than the overall
CPU time measured by BenchExec in the other RQs. For reference, the cactus plot in Fig. 9a also includes the combined
configuration running both scorr and PDR (denoted as “scPDR”), showing its performance across all sampled tasks.
     From Fig. 11 and Table 4, we see that scorr reduced the number of gates for circuits under both encodings, with a
more pronounced reduction for functional encoding. Notably, 356 ReachSafety tasks under functional encoding were
reduced to zero gates after applying scorr (more than half of the 647 considered tasks), which explains the median
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                33

Table 4. Summary of run time and gate counts for ABC’s PDR engine on commonly solved tasks, across different encodings and
with/without scorr (reduction rates are computed from the corresponding mean values; “(sc.+)PDR” denotes the run time of PDR
subsequent to scorr)


    Category                                         Run time (s)                                   #Gates
                 Enc.       Config.
    (#tasks)                            Median       Geo. mean      Reduct. (%)     Median      Arith. mean        Reduct. (%)
                                PDR        0.520         0.830       (baseline)      9 871        25 580             (baseline)
                 Rel.      sc.+ PDR        2.13          3.65       −340
                                                                                     6 835        18 581              27.4
     Reach.               (sc.+)PDR        0.330         0.471        43.2
      (647)                     PDR        0.100         0.201        75.8           6 784        21 834              14.6
                 Func.     sc.+ PDR        0.290         0.693        16.5
                                                                                        0          5 012.2            80.4
                          (sc.+)PDR        0.0100        0.0333       96.0
                                PDR        1.81          1.48        (baseline)     10 849        17 705             (baseline)
                 Rel.      sc.+ PDR        3.47          2.87        −93.5
                                                                                     9 521        11 285              36.3
      Term.               (sc.+)PDR        1.34          1.30         12.4
      (542)
                                PDR        0.270         0.369        75.2           8 606        15 123              14.6
                 Func.     sc.+ PDR        0.170         0.310        79.1
                                                                                      636.5        2 742.5            84.5
                          (sc.+)PDR        0.0200        0.0279       98.1

                 Table 5. Results for ABC’s PDR engine with and without sequential logic optimization (scorr)


               Category                               Relational                             Functional
                             Results
               (#tasks)
                                          w/o scorr     w/ scorr      Δ (%)       w/o scorr     w/ scorr      Δ (%)
                             #Solved           696           682     −2.0             794           856        7.8
              ReachSafety
                               proofs          412           403     −2.2             433           475        9.7
                 (1167)
                               alarms          284           279     −1.8             361           381        5.5
                             #Solved           611           632       3.4            674           838       24
              Termination
                 (1241)        proofs           65            85      31              109           212       94
                               alarms          546           547       0.18           565           626       11


circuit size of zero. Note that, however, this does not imply that the verification problem itself is trivial, as scorr is
a high-effort optimization procedure that involves constraint solving.
  When comparing the entire verification run (PDR vs. scorr + PDR) in Fig. 12 and Table 4, we notice that the efficiency
did not improve with the application of scorr, despite the simplification in the circuit. Nevertheless, effectiveness, in
terms of the number of solved tasks, was improved (see Table 5). In addition, we observe that the run time of PDR
following scorr (denoted by (sc.+)PDR) was generally lower than that of PDR alone, indicating that PDR indeed
benefited from the simplified circuit. This suggests that while circuit optimization can reduce the size of the circuit
and help improve the downstream model-checking performance, it does not always translate to faster end-to-end
verification times due to the overhead of the optimization process itself.

   Sequential logic optimization in ABC effectively reduces circuit size for both encodings, with stronger reductions
   under functional encoding. While this simplification can improve the effectiveness of PDR, it does not necessarily
   lead to faster end-to-end verification due to the non-negligible run-time overhead of the optimization itself.

                                                                                                      Manuscript submitted to ACM
34                                                                               Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer

                                            Table 6. Effect of L2S variable elimination on SV-COMP Termination tasks


                                                                       rIC3 · IC3                                     Pono · k-induction
                          Encoding          Results
                                                           w/o simp.       w/ simp.         Δ (%)               w/o simp.     w/ simp.         Δ (%)
                                            #Solved              575          932       62                          780         1 083          39
                          Relational          proofs             262          244       −6.9                        378           378           0
                                              alarms             313          688      120                          402           705          75
                                            #Solved              770          977          27                       392         1 014         160
                          Functional          proofs             237          281          19                       316           317           0.32
                                              alarms             533          696          31                        76           697         820


                103                                                                                   103



                102                                                                                   102
CPU time (s)




                                                                                      CPU time (s)
                101                                                                                   101



                100                                                                                   100
                                     rIC3 w/o simp.          rIC3 w/ simp.                                                  rIC3 w/o simp.          rIC3 w/ simp.
                                     Pono w/o simp.          Pono w/ simp.                                                  Pono w/o simp.          Pono w/ simp.
               10−1                                                                                  10−1
                      0    200        400        600       800     1 000                                    0      200        400       600         800     1 000
                                   n-th fastest correct result                                                            n-th fastest correct result
                                 (a) Relational encoding                                                             (b) Functional encoding


Fig. 13. Cactus plots for CPV using relational (a) and functional (b) encodings, each comparing different backends with and without
L2S variable elimination on SV-COMP Termination tasks



RQ3.1: Effect of Eliminating Instrumented Variables During L2S. In this RQ, we evaluate the optimization described
in Sect. 7.2. Instead of introducing recording state variables for all state variables in the transformed circuit, the
optimization omits recording variables for auxiliary counter variables introduced during program instrumentation.
In CPV, this behavior can be toggled via a command-line flag. The full verification pipeline of CPV was executed
using rIC3’s IC3 and Pono’s k-induction engines as backends, considering both relational and functional encodings
on SV-COMP Termination tasks.
         Table 6 summarizes the number of tasks solved by CPV with and without L2S variable elimination, and Fig. 13
further visualizes the results using cactus plots.13 The optimization yields substantial improvements for both relational
and functional encodings, as well as for both backend engines. The increase in the number of detected alarms (non-
terminating lassos) is particularly notable. We compared the lasso lengths of the commonly solved instances by Pono’s
k-induction engine with and without variable elimination.14 With relational encoding, the optimization reduces the
lasso length by an average of 98.4 %; with functional encoding, the average reduction is 96.7 %. These results confirm the

13 Table 6 shows more Termination tasks solved by rIC3’s IC3 than Table 2a. There are two reasons: First, only tasks that can be successfully translated
under both encodings are considered in Table 2a. Second, when filtering for bit-vector-only tasks, we checked for the presence of array sorts in the Btor2
file. However, some Btor2 circuits containing arrays can still be handled by rIC3 if the arrays are not in the cone of influence of the property.
14 We did not compare lasso lengths for rIC3’s IC3 engine, as IC3 does not guarantee shortest counterexamples.

Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                        35

     Table 7. Comparison of TransVer and CPV on SV-COMP Termination tasks (✓: TransVer’s L2S transformation succeeded)


                                              TransVer-CPV                                  CPV
        Category             #Tasks
                                                                                     (c)
                                       (a) TransVer✓    (b) Solved     (c) Solved   Δ (%)
                                                                                     (b)      (a) ∩ (c)   Δ(a)∩(c)
                                                                                                           (b)     (%)
        BitVectors                34           31             22            24        9.1          23        4.5
        MainControlFlow          253          231             70            80       14            71        1.4
        Other                  1 526          669            389           910      130           448       15
        Overall                1 813          931            481          1 014     110           542       13


intuition presented in Sect. 7.2 that excluding instrumented counter variables from the state-revisit check substantially
shortens the lasso witnesses, making non-termination easier for hardware model checkers to detect.

   Elimination of instrumented variables during L2S helps increase the number of solved Termination tasks across
   different encodings and backends. The increase is largely due to a higher number of detected alarms, as the
   optimization makes the state-revisit condition easier to satisfy.

RQ3.2: Comparison with TransVer. We further evaluate the capability of CPV’s L2S transformer by comparing it with
TransVer [26], a source-level L2S transformation tool for C programs. TransVer first transforms termination tasks
into reachability tasks, after which CPV verifies the resulting programs. This combined pipeline is referred to as
TransVer-CPV. In our experiment, CPV was executed using functional encoding with Pono’s k-induction as the backend
model-checking engine.
  The evaluation results are summarized in Table 7. Column (a) reports the number of tasks for which TransVer
successfully performed the L2S transformation, while column (b) shows the number of those tasks subsequently solved
by CPV. Column (c) reports the number of tasks solved by CPV using its own L2S transformation. Column (a) ∩ (c)
further provides the number of tasks that are both successfully transformed by TransVer and solved by CPV using
its own L2S transformation.
  CPV’s L2S transformer outperformed TransVer in two aspects: (1) CPV was more robust and was capable of handling
a larger number of the benchmark tasks. TransVer successfully transformed only about half of the termination tasks
(see column (a) in Table 7), as it does not support programs with arrays or dynamic memory allocation. By contrast,
CPV’s L2S transformation can handle all instances that have been successfully translated into Btor2 circuits (see
Table 1). Moreover, TransVer-CPV inherits the same frontend limitation (see RQ1) from CPV. Therefore, the set of tasks
TransVer-CPV can successfully translate is ultimately a subset of those supported by CPV alone, which limits its overall
effectiveness (see columns (b) and (c) in Table 7). (2) Circuits produced by CPV’s L2S transformation were more amenable
to Pono’s k-induction. Among the tasks that were successfully transformed by both TransVer-CPV and CPV, the latter
solved more instances (see columns (b) and (a) ∩ (c) in Table 7), suggesting that CPV’s L2S transformation yields circuits
that are better suited for model checking in our experiments.
  It is worth noting, however, that TransVer and CPV’s L2S transformer serve different purposes. TransVer is designed
as a source-level transformation tool that can be combined with off-the-shelf software verifiers, whereas CPV’s L2S
transformer is an integral part of an end-to-end circuit-based verification pipeline. This design difference leads to
distinct trade-offs in supported language features, robustness, and the structure of the generated representations. It also
reflects differences in implementation complexity: TransVer relies on CPAchecker for CFA construction and implements
                                                                                                  Manuscript submitted to ACM
36                                                                     Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer

                                          Table 8. Validation results of CPV’s violation witnesses


                                                 Witness v1                   Witness v2             Combined     Confirmation
        Category          CPV
                                    CPAchecker        Symbiotic-Witch     CPAchecker     Witch
                                                                                                     #validated     rate (%)

        ReachSafety        1 083           931               1 012             925        1 011         1 018        94.0
        Termination          698           113                   0             496          603           676        96.8



custom instrumentation automata and sequentialization operators, whereas CPV’s L2S transformer operates directly at
the circuit level, which is simpler to manipulate, and is implemented in approximately 200 lines of Python code.

     CPV’s L2S transformer outperforms TransVer in both robustness and effectiveness. It supports a broader range
     of tasks and produces circuits that are more amenable to model checking, resulting in a higher number of
     solved instances. While the two approaches serve different purposes, the results demonstrate the advantage of
     performing L2S at the circuit level in CPV’s pipeline.

RQ4: Witness Generation and Validation. In this RQ, we aim to assess the quality and the validity of the violation
witnesses generated by CPV. We first executed CPV using functional encoding and Pono’s BMC as the backend on
the SV-COMP benchmark set to produce the witnesses in both v1 (GraphML) and v2 (YAML) formats. Subsequently,
CPAchecker, Symbiotic-Witch, and Witch were used to validate the generated witnesses in the formats they support.
     Table 8 summarizes the validation results. Column “CPV” reports the number of detected alarms (and hence the
number of generated violation witnesses). The subsequent columns report the number of witnesses confirmed by each
validator, followed by the combined validation results and the overall confirmation rate.
     For the ReachSafety category, validation results were similar for v1 and v2 witnesses. A slight drop in confirmed cases
by CPAchecker is observed when comparing v1 to v2, even though witnesses in both formats contain essentially the same
information. This issue has been reported to the CPAchecker development team and is currently under investigation.15
     For the Termination category, validation results were notably better for v2 witnesses. In particular, Symbiotic-Witch was
unable to confirm any v1 witnesses. This is because, in the v1 format, certain structural requirements for non-termination
witnesses are not well defined, and their semantics with respect to the original programs are ambiguous. This limitation
lies in the witness format rather than in CPV’s witness translator, and has been addressed in the newer v2 format [133].
     Overall, CPV produces high-quality violation witnesses that can be confirmed by multiple validators, achieving a
combined confirmation rate of approximately 95 % across both categories. The unconfirmed cases are mainly due to
validators reaching resource limits (CPU time or memory).

     Violation witnesses exported by CPV can be reliably validated by multiple witness validators, achieving a high
     overall confirmation rate (about 95 %). Validation results are consistent across formats for ReachSafety, while the
     newer v2 format significantly improves validation for Termination tasks.

RQ5.1: Comparison with SOTA Software Verifiers on ReachSafety Tasks. Finally, we evaluated the end-to-end capability
of CPV on the SV-COMP benchmark set and compared it with state-of-the-art software verifiers. CPV was executed in

15 https://gitlab.com/sosy-lab/software/cpachecker/-/work_items/1494

Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                                     37

                                            Table 9. SV-COMP ReachSafety and Termination results


            Category         Results         CPV       CPAchecker         Esbmc      Kratos2       Symbiotic      UAutomizer         VBS
                            Correct          9 483          8 307          9 631        7 325         4 188           2 869         12 024
                              proofs                        6 590                       6 002         2 671           1 992          9 625
             ReachSafety


                                             8 064                         7 724
               (14 208)


                              alarms         1 419          1 717          1 907        1 323         1 517             877          2 399
                            Incorrect            0              1              0            0             1               0              0
                            Best             4 368            681          5 170          621           926             258              -
                            Unique             606            243            391           65           190             118              -
                            Correct          1 316          1 199            728              -       1 248           1 467          1 772
                              proofs           592            562                             -         613                          1 009
            Termination




                                                                             728                                        875
                              alarms                                           0              -         635             592            763
               (1 993)




                                               724            637
                            Incorrect            0              1              0              -           0               1              0
                            Best               106            200            691              -         634             141              -
                            Unique              18              8              5              -           9             128              -



its SV-COMP configuration, running the sequential portfolios described in Sect. 8.4; the compared tool versions and
configurations are specified in Sect. 9.2.2.
   The upper part of Table 9 summarizes the results for ReachSafety tasks and reports, for each verifier, the number of
“best” results (in terms of CPU time) and uniquely solved tasks. The column “VBS” denotes the virtual best solver, a
hypothetical solver that always achieves the best-performing result (in terms of computational resources) among all
compared tools for each task. Tables 10 and 11 further break down the results by subcategory. In the tables, yellow-
highlighted cells indicate the best results, while light-gray cells indicate the second-best results; both are shown in
boldface. Cells colored in red mark incorrect results. The cactus plots in Fig. 14 visualize the CPU time of the compared
tools on the benchmark tasks, focusing on subcategories where CPV is highlighted at least once in the tables.
   On ReachSafety, CPV achieved competitive results, producing the highest number of proofs and solving the second-
largest number of tasks overall. It did not produce any incorrect results on the benchmark set, indicating reliable
verification behavior. Moreover, CPV solved the most unique instances and achieved the best performance on the second-
largest number of tasks. Since subcategory sizes vary significantly and may bias aggregated results, we additionally
examined performance at the subcategory level. As expected, CPV performed particularly well on hardware-like
programs, including the Hardware subcategory translated from hardware model checking tasks using Btor2C [1]
and the ECA subcategory derived from Event-Condition-Action reactive systems [93]. Strong performance was also
observed on subcategories ProductLines (derived from product-line systems) and XCSP (originating from constraint
programming), as well as on benchmark tasks involving common C constructs, such as subcategories Arrays, BitVectors,
and Hardness [13, 76]. These results indicate that the proposed circuit-based approach is effective across a diverse
range of benchmarks and can outperform many established software-verification techniques.
   The subcategory where CPV showed comparatively weaker performance is Heap, primarily due to frontend limitations
(see RQ1).16 Kratos2, on which CPV’s frontend relies, also exhibited weaker performance on this subcategory. That
said, even in subcategories where CPV is not highlighted in Tables 10 and 11, it still delivered some best or uniquely
solved results, demonstrating its complementary strengths to the other evaluated verifiers.

16 More tasks are reported as correctly solved by CPV’s SV-COMP portfolio in Table 10 than those successfully translated in Table 1, because the portfolio
incorporates multiple translation configurations (e.g., with program slicing), whereas in RQ1, only CPV’s default translation mode was evaluated.
                                                                                                                          Manuscript submitted to ACM
38                                                               Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer

                                Table 10. SV-COMP ReachSafety results for each subcategory (Part 1)


          Category        Results      CPV     CPAchecker      Esbmc    Kratos2    Symbiotic    UAutomizer   VBS
                          Correct       105           74           99        83         154            87     183
                            proofs       32            4           23         7          68            11      94
                            alarms       73           70                                                       89
           Arrays
            (440)                                                  76        76          86            76
                          Incorrect       0            0            0         0           0             0       0
                          Best           18            0           73         7          80             5       -
                          Unique         18            0            1         0          59             2       -
                          Correct         45          43           34        44          38            34      45
                            proofs        33          31           22        32          26            24      33
           BitVectors




                            alarms        12          12           12        12          12            10      12
              (48)




                          Incorrect        0           0            0         0           0             0       0
                          Best            14           0           19         8           4             0       -
                          Unique           1           0            0         0           0             0       -
                          Correct        238         337         398         80         223           108     501
           Combinations




                            proofs        32          31          47         15           0            13      81
                            alarms       206         306         351         65         223            95     420
              (671)




                          Incorrect        0           0           0          0           0             0       0
                          Best            20          66         303         23          89             0       -
                          Unique           5          41          26          0          35             0       -
                          Correct         29          40           25        29          37            40      47
                            proofs        25                       17        24          21                    29
           ControlFlow




                                                      27                                               27
                            alarms         4          13            8         5          16            13      18
              (73)




                          Incorrect        0           0            0         0           0             0       0
                          Best             9           1           21         3          12             1       -
                          Unique           0           1            2         0           0             1       -
                          Correct       596          729         312        662         283           613     964
                            proofs      432          478           0        312           0           421     572
                            alarms      164          251                                283           192     392
           (1 263)




                                                                 312        350
            ECA




                          Incorrect       0            0           0          0           0             0       0
                          Best          255          215          58         77         233           126       -
                          Unique          4           67           0         48          20            70       -
                          Correct        192         446         567        268         407           432     616
                            proofs       159         381         452        219         347           360     477
                            alarms        33          65                     49          60                   139
           (1 400)
           Floats




                                                                 115                                   72
                          Incorrect        0           0           0          0           1             0       0
                          Best            12          14         363         92         113            22       -
                          Unique           4           1          64          1          19             8       -
                          Correct      6 077       4 565        6 371     4 469       1 247           348    6 701
                            proofs     6 077       4 565        6 371     4 469       1 247           348    6 701
           Hardness




                            alarms         0           0            0         0           0             0        0
            (6 789)




                          Incorrect        0           0            0         0           0             0        0
                          Best         3 302         180        3 133        61          25             0        -
                          Unique         277          11          191        15           2             0        -




Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                              39

                                 Table 11. SV-COMP ReachSafety results for each subcategory (Part 2)


         Category          Results      CPV     CPAchecker      Esbmc    Kratos2    Symbiotic    UAutomizer      VBS
                           Correct       792          251         359        459          98            83         823
                             proofs      449          116           5        182          48            51         450
          Hardware




                             alarms                   135                    277          50            32         373
           (1 224)



                                         343                      354
                           Incorrect       0            0           0          0           0             0           0
                           Best          592            3         213         15           0             0           -
                           Unique        283            0          26          0           0             0           -
                           Correct         72         189         212         73         189           156         225
                             proofs        50         118         141         48         120            94         153
                             alarms        22                                 25          69            62          72
          Heap
          (237)




                                                       71          71
                           Incorrect        0           0           0          0           0             0           0
                           Best             0           0         169         18          37             1           -
                           Unique           0           0          31          0           1             1           -
                           Correct        483         480         456        462         593           507         690
                             proofs       358         348         315        322         426           378         507
                             alarms       125         132                    140                       129         183
          Loops
          (762)




                                                                  141                    167
                           Incorrect        0           1           0          0           0             0           0
                           Best            40          26         189        202         131           102           -
                           Unique           4           0           4          1          49            36           -
                           Correct       584          597         503        579         532           356         597
                             proofs                               238        314         267           256         332
          ProductLines




                                         323          332
                             alarms      261          265         265        265         265           100         265
              (597)




                           Incorrect       0            0           0          0           0             0           0
                           Best           84           10         342        112          49             0           -
                           Unique          0            9           0          0           0             0           -
                           Correct        165         455         188         15         296            56         523
          Sequentialized




                             proofs        42         107          40          8          51             6         143
                             alarms       123         348         148          7         245            50         380
              (585)




                           Incorrect        0           0           0          0           0             0           0
                           Best            17         166         183          3         153             1           -
                           Unique           8         113          43          0           5             0           -
                           Correct       105          101         107        102          91            49         109
                             proofs       52           52          53         50          50             3          53
                             alarms                    49                     52          41            46          56
          XCSP
          (119)




                                          53                       54
                           Incorrect       0            0           0          0           0             0           0
                           Best            5            0         104          0           0             0           -
                           Unique          2            0           3          0           0             0           -


  CPV adopts a fundamentally different verification approach from the other tools in the comparison: it “folds” programs
into circuits with a monolithic transition relation, whereas most other verifiers rely on path-based exploration. This
distinction enables CPV to complement existing techniques. Moreover, advances in hardware model checking allow
CPV to leverage powerful engines to effectively analyze the resulting circuits, despite their potential complexity due to
the monolithic encoding. Overall, CPV demonstrates competitive performance on ReachSafety tasks in SV-COMP. As
mentioned previously, we plan to enhance its frontend capability in order to further improve its effectiveness.
                                                                                                        Manuscript submitted to ACM
40                                                                                   Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer

           103                                                    103                                                   103


           102                                                    102                                                   102


           101                                                    101                                                   101


           100                                                    100                                                   100


       10−1                                                      10−1                                                  10−1
                  0           5 000         10 000                       0   50      100     150         200                  0            20            40

                            (a) Overall                                       (b) Arrays                                          (c) BitVectors
            103                                                    103                                                  103


            102                                                    102                                                  102


            101                                                    101                                                  101


            100                                                    100                                                  100


           10−1                                                  10−1                                                  10−1
                  0            200          400                          0           500             1 000                    0    2 000        4 000   6 000

                        (d) Combinations                                          (e) ECA                                         (f) Hardness
     103                                              103                                      103                                              𝑥: n-th fastest result
                                                                                                                                                   𝑦: CPU time (s)
     102                                              102                                      102                                                      CPV
                                                                                                                                                        CPAchecker
     101                                              101                                      101                                                      Esbmc
                                                                                                                                                        Kratos
                                                                                                                                                        Symbiotic
     100                                              100                                      100
                                                                                                                                                        UAutomizer
                                                                                                                                                        VBS
 10−1                                                10−1                                     10−1
           0          200    400      600    800            0      200       400       600           0            50              100

                      (g) Hardware                              (h) ProductLines                               (i) XCSP


Fig. 14. Cactus plots for SV-COMP ReachSafety category and its subcategories, where CPV is highlighted at least once in Tables 10
and 11




      CPV demonstrates competitive performance on the SV-COMP ReachSafety benchmark set, solving the second-
      highest number of tasks and achieving strong results across diverse subcategories. More importantly, it comple-
      ments existing software verifiers by uniquely solving tasks that others cannot handle. Its current weaknesses are
      partly due to frontend limitations, which present opportunities for further improvement.


RQ5.2: Comparison with SOTA Software Verifiers on Termination Tasks. Continuing from RQ5.1, we follow a similar
evaluation procedure to compare CPV with state-of-the-art software verifiers on the SV-COMP Termination benchmark
set. Kratos2 does not support termination analysis for C programs and is therefore excluded from this comparison. The
results are summarized in the lower part of Table 9, with Fig. 15 and Table 12 providing a breakdown by subcategory.
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                              41

                                     Table 12. SV-COMP Termination results for each subcategory


               Category          Results     CPV       CPAchecker    Esbmc    Symbiotic   UAutomizer       VBS
                                 Correct        24          10           13         23            28          33
                                   proofs       13           3           13         13            22          22
               BitVectors


                                   alarms       11           7            0         10             6          11
                  (34)


                                 Incorrect       0           0            0          0             0           0
                                 Best            1           1           12         11             8           -
                                 Unique          1           0            0          0             8           -
                                 Correct        82                       31         75                       215
               MainControlFlow




                                                           178                                    205
                                   proofs       30         130           31         29            156        161
                                   alarms       52          48            0         46             49         54
                    (253)




                                 Incorrect       0           1            0          0              0          0
                                 Best           10         108           28         44             25          -
                                 Unique          0           3            1          0             22          -
                                 Correct           0         5           11         12            76          80
                                   proofs          0         0           11         12            67          71
               MainHeap




                                   alarms          0         5            0          0             9           9
                 (180)




                                 Incorrect         0         0            0          0             1           0
                                 Best              0         5           10          3            62           -
                                 Unique            0         0            0          1            62           -
                                 Correct     1 210        1 006        673       1 138        1 158        1 444
                                   proofs      549          429        673         559          630          755
                                   alarms                   577          0                      528          689
               (1 526)
               Other




                                               661                                 579
                                 Incorrect       0            0          0           0            0            0
                                 Best           95           86        641         576           46            -
                                 Unique         17            5          4           8           36            -



  CPV again performed competitively on Termination, solving the second-largest number of tasks overall and producing
no incorrect results. It also detects the highest number of non-terminating lassos across nearly all subcategories, except
for MainHeap, where the frontend limitations (see RQ1) prevent it from translating the verification tasks into circuits.
CPAchecker and Symbiotic, which employ techniques similar to L2S by checking for state revisits, also perform well in
this regard, detecting the second- and third-largest numbers of non-terminating executions, respectively. These results
suggest that approaches that explicitly check for state revisits are effective for lasso detection in termination analysis.
  For proving termination, however, CPV is less effective than the top-performing tools. UAutomizer, the strongest
verifier in this category, relies on ranking-function synthesis [89, 99, 119] and is particularly effective at proving
termination on the benchmark set, especially in the subcategory MainControlFlow. Esbmc, on the other hand, attempts
to prove termination by exhaustively exploring all program execution paths, for example by checking whether loops
can be fully unrolled to a finite bound. L2S-based approaches introduce auxiliary variables (to record state history)
and additional constraints (to encode state-revisit conditions), which may increase the complexity of the verification
problem. Nevertheless, CPV still achieves reasonable performance.
  Most word-level hardware model checkers in recent editions of HWMCC do not directly support termination analysis.
Consequently, CPV mainly relies on its L2S transformation to reduce termination to reachability problems. Our results
reveal a limitation of this approach: while simple and general, it is less effective than specialized techniques for proving
                                                                                                        Manuscript submitted to ACM
42                                                                         Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer

                                 103                                               103


                                 102                                               102


                                 101                                               101


                                 100                                               100


                                10−1                                              10−1
                                       0    500      1 000   1 500                       0        10        20       30

                                              (a) Overall                                        (b) BitVectors
              103                                              103
                                                                                                                  𝑥: n-th fastest result
              102                                              102                                                   𝑦: CPU time (s)
                                                                                                                          CPV
              101                                              101                                                        CPAchecker
                                                                                                                          Esbmc
                                                                                                                          Symbiotic
              100                                              100
                                                                                                                          UAutomizer
                                                                                                                          VBS
             10−1                                            10−1
                    0           100            200                   0      500          1 000      1 500

                        (c) MainControlFlow                                 (d) Other


 Fig. 15. Cactus plots for SV-COMP Termination category and its subcategories, where CPV is highlighted at least once in Table 12


termination. This observation opens up interesting research directions, such as incorporating more liveness-checking
techniques for transition systems, including FAIR [48], 𝑘-liveness [62], and rlive [57, 132]. Currently, to the best of
our knowledge, Pono [117] is the only hardware model checker that directly supports checking justice constraints
in Btor2 circuits. Several existing model checkers implement the aforementioned liveness-checking algorithms, but
they are not readily applicable in our setting because they target different input formats and do not export witnesses
in Btor2 format.17 By contributing translated Btor2 circuits to HWMCC, we aim to encourage the development of
more advanced liveness-checking capabilities, which could subsequently be integrated into CPV to further improve
its performance on termination analysis.

     CPV achieves competitive results on the SV-COMP Termination benchmark set, solving the second-largest number
     of tasks without producing incorrect results. It is particularly strong in finding non-terminating executions via
     state-revisit detection, while being less effective at proving termination compared to tools based on ranking
     function synthesis.

Summary. Across RQ1–RQ4, we examined the feasibility of the proposed methodology, including encoding C programs
as sequential circuits, reusing off-the-shelf hardware model checkers for verification, and exporting software-level
violation witnesses. In RQ5, competitive performance against state-of-the-art software verifiers further strengthens the
practicality and significance of the proposed framework. Taken together, these findings show that:
17 nuXmv [51], which implements FAIR, 𝑘 -liveness, and rlive, accepts SMV [105], VMT-LIB [61], and Aiger [44] as input, IC3ia [59] accepts VMT-LIB, and
ABC [49] accepts Aiger. Although Btor2Aiger [113], vmt-tools [61], and utility scripts shipped with nuXmv releases provide translations from Btor2 to
these formats, none of them currently supports translating justice constraints.
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                          43


      Sequential circuits are a practical intermediate representation for software verification, and hardware model
      checking can be applied effectively to software-verification problems.


9.4     Threats to Validity
We discuss the potential threats to the validity of our study and the measures taken to mitigate them.

External Validity. The conclusions of our study are drawn from the evaluation results. We used the SV-COMP benchmark
suite, which is the largest and most diverse open-source collection of verification tasks for the programming language C.
Programs containing recursive functions were excluded because recursion is not currently supported by CPV.
  For RQ2, evaluating the complete benchmark suite would have been prohibitively expensive. Therefore, we used
a sampled benchmark set and ensured that all benchmark subcategories were sufficiently represented in the sample.
The observations in RQ2 are also limited to benchmark tasks that can be successfully translated into Btor2 circuits
by CPV. Consequently, the reported effects of different encoding strategies may not generalize to programs that are
currently unsupported by the frontend. Nevertheless, the successfully translated instances span diverse benchmark
categories and program characteristics, providing a solid basis for the study.
  For RQ5, we compared CPV against the top-performing tools in SV-COMP 2026. These tools employ SMT-based
reasoning but differ substantially in their architectures, verification algorithms, and areas of strength. We believe that the
selected competitors reflect the current state of the art and allow a meaningful assessment of CPV’s relative performance.
  CPV’s backend consists of several state-of-the-art hardware model checkers, covering both bit-level (SAT-based) and
word-level (SMT-based) reasoning, as well as a broad range of configurations and verification engines. This provides
representative coverage of mainstream approaches in hardware model checking. In several experiments, CPV ran fixed
sequential portfolios selected from preliminary experiments. Different portfolio configurations may lead to different
performance results. To mitigate this threat, the portfolios were selected using a subset of SV-COMP 2025 benchmark tasks
and combine engines with complementary strengths rather than being optimized for individual benchmark families.

Internal Validity. The experimental results depend on the correctness of CPV and the integrated verification workflow.
During the development of CPV, we discovered several issues in Kratos2, one of the key components used for program
translation. We developed patches and reported the issues to the developers of Kratos2, and all identified issues were
subsequently resolved. To detect potential unsoundness in backend hardware model checkers, every violation witness
produced is validated using BtorSim before being translated into a software-verification witness. This validation step
ensures that the reported counterexample is consistent with regard to the translated sequential circuit. The correctness
of the overall translation pipeline is another potential source of error. To increase confidence in the implementation, CPV
emits software-verification witnesses for the detected violations, which have been validated by multiple independent
witness validators. While we do not claim that CPV is free of bugs, we did not observe any incorrect verification
results in our experiments.
  The generated sequential circuits also depend on the underlying frontend implementation. In particular, the relational
encoding is provided by Kratos2, which is available only as a binary executable. As a result, certain implementation
details, such as the encoding of the symbolic program counter, cannot be controlled or modified by CPV. Different
encodings may produce structurally different circuits. However, the program-counter state variable and its update
logic make up only a small fraction of the overall transition system and are largely independent of the encoding of the
program’s data variables and their corresponding transition logic. We expect the choice of program-counter encoding
                                                                                                    Manuscript submitted to ACM
44                                                             Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


to have only a limited impact on circuit size and verification performance. This expectation is consistent with our
preliminary experiments comparing binary and one-hot program-counter encodings in the functional encoder. We
therefore do not expect this implementation detail to significantly affect the conclusions drawn from our comparison
of relational and functional encodings.
     All experiments were executed via the widely used benchmarking framework BenchExec [31]. BenchExec utilizes
features in the modern Linux kernel such as cgroups for resource measurement and limitation, namespaces for process
isolation, and overlay file systems to prevent benchmark runs from modifying the host environment. To reduce
interference from shared hardware resources (e.g., through hyper-threading), each benchmark run was restricted to
two virtual CPU cores pinned to the same physical core, and that physical core was dedicated exclusively to the run.


10     Conclusion and Future Work
We present CPV, a circuit-based program-verification framework that translates C programs into word-level sequential
circuits and leverages off-the-shelf hardware model checkers as verification backends. The central premise of this
work is that sequential circuits constitute a viable intermediate representation for software verification, allowing the
direct reuse of hardware model checkers without algorithmic reimplementation. Our comprehensive evaluation on
the SV-COMP 2026 benchmark set supports this premise. More than 70 % of the benchmark tasks can be successfully
translated into sequential circuits. Among all evaluated tools, CPV solved the second-largest number of tasks in both
the ReachSafety and Termination categories while complementing existing software verifiers by uniquely solving
many benchmark instances. Approximately 95 % of the generated violation witnesses were confirmed by independent
witness validators. The results further show that functional encoding produces more compact circuits and generally
improves model-checking performance. They also demonstrate the effectiveness of the circuit-level liveness-to-safety
transformation and that eliminating auxiliary instrumentation variables can further improve the lasso-finding capability.
     The current limitations of CPV are primarily in its frontend. The functional encoder does not yet support floating-point
data types, and the underlying C-to-K2 translation does not support several C language features, such as non-constant
initializers in array declarations. Replacing K2 with SV-LIB [23], a recently proposed SMT-LIB-based exchange format
for software-verification tasks, is a promising direction once a robust C-to-SV-LIB translator becomes available. On the
proof side, CPV currently emits only trivial correctness witnesses when a property is proven. Extracting the inductive
invariants produced by hardware model checkers and translating them into program-level loop invariants would enable
the generation of independently checkable correctness witnesses. Another direction for future work is to improve
the selection of verification backends. Currently, CPV employs a fixed sequential portfolio of model-checker engines
determined by the verification property and theories involved. A more adaptive strategy could adopt machine-learning-
based algorithm selection to predict suitable backend configurations for individual verification tasks [102], potentially
improving overall performance and reducing unnecessary computational effort.
     More broadly, this work contributes a large collection of Btor2 circuits translated from the SV-COMP benchmark suite,
which have been made publicly available and used in recent editions of HWMCC. The utility of these circuits is already
evidenced by the development of the model checker Pono, which has shown significant performance improvements
on these translated Btor2 tasks [117] and now serves as the primary backend for CPV. We hope these translated
benchmark tasks will encourage broader support for liveness properties in hardware model checkers, which could
directly benefit CPV’s termination analysis, and further strengthen the connection between the hardware- and software-
verification communities.
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                                      45


Data-Availability Statement
CPV is an open-source project maintained on GitLab, with stable releases archived on Zenodo [53]. The benchmark
set [34], verifiers [3, 35, 55, 68, 86, 100], and validators [6, 8, 35] used in the evaluation are available on Zenodo as well.

Funding Statement
This project was funded in part by the Deutsche Forschungsgemeinschaft (DFG) under grants 378803395 (ConVeY)
and 536040111 (Bridge), the LMU Postdoc Support Fund, and a fellowship from the German Academic Exchange
Service (DAAD).

References
 [1] S. Ates, D. Beyer, P.-C. Chien, and N.-Z. Lee. 2026. Bridging Hardware and Software Analysis with Btor2C: A Word-Level-Circuit-to-C Translator
     (Extended Version). Int. J. Softw. Tools Technol. Transf. (2026). doi:10.1007/s10009-026-00847-z
 [2] P. Ayaziová, D. Beyer, M. Lingsch-Rosenfeld, M. Spiessl, and J. Strejček. 2024. Software Verification Witnesses 2.0. In Proc. SPIN (LNCS 14624).
     Springer, 184–203. doi:10.1007/978-3-031-66149-5_11
 [3] P. Ayaziová, M. Jonáš, V. Mihalkovič, J. Sedláček, and J. Strejček. 2025. Symbiotic: Submission to SV-COMP 2026. Zenodo. doi:10.5281/zenodo.
     17698724
 [4] P. Ayaziová, M. Jonáš, V. Mihalkovič, J. Sedláček, and J. Strejček. 2026. Symbiotic 11: Predicate Abstraction Joins the Party (Competition
     Contribution). In Proc. TACAS (2) (LNCS 16506). Springer, 583–588. doi:10.1007/978-3-032-22749-2_36
 [5] P. Ayaziová and J. Strejček. 2023. Symbiotic-Witch 2: More Efficient Algorithm and Witness Refutation (Competition Contribution). In Proc.
     TACAS (2) (LNCS 13994). Springer, 523–528. doi:10.1007/978-3-031-30820-8_30
 [6] P. Ayaziová and J. Strejček. 2024. Symbiotic-Witch 2: SV-COMP 2025. Zenodo. doi:10.5281/zenodo.18462288
 [7] P. Ayaziová and J. Strejček. 2024. Witch 3: Validation of Violation Witnesses in the Witness Format 2.0 (Competition Contribution). In Proc.
     TACAS (3) (LNCS 14572). Springer, 341–346. doi:10.1007/978-3-031-57256-2_18
 [8] P. Ayaziová and J. Strejček. 2025. Witch 4: SV-COMP 2026. Zenodo. doi:10.5281/zenodo.17697224
 [9] D. Baier, D. Beyer, P.-C. Chien, M.-C. Jakobs, M. Jankola, M. Kettl, N.-Z. Lee, T. Lemberger, M. Lingsch-Rosenfeld, H. Wachowitz, and P. Wendler. 2024.
     Software Verification with CPAchecker 3.0: Tutorial and User Guide. In Proc. FM (LNCS 14934). Springer, 543–570. doi:10.1007/978-3-031-71177-0_30
[10] D. Baier, D. Beyer, P.-C. Chien, M. Jankola, M. Kettl, N.-Z. Lee, T. Lemberger, M. Lingsch-Rosenfeld, M. Spiessl, H. Wachowitz, and P. Wendler. 2024.
     CPAchecker 2.3 with Strategy Selection (Competition Contribution). In Proc. TACAS (3) (LNCS 14572). Springer, 359–364. doi:10.1007/978-3-031-
     57256-2_21
[11] C. Barrett, P. Fontaine, and C. Tinelli. 2025. The SMT-LIB Standard: Version 2.7. Technical Report. University of Iowa. https://smt-lib.org/papers/smt-
     lib-reference-v2.7-r2026-03-27.pdf
[12] M. Bentele, M. Barth, M. Ebbinghaus, J. Körner, D. Dietsch, M. Heizmann, D. Klumpp, F. Schüssele, and A. Podelski. 2026. Ultimate Automizer
     with a One-Dimensional Memory Model (Competition Contribution). In Proc. TACAS (2) (LNCS 16506). Springer, 589–594. doi:10.1007/978-3-032-
     22749-2_37
[13] P. Berger. 2024. Applying Software Model Checking: Experiences and Advancements. Ph. D. Dissertation. RWTH Aachen University. doi:10.18154/
     RWTH-2024-10081
[14] D. Beyer. 2026. FM-Tools Release 2.3: Data Set of Metadata about Tools for Formal Methods (SV-COMP 2026, Test-Comp 2026). Zenodo.
     doi:10.5281/zenodo.18650756
[15] D. Beyer, P.-C. Chien, and M. Jankola. 2024. BenchCloud: A Platform for Scalable Performance Benchmarking. In Proc. ASE. ACM, 2386–2389.
     doi:10.1145/3691620.3695358
[16] D. Beyer, P.-C. Chien, M. Jankola, and N.-Z. Lee. 2024. A Transferability Study of Interpolation-Based Hardware Model Checking for Software
     Verification. Proc. ACM Softw. Eng. 1, FSE, Article 90 (2024), 23 pages. doi:10.1145/3660797
[17] D. Beyer, P.-C. Chien, and N.-Z. Lee. 2023. Bridging Hardware and Software Analysis with Btor2C: A Word-Level-Circuit-to-C Translator. In Proc.
     TACAS (2) (LNCS 13994). Springer, 152–172. doi:10.1007/978-3-031-30820-8_12
[18] D. Beyer, P.-C. Chien, and N.-Z. Lee. 2023. CPA-DF: A Tool for Configurable Interval Analysis to Boost Program Verification. In Proc. ASE. IEEE,
     2050–2053. doi:10.1109/ASE56229.2023.00213
[19] D. Beyer, A. Cimatti, A. Griggio, M. E. Keremoglu, and R. Sebastiani. 2009. Software Model Checking via Large-Block Encoding. In Proc. FMCAD.
     IEEE, 25–32. doi:10.1109/FMCAD.2009.5351147
[20] D. Beyer, M. Dangl, D. Dietsch, M. Heizmann, T. Lemberger, and M. Tautschnig. 2022. Verification Witnesses. ACM Trans. Softw. Eng. Methodol. 31,
     4 (2022), 57:1–57:69. doi:10.1145/3477579
[21] D. Beyer, M. Dangl, and P. Wendler. 2015. Boosting k-Induction with Continuously-Refined Invariants. In Proc. CAV (LNCS 9206). Springer, 622–640.
     doi:10.1007/978-3-319-21690-4_42
                                                                                                                           Manuscript submitted to ACM
46                                                                            Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


 [22] D. Beyer, M. Dangl, and P. Wendler. 2018. A Unifying View on SMT-Based Software Verification. J. Autom. Reasoning 60, 3 (2018), 299–335.
      doi:10.1007/s10817-017-9432-6
 [23] D. Beyer, G. Ernst, M. Jonáš, and M. Lingsch-Rosenfeld. 2025. SV-LIB 1.0: A Standard Exchange Format for Software-Verification Tasks. arXiv/CoRR
      2511, 21509 (December 2025). doi:10.48550/arXiv.2511.21509
 [24] D. Beyer, T. A. Henzinger, and G. Théoduloz. 2007. Configurable Software Verification: Concretizing the Convergence of Model Checking and
      Program Analysis. In Proc. CAV (LNCS 4590). Springer, 504–518. doi:10.1007/978-3-540-73368-3_51
 [25] D. Beyer, M. Jankola, and M. Lingsch-Rosenfeld. 2026. Transition Invariants Revisited: Termination Witnesses and Their Validation. 28–53 pages.
      doi:10.1007/978-3-032-32537-2_2
 [26] D. Beyer, M. Jankola, M. Lingsch-Rosenfeld, T. Xia, and X. Zheng. 2025. TransVer: A Modular Program-Transformation Framework for Reduction
      to Reachability. In Proc. SPIN (LNCS 15945). Springer, 1–24. doi:10.1007/978-3-032-06847-7_1
 [27] D. Beyer and S. Kanav. 2022. CoVeriTeam: On-Demand Composition of Cooperative Verification Systems. In Proc. TACAS (LNCS 13243). Springer,
      561–579. doi:10.1007/978-3-030-99524-9_31
 [28] D. Beyer and N.-Z. Lee. 2024. The Transformation Game: Joining Forces for Verification. In Principles of Verification: Cycling the Probabilistic
      Landscape (LNCS 15262). Springer, 175–205. doi:10.1007/978-3-031-75778-5_9
 [29] D. Beyer, N.-Z. Lee, and P. Wendler. 2025. Interpolation and SAT-Based Model Checking Revisited: Adoption to Software Verification. J. Autom.
      Reasoning 69, 1 (2025), 5. doi:10.1007/s10817-024-09702-9
 [30] D. Beyer and M. Lingsch-Rosenfeld. 2025. CPAchecker 4.0 as Witness Validator (Competition Contribution). In Proc. TACAS (3) (LNCS 15698).
      Springer, 192–198. doi:10.1007/978-3-031-90660-2_11
 [31] D. Beyer, S. Löwe, and P. Wendler. 2019. Reliable Benchmarking: Requirements and Solutions. Int. J. Softw. Tools Technol. Transfer 21, 1 (2019), 1–29.
      doi:10.1007/s10009-017-0469-y
 [32] D. Beyer and J. Strejček. 2025. SV-Benchmarks: Benchmark Set for Software Verification (SV-COMP 2025). Zenodo. doi:10.5281/zenodo.15012096
 [33] D. Beyer and J. Strejček. 2026. Evaluating Software Verifiers for C, Java, and SV-LIB (Report on SV-COMP 2026). In Proc. TACAS (2) (LNCS 16506).
      Springer, 461–502. doi:10.1007/978-3-032-22749-2_23
 [34] D. Beyer and J. Strejček. 2026. SV-Benchmarks: Benchmark Set for Software Verification and Testing (SV-COMP 2026, Test-Comp 2026). Zenodo.
      doi:10.5281/zenodo.18650775
 [35] D. Beyer and P. Wendler. 2025. CPAchecker Release 4.2.2 (unix). Zenodo. doi:10.5281/zenodo.17777566
 [36] A. Biere. 2021. Bounded Model Checking. In Handbook of Satisfiability - Second Edition. Frontiers in Artificial Intelligence and Applications, Vol. 336.
      IOS Press, 739–764. doi:10.3233/FAIA201002
 [37] A. Biere, C. Artho, and V. Schuppan. 2002. Liveness Checking as Safety Checking. In Proc. FMICS (ENTSC 66, 2). Elsevier, 160–177. doi:10.1016/S1571-
      0661(04)80410-9
 [38] A. Biere, A. Cimatti, E. M. Clarke, O. Strichman, and Y. Zhu. 2003. Bounded model checking. Advances in Computers 58 (2003), 117–148.
      doi:10.1016/S0065-2458(03)58003-2
 [39] A. Biere, A. Cimatti, E. M. Clarke, and Y. Zhu. 1999. Symbolic Model Checking without BDDs. In Proc. TACAS (LNCS 1579). Springer, 193–207.
      doi:10.1007/3-540-49059-0_14
 [40] A. Biere, T. Faller, K. Fazekas, M. Fleury, N. Froleyks, and F. Pollitt. 2024. CaDiCaL 2.0. In Proc. CAV (1) (LNCS 14681). Springer, 133–152.
      doi:10.1007/978-3-031-65627-9_7
 [41] A. Biere, K. Fazekas, M. Fleury, and M. Heisinger. 2020. CaDiCaL, Kissat, Paracooba, Plingeling and Treengeling Entering the SAT Competition
      2020. In Proc. SAT Competition – Solver and Benchmark Descriptions (Department of Computer Science Report Series B, Vol. B-2020-1). University of
      Helsinki, 51–53. https://tuhat.helsinki.fi/ws/files/142452772/sc2020_proceedings.pdf.#page=50
 [42] A. Biere, N. Froleyks, and M. Preiner. 2024. Hardware Model Checking Competition 2024. In Proc. FMCAD. TU Wien Academic Press, 7–7.
      doi:10.34727/2024/isbn.978-3-85448-065-5_6
 [43] A. Biere, N. Froleyks, and M. Preiner. 2025. Hardware Model Checking Competition 2025. In Proc. FMCAD. TU Wien Academic Press, 7.
      doi:10.34727/2025/isbn.978-3-85448-084-6_6
 [44] A. Biere, K. Heljanko, and S. Wieringa. 2011. AIGER 1.9 And Beyond. Technical Report 11/2. Institute for Formal Models and Verification, Johannes
      Kepler University. doi:10.35011/fmvtr.2011-2
 [45] A. Biere and D. Kröning. 2018. SAT-Based Model Checking. In Handbook of Model Checking. Springer, 277–303. doi:10.1007/978-3-319-10575-8_10
 [46] N. S. Bjørner, A. Gurfinkel, K. L. McMillan, and A. Rybalchenko. 2015. Horn Clause Solvers for Program Verification. In Fields of Logic and
      Computation II - Essays Dedicated to Yuri Gurevich on the Occasion of His 75th Birthday (LNCS 9300). Springer, 24–51. doi:10.1007/978-3-319-23534-9_2
 [47] A. R. Bradley. 2011. SAT-Based model checking without unrolling. In Proc. VMCAI (LNCS 6538). Springer, 70–87. doi:10.1007/978-3-642-18275-4_7
 [48] A. R. Bradley, F. Somenzi, Z. Hassan, and Y. Zhang. 2011. An Incremental Approach to Model Checking Progress Properties. In Proc. FMCAD.
      FMCAD Inc., 144–153. https://dl.acm.org/doi/10.5555/2157654.2157677
 [49] R. Brayton and A. Mishchenko. 2010. ABC: An Academic Industrial-Strength Verification Tool. In Proc. CAV (LNCS 6174). Springer, 24–40.
      doi:10.1007/978-3-642-14295-6_5
 [50] C. Cadar, D. Dunbar, and D. R. Engler. 2008. Klee: Unassisted and Automatic Generation of High-Coverage Tests for Complex Systems Programs.
      In Proc. OSDI. USENIX Association, 209–224. https://dl.acm.org/doi/10.5555/1855741.1855756


Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                                    47


[51] R. Cavada, A. Cimatti, M. Dorigatti, A. Griggio, A. Mariotti, A. Micheli, S. Mover, M. Roveri, and S. Tonetta. 2014. The nuxmv Symbolic Model
     Checker. In Proc. CAV (LNCS 8559). Springer, 334–342. doi:10.1007/978-3-319-08867-9_22
[52] P.-C. Chien and J.-H. R. Jiang. 2019. Time-Frame Folding: Back to the Sequentiality. In Proc. ICCAD. IEEE, 1–8. doi:10.1109/ICCAD45719.2019.8942078
[53] P.-C. Chien and N.-Z. Lee. [n. d.]. CPV Releases. Zenodo. doi:10.5281/zenodo.10063681
[54] P.-C. Chien and N.-Z. Lee. 2024. CPV: A Circuit-Based Program Verifier (Competition Contribution). In Proc. TACAS (3) (LNCS 14572). Springer,
     365–370. doi:10.1007/978-3-031-57256-2_22
[55] P.-C. Chien and N.-Z. Lee. 2026. CPV Release 1.1. Zenodo. doi:10.5281/zenodo.18773927
[56] A .Cimatti and A. Griggio. 2012. Software Model Checking via IC3. In Proc. CAV (LNCS 7358). Springer, 277–293. doi:10.1007/978-3-642-31424-7_23
[57] A. Cimatti, A. Griggio, C. Johannsen, K. Y. Rozier, and S. Tonetta. 2025. Infinite-State Liveness Checking with rlive. In Proc. CAV (1) (LNCS 15931).
     Springer, 215–236. doi:10.1007/978-3-031-98668-0_11
[58] A. Cimatti, A. Griggio, S. Mover, M. Roveri, and S. Tonetta. 2022. Verification modulo theories. Formal Methods Syst. Des. 60, 3 (2022), 452–481.
     doi:10.1007/S10703-023-00434-X
[59] A. Cimatti, A. Griggio, S. Mover, and S. Tonetta. 2014. IC3 Modulo Theories via Implicit Predicate Abstraction. In Proc. TACAS (LNCS 8413). Springer,
     46–61. doi:10.1007/978-3-642-54862-8_4
[60] A. Cimatti, A. Griggio, B. J. Schaafsma, and R. Sebastiani. 2013. The MathSAT5 SMT Solver. In Proc. TACAS (LNCS 7795). Springer, 93–107.
     doi:10.1007/978-3-642-36742-7_7
[61] A. Cimatti, A. Griggio, and S. Tonetta. 2022. The VMT-LIB Language and Tools. In Proc. SMT (CEUR Workshop Proceedings, Vol. 3185). CEUR-WS.org,
     80–89. https://ceur-ws.org/Vol-3185/extended9547.pdf
[62] K. Claessen and N. Sörensson. 2012. A Liveness Checking Algorithm that Counts. In Proc. FMCAD. IEEE, 52–59. https://ieeexplore.ieee.org/
     document/6462555
[63] E. Clarke and D. Kröning. 2003. Hardware verification using ANSI-C programs as a reference. In Proc. ASP-DAC. ACM, 308–311. doi:10.1145/
     1119772.1119831
[64] E. M. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith. 2003. Counterexample-guided abstraction refinement for symbolic model checking. J. ACM
     50, 5 (2003), 752–794. doi:10.1145/876638.876643
[65] E. M. Clarke, D. Kröning, and F. Lerda. 2004. A Tool for Checking ANSI-C Programs. In Proc. TACAS (LNCS 2988). Springer, 168–176. doi:10.1007/978-
     3-540-24730-2_15
[66] L. C. Cordeiro, B. Fischer, and J. Marques-Silva. 2012. SMT-Based Bounded Model Checking for Embedded ANSI-C Software. IEEE Trans. Software
     Eng. 38, 4 (2012), 957–974. doi:10.1109/TSE.2011.59
[67] R. DeLine and R. Leino. 2005. BoogiePL: A Typed Procedural Language for Checking Object-Oriented Programs. Technical Report MSR-TR-2005-
     70. Microsoft Research. https://www.microsoft.com/en-us/research/publication/boogiepl-a-typed-procedural-language-for-checking-object-
     oriented-programs/
[68] D. Dietsch, M. Bentele, M. Ebbinghaus, M. Heizmann, D. Klumpp, A. Podelski, and F. Schüssele. 2025. Ultimate Automizer SV-COMP 2026. Zenodo.
     doi:10.5281/zenodo.17735224
[69] A. F. Donaldson, L. Haller, D. Kröning, and P. Rümmer. 2011. Software Verification Using 𝑘 -Induction. In Proc. SAS (LNCS 6887). Springer, 351–368.
     doi:10.1007/978-3-642-23702-7_26
[70] B. Dutertre. 2014. Yices 2.2. In Proc. CAV (LNCS 8559). Springer, 737–744. doi:10.1007/978-3-319-08867-9_49
[71] S. A. Edwards, T. Ma, and R. Damiano. 2001. Using a hardware model checker to verify software. In Proc. ASICON. IEEE, 85–90. doi:10.1109/ICASIC.
     2001.982504
[72] N. Eén, A. Mishchenko, and R. K. Brayton. 2011. Efficient Implementation of Property Directed Reachability. In Proc. FMCAD. FMCAD Inc., 125–134.
     https://dl.acm.org/doi/10.5555/2157654.2157675
[73] N. Eén and N. Sörensson. 2003. An Extensible SAT-solver. In Proc. SAT (LNCS 2919). Springer, 502–518. doi:10.1007/978-3-540-24605-3_37
[74] S. Falke, F. Merz, and C .Sinz. 2013. The bounded model checker LLBMC. In Proc. ASE. IEEE, 706–709. doi:10.1109/ASE.2013.6693138
[75] J.-C. Filliâtre and A. Paskevich. 2013. Why3: Where Programs Meet Provers. In Programming Languages and Systems. Springer, 125–128. doi:10.
     1007/978-3-642-37036-6_8
[76] X. Fink, P. Berger, and J.-P. Katoen. 2022. Configurable Benchmarks for C Model Checkers. In Proc. NFM (LNCS 13260). Springer, 338–354.
     doi:10.1007/978-3-031-06773-0_18
[77] N. Froleyks, E. Yu, A. Biere, and K. Heljanko. 2026. Certifying Constraints in Hardware Model Checking. In Proc. FM (1) (LNCS 16556). Springer,
     170–188. doi:10.1007/978-3-032-26204-2_9
[78] N. Froleyks, E. Yu, B. Bogaerts, A. Biere, and K. Heljanko. 2026. Liveness Proofs for Hardware Model Checking. In Proc. CAV (3) (LNCS 16684).
     Springer, 3–27. doi:10.1007/978-3-032-32537-2_1
[79] N. Froleyks, E. Yu, M. Preiner, A. Biere, and K. Heljanko. 2025. Introducing Certificates to the Hardware Model Checking Competition. In Proc.
     CAV (1) (LNCS 15931). Springer, 281–295. doi:10.1007/978-3-031-98668-0_14
[80] M. Gario and A. Micheli. 2015. PySMT: A solver-agnostic library for fast prototyping of SMT-Based algorithms. In Proc. SMT.
[81] A. Girardi, A .Bombardelli, A. Griggio, and J. Tomassi. [n. d.]. PyVMT: A Python library to interact with transition systems. Accessed: 2025-10-15.
     https://github.com/pyvmt/pyvmt


                                                                                                                          Manuscript submitted to ACM
48                                                                           Po-Chun Chien, Nian-Ze Lee, Armin Biere, and Dirk Beyer


 [82] A. Goel and K. Sakallah. 2019. Model Checking of Verilog RTL Using IC3 with Syntax-Guided Abstraction. In Proc. NFM. Springer, 166–185.
      doi:10.1007/978-3-030-20652-9_11
 [83] A. Goel and K. Sakallah. 2020. AVR: Abstractly Verifying Reachability. In Proc. TACAS (LNCS 12078). Springer, 413–422. doi:10.1007/978-3-030-
      45190-5_23
 [84] S. Graf and H. Saïdi. 1997. Construction of Abstract State Graphs with Pvs. In Proc. CAV (LNCS 1254). Springer, 72–83. doi:10.1007/3-540-63166-6_10
 [85] A. Griggio and M. Jonáš. 2023. Kratos2: An SMT-Based Model Checker for Imperative Programs. In Proc. CAV. Springer, 423–436.
      ISBN: 978-3-031-37708-2 doi:10.1007/978-3-031-37709-9_20
 [86] A. Griggio and M. Jonáš. 2023. Artifact for the CAV’23 tool paper “Kratos2: an SMT-Based Model Checker for Imperative Programs”. Zenodo.
      doi:10.5281/zenodo.7890411
 [87] D. M. Harris and S. L. Harris. 2007. Sequential Logic Design. In Digital Design and Computer Architecture. Morgan Kaufmann, 103–165.
      ISBN: 978-0-12-370497-9 doi:10.1016/B978-012370497-9/50004-4
 [88] W. H. Harrison. 1977. Compiler Analysis of the Value Ranges for Variables. IEEE Trans. Softw. Eng. SE-3, 3 (1977), 243–250. doi:10.1109/TSE.1977.
      231133
 [89] M. Heizmann, J. Hoenicke, J. Leike, and A. Podelski. 2013. Linear Ranking for Linear Lasso Programs. In Proc. ATVA (LNCS 8172). Springer, 365–380.
      doi:10.1007/978-3-319-02444-8_26
 [90] M. Heizmann, J. Hoenicke, and A. Podelski. 2013. Software Model Checking for People Who Love Automata. In Proc. CAV (LNCS 8044). Springer,
      36–52. doi:10.1007/978-3-642-39799-8_2
 [91] T. A. Henzinger, R. Jhala, R. Majumdar, and K. L. McMillan. 2004. Abstractions from proofs. In Proc. POPL. ACM, 232–244. doi:10.1145/964001.964021
 [92] P.-H. Ho, T. R. Shiple, K. Harer, J. H. Kukula, R. F. Damiano, V. Bertacco, J. Taylor, and J. Long. 2000. Smart Simulation Using Collaborative Formal
      and Simulation Engines. In Proc. ICCAD. IEEE, 120–126. doi:10.1109/ICCAD.2000.896461
 [93] F. Howar, M. Isberner, M. Merten, B. Steffen, and D. Beyer. 2012. The RERS Grey-Box Challenge 2012: Analysis of Event-Condition-Action Systems.
      In Proc. ISoLA (LNCS 7609). Springer, 608–614. doi:10.1007/978-3-642-34026-0_45
 [94] R. Jhala, A. Podelski, and A. Rybalchenko. 2018. Predicate Abstraction for Program Verification. In Handbook of Model Checking. Springer, 447–491.
      doi:10.1007/978-3-319-10575-8_15
 [95] T. Jussila and A. Biere. 2007. Compressing BMC Encodings with QBF. Electronic Notes in Theoretical Computer Science 174, 3 (2007), 45–56.
      doi:10.1016/j.entcs.2006.12.022
 [96] J. C. King. 1976. Symbolic Execution and Program Testing. Commun. ACM 19, 7 (1976), 385–394. doi:10.1145/360248.360252
 [97] T. Lange, M. R. Neuhäußer, T. Noll, and J.-P. Katoen. 2020. IC3 software model checking. Int. J. Softw. Tools Technol. Transf. 22, 2 (2020), 135–161.
      doi:10.1007/S10009-019-00547-X
 [98] C. Lattner and V. S. Adve. 2004. Llvm: A Compilation Framework for Lifelong Program Analysis and Transformation. In Proc. CGO. IEEE, 75–88.
      doi:10.1109/CGO.2004.1281665
 [99] J. Leike and M. Heizmann. 2015. Ranking Templates for Linear Loops. Logical Methods in Computer Science 11, 1 (2015). doi:10.2168/LMCS-11(1:
      16)2015
[100] X. Li. 2025. ESBMC submission for the pre-run of SV-COMP’26. Zenodo. doi:10.5281/zenodo.17741226
[101] J. Long. 2017. Reasoning about High-Level Constructs in Hardware/Software Formal Verification. Ph. D. Dissertation. University of California, Berkeley.
      http://www2.eecs.berkeley.edu/Pubs/TechRpts/2017/EECS-2017-150.html
[102] Z. Lu, P.-C. Chien, N.-Z. Lee, A. Gurfinkel, and V. Ganesh. 2025. Btor2-Select: Machine Learning Based Algorithm Selection for Hardware Model
      Checking. In Proc. CAV (LNCS 15931). Springer, 296–311. doi:10.1007/978-3-031-98668-0_15
[103] J. McCarthy. 1962. Towards a Mathematical Science of Computation. In Information Processing, Proc. DFIP Congress. North-Holland, 21–28.
      Republished at doi:10.1007/978-94-011-1793-7_2.
[104] R. M. McConnell, K. Mehlhorn, S. Näher, and P. Schweitzer. 2011. Certifying Algorithms. Computer Science Review 5, 2 (2011), 119–161.
      doi:10.1016/j.cosrev.2010.09.009
[105] K. L. McMillan. 1993. The SMV System. In Symbolic Model Checking. Springer, 61–85. doi:10.1007/978-1-4615-3190-6_4
[106] K. L. McMillan. 2003. Interpolation and SAT-Based Model Checking. In Proc. CAV (LNCS 2725). Springer, 1–13. doi:10.1007/978-3-540-45069-6_1
[107] K. L. McMillan. 2006. Lazy Abstraction with Interpolants. In Proc. CAV (LNCS 4144). Springer, 123–136. doi:10.1007/11817963_14
[108] H. Mony, J. Baumgartner, A. Mishchenko, and R. Brayton. 2009. Speculative reduction-based scalable redundancy identification. In Proc. DATE.
      IEEE, 1674–1679. doi:10.1109/DATE.2009.5090932
[109] R. Mukherjee, P. Schrammel, D. Kröning, and T. Melham. 2016. Unbounded safety verification for hardware using software analyzers. In Proc.
      DATE. IEEE, 1152–1155. https://ieeexplore.ieee.org/document/7459484.
[110] R. Mukherjee, M. Tautschnig, and D. Kröning. 2016. v2c: A Verilog to C Translator. In Proc. TACAS (LNCS 9636). Springer, 580–586. doi:10.1007/978-
      3-662-49674-9_38
[111] P. Müller, M. Schwerhoff, and A. J. Summers. 2016. Viper: A Verification Infrastructure for Permission-Based Reasoning. In Proc. VMCAI (LNCS 9583).
      Springer, 41–62. doi:10.1007/978-3-662-49122-5_2
[112] A. Niemetz and M. Preiner. 2023. Bitwuzla. In Proc. CAV (2) (LNCS 13965). Springer, 3–17. doi:10.1007/978-3-031-37703-7_1
[113] A. Niemetz, M. Preiner, C. Wolf, and A. Biere. [n. d.]. A generic parser and tool package for the Btor2 format. https://github.com/hwmcc/btor2tools.
      Accessed: 2026-02-14.
Manuscript submitted to ACM
Circuit-Based Program Verification                                                                                                                     49


[114] A. Niemetz, M. Preiner, C. Wolf, and A. Biere. 2018. Btor2, BtorMC, and Boolector 3.0. In Proc. CAV (LNCS 10981). Springer, 587–595.
      doi:10.1007/978-3-319-96145-3_32
[115] M. A. Noureddine and F. A. Zaraket. 2016. Model Checking Software with First Order Logic Specifications Using AIG Solvers. IEEE Trans. Softw.
      Eng. 42, 8 (2016), 741–763. doi:10.1109/TSE.2016.2520468
[116] A. Ozdemir, F. Brown, and R. S. Wahby. 2022. CirC: Compiler infrastructure for proof systems, software verification, and more. In Proc. SP. IEEE,
      2248–2266. doi:10.1109/SP46214.2022.9833782
[117] Á. R. Perez-Lopez, P.-C. Chien, F. Lonsing, S. Archer, A. Irfan, and C. Barrett. 2026. Pono 2.0: A Versatile SMT-Based Model Checker for Safety and
      Liveness (Long Tool Paper). In Proc. FM (LNCS 16557). Springer, 3–26. doi:10.1007/978-3-032-26220-2_1
[118] N. Piterman and A. Pnueli. 2018. Temporal Logic and Fair Discrete Systems. In Handbook of Model Checking. Springer, 27–73. doi:10.1007/978-3-
      319-10575-8_2
[119] A. Podelski and A. Rybalchenko. 2004. A Complete Method for the Synthesis of Linear Ranking Functions. In Proc. VMCAI (LNCS 2937). Springer,
      239–251. doi:10.1007/978-3-540-24622-0_20
[120] A. Podelski and A. Rybalchenko. 2004. Transition Invariants. In Proc. LICS. IEEE, 32–41. doi:10.1109/LICS.2004.1319598
[121] F. Schrögendorfer. 2021. Bounded Model Checking of Lockless Programs. Master’s thesis. Johannes Kepler University Linz. https://resolver.obvsg.at/
      urn:nbn:at:at-ubl:1-45203
[122] M. Sheeran, S. Singh, and G. Stålmarck. 2000. Checking Safety Properties Using Induction and a SAT-Solver. In Proc. FMCAD. Springer, 127–144.
      doi:10.1007/3-540-40922-X_8
[123] J. Slabý, J. Strejček, and M. Trtík. 2012. Checking Properties Described by State Machines: On Synergy of Instrumentation, Slicing, and Symbolic
      Execution. In Proc. FMICS (LNCS 7437). Springer, 207–221. doi:10.1007/978-3-642-32469-7_14
[124] IEEE Computer Society. 2024. IEEE Standard for SystemVerilog–Unified Hardware Design, Specification, and Verification Language. IEEE Std
      1800-2023 (Revision of IEEE Std 1800-2017) (2024), 1–1354. doi:10.1109/IEEESTD.2024.10458102
[125] Y. Su, Q. Yang, Y. Ci, T. Bu, and Z. Huang. 2025. The rIC3 Hardware Model Checker. In Proc. CAV (1) (LNCS 15931). Springer, 185–199. doi:10.1007/978-
      3-031-98668-0_9
[126] Y. Su, Q. Yang, Y. Ci, Y. Li, T. Bu, and Z. Huang. 2025. Deeply Optimizing the SAT Solver for the IC3 Algorithm. In Proc. CAV (1) (LNCS 15931).
      Springer, 237–257. doi:10.1007/978-3-031-98668-0_12
[127] J. Tafese, I. Garcia-Contreras, and A. Gurfinkel. 2023. Btor2MLIR: A Format and Toolchain for Hardware Verification. In Proc. FMCAD. TU Wien
      Academic Press, 55–63. doi:10.34727/2023/ISBN.978-3-85448-060-0_13
[128] Y. Vizel and O. Grumberg. 2009. Interpolation-Sequence Based Model Checking. In Proc. FMCAD. IEEE, 1–8. doi:10.1109/FMCAD.2009.5351148
[129] Y. Vizel, O. Grumberg, and S. Shoham. 2013. Intertwined Forward-Backward Reachability Analysis Using Interpolants. In Proc. TACAS (LNCS 7795).
      Springer, 308–323. doi:10.1007/978-3-642-36742-7_22
[130] H.-E. Wang, T.-L. Tsai, C.-H. Lin, F. Yu, and J.-H. R. Jiang. 2016. String Analysis via Automata Manipulation with Logic Circuit Representation. In
      Proc. CAV (1) (LNCS 9779). Springer, 241–260. doi:10.1007/978-3-319-41528-4_13
[131] T. Wu, X. Li, E. Manino, R. Menezes, M. Gadelha, S. Xiong, N. Tihanyi, P. Petoumenos, and L. Cordeiro. 2025. ESBMC v7.7: Efficient Concurrent
      Software Verification with Scheduling, Incremental SMT and Partial Order Reduction (Competition Contribution). In Proc. TACAS (3) (LNCS 15698).
      Springer, 223–228. doi:10.1007/978-3-031-90660-2_16
[132] Y. Xia, A. Cimatti, A. Griggio, and J. Li. 2024. Avoiding the Shoals - A New Approach to Liveness Checking. In Proc. CAV (1) (LNCS 14681). Springer,
      234–254. doi:10.1007/978-3-031-65627-9_12
[133] Zs. Ádám, P. Ayaziová, L. Bajczi, D. Beyer, M. Jankola, M. Lingsch-Rosenfeld, and J. Strejček. 2025. Non-termination Witnesses and Their Validation.
      In Proc. ASE 2025. IEEE, 1969–1981. doi:10.1109/ASE63991.2025.00164




                                                                                                                           Manuscript submitted to ACM
