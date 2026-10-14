                                        Practical Formal Verification for MLIR Programs
                                        EMILY TUCKER, Georgia Institute of Technology, USA
                                        LOUIS-NOËL POUCHET, Colorado State University, USA
                                        ERIKA HUNHOFF, AMD, USA
                                        STEPHEN NEUENDORFFER, AMD, USA
                                        ERWEI WANG, AMD, USA
                                        Optimizing compilers have become a cornerstone for high-performance program generation in research and
arXiv:2605.01124v1 [cs.PL] 1 May 2026




                                        industry. Optimizations, including those implemented manually by a user and those target-specific and non-
                                        target-specific, are used to transform programs to achieve good performance. Although these optimizations are
                                        necessary for performance, assessing their correctness has remained a major challenge; the risk of incorrect
                                        code being deployed increases with unproven optimization flows.
                                           In this work, we target the formal verification of correctness of a transformed program by computing
                                        whether a pair of programs are semantically equivalent, one being a transformed version of the other. We
                                        restrict the class of programs supported to enable a hybrid concrete-symbolic interpretation approach to
                                        equivalence, which in turn is mostly agnostic to how the programs are implemented (syntax, schedule, storage,
                                        etc.). This approach can show equivalence in linear time with respect to the operations executed by the
                                        programs. We develop a verifier for a meaningful subset of MLIR, and report on the verification of the AMD
                                        MLIR-AIR and MLIR-AIE toolchains, as well as the standard mlir-opt on hundreds of benchmarks variants.
                                        Additional Key Words and Phrases: Verification, Program equivalence, MLIR, Parallel programming

                                        1   Introduction
                                        It has long been a requirement to optimize a program for performance by modifying its implemen-
                                        tation: altering the order of operations (e.g., loop tiling), parallelizing operations and implementing
                                        their synchronizations, and exposing instruction-level parallelism (e.g., via unrolling) are typical
                                        mandatory optimizations for performance of numerical applications. However, the issue of deter-
                                        mining whether the transformed program maintains the semantics of the original program remains
                                        a fundamental challenge. No global system can systematically prove the correctness of arbitrary
                                        transformations applied to arbitrary programs.
                                           To mitigate the risks of incorrect transformations being deployed, numerous approaches have
                                        been developed, typically targeting a specific framework or program class. The techniques range
                                        from simple testing to more complex fuzzing [15, 37], where the outputs produced by both pro-
                                        grams are compared, facilitating the detection of bugs. Compiler optimizations can be validated
                                        using translation validation techniques, such as Alive2 [36] for LLVM IR. A pair of programs
                                        can be checked for symbolic equivalence using symbolic execution and employing SMT queries
                                        to reason on program properties, as with e.g., UC-KLEE [3, 45] or CIVL [51]. Techniques that
                                        prove equivalence between a pair of affine programs, such as ISA for a class of affine program
                                        transformations [58], have been proposed but are typically very limited in scope. These techniques
                                        all present different trade-offs in terms of coverage (e.g., types of input programs, types of transfor-
                                        mations performed), speed, and accuracy. In this work, we target the verification of correctness
                                        of transformations in a manner mostly agnostic to how they were produced: taking as input a
                                        pair of programs, one being a transformed version of the other, we aim to prove their semantic
                                        equivalence for a practical class of programs that includes highly optimized implementations of
                                        key AI workloads.

                                        Authors’ Contact Information: Emily Tucker, Georgia Institute of Technology, USA, emily.tucker@gatech.edu; Louis-Noël
                                        Pouchet, Colorado State University, USA, pouchet@colostate.edu; Erika Hunhoff, AMD, USA, erika.hunhoff@amd.com;
                                        Stephen Neuendorffer, AMD, USA, stephen.neuendorffer@amd.com; Erwei Wang, AMD, USA, erwei.wang@amd.com.
2                        Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


   PEQC [43] is a hybrid concrete-symbolic interpreter which concretely evaluates (and simplifies)
the input program and builds a symbolic representation of all other operations that contribute to the
production of the final outputs [43]. These representations are then checked for equivalence, either
proving correctness or exposing mismatches. However, PEQC trades generality in the program
structure for restrictions of the class of programs handled: it typically requires fixed problem sizes
(e.g., in a matrix-multiply program, the sizes of matrices are fixed and known at compile-time, and
correctness guarantees apply to any input matrices using this specific size).
   In this work, we leverage the approach developed in PEQC to develop a novel framework
for verification via hybrid concrete-symbolic interpretation. We significantly revisit and extend
PEQC in PEQC-MLIR, the system presented in this paper. PEQC-MLIR supports verification of:
(1) general, hierarchical parallel tasks, (2) arbitrary synchronization with binary (wait/set) and
counting (acquire/release) semaphores, and (3) a class of symbolic conditional control-flow,
significantly broadening the scope of applicability of this approach. Furthermore, we develop a
complete formalization of a proxy parallel language representing PEQC-MLIR’s input, detailing
the process of ensuring correctness of parallel programs and computing their equivalence, and
proving correctness of our approach.
   To enable wide applicability of this approach, we develop a verifier for a set of MLIR [32]
programs, including concurrent programs using the async dialect [40], and the ability to verify
their equivalence to a sequential version. We use this verifier to expose several important bugs in
tools such as mlir-opt. We also contribute support for the MLIR-AIR [5, 59] and MLIR-AIE [4]
systems to map computations to AMD AI Engines [46], enabling the verification of correctness for
practical workloads deployed on the AI Engines. We make the following contributions:
• We present an end-to-end, fully automated approach to verify the equivalence between a pair of
   (concurrent) programs, under practical restrictions.
• We formalize our hybrid concrete-symbolic approach and prove that it correctly detects and
   handles deterministic parallel programs and their equivalence in Sec. 3.
• We introduce our approach to the correctness verification of a rich class of MLIR programs and
   their transformations, by successive lowering and conversion of user-defined dialects to standard
   dialects, and eventually using Parallel Intermediate Representation (PIR) of PEQC-MLIR in Sec. 5.
• We present extensive evaluation of PEQC-MLIR in Sec. 6, over hundreds of MLIR program
   variants generated using mlir-opt and Polygeist, uncovering a variety of bugs and lack of
   analysis to adequately apply transformations. We present our verification for the AMD MLIR-
   AIR and MLIR-AIE toolchains for mapping AI workloads to the AI Engine, exposing subtle
   concurrency bugs that were then fixed in these toolchains.

2   Motivation and Overview
This section presents the target problem, associated challenges, and outlines our proposed solution.
Our objective is to prove the correctness of programs by enabling the seamless integration of
correctness verification within a progressive optimization flow. Starting from a high-level algorith-
mic description, high-performance programs are typically progressively optimized and refined by
automatic or manual modifications to the program.
  The Multi-Level IR (MLIR) ecosystem exemplifies this flow. MLIR [32] is a compiler infrastructure
designed to represent programs using multiple intermediate representations at different levels of
abstraction within a single framework. Rather than relying on a monolithic IR, MLIR organizes
program representations into dialects, each tailored to express specific program semantics, such
as tensor algebra, loop nests, or structured control flow [1, 40]. A central concept in MLIR is
progressive lowering, where programs are gradually transformed from high-level, semantic-rich
representations into lower-level forms that make execution details explicit. Fig. 1 provides an
Practical Formal Verification for MLIR Programs                                                                                                                                    3


illustration of this. MLIR allows analyses and transformations to be applied at the abstraction
level where they are most effective, while preserving program structure as long as possible during
compilation.


  @linalg_structured_op
  d e f matmul_mono (
        A= T e n s o r D e f ( T , S . M, S . K ) ,
        B= T e n s o r D e f ( T , S . K , S . N ) ,
        C= T e n s o r D e f ( T , S . M, S . N , o u t p u t = True ) ,                         module {
  ):                                                                                               f u n c . f u n c @forward (% a r g 0 : memref <16 x 1 6 x i 3 2 > ,
        domain ( D . m, D . n , D . k )                                                            % a r g 1 : memref <16 x 1 6 x i 3 2 > ) −> memref <16 x 1 6 x i 3 2 > {
        C[D . m, D . n ] += A[D . m, D . k ] ∗ B [D . k , D . n ]                                      %c0_i32 = a r i t h . constant 0 : i32
                                                                                                       % a l l o c = memref . a l l o c ( ) : memref <16 x 1 6 x i 3 2 >
  @module_builder                                                                                      %c 0 = a r i t h . c o n s t a n t 0 : i n d e x
  d e f m a t m u l _ o n _ t e n s o r s (m, n , k ) :                                                %c 1 6 = a r i t h . c o n s t a n t 16 : i n d e x
        dtype = I nt ege rT yp e . g e t _ s i g n l e s s ( width =32)                                %c 1 = a r i t h . c o n s t a n t 1 : i n d e x
                                                                                                       s c f . f o r % a r g 2 = %c 0 t o %c 1 6 s t e p %c 1 {
        @func . FuncOp . f r o m _ p y _ f u n c (                                                         %c 0 _ 3 = a r i t h . c o n s t a n t 0 : i n d e x
            MemRefType . g e t ( ( m, k ) , d t y p e ) ,                                                  %c 1 6 _ 4 = a r i t h . c o n s t a n t 16 : i n d e x
            MemRefType . g e t ( ( k , n ) , d t y p e )                                                   %c 1 _ 5 = a r i t h . c o n s t a n t 1 : i n d e x
        )                                                                                                  s c f . f o r % a r g 3 = %c 0 _ 3 t o %c 1 6 _ 4 s t e p %c 1 _ 5 {
        def forward ( lhs , rhs ) :                                                                            memref . s t o r e % c 0 _ i 3 2 , % a l l o c [% a r g 2 , % a r g 3 ] :
            o u t = memref . A l l o c O p ( MemRefType . g e t ( ( m, n ) ,                                   memref <16 x 1 6 x i 3 2 >
            dtype ) , [ ] , [ ] )                                                                          }
            z e r o = a r i t h . ConstantOp ( dtype , 0 )                                             }
            z e r o _ f i l l = l i n a l g . f i l l ( z e r o , o u t s =[ o u t ] )                 %c 0 _ 0 = a r i t h . c o n s t a n t 0 : i n d e x
            matmul_mono ( l h s , rhs , o u t s =[ o u t ] )                                           %c 1 6 _ 1 = a r i t h . c o n s t a n t 16 : i n d e x
            return o u t                                                                               %c 1 _ 2 = a r i t h . c o n s t a n t 1 : i n d e x
                                                                                                       s c f . f o r % a r g 2 = %c 0 _ 0 t o %c 1 6 _ 1 s t e p %c 1 _ 2 {
                                                                                                           %c 0 _ 3 = a r i t h . c o n s t a n t 0 : i n d e x
  #map = a f f i n e _ m a p < ( d0 , d1 , d2 ) −> ( d0 , d2 ) >                                           %c 1 6 _ 4 = a r i t h . c o n s t a n t 16 : i n d e x
  #map1 = a f f i n e _ m a p < ( d0 , d1 , d2 ) −> ( d2 , d1 ) >                                          %c 1 _ 5 = a r i t h . c o n s t a n t 1 : i n d e x
  #map2 = a f f i n e _ m a p < ( d0 , d1 , d2 ) −> ( d0 , d1 ) >                                          s c f . f o r % a r g 3 = %c 0 _ 3 t o %c 1 6 _ 4 s t e p %c 1 _ 5 {
  module {                                                                                                     %c 0 _ 6 = a r i t h . c o n s t a n t 0 : i n d e x
    f u n c . f u n c @forward (% a r g 0 : memref <16 x 1 6 x i 3 2 > ,                                       %c 1 6 _ 7 = a r i t h . c o n s t a n t 16 : i n d e x
    % a r g 1 : memref <16 x 1 6 x i 3 2 > ) −> memref <16 x 1 6 x i 3 2 > {                                   %c 1 _ 8 = a r i t h . c o n s t a n t 1 : i n d e x
        % a l l o c = memref . a l l o c ( ) : memref <16 x 1 6 x i 3 2 >                                       s c f . f o r % a r g 4 = %c 0 _ 6 t o %c 1 6 _ 7 s t e p %c 1 _ 8 {
        %c0_i32 = a r i t h . constant 0 : i32                                                                     %0 = memref . l o a d % a r g 0 [% a r g 2 , % a r g 4 ] :
        l i n a l g . f i l l i n s (% c 0 _ i 3 2 : i 3 2 ) o u t s (% a l l o c :                                 memref <16 x 1 6 x i 3 2 >
        memref <16 x 1 6 x i 3 2 > )                                                                               %1 = memref . l o a d % a r g 1 [% a r g 4 , % a r g 3 ] :
        l i n a l g . g e n e r i c { i n d e x i n g _ m a p s = [ # map , #map1 , # map2 ] ,                      memref <16 x 1 6 x i 3 2 >
        iterator_types = [ " parallel " , " parallel " ,                                                           %2 = memref . l o a d % a l l o c [% a r g 2 , % a r g 3 ] :
        " r e d u c t i o n " ] } i n s (% a r g 0 , % a r g 1 : memref <16 x 1 6 x i 3 2 > ,                       memref <16 x 1 6 x i 3 2 >
        memref <16 x 1 6 x i 3 2 > ) o u t s (% a l l o c : memref <16 x 1 6 x i 3 2 > )                           %3 = a r i t h . m u l i %0 , %1 : i 3 2
        {                                                                                                          %4 = a r i t h . a d d i %2 , %3 : i 3 2
        ^ bb0 (% i n : i 3 2 , % i n _ 0 : i 3 2 , %o u t : i 3 2 ) :                                               memref . s t o r e %4 , % a l l o c [% a r g 2 , % a r g 3 ] :
            %0 = a r i t h . m u l i %in , % i n _ 0 : i 3 2                                                        memref <16 x 1 6 x i 3 2 >
            %1 = a r i t h . a d d i %out , %0 : i 3 2                                                          }
             l i n a l g . y i e l d %1 : i 3 2                                                            }
        }                                                                                              }
        return % a l l o c : memref <16 x 1 6 x i 3 2 >                                                return % a l l o c : memref <16 x 1 6 x i 3 2 >
    }                                                                                              }
  }                                                                                              }



Fig. 1. MLIR example. Top left: the Python program to describe matrix-multiplication, which is then expressed
as a MLIR Linalg program. Bottom left: the resulting Linalg program, for a problem size of 16x16. Right: the scf
program obtained by lowering Linalg to affine with –linalg-to-affine-loops and then to scf with –lower-affine.
PEQC-MLIR targets the verification of correctness for MLIR programs by exploiting such lowerings, as
described in Sec. 5.

   AMD has developed the MLIR-AIR [6, 59] and MLIR-AIE [4, 26] compilation flows, for produc-
tion use to map AI workloads to the AMD AI Engine [59] which is integrated in AMD Ryzen
AI processors. Starting from a high-level description of the computation, for example matmul
4                          Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


in the MLIR linalg dialect or its equivalent Python description, the program is successively
lowered, transformed, and optimized into an AIE program which maps computation and data move-
ment to concurrent hardware units, synchronizing them using FIFOs and counting semaphores
(acquire/release). A 2-line sequential matmul program operating on tensors turns into a multi-
buffered, highly concurrent program of nearly 1k lines. These transformations take place at the
MLIR level and may be either fully automated by a compiler, implemented by AI agents, or im-
plemented manually by human engineers. At every transformation stage, we aim to provide a
system that assesses the correctness of a transformation, be it manual, automated or produced
by an open-source or black-box tool. We validate correctness by computing whether the original
and transformed programs are semantically equivalent: they must produce the same results for all
output variables.
   Challenges Numerous challenges must be addressed to achieve these objectives. First, our system
should be robust to any means used to transform a program, to reflect typical design flows. This
includes programs produced by generative AI. We specifically do not rely on the user to define high-
level semantic properties that an implementation should match or how a transformation should
modify the program. Instead, we directly prove equivalence for a class of programs without user
input. Second, our system should be robust to a wide class of optimizations, which includes arbitrary
data layout changes, bufferization schemes, data reuse implementation, etc.. These transformations
are critical for high-performance execution of AI workloads on accelerators, such as the AI Engine,
where the orchestration of data movement requires careful fine-tuning. Such a system should be
future-proof to new variations of these optimizations, and should avoid the need to specify the
transformation effects to enable verification (e.g., [12, 66]). Third, our system should be fully capable
of reasoning about the correctness of concurrency, parallelization, and arbitrary synchronization
approaches, including assessing the correctness of parallelizing a sequential program. This support
is fundamental because most practical hardware is concurrent, and often has numerous hardware
replications of computation/communication units that must be exploited for high performance.
Fourth, our system should provide stronger guarantees than testing alone. Although testing programs
on pre-defined inputs/outputs can expose bugs (e.g., concurrency bugs with dynamic race detectors
[24]), this is not a guarantee of correctness. The ability to reason symbolically on possible inputs
enables providing correctness guarantees for sets of possible concrete values these symbols may
take, and not simply exposing bugs.

                                                       Report possible
                                                       deadlock or race
                                                                                                                        PEQC

                                           Hybrid                                                                     CDAG
                         MLIR-to-C        concrete/                      Memory State:                       no   normalization
          Input MLIR
                         Translation      symbolic                  Concrete + Symbolic CDAG                       via rewrite
                                         interpreter                                                                  rules
                                                                                               Equivalence
                                                                                                 Check




                                           Hybrid
                         MLIR-to-C        concrete/                      Memory State:
          Input MLIR                                                                                                 yes/no
                         Translation      symbolic                  Concrete + Symbolic CDAG
                                         interpreter




Fig. 2. Overall flow for verification with PEQC-MLIR, and the MLIR-to-PIR translators presented in Sec. 5


  PEQC-MLIR In this paper, we present PEQC-MLIR, which provides a solution to the challenges
above by carefully restricting the class of programs supported while still enabling full support of
representative AI workloads. PEQC-MLIR is based on prior work by Pouchet, Tucker et al. [43, 56],
which we significantly extend to support a much wider class of (concurrent) programs. Their
Practical Formal Verification for MLIR Programs                                                       5


system implements a hybrid concrete-symbolic interpretation of the program, simplifying out any
expressions or control-flow that can be computed at compile time for the program (via partial
concrete interpretation), and computing symbolic values/expressions for everything else. Through
this hybrid interpretation stage, a symbolic representation of the program is built. Equivalence
can then be shown by proving these representations are semantically equivalent (which is trivial
if these normalized representations are identical [43]). This symbolic representation is based on
Computational Directed Acyclic Graphs (CDAGs [19]), which have a space complexity linear in the
number of operations executed in the program. Illustrative examples and intuitions of this approach
are detailed in [43]. For example, in the context of High-Level Synthesis (HLS), we demonstrated that
this approach can verify a highly optimized systolic array. We targeted an implementation produced
by the AutoSA [60] compiler consisting of 8k processing elements and 16k FIFOs. By successfully
verifying this against a 5-line dense matrix-multiply loop, we demonstrated both scalability and
coverage of key concurrency constructs. Indeed, the correctness is proved by treating all elements
of the input matrices 𝐴, 𝐵 as symbols. For every element of the output 𝐶, we compute a symbolic
expression corresponding to the computation performed (itself only a function of elements of 𝐴, 𝐵
[43]). This symbolic analysis ensures equivalence will be satisfied whichever the actual concrete
values these matrices may be at runtime.
   In this work, we entirely revisit the approach to concurrency support and parallelization correct-
ness checking in PEQC, while significantly broadening the class of programs supported, including
some input-dependent symbolic conditional control flow which is modeled as conditional CDAGs.
Fig. 2 outlines our system. The PEQC-MLIR components are presented in Sec. 3, where we develop
small-step operational semantics for a (simplified) parallel language supporting synchronizations
using binary (set/wait) and counting (acquire/release) semaphores. We prove that our system
only accepts deterministic parallel programs (reporting race/deadlock otherwise). We prove it
computes a correct, equivalent symbolic representation of the programs for subsequent equiva-
lence checking. This language is rich enough to accurately capture the semantics of a wide set of
MLIR programs, after conversion and possible lowering, enabling the verification of pairs of MLIR
programs including in the AIR and AIE dialects as well as standard dialects such as async, scf, and
affine. This conversion is presented in Sec. 5 and is fundamental to deploy our staged approach to
correctness verification. Experimental results on a variety of AIR and AIE designs for the AI Engine
are presented in Sec. 6, including subtle concurrency bugs we have exposed for the first time, along
with an extensive evaluation of mlir-opt optimizations over hundreds of benchmarks.

3   Formalization of Program Correctness Verification
We now formalize our approach to computing equivalence between programs, using a hybrid
concrete-symbolic interpretation to compute a normalized symbolic representation of the final
memory state when the program terminates without error.
   We first present a simplified proxy for the parallel language we support in PEQC-MLIR in Sec. 3.1,
and how to evaluate and represent symbolic expressions in our model in Sec. 3.2. We then present
in Sec. 3.3 a small-step operational semantics for this parallel language which is used to build a
state-based representation of the program (𝐺, 𝑀), where 𝐺 is a graph with nodes representing
each execution of every statement, and 𝑀 is the representation of the memory state. We prove our
system can only reach a final state (i.e., the program terminates without error) for deterministic
parallel programs, which implies the absence of race and deadlocks (and conversely, that our system
errors in the presence of deadlocks and races), in Sec. 3.4. In Sec. 3.5, we discuss proving equivalence
between the representations obtained for two programs: (𝐺, 𝑀) ≡ (𝐺 ′, 𝑀 ′ ), and present details of
our full implementation in Sec. 4.
6                         Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


3.1   A Simple Featherweight Language
The grammar in Fig. 3 captures programs in our featherweight language. It is a simplified ver-
sion of our intermediate representation implementation outlined in Sec. 4.1, but it captures all
critical constructs required to build a symbolic representation of the program while reasoning on
synchronizations with semaphores. The semantics of each construct is presented in Sec. 3.3.


                                Program        𝑃    → 𝑠; 𝑃 | 𝜖
                                Statement       𝑠   →     int 𝑣 []
                                                    |     𝑣 [𝑒𝑖 ] = 𝑒
                                                    |     async{𝑃 }
                                                    |     set(𝑒 1, 𝑒 2 )
                                                    |     wait(𝑒 1, 𝑒 2 )
                                                    |     acquire(𝑒 1, 𝑒 2 )
                                                    |     release(𝑒 1, 𝑒 2 )
                                                    |     while(𝑒){𝑃 }
                                Expression      𝑒   →     𝑐
                                                    |     𝑣 [𝑒𝑖 ]
                                                    |     𝑒1 + 𝑒2
                                                    |     𝑒1 < 𝑒2
                                                    |     (𝑒𝑐𝑜𝑛𝑑 ?𝑒 1 : 𝑒 2 )

                              Fig. 3. Grammar for the simplified language.




3.2   Expression Evaluation
Before describing the semantics of our featherweight but complete language, we first present the
evaluation of expressions. This is key for our system: we mix concrete evaluation and symbolic
representation for expressions, and rely on correctly implementing the concrete semantics of
arithmetic expressions in the interpreter. For example, we implement the int 32-bit data type, with
C semantics, to evaluate expressions composed of only concrete values. That is, we replace 1 + 1 in
the program with 2 via concrete evaluation. But if values of some operands in the expression are not
known, for example 𝑖𝑛1 + 1 where the input value 𝑖𝑛1 is read before being written in the program
(live-in), we instead promote this expression to a symbolic representation using an AST-style tree
representation: +(𝑖𝑛1, 1). This symbolic expression is then used to update other expressions. For
example, after interpreting 𝑖𝑛1 = 𝑖𝑛1 + 1; 𝑖𝑛1 = 𝑖𝑛1 ∗ 2, 𝑖𝑛1 is represented as 𝑠𝑦𝑚(∗(+(𝑖𝑛1, 1), 2)),
where 𝑠𝑦𝑚(𝑒) denotes an expression 𝑒 represented symbolically. As shown in Sec. 3.3, we restrict
where symbolic expressions may occur during interpretation to ensure we deterministically obtain
the final memory representation at the end of the program, for example preventing them in array
subscripts (we must always be able to associate a unique name to a memory location) or in values
set for semaphores.
   Expression evaluation is defined in Fig. 4. 𝑒 ⇓𝑀,𝑠 𝑐 represents the evaluation of 𝑒 to 𝑐 (a concrete
value) with respect to statement 𝑠. 𝑒𝑟𝑟 triggers an error state. Helper functions are defined in Sec. 3.3:
𝑣𝑎𝑟 _𝑒𝑣𝑎𝑙 (𝑀, 𝑠, 𝑛, 𝑖) extracts the current representation in memory 𝑀 of the array cell named n[i].
Here we only illustrate key evaluation constructs; our full implementation develops this approach
for additional unary and binary arithmetic operators.
Practical Formal Verification for MLIR Programs                                                                                7


                                                  𝑒𝑖 ⇓𝑀,𝑠 sym(𝑠)                                  𝑒𝑖 ⇓𝑀,𝑠 err
               c ⇓𝑀,𝑠 𝑐                           𝑛[𝑒𝑖 ] ⇓𝑀,𝑠 err                               𝑛[𝑒𝑖 ] ⇓𝑀,𝑠 err

         𝑒𝑖 ⇓𝑀,𝑠 𝑖     𝑣𝑎𝑟 _𝑒𝑣𝑎𝑙 (𝑀, 𝑠, 𝑛, 𝑖) = 𝑣                   𝑒𝑖 ⇓𝑀,𝑠 𝑖         𝑣𝑎𝑟 _𝑒𝑣𝑎𝑙 (𝑀, 𝑠, 𝑛, 𝑖) = ⊥
                      𝑛[𝑒𝑖 ] ⇓𝑀,𝑠 𝑣                                            𝑛[𝑒𝑖 ] ⇓𝑀,𝑠 sym(𝑛[𝑖])

                𝑒 1 ⇓𝑀,𝑠 𝑣 1    𝑒 2 ⇓𝑀,𝑠 𝑣 2                       𝑒𝑐 ⇓𝑀,𝑠 𝑣𝑐          𝑒 1 ⇓𝑀,𝑠 𝑣 1      𝑒 2 ⇓𝑀,𝑠 𝑣 2
             𝑒 1 + 𝑒 2 ⇓𝑀,𝑠 val_add(𝑣 1, 𝑣 2 )                        𝑒𝑐 ?𝑒 1 : 𝑒 2 ⇓𝑀,𝑠 val_tern(𝑣𝑐 , 𝑣 1, 𝑣 2 )
                                                          val_tern(𝑣𝑐 , 𝑣1 , 𝑣2 ) =
 val_add(𝑣 1, 𝑣 2 ) =
                                                          
                                                           𝑣2                     if 𝑣𝑐 = 𝑐 ∧ 𝑐 = 0
   𝑐1 + 𝑐2            if 𝑣 1 = 𝑐 1, 𝑣 2 = 𝑐 2
                                                         
                                                          
                                                                                   if 𝑣𝑐 = 𝑐 ∧ 𝑐 ≠ 0
                                                         
  
                                                         
                                                          
                                                           𝑣 1
  
    sym(𝑠 + 𝑐)        if 𝑣 1 = sym(𝑠), 𝑣 2 = 𝑐
                                                          
                                                            sym(𝑠 𝑐 ?𝑐 1 : 𝑐 2 )   if 𝑣𝑐 = sym(𝑠𝑐 ), 𝑣1 = 𝑐 1 , 𝑣2 = 𝑐 2
  
                                                         
                                                          
                                                         
                                                          
  
                                                         
                                                          
    sym(𝑐 + 𝑠)        if 𝑣 1 = 𝑐, 𝑣 2 = sym(𝑠)            
                                                            sym(𝑠𝑐 ?𝑠 1 : 𝑐 )      if 𝑣𝑐 = sym(𝑠𝑐 ), 𝑣1 = sym(𝑠 1 ), 𝑣2 = 𝑐
                                                            sym(𝑠𝑐 ?𝑐 : 𝑠 1 )      if 𝑣𝑐 = sym(𝑠𝑐 ), 𝑣1 = 𝑐, 𝑣2 = sym(𝑠 1 )
                                                         
   sym(𝑠 1 + 𝑠 2 ) if 𝑣 1 = sym(𝑠 1 ), 𝑣 2 = sym(𝑠 2 )
  
                                                         
                                                          
                                                         
                                                          
                                                            sym(𝑠𝑐 ?𝑠 1 : 𝑠 2 )    if 𝑣𝑐 = sym(𝑠𝑐 ), 𝑣1 = sym(𝑠 1 ), 𝑣2 = sym(𝑠 2 )
                                                         
                                                          
   err               if 𝑣 1 = err ∨ 𝑣 2 = err
                                                         
                                                          
                                                          
                                                           err                    if 𝑣𝑐 = err ∨ 𝑣1 = err ∨ 𝑣2 = err
                                                         
                                                          
                                    Fig. 4. Expression evaluation semantics.

3.3   Small-step Operational Semantics
Our objective is to reason on parallel programs with possibly hierarchical tasks spawned with async
and synchronized with semaphores, proving the absence of data races and deadlock in a program
or producing an error otherwise. While Jin et al. proved a race-free program is deterministic under
synchronization with promises [28], here we prove that any program is deterministically handled
by our system, including when using counting semaphores. A correct parallel program must ensure
that every operation that may execute in parallel cannot read/write the same memory location at
the same time, and that it produces the same symbolic computation result as the reference program.
Here we assume that only explicit synchronizations in the program (i.e., semaphore operations)
can force an ordering between sets of statements in the program; we never rely on latency and
timing of operations to determine their execution order.
   Notation In our semantics, all variables are arrays of either symbolic or concrete values. The
memory of the program is represented by a function 𝑀 : (𝑖𝑑, 𝑛𝑎𝑚𝑒) ⇀ (N ⇀ 𝑣𝑎𝑙𝑢𝑒) that maps a
tuple of task ID and variable name to an array of values. 𝑀 need not be defined on a given task ID
and variable name; similarly, a variable’s value at any index need not be initialized.
   We define several helper functions for accessing and modifying the memory representation.
The function 𝑔𝑒𝑡_𝑣𝑎𝑟 (𝑀, 𝑖𝑑, 𝑣) returns the task ID where the variable name was declared: child
threads can access their parents’ variables. The function 𝑣𝑎𝑟 _𝑒𝑣𝑎𝑙 (𝑀, 𝑖𝑑, 𝑣, 𝑖) returns the value
of a variable at index 𝑖. If 𝑔𝑒𝑡_𝑣𝑎𝑟 (𝑀, 𝑖𝑑, 𝑣) ∈ dom(𝑀) and 𝑖 ∈ dom(𝑀 (𝑔𝑒𝑡_𝑣𝑎𝑟 (𝑀, 𝑖𝑑, 𝑣))), then
𝑣𝑎𝑟 _𝑒𝑣𝑎𝑙 (𝑀, 𝑖𝑑, 𝑣, 𝑖) = 𝑀 (𝑔𝑒𝑡_𝑣𝑎𝑟 (𝑀, 𝑖𝑑, 𝑣)) (𝑖). Otherwise, 𝑣𝑎𝑟 _𝑒𝑣𝑎𝑙 (𝑀, 𝑖𝑑, 𝑣, 𝑖) = ⊥.
   To modify 𝑀, we use the shorthand 𝑀 [(𝑖𝑑, 𝑣) ↦→ (𝑖 ↦→ 𝑒)] to represent a function that is identical
to 𝑀 except with the modification that 𝑀 (𝑖𝑑, 𝑣) (𝑖) = 𝑒. The function 𝑚𝑒𝑚_𝑑𝑒𝑐𝑙 (𝑀, 𝑖𝑑, 𝑣) declares a
variable with a given task ID and name. If (𝑖𝑑, 𝑣) is already in dom(𝑀), 𝑚𝑒𝑚_𝑑𝑒𝑐𝑙 (𝑀, 𝑖𝑑, 𝑣) = 𝑀.
Otherwise, 𝑚𝑒𝑚_𝑑𝑒𝑐𝑙 (𝑀, 𝑖𝑑, 𝑣) = 𝑀 [(𝑖𝑑, 𝑣) ↦→ ∅]: initially, the variable is undefined at all indices.
The function 𝑚𝑒𝑚_𝑢𝑝𝑑𝑎𝑡𝑒 (𝑀, 𝑖𝑑, 𝑣, 𝑖, 𝑒) assigns the value of a variable at index 𝑖 to be a concrete or
symbolic value, 𝑒: 𝑚𝑒𝑚_𝑢𝑝𝑑𝑎𝑡𝑒 (𝑀, 𝑖𝑑, 𝑣, 𝑖, 𝑒) = 𝑀 [𝑔𝑒𝑡_𝑣𝑎𝑟 (𝑀, 𝑖𝑑, 𝑣) ↦→ (𝑖 ↦→ 𝑒)].
   Intuitively, we present a system represented by a graph 𝐺 where every node is one instance of
a statement, and where an edge between two nodes 𝑠 and 𝑠 ′ represent the requirement for 𝑠 to
8                         Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


execute before 𝑠 ′ , as per the program synchronizations. Nodes in the graph are of the form (𝑖𝑑, 𝑃),
where 𝑖𝑑 is the ID of the task executing the statement, and 𝑃 is the rest of the program the task will
execute, starting with the statement the node represents. We use 𝑛 ⇝ 𝑚 to denote that an edge
exists from 𝑛 and 𝑚 in 𝐺, and 𝑛 ⇝∗ 𝑚 to denote that a path exists from 𝑛 to 𝑚 in 𝐺. A new node in
𝐺 is created for each statement instance. For example, in Figure 5, nodes for statements in the loop
body appear 𝑁 times in the graph.
  Definition 3.1 (Happens Before). For graph 𝐺 and two nodes 𝑛, 𝑚 ∈ 𝐺, 𝑛 happens before 𝑚,
denoted 𝑛 ⇝∗ 𝑚, if and only if there exists a path from 𝑛 to 𝑚 in 𝐺.
   Definition 3.2 (May Happen in Parallel). For graph 𝐺 and two nodes 𝑛, 𝑚 ∈ 𝐺, 𝑛 may happen
in parallel with 𝑚, denoted 𝑛 ∥ 𝑚, if and only if 𝑛 ̸⇝∗ 𝑚 and 𝑚 ̸⇝∗ 𝑛.
   We define the semantics of programs as a relation over program states, where a state is either a
tuple (𝑀, 𝐺) of program memory and graph, or an error state 𝑒𝑟𝑟𝑜𝑟 (𝐺) that represents an invalid
state. Error states are identical: for all 𝐺, 𝐺 ′ , we consider 𝑒𝑟𝑟𝑜𝑟 (𝐺) and 𝑒𝑟𝑟𝑜𝑟 (𝐺 ′ ) to be equivalent.
   We present a very simple example of a program and its graph 𝐺 in Fig. 5. Our small-step semantics
operates on the source code on the left to produce and manipulate the graph 𝐺 on the right. Note
that we limit use to the featherweight language constructs, but the featherweight language concepts
are capable of capturing core computations and their synchronizations. We briefly discuss in Sec. 4.1
the full set of additional operations and constructs we handle, and how to convert them to the
featherweight language.

                                                              t0
                                                         1
                                                              i[0] = 0;

                                                              t0
                                                         2
                                                              e[0] = i[0] < 2; ...        t1.t0
     1 // all semaphores initialized to 0                                            11
                                                                                          A[i[0]]=A[i[0]]+1; ...
     2 i [0] = 0;                                             t0
                                                         3    while (e[0]) {...}          t1.t0
     3 e [0] = i [0] < 2;                                                            12
                                                                                          set(sems[i[0]],1);
     4 // for ( i = 0; i < 2; i ++)                           t0
                                                          4
     5 while ( e [0]) {                                       async {...} ...             t2.t0
                                                                                     13
                                                                                          wait(sems[i[0]],1); ...
     6    async {                                             t0
                                                          5   async {...} ...
     7       A [ i [0]] = A [ i [0]] + 1;                                                 t2.t0
                                                                                     14
                                                                                          A[i[0]]=A[i[0]]*2;
     8       set ( sems [ i [0]] , 1);                        t0
                                                          6
     9    }                                                   i[0] = i[0] + 1; ...

    10    async {
                                                              t0
    11       wait ( sems [ i [0]] , 1);                   7   e[0] = i[0] < 2; ...        t3.t0
                                                                                     15
                                                                                          A[i[0]]=A[i[0]]+1; ...
    12       A [ i [0]] = A [ i [0]] * 2;
                                                              t0
    13    }                                               8                               t3.t0
                                                              while (e[0]) {...}     16
                                                                                          set(sems[i[0]],1);
    14    i [0] = i [0] + 1;
                                                              t0
    15    e [0] = i [0] < 2;                             9                                t4.t0
                                                              async {...} ...        17
    16 }                                                                                  wait(sems[i[0]],1); ...

                                                              t0
                                                         10                               t4.t0
                                                              async {...} ...        18
                                                                                          A[i[0]]=A[i[0]]*2;
                                                                     …

Fig. 5. An example simple concurrent program, and the graph 𝐺 representing its happens-before relation.
Nodes and edges in blue represent explicit synchronization.

  Intuitively, any pair of nodes that may execute in parallel must be checked for modifications to
conflicting memory locations. Illustrated below, we develop a small-step operational semantics to
build 𝐺 and 𝑀 for the program, and the associated checks to be performed to detect possible races.
Practical Formal Verification for MLIR Programs                                                                 9


The small-step operational semantics describes constructively the scope of parallel programs we
can interpret and reason about for equivalence, and those we report an error for.

               𝑛 = (𝑠, int 𝑣 []; 𝑃)                         𝑛 = (𝑠, 𝑣 [𝑒𝑖 ] = 𝑒; 𝑃) 𝑒𝑖 ⇓𝑀,𝑠 𝑐 𝑒 ⇓𝑀,𝑠 𝑒 ′
            𝐺 ′ = 𝐺 ∪ {𝑛 ⇝ (𝑠, 𝑃)}                                          ′
                                                                        𝐺 = 𝐺 ∪ {𝑛 ⇝ (𝑠, 𝑃)}
     (𝑀, 𝐺) →𝑛? (𝑚𝑒𝑚_𝑑𝑒𝑐𝑙 (𝑀, 𝑠, 𝑣), 𝐺 ′ )                  (𝑀, 𝐺) →𝑛? (𝑚𝑒𝑚_𝑢𝑝𝑑𝑎𝑡𝑒 (𝑀, 𝑠, 𝑣, 𝑐, 𝑒 ′ ), 𝐺 ′ )

     𝑛 = (𝑠, while(𝑒){𝑃 ′ }; 𝑃) 𝑒 ⇓𝑀,𝑠 𝑐                   𝑛 = (𝑠, while(𝑒){𝑃 ′ }; 𝑃)    𝑒 ⇓𝑀,𝑠 𝑐     𝑐≠0
      𝑐 =0       𝐺 ′ = 𝐺 ∪ {𝑛 ⇝ (𝑠, 𝑃)}                      𝐺 ′ = 𝐺 ∪ {𝑛 ⇝ (𝑠, 𝑃 ′ ; while(𝑒){𝑃 ′ }; 𝑃)}
               (𝑀, 𝐺) →𝑛? (𝑀, 𝐺 ′ )                                        (𝑀, 𝐺) →𝑛? (𝑀, 𝐺 ′ )
               𝑛 = (𝑠, while(𝑒){𝑃 ′ }; 𝑃)                                 𝑛 = (𝑠, 𝑣 [𝑒𝑖 ] = 𝑒; 𝑃)
             𝑒 ⇓𝑀,𝑠 𝑠𝑦𝑚(𝑠𝑦) ∨ 𝑒 ⇓𝑀,𝑠 𝑒𝑟𝑟                       𝑒𝑖 ⇓𝑀,𝑠 𝑠𝑦𝑚(𝑠𝑦) ∨ 𝑒𝑖 ⇓𝑀,𝑠 𝑒𝑟𝑟 ∨ 𝑒 ⇓𝑀,𝑠 𝑒𝑟𝑟
                 (𝑀, 𝐺) →𝑛? 𝑒𝑟𝑟𝑜𝑟 (𝐺)                                       (𝑀, 𝐺) →𝑛? 𝑒𝑟𝑟𝑜𝑟 (𝐺)

                                 𝑛 = (𝑠, async{𝑃 ′ }; 𝑃)  𝑖𝑑 = 𝑓 𝑟𝑒𝑠ℎ_𝑖𝑑 (𝐺)
                                   𝐺 ′ = 𝐺 ∪ {𝑛 ⇝ (𝑠, 𝑃), 𝑛 ⇝ (𝑖𝑑 · 𝑠, 𝑃 ′ )}
                                                  (𝑀, 𝐺) →𝑛? (𝑀, 𝐺 ′ )

         𝑛 = (𝑠, set(𝑠𝑒𝑚, 𝑒); 𝑃)                        𝑛 = (𝑠, wait(𝑠𝑒𝑚, 𝑒); 𝑃)  𝑐𝑜𝑟𝑟 _𝑠𝑒𝑡 (𝐺, 𝑛, 𝑛𝑠𝑒𝑡 )
         𝐺 ′ = 𝐺 ∪ {𝑛 ⇝ (𝑠, 𝑃)}                             𝐺 ′ = 𝐺 ∪ {𝑛 ⇝ (𝑠, 𝑃)} ∪ {𝑛𝑠𝑒𝑡 ⇝ 𝑛}
            (𝑀, 𝐺) →𝑛? (𝑀, 𝐺 ′ )                                         (𝑀, 𝐺) →𝑛? (𝑀, 𝐺 ′ )

                                                      𝑛 = (𝑠, acquire(𝑠𝑒𝑚,      𝑒); 𝑃)             𝑒 ⇓𝑀,𝑠 𝑐
    𝑛 = (𝑠, release(𝑠𝑒𝑚, 𝑒); 𝑃)                                Í
                                                                 {𝑟 𝑣𝑎𝑙 | 𝑐𝑜𝑟𝑟 _𝑟𝑒𝑙 (𝐺, 𝑛, 𝑟 )} = 𝑐
      𝐺 ′ = 𝐺 ∪ {𝑛 ⇝ (𝑠, 𝑃)}
                                                  𝐺 ′ = 𝐺 ∪ {𝑛 ⇝ (𝑠, 𝑃)} ∪ {𝑟 ⇝ 𝑛 | 𝑐𝑜𝑟𝑟 _𝑟𝑒𝑙 (𝐺, 𝑛, 𝑟 )}
         (𝑀, 𝐺) →𝑛? (𝑀, 𝐺 ′ )
                                                                    (𝑀, 𝐺) →𝑛? (𝑀, 𝐺 ′ )

                    𝑛 = (𝑠, op(𝑠𝑒𝑚, 𝑒); 𝑃)  op ∈ {set, wait, release, acquire}
                   (𝑠𝑒𝑚 ⇓𝑀,𝑠 sym(𝑠𝑦) ∨ 𝑠𝑒𝑚 ⇓𝑀,𝑠 err ∨ 𝑒 ⇓𝑀,𝑠 sym(𝑠𝑦) ∨ 𝑒 ⇓𝑀,𝑠 err)
                                              (𝑀, 𝐺) →𝑛? error(𝐺)

               (𝑀, 𝐺) →𝑛? (𝑀 ′, 𝐺 ′ )
                                                              (𝑀, 𝐺) →𝑛? (𝑀 ′, 𝐺 ′ )      ¬𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝐺 ′ )
       𝑡𝑎𝑠𝑘_𝑙𝑒𝑎𝑓 (𝐺, 𝑛)  𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝐺 ′ )
                                                                            (𝑀, 𝐺) → 𝑒𝑟𝑟𝑜𝑟 (𝐺 ′ )
                  (𝑀, 𝐺) → (𝑀 ′, 𝐺 ′ )

                                             (𝑀, 𝐺) →𝑛? 𝑒𝑟𝑟𝑜𝑟 (𝐺 ′ )
                                              (𝑀, 𝐺) → 𝑒𝑟𝑟𝑜𝑟 (𝐺 ′ )
                                    Fig. 6. Statement evaluation semantics.
   Program semantics are defined in terms of two separate relations, shown in Fig. 6. An intermediate
relation, →? ⊆ 𝑆𝑡𝑎𝑡𝑒 ×𝑁𝑜𝑑𝑒 ×𝑆𝑡𝑎𝑡𝑒, defines potential transitions. A state that potentially transitions
from state 𝜎 to 𝜎 ′ by executing the first statement in node 𝑛 is denoted 𝜎 →𝑛? 𝜎. The relation
→⊆ 𝑆𝑡𝑎𝑡𝑒 ×𝑆𝑡𝑎𝑡𝑒 represents the actual program semantics, a restriction of →? that only transitions
on valid nodes. We use →∗ to denote the reflexive transitive closure of →.
   For a statement to be evaluated, it must be the most recent node added with its task ID. This
property is represented by a helper function 𝑡𝑎𝑠𝑘_𝑙𝑒𝑎𝑓 : 𝑡𝑎𝑠𝑘_𝑙𝑒𝑎𝑓 (𝐺, 𝑛) is true for node 𝑛 if and
10                         Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


only if, for all other nodes 𝑚 ∈ 𝐺, 𝑛 ⇝ 𝑚 implies that 𝑛 and 𝑚 have different task IDs. If 𝑛 ∥ 𝑚,
they must have different task IDs: statements are executed sequentially inside tasks, and different
tasks always have different task IDs.
   The rules in Figure 6 build the state transition relation as follows. The variable declaration rule
declares a variable in the current task’s scope using 𝑚𝑒𝑚_𝑑𝑒𝑐𝑙. The assign rule updates 𝑀 with a
new value for the variable 𝑣 at the concrete index value 𝑐. The subsequent two rules assign the next
statements to be executed after a while statement according to the value of the condition 𝑒. The
two rules after these model errors due to symbolic values used in control flow or memory accesses.
   The rest of the →? rules handle semaphore operations. PEQC-MLIR and its semantics support
two types of semaphores: counting semaphores, which use the operations acquire and release,
and binary semaphores, which use the operations set and wait. All of these functions take two
arguments: 𝑠𝑒𝑚, the ID of the semaphore the operation is being performed on, and a concrete value
𝑣. Both semaphores are restricted in their operation to maintain determinism, and only manipulate
the happens-before graph 𝐺 rather than maintaining an internal counter.
   Counting semaphores in PEQC-MLIR mimic the semaphores typical to operating systems. The
operation release(𝑠𝑒𝑚, 𝑣) is a signal that increments the value of 𝑠𝑒𝑚 by 𝑣, and the acquire(𝑠𝑒𝑚, 𝑣)
operation blocks the execution of the task that invokes it until the value of 𝑠𝑒𝑚 ≥ 𝑣, then decrements
𝑠𝑒𝑚 by 𝑣. These operations are represented through graph operations which match release and
acquire nodes. For PEQC-MLIR to evaluate programs deterministically, we restrict releases: they
can be matched to only one acquire, which requires that they sum exactly to the acquire value 𝑣
rather than being greater than or equal to 𝑣.
   For binary semaphores in PEQC-MLIR, on a call to wait(𝑠𝑒𝑚, 𝑣), a binary semaphore 𝑠𝑒𝑚 pauses
the execution of its task until another task calls set(𝑠𝑒𝑚, 𝑣). Similarly to counting semaphores, to
ensure determinism, we restrict the use of binary semaphores such that two concurrent calls to
set which correspond to one wait are disallowed.
   Figure 5 shows an example of binary semaphores. Inside the loop body, wait operations ensure
an ordering exists between the two statements that access A[i[0]], because threads (𝑡2 · 𝑡0) and
(𝑡4 · 𝑡0) cannot proceed until after threads (𝑡1 · 𝑡0) and (𝑡3 · 𝑡0), respectively, call set.
   To maintain the correct happens-before relation over statements, we need to explicitly add syn-
chronization from semaphores to the happens-before graph. A semaphore wait must happen after
its corresponding set, and a semaphore acquire must happen after its corresponding releases. To
add these edges to 𝐺, we define helper functions that define whether a set and release correspond
to a wait and acquire, respectively.
   For a node 𝑛 where 𝑛𝑐𝑜𝑑𝑒 = op(𝑠𝑒𝑚, 𝑒) such that op ∈ {set, wait, release, acquire}, we say
that 𝑛𝑠𝑒𝑚 = 𝑣𝑠 if 𝑠𝑒𝑚 ⇓𝑀,𝑠 𝑣𝑠 and that 𝑛 𝑣𝑎𝑙 = 𝑣𝑒 if 𝑒 ⇓𝑀,𝑠 𝑣𝑒 . We define a helper function 𝑐𝑜𝑟𝑟 _𝑠𝑒𝑡 to
calculate whether a set corresponds to a wait. 𝑐𝑜𝑟𝑟 _𝑠𝑒𝑡 (𝐺, 𝑤, 𝑠) = 𝑡𝑟𝑢𝑒 if and only if 𝑤 is a wait
in 𝐺, 𝑠 is a set in 𝐺, and 𝑤𝑠𝑒𝑚 = 𝑠𝑠𝑒𝑚 and 𝑤 𝑣𝑎𝑙 = 𝑠 𝑣𝑎𝑙 , and 𝑠 happens before or in parallel with 𝑤:
(𝑤 ∥ 𝑠 ∨ 𝑠 ⇝ 𝑤). Additionally, 𝑠 must be the most recent set with respect to 𝑤: there must exist
no set 𝑠 ′ ∈ 𝐺 such that (𝑤𝑠𝑒𝑚 = 𝑠𝑠𝑒𝑚      ′     ∧ 𝑠 ⇝ 𝑠 ′ ∧ (𝑤 ∥ 𝑠 ′ ∨ 𝑠 ′ ⇝ 𝑤)). For example, in Figure 5,
𝑐𝑜𝑟𝑟 _𝑠𝑒𝑡 (𝐺, 𝑛 13, 𝑛 12 ) = 𝑐𝑜𝑟𝑟 _𝑠𝑒𝑡 (𝐺, 𝑛 17, 𝑛 16 ) = 𝑡𝑟𝑢𝑒.
   Similarly, we define a helper function 𝑐𝑜𝑟𝑟 _𝑟𝑒𝑙 for releases and acquires. 𝑐𝑜𝑟𝑟 _𝑟𝑒𝑙 (𝐺, 𝑎, 𝑟 ) =
𝑡𝑟𝑢𝑒 if and only if 𝑎 is an acquire in 𝐺, 𝑟 is a release in 𝐺, 𝑎 and 𝑟 operate on the same semaphore
(𝑎𝑠𝑒𝑚 = 𝑟𝑠𝑒𝑚 ), 𝑟 happens before or in parallel with 𝑎 (𝑎 ∥ 𝑟 ∨ 𝑟 ⇝ 𝑎), and there does not exist an
acquire 𝑎 ′ on the same semaphore such that 𝑟 ⇝ 𝑎 ′ ⇝ 𝑎. Unlike binary semaphores, counting
semaphore releases increment the semaphore rather than overwrite it, so there is no need to
restrict to the “most recent” release.
Practical Formal Verification for MLIR Programs                                                           11


    An important caveat to these semantics is that one semaphore ID can only be used as one type
of semaphore: programs must not, for example, contain set(𝑠, 𝑒) and acquire(𝑠 ′, 𝑒), where 𝑠 and
𝑠 ′ evaluate to the same value.
3.3.1 Graph Validity The relation → also requires that, for an edge (𝑀, 𝐺) → (𝑀 ′, 𝐺 ′ ) to exist, 𝐺 ′
must be valid. Graph validity is defined in the helper function 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 below.
   In state (𝑀, 𝐺), a node 𝑛 = (𝑣 [𝑒𝑖 ] = 𝑒; 𝑃) is a write to 𝑣 [𝑐] if 𝑒𝑖 ⇓𝑀,𝑠 𝑐. A node 𝑛 = (𝑣 [𝑒𝑖 ] = 𝑒; 𝑃)
is a read from 𝑣 ′ [𝑐] if there exists a subtree of the form 𝑣 ′ [𝑒𝑖′ ] such that 𝑒𝑖′ ⇓𝑀,𝑠 𝑐. A node 𝑛 is an
access to 𝑣 [𝑐] if it is either a read from or a write to 𝑣 [𝑐]. Note that nodes containing semaphore
operations can read from variables but not write to them.
   For a graph 𝐺, 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝐺) is true if and only if:
    (1) No two accesses, where one is a write, may happen in parallel: there exist no two nodes
        𝑛, 𝑚 ∈ 𝐺 such that 𝑛 ∥ 𝑚, and there exists no location 𝑣 [𝑐] where both 𝑛 and 𝑚 access 𝑣 [𝑐]
        and either 𝑛 or 𝑚 is a write to 𝑣 [𝑐].
    (2) No wait has more than one corresponding set: there exists no wait 𝑤 ∈ 𝐺 such that, for
        two sets 𝑠, 𝑠 ′ ∈ 𝐺, 𝑐𝑜𝑟𝑟 _𝑠𝑒𝑡 (𝐺, 𝑤, 𝑠) ∧ 𝑐𝑜𝑟𝑟 _𝑠𝑒𝑡 (𝐺, 𝑤, 𝑠 ′ ).
    (3) No release has more than one corresponding acquire: there exists no release 𝑟 ∈ 𝐺
        such that, for two acquires 𝑎, 𝑎 ′ ∈ 𝐺, 𝑐𝑜𝑟𝑟 _𝑟𝑒𝑙 (𝐺, 𝑎, 𝑟 ) ∧ 𝑐𝑜𝑟𝑟 _𝑟𝑒𝑙 (𝐺, 𝑎 ′, 𝑟 ).
    (4) No acquires to the same semaphore may happen in parallel: there exist no two acquires
        𝑎, 𝑎 ′ ∈ 𝐺 such that 𝑎𝑠𝑒𝑚 = 𝑎𝑠𝑒𝑚′  ∧ 𝑎 ∥ 𝑎′ .
    (5) The sum of an acquire’s corresponding release values must          Í not be greater than the value
        of the acquire: there exists no acquire 𝑎 ∈ 𝐺 such that {𝑟 𝑣𝑎𝑙 | 𝑐𝑜𝑟𝑟 _𝑟𝑒𝑙 (𝐺, 𝑎, 𝑟 )} > 𝑎 𝑣𝑎𝑙 .
   For the example graph 𝐺 in Fig. 5, 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝐺) = 𝑡𝑟𝑢𝑒, but if the semaphore synchronization
with nodes 12, 13, 16, and 17 were not present, there would be no edges between nodes 11/14 and
15/18 that access the same index of A, which would cause the graph to be invalid due to a data race.
3.3.2 Program Evaluation To evaluate a program 𝑃, we first assign it an initial state (𝑀0𝑃 , 𝐺 0𝑃 ).
The starting graph, 𝐺 0𝑃 , contains one node that assigns 𝑃 to a single initial task with ID 𝑖𝑑 0 :
𝐺 0𝑃 = {(𝑖𝑑 0, 𝑃)}. The starting memory state, 𝑀0𝑃 , has no variables defined: dom(𝑀0𝑃 ) = ∅.
    We define a program evaluation relation ⇓ such that 𝑃 ⇓ 𝜎 if and only if (𝑀0𝑃 , 𝐺 0𝑃 ) →∗ 𝜎 and
𝜎 ̸→ 𝜎 ′ for any state 𝜎 ′ . We call 𝜎 ′ a final state.

3.4   Determinism in Programs
To prove equivalence between two programs using their final states, we first need to prove that a
final state is unique, i.e., that for every program 𝑃, only one state 𝜎 exists such that 𝑃 ⇓ 𝜎. This
means that program interpretation is deterministic, i.e., will always produce the same end state for
every program. To prove the determinism of our semantics, we follow a similar approach to prior
work on deterministic concurrent systems [14, 28] and prove confluence of our semantics.
   For any state 𝜎, let 𝜎.𝐺 be the state’s memory graph 𝐺, whether the state is of the form (𝑀, 𝐺) or
𝑒𝑟𝑟𝑜𝑟 (𝐺). Similarly, let 𝜎.𝑀 be the (non-error) state’s memory 𝑀. We use 𝜎 →𝑛 𝜎 ′ as a shorthand
for 𝜎 →𝑛? 𝜎 ′ ∧ 𝜎 → 𝜎 ′ .
   Lemma 3.3 (Weak Progress). Let 𝜎 be a state where 𝜎0 →∗ 𝜎, where 𝜎0 is some starting state.
If 𝜎0 →𝑛 𝜎𝑛 and 𝜎0 →𝑚 𝜎𝑚 , then either 𝜎𝑚 = 𝑒𝑟𝑟𝑜𝑟 or there exists a state 𝜎𝑚𝑛 such that 𝜎0 →𝑚
𝜎𝑚 →𝑛 𝜎𝑚𝑛 .
   Proof. All transitions →𝑚 must only add edges to nodes with the same scope as 𝑚. We know
that 𝑛 and 𝑚 have different task IDs because 𝑛 ∥ 𝑚, so we can conclude that 𝑛 will still be a task
leaf in 𝜎𝑚 .𝐺. Since 𝑛 is still a task leaf, the only way for →𝑛 to not be a valid transition out of 𝜎𝑚
12                        Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


is if 𝑛 is a wait or acquire and 𝜎𝑚 .𝐺 does not contain the necessary set or release nodes. We
know that 𝜎0 .𝐺 contains the necessary nodes and that no transitions remove nodes from the graph,
so we can conclude that 𝜎𝑚 → 𝜎𝑚𝑛 for some 𝜎𝑚𝑛 .                                                □
  Lemma 3.4 (Graph Independence). For nodes 𝑛 and 𝑚, if 𝜎0 →𝑛 𝜎𝑛 and 𝜎0 →𝑚 𝜎𝑚 →𝑛 𝜎𝑚𝑛 ,
then 𝜎𝑚𝑛 = 𝑒𝑟𝑟𝑜𝑟 or 𝜎𝑚𝑛 .𝐺 \ 𝜎𝑚 .𝐺 = 𝜎𝑛 .𝐺 \ 𝜎0 .𝐺. If 𝜎𝑛 = 𝑒𝑟𝑟𝑜𝑟 , then 𝜎𝑚𝑛 = 𝑒𝑟𝑟𝑜𝑟 .
   Proof. We consider two different cases based on the rule that produced the transition 𝜎0 →𝑛 𝜎𝑛 .
   First, we consider the cases where 𝜎0 →𝑛? 𝑒𝑟𝑟𝑜𝑟 (𝜎0 .𝐺). This is the only case where 𝜎𝑛 = 𝑒𝑟𝑟𝑜𝑟 and
𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝜎𝑛 .𝐺), and corresponds to a while condition, a variable index containing a symbolic
value, or a semaphore operation depending on a symbolic value.
   In the case where 𝜎𝑛 = 𝜎𝑚𝑛 = 𝑒𝑟𝑟𝑜𝑟 , the lemma trivially holds.
   We show by contradiction that a case where 𝜎𝑛 = 𝑒𝑟𝑟𝑜𝑟 and 𝜎𝑚𝑛 ≠ 𝑒𝑟𝑟𝑜𝑟 cannot exist. Since
𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝜎𝑛 .𝐺), there must exist a symbolic variable, 𝑣 [𝑐], which is read in a loop condition
expression (for while), an index expression (for assignments), or an argument (for semaphore
operations) in 𝑛. This means that 𝑣 [𝑐] has not been written to in 𝜎0 . For 𝜎𝑚𝑛 to not be 𝑒𝑟𝑟𝑜𝑟 , 𝑚 must
be a write to 𝑣 [𝑐] to make 𝑣 [𝑐] defined in 𝜎𝑚 .𝑀. Since 𝑛 ∥ 𝑚, this violates item 1 of 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑
causing a race condition, so ¬𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝜎𝑚𝑛 .𝐺). Therefore, 𝜎𝑚𝑛 = 𝑒𝑟𝑟𝑜𝑟 , contradicting the
assumption that 𝜎𝑚𝑛 ≠ 𝑒𝑟𝑟𝑜𝑟 .
   Next, we consider the cases where 𝜎0 →𝑛? 𝜎𝑛 , where either 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝜎𝑛 .𝐺) and 𝜎𝑛 ≠ 𝑒𝑟𝑟𝑜𝑟 ,
or ¬𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝜎𝑛 .𝐺) and 𝜎0 → 𝑒𝑟𝑟𝑜𝑟 . In both cases, 𝜎𝑚 ≠ 𝑒𝑟𝑟𝑜𝑟 .
   If 𝑛 = (𝑠, 𝑝; 𝑃) and 𝑝 is not an async, while, wait, or acquire statement, its evaluation must
add only {𝑛 → (𝑠, 𝑃)} to the graph according to the semantics, regardless of the previous memory
or graph state. If 𝑚 is evaluated first, we know that 𝑛 can be evaluated from Lemma 3.3 and that
it will add the same node. In this case, 𝜎𝑚𝑛 .𝐺 \ 𝜎𝑚 .𝐺 = 𝜎𝑛 .𝐺 \ 𝜎0 .𝐺 = {𝑛 → (𝑠, 𝑃)}. We also must
prove that 𝜎𝑛 = 𝑒𝑟𝑟𝑜𝑟 implies that 𝜎𝑚𝑛 = 𝑒𝑟𝑟𝑜𝑟 . Since 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝜎𝑚 .𝐺) and 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝜎0 .𝐺),
the invalidity of 𝜎𝑛 .𝐺 must result from the additions from 𝑛, which 𝜎𝑚𝑛 also contains. The only
way additions from 𝑚 could fix this invalidity is if 𝑛 causes a race from 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 item 1 and 𝑚
added an edge that synchronized 𝑛 with the other statement(s) causing a race. This is impossible
because all transitions from 𝑚 can only add edges to nodes with the same ID, and 𝑛 ∥ 𝑚.
   If 𝑛 = (𝑠, async{𝑃 ′ }; 𝑃), the reasoning is the same as above: the nodes added to the graph are
independent of the memory state and 𝑛 must be a task leaf in both 𝜎0 and 𝜎𝑚 , so 𝜎𝑚𝑛 .𝐺 \ 𝜎𝑚 .𝐺 =
𝜎𝑛 .𝐺 \ 𝜎0 .𝐺 = {𝑛 → (𝑠, 𝑃), 𝑛 → (𝑖𝑑 · 𝑠, 𝑃 ′ )}.
   If 𝑛 = (𝑠, wait(𝑠𝑒𝑚, 𝑒); 𝑃), there exists a node 𝑛𝑠 in 𝜎0 .𝐺 such that 𝑐𝑜𝑟𝑟 _𝑠𝑒𝑡 (𝜎0 .𝐺, 𝑛, 𝑛𝑠 ) be-
cause there exists a transition →𝑛 from 𝜎0 , and that ¬𝑐𝑜𝑟𝑟 _𝑠𝑒𝑡 (𝜎0 .𝐺, 𝑛, 𝑚) because 𝑛 ∥ 𝑚 and
𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝜎0 .𝐺). If 𝜎𝑚 .𝐺 \ 𝜎0 .𝐺 contains a node 𝑚 ′ such that 𝑐𝑜𝑟𝑟 _𝑠𝑒𝑡 (𝜎0 .𝐺, 𝑛, 𝑚 ′ ), then 𝜎𝑚𝑛 =
𝑒𝑟𝑟𝑜𝑟 because 𝑛 has more than one corresponding set, violating 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 item 2. Otherwise, the
wait can only add the following set of edges: 𝜎𝑚𝑛 .𝐺 \ 𝜎𝑚 .𝐺 = 𝜎𝑛 .𝐺 \ 𝜎0 .𝐺 = {𝑛 → (𝑠, 𝑃), 𝑛𝑠 → 𝑛}.
   Similarly, if 𝑛 = (𝑠, acquire(𝑠𝑒𝑚, 𝑒); 𝑃), there must exist a set of nodes 𝑁𝑟 ⊆ 𝜎0 .𝐺 such that
𝑐𝑜𝑟𝑟 _𝑟𝑒𝑙 (𝜎0 .𝐺, 𝑛, 𝑛𝑟 ) for all 𝑛𝑟 ∈ 𝑁𝑟 , and |𝑁𝑟 | = 𝑐 where 𝑒 ⇓𝑀,𝑠 𝑐 because there exists a transition
→𝑛 from 𝜎0 . If 𝜎𝑚 .𝐺 \ 𝜎0 .𝐺 contains a node 𝑚 ′ such that 𝑐𝑜𝑟𝑟 _𝑟𝑒𝑙 (𝜎0 .𝐺, 𝑛, 𝑚 ′ ), then 𝜎𝑚𝑛 = 𝑒𝑟𝑟𝑜𝑟
because the sum of corresponding release values is greater than 𝑐, violating 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 item 5. If
𝜎𝑚 .𝐺 \ 𝜎0 .𝐺 contains a node 𝑚 ′ such that 𝑚 ′ is an acquire and 𝑚 ′ ∥ 𝑛, then 𝜎𝑚𝑛 = 𝑒𝑟𝑟𝑜𝑟 because
two acquires can happen in parallel, violating 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 item 4. Otherwise, the acquire can only
add the following set of edges: 𝜎𝑚𝑛 .𝐺 \ 𝜎𝑚 .𝐺 = 𝜎𝑛 .𝐺 \ 𝜎0 .𝐺 = {𝑛 → (𝑠, 𝑃)} ∪ {𝑛𝑟 → 𝑛 | 𝑛𝑟 ∈ 𝑁𝑟 }.
   Statements that use while are the only statements where the nodes that are produced by
evaluation depends on the value of an expression. If 𝑛 = (𝑠, while(𝑒){𝑃 ′ }; 𝑃), we first consider
the case where the set of variables read in the condition 𝑒 and the set of variables written to by
𝑚 are disjoint. In this case, the values of 𝑒 when evaluated under 𝜎𝑛 .𝑀 and 𝜎𝑚𝑛 .𝑀 are the same
Practical Formal Verification for MLIR Programs                                                             13


because 𝑚 does not write to any variables read in 𝑒, so the node added to the graph will be the
same in 𝜎𝑛 and 𝜎𝑚𝑛 . In the case where 𝑚 writes to a variable read in the condition 𝑒, then we know
¬𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝜎𝑚𝑛 .𝐺) as per 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 item 1, so 𝜎𝑚𝑛 .𝐺 = 𝑒𝑟𝑟𝑜𝑟 .                              □
  For two memory states 𝑀 and 𝑀 ′ , we define a difference 𝑀 ′ −𝑀 that represents the changes to 𝑀
performed in 𝑀 ′ . If (𝑖𝑑, 𝑣) ∈ dom(𝑀 ′ ) and either (𝑖𝑑, 𝑣) ∉ dom(𝑀) or (𝑖𝑑, 𝑣) ∈ dom(𝑀)∧𝑀 (𝑖𝑑, 𝑣) ≠
𝑀 ′ (𝑖𝑑, 𝑣), (𝑀 ′ −𝑀) (𝑖𝑑, 𝑣) = 𝑀 ′ (𝑖𝑑, 𝑣). We need to prove that changes to the memory state performed
by statements that may happen in parallel are disjoint, which we formulate similarly to Lemma 3.4.
  Lemma 3.5 (Memory Independence). For nodes 𝑛 and 𝑚, if 𝜎0 →𝑛 𝜎𝑛 and 𝜎0 →𝑚 𝜎𝑚 →𝑛 𝜎𝑚𝑛 ,
then 𝜎𝑚𝑛 = 𝑒𝑟𝑟𝑜𝑟 or 𝜎𝑚𝑛 .𝑀 − 𝜎𝑚 .𝑀 = 𝜎𝑛 .𝑀 − 𝜎0 .𝑀.
   Proof. We only consider 𝜎𝑚𝑛 ≠ 𝑒𝑟𝑟𝑜𝑟 , where 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝜎𝑚𝑛 .𝐺) (otherwise the lemma triv-
ially holds). If 𝑛 is not a declaration or an assignment, 𝜎𝑚𝑛 .𝑀 − 𝜎𝑚 .𝑀 = 𝜎𝑛 .𝑀 − 𝜎0 .𝑀 = ∅ since no
other transitions can modify the memory state.
   If 𝑛𝑐𝑜𝑑𝑒 = (int 𝑣 []; 𝑃), we only need to consider the case where (𝑛𝑖𝑑 , 𝑣) ∉ dom(𝜎0 .𝑀), since
otherwise the transition →𝑛 does not modify the memory state. We assume, for the purpose
of contradiction, that (𝑛𝑖𝑑 , 𝑣) ∈ dom(𝜎𝑚 .𝑀). In this case, 𝑚 must be either a declaration or an
assignment. If (𝑛𝑖𝑑 , 𝑣) has not already been declared, the only way 𝑚 can access (𝑛𝑖𝑑 , 𝑣) is if
𝑚𝑖𝑑 = 𝑛𝑖𝑑 , because otherwise 𝑔𝑒𝑡_𝑣𝑎𝑟 will only return a variable in the global scope, not the
variable associated with 𝑛𝑖𝑑 . Since 𝑛 ∥ 𝑚, 𝑛 and 𝑚 must have different task IDs, which contradicts
our assumption. We now know that (𝑛𝑖𝑑 , 𝑣) ∉ dom(𝜎𝑚 .𝑀), so we can conclude that 𝜎𝑚𝑛 .𝑀 −𝜎𝑚 .𝑀 =
𝜎𝑛 .𝑀 − 𝜎0 .𝑀 = {((𝑛𝑖𝑑 , 𝑣), ∅)} from the definition of 𝑚𝑒𝑚_𝑑𝑒𝑐𝑙.
   If 𝑛𝑐𝑜𝑑𝑒 = (𝑣 [𝑒𝑖 ] = 𝑒; 𝑃), we first consider the case where the set of variables read in the
expressions 𝑒 and 𝑒𝑖 and the set of variables written to by 𝑚 are disjoint. In this case, the values of 𝑒
and 𝑒𝑖 when evaluated under 𝜎0 .𝑀 and 𝜎𝑚 .𝑀 are the same because 𝑚 does not write to any variables
read in 𝑒, so 𝑛 will make the same modifications. In this case, 𝜎𝑚𝑛 .𝑀 − 𝜎𝑚 .𝑀 = 𝜎𝑛 .𝑀 − 𝜎0 .𝑀 =
{((𝑛𝑖𝑑 , 𝑣), (𝑐𝑖 ↦→ 𝑒 ′ )}, where 𝑒𝑖 ⇓𝑀,𝑠 𝑐𝑖 and 𝑒 ⇓𝑀,𝑠 𝑒 ′ . In the case where 𝑚 writes to a variable read
in the condition 𝑒, then we know ¬𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝜎𝑚𝑛 .𝐺) because 𝑛 ∥ 𝑚 as per 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 item 1,
so 𝜎𝑚𝑛 .𝐺 = 𝑒𝑟𝑟𝑜𝑟 .                                                                                       □
   Theorem 3.6 (Diamond Property). For state 𝜎 = (𝑀, 𝐺), if 𝜎 →𝑛 𝜎 ′ and 𝜎 →𝑚 𝜎 ′′ then there
exist 𝜎𝑐′ , 𝜎𝑐′′ such that 𝜎 ′ →= 𝜎𝑐′ and 𝜎 ′′ →= 𝜎𝑐′′ and 𝜎𝑐′ = 𝜎𝑐′′ , where →= is the reflexive closure of →.
    Proof. First, we know that 𝜎 ≠ 𝑒𝑟𝑟𝑜𝑟 and that 𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝐺). If 𝜎 were 𝑒𝑟𝑟𝑜𝑟 , there would be
no outgoing transitions from 𝜎. 𝐺 must be valid because the starting graph for every program is
valid, and all transitions preserve graph validity except transitions to 𝑒𝑟𝑟𝑜𝑟 . We also know 𝑛 ∥ 𝑚. If
𝑛 and 𝑚 were ordered, only one would be a leaf and thus only one would be evaluable from 𝜎.
    If both 𝜎 ′ and 𝜎 ′′ are 𝑒𝑟𝑟𝑜𝑟 , 𝜎𝑐′ = 𝜎𝑐′′ = 𝑒𝑟𝑟𝑜𝑟 .
    If exactly one of 𝜎 ′ and 𝜎 ′′ is 𝑒𝑟𝑟𝑜𝑟 (we assume wlog that 𝜎 ′ = 𝑒𝑟𝑟𝑜𝑟 and 𝜎 ′′ ≠ 𝑒𝑟𝑟𝑜𝑟 ), 𝜎𝑐′ = 𝜎𝑐′′ =
𝑒𝑟𝑟𝑜𝑟 . From Lemma 3.3, we know that a transition 𝜎 ′′ →𝑛 𝜎𝑐 exists for some 𝜎𝑐 . From Lemma 3.4,
we know that 𝜎 ′ = 𝑒𝑟𝑟𝑜𝑟 implies 𝜎𝑐 = 𝑒𝑟𝑟𝑜𝑟 , so 𝜎𝑐′ = 𝜎𝑐′′ = 𝑒𝑟𝑟𝑜𝑟 .
    If neither 𝜎 ′ nor 𝜎 ′′ is 𝑒𝑟𝑟𝑜𝑟 , then we pick 𝜎𝑐′ and 𝜎𝑐′′ such that 𝜎 ′ →𝑚 𝜎𝑐′ and 𝜎 ′′ →𝑛 𝜎𝑐′′ (we know
that these states must exist from Lemma 3.3). From Lemma 3.4, we know that 𝜎𝑐′ .𝐺\𝜎 ′ .𝐺 = 𝜎 ′′ .𝐺\𝜎.𝐺
and 𝜎𝑐′′ .𝐺 \ 𝜎 ′′ .𝐺 = 𝜎 ′ .𝐺 \ 𝜎.𝐺. We also know that 𝜎.𝐺 ⊆ 𝜎 ′ .𝐺 ⊆ 𝜎𝑐′ .𝐺 and 𝜎.𝐺 ⊆ 𝜎 ′′ .𝐺 ⊆ 𝜎𝑐′′ .𝐺,
because all transitions can only add edges to the graph, not remove them. From this, we know that
𝜎𝑐′ .𝐺 = 𝜎𝑐′′ .𝐺 = 𝜎 ′ .𝐺 ∪ 𝜎 ′′ .𝐺, and we define 𝐺𝑐 = 𝜎 ′ .𝐺 ∪ 𝜎 ′′ .𝐺.
    If ¬𝑔𝑟𝑎𝑝ℎ_𝑣𝑎𝑙𝑖𝑑 (𝐺𝑐 ), 𝜎𝑐′ = 𝜎𝑐′′ = 𝑒𝑟𝑟𝑜𝑟 . Otherwise, from Lemma 3.5, we know that 𝜎𝑐′ .𝑀 − 𝜎 ′ .𝑀 =
𝜎 .𝑀 − 𝜎.𝑀 and 𝜎𝑐′′ .𝑀 − 𝜎 ′′ .𝑀 = 𝜎 ′ .𝑀 − 𝜎. Since there are no transitions (𝑀, 𝐺) → (𝑀 ′, 𝐺 ′ ) such
  ′′

that 𝑀 ⊈ 𝑀 ′ , we know that 𝜎.𝑀 ⊆ 𝜎 ′ .𝑀 ⊆ 𝜎𝑐′ .𝑀 and 𝜎.𝑀 ⊆ 𝜎 ′′ .𝑀 ⊆ 𝜎𝑐′′ .𝑀. From this, we know
that 𝜎𝑐′ .𝑀 = 𝜎𝑐′′ .𝑀 = 𝜎.𝑀 ∪ (𝜎 ′ .𝑀 − 𝜎.𝑀) ∪ (𝜎 ′′ .𝑀 − 𝜎.𝑀). We can now conclude that 𝜎𝑐′ = 𝜎𝑐′′ . □
14                         Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


  Theorem 3.7 (Confluence). For state 𝜎, if 𝜎 →∗ 𝜎 ′ and 𝜎 →∗ 𝜎 ′′ then there exist states 𝜎𝑐′ , 𝜎𝑐′′
such that 𝜎 ′ →∗ 𝜎𝑐′ , 𝜎 ′′ →∗ 𝜎𝑐′′ , and 𝜎𝑐′ = 𝜎𝑐′′ .
   Proof. Semi-confluence follows from Theorem 3.6 via induction on the length of the path to 𝜎 ′ ,
from which confluence follows via induction on the length of the path to 𝜎 ′′ [9, § 2.7].      □
     Theorem 3.8 (Determinism). If 𝑃 ⇓ 𝜎 and 𝑃 ⇓ 𝜎 ′ , 𝜎 = 𝜎 ′ .
  Proof. Let the initial state of 𝑃 be 𝜎0 . From the definition of ⇓, 𝜎0 →∗ 𝜎 and 𝜎0 →∗ 𝜎 ′ . From
Theorem 3.7, we know that there exists a 𝜎𝑐′ such that 𝜎 →∗ 𝜎𝑐′ and a 𝜎𝑐′′ such that 𝜎 ′ →∗ 𝜎𝑐′′ . Since
both 𝜎 and 𝜎 ′ are final states, 𝜎 = 𝜎𝑐′ = 𝜎 ′ = 𝜎𝑐′′ .                                                □
   Determinism also means that deadlock is always detectable in our system. We define deadlock
as a non-error state with no outgoing transitions (that is "stuck") where there exists a node that is
a task leaf, but has not finished executing its corresponding program.
   Definition 3.9 (Deadlock). A state 𝜎 = (𝑀, 𝐺) is deadlocked if it is a final state and there exists
a node 𝑛 in 𝐺 such that 𝑡𝑎𝑠𝑘_𝑙𝑒𝑎𝑓 (𝑛) and 𝑛𝑐𝑜𝑑𝑒 ≠ 𝜖.
  Corollary 3.10 (Deadlock Detection). If 𝑃 ⇓ 𝜎 and 𝜎 is deadlocked, every final state of 𝑃
deadlocks.
     Proof. Follows from Theorem 3.8.                                                                         □

3.5     Equivalence between Programs
Our final theorem defines equivalence between programs. First, if two programs 𝑃𝐴 and 𝑃𝐵 have
reached their final state without error, and the memory computed for each is identical, then they
are equivalent, denoted 𝑃𝐴 ≡ 𝑃𝐵 .
  Theorem 3.11 (Strict program eqivalence). Suppose that 𝑃𝐴 ⇓ 𝜎𝐴 = (𝑀𝐴 , 𝐺𝐴 ), 𝑃𝐵 ⇓ 𝜎𝐵 =
(𝑀𝐵 , 𝐺 𝐵 ), 𝜎𝐴 ≠ 𝑒𝑟𝑟𝑜𝑟 , and 𝜎𝐵 ≠ 𝑒𝑟𝑟𝑜𝑟 . If 𝑀𝐴 = 𝑀𝐵 , then 𝑃𝐴 ≡ 𝑃𝐵 .
  Proof. The final state is unique per Theorem 3.8. If 𝑀𝐴 = 𝑀𝐵 , then for all 𝑣, we know 𝑀𝐴 (𝑣) =
𝑀𝐵 (𝑣). If all variables accessed by both programs hold the same final value, then 𝑃𝐴 computes the
same results as 𝑃𝐵 ; that is, 𝑃𝐴 ≡ 𝑃𝐵 .                                                          □
   Note that we can broaden beyond strict equality by designing a system to normalize 𝑀 before
checking for equality of values, for example by deploying rewrite rules to normalize symbolic
expressions (e.g., 𝑠𝑦𝑚(𝑎 ∗ 𝑏) ≡ 𝑠𝑦𝑚(𝑏 ∗ 𝑎)), as discussed below.
   Technically, Theorem 3.11 is overly restrictive: only variables which are still visible when the
program terminates need to have the same values, while temporary variables (e.gw., a loop counter)
may have different values. In our implementation, we keep track of local variables (those local to
tasks spawned by the program and therefore deleted when the task terminates without error), and
only check equivalence for the remaining non-local variables. As we identify variables by name
across programs, it is necessary for non-local variables to have identical names in both programs, a
typical scenario when one program is a transformation of the other. This leads to Theorem 3.12,
where we check the union of programs’ non-local variables to detect side effects appearing in one
program but not the other.
   Theorem 3.12 (Eqivalence of non-local variables). Suppose 𝑃𝐴 ⇓ 𝜎𝐴 = (𝑀𝐴 , 𝐺𝐴 ) and
𝑃𝐵 ⇓ 𝜎𝐵 = (𝑀𝐵 , 𝐺 𝐵 ), and that 𝑆 = {𝑣 | 𝑀𝐴 (𝑣) = 𝑀𝐵 (𝑣)} is the set of variables which are equivalent.
Suppose that 𝑉 is the union of the non-local variables in 𝑃𝐴 and 𝑃𝐵 : memory locations which are
reachable after program termination. Then 𝑉 ⊆ 𝑆 implies that 𝑃𝐴 ≡ 𝑃𝐵 .
Practical Formal Verification for MLIR Programs                                                          15


  Proof. Follows from Theorem 3.11 and Theorem 1 in [43] proving the final CDAGs can only
contain symbols of non-local variables.                                                □

   We remark that equivalence only holds for the set 𝑉 in Theorem 3.12. 𝑉 may contain concrete
values for some variables (e.g., N=32) and symbolic expressions for other (e.g., their final value is
stored as a CDAG C[0][0]=...+(+(*(A[0][0], B[0][0]),*(A[0][1],B[1][0]),...)). If the
programs are correct executable tests, all values are concrete in 𝑉 , and the proof holds only for
these concrete values. However, programs can also contain input non-local variables that are
not written before being read by the program, which are automatically treated as symbolic. The
equivalence result holds for any value symbolic variables may concretely take. However, for
our hybrid interpretation to terminate, the control-flow needs to be deterministically computed.
Typically, this requires fixed problem sizes (e.g., N=32). As shown in Sec. 6, for a large class of useful
programs such as dense linear algebra and related AI workloads, only the problem size is fixed; the
equivalence computation is performed on symbolic input data. This makes the correctness result
highly practical and far more general than simple testing.

4     PEQC-MLIR Implementation
We now present additional details on our full PEQC-MLIR implementation for correctness checking,
before presenting how to translate and lower MLIR programs to PEQC-MLIR’s IR (PIR) in Sec. 5.

4.1    From Featherweight language to PIR
We proved in the prior Sec. 3 that any program processed to termination without error by our
system is a deterministic concurrent program, free of races and deadlocks, and amenable to simple
equivalence checking with other programs. Technically, this is restricted to two programs where
one is a substitute for the other, i.e., they both have necessarily the same execution context. Details
are provided in [43].
   The featherweight language carries all the necessary key constructs (synchronizations, paral-
lelism, control-flow), but it remains a subset of the complete language we support. PEQC-MLIR
supports a subset of the C language in terms of control-flow and arithmetic operations. They
can either be translated immediately to the featherweight language, or are treated identically to
constructs in it.
   The PEQC-MLIR intermediate representation, that is, the language that PEQC-MLIR takes as
input, contains all standard unary and binary operators from the C language, whose treatment is
analogous to 𝑒 1 + 𝑒 2 . Blocks, for loops, and if-conditionals can be reconstructed from while(𝑒){𝑃 }.
Function calls require that user guarantees the function is pure (e.g., 𝑚𝑖𝑛(𝑎, 𝑏)) or that the function
definition exists in the file; control is transferred to its definition, possibly after assigning arguments.
Goto statements are handled similarly. We support general for (init; test; increment) body;
loops in C, they can be immediately translated to init; while (test) { body; increment;};
similarly for if (e) {...}. Function calls are processed using an inlining-style approach, and
recursive functions are not supported. We support all operators of the C language (+, *, /, !=, >>,
etc.) in the concrete evaluator, following C semantics.
   In addition, we provide an API (functions and types) intercepted by PEQC-MLIR to represent
concurrency constructs: peqc_semaphore_wait(), etc. for each of the operations in the feather-
weight language (async, wait, set, acquire, release) which behave as formalized in the prior
section. We also provide a specific data type for the semaphores, enabling their tracking in the
program easily.
   PIR is rich enough to capture a rich set of concurrent programs, as exemplified in Sec. 6. Our
prior work includes supporting a subset of OpenMP pragmas [56] which are lowered to PIR using
16                       Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


semantically equivalent async and semaphore synchronizations. Details and documentation are
available directly in the PEQC-MLIR software on Github [55].


4.2    Hybrid Interpretation and Concurrency Checking
During interpretation, the happens-before graph 𝐺 is represented explicitly, with a node for each
statement instance. In practice, the size of this graph can be reduced significantly by combining
nodes in 𝐺, reducing its size and improving the speed to query it for correctness checking.
   If two statement instances do not contain semaphore operations or spawn a task, both nodes will
only have one input and output edge. The nodes corresponding to these statements can therefore
be merged into a single "macro-node" during interpretation, to reduce the size of the graph and thus
reduce the time to check the happens-before relationship between two nodes. We implemented
this optimization in PEQC-MLIR.


4.3    Equivalence Checking
As shown in Sec. 6, the time to conduct equivalence checking is mostly negligible compared with
the time to build the normalized memory representations using CDAGs [43]: we typically rely
exclusively on exact matching between the two memory states: that is, computing whether CDAGs
are identical, a simple linear-time process. To reduce memory space, we employ memory pooling
and shadow copies, so that CDAGs used in multiple live-out memory cells are represented only
once in memory, leading to linear-time equivalence checking. However, there are situations where
the user may wish to deploy further normalization, for example to tolerate associative/commutative
reorderings of operations, as described below.

   Normalization of symbolic expressions PEQC-MLIR includes a rewrite-rule system that can be
applied on CDAGs to normalize them prior to equivalence checking. This proves particularly
useful to handle transformations that change the nature and count of symbolic operations, such
as factorization/distribution for expressions. The user must ensure that these are semantically
applicable on the program verified; we do not perform any such analysis. We did not use nor need
any such custom rewrites in our experiments in Sec. 6.
   We also support normalization of associative and commutative operations by sorting the tree
lexicographically (average 𝑂 (𝑛𝑙𝑜𝑔(𝑛))) after merging associative operations under a 𝑛-ary node
with all operations of that type, supporting +,*,min,max natively, similar to Eker et al. [18]. We
also offer simple normalizations, such as /($x $x) = 1, +($x 0) = $x, *($x 0) = 0, as well as
their commuted variants.


5     Enabling Correctness Checking of MLIR Programs
We now present our approach to lowering and translation of a rich class of MLIR programs to our
parallel language intermediate representation described in the previous section.
  Our approach to support MLIR program correctness verification is to translate a MLIR program
made only of standard dialects into our intermediate program representation. Technically, PEQC-
MLIR is equipped with a restricted parser for the C language, and exposes an API via specific
function calls in the program which are intercepted by the interpreter to model task spawns and
the various synchronizations we support. Equipped with this translator, we then rely on existing
LLVM MLIR lowering passes for specific dialects (e.g., affine) and develop our own MLIR lowering
passes for the MLIR-AIR and MLIR-AIE dialects, presented in Secs. 5.3 onward.
Practical Formal Verification for MLIR Programs                                                                             17



                              User-defined dialect
                                                     Lowered MLIR
                                  conversion
                                                     program
                                                     scf.for, if
                                                     async.execute                        Interpretable
                                                     async.await_all
                                                                                          Program
             Input MLIR                              func.func, call        MLIR-to-PIR
                              AIR/AIE conversion     memref.load, store
                                                                                          peqc_sem_wait
              program                                                       Translator    peqc_sem_signal
                                                     memref.copy, subview
                                                                                          peqc_task_spawn
                                                     subset of arith ops                  ...
                                                     verif.semaphore
                                                     verif.semaphore.wait
                                Standard dialect     verif.semaphore.set                        Standard dialects
                                   conversion        ...                                        Other dialects
                                                                                                MLIR-to-C+API translation
                                                                                                User-defined conversion


             Fig. 7. Illustration of conversion and translation to PIR for eventual interpretation



5.1   Translation to PEQC-MLIR Intermediate Representation
This stage takes as input an MLIR program made only of a subset of func, arith, math, memref,
scf and async. It then translates it to a C-syntax AST, which contains function calls to PEQC-
MLIR’s concurrent API when translating async. As discussed below in Sec. 5.3, we also provide a
dedicated verif MLIR dialect in PEQC-MLIR, to offer the semaphore types and operations on them
(wait/set/acquire/release) and facilitate encoding of concurrent constructs arising in MLIR
dialects. The verif dialect translates directly to the PEQC-MLIR C API for concurrency.
   We note that the simple route of converting an MLIR program to C does not work in general: the
emitc dialect and associated tools do not support the programs we target, especially when foreign
dialects are used.
   Translation of arith and math is trivial; we support 25 operations to date. scf and func are
similarly straightforward. In contrast, memref and async are more subtle. For memref, we emulate
operations such as copy, subview, etc., with a pointwise loop iterating over all elements to be
copied. subview is treated by creating a temporary variable, and inserting flushes to the original
memref before the original is next accessed. For async, we translate tokens to semaphores and insert
the corresponding set/wait as needed in operations that depend on the tokens, also producing a
final semaphore when the async operation concludes for subsequent use. We encode async.group
entries with distinct semaphores, one per member in the group. We do not implement a barrier
construct, but instead explicitly create as many point-to-point synchronizations as needed. While
this may not be the most efficient, this approach is flexible and allows us to seamlessly model the
asynchronous AIR and AIE dialects, OpenMP programs, etc.

5.2   Leveraging Existing MLIR Lowering Passes
To maximize the set of MLIR programs we can take as input, we rely on existing lowering passes
 provided with the standard mlir-opt toolchain. Correctness verification of these lowering passes is
 outside the scope of this paper; we focus on verification of programs here. Specifically, we expect the
 user to correctly lower programs to a subset of standard dialects from func, arith, math, memref,
 scf, and async. For example, -convert-linalg-to-affine-loops converts linalg operations
(e.g., matmul) to an expanded (e.g., the 3D loop nest for matmul) MLIR affine program. Then
-lower-affine lowers the affine dialect to scf and memref.
    To illustrate, our flow can take as input a linalg program from PyTorch, its tiled, optimized, and
 parallelized variant produced by the MLIR-AIR toolchain, and successfully lower them for eventual
 translation and verification, as shown in Sec. 6.1. To achieve this, we designed our own conversion
 passes to standard dialects for two user-defined dialects: AIR and AIE.
18                                Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


5.3      Lowering of the MLIR-AIR Dialect
The MLIR-AIR dialect captures explicit asynchronous control, hierarchical parallelism, and dataflow
between compute and memory, serving as a structured intermediate layer that bridges high-level
abstractions and low-level accelerator code generation [59]. While some lowering passes are
provided for standard MLIR dialects, user-defined dialects such as AMD’s AIR and AIE must also
be lowered to standard dialects. We developed these converters for a large subset of AIR and AIE
constructs.
  Our open-source software contains extensive documentation on operations we support, our
approach to translation, and the complete C++ implementation of these converters (built using
the LLVM MLIR infrastructure [40]). We illustrate below three constructs from the AIR dialect.
Our implementation supports all AIR operations, albeit with some restrictions on arguments and
options supported.
   Conversion of air.execute The async dialect enables the description of sets of parallel tasks;
tokens produced during task execution enable synchronizations between tasks spawned using
async.execute. We convert air.execute to async.execute, a process that involves analyzing
the air.tokens used for synchronization in the AIR program and converting them to groups of
async tasks, and handling value results returned by parallel tasks. This is a form of lowering, as we
encode the semantics of the source dialect operation via a new MLIR program fragment made only
of standard operations that preserves the original execution semantics. In this case, AIR follows
the semantics of an existing standard async operation, making conversion straightforward.
   Conversion of air.herd Herds in the AIR dialect represent “a one or two dimensional array of
adjacent AIE cores executing the same code region" [6]. In other words, one can create a parallel
task for each AIE core modeled, and execute the same code block on each of them: this amounts to
a parallel loop (nest). We therefore convert air.herd to scf.parallel, a construct capturing the
parallelism and constraints of air.herd.
   Conversion of air.channel AIR Channels are used to communicate data and synchronize
between concurrent entities. In contrast to the above examples, channels do not follow existing
constructs in standard dialects. Channels can have blocking read/write operations (e.g., behaving
like a blocking FIFO), broadcast to multiple destinations, and optionally perform on-the-fly data
layout transformations of the data pushed to or pulled from the channel.
      / / An a r r a y o f 4 x 4 s t r e a m i n g DMA c h a n n e l s
      a i r . c h a n n e l @chan_0 [ 4 , 4 ] { c h a n n e l _ t y p e = " dma_stream " }
      / / A s t r e a m i n g DMA c h a n n e l b r o a d c a s t i n g t o 4 d e s t i n a t i o n s
      a i r . c h a n n e l @chan_1 [ 1 , 1 ] { b r o a d c a s t _ s h a p e = [ 1 , 4 ] , c h a n n e l _ t y p e = " dma_stream " }
      / / R e c e i v e a 4 x4 t i l e i n t o % d s t f r om c h a n n e l @chan_0
      a i r . c h a n n e l . g e t @chan_0 (% d s t [% c0 , %c 0 ] [ % c4 , %c 4 ] [ % c1 , %c 1 ] ) : ( memref <16 x 1 6 x f 3 2 > )
      / / A s y n c h r o n o u s g e t w i t h d e p e n d e n c y on % t 1
      % t 2 = a i r . c h a n n e l . g e t a s y n c [% t 1 ] @chan_1 (% d s t [% c8 , %c 0 ] [ % c4 , %c 4 ] [ % c1 , %c 1 ] ) :
                  ( memref <16 x 1 6 x f 3 2 > )

To implement conversion of air.channel to standard dialects, we developed a conversion using
explicit memref buffers to store the data (and implement required data layout transformations,
by explicitly copying into the proper layout into a new buffer). We developed support for fine-
grain synchronizations to model blocking reads/writes if the channel buffer is full. Unfortunately,
async tokens can only be written once; this prevents modeling semaphores. For instance, to model
a binary semaphore, one would need to create one token per access to the channel, a property
immensely difficult to compute statically. To address this issue, we have developed a minimal verif
Practical Formal Verification for MLIR Programs                                                     19


dialect, dedicated to handling semaphores (wait, set, acquire, and release) as well as the type
verif.semaphore. The verif dialect has direct conversion to the PEQC-MLIR API. Consequently,
air.channels are converted to blocks of code containing: memrefs to store data, loops to copy data
into a different layout, one semaphore per channel, and waits/sets around read/write operations.

5.4    Lowering of the MLIR-AIE Dialect
While MLIR-AIR focuses on higher-level constructs useful for representing computations on
spatial architectures generally, MLIR-AIE is focused primarily on programming constructs that
map cleanly to Neural Processing Units [4]. We have implemented support for the following aie
operations: buffer, core, device, dma_bd, flow, lock, mem, memtile_dma, next_bd, objectfifo,
objectfifo.acquire, objectfifo.createObjectFifo, objectfifo.link, objectfifo.release,
objectfifo.subview.access, tile, use_lock, npu.dma_memcpy_nd, runtime_sequence. This is
not the full AIE dialect; specifically, operations related to low-level routing (e.g., packet_flow,
switchbox) are not currently implemented.
   Specifically, concurrent MLIR-AIE constructs such as aie.core and aie.mem are translated to
parallel tasks in the async dialect. Lock operations, such as lock and use_lock, represent counting
semaphores and are lowered into the verif dialect. More complex communication constructs, such
as aie.objectFifo, are lowered into a combination of buffer allocations, data copy operations,
and semaphores. The main complexity here is representing complex data layout transformations
that can be implemented as part of aie.objectFifo accesses. Most other constructs lower into
standard MLIR dialects representing sequential behavior, although some concurrent subtleties exist
as discussed later in Sec. 6.2.

6     Experiments
We now present experimental results on correctness verification of a variety of MLIR-based opti-
mization flows. We present detailed case studies for AIR in Sec. 6.1 and AIE in Sec. 6.2, demonstrating
the ability of PEQC-MLIR to verify optimized, high-performance implementations for the AI En-
gine, and to uncover subtle potential concurrency bugs. We then present extensive evaluation of
mlir-opt on the PolyBench/C benchmarking suite [42], demonstrating PEQC-MLIR’s ability to
quickly find numerous known limitations but also unknown bugs in the tested toolchain in Sec. 6.3.
  We have implemented all our tools as open-source, BSD-licensed software [55]. PEQC-MLIR
was evaluated using a single CPU core from an Intel Xeon E3-1240v6 server running at 3.70GHz,
with 32GB of memory.

6.1    Verification of MLIR-AIR
To demonstrate the ability of PEQC-MLIR to verify pairs of programs using possibly different
MLIR dialects prior to conversion, Table. 1 displays statistics for the evaluated program variants.
All variants are produced as intermediate steps in the MLIR-AIR compilation flow and eventually
are lowered to MLIR-AIE (further steps are evaluated in Sec. 6.2). Fig. 8 displays the flow of this
correctness verification approach.
   The linalg program is built from a Python specification, and represents a sequential dense
matrix-multiplication kernel, for a matrix (block) of size 32𝑥32 to be run on the AI Engine. air.input,
the reference input program to be compiled by the MLIR-AIR toochain into a valid MLIR-AIE
implementation on the AI Engine, was built by applying lowering of linalg to affine then to
scf. air.tiled is a hierarchically tiled transformation of air.input, specified with a user-defined
transformation script using the MLIR Transform dialect. It introduces AIR operations, such as
segments, DMA copies, etc. air.placed is optimized and lowered from air.tiled, and introduces
air.channels for communications.
20                                  Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang

                            Python                          Linalg                MLIR-AIR
                            matmul                          matmul                 input
                         sequential mm                    sequential mm          sequential mm




                                                                                 MLIR-AIR
                                                       LLVM MLIR
                                                    linalg-to-aﬃne-loops           tile
                                                                                    parallel mm
                      MLIR                                                        fixed 3D tiling
                     standard                                                        herds,…
                   dialects: scf,
                   arith, async
                                                       LLVM MLIR
                                                          lower-aﬃne
                   verif dialect

                                                                                MLIR-AIR
                                                      PEQC-MLIR                  placed
                                                       air-to-standard          concurrent mm
                                                                                 fixed 3D tiling
              MLIR to PEQC-IR
                                                                               herds,channels,..
                convert standard
                dialects in MLIR
                    to parallel
                                                      PEQC-MLIR
                                                       aie-to-standard
               C-style IR for PEQC

                                                                                MLIR-AIE
                                                                                  aie
                    PEQC
              compute normalized                                               concurrent mm
                                                       PEQCm                    fixed 3D tiling
               PEQCm symbolic
              program represent.                       deadlocks/race         core,tile,objfifo,..
                                                         detected,
                                                        deterministic
                     PEQC                             symbolic CDAGs
               Check for equivalence
                                                                                       Generated by AIR/AIE compilers,
                 between pairs of                                                      and manual modifications
                 PEQCm CDAGs
                                                                                      MLIR files: conversion and lowering of
                                                                                      MLIR dialects to standard MLIR dialects
                     YES?                           NO?
                                                                                      PEQC input files in PEQC IR
           Programs are equivalent         Error reported: mismatch
            correctness assessed          in computation performed,
            for all symbolic inputs        deadlocks, race reported


                         Fig. 8. Flow of AIR/AIE correctness checking with PEQC-MLIR.
   These programs are verified pairwise as illustrated in Fig. 8. First, they are converted to equivalent
standard MLIR dialects (using existing LLVM MLIR lowering passes, or PEQC-MLIR lowering passes
we have developed), then translated to PEQC-MLIR’s input Parallel Intermediate Representation
(PIR) as per Sec. 5. These PIR files are then checked pairwise for equivalence, following Sec. 3.
                Table 1. Statistics on intermediate files produced during AIR compilation flow.
      bench         S-LoC C-LoC I-LoC               nb-s nb-conc nb-sync hb-rat           𝑡𝑖𝑛𝑡  𝑡𝑒𝑞
      linalg              8        17       56   201870           0         0       0 1.61s N/A
      air.input          17        51       56   541420           0         0       0 3.39s 0.04s
      air.tiled         102       133      160   743594          25        25 0.0003 5.56s 0.04s
      air.placed        190       902    1030 1320799           440     77815    0.39 9.01s 0.04s

   We report in Table. 1 metrics about the program source (S-LoC: lines of code of original MLIR
file; C-LoC: for the converted program using only standard dialects; I-LoC: for the final PIR file
checked for correctness), and evaluation metrics (nb-s: total number of statements interpreted;
nb-conc: total number of tasks created; nb-sync: total number of synchronizations). hb-rat is the
ratio between the number of nodes in our representation of the graph 𝐺 divided by nb-s. Finally,
𝑡𝑖𝑛𝑡 is the total time to interpret, that is to produce the final memory state for the program, and 𝑡𝑒𝑞
is the total time to check equivalence between two memory states, with the one of the previous file.
In this set of experiments, all files were proved equivalent, leading to the maximum equivalence
time (the process ran to completion).
   Interpretation time follows roughly the number of statements interpreted, while equivalence time
remains constant since the memory states for non-local variables are identical in these experiments
(the programs are equivalent, for symbolic input matrices but a fixed problem size).
Practical Formal Verification for MLIR Programs                                                         21


6.2   Verification of AIE
PEQC-MLIR supports a rich subset of AIE operations, as described in Sec. 5.4. We now illustrate an
important case study, demonstrating the merits of PEQC-MLIR in catching subtle concurrency
bugs, as well as the ability to verify equivalent a low-level “hardware-friendly” optimized MLIR
program with the original, sequential linalg program. In this flow, the final AIR program with
channels and placement is lowered and optimized to an AIE representation with air-opt and
aie-opt.
   The final AIE file is 753 lines of code, leading to about 2.2k LoCs for the final PIR file obtained
after conversion and translation. In this case, PEQC-MLIR reported a possible race. Fig. 9 is an
excerpt from the matrix-multiply AIE program, but zooming in on a chain of acquire-release for a
task to execute on a PE (a memory tile). aie.dma_start(S2MM, 0, ˆbb1, ˆbb5) starts a DMA
communication, in the S2MM direction, and both basic blocks ˆbb1 and ˆbb5 are started in parallel.


 1 %memtile_dma_2_1 = a i e . memtile_dma (% m e m _ t i l e _ 2 _ 1 ) {
 2       %0 = a i e . d m a _ s t a r t ( S2MM , 0 , ^ bb1 , ^ bb5 )
 3    ^ bb1 :       / / 2 p r e d s : ^ bb0 , ^ b b 1
 4       a i e . u s e _ l o c k (% l o c k _ 2 _ 1 , A c q u i r e G r e a t e r E q u a l , 2 )
 5       a i e . dma_bd (% b u f 2 0 : memref <64 x 1 6 x i 3 2 , 1 : i 3 2 > , 0 , 1 0 2 4 )
 6       { task_id = 0 : i32 }
 7       a i e . u s e _ l o c k (% l o c k _ 2 _ 1 _ 0 , R e l e a s e , 2 )
 8       a i e . n e x t _ b d ^ bb1
 9    ^ bb2 :       / / p r e d : ^ bb3
10       a i e . end
11    ^ bb3 :       / / p r e d : ^ bb5
12       %1 = a i e . d m a _ s t a r t ( MM2S , 0 , ^ bb4 , ^ bb2 )
13    ^ bb4 :       / / 2 p r e d s : ^ bb3 , ^ b b 4
14       a i e . u s e _ l o c k (% l o c k _ 2 _ 1 _ 0 , A c q u i r e G r e a t e r E q u a l , 1 )
15       a i e . dma_bd (% b u f 2 0 : memref <64 x 1 6 x i 3 2 , 1 : i 3 2 > , 0 , 5 1 2 ,
16       [ < s i z e = 6 4 , s t r i d e = 16 > , < s i z e = 8 , s t r i d e = 1 >])
17       { task_id = 0 : i32 }
18       a i e . u s e _ l o c k (% l o c k _ 2 _ 1 , R e l e a s e , 1 )
19       a i e . n e x t _ b d ^ bb4
20    ^ bb5 :       / / p r e d : ^ bb0
21       %2 = a i e . d m a _ s t a r t ( MM2S , 1 , ^ bb6 , ^ bb3 )
22    ^ bb6 :       / / 2 p r e d s : ^ bb5 , ^ b b 6
23       a i e . u s e _ l o c k (% l o c k _ 2 _ 1 _ 0 , A c q u i r e G r e a t e r E q u a l , 1 )
24       a i e . dma_bd (% b u f 2 0 : memref <64 x 1 6 x i 3 2 , 1 : i 3 2 > , 8 , 5 1 2 ,
25       [ < s i z e = 6 4 , s t r i d e = 16 > , < s i z e = 8 , s t r i d e = 1 >])
26       { task_id = 0 : i32 }
27       a i e . u s e _ l o c k (% l o c k _ 2 _ 1 , R e l e a s e , 1 )
28       a i e . n e x t _ b d ^ bb6
29 }


                               Fig. 9. Excerpt of acquire/release nondeterminism.

  This code is nondeterministic: in the typical case, both bb4 and bb6 acquire %lock_2_1_0 once
and execute exactly once. In the case of significant stalling on the hardware implementing bb6,
however, bb4 may acquire the lock and execute twice before bb6 is able to acquire the lock once.
Note that the aie.dma_bd operations in bb4 and bb6 do not implement the same movement due to
22                       Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


different arguments. PEQC-MLIR reports this nondeterminism, analyzing the file in less than 5s
(early exit on first error, otherwise 31s for a corrected, equivalent version). This is a case where
testing alone did not discover the concurrency error, which is unlikely to be triggered except in
unusual scenarios involving significant stalling. The implemented fix [4] uses additional locks to
ensure no two basic blocks can access the same buffer.

6.3   Verification of mlir-opt and polymer-opt
We conducted an extensive evaluation of several tools: mlir-opt from LLVM 19.0.0git; cgeist,
and polygeist-opt and polymer-opt from LLVM 18.0.0git, the latest versions available from [2].
   mlir-opt is the base MLIR compiler provided with LLVM, and offers numerous conversion
and optimization passes, as illustrated below. cgeist takes a C program as input, and raises it to
the affine dialect when possible. polymer-opt is a companion to cgeist, taking affine MLIR
programs as input and calling the Pluto polyhedral optimizer [13] on them, to implement automatic
loop transformations for tiling, fusion, and parallelization. We chose these three tools as they
exhibit different levels of maturity: mlir-opt is a community-maintained LLVM package, cgeist
is a separate project [2] developed by MLIR authors, and Pluto is a research compiler.
   For benchmarks, as we can exercise cgeist and Pluto with only affine programs, we chose Poly-
Bench/C version 4.2.1 [44]. Detailed statistics for these benchmarks are available in the Appendix.
PolyBench/C covers key computation patterns in linear algebra, image processing, and machine
learning.
   We systematically raise the PolyBench C benchmark kernel function to MLIR with cgeist and
then apply polymer-opt and/or mlir-opt optimizations. Every resulting MLIR file is converted
and translated to a PEQC-MLIR-ready input, and verified for equivalence.
   In total, we consider 22 different optimization paths for 30 benchmarks, leading to 580 variants
actually generated. For some cases, the toolchain (mlir-opt and/or polymer-opt) fails to produce
a program. Running the entire set on the PolyBench mini dataset takes less than 30 minutes total
(about 15 min. to generate transformed files with MLIR, and about 10 minutes to convert and check
them for equivalence). As shown below, this still allows PEQC-MLIR to uncover a variety of bugs
and possible misuse of some tools (which are not documented), further justifying the inclusion of
such a fast verification scheme in compiler testing procedures. We also evaluated with the medium
dataset size, obtaining identical bugs/correctness results.
   List of optimizations considered Table 2 displays the various optimization paths we evaluate. They
are not meant to capture all possible optimizations, but rather classical ones that some may wish to
apply especially to dense linear algebra programs: tiling, fusion, unroll-and-jam, parallelization; and,
of course, Pluto-based polyhedral tiling+fusion, as a first transformation before these mlir-opt
optimizations are invoked.
   Verification Results for mlir-opt We now present our results, first on verifying only mlir-opt,
without polymer-opt as a first transformation, in Table 3. That is, mlir-opt is applied on the
original program as extracted by cgeist. This table displays the benchmarks that fail to be proved
equivalent; if no benchmark fails, N/A is displayed.
   We observe numerous errors, which we investigated and confirmed manually. Several of these
errors have in fact also been recently reported with HEC [66]. For example, fusion on imperfectly
nested loops such as correlation, doitgen, etc. is incorrectly implemented: inner/no-outer loops
with non-forward dependences have been fused for these benchmarks. More interestingly, for
Floyd-Warshall any tiling or unroll-and-jam is incorrect: mlir-opt tiled all 3 loops, while the 𝑘 loop
is not tilable as-is on FW. On the other hand, the tiling produced is valid for all other benchmarks
except Seidel-2d (which suffers a similar issue). We particularly note that tiling is correct for other
Practical Formal Verification for MLIR Programs                                                           23


                              Table 2. List of individual optimizations considered.

                  Acronym       command
                  FS            mlir-opt –affine-loop-fusion
                  LICM          mlir-opt –affine-loop-invariant-code-motion
                  NM            mlir-opt –affine-loop-normalize
                  CAN           mlir-opt –canonicalize
                  TL            mlir-opt –affine-loop-tile="tile-size=32"
                  UR            mlir-opt –affine-loop-unroll
                  UAJ           mlir-opt –affine-loop-unroll-jam
                  PAR           mlir-opt –affine-parallelize="max-nested=1"
                  Pluto         polymer-opt -reg2mem -extract-scop-stmt -pluto-opt


Table 3. List of failed benchmarks for mlir-opt without Pluto/polymer-opt optimizations. Note ADI and
durbin are not displayed: the code produced by Cgeist fails to be proved equivalent to the original program,
meaning they fail in all cases.
                    Optimization                         Failing benchmarks
                    FS                                   correlation, covariance, deriche,
                                                         doitgen
                    LICM                                 N/A
                    NM                                   N/A
                    TL                                   floyd-warshall, seidel-2d
                    UR                                   N/A
                    UAJ                                  floyd-warshall
                    PAR                                  N/A
                    NM, CAN, TL, UAJ, TL                 floyd-warshall, seidel-2d
                    NM, CAN, FS, TL                      correlation, covariance, deriche,
                                                         doitgen, floyd-warshall, seidel-2d
                    UR, UAJ, TL, LICM, FS, NM            floyd-warshall, seidel-2d
                    UR, UAJ, TL, PAR, LICM, FS, NM       floyd-warshall, seidel-2d


stencils: for the Jacobi stencils for example only the time loop is strip-mined. But for Seidel-2d, all
3 loops are tiled, without skewing, which is incorrect.
   In practice, a question remains open: are these optimization flags in mlir-opt supposed to detect
correctly whether they can be applied on the input MLIR affine program? Their implementation
suggests such analysis is not implemented, yet there are numerous cases where applying these
optimizations lead to a correctly transformed MLIR program. PEQC-MLIR can help systematically
uncover such potential misuse in a mechanical fashion, by testing systematically e.g. on PolyBench
as we conducted above. However, as shown below, it can also uncover critical bugs in tools that
perform such analysis and transformation selection automatically, like Pluto/Polymer.
   Verification results for Pluto and mlir-opt We now report the same evaluation, but the input
MLIR programs have first been optimized by polymer-opt, invoking the polyhedral Pluto optimizer
with default tile size of 32. Pluto raises the program to polyhedral representation, transforms it, and
regenerates an AST for the fused/tiled/skewed program, itself converted back to MLIR affine by
polymer-opt. Note the mlir-opt optimizations considered operate best on an affine MLIR program
without function calls, so after Pluto but prior to mlir-opt optimizations we systematically invoke
mlir-opt –inline, which can itself sometimes fail. In particular, ADI, ludcmp, nussinov and symm
fail at inlining and are not displayed below.
24                         Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


  Table 4 displays the list of failed benchmarks that involve linear-algebra-style computations.
We observe systematic errors on covariance, lu and gramschmidt in particular: the produced
code performs out-of-bound array accesses. We confirmed the bug by simply displaying the array
locations accessed (a printf) in the C code printed by Pluto during debugging: it does produce
negative indices. We remain unsure of the exact reason of these bugs: the program produced by
cgeist is equivalent to the original program, but Pluto-PolyLib itself seems to generate incorrect
code. This could be due to an incorrect polyhedral representation extracted, or a problem in
polymer-opt. For stencil computations (jacobi-1d, jacobi-2d, heat-3d, fdtd-2d, seidel-2d), we omit
Table 4. List of failed benchmarks for Pluto/polymer-opt followed by mlir-opt optimizations, for the linear
algebra benchmarks (polybench/linear-algebra and polybench/datamining benchmarks). NG indicates the
file was Not Generated by mlir-opt.
     Optimizations                           List of failed benchmarks
     Pluto, FS                               correlation, covariance, gramschmidt, lu,
     Pluto, LICM                             covariance, gramschmidt, lu
     Pluto, NM                               covariance, gramschmidt, lu
     Pluto, TL                               covariance, gramschmidt, lu(NG)
     Pluto, UR                               covariance, gramschmidt, lu
     Pluto, UAJ                              covariance, gramschmidt, lu,
     Pluto, PAR                              covariance, doitgen, gramschmidt, trmm
     Pluto, NM, CAN, TL, UAJ, TL             correlation, covariance, gramschmidt, lu
     Pluto, NM, CAN, FS, TL                  correlation, covariance, gramschmidt, lu
     Pluto, UR, UAJ, TL, LICM, FS, NM        covariance, gramschmidt, lu(NG)
     Pluto, UR, UAJ, TL, PAR, LICM, FS, NM   covariance, doitgen, gramschmidt, lu(NG)

the table which is summarized instead as observing systematic failures for fdtd-2d, jacobi-2d and
seidel-2d. All other stencil benchmarks pass. For these 3 failing stencils, they suffer a similar issue
as above: the code produced after Pluto’s skewing is incorrect, and performs an out-of-bound (-1)
array access along the j dimension, which we confirmed by printing the actual value of the accessed
locations in the program printed by Pluto. We are unsure of the location of this problem, but remark
that we exercise a particular case with the MINI dataset: often the problem size is smaller than the
tile size, and we inline loop bounds while Pluto is designed for parametric loop bounds. We suspect
a possible issue with the ceild/floord implementation in this case, but further investigation is
needed. Note that these benchmarks also fail similarly with larger problem sizes (MEDIUM) which
far exceed the tile sizes.
   We also remark that, of course, not all optimizations led to transforming all programs: mlir-opt
does bypass applying these optimizations in numerous cases (supposedly where they are not
applicable), but still applies them incorrectly in several cases, as reported above.
   Verification throughput experiments We conclude this analysis by displaying in Fig. 10 the through-
put, in number of statements interpreted per second, for all experiments conducted above, distin-
guishing MINI and MEDIUM dataset sizes. For the MINI dataset, times are so low that the time
to analyze the input program (compute symbol tables, normalize) has a measurable effect, but
is marginalized when time is dominated by actual interpretation as in the medium dataset. For
mlir-opt, statements are typically 3-address and therefore faster to interpret, but there are often
10x more statements total to interpret.

6.4     Scaling to Larger Problem Sizes
We conclude our experimental evaluation by briefly outlining ongoing work we are conducting to
improve further scaling to larger problem sizes. Scaling to larger problem sizes is mostly limited
Practical Formal Verification for MLIR Programs                                                                                        25


                                                                           MINI-orig   MINI-mlir-opt   MEDIUM-orig   MEDIUM-mlir-opt
                                                                  800000


                                                                  700000
                    Number of statements interpreted per second



                                                                  600000


                                                                  500000


                                                                  400000


                                                                  300000


                                                                  200000


                                                                  100000


                                                                      0



Fig. 10. Throughput of the verifier: interpretation time only, over 2160 program variants built with mlir-opt.
Equivalence time is negligible vs. interpretation time.

by memory consumption, reaching potentially tens of GB for e.g. a 256x256 triple matrix product
[43]. In practice, the CDAGs are stored explicitly, with one node per operation executed. We are
currently developing techniques to automatically synthesize code which when executed implements
exactly the CDAG: this is a form of (affine) folding from the trace [8, 47]. Although we have only
preliminary results for only sequential program verification, our prototype already demonstrates
very strong potential to increase scaling to larger problem sizes.
   For example, for matrix-products, we remove this memory limitation by automatically folding
CDAGs during their construction into a sort of "chain of recurrence" representation, limiting
memory usage to spatial dimensions (that is typically the size of the input data) but becoming
independent of the reduction size, providing an 𝑂 (𝑁 ) improvement in space complexity for GEMM-
style kernels for example.
   In particular, our preliminary CDAG compaction approach excels for programs with affine
evolution of the computations formed to produce the output values (this even if the actual schedule
of operations implemented is itself non-affine), as is typical in e.g. dense linear algebra and inference
of deep learning models, where sequences of matrix/tensor manipulations and multiplications are
dominant.
   We display in Fig. 11 the scaling achieved to verify two versions (original and optimized variants,
not buggy) of two benchmarks: gemm and 2mm from PolyBench, as they particularly exercise
the need to compress reductions. Visibly, the memory consumption does not grow linearly with
instructions executed (𝑂 (𝑁 3 )) anymore when folding is activated. It leaves time to verification
as the only "limit", and can achieve orders of magnitude reduction in memory usage, as seen on
the green and orange lines, which increase with lower slopes than the base version (𝑂 (𝑁 2 )) using
folding.

7   Related Work
While we are unaware of any other approach with the same coverage as experimented in Sec. 6,
especially with the range of transformations and concurrency/parallelism we support, numerous
prior works target related problems (and may handle some of the simpler benchmarks in our
mlir-opt evaluation), and their coverage may intersect with ours.
  UC-KLEE [45] targets equivalence of programs with complex control-flow, via symbolic execution.
However, it often fails to scale even for somewhat simple cases we support. KLEE [3] was extended
26                                                      Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


                                                        GEMM-fold (time)   GEMM-base (time)           2mm-fold (time)   2mm-base (time)
                                                        GEMM-fold (size)   GEMM-base (size)           2mm-fold (size)   2mm-base (size)
                                          100000                                                                                          100000



                                           10000                                                                                          10000




                                                                                                                                                   Memory consumed (in MB)
             Interpretation time (in s)




                                            1000                                                                                          1000



                                             100                                                                                          100



                                              10                                                                                          10



                                               1                                                                                          1
                                                   32               64               128                        256              512
                                                                                       Problem size
                                             0.1                                                                                          0.1




Fig. 11. Time and maximal memory usage for gemm and 2mm, end-to-end verification. Fold uses affine
folding, base uses normal CDAGs


to support floating-point [35], but does not scale to the problem sizes we target, by orders of
magnitude.
   Another fundamental direction to prove correctness of transformations is translation validation
(TV) [41]. Alive2 provides bounded TV for LLVM [36], and it excels at catching a wide class
of intricate bugs related e.g., to incorrect instructions emitted. However, it is not able to prove
equivalence for the scope of programs we target. Other approaches for TV tend to restrict the scope
of programs and optimizations supported, yet deliver significant bug detection capability, including
for MLIR e.g., [10, 61]. TV has also been deployed for specialized languages like Halide [17], and
for HLS [16, 30]. Recent work presented frameworks to develop verifiable compilers, e.g., [20, 48]
complementing existing certified compilers, e.g. [25, 34, 49].
   Numerous works target problems related to the correctness of MLIR programs, typically by
defining formally the behavior of transformations or at least equivalence between them, e.g.,
[12, 21, 62, 66] which all target the verification of MLIR components, albeit for a different scope
than PEQC-MLIR. In contrast to these techniques, we typically trade off requiring additional
information to limit the program scope (such as the problem size), but broaden significantly the
set of program transformations handled therein. No prior work to our knowledge addresses the
correctness verification of MLIR-AIR and MLIR-AIE toolchains.
   More recently, equality saturation has reached a level of performance allowing impactful transfor-
mations to be modeled [22, 39, 54, 63, 64, 67]; and is deployed for MLIR verification [66]. However,
these techniques are far from covering the rewrites necessary to model the class of transforma-
tions we support, especially regarding concurrency, synchronizations, and parallelization. But
approaches such as egglog may be used to normalize our CDAGs further in lieu of of our rewrite
rule system [68].
   Other approaches to checking or guaranteeing the correctness of (parallel) programs include
model checking e.g., [23, 27, 31, 38, 52, 57], as well as static and dynamic race detection approaches
[7, 24, 53] which often also build a representation of the happens-before relation to detect possible
races [24]. SMT-based techniques such as CIVL [31, 52, 65] have the potential ability to reason on a
wider class of programs (e.g., not requiring fixed problem size), however care must be taken that in
practice, most often strong assumptions are made on the range of some variables (such as fixing the
problem size to one or a few values), limiting otherwise scaling/coverage for complex transformed
programs such as those we support.
Practical Formal Verification for MLIR Programs                                                                           27


   PolyCheck is a static+dynamic analysis approach to prove equivalence between a sequential
affine program and its (possibly non-affine) transformation [11]. It supports arbitrary iteration
reordering transformations, and its space complexity is linear in the data size touched by the
program, not the number of operations performed. In contrast, our framework does not require any
of the programs to be affine, and proves equivalence for concurrent programs. ISA [58] targets the
proof of equivalence between a pair of affine programs, including parametric loop bounds, under a
limited yet powerful set of transformations. However, both remain highly limited overall in code
transformation coverage and rely on polyhedral static analyses [11]. Numerous other approaches
have been developed to prove equivalence e.g. of expression trees or limited forms of programs
[29, 50] however their coverage falls short of supporting the complex programs we target.
   Prior works have reasoned formally about determinism for parallel languages, such as for X10 [33],
Concurrent Collections [14], and Habanero-C with promises [28]. Our formalism in Sec. 3 took
initial inspiration from these works, but we profoundly broadened the scope of concurrency and
synchronization styles (e.g., binary and counting semaphores) that are proved to be deterministic,
and also enable reasoning on symbolic variables.

8   Conclusion
Our proposed approach to correctness verification of a class of MLIR programs was presented,
formalized, and evaluated extensively. It provides formal guarantees of correctness for a highly
useful class of programs. The lowering passes implemented in MLIR and by users would also benefit
from correctness verification. To address this issue and provide verified converters in the long
term, we argue that designers should formalize the semantics of their dialect ideally in terms of
operations from standard dialects, equipped with clear semantics for standard dialects (which itself
still needs to be developed). We hope this paper encourages the community to work on formalizing
the semantics of dialects and their lowering to standard dialects, and leverage PEQC-MLIR’s
formalization for verification we presented in this paper.

References
 [1] [n. d.]. LLVM. http://llvm.org.
 [2] [n. d.]. PolyGeist: C/C++ frontend for MLIR. https://github.com/llvm/Polygeist
 [3] 2023. The KLEE Symbolic Execution Engine. https://klee.github.io
 [4] AMD. [n. d.]. MLIR-AIE. https://github.com/Xilinx/mlir-aie
 [5] AMD. [n. d.]. MLIR-AIR. https://xilinx.github.io/mlir-air/
 [6] AMD. [n. d.]. MLIR-AIR. https://github.com/Xilinx/mlir-air
 [7] Simone Atzeni, Ganesh Gopalakrishnan, Zvonimir Rakamaric, Dong H. Ahn, Ignacio Laguna, Martin Schulz, Gregory L.
     Lee, Joachim Protze, and Matthias S. Müller. 2016. ARCHER: Effectively Spotting Data Races in Large OpenMP
     Applications. In 2016 IEEE International Parallel and Distributed Processing Symposium (IPDPS). 53–62. https://doi.org/
     10.1109/IPDPS.2016.68
 [8] Travis Augustine, Janarthanan Sarma, Louis-Noël Pouchet, and Gabriel Rodríguez. 2019. Generating Piecewise-Regular
     Code from Irregular Structures. In Proceedings of the 40th ACM SIGPLAN Conference on Programming Language Design
     and Implementation, PLDI. Phoenix, AZ, USA, 625–639.
 [9] F. Baader and T. Nipkow. 1998. Term Rewriting and All That. Cambridge University Press.
[10] Seongwon Bang, Seunghyeon Nam, Inwhan Chun, Ho Young Jhoo, and Juneyoung Lee. 2022. Smt-based translation
     validation for machine learning compiler. In International Conference on Computer Aided Verification. Springer, 386–407.
[11] Wenlei Bao, Sriram Krishnamoorthy, Louis-Noël Pouchet, Fabrice Rastello, and P. Sadayappan. 2016. PolyCheck:
     Dynamic Verification of Iteration Space Transformations on Affine Programs. In Proceedings of the 43rd Annual ACM
     SIGPLAN-SIGACT Symposium on Principles of Programming Languages.
[12] Siddharth Bhat, Alex Keizer, Chris Hughes, Andrés Goens, and Tobias Grosser. 2024. Verifying Peephole Rewriting in
     SSA Compiler IRs. LIPIcs, Volume 309, ITP 2024 309 (2024), 9:1–9:20. https://doi.org/10.4230/LIPICS.ITP.2024.9
[13] Uday Bondhugula, Albert Hartono, J. Ramanujam, and P. Sadayappan. 2008. A Practical Automatic Polyhedral Program
     Optimization System. In ACM SIGPLAN Conference on Programming Language Design and Implementation. ACM.
28                            Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


[14] Zoran Budimlic, Michael Burke, Vincent Cavé, Kathleen Knobe, Geoff Lowney, Ryan Newton, Jens Palsberg, David
     Peixotto, Vivek Sarkar, and Frank Schlimbach. 2010. Concurrent Collections. Scientific Programming 18, 3-4 (2010),
     203–217.
[15] Yang Chen, Alex Groce, Chaoqiang Zhang, Weng-Keen Wong, Xiaoli Fern, Eric Eide, and John Regehr. 2013. Tam-
     ing compiler fuzzers. In Proceedings of the 34th ACM SIGPLAN conference on Programming language design and
     implementation. 197–208.
[16] Ramanuj Chouksey and Chandan Karfa. 2020. Verification of Scheduling of Conditional Behaviors in High-Level
     Synthesis. IEEE Transactions on Very Large Scale Integration (VLSI) Systems (2020).
[17] Basile Clément and Albert Cohen. 2022. End-to-end translation validation for the halide language. In OOPSLA
     2022-Conference on Object-Oriented Programming Systems, Languages, and Applications.
[18] Steven Eker. 2003. Associative-Commutative Rewriting on Large Terms. In Rewriting Techniques and Applications,
     Gerhard Goos, Juris Hartmanis, Jan van Leeuwen, and Robert Nieuwenhuis (Eds.). Vol. 2706. Springer Berlin Heidelberg,
     Berlin, Heidelberg, 14–29. https://doi.org/10.1007/3-540-44881-0_3
[19] Venmugil Elango, Fabrice Rastello, Louis-Noël Pouchet, Jagannathan Ramanujam, and Ponnuswamy Sadayappan. 2015.
     On characterizing the data access complexity of programs. In Proceedings of the 42nd Annual ACM SIGPLAN-SIGACT
     Symposium on Principles of Programming Languages.
[20] Schuyler Eldridge, Prithayan Barua, Aliaksei Chapyzhenka, Adam Izraelevitz, Jack Koenig, Chris Lattner, Andrew
     Lenharth, George Leontiev, Fabian Schuiki, Ram Sunder, et al. 2021. MLIR as Hardware Compiler Infrastructure. In
     Workshop on Open-Source EDA Technology (WOSET), Vol. 3.
[21] Mathieu Fehr, Yuyou Fan, Hugo Pompougnac, John Regehr, and Tobias Grosser. 2025. First-Class Verification
     Dialects for MLIR. Proceedings of the ACM on Programming Languages 9, PLDI (June 2025), 1466–1490. https:
     //doi.org/10.1145/3729309
[22] Oliver Flatt and Yihong Zhang. [n. d.]. Egglog In Practice: Automatically Improving Floating-point Error. ([n. d.]).
[23] Pavel Golovin, Michalis Kokologiannakis, and Viktor Vafeiadis. 2025. RELINCHE: Automatically Checking Lineariz-
     ability under Relaxed Memory Consistency. Proceedings of the ACM on Programming Languages 9, POPL (Jan. 2025),
     2090–2117. https://doi.org/10.1145/3704906
[24] Yizi Gu and John Mellor-Crummey. 2018. Dynamic Data Race Detection for OpenMP Programs. In SC18: International
     Conference for High Performance Computing, Networking, Storage and Analysis. IEEE, Dallas, TX, USA, 767–778.
     https://doi.org/10.1109/SC.2018.00064
[25] Yann Herklotz, James D Pollard, Nadesh Ramanathan, and John Wickerson. 2021. Formal verification of high-level
     synthesis. Proceedings of the ACM on Programming Languages 5, OOPSLA (2021), 1–30.
[26] Erika Hunhoff, Joseph Melber, Kristof Denolf, Andra Bisca, Samuel Bayliss, Stephen Neuendorffer, Jeff Fifield, Jack Lo,
     Pranathi Vasireddy, Phil James-Roxby, and Eric Keller. 2025. Efficiency, Expressivity, and Extensibility in a Close-to-
     Metal NPU Programming Interface. In 2025 IEEE 33rd Annual International Symposium on Field-Programmable Custom
     Computing Machines (FCCM). 85–94. https://doi.org/10.1109/FCCM62733.2025.00043
[27] Marie-Christine Jakobs. 2021. PEQCHECK: Localized and Context-aware Checking of Functional Equivalence.
     In 2021 IEEE/ACM 9th International Conference on Formal Methods in Software Engineering (FormaliSE). 130–140.
     https://doi.org/10.1109/FormaliSE52586.2021.00019
[28] Feiyang Jin, Lechen Yu, Tiago Cogumbreiro, Jun Shirako, and Vivek Sarkar. 2023. Dynamic Determinacy Race Detection
     for Task-Parallel Programs with Promises. In 37th European Conference on Object-Oriented Programming (ECOOP 2023).
     Schloss Dagstuhl–Leibniz-Zentrum für Informatik, 13–1.
[29] Chandan Karfa, Kunal Banerjee, Dipankar Sarkar, and Chittaranjan Mandal. 2013. Verification of loop and arithmetic
     transformations of array-intensive behaviors. IEEE Trans. on Computer-Aided Design of Integrated Circuits and Systems
     32, 11 (2013), 1787–1800.
[30] C. Karfa, C. Mandal, D. Sarkar, S.R. Pentakota, and C. Reade. 2006. A formal verification method of scheduling in
     high-level synthesis. In 7th International Symposium on Quality Electronic Design (ISQED’06).
[31] Michalis Kokologiannakis, Azalea Raad, and Viktor Vafeiadis. 2019. Model Checking for Weakly Consistent Libraries.
     In Proceedings of the 40th ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2019).
     Association for Computing Machinery, New York, NY, USA, 96–110. https://doi.org/10.1145/3314221.3314609
[32] Chris Lattner, Mehdi Amini, Uday Bondhugula, Albert Cohen, Andy Davis, Jacques Pienaar, River Riddle, Tatiana
     Shpeisman, Nicolas Vasilache, and Oleksandr Zinenko. 2021. MLIR: Scaling compiler infrastructure for domain specific
     computation. In 2021 IEEE/ACM International Symposium on Code Generation and Optimization (CGO). IEEE, 2–14.
[33] Jonathan K. Lee and Jens Palsberg. 2010. Featherweight X10: A Core Calculus for Async-Finish Parallelism. SIGPLAN
     Not. 45, 5 (Jan. 2010), 25–36. https://doi.org/10.1145/1837853.1693459
[34] Xavier Leroy, Sandrine Blazy, Daniel Kästner, Bernhard Schommer, Markus Pister, and Christian Ferdinand. 2016.
     CompCert-a formally verified optimizing compiler. In ERTS 2016: Embedded Real Time Software and Systems, 8th
     European Congress.
Practical Formal Verification for MLIR Programs                                                                               29


[35] Daniel Liew, Daniel Schemmel, Cristian Cadar, Alastair F Donaldson, Rafael Zahl, and Klaus Wehrle. 2017. Floating-
     point symbolic execution: a case study in n-version programming. In 2017 32nd IEEE/ACM International Conference on
     Automated Software Engineering (ASE). IEEE, 601–612.
[36] Nuno P Lopes, Juneyoung Lee, Chung-Kil Hur, Zhengyang Liu, and John Regehr. 2021. Alive2: bounded translation
     validation for LLVM. In ACM SIGPLAN International Conference on Programming Language Design and Implementation.
[37] Michaël Marcozzi, Qiyi Tang, Alastair F Donaldson, and Cristian Cadar. 2019. Compiler fuzzing: How much does it
     matter? Proceedings of the ACM on Programming Languages 3, OOPSLA (2019), 1–29.
[38] Eric G Mercer, Peter Anderson, Nick Vrvilo, and Vivek Sarkar. 2015. Model Checking Task Parallel Programs Using
     Gradual Permissions (N). In 2015 30th IEEE/ACM International Conference on Automated Software Engineering (ASE).
     IEEE, 535–540.
[39] Jules Merckx, Alexandre Lopoukhine, Samuel Coward, Jianyi Cheng, Bjorn De Sutter, and Tobias Grosser. 2025. Eqsat:
     An Equality Saturation Dialect for Non-destructive Rewriting. arXiv preprint arXiv:2505.09363 (2025). arXiv:2505.09363
[40] MLIR [n. d.]. MLIR: Multi-Level IR in LLVM. https://mlir.llvm.org
[41] George C Necula. 2000. Translation validation for an optimizing compiler. ACM SIGPLAN Notices 35, 5 (2000), 83–94.
[42] Louis-Noel       Pouchet.      [n. d.].                PolyBench/C:         the     Polyhedral       Benchmark        suite.
     http://polybench.sourceforge.net.
[43] Louis-Noël Pouchet, Emily Tucker, Niansong Zhang, Hongzheng Chen, Debjit Pal, Gabriel Rodríguez, and Zhiru
     Zhang. 2024. Formal Verification of Source-to-Source Transformations for HLS. In Proceedings of the 2024 ACM/SIGDA
     International Symposium on Field Programmable Gate Arrays. 97–107.
[44] Louis-Noël Pouchet and Tomofumi Yuki. [n. d.]. PolyBench/C 4.2.1. http://polybench.sourceforge.net
[45] David A Ramos and Dawson Engler. 2015. Under-constrained symbolic execution: Correctness checking for real code.
     In 24th {USENIX} Security Symposium ({USENIX} Security 15).
[46] Alejandro Rico, Satyaprakash Pareek, Javier Cabezas, David Clarke, Baris Ozgul, Francisco Barat, Yao Fu, Stephan
     Munz, Dylan Stuart, Patrick Schlangen, Pedro Duarte, Sneha Date, Indrani Paul, Jian Weng, Sonal Santan, Vinod
     Kathail, Ashish Sirasao, and Juanjo Noguera. 2024. AMD XDNA NPU in Ryzen AI Processors . IEEE Micro 44, 06 (Nov.
     2024), 73–82. https://doi.org/10.1109/MM.2024.3423692
[47] Gabriel Rodríguez, José M Andión, Mahmut T Kandemir, and Juan Touriño. 2016. Trace-based affine reconstruction of
     codes. In Proceedings of the 2016 International Symposium on Code Generation and Optimization. 139–149.
[48] Grigore Ros, u and Traian Florin S, erbănută. 2010. An Overview of the K Semantic Framework. The Journal of Logic and
     Algebraic Programming 79, 6 (2010), 397–434.
[49] Jaroslav Ševčík, Viktor Vafeiadis, Francesco Zappa Nardelli, Suresh Jagannathan, and Peter Sewell. 2013. CompCertTSO:
     A verified compiler for relaxed-memory concurrency. Journal of the ACM (JACM) 60, 3 (2013), 1–50.
[50] KC Shashidhar, Maurice Bruynooghe, Francky Catthoor, and Gerda Janssens. 2005. Verification of Source Code
     Transformations by Program Equivalence Checking. CC (2005).
[51] Stephen F Siegel, Manchun Zheng, Ziqing Luo, Timothy K Zirkel, Andre V Marianiello, John G Edenhofner, Matthew B
     Dwyer, and Michael S Rogers. 2015. CIVL: the concurrency intermediate verification language. In Proceedings of the
     International Conference for High Performance Computing, Networking, Storage and Analysis. 1–12.
[52] Stephen F. Siegel, Manchun Zheng, Ziqing Luo, Timothy K. Zirkel, Andre V. Marianiello, John G. Edenhofner, Matthew B.
     Dwyer, and Michael S. Rogers. 2015. CIVL: The Concurrency Intermediate Verification Language. In Proceedings of the
     International Conference for High Performance Computing, Networking, Storage and Analysis. ACM, Austin Texas, 1–12.
     https://doi.org/10.1145/2807591.2807635
[53] Bradley Swain, Yanze Li, Peiming Liu, Ignacio Laguna, Giorgis Georgakoudis, and Jeff Huang. 2020. OMPRacer: A
     Scalable and Precise Static Race Detector for OpenMP Programs. In SC20: International Conference for High Performance
     Computing, Networking, Storage and Analysis. 1–14. https://doi.org/10.1109/SC41405.2020.00058
[54] Ross Tate, Michael Stepp, Zachary Tatlock, and Sorin Lerner. 2009. Equality saturation: a new approach to optimization.
     In Proceedings of the 36th annual ACM SIGPLAN-SIGACT symposium on Principles of programming languages. 264–276.
[55] Emily Tucker and Louis-Noël Pouchet. [n. d.]. PEQC-MLIR. https://github.com/axolotls73/PEQC-MLIR
[56] Emily Tucker and Louis-Noël Pouchet. 2025. Verification of Concurrent Programs Using Hybrid Concrete-Symbolic
     Interpretation. Principles and Practices of Building Parallel Software: Essays Dedicated to Vivek Sarkar on the Occasion of
     His 64th Birthday 14564 (2025), 90.
[57] Martin Vechev, Eran Yahav, Raghavan Raman, and Vivek Sarkar. 2010. Automatic verification of determinism for
     structured parallel programs. In Static Analysis: 17th International Symposium, SAS 2010, Perpignan, France, September
     14-16, 2010. Proceedings 17. Springer, 455–471.
[58] Sven Verdoolaege, Gerda Janssens, and Maurice Bruynooghe. 2012. Equivalence checking of static affine programs
     using widening to handle recurrences. ACM Trans. on Programming Languages and Systems (TOPLAS) 34, 3 (2012), 11.
[59] Erwei Wang, Samuel Bayliss, Andra Bisca, Zachary Blair, Sangeeta Chowdhary, Kristof Denolf, Jeff Fifield, Brandon
     Freiberger, Erika Hunhoff, Phil James-Roxby, et al. 2025. From Loop Nests to Silicon: Mapping AI Workloads onto
30                            Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


     AMD NPUs with MLIR-AIR. arXiv preprint arXiv:2510.14871 (2025).
[60] Jie Wang, Licheng Guo, and Jason Cong. 2021. AutoSA: A polyhedral compiler for high-performance systolic arrays
     on FPGA. In The 2021 ACM/SIGDA International Symposium on Field-Programmable Gate Arrays.
[61] Yanzhao Wang, Fei Xie, Zhenkun Yang, Pasquale Cocchini, and Jin Yang. 2024. A Systematic Translation Validation
     Framework for MLIR-Based Compilers. (2024).
[62] Yanzhao Wang, Fei Xie, Zhenkun Yang, Pasquale Cocchini, and Jin Yang. 2024. A Systematic Translation Validation
     Framework for MLIR-Based Compilers. International Journal of Software Engineering and Knowledge Engineering (June
     2024), 1–20. https://doi.org/10.1142/S021819402450030X
[63] Yisu Remy Wang, Shana Hutchison, Jonathan Leang, Bill Howe, and Dan Suciu. 2020. SPORES: Sum-Product
     Optimization via Relational Equality Saturation for Large Scale Linear Algebra. Proc. VLDB Endow. 13, 12 (jul 2020),
     1919–1932.
[64] Max Willsey, Chandrakana Nandi, Yisu Remy Wang, Oliver Flatt, Zachary Tatlock, and Pavel Panchekha. 2021. Egg:
     Fast and extensible equality saturation. Proceedings of the ACM on Programming Languages (2021).
[65] Wenhao Wu, Jan Hückelheim, Paul D Hovland, and Stephen F Siegel. 2022. Verifying Fortran Programs with CIVL. In
     International Conference on Tools and Algorithms for the Construction and Analysis of Systems. Springer, 106–124.
[66] Jiaqi Yin, Zhan Song, Nicolas Bohm Agostini, Antonino Tumeo, and Cunxi Yu. 2025. HEC: Equivalence Verification
     Checking for Code Transformation via Equality Saturation. In 2025 USENIX Annual Technical Conference (USENIX ATC
     25). 1181–1196.
[67] Yihong Zhang, Yisu Remy Wang, Oliver Flatt, David Cao, Philip Zucker, Eli Rosenthal, Zachary Tatlock, and Max
     Willsey. 2023. Better together: Unifying datalog and equality saturation. Proceedings of the ACM on Programming
     Languages 7, PLDI (2023), 468–492.
[68] Yihong Zhang, Yisu Remy Wang, Oliver Flatt, David Cao, Philip Zucker, Eli Rosenthal, Zachary Tatlock, and Max
     Willsey. 2023. Better Together: Unifying Datalog and Equality Saturation. Proceedings of the ACM on Programming
     Languages 7, PLDI (June 2023), 468–492. https://doi.org/10.1145/3591239
                             Practical Formal Verification for MLIR Programs                                                                                                                                                                                                                      31


                             A        Appendix
                             A.1             Implementation Details: Debugging Features
                             We briefly outline some debugging features we have implemented, to assist developers in un-
                             derstanding PEQC-MLIR’s errors. When using the verifier to assist the developer during their
                             (semi-)manual program code transformations, we recommend testing with small problem sizes,
                             since the execution time of the interpreter is roughly 0.5M statements interpreted per second. Then,
                             once the program is valid on smaller problem sizes, longer verification can be afforded, on the final
                             problem size.
                                Visualizing CDAG differences A typical error manifests as a mismatch between CDAGs produced:
                             the computations differ. We implement a simple visualizer, based on dotty, for the CDAGs of the
                             mismatched memory location. It embeds the line number in the source program that produced
                             every operation, and color-codes the first mismatched node. We illustrate below with a small
                             excerpt of two trees produced for a stencil benchmark, raised to MLIR. While equivalence succeeds
                             when using A/C normalization, it fails without: on the right the operation is (floatconstant * expr),
                             on the left (expr * floatconstant). Note the tree printed here has hundreds of nodes, we only display
                             its root.
                                                                                                                                                                                                                             mul:16
                                                                                                 mul:126



                                                                                                                                                                                             _past_fp_value_0_200000:0                       add:16
                                                                                 add:125                 _past_fp_value_0_200000:0




                                                                      add:122              B[0][1]:124                                                                                                                             add:16             B[0][1]:16




                             Fig. 12. Excerpt of CDAGs of two variants of the same 5-point stencil program, reordering the LHS and RHS
                             of an operation. Line numbers help tracking the location of instructions which produced the operations,
                             especially when temporary variables are used.


                               Optionally, we can also display the value of any variable marked by the user for debug at the time
                            each operation (node in the cdag) was executed. We automatically compute the surrounding loop                                                                                                                                                                                                    add:49
                        mul:16
                            iterators and track them without user assistance, displaying the iteration at which an operation
                            was executed to ease debugging.                                                                                                                                                                   mul:126                                                                                      A[2][0]:48

           _past_fp_value_0_200000:0                                                                                                                    add:16

                                 Reporting races and deadlocks Another major class of bug relates to incorrect parallelization and/or                       add:125                                               _past_fp_value_0_200000:0                                                                                             a

                            synchronization between programs. This is particularly                                       add:16                    critical when     mul:13    verifying optimizations for
                                                                            add:122                                                                         mul:59                                                                                                       add:135
                            HLS that use blocking FIFOs and dataflow parallelization, such as the systolic array implementation
                                                                                                           add:16                       mul:13            _past_fp_value_0_200000:0         add:13
                            of a matrix-multiply kernel [43].
               add:119                                                       mul:59                                                       add:58                 _past_fp_value_0_200000:0                                    add:132                                    mul:91                                          add:74
                                 In the case that the interpreter detects a race condition, the memory location (e.g. temp[0][42])
                  mul:75
                            is displayed, as well as theadd:16
                                                             add:58
                                                                                 line number mul:13
                                                                                   _past_fp_value_0_200000:0
                                                                                                            and thread        _past_fp_value_0_200000:0
                                                                                                                                     id of the instructions
                                                                                                                                add:55             A[0][1]:57
                                                                                                                                                                   add:13
                                                                                                                                                                                  mul:75
                                                                                                                                                                                            add:13
                                                                                                                                                                                 that accessed      A[0][2]:13
                                                                                                                                                                                                   that     location          mul:59                       add:90             _past_fp_value_0_200000:0                      add:71

                            in a possible race. The source code of each thread involved in producing the race is then displayed.
                                                     mul:13                    mul:13            _past_fp_value_0_200000:0              add:13                  add:13        A[2][2]:13    add:13  A[2][2]:13
  add:74                    Optionally, the list of threads that executed and terminated before the race can be displayed.
                      _past_fp_value_0_200000:0                add:55              A[2][1]:54             add:52            A[2][1]:54             add:74              _past_fp_value_0_200000:0                  add:58                _past_fp_value_0_200000:0                  add:87               A[1][3]:67           add:68



13
                                 Our reporting
                  _past_fp_value_0_200000:0           add:13
                                                                 for _past_fp_value_0_200000:0
                                                                       deadlocks, however,                 add:13
                                                                                                                     remainsadd:13
                                                                                                                                          quite
                                                                                                                                            A[1][3]:13
                                                                                                                                                       basic.       We list
                                                                                                                                                               add:13
                                                                                                                                                                                     all threads
                                                                                                                                                                              A[4][2]:13    add:13
                                                                                                                                                                                                   that     are still
                                                                                                                                                                                                    A[1][3]:13                mul:13
  add:71            A[1][2]:51                     add:52             A[4][1]:54                 add:49            A[1][2]:51                add:71              A[1][2]:51                              add:55               A[1][1]:46                       add:84             A[3][3]:86               add:65            A[3][3]:86
                            active but cannot make further progress, along with their source code. We also report which
3][3]:13
       A[3][2]:70
                            semaphore/FIFO add:13
                                      add:49
                                                                 causes a deadlock
                                                         A[1][2]:13
                                                         A[3][2]:70
                                                                                        add:13
                                                                                       A[1][1]:46
                                                                                                      (there
                                                                                                        A[1][1]:13 may
                                                                                                               A[1][0]:48
                                                                                                                                be more
                                                                                                                           add:13          A[3][3]:13than add:13
                                                                                                                                          add:68
                                                                                                                                                              one — A[3][3]:13
                                                                                                                                                              A[3][2]:70
                                                                                                                                                                             we only A[1][2]:13
                                                                                                                                                                                           report theA[1][1]:13
                                                                                                                                                                                                           first one_past_fp_value_0_200000:0
                                                                                                                                                                                                      add:52               A[3][1]:54                 add:81            A[2][4]:102              A[3][2]:70               A[3][1]:54
                            blocking further progress). Any violation of the rules for deterministic concurrency presented
2][4]:13
[3]:86                      in Sec.
                     A[3][1]:54     add:13 3 (e.g.,       multiple add:13
                                                  A[3][2]:13
                                          A[3][0]:48                       concurrent    A[3][1]:13 acquires)      add:13 are A[2][4]:13
                                                                                                                                   reported also.
                                                                                                                                 add:65                 A[3][2]:13 Our A[3][1]:13
                                                                                                                                                    A[2][3]:86              debugging mode essentially
                                                                                                                                                                                             add:49            A[2][2]:70                add: A[2][3]:86            A[2][2]:70

                            displays the trace of all events involving semaphores (initialization, wait/set/acquire/release),
13                      add:13         A[2][3]:13               add:13                                                 A[2][2]:70             A[2][1]:54                   A[2][1]:54         A[2][0]:48
                            whether            they clear           or areA[2][2]:13
                                                                               blocked, andA[2][3]:13      whetherA[2][2]:13   a context-switch is needed. In our experience, this add:13                                                 A[3




     A[2][2]:13              A[2][1]:13                A[2][1]:13               A[2][0]:13                                                                                                                                                                                                     add:13                A[2][2]:13




                                                                                                                                                                                                                                                                             A[2][1]:13                  A[2][0]:13
32                              Emily Tucker, Louis-Noël Pouchet, Erika Hunhoff, Stephen Neuendorffer, and Erwei Wang


exhaustive trace enables the user to quickly locate culprits in case of synchronization bugs, but
is best manipulated for small programs for easier debugging. Future work includes developing a
recording of the synchronization operations executed by threads over the program lifetime, and
displaying a forest of threads as nodes and their connections via semaphores/FIFOs instead of
simply the trace.

A.2    Per-benchmark Evaluation Metrics
   Basic statistics on benchmarks We display details on the benchmarks evaluated. Table 5 displays
the list of all benchmarks considered, as well as some statistics on the number of statements
interpreted, number of nodes in the CDAGs produced, memory use and time to interpret the
original programs, for both the MINI and MEDIUM dataset sizes of PolyBench/C. Interpretation
time of transformed variants follows similar trends. However, often more statements are produced
via transformations, so statement count and interpretation time increases accordingly, sometimes
by up to 3x.

Table 5. List of all 30 PolyBench/C benchmarks, and statistics on interpreting the original input benchmarks
(number of statements interpreted, number of CDAG nodes eventually created, time and space to interpret)
for both the MINI and MEDIUM datasets
 benchmark        description                                  #stmts          #cdag nodes      Mem. used (B)      Time (s)
                                                          MINI     MED      MINI      MED      MINI     MED     MIN MED
 2mm              2 Matrix Mult. (𝛼𝐴𝐵𝐶 + 𝛽𝐷 )             43.2k    44.5M    102.4k 110.2M      6.15M    6.48G   0.14    139
 3mm              3 Matrix Mult. ( (𝐴𝐵) (𝐶𝐷 ) )           70.2k    68.9M    134.9k 137M        8.12M    8.08G   0.23    209
 adi              Alternating Direction Implicit solver   98.1k    55.2M    717.1k 431M        42.1M    25.3G   0.54    298
 atax             Matrix transpose and vector mult.       9993     963.4k   22.5k     2.24M    1.45M    143M    0.03    2.81
 bicg             BiCG sub-kernel of BiCGStab solver      6736     642.8k   22.5k     2.24M    1.45M    143M    0.02    2.30
 cholesky         Cholesky decomposition                  36.2k    32.4M    69.6k     64.6M    4.21M    3.80G   0.12    107
 correlation      Correlation computation                 48.2k    23.2M    101.2k 46.7M       6.07M    2.75G   0.16    70.1
 covariance       Covariance computation                  47.6k    23.1M    90.7k     46.0M    5.45M    2.71G   0.14    70.3
 deriche          Edge detection filter                   133.5k 11.1M      401.5k 33.9M       24.8M    2.09G   0.35    26.8
 doitgen          Multi-res. analysis kernel (MADNESS)    42.8k    22.6M    70.4k     43.3M    4.22M    2.55G   0.12    67.4
 durbin           Toeplitz system solver                  7509     22.6M    10.1k     965.2k   604.5k 56.7M     0.02    1.68
 fdtd-2d          2-D Dinite Diff. Time Domain kernel     108.7k 43.2M      377.5k 157M        22.3M    9.27G   0.45    178
 floyd-warshall   Graph shortest path length              662.7k 17.6M      2.81M     75.8M    164M     4.44G   3.12    83.7
 gemm             Matrix-multiply (𝐶 = 𝛼𝐴𝐵 + 𝛽𝐶 )         49.1k    32.0M    139.7k 95.4M       8.34M    5.61G   0.16    104
 gemver           Vector mult. and matrix add.            15.0k    1.45M    55.2k     5.4M     3.39M    332M    0.05    4.86
 gesummv          Scalar, vector and matrix mult.         3839     251.8k   14.8k     1.00M    1.01M    68.2M   0.01    1.07
 gramschmidt      Gram-Schmidt decomposition              59.2k    34.9M    115.3k 69.7M       6.93M    4.10G   0.18    106
 heat-3d          Heat equation over 3D data domain       73.1k    34.1M    925.2k 494M        54.4M    28.9G   0.84    413
 jacobi-1d        1-D Jacobi stencil computation          3497     239.4k   10.2k     718.0k   604.4k 42.2M     0.01    0.76
 jacobi-2d        2-D Jacobi stencil computation          98.7k    37.1M    473.9k 184M        27.9M    10.8G   0.53    202
 lu               LU decomposition                        69.1k    64.5M    131.8k 128M        7.86M    7.55G   0.24    212
 ludcmp           LU decomposition + Forward Subst.       76.6k    1.83M    141.7k 3.58M       8.45M    211M    0.22    5.02
 mvt              Matrix Vector product and Transpose     9945     963.2k   22.6k     2.24M    1.46M    143M    0.03    2.74
 nussinov         Dyn. programming for seq. alignment     122.4k 3.05M      522.0k 1.00M       30.8M    1.17G   0.66    35.8
 seidel-2d        2-D seidel stencil computation          89.8k    47.7M    785.8k 428M        46.2M    25.1G   0.83    451
 symm             Symmetric matrix-mult.                  26.5k    19.4M    98.5k     72.7M    5.90M    4.27G   0.10    73.9
 syr2k            Symmetric rank-2k update                31.9k    17.6M    171.7k 104M        10.2M    6.14G   0.16    88.2
 syrk             Symmetric rank-k update                 31.9k    17.6M    86.8k     52.3M    5.21M    3.07G   0.11    59.9
 trisolv          Triangular solver                       2597     241.8k   6637      642.4k   520.2k 50.1M     0.01    0.79
 trmm             Triangular matrix-mult.                 20.2k    14.6M    36.9k     28.9M    2.25M    1.70G   0.07    44.3
