                                         Verification of Compiler-to-Accelerator Mappings for
                                         Machine Learning Accelerators
                                         AKASH GAONKAR, Princeton University, USA
                                         MIKE HE, Princeton University, USA
                                         YI LI, Meta Platforms, USA
                                         BO-YUAN HUANG, Intel INT31, USA
                                         ANDREW CHEUNG, University of Washington, USA
arXiv:2609.30651v1 [cs.PL] 25 Sep 2026




                                         VISHAL CANUMALLA, Stanford University, USA
                                         GUS HENRY SMITH, University of Washington, USA
                                         ZACHARY TATLOCK, University of Washington, USA
                                         GRIGORY FEDYUKOVICH, Florida State University, USA
                                         SHARAD MALIK, Princeton University, USA
                                         AARTI GUPTA, Princeton University, USA
                                         To meet the performance needs of modern machine learning (ML) applications, ML compiler frameworks
                                         support compiler-to-accelerator mappings that offload parts of application code to operations in specialized
                                         hardware accelerators. However, most of these frameworks do not verify these mappings down to the hardware
                                         level, potentially resulting in functional mismatches. In this paper we propose Bolt, the first framework for
                                         formally verifying the correctness of compiler-to-accelerator mappings for coarse-grained intrinsics in ML
                                         accelerators, with respect to a formal hardware semantics. Bolt does not require additional information from
                                         the compiler, and verifies the functional equivalence of the application code and the code for the mapped
                                         hardware accelerator intrinsic, including handling of complex loop nests and tensor data layouts in hardware.
                                         It effectively utilizes a pattern of aligning software loops with the hardware, followed by relating corresponding
                                         data layouts, to enable verification using well-aligned product programs. To support these steps, we propose
                                         two custom templates — sync-skeleton, layout-sketch — to guide users in aligning loops and specifying data
                                         layout relationships, respectively. We have developed a proof-of-concept prototype for Bolt and use it to
                                         successfully verify the correctness of several complex mappings for two recent open-source ML accelerators.
                                         CCS Concepts: • Software and its engineering → Formal software verification.
                                         Additional Key Words and Phrases: compiler correctness, machine learning accelerators, formal hardware
                                         semantics, tensor programs, program equivalence verification, product programs.

                                         1   Introduction
                                         Modern machine learning (ML) applications continually demand better performance (speed, power
                                         usage, etc.) that is being met through specialized accelerators. To support this computation trend,
                                         recent ML compiler frameworks such as BYOC [9], Exo [24], MLIR [29], Halide [35, 47], and 3LA [22]
                                         can compile application code to run on these specialized hardware accelerators in addition to the
                                         CPU and GPU. Hardware accelerators provide intrinsics for specialized coarse-grained operations,
                                         such as matrix multiplication [18, 41], or linear-layer [51]. This specialization is made possible by
                                         significant optimizations in the hardware accelerator implementations, particularly by: (i) using
                                         Authors’ Contact Information: Akash Gaonkar, Princeton University, Princeton, NJ, USA, agaonkar@princeton.edu; Mike He,
                                         Princeton University, Princeton, NJ, USA, mikehe@princeton.edu; Yi Li, Meta Platforms, Menlo Park, CA, USA, yili.leeoh@
                                         gmail.com; Bo-Yuan Huang, Intel INT31, Santa Clara, CA, USA, byhuang116@gmail.com; Andrew Cheung, University of
                                         Washington, Seattle, WA, USA, acheung8@cs.washington.edu; Vishal Canumalla, Stanford University, Palo Alto, CA, USA,
                                         vjc@stanford.edu; Gus Henry Smith, University of Washington, Seattle, WA, USA, guscomps@gmail.com; Zachary Tatlock,
                                         University of Washington, Seattle, WA, USA, ztatlock@cs.washington.edu; Grigory Fedyukovich, Florida State University,
                                         Tallahassee, FL, USA, grigory@cs.fsu.edu; Sharad Malik, Princeton University, Princeton, NJ, USA, sharad@princeton.edu;
                                         Aarti Gupta, Princeton University, Princeton, NJ, USA, aartig@cs.princeton.edu.
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
2                                                             Grigory Fedyukovich, Sharad Malik, and Aarti Gupta




Fig. 1. A typical ML compiler flow that targets hardware accelerators. After high-level optimizations and
target selection, code generation for hardware accelerators is performed by using compiler-to-accelerator
mappings (green box). Bolt verifies these mappings with respect to a formal hardware semantics.

hardware parallelization techniques to expedite loops, and (ii) customizing where and how tensor
data are stored in accelerator memory. Accordingly, many frameworks use compiler-to-accelerator
mappings for coarse-grained intrinsics, to produce highly performant executables and/or runtimes.
   This context is illustrated in Fig. 1. An ML compiler (such as Exo [24], Mosaic [2], or 3LA [22])
uses various techniques for code optimization and target selection on the compiler IR (intermediate
representation). Then, during code generation, it maps pieces of IR code to some hardware accel-
erator intrinsics using a compiler-to-accelerator mapping (abbreviated c2a-mapping, or simply a
mapping) – three such mappings are shown pictorially in the figure. Intrinsics are invoked by the
host processor through MMIO (Memory-Mapped IO) or similar instructions – we refer to these as
MMIO code in the rest of the paper. Executing the MMIO code by the host processor is essentially
like calling a function that is implemented in hardware.

1.1   Motivation: Verifying correctness of compiler-to-accelerator mappings
Aside from performance, the correctness of the compiled code is the compiler’s primary requirement.
That is, the compiler’s output must be equivalent to the original program. Many existing ML
compilers [2, 10, 11, 24, 34, 38] use and verify code transformations such as loop reordering, loop
tiling, etc. done in software (discussed in detail §8). However, most stop short of considering a
formal hardware semantics, and the step of mapping a code fragment to a coarse-grained hardware
accelerator intrinsic (i.e., the MMIO code for this hardware function call) is often not verified.
If there is a mistake in configuring the accelerator or there is a functional mismatch with the
supported intrinsic, then errors can result from a single invocation of the accelerator intrinsic (and
accumulate over multiple invocations in an end-to-end ML application).
Problem definition. Given a compiler-to-accelerator mapping from some IR code to some MMIO
code, our goal is to prove the functional equivalence of the code on the two sides, including a formal
hardware semantics, i.e., given the same input tensors, they should produce the same output tensors.
We consider the general case of a black-box mapping, i.e., where there may not be any internal
compiler steps with additional information about how the mapping was constructed or selected. In
this general form, this can be viewed as the classic program equivalence problem. This general
case is also useful for a third-party independent verification of a mapping.
   The problem of verifying the correctness of a compiler-to-accelerator mapping has some sim-
ilarities with translation validation [43, 45], where programs before and after some compilation
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                 3


step are checked for equivalence. However, the programs that we aim to verify for equivalence
constitute the mapping itself, which is used by an ML compiler during code generation. Thus, by
verifying the equivalence of these programs, we prove correctness of the associated compiler step.
   We would like to emphasize that the goal of our work is to demonstrate the tractability of
program-equivalence based verification in this context, rather than full automation (which would
require more engineering effort in developing a tool chain that supports an existing compiler). The
reader may wonder why compiler-to-accelerator mappings are challenging to verify correct—many
hardware intrinsics have been verified through standard hardware verification techniques, such as
bounded model checking (BMC) [5] —so why not the MMIO code of the mappings shown in Fig. 1?
The main reason is that mappings to coarse-grained accelerators are hard to verify because the
hardware operations contain many and deeply nested loops (due to hardware parallelism) and complex
data layouts (in hardware memory buffers). Techniques based on BMC are not able to fully unroll
the loops within resource limits, and existing invariant-based techniques (using interpolants [60]
or IC3 [7]) do not scale on large complex buffers. In §1.3, we describe the verification challenges
due to these hardware features in detail, and reveal them in a real-world example in §2.1. We will
demonstrate how we have customized program equivalence techniques in this hardware-driven
context. We successfully verify several c2a-mappings, even as standard techniques do not scale
(§7.3).

1.2   Proposed framework: Bolt
In this paper, we propose Bolt (Bridging Opaque Loops and Tensors), a new framework and the first
one for formally verifying the correctness of compiler-to-accelerator mappings for coarse-grained
ML accelerator intrinsics, with respect to a formal hardware semantics. Bolt requires the semantics
of the IR code and the MMIO code, but does not depend upon any compiler information such as
internal correspondences between smaller fragments in the IR code and sub-operations or internal
buffers in the hardware.
   There are other efforts that have taken a different approach for considering hardware semantics
when compiling ML applications to hardware accelerators. In particular, a recent effort [38] verifies
an ML compiler pipeline down to hardware accelerators. It is based on a custom compiler that
maps software to a restricted family of accelerators (called coarse-grained reconfigurable arrays) in
a series of smaller compilation steps. They use translation validation on these smaller steps, using
information from the compiler (e.g., scheduling, memory mapping) to perform verification. Another
recent approach [46] uses High-Level Synthesis (HLS), where source-to-source transformations
on C/C++ programs are used for optimizing ML operations (such as matrix-multiply). Here, the
hardware generated by the HLS compiler (e.g., a systolic array accelerator) from the optimized
program is (presumably) correct-by-construction. While these synthesis-based approaches greatly
help verification of the ML compilation pipeline, their goals and approaches are incomparable
to ours – their compilers do not target existing/custom hardware accelerator designs (such as
FlexASR [51]) or coarse-grained ML operations beyond those that their compilers can automatically
synthesize to reconfigurable/systolic arrays.

1.3   Verification Challenges
There are many challenges in verifying the correctness of compiler-to-accelerator mappings. An ML
compiler typically uses a tensor program representation as its high-level IR, and explores different
loop reorderings, loop tilings, etc., to optimize for the most performant loop structure, commonly
referred to as the loop nest. During code generation, c2a-mappings encapsulate the mapping from
selected IR code to MMIO code for the accelerator.
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
4                                                             Grigory Fedyukovich, Sharad Malik, and Aarti Gupta

Formal hardware semantics for MMIO code. A core verification challenge is to bridge the
gap between software semantics on the IR side with hardware semantics (typically state transition
systems) on the other. As mentioned earlier, many existing ML compiler efforts [9, 24, 29, 34] stop
short of verifying against a formal hardware semantics. Our first challenge is that we need to
capture the hardware semantics of the MMIO code in a given mapping.

Complex loop nests and tensor data layouts in hardware. In coarse-grained c2a-mappings,
the hardware side often has complex loop nests due to parallel processing elements and/or single-
instruction-multiple-data (SIMD) parallelism, in addition to loops using hardware counters. Fur-
thermore, the correspondences between tensor data in the IR code and the accelerator code are
obscured by highly optimized tensor data layouts within an accelerator memory. In particular,
partitioning, rearrangement, and duplication of tensor data in hardware introduces complicated
address arithmetic. Thus, checking equivalence of corresponding outputs requires relating complex
data layouts on the two sides, but users often struggle to define them and verifiers struggle to
reason about them.

1.4   Bolt: Key Ideas and Contributions
Insight #1: Our first insight is that mappings to coarse-grained accelerators are hard to verify
because the hardware operations contain many and deeply nested loops (due to hardware parallelism)
and complex data layouts (in hardware memory buffers). Frustratingly, these loop nests and data
layouts are opaque within the semantics of the MMIO code.
   To address the core challenge of capturing the formal hardware semantics and bridging the gap
with IR code, we have developed an Intermediate Verification Language (IVL) called Hex. We do
not claim novelty in its design, which is inspired by other IVLs such as Dafny [30] for program
verification, and HLS languages (such as synthesizable C/C++, SystemC [44]) that model hardware.
   We use Hex to represent the MMIO code as a stateful program (detailed in §3), where the
formal hardware semantics is specified by an Instruction Level Abstraction (ILA) model [23].
Essentially, an ILA model specifies a state transition update for each operation (MMIO command)
of the accelerator, where the update is hierarchically defined by a sequence of updates to some
software-visible architectural state. Importantly, these state transition updates specify updates due
to hardware-implemented parallel as well as iterative loops. In addition to explicating hardware
semantics, Hex provides features for customized modeling of loop nests and tensor buffers touched
in the MMIO code, since these play a critical role in verification. Also, it provides support for users
to specify annotations that enable automated verification via Satisfiability Modulo Theories (SMT)
solvers (e.g., Z3 [13]).
   For verifying program equivalence, Bolt leverages known techniques [4, 49, 59], where a “product”
program is constructed over the two given programs to check that they produce the same outputs
when given the same inputs. There has been extensive work on aligning corresponding parts (e.g.,
loops) of the given programs, to enable use of relational invariants in the product program for
decomposing and simplifying verification [4, 12, 21, 40, 49, 53, 54, 59]. However, none of the existing
techniques (detailed in §8) have been applied to c2a-mappings or to loop nests of similar complexity
as in ML accelerator mappings.
   Inspired by prior work, the key idea in Bolt is to first align the loop nests on the software side
with the hardware side, and then relate data layouts in the tensor updates in the corresponding loops.
In our setting, we have found this pattern — align-loops-with-hardware and then relate-layouts-
of-buffers — to be very useful. It enables decomposing the overall verification problem, which is
essential in practice for verification to succeed. We have developed some insights supporting these
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                    5




                            Fig. 2. Bolt Framework: Components and Main Steps.




two steps, which we have incorporated into the key components in the Bolt framework, depicted
in Fig. 2 (and detailed in the next section with a motivating example).
   Insight #2 (Align step): To support align-loops-with-hardware, we only need to align software
with the compute-performing loops in the hardware side. First, it is easier to perform rewriting
on the pure-functional IR code than on the stateful accelerator Hex code. Furthermore, data
movement loops in hardware do not affect the functional behavior of the hardware side and can be
handled in a later step (Relate). These insights lead us to introduce a template called a sync-skeleton,
which extracts tensor computing loops in the hardware-based operation (including those due to
parallelization or counter-based iteration). The sync-skeleton is used as a guide for the user to
rewrite the IR code to align its loops with hardware. from the latter, and reduce the number of
loops that should be aligned (ideally) in the former.
   Insight #3 (Relate step): For relate-layouts-of-buffers, we combine information (shared loop
counters, tensor sizes, buffer overwriting) provided by the software IR and hardware sides. Con-
cretely, we introduce a template called a layout-sketch, which identifies a correspondence between
the tensor outputs, assuming correspondences on the tensor inputs. This provides a flexible template
for each loop, capturing iterative updates in data computation and data movement in the loop,
which is used to construct important relational invariants that help verification succeed. While the
development of these templates are user-driven, we provide Hex-based tactics to guide the user.
These steps enable construction of a well-aligned product program, along with annotations for data
layout invariants and other invariants, which is verified using automated SMT-based techniques.




Bolt Prototype. We have developed a proof-of-concept prototype, where the user provides the
IR code and the accelerator Hex code, interacts with the prototype to develop the custom templates
sync-skeleton and layout-sketch, performs IR rewriting guided by the sync-skeleton, and provides
loop annotations based on the layout-sketch. The verification procedure in Bolt is automated
and uses the Z3 SMT solver [13]. We log the user effort involved in our prototype as part of our
evaluation (§7.2). At each step, the user largely follows the procedures we prescribe, setting the
stage for future automation.
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
6                                                             Grigory Fedyukovich, Sharad Malik, and Aarti Gupta

Summary of Contributions
       • We present Bolt, the first framework for verifying correctness of compiler-to-accelerator
         mappings for coarse-grained intrinsics in compilers for ML accelerators, with respect
         to a formal hardware semantics. We consider the general case where no information is
         available from the compiler about how these mappings are constructed, and prove program
         equivalence between the software and hardware code in the mapping.
       • We leverage techniques based on product programs and propose custom templates for
         guiding a user to align loops and specify data layout relationships — the sync-skeleton and
         layout-sketch, respectively. We provide heuristics and tactics for extracting these templates
         from programs written in Hex, an intermediate verification language that powers Bolt, and
         for constructing relational invariants that help the solver’s performance. In the common case,
         these heuristics and tactics reduce the burden of aligning loops and specifying relational
         invariants to step-by-step procedures.
       • We evaluate Bolt on case studies from two recent open-source ML accelerators [51, 57]
         with available formal hardware semantics. These case studies show Bolt’s capabilities in
         successful verification of several complex compiler-to-accelerator mappings. Notably, our
         most complex mapping — linear-layer for the FlexASR accelerator — has 29 loops in the
         product program (many nested, up to maximum depth 7). As far as we know, none of the
         existing program equivalence techniques/tools (based on either automated reasoning or
         interactive theorem proving) has demonstrated successful verification of such complex
         product programs.

2     Overview of the Bolt framework
In this section we use a motivating example to illustrate the challenges in verifying a c2a-mapping,
and show how the key components and steps of Bolt enable successful verification.

2.1    Running Example
Consider the c2a-mapping shown in Fig. 3 for a recent open-source ML accelerator called Flex-
ASR [51]. This mapping offloads a linear-layer operation to an intrinsic in FlexASR, as used in the
3LA compiler [22].

IR code for linear-layer. The purple box (upper left) shows the IR code, in a basic pure-functional
tensor language that uses maps and reduces to perform tensor computations. These are highly
structured loop operations that maintain multidimensional tensor representations for data accesses.
In particular, map𝑛𝑖=0 𝑒 constructs a tensor by mapping each 𝑖 ∈ {0, . . . , 𝑛 − 1} to the result of 𝑒 at 𝑖,
i.e., [𝑒 |𝑖=0 · · · 𝑒 |𝑖=𝑛−1 ], and reduce𝑛𝑖=0 (𝑠 = 𝑒 1 in 𝑒 2 ) accumulates the value of 𝑠, starting at 𝑠 = 𝑒 1 and
updating 𝑠 = 𝑒 2 |𝑖,𝑠 for each successive value of 𝑖 ∈ 0, . . . , 𝑛 − 1.

MMIO code for FlexASR linear-layer. The yellow box on the bottom left in Fig. 3 shows the
MMIO code for performing a linear-layer using the FlexASR accelerator, where the host processor is
an Arm Cortex-A53 (supporting A32 assembly). Several MMIO commands configure the accelerator
before the final command (emphasized in red) triggers the linear-layer computation within the
accelerator hardware.

2.2    Bolt in action
We briefly describe the main steps and components of Bolt (Fig. 2), illustrating them using the
running example (with pointers to related sections).
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                         7


𝑊 : tensor( (𝑛𝑜 , 𝑛𝑖 ), R)
𝑋 : tensor( (𝑛𝑡 , 𝑛𝑖 ), R)
𝐵 : tensor( (𝑛𝑜 ), R)
           𝑛𝑡     𝑛𝑜     𝑛𝑖
 let 𝑃 = map map reduce (𝑠 = 0 in 𝑠 + 𝑊 [ 𝑗, 𝑖 ] ∗ 𝑋 [𝑡, 𝑖 ] )
           𝑡 =0   𝑗 =0   𝑖=0
     𝑛𝑡    𝑛𝑜
 in map map (𝑃 [𝑡, 𝑗 ] + 𝐵 [ 𝑗 ] )
    𝑡 =0   𝑗 =0




   Fig. 3. Running example: the compiler-to-accelerator mapping for a linear-layer operation in FlexASR.

Hex language (§3). Bolt is powered by the Hex IVL, which provides a common bridge between
functional IR code on the one hand with state-based accelerator code that respects the formal
hardware semantics (using the ILAs [23]) on the other. We view Hex as a repurposing of exist-
ing HLS-style languages (e.g., C/C++/SystemC), with custom features to support verification of
hardware loop nests and complex data layouts. In particular, Hex supports the development of
sync-skeleton and layout-sketch (itself a first-class object), by identifying hardware counters and
parameters as first-class objects, for reasoning about loop bounds and address arithmetic for data
layouts in the Align and Relate steps. (In the Verify step, we substitute parameters with concrete
values due to solver limitations with nonlinear arithmetic, §6.) Additionally, Hex is used to represent
the product program and supports user annotations of relational invariants that help improve
solver performance.
   For the running example, the yellow box on the right in Fig. 3 shows the accelerator Hex code.
Each hw_call statement (lines 6-10) corresponds one-to-one with an MMIO command, after a
preamble that defines parameters (lines 1-5) that represent key dimensions and sizes for configuring
the accelerator. The code block in lines 10-27 shows (a part of) the computation triggered due to
the operation in line 10.
   Note that the FlexASR accelerator code has 28 hardware loops that implement the linear-layer
operation! These are represented in Hex via imperative-style loops, where the par-for loops
capture hardware parallelism due to parallel processing elements (e.g., line 11) or single-instruction-
multiple-data (SIMD) parallelism (e.g., lines 16, 21). Note also that Hex captures memory accesses
and assignments (e.g., lines 17, 23-25) that manipulate tensor data in hardware. These accesses often
involve significant address arithmetic to to optimize tensor data layouts in memory buffers: Line 17
has a simple indirect memory access (due to replicated control state across processing elements)
that reads from peInOff, a buffer of address offsets computed in a parent loop. Data layouts are
further complicated by overwriting and lazy initialization of buffers, which featured heavily in our
other mappings (§7.2).
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
8                                                             Grigory Fedyukovich, Sharad Malik, and Aarti Gupta


                                                             𝑛𝑔      𝑛𝑏𝑎𝑛𝑘𝑠
                                                                                                  𝑛𝑝
                                                                              𝑛𝑣                         
                                                         1
         𝑛𝑔 𝑛𝑏𝑎𝑛𝑘𝑠    𝑛𝑣
                                       𝑛𝑝                  map map map let 𝑅3 = 4map
                                                                    2       3
    1      2        3                                        𝑔=0         𝑡 =0     𝑣=0              𝑝=0
       ?       ?       ?      let ? = 4map
       0       0       0                 0                                        𝑛𝑝𝑎𝑟 
                                                                                  𝑛𝑢         𝑛𝑝𝑎𝑟 
                 𝑛𝑢      𝑛𝑝𝑎𝑟                                 let 𝑅1 = 5reduce 𝑠 = map 0 in 6map
      let ? = 5 ? 6map                                                            𝑢=0        𝑗=0             𝑗=0
                   0       0                                                        𝑛𝑝𝑎𝑟
                                                                                 7
                      𝑛𝑝𝑎𝑟                                         let 𝑟 2 = reduce 𝑠𝑖 = 0 in accAdd(
                                                                                      𝑖=0
           let ? = 7 ? ?expr (accAdd, adpfMul)
                         0                                                 𝑠𝑖 , adpfMul(𝑊 [...] as AFloat(8),
                                                                                     𝑋 [...] as AFloat(8))
                                      
                  in ?expr (accAdd)                                 
              𝑛𝑝𝑎𝑟                                                 ) in accAdd(𝑠 [ 𝑗], 𝑟 2 )
         in 8map ?expr (acc2actreg, ··· )                              𝑛𝑝𝑎𝑟
                   0                                               in 8map acc2actreg(...)
             𝑛𝑝       𝑛𝑝𝑎𝑟
                                                                         𝑗=0
        in 9map 10map ?expr (fixed2adpf)                           𝑛𝑝       𝑛𝑝𝑎𝑟
              0         0                                    in 9map map fixed2adpf(𝑅3 [𝑝, 𝑗])
                                                                          10
                                                                   𝑝=0          𝑗=0

Fig. 4. Running example: (Left) the sync-skeleton (all ten loops) extracted from the accelerator Hex code.
(Right) the IR code after rewriting. Loop superscripts identify aligned loops (with same numbering of loops
in Figs. 3 and 5).



Loop alignment via the Sync-skeleton (§4). The first main step (Align) in Bolt is to align
the loops on the software side with those on the hardware side. This alignment is guided by
the sync-skeleton, a template extracted from the accelerator Hex code. We provide a Hex-based
heuristic procedure for the extraction, such that each loop in the sync-skeleton identifies a tensor
computation (a map/reduce operation) in the hardware, while loops with only data movement are
abstracted away. The reason for abstracting away the data movement loops is that they do not
appear in the functional IR code, so there is no need to align them. However, these data movement
loops will be included at a later stage when the product program is constructed, since they determine
tensor data layouts in the hardware buffers.
   For the running example, the accelerator Hex code (right box of Fig. 3) clearly identifies the
loops in the hardware, including those due to SIMD and PE parallelism. This loop nest reflects a
fixed loop tiling and loop ordering in hardware, set by parameters and commands of the given
mapping (lines 1-9). Our heuristic procedure enables extracting the sync-skeleton shown in the
left box of Fig. 4. The sync-skeleton contains 10 loops, corresponding to loops of the accelerator
Hex code that perform tensor (map or reduce) computations (identified by loop superscripts in
Figs. 3 and 4) and omits loops that only perform data movement or data initialization. Loop types
are identified where possible, marking loops as map, reduce, or either (denoted by ? in Fig 4).

Rewriting the IR code for loop alignment (§4). The sync-skeleton guides a user to perform
rewriting on the IR code to align with the loop nests in hardware. (Since it is easier to rewrite
functional programs, we advocate rewriting the IR code, rather than rewriting the accelerator Hex
code.) We provide a system of rewriting rules, standard and customized (based on Hex features,
e.g., parameter substitution rules). A user can employ these rewriting rules to align the loops in
the IR code to those in the sync-skeleton. The rewriting and alignment is best-effort, and any
un-aligned loops on either side may require additional invariants but do not affect the soundness
of verification.
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                             9




 Fig. 5. Running example: a layout-sketch and relational invariants for an aligned loop (loop #6, lines 2-8)

   For the running example, the IR code was transformed through 29 rewriting steps to align with
all 10 loops of the sync-skeleton. The resulting IR code is shown in the right box of Fig. 4, containing
the 10 aligned loops (and one unaligned loop that performs zero-initialization).
Relating tensor correspondences via the Layout-sketch (§5). After the loops have been
aligned, the second main step (Relate) in Bolt is to relate the tensor data on the software side and
the hardware side. This is done via a layout-sketch, a template that a user can specify in Hex for
each aligned loop. Informally, a layout-sketch identifies the correspondence between the tensor
elements in the IR code and the buffer elements in the accelerator Hex code, respectively, that are
updated due to assignments in the aligned loop, assuming some given correspondence between the
inputs to the assignment. We provide useful tactics for users to create a layout-sketch as well as a
simple procedure to construct relational invariants from a layout-sketch, to be added as annotations
in the product program.
   For the running example, Fig. 5 shows the layout-sketch (line 1) for an aligned loop. It specifies a
correspondence between IR code tensor element 𝑠[𝑗] with a hardware buffer element 𝑚𝑎𝑐𝐴𝑐𝑐[𝑝, 𝑗],
based on a set of input correspondences (elided in the figure). The resulting relational loop invariants
are shown in lines 3-5 (where the 𝑎𝑒’s represent address arithmetic). If any of these invariants is
not valid, then the verification fails, thus providing a counterexample for the user to refine the
layout-sketch.
Verification via Product Programs (§6). The Align and Relate steps enable construction of a
well-aligned product program in Hex, along with user annotations. In the third step (Verify) in
Bolt, we use standard program verification techniques (e.g., similar to Dafny [30]) to automatically
generate Verification Conditions (VCs) based on relational invariants at aligned loop boundaries
(and other invariants that a user may provide). These VCs are verified using an off-the-shelf SMT
solver (Z3 [13]).
   For the running example, we automatically construct a well-aligned product program (along
with annotations) from the transformed IR code (lowered to Hex) and accelerator Hex code, and
their aligned loops. Users add the invariants constructed in the Relate step and any additional
invariants necessary for verification. Note that due to the Align step, the loops with tensor operations
are already aligned (in a best effort), and due to the Relate step, relational invariants for tensor
data correspondence are defined based on the layout-sketch. These two steps significantly help
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
10                                                            Grigory Fedyukovich, Sharad Malik, and Aarti Gupta

our product program verifier, which generates VCs that are checked by the Z3 SMT solver [13]
(detailed in §6). A “small-world” model of our running example (with reduced bounds and sizes)
was verified in 104s. Verification results for the full model and other case studies are discussed in
our evaluations (§7).

User effort for tasks in the Bolt prototype. In our proof-of-concept prototype, we demonstrate
tractability of program-equivalence based verification of c2a-mappings, rather than full automation.
We briefly summarize the user effort below, where each step largely follows our proposed procedure
(setting the stage for future automation).
    (1) Align - sync-skeleton extraction — Follow procedure in §4.1, heuristics in §4.2
    (2) Align - align IR code with sync-skeleton — Follow procedure in §4.3
    (3) Relate - identify layout-sketches — For each loop, follow tactics in §5.2
    (4) Relate - specify data layout invariants — Follow procedure in §5.3
    (5) Verify - construct product program — automated; user adds invariants here
    (6) Verify - generate and check verification conditions — automated (using Z3).
  Note that only task (2) can introduce unsoundness, via incorrect rewrite rules — these can be
checked using other tools (e.g., ATL [29]). In particular, sync-skeleton extraction is sound and
deterministic, alignment is best-effort, product-program construction is standard and has been
shown sound in prior work [9], and the invariants added in Relate and Verify are checked during
verification.

3   Hex: A Verification Language for Hardware Explication
We present a new Intermediate Verification Language (IVL) called Hex to reveal the formal hardware
semantics of an accelerator’s intrinsics, for the purpose of proving semantic equivalence between
the IR code and MMIO code. The syntax for Hex is shown in Fig. 6. Wherever possible, we borrow
standard constructs from well-known imperative verification languages such as Dafny [30] and
Why3 [6]. Additionally, Hex emphasizes hardware loop nests and data layouts to support the main
steps in the Bolt framework as follows:
     • A variant of the ranged-based for-loop helps align the accelerator Hex code with the
       structured loops of an IR code tensor operation. Additionally, it captures how each loop is
       implemented in hardware (e.g., via SIMD or counter-based iteration), providing heuristics
       for constructing the sync-skeleton in the Align step of Bolt (§4).
     • The multidimensional buffer type provided in Hex is the basis for a user to develop a
       layout-sketch in the Relate step in Bolt, which relates the data tiling of a tensor in the IR
       code with multiple buffers or registers distributed in hardware (§5).
     • We also use Hex to represent the product program in the Verify step, including annotations
       for relational loop invariants (§6).
   Essentially, a Hex program provides a structured-program view of a transition-system-based
hardware semantics. The key features of Hex that support modeling the hardware semantics in our
context and program equivalence verification are briefly highlighted below. Note that in principle,
an existing verification language like Dafny could be extended with these features and replace Hex
in the Bolt framework — we do not claim any novel contribution in Hex.

Parameters for Bounds/Dimensions/Sizes. As shown at the top of Fig. 6, Hex supports dec-
laration of parameters, to specify bounds in loop nests and dimensions/sizes in data layouts. In
particular, it supports application and hardware parameters to capture the dimensions, sizes, and
loop bounds, used by the application or fixed by the hardware design, respectively. For parameters
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                                           11



          Program         ⟨prog⟩      ::= app-params 𝑛®1 ; hw-params 𝑛®2 deriving 𝑛®3 ; ⟨𝑠𝑠⟩
        Statements
        ⟨𝑠𝑠⟩ ::= 𝜖 | ⟨𝑠⟩ ; ⟨𝑠𝑠⟩
                                                 −−→
         ⟨𝑠⟩ ::= assign 𝑥 = ⟨𝑒⟩ | assign 𝑥[ ⟨𝑒 1 ⟩] = ⟨𝑒 2 ⟩
                                                 −→
                  | hw_call “𝑖𝑛𝑠𝑡𝑟 ” with 𝑥® = ⟨𝑒⟩ { ⟨𝑠𝑠⟩ }
                  | if ( ⟨𝑒⟩ ) { ⟨𝑠𝑠⟩ } else { ⟨𝑠𝑠⟩ }
                  | [par-]for (𝑥𝑖 = 0 ; 𝑥𝑖 < 𝑛 ; 𝑥𝑖 ++)
                                 → ∼ 𝑥 by 𝑥−−→ = −
                       [where 𝑥−−ℎ𝑤
                                                      →                 −−→
                                                     ⟨𝑒⟩] [invariant ⟨𝑝⟩] { ⟨𝑠𝑠⟩ }
                                        𝑖      ℎ𝑤
                                                                                    −−→
                  | assume ⟨𝑝⟩ | assert ⟨𝑝⟩ | layout-sketch(→        −
                                                                     𝑥𝑖 ∈ 𝑅, 𝑥[ ⟨𝑒 1 ⟩], ⟨𝑒 2 ⟩, ...)
        Terms
                              −→          −→         −→
         ⟨𝑒⟩ ::= 𝑛 | 𝑥 | 𝑥[ ⟨𝑒⟩] | op( ⟨𝑒⟩) | 𝑓 ( ⟨𝑒⟩)
                                                                 −−→
         ⟨𝑝⟩ ::= ⟨𝑒⟩ | ∀ 𝑥®𝑞 < 𝑛,® ⟨𝑒⟩ | ∀ 𝑥®𝑖 < 𝑛,® (⟨𝑒 1 ⟩ ⇒ 𝑥[ ⟨𝑒 2 ⟩] = ⟨𝑒 3 ⟩)
Fig. 6. The syntax of Hex, with terminal symbols for a parameter 𝑛, variable 𝑥, and uninterpreted function 𝑓 .


that depend on aspects of both sides, Hex supports derived parameters that are computed from a
combination of hardware and application parameters.
   All parameters for our illustrative example are shown in lines 1-2 of the bottom half of Fig. 3.
The relationships between parameters are explicitly specified using assumptions at the start of a
Hex program, as shown in lines 3-5. These relationships are important for manipulating IR code
loop nests in the Align step. Note that while parameters are symbolic in the Align and Relate
steps of Bolt, we substitute parameters with concrete values in the Verify step to overcome
solver limitations in handling non-linear arithmetic (detailed in §6). Thus, while Bolt does not
produce correctness proofs for parametric models, we encourage using parameters for scalability: a
parametric accelerator model can be quickly verified under a “small-world” model before trying
larger bounds and sizes. In future work we plan to explore parametric verification using the Lean
interactive theorem prover [42].
Capturing the formal hardware semantics. Hex provides a hw_call statement to explicate
a hardware state update, building on a formal state transition system model of hardware – Bolt
uses an ILA model [23]. In an ILA model, the semantics of a top-level accelerator intrinsic (e.g.,
linear-layer) is captured by an ILA state update, which is defined hierarchically by a sequence
(including iterative loops) of hardware state updates. We use standard techniques to translate the
ILA transition system into a program in Hex, where a hw_call in the Hex program corresponds
one-to-one with a hierarchically-defined ILA hardware state update.1 Additionally, Hex makes
explicit the loops that occur implicitly in the ILA model due to SIMD- or PE-based parallelism, or
via iteration using hardware counters. Sets of buffers or registers that are used to hold tensor data
in the ILA model are represented as multidimensional buffers in Hex.
Loop Constructs. Hex captures tensor map/reduce operations and data movement using range-
based for loops (for) and a parallel variant (par-for), as shown in Fig. 6. The for and par-for loops
use a common syntax, augmented to describe hardware: Each loop introduces a new counter, 𝑥𝑖 ,
that is incremented until it reaches a limit 𝑛. If 𝑛 depends on the application (as either an application
parameter or a derived hardware parameter), then the hardware must track 𝑥𝑖 via one or more
of its registers. These hardware counter registers (in short hardware counters), 𝑥−−ℎ𝑤→ are captured as
1 Essentially, we extract (i) parallel state updates, and (ii) “back-edges” in the ILA control flow, and explicate them with Hex

par-for and for loops, respectively. Sequential logic is expressed via sequences of assign and if statements.
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
12                                                            Grigory Fedyukovich, Sharad Malik, and Aarti Gupta

first-class objects in a where − by clause, where each hardware counter 𝑥ℎ𝑤 ∈ 𝑥−−ℎ𝑤
                                                                                 → is related back
                                                         −→
to the loop counter 𝑥𝑖 by a corresponding expression 𝑒 ∈ ⟨𝑒⟩ that depends only on parameters, loop
counters, and constants. For example, the for loop in Fig. 3, line 12, has a where − by clause that
explicitly associates the loop counter 𝑢 with the hardware counter pe_ctr_in[𝑝], a PE register.
Like other imperative IVLs, Hex also supports annotating loops with loop invariants, ⟨→ −𝑝 ⟩, which
are checked in the standard assume/assert fashion during verification.
Buffers and Tensor Data. Hex provides a standard multidimensional Buffer type for describing
sets of related hardware registers/buffers, e.g., the Buffer, macAcc, in Fig. 3, line 23, corresponds to
the accumulators in FlexASR’s PEs, where macAcc[𝑝, 𝑗] denotes the 𝑗th accumulator of the 𝑝th PE.
Note that as Hex describes physical hardware, all updates to buffers and registers are atomic and
globally visible. Bolt assumes Hex code is free of data races.
Custom Hardware Numerics. Machine learning accelerators sometimes use custom numerical
representations to optimize the trade-off between numerical accuracy and speed. For example,
FlexASR uses multiple fixed-point representations of various bitwidths, and a custom numeric
called AdaptivFloat [52]. Hex does not capture the details of these numerics, treating their operations
as uninterpreted functions on the accelerator side. To allow alignment of loops, we introduce the
same custom numerics and associated operations on the IR code side in the Align step via Hex-based
custom rewrite rules (see next section, §4). This allows verification (in the Verify step of Bolt) to
check program equivalence modulo uninterpreted functions.

4   Align step: Aligning the IR code with loop nests in hardware
In the Align step, users transform the IR code to match the loop nests of the accelerator Hex code,
laying the groundwork for the Relate and Verify steps that follow.

4.1 Sync-Skeleton
We present an abstraction of the accelerator Hex code, called a sync-skeleton, as a template that
guides the user for transforming the IR code. It is a functional program–style template of the
tensor operations in the accelerator Hex code, that are comprised of statically bounded for and
par-for loops. To extract these tensor computations from their imperative context in the accelerator
Hex code, the sync-skeleton abstracts away: (i) the data buffers that store tensor data, and (ii) the
data-movement loops. (Recall that data-movement loops are included in the product programs but
do not need to be aligned.) The sync-skeleton enables use of standard tensor program rewriting
techniques [34, 48] to align the IR code loop nests with the sync-skeleton, and (by extension) with
the tensor-computing loop nests of the accelerator Hex code.
Components of the sync-skeleton. A sync-skeleton represents a tensor computation with five
types of patterns, as shown in Table 1. These patterns are matched with the IR code during the
rewriting process.
Procedure for sync-skeleton extraction. The sync-skeleton is directly constructed from control
flow constructs in the accelerator Hex code (see the running example in Figs. 3 and 4). Loop-free
blocks, sequences of control flow statements, and if statements are respectively mapped to simple
expr, let assignment, and conditional (ite) patterns. A for or par-for loop is extracted if it performs
a computation on tensor data, and is then mapped either (a) to the corresponding map/ reduce
loop pattern if the tensor operation can be determined; or (b) to an unknown loop, otherwise. We
next describe the heuristics to find the corresponding loop pattern for tensor-computing loops, and
to identify the pure data-movement loops that are ignored in the sync-skeleton.
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                     13


  Name              Pattern               In IR code, can match any:
  Simple Expr        ?expr (𝑜𝑝𝑠 )         loop-free computation with the operations in 𝑜𝑝𝑠
  Let Assign- let ? = 𝑣 in 𝑏              let whose value expression matches pattern 𝑣, and whose
  ment                                    body matches pattern 𝑏. Wildcard “?” is any variable name.
  Conditional ite(𝑐, 𝑏𝑡 , 𝑏 𝑓 )           conditional ite with same condition 𝑐 and T/F branches
                                          matching 𝑏𝑡 , 𝑏 𝑓 , resp.
                      𝑛             𝑛
  Map/Reduce        map 𝑏, reduce 𝑏       corresponding map or reduce, resp., with the same loop
  Loop                0             0     bound 𝑛 and body matching the pattern 𝑏
                       𝑛
  Unknown              ?   𝑏              loop with the same loop bound 𝑛, and whose body matches
  Loop                 0                  the pattern 𝑏.
        Table 1. Sync-skeleton components: pure-functional patterns for matching with the IR code.

4.2   Heuristic procedure for loops in the sync-skeleton
To extract the sync-skeleton from the accelerator Hex code, we present a procedure composed
of two heuristics, which respectively decide: (1) which accelerator Hex code loops to include in
the sync-skeleton, and (2) which sync-skeleton loop pattern to use for a given for loop. These
heuristics benefit from Hex loop annotations: hardware-counter annotations on for loops simplify
reasoning about hardware control state (by relating it back to loop counters), and par-for loops,
being parallel, must be map operations to prevent data races.
Sync-skeleton inclusion heuristic. The sync-skeleton should only include loops that perform
tensor computations, i.e., operations on tensor inputs or intermediate tensor data state. In the accel-
erator Hex code, we know which buffers contain tensor inputs through the initial correspondence
between the IR code and accelerator Hex code at the start of the c2a-mapping. We conservatively
identify intermediate tensor data state in the accelerator Hex code as the forward cone-of-influence
of these buffers. A loop should be included in the sync-skeleton if it performs any operation other
than a load/store on tensor inputs/data state; all others perform data movement only and should be
omitted.
Hardware-map heuristic. We identify that a accelerator Hex code loop corresponds to a map
operation by checking for the absence of any accumulator state that is used by reduce operations to
hold intermediate combined results. Since an accumulator is reused across multiple iterations of a
loop, we conservatively test for accumulators with an SMT check for read-write conflicts: given a
                                                                 −−−→
loop, we check whether the same register or buffer element 𝐵[𝑎𝑑𝑑𝑟 ] is written in one iteration and
read/written in another. Formally, let 𝑅𝐵 and 𝑊𝐵 be sets of formulas denoting the read addresses
and write addresses of buffer 𝐵 inside the loop. Let 𝐿𝑝𝑎𝑟𝑠 be the counters of parent loops, and 𝑥𝑙1, 𝑥𝑙2
and 𝐿𝑐ℎ𝑖𝑙𝑑1, 𝐿𝑐ℎ𝑖𝑙𝑑2 be two copies of the loop counter and counters of child loops respectively. Buffer
𝐵 contains accumulator state if the following query is satisfiable:
                      Ü −−−→                                  Ü −−−→
       𝑥𝑙1 ≠ 𝑥𝑙2 ∧        𝑎𝑑𝑑𝑟 = 𝑤® (𝐿𝑝𝑎𝑟𝑠 , 𝑥𝑙1, 𝐿𝑐ℎ𝑖𝑙𝑑1 ) ∧      𝑎𝑑𝑑𝑟 = 𝑜®(𝐿𝑝𝑎𝑟𝑠 , 𝑥𝑙2, 𝐿𝑐ℎ𝑖𝑙𝑑2 ).
                      ® ∈𝑊𝐵
                      𝑤                                         𝑜® ∈𝑊𝐵 ∪𝑅𝐵

If every register or buffer element written in a loop does not contain accumulator state, the loop is
definitely a map; otherwise, it is soundly mapped to an unknown loop in the sync-skeleton.
Effectiveness of heuristics. The inclusion heuristic is effective when the hardware performs
only the tensor computation being specified, and less so when there are other unrelated tensor
computations co-occurring (rare – we did not see examples of this in our evaluations). The hardware-
map is effective when there is low overwriting during map operations, i.e., when an input tensor is
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
14                                                            Grigory Fedyukovich, Sharad Malik, and Aarti Gupta

                                                                                                    Loops
 Arithmetic (A)                                         #     Rewrite rule                 Cat.
                                                                                                    matched
 (𝑎 + 𝑏) ∗ 𝑐 ⇔ 𝑎 ∗ 𝑐 + 𝑏 ∗ 𝑐,            𝑎 −𝑎 ⇔ 0        1    let-substitute               S            0/10
 Structural (S)                                          2    𝑛𝑡 ⇔ 𝑛𝑔 ∗ 𝑛𝑏𝑎𝑛𝑘𝑠             P            0/10
 𝑛 1 ∗𝑛 2        𝑛1    𝑛2                                3    map-tiling                   S            2/10
 map 𝑒 1 ⇔ map map 𝑒 1 [𝑖 ↦→ 𝑛 1 ∗ 𝑖 + 𝑗]
  𝑖=0            𝑖=0   𝑗=0                               4    𝑛𝑜 ⇔ 𝑛 𝑣𝑝 ∗ 𝑛𝑝               P            2/10
                                                         5    𝑛 𝑣𝑝 ⇔ 𝑛 𝑣 ∗ 𝑛𝑝𝑎𝑟            P            2/10
 Parameter substitution (P)
 𝑛𝑡 ⇔ 𝑛𝑔 ∗ 𝑛𝑏𝑎𝑛𝑘𝑠 , 𝑛𝑖 ⇔ 𝑛𝑢 ∗ 𝑛𝑝𝑎𝑟                       6    associativity                A            2/10
                                                        ...   various                      A,S,P        7/10
 Custom numeric (N)                                    15     mul-adpfloat                 N            7/10
 (𝑒 1 : R) ∗ (𝑒 2 : R) ⇔ afloatMul(                    16     acc-add                      N            7/10
                                                 
      𝑒 1 as AFloat(𝑛), 𝑒 2 as AFloat(𝑛)) as R         17     cast-recast                  T            7/10
                                                        ...   various                      all          8/10
 Type casting (T)
                                                       29     map-let-reordering           S           10/10
  ((𝑒 1 as 𝜏1 ) as 𝜏2 ) ⇔ (𝑒 1 as 𝜏2 )
                                                    Table 3. IR code alignment: The sequence of rewrite rules
Table 2. Rewrite rules: Categories of rewrite rules
                                                    used in the running example Align step. Letters in column
for aligning the IR code with the sync-skeleton.
                                                    ’Cat.’ correspond to categories in Table 2.

not in-place replaced by an output tensor (of different dimensions). Note that reduce operations
always have overwriting, so loops with complex data layouts such as non-stationary output
accumulation are correctly categorized by the heuristic as unknown loops in the sync-skeleton.

4.3     Rewriting the IR code
After a sync-skeleton has been extracted, a user aligns the IR code with the sync-skeleton by
using rewriting techniques that replace parts of IR code with equivalent alternatives, based on
a set of source-to-source rewrite rules. Prior work [34, 48] has developed structural rewrite rules
for exploring loop nests via transformations like loop tiling and loop reordering. Bolt combines
structural rules with four other categories of rewrite rules—shown in Table 2—to achieve cheap
and expressive rewriting via hardware guidance. Bolt depends on the correctness of these (simple)
rewrite rules. For our running example, rules from these five categories are used to match all 10
sync-skeleton loops. We highlight three new categories of hardware-guided rewrite rules.
Parameter substitution rules use known relationships between application and hardware param-
eters to guide structural rewrites towards loop nests that reflect hardware bounds and sizes. These
are derived from the preamble of the accelerator Hex code (see the bottom half of Fig. 3, lines 3-5).
Custom numeric rules are user-specified rules for manipulating (uninterpreted) operations in a
custom numeric, for either (i) converting to the custom numeric from real arithmetic (shown in
Table 2), or (ii) converting between custom numeric operations. A user can guide their application
using the sync-skeleton, by preferring rewrites that result in one or more of the required operations
in a simple expr, ?expr (𝑜𝑝𝑠 ) .
Type casting rules are generic rules that simplify and propagate type casts to better reflect numeric
conversions in hardware. The type-casting rule in Table 2 simplifies nested casts.

   For our running example, Table 3 lists the sequence of 29 rewrites that a user performs to align the
IR code with the sync-skeleton. Combining parameter substitution rules with standard structural
and arithmetic rewrites enables matching 7 of 10 loops of the sync-skeleton, i.e., all loops except
4, 9, and 10. By further adding custom numeric and standard type casting rules, the IR code is
transformed to fully match the sync-skeleton, as seen in the last line of Table 3. Custom numeric
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                       15


rewrite rules are specific to each accelerator design, such as the rules used in our running example
(one of which is shown in Table 2). However we found the majority of rewrite rules used (structural,
arithmetic, type casting) are standard across benchmarks (§7.2), and parameter substitution rules
are extracted from the preamble of the accelerator fragment.
Best-effort Matching. For all the case studies we have evaluated so far (§7), the above extraction
heuristics and rewrite rules were effective in matching completely, or most of the loops in the
sync-skeleton. Although we aim to align all IR code loops to those in the sync-skeleton, due to
incompleteness of the rewriting rules in practice, this step may result in a best-effort alignment that
may leave some unmatched loops on either side, i.e., some loops may remain unaligned. We note
that such unaligned loops may require additional invariants and may affect the solver performance
in the Verify step (i.e., it may fail or take more time). However, they do not affect the soundness of
verification. In the future, we plan to investigate equality saturation frameworks like egg [58] for
exploring a larger/complete space of IR code transformations.

5     Relate step: Relating the tensor data layouts
After the loops are potentially aligned in the IR code and accelerator Hex code due the Align step,
the next step in Bolt– the Relate step – is to capture tensor data correspondences between the IR
code and accelerator Hex code as relational loop invariants.

5.1    Layout-Sketch
For each aligned loop in the transformed IR code and the accelerator Hex code, we propose to
develop a Layout-Sketch, that describes tensor data correspondences for assignments in the loop
bodies. Crucially, layout-sketches bridge the gap between pure-functional tensor computations in
the IR code and imperative buffer updates in the accelerator Hex code. We provide several tactics
for a user to specify a layout-sketch in Hex, and to construct relational data layout invariants from
a layout-sketch.
Aligned loops. Intuitively, a layout-sketch for an aligned loop takes an assignment from each side
(e.g., an IR code let𝑇 = ..., and an accelerator Hex code assign 𝐵[ℎ𝑤𝑎𝑒] = ... ), and states that some
tensor element 𝑇 [...] corresponds to the buffer element 𝐵[ℎ𝑤𝑎𝑒] in every loop iteration, assuming
a given correspondence between the reads that these assignments depend on.
   More formally, a layout-sketch is defined by a tuple (𝑅,𝑇 [𝑎𝑒], 𝐵[ℎ𝑤𝑎𝑒], 𝐶 𝑖𝑛 ), where:
       • 𝑅 = {𝑖® ∈ [0®, 𝑛)}
                         ® defines a quantified range over which the input/output correspondence
         holds, based on 𝑖® and 𝑛, ® which are, respectively, the loop counters and loop bounds of the
         loop and its children loops.
       • 𝑇 [𝑎𝑒] is the LHS term of an IR code assignment, which updates a tensor 𝑇 at the multidi-
         mensional index 𝑎𝑒. We call 𝑎𝑒 an access, and express 𝑎𝑒 in terms of 𝑖®, parent loop counters,
         and parameters (based on the map / reduce operations in the IR code).
       • 𝐵[ℎ𝑤𝑎𝑒] is the LHS term of an assign statement in the accelerator Hex code, which updates
         a buffer 𝐵 at the address ℎ𝑤𝑎𝑒. We call ℎ𝑤𝑎𝑒 a hardware access. Hardware accesses are
         written in terms of offsets and hardware counters; we lift them to expressions over loop
         counters and parameters by back-substitution in the loop body.
       • 𝐶 𝑖𝑛 is a set of input correspondences, where each element 𝐶𝑘𝑖𝑛 = (𝑇𝑘 [𝑎𝑒 𝑘 ], 𝐵𝑘 [ℎ𝑤𝑎𝑒 𝑘 ], isOwr)
         denotes a correspondence 𝑇𝑘 [𝑎𝑒 𝑘 ] = 𝐵[ℎ𝑤𝑎𝑒 𝑘 ] in the IR code and accelerator Hex code
         fragments, respectively. The additional flag isOwr is ⊤ (i.e., true) in the case where the
         accelerator Hex code overwrites parts of 𝐵𝑘 [ℎ𝑤𝑎𝑒 𝑘 ] with a different tensor’s data during
         the loop iterations. This case occurs in one of our FlexASR case studies (pooling, §7).
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
16                                                            Grigory Fedyukovich, Sharad Malik, and Aarti Gupta

Layout-sketch example. For our running example (§2), consider a layout-sketch for the aligned
loop over 𝑗 in Fig. 5 (line 1). It is defined as a tuple (𝑅,𝑇 [𝑎𝑒], 𝐵[ℎ𝑤𝑎𝑒], {𝐶 1𝑖𝑛 , 𝐶 2𝑖𝑛 , 𝐶 3𝑖𝑛 }), where:
     • 𝑅 = {(𝑖, 𝑗) ∈ [0, 𝑛𝑝𝑎𝑟 ) × [0, 𝑛𝑝𝑎𝑟 )},
     • 𝑇 [𝑎𝑒] = 𝑠[𝑗],
     • 𝐵[ℎ𝑤𝑎𝑒] = macAcc[𝑝, 𝑗], where 𝑝 is the loop counter of a parent loop.
     • 𝐶 1𝑖𝑛 = (𝑠[𝑗], macAcc[𝑝, 𝑗], ⊥) relates both sides’ accumulators at the start of the iteration,
     • 𝐶 2𝑖𝑛 = (𝑊 [𝑎𝑒 1 (𝑖, 𝑗)], macWeights[𝑝, 𝑖, 𝑗], ⊥)
     • 𝐶 3𝑖𝑛 = (𝑋 [𝑎𝑒 2 (𝑖)], macInputs[𝑝, 𝑖], ⊥)
Unaligned loops. Loops that perform data initialization or data movement, or are unmatched
tensor computation–performing loops, may be unaligned at the end of the Align step. We have two
options for handling them:
     • Treat as an aligned loop: define a layout-sketch for the unaligned loop where the outputs on
        one side are constants in the case of initialization, or the same as the inputs in the case of
        data movement.
     • Treat as a single-side loop: provide invariants manually or unroll the loop during verification.

5.2   Tactics for developing a layout-sketch
We briefly outline some tactics users can follow when developing a layout-sketch. We mainly
consider the important case of layout-sketches for aligned loops, and touch on constructing a
layout-sketch for data-movement/initialization at the end. These tactics are most effective when
sync-skeleton loops are all aligned and the two sides are mostly in lockstep (aside from data
movement).
Tactic 1 (Capture lockstep behavior). A layout-sketch is designed to help users specify data
layout loop invariants when each side computes the same outputs from the same inputs (with
potentially different data layout) in lockstep. For loops whose bodies or inner loop nests may not be
in lockstep (e.g., they are unaligned despite best-effort matching), a layout-sketch may be harder to
develop, or users may need to provide additional invariants in the Verify step.
Tactic 2 (IR code loops identify tensor data state). Every loop in IR code constructs a new tensor
representing the result of the given map/ reduce operation based on the inputs and previously
constructed tensors. The loop should have a layout-sketch that relates the result tensor to a buffer
in the accelerator Hex code, with an input correspondence for each access to an input/previous
tensor in the operation. For each access, users must identify the corresponding hardware access on
the accelerator Hex code side, i.e., a buffer write/read somewhere within the loop body. We plan to
automate this process through dataflow analysis in future work.
Tactic 3 (Copy from nearby/inner aligned loops). The layout-sketch of a pair of aligned loops
can often reuse the quantified range and correspondences of nearby/inner aligned loops, after
quantifying over the outer loop counter. We can reuse the output correspondence because the
inner loop nests on both sides are still constructing the same IR code result tensor. We can reuse
input correspondences because the input and previous tensors are immutable on the IR code side
(although we may need to capture overwriting within the hardware).
Tactic 4 (Data movement / zero-initialization follow standard patterns). For both a data-
movement loop (which can only be in the accelerator Hex code) and a zero-initialization loop,
we do not have an aligned loop on the other side. However, in the case of data-movement, the
source hardware access is related by some layout-sketch (or initial assumption) to some IR code
tensor. Users can relate the destination hardware access to the same tensor by reasoning about
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                     17


address arithmetic. Zero initialization is even easier, as users only need to specify the order in which
tensor/buffer elements are zero’ed, i.e., quantifying over the loop counters of loops surrounding
the zero-initializing assignment.

5.3    Procedure for specifying data layout invariants from a layout-sketch
 Given a layout-sketch (𝑅,𝑇 [𝑎𝑒], 𝐵[ℎ𝑤𝑎𝑒], 𝐶 𝑖𝑛 ) for a loop 𝑙, we provide a procedure to construct
 relational loop invariants that describe the output correspondence between 𝑇 [𝑎𝑒] and 𝐵[ℎ𝑤𝑎𝑒] and
 input correspondences in 𝐶 𝑖𝑛 . For each output/input correspondence, a data layout invariant takes
 the following form:
                              ∀𝑖® ∈ 𝑅. 𝑔(𝑖®, 𝑖𝑐𝑢𝑟 ) ⇒ 𝑇 [𝑎𝑒 (𝑖®)] = 𝐵[ℎ𝑤𝑎𝑒 (𝑖®)],
 stating that the 𝑖®th tensor elements on both sides are equal (i.e., 𝑇 [𝑎𝑒 (𝑖®)] = 𝐵 [ℎ𝑤𝑎𝑒 (𝑖®)]) for all
®𝑖 ∈ 𝑅. The optional guard 𝑔 captures incremental progress (or regress) of the loop, essentially
 considering a subset of 𝑅 based on the current iteration 𝑖𝑐𝑢𝑟 .
Identifying corresponding tensor elements via (shared) loop counters. The data layout
invariant relies on identifying the corresponding tensor elements 𝑇 [𝑎𝑒 (𝑖®)] = 𝐵 [ℎ𝑤𝑎𝑒 (𝑖®)] for 𝑖® ∈ 𝑅.
This requires defining the range 𝑅 and accesses 𝑎𝑒, ℎ𝑤𝑎𝑒 in terms of the same variables 𝑖®. This
requirement can be fulfilled by defining 𝑅 and the accesses in terms of shared loop counters (and
parameters and constants) using the layout-sketch. This underscores the benefit of the Align step,
which provides shared loop counters by synchronizing the loop nests on both sides.
Determining guards from loop context. For an output correspondence, the choice of guard
𝑔 depends on what tensor-computation is being performed in the loop 𝑙. No guard is necessary
(𝑔 = ⊤) when 𝑇 is the accumulator of a reduce loop (𝑙 itself or a parent). Otherwise, 𝑇 is the output
of a map operation, so 𝑔 states that the correspondence holds for elements up to the current loop
iteration, 𝑖𝑐𝑢𝑟 , via the guard 𝑖𝑙 < 𝑖𝑐𝑢𝑟 , where 𝑖𝑙 ∈ 𝑖® corresponds to 𝑙’s loop counter.
   For an input correspondence (𝑇𝑘 [𝑎𝑒 𝑘 ], 𝐵𝑘 [ℎ𝑤𝑎𝑒]𝑘 , isOwr𝑘 ), a guard is necessary if the accelerator
Hex code’s buffer is being overwritten (i.e., isOwr). In this case, a guard 𝑖𝑙 ≥ 𝑖𝑐𝑢𝑟 is used to state
that the input correspondence holds for the inputs of remaining loop iterations.

6     Verify step: Verifying the product program
The last step in Bolt constructs a well-aligned product program in Hex from the transformed IR
code and the accelerator Hex code, along with annotations of the relational data layout invariants.
We automate this construction using standard techniques [4, 12]. Bolt then uses an automated
procedure for verifying the product program based on generating Verification Conditions (VCs),
using annotations at loop boundaries (in the style of Dafny [30]), and checking their validity using
an SMT solver (Z3 [13]). Our SMT formulas contain theories of bitvectors, uninterpreted functions,
arrays, and linear integer arithmetic. We review the VC-generation procedure and highlight some
design choices below.
Background: VC generation from product programs. Fig. 7 depicts the standard procedure
we use to generate verification conditions from a Hex product program. Essentially, the (product)
program is “cut” at its loops to create a cut-point graph, a graph whose nodes are loop heads
(and program start/end points), and whose edges are loop-free program segments. Each node is
annotated with a Hoare-style specification, and each edge is used for generating a VC that must
be proved valid via an SMT solver. If the SMT solver can prove the validity of every VC, then we
have successfully proved the equivalence of the IR code and accelerator Hex code in the product
program. If a VC is invalid, either the assumed annotation is too weak, or the asserted annotation
is too strong, or the program contains a bug.
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
18                                                            Grigory Fedyukovich, Sharad Malik, and Aarti Gupta




        Fig. 7. Bolt uses standard techniques to generate SMT verification conditions from the TPP.


      Invariant category    Example
      Data layout           ∀ 𝑡𝑔 ∈ [0, 𝑛𝑏𝑎𝑛𝑘𝑠 ), 𝑣 ∈ [0, 𝑛 𝑣 ). (𝑡𝑔 < 𝑡 =⇒ 𝑋 [𝑡𝑔 , 𝑣] = buf[𝑐 1𝑡𝑔 + 𝑐 2𝑣])
      Loop bound            0 ≤ 𝑢 < 𝑛𝑢
      Hardware-counter      ∀ 𝑝 ∈ [0, 𝑛𝑝 ).ctr[𝑝] = 𝑖𝑡𝑒 (𝑢 < 𝑛𝑢 , 𝑢, 0)
      WORM                  addrOff = BASE_OUT + 𝑛𝑝 ∗ ctrTsg
                                Table 4. Verify step: Categories of Invariants


Avoiding non-linear arithmetic. The VCs generated for our product programs often include
address arithmetic with products of parameters. If these parameters are symbolic, the VCs have
non-linear arithmetic formulae, which are notoriously difficult to solve with standard SMT solvers.
Our verifier avoids solver limitation (for now) by substituting parameters with concrete values. Note
that with advances in SMT solvers, or by exploring use of interactive theorem provers like Lean [42],
we hope to support parametric verification in the future, such that program equivalence is verified
for all sizes/dimensions represented by the parameters.
Handling quantifiers. VCs from a Hex program typically have assumptions and assertions with
quantifiers, e.g., from layout-sketch-based relational invariants. SMT solvers often struggle to reason
about quantifiers. Our strategy is to remove the universal quantifiers by bounded flattening [36]
(up to constant bounds in the concrete parameters) in the data layout invariants when used as
assumptions.

6.1    Categories of useful invariants
We list the categories of loop invariants used in Bolt in Table 4, along with examples. These
categories were sufficient in all our evaluations (§7). In addition to data layout invariants (guided
by the layout-sketch, §5), verification typically needs invariants on loop bounds, hardware counters
and registers, briefly described below. Our verifier in Bolt uses simple static analyses to derive
many (but not all) required invariants in these categories.
Loop bound invariants. The for and par-for in Hex are standardized to start at zero and increment
at the end of the loop up to some parameter loop bound. This is captured as a loop bound invariant.
Hardware-counter invariants. To analyze hardware address arithmetic, it is useful to have
invariants for the hardware counters identified in the where-by clauses of a for loop. For example,
the hardware-counter invariant in Table 4 shows a hardware counter that resets on loop end.
WORM invariants. Hardware designs commonly save (computed) address offsets, and configura-
tion information in hardware registers for reuse. We have found that capturing this write-once-
read-many (WORM) pattern as an invariant is useful, especially when the written value is read
much later in another loop.
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                       19


7     Case Studies and Evaluation
We have developed a proof-of-concept prototype for the Bolt/Hex framework and evaluated it for
verifying c2a-mappings for two recent open-source ML accelerators described below. We report
some key statistics (Table 5) for the three main steps (Align, Relate, and Verify) of Bolt, and the
verification results (Table 6) for the product programs using the Z3 SMT solver [13].

7.1    Case studies: Compiler-to-Accelerator Mappings
For our evaluation we used accelerators with available formal hardware semantics. To the best of
our knowledge, thus far, only the 3LA compiler framework [22] provides open-source hardware
semantics for ML accelerators. It does so for three accelerators – FlexASR, HLSCNN, and VTA2 . It
used c2a-mappings for code generation3 , but did not address proving their correctness. Of these
accelerators, VTA has fine-grained mappings, which is not the focus of this work, and thus not
considered. We consider the other two accelerators, and their mappings (described below) are of
significant complexity; verifying their correctness provides a proof of concept of Bolt’s capabilities.
(We will open-source the mappings used in our evaluations, which we converted from the original
DSLs used in 3LA to IR and Hex code for verification.)
FlexASR Accelerator. FlexASR [51] supports various operations used for automatic speech
recognition, including linear-layer, pooling, etc. Some operations are parallelized across multiple
PEs and others are performed directly using data in a global buffer. We verify the linear-layer and
pooling as representative mappings in these two categories, respectively.
     • FlexASR Pooling (FP). FlexASR supports three pooling operations, called max-, add-, and
       mean-pooling. 3LA contained c2a-mappings for the first two; we constructed a similar
       mapping for add-pooling. We used (nearly) the same Align and Relate steps on all three
       (modulo renaming some variables, loops, etc.), so we describe them together in Table 5.
       However, in the Verify step, we check each mapping individually to prove its correctness.
     • FlexASR Linear-layer (FLL). FlexASR linear-layer has been detailed as the running example,
       here we focus on its role as a challenge case study: it has the largest mapping, with significant
       hardware data-parallelism and data-movement.

HLSCNN Accelerator. HLSCNN is a convolutional-layer accelerator [57] that supports the
following operations:
     • HLSCNN 2D Convolution (C2D): HLSCNN supports a 2D convolution operation that has
       variable kernel sizes, and supports batch computation (over filters and channels).
     • HLSCNN C2D Accumulative (C2D+): When verifying C2D, we noted a hardware flag—
       unused by the 3LA mapping—for accumulating outputs onto previous results. As the flag
       significantly changes data layout correspondences, we created and verified C2D+, a mapping
       with the flag enabled.

7.2    Bolt by the numbers
Table 5 lists some key statistics about each Bolt step as it was applied to our case studies. At first
glance, the given mappings (near the top) look simple, with virtually no loops in the MMIO code
(see # loops in MMIO code in the second row).
Accelerator Hex code. Detailing the MMIO code using Hex (the next set of rows) reveals its
hardware complexity — e.g., the code for FlexASR linear-layer (FLL) now has 28 loops, max loop
2 ILAs models for all three accelerators are available at https://github.com/PrincetonUniversity/IMDb/
3 Code available at https://github.com/uwsampl/3la-evaluation
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
20                                                            Grigory Fedyukovich, Sharad Malik, and Aarti Gupta

                                             Mapping         FP   FLL     C2D C2D+
                         Given code
                         # loops in IR code                   2       5      4       4
                         # loops in MMIO code                 0       1      0       0
                         Accelerator Hex code
                         # application params.                2      3       6       6
                         # hardware params.                   3      3       1       1
                         # derived params.                    2      6       5       5
                         # loops in Hex code
                          ↰                                   4     28      12      12
                          ↰  max nesting depth                4      7       8       8
                          ↰  # par-for loops                  1     18       4       4
                             # for loops                      3     10       8       8
                         Align step
                         # loops in sync-skeleton             4     10       8       8
                         # data-movement loops                0     18       4       4
                         # Parameter Subst. Rules             2      5       5       5
                         # Custom Numeric Rules               3      7       3       3
                         # rewrites to align                 12     29      27      27
                         # loops in aligned IR code           4     11       8       8
                         # aligned loops                      4     10       8       8
                         Relate step
                         # layout-sketches                    4     11      12       8
                         # data layout invariants            11     31      10       5
                         Verify step
                         # loops in product program           4     29      12      12
                         # manual invariants                 11     25      10      10
                         # VC queries                        10     15      15      15
          Table 5. Bolt Evaluation: Key statistics for various steps in case studies (listed in §7.1).


nesting depth of 7, and significant hardware data-parallelism (many par-for loops). Various loop
bounds and dimensions are captured via application, hardware, and derived parameters in the
accelerator Hex code.

Align. Each sync-skeleton (extracted from the accelerator Hex code) includes several loops which
guide the user in transforming the IR code for loop alignment. Our heuristic extraction procedure
omits the many pure-data movement loops, allowing the user to focus on tensor-computation loops
in the accelerator code. Users transform the IR code to match the sync-skeleton using our system
of rewriting rules, which we customize to the accelerator using: (1) parameter substitution rules
extracted from the accelerator Hex code preamble, and (2) custom numeric rewrite rules (discussed
in §4.3). As an indicator of user-effort, we report the number of rewriting steps needed to align the
IR code with the sync-skeleton. We note that the aligned IR code successfully matches every loop
in the sync-skeleton (# aligned loops = # loops in sync-skeleton), with only one unaligned IR loop
(in FlexASR linear-layer, FLL) that performs data initialization.

Relate. Following the tactics we provide, users specify layout-sketches for aligned loops. Some
loops require more than one layout-sketch, e.g., in HLSCNN 2D convolution (C2D), extra layout-
sketches specify how HLSCNN initializes accumulators as it iterates. In contrast, C2D+ foregoes
these extra layout-sketches, as accumulators on both sides correspond at all times. We report the
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                   21


                                                            Parameters                   Verif.
                Mapping
                                                            (HW)     ; (App.)            time (s)
               (FP) Add-pool                                (2, 4)   ; (4, 4)                   1
               (4 loops, max depth 4)                       (16, 16) ; (32, 64)              361
               (FP) Max-pool
                                                            (16, 16)    ; (32, 64)           313
               (4 loops, max depth 4)
               (FP) Mean-pool
                                                            (16, 16)    ; (32, 64)           391
               (4 loops, max depth 4)
                                                            (4, 2, 8) ; (4, 16, 16)         423
               (FLL) Linear-layer
                                                            (8, 4, 8) ; (8, 32, 32)       18351
               (29 loops, max depth 7)
                                                            (16, 4, 16) ; (16, 64, 64)      TO
                                                            2 ; (2, 2, 5, 5, 3, 3)          413
               (C2D) 2D convolution
                                                            4 ; (8, 8, 12, 12, 3, 3)        TO
               (12 loops, max depth 8)
                                                            8 ; (8, 8, 12, 12, 3, 3)          –
                                                            2 ; (2, 2, 5, 5, 3, 3)            4
               (C2D+) 2D conv. with accum. flag
                                                            4 ; (8, 8, 12, 12, 3, 3)       7750
               (12 loops, max depth 8)
                                                            8 ; (8, 8, 12, 12, 3, 3)      20579
Table 6. SMT verification results for mappings, with varying concrete parameter values. (TO indicates a
timeout of 6 hours.) The mappings (in the first column) also show # loops in the product program and
maximum loop nesting depth (max depth) in parentheses.


number of data layout invariants, which is high for FLL, the most complex mapping (29 loops in
the product program).
Verify. We automatically construct a product program based on aligned loops (note that # loops in
product program = # loops in accelerator Hex code + # loops in aligned IR code − # aligned loops).
Users annotate the product program with data layout invariants and additional manual invariants
in the different categories (§6)—numbers are higher for more complex mappings (e.g., FLL). Thanks
to the aligned loop nests and relational invariants, our verifier decomposes the product program
into multiple VC queries that are checked using the Z3 SMT solver [13], to prove equivalence of
the given IR code and accelerator Hex code.

7.3   Results for the Verify step
Table 6 shows the time taken to verify the correctness of mappings using the Z3 [13] SMT solver.
Experiments were run with a 6-hour timeout on a 16-core Intel Xeon processor (3.8 GHz CPU, 256
GiB RAM). Times are reported for different values of the concrete hardware/application parameters,
which roughly signal the scale of the verification instance. The last row of a mapping reflects
parameter values of real hardware; in some cases, we also report results for down-scaled versions of
the hardware with smaller parameter values (for faster verification), while still preserving original
loop nests and data layouts. We discuss highlights from the results.
Successful verification of mappings with respect to a formal hardware semantics. Bolt can
successfully verify complex mappings covering a variety of coarse-grained ML operations across
two accelerators. Four mappings were successfully verified with parameter values used by the
actual hardware. The remaining two were verified with downscaled parameters, still capturing key
hardware features like hardware data parallelism, data movement, and complex address arithmetic.
Variations across case studies. In general, mappings with more loops and loop nesting take
longer to verify, as they lead to many VC queries that are also more complex. Keeping loop nests
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
22                                                            Grigory Fedyukovich, Sharad Malik, and Aarti Gupta

constant, C2D and C2D+ show that the more data layout invariants a mapping needs, the longer the
verification time. These speed differences highlight the importance of loop nests and data layouts
when verifying mappings.
Handling of unaligned loops. We experimented with providing sync-skeletons and manual
invariants for unaligned loops rather than unrolling them (the tradeoff discussed in §5.1) for our
mappings with unaligned loops (FLL, C2D, C2D+). Although the additional user-burden reduced
verification time up to 52% for FlexASR linear-layer (FLL), it led to similar or increased time for the
others. Therefore, we unroll unaligned loops as a default, to minimize user burden.
Comparison with standard verification techniques. We attempted to verify our smallest
equivalence checking problem, row 1 of Table 6, using a state-of-the-art Constrained Horn Clause
(CHC) verifier Z3/Spacer [13, 26]. We applied it on the same well-aligned product program, but
without providing any invariants. Even for this small problem, Z3/Spacer failed to complete
verification with a 1-day timeout. Similarly, we tried SMT-based bounded model checking (BMC) [5]
using Z3, and this too failed on even the smallest case studies due to extensive loop unrolling in
nested loops. (We omitted experiments on larger problems/mappings.)

8   Related Work
Verified Compilers for ML. Liu et al. [33, 34] and Courant and Leroy [11] present verified
optimizing compilers from high-level IRs (tensor and affine programs, resp.) to C (or C-like) code.
Both verify compiler passes via an interactive theorem prover (Rocq). Neither considers verification
against loop nests and data layout fixed by hardware, nor proves correctness with respect to a
hardware semantics. CompCert [31] provides certified compilation of C code targeting hardware
(PowerPC, ARM, x86, RISC-V), but does not support coarse-grained ML accelerator intrinsics.
Translation Validation for ML compilers. Melchert et al. [37, 38] design and verify a custom
compilation flow for coarse-grained reconfigurable array (CGRA) accelerators, where they perform
translation validation of individual compiler steps, using information from the compiler. Unlike
Bolt, they do not address verification of black-box mappings for existing coarse-grained accelera-
tors, such as FlexASR. Exo [24] and Mosaic [2] are recent ML compilers with verification support.
Exo optimizes affine programs via user-specified schedules of high-level transformations; it verifies
these transformations using an effect analysis. Mosaic optimizes (sparse) tensor algebra code via
auto-scheduling of high-level transformations, which it verifies using SMT-based assertion checking
(e.g., of tensor bounds, sizes, etc). Both support macro-based accelerator-specific code generation
(through libraries and external functions, respectively), but neither verifies these c2a-mappings with
respect to a formal hardware semantics. Bolt addresses this verification gap for these compilers.
   Pouchet et al. [46] verify the equivalence of High Level Synthesis (HLS) programs (written in
C/C++) resulting from source-to-source transformations for optimizing ML operations (e.g., matrix
multiply), achieving impressive performance. However, their technique is restricted to programs
where branches and loop bounds are statically interpretable—essentially it unrolls all loops—and
they depend on the correctness of the HLS compiler. In contrast, Bolt checks program equivalence
in general, uses loop invariants to avoid loop unrolling, and considers a formal hardware semantics.
Verdoolaege et al. [55] verify affine program transformations via dataflow analysis, identifying data
correspondences similar to our Relate step. Their approach requires identical operations on both
sides of the equivalence problem (modulo associativity and commutativity) and does not verify
correctness with respect to a formal hardware semantics.
ML compiler frameworks. Halide [47] is a language and compiler for high-performance comput-
ing applications, including machine learning. Clément and Cohen [10] verify compilation of Halide
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                                     23


code to an imperative language, using tensor-array relationships similar to those of our Relate step.
However, their approach relies on compiler-provided annotations and they do not target hardware
or consider a formal hardware semantics. Many Halide extensions define compiler-to-accelerator
mappings to ML accelerators [20, 27, 32, 50, 56]; the majority lack a formal hardware semantics for
their accelerator. 3LA [22] automatically identifies offloading opportunities based on compiler-to-
accelerator mappings. TVM [8] with BYOC [9] and MLIR [29] allow user-specified compilation
passes that support hardware accelerators, but they have not been verified. TensorLift [17] automat-
ically extracts tensor-level formal semantics from RTL designs for use by MLIR compilation flows.
The authors formally verify the modeling of some hardware subsystems (e.g., a PE unit), but do not
verify compiler-to-accelerator mappings. Several compilers have been developed for synthesizing
hardware circuits to accelerate ML applications [14, 15, 39]. Synthesis passes are trusted and do
not require code generation.

Automated verification of product programs. Our work is inspired by many prior efforts in
automated verification of product (or relational) programs. Some representative efforts include
applications in compiler validation [16, 59], security verification [1, 3], and differential program
analysis [19, 28]. Prior work has highlighted the importance of loop alignment and presented
techniques to exploit alignment opportunities [4, 21, 25, 49, 53, 59], including use of CHC solvers [12,
40, 54]. The Align and Relate steps of Bolt are inspired by these prior efforts. In addition, we
have proposed the sync-skeleton and the layout-sketch to guide loop alignment and annotation of
relational invariants, respectively. We note that none of the prior work has considered problem
instances with complexity similar to our case studies, in terms of number of loops, deeply nested
loops, and multidimensional and dynamic data layouts.

9   Conclusions and Future Directions
In this work we introduce Bolt, the first framework for verifying compiler-to-accelerator mappings
for coarse-grained ML accelerator intrinsics, with respect to a formal hardware semantics. We use
program equivalence techniques based on product programs, where a sync-skeleton additionally
guides the user in transforming the IR code to align with the loop nests in the accelerator Hex code,
and a layout-sketch provides a sketch for a user to annotate relational data layout invariants on
aligned loops. Our evaluation shows that Bolt can successfully verify many complex mappings for
recent open-source ML accelerators, including those with multiple deeply-nested loops and dynamic
data layouts. In future work, we would like to automatically generate some key invariants using
automated synthesis techniques, and develop a comprehensive set of rewriting transformations via
equality saturation.

References
 [1] José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, François Dupressoir, and Michael Emmi. Verifying constant-time
     implementations. In USENIX, pages 53–70. USENIX Association, 2016.
 [2] Manya Bansal, Olivia Hsu, Kunle Olukotun, and Fredrik Kjolstad. Mosaic: An interoperable compiler for tensor algebra.
     Proceedings of the ACM on Programming Languages, 7(PLDI):394–419, 2023.
 [3] G. Barthe, P.R. D’Argenio, and T. Rezk. Secure information flow by self-composition. In Proceedings. 17th IEEE
     Computer Security Foundations Workshop, 2004., pages 100–114, June 2004.
 [4] Gilles Barthe, Juan Manuel Crespo, and César Kunz. Relational verification using product programs. In Michael Butler
     and Wolfram Schulte, editors, FM 2011: Formal Methods, pages 200–214, Berlin, Heidelberg, 2011. Springer Berlin
     Heidelberg.
 [5] Armin Biere, Alessandro Cimatti, Edmund M. Clarke, and Yunshan Zhu. Symbolic Model Checking without BDDs. In
     TACAS, volume 1579 of LNCS, pages 193–207. Springer-Verlag, 1999.
 [6] François Bobot, Jean-Christophe Filliâtre, Claude Marché, and Andrei Paskevich. Why3: Shepherd your herd of provers.
     In Boogie 2011: First International Workshop on Intermediate Verification Languages, pages 53–64, 2011.
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
24                                                            Grigory Fedyukovich, Sharad Malik, and Aarti Gupta

 [7] Aaron R Bradley. Sat-based model checking without unrolling. In International Workshop on Verification, Model
     Checking, and Abstract Interpretation, pages 70–87. Springer, 2011.
 [8] Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin Zheng, Eddie Yan, Haichen Shen, Meghan Cowan, Leyuan Wang,
     Yuwei Hu, Luis Ceze, et al. TVM: An automated end-to-end optimizing compiler for deep learning. In 13th USENIX
     Symposium on Operating Systems Design and Implementation (OSDI 18), pages 578–594, 2018.
 [9] Zhi Chen, Cody Hao Yu, Trevor Morris, Jorn Tuyls, Yi-Hsiang Lai, Jared Roesch, Elliott Delaye, Vin Sharma, and Yida
     Wang. Bring your own codegen to deep learning compiler. arXiv preprint arXiv:2105.03215, 2021.
[10] Basile Clément and Albert Cohen. End-to-end translation validation for the halide language. Proceedings of the ACM
     on Programming Languages, 6(OOPSLA1):1–30, 2022.
[11] Nathanaël Courant and Xavier Leroy. Verified code generation for the polyhedral model. Proceedings of the ACM on
     Programming Languages, 5(POPL):1–24, 2021.
[12] Emanuele De Angelis, Fabio Fioravanti, Alberto Pettorossi, and Maurizio Proietti. Relational verification through horn
     clause transformation. In Xavier Rival, editor, Static Analysis, pages 147–169, Berlin, Heidelberg, 2016. Springer Berlin
     Heidelberg.
[13] Leonardo De Moura and Nikolaj Bjørner. Z3: an efficient smt solver. In Proceedings of the Theory and Practice of Software,
     14th International Conference on Tools and Algorithms for the Construction and Analysis of Systems, TACAS’08/ETAPS’08,
     page 337–340, Berlin, Heidelberg, 2008. Springer-Verlag.
[14] Schuyler Eldridge, Prithayan Barua, Aliaksei Chapyzhenka, Adam Izraelevitz, Jack Koenig, Chris Lattner, Andrew
     Lenharth, George Leontiev, Fabian Schuiki, Ram Sunder, et al. Mlir as hardware compiler infrastructure. In Workshop
     on Open-Source EDA Technology (WOSET), volume 3, 2021.
[15] Hadi Esmaeilzadeh, Soroush Ghodrati, Jie Gu, Shiyu Guo, Andrew B. Kahng, Joon Kyung Kim, Sean Kinzer, Rohan
     Mahapatra, Susmita Dey Manasi, Edwin Mascarenhas, Sachin S. Sapatnekar, Ravi Varadarajan, Zhiang Wang, Hanyang
     Xu, Brahmendra Reddy Yatham, and Ziqing Zeng. Verigood-ml: An open-source flow for automated ml hardware
     synthesis. In 2021 IEEE/ACM International Conference On Computer Aided Design (ICCAD), pages 1–7, 2021.
[16] Grigory Fedyukovich, Arie Gurfinkel, and Natasha Sharygina. Property directed equivalence via abstract simulation.
     In CAV, volume 9780, Part II, pages 433–453. Springer-Verlag, 2016.
[17] Ruijie Gao, Haoran Jin, Jirong Yang, and Nathaniel Bleier. Tensorlift: Automatic extraction of tensor-level isa semantics
     from accelerator rtl via mlir semantic lifting. In IEEE/ACM International Conference on Computer-Aided Design, ICCAD
     ’26, New York, NY, USA, 2026. Association for Computing Machinery.
[18] Hasan Genc, Seah Kim, Alon Amid, Ameer Haj-Ali, Vighnesh Iyer, Pranav Prakash, Jerry Zhao, Daniel Grubb, Harrison
     Liew, Howard Mao, Albert Ou, Colin Schmidt, Samuel Steffl, John Wright, Ion Stoica, Jonathan Ragan-Kelley, Krste
     Asanovic, Borivoje Nikolic, and Yakun Sophia Shao. Gemmini: Enabling systematic deep-learning architecture
     evaluation via full-stack integration. In 2021 58th ACM/IEEE Design Automation Conference (DAC), pages 769–774.
     IEEE, 2021.
[19] Benny Godlin and Ofer Strichman. Regression verification. In DAC, pages 466–471. ACM, 2009.
[20] Peng Gu, Xinfeng Xie, Yufei Ding, Guoyang Chen, Weifeng Zhang, Dimin Niu, and Yuan Xie. ipim: Programmable
     in-memory image processing accelerator using near-bank architecture. In 2020 ACM/IEEE 47th Annual International
     Symposium on Computer Architecture (ISCA), pages 804–817. IEEE, 2020.
[21] Ameer Hamza and Grigory Fedyukovich. Lockstep composition for unbalanced loops. In Sriram Sankaranarayanan
     and Natasha Sharygina, editors, Tools and Algorithms for the Construction and Analysis of Systems - 29th International
     Conference, TACAS 2023, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2022,
     Paris, France, April 22-27, 2023, Proceedings, Part II, volume 13994 of Lecture Notes in Computer Science, pages 270–288.
     Springer, 2023.
[22] Bo-Yuan Huang, Steven Lyubomirsky, Yi Li, Mike He, Gus Henry Smith, Thierry Tambe, Akash Gaonkar, Vishal
     Canumalla, Andrew Cheung, Gu-Yeon Wei, Aarti Gupta, Zachary Tatlock, and Sharad Malik. Application-level
     validation of accelerator designs using a formal software/hardware interface. ACM Trans. Des. Autom. Electron. Syst.,
     29(2), feb 2024.
[23] Bo-Yuan Huang, Hongce Zhang, Pramod Subramanyan, Yakir Vizel, Aarti Gupta, and Sharad Malik. Instruction-level
     abstraction (ila): A uniform specification for system-on-chip (soc) verification. ACM Trans. Des. Autom. Electron. Syst.,
     24(1), dec 2018.
[24] Yuka Ikarashi, Gilbert Louis Bernstein, Alex Reinking, Hasan Genc, and Jonathan Ragan-Kelley. Exocompilation for
     productive programming of hardware accelerators. In Proceedings of the 43rd ACM SIGPLAN International Conference
     on Programming Language Design and Implementation, PLDI 2022, page 703–718, New York, NY, USA, 2022. Association
     for Computing Machinery.
[25] Marie-Christine Jakobs. Peqcheck: Localized and context-aware checking of functional equivalence (technical report).
     arXiv preprint arXiv:2101.09042, 2021.
Verification of Compiler-to-Accelerator Mappings for Machine Learning Accelerators                                         25


[26] Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. Smt-based model checking for recursive programs. Formal
     Methods in System Design, 48:175–205, 2016.
[27] Ville Korhonen, Pekka Jääskeläinen, Matias Koskela, Timo Viitanen, and Jarmo Takala. Rapid customization of image
     processors using halide. In 2015 IEEE Global Conference on Signal and Information Processing (GlobalSIP), pages 629–633.
     IEEE, 2015.
[28] Shuvendu K. Lahiri, Kenneth L. McMillan, Rahul Sharma, and Chris Hawblitzel. Differential assertion checking. In
     FSE, pages 345–355. ACM, 2013.
[29] Chris Lattner, Mehdi Amini, Uday Bondhugula, Albert Cohen, Andy Davis, Jacques Pienaar, River Riddle, Tatiana
     Shpeisman, Nicolas Vasilache, and Oleksandr Zinenko. Mlir: Scaling compiler infrastructure for domain specific
     computation. In 2021 IEEE/ACM International Symposium on Code Generation and Optimization (CGO), pages 2–14.
     IEEE, 2021.
[30] K. Rustan M. Leino. Dafny: An automatic program verifier for functional correctness. In Proceedings of the 16th
     International Conference on Logic for Programming, Artificial Intelligence, and Reasoning, LPAR’10, page 348–370, Berlin,
     Heidelberg, 2010. Springer-Verlag.
[31] Xavier Leroy. Formal verification of a realistic compiler. Communications of the ACM, 52(7):107–115, 2009.
[32] Jiajie Li, Yuze Chi, and Jason Cong. Heterohalide: From image processing dsl to efficient fpga acceleration. In
     Proceedings of the 2020 ACM/SIGDA International Symposium on Field-Programmable Gate Arrays, FPGA ’20, page
     51–57, New York, NY, USA, 2020. Association for Computing Machinery.
[33] Amanda Liu, Gilbert Bernstein, Adam Chlipala, and Jonathan Ragan-Kelley. A verified compiler for a functional tensor
     language. Proceedings of the ACM on Programming Languages, 8(PLDI):320–342, 2024.
[34] Amanda Liu, Gilbert Louis Bernstein, Adam Chlipala, and Jonathan Ragan-Kelley. Verified tensor-program optimization
     via high-level scheduling rewrites. Proc. ACM Program. Lang., 6(POPL), jan 2022.
[35] Qiaoyi Liu, Jeff Setter, Dillon Huff, Maxwell Strange, Kathleen Feng, Mark Horowitz, Priyanka Raina, and Fredrik
     Kjolstad. Unified buffer: Compiling image processing and machine learning applications to push-memory accelerators.
     ACM Trans. Archit. Code Optim., 20(2), March 2023.
[36] William McCune. Mace 2.0 reference manual and guide. arXiv preprint cs/0106042, 2001.
[37] Jackson Melchert, Yuchen Mei, Kalhan Koul, Qiaoyi Liu, Mark Horowitz, and Priyanka Raina. Cascade: An application
     pipelining toolkit for coarse-grained reconfigurable arrays. IEEE Transactions on Computer-Aided Design of Integrated
     Circuits and Systems, 43(10):3055–3067, 2024.
[38] Jackson Melchert, Caleb Terrill, Aron Ricardo Perez-Lopez, Clark Barrett, and Priyanka Raina. Automated translation
     validation of a compiler for statically scheduled accelerators. In CONFERENCE ON FORMAL METHODS IN COMPUTER-
     AIDED DESIGN–FMCAD 2025, pages 198–208. TU Wien Academic Press, 2025.
[39] Marco Minutoli, Vito Giovanni Castellana, Cheng Tan, Joseph Manzano, Vinay Amatya, Antonino Tumeo, David
     Brooks, and Gu-Yeon Wei. Soda: a new synthesis infrastructure for agile hardware design of machine learning
     accelerators. In Proceedings of the 39th International Conference on Computer-Aided Design, ICCAD ’20, New York, NY,
     USA, 2020. Association for Computing Machinery.
[40] Dmitry Mordvinov and Grigory Fedyukovich. Synchronizing constrained horn clauses. In LPAR-21, 21st International
     Conference on Logic for Programming, Artificial Intelligence and Reasoning, volume 46 of EPiC Series in Computing,
     pages 338–355. EasyChair, 2017.
[41] Thierry Moreau, Tianqi Chen, Luis Vega, Jared Roesch, Eddie Yan, Lianmin Zheng, Josh Fromm, Ziheng Jiang, Luis Ceze,
     Carlos Guestrin, and Arvind Krishnamurthy. A hardware–software blueprint for flexible deep learning specialization.
     IEEE Micro, 39(5):8–16, 2019.
[42] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language. In International
     Conference on Automated Deduction, pages 625–635. Springer, 2021.
[43] George C Necula. Translation validation for an optimizing compiler. In Proceedings of the ACM SIGPLAN 2000
     conference on Programming language design and implementation, pages 83–94, 2000.
[44] Preeti Ranjan Panda. Systemc: a modeling platform supporting multiple design abstractions. In Proceedings of the
     14th International Symposium on Systems Synthesis, ISSS ’01, page 75–80, New York, NY, USA, 2001. Association for
     Computing Machinery.
[45] Amir Pnueli, Michael Siegel, and Eli Singerman. Translation validation. In International Conference on Tools and
     Algorithms for the Construction and Analysis of Systems, pages 151–166. Springer, 1998.
[46] Louis-Noël Pouchet, Emily Tucker, Niansong Zhang, Hongzheng Chen, Debjit Pal, Gabriel Rodríguez, and Zhiru Zhang.
     Formal verification of source-to-source transformations for hls. In Proceedings of the 2024 ACM/SIGDA International
     Symposium on Field Programmable Gate Arrays, pages 97–107, 2024.
[47] Jonathan Ragan-Kelley, Connelly Barnes, Andrew Adams, Sylvain Paris, Frédo Durand, and Saman Amarasinghe.
     Halide: a language and compiler for optimizing parallelism, locality, and recomputation in image processing pipelines.
     In Proceedings of the 34th ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI ’13,
Akash Gaonkar, Mike He, Yi Li, Bo-Yuan Huang, Andrew Cheung, Vishal Canumalla, Gus Henry Smith, Zachary Tatlock,
26                                                            Grigory Fedyukovich, Sharad Malik, and Aarti Gupta

     page 519–530, New York, NY, USA, 2013. Association for Computing Machinery.
[48] Gus Henry Smith, Andrew Liu, Steven Lyubomirsky, Scott Davidson, Joseph McMahan, Michael Taylor, Luis Ceze,
     and Zachary Tatlock. Pure tensor program rewriting via access patterns (representation pearl). In Proceedings of the
     5th ACM SIGPLAN International Symposium on Machine Programming, MAPS 2021, page 21–31, New York, NY, USA,
     2021. Association for Computing Machinery.
[49] Marcelo Sousa and Isil Dillig. Cartesian hoare logic for verifying k-safety properties. In Proceedings of the 37th ACM
     SIGPLAN Conference on Programming Language Design and Implementation, PLDI ’16, page 57–69, New York, NY, USA,
     2016. Association for Computing Machinery.
[50] John A. Stratton, Jyothi Krishna Viswakaran Sreelatha, Rajiv Ravindran, Sachin Sudhakar Dake, and Jeevitha
     Palanisamy. Optimizing halide for digital signal processors. In 2020 IEEE Workshop on Signal Processing Systems (SiPS),
     pages 1–6, 2020.
[51] Thierry Tambe, En-Yu Yang, Glenn G. Ko, Yuji Chai, Coleman Hooper, Marco Donato, Paul N. Whatmough, Alexander M.
     Rush, David Brooks, and Gu-Yeon Wei. A 25mm2 soc for iot devices with 18ms noise robust speech-to-text latency
     via bayesian speech denoising and attention-based sequence-to-sequence dnn speech recognition in 16nm finfet. In
     International Solid-State Circuits Conference (ISSCC), 2021.
[52] Thierry Tambe, En-Yu Yang, Zishen Wan, Yuntian Deng, Vijay Janapa Reddi, Alexander Rush, David Brooks, and
     Gu-Yeon Wei. Algorithm-hardware co-design of adaptive floating-point encodings for resilient deep learning inference.
     In 2020 57th ACM/IEEE Design Automation Conference (DAC), pages 1–6, 2020.
[53] Tachio Terauchi and Alex Aiken. Secure information flow as a safety problem. In Chris Hankin and Igor Siveroni,
     editors, Static Analysis, pages 352–367, Berlin, Heidelberg, 2005. Springer Berlin Heidelberg.
[54] Hiroshi Unno, Tachio Terauchi, and Eric Koskinen. Constraint-based relational verification. In Alexandra Silva
     and K. Rustan M. Leino, editors, Computer Aided Verification, pages 742–766, Cham, 2021. Springer International
     Publishing.
[55] Sven Verdoolaege, Gerda Janssens, and Maurice Bruynooghe. Equivalence checking of static affine programs using
     widening to handle recurrences. ACM Transactions on Programming Languages and Systems (TOPLAS), 34(3):1–35,
     2012.
[56] Sander Vocke, Henk Corporaal, Roel Jordans, Rosilde Corvino, and Rick Nas. Extending halide to improve software
     development for imaging dsps. ACM Trans. Archit. Code Optim., 14(3), aug 2017.
[57] Paul N. Whatmough, Sae Kyu Lee, Marco Donato, Hsea-Ching Hsueh, Sam Likun Xi, Udit Gupta, Lillian Pentecost,
     Glenn G. Ko, David M. Brooks, and Gu-Yeon Wei. A 16nm 25mm2 SoC with a 54.5x flexibility-efficiency range from
     dual-core Arm Cortex-A53 to eFPGA and cache-coherent accelerators. In Proceedings of the 2019 Symposium on VLSI
     Circuits, page 34, New York, NY, USA, 2019. IEEE.
[58] Max Willsey, Chandrakana Nandi, Yisu Remy Wang, Oliver Flatt, Zachary Tatlock, and Pavel Panchekha. egg: Fast
     and extensible equality saturation. Proc. ACM Program. Lang., 5(POPL), jan 2021.
[59] Anna Zaks and Amir Pnueli. CoVaC: Compiler validation by program analysis of the cross-product. In International
     Symposium on Formal Methods (FM 2008), Turku, Finland, May 2008.
[60] Hongce Zhang, Caroline Trippel, Yatin A Manerkar, Aarti Gupta, Margaret Martonosi, and Sharad Malik. Ila-
     mcm: integrating memory consistency models with instruction-level abstractions for heterogeneous system-on-chip
     verification. In 2018 Formal Methods in Computer Aided Design (FMCAD), pages 1–10. IEEE, 2018.
