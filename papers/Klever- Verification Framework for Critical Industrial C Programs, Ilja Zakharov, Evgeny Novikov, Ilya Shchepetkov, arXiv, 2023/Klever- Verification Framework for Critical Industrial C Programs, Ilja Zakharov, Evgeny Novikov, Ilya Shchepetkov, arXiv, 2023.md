                                         Klever: Verification Framework for Critical
                                         Industrial C Programs

                                         Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov
arXiv:2309.16427v1 [cs.SE] 28 Sep 2023




                                         Abstract Automatic software verification tools help to find hard-to-detect faults in
                                         programs checked against specified requirements non-interactively. Besides, they can
                                         prove program correctness formally under certain assumptions. These capabilities
                                         are vital for verification of critical industrial programs like operating system kernels
                                         and embedded software. However, such programs can contain hundreds or thousands
                                         of KLOC that prevent obtaining valuable verification results in any reasonable time
                                         when checking non-trivial requirements. Also, existing tools do not provide widely
                                         adopted means for environment modeling, specification of requirements, verification
                                         of many versions and configurations of target programs, and expert assessment
                                         of verification results. In this paper, we present the Klever software verification
                                         framework, designed to reduce the effort of applying automatic software verification
                                         tools to large and critical industrial C programs.



                                         1 Introduction

                                         Tools that implement an automatic software verification technique also known
                                         as software model checking aim at finding violations of specified requirements
                                         non-interactively and proving program correctness under certain assumptions for-
                                         mally [24]. Automatic software verification tools (for brevity, we will refer to them
                                         as verification tools below) participating in annual competitions on software ver-
                                         ification (SV-COMP) demonstrate excellent results for verification tasks included
                                         in the benchmark suite [5]. Some verification tools miss a few faults and report
                                         fewer false alarms. The benchmark suite contains moderate-sized programs that are
                                         prepared in advance and checked against the predefined list of properties. However,


                                         This work was carried out while authors were working at Ivannikov Institute for System Program-
                                         ming of the Russian Academy of Sciences, Moscow, Russia
                                         e-mail: {ilja.s.zakharov,eunovm,ilya.shchepetkov}@gmail.com


                                                                                                                                      1
2                                                Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

these verification tools cannot be applied to large software projects without prior
preparation.
   This paper considers the verification of large critical industrial C programs such
as operating system kernels, embedded software, web servers, database management
systems, libraries and utilities on which many people rely in their daily lives and
at work. Such programs can contain hundreds or thousands of KLOC and might
evolve rapidly (Table 1). Neither advanced algorithms implemented by developers
of verification tools nor a substantial increase in computing power can guarantee
obtaining valuable verification results in a reasonable time if large enough parts of
these programs’ source code are strongly relevant to checked properties.


Table 1 Characteristics of several open-source programs1.
             Program name and version Size (MLOC) Lines changed2 (MLOC)
                                                      2.6 added (9.7 %)
             Linux 5.7.7 kernel             27
                                                     1.2 deleted (4.4 %)
                                                       5.3 added (22 %)
             FreeBSD 12.1                   25
                                                       3 deleted (12 %)
                                                       2.2 added (15 %)
             GCC 10.1                       14
                                                     0.99 deleted (6.9 %)
                                                     0.13 added (4.2 %)
             GTK 3.24.21                    3.2
                                                     0.1 deleted (3.2 %)
                                                     0.13 added (5.3 %)
             PostgreSQL 12.3                2.2
                                                     0.07 deleted (3.3 %)
                                                      0.24 added (12 %)
             glibc 2.31                      2
                                                     0.25 deleted (13 %)


   The interest in the application of verification tools to critical industrial programs
continually grows due to the following reasons:
• Faults in these programs can result in significant economic losses [9, 36].
• Traditional software quality assurance techniques such as code review, testing
  and static analysis often cannot provide correctness guarantees [8, 19].
• Heavyweight formal verification methods like deductive verification are capable
  of proving functional correctness under certain assumptions. But such methods
  are successfully applied either to fairly small programs whose size is up to
  12 KLOC [1, 21, 27] or to critical components of large programs [16, 17, 20]
  since verification of them as a whole would require enormous efforts.
   Target programs can extensively interact with their environment during operation,
while verification tools are unaware of any restrictions imposed on the corresponding
interactions. Users may need to check that their programs satisfy specific require-
ments in addition to supported properties. Program environment and requirements
can vary for different versions and configurations of target programs. However, there

1 Most of the source code of these programs is written in C. Data was collected using cloc and git.
2 Number of lines added and removed during a period of one year before the release. These numbers
were divided by total sizes of programs to exemplify a pace of changes.
Klever: Verification Framework for Critical Industrial C Programs                    3

is a lack of widely adopted methods and tools for preparing programs for large-
scale verification. At last, existing verification tools do not provide users with a
comprehensive enough suite of means for expert assessment of verification results.
   To reduce efforts that are necessary for the application of automatic software
verification tools for large industrial C programs, we have been developing the
Klever software verification framework and project-specific adaptations considered
in Sections 2 and 3 correspondingly. Section 4 demonstrates the publicly available
achievements of Klever and estimates various aspects of its usage. Section 5 outlines
the related work. In conclusion, we summarize our overall vision of the practical
application of automatic software verification tools.
   The main contribution of the paper is an approach and its implementation in the
Klever verification framework, tailored to apply verification tools to large industrial
programs. This approach is a complex set of methods that tackle each step of a path,
from selecting the scope of the source code to be checked to analyzing verification
results. We provided a solution for each significant challenge that a user might face
on this way. Consequently, the paper might look too broad and cover too many
aspects. But focusing on a single individual problem, like environment modeling or
program decomposition, does not allow seeing the big picture and simplifying the
overall verification process in practice. Therefore, our main contribution is a solid
approach to the application of automatic software verification tools to industrial C
programs that breaks down into corresponding methods for: program decomposition;
environment modeling; stating requirement specifications; presenting verification
results and enabling their triage.
   In addition, the presented verification framework can work with any verification
tool that supports its interface, which is pretty close to the one adopted by the
SV-COMP community. The most vital requirements for us are the possibility to
apply the tool directly to the source code, get verification results non-interactively,
and visualize them. We stick to these criteria mostly for technical reasons and
do not limit the variety of verification approaches and techniques that such tools
can implement under the hood. Discussing the application of other analysis and
verification tools to various software is not our goal in the paper as it is too broad,
so we limit the overview of related work to the particular problem of applying the
aforementioned tools to industrial programs.



2 Klever: A Software Verification Framework

Fig. 1 presents the overall workflow of Klever [32]. Rectangles filled with red
represent manual actions. Green rectangles mean automatic steps executed by Klever.
The only blue rectangle corresponds to the invocation of verification tools. The
rectangle with a dotted border represents an optional step necessary if users would
like to improve verification results.
4                                            Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov


                Verification process setup


                      Program decomposition


                     Environment models generation


                          Verification tasks generation


                                Verification tasks solution


                                  Verification results processing


                                        Verification results analysis


                                     Project-specific adaptations development



Fig. 1 Klever workflow.



   The Klever software verification framework uses SV-COMP compliant verifica-
tion tools as backends and automates the following steps (they are considered in
detail in corresponding subsections below):
• Decomposition of programs into fragments of a moderate size.
• Generation of environment models for various kinds of interactions with an
  environment.
• Generation of verification tasks that includes configuration of verification tools.
• Scheduling and monitoring to enable parallel generation and solution of verifica-
  tion tasks.
• Preliminary processing of verification results.
• Managing verification processes and expert assessment of verification results.
   Klever supports verification of programs developed in the GNU C programming
language on x86 64, ARM, and ARM64 Linux platforms.
   Project-specific adaptations include configurations, specifications and plugins for
checking specific software. If a project adaptation has already been implemented,
users need to deploy Klever and can start using it as is without any additional
Klever: Verification Framework for Critical Industrial C Programs                   5

manual efforts. Otherwise, several iterations dedicated to the development of the
project-specific adaptation are necessary.
    During design and development, we cared about supporting the verification of
different versions and configurations of target programs. This is highly demanded by
the fast-changing industry. Klever does not introduce any changes to the program’s
source code or build processes. Thus, it can pick up a new version or configuration
of a program smoothly to run its verification without extra steps except for adjusting
an appropriate project-specific adaptation if necessary.
    The Klever software verification framework is an open-source project3 primar-
ily implemented in Python 3. Configurations from project-specific adaptations are
stored as JSON files. Specifications are developed using appropriate domain-specific
languages. Project-specific adaptation plugins are implemented as Python 3 mod-
ules. The Klever project repository contains numerous tests written in C. These tests
are checked automatically by a CI/CD system before any substantial update to the
main branch. Klever user documentation can be found at this link4.
    The following subsections describe particular steps of the automated Klever
workflow and related components of the Klever software verification framework. It
is worth noting that different Klever components depend on several auxiliary tools
considered in Appendix A. One can omit any of these subsections if they are not of
interest.



2.1 Decomposition of Programs

One can hardly verify any complicated, large industrial program automatically as
one piece of code. We suggest decomposing large programs by extracting smaller
program fragments from their source to verify them separately. Such an approach
decreases the demand for computational resources and simultaneously increases the
efforts required for environment modeling (more on this in the next subsection).
    We suggest considering logically interconnected program components like, say,
loadable kernel modules or plugins (Table 2) as program fragments. The decompo-
sition is performed only on the file level. Each program fragment can be considered
as a set of C source files. In our experience, this is a ”golden mean” that enables
obtaining useful verification results with moderate efforts for modeling the environ-
ment. Each program fragment should have at least one entry point — a function that
can be called by other program fragments.
    It is hardly possible to propose a universal algorithm for an automatic program
decomposition. Thus, we suggest a configurable and extendable approach illustrated
in Fig. 2. A user should provide configuration properties and the program’s source
code in the form of a Clade build base5. Program decomposition is performed

3 https://forge.ispras.ru/projects/klever, https://github.com/ldv-klever/klever
4 https://klever.readthedocs.io/en/latest
5 One can see Appendix A.1 for more details about Clade and build bases.
6                                             Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

Table 2 Approximate number of components in open-source projects.
                   Project      Number of components (approximately)
                   Linux Kernel               5,000
                   BusyBox                     300
                   GTK                         200
                   Apache                      150
                   VLC                          80



automatically. However, a user can adjust it by tuning configuration properties and
the decomposition specification between runs of Klever.



        Build base

                                       Automatic                        Program
                                     decomposition                     fragments
      Configuration
       properties


                                     Decomposition                      Manual
                                      specification                   refinement




Fig. 2 Iterative method of program decomposition.


    The Project Fragment Generator (PFG) is a Klever component that performs the
automatic decomposition. It implements the algorithm illustrated in Fig. 3. Config-
uration properties, which are denoted as conf, contain the names of files, directo-
ries and program fragments for verification. It also lists the names of tactics that
implement particular decomposition (decomposition tactic) and composition (com-
position tactic) algorithms. These tactics ought to be implemented as part of a spe-
cific program adaptation, and their implementation should be based on a particular
program architecture. However, the repository contains several simple open-source
implementations of such tactics.
    The build base (build base) contains, among other things, an oriented callgraph
and build command graph, which are used by PFG6. The build base contains other
details to resolve dependencies between files, such as definitions of macros and

6 The callgraph consists of nodes that correspond to functions and edges that match function
calls. An edge of a build command graph corresponds to a file that was produced by some build
command and then provided to another build command as an input. Nodes in this graph reflect
build commands.
Klever: Verification Framework for Critical Industrial C Programs                    7

types. We focus mostly on the callgraph because functions are essential means for
implementing the main logic of the program, and the distribution of functions among
files better reflects how the program is organized.


def PFG(conf, build_base):
    decomposition_tactic, composition_tactic = get_methods(conf)
    decomposition_spec = get_decomposition_spec(conf)
    final_program_fragments = set()

     file_graph = prepare_file_graph(build_base)
     fragments_graph = decomposition_tactic(conf, build_base, file_graph)
     if decomposition_spec:
         fragments_graph = refine_fragments(fragments_graph, decomposition_spec)
     target_files = resolve_files(fragments_graph, conf, build_base)
     target_fragments = resolve_fragments(fragments_graph, target_files)

     for fragment in target_fragments:
         extra_fragments = composition_tactic(fragment, fragments_graph, conf,
                                               build_base, file_graph)
         new_target = Fragment(fragment.files)
         for extra_fragment in extra_fragments:
             new_target.add_files(extra_fragment.files)
             final_program_fragments.add(new_target)

     return final_program_fragments



Fig. 3 Algorithm of decomposition into program fragments.


    First, PFG reads conf and chooses two project-specific tactics (for decomposition
and composition) depending on a program, its version and names provided by a
user. The user should choose the best suitable tactics for decomposition and com-
position, depending on the program’s design and its build process. Decomposition
and composition tactics traverse the build command graph and callgraph selecting
files for program fragments for decomposition or merging already selected program
fragments for composition.
    The decomposition specification (decomposition spec) is a JSON file that speci-
fies files to be added or removed from particular program fragments7. PFG uses it
in the next step.
    Then PFG constructs a file graph using the two mentioned graphs. Nodes of the
file graph correspond to the program’s C source files, and edges match function calls
between them. Then, the decomposition tactic constructs a program fragment graph
(fragments graph) for the particular program under verification. Each node of this
graph corresponds to a set of C source files of the program. An edge between two
program fragments exists if the first one calls at least one function defined in the
second one.
    Decomposition and composition tactics work with the file graph, callgraph and
build command graph. Common operations with them, such as traversing over de-
pendencies or finding specific nodes, are separated into a specific shared library that

7 There are a couple of examples of decomposition specifications in Appendix B.
8                                               Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

simplifies the implementation of new tactics. One can find more information about
the configuration of program decomposition in the user documentation8.
    The refine fragments step is the correction of the generated program fragments
according to the provided decomposition specification. This specification serves only
the purpose of manually adjusting the automatically obtained results of program
decomposition using tactics. To achieve that, the user can modify the generated
decomposition specification by changing the list of functions, files, and directories
(either concrete names or regular expressions) describing program fragments. This
specification can be provided at the follow-up run of Klever, and it supersedes
program fragments generated automatically.
    At the next step, PFG marks nodes of the file graph and program fragment graph
as target ones using the configuration. A user can provide a list of functions, files,
and directories (yet again as either concrete names or regular expressions) to specify
targets for verification. If a file is marked as a target one, then all program fragments
that contain the file are also marked as targets.
    The last step is the composition of program fragments. The idea is to find a
few other program fragments for each target program fragment and combine them
together as new program fragments. It might reduce efforts required for environment
modeling. For example, a composition tactic can search for program fragments that
implement missing function definitions for some target program fragment.




       comp1.c                comp2.c                 comp1.c                comp2.c + helper.c
                     3
        3                             4
                                                         3               3
        lib1.c                helper.c
                                                       lib1.c + lib2.c
                     2
        10
                                                             2
        lib2.c               core.c                          core.c




Fig. 4 Decomposition and composition example.


    An example of decomposition and composition is shown in Fig. 4. There is a file
graph in the left part of the picture. For illustrating purposes, we added information
about function calls (numbers), build command dependencies (shapes with the same
color are input files of a single linking command) and lines of code per file (sizes of
ellipse shapes). There is a program fragment graph on the right side of the picture.
There are two target components (comp1.c and comp2.c) that actively use a couple

8 https://klever.readthedocs.io/en/latest/dev decomposition conf.html
Klever: Verification Framework for Critical Industrial C Programs                       9

of libraries (lib1.c and lib2.c). The second component is implemented with a helper;
the first library refers core.c. Decomposition and composition tactics can use this
information to simplify algorithms and make them more precise. Imagine a user
expects to get two program fragments for corresponding components with included
dependencies for verification as a result of the decomposition. PFG makes two
program fragments, illustrated in the left picture, and then the composition tactic
adds a program fragment with libraries to each component. A dashed line on the
right illustrates the result of such a composition.
    It is worth mentioning that the process of decomposition is not very stable regard-
ing changes in the code base if it relies on manual file or function listings. However,
if there is a way to automatically select program components and implement the
routine as a decomposition tactic, then this approach becomes much more stable.
The Linux kernel is a good example. It is hardly possible to manually list files that
correspond to loadable kernel modules that might change significantly from version
to version. But an algorithm that detects files from the build commands tree allows
seamlessly obtaining the list of files for each independent module, until the whole
algorithm for arranging build commands is unchanged.



2.2 Environment Modeling

Libraries, user inputs, other programs, etc. constitute an environment that influences
program execution. Program verification requires providing a model that represents
certain assumptions about the environment:
• It should contain a function that we refer to as an entry point, and all paths
  analyzed by a verification tool should start with this function. This entry point
  should invoke the target program’s API in the same way as the real environment.
• It should contain models of functions that the program calls during execution and
  which can influence verification results, but not necessarily all of them. These
  functions can be defined in other program fragments or libraries. Moreover, some
  functions that require modeling could be just too complicated for verification
  tools and need to be replaced by simplified models.
• It should correctly initialize external global variables.
   Our experience shows that bug finding is possible even without accurate envi-
ronment models if providing verification guarantees is out of scope. However, it is
crucial to provide precise environment models considering the specifics of checked
requirements and programs under verification to achieve high-quality verification
results [39]. It becomes even more important to do that to avoid missing faults and
false alarms after program decomposition.
   The Klever framework allows the development of the environment model either
directly in the C programming language or using the proposed DSL approach. A user
might choose an approach that suits the project best. We focus mostly on the DSL
approach in this section, but before diving deeper into details, let us highlight the main
10                                                 Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

advantages of the proposed solution. The configurable DSL enables detaching the
environment model from the code and maintaining a certain level of abstraction from
program interfaces implemented by a particular program fragment. The approach
pays off if there are many program fragments with a similar design, like operating
system device drivers. Otherwise, the development cost using the DSL might be
close to the cost of developing the model in C manually, especially if each program
fragment has an entirely unique interface and logic.
    We show different kinds of interactions between components called interaction
scenarios in Fig. 5. Each interaction scenario is related to some specific API and
associated with arrows of a particular style. For instance, the device driver provides
initialization and exit functions (long-dashed line), device-specific callbacks (dotted
line), interrupt handlers (chained line) and, in turn, it calls library functions from the
bus driver (thin line) and the kernel (short dashed line). We refer to corresponding
function calls and read or write accesses to global variables as interaction events.
Thus, each interaction scenario can be considered as a set of feasible sequences of
interaction events that can happen during real program execution. We assume that
all interaction events in an interaction scenario should happen in the context of the
same thread or process, but each event happening in the environment is followed by
the execution of some code from the program fragment.


                                                             Library functions
                                 Device-specific handlers
                                        Interrupt handlers

                  Device driver
                                              Init/exit functions


                          Bus driver API                                   Operating
                                                                         system kernel


                                              Init/Exit functions
                    Bus driver

                                        Interrupt handlers
                                 Device-specific handlers
                                                             Library functions


Fig. 5 Interaction scenarios between drivers and their environment.


   The environment model might include different models of interaction scenarios,
depending on the decomposition of a program into fragments. It is possible to verify
either a device driver separately from other components, both device and bus drivers
together, or even add to them extra files from the operating system kernel.
Klever: Verification Framework for Critical Industrial C Programs                        11

   The next subsection describes the semantics of the used representation of envi-
ronment models and an approach to their generation.


2.2.1 Intermediate Model

We propose a notation for the so-called intermediate model to specify environment
models of interaction scenarios, or just scenario models for brevity. In simple words,
the intermediate model describes events that can happen in the environment of
a program fragment in a structured way. The language definition is out of the
paper’s scope, it is given in the Klever documentation. In this section, we present the
semantics of the notation.
    An intermediate model aims at modeling scenarios before their translating to
a C source code of the environment model. Models in the notation can be either
generated or developed by a user.
    Let the interface of a program fragment be 𝐼 =< 𝑉 𝑝 , 𝐹 𝑝 , 𝑅 𝑝 , 𝑇 𝑝 >. 𝑉 𝑝 is a set of
global variables, 𝐹 𝑝 is a set of function declarations, 𝑅 𝑝 is a set of macros, and 𝑇 𝑝
is a set of type definitions provided in the C programming language. The ”p” suffix
means that these objects are declared or defined in the program fragment.
    An intermediate model for the program fragment with interface 𝐼 consists of the
following elements:
                            𝑀𝐼 =< 𝑉𝑒 , 𝐹𝑒 , 𝑅𝑒 , 𝑇𝑒 , 𝐸 𝐹 , 𝐸𝑇 >
                                      𝐸𝑇 = 𝜀 1 ∥ .. ∥ 𝜀 𝑛
   Where 𝑉𝑒 , 𝐹𝑒 , 𝑅𝑒 , 𝑇𝑒 are supplementary global variables, functions, macros and
type definitions provided in the C programming language as separate C source files
or headers. The ”e” suffix helps to distinguish environment-related objects from
the program fragment’s ones. 𝐸 𝐹 and 𝐸𝑇 represent external functions and threads
spawned by an environment correspondingly.
   The set of function definitions 𝐹𝑒 contains two kinds of functions (auxiliary and
project-specific ones). Auxiliary functions are reused between projects, and many
of them depend on a used verification tool. Models of POSIX or C standard library
functions belong to project-specific functions.
   𝐸 𝐹 and 𝐸𝑇 denote definitions of models of external functions and specific sep-
arate threads for events happening in the environment correspondingly. Models of
external functions specify undefined functions from 𝐹 𝑝 \ 𝐹𝑒 (functions that don’t
have definitions or models in either the program fragment or environment model
supplementary files). Both the environment thread and external function models
specify scenario models. The former describes events executed in a separate thread
spawned by an environment. The latter specifies sequences of interaction events
executed in an already existing thread. The notation limits an application scope to
parallel programs with shared memory. The semantics of environment thread models
12                                           Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

assume that interaction events would happen in threads started simultaneously in the
environment model9.
   A scenario model 𝜀 can be considered as a transition system:

                                  𝜀 =< V, A, R, 𝛼0 >

   Where V is a set of labels, A is a set of actions, R is a transition relation of
the scenario model. Labels are local variables of scenario models in simple words.
States of the transition system correspond to different assignments of values to labels
from V and variables 𝑉 𝑝 ∪𝑉𝑒 (global variables defined in the program fragment and
environment model respectively). Actions describe state transitions and interaction
events. Each label has a type defined in the program fragment or the standard C
library. Each scenario model has the first action denoted as 𝛼0 . There are three kinds
of actions: sending/receiving a signal, base block and jump.
   Base blocks contain the C code, such as entry point calls or accesses to the heap
memory and global variables. Each base block action is a couple:

                                       𝛼 =< 𝜑, 𝛽 >

where 𝜑 is a precondition defined as a C logical expression over variables and
labels from V ∪ 𝑉 𝑝 ∪ 𝑉𝑒 . 𝛽 contains C statements over variables and labels from
V ∪ 𝑉 𝑝 ∪ 𝑉𝑒 and functions from (𝐹 𝑝 ∪ 𝐹𝑒 ) \ 𝐸 𝐹 . The base block code should
follow the C programming language syntax. Each block should have a single control
entry and exit points without any goto statements or incomplete switches, loops or
conditional operators. It is also forbidden to introduce new variables in base blocks.
    Signal exchanges allow for describing data and ordering dependencies between
actions in different scenario models. Signals behave according to the Rendezvous
synchronization model proposed by Tony Hoare [22].
    Let us consider a scenario model 𝜀 𝑖 =< V𝑖 , A𝑖 , R 𝑖 , 𝛼0𝑖 > that sends a signal to
𝜀 𝑗 =< V𝑗 , A 𝑗 , R 𝑗 , 𝛼0 𝑗 >. Sending and receiving actions are 𝛼𝑖 ∈ A𝑖 and 𝛼 𝑗 ∈ A 𝑗 :

               𝛼𝑖 =< 𝜑𝑖 , 𝜋𝑖 , 𝑙𝑖 >                𝛼 𝑗 =< 𝜑 𝑗 , 𝜋 𝑗 , 𝑙 𝑗 , 𝜓 𝑗 >

Constants 𝑙𝑖 and 𝑙 𝑗 are signal names. Signal exchange happens if and only if 𝑙 𝑖 = 𝑙 𝑗 .
C logical expressions 𝜑𝑖 , 𝜑 𝑗 and 𝜓 𝑗 over V𝑗 ∪ 𝑉 𝑝 ∪ 𝑉𝑒 define the precondition and
postcondition. Sending action 𝛼𝑖 does not have a postcondition because its local
variables stay unchanged. Two vectors of labels 𝜋𝑖 : 𝑣 1 , ..., 𝑣 𝑘 where 𝑣 𝑡 ∈ V𝑖 for
𝑡 ∈ 1..𝑘 and 𝜋 𝑗 : 𝑢 1 , ..., 𝑢 𝑘 where 𝑢 𝑡 ∈ V𝑗 for 𝑡 ∈ 1..𝑘 describe data transfer:
∀𝑡 = 0..𝑘 : 𝑢 𝑡 := 𝑣 𝑡 . Types of corresponding labels at the same positions in vectors
should match each other.
   Jumps are actions that help to implement loops and recursion. An entrance to a
jump replaces the transfer relation with new transfer relation rules.



9 However, the word ”run” here is used for convenience because the environment model and the
program fragment are never intended for real execution but only for verification.
Klever: Verification Framework for Critical Industrial C Programs                     13

   The order of actions (R and 𝛼0 ) in the example is specified in the process entry
using a simple language. There is a notation for the following kinds of actions:
• < 𝑛𝑎𝑚𝑒 > is a base block action;
• (𝑛𝑎𝑚𝑒) is a signal receiving action. Where (!𝑛𝑎𝑚𝑒) means that the scenario
  model waits for a signal to start.
• [𝑛𝑎𝑚𝑒] is a signal sending action.
• 𝑗𝑢𝑚 𝑝 is a jump that just specifies a new sequence of actions to do. Each jump
  action has its process entry.
   An order of actions is described using two operators:
• . is a sequential combination operator.
• | is a non-deterministic choice operator.
   One can use parentheses in expressions; a sequential combination operator has a
higher priority.
   There is an example of a transfer relation of a scenario model illustrated in Fig. 6.
The order can be defined by the following expressions: (!𝑎). < 𝑏 > .(< 𝑐 > |𝑑).[𝑒]
and a jump action 𝑑 =< 𝑓 > .𝑑| [𝑒].



                                             (!a)



                                             <b>


                              <c>                          <f>


                                             [e]

Fig. 6 Example of an interaction scenario transfer relation.


   The notation of intermediate models is sufficient for specifying realistic envi-
ronment models, as it allows combining an event-oriented description of scenarios
with fragments in C. It gives more freedom to describe the event-driven environment
model, dependencies between events, and a non-deterministic behavior. Descriptions
of actions are separated from definitions of signals and transfer relations of scenario
models. Such organization simplifies the comprehension of the whole model struc-
ture. It is easy to illustrate it as a graph. The model-generating process allows weaving
the environment model into files of program fragments without touching the source
code. It simplifies the work of dealing with different versions and configurations of
a program.
14                                             Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

   The drawbacks of the approach are the large size of JSON files and the redundancy
of many features if an environment model is simple and requires mostly function
models. In this case, it is easier to provide the model directly in C. This case is also
supported in Klever.
   A simplified example of an intermediate model and its description can be found
in Appendix C.


2.2.2 Generating Environment Models

Environment Model Generator (EMG) performs the synthesis of environment models
for program fragments according to the workflow illustrated in Fig. 7. As an input,
EMG receives a program fragment, build base, and optional environment model
specifications developed manually. As its output, EMG synthesizes an environment
model in the aspect-oriented extension of the C programming language. CIF weaves
the program fragment source code to add the environment model, but this step
follows EMG’s work10.
   The EMG’s synthesis process consists of two steps:
1. First, scenario generators independently synthesize scenario models. Their com-
   bination forms an intermediate model.
2. Then, the translator generates the C code of the environment model from the
   provided intermediate model.
   Each scenario generator provides scenario models that can communicate over
signals. Scenario generators are parts of program-specific adaptations and can im-
plement various implementations. The open-source implementation contains gener-
ators for the Linux device drivers, while the implementation just combines manual
environment model specifications. Notations of environment model specifications
for various scenario generators may differ. It is convenient to use a pipeline of
several scenario generators for different kinds of scenario models in practice. For
large event-oriented programs, the development of scenario generators may take a
considerable time.
   In some cases, it is convenient to manually adjust or develop an intermediate
model or its part. We propose to use a specific scenario generator to enable that.
   The translator generates the main single C source file with the entry point and
several files in the aspect-oriented extension of the C programming language called
aspect files. The first EMG translation step is the extraction of the C code denoted
as 𝑉𝑒 , 𝐹𝑒 , 𝑅𝑒 , 𝑇𝑒 from the provided intermediate model. This part of the model does
not need any translation and can be added to the corresponding files.
   Then the translator should generate a function for each scenario model. We refer
to such functions as control functions. We give an example of a control function in
Appendix C. To generate a control function, the translator creates a control function
with local variables per each label from V, adds C control operators to implement
10 The next subsection and Appendix A.2 contain more details about the aspect-oriented extension
of the C programming language and CIF.
Klever: Verification Framework for Critical Industrial C Programs                    15


                                       Program fragment

                       Environment model
                                                          Build base
                         specifications


                                Environment Model Generator

                                       Scenario generators



                                       Intermediate model



                                           Translator


                                       Environment model
                                            (C code)

Fig. 7 Environment Model Generator workflow.



the order of interaction events defined by the intermediate model, and adds an
implementation per event, which is explained below. Subsequently, the translator
determines how to replace references to labels in actions with the newly generated
control function local variables.
   There is a sound approach for translating signal exchanges to C code without
losing scenarios. Unfortunately, preliminary experiments indicated that the existing
verification tools could not cope with complicated parallel models when checking
memory safety or reachability properties. Thus, we have implemented a simplified
translator that implies additional restrictions on models and misses some possible
scenarios. It allows only scenario models that can receive signals as the first and
the last actions. The resulting code is sequential, and it calls corresponding control
functions in place of signal dispatches to scenario models. Such optimization makes
the resulting model straightforward but does not capture the interleaving of actions
from different scenario models that may run simultaneously.
   There is a specific translating algorithm for getting simplified parallel models to
check data races described in [2]. The obtained model is parallel, but it still does not
allow signal exchange between the first and the last actions.
   The translator generates a control flow graph that determines the order of actions
using if and switch operators instead of ”—” and ”.”, and goto jumps instead of
auxiliary jump actions to proceed with the generating control functions. After the
control flow graph is ready, the translator supplies it with the code of base block
actions and newly generated code for receiving and sending actions in particular
places.
16                                               Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

    CIF also adds calls to control functions from aspect files to original source files
of the program to trigger the execution of control functions at points where functions
that correspond to function scenario models are called.
    Some extra details about environment modeling in the Klever framework can be
found in [25, 33, 39] and in the user documentation11.


2.2.3 Modeling Complicated and Undefined Functions

As we already mentioned, it may be necessary to model complicated and undefined
functions that influence the verification results. There is an example of a model of
the Linux kernel memory allocation function kmalloc() in Fig. 8. Fig. 9 shows how
this model is bound with the original function from the Linux kernel.
   The model reduces the ldv kmalloc() function to malloc() which is known by any
verification tool that participates in SV-COMP. The model takes into account that
malloc() does not return NULL according to the SV-COMP rules and that in the
Linux kernel there are reserved error codes that cannot be valid pointer addresses
(they are filtered out by ldv is err()).


/* Definitions of types like gfp_t. */
#include <linux/types.h>
/* Definition of ldv_assume() that shrinks paths with a false value of its argument. */
#include <ldv/verifier/common.h>
/* Definition of ldv_undef_int() that returns any integer type value. */
#include <ldv/verifier/nondet.h>

void *ldv_kmalloc(size_t size, gfp_t flags) {
    void *res;

     /* This allows to check for flags within requirement specifications. */
     ldv_check_alloc_flags(flags);

     /* Returns either NULL or a pointer to a valid kernel memory nondeterministically. */
     if (ldv_undef_int()) {
         /* Always successful according to SV-COMP rules. */
         res = malloc(size);
         ldv_assume(!ldv_is_err(res));
         return res;
     } else
         return NULL;
}

long ldv_is_err(const void *ptr) {
    return ((unsigned long)ptr > (unsigned long)-MAX_ERRNO);
}



Fig. 8 Model of a memory allocating function.


   Using ldv undef int() causes verification tools to traverse both paths when analyz-
ing the target program with the given model. The first path corresponds to successful

11 https://klever.readthedocs.io/en/latest/dev env model specs.html
Klever: Verification Framework for Critical Industrial C Programs                   17

 around: execution(static inline void *kmalloc(size_t size, gfp_t flags))
 {
     return ldv_kmalloc(size, flags);
 }



Fig. 9 Aspect file replacing the kmalloc() function definition with its model.



memory allocation, while the second one is a failure. This allows us to reveal possible
faults in error handling paths that are unlikely to happen during normal operation
and testing.
    ldv kmalloc() invokes ldv check alloc flags() that may be defined by requirement
specifications to check for memory allocation function flags. For instance, one can
ensure that the flag GFP ATOMIC is passed when allocating memory in the interrupt
context and when holding spinlocks within the Linux kernel.
    Fig. 10 gives an example of support for different versions of the Linux kernel.
In this example, the same model ldv is err() is used since only the return type of
IS ERR() changed, but its return values remained the same. In the case of changes
in the semantics of the API, one may need to introduce different models.


 around: execution(static inline long IS_ERR(const void *ptr))
 {
         return ldv_is_err(ptr);
 }

 /* Starting from Linux 3.15 IS_ERR() returns Boolean values. */
 around: execution(static inline bool IS_ERR(const void *ptr))
 {
         long ret;
         ret = ldv_is_err(ptr);
         return (bool)ret;
 }



Fig. 10 Aspect file taking into account changes in the Linux kernel API.


   One can find additional information on this topic in the user documentation12.



2.3 Specifications of Requirements

For checking requirements that do not correspond explicitly to any of the properties
supported by verification tools [5], we suggest to weave an additional source code
into a program. This extra source code should express the requirements using one of
the supported properties. For instance, rules of correct usage of a particular API can
be formulated as the unreachability of the error function, like in Fig. 11 and Fig. 12.

12 https://klever.readthedocs.io/en/latest/dev common api models.html
18                                           Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

For some requirements, it may be hard or even impossible to express them using
additional C expressions and statements. In this case, one has to leverage specific
means of verification tools, e.g., this may be the case for finding data races [2].


/* A device driver can register just one device at a time. */
int register_device(void) {
    ...;
}
/* A device driver can unregister a device just after it registers it. */
void unregister_device(void) {
    ...;
}



Fig. 11 Original program source code.




bool is_device_registered = false;

int register_device(void) {
    if (is_device_registered)
         __VERIFIER_error();
    is_device_registered = true;
    ...;
}
void unregister_device(void) {
    if (!is_device_registered)
         __VERIFIER_error();
    is_device_registered = false;
    ...;
}



Fig. 12 Modified program source code.


   If one expresses weakly related requirements using the same property, it is possible
to check them simultaneously, but we do not recommend this due to the following
issues. The first reason is that it is not an easy task for verification tools to distribute
available computational resources fairly between various requirements. The second
reason is that most verification tools stop after they find a first violation of a checked
property. Therefore, detecting a first fault or a false alarm can prevent finding other
faults.
   Below, we provide an example of a requirements specification. Appendix D
contains its high-level description. If the reader is not interested in this, he/she can
proceed to the next subsection.
   Fig. 13 and Fig. 14 contain an example of a requirements specification that reduces
checking of correct usage of the module reference counter API in the Linux kernel
to a reachability problem. The requirements specification introduces a model state
represented by the global variable ldv module refcounter initialized by 0. The model
state is changed within model functions ldv module get(), ldv try module get(), and
Klever: Verification Framework for Critical Industrial C Programs                       19

ldv module put() according to the semantics of the corresponding API. These model
functions are bound with the original ones by the aspect file shown in Fig. 14.


/* Definition of ldv_assert() that calls __VERIFIER_error() or dereferences NULL. */
#include <ldv/verifier/common.h>
#include <ldv/verifier/nondet.h>

/* NOTE Initialize module reference counter at the beginning */
static int ldv_module_refcounter = 0;

void ldv_module_get(struct module *module)
{
    if (module)
        /* NOTE Increment module reference counter */
        ldv_module_refcounter++;
}

int ldv_try_module_get(struct module *module)
{
    if (module && ldv_undef_int()) {
        /* NOTE Increment module reference counter */
        ldv_module_refcounter++;
        /* NOTE Successfully increment module reference counter */
        return 1;
    }

     /* NOTE Could not increment module reference counter */
     return 0;
}

void ldv_module_put(struct module *module)
{
    if (module) {
        if (ldv_module_refcounter == 1)
            /* ASSERT Decremented module reference counter should be greater than its
                      initial state */
            ldv_assert();
        /* NOTE Decrement module reference counter */
        ldv_module_refcounter--;
    }
}

void ldv_check_final_state(void)
{
    if (ldv_module_refcounter != 0)
        /* ASSERT Module reference counter should be decremented to its initial value
                  before finishing operation */
        ldv_assert();
}



Fig. 13 Example of expressing requirements as a reachability problem.


    The considered requirements specification makes 2 checks by ldv assert(). The
first one is within ldv module put(). It is intended to find out when Linux kernel
loadable modules decrement the module reference counter without first incrementing
it. The second check is within ldv check final state(). It tracks that modules should
decrement the module reference counter to its initial value before finishing their
operation.
20                                              Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

 around: call(void __module_get(struct module *module) {
         ldv_module_get(module);
 }

 around: call(bool try_module_get(struct module *module)) {
         return ldv_try_module_get(module);
 }

 around: call(void module_put(struct module *module)) {
         ldv_module_put(module);
 }



Fig. 14 Aspect file replacing kernel function calls with model ones.



   To emphasize statements that are most relevant to checked requirements, we
suggest using special comments. Such comments in the example begin with the key-
words NOTE and ASSERT. These comments are used during preliminary processing
and visualization of violation witnesses considered in the following subsections.
   One can find more details about the development of requirement specifications in
the corresponding section of the user documentation13.



2.4 Verification Task Generation

Klever generates a verification task for each pair of a program fragment and a
requirements specification. Below, we consider particular steps of this process.


2.4.1 Weaving and Merging of Source Files and Models

First, CIF14 weaves the source code of the program fragment with aspect files from the
requirements specification and the environment model. At this step, preprocessing is
also performed. Thereafter, there are several instrumented and preprocessed original
C source files as well as additional preprocessed model C source files. CIL combines
all the source files. After all, there is a single preprocessed C file cil.i prepared for
an immediate run of a verification tool.


2.4.2 Configuration of Automatic Software Verification Tools

It may be helpful to experiment with different configurations of verification tools in
practice. There is also a need to specify different sets of verification tool options for



13 https://klever.readthedocs.io/en/latest/dev req specs.html
14 One can find more details about CIF and CIL in Appendix A.2 and Appendix A.3 respectively.
Klever: Verification Framework for Critical Industrial C Programs                         21

various requirement specifications. Such sets may even differ for various versions of
the same tool.
   To simplify the configuration process for end-users, we propose to prepare several
so-called verifier profiles in advance. Each requirements specification refers to one
of verifier profiles by default. In addition, a user can choose any other available
variant without investing time into learning particular verification tool options and
capabilities. There is a verifier profiles example in Appendix E.
   At the moment, Klever supports CPAchecker [6] as a verification tool backend
and there is a bunch of verifier profiles for it. To integrate new verification tools
within Klever, users need to do at least the following:
• Describe specific verification tool options suitable for checking requirement spec-
  ifications as extra verifier profiles.
• Provide verification tool binaries to a Klever deployment script.
   One can learn more about configuration of verification tools in the corresponding
section of the user documentation15.


2.4.3 Final Preparation of Verification Tasks

At the final step, Klever combines everything obtained thus far into verification tasks.
Each verification task consists of the following set of files:
1. cil.i (its generation was described above).
2. A property file, like in Fig. 15. Its content is provided by a verifier profile re-
   ferred to by a checked requirements specification. One can see a complete list of
   properties supported by various verification tools in [5].
3. A task definition file16. Klever uses it only to bind two previous files, like in
   Fig. 16.
4. A benchmark definition file17. It connects all previous files as well as specifies
   various verification tool options provided by a user in various configuration files.
   An example of this file is shown in Fig. 17.


 CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )



Fig. 15 Property file example.




15 https://klever.readthedocs.io/en/latest/dev verifier profiles.html
16 https://github.com/sosy-lab/benchexec/blob/main/doc/task-definition-example.yml
17 https://github.com/sosy-lab/benchexec/blob/main/doc/benchexec.md#input-for-benchexec
22                                                Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

 format_version: '1.0'

 input_files: 'cil.i'

 properties:
   - property_file: safe-prps.prp



Fig. 16 Task definition example.

 <?xml version="1.0" ?>
 <benchmark hardtimelimit="300" timelimit="270" tool="cpachecker">
     <rundefinition>
         <option name="-setprop">counterexample.export.exportExtendedWitness=true</option>
         <option name="-ldv-bam"/>
         ...
     </rundefinition>
     <tasks>
         <include>cil.yml</include>
     </tasks>
     <propertyfile>safe-prps.prp</propertyfile>
 </benchmark>



Fig. 17 Benchmark definition example.



2.5 Scheduling and Monitoring

Klever Scheduler operates with two types of objects: verification tasks and verifica-
tion jobs. A verification job is a set of files including a build base18, specifications,
and configuration files that are necessary to start automatic verification. Verification
jobs are solved by a specific Klever component named Klever Core. During the so-
lution of verification jobs, it generates verification tasks according to the approaches
described above. Each Klever Core instance can generate verification tasks in parallel
to speed up the entire verification process.
    Monitoring of available computational resources and their fair distribution be-
tween verification jobs and verification tasks are responsibilities of Klever Sched-
uler. Klever Scheduler respects verification task priorities specified by users. Also,
Klever Scheduler supports canceling verification jobs. Some verification tasks can
require considerably lesser computational resources than specified by the user. To
avoid useless memory reservations, we perform speculative scheduling, trying to run
a verification tool with lesser limitations first.
    We use BenchExec19 to isolate runs of Klever Core and verification tools as
well as to measure and limit computational resources consumed by them at a single
machine. It also lets you get verification results from different verification tools in a
unified format.


18 As a rule, build bases are not explicitly included in verification jobs. They are located and found
in the Klever deployment directory.
19 See Appendix A.4 for more information.
Klever: Verification Framework for Critical Industrial C Programs                       23

   Klever Scheduler currently supports parallel solution of verification jobs and
tasks on a single machine. Also, it can solve verification tasks in parallel using
VerifierCloud20.



2.6 Preliminary Processing of Verification Results

One of the most important functions of the framework is the presentation of verifi-
cation results to users. The Klever component named Verification Result Processor
(VRP) performs preliminary processing of verification results for each solved veri-
fication task.
    Violation witnesses generated by verification tools are machine-readable, and a
user can hardly use them in their raw format. Moreover, verification tools can miss
some details and even parts of corresponding error paths. We supported an extended
witness format for CPAchecker to have all the necessary pieces of information21. In
addition, it allows to add some important internal information from verification tools
to the violation witness. For instance, places where leaked memory is allocated can
be specially noted during memory-safety checking. Other verification tools do not
provide violation witnesses using our format; thus, their visualization may not be as
good as the CPAchecker ones.
    VRP translates violation witnesses into a Klever internal format that is more
convenient for visualization and assessment purposes22. Using information from
violation witnesses, it finds corresponding expressions and statements within cil.i
to be presented to users and adds references to corresponding lines of source files.
Also, at this stage, VRP parses special comments from environment models and
requirement specifications. This helps to distinguish important pieces of information
like invocations of program fragment entry points and changes to model states. In
contrast, VRP marks all parts of violation witnesses that seem irrelevant for found
violations of checked requirements so that they can be hidden during subsequent
visualization.
    The CPAchecker verification tool can provide code coverage reports in addition
to witnesses [12]. These reports are in the GCC test coverage format (GCOV). For
its visualization, one can use standard tools like LCOV23. Code coverage reports are
an important artifact to establish verification in practice. They reflect parts of the
program such as lines of code, branches, and functions that are actually verified. This
information is essential for estimating the quality of an environment model, since
neither violation nor correctness witnesses provide data on actual program paths.
Code coverage reports help to understand which program entry points should be
invoked additionally by environment models.

20 https://vcloud.sosy-lab.org
21 https://klever.readthedocs.io/en/latest/dev.html#extended-violation-witness-format
22 https://klever.readthedocs.io/en/latest/dev.html#error-trace-format
23 http://ltp.sourceforge.net/coverage/lcov.php
24                                              Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

    VRP converts code coverage reports to an internal format to facilitate their vi-
sualization24. Like for violation witnesses, it adds references to the original source
files. Also, it merges reports issued for individual verification tasks to get a single
code coverage report for the program for each requirements specification. At this
step, VRP calculates statistics for each subdirectory of the program source tree, con-
sidering either source files considered by a verification tool or all source files from a
build base. These sets of source files can differ since the verification tool may miss
analysis for certain source files, e.g., due to some internal failures or if some source
files are not included by a considered program configuration.



2.7 User Interface

The Klever software verification framework implements a user interface as a
web-server named Klever Bridge. Below, we consider two major use cases of
Klever Bridge.


2.7.1 Managing Verification Processes

To obtain verification results, users should prepare all the necessary data and then
start verification. At this stage, Klever Bridge provides the following facilities:
• Each new verification activity starts with the creation of a new verification job
  (Fig. 18). Verification jobs consist of specifications and configuration files that are
  necessary to start the verification process and have attributes such as a name, date
  of creation, author, access rights, etc. Verification jobs can be created based on
  templates for corresponding project-specific adaptations or existing verification
  jobs. To proceed to verification, users should choose program fragments and re-
  quirements to be checked. Besides, to get better verification results for particular
  programs and requirements, we suggest incrementally tuning various configura-
  tion options and improving specifications. Klever Bridge provides a featured text
  editor to complete these tasks.
• Klever Scheduler starts the execution of Klever Core as soon as the user wants to
  solve his/her newly created verification job and there are available computational
  resources. Klever Core reports verification results when they become available. It
  is worth noting that since verification can take a considerable time, Klever Bridge
  presents verification results to experts as soon as they appear. In this case, they
  can proceed to their analysis faster; in particular, it is possible to understand that
  something was done wrong without waiting for all verification results.
• Klever Bridge provides information on running and already solved verification
  jobs. For running verification processes, it presents their progress: the number of


24 https://klever.readthedocs.io/en/latest/dev.html#code-coverage-format
Klever: Verification Framework for Critical Industrial C Programs                   25

   already solved and the total number of verification tasks, elapsed time, and approx-
   imate remaining time. The latter is evaluated by Klever Core and Klever Scheduler
   based on accumulated statistics.




Fig. 18 Creation of a new verification job.




2.7.2 Expert Assessment of Verification Results

To simplify the analysis of verification results by experts, we implemented the
following facilities in Klever Bridge:
• Visualization of violation witnesses, code coverage and internal failures (Fig. 19).
  The primary goal of this visualization is to hide from experts as many irrelevant,
  according to domain knowledge, details as possible. Besides, all verification
  results are closely related to the original source files.
• Evaluation of verification results by creating expert marks (Fig. 20). Expert marks
  can be associated with verification results, either manually or automatically. The
  automatic assessment saves a great deal of time by avoiding the analysis of similar
  verification results when different versions or configurations of the same program
  are verified. Often, in these cases, violation witnesses and internal failure reasons
  do not differ considerably, and Klever Bridge matches them by pretty simple rules.
  Experts can provide each mark with a detailed description and tags. To further
  simplify the analysis, Klever Bridge keeps all the history of mark changes.
• Showing various statistics over verification results that can help to understand a
  general picture. For instance, it can be very useful to see how many warnings
  were yielded for a particular verification job, what warnings correspond to faults
  and false alarms, what are the most significant reasons of false alarms, and so on.
• Users can compare both verification jobs as sets of files and their verification
  results. This is useful both for tracking changes for various versions and configu-
  rations of target programs and for estimating changes during the development of
  project-specific adaptations.
26                                                 Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

It might be useful to integrate expert marks with issue tracking systems. However, it
might be worth noting that a mark does not always correspond to a real bug. Marks
might help to distinguish false alarms or issues in the environment models.
   One can find more examples and detailed explanations of some actions with the
Klever user interface in the tutorial25.




Fig. 19 Visualized violation witness and code coverage.




Fig. 20 Creation of a new expert mark.




25 https://klever.readthedocs.io/en/latest/tutorial.html
Klever: Verification Framework for Critical Industrial C Programs                      27

3 Project-Specific Adaptations

This section describes publicly available project-specific adaptations delivered to-
gether with the Klever software verification framework. The application domain of
Klever is, however, not limited to the programs described in this section.
    There are two usable adaptations — for the Linux kernel and BusyBox. The
adaptation for the Linux kernel demonstrates capabilities of verification of complex
event-driven software. The Busybox adaptation is a proof of concept of how Klever
is applicable to user-space programs.



3.1 Adaptation for the Linux Kernel

The Linux kernel architecture is monolithic — it is loaded into RAM during operating
system startup, and then it operates completely in the same shared address space. The
Linux kernel implements main operating system functionalities such as scheduling,
memory management, interprocess communication, interrupt handling, a network
stack, and so on. Besides, it supports modules that can extend its functionality
further. As a rule, device drivers, file systems, network protocols, and audio codecs
are developed as modules. Modules can be either statically compiled into the kernel or
dynamically loaded, but in both cases, they become parts of the monolithic structure.
   We consider the whole Linux kernel, except loadable modules, as a set of sub-
systems. Each subsystem usually consists of all the C source files inside a specific
subdirectory of the kernel source tree. Typical personal computers can load several
hundred modules, but that is a small fraction of all available modules. There are more
than 8,000 modules in Linux 5.12-rc3 compiled for the allmodconfig configuration.
The average module size is about 1.7 KLOC with a median of 500 lines. The average
subsystem size is 7 KLOC with a median of 2 KLOC.
   The adaptation for the Linux kernel includes:
• Tactics for decomposition and composition. They extract modules and subsystems
  from the Linux source code and combine them together.
• A pipeline of several scenario generators to obtain environment models.
• A relatively large set of environment model specifications.
• A set of requirement specifications allowing one to check memory safety, correct
  usage of the Linux kernel API, and the absence of data races.
   Below, these items are treated in detail. In the given section, we do not provide
verification results for the Linux kernel, since it is a matter for the following section.


3.1.1 Decomposition and Composition Tactics

There is only one tactic implemented for decomposing the Linux kernel source code.
This tactic uses a build command graph from the Linux kernel build base as an input.
28                                                 Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

It iterates over LD (linker) and AR (archiver) build commands. The tactic divides
them into two types, depending on the extension of the output files. Files with the
extension ”.ko” correspond to loadable kernel modules. Subsystems are associated
with files ”built-in.o” or ”built-in.a” in recent versions of the Linux kernel.
    The decomposition tactic generates a separate program fragment for each selected
build command. It traverses the build command graph to extract CC (compiler) build
commands whose output files become a part of the module or subsystem. Each CC
build command has an input C source file, and such files together form the final
program fragment.
    The composition step is optional, so we do not consider it here in detail. There
are two composition strategies that allow to combine modules or subsystems that
call exported functions from each other using a greedy algorithm.


3.1.2 Environment Modeling

A program fragment can contain a single module or several modules and subsystems.
An interface for the program fragment can include:
• Subsystem initialization functions. These functions are entry points of subsystems,
  and the Linux kernel calls them in a specific order at boot time.
• Module initialization and exit functions. Pairs of such functions are entry points
  for modules. The Linux kernel calls them when loading and unloading modules
  from memory, respectively.
• Callbacks. Each separate group of callbacks implements operations for handling
  events relevant to a particular resource or device. Callbacks are registered and
  deregistered in the Linux kernel by calling special functions.
• Exported functions. Any module or subsystem can implement functions that are
  exported and used by other Linux kernel components.



                         Environment model
                                                              Build base
                           specifications



                                                                    User model
                     Init/exit caller      Callbacks caller
                                                                     composer




                                           Intermediate
                                        environment model


Fig. 21 Pipeline of scenario generators.
Klever: Verification Framework for Critical Industrial C Programs                                     29

   There is a pipeline of three scenario generators to compose environment models
according to Fig. 21:
1. Init/exit caller. It is a scenarios generator for calling subsystem initialization
   functions and model initialization and exit functions.
2. Callbacks caller. The scenarios generator invokes Linux kernel callbacks.
3. User model composer. The scenarios generator adds handcrafted parts to the
   intermediate model.
    Init/exit caller accepts as input a specification with an order for calling the sub-
system’s initializing functions. Klever contains such a specification that enumerates
a list of relevant macros for this purpose. The scenarios generator checks if these
macros and module init/module exit macros are used in the source code of the pro-
gram fragment. If so, it groups modules’ initialization and exit functions in pairs.
The generator also determines the proper order of calling corresponding functions
if the program fragment contains several modules or subsystems.
    There is an example of an order for calling a subsystem initialization and the
driver’s initialization and exit functions in Fig 22. Both initialization functions can
return an error, and curve arrows reflect these cases. The Linux kernel always
initializes subsystems before loadable kernel modules, so the corresponding function
precedes the module’s initialization function.


                 failed subsystem_init              0
                                                       successful subsystem_init

                           failed driver_init      1
                                                        successful driver_init

                                                   2
                                                        driver_exit




Fig. 22 Order of calling subsystem initialization, driver initialization and driver exit functions.


   Callbacks caller is the most complicated scenario generator. At the first stage, the
generator collects all interface specifications. These specifications list declarations
used at model callbacks’ invocations. Interfaces are grouped into categories corre-
sponding to the specific functionality of the Linux kernel. A category can contain
the following types of interfaces:
• Kernel functions include functions for registering, deregistering, creating, or
  destroying relevant data.
30                                          Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

• Callbacks’ declarations help to detect callbacks’ groups implemented in a program
  fragment.
• Containers are structures storing pointers to callbacks or other important data,
  e.g., pointers to device tables representing supported devices and some of their
  characteristics.
• Resources are objects passed as parameters to multiple callbacks.
    Then, the generator selects categories of those interfaces that are implemented
or used in the source code of the program fragment. The generator gets all the
specifications that describe callbacks’ invocation after that. We refer to them as event
specifications. The specifications’ notation extends the format of an intermediate
model. Main extensions are the following: new labels’ attributes for their binding to
particular interfaces and categories, flags to define labels as resources, callbacks, and
containers. There is a new kind of action named callback. It describes a callback’s
call with labels corresponding to resources.
    Each category needs an event specification to generate an environment model. A
user can explicitly set the connection. Otherwise, a heuristic algorithm is used to
select a suitable event specification for an interface category.
    The final step is the transformation of transition systems from event specifications
to intermediate model notation in accordance with the interfaces implemented or
used in the program fragment. At this step, the generator performs several modi-
fications and simplifications, such as replacing callback actions with code blocks
containing explicit callback calls. If there are several implementations of callbacks
in a certain category, the generator inserts additional scenario models based on the
event specification. Also, it prints callback wrappers if they are implemented as static
functions.
    User model composer accepts serialized and manually modified intermediate
models. They can be obtained at any launch of Klever from its working directory and
then manually corrected. A user can also make the intermediate model from scratch.
The generator does not make any modifications to the provided specifications. It
either adds or replaces parts of the intermediate model already received as input.
    In total, the collection describes callbacks from the following categories: USB,
USB Serial, IIO, PCI, Platfrom, Power Management, Class, I2C, SCSI, HID, TTY,
Parport, file and seq operations, block driver, Super, Net, interrupts, kthreads, timers,
tasklets and workqueues.
    The level of code coverage and the quality of verification results depend on the
number of callbacks invoked by environment models. Fig. 23 shows the dependence
of the share of implementations of device driver callbacks of the most popular
types (categories in our terminology) relative to the number of implementations of
all types of callbacks for Linux 3.14. The plot demonstrates that more than 80 %
of all callbacks belong to the 100 most popular categories. Thus, it would require
significantly more effort to develop environmental model specifications than we have
already spent to get a significantly higher level of code coverage. The code coverage
for particular Linux kernel versions is discussed in Section 4.
    The Klever project’s source tree contains environment model specifications in
the directory presets/jobs/specifications/linux. It includes 36 specifications with 20
Klever: Verification Framework for Critical Industrial C Programs                                                                  31




             The share of corresponding callback implementations
                                                                   100%


                                                                   80%


                                                                   60%


                                                                   40%


                                                                   20%


                                                                    0%
                                                                          0    100   200     300     400     500     600     700
                                                                              The number of most widespread callback types

Fig. 23 Dependence of the share of implementations of callbacks of the most common types on
the number of all callbacks implementations for Linux kernel 3.14.



KLOC of DSL code and 1.5 KLOC of models in C. The collection of specifications
is suitable for the following Linux kernel versions: 2.6.33, 3.14, 4.6.7, 4.15, 4.17
and 5.5. One can use these specifications for other versions as well, but the quality
of verification results can decrease.
   The presets/jobs/specifications directory contains auxiliary functions for different
adaptations in the verifier and common subdirectories. They contain models for
allocating memory, returning undefined values and so on.


3.1.3 Requirement Specifications

Klever includes 34 requirement specifications for checking memory safety and rules
of correct usage of the Linux kernel API as well as for finding data races in Linux
kernel modules and subsystems. In general, these requirement specifications allow
to detect the following faults:
•   Buffer overflows.
•   Null pointer dereferences.
•   Uninitialized memory usages.
•   Double or incorrect memory releases.
•   Data races and deadlocks.
•   Leaks of specific resources of the Linux kernel.
•   Incorrect function calls depending on the execution context.
•   Incorrect initialization of specific Linux kernel resources.
32                                         Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

   Requirement specifications for the Linux kernel are located in the directory pre-
sets/jobs/specifications/linux. The requirement specifications base is placed at pre-
sets/jobs/specifications/linux/Linux.json. In total, requirement specifications’ size is
about 5.4 KLOC. The requirement specifications base consists of approximately
900 lines. Development of a new typical requirements specification can take about
1 week for experts and a month for novices.



3.2 Adaptation for BusyBox

The BusyBox project incorporates several command-line utilities such as cat, tar,
or tail into a single software system. Each utility is called an applet. Each applet
can consist of several C source files. During its operation, it relies only on the libbb
shared library of the project and the C standard library. There is strictly one entry
point function in an applet. Its name is a concatenation of the applet’s name and
the suffix main. The function prototype coincides with the prototype of the main
function.
   The adaptation in Klever matches the BusyBox 1.28.3 version. It includes one
decomposition tactic and a set of requirement and environment model specifications.


3.2.1 Decomposition Tactic

The decomposition tactic for the BusyBox project separates the libbb library and
applets. Its algorithm includes the following steps:
1. Search all C source files from the project source code. Distinguish files from the
   libbb directory as a separate program fragment.
2. Find those files that implement entry point functions according to the mentioned
   above pattern. We refer to them as main files.
3. Collect C source files from other than libbb directory that have dependencies with
   the main file using a callgraph.
4. Prepare a list of program fragments for applets by joining main files with their
   found dependencies.
   The algorithm has an additional configuration parameter to add C source files from
the libbb directory to each program fragment. It is enabled by default. The adaptation
has a decomposition specification for BusyBox. It implies removing eight libbb files
from each program fragment. The excluded files cause problems for Klever and
verification tools.
   Klever successfully generates program fragments for 185 applets of Busybox
configured in defconfig.
Klever: Verification Framework for Critical Industrial C Programs                   33

3.2.2 Environment Modeling

An applet’s environment model calls the main function and provides stubs for certain
undefined functions. Different adaptations share a scenario generator to call functions
in random order and with undefined parameters. It is used in the BusyBox adaptation
to generate calls of applets’ main functions. There is an example of such a harness
for the SSL client applet in Fig. 24.


void main(void) {
    int ldv_arg_0;
    char **ldv_arg_1;
    ldv_arg_1 = external_allocated_data();
    return ssl_client_main(ldv_arg_0, ldv_arg_1);
}



Fig. 24 Example of an environment model for the SSL client applet.


   The set of environment model specifications includes several types of models in
the C programming language:
1. Models of functions from the C standard library and POSIX such as functions for
   working with strings, exit, fork, etc. These models can be reused at verification
   of other user-space programs.
2. Models of functions from the excluded libbb source files.
   The general set of functions is tiny; there are no more than a dozen functions
of each mentioned type. With the current environment models, the line coverage
constitutes 93 % and function coverage is 86 %.


3.2.3 Requirement Specifications

We verified memory safety and consistency of opens and closes of file descriptors
and pipes for BusyBox applets. No faults have been found. The number of false
alarms was less than a dozen.



4 Practical Evaluation

Klever has been used for verification of various operating system kernels and drivers.
As a proof of concept that can be publicly demonstrated, Klever helped to reveal
more than 400 faults acknowledged by the Linux kernel developers26. Many of these
bugs were reported by students of several universities and participants of the Google
Summer of Code program.
26 http://tinyurl.com/487ntw4d
34                                           Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

   We verified a subset of loadable kernel modules of Linux 5.5 released on Jan-
uary 26, 2020 and Linux 5.12-rc3 released on March 14, 2021 to evaluate different
aspects of the user experience with Klever. We built the Linux kernel for the archi-
tecture x86 64 and configuration allmodconfig. Target loadable kernel modules were
considered program fragments. On average, the size of the chosen modules was the
closest to the mean size of all modules of the Linux kernel. These modules were from
the following subdirectories of directory drivers: hid, hwmon, media, mtd, platform,
staging, usb and video. Table 3 presents characteristics of these modules. There are
about 4 % more modules for Linux 5.12-rc3 in comparison with Linux 5.5.


Table 3 Characteristics of target modules.
                     Characteristic          Linux 5.5 Linux 5.12-rc3
                     Number of modules          2,059      2,141
                     Number of C source files 3,383        3,645
                     Total size of modules   2.7 MLOC 2.8 MLOC
                     Average size of modules 1.3 KLOC    1.3 KLOC


   We checked the given modules against 17 requirement specifications intended for
checking the correct usage of the Linux kernel API27. Also, we checked memory
safety for them. Underneath, we especially distinguish memory safety, since the
solution of the corresponding verification tasks considerably differs from the solution
of other verification tasks. Klever uses a CPAchecker configuration on the base of
symbolic memory graphs [15] for memory safety and a CPAchecker configuration
on the base of block-abstraction memoization and a predicate analysis [18] for
requirement specifications intended for checking the correct usage of the Linux
kernel API.
   For experiments, we used Klever 3.1 and the verification tool CPAchecker r36955
from branch klever-fixes. Klever 3.1 was released with some improvements in speci-
fications intended specially for Linux 5.5, while for Linux 5.12-rc3 we did not make
any specific adjustments in both specifications and tools.
   All experiments were conducted on an OpenStack virtual machine with 8 virtual
cores of the Intel Xeon E312xx (Sandy Bridge) CPU, 64 GB of memory and Debian 9
(Stretch) on board. The computational resource limits per verification task were
5 minutes of CPU time and 5 GB of memory.




27 Identifiers of checked requirement specifications are as follows: alloc:{irq, spinlock,
usb lock}, arch:{asm:dma-mapping, mm:ioremap}, drivers:{base:class, clk1, clk2},
drivers:usb:{core:driver, core:urb, core:usb:coherent, core:usb:dev, gadget:udc-core},
fs:sysfs:group, kernel:{module, rcu:update:lock}, net:core:dev.
Klever: Verification Framework for Critical Industrial C Programs                                35

4.1 Verification Results

Klever successfully generated 31,444 verification tasks for Linux 5.5 and 31,886
verification tasks for Linux 5.12-rc3. Table 4 presents the overall statistics of obtained
verification results. One can see from the table that the Unsafes share is approximately
50 times more for memory safety. Besides, the relative number of Unknowns is also
2.5 times higher. For requirement specifications intended for checking the correct
usage of the Linux kernel API the most common verdict was Safe, i.e. the verification
tool could prove correctness under the certain assumptions.


Table 4 Overall statistics of verification results. Unsafes correspond to warnings issued by the
verification tool (they may be either faults or false alarms). Safe means that the verification tool
could prove correctness under the certain assumptions. Unknowns correspond to failures of the
verification tool or Klever components.
                            Verdict     Linux 5.5 Linux 5.12-rc3
                                        Memory safety
                            Unsafe     280 (14 %)      278 (13 %)
                            Safe       910 (44 %)      901 (42 %)
                            Unknown 869 (42 %)         962 (45 %)
                             Correct usage of the Linux kernel API
                            Unsafe     85 (0.24 %)     110 (0.3 %)
                            Safe      29,033 (83 %) 29,319 (81 %)
                            Unknown 5,885 (17 %) 6,968 (19 %)


   The changes in verification results for Linux 5.12-rc3 relatively to Linux 5.5 are
not huge. One can see that there are fewer Safes and more Unknowns. Foremost, this
is associated with some new expressions in the source code that cause failures of
various Klever components and CPAchecker. For instance, CIL started to fail on 19
modules from the directory drivers/staging/greybus/. The number of Unsafes did not
change too much. A detailed analysis shows that the most noticeable changes were
caused by two reasons. The first reason is that modules started to use new APIs that
were not yet modeled. The second reason is that we reported rather many fixes of
faults revealed for Linux 5.5. They were accepted before releasing Linux 5.12-rc3.
Thus, Klever does not find corresponding faults anymore. Anyway, these slight
changes demonstrate that, despite there being quite considerable changes in target
programs (see Table 1 and Table 3), Klever still could produce comparable and
valuable verification results without any changes in the project-specific adaptation
for the Linux kernel.
   Hereinafter, in this subsection, we consider Unsafes and Unknowns in detail.


4.1.1 Unsafes

Table 5 shows the number of faults and the number of false alarms. The number of
faults revealed during checking memory safety is approximately the same as the total
36                                            Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

number of faults that were found for all remaining requirement specifications. Below,
we will separately treat these faults. A false alarm rate when checking memory safety
is higher than for requirement specifications intended for checking the correct usage
of the Linux kernel API. It is explained by the fact that more accurate environment
models are necessary for it. For Linux 5.12-rc3 the false alarm rate increased.
Primarily, this is due to the same reasons as for changes in the number of Unsafes.


Table 5 Distribution of Unsafes.
                           Unsafe type Linux 5.5 Linux 5.12-rc3
                                       Memory safety
                           Fault        34 (12 %)      25 (9 %)
                           False alarm 246 (88 %) 253 (91 %)
                            Correct usage of the Linux kernel API
                           Fault        30 (35 %)     33 (30 %)
                           False alarm 55 (65 %)      77 (70 %)


    Table 6 demonstrates the distribution of false alarms for different reasons. In-
accurate analysis performed by CPAchecker when checking memory safety gives
considerably more false alarms than for other requirement specifications. Besides,
it is more demanding for the accuracy of environment models as was already stated
above. Most such false alarms are due to the absence of definitions and models of
functions that considerably influence verification results, e.g., those functions that
allocate and initialize specific kernel resources.


Table 6 False alarm reasons.
               False alarm reason                     Linux 5.5 Linux 5.12-rc3
                                         Memory safety
               Inaccurate environment models         123 (50 %) 128 (51 %)
               Inaccurate requirement specifications 0 (0 %)        0 (0 %)
               Imprecise verification tool           114 (46 %) 117 (46 %)
               Others                                  9 (4 %)      8 (3 %)
                             Correct usage of the Linux kernel API
               Inaccurate environment models          20 (36 %)    42 (55 %)
               Inaccurate requirement specifications 22 (40 %)     25 (32 %)
               Imprecise verification tool            11 (20 %)    9 (12 %)
               Others                                  2 (4 %)      1 (1 %)


   There is a noticeable difference in the distribution of false alarms for Linux 5.12-rc3
in contrast to Linux 5.5 for requirement specifications intended for checking the cor-
rect usage of the Linux kernel API. It can be explained by the fact that modules
started to use new APIs that should be modeled.
   Users can wonder whether it is possible to get rid of false alarms since they
hinder the assessment of verification results. Hopefully, there are some large groups
of false alarms. For example, about 20 % of all false alarms related to a verifier are
Klever: Verification Framework for Critical Industrial C Programs                   37

due to CPAchecker not supporting attributes packed and aligned. Also, there are
several non-modeled functions, each causing about 10 % of all false alarms related
to environment models.
   Fixing verification tools is a very laborious job, but they get better every year.
Additionally, we improve environment models steadily. Often, it is not enough to
eliminate the initial reasons for false alarms. After that, models for other functions
may be required, or CPAchecker can produce false alarms due to imprecise analysis.
   Caution: We manually assessed the reported Unsafes, so there may be some
mistakes. If the reader tries to repeat this work, one can obtain a more or less
different distribution.


4.1.2 Faults

In this subsection, we discuss the faults that we have found, as they represent quite
an important outcome for most users. There are two primary questions regarding the
discovered faults:
• Whether these faults are crucial enough or benign, of which static analysis tools
  are often accused of.
• Whether these faults can be easily found by other approaches.
   Klever helped to identify faults that can result in various bad consequences, such
as NULL pointer dereference, buffer overflow, usage of non-initialized data, memory
leaks, and so on. We prepared patches fixing some of them and sent these patches to
the Linux kernel developers to demonstrate that these faults are really essential. They
accepted most of the patches and rejected just a few of them since they corresponded
to situations that are not possible in practice (we need to improve our environment
models).
   Appendix F enumerates those faults that were found by Klever in Linux 5.5.
The total number of faults that were fixed by developers after our reports is 20.
The number of faults that were somehow identified by other means as well is 11.
Developers backported 14 commits to stable branches of the Linux kernel repository.
These branches represent a long-term support for older versions. Backporting to them
indicates that the Linux kernel developers agree that the corresponding faults are
really significant.
   Here is a discussion of the ability of other approaches to identify faults found by
Klever. Many faults (41 of 64) revealed in Linux 5.5 happen on error handling paths
that are executed extremely seldom. Moreover, they are unlikely covered by testing
and dynamic analysis tools. Most faults (52 of 64) manifest when a complicated
interaction with an environment takes place. This assumes a specific order of callback
invocation depending on their return values as well as the specific initialization of
their arguments. Besides, it may be necessary to comprehend the semantics of the
called functions, e.g., when, after a successful invocation of one function, another
one should be called. These cases may be pretty hard for lightweight static analysis
38                                          Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

tools. Though, certain tools will be able to find some faults revealed thanks to Klever
after specific tuning.
   We have not reported all detected faults to the Linux kernel developers yet, since
this process occupies quite a lot of time. Nevertheless, we are going to report the
remaining faults gradually.


4.1.3 Unknowns

Table 7 shows the number of Unknowns due to failures of CPAchecker and other
reasons. The share of Unknowns reported by CPAchecker when checking memory
safety is substantially higher than the one for remaining requirement specifications.
There have been no considerable changes in the distribution of Unknowns due to
CPAchecker and other reasons over time. Though, the absolute number of Unknowns
increased, which was already explained at the beginning of this subsection.


Table 7 Distribution of Unknowns.
                          Component   Linux 5.5 Linux 5.12-rc3
                                     Memory safety
                        CPAchecker 557 (64 %)        595 (62 %)
                        Others        312 (36 %)     367 (38 %)
                          Correct usage of the Linux kernel API
                        CPAchecker 579 (10 %)        683 (10 %)
                        Others       5,306 (90 %) 6,285 (90 %)


   Table 8 shows that timeouts are the most common reason for CPAchecker Un-
knowns especially for memory safety. For Linux 5.12-rc3 their share decreased
primarily due to more parsing failures.


Table 8 Distribution of CPAchecker Unknowns.
                          Unknown type Linux 5.5 Linux 5.12-rc3
                                       Memory safety
                          Timeout        510 (92 %) 526 (88 %)
                          Others          47 (8 %)      69 (12 %)
                            Correct usage of the Linux kernel API
                          Timeout        467 (81 %) 467 (68 %)
                          Others         112 (19 %) 216 (32 %)


   Users may wonder why we performed experiments with such small limits on
computational resources per verification task. For instance, for verification tasks
from the SV-COMP benchmark suite these limits are 3 times higher [5].
   Lack of memory is not such a common reason of Unknowns while with a lower
limit, one can solve more verification tasks in parallel or solve them on a less
powerful machine. Timeouts happen much more often. We evaluated the influence
Klever: Verification Framework for Critical Industrial C Programs                       39

of increasing the CPU time limit on the number of timeouts. Using the timeout
of 15 minutes resulted in 5 more Safes and one more Unsafe for requirements
specification drivers:clk1 while originally, there were about 3,300 of Safes and 14
Unsafes. The CPU time consumption of CPAchecker rose from 15 hours to 25 hours.
Further increasing the CPU time limit gave similar improvements in verification
results but degradation in CPU time.



4.2 Code Coverage

Table 9 presents current code coverage. It is reasonably high for particular subdirec-
tories, and for some modules it is 100 % while for some subdirectories and modules it
is very low. This is the case because we developed environment model specifications
not for all types of modules, as was discussed in the previous section. Code coverage
for Linux 5.12-rc3 varies not so much. This again demonstrates that Klever can be
applied to newer versions of target programs without considerable changes (indeed
there were no changes at all for the given experiment).


Table 9 Code coverage.
                              Linux 5.5                      Linux 5.12-rc3
     Subdirectory Line coverage, Function coverage, Line coverage, Function coverage,
                      KLOC           thousands          KLOC           thousands
     hid           24/37 (64 %)    1.2/2.1 (58 %)    25/38 (65 %)    1.3/2.2 (59 %)
     hwmon         33/63 (52 %)    1.5/3.9 (38 %)    34/67 (51 %)    1.5/4.1 (37 %)
     media        114/354 (32 %) 5.7/19.6 (29 %) 120/368 (33 %) 6.0/20.0 (29 %)
     mtd           19/51 (37 %)   0.86/2.8 (31 %)    18/50 (36 %)   0.81/2.7 (30 %)
     platform      13/34 (37 %)   0.76/2.5 (30 %)    15/39 (38 %)   0.89/2.9 (31 %)
     staging      53/159 (33 %)    2.4/8.2 (29 %)   40/127 (32 %)    1.8/6.3 (28 %)
     usb          66/163 (40 %)    3.5/8.8 (40 %)   63/158 (40 %)    3.3/8.5 (39 %)
     video         43/95 (45 %)    1.8/4.6 (40 %)    48/94 (51 %)    1.9/4.6 (41 %)
     Total        365/957 (38 %) 17.8/52.7 (34 %) 364/941 (39 %) 17.5/51.7 (34 %)




4.3 Verification Time

The overall time spent by Klever and the CPU time consumed by Klever components
and CPAchecker is demonstrated in Table 10.
   In total, it took about 7.4 days to get all the verification results. This time can
be considerably reduced by using more machines or a more powerful machine for
both the generation and solution of verification tasks. One can see that more time
was necessary for Linux 5.12-rc3. The primary reason for that is that there are
more modules and, thus, verification tasks. The solution of verification tasks by
40                                            Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

Table 10 Verification time in hours.
                  Type of time                     Linux 5.5 Linux 5.12-rc3
                                        Memory safety
                  Overall time                         10          11
                  CPU time of CPAchecker               52          53
                  CPU time of Klever components        16          17
                             Correct usage of the Linux kernel API
                  Overall time                         71          85
                  CPU time of CPAchecker              223          232
                  CPU time of Klever components       158          190



CPAchecker when checking memory safety consumed the most CPU time. The
generation of verification tasks by Klever components needed a rather considerable
portion of the CPU time to check the correct usage of the Linux kernel API.
   It is worth noting that we launched Klever several times when checking require-
ment specifications devoted to the correct usage of the Linux kernel API. For that rea-
son, some actions, like the generation of environment models, were duplicated during
the generation of verification tasks. These actions are not very time-consuming, so
if one checks these requirement specifications together, there may be up to 10 %
improvement in the overall time and the CPU time of Klever components.



5 Related Work

According to our knowledge, no existing tool automates the preparation of an ar-
bitrary C program before verification, runs verification tools, processes verification
results and provides means for their further analysis and improvement. Below, we
consider several frameworks intended for the verification of specific software, such
as device drivers or embedded software.
   SDV is the best-known example of an application of the automatic software veri-
fication technique in practice [4]. It aims at checking the correct usage of the kernel
API in Windows device drivers using SLAM, YOGI, and Q [3, 28]. There are also
LDV Tools [38], DDVerify[37], and Avinux [34] intended for verification of Linux
device drivers. These frameworks are based on CBMC [14] and CPAchecker [6].
As a result, hundreds of unrevealed faults have been found and acknowledged by
developers.
   CBMC is also known for various other applications, such as verification of
TinyOS [10] and embedded software [35]. Authors deliver successful case stud-
ies as a proof of concept. There is an IDE for development of embedded software
called mbeddr that allows to automatically run CBMC to check programs under de-
velopment against a predefined set of safety properties [11]. The IDE also provides
developers with nicely arranged results. However, mbeddr is not intended for auto-
mated verification of programs that were not developed using it. Another example of
Klever: Verification Framework for Critical Industrial C Programs                   41

a successful integration of CBMC into the development process is the recent work
devoted to verification of the AWS C Common library [13].
   DC2 aims at verification of industrial software [23]. To limit the verification
scope, it generates contracts relevant for finding such faults as memory leaks and
array-bound overflows. If necessary, users can improve these contracts manually.
Then DC2 runs the Varvel model checker. However, it is an in-house NEC research
project, so it is not possible to estimate its applicability to various C programs in
more detail.



6 Conclusion

The paper presents the ongoing work dedicated to applying automatic software
verification tools for critical industrial C programs like operating system kernels and
embedded software. We described the Klever software verification framework and
demonstrated the results of its practical evaluation. We based Klever on solutions
accepted by the SV-COMP community. Moreover, we keep in touch with verification
tool developers to cooperate and to solve the most vital problems together, discussing
the interface, providing feedback and contributing generated verification tasks to the
competition benchmark suite.
   Our experience clearly demonstrates that automatic software verification is a
very promising area since it enables finding faults in programs, many of which
could be hardly detected by other software quality assurance techniques. The more
efforts that are invested in related research, development and, especially, various
applications, the more awesome achievements will be reached. We hope that one day
automatic software verification techniques will become one of the best practices,
along with testing and static analysis. Moreover, we expect that for some industries,
like avionics, railways, and autonomous vehicles, the use of this technique will be
required by appropriate standards.



7 Acknowledgments

We would like to express special thanks to Prof. Dr. Alexander K. Petrenko who
was a scientific supervisor of most related works, researches and theses. Also, much
gratitude is due to Alexey Khoroshilov and Vadim Mutilin for their great ideas and
suggestions starting from the beginning of this project, to Pavel Shved, Alexander
Strakh, Mikhail Mandrykin, Pavel Andrianov, Anton Vasilyev, Vitaliy Mordan and
Denis Efremov for participating in the development of a Klever prototype as well as
for improving auxiliary tools and CPAchecker, to Vladimir Gratinskiy for investing
enormous efforts in the design and development of the most close to the user and
large Klever component, and to numerous students and users who made various
contributions.
42                                                Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

References

 1. Alkassar, E., Paul, W.J., Starostin, A., Tsyban, A.: Pervasive verification of an OS microkernel:
    inline assembly, memory consumption, concurrent devices. In: G.T. Leavens, P. O’Hearn, S.K.
    Rajamani (eds.) Proceedings of the 3rd International Conference on Verified Software: The-
    ories, Tools, Experiments, vol. 6217, pp. 71–85. Springer-Verlag, Berlin, Heidelberg (2010).
    URL https://doi.org/10.1007/978-3-642-15057-9_5
 2. Andrianov, P.: Analysis of correct synchronization of operating system components. Program-
    ming and Computer Software 46(8), 712–730 (2020). URL https://doi.org/10.1134/
    S0361768820080022
 3. Ball, T., Bounimova, E., Kumar, R., Levin, V.: SLAM2: static driver verification with under
    4% false alarms. In: R. Bloem, N. Sharygina (eds.) Proceedings of the 10th International
    Conference on Formal Methods in Computer-Aided Design, pp. 35–42. IEEE (2010). URL
    https://dl.acm.org/doi/10.5555/1998496.1998508
 4. Ball, T., Levin, V., Rajamani, S.K.: A decade of software model checking with SLAM. Com-
    munications of the ACM 54(7), 68–76 (2011). URL https://doi.org/10.1145/1965724.
    1965743
 5. Beyer, D.: Software verification: 10th comparative evaluation (SV-COMP 2021). In: Proceed-
    ings of the 27th International Conference on Tools and Algorithms for the Construction and
    Analysis of Systems, vol. 12652, pp. 401–422. Springer International Publishing (2021). URL
    https://doi.org/10.1007/978-3-030-72013-1_24
 6. Beyer, D., Keremoglu, M.E.: CPAchecker: a tool for configurable software verification. In:
    G. Gopalakrishnan, S. Qadeer (eds.) Proceedings of the 23rd International Conference on
    Computer Aided Verification, vol. 6806, pp. 184–190. Springer, Berlin, Heidelberg (2011).
    URL https://doi.org/10.1007/978-3-642-22110-1_16
 7. Beyer, D., Löwe, S., Wendler, P.: Reliable benchmarking: requirements and solutions. In-
    ternational Journal on Software Tools for Technology Transfer 21(1), 1–29 (2019). URL
    https://doi.org/10.1007/s10009-017-0469-y
 8. Black, P.E., Badger, L., Guttman, B., Fong, E.: Dramatically reducing software vulnerabilities:
    report to the White House Office of Science and Technology Policy. Tech. Rep. NISTIR 8151,
    National Institute of Standards and Technology, Gaithersburg, MD (2016). URL https:
    //doi.org/10.6028/NIST.IR.8151
 9. Brooks, F.P.: No silver bullet – essence and accidents of software engineering. Computer
    20(4), 10–19 (1987). URL https://doi.org/10.1109/MC.1987.1663532
10. Bucur, D., Kwiatkowska, M.Z.: Software verification for TinyOS. In: Proceedings of the
    9th ACM/IEEE International Conference on Information Processing in Sensor Networks, pp.
    400–401. ACM, New York, NY, USA (2010). URL https://doi.org/10.1145/1791212.
    1791274
11. Cârlan, C., Ratiu, D., Schätz, B.: On using results of code-level bounded model checking in
    assurance cases. In: A. Skavhaug, J. Guiochet, E. Schoitsch, F. Bitsch (eds.) Proceedings of the
    2016 International Conference on Computer Safety, Reliability, and Security, vol. 9923, pp.
    30–42. Springer, Cham (2016). URL https://doi.org/10.1007/978-3-319-45480-1_3
12. Castaño, R., Braberman, V., Garbervetsky, D., Uchitel, S.: Model checker execution reports.
    In: Proceedings of the 32nd IEEE/ACM International Conference on Automated Software
    Engineering, pp. 200–205. IEEE Press, Piscataway, NJ, USA (2017). URL https://doi.
    org/10.1109/ASE.2017.8115633
13. Chong, N., Cook, B., Eidelman, J., Kallas, K., Khazem, K., Monteiro, F., Schwartz-Narbonne,
    D., Tasiran, S., Tautschnig, M., Tuttle, M.: Code-level model checking in the software devel-
    opment workflow at amazon web services. Software: Practice and Experience 51(4), 772–797
    (2021). URL https://doi.org/10.1002/spe.2949
14. Clarke, E., Kroening, D., Lerda, F.: A tool for checking ANSI-C programs. In: K. Jensen,
    A. Podelski (eds.) Proceedings of the 10th International Conference on Tools and Algorithms
    for the Construction and Analysis of Systems, vol. 2988, pp. 168–176. Springer, Berlin, Hei-
    delberg (2004). URL https://doi.org/10.1007/978-3-540-24730-2_15
Klever: Verification Framework for Critical Industrial C Programs                              43

15. Dudka, K., Peringer, P., Vojnar, T.: Byte-precise verification of low-level list manipulation.
    In: F. Logozzo, M. Fähndrich (eds.) Proceedings of the 20th International Symposium on
    Static Analysis, vol. 7935, pp. 215–237. Springer, Berlin, Heidelberg (2013). URL https:
    //doi.org/10.1007/978-3-642-38856-9_13
16. Efremov, D., Mandrykin, M., Khoroshilov, A.: Deductive verification of unmodified Linux
    kernel library functions. In: T. Margaria, B. Steffen (eds.) Proceedings of the 8th Interna-
    tional Symposium on Leveraging Applications of Formal Methods, Verification and Valida-
    tion, vol. 11245, pp. 216–234. Springer, Cham (2018). URL https://doi.org/10.1007/
    978-3-030-03421-4_15
17. Ferreira, J.F., Gherghina Cristian He, G., Qin, S., Chin, W.N.: Automated verification of the
    FreeRTOS scheduler in HIP/SLEEK. International Journal on Software Tools for Technology
    Transfer 16(4), 381–397 (2014). URL https://doi.org/10.1007/s10009-014-0307-4
18. Friedberger, K.: CPA-BAM: Block-abstraction memoization with value analysis and predicate
    analysis (competition contribution). In: M. Chechik, J.F. Raskin (eds.) Proceedings of the
    22nd International Conference on Tools and Algorithms for the Construction and Analysis
    of Systems, vol. 9636, pp. 912–915. Springer, Berlin, Heidelberg (2016). URL https:
    //doi.org/10.1007/978-3-662-49674-9_58
19. Glass, R.L.: Facts and fallacies of software engineering. Addison-Wesley Professional (2002)
20. Gotsman, A., Yang, H.: Modular verification of preemptive OS kernels. In: Proceedings of
    the 16th ACM SIGPLAN International Conference on Functional Programming, pp. 404–417.
    ACM, New York, NY, USA (2011). URL https://doi.org/10.1145/2034773.2034827
21. Gu, R., Koenig, J., Ramananandro, T., Shao, Z., Wu, X.N., Weng, S.C., Zhang, H., Guo, Y.:
    Deep specifications and certified abstraction layers. In: Proceedings of the 42nd Annual ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages, pp. 595–608.
    ACM, New York, NY, USA (2015). URL https://doi.org/10.1145/2676726.2676975
22. Hoare, C.A.R.: Communicating sequential processes. Communications of the ACM 21(8),
    666–677 (1978). URL https://doi.org/10.1145/359576.359585
23. Ivančić, F., Balakrishnan, G., Gupta, A., Sankaranarayanan, S., Maeda, N., Imoto, T.,
    Pothengil, R., Hussain, M.: Scalable and scope-bounded software verification in Varvel. Au-
    tomated Software Engineering 22(4), 517–559 (2015). URL https://doi.org/10.1007/
    s10515-014-0164-0
24. Jhala, R., Majumdar, R.: Software model checking. ACM Computing Surveys 41(4), 1–54
    (2009). URL https://doi.org/10.1145/1592434.1592438
25. Khoroshilov, A., Mutilin, V., Novikov, E., Zakharov, I.: Modeling environment for static
    verification of Linux kernel modules. In: A. Voronkov, I. Virbitskaite (eds.) Proceed-
    ings of the 9th International Conference on Perspectives of System Informatics, vol. 8974,
    pp. 400–414. Springer, Berlin, Heidelberg (2015). URL https://doi.org/10.1007/
    978-3-662-46823-4_32
26. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.: Frama-C: a software
    analysis perspective. Formal Aspects of Computing 27(3), 573–609 (2015). URL https:
    //doi.org/10.1007/s00165-014-0326-7
27. Klein, G., Andronick, J., Elphinstone, K., Murray, T., Sewell, T., Kolanski, R., Heiser, G.:
    Comprehensive formal verification of an OS microkernel. ACM Transactions on Computer
    Systems 32(1), 1–70 (2014). URL https://doi.org/10.1145/2560537
28. Lal, A., Qadeer, S.: Powering the Static Driver Verifier using Corral. In: Proceedings of the
    22nd ACM SIGSOFT International Symposium on Foundations of Software Engineering, pp.
    202–212. ACM, New York, NY, USA (2014). URL https://doi.org/10.1145/2635868.
    2635894
29. Necula, G.C., McPeak, S., Rahul, S.P., Weimer, W.: CIL: intermediate language and tools for
    analysis and transformation of C programs. In: R.N. Horspool (ed.) Proceedings of the 11th
    International Conference on Compiler Construction, pp. 213–228. Springer, Berlin, Heidelberg
    (2002). URL https://doi.org/10.1007/3-540-45937-5_16
30. Novikov, E.: An approach to implementation of aspect-oriented programming for C. Program-
    ming and Computer Software 39(4), 194–206 (2013). URL https://doi.org/10.1134/
    S0361768813040051
44                                             Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

31. Novikov, E., Khoroshilov, A.: Using aspect-oriented programming for querying source code.
    Proceedings of the Institute for System Programming of the RAS 23, 371–386 (2012). URL
    https://doi.org/10.15514/ISPRAS-2012-23-21
32. Novikov, E., Zakharov, I.: Towards automated static verification of GNU C programs. In:
    A. Petrenko, A. Voronkov (eds.) Proceedings of the 11th International Andrei Ershov Memorial
    Conference on Perspectives of System Informatics, vol. 10742, pp. 402–416. Springer, Cham
    (2017). URL https://doi.org/10.1007/978-3-319-74313-4_30
33. Novikov, E., Zakharov, I.: Verification of operating system monolithic kernels without ex-
    tensions. In: T. Margaria, B. Steffen (eds.) Proceedings of the 8th International Symposium
    on Leveraging Applications of Formal Methods, Verification, and Validation, vol. 11247, pp.
    230–248. Springer International Publishing, Cham (2018). URL https://doi.org/10.
    1007/978-3-030-03427-6_19
34. Post, H., Küchlin, W.: Integrated static analysis for Linux device driver verification. In:
    Proceedings of the 6th International Conference on Integrated Formal Methods, vol. 4591,
    pp. 518–537. Springer, Berlin, Heidelberg (2007). URL https://doi.org/10.1007/
    978-3-540-73210-5_27
35. Schlich, B., Kowalewski, S.: Model checking C source code for embedded systems. Inter-
    national Journal on Software Tools for Technology Transfer 11(3), 187–202 (2009). URL
    https://doi.org/10.1007/s10009-009-0106-5
36. Tassey, G.: The economic impacts of inadequate infrastructure for software testing: final
    report. Diane Publishing Company (2002). URL https://www.nist.gov/system/files/
    documents/director/planning/report02-3.pdf
37. Witkowski, T., Blanc, N., Kroening, D., Weissenbacher, G.: Model checking concurrent Linux
    device drivers. In: Proceedings of the 22nd IEEE/ACM International Conference on Automated
    Software Engineering, pp. 501–504. ACM, New York, NY, USA (2007). URL https://doi.
    org/10.1145/1321631.1321719
38. Zakharov, I., Mandrykin, M., Mutilin, V., Novikov, E., Petrenko, A., Khoroshilov, A.: Con-
    figurable toolset for static verification of operating systems kernel modules. Program-
    ming and Computer Software 41(1), 49–64 (2015). URL https://doi.org/10.1134/
    S0361768815010065
39. Zakharov, I., Novikov, E.: Compositional environment modelling for verification of GNU C
    programs. In: Proceedings of the 2018 Ivannikov Ispras Open Conference, pp. 39–44. IEEE
    (2018). URL https://doi.org/10.1109/ISPRAS.2018.00013
Klever: Verification Framework for Critical Industrial C Programs                  45

A Appendix: Auxiliary Tools

A.1 Clade

For their operation, several Klever components require a lot of information on a
program under verification and its build process, for instance:
• Original program source files. In some cases their preprocessed versions may be
  necessary as well.
• Information on build commands such as compilation, linking, assembler, archive,
  move, etc. These build commands need to be parsed, and information about their
  input and output files, command-line options and environment variables should
  be collected.
• List of all header dependencies for each C source file.
• Graphs demonstrating connections between build commands both by parent-child
  relations and by relations of their input and output files.
• Definitions and expansions of macros and macro functions. Definitions and dec-
  larations of functions, types and global variables. Source code locations for these
  entities and their usages.
• A function callgraph.
   Surprisingly, for different platforms as well as for different build environments,
many unexpected issues need to be solved in order to support the process of collection
of such information. Reliable solutions for these issues are proprietary; thus, we
decided to develop our own tool called Clade28.
   Clade can intercept all build commands that are executed during a typical
build process. Depending on a platform, it supports several different methods to
do this. On Linux and macOS, Clade intercepts and handles calls to exec func-
tions issued for each build command. This is achieved by using LD PRELOAD and
DYLD INSERT LIBRARIES mechanisms of the dynamic linker correspondingly. On
Windows, Clade uses a simple debugger that:
• Waits for process start events that correspond to the execution of build commands.
• Pauses the build process and reads the memory of newly created processes to find
  and log their command-line arguments
• Resumes the build process.
    Clade includes many extensions that can parse intercepted build commands, col-
lect information about source code, and perform various actions using the collected
data. As a result, Clade outputs a so-called build base, which is a stand-alone folder
that can be archived, easily transferred to a different computer and used there. Clade
has a command-line interface for integration with build processes and execution of
its extensions as well as a stable Python API.



28 https://github.com/17451k/clade
46                                                Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

A.2 CIF

Both Clade and some Klever components need a tool for querying and weaving
source code. Since there was not an appropriate tool at that time when we needed it,
we developed CIF29 [30].
    CIF implements an aspect-oriented extension for the C programming language to
weave so-called cross-cutting concerns into the source code30. We use these capabil-
ities during environment modeling and development of requirement specifications,
e.g. to replace function calls with calls to models. CIF supports source-to-source
weaving that is necessary for application of verification tools. Besides, CIF allows
basic queries to source code [31] which are, nevertheless, powerful enough to get all
information required by Clade.
    CIF is based upon GCC 7.5 and supports a vast majority of GNU C extensions
that can influence verification results. At the moment, CIF does not support some
specific expressions, which may result in failures during weaving and querying of
the source code.



A.3 CIL

CIL is a source-to-source transformation tool allowing merging preprocessed C
source files [29]. Besides, CIL performs many optimizations like removing unused
functions that can simplify verification tasks rather considerably.
   Klever uses CIL from Frama-C [26] with a number of our own improvements
and fixes developed within the VerKer project31 [16]. As with CIF there are some
specific unsupported code constructions.



A.4 BenchExec

BenchExec [7] is a convenient and reliable tool to solve verification tasks using
a single machine. It is used for benchmarking verification tools within SV-COMP
starting from the beginning. There are following important features of BenchExec
for Klever use cases:
• BenchExec allows to precisely measure and limit computational resources such
  as CPU time and memory. Moreover, there is the RunExec tool that helps to run
  other tools in addition to verification tools.



29 https://forge.ispras.ru/projects/cif
30 https://cif.readthedocs.io/en/latest/aoc.html
31 https://forge.ispras.ru/projects/astraver/repository/framac?rev=20.0
Klever: Verification Framework for Critical Industrial C Programs                47

• BenchExec contains wrappers for all verification tools that participate in SV-COMP.
  These wrappers help to run them without changing the format of verification tasks
  and without tool specific output processing.



B Appendix: Decomposition Specification Examples

There are examples of decomposition specifications in Fig. 25 and Fig. 26. The
strings ”3.14” and ”1.28.3” distinguish different versions of each program. The
attribute ”fragments” allows to define program fragments by listing files or other
program fragments explicitly. Attributes ”add to all fragments” and ”exclude from
all fragments” allow to add and remove files, program fragments or even functions
(PFG finds a file with a function definition and adds it).

"3.14": {
  "fragments": {
    "drivers/usb/serial/usbserial.ko": [
      "drivers/usb/serial/usb_debug.ko",
      "drivers/usb/serial/usbserial.ko"
    ]
  }
}



Fig. 25 Decomposition specification example for the Linux kernel.




"1.28.3": {
  "exclude from all fragments": [
     "libbb/getopt32.c",
     "libbb/xfuncs_printf.c"
  ],
  "add to all fragments": [
     "libbb/wfopen.c",
     "libbb/wfopen_input.c"
  ]
}



Fig. 26 Decomposition specification example for Busybox.




C Appendix: Intermediate Model Example

In Fig. 27, one can find a fragment of an intermediate model. It describes a single
scenario model 𝜀 =< V, A, R, 𝛼0 >. In Fig. 28 there is an equivalent scenario
model generated as a function in the C programming language.
48                                           Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

   Labels V are defined in the labels entry. They are escaped with % characters in
C statements and logical expressions below.
   The actions entry describes each action of A in details. There is the fail base
block in the intermediate model. The condition entry describes its precondition 𝜑,
statements correspond to 𝛽. reg is a sending signal action. Its label 𝑙 equals to the
name of the action. Precondition 𝜑 is specified in the condition entry. Vector 𝜋
is stored in parameters but it is empty in the example. Comment entries help to
generate the environment model source code with hints extracted at processing and
visualization of violation witnesses.

{
     "tty/callbacks": {
         "labels": {
              "driver": {"declaration": "struct tty_driver *driver"},
              "retval": {"declaration": "int retval"},
              "ops": {"declaration": "struct tty_operations *ops",
                      "value": "__VERIFIER_nondet_pointer()"}
         },
         "actions": {
           "callbacks": {
              "comment": "Begin functions calls.",
              "parameters": []
           },
           "alloc": {
              "comment": "Allocate device.",
              "statements": ["%driver% = tty_alloc_driver(...);"]
           },
           "reg": {
              "comment": "Register callbacks.",
              "statements": ["tty_set_operations(%driver%, %ops%);",
                             "%retval% = tty_register_driver(%driver%);"],
              "condition": ["%driver% != 0"]
           },
           "unreg": {
              "comment": "Unregister callbacks.",
              "statements": ["tty_unregister_driver(%driver%);",
                             "put_tty_driver(%driver%);"],
              "condition": ["%retval% == 0"]
           },
           "fail": {
              "comment": "Failed to register callbacks.",
              "statements": ["put_tty_driver(%driver%);"],
              "condition": ["%retval% != 0"]
           },
           "skip": {
              "comment": "Failed to allocate memory for the driver.",
              "condition": ["%driver% == 0"]
           }
         },
         "process": "(!callbacks).<alloc>.(<reg>.(<unreg> | <fail>) | <skip>)"
     }
}



Fig. 27 Scenario model example.
Klever: Verification Framework for Critical Industrial C Programs                   49

void entry_point(void) {
    int retval;
    struct tty_driver *driver;
    struct tty_operations *ops;
    ops = __VERIFIER_nondet_pointer();

     driver = tty_alloc_driver(...);
     if (__VERIFIER_nondet_int() && driver != 0) {
         tty_set_operations(driver, ops);
         retval = tty_register_driver(driver);
         if (retval == 0) {
             tty_unregister_driver(driver);
             put_tty_driver(driver);
         } else {
             put_tty_driver(driver);
         }
     }
}



Fig. 28 Scenario model example in the C programming language.



D Appendix: Requirement Specifications Base

A requirement specifications base contains high-level descriptions of requirement
specifications for a given project. These descriptions enumerate requirement speci-
fication files, select how to generate environment models, point out specific options
for a chosen verification tool, etc. Fig. 29 demonstrates how we do this for require-
ment specifications kernel:locking:rwlock, kernel:locking:spinlock, kernel:module,
and memory safety for the Linux kernel. In this example one can see templates
loadable kernel modules and kernel subsystems, and memory safety for loadable
kernel modules and kernel subsystems. They are used to avoid duplicate options for
particular requirement specifications. Each template describes a sequence of plugins
that will be invoked by Klever Core to generate verification tasks for the verification
tool step by step. For instance, template loadable kernel modules and kernel sub-
systems requires Environment Model Generator (EMG), Requirement Specification
Generator (RSG), and Final Verification Task Preparator (FVTP) to be invoked. One
can specify necessary options for each plugin, e.g. common models for RSG that
will be used for all requirement specifications referring this template.
   Requirement specifications themselves are described in the tree form where leaves
represent particular requirement specifications. One can specify template at any
level of the tree, and it will be used by all children recursively unless it will be
overwritten. For instance, requirement specification kernel:locking:rwlock refers
template loadable kernel modules and kernel subsystems. Besides, it says that certain
model linux/kernel/locking/rwlock.c should be used by RSG in addition to common
models. This distinguishes the given requirement specification from the other ones.
   Verifier profiles referred in the figure are discussed in Appendix E.
50                                              Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

{
     "templates": {
        "loadable kernel modules and kernel subsystems": {
          "plugins": [
             {
               "name": "EMG",
               "options": {
                  "generators options": [...],
                  "translation options": {...}
               }
             },
             {
               "name": "RSG",
               "options": {
                  "model compiler input file": "scripts/mod/empty.c",
                  "common models": ["linux/arch/asm/atomic.c", ...]
               }
             },
             {
               "name": "FVTP",
               "options": {
                  "verifier profile": "reachability",
                  "verifier": {"name": "CPAchecker", "version": "trunk:31140"}
               }
             }
          ]
        },
        "memory safety for loadable kernel modules and kernel subsystems": {...}
     },
     "requirement specifications": {
        "description": "Linux requirement specifications",
        "template": "loadable kernel modules and kernel subsystems",
        "children": [
          {
             "identifier": "kernel",
             "children": [
               {
                  "identifier": "locking",
                  "children": [
                     {
                       "identifier": "rwlock",
                       "plugins": [{
                          "name": "RSG",
                          "options": {"models": ["linux/kernel/locking/rwlock.c"]}
                       }]
                     },
                     {"identifier": "spinlock", ...}
                  ]
               },
               {
                  "identifier": "module",
                  "plugins": [{
                     "name": "RSG",
                     "options": {"models": ["linux/kernel/module.c"]}
                  }]
               }
             ]
          },
          {
             "identifier": "memory safety",
             "template": "memory safety for loadable kernel modules and kernel subsystems"
          },
          ...
        ]
     }
}



Fig. 29 Requirement specifications base example.
Klever: Verification Framework for Critical Industrial C Programs                               51

E Appendix: Verifier Profile Example

There is a verifier profiles example in Fig. 30. The snippet contains:
• Three templates CPAchecker common, CPAchecker BAM, and CPAchecker SMG
  that describe common CPAchecker configurations. BAM stands for Block Ab-
  straction Memoization and SMG for Symbolic Memory Graphs.
• Two verifier profiles reachability, and memory safety checking that refer these
  templates and describe final configurations for CPAchecker trunk:31440.
It is allowed to inherit templates and to modify or add some additional options both
in templates and verifier profiles. For instance, template CPAchecker BAM inherits
template CPAchecker common, and specifies certain safety properties to be checked
as well as some extra options in addition. Also, one is capable to provide different
sets of options for various versions of the same tool by describing appropriate verifier
profiles.



F Appendix: Faults Found by Klever in the Linux Kernel

Table 11 enumerates those faults that were found by Klever in Linux 5.5 and that
were already fixed in the mainstream as of May 29, 2021.




32 Commit SHAs in Git repository https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git.
52                                              Ilja Zakharov, Evgeny Novikov, Ilya Shchepetkov

 {
     "templates": {
        "CPAchecker common": {
          "description": "Common options for the CPAchecker tool",
          "add options": [
             {"-setprop": "counterexample.export.exportExtendedWitness=true"},
             ...
          ]
        },
        "CPAchecker BAM": {
          "description": "CPAchecker with BAM for reachability checking",
          "inherit": "CPAchecker common",
          "safety properties": [
             "CHECK( init({entry_point}()), LTL(G ! call(__VERIFIER_error())) )"
          ],
          "add options": [
             {"-ldv-bam": ""},
             ...
          ]
        },
        "CPAchecker SMG": {
          "description": "CPAchecker SMG for memory safety checking",
          "inherit": "CPAchecker common",
          "safety properties": [
             "CHECK( init({entry_point}()), LTL(G valid-free) )",
             ...
          ],
          "add options": [
             {"-smg-ldv": ""},
             ...
          ]
        }
     },
     "profiles": {
        "reachability": {
          "CPAchecker": {
             "trunk:31140": {"inherit": "CPAchecker BAM"}
          }
        },
        "memory safety checking": {
          "CPAchecker": {
             "trunk:31140": {"inherit": "CPAchecker SMG"}
          }
        }
     }
 }



Fig. 30 Verifier profiles example.
Klever: Verification Framework for Critical Industrial C Programs             53

Table 11 Faults found by Klever in Linux 5.5
Loadable kernel module Requirements              Fixed by Reported Mainline Backported
                       specification            developers by us    commit32
aspeed-pwm-tacho.ko    memory safety                No      Yes    bc4071aafcf4 Yes
bttv.ko                memory safety               Yes      No    7b817585b730  Yes
vpif capture.ko        memory safety                No      Yes   602649eadaa0  Yes
qcom-camss.ko          memory safety                No      Yes   f45882cfb152  Yes
s5p-jpeg.ko            memory safety                No      Yes   0862d95b437b  No
vicodec.ko             memory safety               Yes      No    f36592e7b343  Yes
rc-core.ko             memory safety                No      Yes   3b4cfc6966ec  No
usbtv.ko               memory safety               Yes      No    bf65f8aabdb3  Yes
plat-ram.ko            memory safety                No      Yes   8c293f545419  No
goldfish pipe.ko       memory safety               Yes      No    43c2cc2864bc  No
kpc2000.ko             memory safety               Yes      No    b17884ccf29e  Yes
kpc dma.ko             memory safety                No      Yes   8ce8668bfb64  No
rts5208.ko             memory safety                No      Yes   11507bf9a883  Yes
net2272.ko             memory safety               Yes      Yes   9b719c7119e7  No
net2280.ko             memory safety               Yes      Yes   f770fbec4165  No
usbtest.ko             memory safety               Yes      No    28ebeb8db770  Yes
da8xx-fb.ko            memory safety                No      Yes   80a00e90dede  No
savagefb.ko            memory safety                No      Yes   e8d35898a78e  Yes
sm712fb.ko             memory safety                No      Yes   19e55a87ad62  No
rtl2832 sdr.ko         kernel:module                No      Yes   ce5d72b6f5a0  No
isif.ko                arch:mm:ioremap              No      Yes   6651dba2bd83  No
vpss.ko                arch:mm:ioremap              No      Yes   9c487b0b0ea7  Yes
goku udc.ko            arch:mm:ioremap              No      Yes   0d66e04875c5  Yes
net2272.ko             arch:mm:ioremap              No      Yes   ae90cc8237bf  No
sm712fb.ko             arch:mm:ioremap              No      Yes   bcee1609ba96  No
usbtv.ko               drivers:usb:core:usb:dev    Yes      No    bf65f8aabdb3  Yes
stm32 fmc2 nand.ko     drivers:clk1                Yes      No    71d1f1d5958f  No
vf610 nfc.ko           drivers:clk1                 No      Yes   cb7dc3178a98  Yes
cadence-quadspi.ko     drivers:clk1                Yes      No    c61088d1f993  No
ad5933.ko              drivers:clk2                Yes      No    da7de29bb171  No
ci hdrc usb2.ko        drivers:clk2                Yes      No    c2de37b31f17  No
