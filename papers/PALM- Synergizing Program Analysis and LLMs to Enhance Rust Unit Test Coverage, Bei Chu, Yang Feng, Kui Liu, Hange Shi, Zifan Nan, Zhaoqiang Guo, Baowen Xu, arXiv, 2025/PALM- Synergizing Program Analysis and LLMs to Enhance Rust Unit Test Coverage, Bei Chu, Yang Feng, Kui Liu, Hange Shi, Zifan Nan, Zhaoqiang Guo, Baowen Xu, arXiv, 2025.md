                                         PALM: Synergizing Program Analysis and LLMs to
                                                Enhance Rust Unit Test Coverage
                                                    Bei Chu∗ , Yang Feng∗ , Kui Liu† , Hange Shi∗ , Zifan Nan† , Zhaoqiang Guo† and Baowen Xu∗
                                                            ∗ State Key Laboratory for Novel Software Technology, Nanjing University, Nanjing, China
                                                                  † Software Engineering Application Technology Lab, Huawei, Hangzhou, China

                                                  {beichu, hangeshi, gzq}@smail.nju.edu.cn, {fengyang, bwxu}@nju.edu.cn, {kui.liu, nanzifan}@huawei.com


                                             Abstract—Unit testing is essential for ensuring software reli-    as it increases confidence in the software’s correctness by
                                         ability and correctness. Classic Search-Based Software Testing        exercising more of its behavior [7].
                                         (SBST) methods and concolic execution-based approaches for               However, classic automated unit test generation methods
                                         generating unit tests often fail to achieve high coverage due to
                                                                                                               aimed at achieving high coverage, such as search-based soft-
arXiv:2506.09002v3 [cs.SE] 29 Sep 2025




                                         difficulties in handling complex program units, such as branching
                                         conditions and external dependencies. Recent work has increas-        ware testing (SBST) [8], [9], [10], [11], [12] and concolic ex-
                                         ingly utilized large language models (LLMs) to generate test          ecution [13], [14], [15], [16], have inherent limitations. SBST
                                         cases, improving the quality of test generation by providing better   methods employ search algorithms to generate test inputs
                                         context and correcting errors in the model’s output. However,         or call sequences, retaining those that execute correctly and
                                         these methods rely on fixed prompts, resulting in relatively low
                                         compilation success rates and coverage.                               enhance coverage and then mutate these inputs to maximize
                                             This paper presents PALM, an approach that leverages large        coverage. Despite automating test generation through search
                                         language models (LLMs) to enhance the generation of high-             optimization, SBST suffers from high computational costs
                                         coverage unit tests. PALM performs program analysis to identify       due to repeated program executions [9], a critical dependency
                                         branching conditions within functions, which are then combined        on the fitness landscape which may prioritize coverage over
                                         into path constraints. These constraints and relevant contextual
                                         information are used to construct prompts that guide the LLMs
                                                                                                               fault detection [17], sensitivity to the curse of dimensionality
                                         in generating unit tests. We implement the approach and evaluate      in large input/state spaces [18], and difficulties in handling
                                         it in 15 open-source Rust crates. Experimental results show that      complex program semantics and external dependencies [19],
                                         within just two or three hours, PALM can significantly improve        limiting its practical efficacy. Meanwhile, concolic execution
                                         test coverage compared to classic methods, with increases in          techniques, such as Syrust [13] and AUTS [20], can satisfy
                                         overall project coverage exceeding 50% in some instances and
                                         its generated tests achieving an average coverage of 72.30%,
                                                                                                               condition constraints and improve coverage by combining
                                         comparable to human effort (70.94%), highlighting the potential       concrete and symbolic execution on test drivers. Nevertheless,
                                         of LLMs in automated test generation. We submitted 91 PALM-           they may suffer from path explosion [21], [22], [23], the com-
                                         generated unit tests targeting new code. Of these submissions,        putational complexity and scalability limitations of constraint
                                         80 were accepted, 5 were rejected, and 6 remain pending review.       solving [24], significant difficulties in accurately modeling
                                         The results demonstrate the effectiveness of integrating program
                                         analysis with AI and open new avenues for future research in
                                                                                                               environment interactions and external dependencies [25], [26],
                                         automated software testing.                                           and the substantial engineering overhead required for develop-
                                             Index Terms—unit testing, automated test generation, large        ing and maintaining complex symbolic execution engines [27].
                                         language models, Rust, program analysis, coverage.                       Recently, large language models (LLMs) have emerged as a
                                                                                                               promising solution to the limitations of classic test generation
                                                                I. I NTRODUCTION                               methods [28], [29], [30]. LLMs like OpenAI’s GPT series [31]
                                                                                                               and DeepSeek [32] have demonstrated remarkable capabilities
                                            Software testing is crucial in the software development            in understanding and generating natural language [33], [34].
                                         lifecycle, ensuring functionality and compliance with require-        Given that these LLMs are trained on enormous datasets, they
                                         ments [1], [2], [3]. Unit testing [4] is particularly effective in    can also understand and generate code [35], [36]. However,
                                         detecting defects early and maintaining code quality. Mean-           existing approaches leveraging LLMs for unit test generation
                                         while, creating unit tests is often time-consuming, typically         often rely on fixed prompting strategies [37], [38], lacking
                                         consuming over 15% of development time [5], [6]. Manually             explicit guidance on a method’s internal structure and feasi-
                                         writing test cases is tedious and prone to errors, usually            ble execution paths. Consequently, when generating tests for
                                         resulting in incomplete coverage and undetected bugs. This            methods with complex branch conditions, these approaches
                                         underscores the need for automated solutions to generate unit         often fail to cover longer, intricate paths–a shortcoming that
                                         tests efficiently and accurately. Code coverage is the widely-        critically undermines the goal of achieving high coverage, a
                                         used metric for evaluating the effectiveness of such automated        critical testing objective. Addressing this limitation necessi-
                                         tests. It measures the proportion of the source code (e.g.,           tates techniques that explicitly decompose the problem based
                                         statements, branches) executed by the test suite, providing an        on the program’s execution paths, enabling targeted guidance
                                         objective indicator of its comprehensiveness. Achieving high          to the LLM for each distinct scenario.
                                         code coverage is a primary goal in automated test generation,            Different from existing works, in this paper, we develop
PALM, an approach that combines classic program analysis            and error-prone nature of manual testing [5], [6]. Classic
techniques with emerging large language models to generate          approaches fall into two categories: search-based [12], [41],
unit tests satisfying specific path constraints. Recent research    [8], [11] and symbolic execution-based [13], [15], [14], [42].
shows that breaking a problem into smaller steps and prompt-            Search-Based Software Testing (SBST). Search-Based
ing LLMs to solve each step sequentially yields better results      Software Testing (SBST) methods uses meta-heuristic algo-
than directly asking for an answer [39], [40]. This enables         rithms (e.g., genetic algorithms) to iteratively mutate test
LLMs to tackle more complex problems effectively. Based             cases for coverage improvement [18], [43]. Fundamentally,
on this principle, we can decompose the task of generating          these tools operate by leveraging two core steps: (i) ini-
unit tests into several smaller tasks, each corresponding to a      tially generating a random set of test cases as seed inputs
specific execution path within the focal method. This decom-        and (ii) iteratively mutating these test cases to enhance the
position allows LLMs to focus on specific subtasks, resulting       coverage of the focal method. Thanks to search algorithms,
in more accurate and diverse test cases. By combining these         SBST methods can automatically explore possible test inputs
tests, we can create a comprehensive test suite that effectively    and generate tests with higher coverage through optimized
covers various execution paths.                                     search techniques. However, SBST methods face the following
   PALM begins with path analysis of the focal method to            challenges: (i) when dealing with complex and large systems,
identify its execution paths, each representing a sequence of       the search algorithms can consume substantial computational
conditions and return values. We gather contextual informa-         resources [44], (ii) they can get trapped in local optima [45],
tion, including the focal method’s body, other declarations,        and (iii) the quality of the generated tests is influenced by the
definitions, and function call details, to guide the LLM. For       initial inputs and fitness landscape characteristics [46].
each path, we construct a prompt using this information and             PALM decomposes the test generation task based on iden-
ask the LLM to generate test cases. This ensures focused,           tified execution paths, each associated with specific branch
comprehensive test case generation. We have implemented             condition constraints. This decomposition significantly reduces
PALM for Rust and evaluated it on 15 open-source projects           the search space that needs to be considered for each sub-
with 4145 focal methods. The GPT-4o mini-based prototype            task, thereby reducing computational resource consumption
achieved an increase of over 20% in the generation of compil-       compared to SBST. Additionally, by leveraging LLMs’ ability
able tests and an improvement in coverage exceeding 50%. 91         to understand code semantics and constraints, PALM can gen-
unit tests, generated by PALM to cover code regions lacking         erate tests that are more directly aligned with the requirements
prior developer-written tests, were submitted via pull requests.    of a specific path, reducing the reliance on random initial
Subsequently, 80 of these tests were integrated into the project,   inputs and their potential impact on result quality.
representing an 94.12% acceptance rate among those reviewed.            Concolic Execution. Concolic execution blends concrete
   In summary, this paper makes the following contributions:        and symbolic execution to collect path constraints and generate
  • Approach. We introduce PALM, which combines pro-                tests [25], [47], [48]. It uses a constraint solver to reason
     gram analysis with LLMs to generate high-coverage unit         about path constraints, thereby generating test inputs. Through
     tests. This approach breaks the task into steps based on       symbolic execution, this approach can systematically explore
     specific conditional paths within the focal method, using      different execution paths in a program, generating high-
     targeted prompts to guide the LLM.                             coverage test cases. However, this method still faces several
  • Tool. We implemented the PALM based on rustc APIs               challenges in practice. Loops in the program can lead to path
     and designed a system that automatically generates unit        explosion, causing symbolic execution to consume substantial
     tests through interaction with a large language model.         computational resources. Constraint solvers may also struggle
     The system is currently a prototype, with plans for open-      with complex constraint conditions. Furthermore, symbolic
     sourcing upon completion.                                      execution often finds handling code involving external depen-
  • Study. We evaluated PALM on 15 open-source projects             dencies, such as file systems or networks challenging.
     with 4145 focal methods. Our GPT-4o mini-based proto-              Similar to symbolic execution, PALM leverages path analy-
     type increased the ratio of correctly generated, compilable    sis to identify the constraints defining each execution path.
     tests by up to 20% and improved coverage by up to 50%.         However, instead of feeding these constraints to a classic
  • Practical Usage. 91 generated unit tests were submitted         solver, PALM uses the constraints as part of a natural language
     as pull requests to 8 distinct, popular open-source Rust       prompt to guide an LLM to generate concrete input values that
     projects. Project maintainers subsequently accepted and        satisfy the constraints for that specific path. This approach
     merged 80 of these submissions, accompanied by positive        aims to bypass the computational complexity of constraint
     feedback. This represents an acceptance rate of 94.12%         solving and the challenges in modeling external dependencies
     among the unit tests that underwent maintainer review.         inherent in classic symbolic execution engines.
                     II. BACKGROUND                                 B. LLM for Code Generation
A. Unit Test Generation                                                Large language models (LLMs) have demonstrated impres-
  Unit test generation automates test creation for methods          sive capabilities in the field of natural language processing
under test (focal methods), addressing the time-consuming           (NLP), excelling in various tasks such as conversation [34],
    text generation [49], [50], [51], and reasoning [52]. Given their                                 fn wait
    success in NLP, attention has naturally turned to code-related
                                                                                                           ...
    tasks, leading to the creation of numerous code generation                                            loop
    models, such as AlphaCode [53], PolyCoder [54], Codex [36],
                                                                                                         ...
    Google’s program synthesis model [55], and CodeGen [56].                              if let Err(new_queue) = exchange
       The input text provided to the LLM during inference is
    called a prompt, which guides the model’s generation process.            if strict::addr(new_queue)            while !node.signaled
                                                                             & STATE_MASK != curr_state          .load(Ordering::Acquire)
    Through prompt engineering, researchers can accomplish var-
    ious code-related tasks without the need to retrain the model,              return;          ...         thread::park();    break;
                                                                                              continue;
    such as code completion [57], code explanation [58], and                                                                    return;
    code repair [59], [60], [61]. In this work, we apply prompt
    engineering techniques to construct structured prompts that         Fig. 1: Control flow graph of the focal method wait,
    explicitly incorporate the path constraints and context for each    highlighting the complex control flow involving conditional
    execution path, guiding the LLM to generate test cases.             branches and nested loops that pose significant challenges for
                                                                        automated test generation.
          III. D EFINITIONS AND M OTIVATING E XAMPLE
                                                                        flow behavior, we present its control flow graph (CFG) in
       We present the definitions used throughout the paper and         Fig. 1. The CFG of the wait method reveals a structured
    illustrate our objectives with an example.                          composition of 2 conditional branches and 2 nested loops. To
       Context. In this paper, the term context generally refers to     ensure comprehensive coverage, test inputs must be carefully
    the code related to, but distinct from, the focal method and        crafted to meet the constraints.
    the test functions. There are two types of context: (i) focal          Despite its power, symbolic execution struggles with func-
    context, which is the context of the focal method, typically        tions like wait. Its nested loops can trigger a path explo-
    consisting of headers, macros, and global variables in the file     sion, overwhelming the analysis [26], while Rust’s unique
    containing the focal method; the declarations and definitions       ownership model and concurrency primitives like AtomicPtr
    of the class to which the focal method belongs (if applicable);     pose significant modeling challenges for symbolic engines,
    and the declarations and definitions of the data types and          hindering scalability [63], [64]. Meanwhile, existing LLM-
    functions used by the focal method. (ii) test context, which        based approaches often fail because they (i) lack the specific
    is the context of the test functions, usually including the         context to correctly set up the function’s preconditions [36],
    necessary use statements for the test files and any predefined      (ii) cannot generate the precise inputs needed to navigate the
    data structures and variables required for the tests.               intricate control flow for high coverage [65], and (iii) fre-
       Condition Chain. By recording the branch conditions that         quently produce code that violates Rust’s strict ownership and
    must be satisfied for control flow transitions during path          type safety rules, leading to low compilation rates. PALM is
    analysis, we can obtain approximate path constraints, which         designed to overcome these specific challenges by synergizing
    are sequences of conditions that must be met for a given            program analysis with LLM generation.
    execution path. In this paper, we refer to such sequences of
    conditions as condition chains.                                                           IV. M ETHODOLOGY
1  fn wait(queue, mut curr_queue) {                                        In this section, we demonstrate the methodology for gen-
2      loop {                                                           erating unit tests for a focal method, such as wait. PALM
 3         if let Err(new_queue) = exchange {                           involves generating prompts corresponding to the execution
 4             if strict::addr(new_queue) & STATE_MASK !=
                    curr_state {                                        paths within the focal method. This breaks down the task
 5                 return;                                              of generating a comprehensive test suite into several steps,
 6             }                                                        each focused on generating tests for a single path. These
 7             continue;
 8         }                                                            prompts ultimately guide the model in generating unit tests
 9         while !node.signaled.load(Ordering::Acquire) {               with high coverage. When test cases fail to compile, we
10             thread::park();                                          provide the model with erroneous code snippets and error
11         }
12         break;                                                       messages, enabling it to suggest repairs iteratively.
13     }
14 }
                                                                        A. Overview
    Code 1: Motivating examples for wait function. Details of              The core of PALM involves collecting the chain of condi-
    struct/trait definitions are omitted.                               tions along each path in the focal method through path analy-
                                                                        sis. By leveraging this technique, we can capture the program’s
       Next, we illustrate the challenges current test case gen-        behavior and gather the constraints along the execution paths.
    eration methods face using the following example. Code 1               Classic test generation methods based on symbolic exe-
    presents the wait method from the once_cell crate [62],             cution enumerate all possible path constraints and generate
    which is used to block the current thread until a concurrent        test cases by solving these constraints [48]. However, real-
    initialization completes. To better depict the method’s control     world code often includes complex data structures and external
                      Step-I: Condition Chains Extraction              Step-III: Prompt Design and Generation         Step-IV: Tests Generation and Repair
                                                                                 populate                                                                        Error
                      build      traverse          combine                       template                                                                      Messages
                      CFG          CFG
                                           Branch           Path                            Condition
                              CFG                                                                                                                             Error Code
                                          Conditions     Constraints                         Chains                               unit test
                                                                                                                                   case              fail      Snippets
                                                                          JSON
                MIR     analyze data                                             populate                 Prompt
                        structure and               map to                       template
                       functions calls               code    Context
          AST                            AST Node                                            Focal                                              compile      merge
Source                                                                                                                                                                Change
                                                              Code                          Context
 Code                                                                                                                                                                  Logs
                                                                                                                                              Compilation Error Fix
                      Step-II: Context Extraction
                                                                          JSON

Fig. 2: The PALM framework. Step I extracts path constraints from the MIR-level CFG. Step II gathers contextual code via
AST/IR analysis. Step III synthesizes a path-specific prompt. Step IV generates tests and uses iterative, compiler-guided repair.
dependencies, making constraint-solving challenging. Loops                              (CFGs), where nodes represent basic blocks—sequences of
or deeply nested conditions can also lead to path explosion,                            instructions without branches or jumps—and edges represent
consuming significant computational resources.                                          control flow transitions, capturing potential execution paths
   PALM addresses these challenges threefold. First, it retains                         and their associated conditional constraints. By analyzing
complex constraints during condition chain collection, avoid-                           these control flow transitions, we can extract the underlying
ing extensive solving. Second, it leverages the LLM’s under-                            conditional constraints. HIR is a compiler-friendly abstraction
standing of constraints and context for test case generation,                           of the Abstract Syntax Tree (AST) and is closer to the syntactic
instead of relying on constraint solvers. Finally, to reduce                            structure of Rust source code compared to MIR.
computational overhead, PALM selects a minimal path set                                    Using the rustc API, we obtain the MIR and HIR of the
covering all branch conditions, tackling this NP-hard set cover                         focal method and perform a preorder traversal of the CFG
problem with a greedy approximation algorithm [66]. The                                 to explore all possible execution paths. When encountering
number of generated tests is determined by the control flow                             control flow transitions, we analyze the terminator of the basic
complexity of the focal method. By default, PALM generates                              block to extract and record the conditional constraints. Upon
one test per minimized path. Additionally, it may generate one                          reaching the exit basic block, we record the return value,
or two boundary tests for path conditions, budget permitting.                           thereby constructing a conditional chain for the execution path.
The decision is based on the nature of the conditional expres-
sion: one test for single-boundary conditions (e.g., x > 10)                            Algorithm 1 Path Minimization
and two for range-based conditions (e.g., x >= 0 && x <=                                Require: set of path constraints P
10). This strategy is designed to achieve full branch coverage                          Ensure: set of minimized path constraints M
efficiently while also probing critical edge cases.                                       M ←∅
   Therefore, our test generation process consists of four                                S ← getConstraints(P )
steps: (I) collecting condition chains of the focal method; (II)                          while S ̸= ∅ do
gathering and constructing context for the focal method; (III)                              pm ← arg max |getConstraints(p) ∩ S|
                                                                                                                p∈P
designing and populating a prompt template suitable for an
                                                                                               M ← M ∪ {pm }
LLM with the condition chains and context; and (IV) using
                                                                                               S ← S\getConstraints(pm )
the prompt to guide the LLM in generating unit tests and
                                                                                             end while
iteratively fixing any test cases that fail to compile. Fig. 2
provides an overview of PALM to test generation.
                                                                                           2) Path Minimization: The number of possible execution
                                                                                        paths in a method grows exponentially with the number of
B. Step-I: Condition Chains Collection
                                                                                        branches, making it impractical to generate test cases for all
   We aim to generate tests that satisfy specific execution paths                       paths. To address this challenge, we aim to identify a minimal
within the focal method. To achieve this, we must collect                               set of paths that can cover all branch conditions. Our approach
the relevant condition chains and provide this information to                           decomposes the problem into two stages: path traversal and
the model. This step involves a detailed explanation of how                             set cover. During path traversal, we collect all possible paths
we traverse the focal method’s Control Flow Graph (CFG) to                              without filtering to ensure completeness. Subsequently, we
gather the necessary condition chains.                                                  formulate the problem of selecting a minimal set of paths as
   1) Path Constraints Collection: Our approach leverages                               a classic minimum set cover problem.
both the MIR and the HIR to derive conditional con-                                        Algorithm 1 details our approximate solution. It inputs a set
straints from Rust source code. Unlike existing tools like                              of path constraints, each comprising multiple condition con-
MirChecker [67], which focus on flow-sensitive security anal-                           straints, and outputs a minimal subset of these paths covering
yses, our method is specifically designed to recover high-                              all condition constraints. The algorithm greedily constructs the
level semantics for unit test generation. MIR, a simplified                             minimized set M . It begins with a set S containing all unique
version of Rust code, is typically used for flow-sensitive se-                          branch conditions to be covered. In each iteration, it selects the
curity analyses. It is constructed based on control flow graphs                         path from the original set P that covers the maximum number
                                               TABLE I: Condition Chains of wait

                                                                     Conditions
  Path
          let Err(new queue)    strict::addr(new queue)              let Err(new queue)    node.signaled.load     node.signaled.load
          = exchange            & STATE MASK != curr state           = exchange∗           (Ordering::Acquire)    (Ordering::Acquire)∗
    0           false                          —                             —                    true                      —
    1           false                          —                             —                    false                    true
    2           true                          true                           —                     —                        —
    3           true                         false                          false                 true                      —
    4           true                         false                          false                 false                    true
  ∗ Loop-Terminating constraints.


of conditions currently in S. This path is added to M , and its        (including struct/enum definitions, trait implementations), and
corresponding conditions are removed from S. The process               information from call-graph/crate-wide analyses (e.g., trait
repeats until S is empty. By solving this problem, PALM                bounds, return types). This assembled AST is then converted
significantly reduces the number of paths that need testing            to Rust source code suitable for the LLM prompt.
while ensuring complete branch coverage.
   For example, consider the function wait shown in Code 1,            D. Step-III: Prompts Design and Construction
after performing path analysis, we obtained the five condition            Once the condition chains and context for the focal method
chains illustrated in Table I. For the five paths in wait, we          are collected, we construct the prompt based on the focal
first select the path that covers the most conditions, path 4.         method body, path constraints, return values, and other contex-
Next, we choose path 0, which covers most of the remaining             tual information. To balance between overly simplistic prompts
conditions, and finally, path 2. Thus, after minimization, we          that might underestimate LLMs’ capabilities and overly com-
have selected three of the five paths marked red in Table I.           plex prompts that are impractical, we design our prompt
                                                                       by following established practices in unit test generation
C. Step-II: Context Construction
                                                                       research [68], [38] and widely-recognized experiences in using
   Previous work on generating tests using LLMs has shown              ChatGPT [69]. Our prompt consists of two main components:
that incorporating additional context in the prompt enhances           (i) the requirement description part, which explains the task
the quality of the generated tests [29]. To leverage this insight,     to LLMs, and (ii) the code context part, which includes the
we extract and incorporate relevant context through analysis.          focal method and relevant context. An example for wait is
This context is categorized into two types:                            shown in Fig. 3.
  • Structure Context: Definitions or declarations of member              Code Context. Inspired by previous work [29], [68] on
     variables, methods, and structure fields associated with the      generating tests using LLMs and leveraging the content we
     focal method. This helps the model understand the focal           have collected, the code context part includes the following
     method’s role within its class or structure.                      components: (i) focal context. This is the context related to the
  • Dependency Context: Declarations or definitions of param-          focal method. (ii) focal method. This includes the signature and
     eter types, data types, and functions directly or indirectly      the body. (iii) test context. In some cases, the test context must
     used by the focal method. This ensures the generated code         also be included, as it comprises the necessary use statements
     correctly handles external dependencies.                          and type declarations required for test execution.
   To manage token limits and reduce redundancy, we provide               Requirement Description. Based on established practices
full definitions for directly used types and methods, using only       for using ChatGPT [68], our requirement description part
relevant declarations for indirect dependencies.                       includes (i) role-playing instruction, e.g., “as a software testing
   The context extraction begins by parsing the focal file to          expert,” to prime GPT for test generation [69], [70]. (ii) task
extract use statements, global definitions, and type/function          description instructions, such as “please generate test functions
definitions, with use statements and global definitions being          based on the following guidelines:”. To ensure the chat-tuned
added to the context. If the focal method resides within a             model generates only the required test cases without other
struct, the struct’s definition and implementations (fields, asso-     descriptions, we include instructions like “provide the code in
ciated functions, directly called methods) are extracted, while        plain text format”, and “without explanations.” (iii) condition
other methods receive only signatures. Definitions of direct           chains, to ensure that the model generates appropriate test
dependencies–types and functions directly used by the focal            cases. By structuring the prompt this way, we aim to maximize
method–are added. For indirect dependencies, local variable            the model’s ability to generate high-quality unit tests.
types and function calls are extracted by analyzing each func-
tion/method’s Intermediate Representation (IR). Subsequently,          E. Step-IV: Test Generation and Repair
a crate-wide Abstract Syntax Tree (AST) parse resolves use                After constructing the initial prompt, we employ an itera-
and mod dependencies, yielding a structured representation             tive process to guide the model in generating test cases for
including trait bounds and return types. The final context             each execution path. This decomposition by individual paths
aggregates file-level use/globals, direct/indirect dependencies        facilitates a comprehensive, high-coverage test suite. Fig. 4
As a software testing expert, please generate Rust test functions                                       Test for path: !let Err(new_queue) = exchange -> node.signaled.load(Ordering::Acquire)
based on the following guidelines:
1. Provide the code in plain text format, without explanations or Markdown.                              1 #[test]
                                                                                         Requirement     2 fn test_01() {
2. ...
                                                                                         Description     3     let queue_value: *mut Waiter = INCOMPLETE_PTR;
The context for the focal function is as follows:
                                                                                                         4     let queue = AtomicPtr::new(queue_value);
// src/imp_std.rs
                                                                                                         5     let curr_queue: *mut Waiter = INCOMPLETE_PTR;
// crate name is once_cell
                                                                                                         6     wait(&queue, curr_queue);
use std::{...};
                                                                                                         7     assert_eq!(queue.load(Ordering::Relaxed), curr_queue);
const INCOMPLETE: usize = 0x0;
#[repr(align(4))]                                                                                        8 }
struct Waiter {...}                                                                                     Test for path: let Err(new_queue) = exchange -> strict::addr(new_queue) & STATE_MASK != curr_state
fn wait(queue: &AtomicPtr<Waiter>, mut curr_queue: *mut Waiter) {...}
mod strict {                                                                                            1 #[test]
    #[must_use]
                                                                               Focal                    2 fn test_02() {
    #[inline]                                                                  Context Code             3     let queue = AtomicPtr::new(RUNNING as *mut Waiter);
    pub(crate) fn addr<T>(ptr: *mut T) -> usize                                          Context        4     let curr_queue = RUNNING as *mut Waiter;
    where T: Sized, {                                                                                   5     wait(&queue, curr_queue);
        unsafe { core::mem::transmute(ptr) }                                                            6     let new_queue = queue.load(Ordering::Relaxed);
    }                                                                                                   7     assert!(strict::addr(new_queue) & STATE_MASK == RUNNING);
}                                                                                                       8}
The function to be tested is presented as follows:                                                      Test for path: let Err(new_queue) = exchange -> strict::addr(new_queue) & STATE_MASK == curr_state
fn wait(queue: &AtomicPtr<Waiter>, mut curr_queue: *mut Waiter) {...}
                                                                               Focal
Given the following constraints, potential panic-triggering statements,        Method                   -> !let Err(new_queue) = exchange -> !node.signaled.load(Ordering::Acquire)
and expected return values/types (all extracted from the function under test).
                                                                                                        -> node.signaled.load(Ordering::Acquire)
Generate test inputs that maximize the function's runtime satisfaction of                               1 #[test]
all constraints and expected outputs while considering panic conditions:                                2 fn test_03() {
// constraint: exchange matches Err(new_queue) is true                                   Requirement    3     let queue = AtomicPtr::new(INCOMPLETE_PTR);
// constraint: strict::addr(new_queue) & STATE_MASK != curr_state is false               Description    4     let curr_queue = INCOMPLETE_PTR;
// constraint: exchange matches Err(new_queue) is false                        Condition                5     let node = Waiter { ... };
// constraint: node.signaled.load(Ordering::Acquire) is false                  Chains                   6     let node_ptr = &node as *const Waiter as *mut Waiter;
// constraint: node.signaled.load(Ordering::Acquire) is true                                            7     queue.store(node_ptr, Ordering::Release);
                                                                                                        8     wait(&queue, curr_queue);
                                                                                                        9     assert_eq!(queue.load(Ordering::Acquire) as usize & STATE_MASK, COMPLETE);
Fig. 3: Structure of a PALM-generated prompt for the wait                                              10 }

function. The Requirement Description part instructs the LLM                                           Fig. 4: Example tests for wait generated by PALM, with one
and provides the target condition chain. The Code Context part                                         test shown per targeted execution path. Each test is crafted to
supplies source code along with curated contextual definitions.                                        satisfy a distinct sequence of predicates.
illustrates the test cases generated for wait using GPT-4o                                             usize‘. We then populate a prepared template with the error
mini, demonstrating the effectiveness of our approach.                                                 information and several lines of code surrounding the error.
   A significant challenge in generating test cases with LLMs                                          The model returns a corresponding change log based on the
is that the generated tests may fail to compile, compromising                                          provided prompt format. From this change log, we identify the
their effectiveness and coverage. Although truncating uncom-                                           necessary code modifications. The correction involves adding
pilable tests generated by LLMs until they achieve successful                                          the type conversion as usize, resolving the issue.
compilation [71] might appear as a plausible solution, this
                                                                                                           V. E XPERIMENT D ESIGN , R ESULTS AND D ISCUSSION
practice often results in tests that are incomplete or even
semantically invalid, consequently leading to diminished code                                             We address the following RQs in our evaluation:
coverage. A more robust solution is leveraging the model                                                  • RQ 1. Effectiveness. How effective is PALM in gener-
to fix compilation errors. Two established methods are: (i)                                                  ating high-quality unit tests compared with baselines?
providing the error information and context to the model,                                                 • RQ 2. Ablation Study. What is the impact of condition
allowing it to regenerate the tests until they compile or a limit                                            chains, context, and iterative compilation error repair on
is reached [68]; and (ii) providing the error information and                                                the effectiveness of generated unit tests?
code snippets to the model while requesting a change log,                                                 • RQ 3. Practical Usability. How is PALM’s usability for
which is then used to replace the erroneous code [61].                                                       real world applications?
   PALM adopts the second method for fixing compilation                                                   Experiment Settings. All our evaluations were conducted
errors, as regenerating tests may inadvertently alter error-                                           on a system equipped with an Intel Core i7-13700k processor,
free parts. First, we extract error information and relevant                                           64GB of RAM, running Ubuntu 24.04. The implementation
code snippets from the compilation messages. For each error,                                           of the path analysis and context extraction components of the
we construct a prompt instructing the model to generate a                                              PALM approach is based on Rust version nightly-2024-07-
change log based on this information. The code replacements                                            21. We validated PALM on GPT-4o mini [31], an advanced
are extracted from the model’s response and applied before                                             language model developed by OpenAI, designed for faster and
recompiling. This process iterates until the error is resolved or                                      more efficient natural language processing tasks.
the iteration limit I is reached. To prevent the repair process                                           Evaluation Metrics. Based on previous work in test gener-
from becoming excessively time-consuming, we also set an                                               ation [68], [29], [71], we have selected the following metrics:
upper limit E on the number of errors to be fixed for each                                              1) # Tests: The number of generated tests for a project.
test function. In our experiments, we set E and I to 10 and 3,                                          2) Comp Pass: The proportion of tests that can compile.
respectively. Our prompt design is inspired by prior work on                                            3) Exec Pass: The proportion of tests that successfully
using LLMs to fix Rust compilation errors [61], but we have                                                 execute and pass.
streamlined the repair process to improve efficiency.                                                   4) Line & Branch Coverage: This metric reflects the effec-
   Fig. 5 illustrates fixing a compilation error in a test gen-                                             tiveness of the whole generated test suites. Line coverage
erated for the wait function. Initially, we compile the test                                                is defined as the ratio of the number of lines of code
and encounter a compilation error. We extract the error’s                                                   executed to the total number of lines of code in the
location, line number, and message from the compiler output.                                                project after running all generated tests. Similarly, branch
In this example, the error occurs at line 4, with the message:                                              coverage is the ratio of the number of branches covered
error[E0369]: no implementation for ‘*mut imp::Waiter &                                                     to the total number of branches.
                              Error                                                                 Correct                                                  TABLE II: Benchmark Crates
 1 #[test]                                                                1 #[test]
 2 fn test_03() {                                                         2 fn test_03() {
 3     let queue = AtomicPtr::new(INCOMPLETE_PTR);                        3     let queue = AtomicPtr::new(INCOMPLETE_PTR);
 4     let curr_queue = INCOMPLETE_PTR;                                   4     let curr_queue = INCOMPLETE_PTR;                         Crate        Description                                   Downloads   # Files   LOC
 5     let node = Waiter { ... };                                         5     let node = Waiter { ... };
 6     let node_ptr = &node as *const Waiter as *mut Waiter;              6     let node_ptr = &node as *const Waiter as *mut Waiter;
 7     queue.store(node_ptr, Ordering::Release);                          7     queue.store(node_ptr, Ordering::Release);
 8     wait(&queue, curr_queue);                                          8     wait(&queue, curr_queue);                                base64       Base64 decoding and encoding                  567M        30        5k
 9     assert_eq!(queue.load(Ordering::Acquire)                           9     assert_eq!(queue.load(Ordering::Acquire) as usize
                  & STATE_MASK, COMPLETE);                                                 & STATE_MASK, COMPLETE);                      bytes        Utility library for working with bytes        347M        33        6k
10 }                                                                     10 }
                                                                                                                                         fastrand     Random number generator                       302M        5         833
                Compilation                                                                                                              hashbrown    Rust port of SwissTable hash map              629M        35        11k
error[E0369]: no implementation for `*mut imp::Waiter & usize`                                           Code
  --> src/test.rs:9:46                                                                                   Replacement                     http         Library of common HTTP types                  304M        34        10k
   |
13 | assert_eq!(queue.load(Ordering::Acquire) & STATE_MASK, COMPLETE);
   |            ----------------------------- ^ ---------- usize
                                                                                                                                         indexmap     Pure-Rust hash table                          486M        31        9k
                                                                         ChangeLog: test.rs
   |
   |
                |
                *mut imp::Waiter
                                                                                                                                         once cell    One-time initialization for globals           439M        20        2k
                                                                         OriginalCode@7 - 10:
                                                                         [07]     queue.store(node_ptr, Ordering::Release);              qsv          Blazing-fast Data-Wrangling toolkit           225K        217       85k
 <error message>                                                         [08]     wait(&queue, curr_queue);
 #[test]                                                                 [09]     assert_eq!(queue.load(Ordering::Acquire)               quote        Turn Rust syntax tree into source code        582M        19        2k
 fn test_03() { <code> }                                                                     & STATE_MASK, COMPLETE);
 Instructions: ...
                                                                         [10] }                                                          rand         Random generators                             516M        60        9k
 Format instructions: ...
 ChangeLog:K@<file >
                                                                         FixedCode@7 - 10:
                                                                         [07]     queue.store(node_ptr, Ordering::Release);
                                                                                                                                         regex        Search strings for matches of a regex         432M        222       97k
 OriginalCode@M - N:                                                     [08]     wait(&queue, curr_queue);
 [M] <white space > <original code line >                                [09]     assert_eq!(queue.load(Ordering::Acquire) as usize
                                                                                                                                         ryu          Pure Rust implementation of Ryū              418M        29        3k
 FixedCode@M - N:                                                                            & STATE_MASK, COMPLETE);
 [M] <white space > <fixed code line >                                   [10] }                                                          serde        Framework for serializing and deserializing   517M        188       31k
                                                                                                                                         serde json   JSON serialization file format                451M        70        17k
                                                                                                                                         strsim-rs    String similarity metrics                     390M        3         1k
Fig. 5: The iterative repair process. 1) Capture the error
message and surrounding code. 2) Prompt the LLM to generate                                                                                Results. Table III and IV present the comparative findings.
a change log for a minimal fix. 3) The change is applied, and                                                                           While classic tools (RustyUnit, RuMono) achieve high com-
the code is recompiled. This loop continues until compilation                                                                           pilation rates on simpler tests, PALM emerges as the clear
succeeds or a predefined budget is exhausted.                                                                                           leader among all LLM-based methods. It consistently achieves
   Subject Programs. We selected 15 open-source Rust crates                                                                             the highest compilation pass rate in this category, while
from crates.io [72] and GitHub to serve as our subject pro-                                                                             maintaining a high and stable execution pass rate that is com-
grams. These projects are chosen to form a challenging and                                                                              petitive with or superior to other LLM baselines across most
representative benchmark, selected for their maturity, high                                                                             projects. For instance, on hashbrown, PALM’s compilation
popularity (most with over 300 million downloads), and do-                                                                              rate (41.19%) is over 6 times that of SymPrompt (6.63%). In
main diversity. They cover a wide range of applications, from                                                                           terms of code coverage (Table IV), PALM’s superiority is even
data serialization and complex data structures to low-level                                                                             more pronounced. It substantially surpasses all other baselines,
systems programming and core algorithms, aiming to support                                                                              both classic and LLM-based, across nearly every project. The
the generalizability of our findings. In total, we selected 4145                                                                        performance gap is often dramatic; on http, PALM achieves
focal methods to ensure a robust evaluation. Table II provides                                                                          74.75% line coverage, more than 40 percentage points higher
detailed information about these 15 crates, including their                                                                             than the next best LLM-based tool, SymPrompt (29.07%).
download counts, sizes, and other relevant characteristics.                                                                             When benchmarked against these manually-authored tests,
   Baselines. We selected five baselines to compare with                                                                                the original project tests exhibited an average line coverage
PALM: two classic tools and three LLM-based approaches.                                                                                 of 70.94% and an average branch coverage of 66.47%. In
The classic tools are RustyUnit [8], a search-based test suite                                                                          comparison, tests generated by PALM surpassed the line
generator for Rust, and RuMono [73], a fuzzing-based tool that                                                                          coverage of the original tests in almost half of the evaluated
extends RULF [74] with capabilities for generic APIs. The                                                                               projects, achieving an average of 72.30%. Notably, PALM-
LLM-based baselines include: RUG [75], which lacks path-                                                                                generated tests demonstrated superior branch coverage in the
guided prompts and LLM-based repair, relying on fuzzing                                                                                 vast majority of projects, averaging 69.49%.
to enhance coverage; SymPrompt [71], which differs from                                                                                    Discussion. The distinct test generation philosophies in-
PALM by using AST-based path analysis (instead of CFG-                                                                                  fluence output characteristics: RustyUnit (SBST) produces
based) and truncating failing tests (instead of repairing them);                                                                        comprehensive, longer unit tests, while LLM-based tools gen-
and ChatTester [68], which contrasts with PALM’s path-                                                                                  erate shorter tests, often targeting single input conditions.
decomposed generation and patch-based repair by using one-                                                                              RuMono’s fuzz target output scales with API density. We
shot generation and full regeneration for fixes.                                                                                        observed that, unlike the prolonged execution of RuMono,
                                                                                                                                        LLM-based tools typically complete test generation in 2-
A. RQ1: Effectiveness of PALM for Unit Test Generation                                                                                  3 hours, varying with project scale and code complexity.
   We evaluated PALM against five baseline tools on the                                                                                 A noteworthy observation is PALM’s compilation pass rate,
subject crates detailed in Table II. For RuMono, we set a                                                                               which is lower than that of classic tools like RustyUnit and
24-hour timeout. We first measured the number of generated                                                                              RuMono. This is a direct consequence of PALM’s ambition
test artifacts (fuzz targets for RuMono; unit tests for others).                                                                        to generate more complex, human-like tests. Such tests often
We then assessed their compilation success rates. Successfully                                                                          require intricate object setups and API call sequences, which
compiled tests were subsequently executed to determine their                                                                            can trigger the LLM’s inherent limitations, such as factual
pass rates. Finally, we measured line and branch coverage                                                                               inaccuracies or “hallucinations,” making them more prone to
for each project. Furthermore, we quantified the coverage                                                                               compilation errors in a strict language like Rust [76]. This
achieved by the manually-authored unit tests within each                                                                                challenge motivates our inclusion of the iterative self-repair
selected project. Given the mature, popular, and extensively                                                                            mechanism (Section IV-E). As shown in our ablation study
utilized nature of these projects, their existing test coverage                                                                         (Table V), this mechanism is highly effective at boosting the
levels were considered indicative of high-quality, manually-                                                                            final compilation rate and is essential for achieving high test
derived test suites achievable in practice.                                                                                             coverage. While the compilation rate is lower than classic
                            TABLE III: Assessment of Generated Tests: Volume, Compilation, and Execution Success.
                                              # Tests                                                  Comp Pass (%)                                       Exec Pass (%)
 Crate
                RustyUnit   RuMono     RUG      SymPrompt   ChatTester   PALM    RustyUnit   RuMono   RUG     SymPrompt   ChatTester   PALM    RUG     SymPrompt   ChatTester   PALM
 base64            50         16       228          187       266         629      100.0      100.0   46.05     27.81       40.60      48.38   72.38     57.69       87.96      77.78
 bytes             47         300        —a          364      815        1189      51.06      57.67    —        54.40       51.41      79.62    —        82.86       81.25      83.05
 fastrand          50          13       195          66        162        223      100.0      100.0   55.38     77.27       54.94      95.96   85.19     86.27       70.45      90.34
 hashbrown         50          —       1391          347      1310       1527      78.00       —      30.70      6.63       34.73      41.19   89.23     69.57       88.13      82.54
 http              —          213      1870          673      1322       2643       —         48.83   1.12      29.42       41.75      53.35   71.43     88.38       91.85      84.37
 indexmap          48          —       1792          335      1619       1876      100.0       —      37.72     16.72       35.89      50.23   90.38     85.71       91.57      86.02
 once cell         42           8         7          103       211        299      40.48      75.00   28.57     45.54       43.13      89.24   50.00     91.34       84.62      90.94
 qsv               47          —       1117         1989      1450       6483      86.77       —      45.30     27.75       52.76      52.43   67.59     63.77       70.07      65.49
 quote             50          57       205          31         87        113      100.0      100.0   26.83     19.35       14.94      67.60   74.55     100.0       84.62      82.22
 rand              50          —       1139          271       622        840      76.00       —      37.49     36.90       36.82      47.38   84.31     61.00       83.84      82.10
 regex             50         130      3732         1004      3359       8251      94.00      96.92   37.73     27.39       40.19      35.48   83.59     72.91       84.59      85.05
 ryu               50           6        90          115       188        512      94.00      66.67   97.78     77.39       85.64      87.73   52.27     59.55       65.84      83.01
 serde             44          —       5356          954      1625       2274      79.55       —      1.72       5.97       19.57      13.32   82.61     89.47       89.94      93.40
 serde json        50         278      2449          955      2019       3116      48.00      82.09   19.44     15.81       22.44      44.19   81.09     85.74       85.98      86.09
 strsim-rs         50           9        95          85        140        345      100.0      100.0   81.05     60.00       75.00      96.52   92.21     86.27       71.43      84.42
 a
     The — symbol indicates that the tool was unable to generate tests for these projects.

tools, PALM generates a significantly larger volume of tests                                    impact of these components, designing five prompt variants:
(see Table III). This ultimately results in a substantial pool of                               (i) basic function body and task instructions; (ii) (i) + condition
valid test cases, providing the breadth needed to achieve high                                  chains; (iii) (i) + context; (iv) (ii) + (iii); (v) (iv) + LLM error
coverage. Among LLM tools, PALM’s superior compilation                                          fixing, which is PALM. This systematic approach allowed us
rates over others stem from its use of fine-grained contextual                                  to quantify the individual contributions of each method.
information and iterative self-repair of compilation errors.                                       Results. Table V details the ablation study results, revealing
   Regarding coverage, classic SBST methods can be limited                                      distinct impacts of different prompting strategies. Basic and
by initial inputs or local optima, and fuzzing often requires                                   context-only prompts generally produced fewer tests than
extensive runtime. LLMs, with their code understanding, can                                     condition chains-only prompts. Context-only prompts typically
identify unique execution paths. PALM leverages path-specific                                   yielded higher compilation success rates (except on indexmap
requirements to guide generation. While this can sometimes                                      and strsim-rs) and better test pass rates (except on once cell
be affected by conflicting constraints or model hallucina-                                      and rand). For code coverage, the general trend was context-
tions [76], potentially explaining why improvements in cover-                                   only > condition chains-only > basic prompts, though basic
age are not always substantial on every project. Nevertheless,                                  prompts occasionally surpassed condition chains-only on some
this approach, particularly its CFG-based analysis and iterative                                projects. Notably, prompts combining both context and con-
repair mechanism, is the key driver of its overall success. In                                  dition chains generally achieved higher coverage than either
contrast, the AST-based analysis and test truncation strategy                                   component in isolation. The efficacy of model self-iteration
of SymPrompt proved less effective in the complex Rust                                          for repair was evident when comparing configurations with
environment. PALM’s strategy of integrating static analysis for                                 and without this feature, showing universal improvements in
comprehensive function targeting, combined with its higher                                      compilation rates–exceeding 100% in some instances–which
compilation success rates, allows it to generate tests for a                                    consequently boosted test pass rates and coverage. Ultimately,
broader set of functions within a project. This synergy of                                      the full PALM methodology demonstrated superior perfor-
program analysis and effective compilation error correction                                     mance, achieving the highest compilation rates and crucially,
enables PALM to achieve substantially higher coverage than                                      attaining the highest coverage across all evaluated projects.
alternatives, validating its approach and underscoring its po-                                     Discussion. Our ablation study reveals that basic and
tential for practical application. Across the 15 evaluated crates,                              context-only prompts, which direct the model to generate an
PALM and the human-authored test suites each achieved                                           entire test suite in one pass, typically produce fewer tests than
superior line coverage in roughly half of the instances. More-                                  condition chain-inclusive prompts designed to generate tests
over, PALM demonstrated higher branch coverage in 10 out                                        for specific execution paths. Context-only prompts, by incor-
of the 15 crates, further underscoring its practical utility in                                 porating the target method’s external dependencies, enable the
software testing workflows. Instances where PALM did not                                        generation of tests that correctly utilize these dependencies,
attain superior line coverage were predominantly attributed to                                  thus achieving higher compilation success rates. Although
the extensive use of macros within those projects, which posed                                  condition chain-driven prompts are theoretically poised for
challenges for effective test generation. Conversely, PALM’s                                    higher coverage, their increased propensity for compilation
consistent outperformance in branch coverage is likely due to                                   failures often leads to final coverage figures lower than those
its design focus on leveraging branch condition constraints to                                  from context-only prompts. This finding is largely consistent
guide test generation, thereby often achieving more thorough                                    with research on the SymPrompt technique for the GPT-4
exploration of conditional logic than typical manual efforts.                                   model [71], suggesting that for dialogue-tuned models like
                                                                                                GPT-4, contextual information contributes more significantly
B. RQ2: Ablation Study                                                                          to effective test generation than explicit condition chains.
   To optimize test generation, we integrated path constraint-                                  Nevertheless, combining both context and condition chains
based condition chains, focal context, and LLM-driven error                                     generally yields further improvements across most projects.
resolution. We conducted an ablation study to evaluate the                                      Moreover, leveraging LLMs to repair compilation errors sub-
TABLE IV: Evaluation of Test Suite Effectiveness via Code Coverage. Bold indicates the best result among all automated test
generation tools. Manual coverage is provided as a human-authored reference benchmark.
                                               Line Cov. (%)                                                              Branch Cov. (%)
 Crate
                RustyUnit   RuMono     RUG      SymPrompt      ChatTester   PALM    Manual   RustyUnit   RuMono   RUG       SymPrompt       ChatTester   PALM    Manual
 base64            6.36      15.67     58.87      43.33          21.65      58.14   93.49      10.58      17.42   58.17        41.18          19.08      58.24   87.50
 bytes            27.53       9.01       —a       56.17          13.40      83.93   86.48      28.98      10.98     —          48.98          10.00      75.14   73.31
 fastrand         58.59      35.02     60.61      61.28          18.86      93.94   63.64      62.50       7.50   66.96        52.63          18.42      93.75   49.11
 hashbrown         7.16        —       47.50       7.75           3.31      69.88   53.40      5.22         —     54.21         8.00          4.86       63.69   60.57
 http               —        33.94     11.85      29.07           1.77      74.75   64.38       —         31.75   11.31        29.03          2.84       73.51   59.35
 indexmap          8.23        —       66.77      18.70           2.63      74.30   56.96      8.84         —     60.86        14.77          2.86       69.47   52.95
 once cell        42.96      11.93      1.68      50.84           8.11      93.79   80.43      49.34      11.54    1.68        43.82           7.87      92.13   75.00
 qsv               9.81        —       28.94      38.43          14.36      62.18   78.83      8.74         —     28.26        26.65          9.89       54.62   69.49
 quote             3.24       8.18     40.91      16.36           4.48      77.27   50.44      3.24       8.00    48.00        22.22          4.41       70.34   57.69
 rand             14.13        —       74.29      42.59           5.76      61.83   78.06      14.44        —     68.06        36.97           5.37      54.62   66.52
 regex            12.21      53.20     46.77      31.75           6.16      55.49   59.64      10.99      49.70   47.82        32.12           8.72      55.61   54.22
 ryu              37.80      98.27     68.66      74.65          68.82      93.23   100.0      28.92      98.04   61.76        65.57          73.22      90.16   98.04
 serde             8.11        —        1.35      14.38           4.90      19.46   57.00      9.39         —      1.61        13.59          6.81       20.41   55.46
 serde json       13.88      39.45     43.36      21.34           5.72      66.65   66.72      16.79      40.12   50.12        23.18           7.02      73.28   64.01
 strsim-rs        64.72      82.78     95.00      80.52          63.61      99.72   74.17      50.00      81.82   88.64        71.43          54.55      97.40   73.86
 a
     The — symbol indicates that the tool was unable to generate tests for these projects.

stantially boosts compilation rates on several projects, thereby                       D. Qualitative Analysis of Failure Cases
markedly enhancing the quality of the generated tests.                                    While PALM demonstrates strong performance, its reliance
C. RQ3: Practical Usability                                                            on an LLM’s heuristic understanding means it is not infallible.
   To assess the practical usability of PALM-generated unit                            Failures typically arise when the LLM struggles to synthesize
tests, we compared their achieved coverage against the existing                        concrete, valid test code from the abstract path constraints
test coverage in 15 projects, as detailed in Table IV. We                              provided by our analysis. This synthesis requires inferring
then selected tests that demonstrably increased coverage and                           a complete test scenario, including object setup and precise
submitted them as PRs to these open-source projects.                                   API call sequences. We identified two primary failure pat-
   Results. The outcomes of the submitted PRs are summa-                               terns: compilation failures due to misunderstanding language-
rized in the final row of Table V, where ‘P’ denotes PRs still                         specific semantics, and path constraint satisfaction failures due
pending developer feedback. In total, 91 tests were submitted                          to a lack of causal reasoning.
across 8 projects. Of these, 80 were accepted and merged, 5 1 pub fn choice<I>(iter: I) -> Option<I::Item>
were rejected, and 6 are currently awaiting developer feedback. 2 where I: IntoIterator, I::IntoIter: ExactSizeIterator, {
                                                                 3    with_rng(|r| r.choice(iter))
   Discussion. The target projects for this evaluation are popu- 4 }
lar, widely used, and actively maintained, possessing high pre-
                                                                             Code 2: Compilation failure example.
existing test coverage that can be considered representative of
diligent human development efforts. Despite this high baseline,      A common compilation failure mode involves the LLM ap-
PALM successfully generated tests that increased coverage in plying programming patterns from other languages that violate
8 of these projects. Among these, we contributed two PALM- Rust’s strict ownership rules. For example, when testing the
generated unit tests to hashbrown, an officially maintained choice function in Code 2, which takes an iterator, PALM’s
Rust crate that serves as the underlying implementation for LLM component might generate code that moves a Vec into
HashMap and HashSet in the Rust standard library, thereby the function and then attempts to reuse it, triggering a “use
enhancing its test coverage and completeness. For projects of moved value” error. The LLM fails because its general
where PALM did not identify coverage-enhancing tests, our knowledge, trained heavily on languages like Python or Java
investigation revealed extensive use of macros, a feature for where such reuse is common, overrides the specific constraints
which PALM currently lacks specialized handling, thus limit- of Rust’s move semantics.
ing its effectiveness in these specific contexts.
   Developer interactions during the PR process indicated 1 fn reserve_inner(&mut self, additional, allocate) -> bool {
                                                                 2    if kind == KIND_VEC {
that while some expressed caution towards LLM-generated 3                 unsafe {
code, most were receptive, provided the tests were meaningful 4               let off = self.get_vec_pos();
and demonstrably increased coverage. The 5 rejected tests 5                   if self.capacity() - self.len() + off >=
                                                                                   additional && off >= self.len() {
were primarily due to developers seeking additional value 6                   } else {
beyond mere coverage improvement or perceiving the tests 7                        if !allocate {
as redundant. Several tests were merged after incorporating      8                    return false;
                                                                 9                }
developer feedback regarding code style, test descriptions, or 10             }
usage patterns. Feedback is still pending for the remaining 11                return true;
6 tests. Overall, 87.91% of the submitted tests have been 12              }
                                                                13    }
merged by developers. Considering only the tests that received 14 }
developer review, the merge rate is 94.12%, underscoring the
                                                                            Code 3: Path constraint failure example.
practical utility and acceptance of PALM-generated tests.
                                                                 TABLE V: Ablation Result of PALM
 Method                  Metric            base64   bytes   fastrand   hashbrown   http    indexmap   once cell   qsv     quote   rand    regex   ryu     serde   serde json   strsim-rs
                         # Tests            212      561      137        1073      1015     1219        185       1091     52      451    1199     126    1056      1438         109
                         Comp Pass (%)     36.32    49.91    40.88       18.08     36.85    37.90      31.35      49.22   23.08   51.22   43.62   69.84   23.30     19.61       72.48
 Basic Prompt            Exec Pass (%)     96.10    83.93    83.93       77.60     91.98    95.02      89.66      74.10   100.0   85.28   89.29   57.95   93.90     87.27       88.61
                         Line Cov. (%)      7.59     8.84    16.84       3.42      5.05     1.03       3.82       15.90   12.16   9.97    6.30    49.29   3.50      5.10        64.44
                         Branch Cov. (%)    7.65     8.94    13.16       5.03      5.37     1.36       4.49       10.80   11.86   8.40    7.59    49.73   4.93      6.37        58.44
                         # Tests            569     1042      207        1632      2311     1900        270       4936     85      769    2643     409    1873      2978         317
                         Comp Pass (%)     30.23    41.84    41.06       13.66     28.26    29.53      23.33      43.35   12.94   42.78   35.34   73.84   16.60     15.28       82.62
 Condition Chains Only   Exec Pass (%)     70.35    78.21    76.47       81.17     86.68    89.48      82.54      63.50   81.82   79.94   79.44   79.47   90.68     85.62       78.24
                         Line Cov. (%)     31.09    18.35    15.83        2.66     10.93     2.76       0.72      25.17   15.95   11.38    7.09   58.58    3.60      4.81       68.61
                         Branch Cov. (%)   32.94    12.57    14.06        4.18     11.35     4.30       1.12      18.49   16.21    9.66    9.03   54.10    5.42      6.92       62.34
                         # Tests            216      647      146         990      1285     1187        209       1274     69      479    1307     160    1056      1564         117
                         Comp Pass (%)     47.22    68.32    85.62       17.58     50.12    20.64      61.24      59.03   23.19   50.94   47.59   83.12   23.30     31.91       71.79
 Context Only            Exec Pass (%)     84.31    83.94    77.60       81.61     88.82    90.61      95.31      73.01   87.50   68.85   81.03   69.92   93.90     89.65       85.71
                         Line Cov. (%)     35.74    57.01    82.83       15.71     48.64    22.71      62.77      42.92   40.91   44.46   36.47   65.20    3.50     31.65       68.61
                         Branch Cov. (%)   34.12    49.72    73.68       18.44     47.61    20.90      57.30      34.57   33.33   41.18   37.70   65.03    4.93     37.05       64.94
                         # Tests            629     1189      223        1527      2643     1876        299       6483     113     840    3134     512    2274      3116         345
                         Comp Pass (%)     40.38    59.71    90.58       19.19     45.48    25.16      56.52      50.96   25.66   47.02   40.62   73.44   13.28     26.70       86.96
 PALM w/o fix            Exec Pass (%)     62.99    78.45    82.67       79.52     84.36    78.60      89.94      65.07   89.66   70.13   79.73   76.33   93.38     85.36       81.00
                         Line Cov. (%)     57.28    63.79    91.89       17.92     60.72    33.01      68.02      61.47   44.45   47.30   43.88   74.33   16.54     31.28       89.44
                         Branch Cov. (%)   58.24    58.94    92.19       22.63     57.95    30.53      66.29      54.25   37.04   45.38   43.06   73.77   15.27     35.86       84.42
                         # Tests            629     1189      223        1527      2643     1876        299       6483     113     840    3134     512    2274      3116         345
                         Comp Pass (%)     48.38    79.62    95.96       41.19     53.35    50.23      89.24      52.43   67.60   47.38   54.22   87.73   13.32     44.19       96.52
 PALM                    Exec Pass (%)     77.78    83.05    90.34       82.54     84.37    86.02      90.94      65.49   82.22   82.10   85.05   83.01   93.40     86.09       84.42
                         Line Cov. (%)     58.14    83.93    93.94       69.88     74.75    74.30      93.79      62.18   77.27   61.83   55.49   93.23   19.46     66.65       99.72
                         Branch Cov. (%)   58.24    75.14    93.75       63.69     73.51    69.47      92.13      54.62   70.34   54.62   55.61   90.16   20.41     73.28       97.40
                         # Tests acc/rej    P(1)    12/0      19/0        2/0       —        39/0        3/0       —       —       5/5     —       —       —         —           P(5)


   A more subtle failure occurs when a test compiles but does                                fundamental trade-off between formal precision and practical
not trigger the intended path because the LLM fails to reason                                applicability. We do not claim that LLMs are superior to
about the side effects of API calls. Consider satisfying the con-                            dedicated solvers; for mathematical or logical constraints, the
dition off >= self.len() inside the reserve_inner                                            formal guarantees of SMT solvers are unparalleled. PALM,
function in Code 3. Satisfying this condition requires more                                  being heuristic, may fail on complex arithmetic constraints,
than just generating input values; it demands a sequence                                     a limitation we acknowledge. However, PALM’s advantages
of state-manipulating actions. A correct test must first call                                emerge precisely where formal methods often falter: in han-
a method like self.advance() to modify the object’s                                          dling the semantic and environmental complexities of real-
internal state (off) before calling reserve_inner. The                                       world code. For instance, as shown in our motivating example
LLM often fails here because it cannot infer this non-local,                                 (Section III), PALM successfully generates tests for func-
causal dependency between an action (advance()) and its                                      tions involving concurrency primitives, which are notoriously
future consequence on an internal state check, highlighting a                                difficult for concolic engines to handle without specialized,
fundamental gap in reasoning about stateful object lifecycles.                               manually-crafted models. More broadly, LLMs excel at satis-
                                                                                             fying “semantic” constraints–such as correct API usage, com-
E. Cost and Token Analysis                                                                   plex object instantiation, and idiomatic patterns–by leveraging
   The practical adoption of LLM-based tools is intrinsically                                the vast knowledge in their training data. The high compilation
linked to their computational cost. To provide a clear picture                               success rates and positive developer feedback (Section V-C)
of PALM’s resource consumption, we analyzed its token                                        from our study underscore this unique capability.
usage and associated costs during our evaluation. On average,                                   Furthermore, PALM offers crucial advantages in scalability
generating a single unit test required approximately 1500                                    and engineering pragmatism. It directly mitigates the path
input tokens and 300 output tokens. When the iterative repair                                explosion problem, a key limitation of concolic execution,
mechanism was triggered, each repair round consumed an                                       through its path minimization technique (Section IV-B2). By
additional 800 tokens on average. For the entire evaluation                                  strategically selecting a diverse but minimal set of paths, it
across all 15 projects, which involved analyzing approximately                               avoids the costly endeavor of exhaustive path exploration.
40,000 lines of code and generating around 65,000 test cases                                 This, combined with a significantly lower engineering over-
(including the full ablation study), the total consumption was                               head compared to developing and maintaining a symbolic
approximately 800 million tokens. At the prevailing rates for                                execution engine, positions PALM as a more pragmatic and
the model used, this translated to a total cost of about $300.                               readily adaptable alternative. In essence, PALM trades for-
This analysis demonstrates that while not trivial, the cost is                               mal precision on narrow constraints for superior handling of
manageable for comprehensive academic studies and could be                                   semantic complexity, greater scalability, and broader applica-
viable for integration into industrial pipelines, especially when                            bility in modern software systems.
applied selectively to critical or complex code modules.
                                                                                                                       VII. T HREATS TO VALIDITY
                                  VI. D ISCUSSION                                               Threats from Model Selection. Our study relies exclu-
  A core design choice in PALM is to use an LLM as a                                         sively on a single LLM, GPT-4o mini. This presents a threat
heuristic constraint solver rather than a traditional SMT-based                              to external validity, as our findings may not generalize to other
solver used in concolic execution. This choice embodies a                                    models with different architectures or training data. We chose
GPT-4o mini for its strong performance and cost-effectiveness,     effectively test Rust library APIs while ensuring type safety
but acknowledge that evaluating PALM with a diverse range          and proper API call chaining [13]. Unlike these approaches,
of LLMs is a crucial next step. The core techniques of PALM,       we do not use classic constraint solvers to follow specific
however, are model-agnostic and designed to be adaptable.          paths. Instead, we provide the source code of the focal method
   Subject Programs Selection. Our subject crates were se-         to the LLM, delegating the constraint-solving problem to the
lected from 15 popular and actively maintained projects on         LLM, which then generates the tests.
crates.io [72] and GitHub to cover diverse domains. This              LLM based Test Generation. Athenatest fine-tunes pre-
selection aims to enhance the applicability of our findings.       trained transformers using paired method-test data and con-
However, we acknowledge that a study based on 15 projects,         cludes that adding more context in prompts helps generate
despite their diversity and complexity, may not fully represent    high-coverage tests [29]. Mathur et al. utilize T5 and GPT-3 to
the entire Rust ecosystem. Future work should expand this          extract the conversation’s context and topic, subsequently gen-
evaluation to an even larger and more varied set of crates.        erating test cases [81]. Codamosa employs Pynguin, an SBST
   Scope of Evaluation. Our evaluation primarily focuses on        tool for Python, and iteratively invokes Codex to generate ad-
code coverage, a widely-used metric for test suite comprehen-      ditional test cases for methods with low coverage [82]. Yuan et
siveness. While high coverage is a prerequisite for effective      al. perform the first empirical study to evaluate ChatGPT’s ca-
bug finding, a large-scale study on bug detection effectiveness    pability of unit test generation and propose ChatTester, which
was beyond the scope of this work. We consider this an             leverages ChatGPT itself to improve the quality of its gener-
important direction for future research.                           ated tests [68]. MuTAP enhances LLM-generated tests through
                                                                   mutation testing and augmented prompts, demonstrating a
                   VIII. R ELATED W ORK                            significant increase in bug detection probability [83]. These
   Search Based Software Testing (SBST). Randoop uses              methods rely on static prompts, whereas PALM combines
coverage-guided random test generation for Java and includes       program analysis with LLMs to generate different prompts for
sanity-checking oracles to detect common bugs like Null-           different paths, guiding the model to produce high-coverage
PointerExceptions [77], [10]. EvoSuite is a framework that         test suites. RUG [75] introduces a semantic-aware bottom-up
leverages SBST to generate tests for Java. It supports mutation    approach to leverage LLMs for generating unit tests in Rust,
testing and coverage-guided random test generation [9], [41],      addressing compilation errors through context decomposition
[78]. CITRUS is a C++ unit testing tool that generates high-       and enhancing test coverage by integrating coverage-guided
coverage test suites by producing random sequences of method       fuzzing, achieving results comparable to human-written tests.
calls [12]. It is capable of handling challenging technical        SymPrompt [71] is the method most similar to PALM, as it
issues such as template instantiation. Pynguin utilizes SBST       generates corresponding prompts for different paths. However,
to generate regression tests for Python, aiming to ensure code     unlike SymPrompt, we analyze the CFG instead of AST to
reliability and detect regressions effectively [11]. RustyUnit     explore the program’s paths better. Meanwhile, instead of
introduces a search-based approach for automated unit test         merely truncating the model’s output, we leverage the model
generation in Rust, utilizing a compiler wrapper and a many-       to fix compilation errors in the tests.
objective genetic algorithm to achieve high code coverage [8].
PALM conceptually aligns with coverage-driven SBST meth-                                 IX. C ONCLUSION
ods, as both aim to generate test cases guided by coverage cri-
teria. While SBST methods typically employ random search or          This paper introduces PALM, which combines program
optimization algorithms to identify suitable test inputs, PALM     analysis with large language models to generate high-coverage
directs an LLM to generate inputs that satisfy constraints         unit tests. PALM employs path analysis to obtain the condition
specified for a particular execution path.                         chain for each path within the focal method. It then generates
   Symbolic Execution based Test Generation. KLOVER is             a prompt specific to each path by incorporating the context of
the first symbolic execution and automatic test generation tool    the function. The model iteratively generates tests and, using
for C++ [79], [15]. It is built on top of the symbolic execution   provided error information suggests fixes for tests that fail to
engine KLEE [80] and extends it to support C++. Garg et al.        compile. Our experiments with GPT-4o mini demonstrate that
propose a flexible testing framework that alternates between       PALM significantly improves both the compilation pass rate
directed-random search and concolic execution to automati-         and coverage of tests generated by large language models.
cally cover hard-to-reach portions of the program [14]. Chen
et al. propose a host-target split concolic testing method for                         ACKNOWLEDGMENT
embedded executables, performing symbolic execution on a
resource-rich host and concrete execution on the target device,      We thank the anonymous reviewers for their helpful feed-
coordinated via cross-debugging, enabling testing without          back and suggestions. This work was supported in part by the
source code in the real environment [16]. SyRust leverages         National Natural Science Foundation of China under Grant
a novel logical encoding of Rust’s ownership type system           No. 62372225 and No. 62172209, and by the Fundamental Re-
and polymorphic types to synthesize semantically valid test        search Funds for the Central Universities (No. 020214380131
cases, employing symbolic execution and constraint solving to      and No. ZZKT2025A10).
                               R EFERENCES                                         [22] S. Krishnamoorthy, M. S. Hsiao, and L. Lingappan, “Tackling the
                                                                                        path explosion problem in symbolic execution-driven test generation for
 [1] S. Planning, “The economic impacts of inadequate infrastructure for                programs,” in 2010 19th IEEE Asian Test Symposium. IEEE, 2010, pp.
     software testing,” National Institute of Standards and Technology, vol. 1,         59–64.
     no. 2002, 2002.                                                               [23] A. Kolchin, “A novel algorithm for attacking path explosion in model-
 [2] G. J. Myers, C. Sandler, and T. Badgett, The art of software testing.              based test generation for data flow coverage,” in 2018 IEEE First
     John Wiley & Sons, 2011.                                                           International Conference on System Analysis & Intelligent Computing
 [3] S. Siddiqui, Learning Test-Driven Development. ” O’Reilly Media,                   (SAIC). IEEE, 2018, pp. 1–5.
     Inc.”, 2021.                                                                  [24] L. De Moura and N. Bjørner, “Z3: An efficient smt solver,” in Inter-
 [4] K. Beck, Test driven development: By example.              Addison-Wesley          national conference on Tools and Algorithms for the Construction and
     Professional, 2022.                                                                Analysis of Systems. Springer, 2008, pp. 337–340.
 [5] E. Daka and G. Fraser, “A survey on unit testing practices and problems,”     [25] R. Baldoni, E. Coppa, D. C. D’elia, C. Demetrescu, and I. Finocchi,
     in 2014 IEEE 25th International Symposium on Software Reliability                  “A survey of symbolic execution techniques,” ACM Computing Surveys
     Engineering. IEEE, 2014, pp. 201–211.                                              (CSUR), vol. 51, no. 3, pp. 1–39, 2018.
 [6] P. Runeson, “A survey of unit testing practices,” IEEE software, vol. 23,
                                                                                   [26] C. Cadar and K. Sen, “Symbolic execution for software testing: three
     no. 4, pp. 22–29, 2006.
                                                                                        decades later,” Communications of the ACM, vol. 56, no. 2, pp. 82–90,
 [7] P. S. Kochhar, F. Thung, and D. Lo, “Code coverage and test suite                  2013.
     effectiveness: Empirical study with real bugs in large systems,” in 2015
     IEEE 22nd international conference on software analysis, evolution, and       [27] V. Chipounov, V. Kuznetsov, and G. Candea, “S2e: A platform for in-
     reengineering (SANER). IEEE, 2015, pp. 560–564.                                    vivo multi-path analysis of software systems,” Acm Sigplan Notices,
                                                                                        vol. 46, no. 3, pp. 265–278, 2011.
 [8] V. Tymofyeyev and G. Fraser, “Search-based test suite generation for
     rust,” in International Symposium on Search Based Software Engineer-          [28] V. Guilherme and A. Vincenzi, “An initial investigation of chatgpt
     ing. Springer, 2022, pp. 3–18.                                                     unit test generation capability,” in Proceedings of the 8th Brazilian
 [9] G. Fraser and A. Arcuri, “Evosuite: automatic test suite generation for            Symposium on Systematic and Automated Software Testing, 2023, pp.
     object-oriented software,” in Proceedings of the 19th ACM SIGSOFT                  15–24.
     symposium and the 13th European conference on Foundations of soft-            [29] M. Tufano, D. Drain, A. Svyatkovskiy, S. K. Deng, and N. Sundaresan,
     ware engineering, 2011, pp. 416–419.                                               “Unit test case generation with transformers and focal context,” arXiv
[10] C. Pacheco and M. D. Ernst, “Randoop: feedback-directed random                     preprint arXiv:2009.05617, 2020.
     testing for java,” in Companion to the 22nd ACM SIGPLAN conference            [30] A. Deljouyi, “Understandable test generation through capture/replay
     on Object-oriented programming systems and applications companion,                 and llms,” in Proceedings of the 2024 IEEE/ACM 46th International
     2007, pp. 815–816.                                                                 Conference on Software Engineering: Companion Proceedings, 2024,
[11] S. Lukasczyk and G. Fraser, “Pynguin: Automated unit test generation               pp. 261–263.
     for python,” in Proceedings of the ACM/IEEE 44th International Con-           [31] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman,
     ference on Software Engineering: Companion Proceedings, 2022, pp.                  D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat et al., “Gpt-4
     168–172.                                                                           technical report,” arXiv preprint arXiv:2303.08774, 2023.
[12] R. S. Herlim, Y. Kim, and M. Kim, “Citrus: Automated unit testing tool        [32] A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng,
     for real-world c++ programs,” in 2022 IEEE Conference on Software                  C. Zhang, C. Ruan et al., “Deepseek-v3 technical report,” arXiv preprint
     Testing, Verification and Validation (ICST). IEEE, 2022, pp. 400–410.              arXiv:2412.19437, 2024.
[13] Y. Takashima, R. Martins, L. Jia, and C. S. Păsăreanu, “Syrust: automatic   [33] V. Sanh, A. Webson, C. Raffel, S. H. Bach, L. Sutawika, Z. Alyafeai,
     testing of rust libraries with semantic-aware program synthesis,” in               A. Chaffin, A. Stiegler, T. L. Scao, A. Raja et al., “Multitask
     Proceedings of the 42nd ACM SIGPLAN International Conference on                    prompted training enables zero-shot task generalization,” arXiv preprint
     Programming Language Design and Implementation, 2021, pp. 899–                     arXiv:2110.08207, 2021.
     913.                                                                          [34] R. Thoppilan, D. De Freitas, J. Hall, N. Shazeer, A. Kulshreshtha, H.-T.
[14] P. Garg, F. Ivančić, G. Balakrishnan, N. Maeda, and A. Gupta,                    Cheng, A. Jin, T. Bos, L. Baker, Y. Du et al., “Lamda: Language models
     “Feedback-directed unit test generation for c/c++ using concolic execu-            for dialog applications,” arXiv preprint arXiv:2201.08239, 2022.
     tion,” in 2013 35th International Conference on Software Engineering          [35] H. Le, Y. Wang, A. D. Gotmare, S. Savarese, and S. C. H. Hoi,
     (ICSE). IEEE, 2013, pp. 132–141.                                                   “Coderl: Mastering code generation through pretrained models and deep
[15] H. Yoshida, G. Li, T. Kamiya, I. Ghosh, S. Rajan, S. Tokumoto,                     reinforcement learning,” Advances in Neural Information Processing
     K. Munakata, and T. Uehara, “Klover: automatic test generation for c               Systems, vol. 35, pp. 21 314–21 328, 2022.
     and c++ programs, using symbolic execution,” IEEE Software, vol. 34,          [36] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan,
     no. 5, pp. 30–37, 2017.                                                            H. Edwards, Y. Burda, N. Joseph, G. Brockman et al., “Evaluating large
[16] T. Chen, X.-S. Zhang, X.-L. Ji, C. Zhu, Y. Bai, and Y. Wu, “Test                   language models trained on code,” arXiv preprint arXiv:2107.03374,
     generation for embedded executables via concolic execution in a real               2021.
     environment,” IEEE Transactions on Reliability, vol. 64, no. 1, pp. 284–
                                                                                   [37] S. Alagarsamy, C. Tantithamthavorn, and A. Aleti, “A3test: Assertion-
     296, 2014.
                                                                                        augmented automated test case generation,” Information and Software
[17] A. Arcuri, “It does matter how you normalise the branch distance in
                                                                                        Technology, vol. 176, p. 107565, 2024.
     search based software testing,” in 2010 Third International Conference
     on Software Testing, Verification and Validation. IEEE, 2010, pp. 205–        [38] Y. Chen, Z. Hu, C. Zhi, J. Han, S. Deng, and J. Yin, “Chatunitest: A
     214.                                                                               framework for llm-based test generation,” in Companion Proceedings of
[18] P. McMinn, “Search-based software test data generation: a survey,”                 the 32nd ACM International Conference on the Foundations of Software
     Software testing, Verification and reliability, vol. 14, no. 2, pp. 105–           Engineering, 2024, pp. 572–576.
     156, 2004.                                                                    [39] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,
[19] A. Machiry, R. Tahiliani, and M. Naik, “Dynodroid: An input generation             D. Zhou et al., “Chain-of-thought prompting elicits reasoning in large
     system for android apps,” in Proceedings of the 2013 9th joint meeting             language models,” Advances in neural information processing systems,
     on foundations of software engineering, 2013, pp. 224–234.                         vol. 35, pp. 24 824–24 837, 2022.
[20] L. Nguyen Tung, N. V. Binh Duong, K. N. Le, and P. N. Hung, “Au-              [40] E. Zelikman, Y. Wu, J. Mu, and N. Goodman, “Star: Bootstrapping
     tomated test data generation and stubbing method for c/c++ embedded                reasoning with reasoning,” Advances in Neural Information Processing
     projects,” Automated Software Engineering, vol. 31, no. 2, p. 52, 2024.            Systems, vol. 35, pp. 15 476–15 488, 2022.
[21] P. Boonstoppel, C. Cadar, and D. Engler, “Rwset: Attacking path explo-        [41] G. Fraser and A. Arcuri, “Evosuite: On the challenges of test case gener-
     sion in constraint-based test generation,” in Tools and Algorithms for the         ation in the real world,” in 2013 IEEE sixth international conference on
     Construction and Analysis of Systems: 14th International Conference,               software testing, verification and validation. IEEE, 2013, pp. 362–369.
     TACAS 2008, Held as Part of the Joint European Conferences on Theory          [42] S. Rho, P. Martens, S. Shin, and Y. Kim, “Taming the beast: Fully auto-
     and Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-                 mated unit testing with coyote c++,” arXiv preprint arXiv:2401.01073,
     April 6, 2008. Proceedings 14. Springer, 2008, pp. 351–366.                        2024.
[43] P. McMinn, “Search-based software testing: Past, present and future,”      [65] M. Allamanis, E. T. Barr, P. Devanbu, and C. Sutton, “A survey
     in 2011 IEEE Fourth International Conference on Software Testing,               of machine learning for big code and naturalness,” ACM Computing
     Verification and Validation Workshops. IEEE, 2011, pp. 153–163.                 Surveys (CSUR), vol. 51, no. 4, pp. 1–37, 2018.
[44] M. Harman, P. McMinn, J. T. De Souza, and S. Yoo, “Search based soft-      [66] N. Alon, B. Awerbuch, and Y. Azar, “The online set cover problem,”
     ware engineering: Techniques, taxonomy, tutorial,” in LASER Summer              in Proceedings of the thirty-fifth annual ACM symposium on Theory of
     School on Software Engineering. Springer, 2008, pp. 1–59.                       computing, 2003, pp. 100–105.
[45] G. Fraser and A. Arcuri, “Whole test suite generation,” IEEE Transac-      [67] Z. Li, J. Wang, M. Sun, and J. C. Lui, “Mirchecker: detecting bugs
     tions on Software Engineering, vol. 39, no. 2, pp. 276–291, 2012.               in rust programs via static analysis,” in Proceedings of the 2021 ACM
[46] M. Harman, Y. Jia, and Y. Zhang, “Achievements, open problems and               SIGSAC conference on computer and communications security, 2021,
     challenges for search based software testing,” in 2015 IEEE 8th In-             pp. 2183–2196.
     ternational Conference on Software Testing, Verification and Validation    [68] Z. Yuan, M. Liu, S. Ding, K. Wang, Y. Chen, X. Peng, and Y. Lou,
     (ICST). IEEE, 2015, pp. 1–12.                                                   “Evaluating and improving chatgpt for unit test generation,” Proceedings
[47] K. Sen, D. Marinov, and G. Agha, “Cute: A concolic unit testing engine          of the ACM on Software Engineering, vol. 1, no. FSE, pp. 1703–1726,
     for c,” ACM SIGSOFT Software Engineering Notes, vol. 30, no. 5, pp.             2024.
                                                                                [69] J. Kemper, “Chatgpt guide: Use these prompt strategies to maximize
     263–272, 2005.
                                                                                     your results,” https://the-decoder.com/chatgpt-guide-prompt-strategies/,
[48] P. Godefroid, N. Klarlund, and K. Sen, “Dart: Directed automated                2024, (Accessed on 03/07/2025).
     random testing,” in Proceedings of the 2005 ACM SIGPLAN conference         [70] Y. Dong, X. Jiang, Z. Jin, and G. Li, “Self-collaboration code generation
     on Programming language design and implementation, 2005, pp. 213–               via chatgpt,” arXiv preprint arXiv:2304.07590, 2023.
     223.                                                                       [71] G. Ryan, S. Jain, M. Shang, S. Wang, X. Ma, M. K. Ramanathan,
[49] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal,             and B. Ray, “Code-aware prompting: A study of coverage-guided test
     A. Neelakantan, P. Shyam, G. Sastry, A. Askell et al., “Language mod-           generation in regression setting using llm,” Proceedings of the ACM on
     els are few-shot learners,” Advances in neural information processing           Software Engineering, vol. 1, no. FSE, pp. 951–971, 2024.
     systems, vol. 33, pp. 1877–1901, 2020.                                     [72] “Crates.io: Rust package registry,” https://crates.io/, [Accessed 30-04-
[50] A. Chowdhery, S. Narang, J. Devlin, M. Bosma, G. Mishra, A. Roberts,            2025].
     P. Barham, H. W. Chung, C. Sutton, S. Gehrmann et al., “Palm: Scal-        [73] Y. Zhang, J. Wu, and H. Xu, “Rumono: Fuzz driver synthesis for
     ing language modeling with pathways,” Journal of Machine Learning               rust generic apis,” ACM Transactions on Software Engineering and
     Research, vol. 24, no. 240, pp. 1–113, 2023.                                    Methodology, 2024.
[51] M. Shoeybi, M. Patwary, R. Puri, P. LeGresley, J. Casper, and B. Catan-    [74] J. Jiang, H. Xu, and Y. Zhou, “Rulf: Rust library fuzzing via api
     zaro, “Megatron-lm: Training multi-billion parameter language models            dependency graph traversal,” in 2021 36th IEEE/ACM International
     using model parallelism,” arXiv preprint arXiv:1909.08053, 2019.                Conference on Automated Software Engineering (ASE). IEEE, 2021,
[52] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser,                 pp. 581–592.
     M. Plappert, J. Tworek, J. Hilton, R. Nakano et al., “Training verifiers   [75] X. Cheng, F. Sang, Y. Zhai, X. Zhang, and T. Kim, “ RUG: Turbo LLM
     to solve math word problems,” arXiv preprint arXiv:2110.14168, 2021.            for Rust Unit Test Generation ,” in 2025 IEEE/ACM 47th International
[53] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond,             Conference on Software Engineering (ICSE). Los Alamitos, CA, USA:
     T. Eccles, J. Keeling, F. Gimeno, A. Dal Lago et al., “Competition-             IEEE Computer Society, May 2025, pp. 634–634. [Online]. Available:
     level code generation with alphacode,” Science, vol. 378, no. 6624, pp.         https://doi.ieeecomputersociety.org/10.1109/ICSE55347.2025.00097
     1092–1097, 2022.                                                           [76] L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen,
[54] F. F. Xu, U. Alon, G. Neubig, and V. J. Hellendoorn, “A systematic              W. Peng, X. Feng, B. Qin et al., “A survey on hallucination in large
     evaluation of large language models of code,” in Proceedings of the             language models: Principles, taxonomy, challenges, and open questions,”
     6th ACM SIGPLAN International Symposium on Machine Programming,                 ACM Transactions on Information Systems, vol. 43, no. 2, pp. 1–55,
     2022, pp. 1–10.                                                                 2025.
[55] J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan,           [77] C. Pacheco, S. K. Lahiri, M. D. Ernst, and T. Ball, “Feedback-directed
     E. Jiang, C. Cai, M. Terry, Q. Le et al., “Program synthesis with large         random test generation,” in 29th International Conference on Software
     language models,” arXiv preprint arXiv:2108.07732, 2021.                        Engineering (ICSE’07). IEEE, 2007, pp. 75–84.
[56] E. Nijkamp, B. Pang, H. Hayashi, L. Tu, H. Wang, Y. Zhou, S. Savarese,     [78] G. Fraser and A. Arcuri, “1600 faults in 100 projects: automatically
                                                                                     finding faults while achieving high coverage with evosuite,” Empirical
     and C. Xiong, “A conversational paradigm for program synthesis,” arXiv
     preprint arXiv:2203.13474, vol. 30, 2022.                                       software engineering, vol. 20, pp. 611–639, 2015.
                                                                                [79] G. Li, I. Ghosh, and S. P. Rajan, “Klover: A symbolic execution and
[57] A. Ziegler, E. Kalliamvakou, X. A. Li, A. Rice, D. Rifkin, S. Simister,         automatic test generation tool for c++ programs,” in Computer Aided
     G. Sittampalam, and E. Aftandilian, “Productivity assessment of neural          Verification: 23rd International Conference, CAV 2011, Snowbird, UT,
     code completion,” in Proceedings of the 6th ACM SIGPLAN Interna-                USA, July 14-20, 2011. Proceedings 23. Springer, 2011, pp. 609–615.
     tional Symposium on Machine Programming, 2022, pp. 21–29.                  [80] C. Cadar, D. Dunbar, D. R. Engler et al., “Klee: unassisted and automatic
[58] S. Sarsa, P. Denny, A. Hellas, and J. Leinonen, “Automatic generation           generation of high-coverage tests for complex systems programs.” in
     of programming exercises and code explanations using large language             OSDI, vol. 8, 2008, pp. 209–224.
     models,” in Proceedings of the 2022 ACM Conference on International        [81] A. Mathur, S. Pradhan, P. Soni, D. Patel, and R. Regunathan, “Au-
     Computing Education Research-Volume 1, 2022, pp. 27–43.                         tomated test case generation using t5 and gpt-3,” in 2023 9th Interna-
[59] H. Pearce, B. Tan, B. Ahmad, R. Karri, and B. Dolan-Gavitt, “Can                tional Conference on Advanced Computing and Communication Systems
     openai codex and other large language models help us fix security bugs?”        (ICACCS), vol. 1. IEEE, 2023, pp. 1986–1992.
     arXiv preprint arXiv:2112.02125, 2021.                                     [82] C. Lemieux, J. P. Inala, S. K. Lahiri, and S. Sen, “Codamosa: Escaping
[60] J. A. Prenner and R. Robbes, “Automatic program repair with openai’s            coverage plateaus in test generation with pre-trained large language
     codex: Evaluating quixbugs,” arXiv preprint arXiv:2111.03922, 2021.             models,” in 2023 IEEE/ACM 45th International Conference on Software
[61] P. Deligiannis, A. Lal, N. Mehrotra, and A. Rastogi, “Fixing rust               Engineering (ICSE). IEEE, 2023, pp. 919–931.
     compilation errors using llms,” arXiv preprint arXiv:2308.05177, 2023.     [83] A. M. Dakhel, A. Nikanjam, V. Majdinasab, F. Khomh, and M. C.
[62] “GitHub - matklad/once cell: Rust library for single assignment cells           Desmarais, “Effective test generation using pre-trained large language
     and lazy statics without macros — github.com,” https://github.com/              models and mutation testing,” Information and Software Technology, vol.
     matklad/once cell, [Accessed 30-04-2025].                                       171, p. 107468, 2024.
[63] S. Anand, E. K. Burke, T. Y. Chen, J. Clark, M. B. Cohen,
     W. Grieskamp, M. Harman, M. J. Harrold, P. McMinn, A. Bertolino
     et al., “An orchestrated survey of methodologies for automated software
     test case generation,” Journal of systems and software, vol. 86, no. 8,
     pp. 1978–2001, 2013.
[64] S. Bucur, “Improving scalability of symbolic execution for software with
     complex environment interfaces,” Ph.D. dissertation, EPFL, 2015.
