Software and Systems Modeling (2024) 23:289–315
https://doi.org/10.1007/s10270-023-01144-y

    SPECIAL SECTION PAPER



A framework for embedded software portability and verification:
from formal models to low-level code
Renata Martins Gomes1 · Bernhard Aichernig1                    · Marcel Baunach1

Received: 3 June 2022 / Revised: 20 September 2023 / Accepted: 12 December 2023 / Published online: 1 February 2024
© The Author(s) 2024


Abstract
Porting software to new target architectures is a common challenge, particularly when dealing with low-level functionality in
drivers or OS kernels that interact directly with hardware. Traditionally, adapting code for different hardware platforms has
been a manual and error-prone process. However, with the growing demand for dependability and the increasing hardware
diversity in systems like the IoT, new software development approaches are essential. This includes rigorous methods for
verifying and automatically porting Real-Time Operating Systems (RTOS) to various devices. Our framework addresses this
challenge through formal methods and code generation for embedded RTOS. We demonstrate a hardware-specific part of a
kernel model in Event-B, ensuring correctness according to the specification. Since hardware details are only added in late
modeling stages, we can reuse most of the model and proofs for multiple targets. In a proof of concept, we refine the generic
model for two different architectures, also ensuring safety and liveness properties. We then showcase automatic low-level
code generation from the model. Finally, a hardware-independent factorial function model illustrates more potential of our
approach.

Keywords Embedded systems · RTOS · Formal methods · Event-B · Verification · Code generation · Portability


1 Introduction                                                             variety of devices, ranging from simple single-core to more
                                                                           complex multi-core or many-core systems, including special-
The amount of computing devices in the Internet of Things                  ized ASIC or even reconfigurable FPGA components [19,
(IoT) (in, e.g., autonomous vehicles, smart infrastructures,               29].
automated homes, and production facilities), is expected to                   While high-level code can more easily be compiled for
increase exponentially, along with the diversity on both the               a new or different hardware, low-level functionality (i.e.,
hardware (HW) and the software (SW) side [23, 32]. Oper-                   context switches, system initialization routines, interrupt
ating System (OS) developers, who currently focus on just                  handling) are still handwritten for each architecture. To sup-
a couple of different computing platforms, will face a huge                port a new instruction set architecture, for example, an OS
                                                                           must have many low-level parts completely rewritten, which
Communicated by Antonio Cerone and Frank de Boer.                          requires in-depth knowledge of both software and hardware,
Note: This paper results from a combination of [27], a publication that
                                                                           including a deep understanding of their interaction. From our
led to the invitation for this special section, and our subsequent paper   own experience and industry cooperation, supporting addi-
[28]. We have significantly extended the content with unpublished          tional MCU families or just variants is not straightforward,
work, including a new example and more details on how code is              even if there are only a few differences to existing ports [53].
generated from formal models.
                                                                           This increases the development time, often limiting OS sup-
B Marcel Baunach                                                           port to a low number of devices. Even though the code base
     baunach@tugraz.at                                                     of many OSs is modular, there are noticeably often just a few
     Renata Martins Gomes                                                  complete and directly usable ports available. Especially when
     renatamgomes12@gmail.com                                              developed under time pressure, faulty implementations, new
     Bernhard Aichernig                                                    bugs, and security holes are common. Besides, changes in
     aichernig@ist.tugraz.at                                               the logic of low-level software must be manually introduced
1    Graz University of Technology, Graz, Austria


                                                                                                                                123
290                                                                                                               R. M. Gomes et al.


to all implementations, which also hinders or slows down           detailing the operations that happen during these transitions.
important improvements of the OS.                                  We chose the context switch as demonstrating example,
    These difficulties in porting software clearly signal that     because it is architecture-specific, typically requires reim-
new approaches must be sought to make the porting process          plementation for each new architecture, and its correctness
easier and more reliable. This would not only increase the         is crucial: corrupted task contexts, resulting from incorrect
number of supported platforms, but could also have a pos-          implementations, may produce errors that are hard to find
itive impact in the quality of ports, reduce costs, and even       and compromise the OS’s ability to properly interleave con-
open new horizons on software evolution. As an example,            currently running tasks.
model-driven software development has been largely used in             First, we model the OS execution flow and functionality
the embedded software industry. It can improve quality while       incrementally through formal refinements. Then, as a proof
reducing costs and development time. Simple sketches and           of concept, we further refine the generic OS model to two dif-
more elaborate modeling approaches, such as UML, are very          ferent architectures: MSP430 and RISC-V. In order to verify
common [4], and formal modeling approaches are gaining             safety (something bad must not happen) and liveness (some-
traction since a while. Formal methods have been experi-           thing good should eventually happen) properties [44], we
mented on software development, bringing a new perspective         (1) prove that our RTOS models do not corrupt any task’s
and showing that considerable improvements with respect            context by properly saving and loading them, even though
to correctness proofs and verification can be achieved [46,        the process for saving and restoring a context differs for dif-
82]. Despite several obstacles regarding their applicability for   ferent MCU architectures; (2) prove that the kernel runs in the
complex real-world systems [57], industry has been success-        appropriate CPU state and changes it as specified for task exe-
fully exploring the benefits of introducing formal methods to      cution; (3) prove that the kernel executes in the correct order
their development processes [11, 79]. Such methods have            and eventually finishes execution. Since we only introduce
been used for specification and verification, and also for         hardware details in late refinements, most of those proofs
testing and code generation [7]. Even for OS development,          need only be done once, on the generic RTOS model. The
several works apply formal methods with great and promis-          late refinement to each architecture, as well as their proofs
ing results on, e.g., functional safety and security [31, 42,      follow and become much simpler, as we will show.
84].                                                               The second part of our approach addresses a research ques-
    However, to the best of our knowledge, no one has tried        tion on code generation: RQ2: How can low-level software be
to use formal methods to do verification and to improve            engineered to be more portable to different hardware archi-
software portability at the same time for embedded system          tectures?
software, such as OS in, e.g., the IoT. We propose a change of         The methodology is based on using the verified mod-
perspective to what software development is, which has the         els from the first part as an input to EB2LLVM, a tool
potential of not only improving portability, but also overall      that resulted from our research and automatically generates
maintainability and dependability. While this is a big chal-       LLVM intermediate code which is eventually compiled with
lenge and an ongoing work, we have investigated a novel            a target-specific compiler backend. To demonstrate how code
OS development framework based on formal methods and               is generated from Event-B models, we first present another
code generation. This paper presents the framework and its         model, applying the entire framework on the generally known
concepts, along with a proof of concept that shows how an          high-level algorithm to calculate the factorial of a number.
OS context switch can be modeled in a generic way and how          The factorial example presents EB2LLVM’s basic features,
the code can still be automatically generated for two different    and all stages of code generation for the same target archi-
target architectures. Besides the low-level context-switch, we     tectures as for the OS model, i.e., MSP430 and RISC-V. We
have also applied the framework on a high-level mathemat-          also compare the automatically generated code with equiva-
ical function that calculates the factorial of a given number.     lent code compiled from the function implemented in C.
This demonstrates that our framework is not limited to low-            Finally, we show how EB2LLVM generates code from the
level OS functionality, and can potentially be applied to a        presented OS model, including register and array accesses,
wide range of software functionality.                              and, step-by-step, how generic parts of the OS model can
The first part of our approach addresses a research ques-          generate target-specific code considering the target’s hard-
tion on verifying low-level functionality. RQ1: How can            ware model.
low-level software development support guaranteed depend-          Contributions. To the best of our knowledge, this is the first
ability while not undermining portability?                         time that OS low-level functionality is formally modeled
    The methodology is based on incrementally refined formal       with focus on its portability, and code is automatically gen-
models to prove safety and liveness properties. We present         erated for two targets. Our main contributions in this paper
parts of the model of an Real Time Operating System (RTOS)         are: (1) we decouple low-level functionality from hardware
that focus on the switch into the kernel and back to a task,       specifics; (2) a generic formal RTOS model with context


123
A framework for embedded software portability...                                                                              291


switches; (3) safety and liveness verification of two instanti-     use-case, however we have not further explored UML as a
ations of the generic model via interactive theorem proving         modeling language.
and model checking; (4) assembly code is automatically                 Automatic generation of code from formal models has
generated and compiled into binaries for the two model              also been investigated [6, 17, 54, 55, 65, 68]: However, the
instantiations; (5) a formal model of the factorial function,       state-of-the-art modeling approaches rarely take care of sep-
with its automatically generated code.                              arating software from hardware concepts. When high-level
Structure. Section 2 discusses related work and Sect. 3 pro-        functionality is modeled, this does not present an issue, and
vides background on the tools and the two target HW                 the model can be detailed enough that (high-level) code can
architectures. Section 4 presents an overview of the frame-         be generated and then compiled to different hardware plat-
work. Section 5 presents the first part of the framework,           forms. However, as soon as direct interaction with hardware
including the requirements, the general idea of the model-          is necessary, they either model it directly, which means that
ing process and our refinement strategy, the modeled RTOS,          the model does not or only with considerable effort work for
and its verification. The second part of the framework is pre-      different hardware; or they do not detail the model enough
sented in Sect. 6, with the model and code generation for           to be able to automatically generate any code from it. Such
the factorial example, and the code generation for the RTOS         generated high-level code does usually not support direct ref-
model presented in the first part. We conclude in Sect. 7.          erences to, e.g., CPU registers. Apart, corresponding tools
                                                                    like MATLAB [54] commonly lack built-in support for for-
                                                                    mal verification in the way dedicated formal methods tools
2 Related work                                                      like model checkers or theorem provers do. Even if, the
                                                                    verification effort must be repeated for each target, as the
Throughout the history of software development, portabil-           hardware-specific models largely differ. An exception in the
ity has been a difficult to tackle issue. Porting is a common       tooling landscape is AutoFOCUS [6] which comes with for-
source of bugs in drivers [14] and OSs in general [49, 61].         mal semantics, code generation and support for hardware
Code duplication, for example, is often difficult to maintain       deployment. However, AutoFOCUS has been designed for
and often leads to faults [24, 38, 39]. These problems can be       component-based development of embedded applications, its
tracked to the porting process itself [13, 34]. Several works on    focus is not on low-level and portable operating system devel-
porting experiences report difficulties in the low-level code       opment.
[69] and the need to consider several aspects of the target [58],      Finally, Holland [33] proposes an approach to synthesize
and often the ports miss some functionality [53, 83]. Even the      machine-specific OS assembly code by introducing a sub-
generally considered portable Linux and UNIX OSs present            stantial number of new specification languages and tools
important challenges [9, 41, 74, 75]. Solutions for improving       to handle compiler-specific and machine-specific calling
software portability in different domains have been proposed        conventions, data types, memory layouts, etc. While these
[48, 67]. Some works try to improve aspects of portability          languages are tailored to, e.g., the special requirements of
with formal methods and code generation [22, 60]. While             context switching, the verification step only considers the
the generated code is semantically hardware-dependent, low-         correct interaction between the assembly code and the C
level assembly code still cannot be generated.                      compiler that calls the generated sequences. The assembly
    Formal methods can also aid in OS verification, and sev-        code generation must be manually adjusted for each new
eral works investigate how to formally model and verify OSs         architecture.
[5, 10, 12, 15, 16, 18, 56, 71, 72]. The most known formally-          In contrast, our approach is to generate LLVM intermedi-
verified microkernel is probably sel4 [51], whose modeling          ate code from formal software and hardware models. We then
and verification strategies have been largely studied [42, 73].     use the standard compiler toolchain which ultimately gener-
OpenComRTOS [76] develops implementations from formal               ates low-level assembly code for a wide range of supported
models, though these implementations are still handwritten.         target architectures. Since the intermediate representation
It is also possible to formally specify an entire Instruction       language is unified, our code generation algorithm needs
Set Architecture (ISA) and automatically generate a simula-         no adaptation to new hardware. Apart, we allow to directly
tor for it [80, 81].                                                reuse the software model (along with already accomplished
    With modular UML models, Besnard et al.’s work [8]              proofs) for all target architectures by strictly separating it
decouples system and environment models, deploying the              from their hardware models. For a new hardware architec-
same system model for simulation, verification, and execu-          ture, only its hardware model and the instantiation needs to
tion. Also focused on the software deployment, Rivera et            be implemented and verified against the specification. This is
al. [64] present a tool that automates the transformation of        more efficient compared to implementing a new and mixed
Platform-Independent Models (PIMs) into Platform-Specific           hardware/software model for each new target architecture.
Models (PSMs). These approaches are interesting for our


                                                                                                                       123
292                                                                                                                R. M. Gomes et al.


3 Background

3.1 Event-B and Rodin

Event-B is a formal method for system-level modeling and
analysis [2, 21] derived from the B formalism [1]. Based on
set theory and state transitions, Event-B supports refinements
to model different abstraction levels, while mathematical            Fig. 1 : Visualization of the binary search Event-B model
proofs verify correctness and consistency between refine-
ments. The Rodin Platform [37], an Event-B IDE based on
Eclipse, supports the development and refinement of models          have a status, which can be either ordinary (default status,
with automatic generation and partial discharging of math-          the event may occur arbitrarily often), convergent (the event
ematical Proof Obligations (POs). POs are mathematical              must decrease the variant), or anticipated (the event must not
formulas that must be proved (discharged) to ensure correct-        increase the variant). When a machine refines another one, it
ness of the model. Several plugins are available to Rodin that      may introduce details or more variables. The machine events
aid in, e.g., automatic PO discharging and model checking.          must be refined or kept as they were. In special cases, when
    In order to ease the understanding of readers unfamiliar        the event can never be enabled, it may be deleted from the
with Event-B, we introduce the components of Event-B mod-           refined machine. POs define what is to be proved for a model
els and then present a model with most of these components          and are automatically generated by Rodin. For example, the
to show how they can model a sequential program. Listing            POs guarantee that invariants always hold and that refined
1 and Listing 2 present the model explained later, and can          events do not contradict abstract ones.
also be used as reference to the keywords and components               Listing 1 and Listing 2 reproduce an example from
explained next. We assume the reader is familiar with basic         Abrial’s book: the binary search in a sorted array (Section
set theory notation.                                                15.4 of [2]). We have only created a Rodin project and copied
    The two top elements of a model in Event-B are contexts         the Event-B model from the book into it, correcting some
and machines. The term context is overloaded in the domains         typos present in the original and discharging the POs Rodin
of OSs and formal methods. Hence, we will always refer to           generated. To complete our example here, we also added the
a context in Event-B as Event-B context. In contrast, just          Event-B context c1 (Listing 1b), which is not present in the
context refers to task context in operating systems. Event-B        original model. With this example, we can show Event-B’s
contexts describe all static information about the system and       notation and model components, as well as some concepts
can have carrier sets and constants. Axioms are the predicates      for modeling sequential programs introduced by Abrial and
that the constants obey and will be available as hypotheses         used in our models. In this model, we only have four events
in the POs. It is also possible to add theorems which must be       and the state is composed of a few variables. Still, it can
proved. If an Event-B context extends others, it can reference      be challenging to understand how state transitions occur and
sets and constants of the extended Event-B contexts and any         which effect events may have on each other. Therefore, it is
they also extend. Dynamic information about the system is           helpful to visualize the model graphically. Many tools can
described in the machines. A machine can see Event-B con-           create visualizations from Event-B models, producing intri-
texts, such that it can use their sets and constants to relate      cate and detailed graphs. For the sake of simplicity, however,
static and dynamic information, as well as axioms and the-          we present simple state-machine-like graphs representing our
orems to discharge POs. Machines can have variables that            models. As an example, Fig. 1 presents a visualization of the
obey predicates given by their invariants, and theorems can         concrete Event-B model of the binary search. The nodes rep-
be added and proved. Considering machine states as sets of          resent the events’ guards, and edges represent the possible
the variables’ values, each event represents a state transition.    state transitions caused by their actions when they execute.
An event is said to be enabled if the state satisfies its guard     The dashed boxes are the guard expressions defining the state
condition. The mandatory event INITIALISATION serves as             that enables the respective event.
a starting point, has no guards, and only runs once to initialize      Listing 1a shows the Event-B context with the binary
all variables. Event-B does not define which event will be exe-     search pre-conditions: f is an array of natural numbers with
cuted in case more than one is enabled simultaneously. The          size n, and v is a value in the range of f (i.e., an element of
execution of an event modifies the current state according to       the array). The program (modeled in the machine, explained
its actions, which are executed simultaneously. It is possible      later) will search for the index r in the array, such that f(r)
to limit how often an event may be enabled using a variant,         = v. The axiom axm0_4 tells us that the array f is sorted in
which is either a numeric expression or a finite set whose free     a non-decreasing way, and the theorem thm0_1 states that
identifiers are constants or concrete variables. Events always      there is at least one element in the array. Listing 1b is not


123
A framework for embedded software portability...                                                                                  293


 1 C O N T E X T c0
 2 CONSTANTS
 3     n
 4     f                                                           1 M A C H I N E m0
 5     v                                                           2 SEES c0
 6 AXIOMS                                                          3 VARIABLES
 7     axm0_1 : n ∈ N                                              4     r
 8     a x m 0 _ 2 : f ∈ (1..n )→N                                 5 INVARIANTS
 9     a x m 0 _ 3 : v ∈ ran ( f )                                 6     inv0_1 : r ∈ N
10     thm0_1 : n ≥ 1 theorem                                      7 EVENTS
11     a x m 0 _ 4 : ∀ i , j · i ∈ 1..n ∧ j ∈ 1..n                 8 INITIALISATION
         ∧ i ≤ j ⇒ f(i) ≤ f(j)                                     9     THEN
12 END                                                            10       a c t 0 _ i n i t _ 1 : r :∈ N
                                                                  11     END
            (a) Event-B context c0 – pre-conditions               12 p r o g r e s s a n t i c i p a t e d
                                                                  13     THEN
 1 C O N T E X T c1                                               14       a c t 0 _ p r o g _ 1 : r :∈ N
 2 E X T E N D S c0                                               15     END
 3 SETS                                                           16 f i n a l
 4     S                                                          17     WHERE
 5 CONSTANTS                                                      18       g r d 0 _ f i n _ 1 : r ∈ 1..n
 6     s1                                                         19       grd0_fin_2 : f(r) = v
 7     s2                                                         20     THEN
 8     s3                                                         21       skip
 9 AXIOMS                                                         22     END
10     nProB : n = 5                                              23 END
11     v P r o B : v < 10
12     s e t D e f : partition(S, {s1}, {s2}, {s3})                       (c) Event-B machine m0 – post-condition and progress
13 END

                 (b) Event-B context c1 – extends c0

                                       Listing 1: Binary search as Event-B model – initial model


part of the model. However, it shows how an Event-B con-             grd0_fin_1 in final of Listing 1c always holds and can
text can extend another to use (and further detail) elements         therefore be removed from the refined machine m1. The sec-
of the extended context, for example, defining the size n of         ond refinement m2 (Listing 2b) defines how r is to be found
the array f. It also defines a carrier set S and new constants.      within inc and dec, defining the increment and decrement
The axiom setDef defines S as a partition of three subsets           intervals that were non-deterministic in m1. Note that, since
with one element each, effectively creating an enumerated set        event final remains exactly the same as its abstraction,
of three elements. The machine of the initial model (Listing         its guard is omitted and the word REFINES is replaced by
1c) sees the Event-B context c0 and declares the variable            EXTENDS. The goal state is still f(r) = v.
r, which represents the index that the program must find.                While we assume the reader is familiar with basic set the-
Besides the mandatory INITIALISATION event, we add two               ory, our models use some set and relation operators that are
others. Event final represents the specification of the pro-         less generally known. To ensure understanding of the models,
gram, i.e., its post-condition. It has no actions (skip), and        we explain the meaning of these operators with an example.
its guards represent the state where the program has found           Listing 3 defines two sets, S1 and S2, where S2 is a subset
r. Note that axm0_3 states that v is in the range of f, guar-        of S1. The set S1 is a partition of constants a to e (definition
anteeing the program will find r. The other event we add             omitted for simplicity). A relation r is a set of pairs where
is the anticipated event progress, which modifies r in a             its domain dom(r) is the set of all elements occurring on
non-deterministic way. Its refinements will detail how r is          the left side of the pairs and its range ran(r) is the set of
to be found and will eventually be made convergent on a              elements on the right side. A function is a special case of rela-
variant, such that the loop it creates is guaranteed to termi-       tion, where each element of the domain is uniquely related to
nate eventually. In the first refinement m1 (Listing 2a), two        one element of the range. The two relations defined in List-
new variables, p and q, are introduced, representing search          ing 3, r1 and r2, are partial functions from, respectively, S1
indexes of the array f. The abstract event progress is split         and S2 to N. Table 1 shows the values in each relation range.
into events inc and dec, which are made convergent on the            Columns r1 and r2 show the range values defined for these
variant q −p. Since inv1_3 has been introduced, the guard            relations, each cell representing the value mapped to the cor-


                                                                                                                            123
294                                                                                                                R. M. Gomes et al.


 1 M A C H I N E m1
 2 R E F I N E S m0
 3 SEES c0
 4 VARIABLES
 5     r
                                                                          1 M A C H I N E m2
 6     p
                                                                          2 R E F I N E S m1
 7     q
                                                                          3 SEES c0 // c1 for e x t e n d e d
 8 INVARIANTS
                                                                          4 VARIABLES
 9     i n v 1 _ 1 : p ∈ 1..n
                                                                          5     r
10     i n v 1 _ 2 : q ∈ 1..n
                                                                          6     p
11     i n v 1 _ 3 : r ∈ p..q
                                                                          7     q
12     i n v 1 _ 4 : v ∈ f [ p..q ]
                                                                          8 EVENTS
13 V A R I A N T
                                                                          9 INITIALISATION
14 q−p
                                                                         10     THEN
15 E V E N T S
                                                                         11       a c t 2 _ i n i t _ 1 : r := (1+n )/2
16 I N I T I A L I S A T I O N
                                                                         12       a c t 2 _ i n i t _ 2 : p := 1
17     THEN
                                                                         13       a c t 2 _ i n i t _ 3 : q := n
18       a c t 1 _ i n i t _ 1 : r :∈ 1..n
                                                                         14     END
19       a c t 1 _ i n i t _ 2 : p := 1
                                                                         15 inc
20         a c t 1 _ i n i t _ 3 : q := n // typo : q := 1
                                                                         16     R E F I N E S inc
21     END
                                                                         17     WHERE
22 inc c o n v e r g e n t
                                                                         18       grd2_inc_1 : f(r) < v
23     REFINES progress
                                                                         19     THEN
24     WHERE
                                                                         20       a c t 2 _ i n c _ 1 : r := ( r+1+q )/2
25       grd1_inc_1 : f(r) < v
                                                                         21       a c t 2 _ i n c _ 2 : p := r+1
26     THEN
                                                                         22     END
27       a c t 1 _ i n c _ 1 : r :∈ r+1..q
                                                                         23 dec
28       a c t 1 _ i n c _ 2 : p := r+1
                                                                         24     R E F I N E S dec
29     END
                                                                         25     WHERE
30 dec c o n v e r g e n t
                                                                         26       grd2_dec_1 : v < f(r)
31     REFINES progress
                                                                         27     THEN
32     WHERE
                                                                         28       a c t 2 _ d e c _ 1 : r := ( p+r−1)/2
33       grd1_dec_1 : v < f(r)
                                                                         29       a c t 2 _ d e c _ 2 : q := r−1
34     THEN
                                                                         30     END
35         a c t 1 _ d e c _ 1 : r :∈ p..r−1
                                                                         31 f i n a l
36       a c t 1 _ d e c _ 2 : q := r−1
                                                                         32     EXTENDS final
37     END
                                                                         33     THEN
38 f i n a l
                                                                         34       skip
39     REFINES final
                                                                         35     END
40     WHERE
                                                                         36 END
41       grd1_fin_2 : f(r) = v
42     THEN
43       skip                                                                             (b) Event-B machine m2
44     END
45 END

                          (a) Event-B machine m1

                           Listing 2: Binary search as Event-B model – first and second refinements


responding set element. If an element is not in the relation’s     S1 that are not in S2 (thm1). Brackets are used to access a
domain, the cell is marked with “-”. If it is, but there is no     relation element, as exemplified by thm2.
mapping for it in the relation the cell is left blank. The other
columns represent the result of some operations with r1:           3.2 Model checking and ProB
The domain subtraction S2   − r1 removes all S2 from r1’s
domain, leaving only two mapped values. Domain restric-            Temporal logic [52, 59] is a logic system that formally
tion S2  r1 is the inverse, only leaving values mapped            describes properties of time. Linear Temporal Logic (LTL) is
to elements present in S2. The overwrite operation r1 −           the most popular and widely used temporal logic in computer
r2 overwrites the r1 relation with values from r2. Finally,        science to specify and verify the correct behavior of reactive
Listing 3 also shows the results of two other operations as        and concurrent programs [30]. It is particularly useful for
theorems: S1 minus S2 results in a set with all elements from      expressing properties such as safety (given a precondition,


 123
A framework for embedded software portability...                                                                              295


Table 1 Relation operators and
                                      Set          r1       r2        Dom.Subtraction          Dom.Restriction          Overwrite
example values
                                      element                         S2 
                                                                         − r1                  S2  r1                  r1 − r2

                                      a            1        –         1                        –                        1
                                      b            3        –         3                        –                        3
                                      c            5        2         –                        5                        2
                                      d            7                  –                        7                        7
                                      e                     4         –                                                 4




  AXIOMS                                                         interrupt handler. The return from interrupt instruction, i.e.,
      // d e f i n i t i o n s                                   RETI, restores SR and PC from the stack and finally contin-
      d e f S 1 : partition(S1, {a}, {b}, {c}, {d}, {e})         ues where the handler has interrupted the regular execution
      d e f S 2 : S2 = { c , d , e }
                                                                 flow.
      t y p e R 1 : r1 ∈ S1 →N
      d e f R 1 : r1 = { a →1 , b →3 , c →5 , d →7}              RISC-V The open RISC-V instruction set architecture [63]
      t y p e R 2 : r2 ∈ S2 →N                                   was originally developed by UC Berkeley and is mean-
      d e f R 2 : r2 = { c →2 , e →4}                            while supported by a highly active community of software
      // t h e o r e m s that e x e m p l i f y o t h e r
                                                                 and hardware innovators with more than 100 members from
       operations
      thm1 : S1 \ S2 = { a , b } t h e o r e m                   industry and academia. The RISC-V is a load-store architec-
      thm2 : r1 ( a ) = 1             theorem                    ture, and its specification [78] defines privilege levels used
  END                                                            to provide protection between different components of the
                                                                 software stack. We refer to an implementation that supports
       Listing 3: Example of set and relation operators          user and machine modes, with 32-bit integer and multipli-
                                                                 cation/division instructions (RV32IM) [77]. There are 32
                                                                 registers available in all modes, including a zero register and
then undesirable states that violate the safety condition will   the program counter pc. The calling convention specifica-
never occur), liveness (given a precondition, then a desir-      tion assigns meanings to the other registers, such as a stack
able state will eventually be reached), and fairness (involves   pointer sp, function arguments and return values. Addition-
combinations of temporal patterns of the form a predicate        ally, Control and Status Registers (CSRs) with special access
holds “infinitely often” or “eventually always”). ProB is an     instructions are available for, e.g., managing the CPU or
animator, constraint solver, and model checker for the B-        accessing on-chip peripherals in defined privilege levels. An
Method [47] that integrates as a plugin-in Rodin and can be      IRQ switches the CPU into a higher privilege level, while
easily used for LTL model checking of our RTOS models.           software can issue an ECALL instruction for that. In both
                                                                 cases, returning to user level is done by the instruction URET.
3.3 Hardware architectures
                                                                 3.4 LLVM
Next, we present the main characteristics of the two HW
architectures we use as examples for the architecture-specific   The LLVM Compiler Infrastructure is a collection of com-
instantiations of our model in Sect. 5.3.                        piler and toolchain components designed as a set of reusable
MSP430 The TI MSP430 [36] family of MCUs comprises               libraries [50]. All components have well-defined interfaces,
a range of ultra-low power devices featuring 16 and 20-bit       and one of the most important aspects of LLVM for this paper
RISC architectures with a large variation of on-chip periph-     is the LLVM Intermediate Representation (LLVM IR). The
erals, depending on the variant. Among its 16 registers are      LLVM IR is a language with well-defined semantics and a
general purpose registers, the program counter PC, the stack     RISC-like virtual instruction set that supports simple instruc-
pointer SP, and the status register SR, which stores status      tions like add, subtract, compare, and branch. It is strongly
flags, such as interrupt enabled, overflow, etc. The MSP430      typed and uses an infinite set of temporary registers prefixed
offers a very simple architecture with only one execution        with a % character. LLVM IR is defined in three forms: a tex-
mode and a fully orthogonal instruction set. There is no         tual format of the language in .ll files, an in-memory data
privileged mode, nor any memory protection or memory             structure used by optimizers, and an on-disk binary “bitcode”
management unit. Once an interrupt occurs, the PC and            [45], with tools provided to transform one form into another.
SR registers are pushed onto the stack. Then, further inter-         An LLVM compiler has three distinct phases: the frontend
rupt requests (IRQs) are disabled and the PC is overwritten      is responsible for parsing the input code and translating it into
with the address of the first instruction of the corresponding   LLVM IR; this IR can then go through optimizers and ana-


                                                                                                                       123
296                                                                                                                 R. M. Gomes et al.


lyzers that improve the IR code; a backend finally produces
native machine code from the IR code. To take advantage of
the available LLVM backends (and eventually of some opti-
mizers and analyzers), we have written a frontend that takes
Event-B “code” and produces LLVM IR. We then use llc,
the LLVM static compiler, to produce architecture-specific
assembly code that can be used by a native assembler and
linker to generate native binaries.




4 Framework overview

Our approach relies on the separation of software function-
ality from details of the hardware platform on which this
functionality shall run. The idea is to (formally) model the                       Fig. 2 : Framework overview
functionality (i.e., the OS we want to implement), abstracting
away the hardware details that would render the model spe-
cific to a certain target platform, such as registers, interrupt       In our framework, software and hardware are modeled
handling, memory specifications, etc.                              and verified with Event-B, a formal method for system-level
    We can think of this as explaining someone else what the       modeling and analysis [2]. Code is then generated with a
code they should implement must do. We can explain func-           tool (EB2LLVM) that resulted from our research and parts
tionality in an abstract way, such that others (e.g., experts)     of the LLVM compiler infrastructure, taking advantage of
can presumably “understand” what is to be done, without            the backend targets that are already available.
the need to know all the details of the code. For instance,            As usual in formal modeling, the software model starts
in order to support concurrent tasks, a preemptive OS must         from a very abstract view of the modeled software, and
implement context switches, i.e., it must save the currently       is incrementally refined to describe all requirements. The
running task’s runtime information and load the next one’s         refinements integrate, step by step, the software require-
into the CPU. Experts will probably assume that this can           ments, and we also add invariants that guarantee correctness.
be implemented using interrupts, and that the interrupt con-       We also use model checking to verify liveness properties,
troller will save the return address of an interrupted code        and find errors, inconsistencies, or underspecification prob-
sequence somewhere. It might change some CPU configura-            lems early in the modeling, so that they can be fixed in early
tion, such as the ability to take further interrupts, the stack,   phases of the modeling and will not become bugs in the code.
its execution mode, etc., saving the previous values as well.      Since instantiations are nothing more than late refinements of
Finally, it will start executing another defined code sequence     the generic model to arch-specific models, their verification
(e.g., the handler specified for that interrupt). To understand    also profits from the verified generic model, and is almost
the general idea of a context switch, we do not need to know       automatic. Other aspects to be verified, such as timing, secu-
exactly which and how registers are modified, or how they          rity, functional safety, etc. could also be added to the models,
might be saved. When we implement the OS context switch,           and similarly verified at both the generic and the hardware-
we know we must save the “rest" of the context that is not         specific levels. This, however, is part of future work.
automatically saved by the hardware, and change the remain-            Once the software is modeled and verified, it can be easily
ing CPU configuration according to what the OS needs it to         instantiated to different targets, verified again, and the corre-
be.                                                                sponding code automatically generated. When the software
    What we do in our approach is to formalize this abstract       must be ported to a new hardware (e.g., a new architecture),
description, especially about low-level functionality. Figure 2    one only needs to create or adapt the hardware model, instan-
shows an overview of the framework: While the software             tiate the generic software model and verify/generate again.
model has a very abstract view of the hardware, these              While manual porting requires the OS developer to have deep
specifics are separately modeled for each target architecture      knowledge of both software and hardware, creating a hard-
in the hardware models. They are then combined (instanti-          ware model with just the details required for applying our
ated) into architecture-specific models, from which our code       approach is much simpler, as described in Sect. 5.3.2. If OS
generator can generate each target’s specific code. In addi-       requirements change, new features are needed, or the logic
tion, the models are verified through formal proofs, and most      must be changed, one only needs to change the generic OS
of these proofs are reused to verify each arch-specific model.     model, verify the changes, and generate the code again for


123
A framework for embedded software portability...                                                                              297


all targets. This can even accelerate the process of optimiz-      by loading their respective context. To be able to continue
ing the software design, as different options can be quickly       an earlier code sequence from the interrupted instruction, its
evaluated on real hardware, without the need for the software      context is saved before the switch. The actual switching pro-
developer to apply the change to all ports individually. It also   cess as well as the composition of the contexts is defined by
guarantees that the ports are always consistent to each other      the interrupt concept of the CPU; in any case, the hardware
and according to the requirements.                                 automatically saves and loads the contexts. If, in addition to
   Finally, to complete our approach to portability, code is       interrupts of the hardware, an OS supports preemptive, i.e.,
automatically generated from the models. While our frame-          interleaved executable tasks (or threads or processes), the
work aims at generating all code for the models, including         context is extended. In order to switch between tasks, this
linker files, generic and specific C code, etc., this paper        extended information is saved (previous task) and loaded
focuses on the low-level functionality. For the context switch     (next task) by the kernel. Next, we describe our general
that serves as proof-of-concept, we only generate assembly         assumptions about the computing platform and present Smar-
code. The tool we have written, EB2LLVM, takes as input            tOS’s requirements.
the Event-B models, and generates target-specific LLVM IR.
The LLVM IR files generated by EB2LLVM can then be                 5.1.1 Hardware assumptions
compiled with llc, LLVM’s static compiler. While other
Event-B code generators only understand basic arithmetics,         Even though we aim at keeping the OS model initially inde-
EB2LLVM also understands the model’s sets and axioms,              pendent from the hardware, a target architecture must have
such that they are used to generate low-level code that refers     certain general features in order to be capable of running
to target-specific registers and instructions. Taking advan-       an operating system. Focusing only on the relevant aspects
tage of LLVM’s backend, we can generate machine code for           for our RTOS model, we define data storage and interrupt
several different targets.                                         handling features as environmental assumptions, numbering
   The next sections present details of our framework. In          and labeling them env. Different OSs might require other
Sect. 5, we use the example of the context switch in SmartOS       features, but that does not affect our general concept.
[66], an RTOS we have developed and used for many years, to
show how the software can be modeled independently from            ENV1 The CPU provides means to store/load data to/from
the hardware, how it is later instantiated, and how the model is        referable locations. These locations can be, e.g., reg-
verified. Section 6 shows how we generate the context switch            isters or memory addresses.
and factorial code for RISC-V-based architectures [63] and         ENV2 The context is a well-defined subset of locations and
the MSP430 [36].                                                        their stored values that the CPU requires for execu-
                                                                        tion of a code sequence. It must be saved when the
                                                                        code sequence is interrupted, so that it can later be
5 Modeling                                                              resumed from the same point.
                                                                   ENV3 The CPU has an interrupt enabled flag. Interrupts will
This section presents the first part of the framework: mod-             only be accepted if the interrupt enabled flag is set.
eling and verification. Section 5.1 presents the requirements      ENV4 When an interrupt is accepted, the values of the con-
for the context switch and Sect. 5.2 shows the refinement               text or a part of it are automatically copied into other
strategy we used in the model. Section 5.3 details the generic          locations defined by the architecture.
model, while Sect. 5.3.2 presents the model instantiations to      ENV5 The CPU offers a “return from interrupt” instruc-
the target architectures. The verification we have done on this         tion that automatically loads the context with the
model is presented in Sect. 5.4.                                        values automatically saved when the interrupt was
                                                                        accepted (ENV4).
5.1 Requirements                                                   ENV6 The saving process (ENV4) is allowed to modify the
                                                                        context values before they are saved, according to a
We modeled SmartOS [66], an embedded RTOS we have                       well-defined and CPU-specific function.
developed and used for many years. This section summa-             ENV7 The restoring process (ENV5) must reverse the mod-
rizes its architecture and requirements. An important concept           ification of ENV6.
to understand is the context (not in the sense of Event-B, but
in the sense of operating systems): A context is a set of infor-   5.1.2 Software specification
mation and configuration of a CPU or a CPU core that is
required to control the execution flow of software, i.e., code     SmartOS provides, among many other features, a preemptive
sequences. Depending on the CPU state and external events,         and priority-based scheduler for concurrent tasks. The kernel
cores can usually switch between different code sequences          is invoked when an interrupt occurs or a syscall is called, and


                                                                                                                       123
298                                                                                                                    R. M. Gomes et al.


is divided into three parts: (1) the kernel entry is responsible                 Table 2 : Model and requirements
for stack management and context saving. It unites both entry
points, enters kernel mode, and continues to (2) the kernel        Level             ENV                        OS
body which handles the actual interrupt or syscall request         0                 ENV1, ENV2                 OS1
and runs the scheduler that selects the task to be executed
                                                                   1                 –                          OS2
next. Finally, (3) the kernel exit executes a context switch
                                                                   2                 ENV6, ENV7                 OS3, OS4
by loading the selected task’s context and returning to task
                                                                   3                 ENV3                       OS5, OS6
mode.
                                                                   4                 ENV4, ENV5                 OS7, OS8, OS9, OS10
   In this work, we only model the context switches in kernel
                                                                   5                 Target-specific            OS11
entry and exit, and the conditions required by the OS to exe-
cute its other functions. High-level kernel functionality, such
as scheduling, task management, etc. is out of scope. The
requirements for correct context switches and kernel execu-             those values into the task’s save context, and to copy
tion (os) are:                                                          them back where the CPU expects them to be when
                                                                        returning from an interrupt (ENV5).
 OS1 (A) A task executes on the context defined in ENV2.           OS11 If the architecture provides a privileged mode, ker-
     When not running, the values of its context are stored             nel body runs in it, while tasks run in less privileged
     in locations reserved for context saving. (B) Each ele-            modes. Switching the mode must be done on kernel
     ment of the context has its correspondent in the saved             entry and kernel exit.
     context.
 OS2 (A) Once the kernel is invoked, kernel entry saves the        5.2 Refinement strategy: from abstraction to
     old task’s context. (B) On kernel exit the next task’s            detailed specification
     context is loaded into the CPU.
 OS3 (A) Each task has dedicated locations for context sav-        The model has several refinements and showing all would be
     ing. (B) These locations with their stored values are         too cumbersome. So, we divide it into six levels of abstrac-
     the task’s saved context, where contexts are saved to         tion (referred to as Level). Each Level is composed of several
     and loaded from (OS2).                                        refinements and addresses a new set of requirements (Table
 OS4 The scheduler chooses the next task to be executed            2).1 Up to and including Level 4, the model remains generic,
     and is implemented in kernel body.                            only requiring the generic hardware features described in
 OS5 The cause for kernel invocation, unambiguously iden-          Sect. 5.1.1. We only introduce further hardware details in
     tifying which interrupt or syscall has occurred, must         Level 5, where we instantiate the model for specific target
     be recorded for use within the kernel body.                   architectures. This section introduces the general idea of each
 OS6 (A) The kernel body always runs in kernel mode, with          Level, while Sect. 5.3 details how each level was modeled.
     interrupts disabled, and on the OS stack. (B) Each task       This model focuses on the interface between hardware and
     runs on its own stack, with the interrupt flag being the      software in order to model the kernel’s interleaved execution
     same as it was when that task was running last, and           of concurrently running tasks. The goal is to prove that the
     never in kernel mode.                                         kernel does not corrupt any task’s context by properly saving
 OS7 A part of the kernel entry context-saving and CPU             and loading them, as well as to guarantee that tasks and ker-
     preparation is automatically executed by the hardware         nel body run in the appropriate conditions described by the
     (ENV4). The rest must be executed in software after           requirements from Sect. 5.1.
     the automatic part.                                              The state of an Event-B machine is the set of its variables’
 OS8 The kernel is exited with a return from interrupt             values, and state transitions are represented by the machine’s
     instruction (ENV5). The task selected by the sched-           events. In our model, these events represent the different parts
     uler shall continue execution where it was preempted          of the kernel, building a state machine that starts with the
     before.                                                       switch into the kernel and finishes with the switch back to
 OS9 A part of kernel exit context loading and CPU prepa-          a task. The events, therefore, are modeled such that their
     ration is automatically executed by the return from           order is well-defined, in the order the kernel parts must run:
     interrupt instruction (ENV5, OS8). The rest must be           kernel entry executes first, then body, and finally exit; and
     executed in software before the automatic part.               the automatic part of entry executes before the manual part
OS10 (A) If the values copied on interrupt (ENV4) are
     copied into task-specific locations, these locations and      1 Model artifact at https://figshare.com/s/0f262342284eada236f5. The
     their data are considered a part of the saved context.        relationship between refinements and levels can be found in the
     (B) Otherwise, it is the OS’s responsibility to save          README file. Model elements are referenced as [component.label].


123
A framework for embedded software portability...                                                                             299


that must be executed in software (OS7), and in exit manual
executes before automatic (OS9).

Level 0 In this initial abstraction, we only present the
        expected result of the OS execution, i.e., that an old
        context is saved and a new one is loaded, without
        modeling how this will be achieved. We also define
        the basic Event-B sets and their relations, used along
        the refinements.
Level 1 In the first refinements, we define the entry and exit
        parts of the kernel simply as two context copies: one
        in kernel entry for saving a context, and another one
        in kernel exit for loading a context. At this level, we
        do not yet define where those contexts are copied
        from or to, nor do we have any notion of tasks or
        conditions for proper task and kernel body execu-
        tion.
Level 2 Next, we introduce tasks, their saved contexts, and
        kernel body. This level also defines where the con-
        text is saved to and loaded from.
Level 3 Then, we introduce and set up the variables that con-                    Fig. 3 : Diagrams of LOCATION
        trol the conditions for proper task and kernel body
        execution (interrupts disabled, kernel mode, running
                                                                   1 EVENTS
        on its own stack, and cause for the kernel execution).     2 osProgress anticipated
Level 4 Here, we refine the model to a generic hardware            3 THEN
        that automatically saves and loads a subset of the         4   act1 : l o a d e d :∈ CONTEXT→DATA
        context, and the software that complements the             5   act2 : s a v e d :∈ SAVEDCTX→DATA
                                                                   6 END
        switches.                                                  7 osFinal
Level 5 Finally, we refine the model into architecture-            8 ANY
        specific models from which OS code can be gen-             9   new ∈ CONTEXT→DATA
        erated (See Sect. 6).                                     10   old ∈ SAVEDCTX→DATA
                                                                  11 W H E R E
                                                                  12   grd3 : l o a d e d = new
5.3 Context switch model                                          13   grd4 : s a v e d = old
                                                                  14 THEN
                                                                  15   skip // s t a t e not c h a n g e d
This section details the generic part of the context switch
model, i.e., Levels 0 to 4 from Sect. 5.2. Please, refer to
                                                                              Listing 4: Level 0 – Initial abstraction
Sect. 3.1 for the Event-B notation used in the following list-
ings.
                                                                   CONTEXT to DATA, while a saved context is a relation from
5.3.1 Hardware-independent model                                   SAVEDCTX to DATA.
                                                                      The initial abstraction (Listing 4), sees the context
Level 0 First, we define the carrier set LOCATION (Fig. 3a),       switches as two context copies: one copies old context to
an abstract representation of memory addresses and reg-            saved ∈ SAVEDCTX →DATA, and the other loads new context
isters. In combination with DATA, a subset of Z, memory            to loaded ∈ CONTEXT → DATA. The old and new contexts
and registers can be represented according to ENV1. Two            that are copied are simply event parameters, that will later
non-overlapping subsets with the same cardinality, CONTEXT         be refined into the actual contexts that are copied. The OS is
and SAVEDCTX represent the subset of locations that com-           modeled in the event osProgress. The event osFinal
pose the context (ENV2) and the subset of locations of a           is not a part of the OS, but is only introduced to model the
saved context (OS1.A), respectively. The bijective function        state where the OS has successfully finished its execution.
ctx2saved ∈ CONTEXT      SAVEDCTX relates each context           This event is composed only of guards, that is, it is enabled
location to where it is saved, while saved2ctx is its              once the state represented in its guards is reached but does
inverse (OS1.B). The context is defined as a relation from         not change it anymore. The event osProgress, that repre-


                                                                                                                         123
300                                                                                                              R. M. Gomes et al.


 1 osEntry REFINES osProgress
 2 ANY
 3 saveSet ⊆ toSave
 4 old ∈ SAVEDCTX→DATA
 5 WHERE
 6 saveSet = ∅
 7 saved = toSave           − old                                           Fig. 4 : Level 1 states and transitions
 8 l o a d e d = ∅ // load not s t a r t e d
 9 THEN
10 s a v e d := s a v e d ∪ ( s a v e S e t  old )
11 t o S a v e := t o S a v e\ s a v e S e t                      cess will complete and we move to a saved state. Similarly,
                                                                  the new variable toLoad ⊆ CONTEXT represents the context
                                                                  yet to be loaded, while loadSet defines the context subset
              Listing 5: Level 1 – Kernel entry
                                                                  loaded in each run of osExit. The event is made conver-
                                                                  gent on the variant toLoad, and loadSet is subtracted
 1 osExit REFINES osProgress                                      from toLoad on each run (Listing 6, Line 11), allowing the
 2 ANY                                                            event to eventually reach the loaded state. Event osFinal
 3 loadSet ⊆ toLoad
 4 new ∈ CONTEXT→DATA                                             remains unchanged.
 5 WHERE                                                          Level 2 Next, we define the input constants oldTask ∈
 6 loadSet = ∅                                                    TASKS and oldCtx ∈ CONTEXT → DATA that represent the
 7 loaded = toLoad            − new                              old task and its context when the kernel was requested.
 8 t o S a v e = ∅ // save c o m p l e t e
 9 THEN                                                           The saving operation in osEntry must save oldCtx into
10 l o a d e d := l o a d e d ∪ ( l o a d S e t  new )           oldTask’s save space. In order to save the context, we
11 t o L o a d := t o L o a d\ l o a d S e t                      must map it to a saved context. Additionally, the context
                                                                  might be modified during the saving process (ENV6), e.g.,
              Listing 6: Level 1 – Kernel exit                    the stack pointer is changed before it is saved when the archi-
                                                                  tecture automatically pushes some registers onto the stack.
                                                                  We must account for this modification, since what is finally
sents the OS kernel, is allowed to change the variables saved     saved is the transformed version of the values, and not the
and loaded, but does not yet describe how the copies are          original input values. Thus, we define in Listing 7 the func-
made. It is made anticipated, which, in Event-B, means that it    tions transform (axm1) and ctxTransform (axm5).
may execute several times, but must eventually give up con-       The architecture-specific function ctxTransform is only
trol and allow the model to reach osFinal. Refinements of         declared at this level, and represents the modification of
an anticipated event must converge, i.e., decrease a variant,     each value in the context. The function itself is only fully
thereby proving that it eventually gives up control. The idea     specified in Level 5. The function transform converts
is that, since the context is copied in different steps by HW     a context into a saved context according to ctx2saved
and software, this event can be refined into these steps. The     (axm3), modifying the values stored in each location accord-
Proof Obligations (POs) generated by Rodin verify that the        ing to ctxTransform. This is modeled by the axiom axm7
refinements of this abstraction (Levels 1 to 5) are correct. If   in Listing 7.
we can prove that the model always reaches osFinal, we               With these definitions in Event-B contexts, we also refine
prove that the desired state after OS execution is reached.       the machine variables and events. To represent the saved con-
These proofs are shown in Sect. 5.4.                              texts of all tasks (OS3.A), saved is refined into t_saved ∈
Level 1 Listing 5 and Listing 6 show the refinement of            TASKS→( SAVEDCTX → DATA), with glue invariant saved
osProgress into two events: osEntry (OS2.A: kernel                = toSave       − t_saved(oldTask). The new variable
entry responsible for saving the old context), and osExit         rTask ∈ TASKS is equal to the constant oldTask before
(OS2.B: kernel exit is responsible for loading the new con-       kernel body is run, and represents the new scheduled task
text). They model state transitions (Fig. 4), and their guards    after the scheduler has run. While osFinal always uses
define that entry must happen before exit, and exit may only      oldTask to check if the context has been correctly saved,
start after entry is done.                                        osEntry refers to rTask to save the context. Similarly,
    The new variable toSave ⊆ SAVEDCTX keeps track of             as the CPU context is only one, we create cpuCtx ∈
the context yet to be saved, while the parameter saveSet          CONTEXT → DATA to represent it, and its relation to oldCtx
defines the context subset saved in each run of osEntry.          and loaded is given by the glue invariants toSave 
The event is made convergent on the variant toSave, and           oldCtx = toSave  cpuCtx and loaded = toLoad
saveSet is subtracted from toSave in each run (Listing            
                                                                  − cpuCtx. This way, all three kernel parts (entry, body, and
5, Line 11). This guarantees that, eventually, the save pro-      exit) deal with the same variables, simplifying code genera-


 123
A framework for embedded software portability...                                                                                   301


   axm1 : transform ∈ (CONTEXT→DATA)                                     1 osFinal ( guards )
   (SAVEDCTX→DATA)                                                         2 cpuCtx = invTransform ( t_saved ( rTask )
   axm2 : invTransform ∈ (SAVEDCTX→ DATA)                                   )
   (CONTEXT→DATA)                                                          3 t_saved ( oldTask ) = transform ( oldCtx )
   axm3 : ctx2saved ∈ CONTEXT            SAVEDCTX                        4 toSave = ∅
   axm4 : saved2ctx ∈ SAVEDCTX             CONTEXT                       5 toLoad = ∅
   axm5 : ctxTransform ∈ CONTEXT→(DATA→DATA)
   axm6 : ctxInvTransform ∈ SAVEDCTX→(DATA→
   DATA)                                                                                Listing 10: Level 2 – osFinal
   axm7 : ∀ ctx, el · ctx ∈ CONTEXT→DATA ∧ el
   ∈ CONTEXT ⇒ transform(ctx)(ctx2saved(el)) =
   ctxTransform(el)(ctx(el))                                              1 osBody
   axm8 : ∀ sctx , el · sctx ∈ SAVEDCTX→DATA ∧                            2 WHERE
      el ∈ SAVEDCTX ⇒ i n v T r a n s f o r m ( sctx ) (                  3 toSave = ∅
    s a v e d 2 c t x ( el ) ) = c t x I n v T r a n s f o r m ( el ) (   4 t o L o a d = CONTEXT
    sctx ( el ) )                                                         5 THEN
                                                                          6 r T a s k :∈ TASKS

         Listing 7: Generic model axioms in Level 2
                                                                                        Listing 11: Level 2 – osBody

 1 osEntry REFINES osEntry
 2 ANY
                                                                          respectively. Similarly to axm7 for the save functions, axm8
 3 saveSet ⊆ toSave
 4 WHERE                                                                  models how invTransform converts a saved context into
 5 saveSet = ∅                                                            a context.
 6 toSave       − t_saved ( rTask ) = toSave                 −              Now, we can refine the old and new parameters to reflect
     transform ( oldCtx )
                                                                          the real source and destination of the context copies (OS3.B)
 7 l o a d e d = ∅ // load not s t a r t e d
 8 THEN                                                                   in Level 2 (Listing 8, 9, and 10).
 9 t _ s a v e d ( r T a s k ) := t _ s a v e d ( r T a s k ) − (            Finally, the new event osBody models kernel body (List-
     saveSet  transform ( cpuCtx ))                                      ing 11), abstractly representing the scheduler (OS4). We do
10 t o S a v e := t o S a v e\ s a v e S e t
                                                                          not model the typical functionality of the kernel body (e.g.,
                                                                          scheduling, resource management, etc.) in this work, but
                Listing 8: Level 2 – Kernel entry                         will refine it to guarantee its execution according to the OS
                                                                          requirements.
 1 osExit REFINES osExit                                                  Level 3 Though we do not model kernel body with all its
 2 ANY                                                                    functionality, we want to guarantee that kernel entry pre-
 3 loadSet ⊆ toLoad                                                       pares the CPU to start its execution. Analogously, we do not
 4 WHERE
                                                                          model tasks, but want to guarantee that kernel exit prepares
 5 loadSet = ∅
 6 toLoad     − cpuCtx = toLoad            −                            the CPU to run them. Thus, we introduce the variables that
     invTransform ( t_saved ( rTask ))                                    control the conditions for proper task and kernel body execu-
 7 t o S a v e = ∅ // save c o m p l e t e                                tion (OS5, OS6): kernelMode is a flag that indicates when
 8 THEN
                                                                          the kernel has been entered. osBody can only be enabled if
 9 c p u C t x := c p u C t x − ( l o a d S e t 
     invTransform ( t_saved ( rTask )))                                   it is true, and osFinal if it is false; kernelCause records
10 t o L o a d := t o L o a d\ l o a d S e t                              why the kernel has been invoked. It unambiguously identifies
                                                                          each interrupt and syscall, and must be valid within osBody;
                 Listing 9: Level 2 – Kernel exit                         interruptEnable is the interrupt enabled flag (ENV3).
                                                                          It must be false in osBody, and loaded from the next task’s
                                                                          saved context during kernel exit; currStack indicates
tion. We can finally replace the abstract save action in Listing          the stack currently in use, abstractly representing a kernel
5 (Line 10) by the action in Listing 8 (Line 9).                          or a task stack. osBody is enabled if currStack indi-
   The context to be loaded during kernel exit actually comes             cates kernel stack, while osFinal requires it to indicate
from the saved context of rTask, thus we replace the                      task stack. We strengthen osBody and osFinal guards
abstract load from Listing 6 (Line 10) by the load in List-               to fulfill OS5 and OS6. Modifications of these variables in
ing 9 (Line 9). The functions transform, ctx2saved,                       kernel entry and exit remain nondeterministic, since they are
and ctxTransform, used for saving a context have their                    highly hardware-dependent. Listing 12 shows the new sets
inverses also defined in Listing 7: invTransform (axm2),                  and variables, Listing 13 shows the new axioms, and List-
saved2ctx (axm4), and ctxInvTransform (axm6),                             ing 14 shows the new guards for osBody. We also create


                                                                                                                            123
302                                                                                                                  R. M. Gomes et al.


1 SETS ( new )                                                            We refine the events osEntry and osExit by split-
2 STACKS                                                              ting each in two, and refining their parameters (saveSet
3 KERNELCAUSES                                                        in Listing 8 and loadSet in Listing 9) to differentiate the
4 V A R I A B L E S ( new )
                                                                      partitions in CONTEXT and SAVEDCTX. The transform and
5 k e r n e l M o d e ∈ BOOL
6 k e r n e l C a u s e ∈ KERNELCAUSES                                invTransform functions are also refined to reflect the
7 i n t e r r u p t E n a b l e ∈ BOOL                                refinements of this level and the separation of the different
8 c u r r S t a c k ∈ STACKS                                          levels of context copy. The events are refined according to
                                                                      Fig. 5: osAutoEntry saves values from AUTODIRECTCTX
      Listing 12: Level 3 – New carrier sets and variables            into AUTODIRECTSAVE and copies from AUTOTEMPCTX to the
                                                                      new variable temp ∈ TEMP → DATA. For architectures that
                                                                      only copy parts of the context to temporary locations, not
1 A X I O M S ( new )
2 partition (STACKS,KERNELSTACK,TASKSTACKS)
                                                                      saving anything, we refine entryNothingToSave into
3 partition (KERNELCAUSES ,{ k C a u s e _ i n v a l i d } ,          tempSave, adding a copy to temp and making it conver-
    KCAUSE_SYSCALLS,KCAUSE_FLOWINTS)                                  gent on the variant TEMP\dom(temp) (must add elements to
                                                                      temp). We also keep entryNothingToSave only modi-
              Listing 13: Level 3 – New axioms                        fying variables from Level 3. Then, osManualEntry saves
                                                                      MANUALCTX into MANUALSAVED and copies temp into the
                                                                      AUTOTEMPSAVE location, completing the saving of the tem-
1 o s B o d y ( new g u a r d s )                                     porary part of the context. The action that represents this
2 k e r n e l M o d e = TRUE
3 kernelCause = kCause_invalid                                        is shown in Listing 15a. The structure t_saved gives us
4 i n t e r r u p t E n a b l e = FALSE                               the locations where the context is saved for each task, and
5 c u r r S t a c k ∈ KERNELSTACK                                     rTask represents the running task, whose context must be
                                                                      saved. The saved context is overwritten (−) in two steps:
        Listing 14: Level 3 – New guards in osBody                    one takes the values from cpuCtx ∈ CONTEXT → DATA,
                                                                      filtering only the MANUAL part with a domain restriction oper-
                                                                      ator (), while the other takes the values from temp ∈
the event entryNothingToSave, that mimics osEntry                     TEMP → DATA, which has been written by osAutoEntry
and is explained in Level 4.                                          with the AUTOTEMPCTX values from cpuCtx. The inverse
Level 4 Now, kernel entry and exit are divided in two parts:          operation is modeled in kernel exit: First, osManualExit
one models what is automatically done by the hardware, via            loads from MANUALSAVED into MANUALCTX and copies from
an interrupt acceptance or a return from interrupt instruc-           AUTOTEMPSAVE into temp, then osAutoExit loads all
tion (ENV4, ENV5). This may save some registers, turn off             AUTOCTX from temp and AUTODIRECTSAVE. The generic
the interrupt enabled flag, switch the CPU mode, etc. The             model we conclude in this Level is shown in Fig. 6.
remaining actions of kernel entry (OS7) and exit (OS8, OS9)
are fulfilled by their manual parts.                                  5.3.2 Hardware-specific model instantiation
    This Level still does not refer to specific details of a poten-
tial target architecture. Therefore, the model must support           Level 5 This section details the instantiation of the context
different behaviors: the hardware might, on interrupt, copy           switch model, i.e., Level 5, and the hardware models for the
a set of its registers into another set of registers designed         target architectures we instantiate for, MSP430 and RISC-V.
for that (OS10.B), or it might copy them to memory, for                  Having intentionally modeled the OS independent from
example pushing them onto the stack (OS10.A). In the                  the hardware so far, we finally introduce hardware details in
first case, we call this a temporary save, since the desti-           a new refinement level per target architecture. For each tar-
nation is the same for all tasks and must, therefore, still           get, we extend the Event-B context into hardware models.
be made permanent by (manually) copying it to the task’s              We define, within LOCATION, all registers available in the
saved context in kernel entry. To model this, we partition            architecture. At the same time, we also define which of them
CONTEXT and SAVEDCTX in three sections, as shown in Fig. 3b:          are part of CONTEXT (and to which subset), TEMP, etc. We also
MANUALCTX and MANUALSAVED for the locations that are only             define the locations for saved contexts and the CPU-specific
manipulated in the manual part, and two others for those              functions ctxTransform and ctx2saved. The MSP430
automatically handled by the hardware. AUTODIRECTCTX and              model defines the CONTEXT subsets as shown in Listing 16a,
AUTODIRECTSAVE for those locations permanently saved by               while the same subsets are defined for the RISC-V in Listing
the hardware, and AUTOTEMPCTX and AUTOTEMPSAVE for                    16b. Not shown here are the definitions of the SAVEDCTX
those first copied to/from a TEMP location. TEMP is another           subsets, which simply mirror the CONTEXT elements, and
subset of LOCATION, created in this level.                            their relations. The relation ctx2saved, that maps each


123
A framework for embedded software portability...                                                                                   303




                    Fig. 5 : Context saving during kernel entry. Dx ⊂ DATA and Dx = ctxTransform(Dx )




             Fig. 6 : Level 4 – Most detailed but still hardware-independent (generic) model of the context switch




                                    Fig. 7 : Level 5 – target-specific refinements of Level 4 (Fig. 6)

CONTEXT element to its correspondent in SAVECTX, is only               interrupt, it pushes the return address (next program counter
shown for the MSP430.                                                  in R0) and status register (SR/R2) onto the stack, disables
   To instantiate the generic model, we refine, for each target,       interrupts, and starts executing the corresponding interrupt
the last Level 4 machine. It sees the Event-B context cor-             handler. Because each task has its own stack, we can consider
respondent to the target, and the architecture-specific actions        R0 and R2 as automatically saved on interrupt. Therefore, we
from Level 3 are made deterministic.                                   refine osAutoEntry to represent the interrupt. The event
   MSP430. Figure 7a depicts the architecture-specific                 will also be refined to represent the syscalls, becoming two
model for the MSP430. Comparing it to Fig. 6, one can see              different (but equivalent to their abstraction) events. Since no
that the former is a target-specific refinement of the latter.         registers are temporarily saved by the MSP430, tempSave
The guards shown in the generic model are still present                is removed. Once an interrupt is accepted, the MSP430 takes
(and verified) in the architecture-specific model, but omit-           the interrupt handler’s address from the corresponding index
ted in the figure for clarity. When the MSP430 accepts an              in the interrupt vector table and executes the handler. The


                                                                                                                            123
304                                                                                                               R. M. Gomes et al.


  m S a v e :t_saved(rTask) := t_saved(rTask)                          RISC-V. The RISC-V architecture model is depicted
   − (MANUALSAVED  t r a n s f o r m (cpuCtx) )                  in Fig. 7b. The interrupt concept of RISC-V is quite dif-
   − ( a u t o T e m p T E M P S V D t r a n s f o r m (temp) )   ferent: when an interrupt is accepted, the return address is
                                                                   stored in the special register mepc, the status in mstatus,
           (a) Formal definition of the manual save action
                                                                   and the interrupt number goes into mcause. The CPU then
  t_saved(rTask)(mR1) := cpuCtx(R1)                                switches to a more privileged mode and continues execu-
  t_saved(rTask)(mR4) := cpuCtx(R4)                                tion from the address stored in the so called trap vector. We
  t_saved(rTask)(mR5) := cpuCtx(R5)
  ...
                                                                   refine kernelMode to the privilege levels, adding an invari-
                                                                   ant that relates kernelMode = TRUE to machine mode
                   (b) Unrolled save on MSP430                     and kernelMode = FALSE to user mode (OS11). Since
                                                                   the special registers where the AUTOCTX is stored are not
  t_saved(rTask)(mX1) := cpuCtx(x1)
  t_saved(rTask)(mX2) := cpuCtx(x2)                                task-specific, they belong to the AUTOTEMPCTX, and must be
  ...                                                              permanently saved later. Because nothing is automatically
  t_saved(rTask)(mMEPC) := cpuCtx(mepc)                            saved (but only “temporarily” stored), tempSave is refined
  t_saved(rTask)(mMSTAT) := cpuCtx(mstatus)                        to represent the interrupt and osManualEntry follows
  ...
                                                                   after the interrupt. Event osAutoEntry is never enabled
                   (c) Unrolled save on RISC-V                     and we can remove it.
                                                                       For the syscalls, we need to be able to emulate the pre-
Listing 15: Generic (a) and target-specific unrolled (b,c) save    viously described interrupt process. The ecall instruction
actions                                                            is designed exactly for that, as it causes an exception, just
                                                                   like a hardware interrupt. We refine tempSave again, now
  axm4 :AUTODIRECTCTX = {R0,R2}                                    to represent the instruction ecall. However, there is a
  a x m 2 6 :TEMP = ∅                                              difference: what is recorded in mcause is not the ID of
  axm3 :AUTOTEMPCTX = ∅                                            the syscall itself, as the architecture can only register the
  axm5 :MANUALCTX = {R1,R4,R5,R6,R7,R8,R9,                         occurrence of the instruction. Since each syscall must pass
  R10,R11,R12,R13,R14,R15}
  a x m 2 2 :ctx2saved = {R0 → mR0,R1 → mR1,                       its ID to the kernel and call ecall explicitly, we refine
  R2 → mR2,R4 → mR4 ,... ,R15 → mR15}                              entryNothingToSave to do exactly that, also renaming
                                                                   it to syscall.
                            (a) MSP430
  axm4 :AUTODIRECTCTX = ∅                                          5.4 Proofs and model checking
  a x m 1 1 :TEMP = {mepc,mstatus}
  axm3 :AUTOTEMPCTX = {invisiblePC,                                This section shows the properties we verified via theorem
  invisibleSTATUS}
  axm5 :MANUALCTX = {x1,x2,x3,x4,x5,x6,x7,x8
                                                                   proving in Rodin and LTL model checking.
   ,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,                           From the requirements in Sect. 5.1.2, we elaborate some
  x19,x20,x21,x22,x23,x24,x25,x26,x27,x28,                         safety properties to be proved: (S1) Contexts are never cor-
  x29,x30,x31}                                                     rupted by the kernel (OS2), (S2) osBody always runs in
                                                                   the specified conditions for its execution, and osFinal
                            (b) RISC-V
                                                                   is reached with the specified conditions for task execu-
      Listing 16: Hardware models for CONTEXT in Level 5           tion (OS5, OS6). Details for verifying the other OS require-
                                                                   ments are omitted in this paper since the concept is the same.
                                                                   Instead, we also show how to verify some liveness properties:
MSP430 does not record the interrupt ID anywhere, so we            To guarantee that the model reaches the intended states, we
must save it in the specific interrupt handler before proceed-     verify that the steps resulting from the OS requirements are
ing to osManualEntry. We thus refine entryNTS to save              executed in the appropriate orders. (L1) The kernel executes
the interrupt ID and rename it to intHandler.                      in the correct order, and (L2) always finishes execution by
    The refinement of osAutoEntry to syscall executes              always reaching osFinal.
the actions of both interrupt and intHandler events,
i.e., it saves the AUTOCTX, disables interrupts, and stores the    5.4.1 Theorem proving
syscall ID. In osManualEntry the rest of the context is
saved, the stack is switched to kernel stack, and kernel mode      All refinements in our model must correspond to their
is set to true. Since the MSP430 does not have differently         abstraction, which is proved with discharging the POs gen-
privileged modes, we simulate the switch into kernel by set-       erated by Rodin. The initial abstraction, Level 0, defines the
ting a simple variable.                                            state (osFinal guards) we want to achieve after OS execu-


123
A framework for embedded software portability...                                                                                      305

             Table 3 : Number of POs discharged                           The SIM POs involving save and load actions, however,
                                                                      were rather complex, especially in Level 4. In particular for
Level          #POs           Auto           Simple       Complex     events osManualEntry and osAutoExit, we had to
0              8              8              0            0
                                                                      create a new parameter and an extra theorem in order to
                                                                      discharge the SIM POs. We detail here the proof strategy
1              17             15             2            0
                                                                      for the save action SIM PO in osManualEntry. The same
2              63             52             11           0
                                                                      strategy was applied to osAutoExit. We must prove that
3              14             14             0            0
                                                                      the manual save action from Level 4 (Listing 15a) simulates
4              83             39             35           9
                                                                      its abstract correspondent of Level 2 (Listing 8, Line 9). We
5              70             58             6            6
                                                                      replace the temporary save part of the action by the parameter
Total          255            186            54           15
                                                                        aux = a u t o S a v e S e t 
               100%           73%            21%          6%
                                                                         a u t o T e m p T E M P S V D t r a n s f o r m ( temp )

                                                                         and add to the event’s guards the theorem
tion, namely that an old context is saved and a new context is
                                                                        aux = a u t o S a v e S e t  a u t o T e m p T r a n s f o r m
loaded. This state must be reached by osProgress, which                 (AUTOTEMPCTX c p u C t x )
models the OS. Thus, event osProgress is refined into the
three main parts of the kernel (entry, body, and exit). Entry         After proving the theorem, the SIM PO is much easier to
and exit are responsible, respectively, for saving the old task’s     discharge.
context and loading the new task into the CPU. The first
abstraction is modeled such that osProgress can not run               5.4.2 LTL model checking
forever. The idea is that it must change the state until it finally
enables osFinal, i.e., the desired terminal state. Through            For the liveness verification, we encode a set of LTL for-
the refinements, we model how exactly this happens, splitting         mulas that guarantee the specified execution order and that
osProgress into several events, and creating invariants               osFinal is eventually enabled. The model shall (1) even-
and actions that model the OS requirements.                           tually reach osFinal, staying there forever, (2) not reach a
   Some of the discharged POs guarantee that the events               state where all events are disabled, (3) always have exactly
refining osProgress also give up control, and in Sect. 5.4.2          one event enabled, and (4) implement the specified execu-
we prove that they indeed modify the state such that it eventu-       tion order: entry first, then body, and finally exit; and manual
ally reaches osFinal. Other POs prove that actions always             save after auto save (OS7) and manual load before auto
respect the invariants (INV POs), or that a concrete event’s          load (OS9).
actions do simulate the abstract correspondents (SIM POs).                Since the model’s axioms are rather complex, we need
There are several other rules for PO generation, which we do          to create a minimal set of CONTEXT and SAVEDCTX elements
not detail here. Table 3 summarizes the number of POs gen-            to represent the locations that compose contexts and saved
erated in each level of abstraction, and shows how many of            contexts, otherwise the state space explodes and ProB cannot
them were automatically or manually discharged. The man-              complete verification. For this, we extend the Event-B con-
ually discharged ones are differentiated according to their           texts with the constant instantiations, and refine the machines
discharging complexity: simple POs only required a few steps          we want to check. These machines are not modified any fur-
to be discharged, while the complex POs required more expe-           ther, except for the model checks of Level 3 and 4, where the
rience with the proving system and the PO’s breakdown in              nondeterministic actions introduced in Level 3 would cause
several proving steps.                                                the checks to fail, since paths would exist in which osBody
   In Level 2, two invariants guarantee that the save and load        and osFinal could not be reached. As our intention is to
processes do save oldCtx and load the rTask’s saved con-              leave this determinism to the architecture-specific models,
text:                                                                 the actions are modified to enforce the correct execution path.
                                                                      In Level 5, all actions are left unmodified, and we can check
    m05 . inv2 : t o S a v e = ∅ ⇔ s a v e d =                        if the variables have been correctly set.
     transform ( oldCtx )
    m07 . inv4 : t o L o a d = ∅ ⇔ l o a d e d =
                                                                          One error was found in Level 2, where LTL found a coun-
     invTransform ( t_saved ( rTask ))                                terexample for reachability, so the model may never reach
                                                                      osFinal: An infinite loop is possible, because osBody
Discharging the related INV POs proves that, for every refine-        does not decrease any variant and does not modify any
ment, when our model considers the old context as saved and           variables that affect its guards. Thus, we introduce a new
the new context as loaded, they indeed are. Those INV POs             boolean variable osBodyRun, initialize it with FALSE,
were always automatically discharged, except in few refine-           and add the guard osBodyRun = FALSE and an action
ments, where they were manually discharged in a few steps.            osBodyRun := TRUE. A similar error was found when


                                                                                                                                    123
306                                                                                                                      R. M. Gomes et al.


                                                                    function named after the Event-B machine, with one code
                                                                    block for each of its events. In Event-B, control flow between
                                                                    events is not directly modeled, but defined within the event’s
                                                                    guards. To extract this control flow information, we use the
                                                                    event enabling analysis of the model provided by ProB [47].
                                                                    At the end of each block, compare and jump instructions are
                                                                    created to direct the flow to the appropriate next block.
                                                                       Each block of code will be filled with code generated
                                                                    from the actions of the corresponding event. As in most code
                                                                    generators for Event-B, actions with basic arithmetics, vari-
                                                                    able assignment, etc. can be converted to their corresponding
                                                                    instructions. Additionally, EB2LLVM also supports array
                                                                    accesses, direct register accesses, and is capable of unrolling
                                                                    set expressions and relations, as well as solving equations2 .
                                                                    For that, it uses definitions and declarations (axioms) from
                                                                    the concrete model and all its abstractions.
                                                                       The code generation for the OS model will be presented
                                                                    in Sect. 6.2. Before, in Sect. 6.1, we give an overview of
                                                                    the entire framework on a generally known algorithm, the
            Fig. 8 : Overview of code generation                    mathematical function factorial. The factorial example will
                                                                    show the more basic features of EB2LLVM, while the OS
                                                                    example digs deeper in the more complex features that allow
entryNothingToSave was introduced, prompting us to                  EB2LLVM to generate code that communicates directly with
make it convergent and create a variant as explained in Level 4     the hardware, such as for the context switch.
(Sect. 5.3).
    Model checking Level 4 also revealed that the execu-
tion order of events was not as intended: one formula fails         6.1 Factorial example
because we forgot to strengthen osManualEntry’s guards
to require it to only be enabled after all AUTODIRECTSAVE ele-      The factorial of a natural number n, denoted n!, is the prod-
ments have been saved, as required by OS7. The new guard            uct of all natural numbers from 1 to n. The factorial of 0
AUTODIRECTSAVE ∩ toSave = ∅ forces this order. Simi-                is, by definition, 0! = 1. Factorial is often implemented
larly, osAutoExit may only execute after all MANUALCTX              recursively, where f(n) = n * f(n-1). Our Event-B
is loaded (OS9), thus the new guard MANUALCTX ∩ toLoad              model will use recursion for the model checking. However,
= ∅ was introduced.                                                 the intended implementation is an iterative one, as Listing 17
    With these modifications to the models and the discharg-        shows. This C code is not relevant for code generation, but
ing of all proofs, we can formally prove that all requirements      just to (1) present the algorithm in comparison to the model
from Sect. 5.1 are fulfilled and the OS model is correct.           and (2) to compare the final binaries compiled from the C
                                                                    code and our generated LLVM IR.
                                                                        Following our modeling strategy described in Sect. 5, the
                                                                    model’s machine is shown in Listing 18. It contains the
6 Code generation
                                                                    fFinal event that models the goal of the factorial func-
                                                                    tion in its guards, and has no actions (skip). The guard
With generic and target-specific models complete and ver-
                                                                    [fFinal.modelGoal] assures the correctness of the calculated
ified, we can generate code for the target architectures.
                                                                    result. Since some parts of the model are not intended for
Figure 8 shows an overview of the code generation process.
                                                                    code generation, such as this guard, any statement with the
We start by exporting all Event-B contexts and machines to
                                                                    label starting with “model” will be ignored by EB2LLVM.
text format. The plain text format (.eb) allows EB2LLVM
                                                                    The event where the factorial of input is calculated is calc
to work outside of Rodin. The Rodin plugin we use to export
                                                                    (Listing 18, Line 16). This event is equivalent to the while
the model is a modified version of the B2Latex plugin [20],
                                                                    block in Listing 17.
that we call EB2LatexLst.
    Using Flex and Bison [25, 26], EB2LLVM can read and
parse these .eb files into abstract syntax trees that it can pro-   2 Computational equation solving is a rather complex topic that we have
cess to generate code. For each concrete Event-B machine,           not explored fully. EB2LLVM’s capabilities are limited to the specific
EB2LLVM will create one LLVM IR file, containing one                equations we needed for this proof of concept.


123
A framework for embedded software portability...                                                                                   307


  1   int input ;                                                     1 CONTEXT factorialCtx
  2   int cnt , res ;                                                 2 CONSTANTS
  3                                                                   3   D AT A
  4   void factorial () {                                             4   max I nt
  5     cnt = 0;                                                      5    f at Func
  6     res = 1;                                                      6   input
  7                                                                   7   max I nput
  8       while( cnt < input ) {                                      8 AXIOMS
  9         cnt = cnt+1;                                              9   m a x I n t T y p e : max I nt ∈ N
 10         res = cnt∗res ;                                          10   d a t a T y p e : D AT A = 0..max I nt
 11       }                                                          11   m a x I n t 1 : max I nt ≥ 1
 12   }                                                              12   m a x I n T y p e : max I nput ∈ D AT A
                                                                     13   i n P a r a m : input ∈ 0..max I nput
                                                                     14   f T y p e : f at Func ∈ 0..max I nput → D AT A
Listing 17: C code of the factorial function. Parameters and         15   f C a l c : ∀ x · x ∈ 0..max I nput ∧ x > 0 ⇒
return value passed via global variables                                    f at Func(x) = x ∗ f at Func(x−1)
                                                                     16   f Z e r o : f at Func(0) = 1
                                                                     17   m a x I n : f at Func(max I nput) ≤ max I nt
 1 MACHINE factorial                                                 18 END
 2 SEES f a c t o r i a l C t x
 3 VARIABLES
 4    cnt                                                                 Listing 19: Event-B context for the factorial model
 5    r es
 6 INVARIANTS
 7     c n t T y p e : cnt ∈ 0.. max I nput
 8     r e s T y p e : r es ∈ D AT A                                 tially be represented, e.g., by unsigned long integers, the
 9     r e s I n v : r es = f at Func(cnt)                           instantiation must consider them signed integers. It follows
10 E V E N T S                                                       that DATA ∈ 0..(2b−1 − 1), where b is the bit-width of the tar-
11 I N I T I A L I S A T I O N                                       get. For the 16-bit MSP430, this means maxInt = (215 −1),
12     THEN
13         i n i t C n t :cnt := 0                                   while for the 32-bit RISC-V, maxInt = (231 − 1).
14         i n i t R e s :r es := 1                                     We will now explain the LLVM IR generated from our
15     END                                                           models and shown in Listing 20 for the MSP4303 : In the
16 calc                                                              enabling analysis generated by ProB (Table 4) the connection
17     WHERE
18         l o o p C o n d :cnt < input                              between fFinal with itself is syntactic_independent, since
19     THEN                                                          once the event executes, the state does not change anymore.
20         m u l R e s :r es := (cnt + 1) ∗ r es                     EB2LLVM interprets this as a return instruction. The possible
21         i n c C n t :cnt := cnt + 1                               connections in the enabling analysis will all generate condi-
22     END
23 f F i n a l                                                       tional branches at the end of the origin block. The condition
24     WHERE                                                         is generated from the guards of the destination. All possible
25         l o o p S t o p :cnt = input                              destinations will be considered: having INITIALIZATION
26         m o d e l G o a l :r es = f at Func(input)                as origin, both calc and fFinal are possible. Therefore,
27     THEN
28       skip                                                        two conditional branches will be generated. The first, in List-
29     END                                                           ing 20 (Lines 7–10) branches to calc if cnt < input, as
30 END                                                               required by the guard [calc.loopCond]. Otherwise, it jumps to
                                                                     a newly created block INITIALIZATION_fFinal (Lines
      Listing 18: Event-B machine of the factorial model             32–36) that then jumps to fFinal if cnt = input (Line 26).
                                                                     Otherwise, it jumps to the default error block (Line 29).
                                                                     Similarly, calc may either jump back to itself (Lines 21–24)
   The model sets the function’s pre-conditions in the               or to calc_fFinal (Lines 38–42).
axioms of Listing 19. Therefore, the generated function                 In this example, one can also notice several load and
factorial will assume that these pre-conditions hold, and            store instructions generated from Event-B variable reads
will not, e.g., check if input ∈ 0..maxInput.                        and assignments. Basic arithmetics are also translated to their
   Since the factorial model does not make any use of, e.g.,         LLVM equivalents. In the factorial example, we have addi-
registers or interrupts, its instantiation consists of only defin-   tion and multiplication being converted to, respectively, the
ing the DATA type as a function of the target’s bit-width.           instructions add and mul.
It is important to notice that, currently, EB2LLVM only
supports signed integers with the architecture’s bit-width.
Therefore, even though the model’s variables could poten-            3 The RISC-V code is the same, except for the bit-widths.




                                                                                                                                 123
308                                                                                                        R. M. Gomes et al.


 1 ...
 2 ; F u n c t i o n A t t r s : naked
 3 d e f i n e void @ f a c t o r i a l () n a k e d {
 4 INITIALISATION :
 5     s t o r e i16 0 , i16 * @cnt , ! l a b e l !{! " i n i t C n t " }
 6     s t o r e i16 1 , i16 * @res , ! l a b e l !{! " i n i t R e s " }
 7     %0 = load i16 , i16 * @cnt
 8     %1 = load i16 , i16 * @ i n p u t
 9     % c o m p a r e = icmp slt i16 %0 , %1
10     br i1 %compare , l a b e l %calc , l a b e l % I N I T I A L I S A T I O N _ f F i n a l , ! l a b e l !{! "
        possible "}
11
12 calc :                ; preds = %calc , % I N I T I A L I S A T I O N
13     %2 = load i16 , i16 * @res
14     %3 = load i16 , i16 * @cnt
15     %4 = add i16 %3 , 1
16     %5 = mul i16 %4 , %2
17     s t o r e i16 %5 , i16 * @res , ! l a b e l !{! " m u l R e s " }
18     %6 = load i16 , i16 * @cnt
19     %7 = add i16 %6 , 1
20     s t o r e i16 %7 , i16 * @cnt , ! l a b e l !{! " i n c C n t " }
21     %8 = load i16 , i16 * @cnt
22     %9 = load i16 , i16 * @ i n p u t
23     % c o m p a r e 2 = icmp slt i16 %8 , %9
24     br i1 %compare2 , l a b e l %calc , l a b e l % c a l c _ f F i n a l , ! l a b e l !{! "
        possible_disable "}
25
26 f F i n a l :         ; preds = % c a l c _ f F i n a l , % I N I T I A L I S A T I O N _ f F i n a l
27     ret void , ! l a b e l !{! " s y n t a c t i c _ i n d e p e n d e n t " }
28
29 e r r o r :           ; preds = % c a l c _ f F i n a l , % I N I T I A L I S A T I O N _ f F i n a l
30     ret void
31
32 I N I T I A L I S A T I O N _ f F i n a l : ; preds = % I N I T I A L I S A T I O N
33     %10 = load i16 , i16 * @cnt
34     %11 = load i16 , i16 * @ i n p u t
35     % c o m p a r e 1 = icmp eq i16 %10 , %11
36     br i1 %compare1 , l a b e l %fFinal , l a b e l %error , ! l a b e l !{! " p o s s i b l e " }
37
38 c a l c _ f F i n a l :     ; preds = % c a l c
39     %12 = load i16 , i16 * @cnt
40     %13 = load i16 , i16 * @ i n p u t
41     % c o m p a r e 3 = icmp eq i16 %12 , %13
42     br i1 %compare3 , l a b e l %fFinal , l a b e l %error , ! l a b e l !{! " p o s s i b l e _ e n a b l e " }
43 }


Listing 20: MSP430 generated LLVM IR for the factorial model. The generated IR code for RISC-V is the same, except for
the bit-widths.


    The last step in the code generation is to compile the     9.0.0 (with the -march=rv32i option), the same LLVM
LLVM IR into assembly with llc, LLVM’s static compiler.        version we use in our code generation. The compiled code is
For the factorial example, we use the default optimization     shown in Listing 22b. Both used the same level of optimiza-
-O2 to generate assembly code for the targets MSP430 and       tion -O2.
RISC-V. The generated code is shown in Listing 21a and List-      The code compiled from C for the MSP430 (Listing 21b)
ing 22a respectively. The code generated from the Event-B      is a few instructions longer than the one we generated from
model, can be compared to the code compiled from the C         the Event-B model (Listing 21a). One of the reasons is that
factorial function in Listing 17. For the MSP430, we used      the gcc compiler inserted prologue and epilogue to save and
the MSPgcc 6.2.1 compiler, and the resulting assembly          restore registers used within the function. Since our code
is shown in Listing 21b. A clang compiler was available for    generator aims at generating exactly what is modeled, these
RISC-V, and we used version RISC-V rv32gc clang


123
A framework for embedded software portability...                                                                                               309


Table 4 Control flow generated
                                      Origin/destination                       calc                                          fFinal
by ProB
                                      INITIALISATION                           possible                                      possible
                                      calc                                     possible_disable                              possible_enable
                                      fFinal                                   syntactic_unchanged                           syntactic_independent



                                                                      1 f a c t o r i a l () :
                                                                      2 P U S H M . W #4 , R10
 1 factorial :                    ; @factorial                        3 P U S H M . W #1 , R4
 2 ; %bb .0:                      ;                                   4 MOV . W           R1 , R4
    %INITIALISATION                                                   5 MOV . W           #0 , & cnt
 3 mov #1 , & res                                                     6 MOV . W           #1 , & res
 4 clr & cnt                                                          7 MOV . W           & input , R7
 5 cmp #1 , & i n p u t                                               8 MOV . B           #0 , R12
 6 jl . L B B 0 _ 2                                                   9 CMP . W           R7 , R12
 7 . LBB0_1 :                     ; %calc                            10 JGE . L1
 8     ; = > This Inner Loop Header : Depth                          11 MOV . W           R7 , R8
        =1                                                           12 ADD . W           #1 , R8
 9 mov #1 , r 1 0                                                    13 MOV . B           #1 , R10
10 add & cnt , r 1 0                                                 14 MOV . W           R10 , R12
11 mov & res , r 1 3                                                 15 MOV . W           # _ _ m s p a b i _ m p y i , R9
12 mov r 1 0 , r 1 2                                                 16 . L3 :
13 call # _ _ m s p a b i _ m p y i                                  17 MOV . W           R10 , R13
14 mov r 1 2 , & res                                                 18 CALL              R9
15 mov r 1 0 , & cnt                                                 19 ADD . W           #1 , R10
16 cmp & input , r 1 0                                               20 CMP . W           R8 , R10
17 jl . L B B 0 _ 1                                                  21 JNE . L3
18 . L B B 0 _ 2 :                ; %calc_fFinal                     22 MOV . W           R7 , & cnt
19    cmp & input , & cnt                                            23 MOV . W           R12 , & res
20 ret                                                               24 . L1 :
                                                                     25 POPM . W          #1 , r 4
(a) Compiled from auto-generated IR for MSP430                       26 POPM . W          #4 , r 1 0
(Event-B GGGGGGGGGGGGA
           EB2LLVM     LLVM GGGGA
                               llc ASM)                              27 RET

                                                                             (b) Compiled from the C code for MSP430 (C GGGGGA
                                                                                                                          gcc ASM)



                                               Listing 21: MSP430 assembly code for factorial


registers are silently overwritten.4 Further, the gcc version                 Also similarly to the MSP430, the assembly code gener-
has more instructions to prepare for the while loop, however               ated by clang for the RISC-V (Listing 22b) has prologue
the instructions sequence inside the loop is more optimized.               and epilogue, while the code generated from Event-B (List-
   A note about the compare instruction in Listing 21a, Line               ing 22a) does not. The while loop is also more optimized,
19: our code generator correctly generated it from Listing                 and instead of storing partial results in each iteration, clang
20, Lines 39 to 41, however the corresponding branch in                    only stores the end values before return. Though slightly less
Line 42 was omitted. This is functionally correct, since both              efficient, the code generated from Event-B for both MSP430
destinations of this branch (fFinal and error) would                       and RISC-V can be compiled into binaries that execute as
result in the execution of a return instruction, which fol-                intended.
lows the compare in the generated assembly code. However,
this renders the compare instruction useless. A similar situa-
tion happens in the code generated for RISC-V: all the load                6.2 OS code generation
instructions between Lines 24 and 31 in Listing 22a are gen-
erated from Listing 20, Lines 39 to 41, but never used in the              Generating code for our context switch model requires more
compare/branch for which they were intended.                               complex features from EB2LLVM. Since the context switch
                                                                           must communicate with the hardware directly, the code gen-
                                                                           erator must know how to, e.g., translate and interpret register
4 Support for function parameters and return values are future work for    accesses, interrupts, and specific instructions. The model also
EB2LLVM.                                                                   uses array accesses, sets and relations, and equations that


                                                                                                                                        123
310                                                                                                                   R. M. Gomes et al.


 1 factorial : # @factorial
 2 . cfi_startproc                                                1 f a c t o r i a l () : # @ f a c t o r i a l ()
 3 # %bb .0:       # %INITIALISATION                              2                 addi        s p , s p , -16
 4 lui s 2 , %hi ( cnt )                                          3                 sw          r a , 12( s p )
 5 sw z e r o , %lo ( cnt ) ( s 2 )                               4                 sw          s 0 , 8( s p )
 6 lui s 1 , %hi ( res )                                          5                 sw          s 1 , 4( s p )
 7 addi a 0 , z e r o , 1                                         6                 lui         a 0 , %hi ( cnt )
 8 sw a 0 , %lo ( res ) ( s 1 )                                   7                 sw          z e r o , %lo ( cnt ) ( a 0 )
 9 lui s 3 , %hi ( i n p u t )                                    8                 lui         a 0 , %hi ( res )
10 lw a 1 , %lo ( i n p u t ) ( s 3 )                             9                 addi        a1 , z e r o , 1
11 blt a 1 , a 0 , . L B B 0 _ 3                                 10                 sw          a 1 , %lo ( res ) ( a 0 )
12 . L B B 0 _ 1 : # %calc                                       11                 lui         a 0 , %hi ( i n p u t )
13 # = > This Inner Loop H e a d e r : D e p t h =1              12                 lw          s 1 , %lo ( i n p u t ) ( a 0 )
14 lw a 0 , %lo ( cnt ) ( s 2 )                                  13                 blt         s 1 , a1 , . LBB0_4
15 addi s 0 , a 0 , 1                                            14                 mv          s0 , z e r o
16 lw a 1 , %lo ( res ) ( s 1 )                                  15 . L B B 0 _ 2 : # = > T h i s I n n e r L o o p H e a d e r :
17 mv a 0 , s 0                                                      D e p t h =1
18 call _ _ m u l s i 3                                          16                 addi        s0 , s0 , 1
19 sw a 0 , %lo ( res ) ( s 1 )                                  17                 mv          a0 , s 0
20 sw s 0 , %lo ( cnt ) ( s 2 )                                  18                 call        __mulsi3
21 lw a 0 , %lo ( i n p u t ) ( s 3 )                            19                 mv          a1 , a 0
22 blt s 0 , a 0 , . L B B 0 _ 1                                 20                 blt         s 0 , s 1 , . LBB0_2
23 # %bb .2:       # %calc_fFinal                                21                 lui         a 0 , %hi ( res )
24    lui a 0 , %hi ( i n p u t )                                22                 sw          a 1 , %lo ( res ) ( a 0 )
25 lw a 0 , %lo ( i n p u t ) ( a 0 )                            23                 lui         a 0 , %hi ( cnt )
26 lui a 1 , %hi ( cnt )                                         24                 sw          s 0 , %lo ( cnt ) ( a 0 )
27 lw a 1 , %lo ( cnt ) ( a 1 )                                  25 . L B B 0 _ 4 :
28 ret                                                           26                 lw          s 1 , 4( s p )
29 . L B B 0 _ 3 : # %INITIALISATION_fFinal                      27                 lw          s 0 , 8( s p )
30 lw a 0 , %lo ( i n p u t ) ( s 3 )                            28                 lw          r a , 12( s p )
31    lw a 1 , %lo ( cnt ) ( s 2 )                               29                 addi        s p , s p , 16
32 ret                                                           30                 ret

(a) Compiled from auto-generated IR for RISC-V                       (b) Compiled from the C code for RISC-V (C GGGGGGGA
                                                                                                                  clang ASM)
(Event-B GGGGGGGGGGGGA
           EB2LLVM     LLVM GGGGA
                               llc ASM)



                                  Listing 22: RISC-V assembly code for the factorial function


need to be used in the code generation, as opposed to the           interrupt, and automatically generate a return from inter-
factorial model, where these were only used for the model           rupt instruction when it finds an event named reti.
verification.                                                          The context switch model is much larger than the fac-
   For the two architectures shown in Fig. 7, each inner-most       torial, and, to demonstrate its code generation, we selected
box (representing the concrete events) results in one block         one crucial snippet of it: the save action from Listing 15a.
of code. They are executed sequentially, and the enabling           Besides showing the remaining features of EB2LLVM, this
analysis from ProB reflects that dubbing each connection            is also the action that allows the model to remain mostly
guaranteed, while other possible connections are impos-             generic up to refinement Level 4 and yet detailed enough to
sible. The guaranteed connections generate unconditional            generate architecture-specific code from refinement Level 5.
branches from the origin block to the destination.                  In the save action, the context is saved into t_saved. We
   In our models, events model what the hardware does               know from the model that t_saved is a two-dimensional
when an interrupt occurs and when a return from inter-              array, with one block of SAVEDCTX elements for each task
rupt instruction is issued. The actions within these events         in the system (see Fig. 3b). The running task rTask is our
should, therefore, not produce any code. Furthermore, an            reference here, and each context element is to be stored in
event modeling a specific instruction, such as the return from      the array t_saved[rTask]. EB2LLVM will use the HW
interrupt, should be translated to the equivalent instruction.      models (Listing 16) to unroll the action into several store
This is achieved by using pre-defined names for these events        instructions, according to the other elements of the expres-
to indicate to the code generator which instruction to use.         sion. It applies transform to save each cpuCtx and temp
For example, the code generator will ignore events called           value into their appropriate saved context index, filtering only
                                                                    MANUAL* cpuCtx values due to the restriction operator ().



123
A framework for embedded software portability...                                                                                                    311


The results of this process for both MSP430 and RISC-V are                    1 %R8 = call i16 @llvm . r e a d _ r e g i s t e r . i16 ( r8 )
shown in Listing 15b and Listing 15c, respectively.                           2 %rTsk = load i16 , i16 * @ r T a s k
                                                                              3 // t _ s a v e d [ rTask ]
   However, the definition of transform involves fur-                         4 % g e p R T = g e t e l e m e n t p t r i16 , i16 * @t_saved ,
                                                                              5 i16 %rTsk
ther axioms and its evaluation during code generation                         6 // t _ s a v e d [ rTask ][ mR8 ] , with mR8 =5
is rather complex. Listing 23 shows it step by step for                       7 % g e p M R 8 = g e t e l e m e n t p t r i16 , i16 * %gepRT ,
                                                                              8 i16 5
saving one MSP430 register. First, the save action is                         9 store i16 %R8 , i16 * % g e p M R 8
unrolled, resulting in several expressions like ①. Then, the
code generator matches the right-hand side (②) to axm7
                                                                                   Listing 24: LLVM IR generated from Listing 23 , ⑤
from Listing 7, also using the hardware-specific defini-
tion of ctx2saved (axm22 in Listing 16a) to solve
③. Finally, ctxTransform (④) is evaluated in a sim-                          1 mov & rTask , r 1 2
                                                                                                         1 lui a 0 , %hi ( t _ s a v e d )
                                                                                                         2 addi a 0 , a 0 , %lo ( t _ s a v e d )
ilar way. In this particular case it does nothing (i.e.,                     2 add r 1 2 , r 1 2         3 lui a 1 , %hi ( rTask )
                                                                             3 mov r 8 , t _ s a v e d
ctxTransform(el)(ctx(el)) = ctx(el)), so the final                             +10( r 1 2 )
                                                                                                         4 lw a 1 , %lo ( rTask ) ( a 1 )
                                                                                                         5 slli a 1 , a 1 , 2
expression that will be translated into LLVM IR shows in                                                 6 add a 0 , a 0 , a 1
                                                                                                         7 sw s 0 , 28( a 0 )
⑤. If a modification was defined by ctxTransform in the                       (a) MSP430: save r8
model, it would be taken into account and the appropriate                     (see Listing 24)
                                                                                                            (b) RISC-V: save register x8 (s0)
instruction would be generated.
                                                                                Listing 25: Generated assembly code to save one register


                                                                                 Finally, assembly code is generated from the automati-
                                                                              cally generated LLVM IRs by llc. This time, we turn off
                                                                              optimizations (-O0) to assure that unintended modifications
                                                                              to the model’s logic will not occur. For the MSP430, each
                                                                              block that saves one register (such as in Listing 24) is trans-
                                                                              lated to assembly as shown in Listing 25a. The index for the
                                                                              array access in Line 3 is automatically calculated by llc
                                                                              as mR8 ∗ ByteW idth, and since the MSP430 is a 16-bit (2
                                                                              bytes) architecture: 5∗2 = 10 (Line 3). Listing 25b shows the
                                                                              RISC-V generated code to save register x8 in the save index
                                                                              mX8 = 7. Our model only uses the architecture’s specified
                                                                              register names, but llc uses the Abstract Binary Interface
                                                                              (ABI) names (x8 = s0). The index calculated for RISC-V’s
The save operation can then be translated into LLVM IR5                       32-bit (4 bytes) architecture is 7 ∗ 4 = 28 (Line 7).
as shown in Listing 24. The register access cpuCtx(R8)                           The generated code could still be optimized: Lines 1 to 2
(Listing 23, ⑤) is converted to a call to the intrinsic LLVM                  in Listing 25a and Lines 1 to 6 in Listing 25b are repeated for
function read_register (→ Line 1). In Lines 4 and 7                           each register saved, though they could be present only once.
we can see that the accesses to elements in a relation are                    Furthermore, while the model assures, for example, that no
converted to LLVM’s GEP instruction6 , and the value from                     register will be overwritten before it is saved, the code gen-
the register is finally stored in the appropriate array position              erator might need to use temporary variables for temporary
mR8. Note that the save index mR8 is defined, in the model,                   storage of register values. Thus, a tighter integration between
as a constant value, and therefore expressed as the immediate                 EB2LLVM and llc is needed to assure that any modification
value 5 in Line 7. This is repeated for each element that must                caused by a generated instruction is intentional according to
be saved, according to the model. The LLVM IR code for                        the model.
RISC-V is similar to Listing 24: The register name and its
index, as well as the data sizes are replaced according to the
RISC-V model.
                                                                              7 Conclusion and outlook
5 To make the LLVM IR listings more readable, we have replaced meta-
                                                                              We have presented our framework for OS portability based
data with their actual values, renamed virtual registers to better reflect
what they represent, and added comments to some lines.
                                                                              on formal methods and code generation.
6 The getelementptr (GEP) instruction is often misunderstood,                    First, with regard to RQ1 from the introduction, we have
but here it is enough to understand it as calculating the address of an       shown a generic formal RTOS model in Event-B with context
array element.                                                                switches that decouples low-level functionality from hard-


                                                                                                                                          123
312                                                                                                                 R. M. Gomes et al.


ware specifics. This allows us to reuse the model and its         ability. In fact, we have shown how the same formal models
proofs for several architectures. Then, we instantiated the       can be be used for both code generation (RQ2) and verifica-
model for two architectures and verified them via interactive     tion (RQ1). On the long-term, we believe that the approach
theorem proving and model checking. The safety and live-          will essentially simplify the creation and maintenance of
ness verification of the models (1) proved that the generic       software. This will not only save costs, but it will also be bene-
model and its instantiations do not corrupt task contexts by      ficial for future systems in various domains (e.g., automotive,
having them properly saved and loaded; (2) proved that the        avionics, the IoT, etc.), where guaranteed dependability is
kernel and the tasks run in the appropriate CPU states and        crucial. The effort invested in modeling can be mitigated by
privilege levels by having them properly changed; (3) proved      increasing the number of ports and partially replacing test-
that the kernel executes in the correct order and finishes exe-   ing by verification for guaranteed dependability during the
cution. This verification also helped us detect and eliminate     development process. Therefore, we continue our work to
issues early in the design.                                       support more target architectures and to verify the generated
   Within the proof of concept for the next stage of the          code.
framework, and with regard to RQ2 from the introduction,              With regard to the validity and applicability of our
we showed how code is automatically generated from the            approach, a potential issue we must mention is the time
models: EB2LLVM generates LLVM IR code from the veri-             and computation power required for model checking. The
fied models. The IR is then compiled with the target-specific     axioms in the presented model already cause a state explo-
compiler backend, generating assembly code for the con-           sion in ProB if all registers available in the target architectures
text switch of SmartOS. Additionally, we presented another,       are included, which prompted us to create a minimal set for
hardware-independent model, applying the entire framework         model checking. With bigger and more complex models of,
on the generally known high-level algorithm to calculate the      e.g., bigger and more complex OS kernels or targets, even a
factorial of a number. We compared the automatically gener-       minimal set might eventually not avoid state explosion. We
ated code with equivalent code compiled from the function         hope that advances in formal methods will eventually solve
implemented in C. Though less efficient, the code generated       this problem. Other methods, such as TLA+, Isabelle/HOL,
from Event-B for both MSP430 and RISC-V can be compiled           and HOL4 are potentially suitable for the model presented
into binaries and work as intended, successfully generating       in this work, and should be investigated in future works.
a binary that corresponds to the model.                               We have already investigated more complex architectures,
   An important aspect of our approach is to initially keep       such as the Infineon Aurix [35]. In fact, though the work is
the software models and the hardware models independent           not yet complete, our initial models do already consider some
from each other. From a potential pool of OS models and           Aurix-specific concepts, and show the general applicability
architecture models we can then pick one, respectively, and       of our approach. In order to actually generate code for it, the
only combine them in a last instantiation step before code        instantiation step will likely be more complex than for the two
generation. This way, most of the modeling and verification       simple architectures we have presented in this work. Since
efforts are concentrated in the generic parts of the mod-         the Aurix supports special instructions and a linked list data
els, and supporting a new architecture requires much less         structure in hardware to handle contexts, the code generator
effort compared to traditional approaches, where hardware         would also have to be extended to generate the appropriate
and software are inherently mixed in one model which must         code.
then be created from scratch. In addition, the automatic code         In any case, we still need to work on verifying the code
generation from one OS model to many architectures assures        generator itself, so we can guarantee the correct translation
consistency between the ports, and makes it easier to adapt       of the model into LLVM IR. Regarding the final compilation
to new or changing OS specifications. The framework can           step into an executable binary, we rely on the LLVM commu-
thus accelerate the optimization of the software, as different    nity, where several works already try to provide verification
design options can be quickly evaluated on real hardware          for the compiler backend [3, 40, 43]. The verification of the
without the need to adapt all ports individually and manu-        toolchain parts we have developed is still open and not part
ally. This even shows that RQ1 and RQ2 can be addressed in        of this work.
combination.                                                          Apart, we have already started to extend our modeling
   Formal modeling of software is still not very common in        concept to also support the verification of (non-)functional
real-world projects – especially when it comes to generating      aspects in (other) OS kernels and application software, such
executable code. The effort often seems too high compared         as timing and liveness. We are therefore working on modeling
to traditional implementation and acceptance on the devel-        timed automata to analyze the interaction of the application
opers’ side must first be built. However, studies have already    and OS layers through syscalls as well as on the response
shown that formal methods can drastically increase software       times of kernel functions and concurrently running tasks [62].
quality and have a great positive impact on its overall depend-   A possible threat to the applicability of our approach to gen-


123
A framework for embedded software portability...                                                                                                   313


eral OSs could be their sheer set of features and the commonly                  and embedded execution. In: Proceedings of the 23rd ACM/IEEE
very complex interactions in between. Regarding SmartOS,                        International Conference on Model Driven Engineering Languages
                                                                                and Systems: Companion Proceedings, MODELS ’20, New York.
we aim to model the entire kernel by separating its parts                       Association for Computing Machinery (2020)
and features into distinct model modules with well-defined                   9. Bodenstab, D.E., Houghton, T.F., Kelleman, K.A., Ronkin, G.,
input/output interfaces. This way, we can model and verify                      Schan, E.P.: The UNIX system: UNIX operating system porting
all modules independently first (e.g., the kernel body), and                    experiences. AT T Bell Lab. Tech. J. 63(8), 1769–1790 (1984)
                                                                            10. Brandenburg, B.B.: The case of an opinionated, theory-oriented
only later verify their interaction (e.g., with the context switch              real-time operating system. NGOSCPS19, 04 (2019)
model presented here). Early experiences with AUTOSAR                       11. Butler, M., Körner, P., Krings, S., Lecomte, T., Leuschel, M., Mejia,
[70] have shown that other low-level functionality of the OS,                   L.-F., Voisin, L.: The first twenty-five years of industrial use of the
such as device drivers, can also be modeled and verified sim-                   B-Method. In: ter Beek, M.H., Ničković, D. (eds.) Formal Meth-
                                                                                ods for Industrial Critical Systems, pp. 189–209. Springer, Cham
ilarly to the context switch presented here. The individually                   (2020)
verified model modules would then be combined for the ver-                  12. Cheng, S., Woodcock, J., D’Souza, D.: Using formal reasoning on
ification of overarching aspects in complete software stacks.                   a model of tasks for FreeRTOS. Formal Aspects Comput. 27(1),
                                                                                167–192 (2014)
Funding Open access funding provided by Graz University of Tech-            13. Cho, D., Bae, D.: Case study on installing a porting process for
nology.                                                                         embedded operating system in a small team. In: 2011 Fifth Inter-
                                                                                national Conference on Secure Software Integration and Reliability
Open Access This article is licensed under a Creative Commons                   Improvement-Companion, pp. 19–25 (2011)
Attribution 4.0 International License, which permits use, sharing, adap-    14. Chou, A., Yang, J., Chelf, B., Hallem, S., Engler, D.: An empirical
tation, distribution and reproduction in any medium or format, as               study of operating systems errors. SIGOPS Oper. Syst. Rev. 35(5),
long as you give appropriate credit to the original author(s) and the           73–88 (2001)
source, provide a link to the Creative Commons licence, and indi-           15. Craig, I.D.: Formal Refinement for Operating System Kernels.
cate if changes were made. The images or other third party material             Springer, New York, Secaucus (2007)
in this article are included in the article’s Creative Commons licence,     16. Craig, I.D.: Formal Models of Operating System Kernels, 1st edn.
unless indicated otherwise in a credit line to the material. If material        Springer Publishing Company, Incorporated, Berlin (2010)
is not included in the article’s Creative Commons licence and your          17. Dalvandi, M., Butler, M.J., Fathabadi, A.S.: SEB-CG: code gen-
intended use is not permitted by statutory regulation or exceeds the            eration tool with algorithmic refinement support for event-b. In:
permitted use, you will need to obtain permission directly from the copy-       Sekerinski, E., Moreira, N., Oliveira, J.N., Ratiu, D., Guidotti, R.,
right holder. To view a copy of this licence, visit http://creativecomm         Farrell, M., Luckcuck, M., Marmsoler, D., Campos, J., Astarte, T.,
ons.org/licenses/by/4.0/.                                                       Gonnord, L., Cerone, A., Couto, L., Dongol, B., Kutrib, M., Mon-
                                                                                teiro, P., Delmas, D. (eds) Formal Methods. FM 2019 International
                                                                                Workshops-Porto, Portugal, October 7–11, 2019, Revised Selected
                                                                                Papers, Part I, volume 12232 of Lecture Notes in Computer Sci-
References                                                                      ence, pp 19–29. Springer (2019)
                                                                            18. Danmin, C., Yue, S., Zhiguo, C.: A formal specification in b of
 1. Abrial, J.-R.: The B Book-Assigning Programs to Meanings. Cam-              an operating system. Open Cybern. System. J. 9(1), 1125–1129
    bridge University Press, Cambridge (1996)                                   (2015)
 2. Abrial, J.-R.: Modeling in Event-B: System and Software Engi-           19. Dhote, S., Charjan, P., Phansekar, A., Hegde, A., Joshi, S.,
    neering, 1st edn. Cambridge University Press, New York (2010)               Joshi, J.: Using FPGA-SoC interface for low cost IoT based
 3. Ahmed, A.: Verified compilers for a multi-language world. In: Ball,         image processing. In: 2016 International Conference on Advances
    T., Bodik, R., Krishnamurthi, S., Lerner, B.S., Morrisett, G. (eds)         in Computing, Communications and Informatics (ICACCI), pp.
    1st Summit on Advances in Programming Languages (SNAPL                      1963–1968 (2016)
    2015), volume 32 of Leibniz International Proceedings in Infor-         20. Event-B. B2Latex—Event-B. https://wiki.event-b.org/index.php/
    matics (LIPIcs), pp 15–31, Dagstuhl, Germany, (2015). Schloss               B2Latex
    Dagstuhl–Leibniz-Zentrum fuer Informatik                                21. Event-B. Event-B and the Rodin Platform. www.event-b.org
 4. Akdur, D., Garousi, V., Demirörs, O.: A survey on modeling              22. Fathabadi, A.S., Butler, M.J., Yang, S., Maeda-Nunez, L.A.,
    and model-driven engineering practices in the embedded software             Bantock, J., Al-Hashimi, B.M., Merrett, G.V.: A model-based
    industry. J. Syst. Architect. 91, 62–82 (2018)                              framework for software portability and verification in embedded
 5. Alkhammash, E.H., Butler, M.J., Cristea, C.: International Confer-          power management systems. J. Syst. Architect. 82, 12–23 (2018)
    ence on Communication, Management and Information Technol-              23. Frühwirth, T., Krammer, L., Kastner, W.: Dependability demands
    ogy, Chapter Modeling Guidelines of FreeRTOS in Event-B, pp.                and state of the art in the internet of things. In: 2015 IEEE 20th Con-
    453–462. CRC Press (2017)                                                   ference on Emerging Technologies Factory Automation (ETFA),
 6. Aravantinos, V., Voss, S., Teufl, S., Hölzl, F., Schätz, B.: AutoFO-        pp. 1–4 (2015)
    CUS 3: tooling concepts for seamless, model-based development           24. Gabel, M., Yang, J., Yu, Y., Goldszmidt, M., Su, Z.: Scalable
    of embedded systems. In: ACES-MB&WUCOR@MoDELS 2015,                         and systematic detection of buggy inconsistencies in source code.
    CEUR Workshop Proceedings, pp. 19–26. CEUR-WS.org (2015)                    In: Proceedings of the ACM International Conference on Object
 7. Basile, D., ter Beek, M.H., Fantechi, A., Gnesi, S., Mazzanti, F.,          Oriented Programming Systems Languages and Applications,
    Piattino, A., Trentini, D., Ferrari, A.: On the industrial uptake of        OOPSLA10, pp. 175–190. Association for Computing Machinery,
    formal methods in the railway domain. In: Furia, C.A., Winter,              New York (2010)
    K. (eds.) Integrated Formal Methods, pp. 20–29. Springer, Cham          25. GNU Project. Bison. https://www.gnu.org/software/bison/
    (2018)                                                                  26. GNU Project. The fast lexical analyzer. https://github.com/westes/
 8. Besnard, V., Jouault, F., Brun, M., Teodorov, C., Dhaussy, P., Dela-        flex
    tour, J.: Modular deployment of uml models for v&v activities


                                                                                                                                          123
314                                                                                                                                  R. M. Gomes et al.


27. Gomes, R.M., Aichernig, B., Baunach, M.: A formal modeling               45. Lattner, C.: Introduction to the LLVM compiler system. In:
    approach for portable low-level OS functionality. In: de Boer,               Advanced Computing and Analysis Techniques in Physics
    F., Cerone, A. (eds) Software Engineering and Formal Methods,                Research (ACAT) (2008)
    pp.155–174. Springer, Cham (2020)                                        46. Lecomte, T., Deharbe, D., Prun, E., Mottin, E.: Applying a for-
28. Gomes, R.M., Baunach, M.: A framework for OS portability: from               mal method in industry: a 25-year trajectory. In: Cavalheiro, S.,
    formal models to low-level code. In: The 37th ACM/SIGAPP Sym-                Fiadeiro, J. (eds.) Formal Methods: Foundations and Applications,
    posium On Applied Computing (2022)                                           pp. 70–87. Springer, Cham (2017)
29. Gomes, T., Pinto, S., Gomes, T., Tavares, A., Cabral, J.: Towards an     47. Leuschel, M., Butler, M.: ProB: an automated analysis toolset for
    FPGA-based edge device for the internet of things. In: 2015 IEEE             the B method. Int. J. Softw. Tools Technol. Transf. 10(2), 185–203
    20th Conference on Emerging Technologies Factory Automation                  (2008)
    (ETFA), pp. 1–4 (2015)                                                   48. Lewis, B.: Software portability gains realized with METAH and
30. Goranko, V., Galton, A.: Temporal logic. In: Zalta, E.N. (ed) The            Ada95. In: Proceedings of the 11th International Workshop on
    Stanford Encyclopedia of Philosophy. Metaphysics Research Lab,               Real-time Ada Workshop, IRTAW ’02, pp. 37–46. ACM, New York
    Stanford University, winter 2015 edition (2015)                              (2002)
31. Gu, R., Shao, Z., Chen, H., Wu, X.(Newman), Kim, J. Sjöberg,             49. Li, Z., Lu, S., Myagmar, S., Zhou, Y.: CP-Miner: a tool for finding
    V., Costanzo, D.: Certikos: an extensible architecture for building          copy-paste and related bugs in operating system code. In: OSdi,
    certified concurrent OS kernels. In: 12th USENIX Symposium on                vol. 4, pp. 289–302 (2004)
    Operating Systems Design and Implementation (OSDI 16), pp.               50. llvm-admin team. The LLVM compiler infrastructure. https://llvm.
    653–669. USENIX Association, Savannah (2016)                                 org/
32. Hahm, O., Baccelli, E., Petersen, H., Tsiftes, N.: Operating systems     51. Lyons, A., Danis, A., Yyshen, A., Hesham, S., Stephen, Z., Amir-
    for low-end devices in the internet of things: a survey. IEEE Internet       reza, M., Kent, K., Gerwin, P., Latent, B., Joel, S., Thomas, A.,
    Things J. 3(5), 720–734 (2016)                                               Kolanski, R., Boettcher, A., Susarla, P., Brecknell, M., Waugh, J.,
33. Holland, D.A.: Toward Automatic Operating System Ports via                   Holzapfel, S., Guikema, C., Richardson, C., Cloudier, V., Robbie,
    Code Generation and Synthesis. Ph.d thesis (2020)                            M., Mokshasoft, N., Tim, M., Luke, M., Jesse, J., Studer, N., Millar,
34. Hu, J., Lu, E., Holland, D.A., Kawaguchi, M., Chong, S., Seltzer,            C.: seL4/seL4: MCS pre-release (2018)
    M.I.: Trials and tribulations in synthesizing operating systems. In:     52. Manna, Z., Pnueli, A.: The Temporal Logic of Reactive and Con-
    Proceedings of the 10th Workshop on Programming Languages and                current Systems: Specification. Springer, Berlin (2012)
    Operating Systems, PLOS19, pp. 67–73. Association for Comput-            53. Martins, G. Renata, B.M.: A study on the portability of iot operating
    ing Machinery, New York (2019)                                               systems. In: Tagungsband des FG-BS Frühjahrstreffens 2021, Bonn
35. Infineon. AURIX TriCore Microcontroller. https://www.                        (2021). Gesellschaft für Informatik e.V
    infineon.com/cms/en/product/microcontroller/32-bit-tricore-              54. MATLAB. The MathWorks Inc., Natick (2010)
    microcontroller/                                                         55. Méry, D., Singh, N.K.: Automatic code generation from event-b
36. Instruments, Texas, MSP430 ultra-low-power sensing and mea-                  models. In: Proceedings of the Second Symposium on Information
    surement MCUs (2019)                                                         and Communication Technology, SoICT ’11, pp. 179–188. ACM,
37. Jastram, M., Butler, P.M.: Rodin user’s handbook: covers Rodin               New York (2011)
    V.2.8. USA (2014)                                                        56. Novikov, E., Zakharov, I.: Verification of operating system mono-
38. Jiang, L., Su, Z., Chiu, E.: Context-based detection of clone-related        lithic kernels without extensions. In: Margaria, T., Steffen, B. (eds)
    bugs. In: Proceedings of the the 6th Joint Meeting of the European           Leveraging Applications of Formal Methods, Verification and Val-
    Software Engineering Conference and the ACM SIGSOFT Sym-                     idation. Industrial Practice, pp. 230–248. Springer, Cham (2018)
    posium on The Foundations of Software Engineering, ESEC-FSE              57. Nyberg, M., Gurov, Dilian, L., Christian, R., Andreas, W.J.: For-
    ’07, pp. 55–64. Association for Computing Machinery, New York,               mal verification in automotive industry: enablers and obstacles. In:
    (2007)                                                                       Margaria, T., Steffen, B. (eds) Leveraging Applications of Formal
39. Juergens, E., Deissenboeck, F., Hummel, B., Wagner, S.: Do code              Methods, Verification and Validation. Industrial Practice, pp. 139–
    clones matter? In: 2009 IEEE 31st International Conference on                158. Springer, Cham (2018)
    Software Engineering, pp. 485–495 (2009)                                 58. Oikonomou, G., Phillips, I.: Experiences from porting the Contiki
40. Kang, J., Kim, Y., Song, Y., Lee, J., Park, S., Shin, M.D., Kim,             operating system to a popular hardware platform. In: 2011 Inter-
    Y., Cho, S., Choi, J., Hur, C.-K., Yi, K.: Crellvm: verified cred-           national Conference on Distributed Computing in Sensor Systems
    ible compilation for llvm. In: Proceedings of the 39th ACM                   and Workshops (DCOSS), pp. 1–6 (2011)
    SIGPLAN Conference on Programming Language Design and                    59. Pnueli, A.: The temporal logic of programs. In: 18th Annual Sym-
    Implementation, PLDI 2018, pp. 631–645. Association for Com-                 posium on Foundations of Computer Science (sfcs 1977), pp.
    puting Machinery, New York (2018)                                            46–57 (1977)
41. Kleen, A.: Porting linux to x86-64. In: Proceedings of the Linux         60. Popp, M., Moreira, O., Yedema, W., Lindwer, M.: Automatic HAL
    Symposium (2001)                                                             generation for embedded multiprocessor systems. In: Proceed-
42. Klein, G., Andronick, J., Elphinstone, K., Murray, T., Sewell, T.,           ings of the 13th International Conference on Embedded Software,
    Kolanski, R., Heiser, G.: Comprehensive formal verification of an            EMSOFT ’16. ACM, New York (2016)
    OS microkernel. ACM Trans. Comput. Syst. 32(1) (2014)                    61. Ray, B., Kim, M., Person, S., Rungta, N.: Detecting and charac-
43. Lammich, P.: Generating Verified LLVM from Isabelle/HOL. In:                 terizing semantic inconsistencies in ported code. In: 2013 28th
    Harrison, J., O’Leary, J., Tolmach, A. (eds) 10th International Con-         IEEE/ACM International Conference on Automated Software
    ference on Interactive Theorem Proving (ITP 2019), volume 141                Engineering (ASE), pp. 367–377 (2013)
    of Leibniz International Proceedings in Informatics (LIPIcs), pp.        62. Ribeiro, L.B., Lorber, F., Nyman, U., Larsen, G., Baunach, M.:
    22:1–22:19. Schloss Dagstuhl–Leibniz-Zentrum fuer Informatik,                A modeling concept for formal verification of os-based composi-
    Dagstuhl (2019)                                                              tional software. In: Under review at 16th USENIX Symposium on
44. Lamport, L.: Proving the correctness of multiprocess programs.               Operating Systems Design and Implementation (OSDI) (2022)
    IEEE Trans. Softw. Eng. SE–3(2), 125–143 (1977)                          63. RISC-V Foundation. RISC-V
                                                                             64. Rivera, L.F., Villegas, N.M., Tamura, G., Jiménez, M., Müller,
                                                                                 H.A.: Uml-driven automated software deployment. In: Proceed-


123
A framework for embedded software portability...                                                                                              315


    ings of the 28th Annual International Conference on Computer          84. Zhou, Z., Liang, B., Jiang, L., Shi, W., He, Y.: A formal descrip-
    Science and Software Engineering, CASCON ’18, pp. 257–268.                tion of SECIMOS operating system. In: Gorodetsky, V., Kotenko,
    IBM Corp, USA (2018)                                                      I., Skormin, V. (eds) Computer Network Security, pp. 286–297.
65. Rivera, V., Cataño, N., Wahls, T., Rueda, C.: Code generation for         Springer, Berlin, Heidelberg (2005)
    event-b. Int. J. Softw. Tools Technol. Transf. 19(1), 31–52 (2017)
66. Scheipel, T., Batista Ribeiro, L., Sagaster, T., Baunach, M.: Smar-
    tOS: An OS architecture for sustainable embedded systems. In:
                                                                          Publisher’s Note Springer Nature remains neutral with regard to juris-
    Tagungsband des FG-BS Frühjahrstreffens 2022. Gesellschaft für
                                                                          dictional claims in published maps and institutional affiliations.
    Informatik e.V, Bonn (2022)
67. Smith, R., Smith, G., Wardani, A.: Software reuse in robotics:
    enabling portability in the face of diversity. In: IEEE Conference                                         Renata Martins Gomes received
    on Robotics, Automation and Mechatronics, 2004., vol. 2, pp. 933–                                          her engineer’s degree in Computer
    938 (2004)                                                                                                 Engineering at Universidade Fed-
68. Sritharan, S., Hoang, T.S.: Towards generating spark from event-b                                          eral de Itajuba, Brazil, and her
    models. In: Dongol, B., Troubitsyna, E. (eds.) Integrated Formal                                           Ph.D. with distinction in Informa-
    Methods, pp. 103–120. Springer, Cham (2020)                                                                tion and Communications Engi-
69. Stan, A.: Porting the core of the Contiki operating system to the                                          neering at Graz University of Tech-
    TelosB and MicaZ platforms. International University, Bremen,                                              nology, Austria. Her research inter-
    Bachelor thesis (2007)                                                                                     ests focus on portability and cor-
70. Staron, M., Durisic, D.: AUTOSAR standard. In: Automotive Soft-                                            rectness of real-time operating sys-
    ware Architectures, pp. 81–116. Springer (2017). https://doi.org/                                          tems, including code generation
    10.1007/978-3-319-58610-6_4                                                                                and formal verification of hard-
71. Stoddart, B., Cansell, D., Zeyda, F.: Modelling and proof analysis                                         ware and software models. As soft-
    of interrupt driven scheduling. In: Julliand, J., Kouchnarenko, O.                                         ware engineer in industry, she
    (eds.) B 2007: Formal Specification and Development in B, pp.                                              focuses on compositional and
    155–170. Springer, Berlin, Heidelberg (2006)                          RTOS-based embedded systems.
72. Su, W., Abrial, J.-R., Pu, G., Fang, B.: Formal development of
    a real-time operating system memory manager. In: 2015 20th
    International Conference on Engineering of Complex Computer                                               Bernhard Aichernig is a tenured
    Systems (ICECCS). IEEE (2015)                                                                             associate professor (ao. Univ.-Prof.)
73. Syeda, H.T., Klein, G.: Formal reasoning under cached address                                             at Graz University of Technol-
    translation. J. Autom. Reason. (2020)                                                                     ogy, Austria. He and his research
74. Takata, H., Sugai, N., Yamamoto, H.: Porting Linux to the M32R                                            group investigates the foundations
    processor. In: Lockhart, J.W. (ed) Linux Symposium, pp. 398. The                                          of software engineering for real-
    Linux Foundation (2003)                                                                                   ising dependable computer-based
75. Torvalds, L.: Linux: a Portable Operating System. Master’s thesis,                                        systems. Bernhard is an expert in
    University of Helsinki (1997)                                                                             formal methods and testing. His
76. Verhulst, E., Boute, R.T., Faria, J.M., Sampaio, S., Bernhard,                                            research covers a variety of areas
    M.: Vitaliy: Formal Development of A Network-Centric RTOS.                                                combining falsification, verifica-
    Springer, New York (2011)                                                                                 tion and abstraction techniques.
77. Waterman, A., Asanović, K.: The RISC-V instruction set manual                                            Current topics include the Inter-
    volume I: user-level ISA version 2.2 (2017)                                                               net of Things, model learning, and
78. Waterman, A., Lee, Y., Avizienis, R., Patterson, D.A., Asanović,                                         statistical model checking. Bern-
    K.: The RISC-V instruction set manual volume II: privileged archi-    hard holds a habilitation in Practical Computer Science and Formal
    tecture version 1.7. Technical Report UCB/EECS-2015-49, EECS          Methods, a doctorate, and a diploma engineer degree from Graz Uni-
    Department, University of California, Berkeley (2015)                 versity of Technology.
79. Woodcock, J., Larsen, P.G., Bicarregui, J., Fitzgerald, J.: Formal
    methods: practice and experience. ACM Comput. Surv. 41(4), 19:1-                                           Marcel Baunach is professor for
    19:36 (2009)                                                                                               Embedded Automotive Systems
80. Wright, S.: Formal construction of instruction set architectures.                                          and head of the EAS Group at the
    Ph.d. thesis, University of Bristol (2009)                                                                 Institute of Technical Informatics
81. Wright, S.: Automatic generation of C from Event-B. In: Workshop                                           at Graz University of Technol-
    on integration of model-based formal methods and tools, pp. 14                                             ogy, Austria. His research areas
    (2009)                                                                                                     include hardware and software for
82. Zhang, F., Niu, W.: A survey on formal specification and verifi-                                           highly dependable and sustainable
    cation of system-level achievements in industrial circles. Acad. J.                                        embedded systems. The focus is
    Comput. Inf. Sci. (2019)                                                                                   on real-time operating systems and
83. Zhang, S., Kobetski, A., Johansson, E., Axelsson, J., Wang, H.:                                            processor architectures, in partic-
    Porting an AUTOSAR-compliant operating system to a high per-                                               ular on concepts for the design,
    formance embedded platform. SIGBED Rev. 11(1), 62–67 (2014)                                                verification and portability of sys-
                                                                                                               tem software, dynamic composi-
                                                                                                               tion of modular software, as well
                                                                          as application-specific and reconfigurable processors. Application
                                                                          areas include, e.g., future vehicles, the Internet of Things or cyber-
                                                                          physical systems.



                                                                                                                                      123
