                                              Enhancing Automated Loop Invariant Generation for
                                               Complex Programs with Large Language Models

                                                  Ruibang Liua , Minyu Chena , Ling-I Wua , Jingyu Kea , Guoqiang Lia,∗
                                                               a Shanghai Jiao Tong University, 200240, Shanghai, China
arXiv:2412.10483v3 [cs.SE] 16 Sep 2025




                                         Abstract
                                         Automated program verification has always been an important component of building
                                         trustworthy software. While the analysis of loops remains a theoretical challenge, the
                                         automation of loop invariant analysis has effectively resolved the problem. However,
                                         existing invariant generation tools are predominantly effective for programs with purely
                                         numerical or purely pointer-based structures. Real-world programs often mix complex
                                         data structures and control flows. These structures can include arrays, pointers, and
                                         recursive definitions, while control flows may involve multiple nested or concurrent
                                         loops. Traditional methods generally only generate invariants for simple numerical
                                         programs or specific segments, lacking broad applicability. In order to automatically
                                         generate loop invariants for real-world programs, we proposed ACInv, an Automated
                                         Complex program loop Invariant generation tool, which combines static analysis with
                                         prompting with Large Language Models (LLM) to generate the proper loop invariants.
                                         We employ static analysis to systematically decompose the program’s data structures
                                         and loops. This involves layer-by-layer transmission of structural information about
                                         variables, numerical data, and the complete loop structure to the LLM, enabling the
                                         generation of corresponding invariants. In comparison to prior work on AutoSpec, we
                                         delve deeper into the variable information within each loop. We conducted experiments
                                         on ACInv, which showed that ACInv outperformed previous tools on data sets with data
                                         structures and maintained similar performance to the state-of-the-art tool AutoSpec on
                                         numerical programs without data structures. For the total data set, ACInv can solve 21%
                                         more examples than AutoSpec, and can generate reference data structure templates.
                                         Keywords: loop invariant generation, static analysis, large language models


                                         1. Introduction

                                             Program verification has progressively emerged as a fundamental component in the
                                         development of reliable software within the industry, thereby necessitating advanced
                                         tools for automated program verification. Nonetheless, the verification of program
                                         properties in the presence of loops is inherently undecidable. Within the framework of

                                           ∗ Corresponding author.

                                             Email address: li.g@sjtu.edu.cn (Guoqiang Li)


                                         Preprint submitted to Science of Computer Programming                            September 17, 2025
Hoare logic [1], loop invariants, which are usually assertions that are always true during
the entry and execution of the loop, serve as critical abstractions of loop properties.
These invariants are indispensable in enabling verification tools to rigorously establish
the correctness of programs. However, in the practical implementation of program
verification tools such as CPAchecker [2], CBMC [3], SMACK [4] and Frama-C [5], the
derivation of loop invariants often necessitates manual intervention by domain experts,
which poses a substantial impediment to the full automation of program verification.
     Loop invariants are usually defined inductively, which means that they must meet
the following two conditions: (1) Initialization: It is true before the first iteration of the
loop; (2) Maintenance: If the invariant holds true at the beginning of an iteration, it
must also hold true at the end of that iteration. From a theoretical perspective, for any
real-world program containing loops, irrespective of the programming language or the
complexity of the program’s code structure or data structure, we aim to automatically
generate correct loop invariants. Moreover, these loop invariants should be strong
enough to support the verification of relevant properties under various conditions.
     Although there is a substantial body of prior work on the automatic generation of
loop invariants, these methods often face challenges when applied to the verification
of real-world programs, primarily due to their generality and associated performance
overhead. Abstract interpretation baesd methods [6, 7, 8] was initially adopted by
researchers. These approaches typically employ static analysis techniques, such as
value analysis and interval analysis, to trace the values manipulated by the program
and subsequently synthesize these values to construct loop invariants. However, these
methods are limited to analyzing programs with simple numerical types and are less
effective in handling complex loops, advanced data types and structures, and fail to
adequately address intricate relationships between variables. Template-based meth-
ods [9, 10, 11, 12, 13] typically involve predefining invariants using SMT formulas,
proposing parameterized invariant templates via uninterpreted functions or inequalities,
and employing heuristic strategies to determine the parameters. While this approach
can reveal more complex relationships between variables, it remains largely confined
to linear numerical inequalities and imposes significant computational costs due to the
introduction of SMT constraint solving. The widespread adoption of machine learning
has led many researchers to propose learning-based methods [14, 15, 16, 17], which
infer suitable invariant templates through specific deductions and learn the correspond-
ing parameters using various learning techniques to generate invariants. However, their
effectiveness remains limited by the predefined templates and the quality of the training
data.
     In recent years, Large Language Models (LLMs), such as ChatGPT, have emerged
as powerful tools for automating various generative tasks. Several studies [18, 19] have
demonstrated their strong performance in program-related reasoning tasks. Notably,
recent works [20, 21, 22, 23, 24] have highlighted the potential of LLMs in generating
loop invariants. Trained on vast datasets encompassing both code and natural language,
LLMs possess a sophisticated understanding of code patterns and semantic relation-
ships. They excel at recognizing complex structures, such as loops, and are capable of
automating invariant generation across extensive codebases, significantly reducing the
need for manual effort.
     Despite the potential of LLMs in invariant generation, several challenges remain.


                                              2
First, as highlighted by prior studies [25, 26, 27, 28], the inferential capabilities of LLMs
require further exploration, particularly through carefully crafted prompts. Second,
LLMs may produce incorrect invariants, and these errors can compound when the
models are repeatedly invoked. To mitigate this issue, researchers have integrated SMT
solvers or verification tools into the workflow to filter out erroneous invariants. However,
this solution introduces significant performance overhead, and its effectiveness hinges
on the strength of the verification tool. Moreover, certain correct yet complex loop
invariants may be rejected by the tool, necessitating additional manual intervention,
which conflicts with the goal of an end-to-end approach. Lastly, even when error-
free, the invariants generated by LLMs may lack sufficient strength to capture precise
properties, thereby failing to assist in verifying the target property.
     To address these challenges, we propose ACInv, an Automated Complex program
loop Invariant generation tool leveraging Large Language Models (LLMs) in conjunction
with static analysis. In order for ACInv to be able to abstract data structures and reason
about invariants, we need some necessary program information. The tool begins by
extracting detailed information about the program’s data structures and variable values
within loops using static analysis techniques. ACInv then queries LLMs to generate
appropriate predicate templates, which abstract potential data structure properties in
the program. After this step, it inserts the predicates generated by LLMs as comments
in the program, further analyzing variable information within loops and annotating
those variables that undergo value changes in each iteration. For nested loops, the tool
recursively queries LLMs, starting with the innermost loop.
     In order to enable ACInv to determine the correctness of the invariants it generates
and further enhance the invariants it generates, we check and enhance each invariant
generated by ACInv. This step is completed by the evaluator and optimizer built by
LLM. The evaluator first evaluates the correctness of the invariant and then passes the
evaluation results and the corresponding invariant to the optimizer for processing. For
valid invariants, the optimizer seeks to refine them, while incorrect invariants are either
weakened to align with the correct program states or discarded altogether.
     We contend that ACInv offers several distinct advantages over existing tools. First, it
is capable of analyzing a wide range of complex, real-world code, with its sophisticated
template processing for data structures and effective handling of nested loops, enabling
it to tackle intricately structured programs. Second, ACInv delivers a fully automated,
end-to-end solution for loop invariant generation, significantly reducing the need for
manual intervention throughout the process. Lastly, while maintaining a competitive
level of correctness, ACInv minimizes time overhead and optimizes the quality of the
generated invariants.
     To evaluate ACInv, we conducted a series of experiments. We conducted experiments
on ACInv on datasets with and without data structures. The experiments showed that
ACInv performed better than all current tools on datasets with data structures. On
datasets without data structures, ACInv also performed close to the performance of the
state-of-art tool AutoSpec [22]. Overall, ACInv can solve 21.08% more examples than
AutoSpec.
     In summary, our contribution is:
    • We have built a better automatic invariant generation analysis method based on


                                             3
      LLM that can handle relatively complex data structures while maintaining a
      relatively high correctness rate with low local time consumption, and built a tool
      ACInv based on it.
    • We generated some predicate templates that may be useful for some commonly
      used data structures and other user-defined data structures on benchmarks such as
      [23, 29] and SV-COMP [30, 31].


2. Background

2.1. Loop Invariant
     To provide a formal characterization of the invariant, we first abstract the loop and
its invariants using Hoare logic [1] as follows:

                                    {I ∧ B} S {I}
                            {I} while (B) do (S) {I ∧ ¬B}

    Where we abstract the general loop structure in the form of pseudo-code into
the expression while (B) do (S), defining B as the guard condition, S as the loop
body, and I as the sought loop invariant. Given a loop invariant I, if the body S
preserves I under the condition that both I and B hold, i.e., {I ∧ B} S {I} is valid,
then initiating the loop in a state satisfying I ensures that upon termination, the state
satisfies both the invariant I and the negation of the guard condition ¬B, formally,
{I} while (B) do (S) {I ∧ ¬B}. This rule underscores the critical role of identifying
a suitable loop invariant I for verifying loop behavior.




                      Figure 1: A simple C code example with loop invariants.


     An example of loop invariants in ACSL The vast majority of invariant research is
based on the C language, so this paper will also use C language code as the research
object. In the following paper, we will use ANSI/ISO C Specification Language (ACSL)
to describe the loop invariants of the C program, which can be automatically checked
by the verification tool Frama-C [5] and its plugin WP. In ACSL, all the information
needed is implemented as the annotation which begins with \\@ or is wrapped with
\*@...*\, where loop invariants are annotated beginning with loop invariant.
     Consider the example depicted in Fig 1. The provided C code snippet above demon-
strates a simple while loop. The program starts by declaring an integer variable i and
initializing it to 0. The while loop runs as long as the condition i < 30 holds true.


                                                4
During each iteration, the value of i is incremented by 1 (++i). When i reaches 30,
the condition i < 30 becomes false, and the loop terminates. The C program imple-
ments a bounded iteration construct with a formally verified loop invariant 0 ≤ i ≤ 30
specified in ACSL annotations, where the loop initializes i to 0 and increments it
via pre-increment operation + + i until the guard condition i < 30 becomes false.
Through Hoare logic verification, the invariant satisfies initialization at entry (i = 0 ⇒
0 ≤ 0 ≤ 30), preservation under execution (0 ≤ i ≤ 30 ∧ i < 30 ⊢ 0 ≤ i + 1 ≤ 30
since i ≤ 29), and conclusion upon termination (0 ≤ i ≤ 30 ∧ ¬(i < 30) ≡ i = 30).
    What we still need to add and explain is, the invariant and predicate referenced herein,
along with those mentioned subsequently, are incorporated into the original code in the
form of annotations. However, these annotations differ significantly from conventional
comments. Traditional comments are authored by programmers to articulate their
design intentions informally. In contrast, predicates and invariants are employed to
specify certain program properties rigorously; they serve to assist in program verification
and similar tasks, and are expressed in a strict formal language based on the ACSL
(ANSI/ISO C Specification Language). Consequently, they serve distinct purposes and
are conventionally demarcated by specialized syntactic markers in practice.

2.2. Large Language Models (LLMs)
    In recent years, the field of Natural Language Processing (NLP) has achieved
significant advances. State-of-the-art models, particularly those built on the transformer
architecture [32], have achieved remarkable success in addressing a wide range of
natural language tasks. Large Language Models (LLMs), sophisticated neural networks
trained on massive text corpora, have emerged as powerful tools for understanding
and generating human-like language. By utilizing deep learning frameworks such
as transformers, LLMs can effectively capture and model intricate linguistic patterns
and relationships. These models represent a major leap forward in NLP, driven by
the convergence of novel architectures, vast datasets, and enhanced computational
resources. The development of large-scale pre-trained models like BERT (Bidirectional
Encoder Representations from Transformers) [33] and GPT (Generative Pre-trained
Transformer) [34] has led to substantial improvements across a variety of NLP tasks.
    Prompting is a technique where specific input phrases or instructions, known as
"prompts", are used to guide the LLM’s responses. Prompting leverages the model’s
pre-existing knowledge, allowing for immediate, on-the-fly task execution without the
need for additional training. This method is highly flexible and efficient, especially for
exploratory or dynamic tasks, as it does not require any modifications to the model’s
internal parameters. Previous work has demonstrated that techniques such as Chain-
of-Thought (CoT) prompting [26] and few-shot learning [34] are highly effective in
enhancing the performance of prompts. CoT prompting encourages the model to break
down complex problems into intermediate reasoning steps, enabling more structured
and logical responses. Few-shot learning involves providing the model with a small
number of task-relevant examples within the prompt, which helps the model understand
the specific format, context, or structure required for the task, even when it has not been
explicitly fine-tuned for it. Drawing from various prompting techniques [25, 26, 27, 28],
we designed a structured prompt framework to help us enhance computational efficiency
in deploying LLMs for inference.


                                             5
3. Methodology

3.1. Overview




                               Figure 2: The Workflow of ACInv


    In Figure 2, we present an overview diagram illustrating our proposed approach.
To address the aforementioned challenge, we introduce ACInv, an LLM-based tool for
automatic loop invariant generation. ACInv’s process consists of three main phases: (1)
Extraction Phase: ACInv initially extracts data structure and loop information from the
target program. This involves performing basic control flow and value analyses, classi-
fying loops, and gathering relevant variable information for each loop. (2) Generation
Phase: During this phase, ACInv embeds the extracted data structure information into
data structure prompts, querying LLMs to derive predicates that abstract key properties
of the data structure. These predicates, along with loop-specific information, are then
embedded into invariant prompts to generate loop invariants. If the current loop is not
the first in the program, information from preceding loops, along with their generated
invariants, will also be incorporated into the prompts. (3) Augmentation Phase: This
section mainly consists of two components: the evaluator, and the optimizer, which
are all composed of LLMs. The evaluator assesses the correctness of each generated
invariant. For correct invariants, the optimizer attempts to strengthen them. For in-
correct invariants, the optimizer weakens them to align with the correct program state.
If an invariant cannot be refined to the correct level after k iterations, it is discarded.
In the remainder of this section, we will provide a detailed explanation of the entire
methodology and its related intricacies.

3.2. Problem description
    To provide a more formal description of this problem, we formulate the invariants
generation task as follows: let M denote the LLMs, and P represent the program with a
maximum of n lines. Each line location in the code is denoted by l0 , l1 , · · · , ln , which
may correspond to a line in a loop or data structure.
    Let dnum ∈ D denote the indexed data structure instance retrieved by ordinal num,
while loopnum ∈ L corresponds to an independent loop structure identified with the
same indexing scheme, where D and L is the set of corresponding information. For each
loop loopnum , assuming its specific position in the program P starts at line li , where
i ∈ {1, n}, we define:
    • P as the prompts, which mainly include four prompts, predicate prompt as Pds ,
      invariant prompt as Pinv , evaluator prompt as Pev , and optimizer prompt as Pop ,


                                             6
    • M(P(loopnum , li , P, D)) as the query result specific to (loopnum , li ), and
    • {Iknum }mnum
              k=0  as the set of loop invariants at li .
Therefore, the current problem becomes: Given a program P with a maximum number
of lines n, for each loop loopnum ∈ L and its corresponding line li where i ∈ {1, n},
generate loop invariants {Iknum }m num
                                 k=0   ∈ I.




                                 Figure 3: Diagram of properties

     To formalize our requirements for the generated invariants’ properties, we employ
Fig. 3 to illustrate key characteristics. In this representation, distinct variables correspond
to different dimensions. The value ranges of these variables and their interrelationships
collectively delineate all reachable program states, denoted as P S in the figure. For
simplicity, only two variables x and y are shown; practical scenarios may involve
higher-dimensional relationships.
     The invariant I we aim to generate typically constitutes an over-approximation of
P S. Consequently, our primary requirement is correctness: the invariant must subsume
all reachable program states, i.e., P S ⊆ I. Under this correctness guarantee, a stronger
invariant is preferred, characterized by a tighter approximation closer to the true program
state. Formally, smaller variable ranges yield stronger invariants. As illustrated, I1 is
stronger than I0 , whereas I2 is weaker.

3.3. An illustrative example
    Consider the example illustrated in Fig 4. This program fragment is from the
widely-used FFmpeg [35] library, an open-source multimedia framework written in
C that facilitates the recording, conversion, and streaming of audio, video, and other
multimedia files. For this program fragment, we will focus on its main components,
omitting less relevant details.
    The VolDetectContext structure is employed to store audio sample values
for plotting frequency distributions. It contains a single member, histogram[],


                                               7
                    Figure 4: An illustrative example of C code from FFmpeg



which is an array of unsigned 64-bit integers used to represent the distribution of audio
sample frequencies. The filter_frame function processes audio filters within
FFmpeg, specifically handling audio frames and updating frequency distributions. It
iterates through each audio plane of the input audio frame (AVFrame) and adjusts
the corresponding count in vd->histogram, thus forming a nested loop structure.
The expression pcm[i] + 0x8000 shifts the sample values (typically ranging from
-32768 to 32767) to a 0 to 0xFFFF range for indexing purposes. This illustrative case
forms the basis for our theoretical extension in the following section, where we derive
generalized insights through rigorous analytical decomposition.

3.4. Extraction Phase
    The primary objective of this phase is to extract structural and loop information from
the target program P. The input of this phase is a program or code segment P, and output
the data structure information D = {dnum } and loop information L = {loopnum }. To
achieve this, we implement a specialized parsing module that systematically traverses
the entire program. The module first extracts data structure declarations and constructs
a comprehensive data structure information list, denoted as D = {dnum }. For each
identified data structure, the module retrieves all its members and determines whether
the data structure is recursive. A data structure is considered recursive if it contains a
member of its own type. The recursiveness of a data structure significantly influences
subsequent processing stages. At this phase, we merely flag the recursive nature of data
structures, with detailed processing strategies to be elaborated in later stages.
    More specifically, this stage actually achieves the following operations, such as
Algorithm 1:
    This algorithm performs static analysis of C programs through abstract syntax tree
(AST) traversal, extracting structural and behavioral metadata. The procedure takes
a C program P as input and outputs two sets: D for data structure declarations and
L for loop information. Initialization establishes empty sets D and L, along with an
empty loop stack to track nesting depth. During AST traversal, when encountering a
struct declaration, the algorithm extracts its composite data type definition τ and adds
τ to D. For loop constructs (for/while/do-while), it pushes the loop node onto the
stack, identifies all modified variables Vmod within the loop body, computes the current


                                              8
  Algorithm 1: The algorithm for extraction phase
    Input :A C program P
    Output :Set D of data structures, Set L of loop information
  1 D ←∅;                            // Initialize data structure set
  2 L←∅;                          // Initialize loop information set
  3 loopStack ← empty stack ;           // Track nested loop positions
  4 foreach node n in the Abstract Syntax Tree (AST) of P do
  5     if n is a struct declaration then
  6         D ← D ∪ {(datatype, dataname))} ;             // Record struct
  7     else if n is a loop (for/while/do-while) then
  8         push n onto loopStack ;                // Update loop position
  9         modif iedV ars ← ∅ ;
 10         foreach variable v modified in n’s body do
 11              modif iedV ars ← modif iedV ars ∪ {v}
 12          loopDepth ← |loopStack|
              L ← L ∪ {(modif iedV ars, loopDepth)} ;            // Record loop
 13          pop n from loopStack
14    return (D, L);


nesting depth as the stack size, records the tuple (Vmod , depth) to L, and finally pops
the loop node from the stack. The algorithm terminates by returning the tuple (D, L),
providing comprehensive structural definitions and loop mutation patterns essential for
downstream program analysis tasks such as parallelization or dataflow verification, with
O(n) complexity proportional to AST node count.
     Subsequently, ACInv systematically traverses the control flow graph of the program,
with particular emphasis on loop structures. To facilitate structural analysis and provide
clear decomposition pathways for the LLM, a hierarchical decomposition strategy is
employed to break down complex loop constructs. During this process, ACInv identifies
all loop instances within the program and assigns unique sequence numbers organized
in a loop stack method. The numbering scheme follows these principles: for nested
loops, the innermost loop receives the smallest number, while for parallel loops, priority
is given to the loop appearing earlier in the program text. As illustrated in Fig 4, the
innermost loop is labeled as 1, the enclosing loop as 2, and if there is a subsequent
loop following this nested structure, it would be assigned number 3. This sequential
numbering scheme establishes an analytical framework that guides the program analysis
in subsequent phases, ensuring systematic exploration of the program’s control flow.
     Variable information can help LLM focus its attention on key parts, providing
assistance in generating invariants. For each loop, ACInv also captures key variable
information, which is specifically, all assigned variables and parameters passed as
pointers in function calls. The parser will provide all variables that have undergone
value changes and determine their variable types, including whether they belong to the
abstract data types defined by the previously extracted data structure. All the information,
along with the loop sequence number, forms the loop structure information loopnum


                                             9
and is then maintained in the list L = {loopnum }.
    For the example in Fig 4, ACInv will record the declaration of the structure
VolDetectContext, provide a judgment that it is not recursive, and then traverse the
program body. After completing the traversal of the loop body, it assigns sequence num-
ber 1 to the inner loop with line numbers 23-24 and extracts key variables: {i, vd};
then assigns sequence number 2 to the outer loop with line numbers 20-25 and extracts
key variables: {plane, pcm[]}, as well as {i, vd} inherited from the inner loop.

3.5. Generation Phase
    In this phase, ACInv will leverage the information extracted in the previous phase to
generate loop invariants by querying LLMs. The generation module of ACInv accepts
the input (P, D, L), which is the target program and the information of data structure
                                                                   num
and loop parsed in the extraction module, and give the output {I ′ k }m  k=0 which is the
preliminary invariant for each loop loopnum ∈ L.




                             Figure 5: The prompts used in ACInv


    In real-world programs, a fundamental challenge in automated invariant generation
stems from the prevalence of custom data structures that frequently appear in real-world
programs. These structures often represent either specialized variations of conventional
data structures or, more commonly, intricate compositions tailored to specific application
requirements. To address this challenge, our approach emphasizes the systematic
characterization and formal specification of the properties of these data structures as
a prerequisite step prior to invariant generation. This preliminary analysis enables
more accurate and meaningful invariant derivation that properly reflects the semantic
complexity of real-world data organizations. First, ACInv will embed the data structure
information D = {dnum } into the predicate prompts Pds , which is illustrated in
Figure 5 and query the LLM to obtain predicate templates that may be used for this data


                                             10
structure. In prompts, we emphasize that these predicates need to be able to abstract
the data structure itself, and in addition, provide some other properties about this data
structure.
    A critical observation reveals that the recursiveness of custom data structures consti-
tutes a fundamental property that significantly influences both the formal specification
of these structures in ACSL and the derivation of their associated properties. This
characteristic plays a pivotal role in determining the appropriate representation and
analysis of data structures throughout the verification process. In the syntax of ACSL,
we can use predicate to define predicates related to non-recursive data structures,
and inductive to define predicates related to recursive data structures. In order to
help LLM understand predicate generation, we provided some examples to LLM, which
are called shots in LLM prompting. The [[Examples]] section in the predicate
prompts acts as a placeholder that will be dynamically filled with specific examples.
Similarly, the [[Code]] placeholder will be replaced with the actual corresponding
data structure. For non-recursively defined data structures, we provide a classic example:
the stack, whose C language definition is usually as Figure 6a.
    In order to help LLM understand predicate generation, we provided some examples
to LLM, which are called shots in LLM prompting. For non-recursively defined data
structures, we provide a classic example: the stack, whose C language definition is
usually as Figure 6a.


1 struct stack_int{                                         1 struct Node{
2     size_t top;                                           2     int data;
3     int data[MAX_SIZE];                                   3     struct Node * next;
4}                                                          4 };


  (a) An non-recursive data structure example: stack            (b) A recursive data structure example: linked list

                                    Figure 6: Two examples of data structure.


    We expect the generated predicate to at least express that this is an effective stack; In
addition, we also hope that it can express some other properties about the stack, such as
whether the stack is empty or full. Therefore, in this example, we provide the following
predicate such as Figure 7a. In ACSL grammar, \valid(s) means the pointer s is
valid to read or write. The recursive data structure is usually related to pointers. Taking
inspiration from separation logic [36], we provide such a recursive definition for the
following single linked list, which considered both empty and non-empty linked lists,
and expressed that the pointer p1 to p2 is a single linked list such as Figure 7b.
    Then, combined with the possible predicates, ACInv embeds the program P and
the loop information L into the invariants prompt Pinv to query the LLM. Based on
the order of the loops, ACInv will sequentially query the LLM for the loop with the
smallest ordinal number, and require the LLM to generate invariants for that loop.
Within each loop, we embed the processed program into prompts and require the
LLM to analyze the following: (1) the range of values of the annotated variables;
(2) Possible logical relationships between these variables and constants; (3) Does the
data structure variable satisfies the predicate. The [[Example]] section provides


                                                       11
            (a) The predicates of stack                          (b) The predicates of linked list

                                Figure 7: Two examples of data structure.



multiple program instances accompanied by their corresponding loop invariants, with
particular emphasis on detailed explanations of nested loop structures and the associated
data structures utilized within these examples. This section serves to illustrate both
the general patterns and specific considerations for invariant generation in complex
control flow scenarios and custom data structure implementations. From the responses
generated by the LLM, we systematically extract the invariants corresponding to their
designated positional indices. Specifically, for a given loop identified by its numerical
                                                                num
label num, we obtain its corresponding invariant {I ′ k }m          k=0 . When the traversal
of all loops is completed, we obtain a comprehensive set of invariants, denoted as
            1          ′ 2 m2              ′ num mnum
I ′ = {{I ′ k }m
               k=0 , {I k }k=0 , · · · , {I k
                 1
                                                }k=0 , · · · }.
    Figure 4 illustrates the majority of the process for this step. Initially, two predi-
cates are generated based on the data structure, which represents whether it is a valid
VolDetectContext and the non-negativity of the array histogram[]. Using
these predicates, ACInv first derives an invariant for Loop 1, which is an inner loop.
Once this invariant is obtained, all invariants within this loop are forwarded to the next
stage for enhancement. Following this, the enhanced invariant is used as a reference for
generating the invariant for Loop 2 by querying the LLM.

3.6. Augmentation Phase
     A prevalent challenge is that the invariants generated by LLMs often tend to be
weak—for instance, trivial solutions such as I = T RU E are frequently produced. To
address this issue while simultaneously filtering out incorrect candidates, we introduce
an augmentation phase. In this phase, ACInv focuses on refining the generated invariants
by either strengthening or weakening them. Building upon the previous phase where we
derived the initial set of invariants I ′ from program P, we now aim to perform a deeper
analysis to refine and enhance the invariant collection. We seek to obtain an optimized
set of invariants I that more accurately captures the program’s behavioral properties
and provides stronger verification guarantees. Unlike the previous phase, this stage
is loop level, which means that for each individual loop, the generated invariant will
first be sent to this stage to try to be enhanced, and then the enhanced invariant group
will be sent back to the generation phase as a reference for generating the invariant in
                                                                             num
subsequent loops. For each loop loopnum , the i-th generated invariant I ′ i      will be
enhanced independently.
     It begins by utilizing an evaluator to assess the correctness of the invariants and
then calls upon an optimizer to take appropriate actions based on the evaluation. Both
the evaluator and optimizer are LLM-based. As illustrated in Fig 5, we use elaborately


                                                  12
designed dedicated prompts and examples to implement the LLM-based evaluator and
optimizer. It is important to note that these components utilize LLMs independently,
both with each other and with the LLM employed in the aforementioned generation
phase. As mentioned earlier, we hope to use evaluators to ensure the correctness and
optimizers to guarantee a stronger invariant. However, a very normal concern is that the
LLM may make mistakes. However, relevant studies [20] have shown that the existing
LLMs already have a strong enough reasoning ability and can give results with relatively
reliable correctness rates to a certain extent. Through multiple independent information
processing operations, we can further reduce its error probability. We expect to complete
an end-to-end invariant generation work based on LLM, and thus it can be applied to
scenarios that tolerate certain errors.
     If an invariant is deemed correct, ACInv will attempt to "strengthen" it. In the
context of invariants, this typically involves narrowing the range of program variable
states represented, resulting in a more precise invariant. Conversely, if the invariant is
deemed to be incorrect, ACInv seeks to "weaken" it. This process involves expanding
the range of program variable states to encompass the correct set of states within the
revised invariant. By broadening the scope of the incorrect invariant, ACInv aims to
adjust it to better reflect the valid program states. However, our weakening process
incorporates a rejection mechanism, allowing the LLM to decline the weakening attempt
if it determines that the invariant cannot be properly weakened while maintaining
correctness. Following this step, the results are subsequently returned to the evaluator
for further validation. To control the iterative refinement process, we introduce a
parameter k that limits the maximum number of query cycles. When this threshold is
reached, invariants that remain incorrect are permanently rejected, while those that have
been successfully validated are retained in the final invariant set. At this stage, we obtain
the final set of invariants, denoted as I = {{Ik1 }m       2 m2               num mnum
                                                   k=0 , {Ik }k=0 , · · · , {Ik
                                                     1
                                                                                 }k=0 , · · · }.
     In practice, before entering the augmentation phase, the invariant generated by
ACInv for Loop 2 in Figure 4 is 0 <= plane < nb_planes. However, during the
execution of the loop, although the outer loop condition is plane < nb_planes,
the final iteration may satisfy plane == nb_planes. Thus, this invariant does not
cover all possible program states. The evaluator can identify this issue and the optimizer
can adjust the invariant by expanding its range to 0 <= plane <= nb_planes,
ultimately providing the refined invariant.

4. Experiment
4.1. Reaserch Question
    In this section, we will propose several intriguing research questions concerning
ACInv and conduct experiments to address these questions:
    • RQ1: Can ACInv generate correct predicate templates for complex programs
      with data structure and thus generate correct loop invariants?
    • RQ2: Can ACInv generate correct loop invariants for complex programs without
      data structure?
    • RQ3: How useful is the augmentation phase for ACInv?


                                              13
4.2. Experimental Setup
    Benchmark Our dataset is mainly divided into two parts: those with data structures
and those without data structures. The dataset of data structure consists of three parts:
LIG-MM [23, 29], SV-COMP [30, 31], and FFmpeg [35]. We will elaborate on these
three datasets in more detail later. The dataset without data structure mainly comes from
the benchmark from AutoSpec [22], and we will also briefly describe this dataset.
    First, we selected the benchmark from LIG-MM, which is a new benchmark specifi-
cally for programs with complex data structures and memory manipulations. LIG-MM
is also divided into four parts: (1) the course programs which originate from course
homework; (2) SV-COMP [37], the competition on software verification; (3) Benchmark
from SLING [38], which is a separation logic loop invariant inferring tool using dy-
namic analysis; (4) Some real-world programs from well-known software and systems.
LIG-MM consists of C code and focuses on some complex data structures, especially the
single-linked list, double-linked list, tree, and hash table, which can be an appropriate
reference dataset. Due to the limit on the number of tokens, we selected 227 examples
with relatively few lines of code for testing.
    We also picked C programs from SV-COMP 2024. LIG-MM and the benchmark of
AutoSpec both select some programs from SV-COMP. But unlike them, we chose differ-
ent parts. We selected twenty-six programs, all of which include at least one loop and
one data structure. Among these data structures, we excluded all structures containing
the single-linked list, double-linked list, tree, and hash table to avoid duplication with
the selected parts in LIG-MM. Therefore, these programs also include many different
types of structures.
    To evaluate the effectiveness of ACInv on real-world programs, we selected several
program segments from the widely used FFmpeg, the audio and video processing library.
Given the complexity of function calls and structures within C programs, as well as the
extensive codebase, we focused on specific portions of the program. We applied simple
partitioning techniques, ensuring that ACInv could concentrate on the relevant functions
for analysis, and we picked the programs with at least one loop and at least one data
structure.
    We also selected programs from AutoSpec, an automated tool for generating ACSL
specifications for C programs. AutoSpec’s benchmark assesses the tool’s ability to
synthesize specifications, including loop invariants, preconditions, and postconditions
of functions. Notably, some C programs in this benchmark do not contain loops, so we
specifically chose a subset that includes loops for our testing.
    Benchmark from AutoSpec comprises four parts, which we introduce briefly: (1)
Frama-C problems[39], a repository focused on program verification challenges for
Frama-C. We selected a portion containing C programs with loops. (2) SyGuS[40],
which represents the invariants track from the Syntax-Guided Synthesis competition,
featuring only programs with linear loop structures. (3) OOPSLA-13[41, 42], and (4)
SV-COMP[37], both of which include benchmarks that may have nested or multiple
loops. All these benchmarks consist of C code, primarily focused on numerical programs
without explicit structural declarations.
    Baseline In this study, we compare the performance of several tools with ACInv on
datasets both with and without data structures. For datasets with data structures, we eval-
uate SLING, LLM-SE [23], GPT-4o, and AutoSpec. SLING is a dynamic analysis tool


                                            14
                      Table 1: Comparison of Performance on Multiple Datasets


                      Data Structure                    non-Data Structure                    Overall
Tools
             LIG-MM     SVCOMP24 FFmpeg       Frama-C   SyGuS     OOPSLA SVCOMP22 Struc       non-Struc   All

non-LLM
SLING          .171        .000        .000      -         -         -           -     .128       -       .055
CODE2Inv        -           -           -      .000      .549       .196        .000    -       .358      .204
CLN2Inv         -           -           -      .000      .932       .000        .000    -       .541      .309

LLM-based
LLM-SE         .419         -           -        -         -         -           -     .314       -       .135
GPT-4o         .054        .192        .059    .172      .278       .261        .143   .076     .249      .175
AutoSpec       .016        .308        .059    .414      .857       .826        .762   .064     .786      .476
ACInv-3.5      .139        .307        .118    .345      .714       .457        .429   .163     .589      .407
ACInv-4o       .318        .462        .353    .483      .797       .761        .762   .343     .747      .574




for inferring loop invariants based on separation logic. LLM-SE leverages a fine-tuned
LLM (which is CodeGen [43] in the specific implementation) to generate separation
logic loop invariants, incorporating predicate decomposition into its training. AutoSpec
employs hierarchical specification generation to produce ACSL-style annotations. Both
LLM-SE and AutoSpec utilize verification checkers to ensure the correctness of the
generated invariants. GPT-4o, in this context, is used by directly embedding the code
into prompts, asking GPT-4o-2024-08-06 to generate loop invariants without employing
specific prompting techniques or examples.
    For datasets without data structures, we assess CODE2Inv [16, 44], CLN2Inv [14],
GPT-4o, and AutoSpec. CODE2Inv and CLN2Inv are state-of-the-art invariant genera-
tion tools for numerical programs, based on graph neural networks and continuous logic
networks, respectively. AutoSpec was originally a tool for testing on this benchmark,
and we naturally referred to its results.
    Environment We primarily employ GPT-4o-2024-08-06 as the core model for
implementing ACInv, with GPT-3.5-turbo serving as a control in our experiments. The
experiments are performed on a system equipped with an AMD Ryzen 9 5950X CPU,
running Ubuntu 23.04, 128GB of RAM, and two NVIDIA RTX 4090 GPUs, each with
24GB of memory.

4.3. RQ1: Performance on Structure Datasets
     Table 1 shows the main results of our experiments, where completion means the
rate of programs whose loop invariants can be inferred correctly to complete the ver-
ification of this program. In this experiment, considering the balance between time
and performance, we set the augmentation iteration parameter k to 5. Compared to the
traditional tool SLING, LLM-based technologies, including ACInv, demonstrate strong
applicability. While SLING can only reason about the linked list portion of LIG-MM,
it struggles with other complex data structures. Experimental results from LLM-SE
indicate good performance on singly linked lists (sll), doubly linked lists (dll), trees,


                                                 15
and hash tables. However, LLM-SE did not provide training sets or fine-tuned models,
limiting the ability to evaluate its performance on other data structures. Additionally,
LLM-SE incorporates pre-defined predicates during fine-tuning, enabling abstraction
during reasoning, though this approach may restrict its effectiveness on other data
structures or non-pointer data structures.
    In comparison to pure LLM querying and the latest technology, AutoSpec, ACInv
performs well on datasets involving data structures. This performance is anticipated.
In pure LLM querying, we observed that while the LLM can recognize data structures
in the program and analyze the associated variables, it struggles to abstract them into
suitable logical forms. This often results in accurate formulas being expressed in natural
language rather than logical terms. Regarding AutoSpec, its examples primarily focus
on numerical types, leading to suboptimal performance on benchmarks involving data
structures.
    The FFmpeg dataset presents significant challenges due to its many unpredictable
user-defined data structures, making it difficult for large models to abstract their proper-
ties. None of the tools performed well in this scenario, though ACInv exhibited some
advantages. Overall, the experiments suggest that ACInv possesses a notable degree
of abstraction and reasoning capability across various datasets involving complex data
structures.

4.4. RQ2: Performance on non-Structure Datasets
     In numerical programs, ACInv demonstrated performance comparable to AutoSpec.
The SyGuS benchmarks, which consist of relatively simple programs with a single loop
and focus on basic numerical transformations, saw CLN2Inv achieving the best results.
However, both CODE2Inv and CLN2Inv performed poorly on other datasets, likely due
to limitations in their training sets, highlighting the broader applicability of LLM-based
technologies. The Frama-C problems benchmark, which involves nested loops and
more complex variable interactions, posed greater challenges. ACInv, leveraging value
analysis, performed notably better in these cases.
     Overall, ACInv approached state-of-the-art performance in numerical programs
without data structures and demonstrated clear advantages across diverse datasets.

4.5. Case Study:
     Considering the example as Figure 8. This program snippet performs an in-place
iterative reversal of a singly linked list through pointer manipulation. Three pointers
are initialized: old references the head of the original list, newn is set to NULL,
representing the nascent reversed list, and curr is initialized to traverse the original list
starting at old. During each iteration, old is advanced to its successor node to preserve
traversal integrity, the next pointer of curr is redirected to newn to reverse linkage
direction, newn is updated to reference the current node, thus extending the reversed
sublist, and curr is reset to old for subsequent processing. The loop terminates when
curr becomes NULL, at which point newn references the head of the fully reversed
list. To give a specific example, if this linked list was originally A->B->C->NULL, it
becomes C->B->A->NULL after the reversal.
     Most of the other methods based on LLM can only obtain one invariant for this
loop, namely old == curr. By observing the detailed output of the LLM, we can


                                            16
                           Figure 8: In-place reversal of the singly linked list



find that the LLM can actually capture some more specific properties. That is, this
linked list is divided into two parts from the pointers old and curr. The part before
curr is the flipped linked list, while the part after old is the linked list that has not
been flipped yet. However, LLMs cannot describe this property completely formally.
Instead, it describes it in a semi-formal and semi-natural language way, such as curr
== suffix of the original list starting at position i. And our work can provide a
more formal description of this nature, namely is_linked_list(curr,NULL),
is_linked_list(old,NULL).

4.6. RQ3: Testing for the Augmentation

                                                                                                86.63
                                      85                                             84.30
                                                                          80.23
                                      80                      78.49
                       Accuracy (%)




                                      75

                                                    70.35
                                      70


                                      65

                                           61.05
                                      60
                                           No Aug   GPT-3.5   GPT-4o@1    GPT-4o@3   GPT-4o@5   GPT-4o@10
                                                                     Models

                           Figure 9: Performance of Augmentation of ACInv


    Figure 9 shows the results of the experiment on the augmentation of ACInv. We
tested the invariants generated by ACInv on a structured dataset, where Acc means the
proportion of generated invariants that can pass the frama-c check, and model@k means
k augmentation iterations were performed on the model. The experiment shows that
when we use appropriate prompts and examples, the augmentation stage can judge the
correctness of the invariants with a relatively high probability and filter out incorrect
invariants.

4.7. Threats to validity
    Data leakage. The extensive training sets used in LLMs can lead to potential data
leakage, meaning that some of the code related to the questions we inquired about might


                                                                    17
have appeared in the training data of certain models. Although we have applied simple
variable renaming and reordered the code, similar issues may still arise.
    Correctness determination. Most related work, particularly during the final evalua-
tion stage (and in some cases even in earlier stages), employs a deterministic checker to
validate the generated invariants for filtering purposes. We did not adopt this approach
here, partly due to performance overhead concerns and partly to avoid making the
generated invariants dependent on a specific checker. In our experiments, we observed
that some correct invariants could not be verified by the checker due to limitations in the
checker’s capability and available computational resources. In future work, we aim to
follow up on this aspect, seeking to strike a more effective balance between correctness
and scalability.


5. Related Work

5.1. LLM for static analysis
    Recent advances in LLMs have opened new avenues in static analysis. By integrating
LLMs with traditional static analysis techniques, their scope can be broadened, leading
to more effective and deeper program comprehension.
    LLM4SA [45] leverages LLMs to analyze static warnings, reducing the need for
manual effort. LLift [18] integrates static analysis with LLM-based prompting, success-
fully identifying Use Before Initialization (UBI) bugs in the Linux kernel. CFStra [19]
employs LLMs to automatically select verification strategies based on code features
and specifications. IRIS [46] combines LLMs with static analysis to perform whole-
repository reasoning, detecting security vulnerabilities. NS-Slicer [47] uses a fine-tuned
model to predict static program slices for both complete and partial code. Codeplan [48]
synthesizes a multi-step chain of edits to assist with repository-level coding. Clari-
fyGPT [49] enhances code generation by leveraging LLMs, while AutoFL [50] utilizes
LLMs to generate explanations of bugs for the purpose of Fault Localization (FL).
Overall, incorporating LLMs has mitigated challenges related to applicability and per-
formance overhead in static analysis and has enhanced the ability to analyze real-world
code.

5.2. Invariants Generation
    Symbolic methods Traditional symbolic methods for invariant generation typically
involve direct code analysis, mainly including abstraction interpretation and constraint
solving. Abstract interpretation [51] approximates a program’s behavior by mapping its
concrete semantics to a simplified abstract domain, often using fixed-point calculations
to abstract program states in the presence of loops. Enric et al.[6] developed a framework
for generating conjunctions of loop invariants constrained to linear inequalities or
polynomial equations, later extending the approach to polynomial invariants of bounded
degree[7]. Steven et al. [8] applied a combination of Groebner bases, linear algebra,
and abstract interpretation to generate polynomial invariants. Constraint-based methods,
on the other hand, rely on pre-defined templates and employ SMT solvers to filter out
appropriate invariant expressions. Farkas’ lemma [9, 10, 11, 12, 13] is frequently used



                                            18
to extract linear relationships from loops, while other constraint templates, such as those
based on Craig’s interpolant [52, 41, 42], are also employed.
     Separation Logic (SL) [36] is an extension of Hoare logic to reason about memory
structures and the interactions of programs with dynamically allocated memory. It
introduced the concept of "separating conjunction," which allows for concise reasoning
about disjoint memory regions and parallel computation. Based on the extension of
list manipulation [53], THOR [54, 55, 56] and MemCAD [57] are able to infer loop
invariants on numeric and linked list programs. More recently, SLING [38] advances
SL invariant generation by employing dynamic analysis to track memory and numerical
changes in pointer-related structures.
     Learning-based methods Learning-based methods often build upon template-based
approaches by learning the parameters within these templates through various machine-
learning techniques and ultimately invoking an SMT solver to filter suitable invariants.
C2I [58] employs a randomized search to discover candidate invariants, followed by a
checker to validate them. ICE [15] did learning for synthesizing invariants, leveraging
examples, counterexamples, and implications. Then they combined them with decision
trees [59]. CODE2INV [16, 44] utilizes reinforcement learning and graph neural
networks to learn program structures. LIPuS [17] also adopts reinforcement learning
and uses pruning to reduce the search space. CLN2INV [14] introduces Continuous
Logic Networks (CLN) to automatically learn loop invariants directly from program
execution traces, while Gated-CLN (G-CLN) [60] extends this approach to allow the
model to robustly learn general invariants across a large number of terms.
     LLMs for loop invariants Just as we talked about above in the experiment section,
LIG-SE [23] fine-tuned the large model and combined it with a checker, giving the LLM
the ability to handle separation logic. It can also handle data structures and abstract
predicate properties to a certain extent. Autospec [22] employs hierarchical specification
generation to produce ACSL-style annotations, which include loop invariants and have
achieved good performance in the processing of numerical programs. Both LLM-SE
and AutoSpec call the checker at the end to ensure the correctness of the generated
invariants. Several other works have explored the intersection of LLMs and loop
invariant generation with promising outcomes. The iRank tool [20] introduces a re-
ranking approach that evaluates loop invariants produced by LLMs. Unlike other
methods, iRank does not focus on generating loop invariants but instead addresses the
challenge of verifying the correctness of LLM-generated invariants. To achieve this, the
authors employed two distinct LLM-based embedding models to learn the criteria for
determining invariant correctness. Kexin et al.[21] aimed to fine-tune a pre-trained LLM
for abstract reasoning over program executions, allowing for the generation of loop
invariants. Their approach relies on a dynamic analyzer to trace program executions,
which are then used to derive invariants. However, their evaluation is limited to a
comparison against invariants generated by the dynamic analyzer, which poses inherent
constraints. Loopy[24], on the other hand, continuously queries LLMs to generate
invariants and employs a verification tool to ensure correctness. While they enhance the
generated invariants by cyclically applying the Houdini algorithm and making repairs,
the repeated invocation of the verifier introduces significant performance overhead.




                                            19
6. Conclusion

    In this paper, we proposed ACInv, an Automated Complex program loop Invariant
generation tool leveraging Large Language Models (LLMs) in conjunction with static
analysis. ACInv can abstract the data structure properties in complex programs and
combine them to generate invariants. ACInv can also evaluate and enhance the generated
invariants to a certain extent. We have conducted experiments on the effect of ACInv,
and the experiments show that ACInv has achieved certain results on various data sets.

Acknowledgment
   This work is supported by the National Natural Science Foundation of China Grant
No. 61872232.


References

 [1] C. A. R. Hoare, An axiomatic basis for computer programming, Commun. ACM 12
     (1969) 576–580. URL: https://doi.org/10.1145/363235.363259.
     doi:10.1145/363235.363259.
 [2] D. Beyer, M. E. Keremoglu, Cpachecker: A tool for configurable software
     verification, in: G. Gopalakrishnan, S. Qadeer (Eds.), Computer Aided Verification,
     Springer Berlin Heidelberg, Berlin, Heidelberg, 2011, pp. 184–190.

 [3] D. Kroening, M. Tautschnig, Cbmc – c bounded model checker, in: E. Ábrahám,
     K. Havelund (Eds.), Tools and Algorithms for the Construction and Analysis of
     Systems, Springer Berlin Heidelberg, Berlin, Heidelberg, 2014, pp. 389–391.
 [4] Z. Rakamarić, M. Emmi, Smack: Decoupling source language details from verifier
     implementations, in: A. Biere, R. Bloem (Eds.), Computer Aided Verification,
     Springer International Publishing, Cham, 2014, pp. 106–113.
 [5] F. Kirchner, N. Kosmatov, V. Prevosto, J. Signoles, B. Yakobowski, Frama-
     c: A software analysis perspective,       Form. Asp. Comput. 27 (2015)
     573–609. URL: https://doi.org/10.1007/s00165-014-0326-7.
     doi:10.1007/s00165-014-0326-7.

 [6] E. Rodríguez-Carbonell, D. Kapur, An abstract interpretation approach for auto-
     matic generation of polynomial invariants, in: R. Giacobazzi (Ed.), Static Analysis,
     Springer Berlin Heidelberg, Berlin, Heidelberg, 2004, pp. 280–295.
 [7] E. Rodríguez-Carbonell, D. Kapur, Automatic generation of polynomial
     invariants of bounded degree using abstract interpretation, Science of Computer
     Programming 64 (2007) 54–75. URL: https://www.sciencedirect.
     com/science/article/pii/S0167642306001572.                          doi:https:
     //doi.org/10.1016/j.scico.2006.03.003, special issue on the 11th
     Static Analysis Symposium - SAS 2004.




                                          20
 [8] S. de Oliveira, S. Bensalem, V. Prevosto, Polynomial invariants by linear algebra,
     in: Automated Technology for Verification and Analysis, Springer International
     Publishing, Cham, 2016, pp. 479–494.
 [9] S. Sankaranarayanan, H. B. Sipma, Z. Manna, Constraint-based linear-relations
     analysis, in: R. Giacobazzi (Ed.), Static Analysis, Springer Berlin Heidelberg,
     Berlin, Heidelberg, 2004, pp. 53–68.
[10] P. Yao, J. Ke, J. Sun, H. Fu, R. Wu, K. Ren, Demystifying template-based invariant
     generation for bit-vector programs, in: 2023 38th IEEE/ACM International
     Conference on Automated Software Engineering (ASE), IEEE, Luxembourg,
     Luxembourg, 2023, pp. 673–685. doi:10.1109/ASE56229.2023.00069.

[11] H. Liu, G. Li, Empirically scalable invariant generation leveraging divide-and-
     conquer with pruning, in: W.-N. Chin, Z. Xu (Eds.), Theoretical Aspects of
     Software Engineering, Springer Nature Switzerland, Cham, 2024, pp. 324–342.
[12] M. A. Colón, S. Sankaranarayanan, H. B. Sipma, Linear invariant generation using
     non-linear constraint solving, in: W. A. Hunt, F. Somenzi (Eds.), Computer Aided
     Verification, Springer Berlin Heidelberg, Berlin, Heidelberg, 2003, pp. 420–432.
[13] H. Liu, H. Fu, Z. Yu, J. Song, G. Li, Scalable linear invariant generation with
     farkas’ lemma, Proc. ACM Program. Lang. 6 (2022). URL: https://doi.
     org/10.1145/3563295. doi:10.1145/3563295.
[14] G. Ryan, J. Wong, J. Yao, R. Gu, S. Jana, Cln2inv: Learning loop invariants
     with continuous logic networks, in: International Conference on Learning Rep-
     resentations, OpenReview.net, Addis Ababa, Ethiopia, 2020, pp. 1–17. URL:
     https://openreview.net/forum?id=HJlfuTEtvB.
[15] P. Garg, C. Löding, P. Madhusudan, D. Neider, Ice: a robust framework for learn-
     ing invariants, in: A. Biere, R. Bloem (Eds.), Computer Aided Verification,
     Springer International Publishing, Cham, 2014, pp. 69–87.
[16] X. Si, H. Dai, M. Raghothaman, M. Naik, L. Song, Learning loop invariants for
     program verification, in: Advances in Neural Information Processing Systems,
     volume 31, Curran Associates, Inc., Palais des Congrès de Montréal, Montréal
     CANADA, 2018, pp. 7762–7773.

[17] S. Yu, T. Wang, J. Wang, Loop invariant inference through smt solving enhanced
     reinforcement learning, in: Proceedings of the 32nd ACM SIGSOFT International
     Symposium on Software Testing and Analysis, ISSTA 2023, Association for Com-
     puting Machinery, New York, NY, USA, 2023, p. 175–187. URL: https://doi.
     org/10.1145/3597926.3598047. doi:10.1145/3597926.3598047.

[18] H. Li, Y. Hao, Y. Zhai, Z. Qian, Enhancing static analysis for practical bug
     detection: An llm-integrated approach, Proc. ACM Program. Lang. 8 (2024).
     URL: https://doi.org/10.1145/3649828. doi:10.1145/3649828.



                                          21
[19] J. Su, L. Deng, C. Wen, S. Qin, C. Tian, Cfstra: Enhancing configurable program
     analysis through llm-driven strategy selection based on code features, in: Theoret-
     ical Aspects of Software Engineering, Springer Nature Switzerland, Cham, 2024,
     pp. 374–391.
[20] S. Chakraborty, S. Lahiri, S. Fakhoury, A. Lal, M. Musuvathi, A. Rastogi,
     A. Senthilnathan, R. Sharma, N. Swamy, Ranking LLM-generated loop invari-
     ants for program verification, in: Findings of the Association for Computational
     Linguistics: EMNLP 2023, Association for Computational Linguistics, Singa-
     pore, 2023, pp. 9164–9175. URL: https://aclanthology.org/2023.
     findings-emnlp.614. doi:10.18653/v1/2023.findings-emnlp.
     614.
[21] K. Pei, D. Bieber, K. Shi, C. Sutton, P. Yin, Can large language models reason
     about program invariants?, in: Proceedings of the 40th International Conference
     on Machine Learning, volume 202 of Proceedings of Machine Learning Research,
     PMLR, Honolulu, Hawaii, USA, 2023, pp. 27496–27520. URL: https://
     proceedings.mlr.press/v202/pei23a.html.
[22] C. Wen, J. Cao, J. Su, Z. Xu, S. Qin, M. He, H. Li, S.-C. Cheung, C. Tian,
     Enchanting program specification synthesis by large language models using static
     analysis and program verification, in: Computer Aided Verification, Springer
     Nature Switzerland, Cham, 2024, pp. 302–328.
[23] C. Liu, X. Wu, Y. Feng, Q. Cao, J. Yan, Towards general loop invariant generation:
     A benchmark of programs with memory manipulation, 2024. URL: https:
     //arxiv.org/abs/2311.10483. arXiv:2311.10483.
[24] A. Kamath, A. Senthilnathan, S. Chakraborty, P. Deligiannis, S. K. Lahiri, A. Lal,
     A. Rastogi, S. Roy, R. Sharma, Finding inductive loop invariants using large
     language models, 2023. URL: https://arxiv.org/abs/2311.07948.
     arXiv:2311.07948.
[25] P. Liu, W. Yuan, J. Fu, Z. Jiang, H. Hayashi, G. Neubig, Pre-train, prompt,
     and predict: A systematic survey of prompting methods in natural language
     processing, ACM Comput. Surv. 55 (2023). URL: https://doi.org/10.
     1145/3560815. doi:10.1145/3560815.
[26] J. Wei, X. Wang, D. Schuurmans, M. Bosma, b. ichter, F. Xia, E. Chi, Q. V.
     Le, D. Zhou, Chain-of-thought prompting elicits reasoning in large language
     models, in: S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, A. Oh
     (Eds.), Advances in Neural Information Processing Systems, volume 35, Curran
     Associates, Inc., Louisiana, United States, 2022, pp. 24824–24837. URL: https:
     //proceedings.neurips.cc/paper_files/paper/2022/file/
     9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf.
[27] S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, K. Narasimhan, Tree
     of thoughts: Deliberate problem solving with large language models, in:
     A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, S. Levine (Eds.),


                                          22
     Advances in Neural Information Processing Systems, volume 36, Curran
     Associates, Inc., New Orleans, LA, USA, 2023, pp. 11809–11822. URL: https:
     //proceedings.neurips.cc/paper_files/paper/2023/file/
     271db9922b8d1f4dd7aaef84ed5ac703-Paper-Conference.pdf.
[28] C. Yang, X. Wang, Y. Lu, H. Liu, Q. V. Le, D. Zhou, X. Chen, Large language
     models as optimizers, in: The Twelfth International Conference on Learning
     Representations, OpenReview.net, Messe Wien Exhibition and Congress Center,
     Vienna Austria, 2024, pp. 1–41. URL: https://openreview.net/forum?
     id=Bb4VGOWELI.
[29] Thinklab-SJTU, Lig-mm, 2023. URL: https://github.com/
     Thinklab-SJTU/LIG-MM/tree/main, accessed: 2024-07-26.
[30] D. Beyer, State of the art in software verification and witness validation: Sv-
     comp 2024, in: B. Finkbeiner, L. Kovács (Eds.), Tools and Algorithms for the
     Construction and Analysis of Systems, Springer Nature Switzerland, Cham, 2024,
     pp. 299–329.

[31] SoSy-Lab, Sv-comp 2024, 2024. URL: https://gitlab.com/sosy-lab/
     benchmarking/sv-benchmarks/tree/svcomp24, accessed: 2024-07-
     06.
[32] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N.
     Gomez, L. u. Kaiser, I. Polosukhin,  Attention is all you need, in:
     Advances in Neural Information Processing Systems, volume 30, Cur-
     ran Associates, Inc., Long Beach, CA, USA, 2017, pp. 5998–6008.
     URL: https://proceedings.neurips.cc/paper_files/paper/
     2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf.
[33] J. Devlin, M.-W. Chang, K. Lee, K. Toutanova, BERT: Pre-training of deep
     bidirectional transformers for language understanding, in: Proceedings of the
     2019 Conference of the North American Chapter of the Association for Compu-
     tational Linguistics: Human Language Technologies, Volume 1 (Long and Short
     Papers), Association for Computational Linguistics, Minneapolis, Minnesota,
     2019, pp. 4171–4186. URL: https://aclanthology.org/N19-1423.
     doi:10.18653/v1/N19-1423.

[34] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal,
     A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss,
     G. Krueger, T. Henighan, R. Child, A. Ramesh, D. Ziegler, J. Wu, C. Win-
     ter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark,
     C. Berner, S. McCandlish, A. Radford, I. Sutskever, D. Amodei, Language
     models are few-shot learners, in: Advances in Neural Information Processing
     Systems, volume 33, Curran Associates, Inc., virtual, 2020, pp. 1877–1901.
     URL: https://proceedings.neurips.cc/paper_files/paper/
     2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf.



                                        23
[35] FFmpeg, Ffmpeg, 2023. URL: https://github.com/FFmpeg/FFmpeg,
     accessed: 2024-07-26.
[36] J. Reynolds, Separation logic: a logic for shared mutable data structures, in:
     Proceedings 17th Annual IEEE Symposium on Logic in Computer Science,
     IEEE, Copenhagen, Denmark, 2002, pp. 55–74. doi:10.1109/LICS.2002.
     1029817.
[37] D. Beyer, Progress on software verification: Sv-comp 2022, in: Tools and
     Algorithms for the Construction and Analysis of Systems, Springer International
     Publishing, Cham, 2022, pp. 375–402.
[38] T. C. Le, G. Zheng, T. Nguyen, Sling: using dynamic analysis to infer
     program invariants in separation logic, in: Proceedings of the 40th ACM
     SIGPLAN Conference on Programming Language Design and Implementa-
     tion, PLDI 2019, Association for Computing Machinery, New York, NY,
     USA, 2019, p. 788–801. URL: https://doi.org/10.1145/3314221.
     3314634. doi:10.1145/3314221.3314634.

[39] M. Patnaik, frama-c-problems, 2023. URL: https://github.com/
     manavpatnaik/frama-c-problems, accessed: 2024-07-06.
[40] R. Alur, D. Fisman, S. Padhi, R. Singh, A. Udupa, Sygus-comp 2018: Re-
     sults and analysis, 2019. URL: https://arxiv.org/abs/1904.07146.
     arXiv:1904.07146.

[41] I. Dillig, T. Dillig, B. Li, K. McMillan, Inductive invariant generation via abductive
     inference, SIGPLAN Not. 48 (2013) 443–456. URL: https://doi.org/10.
     1145/2544173.2509511. doi:10.1145/2544173.2509511.
[42] I. Dillig, T. Dillig, B. Li, K. McMillan, Inductive invariant generation via ab-
     ductive inference, in: Proceedings of the 2013 ACM SIGPLAN International
     Conference on Object Oriented Programming Systems Languages &amp; Applica-
     tions, OOPSLA ’13, Association for Computing Machinery, New York, NY,
     USA, 2013, p. 443–456. URL: https://doi.org/10.1145/2509136.
     2509511. doi:10.1145/2509136.2509511.
[43] E. Nijkamp, H. Hayashi, C. Xiong, S. Savarese, Y. Zhou, Codegen2: Lessons
     for training llms on programming and natural languages, 2023. URL: https:
     //arxiv.org/abs/2305.02309. arXiv:2305.02309.
[44] X. Si, A. Naik, H. Dai, M. Naik, L. Song, Code2inv: A deep learning framework
     for program verification, in: Computer Aided Verification, Springer International
     Publishing, Cham, 2020, pp. 151–164.

[45] C. Wen, Y. Cai, B. Zhang, J. Su, Z. Xu, D. Liu, S. Qin, Z. Ming, T. Cong,
     Automatically inspecting thousands of static bug warnings with large language
     model: How far are we?, ACM Trans. Knowl. Discov. Data 18 (2024). URL:
     https://doi.org/10.1145/3653718. doi:10.1145/3653718.


                                           24
[46] Z. Li, S. Dutta, M. Naik, Llm-assisted static analysis for detecting secu-
     rity vulnerabilities, 2024. URL: https://arxiv.org/abs/2405.17238.
     arXiv:2405.17238.
[47] A. Yadavally, Y. Li, S. Wang, T. N. Nguyen, A learning-based approach to
     static program slicing, Proc. ACM Program. Lang. 8 (2024). URL: https:
     //doi.org/10.1145/3649814. doi:10.1145/3649814.
[48] R. Bairi, A. Sonwane, A. Kanade, V. D. C., A. Iyer, S. Parthasarathy, S. Raja-
     mani, B. Ashok, S. Shet, Codeplan: Repository-level coding using llms and
     planning, Proc. ACM Softw. Eng. 1 (2024). URL: https://doi.org/10.
     1145/3643757. doi:10.1145/3643757.

[49] F. Mu, L. Shi, S. Wang, Z. Yu, B. Zhang, C. Wang, S. Liu, Q. Wang, Clarifygpt:
     A framework for enhancing llm-based code generation via requirements clarifica-
     tion, Proc. ACM Softw. Eng. 1 (2024). URL: https://doi.org/10.1145/
     3660810. doi:10.1145/3660810.
[50] S. Kang, G. An, S. Yoo, A quantitative and qualitative evaluation of llm-based
     explainable fault localization, Proc. ACM Softw. Eng. 1 (2024). URL: https:
     //doi.org/10.1145/3660771. doi:10.1145/3660771.
[51] P. Cousot, R. Cousot, Abstract interpretation: a unified lattice model for static anal-
     ysis of programs by construction or approximation of fixpoints, in: Proceedings of
     the 4th ACM SIGACT-SIGPLAN Symposium on Principles of Programming Lan-
     guages, POPL ’77, Association for Computing Machinery, New York, NY, USA,
     1977, p. 238–252. URL: https://doi.org/10.1145/512950.512973.
     doi:10.1145/512950.512973.
[52] K. L. McMillan, Interpolation and sat-based model checking, in: Computer Aided
     Verification, Springer Berlin Heidelberg, Berlin, Heidelberg, 2003, pp. 1–13.

[53] S. Magill, A. Nanevski, E. M. Clarke, P. Lee, Inferring invariants in separa-
     tion logic for imperative list-processing programs, in: Conference Record of
     the 33rd ACM SIGPLAN-SIGACT Symposium on Principles of Programming
     Languages, Association for Computing Machinery, New York, NY, USA, 2006,
     pp. 47–60. URL: https://software.imdea.org/~aleks/papers/
     separation/separation.pdf.

[54] S. Magill, M.-H. Tsai, P. Lee, Y.-K. Tsay, Thor: A tool for reasoning about shape
     and arithmetic, in: Computer Aided Verification, Springer Berlin Heidelberg,
     Berlin, Heidelberg, 2008, pp. 428–432.
[55] S. Magill, M.-H. Tsai, P. Lee, Y.-K. Tsay, Automatic numeric abstrac-
     tions for heap-manipulating programs, in: Proceedings of the 37th Annual
     ACM SIGPLAN-SIGACT Symposium on Principles of Programming Lan-
     guages, POPL ’10, Association for Computing Machinery, New York, NY,
     USA, 2010, p. 211–222. URL: https://doi.org/10.1145/1706299.
     1706326. doi:10.1145/1706299.1706326.


                                            25
[56] S. Magill, M.-H. Tsai, P. Lee, Y.-K. Tsay,    Automatic numeric ab-
     stractions for heap-manipulating programs, SIGPLAN Not. 45 (2010)
     211–222. URL: https://doi.org/10.1145/1707801.1706326.
     doi:10.1145/1707801.1706326.
[57] H. Illous, M. Lemerre, X. Rival, A relational shape abstract domain, in: NASA
     Formal Methods, Springer International Publishing, Cham, 2017, pp. 212–229.
[58] R. Sharma, A. Aiken, From invariant checking to invariant inference using
     randomized search, in: Computer Aided Verification, Springer International
     Publishing, Cham, 2014, pp. 88–105.
[59] P. Garg, D. Neider, P. Madhusudan, D. Roth,            Learning invari-
     ants using decision trees and implication counterexamples,   SIGPLAN
     Not. 51 (2016) 499–512. URL: https://doi.org/10.1145/2914770.
     2837664. doi:10.1145/2914770.2837664.
[60] J. Yao, G. Ryan, J. Wong, S. Jana, R. Gu, Learning nonlinear loop in-
     variants with gated continuous logic networks, in: Proceedings of the 41st
     ACM SIGPLAN Conference on Programming Language Design and Imple-
     mentation, PLDI 2020, Association for Computing Machinery, New York, NY,
     USA, 2020, p. 106–120. URL: https://doi.org/10.1145/3385412.
     3385986. doi:10.1145/3385412.3385986.




                                       26
