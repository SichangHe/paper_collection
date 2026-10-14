                                                  B INSEC /R EL: Efficient Relational Symbolic
                                                  Execution for Constant-Time at Binary-Level
                                                                            Lesly-Ann Daniel∗ , Sébastien Bardin∗ , Tamara Rezk†
                                                                                    ∗ CEA, List, Université Paris-Saclay, France
                                                                                 † INRIA Sophia-Antipolis, INDES Project, France


                                                                      lesly-ann.daniel@cea.fr, sebastien.bardin@cea.fr, tamara.rezk@inria.fr
arXiv:1912.08788v2 [cs.CR] 11 Jul 2020




                                            Abstract—The constant-time programming discipline (CT) is         gations eventually become vulnerable to new generations of
                                         an efficient countermeasure against timing side-channel attacks,     attacks and provide only pseudo security [7].
                                         requiring the control flow and the memory accesses to be                The constant-time programming discipline (CT) [8],
                                         independent from the secrets. Yet, writing CT code is challenging
                                         as it demands to reason about pairs of execution traces (2-          a.k.a. constant-time policy, is a software-based countermeasure
                                         hypersafety property) and it is generally not preserved by the       to timing attacks which requires the control flow and the
                                         compiler, requiring binary-level analysis. Unfortunately, current    memory accesses of the program to be independent from the
                                         verification tools for CT either reason at higher level (C or        secret input1 . Constant-time has been proven to protect against
                                         LLVM), or sacrifice bug-finding or bounded-verification, or do       cache-based timing attacks [8], making it the most effective
                                         not scale. We tackle the problem of designing an efficient
                                         binary-level verification tool for CT providing both bug-finding     countermeasure against timing attacks, already widely used
                                         and bounded-verification. The technique builds on relational         to secure cryptographic implementations (e.g. BearSSL [9],
                                         symbolic execution enhanced with new optimizations dedicated         NaCL [10], HACL* [11], etc).
                                         to information flow and binary-level analysis, yielding a dramatic
                                         improvement over prior work based on symbolic execution. We          Problem. Writing constant-time code is complex as it requires
                                         implement a prototype, B INSEC /R EL, and perform extensive          low-level operations deviating from traditional programming
                                         experiments on a set of 338 cryptographic implementations,           behaviors. Moreover, this effort is brittle as it is generally
                                         demonstrating the benefits of our approach in both bug-finding       not preserved by compilers [12], [13]. For example, reasoning
                                         and bounded-verification. Using B INSEC /R EL, we also automate      about CT requires to know whether the code c=(x<y)-1
                                         a previous manual study of CT preservation by compilers.
                                         Interestingly, we discovered that gcc -O0 and backend passes         will be compiled to branchless code, but this depends on
                                         of clang introduce violations of CT in implementations that          the compiler version and optimization [12]. As shown in
                                         were previously deemed secure by a state-of-the-art CT verifi-       the attack on a “constant-time” implementation of elliptic
                                         cation tool operating at LLVM level, showing the importance of       curve Curve25519 [13], writing constant-time code is error
                                         reasoning at binary-level.                                           prone [7], [12], [13].
                                                                                                                 Several CT-analysis tools have been proposed to analyze
                                                               I. I NTRODUCTION                               source code [14], [15], or LLVM code [16], [17], but leave
                                                                                                              the gap opened for violations introduced in the executable code
                                            Timing channels occur when timing variations in a sequence        either by the compiler [12] or by closed-source libraries [13].
                                         of events depends on secret data. They can be exploited by           Binary-level tools for CT using dynamic aproaches [18]–
                                         an attacker to recover secret information such as plaintext          [21] can find bugs but miss vulnerabilities in unexplored
                                         data or secret keys. Timing attacks, unlike other side-channel       portions of the code, making them incomplete; while static
                                         attacks (e.g based on power-analysis, electromagnetic radiation      approaches [22]–[24] cannot report precise counterexamples
                                         or acoustic emanations) do not require special equipment and         – making them of minor interest when the implementation
                                         can be performed remotely [1], [2]. First timing attacks ex-         cannot be proven secure. Aside from a posteriori analysis,
                                         ploited secret-dependent control flow with measurable timing         correct-by-design approaches [11], [25]–[27] require to reim-
                                         differences to recover secret keys [3] from cryptosystems. With      plement cryptographic primitives from scratch, and OS-based
                                         the increase of shared architectures (e.g. infrastructure as a       countermeasures [28]–[31] incur runtime overhead and require
                                         service) arise more powerful attacks where an attacker can           specific OS- or hardware-support.
                                         monitor the cache of the victim and recover information on
                                         secret-dependent memory accesses [4]–[6].                            Challenges. Two main challenges arise in the verification of
                                            Therefore, it is of paramount importance to implement             constant-time:
                                         adequate countermeasures to protect cryptographic implemen-            • First, common verification methods do not directly apply

                                         tations from these attacks. Simple countermeasures consisting             because information flow properties like CT are not
                                         in adding noise or dummy computations can reduce timing                 1 Some versions of CT also require that the size of operands of variable-time
                                         variations and make attacks more complex. Yet, these miti-           instructions (e.g. integer division) is independent from secrets.
      regular safety properties but 2-hypersafety properties [32]    Contributions. Our contributions are the following:
      (i.e. relating two execution traces), and their standard          • We design dedicated optimizations for information flow
      reduction to safety on a transformed program, self-                  analysis at binary-level. First, we complement relational
      composition [33], is inefficient [34];                               symbolic execution with a new on-the-fly simplification
   • Second, it is notoriously difficult to adapt formal methods           for binary-level analysis, to track secret-dependencies and
      to binary-level because of the lack of structure informa-            maximize sharing in the memory (Section V-A1). Second,
      tion (data & control) and the explicit representation of             we design new simplifications for information flow anal-
      the memory as a single large array of bytes [35], [36].              ysis: untainting (Section V-A2) and fault-packing (Sec-
A technique that scales well on binary code and that naturally             tion V-A3). Moreover, we formally prove that our analysis
comes into play for bug-finding and bounded-verification is                is correct for bug-finding and bounded-verification of CT
symbolic execution (SE) [37], [38]. While it has proven very               (Section V-B).
successful for standard safety properties [39], its direct adapta-      • We propose a verification tool named B INSEC /R EL for
tion to CT and other 2-hypersafety properties through (variants            CT analysis (Section VI). Extensive experimental evalua-
of) self-composition suffers from a scalability issue [40]–[42].           tion (338 samples) against standard approaches based on
Some recent approaches achieve better scaling, but at the cost             self-composition and RelSE (Section VII-B) shows that
of sacrificing either bounded-verification [20], [43] (under-              it can find bugs in real-world cryptographic implementa-
approximation) or bug-finding [17] (over-approximations).                  tions much faster than these techniques (×700 speedup)
   The idea of analyzing pairs of executions for the veri-                 and can achieve bounded-verification when they timeout,
fication of 2-hypersafety is not new (e.g. relational Hoare                with performances close to standard SE (×1.8 overhead).
logic [44], self-composition [33], product programs [45],               • In order to prove the effectiveness of B INSEC /R EL , we
multiple facets [46], [47]). In the context of symbolic exe-               perform an extensive analysis of CT at binary-level. In
cution, it has first been coined as ShadowSE [48] for back-                particular, we analyze 296 cryptographic implementations
to-back testing, and later as relational symbolic execution                previously verified at a higher-level (incl. codes from
(RelSE) [49]. However, a direct adaptation of this technique               HACL* [11], BearSSL [9], NaCL [10]), we replay known
does not scale in the context of binary-level analysis because             bugs in 42 samples (incl. Lucky13 [50]) and automati-
of the representation of the memory as a single large array                cally generate counterexamples (Section VII-A).
which prevents sharing between executions, sending a high               • Simon et al. [12] have demonstrated that clang’s op-
number of queries to the constraint solver which could have                timizations break constant-timeness of code. We extend
been simplified beforehand with a better information flow                  this work in four directions – from 192 in [12] to
tracking.                                                                  408 configurations (Section VII-A): (1) we automatically
                                                                           analyze the code that was manually checked in [12],
Proposal. We tackle the problem of designing an efficient                  (2) we add new implementations, (3) we add the gcc
symbolic verification tool for constant-time at binary-level               compiler and a more recent version of clang, (4) we
that leverages the full power of symbolic execution without                add ARM binaries. Interestingly, we discovered that gcc
sacrificing correct bug-finding nor bounded-verification. We               -O0 and backend passes of clang with -O3 -m32
present B INSEC /R EL, the first efficient binary-level automatic          -march=i386 introduce violations of CT that cannot
tool for bug-finding and bounded-verification of constant-time             be detected by LLVM verification tools like ct-verif [16].
at binary-level. It is compiler-agnostic, targets x86 and ARM
                                                                     Our technique is shown to be highly efficient on bug-finding
architectures and does not require source code.
                                                                     and bounded-verification compared to alternative approaches,
   The technique is based on relational symbolic execu-              paving the way to a systematic binary-level analysis of CT on
tion [48], [49]. It models two execution traces following            cryptographic implementations, while our experiments demon-
the same path in the same symbolic execution instance and            strate the importance of developing CT-verification tools rea-
maximizes sharing between them. We show via experiments              soning at binary-level. Besides CT, the technique can be
(Section VII-B) that RelSE (and ShadowSE) alone does not             readily adapted to other hyperproperties of interest in security
scale at binary-level to analyze CT on real cryptographic            (e.g., cache-side channels, secret-erasure), as long as they are
implementations.                                                     restricted to pairs of traces following the same path.
   Our key technical insights are (1) to use this sharing to
track secret-dependencies and reduce the number of queries                                 II. BACKGROUND
sent to the solver, and (2) to complement it with dedicated            In this section, we present the basics of contant-time and
optimizations offering a fine-grained information flow tracking      symbolic execution. Small examples of CT and standard
in the memory for efficient binary analysis.                         adaptations of symbolic execution are presented in Section III,
   B INSEC /R EL can analyze about 23 million instructions in        while a formal definition of CT is given in Section IV.
98 min, (i.e. 3860 instructions per second), outperforming
similar state of the art binary-level verification tools based on    A. Constant-Time
symbolic execution [20], [43] (cf. Table VIII, page 13), while          Information flow policies regulate the transfer of informa-
being still correct and complete for CT.                             tion between public and secret domains. To reason about infor-
mation flow, we partition the program input into two disjoint               to reason explicitely about the memory in a very precise
sets: low (i.e. public) and high (i.e. secret). Typical information         way. Second, the high level control flow structure (e.g. for
flow properties require that the observable output of a program             loops) is not preserved, and there are dynamic jumps to handle
does not depend on the high input (non-interference). CT is a               (e.g. instruction of the form jmp eax).
special case requiring both the program control flow and the                   Fortunately, it turns out that SE is less difficult to adapt
memory accesses to be independent from high input.                          from source code to binary code than other semantic analysis
   Contrary to a standard safety property which states that                 – due to both the efficiency of SMT solvers and concretization
nothing bad can happen along one execution trace, information               (i.e., simplifying a formula by constraining some variables
flow properties relate two execution traces – they are 2-                   to be equal to their observed runtime values). Hence, strong
hypersafety properties [32]. Unfortunately, the vast major-                 binary-level SE tools do exist and have yielded several highly
ity of symbolic execution tools [37], [51]–[55] is designed                 promising case studies [37], [52]–[55], [61], [62].
for safety verification and cannot directly be applied to 2-
                                                                            Logical notations. Binary-level SE relies on the theory of
hypersafety properties. In principle, 2-hypersafety properties
                                                                            bitvectors and arrays, QF_ABV [63]. Values (e.g. registers,
can be reduced to standard safety properties of a self-composed
                                                                            memory addresses, memory content) are modeled with fixed-
program [33] but this reduction alone does not scale [34].
                                                                            size bitvectors [64]. We will use the type Bvm , where m is a
B. Symbolic Execution                                                       constant number, to represent symbolic bitvector expressions.
   Symbolic Execution (SE) [37], [38], [56] consists in ex-                 The memory is modeled with a logical array [65], [66] of type
ecuting a program on symbolic inputs instead of concrete                    (Array Bv32 Bv8 ) (assuming a 32 bit architecture). A logical
input values. Variables and expressions of the program are                  array is a function (Array I V) that maps each index i ∈ I
represented as terms over symbolic inputs and the current path              to a value v ∈ V. Operations over arrays are:
is modeled by a path predicate (a logical formula), which is                   • select : (Array I V) × I → V takes an array a and an

the conjunction of conditional expressions encountered along                     index i and returns the value v stored at index i in a,
the execution.                                                                 • store : (Array I V) × I × V → (Array I V) takes an

   SE is built upon two main steps. (1) Path search: at                          array a, an index i, and a value v, and returns the array
each conditional statement the symbolic execution forks, the                     a in which i maps to v.
expression of the condition is added to the first branch and                These functions satisfy the following constraints for all
its negation to the second branch, then the symbolic execution              a ∈ (Array I V), i ∈ I, j ∈ I, v ∈ V:
continues along satisfiable branches; (2) Constraint solving:                  • select (store a i v) i = v
the path predicate can be solved with an off-the-shelf auto-                   • i 6= j =⇒ select (store a i v) j = select a j
mated constraint solver, typically SMT [57], to generate a
concrete input exercising the path.                                                          III. M OTIVATING E XAMPLE
   Combining these two steps, SE can explore many different                    Let us consider the toy program in Listing 1. The value of
program paths and generate test inputs exercising these paths.              the conditional at line 3 and the memory access at line 4 are
It can also check local assertions in order to find bugs or                 leaked. We say that a leak is insecure if it depends on the
perform bounded-verification (i.e., verification up to a certain            secret input. Conversely, a leak is secure if it does not depend
depth). Dramatic progresses in program analysis and constraint              on the secret input. CT holds for a program if there is no
solving over the last two decades have made SE a tool of                    insecure leak.
choice for intensive testing [38], [39], vulnerability analy-               1   x := private_input();
sis [52], [58], [59] and other security-related analysis [60],              2   y := public_input();
[61].                                                                       3   if y then return 0; // leak y = 0
C. Binary-Level Symbolic Execution                                          4   else return tab[x]; // leak x
   Low-level code operates on a set of registers and a single                   Listing 1: Toy program with one control-flow leak and
(large) untyped memory. During the execution, a call stack                      one memory leak.
contains information about the active functions such as their                  Let us take two executions of this program with the same
arguments and local variables. A special register esp (stack                public input: (x, y) and (x0 , y 0 ) where y = y 0 . Intuitively, we
pointer) indicates the top address of the call stack and local              can see that the leakages produced at line 3, y = 0 and y 0 = 0,
variables of a function can be referenced as offsets from the               are necessarily equal in both executions because y = y 0 ; hence
initial esp2 .                                                              this leak does not depend on the secret input and is secure.
Binary-level symbolic execution. Binary-level code analysis                 On the contrary, we can see that the leakages x and x0 at line
is notoriously more challenging than source code analysis [35],             4 can differ in both executions (e.g. take x := 0 and x0 := 1);
[36]. First, evaluation and assignments of source code vari-                hence this leak depends on the secret input and is insecure.
ables become memory load and store operations, requiring                       The goal of an automatic analysis is to prove that the leak
                                                                            at line 3 is secure and to return concrete input showing that
  2 esp is specific to x86, but this is generalizable, e.g. sp for ARMv7.   the leak at line 4 is insecure.
Symbolic Execution & Self-Composition (SC). Symbolic                and p0 (typically, the low inputs) are represented as simple
execution can be adapted to the case of CT following the self-      expressions while those that may be different are represented
composition principle. Instead of self-composing the program,       as pairs of expressions. First, this enables to share redundant
we rather self-compose the formula with a renamed version of        parts of p and p0 , reducing the size of the self-composed
itself plus a precondition stating that the low inputs are equal.   formula. Second, variables mapping to simple expressions
Basically, this amounts to model two different executions           cannot depend on the secret input, allowing to easily spare
following the same path and sharing the same low input in           some insecurity queries.
a single formula. At each conditional statement, exploration           As an example, let us perform RelSE of the toy program
queries are sent to the solver to determine satisfiable branches    in Listing 1. Variable x is assigned a pair of expressions
– followed by both executions (similar to standard SE ex-           hβ | β 0 i and y is assigned a simple expression hλi. Note that
ploration). Moreover, additional insecurity queries specific to     the precondition that public variables are equal is now implicit
CT are sent before each conditional statement and memory            since we use the same symbolic variable in both executions. At
access to determine if they depend on the secret or not – if an     line 3, the conditional expression is evaluated to c = hλ > 0i
insecurity query is satisfiable then a CT violation is found.       and we need to check that the leakage of c is secure. Since c
   As an illustration, let us consider the program in Listing 1.    maps to a simple expression, we know by definition that it does
First, we assign symbolic values to x and y and use symbolic        not depend on the secret, hence we can spare the insecurity
execution to generate a formula of the program until the first      query.
conditional (line 3), resulting in the formula: x = β ∧ y =            RelSE maximizes sharing between both executions and
λ ∧ c = (λ > 0). Second, self-composition is applied on the         tracks secret-dependencies enabling to spare insecurity
formula with precondition λ = λ0 to constraint the low inputs       queries and reduce the size of the formula.
to be equal in both executions. Finally, a postcondition c 6= c0
asks whether the value of the conditional can differ, resulting     Challenge of binary-level analysis. Recall that, in binary-
in the following insecurity query:                                  level SE, the memory is represented as a special variable of
                                                                    type (Array Bv32 Bv8 ). We cannot directly store relational
                                                     !
       0        x = β ∧ y = λ ∧ c = (λ > 0) ∧
λ=λ ∧                                                   ∧ c 6= c0   expressions in it, so in order to store high inputs at the
               x0 = β 0 ∧ y 0 = λ0 ∧ c0 = (λ0 > 0)                  beginning of the execution, we have to duplicate it. In other
   This formula is sent to a SMT-solver. If the solver returns      words the memory is always duplicated. Consequently, every
UNSAT , meaning that the query is not satisfiable, then the         select operation will evaluate to a duplicated expression,
conditional does not differ in both executions and thus is          preventing to spare queries in many situations.
secure. Otherwise, it means that the outcome of the conditional        As an illustration, consider the compiled version of the
depends on the secret and the solver will return a counterexam-     previous program, given in Listing 2. The steps of RelSE on
ple satisfying the insecurity query. Here, z3 answers that the      this program are given in Fig. 1. Note that when the secret
query is UNSAT and we can conclude that the leak is secure.         input is stored in memory at line (1), the array representing the
With the same method, the analysis finds that the leak at line 4    memory is duplicated. This propagates to the load expression
is insecure, and returns two inputs (0,0) and (1,0), respectively   in eax at line (3) and to the conditional expression at line (4).
leaking 0 and 1, as a counterexample showing the violation.         Intuitively, at line (4), eax should be equal to the simple ex-
Limits. Basic self-composition suffer from two weaknesses:          pression hλi in which case we could spare the insecurity query
  • It generates lots of insecurity queries – at each condi-
                                                                    like in the previous example. However, because dependencies
    tional statement and memory access. Yet, in the previous        cannot be tracked in the array representing the memory, eax
    example it is clear that the conditional does not depend        evaluates to a pair of select expression and we have to send
    on secrets and could be spared with better information          the insecurity query to the solver.
    flow tracking.                                              1    @[ebp-8] := hβ | β 0 i; // store high input
  • The whole original formula is duplicated so the size of 2        @[ebp-4] := hλi;        // store low input
    the self-composed formula is twice the size of the original 3    eax := @[ebp-4];        // assign hλi to eax
    formula. Yet, because the parts of the program that only 4       ite eax ? l1 : l2 ; // leak hλi
    depend on public inputs are equal in both executions, the 5      [...]
    self-composed formula contains redundancies that are not
    exploited.                                                       Listing 2: Compiled version of the conditional in Listing 1,
                                                                     where x := hβ | β 0 i (resp. x := hλi) denotes that x is
Relational Symbolic Execution (RelSE). We can improve SC             assigned a high (resp. low) input.
by maximizing sharing between the pairs of executions [48],
[49]. As previously, RelSE models two executions of a pro-          Practical impact. We report in Table I the performances
gram P in the same symbolic execution instance, let us call         of CT-analysis on an implementation of elliptic curve
them p and p0 . But in RelSE, variables of P are mapped to          Curve25519-donna [67]. Both SC and RelSE fail to prove the
relational expressions which are either pairs of expressions        program secure in less than 1h. RelSE does reduce the number
or simple expressions. The variables that must be equal in p        of queries w.r.t. SC, but it is not sufficient.
(init)     mem := hµ0 i and ebp := hebpi                                 • l ∈ Loc is the current location, and P.l returns the current
   (1)     mem := hµ1 | µ01 i where µ1 , store(µ0 , ebp − 8, β)            instruction,
                                and µ01 , store(µ0 , ebp − 8, β 0 )      • r : V ar → BVn is a register map that maps variables to

   (2)                     0
           mem := hµ2 | µ2 i where µ2 , store(µ1 , ebp − 4, λ)             their bitvector value,
                                and µ02 , store(µ01 , ebp − 4, λ)        • m : BV32 → BV8 is the memory, mapping 32-bit

   (3)                   0
           eax := hα | α i where α , select(µ2 , ebp − 4)                  addresses to bytes and is accessed by the operator @ (read
                                and α0 , select(µ02 , ebp − 4)             in an expression and write in a left value).
                             0                                         The initial configuration is given by c0 , (l0 , r0 , m0 ) with l0
   (4)     leak hα 6= 0 | α 6= 0i
                                                                       the address of the entrypoint of the program, r0 an arbitrary
Figure 1: RelSE of program in Listing 2 where mem is the
                                                                       register map, and m0 an arbitrary memory.
memory variable, ebp and eax are registers, µ0 , µ1 , µ01 , µ2 , µ02
are symbolic array variables, and ebp, β, β 0 , λ, α, α0 are sym-      Leakage model. The behavior of the program is modeled
bolic bitvector variables                                              with an instrumented operational semantics taken from [69]
                                                                       in which each transition is labeled with an explicit notion of
         Version              #I     #Q     T      #I/s   S
         SC (e.g. [43])       11k   9051    TO        3
                                                                       leakage. A transition from a configuration c to a configuration
         RelSE (e.g. [49])    13k   5486    TO        4                c0 produces a leakage t, denoted c →  − c0 . Analogously, the
                                                                                                             t
         B INSEC /R EL       10M       0   1166   8576    3            evaluation of an expression e in a configuration (l, r, m),
Table I: Performances of CT-analysis of donna compiled with            denoted (l, r, m) e `t bv, produces a leakage t. The leakage
gcc-5.4 -O0, in terms of number of explored unrolled                   of a multistep execution is the concatenation of leakages
instructions (#I), number of queries (#Q), execution time in           produced by individual steps. We use →   − k with k a natural
                                                                                                                t
seconds (T), instructions explored per second (#I/s), and status       number to denote k steps in the concrete semantics.
(S) set to secure (3) or timeout ( ) set to 3600s.                        An excerpt of the concrete semantics is given in Fig. 3
                                                                       where leakage by memory accesses occur during execution of
                                                                       load and store instructions and control flow leakages during
Our solution. To mitigate this issue, we propose dedicated             execution of dynamic jumps and conditionals. The full set of
simplifications for binary-level relational symbolic execution         rules is given in Appendix A1.
that allow a precise tracking of secret-dependencies in the
memory (details in Section V-A). In the particular example
of Table I, our prototype B INSEC /R EL does prove that the code                               (l, r, m) e `t bv
                                                                                  LOAD
is secure in less than 20 minutes. Our simplifications simplify                          (l, r, m) @ e `t·[bv] m bv
all the queries, resulting in a ×2000 speedup compared to                D _ JUMP

standard RelSE and SC in terms of number of instructions                 P.l = goto e           (l, r, m) e `t bv       l0 , to_loc(bv)
                                                                                                               0
treated per second.                                                                          (l, r, m) −−−→
                                                                                                          0
                                                                                                             (l , r, m)
                                                                                                        t·[l ]
         IV. C ONCRETE S EMANTICS & FAULT M ODEL                         T- ITE
                                                                         P.l = ite e ? l1 : l2     (l, r, m) e `t bv          bv 6= 0
Dynamic Bitvectors Automatas (DBA) [68] is used by                                     (l, r, m) −−−→ (l1 , r, m)
B INSEC[55] as an Intermediate Representation to model low-                                            t·[l1 ]
level programs and perform its analysis. The syntax of DBA
programs is presented in Fig. 2.                                                                  P.l = @e := e0
                                                                                    (l, r, m) e `t bv     (l, r, m) e0 `t0 bv0
                                                                             STORE
prog ::= ε | stmt prog         lval ::= v | @ expr                                 (l, r, m) −−
                                                                                              0
                                                                                                −−−→ (l + 1, r, m[bv 7→ bv’])
                                                                                                t ·t·[bv]
stmt ::= < l, inst >          expr ::= v | bv | @ expr
 inst ::= lval := expr                 | u expr                        Figure 3: Concrete evaluation of DBA instructions and expres-
         | ite expr? l1 :l2            | expr b expr                   sions (excerpt), where · is the concatenation of leakages and
         | goto expr | goto l     u ::= ¬ | −                          to_loc : BV32 → Loc converts a bitvector to a location.
         | halt                   b ::= + | × | ≤ | . . .

Figure 2: The syntax of DBA programs, where l, l1 , l2 are             Secure program. Let Hv ⊆ V ar be the set of high (secret)
program locations, v is a variable and bv is a value.                  variables and Lv := V ar \ Hv be the set of low (public)
                                                                       variables. Analogously, we define H@ ⊆ BV32 (resp. L@ :=
   Let Inst denote the set of instructions and Loc the set of          BV32 \ H@ ) as the addresses containing high (resp. low) input
(program) locations. A program P : Loc → Inst is a map                 in the initial memory.
from locations to instructions. Values bv and variables v range           The low-equivalence relation over concrete configurations
                                                     n
over the set of fixed-size bitvectors BVn := {0, 1} (set of n-         c and c0 , denoted c 'L c0 , is defined as the equality of
bit words). A concrete configuration is a tuple (l, r, m) where:       low variables and low parts of the memory. Formally, two
configurations c , (l, r, m) and c0 , (l0 , r0 , m0 ) are low-           Notice that a simple expression hϕi does not depend on
equivalent iff,                                                       secrets and can be leaked securely. Thus it spares an insecurity
                  ∀v ∈ Lv . r v = r0 v                                query to the solver. On the other hand, a duplicated expression
                      ∀a ∈ L@ . m a = m0 a                            hϕl | ϕr i may depend on secrets. Hence an insecurity query
                                                                      must be sent to the solver to ensure that the leak is secure.
Definition 1 (Constant-time up to k). A program is constant-             Detailed explanations of the symbolic evaluation rules fol-
time (CT) up to k iff for all low-equivalent initial configura-       low:
tions c0 and c00 , that evaluate in k steps to ck and c0k producing      LOAD is the evaluation of a load expression. The rule returns
leakages t and t0 ,                                                   a pair of logical select formulas from the pair of symbolic
    c0 'L c00        − k ck ∧ c00 −  k 0
                                       ck =⇒ t = t0
                                                                                      V


                ∧ c0 →            →                                   memories µ (the box in the hypotheses should be ignored
                        t          0    t
                                                                      for now, it will be explained in Section V-A). Note that the
 V. B INARY- LEVEL R ELATIONAL S YMBOLIC E XECUTION                   returned expression is always duplicated as the select must
   Our symbolic execution relies on the QF_ABV [63] first-            be performed in the left and right memories independently.
order logic. We let β, β 0 , λ, ϕ, i, j range over the set of            D _ JUMP is the evaluation of a dynamic jump. The rule
                                                                      finds a concrete value l0 for the jump target, and updates
                                                                 V


formulas Φ in the QF_ABV logic. A relational formula ϕ
is either a QF_ABV formula hϕi or a pair hϕl | ϕr i of two            the path predicate and the location. Note that this rule is
                                                                      nondeterministic as l0 can be any concrete value satisfying the
                                   V            V


QF_ABV formulas. We denote ϕ|l (resp. ϕ|r ), the projection
                                    V       V             V


on the left (resp. right) value of ϕ. If ϕ = hϕi, then ϕ|l and
V
                                                                      constraint. In practice, we call the solver to enumerate jump
ϕ|r are both defined as ϕ. We let Φ be the set of relational          targets up to a given bound and continue the execution along
formulas and Bvn be the set of relational symbolic bitvectors         the valid targets (which jump to an executable section).
of size n.                                                               ITE - TRUE is the evaluation of a conditional jump when

Symbolic configuration. Since we restrict our analysis to pairs       the expression evaluates to true (the false case is analogous).
of traces following the same path – which is sufficient for           The rule updates the path predicate and the next location
constant-time – the symbolic configuration only considers a           accordingly.
single program location l ∈ Loc at any point of the execution.           STORE is the evaluation of a store instruction. The rule
                                                                      evaluates the index and value of the store and updates the
                                                   V
                                                                      symbolic memories and the path predicate with a logical store
A symbolic configuration is of the form l, ρ, µ, π where:
                                                                      operation.
  • l ∈ Loc is the current program point,
  • ρ : V ar → Φ is a symbolic register map, mapping
    variables from a set V ar to their symbolic representation         LOAD
                                                                                                                       ^




    as a relational formula in Φ,                                                                       ρ, µ e ` φ
                                                                                                            ^




      V


  • µ : (Array Bv32 Bv8 ) × (Array Bv32 Bv8 ) is the
                                                                                               ^                            ^                             ^




                                                                        ϕ , hselect(µ|l , φ|l ) | select(µ|r , φ|r )i
                                                                        ^                 ^                         ^




                                                                                                                                                secLeak (φ)
    symbolic memory – a pair of arrays of values in Bv8                                               
    indexed by addresses in Bv32 ,                                                                ρ, µ @e ` ϕ
                                                                                                            ^               ^




  • π ∈ Φ is the path predicate – a conjunction of conditional         D _ JUMP
                                                                                                                     π 0 , π ∧ (ϕ|l = ϕ|r )
                                                                                                       
    statements and assignments encountered along a path.                                          ρ, µ e ` ϕ
                                                                                                       ^            ^                            ^        ^




                                                                       P.l = goto e
                                                                              M  π0              l0 , M (ϕ|l )
                                                                                                                ^                                 ^




                                                                                                                      secLeak (ϕ)
Symbolic evaluation of instructions, denoted s        s0 where s
                                                                                                             l0 , ρ, µ, π 0
                                                                                                    ^                         ^



      0
and s are symbolic configurations, is given in Figure 4 – the                                 l, ρ, µ, π
complete set of rules is given in Appendix    A2. The evaluation        ITE - TRUE
                                   V 
of an expression in a state ρ, µ to a relational formula ϕ,
                                                                V
                                                                                    P.l = ite e ? ltrue: lf alse
                                                                                    l0 , ltrue      ρ, µ e ` ϕ
                                                                                                                        ^               ^
                  V            V


is given by (l, ρ, µ) expr ` ϕ. A model M assigns concrete
                                                                         0
                                                                        π , π ∧ (true = ϕ|l = ϕ|r )       π0
                                                                                                ^           ^                                             ^




values to symbolic variables. The satisfiability of a formula π                                                     secLeak (ϕ)
with a model M is denoted M  π. Whenever the model is                                               0          0
                                                                                                   ^                          ^




                                                                                      l, ρ, µ, π    l , ρ, µ, π
not needed for our purposes, we leave it implicit and simply          STORE
write  π for satisfiability. In the implementation, we use an                                 P.l = @e := e0                                         ^



                                                                                  0
SMT -solver to determine satisfiability of a formula.                                                                  ρ, µ e0 ` φ
                                                                                                                            
                                                                                               ρ, µ e ` ϕ
                                                                                                           ^            ^               ^




                                                                             l =l+1
   For the security evaluation of the symbolic leakage we                     0
                                                                                                                ^                                ^




                                                                             µ , hstore(µ|l , ϕ|l , φ|l ) | store(µ|r , ϕ|r , φ|r )i
                                                                               ^                ^       ^                           ^       ^




define a function secLeak which verifies that a relational              0       0
                                                                                                                ^


                                                                                                                   0
                                                                                                                                                              ^




                                                                       π , π ∧ µ|l = store(µ|l , ϕ|l , φ|l ) ∧ µ|r = store(µ|r , ϕ|r , φ|r )
                                                                                      ^            ^    ^                   ^                    ^    ^




formula in the symbolic leakage does not differ in its right                                                            ^




and left components,    i.e. that the symbolic leakage is secure:                               secLeak (ϕ)
                                                                                                                     0
                                                                                                           l0 , ρ, µ , π 0
                                                                                                   ^                          ^




                                                                                        l, ρ, µ, π
                             V


                
                  true      if ϕ = hϕi
           V                  V                                
secLeak (ϕ)= true if ϕ = hϕl | ϕr i∧ 2 π ∧ (ϕl 6= ϕr                  Figure 4: Symbolic evaluation of DBA instructions and ex-
                
                   f alse otherwise                                   pressions (excerpt).
                
Specification of high and low input. By default, the content         Lookup. The symbolic memory can be seen as the history
of the memory and registers is low so we have to specify             of the successive store operations beginning with the initial
addresses that initially contain secret inputs. The addresses of     memory µ0 . Therefore, a memory select can be resolved by
high variables can be specified as offsets from the initial stack    going back up the history and comparing the index to load,
pointer esp. A pair hβ | β 0 i ∈ Bv8 of fresh symbolic variables     with indexes previously stored. Our optimization consists in
is stored at each given offset h and modifies the symbolic con-      replacing selection in the memory (Figure 4, LOAD rule, boxed
figuration just as a store instruction @[esp + h] := hβ | β 0 i      hypothesis) by a new function lookup : ((Array Bv32 Bv8 )×
would. Similarly, offsets containing low inputs can be set to        (Array Bv32 Bv8 )) × Bv32 → Bv8 which takes a relational
simple symbolic expressions hλi – although it is not necessary       memory and an index, and returns the relational value stored
since the initial memory is equal in both executions.                at that index. The lookup function can be lifted to relational
                                                                     indexes but for simplicity we only define it for simple indexes
Bug-Finding. A vulnerability is found when the function              and assume that relational store operations happen to the same
secLeak (ϕ) evaluates to false. In this case, the insecurity         index in both sides – note that for constant-time analysis, this
query is satisfiable and there exists a model M such that
              V        V
                                                                     hypothesis holds. The function returns a relational bitvector
M  π ∧ (ϕ|l 6= ϕ|r ). The model M assigns concrete                  formula, and is defined as follows:
values to variables that satisfy the insecurity query. Therefore                          V                           V


                                                                               lookup (µ0 , i) = hselect(µ0|l , i) | select(µ0|r , i)i
                                                                                                                                      V




it can be returned as a concrete counterexample which triggers                            V



the vulnerability, along with the current location l of the                      lookup (µn , i) =
                                                                                  
vulnerability.
                                                                                  hϕl i
                                                                                                             if eq # (i, j) ∧ eq # (ϕl , ϕr )
                                                                                                              if eq # (i, j) ∧ ¬eq # (ϕl , ϕr )
                                                                                  
                                                                                  hϕ | ϕ i
                                                                                      l  r
A. Optimizations for binary-level SE                                                                          if ¬eq # (i, j)
                                                                                               V

                                                                                  lookup (µn−1 , i)
                                                                                  
                                                                                    V



                                                                                    φ                         if eq # (i, j) = ⊥
                                                                                  
   Relational symbolic execution does not scale in the context
of binary-level analysis (see RelSE in Table V). In order                where
to achieve better scalability, we enrich our analysis with                       V                 V                        V


                                                                                 µn , hstore(µn−1 |l , j, ϕl ) | store(µn−1 |r , j, ϕr )i
an optimization, called on-the-fly-read-over-write (FlyRow in                    V
                                                                                               V                       V


Table VI), based on read-over-write [66]. This optimization                      φ , hselect(µn|l , i) | select(µn|r , i)i
simplifies expressions and resolves load operations ahead of         where eq # (i, j) is a comparison function relying on syntactic
the solver, often avoiding to resort to the duplicated memory        term equality, which returns true (resp. false) only if i and j
and allowing to spare insecurity queries. We also enrich our         are equal (resp. different) in any interpretation. If the terms
analysis with two further optimizations, called untainting and       are not comparable, it is undefined, denoted ⊥.
fault-packing (Unt and fp in Table VI), specifically targeting
SE for information flow analysis.                                    Example 1 (Lookup). Let us consider the memory:
   1) On-the-Fly Read-Over-Write: Solver calls are the main          V


                                                                                                       ebp − 8 hβ | β 0 i    esp hebpi
                                                                      µ =        ebp − 4 hλi                                                  []
bottleneck of symbolic execution, and reasoning about store
and select operations in arrays is particularly challenging [66].                                  V




Read-over-write (Row) [66] is a simplification for the theory            • A call to lookup (µ, ebp − 4) returns λ.
                                                                                                   V



of arrays that efficiently resolves select operations. This              • A call to lookup (µ, ebp − 8) first compares the indexes

simplification is particularly efficient in the context of binary-         [ebp−4] and [ebp−8]. Because it can determine that these
level analysis because the memory is represented as an array               indexes are syntactically distinct, the function moves to
and formulas contain many store and select operations.                     the second element, determines the syntactic equality of
   The standard read-over-write optimization [66] has been                 indexes and returns hβ | β 0 i.
                                                                                                   V



implemented as a solver-pre-processing, simplifying a formula            • A call to lookup (µ, esp) tries to compare the indexes

before sending it to the solver. While it has proven to be                 [ebp−4] and [esp]. Without further information, the equal-
very efficient to simplify individual formulas of a single                 ity or disequality of ebp and esp cannot be determined,
execution [66], we show in Section VII-B that it does not scale            therefore the lookup is aborted and the select operation
in the context of relational reasoning, where formulas model               cannot be simplified.
two executions and a lot of queries are sent to the solver.
   Thereby, we introduce on-the-fly read-over-write (FlyRow)         Term rewriting. To improve the conclusiveness of this syn-
to track secret-dependencies in the memory and spare inse-           tactic comparison, the terms are assumed to be in normalized
curity queries in the context of information flow analysis.          form β + o where β is a base (i.e. an expression on symbolic
By keeping track of relational store expressions along the           variables) and o is a constant offset. In order to apply FlyRow,
symbolic execution, it can resolve select operations – often         we normalize all the formulas created during the symbolic
avoiding to resort to the duplicated memory – and drastically        execution (details of our normalization function are ommited
reduces the number of queries sent to the solver, improving          for space reasons). The comparison of two terms β + o and
the performances of the analysis.                                    β 0 + o0 in normalized form can be efficiently computed as
                       V                            V
                                                                             accesses along the basic block that evaluate to hϕ | ϕ0 i
       untaint(ρ, µ, hvl | vr i) = (ρ[vr \vl ], µ[vr \vl ])
                V                                                           and hφ | φ0 i, we would normally generate two insecurity
  untaint(ρ, µ, h¬tl | ¬tr i)        
                                                                            queries (π ∧ ϕ 6= ϕ0 ) and (π ∧ φ 6= φ0 ) – one for each
                V                    
  untaint(ρ, µ, h−tl | − tr i)                                               memory access. fp regroupsthese checks into a single query
                                     
                                     
                                     
                                     
                V                                          V


  untaint(ρ, µ, htl + k | tr + ki) = untaint(ρ, µ, htl | tr i)                π ∧ ((ϕ 6= ϕ0 ) ∨ (φ 6= φ0 )) sent to the solver at the end of
                V                                                           the basic block.
  untaint(ρ, µ, htl − k | tr − ki)
                                     
                                     
                                     
                V


  untaint(ρ, µ, htl :: k | tr :: ki)
                                     
                                                                               This optimization reduces the number of insecurity queries
                                                                             sent to the solver and thus helps improving performance.
Figure 5: Untainting rules where vl , vr are bitvector variables             However it degrades the precision of the counterexample:
and tl , tr , k are arbitrary bitvector terms, and f [vr \vl ] indi-         while checking each instruction individually precisely points
cates that the variable vr is substituted with vl in f .                     to vulnerable instructions, fault-packing reduces accuracy to
                                                                             vulnerable basic blocks only. Note that even though disjunctive
                                                                             constraints are usually harder to solve than pure conjunctive
follows: if the bases β and β 0 are syntactically equal, then                constraints, those introduced by fp are very limited (no nesting)
return o = o0 , otherwise the terms are not comparable.                      and thus do not add much complexity. Accordingly, they never
   In order to increase the conclusiveness of FlyRow, we also                end up in a performance degradation (see Table VI).
need variable inlining. However, inlining all variables is not
a viable option as it would lead to an exponential term size                 B. Theorems
growth. Instead, we define a canonical form v + o where v
                                                                                 In order to define properties of our symbolic execution,
is a bitvector variable, and o is a constant bitvector offset,
                                                                             we use →− k (resp. k ), with k a natural number, to denote k
and we only inline formulas that are in canonical form. It
                                                                             steps in the concrete (resp. symbolic) evaluation.
enables rewriting of most of the memory accesses on the stack
                                                                             Definition 2 ( ∼∼p ). We define a concretization relation ∼
which are of the form ebp + bv while avoiding term-size                                      ∼ M                                           ∼ M
                                                                                                                                           ∼p
explosion.                                                                   between concrete and symbolic configurations, where M is a
   2) Untainting: After the evaluation of a rule with the pred-              model and p ∈ {l, r} is a projection on the left or right side
icate secLeak for a duplicated expression hϕl | ϕr i, we know                of a symbolic configuration. Intuitively, the relation c ∼∼ M
                                                                                                                                       ∼p s is
that the equality ϕl = ϕr holds in the current configuration.                the concretization of the p-side of the symbolic state s with the
From this equality, we can deduce useful information about
                                                                                                                                V


                                                                             model M . Let c , (l1 , r, m) and s , l2 , ρ, µ, π . Formally
variables that must be equal in both executions. We can then                 c ∼∼ M
                                                                                ∼p s holds iff M  π, l1 = l2 and for all expression e,
propagate this information to the register map and memory in                 either the symbolic evaluation of e gets stuck or we have
order to spare subsequent insecurity queries concerning these                           V      V            V


                                                                                     ρ, µ e ` ϕ ∧ (M (ϕ|p ) = bv ⇐⇒ c e ` bv)
variables. For instance, consider the leak of the duplicated
                                                                                Notice that because both executions represented in the ini-
expression hvl + 1 | vr + 1i, where vl and vr are symbolic
                                                                             tial configuration s0 are low-equivalent, c0 ∼∼l s0 ∧ c0 ∼
                                                                                                                           ∼ M          0 ∼M
                                                                                                                                           ∼r
variables. If the leak is secure, we can deduce that vl = vr and                                      0
                                                                             s0 implies that c0 'L c0 .
replace all occurrences of vr by vl in the rest of the symbolic
execution.                                 V   V
                                                                                Through this section, we assume that the program P is de-
   We define a function untaint (ρ, µ, ϕ) that takes a register
                     V                                     V
                                                                             fined on all locations computed during the symbolic execution.
map ρ, a memory µ, and a duplicated expression ϕ; it applies                 Under this hypothesis, the symbolic execution can only get
the rules defined in Fig. 5 which deduce variable equalities
                                                                                                         V                                    V



      V                               V
                                                                             stuck when an expression ϕ is leaked such that ¬secLeak (ϕ).
from ϕ, propagate them in ρ and µ, and return a pair of updated              In this case, a vulnerability is detected and there exists a model
                                   0
register map and memory (ρ0 , µ ). Intuitively, if the equality
                                     V                                                                 V         V



                                                                      V
                                                                             M such that M  π ∧ (ϕ|l 6= ϕ|r ).
of variables vl and vr can be deduced from secLeak (ϕ),
                                                                                The following theorem claims the completeness of our
the untaint function replaces occurences of vr by vl in
                                                                             symbolic execution relatively to an initial symbolic state. If
the memory and the register map. As a result, a duplicated
                                                                             the program is constant-time up to k, then for each pair of
expression hvl | vr i would be replaced by the simple expression
                                                                             concrete executions up to k, there exists a corresponding
hvl i in the rest of the execution3 .
                                                                             symbolic execution (no under-approximation). A proof is
   3) Fault-Packing: For CT, the number of insecurity checks
                                                                             given in Appendix B1.
generated along the symbolic execution is substantial. The
fault-packing (fp) optimization gathers these insecurity checks              Theorem 1 (Relative Completeness of RelSE). Let P be a
along a path and postpones their resolution to the end of the                program constant-time up to k and s0 be a symbolic initial
basic block.                                                                 configuration for P . For every concrete states c0 , ck , c00 , c0k ,
Example 2 (Fault-packing). For example, let us consider a                    and model M such that c0 ∼   ∼l s0 ∧ c0 ∼
                                                                                                          ∼ M          0 ∼M
                                                                                                                         ∼r s0 , if c0 →    −k
                                                                                                                                              t
basic-block with a path predicated π. If there are two memory                ck and c00 −→  k 0
                                                                                              ck with t = t0 then there exists a symbolic
                                                                                         t0
  3 We implement untainting with a cache of "untainted variables" that are   configuration sk and a model M 0 such that:
                                                                                                          M0         0 ∼M 0
substituted in the program copy when relational expressions are built.                  s0 k sk ∧ ck ∼  ∼l sk ∧ ck ∼
                                                                                                        ∼              ∼r sk
   The following theorem claims the correctness of our sym-
bolic execution, stating that for each symbolic execution and
model M satisfying the path predicate, the concretization
of the symbolic execution with M corresponds to a valid
concrete execution (no over-approximation). A proof is given
in Appendix B2.
Theorem 2 (Correctness of RelSE). For every symbolic con-
figurations s0 , sk such that s0 k sk and for every concrete
configurations c0 , ck and model M , such that c0 ∼
                                                  ∼  M
                                                  ∼p s0 and
ck ∼∼ M
    ∼p sk , there exists a concrete execution c0 →
                                                   k
                                                 − ck .
  The following is our main result. If the symbolic execution
does not get stuck due to a satisfiable insecurity query, then the      Figure 6: B INSEC architecture with B INSEC /R EL plugin.
program is constant-time. The proof is given in Appendix B3.


Theorem 3 (Bounded-Verification for CT). Let s0 be a                    We explore the program in a depth-first search manner and
symbolic initial configuration for a program P . If the symbolic      we rely on the Boolector SMT-solver [70], currently the best
evaluation does not get stuck, then P is constant-time w.r.t.         on theory QF_ABV [66], [71].
                                     k
s0 . Formally, if for all k, s0         sk then for all initial       Overall architecture is illustrated in Fig. 6. The D ISASM
configurations c0 and c0 and model M such that c0 ∼
                         0                               ∼ M
                                                         ∼l s0 ,      module loads the executable and lifts the machine code to
      0 ∼ M
and c0 ∼∼r s0 ,                                                       the DBA intermediate representation [68]. Then, the analysis
  c0 'L c00          − k ck ∧ c00 −
                ∧ c0 →            →0
                                     k 0
                                       ck =⇒ t = t0                   is performed by the R EL module on the DBA code. The
                        t               t
                                                                      F ORMULA module is in charge of building and simplifying
Additionally, if s0 is fully symbolic, then P is constant-time.
                                                                      formulas, and sending the queries to the SMT-solver. The
  The following theorem expresses that when the symbolic              queries are exported to the SMTLib [63] standard which
execution gets stuck, then there is a concrete path that violates     permits to interface with many off-the-shelf SMT-solvers. The
constant-time. The proof is given in Appendix B4.                     R EL plugin represents ≈3.5k lines of Ocaml.
Theorem 4 (Bug-Finding for CT). Let s0 be an initial sym-             Usability. Binary-level semantic analyzers tend to be harder
bolic configuration for a program P . If the symbolic evaluation      to use than their source-level counterparts as inputs are more
gets stuck in a configuration sk then P is not constant-time.         difficult to specify and results more difficult to interpret.
Formally, if there exists k st. s0 k sk and sk is stuck, then         In order to mitigate this point, we propose a vizualisation
there exists a model M and concrete configurations c0 ∼ ∼ M
                                                        ∼l s0 ,       mechanism (based on IDA, which highlight coverage and vio-
 0 ∼ M          ∼ M           0  ∼M
c0 ∼
   ∼r s0 , ck ∼ ∼l sk and ck ∼   ∼r sk such that,                     lations) and easy input specification (using dummy functions,
                                                                      cf. Appendix C) when source-level information is available.
  c0 'L c00 ∧ c0 →
                 − k ck ∧ c00 −
                              →0
                                 k
                                   c0k ∧ t 6= t0
                            t               t
                                                                                     VII. E XPERIMENTAL R ESULTS
                    VI. I MPLEMENTATION                                  We answer the following research questions:
  We implemented our relational symbolic execution, B IN -            RQ1: Effectiveness Is B INSEC /R EL able to perform
SEC /R EL, on top of the binary-level analyzer B INSEC [55].               constant-time analysis on real cryptographic binaries, for
B INSEC /R EL takes as input a x86 or ARM executable, a spec-              both bug finding and bounded-verification?
ification of high inputs and an initial memory configuration          RQ2: Genericity Is B INSEC /R EL generic enough to encom-
(possibly fully symbolic). It performs bounded exploration of              pass several architectures and compilers?
the program under analysis (up to a user-given depth), and            RQ3: Comparison vs. Standard Approaches How               does
reports the identified CT violations together with counterexem-            B INSEC /R EL scale compared to traditional approaches
ples (i.e., initial configurations leading to the vulnerabilities).        based on standard SC and RelSE?
In case no violation is reported, if the initial configuration is     RQ4: Impact of simplifications What are the respective im-
fully symbolic and the program has been explored exhaustively              pacts of our different simplifications?
then the program is proven secure.                                    RQ5: Comparison vs. SE What is the overhead of B IN -
   B INSEC /R EL is composed of a relational symbolic ex-                  SEC /R EL compared to standard SE, and can our simpli-
ploration module and an insecurity analysis module. The                    fications be useful for standard SE?
symbolic exploration module chooses the path to explore,                 Experiments were performed on a laptop with an Intel(R)
updates the symbolic configuration, builds the path predicate         Core(TM) i5-2520M CPU @ 2.50GHz processor and 32GB
and ensure that it is satisfiable. The insecurity analysis module     of RAM, running Linux Mint 18.3 Sylvia. Similarly to related
builds insecurity queries and check that they are not satisfiable.    work (e.g. [23]), esp is initialized to a concrete value, we
                                                                                                                     ≈ #I        #Iu       T         S
start the analysis from the beginning of the main function,                                             ct-select    1015         1507     .21    29 × 3
we statically allocate data structures and the length of keys                                             ct-sort    2400         1782     .24    12 × 3
                                                                                   utility
and buffers is fixed (e.g. for Curve25519-donna [67], three                                                Hacl*     3850       90953     9.34   110 × 3
                                                                                                       OpenSSL       4550         5113     .75   130 × 3
256-bit buffers are used to store the input, the output and the                                             -O0       290          953     .12       3
secret key). When not stated otherwise, programs are compiled                      tea
                                                                                                            -O3       250          804     .12       3
for x86 (32bit) with their default compiler setup.                                                          -O0      7083       10.2M    1166        3
                                                                                   donna
                                                                                                            -O3      4643        2.7M      401       3
A. Effectiveness (RQ1,RQ2)                                                                               salsa20     1627         6.5k      .7       3
                                                                                                       chacha20      2717        30.0k     5.0       3
                                                                                   libsodium
   We carry out three experiments to assess the effectiveness                                            sha256      4879        38.7k     4.5       3
of our technique: (1) bounded-verification of secure crypto-                                             sha512     16312        62.1k     7.1       3
                                                                                                       chacha20      1221         5.0k     1.0       3
graphic primitives previously verified at source- or LLVM-                                           curve25519      8522        9.4M    1110        3
                                                                                   Hacl*
level [11], [15], [16], (2) automatic replay of known bug                                                sha256      1279        16.8k     2.8       3
studies [12], [16], [50], (3) automatic study of CT preservation                                         sha512      2013        31.8k     4.3       3
                                                                                                          aes_ct      357         3.5k      .6       3
by compilers extending prior work [12]. Overall, our study                         BearSSL
                                                                                                          des_ct      682        38.5k    33.9       3
encompasses 338 representative code samples for a total of                         OpenSSL     tls-rempad-patch       424        35.7k     406       3
70k machine instructions and 22M unrolled instructions (i.e.,                      Total                            64114       22.7M    3154    296 × 3
instructions explored by B INSEC /R EL).
                                                                                 Table II: Bounded verification of constant-time cryptographic
Bounded-Verification (RQ1). We analyze a large range of                          implementations where #I (resp. #Iu ) is the number of static
secure constant-time cryptographic primitives (296 samples,                      (resp. unrolled) instructions, T is the execution time in sec-
64k instructions), comprising: (1) several basic constant-time                   onds, and S is the status ( for timeout or 3 for exhaustive
utility functions such as selection functions [12], sort func-                   exploration).
tions [72] and utility functions from HACL*4 and OpenSSL5 ;
(2) a set of representative constant-time cryptographic prim-
                                                                                    Results are reported in Table III with fault-packing disabled
itives already studied in the literature on source code [15]
                                                                                 to report vulnerabilities at the instruction level. All bugs have
or LLVM [16], including implementations of TEA [73],
                                                                                 been found within the timeout. Interestingly, we found 3
Curve25519-donna [67], aes and des encryption functions
                                                                                 unexpected binary-level vulnerabilities (from secure source
taken from BearSSL [9], cryptographic primitives from lib-
                                                                                 codes) that slipped through previous analysis:
sodium [10] and the constant-time padding remove function
                                                                                    • function ct_select_v1 [12] was deemed secured
tls-cbc-remove-padding from OpenSSL [16]; (3) a set
of functions from the HACL* library [11].                                             through binary-level manual inspection, still we confirm
   Results are reported in Table II. For each program, B IN -                         that any version of clang with -O3 introduces a secret-
SEC /R EL is able to perform an exhaustive exploration without
                                                                                      dependent conditional jump which violates constant-time;
                                                                                    • functions ct_sort and ct_sort_mult, verified by
finding any violations of constant-time in less than 20 min-
utes. Note that exhaustive exploration is possible because in                         ct-verif [16] (LLVM bytecode compiled with clang),
cryptographic programs, bounding the input size bounds loops.                         are vulnerable when compiled with gcc -O0 or clang
These results show that B INSEC /R EL can perform bounded-                            -O3 -m32 -march=i386.
verification of real-world cryptographic implementations at                      A few more details on these vulnerabilities are provided
binary-level in a reasonable time, which was impractical with                    in the next study. Finally, we describe the application of
previous approaches based on self-composition or standard                        B INSEC /R EL to the Lucky13 attack in Appendix D.
RelSE (see Section VII-B).                                                                                                 CT
                                                                                                             ≈ #I #Iu       T   S      Comment
   This is the first automatic CT-analysis of these crypto-                                                                 src
graphic libraries at the binary-level.                                                            ct-select 735 767 .29 Y 21×7 21 1 new 7
                                                                                 utility
                                                                                                    ct-sort 3600 7513 13.3 Y 18×7 44 2 new 7
Bug-Finding (RQ1). We take three known bug studies from                                            aes_big 375 873 1574 N       7   32    -
                                                                                 BearSSL
                                                                                                   des_tab 365 10421 9.4 N      7    8    -
the literature [12], [50], [72] and replay them automatically at                 OpenSSL tls-rempad-luk13 950 11372 2574 N      7    5    -
binary-level (42 samples, 6k instructions), including: (1) bina-                 Total                      6025 30946 4172 - 42×7 110    -
ries compiled from constant-time sources of a selection func-
tion [12] and sort functions [72], (2) non-constant-time ver-                    Table III: Bug-finding of constant-time in cryptographic imple-
sions of aes and des from BearSSL [9], (3) the non-constant-                     mentations where #I (resp. #Iu ) is the number of static (resp.
time version of OpenSSL’s tls-cbc-remove-padding6                                unrolled) instructions, T is the execution time in seconds, CT
responsible for the famous Lucky13 attack [50].                                  src means that the source is constant-time, S is the status (7
                                                                                 for insecure program), and is the number of bugs.
  4 https://github.com/project-everest/hacl-star/blob/master/snapshots/hacl-c/
Hacl_Policies.c and https://github.com/project-everest/hacl-star/blob/master/
snapshots/hacl-c/kremlib_base.h
                                                                                 Effects of compiler optimizations on CT (RQ1, RQ2).
  5 https://github.com/xbmc/openssl/blob/master/crypto/constant_time_locl.h      Simon et al. [12] manually analyse whether clang optimiza-
  6 https://github.com/openssl/openssl/blob/OpenSSL_1_0_1/ssl/d1_enc.c           tions break the constant-time property, for 5 different versions
of a selection function. We reproduce their analysis in an                   ARM. Overall, it demonstrates that B INSEC /R EL does scale
automatic manner and extend it significantly, adding: 29 new                 to realistic applications for both bug-finding and bounded-
functions, a newer version of clang, the ARM architecture,                   verification (RQ1), and that the technology is generic (RQ2).
the gcc compiler and arm-linux-gnueabi-gcc version                           We also get the following interesting side results:
5.4.0 for ARM – for a total of 408 executables (192 in the                      • We proved CT-secure 296 binaries of interest;
initial study). Results are presented in Table IV.                              • We found 3 new vulnerabilities that slipped through pre-
                                                                                   vious analysis – manual on binary code [12] or automated
                         cl-3.0 cl-3.9 cl-7.1   gcc-5.4 gcc-8.3   arm-gcc
                        O0 O3 O0 O3 O0 O3       O0 O3 O0 O3       O0 O3            on LLVM [16];
ct_select_v1            3 7 3 7 3 7             3 3 3 3           3 3           • We significantly extend and automate a previous study on
ct_select_v2            3 7 3 7 3 7             3 3 3 3           3 3              effects of compilers on CT [12];
ct_select_v3            3 3 3 7 3 7             3 3 3 3           3 3
                                                                                • We found that gcc optimizations tend to help enforcing
ct_select_v4            3 7 3 7 3 7             3 3 3 3           3 3
select_naive (insecure) 7 7 7 7 7 7              7 7 7 7           7 3             CT – on ARM, gcc even sometimes produces secure
ct_sort                 3 7 3 7 3 3              7 3 7 3           7 3             binaries from insecure sources.
ct_sort_mult            3 7 3 7 3 3              7 3 7 3           7 3
sort_naive (insecure)    7 7 7 7 7 7             7 7 7 7           7 3       B. Comparisons (RQ3,RQ4,RQ5)
hacl_utility (×11)      3 3 3 3 3 3             3 3 3 3           3 3
openssl_utility (×13) 3 3 3 3 3 3               3 3 3 3           3 3           We compare B INSEC /R EL with standard approaches based
tea_encrypt             3 3 3 3 3 3             3 3 3 3           3 3        on self-composition (SC) and relational symbolic execution
tea_decrypt             3 3 3 3 3 3             3 3 3 3           3 3
                                                                             (RelSE) (RQ3), then we analyze the performances of our
Table IV: Constant-time analysis of several functions compiled               different simplifications (RQ4), and finally we investigate
with gcc or clang (cl) and optimization levels O0 or 03. 3                   the overhead of B INSEC /R EL compared to standard SE, and
indicate that the program is secure and 7 that it is insecure.               whether our simplifications are useful for SE (RQ5).
Bold programs and compilers are extensions of [12] and 7                        Experiments are performed on the programs introduced in
indicates a different result than [12].                                      Section VII-A for bug-finding and bounded-verification (338
                                                                             samples, 70k instructions). We report the following metrics:
   We confirm the main conclusion of Simon et al. [12] that                  total number of unrolled instruction #I, number of instruction
clang is more likely to optimize away CT protections as                      explored per seconds (#I/s), total number of queries sent
the optimization level increases. Yet, contrary to their work,               to the solver (#Q), number of exploration (resp. insecurity)
our experiments show that newer versions of clang are                        queries (#Qe ), (resp. #Qi ), total execution time (T), timeouts
not necessarily more likely than older ones to break CT                      ( ), programs proven secure (3), programs proven insecure
(e.g. ct_sort is compiled to a non-constant-time code with                   (7), unknown status (∼). Timeout is set to 3600 seconds.
clang-3.9 but not with clang-7.1).                                           Comparison vs. Standard Approaches (RQ3). We evaluate
   Surprisingly, in contrast with clang, gcc optimizations                   B INSEC /R EL against SC and RelSE. Since no implementation
tend to remove branches and thus, are less likely to introduce               of these methods fit our particular use-cases, we implement
vulnerabilities in constant-time code. Especially, gcc for ARM               them directly in B INSEC. RelSE is obtained by disabling
produces secure binaries from the insecure source codes 7                    B INSEC /R EL optimizations (Section V-A), while SC is imple-
sort_naive and select_naive.                                                 mented on top of RelSE by duplicating low inputs instead of
   Although [12] reports that the ct_select_v1 function                      sharing them and adding the adequate preconditions. Results
is secure in all their settings, we find the opposite. Manual                are given in Table V.
inspection confirms that clang with -O3 introduces a secret-
dependent conditional jump violating constant-time.                                          #I  #I/s #Q #Qe #Qi      T       3 7 ∼
   Finally, as previously discussed, we found that the                       SC             252k  3.9 170k 16k 154k 65473 15 282 41 15
                                                                             RelSE          320k  5.4 97k 19k 78k 59316 14 283 42 13
ct_sort and ct_sort_mult functions, taken from the
                                                                             B INSEC /R EL 22.8M 3861 3.9k 2.7k 1.3k 5895 0 296 42 0
benchmark of the ct-verif [16] tool, can be compiled
to insecure binaries. Those vulnerabilities are out of reach                        Table V: B INSEC /R EL vs. standard approaches
of ct-verif because it targets LLVM code compiled with
clang, while the vulnerabilities are either introduced by                       While RelSE performs slightly better than SC (×1.38
gcc or by backend passes of clang – we did confirm                           speedup) thanks to a noticeable reduction of the number of
that ct-verif with the setting -clang-options="-O3                           queries (≈50%), both techniques are not efficient enough on
-m32 -march=i386" does not report the vulnerability.                         binary code: RelSE times out in 14 cases and achieves an
                                                                             analysis speed of only 5.4 instructions per second while SC
Conclusion (RQ1, RQ2). We perform an extensive analysis                      is worse. B INSEC /R EL completely outperforms both previous
over 338 samples of representative cryptographic primitive                   approaches, especially its simplifications drastically reduce
studied in the literature [11], [15], [16], compiled with dif-               the number of queries sent to the solver (×60 less insecurity
ferent versions and options of clang and gcc, over x86 and                   queries than RelSE):
   7 The compiler takes advantage of the many ARM conditional instructions      • B INSEC /R EL reports no timeout, it is 715 times faster
to remove conditional jumps.                                                      than RelSE and 1000 times faster than SC;
    Version       #I   #I/s #Q    #Qe     #Qi  T      3 7 ∼
                                                                       • FlyRow completely outperforms PostRow. First, PostRow
Standard RelSE with Unt and fp
RelSE            320k 5.4 96919 19058 77861 59316 14 283 42 13
                                                                         is not designed for relational verification and must reason
+ Unt            373k 8.4 48071 20929 27142 44195 8 288 42 8             about pairs of memory. Second, PostRow simplifica-
+ fp             391k 10.5 33929 21649 12280 37372 7 289 42 7            tions are not propagated along the execution and must
B INSEC /R EL (RelSE + FlyRow + Unt + fp)                                be recomputed for every query, producing a significant
RelSE+FlyRow 22.8M 3075 4018 2688 1330 7402 0 296 42 0
+ Unt           22.8M 3078 4018 2688 1330 7395 0 296 42 0
                                                                         simplification-time overhead. On the contrary, FlyRow
+ fp            22.8M 3861 3980 2688 1292 5895 0 296 42 0                models a single memory containing relational values and
                                                                         propagates along the symbolic execution.
  Table VI: Performances of B INSEC /R EL simplifications.             • FlyRow also improves the performance of standard SE
                                                                         by a factor 450, performing much better than PostRow in
  •   B INSEC /R EL performs bounded-verification of large pro-          our experiments.
      grams (e.g. donna, des_ct, chacha20, etc.) that were           Conclusion (RQ3, RQ4, RQ5). B INSEC /R EL performs signif-
      out of reach of standard methods.                              icantly better than previous approaches to relational symbolic
Performances of Simplifications (RQ4). We consider on-               execution (×715 speedup vs. RelSE). The very main source
the-fly read-over-write (FlyRow), untainting (Unt) and fault-        of improvement is the FlyRow on-the-fly simplification (×569
packing (fp). Results are reported in Table VI:                      speedup vs. RelSE, ×60 less insecurity queries). Note that,
   • FlyRow is the major source of improvement in B IN -             in our context, FlyRow completely outperforms state-of-the-
      SEC /R EL, drastically reducing the number of queries sent     art binary-level simplifications, as they are not designed to
      to the solver and allowing a ×569 speedup w.r.t. RelSE;        efficiently cope with relational properties and introduce a sig-
   • Untainting and fault-packing do have a positive impact on       nificant simplification-overhead at every query. Fault-packing
      RelSE (untainting alone reduces the number of queries by       and untainting, while effective over RelSE, have a much
      50%, the two optimizations together yield a ×2 speedup);       slighter impact once FlyRow is activated; fault-packing can
   • Yet, their impact is more modest once FlyRow is ac-             still be useful when report precision is not the main concern.
      tivated: untainting leads to a very slight speedup, while      Finally, in our experiments, FlyRow significantly improves the
      fault-packing still achieves a ×1.25 speedup.                  performance of standard SE (×450 speedup).
Still, fp can be interesting on some particular programs, when                             VIII. D ISCUSSION
the precision of the bug report is not the priority. Consider for
instance the non-constant-time version of aes in BearSSL (i.e.       Implementation limitations. Our implementation shows three
aes_big): B INSEC /R EL without fp reports 32 vulnerable             main limitations commonly found in research prototypes: it
instructions in 1580 seconds, while B INSEC /R EL with fp            does not support dynamic libraries – executable must be
reports 2 vulnerable basic blocks (covering the 32 vulnerable        statically linked or stubs must be provided for external function
instructions) in only 146 seconds.                                   calls, it does not implement predefined syscall stubs, and it
Comparison vs. Standard SE (RQ5). Standard SE is directly            does not support floating point instructions. These problems
implemented in the R EL module and models a single execution         are orthogonal to the core contribution of this paper and the
of the program with exploration queries but without insecurity       two first ones are essentially engineering tasks. Moreover, the
queries. We also consider a recent implementation of read-           prototype is already efficient on real-world case studies.
over-write [66] implemented as a formula pre-processing,
                                                                     Threats to validity in experimental evaluation. We assessed
posterior to SE (PostRow). Results are presented in Table VII.
                                                                     the effectiveness of our tool on several known secure and
                              #I    #I/s    #Q       T               insecure real-world cryptographic binaries, many of them
                      SE     440k   15.1   23453   29122    7        taken from prior studies. All results have been crosschecked
        SE+PostRow[66]       509k   18.5   27252   27587    7
             SE+FlyRow      22.8M   6804    2688    3346    0        with the expected output, and manually reviewed in case of
                  RelSE      320k    5.4   96919   59316   14        deviation.
         RelSE+PostRow       254k    4.0   75043   63693   16           Our prototype is implemented as part of B INSEC [55],
            B INSEC /R EL   22.8M   3861    3980    5895    0
                                                                     whose efficiency and robustness have been demonstrated in
Table VII: Performances of relational symbolic execution             prior large scale studies on both adversarial code and managed
compared to standard symbolic execution with/without binary          code [61], [74]–[76]. The IR lifting part has been positively
level simplifications.                                               evaluated in external studies [53], [77] and the symbolic
                                                                     engine features aggressive formula optimizations [66]. All our
  •   The overhead of B INSEC /R EL compared to our best             experiments use the same search heuristics (depth-first) and,
      setting for SE (SE+FlyRow), in terms of speed (#I/s),          for bounded-verification, smarter heuristics do not change the
      is only ×1.8. Hence CT comes almost for free on top            performances. Also, we tried Z3 and confirmed the better
      of standard SE. This is consistent with the fact that          performance of Boolector.
      our simplifications discard most insecurity queries, letting      Finally, we compare our tool to our own versions of SC
      only the exploration queries which are also part of SE.        and RelSE, primarily because none of the existing tools can
                                                                     Tool             Target Analysis       Technique         P/BV/BF/C
be easily adapted for our setting, and also because this allows      ct-ai [15]         C     static  abstract-interpretation  3/3/7/7
comparing very close implementations.                                FlowTracker [81] LLVM static          type-system         3/3/7/7
                                                                     ct-verif [16]    LLVM static logical, product-programs 3/3/7∗ / 7
                     IX. R ELATED W ORK                              Casym [17]‡      LLVM static       over-approx. SE        3/3/7/7
                                                                     VirtualCert† [8]  x86    static       type-system         3/3/7/7
   Related work has already been lengthly discussed along the        ctgrind [18]     binary dynamic         Valgrind          7/7/7/3
paper. We add here only a few additional discussions, as well        CacheAudit [24]‡ binary static   abstract-interpretation  3/3/7/7
as an overview of existing SE-based tools for information flow       CacheD [20]‡     binary dynamic           DSE             7/7/3/3
(Table VIII) and an overview of (other) existing automatic           B INSEC /R EL    binary   SE        RelSE + simpl.        7/3/3/3
analyzers for CT (Table IX), partly taken from [16].                 Table IX: Automatic analysis tools for CT-like properties
Tool               Target NI  Technique    P/BV/BF/C ≈XP max Iu /s   (see [16]). ∗ ct-verif can be incomplete because of invariant
RelSym [49]       imp-for 3     RelSE       3/3/3/3    10 loc NA     inference. † As part of CompCert, cannot be used on arbitrary
IF-exploit[41]      Java 3        SC        3/3/3/3    20 loc NA     executables. ‡ Also implements a cache model.
Type-SC-SE[42]       C    3 type-based SC 7/7/3/3      20 loc NA
Casym [17]         LLVM 3 SC+over-approx 3/3/7/7      200 (C) NA
IF-low-level [40] binary 3 SC + invariants 3/3/7/7     250 Is NA
IF-firmware[43] binary 7 SC + concretize 7/7/3/3      500k Iu 260    take the opposite side and sacrifice precision for scalability
CacheD [20]       binary 7 concret+tainting 7/7/3/3   31M Iu 2010    (no bug-finding). Their analysis scales by over-approximating
B INSEC /R EL     binary 7 RelSE + simpl. 7/3/3/3     10M Iu 3861    loops and resetting the symbolic state at chosen code locations.
Table VIII: SE-based tools for Information Flow. NI indi-               We adopt a different approach and scale by heavy formula
cates whether the technique handles general non-interference         optimizations, allowing us to keep both correct bug-finding
(diverging paths) or not (CT-like properties), P: proof, BV:         (BF) and correct bounded-verification (BV). Interestingly, our
bounded-verification, BF: bug-finding, C: counterexample. Is :       method is faster than these approximated ones. We propose
static instr., Iu : unrolled instr., NA: non-applicable.             the first technique for CT-verification at binary-level that is
                                                                     correct for BF and BV and scales on real world cryptographic
                                                                     examples. Moreover, our technique is compatible with the
Self-compositon and SE has first been used by Milushev et            previous approximations for extra-scaling.
al. [42]. They use type-directed self-composition and dynamic
symbolic execution to find bugs of noninterference but they do       Other Methods for CT Analysis. Static approaches based
not address scalability and their experiments are limited to toy     on sound static analysis [8], [14]–[16], [22]–[24], [79]–[81]
examples. The main issues here are the quadratic explosion of        give formal guarantees that a program is free from time
the search space (due to the necessity of considering diverging      side-channels but they cannot find bugs when a program is
paths) and the complexity of the underlying formulas. Later          rejected. Some works also propose program transformations
works [40], [41] suffer from the same problems.                      to make a program secure [17], [79], [80], [82], [83] but
   Instead of considering the general case of noninterference,       they consider less capable attackers and target higher-level
we focus on CT, and we show that it remains tractable for SE         code. Dynamic approaches for constant-time are precise (they
with adequate optimizations.                                         find real violations) but limited to a subset of the execution
                                                                     traces, hence they are not complete. These techniques include
Relational symbolic execution. Shadow Symbolic Execu-                statistical analysis [84], dynamic binary instrumentation [18],
tion [48], [78] aims at efficiently testing evolving softwares       [21], and dynamic symbolic execution (DSE) [19].
by focusing on the new behaviors introduced by a patch.
The paper introduces the idea of sharing formulas across                                    X. C ONCLUSION
two executions in the same SE instance. The term relational             We tackle the problem of designing an automatic and
symbolic execution has been coined more recently [49] but            efficient binary-level analyzer for constant-time, enabling both
this work is limited to a simple toy imperative language and         bug-finding and bounded-verification on real-world crypto-
do not address scalability.                                          graphic implementations. Our approach is based on relational
   We maximize sharing between pairs of executions, as Shad-         symbolic execution together with original dedicated optimiza-
owSE does, but we also develop specific optimizations tailored       tions reducing the overhead of relational reasoning and allow-
to the case of binary-level CT. Experiments show that our            ing for a significant speedup. Our prototype, B INSEC /R EL,
optimizations are crucial in this context.                           is shown to be highly efficient compared to alternative ap-
                                                                     proaches. We used it to perform extensive binary-level CT
Symbolic execution for CT. Only three previous works in
                                                                     analysis for a wide range of cryptographic implementations
this category achieve scalability, yet at the cost of either
                                                                     and to automate and extend a previous study of CT preserva-
precision or soundness. Wang et al. [20] and Subramanyan
                                                                     tion by compilers. We found three vulnerabilities that slipped
et al. [43] sacrifice soundness for scalability (no bounded-
                                                                     through previous manual and automated analyses, and we
verification). The former performs symbolic execution on fully
                                                                     discovered that gcc -O0 and backend passes of clang
concrete traces and only symbolize the secrets. The latter
                                                                     introduce violations of CT out of reach of state-of-the-art CT
concretizes memory accesses. In both cases, they may miss
                                                                     verification tools at LLVM or source level.
feasible paths as well as vulnerabilities. Brotzman et al. [17]
                           R EFERENCES                                      [20]   S. Wang, P. Wang, X. Liu, D. Zhang, and D. Wu,
 [1]   D. Brumley and D. Boneh, “Remote timing attacks are                         “Cached: Identifying cache-based timing channels in
       practical”, Computer Networks, vol. 48, no. 5, 2005.                        production software”, in USENIX, 2017.
 [2]   B. B. Brumley and N. Tuveri, “Remote timing attacks                  [21]   J. Wichelmann, A. Moghimi, T. Eisenbarth, and B.
       are still practical”, in ESORICS, 2011.                                     Sunar, “Microwalk: A framework for finding side chan-
 [3]   P. C. Kocher, “Timing attacks on implementations of                         nels in binaries”, in ACSAC, 2018.
       Diffie-Hellman, RSA, DSS, and other systems”, in                     [22]   B. Köpf, L. Mauborgne, and M. Ochoa, “Automatic
       Annual International Cryptology Conference, 1996.                           Quantification of Cache Side-Channels”, in CAV, 2012.
 [4]   D. J. Bernstein, “Cache-timing attacks on AES”, 2005.                [23]   G. Doychev, B. Köpf, L. Mauborgne, and J. Reineke,
 [5]   D. A. Osvik, A. Shamir, and E. Tromer, “Cache attacks                       “CacheAudit: A Tool for the Static Analysis of Cache
       and countermeasures: The case of AES”, in CT-RSA,                           Side Channels”, ACM Transactions on Information and
       2006.                                                                       System Security, vol. 18, no. 1, 2015.
 [6]   C. Percival, “Cache missing for fun and profit”, 2009.               [24]   G. Doychev and B. Köpf, “Rigorous analysis of soft-
 [7]   E. Ronen, K. G. Paterson, and A. Shamir, “Pseudo                            ware countermeasures against cache attacks”, in PLDI,
       constant time implementations of TLS are only pseudo                        2017.
       secure”, in CCS, 2018.                                               [25]   J. B. Almeida, M. Barbosa, G. Barthe, A. Blot, B. Gré-
 [8]   G. Barthe, G. Betarte, J. D. Campo, C. D. Luna, and D.                      goire, V. Laporte, T. Oliveira, H. Pacheco, B. Schmidt,
       Pichardie, “System-level non-interference for constant-                     and P. Strub, “Jasmin: High-assurance and high-speed
       time cryptography”, in CCS, 2014.                                           cryptography”, in CCS, 2017.
 [9]   T. Pornin, BearSSL. [Online]. Available: https://www.                [26]   B. Bond, C. Hawblitzel, M. Kapritsos, K. R. M. Leino,
       bearssl.org/ (visited on 05/23/2019).                                       J. R. Lorch, B. Parno, A. Rane, S. T. V. Setty, and
[10]   D. J. Bernstein, T. Lange, and P. Schwabe, “The security                    L. Thompson, “Vale: Verifying high-performance cryp-
       impact of a new cryptographic library”, in LATIN-                           tographic assembly code”, in USENIX, 2017.
       CRYPT, 2012.                                                         [27]   S. Cauligi, G. Soeller, F. Brown, B. Johannesmeyer,
[11]   J. K. Zinzindohoué, K. Bhargavan, J. Protzenko, and B.                      Y. Huang, R. Jhala, and D. Stefan, “Fact: A flexi-
       Beurdouche, “Hacl*: A verified modern cryptographic                         ble, constant-time programming language”, in SecDev,
       library”, in CCS, 2017.                                                     2017.
[12]   L. Simon, D. Chisnall, and R. J. Anderson, “What you                 [28]   Z. Zhou, M. K. Reiter, and Y. Zhang, “A software ap-
       get is what you C: controlling side effects in mainstream                   proach to defeating side channels in last-level caches”,
       C compilers”, in EuroS&P, 2018.                                             in CCS, 2016.
[13]   T. Kaufmann, H. Pelletier, S. Vaudenay, and K. Ville-                [29]   F. Liu, Q. Ge, Y. Yarom, F. McKeen, C. V. Rozas,
       gas, “When constant-time source yields variable-time                        G. Heiser, and R. B. Lee, “Catalyst: Defeating last-
       binary: Exploiting curve25519-donna built with MSVC                         level cache side channel attacks in cloud computing”,
       2015”, in CANS, 2016.                                                       in HPCA, 2016.
[14]   J. B. Almeida, M. Barbosa, J. S. Pinto, and B.                       [30]   Q. Ge, Y. Yarom, T. Chothia, and G. Heiser, “Time
       Vieira, “Formal verification of side-channel counter-                       protection: The missing OS abstraction”, in EuroSys,
       measures using self-composition”, Sci. Comput. Pro-                         2019.
       gram., vol. 78, no. 7, 2013.                                         [31]   D. Gruss, J. Lettner, F. Schuster, O. Ohrimenko, I.
[15]   S. Blazy, D. Pichardie, and A. Trieu, “Verifying                            Haller, and M. Costa, “Strong and efficient cache side-
       constant-time implementations by abstract interpreta-                       channel protection using hardware transactional mem-
       tion”, in ESORICS, 2017.                                                    ory”, in USENIX, 2017.
[16]   J. B. Almeida, M. Barbosa, G. Barthe, F. Dupressoir,                 [32]   M. R. Clarkson and F. B. Schneider, “Hyperproperties”,
       and M. Emmi, “Verifying Constant-Time Implementa-                           Journal of Computer Security, vol. 18, no. 6, 2010.
       tions.”, in USENIX, 2016.                                            [33]   G. Barthe, P. R. D’Argenio, and T. Rezk, “Secure
[17]   R. Brotzman, S. Liu, D. Zhang, G. Tan, and M. Kan-                          information flow by self-composition”, in CSFW, 2004.
       demir, “CaSym: Cache aware symbolic execution for                    [34]   T. Terauchi and A. Aiken, “Secure information flow as
       side channel detection and mitigation”, in S&P, 2019.                       a safety problem”, in SAS, 2005.
[18]   A. Langley, ImperialViolet - Checking that functions are             [35]   G. Balakrishnan and T. W. Reps, “WYSINWYX: what
       constant time with Valgrind, 2010. [Online]. Available:                     you see is not what you execute”, ACM Trans. Program.
       https : / / www. imperialviolet . org / 2010 / 04 / 01 / ctgrind .          Lang. Syst., vol. 32, no. 6, 2010.
       html.                                                                [36]   A. Djoudi, S. Bardin, and É. Goubault, “Recovering
[19]   S. Chattopadhyay, M. Beck, A. Rezine, and A. Zeller,                        high-level conditions from binary programs”, in FM,
       “Quantifying the information leak in cache attacks via                      2016.
       symbolic execution”, in MEMOCODE, 2017.                              [37]   P. Godefroid, M. Y. Levin, and D. Molnar, “SAGE:
                                                                                   Whitebox fuzzing for security testing”, Communica-
                                                                                   tions of the ACM, vol. 55, no. 3, 2012.
[38]   C. Cadar and K. Sen, “Symbolic execution for software       [56]   J. C. King, “Symbolic execution and program testing”,
       testing: Three decades later”, Communications of the               Commun. ACM, vol. 19, no. 7, 1976.
       ACM, vol. 56, no. 2, 2013.                                  [57]   J. Vanegue and S. Heelan, “SMT solvers in software
[39]   E. Bounimova, P. Godefroid, and D. A. Molnar, “Bil-                security”, in WOOT, 2012.
       lions and billions of constraints: Whitebox fuzz testing    [58]   T. Avgerinos, S. K. Cha, B. L. T. Hao, and D. Brumley,
       in production”, in ICSE, 2013.                                     “AEG: automatic exploit generation”, in NDSS, 2011.
[40]   M. Balliu, M. Dam, and R. Guanciale, “Automating            [59]   E. J. Schwartz, T. Avgerinos, and D. Brumley, “Q:
       information flow analysis of low level code”, in CCS,              exploit hardening made easy”, in USENIX, 2011.
       2014.                                                       [60]   B. Yadegari, B. Johannesmeyer, B. Whitely, and S. De-
[41]   Q. H. Do, R. Bubel, and R. Hähnle, “Exploit generation             bray, “A generic approach to automatic deobfuscation
       for information flow leaks in object-oriented programs”,           of executable code”, in S&P, 2015.
       in SEC, 2015.                                               [61]   S. Bardin, R. David, and J. Marion, “Backward-bounded
[42]   D. Milushev, W. Beck, and D. Clarke, “Noninterference              DSE: targeting infeasibility questions on obfuscated
       via symbolic execution”, in Formal Techniques for                  codes”, in S&P, 2017.
       Distributed Systems, 2012.                                  [62]   J. Salwan, S. Bardin, and M. Potet, “Symbolic deobfus-
[43]   P. Subramanyan, S. Malik, H. Khattri, A. Maiti, and                cation: From virtualized code back to the original”, in
       J. M. Fung, “Verifying information flow properties of              DIMVA, 2018.
       firmware using symbolic execution”, in DATE, 2016.          [63]   C. Barrett, P. Fontaine, and C. Tinelli, “The SMT-
[44]   N. Benton, “Simple relational correctness proofs for               LIB Standard: Version 2.6”, Department of Computer
       static analyses and program transformations”, in POPL,             Science, The University of Iowa, Tech. Rep., 2017.
       2004.                                                       [64]   FixedSizeBitVectors Theory, SMT-LIB. [Online]. Avail-
[45]   G. Barthe, J. M. Crespo, and C. Kunz, “Relational                  able: http : / / smtlib . cs . uiowa . edu / theories -
       verification using product programs”, in FM, 2011.                 FixedSizeBitVectors.shtml (visited on 04/02/2019).
[46]   T. H. Austin and C. Flanagan, “Multiple facets for          [65]   ArraysEx Theory, SMT-LIB. [Online]. Available: http:
       dynamic information flow”, in POPL, 2012.                          //smtlib.cs.uiowa.edu/theories-ArraysEx.shtml (visited
[47]   M. Ngo, N. Bielova, C. Flanagan, T. Rezk, A. Russo,                on 04/02/2019).
       and T. Schmitz, “A better facet of dynamic information      [66]   B. Farinier, R. David, S. Bardin, and M. Lemerre, “Ar-
       flow control”, in WWW (Companion Volume), 2018.                    rays made simpler: An efficient, scalable and thorough
[48]   H. Palikareva, T. Kuchta, and C. Cadar, “Shadow of a               preprocessing”, in LPAR, 2018.
       doubt: Testing for divergences between software ver-        [67]   D. J. Bernstein, “Curve25519: New diffie-hellman speed
       sions”, in ICSE, 2016.                                             records”, in Public Key Cryptography, 2006.
[49]   G. P. Farina, S. Chong, and M. Gaboardi, “Relational        [68]   S. Bardin, P. Herrmann, J. Leroux, O. Ly, R. Tabary,
       symbolic execution”, in PPDP, 2019.                                and A. Vincent, “The BINCOA framework for binary
[50]   N. J. AlFardan and K. G. Paterson, “Lucky thirteen:                code analysis”, in CAV, 2011.
       Breaking the TLS and DTLS record protocols”, in S&P,        [69]   G. Barthe, B. Grégoire, and V. Laporte, “Secure com-
       2013.                                                              pilation of side-channel countermeasures: The case of
[51]   C. Cadar, D. Dunbar, and D. R. Engler, “KLEE: Unas-                cryptographic "constant-time"”, in CSF, 2018.
       sisted and Automatic Generation of High-Coverage            [70]   A. Niemetz, M. Preiner, and A. Biere, “Boolector 2.0
       Tests for Complex Systems Programs.”, in OSDI, 2008.               system description”, Journal on Satisfiability, Boolean
[52]   T. Avgerinos, D. Brumley, J. Davis, R. Goulden, T.                 Modeling and Computation, vol. 9, 2014.
       Nighswander, A. Rebert, and N. Williamson, “The             [71]   SMT-COMP. [Online]. Available: https : / / smt - comp .
       mayhem cyber reasoning system”, IEEE Security &                    github.io/2019/results.html (visited on 10/11/2019).
       Privacy, vol. 16, no. 2, 2018.                              [72]   Imdea-software/verifying-constant-time.        [Online].
[53]   V. Chipounov, V. Kuznetsov, and G. Candea, “The S2E                Available: https://github.com/imdea-software/verifying-
       platform: Design, implementation, and applications”,               constant-time (visited on 10/13/2019).
       ACM Trans. Comput. Syst., vol. 30, no. 1, 2012.             [73]   D. J. Wheeler and R. M. Needham, “Tea, a tiny
[54]   Y. Shoshitaishvili, R. Wang, C. Salls, N. Stephens,                encryption algorithm”, in FSE, 1994.
       M. Polino, A. Dutcher, J. Grosen, S. Feng, C. Hauser,       [74]   F. Recoules, S. Bardin, R. B. Bonichon, L. Mounier,
       C. Kruegel, and G. Vigna, “SOK: (State of) The Art                 and M.-L. Potet, “Get rid of inline assembly through
       of War: Offensive Techniques in Binary Analysis”, in               verification-oriented lifting”, in ASE, 2019.
       S&P, 2016.                                                  [75]   B. Farinier, S. Bardin, R. Bonichon, and M. Potet,
[55]   R. David, S. Bardin, T. D. Ta, L. Mounier, J. Feist,               “Model generation for quantified formulas: A taint-
       M. Potet, and J. Marion, “BINSEC/SE: A dynamic                     based approach”, in CAV (2), 2018.
       symbolic execution toolkit for binary-level analysis”, in   [76]   R. David, S. Bardin, J. Feist, L. Mounier, M. Potet,
       SANER, 2016.                                                       T. D. Ta, and J. Marion, “Specification of concretization
       and symbolization policies in symbolic execution”, in                                                            CST
       ISSTA, 2016.                                                                           Expr                            (l, r, m) bv ` bv
[77]   M. Jung, S. Kim, H. Han, J. Choi, and S. K. Cha, “B2r2:
                                                                                                                                     (l, r, m) e ` bv
       Building an efficient front-end for binary analysis”, in             VAR                                           UNOP
                                                                                  (l, r, m) v ` r v                               (l, r, m) u e ` u bv
       The BAR Workshop, Internet Society, 2019.
[78]   C. Cadar and H. Palikareva, “Shadow symbolic execu-                                    (l, r, m) e1 ` bv1        (l, r, m) e2 ` bv2
                                                                                      BINOP
       tion for better testing of evolving software”, in ICSE,                                       (l, r, m) e1 b e2 ` bv1 b bv2
       2014.
                                                                                                              (l, r, m) e `t bv
[79]   J. Agat, “Transforming out timing leaks”, in POPL,                                      LOAD
                                                                                                         (l, r, m) @e `t·[bv] m bv
       2000.
[80]   D. Molnar, M. Piotrowski, D. Schultz, and D. A. Wag-                                                        P.l = goto l0
                                                                                              S _ JUMP
       ner, “The program counter security model: Automatic                                                    (l, r, m) −→ (l0 , r, m)
                                                                              Instr                                     [l]
       detection and removal of control-flow side channel
       attacks”, in ICISC, 2005.                                            D _ JUMP
[81]   B. Rodrigues, F. M. Q. Pereira, and D. F. Aranha,                    P.l = goto e           (l, r, m) e `t bv    l0 , to_loc(bv)
                                                                                                                  0
       “Sparse representation of implicit flows with applica-                                  (l, r, m) −−−→ (l , r, m)
                                                                                                              t·[l0 ]
       tions to side-channel detection”, in CC, 2016.
[82]   S. Chattopadhyay and A. Roychoudhury, “Symbolic                      ITE - TRUE
                                                                             P.l = ite e ? l1 : l2    (l, r, m) e `t bv                  bv 6= 0
       verification of cache side-channel freedom”, IEEE
                                                                                          (l, r, m) −−−→ (l1 , r, m)
       Trans. on CAD of Integrated Circuits and Systems,                                                      t·[l1 ]

       vol. 37, no. 11, 2018.                                               ITE - FALSE
[83]   M. Wu, S. Guo, P. Schaumont, and C. Wang, “Elimi-                     P.l = ite e ? l1 : l2    (l, r, m) e `t bv                  bv = 0
       nating timing side-channel leaks using program repair”,                            (l, r, m) −−−→ (l2 , r, m)
                                                                                                              t·[l2 ]
       in ISSTA, 2018.
[84]   O. Reparaz, J. Balasch, and I. Verbauwhede, “Dude, is                               P.l = v := e       (l, r, m)e `t bv
                                                                                  ASSIGN
       my code constant time?”, in DATE, 2017.                                             (l, r, m) −
                                                                                                     → (l + 1, r[v 7→ bv], m)
                                                                                                          t

                            A PPENDIX                                         STORE
                                                                              P.l = @e := e0      (l, r, m) e `t bv  (l, r, m) e0 `t0 bv0
A. Full Set of rules                                                                  (l, r, m) −−−−−→ (l + 1, r, m[bv 7→ bv’])
                                                                                                     t0 ·t·[bv]
  1) Concrete Evaluation: The full set of rules for the
concrete evaluation is reported in Figure 7.                            Figure 7: Concrete evaluation of DBA instructions and expres-
  2) Symbolic Evaluation: The full set of rules for the                 sions, where · is the concatenation of leakages and to_loc :
symbolic evaluation is reported in Figure 8.                            BV32 → Loc converts a bitvector to a location.

B. Proofs
We recall essential elements that we will use in the proofs.            Proof. (Induction on k). Case k = 0 is trivial.
                                                                           Let ck and c0k be concrete configurations and sk a symbolic
Proposition 1. Concrete semantics is deterministic, c.f. rules
                                                                        configuration for which the inductive hypothesis holds up to
of the concrete semantics in Fig. 7.
                                                                        k − 1. We need to show that Theorem 1 still holds at step k,
Proposition 2. If a program P is constant-time up to k then             meaning that if P is constant-time up to step k, then for each
then for all j ≤ k, P is constant-time up to j.                         concrete steps ck−1 → − ck and c0k−1 − →   c0k such that t = t0 ,
                                                                                               t               t0
                                                                        we need to show that we can perform a step in the symbolic
Hypothesis 1. Symbolic execution does not get stuck unless
                                                                        execution sk−1      sk and that ck ∼
                                                                                                           ∼l sk ∧ ck ∼
                                                                                                           ∼ M          0 ∼M
                                                                                                                          ∼r sk holds.
secLeak evaluates to false. In particular, this implies that
P is defined on all locations computed during the symbolic                 We can proceed case by case on the concrete evaluation of
execution.                                                              ck−1 and c0k−1 .
                                                                           Case STORE: In the concrete execution, the instruction
  1) Proof of Relative Completeness of RelSE (Theorem 1):               @eidx := eval is evaluated and leaks the index eidx of the
Theorem 1 (Relative Completeness of RelSE). Let P be a                  store. By Proposition 1, concrete semantics of the STORE rule,
program constant-time up to k and s0 be a symbolic initial              and because t = t0 , we have:
configuration for P . For every concrete states c0 , ck , c00 , c0k ,               ck−1 eidx ` bvi and c0k−1 eidx ` bvi            (1)
and model M such that c0 ∼   ∼l s0 ∧ c0 ∼
                             ∼ M          0 ∼M
                                            ∼r s0 , if c0 →    −k
                                                                 t         First, we show that there exists a step from sk−1 ,
ck and c00 −→  k 0
                 ck with t = t0 then there exists a symbolic                  V


                                                                         l, ρ, µ, π in the symbolic execution. We have to consider
            t0
configuration sk and a model M 0 such that:                             the case where the symbolic evaluation of expressions is not
                             M0         0 ∼M 0
           s0 k sk ∧ ck ∼  ∼l sk ∧ ck ∼
                           ∼              ∼r sk                         stuck and the case where the evaluation of an expression gets
                        CST         ^                                   VAR             
                                                                                         ^
                                                                                                                     d0k−1 also evaluate the instruction @eidx := eval , and that
          Expr                  ρ, µ bv ` hbvi                                       ρ, µ v ` ρ v
                                                                                                                             dk−1 eidx ` M 0 (ι|l ) and d0k−1 eidx ` M 0 (ι|r )
                                                                                                                                                        V                              V




                                 
                             ρ, µ e ` φ
                                         ^




                                            ϕ , u φ
                                                         ^
                                                                     ^
                                                                                     ^



                                                                                                                     Therefore, we have d0 −−−−→k dk and d00 −−     0
                                                                                                                                                                      −−→0
                                                                                                                                                                           k 0
                                                                                                                                                                               dk with
                        UNOP                                                                                                                            t·[bvi ]               t ·[bvi ]
                                                                                                                     bv 6= bv0i , meaning that P is not constant-time at step k.
                                                    ^                   ^




                                   ρ, µ u e ` ϕ
                        ^           ^
                                                        ^
                                                                             ^
                                                                                         ^
                                                                                                 ^       ^
                                                                                                                     This contradicts the hypothesis that P is constant-time up to
                       ρ, µ e1 ` φ               ρ, µ e2 ` ψ                             ϕ , φ b ψ                                         V       V


          BINOP                                    ^                        ^
                                                                                                                     k, hence 2 π ∧ ι|l 6= ι|r and secLeak holds. Therefore, there
                                             ρ, µ e1 b e2 ` ϕ
                                                                                                                     exists a step sk−1     sk in the symbolic execution.
                                                                                                                                    V


                                                                                                                        Case ρ, µ eidx is stuck. From Hypothesis 1, secLeak
                                                                         ^
                                                        ^




                                    ρ, µ e ` φ
                                                                                                                     evaluates to false in the evaluation of the expression. With the
                                        ^                                ^                                       ^
               ^                ^                                ^




         ϕ , hselect(µ|l , φ|l ) | select(µ|r , φ|r )i                                       secLeak (φ)
    LOAD                                               ^                ^

                                                                                                                     same reasoning as in the previous case, this implies that P is
                                   ρ, µ @e ` ϕ
                                                                                                                     not constant-time at step k, which contradicts the hypothesis
                                                                  P.l = goto l0                                      of Theorem 1. Hence the symbolic evaluation of eidx cannot
                                     S _ JUMP
                                                                          l0 , ρ, µ, π
                                                                     ^                         ^




   Instr                                                    l, ρ, µ, π                                               be stuck.     V


                                                                                                                        Case ρ, µ eval is stuck is analogous.
                                                              π 0 , π ∧ (ϕ|l = ϕ|r )
                                                   ^            ^                               ^               ^




               P.l = goto e                 ρ, µ e ` ϕ
                      M  π0                  0                  ^                                   ^




                                            l , M (ϕ|l )       secLeak (ϕ)                                                                                                                 0
  D _ JUMP                                                                                                            Now, we need to show that there is a model M                            such that
                                                      l0 , ρ, µ, π 0                                                       0              0
                                                                    
                                                                                                                     ck ∼    sk ∧ c0k ∼
                                                 ^                           ^




                                        l, ρ, µ, π                                                                      ∼M            ∼M    sk holds.
                                                                                                                        ∼l            ∼ r
  ITE - TRUE                                                                                                            Recall that the program location in sk−1 evaluates to a store
                                 l0 , ltrue
                                                                                        ^               ^




  P.l = ite e ? ltrue : lf alse                     ρ, µ e ` ϕ
                                                                                                                                                                   V




      0                         ^        ^

                                           0                                                     ^
                                                                                                                     instruction @eidx := eval and let ι be the symbolic   index and
    π , π ∧ (true = ϕ|l = ϕ|r )       π         secLeak (ϕ)                                                         V                                                        V                    V


                                                                                                                     ν be the symbolic value, meaning that  ρ, µ eidx ` ι and
                                l0 , ρ, µ, π 0
                               ^                           ^




                   l, ρ, µ, π                                                                                            V              V                          V


                                                                                                                       ρ, µ eval ` ν . Let sk , lk , ρk , µk , π k .
  ITE - FALSE                                                                                                           First we need to show that the location in configurations ck ,
                                     l0 , lf alse
                                                                                        
                                                                                                                     c0k and sk are identical. Because concrete and symbolic STORE
                                                                                          ^              ^




  P.l = ite e ? ltrue : lf alse                                                     ρ, µ e ` ϕ
    π 0 , π ∧ (f alse = ϕ|l = ϕ|r )        π0
                                ^           ^                                                    ^




                                                                                 secLeak (ϕ)
                                                                                                                     rules increment the program location by 1 and because the
                                    l , ρ, µ, π 0
                                     0
                                
                                ^                            ^




                     l, ρ, µ, π                                                                                      program locations are identical in ck−1 , c0k−1 and sk−1 (from
               P.l = v := e
                                                   ^




                                           ρ, µ e ` ϕ      ϕ0 , canonical (ϕ)
                                                                 ^           ^                                   ^
                                                                                                                     induction hypothesis), the program locations are still identical
               ρ0 , ρ[v 7→ ϕ0 ]
                                ^




                                            π , π ∧ (ϕ0|l = ϕ|l ) ∧ (ϕ0|r = ϕ|r )
                                              0                      ^           ^               ^           ^


                                                                                                                     in ck , c0k and sk .
   ASSIGN                                   ^




                                    l, ρ, µ, π
                                               
                                                   l + 1, ρ0 , µ, π 0
                                                                                    ^


                                                                                                                        Second, we have to show that there exists M 0 such that
                                                                                                                     M 0  π k and that for all expression e, either the symbolic
   STORE                                                                                                                                                               V   V




             P.l = @e := e0         l0 = l + 1
                                                              
                                                          ρ, µ e ` ϕ
                                                                                     ^           ^
                                                                                                                     evaluation gets stuck on e, or ρk , µk e ` ϕ and
                                                                                                                                     M 0 (ϕ|l ) = bv ⇐⇒ ck e ` bv ∧
                   ^                                                 ^                                       ^
                                                                                                                                                V
       ^  0            0   ^                       ^        ^                            ^      ^




    ρ, µ e ` φ        µ , hstore(µ|l , ϕ|l , φ|l ) | store(µ|r , ϕ|r , φ|r )i
                                                     ^                                                       ^

                                                                                                                                                                                  (2)
    π 0 , π ∧ µ0|l = store(µ|l , ϕ|l , φ|l ) ∧ µ0|r = store(µ|r , ϕ|r , φ|r )                                                           M 0 (ϕ|r ) = bv ⇐⇒ c0k e ` bv
                   ^                ^       ^                    ^                           ^       ^
                                                                                                                                                    V



                                                             ^




                                 secLeak (ϕ)
                                                                                                                     We can build the new model M 0 as
                                           l0 , ρ, µ0 , π 0
                                    ^                              ^




                         l, ρ, µ, π
                                                                                                                         M 0 , M [µk 7→ hml | mr i]
                                                                                                                                    V




Figure 8: Symbolic evaluation of DBA instructions and ex-                                                                                                              V   V                   V

                                                    V                        V
                                                                                                                                                where ml , M (µ|l )[M (ι|l ) 7→ M (ν |l )]
pressions where canonical (ϕ) returns ϕ if it is in canonical                                                                                                          V   V                    V


form or a temporary variable otherwise; and u (resp. b ) is                                                                              and mr , M (µ|r )[M (ι|r ) 7→ M (ν |r )]
the logical counterpart of the concrete operator u (resp. b ).                                                       Intuitively, M 0 is equal to the old model M in which we add
                                                                                                                                                            V


                                                                                                                     the new symbolic memory µk , mapping to the concrete value
                                                                                                                                                        V                          V


                                                                                                                     of the old memory M (µ) where the index M (ι) maps to the
                                                                                                                     value M (ν ). Notice that M 0  π k .
                                                                                                                                V



stuck.
                                                                                                                        Case of the left projection (right case is analogous). We
    Case evaluation of expressions     is not stuck. Let ι be the
                                                     V                           V
                                                                                                                     can prove by induction on the structure of expressions that for
symbolic index such that ρ, µ eidx ` ι. To apply the rule
STORE , we must ensure that secLeak (ι) holds. If ι = hιi then
                                                                         V                       V
                                                                                                                     any expression, if sk does not get stuck then Eq. (2) holds for
secLeak is true, otherwise we must show 2 π ∧ ι|l 6= ι|r . We
                                                                                                 V           V
                                                                                                                     the model M 0 . Note that only the memory is updated from
show that by contradiction.                                                                                          step k − 1 to step k, meaning that ck , sk , and M 0 only differ
    Assume that there exists M 0 such that M 0  π∧ι|l 6= ι|r and
                                                                                                 V           V
                                                                                                                     from ck−1 , sk−1 and M on expressions involving the memory.
let M 0 (ι|l ) = bvi and M 0 (ι|r ) = bv0i . Notice that bvi 6= bv0i .
           V                                 V
                                                                                                                     Thus, we only need to consider the rule LOAD, as the proof
                                                                                                                     for other rules directly follows from the induction hypothesis
    Let d0 , d00 , dk−1 , d0k−1 be concrete configurations such
               M0                  M0                 M0
                                                                                                                     and the definition of M 0 .
that d0 ∼    ∼
             ∼0l      s0 , d00 ∼ ∼
                                 ∼r    s0 , dk−1 ∼  ∼
                                                    ∼l      sk−1 , and                                                  Assume an expression       @e such that sk does     not get
dk−1 ∼
  0      ∼
         ∼r
            M
                   s     .   From  Theorem   2,   there   are  concrete
                                                                                                                                                                   V                                    V


                    k−1
                                                                                                                     stuck and let ρk , µk e ` ι end ρk , µk @e ` ν 0 .
                                                                                                                                                         0
                                                                                                                                                   V                         V




executions d0 →      − k−1 dk−1 and d00 −     →  k−1
                                                      d 0
                                                        k−1 Because
                                                             .
                     t                        t0                                                                     We show that if Eq. (2) holds for the expression e,
         0                          0
dk ∼ ∼ M
     ∼ sk−1 and d
                           0    ∼
                                ∼ M
                                ∼ sk−1 , we know that dk−1 and                                                       then it holds for the expression @e. Formally, we must
      l                         k−1             r
                     V



show that if M 0 (ι0 |l ) = bvidx       ⇐⇒           ck e ` bvidx then        Let π 0 be the new path predicate in configuration sk . Note
                                                                           that because π is a sub-formula of π 0 , we also have M 0  π.
    V


   0 0
M (ν |l ) = bvval ⇐⇒ ck @e ` bvval .
                                                                                                                            M0
                                                                           Therefore, there exists ck−1 such that ck−1 ∼  ∼
                                                                                                                          ∼p sk−1 , and
                                 V



First, we can simplify M 0 (ν 0 |l ) as                                                M0
    V                            V
                                                                           because ∼ ∼
                                                                                     ∼p is a tight relation, ck−1 is unique. Additionally,
M 0 (ν 0 |l ) = M 0 (select(µk|l , ι0 |l )) by symbolic rule LOAD
                             V




                                                                           from the induction hypothesis for all concrete configuration c0
                                                                                            M0
                                                                           such that c0 ∼                     − k−1 ck−1 .
                                                     V



          = M (µ|l )[M (ι|l ) 7→ M (ν |l )][M 0 (ι0 |l )] by def. of M 0
                 V           V               V
                                                                                          ∼
                                                                                          ∼p s0 , we have c0 →
                                                                              Finally, because the symbolic execution is updated without
                                                                           over-approximation, we also have ck−1 →   − ck . Therefore, for
From this point, there are two cases:                                      each model M 0 and configuration c0 and ck such that c0 ∼  ∼ M0
                                                                                                                                      ∼p
                                                                                           0
   - The address of the load is the same as the address
                                             V                             s0 and ck ∼ ∼ M
                                                                                       ∼p sk , we have c0 → − k ck .
     of the previous store: M 0 (ι0 |l ) = M (ι|l ), therefore
                                                         V



          V



     M 0 (ν 0 |l ) = M (ν |l ).
                         V


                                                                             3) Proof of CT Security (Theorem 3):
     From the induction hypothesis, the concrete index of the
                                                                           Theorem 3 (Bounded-Verification for CT). Let s0 be a
                                 V                       V



     load evaluates to M 0 (ι0 |l ), i.e. ck e ` M 0 (ι0 |l ) which can
                                         V
                                                                           symbolic initial configuration for a program P . If the symbolic
     be rewritten as ck e ` M (ι|l ). From concrete rule STORE
                                                                           evaluation does not get stuck, then P is constant-time w.r.t.
     and ck−1 ∼    ∼  M
                   ∼l sk−1 , we know that the concrete memory                                                   k
                                                         V
                                                                           s0 . Formally, if for all k, s0         sk then for all initial
     from ck−1 to ck is updated at index M (ι|l ) to map to
                     V                                           V
                                                                           configurations c0 and c0 and model M such that c0 ∼
                                                                                                    0                               ∼ M
                                                                                                                                    ∼l s0 ,
     the value M (ν |l ), which leads to ck @e ` M (ν |l ) and, by               0 ∼ M
                                     V
                                                                           and c0 ∼∼r s0 ,
     rewriting, to ck @e ` M 0 (ν 0 |l ). Therefore we have shown
                                                                             c0 'L c00          − k ck ∧ c00 −
                                                                                           ∧ c0 →            →  k 0
                                                                                                                  ck =⇒ t = t0
               V



     that M 0 (ν 0 |l ) = bvval ⇐⇒ ck @e ` bvval                                                  t           0    t
   - The address of the load is different from the address
                                             V
                                                                           Additionally, if s0 is fully symbolic, then P is constant-time.
     of the previous store: M 0 (ι0 |l ) 6= M (ι|l ), therefore
                                                         V



          V                          V
                                                                           Proof. (Induction on k). Let s0 be an initial symbolic configu-
     M 0 (ν 0 |l ) = M (µ|l )[M 0 (ι0 |l )].
                         V



                                                                           ration for which the symbolic evaluation never gets stuck. Let
     From the induction hypothesis, the concrete index of
                                             V                       V     us consider a model M and concrete configurations c0 ∼     ∼ M
                                                                                                                                      ∼l s0 ,
     the load evaluates to M 0 (ι0 |l ), i.e. ck e ` M 0 (ι0 |l ).          0 ∼  M
                                                                           c0 ∼ ∼r s0 , for which the induction hypothesis holds at step
     From concrete rule STORE, we know that the concrete                   k, meaning that for all ck , (l, r, m) and ck0 , (l0 , r0 , m0 )
     memory from ck−1 to ck is only updated at address                     such that c0 →− k ck , c00 − →     ck , then t = t0 . We show that
                                                                                                            k 0
                                                                                          t              t0
                                                     V



     M (ι|l ) and untouched at address M 0 (ι0 |l ). Plus, we know
         V



                                                             V
                                                                           Theorem 3 still holds at step k + 1.
     from ck−1 ∼       ∼M     sk−1 that address M 0 (ι0 |l ) maps to
                                                                                                                           V      
                     V
                       ∼ l                                                    From Theorem 1, there exists sk , ls , ρ, µ, π such that:
                    0 0
                                                                                       s0 k sk ∧ ck ∼       ∼l sk ∧ ck ∼
                                                                                                              M           0 ∼M
         V


     M (µ|l )[M (ι |l )] in ck−1 . Therefore, in configuration
                         V                               V
                                                                                                            ∼               ∼r sk         (3)
     ck , index M 0 (ι0 |l ) maps to M (µ|l )[M 0 (ι0 |l )] which, by      Note that from Eq. (3) and Definition 2, we have ls = l = l0 ,
                                                 V




                                                 V



     rewriting, leads to ck @e ` M 0 (ν 0 |l ). Therefore we have          therefore the same instructions and expression are evaluated
                                                                           in configurations ck , c0k , and sk .
                         V



     shown that M 0 (ν 0 |l ) = bvval ⇐⇒ ck @e ` bvval .
                                                                              Because the symbolic execution does not get stuck, there
   Other cases: The reasoning is analogous. For the non-                   exists sk+1 such that sk          sk+1 . We show by contradiction
deterministic rules ITE - TRUE, ITE - FALSE, and D - JUMP, be-             that the leakages bv and bv0 produced by ck −→ ck+1 and
cause the leakages t and t0 determine the control flow of the                                                                    bv
program, there exist a unique symbolic rule that can be applied            c0k −−→
                                                                                 0
                                                                                   c0k+1 are necessarily equal.
                                                                              bv
to match the execution of both ck−1 and c0k−1 .                               Suppose that ck and c0k produce distinct leakages. This can
                                                                           happen during the evaluation of a rule LOAD, D _ JUMP, ITE,
  2) Proof of Correctness of RelSE (Theorem 2):                            STORE .
                                                                              Case LOAD: The evaluation of the expression @e in configu-
Theorem 2 (Correctness of RelSE). For every symbolic con-
                                                                           rations ck and c0k produces leakages bv and bv0 and, assuming
figurations s0 , sk such that s0 k sk and for every concrete
                                                                           the load is insecure, we have bv 6= bv0 .
configurations c0 , ck and model M , such that c0 ∼
                                                  ∼ M
                                                  ∼p s0 and                        V


                                                                              Let ϕ be the evaluation    of the leakage in the symbolic
ck ∼∼ M
                                                 − k ck .
    ∼p sk , there exists a concrete execution c0 →                                            V       V


                                                                           configuration: ρ, µ, e ` ϕ. From Eq. (3), Definition 2 and
Proof. (Induction on k). Case k = 0 is trivial.                            because symbolic execution does not get stuck, there exists M
                                                                           s.t. M  π, bv = M (ϕ|l ) and bv0 = M (ϕ|r ).
                                                                    V                            V                    V


   Let us consider a symbolic configuration sk−1 , l, ρ, µ, π
                                                                              Because we assumed bv 6= bv0 , then M (ϕ|l ) 6= M (ϕ|r ).
                                                                                                                           V           V


for which the induction hypothesis holds. Formally, for each
model M and configurations c0 , ck−1 such that c0 ∼∼ M
                                                                                                         V     V



                                                   ∼p s0 and               Therefore, we have M  π∧ϕ|l 6= ϕ|r , meaning that secLeak
ck−1 ∼∼ M
      ∼p sk−1 , we have c0 → − k−1 ck−1 . We need to show for              evaluates to false and the symbolic execution is stuck. How-
each symbolic step sk−1       sk , that for each model M 0 and             ever, because sk is non-blocking we have a contradiction.
                                          M0            M0
configurations c0 and ck such that c0 ∼ ∼p s0 and ck ∼
                                        ∼             ∼
                                                      ∼p sk ,              Therefore bv = bv0 .
we have c0 →− k ck .                                                          Cases D _ JUMP, ITE, STORE: The reasoning is analogous.
We have shown that the hypothesis holds for k + 1. If                       A call to a function high_input_n(addr), where n is
        k+1
s0          sk+1 , then for all model M and low-equivalent               a constant value, specifies that the memory must be initialized
initial configurations c0 ∼  ∼l s0 and c0 ∼
                             ∼ M            0 ∼M
                                               ∼r s0 such that           with n secret bytes, starting at address addr.
       k                     0     k 0        0              0
c0 →− ck −→ ck+1 and c0 −       →    ck −
                                        −→   ck+1 where t = t ,          Example 3 (Stub for specifying high locations). A user can
     t       bv                 t0      bv0
then t · [bv] = t0 · [bv0 ].                                             write a wrapper around a function foo to mark its arguments
                                                                         as low or high as shown in Listing 3. The function foo can be
  4) Proof of Bug-Finding for CT (Theorem 4):
                                                                         defined in an external library which must be statically linked
Theorem 4 (Bug-Finding for CT). Let s0 be an initial sym-                with the wrapper program.
bolic configuration for a program P . If the symbolic evaluation
gets stuck in a configuration sk then P is not constant-time.                uint8_t secret[4]; uint8_t public[4];
                                                                             high_input_4(secret); //4 bytes high input
Formally, if there exists k st. s0 k sk and sk is stuck, then                low_input_4(public); //4 bytes low input
there exists a model M and concrete configurations c0 ∼ ∼ M
                                                        ∼l s0 ,              return foo(secret, public);
c00 ∼
    ∼r s0 , ck ∼
    ∼ M
                ∼l sk and ck ∼
                ∼ M           0 ∼ M
                                 ∼r sk such that,                              Listing 3: Wrapper around external function foo
  c0 'L c00 ∧ c0 →
                 − k ck ∧ c00 −
                              →0
                                 k
                                   c0k ∧ t 6= t0
                           t                  t
                                                                         During  the  symbolic      execution, the     function
Proof. Let us consider symbolic configurations s0 and sk such
                                                                         high_input_4(secret) is encountered, it is stubbed as:
that s0 k sk and sk is stuck. This can happen during the
evaluation of a rule LOAD, D _ JUMP, ITE, STORE.                         @[secret+0] := hβ0 | β00 i  @[secret+1] := hβ1 | β10 i
   Case LOAD: where an expression @e in the configuration               @[secret+2] := hβ2 | β20 i         @[secret+3] := hβ3 | β30 i
                                                           
                                                                                     0
             V                            V               V        V


sk , ls , ρ, µ, π produces a leakage ϕ st. ρ, µ, e ` ϕ.
                                              V
                                                                         where βi , βi are fresh 8-bit bitvector variables.
   This evaluation blocks iff ¬secLeak (ϕ), meaning that there
exists a model M such that
                                    V     V
                                                                         D. Zoom on the Lucky13 Attack
                      M  π ∧ (ϕ|l 6= ϕ|r )                        (4)
   Let us consider the concrete configurations c0 , c00 ,                   Lucky 13 [50] is a famous attack exploiting timing vari-
ck , (l, r, m), and ck0 , (l0 , r0 , m0 ) such that:                     ations in TLS CBC-mode decryption to build a Vaudenay’s
        c0 ∼
           ∼l s0 , c0 ∼
           ∼ M
                      ∼r s0 , ck ∼
                    0 ∼M
                                     ∼l sk and ck ∼
                                     ∼ M           0 ∼M
                                                         ∼r sk           padding oracle attack and enable plaintext recovery [7], [50].
It follows by Theorem 2, that c0 →       k
                                      − ck and c0 →  0
                                                         − k c0k .       We do not actually mount an attack but show how to find
                                       ∼                                 violations of constant-time that could potentially be exploited
                                       ∼l s0 and c0 ∼
                                          M              0   M
   From Definition 2, because c0 ∼                         ∼
                                                           ∼r s0 we
               0
have c0 'L c0 and because ck ∼        ∼ M              0   ∼ M           to mount such attack.
                                      ∼l sk and ck ∼       ∼r sk , we
have ls = l = l0 .                                                          We focus on the function tls-cbc-remove-padding
   Therefore the evaluation of ck and c0k also contains the              which checks and removes the padding of the decrypted
expression @e, producing leakages bv and bv0 st. ck @e ` bv              record. We extract the vulnerable version from OpenSSL-
and c0k @e ` bv0 .                                                       1.0.16 and its patch from [16]. Finally, we check that no
   From Definition 2 we have bv = M (ϕ|l ) and bv0 =
                                                      V
                                                                         information is leaked during the padding check by specifying
M (ϕ|r ), and from Eq. (4), we can deduce bv 6= bv0 .
   V
                                                                         the record data as private.
                                                                            On the insecure version, B INSEC /R EL accurately reports
Therefore, we have a model M and concrete configurations
                                                                         5 violations, and for each violation, returns the address of
c0 ∼
   ∼l s0 , c0 ∼
   ∼ M
              ∼r s0 , ck ∼
            0 ∼M
                         ∼l sk and ck ∼
                         ∼ M        0 ∼M
                                      ∼r sk such that,                   the faulty instruction, the execution trace which can be vi-
                 − k ck −→ ck+1 ∧ c00 →
  c0 'L c00 ∧ c0 →                    − k c0k −−→
                                                0
                                                  c0k+1                  sualized with IDA, and an input triggering the violation.
                       t       bv                 t           bv
                                                                         For instance, on the portion of code in Listing 4, three
                                     ∧ t · [bv] 6= t0 · [bv0 ]
                                                                         violation are reported: two conditional statement depending
which shows that the program is insecure.                                on the padding length at lines 3 and 4, and a memory
  Cases D _ JUMP, ITE, STORE: The reasoning is analogous.                access depending on the padding length at line 4. For the
                                                                         conditional at line 3, when the length LEN of the record data
                                                                         is set to 63, B INSEC /R EL returns in 0.11s the counterexam-
C. Usability: Stubs for Input Specification
                                                                         ple “data_l[62]=0; data_r[62]=16”, meaning that
   We enable the specification of high and low variables in              an execution with a padding length set to 0 will take a different
C source code using dummy functions that are stubbed in                  path that an execution with a padding length set to 16.
the symbolic execution (cf. Example 3). Note that this is at
the cost of portability (it can only be used around C static             1   pad_len = rec->data[LEN-1]; // Get padding length
libraries or when in possession of the C source code). If                2   [...]
                                                                         3   for (i = LEN - pad_len; i < LEN; i++)
portability is required, the user can still refer to the binary-         4     if (rec->data[i] != pad_len)
level specification method (Section V) which relies on manual            5       return -1; // Incorrect padding
reverse-engineering to find the offsets of secrets relatively to
                                                                                  Listing 4: Padding check in OpenSSL-1.0.1
the initial esp.
  On the secure version, when the length LEN of the record
data is set to 63, B INSEC /R EL explores all the paths in 400s
and reports no vulnerability.
