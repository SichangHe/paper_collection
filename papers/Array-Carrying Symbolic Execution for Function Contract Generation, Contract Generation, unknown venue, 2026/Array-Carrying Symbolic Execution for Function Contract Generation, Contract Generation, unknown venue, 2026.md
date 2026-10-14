                                         Array-Carrying Symbolic Execution for Function
                                                      Contract Generation

                                          Weijie Lu∗1 , Jingyu Ke∗1 , Hongfei Fu1 , Zhouyue Sun1 , Yi Zhou1 , Guoqiang
                                                                       Li1 , and Haokun Li2
                                                         1
                                                             Shanghai Jiao Tong University, Shanghai, China
                                                                 2
                                                                   Peking University, Beijing, China
arXiv:2602.23216v2 [cs.PL] 27 Feb 2026




                                               Abstract. Function contract generation is a classical problem in pro-
                                               gram analysis that targets the automated analysis of functions in a pro-
                                               gram with multiple procedures. The problem is fundamental in inter-
                                               procedural analysis where properties of functions are first obtained via
                                               the generation of function contracts and then the generated contracts are
                                               used as building blocks to analyze the whole program. Typical objectives
                                               in function contract generation include pre-/post-conditions and assigns
                                               information (that specifies the modification information over program
                                               variables and memory segments during function execution). In programs
                                               with array manipulations, a crucial point in function contract generation
                                               is the treatment of array segments that imposes challenges in inferring
                                               invariants and assigns information over such segments. To address this
                                               challenge, we propose a novel symbolic execution framework that carries
                                               invariants and assigns information over contiguous segments of arrays.
                                               We implement our framework as a prototype within LLVM, and further
                                               integrate our prototype with the ANSI/ISO C Specification Language
                                               (ACSL) assertion format and the Frama-C software verification plat-
                                               form. Experimental evaluation over a variety of benchmarks from the
                                               literature and functions from realistic libraries shows that our framework
                                               is capable of handling array manipulating functions that indeed involve
                                               the carry of array information and are beyond existing approaches.

                                         1 Introduction
                                         In program analysis, functional contract generation aims at the automated gen-
                                         eration of contracts that specify the input-output relationship of an individ-
                                         ual function. The input-output relationship typically involves preconditions and
                                         postconditions, and may also include assigns information (from the ANSI/ISO
                                         C Specification Language (ACSL) assertion format) that specifies possible mod-
                                         ifications over memory segments. The problem is fundamental in program anal-
                                         ysis, as it facilitates interprocedural analysis by providing the basic information
                                         of functions. In this work, we focus on function contract generation for array-
                                         manipulating programs.
                                             In the literature, various approaches have been proposed to address the auto-
                                         mated generation of function contracts, including abstract interpretation [7, 13–
                                         15,22,38,45], model checking/SMT solving [12,21,32], instrumentation [3], large
                                           * These authors contributed equally to this work.
2         Weijie Lu et al.

language models (LLMs) [43, 59], etc. Abstract interpretation chooses a suit-
able abstract domain for the abstraction of program states, and then performs a
top-down analysis for each function. Existing abstract interpretation approaches
accommodate contiguous array memory segments and support the inference of
array invariants [15, 22, 38]. Model checking/SMT solving approaches [12, 21]
encode program execution as rules and leverage SMT solvers to verify whether
an assertion in the function holds or not. The treatment of contiguous mem-
ory segments can be readily encoded by SMT constraints. Instrumentation [3]
allows a user to specify rules to transform programs into a form with ghost vari-
ables that is easier to analyze, where specific array patterns (e.g., summation,
maximum) are handled by special instrumentation rules. LLM-based approaches
(e.g. [43, 59]) perform supervised fine-tuning (SFT) using manually annotated
programs as training data. The resulting fine-tuned model then infers function
contracts using suitable prompts, often with possible guidance from static anal-
ysis and external experts.
    While existing approaches tackle function contracts with array manipulations
from different perspectives, they are limited in various aspects. For example,
abstract interpretation has developed relational and segment-oriented domains
that can reason about many array invariants [7, 13, 15, 22, 38]. However, for fully
automated contract synthesis, preserving path-sensitive disjunctive loop-exit in-
formation and translating it into precise merged array-segment assigns infor-
mation remains challenging. Model checking/SMT solving approaches can also
infer summaries/contracts in multiple settings [2,12,19,21,32]. Nevertheless, de-
pending on the encoding and property setup, many workflows are geared toward
proving specific assertions, and may require additional summarization layers to
produce reusable function-level contracts of the form hPre, Post, Assigni. Instru-
mentation focuses on manual specification of ghost variables, and hence does not
have a dedicated treatment of contiguous array segments. LLM approaches usu-
ally require manual guidance from experts to avoid producing incorrect results
caused by hallucinations. As a result, it remains a challenge to build a framework
that handles array segments and invariants in function contract generation.
    To address the aforementioned challenge, we propose a novel symbolic exe-
cution framework that carries array invariants and has a dedicated treatment
of the contiguous array segments. Compared with previous results and existing
symbolic execution techniques, our symbolic execution framework carries invari-
ants generated from external invariant generators along the program statements,
and carefully handles disjunction, splitting and merging of contiguous array seg-
ments. In our implementation, the invariant-generation back-end combines an
aﬀine/linear generator (the StInGX-style plugin based on Farkas-lemma rea-
soning [28, 41]) with idiom-oriented generators for search and max/min loops.
Appendix C.1 gives concrete examples of these generators and the ACSL clauses
they produce. The detailed contributions are as follows.

    – Our symbolic execution is designed to receive numerical and array invariants
      from external invariant generators and propagate them along the execution of
      program statements. This allows our framework to leverage loop invariants to
      Array-Carrying Symbolic Execution for Function Contract Generation         3

   generate function contracts for general properties. Moreover, the propagation
   of invariants also produces tight preconditions for subsequent loop analysis.
 – Our symbolic execution has a refined treatment of contiguous array seg-
   ments. In detail, our framework handles disjunction of array segments re-
   sulting from different program execution paths (including different loop exit
   modes), and the merge/split of array segments during the symbolic execu-
   tion. The merge and split of array segments allow precise tracking of infor-
   mation over these segments that is crucial to derive overall contracts related
   to array segments.
 – We implement our symbolic execution technique as a prototype that com-
   prises about 19000 lines in C++ within the LLVM platform [36, 56].
   We also integrate our prototype with the ACSL assertion format and the
   Frama-C software verification platform [9, 17], so that the result of our sym-
   bolic execution can be fully verified by external verifiers.

Experimental evaluation over a wide range of benchmarks (including realistic
benchmarks from active libraries) shows that our framework is capable of gener-
ating contracts that describe precise behavior of array-manipulating functions,
while previous approaches fail to handle many of these benchmarks.
Limitations. Our symbolic execution has limited ability to handle pointers. Cur-
rently, we can only handle simple pointer arithmetic with base and offset arising
from array addresses, and cannot handle recursive pointer structures such as
linked lists and binary trees.

1.1 Related Works
Below we describe related works on function contract generation.
Abstract interpretation. Abstract interpretation [13, 16] generates function con-
tracts by a top-down analysis that propagates elements from an abstract domain
along the execution of the program, where functions are inlined upon procedure
calls. Existing abstract interpretation methods handle arrays by abstract do-
mains that express invariants over contiguous memory segments of arrays [15,38].
As we consider to extend symbolic execution with array segments and invariants,
our result has a different focus from abstract interpretation methods.
Model checking. Model checking approaches [12, 21] often encode read/write op-
erations of arrays by SMT rules and then solve target assertions with arrays.
The most relevant works are by Tricera [2] and a SeaHorn-based verifier [20]
that generate function contracts through a transformation into CHC solving
(via e.g. the state-of-the-art CHC solver Eldarica [24]). A major disadvantage
of existing model checking approaches is that they often follow top-down anal-
ysis, so the generated specification is often highly specific to the initial values
of a program. Our approach circumvents this limitation by leveraging external
invariant generators in our symbolic execution.
Large language models. In recent years, there has been a burgeoning focus on
applying Large Language Models (LLMs) to support code specification gen-
eration [34, 37, 43, 60]. A standard framework is AutoSpec [59] that leverages
4       Weijie Lu et al.

LLMs to synthesize ACSL-language specifications for C programs via a static
analysis-guided bottom-up iterative approach, offering wider applicability than
traditional works. Additionally, further studies [30,40,42,47,48] mainly focus on
LLM-based invariant generation.
Symbolic execution. Existing symbolic execution techniques analyze program
with memory operations by symbolically encoding program states and main-
taining a symbolic memory model that tracks heap and array updates across
execution paths. For example, Clang Static Analyzer [33] performs a path-
sensitive symbolic execution with a region-based memory model, but its reason-
ing over arrays and heap is local and non-relational. It propagates per-element
constraints along each path, detecting out-of-bounds or null dereferences, yet
lacks the ability to summarize iteration effects or infer relational properties over
contiguous array regions across loop executions. KLEE [8] symbolically exe-
cutes LLVM bitcode with SMT-based constraint solving, representing memory
as byte-addressable symbolic objects and focusing on path exploration rather
than invariant inference. While several extensions [27, 49] enhance its handling
of heap-allocated objects and symbolic pointers, KLEE and its variants still
analyze memory at the level of individual allocations and lack the capability
to infer relational or inductive invariants over contiguous array regions. The
Gillian platform [44, 55] provides a language-parametric symbolic execution ar-
chitecture, and further integrates separation-logic-based verification with com-
positional memory models for JavaScript and C. Compared with Gillian, our
work focuses on automatic contract synthesis for array-manipulating functions
in C, where quantified array invariants are carried and merged along symbolic
execution to synthesize ACSL requires/ensures/assigns clauses. Compared
with existing results, our approach extends symbolic execution with contiguous
memory segments of arrays.
Invariant generation. Invariant generation can be addressed by abstract interpre-
tation [7, 13, 15, 22, 38], constraint solving [10, 11, 28, 35, 41], instrumentation [3],
recurrence analysis [29, 58], etc. Low-level Bi-Abduction [25] is particularly rel-
evant for compositional analysis of low-level pointer-intensive fragments, infer-
ring function contracts through separation-logic bi-abduction with support for
operations such as pointer arithmetic and block splitting/merging. In contrast,
our target is contiguous array reasoning with carried quantified invariants and
disjunctive segment summaries, which is tailored to postcondition and assigns
synthesis in ACSL rather than low-level heap-shape reasoning over intrusive
linked structures. Moreover, by integrating a Linear/Aﬀine invariant generator
plugin (in the style of StInGX/Farkas-lemma-based inference [28, 41]) into our
loop-analysis pipeline, our framework can effectively handle a broad class of
numerical loops as well, including loops whose key properties are captured by
aﬀine index/value relations. Our approach utilizes these methods to generate
numerical and array invariants to be carried during our symbolic execution.
         Array-Carrying Symbolic Execution for Function Contract Generation                                             5

2 Overview

Below we have an overview of our results via two illustrative examples.


   /*@ requires size >= 1; */                      uint BinAdd(uint *r, const uint *a, const uint *b, uint n)
   uint SearchZero(const uint *data, int size)     {
   {                                                   uint carry = 0; uint nn = n;
      uint i = 0;                                      const uint *aa = a; const uint *bb = b;
      while (i < size) {                               uint *rr = r;
          if (data[i] == 0) break;
          i++;                                         while (nn >= 4) { /* Process 4 groups in batches. */
      }                                                    ADD_ABC(carry, rr[0], aa[0], bb[0], carry); /* offset 0 */
                                                           ADD_ABC(carry, rr[1], aa[1], bb[1], carry); /* offset 1 */
       if (i == size) return 0;                            ADD_ABC(carry, rr[2], aa[2], bb[2], carry); /* offset 2 */
       else return 1;                                      ADD_ABC(carry, rr[3], aa[3], bb[3], carry); /* offset 3 */
   }                                                       rr += 4; /* a group of 4 */    aa += 4; /* a group of 4 */
                                                           bb += 4; /* a group of 4 */    nn -= 4; /* a group of 4 */
             (a) SearchZero function                   }

                                                       uint i = 0;
   #define ADD_ABC(carry, r, a, b, c)
                                                       for (; i < nn; i++) {
      do {
                                                           ADD_ABC(carry, rr[i], aa[i], bb[i], carry);
           uint macroTmpS = (b) + (c);
                                                       }
           carry = (macroTmpS < (c)) ? 1 : 0;
           (r) = macroTmpS + (a);
                                                       return carry;
           carry += ((r) < macroTmpS) ? 1 : 0;
                                                   }
      } while (0)

                (b) ADD_ABC macro                                        (c) BinAdd example




                                       Fig. 1. Array program examples



First example. Consider the array manipulating function shown in Figure 1(a),
which is a function that searches whether there is a zero entry in the array data.
The precondition of the function is size ≥ 1 which specifies that the size of the
array should be positive. A notable feature of this function is that after the
while loop, the function continues to check whether i equals size. If so, then the
function returns 0, meaning that no zero entry is found. Otherwise, the function
returns 1, meaning that a zero entry has been found.
    To generate a complete contract for this function, our symbolic execution
maintains both array invariants and contiguous array segments. For this exam-
ple, our symbolic execution first calls an external invariant generator to generate
loop invariant and summary for the while loop. By distinguishing different exit
ways of the loop, our symbolic execution receives a disjunctive loop summary
of two branching execution paths: one corresponds to the case when the loop
exits upon encountering the conditional branch data[i] != 0, denoted as π0 ,
and the other corresponds to the case when the condition data[i] == 0 con-
sistently holds, denoted as π1 . Based on these execution paths, we extract the
loop summary with information over the contiguous array segment with index
from 0 to i as follows. Specifically, along the path π0 , our symbolic execution
receives the assertion at the loop exit: (∀j. 0 ≤ j < i → data[j] = 0) ∧ data[i] 6=
0 ∧ i < size. On the other hand, along the path π1 , our symbolic execution
receives (∀j. 0 ≤ j < i → data[j] = 0) ∧ i = size. Note that the assertions of the
two paths cannot be merged as they differ at whether data[i] == 0 and i ==
size. Our symbolic execution maintains the disjunction of these two assertions,
6       Weijie Lu et al.

and carries it forward to the remaining part of the program so that the function
contract below
 Pre : size ≥ 1    Assigns : ∅
       [                                                       ]
Post : (i = size) ∧ (∀j. 0 ≤ j < size → data[j] = 0) ∧ res = 0
           [                                                                   ]
        ∨ (i < size) ∧ (data[i] 6= 0) ∧ (∀j. 0 ≤ j < i → data[j] = 0) ∧ res = 1 .

is inferred, capturing precisely the behavior of the function. The main contribu-
tion of our symbolic execution here is the carry of (disjunctive) invariants and
contiguous array segments.
Second example. Consider the BnADD function extracted from the openHiTLS
library [46], as shown in Figure 1(c) (with macro given in Figure 1(b)). To
capture the overall memory modification in the execution of the function, one
needs to merge the range of modified array segments in the two loops. Our
symbolic execution detects changed array segments in each loop of the function,
and merge the two segments into a single segment. In this example, the modified
array range of the first loop is detected as rr[0..4k), corresponding to the batched
updates of four elements per iteration, where k is a ghost variable implicitly
defined within the loop to represent the number of iterations executed so far.
Informally, the term rr[0..4k) means that the content from index 0 to index
4k of the array rr may be modified after k loop iterations. The counterpart of
the second loop is detected as rr[4k..n), which handles the remaining elements
after the batch processing. By merging the two modified ranges, our symbolic
execution generates the overall modified range rr[0..n). The major contribution
here is the merging of modified memory segments in our symbolic execution that
allows us to generate the complete assigns information in the function contract.


3 Array-Carrying Symbolic Execution
In this section, we illustrate our symbolic execution framework over functions
with integer and array variables that carries invariants and contiguous array seg-
ments, and aims at automatically synthesizing a function contract for a function
in a given C program.
    Due to the space constraints, we present the key concepts of invariants and
function contracts in our symbolic execution informally, and relegate the detailed
definitions (over a simplified program model in Appendix A) to Appendix B.
An invariant is a collection of formulas at certain program counters required
to hold in every program state along every feasible execution path, thereby
over-approximating the set of reachable program states. A function contract
characterizes the intended behavior of a function by a precondition restricting
admissible input program states, a postcondition describing the property that
must hold upon termination, and an assigns information indicating possible
memory locations whose content may be modified during function execution.
Overview. Figure 2 demonstrates the workflow of our symbolic execution frame-
work. The framework first takes as input an abstract syntax tree of the function
          Array-Carrying Symbolic Execution for Function Contract Generation                                          7

                           Symbolic Statement Executor                                Output C Program
                                                                                     with ACSL Annotation
                                 Potential Execution Paths
  Abstract Syntax Tree
                                                       …                       /*@
                                      𝑃1         𝑃2            𝑃𝑛                   assigns \nothing;
                                                                                    ensures \result == \Old(x)
                                                                               */
                                    Carry Contiguous Array Segs                int test(int x) {
  int test(int x) {
      int a = x;                    ar[n]                                         …
      int y = 0;                                                                  /*@
                                                                                      loop assigns y, a;
        while (a != 0) {                                                              loop invariant y + a - x == 0
                                                             Path Conditions          …
            y = y + 1;
            a = a - 1;     Invariant Generator                                    */
                                                                                  while(a != 0) {
        }                                                      Invariants
        return y;                                                                       …
  }                                                                               }
                                                             Loop Summaries       return y;
                                                                               }

      Input C Program




                Fig. 2. General workflow of array-carrying symbolic execution


body of the function to be analyzed. Then, a symbolic statement executor simu-
lates the execution of the function body, producing multiple potential execution
paths. During the simulation, the statement executor calls external invariant
generators to generate invariants and summaries for loops. Moreover, the execu-
tor carefully maintains contiguous array segments of array contents and invari-
ants, and carries them forward in the remaining execution. Finally, the execution
paths with their path conditions, together with the carried invariants and con-
tiguous array contents, are combined to obtain the function contract of the whole
function. To maintain array segments and invariants, our symbolic statement ex-
ecutor incorporates an extended memory model to support constraint inference
involving arrays and pointers.
    Below we first present the high-level workflow of our framework, then the
technical details on handling invariants and contiguous array segments, and fi-
nally a prototype implementation for our framework in LLVM.

3.1 Symbolic Execution Framework
In this section, we introduce our symbolic execution framework. We focus on the
read and write aspects of arrays, and omit other technical aspects such as records
and pointer arithmetic. A high-level program model is relegated to Appendix A
for space constraints.
    As our symbolic execution handles array operations, we model array access
and modification operations by direct read and write operations at memory ad-
dresses of array variables. In our framework, we consider arithmetic expressions γ
with memory read operations by γ ::= c | x | a | γ1 ⊕ γ2 | R(a). In the syntax, we
have integer variables x, integer constants c, address variables a and arithmetic
operations ⊕ including addition, subtraction and multiplication (we omit divi-
sion to avoid floating point errors and division by zero for simplicity). Moreover,
8       Weijie Lu et al.

the expression R(a) represents the result of the read operation at the address
variable a. Integer variables and constants are extracted from the underlying
program, while address variables are fresh variables referring to pointers.
    Let Addr be a countable set of address constants and V be a countable
set of symbolic values (for undetermined values). We denote the counterpart of
arithmetic expressions γ where the role of program variables switches to symbolic
values as symbolic expressions, denoted by β with possible subscripts.
    A symbolic address is an ordered pair (β1 , β2 ) of symbolic expressions in the
syntax above for which β1 is the base expression and β2 is the offset expression,
which implicitly corresponds to the sum of the base and the offset (multiplied
with the size of array entry). However, for the sake of clearly representing pointer
arithmetic and intra-array offsets, we shall consistently use the pair notation
(β1 , β2 ) throughout the remainder of the paper to denote all address values. In
our symbolic execution, we consider an intermediate program syntax as follows:

 S ::= x := γ | a := &x | W (a, γ) | if b then S1 else S2 | while b do S | S1 ; S2 .

In the grammar, we have assignment statements for integer variables x := γ,
conditional branches if b then S1 else S2 , while loops while b do S, in which b
represents the boolean expressions built from comparison of symbolic expres-
sions and propositional logic connectives. In addition, we have a statement form
a := &x that assigns the symbolic address of x to an address variable a, corre-
sponding to the address-of operation, and a statement form W (a, γ) that writes
the expression γ to the symbolic address of the address variable a.
    Our symbolic execution works with symbolic states. Formally, a symbolic
state Σ is an ordered pair (M, A) where M is a memory map that maps ev-
ery symbolic address encountered so far to the symbolic expression held at the
symbolic address, and A is an address map that maps each address and integer
variable to its corresponding symbolic address where its concrete value lies. A
symbolic state records the current symbolic addresses of the integer and array
variables, and the current symbolic expressions at the symbolic addresses.
    In our framework, read and write operations on addresses are realized by
updating the corresponding maps in the current symbolic state. For example, the
read expression R(a) for a symbolic state (M, A) denotes the symbolic address
M (A(a)) held in the address variable a.
    The workflow of our symbolic execution is a traversal of program statements
in the adapted program syntax S. During the traversal, we maintain a symbolic
configuration Conf. Formally, a symbolic configuration Conf is a finite set of sym-
bolic paths, where each symbolic path P ∈ Conf is a tuple (ℓ, Σ, Seg, pathCond)
that specifies the current status after the execution of the path: ℓ is the cur-
rent program counter, Σ is the current symbolic state, Seg is a structure that
records the current information for contiguous array segments, and pathCond
is a collection of path conditions resulting from the execution of the symbolic
path. Invariants are treated as path conditions in pathCond.
    Algorithm 1 presents the pseudocode of our queue-based symbolic execution
procedure. The main workflow is an enumeration of all feasible execution paths
      Array-Carrying Symbolic Execution for Function Contract Generation         9

under a program in the syntax of S. In this pseudocode, we require an input
PreCond that corresponds to the input ACSL precondition (i.e., the requires
clause of the target function). Here we focus on the update of ℓ, Σ and conditions
in pathCond along the symbolic execution, and relegate the details for the update
of Seg and invariants in pathCond to the next subsection.
    The procedure begins by initializing the initial symbolic state Σ0 = (M0 , A0 )
at the entry of a program, as shown in Algorithm 1, starting from line 1. The
initialization works as follows.

 – In the initial address map A0 , each program variable x ∈ X is mapped to
   a symbolic address addr(x) drawn from the set Addr. As defined earlier,
   every addr(x) takes the form (β1 , β2 ). The base address β1 is a fresh address
   constant; for integer variables and pointers, the offset address β2 is set to
   0, whereas for an array element arr[i], the offset is the symbolic expression
   M0 (A0 (i)).
 – For each symbolic address addr(x) associated with a variable x in A0 , we
   insert into M0 a mapping from addr(x) to an initial symbolic expression
   βx . The expression βx corresponds to the initial value assigned to x in the
   program. If such a value does not exist or cannot be statically determined,
   we instead assign a fresh symbolic value taken from V as the βx . We also
   substitute program variables x in the given precondition by βx .

    Throughout this initialization procedure, all symbolic addresses addr(x) and
symbolic values used for different variables are guaranteed to be distinct.
    After the initialization, as shown in Algorithm 1 starting from line 6, the
symbolic executor traverses the statements in the function. Suppose that S is
the current statement in the traversal. To symbolically execute S, the algorithm
dequeues existing symbolic paths from the path queue, and for each path P ,
invokes the Exec procedure. The Exec procedure serves as the symbolic transfer
function: it interprets the semantics of S to compute the successor symbolic
state and update the path conditions. Depending on the specific type of the
statement S, the symbolic path P = (Σ = (M, A), pathCond) is updated by
Exec as follows. (Here we omit the components ℓ, Seg in the path description as
(i) the update of ℓ corresponds to the natural control flow successor of S and
(ii) the update of Seg will be detailed in the next subsection.) Below, given a
memory map M , we denote by M [(β1 , β2 ) 7→ β] the memory map that maps the
symbolic address (β1 , β2 ) to the symbolic expression β, while maintaining the
existing mappings for all other symbolic addresses.

 – If S is a conditional statement with condition b, as shown in Algorithm 1
   starting from line 10, then the symbolic executor splits the symbolic path
   P into two new symbolic paths Pb , P¬b . The symbolic path Pb equals (Σ,
   pathCond ∪ {[b]Σ }), for which the condition [b]Σ is obtained by replacing
   every integer program variable x and read operation R(a) in b by their
   corresponding symbolic expressions M (A(x)) and M (A(a)), respectively.
   The case for P¬b is similar.
10       Weijie Lu et al.


 Algorithm 1: Symbolic Execution and Contract Synthesis Workflow
     Input: F unc as target function context, P reCond as the set of preconditions
     Output: Conf, Iall , Cfunc as symbolic configuration, loop invariants and
              synthesized function contracts
 1 Extract variable set X from F unc;
 2 foreach x ∈ X do
 3    A0 (x) ← addr(x); Init(M0 (addr(x));
 4   Σ0 = (M0 , A0 ); pathCond0 ← ∅;
 5   P0 = (Σ0 , pathCond0 ); Path.enqueue(P0 ); Iall ← ∅;
 6 foreach S ∈ F unc in program order do
 7    Path′ ← ϕ;
 8    while P ath is not empty do
 9        Dequeue P = (Σ, pathCond) from P ath;
10        if S is ifstmt then
11            P1 ← (Σ, pathCond ∧ [b]Σ );
12            (Σ′1 , pathCond′1 ) ← Exec(S1 , P1 );
13            P ath′ .enqueue (Σ′1 , pathCond′1 );
14            P2 ← (Σ, pathCond ∧ [¬b]Σ );
15            (Σ′2 , pathCond′2 ) ← Exec(S2 , P2 );
16            P ath′ .enqueue (Σ′2 , pathCond′2 );
17        else if S is whilestmt then
18            (Mloop , P Cloop , Inv) ← LoopAnalyzer(S, P );
19            Iall ← Iall ∪ Inv;
20            (Σ′ , pathCond′ ) = Update((Mloop , P Cloop , Inv), P );
21            P ath′ .enqueue(Σ′ , pathCond′ );
22        else
              // Handle assignment statements
23            (Σ′ , pathCond′ ) ← Exec(S, (Σ, pathCond));;
24            P ath′ .enqueue(Σ′ , pathCond′ );

25      P ath ← P ath′ ;

26   Conf ← P ath; Cfunc ← ContractGen(Conf );
27   return (Conf, Iall , Cfunc );



 – If S is an assignment statement, as shown in Algorithm 1 starting from
   line 22, then the symbolic path is updated to (Σ′ , pathCond) for which the
   updated symbolic state Σ′ depends on the type of the assignment.
     1. If S is a variable assignment x := γ, we evaluate γ under Σ (by substitut-
        ing each integer or address variable u into symbolic expressions stored
        at A(u), namely M (A(u)), and each symbolic address (β1 , β2 ) into the
        symbolic expression M (β1 , β2 ) held at the address) to obtain a symbolic
        expression [γ]Σ , and then update the memory map at the address of x:
        Σ′ = ( M [A(x) 7→ [γ]Σ ], A ).
      Array-Carrying Symbolic Execution for Function Contract Generation       11

    2. If S is an address-of statement a := &x, we update the symbolic expres-
        sion stored at A(a) in the memory map with the address value A(x):
        Σ′ = ( M [A(a) 7→ A(x)], A ).
    3. If S is a write-back statement W (a, γ), we evaluate γ to obtain [γ]Σ , as
        described earlier. Then we update the corresponding memory entry at
        M (A(a)), i.e. the memory location at the address expression stored in
        a: Σ′ = ( M [M (A(a)) 7→ [γ]Σ ], A ).
 – If the next statement is the entry of a while loop, as shown in Algorithm
   1 starting from line 17, the symbolic executor invokes an external loop an-
   alyzer. For each symbolic path in the current configuration, the executor
   sends the current symbolic state and path conditions, as the precondition
   for the loop), to the analyzer, which returns a set of inferred invariants and
   a loop summary.
   Let Mloop denote the modifications applied to the memory map during the
   loop execution, P Cloop the path conditions of the loop, and Inv the set of
   inferred loop invariants. The invariants Inv are added to the global collection
   Iall for contract synthesis. The executor then transfers control to P Cloop and
   updates the symbolic path accordingly. This update has two components:
   (1) conjoining the inferred invariants with the current path condition, and
   (2) updating the memory map to incorporate the loop effects. For post-
   loop variable states, the executor introduces fresh symbol values for the exit
   values of the program variables to facilitate subsequent symbolic execution
   when necessary—namely, for variables modified inside the loop whose final
   values cannot be precisely determined or summarized. Our current imple-
   mentation uses a preliminary loop analyzer described in Appendix C.

    After the symbolic execution, the overall function contract Cfunc is inferred
from the final symbolic configuration Conf . The assigns clause is derived by
comparing the final memory map M of each path against the initial memory map
M0 from the function entry: any memory location whose final symbolic value
differs from its initial value is recorded as modified. The logical components of
the contract are then extracted from the accumulated path conditions pathCond
and the segment structural information in Seg. The projection step is performed
by eliminating intermediate symbols introduced during execution and retaining
only symbols associated with the function entry (for requires) and return state
(for ensures/assigns). Concretely, we substitute each symbolic address with
the corresponding source-level variable term, rewrite segment constraints into
index-range predicates over arrays, and existentially quantify auxiliary symbols
that do not correspond to user-visible program variables. The resulting formulas
characterize the preconditions and postconditions under which the function is
well-defined and the properties that must hold of its outcomes.
3.2 The Carrying of Invariants and Contiguous Array Segments

Invariant Carrying. The path-condition set pathCond records constraints over
the symbolic expressions containing symbolic values which are generated during
execution, rather than the program variables that may temporarily reference
12      Weijie Lu et al.

those expressions. When a loop invariant and its corresponding summary are
obtained from the external invariant generator, the symbolic executor may in-
troduce fresh symbolic values from V to represent the values of the integer
variables upon loop termination. The loop summary is then instantiated by sub-
stituting these fresh symbolic values for the concrete integer variables, and the
resulting condition is appended to pathCond. The symbolic execution of the re-
maining program proceeds using these newly introduced symbolic values as the
initial values for their respective integer variables.
Representing Contiguous Array Segments. We formally define contiguous array
segments using our address model. As mentioned earlier, each symbolic path
carries a set of active segments, denoted as Seg. Unlike the memory map M
which can only record independent symbolic expressions stored at discrete sym-
bolic addresses, segments capture the relationship between the properties of a
contiguous memory region and the symbolic expressions stored over that region.
Based on this, one can derive different patterns of symbolic expressions that
serve as constraint conditions associated with that memory segment.
     We define a segment s ∈ Seg as a triple s := h(βb , βo ), βlen , Ci, where
(βb , βo ) denotes the starting symbolic address of the segment, βlen is a symbolic
expression representing the number of elements in the segment, and C denotes
the content summary of the segment, representing the pattern of invariants that
hold over this segment.
     Our framework employs a hybrid strategy to obtain the content summary C:

 1. Directly-Indexed Invariants: When the array content can be expressed as
    a function of the index, C is a symbolic expression ϕ(iof f ). Here, ϕ is a
    function representing the invariant pattern, and iof f is a placeholder variable
    representing the relative offset within the segment. For example, given the
    constraint ∀0 ≤ i ≤ n−1, arr[i] = i+2 over the array arr, where n denotes the
    length of arr, one can derive the segment s = h(A(arr), 0), n − 1, ϕ(iof f ) :=
    iof f + 2i.
 2. Aggregate Abstractions: Certain program logic relies on reduction opera-
    tions [3] (e.g., sum, max) over an array range. In such cases, we model C
    as a first-class arithmetic expression, denoted as βagg := Agg(⊕, s). Here, ⊕
    represents the reduction operator and s is the target segment. Unlike logical
    constraints which are restricted to pathCond, these aggregate expressions be-
    have identically to standard symbolic expressions. Consequently, they can be
    inserted into the the memory map M as the symbolic expressions associated
    with the corresponding symbolic addresses and participate in subsequent
    arithmetic computations, enabling algebraic reasoning over array properties.

   Certain loop-based properties require quantification over the actual iteration
domain of the loop (i.e., the iterator k ranging over the loop bounds). Such
invariants cannot be captured through simple index-pattern abstractions and
therefore are not stored inside the segment tuple. Instead, they are represented
explicitly as logical statements and added to the path condition set pathCond.
      Array-Carrying Symbolic Execution for Function Contract Generation             13

    We formalize these complex invariants as quantified constraints. Formally,
such a constraint is a tuple Φ := hQ, R, ψi, representing the logical formula
Q k ∈ R.ψ(k), where Q ∈ {∀, ∃} is the quantifier, R denotes the index range,
typically defined by bounds [βlower , βupper ), and ψ(k) is the predicate over the
loop iterator k. For instance, consider the SearchZero function presented in the
overview, shown in Figure 1(a). The loop iterates through the array to find the
first non-zero element, effectively maintaining the invariant that all elements
scanned so far are zero. Our framework captures this property as the tuple
h∀, [0, i), data[k] = 0i. Here, the quantifier ∀ applies to the index range [0, i)
(where i is the current loop variable), and the predicate data[k] = 0 asserts the
specific constraint validated by the loop logic.
Updates on Segments and Invariants. During symbolic execution, the executor
maintains and forwards the array-related information encoded in the segments,
and performs the corresponding segment updates whenever a related array mem-
ory operation is executed.

 – Read R(a): Let a = (βarr , βlen ) be the symbolic address being read, where
   the offset address βlen is a symbolic expression evaluated under the current
   symbolic state. The executor first locates all segments s = h(βarr , βo ), βl , Ci ∈
   Seg whose index range may overlap with βlen , i.e., all s satisfying βo ≤ βlen <
   βo + βl . For each such segment, the executor performs an index-based sub-
   stitution, replacing the placeholder iidx in its content summary C with the
   offset βlen , yielding the expression C(βlen ). If multiple segments are simul-
   taneously feasible (e.g., due to symbolic index∨ uncertainty), the executor
   constructs a disjunctive invariant of the form C∈Cand C(βlen ), where Cand
   is the set of all feasible segments.
 – Write W (a, γ): A write operation W (a, γ) to an address a falling within
   a segment s may invalidate or split the segment. If a represents a con-
   crete offset relative to the segment base, s is split into two or more new,
   smaller segments. For instance, writing to arr[j] may split a target seg-
   ment s = h(βarr , 0), n, Ci into a prefix segment s1 = h(βp , 0), j, C1 i and a
   suﬀix segment s2 = h(βp , j + 1), n − j − 1, C2 i. The original content summary
   C is propagated to these new, smaller segments. In the current prototype,
   this splitting operation is implemented for segments with constant offset and
   length, while segments with symbolic offset or length remain a subject for
   future work.
 – Segment Merging: The framework also merges segments to maintain coarse-
   grained array summaries. After a write operation or loop analysis, a syn-
   tactic merging strategy is applied. This procedure scans all segments shar-
   ing the same base address and identifies pairs of adjacent segments—e.g.,
   s1 = h(βb , βo ), βL1 , C1 i and s2 = h(βb , βo + βL1 ), βL2 , C2 i. If their content
   summaries are syntactically equivalent, the two are merged into a single,
   larger segment snew = h(βb , βo ), βL1 + βL2 , C1 i.

   We provide an example for the carrying process as follows.
14      Weijie Lu et al.

Example 1. Consider the first code example in Figure 1(a). Starting from the in-
put ACSL precondition size ≥ 1, symbolic execution initializes i and the symbolic
state, then invokes the loop analyzer at the while entry. The analyzer returns a
disjunctive summary: one branch exits with (∀0 ≤ j < i. data[j] = 0) ∧ data[i] 6=
0 ∧ i < size, while the other exits with (∀0 ≤ j < i. data[j] = 0) ∧ i = size. We
append these formulas to pathCond, carry the corresponding segment informa-
tion in Seg, and continue symbolic execution through the final branch if (i ==
size). The two resulting paths are finally merged into a disjunctive postcondi-
tion, while the assigns set remains empty for this read-only function.

Remark 1. As our symbolic execution framework relies on specific invariant gen-
erators, we describe the current state of the art on the invariant generation with
numerical values and arrays. Numerical invariant generation (e.g., linear and
polynomial invariants) has been extensively studied, including abstract inter-
pretation [7, 13], constraint solving [4, 10, 11, 26, 28, 39, 41, 61], recurrence analy-
sis [29,58], etc. Invariant generation with arrays is mostly tackled via contiguous
array segments [15, 22, 35, 38]. Array invariants can also be solved via CHC solv-
ing [19]. A recent result investigates instrumentation [3] to aid the generation of
array invariants.

3.3 Prototype Implementation Detail
Our prototype is implemented on top of the Clang/LLVM toolchain [36] that
comprises about 19000 lines in C++. We use the Clang front-end to obtain
the abstract syntax tree of the input C program and traverse the AST to con-
struct the intermediate program syntax S and the initial symbolic configuration
described in Section 3.1. Our framework incorporates records and pointer arith-
metic. For pointer arithmetic, the current implementation supports simple forms
(e.g., linear base-plus-offset patterns), but does not yet handle complex shape
analysis such as linked lists or binary trees. For each analyzed function, the
framework generates corresponding ACSL annotations [5] that encode the syn-
thesized function contract, including preconditions, postconditions, and assigns
clauses. These annotations are then fed to Frama-C [31], where the WP plugin
is used to automatically discharge the resulting proof obligations and thereby val-
idate the soundness of the inferred contracts with respect to the original C code.
Loop reasoning in the prototype is realized via the plugin-based LoopAnalyzer
introduced in Appendix C.

4 Evaluation

We evaluate our symbolic execution framework by comparing it against Au-
toDeduct [50], a state-of-the-art toolchain capable of generating ACSL anno-
tations for C programs. The toolchain incorporates Saida [52], which requires
TriCera [19, 53, 57], and the Interface Specification Propagator (ISP) [51] to
manage, propagate, and emit specifications. We do not compare with popular
software verification tools such as Seahorn [23] and CPAChecker [6] since they
        Array-Carrying Symbolic Execution for Function Contract Generation       15

usually require assertions to verify, while our approach does not require asser-
tions and instead tries to generate precise contracts without manually given
assertions. We also do not compare with large language models as they follow
a completely different principle (see Appendix D for details). All experiments
were conducted in a Docker container based on Ubuntu 24.04.3 LTS running
on a WSL2 host (version 6.6.87.2-microsoft-standard-WSL2) on a machine with
AMD Ryzen 7 8845H CPU and 8 GB RAM1
4.1 Experimental Setup

Benchmarks. We assembled a diverse dataset of 282 C programs comprising five
distinct benchmark suites collected in [59], together with an additional set of
real-world cryptographic routines, ranging from micro-benchmarks to realistic
cryptographic modules:
1. SyGuS [1]: 133 C programs with single loops, adapted from the SyGuS
   competition.
2. OOPSLA-13 [18]: 46 programs featuring various loop types, used in prior
   loop analysis research.
3. Frama-C Problems: 51 programs covering diverse logic patterns.
4. SV-Comp: 14 complex programs selected from the Software Verification
   Competition.
5. X-509: 6 programs derived from realistic PKI certificate processing code.
6. openHiTLS: 31 C functions extracted from the openHiTLS project, a mod-
   ular high-performance TLS and cryptographic library, covering big-number
   arithmetic, low-level buffer operations, and certificate-processing related rou-
   tines.

Baseline and Configuration. As mentioned previously, we compare our approach
with AutoDeduct. To ensure a fair comparison regarding execution time, we
account for the runtime characteristics of AutoDeduct, which is partially im-
plemented in Scala and relies on the JVM. We execute AutoDeduct twice on
the benchmarks without stopping the container; data from the second run is
recorded to mitigate JVM warm-up and JIT compilation overheads.
Verification Workflow. For both tools, the evaluation follows a strictly auto-
mated pipeline: (1) The tool takes the C source code as input and generates an
annotated file with ACSL contracts (preconditions, postconditions, loop invari-
ants, and assigns clauses). (2) The annotated file is passed to the Frama-C WP
plugin. (3) A verification is considered “Success” only if Frama-C WP can prove
all generated verification goals.
4.2 Experimental Results

RQ1: Effectiveness and Precision. We assess effectiveness by the number
of programs for which the tools generate suﬀicient invariants and contracts to
satisfy Frama-C WP. Table 1 summarizes the results.
1
    We provide the source code, Docker environment, and benchmark scripts at: https:
    //doi.org/10.5281/zenodo.18601854.
16       Weijie Lu et al.

Table 1. Comparison of verification results. The reported runtime for our approach
includes both symbolic execution and invariant-generation time. We additionally re-
port partial-verification, timeout, and generation-failure counts to make unresolved
cases explicit. Full: Fully verified; Part.: Partial verification (ACSL generated but
verification failed); T/O: Timeout; Fail: Generation failed; Time: Average runtime
for successfully generated cases; AD: AutoDeduct

                      Full (#) Part. (#) T/O (#) Fail (#) Time (s)
 Suite          Total Ours AD Ours AD Ours AD Ours AD Ours AD
 SyGuS             133      53    0    78 131      0    0     2    2 0.140     2.23
 OOPSLA-13          46       2    1    20 42       0    0    24    3 0.141     4.44
 Frama-C            51       9    8    29 34       1    0    13    9 0.260     2.26
 SV-Comp            14       3    0     5 13       0    0     6    1 0.065     3.48
 X-509               6       1    1     2   5      0    0     3    0 0.090     1.98
 openHiTLS          31       0    0    10   0      0    0    21   31 0.080        –
 Total            281       68   10   143 225     1     0    69   46 0.148 2.703



    Our framework demonstrates significantly higher precision than the base-
line. Out of the total 281 benchmarks, our tool successfully generated verifiable
contracts for 68 programs. In contrast, AutoDeduct was only able to achieve
complete verification for 10 programs. This disparity highlights the advantage
of carrying segment-based array invariants and handling pointer arithmetic re-
cursively, which allows our tool to prove complex properties that rely on precise
memory information.
RQ2: Eﬀiciency and Scalability. As shown in the “Avg. Time” column of
Table 1, our framework demonstrates a substantial performance advantage.
The weighted average execution time for our tool is 0.160 seconds per file,
whereas AutoDeduct averages 2.706 seconds. This represents an approximate
17.1× speedup. While AutoDeduct incurs overhead from the JVM environment
(even after accounting for warm-up phases), our tool’s eﬀiciency stems primarily
from the lightweight design of the symbolic execution engine. By carrying ar-
ray segments and invariants abstractly rather than unrolling loops or explicitly
enumerating all array elements, our approach minimizes the symbolic state ex-
plosion, allowing for rapid analysis even on benchmarks with partial verification.
Analysis of failed cases. To better understand the limitations of both tools,
we analyzed the cases classified as “Fail” (Generation Failed) and those that
generated contracts but failed to fully verify (“Part.”).
    For our framework, Fail (69 cases) are primarily caused by syntax limita-
tions in the current prototype. Specifically, the tool currently lacks support for
certain bitwise and arithmetic operators (e.g., %, <<, >>) and does not yet han-
dle nested loops. When these constructs are encountered, the analysis aborts to
avoid unsoundness. The single T/O case is due to a program bug in our han-
dling of recursive functions, which triggers unintended infinite recursion during
       Array-Carrying Symbolic Execution for Function Contract Generation            17

analysis. The cases of Part. (where contracts are generated but not proven)
are largely attributed to the loop invariant inference. While our plugin system
captures many properties, some complex loops require stronger inductive in-
variants than our current plugins can synthesize. Moreover, another reason is
that the current invariant generation methods have some compatibility issues
with ACSL format and Frama-C WP. Nevertheless, the generated contracts re-
main semantically meaningful: manual inspection confirms that they accurately
characterize the memory footprints and critical range constraints, providing a
valuable descriptive summary of the function behaviour.
    In contrast, AutoDeduct’s failures are more structural. Its Fail cases often
result from unsupported C syntax involving complex array initializers. More
critically, its low verification success rate (only 10 fully verified) is due to its in-
ability to incorporate loop invariants. For the vast majority of programs contain-
ing loops, AutoDeduct fails to synthesize the necessary loop invariant clauses,
rendering the generated ACSL unverifiable by Frama-C WP.

5 Conclusion
In this work, we proposed a framework for symbolic execution that carries con-
tiguous array segments and invariants to address the automated generation of
function contracts with array manipulations. The main feature of our framework
is the carry of contiguous array segments and array invariants (with merging and
split operations) along the symbolic execution. A prototype is implemented in
LLVM. Future works include a more thorough treatment of invariants into the
splitting and merging of array segments, an extension in interprocedural analysis
that utilizes contracts of lower level functions to generate contracts of higher level
functions, and a deeper integration with existing invariant generation methods.

Acknowledgement
The authors would like to thank the anonymous reviewers for their valuable com-
ments and constructive suggestions that helped improve the quality of this paper.
This work is partially supported by the National Natural Science Foundation of
China (NSFC) under Grant No. 62572297 and sponsored by the CCF-Huawei
Populus Grove Fund.

References
 1. Alur, R., Fisman, D., Padhi, S., Singh, R., Udupa, A.: Sygus-comp 2018: Results
    and analysis (2019), https://arxiv.org/abs/1904.07146
 2. Amilon, J.: Automated inference of acsl function contracts using tricera (2021)
 3. Amilon, J., Esen, Z., Gurov, D., Lidström, C., Rümmer, P.: Automatic program
    instrumentation for automatic verification. In: Enea, C., Lal, A. (eds.) Computer
    Aided Verification - 35th International Conference, CAV 2023, Paris, France, July
    17-22, 2023, Proceedings, Part III. Lecture Notes in Computer Science, vol. 13966,
    pp. 281–304. Springer (2023). https://doi.org/10.1007/978-3-031-37709-9_14
18      Weijie Lu et al.

 4. Asadi, A., Chatterjee, K., Fu, H., Goharshady, A.K., Mahdavi, M.: Polynomial
    reachability witnesses via stellensätze. In: Freund, S.N., Yahav, E. (eds.) PLDI
    ’21: 42nd ACM SIGPLAN International Conference on Programming Language
    Design and Implementation, Virtual Event, Canada, June 20-25, 2021. pp. 772–
    787. ACM (2021). https://doi.org/10.1145/3453483.3454076, https://doi.
    org/10.1145/3453483.3454076
 5. Baudin, P., Filliâtre, J.C., Marché, C., Monate, B., Moy, Y., Prevosto, V.: ACSL:
    ANSI/ISO C specification. URL https://frama-c.com/html/acsl.html (2021)
 6. Beyer, D., Keremoglu, M.E.: Cpachecker: A tool for configurable software verifi-
    cation. In: Gopalakrishnan, G., Qadeer, S. (eds.) Computer Aided Verification -
    23rd International Conference, CAV 2011, Snowbird, UT, USA, July 14-20, 2011.
    Proceedings. Lecture Notes in Computer Science, vol. 6806, pp. 184–190. Springer
    (2011). https://doi.org/10.1007/978-3-642-22110-1_16
 7. Boutonnet, R., Halbwachs, N.: Disjunctive relational abstract interpretation for in-
    terprocedural program analysis. In: Enea, C., Piskac, R. (eds.) Verification, Model
    Checking, and Abstract Interpretation - 20th International Conference, VMCAI
    2019, Cascais, Portugal, January 13-15, 2019, Proceedings. Lecture Notes in Com-
    puter Science, vol. 11388, pp. 136–159. Springer (2019). https://doi.org/10.100
    7/978-3-030-11245-5_7
 8. Cadar, C., Dunbar, D., Engler, D.R., et al.: Klee: unassisted and automatic gen-
    eration of high-coverage tests for complex systems programs. In: OSDI. vol. 8, pp.
    209–224 (2008)
 9. CEA LIST: Frama-C: A software analysis platform (2024), https://frama-c.com
10. Chatterjee, K., Fu, H., Goharshady, A.K., Goharshady, E.K.: Polynomial invariant
    generation for non-deterministic recursive programs. In: Donaldson, A.F., Torlak,
    E. (eds.) Proceedings of the 41st ACM SIGPLAN International Conference on
    Programming Language Design and Implementation, PLDI 2020, London, UK,
    June 15-20, 2020. pp. 672–687. ACM (2020). https://doi.org/10.1145/338541
    2.3385969
11. Colón, M., Sankaranarayanan, S., Sipma, H.: Linear invariant generation using
    non-linear constraint solving. In: Jr., W.A.H., Somenzi, F. (eds.) Computer Aided
    Verification, 15th International Conference, CAV 2003, Boulder, CO, USA, July 8-
    12, 2003, Proceedings. Lecture Notes in Computer Science, vol. 2725, pp. 420–432.
    Springer (2003). https://doi.org/10.1007/978-3-540-45069-6_39
12. Cordeiro, L., Fischer, B., Marques-Silva, J.: Smt-based bounded model checking
    for embedded ansi-c software. IEEE Transactions on Software Engineering 38(4),
    957–974 (2011)
13. Cousot, P., Cousot, R.: Abstract interpretation: a unified lattice model for static
    analysis of programs by construction or approximation of fixpoints. In: Proceedings
    of the 4th ACM SIGACT-SIGPLAN symposium on Principles of programming
    languages. pp. 238–252 (1977)
14. Cousot, P., Cousot, R., Fähndrich, M., Logozzo, F.: Automatic inference of nec-
    essary preconditions. In: Giacobazzi, R., Berdine, J., Mastroeni, I. (eds.) Veri-
    fication, Model Checking, and Abstract Interpretation, 14th International Con-
    ference, VMCAI 2013, Rome, Italy, January 20-22, 2013. Proceedings. Lecture
    Notes in Computer Science, vol. 7737, pp. 128–148. Springer (2013). https:
    //doi.org/10.1007/978-3-642-35873-9_10
15. Cousot, P., Cousot, R., Logozzo, F.: A parametric segmentation functor for fully
    automatic and scalable array content analysis. In: Ball, T., Sagiv, M. (eds.) Pro-
    ceedings of the 38th ACM SIGPLAN-SIGACT Symposium on Principles of Pro-
       Array-Carrying Symbolic Execution for Function Contract Generation            19

    gramming Languages, POPL 2011, Austin, TX, USA, January 26-28, 2011. pp.
    105–118. ACM (2011). https://doi.org/10.1145/1926385.1926399
16. Cousot, P., Cousot, R., Logozzo, F.: Precondition inference from intermittent as-
    sertions and application to contracts on collections. In: International Workshop on
    Verification, Model Checking, and Abstract Interpretation. pp. 150–168. Springer
    (2011)
17. Cuoq, P., Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.:
    Frama-C: A software analysis perspective. In: Proceedings of the 10th International
    Conference on Software Engineering and Formal Methods (SEFM 2012). LNCS,
    vol. 7504, pp. 233–247. Springer (2012), software version 31.0 (Gallium) used in
    this work
18. Dillig, I., Dillig, T., Li, B., McMillan, K.: Inductive invariant generation via ab-
    ductive inference. SIGPLAN Not. 48(10), 443–456 (Oct 2013). https://doi.org/
    10.1145/2544173.2509511
19. Esen, Z., Rümmer, P.: TriCera: Verifying C programs using the theory of heaps.
    In: Proceedings of the 22nd Conference on Formal Methods in Computer-Aided
    Design (FMCAD 2022). pp. 360–367. TU Wien Academic Press (2022). https:
    //doi.org/10.34727/2022/isbn.978-3-85448-053-2_45
20. Garcia-Contreras, I., Gurfinkel, A., Navas, J.A.: Eﬀicient modular SMT-based
    model checking of pointer programs. In: International Static Analysis Symposium.
    pp. 227–246. Springer (2022)
21. Ghilardi, S., Nicolini, E., Ranise, S., Zucchelli, D.: Towards SMT model checking of
    array-based systems. In: International Joint Conference on Automated Reasoning.
    pp. 67–82. Springer (2008)
22. Gopan, D., Reps, T.W., Sagiv, S.: A framework for numeric analysis of array
    operations. In: Palsberg, J., Abadi, M. (eds.) Proceedings of the 32nd ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL
    2005, Long Beach, California, USA, January 12-14, 2005. pp. 338–350. ACM
    (2005). https://doi.org/10.1145/1040305.1040333
23. Gurfinkel, A., Kahsai, T., Komuravelli, A., Navas, J.A.: The seahorn verification
    framework. In: Kroening, D., Pasareanu, C.S. (eds.) Computer Aided Verification
    - 27th International Conference, CAV 2015, San Francisco, CA, USA, July 18-
    24, 2015, Proceedings, Part I. Lecture Notes in Computer Science, vol. 9206, pp.
    343–361. Springer (2015). https://doi.org/10.1007/978-3-319-21690-4_20
24. Hojjat, H., Rümmer, P.: The eldarica horn solver. In: 2018 Formal Methods in
    Computer Aided Design (FMCAD). pp. 1–7. IEEE (2018)
25. Holík, L., Peringer, P., Rogalewicz, A., Šoková, V., Vojnar, T., Zuleger, F.: Low-
    level Bi-abduction. In: 36th European Conference on Object-Oriented Program-
    ming (ECOOP 2022). LIPIcs (2022), arXiv:2205.02590
26. Ji, Y., Fu, H., Fang, B., Chen, H.: Aﬀine loop invariant generation via ma-
    trix algebra. In: Shoham, S., Vizel, Y. (eds.) Computer Aided Verification -
    34th International Conference, CAV 2022, Haifa, Israel, August 7-10, 2022, Pro-
    ceedings, Part I. Lecture Notes in Computer Science, vol. 13371, pp. 257–281.
    Springer (2022). https://doi.org/10.1007/978-3-031-13185-1_13, https:
    //doi.org/10.1007/978-3-031-13185-1_13
27. Kapus, T., Cadar, C.: A segmented memory model for symbolic execution. In:
    ESEC/FSE. pp. 1002–1012. ACM (2019)
28. Ke, J., Fu, H., Liu, H., Sun, Z., Chen, L., Li, G.: Aﬀine disjunctive invariant
    generation with Farkas’lemma. In: International Conference on Verification, Model
    Checking, and Abstract Interpretation. pp. 187–213. Springer (2025)
20      Weijie Lu et al.

29. Kincaid, Z., Cyphert, J., Breck, J., Reps, T.: Non-linear reasoning for invariant
    synthesis. Proceedings of the ACM on Programming Languages 2(POPL), 1–33
    (2017)
30. King, D., Koutavas, V., Kovács, L.: LLM-Based Generation of Weakest
    Preconditions and Precise Array Invariants. In: Proceedings of the 13th
    IEEE/ACM International Conference on Formal Methods in Software Engineering,
    (FormaliSE@ICSE’25). pp. 1–5. IEEE (2025)
31. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.: Frama-c: A
    software analysis perspective. Formal aspects of computing 27(3), 573–609 (2015)
32. Komuravelli, A., Gurfinkel, A., Chaki, S.: SMT-based model checking for recursive
    programs. Formal Methods Syst. Des. 48(3), 175–205 (2016). https://doi.org/
    10.1007/S10703-016-0249-4
33. Kremenek, T.: Finding software bugs with the clang static analyzer. Apple Inc 8,
    2008 (2008)
34. Krishna, M., Gaur, B., Verma, A., Jalote, P.: Using LLMs in Software
    Requirements Specifications: An Empirical Evaluation. In: Preceedings of the 32nd
    IEEE International Requirements Engineering Conference (RE’24). pp. 475–483.
    IEEE (2024)
35. Larraz, D., Rodríguez-Carbonell, E., Rubio, A.: SMT-based array invariant gen-
    eration. In: Giacobazzi, R., Berdine, J., Mastroeni, I. (eds.) Verification, Model
    Checking, and Abstract Interpretation, 14th International Conference, VMCAI
    2013, Rome, Italy, January 20-22, 2013. Proceedings. Lecture Notes in Computer
    Science, vol. 7737, pp. 169–188. Springer (2013). https://doi.org/10.1007/97
    8-3-642-35873-9_12
36. Lattner, C., Adve, V.: LLVM: A compilation framework for lifelong program
    analysis & transformation. In: Proceedings of the International Symposium on
    Code Generation and Optimization (CGO’04). pp. 75–86. IEEE Computer Society
    (2004), software version 19.1.7 used in this work
37. Le-Cong, T., Le, B., Murray, T.: Can LLMs Reason About Program Semantics? A
    Comprehensive Evaluation of LLMs on Formal Specification Inference. In: Proceed-
    ings of the 63rd Annual Meeting of the Association for Computational Linguistics
    (ACL’25). pp. 21991–22014. Association for Computational Linguistics (2025)
38. Li, B., Tang, Z., Zhai, J., Zhao, J.: Automatic invariant synthesis for arrays in
    simple programs. In: 2016 IEEE International Conference on Software Quality,
    Reliability and Security (QRS). pp. 108–119. IEEE (2016)
39. Li, Y., Fu, H., Long, H., Li, G.: Constraint based invariant generation with modular
    operations. In: Bourke, T., Chen, L., Goharshady, A.K. (eds.) Dependable Software
    Engineering. Theories, Tools, and Applications - 10th International Symposium,
    SETTA 2024, Hong Kong, China, November 26-28, 2024, Proceedings. Lecture
    Notes in Computer Science, vol. 15469, pp. 64–84. Springer (2024). https://doi.
    org/10.1007/978-981-96-0602-3_4, https://doi.org/10.1007/978-981-96-0
    602-3_4
40. Liu, C., Wu, X., Feng, Y., Cao, Q., Yan, J.: Towards General Loop Invariant
    Generation: A Benchmark of Programs with Memory Manipulation. In: Annual
    Conference on Neural Information Processing Systems( NeurIPS’24). Advances in
    Neural Information Processing Systems, vol. 38 (2024)
41. Liu, H., Fu, H., Yu, Z., Song, J., Li, G.: Scalable linear invariant genera-
    tion with Farkas’lemma. Proceedings of the ACM on Programming Languages
    6(OOPSLA2), 204–232 (2022)
        Array-Carrying Symbolic Execution for Function Contract Generation                              21

42. Liu, R., Chen, M., Wu, L., Ke, J., Li, G.: Enhancing Automated Loop Invariant
    Generation for Complex Programs with Large Language Models. Science of Com-
    puter Programming 248, 103387 (2026)
43. Ma, L., Liu, S., Li, Y., Xie, X., Bu, L.: SpecGen: Automated Generation of Formal
    Program Specifications via Large Language Models. In: Proceedings of the 47th
    IEEE/ACM International Conference on Software Engineering, (ICSE’25). pp. 16–
    28. IEEE (2025)
44. Maksimović, P., Ayoun, S.É., Santos, J.F., Gardner, P.: Gillian, part II: Real-world
    verification for javascript and c. In: Computer Aided Verification (CAV 2021),
    Proceedings, Part II. Lecture Notes in Computer Science, vol. 12760, pp. 827–850.
    Springer (2021). https://doi.org/10.1007/978-3-030-81688-9_38
45. McCloskey, B., Reps, T.W., Sagiv, M.: Statically inferring complex heap, array,
    and numeric invariants. In: Cousot, R., Martel, M. (eds.) Static Analysis - 17th
    International Symposium, SAS 2010, Perpignan, France, September 14-16, 2010.
    Proceedings. Lecture Notes in Computer Science, vol. 6337, pp. 71–99. Springer
    (2010). https://doi.org/10.1007/978-3-642-15769-1_6
46. openHiTLS Project: openhitls. https://github.com/openHiTLS/openHiTLS
    (2023), cryptography and TLS library. Accessed: 2025-11-27
47. Pei, K., Bieber, D., Shi, K., Sutton, C., Yin, P.: Can Large Language Models
    Reason about Program Invariants? In: International Conference on Machine Learn-
    ing (ICML’23). Proceedings of Machine Learning Research, vol. 202, pp. 27496–
    27520. PMLR (2023)
48. Pirzada, M.A.A., Reger, G., Bhayat, A., Cordeiro, L.C.: LLM-generated Invariants
    for Bounded Model Checking without Loop Unrolling. In: Proceedings of the
    39th IEEE/ACM International Conference on Automated Software Engineering
    (ASE’24). pp. 1395–1407. ACM (2024)
49. Ramos, D.A., Engler, D.: Under-constrained symbolic execution: Correctness
    checking for real code. In: USENIX Security (2015)
50. RSE-Verification: Auto-Deduct Toolchain: Automated formal verifica-
    tion toolchain. h t t p s : / / g i t h u b . c o m / r s e - v e r i f i c a t i o n / a u t o - d e d
    u c t- t o o l c h a in (2025), accessed: 2025-11-30, Branch: main, Commit:
    cc41d5a602ab58dc997662530a8aa23efac36633
51. RSE-Verification: Interface Specification Propagator (ISP): Frama-c plugin. https:
    //github.com/rse- verification/interface- specification- propagator
    (2025), accessed: 2025-11-30
52. RSE-Verification: Saida: A frama-c plugin for acsl contract verification. https:
    //github.com/rse-verification/saida (2025), accessed: 2025-11-30
53. RSE-Verification: Tricera: A model checker for c programs (rse-verification fork).
    https://github.com/rse-verification/tricera (2025), accessed: 2025-11-30.
    Fork of https://github.com/uuverifiers/tricera
54. Sankaranarayanan, S., Sipma, H.B., Manna, Z.: Constraint-based linear-relations
    analysis. In: Giacobazzi, R. (ed.) Static Analysis, 11th International Symposium,
    SAS 2004, Verona, Italy, August 26-28, 2004, Proceedings. Lecture Notes in Com-
    puter Science, vol. 3148, pp. 53–68. Springer (2004). https://doi.org/10.1007/
    978-3-540-27864-1_7, https://doi.org/10.1007/978-3-540-27864-1_7
55. Santos, J.F., Maksimović, P., Ayoun, S.É., Gardner, P.: Gillian, part I: A multi-
    language platform for symbolic execution. In: Proceedings of the 41st ACM SIG-
    PLAN International Conference on Programming Language Design and Implemen-
    tation (PLDI 2020). pp. 927–942. ACM (2020). https://doi.org/10.1145/3385
    412.3386014
22      Weijie Lu et al.

56. The LLVM Compiler Infrastructure: LLVM compiler infrastructure (2025), https:
    //llvm.org, release 19.1.7
57. Uppsala University (uuverifiers): TriCera: A model checker for C programs. https:
    //github.com/uuverifiers/tricera (2025), accessed: 2025-11-30
58. Wang, C., Lin, F.: Solving conditional linear recurrences for program verification:
    The periodic case. Proc. ACM Program. Lang. 7(OOPSLA1), 28–55 (2023). https:
    //doi.org/10.1145/3586028
59. Wen, C., Cao, J., Su, J., Xu, Z., Qin, S., He, M., Li, H., Cheung, S., Tian, C.:
    Enchanting Program Specification Synthesis by Large Language Models Using
    Static Analysis and Program Verification. In: Proceedings of the 36th International
    Conference on Computer Aided Verification (CAV’24) Part II. Lecture Notes in
    Computer Science, vol. 14682, pp. 302–328. Springer (2024)
60. Xie, D., Yoo, B., Jiang, N., Kim, M., Tan, L., Zhang, X., Lee, J.S.: How Effective
    are Large Language Models in Generating Software Specifications? In: Proceedings
    of the 32nd IEEE International Conference on Software Analysis, Evolution and
    Reengineering (SANER’25). pp. 1–12. IEEE (2025)
61. Yao, P., Ke, J., Sun, J., Fu, H., Wu, R., Ren, K.: Demystifying template-based
    invariant generation for bit-vector programs. In: 38th IEEE/ACM International
    Conference on Automated Software Engineering, ASE 2023, Luxembourg, Septem-
    ber 11-15, 2023. pp. 673–685. IEEE (2023). https://doi.org/10.1109/ASE56229
    .2023.00069, https://doi.org/10.1109/ASE56229.2023.00069


A A Basic Program Model
We consider arithmetic programs with array manipulations as the basic program
model for the function body of a function. The syntax is given as follows.


  e ::= c | x | e1 ⊕ e2 | ar[e],       ⊕ ∈ {+, −, ∗}
  b ::= e1 ⊗ e2 | ¬b | b1 ∧ b2 | b1 ∨ b2 ,        ⊗ ∈ {≤, <, ≥, >, 6=, =}
 P ::= x := e | ar[x] := e | if b then P1 else P2 | while b do P | P1 ; P2


    In the grammar above, the nonterminal e stands for an arithmetic expres-
sion with array entries that is composed of integer variables x, integer constants
c, arithmetic operations including addition, subtraction and multiplication (we
omit division to avoid floating point errors and division by zero for simplicity)
and array entry accesses ar[e] with the array variable ar and index arithmetic
expression e (meaning the element residing in the array a at the index e). The
nonterminal b stands for boolean expressions that are built from comparison
of arithmetic expressions and propositional logic connectives. The nonterminal
P stands for program statements that involve standard imperative constructs
such as variable assignment statement x := e (assigning the value of expression
e to the integer variable x), array assignment statement ar[x] := e (changing
the element of index x in the array ar to the value of expression e), conditional
branches if b then P1 else P2 (executing P1 if b evaluates to true and P2 oth-
erwise), while loops while b do P (repeatedly executing P until b evaluates to
      Array-Carrying Symbolic Execution for Function Contract Generation       23

false), and sequential composition P1 ; P2 (executing P1 first and P2 second). We
omit array creation statements and simply assume that each array variable is
initialized to a contiguous segment of memory units with finite length. In our ba-
sic program model, we only allow arrays with integer elements. Moreover, upon
encountering a function call, we simply inline the function. We do not consider
recursive functions in this work.
    The operational semantics of our basic program model is given by transition
systems with memory model. To illustrate our operational semantics, we first
present our memory model as follows.
Memory Model. We consider a unified memory model in which all integer vari-
ables and array contents reside in a single unbounded contiguous memory region,
without distinguishing between heap and stack memories. Each integer and ar-
ray variable is assigned a unique, non-overlapping address that remains fixed
during program execution.
    Formally, let the set Addr of memory addresses simply be the set of non-
negative integers, and X be the set of integer and array variables appearing in
the underlying program. An address map is an injective map A : X → Addr
from the set of program variables X to the address space Addr that specifies
the addresses of the variables, for which the injective property ensures disjoint
memory allocation of variables. A memory map is a map M : Addr → Val that
for each address a, M (a) is the integer element that resides at this address.
It follows that given an address map A and a memory map M , the notation
M (A(x)) with an integer variable x denotes the value of the variable, and the
notation M (A(ar) + i) denotes the array entry ar[i]. Here, the index i is also
called the address offset w.r.t the address of the array variable ar. Since all
addresses are statically assigned and disjoint, array access operations can be
treated as direct access to symbolic addresses, and therefore we do not consider
aliasing of different array variables.
    Usually, one requires that array contents are allocated as contiguous and
non-overlapping memory ranges. Formally, if A, B ∈ X are array variables with
implicit lengths |A| and |B| (measured in addressable cells), then their address
memory intervals [A(A), A(A) + |A| − 1] and [A(B), A(B) + |B| − 1] should
be disjoint, i.e., IA ∩ IB = ∅. In this work, we take a lightweight treatment of
array bounds so that each array variable ar is treated as a pointer. This allows
the index i in an array access ar[i] to be unbounded. We do not eliminate array
out-of-bounds explicitly.
    Below we present our control flow graph to represent the execution workflow
of a program in our program model. The control flow graph consists of locations
(referring to program counters) and transitions between these locations.
Control flow graphs. A control flow graph (CFG) is a tuple T = hX, L, T, θi,
where:

 – X is a finite set of integer and array variables that refer to the variables
   appearing in the concerned program.
24      Weijie Lu et al.

 – L is a finite set of locations with a designated initial location l∗ and a desig-
   nated end (termination) location l⊥ . Each location corresponds to a program
   counter in the underlying program.
 – T is a finite set of transitions. Each transition τ ∈ T is a tuple hℓ, ℓ′ , g, F i
   that specifies the execution of a statement moving from the location ℓ to the
   location ℓ′ in the underlying program, for which the component g is the guard
   condition of the transition that is a formula over integer and array variables,
   and F is the update function of the execution that maps the current memory
   map M and address map A to the next memory map F (M, A) after the
   execution of the transition.
 – θ is the initial condition that specifies constraints on the initial values of
   integer variables and the initial memory content of array variables.

In a CFG, the update function of a transition is determined by the statement
in the original program to be executed by the transition. For example, if the
statement is an array assignment statement ar[x] := e, then the update function
updates the current memory map (w.r.t the current variable map) by chang-
ing the integer value held at the address M (A(ar) + x) to be the value of the
expression e.
    A transformation of a program in our program model into its control flow
graph is straightforward. One just collects the program counters in the pro-
gram and establish the transitions between the locations. Below we list several
representative cases in a transformation.
 – If a program counter ℓ corresponds to a conditional statement with condition
   b, then we have two transitions (ℓ, ℓthen , b, id) and (ℓ, ℓelse , ¬b, id), where ℓthen
   (resp. ℓelse ) is the program counter of the then (resp. else) branch, and id is
   the identity update function such that id(M, A) = M for all M, A.
 – If a program counter ℓ corresponds to an assignment statement ar[x] :=
   e, then we have a transition (ℓ, ℓ′ , true, Far[x]:=e ) for which Far[x]:=e is the
   update function for the assignment statement such that given a memory map
   M and an address map A, Far[x]:=e (M, A) is the memory map that changes
   the integer value M (A(x)) to the evaluation result of the expression e under
   M and A, and keeps other memory values in M unchanged. Note that the
   address map A keeps unchanged.
 – If a program counter ℓ corresponds to the entry point of a while loop with
   loop guard b, then it has two transitions (ℓ, ℓ′ , b, id) and (ℓ, ℓ′′ , ¬b, id), for
   which ℓ′ is the program counter of the starting point of the loop body, and
   ℓ′′ is the successor program counter after the while loop. Moreover, if a
   program counter ℓ refers to the last statement in the loop body of a while
   loop, then its successor location is set to the entry point of the loop.

   A further transformation from a CFG in our program model into the gram-
mar in our symbolic execution is straightforward: just assigns non-overlapping
address constants from Addr to integer and array variables so that each variable
receives a distinct address constant, and the assignments respect that the con-
tents of different arrays in the memory are non-overlapping. Furthermore, one
       Array-Carrying Symbolic Execution for Function Contract Generation                  25

treats every array access ar[β] as the read operation R(b), where a fresh address
variable b is introduced to represent the symbolic address (ar, β · sar ). Here, the
variable ar denotes the base address of the array, while the expression β · sar
specifies the address offset, with β indicating the index position of the accessed
element and sar representing the size of each element in the array.
    Given a CFG, a program state is a tuple (M, A) for which M is the current
memory map and A is the address map that does not change throughout the
program execution. A configuration is an ordered pair (ℓ, (M, A)) for which ℓ
represents the current location and (M, A) represents the current memory map
and (fixed) address map. Recall that given a configuration (ℓ, (M, A)), the cur-
rent value of an integer variable x is given by M (A(x)). Given a formula ψ over
integer and array variables and a program state σ = (M, A), we write σ |= ψ to
denote that σ satisfies ψ, i.e., ψ is true when its open variables are substituted
by their integer/memory values in σ.
    The operation semantics of a CFG T = hX, L, T, θi is given by execution
paths as follows. An execution path π in a CFG is a finite sequence of configu-
rations π = (ℓ0 , σ0 ), (ℓ1 , σ1 ), . . . , (ℓk , σk ) such that:
 – ℓ0 = ℓ∗ and σ0 |= θ, i.e., the execution path starts from the initial location
   and the initial program state fulfills the initial condition θ.
 – for every 0 ≤ j ≤ k − 1, there exists a transition τ = hℓ, ℓ′ , g, F i ∈ T such
   that ℓ = ℓj , ℓ′ = ℓj+1 , σj |= g and σj+1 = (F (σ), A0 ) where A0 is the address
   map in σ0 that does not change throughout the execution path.
     Informally, an execution path specifies a run of the CFG under a possible
initial program state that fulfills the initial condition θ. In an execution path π =
(ℓ0 , σ0 ), (ℓ1 , σ1 ), . . . , (ℓk , σk ), each (ℓj , σj ) (0 ≤ j ≤ k) represents the program
state after executing j statements along the path.


B Invariants and Function Contracts
In this work, we consider invariants and function contracts of programs in our
program model. Below we give the formal definitions of invariant and function
contracts. Let Γ = (X, L, T, θ) be a CFG of concern.
Invariants. We define invariants in the form of assertion maps [11,28,41,54]. An
assertion map is a map η that assigns each location ℓ ∈ L a formula η(ℓ) over
the integer and array variables. An invariant is then an assertion map I such
that for every execution path π = {(ℓ0 , σ0 ), (ℓ1 , σ1 ), . . . , (ℓk , σk )}, we have that
σj |= I(ℓj ) for all 0 ≤ j ≤ k. Informally, an invariant over-approximates the
set of reachable program states (i.e., program states that could appear in some
execution path).
Function contracts. To define the notion of function contracts, we first de-
fine assigns information as follows. An assigns information Assgn is a finite
set of (contiguous) array segments, for which each array segment takes the
form ar[start..end] where ar is an array variable, start is the start index ex-
pression of the segment and end is the end index expression of the segment.
26       Weijie Lu et al.

Given an array segment ar[start..end] and a program state (M, A), the con-
crete address range har[start..end]i(M, A) is defined as the interval [M (A(ar))+
hstarti(M, A), M (A(ar)) + hendi(M, A))], where for an arithmetic expression e
with array accesses, the notation hei(M, A) means the evaluation of the expres-
sion e by substituting the variables in e by the integer and memory values in
(M, A). Given an assigns information Assgn and a program state σ, the con-
crete
∪     address range hAssgni(σ) covered by Assgn under σ, is given as the union
  S∈Assgn
           hSi(σ).
    We now define function contracts. A function contract specifies the expected
behavior of a function in terms of its input–output relation and side effects on
the program state. It typically consists of a precondition Pre that is a formula to
constrain the valid inputs with which the function may be invoked, a postcondi-
tion Post that is a formula specifying a property that any resultant program state
after the execution of a function starting from some program state satisfying the
precondition Pre should fulfill, and an assigns information Assgn that specifies
the memory addresses whose content may be modified during the execution of
the function.
    Formally, a function contract C of a function whose function body has the
CFG T is defined as a tuple C = hPre, Post, Assgni where Pre, Post are formulas
over the integer and array variables and Assgn is an assigns information, such
that for any execution path π = (ℓ0 , σ0 ), (ℓ1 , σ1 ), . . . , (ℓk , σk ) satisfying σ0 |= Pre
and ℓk = ℓ⊥ , we have that σk |= Post and the set of memory addresses over which
σk and σ0 hold different values is a subset of hAssgni(σ0 ).


C Loop Analysis
This subsection provides a more detailed explanation of the loop analysis and
post-state update processes introduced in Algorithm 1.
    Algorithm 2 illustrates the fundamental workflow for analyzing loops, which
is implemented through two pipelined plugin stages to decompose the logic to en-
hance maintainability. The first stage, LoopInfoPlugins, analyzes the symbolic
pre-state Σpre and the loop statement S to generate the basic loop information,
including the symbolic state at the loop entry Σentry and the corresponding
program point Pentry . The second stage, LoopAnalysisPlugins, performs a de-
tailed analysis based on the pre-state and the basic loop information, ultimately
producing the updated memory mapping Mloop after the loop, the set of post-
loop path conditions P Cloop , and the inferred invariants set Inv. To demonstrate
the capability of our extensible architecture, we have currently implemented spe-
cialized analysis plugins targeting common array processing idioms. Specifically,
our prototype includes support for reduction patterns (e.g., computing the
maximum or minimum value within an array segment) and linear search pat-
terns (e.g., locating the first index satisfying a specific predicate). Upon detect-
ing these idioms via structural matching, these plugins automatically synthesize
precise, high-level invariants—such as universal quantifiers for extremum prop-
        Array-Carrying Symbolic Execution for Function Contract Generation      27


 Algorithm 2: Loop Analysis
     Input: loop statement S, pre-path Ppre = (Σpre , Gpre )
     Output: memory map Mloop , post conditions P Cloop , loop invariants Inv
 1 (Σentry , Pentry ) ← LoopInfoPlugins(Σpre , S);
 2 (Mloop , P Cloop , Inv) ← LoopAnalysisPlugins(Σpre , Σentry , Pentry );
 3 return (Mloop , P Cloop , Inv);




erties or range constraints for search results—thereby enabling the verification
of functional correctness for these standard algorithmic constructs.
    After obtaining the post-loop program state, it is necessary to update the
address expressions and variable expressions within the symbolic states of all
successor paths. We only focus on variables originating from the loop entry Pentry
during the entire loop execution, and categorize the update cases as follows:
 – For a variable v, its corresponding symbolic value at the loop entry is located
   through its address Apre (v). If the variable is not modified within the loop,
   the original expression Mpre (Apre (v)) from the loop entry is reused as its
   current symbolic value, otherwise its symbolic value is replaced with the
   updated expression.
 – If the address expression a that points to the expression v has changed, the
   corresponding mapping in the previous memory map Mpre must be updated
   accordingly, producing a new mapping Mpost (a′ ) = v.
    The substitute function in Algorithm 3 represents this update process. For
variables and addresses that remain unchanged, their mappings are directly in-
herited into the post-state memory map Mpost . Additionally, the path conditions
contained in the post-condition set P Cloop are also updated and merged with
the pre-path conditions Gpre , yielding the final post-loop paths.
    With the mechanism for state updates established in Algorithm 3, we now
turn to the concrete implementation of the analysis pipeline that produces the
invariants and loop summaries. A collection of LoopInfoPlugins first performs
a lightweight symbolic exploration of the loop body to extract structural infor-
mation such as iteration bounds, induction variables, and memory access pat-
terns. This information is subsequently consumed by InvariantPlugins, one of
which invokes an external aﬀine invariant generation engine [28] based on Farkas’
Lemma to synthesize linear invariants and loop postconditions. These generated
invariants are injected into the symbolic post-state and simultaneously emitted
as ACSL loop invariants and postconditions. In combination, this architecture
enables the prototype to automatically infer and verify array-carrying contracts
for a range of realistic C loops without resorting to loop unrolling.
Next, we provide further technical details regarding the extensibility of our sym-
bolic expression system and the architectural design of the loop analyzer.
Extensible Aggregate Expressions. This framework is designed to be extensible.
Other properties of array segments can be captured by creating new aggregate
28       Weijie Lu et al.


 Algorithm 3: Post-State Update
     Input: pre-path Ppre = (Σpre , Gpre ), memory map Mloop , post conditions
            P Cloop , from point Pentry
     Output: post-path Ppost = (Σpost , Gpost )
 1 Decompose Σpre = (Mpre , Apre );
 2 Mpost ← ∅; Gpost ← ∅;
 3 foreach (a, v) ∈ Mloop do
 4    if from(a) = Pentry then
 5         a′ ← substitute(a, Ppre );
 6         v ′ ← substitute(v, Ppre );
 7         Mpost (a′ ) ← v ′ ;
 8    else
 9         Mpost (a) ← v;

10   foreach (a, v) ∈ Mpre such that a ∈
                                       / dom(Mloop ) do
11      Mpost (a) ← v;
12 foreach cond ∈ PCloop do
13    cond′ ← substitute(cond, Ppre );
14    Gpost ← Gpost ∧ cond′ ;
15   Σpost ← (Mpost , Apre ); Gpost ← Gpost ∧ Gpre ;
16   return Ppost = (Σpost , Gpost );



expression classes. For example, a SumOverRange class can represent the sum
of all elements in a segment habase , Li. This symbolic expression can then be
stored in M or used in path conditions, just like any other symbolic value. This
allows the LoopAnalyzer to generate powerful summaries of loops that compute
aggregate values over arrays.
Loop Analysis and Plugin Architecture. To address the complexity of loop han-
dling without unrolling, the LoopAnalyzer adopts a modular, plugin-based ar-
chitecture. The analysis proceeds in a two-stage pipeline.
First, a set of LoopInfoPlugins performs a preliminary symbolic execution of
the loop body to extract structural information, such as control flow patterns
and memory access deltas. These intermediate results are then consumed by the
InvariantPlugins, which are responsible for generating ACSL annotations and
constructing the symbolic post-state.
The InvariantPlugins are further categorized based on their interaction with
the execution path. Path-insensitive plugins derive universal properties that hold
across all execution traces, contributing global ACSL clauses. Path-sensitive plu-
gins, however, directly influence the shape of the symbolic configuration. To
manage potential conflicts, the framework employs a priority-based mechanism
to select a single ”principal handler” from the available path-sensitive plugins.
This principal plugin determines the exact number and condition of the post-
loop paths (e.g., distinguishing between a normal exit and an early break). Sub-
      Array-Carrying Symbolic Execution for Function Contract Generation       29

sequent plugins then traverse these established paths to attach specific symbolic
information.
Example: loop assigns. We illustrate this workflow with the LoopAssignsPlugin.
Leveraging the memory access patterns captured by the LoopInfoPlugins, and
assuming a decidable loop bound (e.g., i < n), this plugin computes a maximal
over-approximation of the memory footprint touched by the loop. For every
concrete or symbolic address accessed, the plugin emits the corresponding ACSL
assigns clause. Crucially, in the symbolic post-state, it maps these modified
locations to a symbolic Unknown value (>). This establishes a sound baseline;
plugins with higher precision invoked later in the pipeline can then refine the
state by overwriting these Unknown entries with specific symbolic formulas or
concrete values.


C.1 Examples of Invariant Generators
To clarify the role of invariant generators in our implementation, we summarize
three representative generators from our current plugin set and illustrate the
shape of the emitted ACSL clauses.
(1) Linear/Aﬀine Generator (StInGXPlugin). For loops whose guards can be
normalized into linear forms (e.g., i < n, i ≥ 0) and whose updates are aﬀine,
this generator invokes an aﬀine invariant engine based on Farkas-lemma reason-
ing [28, 41]. A typical output includes index-range invariants and aﬀine relations
over scalar variables. For example, for a loop for(i=0;i<n;i++){x=x+c;}, it
may emit clauses of the form:

       loop invariant 0 ≤ i ≤ n;         loop invariant x = x0 + c · i.

(2) Search-Pattern Generator (paradigmSearch). For single-break search loops,
the path-sensitive generator emits quantified conditions that distinguish nor-
mal exit and interrupt exit. For the pattern while(i<n){if(a[i]==t) break;
i++;}, representative generated facts are:

             loop invariant ∀ integer k; 0 ≤ k < i ⇒ a[k] 6= t,

and on the interrupt path:

                       ∃ integer k; 0 ≤ k ≤ i ∧ a[k] = t.

(3) Max/Min-Pattern Generator (paradigmMaxMin). For loops recognized as
extremum computation (e.g., if (m < a[i]) m = a[i];), the generator emits
template invariants expressing both boundness and witness existence:

 ∀ integer k; 0 ≤ k < i ⇒ a[k] ≤ m,         ∃ integer j; 0 ≤ j < i ∧ m = a[j].

This class of templates is especially useful for producing strong postconditions
of reduction-style loops.
30     Weijie Lu et al.

D Rationale for Excluding LLM-based Baselines

While Large Language Models (LLMs) have demonstrated impressive capabil-
ities in code and specification generation, we intentionally exclude them from
our evaluation baselines for three primary reasons.
    First, from a methodological perspective, our work focuses on advancing
the algorithmic capabilities of symbolic execution and constraint-based Invariant
Generation. These approaches provide deterministic, logically derivable guaran-
tees based on program semantics. In contrast, LLMs operate on a probabilistic
paradigm of token prediction. Comparing a rigorous deductive framework against
a stochastic model is methodologically inconsistent, as they serve different roles
in the software engineering landscape.
    Second, in the context of formal verification, soundness and traceability
are paramount. LLMs are prone to hallucinations—generating syntactically cor-
rect but semantically flawed ACSL specifications that may reference non-existent
variables or hallucinate convenient but false invariants. Our framework ensures
that every generated invariant is a strict logical consequence of the symbolic
execution path, providing a level of reliability that current statistical models
cannot guarantee.
    Finally, there is a significant risk of benchmark contamination. The stan-
dard verification suites used in this study (e.g., SV-Comp, SyGuS) are widely
available in open-source repositories and are highly likely to be included in the
training corpora of commercial LLMs. Comparing our solver-based approach,
which must synthesize invariants from scratch, against models that may have
effectively memorized the solutions would not constitute a fair assessment of al-
gorithmic reasoning capabilities. Therefore, we limit our evaluation to deductive
and constraint-based tools to ensure a rigorous and equitable comparison.
