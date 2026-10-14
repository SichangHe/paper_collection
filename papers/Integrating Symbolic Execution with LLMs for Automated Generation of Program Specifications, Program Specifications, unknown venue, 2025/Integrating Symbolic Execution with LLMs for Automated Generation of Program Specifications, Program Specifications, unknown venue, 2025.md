                                         Integrating Symbolic Execution with LLMs for Automated Generation of
                                         Program Specifications

                                         FANPENG YANG, Institute of Software, Chinese Academy of Sciences, UCAS, China
                                         XU MA, Institute of Software, Chinese Academy of Sciences, UCAS, China
                                         SHULING WANG∗ , Institute of Software, Chinese Academy of Sciences, UCAS, China
                                         XIONG XU, Institute of Software, Chinese Academy of Sciences, China
                                         QINXIANG CAO, Sch. of Computer Science & Sch. of Artificial Intelligence, Shanghai Jiao Tong University, China
                                         NAIJUN ZHAN, School of Computer Science, Peking University, China
arXiv:2506.09550v4 [cs.SE] 20 Jan 2026




                                         XIAOFENG LI, Beijing Institute of Control Engineering, China
                                         BIN GU, Beijing Institute of Control Engineering, China
                                         Automatically generating formal specifications including loop invariants, preconditions, and postconditions for legacy code is critical
                                         for program understanding, reuse and verification. However, the inherent complexity of control and data structures in programs makes
                                         this task particularly challenging. This paper presents a novel framework that integrates symbolic execution with large language
                                         models (LLMs) to automatically synthesize formally verified program specifications. Our method first employs symbolic execution
                                         to derive precise strongest postconditions for loop-free code segments. These symbolic execution results, along with automatically
                                         generated invariant templates, then guide the LLM to propose and iteratively refine loop invariants until a correct specification is
                                         obtained. The template-guided generation process robustly combines symbolic inference with LLM reasoning, significantly reducing
                                         hallucinations and syntactic errors by structurally constraining the LLM’s output space. Furthermore, our approach can produce
                                         strong specifications without relying on externally provided verification goals, enabled by the rich semantic context supplied by
                                         symbolic execution, overcoming a key limitation of prior goal-dependent tools. Extensive evaluation shows that our tool SESpec
                                         outperforms the existing state-of-the-art tools across numerical and data-structure benchmarks, demonstrating both high precision
                                         and broad applicability.

                                         CCS Concepts: • Theory of computation → Automated reasoning; • Software and its engineering → Software functional
                                         properties; • Computing methodologies → Artificial intelligence.

                                         Additional Key Words and Phrases: Program specification, Loop invariants, Symbolic execution, Large language models, Formal
                                         verification

                                         ∗ Corresponding author



                                         Authors’ Contact Information: Fanpeng Yang, Institute of Software, Chinese Academy of Sciences, UCAS, Beijing, China, yangfp@ios.ac.cn; Xu Ma,
                                         Institute of Software, Chinese Academy of Sciences, UCAS, Beijing, China, maxu@ios.ac.cn; Shuling Wang, Institute of Software, Chinese Academy
                                         of Sciences, UCAS, Beijing, China, wangsl@ios.ac.cn; Xiong Xu, Institute of Software, Chinese Academy of Sciences, Beijing, China, xux@ios.ac.cn;
                                         Qinxiang Cao, Sch. of Computer Science & Sch. of Artificial Intelligence, Shanghai Jiao Tong University, Shanghai, China, caoqinxiang@sjtu.edu.cn;
                                         Naijun Zhan, School of Computer Science, Peking University, Beijing, China, znj@ios.ac.cn; Xiaofeng Li, Beijing Institute of Control Engineering, Beijing,
                                         China, 1351127502@126.com; Bin Gu, Beijing Institute of Control Engineering, Beijing, China, gubin@ios.ac.cn.


                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not
                                         made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components
                                         of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on
                                         servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.
                                         © 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         Manuscript submitted to ACM


                                         Manuscript submitted to ACM                                                                                                                             1
2                                                                                                                  Yang et al.


ACM Reference Format:
Fanpeng Yang, Xu Ma, Shuling Wang, Xiong Xu, Qinxiang Cao, Naijun Zhan, Xiaofeng Li, and Bin Gu. 2026. Integrating Symbolic
Execution with LLMs for Automated Generation of Program Specifications. 1, 1 (January 2026), 27 pages. https://doi.org/10.1145/
nnnnnnn.nnnnnnn



1    Introduction
Across diverse software domains, ranging from general-purpose systems to safety-critical fields such as aerospace, a
vast amount of legacy code exists but lacks formal specifications defining its functionality. Automatically generating
program specifications is therefore essential for program comprehension, reuse, and formal verification against the
design requirements. Common forms of formal specifications include loop invariants, preconditions, and postconditions.
However, generating such specifications remains challenging due to complex control structures (e.g., nested branches,
loops, and function calls) and intricate data structures (e.g., structs, pointers, and inductive datatypes such as linked
lists).
    In this work, we focus on the problem of functional correctness specification. Our goal is to generate specifications
that fully characterize program behavior across all execution paths and relevant variables, rather than producing the
specifications sufficient only to satisfy a particular verification goal. We therefore view specification generation as
a form of functional summarization. While verification goals play an important role and can guide the generation
process, our approach is not limited to producing specifications tailored only to a given goal. Instead, we seek to infer
specifications that are as strong and informative as possible. As a principled first step, we ground the specification
generation process by leveraging precise, path-sensitive symbolic execution.
    Existing research on program specification generation has predominantly centered around loop invariants. Traditional
techniques reduce the problem of synthesizing loop invariants to constraint solving [9, 20], Craig interpolation [16–
18], recurrence analysis [3, 33], shape analysis [5], etc, however, these approaches suffer from restrictions in the
types of programs and invariants they can handle; moreover, their complexity often hinders scalable, automated
inference, requiring manual guidance. Dynamic methods, such as Daikon [15], synthesize invariants by monitoring test
executions against predefined templates, however, their effectiveness heavily relies on test coverage and quality, and
they provide no formal guarantees of correctness. Recent efforts combine machine learning with SMT solvers to improve
efficiency [6, 30, 37], but these methods remain largely confined to numeric programs. More recently, Large Language
Models (LLMs) have been applied to the specification generation of broader programs. While LLMs exhibit a strong
capability to understand program semantics, they often struggle to produce syntactically valid and semantically precise
formal specifications: hallucinations may lead to ill-formed assertions, and even syntactically correct specifications
tend to be incorrect or overly trivial, failing to faithfully capture program behavior.
    Several recent efforts have sought to address these challenges [21, 22, 32]. Among them, AutoSpec, the state-of-the-art
LLM-based approach, integrates static analysis, LLMs, and formal verification to decompose programs and generate
specifications bottom-up. However, its performance degrades for programs involving data structures such as structs
and linked lists. More fundamentally, while static analysis enables a divide-and-conquer decomposition of programs,
the specification generation of AutoSpec still largely relies on LLMs’ semantic understanding. As a result, static analysis
alone is insufficient to mitigate hallucinations at both the syntactic and semantic levels. Finally, like most existing
approach, AutoSpec is goal-directed, relying on predefined verification goals to synthesize specifications sufficient to
prove a given property. Such specifications are often narrowly tailored to a single objective and may over-approximate
Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                                 3


the behaviors outside that goal, thus failing to describe a program’s overall functional correctness, particularly when
explicit verification goals are absent.
  To overcome these limitations, we propose a novel method for generating program specifications even in the absence
of explicit verification goals, with the primary objective of capturing a program’s functional correctness rather than
merely proving a specific property. Our approach integrates symbolic execution, LLMs and formal verification to generate
formally verified specifications. This unified methodology handles diverse program constructs in a principled manner.
For loop-free code, symbolic execution precisely tracks path conditions and state transitions, directly constructing
strongest specifications that characterize exact functional behavior. For loops, candidate invariants are generated by
LLMs within localized contexts guided by precise symbolic execution results and equality-constraint based invariant
templates. These invariants are then iteratively refined using verification feedback and adaptive LLM strategies until
they are formally validated, and are sufficiently strong to support verification goals when such goals are provided. For
complex constructs, they are handled in a bottom-up fashion. Function calls and nested loops are managed using stacks
that enable compositional specification generation from inner to outer scopes. Non-recursive data structures, including
pointers, arrays, and structs, are modeled using a flattened memory representation that explicitly tracks separation
and aliasing, while recursive data structures are specified using inductive predicates. Together, these techniques are
designed to collectively infer maximally precise functional correctness specifications.
  In the actual implementation, we leverage QCP’s symbolic execution engine [36, 38] for its ability to precisely track
symbolic execution results at arbitrary execution points, combined with Frama-C [12] as our formal verifier due to its
automated verification capability and also ACSL-style assertions that are amenable to LLM processing. Our framework
tightly integrates QCP, Frama-C and LLMs, where each component’s strengths compensate for the others’ limitations.
  We performed a comprehensive and rigorous experimental evaluation to validate our approach. This includes an
ablation study confirming the contribution of each technical component, along with extensive benchmark assessments.
The results demonstrate the effectiveness and broad applicability of our approach across diverse tasks in invariant and
program specification generation. On numerical benchmarks, our method performs competitively with specialized
tools designed for numerical programs. Compared to recent LLM-based approaches such as AutoSpec and ACInv,
our approach demonstrates superior performance on numerical benchmarks. Furthermore, we introduced three new
benchmarks targeting distinct programs: more complex numerical programs, multi-layered structs and branches derived
from real aerospace applications, and recursive data structures with singly linked lists. Our method significantly
outperforms both AutoSpec and ACInv across these benchmarks, demonstrating the generalizability and robustness
of our method across a wide spectrum of programs. Additionally, we evaluated our method on loop invariant and
program specification generation under masked verification goals using the SyGuS and Frama-C benchmarks. The
results indicate that our approach continues to produce high-quality specifications with a small drop in performance,
while substantially outperforming the state-of-the-art tool AutoSpec under identical masking conditions. These findings
highlight the robustness of our approach even in the absence of explicit verification goal guidance.
  The rest of the paper is organized as follows: Sect. 2 introduces a motivating example and provides an overview of
our approach. Sect. 3 and Sect. 4 detail our core technical contributions on the generation of function specifications and
loop invariants. Sect. 6 evaluates our approach empirically. Sect. 7 discusses threats to validity. Finally, Sect. 8 presents
the related work, and Sect. 9 concludes the paper with directions for future work. The details on tool implementation,
LLM configurations, and experimental results are available at https://github.com/anon-hiktyq/TOSEM2026-SESpec .



                                                                                                   Manuscript submitted to ACM
4                                                                                                                  Yang et al.


2   A Motivating Example And Our Approach
Automating the generation of formal specifications for real-world C code remains challenging due to the prevalence
of complex language features such as loops, pointer manipulations and data structures. Consider the code fragment
shown in Fig. 1, which originates from the Sun Search system, a legacy embedded software component in the aerospace
domain. The code starts to define a struct CheckCal with three fields: an integer array pkv[10], an integer field len
representing the number of valid elements in the array, and an integer chksum storing the sum of the array’s elements.
Then, function foo invokes CheckCalFun on a CheckCal pointer pIp, with a given verification goal annotated by
/*@assert · · · */. The callee function CheckCalFun takes as input a CheckCal pointer pIp, computes the sum of the
len elements in the array pkv via a loop and then stores the result in the field chksum of pIp. This example exhibits
diverse features: complex data structures (structs, arrays and pointers), a loop with inductive operations over arrays,
and pointer-induced aliasing and side effects. In consequence, it faces the following challenges:
     • Loop reasoning: The summation loop for(; i<pIp->len; i++) requires determining whether the initial
       condition allows to enter the loop, and if the loop executes, establishing the invariants sufficient enough to
       specify the precise behavior of the loop, i.e. to relate the partial sum to the processed prefix of the array.
     • Structs and Pointers: The procedures involve operations such as accessing arrays, reading and writing to struct
       fields via pointers, making it essential to account for the resulting aliasing and side effects in their specifications.
       For instance, the specification for function CheckCalFun must guarantee memory safety for dereferencing
       pIp->pkv[i], precisely describe the write effect on pIp->chksum, and specify the frame property for other fields
       of pIp that remain unchanged.
     • Inductive predicates: Properties of arrays in loop such as aggregate sums are most naturally expressed with
       inductive predicates. Automatically writing correct forms of such predicates and furthermore verifying them
       remains a central challenge for programs involving recursive operations or data structures.
    As shown in Fig. 1, the code is annotated with the full ACSL specifications enclosed in /∗@... ∗ /, including
preconditions (beginning with requires), postconditions (beginning with ensures), loop invariants (beginning with
loop invariant), and verification goals (beginning with assert). Among these, the loop invariants, the default
preconditions and the postconditions are generated automatically by our tool SESpec, while the assert clause represents
verification goals provided a priori, and certain (non-default, line 4-5) preconditions reflect additional requirements
from the designers.
    Before presenting our method, we attempted to generate the specification for this example using GPT-4o, GPT-5
and AutoSpec respectively, given both the preconditions and the verification goal. The loop invariants they produced,
shown below, were all found to be incorrect:




Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                      5




                                           Fig. 1. Motivating Example


             loop invariant 0 <= i <= pIp->len;
             loop invariant chksum == \sum(0, i-1, \lambda integer k; pIp->pkv[k]);     (GPT-4o)


             loop invariant 0 <= i <= pIp->len;
             loop invariant chksum == \sum(integer k = 0; k < i; pIp->pkv[k]);
             loop assigns i, chksum;
             loop variant pIp->len - i;    (GPT-5)


             loop invariant 0 <= i <= pIp->len;
             loop invariant chksum == \sum(0, i-1, pIp->pkv);
             loop invariant \forall integer k; 0 <= k < i ==> chksum >= pIp->pkv[k];
             loop assigns i, chksum;    (AutoSpec)
                                                                                        Manuscript submitted to ACM
6                                                                                                                Yang et al.


    The failures highlight the common limitations of pure LLM-based approaches. First, LLMs often neglect whether a
loop is ever entered, so their generated invariants presume loop entry without establishing necessary preconditions
(e.g., pIp->len might be negative). Even when we explicitly prompted GPT-4o to "consider the case when the loop is
not entered", it still failed to generate the correct conditional invariant structure. Second, when reasoning about arrays,
LLMs introduce uninterpreted functions (e.g., a custom sum) that are undefined in the target verification framework
(such as Frama-C), causing verification failures.

2.1   Our Approach
Fig. 2 shows an overview of our approach. Without loss of generality, given a function and an optional verification
goal, the objective is to automatically generate loop invariants and function pre-/postconditions. If a verification goal is
provided, these specifications must be sufficient to prove it; otherwise, they should be strong enough to capture the
function’s core behavior.
    The entire process Function Specification Generation comprises four stages, as illustrated in Fig. 2. It begins
with Default Precondition Generation (marked in green), which produces the weakest preconditions ensuring
memory-safe execution (node 0 in Fig. 1). Our tool employs a flattened memory model that recursively decomposes
input data structures into atomic memory locations, generating validity and separation constraints to guarantee valid
memory accesses. Since other properties beyond memory safety are not required for symbolic execution, they are left
for users to specify as needed.
    Using this precondition, the tool initiates symbolic execution from the function’s entry point (node 1 in Fig. 1)
. When a function call is encountered (node 2 in Fig. 1), the current symbolic execution is paused and the tool call
Callee Specification Generation (mark in purple in Fig. 2). It recursively processes the callee function to generate its
specification (node 3 - node 6 in Fig. 1). Upon completion, the tool returns to the call site, incorporates the generated
pre-/postcondition of the callee and resumes symbolic execution of the caller. Throughout this process, a call stack is
maintained to support nested function calls. Functions are processed in a bottom-up order, and all generated function
specifications are stored for reuse across different calling contexts.
    When symbolic execution encounters a loop within the current function (node 5 in Fig. 1), it pauses and transfers
control to the Loop Invariant Generation (mark in blue in Fig. 2), the core component of our tool. The Loop Analysis
module is first invoked, taking as input the complete symbolic state at the loop entry, and identifies different types of
variables by analyzing the behavior of the loop body. In the presented example, the analysis produces the following
results: the unchanged variables pIp->len, pIp and pIp->pkv; the inductive variables i and chksum. Additionally,
the loop entry condition is established, i.e., i < pIp->len. Subsequently, the tool generates parameterized invariant
templates designed to capture various execution scenarios, such as whether the loop is entered, which variables remain
unchanged, which evolve inductively and how they behave. These templates are expressed as ACSL skeletons using
equality constraints to facilitate the synthesis of more precise invariants. Below we present part of the generated
templates for the motivation example (see Fig. 1 for the full set):

                        loop invariant (0 < \at(pIp, Pre)->len) ==> PLACE_HOLDER_for_i;
                        loop invariant (0 < \at(pIp, Pre)->len) ==> PLACE_HOLDER_for_chksum;
                        loop invariant pIp == \at(pIp, Pre);
    These skeletons provide specific PLACE_HOLDER tags for the LLM to populate (marked as the blue boxes in Fig. 1).
Guided by these structured templates and symbolic execution results, LLM produces loop invariants that precisely
Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                               7




                                             Fig. 2. Overview of Our Approach



characterize the behavior of different types of variables. This structural guidance significantly reduces hallucinations,
minimizes syntax errors, and narrows the overall search space. For instance, the generated invariants correctly in-
corporate the loop-entry condition (0 < \at(pIp, Pre)->len), a critical logical constraint that pure LLM-based
approaches consistently overlook.
  During the Loop Invariant Generation, a refinement procedure is iteratively invoked to assess the validity (able to
pass the formal verification) and the accuracy (sufficient to guarantee the given verification goal) of the generated loop
invariants. Depending on the feedback from the verifier, different refinement strategies are applied to guide the LLM
toward correct invariants.
  When symbolic execution of the callee is completed (node 6 in Fig. 1), the Function Postcondition Generation
(mark in red in Fig. 2) is triggered, the resulting symbolic states are used to synthesize a postcondition that summarizes
the callee’s functional behavior. Upon completion, the generated pre-/postconditions are returned to the call site and
reused as a functional summary in the caller (node 7 in Fig. 1), enabling symbolic execution of the caller to resume
without re-analyzing the callee’s internal control flow.
  If symbolic execution has not completed, it proceeds until the final postcondition of the function is generated.
Consequently, our approach synthesizes complete functional summaries for this example, including the weakest
preconditions (marked in green) that ensure memory safety, the loop invariants that capture loop-entry conditions,
inductive effects, and the identification of unchanged variables, and the postconditions sufficient to prove the given
                                                                                                 Manuscript submitted to ACM
8                                                                                                                      Yang et al.


verification goal. Notably, the same postcondition for CheckCalFun can still be generated even when the verification
goal is masked, demonstrating that our specification generation is not solely driven by the goal itself.



3     Pre-/Postcondition Specification Generation
This section first introduces the generation of strongest specifications for code segments without loops via symbolic
execution, and then presents the generation of general function specifications. Loop invariant generation is deferred to
next section.



3.1    Symbolic Execution and Strongest Pre-/Postconditions
We use a flattened memory model to explicitly track memory values and aliasing during symbolic execution. In this
model, each program point 𝑝 is associated with a scope consisting of a set of variables accessible at that point, and the
memory at 𝑝 is modeled as a collection of atomic memory locations L𝑝 reachable from these variables, each of which is
treated as a symbolic variable corresponding to a primitive memory unit.
    Within this model, the symbolic execution of statements maintains a symbolic state (𝑃𝐶𝜋 , 𝜎𝜋 ) for each execution
path 𝜋, where
      • 𝑃𝐶𝜋 denotes the path condition, i.e. a logical formula over initial symbolic values of L𝑝 and constants, that
        expresses the conditions required to traverse path 𝜋. 𝑃𝐶𝜋 is updated when a branch is taken along 𝜋.
      • 𝜎𝜋 denotes the symbolic store along path 𝜋, i.e. a logical formula specifying the symbolic values of L𝑝 . 𝜎𝜋 is
        updated when statements such as assignments or memory updates execute along 𝜋.
    The symbolic execution of a program is defined as a transformation over sets of symbolic states, accounting for
divergent control flow at branches. Formally, execution begins at the function entry point 𝑝 0 with an initial symbolic
state set containing a single element (𝑃𝐶 0, 𝜎0 ). Here, 𝜎0 assigns initial symbolic values to all variables in the logical
variable set L𝑝 , and 𝑃𝐶 0 is the path condition that encodes the precondition constraining those initial values. For
any program point 𝑝, the set of all reachable symbolic states is given by the collection of pairs {(𝑃𝐶𝜋𝑖 , 𝜎𝑝,𝜋𝑖 )}𝑚
                                                                                                                   𝑖=1 for
every path 𝜋𝑖 from the entry point 𝑝 0 to 𝑝. From this set, we derive a logical formula characterizing all feasible states
                Ô
at 𝑝, defined as 𝑚𝑖=1 (𝑃𝐶 𝜋𝑖 ∧ 𝜎𝑝,𝜋𝑖 ). At the entry point 𝑝 0 , this formula simplifies to the precondition 𝑃𝐶 0 ∧ 𝜎0 . For
any subsequent program point, the corresponding formula represents the postcondition that holds up to that point in
execution.
    We implement a symbolic execution procedure SEStart(F , Pre, 𝑝 start ). Given a code segment F and a precondition
Pre (a formula representing symbolic states) at a starting point 𝑝 start , the procedure executes symbolically from 𝑝 start ,
exploring the execution paths until it encounters a loop or a function call.
    Based on the above definition of symbolic execution, we can derive the strongest specifications for loop-free, straight-
line code. It consists of a weakest precondition and a strongest postcondition, together giving the most precise description
of the input/output behavior. In our approach, a default weakest precondition is automatically generated, requiring that
all accessible atomic memory locations at the entry point are initialized and contain valid symbolic values. Given a
precondition Pre at the entry point 𝑝 start , the strongest postcondition at 𝑝 end for F , denoted by SP(F , Pre, 𝑝 start, 𝑝 end ),
is the logical formula describing the disjunction of all symbolic states (defined as above) reachable at 𝑝 end from 𝑝 start
under Pre.

Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                                 9


3.2    Generation of Program Specifications
Without loss of generality, we describe the process of generating specifications of functions based on symbolic execution
by Algorithm 1. The algorithm takes as inputs a function F , a stack 𝑐𝑆 of callee functions with empty specifications,
a list 𝑎𝐹 of functions annotated with generated specifications. It performs symbolic execution throughout the entire
procedure, recursively invoking the generation of specifications for callee functions and of loop invariants as needed.
Upon termination, it produces an annotated version of F equipped with its specification, including the pre-/postcondition
and loop invariants.


 Algorithm 1: Function Specification Generation FuncSpec
   Input: F, callStack cS, annoFuncs aF
   Output: Function F with specification S
 1 if F ∈ aF then
 2     return
 3 cS.push( F);
 4 lS ← InitLoopStack( );
 5 P ← DefaultPre( F);
 6 𝑝 start ← 𝑝 0 ;
 7 SEStart( F, P, 𝑝 start );
 8 while 𝑝 ≠ 𝑝 −1 do
 9       𝑃 ← SP( F, P, 𝑝 start , 𝑝 );
10       𝑝 start ← 𝑝;
11       if 𝑝 = 𝑝 loop then
12              F ← LoopInvGen( F, 𝑝, lS, cS, aF, 𝑃, LLM);
13      if 𝑝 = 𝑝 callee then
14           Fcallee ← FuncSpec( Fcallee , cS, aF);
15      SEStart( F, P, 𝑝 start );
16 S ← SP( F, P, 𝑝 start , 𝑝 −1 ) ;
17 F ← ( F, S);
18 aF.append(cS.pop());
19 return F;




     Algorithm 1 is explained as follows. If F is already in 𝑎𝐹 , it returns directly (Lines 1-2). Otherwise, it is added to
the call stack 𝑐𝑆, which stores functions encountered during execution that lack specifications, and a loop stack 𝑙𝑠 is
initialized (Lines 3-4). They are used to handle nested function calls and loops respectively. Lines 5-6 initialize the
default precondition at the entry point 𝑝 0 (denoted by 𝑃) and sets the starting point for symbolic execution to be 𝑝 0
(denoted by 𝑝 start ). Function DefaultPre assigns initial symbolic values to all atomic memory locations reachable from
variables in scope at 𝑝 0 (typically the function’s parameters). Symbolic execution of F then starts from 𝑝 start with
precondition 𝑃 by invoking SEStart (Line 7), which will stop whenever a loop or a function call is encountered. If the
symbolic execution pauses at 𝑝, which is not the exit point of F (denoted by 𝑝 −1 ), the postcondition 𝑃 at 𝑝 is obtained
via SP based on the symbolic execution results, and 𝑝 start (the starting point for resuming symbolic execution in the
future) is reset to 𝑝 (Lines 9-10). If it is a loop (Lines 11-12), LoopInvGen is invoked to synthesize a loop invariant, with
𝑃 as the loop precondition and 𝑝 as the loop entry, and returns the updated F that annotates the loop with its invariant.
If it is a function call (Lines 13-14), FuncSpec is recursively invoked to obtain the specification of the callee function.
The use of call stacks enables a compositional approach to handle nested function calls by first deriving, then leveraging
                                                                                                   Manuscript submitted to ACM
10                                                                                                                     Yang et al.


these generated function specifications across different calling contexts. For both of the cases, the symbolic execution
will re-proceed from 𝑝 start with the corresponding annotations (Line 15). When the symbolic execution reaches the
function’s exit, the algorithm derives the postcondition S of F , adds the annotated F with its generated specifications
to aF, and finally returns (Lines 16-19).

4     Loop Invariant Generation
The general loop invariant generation problem can be defined as follows:

     Definition 1. Given a loop 𝑙 :while B do C of program P, a precondition 𝑃 that holds at entry 𝑙, and an (optional)
postcondition 𝑄, the loop invariant generation problem is to find a logical formula Inv that satisfies the following conditions:
      • Base: 𝑃 ⇒ Inv, i.e., the invariant Inv holds initially;
      • Preservation: {Inv ∧ 𝐵} 𝐶 {Inv}, i.e. if Inv holds at the start of a loop iteration and loop condition 𝐵 is true, executing
        loop body 𝐶 preserves Inv;
      • Termination: Inv ∧ ¬𝐵 ⇒ 𝑄, i.e. upon loop termination, 𝐵 turns false, Inv remains true and implies postcondition
        𝑄.

     Among these conditions, the postcondition serves as the verification target, whose objective is to synthesize
sufficiently strong invariants that imply it. Our invariant generation algorithm, presented below, is designed to produce
strong invariants even in the absence of postconditions. We achieve this through a combination of symbolic execution
and Large Language Models (LLMs), using equality-based invariant templates to precisely capture relationships between
symbolic states. The effectiveness of this approach is experimentally demonstrated in Section 6.5.


    Algorithm 2: Loop Invariant Generation LoopInvGen
   Input: F, 𝑝 loop , loopStack lS, callStack cS, annoFuncs aF, loop precondition 𝑃, LLM
   Output: Function F annotated with loop invariant I for loop Floop
   // Floop is loop body for loop at 𝑝 loop in F
 1 ThinkInNaturalLanguage( Floop , 𝐿𝐿𝑀 );
 2 lS.𝑝𝑢𝑠ℎ ( Floop );
 3 ( Floop , 𝑃 );
 4 F𝑙𝑜𝑜𝑝 , uV, nV ← LoopAnalysis( Floop , 𝑃, lS, cS, aF, LLM);
 5 lS.𝑝𝑜𝑝 ( );
 6 Assert(lS.𝑒𝑚𝑝𝑡 𝑦 ( ) );
 7 T ← LoopInvTemGen( Floop , 𝑃, uV, nV);
 8 I ← OuterLoopLLMCall( F, Floop , 𝑃, T, LLM);
 9 F ← ( F, I ) ;
10 while ¬Verify( F) do
11      F ← LoopInvRefinement( F, LLM);
12   return F;




4.1    Invariant Generation for Loops
Algorithm 2 presents a procedure for the invariant generation of a loop in F . Among the inputs, 𝑝 loop denotes the
entry point of the loop in F , 𝑃 is the precondition before 𝑝 loop obtained through previous symbolic execution, the large
language model (LLM) serves as the reasoning component. Other parameters remain as previously defined.
Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                               11


     First of all (Line 1), the original outermost Floop is sent to LLM for chain-of-thought in natural language, where
LLM were asked few questions for comprehensive understanding. Floop is pushed into the loop stack and analyzed by
LoopAnalysis, which performs the symbolic execution of the loop body to obtain the set of unchanged and non-inductive
variables and furthermore recursively handle all inner loops and annotates their invariants into 𝐹𝑙𝑜𝑜𝑝 , and after that, the
outermost loop Floop is popped from the stack. Third (Lines 6-8), the invariant for the outermost loop is generated: The
results obtained from LoopAnalysis serve as inputs to LoopInvTemGen, which generates a set of invariant templates
corresponding to the current loop. Based on these invariant templates, the invariant synthesis for the outermost loop
is performed by invoking the LLM-based procedure OuterLoopLLMGen. At the end (Lines 9-11), LoopInvRefinement
carries out verification-driven refinement, where the LLM interacts iteratively with the verifier to repair and strengthen
the generated invariants until they are verified.

 Algorithm 3: loop Analysis LoopAnalysis
   Input: F, precondition Pre, loopStack lS, callStack cS, annoFuncs aF, LLM
   Output: F, unchanged and noninductive variables uV, nV
 1 Funfolded ← UnfoldLoop( F𝑙𝑜𝑜𝑝 );
 2 𝑃 ← Pre;
 3 𝑝 start ← 𝑝 unfolded_0 ;
 4 SEStart( Funfolded , P, 𝑝 start );
 5 while 𝑝 ≠ 𝑝 unfolded_−1 do
 6       ... // Same to FuncSpec, reset new precondition and starting point
 7       if 𝑝 = 𝑝 nestedLoopEntry then
 8             lS.𝑝𝑢𝑠ℎ ( Fnested );
 9      if 𝑝 = 𝑝 nestedLoopExit then
10           Fnested ← lS.𝑝𝑜𝑝 ( );
11           F ← NestedLoopLLMCall( F, Fnested , LLM);
12      if 𝑝 = 𝑝 callee then
13           Fcallee ← FuncSpec( Fcallee , cS, aF);
14      SEStart( Funfolded , P, 𝑝 start );
15 ... // Same to FuncSpec, construct the final postcondition S
16 uV ← FetchUnchangeVars( S);
17 nV ← FetchNonInductiveVars( S);
18 return F, uV, nV ;




4.2    Loop Analysis
Algorithm 3 implements LoopAnalysis, which generates invariants for nested loops in Floop and identifies its unchanged
and non-inductive variables. It performs symbolic execution on a single-iteration unfolding Funfolded (Lines 1-4). The
key difference with FuncSpec lies in the handling of nested loops: whereas outer loops use symbolic execution-derived
loop preconditions and templates to guide LLM-based invariant generation (OuterLoopLLMCall), nested loops are
processed purely via LLM (NestedLoopLLMCall), which infers invariants directly from the code context without relying
on preconditions and templates, due to the lack of well-defined preconditions of nested loops. As shown in Algorithm 3,
nested loops are processed in a bottom-up manner using a loop stack lS, while function calls are handled consistently
with FuncSpec with the help of a call stack (Lines 7-13). Upon completion of the symbolic execution of the outermost
loop body, the final postcondition is derived, and all nested loops are annotated with the generated invariants; This
postcondition is then used to identify unchanged and non-inductive variables within the outermost loop (Lines 15-17).
                                                                                                  Manuscript submitted to ACM
12                                                                                                              Yang et al.


4.3    Template Generation
The LoopInvTemGen procedure takes as inputs the loop body, the loop precondition and the sets of unchanged and non-
inductive variables, and generates a set of invariant templates. These templates have parameters partially determined
by symbolic execution results, while the remaining undetermined parameters are completed using the subsequent LLM
synthesis method (i.e. OuterLoopLLMCall in Algorithm 2). Below we introduce five forms of invariant templates.
      • Unchanged variables: For any variable 𝑣 ∈ 𝑢𝑉 and any execution path 𝜋 𝑗 to the loop entry 𝑝, 𝑣 retains its
         symbolic value 𝜎𝑝,𝜋 𝑗 (𝑣) at the loop entry:

                                                        𝑃𝐶𝜋 𝑗 ⇒ 𝑣 = 𝜎𝑝,𝜋 𝑗 (𝑣)

      • Loop skip conditional property: For a path 𝜋 𝑗 to 𝑝 and a loop condition 𝐵, if 𝐵 for path 𝜋 𝑗 is false, the loop is
         skipped without altering variables:

                                            ¬(𝐵 ∧ (𝑃𝐶𝜋 𝑗 ∧ 𝜎p,𝜋j )) ⇒ 𝑣 = 𝜎𝑝,𝜋 𝑗 (𝑣)

      • Non-inductive variables: For a non-inductive variable 𝑣 (whose value is updated independently of its value from
         the previous iteration) and any path 𝜋 𝑗 to 𝑝:

                                        (𝐵 ∧ (𝑃𝐶𝜋 𝑗 ∧ 𝜎p,𝜋j )) ⇒ (𝑣 = 𝜎𝑝,𝜋 𝑗 (𝑣)) ∨ Φ(𝑣)

        where Φ(𝑣) is the inductive invariant to be synthesized.
      • Inductive variables: For an inductive variable 𝑣 (which is neither unchanged nor non-inductive) and any path 𝜋 𝑗
         to 𝑝:
                                                 (𝐵 ∧ (𝑃𝐶𝜋 𝑗 ∧ 𝜎p,𝜋j )) ⇒ Φ(𝑣)
      • Verification goals: In addition to variable-specific templates, we also introduce templates corresponding to each
        verification goal. For an verification goal 𝑔 and any path 𝜋 𝑗 to 𝑝:

                                                 (𝐵 ∧ (𝑃𝐶𝜋 𝑗 ∧ 𝜎p,𝜋j )) ⇒ Φ(𝑔)

     This template-driven approach is crucial for our loop invariant generation algorithm. By leveraging precise informa-
tion derived from symbolic execution, it simplifies the LLM’s task, shifting from full invariant generation from scratch
to completing invariant templates. It also offers structural guidance, helping the LLM produce formulas that conform to
the required ACSL logical syntax. More importantly, this approach ensures the generation of strong invariants that
capture all relevant variable behaviors across every execution path, thereby closely over-approximating the set of all
possible variable updates within the loop.

4.4    Loop Invariant Refinement
Loop invariants generated by the LLM are not always valid (able to pass formal verification) or sufficiently strong to
guarantee the verification goal. Also, our template-based approach improves the precision of invariant generation, but
also constrains the diversity of invariants. To alleviate these, we propose a fine-grained iterative refinement framework,
as shown in Algorithm 4, to combine verifier feedback with the LLM’s self-correction ability. This framework is
motivated by the observation that LLMs often produce loop invariants that are inaccurate, and that the templates, while
improving precision, reduce diversity.
     During the refinement process, depending on the verifier’s feedback, different strategies are applied: Syntax errors
are repaired directly, weak invariants (passing Base and Preservation but not Termination) are strengthened, invariants
Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                               13


    Algorithm 4: Iterative Refinement LoopInvRefinement
    Input: F with candidate loop invariants I0 , LLM
    Output: F ∗ with verified invariants I ∗
 1 I ← I0 ;
      −
 2 F ← F − 𝐼0
    // Run verifier and collect errors
 3 while Errors ← ¬Verify( F) do
 4      if reach iteration limit then
             // Find largest valid subset in I
 5           while I remains invalid do
 6               foreach 𝑒 ∈ Errors do
  7                   𝑖 ← associate loop invariant with e;
  8                   I ← Elimination( I, 𝑖 );

 9          F ← ( F − , I );
10          break;
11      if Errors = syntax error then
12           I ← RepairCallLLM( I );
13      else
14           guidance ← { } ;
15           if 𝐸𝑟𝑟𝑜𝑟𝑠 = verification goals fail then
                 // Only termination failed
16                guidance ← guidance ∪ strengthGuide( I );
17           else
18                foreach 𝑒 ∈ Errors do
19                    if 𝑒 = loop invariant error then
20                         𝑖 ← associate loop invariant with e;
21                         if e not base then
22                              guidance ← guidance ∪ WeakenGuide(𝑖 );
23                         if e not preservation then
24                              guidance ← guidance ∪ AdjustGuide(𝑖 );
25                    else
26                         guidance ← guidance ∪ RegenGuide(𝑖 );

27      I ← RefineCallLLM( I, guidance);
28      F ← ( F − , I );
29   return F



failing Base or Preservation but still implying the Postcondition are weakened or adjusted, and invariants failing all
checks are discarded and regenerated. At each step, the LLM is guided by a specialized prompt that encodes these
refinement strategies. If repeated attempts fail, a final elimination step removes consistently invalid invariants. The
refinement continues until a correct invariant is achieved or an iteration limit is reached. Similarly, the refinement of a
function specification can apply these strategies.

5     Implementation
5.1    Toolchain Integration and Data Flow
The implementation architecture and the underlying data flow between the components are illustrated in Fig. 3. The
process initiates with the C source code entering the Executor, which performs symbolic execution to generate SE Info
                                                                                                  Manuscript submitted to ACM
14                                                                                                                Yang et al.




                                        Fig. 3. The Implementation Design Framework



in the form of symbolic states (pairs of path conditions and symbolic stores). This symbolic information is then passed to
the Translator, which transforms the symbolic states in the syntax of the Executor into Natural Language descriptions
and the input syntax of the formal Verifier. Based on these translated representations, the Generator synthesizes
candidate specifications, which are subsequently sent to the Verifier for automated verification. If a specification is
successfully verified, it is translated back and fed into the Executor for further symbolic execution, allowing the system
to progressively cover the entire program. If verification fails, the resulting Error Info is translated into Natural Language
together with the original error context and fed back to the Generator for iterative refinement. This feedback-driven
loop tightly couples symbolic execution, specification synthesis, and formal verification, ensuring that the final output
specification is both semantically meaningful and formally sound.
     This architecture is instantiated using QCP [36, 38] as the symbolic execution engine and Frama-C [12] as the
formal verifier, a combination motivated by their complementary strengths. QCP serves as our foundational symbolic
executor because it generates Coq-verified postconditions and exposes symbolic execution results at arbitrary control
points in a logical form. Moreover, QCP provides strong support for programs manipulating complex data structures,
along with a rich library of verified inductive predicates and lemmas, which aligns well with our goal of generating
formally precise specifications. In contrast, widely used symbolic execution tools such as Klee [4] neither expose
intermediate symbolic states at arbitrary program locations nor represent execution states in a logic-oriented form
suitable for direct specification synthesis. However, QCP requires manual annotations for loop invariants and callee
function pre/postconditions, and may introduce unproven lemmas that require additional Coq proofs. To mitigate
these limitations, we leverage the Generator to automatically synthesize candidate invariants, and integrate Frama-C
as the Verifier to discharge proof obligations automatically. Frama-C’s ACSL assertion language provides an LLM-
friendly interface for specification generation, while its integration with SMT solvers enables scalable and automated
verification. Together, QCP and Frama-C form a synergistic execution–verification backbone that supports our iterative,
LLM-in-the-loop specification generation workflow.
Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                            15




                                               Fig. 4. The Prompt Design


  The Translator serves as a critical interoperability layer in our system, mediating the interaction between the
Executor (QCP), the Generator, and the Verifier (Frama-C). It establishes a bidirectional translation between ACSL and
the QCPL (QCP’s annotation language), enabling symbolic execution and formal verification to be tightly integrated in an
iterative loop. During the LoopInvGen phase, specifications in ACSL are translated into QCPL so that QCP can interpret
them consistently across loop and function boundaries. Conversely, symbolic execution results produced by QCP are
translated back into ACSL and discharged by Frama-C through automated verification. In this way, the Translator
enables continuous information flow between execution and verification. A key design choice of the Translator is that
the internal QCPL representation is never exposed to the LLM. Instead, symbolic execution results are transformed
into a combination of Natural Language explanations and ACSL skeletons before being passed to the Generator. This
transformation shields the model from low-level syntactic and semantic details specific to QCPL, reducing ambiguity
and preventing the model from confusing QCPL with ACSL during generation. At the same time, the use of ACSL
                                                                                               Manuscript submitted to ACM
16                                                                                                                Yang et al.


skeletons provides a pre-structured formal framework, allowing the LLM to focus on logical correctness rather than
grammatical well-formedness.

5.2    Prompt Designs

     Prompt Design for Loop Invariant Generation. Our prompt design strategy illustrated in Fig.4 is intricately mapped
to the multi-stage control flow of Algorithm 2 (LoopInvGen), ensuring that the LLM’s role dynamically adapts to each spe-
cific execution phase. The process initiates with the "Think In Natural Language" prompt (ThinkInNaturalLanguage, Line
1) to establish initial program comprehension, followed by the "Loop Invariant Generation" prompt (OuterLoopLLMCall,
Line 8), which constrains the LLM to fill precise, symbolic execution-derived Loop Invariant Template, providing a
structured skeletal format for ACSL annotations (LoopInvTemGen, Line 7). Crucially, the differential prompting logic is
applied across both stages: during the generation phase, prompts and placeholders for arrays or inductive predicates
are omitted when irrelevant to the program context; during the refinement procedure (LoopInvRefinement, Line 10),
the system dynamically selects appropriate instruction sets—such as repair, weakening, adjustment, strengthening, or
regeneration—thereby guiding the LLM to address the specific logical deficiencies identified by the verifier.

     Prompt Design for Inductive predication. For numerical programs, the specifications can be expressed using
arithmetic formulas in first-order logic, and our symbolic execution-guided LLM approach provides high accuracy
for inferring loop invariants. However, programs involving recursive data structures or inductive operations require
specifications expressed using inductive predicates or recursive functions. In these cases, LLMs often struggle not with
understanding program semantics, but with correctly adhering to the syntactic and semantic conventions of inductive
specifications in the target specification language, frequently producing assertions with syntax errors or uninterpreted
functions that lack formal definitions.
     To address this issue, in the prompt design (see Fig. 4), we provide two textbook-style illustrative examples in Frama-C
format, drawn from publicly available and well-established sources: one over arrays and one over single linked lists,
taken from the QCP and Frama-C repositories, respectively. These examples are not used to convey program-specific
properties, nor to bias the model toward particular benchmark structures. Instead, they serve solely to calibrate the
LLM to the proper syntactic forms and intended semantic usage of inductive predicates and functions, thereby reducing
hallucinations and malformed specifications.
     With this lightweight calibration, the LLM is able to correctly instantiate and synthesize inductive predicates when
required, while relying on symbolic execution to infer program-specific behavior. As a result, our approach can handle
programs manipulating single linked lists and arithmetic inductive computations (e.g., factorial), which remains beyond
the capabilities of [32]—all without resorting to training or large-scale external data.

6     Experiments
This section evaluates our approach for automatic specification generation based on symbolic execution (hereafter
referred to as SESpec).

6.1    Experimental Setup
     Benchmark. We evaluate our approach on multiple prominent and widely-adopted benchmarks, which are commonly
used by recent state-of-the-art tools. These include: SyGuS [2], collected by CODE2INV [30]; OOPSLA [14]; NLA,
collected by LIPuS [37]; the datasets from SV-COMP and Frama-C, collected by AutoSpec [32]. In addition, we
Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                                  17


constructed three new benchmarks to capture more program scenarios: The pIp set is extracted from an actual Sun
Search System used in aerospace control software, involving pointer and struct manipulations as well as complex
branching structures. We carefully adapt and reformulate pIp programs into a format acceptable to Frama-C and QCP,
thereby establishing a new dataset, which constitutes one of our contributions; the list-S set is derived from the LIG-
MM[19] benchmark and includes all singly linked list programs from SLING and SV-COMP; and the numer-S set is a
curated collection of additional programs, comprising 20 linear and 20 nonlinear loops primarily from CLAUSE2INV [4],
which exceed the difficulty of those in SyGuS and NLA.

  Verifier. All experiments are performed using Frama-C version 29.0 (Copper). We employ the WP plugin as the
verification backend, which enforces a 3-second timeout per query, uses Z3 as the primary SMT solver, and applies the
Typed memory model.

  Model. Our LLM selection for evaluating specification generation balanced model maturity, prevalence, and cutting-
edge performance: GPT-3.5-turbo is an earlier, foundational model that serves as an essential baseline; GPT-4o-mini,
a smaller, established model optimized for efficiency; GPT-4o, a widely adopted model for general code comprehension
and generation; and Claude-3.7-sonnet, a stronger hybrid model with advanced reasoning and code understanding,
representing the top tier of our tool’s capabilities. For all experiments, we use a fixed sampling temperature of 0.7 to
balance output diversity and stability.
  Below we evaluate our approach through four research questions:
      • RQ1: What Types of Programs can SESpec Manage?
      • RQ2: How does SESpec Perform on Program Specification Generation?
      • RQ3: Is SESpec Effective?
      • RQ4: What are the Advantages of SESpec Over Other Work?

6.2    RQ1: What Types of Programs can SESpec Manage?

                                           Table 1. Dataset Overview of Program Types


 Program Type                SyGus   OOPSLA      SV-COMP     NLA    numer-S    Frama-C   pIp   list-S    #Program     #Solved

 Linear Loop                  133      30            14        0       20          7      0      0         204         197
 Non Linear Loop               0       0             0        30       20          3      0      0          53          41
 Nested & Multi Loop           0       16            7         0        0          1      0      0          24          15
 Memory & Loop                 0       0             2         0        0         17     12     24          53          45
 Iteration Free                0       0             0         0        0         20     38      0          58          56
 External & Recursive Call     0       0             0         0        0          3      0      0           3           0

 #Program                     133     46            21       30       40         51      50    24          395
 #Solved                      133     40            16       25       34         39      44    23                      354
 Avg. LoC                      19     24            22       21       19         18      57    24


  Table 1 summarizes the 395 benchmark programs used in our evaluation. They encompass a diverse range of program
structures, including linear/non-linear/nested/multi-loops, function calls, along with data structures involving pointer
manipulations, and recursively-defined data types such as linked lists. Importantly, our benchmark suite includes both
                                                                                                     Manuscript submitted to ACM
18                                                                                                                Yang et al.


loop-only programs (indicated by Blue cells), requiring invariant generation, and programs requiring full specification
generation, i.e. loop invariant/pre/postcondition (indicated by Red cells).
     Overall, SESpec successfully verified 354 out of 395 programs (nearly 90%). The results demonstrate that our method
is applicable to a wide range of program types, especially generalizes to real-world industrial cases in the pIp dataset
selected from an actual Sun Search System. Our current approach does not yet cover recursive functions or programs
involving library functions and system calls, which we leave as future work.
     Furthermore, our evaluation reveals that lines of code (LOC) do not reliably reflect verification difficulty on these
benchmarks; instead, the primary challenge arises from the complexity of loop invariants. As shown in our results,
SESpec achieves a 97% success rate on Linear Loop and Iteration-Free programs. However, the success rate drops to
77% for Non-Linear Loop programs and to 63% for Nested & Multi-Loop programs. This decline is primarily due to the
increased difficulty of synthesizing invariants that capture complex numerical relationships, intricate data structure
properties, and interactions among nested or multi-level loop structures.

6.3    RQ2: How does SESpec Perform on Program Specification Generation?
We evaluate correctness through three metrics:
      • Syntax rate (Syn.): the percentage of generated specifications that are syntactically correct;
      • Validity rate (Val.): the percentage of generated specifications that are syntactically correct and valid, meaning
         that they can pass the formal verification of verifiers such as Frama-C. For example, the generated invariants for
         loops are valid if they satisfy both the Base and Preservation conditions;
      • Accuracy rate (Acc.): the percentage of generated specifications that are syntactically correct, valid, and also
         satisfy the verification goal. For example, the generated invariants for loops are accurate if they satisfy the Base,
         Preservation, and Termination conditions.
These metrics are assessed under different Pass@k settings, reflecting the system’s ability to attempt multiple generations
until the specifications pass all three metrics.
     Table 2 presents a comprehensive overview of our experimental results.
     The observed gaps among different evaluation metrics reveal important characteristics of both benchmark difficulty
and model capability. As benchmark complexity increases, the discrepancies between Syn., Val., and Acc. become more
pronounced. A similar trend is observed across models: weaker models tend to exhibit larger gaps between these metrics.
Notably, Val. does not trivially coincide with Syn. in our results, indicating that the generated specifications are not
simplistic invariants (e.g., true) or trivial properties that programs would satisfy by default. Instead, our approach aims
to capture complete program semantics and functional correctness, which naturally induces a meaningful distinction
between syntactic correctness and semantic validity.
     Importantly, our method demonstrates consistent effectiveness across different models and significantly narrows
the performance gap between stronger and weaker ones. For example, on benchmarks such as SV-COMP, NLA, and
numer-S, GPT-4o and Claude achieve identical performance at higher Pass@k levels (Pass@3 and Pass@5), highlighting
the capability of our approach to amplify the effectiveness of comparatively weaker models. Furthermore, the method
exhibits rapid convergence under Pass@k evaluation. Performance improvements from Pass@3 to Pass@5 are marginal
across several benchmarks, including NLA, numer-S, and pIp, suggesting high resource efficiency by reducing the
need for excessive evaluation cycles.
     The results also indicate comparatively lower accuracy on the OOPSLA, SV-COMP, and Frama-C benchmarks.
For OOPSLA and SV-COMP, this is primarily due to the presence of nested and multiple loops, where symbolic
Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                              19

                                  Table 2. Specification Generation Performance Overview


                                              Pass@1 (%)                  Pass@3 (%)                 Pass@5 (%)
 Benchmark              Model
                                          Syn.     Val.     Acc.     Syn.      Val.    Acc.     Syn.      Val.      Acc.
                    GPT-4o-mini     90.98 87.97 78.20 97.74 95.49 88.72 98.50 96.99 90.23
                    GPT-3.5-turbo   93.23 88.72 84.21 97.74 97.74 92.48 98.50 98.50 93.23
     SyGus
                       GPT-4o       98.50 98.50 93.98 100.00 99.25 99.25 100.00 100.00 100.00
                  Claude-3.7-sonnet 100.00 100.00 100.00 100.00 100.00 100.00 100.00 100.00 100.00
                    GPT-4o-mini          89.37     78.95    65.41    89.13    86.96    43.48 89.13 86.96           47.83
                    GPT-3.5-turbo        82.61     82.61    47.83    86.96    86.96    52.17 86.96 86.96           52.17
   OOPSLA
                       GPT-4o            91.30     69.57    60.87    95.65    76.09    73.91 100.00 82.61          76.08
                  Claude-3.7-sonnet      93.48     69.67    63.04    97.83    80.43    76.09 97.83 93.57           86.96
                    GPT-4o-mini     61.90 61.90             28.57 80.95 80.95          42.86 85.71 80.95           57.14
                    GPT-3.5-turbo   95.24 90.48             66.67 95.24 90.48          66.67 95.24 90.48           66.67
  SV-COMP
                       GPT-4o       90.48 90.48             52.38 100.00 100.00        71.43 100.00 100.00         76.19
                  Claude-3.7-sonnet 100.00 100.00           71.43 100.00 100.00        71.43 100.00 100.00         76.19
                    GPT-4o-mini          90.00     83.33    76.67    90.00    83.33    76.67    90.00    83.33     76.67
                    GPT-3.5-turbo        76.67     70.00    50.00    80.00    80.00    56.67    80.00    80.00     56.67
      NLA
                       GPT-4o            90.00     86.67    80.00    93.33    93.33    83.33    93.33    93.33     83.33
                  Claude-3.7-sonnet      93.33     93.33    83.33    93.33    93.33    83.33    93.33    93.33     83.33
                    GPT-4o-mini      95.00 90.00            72.50 100.00 95.00         75.00 100.00 95.00          75.00
                    GPT-3.5-turbo    92.50 85.00            62.50 95.00 90.00          65.00 95.00 92.50           67.50
   numer-S
                       GPT-4o       100.00 100.00           82.50 100.00 100.00        82.50 100.00 100.00         82.50
                  Claude-3.7-sonnet 100.00 97.50            85.00 100.00 100.00        85.00 100.00 100.00         85.00
                    GPT-4o-mini          54.90     49.02    47.06    62.75    50.98    49.02    64.71    50.98     49.02
                    GPT-3.5-turbo        77.08     60.42    52.08    83.33    62.50    54.17    83.33    62.50     54.17
   Frama-C
                       GPT-4o            82.35     72.55    66.67    86.27    76.47    70.59    86.27    78.43     72.55
                  Claude-3.7-sonnet      86.27     78.43    72.55    92.16    82.35    76.47    92.16    84.31     76.47
                    GPT-4o-mini     90.00          87.50    65.00 92.50       92.50    72.50 92.50       92.50     75.00
                    GPT-3.5-turbo   84.00          76.00    66.00 88.00       78.00    72.00 88.00       78.00     76.00
      pIp
                       GPT-4o       94.00          78.00    64.00 94.00       78.00    76.00 94.00       78.00     78.00
                  Claude-3.7-sonnet 100.00         88.00    82.00 100.00      90.00    88.00 100.00      92.00     88.00
                    GPT-4o-mini          62.50     41.67    33.33 75.00 45.83          41.67 79.17 54.17           45.83
                    GPT-3.5-turbo        70.83     20.83     8.33 79.17 25.00          16.67 79.17 25.00           16.67
     list-S
                       GPT-4o            70.83     62.50    54.17 87.50 83.33          75.00 91.67 87.50           79.17
                  Claude-3.7-sonnet      95.83     83.33    75.00 100.00 100.00        95.83 100.00 100.00         95.83


execution often fails to derive sufficiently strong preconditions. In addition, the absence of explicit loop conditions in
OOPSLA further complicates invariant inference. In the case of Frama-C, the difficulty mainly stems from complex loop
structures involving array manipulations, external function calls, and recursive behaviors, which remain challenging
for symbolic execution. Despite these obstacles, our method still achieves notable performance on these challenging
                                                                                                 Manuscript submitted to ACM
20                                                                                                                        Yang et al.


benchmarks. Moreover, the consistent improvements from Pass@1 to Pass@5 further underscore the robustness and
scalability of our approach in complex verification scenarios.

6.4    RQ3: Is SESpec Effective?
To assess the individual contributions of each component in our method, we conducted a detailed ablation study using
100 randomly chosen programs, consisting of 70 loop-related and 30 function-related cases. To ensure a fair comparison
under controlled computational budgets, we designed the experiment to maintain consistent LLM token usage across
all configurations. Specifically, we capped the refinement process at a maximum of 3 iterations.
     We compared four distinct configurations: The Only LLM (Pass@3) baseline uses the LLM for trivial invariant
generation without any external guidance. The LLM + SE (Pass@3) variant enhances the LLM with symbolic execution,
providing structural templates and program context. LLM + SE + REFINE (Pass@1) incorporates our refinement
module for iterative improvement. These configurations are designed to facilitate comparison with the incremental
approach employed in our work.




            Method              Syn. (%)   Val. (%)   Acc. (%)

            Only LLM            97.50       37.50      28.75
            LLM + SE            95.71       62.86      60.00
            LLM + SE + REFINE   95.71       95.71      87.21

            Only LLM            66.67       26.67      16.67
            LLM + SE            76.67       50.00      46.67
            LLM + SE + REFINE   93.33       86.67      86.67



Fig. 5. Ablation Study. Blue cells: loop invariant generation. Red   Fig. 6. The impact of masking verification goals for specification
cells: program specification generation.                             generation. Gray-shaded dots are results reproduced by us.


     The ablation results indicate that using the LLM alone yields high syntactic correctness, but exhibits notably low
validity and accuracy. Across both experimental settings, the integration of symbolic execution (SE) leads to substantial
improvements in validity and accuracy—with an average increase of 30%—while only slightly reducing syntactic
correctness in the first setting (less than 2%). The incorporation of the refinement step (REFINE) further elevates
performance, achieving perfect scores across all metrics in the first setting and delivering an average improvement of
20% in validity and accuracy in the second.
     Overall, the ablation study confirms that each component contributes positively to the final outcome, with symbolic
execution and refinement yielding the most significant gains.

6.5    RQ4: What are the Advantages of SESpec Over Other Work?
Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                                  21

    Table 3. Specification Generation Performance Comparison. The Gray-shaded cells represent results reproduced by us.


  Method                        SyGus    OOPSLA      SV-COMP        NLA      numer-S       Frama-C        pIp       list-S

  CODE2INV                      54.9%       —             —           —          —             —           —          —
  HOLA                            —       93.5%           —           —          —             —           —          —
  CLN2INV                       93.2%       —             —           —          —             —           —          —
  LiPus                         93.2%       —             —         83.3%        —             —           —          —
  CLAUSE2INV                    99.2%       —             —         93.3%        —             —           —          —

  AutoSpec-3.5                  85.7%     82.6%         76.2%       70.0%      75.0%         60.8%       14.0%       0.0%
  AutoSpec-4o                   86.5%     71.7%         66.7%       70.0%      72.5%         68.6%       22.0%       0.0%
  AutoSpec-Claude-3.7           88.7%     80.4%         66.7%       60.0%      55.0%         74.5%       4.0%        0.0%
  ACInv-3.5                     71.4%     45.7%         42.9%         —          —           34.5%         —          —
  ACInv-4o                      79.9%     76.1%         76.2%         —          —           48.3%         —          —
  SESpec-3.5                    93.2%     52.2%         66.7%       56.7%      67.5%         51.0%       76.0%      16.7%
  SESpec-4o                     100.0%    76.1%         76.2%       83.3%      82.5%         72.6%       78.0%      79.2%
  SESpec-Claude-3.7             100.0%    87.0%         76.2%       83.3%      85.0%         76.5%       88.0%     95.83%




  Overall Comparison With LLM Approaches. Table 3 compares three representative LLM-based approaches:
AutoSpec, ACInv, and our tool SESpec. First, on the four datasets originally introduced by AutoSpec, our method con-
sistently outperforms ACInv across both GPT-3.5-turbo and GPT-4o. Moreover, the performance gains from upgrading
the underlying model are similar for ACInv and SESpec, highlighting that our workflow is comparably scalable yet
significantly more effective.
  In contrast, AutoSpec exhibits negligible improvement when transitioning from GPT-3.5-turbo to GPT-4o. This
stagnation stems from AutoSpec’s reliance on few-shot prompting combined with exhaustive sampling and verification-
based filtering. By prioritizing the generation of massive candidate pools rather than leveraging the full reasoning
potential of LLMs, AutoSpec hits a performance ceiling that stronger models cannot easily break. Consequently, our
reproduction of AutoSpec-4o remains at a similar level to the reported AutoSpec-3.5 results.
  Conversely, SESpec demonstrates steady and reliable gains as the underlying model improves. Our workflow demands
complex reasoning capabilities—specifically, simulating execution via a "Thinking In Natural Language" procedure and
iteratively repairing, strengthening, or weakening invariants based on verification feedback. This complexity exceeds
the instruction-following limits of GPT-3.5-turbo, resulting in less competitive performance on the weaker model. The
use of symbolic execution reduces this complexity by providing structured symbolic constraints, enabling superior
models like GPT-4o to achieve significant performance gains through deeper reasoning, eventually surpassing AutoSpec
across almost all benchmarks.
  This distinction is further illustrated by the performance on complex datasets like pIp. We observe that AutoSpec-
Claude-3.7 performs poorly despite the model’s advanced capabilities. Although Claude possesses superior mathematical
logic and coding abilities, it often struggles to generate correct ACSL syntax, leading to high failure rates. SESpec
                                                                                                   Manuscript submitted to ACM
22                                                                                                            Yang et al.


mitigates this issue by utilizing an ACSL skeleton to represent symbolic states, which structurally constrains the output
to avoid syntactic errors while fully leveraging the model’s logical reasoning strengths.
     Finally, we emphasize the difference in experimental setup. SESpec operates primarily in a zero-shot setting. In
contrast, AutoSpec relies on handcrafted few-shot examples as an indispensable part of its workflow. This highlights
the stronger generalization ability of SESpec: it achieves competitive or superior performance through autonomous
reasoning rather than depending on few-shot engineering.

     Detailed Results over Benchmarks on SESpec. Our method demonstrates consistent advantages over SMT-based
approaches (combined with machine learning) across several major numerical invariant benchmarks. On the SyGuS
dataset introduced by CODE2INV, our approach achieves a 100% success rate, outperforming the state-of-the-art
SMT-based tool CLAUSE2INV. For the nonlinear numerical NLA benchmark proposed by LiPus, our method matches
the success rate of LiPus and remains competitive, although it trails CLAUSE2INV by 10%. Furthermore, on the OOPSLA
dataset, proposed by the abductive inference-based invariant generator HOLA and designed for numerical loops without
explicit conditions, including nested and multiple loops, our method achieves a success rate of 87% on this challenging
case. However, these existing approaches based on SMT solvers are specialized for numerical loops.
     By integrating symbolic execution, our method demonstrates significant advantages over purely neural baselines
like the state-of-the-art AutoSpec and ACInv on numerical benchmarks. It achieves a 15% higher accuracy on SyGuS
and noticeably outperforms them on NLA and numer-S. On the OOPSLA benchmark, our approach achieves a success
rate comparable to ACInv and is only marginally lower than AutoSpec (With the Claude-3.7 model, we achieve 5%
higher rate). All three methods perform equally on SV-COMP benchmark. We speculate that this is due to the dataset’s
non-uniform distribution of problem difficulty, with challenging nested and multi-loops that remain unsolved by
all existing approaches. The above results demonstrate how symbolic guidance enables more precise specification
generation that pure neural methods cannot achieve.
     On the Frama-C benchmark for functional program verification, our method noticeably outperforms AutoSpec by
incorporating support for inductive predicates, enabling more expressive specification inference. When evaluated on
the pIp benchmark from the real-world Sun Search system, which features extensive use of structures and pointer
operations, our approach achieves an average 50% higher success rate compared to AutoSpec, thanks to the combination
of a flattened memory model and precise symbolic execution. Furthermore, our method attains high performance on
the list-S benchmark comprising linked lists, a capability absent in AutoSpec due to its lack of support for inductive
data types. These results demonstrate that our approach offers robust and generalizable support for both closed struct
types (via flattened unfolding) and inductive data structures (through inductive predicates).

     Specification Generation without Verification Goals. To demonstrate the capability of our tool SESpec on
specification generation in the absence of verification goals, we conducted experiments on syGus and Frama-C by
deliberately masking the goals and compared with AutoSpec. We performed GPT-4o with Pass@1 experiments on
SESpec and chose their own configuration on AutoSpec [32], respectively, to compare the accuracy of the two and to
analyze the impact of masking verification goals. As shown in Figure 6, SESpec maintains relatively stable accuracy
across the two settings, decreasing from 93.98% to 80.45%. Similarly, in the Frama-C benchmark, the accuracy only
drops slightly from 70.83% to 64.71%, further demonstrating the robustness of SESpec without verification goal. By
contrast, AutoSpec experiences a drastic decline in accuracy: On the syGus benchmark, accuracy falls from 85.71% to
57.89%, while on Frama-C it decreases sharply from 60.78% to just 29.41%.
Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                              23


    The performance drop of SESpec is primarily due to the refinement process, which performs targeted optimization
with respect to the specific verification goal. A key finding is that if the improvement from refinement is disregarded in
our approach, the performance under the two settings is still nearly identical. This demonstrates that our symbolic
execution-guided reasoning ensures high-quality specification generation even in the absence of specific verification
targets.


7    Threats to Validity


    Data Leakage. A major threat to the validity of specification generation approaches lies in unintended bias, data
leakage, and overfitting to evaluation benchmarks, especially in the context of program verification where truly domain-
specific data are scarce. Training-based or retrieval-augmented methods are particularly vulnerable to these issues, as
benchmark adjacent corpora, curated examples, or synthetically generated programs may implicitly encode benchmark
specific patterns, leading to over-optimization for a given dataset rather than genuine semantic understanding.
    We mitigate these threats by deliberately avoiding all forms of external supervision and dataset dependency. Our
approach does not involve model fine-tuning, retrieval from large-scale external corpora, synthesized datasets, or
few-shot prompting. Consequently, the model cannot adapt its behavior to any specific benchmark distribution or
overfit to particular datasets. Instead, we exclusively rely on the in-context reasoning capabilities of pretrained large
language models, guided by symbolic execution results derived solely from the target program. These symbolic states
provide precise semantic context without introducing any external information about benchmark structure or expected
specifications.
    As a result, the generated specifications are grounded purely in the semantics of the analyzed program rather
than in prior exposure to benchmark-related data. This design substantially strengthens the internal validity of our
evaluation by minimizing bias, preventing data leakage, and avoiding overfitting to any dataset, ensuring that observed
performance gains stem from the proposed symbolic execution–guided reasoning process rather than dataset-specific
artifacts.

    Benchmark and Baseline Selection. To ensure a fair and comprehensive evaluation, we selected benchmarks that
align with the current state-of-the-art in program verification. Our evaluation includes benchmarks used in the works
we compare against, specifically the AutoSpec benchmark and two external datasets from Lipus and Clause2Inv. These
benchmarks are representative of the field’s development, featuring comparable levels of loop complexity and lines of
code (LoC). To further stress-test our approach, we introduced an original benchmark pIp that feature significantly
more complex data structures and intricate control-flow patterns than existing sets.
    Regarding the exclusion of SpecGen[22] from our direct comparison, we note two primary reasons: first, a fundamental
architectural mismatch exists as SpecGen targets different programming and specification languages (Java/JML in
SpecGen vs. C/ACSL in our work), creating translation barriers that make direct, automated comparison infeasible.
Second, SpecGen was evaluated on a custom dataset rather than the established AutoSpec benchmark used in our study
and other baseline works. By grounding our evaluation in widely recognized datasets while adding more challenging
cases, we ensure that our results are both comparable to previous research and indicative of performance on complex
softwares.


8    Related Work
                                                                                                 Manuscript submitted to ACM
24                                                                                                               Yang et al.


     Traditional approach. Traditional techniques for program specification and invariant inference can be broadly
categorized into dynamic and static methods. Dynamic approaches infer specifications and invariants by analyzing
runtime data collected during test execution. Daikon [15] executes test cases to gather program traces and produces
a set of candidate invariants based on a predefined library of templates, which are subsequently filtered using the
observed data. Sharma et al. [29] employ a similar approach to generate candidate invariants, but additionally verify
their soundness using SMT solvers. In contrast, DIG [24] bypasses template-based filtering and instead directly infers
invariants from execution traces by integrating techniques from equation solving, polyhedra construction, and theorem
proving. Despite their practicality, dynamic methods are highly dependent on the coverage and quality of the test suites.
     Static methods eliminate the dependency on test cases and explore a variety of techniques, including constraint
solving [9, 20], abstract interpretation [10] [11], abductive inference [14], Craig interpolation [16–18], recurrence
analysis [13, 27, 28], shape analysis, and other methods [8] [23]. Colón et al. [9] present the first complete invariant
generation method based on Farkas’ lemma and solves the non-linear invariant constraints via quantifier elimination,
which is of double exponential time complexity. Some heuristics are proposed to promote the efficiency of solving the
constraints [20]. Cousot et al. [11] utilize convex polyhedra along with transformations and widening operations to
discover linear invariants based on abstract interpretation. However, due to the intrinsic nature of abstract interpretation,
the efficiency of the analysis heavily depends on the choice of abstract domains, and moreover, the approach offers
no theoretical guarantee on the accuracy of the generated invariants due to the precision loss in abstraction. Lin et
al. [18] synthesize inductive invariants using Craig interpolants derived from reachability analyses, and nonlinear Craig
interpolant generation was first studied in [17]. The recurrence-based methods [13, 27, 28] derive recurrence relations
from loops and solve these recurrences to obtain closed-form solutions as invariants. A key limitation of this approach,
however, is restricted to the cases where the recurrences admit closed-form solutions or satisfy some strong conditions.
Wu et al. [35] solve the strong and weak invariant synthesis problems of polynomial programs by combining invariant
templates, semidefinite programming and constraint solving techniques. However, these traditional static methods are
often not scalable and may require manual intervention. In contrast to these techniques, which are powerful yet often
specialized for programs adhering to specific forms (e.g., certain types of loops or invariants), our approach leverages
LLMs to achieve greater generality. In particular, some of these works focus primarily on theoretical challenges, and as
a result, often exhibit limited efficiency and are difficult to apply directly to invariant generation at the program scale.


     Machine learning and SMT-based approach. Machine learning techniques and Large Language Models have been
increasingly used for synthesizing loop invariants. Recent advancements [7, 26, 30, 34, 37], particularly in deep learning
and reinforcement learning, have spurred new approaches for invariant and specification generation. CODE2INV [30],
based on Counterexample-Guided Inductive Synthesis (CEGIS) [1], utilizes graph neural networks to learn neural
representations of program structures. While CODE2INV employs a reinforcement learning approach, it often faces
challenges with limited performance and sparse rewards. To address these issues, LIPuS [37] establishes a clearer division
of labor between the capabilities of RL and SMT solvers and introduces a novel two-dimensional reward mechanism
to alleviate the sparse reward problem of CODE2INV. Clause2Inv [6] refines the guess-and-check paradigm into a
generate-combine-check framework, employing an LLM to generate candidate clauses and a counterexample-driven
combiner to synthesize them into loop invariants. However, these approaches are mostly confined to numeric programs
and do not constitute an end-to-end invariant generation framework; instead, they produce invariants in SMT format.
Moreover, they are goal-directed, i.e., they rely on pre-given verification goals to generate accurate specifications.

Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                                                       25


Empirical comparisons on numeric benchmarks show that our tool achieves competitive performance, and in some
cases even outperforms these methods.

     LLM-based approach. Pei et al. [25] demonstrates that fine-tuning pre-trained LLMs on code can effectively predict
program invariants, with better performance than Daikon if the set of available tests is limited. However, same as Daikon,
it has no formal guarantee for the validity of the generated invariants through formal verification. SpecGen [22] is a Java-
oriented tool that employs a two-phase process to generate specifications: it first leverages LLM to produce invariant
candidates, and then applies mutation operators with a weighted heuristic strategy to generate verifiable specifications
when initial generation fails. Preguss [31] adopts a divide-and-conquer strategy that leverages potential runtime
error assertions from static analysis to guide LLM-based synthesis of interprocedural specifications. AutoSpec [32]
decomposes programs into smaller parts and uses carefully designed prompts including few-shot examples to guide
an LLM in generating specifications, which are then verified using Frama-C. ACInv [21] utilizes static analysis to
extract essential information about loops and data structures, which is then embedded into prompts for an LLM to
generate candidate invariants and abstract predicates. We provide a detailed comparison in Section 6 with ACInv [21]
and AutoSpec [32], both of which target C programs.

9    Conclusion
In this paper, we introduce a novel end-to-end framework for the automatic generation of C program specifications,
including loop invariants and pre-/postconditions, by integrating symbolic execution, large language models (LLMs),
and formal verification. Experimental results across diverse benchmarks demonstrate that our approach significantly
outperforms existing methods in both invariant and functional specification generation. Furthermore, with the help of
flattened memory model and inductive predicates, our tool supports programs with complex data structures including
structs, pointers and recursively defined types (e.g., single linked lists), as well as inductive operations. Notably, even
without explicit verification goals, our method maintains competitive accuracy and consistently surpasses prior tools.
     For future work, we aim to extend the framework to more complex recursive data structures and recursive functions,
and to strengthen invariant generation for challenging cases such as nested loops, where correlations among multiple
induction variables arise. In particular, we plan to enhance the current LLM-based approach by integrating it with
symbolic sampling and targeted training strategies to improve precision of the invariant generation of nested loops.

10     Data Availability
All datasets, implementation code, experimental results, and supplementary materials including the appendix related to
this work are publicly available at https://github.com/anon-hiktyq/TOSEM2026-SESpec.

References
[1] A. Abate, C. David, P. Kesseli, D. Kroening, and E. Polgreen. 2018. Counterexample Guided Inductive Synthesis Modulo Theories. In Computer Aided
    Verification. Springer International Publishing, 270–288.
[2] R. Alur, D. Fisman, S. Padhi, R. Singh, and A. Udupa. 2019. Sygus-comp 2018: Results and analysis. CoRR abs/1904.07146 (2019). arXiv:1904.07146
[3] Dirk Beyer, Matthias Kettl, and Thomas Lemberger. 2024. Decomposing software verification using distributed summary synthesis. Proceedings of
    the ACM on Software Engineering 1, FSE (2024), 1307–1329.
[4] Cristian Cadar, Daniel Dunbar, and Dawson R. Engler. 2008. KLEE: Unassisted and Automatic Generation of High-Coverage Tests for Complex
    Systems Programs. In 8th USENIX Symposium on Operating Systems Design and Implementation (OSDI). USENIX Association, 209–224.
[5] Cristiano Calcagno, Dino Distefano, Peter O’Hearn, and Hongseok Yang. 2009. Compositional shape analysis by means of bi-abduction. In Proceedings
    of the 36th annual ACM SIGPLAN-SIGACT symposium on Principles of programming languages. 289–300.
                                                                                                                      Manuscript submitted to ACM
26                                                                                                                                         Yang et al.


 [6] Weining Cao, Guangyuan Wu, Tangzhi Xu, Yuan Yao, Hengfeng Wei, Taolue Chen, and Xiaoxing Ma. 2025. Clause2Inv: A Generate-Combine-Check
     Framework for Loop Invariant Inference. Proc. ACM Softw. Eng. 2, ISSTA (2025), 1009–1030.
 [7] S. Chakraborty, S. Lahiri, S. Fakhoury, A. Lal, M. Musuvathi, A. Rastogi, A. Senthilnathan, R. Sharma, and N. Swamy. 2023. Ranking LLM-Generated
     Loop Invariants for Program Verification. In Findings of the Association for Computational Linguistics: EMNLP 2023. Association for Computational
     Linguistics, 9164–9175. https://aclanthology.org/2023.findings-emnlp.614/
 [8] M. Chalupa and J. Strejček. 2021. Backward Symbolic Execution with Loop Folding. In Static Analysis. Springer International Publishing, 49–76.
 [9] Michael Colón, Sriram Sankaranarayanan, and Henny Sipma. 2003. Linear Invariant Generation Using Non-linear Constraint Solving. In Computer
     Aided Verification CAV (Lecture Notes in Computer Science, Vol. 2725). Springer, 420–432.
[10] P. Cousot and R. Cousot. 1977. Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of
     fixpoints. In Proceedings of the 4th ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL ’77). Association for Computing
     Machinery, 238–252.
[11] P. Cousot and N. Halbwachs. 1978. Automatic discovery of linear restraints among variables of a program. In Proceedings of the 5th ACM
     SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL ’78). Association for Computing Machinery, 84–96.
[12] P. Cuoq, F. Kirchner, N. Kosmatov, V. Prevosto, J. Signoles, and B. Yakobowski. 2012. Frama-C: A software analysis perspective. In International
     conference on software engineering and formal methods. Springer, 233–247.
[13] John Cyphert and Zachary Kincaid. 2024. Solvable Polynomial Ideals: The Ideal Reflection for Program Analysis. Proc. ACM Program. Lang. 8, POPL
     (2024), 724–752.
[14] I. Dillig, T. Dillig, B. Li, and K. McMillan. 2013. Inductive invariant generation via abductive inference. In Proceedings of the 2013 ACM SIGPLAN
     International Conference on Object Oriented Programming Systems Languages & Applications (OOPSLA ’13). Association for Computing Machinery,
     443–456.
[15] M. D. Ernst, J. H. Perkins, P. J. Guo, S. McCamant, C. Pacheco, M. S. Tschantz, and C. Xiao. 2007. The Daikon system for dynamic detection of likely
     invariants. Sci. Comput. Program. 69, 1 (2007), 35–45. Special issue on Experimental Software and Toolkits.
[16] Ting Gan, Liyun Dai, Bican Xia, Naijun Zhan, Deepak Kapur, and Mingshuai Chen. 2016. Interpolant Synthesis for Quadratic Polynomial Inequalities
     and Combination with EUF. In Automated Reasoning - 8th International Joint Conference, IJCAR (Lecture Notes in Computer Science, Vol. 9706).
     Springer, 195–212.
[17] T. Gan, B. Xia, B. Xue, N. Zhan, and L. Dai. 2020. Nonlinear Craig Interpolant Generation. In Computer Aided Verification. Springer International
     Publishing, 415–438.
[18] S.-W. Lin, J. Sun, H. Xiao, Y. Liu, D. Sanán, and H. Hansen. 2017. FiB: Squeezing loop invariants by interpolation between forward/backward
     predicate transformers. In 2017 32nd IEEE/ACM International Conference on Automated Software Engineering (ASE). 793–803.
[19] Chang Liu, Xiwei Wu, Yuan Feng, Qinxiang Cao, and Junchi Yan. 2024. Towards general loop invariant generation: a benchmark of programs with
     memory manipulation. Advances in Neural Information Processing Systems 37 (2024), 129120–129145.
[20] Hongming Liu, Hongfei Fu, Zhiyong Yu, Jiaxin Song, and Guoqiang Li. 2022. Scalable linear invariant generation with Farkas’ lemma. Proc. ACM
     Program. Lang. 6, OOPSLA2 (2022), 204–232.
[21] R. Liu, G. Li, M. Chen, L.-I. Wu, and J. Ke. 2024. Enhancing Automated Loop Invariant Generation for Complex Programs with Large Language
     Models. CoRR abs/2412.10483 (2024). arXiv:2412.10483 https://doi.org/10.48550/arXiv.2412.10483
[22] L. Ma, S. Liu, Y. Li, X. Xie, and L. Bu. 2025. SpecGen: Automated Generation of Formal Program Specifications via Large Language Models. In 2025
     IEEE/ACM 47th International Conference on Software Engineering (ICSE). IEEE Computer Society, 666–666.
[23] T. Nguyen, M. B. Dwyer, and W. Visser. 2017. SymInfer: inferring program invariants using symbolic states. In Proceedings of the 32nd IEEE/ACM
     International Conference on Automated Software Engineering (ASE ’17). IEEE Press, 804–814.
[24] T. Nguyen, D. Kapur, W. Weimer, and S. Forrest. 2014. DIG: A Dynamic Invariant Generator for Polynomial and Array Invariants. ACM Trans. Softw.
     Eng. Methodol. 23, 4, Article 30 (2014), 30 pages.
[25] K. Pei, D. Bieber, K. Shi, C. Sutton, and P. Yin. 2023. Can large language models reason about program invariants?. In Proceedings of the 40th
     International Conference on Machine Learning (ICML’23). JMLR.org, Article 1144, 25 pages.
[26] M. A. A. Pirzada, G. Reger, A. Bhayat, and L. C. Cordeiro. 2024. LLM-Generated Invariants for Bounded Model Checking Without Loop Unrolling. In
     Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (ASE ’24). Association for Computing Machinery,
     1395–1407.
[27] Enric Rodríguez-Carbonell and Deepak Kapur. 2004. Automatic Generation of Polynomial Loop Invariants: Algebraic Foundations. In International
     symposium on Symbolic and algebraic computation (ISSAC). Springer, 266–273.
[28] Enric Rodríguez-Carbonell and Deepak Kapur. 2007. Generating all polynomial invariants in simple loops. J. Symb. Comput. 42, 4 (2007), 443–476.
[29] R. Sharma, S. Gupta, B. Hariharan, A. Aiken, P. Liang, and A. V. Nori. 2013. A Data Driven Approach for Algebraic Loop Invariants. In Programming
     Languages and Systems. Springer Berlin Heidelberg, 574–592.
[30] X. Si, A. Naik, H. Dai, M. Naik, and L. Song. 2020. Code2Inv: A Deep Learning Framework for Program Verification. In Computer Aided Verification.
     Springer International Publishing, 151–164.
[31] Zhongyi Wang, Tengjie Lin, Mingshuai Chen, Haokun Li, Mingqi Yang, Xiao Yi, Shengchao Qin, Yixing Luo, Xiaofeng Li, Bin Gu, Liqiang
     Lu, and Jianwei Yin. 2025. A Tale of 1001 LoC: Potential Runtime Error-Guided Specification Synthesis for Verifying Large-Scale Programs.
     https://api.semanticscholar.org/CorpusID:284351244
Manuscript submitted to ACM
Integrating Symbolic Execution with LLMs for Automated Generation of Program Specifications                                                        27


[32] C. Wen, J. Cao, J. Su, Z. Xu, S. Qin, M. He, H. Li, S.-C. Cheung, and C. Tian. 2024. Enchanting Program Specification Synthesis by Large
     Language Models Using Static Analysis and Program Verification. In Computer Aided Verification: 36th International Conference, CAV 2024, Montreal.
     Springer-Verlag, 302–328.
[33] Daniel Wonisch and Heike Wehrheim. 2012. Predicate analysis with block-abstraction memoization. In International Conference on Formal Engineering
     Methods. Springer, 332–347.
[34] H. Wu, C. Barrett, and N. Narodytska. 2024. Lemur: Integrating Large Language Models in Automated Program Verification. In The Twelfth
     International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net. https://openreview.net/forum?id=
     Q3YaCghZNt
[35] H. Wu, Qi. Wang, B. Xue, N. Zhan, L. Zhi, and Z. Yang. 2025. Synthesizing Invariants for Polynomial Programs by Semidefinite Programming. ACM
     Trans. Program. Lang. Syst. 47, 1, Article 1 (Feb. 2025), 35 pages.
[36] Xiwei Wu, Yueyang Feng, Xiaoyang Lu, Tianchuan Lin, Kan Liu, Zhiyi Wang, Shushu Wu, Lihan Xie, Chengxi Yang, Hongyi Zhong, Naijun
     Zhan, Zhenjiang Hu, and Qinxiang Cao. 2025. QCP: A Practical Separation Logic-based C Program Verification Tool. arXiv:2505.12878 [cs.PL]
     https://arxiv.org/abs/2505.12878
[37] S. Yu, T. Wang, and J. Wang. 2023. Loop Invariant Inference through SMT Solving Enhanced Reinforcement Learning. In Proceedings of the 32nd
     ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA 2023). Association for Computing Machinery, 175–187.
[38] L. Zhou, J. Qin, Q. Wang, A. W. Appel, and Q. Cao. 2024. VST-A: A Foundationally Sound Annotation Verifier. Proc. ACM Program. Lang. 8, POPL,
     Article 69 (2024), 30 pages.




                                                                                                                        Manuscript submitted to ACM
