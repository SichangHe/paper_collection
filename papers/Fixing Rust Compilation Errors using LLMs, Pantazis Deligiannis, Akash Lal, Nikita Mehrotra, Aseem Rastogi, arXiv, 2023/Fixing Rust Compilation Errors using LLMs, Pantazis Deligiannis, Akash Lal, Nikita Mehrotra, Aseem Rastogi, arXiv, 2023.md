                                                                Fixing Rust Compilation Errors using LLMs
                                                               Pantazis Deligiannis                                                               Akash Lal
                                                                 Microsoft Research                                                          Microsoft Research
                                                                 Redmond, WA, USA                                                             Bengaluru, India
                                                               pdeligia@microsoft.com                                                      akashl@microsoft.com

                                                                  Nikita Mehrotra                                                             Aseem Rastogi
                                                                 Microsoft Research                                                         Microsoft Research
                                                                  Bengaluru, India                                                           Bengaluru, India
                                                             t-nmehrotra@microsoft.com                                                    aseemr@microsoft.com
arXiv:2308.05177v1 [cs.SE] 9 Aug 2023




                                        ABSTRACT                                                                   15   struct Foo { map: RwLock<HashMap<String, Bar>> }
                                                                                                                   16
                                        The Rust programming language, with its safety guarantees, has             17   impl Foo {
                                        established itself as a viable choice for low-level systems program-       18     pub fn get(&self, key: String) → &Bar {
                                                                                                                   19       self.map.write().unwrap().entry(key).or_insert(Bar::new())
                                        ming language over the traditional, unsafe alternatives like C/C++.        20     }
                                        These guarantees come from a strong ownership-based type sys-              21   }
                                        tem, as well as primitive support for features like closures, pattern
                                        matching, etc., that make the code more concise and amenable to                    Figure 1: Snippet from a Stack Overflow question
                                        reasoning. These unique Rust features also pose a steep learning
                                        curve for programmers.                                                        The Rust typechecker, with a novel borrow checker at its core,
                                           This paper presents a tool called RustAssistant that leverages          ensures that the Rust programs are free of memory-safety errors
                                        the emergent capabilities of Large Language Models (LLMs) to auto-         and data races that have plagued low-level systems for decades1 .
                                        matically suggest fixes for Rust compilation errors. RustAssistant         The main idea is that every value is used linearly and has exactly
                                        uses a careful combination of prompting techniques as well as itera-       one owner. A value may be borrowed using references—there may
                                        tion with an LLM to deliver high accuracy of fixes. RustAssistant          exist multiple immutable borrows or a single, exclusive mutable
                                        is able to achieve an impressive peak accuracy of roughly 74% on           borrow for a value at any point in the program. In addition, Rust
                                        real-world compilation errors in popular open-source Rust reposi-          has primitive support for features like closures, pattern matching,
                                        tories. We plan to release our dataset of Rust compilation errors to       etc., that make the code more concise and amenable to reasoning.
                                        enable further research.                                                      However, this also means that there is a steep learning curve
                                                                                                                   for programmers coming to Rust from the traditional C/C++ back-
                                                                                                                   ground. Although Rust tooling (compiler error messages, IDE sup-
                                                                                                                   port [46]) is well-designed to help programmers understand and fix
                                        1   INTRODUCTION                                                           the compilation errors, they can still be intimidating for Rust begin-
                                        The emergence of Large Language Models (LLMs) and their code               ners. A recent survey by the Rust team [51], for example, reports
                                        comprehension capabilities is disrupting the way we build, main-           that 83% of the responders who adopted Rust at work found it to be
                                        tain, and deploy software systems. LLMs are rapidly becoming               challenging. Though adopting a new language and its ecosystem is
                                        an integral part of the workflow, starting from software develop-          always challenging, 27% of the responders also say that using Rust
                                        ment [10], testing [11], repair and debugging [6, 7, 21, 22, 43–45, 66],   is at times a struggle.
                                        to how the users interact with the software [32, 33].                         Consider, for example, Figure 1 showing snippet from a Stack
                                           LLMs are large models, that have been trained on vast amount            Overflow question [16] about the following error that the Rust
                                        of public data, including open-source code [2, 40, 41, 57, 58]. The        compiler emits on this code:
                                        promise of LLMs is that, without any need for fine-tuning the                    error[E0515]: cannot return value referencing temporary value
                                        model for the task at hand, one can interact with them using nat-                −−> src/example.rs:21:4
                                                                                                                            |
                                        ural language prompts and get them to follow the instructions to                 21 | self.map.write().unwrap().entry(key).or_insert(Bar::new())
                                        accomplish the task. Using prompt engineering to study and har-                     | −−−−−−−−−−−−−−−−−−−^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                                                                            | |
                                        ness the novel emergent behaviors of LLMs has become an active                      | returns a value referencing data owned by the current function
                                        area of research [36, 52].                                                          | temporary value created here
                                           In this paper, we consider the task of fixing Rust [47] compilation
                                        errors using LLMs. Rust, with its safety guarantees, has established          Fixing this error is not straightforward. For non-experts, making
                                        itself as a viable choice for low-level systems programming lan-           sense of the Rust borrow checking rules, especially with mutex and
                                        guage over the traditional, unsafe alternatives like C/C++. Rust           concurrency can be daunting. And even if the solution is concep-
                                        enjoys strong support from both the open-source community (e.g.,           tually clear to the experts, they still need to know about the Rust
                                        support for Rust in the Linux kernel [26], voted as the most loved         libraries to use for the fix (we get back to the example in Section 2).
                                        language in the Stack Overflow survey [54]) and technology com-            1 A Microsoft study found that ∼ 70% of the vulnerabilities Microsoft assigns a CVE
                                        panies alike [3, 29].                                                      each year continue to be memory safety issues [35].
                                                                                       Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, and Aseem Rastogi


   Contributions. We present RustAssistant, an LLM-based tool                ChangeLog:1@src/example.rs
                                                                             FixDescription: Change the return type of the 'get' method to return an
for automatically fixing Rust compilation errors. RustAssistant is           Arc<Bar> and wrap the Bar in an Arc when inserting it into the HashMap.
a command-line tool that given a filesystem path of a Rust develop-          OriginalCode@19−23:
ment, potentially containing build errors, iterates with an LLM to           [19] impl Foo {
                                                                             [20] pub fn get(&self, key: String) → &Bar {
fix those errors and generate patches. RustAssistant specializes             [21] self.map.write().unwrap().entry(key).or_insert(Bar::new())
prompt construction for the purpose of fixing compilation errors,            [22] }
and uses a novel changelog format in order to harness the LLM                [23] }
                                                                             FixedCode@19−24:
capabilities (Section 3).                                                    [19] impl Foo {
   To evaluate RustAssistant, we built a dataset of Rust compi-              [20] pub fn get(&self, key: String) → std::sync::Arc<Bar> {
                                                                             [21] self.map.write().unwrap().entry(key).or_insert_with(
lation errors collected from three different sources: (a) 270 micro-         [22]    || std::sync::Arc::new(Bar::new())).clone()
benchmarks that we have written ourselves, covering 270/506 offi-            [23] }
cial Rust error codes [50], (b) 50 Rust programs collected from Stack        [24] }
Overflow questions, and (c) 182 GitHub commits with compilation
errors from the top-100 Rust crates from crates.io (Section 4).                          Figure 2: Output of RustAssistant.
   Using RustAssistant and our dataset, we systematically study
and evaluate capabilities of two LLMs, GPT-3.5 [40] and GPT-4 [41],        2.2    Overview of the RustAssistant pipeline
for fixing Rust compilation errors. With GPT-4, we find that Rus-          The code snippet in Figure 1 contains struct Foo, which maintains
tAssistant is able to fix 92.59% of the micro-benchmarks, 72% of           a HashMap mapping String keys to Bar values. The hashmap is
the Stack Overflow programs, and 73.63% of the GitHub commits.             concurrency-protected with a RwLock, a locking mechanism in
We also find that GPT-4 performs better than GPT-3.5 in the task.          Rust that allows multiple readers but at-most one writer at a time.
We report on several ablation studies, to investigate the impact of        The programmer’s intent in the function get is to return a reference
algorithmic and prompting variations (Section 5).                          to the value mapped to key in the hashmap.
   We also demonstrate the generalizability of RustAssistant on                The implementation of get first calls RwLock::write, a blocking
errors beyond compilation errors. We show that RustAssistant,              call that returns a guarded, exclusive, write access to the object
with minor prompt modifications, can handle linter errors generated        protected by the lock, in this case the hashmap. The write access is
by Rust Clippy, one of the most popular static analysis tool for Rust      released as the guard goes out-of-scope, e.g., when the function call
[48]. RustAssistant achieves an accuracy of 75% on the top-10              returns. The function then proceeds to read the value of key, and
Rust crates for fixing Clippy-reported errors, which is almost 2.4         return a reference to the read value. When this code is compiled
times better fix rate than Clippy’s own auto-fix feature.                  with Rust, the compiler complains with the error shown in Section 1.
   We plan to open-source both our dataset as well as the imple-               Rust maintains a list of all the error codes that can be emitted
mentation of RustAssistant.                                                by the compiler [50]. Here the the error code is E0515 on line 21,
                                                                           meaning that the function is trying to return reference to a local
                                                                           variable. The error comes from the Rust borrow checker. The re-
                                                                           turned reference, which is derived from the mutex owned hashmap,
2     OVERVIEW                                                             escapes the function scope, and therefore, outlives the mutex guard
In this section we describe the scope of our work and walk through         lifetime—a violation of the borrow checking rules.
the RustAssistant pipeline using the example from Section 1.                   Let’s see how RustAssistant fixes the code. RustAssistant
                                                                           first invokes the Rust compiler on the input code and collects the
                                                                           error message. It then feeds the code and the compilation error,
                                                                           along with instructions in a prompt, to the LLM. RustAssistant
2.1    Scope                                                               is parametric in the choice of LLM; we show the interactions with
Our goal is to build a toolchain and systematically evaluate the           GPT-4 in this section. Figure 2 shows the output of GPT-4. The
capabilities of LLMs for generating fixes for Rust compilation errors.     output contains the suggested fix in text, and a form of changelog.
These fixes must pass the compiler and must also retain the intended       RustAssistant prompts the LLM to use this specific format; we
semantics of the code. The former is an objective criterion while          explain the LLM prompt and the output format in detail in the next
the latter is subjective. Since the code that we start with is not even    section.
well-typed, let alone have a well-defined semantics, one requires              The suggested fix is to change the return type of get to Arc<Bar>,
external judgement to assess the quality of a fix. In the evaluation       and also insert Arc<Bar> in the hashmap. Arc in Rust is an atomi-
of RustAssistant (Section 5), we either rely on test cases (fix must       cally reference-counted, thread-safe pointer. With this change, the
build and pass the test) or a comparison with the actual fix made          get function can return a copy of the value, an Arc pointer that
by a developer to establish quality.                                       points to the same heap location as the value in the map (clone
    We focus on fixing code-related issues and, thus, consider editing     creates the copy).
only the Rust source files (i.e., files with .rs extension). Errors that       RustAssistant parses this LLM output, applies the suggested
require changing a configuration (e.g., adding a package to a .toml        patch to the code, and compiles the program again. This time, the
file) are currently out of scope. We also do not consider errors           Rust compiler complains with the error shown in Figure 3.
related to the use of the unsafe keyword, which provides an escape             The error is about the mismatch between the declared type of
hatch from the typechecker.                                                hashmap, mapping String keys to Bar values, and the usage of it as
Fixing Rust Compilation Errors using LLMs


     error[E0308]: mismatched types                                                retrieve the contents of the files, edit them, or even revert them to
     −−> src/example.rs:22:6
        |
                                                                                   a previous state.
     22 |   || std::sync::Arc::new(Bar::new())).clone()                               RustAssistant must handle the complexities of fixing errors in
        |      ^^^^^^^^^^^^^^^^^^^^^^^^^                                           real-world scenarios. Source files can be large relative to the LLM
        |      expected struct `Bar`, found struct `Arc
                                                                                   prompt sizes that were available to us (maximum of 32K tokens,
Figure 3: Error after the first fix suggested by RustAssistant                     for GPT-4), and most of the code in a file might not be relevant
                                                                                   to a reported error any way. RustAssistant, therefore, performs
a map from String keys to Arc<Bar> values—indeed, the previous                     localization for each error to identify relevant parts of the source
patch did not fix the declaration of the hashmap.                                  code and presents only those parts to the LLM, i.e., a single prompt
   RustAssistant sends the code and the error to the LLM again.                    may contain multiple code snippets. This implies that we need a
In this instance, GPT-4 responds with the following fix, correctly                 way of parsing the LLM response to know which change needs to be
suggesting to change the type of map.                                              applied where. We tried a naive approach where we asked the LLM
                                                                                   to simply give us the revised code snippets. This approach did not
    ChangeLog:1@src/example.rs
    FixDescription: Change the type of values stored in the HashMap to Arc<Bar>.
                                                                                   work in our real-world evaluation. As Section 5 will show (Table 4),
    OriginalCode@16−16:                                                            the accuracy of RustAssistant tanked below 10%, making the
    [16] map: RwLock<HashMap<String, Bar>>                                         tool unusable. To account for this, we define a simple, but effective,
    FixedCode@16−16:
    [16] map: RwLock<HashMap<String, std::sync::Arc<Bar>>                          changelog format that only captures the changes that need to be
                                                                                   made to the given code snippets. We describe this format in the
  RustAssistant parses the output, applies the patch to the code,                  prompt and instruct the model to follow it. RustAssistant uses
and invokes the Rust compiler again. This time the compiler suc-                   a lightweight parser to understand the changelog in the LLM’s
ceeds and the tool returns. Using Arc is also the accepted Stack                   response and can then easily apply the changes to the original
Overflow answer for this question [16].                                            source code. This approach significantly increases RustAssistant’s
                                                                                   accuracy, essentially because the LLM stays focussed on the changes
3     RUSTASSISTANT IMPLEMENTATION                                                 that it needs to make (more details in Section 5). This justifies why
                                                                                   our prompt construction is an important contribution.
Algorithm 1 The RustAssistant algorithm.                                              Algorithm 1 shows the RustAssistant core algorithm. The
Require: 𝑚: LLM, 𝑁 : Number of completions                                         algorithm starts by invoking the checker on the project to gather
Require: 𝑝𝑟𝑜 𝑗𝑒𝑐𝑡: Rust project                                                    the initial list of errors, and starts fixing them one at a time (line 2).
 1: 𝑒𝑟𝑟𝑠 ← check(𝑝𝑟𝑜 𝑗𝑒𝑐𝑡)                                                            Inner loop for fixing an input error. The inner loop (lines
 2: while 𝑒𝑟𝑟𝑠 ≠ ∅ do                                                              6 − 17) iterates with the LLM with the goal of fixing a single input
 3:     𝑒 ← choose_any(𝑒𝑟𝑟𝑠)                                                       error (𝑒). During this iteration, the source files may change and
 4:     𝑔 ← {𝑒}                                                                    those changes may themselves induce additional errors. To accom-
 5:     𝑠𝑛𝑎𝑝 ← 𝑝𝑟𝑜 𝑗𝑒𝑐𝑡                                                            modate this, we introduce an abstraction called an error group as
 6:     while 𝑔 ≠ ∅ do                                                             the working unit of the RustAssistant inner loop. An error group
 7:         𝑒 ′ ← choose_any(𝑔)                                                    is a set of errors that RustAssistant is currently trying to fix. An
 8:         𝑝 ← instantiate_prompt(𝑒 ′ )                                           error group is initialized with the input error (line 4) and may grow
 9:         𝑛 ← invoke_llm(𝑚, 𝑝, 𝑁 )                                               or shrink within the loop. The loop terminates when either the
10:         𝑐 ← best_completion(𝑝𝑟𝑜 𝑗𝑒𝑐𝑡, 𝑛)                                       error group becomes empty, implying that the original error 𝑒 was
11:         𝑝𝑟𝑜 𝑗𝑒𝑐𝑡 ← apply_patch(𝑝𝑟𝑜 𝑗𝑒𝑐𝑡, 𝑐)                                    fixed, or RustAssistant gives up on the error group (line 13), in
12:         𝑔 ← check(𝑝𝑟𝑜 𝑗𝑒𝑐𝑡) − 𝑒𝑟𝑟𝑠                                             which case the project is restored to its initial state at the beginning
13:         if giveup() then                                                       of the output loop. We now explain the body of the inner loop.
14:             𝑝𝑟𝑜 𝑗𝑒𝑐𝑡 ← 𝑠𝑛𝑎𝑝
15:             break                                                                   Prompt construction ( instantiate_prompt). For each error
16:         end if                                                                 (𝑒 ′ ) in the current error group, RustAssistant constructs a prompt
17:     end while                                                                  𝑝, shown in Figure 4 (the headings are for illustration purposes
18:     𝑒𝑟𝑟𝑠 ← check(𝑝𝑟𝑜 𝑗𝑒𝑐𝑡)                                                     only), asking for a fix to the error. The prompt is parameterized over
19: end while
                                                                                   error-specific content, using the ‘{}’ syntax. The preamble section
                                                                                   instantiates the checker command that was used (cmd). The next
                                                                                   section of the prompt contains the error and its textual explanation.
    RustAssistant is a command-line tool that takes as input the                   For the Rust compilation errors, the errors are self-explanatory,
filesystem path to a Rust project, potentially with errors. For in-                so we use the text from the error message as its explanation. For
stance, the project may have compilation errors, reported by the                   the Clippy lint errors, we use the Rust command cargo clippy
Rust compiler, or linting errors reported by a tool like Rust Clippy               --explain ERROR_CODE to fill-in the explanation. This is followed by
[48]. We keep the notion of the underlying checker (Rust compiler                  code snippet(s) that RustAssistant deems necessary to present to
or clippy) and the errors (build errors or lint errors) abstract in this           the LLM for fixing the error. These are obtained by first identifying
section. RustAssistant parses the project to build an in-memory                    source locations in the error. The Rust compiler, for instance, not
index of the Rust source files. The index allows RustAssistant to                  just points to the error location, but to related locations as well.
                                                                                       Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, and Aseem Rastogi


In the example error message below, the location after note is a                            RustAssistant prompt template preamble
related location:                                                          You are given the below error from running '{ cmd } ' and Rust code
                                                                           snippets from one or more '.rs ' files related to this error .
   error[E0369]: binary operation `>=' cannot be applied to `Verbosity'
   −−> src/logger.rs:53:21                                                            Prompt context with error information and code snippets
      |
   53 | if self.verbosity >= Verbosity::Exhaustive {                       { error } { error_explanation }
      | −−−−−−−−−−− ^^^ −−−−−−−−−−−−−                                      ---
   note: an implementation of `PartialOrd<_>' might be missing             { code_snippets }
   −−> src/logger.rs:16:1
      |                                                                                           Instructions for fixing the error
   16 | pub enum Verbosity {                                               Instructions : Fix the error on the above code snippets . Not every
      | ^^^^^^^^^^^^^^^^ must implement `PartialOrd<_>'                    snippet might require a fix or be relevant to the error , but take
   help: consider annotating with `#[derive(PartialEq, PartialOrd)]'       into account the code in all above snippets as it could help you
      |                                                                    derive the best possible fix . Assume that the snippets might not
   16 | #[derive(PartialEq, PartialOrd)]                                   be complete and could be missing lines above or below . Do not add
                                                                           comments or code that is not necessary to fix the error . Do not
    RustAssistant then extracts a window of ±50 lines (config-             use unsafe or unstable features ( through '#![ feature (...) ] ') . For
urable) around each location, and adds these snippets to the prompt.       your answer , return one or more ChangeLog groups , each containing
                                                                           one or more fixes to the above code snippets . Each group must be
It also adds the line number for each line of code as a prefix, which      formatted with the below instructions .
helps the LLM to better identify the code lines in the prompt. In an
initial attempt, we tried only extracting code segments in a proper                Instructions and examples for formatting the changelog output

lexical scope (e.g., the entire body of a function where a relevant        Format instructions : Each ChangeLog group must start with a
                                                                           description of its included fixes . The group must then list one
line appears). This not only increase the complexity of our tooling        or more pairs of ( OriginalCode , FixedCode ) code snippets . Each
(because one needs to parse the Rust code and obtain an AST) but           OriginalCode snippet must list all consecutive original lines of
we also found that LLMs are robust even to non-lexical scopes. We,         code that must be replaced ( including a few lines before and
                                                                           after the fixes ) , followed by the FixedCode snippet with all
hence, decided in favor of keeping our tooling simple.                     consecutive fixed lines of code that must replace the original
    The next section of the prompt (instructions) are simple in-           lines of code ( including the same few lines before and after the
                                                                           changes ). In each pair , the OriginalCode and FixedCode snippets
structions that ask for a fix. For instance, it instructs the model to     must start at the same source code line number N. Each listed
avoid adding unsafe code, in an effort to keep the tool focused on         code line , in both the OriginalCode and FixedCode snippets , must
generating good Rust code.                                                 be prefixed with [N] that matches the line index N in the above
                                                                           snippets , and then be prefixed with exactly the same whitespace
    The final section of the prompt contains instructions to the           indentation as the original snippets above .
LLM for formatting the output, as a list of one or more change             ---
logs. Each changelog begins with an ID numbered starting with 1            ChangeLog :1@ < file >
                                                                           FixDescription : < summary >.
and the source file to which it is applied (ChangeLog line in Fig-         OriginalCode@4 -6:
ure 4). Next is free-form description of the fix (FixDescription           [4] < white space > < original code line >
                                                                           [5] < white space > < original code line >
line). This description is not parsed; it is only to enable scratchpad     [6] < white space > < original code line >
reasoning in the model [38]. Next is a repetition of a part of the         FixedCode@4 -6:
input code that was provided to the model (OriginalCode). This             [4] < white space > < fixed code line >
                                                                           [5] < white space > < fixed code line >
part is defensive because it is a repetition of the input; RustAs-         [6] < white space > < fixed code line >
sistant rejects the changelog if the OriginalCode segment fails            OriginalCode@9 -10:
to match the actual original code. Finally, the output must have           [9] < white space > < original code line >
                                                                           [10] < white space > < original code line >
the fixed code (FixedCode) that should replace all the lines of the        FixedCode@9 -9:
original code. If this segment is empty, for example, then it implies      [9] < white space > < fixed code line >
                                                                           ...
that the corresponding original code segment should be deleted.            ChangeLog :K@ < file >
There are other defensive checks in the changelog format: each             FixDescription : < summary >.
of OriginalCode and FixedCode segments must mention the line               OriginalCode@15 -16:
                                                                           [15] < white space > < original code line >
number range; and this number range repeats again in the code              [16] < white space > < original code line >
segment. All such checks act as a guard; change logs are rejected          FixedCode@15 -17:
when this information fails to match.                                      [15] < white space > < fixed code line >
                                                                           [16] < white space > < fixed code line >
                                                                           [17] < white space > < fixed code line >
   LLM invocation ( invoke_llm). Once the prompt is instanti-
                                                                           OriginalCode@23 -23:
ated, RustAssistant invokes the LLM with the prompt (line 9)               [23] < white space > < original code line >
asking for 𝑁 completions, essentially, 𝑁 responses to the same             FixedCode@23 -23:
                                                                           [23] < white space > < fixed code line >
prompt. On receiving these completions, RustAssistant ranks                ---
them and picks the best completion (line 10). To rank the comple-          Answer :
tions, RustAssistant applies all the changelogs in a completion
and counts the number of resulting errors reported by the checker.               Figure 4: The RustAssistant prompt template.
The completion that results in the least number of errors is ranked
the highest. This is, in essence, a best-first search strategy.           with the inner loop. When the inner loop completes, RustAssis-
   The best completion is applied to the project (line 11), the current   tant updates the set of pending errors (line 18) because it is possible
error group is updated (line 12) and RustAssistant then continues         that fixing one error group caused the errors to change. (As a detail,
Fixing Rust Compilation Errors using LLMs


errors that were previously given up, on line 13, are not tried again;    these test cases are designed to specify the intended semantics of
but this is omitted from the algorithm).                                  the programs.
   RustAssistant uses a few heuristics to ensure termination of           Top-100 crates: For a more comprehensive real-world evaluation,
the inner and the outer loops. First, it provides a configurable option   we look at the GitHub repositories of the top-100 Rust crates (the
(default 100) to limit the maximum number of unique errors that an        most widely-used Rust library packages) from crates.io [49]. We
error group can have over its lifetime in the inner loop. If this limit   examine the history of these repositories and identify commits
is reached, the inner loop gives up. Second, if the set of errors in      that have compilation errors (we clone the commits and build them
an error group does not change across iterations of the inner loop,       locally, we also filter out commits where the errors are out-of-scope).
RustAssistant considers it as not making progress and gives up            We found 182 such commits. The benchmark then is to fix the
on the error group. The outer loop is bounded to run for as many          commits so that they pass the Rust typechecker. In our evaluation,
iterations as the initial number of errors obtained on line 1. (For the   we manually audit the fixes to check whether they preserve the
purpose of checking if two errors are same, which is needed when          intended semantics (see RQ4 in Section 5).
performing set operations, RustAssistant represents an error as              To build a dataset of lint errors, we pick top-10 crates, and run
the concatenation of its error code, error message, and the file name,    rust-clippy on the latest commit in the main branch of their cor-
without any line numbers.)                                                responding GitHub repositories. Clippy [48] is one of the most
                                                                          popular open-source static analysis tool for Rust with roughly 10K
                                                                          stars on GitHub. It is designed to help developers write idiomatic,
4    RUST ERROR DATASET                                                   efficient, and bug-free Rust code by providing a set of predefined
We build a dataset of Rust compilation errors collected from three        linting rules. Clippy also provides helpful messages and sugges-
different sources, as well as linting errors from Clippy [48] tool.       tions to guide developers in making improvements to their code.
Micro-benchmarks: Rust offers a comprehensive catalog of errors,          Fixing Clippy errors tests the ability of RustAssistant to general-
indexed by error codes, that the Rust compiler may emit. The catalog      ize beyond compilation errors. Our dataset has a total of 346 Clippy
is accompanied by small programs that trigger the specific error          errors.
codes [50]. To build our micro-benchmarks dataset, we wrote small            Clippy has multiple categories of checks [48]. For our dataset,
Rust programs, one per error code, designed specially to trigger          we only consider Pedantic, Complexity, and Style. The rest of the
that error code. Although we wrote these programs ourselves, we           categories did not raise errors in the top-10 crates. Additionally,
used the snippets in the Rust catalog as a reference.                     there is a category called Nursery, but it consists of lints that are not
   We consider 270 error codes out of a total of 506. We exclude          yet stable, so we exclude it from our consideration. Pedantic refers
error codes that are no longer relevant in the latest version of the      to stylistic or convention violations, Complexity refers to unneces-
Rust compiler (1.67.1). Additionally, we exclude all errors related to    sarily complex or convoluted code that hamper maintainability, and
package use, build configuration files, and foreign function interop,     Style covers various linting rules related to code style and best prac-
as well as error codes on the use of unsafe; as mentioned in Section 2,   tices, focusing on conventions such as naming, spacing, formatting,
these errors are out-of-scope for us. We also create a unit test for      and other stylistic aspects of the code.
each error code that specifies the intended behavior of the program.
We define passing this test as the measure that the compilation           5    EVALUATION
error is fixed in a semantics-preserving way.                             The evaluation of RustAssistant is designed to answer the fol-
   We further classified each of the errors codes into one of the         lowing research questions:
six categories: Syntax, Type, Generics, Traits, Ownership, and Life-
                                                                             (1) RQ1: To what extent is RustAssistant successful in fixing
time. The primary objective of this benchmark is to determine if
                                                                                 Rust compilation errors?
RustAssistant is more proficient at fixing certain types of errors
                                                                             (2) RQ2: How effective are different prompting strategies and
compared to others.
                                                                                 algorithmic variations?
Stack Overflow (SO) code snippets: Stack Overflow (SO) is a
                                                                             (3) RQ3: Can RustAssistant generalize to fix errors reported
popular online community where programmers and developers seek
                                                                                 by a Rust static analyzer?
help for coding issues. We manually scrape SO to collect questions
                                                                             (4) RQ4: How accurate are the fixes generated by RustAssis-
about Rust compilation errors. To limit the effort, we concentrate
                                                                                 tant for real-world code repositories?
on memory-safety and thread-safety issues, two areas in which the
Rust type system is stricter than C/C++.                                     LLM Configuration. For creative and unconstrained responses,
   To ensure that the questions are relevant and substantial, we          we set both the frequency_penalty and presence_penalty pa-
apply some filtering criteria. For example, we require each question      rameters to 0. We also adopted a deterministic approach by using
to have at least one answer and exclude cases that deem trivial (e.g.,    top_p=1, meaning that the most likely token is selected at each gen-
the question is misclassified or contains syntax errors unrelated to      eration step. To maintain the focus and consistency of the outputs,
the intended category). After applying these filtering criteria, we       we opt for a low temperature of 0.2. While the maximum length
select the first 50 most relevant questions.                              of the generated output is set to the default value of 800 tokens,
   Code snippets in these questions are not always self-contained.        in practice, our experiments primarily involve returning concise
We manually add code and stubs to scope the compilation issue             changelog snippets, which are significantly smaller in length.
to only what was asked in the corresponding SO question. We                  We evaluate both GPT-3.5-turbo (300B parameters) [40] (which
manually add test cases also. Similar to the micro-benchmarks,            we call as GPT-3.5 in this paper) and GPT-4 [41]; a comparison
                                                                                                                                                                            Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, and Aseem Rastogi


                                                                                                 #Failures




                                                                                                                                  Number of solved benchmarks
                                                                                                                                                                250

           Model #N                                  Fix%           #Fixed            Format Build Test
                                           1        52.96%         143 / 270               59                  56           12
  GPT-3.5                                                                                                                                                       200
                                           5        73.70%         199 / 270               44                  10           17
                                           1        92.22% 249 / 270                        ✗                   8           13
                          GPT-4                                                                                                                                 150
                                           5        92.59% 250 / 270                        1                   5           14
                                                                                                                                                                                                                                                                        GPT-3.5
Table 1: Evaluation on the 270 error code micro-benchmarks.                                                                                                                                                                                                             GPT-4
                                                                                                                                                                100
                                                                                                                                                                        1       2       3       4        5       6       7       8       9        10    11    12   13   14   15
                                                                                                                                                                                                    Number of inner-loop iterations
                                                                                 GPT-3.5 (5N)               GPT-4 (5N)
                                                                                                                                                                Figure 6: Iterations required for micro-benchmarks.
    Fix rate in percentage (%)




                                 100
                                  90
                                  80
                                  70




                                                                                                                                  Number of solved benchmarks
                                                                                                                                                                40
                                  60
                                  50                                                                                                                            35
                                  40
                                                                                                                                                                30
                                  30
                                  20                                                                                                                            25
                                  10
                                                                                                                                                                20
                                   0
                                       Syntax       Type     Generics   Traits     Ownership    Lifetime        Total                                           15

Figure 5: Comparing the fix rate % of GPT-3.5 and GPT-4                                                                                                         10
                                                                                                                                                                                                                                                                        GPT-3.5
(both with 𝑁 = 5) across error code categories.                                                                                                                  5
                                                                                                                                                                                                                                                                        GPT-4
                                                                                                                                                                 0
                                                                                                                                                                       1    2       3       4        5       6       7       8       9       10    11    12   13   14   15   16
                                                                                                                                                                                                Number of inner-loop iterations
                                                                                               #Failures
                                                                                                                                                                     Figure 7: Iterations required for SO benchmarks.
                                  Model #N Fix% #Fixed Format Build Test
                                                1          24%     12 / 50             18                  18           2
                     GPT-3.5                                                                                                                                         Model #N Commits% #Commits Errors% #Errors
                                                5          50%     25 / 50             21                  2            2
                                                                                                                                                                                    1           30.22%                   55 / 182                  44.76% 414 / 925
                                                1      74%        37 / 50              1                   7            5                                       GPT-3.5
                                   GPT-4                                                                                                                                            5           35.71%                   65 / 182                  55.03% 509 / 925
                                                5      72%        36 / 50              3                   4            7
                                                                                                                                                                                    1           54.40%                    99 / 182                 86.05% 796 / 925
                                                                                                                                                                      GPT-4
Table 2: Evaluation on 50 benchmarks from Stack Overflow.                                                                                                                           5           73.63%                   134 / 182                 91.46% 846 /925

                                                                                                                                                                      Table 3: Evaluation on the top-100 Rust crates.
between them helps understand the effect of model scaling on
RustAssistant’s accuracy. For both LLMs, we also vary the number
of LLM completions (#N) from 1 to 5 to provide insights into the                                                                 𝑁 = 1. We also notice that GPT-3.5 often fails to follow our for-
optimal balance between computation time and quality of the fixes.                                                               matting requirement in its output (59 failures with 𝑁 = 1) or fails
    RQ1 “To what extent is RustAssistant successful in fixing Rust                                                               to satisfy the compiler (56 failures with 𝑁 = 1). GPT-4 outshines
compilation errors?” For micro-benchmarks and SO code snippets,                                                                  GPT-3.5 on these aspects. Interestingly, sometimes it produces a fix
we report fix rate (Fix%) as the percentage of the programs that build                                                           that fails the corresponding unit test (13 test failures with 𝑁 = 1);
and pass their associated unit test after running RustAssistant. A                                                               the following is an example:
generated fix can fail for three reasons: (1) Format Errors, where
                                                                                                                                                   pub fn get_value() → f64 {
the generated changelog is not correctly formatted, or the format                                                                                    let mut val: f64 = 7.0;
is correct but the original code or lines do not match, leading to the                                                                               val <<= 2.0;
                                                                                                                                                     val
rejection of the changelog; (2) Build Errors, the fix when applied                                                                                 }
still results in compilation errors; (3) Failed Tests, there are no
formatting or compilation errors, but the corresponding unit test                                                                   This code fails to build because it uses the bitwise operator <<=
fails. For the top-100 crates benchmark, we report the number                                                                    on a floating point value (error code E0368). GPT-4 proposes a fix
(percentage) of commits that successfully compile after running                                                                  to change the operator to multiplication, but it keeps the unit as
our tool. We also report the number (percentage) of compilation                                                                  2.0, instead of changing it to 4.0. An alternate fix could have been
errors fixed across all the commits.                                                                                             to use u32 instead of f64 in the example. Expectedly, the GPT-4 fix
    Table 1 shows the performance of RustAssistant on the micro-                                                                 fails our unit test.
benchmarks, achieving a peak accuracy of 92.59%. GPT-4’s perfor-                                                                    Figure 5 shows the fix rate across different error code categories
mance is significantly better than GPT-3.5, so model scaling helps.                                                              (outlined in Section 4). The performance of the models is fairly
Increasing the number of completions helps, but only minimally                                                                   consistent across categories, suggesting that there are no specific
for GPT-4, potentially because its fix rate is already very high with                                                            error codes that are easier or harder for the models to fix.
Fixing Rust Compilation Errors using LLMs


   Table 2 presents results on SO benchmarks. Overall trends, with            Model Prompt G #N Commits% #Commits Errors% #Errors
respect to the two models and the number of completions, are                                       1     9.89%      18 / 182     32.22% 298 / 925
                                                                            GPT-3.5      P0    ✓
similar to Table 1. However, the Fix percentages are consistently                                  5     8.79%      16 / 182     41.30% 382 / 925
lower. RustAssistant is able to achieve a peak fix percentage of
                                                                                                   1    9.89%       18 / 182     4.97% 46 / 925
74% demonstrating that these benchmarks are harder. Indeed as               GPT-3.5      P4    ✗
                                                                                                   5    32.42%      59 / 182     13.95% 129 / 925
the code snippet in Section 1 shows, these examples use non-trivial
Rust concepts.
                                                                                  Table 4: Ablations on the top-100 Rust packages.
   Across the micro-benchmarks and SO benchmarks, we manu-
ally investigate the reasons for failure. In some cases, the model                                                               #Failures
suggests a correct partial fix but then does not follow up with the
additional fixes required. In other cases, it gets stuck in a loop              Prompt Variant           Fix%    #Fixed Format Build Test
where it proposes a fix and undoes it in the next iteration, causing        P1 ChangeLog-basic 10.74% 29 / 270                 236     2      3
RustAssistant to give up. In a few cases, the model tries to import         P2 Line prefixes     24.07% 65 / 270               197     4      4
a package that it needs, but RustAssistant is not prepared to edit          P3 Localization      58.15% 157 / 270               67     35     11
the .toml project file for actually doing the import. It is possible        P4 Description first 73.70% 199 / 270               44     10     17
that further refinement of the LLM prompt can fix such issues; we
leave it for future work.                                                   Table 5: Evaluating variants of the RustAssistant prompt
   For the cases where RustAssistant produced a correct fix, Fig-           template on the Rust error code micro-benchmarks with
ures 6 and 7 show the number of iterations of the inner-loop re-            GPT-3.5.
quired for micro-benchmarks and SO benchmarks, respectively.
GPT-4 requires at most 6 iterations for micro-benchmarks, but up               Table 4 shows the results on the top-100 crates benchmark. We
to 15 iterations in the harder SO benchmarks. GPT-3.5 typically             see that P0 results in very poor performance (compare its first
requires much higher number of iterations. In several cases, the            two rows with those of Table 3). We found that the model, when
iterations were indeed required; for instance, if the type of a func-       returning the fixed code snippet would get tempted in making code
tion parameter is changed (by, say, adding the mut qualifier) then          changes that were unrelated to the task of fixing the compiler error.
the function call sites also need to change, etc.                           This justifies the need for investing in changelog format to keep
   Table 3 presents results on the top-100 crates benchmark. Rus-           the model focused on the fix.
tAssistant is able to achieve an impressive peak accuracy of 91.46%            Table 4 also shows that turning off grouping significantly drops
in terms of fixing errors, matching what is also observed in the            the error fix rate (compare the last two rows of Table 4 with the first
micro-benchmarks. When we consider the ability to fix all errors            two rows of Table 3). Without grouping, RustAssistant would fix
in a commit, the fix rate is lower, but still impressive at 73.63%, i.e.,   errors in a random order, which increased the chances of it getting
roughly three-fourths of the commits could have been automatically          stuck with an error that it could not fix, leading to a ever-increasing
fixed!                                                                      blow-up of code changes and resulting errors. Error grouping helps
   RQ2 “How effective are different prompting strategies and algo-          in detecting such cases, allowing RustAssistant to gracefully give
rithmic variations?” We perform an ablation study by permuting              up on them, and then move on to the other errors in the project.
between different prompting and algorithmic variations, in order to         This justifies the importance of error grouping.
identify the most effective features of RustAssistant. We consider             Table 5 presents the results for prompt ablations with GPT-3.5
five prompt variants, which differ in the way RustAssistant asks            (we skip GPT-4 due to limited capacity with the model). It demon-
LLMs to output the fixes, i.e. the output formatting instructions.          strates that the addition of each new feature to the changelog format
                                                                            raises accuracy by a significant margin. The basic format (P1) only
    (1) P0 (Basic): This variant serves as the baseline. It does not        provides roughly 10% accuracy. We saw that P1 response would
        have the changelog section; it instead asks for the complete        trip most on the formatting of its output, an important requirement
        revised snippets.                                                   in order to handle large code bases. The number of formatting er-
    (2) P1 (ChangeLog-basic): This uses the changelog, but only             rors reduce significantly as the changelog format is improved. It is
        the FixedCode section, without the line number prefixes.            interesting that the simple act of describing the fix (going from P3
    (3) P2 (Line prefixes): In addition to P1, we require line num-         to P4), helps the model accuracy significantly.
        ber prefixes in front of code snippets.                                RQ3 “Can RustAssistant generalize to fix errors reported by a
    (4) P3 (Localization): In addition to P2, we require the original       Rust static analyzer?” Fixing Clippy errors tests the ability of Rus-
        code section.                                                       tAssistant to generalize beyond compilation errors. Clippy also
    (5) P4 (Description first): This is the full prompt of Figure 4,        comes with an auto-fix option that is based on pattern-matching.
        i.e., P3 with the FixDescription section.                           We use it as a baseline for comparison.
                                                                               Table 6 present the results on fixing Clippy errors. RustAssis-
   For algorithmic ablations, we vary the number of completions             tant is able to fix 2.4x more errors than Clippy’s own auto-fix
(#N) to either 1 or 5 (already reported for RQ1), and we turn off error     option, achieving a peak accuracy of nearly 75%. The accuracy on
grouping. Without error grouping, the RustAssistant algorithm               Complexity and Style categories exceeds 90%.
has a single loop that attempts to fix one error at a time from the            RQ4 “How accurate are the fixes generated by RustAssistant
current bag of errors.                                                      for real-world code repositories?” To answer RQ4, we qualitatively
                                                                                         Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, and Aseem Rastogi


                                Clippy               RustAssistant             The fix produced by RustAssistant follows the suggestion in
        Category          Fix%        #Fixed         Fix%        #Fixed     the error, and comes up with the following patch:
      Complexity         50.00%       17 / 34       91.18%       31 / 34      - let actual = atom.compare_and_swap(ptr as _, shared as _, Ordering::AcqRel);
                                                                              + let actual = atom.compare_exchange(ptr as _, shared as _, Ordering::AcqRel,
        Pedantic         26.12%      76 / 291       71.48%      208 / 291                                         Ordering::Acquire).unwrap_or_else(|x| x);
           Style         76.19%       16 / 21       95.24%       20 / 21
                                                                               The third category, non-matching but same runtime behavior,
               Total     31.50%      109 / 346      74.86%      259 / 346   classifies the fixes where the fix produced by RustAssistant does
Table 6: Evaluating RustAssistant (GPT-4) against Clippy’s                  not match the fix in the repository, but to the best-of-our estimation,
auto-fix on the top-10 Rust packages.                                       the fix does not alter the runtime behavior of the program (recall
                                                                            that the fix passes the Rust typechecker). This is an interesting
                                                                # Commits   category where the LLM produces reasonable fixes that do not
                                                                            match the programmer intent.
    Unambiguous                                                       55
                                                                               One example in this category is the following error:
    Matching                                                          41
    Non-matching, same runtime behaviour                              29      error[E0015]: cannot call non−const fn `ArrayString::<CAP>::capacity`
                                                                              in constant functions
    Different runtime behavior                                        9
Table 7: Analysis of fixed commits in the top-100 benchmark                   The error is in a function defined as const:
                                                                              pub const fn remaining_capacity(&self) → usize

                                                                                The compiler complains that the function calls another function
                                                                            capacity , passing it the self argument, but capacity is a non-const
examine the fixes generated by RustAssistant on all the 134 fixed
                                                                            function. LLM chose to fix this error by removing the const qual-
commits from the top-100 crates benchmark. As shown in Table 7,
                                                                            ifier from remaining_capacity, whereas the programmer fixed it
we categorize the commits into 4 categories. The categories are
                                                                            by adding const qualifier to capacity . We found similar instances
defined in term of individual error fixes, and a commit is classified
                                                                            related to other qualifiers such as mut and public.
into a category if all its fixes2 belong to the category or to the cate-
                                                                                Another example in the category is the error in the following
gories above it. For example, a commit is classified as Non-matching,
                                                                             trait definition:
same runtime behavior if all its fixes are either Unambiguous, or
Matching, or Non-matching, same runtime behavior.                             pub trait MendSlice { fn mend(Self, Self) → Result<Self,(Self,Self)>; }
   Unambiguous fixes classify fixes for errors like syntax errors              Rust compiler complains that it needs to statically know the size
(e.g., missing ; or braces), missing instantiations for generics type       of Self , and suggests bounding Self with the Sized trait:
parameters, type-incorrect format string specifiers, etc. Since there
                                                                              error[E0277]: the size for values of type `Self` cannot be known at compilation
is mostly a unique way to fix these errors, and the RustAssistant                     time
fix passes the Rust typechecker, we consider it good.                         −−> src/misc.rs:151:41
   Matching fixes classify the fixes where the fix matches the de-               |
                                                                              151 | fn mend(Self, Self) → Result<Self, (Self, Self)>;
veloper fix in the repository—we checked this by comparing the                   | ^^^^^^^^^^^^ doesn't have a size known at compile−time
patched code from RustAssistant with the corresponding code                      |
                                                                                 = note: only the last element of a tuple may have a dynamically sized type
from the latest commit in the main branch of the repository. This             help: consider further restricting `Self`
category contains non-trivial examples that provide some evidence                |
that the LLMs have learnt common Rust idioms. For example, a                  151 | fn mend(Self, Self) → Result<Self, (Self, Self)> where Self: Sized;
common pattern to destruct a pointer in Rust is to wrap it using              The RustAssistant fix in this case was to bound the Self argu-
Box :: from_raw(ptr), and let the Box destructor call the destructor        ment at the level of MendSlice definition
for the pointer. In a few instances in our benchmark, void return-
                                                                              pub trait MendSlice: {Sized} { fn mend(Self, Self) → Result<Self,(Self,Self)>; }
ing functions had Box :: from_raw(ptr) as the last statement, which
the Rust compiler complains about as unused value. RustAssistant               whereas in the repository, the fix is what the error message
fixes these errors by rewriting it as drop(Box :: from_raw(ptr)), which     suggested. This is an interesting case since the LLM chose to ignore
matches the actual fix in the repository.                                   the suggestion in the error message.
   Similarly, there are examples where the Rust compiler complains             The final category is for the fixes where the changes introduced
about a function modifying an argument through an immutable                 by the LLM, again to the best of our estimation, alter the runtime
reference. RustAssistant fixed such cases by changing the signa-            behavior of the program. In a few of these cases, the LLM patch was
ture of the function to demand &mut references. Another class of            blatantly wrong, e.g., it removed some code, introduced alternate
errors in this category are deprecation warnings/errors, e.g.:              implementations of some unrelated functions, etc. However, in
   error: use of deprecated associated function
                                                                            some cases it was understandable that the LLM patch did not match
   `core::sync::atomic::AtomicPtr::<T>::compare_and_swap`:                  the developer. An example is as follows. Rust supports enumerated
   Use `compare_exchange` or `compare_exchange_weak` instead                types and a match construct to inspect the variant of the enum
   −−> src/bytes.rs:1002:23
                                                                            and execute different code based on the variant. If the match is not
                                                                            exhaustive, i.e. it doesn’t mention all the variant cases, the compiler
2 Note that a commit can have multiple errors and hence multiple fixes.     raises an error. In a few cases of these errors in our benchmark, LLM
Fixing Rust Compilation Errors using LLMs


got it right (e.g., a match that is just converting enum variant name     updated without any prior intimation, which can impact RustAs-
to a string), but when the error occurred in the context of more          sistant’s fix accuracy.
involved match, we found that LLMs came up with a fix different
from the developer.
                                                                          7   RELATED WORK
   Summary. From our evaluation, we conclude that the pre-trained         The area of Automated Program Repair (APR) is concerned with
LLMs seem to have internalized the knowledge of Rust syntax and           the problem of taking as input a “buggy” code fragment as well
commonly used Rust idioms. They also follow the errors and come           as a correctness specification, and producing correct code as out-
up with the relevant and intended fixes in most cases. They do,           put. This process is very fundamental to software engineering and,
however, require careful prompt construction, and the iteration           consequently, has received much attention from the research com-
with a compiler was necessary especially for propagating changes          munity [12, 14, 34]. Our work can be considered as an instance of
across different parts of the code.                                       the APR problem, where the buggy code is the current version of
   It is interesting future work to see if we can embed more Rust         Rust code on a developer’s machine that does not compile, and the
idioms in the LLM prompt to match the developer intention, basi-          correctness specification is to pass the compiler. We elaborate on a
cally try to move the cases in the third category of Table 7 to the       comparison between our approach and existing APR solutions.
second. For example, we can instruct the LLM to first try fixing the         In terms of techniques, some APR solutions are based on classical
code with strict qualifiers (immutable, private , const). We would        (non-learning-based) techniques. Examples include search-based
also need to implement better contextualization to pass the relevant      techniques [18, 27, 30, 55, 56, 62, 68, 70] that have a pre-defined
code snippets in the prompt.                                              space of potential patches and must find one that works in this
                                                                          space. Semantics-based techniques [28, 31, 37, 67] formulate the
                                                                          repair as a constraint that must be solved. Symbolic techniques rely
6    THREATS TO VALIDITY                                                  on manually-designed transformations for constructing the fix [5,
   Internal Threats. One internal threat to validity arises from the      15, 60]. These techniques, by construction, are limited in the space
qualitative examination of the fixes generated by RustAssistant           of possible repairs that they consider. Learning-based approaches
to assess their semantic correctness (RQ4, Section 5). To address this    [1, 4, 13, 19, 20, 25, 53, 59, 63, 69, 71] overcome this limitation by
concern, we implemented a structured consensus-based manual               leveraging deep learning, however, they require supervised training
evaluation involving multiple evaluators, ensuring more reliable          data (pairs of buggy and patched code) which is time-consuming
and consistent assessments. Another potential internal threat is          and expensive to set up. RustAssistant, on the other hand, does
data contamination, where it might be possible that fixes to the          not need training, or even fine-tuning, thus skipping data collection
compilation issues that we mined from open source might have              altogether. It instead uses the latest pre-trained LLMs; these models
already been included in the training data of the LLMs that we            are trained on a massive scale, and have the ability of following
used. There is no ideal way to completely remove contamination            generic instructions [42].
without sacrificing real-world scenarios, given the scope of training        The potential of LLMs as powerful APR agents has been acknowl-
data that is consumed for these models today. However, the fixes,         edged in previous studies [7, 21, 22, 43–45, 65, 66]. For instance,
especially for the top-100 benchmarks were never presented online         Xia et al. [65] conducts an extensive study on the application of
in the form of a fix or alongside the corresponding compiler error,       nine state-of-the-art pre-trained language models (PLMs) for APR
to the best of our knowledge. Only the fixed version of the code          on datasets from three different languages. They demonstrate that
might appear in a later version of the repository.                        PLMs outperform existing APR techniques, with larger models
   Additionally, the use of handwritten test cases for micro-             achieving better performance. Fan et al. [7] evaluates the Codex
benchmarks and Stack Overflow code snippets to verify the gen-            edit model [39] on a Java defects dataset from LeetCode [24]. Pren-
erated fixes introduces a potential threat to construct validity. To      ner et al. [45] explores Java and Python implementations of buggy
counter this, we designed the testcases independently from the            algorithms, generating complete fixed functions using LLMs. Build-
RustAssistant’s implementation.                                           ing on this line of work, Xia et al. [66] experiments with newer
   Our evaluation on Rust Clippy errors, while it demonstrates the        LLMs (GPT-3 series, CodeT5 [61], and InCoder [9]), a larger set of
generalizability of RustAssistant to non-compiler errors, was             benchmarks (such as Defects4J [23]), and compares against multiple
limited to checking if the resulting fixes passed clippy. A qualitative   APR tools. Additionally, researchers have investigated the potential
assessment of the generated fix, say, by checking if existing tests       of APR techniques to enhance the reliability of code generated by
continue to pass, or via manual inspection, would be necessary to         LLMs. Jesse et al. [17] examines the generation of single statement
claim that RustAssistant can be readily adopted for fixing clippy         bugs (SStuBs) by Codex and propose avoidance strategies, while
errors.                                                                   Fan et al. [8] systematically studies the use of automated program
                                                                          repair techniques to fix incorrect solutions produced by LLMs in
   External Threats. While our evaluation of RustAssistant en-            LeetCode contests.
compasses an extensive analysis of three Rust error datasets from            The above techniques differ from our work in multiple dimen-
popular sources, we acknowledge that the generalizability of our          sions. First, they rely exclusive on the model to produce the patch,
findings to different datasets may vary.                                  whereas we use a pipeline that iterates with the compiler to arrive
   Furthermore, the nature of API access from OpenAI implies that         at the fix. Second, our focus on Rust is unique. There is relatively
the LLM performance can vary over time as the models may get              much lesser code in Rust compared to Java and Python that the
                                                                                       Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, and Aseem Rastogi


above work had used. It is not immediately evident if LLM-based            This evidence should add encouragement to the wave of building
techniques will carry over to Rust without impacting their accu-         LLM-powered tools for software engineering. We plan to release
racy, justifying the need to study Rust errors. Third, we consider       our dataset to enable further research.
compiler errors as opposed to above work that considered multiple
kinds of functional errors with the requirement of passing given         REFERENCES
test cases. These are different kinds of errors, and moreover, our        [1] Toufique Ahmed, Noah Rose Ledesma, and Premkumar Devanbu. 2023. SynShine:
work does not require the presence of a test suite, making it readily         Improved Fixing of Syntax Errors. IEEE Transactions on Software Engineering
                                                                              49, 4 (2023), 2169–2181. https://doi.org/10.1109/TSE.2022.3212635
deployable in any scenario where the user is ready to build their         [2] Rohan Anil, Andrew M. Dai, Orhan Firat, Melvin Johnson, Dmitry Lepikhin,
code. Furthermore, we leverage the specific nature of errors, namely,         Alexandre Passos, and et al. 2023. PaLM 2 Technical Report. CoRR abs/2305.10403
compiler-generated error messages, for crafting the prompt and                (2023). https://doi.org/10.48550/arXiv.2305.10403 arXiv:2305.10403
                                                                          [3] AWS. 2022. Sustainability with Rust. https://aws.amazon.com/blogs/opensource/
improving accuracy.                                                           sustainability-with-rust/.
   There is also work on fixing statically-detected errors, as op-        [4] Aidan Connor, Aaron Harris, Nathan Cooper, and Denys Poshyvanyk. 2022.
                                                                              Can We Automatically Fix Bugs by Learning Edit Operations?. In 2022 IEEE
posed to fixing of failing test cases, For instance, RING [22] consid-        International Conference on Software Analysis, Evolution and Reengineering
ers retrieval-augmented few-shot prompting to fix syntactic errors            (SANER). 782–792. https://doi.org/10.1109/SANER53432.2022.00096
in multiple languages. It divides the bug-fixing process into three       [5] Andreea Costea, Abhishek Tiwari, Sigmund Chianasta, Kishore R, Abhik Roy-
                                                                              choudhury, and Ilya Sergey. 2021. HIPPODROME: Data Race Repair using
stages: fault localization using language tooling, program trans-             Static Analysis Summaries. CoRR abs/2108.02490 (2021). arXiv:2108.02490
formation through few-shot learning with LLMs, and candidate                  https://arxiv.org/abs/2108.02490
ranking based on token probabilities. RING effectively leverages          [6] Emery Berger. 2023. ChatDBG. https://github.com/plasma-umass/ChatDBG.
                                                                          [7] Zhiyu Fan, Xiang Gao, Martin Mirchev, Abhik Roychoudhury, and Shin Hwei
developer intuition and LLM capabilities to address various types             Tan. 2023. Automated Repair of Programs from Large Language Models. In
of bugs without requiring user intervention. InferFix [21] uses an            45th IEEE/ACM International Conference on Software Engineering, ICSE 2023,
                                                                              Melbourne, Australia, May 14-20, 2023. IEEE, 1469–1481. https://doi.org/10.
LLM to fix errors reported by a static analysis tool (CodeQL). They           1109/ICSE48619.2023.00128
rely on fine-tuning Codex for improved accuracy. Pearce et al. [44]       [8] Zhiyu Fan, Xiang Gao, Martin Mirchev, Abhik Roychoudhury, and Shin Hwei
performs a large scale study to explore the potential of LLMs in au-          Tan. 2023. Automated Repair of Programs from Large Language Models. In
                                                                              2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE).
tomatically repairing cybersecurity bugs. They investigate the use            1469–1481. https://doi.org/10.1109/ICSE48619.2023.00128
of zero-shot vulnerability repair with five commercially available        [9] Daniel Fried, Armen Aghajanyan, Jessy Lin, Sida Wang, Eric Wallace, Freda Shi,
LLMs, an open-source model, and a locally-trained model, which are            Ruiqi Zhong, Scott Yih, Luke Zettlemoyer, and Mike Lewis. 2023. InCoder: A
                                                                              Generative Model for Code Infilling and Synthesis. In The Eleventh International
evaluated on a mix of synthetic, handcrafted, and real-world secu-            Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5,
rity bug scenarios. FitRepair [64] combines LLMs in cloze-style APR           2023. OpenReview.net. https://openreview.net/pdf?id=hQwb-lbM6EL
                                                                         [10] GitHub. 2022. GitHub Copilot. https://github.com/features/copilot.
with insights from the plastic surgery hypothesis. Their method          [11] GitHub. 2023. GitHub Copilot-X. https://github.com/features/preview/copilot-x.
involves training two separate models using innovative fine-tuning       [12] Claire Le Goues, Michael Pradel, and Abhik Roychoudhury. 2019. Automated
strategies: Knowledge-Intensified fine-tuning, and Repair-Oriented            program repair. Commun. ACM 62, 12 (2019), 56–65. https://doi.org/10.1145/
                                                                              3318162
fine-tuning. Additionally, it introduces a Relevant-Identifier prompt-   [13] Rahul Gupta, Soham Pal, Aditya Kanade, and Shirish K. Shevade. 2017. DeepFix:
ing strategy by using information retrieval and static analysis to            Fixing Common C Language Errors by Deep Learning. In Proceedings of the
obtain a list of relevant/rare identifiers not seen in the model’s            Thirty-First AAAI Conference on Artificial Intelligence, February 4-9, 2017, San
                                                                              Francisco, California, USA, Satinder Singh and Shaul Markovitch (Eds.). AAAI
immediate context. Our work does not rely on fine-tuning, and                 Press, 1345–1351. http://aaai.org/ocs/index.php/AAAI/AAAI17/paper/view/
instead utilizes iterative fixing with instruction-tuned LLMs. We do,         14603
                                                                         [14] Kai Huang, Zhengzi Xu, Su Yang, Hongyu Sun, Xuejun Li, Zheng Yan,
however, believe that RustAssistant can benefit from few-shot                 and Yuqing Zhang. 2023. A Survey on Automated Program Repair Tech-
prompting where similar examples of fixing a particular compiler              niques. CoRR abs/2303.18184 (2023). https://doi.org/10.48550/arXiv.2303.18184
error as provided as part of the prompt [36]. We leave this direction         arXiv:2303.18184
                                                                         [15] Zhen Huang, David Lie, Gang Tan, and Trent Jaeger. 2019. Using Safety Properties
as future work.                                                               to Generate Vulnerability Patches. In 2019 IEEE Symposium on Security and
                                                                              Privacy, SP 2019, San Francisco, CA, USA, May 19-23, 2019. IEEE, 539–554. https:
                                                                              //doi.org/10.1109/SP.2019.00071
                                                                         [16] jeromefroe. 2016. Question about a Rust compilation error on Stack Overflow.
                                                                              https://stackoverflow.com/questions/40299671.
                                                                         [17] Kevin Jesse, Toufique Ahmed, Premkumar T. Devanbu, and Emily Morgan.
8   CONCLUSIONS                                                               2023. Large Language Models and Simple, Stupid Bugs. In 2023 IEEE/ACM
                                                                              20th International Conference on Mining Software Repositories (MSR). 563–575.
This paper presents RustAssistant as a tool for automatically                 https://doi.org/10.1109/MSR59073.2023.00082
generating patches for compilation errors in Rust. RustAssistant         [18] Jiajun Jiang, Yingfei Xiong, Hongyu Zhang, Qing Gao, and Xiangqun Chen.
                                                                              2018. Shaping program repair space with existing patches and similar code. In
leverages emergent capabilities of Pre-Trained Large Language                 Proceedings of the 27th ACM SIGSOFT International Symposium on Software
Models to deliver impressive results. It demonstrates that the latest         Testing and Analysis, ISSTA 2018, Amsterdam, The Netherlands, July 16-21,
advancements in LLMs (e.g., GPT-4 over GPT-3.5) as well as com-               2018, Frank Tip and Eric Bodden (Eds.). ACM, 298–309. https://doi.org/10.
                                                                              1145/3213846.3213871
bining them with formal tools such as a compiler leads to a very         [19] Nan Jiang, Thibaud Lutellier, Yiling Lou, Lin Tan, Dan Goldwasser, and Xiangyu
effective solution for fixing code errors.                                    Zhang. 2023. KNOD: Domain Knowledge Distilled Tree Decoder for Automated
                                                                              Program Repair. arXiv:2302.01857 [cs.SE]
   LLMs are sensitive to the prompts that they are supplied. We          [20] Nan Jiang, Thibaud Lutellier, and Lin Tan. 2021. CURE: Code-Aware Neu-
demonstrate the features that were needed to help the model com-              ral Machine Translation for Automatic Program Repair. In 43rd IEEE/ACM
municate code changes, bring accuracy up from a mere 10% to                   International Conference on Software Engineering, ICSE 2021, Madrid, Spain,
                                                                              22-30 May 2021. IEEE, 1161–1173. https://doi.org/10.1109/ICSE43902.2021.00107
nearly 74%. We further demonstrate generality of RustAssistant           [21] Matthew Jin, Syed Shahriar, Michele Tufano, Xin Shi, Shuai Lu, Neel Sundaresan,
by auto-fixing rust lint errors.                                              and Alexey Svyatkovskiy. 2023. InferFix: End-to-End Program Repair with
Fixing Rust Compilation Errors using LLMs


     LLMs. CoRR abs/2303.07263 (2023). https://doi.org/10.48550/arXiv.2303.07263             Francisco, CA, USA, May 21-25, 2023. IEEE, 2339–2356. https://doi.org/10.1109/
     arXiv:2303.07263                                                                        SP46215.2023.10179420
[22] Harshit Joshi, José Pablo Cambronero Sánchez, Sumit Gulwani, Vu Le, Ivan           [45] Julian Aron Prenner, Hlib Babii, and Romain Robbes. 2022. Can OpenAI’s
     Radicek, and Gust Verbruggen. 2022. Repair Is Nearly Generation: Multilingual           Codex Fix Bugs?: An evaluation on QuixBugs. In 3rd IEEE/ACM International
     Program Repair with LLMs. CoRR abs/2208.11640 (2022). https://doi.org/10.               Workshop on Automated Program Repair, APR@ICSE 2022, Pittsburgh, PA,
     48550/arXiv.2208.11640 arXiv:2208.11640                                                 USA, May 19, 2022. IEEE, 69–75. https://doi.org/10.1145/3524459.3527351
[23] René Just, Darioush Jalali, and Michael D. Ernst. 2014. Defects4J: a database      [46] Rust Analyzer Team. 2020. Rust Analyzer. https://github.com/rust-lang/rust-
     of existing faults to enable controlled testing studies for Java programs. In           analyzer.
     International Symposium on Software Testing and Analysis, ISSTA ’14, San Jose,     [47] Rust Team. 2023. Rust. https://www.rust-lang.org/.
     CA, USA - July 21 - 26, 2014, Corina S. Pasareanu and Darko Marinov (Eds.).        [48] Rust Team. 2023. Rust Clippy Static Analysis. https://doc.rust-lang.org/clippy.
     ACM, 437–440. https://doi.org/10.1145/2610384.2628055                              [49] Rust Team. 2023. The Rust community’s crate registry. https://crates.io.
[24] LeetCode. 2023. LeetCode Contest. https://leetcode.com/contest.                    [50] Rust Team. 2023. Rust error codes index. https://doc.rust-lang.org/error_codes/
[25] Yi Li, Shaohua Wang, and Tien N. Nguyen. 2020. DLFix: context-based                     error-index.html.
     code transformation learning for automated program repair. In ICSE ’20: 42nd       [51] Rust Team. 2023. Rust Survey. https://blog.rust-lang.org/2022/02/15/Rust-
     International Conference on Software Engineering, Seoul, South Korea, 27 June           Survey-2021.html.
     - 19 July, 2020, Gregg Rothermel and Doo-Hwan Bae (Eds.). ACM, 602–614.            [52] Abulhair Saparov and He He. 2023. Language Models Are Greedy Reasoners: A
     https://doi.org/10.1145/3377811.3380345                                                 Systematic Formal Analysis of Chain-of-Thought. arXiv:2210.01240 [cs.CL]
[26] Linux kernel development community. 2020. Rust in Linux Kernel. https:             [53] Mifta Sintaha, Noor Nashid, and Ali Mesbah. 2023. Katana: Dual Slicing Based
     //docs.kernel.org/next/rust/index.html.                                                 Context for Learning Bug Fixes. ACM Trans. Softw. Eng. Methodol. 32, 4, Article
[27] Kui Liu, Anil Koyuncu, Dongsun Kim, and Tegawendé F. Bissyandé. 2019.                   100 (may 2023), 27 pages. https://doi.org/10.1145/3579640
     AVATAR: Fixing Semantic Bugs with Fix Patterns of Static Analysis Viola-           [54] Stack Overflow. 2021. Stack Overflow survey. https://insights.stackoverflow.
     tions. In 26th IEEE International Conference on Software Analysis, Evolution            com/survey/2021.
     and Reengineering, SANER 2019, Hangzhou, China, February 24-27, 2019, Xinyu        [55] Shin Hwei Tan, Zhen Dong, Xiang Gao, and Abhik Roychoudhury. 2018. Repair-
     Wang, David Lo, and Emad Shihab (Eds.). IEEE, 456–467. https://doi.org/10.              ing crashes in Android apps. In Proceedings of the 40th International Conference
     1109/SANER.2019.8667970                                                                 on Software Engineering, ICSE 2018, Gothenburg, Sweden, May 27 - June 03,
[28] Kui Liu, Shangwen Wang, Anil Koyuncu, Kisub Kim, Tegawendé F. Bissyandé,                2018, Michel Chaudron, Ivica Crnkovic, Marsha Chechik, and Mark Harman
     Dongsun Kim, Peng Wu, Jacques Klein, Xiaoguang Mao, and Yves Le Traon.                  (Eds.). ACM, 187–198. https://doi.org/10.1145/3180155.3180243
     2020. On the efficiency of test suite based program repair. In Proceedings of      [56] Shin Hwei Tan and Abhik Roychoudhury. 2015. relifix: Automated Repair of
     the ACM/IEEE 42nd International Conference on Software Engineering. ACM.                Software Regressions. In 37th IEEE/ACM International Conference on Software
     https://doi.org/10.1145/3377811.3380338                                                 Engineering, ICSE 2015, Florence, Italy, May 16-24, 2015, Volume 1, Antonia
[29] Mark Russinovich. 2023. Rust in the Windows kernel. https://twitter.com/                Bertolino, Gerardo Canfora, and Sebastian G. Elbaum (Eds.). IEEE Computer
     markrussinovich/status/1656416376125538304?lang=en.                                     Society, 471–482. https://doi.org/10.1109/ICSE.2015.65
[30] Sergey Mechtaev, Xiang Gao, Shin Hwei Tan, and Abhik Roychoudhury. 2018.           [57] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne
     Test-Equivalence Analysis for Automatic Patch Generation. ACM Trans. Softw.             Lachaux, Timothée Lacroix, and et al. 2023. LLaMA: Open and Efficient Founda-
     Eng. Methodol. 27, 4 (2018), 15:1–15:37. https://doi.org/10.1145/3241980                tion Language Models. CoRR abs/2302.13971 (2023). https://doi.org/10.48550/
[31] Sergey Mechtaev, Jooyong Yi, and Abhik Roychoudhury. 2016. Angelix: scalable            arXiv.2302.13971 arXiv:2302.13971
     multiline program patch synthesis via symbolic analysis. In Proceedings of the     [58] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yas-
     38th International Conference on Software Engineering, ICSE 2016, Austin, TX,           mine Babaei, and et al. 2023. Llama 2: Open Foundation and Fine-Tuned Chat
     USA, May 14-22, 2016, Laura K. Dillon, Willem Visser, and Laurie A. Williams            Models. CoRR abs/2307.09288 (2023). https://doi.org/10.48550/arXiv.2307.09288
     (Eds.). ACM, 691–701. https://doi.org/10.1145/2884781.2884807                           arXiv:2307.09288
[32] Microsoft. 2023. AI powered Bing. https://blogs.microsoft.com/blog/2023/02/07/     [59] Michele Tufano, Cody Watson, Gabriele Bavota, Massimiliano Di Penta, Martin
     reinventing-search-with-a-new-ai-powered-microsoft-bing-and-edge-your-                  White, and Denys Poshyvanyk. 2019. An Empirical Study on Learning Bug-
     copilot-for-the-web/.                                                                   Fixing Patches in the Wild via Neural Machine Translation. ACM Trans. Softw.
[33] Microsoft. 2023. Microsoft 365 Copilot. https://blogs.microsoft.com/blog/2023/          Eng. Methodol. 28, 4 (2019), 19:1–19:29. https://doi.org/10.1145/3340544
     03/16/introducing-microsoft-365-copilot-your-copilot-for-work/.                    [60] Rijnard van Tonder and Claire Le Goues. 2018. Static automated program repair
[34] Martin Monperrus. 2018. Automatic Software Repair: A Bibliography. ACM                  for heap properties. In Proceedings of the 40th International Conference on
     Comput. Surv. 51, 1 (2018), 17:1–17:24. https://doi.org/10.1145/3105906                 Software Engineering, ICSE 2018, Gothenburg, Sweden, May 27 - June 03, 2018,
[35] MSRC Team. 2023. A proactive approach to more secure code. https://msrc.                Michel Chaudron, Ivica Crnkovic, Marsha Chechik, and Mark Harman (Eds.).
     microsoft.com/blog/2019/07/a-proactive-approach-to-more-secure-code/.                   ACM, 151–162. https://doi.org/10.1145/3180155.3180250
[36] Noor Nashid, Mifta Sintaha, and Ali Mesbah. 2023. Retrieval-Based Prompt           [61] Yue Wang, Weishi Wang, Shafiq R. Joty, and Steven C. H. Hoi. 2021. CodeT5:
     Selection for Code-Related Few-Shot Learning. In 45th IEEE/ACM International            Identifier-aware Unified Pre-trained Encoder-Decoder Models for Code Under-
     Conference on Software Engineering, ICSE 2023, Melbourne, Australia, May                standing and Generation. In Proceedings of the 2021 Conference on Empirical
     14-20, 2023. IEEE, 2450–2462. https://doi.org/10.1109/ICSE48619.2023.00205              Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta
[37] Hoang Duong Thien Nguyen, Dawei Qi, Abhik Roychoudhury, and Satish Chan-                Cana, Dominican Republic, 7-11 November, 2021, Marie-Francine Moens, Xuan-
     dra. 2013. SemFix: program repair via semantic analysis. In 35th International          jing Huang, Lucia Specia, and Scott Wen-tau Yih (Eds.). Association for Computa-
     Conference on Software Engineering, ICSE ’13, San Francisco, CA, USA, May               tional Linguistics, 8696–8708. https://doi.org/10.18653/v1/2021.emnlp-main.685
     18-26, 2013, David Notkin, Betty H. C. Cheng, and Klaus Pohl (Eds.). IEEE Com-     [62] Ming Wen, Junjie Chen, Rongxin Wu, Dan Hao, and Shing-Chi Cheung.
     puter Society, 772–781. https://doi.org/10.1109/ICSE.2013.6606623                       2018. Context-aware patch generation for better automated program repair.
[38] Maxwell I. Nye, Anders Johan Andreassen, Guy Gur-Ari, Henryk Michalewski, Ja-           In Proceedings of the 40th International Conference on Software Engineering,
     cob Austin, David Bieber, David Dohan, Aitor Lewkowycz, Maarten Bosma, David            ICSE 2018, Gothenburg, Sweden, May 27 - June 03, 2018, Michel Chaudron,
     Luan, Charles Sutton, and Augustus Odena. 2021. Show Your Work: Scratchpads             Ivica Crnkovic, Marsha Chechik, and Mark Harman (Eds.). ACM, 1–11. https:
     for Intermediate Computation with Language Models. CoRR abs/2112.00114                  //doi.org/10.1145/3180155.3180233
     (2021). arXiv:2112.00114 https://arxiv.org/abs/2112.00114                          [63] Martin White, Michele Tufano, Christopher Vendome, and Denys Poshy-
[39] OpenAI. 2023. Codex Edit Model. https://openai.com/blog/gpt-3-edit-insert.              vanyk. 2016. Deep learning code fragments for code clone detection. In
[40] OpenAI. 2023. GPT-3.5. https://platform.openai.com/docs/models/gpt-3-5.                 Proceedings of the 31st IEEE/ACM International Conference on Automated
[41] OpenAI. 2023. GPT-4 Technical Report. CoRR abs/2303.08774 (2023). https:                Software Engineering, ASE 2016, Singapore, September 3-7, 2016, David Lo, Sven
     //doi.org/10.48550/arXiv.2303.08774 arXiv:2303.08774                                    Apel, and Sarfraz Khurshid (Eds.). ACM, 87–98. https://doi.org/10.1145/2970276.
[42] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright,                2970326
     Pamela Mishkin, and et al. 2022. Training language models to follow instructions   [64] Chunqiu Steven Xia, Yifeng Ding, and Lingming Zhang. 2023. Revisiting the
     with human feedback. In NeurIPS. http://papers.nips.cc/paper_files/paper/2022/          Plastic Surgery Hypothesis via Large Language Models. arXiv:2303.10494 [cs.SE]
     hash/b1efde53be364a73914f58805a001731-Abstract-Conference.html                     [65] Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. 2022. Practical Program
[43] Hammond Pearce, Benjamin Tan, Baleegh Ahmad, Ramesh Karri, and Brendan                  Repair in the Era of Large Pre-trained Language Models. arXiv:2210.14179 [cs.SE]
     Dolan-Gavitt. 2021. Can OpenAI Codex and Other Large Language Models               [66] Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. 2023. Automated Pro-
     Help Us Fix Security Bugs? CoRR abs/2112.02125 (2021). arXiv:2112.02125                 gram Repair in the Era of Large Pre-trained Language Models. In 45th IEEE/ACM
     https://arxiv.org/abs/2112.02125                                                        International Conference on Software Engineering, ICSE 2023, Melbourne,
[44] Hammond Pearce, Benjamin Tan, Baleegh Ahmad, Ramesh Karri, and Brendan                  Australia, May 14-20, 2023. IEEE, 1482–1494. https://doi.org/10.1109/ICSE48619.
     Dolan-Gavitt. 2023. Examining Zero-Shot Vulnerability Repair with Large Lan-            2023.00129
     guage Models. In 44th IEEE Symposium on Security and Privacy, SP 2023, San
                                                                                                  Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, and Aseem Rastogi


[67] Jifeng Xuan, Matias Martinez, Favio Demarco, Maxime Clement, Sebastian              Conference on Software Engineering, ICSE 2022, Pittsburgh, PA, USA, May
     R. Lamelas Marcote, Thomas Durieux, Daniel Le Berre, and Martin Monper-             25-27, 2022. ACM, 1506–1518. https://doi.org/10.1145/3510003.3510222
     rus. 2017. Nopol: Automatic Repair of Conditional Statement Bugs in Java       [70] Yuan Yuan and Wolfgang Banzhaf. 2020. ARJA: Automated Repair of Java
     Programs. IEEE Trans. Software Eng. 43, 1 (2017), 34–55. https://doi.org/10.        Programs via Multi-Objective Genetic Programming. IEEE Trans. Software Eng.
     1109/TSE.2016.2560811                                                               46, 10 (2020), 1040–1067. https://doi.org/10.1109/TSE.2018.2874648
[68] Deheng Yang, Xiaoguang Mao, Liqian Chen, Xuezheng Xu, Yan Lei, David Lo,       [71] Qihao Zhu, Zeyu Sun, Yuan-an Xiao, Wenjie Zhang, Kang Yuan, Yingfei Xiong,
     and Jiayu He. 2023. TransplantFix: Graph Differencing-Based Code Transplan-         and Lu Zhang. 2021. A syntax-guided edit decoder for neural program repair.
     tation for Automated Program Repair. In Proceedings of the 37th IEEE/ACM            In ESEC/FSE ’21: 29th ACM Joint European Software Engineering Conference
     International Conference on Automated Software Engineering (Rochester, MI,          and Symposium on the Foundations of Software Engineering, Athens, Greece,
     USA) (ASE ’22). Association for Computing Machinery, New York, NY, USA,             August 23-28, 2021, Diomidis Spinellis, Georgios Gousios, Marsha Chechik, and
     Article 107, 13 pages. https://doi.org/10.1145/3551349.3556893                      Massimiliano Di Penta (Eds.). ACM, 341–353. https://doi.org/10.1145/3468264.
[69] He Ye, Matias Martinez, and Martin Monperrus. 2022. Neural Program Repair           3468544
     with Execution-based Backpropagation. In 44th IEEE/ACM 44th International
