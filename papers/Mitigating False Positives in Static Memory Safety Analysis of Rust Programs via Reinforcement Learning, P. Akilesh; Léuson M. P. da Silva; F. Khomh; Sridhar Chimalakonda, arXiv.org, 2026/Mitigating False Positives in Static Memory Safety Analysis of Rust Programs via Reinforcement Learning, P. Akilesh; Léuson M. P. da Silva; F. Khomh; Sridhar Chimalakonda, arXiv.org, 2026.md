                                            Mitigating False Positives in Static Memory Safety Analysis of
                                                     Rust Programs via Reinforcement Learning
                                                         P Akilesh                                Leuson Da Silva                           Foutse Khomh                    Sridhar Chimalakonda
                                                   Indian Institute of                         Polytechnique Montreal                    Polytechnique Montreal                  Indian Institute of
                                                      Technology                                  Montreal, Canada                          Montreal, Canada                        Technology
                                                     Tirupati, India                           leuson-mario-pedro.da-                   foutse.khomh@polymtl.ca                    Tirupati, India
                                                  cs22b040@iittp.ac.in                            silva@polymtl.ca                                                                 ch@iittp.ac.in

                                        Abstract                                                                                        Keywords
                                        Static analysis tools are essential for ensuring memory safety in                               Reinforcement Learning, Static Analysis, Memory Safety, Rust,
arXiv:2605.04000v2 [cs.SE] 6 May 2026




                                        Rust programs, particularly as Rust gains adoption in safety-critical                           False Positive
                                        domains. However, existing tools such as Rudra and MirChecker
                                                                                                                                        ACM Reference Format:
                                        suffer from high false positive rates, which diminish developer trust,                          P Akilesh, Leuson Da Silva, Foutse Khomh, and Sridhar Chimalakonda. 2026.
                                        increase manual review effort, and may obscure genuine vulnerabil-                              Mitigating False Positives in Static Memory Safety Analysis of Rust Pro-
                                        ities. This paper presents a novel reinforcement learning (RL)-based                            grams via Reinforcement Learning. In Proceedings of The 30th International
                                        approach for automatically classifying and suppressing spurious                                 Conference on Evaluation and Assessment in Software Engineering (EASE
                                        warnings in static memory safety analysis for Rust. To achieve this,                            2026). ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/nnnnnnn.
                                        we design an RL agent that learns a warning suppression policy by                               nnnnnnn
                                        extracting contextual features from Rust’s Mid-level Intermediate
                                        Representation (MIR) and optimizing its decisions through interac-                              1    Introduction
                                        tion with static analysis outputs. To improve decision quality, we                              The demand for memory-safe systems programming has catalyzed
                                        integrate dynamic validation via cargo-fuzz as an auxiliary feedback                            the rapid adoption of Rust across critical domains, including operat-
                                        mechanism, allowing the agent to selectively validate suspicious                                ing systems, cloud infrastructure, embedded systems, and security-
                                        warnings through targeted fuzz testing. Our evaluation shows that                               sensitive applications [51]. Major technology organizations have
                                        the proposed approach significantly outperforms state-of-the-art                                embraced Rust for its unique combination of performance and
                                        LLM-based baselines, achieving 65.2% accuracy and an F1 score of                                safety: the Linux kernel officially integrated Rust support in version
                                        0.659, an improvement of 17.1% over the best LLM baseline. With                                 6.1 [54], Microsoft has adopted Rust for Windows components [11],
                                        a recall of 74.6%, our method successfully identifies nearly three-                             and companies like AWS, Cloudflare, and Discord report signifi-
                                        quarters of true bugs while substantially reducing false positives,                             cant reliability improvements after migrating performance-critical
                                        improving precision from 25.6% in raw Rudra output to 59.0%. In-                                services from C/C++ to Rust [15, 50]. Such widespread adoption
                                        corporating dynamic fuzzing further boosts performance, yielding                                stems from Rust’s ownership model and type system, which provide
                                        additional improvements of 10.7 percentage points in accuracy and                               compile-time guarantees that eliminate entire classes of memory
                                        8.6 percentage points in F1 score over the RL-only variant. Over-                               safety vulnerabilities, including use-after-free, double-free, and data
                                        all, our work demonstrates that combining reinforcement learning                                races, without requiring garbage collection [26, 36].
                                        with hybrid static–dynamic analysis can substantially reduce false                                 Despite these powerful safety guarantees, the reality of systems
                                        positives and improve the practical usability of memory safety                                  programming necessitates escape hatches. Rust’s unsafe keyword
                                        verification tools for Rust.                                                                    permits operations that the compiler cannot statically verify. Em-
                                                                                                                                        pirical studies reveal that unsafe code is pervasive throughout the
                                        CCS Concepts                                                                                    Rust ecosystem, with 25–30% of packages on crates.io containing at
                                        • Software and its engineering → Software verification; Auto-                                   least one unsafe block [4, 19]. Even the Rust standard library relies
                                        mated static analysis; • Theory of computation → Reinforce-                                     on unsafe code for core abstractions like Vec and Mutex, as it is
                                        ment learning.                                                                                  essential for FFI, performance-critical optimizations, and low-level
                                                                                                                                        implementations that cannot be expressed in safe Rust [41].
                                                                                                                                           To address the verification challenges introduced by unsafe code,
                                                                                                                                        previous studies have developed static analysis tools based on Rust’s
                                                                                                                                        Mid-level Intermediate Representation (MIR) to detect memory
                                        Permission to make digital or hard copies of all or part of this work for personal or
                                        classroom use is granted without fee provided that copies are not made or distributed           safety violations at scale. Representative MIR-based tools include
                                        for profit or commercial advantage and that copies bear this notice and the full citation       Rudra [7], MirChecker [32], and Yuga [21]. Despite this success,
                                        on the first page. Copyrights for components of this work owned by others than the              false positives remain the dominant barrier to practical adoption,
                                        author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
                                        republish, to post on servers or to redistribute to lists, requires prior specific permission   as current SOTA tools exhibit severe imprecision. Prior studies
                                        and/or a fee. Request permissions from permissions@acm.org.                                     report that MirChecker produces false positives in 95.1% of its
                                        EASE 2026, Glasgow, Scotland, United Kingdom                                                    warnings, while Rudra and Yuga exhibit substantially lower false-
                                        © 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                        ACM ISBN 978-x-xxxx-xxxx-x/YYYY/MM                                                              positive rates of 50% and 46.15%, respectively [7, 21, 32]. Such rates
                                        https://doi.org/10.1145/nnnnnnn.nnnnnnn                                                         impose substantial manual review effort and lead to warning fatigue,
EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom                                                                            Akilesh et al.


where developers increasingly distrust or ignore analysis results [14,        output (from 25.6% to 59.0%). Selective dynamic fuzzing provides
25]. Meanwhile, empirical studies show that false positive rates              additional gains, improving accuracy by 10.7 percentage points and
above 20–30% frequently result in tool abandonment in industrial              F1 score by 8.6 percentage points over the RL-only variant.
settings [8, 48].                                                                Overall, the primary contributions of this work are as follows:
    To overcome these weaknesses, different approaches have been                  (1) A reinforcement learning–based framework for reducing
explored. For example, traditional approaches have relied on man-                     false positives in Rust static memory safety analysis [1].
ual tuning of analysis heuristics, pattern-based filtering rules de-              (2) A hybrid static–dynamic formulation that incorporates cargo-
rived from observed false positive patterns, or developer-provided                    fuzz as a selective RL action.
annotations to guide analysis [6, 30]. While effective in limited con-            (3) A curated dataset of 4,879 manually labeled static analysis
texts, these techniques require significant domain expertise, lack                    warnings collected from approximately 20,000 Rust crates.
adaptability to evolving codebases, and fail to generalize across                 (4) A large-scale empirical evaluation showing that our approach
different projects or programming idioms. More recent efforts have                    outperforms state-of-the-art LLM-based baselines while re-
explored machine learning techniques for warning prioritization                       maining practical for real-world use.
and classification [23, 28, 46]. These approaches typically depend                (5) A modernized implementation of Rudra compatible with the
on hand-crafted features, supervised learning with limited labeled                    current Rust ecosystem [2].
training data, or models that cannot adapt post-deployment as code
patterns evolve.                                                              2     Background
    To address these challenges, we introduce a reinforcement learn-
                                                                              This section provides foundational concepts for understanding our
ing–based approach that automatically learns policies for classify-
                                                                              reinforcement learning-based approach. First, we discuss Rust’s
ing and suppressing false positive warnings in Rust static analy-
                                                                              memory safety model, followed by static analysis for Rust, and the
sis. Unlike supervised learning methods that rely on large labeled
                                                                              adoption of fuzzing.
datasets and remain fixed after training, reinforcement learning
provides a general framework for optimizing sequential decision
                                                                              2.1    Rust’s Memory Safety Model
policies through interaction with an environment and reward feed-
back [53]. In our setting, this enables an agent to learn suppression         Rust is a systems programming language that provides memory
strategies that trade off false-positive reduction against preserving         safety without garbage collection through a sophisticated type
true vulnerability detection.                                                 system and ownership model [36]. Unlike C/C++, Rust enforces
    Our approach leverages rich semantic features extracted directly          safety at compile time, eliminating entire classes of memory errors.
from Rust’s MIR, enabling precise reasoning about control flow, type          Rust’s safety guarantees rest on three fundamental principles:
and lifetime constraints, and unsafe operations, capabilities that               Ownership. Every value in Rust has a single owner that stat-
are difficult to achieve at the source level, particularly in the pres-       ically determines its lifetime. When the owner goes out of scope,
ence of generics and macro expansion. We instantiate our approach             the value is automatically deallocated through RAII-style drop se-
on top of Rudra, a MIR-based analyzer, whose scope and warning                mantics [26]. This prevents use-after-free and double-free errors in
diversity make it well-suited for learning-based suppression [7].             safe Rust code (see Listing 1):
To further improve decision confidence, the agent selectively in-         1 fn ownership_example () {
tegrates dynamic validation via cargo-fuzz when static evidence           2     let s1 = String :: from ( " hello " ) ;
is insufficient, gathering concrete runtime feedback to resolve am-       3     let s2 = s1 ; // s1 moved to s2
biguous warnings [9, 29]. This hybrid static–dynamic formulation          4     // println !("{}" , s1 ) ; // Error : s1 no longer
enables cost-aware suppression policies that strategically allocate                 valid
expensive fuzzing resources, bridging the gap between conservative        5     println !( " {} " , s2 ) ; // OK
                                                                          6 } // s2 dropped here
static analysis and concrete program behavior while preserving
scalability.                                                                      Listing 1: Ownership example showing move semantics
    We evaluate our approach through a large-scale empirical study.
We first modernized the Rudra static analyzer to support the current              Borrowing. Values can be temporarily borrowed through refer-
Rust ecosystem and applied it to approximately 20,000 crates from             ences without transferring ownership. The borrow checker ensures
crates.io, producing a curated dataset of 4,879 warnings spanning di-         that references do not outlive the data they point to [36] (see Listing
verse unsafe usage patterns. Ground truth labels are established via          2):
systematic manual classification by domain experts in Rust mem-
                                                                          1 fn borrowing_example () {
ory safety. We then benchmark our RL-based approach against               2     let s = String :: from ( " hello " ) ;
state-of-the-art large language models, including CodeLlama 34B,          3     let len = calculate_length (& s ) ; // Borrowed
Llama3 (8B and 70B), Mixtral 8×7B, ChatGPT-4o mini, and Claude            4     println !( " {} has length {} " , s , len ) ;
Opus 4.1, representing current LLM capabilities for code analy-           5 }
sis [13, 22, 24, 42]. Our results show that the RL agent with fuzzing     6 fn calculate_length ( s : & String ) -> usize {

integration achieves 65.2% accuracy and a 0.659 F1 score, outper-         7     s . len ()
forming the best LLM baseline by 17.1 percentage points. With a           8 } // s goes out of scope ( only borrowed )

recall of 74.6%, our approach identifies nearly three-quarters of true
                                                                                   Listing 2: Borrowing example with reference passing
bugs while more than doubling precision compared to Rudra’s raw
    Mitigating False Positives in Static Memory Safety Analysis of Rust Programs via Reinforcement Learning   EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom


       Aliasing XOR Mutability. At any time, a value may have either                           leading to conservative over-approximation and false positives. The
    multiple shared references or one mutable reference, but never                             Send/Sync Variance (SV) checker analyzes thread-safety proper-
    both [26]. This prevents data races and iterator invalidation (see                         ties of generic types by inferring required trait bounds from public
    Listing 3):                                                                                APIs and comparing them against concrete implementations.
                                                                                                  Rudra targets three critical classes of bugs that arise from in-
1 fn aliasing_xor_mutability () {
2     let mut data = vec ![1 , 2 , 3];                                                         correct use of unsafe code in Rust [7, 57]. First, when Rust panics,
3     let r1 = & data ; // Shared reference                                                    stack unwinding executes destructors as control propagates up-
4     let r2 = & data ; // OK : multiple shared refs                                           ward, leading to Panic Safety issues. If unsafe code temporarily
5     // let r3 = & mut data ; // Error : cannot borrow                                        violates internal invariants (e.g., mutating vector length during
             as mutable                                                                        reorganization), a panic triggered by a caller-provided closure can
6     drop ( r1 ) ; drop ( r2 ) ; // End shared borrows                                        cause use-after-free or double-free. A representative example is
7     let r3 = & mut data ; // OK : can mutably borrow                                         CVE-2020-36317 in String::retain(), where panicking closures
8     r3 . push (4) ;                                                                          left strings in an invalid UTF-8 state [38].
9 }
                                                                                           1 fn unsafe_retain ( v : & mut Vec < u8 >) {
           Listing 3: Aliasing XOR mutability enforcement                                  2     let len = v . len () ;
                                                                                           3     unsafe { v . set_len (0) ; } // invariant broken
       Despite Rust’s strong safety guarantees, certain operations essen-                  4     // if closure panics here , destructor runs
    tial to systems programming cannot be verified by the compiler [4].                    5     // on invalid state -> use - after - free
    To support these cases, Rust provides the unsafe keyword, which                        6     v . retain (| x | * x > 0) ;
    permits five specific capabilities: dereferencing raw pointers, calling                7     unsafe { v . set_len ( len ) ; }
    unsafe functions, accessing mutable static variables, implementing                     8 }

    unsafe traits, and accessing union fields.
                                                                                               Listing 5: Panic safety violation: unsafe invariant broken
                                                                                               before panic.
    2.2     Static Analysis for Rust
    Static analysis tools leverage Rust’s intermediate representations                            As shown in Listing 5, Rudra’s UD checker flags the set_len
    (IRs) to detect memory safety violations at scale. In this work, we fo-                    call as a lifetime-bypassing operation whose invariant may not be
    cus on Rudra [7], which analyzed over 43,000 packages, discovering                         restored if a panic occurs before the matching restore.
    264 previously unknown bugs, but suffers from high false-positive                             Second, Higher-Order Invariants are related to unsafe code
    rates, highlighting the need for automated reduction. Rudra per-                           that often relies on semantic assumptions about generic functions
    forms ecosystem-scale analysis to detect memory safety bugs in                             that are not captured by type signatures, such as purity or con-
    unsafe Rust code. Implemented as a custom compiler driver, Rudra                           sistency of results [41]. Violations of these assumptions can lead
    intercepts compilation after type checking to inject analysis algo-                        to memory corruption. For example, CVE-2020-36323 in join()
    rithms. Its key innovation is hybrid IR analysis, which combines                           assumed that Borrow implementations return consistent results;
    High-Level IR (HIR), preserving source-level structure, with Mid-                          impure implementations violated this invariant, causing buffer
    Level IR (MIR), which exposes explicit control flow. This design                           overflows [17]. Finally, generic types must correctly propagate
    enables generic-aware analysis that is difficult to achieve at the                         thread-safety requirements through appropriate Send and Sync
    LLVM IR level.                                                                             bounds. Missing or incorrect bounds can allow data races through
                                                                                               safe code. This Send/Sync Variance issue can be observed in
1 // Source / HIR - level ( preserves structure ) :                                            CVE-2020-35905 in the futures-rs crate, which occurred because
  let s1 = String :: from ( " hello " ) ;
                                                                                               MappedMutexGuard failed to enforce bounds on mapped types, en-
2

3 let s2 = s1 ; // ownership moved
4
                                                                                               abling data races involving Rc (a single-threaded reference-counted
5 //      MIR - level ( explicit move + invalidation ) :                                       smart pointer that is not thread-safe) [16].
6 _1      = String :: from ( const " hello " ) ; // s1
7 _2      = move _1 ;                            // s2                                         2.3    Fuzzing and Dynamic Analysis
8 //      _1 is now invalid ( move tracked explicitly )                                        Fuzzing automatically generates test inputs to discover bugs through
                                                                                               concrete execution [29]. Modern coverage-guided fuzzers, such as
    Listing 4: HIR vs. MIR representation of a simple ownership
                                                                                               AFL and libFuzzer, leverage execution feedback to efficiently ex-
    transfer.
                                                                                               plore program paths [58]. When combined with sanitizers, like
        As shown in Listing 4, MIR makes ownership transfers explicit                          AddressSanitizer, MemorySanitizer, and ThreadSanitizer, fuzzing
    as move operations, allowing Rudra to precisely track lifetime-                            enables high-confidence detection of memory safety and concur-
    bypassing flows that are implicit at the HIR level.                                        rency errors. Cargo-fuzz integrates libFuzzer into the Rust ecosys-
        Rudra implements two primary algorithms. The Unsafe Dataflow                           tem [43]. While effective for bugs with well-defined input surfaces,
    (UD) checker performs taint-style tracking to identify flows from                          fuzzing faces challenges in exercising subtle semantic violations,
    lifetime-bypassing operations (e.g., uninitialized memory and dupli-                       such as Send/Sync errors that require specific thread interleaving
    cated values) to potentially dangerous operations. It approximates                         or execution contexts. Moreover, due to its computational cost, in-
    dangerous points using unresolvable generic functions, functions                           discriminate adoption of fuzzing across all potential warnings is
    whose implementation depends on caller-supplied type parameters,                           impractical at scale [29].
EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom                                                                             Akilesh et al.


   Static and dynamic analysis exhibit complementary trade-offs:
static analysis offers broad coverage and generic reasoning, but
often produces false positives, whereas dynamic analysis only
explores executed paths but provides concrete evidence of real
bugs [31]. Hybrid approaches combining both techniques have
been shown to achieve superior results [9]. Our RL framework
operationalizes this paradigm by learning when to apply static or
dynamic validation based on their relative effectiveness for different
classes of warnings.


3     Methodology and Approach                                                 Figure 1: Overview of the warning classification pipeline.
This section describes our reinforcement learning-based approach               Rust warnings are processed through feature collection and
for addressing the occurrence of false positives in Rudra’s static             confidence assessment. High-confidence warnings are di-
memory safety analysis. First, we begin by outlining the dataset               rectly classified as true positives or false positives. Low-
construction process, followed by our feature extraction strategy,             confidence warnings trigger automated harness generation,
the RL formulation, and the integration of cargo-fuzz as a dynamic             compilation and configuration, and fuzzing. The outcomes
validation mechanism.                                                          of fuzzing are aggregated in the final processing and used to
                                                                               make the final classification decision.

3.1     Dataset Construction and Labeling
Our work begins with creating a large-scale dataset of Rudra warn-
ings from real-world Rust code. To enable this, we first updated               paths reported by Rudra, and determined whether the warning
the Rudra static analyzer to be compatible with contemporary Rust              corresponded to a genuine soundness violation or a false alarm.
compiler versions. The original implementation of Rudra was devel-
oped for the Rust nightly-2021-10-21 compiler [45] and depends on          1   {
                                                                           2        " level " : " Warning " ,
MIR representations and compiler APIs that have since evolved. As
                                                                           3        " analyzer " : " UnsafeDestructor " ,
a result, it is incompatible with the current Rust toolchain. Our up-      4        " op_type " : null ,
dated implementation targets the Rust nightly-2025-06-26 compiler          5        " description " : " unsafe block detected in drop " ,
[44] and incorporates adaptations to modern MIR representations            6        " file " : " aarc -0.3.2/ src / smart_ptrs . rs " ,
and changes to Rust’s type system introduced in later compiler             7        " start_line " : 118 , " start_col " : 1 ,
releases. Our implementation is available online [2]. To ensure            8        " end_line " : 118 , " end_col " : 33 ,
correctness, we validated our implementation against Rudra’s of-           9        " code_snippet " : " impl < T : ' static > Drop for Arc
ficial regression test suite, which covers Unsafe Dataflow, Panic                        <T > {...} } "
Safety, and Send/Sync Variance analyses with both positive and            10   }
negative cases. We ran the test suite under the Rust nightly-2025-06-
26 compiler, and all tests successfully passed (23/23 standard cases,          Listing 6: Rudra JSON report for an unsafe destructor in aarc.
1/1 false-negative, and 3/3 false-positive cases), showing that our
implementation correctly reproduces the behavior of the original                  To assess labeling reliability, a second reviewer independently
analyzer.                                                                      classified a random subsample of 150 warnings, yielding 82.7% raw
   Using the updated analyzer, we ran Rudra on approximately                   agreement (Cohen’s 𝜅 = 0.63), indicating substantial inter-rater
20,000 crates from crates.io that contained at least one unsafe block,         agreement. The labeling process focused on the underlying bug
ensuring relevance to our analysis target. This analysis produced              pattern rather than exploitability, as our goal is to improve the
4,879 unique warnings generated by Rudra’s Unsafe Dataflow and                 precision of static analysis rather than assess security impact. For
Send/Sync Variance checkers. Each warning is associated with its               example, in Listing 6, Rudra’s UnsafeDestructor analyzer reports
source code location, the detected bug pattern (panic safety, higher-          a dereference inside a Drop implementation. These operations in
order invariant, or Send/Sync variance), the precision level reported          destructors are known to be error-prone, as invalid pointer derefer-
by Rudra, and contextual information describing the surrounding                ences or concurrency violations at this stage may lead to undefined
code structure. To illustrate the collected warnings, Listing 6 shows          behavior. Finally, Rudra correctly classifies this instance as a poten-
the raw JSON output produced by Rudra for a warning in the aarc                tial higher-order invariant violation (true positive).
crate (v0.3.2) [3]. The report includes the warning level, the respon-            Overall, this process identified 1,247 true positives (25.6%) and
sible analyzer, a textual description, the precise source location, and        3,632 false positives (74.4%), available in our online appendix [1],
the extracted code snippet.                                                    highlighting the substantial false positive burden that motivates
   For each collected warning, one reviewer, with experience in                this work. We partitioned the dataset into training (70%), validation
Rust memory safety semantics, manually classified all 4,879 warn-              (15%), and test (15%) sets using stratified sampling to preserve class
ings through careful code review. For each warning, the reviewer               distribution, yielding 732 warnings in the held-out test set used for
examined the surrounding code context, inspected the data-flow                 final evaluation.
Mitigating False Positives in Static Memory Safety Analysis of Rust Programs via Reinforcement Learning   EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom


3.2     Feature Extraction from MIR                                                         We parameterize the policy using a neural network with two
Effective classification requires features that capture characteristics                  hidden layers of 256 and 128 units, respectively, employing ReLU
distinguishing true bugs (true positives) from false alarms (false                       activations and dropout regularization to mitigate overfitting. Train-
positives). To this end, we extract features at multiple levels of                       ing is performed using Proximal Policy Optimization (PPO), a policy
abstraction, leveraging Rust’s Mid-level Intermediate Representa-                        gradient algorithm that offers stable training dynamics for discrete
tion (MIR) to access rich semantic information while preserving                          action spaces and has proven effective in similar code analysis tasks
awareness of generic types.                                                              [49] The agent is trained in an offline setting using the labeled
   Our feature extraction process is organized into three primary                        dataset, with optimization proceeding over multiple epochs until
categories. First, we extract MIR-level semantic features that charac-                   validation performance converges.
terize program behavior surrounding each warning. These include
type system properties (e.g., number of generic parameters, pres-                        3.4     Cargo-Fuzz Integration
ence of trait bounds, and generic nesting depth); ownership and                          We integrate cargo-fuzz as a selective dynamic validation action
borrowing patterns (e.g., borrow ratios, nesting depth, and use of                       available to the RL agent, rather than applying fuzzing uniformly
smart pointers); control-flow characteristics derived from the MIR                       to all warnings. The agent invokes fuzzing only for low-confidence
control-flow graph (e.g., cyclomatic complexity, loop nesting depth,                     cases based on confidence estimates derived from static features.
and number of panic paths); and unsafe operation context, such as                        Confidence is assessed using two complementary signals: (i) the
the lifetime bypass category and the distance between the bypass                         gap between the top two action Q-values, where smaller gaps indi-
and the potentially dangerous operation.                                                 cate uncertainty, and (ii) the entropy of the policy network’s action
   Second, we extract structural code features from the surrounding                      distribution, where higher entropy reflects lower confidence. Warn-
package and module context. These capture package-level signals                          ings whose confidence falls below a threshold trigger the fuzzing
such as download counts from crates.io (used as a proxy for code                         action. Rather than being a fixed hyperparameter, this threshold
maturity and scrutiny), the prevalence of unsafe code within the                         emerges implicitly from the learned policy as the agent optimizes
package, and whether the warning occurs in a public API surface.                         the trade-off between classification accuracy and fuzzing cost.
We also include standard structural metrics, including lines of code,                       Figure 1 illustrates the fuzzing integration pipeline. Upon se-
parameter counts, and comment density. Third, we incorporate                             lecting the fuzzing action, the system automatically generates a
analysis-specific features derived directly from Rudra. These in-                        targeted harness using templates corresponding to the detected bug
clude the checker that generated the warning, Rudra’s assigned pre-                      pattern (e.g., panic safety, higher-order invariants, or Send/Sync
cision level, and clustering information indicating whether multiple                     variance), instantiated with function signatures and type infor-
warnings occur at nearby code locations. After removing highly cor-                      mation from the warning context. Fuzzing outcomes—including
related features and applying domain knowledge to avoid spurious                         crashes, sanitizer violations, or clean executions—are encoded into
correlations, the final feature set comprises ~87 features.                              the agent’s state representation and used to inform the final classifi-
                                                                                         cation decision. Through training, the agent learns when fuzzing is
3.3     Reinforcement Learning Formulation                                               most beneficial, enabling selective dynamic validation that improves
                                                                                         classification accuracy while controlling computational overhead.
We formulate the false positive classification problem as a Markov
Decision Process (MDP) in which an agent learns to classify static
analysis warnings using feedback derived from labeled data. The                          3.5     Baseline Comparisons
state space consists of the feature vectors described above, nor-                        To evaluate our approach, we established baselines using state-of-
malized to facilitate neural network training. Each state represents                     the-art large language models (LLMs), including (i) code-specialized
the complete observable context required to make a classification                        models (CodeLlama), (ii) general-purpose large language models
decision for a single warning.                                                           (GPT-4o Mini and Claude Opus), and (iii) mixture-of-experts archi-
   The action space comprises three discrete actions: classifying                        tectures (Mixtral). We also considered models with varying param-
a warning as a true positive, classifying it as a false positive, or                     eter scales (from 8B to 70B+) to assess the impact of model capacity
invoking dynamic fuzzing to gather additional evidence prior to                          on this task. Finally, all selected models are widely used in code
making a final classification. This design allows the agent to selec-                    analysis [33, 37]. All models were evaluated using their default
tively request costly dynamic validation when static features alone                      decoding parameters, as no explicit configuration of temperature,
do not provide sufficient confidence.                                                    top-p, or other sampling parameters was applied. In addition, all
   The reward function balances classification accuracy against                          models were evaluated on the same binary classification task of dis-
computational efficiency. Correct classifications receive positive                       tinguishing true positives from false positives. For each model, we
rewards (+15), while incorrect classifications are penalized (-15),                      constructed prompts containing the warning message, surrounding
reflecting the cost of misclassification in safety-critical analysis.                    code context, and a description of the associated bug pattern, and
Executing the fuzzing action incurs a cost penalty (-5) to discourage                    instructed the model to classify each warning as either a real issue
indiscriminate use. When fuzzing yields definitive evidence that                         or a false positive. To ensure consistency across models, outputs
enables a correct classification, the agent receives an additional                       were constrained to a fixed JSON schema encoding the classifica-
bonus reward (+10 for a found bug, confirming a true positive;                           tion decision. We experimented with multiple prompting strategies,
+8 for clean, confirming a false positive; +3 when helpful but not                       including zero-shot and few-shot configurations, and report results
definitive), encouraging effective use of dynamic validation.                            for the best-performing setup for each model.
EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom                                                                            Akilesh et al.


   These LLM-based baselines serve as a comparison point, repre-          Table 1: Classification Performance Comparison on Test Set
senting the capabilities of advanced language models applied to
static analysis warning classification, without access to structured       Approach            Acc. Prec. Rec.         F1     MCC ROC           PR
MIR-level features or a learned decision policy. The full prompt
                                                                           Raw Rudra Output     –     0.256   1.000   0.407      –       –       –
templates used in our experiments are provided in the appendix             RL+Fuzz            0.652   0.590   0.746   0.659   0.323    0.661   0.554
[1].                                                                       RL                 0.545   0.496   0.679   0.573    0.117   0.557   0.481
                                                                           Claude             0.533   0.486   0.669   0.563    0.094   0.546   0.474
3.6     Evaluation Metrics                                                 Llama70B           0.503   0.360   0.136   0.197   -0.082   0.469   0.437
                                                                           GPT-4o Mini        0.490   0.453   0.650   0.534    0.010   0.505   0.452
We evaluate our approach and all baselines using the ground-truth          CodeLlama          0.431   0.409   0.598   0.486   -0.112   0.446   0.425
labels of the dataset described in Section 3.1. Each warning is labeled    Mixtral            0.326   0.328   0.476   0.388   -0.336   0.339   0.392
as either a true or false positive (genuine or spurious warning,           Llama8B            0.487   0.437   0.487   0.460   -0.026   0.487   0.443
respectively), enabling a binary classification evaluation.
   To assess classification performance, considering class imbal-
ance, we report seven complementary metrics, including accuracy,
precision, recall, and F1 score, which together capture overall cor-
                                                                          of classification quality, providing a comprehensive comparison of
rectness and the precision–recall trade-off relevant to false positive
                                                                          their respective strengths and limitations (see Table 1).
reduction. To more robustly account for class imbalance, we addi-
                                                                             Our RL-based approach with fuzzing integration achieves the
tionally report the Matthews Correlation Coefficient (MCC), which
                                                                          highest performance across all seven evaluation metrics. With an ac-
summarizes classification quality across all four confusion matrix
                                                                          curacy of 65.2% and an F1 score of 0.659, our approach substantially
categories. Finally, we report the Receiver Operating Characteris-
                                                                          outperforms all baselines. The 17.1 percentage point improvement
tic curve (AUC-ROC) and the Precision–Recall curve (AUC-PR) to
                                                                          in F1 score over the best LLM baseline (Claude Opus 4.1 at 0.563)
assess discriminative capability across decision thresholds, with
                                                                          demonstrates the value of our specialized approach by combining
AUC-PR being particularly informative given the skewed class dis-
                                                                          structured feature extraction from MIR with learned classification
tribution.
                                                                          policies. This improvement is particularly notable given that we
                                                                          are working with a challenging, imbalanced dataset where 74.4% of
4     Results                                                             warnings are false positives. The high recall of 0.746 is especially
This section presents our comprehensive experimental results. To          important in our safety-critical context, as it indicates we success-
evaluate the performance of our RL-based approach compared to             fully identify 74.6% of true bugs while suppressing false alarms.
LLM baselines and evaluate the impact of fuzzing integration, we          This recall rate substantially exceeds most LLM baselines, with
define the following Research Questions (RQs):                            only our RL variant without fuzzing (0.679) and Claude Opus 4.1
                                                                          (0.669) achieving comparable recall. At the same time, our precision
      • RQ1: How effective is the RL-based approach at reducing           of 0.590 indicates that nearly 60% of reported warnings correspond
        false positives in Rust compared to existing baselines?           to genuine bugs, more than doubling the precision of the raw Rudra
      • RQ2: What is the impact of selectively integrating dynamic        output, whose precision equals the base rate of 25.6%.
        fuzzing into the RL-based approach?                                  Among the LLM baselines, Claude Opus 4.1 achieves the strongest
      • RQ3: What insights do the learned RL policy provide about         results (F1: 0.563), followed by ChatGPT-4o Mini (0.534). Llama3
        warning characteristics and decision strategies?                  70B performs poorly (F1: 0.197) due to extremely low recall (0.136),
   These research questions are designed to jointly assess the ef-        while CodeLlama 34B achieves only 0.486 F1 despite code-specific
fectiveness, added value, and interpretability of our RL approach.        pretraining. This indicates that pretraining alone is insufficient, as
RQ1 evaluates whether the proposed RL-based framework achieves            performance depends more on reasoning about complex semantic
meaningful reductions in false positives compared to strong LLM           properties than surface-level code familiarity.
baselines, addressing the core practical challenge of static analysis        Mixtral 8x7B shows the weakest performance with a 0.388 F1
adoption. RQ2 isolates the contribution of selective dynamic fuzzing,     score and 0.326 accuracy, barely exceeding random guessing for
allowing us to quantify the benefits of hybrid static–dynamic rea-        this imbalanced dataset. The negative MCC of -0.336 indicates pre-
soning beyond static features alone. Finally, RQ3 examines the            dictions worse than random, suggesting the mixture-of-experts ar-
learned decision policies to provide insight into which warning           chitecture may not be well-suited to this task without task-specific
characteristics drive classification outcomes and how the agent allo-     fine-tuning. Comparing the two Llama3 variants provides insight
cates dynamic validation resources. Together, these questions offer       into how model scale affects performance on this task. Surprisingly,
a holistic evaluation of performance, mechanism, and behavior.            Llama3 8B achieves a 0.460 F1 score, substantially outperforming
                                                                          the larger Llama3 70B at a 0.197 F1 score. This counterintuitive
                                                                          result suggests that larger models may be more prone to overthink-
4.1     RQ1: Overall Effectiveness of the RL-Based                        ing the task or being misled by the class imbalance, potentially
        Approach                                                          learning to predict the majority class too aggressively. In contrast,
Table 1 reports the classification performance of all approaches on a     the smaller model’s more balanced predictions (0.487 recall) re-
held-out test set comprising 732 warnings. We evaluate each method        sult in better overall performance despite presumably having less
using seven complementary metrics that capture different aspects          reasoning capacity.
Mitigating False Positives in Static Memory Safety Analysis of Rust Programs via Reinforcement Learning      EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom


                  0.8


                  0.6
   Metric Value




                  0.4


                  0.2


                   0
                               z




                                           RL




                                                                                               4o
                                                             e




                                                                             0B




                                                                                                                  a




                                                                                                                                    l




                                                                                                                                                  B
                                                                                                                                 tra
                              uz




                                                           ud




                                                                                                                am




                                                                                                                                                 a8
                                                                                              T
                                                                           a7
                          +F




                                                                                                                               ix
                                                            a




                                                                                                                                               am
                                                                                           GP




                                                                                                                Ll
                                                         Cl




                                                                         am




                                                                                                                             M
                         RL




                                                                                                              de




                                                                                                                                             Ll
                                                                        Ll




                                                                                                           Co
                                                                  Accuracy        Precision       Recall     F1 Score


Figure 2: Comparison of key performance metrics across all approaches. Our RL+Fuzzing approach achieves the highest
Accuracy, Precision, Recall, and F1 Score, demonstrating superior classification performance compared to RL alone and various
LLM-based models.


   Our RL + Fuzzing approach achieves MCC of 0.323, the only                             beyond static features alone. The MCC improvement of 0.206 is
method above 0.3, indicating moderate positive correlation between                       particularly significant, as it indicates that fuzzing helps the model
predictions and ground truth. In contrast, Claude Opus 4.1 achieves                      make genuinely better predictions rather than simply shifting the
only 0.094, while several baselines show negative MCC values. This                       bias toward one class.
substantial gap validates that our approach provides genuine dis-                           The fuzzing integration improves performance through two com-
criminative power beyond simply predicting the majority class. The                       plementary mechanisms. First, when fuzzing successfully triggers
AUC-ROC metric of 0.661 for our approach indicates reasonable                            a bug (finding a sanitizer violation), it provides near-definitive
discriminative ability across different classification thresholds, sub-                  evidence that the warning represents a true positive. This high-
stantially exceeding the 0.5 baseline for random classification. The                     confidence signal allows the agent to correctly classify warnings
AUC-PR metric of 0.554 is particularly important for imbalanced                          that would be ambiguous based on static features alone. Second,
datasets, as it focuses on performance on the minority (positive)                        when fuzzing executes cleanly without detecting issues, this pro-
class. Our approach achieves the highest AUC-PR among all meth-                          vides evidence (though not proof) against the warning, helping filter
ods, confirming strong performance at identifying true positives                         false positives. Through training, the agent learns to appropriately
even in the presence of substantial class imbalance.                                     weigh these different forms of dynamic evidence.
                                                                                            The relatively larger improvement in precision (+9.4 percentage
                                                                                         points) compared to recall (+6.7 percentage points) indicates that
          RQ1 Findings: Our reinforcement learning–based ap-                             fuzzing is particularly effective at increasing confidence in positive
          proach substantially outperforms both raw static analysis                      classifications rather than uncovering previously missed bugs. This
          output and state-of-the-art LLM baselines in false positive                    behavior aligns with the inherent strengths of fuzzing: it excels at
          reduction. The proposed method achieves 65.2% accuracy                         providing concrete evidence of failures but cannot establish the
          and 0.659 F1 score, improving F1 by 17.1 percentage                            absence of bugs. The substantial observed precision gains indicate
          points over the strongest LLM baseline (Claude Opus 4.1).                      that fuzzing helps filter spurious static warnings by corroborating
          Most importantly, the approach more than doubles pre-                          which reported issues manifest under concrete execution.
          cision, increasing it from 25.6% (raw Rudra output) to                            A central question is whether the RL agent learns to invoke
          59.0%, while maintaining a high recall of 74.6%.                               fuzzing selectively or applies it uniformly across warnings. Our
                                                                                         observations during training indicate that the agent converges to
                                                                                         a targeted fuzzing strategy. Early in training, fuzzing is invoked
4.2               RQ2: Impact of Selective Dynamic Fuzzing                               broadly as part of exploration. As training progresses, fuzzing us-
In this RQ, we aim to investigate and better understand the impact                       age becomes increasingly selective, concentrating on warnings for
observed by using fuzzing as a dynamic resource for our RL agent.                        which static features indicate higher uncertainty. This behavior
Comparing our full RL + Fuzzing approach against the RL-only                             suggests that the learned policy effectively balances the compu-
variant provides clear evidence for the value of integrating dynamic                     tational cost of fuzzing against its expected informational benefit,
validation. The performance improvements are substantial across                          consistent with the reward design.
all metrics (see Table 1, 2nd and 3rd rows). These improvements                             Further analysis reveals that fuzzing is preferentially applied to
represent relative gains of 19.6% in accuracy and 15.0% in F1 score,                     specific classes of warnings. In particular, warnings involving com-
demonstrating that fuzzing integration provides substantial value                        plex generic code or higher-order functions, where static analysis
EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom                                                                       Akilesh et al.


is inherently limited, are more likely to trigger fuzzing invocations.   are only present for the subset of warnings on which dynamic vali-
In contrast, warnings with clear static signatures, such as obvious      dation is invoked, and their influence is therefore highly localized.
Send/Sync violations with simple types, are typically classified di-     In those cases, however, their contribution is strong and often deci-
rectly without dynamic validation. These observations indicate that      sive. This explains why fuzzing features exhibit moderate global
the agent learns to allocate fuzzing resources to cases where dy-        SHAP values despite the integration of fuzzing yielding an over-
namic evidence is most likely to improve classification confidence.      all improvement of 8.6 percentage points in F1 score. Rather than
                                                                         driving decisions uniformly, fuzzing acts as a targeted source of
                                                                         high-confidence evidence when static analysis alone is insufficient.
      RQ2 Findings: Dynamic fuzzing provides substantial ad-
      ditional benefits beyond static feature–based classification.
      Incorporating cargo-fuzz as a strategic RL action improves               RQ3 Findings: MIR-level semantic features are the
      accuracy by 10.7 percentage points and F1 score by                       strongest predictors of warning validity, particularly those
      8.6 percentage points compared to the RL-only vari-                      capturing generic type complexity, control-flow struc-
      ant. Importantly, the agent learns to invoke fuzzing se-                 ture, and unsafe operation context. SHAP-based fea-
      lectively, approximately 23% of warnings, making the                     ture importance shows that warnings arising in complex
      hybrid static–dynamic approach computationally feasible                  generic code and high–panic-path control flow are
      at scale while significantly improving classification confi-             more likely to correspond to true bugs. Finally, the agent
      dence.                                                                   also learns to strategically allocate fuzzing resources to
                                                                               warnings exhibiting high semantic uncertainty.

4.3     RQ3: Analysis of Learned Policies and
                                                                         5     Discussion
        Warning Characteristics
                                                                         This section explores the broader implications of our findings, dis-
To better understand the factors driving classification performance,
                                                                         cusses practical considerations for deployment, and reflects on the
we analyze the features that contribute most strongly to the RL
                                                                         limitations of our approach.
agent’s decisions. We employ SHAP (SHapley Additive exPlana-
tions) values to quantify the contribution of individual features to
                                                                         5.1     Practical Implications
the model’s predictions.[35]
   The most influential features span multiple categories. MIR-level     Our RL-based approach demonstrates practical potential for inte-
semantic features are the strongest contributors, particularly those     gration into real-world Rust development workflows. By improving
capturing type complexity (e.g., number of generic parameters and        precision from Rudra’s 25.6% to 59.0%, the approach can substan-
presence of trait bounds), control-flow characteristics (e.g., cyclo-    tially reduce manual warning review effort, addressing a major
matic complexity and number of panic paths), and unsafe operation        obstacle to adopting static analysis in CI/CD pipelines. Scalabil-
context (e.g., lifetime bypass categories and the distance between       ity is supported by the learned selective fuzzing strategy, which
unsafe operations). These features encode program properties that        invokes dynamic validation only for warnings with high classi-
are central to determining whether a warning reflects a genuine          fication uncertainty. In our experiments, fuzzing was applied to
soundness violation or conservative over-approximation by static         approximately 23% of warnings, enabling significant accuracy im-
analysis.                                                                provements while maintaining throughput suitable for large-scale
   Analysis-specific features derived from Rudra also contribute         continuous integration.
substantially. In particular, Rudra’s assigned precision level and          Although our evaluation focuses on Rudra, the methodology
warning clustering patterns provide useful signals. Such an obser-       itself is not tool-specific. The combination of semantic features
vation suggests that Rudra’s internal confidence estimates, while        from intermediate representations with structural and analysis-
insufficient on their own, contain meaningful information that the       specific metadata can be adapted to other Rust analyzers, such as
RL agent can effectively recalibrate when combined with richer se-       MirChecker and Yuga, as well as to static analysis tools for other
mantic context. Structural features, such as package popularity and      languages. More broadly, the RL framework’s ability to learn tool-
code complexity metrics, provide an additional but secondary sig-        specific warning characteristics suggests that similar approaches
nal. Although individually less predictive than MIR-level features,      may generalize across analyzers. An important direction for future
they help contextualize warnings at the package level. For example,      work is transfer learning across tools. Training on warnings from
warnings in widely used and actively maintained packages are more        multiple analyzers could enable more generalizable policies that
likely to be false positives, whereas warnings in highly complex         capture common distinctions between true bugs and false positives
code with limited documentation are more frequently associated           [47]. Our labeled dataset provides an initial foundation for exploring
with true positives. The dominance of MIR-level features corrobo-        such multi-tool learning scenarios.
rates our design choice, as MIR exposes precise type, control-flow,
and unsafe operation semantics that are difficult to recover from        5.2     Comparison with Alternative Approaches
source code, particularly in the presence of macros and deeply           One might question whether supervised learning with sufficient
nested generics.                                                         labeled data could achieve similar results without the complexity
   The comparatively lower global importance of fuzzing-related          of reinforcement learning. Our RL formulation offers several ad-
features requires careful interpretation. Fuzzing-derived features       vantages: (i) the ability to incorporate fuzzing as a strategic action
Mitigating False Positives in Static Memory Safety Analysis of Rust Programs via Reinforcement Learning   EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom


rather than a fixed post-processing step, (ii) the natural framework                     decision processes, may enhance the system’s ability to reason
for balancing accuracy against computational costs through reward                        about warnings.
shaping, and (iii) the potential for online learning and adaptation                         Recent advances in LLMs have introduced enhanced reasoning
as new warnings are encountered. However, we acknowledge that                            capabilities, like chain-of-thought prompting [56] and inference-
a well-designed supervised classifier with the same rich feature set                     time strategies [18, 39]. However, in our evaluation, LLMs were
might achieve competitive performance. The key advantage of RL                           used in a constrained classification setting without explicit reason-
lies in its flexibility for incorporating sequential decision-making                     ing prompts or intermediate explanations. As a result, the observed
(such as the choice to invoke fuzzing) and its conceptual clarity for                    performance reflects the ability of LLMs to directly infer decisions
representing the trade-offs inherent in false positive reduction.                        from code and warning context, rather than their full reasoning
   An alternative to our baseline comparison would be to fine-tune                       potential. While reasoning-enhanced prompting could potentially
code-specialized large language models on the labeled dataset used                       improve performance by enabling more structured analysis of pro-
in this study. Such fine-tuning would likely improve performance                         gram semantics, our current results suggest that even strong models,
relative to zero-shot or few-shot LLM baselines. However, fine-                          like Claude Opus 4.1, still struggle to match approaches that lever-
tuning LLMs typically requires substantial computational resources                       age explicit intermediate representations such as MIR. Exploring
and specialized expertise. Moreover, even fine-tuned models must                         the integration of reasoning strategies with structured represen-
still reason about complex semantic properties, such as lifetimes,                       tations remains an important direction for future work. Finally,
ownership, and unsafe abstractions, primarily from source-level                          while LLMs exhibit strong code reasoning capabilities, their use in
representations and limited context windows.                                             large-scale static analysis raises cost and scalability concerns. In
                                                                                         our experiments, proprietary models incurred nontrivial monetary
                                                                                         costs (approximately $5–$40 USD), which scale linearly with the
5.3     Challenges and Future Research Directions                                        number of warnings and may be prohibitive for ecosystem-wide or
Although our dataset of 4,879 manually labeled warnings represents                       continuous analysis. Open-source models mitigate monetary cost
a substantial labeling effort, it covers only approximately 20–25%                       but still impose substantial computational overhead.
of the crates.io ecosystem at the time of analysis. Consequently,
certain classes of unsafe code, particularly those in specialized
domains such as embedded systems or cryptography, may be un-                             6     Threats to Validity
derrepresented. The dataset also exhibits class imbalance (74.4%                         We discuss threats to the validity of our empirical evaluation.
false positives), which reflects Rudra’s real-world output distribu-                        Internal Validity. Ground-truth labels are derived from manual
tion. While our RL-based approach remains effective under this                           classification by a single expert. Despite careful review, mislabeling
imbalance (MCC = 0.323), expanding the dataset and improving                             remains possible due to the subtle and context-dependent nature
sampling strategies remain important directions for future work.                         of Rust memory safety violations. We mitigated this risk through
   While our evaluation focuses on Rudra, it remains an open ques-                       multiple review iterations and by excluding ambiguous cases. Fea-
tion how well learned policies generalize to other static analyzers                      ture extraction relies on analysis of Rust MIR, and implementation
without retraining. Different analyzers exhibit distinct false positive                  errors could introduce noise or bias. We reduced this risk through
characteristics due to their underlying design choices. Extending                        targeted testing and consistency checks, though residual errors may
our approach to other Rust analyzers, such as MirChecker or Yuga,                        remain. Model performance may also depend on hyperparameter
would enable the study of cross-tool generalization and transfer                         choices and fuzzing configurations. We tuned hyperparameters
learning, while adapting the methodology to analyzers for other                          via validation and selected fuzzing timeouts based on preliminary
languages represents a natural extension.                                                experiments, but alternative settings could yield different results.
   Fuzzing provides strong evidence for the presence of bugs but                            Construct Validity. We define ground truth in terms of memory
cannot prove their absence; therefore, clean runs serve only as                          safety violations rather than concrete exploitability, aligning with
negative evidence against a warning. Moreover, some bug classes,                         the goals of static analysis but differing from vulnerability-centric
such as Send/Sync variance issues, are difficult to trigger reliably                     perspectives. Similarly, the absence of a fuzzing-triggered failure
due to their dependence on specific thread interleavings. Finally,                       does not imply correctness, reflecting an inherent limitation of
the limited fuzzing time budget (30–60 seconds per warning) and                          dynamic analysis that may influence classification decisions. To
template-based harness generation constrain the depth of dynamic                         assess labeling reliability, a second reviewer independently analyzed
exploration. Future work could explore more precise harness con-                         a subsample of 150 cases, yielding 82.7% raw agreement and a
struction informed by inferred preconditions or data dependencies,                       Cohen’s 𝜅 = 0.63, indicating substantial inter-reviewer agreement.
as well as directed or adaptive fuzzing strategies that better balance                      External Validity. Our dataset consists of crates from crates.io
validation cost and classification confidence.                                           and may not fully represent Rust code in enterprise, embedded, or
   As previously discussed, our feature importance analysis high-                        OS-level settings. Moreover, our evaluation focuses exclusively on
lights promising directions for future work. The strong contribution                     warnings produced by Rudra; other analyzers may exhibit different
of MIR-level semantic features suggests that incorporating more                          false positive characteristics. Our fuzzing-based validation depends
precise program analyses, such as data-flow or alias analysis, could                     on external toolchains whose evolution could affect results. Finally,
further improve classification performance. Additionally, exploring                      the dataset reflects Rust code and tooling from 2024–2025; changes
learning architectures that model program structure more explicitly,                     in the language or ecosystem may require retraining to maintain
for instance, through graph-based representations or hierarchical                        effectiveness.
EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom                                                                      Akilesh et al.


    Conclusion Validity. While our test set of 732 warnings pro-         further improve code understanding [20, 42, 55]. However, such
vides reasonable statistical power, some analyses rely on smaller        models remain limited by context window constraints and their
subsets and thus have higher uncertainty. Reinforcement learning         inability to reason soundly about all execution paths.
introduces stochasticity through initialization and exploration; al-        Reinforcement learning has been explored more selectively, pri-
though we fix random seeds, results may vary across runs. Finally,       marily for guiding fuzzing, symbolic execution, test generation,
our LLM baselines use zero-shot prompting without fine-tuning,           and automated program repair [12]. Hybrid static–dynamic ap-
and thus represent general-purpose usage rather than best-case           proaches combine static reasoning with execution-based validation,
LLM performance.                                                         such as static-guided fuzzing and counterexample-guided refine-
    Ethical Considerations. Our study exclusively analyzes pub-          ment, but often apply dynamic validation uniformly, incurring high
licly available open-source code from crates.io. No human subjects       cost. Our work differs by framing false positive reduction as a se-
were involved, and all experimental data derives from published          quential decision-making problem, using reinforcement learning to
software artifacts distributed under open-source licenses.               adaptively determine when static evidence is sufficient and when
                                                                         dynamic validation via fuzzing is warranted, enabling scalable, cost-
                                                                         aware hybrid verification for Rust.
7    Related Work
This section surveys related work on memory safety analysis in           8   Conclusion and Future Work
Rust, learning-based warning classification, and hybrid static–dynamic   This paper introduced a reinforcement learning–based approach
verification, positioning our work as addressing the underexplored       for reducing false positives in static memory safety analysis of
problem of false positive reduction in scalable Rust analyzers           Rust programs. By leveraging rich semantic features extracted from
   Several static and verification tools target memory safety in         Rust’s Mid-level Intermediate Representation (MIR) and learning
Rust, each with distinct goals and trade-offs. Beyond Rudra, our         cost-aware classification policies, our approach substantially out-
target tool in this study, MirChecker analyzes Rust programs at the      performs both raw static analysis output and state-of-the-art LLM
MIR level to preserve type and lifetime information while checking       baselines. The integration of selective dynamic validation through
memory safety properties [32]. Its focus on different bug classes        fuzzing further improves accuracy while maintaining scalability.
and analysis techniques results in complementary coverage rather            Our empirical evaluation on 4,879 manually labeled warnings
than direct overlap. SMACK translates Rust programs into the Boo-        from 20,000 Rust crates shows that learning-based suppression
gie intermediate language and applies SMT-based verification to          policies can substantially improve the practical precision of static
prove correctness properties [10], while Prusti provides deductive       analysis without sacrificing recall. Specifically, our approach in-
verification for Rust by leveraging the Viper infrastructure and         creases precision from Rudra’s baseline of 25.6% to 59.0% while
user-supplied specifications [5]. While expressive and precise, both     maintaining a recall of 74.6%, effectively more than doubling the
approaches require manual annotations and are intended for verify-       proportion of reported warnings that correspond to genuine bugs.
ing small, critical components rather than ecosystem-scale analysis.     Overall, the proposed method achieves 65.2% accuracy and a 0.659
Miri is an interpreter for Rust MIR that detects undefined behav-        F1 score, representing a 17.1 percentage point improvement over
ior during execution [27]. While effective for uncovering subtle         the strongest LLM baseline.
bugs in test suites, Miri is fundamentally limited by dynamic path          Furthermore, integrating cargo-fuzz as a strategic action within
coverage and cannot provide the scalability required for whole-          the RL framework enables a principled combination of static and dy-
ecosystem analysis. In contrast to these tools, our work does not        namic analysis. Instead of treating fuzzing as a fixed post-processing
aim to strengthen static analyses or introduce additional annota-        step, the agent learns when dynamic validation is most valuable,
tions. Instead, we focus on reducing false positives produced by         yielding a 10.7 percentage point improvement in accuracy over
scalable analyzers such as Rudra through learning-based suppres-         static analysis alone while preserving computational feasibility.
sion.                                                                    Our modernized Rudra implementation, compatible with the cur-
   Empirical studies provide important context for memory safety         rent Rust ecosystem, supports continued research and practical
analysis in Rust. Evans et al. [19] report that unsafe code appears      deployment as the language evolves.
in approximately 25–30% of Rust crates, primarily for FFI and               Looking forward, promising directions include extending the ap-
performance-critical optimizations, with widely varying encap-           proach to additional static analyzers and programming languages,
sulation practices [4]. Most Rust-related CVEs arise from incorrect      improving fuzzing guidance and harness generation, and enabling
unsafe encapsulation rather than direct misuse [57], and misuse of       continuous adaptation through online learning. We believe that
Send and Sync traits remains a persistent source of concurrency          combining classical program analysis with learning-based decision-
errors [41].                                                             making represents a powerful path toward more effective and
   Machine learning has increasingly been applied to program anal-       trusted verification tools for safety-critical software.
ysis tasks such as bug detection and warning prioritization [52].
Early approaches rely on supervised learning, using either manually
engineered features or learned representations to classify warnings      Acknowledgments
[34, 40]. While effective for common bug patterns, these methods         This work was partially supported by the Natural Sciences and
require large labeled datasets and often struggle with rare or se-       Engineering Research Council of Canada, the Canadian Institute
mantically complex errors. Representation learning and pre-trained       for Advanced Research, and the Canada Research Chairs Program.
language models, including CodeBERT, CodeT5, and CodeLlama,
Mitigating False Positives in Static Memory Safety Analysis of Rust Programs via Reinforcement Learning          EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom


References                                                                                         672–681. doi:10.1109/ICSE.2013.6606613
 [1] 2025. https://github.com/Akileshdash/rl-guided-static-analysis-rust/blob/main/           [26] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2018.
     README.md.                                                                                    RustBelt: Securing the Foundations of the Rust Programming Language. In
 [2] 2025. https://github.com/Akileshdash/Rudra/blob/master/README.md.                             Proceedings of the ACM on Programming Languages (POPL), Vol. 2. 66:1–66:34.
 [3] aarc Developers. 2021. aarc crate, version 0.3.2. https://crates.io/crates/aarc/0.3.2.        doi:10.1145/3158154
     Accessed: 2026-01-10.                                                                    [27] Ralf Jung, Benjamin Kimock, Christian Poveda, Eduardo Sánchez Muñoz, Oli
 [4] Vytautas Astrauskas, Christoph Matheja, Federico Poli, Peter Müller, and Alexan-              Scherer, and Qian Wang. 2026. Miri: Practical Undefined Behavior Detection
     der J. Summers. 2020. How Do Programmers Use Unsafe Rust?. In Proceed-                        for Rust. Proceedings of the ACM on Programming Languages 10, POPL (2026),
     ings of the ACM on Programming Languages (OOPSLA), Vol. 4. 136:1–136:27.                      1383–1411.
     doi:10.1145/3428204                                                                      [28] Sunghun Kim and Michael D. Ernst. 2007. Which Warnings Should I Fix First?.
 [5] Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J Summers. 2019.              In Proceedings of the 6th Joint Meeting of the European Software Engineering
     Leveraging Rust types for modular specification and verification. In Proceedings              Conference and the ACM SIGSOFT Symposium on the Foundations of Software
     of the ACM on Programming Languages (OOPSLA), Vol. 3. 1–30.                                   Engineering (ESEC/FSE). 45–54. doi:10.1145/1287624.1287633
 [6] Nathaniel Ayewah, David Hovemeyer, J. David Morgenthaler, John Penix, and                [29] George Klees, Andrew Ruef, Benji Cooper, Shiyi Wei, and Michael Hicks. 2018.
     William Pugh. 2008. Using Static Analysis to Find Bugs. IEEE Software 25, 5,                  Evaluating Fuzz Testing. In Proceedings of the 2018 ACM SIGSAC Conference on
     22–29. doi:10.1109/MS.2008.130                                                                Computer and Communications Security (CCS). 2123–2138. doi:10.1145/3243734.
 [7] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon Lim, and Taesoo Kim. 2021.                     3243804
     Rudra: Finding Memory Safety Bugs in Rust at the Ecosystem Scale. In Proceedings         [30] Ted Kremenek, Ken Ashcraft, Junfeng Yang, and Dawson Engler. 2004. Corre-
     of the ACM SIGOPS 28th Symposium on Operating Systems Principles (SOSP). 84–99.               lation Exploitation in Error Ranking. In Proceedings of the 12th ACM SIGSOFT
     doi:10.1145/3477132.3483570                                                                   International Symposium on Foundations of Software Engineering (FSE). 83–93.
 [8] Al Bessey, Ken Block, Ben Chelf, Andy Chou, Bryan Fulton, Seth Hallem, Charles                doi:10.1145/1029894.1029909
     Henri-Gros, Asya Kamsky, Scott McPeak, and Dawson Engler. 2010. A Few                    [31] Yi Li, Aws Albarghouthi, Zachary Kincaid, Mayur Naik, et al. 2019. Hybrid
     Billion Lines of Code Later: Using Static Analysis to Find Bugs in the Real World.            program analysis for effective bug detection. In Proceedings of the ACM/IEEE
     In Communications of the ACM, Vol. 53. 66–75. doi:10.1145/1646353.1646374                     International Conference on Software Engineering.
 [9] Marcel Böhme, Van-Thuan Pham, Manh-Dung Nguyen, and Abhik Roychoudhury.                  [32] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John C. S. Lui. 2021. MirChecker:
     2017. Directed greybox fuzzing. In Proceedings of the 2017 ACM SIGSAC Conference              Detecting Bugs in Rust Programs via Static Analysis. In Proceedings of the 2021
     on Computer and Communications Security. 2329–2344.                                           ACM SIGSAC Conference on Computer and Communications Security (CCS). 2183–
[10] Montgomery Carter, Shaobo He, Jonathan Whitaker, Zvonimir Rakamarić, and                      2196. doi:10.1145/3460120.3484541
     Michael Emmi. 2016. SMACK software verification toolchain. In Proceedings of             [33] Kevin Lira, Baldoino Fonseca, Wesley KG Assunccao, Davy Baya, and Marcio
     the 38th International Conference on Software Engineering Companion. 589–592.                 Ribeiro. 2025. Beyond Code Explanations: a Ray of Hope for Cross-Language Vul-
[11] Microsoft Security Response Center. 2019. Why Rust for Safe Systems Program-                  nerability Repair. In 2025 2nd IEEE/ACM International Conference on AI-powered
     ming. https://msrc-blog.microsoft.com/2019/07/22/why-rust-for-safe-systems-                   Software (AIware). IEEE, 01–09.
     programming/. Accessed: 2024-12-10.                                                      [34] Guoming Long, Jingzhi Gong, Hui Fang, and Tao Chen. 2025. Learning Software
[12] Partha Chakraborty, Mahmoud Alfadel, and Meiyappan Nagappan. 2024. RLoca-                     Bug Reports: A Systematic Literature Review. ACM Transactions on Software
     tor: Reinforcement learning for bug localization. IEEE Transactions on Software               Engineering and Methodology (2025).
     Engineering (2024).                                                                      [35] Scott Lundberg and Su-In Lee. 2017. A Unified Approach to Interpreting Model
[13] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira                  Predictions. arXiv:1705.07874 [cs.AI] https://arxiv.org/abs/1705.07874
     Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman,          [36] Nicholas D. Matsakis and Felix S. Klock. 2014. The Rust Language. In Proceedings
     et al. 2021. Evaluating Large Language Models Trained on Code. In arXiv preprint              of the 2014 ACM SIGAda Annual Conference on High Integrity Language Technology
     arXiv:2107.03374.                                                                             (HILT). 103–104. doi:10.1145/2663171.2663188
[14] Maria Christakis and Christian Bird. 2016. What Developers Want and Need                 [37] Nathalia Nascimento, Everton Guimaraes, Sai Sanjna Chintakunta, and San-
     from Program Analysis: An Empirical Study. In Proceedings of the 31st IEEE/ACM                thosh Anitha Boominathan. 2025. How Effective are LLMs for Data Science
     International Conference on Automated Software Engineering (ASE). 332–343.                    Coding? A Controlled Experiment. In 2025 IEEE/ACM 22nd International Confer-
     doi:10.1145/2970276.2970347                                                                   ence on Mining Software Repositories (MSR). IEEE, 211–222.
[15] Cloudflare. 2020. Enjoy a Slice of QUIC, and Rust! https://blog.cloudflare.com/          [38] National Vulnerability Database. 2021. CVE-2020-36317. https://nvd.nist.gov/
     enjoy-a-slice-of-quic-and-rust/. Accessed: 2024-12-10.                                        vuln/detail/CVE-2020-36317. Accessed: 2026-01-09.
[16] National Vulnerability Database. 2020. CVE-2020-35905. https://nvd.nist.gov/             [39] Shubham Parashar, Blake Olson, Sambhav Khurana, Eric Li, Hongyi Ling, James
     vuln/detail/CVE-2020-35905. Accessed: 2026-01-09.                                             Caverlee, and Shuiwang Ji. 2025. Inference-time computations for llm reasoning
[17] National Vulnerability Database. 2021. CVE-2020-36323. https://nvd.nist.gov/                  and planning: A benchmark and insights. arXiv preprint arXiv:2502.12521 (2025).
     vuln/detail/CVE-2020-36323. Accessed: 2026-01-09.                                        [40] Michael Pradel and Koushik Sen. 2018. Deepbugs: A learning approach to name-
[18] Xiangjue Dong, Maria Teleki, and James Caverlee. 2024. A survey on llm inference-             based bug detection. Proceedings of the ACM on Programming Languages 2,
     time self-improvement. arXiv preprint arXiv:2412.14352 (2024).                                OOPSLA (2018), 1–25.
[19] Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa. 2020. Is Rust Used                [41] Boqin Qin, Yilun Chen, Zeming Yu, Linhai Song, and Yiying Zhang. 2020. Under-
     Safely by Software Developers?. In Proceedings of the ACM/IEEE 42nd International             standing Memory and Thread Safety Practices and Issues in Real-World Rust Pro-
     Conference on Software Engineering (ICSE). 246–257. doi:10.1145/3377811.3380413               grams. In Proceedings of the 41st ACM SIGPLAN Conference on Programming Lan-
[20] Z Feng. 2020. Codebert: A pre-trained model for program-ming and natural                      guage Design and Implementation (PLDI). 763–779. doi:10.1145/3385412.3386036
     languages. arXiv preprint arXiv:2002.08155 (2020).                                       [42] Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiao-
[21] Sushant Ghimire, Michael W. Godfrey, and Chanchal K. Roy. 2023. Yuga: Au-                     qing Ellen Tan, Yossi Adi, Jingyu Liu, Tal Remez, Jérémy Rapin, et al. 2023. Code
     tomatically Detecting Lifetime Annotation Bugs in the Rust Language. IEEE                     Llama: Open Foundation Models for Code. arXiv preprint arXiv:2308.12950 (2023).
     Transactions on Software Engineering 49, 4 (2023), 2075–2091. doi:10.1109/TSE.           [43] Rust Fuzzing Authority. 2024. cargo-fuzz: Fuzz testing for Rust. https://github.
     2022.3200162                                                                                  com/rust-fuzz/cargo-fuzz.
[22] Aaron Grattafiori et al. 2024.              The Llama 3 Herd of Models.                  [44] Rust Project Developers. 2025. Rust Version 1.88.0. https://doc.rust-lang.org/
     arXiv:2407.21783 [cs.AI] https://arxiv.org/abs/2407.21783                                     beta/releases.html#version-1880-2025-06-26. Accessed: 2026-01-10.
[23] Sarah Heckman and Laurie Williams. 2009. A Model Building Process for Iden-              [45] Rust Release Notes. 2021. Rust Version 1.56.0. https://doc.rust-lang.org/beta/
     tifying Actionable Static Analysis Alerts. In Proceedings of the 2009 Interna-                releases.html#version-1560-2021-10-21. Accessed: 2026-01-10.
     tional Conference on Software Testing Verification and Validation (ICST). 161–170.       [46] Joseph R. Ruthruff, John Penix, J. David Morgenthaler, Sebastian Elbaum, and
     doi:10.1109/ICST.2009.47                                                                      Gregg Rothermel. 2008. Predicting Accurate and Actionable Static Analysis
[24] Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche                 Warnings: An Experimental Approach. In Proceedings of the 30th International
     Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou                   Conference on Software Engineering (ICSE). 341–350. doi:10.1145/1368088.1368135
     Hanna, Florian Bressand, Gianna Lengyel, Guillaume Bour, Guillaume Lample,               [47] Iman Saberi, Amirreza Esmaeili, Fatemeh Fard, and Fuxiang Chen. 2025. Adv-
     Lélio Renard Lavaud, Lucile Saulnier, Marie-Anne Lachaux, Pierre Stock, Sandeep               Fusion: Adapter-based Knowledge Transfer for Code Summarization on Code
     Subramanian, Sophia Yang, Szymon Antoniak, Teven Le Scao, Théophile Gervet,                   Language Models. In 2025 IEEE International Conference on Software Analysis,
     Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed. 2024.                    Evolution and Reengineering (SANER). IEEE, 563–574.
     Mixtral of Experts. arXiv:2401.04088 [cs.LG] https://arxiv.org/abs/2401.04088            [48] Caitlin Sadowski, Edward Aftandilian, Alex Eagle, Liam Miller-Cushon, and
[25] Brittany Johnson, Yoonki Song, Emerson Murphy-Hill, and Robert Bowdidge.                      Ciera Jaspan. 2018. Lessons from Building Static Analysis Tools at Google. In
     2013. Why Don’t Software Developers Use Static Analysis Tools to Find Bugs?.                  Communications of the ACM, Vol. 61. 58–66. doi:10.1145/3188720
     In Proceedings of the 2013 International Conference on Software Engineering (ICSE).      [49] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov.
                                                                                                   2017. Proximal Policy Optimization Algorithms. arXiv:1707.06347 [cs.LG] https:
EASE 2026, 9–12 June, 2026, Glasgow, Scotland, United Kingdom                                                                                                Akilesh et al.


     //arxiv.org/abs/1707.06347                                                       [54] Linus Torvalds and Linux Kernel Team. 2022. Linux 6.1: Rust Support Merged
[50] Amazon Web Services. 2020. Why AWS Loves Rust, and How We’d Like to                   into Mainline Kernel. https://www.kernel.org/. Accessed: 2024-12-10.
     Help. https://aws.amazon.com/blogs/opensource/why-aws-loves-rust-and-how-        [55] Yue Wang, Weishi Wang, Shafiq Joty, and Steven CH Hoi. 2021. Codet5: Identifier-
     wed-like-to-help/. Accessed: 2024-12-10.                                              aware unified pre-trained encoder-decoder models for code understanding and
[51] Ayushi Sharma, Shashank Sharma, Sai Ritvik Tanksalkar, Santiago Torres-Arias,         generation. arXiv preprint arXiv:2109.00859 (2021).
     and Aravind Machiry. 2024. Rust for embedded systems: current state and open     [56] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi,
     problems. In Proceedings of the 2024 on ACM SIGSAC Conference on Computer and         Quoc V Le, Denny Zhou, et al. 2022. Chain-of-thought prompting elicits reasoning
     Communications Security. 2296–2310.                                                   in large language models. Advances in neural information processing systems 35
[52] Tushar Sharma, Maria Kechagia, Stefanos Georgiou, Rohit Tiwari, Indira Vats,          (2022), 24824–24837.
     Hadi Moazen, and Federica Sarro. 2021. A survey on machine learning techniques   [57] Hui Xu, Zhuangbin Chen, Mingshen Sun, Yangfan Zhou, and Michael R. Lyu.
     for source code analysis. arXiv preprint arXiv:2110.09610 (2021).                     2021. Memory-Safety Challenge Considered Solved? An In-Depth Study with
[53] Richard S. Sutton and Andrew G. Barto. 2018. Reinforcement Learning: An Intro-        All Rust CVEs. In ACM Transactions on Software Engineering and Methodology
     duction (2nd ed.). MIT Press.                                                         (TOSEM), Vol. 31. 3:1–3:25. doi:10.1145/3466642
                                                                                      [58] Michal Zalewski. 2014. American fuzzy lop. http://lcamtuf.coredump.cx/afl/.
