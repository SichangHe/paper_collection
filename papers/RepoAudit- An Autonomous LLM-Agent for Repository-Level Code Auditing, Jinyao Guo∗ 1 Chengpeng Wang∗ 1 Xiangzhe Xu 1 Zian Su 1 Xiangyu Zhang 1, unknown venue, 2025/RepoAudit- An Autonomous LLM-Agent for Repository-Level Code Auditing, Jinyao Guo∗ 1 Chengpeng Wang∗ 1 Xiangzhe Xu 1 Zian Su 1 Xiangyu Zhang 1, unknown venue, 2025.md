                                         R EPOAUDIT: An Autonomous LLM-Agent for Repository-Level Code Auditing


                                                            Jinyao Guo∗ 1 Chengpeng Wang∗ 1 Xiangzhe Xu 1 Zian Su 1 Xiangyu Zhang 1


                                                                   Abstract                                      LLM-powered IDE plugins, such as Copilot, enable agile
                                                                                                                 code generation by facilitating flexible interactions with
                                              Code auditing is the process of reviewing code                     LLMs (Barke et al., 2023). However, in the era of LLMs,
                                              with the aim of identifying bugs. Large Language                   auditing the rapidly expanding codebase presents a more
arXiv:2501.18160v3 [cs.SE] 29 May 2025




                                              Models (LLMs) have demonstrated promising ca-                      formidable challenge than writing code. Traditional pro-
                                              pabilities for this task without requiring compi-                  gram analysis techniques, such as dynamic and static analy-
                                              lation, while also supporting user-friendly cus-                   sis, focus primarily on observing runtime behaviors or sym-
                                              tomization. However, auditing a code repository                    bolically reasoning about intermediate code generated dur-
                                              with LLMs poses significant challenges: limited                    ing compilation (King, 1976; Cadar et al., 2008; Calcagno
                                              context windows and hallucinations can degrade                     et al., 2009; Sui and Xue, 2016; Shi et al., 2018a). Un-
                                              the quality of bug reports, and analyzing large-                   fortunately, software systems are often non-executable and
                                              scale repositories incurs substantial time and to-                 even uncompilable during the human-LLM collaborative
                                              ken costs, hindering efficiency and scalability.                   development phase. Moreover, existing analysis techniques
                                              This work introduces an LLM-based agent, R E -                     demand substantial expertise, such as a deep understanding
                                              POAUDIT , designed to perform autonomous                           of compiler internals (Zhang et al., 2024; Zhou et al., 2024).
                                              repository-level code auditing. Equipped with                      Therefore, current program analysis approaches often fall
                                              agent memory, R EPOAUDIT explores the code-                        short in meeting the practical requirements of code auditing
                                              base on demand by analyzing data-flow facts                        in real-world contexts (Johnson et al., 2013).
                                              along feasible program paths within individual
                                                                                                                 In recent years, extensive research has focused on leverag-
                                              functions. It further incorporates a validator mod-
                                                                                                                 ing LLMs for code auditing via prompt engineering (Fang
                                              ule to mitigate hallucinations by verifying data-
                                                                                                                 et al., 2024; Hao et al., 2023; Ding et al., 2024). Unlike
                                              flow facts and checking the satisfiability of path
                                                                                                                 traditional analysis techniques, LLM-driven code auditing
                                              conditions associated with potential bugs, thereby
                                                                                                                 directly analyzes source code without program compilation
                                              reducing false positives. R EPOAUDIT detects 40
                                                                                                                 or execution. By describing analysis requirements through
                                              true bugs across 15 real-world benchmark projects
                                                                                                                 natural language and few-shot examples in prompts, the cus-
                                              with a precision of 78.43%, requiring on aver-
                                                                                                                 tomization of analysis is also significantly simplified. How-
                                              age only 0.44 hours and $2.54 per project.Also,
                                                                                                                 ever, many existing LLM-driven code auditing techniques
                                              it detects 185 new bugs in high-profile projects,
                                                                                                                 are largely restricted to small-scale codebases, such as smart
                                              among which 174 have been confirmed or fixed.
                                                                                                                 contracts (Sun et al., 2024; Zhang and Zhang, 2024), and
                                              We have open-sourced R EPOAUDIT at https:
                                                                                                                 lack the capability to support repository-level code auditing
                                              //github.com/PurCL/RepoAudit.
                                                                                                                 in complex, real-world scenarios.
                                                                                                                 Direct Prompting Hardly Works. A straightforward solu-
                                         1. Introduction                                                         tion is to break down a repository into smaller pieces and
                                                                                                                 prompt the model with individual pieces. This approach
                                         The rapid innovation of large language models (LLMs) has                often falls short for non-local bugs, which may require rea-
                                         remarkably enhanced the productivity of software develop-               soning across a large number of interconnected code snip-
                                         ers (Wang et al., 2021; Rozière et al., 2023; Guo et al., 2024).       pets spanning multiple functions, classes, and files. Even
                                            *                                                                    with significant future advancements in model reasoning
                                              Equal contribution 1 Department of Computer Science, Pur-
                                         due University, West Lafayette, IN, USA. Correspondence                 capacity, the fundamental differences between programs
                                         to: Jinyao Guo <guo846@purdue.edu>, Chengpeng Wang                      and natural language texts for which transformer models
                                         <wang6590@purdue.edu>.                                                  were designed make LLMs insufficient for comprehensive
                                                                                                                 repository analysis. In particular, a code repository can be
                                         Proceedings of the 42 nd International Conference on Machine            conceptualized as an enormous graph, with nodes repre-
                                         Learning, Vancouver, Canada. PMLR 267, 2025. Copyright 2025
                                         by the author(s).                                                       senting individual statements and edges capturing intricate

                                                                                                             1
relationships such as control flow, data flow, and other in-           when scanning for null pointer dereference bugs. Second,
terdependencies between statements. These relationships                the explorer traverses the relevant functions on demand.
are precisely defined and immensely complex at the reposi-             Similar to how human auditors analyze code function by
tory level. For instance, the number of data-flow edges in             function, the explorer starts by querying the LLMs with the
the project shadowsocks-libev exceeds one million,                     functions containing these starting points. Instead of ex-
significantly surpassing the complexity of the implicit graph-         plicitly and programmatically enumerating individual paths
ical structure present in any LLM’s pre-training data sample.          inside a function, as in traditional compiler-based automated
Such distribution differences render direct prompting inef-            scanners, the explorer leverages LLMs’ inherent ability to
fective as shown by our experiments in Section 2.2.                    implicitly distinguish relevant paths from irrelevant ones
                                                                       and only reasons about the former. If invocations to other
In addition, detecting many types of bugs requires reasoning
                                                                       functions and returns within a function are considered rele-
about properties along specific program paths. For instance,
                                                                       vant after analyzing paths within the function—for instance,
a memory leak occurs when allocated memory is not freed
                                                                       when null pointer values propagate through these function
along some program path. Detecting such so-called path-
                                                                       boundaries—the system synthesizes follow-up prompts to
sensitive bugs (Shi et al., 2018a) necessitates unfolding the
                                                                       extend the scanning into callee or caller functions as needed.
program’s graph structure into individual paths and ana-
                                                                       Third, R EPOAUDIT checks the output of the explorer before
lyzing these paths one by one. However, this leads to the
                                                                       storing it in the agent memory and also examines the bug
well-known path explosion problem, as the number of paths
                                                                       report candidates by examining the path conditions of the
grows exponentially with the number of statements. Hence,
                                                                       buggy program paths. This validation design can signifi-
direct prompting is akin to presenting a large project on an
                                                                       cantly improve the precision of R EPOAUDIT.
enormous screen and expecting a human auditor to identify
bugs along complex and lengthy paths solely by reading and             We implement R EPOAUDIT powered with Claude 3.5 Son-
interpreting the code—a task highly unlikely to succeed.               net and test it on three typical bug types of memory con-
                                                                       curruption. We first evaluate R EPOAUDIT upon fifteen real-
Human Auditing. In practice, human auditors do not op-
                                                                       world projects used in existing studies, with an average
erate in such a manner. As revealed by existing cognitive
                                                                       size of 251 KLoC. It is shown that R EPOAUDIT effectively
science literature (Anicic et al., 2012), humans are highly
                                                                       reproduces 21 previously reported bugs and uncovers 19
effective at reasoning about events that occur in order, e.g.,
                                                                       newly discovered bugs, 14 of which have already been fixed
in temporal or spatial order. Human auditors hence tend to
                                                                       in the latest commit, achieving a precision of 78.43%. In
explore complex graphical structures in code by following
                                                                       contrast, the industrial static bug detector Amazon C ODE -
paths that denote the execution order. To avoid excessive
                                                                       G URU reports 18 false positives (FPs) with no true positives
exploration, they traverse only a subset of paths most rele-
                                                                       (TPs), while Meta I NFER also only reports seven TPs along
vant to the targeted property, leveraging implicit abstraction
                                                                       with two FPs. Besides, R EPOAUDIT exhibits high efficiency
to preclude irrelevant paths. An example of detecting null
                                                                       and incurs low token costs, averaging 0.44 hours and $2.54
pointer dereference can be found in Section 2.1.
                                                                       per project. Powered by Deepseek R1, Claude 3.7 Sonnet,
Our Solution. It is widely believed that LLMs operate sim-             and OpenAI o3-mini, it achieves the precision of 88.46%,
ilarly to humans but with significantly greater “endurance”            86.79%, and 82.35%, respectively. To demonstrate its real-
and access to a broader spectrum of knowledge (Li et al.,              world impact, we further scan ten actively maintained repos-
2023; Long et al., 2024; Qian et al., 2024). Building on               itories and detect 185 new bugs in two months, 95 and
this perspective, we propose a novel LLM-based repository              79 of which have been confirmed and fixed by developers,
auditing agent, named R EPOAUDIT, inspired by human au-                respectively. Notably, R EPOAUDIT facilitates development-
diting practices. R EPOAUDIT addresses the fundamental                 time code auditing, which cannot be supported by Meta
misalignment between LLMs’ tendency to reason sequen-                  I NFER and other compilation-dependent bug detectors. To
tially and the inherently complex graphical structures of soft-        the best of our knowledge, R EPOAUDIT is the first purely
ware repositories through path-sensitive and demand-driven             LLM-driven code auditor for real-world code repositories.
graph traversal. By leveraging LLMs’ abstraction capabil-
ities, R EPOAUDIT mitigates path explosion by excluding                2. Preliminaries
irrelevant code regions and sub-paths. Also, it minimizes
inherent hallucinations by sanitizing final outputs through            In this section, we first discuss the essence of repository-
the validation of several well-formed properties.                      level code auditing. Next, we illustrate the limitations of
                                                                       the LLMs in this task. Finally, we highlight several intrinsic
More specifically, the agent R EPOAUDIT consists of three
                                                                       strengths of LLMs in tackling primitive tasks that can be
components, including the initiator, the explorer, and the
                                                                       leveraged to build our repository-level auditing tool.
validator. First, the initiator identifies starting points based
on the properties under investigation, such as NULL values

                                                                   2
    google/protobuf/descriptor.c                 google/protobuf/descriptor.c            src/sofa/pbrpc/pbjson.cc

  1. bool is_optional(u32 member_offset) {…}   1. bool is_repeated() const {…}
                                                                                        1. Value* field2json(FieldDescriptor *field, Value* default){
                                                                                        2.   ...
    src/sofa/pbrpc/pbjson.cc                                                            3.   bool repeated = field->is_repeated();
                                                                                        4.   Value* json = NULL;①
   1. Value* parse_msg(const Message *msg, Value::AllocatorType& allocator){            5.   if (repeated) {
   2.   ...                                                                             6.     json = new Value(kArrayType);
   3.   for (size_t i = 0; i != count; ++i){                                            7.   }
   4.     ...                                                                           8.   switch (field->cpp_type()){
   5.     if (field->is_optional()){...}                                                9. ② case CPPTYPE_DOUBLE:
   6.     else {                    ③                                                  10.     ...
   7.       Value* field_json = field2json(msg, field, allocator) ;                    11.     default: break;
   8.       root->AddMember(name, *field_json, allocator);                             12.   }
   9.       ...                                                                        13.   if (!repeated || field->value.GetType() != kArrayType)
  10.     }                   ④             Null Pointer Dereference                   14.     return json;
  11.   }                                                                              15.   return default;
  12.   return root;                                                                   16. }
  13. }


       1. bool is_optional(u32 capacity) {…}
      src/rapidjson/document.h                                                       src/rapidjson/document.h

  1. AddMember(Ch* name, GenericValue& value, Allocator& allocator) {…}            1. Type GetType(){ return static_cast<Type>(flags_ & kTypeMask); }


Figure 1. A simplified code snippet from the project sofa-pbrpc contains a real NPD bug found by R EPOAUDIT. The blue dashed
arrows indicate the edges in the call graph. The red solid arrows show the data-flow facts indicating the null value propagation. The call
graph of the project contains 1,508 nodes and 6,196 edges, while its data dependence graph contains 160,875 nodes and 360,096 edges.
2.1. Auditing Entails Path-Sensitive Reasoning on                               ing the data-flow fact NULL@s4 ,→ json@s4 , which is
     Complex Graphs                                                             labeled with 1 in Figure 1. When repeated is false, the
                                                                                value of json at line 4 propagates to the return statement
While several bug types, such as API misuse (Li et al., 2021),
                                                                                at line 14. This data-flow fact, denoted by json@s4 ,→
require only localized reasoning upon abstract syntax trees
                                                                                json@s14 , is labeled with 2 . Subsequently, in the func-
(ASTs) and are relatively easy to detect with highly effec-
                                                                                tion parse_msg, the return value of field2json is as-
tive scanners, many critical bug types demand modeling the
                                                                                signed to the pointer field_json at line 7 and further
entire project as a massive graph and reasoning about prop-
                                                                                dereferenced at line 8 of the function parse_msg, which
erties along and across individual paths in that graph. For
                                                                                eventually causes an NPD bug.
example, detecting Null Pointer Dereference (NPD) bugs
relies on constructing and analyzing a specialized graph                        Furthermore, we study the 2024 CWE Top 25 Most Dan-
structure called the data dependence graph (DDG) (Fer-                          gerous Software Weaknesses, a curated list of the most
rante et al., 1984), where the nodes represent statements,                      critical and prevalent vulnerabilities underlying the 31,770
and the edges indicate data-flow facts between different pro-                   Common Vulnerabilities and Exposures (CVE) records re-
gram values at specific statements. Specifically, a data-flow                   ported in 2024. Our investigation reveals that 19 out of
fact exists from the variable u at the statement sta to the                     the 25 weakness (76%) categories necessitate global, path-
variable v at the statement stb , denoted as u@sta ,→ v@stb ,                   sensitive reasoning of source-sink reachability upon call
if the value of the variable u at the statement sta may affect                  graphs, DDGs, and control-flow graphs (CFGs), whereas
the value of the variable v at the statement stb following                      only 6 categories can be effectively identified through local-
some program path. A program path is a sequence of state-                       ized analysis based on ASTs.
ments that follow the execution order. Also, it is feasible if
there exists an input that satisfies all the conditional checks                 2.2. LLMs’ Inadequacy
along the path. Hence, a data-flow fact can occur between
two statements that are far apart, such as when a global                        According to (Rozière et al., 2023; OpenAI, 2023), many
variable is read and written across different directories.                      foundation models are initially pre-trained on relatively
                                                                                short text or code snippets. For long contexts, models
Determining whether a data-flow fact may hold in the pro-                       like DeepSeek-V3 (Liu et al., 2024), Llama3 series (Dubey
gram requires collecting feasible program paths and analyz-                     et al., 2024), and QWen2.5-Coder (Hui et al., 2024) typically
ing data-flow facts along them. Consider the detection of                       adopt NTK-aware length interpolation such as YaRN (Peng
Null Pointer Dereference (NPD) as an example. Given the                         et al., 2024) to progressively extend context window from
DDG, the code auditor ought to find a chain of data-flow                        the initial 4K/8K to 128K tokens. Although these models
facts leading from a null value (as a source value) to a deref-                 perform well in “Needle in a Haystack” (Kamradt, 2023)
erenced pointer (as a sink value) along a feasible program                      evaluation, the task is intended for RAG-and does not align
path. In Figure 1, for instance, the function field2json                        well with the path-sensitive program understanding ability
initializes a null value at the line 4 of the function, induc-                  needed in our application.


                                                                          3
       Please analyze the function field2json in Figure 1.                What are the points-to facts of the variable json at
       We only care about the statements that affect the                  line 8 in the function field2json shown in Figure 1?
 propagation of the NULL value at line 3. Please simplify the
 function field2json for program abstraction.                           The pointer variable json is initialized to NULL value
                                                                        at line 4 and then points to the newly allocated memory at
                                                                   line 6 if repeated is true. Hence, we have:
        Here is the program after abstraction.                     (1) repeated = true: The pointer variable json points to the
                                                                      object allocated at line 6;
   1. Value* field2json(FieldDescriptor *field,                    (2) repeated = false: the pointer variable json is NULL
                        Value* default){
   2.   bool repeated = field->is_repeated();                                           (b) An example of pointer handling
   3.   Value* json = NULL;
   4.   if (repeated) {                                                   Collect the feasible program paths from the function
   5.      json = new Value(rapidjson::kArrayType);                       field2json in Figure 1.
   6.   }
   7.   if (!repeated || field->value.GetType() != kArrayType)            The branch conditions at lines 5 and 13 contradict.
   8.     return json;                                                    Feasible path 1: Lines 1-5, 8-12, 13-14
   9. }                                                                   Feasible path 2: Lines 1-5, 8-12, 13, 15
                                                                          Feasible path 3: Lines 1-7, 8-12, 13-14

                (a) An example of program abstraction                              (c) An example of feasible program path exploration
                                    Figure 2. Three examples of showing intrinsic strengths of LLMs
To validate our speculation, we conducted a controlled ex-             in the program and focuses on key statements such as null
periment where we prompt Claude 3.5 Sonnet with all the                pointer assignments, value propagations, conditional checks
five functions shown in Figure 1 to identify the NPD bug,              guarding the propagations, and cross-function propagations
following a methodology similar to a recent study (Fang                (e.g., passing the pointer to a callee function via a parameter,
et al., 2024). This is a controlled experiment because, in             returning it to a caller function, or writing it to a global vari-
practice, we cannot guarantee knowledge of the compre-                 able). In a preliminary experiment shown in Figure 2(a), for
hensive set of functions associated with a bug. The model              example, we feed the function field2json in Figure 1
exhibited substantial hallucinations, reporting that almost            to Claude 3.5 Sonnet and ask it to abstract the program. Ob-
all the dereferenced pointers have null values. Even if we             serve that the program returned by the LLM only contains
improve the prompts by offering several few-shot examples              critical statements relating to the null value propagation,
and explanations on how a null pointer dereference bug oc-             while irrelevant ones are removed, such as the switch state-
curs, the model still hallucinates, producing false positives          ment from line 8 to line 12 in the function field2json
and incorrect explanations. More numerical results can be              in Figure 1. Notably, human auditors often perform such
found in Appendix A.                                                   abstraction implicitly, enabling them to analyze complex
                                                                       code without the excessive path exploration that hampers
2.3. Intrinsic Strengths of LLMs                                       classic tools like symbolic execution (Cadar et al., 2008)
                                                                       and software model checking (Clarke, 1997).
On the bright side, we observe that LLMs can effectively
perform basic analyses when the scope is limited. This ca-             2.3.2. P OINTER H ANDLING
pability enables us to surpass traditional program analysis
methods, which require compilation and struggle to scale ef-           Pointer variables in C and reference variables in Java may
ficiently. Specifically, we identify several primitive abilities       point to different memory objects depending on their run-
critical for auditing: program abstraction, pointer handling,          time values. Consequently, reads and writes via pointer
and feasible program path exploration. While traditional au-           dereferences create data-flow facts that dynamically vary
diting tools rely on heavy-weight yet rigorous techniques to           based on pointer values. Determining the set of memory
achieve these capabilities, skilled human auditors often rely          objects a pointer variable may point to is known as points-to
on intuition to handle such challenges within a constrained            analysis (Smaragdakis et al., 2015), one of the most chal-
analysis scope. We observe similar traits in LLMs.                     lenging problems for downstream static analysis, such as
                                                                       DDG construction. Traditional points-to analysis techniques
2.3.1. P ROGRAM A BSTRACTION                                           often rely on conservative and relational methods, which
                                                                       tend to significantly over-approximate the set of possible
Abstraction is essential for scalability in program analy-             memory objects, complicating downstream analysis tasks.
sis. Given a property, a set of initial program points, and            In contrast, human auditors can often intuitively and ac-
a defined scope (e.g., a function), abstraction identifies the         curately determine the points-to facts of a specific pointer
subset of statements relevant to the property within the               variable through their understanding of program semantics.
scope. These statements form a self-contained, smaller pro-            Advanced LLMs exhibit similar capabilities, particularly
gram, significantly reducing the number of paths to analyze.           within the scope of individual functions. As shown in Fig-
For instance, in the NPD detection (as illustrated in Sec-             ure 2(b), for example, we prompt Claude 3.5 Sonnet with the
tion 2.1), abstraction targets how null values are propagated          function field2json in Figure 1 and query the points-to

                                                                   4
                                                  Initiator       Parser    LLM


                            Bug                                                         Validator       Bug Reports
                  Program Definition


                                                  Explorer             Memory

                                            Figure 3. The architecture of R EPOAUDIT
facts of the return value of the function. The model accu-            sponses for each function, and a dedicated agent memory
rately identifies the two possible points-to facts within the         ensures that analysis results across functions are seamlessly
function. It even identifies the path constraints that make           shared. To achieve cost-effective and path-sensitive analysis
the corresponding points-to facts hold. In contrast, the sym-         at the function level, R EPOAUDIT leverages LLMs’ intrin-
bolic static analyzer SVF (Sui and Xue, 2016) computes the            sic capabilities by providing explicit prompts for program
points-to facts without path conditions by default due to its         abstraction, pointer handling, and feasible program path
inherent limitations in semantic analysis.                            exploration, fully capitalizing on the model’s strengths.
                                                                      Figure 3 depicts the architecture of our agent. The initia-
2.3.3. F EASIBLE P ROGRAM PATH E XPLORATION
                                                                      tor tool ( 1 ) takes a specified bug definition and the target
A bug report is often considered valid only if it provides            repository as inputs, identifying the source values for anal-
a feasible program path (from the root cause to the symp-             ysis, such as the null values for the NPD detection. Each
tom) as evidence. To determine feasibility, traditional tools         source value triggers a scanning procedure. The explorer
rely on modeling conditional checks along a path as sym-              tool ( 2 ) conducts iterative, demand-driven exploration of
bolic constraints (e.g., in the form of first-order logic for-        the repository by prompting the model to analyze one func-
mulas) and querying a theorem prover (e.g., SMT solver                tion at a time. The results of each analysis are stored in
Z3 (de Moura and Bjørner, 2008)) to check if an input can             the agent memory, guiding further exploration. The anal-
satisfy the constraints. This process is computationally ex-          ysis prompts are dynamically generated for each function,
pensive and prone to failure, as converting program paths             providing detailed instructions for abstraction tailored to
to logic formulas requires exploring an explosively large             the specific function and adjusted based on the results of
number of program paths and modeling a wide range of                  prior analyses. While the agent may still hallucinate in the
program behaviors that lack direct representation in logi-            analysis of single functions and produce false positive bug
cal term, such as loops, array indexing, aliasing, pointer            reports, a set of validator tools ( 3 ) verify the result of the
arithmetic, and unbounded string operations. In contrast, hu-         explorer from multiple perspectives, including the validity
mans, as well as the LLMs, rely on abstraction and intuitive          of the control flow order and the satisfiability of the path
logical reasoning to assess feasibility, which is highly effec-       conditions across functions.
tive within a limited scope. In Figure 2(c), we demonstrate
an example of feasible program path exploration upon the              3.1. Initiator
function field2json using Claude 3.5 Sonnet. Observe
that the model can skip the irrelevant statements, such as            The initiator identifies the starting points of scanning (i.e.,
the switch statement, avoiding exploring a huge number of             the sources). In our implementation, we employ the
program paths. It also discovers the contradiction between            tree-sitter parsing library to create a suite of tailored
the branch conditions at lines 5 and 13, which refutes pro-           pattern matchers for the sources of the bug types supported
gram paths covering both lines 6 and 14, thereby reporting            by R EPOAUDIT. These matchers are concise, often con-
the three feasible program paths in Figure 2(c).                      sisting of just a few lines of code, and require a one-time
                                                                      implementation effort. Alternatively, recent advancements
                                                                      offer a promising avenue of synthesizing such matchers
3. R EPOAUDIT                                                         using LLMs (Wang et al., 2024a).
Building on the findings of the previous section, the core
design rationale of R EPOAUDIT is as follows: Since LLMs              3.2. Explorer
struggle to reason about path-sensitive properties in large-          For each source value identified by the initiator, the explorer
scale program graphs, R EPOAUDIT employs an agent-                    conducts a round of scanning over the repository. During
centric approach to navigate these graphs externally, prompt-         each round, the explorer traverses a subset of functions on
ing the model with one unit (e.g., a function) at a time. This        demand, beginning with the identified sources. It queries the
demand-driven navigation adapts based on the model’s re-              LLM to analyze one function at a time, storing the results


                                                                  5
 Task: Determine data-flow facts starting from a given value along            Agent Memory. After analyzing a function, the explorer
 different program paths in a single function.                                obtains a set of data-flow facts for each feasible program
 Hints: You can collect the feasible program paths into 3 steps:              path and stores them into the memory of the agent. Specif-
 (1) Identify the aliased pointers in the program.
 (2) Extract the critical statements relating to the value propagation,       ically, the agent memory is a function M relating to the
 like function call statements, return statements, and assignments.           function f and a program value v@s. Each element in
 (3) Collect the feasible program paths covering critical statements.         M(f, v@s) is a pair of a program path and a set of data-
 For each feasible program path, simulate the program execution and           flow facts. After analyzing the function field2json and
 determine the data-flow facts starting from the given value.
 Examples: Here are several examples.
                                                                              the null value at the line 4, for instance, the memory maps
 Example 1: User: [Program] [Question]                                        (field2json, NULL@s4 ) as follows:
 System: <Path information: Lines 4-7, 11> <Explanation>
                                                                                                         
                                                                                M field2json, NULL@s4
 <Data-flow facts: 𝑝𝑡𝑟@ℓ! ↪ 𝑞𝑡𝑟@ℓ" , 𝑝𝑡𝑟@ℓ! ↪ 𝑟𝑡𝑟@ℓ## >                        n                                                
 [Other examples]                                                             = p1 , {NULL@s4 ,→ json@s4 , json@s4 ,→ json@s14 } ,
 Question: Given [FUNCTION], what are the data-flow facts from                                              
 [VAL_NAME] at line [VAL_LINE] along different program paths?                    p2 , {NULL@s4 ,→ json@s4 } ,
                                                                                                            o
Figure 4. The prompt template for analyzing individual functions                 p3 , {NULL@s4 ,→ json@s4 }

in the agent memory. The explorer performs several actions,
                                                                              3.2.2. S ELECTING F UNCTIONS FOR E XPLORATION
each guided by corresponding prompts. These actions in-
clude: analyzing individual functions, selecting functions                    After analyzing a function, if the targeted program value
for exploration, and generating bug report candidates. We                     propagates across function boundaries, the explorer queries
will introduce the details of the three actions as follows.                   the underlying call graph to identify the relevant functions
                                                                              for further exploration. This follow-up exploration is guided
3.2.1. A NALYZING I NDIVIDUAL F UNCTIONS                                      by the program values escaping the current function bound-
                                                                              aries. For example, in Figure 1, the null value at the line 4
As discussed in Section 2.1, scanning for most bug types
                                                                              of field2json is propagated to the return value. Hence,
can be reduced to traversing a limited set of graphs, such
                                                                              in the next step, the explorer analyzes the caller function
as the DDG and the CFG. This enables the use of general
                                                                              of field2json, i.e., parse msg, and examines how the
analysis prompts for these graph types, eliminating the need
                                                                              return value is propagated.
for bug-specific prompts. Moreover, instead of explicitly
enumerating and analyzing individual paths, we leverage the                   Note that if the program value does not escape, the analysis
intrinsic capabilities of LLMs to distinguish paths and per-                  does not lead to the explorations of other functions. For
form path-sensitive reasoning. The key of this approach lies                  example, if we consider the second and third program paths,
in pointer handling and program abstraction demonstrated                      i.e., p2 and p3 in the example shown in Section 3.2.1, the
in Section 2.3.2 and Section 2.3.1, respectively, which im-                   value of json at the line 4 of the function field2json
plicitly reduces the function to a significantly smaller code                 does not propagate. Hence, the explorer does not enter any
snippet with far fewer paths. This can eventually facilitate                  other functions. Furthermore, we leverage the existing data-
the efficient exploration of feasible program paths demon-                    flow facts stored in the memory as caches to avoid redundant
strated in Section 2.3.3. We design the prompt template                       analysis. Specifically, before analyzing the propagation of
used for analyzing individual functions in Figure 4. After                    a specific program value in a function, the explorer first
describing the task at the beginning, we offer the three-step                 checks the agent memory and determines whether this has
hints to the LLM, enforcing the LLM to unleash its power                      been done before. In our evaluation, we will quantify how
step-by-step in pointer handling, abstraction, and feasible                   the caching strategy reduces computational costs.
program path exploration. By offering several few-shot ex-
amples, we pose the question at the end and ask the LLM to                    3.2.3. G ENERATING B UG R EPORT C ANDIDATES
identify the data-flow facts starting from the initial value(s)
                                                                              After analyzing a function, the explorer evaluates whether
of interest along different feasible program paths.
                                                                              any new bug candidates can be identified. Consider the NPD
Consider the function filed2json and the initial null                         detection as an example. The explorer examines whether
value at the line 4 as an example. Utilizing the instrinsic                   it identifies any new data-flow facts reaching a sink value,
strengths of LLMs, R EPOAUDIT collects three feasible pro-                    i.e., a dereferenced pointer. If so, a bug report is generated
gram paths shown in Figure 2(c). By simulating the program                    by assembling the complete trail of data-flow facts across
execution along the first program path, denoted by p1 , the                   functions along with the corresponding inter-procedural
LLM identifies the data-flow facts NULL@s4 ,→ json@s4                         program path. For example, the explorer enters the func-
and json@s4 ,→ json@s14 . For the second and third pro-                       tion parse msg and examines how the return value of
gram paths, denoted by p2 and p3 , the LLM only identifies                    field2json propagates. Based on the two discovered
the data-flow fact NULL@s4 ,→ json@s4 .                                       data-flow facts labeled as 3 and 4 in Figure 1, the explorer

                                                                          6
 Task: Determine whether a given path is feasible or not.                                Table 1. The statistics of evaluation subjects
 Hint: If branch conditions conflict or variable values contradict the        Bug Type     ID    Repository Name             Size (LoC)   Stars
 required conditions, the path is infeasible.                                              N1    sofa-pbrpc                    40,723      2.1K
 Examples: Here are several examples.                                                      N2    ImageMagick/MagickCore       242,555     12.6K
 Example 1: User: [Program] [Question]                                          NPD        N3    coturn/src/server              8,976     11.7K
 System: <Explanation> <Answer: Yes or No>                                                 N4    libfreenect                   37,582      3.6K
 [Other examples]                                                                          N5    openldap                     442,955      486
 Question: Given the functions [FUNCTION], is the following                                M1    libsass                       40,934      4.3K
 program path feasible? [PATH]                                                             M2    memcached                     14,654     13.7K
                                                                                MLK        M3    linux/driver/net             914,025     186K
    Figure 5. The prompt template for feasibility validation                               M4    linux/sound                 1,378,262    186K
                                                                                           M5    linux/mm                     171,721     186K
reaches a sink value, i.e., the dereferenced pointer at line                               U1    Redis                        179,723     67.7K
8. Hence, the explorer identifies a potential bug and report                               U2    linux/drivers/peci             2,130     186K
                                                                                UAF        U3    shadowsocks-libev             71,080     186K
it by concatenation the data-flow facts 1 , 2 , 3 , and 4 .                                U4    wabt-tool                      3,214       7K
For several bug types, such as MLK, the explorer reports a                                 U5    icu/icu4c/source/i18n        220,359      2.9K
potential bug if it fails to reach any sink point along feasible
                                                                             common practice in evaluating reasoning tasks (Ye et al.,
paths, e.g., the argument of free function.
                                                                             2023), we set the temperature to 0.0 to reduce the random-
                                                                             ness. Similar to existing code auditing works (Heo et al.,
3.3. Validator
                                                                             2017), we introduce an upper bound K on the calling con-
To improve the quality of bug reports, we introduce two                      text and set it to 4, i.e., R EPOAUDIT investigates data-flow
kinds of validation mechanism for the explorer.                              facts across a maximum of four functions.
Alignment Validation of Data-flow Facts and Control                          4.1. Bug Types and Dataset
Flow. When dealing with complex code, the LLM may
hallucinate and incorrectly infer a data-flow fact u@s1 ,→                   We focus on three bug types, namely NPD, MLK, and UAF,
v@s2 along some program path p that violates the control-                    which are among the CWE Top 25 most dangerous weak-
flow order. Specifically, this implies that a statement s2 must              nesses. Our evaluation first aims to reproduce bugs reported
appear after another statement s1 in the program path p, yet                 in previous works. Specifically, we investigate recent works
the model concludes that a variable defined at s2 can be                     in the venues of computer security and software engineering
used by s1 . To detect such misalignments, a parsing-based                   and collect the bug reports published by the authors (Huang
analyzer is employed to verify the control-flow order. Only                  et al., 2024; Shi et al., 2021; 2018b). Also, we attempt to
the data-flow facts that conform to the control-flow order                   detect new bugs within the targeted code repositories. As
will be stored in the agent memory.                                          shown by Table 1, we choose five well-maintained projects
                                                                             for each bug type from the bug reports of previous works,
Path Feasibility Validation. While path feasibility within                   which mostly have thousands of stars on GitHub with 251
individual functions is inherently checked by the explorer,                  KLoC and thousands of functions on average.
contradictions can arise in conditional checks across func-
tions, resulting in infeasible inter-procedural program paths.               4.2. Evaluation Results
Recall that each bug report is the concatenation of multiple
                                                                             Main Result. As shown in Table 2, R EPOAUDIT success-
data-flow facts, such as 1 , 2 , 3 , and 4 in Figure 1. The
                                                                             fully detects all the previously reported bugs, and mean-
data-flow facts in different functions may hold under the
                                                                             while, reports 19 new bugs in historic versions, 14 of which
specific conditions along the corresponding program paths.
                                                                             have already been fixed in the latest commit. In total, it re-
A bug report candidate is valid only if the path conditions in
                                                                             ports 40 TPs and 11 FPs, resulting in a precision of 78.43%.
different functions do not contradict, implying their logical
                                                                             Notably, 21 TPs are inter-procedural bugs. R EPOAUDIT
conjunction satisfiable. To check the validity, we prompt
                                                                             also demonstrates both efficiency and cost-effectiveness.
the LLM with the inter-procedural path and task it with
                                                                             On average, it takes only 0.44 hours (i.e., 1,577.22 secs)
identifying any contradictions in the path conditions. If a
                                                                             to analyze a project, completing the code auditing within
contradiction is found, the bug report is discarded. The
                                                                             100.67 prompting rounds. The average cost per project audit
prompt template is shown in Figure 5.
                                                                             is $2.54, with each true bug detection costing $0.95. Hence,
                                                                             R EPOAUDIT can effectively detect the bugs upon real-world
4. Evaluation                                                                programs with low time cost and financial cost.
We utilize the tree-sitter parsing library to provide                        Comparison with LLM-driven Bug Detectors. We com-
a set of primitive tools for R EPOAUDIT, e.g., call graph                    pare R EPOAUDIT with two kinds of LLM-driven tech-
constructor and control flow order validator. We select LLM                  niques, namely end-to-end few-shot CoT prompting-based
Claude 3.5 Sonnet to power R EPOAUDIT. Following the                         approaches (Chen et al., 2023; Ding et al., 2024) and agent-

                                                                         7
Table 2. The statistics of R EPOAUDIT powered by Claude 3.5 Sonnet. The column “Old” denotes the bugs reported by existing works. A
pair (m, n) in the column New indicates m new bugs detected in the versions used by existing works, n of which still exist in the latest
versions. The columns “Intra” and “Inter” show the numbers of intra-procedural and inter-procedural bugs, respectively.
                                   TP                  Feature                         # Tokens
         Bug Type     ID                     FP                     # Prompts                           Financial ($)   Time (s)
                             Old     New          # Intra # Inter                  Input      Output
                      N1      1      (3,3)   2       0         4      145         709,919      55,863       2.97         2026.13
                      N2      7      (1,0)   0       4         4       17         97,717       8,518        0.42          283.84
           NPD        N3      1      (1,0)   3       1         1      109         599,674      52,936       2.59         1747.90
                      N4      1      (0,0)   1       0         1       29         126,852      13,654       0.59          435.09
                      N5      1      (5,4)   1       0         6       63         420,710      31,375       1.73         1059.57
                      M1      1      (2,1)   1       2         1      205        1,132,763     85,279       4.68         2,917.91
                      M2      1      (6,6)   2       4         3      146         845,148      71,243       3.60         2282.31
           MLK        M3      1      (0,0)   0       1         0        2         10,481       1,019        0.05          34.34
                      M4      1      (0,0)   0       1         0        1           5691        619         0.03          17.94
                      M5      1      (0,0)   0       1         0       35         181,348      20,779       0.86          599.92
                      U1      1      (0,0)   0       1         0       36         179,939      17,547       0.80          582.23
                      U2      1      (0,0)   0       1         0        2           8900        869         0.04          31.95
           UAF        U3      1      (0,0)   0       1         0       48         317,713      23,067       1.30          791.98
                      U4      1      (0,0)   0       1         0       10         48,087       5,883        0.23          185.22
                      U5      1      (1,0)   1       1         1      662        4,534,444    303,645      18.15        10,661.98
            Average                                                  100.67     614,625.73 46,153.07        2.54         1,577.22

Table 3. The statistics of Meta I NFER and Amazon C ODE G URU             true bugs and two false positives. Amazon C ODE G URU sup-
       Bug Type     ID     Build
                                      I NFER      C ODE G URU             ports the detection of NPD and UAF bugs, while it reports
                                    TP     FP     TP      FP              18 false positives with no true positives. Compared with
                    N1      ✗       N/A N/A        0       0
                    N2      ✓        1      0      0       0              Meta I NFER, R EPOAUDIT obtains comparable precision
         NPD        N3      ✓       N/A N/A        0       0              while detecting more true bugs. More detailed illustrations
                    N4      ✓        5      0      0       2              on the comparison results are provided in Appendix B.
                    N5      ✓        1      2      0       3
                    M1      ✓        0      0                             Ablation Study. We introduce three ablation variants of
                    M2      ✓        0      0                             R EPOAUDIT, without abstraction, without validators, and
         MLK        M3      ✓       N/A N/A       N/A   N/A
                    M4      ✓        0      0                             without caching. We observe that without abstraction, the
                    M5      ✓       N/A N/A                               number of TPs is decreased by 47.50% and the number
                    U1      ✓       N/A N/A        0      0               of FPs is increased by 181.82%. Without validators, the
                    U2      ✓       N/A N/A        0      0               number of FPs increases by 245.45%. Without caching, the
         UAF        U3      ✗       N/A N/A        0      0
                    U4      ✓        0      0      0      0               costs become 3-4 times higher on average, and in the worst
                    U5      ✓        0      0      0     13               case, 30 times higher. Details can be found in Appendix C.
            Total                    7      2      0     18
                                                                          Different Model Choices and Temperature Settings.
centric approaches (Wang et al., 2024a; Li et al., 2024a;b).              We also evaluate R EPOAUDIT with Deepseek R1, Claude
It is shown that CoT prompting can only detect one true                   3.7 Sonnet, and OpenAI o3-mini, achieving precisions of
bug in the single function-level bug detection and 10 true                88.46%, 86.79%, and 82.35%, respectively. In addition, we
bugs in the multiple-level bug detection when analyzing the               assess R EPOAUDIT powered by Claude 3.5 Sonnet under
functions relating to the true bugs detected by R EPOAUDIT.               the temperatures of 0.25, 0.5, 0.75, and 1.0, achieving con-
For the agent-centric solution LLMDFA, the numbers of its                 sistently high precision (≥ 72.92%) and recall (≥ 85.71%).
prompting rounds and token costs are 165.23 and 123.18                    More details are provided in Appendix D and Appendix E.
times with the ones of R EPOAUDIT on average when it ana-                 Real-World Impact. We further scan nine open-source
lyzes relevant functions relating to the buggy program paths,             GitHub projects spanning diverse domains and sizes rang-
showing its high computation costs in analyzing real-world                ing from 14K to 1.7M LoC. On average, they have 420K
programs. More details can be found in Appendix A.                        LoC and 8.8K GitHub stars, reflecting their complexity and
Comparison with Industrial Tools. We compare R EPOAU -                    popularity. Table 4 shows the detailed statistics. Specifically,
DIT with two representative industrial tools, namely Meta                 the columns TP and FP show the numbers of TPs and FPs
I NFER (Meta, 2025) and Amazon C ODE G URU (Amazon,                       reported by R EPOAUDIT, respectively, while the columns
2025). As shown in Table 3, two projects (labeled by ✗) can-              Con and Fix denotes the numbers of confirmed bugs and
not be successfully built in our environment. Another five                fixed bugs, respectively. Overall, R EPOAUDIT detects 185
projects (labeled with NA) cannot be handled by I NFER due                true bugs with the precision of 85.71%. Notably, 95 and 79
to incompatibilities, a prominent limitation of build/compi-              bugs confirmed and fixed by developers, respectively.
lation dependent tools. In total, Meta I NFER reports seven

                                                                      8
                                Table 4. The statistics of R EPOAUDIT in nine additional real-world projects
                                                               NPD                     MLK                   UAF
                 Project         Size (LoC)   Stars
                                                      TP    FP Con       Fix   TP   FP Con     Fix   TP   FP Con    Fix
              clickhouse-odbc      209,197     258     0     0     0      0     2    0    0     2     0    1    0    0
                     htop          35,910      6.9K    1     3     0      1     0    2    0     0     0    0    0    0
              TrinityEmulator     1,767,100    292     2     2     0      2     4    0    0     4     0    0    0    0
                   rtl 433         66,253      6.5K    0     0     0      0     1    1    0     1     0    0    0    0
                      frr         1,050,020    3.6K    4     5     4      0     0    1    0     0     0    0    0    0
                    libuv          80,360      25K     86    2    84      2     1    2    0     1     0    0    0    0
                  openldap         442,955     486     8     2     0      8     0    0    0     0     3    0    0    0
                    nginx          505,513    26.4K    5     2     0      0     0    0    0     0     0    0    0    0
                 memcached         14,654     13.7K    1     3     1      0    67    4    6    58     0    0    0    0
                    Total                             107   19    89     13    76   10    6    66     3    2    0    0


4.3. Limitations and Future Works                                        context for the buggy functions, thereby degrading the va-
                                                                         lidity of such function-level code auditing techniques (Risse
Apart from the false positives and negatives caused by LLM
                                                                         and Böhme, 2024). As for repository-level code auditing,
hallucinations, R EPOAUDIT faces several limitations. First,
                                                                         existing techniques can generally be categorized into two
the analysis overhead of R EPOAUDIT is highly sensitive
                                                                         groups. The first group harnesses LLMs to provide special-
to the number of source elements within a repository. In
                                                                         ized pre-knowledge to symbolic code analyzers or examine
cases where a large number of sources exist, the tool may
                                                                         initial bug reports, while the main body of the code base is
incur substantial time and token costs. Second, R EPOAUDIT
                                                                         scanned by conventional symbolic analyzers (Wang et al.,
is not sound in detecting inter-procedural data-flow facts,
                                                                         2024b; Li et al., 2024b;a). Typically, IRIS employs LLMs to
as it currently limits flow analysis to a maximum of four
                                                                         pinpoint sensitive values within programs (Li et al., 2024b),
functions. This constraint may cause it to miss complex bugs
                                                                         aiding traditional analyzers like C ODE QL (Avgustinov et al.,
involving longer call chains. To address these limitations,
                                                                         2016) in taint-style bug detection. However, due to the com-
we outline several directions for future improvement:
                                                                         pilation reliance on symbolic analysis, these techniques lack
Enhancing Model Reasoning Capabilities: We can im-                       the capacity for IDE-time analysis. The second category
prove the LLM’s ability to reason by either adopting more                utilizes LLMs as code interpreters, extracting semantic prop-
advanced models or fine-tuning the current models for                    erties via prompt engineering (Fang et al., 2024; Wang et al.,
specific tasks. Fine-tuning can be tailored to particular                2024c;a; Sun et al., 2024). Typically, LLMDFA (Wang
sub-tasks like exploring feasible program paths in single                et al., 2024a) and LLMSAN (Wang et al., 2024c) incorpo-
functions. Additionally, incorporating specialized training              rate few-shot CoT prompting to discover data-flow paths for
datasets focused on programming languages, debugging,                    bug detection. R EPOAUDIT belongs to the latter category.
and code analysis could further enhance the model’s accu-                Unlike LLMDFA, R EPOAUDIT adopts a demand-driven
racy in these contexts.                                                  strategy for codebase exploration, which avoids exhaustive
                                                                         data-flow summary generation for all functions, thereby
Expanding the Tool Suite for Better Retrieval: Develop-
                                                                         enhancing analysis scalability. Additionally, R EPOAUDIT
ing a more comprehensive tool suite that facilitates the re-
                                                                         outperforms LLMSAN in terms of recall by employing
trieval across the entire codebase is crucial. A significant en-
                                                                         individual function analysis instead of repository-level end-
hancement would involve integrating existing compilation-
                                                                         to-end prompting, effectively mitigating hallucinations in
free analysis tools to identify all potential branches and
                                                                         the overall analysis.
loops within a program. This integration would offer a
clearer representation of the program’s control flow struc-
ture to the model. Such an improved RAG design has the                   6. Conclusion
potential to significantly reduce the false positives and false
                                                                         This paper introduces R EPOAUDIT, an autonomous LLM-
negatives produced by RepoAudit.
                                                                         agent that facilitates precise and efficient repository-level
                                                                         code auditing. By mimicking manual code auditing, R E -
5. Related Work                                                          POAUDIT leverages the intrinsic strength of the LLM, such
                                                                         as program abstraction, and conducts the path-sensitive rea-
A considerable volume of literature has focused on utilizing
                                                                         soning. Powered by Claude-3.5-Sonnet, it detects 40 true
LLMs for code auditing (Zheng et al., 2025; Zheng et al.; Li
                                                                         bugs in 15 real-world benchmark projects, achieving the pre-
et al., 2024b;a; Wang et al., 2024a). In recent years, various
                                                                         cision of 78.43% and reproducing all the bugs discovered by
benchmarks like BigVul (Fan et al., 2020), PrimeVul (Ding
                                                                         existing techniques. It also detects 185 previously unknown
et al., 2024), and DiverseVul (Chen et al., 2023) have been
                                                                         bugs in nine high-profile open-source projects, 174 of which
established. Nevertheless, these benchmarks lack calling
                                                                         have been confirmed or fixed by developers.

                                                                     9
Acknowledgement                                                       Third, classical code auditing requires reasoning about the
                                                                      semantics of IRs and reimplementing the same algorithm
We are grateful to the Center for AI Safety for provid-               for different languages. In contrast, LLMs serve as general
ing computational resources. This work was funded in                  code interpreters and have exceptional performance in un-
part by the National Science Foundation (NSF) Awards                  derstanding short code snippets, no matter which program-
SHF-1901242, SHF-1910300, Proto-OKN 2333736, IIS-                     ming languages are used. By following similar prompting
2416835, DARPA VSPELLS - HR001120S0058, ONR                           strategies, we can easily extend R EPOAUDIT to analyze
N00014-23-1-2081, and Amazon. Any opinions, findings                  programs in other languages, including but not limited to
and conclusions or recommendations expressed in this ma-              C/C++, Python, and JavaScript.
terial are those of the authors and do not necessarily reflect
the views of the sponsors.
                                                                      References
Impact Statement                                                      Yue Wang, Weishi Wang, Shafiq R. Joty, and Steven
                                                                        C. H. Hoi. CodeT5: Identifier-aware unified pre-trained
This paper presents work whose goal is to advance the                   encoder-decoder models for code understanding and gen-
field of Machine Learning, targeting a complicated code-                eration. In Marie-Francine Moens, Xuanjing Huang, Lu-
reasoning task, namely repo-level code auditing. We demon-              cia Specia, and Scott Wen-tau Yih, editors, Proceedings
strate the limitations of our work above. We do not expect              of the 2021 Conference on Empirical Methods in Natu-
our work to have a negative broader impact, though lever-               ral Language Processing, EMNLP 2021, Virtual Event /
aging LLMs for repo-level code auditing may come with                   Punta Cana, Dominican Republic, 7-11 November, 2021,
certain risks, e.g., the leakage of source code in private or-          pages 8696–8708. Association for Computational Lin-
ganizations and potential high token costs. Meanwhile, it               guistics, 2021. doi: 10.18653/V1/2021.EMNLP-MAIN.
is worth more discussions to highlight that our work has                685.
the potential to dramatically change the field of software
engineering with the power of LLMs. Specifically, LLM-                Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten
powered code auditing not only enables the analysis of                  Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu
incomplete programs with little customization but addresses             Liu, Tal Remez, Jérémy Rapin, Artyom Kozhevnikov,
other challenges in the code auditing.                                  Ivan Evtimov, Joanna Bitton, Manish Bhatt, Cristian
                                                                        Canton-Ferrer, Aaron Grattafiori, Wenhan Xiong, Alexan-
First, classical code auditors primarily rely on specific ver-
                                                                        dre Défossez, Jade Copet, Faisal Azhar, Hugo Tou-
sions of intermediate representations (IRs) generated by
                                                                        vron, Louis Martin, Nicolas Usunier, Thomas Scialom,
compilation infrastructures. As compilation infrastructures
                                                                        and Gabriel Synnaeve. Code llama: Open foundation
evolve, IR formats often change across compiler versions,
                                                                        models for code. CoRR, abs/2308.12950, 2023. doi:
necessitating continuous adaptation of the analysis imple-
                                                                        10.48550/ARXIV.2308.12950.
mentation. For instance, the Clang compiler has experienced
ten major version updates over the past decade, each intro-           Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong,
ducing variations in the generated IR. These differences                Wentao Zhang, Guanting Chen, Xiao Bi, Yu Wu, YK Li,
require substantial manual effort to migrate and maintain               et al. Deepseek-coder: When the large language model
compatibility with newer IRs. In contrast, LLM-powered                  meets programming–the rise of code intelligence. arXiv
code auditing operates directly on source code, inherently              preprint arXiv:2401.14196, 2024.
supporting multiple language standards and eliminating the
dependency on compiler-specific IRs.                                  Shraddha Barke, Michael B James, and Nadia Polikarpova.
                                                                        Grounded copilot: How programmers interact with code-
Second, classical code auditing heavily relies on various ab-           generating models. Proceedings of the ACM on Program-
straction designs, particularly in pointer analysis, which              ming Languages, 7(OOPSLA1):85–111, 2023.
serves as a foundational pre-analysis step. Developers
must carefully select and implement specific analysis strate-         James C. King. Symbolic execution and program testing.
gies—such as Andersen-style or Steensgaard’s pointer anal-              Commun. ACM, 19(7):385–394, 1976. doi: 10.1145/
ysis—each involving distinct trade-offs in precision and                360248.360252.
scalability. This process requires substantial implementa-
tion effort and domain expertise. In contrast, LLMs, which            Cristian Cadar, Daniel Dunbar, and Dawson R. Engler.
are inherently aligned with program semantics, can interpret            KLEE: unassisted and automatic generation of high-
code behavior directly. As a result, they obviate the need              coverage tests for complex systems programs. In Richard
for manually crafting abstractions or implementing analysis             Draves and Robbert van Renesse, editors, 8th USENIX
algorithms tailored to particular precision levels.                     Symposium on Operating Systems Design and Implemen-
                                                                        tation, OSDI 2008, December 8-10, 2008, San Diego,

                                                                 10
  California, USA, Proceedings, pages 209–224. USENIX                 Chongzhou Fang, Ning Miao, Shaurya Srivastav, Jialin Liu,
  Association, 2008.                                                    Ruoyu Zhang, Ruijie Fang, Ryan Tsang, Najmeh Nazari,
                                                                        Han Wang, Houman Homayoun, et al. Large language
Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn,
                                                                        models for code analysis: Do {LLMs} really do their
  and Hongseok Yang. Compositional shape analysis
                                                                        job? In 33rd USENIX Security Symposium (USENIX
  by means of bi-abduction. In Zhong Shao and Ben-
                                                                        Security 24), pages 829–846, 2024.
  jamin C. Pierce, editors, Proceedings of the 36th ACM
  SIGPLAN-SIGACT Symposium on Principles of Program-                  Yu Hao, Weiteng Chen, Ziqiao Zhou, and Weidong Cui.
  ming Languages, POPL 2009, Savannah, GA, USA, Jan-                    E&v: Prompting large language models to perform is by
  uary 21-23, 2009, pages 289–300. ACM, 2009. doi:                      pseudo-code execution and verification. arXiv preprint
  10.1145/1480881.1480917.                                              arXiv:2312.08477, 2023.
Yulei Sui and Jingling Xue. SVF: interprocedural static               Yangruibo Ding, Yanjun Fu, Omniyyah Ibrahim, Chawin
  value-flow analysis in LLVM. In Ayal Zaks and Manuel V.               Sitawarin, Xinyun Chen, Basel Alomair, David Wagner,
  Hermenegildo, editors, Proceedings of the 25th Interna-               Baishakhi Ray, and Yizheng Chen. Vulnerability detec-
  tional Conference on Compiler Construction, CC 2016,                  tion with code language models: How far are we? arXiv
  Barcelona, Spain, March 12-18, 2016, pages 265–266.                   preprint arXiv:2403.18624, 2024.
  ACM, 2016. doi: 10.1145/2892208.2892235.
                                                                      Yuqiang Sun, Daoyuan Wu, Yue Xue, Han Liu, Haijun
Qingkai Shi, Xiao Xiao, Rongxin Wu, Jinguo Zhou, Gang
                                                                        Wang, Zhengzi Xu, Xiaofei Xie, and Yang Liu. Gptscan:
  Fan, and Charles Zhang. Pinpoint: Fast and precise sparse
                                                                        Detecting logic vulnerabilities in smart contracts by com-
  value flow analysis for million lines of code. In Jeffrey S.
                                                                        bining gpt with program analysis. In Proceedings of the
  Foster and Dan Grossman, editors, Proceedings of the
                                                                        IEEE/ACM 46th International Conference on Software
  39th ACM SIGPLAN Conference on Programming Lan-
                                                                        Engineering, pages 1–13, 2024.
  guage Design and Implementation, PLDI 2018, Philadel-
  phia, PA, USA, June 18-22, 2018, pages 693–706. ACM,                Brian Zhang and Zhuo Zhang. Detecting bugs with sub-
  2018a. doi: 10.1145/3192366.3192418.                                  stantial monetary consequences by llm and rule-based
Bowen Zhang, Wei Chen, Peisen Yao, Chengpeng Wang,                      reasoning. In The Thirty-eighth Annual Conference on
  Wensheng Tang, and Charles Zhang. SIRO: empower-                      Neural Information Processing Systems, 2024.
  ing version compatibility in intermediate representations           Darko Anicic, Sebastian Rudolph, Paul Fodor, and Nenad
  via program synthesis. In Rajiv Gupta, Nael B. Abu-                   Stojanovic. Real-time complex event recognition and
  Ghazaleh, Madan Musuvathi, and Dan Tsafrir, editors,                  reasoning–a logic programming approach. Applied Artifi-
  Proceedings of the 29th ACM International Conference                  cial Intelligence, 26(1-2):6–57, 2012.
  on Architectural Support for Programming Languages
  and Operating Systems, Volume 3, ASPLOS 2024, La                    Guohao Li, Hasan Hammoud, Hani Itani, Dmitrii
  Jolla, CA, USA, 27 April 2024- 1 May 2024, pages 882–                 Khizbullin, and Bernard Ghanem. Camel: Commu-
  899. ACM, 2024. doi: 10.1145/3620666.3651366.                         nicative agents for” mind” exploration of large language
                                                                        model society. Advances in Neural Information Process-
Anshunkang Zhou, Chengfeng Ye, Heqing Huang, Yuandao
                                                                        ing Systems, 36:51991–52008, 2023.
  Cai, and Charles Zhang. Plankton: Reconciling binary
  code and debug information. In Rajiv Gupta, Nael B. Abu-            Xinwei Long, Jiali Zeng, Fandong Meng, Zhiyuan Ma,
  Ghazaleh, Madan Musuvathi, and Dan Tsafrir, editors,                  Kaiyan Zhang, Bowen Zhou, and Jie Zhou. Genera-
  Proceedings of the 29th ACM International Conference                  tive multi-modal knowledge retrieval with large language
  on Architectural Support for Programming Languages                    models. In Proceedings of the AAAI Conference on Artifi-
  and Operating Systems, Volume 2, ASPLOS 2024, La                      cial Intelligence, volume 38, pages 18733–18741, 2024.
  Jolla, CA, USA, 27 April 2024- 1 May 2024, pages 912–
  928. ACM, 2024. doi: 10.1145/3620665.3640382.                       Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan
                                                                        Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng
Brittany Johnson, Yoonki Song, Emerson R. Murphy-Hill,                  Su, Xin Cong, et al. Chatdev: Communicative agents for
  and Robert W. Bowdidge. Why don’t software devel-                     software development. In Proceedings of the 62nd Annual
  opers use static analysis tools to find bugs? In David                Meeting of the Association for Computational Linguistics
  Notkin, Betty H. C. Cheng, and Klaus Pohl, editors,                  (Volume 1: Long Papers), pages 15174–15186, 2024.
  35th International Conference on Software Engineering,
  ICSE ’13, San Francisco, CA, USA, May 18-26, 2013,                  Ziyang Li, Aravind Machiry, Binghong Chen, Mayur Naik,
  pages 672–681. IEEE Computer Society, 2013. doi:                      Ke Wang, and Le Song. ARBITRAR: user-guided API
  10.1109/ICSE.2013.6606613.                                            misuse detection. In 42nd IEEE Symposium on Security

                                                                 11
  and Privacy, SP 2021, San Francisco, CA, USA, 24-27             Chengpeng Wang, Wuqi Zhang, Zian Su, Xiangzhe Xu,
  May 2021, pages 1400–1415. IEEE, 2021. doi: 10.1109/              Xiaoheng Xie, and Xiangyu Zhang. LLMDFA: Analyzing
  SP40001.2021.00090.                                               dataflow in code with large language models. In The
                                                                    Thirty-eighth Annual Conference on Neural Information
Jeanne Ferrante, Karl J Ottenstein, and Joe D Warren. The           Processing Systems, 2024a.
  program dependence graph and its use in optimization.
  In International Symposium on Programming, pages 125–           Xi Ye, Qiaochu Chen, Isil Dillig, and Greg Durrett. SatLM:
  132. Springer, 1984.                                              Satisfiability-aided language models using declarative
                                                                    prompting. In Alice Oh, Tristan Naumann, Amir Glober-
OpenAI. GPT-4 technical report. CoRR, abs/2303.08774,               son, Kate Saenko, Moritz Hardt, and Sergey Levine, edi-
  2023. doi: 10.48550/ARXIV.2303.08774.                             tors, Advances in Neural Information Processing Systems
                                                                    36: Annual Conference on Neural Information Process-
Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao                ing Systems 2023, NeurIPS 2023, New Orleans, LA, USA,
  Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng,                     December 10 - 16, 2023, 2023.
  Chenyu Zhang, Chong Ruan, et al. Deepseek-v3 technical
  report. arXiv preprint arXiv:2412.19437, 2024.                  Kihong Heo, Hakjoo Oh, and Kwangkeun Yi. Machine-
                                                                    learning-guided selectively unsound static analysis. In
Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Ab-                2017 IEEE/ACM 39th International Conference on Soft-
  hishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil               ware Engineering (ICSE), pages 519–529. IEEE, 2017.
  Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The
                                                                  Jianjun Huang, Jianglei Nie, Yuanjun Gong, Wei You, Bin
  llama 3 herd of models. arXiv preprint arXiv:2407.21783,
                                                                     Liang, and Pan Bian. Raisin: Identifying rare sensi-
  2024.
                                                                     tive functions for bug detection. In Proceedings of the
Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng               IEEE/ACM 46th International Conference on Software
  Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu,                Engineering, pages 1–12, 2024.
  Keming Lu, et al. Qwen2.5-coder technical report. arXiv         Qingkai Shi, Peisen Yao, Rongxin Wu, and Charles Zhang.
  preprint arXiv:2409.12186, 2024.                                  Path-sensitive sparse analysis without path conditions. In
                                                                    Proceedings of the 42nd ACM SIGPLAN International
Bowen Peng, Jeffrey Quesnelle, Honglu Fan, and Enrico               Conference on Programming Language Design and Im-
  Shippole. Yarn: Efficient context window extension of             plementation, pages 930–943, 2021.
  large language models. In The Twelfth International
  Conference on Learning Representations, 2024.                   Qingkai Shi, Xiao Xiao, Rongxin Wu, Jinguo Zhou, Gang
                                                                    Fan, and Charles Zhang. Pinpoint: Fast and precise sparse
Greg Kamradt. Needle in a haystack - pressure test-                 value flow analysis for million lines of code. In Pro-
  ing LLMs, 2023. URL https://github.com/                           ceedings of the 39th ACM SIGPLAN Conference on Pro-
  gkamradt/LLMTest_NeedleInAHaystack.                               gramming Language Design and Implementation, pages
                                                                    693–706, 2018b.
Edmund M Clarke. Model checking. In Foundations of
  Software Technology and Theoretical Computer Science:           Yizheng Chen, Zhoujie Ding, Lamya Alowain, Xinyun
  17th Conference Kharagpur, India, December 18–20,                 Chen, and David Wagner. Diversevul: A new vulner-
  1997 Proceedings 17, pages 54–56. Springer, 1997.                 able source code dataset for deep learning based vulner-
                                                                    ability detection. RAID ’23, page 654–668, New York,
Yannis Smaragdakis, George Balatsouras, et al. Pointer              NY, USA, 2023. Association for Computing Machinery.
  analysis. Foundations and Trends® in Programming                  ISBN 9798400707650. doi: 10.1145/3607199.3607242.
  Languages, 2(1):1–69, 2015.
                                                                  Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian. En-
Leonardo Mendonça de Moura and Nikolaj Bjørner. Z3:                hancing static analysis for practical bug detection: An
  an efficient SMT solver. In C. R. Ramakrishnan and                llm-integrated approach. Proc. ACM Program. Lang., 8
  Jakob Rehof, editors, Tools and Algorithms for the Con-           (OOPSLA1):474–499, 2024a. doi: 10.1145/3649828.
  struction and Analysis of Systems, 14th International           Ziyang Li, Saikat Dutta, and Mayur Naik. LLM-assisted
  Conference, TACAS 2008, Held as Part of the Joint Eu-             static analysis for detecting security vulnerabilities.
  ropean Conferences on Theory and Practice of Software,            CoRR, abs/2405.17238, 2024b. doi: 10.48550/ARXIV.
  ETAPS 2008, Budapest, Hungary, March 29-April 6,                  2405.17238.
  2008. Proceedings, volume 4963 of Lecture Notes in
  Computer Science, pages 337–340. Springer, 2008. doi:           Meta. Infer Static Analyzer. https://fbinfer.com/,
  10.1007/978-3-540-78800-3\ 24.                                   2025. [Online; accessed 29-Jan-2025].

                                                             12
Amazon. Code Review Tool: Amazon CodeGuru Se-                                                         NPD        MLK         UAF
                                                                                      25
 curity. https://aws.amazon.com/codeguru/,
 2025. [Online; accessed 29-Jan-2025].                                                20

Mingwei Zheng, Danning Xie, and Xiangyu Zhang.                                        15




                                                                         Bug Number
 Large language models for validating network proto-                                  10
 col parsers, 2025. URL https://arxiv.org/abs/
 2504.13515.                                                                           5

                                                                                       0
Mingwei Zheng, Danning Xie, Qingkai Shi, Chengpeng                                         Single-function   Multiple-function     RepoAudit
 Wang, and Xiangyu Zhang. Validating network protocol
 parsers with traceable rfc document interpretation. In               Figure 6. The comparison results with single-function level and
                                                                      multiple-function level bug detectors
 Proceedings of the 34th ACM SIGSOFT International
 Symposium on Software Testing and Analysis, ISSTA                    bug detection is widely adopted and evaluated by many re-
 2025.                                                                cent studies (Chen et al., 2023; Ding et al., 2024). These
Jiahao Fan, Yi Li, Shaohua Wang, and Tien N Nguyen. A                 techniques are applicable for models with a limited context
   C/C++ code vulnerability dataset with code changes and             length. To compare with single-function level bug detection,
   cve summaries. In Proceedings of the 17th International            we collect all the functions that contain the sink values yield-
   Conference on Mining Software Repositories, pages 508–             ing TPs to the LLM along with few-shot examples, asking
   512, 2020.                                                         the LLM to determine whether the function can introduce
                                                                      specific types of bugs. Second, multiple-function level bug
Niklas Risse and Marcel Böhme. Top score on the wrong                detectors attempt to feed the whole program to the LLM
  exam: On benchmarking in machine learning for vul-                  so that the calling contexts of buggy functions can be in-
  nerability detection. arXiv preprint arXiv:2408.12986,              cluded (Wang et al., 2024c). Unfortunately, the huge size
  2024.                                                               of a real-world software system often makes the prompts
Chengpeng Wang, Jipeng Zhang, Rongxin Wu, and Charles                 exceed the context limit of LLM. Hence, we only feed the
  Zhang. DAInfer: Inferring API aliasing specifications               relevant functions covered by the buggy program paths to
  from library documentation via neurosymbolic optimiza-              the LLM in our evaluation.
  tion. Proc. ACM Softw. Eng., 1(FSE):2469–2492, 2024b.               Among agent-centric approaches (Wang et al., 2024a; Li
  doi: 10.1145/3660816.                                               et al., 2024a;b), we select LLMDFA (Wang et al., 2024a) as
                                                                      a baseline for comparison, as it supports compilation-free
Pavel Avgustinov, Oege de Moor, Michael Peyton Jones, and
                                                                      and customizable analysis. Since LLMDFA cannot support
  Max Schäfer. QL: object-oriented queries on relational
                                                                      the MLK detection, we focus our comparison between R E -
  data. In Shriram Krishnamurthi and Benjamin S. Lerner,
                                                                      POAUDIT and LLMDFA specifically on NPD and UAF bugs.
  editors, 30th European Conference on Object-Oriented
                                                                      LLMDFA works by summarizing all data-flow facts for each
  Programming, ECOOP 2016, July 18-22, 2016, Rome,
                                                                      function and then correlating these facts. Its overall compu-
  Italy, volume 56 of LIPIcs, pages 2:1–2:25. Schloss
                                                                      tational costs—time and token costs—can be substantial. To
  Dagstuhl - Leibniz-Zentrum für Informatik, 2016. doi:
                                                                      avoid the excessive computation costs, we conduct a group
  10.4230/LIPIcs.ECOOP.2016.2.
                                                                      of controlled experiments under two settings. In the first
Chengpeng Wang, Wuqi Zhang, Zian Su, Xiangzhe Xu, and                 setting, LLMDFA is only applied to functions covered by
  Xiangyu Zhang. Sanitizing large language models in                  buggy program paths, generating data-flow summaries for
  bug detection with data-flow. In Findings of the Associa-           these functions. In the second setting, LLMDFA is tasked
  tion for Computational Linguistics: EMNLP 2024, pages               with generating data-flow summaries for functions reach-
  3790–3805, 2024c.                                                   able from each source value. We refer to these settings as
                                                                      LLMDFA-PATH S CAN and LLMDFA-S RC S CAN, respec-
                                                                      tively. Notably, the number of prompting rounds and com-
A. Comparison with LLM-driven Detectors                               putational costs of LLMDFA-PATH S CAN and LLMDFA-
                                                                      S RC S CAN are lower than those of LLMDFA, as the latter
Setup and Metrics. To the best of our knowledge, there are
                                                                      two only reason a subset of the functions in the repository.
two kinds of LLM-driven code auditing techniques, namely
end-to-end few-shot chain-of-thought (CoT) prompting-                 Result. Figure 6 shows the comparison results between the
based approaches and agent-centric approaches. Specif-                single-function level bug detector, multiple-function level
ically, the former can be divided into two categories, in-            bug detector, and R EPOAUDIT. The single-function level
cluding single-function level bug detection and multiple-             bug detector can detect only one intra-procedural NPD bug.
function level bug detection. First, the single-function level        The key reasons are twofold. First, it only accesses the

                                                                 13
                      Listing 1. An example of control flow facts ignored by single-function level bug detectors
    1. static int __init damon_reclaim_init(void){
    2.   ctx = damon_new_ctx();
    3.   if (!ctx)
    4.       return -ENOMEM;
    5.   if (damon_select_ops(ctx, DAMON_OPS_PADDR))
    6.       return -EINVAL;
    7.   ctx->callback.after_wmarks_check = damon_reclaim_after_wmarks_check;
    8.   ctx->callback.after_aggregation = damon_reclaim_after_aggregation;
    9.   target = damon_new_target();
   10. if (!target) {
   11.      damon_destroy_ctx(ctx);
   12.      return -ENOMEM;
   13. }
   14. damon_add_target(ctx, target);
   15. schedule_delayed_work(&damon_reclaim_timer, 0);
   16. damon_reclaim_initialized = true;
   17. return 0;
   18. }


                                                                      rounds for LLMDFA-PATH S CAN is 165 times that of R E -
Table 5. The ratios of the prompting rounds (Prompt) and input
                                                                      POAUDIT , and the input token count is 123 times higher.
token costs (In token) of LLMDFA under two settings
                   LLMDFA-PATH S CAN     LLMDFA-S RC S CAN            Similarly, for LLMDFA-S RC S CAN, the number of prompt-
 Bug Type     ID
                   Prompt In Token       Prompt   In Token            ing rounds is 1,737 times that of R EPOAUDIT, with an
              N1   115.39   81.23         871.61    522.40            input token count 1,193 times higher. It is important to
              N2   217.00  120.23        2,839.00  2,087.27           note that the actual cost of LLMDFA would be even greater
   NPD        N3     6.83    3.13         255.57    224.82
              N4   115.76   74.91         778.17    715.23            in practical scenarios. This significant performance gap
              N5   199.43  125.53        7,121.86  5,350.62           stems from the fact that LLMDFA follows a desgin similar
              U1    41.89   23.08        4,536.75  2,530.74           to compiler-based scanners that first collect all primitive
              U2    24.00   12.29          50.00     26.26            data-flow facts and then correlate them to find bugs. For
   UAF        U3   759.48  693.73          17.63     6.17
              U4   167.50   95.58          46.60     25.42            example, to detect the NPD bugs in the example program
              U5     4.98    2.09         853.20    447.36            shown in Figure 1, LLMDFA begins with the NULL value
    Average        165.23  123.18        1737.04   1193.63            at line 4 in the function field2json, analyzing the de-
                                                                      pendencies of it with all the arguments, return value, and
last function in the buggy path and lacks the calling con-            dereference pointers (e.g., field at line 8) within this func-
text of the function. In NPD detection, for example, the              tion. Hence, LLMDFA fails to scale to large-size projects
single-function level detector cannot determine whether the           in the real-world senarios.
parameter is null or not, which makes it fail to detect inter-
procedural bugs. Second, the model may overlook essential
control flows within a function, which results in its inabil-
                                                                      B. Comparison with Industrial Bug Detectors
ity to accurately identify the data-flow facts of a specific          Setup and Metrics. We choose two typical static bug de-
value, thereby achieving low recall in intra-procedural bug           tectors as the representatives of industrial tools, namely
detection. For instance, as shown by Listing 1, the LLM               Meta I NFER (Meta, 2025) and Amazon C ODE G URU (Ama-
ignores the error handling branch at line 6, which causes             zon, 2025). Specifically, Meta I NFER is a static analysis
the function to return without releasing the memory object            tool from Meta. Benefiting from its sophisticated mem-
allocated by the function damon_new_ctx(), leading to                 ory model (Calcagno et al., 2009), Meta I NFER features
its failure to detect this memory leak bug. With access to the        its outstanding ability in memory bug detection. All three
full calling context, the multiple-function level bug detector        bug types in our evaluation are supported by Meta I NFER.
is able to detect 10 bugs. This demonstrates that providing           Notably, Meta I NFER is only applicable to projects that
additional calling context can improve the bug detection              can be successfully compiled. Amazon C ODE G URU, as an
capabilities of the LLM. However, the improvement is still            AWS service, combines machine learning and automated
limited. Due to hallucinations, the LLM may still wrongly             reasoning to identify underlying bugs. Unlike Meta I NFER,
analyze certain intra-procedural and inter-procedural data-           Amazon C ODE G URU can directly analyze source code with-
flow facts, resulting in a significant number of FNs. In              out compilation. As Amazon C ODE G URU does not support
contrast, R EPOAUDIT performs the path-sensitive reason-              MLK detection, we only evaluate it for the NPD and UAF
ing by employing the program abstraction, which facilitates           detection. After running the two industrial bug detectors, we
precisely discovering data-flow facts for code auditing.              manually check the bug reports, label the TPs and FPs, and
Table 5 shows the comparison results between LLMDFA                   compare with the results by R EPOAUDIT shown by Table 2
and R EPOAUDIT. On average, the number of prompting                   in Section 4.2.

                                                                 14
Result. Table 3 presents the results of Meta I NFER and              Table 6. The statistics of R EPOAUDIT -N OA BS and R EPOAUDIT -
Amazon C ODE G URU. As shown by the column Build in                  N OVAL
                                                                                         R EPOAUDIT -N OA BS      R EPOAUDIT -N OVAL
Table 3, 13 projects can be successfully compiled However,
                                                                      Bug Type     ID        TP                       TP
five of them still cause crashes in Meta I NFER, namely the                                            FP                       FP
                                                                                         Old New                  Old New
projects with the IDs N3, M3, M5, U1, and U2, even after                           N1     1    (3,3)    4          1    (3,3)     2
we have tried multiple versions of Infer, including v1.2.0                         N2     4    (0,0)    5          7    (1,0)     0
(latest), v1.0.0, and v0.9.0. We have reported these issues             NPD        N3     0    (0,0)    6          1    (1,0)    10
                                                                                   N4     0    (0,0)    0          1    (0,0)     5
to Meta I NFER, but haven’t received any response yet. The                         N5     1    (2,2)    2          1    (5,4)     4
failures of compiling and analyzing successfully compiled                          M1     1    (1,1)    2          1    (2,1)     3
projects demonstrate the restricted applicability and insta-                       M2     1    (1,1)    5          1    (6,6)     5
bility of compilation-dependent bug detectors. Eventually,              MLK        M3     1    (0,0)    0          1    (0,0)     0
we successfully analyze eight projects with Meta I NFER,                           M4     0    (0,0)    0          1    (0,0)     1
                                                                                   M5     0    (0,0)    0          1    (0,0)     2
obtaining a total of seven TPs and two FPs. Notably, for                           U1     1    (0,0)    0          1    (0,0)     0
project libfreenect with the project ID N4, the five                               U2     1    (0,0)    0          1    (0,0)     0
TPs generated by Infer are based on the assumption that                 UAF        U3     1    (0,0)    1          1    (0,0)     0
external APIs realloc and malloc can return null point-                            U4     1    (0,0)    0          1    (0,0)     0
                                                                                   U5     0    (1,0)    6          1    (1,0)     6
ers upon allocation failure. However, this assumption does
                                                                           Total         13      8      31        21     19      38
not always hold. In our implementation, R EPOAUDIT does
not rely on such assumptions and instead begins its analysis
with null literal values or other user-defined APIs. Lastly,         Table 7. The computational costs of R EPOAUDIT -N O C ACHE.
although Meta I NFER is known for its powerful memory                OOT: the out-of-time, indicating that R EPOAUDIT -N O C ACHE
model, it still fails to detect any MLK or UAF bugs discov-          does not finish the code auditing in 72 hours.
ered by R EPOAUDIT. In comparison, R EPOAUDIT not only                Bug Type     ID
                                                                                          # Prompts      Financial($)         Time(s)
supports non-compilation analysis with greater applicability                             Num    Ratio   Num Ratio          Num      Ratio
                                                                                   N1    436    3.01     8.65   2.91     6,316.37     3.12
but also shows stronger detection capabilities, identifying                        N2     18    1.06     0.43   1.03      312.01      1.10
40 TPs in total.                                                        NPD        N3    175    1.61     4.12   1.59     3,098.59     1.77
                                                                                   N4    181    6.24     3.06   5.19     2,342.23     5.38
As shown by the last two columns in Table 3, Amazon                                N5    137    2.17     4.09   2.37     2,626.21     2.48
C ODE G URU does not detect any TPs upon the targeted 10                           M1    459    2.24    10.49 2.24       7,070.68     2.42
                                                                                   M2    584    4.00    15.83 4.40      10,852.80 4.76
projects, while generating 18 FPs. Due to the limitations of            MLK        M3      2    1.00     0.05   0.95       34.34      1.00
its inherent formal reasoning techniques and machine learn-                        M4      1    1.00     0.03   0.87       20.13      1.12
ing models, Amazon C ODE G URU can only detect certain                             M5    200    5.71     4.88   5.67     3,635.66     6.06
                                                                                   U1    657    18.25   14.34 17.93     11,528.96 19.80
patterns of bugs and is not robust to the various ways of                          U2      2    1.00     0.04   1.00       32.78      1.03
writing similar buggy code.                                             UAF        U3     67    1.40     2.10   1.62     1,153.46     1.46
                                                                                   U4     10    1.00     0.23   0.99      174.43      0.94
                                                                                   U5    N/A     N/A     N/A    N/A        OOT        N/A
C. Ablation Study                                                        Average        209.21 3.55      4.88   3.48     3,514.19     3.75

Setup and Metrics. To evaluate the effectiveness of each
technical design, we introduce three ablation variants of            tion paths created by numerous conditional branches, loop
R EPOAUDIT, namely R EPOAUDIT -N OA BS, R EPOAUDIT -                 structures, and their nested combinations within functions.
N OVAL, and R EPOAUDIT -N O C ACHE. Specifically, R E -              When analyzing such cases, the model becomes more sus-
POAUDIT -N OA BS skips the program abstraction, i.e., re-
                                                                     ceptible to hallucinations, resulting in missed buggy propa-
moving the second step in the prompt template shown in               gation paths or incorrect identification of non-existent ones.
Figure 4. R EPOAUDIT -N OVAL removes the validation of
the data-flow facts discovered by the explorer and also skips        When the validators are disabled, the number of FPs in-
examining the bug reports. R EPOAUDIT -N O C ACHE dis-               creases to 31, causing a 245.45% increase. This rise
ables the caching strategy upon the agent memory when the            is mainly caused by the presence of various conditional
explorer analyzes individual functions.                              branches and jump statements, such as if-else and
                                                                     switch, as well as early exits in certain branches (e.g.,
Result. Table 6 presents the results of R EPOAUDIT -N OVAL           error handling). Without the validator, the LLM may hal-
and R EPOAUDIT -N OA BS. Without the program abstrac-                lucinate and fail to account for these critical branches, re-
tion, R EPOAUDIT -N OA BS decreases the number of TPs by             sulting in a large number of spurious data-flow facts that
47.50%, while increasing the number of FPs by 181.82%,               do not meet feasibility requirements. Besides, the conflicts
leading to a precision degradation to 40.38%. This decline is        between branch conditions discovered by the LLM can also
attributed to the complex control flows and multiple execu-          contribute to the high precision.

                                                                15
                                      Table 8. The statistics of R EPOAUDIT powered by DeepSeek R1
                                            TP                                     # Tokens
                 Bug Type      ID                      FP      # Prompts                            Financial ($)    Time (s)
                                      Old     New                              Input      Output
                               N1      1      (3,3)    2          136         675,711     46,839        1.20         12,378.10
                               N2      7      (2,0)    0           14         74,918       6,057        0.14          1,588.65
                   NPD         N3      1      (1,0)    0           97         524,915     38,644        0.95          9,044.85
                               N4      1      (0,0)    0            7         29,898       2,288        0.05           247.99
                               N5      1      (7,6)    0           43         270,880     15,689        0.47          2,936.52
                               M1      1      (2,2)    2          165         910,153     55,623        1.58         14,633.28
                               M2      1      (9,9)    1           93         562,470     35,498        0.98          5,583.13
                   MLK         M3      1      (0,0)    0            2         10,481        832         0.02           74.01
                               M4      1      (0,0)    0            1           5691        214         0.01           93.23
                               M5      1      (0,0)    0           18         92,573       8,289        0.18          1,572.31
                               U1      1      (0,0)    0           50         255,048     19,494        0.46          2,444.72
                               U2      1      (0,0)    0            2           8900        704         0.02           88.76
                   UAF         U3      1      (0,0)    0           29         227,336     10,269        0.37          2,768.59
                               U4      1      (0,0)    0           11         53,647       3,617        0.09          1,997.20
                               U5      1      (1,0)    1          226        1,191,391    78,226        2.10         13,124.44
                     Average                                     59.60      326,267.47 21,485.53        0.57          4,571.72

                                    Table 9. The statistics of R EPOAUDIT powered by Claude 3.7 Sonnet
                                            TP                                      # Tokens
                 Bug Type      ID                       FP      # Prompts                            Financial ($)    Time (s)
                                      Old     New                               Input      Output
                               N1      1      (3,3)        2        85        371,008      58,822        2.00         1,650.53
                               N2      7      (1,0)        0        15         98,473       9,015        0.43          264.68
                   NPD         N3      1      (1,0)        0        74        480,786      78,725        2.62         2,076.32
                               N4      1      (0,0)        0        15         62,634       8,822        0.32          233.96
                               N5      1      (7,6)        0        27        213,483      21,107        0.96          592.74
                               M1      1      (2,2)        2       215        1195594      118735        5.37         3,510.25
                               M2      1     (10,10)       1        87         537290       61472        2.53         1,842.90
                   MLK         M3      1      (0,0)        0         2          10548        1097        0.05          46.25
                               M4      1      (0,0)        0         1           5741        1024        0.03          32.86
                               M5      1      (0,0)        0        16         81,970       9,442        0.39          402.17
                               U1      1      (0,0)        0        18          93466       17159        0.54          462.51
                               U2      1      (0,0)        0         2           8870        1145        0.04          117.50
                   UAF         U3      1      (0,0)        0        82         605597      70,666        2.88         1,936.22
                               U4      1      (0,0)        0        10          48206        9823        0.29          314.60
                               U5      1      (1,0)        0       207        1069189      147422        5.42         4,387.80
                     Average                                      57.07      325,523.67 40,965.06        1.59         1,191.42

The results of R EPOAUDIT -N O C ACHE are presented in Ta-                      Claude 3.7 Sonnet, and OpenAI o3-mini separately. In gen-
ble 7. For the project icu, the analysis time exceeds 72                        eral, when integrated with reasoning models, R EPOAUDIT
hours and the number of prompting rounds exceeds 20,000,                        demonstrates stronger bug detection capabilities than the
more than 30 times that of R EPOAUDIT. For the remaining                        one powered by Claude 3.5 Sonnet. It is able to identify
projects, on average, the number of prompting rounds in-                        all known bugs reported by existing works and can further
creases by 3.55 times, the financial cost by 3.48 times, and                    discover additional previously unreported bugs with higher
the analysis time by 3.75 times compared to R EPOAUDIT.                         precision. This better performance is largely attributed to
Moreover, the cache hit rate is closely related to the project’s                the reasoning model’s ability to autonomously construct
size and the density of underlying graphs. In projects with                     logical reasoning pathways, thus facilitating more precise
intricate call graphs and dense DDGs, a single function can                     reasoning of control-flow and data-flow facts of a program.
appear in multiple propagation paths of faulty values. For
                                                                                As shown in Table 8, R EPOAUDIT powered by
example, in the icu project, parsing-related functions are
                                                                                DeepSeek R1 successfully identifies 46 true positives,
hit in the cache 623 times. In such cases, the caching strat-
                                                                                achieving a precision of 88.46%, the highest among all
egy effectively reduces analysis costs and keeps the analysis
                                                                                evaluated models. This indicates a superior capability of
time within an acceptable range.
                                                                                DeepSeek R1 in analyzing program control-flow and data-
                                                                                flow. In terms of cost efficiency, DeepSeek R1 incurs an
D. Evaluation with More Reasoning Models                                        average cost of $0.57 per project. However, it is also the
Table 8, Table 9, and Table 10 show the results                                 slowest model, with an average analysis time of 4,571 sec-
of R EPOAUDIT with reasoning models DeepSeek R1,                                onds per project, which may be attributed to factors such as
                                                                                network latency and limited throughput.

                                                                           16
                                  Table 10. The statistics of R EPOAUDIT powered by OpenAI o3-mini
                                         TP                                # Tokens
                Bug Type     ID                    FP   # Prompts                            Financial ($)    Time (s)
                                   Old     New                         Input      Output
                             N1     1      (3,3)   2        49       237,382      26,360          0.38          782.75
                             N2     7      (1,0)   0        17       104,462      10,286          0.16          321.19
                  NPD        N3     1      (0,0)   0        16        86,930       8,724          0.13          261.61
                             N4     1      (0,0)   2        17        80,877       8,169          0.12          299.13
                             N5     1      (6,5)   1        24       170,504      13,115          0.25       598.2588062
                             M1     1      (2,2)   0        39        196898      18937           0.30          609.81
                             M2     1      (7,7)   2        46        303005      24773           0.44         1,005.86
                  MLK        M3     1      (0,0)   0        2          10481       1134           0.02           44.26
                             M4     1      (0,0)   0        1           5691        811           0.01           36.87
                             M5     1      (0,0)   0        13         66601       7672           0.11          330.96
                             U1     1      (0,0)   0        24        128434      12641           0.20          266.63
                             U2     1      (0,0)   0        2           9422        958           0.01           24.08
                  UAF        U3     1      (1,0)   1        83        634100      48,528          0.91         1,176.46
                             U4     1      (0,0)   0        10         50966       4044           0.07          190.54
                             U5     1      (1,0)   1       178        976191      82933           1.44         3,427.38
                   Average                                34.73     204,129.60 17,939.00          0.30          625.05


As shown in Table 9, R EPOAUDIT powered by
                                                                         Table 11. The statistics of R EPOAUDIT with different temperature
Claude 3.7 Sonnet also detects 46 true positives, yielding
                                                                         settings. The column # Reproduce indicates the number of the
the precision of 86.79%, which is marginally below that of               reproduced bugs that are previously reported by existing works.
DeepSeek R1. Given the inherent randomness, we consider                   Temperature   TP   FP    # Reproduce   Precision (%)   Recall (%)
Claude 3.7 Sonnet Sonnet’s program analysis capabilities to                    0        40   11         21           78.43          100
be comparable to those of DeepSeek R1. In terms of prompt-                   0.25       38   12         21           76.00          100
                                                                              0.5       38   12         20           76.00         95.24
ing rounds and token usage, Claude 3.7 Sonnet induces sim-                   0.75       33   11         18           75.00         85.71
ilar prompting rounds and input token numbers per project                     1.0       35   13         19           72.92         90.48
as DeepSeek R1. However, its output token count is 1.9
times higher. Based on the pricing policy,Claude 3.7 Sonnet              temperatures, we evaluate R EPOAUDIT under four addi-
is the most expensive model, resulting in the highest average            tional temperature settings: 0.25, 0.5, 0.75, and 1.0. For
financial cost of $1.59 per project.                                     each setting, we record the number of true positives and
                                                                         false positives detected by R EPOAUDIT, and compute the
As shown in Table 10, R EPOAUDIT powered by
                                                                         corresponding precision. Also, we measure the recall by
OpenAI o3-mini demonstrates slightly lower code analy-
                                                                         investigating the proportion of reproduced bugs.
sis performance, detecting 42 true positives with a precision
of 82.35%. This may be due to its relatively weaker ability
to capture complex code semantics, particularly in modeling              Results. As shown in Table 11, R EPOAUDIT demonstrates
data-flow, potentially resulting in both false positives and             stable performance across varying temperature levels, with
missed bugs. In terms of efficiency, OpenAI o3-mini issues               precision remaining above 72% and recall consistently high.
significantly fewer queries per project compared to the other            However, as the temperature increases to 1.0, both precision
two models, which may also contribute to its narrower func-              and recall decline, suggesting that greater randomness in
tion coverage and oversight of potential data-flows. Besides,            the model’s output can lead to incorrect reasoning steps,
OpenAI o3-mini incurs the lowest cost per query and of-                  ultimately resulting in an increased number of false positives
fers the fastest analysis speed. On average, R EPOAUDIT                  and false negatives.
powered by OpenAI o3-mini results in the financial cost of
$0.30 and the time cost of 624.05 seconds per project.
                                                                         F. Examples of False Positive/Negative
The above statistics demonstrate that R EPOAUDIT can seam-
lessly benefit from advances in LLM capabilities, leading                We present representative a false positive and a false neg-
to improved precision and recall in code auditing. Also, en-             ative of R EPOAUDIT as follows. These cases can reflect
hancements in LLM inference efficiency can further boost                 several limitations of our approach, including the model’s
the overall performance of the auditing process.                         tendency to hallucinate during complex control-flow reason-
                                                                         ing and its insufficient understanding of implicit semantic
                                                                         constraints.
E. Evaluation with Different Temperatures
                                                                         In Listing 2, the function vrf_get can return NULL when
Setup and Metrics. In our evaluation, we set the tem-                    name=NULL and vrf_id=VRF_UNKNOWN. In the func-
perature to 0.0 by default. To assess the impact of the                  tion lib_vrf_create, the return value of vrf_get is

                                                                    17
      Listing 2. An example of a false positive reported by R EPOAUDIT due to unawareness of the YANG schema constraints.
    1 struct vrf *vrf_get(vrf_id_t vrf_id, const char *name)
    2 {
    3     struct vrf *vrf = NULL;
    4      Nothing to see, move along here
    5     if (!name && vrf_id == VRF_UNKNOWN)
    6         return NULL;
    7     ...
    8 }

    1 static int lib_vrf_create(struct nb_cb_create_args *args)
    2 {
    3    const char *vrfname;
    4    struct vrf *vrfp;
    5    vrfname = yang_dnode_get_string(args->dnode, "name");
    6    if (args->event != NB_EV_APPLY)
    7       return NB_OK;
    8    vrfp = vrf_get(VRF_UNKNOWN, vrfname);
    9    SET_FLAG(vrfp->status, VRF_CONFIGURED);
   10    ...
   11 }




Listing 3. An example of a false negative reported by R EPOAUDIT results from Claude 3.5 Sonnet overlooking the error-handling path.
    1 struct Sass_Compiler* ADDCALL sass_make_data_compiler (struct Sass_Data_Context* data_ctx) {
    2   if (data_ctx == 0) return 0;
    3   Context* cpp_ctx = new Data_Context(*data_ctx);
    4   return sass_prepare_context(data_ctx, cpp_ctx);
    5 }

    1 static Sass_Compiler* sass_prepare_context (Sass_Context* c_ctx, Context* cpp_ctx) throw() {
    2   void* ctxmem = calloc(1, sizeof(struct Sass_Compiler));
    3   if (ctxmem == 0) {
    4     std::cerr << "Error allocating memory for context" << std::endl;
    5     return 0;
    6   }
    7   Sass_Compiler* compiler = (struct Sass_Compiler*) ctxmem;
    8   compiler->c_ctx = c_ctx;
    9   return compiler;
   10 }




assigned to the pointer vrfp, which is subsequently deref-            sue as it did not accurately track all relevant execution paths,
erenced without a null check, seemingly leading to a po-              particularly the error-handling path in this case. In contrast,
tential Null-Pointer-Dereference (NPD) bug. R EPOAUDIT                reasoning-oriented models like Deepseek R1 demonstrated
reports an NPD bug at line 9, where vrfp->status is                   superior capability in recognizing execution paths precisely,
accessed without checking whether vrfp is NULL. How-                  allowing R EPOAUDIT to detect such memory management
ever, this issue is a false positive. Due to YANG schema              issues more effectively.
validation, the vrfname variable is guaranteed to be non-
NULL. Given that vrf_get only returns NULL when both
name=NULL and vrf_id=VRF_UNKNOWN, it cannot re-
turn NULL when vrfname!=NULL. Hence, the derefer-
ence is safe in practice. The root cause of the false positive
is that the LLMs are not aware of the fact that the return
value of yang_dnode_get_string is never NULL.
In Listing 3, a memory object is allocated by the function
sass_make_data_compiler and passed as the sec-
ond argument to the function sass_prepare_context.
Within sass_prepare_context, if calloc fails at
line 3, ctxmem is set to 0, and the function returns 0
without freeing the allocated memory object cpp_ctx
or assigning it to any other pointer, leading to a memory
leak. This bug was detected by Deepseek R1 but missed by
Claude 3.5 Sonnet. The latter model failed to identify the is-

                                                                 18
