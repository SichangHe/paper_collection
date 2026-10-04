# HarnessLLM: Rust Verification Harness Generation with Large Language Models

[Minghua Wang](https://orcid.org/0000-0002-2270-2076)<sup>∗</sup> Ant Group Beijing, China minghua.wmh@antgroup.com

[Yuwei Liu](https://orcid.org/0000-0001-5170-3388) Ant Group Hangzhou, Zhejiang, China lyw458372@antgroup.com

[Lin Huang](https://orcid.org/0009-0002-5659-1471) Ant Group Beijing, China linyu.hl@antgroup.com

#### Abstract

Rust's ownership and type system offer strong memory safety guarantees, but unsafe code and runtime panics still present significant risks. Formal verification is essential to ensure memory safety, but developing verification harnesses remains a challenging and manual task. Although large language models (LLMs) have shown strong performance in various code analysis tasks, directly applying them to harness generation often results in inaccurate API invocations, inefficient nondeterministic data generation, and fabricated fixes.

In this paper, we present HarnessLLM, an automated workflow that leverages LLMs to generate verification harnesses for Rust code directly from existing test suites. HarnessLLM automatically extracts calling scenarios from test cases, generates nondeterministic arguments based on dependency analysis, and incrementally synthesizes harnesses. It then iteratively refines the harnesses, preserving critical code regions and reporting fabricated types or functions to LLMs for correction. In our evaluation on 9 real-world Rust codebases, HarnessLLM extracted 294 calling scenarios from 494 test cases with 94.66% precision and generated harnesses for all scenarios in an average of 145 seconds each. It outperformed the existing approach, Autoharness, which succeeded on only 41% of those scenarios. Finally, 6 real-world memory safety bugs were detected using the generated harnesses, demonstrating the practical utility of our approach in verification. To our knowledge, this is the first work to use LLMs for generating harnesses aimed at memory safety verification in real-world Rust projects.

#### ACM Reference Format:

Minghua Wang, Yuwei Liu, and Lin Huang. 2026. HarnessLLM: Rust Verification Harness Generation with Large Language Models. In . ACM, New York, NY, USA, [12](#page-11-0) pages.<https://doi.org/10.1145/nnnnnnn.nnnnnnn>

# 1 Introduction

Rust's ownership and type system provide strong guarantees against memory safety issues. However, unsafe code can bypass these guarantees and introduce vulnerabilities [\[20,](#page-10-0) [34,](#page-11-1) [54\]](#page-11-2). Even safe Rust inserts runtime assertions to prevent overflows and out-of-bounds accesses, which may trigger panics unacceptable in security-critical

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

Conference'17, Washington, DC, USA

© 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 978-x-xxxx-xxxx-x/YYYY/MM <https://doi.org/10.1145/nnnnnnn.nnnnnnn>

contexts. While program analysis techniques [\[3,](#page-10-1) [10,](#page-10-2) [26,](#page-11-3) [30\]](#page-11-4) detect many bugs, they lack sound guarantees. Formal methods like theorem proving [\[4,](#page-10-3) [18,](#page-10-4) [19,](#page-10-5) [22,](#page-10-6) [44\]](#page-11-5) and deductive verification [\[2,](#page-10-7) [11,](#page-10-8) [23\]](#page-10-9) offer stronger assurances but demand substantial manual effort. Bounded model checking (BMC) [\[35,](#page-11-6) [45\]](#page-11-7), as one type of automated approach, has been widely adopted in memory safety verification. It encodes execution traces as SAT/SMT problems and produces counterexamples for violations and bounded proofs.

Verification harnesses are essential for applying BMC but are tedious to craft manually, requiring developer effort to identify meaningful API scenarios. Existing tools like RULF [\[21\]](#page-10-10) and RPG [\[56\]](#page-11-8) can synthesize Rust API invocation sequences, but they often lack sufficient semantic insight to prevent API misuse. PropProof [\[40\]](#page-11-9) converts proptest cases [\[33\]](#page-11-10) into Kani harnesses but is limited by test availability. Kani's Autoharness [\[12,](#page-10-11) [45\]](#page-11-7) automates harness generation for functions whose parameter types implement kani::Arbitrary but fails to produce nondet[1](#page-0-0) user-defined types that do not implement this trait. Traditional program analysis approaches face challenges with Rust's advanced features (e.g., generics, closures, higher-order functions) and suffer from LLVM and Rustc version incompatibilities. Recent LLMs have demonstrated superior capabilities at code summarization [\[52\]](#page-11-11), vulnerability detection [\[27,](#page-11-12) [29\]](#page-11-13), software engineering [\[17,](#page-10-12) [53\]](#page-11-14), and program verification [\[7,](#page-10-13) [58\]](#page-11-15), yet have not been applied to harness generation. This paper introduces an LLM-assisted approach for automatically generating Rust verification harnesses, enabling BMC to check for memory safety violations and runtime panics.

However, directly using LLMs to generate verification harnesses for Rust code presents several challenges.

C1: LLMs struggle to capture complete calling scenarios. Formal verification requires validating diverse API usage scenarios to ensure soundness. For small programs, providing the complete code to an LLM may suffice, but in real-world codebases the context window limitations prevent the inclusion of all relevant code.

C2: LLMs have difficulty generating nondet complex arguments. Synthesizing harnesses requires creating nondet arguments. Although LLMs can produce nondet Rust primitive types (e.g., integers, boolean), constructing nondet complex, interdependent types remains challenging. Without precise and clear instructions, LLMs struggle to resolve dependencies to construct required arguments. C3: LLMs may fabricate types and functions. To produce syntactically correct harnesses, Rust compilers are used to compile generated code and provide error feedback. However, due to hallucinations, LLMs may fabricate type definitions or function implementations to bypass compiler errors after multiple attempts. Moreover,

<sup>∗</sup>Corresponding author.

<span id="page-0-0"></span><sup>1</sup>Throughout this paper, the terms nondet (abbreviated) and nondeterministic (full form) are employed synonymously.

error corrections may include arbitrary modifications or even alter previously correct code, inadvertently introducing new errors. This reduces repair efficiency and makes generating a correct harness within a limited number of iterations more difficult.

We observe that, unlike C/C++ projects, Rust codebases often include high-quality test suites covering diverse API usage. Inspired by this, we propose HarnessLLM, a method that leverages LLMs to automatically generate verification harnesses from existing tests. HarnessLLM consists of four phases: code analysis, calling scenario extraction, harness synthesis, and harness compilation. In the code analysis phase, we extract types, traits as well as function definitions, and identify test cases related to the target API. During the calling scenario extraction phase, we isolate individual calling scenarios from the tests (addressing C1) and encapsulate each as an independent "scenario function." In the harness synthesis phase, we first generate nondet parameters and then invoke scenario functions to produce a complete harness. To generate nondet parameters, we construct a type dependency graph and, based on this, produce Chain-of-Thought (CoT) instructions that guide the LLM to incrementally construct the required data types with their public constructors (addressing C2). Finally, in the harness compilation phase, we compile the generated harness with Kani and feed any errors back to the LLM. We specify code regions that must remain unchanged and, at each iteration, check and report any fabricated types or functions to the LLM (addressing C3).

We evaluated HarnessLLM on 9 real-world Rust libraries from crates.io [\[9\]](#page-10-14). From 494 test cases, HarnessLLM extracted 294 invocation scenarios with 94.66% precision, generated 294 syntactically correct verification harnesses with a 100% success rate and an average generation time of 145 seconds seconds per harness. On the same dataset, Kani's Autoharness achieved only 41% coverage. Ablation studies confirmed the effectiveness of HarnessLLM's components, and applying the generated harnesses uncovered 6 real-world memory safety bugs, demonstrating its practical utility. We summarize the contribution as follows:

- We introduce HarnessLLM, the first automated workflow that uses LLMs to generate Rust verification harnesses from existing test suites, enabling memory safety verification of real-world Rust codebases.
- We decompose harness generation into phases of code analysis, call scenario extraction, harness synthesis, and harness compilation, and design prompting strategies to guide LLMs in producing reliable, high-quality outputs at each stage.
- In evaluations across 9 real-world Rust libraries, HarnessLLM achieved 94.66% precision in scenario extraction, a 100% success rate in harness generation, significantly outperforming Kani's Autoharness which only generated harnesses for only 41% of scenarios, with an average generation time of 145 seconds per harness.
- Applying the generated harnesses uncovered 6 real-world memory safety bugs (5 fixed), demonstrating HarnessLLM's practical utility for Rust memory safety verification.

# 2 Background

Safe Rust and Unsafe Rust. Rust's popularity stems from its memory safety features and minimal runtime overhead. However, the unsafe keyword allows operations that bypass safety guarantees, introducing memory safety vulnerabilities. Furthermore, even in safe Rust, runtime errors, including panics, can still occur. The compiler inserts assertions in critical statements (e.g., arithmetic operations and unwrapping), which, if violated, cause program aborts. In this paper, we generate harnesses to verify the absence of memory safety issues and runtime panics.

Bounded Model Checking. Bounded Model Checking (BMC) is a widely used technique for verifying memory safety in unsafe Rust. It encodes program traces as symbolic SAT/SMT problems and employs solvers to provide bounded proofs. However, BMC requires setting fixed bounds on loop iterations and recursion depths. Small bounds risk incomplete unwinding and may miss genuine bugs, while large bounds can cause memory exhaustion and premature termination of the checker. Kani [\[45\]](#page-11-7), a bit-precise BMC for Rust, effectively verifies unsafe Rust code. It can detect memory safety violations such as null pointer dereferences and use-afterfree errors, as well as runtime panics from unexpected behaviors like index-out-of-bounds accesses and arithmetic overflows. Kani uses proof harnesses with symbolic inputs to analyze programs. To generate symbolic inputs for a type, the type must implement the kani::Arbitrary trait, which is already available for most primitive and many standard library types, but user-defined types may require manual implementations. Kani has been successfully applied to verify several real-world Rust projects [\[46](#page-11-16)[–48\]](#page-11-17). In this paper, we leverage Kani to check the harnesses generated by LLMs.

Large Language Models. Large language models (LLMs) have been widely applied to code analysis tasks, including fuzzing [\[29,](#page-11-13) [55,](#page-11-18) [57\]](#page-11-19), automated program repair [\[53\]](#page-11-14), and software testing [\[25\]](#page-10-15). Prompt engineering is a key methodology for interacting with LLMs, employing techniques such as zero-shot prompting [\[50\]](#page-11-20), few-shot prompting [\[5\]](#page-10-16), Chain-of-Thought [\[51\]](#page-11-21), and ReAct [\[60\]](#page-11-22) to improve output accuracy. In this paper, we exploit the capabilities of LLMs and integrate them into the process of harness generation.

## 3 Methodology

# 3.1 Overview

To facilitate harness generation for eliminating Rust memory safety issues and runtime panics, we propose HarnessLLM, a method that leverages LLMs to automatically generate harnesses for Rust code. [Fig. 1](#page-2-0) outlines our approach, which begins with lightweight code analysis, including parsing the Rust source code for the implementation details of functions and types, and identifying all the APIs containing unsafe and the operations potential causing runtime panics. HarnessLLM also locates test cases for those APIs in the codebase. Next, HarnessLLM extracts calling scenarios from these test cases and encapsulates each scenario into a separate function, called a scenario-separated test function. Since these scenario-separated test functions may represent redundant scenarios, HarnessLLM instruments the Rust functions and compares their execution traces to eliminate duplicates, finally forming scenario functions, with each represents distinct scenario.

Harness synthesis then begins with generating nondet parameters for each scenario function. For each scenario function, HarnessLLM first checks whether its parameters can be constructed directly using Kani's primitives. If not, HarnessLLM identifies public

<span id="page-2-0"></span>![](_page_2_Figure_2.jpeg)

Fig. 1: Architecture of HarnessLLM.

type constructors for the parameter types and generates nondet data using them. If these constructors require parameters, the process is recursively applied until all required types can be built using Kani's primitives. During this process, a dependency graph is constructed with each node representing a type constructor (tyf) and edges pointing to the constructors for tyf's parameter types. By traversing this graph, HarnessLLM produces Chain-of-Thought (CoT) instructions that include only the essential type construction steps, ensuring they fit within LLMs' context window. An external knowledge database on common Kani usage further refines these instructions. Finally, a self-contained harness is synthesized by combining the scenario function, the nondet parameter generation code, and its invocation.

After synthesis, HarnessLLM initiates an iterative harness compilation process. In each iteration, HarnessLLM invokes Kani to compile the harness, and LLMs are instructed to fix errors only in the affected code sections. HarnessLLM inspects for any fabricated types or functions and generates feedback prompts for targeted fixes. This process continues until all errors are resolved or a predefined iteration limit is reached.

A Running Example. [Fig. 2](#page-3-0) illustrates HarnessLLM's workflow for generating a verification harness for the function encode. [Fig. 2a](#page-3-0) presents a test case for the function encode, from which we extract calling scenarios. Two temporary scenario-separated test functions are generated, representing equivalent scenarios, as seen in [Fig. 2b,](#page-3-0) and after refinement, we obtain the final scenario function scen\_encode\_array [\(Fig. 2c\)](#page-3-0). This function takes a Value parameter whose definition, as well as that of its dependent type Object, is shown in [Fig. 2d.](#page-3-0) To generate nondet arguments, we first construct a dependency graph and then generate a set of Chain-of-Thought instructions based on the graph for the LLM, instructing it to generate a nondet Object before constructing the Value (see [Fig. 2d\)](#page-3-0). The final synthesized harness [\(Fig. 2e\)](#page-3-0) includes the scenario function, the Kani harness function, and the functions required for constructing nondet data. Finally, the harness is compiled and iteratively refined until a syntactically correct harness for the function encode is obtained.

#### 3.2 Code Analysis

As the first step, we perform a lightweight static analysis of the entire Rust codebase to identify those functions that require verification harnesses. Specifically, we traverse the Rust's MIR to find all functions that either contain unsafe blocks or can trigger a runtime panic. We focus solely on functions implemented within the Rust codebase, excluding those from the Rust standard library and third-party dependencies. After identifying these target functions, we locate all test cases that target them. These test cases serve as the sources for extracting calling scenarios.

Harness synthesis requires creating nondet inputs, so we must locate, for every parameter type, the public constructors that can produce values of that type. To this end, we scan impl Ty blocks for public methods whose return type is Self, Ty, Result<Ty>, or Option<Ty>. When such methods include documentation examples or doctests in their comments, we extract those examples as well, since they often demonstrate valid usage patterns. We also gather the full definitions and visibility attributes of all types and traits declared in the code, recording which traits each type implements and which types implement each trait. This information enhances the accuracy and reliability of type dependency analysis, thereby facilitating effective harness synthesis.

#### <span id="page-2-1"></span>3.3 Calling Scenario Extraction

Our scenario extraction approach builds on two key observations. First, test functions typically use assert statements to exercise target APIs, with each assert representing a distinct invocation scenario. Second, the literal constants in those tests reveal valid API inputs and should be treated symbolically during verification to cover a broader input space. Based on these insights, we first extract the statement sequence leading up to each assert and encapsulate it into a separate function, called a scenario-separated test function. Next, we promote the constants within the sequence to function parameters, resulting in a new function, which we denote as a scenario function. Finally, to ensure that the extracted scenario preserves the original behavior, we replay each scenario function with the same constants as in the scenario-separated test function, compare its execution trace to that of the original. If they match, we consider that the invocation scenario has been accurately preserved.

Traditional program analysis tools, such as custom LLVM or MIR passes, could automate parts of this process, but they often struggle with Rust's generics, closures, and higher-order functions and frequently break across different Rustc or LLVM versions. By contrast, LLMs handle these challenges smoothly when guided by well-designed prompts, enabling a lightweight, robust implementation. Therefore, we integrate LLMs into this process.

Scenario-separated Test Functions. In this stage, we extract individual calling scenarios by encapsulating each assert and its dependent code into a separate function, namely, a scenario-separated test function. As shown in [Fig. 3,](#page-3-1) the prompt directs the LLM to identify all assert statements, perform backward dataflow analysis on the operands to locate all dependent variables and statements, and then organize these statements into separate functions with specified names.

[Fig. 2b](#page-3-0) shows an example of two extraced scenario-separated test functions (encode\_with\_array\_macro and encode\_with\_push\_null)

```
fn encode with array marco()
#[test]
fn encode_array(){
                                                                       { assert_eq!(encode(array![Null]), "[null]");}
  assert_eq!(encode(array![Null]), "[null]");
let mut arr = Value::new_arary();
                                                                                                                                                       fn scen_encode_array(v: Value) {
                                                                       fn encode with push null(){
  let mut arr = Value::new_arar,
arr.push(Null).unwrap();
arr.push(null).unwrap();

                                                                                                                                                            let mut arr = Value::new_array();
arr.push(v).unwrap();
                                                                          let mut arr
                                                                                             Value::new_arary();
                                                                         arr.push(Null).unwrap();
assert_eq!(encode(arr), "[null]");
                                                                                                                                                             encode(arr);
              (a) Test function for encode
                                                                                 (b) Scenario-separated test functions for encode.
                                                                                                                                                                      (c) Scenario function for encode.
                                                                                                                                              fn scen_encode_arary(..) {..}//omitted for space
                                                                   # Instructions:
    pub enum Value {
                                                                                                                                                   mod harness
                                                                                                                                                  [Kani::proof] fn harn_scen_encode_array() {
scen_encode_array(_verifier_nondet_Value());
       Null, Object(Object), ..
                                                                   ## Sect 1: nondet fields for `Value`:
                                                                   pub enum Value{
    pub struct Object{
                                                                     Null, Object(Object), ..
                                                                                                                                                  / build complex types:
n_verifier_nondet_Object() -> Object {
  let sz = _verifier_nondet_int(0, usize::MAX);
  let e = _verifier_nondet_int(0, usize::MAX);
  Object::new(e, sz) // call constructor
       obj: Vec<u32>
     impl Object{
                                                                    *Preparing variant `Obiect`:*
       // constructor
pub fn new(e:u32, sz:usize) -> Self
{ Object{obj:vec![e;sz]} }
                                                                    Refer to [Sect 2] to create this...
                                                                   ## Sect 2: nondet `Object`:
                                                                                                                                                    verifier nondet Value() -> Value
                                                                    Call `fi
                                                                           `fn new(e:u32,sz:usize) -> Self` to create
                                                                                                                                                  match _verifier_nondet_int(0, u8::MAX) {
  1 => Value::Object(_verifier_nondet_Object()),...
                                                                   <!--External Knowledge-->
## Sect X: nondet `u8/u32.
                                                                                                                                                 primitives (from External Knowledge)
                                                                                                                                                    _verifier_nondet_int<T>(min:T,max:T) ->
                                                                   fn verifier nondet int<T>(..) {..}
                                                                                                                                                  kani::any_where(|x: &T|*x<=max && *x>=min)
                              (d) Type definition, dependency graph and CoT instructions.
                                                                                                                                                               (e) Synthesized harness for encode
```

Fig. 2: An example of HarnessLLM's workflow.

representing identical invocation scenarios, which should be represented by scen\_encode\_array. To prevent redundant work in downstream harness generation, we deduplicate scenario-separated test functions so that each distinct invocation scenario is represented only once. This is achieved by instrumenting function entry points in the Rust code to trace execution, running all scenario-separated test functions, and comparing their traces to identify and remove redundant functions.

```
'`rust

<test_fn_code_mutilple_asserts>

Separate the function into multiple test functions, each with a single
'assert'.

# Instructions:

1. Perform a backward use-def analysis on each asserted expression and identify all dependent statements.

2. Extract the identified dependent statements and the corresponding 'assert' to form a new test function.

3. Name the new function as 'scen_separated_test_<\S'\'.'<\S'\' starts from 1.

# Output:

"'rust
#[test] fn scen_separated_test_<\S'() {
// statements that have a data dependency on the asserted expression
}

...
</pre>
```

Fig. 3: Scenario-separated test function generation prompt.

Scenario Function Generation. A scenario function represents a distinct invocation scenario of a target API, with its parameters capturing all possible input values for that scenario. We generate scenario functions by refactoring scenario-separated test functions through a process of assert removal, constant promotion, and parameter refinement. This workflow leverages prompt chaining [37] (Fig. 4), which is particularly effective for complex tasks that might overwhelm LLMs if addressed with a very detailed prompt.

First, we remove the assert statement from scenario-separated test functions, as our focus is on memory safety and runtime panic issues rather than functional correctness. This is achieved by replacing asserted expressions with separate variables and returning

a variable that represents a comprehensive execution context, as depicted in Fig. 4a.

Next, we promote the constants in the scenario-separated test function to parameters of the scenario function while ensuring that the function returns specified variables. The LLM is prompted to identify all actively used constants that are assigned to variables and used in subsequent statements, and promote them as parameters without altering the function's semantics, as shown in Fig. 4b.

Finally, we refine the scenario function's parameters by removing any that are not essential for the invocation scenario. In the harness synthesis stage, each parameter is assigned nondet values, and superfluous parameters cause unnecessary LLM generations. We observed that removing unused variables can help eliminate unused parameters. As Rustc flags unused variables during compilation, we iteratively instruct the LLM with the prompt shown in Fig. 4c to remove unused parameters by leveraging Rustc warnings about unused variables.

**Preservation of Calling Scenarios.** To validate that each scenario function preserves its original calling context, we automatically generate test cases for it by reusing the literal constants from its corresponding scenario-separated test function. We invoke the scenario function with the same constants and apply identical assertions, then compare the execution traces of both the scenario function and the original scenario-separated test function. If the traces match, the scenario function is considered to have preserved the invocation scenario. Otherwise, it is excluded from further harness generation. The test suites may also contain flaky tests whose outcomes vary across different runs. To address this, we run each scenario function multiple times and aggregate all observed traces into a set, ensuring we capture as many execution paths as possible and avoid transient mismatches. Test case generation for scenario functions is driven by the prompt shown in Fig. 5, which specifies the relationship between the scenario function and its original test. With prior instrumentation in place, we execute both versions, collect their traces, and perform the comparisons.

```
Refactor this by removing `assert`.
```rust
<scen_separate_test_fn>
1.Extract each asserted expression into: `let new_var =
<asserted_expr>`
2.Replace asserted expressions with `<new_var>`.
3.Remove `assert`.
# Output
```rust
//return: <new_var> represents a more comprehensive ctxt
<scen_separate_test_fn_noassert>
                                                                 Refactor the code into a new function <scen_fn> by
                                                                  promoting the consts into new params
                                                                 ```rust
                                                                 <scen_separate_test_fn_noassert>
                                                                 # Instructions:
                                                                 1.Extract all constants actively used
                                                                 2.Pass active constants as <scen_fn>'s params
                                                                 # Output:
                                                                 ```rust
                                                                 <scen_fn_code>
                                                                                                                        Fix the warnings of unused vars or params.
                                                                                                                        # Rust Function
                                                                                                                        ```rust
                                                                                                                        <scen_fn_code>
                                                                                                                        # Compilation Message
                                                                                                                        ```text
                                                                                                                        <rustc_msg>
                                                                                                                        # Output
                                                                                                                        ```rust
                                                                                                                        <scen_fn_code_fixed>
```

(a) Assert removal.

(b) Constant promotion.

(c) Parameter refinement.

Fig. 4: Prompt chaining for scenario function generation.

```
<scen_fn> is derived from
<scen_separate_test_fn>. Generate a test
for <scen_fn> that uses constants in
<scen_separate_test_fn>, calls <scen_fn>
and inserts corresponding assertions.
# Function for reference
<scen_separate_test_fn>
# Function to test
<scen_fn_code>
                                               # Output
                                               fn test_<scen_fn>() {
                                                 // use the constants in
                                                // <scen_separate_test_fn>
                                                 let val_1 = <const_1>;
                                                 let expected = <const_2>;
                                                 // call `<scen_fn>`
                                                 let r = <scen_fn>(val_1..);
                                                 assert_eq!(r, expected);
```

Fig. 5: Prompt of generating tests for scenario functions.

# 3.4 Harness Synthesis

We leverage the prompt shown in [Fig. 6](#page-4-2) to synthesize harnesses. The harness is constructed in a separate Rust module, with Kani harness functions attributed with #[kani::proof], and necessary functions for nondet type construction.

The most challenging aspect, highlighted in the figure, is the construction for nondet parameters of the scenario function. Firstly, Kani provides functions for constructing nondet types, but these are limited to primitive Rust types. For complex types, although Kani offers the Arbitrary trait to allow users to manually construct nondet data, it requires adding this to all dependent data types. This requires extensive manual modifications to the codebase, which is error-prone. Additionally, the construction of nondet types must account for Rust's type conversions. For example, some parameters may be traits, requiring the identification of all concrete types that implement the trait.

To overcome these challenges, we adopt the following strategy for constructing nondet types. If Rust basic types can be built with Kani's primitives, we directly utilize them for construction. Otherwise, we use the type's public constructor to create it. The same approach is applied recursively to the parameters of constructor functions. Through this process, we can incrementally build nondet data for all required types. This strategy can be represented by constructing a dependency graph, where each of the other nodes represents a type constructor, and its edges point to the constructors of the parameters required by that type constructor. Finally, the steps to build parameters of scenario function can be determined by performing a topological traversal of the dependency graph.

Dependency Graph. [Algorithm 1](#page-5-0) describes the process of building the dependency graph, denoted as G. In this algorithm, cnstr\_fn represents a type constructor and fn\_par\_tys represents the constructor's parameters. db stores the results of code analysis, and llm refers to the LLM utilized to generate the necessary code for constructing the nondet data. The algorithm begins by fetching

```
Generate Kani harnesses for:
```rust
<scen_fn_code>
# Instructions
1. Generate nondet arguments.
2. Invoke <scen_fn> with the
 nondet arguments.
# Nondet Argument Construction
<CoT Instructions>
                                  # Output:
                                  mod harness_ {
                                   #[kani::proof] fn harness_<scen_fn>(){
                                    // prepare nondet args
                                    let arg1=_verifier_nondet_<ty1>();
                                    <scen_fn>(arg1, ...); // invoke
                                   // Functions to gen nondet types:
                                   fn _verifier_nondet_<tyX>(..)->tyX{..}
```

Fig. 6: Harness synthesis prompt with detailed nondet type construction steps (highlighted).

example usages of the constructor from db, the codebase's documentation tests, providing high-quality references for the LLM (line 3-4). It then checks whether the parameters of the constructor function are traits. If so, it queries db to identify all concrete types that implement the trait (line 7-9). The LLM is then prompted to generate nondet data for these concrete types using prompts as illustrated in [Fig. 7](#page-4-3) (line 11). For a concrete type (par\_ty), its definition is provided to the LLM, and if the LLM successfully generates the construction code, this code is wrapped into a new function (serving as the "nondet constructor" for par\_ty) and added as a node to the dependency graph (line 14-16). If generation fails, the algorithm retrieves par\_ty's constructors from db (via db.get\_constructors\_for), fetches the parameters of each constructor, links each constructor from the current node, and recursively invokes itself (line 19-25). Note that definitions of pub enum and pub struct with all public fields are also treated as their constructors, as they can be directly instantiated through their fields, which serve as the parameters. In the initial invocation of this algorithm, the parameters cnstr\_fn and fn\_par\_tys correspond to scenario function and its parameters, making the scenario function the root node of the graph.

```
Generate nondet <type_name>:
<type_def>
<external_knowledge_of_using_kani>
Output one of the answers:
1.`NULL` for insufficient type defs.
2.Otherwise, output as below:
```rust
fn _verifier_nondet_<ty>(..)-><ty>{
// recursively create nondet with the
 guidelines
                                        # Examples of Using Kani for Nondet
                                        Data Generation in Common Cases
                                        ## Integers:
                                        <code_example>
                                        ## Enum:
                                        Use a nondet int to select variants:
                                        <code_example>
                                        ## Struct
                                        Create nondet members recursively:
                                        <code_example>
                                        ...
```

Fig. 7: The left is the nondet type generation prompt used in [Algorithm 1,](#page-5-0) with the highlighted representing embedded external knowledge shown on the right.

Additionally, the external knowledge embedded in the prompt in [Fig. 7](#page-4-3) includes specific, pre-implemented and syntactically correct code examples that demonstrate how to use Kani to generate nondet data for common scenarios, including primitive types, enums, and structs. These examples enable the LLM to reference or directly adopt correct code during generation, improving compilation success and reducing subsequent harness compilation overhead.

Algorithm 1: Generate Dependency Graph

```
1 Function GEN_DEP_GRAPH(G, llm, db, cnstr_fn, fn_par_tys):
2 /* Get example usages for cnstr_fn */
3 examples ← db.get_usages(cnstr_fn)
4 G.add_node(cnstr_fn, examples)
5 for varpar_ty ∈ fn_par_tys do
6 /* Get types that impl par_ty */
7 ty_impl ← db.get_impl_trait(par_ty, cnstr_fn)
8 if ty_impl is not empty then
9 par_ty ← ty_impl
10 /* Ask LLM to gen nondet par_ty */
11 ans ← llm.gen_nondet_for(par_ty)
12 if ans ≠ 'NULL' then
13 /* If LLM generates nondet par_ty, wrap it as its nondet
        constructor */
14 nondet_fn ← wrap_fn(par_ty, ans)
15 if no_circle(G, nondet_fn, cnstr_fn) then
16 G.add_edge(cnstr_fn, nondet_fn)
17 else
18 /* Otherwise, look for par_ty's constructors */
19 for par_cnstr_fn ∈ db.get_constructors_for(par_ty) do
20 if no_circle(G, cnstr_fn, par_cnstr_fn) then
21 /* cnstr_fn points to its param's constructor par_cnstr_fn */
22 G.add_edge(cnstr_fn, par_cnstr_fn)
23 par_fn_tys ← db.get_param_types(par_cnstr_fn)
24 /* Recursive call */
25 GEN_DEP_GRAPH(G, llm, db, par_cnstr_fn, par_fn_tys)
```

CoT Instructions for Synthesis. We then perform a topological traversal of the dependency graph to generate CoT instructions that guide LLMs in incrementally producing nondet arguments for the scenario function. These instructions, formatted in Markdown, allocate one section per graph node. For leaf nodes (those with no outgoing edges), each section provides code snippets or examples to construct the corresponding nondet types. For non-leaf nodes, which include public constructor functions, pub struct (with all public fields), or pub enum, the sections describe how to create nondet parameters or fields, and indicate which sections should be referenced in the construction process. [Fig. 8](#page-5-1) illustrates the structure of the output CoT instructions.

# <span id="page-5-3"></span>3.5 Harness Compilation

After synthesizing harnesses, we invoke Kani to compile them and use LLMs to resolve compilation errors. To ensure successful compilation, HarnessLLM makes the code self-contained by including the scenario function and the nondet data generation functions

```
# Nondet Argument Constructions:
## Sect 1: nondet <ty_1>:
<kani_code>
## Sect X: nondet fields for <ty_2>
```rust
pub enum <ty_2> { // definition }
*Preparing variant 1,<name_1>:*
 Refer to [Sect X] to create this
*Preparing variant 2,<name_2>:*
 Call `<pub_ty_constructor>` to create
 this. Refer to [Sect Z] for nondet
 construction.
                                        ## Sect Y: nondet fields for <ty_3>
                                        ```rust
                                        pub struct <ty_3> {// definition }
                                        *Preparing member 1,<name_1>:*
                                         Refer to [Sect X] to create this
                                        ...
                                        ## Sect Z: nondet params for
                                         <pub_ty_constructor>:
                                        *Preparing param 1,<name_1>:*
                                         Refer to [Sect 1] to create this
                                        *Preparing param 2,<name_2>:*
                                         Refer to [Sect Y] to create this
                                        ...
```

Fig. 8: Structure of CoT instructions for LLMs to generate nondet parameters.

from the external knowledge database in the synthesized code. HarnessLLM invokes Kani to compile the entire code. If Kani fails to compile, HarnessLLM constructs a feedback prompt containing the error messages and instructs the LLM to fix the issues. This process is repeated until the LLM successfully resolves all compilation errors or the predefined iteration limit is reached.

```
Fix the error(s) below.
{error_msg}
# Output:
Provide the corrected code as below.
<fixed_code>
           (a) Simple error-fix prompt (simple-err-fix).
Fix the error(s) below and remove the fabricated types.
{error_msg}
{fabricated_types}
# Output:
Ensure it contains 3 parts:
// P1: Implementation of `<scen_fn>`. No touch!
{scen_fn_code}
// P2: Functions to generate nondet primitives. No touch!
{code_from_external_knowledge}
// P3: All harnesses for `<scen_fn>`.
<fixed_code>
                   (b) Error-fix prompt (err-fix).
```

Fig. 9: Different prompts designed for error fixing.

[Fig. 9a](#page-5-2) showcases a simple error-fix prompt, which is not effective (as tested in [§5.3\)](#page-7-0). As the scenario function and the external knowledge functions are already syntactically correct, they should remain unchanged during the error-fixing process. Therefore, we designed the prompt shown in [Fig. 9b](#page-5-2) to guide the LLM in error correction. The LLM is instructed to generate the responses in three parts: scenario function, which is guaranteed to be syntactically correct as ensured by the generated test cases [\(§3.3\)](#page-2-1), pre-implemented and syntactically correct functions from the external knowledge database, and the necessary error fixes. It is crucial that the first two parts remain unchanged throughout the error-fixing process, as explicitly emphasized in the prompt. Our experiments have shown that omitting these components, for instance, using the prompt shown in [Fig. 9a,](#page-5-2) can increase the number of generation attempts. This is because LLMs may become distracted from the core task of error correction or introduce additional errors. Furthermore, due to potential hallucinations, the LLM may fabricate types to ensure the code compiles with Kani. To mitigate this, we introduce a lightweight AST checker inspecting whether a type already defined in the codebase is redefined in the LLM-generated code. If such

duplication is detected, we notify the LLM of the error and instruct it to generate new code without introducing any new types.

# 4 Implementation

We implemented HarnessLLM in about 3,000 lines of Python code and 260 lines of Rust code.

Preprocess. We apply function tracing to refine redundant calling scenarios. Using the logfn Rust crate [\[28\]](#page-11-24), we instrument function entries by inserting the attribute #[logfn::logfn(Pre,Debug,fn)] before each function. This logs function execution when the environment variable RUST\_LOG is set to debug. Function names are then extracted from log lines containing DEBUG to form the traces. This instrumentation is performed prior to our workflow.

Code Analysis. We analyze Rust's MIR to identify unsafe code and potential runtime panics. Runtime panics are detected by matching Option/Result::unwrap calls and compiler-inserted assertions at the end of MIR basic blocks. Unsafe code is identified using each function's MIR safety property (MIR.source\_scopes.local\_data.s afety), which marks functions containing or declared as unsafe. All analyses are implemented as a Rustc plugin.

To detect fabricated types or functions during harness compilation, we use tree-sitter [\[39\]](#page-11-25) to parse the AST of LLM-generated harness code. By comparing parsed definitions with those in the original codebase, we can identify any fabricated code.

Rust Compilers. Our workflow employs two Rust compilers: Rustc for eliminating unused parameters during the scenario function generation process, and Kani-0.63.0 [\[45\]](#page-11-7) to compile the LLM-generated harnesses. Kani provides error messages that are fed back to the LLM for iterative error correction.

LLM Settings. We implement HarnessLLM atop OpenAI's GPT-4.1 API [\[31\]](#page-11-26) (gpt-4.1-2025-04-14), with the temperature fixed at 0 and all other parameters set to default. In all iterative interactions with Rust compilers, we limit the number of iterations to 10.

#### 5 Evaluation

Our evaluation aims to address the following research questions.

- RQ1: How does HarnessLLM perform harness generation for real-world Rust codebases?
- RQ2: How do the key components of HarnessLLM contribute to the effectiveness?
- RQ3: How does HarnessLLM compare against existing harness generation methods?
- RQ4: How does HarnessLLM perform when applied with different LLMs?

We evaluated these questions using GPT-4.1 (gpt-4.1-2025-04-14). For RQ4, we also test with claude-sonnet-4-20250514 [\[1\]](#page-10-17), DeepSeekv3-0324 [\[42\]](#page-11-27) and DeepSeek-R1-0528 [\[43\]](#page-11-28) using the same parameter settings as GPT-4.1.

#### 5.1 Settings

Dataset. We used two datasets to evaluate HarnessLLM:

• Real-world Rust libraries ( ). We selected 9 Rust libraries from various categories on crates.io [\[9\]](#page-10-14), comprising a total of 494 tests and 6651 lines of code. Details are presented in [Table 1.](#page-6-0) This dataset was used to assess the overall effectiveness of HarnessLLM. • Scenario functions dataset (). 294 scenario functions were extracted during the harness generation on . These scenario functions were used to evaluate the individual contributions of harness synthesis and compilation.

Platform. The evaluation was conducted using an Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz with 80 cores and 256GB RAM, and a 1TB hard drive, running Ubuntu 20.04.6 LTS.

<span id="page-6-0"></span>

| Library      | Category             | #Test Files | #Test Funcs | LoC  |  |
|--------------|----------------------|-------------|-------------|------|--|
| pdf-rs       | pdf                  | 12          | 34          | 521  |  |
| tar-rs       | tar / encoding       | 4           | 100         | 2387 |  |
| jpeg-decoder | image / decoder      | 9           | 21          | 447  |  |
| tempfile     | filesystem           | 5           | 52          | 637  |  |
| jzon-rs      | json / serialization | 9           | 192         | 1429 |  |
| image-webp   | encoding / decoding  | 4           | 18          | 291  |  |
| lexical-util | numeric conversion   | 9           | 26          | 442  |  |
| prost-types  | prost definitions    | 5           | 15          | 151  |  |
| p256         | elliptic curve       | 6           | 36          | 346  |  |
| Total        | /                    | 63          | 494         | 6651 |  |

Table 1: Details of Rust libraries in , including each name, category, number of test files and functions, and total lines of test functions.

# 5.2 RQ1: Effectiveness

Calling Scenarios Extraction. [Table 2](#page-6-1) summarizes the calling scenarios extracted by HarnessLLM from the libaries in . The #Scenarios column indicates the number of calling scenarios extracted from the tests. The #Prsv. column shows the percentage of scenarios that accurately preserve the original calling scenarios within the test functions. In contrast, the #Non-Prsv. column reflects the percentage of scenarios that differ from the original test functions. As detailed in [§3.3,](#page-2-1) we instrument the functions within these libraries, generate tests for the extracted calling scenarios, execute them to obtain function traces, and compare these traces with those from the original test functions. A scenario is considered correctly preserved if the traces match.

Our results show that, across the 9 libraries, 94.66% of calling scenarios were preserved on average, with image-webp, lexical-util, and jpeg-decoder achieving full preservation. This demonstrates that our approach effectively extracts calling scenarios, laying a solid foundation for harness generation.

<span id="page-6-1"></span>

| Library      | #Scenarios | #Prsv. | #Non-Prsv. | Prsv. Rate |
|--------------|------------|--------|------------|------------|
| pdf-rs       | 27         | 25     | 2          | 92.59%     |
| tar-rs       | 82         | 80     | 2          | 97.56%     |
| jpeg-decoder | 7          | 7      | 0          | 100%       |
| tempfile     | 36         | 35     | 1          | 97.22%     |
| jzon-rs      | 80         | 65     | 15         | 81.25%     |
| image-webp   | 9          | 9      | 0          | 100%       |
| lexical-util | 27         | 27     | 0          | 100%       |
| prost-types  | 6          | 5      | 1          | 83.33%     |
| p256         | 19         | 19     | 0          | 100%       |
| Average      | 32         | 30     | 2          | 94.66%     |

Table 2: Effectiveness of calling scenarios extraction.

Harness Generation. [Table 3](#page-8-0) presents the results of generated harnesses, with the FULL column showing the results obtained through

the complete workflow. The #Harn. column indicates the number of harnesses generated by HarnessLLM for each Rust library. As described in [§3.5,](#page-5-3) during the harness compilation phase, the LLM interacts iteratively with Kani to refine the harnesses, with the number of interactions denoted as @Pass. The @Pass=0 column shows the proportion of harnesses that compiled correctly immediately after the synthesis stage. The columns @Pass<=3,5,10 show the proportions of harnesses that successfully compiled within 3, 5, and 10 interactions with the LLM, respectively, relative to the total number of harnesses (#Harn.). Finally, the #Generations column presents the total number of harness generation attempts when the interaction limit is set to 10.

Within 10 generation attempts, HarnessLLM produced syntactically correct harnesses for all 9 Rust libraries. For image-webp and prost-types, every harness was correct on the first synthesis pass. With up to three generation attempts (@Pass≤3), the overall syntactic correctness rate reached 97.3%, with 5 out of 9 libraries achieving 100%. In total, HarnessLLM generated 294 harnesses across the 9 libraries (32 per library on average), requiring an average of 46 generation attempts, or about 1.4 attempts per valid harness. These results highlight the effectiveness of harness generation.

Performance. For the 294 harnesses, HarnessLLM with GPT-4.1 achieved an average generation time of 145 seconds (2.42 minutes). This time included both compiler execution and network latency. The average cost per harness generation was \$0.03. Additional LLMs were evaluated in [§5.5.](#page-8-1)

Bug Discovery. We ran Kani on the harnesses generated by HarnessLLM and identified six memory safety issues in pdf-rs, as shown in [Table 4.](#page-8-2) Five issues have been fixed, while one is still under developer review.

[Fig. 10](#page-7-1) demonstrates a bug occurred in function utf16be\_to\_ string\_lossy. It calls utf16be\_to\_char, which in turn invokes char ::decode\_utf16 over an iterator that maps each 2-byte chunk of data to a u16 using u16::from\_be\_bytes([w[0],w[1]]). When the length of data is less than 2, accessing w[1] results in an out-ofbound access. [Fig. 11](#page-7-2) shows a test function for the buggy function, the extracted scenario function, and the generated harness. The harness initialized a nondet vector whose length was also nondet. The LLM specified a maximum length, allowing the vector to have any size less than SLICE\_MAX\_LEN. This vector was then passed to the scenario function scen\_test\_to\_char\_4. The bug was detected with "cargo kani --tests --harness harness\_scen\_test\_to\_char - unwind 10 --no-unwinding-checks". Setting an unwind limit is generally essential for analyzing real-world codebases with intricate functions and loops, as it prevents BMC from exhausting resources.

```
pub fn utf16be_to_string_lossy(| data : &[u8])->String{
 utf16be_to_char(| data ).map(|r| r.unwrap_or(char::REPLACEMENT_CHARACTER)).collect()
pub fn utf16be_to_char( data : &[u8]) -> impl Iterator<Item = std::result::Result<char,
char::DecodeUtf16Error>> + '_ {
  char::decode_utf16( data .chunks(2).map(| w | u16::from_be_bytes([w[0], w[1] ])))
```

Fig. 10: Buggy function with the dataflow highlighted.

Sparse Tests. Harness generation success is unaffected by sparse tests. In 9 libraries, we randomly selected a limited number of existing test functions to simulate such cases (#Tests shows the

```
#[test] // existing test function
fn test_to_char() {
 let v = [0xD8, 0x34, 0xDD, 0x1E, 0x00,
 0x6d, 0x00,..]; //10-byte array
 let mut lossy=String::from("?mus");
 lossy.push(char::REPLACEMENT_CHARACTER);
 lossy.push('i'); lossy.push('c');
 lossy.push(char::REPLACEMENT_CHARACTER);
 assert_eq!(utf16be_to_string_lossy(&v),
 lossy);
// scenario function generated:
fn scen_test_to_char_4(v: &[u8]) ->
 String { utf16be_to_string_lossy(v) }
                                           mod harness { // harness generated:
                                            const SLICE_MAX_LEN: usize = 10;
                                            #[kani::proof]
                                            fn harness_scen_test_to_char(){
                                              let l=kani::any_where(|x|*x<SLICE_MAX_LEN);
                                              let arg1 = _verifier_nondet_vec::<u8>(l);
                                              scen_test_to_char_4(&arg1);
                                            fn _verifier_nondet_vec<T>(n: usize)->Vec<T>{
                                              let mut vec = Vec::new();
                                              for _ in 0..n {vec.push(kani::any::<T>());}
                                              vec
```

Fig. 11: The harness for the buggy function, along with its test function and the extracted scenario function.

counts). As shown in [Table 5,](#page-8-3) success rates remain close to 100% within three attempts. However, scenario coverage decreased under sparse tests. To address this, for projects with sparse tests, additional tests could be generated, for instance, by using LLMs to summarize function semantics and derive meaningful calling sequences to enrich scenarios before applying HarnessLLM.

#### <span id="page-7-0"></span>5.3 RQ2: Ablation Study

For harness synthesis, we use a dependency graph and incorporate external knowledge to generate CoT instructions, enabling LLMs to incrementally construct nondet parameters. During harness compilation, we guide LLMs' attention on generating reasonable fixes. This section evaluates the contributions of these methods to the successful generation of harnesses with the dataset .

Contribution of CoT Instructions Design. We designed a new prompt, simple-nondet-gen, for a comparative experiment. This prompt differs from the original shown in [Fig. 6](#page-4-2) by removing the highlighted "Nondet Argument Construction" section containing the CoT instructions. Column SNG in [Table 3](#page-8-0) presents the results using this new prompt. Column @Pass=0 shows the proportion of harnesses that were syntactically correct immediately after the harness synthesis stage. Compared to the original prompt (Column FULL), the absence of nondet generation guidance resulted in an average decrease of 23.1% in the proportion of correctly synthesized harnesses. Specifically, pdf-rs saw the largest decline (37%), as its scenario functions involved more user-defined parameter types. In the subsequent iterative error-fixing phases, the proportions of successfully generated harnesses decreased by 3.3%, 1.9%, and 1.0% at @Pass≤3,5,10, respectively.

Without the CoT guidance, the LLM needed more attempts to produce correct harnesses. For example, the number of generation attempts for lexical-util increased by over 54%. When the interaction limit was set to 10, the total number of generation attempts by the LLM increased by an average of 28.3%.

Contribution of Error-Fix Design. We used simple-err-fix (SEF) shown in [Fig. 9a](#page-5-2) for comparative evaluations, and [Table 3](#page-8-0) presents the results. With SEF, the first-pass success rate for producing syntactically correct harnesses dropped by 18.7% compared to the full workflow. prost-types suffered the largest decline (67%), while jpeg-decoder, tempfile, and image-webp showed no decrease. In the subsequent multi-round error-fixing phases, the success rates at Pass≤3,5,10 fell by 7.7%, 0.8%, and 0.4%, respectively. Overall, the average number of generation attempts increased by 23.9%.

<span id="page-8-0"></span>

| Library      | #Harn.   | @Pass=0 |        | (                 | @Pass≤3 @Pass≤5 |                   | @Pass≤10          |       |                   | #Generations      |      |                       |                   |      |        |                   |
|--------------|----------|---------|--------|-------------------|-----------------|-------------------|-------------------|-------|-------------------|-------------------|------|-----------------------|-------------------|------|--------|-------------------|
| Library      | #11a111. | FULL    | SNG    | SEF               | FULL            | SNG               | SEF               | FULL  | SNG               | SEF               | FULL | SNG                   | SEF               | FULL | SNG    | SEF               |
| pdf-rs       | 27       | 63%     | ↓37%   | ↓19%              | 93%             | ↓12%              | ↓4%               | 97%   | ↑3%               | ↓1%               | 100% | $\longleftrightarrow$ | ↓4%               | 46   | ↑37%   | ↑22%              |
| tar-rs       | 82       | 70%     | ↓11%   | ↓21%              | 98%             | ↓4%               | ↓5%               | 100%  | $\leftrightarrow$ | $\leftrightarrow$ | 100% | $\leftrightarrow$     | $\leftrightarrow$ | 137  | ↑13%   | ↑20%              |
| jpeg-decoder | 7        | 86%     | ↓29%   | $\leftrightarrow$ | 100%            | $\leftrightarrow$ | $\leftrightarrow$ | 100%  | $\leftrightarrow$ | $\leftrightarrow$ | 100% | $\leftrightarrow$     | $\leftrightarrow$ | 11   | ↑22%   | $\leftrightarrow$ |
| tempfile     | 36       | 81%     | ↓28%   | $\leftrightarrow$ | 100%            | ↓3%               | $\leftrightarrow$ | 100%  | $\leftrightarrow$ | $\leftrightarrow$ | 100% | $\leftrightarrow$     | $\leftrightarrow$ | 44   | ↑34%   | $\leftrightarrow$ |
| jzon-rs      | 80       | 83%     | ↓30%   | ↓37%              | 95%             | $\leftrightarrow$ | ↓2%               | 96%   | ↓4%               | ↓1%               | 100% | ↓2%                   | $\leftrightarrow$ | 107  | ↑34%   | ↑38%              |
| image-webp   | 9        | 100%    | ↓22%   | $\leftrightarrow$ | 100%            | $\leftrightarrow$ | $\leftrightarrow$ | 100%  | $\leftrightarrow$ | $\leftrightarrow$ | 100% | $\leftrightarrow$     | $\leftrightarrow$ | 9    | ↑22%   | $\leftrightarrow$ |
| lexical-util | 27       | 63%     | ↓9%    | ↓2%               | 100%            | ↓11%              | $\leftrightarrow$ | 100%  | ↓11%              | $\leftrightarrow$ | 100% | ↓7%                   | $\leftrightarrow$ | 37   | ↑54%   | $\leftrightarrow$ |
| prost-types  | 6        | 100%    | ↓33%   | ↓67%              | 100%            | $\leftrightarrow$ | ↓33%              | 100%  | $\leftrightarrow$ | $\leftrightarrow$ | 100% | $\leftrightarrow$     | $\leftrightarrow$ | 6    | ↑50%   | ↑133%             |
| p256         | 20       | 75%     | ↓25%   | ↓25%              | 90%             | $\leftrightarrow$ | ↓25%              | 100%  | ↓5%               | ↓5%               | 100% | $\leftrightarrow$     | $\leftrightarrow$ | 31   | ↑32%   | <b>↑</b> 61%      |
| Average      | 32       | 80.6%   | ↓23.1% | ↓18.7%            | 97.3%           | ↓3.3%             | ↓7.7%             | 97.8% | ↓1.9%             | ↓0.8%             | 100% | ↓1.0%                 | ↓0.4%             | 46   | ↑28.3% | ↑23.9%            |

Table 3: Comparison of harness generation effectiveness using the complete workflow (FULL), the simple-nondet-gen prompt (SNG) and the simple-err-fix prompt (SEF). ↓ indicates a percentage decrease relative to FULL, ↑ indicates a percentage increase, and ↔ indicates no change.

<span id="page-8-2"></span>

| File          | Buggy Function               | Bug Type            | Fixed |
|---------------|------------------------------|---------------------|-------|
| parse_xref.rs | read_u64_from_stream         | Arith. Overflow     | ✓     |
| font.rs       | utf16be_to_string_lossy      | Access out-of-bound | ✓     |
| file.rs       | load_storage_and_trailer_pwd | Access out-of-bound | ✓     |
| crypt.rs      | Decoder::decrypt             | Access out-of-bound | ✓     |
| crypt.rs      | Decoder::key                 | Access out-of-bound | ×     |
| primitive.rs  | Date::from_primitive         | Not char boundary   | ✓     |

Table 4: Bugs found in pdf-rs (version: 0.9.0).

<span id="page-8-3"></span>

| Libray       | @Pass=0 | @Pass≤3 | @Pass≤5 | @Pass≤10 | #Tests |
|--------------|---------|---------|---------|----------|--------|
| pdf-rs       | 71%     | 100%    | 100%    | 100%     | 6      |
| tar-rs       | 60%     | 100%    | 100%    | 100%     | 10     |
| jpeg-decoder | 50%     | 100%    | 100%    | 100%     | 2      |
| tempfile     | 75%     | 75%     | 100%    | 100%     | 5      |
| jzon-rs      | 70%     | 100%    | 100%    | 100%     | 8      |
| image-webp   | 100%    | 100%    | 100%    | 100%     | 3      |
| lexical-util | 80%     | 100%    | 100%    | 100%     | 3      |
| prost-types  | 100%    | 100%    | 100%    | 100%     | 3      |
| p256         | 50%     | 100%    | 100%    | 100%     | 4      |
| Average      | 72.9%   | 97.2%   | 100%    | 100%     | 5      |

Table 5: Harness generation success rate on sparse tests with the complete workflow (FULL).

#### 5.4 RQ3: Comparisons

Autoharness [12], developed by Kani [45], generates nondeterministic parameters by automatically creating inputs for types that implement Kani::Arbitrary trait and invoking the target functions with these inputs. For Rust primitive types like integers, it automatically generates nondet data, thereby eliminating the need for tedious manual workload.

To ensure a fair comparison, we provided the scenario functions from  $D_{scen}$  to both Autoharness and HarnessLLM, and compared the number of successfully generated harnesses. Fig. 12 illustrates their harness generation performance across various libraries. For pdf-rs, Autoharness failed to generate harnesses for 92.59% of the scenario functions. The best performance was observed in prost-types, where Autoharness generated harnesses for around 66.67% of the scenario functions. The average generation success rate was 41%. This limitation arises because Autoharness currently supports nondet generation only for basic types that implement

kani::Arbitrary trait and cannot handle complex types, particularly user-defined ones within the crate. In contrast, *HarnessLLM* has no such restrictions. By generating CoT instructions from the dependency graph, *HarnessLLM* successfully constructs the necessary nondet parameters, enabling harness generation for every scenario function.

<span id="page-8-4"></span>![](_page_8_Figure_12.jpeg)

Fig. 12: Comparison with Autoharness on  $D_{scen}$ . The average generation success rate of Autoharness was 41%, while HarnessLLM was 100%.

#### <span id="page-8-1"></span>5.5 RQ4: Alternative Models

Fig. 13 presents the generation results of HarnessLLM on the  $D_{rwd}$  dataset using additional LLMs. All models achieved a 100% success rate within 10 attempts. Specifically, in the first generation round, the reasoning model DS-R1 (Deepseek-R1-0528) led with a success rate of 82.67%, followed by Claude-4 (claude-sonnet-4-20250514) at 70%, and DS-V3 (DeepSeek-V3-0324) with the lowest at 67.44%. The initial harness generation relies on the LLM's understanding of the guidelines for nondet generation, highlighting DS-R1's superior comprehension capabilities in this context.

<span id="page-8-5"></span>

| LLMs            | GPT-4.1 | DS-V3 | Claude-4 | DS-R1 |
|-----------------|---------|-------|----------|-------|
| Avg. Time (sec) | 145     | 353   | 188      | 1526  |
| Avg. Cost (USD) | 0.03    | 0.004 | 0.05     | 0.04  |

Table 6: Comparison of generation time and cost per harness.

Table 6 presents the differences among various LLMs in terms of generation time and token cost per harness. Claude-4 incurred

<span id="page-9-0"></span>![](_page_9_Figure_2.jpeg)

Fig. 13: Comparison of LLMs on generation success rate within 10 attempts.

the highest average token cost (\$0.05), while DS-V3 had the lowest (\$0.004). DS-R1 exhibited the longest average harness generation time, as it was the only reasoning model tested, dedicating a significant portion of its time to generating its reasoning steps. In contrast, GPT-4.1 achieved the shortest average generation time.

#### 6 Discussion

Traditional Approaches vs. LLMs. Traditional program analysis approaches like custom LLVM [\[35\]](#page-11-6) or MIR passes [\[13,](#page-10-18) [26\]](#page-11-3), can address parts of our pipeline but often struggle with Rust's advanced features (e.g., generics, closures, and higher-order functions) and are prone to breaking across different Rustc or LLVM versions. By contrast, LLMs excel at code analysis and generation, handling these complexities through well-designed natural language prompts. Therefore, we propose integrating LLMs into our workflow to provide a lightweight but effective solution.

Difference from LLM-based Fuzzing Harness Generation. Unlike prior LLM-based harness generation for fuzzers (e.g., [\[29\]](#page-11-13), [\[55\]](#page-11-18)), which often relies on type dependencies or unconstrained LLM predictions and thus suffers from API misuse, our approach extracts realistic calling scenarios directly from existing well-crafted tests by developers, greatly mitigating misuse issues. Moreover, HarnessLLM is tailored for Rust. It accounts for language-specific features such as traits and leverages Kani knowledge, whereas existing fuzzing harness methods have limited applicability in this setting.

Coverage. The coverage of calling scenarios in the generated harnesses depends on the comprehensiveness of the existing test cases. Our method achieves high success in preserving scenarios, as test cases are typically well-designed by developers. If certain functions lack coverage, additional test cases can be generated to enhance scenario coverage. Furthermore, the Kani harnesses we create use unconstrained symbolic variables for arguments, so the statement coverage can be guaranteed.

Bound Values. Kani, as a BMC, requires explicit bounds for slice lengths. LLMs infer suitable bounds, either constant or unconstrained, based on code understanding, as demonstrated in [Fig. 11.](#page-7-2) Providing appropriate bounds remains a challenge for BMCs. Interval analysis [\[16,](#page-10-19) [49\]](#page-11-29) could help determine bounds. Moreover, as Kani reports unwinding errors along with runtime execution contexts when programs fail to fully unwind, supplying this information, together with relevant code contexts, to LLMs could enable adaptive bound selections. We leave this for future work.

Function Tracing. HarnessLLM only instruments functions in surface Rust code, potentially missing those generated by macros not visible at this level. However, macros make up a small portion of most Rust codebases, so this limitation has minimal impact on the results. As all the functions are visible in Rust's MIR or LLVM IR, we plan to extend instrumentation to those levels by writing passes in future work.

## 7 Related Work

Rust Verification. Several studies focus on Rust verification. Theorem proving approaches like RustBelt [\[22\]](#page-10-6), Aeneas [\[19\]](#page-10-5), Refined Rust [\[18\]](#page-10-4), and HAX [\[4\]](#page-10-3) translate Rust's MIR into Coq or F\* to establish type-system soundness. Prusti [\[2\]](#page-10-7) and Creusot [\[11\]](#page-10-8) apply deductive verification to safe Rust by requiring user-written function contracts and loop invariants. Verus [\[23\]](#page-10-9) uses SMT-based proofs to verify safe Rust and certain unsafe constructs like raw pointers and RefCell. Gillian-Rust [\[63\]](#page-11-30) combines automated verification for safe Rust with separation-logic to handle unsafe code, eliminating the need for external harnesses.

Automatic verification techniques like BMC [\[35,](#page-11-6) [45\]](#page-11-7) and symbolic execution [\[14,](#page-10-20) [32,](#page-11-31) [62\]](#page-11-32) rely on explicit harnesses. Smack [\[35\]](#page-11-6) translates LLVM bitcode to Boogie IR [\[24\]](#page-10-21) to detect memory safety bugs in unsafe Rust. Kani [\[45\]](#page-11-7) checks both safe and unsafe code, verifying a subset of Rust's undefined behaviors and user assertions, but cannot guarantee unbounded proof. UnsafeCop [\[49\]](#page-11-29) extends Kani with loop bound inference, loop stubbing and scheduling strategies to improve scalability. To reduce the manual burden of harness writing, Autoharness [\[12\]](#page-10-11) automates harness generation for functions whose parameters implement kani::Arbitrary, but it cannot handle user-defined types. PropProof [\[40\]](#page-11-9) converts existing proptest [\[33\]](#page-11-10) harnesses into Kani harnesses. TraitInv [\[6\]](#page-10-22) synthesizes harnesses for some built-in traits but not user-defined ones. Erdin [\[15\]](#page-10-23) targets user-defined correctness properties but requires developer-supplied annotations to generate harnesses.

LLM for Harness Generation. No prior work has directly applied LLMs to generate verification harnesses, but related studies have employed LLMs to generate testing harnesses, such as fuzzing harnesses [\[29,](#page-11-13) [55,](#page-11-18) [57\]](#page-11-19), and standard test cases [\[25,](#page-10-15) [36,](#page-11-33) [38\]](#page-11-34). GPTFuzz [\[61\]](#page-11-35) leverages LLMs to generate vulnerable inputs for assessing the robustness of deep learning library APIs. PromptFuzz [\[29\]](#page-11-13) introduces an iterative fuzzing loop that generates drivers to explore previously untested code paths. CKGFuzzer [\[55\]](#page-11-18) uses a code knowledge graph via interprocedural analysis to create fuzz drivers. Whitefox [\[57\]](#page-11-19) generates test programs targeting deep learning compilers to uncover optimization bugs. Several works also explore unit test generation with LLMs. CodaMosa [\[25\]](#page-10-15) supplies test cases for uncovered functions when search-based methods reach coverage saturation. ChatUnitTest [\[8\]](#page-10-24) generates unit tests by extracting key project information and building an adaptive focal context that fits within the LLM's token limit. Tang et al. [\[41\]](#page-11-36) systematically compared

test suites generated by ChatGPT with those from state-of-the-art search-based software testing tools.

LLM for Rust Verification. Another related research [\[7,](#page-10-13) [58,](#page-11-15) [59\]](#page-11-37) explore the integration of LLMs with Rust verification, focusing on automatically generating the proofs necessary for program correctness. The work [\[59\]](#page-11-37) decomposes the verification process into smaller tasks by iteratively querying LLMs and combining their outputs with lightweight static analysis, thereby synthesizing proof structures such as function contracts, invariants, and assertions for Verus and significantly reducing the human workload. AutoVerus [\[58\]](#page-11-15) integrates expert knowledge with formal methods to assist LLMs in generating proofs, employing LLM agents to perform preliminary proof generation, refine proofs based on general guidelines, and debug proofs through verification errors, achieving a 90% success rate in producing corrected proofs. Similarly, SAFE [\[7\]](#page-10-13) introduces a self-evolving framework that addresses data scarcity by combining data synthesis with model fine-tuning, demonstrating superior efficiency and precision over approaches that rely solely on GPT-4.

## 8 Conclusion

We introduce HarnessLLM, an automated workflow leveraging LLMs to generate verification harnesses for Rust code directly from existing test suites. It extracts calling scenarios from test cases, constructs harnesses with nondeterministic arguments, and iteratively refines them using compiler feedback. In evaluations across 9 realworld Rust codebases, HarnessLLM extracted 294 calling scenarios from 494 test cases with a precision of 94.66%, successfully generated 294 harnesses, achieving a 100% success rate, with an average generation time of around 145 seconds per harness, outperforming Autoharness which succeeded on only 41% of the extracted scenarios. Finally, 6 real-world memory safety bugs were identified using the generated harnesses, demonstrating the practical utility of our approach. To the best of our knowledge, HarnessLLM is the first tool to use LLMs for generating harnesses aimed at memory safety verification in real-world Rust projects.

# References

- <span id="page-10-17"></span>[1] Anthropic. 2025. Claude Sonnet 4. [https://docs.anthropic.com/en/docs/about](https://docs.anthropic.com/en/docs/about-claude/models/overview#model-comparison-table)[claude/models/overview#model-comparison-table](https://docs.anthropic.com/en/docs/about-claude/models/overview#model-comparison-table)
- <span id="page-10-7"></span>[2] Vytautas Astrauskas, Aurel Bílý, Jonáš Fiala, Zachary Grannan, Christoph Matheja, Peter Müller, Federico Poli, and Alexander J. Summers. 2022. The Prusti Project: Formal Verification for Rust. In NASA Formal Methods, Jyotirmoy V. Deshmukh, Klaus Havelund, and Ivan Perez (Eds.). Springer International Publishing, Cham, 88–108.
- <span id="page-10-1"></span>[3] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon Lim, and Taesoo Kim. 2021. Rudra: Finding Memory Safety Bugs in Rust at the Ecosystem Scale. In Proceedings of the ACM SIGOPS 28th Symposium on Operating Systems Principles (Virtual Event, Germany) (SOSP '21). Association for Computing Machinery, New York, NY, USA, 84–99. [doi:10.1145/3477132.3483570](https://doi.org/10.1145/3477132.3483570)
- <span id="page-10-3"></span>[4] Karthikeyan Bhargavan, Maxime Buyse, Lucas Franceschino, Lasse Letager Hansen, Franziskus Kiefer, Jonas Schneider-Bensch, and Bas Spitters. 2025. hax: Verifying Security-Critical Rust Software using Multiple Provers. Cryptology ePrint Archive, Paper 2025/142.<https://eprint.iacr.org/2025/142>
- <span id="page-10-16"></span>[5] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. 2020. Language models are few-shot learners. In Proceedings of the 34th International Conference on Neural Information Processing

- Systems (Vancouver, BC, Canada) (NIPS '20). Curran Associates Inc., Red Hook, NY, USA, Article 159, 25 pages.
- <span id="page-10-22"></span>[6] Twain Byrnes, Yoshiki Takashima, and Limin Jia. 2024. Automatically Enforcing Rust Trait Properties. In Verification, Model Checking, and Abstract Interpretation, Rayna Dimitrova, Ori Lahav, and Sebastian Wolff (Eds.). Springer Nature Switzerland, Cham, 210–223.
- <span id="page-10-13"></span>[7] Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Hao Yu, Nan Duan, Peng Cheng, Fan Yang, Shuvendu K Lahiri, Tao Xie, and Lidong Zhou. 2024. Automated Proof Generation for Rust Code via Self-Evolution. arXiv[:2410.15756](https://arxiv.org/abs/2410.15756) [cs.SE] [https://arxiv.org/abs/2410.](https://arxiv.org/abs/2410.15756) [15756](https://arxiv.org/abs/2410.15756)
- <span id="page-10-24"></span>[8] Yinghao Chen, Zehao Hu, Chen Zhi, Junxiao Han, Shuiguang Deng, and Jianwei Yin. 2024. ChatUniTest: A Framework for LLM-Based Test Generation. In Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software Engineering (Porto de Galinhas, Brazil) (FSE 2024). Association for Computing Machinery, New York, NY, USA, 572–576. [doi:10.1145/3663529.3663801](https://doi.org/10.1145/3663529.3663801)
- <span id="page-10-14"></span>[9] The crates.io Team. 2025. The Rust community's crate registry.<https://crates.io> Last accessed Nov. 2025.
- <span id="page-10-2"></span>[10] Mohan Cui, Chengjun Chen, Hui Xu, and Yangfan Zhou. 2023. SafeDrop: Detecting Memory Deallocation Bugs of Rust Programs via Static Data-flow Analysis. ACM Trans. Softw. Eng. Methodol. 32, 4, Article 82 (May 2023), 21 pages. [doi:10.1145/3542948](https://doi.org/10.1145/3542948)
- <span id="page-10-8"></span>[11] Xavier Denis, Jacques-Henri Jourdan, and Claude Marché. 2022. Creusot: A Foundry for the Deductive Verification of Rust Programs. In Formal Methods and Software Engineering, Adrian Riesco and Min Zhang (Eds.). Springer International Publishing, Cham, 90–105.
- <span id="page-10-11"></span>[12] Kani Developers. 2025. Autoharness. [https://model-checking.github.io/kani/](https://model-checking.github.io/kani/reference/experimental/autoharness.html) [reference/experimental/autoharness.html](https://model-checking.github.io/kani/reference/experimental/autoharness.html)
- <span id="page-10-18"></span>[13] The Mirai developers. 2025. MIRAI: Rust mid-level IR Abstract Interpreter. <https://github.com/facebookexperimental/MIRA> Last accessed Nov. 2025.
- <span id="page-10-20"></span>[14] "The RVT developers". 2025. "Rust Verification Tools". [https://project-oak.github.](https://project-oak.github.io/rust-verification-tools/about.html) [io/rust-verification-tools/about.html](https://project-oak.github.io/rust-verification-tools/about.html) Last accessed Nov. 2025.
- <span id="page-10-23"></span>[15] Matthias Erdin. 2019. Verification of Rust Generics, Typestates, and Traits (Master's thesis). Master's thesis. ETH Z¨urich.
- <span id="page-10-19"></span>[16] Andreas Ermedahl, Christer Sandberg, Jan Gustafsson, Stefan Bygde, and Björn Lisper. 2007. Loop Bound Analysis based on a Combination of Program Slicing, Abstract Interpretation, and Invariant Analysis. In 7th International Workshop on Worst-Case Execution Time Analysis (WCET'07) (Open Access Series in Informatics (OASIcs), Vol. 6), Christine Rochange (Ed.). Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 1–6. [doi:10.4230/OASIcs.WCET.2007.1194](https://doi.org/10.4230/OASIcs.WCET.2007.1194)
- <span id="page-10-12"></span>[17] Sidong Feng and Chunyang Chen. 2024. Prompting Is All You Need: Automated Android Bug Replay with Large Language Models. In Proceedings of the IEEE/ACM 46th International Conference on Software Engineering (Lisbon, Portugal) (ICSE '24). Association for Computing Machinery, New York, NY, USA, Article 67, 13 pages. [doi:10.1145/3597503.3608137](https://doi.org/10.1145/3597503.3608137)
- <span id="page-10-4"></span>[18] Lennard Gäher, Michael Sammler, Ralf Jung, Robbert Krebbers, and Derek Dreyer. 2024. RefinedRust: A Type System for High-Assurance Verification of Rust Programs. Proc. ACM Program. Lang. 8, PLDI, Article 192 (June 2024), 25 pages. [doi:10.1145/3656422](https://doi.org/10.1145/3656422)
- <span id="page-10-5"></span>[19] Son Ho and Jonathan Protzenko. 2022. Aeneas: Rust verification by functional translation. Proc. ACM Program. Lang. 6, ICFP, Article 116 (Aug. 2022), 31 pages. [doi:10.1145/3547647](https://doi.org/10.1145/3547647)
- <span id="page-10-0"></span>[20] Sandra Höltervennhoff, Philip Klostermeyer, Noah Wöhler, Yasemin Acar, and Sascha Fahl. 2023. "I wouldn't want my unsafe code to run my pacemaker": an interview study on the use, comprehension, and perceived risks of unsafe rust. In Proceedings of the 32nd USENIX Conference on Security Symposium (Anaheim, CA, USA) (SEC '23). USENIX Association, USA, Article 141, 17 pages.
- <span id="page-10-10"></span>[21] Jianfeng Jiang, Hui Xu, and Yangfan Zhou. 2022. RULF: rust library fuzzing via API dependency graph traversal. In Proceedings of the 36th IEEE/ACM International Conference on Automated Software Engineering (ASE '21). IEEE Press, Melbourne, Australia, 581–592. [doi:10.1109/ASE51524.2021.9678813](https://doi.org/10.1109/ASE51524.2021.9678813)
- <span id="page-10-6"></span>[22] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. RustBelt: Securing the foundations of the Rust programming language. Proceedings of the ACM on Programming Languages 2, POPL (2017), 1–34.
- <span id="page-10-9"></span>[23] Andrea Lattuada, Travis Hance, Jay Bosamiya, Matthias Brun, Chanhee Cho, Hayley LeBlanc, Pranav Srinivasan, Reto Achermann, Tej Chajed, Chris Hawblitzel, Jon Howell, Jacob R. Lorch, Oded Padon, and Bryan Parno. 2024. Verus: A Practical Foundation for Systems Verification. In Proceedings of the ACM SIGOPS 30th Symposium on Operating Systems Principles (Austin, TX, USA) (SOSP '24). Association for Computing Machinery, New York, NY, USA, 438–454. [doi:10.1145/3694715.3695952](https://doi.org/10.1145/3694715.3695952)
- <span id="page-10-21"></span>[24] K Rustan M Leino. 2008. This is boogie 2. manuscript KRML 178, 131 (2008), 9.
- <span id="page-10-15"></span>[25] Caroline Lemieux, Jeevana Priya Inala, Shuvendu K. Lahiri, and Siddhartha Sen. 2023. CodaMosa: Escaping Coverage Plateaus in Test Generation with Pre-Trained Large Language Models. In Proceedings of the 45th International Conference on Software Engineering (ICSE '23). IEEE Press, Melbourne, Victoria, Australia, 919–931. [doi:10.1109/ICSE48619.2023.00085](https://doi.org/10.1109/ICSE48619.2023.00085)

- <span id="page-11-3"></span><span id="page-11-0"></span>[26] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John C.S. Lui. 2021. MirChecker: Detecting Bugs in Rust Programs via Static Analysis. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security (Virtual Event, Republic of Korea) (CCS '21). Association for Computing Machinery, New York, NY, USA, 2183–2196. [doi:10.1145/3460120.3484541](https://doi.org/10.1145/3460120.3484541)
- <span id="page-11-12"></span>[27] Jinghua Liu, Yi Yang, Kai Chen, and Miaoqian Lin. 2024. Generating API Parameter Security Rules with LLM for API Misuse Detection. arXiv[:2409.09288v2 \[](https://arxiv.org/abs/2409.09288v2)cs.CR] <https://arxiv.org/pdf/2409.09288v2>
- <span id="page-11-24"></span>[28] The logfn developer. 2025.<https://crates.io/crates/logfn> Last accessed Nov. 2025.
- <span id="page-11-13"></span>[29] Yunlong Lyu, Yuxuan Xie, Peng Chen, and Hao Chen. 2024. Prompt Fuzzing for Fuzz Driver Generation. In Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security (Salt Lake City, UT, USA) (CCS '24). Association for Computing Machinery, New York, NY, USA, 3793–3807. [doi:10.](https://doi.org/10.1145/3658644.3670396) [1145/3658644.3670396](https://doi.org/10.1145/3658644.3670396)
- <span id="page-11-4"></span>[30] Vikram Nitin, Anne Mulhern, Sanjay Arora, and Baishakhi Ray. 2024. Yuga: Automatically Detecting Lifetime Annotation Bugs in the Rust Language. IEEE Trans. Softw. Eng. 50, 10 (Oct. 2024), 2602–2613. [doi:10.1109/TSE.2024.3447671](https://doi.org/10.1109/TSE.2024.3447671)
- <span id="page-11-26"></span>[31] OpenAI. 2025. GPT-4.1.<https://platform.openai.com/docs/models/gpt-4.1>
- <span id="page-11-31"></span>[32] Stuart Pernsteiner, Iavor S. Diatchki, Robert Dockins, Mike Dodds, Joe Hendrix, Tristan Ravich, Patrick Redmond, Ryan Scott, and Aaron Tomb. 2024. Crux, a Precise Verifier for Rust and Other Languages. arXiv[:2410.18280](https://arxiv.org/abs/2410.18280) [cs.PL] [https:](https://arxiv.org/abs/2410.18280) [//arxiv.org/abs/2410.18280](https://arxiv.org/abs/2410.18280)
- <span id="page-11-10"></span>[33] The proptest developers. 2025. Proptest.<https://github.com/proptest-rs/proptest> Last accessed Nov.2025.
- <span id="page-11-1"></span>[34] Boqin Qin, Yilun Chen, Zeming Yu, Linhai Song, and Yiying Zhang. 2020. Understanding memory and thread safety practices and issues in real-world Rust programs. In Proceedings of the 41st ACM SIGPLAN Conference on Programming Language Design and Implementation (London, UK) (PLDI 2020). Association for Computing Machinery, New York, NY, USA, 763–779. [doi:10.1145/3385412.3386036](https://doi.org/10.1145/3385412.3386036)
- <span id="page-11-6"></span>[35] Zvonimir Rakamarić and Michael Emmi. 2014. SMACK: Decoupling Source Language Details from Verifier Implementations. In Computer Aided Verification, Armin Biere and Roderick Bloem (Eds.). Springer International Publishing, Cham, 106–113.
- <span id="page-11-33"></span>[36] Gabriel Ryan, Siddhartha Jain, Mingyue Shang, Shiqi Wang, Xiaofei Ma, Murali Krishna Ramanathan, and Baishakhi Ray. 2024. Code-Aware Prompting: A Study of Coverage-Guided Test Generation in Regression Setting using LLM. Proc. ACM Softw. Eng. 1, FSE, Article 43 (July 2024), 21 pages. [doi:10.1145/3643769](https://doi.org/10.1145/3643769)
- <span id="page-11-23"></span>[37] Elvis Saravia. 2022. Prompt Engineering Guide.
- <span id="page-11-34"></span>[38] Mohammed Latif Siddiq, Joanna Cecilia Da Silva Santos, Ridwanul Hasan Tanvir, Noshin Ulfat, Fahmid Al Rifat, and Vinícius Carvalho Lopes. 2024. Using Large Language Models to Generate JUnit Tests: An Empirical Study. In Proceedings of the 28th International Conference on Evaluation and Assessment in Software Engineering (Salerno, Italy) (EASE '24). Association for Computing Machinery, New York, NY, USA, 313–322. [doi:10.1145/3661167.3661216](https://doi.org/10.1145/3661167.3661216)
- <span id="page-11-25"></span>[39] The Tree sitter developer. 2025.<https://github.com/tree-sitter/tree-sitter> Last accessed Nov. 2025.
- <span id="page-11-9"></span>[40] Yoshiki Takashima. 2023. PropProof: Free Model-Checking Harnesses from PBT. In Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (San Francisco, CA, USA) (ESEC/FSE 2023). Association for Computing Machinery, New York, NY, USA, 1903–1913. [doi:10.1145/3611643.3613863](https://doi.org/10.1145/3611643.3613863)
- <span id="page-11-36"></span>[41] Yutian Tang, Zhijie Liu, Zhichao Zhou, and Xiapu Luo. 2024. ChatGPT vs SBST: A Comparative Assessment of Unit Test Suite Generation. IEEE Trans. Softw. Eng. 50, 6 (June 2024), 1340–1359. [doi:10.1109/TSE.2024.3382365](https://doi.org/10.1109/TSE.2024.3382365)
- <span id="page-11-27"></span>[42] The DeepSeek Team. 2025. deepseek-chat.<https://api-docs.deepseek.com/>
- <span id="page-11-28"></span><span id="page-11-5"></span>[43] The DeepSeek Team. 2025. deepseek-reasoner.<https://api-docs.deepseek.com/> [44] Sebastian Ullrich. 2016. Simple Verification of Rust Programs via Functional Purifi-
- cation (Master's thesis). Master's thesis. Fakultät für Informatik.
- <span id="page-11-7"></span>[45] Alexa VanHattum, Daniel Schwartz-Narbonne, Nathan Chong, and Adrian Sampson. 2022. Verifying dynamic trait objects in rust. In Proceedings of the 44th International Conference on Software Engineering: Software Engineering in Practice (Pittsburgh, Pennsylvania) (ICSE-SEIP '22). Association for Computing Machinery, New York, NY, USA, 321–330. [doi:10.1145/3510457.3513031](https://doi.org/10.1145/3510457.3513031)
- <span id="page-11-16"></span>[46] Kani Verifier. 2022. Use Kani action in CI. [https://github.com/aws/s2n-quic/pull/](https://github.com/aws/s2n-quic/pull/1556) [1556](https://github.com/aws/s2n-quic/pull/1556)
- [47] Kani Verifier. 2023. How Kani helped find bugs in Hifitime. [https://model](https://model-checking.github.io/kani-verifier-blog/2023/03/31/how-kani-helped-find-bugs-in-hifitime.html)[checking.github.io/kani-verifier-blog/2023/03/31/how-kani-helped-find-bugs](https://model-checking.github.io/kani-verifier-blog/2023/03/31/how-kani-helped-find-bugs-in-hifitime.html)[in-hifitime.html](https://model-checking.github.io/kani-verifier-blog/2023/03/31/how-kani-helped-find-bugs-in-hifitime.html)
- <span id="page-11-17"></span>[48] Kani Verifier. 2023. Using Kani to Validate Security Boundaries in AWS Firecracker. [https://model-checking.github.io/kani-verifier-blog/2023/08/31/using](https://model-checking.github.io/kani-verifier-blog/2023/08/31/using-kani-to-validate-security-boundaries-in-aws-firecracker.html)[kani-to-validate-security-boundaries-in-aws-firecracker.html](https://model-checking.github.io/kani-verifier-blog/2023/08/31/using-kani-to-validate-security-boundaries-in-aws-firecracker.html)
- <span id="page-11-29"></span>[49] Minghua Wang, Jingling Xue, Lin Huang, Yuan Zi, and Tao Wei. 2025. UnsafeCop: Towards Memory Safety for Real-World Unsafe Rust Code with Practical Bounded Model Checking. In Formal Methods, Andre Platzer, Kristin Yvonne Rozier, Matteo Pradella, and Matteo Rossi (Eds.). Springer Nature Switzerland, Cham, 307–324.
- <span id="page-11-20"></span>[50] Jason Wei, Maarten Bosma, Vincent Y. Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M. Dai, and Quoc V. Le. 2022. Finetuned Language Models Are Zero-Shot Learners. arXiv[:2109.01652](https://arxiv.org/abs/2109.01652) [cs.CL] [https://arxiv.org/abs/](https://arxiv.org/abs/2109.01652)

- [2109.01652](https://arxiv.org/abs/2109.01652)
- <span id="page-11-21"></span>[51] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. 2022. Chain-of-thought prompting elicits reasoning in large language models. In Proceedings of the 36th International Conference on Neural Information Processing Systems (New Orleans, LA, USA) (NIPS '22). Curran Associates Inc., Red Hook, NY, USA, Article 1800, 14 pages.
- <span id="page-11-11"></span>[52] Yifan Wu, Ying Li, and Siyu Yu. 2024. Commit Message Generation via Chat-GPT: How Far Are We?. In Proceedings of the 2024 IEEE/ACM First International Conference on AI Foundation Models and Software Engineering (Lisbon, Portugal) (FORGE '24). Association for Computing Machinery, New York, NY, USA, 124–129. [doi:10.1145/3650105.3652300](https://doi.org/10.1145/3650105.3652300)
- <span id="page-11-14"></span>[53] Yonghao Wu, Zheng Li, Jie M. Zhang, and Yong Liu. 2024. ConDefects: A Complementary Dataset to Address the Data Leakage Concern for LLM-Based Fault Localization and Program Repair. In Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software Engineering (Porto de Galinhas, Brazil) (FSE 2024). Association for Computing Machinery, New York, NY, USA, 642–646. [doi:10.1145/3663529.3663815](https://doi.org/10.1145/3663529.3663815)
- <span id="page-11-2"></span>[54] Hui Xu, Zhuangbin Chen, Mingshen Sun, Yangfan Zhou, and Michael R. Lyu. 2021. Memory-Safety Challenge Considered Solved? An In-Depth Study with All Rust CVEs. ACM Trans. Softw. Eng. Methodol. 31, 1, Article 3 (Sept. 2021), 25 pages. [doi:10.1145/3466642](https://doi.org/10.1145/3466642)
- <span id="page-11-18"></span>[55] Hanxiang Xu, Wei Ma, Ting Zhou, Yanjie Zhao, Kai Chen, Qiang Hu, Yang Liu, and Haoyu Wang. 2024. CKGFuzzer: LLM-Based Fuzz Driver Generation Enhanced By Code Knowledge Graph. arXiv[:2411.11532](https://arxiv.org/abs/2411.11532) [cs.SE] [https://arxiv.org/abs/2411.](https://arxiv.org/abs/2411.11532) [11532](https://arxiv.org/abs/2411.11532)
- <span id="page-11-8"></span>[56] Zhiwu Xu, Bohao Wu, Cheng Wen, Bin Zhang, Shengchao Qin, and Mengda He. 2024. RPG: Rust Library Fuzzing with Pool-based Fuzz Target Generation and Generic Support. In Proceedings of the IEEE/ACM 46th International Conference on Software Engineering (Lisbon, Portugal) (ICSE '24). Association for Computing Machinery, New York, NY, USA, Article 124, 13 pages. [doi:10.1145/3597503.](https://doi.org/10.1145/3597503.3639102) [3639102](https://doi.org/10.1145/3597503.3639102)
- <span id="page-11-19"></span>[57] Chenyuan Yang, Yinlin Deng, Runyu Lu, Jiayi Yao, Jiawei Liu, Reyhaneh Jabbarvand, and Lingming Zhang. 2024. WhiteFox: White-Box Compiler Fuzzing Empowered by Large Language Models. Proc. ACM Program. Lang. 8, OOPSLA2, Article 296 (Oct. 2024), 27 pages. [doi:10.1145/3689736](https://doi.org/10.1145/3689736)
- <span id="page-11-15"></span>[58] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui, Yeyun Gong, Chris Hawblitzel, Shuvendu Lahiri, Jacob R. Lorch, Shuai Lu, Fan Yang, Ziqiao Zhou, and Shan Lu. 2025. AutoVerus: Automated Proof Generation for Rust Code. arXiv[:2409.13082](https://arxiv.org/abs/2409.13082) [cs.SE]<https://arxiv.org/abs/2409.13082>
- <span id="page-11-37"></span>[59] Jianan Yao, Ziqiao Zhou, Weiteng Chen, and Weidong Cui. 2023. Leveraging Large Language Models for Automated Proof Synthesis in Rust. arXiv[:2311.03739](https://arxiv.org/abs/2311.03739) [cs.FL] <https://arxiv.org/abs/2311.03739>
- <span id="page-11-22"></span>[60] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language Models. arXiv[:2210.03629](https://arxiv.org/abs/2210.03629) [cs.CL]<https://arxiv.org/abs/2210.03629>
- <span id="page-11-35"></span>[61] Jiahao Yu, Xingwei Lin, Zheng Yu, and Xinyu Xing. 2024. GPTFUZZER: Red Teaming Large Language Models with Auto-Generated Jailbreak Prompts. arXiv[:2309.10253](https://arxiv.org/abs/2309.10253) [cs.AI]<https://arxiv.org/abs/2309.10253>
- <span id="page-11-32"></span>[62] Ying Zhang, Peng Li, Yu Ding, Lingxiang Wang, Dan Williams, and Na Meng. 2024. Broadly Enabling KLEE to Effortlessly Find Unrecoverable Errors in Rust. In Proceedings of the 46th International Conference on Software Engineering: Software Engineering in Practice (Lisbon, Portugal) (ICSE-SEIP '24). Association for Computing Machinery, New York, NY, USA, 441–451. [doi:10.1145/3639477.3639714](https://doi.org/10.1145/3639477.3639714)
- <span id="page-11-30"></span>[63] Sacha Élie Ayoun, Xavier Denis, Petar Maksimović, and Philippa Gardner. 2025. A hybrid approach to semi-automated Rust verification. arXiv[:2403.15122](https://arxiv.org/abs/2403.15122) [cs.PL] <https://arxiv.org/abs/2403.15122>