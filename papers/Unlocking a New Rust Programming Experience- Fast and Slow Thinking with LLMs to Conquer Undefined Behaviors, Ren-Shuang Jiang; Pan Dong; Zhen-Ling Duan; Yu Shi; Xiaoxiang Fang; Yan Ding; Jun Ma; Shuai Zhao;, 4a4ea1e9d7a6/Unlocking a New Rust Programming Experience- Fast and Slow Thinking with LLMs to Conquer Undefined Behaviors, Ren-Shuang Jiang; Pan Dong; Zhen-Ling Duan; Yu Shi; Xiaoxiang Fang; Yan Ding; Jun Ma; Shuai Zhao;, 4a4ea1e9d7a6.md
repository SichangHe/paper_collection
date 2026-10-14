                                           Unlocking a New Rust Programming Experience: Fast and
                                          Slow Thinking with LLMs to Conquer Undefined Behaviors
                                                         Renshuang Jiang                                         Pan Dong                                                Zhenlin Duan
                                            National University of Defense Technology          National University of Defense Technology              National University of Defense Technology
                                                        Changsha, China                                    Changsha, China                                        Changsha, China
                                                      rshuang@nudt.edu.cn                                pandong@nudt.edu.cn                                   15779658249@163.com

                                                            Yu Shi                                          Xiaoxiang Fang                                                 Yan Ding
                                        National University of Defense Technology            National University of Defense Technology                National University of Defense Technology
                                                    Changsha, China                                      Changsha, China                                          Changsha, China
                                                  shiyu19@nudt.edu.cn                                 xiaoxiang200@163.com                                      yanding@nudt.edu.cn

                                                           Jun Ma                                               Shuai Zhao                                         Zhe Jiang*
arXiv:2503.02335v1 [cs.SE] 4 Mar 2025




                                        National University of Defense Technology                         Sun Yat-sen University                               Southeast University
                                                   Changsha, China                                          Guangzhou, China                                     Nanjing, China
                                                  majun@nudt.edu.cn                                     zhaosh56@mail.sysu.edu.cn                            zhejiang.uk@gmail.com



                                           Abstract—To provide flexibility and low-level interaction capabilities,                    Fast Thinking                           Slow Thinking
                                        the “unsafe” tag in Rust is essential in many projects, but undermines
                                                                                                                          heuristic       Input: Rust code                    Decomposing      logical
                                        memory safety and introduces Undefined Behaviors (UBs) that reduce
                                        safety. Eliminating these UBs requires a deep understanding of Rust’s             intuitive           Feature
                                                                                                                                                                                                well-
                                                                                                                                                                             Verification &   considered
                                        safety rules and strong typing. Traditional methods require depth analysis        assumpt            Extraction                       Reasoning
                                        of code, which is laborious and depends on knowledge design. The power-             ions                                                              judgement
                                        ful semantic understanding capabilities of LLM offer new opportunities                                Solution
                                                                                                                          unconsc            Generation                      Generalization    formal
                                        to solve this problem. Although existing large model debugging frame-               ious
                                        works excel in semantic tasks, limited by fixed processes and lack adaptive
                                        and dynamic adjustment capabilities. Inspired by the dual process theory                            send back information in the form of feedback
                                        of decision-making (“Fast and Slow Thinking”), we present a LLM-based               Fig. 1: RustBrain: Fast and Slow thinking LLM processes.
                                        framework called RustBrain that automatically and flexibly minimizes
                                        UBs in Rust projects. Fast thinking extracts features to generate solutions,   essential to addressing Rust safety issues. Traditional methods [33]–
                                        while slow thinking decomposes, verifies, and generalizes them abstractly.     [37] require engineers to apply specialized knowledge along with
                                        To apply verification and generalization results to solution generation,
                                                                                                                       strict logical reasoning, judgment, and verification processes, where
                                        enabling dynamic adjustments and precise outputs, RustBrain integrates
                                        two thinking through a feedback mechanism. Experimental results on             the efficiency of resolution is closely tied to experience and expertise.
                                        Miri dataset show a 94.3% pass rate and 80.4% execution rate, improving        The powerful self-reasoning and semantic understanding capabilities
                                        flexibility and Rust projects safety.                                          of large language models (LLMs) offer new opportunities to enhance
                                                                                                                       the safety of Rust programs [10]–[13]. Due to high training costs and
                                                                  I. I NTRODUCTION                                     a lack of high-quality data in specific domains, conventional LLMs
                                           Rust, a systems programming language, is popular for its guaran-            struggle with deep understanding and complex relational reasoning
                                        tees of memory safety and concurrency [1], [2]. For flexibility, Rust          when handling specialized languages like Rust. In contrast, existing
                                        has a secondary language hidden inside it which does not enforce               large model repair frameworks [12], [13], while providing assistance
                                        memory safety guarantees: it’s called Unsafe Rust and works just like          for such problems, typically follow pre-designed and fixed repair
                                        regular Rust (it’s called Safe Rust). Safe Rust ensures safety through         processes, lacking the professional capabilities to tailor solutions
                                        strict compiler checks. Unsafe Rust uses unsafe keyword to grant               based on the specific characteristics of the code.
                                        direct control over memory and system resources, bypassing certain                Inspired by human cognitive psychology, “Thinking Fast and
                                        compiler checks, with safety guarantees that depend on the developer.          Slow” [14], we observe that LLMs provide a broad, generalized
                                        Therefore, this capability introduces the potential for Undefined              understanding that resembles the “fast thinking” of humans. This
                                        Behaviors (UBs), a class of run-time bugs that are difficult to detect         thinking is rapid and intuitive, but it is also error-prone reasoning. Yet,
                                        and can lead to severe security vulnerabilities and instability [3],           unlike human cognition, LLMs lack a “slow thinking” mechanism,
                                        [4]. Since Unsafe Rust cannot be avoided [5], especially in system             employing specialized knowledge and logical reasoning to enhance
                                        software, how to perform fixes is a key in ensuring Rust’s safety.             accuracy, identify discrepancies, and mitigate errors. This is crucial
                                           The main methods for fixing UBs in Unsafe Rust include safe                 when addressing complex problems that demand deliberate and
                                        substitution, inserting assertions, and semantic modification [6]–[9].         systematic approaches to detect inaccuracies and ensure correctness.
                                        Rust’s strongly typed system, along with its strict ownership, lifetime,       These two complementary processes – fast, intuitive reasoning and
                                        and borrowing rules, makes this process challenging, requiring an              slow, analytical reasoning – form a holistic framework for under-
                                        in-depth understanding of complex code semantics [40]. Although                standing and solving complex problems, e.g., solving UBs in Rust.
                                        the types of Unsafe Rust operations are finite (five types of unsafe              In light of this, we introduce RustBrain, a framework that integrates
                                        operation [1], [5]), minor semantic variation can significantly affect         these cognitive processes, leveraging their respective strengths to
                                        how code modification is approached [3], [9], leading to situations            autonomously and flexibly minimize UBs. As depicted in Fig. 1,
                                        where similar UB may not yield comparable solutions. Therefore,                in the fast-thinking process, it extracts code information, identifies
                                        understanding semantics and possessing specialized knowledge are               error types, and analyzes them using a broad knowledge base to
generate multiple repair solutions. In the slow-thinking process, the                                                F. Process1: Fast Thinking
framework in-depth analyzes and validates the repair solutions based                         F1.Using Miri Test                                  F2.Feature Extraction
                                                                                                                                                  Solution Generation
on the four design principles: decomposition, verification, reasoning
                                                                                                                                               Feature       Solution   Output
and generalization. First, the solutions are decomposed and executed                        Input:
                                                                                            Rust Code                 Miri Test
using multiple agents. In this stage, based on observations of Rust, we                       Safe
                                                                                                                     Errors:
                                                                                             Rust
designed several agents,including three types of error-fixing agents,                       Unsafe                  Undefined
                                                                                             Rust                   Behavior                                            Solution
adaptive rollback agent, and abstract reasoning agent, to support                                                                                                         1..N
better decomposition and verification. Then, the solution is fine-tuned                                                                                                             Feedback
based on verification results in slow-thinking, further optimizing          Solutions                                                                                               Solution
                                                                            as Input                                S. Process2: Slow Thinking                                     Optimization
the solution. Finally, to enhance the framework’s generalization
capability and better support precise solutions for similar errors,                                                               S2.Verfication                        S3.
                                                                                        S1.Decomposing                             & Reasoning                     Generalization
RustBrain establishes an evaluation and self-learning mechanism.                                                                                    Reasoning
                                                                                                                                Rollback              Better               Error
This feeds the execution and evaluation results from the slow-thinking                  Abstract solution
                                                                                                                                 Agent              steps from
                                                                                                                                                    evaluation
                                                                                                                                                                          Feature
                                                                                                                                 AST     `
stage back into the fast-thinking, continuously optimizing solution                     Decomposing step                         Agent
                                                                                                            Step1                                        Step2
generation and refining decision-making.                                                Solution1           Step2
                                                                                                            Step3
                                                                                                                            Fix Agent
                                                                                                                                                                           Better
                                                                                                                        Other tools……
   To evaluate RustBrain, we utilize a dataset containing UBs pro-                                  Step2
                                                                                                                                             Evaluate Reasoning           Solution

vided by Miri repository [17]. The results demonstrate that it achieves                                              Fine-tune Solution
94% pass rate and 80% execution semantic acceptability rate. Com-
pared to the state-of-the-art Rust fix tool (RustAssistant [13]), it        Fig. 2: RustBrain Overview: it leverages Miri for static analysis
pass rate has increased by 30% . Additionally, compared to engineer         (F1). Extracts and combines features for solution generation (F2).
experts, the speed evaluation shows an improvement of up to 18x.            Abstraction and decomposition into steps (S1), integrates multi-
                                                                            agent verification to reduce UBs. Evaluate and reason to fine-tune
                 II. RUST B RAIN : A N OVERVIEW                             solution(S2). Generalization provides a solution for such UBs(S3).
A. Scope
                                                                              • Stage F1 and F2: During fast thinking process, Rust code is
   Our goal is to build a toolchain that flexibly and systematically
                                                                                used as input, and Miri is utilized to detect UBs. If no UBs
evaluates the capabilities of RustBrain for eliminating UBs in Rust
                                                                                are found, the process terminates, outputting “pass”. Conversely,
at compile time. Repaired code must pass the Miri compiler while
                                                                                relevant errors, code, and design hints are sent to a LLM agent
preserving its expected semantics. Miri [17] is a UB detection
                                                                                for feature extraction. Subsequently, these features are integrated
tool for Rust. Since many Rust code repairs are closely tied to
                                                                                with another LLM to rapidly generate multiple repair solutions.
context, the acceptability of semantics before and after the repair
                                                                              • Stage S1: These solutions are decomposed, validated, reasoned
may vary significantly. Therefore, this paper validates semantics using
                                                                                and generalized during the slow thinking process. Each solution
test benchmarks composed of developer-repaired code. Compared to
                                                                                is broken down into refined steps to enable distributed pro-
direct testing through Miri, this semantic judgment approach may
                                                                                cessing and resolution by different agents. The order of these
introduce a degree of subjectivity. This is due to factors such as the
                                                                                steps reflects diverse repair strategies, enabling flexible process
size of the benchmark (i.e., the probability of covering all possible
                                                                                combinations to optimize repair paths and outcomes.
semantics) and other variables. Besides, we use Miri to detect Rust
                                                                              • Stage S2: This stage integrates multiple agents to verify solu-
UBs and only considers Rust source files (i.e, files with .rs extension).
                                                                                tions, including agents designed in previous work [27], [41], and
Errors not detected by Miri are beyond the scope of this paper. In
                                                                                new agents specifically developed based on Rust’s unique char-
addition, RustBrain uses LLMs to guide the reduction of UBs, and
                                                                                acteristics. These agents include: (i) safe-replacement, assertion-
we temporarily disregard Rust code that exceeds LLM tokens limits.
                                                                                adding, and code-modification agents fix UBs to improve code
B. RustBrain Overview                                                           safety. (ii) adaptive rollback agent to reduce hallucinations and
                                                                                propagation in LLMs by reverting to the optimal code state; (iii)
   According to Kahneman’s theory [14], human decision-making
                                                                                abstract reasoning agent supports deep semantic understanding
relies on two main processes: fast thinking, which handles intuitive,
                                                                                and provides more professional fixes. Additionally, the evalua-
quick, often unconscious decisions, and slow thinking, which tackles
                                                                                tion mechanism is designed to conduct multidimensional assess-
complex situations through logical reasoning and careful analysis
                                                                                ments of solutions and further refine them through reasoning. For
for well-considered choices. These are suitable for solving highly
                                                                                instance, increasing the iteration count, adjusting parameters in
specialized problems that require comprehensive analysis and precise
                                                                                the repair steps, optimizing the execution path, etc.
judgment. We observe that unsafe operations in Rust are limited and
                                                                              • Stage S3: To provide precise and efficient solutions for similar
rely on intuitive, pattern-driven processes, similar to fast thinking.
                                                                                errors, a generalized approach is essential. In the S3 stage, we
However, Rust’s strong type system requires specialized verification
                                                                                design a feedback mechanism to match and analyze error fea-
and improvements, similar to slow thinking. Therefore, RustBrain
                                                                                tures with optimized solutions, combining in-depth evaluation of
is designed as a dual-phase thinking framework incorporating fast
                                                                                slow thinking with generation of fast thinking. This self-learning
and slow thinking (see Fig. 2). Fast thinking is intuitive and rapidly
                                                                                approach leverages the strengths of both stages, reducing the
processes tasks, generating potential repair solutions based on code
                                                                                dependency of fixed frameworks on knowledge base and enables
features which include error identification, code feature extraction.
                                                                                dynamic solution refinement.
Slow thinking provides deliberate and in-depth processing. It com-
bines decomposition, validation, reasoning and generalization to               Overall, RustBrain integrates fast and slow thinking to eliminate
better understand the essence of the problem, delivering more targeted      Rust-UBs, overcoming the limitations of traditional repair frame-
and comprehensive solutions for these types of UBs. By leveraging           works. It also combines decomposition, verification, reasoning, and
these two types of thinking, the framework achieves adaptive and            generalization to achieve deep semantic understanding and expert-
high-precision repairs, improving both efficiency and reliability in        level support, providing more precise solutions for similar errors
eliminating UBs. RustBrain framework involves the following stages:         while reducing reliance on knowledge bases.
               III. RUST B RAIN I MPLEMENTATION                              •   Principle 1: All Unsafe Rust operations are explicitly marked
   This section explores the technical implementation of the “Fast               with the “unsafe” keyword, reducing the surface area for poten-
and Slow Thinking” framework. First, we classify five types of                   tial memory safety vulnerabilities facilitates error localization.
                                                                              • Principle 2: The limited types of UBs caused by Unsafe Rust
unsafe Rust operations and design the fast thinking process for
generating solutions (Section III-A). Then, we present the slow                  can be further classified into three categories: replaced by Safe
thinking process to decompose solutions and execute them with multi-             Rust, prevented by assertions and require semantic modification.
                                                                              • Principle 3: Under Rust’s strong typing characteristics, a single
agents: agents for errors fixing with LLMs (Section III-B1); agents of
rollback mechanisms and optimal code selection (Section III-B2) to               piece of code may exhibit multiple patterns, necessitating that
mitigate hallucinations; and abstract reasoning agents leveraging Rust           changes be combined with semantic analysis.
semantics for expert guidance(Section III-B3). Finally, the results           2) Fast Thinking Process: Undefined behaviors usually occur at
from the slow-thinking are feedback into the fast-thinking to refine       runtime. We believe that prevention is better than cure, therefore
evaluations and generate more specialized solutions (Section III-C).       RustBrain integrates tools such as Miri compiler to analyze the Rust
                                                                           code. This static analysis occurs at compile time, where the compiler
A. Classification of Unsafe Rust and Fast Thinking Process                 identifies potential UBs within the code, and records them for further
   To match the error types as closely as possible with the solutions      examination. Once the detection phase is complete, the framework
generated by the fast thinking process, we further classify Unsafe         enters the fast thinking process.
Rust from the perspective of error repair. This classification allows         In this process, RustBrain quickly identifies and generates fix
for targeted problem-solving by identifying the unique characteristics     solutions based on intuitive Unsafe Rust error pattern recognition.
and challenges of each type of unsafe operation.                           Firstly, RustBrain, based on five types of unsafe operations, employs
   1) Classification of Unsafe Rust: Rust’s unique design ensures          a general-knowledge LLM to rapidly analyze code features, lever-
that programs written in Safe Rust have no memory safety issues [5],       aging its generalization capability to identify typical error patterns
[22]. However, Unsafe Rust allows programmers to bypass these              and guide solution generation. According to Principle 1, UBs are
safety checks and perform certain operations. Unlike C, where unsafe       generally confined to unsafe regions, which narrows the scope of code
operations are everywhere and are barely checked by the com-               analysis and reduces the noise impact of irrelevant code on feature
piler [23], we observe that Rust explicitly classifies unsafe operations   extraction. Then, since Unsafe Rust operations are limited in types,
and limits them to “unsafe” code blocks. Even errors arising from          even with strong typing considerations, similar repair solutions can
interactions between unsafe and safe code occur within the “unsafe”        typically be found for most issues. Based on this, RustBrain generates
block. This design significantly reduces the surface area for potential    multiple repair solutions tailored to different code characteristics by
memory safety bugs, thereby facilitating error localization.               integrating Principle 2, ensuring that the repair methods are both
                                                                           adaptable and diverse in addressing the unique traits of the code.
   Unsafe Rust can be divided into five categories [1]: dereference raw
pointers, call unsafe functions, implement unsafe traits, access/modify    B. Slow Thinking Process
mutable static variables, and access union fields. Based on experience        After fast thinking generates preliminary solutions, RustBrain tran-
and research [4], [9], we further categorize Unsafe Rust from the          sitions into slow thinking for deeper thinking. Due to Principle 3, we
perspective of error fixing as follows: (i) Operations with Safe           need to further decompose, validate, infer, and generalize solutions.
Alternatives: Certain unsafe operations can be replaced with safer         First, RustBrain splits solutions into multiple steps, analyzing and
APIs from Rust’s standard library. (ii) Operations Checking via            addressing UBs layer by layer. Then, it integrates agents design to
Assertion: Adding assertions helps detect boundary and type viola-         validate and evaluate each generated solution’s compatibility with
tions, enhancing safety without fundamentally altering the program’s       type and safety requirements. We introduce new agents based on
structure. (iii) Operations Semantic Modification: Understanding           Rust features to support deep and professional fixes.
the underlying intentions of the original code, modifying erroneous           1) Three Types of Error Fixing Agents: To better guide LLM
semantics, and ensuring that these intentions are preserved in the         in fixing UBs errors, inspired by Principle 2, RustBrain constructs
modifications. Given Rust’s strong type system, we observe that            three types of special agents: equivalent replacement, assertion and
similar unsafe operations often require distinct handling methods.         modification. We observe that unsafe Rust is often misused, with
For instance, in case (i), as shown in Fig 3, the same unsafe API          some cases where safe code could achieve the same functionality [3],
may require different replacement APIs depending on the context.           [4], [9]. Therefore, RustBrain designs an agent to identify situations
          Safe Alternatives                                                where safe alternatives can replace unsafe operations. This minimizes
                                                                           unsafe code usage, enhancing the overall safety and reliability of
         Certain unsafe operation can be replaced with safe API.           Rust. Besides, we design an assertion agent that adds assertions in
          But same API requires different replacement methods
                                                                           appropriate places to capture potential UBs at runtime before they can
        1| let p = & 0;     Different sizes and alignment                  propagate. This avoids altering the code’s semantics while detecting
        2| let p = unsafe {mem::transmute::<&i32, usize>(p) };             and stopping potential UBs during execution in a timely manner,
                                                                           preventing it from leading to more severe security vulnerabilities.
        3|        Repalce: let p = p as *const i32 as usize ;
        4|                                                                 However, in certain complex scenarios, UBs involve deeper logical
        5| let n1 = [0x17,0x07] ;     Type size mismatch                   errors or dependencies on external states, and assertions alone cannot
        5| let n2 = unsafe{mem::transmute::<[u8;2],u32>(n1)};              directly resolve these issues. To address this, RustBrain introduces a
        6|                                                                 modification agent, where adjust the erroneous semantics in the Rust
                   Repalce: let n2 = u32::from_le_bytes(n1) ;
        7|                                                                 code, ensuring that the code’s functionality remains unchanged while
                                                      Replace
                                                                           effectively reducing the risk of UBs. Prompts are shown in the Fig. 4.
                                                                              2) Adaptive Rollback and Optimal Code Selection Agent: Using
   Fig. 3: The same API requires different substitution methods.           multiple fix agents can significantly reduce UBs in Rust code (Section
  Therefore, based on this classification, the following principles are    IV). However, we observe that in some cases, the number of errors
proposed in this paper to guide the framework design:                      increases after repair, and analyzed and discussed this.
                                                                                 retains the LLM’s reasoning capabilities while reducing the overhead
          Fast Thinking Generation                    Error Type &Example
                                                                                 generated by reasoning.
         [Ex1] Replace Box::into_raw() to as_ptr                use after free      3) Abstract Reasoning Agent: To better understand Rust’s unique
         [Ex2] Insert assert!(bytes<isize::MAX)                 out of bounds    programming semantics and conventions, we propose incorporating
         [Ex3] Modify lifetime ensure not released              use after free
                                                                                 a abstract reasoning knowledge agent to facilitate complex relational
                                                                                 reasoning and deeper insights.
          Slow Thinking Executaion                    Three Types Prmopt            Traditional debugging frameworks typically rely on source code
                                                                                 snippet libraries, syntax and API specifications, as well as error
                Root Cause: 1. A brief summary of Miri error. 2. The
                root cause of UB, referencing specific lines in code.
                                                                                 patterns and repair strategy libraries [9], [28], [29] to design knowl-
                                                                                 edge bases. However, these methods are not suitable for Rust. As
                Solution: It can be divided into three parts                     explained in Principle 3, Rust’s strong typing characteristics mean
           [Prompt1] Find Safe API with same functionally for replacement.
                                                                                 that a single unsafe API may exhibit multiple patterns simultaneously,
           [Prompt2] Pre-assertion added before UB is possible, prevent it .
           [Prompt3] Add assertion and replace cannot resolve, logic issues.     requiring knowledge bases with precise error pattern comprehension
           Keep functionally and semantic, avoidng UBs by modifications.         and adaptable fixes. Existing designs typically rely on pattern match-
                                                                                 ing and learning, which makes it difficult to cover all potential error
                Fig. 4: Three types of prompt strategies.                        scenarios [9]. Additionally, the complex syntax and nested structures
                                                                                 in Rust can introduce a large amount of invalid or misleading noise
   We define two sequences: T = {T0 , T1 , . . . , Tp } for thoughts             during the construction of the knowledge base, which interferes with
generated by slow thinking, and N = {n0 , n1 , . . . , np } for errors           the judgment and generation of LLM and limits the effectiveness of
detected by Miri, where Ti represents thoughts, ni the errors count,             these methods. Therefore, RustBrain introduces a knowledge base
and p the iteration count. During the slow thinking, the error                   centered on AST (Abstract Syntax Tree) and semantic analysis.
sequence N may continue to grow, as in the example sequence
                                                                                          Extract AST               Prune AST                  Fix UBs Agent
N1 = {1, 3, 4, 6, 9}. This phenomenon is known as “large model                             with LLM                 Query SQL
hallucination” [24], [25]. As shown in Fig. 5 (a), without rollback                                                 - Location Unsafe               - Modify prompt
                                                                                                                                                    - Shot AST prompt
                                                                                                                    - Error Cause
mechanism, the process would proceed from the current error stage                                                   - Prune AST Tree                - Generation code
to the next stage, exacerbating the impact of hallucinations. Existing                                              -Vector Error AST       Error             Correct
                                                                                   Rust      LLM     AST            -Compare similarities   AST                  AST
debugging frameworks [26], [27] typically rollback directly to the                 Code     Layer   Layer           -Extract correct AST

initial state T0 to eliminate accumulated errors and mitigate the
                                                                                                        Fig. 6: Abstract Reasoning Agent.
propagation of incorrect fixes. However, this discards valuable partial
corrections made during the iteration process and creates a large                  As shown in Fig. 6, RustBrain extracts the code’s AST using
overhead (c ∗ Tn , where c is the number of rollbacks) [26].                     LLM instead of traditional Rust parsing tools like syn. The AST
   We observe another type of error sequence, such as N2 =                       constructed by syn is overly complex and lacks higher-level semantic
{3, 1, 5, 2, 0}. This indicates that while errors may increase in certain        understanding. LLM not only preserves the semantic context of the
iterations, the overall trend shows a fluctuating decline. This behavior         code but also flexibly handles the complex contextual relationships.
is similar to humans often providing frequent and random errors                  However, the AST extracted contains irrelevant or noisy information,
during reasoning, but eventually decrease them and converge to a                 which distracts the model’s attention and decreasing fix performance.
solution. Therefore, we suggest that slow thinking a certain degree              According to Principle 1, all Unsafe Rust operations are marked with
of self-correcting capability, allowing it to gradually converge towards         “unsafe” keyword. RustBrain designs a pruning algorithm (as shown
the correct through multiple iterations.                                         in Algo.1) to retain safety-relevant and functional fix components,
                                                                                 minimizing the interference of irrelevant code for the LLM, thus
           Q                           Q
                                                                                 improving the efficiency and accuracy of the repair process.
                                                                Q Question
           T1
                             T1
                                                ×
                                                T2
                                                       Assert
                                                                Tn Thought        Algorithm 1: Pruning irrelevant nodes for Rust AST.
                                                                                   Input: Original Rust AST: Aorig ; Miri errors: EM iri ;
          ×T2
                       T6         T7       T3    T4       T5
                                                                    Result
                                                                    Forward
                                                                   reasoning
                                                                                   Output: Pruned AST: Apruned ;
                                                                                   Initialize pruned AST Apruned ← ∅; foreach node in Aorig
           T3                                                         Bad           do
                                                                ×
          ×R1
                                  R2
                                                ×R1
                                                       Modify
                                                                   Thought
                                                                    Rollback
                                                                                        if node contains unsafe keyword then
                                                                                            Mark the node as unsafe operation; Add node to
                                                                                             Apruned ;
     (a) No rollback        (b) Two stage adaptive rollback mechanism
       mechanism                                                                   foreach unsafe node in Apruned do
                                                                                       if EM iri != 0 then
Fig. 5: No Rollback Mechanism and Adaptive Rollback Mechanism.                             Analyze context of error node;
   Based on the analysis, RustBrain introduces an adaptive rollback                        if context node is irrelevant to unsafe operation then
mechanism that selects intermediate states intelligently, enabling a                           delete context node to Apruned ;
more precise and efficient correction process. As shown in Fig. 5
(b), before proceeding to the next stage, the process rollback to                  return Apruned ;
the optimal code state (the fewest detected errors) to prevent error
propagation. This ensures that subsequent iterations are based on the               Finally, RustBrain vectorizes the pruned AST and uses similarity-
most refined and stable version of the code, minimizing error propa-             based search to query the knowledge base, retrieving repair solutions
gation and improving overall fix accuracy. The rollback overhead is              for error-prone AST structures. These solutions are added to prompts
expressed as: c ∗ Tn−a (where a is the number of thoughts produced               to guide the LLM in generating precise fixes for semantically similar
in the assertion). Compared to direct rollback, RustBrain significantly          code, which improves repair accuracy (Section IV).
C. Feedback Mechanism in Fast and Slow Thinking
   Fast and slow thinking improves the flexibility and accuracy in
eliminating Rust UBs. However, the quality of the results from slow
thinking are not evaluated against fast thinking solutions. It limits
dynamic adjustment of repair solution based on discovered issues,
leading to the persistence of incorrect or inadequate repair solutions
and affecting the overall effectiveness of the repair process.
   RustBrain designs a feedback mechanism that integrates validation
results into solution generation, allowing further adjustments to initial
solutions. Specifically, we establish a triplet: (accuracy, acceptability,   Fig. 7: RustBrain flexibly fixes UBs. Agents, shown on the left,
overhead), to evaluate solutions from multiple dimensions. Accuracy          can be enabled [ ] or disabled [ ], with serial numbers indicating
ensures the solution passes Miri; acceptability checks semantics             repair order. Blue denotes agents used in execution, and red indicates
consistency; and overhead measures execution time and resource use.          semantically acceptable code, otherwise it only passes Miri.
Through multi-dimensional evaluation and feedback mechanism, fast-           on knowledge base. (iii) Fixed repair framework can cover a wide
thinking is able to absorb the precise analysis and validation infor-        range of issues, it often includes numerous generic steps, which may
mation from slow-thinking, allowing the generated repair solutions           introduce unnecessary complexity and overhead (Group 3). RustBrain
to achieve a better balance between speed and accuracy, effectively          dynamically designs solutions based on code features, avoiding
enhancing the overall quality and reliability of the repairs. Moreover,      redundant steps and improve accuracy. (iv) Specific scenarios exist for
this self-learning process enhances RustBrain’s generalization ability,      the three types of repair solutions for UBs. Fixed repair frameworks
supports similar errors repairs, reduces dependency on the knowledge         often provide inappropriate solutions, exacerbate hallucination and
base, and avoids the limitations posed by highly specialized issues.         reduce accuracy. In Groups 3, 7, and 10, even with knowledge base
                                                                             support, semantic acceptable fixes could not be achieved. RustBrain,
                           IV. E VALUATION                                   based on code features and feedback mechanism, better guides the
   The evaluation of RustBrain designed to answer the following              generation of solutions for similar error types, avoiding unsuitable
research questions:                                                          fixes and improving both repair accuracy and efficiency.
                                                                                RQ2 (Accuracy): We evaluated RustBrain’s repair effectiveness
   1) RQ1 (Flexibility): How does RustBrain flexibility affect repair
                                                                             and robustness using various configurations, including different
       pass rate and performance?
                                                                             LLMs and knowledge base usage. Experimental results, shown in
   2) RQ2 (Accuracy): What extent is RustBrain successful in fixing
                                                                             Fig. 8 and Fig. 9, compare repair pass rates and semantic exec rates.
       Rust UBs errors as measured by metrics of pass and exec?                 Results indicate that for GPT-4 model, integrating RustBrain
   3) RQ3 (Sensitivity): How does LLM configurations in GPT-4                achieved a pass rate of 90.5% and an execution rate of 70.2%,
       impact the performance of RustBrain?                                  representing an improvement of 25-35% compared to using GPT-4
   4) RQ4 (Advancement): How does the effectiveness and per-                 alone for repair. Furthermore, when RustBrain is integrated with the
       formance of RustBrain in eliminating UBs compared to the              knowledge base, it achieves the highest pass and execution rates,
       state-of-the-art method and human expert?                             averaging 94.3% and 80.4% , respectively. Additionally, although
   Firstly, we give a brief explanation of the datasets, large language      GPT-3.5 performed lower than GPT-4, combining it with RustBrain
models, baselines and metrics used in this paper.                            achieved a comparable level to GPT-4 in terms of fix pass and execu-
Datasets. We use a dataset collected from the official Miri [17],            tion rate. This suggests that the design in RustBrain compensates for
containing code with UBs. The dataset is categorized into different          the limitations of the base model, improving the accuracy and con-
types, including alloc, dangling pointers, and concurrency issues.           sistency in handling UBs. For Claude-3.5, it exhibits initial semantic
LLMs. We use four LLMs: GPT-3.5 [18], GPT-4 [19], GPT-O1 [20],               capabilities in reducing UBs, comparable to GPT-4. However, when
and Claude 3.5 [21], each with a default temperature of 0.5.                 combined with RustBrain, Claude-3.5 performs less effectively than
Baselines. Apart from the Miri test, the comparison includes state-          GPT-4 in understanding complex dependencies and resolving issues.
of-the-art approaches such as human expert repair (Thetis-Lathe,             Compared to standalone Claude-3.5, RustBrain+Claude-3.5 improves
2023) [3], and a LLM-based fix method (RustAssistant, 2024) [13].            the pass rate and execution rate by 17% and 20%, respectively.
Metrics. All experiments report pass rate(%) and execution rate(%),             Besides, we also compare RustBrain with the state-of-the-art GPT
among which pass rate refers to the percentage of code passing Miri          model, GPT O1. Due to O1’s high cost, a subset of error types
after repair, and execution rate refers to the percentage of code passing    was analyzed, with results shown in Fig. 10. Despite GPT-O1’s
Miri with acceptable semantics.                                              exceptional reasoning, its repair effectiveness remains inferior to
   Subsequently, we analyze the results to answer these questions.           RustBrain. For uncommon errors like panic errors, GPT-O1 fails
   RQ1 (Flexibility): We select a type of UB (requiring semantic             to provide suitable solutions based on code features. In contrast,
modification) and input it into RustBrain. Ten solutions are generated       RustBrain, leverages the combination of fast and slow thinking to
through fast thinking, followed by reasoning and validation using            generate more targeted solutions, improving execution rate by 35.6%.
slow thinking, as depicted in Fig. 7.                                           RQ3 (Sensitivity): Temperature is a key parameter affecting output
   RustBrain provides more flexible solution and improves the possi-         diversity in model generation [30]. We conduct sampling tests in Miri
ble and accuracy of fixing UBs. The results indicate that: (i) For same      dataset and evaluate the stability of the repair results by calculating
problem, RustBrain uses fast thinking to generate diverse solutions,         the confidence intervals [31]. The Confidence Interval(CI) reflects the
overcoming the limitations of fixed-process frameworks that offer            uncertainty of fixing UBs in LLMs, ensuring that the reported pass
only one option, enhancing flexibility and repair effectiveness. (ii)        and exec rates are reliable within a certain probability range (c=95%).
Comparing Group 1 with Groups 5, 6, 8, and 9, knowledge base                 In the experiments, we analyze the impact of different temperature
can enhance problem-solving abilities, but introduce 2x-4x overhead,         settings on the performance of RustBrain in GPT-4.
and depends on its size. Feedback mechanism supports more accurate              As shown in Fig. 11, pass and exec rates reach highest points
solution selection, improves repair performance and reduces reliance         of 97% and 77% with a temperature of 0.5. Higher temperatures
                                                                                 GPT-3.5          Claude-3.5     GPT-4         GPT-3.5+RustBrain                                                                                            GPT-3.5          Claude-3.5     GPT-4         GPT-3.5+RustBrain
                                                                             Claude-3.5+RustBrain     GPT-4+RustBrain(non knowledge)    GPT-4+RustBrain                                                                                 Claude-3.5+RustBrain     GPT-4+RustBrain(non knowledge)     GPT-4+RustBrain
            100                                                                                                                                                                             100
  Code Pass by Miri(%)


                          80                                                                                                                                                                             80




                                                                                                                                                                                    Execution(%)
                          60                                                                                                                                                                             60

                          40                                                                                                                                                                             40

                          20                                                                                                                                                                             20

                                  0                                                                                                                                                                       0
                                                       c            r                      e                          .call         ter                    dity                                                        c            r                                               .call         ter                  dity
                                                  allo         inte                ic
                                                                                pan venanc      borr
                                                                                                     ow     race              .poin           rrow     vali            lign
                                                                                                                                                                            e   d
                                                                                                                                                                                                                  allo         inte        pan
                                                                                                                                                                                                                                                 ic
                                                                                                                                                                                                                                                      ena
                                                                                                                                                                                                                                                          nce borrow      race              .poin           rrow   vali          lign
                                                                                                                                                                                                                                                                                                                                      ed
                                                           gpo                                          data     func                     kbo                       una                                                    gpo                                       data      func                     kbo                   una
                                                      glin                         pro     both                          func        stac                                                                             glin                       prov       both                       func        stac
                                                  dan                                                                                                                                                         dan
                                                                      Fig. 8: RustBrain fixes UBs pass by Miri rate.                                                                                               Fig. 9: RustBrain fixes UBs semantic acceptability rate.
                                                                                    GPT-4+RustBrain(Pass)                  GPT-O1+RustBrain(Pass)                                                                                         GPT-4+RustBrain(Pass)      Rustassisant(Pass)     GPT-4+RustBrain(Exec)
                                                                                    GPT-4+RustBrain(Exec)                  GPT-O1+RustBrain(Exec)                                                                                                   Rustassisant(Exec)        GPT-4+RustBrain(Non Knowledge Exec)
                                                    100                                                                                                                                                  100




                                                                                                                                                                                     pass/exec rate(%)
                                          pass/exec rate(%)




                                                              80                                                                                                                                          80

                                                                                                                                                                                                          60
                                                              60
                                                                                                                                                                                                          40
                                                              40
                                                                                                                                                                                                          20
                                                              20
                                                                                                                                                                                                              0
                                                               0                                                                                                                                                       c       r             ic      e             it    w      e        ll      r       w                dity ligned
                                                                                                       r                                                                                                           allo pointe            pan venanc           unin borro atarac func.ca c.pointe kborro              vali
                                                                    allo
                                                                        c             all         inte              ter   pan
                                                                                                                              ic
                                                                                                                                        gne
                                                                                                                                            d             .ca  ll
                                                                                                                                                                                                                      glin
                                                                                                                                                                                                                           g                                      both     d
                                                                                                                                                                                                                                                                                               stac                           una
                                                                                tailc          gpo            .poin                 nali             func                                                         dan
                                                                                                                                                                                                                                            pro                                        fun
                                                                                          glin           func                      u
                                                                                     dan
                                                                                                                                                                                    Fig. 12: Comparison of RustBrain with RustAssisant on UBs Repair.
 Fig. 10: Comparison of RustBrain with GPT-O1 on UBs Repair.
                                                              1.1                                                                                                                   cise solutions, without being fully dependent on the design of the
                                                                      Exec CI
                                                               1        Exec                                                                                                        knowledge base, reducing the overhead and time to fix UBs.
                                                                      Pass CI
                                                                        Pass
                                                              0.9                                                                                                                                                    TABLE I: Execution Time of RustBrain against Human
                         Proportion (%)




                                                              0.8
                                                                                                                                                                                                                                                                Average Time/s
                                                              0.7
                                                                                                                                                                                                                        Types                             GPT-4+RustBrain                                                      Speedup
                                                                                                                                                                                                                                                                                                          Human
                                                              0.6                                                                                                                                                                                     No knowledge   knowledge
                                                              0.5                                                                                                                                           stack borrow                                   86           123                                 366                      2.81x
                                                                                                                                                                                                         unaligned pointer                                 74           118                                 222                      4.63x
                                                              0.4
                                                                                                                                                                                                               validity                                    79           109                                 678                      8.58x
                                                                       0.1        0.2          0.3          0.4      0.5      0.6          0.7           0.8              0.9                                   alloc                                      40            77                                 450                     11.25x
                                                                                                                  Temperature                                                                              func. pointer                                   39            50                                 480                     12.3x
             Fig. 11: Different Temperatures on RustBrain Repair Efficacy.                                                                                                                                   provenance                                    45            64                                 240                      5.33x
                                                                                                                                                                                                                panic                                      76           107                                 336                      4.42x
increase the flexibility of outputs. However, this flexibility comes                                                                                                                                         func. calls                                   65            74                                 1176                     18.1x
at the cost of semantic integrity, leading to a decrease in semantic                                                                                                                                     dangling pointer                                  70            74                                 114                      1.63x
acceptability (e.g, 0.7). In contrast, lower temperatures limit flexibility                                                                                                                                both borrow                                     69            87                                 762                       11x
and potentially missing opportunities to repair UBs.                                                                                                                                                        concurrency                                    45            45                                 144                      3.2x
   RQ4 (Advancement): To evaluate the effectiveness and efficiency                                                                                                                                            data race                                    63            91                                 336                      5.3x
                                                                                                                                                                                                               Average                                    62.6          84.9                                442                      7.4x
of RustBrain, compared to RustAssistant (the state-of-the-art Rust fix
tool) and human experts. As shown in Fig. 12, compared to RustAs-                                                                                                                                            V. R ELATED W ORK
sisant, the pass rate and execution rate of RustBrain increased by 33%                                                                                                                 Efforts to improve Rust’s safety target Unsafe Rust, divided
and 41%, respectively. This indicates that RustBrain offers greater                                                                                                                 into manual, semi-automated, and fully automated methods. Manual
flexibility, breaking the limitations of existing repair frameworks. It                                                                                                             methods, like formal methods [33], [34], static analysis [35], [36],
is able to address issues that the current frameworks cannot solve,                                                                                                                 rely on developer expertise for precise fixes but are time-consuming
thereby reducing UBs and improving overall safety.                                                                                                                                  and error-prone. Semi-automated methods, such as symbolic ex-
   To evaluate RustBrain’s effectiveness compared to human experts,                                                                                                                 ecution [37], [38], combine tool-based detection with developer
we assessed their performance across various error types, as shown                                                                                                                  analysis. Fully automated methods use machine learning [9], [39] and
in Table I. While human experts excel in debugging, the framework                                                                                                                   LLMs [12], [13] to reduce human involvement but face limitations
demonstrates competitive performance in addressing UBs caused by                                                                                                                    in accuracy, coverage, and contextual understanding. Our approach
complex semantic rules. On average, RustBrain achieves a 7x speedup                                                                                                                 employs a collaboration of fast and slow thinking to provide flexible
across different error types, with the gap widening for more complex                                                                                                                and precise repair solutions while maintaining the safety of the Rust.
or rare errors. For example, in function pointer UBs, which mainly
involve type conversion problems and require deeper Rust expertise                                                                                                                                           VI. C ONCLUSION
for guidance, RustBrain shows up to 18x. Furthermore, we note                                                                                                                          We propose RustBrain, a dynamic, automated framework to elim-
that when the dataset contains similar UBs, RustBrain can reduce                                                                                                                    inate UBs in Rust projects. Combine fast and slow thinking two
dependency on the knowledge base and generate precise solutions                                                                                                                     phases, RustBrain overcomes traditional framework limitations, offer-
through the feedback mechanism, effectively minimizing UBs and                                                                                                                      ing flexible fixes and enhancing Rust code safety. The fast-thinking
overhead, as shown in the red sections of Table I.                                                                                                                                  phase extracts code features to generate multiple fixes, while the
   Overall, fixed frameworks like RustAssistant rely on their knowl-                                                                                                                slow-thinking phase employs Rust feature-based agents to execute
edge base for speedup over human experts, but their problem-solving                                                                                                                 solutions. Feedback from execution refines decision-making. Exper-
ability is constrained by the knowledge they contain. RustBrain                                                                                                                     imental show RustBrain achieves pass rate of 94.3% and exec rate
leverages a feedback mechanism that feeds back evaluated solutions                                                                                                                  80.4%, with up to 7x speedup compared with human experts. Future
from the slow-thinking phase into the fast-thinking phase. Through                                                                                                                  work, we are interested in providing automated safety enhancements
this self-learning process, the fast-thinking can generate more pre-                                                                                                                for complex Rust code involving multi-module calls.
                               R EFERENCES                                       [29] Sun K, Xu Y E, Zha H, et al. Head-to-tail: How knowledgeable are large
                                                                                      language models (llm)? AKA will llms replace knowledge graphs?[J].
 [1] Matsakis N D, Klock F S. The rust language[J]. ACM SIGAda Ada                    arXiv preprint arXiv:2308.10168, 2023.
     Letters, 2014, 34(3): 103-104.                                              [30] Renze M, Guven E. The effect of sampling temperature on problem
 [2] StackOverflow.          https://stackoverflow.blog/2024/07/24/developers-        solving in large language models[J]. arXiv preprint arXiv:2402.05201,
     want-more-more-more-the-2024-results-from-stack-overflow-s-annual-               2024.
     developer-survey/                                                           [31] Smithson M. Confidence intervals[M]. Sage, 2003.
 [3] Jiang R, Dong P, Ding Y, et al. Thetis: A Booster for Building Safer        [32] Dewey J. Reconstruction in philosophy[M]. Beacon Press, 1971.
     Systems Using the Rust Programming Language[J]. Applied Sciences,           [33] Jung R, Jourdan J H, Krebbers R, et al. RustBelt: Securing the foun-
     2023, 13(23): 12738.                                                             dations of the Rust programming language[J]. Proceedings of the ACM
 [4] Qin B, Chen Y, Yu Z, et al. Understanding memory and thread safety               on Programming Languages, 2017, 2(POPL): 1-34.
     practices and issues in real-world Rust programs[C]//Proceedings of the     [34] Astrauskas V, Müller P, Poli F, et al. Leveraging Rust types for
     41st ACM SIGPLAN Conference on Programming Language Design                       modular specification and verification[J]. Proceedings of the ACM on
     and Implementation. 2020: 763-779.                                               Programming Languages, 2019, 3(OOPSLA): 1-30.
 [5] Zhu S, Zhang Z, Qin B, et al. Learning and programming challenges of        [35] Li Z, Wang J, Sun M, et al. MirChecker: detecting bugs in Rust
     rust: A mixed-methods study[C]//Proceedings of the 44th International            programs via static analysis[C]//Proceedings of the 2021 ACM SIGSAC
     Conference on Software Engineering. 2022: 1269-1281.                             conference on computer and communications security. 2021: 2183-2196.
 [6] Bae Y, Kim Y, Askar A, et al. Rudra: finding memory safety bugs in          [36] Cui M, Chen C, Xu H, et al. SafeDrop: Detecting memory deallocation
     rust at the ecosystem scale[C]//Proceedings of the ACM SIGOPS 28th               bugs of rust programs via static data-flow analysis[J]. ACM Transactions
     Symposium on Operating Systems Principles. 2021: 84-99.                          on Software Engineering and Methodology, 2023, 32(4): 1-21.
 [7] Bang I, Kayondo M, Moon H, et al. TRust: A Compilation Frame-               [37] Lindner M, Fitinghoff N, Eriksson J, et al. Verification of safety
     work for In-process Isolation to Protect Safe Rust against Untrusted             functions implemented in Rust-a symbolic execution based ap-
     Code[C]//32nd USENIX Security Symposium (USENIX Security 23).                    proach[C]//2019 IEEE 17th International Conference on Industrial In-
     2023: 6947-6964.                                                                 formatics (INDIN). IEEE, 2019, 1: 432-439.
 [8] Cui M, Chen C, Xu H, et al. SafeDrop: Detecting memory deallocation         [38] Lindner M, Aparicius J, Lindgren P. No panic! Verification of Rust
     bugs of rust programs via static data-flow analysis[J]. ACM Transactions         programs by symbolic execution[C]//2018 IEEE 16th International Con-
     on Software Engineering and Methodology, 2023, 32(4): 1-21.                      ference on Industrial Informatics (INDIN). IEEE, 2018: 108-114.
 [9] Dong Y, Zhang Z, Cui M, et al. SafeNet: Towards mitigating replaceable      [39] Lu X, Zhang Z, Xu H. Safe Rust Code Recommendation Based
     unsafe Rust code via a recommendation-based approach[J]. Software                on Siamese Graph Neural Network[C]//2022 IEEE 27th Pacific Rim
     Testing, Verification and Reliability, 2024: e1875.                              International Symposium on Dependable Computing (PRDC). IEEE,
[10] Zhong L, Wang Z, Shang J. Ldb: A large language model debug-                     2022: 1-11.
     ger via verifying runtime execution step-by-step[J]. arXiv preprint         [40] Jung R. Understanding and evolving the Rust programming language[J].
     arXiv:2402.16906, 2024.                                                          2020.
[11] Li H, Hao Y, Zhai Y, et al. Enhancing Static Analysis for Practical Bug     [41] Kang S, Chen B, Yoo S, et al. Explainable automated debugging
     Detection: An LLM-Integrated Approach[J]. Proceedings of the ACM                 via large language model-driven scientific debugging[J]. arXiv preprint
     on Programming Languages, 2024, 8(OOPSLA1): 474-499.                             arXiv:2304.02195, 2023.
[12] Wu X, Cheriere N, Zhang C, et al. RustGen: An Augmentation Approach
     for Generating Compilable Rust Code with Large Language Models[J].
[13] Deligiannis P, Lal A, Mehrotra N, et al. RustAssistant: Using LLMs to
     Fix Compilation Errors in Rust Code[C]//2025 IEEE/ACM 47th Inter-
     national Conference on Software Engineering (ICSE). IEEE Computer
     Society, 2024: 267-279.
[14] Daniel K. Thinking, fast and slow[M]. 2017.
[15] Booch G, Fabiano F, Horesh L, et al. Thinking fast and slow in
     AI[C]//Proceedings of the AAAI Conference on Artificial Intelligence.
     2021, 35(17): 15042-15046.
[16] Ganapini M B, Campbell M, Fabiano F, et al. Thinking fast and
     slow in AI: The role of metacognition[C]//International Conference on
     Machine Learning, Optimization, and Data Science. Cham: Springer
     Nature Switzerland, 2022: 502-509.
[17] Miri.https://github.com/rust-lang/miri.
[18] OpenAI. GPT-3.5. https://platform.openai.com/docs/models/gpt-3-5.
[19] OpenAI. GPT-4. https://platform.openai.com/docs/models#gpt-4-turbo-
     and-gpt-4.
[20] OpenAI. GPT-O1-Preview. https://platform.openai.com/docs/models#o1
[21] Claude 3.5. https://www.anthropic.com/claude/sonnet.
[22] Jung R, Jourdan J H, Krebbers R, et al. RustBelt: Securing the foun-
     dations of the Rust programming language[J]. Proceedings of the ACM
     on Programming Languages, 2017, 2(POPL): 1-34.
[23] Ling M, Yu Y, Wu H, et al. In Rust we trust: a transpiler from unsafe
     C to safer Rust[C]//Proceedings of the ACM/IEEE 44th international
     conference on software engineering: companion proceedings. 2022: 354-
     355.
[24] Rawte V, Sheth A, Das A. A survey of hallucination in large foundation
     models[J]. arXiv preprint arXiv:2309.05922, 2023.
[25] Jiang C, Xu H, Dong M, et al. Hallucination augmented contrastive
     learning for multimodal large language model[C]//Proceedings of the
     IEEE/CVF Conference on Computer Vision and Pattern Recognition.
     2024: 27036-27046.
[26] Chen S, Li B. Toward Adaptive Reasoning in Large Language Mod-
     els with Thought Rollback[C]//Forty-first International Conference on
     Machine Learning.
[27] Xu K, Sun J, Hu Y, et al. MEIC: Re-thinking RTL Debug Automation
     using LLMs[J]. arXiv preprint arXiv:2405.06840, 2024.
[28] Feng S, Shi W, Wang Y, et al. Don’t Hallucinate, Abstain: Identifying
     LLM Knowledge Gaps via Multi-LLM Collaboration[J]. arXiv preprint
     arXiv:2402.00367, 2024.
