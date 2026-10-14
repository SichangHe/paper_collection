                                         CryptOpt: Verified Compilation with Randomized Program
                                         Search for Cryptographic Primitives (full version)
                                         JOEL KUEPPER, University of Adelaide, Australia
arXiv:2211.10665v3 [cs.CR] 22 May 2023




                                         ANDRES ERBSEN, Massachusetts Institute of Technology, USA
                                         JASON GROSS, Massachusetts Institute of Technology, USA
                                         OWEN CONOLY, Massachusetts Institute of Technology, USA
                                         CHUYUE SUN, Stanford University, USA
                                         SAMUEL TIAN, Massachusetts Institute of Technology, USA
                                         DAVID WU, University of Adelaide, Australia
                                         ADAM CHLIPALA, Massachusetts Institute of Technology, USA
                                         CHITCHANOK CHUENGSATIANSUP, The University of Melbourne, Australia
                                         DANIEL GENKIN, Georgia Institute of Technology, USA
                                         MARKUS WAGNER, Monash University, Australia
                                         YUVAL YAROM, Ruhr University Bochum, Germany



                                         Most software domains rely on compilers to translate high-level code to multiple different machine languages,
                                         with performance not too much worse than what developers would have the patience to write directly
                                         in assembly language. However, cryptography has been an exception, where many performance-critical
                                         routines have been written directly in assembly (sometimes through metaprogramming layers). Some past
                                         work has shown how to do formal verification of that assembly, and other work has shown how to generate
                                         C code automatically along with formal proof, but with consequent performance penalties vs. the best-
                                         known assembly. We present CryptOpt, the first compilation pipeline that specializes high-level cryptographic
                                         functional programs into assembly code significantly faster than what GCC or Clang produce, with mechanized
                                         proof (in Coq) whose final theorem statement mentions little beyond the input functional program and the
                                         operational semantics of x86-64 assembly. On the optimization side, we apply randomized search through the
                                         space of assembly programs, with repeated automatic benchmarking on target CPUs. On the formal-verification
                                         side, we connect to the Fiat Cryptography framework (which translates functional programs into C-like IR
                                         code) and extend it with a new formally verified program-equivalence checker, incorporating a modest subset
                                         of known features of SMT solvers and symbolic-execution engines. The overall prototype is quite practical,
                                         e.g. producing new fastest-known implementations of finite-field arithmetic for both Curve25519 (part of the
                                         TLS standard) and the Bitcoin elliptic curve secp256k1 for the Intel 12𝑡ℎ and 13𝑡ℎ generations.




                                         Authors’ addresses: Joel Kuepper, University of Adelaide, Australia; Andres Erbsen, Massachusetts Institute of Technology,
                                         USA; Jason Gross, Massachusetts Institute of Technology, USA; Owen Conoly, Massachusetts Institute of Technology, USA;
                                         Chuyue Sun, Stanford University, USA; Samuel Tian, Massachusetts Institute of Technology, USA; David Wu, University
                                         of Adelaide, Australia; Adam Chlipala, Massachusetts Institute of Technology, USA; Chitchanok Chuengsatiansup, The
                                         University of Melbourne, Australia; Daniel Genkin, Georgia Institute of Technology, USA; Markus Wagner, Monash
                                         University, Australia; Yuval Yarom, Ruhr University Bochum, Germany.
2                Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom




1     INTRODUCTION
Being a foundational pillar of computer security, cryptographic software needs to achieve three
often-competing aims. First, being security-critical, the software needs to be correct and protected
from implementation attacks. Second, because it is used frequently, it needs to be efficient. Third,
for migration to new architectures, the software needs to be portable. Implementations of crypto-
graphic code, therefore, must strike a trade-off between these needs. Implementations that aim for
portability tend to use high-level languages, such as Java or C. These allow for easy maintenance
and are essentially platform-independent, assuming the existence of suitable development tools
like compilers and assemblers.
   At the same time, compiler-based code generation can be a double-edged sword. First, compiler-
produced cryptographic code tends to underperform when compared to hand-optimized code [Bern-
stein et al. 2013, 2014a,b, 2017; Chou 2015, 2016; Chuengsatiansup et al. 2013; Chuengsatiansup
and Stehlé 2019; Kannwischer et al. 2019], typically written directly in the platform’s assembly lan-
guage. Beyond slower performance, compilers are typically not designed for maintaining security
properties. In particular, compilation bugs could result in incorrect code [Erbsen et al. 2019, §V-B],
while overly aggressive optimizations may even strip side-channel protections [Barthe et al. 2018;
D’Silva et al. 2015; Kaufmann et al. 2016].
   We note that the difficulties compilers have when operating over cryptographic code are not
caused by high code complexity. In fact, cryptographic code tends to be simpler than a typical
program code, due to its avoidance of data-dependent control flows and memory-access patterns for
reasons of side-channel resistance. Ironically, compiler optimization passes often focus on control
flow, as it offers higher impact than fine-tuning straight-line code [Aho et al. 1986].
   Instead, the cause is that such code tends to be simpler than a typical program code, and this
simplicity deprives the compiler of optimization opportunities. At the same time, we observe that
such simplicity may offer opportunities for using strategies not commonly exploited by compilers,
such as reordering arithmetic operations within a basic block or exchanging machine instructions
with semantically equivalent machine instructions. Thus, our work starts from the question:
How can we exploit the simplicity of cryptographic primitives in order to generate efficient and provably
correct implementations of cryptographic functions?

1.1    Our Contribution
We present CryptOpt, a new code generator that produces highly efficient code tailored to the
architecture it runs on. The task is split between finding performant program variants and checking
that they have preserved program behavior. The former works via randomized search, and the latter
works via a formally verified program-equivalence checker that should be applicable even with
other optimization strategies. As a result, the randomized-search procedures need not be trusted,
and, when we compose them with the Fiat Cryptography Coq-verified compiler [Erbsen et al. 2019]
and our new equivalence checker (as shown in Figure 1), we get end-to-end functional-correctness
proofs for fast assembly code – faster than any code demonstrated for the cryptographic algorithms
we study, when compiling automatically from high-level programs as we do.
  To find performant machine-code variants, instead of relying on human heuristics, CryptOpt
represents code generation as a combinatorial optimization problem. That is, CryptOpt considers
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives           3


a solution space that consists of machine-code implementations of the target function and uses
techniques from the randomized-search domain to seek the best-performing implementation.
   To optimize, CryptOpt first chooses an arbitrary correct im-
plementation of the target function. It then mutates the imple-             Field            Fiat
mentation by either changing the instruction(s) that implements          Parameters     Cryptography
a certain operation or changing the order of operations. If the mu-
tated implementation is not worse than the original, the mutated
                                                                                         Optimizer
implementation is kept; otherwise it is discarded.                         Fiat IR

   Instead of trying to predict code performance like in work by
Joshi et al. [2002]; Schkufza et al. [2013], CryptOpt measures actual                    Assembly
execution time. This approach is important because it avoids inac-
curacies inherent in hardware models and allows CryptOpt to tailor         Checker
produced code to the target processor while treating the processor
itself as an opaque unit. A particular advantage of the approach
                                                                      Fig. 1. Integration design. Boxes
is that once manufacturers release new hardware, which changes represent individual components,
e.g. pipelining effects or caching behavior, CryptOpt adapts to it arrows represent data flow, and
automatically without requiring manual adaptation of hardware filled boxes represent files. Op-
models. This find-and-optimize approach is implemented by the timizer and Checker are results
Optimizer component in Figure 1.                                      of this work. Fiat Cryptography
   To check that generated code is correct, CryptOpt integrates and Checker are formally veri-
with Fiat Cryptography [Erbsen et al. 2019]. That framework, im- fied.
plemented in Coq, already generates low-level IR programs proven
to preserve behavior of high-level functional programs, and it has been adopted by all major web
browsers and mobile platforms for small but important parts of their TLS implementations, so
there is high potential for impact improving performance further without sacrificing formal rigor.
CryptOpt begins with Fiat IR programs and generates x86-64 assembly code. To avoid needing to
model the randomized-search process, we instead build and prove an equivalence checker, which
can compare programs across Fiat IR and x86-64 assembly. Its two main pieces implement modest
subsets of features known from SMT solvers and symbolic-execution engines. From SMT solvers,
we take an E-graph data structure [Detlefs et al. 2005] to canonicalize logical expressions via
rewrite rules. From symbolic-execution engines, we take maintenance of symbolic states that tie
registers and symbolic memory locations to logical expressions known to the solver. Thanks to
their combined proof in Coq, none of these details need to be trusted. This checking is done by the
Checker component in Figure 1.
   We evaluate CryptOpt using finite fields with nine different prime moduli. We use Fiat Cryptog-
raphy to generate the Fiat IR for the multiply and square operations for these fields. We then use
the CryptOpt optimizer to generate x86-64 assembly code for these operations and the equivalence
checker to verify that the code matches the Fiat IR. The produced x86-64 assembly code achieves
a mean speedup of 1.74 compared to GCC 12.1.0 (speedup 1.40 against Clang 15.0.6), across ten
different x86-64 platforms (four AMD, six Intel).
   We further evaluate the CryptOpt optimizer as a stand-alone code generator. For that, we
create an input function from the C code of libsecp256k1 [Bitcoin Core 2021], feed it into the
CryptOpt optimizer, and obtain an average speedup of 1.04 against the hand-optimized assembly
code in libsecp256k1. As we do not have Fiat IR code matching libsecp256k1, we cannot use
the equivalence checker to verify the code we produce.
4                Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


1.2    Summary of Contributions
In summary, we make the following contributions in this paper:
• We present CryptOpt, a code generator that relies on combinatorial optimization instead of
  compiler heuristics for producing highly efficient code (Section 5). This broad approach is shown
  to apply to larger routines than past work has tackled successfully, while also being integrated
  with formal verification for the first time.
• We demonstrate that a relatively modest Fiat Cryptography extension (Section 6) suffices to
  enable integration with a wide range of backend compiler heuristics. We implemented and verified
  Coq functional programs with a minimal subset of well-known features from SMT solvers and
  symbolic-execution engines, leading to a single extractable compiler that checks assembly files
  for semantic equivalence with high-level functional programs. To our knowledge, this is the first
  such equivalence checker with mechanized proof from first principles.
• We generate formally verified high-performance cryptographic code optimized for ten CPU
  architectures, obtaining considerable speedups over GCC and Clang (Section 7).

    The source code for CryptOpt is available at https://github.com/0xADE1A1DE/CryptOpt.

2     BACKGROUND
In this section we present basic background required for the rest of the paper.

2.1    Random Local Search
A combinatorial optimization problem aims to find an optimal solution (e.g. one that minimizes
a given objective function) within a discrete set of candidate solutions. Random Local Search
(RLS) [Auger and Doerr 2011; Doerr and Neumann 2019] is a simple optimization strategy that is
often efficient and effective in finding local optima. A run of RLS starts from a random candidate
solution. It then applies a random mutation to the current candidate solution, generating another
solution within the possible solutions set. If the mutation improves (or does not deteriorate) the
solution, the mutated solution is kept, replacing the current candidate solution. Otherwise, the
mutation is discarded, and the current candidate solution remains unchanged. This mutation and
evaluation repeats until some predefined termination condition is satisfied.
   RLS is often highly sensitive to the initial conditions, i.e. the candidate solution it starts from.
To address such erratic behavior, the simple Bet-and-Run heuristic [Fischetti and Monaci 2014;
Weise et al. 2019] turns the sensitivity to the initial conditions into an advantage by employing
multiple runs. A typical use of Bet-and-Run starts with multiple independent runs of RLS, each
optimizing for a predefined number of mutations. After this initialization step, the algorithm selects
the best run and lets this run continue optimizing from that step, stopping when a total number of
mutations is explored.

2.2    Finite-Field Arithmetic for Cryptography
We focus on elliptic-curve cryptography (ECC), which is used widely in Internet standards like TLS.
It involves certain geometric aspects that are orthogonal to our tooling, which supports arithmetic
modulo large prime numbers, otherwise known as finite-field arithmetic (FFA).
    Because the FFA is a performance-critical component in the implementations, many tend to
implement it by hand. For instance, targeting different architectures, the ubiquitous cryptographic
library OpenSSL [OpenSSL 2022] has many hand-optimized implementations for Curve25519 and
NIST P-256, which are both well-known instantiations of ECC. The Bitcoin blockchain uses yet
another curve called secp256k1 for their block signatures. Its core library libsecp256k1 contains
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives           5


hand-optimized code for the field arithmetic as well as a C implementation used as a fallback in
architectures for which no optimized version exists.
   FFA is not trivial to implement. In particular, a field element is typically represented by multiple
limbs using several CPU registers, and thus every field operation requires multiple CPU cycles.
However, these implementations tend to be straight-line code, heavy on arithmetic rather than
control flow, leading to ineffective optimization by standard compilers. Human experts instead
manually apply simultaneous instruction selection, instruction scheduling, and register alloca-
tion, which, going well beyond capabilities of off-the-shelf C compilers, should take into account
microarchitecture details such as macro-op fusion [Celio et al. 2016; Ronen et al. 2004], cache
prediction [Hooker and Eddy 2013; Lepak and Lipasti 2000; Subramaniam and Loh 2006], cache-
replacement policies [Vila et al. 2020], and other (potentially undocumented) microarchitectural
choices.

2.3   Fiat Cryptography
Erbsen et al. [2019] present the Fiat Cryptography framework, which translates descriptions of
field arithmetic into code with Coq proof of functional correctness. The starting point is a library
of functional programs that are used as templates for generating code for performing operations
in finite fields. These functional programs, which have been proven correct, can be specialized
with a specific prime order for generating an intermediate representation (Fiat IR) of the code that
performs field arithmetic operations for the required field.
   In execution, Fiat Cryptography selects the functional program to specialize for the required field
size and produces provably correct Fiat IR. It then uses one of the available backends to process the
Fiat IR code and produce an implementation in one of the supported languages, including C, Java,
and Zig.

2.4   Equivalence Checking
Formally proved compilers are the gold standard to address concerns of optimization soundness.
For instance, CompCert [Leroy 2009; Leroy et al. 2016] was proved as a correct C compiler using
the Coq theorem prover, which we also rely on. However, proving a whole compiler can be very
labor-intensive, and thus it is often appealing to prove a checker for compiler outputs, known as a
translation validator. For instance, CompCert was extended in that way [Tristan and Leroy 2008].
To date, however, the formally proved translation validators have not incorporated reasoning with
algebraic properties of arithmetic, as we found we needed in CryptOpt.
   In contrast, translation validation with SMT solvers uses rich reasoning to prove equivalence
between the high-level input program and the obtained low-level output. The Alive project [Lopes
et al. 2021] for LLVM is a good example. Compared to work with formally proved translation
validators, Alive and similar tools include much larger trusted bases, for instance including a full
SMT solver like Z3 [de Moura and Bjørner 2008]. Some SMT solvers have been extended to produce
proofs that can be checked in tools like Coq, as in SMTCoq [Armand et al. 2011].
   In our experience, these tools hit performance bottlenecks when working with large bitvectors.
Even if we imagine those issues as fixed some day, there are still benefits to creating a customized
checker, keeping just the relevant aspects of SMT. A benefit of a slimmed-down custom prover is
that it becomes more feasible to prove the prover itself, rather than just a checker for its outputs,
which improves performance and reduces surprise from proof-generation bugs.

2.5   The E-graph
Following SMT-solver conventions [Detlefs et al. 2005], our E-graphs include nodes for equivalence
classes of symbolic expressions, in addition to the edges representing subterm relationships. Each
6                   Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


node is configured to present the most compact representation of its equivalence class. For instance,
whenever a node becomes provably equal to a constant, it is labeled with that constant, without
outgoing edges. When a node is most succinctly expressed as a sum, it is labeled with a “+” operator
and has edges to the other nodes being added.
   Figure 2 animates a sim-
ple example. It steps through      1       Add: 𝑥 + 𝑧 + (𝑦 ≫ 9) + 𝑦            2       Add: 𝑥 + 𝑧 + (𝑦 ≫ 9) + 𝑦
stages of adding a new node
to the graph, representing the            2: +(0, 1)      3: 𝑧      5:≫ (1, 4)        2: +(0, 1)        3: 𝑧    5:≫ (1, 4)
                                            𝑥 +𝑦                      𝑦 ≫9              𝑥 +𝑦                      𝑦 ≫9
new symbolic expression: (𝑥 +
𝑧 + (𝑦 ≫ 9) + 𝑦). Step 1 shows       0: 𝑥            1: 𝑦                 4: 9   0: 𝑥            1: 𝑦                 4: 9
the initial state. Nodes 2 and 5
                                                                                               6: +(0, 1, 3, 5)
are labeled with operators and     3       Add: 𝑥 + 𝑧 + (𝑦 ≫ 9) + 𝑦            4           𝑥 + 𝑧 + (𝑦 ≫ 9) + 𝑦
IDs of operands. To process the                                                         Add:
                                          2: +(0, 1)                5:≫ (1, 4)        2: +(0, 1)                5:≫ (1, 4)
expression we are evaluating,               𝑥 +𝑦          3: 𝑧        𝑦 ≫9              𝑥 +𝑦
                                                                                                        3: 𝑧      𝑦 ≫9
we first look up existing graph      0: 𝑥            1: 𝑦                 4: 9   0: 𝑥            1: 𝑦                 4: 9
nodes for all of its leaf expres-
sions, as Step 2 shows. Then we
proceed bottom-up in the ex-
                                        Fig. 2. Example of operations on an E-graph-style structure
pression tree, finding an exist-
ing node or building a new one
for each subexpression. In this case, we next need to find a node for 𝑦 ≫ 9, in Step 3. As we
resolved 𝑦 to node 1 and 9 to node 4, we are able to search the DAG for a node already labeled
with operator ≫ and argument nodes 1 and 4, finding node 5. In the final step, Step 4, we need
to find a node for 𝑥 + 𝑧 + (𝑦 ≫ 9) + 𝑦. We have node IDs for all four operands of addition, and
we sort them by ID, taking advantage of associativity and commutativity of addition, to find a
canonical description of this node. No existing node has that description, so we add a new one.
The main complication absent from this example is normalization with rewrite rules going beyond
associativity and commutativity; the approach is parameterized on a set of such rules (which must
have proofs in Coq), and they are applied as each node of the input AST is processed.

3     RELATED WORK
With CryptOpt we combine several known techniques to generate fast and formally verified code.
We now sketch related work in the areas of genetic improvement (GI), optimal optimization pass
finding for off-the-shelf compilers, superoptimization, peephole optimization, translation validation
and computer-aided cryptography.

3.1    Genetic Improvement
CryptOpt applies GI, an area within search-based software engineering [Harman and Jones 2001]
that automatically searches out improved software versions. Genetic improvement is a relatively
young research field; its first survey appeared in 2018 [Petke et al. 2018]. Despite its youth, GI has al-
ready had real-world impact: maintainers have accepted GI patches into both open-source [Langdon
et al. 2015] and commercial [Haraldsson et al. 2017] projects.
   CryptOpt utilizes GI in the code-generation phase to generate fastest code per-microarchitecture.
To the best of our knowledge, CryptOpt is the first automatic compiler to offer both this level of
microarchitecture-tuned performance (albeit for the limited domain of straight-line crypto code)
and the highest level of formal assurance (Coq verification of all compiler phases that matter for
soundness). However, related work has tackled some of the constituent challenges.
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives             7


   Bosamiya et al. [2020] is most similar to CryptOpt as they also use GI to find fast code per-
architecture while being provably correct. The primary objective is to parse optimized x86-64 assem-
bly and then use verified transformations to transform it back into a clean form, which is then easier
to reason about. From those transformations, they selected the “prefetch insertion” and “instruction-
reordering” transformations and conducted a case study on using GI to find fast implementations
based on OpenSSL’s AES-GCM (which uses AES-NI instructions). Their approach can improve the
performance of existing code and verify the correctness of the produced code. Their starting point is
handwritten assembly code within a relatively shallow metaprogramming framework. In contrast,
we show that randomized search can be used as part of a fully automated pipeline that starts from
high-level functional programs, allowing us to generate fast code for multiple elliptic curves, not
just multiple target architectures from a single algorithm for Bosamiya et al. Generating the code
allows CryptOpt additional flexibility, with support for optimizing register allocation (in particular
spills to memory) and instruction selection. For example, using their reordering transformation,
they cannot substitute an add-using-overflow adox for an add-using-carry adcx, let alone have
those calculate two independent additions in parallel, because they only consider reads and writes
to the flag register in general, rather than the granularity of individual flags (i.e. read CF, write OF
are independent). CryptOpt also benefits from compatibility with Fiat Cryptography, which makes
code generation for finite fields for new primes easy.

3.2   Optimization-Pass Finding
Stephenson et al. [2003] and Peeler et al. [2022] both use GI to select and order existing optimization
passes of off-the-shelf compilers for optimal running time, where the former uses a simulated
running time (Trimaran [Chakrapani et al. 2005]) as the objective function and the latter uses the
actual running time. CryptOpt, however, is not bound by either applying or not applying those
fixed optimization passes from off-the-shelf compilers. Rather, it explores many different variations
for any particular code section and is also able to apply optimizations selectively at certain locations
and avoid using them at others.

3.3   Superoptimization
Massalin [1987] coined the term “superoptimizer” to describe a tool for exhaustive enumeration of
all possible programs to implement a given function. The key idea making this feasible is the use of
a probabilistic test set, which rejects the majority of incorrect candidates. At the time of writing, it
is able to generate programs of 12 instructions after several hours of running (on a 16MHz 68020
computer). Sasnauskas et al. [2017] present Souper, a tool to synthesize new optimizations on
the LLVM IR. Working on the IR, by design, they are unable to generate optimizations to exploit
target-specific code sequences.
   Joshi et al. [2002] present Denali, a superoptimizer for very short programs. They model the
architecture of their processor (Alpha EV6) and use solvers to reject conjectures of the form
“No program can compute 𝑃 in at most 8 cycles.” Combining this framing with a binary-search
algorithm, they end up with the most efficient program. Schkufza et al. [2013] present STOKE, a
superoptimizer which is able to synthesize and optimize programs. It combines correctness indicator
and performance into a cost function and then randomly (1) changes opcodes, (2) changes arguments,
(3) deletes instructions, and (4) inserts nops. By starting from scratch, they can find algorithmically
different solutions, which cannot be found by other superoptimizers. The resulting programs range
up to tens of instructions long. Subsequent work extends STOKE to optimize floating-point kernels
[Schkufza et al. 2014], optimize loops [Sharma et al. 2013], and more aggressively optimize kernels
based on verified runtime preconditions with cSTOKE [Sharma et al. 2015].
8                Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


   While CryptOpt shares the idea of a randomized search with superoptimization approaches,
there are a few important differences between the two. First, superoptimization approaches, and in
particular STOKE, apply random changes to existing code, whereas CryptOpt aims to generate
the code from a high-level specification. Moreover, unlike superoptimization, CryptOpt only uses
semantics-preserving approaches. This significantly reduces the search space, allowing CryptOpt
to handle functions with hundreds and even thousands of instructions. As shown in Section 7.4,
superoptimizers tend to fail on the inputs that CryptOpt processes. Finally, superoptimizers tend
to use a model of the hardware for which they optimize the code. CryptOpt, in contrast, optimizes
to the actual hardware, allowing it to adapt to new hardware without the need to model the
microarchitecture of the new hardware.

3.4   Peephole Optimization
Peephole optimizers use a sliding window on instructions (the peephole) and replace sets of instruc-
tions with more performant instructions [Aho et al. 1986; Bergmann 2003; Cooper and Torczon
2012]. The replacement is usually done based on a predefined rule set (applying only to short
instruction sequences), which itself is based on heuristics for estimating which set of instructions
is shorter or more performant. Yet another approach is to find and learn good peephole optimiza-
tions automatically: Bansal and Aiken [2006] use machine-learning techniques to characterize
small sections of code. Then, based on those characteristics, they replace a code sequence with
a semantically equivalent one assumed to be more performant. While they only focus on small
sections (on the order of tens of instructions), Pekhimenko and Brown [2010] use machine-learning
techniques to characterize entire methods and then apply certain optimization transformations to
them. Similarly, CryptOpt considers the entire function as a whole, but rather than characterizing,
learning and applying that knowledge to new functions, CryptOpt considers each architecture and
function as a black box and eventually finds a fast implementation.

3.5   Verified Transformations
Instead of proving the correctness of the compiler, translation validation [Pnueli et al. 1998]
does not trust the compiler but verifies that the compiled code preserves the semantics of the
source. Bosamiya et al. [2020], as already mentioned, used their tool to transform optimized
(manually written) assembly code to easily verifiable code. Similarly, TInA [Recoules et al. 2019]
lifts inline assembly to semantically equivalent C code amenable to verification with known
tools. Only targeting the code for Curve25519, Schoolderman et al. [2021] used the Why3 proving
platform [Filliâtre and Paskevich 2013] to verify an 8-bit AVR implementation.
   CryptoLine [Chen et al. 2014; Fu et al. 2019; Polyakov et al. 2018; Tsai et al. 2017] is an automatic
verification engine utilizing SMT solvers (BOOLECTOR) and computer-algebra systems (Singular),
applying to their own IR. The approach to validating assembly files is similar to ours. CryptoLine
has only worked via unverified translators from assembly languages to their IR, and the translator
must be trusted, unlike ours, though it likely accepts some correct programs that ours rejects.
   Last, Sewell et al. [2013] go further and parse the binary code of the seL4-Linux microkernel and
transform it until they could prove equivalence to the already-verified C code.
   We would like to emphasize that those works aim to verify existing implementations, whereas
CryptOpt generates them. Targeting a wide range of microarchitectures for performance optimiza-
tions manually would quickly become practically infeasible.

3.6   Real-World Applications of Computer-Aided Cryptography
Provably correct generated code is already deployed in important projects: all major web browsers
use finite-field code generated by Fiat Cryptography [Erbsen et al. 2019] (via Google’s BoringSSL and
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives            9


other libraries), and Firefox includes routines arising from the more comprehensive efforts of Project
Everest [Bhargavan et al. 2017b], including compilation of nonstraightline code to C [Protzenko
et al. 2017], verified metaprogramming of assembly [Fromherz et al. 2019], tying it together in
the EverCrypt library [Protzenko et al. 2020], and even adding protocol verification [Bhargavan
et al. 2017a]. The Everest stack supports many different algorithms for the same functionality
(e.g. AES+GCM or ChaCha20+Poly1305 for authenticated encryption) and for each of those many
different hand-optimized implementations depending on platform and hardware. We already
mentioned the work of Bosamiya et al. [2020] on automatic program search, the only approach to
automatic assembly generation that we have seen in the Everest ecosystem, and it does not seem to
have been applied yet to elliptic curves. CryptOpt also has the usual advantage of proof-assistant
work, that, despite our usage of a stack of domain-specific tools, none of them need be trusted.
   Belyavsky et al. [2020] published work on generating prime-agnostic point arithmetic in C using
verified field arithmetic from Fiat Cryptography and claim timing-side-channel-resistant code;
however, there is no formal verification of correctness or constant time.

4   CRYPTOPT OVERVIEW
Our aim is to strengthen Fiat Cryptography to both increase the performance of the produced code
and to decrease the size of the trusted code base. To that end, we implement two novel components
and integrate them with Fiat Cryptography as sketched in Figure 1.
   The first component, the CryptOpt optimizer, is a new backend for Fiat Cryptography, which
ingests Fiat IR and produces x86-64 assembly code. A unique and novel property of the optimizer
is that instead of relying on classic compiler-optimization techniques, it draws on techniques from
the domain of evolutionary computation. Specifically, as illustrated in Figure 3, the CryptOpt
optimizer first randomly generates x86-64 assembly code that implements the input function. It
then repeatedly mutates the code and measures the execution time of both the original and the
mutated code, discarding the slower one. The process continues until a predefined computational
budget is used up.
   The second component is a new program-equivalence checker,
which, given an original Fiat IR program and its optimized assem-                   Generate
bly, is able to verify behavior preservation with no further hints (c.f.          Initial Code
Figure 1). It is codesigned with the CryptOpt optimizer to support
the same set of transformations, significantly reducing the complex-                 Mutate
ity compared to a generic equivalence checker. The checker itself
is implemented and verified in Coq. Thus, only Fiat Cryptography
and the checker are verified, whereas the optimizer itself need not                 Measure
be trusted. While not trusted, the optimizer is designed to only use
semantics-preserving transforms. Thus, during normal operation,
we expect verification always to succeed.
   The combination of these two components allows us to achieve                      Worse      No
                                                                                  Performance?
our aims. As we demonstrate, random search can generate code that
performs as well as hand-optimized code, significantly surpassing
the performance of compiler-produced code. At the same time,                              Yes
the formally verified checker strengthens the unified theorems of                    Revert
                                                                                   Mutation
compilation to cover the whole span from functional programs to
x86-64 assembly instead of Fiat IR, removing the compiler from
the trusted code base.                                                   Fig. 3. Optimizer system archi-
   While designed as a backend for Fiat Cryptography, CryptOpt tecture
can operate as a stand-alone optimizer. To demonstrate this use
10                 Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


case, we transform a C implementation of field arithmetic to LLVM IR using Clang. (Specifically,
we use the C implementation of the Bitcoin libsecp256k1 library.) We then use a simple script to
translate the LLVM IR to the input format of CryptOpt and optimize it. Because the C code we use
is not formally verified, we skip the formal-verification aspect in this use case, focusing just on
further evaluation of the randomized optimizer.
   Finally, we note that the generated code from Fiat Cryptography utilizes neither secret-dependent
memory accesses nor secret-dependent branching. Consequently, the code follows the constant-
time programming paradigm [Almeida et al. 2016], providing protection against microarchitectural
side-channel attacks [Ge et al. 2018].
   Now we are ready to fill in the details of CryptOpt (randomized search in Section 5 and equiva-
lence checking in Section 6) and how we evaluated it (Section 7).

5     RANDOMIZED SEARCH FOR ASSEMBLY PROGRAMS
The first half of our approach is the CryptOpt optimizer, which generates highly performant x86-
64 assembly code that implements an input Fiat IR function. A unique feature of CryptOpt is that
instead of relying on heuristics for generating the code, CryptOpt explicitly casts the problem as a
combinatorial optimization problem. That is, we observe that searching the set of assembly code
sequences that implement a given input function is discrete. Hence, the problem of searching this
set for the assembly code sequence that minimizes execution time is a combinatorial optimization
problem.
   For optimization, we employ the RLS strategy with the Bet-and-Run heuristics. Recall that for
RLS, we need to first choose a random solution and then repeatedly mutate the solution. While
RLS is a relatively simple approach for combinatorial optimization, we find that it is effective and,
as we show below, achieves good results. We leave the task of experimenting with more complex
optimization strategies to future work. In the rest of this section we present our approach for
generating and mutating solutions. We start with a description of the input format and then explain
how we generate and mutate code.

5.1    Input Format
Recall (Section 4) that CryptOpt takes Fiat IR as
                                                         Variable 𝑥
an input. This intermediate language is truly a Binary integer 𝑏
minimal one (see Figure 4), with the only note-         Operand   𝑒 ::= 𝑥 | 𝑏
                                                        Operator 𝑜     ::= ! | & | ∗ | + | − | << | = | >> | ∼ |
worthy syntactic twist being that integer con-                              or | addcarryx | cmovznz | mulx |
stants are presented as binary numbers (clearly                             static_cast | subborrowx
                                                      Expression 𝐸 ::= return 𝑒 | 𝑥, . . . , 𝑥 ← 𝑜 (𝑒, . . . , 𝑒); 𝐸
indicating bitwidth), though we will often ab-
breviate them in decimal form, when bitwidth                        Fig. 4. Fiat IR syntax
is clear from context. Operators may in general
take not just multiple operands but also generate multiple results, associated with less common
operators like addition with carry or multiplication producing double-wide results via two output
words.
   Input programs contain no branches or explicit memory accesses, just accesses of local variables.
As a result, generated assembly programs will not be too much more complex, avoiding all memory
aliasing and restricting pointer expressions to be constant offsets of either function parameters (for
data structures passed by reference) or the stack pointer (for spilled variables). The assembly we
generate is timing-secure for the same reasons that Fiat IR is timing-secure; we only use primitive
program mutations that either preserve relevant behavior (the trace of program memory accesses
and control-flow decisions) or add new behaviors in ways independent of secrets (all memory
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives                    11


accesses are to constant offsets from either the stack pointer or arrays that are function parameters),
so by induction the initially secure programs are still secure after optimization.
   Algorithm 1 shows a Fiat IR pro-
gram, which we will use through- Algorithm 1: An Ex-
                                                                                       𝑋       𝑌          𝑍

out this paper as a running exam- ample Function                                                Add1    Mul1

ple. The program takes three in-         input : 𝑋 , 𝑌 , 𝑍 such that 0 ≤                         𝑡0   𝑡2 𝑡1
                              2                     𝑋 , 𝑌 , 𝑍 < 263                     Mul2
puts (𝑋, 𝑌 , 𝑍 ) and outputs 𝑍 +(𝑌 +     output : 𝑂 = 264𝑂 1 + 𝑂 0 =                𝑡4      𝑡3
𝑍 ) · 𝑋 + 𝑍 using two types of op-                  𝑍 2 + (𝑌 + 𝑍 ) · 𝑋 + 𝑍                              Add2
erations: Add and Mul. The oper-         function example(𝑋 , 𝑌 , 𝑍 )                                 𝑐 0 𝑡5
                                         begin                                          Add4            Add3
ation Add adds two 64-bit num-                𝑡 2 , 𝑡 1 ← Mul1 (𝑍, 𝑍 )
bers and one 1-bit carry, then re-           𝑐 ∅ , 𝑡 0 ← Add1 (𝑌 , 𝑍, 0)           𝑡 6                𝑐 1
                                              𝑡 4 , 𝑡 3 ← Mul2 (𝑡 0 , 𝑋 )               Add5
turns the sum as one 64-bit num-              𝑐 0 , 𝑡 5 ← Add2 (𝑡 3 , 𝑡 1 , 0)
ber and one 1-bit carry. The op-              𝑐 1 , 𝑂 0 ← Add3 (𝑡 5 , 𝑍, 0)              𝑂1               𝑂0
                                             𝑐 ∅ , 𝑡 6 ← Add4 (𝑡 4 , 𝑡 2 , 𝑐 0 )
eration Mul multiplies two 64-bit            𝑐 ∅ , 𝑂 1 ← Add5 (𝑡 6 , 0, 𝑐 1 )
numbers, then returns the 128-bit              return 𝑂 1 , 𝑂 0                  Fig. 5. Data flow of the running
                                         end
product as two 64-bit words. For                                                 example in Algorithm 1
simplicity, we assume that the ar-
guments are in the range 0 ≤ 𝑋, 𝑌 , 𝑍 < 263 , allowing us to ignore some carries known to be 0. We
mark these carries with 𝑐 ∅ .
   In the absence of memory aliasing and control flow, the restrictions on operation evaluation
order in the programs we optimize are captured by the data flow. Figure 5 shows the data-flow
graph of the code in Algorithm 1.

5.2   Code Generation
The process of generating those assembly candidates can be under-
                                                                                       Mul1
stood as split between instruction scheduling, instruction selection,
and register allocation, in that order. Each phase makes certain arbi-
trary decisions that may be changed by a later random mutation. We                     Add1
summarize the phases here before returning to details of generation              𝑡1      𝑡0
and mutation.                                                                          Mul2
   First, for instruction scheduling (see Section 5.3), we use data-flow                         𝑡4 𝑡2
                                                                                         𝑡3
analysis to determine the data-flow dependencies between opera-
tions and choose a random topological order of the dependency                          Add2
graph as the initial order of operations in the code. Then, for in-                      𝑡5
struction selection (see Section 5.4), each operation gets assigned             𝑐0     Add3
a compatible x86-64 assembly instruction template. Finally, in our
setting, register allocation (see Section 5.5) arises mostly in ensuring        𝑐1     Add4
compatibility with operand restrictions of the instruction templates
                                                                                         𝑡6
that were selected. For example, consider the objective to multiply
two values (one single instruction can at most read from one mem-                      Add5
ory location), in a context where both operands reside in memory.
                                                                               Fig. 6. One ordering. Round
The relevant dimension of freedom is which value to load into a                rectangles show the operations,
register explicitly and into which register. After the decisions of the        which are evaluated top-down.
three phases have been recorded, it is easy to read off the chosen             Arrows indicate creation and
assembly program sequentially. Recall that all of these decisions              consumption of intermediate
may be revisited later in random mutations.                                    values. Vertical bars show the
   To present details of the three phases, we focus on the example             intervals in which an operation
program from Algorithm 1. Figure 6 shows how operations are                    can be scheduled.
12               Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


initially ordered and potential scheduling intervals; the mutations are shown in Figure 7; until
finally we see the emitted code with and without the effects of the mutations in Figure 8. We will
reference those illustrations later as needed.

5.3   Instruction Scheduling
Thanks to the simplicity of Fiat IR, every variable is assigned              I                    II
exactly once in the straight-line programs that the CryptOpt
optimizer takes as input. Consequently, any operation can be              Mul1                  Mul1
evaluated whenever all its inputs have been computed. In the                      mulx      𝛽          mulx
example, Mul2 can be evaluated when 𝑡 0 and 𝑋 are computed.
                                                                          Add1                  Add1
                                                                                  adcx                  add
Initial Ordering. To create an initial ordering, the CryptOpt
optimizer simply computes a topological order of the data-                Mul2                  Mul2
flow graph. Figure 6 shows an example of an initial ordering                      mulx                 mulx
for our running example. We would like to emphasize that
                                                                          Add2                  Add2
the selection does not rely on any heuristic. While this initial                  add                   add
selection does affect the subsequent mutated ordering, our
mutation strategy guarantees that any possible ordering can be            Add3                  Add4
                                                                                  add                   add
reached from any initial random starting point via a sequence                              𝛼
of mutation steps.                                                        Add4                  Add3
                                                                                  add                   add
Mutation Step. An instruction-scheduling mutation step
randomly selects one operation in the current ordering. This              Add5                  Add5
                                                                                  add                   add
operation is moved to a randomly chosen location within the
interval where it would be valid to move: not before the last
assignment responsible for setting a variable that is used here        Fig. 7. I : Initial ordering of operations
as an operand, nor after the first assignment that reads the           (colored rounded rectangles) with at-
variable being set here. We begin with the ordering shown in           tached templates (black ellipses); II : Af-
Figure 6. The vertical colored bars indicate the intervals where       ter two mutations 𝛼 and 𝛽: mutation 𝛼
the respective operations can be scheduled. Step 𝛼 of Figure 7         in topological ordering, mutation 𝛽 in
shows the effect of moving Add4 up one position.                       instruction-template selection. Data-
   Selecting the position to move an operation to is biased to-        flow arrows omitted; dashed arrows
wards larger moves, i.e. further away from the initial position,       indicate mutations.
in an effort to minimize spills by minimizing distance between
computing a value and using it.

5.4   Instruction Selection
An important property of complex instruction sets such as x86-64 is that there can be multiple
alternative implementations for each high-level operation, each with slightly different semantics
and impact on the processor pipeline. To match machine instructions to operations, the CryptOpt
optimizer uses templates describing the possible implementations for each operation.
   Consider, for example, the Add operation, which can be implemented using multiple instructions,
such as add, adcx, or adc. Though semantically equivalent, these choices influence program state
differently. For instance, in the case of no input carry (Add1−3 ), implementing an Add operation
using an adcx instruction requires clearing the carry flag. The template of the adcx instruction
accounts for that and issues a clear-carry instruction (clc) before the adcx instruction, unless
CryptOpt determines that the carry is already clear. Lines 6 and 7 of Figure 8 show this choice for
Add1 .
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives                                 13


Initial Template Mapping. When creating the initial code, CryptOpt selects a random template
for each operation as an initial mapping. Figure 7 (I ) shows an example of a possible mapping of
templates to the operations of our example function. The figure indicates the operation Mul1 is
implemented using the mulx, Add1 uses adcx, and so forth.
Mutation Step. To mutate the instruction selection, CryptOpt chooses an operation at random
and replaces the template for that instruction with one alternative. Mutation 𝛽 in Figure 7 shows an
example of replacing the template for Add1 to use the add instruction instead of the original adcx.
Flag Spills. The series of additions Add2, . . . , Add5 show not only the influence of different
orderings on the resulting code but also how a template is used to handle flag spills. Consider
the code in Figure 8a where Add2 results in CF=𝑐 0 . Later on, Add3 needs to write its own CF=𝑐 1 .
Therefore, the current CF needs to be spilled (into another register). In this case, it does so with
setc dl (line 17). Similarly, Add4 then needs to spill 𝑐 1 (line 22) to avoid overwriting it with its 𝑐 ∅ .
    At this point (line 23), CryptOpt needs to add 1 ; 𝑡 , 𝑡 ← Mul (𝑍, 𝑍 )                  ; 𝑡 2 , 𝑡 1 ← Mul1 (𝑍, 𝑍 )
                                                               2 1          1
the values of three operands, i.e. 𝑡 4 + 𝑡 2 + 𝑐 0 . As 2 mov rdx, [Z]                      mov rdx, [Z]
                                                         3 mulx r8,
the x86-64 assembly language does not have 4                                r9, [Z]         mulx r8,         r9, [Z]

a single three-operand addition instruction, 5 ; 𝑐 ∅, 𝑡0 ← Add1 (𝑌 , 𝑍, 0) ; 𝑐 ∅, 𝑡0 ← Add1 (𝑌 , 𝑍, 0)
                                                         6 clc
CryptOpt first adds two operands together then 7 adcx rdx, [Y]                              add rdx, [Y]
adds the sum to the third one. Note that this 8
                                                         9 ; 𝑡 4 , 𝑡 3 ← Mul2 (𝑡 0 , 𝑋 )    ; 𝑡 4 , 𝑡 3 ← Mul2 (𝑡 0 , 𝑋 )
changes the evaluation order from 𝑡 4 + 𝑡 2 +𝑐 0 to 10 mov [rsp], r8 ; spill mov [rsp], r8 ; spill
(𝑡 2 +𝑐 0 ) +𝑡 4 . As the Add operation is associative 11
                                                        12
                                                           mulx r8,         rdx, [X]        mulx r8,         rdx, [X]

and commutative, any evaluation order main- 13 ; 𝑐 0, 𝑡5 ← Add2 (𝑡3, 𝑡1, 0)                 ; 𝑐 0 , 𝑡 5 ← Add2 (𝑡 3 , 𝑡 1 , 0)
tains correctness. The equivalence checker ac- 14       15
                                                           add r9,          rdx             add rdx, r9

counts for this change in evaluation order (see 16 ; 𝑐 1, 𝑂 0 ← Add3 (𝑡5, 𝑍, 0) ; 𝑐 ∅, 𝑡6 ← Add4 (𝑡4, 𝑡2, 𝑐 0 )
                                                        17 setc dl               ; dl ← 𝑐 0
Section 6.3).                                           18 add       r9,    [Z]             adc r8,          [rsp]
                                                              19 0 mov   [𝑂 ],   r9
Strength Reduction. Some of the templates 20
we use support limited forms of strength reduc- 21 ; 𝑐 ∅, 𝑡6 ← Add4 (𝑡4, 𝑡2, 𝑐 0 )
                                                  22 setc r9b            ; r9b ← 𝑐 1 ; 𝑐 1 , 𝑂 0 ← Add3 (𝑡 5 , 𝑍, 0)
tion. For example, we have templates to imple- 23 movzx rdx, dl
ment multiplication by a constant, including us- 25 add r8, rdx
                                                  24 add     rdx,    [rsp]              add rdx, [Z]
                                                                                        mov [𝑂 0 ], rdx
ing a left-shift operation (i.e. 𝑥 × 8 =⇒ 𝑥 ≪ 3), 26
                                                  27 ; 𝑐 ∅ , 𝑂 1 ← Add5 (𝑡 6 , 0, 𝑐 1 ) ; 𝑐 ∅ , 𝑂 1 ← Add5 (𝑡 6 , 0, 𝑐 1 )
a series of multiplications and additions (i.e. 28    movzx r9,      r9b
𝑥 × 5 =⇒ 𝑥 × 2 + 𝑥), or a combination thereof. 29 add r8, r9                            adc r8,        0
                                                  30 mov     [𝑂 1 ], r8                 mov [𝑂 1 ], r8
The final template selection is left to the opti-
mizer.                                            (a) Code from I (initial              (b) Code from II (code af-
                                                              code)                             ter two mutations)
5.5    Register Allocation
                                                              Fig. 8. Emitted assembly code. Highlighted lines show
The register-allocation step of CryptOpt effects from mutations.
achieves two aims. It must both decide which
values are assigned to registers and which registers to spill to memory when running out of registers.
CryptOpt uses randomized search for the former and a deterministic strategy for the latter.
Register Assignment. Registers need to be assigned in two main cases: when computing a new
value and when reading a value from memory, either from the input or following a register spill.
CryptOpt keeps track of the live registers, allocating a free register if one is available. If none
is available, CryptOpt spills the contents of a register to memory and uses the freed register. To
choose the register to spill, CryptOpt scans the future use of all registers and spills the register
whose next use is furthest based on the current operation order.
   For example, lines 10–11 in Figure 8 implement the Mul2 operation. (For this example, we
assume that the architecture only has three general-purpose registers: r8, r9, and rdx.) At this
14                  Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


Inductive REG := rax | rcx | (∗ ...65 omitted... ∗) | r15b.
Inductive AccessSize := byte | word | dword | qword.
Record MEM := { mem_bits_access_size : option AccessSize; mem_base_reg : option REG;
            mem_scale_reg : option (Z ∗ REG); mem_base_label : option string; mem_offset : option Z }.
Inductive FLAG := CF | PF | AF | ZF | SF | OF.
Inductive OpPrefix := rep | repz | repnz.
Inductive OpCode := adc | adcx | add | adox | and | bzhi | call | clc | cmovb | cmovc | cmovnz | cmp
 | db | dd | dec | dq | dw | imul | inc | je | jmp | lea | mov | movzx | mul | mulx | pop | push
 | rcr | ret | sar | sbb | setc | seto | shl | shlx | shr | shrx | shrd | sub | test | xchg | xor.
Record JUMP_LABEL := { jump_near : bool; label -name : string }.
Inductive ARG := reg (r : REG) | mem (m : MEM) | const (c : Z) | label (l : JUMP_LABEL).
Record NormalInstruction := { prefix : option OpPrefix; op : OpCode; args : list ARG }.


                              Fig. 9. Syntax of Coq embedding of x86-64 assembly


point, registers r8, r9, rdx have been used for 𝑡 2 , 𝑡 1 , and 𝑡 0 , respectively. Hence, the need to spill a
register. Observing that 𝑡 2 is not required until Add4 , whereas 𝑡 0 and 𝑡 1 are used earlier, CryptOpt
spills r8 (line 10).
Memory Loads. Most arithmetic operations in the x86-64 architecture support instruction formats
that take one argument from memory. When an argument of an operation is in memory, CryptOpt
tries to use such an instruction format. When this is not possible, e.g. when the values of two
arguments are in memory, CryptOpt resorts to loading a value from memory into a register. In the
case of associative operations, such as addition and multiplication, CryptOpt initially randomly
chooses the value to load, though mutations may later alter the choice.
Exploiting Simplicity. Finally, we note that the absence of control flow and avoidance of human
heuristics are key enablers for memory-spill decisions. The former simplifies dependency analysis,
allowing CryptOpt to determine the requirements for downstream operations. The latter allows
CryptOpt to examine the entire function rather than focusing on instructions within a peephole
window, a technique commonly used by off-the-shelf compilers.

5.6    Objective-Function Evaluation
We compare different random program variants by running them on the actual processors of
interest. Controlling noise in running-time measurement is of utmost importance because with too
much noise, randomized search could be driven into unproductive oscillation. We found the details
of such measurement surprisingly difficult to get right. Appendix A gives those details, which rely
on running a chosen number of repetitions of the two candidate programs, interleaved in a random
order, then returning the median timing observed per program.

6     CHECKING PROGRAM EQUIVALENCE
Our goal with CryptOpt was to preserve or even strengthen the formal guarantees of Fiat Cryp-
tography. One way to achieve that goal would have been to verify the whole randomized-search
process with Coq, but we wanted to find a simpler strategy that would have the side benefit of also
potentially supporting automatic verification of various handwritten assembly solutions. There-
fore, we decided to write a program-equivalence checker in Coq and verify it. Industrial-strength
translation validation as in Alive [Lopes et al. 2021] is now well-established, but again, proving
such a tool from first principles would be a substantial undertaking. We were curious, instead, how
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives           15


far we could get implementing (and proving) our checker from scratch, lifting just those features of
more conventional checkers that turned out to be important in our domain.
   Figure 9 shows a nearly complete description of the x86-64 assembly syntax accepted by our
checker. For better error messages, some control-flow opcodes like jmp are included, though they
will always be rejected by the checker. This type of syntax trees is given a very standard semantics,
in the form of an interpreter as a Coq function. The simplicity of syntax and semantics is important,
since both are referenced by the final theorem for any specific compilation, while the syntax and
semantics of Fiat IR drop out of the picture as untrusted.

6.1   Code Verification
The best-performing implementation produced by CryptOpt is assured to be correct through a
formally verified equivalence checker. Specifically, we verify the correctness of CryptOpt’s output
through functional equivalence between programs in the Fiat IR and x86-64 assembly. We developed
simple symbolic-execution engines for the relevant subsets of both languages, producing program-
state descriptions in a common logical format. The next task is to check that function-output
registers and memory locations store provably equivalent values between the two programs. To
that end, we developed a simple equivalence theorem prover that borrows from SMT solvers, using
a similar (E-graph) data structure.
   The public API connecting the checker’s two main components is based on the following
definition of expressions:
                              Integer constants 𝑛
                                      Variables 𝑥
                                     Operators 𝑜
                                   Expressions 𝑒         ::= 𝑛 | 𝑥 | 𝑜 (𝑒, . . . , 𝑒)
The E-graph exposes a function internalize that takes in an expression and returns a variable
now associated with that expression’s value. Importantly, the expression will usually mention
variables that came out of previous calls, which lets us work with exponentially more compact
representations than if we expanded out all variables. The internal E-graph takes advantage of this
sharing for efficiency. Also, crucially, every internalize invocation proactively infers equalities
between previously considered expressions and the new expression and its subterms. Thus, we
may check two expressions for equality simply by verifying that internalize maps them to the
same variable, which becomes a chosen representative of an equivalence class of expressions.

6.2   Symbolic Execution
We built symbolic-execution engines for the two relevant languages, Fiat IR and x86-64 assembly.
   The engine for the IR is simpler than for x86-64 assembly. Programs in this IR are just purely
functional sequences of variable assignments with expressions that effectively already match the
grammar we just gave. Thus, to evaluate such a program symbolically, we just maintain a dictionary
associating program variables to logical variables; the latter are effectively handles into the E-graph.
   The execution engine for x86-64 assembly is moderately more complicated. Now the symbolic
state associates not program variables but registers and memory addresses with logical variables. We
take advantage of the stylized structure of cryptographic code to simplify the treatment of memory.
The only valid pointer expressions are constant offsets from either function parameters (standing
for cells within data structures passed to the function) or the stack pointer (standing for spilled
temporaries). Thus, it is appropriate to make the symbolic memory a dictionary keyed off of pairs
of logical variables and integers. The logical variable is the base address of an array in memory,
while the integer gives a fixed offset into one of its words.
16                  Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


   With this convention fixed, it is fairly straightforward to march through the instructions in a
program, updating the register and memory dictionaries with the results of internalize calls. The
symbolic executor effectively breaks each (possibly complex) x86 instruction down into multiple
simpler operations on integers. There are multiple operations because many instructions affect
both flags and their explicit destination registers. The explanations of those effects are expressions
from the grammar above, using a relatively small vocabulary of bitvector operators.
   At the end of symbolic execution of an assembly function, we pull the output values out of
calling-convention-designated registers and memory locations. These can then be compared against
the explicit return value of a Fiat IR program. Both are expressed as logical variables connected to
a common E-graph, so they should be syntactically equal exactly when the E-graph found a proof
of equality. Importantly, both symbolic states are initialized with common logical variables.

6.3   Equivalence
Algorithm 2 presents the internalize algo-
rithm more generally. Without loss of gener- Algorithm 2: Internalize expression into
ality, we assume it is called on an expression the E-graph
                                                     input : Op an operator, Args its list of argument variables
that is an operator applied to a list of variables,  output : 𝑛 , a variable / graph node for the expression’s
which are used as E-graph node names. To                      equivalence class
internalize expressions with constants and/or        function internalize(Op, Args)
                                                     begin
deeper nesting of operands, we can simply tra-            if Op is associative then
verse their trees bottom-up, internalizing each                  for argument 𝑎 in Args do
                                                                       if 𝑎 is also labeled with Op then
node to obtain a variable (i.e. E-graph node) to                             Expand 𝑎 in the list into its own
replace it with. Elided from the figure are ad-                                E-graph neighbors
                                                                       end
ditional rewrite rules to complement the one                     end
we include, which notices that an operation to            end
extract the low byte of a constant is extraneous,         if Op has identity element e then
                                                                 Remove from Args any variable whose node is
when the constant is low enough. The algo-                         labeled with constant 𝑒 .
rithm ends in a linear scan of the E-graph for            end
                                                          if Op is LowByte and len(Args) = 1 and Args[0] is labeled
existing nodes matching the normalized input,               with a constant below 28 then
                                                                 return Args[0]
which perhaps surprisingly turned out to be               end
more than fast enough for our examples.                  /* Many other algebraic rewrite rules */
   The actual implementation includes a gen-              if Op is commutative then
                                                                 Sort Args by textual variable name.
eral range analysis to establish upper bounds             end
on variable nodes based on bounds on their in-            for node 𝑛 in the E-graph do
                                                                 if n is labeled with Op and has Args as its edge list
puts. This feature is used to elide truncations                    then
whenever appropriate and to gate other rewrite                         return n
                                                                 end
rules: for example, the carry bit resulting from          end
adding small numbers is always 0, and a sum              𝑛 ← new E-graph node;
of a couple of carry bits fits in a byte.                𝑛.label ← Op;
                                                         𝑛.edges ← Args;
   Here it is interesting to note which standard          return 𝑛
features of SMT-based verification tools did not     end

need to be implemented, saving us from need-
ing to prove their soundness. We incorporated no SAT-style management of case splits, nor did
we need to include specialized cooperating decision procedures for domains like arithmetic on
mathematical integers or bitvectors. It sufficed to stick to congruence-closure-style reasoning in
the theory of equality with uninterpreted functions, augmented with a modest pool of rewrite
rules, as SMT solvers are also often effective at applying. Note also that we omitted a central
complexity of E-graph implementations: merging nodes (usually through union-find algorithms)
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives        17


as it is discovered that they are equal. Our domain is simple enough that relevant equalities are
always discovered at node-creation time. As for symbolic execution, we avoided the characteristic
complexities of control flow (e.g. merging logical states) and memory access (e.g. flexible-enough
addressing that pointer aliasing is nontrivial to check).

6.4    Proof
We proved the Coq implementation of equivalence checking correct, in the sense that symbolically
executing an assembly (or IR) program produces an expression (E-graph) that would evaluate to
the same output as the original program from all starting states. A fairly direct corollary is our
main theorem: if two programs are symbolically executed with the same (symbolic) inputs and
produce outputs that are represented by the same E-graph nodes, then the programs are equivalent.
We combine the Fiat IR symbolic evaluator with the larger Fiat Cryptography pipeline, and we
verify it against the existing semantics of the IR, before extracting the pipeline to a command-line
program. That program takes as input a choice of cryptographic algorithm, its numeric parameters,
and an assembly file, and it checks that the assembly file matches the behavior of the algorithm, by
comparing it with the Fiat IR code (itself generated by a verified compiler).
   It is important that the top-level theorem of the equivalence checker avoids mentioning any
specifics of symbolic execution or E-graphs, as those are relatively complex techniques. Instead,
that theorem refers only to formal semantics of Fiat IR and x86-64 assembly. Slightly more precisely,
we depend on the following preconditions, several of which we formalize using notations borrowed
from separation logic [Reynolds 2002].
     • Calling-convention-designated registers hold input values, input-array base pointers, and
        output-array base pointers.
     • Input-array base pointers point to arrays in memory holding input values.
     • Output-array base pointers are valid.
     • rsp points to the end of the stack, which must be valid.
Then the main theorem concludes the following postconditions.
     • Input-array base pointers are still valid.
     • Output-array base pointers point to arrays in memory holding the output values.
     • The stack base-pointer address is still a valid pointer to an array of the right size.
     • Callee-save registers have the same values as before the code execution.
     • All other memory is untouched.
   A few other concerns must be stated in the full theorem, including that all source-program initial
variable values fit in machine words, arrays are laid out contiguously (the symbolic-execution
engine allows more flexible specification of memory contexts), and every array has a start address
stored directly in a register.

7     PERFORMANCE EVALUATION
In this section, we evaluate the performance of code produced by CryptOpt. Specifically, we answer
four main questions:
   (1) How does optimization progress over time (Section 7.2)?
   (2) How does CryptOpt compare with traditional compilation (Section 7.3)?
   (3) Is CryptOpt optimization platform-specific (Section 7.5)?
   (4) How does CryptOpt-optimized code perform as part of a cryptographic implementation
       (Section 7.6)?
   We first describe the setup and the procedures we use for the evaluation. We then describe the
experiments we carry out and their results.
18                  Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


7.1     Experimental Setup
In this subsection, we describe the hardware platforms and discuss the generation of results through
optimization, plus the evaluation of which one is the best of all the results.
Hardware Platforms. To compare across multiple Table 1. Overview of target machines used in the
processor architectures, we evaluate CryptOpt on experiments
multiple hardware platforms, summarized in Table 1.
                                                             Name   CPU                        𝜇 -architecture
We did not observe differences in optimization be-
                                                             1900X  AMD Ryzen Theadr. 1900X Zen 1
havior on machines with SMT enabled or disabled.             5800X  AMD Ryzen 7 5800X          Zen 3
We use Ubuntu Server 22.04.1 LTS for all machines,           5950X  AMD Ryzen 9 5950X          Zen 3
                                                             7950X  AMD Ryzen 9 7950X          Zen 4
with all packages up-to-date. Moreover, because per-         i7 6G  Intel Core i7-6770HQ       Skylake-H
formance counters are not available on the efficiency        i7 10G Intel Core i7-10710U       Comet Lake-U
                                                             i9 10G Intel Core i9-10900K       Comet Lake-S
cores of the i9 12G and i9 13G, we only use the per-         i7 11G Intel Core i7-11700KF      Rocket Lake-S
formance cores on those machines.                            i9 12G Intel Core i9-12900KF      Alder Lake-S
                                                             i9 13G Intel Core i9-13900KF      Raptor Lake-S
Generation. Every platform has at least four phys-
ical cores. For a fair comparison, we run the same number of optimization processes in parallel on
all platforms. We pin the optimization processes to cores to reduce noise due to context switching.
We choose to run three optimizations in parallel, keeping one core free for general OS activity.
This results in three assembly files for each primitive per platform, of which we report only the
best-performing. The number of assembly instructions varies from 51 to 1281, depending on the
field, the operation, and how well the optimization went. See Table 2 for details.
Bet-and-Run. Each optimization process has a budget of 200 000 Table 2. Instruction count (average
mutations. In the bet stage, we explore 20 initial candidate so- over all eight platforms)
lutions, optimizing each for 1 000 mutations. Hence, overall, we
use 20 000 mutations, which are 10% of the total budget, for the           Primitive      Multiply Square
bet part. The remaining 180 000 mutations are used for the run             Curve25519 173.300 123.333
stage of the Bet-and-Run strategy. With those parameters, the              NIST P-224     226.967 222.233
generation and verification of all of the 18 Fiat IR primitives takes      NIST P-256     206.133 198.600
                                                                           NIST P-384     580.400 570.300
between 20 and 40 wall-clock hours, depending on the machine.              SIKEp434       968.333 927.833
Code Verification. When combined with Fiat Cryptography,                   Curve448       550.133 359.467
the optimization process verifies that the code it produces is             NIST P-521     575.233 359.233
equivalent to the Fiat IR code. We perform verification only on            Poly1305        73.333       55.633
                                                                           secp256k1      228.333 223.500
the final output of the optimization. Table 3 shows the time it
takes to verify one assembly implementation as an average over the ten platforms.
                                      Performance Metric. To compare the performance of differ-
Table 3. Verification times (average
over all ten platforms)
                                      ent implementations, we need a stable metric. To reduce system
                                      noise we fix the CPU frequency, disable boosting, and set the
                                      governor to performance. We note that we only apply these
   Primitive     Multiply Square
                                      settings when evaluating the performance but not during opti-
   Curve25519       0.29 𝑠   0.18 𝑠   mization. For more details on this aspect of our experimental
   NIST P-224       2.16 𝑠   1.94 𝑠
                                      setup, see Appendix A.
     NIST P-256     1.07 𝑠     0.95 𝑠
     NIST P-384    29.09 𝑠    25.81 𝑠
     SIKEp434     315.23 𝑠   284.32 𝑠
                                         7.2   Optimization Progress
     Curve448       3.02 𝑠     1.44 𝑠    The first evaluation question we answer is how the optimization
     NIST P-521     3.14 𝑠     1.46 𝑠    progresses over time. We include details in Appendix B, but a
     Poly1305       0.07 𝑠     0.06 𝑠
                                         summary is that optimization progress is roughly logarithmic
     secp256k1      1.78 𝑠     1.65 𝑠
                                         in the number of mutations, with some interesting differences
                                         in measurement stability across platforms.
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives          19


7.3   CryptOpt vs. Off-the-Shelf Compilers
To compare CryptOpt with traditional compilers, we use the implementations of finite-field arith-
 metic as produced by Fiat Cryptography. Specifically, we use Fiat Cryptography to produce
 implementations of the multiply and the square functions in nine fields. We consider prime fields
 of the standardized NIST P curves: Curve P-224, Curve P-256, Curve P-384 and Curve P-521 [NIST
 2000]. Moreover, we consider the field of the popular ‘Bitcoin’ curve secp256k1 [Certicom Re-
 search 2000], the high-speed de-facto standard Curve25519 [Bernstein 2006], and a high-security
 Curve448 [Hamburg 2015]. In addition to elliptic-curve cryptography, we apply our method to
 the underlying fields of the post-quantum scheme SIKEp434 [Azarderakhsh et al. 2019] and of the
 Poly1305 message-authentication scheme [Bernstein 2005]. It is worth noting that Erbsen et al.
 [2019] reported that their generated C code was roughly the best-performing available for all
 elliptic curves, up to the usual vagaries of C-compiler optimizers fluctuating in behavior across
versions, so it makes sense to use that C code as our performance baseline.
    We run CryptOpt on each of the ten platforms
                                                          Table 4. Geometric means of CryptOpt vs. off-
 summarized in Table 1 and select the best result
                                                          the-shelf compilers.
 as described in Section 7.1. Additionally, we com-
 pile the equivalent C code, as produced by Fiat
 Cryptography, with GCC 12.1.0 [GCC 2022] and                              Multiply         Square
 Clang 15.0.6 [Clang 2022]. We use the highest Curve                    Clang GCC       Clang GCC
 optimization level the compilers support and en- Curve25519 1.25 1.16                   1.18    1.17
 able native support using the compilation switches P-224                1.54    2.52    1.40    2.56
-march=native -mtune=native -O3.                          P-256          1.70    2.61    1.63    2.59
    Table 4 shows a summary of the results. For each P-384               1.45    2.49    1.37    2.51
 function the table presents the geometric mean per- SIKEp434            1.70    2.43    1.73    2.39
 formance gain of CryptOpt over GCC and Clang. Curve448                  1.19    0.98    1.07    1.05
The mean is calculated over the different platforms;      P-521          1.30    0.97    1.35    1.03
 see Table 6 in Appendix C for the full details.          Poly1305       1.12    1.22    1.11    1.26
    The table shows that CryptOpt achieves signifi-       secp256k1      1.80    2.62    1.71    2.54
 cant performance gains in the majority of functions.
The performance gains are somewhat more modest when the produced code does not require
 any memory spills, as is the case for operations in the fields of Curve25519 and Poly1305. For the
 large fields, as in P-521 and Curve448, CryptOpt is less successful, achieving modest gains for
 the square function compared to GCC and slightly underperforming for multiply compared to
 GCC. We note that the code produced for these curves is quite large. As an example, the resulting
x86-64 assembly files for Curve448-mul are in the range of 511–602 instructions and for P-521-mul
 509–648 instructions depending on the platform. For comparison, Curve25519-mul is in the order
 of 160–195 instructions and in the range of 66–83 for Poly1305-mul. We suspect that CryptOpt’s
 simple mutations have less impact on the execution time for those big functions than what would
 be needed to be measurable and direct the optimizer towards the optimal instruction sequences.
We leave more sophisticated genetic-improvement strategies for future work.
    We further evaluated the impact of profile-guided optimization (PGO) on the performance of
 code produced by the mainstream compilers. Specifically, we compiled the methods adding the
 profiling option ( -fprofile-generate in GCC and -fprofile-instr-generate in Clang). We
 then ran each function in a tight loop for 10 000 iterations with random input, generating profile
 traces. Lastly, to use the profile traces, we added the -fprofile-use switch (including one call to
 llvm-profdata merge to create the correct format and the switch -fprofile-instr-use when
20               Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


using Clang) to our compilation options. We then measured the performance of the code generated
from this last compilation.
   Using PGO with Clang only changes the position of the code for the Curve25519 and P-521 fields
and only results in negligible performance changes. Using PGO with GCC improves the mean
performance by ∼2% over the whole set of functions. Notably, PGO improves the performance of
the SIKEp434 operations by ∼15%. In all tested functions, CryptOpt significantly outperforms GCC
even when used with PGO.

7.4   CryptOpt vs. Superoptimization
To compare CryptOpt to superoptimizers, we use STOKE [Schkufza et al. 2013]. STOKE supports
two operation modes: synthesize, where it aims to generate new code that performs the function;
and optimize, where it attempts to modify a function to find a faster alternative. Synthesize mode
failed to generate correct code from scratch even though we let it run for more than three days.
This is expected because in synthesize mode, STOKE aims for small kernels, whereas functions for
finite-field arithmetic are on the order of hundreds of instructions.
   For the optimize mode, we compile our test functions with Clang 3.4 and GCC 4.9. (STOKE does
not support newer versions of these compilers.) We then try to optimize the assembly code that the
compilers emit.
   In four of the prime fields (Curve25519, Poly1305, P-448 and P-521), the code produced by the
compilers uses the shrd instruction, which is not supported in STOKE due to the potential for
undefined behavior. For the remaining fields, in most optimization attempts, STOKE either times out
or emits assembly code that contains either syntactical errors that prevent it from being assembled
or logical errors that result in incorrect code.
   We only managed to get results for the square function of secp256k1, when compiled with
GCC 4.9. When optimizing this function, STOKE produces code that is about 6% faster than the
output of compilation with GCC 11. However, the code is still 73% slower than the code that
CryptOpt produces for the same function.

7.5   Platform-Specific Optimization
CryptOpt optimizes the execution time of the function on the platform it executes on. Because
different platforms have different hardware components, the fastest code on one platform is not
necessarily the fastest on another. Surprisingly, sometimes it does pay off to optimize on a different
platform than the target, apparently when the host supports more stable performance measurement.
See Appendix C for details.

7.6   Scalar Multiplication
So far we have focused on the optimized functions in isolation. In this section, we investigate
the use of the field operations within the context of elliptic-curve cryptography. Specifically, we
investigate implementations of two popular elliptic curves: Curve25519 and secp256k1. We compare
the performance of 15 implementations of these curves, four of which use CryptOpt code for field
operations. In Table 5, we summarize the implementations we investigate.
State of the Art. For Curve25519, the SUPERCOP benchmark framework [Bernstein and Lange
2022] provides us with many implementations: sandy2x [Chou 2015], amd64-51 and amd64-64 [Chen
et al. 2014], as well as donna and donna-c64 [Langley 2022]. OpenSSL [OpenSSL 2022] provides three
implementations: a portable C implementation that we identify as O’SSL, and two assembly-based
implementations, based on amd64-51 and amd64-64, which we identify as O’SSL fe-51 and O’SSL
fe-64, respectively. At runtime, OpenSSL chooses which implementation to use, opting by default
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives      21


for O’SSL fe-64. Additionally, Project Everest [HACL 2022] provides an assembly implementation
in which the computations of two field operations are interleaved to achieve better utilization of
the CPU pipeline.
   For secp256k1, we use two implementations from the libsecp256k1 library [Bitcoin Core 2021],
one hand-optimized assembly and the other portable C.
CryptOpt-Based Implementations. For the com- Table 5. Performance of Scalar Multiplication
parison, we use four implementations with Crypt- (Geometric Mean).
Opt-optimized code. Specifically, for Curve25519,
we replace the field operations in O’SSL-fe51 and                       Curve25519
in O’SSL-fe64 with CryptOpt-optimized field op- Implementation                      Lang  Cycles
erations. We call these implementations O’SSL fe- sandy2x [Chou 2015]               asm-v  486k
51+CryptOpt and O’SSL fe-64+CryptOpt, respec- amd64-64 [Chen et al. 2014]           asm    542k
tively.                                               amd64-51 [Chen et al. 2014]   asm    546k
   For secp256k1 we use two implementations. The      donna [Langley 2022]          asm-v  972k
first, libsecp256k1+CryptOpt (Fiat), uses the scalar donna-c64 [Langley 2022]       C      577k
                                                      O’SSL [OpenSSL 2022]          C      530k
multiplication code from libsecp256k1 with the O’SSL fe-51 [OpenSSL 2022]           asm    530k
field operations as produced by Fiat Cryptography O’SSL fe-51+CryptOpt              asm    524k
and optimized with CryptOpt.                          O’SSL fe-64 [OpenSSL 2022]    asm    455k
   Additionally, to demonstrate the use of the Crypt- O’SSL fe-64+CryptOpt          asm    461k
                                                      HACL* fe-64 [HACL 2022]       asm    452k
Opt optimizer as a stand-alone tool, we use Clang
to compile the field operations of the portable                         secp256k1
implementation of libsecp256k1 into LLVM IR, Implementation                         Lang  Cycles
which we convert to the input format of the Crypt- libsecp256k1 [Bitcoin Core 2021] asm    547k
Opt optimizer. We then use the latter to opti- libsecp256k1 [Bitcoin Core 2021] C          530k
                                                      libsecp256k1+CryptOpt (Fiat)  asm    527k
mize the code, replacing the field operations with
                                                      libsecp256k1+CryptOpt (Opt)   asm    528k
the optimized code. This implementation is called
libsecp256k1+CryptOpt (Opt).
Evaluation. We use the SUPERCOP benchmark framework [Bernstein and Lange 2022] to measure
the performance of the evaluated implementations. For each implementation, SUPERCOP tries
multiple combinations of compilers and compiler options and reports the execution time (for two
base-point multiplications and two variable-point multiplications) of the fastest compiler setting.
We evaluate each implementation on the ten hardware platforms (c.f. Table 1) and report the
geometric mean (rounded to the nearest 1000 cycles) in Table 5. (See Table 7 in Appendix D for the
full details.)
Results. Comparing CryptOpt with the similarly structured hand-optimized implementations
of OpenSSL fe-51 and fe-64, we find that the performance with and without CryptOpt is similar.
On average, CryptOpt generates slightly faster implementations for fe-51 and slightly slower
implementations for fe-64. Manual optimization of code requires significant expertise and a large
time investment, which needs to be repeated for each finite field. In contrast, using CryptOpt is
fairly straightforward and only requires moderate computing resources to achieve similar results.
CryptOpt also underperforms highly optimized implementations that use a different API (HACL*),
which we do not support yet.
   For secp256k1, the libsecp256k1+CryptOpt (Fiat) implementation beats the performance of the
hand-tuned assembly, slightly outperforms the C compiled code, and provides verified formal
correctness. The libsecp256k1+CryptOpt (Opt) implementation achieves higher performance than
both the state-of-the-art and our verified implementation albeit slightly slower than the version
based on Fiat Cryptography.
22                 Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


  We leave the tasks of verifying the implementation for secp256k1 and emitting field operations
similar to the HACL* API to future work.
CryptOpt on New Hardware. When looking at the results on specific machines (Table 7),
we see that CryptOpt excels on the i7 11G, i9 12G, and i9 13G platforms, providing the overall
fastest implementations for fe-64-based field operations. On these platforms, CryptOpt-based
implementations of Curve25519 and secp256k1 are the fastest, outperforming hand-optimized
implementations, including those that use advanced processor features, such as vector instructions.
The 12𝑡ℎ generation of Intel processors is a major update of the microarchitecture. We believe that
CryptOpt’s automated search allows it to exploit the benefits of the new design automatically. In
contrast, prior implementations and mainstream compilers need to change to adapt to these new
features. We anticipate that in due course, implementations will be adapted to the new design,
and hand-tuned implementations will outperform CryptOpt. However, CryptOpt does not require
manual effort to adapt to new designs.

7.7    Artifacts
The artifact, on which the evaluation was done, is available at: https://zenodo.org/record/7710435,
with the DOI 10.5281/zenodo.7710435. The artifact includes instructions to reproduce the claimed
results in this paper. As of April 2023, the most up-to-date version of Fiat Cryptography can be
found in their repository at https://github.com/mit-plv/fiat-crypto, and up-to-date versions of
CryptOpt at https://github.com/0xADE1A1DE/CryptOpt.

8     CONCLUSION
We presented CryptOpt, a tool that brings a perhaps-surprising confluence of improving perfor-
mance and increasing formal assurance. It tackles the distinctive simplifications and complexities of
straight-line cryptographic code. We showed empirically that certain simplifications to established
techniques suffice to set new performance records for important routines on some relevant plat-
forms. In generation of fast code, we developed a simple set of transformation operators that make
genetic search effective. In checking of fast code with foundational mechanized proofs, we followed
SMT solvers and symbolic-execution engines, while avoiding their most complex aspects, like
arithmetic decision procedures or nontrivial pointer-aliasing checks. We hope that these techniques
can be generalized to other domains of compilation.

ACKNOWLEDGMENTS
Input from many anonymous reviewers has helped shaping this paper. We are grateful to all for
their work and valuable comments. In particular, we thank our shepherd, Yaniv David, for the
careful reading, guidance, and support.
   This research was supported by the Air Force Office of Scientific Research (AFOSR) under award
number FA9550-20-1-0425; the Australian Research Council projects DE200101577, DP200102364
and DP210102670; the Blavatnik ICRC at Tel-Aviv University; CSIRO’s Data61; the Deutsche
Forschungsgemeinschaft (DFG, Germany’s Excellence Strategy) under Germany’s Excellence Strat-
egy EXC 2092 CASA - 390781972; the National Science Foundation under grants CNS-1954712
and CNS-2130671; the National Science Foundation Expedition on the Science of Deep Specifica-
tion (award CCF-1521584); the Phoenix HPC service at the University of Adelaide; and gifts from
Amazon Web Services, AMD, Facebook, Google, Intel and the Tezos Foundation.
   Part of this work was carried out while Chitchanok Chuengsatiansup, Markus Wagner, and Yuval
Yarom were affiliated with the University of Adelaide, and while Chuyue Sun was affiliated with
the Massachusetts Institute of Technology.
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives                              23


REFERENCES
0xADE1A1DE. 2022. AssemblyLine v1.3.2. https://github.com/0xADE1A1DE/AssemblyLine 28
Alfred V. Aho, Ravi Sethi, and Jeffrey D. Ullman. 1986. Compilers: Principles, Techniques, and Tools. Addison-Wesley. 2, 8
Alaa R Alameldeen and David A Wood. 2003. Variability in architectural simulations of multi-threaded workloads. In HPCA.
   7–18. 26
José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, François Dupressoir, and Michael Emmi. 2016. Verifying Constant-
   Time Implementations. In USENIX Security. 53–70. https://www.usenix.org/conference/usenixsecurity16/technical-
   sessions/presentation/almeida 10
Michaël Armand, Germain Faure, Benjamin Grégoire, Chantal Keller, Laurent Théry, and Benjamin Werner. 2011. A Modular
   Integration of SAT/SMT Solvers to Coq through Proof Witnesses. In CPP. 135–150. 5
Anne Auger and Benjamin Doerr (Eds.). 2011. Theory of Randomized Search Heuristics: Foundations and Recent Developments.
   Series on Theoretical Computer Science, Vol. 1. World Scientific. 4
Reza Azarderakhsh, Matthew Campagna, Craig Costello, Luca De Feo, Basil Hess, Amir Jalali, Brian Koziel, Brian LaMac-
   chia, Patrick Longa, Michael Naehrig, Geovandro Pereira, Joost Renes, Vladimir Soukharev, and David Urbanik. 2019.
   Supersingular Isogeny Key Encapsulation – Submission to the NIST Post-Quantum Standardization Project, round 2.
   https://sike.org 19
Sorav Bansal and Alex Aiken. 2006. Automatic generation of peephole superoptimizers. In ASPLOS. 394–403. 8
Gilles Barthe, Benjamin Grégoire, and Vincent Laporte. 2018. Secure Compilation of Side-Channel Countermeasures: The
   Case of Cryptographic “Constant-Time”. In CSF. 328–343. 2
Dmitry Belyavsky, Billy Bob Brumley, Jesús-Javier Chi-Domínguez, Luis Rivera-Zamarripa, and Igor Ustinov. 2020. Set It
   and Forget It! Turnkey ECC for Instant Integration. In ACSAC. 760–771. 9
Seth D. Bergmann. 2003. Compilers. In Encyclopedia of Information Systems. 141–170. 8
Daniel J. Bernstein. 2005. The Poly1305-AES Message-Authentication Code. In FSE. 32–49. 19
Daniel J. Bernstein. 2006. Curve25519: New Diffie-Hellman Speed Records. In PKC. 207–228. 19
Daniel J. Bernstein, Tung Chou, and Peter Schwabe. 2013. McBits: Fast Constant-Time Code-Based Cryptography. In CHES,
   Vol. 8086. 250–272. 2
Daniel J. Bernstein, Chitchanok Chuengsatiansup, and Tanja Lange. 2014a. Curve41417: Karatsuba Revisited. In CHES.
   316–334. 2
Daniel J. Bernstein, Chitchanok Chuengsatiansup, Tanja Lange, and Peter Schwabe. 2014b. Kummer Strikes Back: New DH
   Speed Records. In ASIACRYPT. 317–337. 2
Daniel J. Bernstein, Chitchanok Chuengsatiansup, Tanja Lange, and Christine van Vredendaal. 2017. NTRU Prime: Reducing
   Attack Surface at Low Cost. In SAC. 235–260. 2
Daniel J. Bernstein and Tanja Lange. 2022. eBACS: ECRYPT benchmarking of cryptographic systems. http://bench.cr.yp.to/
   supercop/supercop-20221005.tar.xz 20, 21
Karthikeyan Bhargavan, Bruno Blanchet, and Nadim Kobeissi. 2017a. Verified Models and Reference Implementations for
   the TLS 1.3 Standard Candidate. In IEEE SP. 483–502. 9
Karthikeyan Bhargavan, Barry Bond, Antoine Delignat-Lavaud, Cédric Fournet, Chris Hawblitzel, Catalin Hritcu, Samin
   Ishtiaq, Markulf Kohlweiss, Rustan Leino, Jay Lorch, Kenji Maillard, Jianyang Pang, Bryan Parno, Jonathan Protzenko,
   Tahina Ramananandro, Ashay Rane, Aseem Rastogi, Nikhil Swamy, Laure Thompson, Peng Wang, Santiago Zanella-
   Béguelin, and Jean-Karim Zinzindohoué. 2017b. Everest: Towards a Verified and Drop-in Replacement of HTTPS. In Proc.
   SNAPL. https://project-everest.github.io/assets/snapl2017.pdf 9
Bitcoin Core. 2021. libsecp256k1 - Optimized C Library for ECDSA Signatures and Secret/Public Key Operations on Curve
   secp256k1. https://github.com/bitcoin-core/secp256k1/blob/9526874d1406a13193743c605ba64358d55a8785/src/field_
   5x52_int128_impl.h 3, 21, 32
Mahmoud A. Bokhari, Brad Alexander, and Markus Wagner. 2020. Towards rigorous validation of energy optimisation
   experiments. In GECCO. 1232–1240. 26
Mahmoud A Bokhari, Lujun Weng, Markus Wagner, and Bradley Alexander. 2019. Mind the gap - a distributed framework
   for enabling energy optimisation on modern smart-phones in the presence of noise, drift, and statistical insignificance.
   In IEEE CEC. 1330–1337. 26
Jay Bosamiya, Sydney Gibson, Yao Li, Bryan Parno, and Chris Hawblitzel. 2020. Verified Transformations and Hoare Logic:
   Beautiful Proofs for Ugly Assembly Language. In VSTTE. 106–123. 6, 8, 9
Christopher Celio, Palmer Dabbelt, David A. Patterson, and Krste Asanovic. 2016. The Renewed Case for the Reduced
   Instruction Set Computer: Avoiding ISA Bloat with Macro-Op Fusion for RISC-V. arXiv 1607.02318. 5
Certicom Research. 2000. SEC 2: Recommended elliptic curve domain parameters, version 1.0. http://www.secg.org/SEC2-
   Ver-1.0.pdf. 19
Lakshmi N. Chakrapani, John Gyllenhaal, Wen-mei W. Hwu, Scott A. Mahlke, Krishna V. Palem, and Rodric M. Rabbah.
   2005. Trimaran: An Infrastructure for Research in Instruction-Level Parallelism. In Languages and Compilers for High
24                  Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


   Performance Computing. 32–41. 7
Yu-Fang Chen, Chang-Hong Hsu, Hsin-Hung Lin, Peter Schwabe, Ming-Hsien Tsai, Bow-Yaw Wang, Bo-Yin Yang, and
   Shang-Yi Yang. 2014. Verifying Curve25519 Software. In CCS. 299–309. 8, 20, 21, 32
Tung Chou. 2015. Sandy2x: New Curve25519 Speed Records. In SAC. 145–160. 2, 20, 21, 32
Tung Chou. 2016. QcBits: Constant-Time Small-Key Code-Based Cryptography. In CHES, Vol. 9813. 280–300. 2
Chitchanok Chuengsatiansup, Michael Naehrig, Pance Ribarski, and Peter Schwabe. 2013. PandA: Pairings and Arithmetic.
   In Pairing, Vol. 8365. 229–250. 2
Chitchanok Chuengsatiansup and Damien Stehlé. 2019. Towards Practical GGM-Based PRF from (Module-) Learning-with-
   Rounding. In SAC. 693–713. 2
Clang. 2022. Clang: a C language family frontend for LLVM. https://clang.llvm.org 19
Keith D. Cooper and Linda Torczon. 2012. Chapter 11 - Instruction Selection. In Engineering a Compiler (Second Edition).
   597–638. 8
Charlie Curtsinger and Emery D. Berger. 2013. STABILIZER: statistically sound performance evaluation. In ASPLOS. 219–228.
   26
Leonardo Mendonça de Moura and Nikolaj S. Bjørner. 2008. Z3: An Efficient SMT Solver. In TACAS. 337–340. 5
David Detlefs, Greg Nelson, and James B. Saxe. 2005. Simplify: a theorem prover for program checking. J. ACM 52, 3 (2005),
   365–473. 3, 5
Benjamin Doerr and Frank Neumann. 2019. Theory of evolutionary computation: Recent developments in discrete optimization.
   Springer. 4
Vijay D’Silva, Mathias Payer, and Dawn Xiaodong Song. 2015. The Correctness-Security Gap in Compiler Optimization. In
   IEEE SP Workshops. 73–87. 2
Andres Erbsen, Jade Philipoom, Jason Gross, Robert Sloan, and Adam Chlipala. 2019. Simple High-Level Code for Crypto-
   graphic Arithmetic - With Proofs, Without Compromises. In IEEE SP. 1202–1219. 2, 3, 5, 8, 19
Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3 - Where Programs Meet Provers. In ESOP. 125–128. 8
Matteo Fischetti and Michele Monaci. 2014. Exploiting Erraticism in Search. Operations Research 62, 1 (2014), 114–122. 4
Aymeric Fromherz, Nick Giannarakis, Chris Hawblitzel, Bryan Parno, Aseem Rastogi, and Nikhil Swamy. 2019. A verified,
   efficient embedding of a verifiable assembly language. In POPL. 63:1–63:30. 9
Yu-Fu Fu, Jiaxiang Liu, Xiaomu Shi, Ming-Hsien Tsai, Bow-Yaw Wang, and Bo-Yin Yang. 2019. Signed Cryptographic
   Program Verification with Typed CryptoLine. In CCS. ACM, 1591–1606. 8
GCC. 2022. GCC, the GNU Compiler Collection. https://gcc.gnu.org 19
Qian Ge, Yuval Yarom, David Cock, and Gernot Heiser. 2018. A survey of microarchitectural timing attacks and counter-
   measures on contemporary hardware. J. Cryptogr. Eng. 8, 1 (2018), 1–27. 10
HACL. 2022. HACL. https://github.com/hacl-star/hacl-star 21, 31, 32
Mike Hamburg. 2015. Ed448-Goldilocks, a new elliptic curve. IACR Cryptology ePrint Archive 2015 (2015), 625. 19
Saemundur O. Haraldsson, John R. Woodward, Alexander E. I. Brownlee, and Kristin Siggeirsdottir. 2017. Fixing bugs in
   your sleep: how genetic improvement became an overnight success. In GECCO (Companion). 1513–1520. 6
Mark Harman and Bryan F. Jones. 2001. Software engineering using metaheuristic innovative algorithms: workshop report.
   Inf. Softw. Technol. 43, 14 (2001), 905–907. 6
Rodney E. Hooker and Collin Eddy. 2013. Store-to-load forwarding based on load/store address computation source
   information comparisons. US Patent 8533438. 5
Rajeev Joshi, Greg Nelson, and Keith H. Randall. 2002. Denali: A Goal-directed Superoptimizer. In PLDI. ACM, 304–314. 3, 7
Tomas Kalibera, Lubomir Bulej, and Petr Tuma. 2005a. Automated detection of performance regressions: The Mono experi-
   ence. In 13th IEEE International Symposium on Modeling, Analysis, and Simulation of Computer and Telecommunication
   Systems (MASCOTS). 183–190. 26
Tomas Kalibera, Lubomir Bulej, and Petr Tuma. 2005b. Benchmark precision and random initial state. In 2005 International
   Symposium on Performance Evaluation of Computer and Telecommunications Systems (SPECTS). 853–862. 26
Tomas Kalibera and Richard Jones. 2013. Rigorous benchmarking in reasonable time. ACM SIGPLAN Notices 48, 11 (2013),
   63–74. 26
Matthias J. Kannwischer, Joost Rijneveld, and Peter Schwabe. 2019. Faster Multiplication in Z2𝑚 [𝑥 ] on Cortex-M4 to Speed
   up NIST PQC Candidates. In ACNS. 281–301. 2
Thierry Kaufmann, Hervé Pelletier, Serge Vaudenay, and Karine Villegas. 2016. When Constant-Time Source Yields
   Variable-Time Binary: Exploiting Curve25519-donna Built with MSVC 2015. In CANS. 573–582. 2
William B. Langdon, Brian Yee Hong Lam, Justyna Petke, and Mark Harman. 2015. Improving CUDA DNA Analysis Software
   with Genetic Programming. In GECCO. 1063–1070. 6
Adam Langley. 2022. Curve25519-donna. https://github.com/agl/curve25519-donna 20, 21, 32
Kevin M. Lepak and Mikko H. Lipasti. 2000. On the value locality of store instructions. In ISCA. 182–191. 5
Xavier Leroy. 2009. A Formally Verified Compiler Back-end. J. Autom. Reason. 43, 4 (2009), 363–446. 5
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives                               25


Xavier Leroy, Sandrine Blazy, Daniel Kästner, Bernhard Schommer, Markus Pister, and Christian Ferdinand. 2016. CompCert
   — A Formally Verified Optimizing Compiler. In ERTS. 5
Nuno P. Lopes, Juneyoung Lee, Chung-Kil Hur, Zhengyang Liu, and John Regehr. 2021. Alive2: bounded translation
   validation for LLVM. In PLDI. 65–79. 5, 14
Henry Massalin. 1987. Superoptimizer - A Look at the Smallest Program. In ASPLOS. ACM Press, 122–126. 7
Todd Mytkowicz, Amer Diwan, Matthias Hauswirth, and Peter F Sweeney. 2009. Producing wrong data without doing
   anything obviously wrong! ACM SIGARCH Computer Architecture News 37, 1 (2009), 265–276. 26, 28
NIST. 2000. FIPS PUB 186-2: Digital signature standard. 19
OpenSSL. 2022. OpenSSL. https://www.openssl.org/ 4, 20, 21, 32
Hannah Peeler, Shuyue Stella Li, Andrew N. Sloss, Kenneth N. Reid, Yuan Yuan, and Wolfgang Banzhaf. 2022. Optimizing
   LLVM Pass Sequences with Shackleton: A Linear Genetic Programming Framework. arXiv 2201.13305. 7
Gennady Pekhimenko and Angela Demke Brown. 2010. Efficient Program Compilation Through Machine Learning
   Techniques. In Software Automatic Tuning, From Concepts to State-of-the-Art Results. Springer, 335–351. 8
Justyna Petke, Saemundur O. Haraldsson, Mark Harman, William B. Langdon, David Robert White, and John R. Woodward.
   2018. Genetic Improvement of Software: A Comprehensive Survey. IEEE Trans. Evol. Comput. 22, 3 (2018), 415–432. 6
Amir Pnueli, Michael Siegel, and Eli Singerman. 1998. Translation Validation. In TACAS. 151–166. 8
Andy Polyakov, Ming-Hsien Tsai, Bow-Yaw Wang, and Bo-Yin Yang. 2018. Verifying Arithmetic Assembly Programs in
   Cryptographic Primitives (Invited Talk). In CONCUR (LIPIcs, Vol. 118). Schloss Dagstuhl - Leibniz-Zentrum für Informatik,
   4:1–4:16. 8
Jonathan Protzenko, Bryan Parno, Aymeric Fromherz, Chris Hawblitzel, Marina Polubelova, Karthikeyan Bhargavan,
   Benjamin Beurdouche, Joonwon Choi, Antoine Delignat-Lavaud, Cédric Fournet, Natalia Kulatova, Tahina Ramananandro,
   Aseem Rastogi, Nikhil Swamy, Christoph M. Wintersteiger, and Santiago Zanella Béguelin. 2020. EverCrypt: A Fast,
   Verified, Cross-Platform Cryptographic Provider. In IEEE SP. 983–1002. 9
Jonathan Protzenko, Jean Karim Zinzindohoué, Aseem Rastogi, Tahina Ramananandro, Peng Wang, Santiago Zanella
   Béguelin, Antoine Delignat-Lavaud, Catalin Hritcu, Karthikeyan Bhargavan, Cédric Fournet, and Nikhil Swamy. 2017.
   Verified low-level programming embedded in F*. Proceedings of the ACM on Programming Languages 1 (2017), 1 – 29. 9
Kishore Kumar Pusukuri, Rajiv Gupta, and Laxmi N Bhuyan. 2012. Thread tranquilizer: Dynamically reducing performance
   variation. ACM TACO 8, 4 (2012), 46. 26
Frédéric Recoules, Sébastien Bardin, Richard Bonichon, Laurent Mounier, and Marie-Laure Potet. 2019. Get Rid of Inline
   Assembly through Verification-Oriented Lifting. In 2019 34th IEEE/ACM International Conference on Automated Software
   Engineering (ASE). 577–589. https://doi.org/10.1109/ASE.2019.00060 8
John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In LICS. 17
Ronny Ronen, Alexander Peleg, and Nathaniel Hoffman. 2004. System and method for fusing instructions. US Patent
   6675376B2. 5
Raimondas Sasnauskas, Yang Chen, Peter Collingbourne, Jeroen Ketema, Jubi Taneja, and John Regehr. 2017. Souper: A
   Synthesizing Superoptimizer. CoRR abs/1711.04422 (2017). 7
Eric Schkufza, Rahul Sharma, and Alex Aiken. 2013. Stochastic superoptimization. In ASPLOS. ACM, 305–316. 3, 7, 20
Eric Schkufza, Rahul Sharma, and Alex Aiken. 2014. Stochastic optimization of floating-point programs with tunable
   precision. In PLDI. ACM, 53–64. 7
Marc Schoolderman, Jonathan Moerman, Sjaak Smetsers, and Marko C. J. D. van Eekelen. 2021. Efficient Verification of
   Optimized Code - Correct High-Speed X25519. In NFM. 304–321. 8
Thomas Arthur Leck Sewell, Magnus O. Myreen, and Gerwin Klein. 2013. Translation validation for a verified OS kernel. In
   PLDI. 471–482. 8
Rahul Sharma, Eric Schkufza, Berkeley R. Churchill, and Alex Aiken. 2013. Data-driven equivalence checking. In OOPSLA.
   ACM, 391–406. 7
Rahul Sharma, Eric Schkufza, Berkeley R. Churchill, and Alex Aiken. 2015. Conditionally correct superoptimization. In
   OOPSLA. ACM, 147–162. 7
Mark Stephenson, Una-May O’Reilly, Martin C. Martin, and Saman P. Amarasinghe. 2003. Genetic Programming Applied to
   Compiler Heuristic Optimization. In EuroGP. 238–253. 7
Samantika Subramaniam and Gabriel H. Loh. 2006. Fire-and-Forget: Load/Store Scheduling with No Store Queue at All. In
   MICRO. 273–284. 5
Jean-Baptiste Tristan and Xavier Leroy. 2008. Formal verification of translation validators: a case study on instruction
   scheduling optimizations. In POPL. 17–27. 5
Ming-Hsien Tsai, Bow-Yaw Wang, and Bo-Yin Yang. 2017. Certified Verification of Algebraic Properties on Low-Level
   Mathematical Constructs in Cryptographic Programs. In CCS. ACM, 1973–1987. 8
Pepe Vila, Pierre Ganty, Marco Guarnieri, and Boris Köpf. 2020. CacheQuery: learning replacement policies from hardware
   caches. In PLDI. 519–532. 5
26                Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


Thomas Weise, Zijun Wu, and Markus Wagner. 2019. An Improved Generic Bet-and-Run Strategy with Performance
  Prediction for Stochastic Local Search. In AAAI. 2395–2402. 4


A     ON RELIABLE PERFORMANCE MEASUREMENT
A.1    Background
The execution time of a program can be affected by a myriad of factors, such as, the state of
cache memory [Alameldeen and Wood 2003]; context switches [Pusukuri et al. 2012]; memory
layout and OS environment variables [Curtsinger and Berger 2013; Mytkowicz et al. 2009]. Even
when a platform is rebooted between runs there can be significant variation in benchmark run
times [Kalibera et al. 2005a]. Furthermore, measurements of the benchmark operation can be
subject to inherent and external random changes to the benchmark operation, as well as the
system state prior to execution [Kalibera et al. 2005b; Kalibera and Jones 2013]. In addition, sensor
readings themselves can drift over time [Bokhari et al. 2019]. Consequently, all these factors
together result in measurement noise, which can affect both the sensitivity and specificity of
performance measurements. One recent work, which surveyed and compared validation approaches
in the context of energy consumption optimization [Bokhari et al. 2020], found that a number of
measurement approaches failed to mitigate the effects of measurement noise. Only the proposed
approach R3-validation was not misled: it exercised the tests in a rotated-round-robin fashion,
while accommodating the necessary regular restarting and recharging of the test platform.

A.2    Cost-Function Evaluation
Recall that CryptOpt generates solutions, mutates them, and measures their respective performance.
Measuring this performance on physical machines is inherently noisy. To lower the effect of noise
and enable more stable and fair comparisons, we base our measurement on R3-validation, which
exercises tests in a rotated-round-robin fashion. This approach was used in previous work [Bokhari
et al. 2020] in the context of energy consumption in order to mitigate the effects of measurement
noise.
   In our work, we adapt R3-validation in two ways. First, we forgo the restart of the computer
as we do not observe any measurement drift over time. Second, we perform a random scheduling
of program variants for performance measurement instead of strictly following a given order of
measurements.
Measuring Performance. Algorithm 3 presents our performance-measurement routine. We now
explain the rationale behind this from the inside out (inside the loop of the algorithm to the outside
of the measure function).
   Cycle counters are integers with a granularity of at best 1. Recall that CryptOpt can optimize
functions of arbitrary size, ranging in our experiments from fewer than 100 to around 2000 instruc-
tions. That means that the accuracy of the fixed-granularity counter relative to the length-varying
function changes. In other words, the same “stopwatch” is not appropriate to time an Olympic
sprinter and a marathon runner.
   The solution to that is to measure multiple executions of the same function instead of just one.
We call multiple executions of the same function a batch. The batch size bs specifies how many
executions of the same function are being measured with one measurement. It follows logically that
small functions should have a bigger bs than long functions in order to get similar cycle accuracy.
   Hence, we came up with the idea of the cyclegoal. That is, we want the measured cycles count
for one batch across all functions to be in the order of cyclegoal = 10 000 measured cycles. The
reason for this particular number is that we then have four to five digits of accuracy. CryptOpt
then scales the value for bs up or down by comparing the measured cycles against the cyclegoal.
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives        27


 Algorithm 3: Execution Time Measurement
  input : A pointer to code A,
           B pointer to code B,
           bs size of a measurement batch,
           nob number of batches to measure
  output : PA performance of code A in cycles,
           PB performance of code B in cycles
  function measure(A, B, bs, nob)
  begin
       /* initialize cycle lists                                                             */
       𝑐𝑦𝑐𝑙𝑒𝑠𝐴 ← empty list
       𝑐𝑦𝑐𝑙𝑒𝑠𝐵 ← empty list
       repeat
           /* f points to either A or B                                                      */
           𝑓 ← randomSelect(𝐴, 𝐵)
           /* run bs times and get elapsed cycles                                            */
           cycles ← countCyclesForNRuns(𝑏𝑠, 𝑓 )
           /* append elapsed cycles to list A/B resp.                                        */
          append(cycles 𝑓 , cycles)
       until both have been measured nob times;
       PA ← median(cycles𝐴 )
       PB ← median(cycles𝐵 )
     return PA, PB
  end



   This technique also mitigates another inherent problem that arises when measuring performance
in cycles on hardware: different hardware platforms interpret “cycles” differently, and additional
challenges arise due to different types of boosting. However, because CryptOpt adjusts bs in each
evaluation of the mutation (i.e. before each call to “measure”) and it does so on each platform
independently, we get comparable accuracy for all functions across platforms.
   Inherent with measuring time on hardware is measurement noise, which we as developers can
hardly control. This noise can be due to the OS’s interrupt event handlers or process scheduling.
It can also be due to temperature rises the hardware limits itself. The technique above mitigates
the problems having a bad “stopwatch” but at the same time increases the captured noise. Similar
to the R3-validation, we mitigate this problem by simply measuring each batch multiple times,
called numbers of batches or nob for short. That means that we have nob measurements for the
same function. We take the median as the performance measurement for a function to drop outlier
measurements. (Using the minimum rather than median did not have statistically significant effects
– neither positive nor negative.) Empirically, setting nob = 31 works well on our experimental
platforms.
   Complex processors nowadays can cause biases to one or another function by their speculative
execution, prediction behavior and caching, just to name a few reasons. The R3-validation also
mitigates this issue by using a random sequence of the functions to measure. We do this by randomly
selecting either function to measure a batch of.
28                      Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom




             1.8
             1.6
 speedup




             1.4
             1.2
             1.0
             0.8
                   10                 100                   1000                  10000                 100000
                                                             mutation

                                            (a) NIST P-384–square on i7 10G


             1.8
             1.6
 speedup




             1.4
             1.2
             1.0
             0.8
                   10                 100                   1000                  10000                 100000
                                                             mutation

                                              (b) secp256k1–mul on 1900X

Fig. 10. CryptOpt optimization progress of NIST P-384–square and secp256k1–mul on two different platforms.
Each line traces an optimization run over time (X-axis, log-scale), showing the relative performance gain over
Clang. Bet-and-Run used for 20 runs with a budget of 1 000 mutations each. The best-performing candidate
continues for another 180 000 mutations. Progress over time is roughly logarithmic in the number of mutations,
achieving a performance gain of 61–80%. We generate one data point every ten mutations.



A.3         AssemblyLine
CryptOpt uses AssemblyLine [0xADE1A1DE 2022] to assemble the generated initial and mutated
code into memory positions A and B. AssemblyLine is a lightweight in-memory assembler for
x86-64 assembly instructions. It takes an input string of instructions, assembles them into machine
code and returns a pointer to the executable code. We use AssemblyLine to eliminate the overhead
of writing to the file system and invoking a typical compiler tool chain for every evaluation.
Additionally, CryptOpt uses AssemblyLine to assemble the code to the start of a memory page. This
reduces noise in measurements because it always assembles aligned code for all functions, which,
in turn, reduces memory-biased performance impacts [Mytkowicz et al. 2009]. Once assembled,
CryptOpt calls the measure function with pointers to that code and values for batch size bs and
number of batches nob.

B          OPTIMIZATION PROGRESS
The first evaluation question we answer is how the optimization progresses over time. Figure 10
shows examples of optimization runs on i7 10G and 1900X, targeting the field-square operation
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives         29


corresponding to the prime field for NIST P-384 and the field-multiplication for the prime field
secp256k1.
   The figures show performance over time, where performance is measured as gain over the
baseline Clang-compiled code, while optimization time is measured in mutations (shown in log
scale).
   The figure shows the Bet-and-Run strategy in action. The optimization starts with 20 runs,
each with a budget of 1 000 mutations. CryptOpt then selects the best-performing and continues
optimizing it for a further 180 000 mutations. As the figure shows, in all runs, optimization progress
is roughly logarithmic in the number of mutations.
   A notable difference between the two optimizations is the overall performance gain and the
presence of noise. On the i7 10G platform the optimization converges rather quickly, whereas on
1900X we see monotonic improvement until the very end. Finally, we note that these variations
and performance gain are dependent on field, method and machine; here we see a gain 61–80%.

C   PLATFORM-SPECIFIC OPTIMIZATION
CryptOpt optimizes the execution time of the function on the platform it executes on. Because
different platforms have different hardware components, the fastest code on one platform is not
necessarily the fastest on another. Thus, in this section we ask whether CryptOpt overfits to the
platform it executes on, as opposed to universally optimizing for all platforms. That is, we test how
native optimization, where the code executes on the same platform it was optimized on, compares
with cross optimization, where code is optimized on one platform and executes on another.
   To test this, we first optimize each of the functions on each of the platforms. We then measure the
performance of the produced code from all platforms on all platforms (as per evaluation described
in Appendix A). Table 6 shows the results for the operations multiply and square on all nine
fields we tested. Rows correspond to the platform the code was optimized on and columns to the
platform the code is executed on. The value in a cell shows the ratio between the execution time
of the cross-optimized code and that of the native code. An example value of 1.10 indicates that
the cross-platform code (from the “row” platform) needs 1.10 times as many cycles as the native
code (from the “column” platform). In other words, a blue cell means that code from the column
architecture outperforms code from the row architecture, and the number indicates by how much.
   The additional column G.M. shows the geometric mean of the numbers in the row. This gives a
measure of “how platform-specific” one optimization is: A value larger than one (blue) in column
G.M. in the row for platform X indicates that on average, code from other platforms outperform
the code from X, if ran on platforms other than X. In turn, a value smaller than one means that
the code from platform X tends to outperform platform-specific code on other platforms. Please
note that a “large number” can arise for two reasons: (a) The platform-specific code is very bad
(thus easy to outperform), or (b) the generated code is very generic and can thus compete with
the platform-specific ones. To see which is applicable per platform, one needs to see how well
the code compares to off-the-shelf compilers. Note that this is also not a universal measure, as
off-the-shelf compilers generate different code per platform. Alternatively, running the same code
on all platforms would also not give a fair baseline, as compilers would not be enabled to generate
platform-specific code, whereas CryptOpt would be.
   As can be seen in Table 6 for Curve25519, optimizing and running on the same architecture
tends to outperform cross-architecture optimizations (which would mean the 10-by-10 is mostly
blue, and the G.M. column is fully blue, too). However, there are cases where cross-architectural
optimizations are better. In particular it appears that optimization of SIKEp434 functions on AMD
is not ideal, and the results underperform code optimized on Intel processors. (Still, faster than
compiling with off-the-shelf compilers).
30                                           Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom


Table 6. Optimization results. We show the relative improvements in % for the multiplication (top) and squaring (bottom) operations; time savings are marked
in blue. First, to observe hardware-specific optimization, the 10-by-10 matrix shows the performance the optimized operation that have been optimized on one
machine and then run on another. The subsequent two rows (Clang/GCC) then show the time savings of our optimized operations over off-the-shelf-compilers.
Lastly, “Final” shows the time savings of our best-performing implementation over the best-performing compiler-generated version.
                             Curve25519             i7 10G
                                                                                                                                          P-224                                                                                              P-256
                                                             i9 10G
                                                                      i7 11G
                                                                               i9 12G
                                                                                        i9 13G




                                                                                                                                                       i7 10G
                                                                                                                                                                i9 10G
                                                                                                                                                                         i7 11G
                                                                                                                                                                                  i9 12G
                                                                                                                                                                                           i9 13G




                                                                                                                                                                                                                                                          i7 10G
                                                                                                                                                                                                                                                                   i9 10G
                                                                                                                                                                                                                                                                            i7 11G
                                                                                                                                                                                                                                                                                     i9 12G
                                                                                                                                                                                                                                                                                              i9 13G
            1900X
                    5800X
                            5950X
                                    7950X




                                                                                                               1900X
                                                                                                                       5800X
                                                                                                                               5950X
                                                                                                                                       7950X




                                                                                                                                                                                                                  1900X
                                                                                                                                                                                                                          5800X
                                                                                                                                                                                                                                  5950X
                                                                                                                                                                                                                                          7950X
                                            i7 6G




                                                                                                                                               i7 6G




                                                                                                                                                                                                                                                  i7 6G
                                                                                                 G.M.




                                                                                                                                                                                                    G.M.




                                                                                                                                                                                                                                                                                                       G.M.
     run on                                                                                             run on                                                                                             run on
     opt on                                                                                             opt on                                                                                             opt on
      1900X      1.071.111.081.071.061.041.171.311.281.12                                                1900X      1.031.031.091.081.041.071.031.111.071.05                                                1900X      1.000.950.961.041.021.061.011.101.081.02
      5800X 1.07     1.051.051.071.051.051.121.231.191.09                                                5800X 1.06     1.011.051.091.051.081.061.171.181.07                                                5800X 1.06     0.950.971.051.031.081.031.171.141.05
      5950X 1.010.97     1.001.051.021.021.131.191.161.05                                                5950X 1.060.99     1.061.051.011.041.011.071.091.04                                                5950X 1.161.05     1.041.091.071.111.041.151.121.08
      7950X 1.051.021.05      1.101.111.081.161.251.221.10                                               7950X 1.010.960.96      1.051.031.041.031.121.111.03                                               7950X 1.121.040.99      1.081.071.091.051.211.161.08
       i7 6G 1.041.081.131.10     0.981.011.121.291.271.10                                                i7 6G 1.041.011.011.05     0.960.991.011.031.041.02                                                i7 6G 1.091.040.991.02     0.971.011.051.101.071.03
     i7 10G 1.101.091.131.101.02      1.021.071.241.211.10                                              i7 10G 1.051.041.051.101.02      1.031.021.071.061.04                                              i7 10G 1.111.081.031.061.02      1.051.041.121.081.06
     i9 10G 1.041.081.121.081.001.00      1.131.291.261.10                                              i9 10G 1.010.980.991.041.010.97      0.991.021.031.00                                              i9 10G 1.051.040.991.020.970.95      1.031.051.021.01
     i7 11G 1.051.051.111.121.041.021.02      1.211.191.08                                              i7 11G 1.071.051.081.121.111.061.10      1.061.071.07                                              i7 11G 1.111.071.011.051.061.021.06      1.111.071.06
     i9 12G 1.000.991.041.050.980.960.951.04      0.981.00                                              i9 12G 1.031.021.021.061.020.981.010.97      1.001.01                                              i9 12G 1.081.030.981.011.000.981.020.99      0.961.00
     i9 13G 1.020.991.041.030.980.960.961.051.03      1.01                                              i9 13G 1.061.021.031.071.051.011.061.010.99      1.03                                              i9 13G 1.081.061.011.031.021.001.041.011.03      1.03
      Clang 1.181.201.261.231.271.251.241.291.291.251.25                                                 Clang 1.501.471.481.441.581.511.571.511.671.691.54                                                 Clang 1.671.691.611.561.671.631.721.681.971.831.70
        GCC 1.001.121.171.231.111.091.091.181.341.321.16                                                   GCC 2.282.002.022.052.882.732.862.543.103.102.52                                                   GCC 2.502.142.032.082.892.842.952.653.233.132.61
       Final 1.001.161.171.231.141.131.151.181.291.281.17                                                 Final 1.501.531.551.441.581.571.581.551.691.691.57                                                 Final 1.671.701.691.621.731.721.721.701.971.901.74
     1900X       1.081.071.061.061.081.071.141.351.361.12                                               1900X       1.031.000.951.071.061.031.091.151.161.05                                               1900X       1.011.020.991.031.021.071.101.061.111.04
     5800X 1.08      1.001.001.071.091.061.111.181.201.08                                               5800X 1.07      0.970.921.101.091.061.181.231.221.08                                               5800X 1.08      1.020.961.051.051.051.121.101.161.06
     5950X 1.101.01      1.001.071.091.061.151.191.211.08                                               5950X 1.101.04      0.941.141.151.081.131.221.211.10                                               5950X 1.080.97      0.961.051.031.071.071.051.081.04
     7950X 1.111.041.03      1.101.131.081.141.211.221.10                                               7950X 1.151.101.06      1.181.161.131.171.261.251.14                                               7950X 1.081.041.06      1.101.081.121.131.121.171.09
      i7 6G 1.121.121.151.10     1.020.991.051.371.391.12                                                i7 6G 1.031.020.980.94     0.980.951.031.041.031.00                                                i7 6G 1.051.021.040.99     0.970.981.051.051.101.02
     i7 10G 1.121.091.071.050.99     0.971.041.341.371.10                                               i7 10G 1.061.041.010.971.02     0.971.011.051.061.02                                               i7 10G 1.071.061.081.041.01     1.011.071.071.121.05
     i9 10G 1.121.101.091.101.011.03     1.101.311.331.11                                               i9 10G 1.101.081.050.991.051.03     1.101.161.151.07                                               i9 10G 1.051.021.030.991.000.99     1.051.061.111.03
     i7 11G 1.111.141.141.151.061.081.05     1.451.461.15                                               i7 11G 1.051.051.020.961.081.071.03     1.081.071.04                                               i7 11G 1.101.041.061.031.071.051.06     1.061.081.05
     i9 12G 1.050.990.980.970.960.990.951.02     1.010.99                                               i9 12G 1.041.041.000.951.031.010.981.04     0.991.01                                               i9 12G 1.081.051.091.031.071.071.071.07     1.031.06
     i9 13G 1.020.990.980.950.930.950.950.980.99     0.97                                               i9 13G 1.031.041.010.961.061.020.991.050.98     1.01                                               i9 13G 1.051.051.071.031.021.011.041.070.97     1.03
      Clang 1.201.171.161.121.181.201.171.121.211.321.18                                                 Clang 1.361.361.321.191.481.461.421.401.571.521.40                                                 Clang 1.561.601.621.481.641.621.671.631.751.791.63
       GCC 1.131.181.161.181.081.101.081.151.311.301.17                                                   GCC 2.372.072.011.852.932.862.802.663.303.282.56                                                   GCC 2.432.142.182.062.892.862.892.732.913.092.59
       Final 1.131.171.181.171.161.161.151.141.221.301.18                                                 Final 1.361.361.361.291.481.491.501.401.591.531.43                                                 Final 1.561.641.621.541.641.671.691.631.801.791.66
                                       P-384                                                                                       SIKEp434                                                                                           Curve448
                                                    i7 10G
                                                             i9 10G
                                                                      i7 11G
                                                                               i9 12G
                                                                                        i9 13G




                                                                                                                                                                                                                                                          i7 10G
                                                                                                                                                                                                                                                                   i9 10G
                                                                                                                                                                                                                                                                            i7 11G
                                                                                                                                                                                                                                                                                     i9 12G
                                                                                                                                                                                                                                                                                              i9 13G
                                                                                                                                                       i7 10G
                                                                                                                                                                i9 10G
                                                                                                                                                                         i7 11G
                                                                                                                                                                                  i9 12G
                                                                                                                                                                                           i9 13G
            1900X
                    5800X
                            5950X
                                    7950X




                                                                                                                                                                                                                  1900X
                                                                                                                                                                                                                          5800X
                                                                                                                                                                                                                                  5950X
                                                                                                                                                                                                                                          7950X
                                                                                                               1900X
                                                                                                                       5800X
                                                                                                                               5950X
                                                                                                                                       7950X
                                            i7 6G




                                                                                                                                                                                                                                                  i7 6G
                                                                                                                                               i7 6G
                                                                                                 G.M.




                                                                                                                                                                                                                                                                                                       G.M.
                                                                                                                                                                                                    G.M.



     run on                                                                                             run on                                                                                             run on
     opt on                                                                                             opt on                                                                                             opt on
      1900X      1.351.331.271.571.541.601.451.031.041.30                                                1900X      0.931.060.941.751.811.881.420.950.941.22                                                1900X      1.171.221.141.171.131.161.251.101.041.14
      5800X 0.80     0.980.951.151.161.181.060.780.780.97                                                5800X 1.20     1.141.021.962.082.111.631.061.061.36                                                5800X 0.95     1.040.991.051.041.051.010.980.961.01
      5950X 0.821.01     0.951.161.181.181.090.810.800.99                                                5950X 0.930.88     0.891.711.821.841.350.930.921.17                                                5950X 0.950.97     0.941.051.051.041.030.970.930.99
      7950X 0.851.091.04      1.201.221.231.070.780.791.01                                               7950X 1.291.011.14      2.122.212.291.611.101.131.41                                               7950X 0.961.031.08      1.061.061.071.060.960.931.02
       i7 6G 0.761.000.980.93     1.011.031.020.750.750.91                                                i7 6G 0.630.670.760.67     1.051.080.980.660.620.79                                                i7 6G 0.951.021.061.00     0.981.010.990.960.910.99
     i7 10G 0.771.000.980.940.99      1.000.970.670.670.89                                              i7 10G 0.630.650.730.660.98      1.050.950.660.630.78                                              i7 10G 0.951.021.061.011.02      1.001.030.950.910.99
     i9 10G 0.750.960.940.930.971.00      0.970.710.700.88                                              i9 10G 0.620.640.730.640.930.97      0.910.630.600.75                                              i9 10G 0.941.031.071.011.001.00      1.000.980.941.00
     i7 11G 0.801.051.030.971.091.111.11      0.700.710.94                                              i7 11G 0.670.700.790.701.131.171.23      0.670.640.84                                              i7 11G 0.961.061.111.041.041.061.03      0.980.941.02
     i9 12G 1.021.361.341.271.521.531.561.44      1.001.28                                              i9 12G 1.220.991.131.001.962.042.121.54      0.981.33                                              i9 12G 1.021.161.211.131.161.141.141.16      0.981.11
     i9 13G 1.021.381.371.291.521.541.561.461.00      1.29                                              i9 13G 1.231.021.151.031.912.032.041.581.04      1.34                                              i9 13G 1.041.201.261.181.171.171.161.231.03      1.14
      Clang 1.071.601.561.311.721.741.761.601.121.231.45                                                 Clang 1.211.381.571.242.222.312.382.211.531.481.70                                                 Clang 1.041.051.101.031.321.311.311.341.201.251.19
        GCC 1.842.082.041.983.283.293.343.312.222.212.49                                                   GCC 1.681.862.121.543.523.673.783.652.041.962.43                                                   GCC 0.870.951.000.931.041.041.040.990.970.960.98
       Final 1.431.661.651.421.771.741.761.661.651.851.65                                                 Final 1.962.172.171.932.372.372.382.432.442.462.26                                                 Final 0.920.991.000.991.051.061.051.011.021.051.01
     1900X       1.301.341.241.481.521.551.491.171.001.29                                               1900X       0.931.050.911.771.811.771.380.990.931.20                                               1900X       1.091.101.051.101.111.121.131.091.061.09
     5800X 0.81      1.040.971.141.221.201.200.940.791.02                                               5800X 1.34      1.130.982.082.102.081.651.131.091.39                                               5800X 1.03      1.000.981.111.131.121.131.161.121.08
     5950X 0.820.97      0.941.141.201.201.120.910.781.00                                               5950X 1.090.88      0.861.791.821.801.520.970.941.21                                               5950X 1.041.00      0.981.141.121.121.121.161.131.08
     7950X 0.851.061.08      1.231.291.301.190.960.831.07                                               7950X 1.361.031.16      2.132.072.111.611.141.111.41                                               7950X 1.011.021.02      1.101.101.131.101.131.091.07
      i7 6G 0.750.981.000.94     1.041.031.060.890.740.94                                                i7 6G 0.660.640.730.62     0.981.010.890.660.610.76                                                i7 6G 1.011.021.031.01     0.991.011.031.131.091.03
     i7 10G 0.740.960.990.930.93     0.981.010.760.640.89                                               i7 10G 0.680.650.740.641.00     1.000.870.610.570.76                                               i7 10G 1.011.031.041.021.00     1.011.051.141.101.04
     i9 10G 0.740.950.980.910.961.02     1.000.810.680.90                                               i9 10G 0.680.690.740.641.001.02     0.910.650.600.78                                               i9 10G 1.001.011.021.010.980.98     1.051.071.041.02
     i7 11G 0.770.991.030.941.031.081.07     0.790.680.93                                               i7 11G 0.730.690.780.691.191.171.20     0.740.680.86                                               i7 11G 1.011.021.041.031.021.031.04     1.131.111.04
     i9 12G 0.921.201.231.141.301.361.381.28     0.861.15                                               i9 12G 1.220.971.100.941.801.831.781.47     0.931.26                                               i9 12G 1.021.041.051.011.041.051.061.06     0.971.03
     i9 13G 1.011.321.361.251.551.651.621.501.18     1.32                                               i9 13G 1.261.001.140.991.921.951.901.511.08     1.32                                               i9 13G 1.021.041.041.001.061.061.081.061.03     1.04
      Clang 1.021.451.491.221.541.621.621.581.181.121.37                                                 Clang 1.341.421.611.212.312.332.322.221.571.481.73                                                 Clang 0.991.031.041.041.071.081.091.161.101.061.07
       GCC 1.922.042.101.933.263.533.423.082.492.092.51                                                   GCC 1.961.551.751.503.713.783.713.652.091.952.39                                                   GCC 0.981.041.051.021.011.021.031.011.181.121.05
       Final 1.391.521.521.341.661.621.651.591.551.751.55                                                 Final 2.032.212.211.952.322.382.322.542.562.592.30                                                 Final 0.981.031.041.051.041.041.031.011.101.101.04
                                       P-521                                                                                           Poly1305                                                                                      secp256k1
                                                    i7 10G
                                                             i9 10G
                                                                      i7 11G
                                                                               i9 12G
                                                                                        i9 13G




                                                                                                                                                       i7 10G
                                                                                                                                                                i9 10G
                                                                                                                                                                         i7 11G
                                                                                                                                                                                  i9 12G
                                                                                                                                                                                           i9 13G




                                                                                                                                                                                                                                                          i7 10G
                                                                                                                                                                                                                                                                   i9 10G
                                                                                                                                                                                                                                                                            i7 11G
                                                                                                                                                                                                                                                                                     i9 12G
                                                                                                                                                                                                                                                                                              i9 13G
            1900X
                    5800X
                            5950X
                                    7950X




                                                                                                               1900X
                                                                                                                       5800X
                                                                                                                               5950X
                                                                                                                                       7950X




                                                                                                                                                                                                                  1900X
                                                                                                                                                                                                                          5800X
                                                                                                                                                                                                                                  5950X
                                                                                                                                                                                                                                          7950X
                                            i7 6G




                                                                                                                                               i7 6G




                                                                                                                                                                                                                                                  i7 6G
                                                                                                 G.M.




                                                                                                                                                                                                    G.M.




                                                                                                                                                                                                                                                                                                       G.M.




     run on                                                                                             run on                                                                                             run on
     opt on                                                                                             opt on                                                                                             opt on
      1900X      1.091.101.031.151.151.191.221.091.031.10                                                1900X      1.151.121.141.161.111.171.121.211.211.14                                                1900X      1.020.991.021.011.021.011.021.051.121.03
      5800X 1.00     1.010.961.131.081.121.101.061.001.04                                                5800X 1.15     0.971.031.131.061.161.141.171.191.10                                                5800X 1.04     0.970.971.021.041.031.011.081.131.03
      5950X 0.990.99     0.971.061.051.081.021.010.941.01                                                5950X 1.201.05     1.001.121.021.091.151.231.221.10                                                5950X 1.061.03     1.011.041.051.041.041.051.111.04
      7950X 1.021.031.05      1.151.131.151.231.101.031.09                                               7950X 1.131.031.00      1.111.041.121.081.261.261.10                                               7950X 1.041.030.99      1.081.091.061.071.101.161.06
       i7 6G 0.970.991.000.96     0.961.011.021.081.011.00                                                i7 6G 1.121.101.051.05     0.961.001.021.381.391.10                                                i7 6G 1.091.081.051.07     1.011.011.021.061.121.05
     i7 10G 0.991.031.040.991.02      1.021.041.050.991.02                                              i7 10G 1.171.171.141.141.01      1.021.051.471.491.15                                              i7 10G 1.081.111.091.060.98      0.991.011.081.141.05
     i9 10G 0.960.970.980.940.970.95      1.021.000.930.97                                              i9 10G 1.141.131.091.131.030.95      1.061.391.421.12                                              i9 10G 1.081.091.061.081.011.01      1.011.031.091.05
     i7 11G 0.991.041.041.001.061.021.07      1.020.971.02                                              i7 11G 1.091.101.061.071.010.961.01      1.361.381.10                                              i7 11G 1.111.151.111.101.081.091.09      1.091.151.10
     i9 12G 1.061.131.141.101.221.191.231.29      0.951.12                                              i9 12G 1.101.041.011.031.030.981.031.00      1.001.02                                              i9 12G 1.121.131.081.091.031.071.041.02      1.061.06
     i9 13G 1.061.141.151.071.281.181.281.321.07      1.15                                              i9 13G 1.111.051.011.031.000.961.011.061.00      1.02                                              i9 13G 1.061.061.031.051.001.021.010.970.96      1.02
      Clang 1.131.201.211.141.441.391.461.421.401.251.30                                                 Clang 1.121.061.031.041.131.101.151.121.321.201.12                                                 Clang 1.801.891.831.631.801.831.811.791.771.871.80
        GCC 1.011.101.110.990.930.900.940.930.950.880.97                                                   GCC 1.111.131.101.121.281.221.281.201.431.361.22                                                   GCC 2.442.212.132.132.902.902.922.603.043.222.62
       Final 1.051.141.141.050.960.950.940.930.950.941.00                                                 Final 1.111.061.061.041.131.151.151.121.331.201.13                                                 Final 1.801.891.881.681.831.831.831.841.831.871.83
     1900X       1.051.051.071.211.171.181.101.331.231.14                                               1900X       1.111.101.061.091.101.101.081.151.101.09                                               1900X       1.011.061.021.071.041.051.031.111.161.05
     5800X 0.99      0.991.031.211.191.161.031.331.201.11                                               5800X 1.06      1.101.001.061.081.101.031.071.021.05                                               5800X 1.06      1.061.031.061.071.061.061.151.201.07
     5950X 1.031.02      1.021.241.251.171.121.381.261.14                                               5950X 1.041.02      1.011.091.091.101.091.181.121.07                                               5950X 1.010.95      0.991.031.051.041.021.121.171.04
     7950X 1.000.990.99      1.201.171.141.061.301.211.10                                               7950X 1.051.041.04      1.091.081.081.061.081.031.05                                               7950X 1.060.991.05      1.071.071.061.071.151.191.07
      i7 6G 0.921.000.961.01     0.980.960.951.251.181.02                                                i7 6G 1.051.091.091.06     1.011.011.001.351.311.09                                                i7 6G 1.031.031.091.14     1.011.001.041.081.131.05
     i7 10G 0.911.041.021.061.02     0.990.971.241.161.04                                               i7 10G 1.061.141.141.110.99     1.001.041.271.251.10                                               i7 10G 1.041.031.081.050.98     0.991.021.081.141.04
     i9 10G 0.940.990.971.001.021.02     0.991.271.201.04                                               i9 10G 1.091.161.151.180.991.00     1.041.401.361.13                                               i9 10G 1.061.021.081.040.991.03     1.001.101.151.05
     i7 11G 1.001.081.071.071.181.161.12     1.331.231.12                                               i7 11G 1.061.121.131.131.041.021.02     1.411.361.12                                               i7 11G 1.051.041.091.061.051.061.05     1.141.191.07
     i9 12G 0.920.960.950.981.051.031.010.91     0.930.97                                               i9 12G 1.051.061.061.061.031.031.031.01     0.951.03                                               i9 12G 1.071.041.101.071.031.031.021.02     1.051.04
     i9 13G 0.971.021.011.041.131.121.100.991.07     1.04                                               i9 13G 1.051.141.181.111.011.021.021.011.05     1.06                                               i9 13G 1.011.001.051.010.991.001.000.950.97     1.00
      Clang 1.011.201.181.311.591.551.521.611.401.281.35                                                 Clang 1.011.121.121.091.121.131.131.071.201.151.11                                                 Clang 1.611.711.801.551.731.741.731.641.781.861.71
       GCC 0.991.051.041.031.000.980.960.931.221.121.03                                                   GCC 1.091.291.301.171.301.301.321.281.291.241.26                                                   GCC 2.282.032.142.092.782.772.802.483.073.232.54
       Final 1.091.091.091.051.001.001.001.021.221.211.07                                                 Final 1.011.121.121.091.131.131.131.071.201.201.12                                                 Final 1.611.801.801.571.761.741.741.731.841.861.74
CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives           31


   Another effect that the table highlights is that optimization overfits for processor families, for
some families more than others. In particular, Intel 6th and 10th generations show little differences in
the respective inter-platform performance. For example, the related 3x3 sub-matrices for Curve25519
in Table 6 have values in the small interval [0.98, 1.02] (mul), [0.97, 1.03] (square); as do AMD
Zen 3 processors in the 2x2 sub-matrices have values in the small interval [0.97, 1.05] (mul), and
[1.00, 1.02] for square.
   This specialization to platforms is a double-edged sword. On the one hand, it allows CryptOpt
to produce high-performing code, as previously shown. On the other hand, it also means that the
code is potentially less generic, and it might be less performant if executed on platforms other than
originally intended, as observed in our a-posteriori analysis.

D    DETAILED PERFORMANCE INFORMATION
Table 7 shows the detailed performance information of the scalar multiplication experiments. We
use SUPERCOP to evaluate and report the cycles for two base-point and two variable-point scalar
multiplications. The table is divided in two sections, one for Curve25519 and one for secp256k1.
In each of those sections we compare different implementations of the scalar multiplication for
respective curve against each other. The language, in which the core operations are implemented,
is written in the column Lang. The following columns show the elapsed cycles for the scalar
multiplication. The fastest implementation per section and per platform is highlighted in (bold
text) and notes a (1.00x). All other implementations are then compared against this fastest in
the form of the ratio, which is written in parenthesis. E.g. 1.05x means that it takes 1.05 times as
many cycles than the fastest. The last column, G.M., is the geometric mean of the cycles across all
platforms, the ratio is then recalculated on that G.M. as well.
   For secp256k1, we base all evaluation on the implementation for scalar multiplication on the
one from libsecp256k1. What changes is the implementation of the field arithmetic. That is, the
first two rows are the asm and C implementations from libsecp256k1. In the third row, we plug
in verified and optimized field operations based on Fiat Cryptography, and in the last row we
use the optimized versions of libsecp256k1’s own implementation (i.e. no formal correctness
verification).
   Note: “ots” stands for off-the-shelf; “asm” means assembly; “-v” indicates the use of vector instruc-
tions. The HACL* implementation [HACL 2022] uses parallelized field arithmetic. For Curve25519,
“-51“ and “-64“ indicates whether the representation for the field elements is unsaturated or saturated.
                                                                                                                                                                                                                                        32
             Implementation                     Lang.        1900X           5800X           5950X           7950X            i7 6G          i7 10G          i9 10G          i7 11G          i9 12G          i9 13G            G.M.
             sandy2x [Chou 2015]                asm-v    603k (1.05x)   426k (1.00x)    426k (1.00x)    421k (1.00x)     521k (1.15x)    521k (1.15x)    521k (1.15x)    492k (1.15x)    480k (1.31x)    480k (1.31x)    486k (1.07x)
             amd64-64 [Chen et al. 2014]        asm      622k (1.09x)    573k (1.34x)    573k (1.34x)    528k (1.25x)    569k (1.26x)    571k (1.26x)    572k (1.26x)    536k (1.26x)    452k (1.23x)    452k (1.23x)    542k (1.20x)
             amd64-51 [Chen et al. 2014]        asm      772k (1.35x)    586k (1.37x)    586k (1.37x)    563k (1.34x)    567k (1.26x)    567k (1.26x)    567k (1.25x)    490k (1.15x)    420k (1.14x)    421k (1.15x)    546k (1.21x)
Curve25519   donna [Langley 2022]               asm-v   1089k (1.90x)    973k (2.28x)    971k (2.28x)    954k (2.26x)   1023k (2.27x)   1015k (2.25x)   1014k (2.24x)    958k (2.25x)    871k (2.37x)    872k (2.38x)    972k (2.15x)
             donna-c64 [Langley 2022]           C        807k (1.41x)    599k (1.40x)    598k (1.40x)    637k (1.51x)    581k (1.29x)    582k (1.29x)    582k (1.29x)    550k (1.29x)    453k (1.23x)    451k (1.23x)    577k (1.27x)
             OSSL ots [OpenSSL 2022]            C        700k (1.22x)    538k (1.26x)    541k (1.27x)    536k (1.27x)    568k (1.26x)    567k (1.26x)    568k (1.25x)    494k (1.16x)    421k (1.15x)    420k (1.15x)    530k (1.17x)
             OSSL fe-51 ots [OpenSSL 2022]      asm      696k (1.22x)    540k (1.27x)    540k (1.27x)    536k (1.27x)    580k (1.28x)    568k (1.26x)    568k (1.25x)    493k (1.16x)    419k (1.14x)    420k (1.15x)    530k (1.17x)
             OSSL fe-51+CryptOpt                asm      709k (1.24x)    536k (1.26x)    528k (1.24x)    512k (1.22x)    571k (1.27x)    579k (1.28x)    571k (1.26x)    508k (1.19x)    399k (1.09x)    398k (1.09x)    524k (1.16x)
             OSSL fe-64 ots [OpenSSL 2022]      asm     572k (1.00x)     444k (1.04x)    444k (1.04x)    431k (1.02x)    462k (1.02x)    460k (1.02x)    464k (1.03x)    465k (1.09x)    411k (1.12x)    412k (1.13x)    455k (1.01x)
             OSSL fe-64+CryptOpt                asm      594k (1.04x)    455k (1.07x)    460k (1.08x)    456k (1.08x)    482k (1.07x)    489k (1.08x)    480k (1.06x)    446k (1.05x)    387k (1.05x)    392k (1.07x)    461k (1.02x)




                                                                                                                                                                                                                                        Kuepper, Erbsen, Gross, Conoly, Sun, Tian, Wu, Chlipala, Chuengsatiansup, Genkin, Wagner, Yarom
             HACL* fe-64 [HACL 2022]            asm      588k (1.03x)    496k (1.16x)    493k (1.16x)    473k (1.12x)   451k (1.00x)    451k (1.00x)    452k (1.00x)    426k (1.00x)    367k (1.00x)    366k (1.00x)    452k (1.00x)
secp256k1




             libsecp256k1 [Bitcoin Core 2021]   asm      719k (1.07x)    567k (1.05x)    567k (1.05x)    560k (1.06x)    565k (1.03x)    563k (1.02x)    564k (1.02x)    539k (1.07x)    436k (1.04x)    439k (1.06x)    547k (1.04x)
             libsecp256k1 [Bitcoin Core 2021]   C       671k (1.00x)    540k (1.00x)    539k (1.00x)     529k (1.01x)    562k (1.02x)    563k (1.02x)    562k (1.02x)    505k (1.00x)    437k (1.04x)    435k (1.05x)    530k (1.01x)
             libsecp256k1+CryptOpt(Fiat)        asm      705k (1.05x)    548k (1.02x)    550k (1.02x)    533k (1.01x)   549k (1.00x)    550k (1.00x)     554k (1.00x)   504k (1.00x)    419k (1.00x)    416k (1.00x)    527k (1.00x)
             libsecp256k1+CryptOpt(Opt)         asm      718k (1.07x)    542k (1.00x)    540k (1.00x)   527k (1.00x)     551k (1.00x)    556k (1.01x)   553k (1.00x)     509k (1.01x)    421k (1.01x)    418k (1.01x)    528k (1.00x)

                                Table 7. Cost of scalar multiplication (in cycles) of different implementations benchmarking on different machines.
