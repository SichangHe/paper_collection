                                              AutoINV: Automated Invariant Generation
                                           Framework for Formal Verification on High-Level
                                                         Synthesis Designs
                                                        Xiaofeng Zhou∗ , Linfeng Du∗ , Guangyu Hu∗ , Sharad Sinha† , Hongce Zhang§ , Wei Zhang∗
                                             ∗
                                                 The Hong Kong University of Science and Technology, Hong Kong, † Indian Institute of Technology Goa, Goa, India
                                                             §
                                                               The Hong Kong University of Science and Technology (Guangzhou), Guangzhou, China
                                                   {xzhoubu, linfeng.du, ghuae}@connect.ust.hk, eeweiz@ust.hk, sharad@iitgoa.ac.in, hongcezh@hkust-gz.edu.cn


                                            Abstract—High-level synthesis (HLS) transforms an algorith-          a proof ensuring that a certain target assertion always holds
arXiv:2604.22285v1 [cs.AR] 24 Apr 2026




                                         mic description of hardware from a higher abstraction (e.g.,            in the design, regardless of inputs. They can also output a
                                         C/C++) into a register-transfer level (RTL) design, offering            counterexample trace if any states violating the assertion can
                                         reduced development time and greater flexibility in design space
                                         exploration. However, such machine-generated RTL designs may            be reached with a certain sequence of input values. Popular
                                         contain major functional bugs or security vulnerabilities due to        model checking algorithms include the K-induction algorithm,
                                         limitations or errors in the HLS tools. One of the most reliable        Binary-Decision-Diagram-based model checking, and IC3 [3],
                                         methods to identify these vulnerabilities is formal verification,       which was later developed into the Property-Directed Reach-
                                         particularly model checking. Nevertheless, the large size of the        ability (PDR) algorithm [4]. We refer to this commonly used
                                         generated RTL often causes model checking to struggle to
                                         conclude within reasonable time or resource limits.                     model checking algorithm as the IC3/PDR algorithm in the rest
                                            In this study, we propose utilizing the high-level design features   of the paper. In this work, we will perform hardware formal
                                         from the HLS flow to construct a set of helper assertions aimed         verification on HLS designs using the IC3/PDR algorithm due
                                         at guiding the model checker and accelerating the verification          to its efficiency and potential for optimization and exploration.
                                         process. To identify the most effective set of helpers to assist the       Although model checking is an effective method for
                                         model checker, we develop a proving mechanism that iteratively
                                         reuses proving information to select the potentially most useful        detecting potential bugs and producing guarantees, it often
                                         set of helpers.                                                         encounters scalability issues known as the state space
                                            We evaluate the proposed framework on a set of HLS                   explosion. When the number of registers in the RTL design
                                         design benchmarks. Experimental results demonstrate that, when          is substantial or the transition relation becomes complex,
                                         compared to vanilla model checking, our approach achieves a             model checking algorithms struggle to derive a proof within
                                         speedup of up to 6.05×, and 2.23× on average.
                                            Index Terms—Model Checking, High-level Synthesis.                    a reasonable timeframe.
                                                                                                                    To alleviate the computational burden of model checking
                                                                I. I NTRODUCTION                                 caused by the aforementioned state space explosion problem,
                                            High-level synthesis (HLS) tools accelerate digital circuit          one approach is to extract notable facts from the design as
                                         development by compiling functions written in high-level                helpers to aid the verification process. As an example, the
                                         programming languages, such as C and C++, into register-                study in [5] identified a set of potential facts of designs and
                                         transfer level (RTL) descriptions. Although HLS tools have              expressed them as RTL assertions. Once proved, these asser-
                                         been well-studied in terms of performance optimization and              tions can serve as assumptions that constrain the state space
                                         design space exploration (DSE), recent studies [1], [2] indi-           when verifying the property specification under examination.
                                         cate that commonly used HLS tools are likely to introduce                  The state explosion problem becomes increasingly trou-
                                         functional and security vulnerabilities into the generated RTL          blesome, particularly when checking RTL code generated by
                                         designs. Consequently, there is a growing need to verify the            HLS tools. This code contains not only user-defined software
                                         correctness and safety of RTL designs generated by HLS tools.           functionalities but also scheduling information produced by
                                            Hardware formal verification is a viable option for                  HLS tools. Unfortunately, limited efforts have been made
                                         verification. Unlike hardware testing, which provides only              to alleviate the computational burden of hardware formal
                                         limited guarantees depending on the coverage of test cases,             property verification on HLS designs. While it is possible for
                                         hardware formal verification mathematically proves whether              a verification engineer to manually extract and write helpers
                                         a property specification in hardware design holds or not. A             to assist the model checking process in small RTL designs,
                                         common practice in hardware formal verification is SAT-based            the scale of RTL code in HLS designs is usually large (≥1K
                                         model checking. SAT-based model checking algorithms, built              lines of Verilog code) and often incomprehensible to human
                                         upon SAT solvers, attempt to establish a proof that guarantees          engineers, especially those without hardware expertise.
                                         a property specification holds in an RTL design by solving                 In this work, we design an automated helper generation
                                         a sequence of SAT problems. These algorithms can produce                framework named AutoINV to assist in model checking of
                                                                                                                 property specifications in HLS designs without any limitations
on either design or property specification. There are two main       mine [11], [12], [13] learns assertions from simulation traces.
challenges addressed by this framework: first, how to extract        They rank assertions by coverage. The work HARM [14] pro-
high-quality helpers that best assist the verification process of    vides the user with a more flexible assertion generation scheme
the targeted property specification; and second, once we derive      with a wider range of operators supported. AssertLLM [15]
a large set of helpers, how to identify the most effective subset    utilizes large language models to generate assertions based on
that introduces the least overhead in checking.                      specifications written in natural language. LFPS [5] uses RTL
   To address the first challenge, we design an extraction           templates to generate helper assertions.
method that identifies common HLS design features and uses              The helper generation in AutoINV can be viewed as
these features to generate helpers. This method is implemented       hardware property mining, but existing techniques do not
as the AutoINV Helper Generator in the AutoINV framework.            directly apply. Prior work mainly mines assertions to improve
For the second challenge, we propose a novel verification            coverage, whereas we mine helpers that accelerate proving a
method that dynamically selects the most promising helpers           given target property. Moreover, most methods assume human-
based on previous proving trials of the target property. This        written RTL; HLS designs are much larger, making the helper
method is implemented in the AutoINV Helper Ranker module            search space far bigger and thus expensive to explore with for-
and the AutoINV Prover module.                                       mal guarantees. Finally, many approaches are template-based,
   In summary, this paper makes the following contributions:         but general templates do not capture the recurring patterns in
   • We automate the generation of high-quality helpers for          HLS-generated logic effectively. Among prior works, [16] is
      formal verification of HLS designs. Specifically, we iden-     the closest: it generates invariants to speed up reasoning about
      tify the common hardware patterns in HLS design and            handshake signals in dynamically scheduled HLS designs. In
      derive a template-free helper generation method that takes     contrast, our work targets verification-time acceleration for
      advantage of these patterns.                                   general property checking, rather than design-time optimiza-
   • We develop an effective helper selection mechanism to           tion for a narrow class of handshake/control properties.
      identify promising helpers that assist the verification pro-   Property Ordering/Ranking. Several studies use statistical
      cess based on both information from RTL design structure       information to speed up model checking across many proper-
      and timeout trials. Unlike black-box approaches such as        ties. Works such as [17], [18] cluster similar properties using
      deep learning models, our method does not require time-        circuit structure and distribute them to different engines based
      consuming data collection and training processes.              on estimated difficulty. PURSE [19] further uses IC3/PDR
   • We have developed a framework, named AutoINV, for               runtime statistics to dynamically schedule property proving. In
      accelerating formal verification tasks in HLS designs,         contrast, our work targets improving the proof of a single prop-
      significantly reducing the proving time. Compared to           erty and exploits characteristics of HLS-generated designs.
      vanilla model checking, our framework achieves an aver-
                                                                                            III. BACKGROUND
      age speedup of 2.23×.
   The remainder of this paper is organized as follows: Section      A. IC3/PDR Algorithm
II reviews related works. Section III presents the background           An RTL design is modeled as a state transition system
of the IC3/PDR algorithm and the AutoINV framework.                  ⟨V, Tr (V, V ′ ), INIT (V )⟩, where V = {vi } are Boolean
Section IV describes the motivation for developing our frame-        variables (registers and inputs), INIT (V ) characterizes the
work. Section V details the functioning of each component            initial states, and Tr (V, V ′ ) is the one-cycle transition relation
in our framework. Section VI presents the experimental re-           with V ′ denoting next-state variables.
sults obtained from a set of benchmarks to demonstrate the              Given a safety property P (V ), IC3/PDR checks whether a
effectiveness of our framework.                                      violating state ¬P (V ) is reachable (a bad state). The algorithm
                                                                     incrementally learns CNF clauses (disjunctions of literals such
                     II. R ELATED W ORKS
                                                                     as v or ¬v) to block bad states while maintaining an over-
Equivalence checking of HLS-generated designs.                       approximation of reachable states; these clauses are also the
Vericert [6], [7] is a formally proved HLS tool that generates       unit reused by clause side-loading in later sections.
RTL from C while maintaining functional consistency. The                A proof of safety is an inductive invariant INV (V ) satisfy-
work in [8] presents KAIROS, a tool to verify the equivalence        ing Formula 1. IC3/PDR constructs such an invariant through
of RTL implementations generated under different HLS direc-          a sequence of frames [F0 , F1 , . . . , FN ], where each Fi is a
tives. The work SE3 [9] checks for non-cycle-accurate equiv-         conjunction of learned clauses and F0 ≡ INIT (V ). The
alence between two HLS designs. These methods are limited            frames are maintained to satisfy Formula 2. The algorithm
to equivalence checking scenarios, while this paper considers        converges when it finds N such that FN +1 → FN ; together
accelerating general model checking problems on HLS-                 with FN → FN +1 implied by the first constraint in Formula 2,
generated designs with no restrictions on the property to check.     this yields a fixed point FN ≡ FN +1 , and FN serves as an
Hardware Property Generation/Mining. Hardware property               inductive invariant proving P .
mining is a process to mine possible properties from RTL                IC3/PDR alternates two subroutines. Strengthen searches for
designs. For example, IODINE [10] constructs possible asser-         counterexamples to the current frames (e.g., a bad state or a
tions by analyzing simulation traces with fixed patterns; Gold-      state violating the consecution constraint in Formula 2) and
refines the frames by adding blocking clauses; if the violation                2
                                                                                V
                                                                                                    2
                                                                                                     V

can be traced back to F0 , a real counterexample trace is                                                                 Clause from high-
                                                                                                                          level knowledge
reported. Propagate attempts to push learned clauses forward                INV(V)               INV’(V)                   Clause from
to later frames whenever allowed by Formula 2; successful
                                                                                                                           model checker
propagation helps reach the convergence condition.
                                                                   Fig. 1: Comparison of finding an inductive invariant without
             INIT (V ) → INV (V )
               INV (V ) ∧ Tr (V, V ′ ) → INV (V ′ )         (1)     or with constraints obtained from high-level design insights.
               INV (V ) → P (V )
            
                                                                   goal is to find an execution trace that drives ap_done, which
              Fi (V ) → Fi+1 (V )                                  indicates the hardware finishes execution, to 1 (PDR returns a
                Fi (V ) ∧ Tr (V, V ′ ) → Fi+1 (V ′ )        (2)
                                                                    witness trace if reachable). However, due to the requirement
                Fi (V ) → P (V )
             
                                                                    of thousands of state transitions to reach the completion state,
B. Clause Side-loading                                              the IC3/PDR algorithm must construct numerous frames to
   Clause side-loading is a technique implemented in                determine state reachability.
DeepIC3 [20] to equip the model checking algorithm with                By examining the source code and HLS reports produced
a potentially better starting point on F1 , where the IC3/PDR       from the HLS tool, it is evident that the upper bound of
algorithm starts. These clauses are checked before loading onto     the loop variable is 1000. This high-level constraint can be
F1 to ensure their correctness. The loaded clauses can provide      incorporated into a helper assertion: assert (i_reg ≤
an initial constraint to the state space and influence the choice   1000). The proof of helper takes 0.07 seconds and results
of bad states made by the SAT solver, potentially guiding           in an inductive invariant containing 4 clauses. These clauses
the proof search of the IC3/PDR algorithm into a “better”           are side-loaded to the proving process of the target property,
direction. These clauses will also be loaded to later frames        enabling the IC3/PDR algorithm to find a trace leading to the
automatically by the propagate procedure of the IC3/PDR             ap_done signal 1.19× faster, with only 60.6% of the frames
algorithm, forming a stronger guarantee in the proving process      constructed, as demonstrated in the right part of Figure 2.
of the target property. In DeepIC3, the authors showed the                                                     4




                                                                                                                                            Number of frames
                                                                    #define N 1000                                                      200
effectiveness of side-loading high-quality clauses by directly      void top(int a[N],




                                                                                                         Time(s)
picking up clauses from the inductive invariant and observing           int b[N],int c[N])                     2                        100
a speed-up in the verification process.                                 for (int i=0;i<N;i++)
                                                                    #pragma HLS pipeline
   In this paper, we will also use the side-loading technique to                                               0                        0
                                                                            c[i]=a[i]+b[i];                        w.            w.o.
load the clauses from the inductive invariants generated from                                                           Method
proving helpers with the IC3/PDR algorithm. In our method,          Fig. 2: Comparison of verification performance with and
we expect the convergence of proving the target property can        without Helper on the vector addition example.
benefit from the clauses associated with the helpers.
                                                                               V. P ROPOSED F RAMEWORK : AUTO INV
                       IV. M OTIVATION
                                                                       In this section, we provide a detailed explanation of the
   The verification process of the IC3/PDR algorithm                AutoINV framework. An overview of AutoINV is depicted
fundamentally revolves around identifying an inductive              in Figure 3. The framework accepts an HLS project directory
invariant INV (V ) that effectively distinguishes reachable         and a user-defined target property written in SystemVerilog
states from undesirable states. As previously discussed, the        Assertion (SVA) as inputs. The output of AutoINV is a proof
complexity of a design can significantly increase the time          or a counterexample trace violating the target property. When
required to discover an inductive invariant within a reasonable     AutoINV runs out of time, the output will be unknown. The
timeframe. This challenge can be likened to sculpting a             HLS project directory is required to contain both the HLS
massive statue from a large block of stone using a small            compilation report and the compiled HLS design in RTL.
chisel. This analogy is depicted in the left rectangle of Figure    As previously introduced, AutoINV contains three parts:
1, where the black lines represent the clauses generated by         AutoINV Helper Generator generates helper assertions from
the model checker, which constrain the state space 2V .             analysis of RTL codes and high-level information of the design
   To mitigate this issue, incorporating constraints based on       in HLS reports. AutoINV Helper Ranker ranks the helper
high-level knowledge into the search space beforehand is akin       assertions by importance according to the proving information
to an experienced sculptor using a power cutter to remove           from past trials. AutoINV Prover iteratively picks up the
unnecessary portions of the stone initially. This approach          most significant helper assertion. It first checks the helper’s
reduces the space required to identify the inductive invariant,     validity. Then, it side-loads the clauses derived from the helper
as illustrated by the right rectangle in Figure 1, where the        checking into the proving procedure of the target property.
brown lines eliminate a substantial portion of the state space,
thereby significantly alleviating the burden on model checkers.     A. AutoINV Helper Generator
   Below is a motivating example. Consider a simple vector            In the AutoINV Helper Generator, we identify and extract
adder written in C++, as shown in the left part of Figure 2. Our    helper properties from the characteristic design patterns of
                                                                                                           Comb.                            Comb.
    C++ Code    HLS Tool           HLS Dir          Target Property                    D      Q
                                                                                                            Logic
                                                                                                                            D      Q
                                                                                                                                             Logic
                                                                                                                                                             D     Q
                                                                                        enable                               enable                           enable
       AutoINV Helper Generator                          Yosys                           En.st.1                            En.st.2                           En.st.3
            Static Analysis                                                              Ex.st.1                             Ex.st.2                          Ex.st.3
                                                    AutoINV Prover
      SW-GEN                HW-GEN                                                    clock                                        clock
                                             unknown
                                                       IC3/PDR        * Output:      En.St.1                                      Ex.St.1
                                                                      (1) Proof      En.St.2                                      Ex.St.2
                                                ckp                                  En.St.3                                      Ex.St.3
            Helper assertion set                                      (2) Cex                  000 110              011                              000   100 111
                                                                      (3) Unk                    100 111              001                                    110
         AutoINV Helper Ranker                           Clause
                                             If fail   Transform                  Fig. 4: A simplified diagram of pipeline behavior in HLS
            Helper Analysis                  cex
                      Helper COI             unknown
                                                                                  designs during one execution of a loop. En.st.i and Ex.st.i
      CTI-guided Helper Evaluation           Best
                                                       IC3/PDR                    represent the control registers for enabling and the exit con-
                           CTI statistics from last proving                       dition at stage i, respectively.
       Static Analysis       CTI-guided Analysis       External Tools
                  User Input            Clause Manipulation
                                                                                  the helper from FSM can be written as one-hot encoding,
Fig. 3: AutoINV framework overview. SW-GEN and HW-                                where F SMi represent the i-th bit in the FSM registers. Since
GEN represent the software helper assertion generator and                         FSM is the pump that drives the behavior of other modules,
hardware helper assertion generator, respectively.                                the clauses in the IC3/PDR algorithm are likely to contain
                                                                                  literals referring to the FSM registers. The one-hot constraints
HLS-generated hardware, with particular emphasis on control                       for FSM could remind the IC3/PDR algorithm of the one-hot
signals. These control signals exhibit highly consistent patterns                 state transition constraints of FSM.
and are typically encoded with less optimization than manually                       (C) Pipeline: In HLS designs, pipeline is a common
crafted RTL codes. In this work, we focus on identifying and                      structure to parallelize software loops in hardware execution
leveraging these recurring signal patterns to extract effective                   [21], [22], [23]. In a pipeline, the loop body in software is
helper properties.                                                                divided into several stages. During the execution, each stage
   The extraction process employs a pattern recognition ap-                       processes a different part of the loop iteration, allowing for
proach that analyzes control signal relationships within the                      parallel execution and improved performance. The execution
generated hardware. This approach does not necessitate perfect                    of each stage in HLS loops is controlled by two registers: one
correctness in helper generation; when a proposed helper fails                    represents whether the stage is enabled, and another stores the
verification, it is eliminated, allowing AutoINV to proceed                       calculated exiting condition for the stage.
with alternative helper candidates without compromising over-                        Owing to the nature of loop execution, the stages in the
all verification correctness.                                                     pipeline are enabled sequentially, and the satisfaction of the
   The AutoINV Helper Generator primarily focuses on                              exiting condition for each stage is propagated sequentially
two principal categories of properties as potential helpers:                      accordingly through the stages. If we draw the behavior
hardware-related properties, which examine structural charac-                     pattern of those stage control registers using a waveform,
teristics of the implementation, and software-related proper-                     Figure 4 illustrates a simplified diagram of three execution
ties, which derive from the behavioral specifications of the                      stages inside the pipeline, which is accompanied by the two
original algorithm.                                                               sets of control registers that represent the execution status of
   Hardware-related helpers are generated from concise yet                        each stage. The waveform at the bottom of Figure 4 shows
expressive facts in hardware using a rule-based design behav-                     all possible behavioral patterns of control registers among the
ior characterization method. In this method, we mainly explore                    three pipeline stages. We can thus summarize the following
the behavioral pattern of three common design components in                       rules: For both sets of pipeline exiting conditions and stage
HLS designs: FIFO, FSM, and Pipeline.                                             enabling registers, at most one register can be flipped in one
   (A) FIFO: The control part of FIFO in HLS designs                              cycle. Meanwhile, the register that is going to be flipped
is implemented with three groups of state registers: two                          must follow a monotonic increasing or decreasing order.
indicating whether the FIFO is full or empty, and one                                Software-related helpers are mostly extracted from the
representing the pointer to the data part. The data storage is                    software execution order defined in the input C++ code.
implemented as either a shift register or a memory. We use                        Although HLS tools enable parallelization by mapping the
the following rules to generate helpers regarding FIFO: When                      input sequential software to hardware, certain execution
the pointer inside FIFO is not at its reset value, the FIFO is                    orders should be kept owing to the inherent dependencies.
not empty; When the pointer is not equal to the FIFO depth                        Such an execution order can be reflected in the behavioral
parameter, the FIFO is not full; the pointer of data storage                      pattern of control signals. However, not all execution orders
should not exceed the FIFO depth; The FIFO should not be                          can be converted to helpers that can be mined. For example,
empty and full at the same time.                                                  the execution order inside a loop body that contains an
   (B) FSM: For the sake of speed and power consumption                           addition followed by a multiplication is already guaranteed
of the generated designs, usually the FSM registers of each                       by the structure of the circuit: the output of the multiplier
module inside HLS designs are one-hot encoded. As a result,
is connected to the input of the adder, shown in Figure                    consider a typical block-level control interface in HLS designs.
5a. In such a case, no control signals are involved, and the               It consists of four signals: (1) an input start signal that starts
information of such an order cannot constrain the state space              the execution of a module (2) an output done signal indicating
of the design. As a result, we only consider the execution                 that the module finishes execution, (3) an output idle signal
order of loops and functions that are directly controlled by               indicating that the module is currently idle (4) an output ready
registers on the control path. In this work, we mine helpers               signal indicating that the module is ready to receive another
from the coarse-grained execution order in HLS designs,                    group of data for processing. Similar to the execution order
namely loop-level helpers and function-level helpers.                      of loops, when a function is executed before another function,
   Loop-level helpers are helpers generated from the                       the block-level control interface will present a constrained
execution order of loops. Figure 5b illustrates a simple                   behavior regarding the execution order. A general behavior
example: the input of instructions in loop TASK2 is dependent              pattern of such a control interface influenced by the execution
on the results of loop TASK1, and both loops are pipelined.                order is shown in Figure 5c. In this case, the function FUNC1
From the waveform of control registers for each loop, we                   is executed before the function FUNC2; the block-level control
can observe that the stage enable register in TASK2 will not               interface shows the following patterns in the waveform: the
be set until the corresponding enable register in TASK1 is                 change of block-level control signal value of FUNC2 is later
reset, indicating that loop TASK1 finishes the execution. For              than that of FUNC1 and generally follows the same pattern.
general cases, if any pair of loops are executed one after the                Loop variable helpers are helpers generated when a loop
other, we can derive a logic implication between the control               has a fixed number of trip-count and is reflected directly from
signals: If TASK1 execute before TASK2, the set of enable                  the loop variable. Such a constraint, although unrelated to the
registers in TASK2 implies the reset of enable registers of                execution order, is an important part of the helper set. Ri is
TASK1. Similarly, for the registers that store exit condition              the set of possible values of the loop variable in the i-th loop
for those loops, such an implication can be derived as well.               in the design.
                                                                           B. AutoINV Helper Ranker
                                         c
 void top(...) {
     int a = b * c;
                                         b
                                                      ×   a
                                                              +    d
                                                                              In our method, we use clause side-loading to accelerate
     int d = a + b; }                                                      model checking. However, not all clauses side-loaded into the
 (a) Instruction execution order reflected in hardware implementa-
                                                                           proof engine lead to a quicker convergence of the IC3/PDR
 tion.                                                                     algorithm. Some unrelated side-loaded clauses potentially lead
                                                                           the algorithm in an undesired direction or cause extra costs
                                                                           when propagating them to higher levels. For example, in a
void top(...) {                                                            simple equivalence checking task of different implementations
                                                   TASK1
    int m[N];
                                      Data Depdendency
                                                                           of bit-wise XOR operation for two bit vectors, side-loading
    TASK1: for (...) {
#pragma HLS pipeline
                                                                           clauses naively without proper filtering may cause perfor-
    /* compute and                                                         mance degradation even if the clauses are from the inductive
       write to m */}                                                      invariant of exactly the same property. This is shown by our
    TASK2: for (...) {                             TASK2
#pragma HLS pipeline            clock
                                                                           experimental results in Figure 6. When side-loading 10%, 20%
    /* read from m      TASK1.En.St.1                                      or 40% clauses from inductive invariants, the checking time
       and compute */}} TASK1.En.St.2
                        TASK1.En.St.3                                      for the target property and the number of frames constructed
                                      TASK2.En.St.1                        for the IC3/PDR algorithm are actually worse than the case
                                      TASK2.En.St.2
                                      TASK2.En.St.3                        without side-loading. What’s more, compiling and verifying
  (b) Loop execution order reflected in hardware implementation.           hundreds of helpers formally with the IC3/PDR algorithm
void top(...) {                           clock                            could also be costly. Therefore, it is necessary to filter the
    FUNC1(...);                     FUNC1.Start                            set of helper assertions and only keep a subset of helpers ben-
    FUNC2(...);                      FUNC1.Idle
    FUNC3(...);}
                                    FUNC1.Done                             eficial to the proving process of the target property. However,
                                   FUNC1.Ready
                                    FUNC2.Start                            as is mentioned in Section I, it is hard to select an optimal
                                     FUNC2.Idle
   FUNC1
              top
             FUNC2         FUNC3
                                    FUNC2.Done                             subset of helper assertion candidates produced by the AutoINV
                                   FUNC2.Ready
           Control logic                    FUNC1 ends        FUNC2 ends   Helper Generator owing to an exponential number of possible
                                                                           combinations. We propose to derive a beneficial subset of
(c) Function execution order reflected in hardware implementation.         helper assertions using preliminary trials when proving the
Fig. 5: Execution order reflected in hardware implementation.              target assertion. Specifically, we extract internal prover infor-
                                                                           mation related to counterexample-to-induction (CTI) (detailed
   Function-level helpers are helpers generated from the                   later) to evaluate the helpers. Such information in those trials
execution order of functions. These software functions are                 reveals what the IC3/PDR algorithm is struggling with and
implemented as hardware modules in the generated RTL code                  is, therefore, meaningful for helper evaluation. Based on this
from HLS tools. The function-level helpers are extracted from              information, we construct an evaluation metric to rank the
the block-level control interface functions. In this work, we              helper assertions by their potential benefits.
                                                                                   Algorithm 1 AutoINV Prover
                                                                                    1: Input: AutoINV Helper Ranker object, the design under verification At
                                                                                       in AIG.
                     Performance degradation                                        2: Parameters: α, T0 , Th , Nh
                     in naive side-loading                                          3: Output: The proving result of the target property
                                                                                    4: T ← T0 ; ckp ← []
                                                                                    5: pdr result ← pdr(At , T, ∅, ckp)
                                                                                    6: if pdr result.is proved() ∨ pdr result.is cex() then
Fig. 6: Performance     degradation in naive clause side-loading.
              Helper: h = f(v , v )                                                 7:     return pdr result
                                 1   2               Score = 35
                v2                                                                  8: end if
                                                    v2
                                         r1                                         9: while True do
                                                                                   10:     Hj ← ranker.get best helpers(pdr result, Nh )
                                              r2                                   11:     Cj ← ∅
                 v1                                 v1
                                                                                   12:     while Hj ̸= ∅ do
                                               r3                                  13:         hj,k ← an element in Hj
                                                    r4                             14:         Hj ← Hj \ hj,k
                                                             r1    10              15:         Aj,k ← Compile(hj,k , At )
                                 CTI1 = r1 ∧ r2 ...         r2     20
                                                            r3      5              16:         pdr result helper ← pdr(Aj,k , Th , ∅, [])
      safe: target               CTI2 = r2 ∧ ¬r4 ...        r4     10
                                                            r5
                                                                                   17:         if not pdr result helper.is proved() then
                      unsafe ...                                    1
                                                     Number of occurrence in CTI
                                                                                   18:             Hj ← Hj ∪ ranker.get best helpers(pdr result, 1)
       IC3/PDR algorithm                                                           19:         else
                                                                                   20:             Ihj,k ← pdr result helper.get ind inv()
      Fig. 7: The workflow of AutoINV Helper Ranker.                               21:             Chj,k ← Translate(Ihj,k , Aj,k , At )
                                                                                   22:             Cj ← Cj ∪ Chj,k
   In the bottom left of Figure 3, AutoINV Helper Ranker                           23:         end if
takes as input the helper assertion set from AutoINV Helper                        24:     end while
                                                                                   25:     pdr result ← pdr(At , T, Cj , ckp)
Generator and the proving information from the last timeout                        26:     if pdr result.is proved() ∨ pdr result.is cex() then
trial. It provides a set of helper assertions with top scores                      27:         return pdr result
once the downstream AutoINV Prover is asking for. AutoINV                          28:     end if
                                                                                   29:     ckp ← pdr result.get checkpoint()
Helper Ranker evaluates a helper assertion in two steps: first,                    30:     T ← αT
it utilizes the static information in the RTL code to analyze                      31: end while
the helper assertion under evaluation; second, it employs the
dynamic information from the last timeout proving trial on
the target property to rank the priority of using the helper                       node u that appears in all CTIs in the last trial.
assertions. The details are shown in Figure 7.                                     C. AutoINV Prover
   In the first step, we find the set of registers and inputs that
are located in the transitive fan-in (TFI) cone of variables in                       AutoINV Prover is shown in the right part of Figure 3. It
the assertion hi . In the netlist of the circuit under verification,               iteratively takes helpers and outputs the checking result of
TFI of a variable represents the set of nodes from which there                     the target property. The core of AutoINV Prover is a proof
exists a path in the netlist from the node to the variable.                        engine implementing the IC3/PDR algorithm with checkpoint
Subsequently, we collect all registers and inputs found in the                     functionality, and it is responsible for proving helper assertions
TFI cone as the set Rhi .                                                          and the target property. The algorithm takes RTL design and
   After AutoINV Helper Ranker derives Rhi , it then                               the target property in and-inverter graph (AIG). The behavior
evaluates the benefit of the helper to the upcoming proving                        of AutoINV Prover is defined by hyperparameters including
process based on the proving information of the previous trial.                    the number of helper assertions taken from AutoINV Helper
Here, we perform the evaluation based on CTI. In IC3/PDR,                          Ranker each time, denoted as Nh ; the Timeout limit of the
a CTI (counterexample to induction) is a cube that falsifies                       initial proving trial T0 ; The growth rate of proving timeout
the inductiveness of a candidate invariant at some frame by                        limit α; and the Timeout limit of proving helper assertion
exhibiting a predecessor that can transition to a violating                        Th . Details are provided in Algorithm 1.
state. When a CTI is encountered, the IC3/PDR algorithm will                          In Algorithm 1, AutoINV Prover first launches an initial
start refining existing frames to block the CTI. As inductive                      trial of prove engine with timeout limit T0 , as is shown in Line
invariants are generated piece by piece by blocking the CTIs,                      5. Function pdr(·) is a single call of IC3/PDR prove engine,
we center our evaluation method around CTIs and try to                             function arguments includes AIG of design and the target
pick out helpers that possibly best assist in blocking CTIs. In                    property under verification, timeout limit, side-loaded clauses,
AutoINV Helper Ranker, we use the number of occurrences                            and checkpoint of the previous timeout trial. Checkpoint
of each variable in all CTIs encountered in the last proving                       records clauses in the frames that are already constructed each
attempt to calculate the score of helper hi , denoted as Mhi .                     time pdr(·) finishes the construction of a frame. The clauses
Such a number of occurrences reflects the potential benefit                        learned from helper assertions are loaded onto the first frame.
of using a helper to constrain the variable. We sum these                          The IC3/PDR algorithm will attempt to push the side-loaded
numbers of occurrences to get the score Mhi . In this equation,                    clause to higher frames in the propagation stage. If the target
fv (u) represents the frequency of the variable associated with                    property is simple enough to derive a result within time T0 ,
                                                                                   AutoINV can directly return the proving result without any
overhead of generating and evaluating the helper assertions.                      TABLE I: The scale of benchmarks.
If the initial trial fails to derive any result within the timeout           vac-e vsc-e mac-e autosa-mm-f [26] autosa-cnn-f [26]
limit, the IC3/PDR algorithm will terminate once the current             AND 1468 1528 1781 11164               20821
                                                                         FF  204 213 242       1388             2941
frame finishes construction. A checkpoint is dumped together             LOC 1834 1454 2524 15925               25086
with other related proving information.
   After the initial trial, the algorithm reaches the main loop      vac-e, vsc-e, mac-e, autosa-mm-f, and autosa-cnn-f. In the
from line 9 to line 31. Inside the j-th iteration, we first pick     experiment, we will first tune the hyperparameters of the
up the Nh helper assertions with highest scores as Hj =              AutoINV Prover using vac-e (Functional consistency of
{hj,1 , hj,2 , · · · , hj,Nh } from AutoINV Helper Ranker (Line      vector accumulators), vsc-e (Functional consistency of vector
10). Yosys is used to compile every hj,k in Hj into AIG format       accumulators), and mac-e (Functional consistency of MAC
with the design under verification. Line 15 compiles the helper      elements), shown in Section VI-D. Subsequently, we will
assertion into the corresponding AIG Aj,k . Next, in Line 16,        use the optimal hyperparameter configuration to evaluate
AutoINV Prover calls pdr(·) to verify the helper assertion           the AutoINV framework on autosa-mm-f and autosa-cnn-f
within time Th . If the pdr(·) function returns the helper to        (FIFOs have no block in AutoSA-MM and AutoSA-CNN),
be incorrect or unknown within time Th , it is abandoned             which are two large-scale, real-world HLS designs generated
and the AutoINV Helper Ranker will provide another set of            by the AutoSA [26] framework.
promising helpers (Line 18). Once hj,k is proved, we can get            The resource consumption and RTL code size of the bench-
an inductive invariant Ihj,k (Line 20), which contains a set of      marks are reported in Table I. The resource consumption is
clauses learned from hj,k .                                          detailed in the first and second rows of the table, indicating the
   Before feeding the learned clauses into the pdr(·) function,      number of AND gates and flip-flops in the AIG that feed into
it is required to pass a translation phase since the AIG that        the IC3/PDR algorithm. This reflects the scale of properties
was used to prove hj,k is different from the AIG used to             after abstraction. The third row presents the lines of code in
prove the target assertion. It is implemented in Function            each RTL design. From these statistics, it is evident that the
Translate(·) via variable name mapping. The translated               benchmarks are too complex in code size to perform manual
inductive invariants are marked as Chj,k (Line 21). The set of       helper extraction.
clauses Chj,k is later merged into the set of learned clauses
of the current iteration (Line 22).                                  C. Effectiveness of AutoINV Helper Generator
   Line 25 invokes the function pdr(·) to initiate a new                In this subsection, we show the effectiveness of AutoINV
attempt at proving the target property. This process leverages       Helper Generator in the helper generation task. We compare
the checkpoint from the previous proving attempt and the             our helper generation scheme against HARM [14], a flexible
learned clauses from Hj . If this attempt exceeds the allotted       assertion generation framework, to illustrate its efficiency in
time and the current frame completes its construction, the           generating helpers for the verification of the target property.
process is terminated, and a checkpoint is saved. Subsequently,      Table III presents the comparison results on three benchmarks:
the proving information is provided to the AutoINV Helper            vac-e, vsc-e, and mac-e. Using the default configuration of
Ranker to select more promising helper assertions. Line 30           HARM, assertions were generated with the template restricted
adjusts the timeout limit for each trial by a factor of α. It is     to the format of implication: condition → result. In the
important to note that once the timeout limit is reached in a        provided cases, HARM requires hours to generate a large
proving trial, the IC3/PDR algorithm will not complete until         number of assertions using a fine-tuned ranking mechanism.
the current frame finishes construction.                             Although the assertions generated by HARM maintain a
                                                                     reasonable correctness rate, they fail to produce even a few
                       VI. E VALUATION
                                                                     useful assertions for verification as helpers. If our framework
A. Experimental Setup                                                attempts to generate and identify useful helpers from HARM,
   Our experiments are conducted on a server running the             it will incur significant CPU time to generate a set of helper
Ubuntu 20.04 system. It is equipped with an Intel Core(TM)           assertions, and even more time to find a useful subset that
i5-11400 CPU working at a frequency of 4.2GHz and 128GB              potentially benefits the verification process of the target prop-
of memory. We take the open-source IC3/PDR algorithm                 erty. In contrast, AutoINV can generate a relatively small but
implementation in IC3Ref [24] and use AMD Vitis 2020.2               meaningful set of helpful assertions in a short time. The results
as the HLS tool. The target frequency for HLS compilation            demonstrate that the AutoINV helper generator is effective for
is 100MHz, and the target FPGA chip is xc7z020clg484-2.              helper generation in verification tasks on HLS designs and can
Yosys0.9 is used to compile the Verilog designs with assertions      quickly identify helpers that constrain the state space.
to the AIG file that can be taken as the input of IC3Ref. For
                                                                     D. Hyperparameter Configuration Evaluation
RTL design analysis, we use PyVerilog 1.3.0 [25].
                                                                        In this subsection, we evaluate the effectiveness of AutoINV
B. Benchmarks                                                        under different hyperparameter configurations on the AutoINV
  To validate the effectiveness of AutoINV, we employ several        Prover. The hyper-parameters include Nh , T0 , and α, as
designs with their respective target properties as benchmarks:       introduced in Section V-C. We limit Th to 10 seconds. The
    TABLE II: IC3/PDR results on benchmarks for hyper-parameter tuning on various configurations of AutoINV Prover.
         vac-e                                                vsc-e                                         mac-e                                      AVGh
 Config SAT.Qa CTIb ITc CLd FRe Time(s)f Accg SAT.Q                     CTI IT CL FR Time(s) Acc            SAT.Q      CTI IT CL FR Time(s) Acc        Acc
  Raw 12111500 78817 1 0              42 8310.22        -     23354152 71560 1 0       95 7704.33       -   16317585 36303 1 0 106 6239.64         -      -
   1     12991356 77729 5 210 50 6972.62 1.19× 8731930 27299 4 185 64 1510.68 5.10× 10561985 33246 4 161 97 2190.29 2.84×                              2.11×
   2     11620294 81727 9 183 38 6751.35 1.23× 9913628 31741 6 200 84 1620.94 4.75× 9586488 29785 7 248 90 1984.17 3.14×                               2.17×
   3     10249622 74325 6 155 38 5288.30 1.57× 13327248 34672 5 192 122 2162.91 3.56× 11956644 30859 5 234 97 2996.11 2.08×                            2.16×
   4     10768763 76494 9 236 44 5470.70 1.51× 8270314 25082 7 213 97 1271.50 6.05× 9825256 28152 9 295 85 2383.76 2.61×                               2.47×
   5     10016820 73685 6 221 36 5350.88 1.55× 10981527 29735 4 207 96 1850.83 4.16× 10067206 29840 5 262 86 2872.73 2.17×                             2.23×
 a The number of SAT solver calls in the verification process. b The number of CTIs encountered. c The number of iterations of the AutoINV Prover.
 d The number of side-loaded clauses. e The number of frames constructed in the IC3/PDR algorithm. f The time usage to prove the target property.
 g The speed-up ratio under different hyper-parameter configurations. h The average speed-up ratio of benchmarks provided.

TABLE III: The comparison on assertion generation efficiency.
              HARM [14]                          AutoINV Helper Generator          construct fewer frames to converge to the inductive invariant,
 Benchmark    Time(s)a   NUMb   CRce     URde     Time(s) NUM CR          UR       demonstrating our framework’s ability to guide the IC3/PDR
 vac-e        5147.57 266273 100.0% 0.0% 3.02               83    75.9% 73.5%      algorithm towards a more radical approximation of the reach-
 vsc-e        3682.66 197749 44.7% 0.2% 1.73                51    74.5% 70.6%
 mac-e        4981.16 328498 79.9% 0.2% 3.23                89    76.4% 74.1%
                                                                                   able states.
 a The CPU time cost for generating assertions. b Number of assertions.               The average speed-up for each configuration is shown in
 c The correctness rate (CR) of the top 1000 ranked assertions checked formally.
 d The useful rate (UR) of the top 1000 ranked assertions can produce clauses.
                                                                                   the last column, indicating that AutoINV can achieve an
 e Both CR and UR are evaluated at a time frame limit of 10 seconds.               average speed-up range from 2.11× to 2.47× regardless of
                                                                                   the configurations. In the next subsection, we will use config-
configurations are shown in Table IV. In our experiments, five                     uration 4, which has the highest speed-up of 2.47×, to conduct
hyperparameter configurations are used. The “Raw” config-                          verification tasks on large designs.
uration in the table refers to the vanilla IC3/PDR algorithm
without any side-loading.                                                          E. Results on AutoSA designs
   During verification, every task was proven as expected.                            This subsection presents the results of AutoINV on two
Table II provides results for vac-e, vsc-e, and mac-e under                        AutoSA designs. We set the timeout bound for AutoINV to
different configurations. From the statistics, we observe that                     12 hours. The hyperparameters for the AutoINV Prover are
in vac-e, AutoINV achieves a speed-up ranging from 1.19× to                        set to configuration 4, as concluded from Section VI-D. Table
1.57× compared to the vanilla IC3/PDR algorithm; in vsc-e,                         V shows the results of the verification tasks: autosa-mm-f
AutoINV achieves a speed-up of 3.56× to 6.05×; and in mac-                         and autosa-cnn-f.
e, AutoINV achieves a speed-up of 2.08× to 3.14×. These                               In autosa-mm-f, AutoINV achieves a 4.76× speed-up
speed-up ratios demonstrate the effectiveness of our verifica-                     compared to the vanilla IC3/PDR algorithm without side-
tion framework for formal verification tasks of HLS designs.                       loading. With proper guidance from our methodology, the
   Additionally, in most cases, the speed-up is accompanied by                     number of SAT queries is reduced by 83.0%, and the number
a reduced number of SAT solver calls and CTIs encountered.                         of CTIs encountered is reduced by 38.5%. IC3/PDR produces
For example, in vsc-e, the number of SAT solver calls is                           a 35-cycle counterexample trace that drives the FIFO to
reduced by 42.9% to 64.9%, and the CTIs encountered                                the full state. This suggests that the FIFO length should be
during verification are reduced by 51.5% to 64.9%. This                            increased in the original design to avoid a potential FIFO
indicates that our method can prune the state space early in                       block that could affect the overall execution speed.
the verification process and guide the IC3/PDR algorithm                              In autosa-cnn-f, the target property is proven by AutoINV in
towards a better direction for searching for potential inductive                   322.09 seconds, indicating that there is no execution trace that
invariants or counterexamples.                                                     causes the FIFO to become full. However, the vanilla IC3/PDR
   Although there are some cases, such as configuration 1                          algorithm fails to derive a proof within the timeout bound.
and configuration 2, when verifying vac-e, where more SAT                              TABLE V: IC3/PDR results on AutoSA benchmarks.
queries or CTIs are required compared to the baseline, the total                        Config   Time(s) SAT.Q    CTI    IT CL        FR    Result
verification time is still reduced. This is due to the clauses                                                 autosa-mm-f [26]
added by AutoINV simplifying the SAT engine’s solving                                     4      468.88 486608 8817 5 436             35     Cex
process or better generalization of CTIs that require more                               Raw     2235.16 2858343 14346 1 0            35     Cex
                                                                                                               autosa-cnn-f [26]
SAT queries. Better generalization of CTIs is reflected by the
                                                                                          4      322.09 14454     254    4 240        38  Proof
reduction in the number of counterexamples to generalization                             Raw     O.O.T. -         -      - -          -  Unknown
(CTG) by 16.44% and 4.34%, respectively, despite the increase
in CTIs in configuration 2.                                                                               VII. C ONCLUSION
   In most cases, AutoINV enables the IC3/PDR algorithm to                            In this paper, we propose AutoINV, a framework that guides
                                                                                   formal verification of hardware properties in HLS designs.
TABLE IV: Configurations of hyperparameters on AutoINV
                                                                                   AutoINV generates helper-assertion candidates from common
Prover.
                                                                                   HLS patterns and dynamically prioritizes effective ones based
   Config    Nh T0 α          Config Nh T0 α          Config Nh T0 α
   Raw       -  inf -         1      5  10 5          2      5  10 2               on CTIs observed in timeout trials. It iteratively applies
   3         5  100 2         4      10 1 2           5      10 100 2
selected helpers until IC3/PDR proves the target property. Ex-                   [14] S. Germiniani and G. Pravadelli, “Harm: A hint-based assertion miner,”
periments on diverse HLS designs and properties demonstrate                           IEEE Transactions on Computer-Aided Design of Integrated Circuits
                                                                                      and Systems, vol. 41, no. 11, pp. 4277–4288, 2022.
that AutoINV significantly improves verification speed.                          [15] Z. Yan, W. Fang, M. Li, M. Li, S. Liu, Z. Xie, and H. Zhang,
                                                                                      “Assertllm: Generating hardware verification assertions from design
                              R EFERENCES                                             specifications via multi-llms,” in Proceedings of the 30th Asia and
 [1] Y. Herklotz, Z. Du, N. Ramanathan, and J. Wickerson, “An empirical               South Pacific Design Automation Conference, ser. ASPDAC ’25. New
     study of the reliability of high-level synthesis tools,” 2021.                   York, NY, USA: Association for Computing Machinery, 2025, p.
 [2] N. Pundir, S. Aftabjahani, R. Cammarota, M. Tehranipoor, and F. Farah-           614–621. [Online]. Available: https://doi.org/10.1145/3658617.3697756
     mandi, “Analyzing security vulnerabilities induced by high-level syn-       [16] J. Xu and L. Josipović, “Automatic inductive invariant generation for
     thesis,” ACM Journal on Emerging Technologies in Computing Systems,              scalable dataflow circuit verification,” in 2023 IEEE/ACM International
     vol. 18, 2022.                                                                   Conference on Computer Aided Design (ICCAD). IEEE, 2023, pp. 1–9.
 [3] A. R. Bradley, “Sat-based model checking without unrolling,” in In-         [17] R. Dureja, J. Baumgartner, R. Kanzelman, M. Williams, and K. Y.
     ternational Workshop on Verification, Model Checking, and Abstract               Rozier, “Accelerating parallel verification via complementary property
     Interpretation. Springer, 2011, pp. 70–87.                                       partitioning and strategy exploration,” in 2020 Formal Methods in
 [4] N. Eén, A. Mishchenko, and R. Brayton, “Efficient implementation of             Computer Aided Design (FMCAD), 2020, pp. 16–25.
     property directed reachability,” in 2011 Formal Methods in Computer-        [18] R. Dureja, J. Baumgartner, A. Ivrii, R. Kanzelman, and K. Y. Rozier,
     Aided Design (FMCAD). IEEE, 2011, pp. 125–134.                                   “Boosting verification scalability via structural grouping and semantic
 [5] M. Kang, A. Nova, E. Singh, G. S. Bathini, and Y. Viktorov, “Lfps:               partitioning of properties,” in 2019 Formal Methods in Computer Aided
     Learned formal proof strengthening for efficient hardware verification,”         Design (FMCAD), 2019, pp. 1–9.
     in 2023 IEEE/ACM International Conference on Computer Aided Design          [19] S. Das, A. Hazra, P. Dasgupta, S. Kundu, and H. Jain, “Purse: Property
     (ICCAD). IEEE, 2023, pp. 1–9.                                                    ordering using runtime statistics for efficient multi - property verifi-
 [6] Y. Herklotz, J. D. Pollard, N. Ramanathan, and J. Wickerson,                     cation,” in 2024 Design, Automation & Test in Europe Conference &
     “Formal verification of high-level synthesis,” Proc. ACM Program.                Exhibition (DATE), 2024, pp. 1–6.
     Lang., vol. 5, no. OOPSLA, Oct. 2021. [Online]. Available:                  [20] G. Hu, J. Tang, C. Yu, W. Zhang, and H. Zhang, “Deepic3: Guiding ic3
     https://doi.org/10.1145/3485494                                                  algorithms by graph neural network clause prediction,” in 2024 29th Asia
 [7] M. Pardalos, Y. Herklotz, and J. Wickerson, “Resource sharing for                and South Pacific Design Automation Conference (ASP-DAC). IEEE,
     verified high-level synthesis,” in 2022 IEEE 30th Annual Interna-                2024, pp. 262–268.
     tional Symposium on Field-Programmable Custom Computing Machines            [21] B. C. Schafer and Z. Wang, “High-level synthesis design space explo-
     (FCCM), 2022, pp. 1–6.                                                           ration: Past, present, and future,” IEEE Transactions on Computer-Aided
 [8] L. Piccolboni, G. Di Guglielmo, and L. P. Carloni, “Kairos: Incremental          Design of Integrated Circuits and Systems, vol. 39, no. 10, pp. 2628–
     verification in high-level synthesis through latency-insensitive design,”        2639, 2020.
     in 2019 Formal Methods in Computer Aided Design (FMCAD). IEEE,              [22] L. Du, T. Liang, X. Zhou, J. Ge, S. Li, S. Sinha, J. Zhao, Z. Xie,
     2019, pp. 105–109.                                                               and W. Zhang, “Fado: Floorplan-aware directive optimization based
 [9] Y. Li, G. Zhao, Y. He, and H. Zhou, “Se3: Sequential equivalence                 on synthesis and analytical models for high-level synthesis designs on
     checking for non-cycle-accurate design transformations,” in 2023 60th            multi-die fpgas,” ACM Trans. Reconfigurable Technol. Syst., vol. 17,
     ACM/IEEE Design Automation Conference (DAC). IEEE, 2023, pp.                     no. 3, Sep. 2024. [Online]. Available: https://doi.org/10.1145/3653458
     1–6.                                                                        [23] J. Zhao, L. Feng, S. Sinha, W. Zhang, Y. Liang, and B. He, “Comba: A
[10] S. Hangal, N. Chandra, S. Narayanan, and S. Chakravorty, “Iodine:                comprehensive model-based analysis framework for high level synthesis
     a tool to automatically infer dynamic invariants for hardware                    of real applications,” in 2017 IEEE/ACM International Conference on
     designs,” in Proceedings of the 42nd Annual Design Automation                    Computer-Aided Design (ICCAD), 2017, pp. 430–437.
     Conference, ser. DAC ’05. New York, NY, USA: Association                    [24] A. Bradley, “An implementation of ic3,” 2022. [Online]. Available:
     for Computing Machinery, 2005, p. 775–778. [Online]. Available:                  https://github.com/arbrad/IC3ref
     https://doi.org/10.1145/1065579.1065786                                     [25] S. Takamaeda-Yamazaki, “Pyverilog: A python-based hardware design
[11] S. Vasudevan, D. Sheridan, S. Patel, D. Tcheng, B. Tuohy, and D. John-           processing toolkit for verilog hdl,” in Applied Reconfigurable
     son, “Goldmine: Automatic assertion generation using data mining                 Computing, ser. Lecture Notes in Computer Science, vol. 9040.
     and static analysis,” in 2010 Design, Automation & Test in Europe                Springer International Publishing, Apr 2015, pp. 451–460. [Online].
     Conference & Exhibition (DATE 2010), 2010, pp. 626–629.                          Available: http://dx.doi.org/10.1007/978-3-319-16214-0 42
[12] L. Liu, D. Sheridan, V. Athavale, and S. Vasudevan, “Automatic genera-      [26] J. Wang, L. Guo, and J. Cong, “Autosa: A polyhedral compiler for
     tion of assertions from system level design using data mining,” in Ninth         high-performance systolic arrays on fpga,” in Proceedings of the 2021
     ACM/IEEE International Conference on Formal Methods and Models                   ACM/SIGDA International Symposium on Field-Programmable Gate
     for Codesign (MEMPCODE2011), 2011, pp. 191–200.                                  Arrays, 2021.
[13] L. Liu, C.-H. Lin, and S. Vasudevan, “Word level feature discovery to
     enhance quality of assertion mining,” in 2012 IEEE/ACM International
     Conference on Computer-Aided Design (ICCAD), 2012, pp. 210–217.
