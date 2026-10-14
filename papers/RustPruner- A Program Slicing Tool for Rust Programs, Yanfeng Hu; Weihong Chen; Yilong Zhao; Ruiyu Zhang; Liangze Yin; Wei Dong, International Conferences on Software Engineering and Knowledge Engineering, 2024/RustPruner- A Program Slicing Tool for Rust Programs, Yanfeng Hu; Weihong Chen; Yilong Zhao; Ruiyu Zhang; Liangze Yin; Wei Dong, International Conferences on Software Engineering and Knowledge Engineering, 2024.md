         RustPruner: A Program Slicing Tool for Rust
                         Programs
                   Yanfeng Hu, Weihong Chen, Yilong Zhao, Ruiyu Zhang, Liangze Yin∗ , Wei Dong
                        College of Computer, National University of Defense Technology, Changsha, China
                        {huyanfeng22, chenweihong, zylong, zhangruiyu, yinliangze, wdong}@nudt.edu.cn


   Abstract—In the realm of analyzing Rust programs, traditional            is not only inefficient but also fails to fully leverage the
full-scale analytical approaches are often rendered impractical             distinctive features of the Rust language.
due to considerable time and performance expenditures. Despite                 To address these issues, this paper presents RustPruner, a
the potential for program slicing technologies to drastically
curtail these expenses, the vast majority of existing slicing tools         tool designed to provide Rust developers with an efficient
lack compatibility with the Rust language. This study introduces            and precise solution for code slicing. RustPruner resolves
RustPruner, a specialized tool designed for slicing Rust code.              compatibility issues with traditional slicing tools by trans-
RustPruner commences by constructing a goto-style control flow              forming programs into an intermediate goto representation
graph (CFG) through rigorous control flow analysis, comprehen-              that captures the language-specific features of Rust. Through
sively mapping out all feasible execution paths. Subsequently, it
leverages a backward slicing algorithm, integrating the outcomes            backward analysis [4], it traces from the program’s outputs
of program dependency analysis and abstract syntax tree (AST)               or assertions to all code that may affect the results, revealing
analysis, to generate precise program slices. By innovatively               the dependencies among various parts of the program. This
adapting slicing technology to Rust, RustPruner facilitates com-            analysis is especially crucial for understanding the system
prehensive, low-level analysis of Rust’s distinctive features. The          structure in large software projects. Through this process, we
generated slices undergo rigorous compilation and verification
procedures, thereby enhancing the efficiency of the analysis                can obtain the most minimal code segments closely related
process. The effectiveness of RustPruner has been validated                 to the target, effectively reducing interference from irrelevant
within some crucial system modules of operational operating                 code and enhancing the focus and accuracy of the analysis.
systems, which significantly improves both the efficiency and                  In the experimental section, this paper employs validation
accuracy of the verification.                                               projects from real-world operating systems to assess the ef-
   Index Terms—Rust analysis, program slicing, control flow
                                                                            fectiveness and performance of RustPruner. The four projects
graph, abstract syntax tree
                                                                            in the experimental section all originate from the process
                                                                            scheduling module, which is a key module of the operating
                         I. I NTRODUCTION
                                                                            system. The experimental results indicate that RustPruner
   Rust has rapidly emerged in the field of software develop-               not only significantly reduces the amount of code but also
ment, championed by its safety features. Following its initial              maintains the consistency of verification properties through
release in 2010, Rust has been extensively adopted across vari-             program verification operations on the generated slices. This
ous critical domains. To guarantee the security and correctness             enhances the efficiency and precision of verification and
of these systems, thorough code analysis and verification are               analysis tasks and also confirms the practicality of the tool
required, which can significantly deplete time and performance              in managing larger projects.
resources. Program slicing can mitigate much of such resource                  The contributions of this paper are as follows:
expenditure by eliminating unnecessary analysis, making it                     1) We propose a framework for program slicing in Rust
especially vital in Rust development. However, despite the                         that effectively tackles the challenges associated with
swift growth of Rust, there is a notable lack of slicing tools                     Rust language slicing, thereby enhancing the efficiency
tailored for Rust.                                                                 and accuracy of code analysis.
   Program slicing [1] is a method of code analysis that                       2) Compatibility issues of Rust language features in tradi-
enables developers to extract code segments related to specific                    tional slicing tools are resolved, and efficient filtering
functionalities or requirements. Although Rust slicing holds                       and reorganization of code are achieved through precise
significant potential in theory, it faces considerable challenges                  AST analysis using a custom visitor.
in practical application. Firstly, the unique ownership [2] and                3) The RustPruner tool is successfully implemented based
lifetime [3] rules of the Rust language complicate the applica-                    on the proposed framework and its performance are eval-
tion of slicing techniques. Secondly, the current lack of slicing                  uated in complex verification projects, demonstrating the
tools tailored for the Rust language often necessitates reliance                   tool’s validity and capabilities.
on manual analysis for Rust program slicing operations, which                  The rest of this paper is organized as follows. Section
                                                                            2 provides background information. Section 3 discusses the
  This work was funded by the National Nature Science Foundation of China
(No. U2341212, No. 62032024).                                               technical framework of the tool. Section 4 evaluates the
  *Corresponding author                                                     efficacy of RustPrunner. Section 5 lists related literature.

DOI reference number: 10.18293/SEKE2024-118
                                                                Sour ce Code Pr ocessing                                                     Slicing Implementation
      use
        usestd::*;
               std::*;
      ......
        ......                                  single_file
      fnfnfunc1(x:
              func1(x:i32)->i32{
                         i32)->i32{
           return
             returnxx++1;1;                                            Control Flow Analysis               Backward Slicing
                                                                                                                              Dependence
      }}                               Source                  Proof                             Goto
                                                                               Kani                             CBMC            Relation
      fnfnfunc2(x:
              func2(x:i32)->i32{
                         i32)->i32{                                                                                                                                      Slice_Rust
           return
             returnxx++2;2;                     project_file                                                                                           File Processing
      }}
      fnfnmain(){
              main(){                                                                                                                       Matching
           let
             letxx==0;0;
           let
             letyy==1;1;                                                                                                                                     File
           let
             letaa==func(x);
                       func(x);                                            AST Analysis                                                                Transformation
           assert!
             assert! (a   == 1);
                       (a ==  1);
      }}                                                          syn                              visit
                                                   Source                         AST                              Span
                                                                                               CodeCollector




                                                                  Fig. 1: The RustPruner Overview


                                 II. BACKGROUND                                                            code. In Rust, the language’s AST can be obtained through
A. Program Slicing                                                                                         the syn library [12]. The Span in the syn library is a core
                                                                                                           concept, representing a specific area in the source code, such
   Program slicing [1] is a code analysis technique that extracts                                          as the start and end positions of an identifier, expression, or
the smallest segment of code directly related to a specific goal                                           statement. This concept is crucial for understanding the code
from complex program code. This concept was first formally                                                 structure and performing precise code analysis.
introduced by Weiser in his 1979 doctoral dissertation [5].                                                   Furthermore, Kani [13] is a symbolic model checking tool
The basic process of program slicing includes several key                                                  for the intermediate intermediate representation (MIR) [14]
steps: first, construct the control flow graph (CFG) [6], which                                            of Rust. It serves as a backend for the Rust compiler’s code
represents all possible execution paths in the program; then                                               generation, using the kani::proof attribute to specify functions
perform data flow analysis to determine how the values of                                                  that need to be verified with the Kani tool. Kani performs
variables and expressions propagate within the program; then,                                              control flow and data flow analysis on these functions and
based on the analysis results, construct a dependency graph                                                transforms MIR into goto programs. Goto programs are a
[7] and use slicing algorithms, such as forward slicing [8],                                               type of control flow graph that includes key information such
backward slicing [9], static slicing [10], dynamic slicing [11],                                           as variable and type information, function call relationships,
etc., to extract code segments related to requirements from the                                            execution paths, and conditional judgments. However, it is
dependency graph.                                                                                          worth noting that Kani does not support slicing functions and
B. Challenges                                                                                              therefore cannot perform slicing analysis.
                                                                                                              In addition, CBMC [15] is a static verification tool designed
   As an emerging system programming language, Rust’s
                                                                                                           to identify potential errors in programs. CBMC can optimize
unique ownership [2] and lifetime [3] checking mechanisms
                                                                                                           goto programs, including dead code elimination [16], function
directly affect the slicability of code. In the Rust programming
                                                                                                           inlining [17], Goto slicing [18], etc. The core mechanism of
language, ownership and lifetimes are two core concepts for
                                                                                                           Goto slicing is to deeply analyze the Control Flow Graph
memory safety at compile time. Ownership rules define how
                                                                                                           (CFG) [6], identify and replace unreachable basic blocks with
resources are allocated, shared, and released, while lifetimes
                                                                                                           skip statements, which are ultimately removed. This process
ensure the validity of references. When slicing, it is necessary
                                                                                                           specifically targets functions or methods that will never be
to clarify the ownership of the data to avoid multiple releases
                                                                                                           touched during program execution, as well as branches in con-
of data or dangling references. At the same time, the lifetime
                                                                                                           ditional statements that are never satisfied. Although CBMC is
of the slice must be consistent with the shortest lifetime of the
                                                                                                           a powerful tool, it is mainly designed for C and C++ languages
referenced data. These factors combined bring new challenges
                                                                                                           and lacks support for features of other languages, such as
to slicing Rust programs, leading to a relative scarcity of Rust
                                                                                                           Rust’s ownership and lifetime.
slicing tools at present.

C. Current Status of Tools                                                                                                                 III. M ETHODOLOGY
   In the Rust language, the abstract syntax tree (AST) plays                                                 Fig. 1 depicts the technical framework of RustPruner. It
an extremely important role. The AST represents various                                                    consists of three principal processes: source code processing,
elements in the source code and their interrelationships in                                                AST analysis, and slicing implementation. The remaining
a tree-like form. By recursion or iteration, each node of the                                              sections will provide an in-depth presentation of the specifics
AST can be easily accessed, making it simple to traverse the                                               for each process.
A. Source Code Processing                                            21     let p3 = Point{x: 0, y: 0};
                                                                     22     let dist = p1.distance(&p2);
   Our tool can conduct dependency analysis on both individ-         23     assert!(dist == 4);
ual Rust files and entire Rust projects. Single files typically do   24 }
not import Rust libraries other than the standard library and        25 #[kani::proof]
only contain Rust source code, suitable for simple scenarios.        26 fn verifymain(){
On the other hand, project files consist of multiple source files,   27 main();
                                                                     28 }
configuration files, and dependencies, managed by Cargo, suit-
able for the development of complex applications or libraries.          The above source code can be parsed into the structure
Therefore, during dependency acquisition, the two inputs are         diagram shown in Fig. 2. As the Figure shows, each red
processed separately to improve the accuracy and efficiency          arrow in the parsing diagram is obtained through source code
of the analysis.                                                     processing. Starting from the entry flag proof, it enters the
   We receive a Rust file (or project) for verification and start    unique called function main of the function verifymain(), from
from each statement in the target function proof, which is the       assert it finds the definition statement of the variable dist,
entry function for the Kani verification tool and also the slicing   and then according to the definition statement, it finds the
entry for RustPruner. Conduct a data flow analysis, using the        called function distance and parameters p1 and p2 in the right
Kani verification tool to obtain a control flow graph in the form    value of the statement, and finds the structure definition of the
of a goto file, which includes all possible execution paths and      parameter struct. Finally, the nodes involved are connected
a large amount of dependency information unrelated to the            with red arrows. The arrows in the diagram represent the
proof framework. Then, conduct a backward analysis through           dependency and dependent relationships, with the starting
the assertions in the proof or the output or assertions in the       point of the arrow depending on the endpoint of the arrow.
functions it calls. Using CBMC, mark the key information
and remove the irrelevant information from these goto files
to obtain a new goto file that only contains dependency
information related to the proof framework. Finally, we ex-
tract the source code information corresponding to the key
information from the new goto file, including the proof of
the target function and all its related dependencies, forming a
dependency relationship. A dependency relationship refers to a
Rust element (such as a function, static variable, enumeration,
etc.) that requires another Rust element to function properly.
This relationship indicates that if the depended-upon element
changes, the elements that depend on it may also need to
change accordingly.                                                                     Fig. 2: Program Analysis
   The following Rust code snippet is an example of demon-
strating the function of each method.                                B. AST Analysis
1 struct Point {                                                        Upon receiving a file (or project) for verification, we also
2     x: i32,                                                        conduct code parsing on the source files, which is done
3     y: i32,
4}                                                                   concurrently with dependency analysis. We compile the source
5 impl Point {                                                       code and construct an abstract syntax tree (AST) at the same
6     fn distance(&self, other: &Point) -> i32                       time, traversing the AST to obtain the necessary structures and
              {                                                      data from the source code.
 7         let dx = self.x - other.x;                                   Specifically, we have defined an information collector
 8         let dy = self.y - other.y;
 9         (dx.abs() + dy.abs()).max(0)                              named CodeCollector, which traverses all files in the specified
10     }                                                             directory and filters out all Rust source files. For each Rust
11 }                                                                 source file, it reads the file content and uses the syn library
12 fn midpoint(p1: &Point, p2: &Point) -> Point                      to parse the content into an abstract syntax tree (AST). Addi-
         {                                                           tionally, CodeCollector implements the visit trait, enabling it
13      Point{x: (p1.x + p2.x) / 2, y: (p1.y +
            p2.y) / 2}                                               to customize the access and extraction of specific information
14 }                                                                 within the code. To be precise, it obtains basic information of
15 fn sum_of_coordinates(point: &Point) -> i32                       different types of Rust language elements from the AST, which
       {                                                             is the Node information. Node information includes the name,
16     point.x + point.y                                             type, starting line number, and ending line number, etc. The
17 }
18 fn main() {                                                       different types of Rust language elements include functions,
19     let p1 = Point{x: 1, y: 2};                                   static variables, enumerations, traits, and impl blocks, etc. All
20     let p2 = Point{x: 5, y: 2};                                   collected Node information is stored in the CodeCollector’s
information collector, forming a Rust element information            9         (dx.abs() + dy.abs()).max(0)
repository, namely the Span library. This plays a crucial role      10     }
in the subsequent code slicing process.                             11 }
                                                                    12 fn main() {
   When dealing with Rust’s lifetime and ownership issues,          13     let p1 = Point{x: 1, y: 2};
the Node information is utilized. Each Node information             14     let p2 = Point{x: 5, y: 2};
covers the entire scope of Rust elements, essentially ensuring      15     let dist = p1.distance(&p2);
the complete architecture of the dependent elements. In this        16     assert!(dist == 4);
way, semantic boundaries, operational logic, and resource           17 }
                                                                    18 #[kani::proof]
management are encapsulated within a closed context, thereby        19 fn verify_main(){
ensuring the correctness and reliability of the program. Thus,      20 }
the internal code logic is complete, including the entire process
of variable creation, usage, and destruction. At the same time,                 IV. EXPERIMENTAL EVALUATION
the paths of ownership transfer are not mistakenly truncated.
                                                                      Multiple experiments were conducted to evaluate the effi-
So it is unlikely to accidentally remove key variables and
                                                                    cacy of program slicing for Rust applications. This section
create or destroy code when extracting code snippets, which
                                                                    describes the experimental setup and experimental result.
can greatly reduce the risk of code violating ownership and
lifetime rules after slicing.                                       A. Experimental Setup
   As shown in Fig. 2, each yellow node is obtained through            The experimental setup includes the experimental environ-
the AST analysis, representing different types of items in          ment, the test set used, the slicing criteria and an explanation of
the Rust source code, including constants (Const), functions        the benchmarks for comparison. All experiments were done on
(Fn), structures (Struct), implementations (Impl), and asser-       a machine equipped with AMD Ryzen 8845H CPUs, operating
tions (assert) types, totaling 10 nodes. Each node contains         at 3.80 GHz, and configured with 32 GB of RAM. Each
corresponding information, including line number information,       experiment was constrained to utilize only a single core and 8
code structure type flags, source code paths, and other infor-      GB of memory.The software environment for the experiments
mation.                                                             is described in Table 1.
C. Slicing Implementation                                                   TABLE I: Experimental Software Environment
    In the slicing implementation phase, we first traverse and
filter the Span library within the organizational structure                       Software                 Version
information. According to specific sorting rules, we extract                       Ubuntu               22.04.4 LTS
the Nodes that match the dependency relationships from the                          Rust               1.70.0-nightly
                                                                                    Kani                   0.51.0
library and map the source code portions of these Nodes to                         CBMC       cbmc-5.95.1 (64-bit x86 64 linux)
a new file. Specifically, for each function Node, we deter-
mine whether its starting and ending line numbers include
the function line numbers collected in the dependency rela-            The test set for the experiments comprises four verification
tionships. If the condition is met, we selectively write the        projects extracted from actual operating system projects. All
function definitions into the new file. Similarly, we achieve       are from the task scheduling module: Project A selects the
the extraction and preservation of code snippets such as use        first ready thread from the thread queue to be the current
statements, structures, and so on.                                  thread. Project B executes the current thread and switches
    In Fig. 2 , the blue dashed line is the function implemented    between user mode and kernel mode. Project C performs
in this part. The ones that match successfully will appear above    cleanup operations based on the status of the thread that has
the blue dividing line, and then be sorted and reorganized; the     finished running. Project D is the main loop of the user-mode
nodes that do not match successfully, that is, those irrelevant     program. Each project has an average of 1,079 source lines of
codes, will be below the blue dividing line, ready to be            code (sloc). The largest project contains 1,543 sloc, while the
eliminated.                                                         smallest includes 222 sloc computed by VS Code Counter1 .
    Therefore, by inputting the example source code into Rust-         Our slicing criterion involves all statements under the
Pruner and proceeding through the aforementioned three steps,       #[kani::proof] attribute. This attribute marks functions as entry
the following sliced code is obtained.                              points for Kani to verification, indicating to the Kani that the
                                                                    specified function contains assertions for formal verification.
1 struct Point {                                                    When Kani is executed, it focuses specifically on these marked
2     x: i32,
                                                                    functions, attempting to formally verify that the assertions
3     y: i32,
4}                                                                  hold true under all possible inputs. Our slicing tool retains all
5 impl Point {                                                      statements dependent on these functions. Through algorithmic
6     fn distance(&self, other: &Point) -> i32                      processing tailored for Rust programs, it ensures that the sliced
              {
7            let dx = self.x - other.x;                               1 https://marketplace.visualstudio.com/items?itemName=uctakeoff.
8            let dy = self.y - other.y;                             vscode-counter
program remains executable and that the verification results are                 TABLE III: experimental statistics
consistent with the original program.                                  Proj.   Ver. Time     Src Size    Slice Size   Slice Time
   Prior to verifying Rust projects, we conducted a survey of
many static slicing tools. Within our current research scope, no        A       0.98 s        222 sloc   186 sloc     1.25 ms
                                                                        B       2.17 s       1013 sloc   761 sloc      7.89 ms
practical tools were found capable of slicing Rust programs             C       2.97 s       1543 sloc   978 sloc     11.26 ms
directly. Consequently, we compiled Rust into LLVM code                 D       3.67 s       1538 sloc   1316 sloc    24.96 ms
and tested a variety of tools that perform slicing on LLVM-IR
or LLVM-bitcode. These tools included LLVM-slicing [19],
LLVM-slicer2 , semslice [20], DG [21], and sbt-slicer3 . How-
ever, we discovered that existing LLVM-level slicing tools do
not support slicing of Rust programs effectively. Therefore, our
experiments primarily focus on evaluating the performance of
our tool rather than comparing it with other existing tools.
B. Experimental Result
   We conducted experiments on the aforementioned test set
by measuring the slicing time, verification time and the size of
the slice. All the algorithms and ideas described in this paper
have been implemented to ensure the feasibility of slicing Rust
programs and to maintain the executability and verifiability of
the programs after slicing.

                    TABLE II: Verification Results

      Project      Verification Consistency   Failures   Success   Fig. 3: Comparison of Size and Verification Time Before and
         A                     True              1         0                              After Slicing
         B                     True              0         3
         C                     True              0         1
         D                     True              0         1       Each project underwent a series of measurements that assessed
                                                                   slicing efficiency based on source size reduction before and
   After slicing, the projects maintain consistency with the       after slicing.
original projects in terms of verification attributes, as shown       During the course of the experiment, Proj. A demonstrated
in TABLE II . Project A has 1 failure, Project B has 3             the smallest reduction in source code size but was processed
successfully verified harnesses, and both Project C and Project    the fastest, indicating efficiency in handling smaller-scale
D have 1 successfully verified harness each. The summary           projects. In contrast, Proj. B, with a larger original source
of the experimental results is shown in TABLE III. The             size, showed significant reductions in source lines but required
descriptions for some columns in TABLE III are as follows:         longer processing times, reflecting the increased complexity
   • Ver. Time: Average verification time of the original          when dealing with large codebases.
     project                                                          Particularly, Proj. C and Proj. D, which started with larger
   • Src Size: Number of source lines of code in the original      source sizes, exhibited substantial reductions post-slicing, val-
     project                                                       idating the effectiveness of the slicing tool in handling larger
   • Slice Size: Number of source lines of code after project      projects. At the same time, the reduction in size and the
     slicing                                                       decrease in verification time after slicing may indicate a
   • Slice Time: Average slicing time for the project              positive correlation: that is, the reduction in project size helps
   The methodology adopted for measuring performance in-           to speed up the verification process.
cluded the following procedure: Each time measurement,                These findings demonstrate that the RustPruner tool has suc-
whether for project verification or a specific slice, was per-     cessfully extended the application of program slicing to Rust
formed 10 times. The initial iteration was always discarded        projects, ensuring, to some extent, that the slicing outcomes
to eliminate the effects of dynamically loading libraries into     are executable and that the verification results are consistent.
physical memory and data remaining in the disk cache. After                                V. R ELATED W ORK
each slicing or verification, the project’s object files were
                                                                      Program slicing can be categorized based on the consider-
cleared before conducting the experiment again.
                                                                   ation of specific inputs to the program into static slicing [5]
   TABLE III and Fig. 3 provide a comprehensive analysis of
                                                                   and dynamic slicing [22]. Static slicing [5] involves analysis
the slicing effects on various projects labeled A, B, C, and D.
                                                                   directly from the program’s source code, employing techniques
  2 https://github.com/jirislaby/LLVMSlicer                        such as data flow and control flow analysis to extract segments
  3 https://github.com/staticafi/sbt-slicer                        of code related to a particular point of interest. This approach
takes into account all possible executions of the program,                                          R EFERENCES
yielding a more comprehensive slicing result. In contrast,            [1] Silva and Josep, “A vocabulary of program slicing-based techniques,”
dynamic slicing [22] is conducted during the actual execution             ACM computing surveys, pp. 12(1–41), 2012.
of the program, where relevant code segments are extracted            [2] W. Crichton, G. Gray, and S. Krishnamurthi, “A grounded conceptual
                                                                          model for ownership types in rust,” Proceedings of the ACM on
based on the program’s execution path and state information.              Programming Languages, pp. 1224–1252, 2023.
Dynamic slicing is more readily implementable and tends to            [3] D. Blaser, “Simple explanation of complex lifetime errors in rust,” ETH
produce more precise slicing outcomes.                                    Zürich, 2019.
                                                                      [4] Y. Kashima, T. Ishio, and K. Inoue, “Comparison of backward slicing
   Program slicing is distinguished by the direction of analysis          techniques for java,” IEICE Trans. Inf. Syst., vol. 98, no. 1, pp. 119–130,
relative to a variable of interest, categorized into forward slic-        2015.
                                                                      [5] W. M., “Program slices : Formal, psychological, and practical inves-
ing [8] and backward slicing [9].Forward slicing [8] initiates            tigations of an automatic program abstraction method,” PhD thesis,
at a designated starting point, such as a specific variable or            University of Michigan, 1979.
statement, and proceeds in the direction of the program’s             [6] F. Allen, “Control flow analysis,” ACM SIGPLAN Notices, pp. 1–19,
                                                                          1970.
control and data flow to identify all code segments that could        [7] S. Liang and L. Larson, “Slicing objects using system dependence
potentially influence this point of origin. Conversely, backward          graphs,” pp. 358–367, November 1998.
slicing [9] commences at a specified endpoint, like a particular      [8] K. Awad, M. Abdallah, A. Tamimi, A. Ngah, and H. Tamimi, “A
                                                                          proposed forward clause slicing application,” Indonesian Journal of
output or error, and retraces the control and data flow pathways          Electrical Engineering and Computer Science, pp. 1–6, 2019.
to extract code segments that may have an impact on this              [9] B. Alokush, M. Abdallah, and M. Alrifaee, “A proposed java static
terminal point.                                                           slicing approach,” Indonesian Journal of Electrical Engineering and
                                                                          Computer Science, pp. 308–317, 2018.
   Program slicing can be differentiated by the analytical tech-     [10] X. Zhaogui, Q. Ju, C. Lin, C. Zhifei, and X. Baowen, “Static slicing
niques and methodologies employed, which include Weiser’s                 for python first-class objects,” 13th International Conference on Quality
                                                                          Software, pp. 117–124, 2013.
original slicing method [5], methods based on program infor-         [11] B. Korel and J. Laski, “Dynamic slicing of computer programs,” Journal
mation flow relationships [23], and graph reachability-based              of Systems and Software, pp. 187–195, 1990.
slicing methods [24]. Weiser’s original slicing method [5]           [12] The crate syn. https://crates.io/crates/syn. Accessed: 2024-05-11.
                                                                     [13] A. VanHattum, D. Schwartz-Narbonne, N. Chong, and A. Sampson,
centers on scrutinizing the trajectory of data within a program           “Verifying dynamic trait objects in rust,” in ICSE-SEIP ’22: Proceedings
and ascertaining the statements that exert influence over the             of the 44th International Conference on Software Engineering: Software
data’s values. Methods based on program information flow                  Engineering in Practice, 2022.
                                                                     [14] Z. Li, J. Wang, M. Sun, and J. C. Lui, “Mirchecker: Detecting bugs in
relationships [23] concentrate on the interdependencies among             rust programs via static analysis,” in CCS ’21: Proceedings of the 2021
program statements, employing a syntax-directed, bottom-                  ACM SIGSAC Conference on Computer and Communications Security,
up methodology to compute these dependencies. Conversely,                 2021.
                                                                     [15] D. Kröning and M. Tautschnig, “CBMC: The c bounded model checker,”
graph reachability-based slicing methods [24] spotlight the               Proc. TACAS, pp. 389–391, 2014.
dependencies and reachability among program statements. By           [16] T. T., R. M., and S. Z., “Finding missed optimizations through the lens
fabricating distinct dependency graphs, which encapsulate a               of dead code elimination,” International Conference on Architectural
                                                                          Support for Programming Languages and Operating Systems - ASPLOS,
variety of relational contexts, a spectrum of slicing outcomes            pp. 697–709, 2022.
can be realized.                                                     [17] P. Zhao and J. Amaral, “Function outlining and partial inlining,” in
                                                                          17th International Symposium on Computer Architecture and High
   Program slicing methodologies are classified into the Pro-             Performance Computing, 2005.
gram Dependence Graph (PDG) [25] and the System Depen-               [18] J.-D. Choi and J. Ferrante, “Static slicing in the presence of goto state-
dence Graph (SDG) [26] based on their scope of analysis. PDG              ments,” ACM Transactions on Programming Languages and Systems,
                                                                          vol. 16, no. 4, pp. 1097–1113, 1994.
[25] is a graphical representation of a program that captures        [19] Y.-Z. Zhang, “Sympas: Symbolic program slicing,” J. Comput. Sci.
control and data dependencies, serving as a foundation for                Technol., p. 397–418, apr 2021.
intraprocedural slicing by enabling the precise extraction of        [20] B. Beckert, T. Bormer, S. Gocht, M. Herda, D. Lentzsch, and M. Ulbrich,
                                                                          “Semslice: Exploiting relational verification for automatic program
code segments related to specific program points. Building                slicing,” in Integrated Formal Methods. 13th International Conference,
upon this, the SDG [26] extends the scope to interprocedural              IFM, 2017.
slicing by incorporating dependencies across multiple proce-         [21] M. Chalupa, “Dg: Analysis and slicing of llvm bitcode,” in Auto-
                                                                          mated Technology for Verification and Analysis, ser. LNCS, vol. 12302.
dures, thus accounting for the broader context of a system’s              Springer, 2020.
behavior.                                                            [22] B. Korel and J. Laski, “Dynamic slicing of computer programs,” Journal
                                                                          of Systems and Software, pp. 187–195, 1990.
   Our methodology adeptly applies the graph reachability            [23] J.-F. Bergeretti and B. Carré, “Information-flow and data-flow analysis
approach through the utilization of PDG, conducting a rigorous            of while-programs,” ACM Transactions on Programming Languages and
intraprocedural analysis. We introduce a novel custom visitor             Systems (TOPLAS), pp. 37–61, 1985.
                                                                     [24] X. Qi and B. Xu, “An approach to slicing concurrent ada programs based
for traversing AST, which efficiently identifies and collects             on program reachability graphs,” International Journal of Computer
critical code elements. By focusing on backward, static slic-             Science and Network Security, pp. 29–37, 2006.
ing and capitalizing on the strengths of graph reachability,         [25] K. Ottenstein and L. Ottenstein, “The program dependence graph in a
                                                                          software development environment,” ACM SIGPLAN Notices, pp. 177–
our research effectively surpasses the limitations of current             184, 1984.
methods. RustPruner’s providing a refined and effective slicing      [26] S. Horwitz and T. Reps, “Interprocedural slicing using dependence
technique that bolsters the analytical capabilities of software           graphs,” ACM Transactions on Programming Languages and Systems
                                                                          (TOPLAS), pp. 26–60, 1990.
engineering practitioners and researchers alike.
