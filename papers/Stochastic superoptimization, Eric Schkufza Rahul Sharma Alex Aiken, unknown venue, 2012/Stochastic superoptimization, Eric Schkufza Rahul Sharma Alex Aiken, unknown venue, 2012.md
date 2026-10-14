                                                                                 Stochastic Superoptimization

                                                              Eric Schkufza                                    Rahul Sharma                                 Alex Aiken
                                                            Stanford University                               Stanford University                       Stanford University
                                                               Stanford, CA                                      Stanford, CA                              Stanford, CA
                                                   eschkufz@cs.stanford.edu sharmar@cs.stanford.edu                                                aiken@cs.stanford.edu



                                       ABSTRACT                                                                                 generating consistently good code, leads to the well-known
                                                                                                                                phase ordering problem. In many cases, the best possible
arXiv:1211.0557v1 [cs.PF] 2 Nov 2012




                                       We formulate the loop-free, binary superoptimization task
                                       as a stochastic search problem. The competing constraints                                code can only be obtained through the simultaneous consid-
                                       of transformation correctness and performance improvement                                eration of mutually dependent issues such as instruction se-
                                       are encoded as terms in a cost function, and a Markov Chain                              lection, register allocation, and target-dependent optimiza-
                                       Monte Carlo sampler is used to rapidly explore the space of                              tion.
                                       all possible programs to find one that is an optimization of a                              Previous approaches to this problem have focused on the
                                       given target program. Although our method sacrifices com-                                exploration of all possibilities within some limited class of
                                       pleteness, the scope of programs we are able to reason about,                            programs. In contrast to a traditional compiler, which uses
                                       and the quality of the programs we produce, far exceed those                             performance constraints to drive code generation of a single
                                       of existing superoptimizers. Beginning from binaries com-                                program, these systems consider multiple programs and then
                                       piled by llvm -O0 for 64-bit X86, our prototype implemen-                                ask how well they satisfy those constraints. Solutions range
                                       tation, STOKE, is able to produce programs which either                                  from the explicit enumeration of a class of programs that
                                       match or outperform the code sequences produced by gcc                                   can be formed using a large executable hardware instruction
                                       with full optimizations enabled, and, in some cases, expert                              set [3] to implicit enumeration through symbolic theorem
                                       handwritten assembly.                                                                    proving techniques of programs over some restricted register
                                                                                                                                transaction language [14, 11, 9].
                                                                                                                                   An attractive feature of these systems is completeness: If
                                       Categories and Subject Descriptors                                                       a program exists meeting the desired constraints, that pro-
                                       H.4 [Information Systems Applications]: Miscellaneous;                                   gram will be found. Unfortunately, completeness also places
                                       D.2.8 [Software Engineering]: Metrics—complexity mea-                                    limitations on the space of programs that can be effectively
                                       sures, performance measures                                                              reasoned about. Because of the huge number of programs in-
                                                                                                                                volved explicit enumeration-based techniques are limited to
                                       General Terms                                                                            programs up to some fixed length, and currently this bound
                                                                                                                                is well below the threshold at which many interesting opti-
                                       Compilation and Optimization, Code Generation and Syn-
                                                                                                                                mizations take place. Implicit enumeration techniques can
                                       thesis, Machine Learning Applied to Compilation
                                                                                                                                overcome this limitation, but at the cost of expert-written
                                                                                                                                rules for shrinking the search space. The resulting optimiza-
                                       Keywords                                                                                 tions are as good, but no better, than the quality of the rules
                                       X86, Superoptimizer, Binary, Validation, MCMC, Markov                                    written by an expert.
                                       Chain Monte Carlo, Stochastic Search                                                        To overcome these limitations we take a different approach
                                                                                                                                based on incomplete search. We show how the competing re-
                                       1.     INTRODUCTION                                                                      quirements of correctness and speed can be defined as terms
                                                                                                                                in a cost function over the complex search space of all loop-
                                         For many application domains there is considerable value
                                                                                                                                free executable hardware instruction sequences, and how the
                                       in producing the most performant code possible. Unfortu-
                                                                                                                                program optimization problem can be formulated as a cost
                                       nately, the traditional structure of a compiler’s optimization
                                                                                                                                minimization problem. Although the resulting search space
                                       phase is often ill-suited to this task. Attempting to factor
                                                                                                                                is highly irregular and not amenable to exact optimization
                                       the optimization problem into a collection of small subprob-
                                                                                                                                techniques, we demonstrate that the common approach of
                                       lems that can be solved independently, although suitable for
                                                                                                                                employing a Markov Chain Monte Carlo (MCMC) sampler
                                                                                                                                to explore the function and produce low-cost samples is suf-
                                                                                                                                ficient for producing high quality code sequences.
                                       Permission to make digital or hard copies of all or part of this work for                   Although our technique sacrifices completeness by trading
                                       personal or classroom use is granted without fee provided that copies are                systematic enumeration for stochastic search, we show that
                                       not made or distributed for profit or commercial advantage and that copies               we are able to dramatically increase the space of programs
                                       bear this notice and the full citation on the first page. To copy otherwise, to          that our system can reason while simultaneously improv-
                                       republish, to post on servers or to redistribute to lists, requires prior specific
                                       permission and/or a fee.
                                                                                                                                ing the quality of the code produced. Consider the exam-
                                       ASPLOS ’13 Houston, Texas USA                                                            ple code shown in Figure 1, the Montgomery multiplication
                                       Copyright 20XX ACM X-XXXXX-XX-X/XX/XX ...$15.00.


                                                                                                                            1
# rsi=np, ecx=mh, edx=ml, rdi=c0, r8=c1                             previous work in superoptimization and discusses its limi-
# c1 : c0 := np * mh:ml + c1 + c0                                   tations. Section 3 presents a mathematical formalism for
                                                                    transforming the program optimization task into a stochas-
.set c0 0xffffffff                                                  tic cost minimization problem. Section 4 discusses how that
.set c1 0x100000000                                                 theory is applied in a system for optimizing the runtime per-
                                                                    formance of 64-bit X86 binaries, and Section 5 describes our
                                                                    prototype implementation, STOKE. Finally, Section 6 eval-
.L0                             .L0                                 uates STOKE on a set of benchmarks drawn from cryptog-
  movq    rsi,       r9           shlq     32,      rcx             raphy, linear algebra, and low-level programming, and shows
  mov     ecx,       ecx          mov      edx,     edx             that STOKE is able to produce code that either matches or
  shrq    32,        rsi          xorq     rdx,     rcx             outperforms the code produced by production compilers.
  andl    c1,        r9d          movq     rcx,     rax
  movq    rcx,       rax          mulq     rsi                      2.   RELATED WORK
  mov     edx,       edx          addq     r8,      rdi                Previous approaches to superoptimization have focused
  imulq   r9,        rax          adcq     0,       rdx             on the exploration of all possibilities within some restricted
  imulq   rdx,       r9           addq     rdi,     rax             class of programs. Although these systems have been demon-
  imulq   rsi,       rdx          adcq     0,       rdx             strated to be quite effective within certain domains, their
  imulq   rsi,       rcx          movq     rdx,     r8              general applicability has remained limited. We discuss these
  addq    rdx,       rax          movq     rax,     rdi             limitations in the context of the Montgomery multiplication
  jae     .L2                                                       kernel shown in Figure 1.
  movabsq c1,        rdx                                               The high-level organization of the code is as follows: Two
  addq    rdx,       rcx                                            32-bit values, ecx and edx, are concatenated and then mul-
.L2                                                                 tiplied by the 64-bit rsi to produce a 128-bit value. Two
  movq    rax,       rsi                                            64-bit values, rdi and r8 are added to that product, and the
  movq    rax,       rdx                                            result is written to two registers: the upper half to r8, and
  shrq    32,        rsi                                            the lower half to rdi. The primary source of optimization is
  salq    32,        rdx                                            best demonstrated by comparison. The code produced by
  addq    rsi,       rcx                                            gcc -O3, Figure 1(left), performs the 128-bit multiplication
  addq    r9,        rdx                                            as four 64-bit multiplications and then combines the results;
  adcq    0,         rcx                                            the rewrite produced by STOKE, Figure 1(right), uses a
  addq    r8,        rdx                                            hardware intrinsic to perform the multiplication in a single
  adcq    0,         rcx                                            step.
  addq    rdi,       rdx                                               Massalin’s original paper on superoptimization [14] de-
  adcq    0,         rcx                                            scribes a system that explicitly enumerates sequences of code
  movq    rcx,       r8                                             of increasing length and selects the first such code identical
  movq    rdx,       rdi                                            to the input program on a set of testcases. Massalin re-
                                                                    ported being able to optimize instruction sequences of up to
Figure 1: Montgomery multiplication kernel from                     length 12, however to do so, it was necessary to restrict the
the OpenSSL big number library, compiled by gcc                     set of enumerable opcodes to between 10 and 15. The 11
-O3 (left) and STOKE (right). The STOKE code is                     instruction kernel produced by STOKE in Figure 1 is found
16 lines shorter, 1.6x faster, and slightly faster than             by considering a large subset of the nearly 400 64-bit X86
expert handwritten assembly.                                        opcodes, some of which have as many as 10 variations. It is
                                                                    unlikely that Massalin’s approach would scale to an instruc-
                                                                    tion set of this magnitude.
kernel from the OpenSSL big number library for arbitrary               Denali [11], and the more recent Equality Saturation tech-
precision integer arithmetic. Beginning with a binary com-          nique [18], attempt to gain scalability by only considering
piled by llvm -O0 (116 lines, not shown), we are able to            programs that are known to be equal to the input program.
produce a program which is 16 lines shorter and 1.6 times           Candidate programs are explored through successive appli-
faster than the code produced by gcc with full optimizations        cation of equality preserving transformation axioms. Be-
enabled. Most interestingly, the code that our method finds         cause it is goal-directed this approach dramatically improves
uses a different assembly level algorithm than the original,        both the number of primitive instructions and the length of
and is slightly better than the expert handwritten assem-           programs that can be considered, but it also relies heavily
bly code included with the OpenSSL repository. The code             on expert knowledge. It is unclear whether an expert would
is discovered automatically, and is automatically verified to       know a priori to encode an equality axiom defining the mul-
be equivalent to the original llvm -O0 code. To the best of         tiplication transformation discovered by STOKE. More gen-
our knowledge, the code is truly optimal: it is the fastest         erally, it is unlikely that a set of expert written rules would
program for this function written in the 64-bit X86 instruc-        ever cover the set of all interesting optimizations. It is worth
tion set (the strange looking mov edx, edx produces the             noting that these techniques can to a certain extent deal with
non-obvious but necessary side effect of zeroing the upper          loop optimizations, while other techniques, including ours,
32 bits of rdx).                                                    are limited to loop-free code.
   To summarize, our work makes a number of contributions              Bansal [3] describes a system that automatically enumer-
that have not previously been demonstrated. The remainder           ates 32-bit X86 superoptimizations and stores the results
of this paper explores each in turn. Section 2 summarizes           in a database for later use. By exploiting symmetries be-


                                                                2
tween programs that are equivalent up to register renaming,                                       (
Bansal was able to scale this method to optimizations tak-                                         1   φ = true
ing input code sequences of at most length 6 and producing                               1{φ} =                                  (1)
                                                                                                   0   φ = false
code sequences of at most length 3. This approach has the
dual benefit of hiding the high cost of superoptimization by
performing a search once and for all offline and eliminat-
                                                                      3.1    Cost Function
ing the dependence on expert knowledge. To some extent,                 Although we have considerable freedom in defining a cost
the low cost of performing a database query allows the sys-           function, at the highest level, it should include two terms
tem to overcome the low upper bound on instruction length             with the following properties:
through the repeated application of the optimizer along a
sliding code window. However, the Montgomery multipli-                              c(R; T ) = eq(R; T ) + perf(R; T )           (2)
cation kernel has the interesting property shared by many
real world codes that no sequence of short superoptimiza-                                    eq(R; T) = 0
                                                                                                                                 (3)
                                                                                                                
tions will transform the code produced by gcc -O3 into the                             R = arg minr perf(r; T )
code produced by STOKE. We follow Bansal’s approach in
                                                                         eq(·) is a correctness metric, measuring the similarity of
overall system architecture, using testcases to help classify
                                                                      two functions. The metric is zero if and only if the two
programs as promising or not and eventually submitting the
                                                                      functions are equal. For our purposes, two code sequences
most promising candidates to a verification engine to prove
                                                                      are regarded as functions of registers and memory contents,
or refute their correctness.
                                                                      and are are equal if for all machine states that agree on
   More recently both Sketching [17] and Brahma [9] have
                                                                      the live inputs with the respect to the target, the two codes
made progress in addressing the closely related component-
                                                                      produce identical side effects on the live outputs with respect
based program synthesis problem. These systems rely on
                                                                      to the target. Because program optimization is undefined for
either a declarative program specification, or a user-specified
                                                                      ill-formed programs, it is unnecessary that eq(·) be defined
partial program, and operate on statements in bit-vector
                                                                      for a target or rewrite producing some undefined behavior.
calculi rather than directly on hardware instructions. Liang
                                                                      However nothing prevents us from doing so, and it would be
[13] considers the task of learning programs from testcases
                                                                      a straightforward extension to produce a definition of eq(·)
alone, but at a similarly high level of abstraction. Although
                                                                      which preserved hardware exception behavior as well.
useful for synthesizing results, the internal representations
                                                                         perf(·) quantifies the performance improvement of a rewrite
used by these system preclude them from reasoning directly
                                                                      with respect to the target. Depending on the application,
about the runtime performance of the resulting code.
                                                                      this term could reflect code size, expected runtime, number
   STOKE differs from previous approaches to superopti-
                                                                      of disk accesses, power consumption, or any other measure of
mization by relying on incomplete stochastic search. In do-
                                                                      resource usage. Crucially, the extent to which this term ac-
ing so, it makes heavy use of Markov Chain Monte Carlo
                                                                      curately reflects the performance improvement of a rewrite
(MCMC) sampling to explore the extremely high dimen-
                                                                      directly affects the quality of the results discovered by a
sional, irregular search space of loop-free assembly programs.
                                                                      search procedure.
For many optimization problems of this form, MCMC sam-
pling is the only known general solution method which is              3.2    MCMC Sampling
also tractable. Successful applications are many, and in-                In general, we expect cost functions of the form described
clude protein alignment [16], code breaking [7], and scene            above to be highly irregular and not amenable to exact opti-
modeling and rendering in computer graphics [19, 6].                  mization techniques. The common approach to solving this
                                                                      problem is to employ the use of an MCMC sampler. Al-
3.   COST MINIMIZATION                                                though a complete discussion of MCMC is beyond the scope
   To cast program optimization as a cost minimization prob-          of this paper, we summarize the main ideas here.
lem, it is necessary to define a cost function with terms                MCMC is a technique for sampling from a probability
that balance the hard constraint of correctness preservation          density function in direct proportion to its value. That is,
and the soft constraint of performance improvement. The               regions of higher probability are sampled more often than
primary advantage of this approach is that it removes the             regions of low probability. When applied to cost minimiza-
burden of reasoning directly about the mutually-dependent             tion, it has the attractive property that in the limit the most
optimization issues faced by a traditional compiler. For in-          samples will be taken from the minimum (optimal) value of
stance, rather than consider the interaction between register         the function. In practice, well before this limit behavior is
allocation and instruction selection, we might simply define          observed, MCMC functions as an intelligent hill climbing
a term to encode the primary consequence: expected run-               method which is robust against irregular functions that are
time. Having done so, we may then utilize a cost minimiza-            dense with local minima. A common method (described by
tion search procedure to discover a program that balances             [1]) for transforming an arbitrary cost function, c(·), into a
those issues as effectively as possible. We simply run the            probability density function is the following, where β is a
procedure for as long as we like, and select the lowest-cost          constant and Z is a partition function that normalizes the
result which has satisfied all of the hard constraints.               distribution:
   In formalizing this idea, we make use of the following no-
tation. We refer to the input program as the target (T )                                       1                   
                                                                                   p(R; T ) =    exp − β · c(R; T )            (4)
and a candidate compilation as a rewrite (R), we say that                                     Z
a function f (X; Y ) takes inputs X and is parameterized by              Although computing Z is in general intractable, the Metro-
Y , and finally, we define the indicator function for boolean         polis-Hastings algorithm for generating Markov chains is de-
variables:                                                            signed to explore density functions such as p(·) without the


                                                                  3
need to compute the partition function [15, 10]. The basic                                      20                                                                  8
idea is simple. The algorithm maintains a current rewrite




                                                                                                                                     Testcases / second (x10,000)
R and proposes a modified rewrite R∗ as the next step in                                        15                                                                  6




                                                                         Validations / second
the chain. The proposal R∗ is either accepted or rejected.
If the proposal is accepted, R∗ becomes the current rewrite,
                                                                                                10                                                                  4
otherwise another proposal based on R is generated. The al-
gorithm iterates until its computational budget is exhausted,
and so long as the proposals are ergodic (capable of trans-                                      5                                                                  2
forming any point in the space to any other through some se-
quence of steps) the algorithm will in the limit produce a se-                                   0                                                                  0
quence of samples with the properties described above (i.e.,                                         < 10 30   50   70   90 > 90                                        < 20 25   30   35   40 > 40
in proportion to their cost). This global property depends
on the local acceptance criteria of a proposal R → R∗ , which            Figure 2: Histograms of validations per second
is governed by the Metropolis-Hastings acceptance probabil-              (left), and testcase evaluations per second (right),
ity, where q(R∗ |R) is the proposal distribution from which              for the benchmarks discussed in Section 6, The low
a new rewrite R∗ is sampled given the current rewrite, R:                validation throughput is insufficient for MCMC.
                                                          !
                  ∗            p(R∗ ; T )q(R|R∗ )
        α(R → R ; T ) = min 1,                                 (5)          Unfortunately, despite advances in the technology, the to-
                               p(R; T )q(R∗ |R)                          tal number of validations that can be performed per second,
   This proposal distribution is key to a successful applica-            even for modestly sized codes, is low. Figure 2 (left) suggests
tion of the algorithm. Empirically, the best results are ob-             that for the benchmarks discussed in Section 6 the number
tained by a distribution which makes both local proposals                is well below 100. Because MCMC is effective only insofar as
that make minor modifications to R and global proposals                  it is able to explore sufficiently large numbers of proposals,
that induce major changes. In the event that the proposal                the repeated computation of Equation 7 in its inner-most
distributions are symmetric, q(R∗ |R) = q(R|R∗ ), the ac-                loop would almost certainly drive that number well below a
ceptance probability can be reduced to the much simpler                  useful threshold.
Metropolis ratio, which can be computed directly from c(·):                 This observation motivates the definition of an approxi-
                                                                         mation to eq(·) based on testcases, τ . Intuitively, we run the
                                         !                               proposal R∗ on a set of inputs and measure “how close” the
              ∗             p(R∗ ; T )                                   output is to the output of the target on those same inputs.
     α(R → R ; T ) = min 1,
                            p(R; T )                                     For a given input, we use the number of bits difference in
                                                          !!   (6)       live outputs (i.e., the Hamming distance) to measure cor-
                                             c(R∗ ; T )                  rectness. Besides being much faster than using a theorem
                      = min 1, exp   −β·
                                              c(R; T )                   prover, this approximation of program equivalence has the
                                                                         added advantage of producing a smoother landscape than
  The important properties of the acceptance criteria are                the 0/1 output of a symbolic equality test—it provides a
the following: If R∗ is better (has a higher probability/lower           useful notion of “almost correct” that can help guide the
cost) than R, the proposal is always accepted. If R∗ is worse            search.
(has a lower probability/higher cost) than R, the proposal
may still be accepted with a probability that decreases as a                                                             X
function of the ratio in value between R∗ and R. This is the                                         eq0 (R; T , τ ) =         reg(R; T , t) + mem(R; T , t)
property that prevents the search from becoming trapped in                                                               t∈τ
                                                                                                                                                                                                 (8)
local minima while remaining less likely to accept a move
                                                                                                                         X
                                                                                                                     +         err(R; T , t)
that is much worse than available alternatives.                                                                          t∈τ

                                                                            reg(·) compares the side effects, val(·), that both functions
4.    X86 BINARY OPTIMIZATION                                            produce on live register outputs, ρ, with respect to the tar-
   Having discussed program optimization as cost minimiza-               get, and counts the number of bits that the results differ by.
tion in the abstract, we turn to the practical details of imple-         These outputs can include general purpose, SSE, and condi-
menting cost minimization for optimizing the runtime per-                tion registers. mem(·) is defined analogously for live memory
formance of 64-bit X86 binaries. As 64-bit X86 is one of                 outputs, µ. We use the population count function, POP(·),
the most complex ISAs in production, we expect that the                  to count the number of 1-bits in the 64-bit representation of
discussion in this section should generalize well to other ar-           an integer.
chitectures.
                                                                                                                                                         
4.1     Transformation Correctness
                                                                                                                         X
                                                                                                     reg(R; T , t) =           POP val(T , r) ⊕ val(R, r)                                        (9)
   For loop-free sequences of X86 assembly code, a natural                                                               r∈ρ
choice for implementing the transformation correctness term                                                          X                               
is a symbolic validator such as the one used in [5]. For a                                      mem(R; T , t) =            POP val(T , m) ⊕ val(R, m)                                           (10)
candidate rewrite, the term may be defined in terms of an                                                            m∈µ
invocation of the validator as:
                                                                            err(·) is used to distinguish programs which exhibit unde-
                                                                       fined behavior, by counting and then penalizing the number
          eq(R; T ) = 1 − 1{VALIDATE(T , R)}                   (7)       of segfaults, sigsegv(·), floating point exceptions, sigfloat(·),


                                                                     4
                      20                                                                         rewrite code and compare their runtimes. Unfortunately, as
                      18
                                                                                                 with the transformation correctness term, the amount of
                      16
                                                                                                 time required to both compile a function and execute it suf-
Actual Runtime (ns)



                      14
                      12                                                                         ficiently many times to eliminate transient performance ef-
                      10                                                                         fects is prohibitively expensive to be used in MCMC’s inner-
                       8                                                                         most loop. For this paper, we adopt a simple heuristic for
                       6
                                                                                                 approximating the runtime performance of a function, which
                       4
                       2                                                                         is based on a static approximation of the average latency of
                       0                                                                         its instructions.
                           0    10       20           30        40          50   60    70
                                             Predicted Runtime (unitless)                                    perf(R; T ) = H(T ) − H(R)
                                                                                                                                                          (13)
                                                                                                                            X
Figure 3: Comparison of predicted and actual run-                                                                 H(f ) =         LATENCY(i)
times for the benchmarks described in Section 6,                                                                           i∈inst(f )

along with rewrites generated while writing this                                                    Figure 3 shows a high correlation between the heuristic
paper. The points are well correlated but distin-                                                and the actual runtimes of the benchmarks described in
guished by outliers corresponding to codes with high                                             Section 6, along with rewrites for those benchmarks which
instruction level parallelism at the micro-op level.                                             were generated in the process of writing this paper. Out-
The approximation is sufficient for the benchmarks                                               liers correspond to rewrites with a disproportionately high
we consider.                                                                                     or low amount of instruction level parallelism at the micro-
                                                                                                 op level. A more accurate model of the second order per-
                                                                                                 formance effects introduced by a modern CISC processor is
and reads from undefined memory or registers, undef(·),
                                                                                                 straightforward if tedious to construct and we expect would
which occur during execution of the rewrite. Note that
                                                                                                 be necessary for some programs. However, the approxima-
sigsegv(·) is defined in terms of the target, which determines
                                                                                                 tion is largely sufficient for the benchmarks we consider in
the set of addresses which may be successfully dereferenced
                                                                                                 this paper.
by a rewrite for a particular testcase. Rewrites are run in a
                                                                                                    Small errors of this form can be addressed by recomput-
sandbox to ensure that undefined behavior can be detected
                                                                                                 ing perf(·) using the slower JIT compilation method as a
safely. The extension to additional kinds of counters would
                                                                                                 postprocessing step. We simply record the top-n lowest cost
be straightforward.
                                                                                                 samples taken by MCMC, rerank them based on their actual
                                                                                                 runtimes, and return the best result.
                               err(R; T , t) = wsf · sigsegv(R; T , t)
                                                + wf p · sigfloat(R; t)               (11)
                                                                                                 4.3   MCMC Sampling
                                                                                                    For X86 binary optimization, candidate rewrites are finite
                                                + wur · undef(R; t)
                                                                                                 loop-free sequences of instructions, of length `, where a dis-
   The evaluation of eq0 (·) may be accomplished either by                                       tinguished token, UNUSED, allows for the representation of
JIT compilation, or the use of a hardware emulator. For this                                     programs with fewer than ` instructions. This simplifying
paper we have chosen the latter. Figure 2(right) shows the                                       assumption is essential to the formulation of MCMC dis-
number of testcase executions that our emulator is able to                                       cussed in Section 3.2, as it places a constant value on the
perform per second: just under 500,000. This implementa-                                         dimensionality of the search space. The interested reader
tion allows us to define an optimized method for computing                                       may consult [2] for a thorough treatment of why this is
eq(·) which achieves sufficient throughput to be useful for                                      necessary. Our definition of the proposal distribution, q(·),
MCMC.                                                                                            chooses among four possible moves: the first two minor, and
                                                                                                 the latter two major:
                                         (                                                          Opcode. With probability pc , an instruction is selected
                           ∗                 eq(R; T )          eq0 (R; T , τ ) = 0              at random, and its opcode is replaced by a random opcode.
                      eq (R; T , τ ) =                                                (12)
                                             eq0 (R; T , τ )    otherwise                        The new opcode is drawn from an equivalence class of op-
                                                                                                 codes expecting the same number and type of operands as
   In addition to performance, Equation 12 has the follow-                                       the old opcode. For this paper, we construct these classes
ing desirable properties. First, failed computations of eq(·)                                    from the set of arithmetic and fixed point SSE opcodes.
will produce a counterexample testcase that may be used                                             Operand. With probability po , an instruction is selected
to refine τ as described in [5]. The careful reader will note                                    at random and one of its operands is replaced by a ran-
that refining τ affects the cost function, c(·), and effectively                                 dom operand drawn from an equivalence class of operands
changes the search space that it defines. However in prac-                                       with types equivalent to the old operand. If the operand is
tice, the number of failed validations that are required to                                      an immediate, its value is drawn from a bag of predefined
produce a robust set of testcases that accurately predict suc-                                   constants.
cess is quite low. Second, as discussed above, it smooths the                                       Swap. With probability ps , two instructions are selected
search space by allowing the transformation equality metric                                      at random and interchanged.
to quantify how different two codes are.                                                            Instruction. With probability pi , an instruction is se-
                                                                                                 lected at random, and its opcode is replaced either by an
4.2                        Performance Improvement                                               unconstrained random instruction or the UNUSED token.
  A straightforward method for computing the performance                                         A random instruction is constructed by first selecting an op-
improvement term is to JIT compile both the target and the                                       code at random and then choosing random operands of the


                                                                                             5
                                                                                               36                                       6




                                                                                                                                            Proposals / second (x10,000)
                                                                                               30                                       5




                                                                        Testcases / Proposal
          Expert                                   gcc -O3                                     24                                       4

                                                                                               18                                       3

                                                                                               12                                       2
                                                                                                       Testcases
                                                                                               6       Proposals                        1
                                                                                                       Cost Function
                                                                                               0                                        0
                                        llvm -O0

              Random
                                                                      Figure 5: Proposals evaluated per second versus
                                                                      testcases evaluated prior to early termination, dur-
                                                                      ing synthesis for the Montgomery multiplication
Figure 4: Abstract depiction of the search space for                  benchmark. Reducing the number of evaluated test-
the Montgomery multiplication benchmark. O0 and                       cases produces an almost 3x improvement in pro-
O3 optimized codes occupy a densely connected part                    posal throughput. Cost function shown unitless.
of the space which is easily traversed. Expert code
occupies an entirely different region of the space
reachable only by an extremely low probability path.                  tirely different region of the search space. As noted earlier,
                                                                      it has the property that no sequence of small equality pre-
                                                                      serving transformations connect it to either the llvm -O0
appropriate types. The UNUSED token is proposed with                  or the gcc -O3 code. It represents a completely distinct
probability pu .                                                      algorithm for implementing the Montgomery multiplication
  These definitions satisfy the ergodicity property described         kernel at the assembly level. The only method we know of
in Section 3.2. Any program can be transformed into any               for a local search procedure to transform either code into
other through repeated application of Instruction moves.              the expert code is to traverse the extremely low probability
These definitions also satisfy the symmetry property, and             path that builds the expert code in place next to the original,
thus allow the computation of acceptance probability using            all the while increasing its cost, only to delete the original
Equation 6. To see why, note that the probabilities of per-           code at the very end. Although MCMC is guaranteed to
forming all four moves types are equal to the probabilities           traverse this path in the limit, the likelihood of it doing so
of undoing the transformations they produce using a move              in any reasonable amount of time is so low as to be useless
of the same type. The opcode and operand moves are con-               in practice.
strained to sample from identical equivalence classes before             This observation motivates dividing the cost minimization
and after acceptance. Similarly, the swap and instruction             into two phases:
moves are equally unconstrained in both directions.
                                                                                      • A synthesis phase focused solely on correctness, which
4.4    Separating Synthesis From Optimization                                           attempts to locate regions of equal programs distinct
                                                                                        from the region occupied by the target.
   An early implementation of STOKE, based on the above
principles, was able to consistently transform llvm -O0 code                          • An optimization phase focused on speed, which searches
into the equivalent of gcc -O3 code. Unfortunately, it was                              for the fastest program within each of those regions.
rarely able to produce code competitive with expert hand-
written code. The reason is suggested by Figure 4, which                 The two phases share the same search implementation;
gives an abstract depiction of the search space for the Mont-         only the starting point and the acceptance functions are dif-
gomery multiplication benchmark. For loop-free sequences              ferent. Synthesis begins with a random starting point (a
of code, llvm -O0 and gcc -O3 codes differ primarily with             sequence of randomly chosen instructions), while optimiza-
respect to efficient use of the stack and choices of individ-         tion begins with a code sequence known to be equivalent to
ual instructions. Yet despite these differences, the resulting        the target. For proposals, synthesis ignores the performance
codes are algorithmically quite similar. To see this, note that       improvement term altogether and simply uses Equation 12
compiler optimizers are generally designed to compose many            as its cost function. Optimization uses both terms, allowing
small local transformations: dead code elimination deletes            it to measure improvement while also allowing it to exper-
one instruction, constant propagation changes one register            iment with “shortcuts” that (temporarily) violate transfor-
to an immediate, strength reduction replaces a multiplica-            mation correctness.
tion with an add. With respect to the search space, such
sequences of local optimizations occupy a region of equiv-            4.5                       Optimized Acceptance Computation
alent programs that are densely connected by very short                  The optimized method for computing eq∗ (·) given in Equa-
sequences of moves (often a single move) that is easily tra-          tion 12 is sufficiently fast for MCMC. However, its perfor-
versed by a local search method. Beginning from llvm -O0              mance can be further improved. As described so far, eq∗ (·)
code, a random search method will quickly identify local in-          is computed by first running the proposal on the testcases,
efficiencies one by one, improve them in turn, and hill climb         summing their costs, noting the ratio in total cost with the
its way to a gcc -O3 code.                                            current rewrite, and then sampling a random variable to de-
   The expert code discovered by STOKE occupies an en-                cide whether to accept the proposal. Instead, we can sample


                                                                  6
                                                                                                  1000
               al           bl             cl               dl                                                                                       Improved
                                                                                                  750                                                Strict
              1111         0000          0000              0000                                                                                      Random




                                                                                  Cost Function
                                                                                                  500
                                 Target
                                                                                                  250
              0000         1000          1100              1111
                                                                                                    0
                                                                                                         0      200        400       600    800    1000     1200
                                 Rewrite
                                                                                                                                 Time (s)
                                         al       bl          cl       dl
     val(T , al) ⊕ val(R, ·)          1111     0111        0011     0000        Figure 7: Strict versus improved synthesis cost
 POP val(T , al) ⊕ val(R, ·)              4        3              2    0          functions for the Montgomery multiplication bench-
                                                                                  mark. In the amount of time (s) required for im-
              wm · 1{al 6= ·}             0        1              1    1
                                                                                  proved to converge, strict produces a result similar
               reg(T , R, τ ) = 4                                                 to a purely random search.
              reg0 (T , R, τ ) = min(4, 3 + 1, 2 + 1, 1)
                               =1                                                 and a target function that produces side effects on register
                                                                                  al. The final machine states produced by running the target
Figure 6: Strict versus improved equality functions                               and a candidate rewrite are shown at the top of the figure.
for a machine state in which ax is live out. Strict as-                           Because the value that the rewrite produces for al has no
signs the maximum possible cost to a rewrite which                                correct bits the rewrite is assigned the maximum possible
produces the correct value in the wrong location.                                 cost. However the rewrite does produce the correct value,
Improved assigns a cost of almost zero.                                           only in the wrong location: dl. The improvement is to re-
                                                                                  ward rewrites that produce correct (or nearly correct) values
                                                                                  in the wrong places. The improved cost function examines
the random variable p first, compute the maximum value of                         all registers of equivalent bit-width bw(·) and selects the one
the ratio we can accept given p, and then run testcases but                       that matches the target register most closely, assigning an
terminate early if the bound is exceeded.                                         additional small penalty if the selected register is not the
  More technically, because our formulation of the proposal                       correct one:
distribution q(·) is symmetric we may compute the accep-                                                    X
tance probability α(·) of a proposal directly from c(·) as                               reg0 (R; T , τ ) =    0
                                                                                                                 min R(r, r0 ; τ )
                                                                                                                              r ∈bw(r)
                                                                                                                        r∈ρ
shown in Equation 6. By first sampling p we can invert                                                                                                        (15)
α(·) to solve for the maximum cost rewrite c(·) that we will                                             R(r, r0 ; τ ) = POP val(T , r) ⊕ val(R, r0 )
accept.
                                                                                                                      + wm · 1{r 6= r0 }
                 p < α(R → R∗ ; T )                                               For brevity, we note that we improve the definition of mem-
                                                       ∗
                                                                 !!               ory equality analogously.
                                                 c(R ; T )                           Figure 7 shows the results of using the improved defini-
                     < min 1, exp        −β·
                                                  c(R; T )             (14)       tions of register and memory equality during synthesis for
                                        log(p)                                    the Montgomery multiplication benchmark. In the amount
      c(R∗ ; T , τ ) < c(R; T , τ ) −                                             of time required for the improved cost function to converge
                                          β
                                                                                  to a zero-cost rewrite, the strict version obtained a mini-
   Because the computation of eq0 (·) is based on the iterative                   mum cost which was only slightly superior to that obtained
evaluation of testcases, it is only necessary to do so for as                     by a pure random search. The dramatic increase in perfor-
long as the running sum does not exceed this upper bound.                         mance can be explained as an implicit parallelization of the
Once it does, we know that the proposal is guaranteed to be                       search procedure. By allowing a candidate rewrite to place
rejected, and no further computation is necessary. Figure 5                       a correct value in an arbitrary location, the improved cost
shows the result of applying this optimization during synthe-                     function allows candidate rewrites to simultaneously explore
sis for the Montgomery multiplication benchmark. As the                           as many alternate computations as can be fit within a se-
value of the cost function decreases, so too do the average                       quence of length `.
number of testcases which must be evaluated prior to early
termination. This in turn produces a considerable increase                        4.7               Why and When Synthesis Works
in the number of testcases evaluated per second, which at                            It is not intuitive that a randomized search procedure
peak exceeds 50,000.                                                              should synthesize a correct rewrite from such an enormous
                                                                                  search space in a short amount of time. In our experience,
4.6     Improved Equality Metric                                                  the secret is that synthesis is effective precisely when it is
   A second and even more important improvement stems                             possible to discover parts of a correct rewrite incrementally,
from the observation that the definition of reg(·) given in                       as opposed to all at once. Figure 8 plots the current best cost
Equation 9 is unnecessarily strict. Figure 6 gives an illustra-                   obtained during synthesis against the percentage of instruc-
tive example. Consider a machine with four 4-bit registers,                       tions appearing in both that rewrite and the final correct


                                                                              7
                      target() {}
                                      1

                                                                      Synthesis                                    Optimization            Ranker
                                                                                                                                                         6
                      driver() {
                        target(x1);            Inst/Exec                                       4                         5
                        target(x2);
                        ...
                      }                                                                        ...                      ...               rewrite() {}
                                      2                    3                                                                                             7




Figure 9: The high-level design of STOKE. A target binary created by a production compiler (1) and
driver code (2) are run under instrumentation (3) using automatically generated inputs to produce testcases.
Synthesis threads (4) use the target and testcases to generate candidate rewrites, which along with the target
are refined by optimization threads (5). The results are ranked (6) and the rewrite with the lowest cost is
returned to the user (7).


                800                                            100%                                      to the constant zero function, which although almost cor-
                        Cost Function
                        Percent (with trend)
                                                                                                         rect is completely wrong, and exhibits no partially correct
                                                                                                         computations that can be hill-climbed to a correct rewrite.
                                                                       Percent of Final Code

                600                                            75%
                                                                                                           Fortunately, we note that even when synthesis fails, opti-
Cost Function




                                                                                                         mization is still possible. It must simply proceed only from
                400                                            50%                                       the region occupied by the target as a starting point.

                200                                            25%                                       5.    STOKE
                                                                                                           STOKE is a prototype implementation of the concepts de-
                 0                                             0%                                        scribed in this paper with high-level design shown in Figure
                                                                                                         9. A user provides a target binary which was created using
Figure 8: Cost function versus percentage of instruc-                                                    a production compiler (in our case, llvm -O0); in the event
tions which appear relative to final zero-cost rewrite.                                                  that the target contains loops, STOKE identifies loop-free
Random search is an effective method for perform-                                                        subsequences of the code which it will attempt to optimize.
ing synthesis insofar as it is able to discover partially                                                The user also provides an annotated driver in which the tar-
correct rewrites incrementally.                                                                          get is called in an appropriate context. Based on the user’s
                                                                                                         annotations, STOKE automatically generates random in-
                                                                                                         puts to the target, compiles the driver, and then runs the
                                                                                                         code under instrumentation to produce testcases. The tar-
rewrite for the Montgomery multiplication benchmark. As                                                  get and testcases are broadcast to a small cluster of synthesis
search proceeds, the percentage of correct code increases in                                             threads which after a fixed amount of time report back can-
inverse proportion to the value of the cost function. While                                              didate rewrites. In like fashion, a small cluster performs
this is very encouraging and there are many programs that                                                optimization on both the target and those rewrites. Finally,
satisfy the property that they can be synthesized in pieces,                                             the set of rewrites with a final cost that is within 20% of the
each of which increases the average number of correct bits                                               minimum are re-ranked based on actual runtime, and the
in the output, there are certainly interesting programs that                                             best is returned to the user.
do not have this property. In the limit, any code performing
a complex computation that is reduced to a single boolean                                                5.1    Test Case Generation and Evaluation
value poses a problem for our approach. The discovery of                                                    STOKE automatically generates testcases using annota-
partially correct computations is useful as a guide for ran-                                             tions provided by a user. Because STOKE operates on 64-
dom search only insofar as they are able to produce a par-                                               bit X86 assembly, those inputs are limited to fixed-width bit
tially correct result, which can be detected by a cost func-                                             strings, which unless otherwise specified, are sampled uni-
tion.                                                                                                    formly at random. If the target uses an input to form a
   This observation motivates the desire for a cost function                                             memory address, the user must annotate that input with a
which maximizes the signal produced by a partially correct                                               range of values that guarantee that the resulting addresses
rewrite. We discussed a successful application of this princi-                                           are legal given the context in which the target is called. The
ple in Section 4.6. Nonetheless, there remains room for im-                                              compiled program is executed under instrumentation using
provement. Consider the program which rounds its inputs                                                  Intel’s PinTool [12]. As each instruction is executed, the tool
up to the next highest power of two. This program has the                                                records the state of all general purpose, SSE, and condition
interesting property that it differs from the program which                                              registers, as well as dereferenced memory. The initial state
simply returns zero in only one bit per testcase. The im-                                                of the registers, along with the first values dereferenced from
proved cost function discussed above assigns a very low cost                                             each memory address are used to form testcase inputs. Out-


                                                                                                     8
 7
              gcc -O3
 6
              icc -O3
 5            STOKE
              llvm -O0
 4

 3

 2

 1

 0




                                                                                                                      * p18




                                                                                                                                                  * p22
      p01

             p02

                   p03

                         p04

                                   p05



                                                 p07

                                                       p08

                                                              p09

                                                                     p10

                                                                           p11



                                                                                       p13

                                                                                             p14

                                                                                                   p15

                                                                                                         p16

                                                                                                                p17




                                                                                                                                    p20

                                                                                                                                          * p21



                                                                                                                                                          * p23

                                                                                                                                                                  p24

                                                                                                                                                                        * p25
                                          p06




                                                                                 p12




                                                                                                                              p19




                                                                                                                                                                                * mont



                                                                                                                                                                                                * saxpy
                                                                                                                                                                                         list
Figure 10: Average speedup over llvm -O0 for benchmark kernels. Beginning from code produced by llvm
-O0, STOKE discovers rewrites which are comparable to code produced by gcc and icc with full optimizations
enabled. In some cases, the rewrite outperforms both, and are comparable to expert handwritten assembly.
Kernels for which STOKE discovered an algorithmically distinct rewrite are annotated with a star.


                    wsf        1         pc     0.16     pu         0.16                           of memory accesses at addresses addr1 and addr2 , STOKE
                    wf p       1         po      0.5     β           0.1                           asserts an additional constraint which relates their values:
                    wur        2         ps     0.16      `          50                            addr1 = addr2 ⇒ val1 = val2 . Using these constraints,
                    wm         3         pi     0.16                                               STOKE performs an STP query which asks whether there
                                                                                                   does not exist an initial machine state which causes the two
Figure 11: MCMC parameters used by STOKE for                                                       sequences to produce different values for the live outputs
synthesis and optimization.                                                                        with respect to the target. If the answer is “yes”, then the
                                                                                                   sequences are equal. If the answer is “no”, then the prover
                                                                                                   produces a counter example which is used to produce a new
puts are formed analogously. By default, STOKE generates                                           testcase.
32 testcases for each target.                                                                         STOKE makes two simplifying assumptions which are
   For each testcase, The set of addresses dereferenced by                                         necessary to keep validator runtimes tractable. First, it as-
the target are used to define the sandbox in which candi-                                          sumes that stack addresses are represented exclusively as
date rewrites are executed. Attempts to dereference invalid                                        constant offsets from the stack pointer. This allows STOKE
addresses are trapped and replaced by instructions which                                           to treat stack addresses as nameable locations, and mini-
produce a constant zero value. Attempts to read from regis-                                        mizes the number of expensive memory constraints which
ters in an undefined state and computations which produce                                          must be asserted. This is essential for validating against
floating point exceptions are handled similarly.                                                   llvm -O0 code, which exhibits heavy stack traffic. Second,
                                                                                                   it treats 64-bit multiplication and division as uninterpreted
5.2         Validation                                                                             functions, by asserting the constraint that the instructions
   STOKE uses a sound procedure for validating the equality                                        produce identical random values when executed on identi-
of two sequences of loop-free assembly which is similar to the                                     cal inputs. Whereas STP diverges when reasoning explicitly
one described in [3]. Code sequences are converted into SMT                                        about two or more such operations, our benchmarks contain
formulae in the quantifier free theory of bit-vector arithmetic                                    as many as four per sequence.
used by the STP [8] theorem prover, and used to produce a
query which asks whether both sequences produce the same                                           5.3         Parallel Synthesis and Optimization
side effects on live outputs when executed from the same                                             Synthesis and optimization are executed in parallel on
initial machine state. For our purposes, a machine state                                           a small cluster consisting of 40 dual-core 1.8 GHz AMD
consists of general purpose, SSE, and condition registers,                                         Opterons. Both are allocated computational budgets of 30
and memory. Depending on type, registers are modeled as                                            minutes. The MCMC parameters used by both phases are
between 8- and 128-bit vectors. Memory is modeled as two                                           summarized in Figure 11.
vectors: a 64-bit address and an 8-bit value (X86 is byte
addressable).
   STOKE first asserts the constraint that both sequences                                          6.     EVALUATION
agree on the initial machine state of the live inputs with                                           In addition to the Montgomery multiplication kernel dis-
respect to the target. Next, it iterates over the instruc-                                         cussed so far, STOKE was evaluated on benchmarks drawn
tions in the target, and for each instruction asserts a con-                                       both from literature and real-world high-performance codes.
straint which encodes the transformation it produces on                                            The performance improvements obtained for those kernels
the machine state. These constraints are chained together                                          are summarized in Figure 10, while corresponding STOKE
to produce a constraint on the final machine state of the                                          runtimes are shown in Figure 12. Beginning with a bi-
live outputs with respect to the target. Analogous con-                                            nary compiled by llvm -O0, STOKE consistently discovers
straints are asserted for the rewrite. Finally, for all pairs                                      rewrites which match the performance of the code produced


                                                                                              9
1000         Synthesis
             Optimization


 100




  10




   1




                                                                                                                      *p19

                                                                                                                             *p20
       p01

               p02

                     p03

                            p04




                                              p07

                                                    p08

                                                          p09

                                                                p10

                                                                      p11

                                                                            p12

                                                                                  p13

                                                                                        p14

                                                                                              p15

                                                                                                    p16

                                                                                                          p17

                                                                                                                p18




                                                                                                                                          p22

                                                                                                                                                p23

                                                                                                                                                      *p24

                                                                                                                                                             p25
                                  p05

                                        p06




                                                                                                                                    p21




                                                                                                                                                                                 saxpy
                                                                                                                                                                   mont

                                                                                                                                                                          list
Figure 12: STOKE runtimes for synthesis and optimization (s) required to produce the results shown in
Figure 10. Kernels for which synthesis timed out are annotated with a star.


int p21(int x, int a, int b, int c) {                                                         superotpimization, and identified a 25 program benchmark
  return ((-(x == c)) & (a ^ c)) ^                                                            which ranges in complexity from turning off the right-most
         ((-(x == a)) & (b ^ c)) ^ c;                                                         bit in a word, to rounding up to the next highest power
}                                                                                             of 2, or selecting the upper 32 bits from a 64-bit multiplica-
                                                                                              tion. Our implementation of the benchmark uses the C code
                                                                                              found in the original text. For brevity, we discuss only the
.L0                                           .L0                                             programs for which STOKE discovered an algorithmically
  movl         edx, eax                         cmpl   edi, ecx                               distinct rewrite.
  xorl         edx, edx                         cmovel esi, ecx                                  Figure 13 shows the “Cycle Through 3 Values” benchmark,
  xorl         ecx, eax                         xorl   edi, esi                               which takes an input, x, and transforms it to the next value
  cmpl         esi, edi                         cmovel edx, ecx                               in the sequence ha, b, ci: a becomes b, b becomes c, and c
  sete         dl                               movq   rcx, rax                               becomes a. Hacker’s Delight points out that the most nat-
  negl         edx                                                                            ural implementation of this function is a sequence of condi-
  andl         edx, eax                                                                       tional assignments, but notes that on an ISA without condi-
  xorl         edx, edx                                                                       tional move intrinsics the implementation shown is cheaper
  xorl         ecx, eax                                                                       than one which uses branch instructions. For 64-bit X86,
  cmpl         ecx, edi                                                                       which has conditional move intrinsics, this turns out to be
  sete         dl                                                                             an instance of premature optimization. Unfortunately, nei-
  xorl         ecx, esi                                                                       ther gcc nor icc are able to detect this, and are forced to
  negl         edx                                                                            transcribe the code as written. There are no sub-optimal
  andl         esi, edx                                                                       subsequences in the resulting code and the production com-
  xorl         edx, eax                                                                       pilers are simply unable to reason about the semantics of
                                                                                              the function as a whole. For this reason, we expect that
Figure 13: Cycling Through 3 Values benchmark.                                                equality-preserving superoptimizers would exhibit the same
STOKE sees through the esoteric implementation                                                behavior. STOKE on the other hand, has no trouble redis-
which gcc -O3 translates literally (left) and rediscov-                                       covering the natural implementation from the 41 line llvm
ers the intuitive algorithm using conditional move                                            -O0 compilation. We note that although this rewrite is only
intrinsics (right).                                                                           five lines long, it remains beyond the reach of superoptimiz-
                                                                                              ers based on bruteforce enumeration.
                                                                                                 In similar fashion, the implementation that Hacker’s De-
by gcc and icc with full optimizations enabled. In several                                    light recommends for the “Compute the Higher Order Half of
cases, the performance exceeds both and is comparable to                                      a 64-bit Product” multiplies two 32-bit inputs in four parts
expert handwritten assembly. As we explain below, the im-                                     and aggregates the results. The computation resembles the
provement often results from the discovery of a completely                                    Montgomery multiplication benchmark, and STOKE discov-
distinct assembly level algorithm for implementing the tar-                                   ers a rewrite which requires a single multiplication using the
get code. We close with discussion of the benchmarks which                                    appropriate bit-width intrinsic. STOKE additionally dis-
highlight STOKE’s limitations.                                                                covers a number of typical superoptimizer rewrites. These
                                                                                              include using the popcnt intrinsic, which counts the number
6.1    Hacker’s Delight                                                                       of 1-bits in an integer, as an intermediate step in the “Com-
  Hacker’s Delight [20], commonly referred to as “the bible                                   pute Parity” and “Determine if an Integer is a Power of 2”
of bit-twiddling hacks”, is a collection of techniques for en-                                benchmarks.
coding otherwise complex algorithms as small loop-free se-
quences of bit-manipulating instructions. Gulwani [9] noted                                   6.2     SAXPY
this as a fine source of benchmarks for program synthesis and                                   SAXPY (Single-precision Alpha X Plus Y) is a level 1


                                                                                        10
  void SAXPY(int* x, int* y, int a) {                                 while ( head != 0 ) {
    x[i]   = a * x[i]   + y[i];                                         head->val *= 2;
    x[i+1] = a * x[i+1] + y[i+1];                                       head = head->next;
    x[i+2] = a * x[i+2] + y[i+2];                                     }
    x[i+3] = a * x[i+3] + y[i+3];
  }

  .L0                                                                  movq -8(rsp), rdi                .L4
    movslq ecx, rcx                                                   .L4                                movq -8(rsp), rdi
    leaq   (rsi,rcx,4), r8                                             sall (rdi)                        sall (rdi)
    leaq   1(rcx),      r9                                             movq 8(rdi), rdi                  movq 8(rdi), rdi
    movl   (r8),        eax                                           .L6                                movq rdi, -8(rsp)
    imull edi,          eax
    addl   (rdx,rcx,4), eax                                            testq rdi,    rdi                .L6
    movl   eax,         (r8)                                           jne   .L4                         movq -8(rsp), rdi
    leaq   (rsi,r9,4), r8                                                                                testq rdi, rdi
    movl   (r8),        eax                                                                              jne   .L4
    imull edi,          eax
    addl   (rdx,r9,4), eax                                            Figure 15:     Linked List Traversal benchmark.
    leaq   2(rcx),      r9
    addq   3,           rcx                                           STOKE discovers the same rewrite (right) as
    movl   eax,         (r8)                                          Bansal’s superoptimizer, but fails to cache the head
    leaq   (rsi,r9,4), r8                                             pointer in a register, as in the gcc -O3 code (left).
    movl   (r8),        eax
    imull edi,          eax
    addl   (rdx,r9,4), eax                                               Bansal’s superoptimizer [3] was evaluated on the Linked
    movl   eax,         (r8)
    leaq   (rsi,rcx,4), rax                                           List Traversal Benchmark shown in Figure 15. The code
    imull (rax),        edi                                           iterates over a list of integers and multiplies each of the
    addl   (rdx,rcx,4), edi                                           elements by two. The code is unique with respect to the
    movl   edi,         (rax)                                         benchmarks discussed so far, as it contains a loop. As a re-
                                                                      sult, STOKE is unable to optimize the function as a whole,
  .L0                                                                 but rather only it’s inner-most loop-free fragment. STOKE
    movd   edi,         xmm0
    shufps 0,           xmm0, xmm0                                    discovers the same optimizations as Bansal’s superoptimizer,
    movups (rsi,rcx,4), xmm1                                          the elimination of stack traffic and a strength reduction from
    pmullw xmm1,        xmm0                                          multiplication to bit shifting. However it fails in like fashion
    movups (rdx,rcx,4), xmm1                                          to eliminate the instructions which copy the head pointer
    paddw xmm1,         xmm0                                          from and to the stack on every iteration of the loop. The
    movups xmm0,        (rsi,rcx,4)                                   production compilers on the other hand, are able to elimi-
                                                                      nate the memory traffic by caching the pointer in a register
Figure 14: SAXPY benchmark. Unlike gcc -O3                            prior to entering the loop. As a result, the rewrite discov-
(top), STOKE discovers a rewrite which uses SSE                       ered by STOKE is slower than the code produced by gcc -O3
vector instructions (bottom).                                         (surprisingly, icc does not perform strength reduction, and
                                                                      produces code which performs similarly). This shortcoming
                                                                      could be addressed by extending our framework to validate
vector operation in the Basic Linear Algebra Subsystems               and propose modifications to code containing loops.
Library [4]. The code makes heavy use of heap accesses and               As shown in Figure 12, STOKE is unable to synthesize a
presents the opportunity for optimization using vector in-            rewrite for three of the Hacker’s Delight Benchmarks. All
trinsics. To enable STOKE to discover this possibility, our           three benchmarks, despite being quite complex, have the
implementation is unrolled four times by hand, as shown in            interesting property that they produce results which differ
Figure 14. Despite heavy annotation to indicate that the              by only a single bit from a simple yet completely incorrect
addresses pointed to by x and y are aligned and do not                alternative. The “Round Up to the Next Highest Power of
alias each other, the production compilers either cannot de-          2” benchmark is nearly indistinguishable from the function
tect the possibility of a compilation using vector intrinsics,        which always returns zero. The same is true of the “Next
or are precluded by some internal heuristic from doing so.            Highest with Same Number of 1-bits”, and a small trans-
STOKE on the other hand, discovers the natural implemen-              formation to the “Exchanging Two Fields” benchmark with
tation: the constant a is broadcast four ways from a general          respect to the identity function. Fortunately, for these three
purpose register into an SSE register, and then multiplied            benchmarks, using its optimization phase alone STOKE is
by, and added to the contents of x and y, which are loaded            still able to discover rewrites which perform comparably to
into SSE registers four elements at a time. The four way              the production compiler code, which we believe to be opti-
broadcast does not appear anywhere in either the gcc -O3              mal. In general, however, we do not expect this to be the
code, or in the original 61 line llvm -O0 code. As observed           case. A more sophisticated cost function, as described in
above, this and the length of the final rewrite allow STOKE           section 4.7, is surely necessary.
to outperform both the production compilers and likely ex-
isting superoptimizers as well.
                                                                      7.   CONCLUSION AND FUTURE WORK
6.3   Limitations                                                       We have shown a new approach to the loop-free binary su-


                                                                 11
peroptimization task which reformulates program optimiza-             [7] P. Diaconis. The Markov Chain Monte Carlo
tion as a stochastic search problem. Compared to a tradi-                 Revolution. Bulletin of the American Mathematical
tional compiler, which factors optimization into a sequence               Society, 46(2):179–205, Nov. 2008.
of small independently solvable subproblems, our framework            [8] V. Ganesh and D. L. Dill. A decision procedure for
is based on cost minimization and considers the competing                 bit-vectors and arrays. In CAV, pages 519–531, 2007.
constraints of transformation correctness and performance             [9] S. Gulwani, S. Jha, A. Tiwari, and R. Venkatesan.
improvement simultaneously as terms in a cost function.                   Synthesis of loop-free programs. In Proceedings of the
We show that an MCMC sampler can be used to rapidly                       32nd ACM SIGPLAN conference on Programming
explore functions of this form and produce low cost samples               language design and implementation, PLDI ’11, pages
which correspond to high quality code sequences. Although                 62–73, New York, NY, USA, 2011. ACM.
our method sacrifices completeness, the scope of programs            [10] W. K. Hastings. Monte Carlo sampling methods using
which we are able to reason about, and the quality of the                 Markov chains and their applications. Biometrika,
rewrites we produce, far exceed those of existing superopti-              57(1):97–109, Apr. 1970.
mizers.                                                              [11] R. Joshi, G. Nelson, and K. H. Randall. Denali: A
   Although our prototype implementation, STOKE, is in                    goal-directed superoptimizer. In PLDI, pages 304–314,
many cases able to produce rewrites which are competitive                 2002.
with or outperfrom the code produced by production com-
                                                                     [12] C. keung Luk, R. Cohn, R. Muth, H. Patil,
pilers, there remains substantial room for improvement. In
                                                                          A. Klauser, G. Lowney, S. Wallace, V. Janapa, and
future work, we intend to pursue both a validation and pro-
                                                                          R. K. Hazelwood. Pin: Building customized program
posal mechanism for code containing loops and a synthesis
                                                                          analysis tools with dynamic instrumentation. In In
cost function which is robust against targets with numerous
                                                                          Programming Language Design and Implementation,
deceptively attractive, albeit completely incorrect synthesis
                                                                          pages 190–200. ACM Press, 2005.
alternatives.
                                                                     [13] P. Liang, M. I. Jordan, and D. Klein. Learning
                                                                          programs: A hierarchical Bayesian approach. In
8.   ACKNOWLEDGMENTS                                                      International Conference on Machine Learning
  The authors would like to thank Peter Johnston, Juan                    (ICML), 2010.
Manuel Tamayo, and Kushal Tayal for their assistance in              [14] H. Massalin. Superoptimizer: a look at the smallest
the implementation of STOKE, Ankur Taly for his help with                 program. In Proceedings of the second international
semantics of X86 opcodes, David Ramos for his help with                   conference on Architectual support for programming
STP, Jake Herczeg for his time spent designing Figure 4,                  languages and operating systems, ASPLOS-II, pages
and Martin Rinard for suggesting a technique which focuses                122–126, Los Alamitos, CA, USA, 1987. IEEE
more on testcases than validation.                                        Computer Society Press.
                                                                     [15] N. Metropolis, A. W. Rosenbluth, M. N. Rosenbluth,
                                                                          A. H. Teller, and E. Teller. Equation of State
9.   REFERENCES                                                           Calculations by Fast Computing Machines. The
 [1] Markov Chain Monte Carlo in Practice:                                Journal of Chemical Physics, 21(6):1087–1092, 1953.
     Interdisciplinary Statistics (Chapman & Hall/CRC                [16] A. F. Neuwald, J. S. Liu, D. J. Lipman, and C. E.
     Interdisciplinary Statistics). Chapman and Hall/CRC,                 Lawrence. Extracting protein alignment models from
     1 edition, Dec. 1995.                                                the sequence database. Nucleic Acids Research,
 [2] C. Andrieu, N. de Freitas, A. Doucet, and M. I.                      25:1665–1677, 1997.
     Jordan. An Introduction to MCMC for Machine                     [17] O. Solar-lezama, L. Tancau, R. Bodik, V. Saraswat,
     Learning. Machine Learning, 50(1):5–43, Jan. 2003.                   and S. Seshia. Combinatorial sketching for finite
 [3] S. Bansal and A. Aiken. Automatic generation of                      programs. In In 12th International Conference on
     peephole superoptimizers. In Proceedings of the 12th                 Architectural Support for Programming Languages and
     international conference on Architectural support for                Operating Systems (ASPLOS 2006, pages 404–415.
     programming languages and operating systems,                         ACM Press, 2006.
     ASPLOS-XII, pages 394–403, New York, NY, USA,                   [18] R. Tate, M. Stepp, Z. Tatlock, and S. Lerner. Equality
     2006. ACM.                                                           saturation: a new approach to optimization. In POPL,
 [4] L. S. Blackford, J. Demmel, J. Dongarra, I. Duff,                    1 2009.
     S. Hammarling, G. Henry, M. Heroux, L. Kaufman,                 [19] E. Veach and L. J. Guibas. Metropolis light transport.
     A. Lumsdaine, A. Petitet, R. Pozo, K. Remington,                     In Computer Graphics (SIGGRAPH ’97 Proceedings,
     and R. C. Whaley. An updated set of basic linear                     pages 65–76. Addison Wesley, 1997.
     algebra subprograms (blas). ACM Transactions on                 [20] H. S. Warren. Hacker’s Delight. Addison-Wesley
     Mathematical Software, 28:135–151, 2001.                             Longman Publishing Co., Inc., Boston, MA, USA,
 [5] C. Cadar, D. Dunbar, and D. Engler. Klee: Unassisted                 2002.
     and automatic generation of high-coverage tests for
     complex systems programs. In Proceedings of the 8th
     USENIX conference on Operating systems design and
     implementation, OSDI’08, pages 209–224, Berkeley,
     CA, USA, 2008. USENIX Association.
 [6] S. Chenney and D. A. Forsyth. Sampling plausible
     solutions to multi-body constraint problems, 2000.


                                                                12
