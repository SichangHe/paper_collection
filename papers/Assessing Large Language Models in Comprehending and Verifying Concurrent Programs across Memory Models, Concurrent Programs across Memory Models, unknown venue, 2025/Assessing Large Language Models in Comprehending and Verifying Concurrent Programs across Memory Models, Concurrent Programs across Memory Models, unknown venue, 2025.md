Assessing Large Language Models in Comprehending and Verifying
Concurrent Programs across Memory Models
RIDHI JAIN, IIIT-Delhi, India
RAHUL PURANDARE, University of Nebraska–Lincoln, USA
As concurrent programming becomes increasingly prevalent, effectively identifying and addressing concurrency issues such
as data races and deadlocks is critical. This study evaluates the performance of several leading large language models (LLMs),
including GPT-3.5-turbo, GPT-4, GPT-4o, GPT-4o-mini, and Mistral-AI’s Large2, in understanding and analyzing concurrency
issues within software programs. Given that relaxed memory models, such as Total Store Order (TSO) and Partial Store Order
(PSO), are widely implemented and adapted in modern systems—supported even by commodity architectures like ARM and
x86—our evaluation focuses not only on sequentially consistent memory models but also on these relaxed memory models.
Specifically, we assess two main aspects: the models’ capacity to detect concurrency problems under a sequentially consistent
memory model and their ability to verify the correctness conditions of concurrent programs across both sequentially consistent
and relaxed memory models. To do this, we leverage SV-COMP’s pthread tests and 25 ARM Litmus tests designed to evaluate
Total Store Order (TSO) and Partial Store Order (PSO) memory models.
   The experimental results reveal that GPT-4, GPT-4o, and Mistral-AI’s Large2 demonstrate a robust understanding of
concurrency issues, effectively identifying data races and deadlocks when assessed under a sequentially consistent memory
model. However, despite its superior performance, all selected LLMs face significant challenges verifying program correctness
under relaxed memory models. These LLMs exhibit limitations in accurately capturing memory ordering constraints, and
their current capabilities fall short in verifying even small programs in these complex scenarios. This study highlights the
gap in LLMs’ effectiveness for relaxed memory models and emphasizes the need for further advancements to improve their
reliability in concurrent program analysis and verification.
CCS Concepts: • Software and its engineering → Empirical software validation.
Additional Key Words and Phrases: Large Language Models, Concurrency, Relaxed Memory Models

1   Introduction
As modern software systems grow increasingly complex and hardware evolves to feature multi-core processors,
the ability to run multiple threads or processes concurrently has become essential. This shift toward concurrency
is driven by the need to maximize performance and optimize resource utilization. However, along with these
benefits comes significant challenges: ensuring that concurrent programs operate correctly. Issues like race
conditions, deadlocks, and synchronization errors can lead to unpredictable behavior and critical failures in
software systems. These complexities make verifying and testing concurrent programs one of the most difficult
tasks in software development. These issues are further compounded by the intricacies introduced by relaxed
memory models, which define how operations on shared memory (reads and writes) are ordered and observed by
different threads or processors in a concurrent system.
    Traditional software engineering techniques like static and dynamic analysis have long been employed to detect
bugs, optimize performance, and verify program correctness. Static analysis examines code without executing
it, identifying issues such as memory leaks or null pointer dereferences by analyzing control flow, data flow,
and structure. These techniques rely on predefined rules and heuristics, often tailored to specific programming
environments. In contrast, dynamic analysis monitors a program during execution to catch runtime issues like
race conditions and deadlocks that static analysis might miss. While both methods are effective, they typically
demand extensive domain knowledge and significant computational resources, particularly when applied to large
or complex codebases. Running static analysis on massive projects or conducting dynamic analysis on intricate
systems can be computationally expensive, often resulting in long processing times. Moreover, their reliance on
predefined rules makes them less adaptable to rapidly evolving software environments, limiting their flexibility
in modern, agile development contexts.
    Deep learning techniques are increasingly adopted in software engineering and testing to address these
challenges. By leveraging models such as recurrent neural networks (RNNs) [32, 65], convolutional neural
networks (CNNs) [95, 99], and graph neural networks (GNNs) [18, 23, 109], deep learning has enabled the
automation of tasks like bug detection, code optimization [6, 26, 36], and code generation [54, 83]. These models
excel at identifying patterns within large codebases and can detect subtle issues that traditional tools may overlook.
Authors’ Contact Information: Ridhi Jain, IIIT-Delhi, India, ridhij@iiitd.ac.in; Rahul Purandare, University of Nebraska–Lincoln, USA,
rahul@unl.edu.


                                                                              , Vol. 1, No. 1, Article . Publication date: September 2025.
2                                                                                              R. Jain and R. Purandare


However, the application of deep learning to concurrent programming is still evolving, as the unique intricacies
of concurrency require specialized datasets and architectures.
   Recent breakthroughs in natural language processing (NLP), particularly through transformer-based large
language models (LLMs) such as GPT-4, have demonstrated unprecedented capabilities in understanding and
generating code. These models excel in various programming-related tasks, including code completion [22, 31,
61, 92], bug detection [59, 66], and automated code repair [3, 13, 41, 46, 48] by leveraging vast training data and
sophisticated neural network architectures. However, LLM-generated code can also introduce vulnerabilities
due to their reliance on probabilistic patterns and potential exposure to insecure or flawed examples during
training [75]. Given their success and limitations in these areas, it is imperative to explore the potential of LLMs
in verifying concurrent programs.
   LLMs have transformed software development by offering human-like code understanding and generation.
Trained on vast code and natural language datasets, these models can translate high-level descriptions into
functional code, detect vulnerabilities, and aid debugging. They are particularly promising for concurrent pro-
gramming, potentially identifying complex synchronization issues that rule-based tools often miss. By bridging
human intent and machine execution, LLMs have become invaluable for writing and analyzing code.
   Despite their strengths in code completion, bug detection, and automated generation, LLMs’ capabilities in veri-
fying concurrent programs remain underexplored. Given the complexity of concurrency issues—such as managing
shared resources, synchronization primitives, and subtle bugs under relaxed memory models—evaluating how
well LLMs can assist in verifying these programs is crucial. Although LLMs produce syntactically correct code,
they may generate logically flawed or unsafe code [64], a concern that is magnified in concurrent programming
due to the intricate nature of potential errors.
   While there have been significant advancements in concurrency analysis tools [28, 45, 72], including static
analyzers, model checkers [1, 35, 53], and dynamic testing frameworks, these tools typically require intricate
knowledge of the underlying memory models. They can be limited in their ability to scale to large, real-world
software systems. Moreover, they may not generalize well to novel concurrency patterns or emerging program-
ming paradigms. LLMs, such as GPT-4 and its successors, have demonstrated remarkable natural language
understanding, code generation [5, 44], and general pattern recognition capabilities. These models have been
trained on vast amounts of textual and code data, enabling them to perform tasks ranging from code completion
to bug detection. However, their potential in understanding and analyzing concurrent programs, especially under
relaxed memory models, remains an open question.
   As hardware systems increasingly adopt relaxed memory models to boost performance and efficiency, the need
for effective verification tools has become more urgent. Understanding these models is crucial to avoid subtle bugs,
such as race conditions, which can lead to unpredictable behavior, data corruption, or security vulnerabilities.
Additionally, because various architectures implement different memory models, developers must understand the
specifics of each model to write efficient and reliable code.
   LLMs have shown impressive general-purpose reasoning abilities [17, 60], but their proficiency in specialized
and complex domains, such as concurrent programs under relaxed memory models (e.g., Total Store Order
(TSO) and Partial Store Order (PSO)), remains largely untested. Assessing their reasoning capacity in these
specific technical areas presents significant challenges. Unlike traditional program analysis tools, designed with
a deep understanding of computational rules, LLMs lack a built-in conceptual framework for handling the
low-level details of memory consistency, thread interactions, and synchronization mechanisms. This gap can
lead to difficulties in accurately predicting or explaining complex behaviors in concurrent programs, making it
challenging for LLMs to offer reliable guidance on memory model-related issues. Furthermore, the probabilistic
nature of LLMs may produce outputs that sound plausible but are technically incorrect when dealing with the
stringent and precise requirements of memory models in software development.
   This paper seeks to explore the capabilities of LLMs in detecting concurrency issues within programs, with a
particular focus on how well they handle the complexities introduced by relaxed memory models. Specifically,
we investigate the performance of LLMs in reasoning about TSO and PSO, two widely studied relaxed memory
models critical for understanding modern concurrency. These models are chosen because TSO allows for some
instruction reordering while maintaining a relatively strong consistency guarantee, and PSO introduces further
flexibility by permitting even more relaxed ordering of store operations. By analyzing these two models, we aim
to answer three primary research questions through experiments and case studies.

     • RQ1: How accurately can LLMs understand and summarize concurrent programs† ?

, Vol. 1, No. 1, Article . Publication date: September 2025.
Assessing Large Language Models in Comprehending and Verifying Concurrent Programs across Memory Models                                      3


      • RQ2: How can LLMs effectively identify common concurrency issues such as race conditions, deadlocks,
        and synchronization errors in concurrent programs?
      • RQ3: How do LLMs compare to traditional static and dynamic analysis tools in verifying concurrent
        programs in terms of both accuracy and efficiency?
      • RQ4: Can LLMs predict correct program behaviors under relaxed memory models?
   By investigating these research questions, we aim to provide a comprehensive evaluation of the capabilities of
LLMs in the context of concurrent programming. Understanding these aspects is crucial for integrating LLMs
into software development workflows, potentially enhancing tools for debugging and verifying concurrent code.
The findings of this study could pave the way for more advanced and efficient tools for verifying concurrent
programs, ultimately contributing to the development of more reliable and robust software systems.
   The main contributions of this paper are as follows.
    (1) Prompt-Based Evaluation: The paper introduces a set of targeted prompts designed to assess LLMs on their
        understanding of concurrency issues in programs. These prompts focus on various aspects of concurrent
        programming, such as thread management and synchronization.
    (2) Performance Insights: The paper provides a detailed analysis of LLM performance in understanding and sum-
        marizing concurrency-related problems by applying these prompts. This analysis highlights the strengths
        and limitations of LLMs in this context.
    (3) Benchmarking LLMs: The study sets benchmarks for evaluating LLMs based on their prompt responses. This
        approach facilitates a structured assessment of LLM capabilities and provides a basis for future evaluations.
Overall, the paper advances the understanding of LLMs in concurrent program analysis by evaluating their
performance through specific questions, aiming to enhance the integration of LLMs into software development
practices. To promote transparency and facilitate further research, the artifacts associated with this work, including
the experimental datasets, code samples, and LLM responses, are publicly available at https://anonymous.4open.
science/r/LLM-Conc-RMM-13F8.
   The structure of this paper is as follows: Section 2 provides an overview of prior research and related work.
Section 3 details our approach to evaluating the LLMs. The experimental setup and results are presented in
Section 4, which also addresses the research questions posed in Section 1. Section 5 discusses the findings, while
Section 6 explores potential future directions and opportunities. Finally, Section 7 summarizes and concludes this
work.

2     Related Work
The field of concurrency analysis and verification has evolved over the years, with various methodologies being
applied to identify and address the challenges of analyzing multi-threaded programs. This section reviews the
most relevant related work.

2.1    Traditional Verification Tools
Traditional verification tools, including both static [10, 15, 35, 49, 102] and dynamic analysis [7, 45, 52, 68, 85],
have long been employed to identify concurrency issues in concurrent programs. Static analysis tools analyze
code without executing it, relying on heuristics and symbolic execution to detect potential issues such as race
conditions and deadlocks [11, 24]. These tools are often highly effective in finding certain errors, but they can
struggle with complex, dynamic interactions in concurrent programs. They may produce many false positives [47],
where potential issues are flagged but would not occur in actual execution, and false negatives [25], where subtle
concurrency bugs go undetected [51].
   In contrast, dynamic analysis tools monitor the execution of a program to detect concurrency issues in real
time [37, 90, 105]. These tools typically have a lower false-positive rate in detecting real-world concurrency
problems since they observe the actual execution behavior. However, their effectiveness is limited by the coverage
of the test cases used during execution [90]. Dynamic analysis can be computationally expensive and may
introduce significant overhead, slowing program execution. Moreover, such tools might miss issues manifest
only under specific conditions or rarely encountered inputs. The balance between accuracy and efficiency and
the challenge of minimizing false positives and negatives highlights the complexity and limitations inherent in
traditional verification approaches for concurrent programs.

0 † Unless explicitly stated, concurrent programs refer to concurrent programs under a sequentially consistent memory model in this paper.



                                                                                   , Vol. 1, No. 1, Article . Publication date: September 2025.
4                                                                                                R. Jain and R. Purandare


2.2    Deep Learning for Code Analysis
Deep learning (DL) models, particularly those trained on large-scale code repositories, have shown significant
potential in capturing intricate patterns and semantics within code, enabling advanced tasks such as code
completion [43, 87], bug detection, and vulnerability identification. Integrating these techniques into code
analysis has facilitated the development of more sophisticated models that can learn from vast amounts of data,
especially from open-source software (OSS) communities.
   Traditional code analysis techniques often rely on rule-based systems [27, 39] or symbolic reasoning [12, 16, 80],
which may struggle with the complexity and variability of real-world code. In contrast, deep learning models,
particularly those based on neural networks, have demonstrated the ability to learn patterns and representations
from large code data [19, 40]. With increasing accuracy, these models can be trained to perform tasks such as
code completion, bug detection [58, 78], and vulnerability identification [18, 97]. Recent developments in neural
code representation, such as Graph Neural Networks (GNNs) and Transformer-based architectures, have further
enhanced the capability to capture the intricate dependencies and control flows in code [23, 55, 113]. These
methods have shown to be useful in identifying data races [89, 112], deadlocks [38], and other concurrency-related
issues [79]. However, while deep learning models have succeeded in various code analysis tasks, their performance
in handling concurrency, especially under relaxed memory models, remains challenging. This gap underscores the
need for further research, particularly in the context of LLMs, which have begun to show potential in analyzing
and summarizing concurrent code. Integrating deep learning techniques with LLMs presents a promising direction
for advancing the state of the art in concurrent code analysis.

2.3    Large Language Models in Code Analysis
The rapid advancements in LLMs have enabled their application across various domains, including code-related
tasks [44, 71]. These models have shown promising results in enhancing programming error messages, making
them more interpretable and actionable for novice programmers [56]. One of the key areas where LLMs have been
employed is content analysis( [69]. LLMs have also shown to enhance the decompilation process by translating
binary code into high-level representations [42, 88]. Leveraging their training on both source code and binaries,
they can improve decompilers by providing insights. As these models become increasingly integrated into
technical systems, it is crucial to understand their limitations and potential pitfalls, particularly in the context of
code content analysis.
   LLMs are trained on vast source code and natural language datasets, enabling them to identify patterns indicative
of bugs [46, 57], such as common coding errors, logical inconsistencies [86, 111], or security vulnerabilities [4, 34].
In bug detection, LLMs can analyze code snippets to predict potential issues [29, 107] [30], often providing
explanations or suggestions for correction. LLMs can automatically generate patches for bug repair by rewriting
faulty code or proposing changes that align with best practices [77, 100] [13, 48, 98, 104]. However, patches
generated by LLMs may not always be trustworthy [33, 62, 63, 76, 91].
   Recent research suggests LLMs can enhance various stages of the testing lifecycle [50, 96]. They automate
test case generation from natural language requirements and code specifications, reducing manual effort and
improving test coverage. In CI/CD pipelines, LLMs generate and update test scripts, ensuring alignment with
ongoing code [110]. They also contribute to code coverage analysis by identifying untested regions and suggesting
targeted tests, while in bug detection and repair, they identify programming errors and propose fixes. LLMs
enhance automated code reviews by enforcing coding standards and identifying issues pre-integration, and they
prioritize regression testing based on recent code changes. Furthermore, LLMs are used in fuzzing [73, 103, 108],
where they generate diverse and unexpected input data to uncover edge cases and vulnerabilities, expanding the
scope of traditional testing methods.
   LLMs can be integrated with static analysis tools to assist in the automated program verification [20, 101], bug
detection and repair [8, 46]. These tools leverage the LLMs’ ability to understand and generate code to suggest
fixes for concurrency-related bugs or to verify the correctness of synchronization mechanisms. However, while
LLMs show promise in catching common and well-understood bugs, they still face challenges in addressing
complex, domain-specific issues or understanding the full context of the software [93].

2.4    Gaps and Challenges
Despite the rapid advancements in LLMs for code analysis, applying these models to concurrent programs remains
under-explored [21, 67, 70, 81, 94]. While LLMs have shown proficiency in various programming tasks, such as

, Vol. 1, No. 1, Article . Publication date: September 2025.
Assessing Large Language Models in Comprehending and Verifying Concurrent Programs across Memory Models                                                                       5



           Q: How do relaxed memory models such as total store order
                                                                                                                                     Responses
                   and partal store order affect the following
                        program's behaviourbehaviour?

           Q: Can you identify a potential datarace or race condition in
                             the following program?

             Q: Can you summarize what the following program
                                     does?
              Q: Does the assert condition always hold in the
                                                                                        C/C++
            following program or can there be a case where the
                                assertion fails?
          Q: Can you identify a potential deadlock in the following
                                   program?
                                                                                      Source Code
                          Questions
                                                                                                                                     Inspection &
                                                        Prompt                                                    LLMs                                       Results
                                                                                                                                      Evaluation


                                                                                 Fig. 1. An overview of our approach.

    Feature                          GPT-4o                                GPT-4                    GPT-3.5-turbo              GPT-40-mini               Mistral-Large2
    Initial     Release              May 13, 2024                          March 14, 2023           Nov, 2022                  July 24, 2024             July 24, 2024
    Date
    Modality  2                      Text and Images                       Text and Images          Text and Images            Text and Images           Text and Images
    Output Tokens2                   4096                                  8192                     4096                       16384                     8192
    Parameters [14, 82,              70B1                                  1.8T3                    175B                       8B                        123B
    106]
    Cost per 1M to-                  Input: $5                             Input: $30               Input: $3                  Input: $0.15              Input: $3
    ken [74, 84]
                                     Output: $15                           Output: $60              Output: $6                 Output: $0.6              Output: $9
    Context    win-                  128k                                  8192                     16385                      128k                      128k
    dow4 [106]
    Trained on Data                  Oct’ 23                               Sept’ 21                 Sept’ 21                   Oct’ 23                   Unknown
    Until
                                                                  Table 1. Details of the LLMs selected for the assessment.



code generation, bug detection, and refactoring, their ability to understand and analyze concurrency—a critical
aspect of modern software—has not been extensively studied. Concurrent programs introduce complexities such
as thread interactions, synchronization issues, and race conditions, which are challenging for even the most
advanced models to interpret and reason about accurately. Moreover, the situation becomes even more intricate
when considering relaxed memory models, like TSO and PSO, where traditional assumptions about memory
consistency do not hold. These models allow for non-intuitive instruction reordering, making the correct program
behavior analysis particularly difficult. The lack of research in this area highlights a significant gap in the current
capabilities of LLMs, underscoring the need for further investigation into how these models can be adapted or
enhanced to effectively handle the unique challenges posed by concurrent programming under relaxed memory
models.

3      Methodology
This section outlines the approach used to evaluate the capabilities of LLMs in verifying concurrent programs
under relaxed memory models. Our approach is divided into several phases, as shown in Figure 1, to assess these
capabilities systematically, each focusing on a critical aspect of the analysis process.

3.1      Program Selection
In this study, we aim to assess the comprehension of LLMs in analyzing concurrent programs under Sequential
Consistency (SC) as well as two widely studied relaxed memory models: Total Store Order (TSO) and Partial Store
Order (PSO). SC is the most intuitive memory model where operations from all threads are executed in a global
order that respects program order within each thread. TSO is a relaxed memory model that allows the reordering
of load instructions before store instructions, as long as these events are independent. On the other hand, PSO
further relaxes by allowing both loads and stores to be reordered. Unlike TSO, which ensures that stores are
1 https://docs.google.com/spreadsheets/d/1kc262HZSMAWI6FVsh0zJwbB-ooYvzhCHaHcNUiA0_hY
2 https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4
3 https://explodingtopics.com/blog/gpt-parameters
3 https://platform.openai.com/docs/models/gpt-4o



                                                                                                                    , Vol. 1, No. 1, Article . Publication date: September 2025.
6                                                                                                    R. Jain and R. Purandare

                                                                                                                 o
    Program Comprehension                    Q1. Can you summarize what the following program does?                   RQ1
    Concurrency Issues                       Q2. Can you identify a potential data race in the following pro-     
                                                                                                                  
                                                                                                                  
      Identification
                                                                                                                  
                                                                                                                  
                                                 gram?                                                                RQ2
                                             Q3. Can you identify a potential deadlock in the following pro-      
                                                                                                                  
                                                                                                                  
                                                 gram?                                                            
                                                                                                                 o
    Verification under SC                    Q4. Does the assert condition always hold in the following pro-          RQ3
                                                 gram or can there be a case where the assertion fails?
                                                                                                                 o
    Verification under RMM                   Q5. How do relaxed memory models such as total and partial store         RQ4
                                                 orders affect the following program’s behavior?

                                                 Table 2. Grouped Evaluation Questions



propagated in the order they appear within a thread, PSO allows independent stores to be propagated out of
order. This introduces additional flexibility and potential performance gains but also increases the complexity
of reasoning about memory behavior. By examining LLM performance across SC, TSO, and PSO, we aim to
understand how these models can reason about complex memory interactions and identify concurrency issues
under different memory model constraints.
   LLMs may operate better within limited context windows and token sizes (and the concurrent programs are
already complex), so we carefully select small concurrent programs for our experiments. We use the pthread
benchmarks from the SV-COMP dataset to evaluate concurrency under SC, with code lengths ranging from 39 to
172 lines. We utilize specially designed litmus tests ranging from 38 to 74 lines of code to capture the behavior
under these specific memory models for TSO and PSO.

3.2    Prompt Creation
Appropriate prompts must be passed to the LLM to generate relevant results. Thus, we carefully craft questions
that are passed along with the code to the LLM. These prompts are listed in Table 2. We categorize these prompts
into four categories:
    (1) Program Comprehension: LLMs show promise in LLMs show promise in understanding and summarizing
        code. The prompts in this category are designed to assess the LLM’s ability to understand the functionality
        and intent of the program. These questions ask the LLM to describe the purpose of the code, explain
        how the threads interact, and identify key variables and operations. By evaluating how well the LLMs
        can comprehend multi-threaded programs, we aim to gauge their general understanding of concurrency
        constructs like threads, atomic operations, and synchronization mechanisms.
    (2) Concurrency Issues Identification: One of the primary objectives is to assess whether LLMs can
        correctly identify concurrency-related issues such as data races, deadlocks, and race conditions. LLMs
        can parse intricate code structures, identify parallelism, and understand synchronization constructs like
        mutexes, semaphores, and atomic operations by leveraging extensive training on diverse codebases. The
        prompts in this category focus on asking the LLM to pinpoint areas in the code where these issues might
        arise. For instance, questions may prompt the LLM to check for shared variable accesses without proper
        synchronization or potential deadlock situations due to improper locking mechanisms. This category aims
        to evaluate the LLM’s ability to detect concurrency bugs in both simple and complex scenarios.
    (3) Verification under Sequential Consistency (SC): Sequential consistency is a simpler and more intuitive
        memory model where operations across threads are executed globally. In this category, the prompts evaluate
        whether the LLM can verify program behavior under SC, where issues such as data races may still arise
        despite the memory model’s simplicity. These prompts ask the LLM to reason about thread execution order
        and whether assertions or invariants in the code can be violated. This category is essential for benchmarking
        LLMs’ performance under the most straightforward concurrency scenarios.
    (4) Verification under Relaxed Memory Models (RMM): Relaxed memory models such as TSO and PSO
        introduce complexity in concurrent program behavior, as instructions can be reordered, potentially leading
        to unexpected outcomes. The prompts in this category are designed to test the LLM’s understanding of

, Vol. 1, No. 1, Article . Publication date: September 2025.
Assessing Large Language Models in Comprehending and Verifying Concurrent Programs across Memory Models                            7


       program behavior under such memory models. For example, questions may ask the LLM whether the
       assertion in a program will always hold under TSO or PSO or if the reordering of instructions might lead
       to subtle bugs. This set of prompts helps us assess the LLMs’ capability to reason about non-intuitive
       behaviors introduced by relaxed memory models.

3.3    Prompting LLMs
The selection of LLMs for this study was driven by the need to evaluate models with diverse capabilities in
understanding and reasoning about concurrent programs. We chose a range of state-of-the-art models, including
GPT-4, GPT-3.5-turbo, GPT-4o, GPT-4o-mini, and Mistral-AI’s Large2, for their varying architectural strengths,
token handling capacities, and performance across natural language processing tasks, as shown in Table 1.
These models represent different levels of reasoning complexity and context comprehension, which is critical for
assessing how well they can handle the intricacies of concurrency and memory models.
  Effective interaction with LLMs requires carefully crafted prompts that elicit relevant and precise responses.
Given the intricacies of concurrency and memory model behavior, we designed targeted prompts that guide
the LLMs toward identifying key aspects of the programs. Each LLM was given a task framed as a question or
instruction. Since LLMs can produce verbose output, we designed prompts encouraging focused and succinct
responses.

3.4    Manual Inspection
LLMs often generate verbose responses with portions that may be correct, incorrect, or irrelevant to the task, so
a thorough manual examination of each output is essential. After prompting the LLMs, we carefully reviewed
every response to assess its factual accuracy, relevance to the question asked, and the level of detail provided.
   During this manual labeling process, special attention is paid to whether the LLMs correctly handle more subtle
issues, such as race conditions or memory reordering under TSO and PSO models. We also consider whether the
responses provide feasible error traces or if the LLMs merely speculate about potential issues without justifying
their conclusions.
   Once categorized, the responses are labeled accordingly, with correct information highlighted as useful and
reliable, while incorrect or irrelevant segments are flagged for further analysis. This systematic evaluation ensures
a comprehensive understanding of each LLM’s ability to handle complex concurrency scenarios, enabling us to
identify areas where the models excel or struggle.

4     Evaluation
4.1    Experimental Setup and Objectives
We conducted a series of experiments using a well-defined setup to evaluate the capabilities of LLMs in verifying
concurrent programs. This section details the hardware and software environments, datasets used, and procedures
followed to ensure the reproducibility and robustness of our results. Our experiments were performed on an
Intel x86/64 Linux machine with Ubuntu 20.04, 32GB RAM, an Intel Core i7-4510U CPU with a clock speed of up
to 3.10GHz, and kernel version 5.14.0-1029-oem. Notably, these experiments were conducted using pre-trained
LLMs without any fine-tuning.

4.2    Dataset Description
The dataset combines 25 ARM Litmus tests [2] designed for relaxed memory models, specifically TSO and
PSO, with the pthread benchmarks from the Software Verification Competition (SV-COMP) [9]. The Litmus
tests examine behaviors such as message passing, store buffering, load buffering, read consistency, and write-
read ordering to identify and analyze potential anomalies in memory ordering and consistency under different
relaxed memory models. The pthread benchmarks cover a variety of concurrency scenarios, including simple
locking mechanisms, the producer-consumer problem, dining philosophers, reader-writer locks, and barrier
synchronization. These benchmarks evaluate multi-threaded programs’ correctness and safety properties using
pthreads. Together, these datasets provide comprehensive coverage for studying concurrency and memory
model behaviors, offering theoretical analysis through litmus tests and practical evaluation through pthread
benchmarks. Note that all selected tests contain information on our interest in concurrency issues. We consider
this information as ground truth. However, we strip these tests of any comments they contain to eliminate biases.

                                                                         , Vol. 1, No. 1, Article . Publication date: September 2025.
8                                                                                                                        R. Jain and R. Purandare

                                                    Mistral-AI
                                Ground Truth                          GPT-3.5-turbo     GPT-4o-mini               GPT-4                  GPT-4o
                                                     Large2
    Test                  LoC   Q2   Q3    Q4    Q2    Q3      Q4     Q2   Q3   Q4    Q2     Q3     Q4     Q2      Q3       Q4    Q2      Q3      Q4
    2.2W                  44    ✗    ✗     ✗     ✗      ✗      ✓      ✓    ✓    ✓     ✗      ✗      ✗      ✗       ✗        ✓     ✗       ✗       ✗
    CoWR                  41    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✗       ✗        ✓     ✗       ✗       ✗
    RWC+dmbs              54    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✓      ✗      ✗       ✗        ✗     ✗       ✗       ✗
    R+dmbs                43    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✓       ✗        ✓     ✓       ✗       ✗
    R                     44    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✓       ✗        ✓     ✓       ✗       ✓
    SB+dmbs               63    ✗    ✗     ✗     ✗      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✗       ✗        ✗     ✗       ✗       ✗
    SB                    58    ✗    ✗     ✗     ✗      ✗      ✓      ✓    ✓    ✓     ✓      ✓      ✓      ✗       ✓        ✓     ✓       ✗       ✗
    R+po+dmb              43    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✗      ✗      ✗      ✗       ✗        ✓     ✗       ✗       ✓
    R+dmb+po              47    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✓       ✗        ✓     ✓       ✗       ✗
    WRW+2W+dmbs           60    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✓       ✗        ✓     ✗       ✗       ✓
    RWC+dmb+po            53    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✗       ✗        ✓     ✗       ✗       ✗
    CoRR1                 40    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✗       ✗        ✗     ✗       ✗       ✓
    2+2W+reads            62    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✗      ✗      ✓      ✓       ✗        ✓     ✗       ✗       ✗
    2+2W+dmbs             39    ✗    ✗     ✗     ✗      ✗      ✓      ✓    ✓    ✓     ✗      ✗      ✓      ✗       ✗        ✓     ✗       ✗       ✗
    WRW+2W                59    ✗    ✗     ✗     ✗      ✗      ✓      ✓    ✓    ✓     ✗      ✗      ✓      ✓       ✗        ✓     ✗       ✗       ✗
    S+po+dmb              52    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✗      ✗      ✓      ✗       ✗        ✓     ✗       ✗       ✗
    CoRW                  38    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✗       ✗        ✓     ✗       ✗       ✗
    CoRR2                 74    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✓       ✗        ✓     ✗       ✗       ✗
    S+dmbs                53    ✗    ✗     ✗     ✗      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✗       ✗        ✓     ✓       ✗       ✓
    S                     52    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✓       ✗        ✓     ✗       ✗       ✗
    2+2W+dmbs+reads       63    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✓      ✓       ✗        ✓     ✗       ✗       ✗
    RWC                   57    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✗      ✗       ✗        ✓     ✗       ✗       ✗
    2+2W+dmbs+po          39    ✗    ✗     ✗     ✗      ✗      ✓      ✓    ✓    ✓     ✗      ✗      ✓      ✓       ✗        ✓     ✗       ✗       ✗
    SB+dmb+po             54    ✗    ✗     ✗     ✓      ✗      ✓      ✓    ✓    ✓     ✓      ✗      ✗      ✗       ✗        ✓     ✗       ✗       ✗
    WRW+2W+dmb+po         57    ✗    ✗     ✗     ✗      ✗      ✓      ✓    ✓    ✓     ✗      ✗      ✗      ✓       ✗        ✓     ✗       ✗       ✗
    True Positive (TP)                             0     0     0       0    0    0    0       0     0       0      0        0      0       0      0
    False Positive (FP)                           17     0     24     25   25   25    16      2     20     11      0        23     3       0      5
    True Negative (TN)                             8     25    1       0    0    0    9      23     5      14      25       3      22      25     20
    False Negative (FN)                            0     0     0       0    0    0    0       0     0       0      0        0      0       0      0
    Accuracy                                     0.32   1.00   0.04   0    0     0    0.36   0.92   0.20   0.56   1.00     0.12   0.88    1.00    0.80
Table 3. Comparison of different LLMs’ ability to detect concurrency issues in multithreaded programs from litmus tests.




4.3      Model Selection
Selecting an appropriate model is a critical step in evaluating the capabilities of lLLMs for verifying concurrent
programs. This study considers well-established LLMs such as Mistral-AI, GPT-3.5-turbo, and GPT-4, which are
known for their superior language understanding and generation capabilities. These models have demonstrated
state-of-the-art performance in various natural language processing tasks, making them prime candidates for our
investigation. Additionally, we will compare the performance of these models against smaller, more specialized
models to assess whether larger models’ increased complexity and resource demands translate into significantly
better performance.
   In this study, we have chosen a range of models, including GPT-3.5-turbo, GPT-4, GPT-4-o, GPT-4o-mini, and
Mistral Large-latest to cover a spectrum of capabilities, from advanced general-purpose language processing to
specialized tasks. GPT-3.5-turbo was selected for its efficiency and balance between performance and computa-
tional cost, making it ideal for scenarios where rapid prototyping and cost-effective solutions are needed. GPT-4,
known for its enhanced reasoning abilities and broader context handling, serves as our benchmark for complex
language understanding tasks. The GPT-4-o and GPT-4o-mini variants are included to explore trade-offs between
performance and model size, allowing us to evaluate the scalability and adaptability of the GPT-4 architecture.
Finally, Mistral’s Latest, a cutting-edge model known for its specialization in certain domains, is selected to assess
its ability to handle tasks that require domain-specific knowledge or enhanced generative capabilities.
   The temperature setting for all models was maintained at their respective default values. The temperature
parameter controls the randomness of the model’s output, with lower values resulting in more deterministic
responses and higher values producing more creative or diverse outputs. Using the default temperature settings
ensures a fair comparison across models, allowing each to operate within its optimal configuration for generating
coherent and contextually appropriate responses.

4.4      Prompt Creation
To address the research questions outlined in this paper, we developed multiple prompts specifically designed to
evaluate the capabilities of LLMs. These prompts were carefully crafted to assess various aspects of LLM perfor-
mance, including their ability to understand, summarize, and analyze concurrent programs. By systematically

, Vol. 1, No. 1, Article . Publication date: September 2025.
Assessing Large Language Models in Comprehending and Verifying Concurrent Programs across Memory Models                                       9

                                                         Mistral-AI
                                        Ground Truth                      GPT-3.5-turbo     GPT-4o-mini            GPT-4             GPT-4o
                                                          Large2
 Test                             LoC   Q2   Q3   Q4   Q2 Q3      Q4      Q2     Q3   Q4    Q2    Q3   Q4    Q2     Q3     Q4   Q2     Q3     Q4
 triangular-2                     53    ✗    ✗    ✓    ✓   ✗      ✓       ✓      ✗    ✓     ✓     ✓    ✗     ✓      ✗      ✓    ✓      ✓      ✗
 singletonwith-unint-problems-b   60    ✓    ✗    ✓    ✓   ✗      ✓       ✓      ✓    ✓     ✓     ✗    ✗     ✓      ✗      ✓    ✓      ✗      ✓
 stateful-01-1                    63    ✗    ✗    ✓    ✗   ✗       ✗      ✓      ✓    ✓     ✓     ✓    ✗     ✗      ✗      ✓    ✓      ✓      ✗
 stack-2                          131   ✗    ✗    ✓    ✓   ✓      ✓       ✓      ✓    ✓     ✓     ✗    ✗     ✗      ✗      ✓    ✓      ✓      ✓
 triangular-longest-2             53    ✗    ✗    ✓    ✓   ✗      ✓       ✓      ✓    ✓     ✓     ✓    ✓     ✗      ✗      ✓    ✓      ✓      ✓
 bigshot-s                        40    ✗    ✗    ✗    ✗   ✗       ✗      ✓      ✓    ✓     ✓     ✗    ✗     ✓      ✗      ✗    ✓      ✗      ✗
 stack-longer-1                   127   ✗    ✗    ✓    ✓   ✓      ✓       ✓      ✓    ✓     ✓     ✓    ✓     ✓      ✗      !    ✓      ✓      ✓
 two-stage-3                      131   ✗    ✗    ✓    ✗   ✗      ✓       ✓      ✓    ✓     ✓     ✓    ✗     ✓      ✗      ✓    ✓      ✓      ✓
 stateful-01-2                    63    ✗    ✗    ✗    ✗   ✗       ✗      ✓      ✓    ✓     ✓     ✓    ✗     ✗      ✗      ✗    ✓      ✓      ✗
 sync-01                          71    ✗    ✗    ✗    ✗   ✓      ✓       ✓      ✓    ✓     ✓     ✗    ✓     ✗      ✗      ✗    ✓      ✗      ✗
 reorder-5                        84    ✓    ✗    ✗    ✓   ✗      ✓       ✓      ✓    ✓     ✓     ✗    ✓     ✓      ✗      ✓    ✓      ✗      ✓
 bigshot-s2                       40    ✗    ✗    ✗    ✗   ✗       ✗      ✓      ✓    ✓     ✓     ✗    ✗     ✗      ✗      ✓    ✓      ✗      ✓
 reorder-2                        86    ✓    ✗    ✓    ✓   ✗      ✓       ✓      ✗    ✓     ✓     ✗    ✓     ✓      ✗      ✓    ✓      ✗      ✗
 indexer                          87    ✗    ✗    ✗    ✗   ✓       ✗      ✓      ✓    ✓     ✓     ✓    ✗     ✓      ✓      ✗    ✓      ✓      ✗
 queue-ok-longer                  156   ✗    ✗    ✗    ✗   ✓      ✓       ✓      ✓    ✓     ✓     ✓    ✓     ✗      ✗      ✓    ✓      ✓      ✓
 bigshot-p                        39    ✓    ✗    ✓    ✓   ✗      ✓       ✓      ✓    ✓     ✓     ✗    ✓     ✓      ✗      ✓    ✓      ✓      ✓
 stack-1                          128   ✗    ✗    ✓    ✓   ✗       ✗      ✓      ✓    ✓     ✓     ✓    ✓     ✗      ✗      ✗    ✓      ✓      ✓
 queue-longer                     170   ✗    ✗    ✓    ✓   ✓      ✓       ✓      ✓    ✓     ✓     ✓    ✓     ✗      ✗      ✓    ✓      ✓      ✓
 triangular-longer-1              52    ✗    ✗    ✗    ✓   ✗       ✗      ✓      ✓    ✓     ✓     ✗    ✓     ✗      ✗      ✓    ✓      ✗      ✓
 queue-ok                         156   ✗    ✗    ✗    ✗   ✓      ✓       ✓      ✓    ✓     ✓     ✓    ✓     ✗      ✗      ✓    ✓      ✓      ✓
 triangular-longer-2              52    ✗    ✗    ✓    ✓   ✗      ✓       ✓      ✓    ✓     ✓     ✗    ✓     ✗      ✗      ✓    ✓      ✗      ✓
 queue-ok-longest                 155   ✗    ✗    ✗    ✗   ✓      ✓       ✓      ✓    ✓     ✓     ✓    ✓     ✗      ✗      ✓    ✓      ✗      ✓
 triangular-longest-1             53    ✗    ✗    ✗    ✗   ✗      ✓       ✓      ✓    ✓     ✓     ✓    ✗     ✗      ✗      ✓    ✓      ✓      ✗
 sigma                            55    ✓    ✗    ✓    ✓   ✗      ✓       ✓      ✓    ✓     ✓     ✗    ✓     ✓      ✗      ✓    ✓      ✓      ✗
 singletonwith-unint-problems     66    ✓    ✗    ✓    ✓   ✗      ✓       ✓      ✓    ✓     ✓     ✓    ✗     ✓      ✗      ✓    ✓      ✗      ✗
 singleton                        66    ✓    ✗    ✓    ✓   ✗      ✓       ✓      ✓    ✓     ✓     ✗    ✓     ✓      ✗      ✓    ✓      ✗      ✓
 singleton-b                      60    ✓    ✗    ✓    ✓   ✗      ✓       ✓      ✓    ✓     ✓     ✗    ✓     ✗      ✗      ✓    ✓      ✗      ✓
 stack-longest-2                  128   ✗    ✗    ✗    ✓   LL     ✓       ✓      ✓    ✓     ✓     ✓    ✓     ✗      ✗      ✗    ✓      ✓      ✓
 queue                            172   ✗    ✗    ✓    ✓   ✓      ✓       ✓      ✓    ✓     ✓     ✓    ✓     ✗      ✓      ✓    ✓      ✓      ✓
 lazy-01                          56    ✗    ✗    ✓    ✗   ✗      ✓       ✓      ✓    ✓     ✓     ✓    ✓     ✗      ✗      ✓    ✓      ✓      ✓
 stack-longest-1                  129   ✗    ✗    ✓    ✓   ✓      ✓       ✓      ✓    ✓     ✓     ✓    ✓     ✓      ✗      ✓    ✓      ✓      ✓
 triangular                       52    ✗    ✗    ✗    ✓   ✗      ✓       ✓      ✓    ✓     ✓     ✗    ✓     ✗      ✗      ✓    ✓      ✗      ✓
 stack-longer-2                   127   ✗    ✗    ✗    ✗   LL      ✗      ✓      ✓    ✓     ✓     ✗    ✗     ✗      ✗      ✗    ✓      ✗      ✗
 queue-longest                    170   ✗    ✗    ✓    ✓   ✓      ✓       ✓      ✓    ✓     ✓     ✓    ✓     ✓      ✗      ✓    ✓      ✓      ✓
 True Positive (TP)                                    8    0      18     7      0    20    8     0    14    7      0      18   8       0     15
 False Positive (FP)                                   13   13      8     27     32   14    26    19   8     7      2      8    26     20     8
 True Negative (TN)                                    13   21      6     0      2    0     0     15   6     19     32     6    0      14     6
 False Negative (FN)                                   0    0       2     0      0    0     0     0    6     1      0      2    0       0     5
 Precision                                             0.38 0      0.69   0.21   0    0.59 0.24 0      0.64 0.50     0     0.69 0.24   0      0.65
 Recall                                                1.00 0      0.90   1.00   0    1.00 1.00 0      0.70 0.88     0     0.90 1.00   0      0.75
 Accuracy                                              0.62 0.62   0.71   0.21 0.06   0.59 0.24 0.44 0.59 0.76 0.94        0.71 0.24 0.41     0.62
 F1-Score                                              0.55 0      0.78   0.34 0      0.74 0.38 0    0.67 0.64   0         0.78 0.38 0        0.70
   Table 4. Comparison of different LLMs in their ability to detect concurrency issues in multithreaded programs from
SV-COMP. LL: Livelock. !: Code has assert, but LLM does not detect it. We consider LL as ✓ and ! as ✗ while computing TP,
                                                     FP, TN and TN.




applying these prompts, we aim to gain insights into the strengths and limitations of LLMs in handling the
complexities of concurrency, enabling a thorough examination of their effectiveness in this domain.
  Table 2 provides a comprehensive listing of all the prompts specifically designed for querying different memory
models. In the analysis process, these prompts are systematically appended to the code being examined before
being submitted to the LLM for processing. The generated responses from the LLMs are then meticulously
reviewed through manual examination. Our detailed findings, based on this rigorous evaluation, are presented
and discussed in the subsequent subsections.

4.5   Structure of the Tables
The experimental results are presented in Tables 3,4, and5. Each table’s first column lists the name of the test
program, providing a reference point for the specific concurrency scenario being evaluated. The second column
in Tables 3 and 4 indicates the number of lines of code (LoC) in each test program, offering insight into the
complexity of the code analyzed.
   The column titled Ground Truth presents the actual, verified results for each question, serving as a benchmark
against which the performance of various LLMs is measured. Following this, the columns labeled Mistral-AI,
GPT-3.5-turbo, GPT-4o-mini, GPT-4, and GPT-4o display the results generated by each respective LLM in response
to the specific questions posed.

                                                                                  , Vol. 1, No. 1, Article . Publication date: September 2025.
10                                                                                                                 R. Jain and R. Purandare

                                                     Mistral-AI
                                  Ground Truth                     GPT-3.5-turbo   GPT-4o-mini          GPT-4            GPT-4o
                                                       Large2
           Test                         Q5          Q5    Reason   Q5     Reason   Q5     Reason   Q5     Reason    Q5      Reason
           2.2W                         ✓           ✗        ✗     ✓        ✗      ✓        ✗      ✓        ◦       ✗         ✗
           CoWR                         ✗           ✗        ✓     ✓        ✗      ✗        ✗      ✗        ✓       ✓         ✗
           RWC+dmbs                     ✗           ✗        ✓     ✓        ✗      ✓        ✓      ✗        ✓       ✓         ✗
           R+dmbs                       ✗           ✗        ✓     ✓        ✗      ✓        ✗      ✗        ✓       ✗         ✓
           R                            ✓           ✗        ✗     ✓        ✗      ✓        ✗      ✓        ✗       ✓         ✗
           SB+dmbs                      ✗           ✗        ✓     ✓        ✗      ✓        ✗      ✓        ✓       ✓         ✗
           SB                           ✓           ✗        ✗     ✓        ✓      ✓        ✗      ✓        ◦       ✓         ✗
           R+po+dmb                     ✓           ✗        ✗      -       ✗      ✓        ✗      ✓        ✗       ✗         ✗
           R+dmb+po                     ✓           ✗        ✗      -       ✗      ✓        ✗      ✓        ✗       ✓         ✗
           WRW+2W+dmbs                  ✗           ✗        ✓     ✓        ✗      ✓        ✗      ✗        ✗       ✓         ✗
           RWC+dmb+po                   ✓           ✗        ✗     ✓        ✗      ✓        ✗      ✓        ✗       ✓         ✗
           CoRR1                        ✗           ✗        ✓     ✗        ✗      ✗        ✗      ✓        ✗       ✗         ✓
           2+2W+reads                   ✓           ✗        ✗      -       ✗      ✓        ✗      ✓        ✓       ✓         ✗
           2+2W+dmbs                    ✗           ✗        ✓     ✓        ✗      ✓        ✗      ✓        ✗       ✓         ✗
           WRW+2W                       ✓           ✗        ✗     ✓        ◦      ✓        ✗      ✓        ✗       ✗         ✗
           S+po+dmb                     ✓           ✗        ✗     ✓        ✗      ✓        ✗      ✓        ✗       ✓         ◦
           CoRW                         ✗           ✗        ✓     ✓        ✗      ✗        ✗      ✓        ✗       ✓         ✗
           CoRR2                        ✗           ✗        ✓      -       ✗      ✓        ✗      ✓        ✗       ✓         ✗
           S+dmbs                       ✗           ✓        ✗      -       ✗      ✓        ✗      ✓        ✗       ✗         ✓
           S                            ✓           ✓        ✗     ✓        ✗      ✓        ✗      ✓        ✗       ✓         ✗
           2+2W+dmbs+reads              ✗           ✓        ✗      -       ✗      ✓        ✗      ✗        ✓       ✗         ✓
           ✓RWC                         ✓           ✗        ✗     ✓        ✗      ✓        ✗      ✓        ✗       ✓         ✗
           2+2W+dmbs+po                 ✓           ✗        ✗      -       ✗      ✗        ✗      ✓        ✗       ✓         ◦
           SB+dmb+po                    ✓           ✗        ✗      -       ✗      ✓        ✗      ✓        ✗       ✓         ✗
           WRW+2W+dmb+po                ✓           ✗        ✗     ✓        ✓      ✓        ✗      ✓        ✓       ✗         ✗
           True Positive (TP)                        2              9              13              14               10
           False Positive (FP)                       2              7               8               7                7
           True Negative (TN)                        8              4               3               4                4
           False Negative (FN)                      13              5               1               0                4
           Precision                                0.50           0.56            0.62            0.67             0.59
           Recall                                   0.13           0.64            0.93            1.00             0.71
           Accuracy                                 0.40           0.52            0.64            0.72             0.56
           F1-Score                                 0.21           0.60            0.74            0.80             0.65
Table 5. Comparison of different LLMs in their ability to detect concurrency issues in multithreaded programs from litmus
    tests under relaxed memory models. -: The LLM response does not include assertions. ◦: The LLM produces partial
                            information. We consider - as ✗ in computing TP, FP, TN, and FN.



   Within these columns, the sub-columns titled with Q<index number> correspond to the questions listed in
Table 2, which were used to construct the prompts passed to the LLMs. This detailed breakdown allows for a
side-by-side comparison of how each LLM performed in identifying and addressing concurrency-related issues
across different test cases. The structure of these tables facilitates a clear understanding of each model’s strengths
and weaknesses, providing valuable insights into their capabilities in handling complex concurrency scenarios.
   Tables 3 and 4 capture details present the results for Q2, Q3 and Q4 on different models. We mark yes with
✓and no with ✗. Since LLMs do not typically provide binary answers, all generated responses were manually
evaluated before being assigned. For example, Q2 specifically asks about data races, but the models may generate
responses related to logical races or general race conditions. Similarly, in Q3, which queries deadlocks, some LLMs
may incorrectly respond with livelocks. For Q4, which looks for potential assertion failures, the models may miss
key assert conditions in the code, leading to incorrect conclusions.
   Table 5 provides a comparison of different LLMs in their ability to detect assertion failures in concurrent
programs running under relaxed memory models, such as TSO and PSO. In these scenarios, LLMs not only
generate a prediction of whether an assertion failure might occur but also attempt to provide reasoning for why
the failure happens, often including possible execution traces. For each model, we not only assess whether it
correctly identifies assertion failures but also evaluate the accuracy of the provided explanations. The reasoning
behind an assertion failure is crucial because understanding the underlying cause is key to resolving the issue.
For example, an LLM might correctly predict an assertion failure but offer an incorrect or incomplete explanation
regarding thread interactions, memory ordering, or synchronization mechanisms.

4.6    Results and Analysis
Our analysis aims to answer the research questions outlined earlier in this paper, focusing on the LLMs’ ability to
handle complex concurrency patterns, detect bugs, and reason about relaxed memory models such as TSO and
PSO.

, Vol. 1, No. 1, Article . Publication date: September 2025.
Assessing Large Language Models in Comprehending and Verifying Concurrent Programs across Memory Models                           11


4.6.1 Answering RQ1: How accurately can LLMs understand and summarize concurrent programs?
The accuracy of LLMs in understanding and summarizing concurrent programs varies depending on several
factors, including the complexity of the code, the structure of the code, and the memory model supported by
the host architecture. However, for this particular research question, we prompt the LLM with the Q1 in Table 2
along with the test code without specifying any memory model. We evaluate the selected models based on the
following key points:
  (1) Basic Understanding: All selected models could identify what the program did under a sequentially
      consistent memory model. Interestingly, while the other models produced detailed output by identifying
      global variables and explaining other program details such as function definitions and the assertion
      conditions, GPT-3.5-turbo generally captures the high-level details only.
  (2) Identifying Concurrency Issues: LLMs show varying degrees of success in identifying common con-
      currency issues such as data races, deadlocks, and atomicity violations. While they can sometimes point
      out potential issues, they may miss subtleties, especially in more complex scenarios involving intricate
      inter-thread interactions or relaxed memory models. As per the results of our experiments reported in
      Table 3, GPT-4 outperforms all other models in identifying concurrency issues.
  (3) Summarization: LLMs can generate coherent summaries of concurrent programs, highlighting key com-
      ponents like synchronization mechanisms and shared resources. However, the accuracy and completeness
      of these summaries can be inconsistent. For more complex concurrency patterns, the summaries may omit
      critical details or oversimplify important aspects of the program’s behavior.

4.6.2 Answering RQ2: How can LLMs effectively identify common concurrency issues such as race
conditions, deadlocks, and synchronization errors in concurrent programs?
 To address this research question, we utilized prompts Q2, Q3, and Q4 from Table 2, appending them to the
test code for each of the selected litmus tests and SV-COMP pthread tests. The outcomes of our experiments
are systematically documented in Tables 3 and 4, which present the results for the litmus tests and the pthread
tests, respectively. Each model’s response was manually validated to ensure accuracy and reliability. These tables
provide a detailed analysis of the models’ performance in responding to the prompts across different test scenarios,
offering insights into their ability to understand and process the complexities of concurrent programming under
various conditions.
   Prompts Q2 and Q3 are curated to evaluate LLMs’ capabilities in identifying data races and deadlocks, re-
spectively. Prompt Q4 is designed to investigate whether LLMs can detect assertion failures caused by thread
interactions in concurrent programs. We use atomic load and store instructions with default sequentially consis-
tent ordering to evaluate LLM’s understanding of the program behavior under a sequentially consistent memory
model.
   Prompts Q2 and Q3 were specifically curated to evaluate the capabilities of LLMs in identifying data races and
deadlocks, respectively. In contrast, prompt Q4 is designed to probe whether LLMs can detect assertion failures
that arise from thread interactions in concurrent programs. We employed atomic load and store instructions to
assess the LLMs’ understanding of program behavior under a sequentially consistent memory model, ensuring
they followed the default sequentially consistent ordering. This approach allows us to rigorously test the models’
ability to accurately interpret and analyze the behavior of concurrent programs in environments where memory
operations are expected to maintain a strict order.
   As shown in Tables 3 ans 4, Mistral-AI’s Large2, GPT-4, and GPT-4o outperform the other models. The results
vary slightly between the Litmus tests and SV-COMP’s pthread tests. For instance, in the Litmus tests, Mistral-AI’s
Large2 achieves the highest accuracy in detecting deadlocks, while in the SV-COMP tests, GPT-4 performs best in
this category.
   It is important to note that in Table 3, none of the tests exhibit data races, deadlocks, or assertion failures under
the SC memory model, as they are specifically designed to trigger bugs under the relaxed memory models, TSO
and PSO. Consequently, for all tests, the True Positives and False Negatives are zero, leading to Precision, Recall,
and F1-Score values of zero. As a result, we report only the Accuracy for these cases.

4.6.3 Answering RQ3: How do LLMs compare to traditional static and dynamic analysis tools in verify-
ing concurrent programs in terms of both accuracy and efficiency?
 Some LLMs can effectively identify common concurrency issues such as race conditions, deadlocks, and synchro-
nization errors in concurrent programs by leveraging their ability to analyze code, understand control flow, and

                                                                         , Vol. 1, No. 1, Article . Publication date: September 2025.
12                                                                                              R. Jain and R. Purandare


recognize patterns associated with concurrency problems. The tests listed in Table 3 are manually curated from
the ARM Litmus Tests [2], with all load and store operations on global variables defined as atomic. Consequently,
these tests are free of data races. Additionally, they have been carefully designed to avoid any deadlock scenarios.
Assertion failures in these tests were verified using the Nidhugg tool, with the sequentially consistent memory
model specified by the –sc option. The ground truth for the results reported in Table 4 was generated using the
popular bounded model checking tool ESBMC [35]. This ground truth was further manually verified (with the
.yml files provided with the tests) to ensure accuracy, providing a reliable baseline against which the performance
of the LLMs can be evaluated.
   We consider the following key criteria to evaluate LLMs in their ability to identify common concurrency issues.
     (1) Race condition
         • Pattern Recognition: LLMs can be trained to recognize common code patterns that lead to race conditions,
           such as multiple threads accessing shared variables without proper synchronization. By analyzing
           how variables are read, written, and modified in concurrent code, LLMs can identify scenarios where
           interleaving operations may lead to inconsistent states. Our experiments show that while LLMs have
           limitations in accurately predicting the absence of data races, GPT-4o performed the best among the
           selected LLMs.
         • Semantic Understanding: Contextual Understanding: LLMs can analyze the interactions between different
           threads and the resources they access. They can evaluate whether appropriate locks or synchronization
           mechanisms, such as mutexes, semaphores, or atomic operations, are employed. LLMs can flag potential
           issues by identifying instances where shared data is accessed without adequate protection. In our
           experiments, all selected LLMs demonstrated the ability to correctly identify synchronization primitives.
     (2) Deadlock
         • Locking Order Analysis: LLMs can analyze the sequence in which locks are acquired in a program, helping
           to identify potential deadlocks. Deadlocks often arise when threads attempt to acquire multiple locks in
           an inconsistent order. By examining the sequence of lock acquisitions across threads, LLMs can detect
           circular dependencies or problematic lock hierarchies that might lead to deadlocks. Our experiments reveal
           that while LLMs accurately identified locks and synchronization mechanisms, some models incorrectly
           detected deadlocks. However, LLMs such as Mistral-AI, GPT-4, and GPT-4o achieved a 100 percent
           accuracy rate for litmus tests.
         • State Space Exploration:LLMs can simulate or reason about various execution paths in concurrent pro-
           grams, exploring potential states where deadlocks might occur. LLMs can identify and highlight possible
           deadlock scenarios by simulating thread interactions and resource acquisitions before they manifest. Our
           observations show that all selected models, except GPT-3.5-turbo, generated feasible execution traces for
           the test program.
  Furthermore, Table 5 presents the results of the LLMs’ capabilities in identifying assertion failures that may
occur under relaxed memory models, specifically TSO and PSO. The ground truth for these tests was determined
using the Nidhugg tool with the memory model option –pso, and these results were also manually verified for
correctness. This thorough verification process ensures that the LLMs’ outputs can be accurately assessed against
established standards, allowing for a robust evaluation of their ability to handle complex concurrency issues
under various memory models."

4.6.4 Answering RQ4: Can LLMs predict correct program behaviors under relaxed memory models?
 The 25 litmus tests selected for this study were specifically chosen to address Research Question 5 (RQ5), which
examines the capabilities of LLMs in understanding program behavior under relaxed memory models. These tests
are uniquely tailored to assess the complexities of relaxed memory models, particularly TSO and PSO. To ensure
that the LLMs accurately capture the semantics of relaxed memory, all read and write operations are specified
as atomic and tagged with std::memory_order_relaxed. Table 5 provides key insights in response to Research
Question 5 (RQ5), offering a comparative analysis of the models evaluated:
     (1) Performance in Identifying Relaxed Memory Model Behavior: Among the evaluated models, GPT-4
         demonstrates superior performance in identifying behaviors associated with relaxed memory models, such
         as TSO and PSO. However, despite its relative strength, GPT-4’s performance remains inferior to specialized
         existing tools designed for this specific purpose.

, Vol. 1, No. 1, Article . Publication date: September 2025.
Assessing Large Language Models in Comprehending and Verifying Concurrent Programs across Memory Models                           13


  (2) Accuracy in Identifying Assertion Failures: Models like GPT-4 and GPT-4o show a commendable ability
      to accurately identify assertion failures triggered under relaxed memory models, specifically TSO and
      PSO. Nevertheless, these models often fail to provide correct explanations for the causes of these assertion
      failures. While they generally describe the intra-thread reordering allowed by TSO and PSO accurately,
      they incorrectly attribute the assertion failures to inter-thread reordering when applying their reasoning to
      the test program.
  (3) Handling of Memory Fences: LLMs including, GPT-4, GPT-4o and Mistral-Large2 correctly recognize
      scenarios where memory fences constrain instruction reordering. In these cases, the models accurately
      determine that the assertion holds, acknowledging the role of memory fences in preserving program order
      and ensuring correctness.
  (4) Interleaving Generation: While nearly all evaluated models—except GPT-3.5-turbo—were able to generate
      some feasible traces, none successfully captured the intra-thread reorderings permitted by the relaxed
      memory models. Despite this shortcoming, the detailed outputs provided by the models do offer explanations
      of how events can be reordered within a thread. Interestingly, in some instances, the models mistakenly
      included load-load reorderings under Partial Store Order (PSO), which are, in fact, restricted by this memory
      model. This indicates a partial understanding but also highlights limitations in the models’ comprehension
      of the specific constraints imposed by relaxed memory models.
   While GPT-4 and other advanced LLMs show some ability to understand relaxed memory models and identify
behaviors like TSO and PSO, their performance remains noticeably weaker than that of specialized tools designed
for these specific tasks. Although these models can occasionally identify assertion failures and recognize the role
of memory fences in maintaining program order, they frequently fail to provide accurate explanations for the
underlying causes of these failures, often incorrectly attributing them to inter-thread reorderings. Furthermore,
the models struggle with correctly handling intra-thread reorderings and misunderstand restricted behaviors,
such as load-load reordering under PSO, which exposes significant gaps in their understanding of the complexities
inherent in relaxed memory models.
   Tables 3 and 4 provide a comparative analysis of the efficacy of different LLMs in identifying concurrency-
related issues in multi-threaded programs, benchmarked against the established ground truth. These tables
showcase the performance of the LLMs in detecting critical issues such as data races, deadlocks, and assertion
failures, highlighting the strengths and limitations of each model.
   It is important to note that the prompts passed to the LLMs during these evaluations did not explicitly specify
any particular memory model. This omission intentionally assessed the LLMs’ inherent ability to reason about
concurrency issues without relying on predefined memory model constraints. The results captured in these
tables offer insights into how well the LLMs can generalize and apply their understanding of concurrency across
different scenarios, even when the underlying memory model is not explicitly defined. This approach allows us
to gauge the models’ adaptability and robustness in handling complex, real-world concurrency challenges.

4.7 Case Study
Listings 1 and 2 showcase two sample codes from the Litmus tests, CoRW and 2+2W, respectively. We provide
the corresponding question posed to the LLMs and the test code for each listing. Additionally, on the same page,
responses from various LLMs are presented alongside the listings for comparison.
   Listing 1 presents a code snippet that creates two threads, contains no data races, and where the assertion
always holds under SC, TSO, and PSO memory models. In addition, the code snippet contains atomic operations
with default SC semantics. We showcase the responses generated by various LLMs when asked whether they
could identify any data race in the provided code. As LLM responses are often verbose, we include pruned versions
that capture the key points. Responses are color-coded: 1) green for factually correct and relevant answers, 2)
yellow for correct but non-essential or partial information, and 3) red for incorrect information.
   We observe that GPT-4 generates the most factually correct and relevant information compared to the evaluated
models. Although GPT-4 answers the question correctly, it occasionally includes irrelevant or incorrect details. In
contrast, GPT-3.5-turbo, GPT-4o-mini, and Mistral-AI’s Large2 incorrectly predict the presence of a data race
in the code. GPT-4o, while producing a significant amount of irrelevant information, ultimately identifies the
absence of data races correctly with default SC semantics. We showcase the responses generated by various LLMs
when asked "Can you identify a potential data race or race condition in the following program?" along with the test
program.

                                                                         , Vol. 1, No. 1, Article . Publication date: September 2025.
14                                                                                                                          R. Jain and R. Purandare



     Listing 1. A concurrent code example (CoRW) from                                           GPT-3.5-turbo Response
                                                                           Yes, there is a potential data race in the program. The
     the limus tests.                                                      data race occurs when both ‘thread1‘ and ‘thread2‘ access
     # include < pthread .h >                                              and modify the shared atomic variable ‘x‘ without proper
     # include < atomic >                                                  synchronization.
     # include < assert .h >                                               In ‘thread1‘ function, ‘x‘ is first loaded and then compared to 2
                                                                           to store a value in the atomic variable ‘a‘. However, in ‘thread2‘
     using namespace std ;                                                 function, ‘x‘ is directly modified without any synchronization.
                                                                           If ‘thread2‘ modifies ‘x‘ after ‘thread1‘ has loaded but before
     atomic_int x;                                                         the comparison is made in ‘thread1‘, then the assertion at the
     atomic_int a;                                                         end of ‘main‘ may fail.
                                                                           To resolve this potential data race, you can use proper syn-
     void * thread1 ( void * threadid )                                    chronization mechanisms such as mutex locks or atomic oper-
     {                                                                     ations to ensure that only one thread can access and modify
         int p;                                                            the shared variable ‘x‘ at a time.
         atomic_store (&x , 1) ;
         p = atomic_load (& x );
         if (p == 2)
         {                                                                                      GPT-4 Response
              atomic_store (&a , 1) ;                                      No, there is no data race in this program. All the shared data –
         }                                                                 ‘x‘ and ‘a‘ – are accessed using atomic operations, guarantee-
     }                                                                     ing that the operations are performed in a thread-safe manner.
                                                                           There is, however, a race condition between ‘thread1‘ and
     void * thread2 ( void * threadid )                                    ‘thread2‘ regarding the value of ‘x‘.
     {                                                                     In ‘thread1‘, if ‘x‘ equals ‘2‘, it will set ‘a‘ to ‘1‘. In ‘thread2‘,
         atomic_store (&x , 2) ;                                           ‘x‘ is set to ‘2‘. However, the order in which thread1 and
     }                                                                     thread2 are scheduled to run is not deterministic. Therefore,
                                                                           it’s possible ‘thread1‘ executes before ‘thread2‘ and hence the
     int main ()                                                           if-condition ‘p == 2‘ will never be true and ‘a‘ would never be
     {                                                                     set to ‘1‘. On the other hand, if ‘thread2‘ runs before ‘thread1‘,
       int i =0;                                                           ‘x‘ is set to ‘2‘ and thus ‘a‘ will be set to ‘1‘. These represent
       int j =1;                                                           two different execution outcomes based on scheduling, which
       int rc1 , rc2 ;                                                     is a race condition (related to timing and sequencing), but not
       pthread_t threads [2];                                              a data race.
       rc1 = pthread_create (& threads [0] , NULL ,
                                   thread1 , ( void *) i );
       rc2 = pthread_create (& threads [1] , NULL ,
                                   thread2 , ( void *) j );                                     GPT-4o Response
       ( void ) pthread_join ( threads [0] , NULL );                       To identify a potential data race in the given program, let’s
       ( void ) pthread_join ( threads [1] , NULL );                       analyze the interplay between the two threads and the shared
       assert ( x != 1 || a != 1) ;                                        atomic variables ‘x‘ and ‘a‘.
     }                                                                     Here’s a breakdown of the execution flow:
                                                                                 • Thread 1 (‘thread1‘ function): - Loads the value of ‘x‘
                                                                                    into ‘p‘. - Stores ‘1‘ into ‘x‘. - If ‘p‘ is ‘2‘, then stores
     Q Can you identify a potential data race or race                               ‘1‘ into ‘a‘.
                                                                                 • Thread 2 (‘thread2‘ function): - Stores ‘2‘ into ‘x‘.
     condition in the following program?                                         • Main function: - Creates two threads running
                                                                                    ‘thread1‘ and ‘thread2‘. - Joins the threads. - Asserts
                                                                                    that ‘a != 1 || x != 2‘.
                                                                           In the context of atomic operations:
                             Mistral-AI Response                                 • Atomicity and Atomic Operations: -Atomic opera-
         Yes, there is a potential data race in the given program. The              tions themselves do not have data races because they
         data race occurs because the two threads can access and                    complete without interference. -However, the pro-
         modify the shared atomic variables ‘x‘ and ‘a‘ concurrently                gram’s logic could still lead to unintended outcomes,
         without proper synchronization, leading to unpredictable                   depending on the order of atomic operations between
         behavior. The race condition arises because the order of                   the two threads.
         execution of these operations is not deterministic. Here
         are some possible scenarios:
         Scenario 1:
                • Thread 1 stores ‘1‘ into ‘x‘.                                               GPT-4o-mini Response
                • Thread 2 stores ‘2‘ into ‘x‘.                            The program you provided has potential data races due to
                • Thread 1 loads ‘2‘ from ‘x‘ into ‘p‘.                    improper synchronization between the threads. We need to
                • Since ‘p‘ is ‘2‘, Thread 1 stores ‘1‘ into ‘a‘.          analyze the code step by step to identify potential issues.
                                                                            Potential Data Race Analysis Thread Scheduling:
         Scenario 2:
                                                                                • The execution of thread 1 and thread 2 is non-
                • Thread 1 stores ‘1‘ into ‘x‘.                                    deterministic. The order in which they run can vary.
                • Thread 1 loads ‘1‘ from ‘x‘ into ‘p‘.                         • If thread 1 runs first, it will store ‘1‘ in ‘x‘ and subse-
                • Since ‘p‘ is not ‘2‘, Thread 1 does not store ‘1‘ into           quently load the value of ‘x‘. If thread 2 has not yet
                  ‘a‘.
                                                                                   executed, ‘p‘ will be ‘1‘, and ‘a‘ will not be set.
                • Thread 2 stores ‘2‘ into ‘x‘.                                 • If thread 1 runs first, it will store ‘1‘ in ‘x‘ and subse-
         In the first scenario, both ‘x‘ and ‘a‘ could end up being                quently load the value of ‘x‘.
         ‘1‘, which would violate the assertion ‘assert(x != 1 || a !=          • If thread 2 runs first, it sets ‘x‘ to ‘2‘ before thread 1
         1)‘.                                                                      reads the value. In this case, when thread 1 reads ‘x‘,
                                                                                   it finds ‘p == 2‘, and thus ‘a‘ is set to ‘1‘.



        True &               True but                False
       Relevant             Irrelevant            Statement
, Vol. 1, No. 1, Article . Publication date: September 2025.
Assessing Large Language Models in Comprehending and Verifying Concurrent Programs across Memory Models                                            15




    Listing 2. A concurrent code example (2+2W) from                                            GPT-3.5-turbo Response
    the limus tests.                                                      In this particular program, the use of relaxed memory order
    # include   < iostream >                                              for storing and loading values in the atomic variables x, y, a,
    # include   < pthread .h >                                            and b can lead to race conditions. For example, in thread2 and
    # include   < atomic >                                                thread3, there is no synchronization mechanism to ensure
    # include   < assert .h >                                             proper ordering of operations on the shared variables x and
                                                                          y. As a result, it is possible for the atomic stores and loads to
    std :: atomic < int > x;                                              be reordered in a way that violates the intended logic of the
    std :: atomic < int > y;                                              program. Additionally, the use of std::atomic_thread_fence
                                                                          with memory_order_seq_cst in thread2 and thread3 does not
    void * thread1 ( void * threadid )                                    guarantee the necessary synchronization between threads
    {                                                                     to prevent data races. The relaxed memory orders used in
                                                                          combination with the fence may lead to unexpected behavior
          x. store (2 , std :: memory_order_relaxed );                    due to lack of synchronization.
          y. store (1 , std :: memory_order_relaxed );
    }

    void * thread2 ( void * threadid )                                                        GPT-4 Response
    {                                                                     Here are the possible scenarios for this program:
        y. store (3 , std :: memory_order_relaxed );                      1. Thread1 runs then thread2 runs: The final values will be ‘x
        x. store (4 , std :: memory_order_relaxed );                      = 4, y = 3‘ and the assert will not fail.
    }                                                                     2. Thread2 runs then thread1 runs: The final values will be ‘x
                                                                          = 2, y = 1‘ and the assert will not fail.
    int main ()                                                           3. Thread1 and thread2 run concurrently and the operations
    {                                                                     interleave: The potential outcomes are harder to predict due
      int i =0;                                                           to reordering allowed by the relaxed memory model. It’s pos-
      int j =1;                                                           sible for either ‘x or y‘ or both to get either of their possible
      int rc1 , rc2 ;                                                     values from the threads (2 or 4 for ‘x‘, 1 or 3 for ‘y‘), and these
      pthread_t threads [2];                                              assignments can happen in any order.
      rc1 = pthread_create (& threads [0] , NULL ,                        Therefore, With the relaxed memory model, it’s theoretically
                                  thread1 , ( void *) i);                 possible to reach a state where ‘x = 2 and y = 3‘, which would
      rc2 = pthread_create (& threads [1] , NULL ,                        cause the assert to fail.
                                  thread2 , ( void *) j);
      ( void ) pthread_join ( threads [0] , NULL );
      ( void ) pthread_join ( threads [1] , NULL );
                                                                                                 GPT-4o Response
        assert ( x != 2 || y != 3 );
                                                                          TSO is relatively strict, so while it allows some reordering, it
                                                                          guarantees that writes will appear in order from each thread’s
    }
                                                                          perspective.
                                                                          Partial Store Order (PSO) PSO allows even more flexibility
                                                                          than TSO, as stores can appear out of order even within a
                                                                          single thread.
    Q How do relaxed memory models such as total                          Even under PSO, the memory model allows more reordering
    store order and partial store order affect the                        and relaxation compared to TSO, but given the constraints of
                                                                          atomic variables and basic operations, the assertion ‘assert(x
    following program’s behavior?                                         != 2 || y != 3);‘ will still hold true. The program’s safe ordering
                                                                          practices due to atomic variables ensure that ‘x == 2‘ and ‘y
                                                                          == 3‘ are not observed together.
                                                                          In conclusion, the assertion will not fail in either TSO or
                            Mistral-AI Response                           PSO due to the properties of atomic operations, even with
          Relaxed memory models, such as Total Store Order (TSO)          ‘memory_order_relaxed‘.
          and Partial Store Order (PSO), allow for certain reorder-
          ings of memory operations that can affect the behavior of
          concurrent programs. Let’s analyze how these memory
          models might affect the given program.                                               GPT-4o-mini Response
          ***Generates SC Traces***                                       • Thread 1 Completes First: Suppose Thread 1 executes
          Assertion Analysis                                                first and sets ‘x‘ to ‘2‘ and then ‘y‘ to ‘1‘. After this completes,
          The assertion assert(x != 2 || y != 3) checks that it is not      we can have: - ‘x = 2‘ and ‘y = 1‘ - This would not trigger
          possible for x to be 2 and y to be 3 at the same time.            the assert.
                                                                          • Thread 2 Completes First" If Thread 2 sets ‘y‘ to ‘3‘ first
          Given the possible outcomes listed above, it is clear that        and then ‘x‘ to ‘4‘, then afterwards: - ‘x = 4‘ and ‘y = 3‘ -
          the assertion should never fail because:                          This would also not trigger the assert.
          • If x is 2, then y must be 1 (since Thread 1 sets y to 1       • 3. Interleavings: However, because of relaxed memory
             after setting x to 2).                                         (especially in PSO), Thread 1 and Thread 2 can have inter-
          • If y is 3, then x must be 4 (since Thread 2 sets x to 4         leaved executions: - Thread 1 sets ‘x = 2‘ - Thread 2 sets
             after setting y to 3).                                         ‘y = 3‘ - Thread 1 sets ‘y = 1‘ - Thread 2 sets ‘x = 4‘ In this
                                                                            final state, the values at the end would be: - ‘x = 4‘ and ‘y =
          Therefore, the assertion assert(x != 2 || y != 3) will always
                                                                            1‘ - This does not trigger the assert.
          hold true, regardless of the interleaving of the threads
          under TSO or PSO.
                                                                          • 4. **Unexpected Visibility**: Yet, due to memory reordering,
                                                                            it’s also possible (though implausible under these atomic
                                                                            operations) that Thread 2 could see ‘x = 2‘ and ‘y = 3‘ if
                                                                            operations were reordered at the store level (which might
                                                                            not normally happen but could theoretically if compilers
         True &              True but               False                   optimized it in an unintended way).

        Relevant            Irrelevant           Statement



                                                                                , Vol. 1, No. 1, Article . Publication date: September 2025.
16                                                                                             R. Jain and R. Purandare


   Similarly, the sample code in Listing 2 creates two threads that perform atomic operations on variables x and y.
These events can be reordered according to the specified memory order memory_order_relaxed within the
thread, potentially leading to an assertion failure. However, since the operations are atomic, no data race occurs.
We explicitly specify memory order consistency when prompting the LLMs about the code’s behavior under
relaxed memory models, TSO, and PSO. The responses are pruned and color-coded for clarity.
   Although reasoning about a concurrent program’s behavior under relaxed memory models can be challenging
for LLMs due to insufficient training data, GPT-4 correctly identifies the potential for an assertion failure under
PSO memory ordering, though it also generates some irrelevant information. Interestingly, it does not produce the
trace, which leads to the error. Mistral-AI Large 2 and GPT-4o, while accurately defining the memory orderings
permitted under TSO and PSO, incorrectly respond that the assertion always holds, as they fail to provide a
feasible trace leading to the error. Surprisingly, GPT-4o-mini offers only correct and relevant information but also
fails to produce the failing trace.
   Our evaluation of LLM responses to concurrent programming code shows varying performance. For Listing 1,
which tests for data races, GPT-4 is the most accurate, though it occasionally includes irrelevant details. GPT-
3.5-turbo, GPT-4o-mini, and Mistral-AI Large2 mistakenly identify a data race, while GPT-4o provides mostly
irrelevant information but correctly identifies the absence of data races. For Listing 2, which involves atomic
operations under relaxed memory models, GPT-4 accurately predicts potential assertion failures under PSO but
does not provide the error trace. Mistral-AI Large 2 and GPT-4o correctly describe memory orderings but fail to
detect assertion failures, and GPT-4o-mini, while accurate, also misses the error trace.

5     Discussion
In this section, we discuss the key strengths and limitations of LLMs in the context of concurrent program analysis
based on the results of our study.

5.1    Strengths
5.1.1 Natural Language Reasoning and Explanation. One of the core strengths of LLMs, particularly models like
GPT-4, is their ability to reason about code and explain in natural language. This capability makes them highly
accessible to developers who may not be well-versed in formal verification tools. LLMs can explain the potential
risks or issues in concurrent code, such as race conditions or deadlocks, in an intuitive and human-readable
manner.

5.1.2 Detection of Simple Concurrency Bugs. LLMs can detect basic concurrency issues like race conditions and
deadlocks in simpler, small-scale programs. In our study, GPT-4 and GPT-4o demonstrate the highest accuracy
in successfully identifying common concurrency bugs that were present in the selected tests. This shows the
potential of LLMs to serve as a first pass for identifying glaring concurrency bugs without the need for complex
tool configurations.

5.1.3 Flexibility Across Various Codebases. Unlike traditional static analysis tools, which often require config-
uration and may be language-specific, LLMs can analyze a wide range of codebases with minimal setup. This
flexibility allows LLMs to be used in various programming languages and frameworks, providing a more universal
solution.

5.1.4 Understanding of High-Level Memory Model Concepts. LLMs, especially GPT-4, reasonably understood
high-level memory model concepts such as Total Store Order (TSO) and Partial Store Order (PSO). While their
analysis was not always precise, their ability to reason about the effects of memory ordering on program behavior
demonstrated promise.

5.2    Challenges
5.2.1 Incomplete and Inconsistent Analysis. Despite their strengths in detecting basic concurrency issues, LLMs
are prone to incomplete and inconsistent analysis. The models may struggle to provide accurate or actionable
insights in complex scenarios involving deep synchronization mechanisms or rare concurrency bugs. For example,
GPT-4 correctly identified some concurrency bugs but often missed subtle issues, such as those arising from
intricate interleavings of thread execution. This inconsistency limits the reliability of LLMs for comprehensive
program verification.

, Vol. 1, No. 1, Article . Publication date: September 2025.
Assessing Large Language Models in Comprehending and Verifying Concurrent Programs across Memory Models                           17


5.2.2 Lack of Formal Guarantees. Unlike traditional verification tools, which can provide formal guarantees of
program correctness, LLMs rely on probabilistic models that generate responses based on learned patterns. As a
result, LLMs cannot offer the same level of certainty in their analysis. For instance, while models like ESBMC [35]
and Nidhugg [1] systematically explore all possible execution paths to identify concurrency issues, LLMs may
overlook important edge cases or provide incorrect solutions that only appear plausible.
5.2.3 Difficulty in Handling Relaxed Memory Models. Although LLMs showed some understanding of relaxed
memory models, they struggled to handle the intricacies of TSO and PSO effectively. The models often failed to
provide detailed error traces or identify subtle reordering issues that could lead to assertion failures.
5.2.4 Verbose and Irrelevant Responses. Another notable limitation of LLMs is the tendency to produce verbose
responses, often including irrelevant or tangential information. In many cases, LLMs would provide lengthy
explanations that mixed correct and incorrect information, making it difficult to extract useful insights. This
verbosity can hinder developers who need concise, actionable feedback on concurrency issues.

6   Future Work
Our evaluation of LLMs for verifying concurrent programs under relaxed memory models highlights several
exciting future research opportunities. One key direction is to enhance the integration between LLMs and
traditional verification tools to improve the accuracy and depth of automated verification. Developing interfaces
that allow LLMs to effectively utilize verification results could enable the automation of complex verification
tasks. A promising approach is creating hybrid systems that combine the LLM’s natural language reasoning with
classical verification methods, potentially allowing these systems to automatically generate and validate patches
or bug fixes.
   Further, current LLMs struggle to accurately handle the subtleties of concurrency and memory models like
TSO and PSO. Future research could focus on fine-tuning LLMs using datasets specifically curated for concurrent
programming and memory model behaviors. By training LLMs on a broader set of code examples involving
complex thread interactions, non-deterministic behaviors, and relaxed memory model effects, we can potentially
improve their performance in identifying concurrency bugs and reasoning about reordering scenarios.
   Another promising direction is the automatic generation of test cases for concurrency issues. LLMs could be
utilized to generate synthetic test cases designed to expose subtle bugs in multi-threaded programs under various
memory models.
   While this study focused on TSO and PSO memory models, other relaxed memory models, such as Release
Consistency (RC) and Weak Memory Consistency (WMC), are used in various hardware architectures. Future
research could expand LLM analysis to include these additional memory models. Additionally, extending LLM
capabilities to cover a broader range of programming languages commonly used for concurrent programming,
such as Rust, Go, and Erlang, would enhance the study’s relevance. Supporting multiple languages would enable
wider adoption and applicability of LLMs across diverse industries and software systems, beyond the scope of the
C/C++ programs evaluated in this study.

7   Conclusion
This paper has examined the capabilities of LLMs in verifying concurrent programs under relaxed memory
models. Our evaluation highlights both the potential and limitations of these models in addressing the inherent
complexities of concurrency and memory consistency.
   LLMs can be a powerful tool in the verification of concurrent programs, especially under related memory
models. They can help developers understand and manage the complexities of concurrency, generate useful
test cases, and even suggest optimizations. However, they should be used as a complement to, rather than a
replacement for, traditional formal methods and testing tools, particularly when dealing with the nuanced and
often complex nature of memory models.
   This study underscores the potential and limitations of LLMs in analyzing concurrency issues within software
programs. While GPT-4 outperforms other models in identifying data races and deadlocks under a sequentially
consistent memory model, it, along with the other evaluated models, struggles to effectively verify program
correctness under relaxed memory models like TSO and PSO. The findings highlight a significant gap in the
current capabilities of LLMs, particularly in accurately capturing the complexities of memory ordering constraints.
As concurrent programming continues to grow in importance, advancing LLMs to better handle these challenges
is crucial for enhancing their reliability in concurrent program analysis and verification. Future research should

                                                                         , Vol. 1, No. 1, Article . Publication date: September 2025.
18                                                                                                                  R. Jain and R. Purandare


focus on refining these models to address the nuanced demands of relaxed memory models, aiming to bridge the
gap in their applicability to real-world concurrent programming scenarios.

8    Availability
To promote reproducibility and enable further research, all resources and materials used in this study are fully
accessible to the research community. This includes the datasets, such as SV-COMP’s pthread tests and ARM
Litmus tests, as well as the complete code implementations used in our experiments. Furthermore, all custom
scripts, evaluation metrics, and additional tools developed during this study are openly shared in a public
repository, available at https://anonymous.4open.science/r/LLM-Conc-RMM-13F8. This ensures that researchers
can not only reproduce our results but also expand upon them by extending the scope of this work. By prioritizing
transparency and accessibility, we aim to accelerate advancements in the analysis of concurrent programs under
relaxed memory models and LLM evaluation.

References
  [1] Abdulla, P. A., Aronis, S., Atig, M. F., Jonsson, B., Leonardsson, C., and Sagonas, K. Stateless model checking for tso and pso.
      Acta Informatica 54 (2017), 789–818.
  [2] Alglave, J., Maranget, L., Sarkar, S., and Sewell, P. Litmus: Running tests against hardware. In International Conference on Tools
      and Algorithms for the Construction and Analysis of Systems (2011), Springer, pp. 41–44.
  [3] Alrashedy, K., and Aljasser, A. Can llms patch security issues? arXiv preprint arXiv:2312.00024 (2023).
  [4] Ashiwal, V., Finster, S., and Dawoud, A. Llm-based vulnerability sourcing from unstructured data. In 2024 IEEE European Symposium
      on Security and Privacy Workshops (EuroS&PW) (2024), IEEE, pp. 634–641.
  [5] Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski, H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., et al. Program synthesis
      with large language models. arXiv preprint arXiv:2108.07732 (2021).
  [6] Baghdadi, R., Merouani, M., Leghettas, M.-H., Abdous, K., Arbaoui, T., Benatchba, K., et al. A deep learning based cost model
      for automatic code optimization. Proceedings of Machine Learning and Systems 3 (2021), 181–193.
  [7] Bao, W., Krishnamoorthy, S., Pouchet, L.-N., Rastello, F., and Sadayappan, P. Polycheck: Dynamic verification of iteration space
      transformations on affine programs. ACM SIGPLAN Notices 51, 1 (2016), 539–554.
  [8] Berabi, B., Gronskiy, A., Raychev, V., Sivanrupan, G., Chibotaru, V., and Vechev, M. Deepcode ai fix: Fixing security vulnerabilities
      with large language models. arXiv preprint arXiv:2402.13291 (2024).
  [9] Beyer, D. Competition on software verification and witness validation: Sv-comp 2023. In International Conference on Tools and
      Algorithms for the Construction and Analysis of Systems (2023), Springer, pp. 495–522.
 [10] Beyer, D., and Lemberger, T. Cpa-symexec: efficient symbolic execution in cpachecker. In Proceedings of the 33rd ACM/IEEE
      International Conference on Automated Software Engineering (2018), pp. 900–903.
 [11] Blackshear, S., Gorogiannis, N., O’Hearn, P. W., and Sergey, I. Racerd: compositional static race detection. Proceedings of the ACM
      on Programming Languages 2, OOPSLA (2018), 1–28.
 [12] Bliudze, S., Cimatti, A., Jaber, M., Mover, S., Roveri, M., Saab, W., and Wang, Q. Formal verification of infinite-state bip models. In
      Automated Technology for Verification and Analysis: 13th International Symposium, ATVA 2015, Shanghai, China, October 12-15, 2015,
      Proceedings 13 (2015), Springer, pp. 326–343.
 [13] Bouzenia, I., Devanbu, P., and Pradel, M. Repairagent: An autonomous, llm-based agent for program repair. arXiv preprint
      arXiv:2403.17134 (2024).
 [14] Brown, T. B. Language models are few-shot learners. arXiv preprint ArXiv:2005.14165 (2020).
 [15] Bu, L., Xie, Z., Lyu, L., Li, Y., Guo, X., Zhao, J., and Li, X. Brick: Path enumeration based bounded reachability checking of c program
      (competition contribution). In International Conference on Tools and Algorithms for the Construction and Analysis of Systems (2022),
      Springer, pp. 408–412.
 [16] Cadar, C., and Nowack, M. Klee symbolic execution engine in 2019. International Journal on Software Tools for Technology Transfer 23
      (2021), 867–870.
 [17] Cai, Q., Wang, Z., Diao, S., Kwok, J., and Song, Y. Codegraph: Enhancing graph reasoning of llms with code. arXiv preprint
      arXiv:2408.13863 (2024).
 [18] Cao, S., Sun, X., Bo, L., Wei, Y., and Li, B. Bgnn4vd: Constructing bidirectional graph neural-network for vulnerability detection.
      Information and Software Technology 136 (2021), 106576.
 [19] Carpenter, G. A. Neural network models for pattern recognition and associative memory. Neural networks 2, 4 (1989), 243–257.
 [20] Charalambous, Y., Tihanyi, N., Jain, R., Sun, Y., Ferrag, M. A., and Cordeiro, L. C. A new era in software security: Towards
      self-healing software via large language models and formal verification. arXiv preprint arXiv:2305.14752 (2023).
 [21] Chen, L., Ding, X., Emani, M., Vanderbruggen, T., Lin, P.-H., and Liao, C. Data race detection using large language models. In
      Proceedings of the SC’23 Workshops of The International Conference on High Performance Computing, Network, Storage, and Analysis
      (2023), pp. 215–223.
 [22] Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. D. O., Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman, G., et al.
      Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374 (2021).
 [23] Cheng, X., Wang, H., Hua, J., Xu, G., and Sui, Y. Deepwukong: Statically detecting software vulnerabilities using deep graph neural
      network. ACM Transactions on Software Engineering and Methodology (TOSEM) 30, 3 (2021), 1–33.
 [24] Costea, A., Tiwari, A., Chianasta, S., Roychoudhury, A., and Sergey, I. Hippodrome: Data race repair using static analysis
      summaries. ACM Transactions on Software Engineering and Methodology 32, 2 (2023), 1–33.

, Vol. 1, No. 1, Article . Publication date: September 2025.
Assessing Large Language Models in Comprehending and Verifying Concurrent Programs across Memory Models                                      19


 [25] Cui, H., Xie, M., Su, T., Zhang, C., and Tan, S. H. An empirical study of false negatives and positives of static code analyzers from the
      perspective of historical issues, 2024.
 [26] Cummins, C., Fisches, Z. V., Ben-Nun, T., Hoefler, T., and Leather, H. Programl: Graph-based deep learning for program optimization
      and analysis. arXiv preprint arXiv:2003.10536 (2020).
 [27] De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. A rule-based verification strategy for array manipulating programs.
      Fundamenta Informaticae 140, 3-4 (2015), 329–355.
 [28] Demsky, B., and Lam, P. Satcheck: Sat-directed stateless model checking for sc and tso. ACM SIGPLAN Notices 50, 10 (2015), 20–36.
 [29] Deng, Y., Xia, C. S., Peng, H., Yang, C., and Zhang, L. Large language models are zero-shot fuzzers: Fuzzing deep-learning libraries
      via large language models. In Proceedings of the 32nd ACM SIGSOFT international symposium on software testing and analysis (2023),
      pp. 423–435.
 [30] Eberhardt, G., and Milánkovich, Á. Vulngpt: Enhancing source code vulnerability detection using autogpt and adaptive supervision
      strategies. In 2024 20th International Conference on Distributed Computing in Smart Systems and the Internet of Things (DCOSS-IoT)
      (2024), IEEE, pp. 450–454.
 [31] Eghbali, A., and Pradel, M. De-hallucinator: Iterative grounding for llm-based code completion. arXiv preprint arXiv:2401.01701
      (2024).
 [32] Fan, G., Diao, X., Yu, H., Yang, K., and Chen, L. Software defect prediction via attention-based recurrent neural network. Scientific
      Programming 2019, 1 (2019), 6230953.
 [33] Fan, Z., Gao, X., Roychoudhury, A., and Tan, S. H. Automated repair of programs from large language models. arXiv preprint
      arXiv:2205.10583 (2022).
 [34] Ferrag, M. A., Battah, A., Tihanyi, N., Debbah, M., Lestable, T., and Cordeiro, L. C. Securefalcon: The next cyber reasoning
      system for cyber security. arXiv preprint arXiv:2307.06616 (2023).
 [35] Gadelha, M. R., Monteiro, F. R., Morse, J., Cordeiro, L. C., Fischer, B., and Nicole, D. A. Esbmc 5.0: an industrial-strength c model
      checker. In ACM/IEEE ASE (2018), pp. 888–891.
 [36] Gao, S., Gao, C., Gu, W., and Lyu, M. Search-based llms for code optimization. arXiv preprint arXiv:2408.12159 (2024).
 [37] Gu, Y., and Mellor-Crummey, J. Dynamic data race detection for openmp programs. In SC18: International Conference for High
      Performance Computing, Networking, Storage and Analysis (2018), IEEE, pp. 767–778.
 [38] Hasanzad, E., and Babamir, S. M. Prediction of deadlocks in concurrent programs using neural network.
 [39] Havelund, K. Rule-based runtime verification revisited. International Journal on Software Tools for Technology Transfer 17 (2015),
      143–170.
 [40] Hellendoorn, V. J., and Devanbu, P. Are deep neural networks the best choice for modeling source code? In Proceedings of the 2017
      11th Joint meeting on foundations of software engineering (2017), pp. 763–773.
 [41] Hidvégi, D., Etemadi, K., Bobadilla, S., and Monperrus, M. Cigar: Cost-efficient program repair with llms. arXiv preprint
      arXiv:2402.06598 (2024).
 [42] Hu, P., Liang, R., and Chen, K. Degpt: Optimizing decompiler output with llm. In Proceedings 2024 Network and Distributed System
      Security Symposium (2024). https://api. semanticscholar. org/CorpusID (2024), vol. 267622140.
 [43] Hu, X., Men, R., Li, G., and Jin, Z. Deep-autocoder: Learning to complete code precisely with induced code tokens. In 2019 IEEE 43rd
      Annual Computer Software and Applications Conference (COMPSAC) (2019), vol. 1, IEEE, pp. 159–168.
 [44] Jain, N., Vaidyanath, S., Iyer, A., Natarajan, N., Parthasarathy, S., Rajamani, S., and Sharma, R. Jigsaw: Large language models
      meet program synthesis. In Proceedings of the 44th International Conference on Software Engineering (2022), pp. 1219–1231.
 [45] Jain, R., Purandare, R., and Sharma, S. Bird: Race detection in software binaries under relaxed memory models. ACM Transactions
      on Software Engineering and Methodology (TOSEM) 31, 4 (2022), 1–29.
 [46] Jin, M., Shahriar, S., Tufano, M., Shi, X., Lu, S., Sundaresan, N., and Svyatkovskiy, A. Inferfix: End-to-end program repair with
      llms. In Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software
      Engineering (2023), pp. 1646–1656.
 [47] Johnson, B., Song, Y., Murphy-Hill, E., and Bowdidge, R. Why don’t software developers use static analysis tools to find bugs? In
      35th International Conference on Software Engineering (ICSE) (2013), IEEE, pp. 672–681.
 [48] Joshi, H., Sanchez, J. C., Gulwani, S., Le, V., Verbruggen, G., and Radiček, I. Repair is nearly generation: Multilingual program
      repair with llms. In Proceedings of the AAAI Conference on Artificial Intelligence (2023), vol. 37, pp. 5131–5140.
 [49] Jourdan, J.-H. Verasco: a formally verified C static analyzer. PhD thesis, Universite Paris Diderot-Paris VII, 2016.
 [50] Kande, R., Pearce, H., Tan, B., Dolan-Gavitt, B., Thakur, S., Karri, R., and Rajendran, J. (security) assertions by large language
      models. IEEE Transactions on Information Forensics and Security (2024).
 [51] Kester, D., Mwebesa, M., and Bradbury, J. S. How good is static analysis at finding concurrency bugs? In 10th IEEE Working
      Conference on Source Code Analysis and Manipulation (2010), IEEE, pp. 115–124.
 [52] Khanna, D., Sharma, S., Rodríguez, C., and Purandare, R. Dynamic symbolic verification of mpi programs. In Formal Methods: 22nd
      International Symposium, FM 2018, Held as Part of the Federated Logic Conference, FloC 2018, Oxford, UK, July 15-17, 2018, Proceedings 22
      (2018), Springer, pp. 466–484.
 [53] Kokologiannakis, M., and Vafeiadis, V. Hmc: Model checking for hardware memory models. In Proceedings of the Twenty-Fifth
      International Conference on Architectural Support for Programming Languages and Operating Systems (2020), pp. 1157–1171.
 [54] Le, H., Wang, Y., Gotmare, A. D., Savarese, S., and Hoi, S. C. H. Coderl: Mastering code generation through pretrained models and
      deep reinforcement learning. Advances in Neural Information Processing Systems 35 (2022), 21314–21328.
 [55] LeClair, A., Haqe, S., Wu, L., and McMillan, C. Improved code summarization via a graph neural network. In Proceedings of the
      28th international conference on program comprehension (2020), pp. 184–195.
 [56] Leinonen, J., Hellas, A., Sarsa, S., Reeves, B., Denny, P., Prather, J., and Becker, B. A. Using large language models to enhance
      programming error messages. In Proceedings of the 54th ACM Technical Symposium on Computer Science Education V. 1 (2023),


                                                                                    , Vol. 1, No. 1, Article . Publication date: September 2025.
20                                                                                                                     R. Jain and R. Purandare


      pp. 563–569.
 [57] Li, H., Hao, Y., Zhai, Y., and Qian, Z. Enhancing static analysis for practical bug detection: An llm-integrated approach. Proceedings of
      the ACM on Programming Languages 8, OOPSLA1 (2024), 474–499.
 [58] Li, J., He, P., Zhu, J., and Lyu, M. R. Software defect prediction via convolutional neural network. In 2017 IEEE international conference
      on software quality, reliability and security (QRS) (2017), IEEE, pp. 318–328.
 [59] Li, Z., Dutta, S., and Naik, M. Llm-assisted static analysis for detecting security vulnerabilities. arXiv preprint arXiv:2405.17238 (2024).
 [60] Liu, C., Zhang, S. D., and Jabbarvand, R. Codemind: A framework to challenge large language models for code reasoning. arXiv
      preprint arXiv:2402.09664 (2024).
 [61] Liu, J., Chen, Y., Liu, M., Peng, X., and Lou, Y. Stall+: Boosting llm-based repository-level code completion with static analysis. arXiv
      preprint arXiv:2406.10018 (2024).
 [62] Liu, J., and et al. Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation.
      In NeurIPS (2024).
 [63] Liu, J., Xia, C. S., Wang, Y., and Zhang, L. Is your code generated by chatgpt really correct? rigorous evaluation of large language
      models for code generation. arXiv preprint arXiv:2305.01210 (2023).
 [64] Liu, J., Xia, C. S., Wang, Y., and Zhang, L. Is your code generated by chatgpt really correct? rigorous evaluation of large language
      models for code generation. Advances in Neural Information Processing Systems 36 (2024).
 [65] Liu, Z., Feng, Y., Yin, Y., and Chen, Z. Deepstate: selecting test suites to enhance the robustness of recurrent neural networks. In
      Proceedings of the 44th International Conference on Software Engineering (2022), pp. 598–609.
 [66] Lu, G., Ju, X., Chen, X., Pei, W., and Cai, Z. Grace: Empowering llm-based software vulnerability detection with graph structure and
      in-context learning. Journal of Systems and Software 212 (2024), 112031.
 [67] Mahmud, Q. I., TehraniJamsaz, A., Phan, H. D., Ahmed, N. K., and Jannesari, A. Autoparllm: Gnn-guided automatic code
      parallelization using large language models. arXiv preprint arXiv:2310.04047 (2023).
 [68] Mutlu, E., Gajinov, V., Cristal, A., Tasiran, S., and Unsal, O. S. Dynamic verification for hybrid concurrent programming models.
      In Runtime Verification: 5th International Conference, RV 2014, Toronto, ON, Canada, September 22-25, 2014. Proceedings 5 (2014), Springer,
      pp. 156–161.
 [69] Nicholas, G., and Bhatia, A. Lost in translation: large language models in non-english content analysis. arXiv preprint arXiv:2306.07377
      (2023).
 [70] Nichols, D., Davis, J. H., Xie, Z., Rajaram, A., and Bhatele, A. Can large language models write parallel code? In Proceedings of the
      33rd International Symposium on High-Performance Parallel and Distributed Computing (2024), pp. 281–294.
 [71] Nichols, D., Marathe, A., Menon, H., Gamblin, T., and Bhatele, A. Modeling parallel programs using large language models. arXiv
      preprint arXiv:2306.17281 (2023).
 [72] Norris, B., and Demsky, B. Cdschecker: checking concurrent data structures written with c/c++ atomics. In Proceedings of the 2013
      ACM SIGPLAN international conference on Object oriented programming systems languages & applications (2013), pp. 131–150.
 [73] Oliinyk, Y., Scott, M., Tsang, R., Fang, C., Homayoun, H., et al. Fuzzing busybox: Leveraging llm and crash reuse for embedded bug
      unearthing. arXiv preprint arXiv:2403.03897 (2024).
 [74] OpenAI. Pricing. https://openai.com/api/pricing, 2024. [Accessed 06-June-2024].
 [75] Panichella, S. Vulnerabilities introduced by llms through code suggestions. In Large Language Models in Cybersecurity: Threats,
      Exposure and Mitigation. Springer Nature Switzerland Cham, 2024, pp. 87–97.
 [76] Pearce, H., Tan, B., Ahmad, B., Karri, R., and Dolan-Gavitt, B. Examining zero-shot vulnerability repair with large language
      models. In SP (2022), IEEE, pp. 1–18.
 [77] Pearce, H., Tan, B., Ahmad, B., Karri, R., and Dolan-Gavitt, B. Examining zero-shot vulnerability repair with large language
      models. In 2023 IEEE Symposium on Security and Privacy (SP) (2023), IEEE, pp. 2339–2356.
 [78] Phan, A. V., Le Nguyen, M., and Bui, L. T. Convolutional neural networks over control flow graphs for software defect prediction. In
      2017 IEEE 29th International Conference on Tools with Artificial Intelligence (ICTAI) (2017), IEEE, pp. 45–52.
 [79] Qin, F., Zheng, Z., Sui, Y., Gong, S., Shi, Z., and Trivedi, K. S. Cross-project concurrency bug prediction using domain-adversarial
      neural network. Journal of Systems and Software 214 (2024), 112077.
 [80] Ramos, D. A., and Engler, D. {Under-Constrained} symbolic execution: Correctness checking for real code. In 24th USENIX Security
      Symposium (2015), pp. 49–64.
 [81] Schneider, N., Hasabnis, N., Vo, V. A., Kadosh, T., Krien, N., Capota, M., Tamir, G., Willke, T. L., Ahmed, N., Pinter, Y., et al.
      Mpirigen: Mpi code generation through domain-specific language models. In Proceedings of the 2024 Workshop on AI For Systems,
      pp. 1–6.
 [82] Schreiner, M. Gpt-4 architecture, datasets, costs and more leaked. https://the-decoder.com/gpt-4-architecture-datasets-costs-and-
      more-leaked, July 2023. [Accessed 07-June-2024].
 [83] Sethi, A., Sankaran, A., Panwar, N., Khare, S., and Mani, S. Dlpaper2code: Auto-generation of code from deep learning research
      papers. In Proceedings of the AAAI Conference on Artificial Intelligence (2018), vol. 32.
 [84] Sheremetov, D., and Bitkina, A. Openai api pricing 2024: Understanding gpt-3 pricing in-depth. https://onix-systems.com/blog/how-
      much-does-it-cost-to-use-gpt-models, June 2023. [Accessed 07-June-2024].
 [85] Singh, S., Sharma, D., and Sharma, S. Dynamic verification of c11 concurrency over multi copy atomics. In 2021 International
      Symposium on Theoretical Aspects of Software Engineering (TASE) (2021), IEEE, pp. 39–46.
 [86] Sosa, R. U., Ramamurthy, K. N., Chang, M., and Singh, M. Reasoning about concepts with llms: Inconsistencies abound. In First
      Conference on Language Modeling.
 [87] Svyatkovskiy, A., Zhao, Y., Fu, S., and Sundaresan, N. Pythia: Ai-assisted code completion system. In Proceedings of the 25th ACM
      SIGKDD international conference on knowledge discovery & data mining (2019), pp. 2727–2735.
 [88] Tan, H., Luo, Q., Li, J., and Zhang, Y. Llm4decompile: Decompiling binary code with large language models. arXiv preprint


, Vol. 1, No. 1, Article . Publication date: September 2025.
Assessing Large Language Models in Comprehending and Verifying Concurrent Programs across Memory Models                                      21


      arXiv:2403.05286 (2024).
 [89] Tehrani, A., Khaleel, M., Akbari, R., and Jannesari, A. Deeprace: finding data race bugs via deep learning. arXiv preprint
      arXiv:1907.07110 (2019).
 [90] Thokair, M. A., Zhang, M., Mathur, U., and Viswanathan, M. Dynamic race detection with o (1) samples. Proceedings of the ACM
      on Programming Languages 7, POPL (2023), 1308–1337.
 [91] Tian, H., Lu, W., Li, T. O., Tang, X., Cheung, S.-C., Klein, J., and Bissyandé, T. F. Is chatgpt the ultimate programming assistant–how
      far is it? arXiv preprint arXiv:2304.11938 (2023).
 [92] Ugare, S., Suresh, T., Kang, H., Misailovic, S., and Singh, G. Improving llm code generation with grammar augmentation. arXiv
      preprint arXiv:2403.01632 (2024).
 [93] Ullah, S., Han, M., Pujar, S., Pearce, H., Coskun, A., and Stringhini, G. Llms cannot reliably identify and reason about security
      vulnerabilities (yet?): A comprehensive evaluation, framework, and benchmarks. In IEEE Symposium on Security and Privacy (2024).
 [94] Valero-Lara, P., Huante, A., Lail, M. A., Godoy, W. F., Teranishi, K., Balaprakash, P., and Vetter, J. S. Comparing llama-2 and
      gpt-3 llms for hpc kernels generation. arXiv preprint arXiv:2309.07103 (2023).
 [95] Wang, B., Xu, L., Yan, M., Liu, C., and Liu, L. Multi-dimension convolutional neural network for bug localization. IEEE Transactions on
      Services Computing 15, 3 (2020), 1649–1663.
 [96] Wang, J., Huang, Y., Chen, C., Liu, Z., Wang, S., and Wang, Q. Software testing with large language models: Survey, landscape, and
      vision. IEEE Transactions on Software Engineering (2024).
 [97] Wang, W., Nguyen, T. N., Wang, S., Li, Y., Zhang, J., and Yadavally, A. Deepvd: Toward class-separation features for neural network
      vulnerability detection. In 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE) (2023), IEEE, pp. 2249–2261.
 [98] Wang, X., Wang, Y., Wan, Y., Mi, F., Li, Y., Zhou, P., Liu, J., Wu, H., Jiang, X., and Liu, Q. Compilable neural code generation with
      compiler feedback. arXiv preprint arXiv:2203.05132 (2022).
 [99] Wang, Z., Tong, W., Li, P., Ye, G., Chen, H., Gong, X., and Tang, Z. Bugpre: an intelligent software version-to-version bug prediction
      system using graph convolutional neural networks. Complex & Intelligent Systems 9, 4 (2023), 3835–3855.
[100] Wei, Y., Xia, C. S., and Zhang, L. Copiloting the copilots: Fusing large language models with completion engines for automated
      program repair. In Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of
      Software Engineering (2023), pp. 172–184.
[101] Wen, C., Cao, J., Su, J., Xu, Z., Qin, S., He, M., Li, H., Cheung, S.-C., and Tian, C. Enchanting program specification synthesis by large
      language models using static analysis and program verification. In International Conference on Computer Aided Verification (2024),
      Springer, pp. 302–328.
[102] Wolf, F. A., Arqint, L., Clochard, M., Oortwijn, W., Pereira, J. C., and Müller, P. Gobra: Modular specification and verification
      of go programs. In International Conference on Computer Aided Verification (2021), Springer, pp. 367–379.
[103] Xia, C. S., Paltenghi, M., Le Tian, J., Pradel, M., and Zhang, L. Fuzz4all: Universal fuzzing with large language models. In Proceedings
      of the IEEE/ACM 46th International Conference on Software Engineering (2024), pp. 1–13.
[104] Xia, C. S., Wei, Y., and Zhang, L. Automated program repair in the era of large pre-trained language models. In 2023 IEEE/ACM 45th
      International Conference on Software Engineering (ICSE) (2023), IEEE, pp. 1482–1494.
[105] Xu, M., Kashyap, S., Zhao, H., and Kim, T. Krace: Data race fuzzing for kernel file systems. In 2020 IEEE Symposium on Security and
      Privacy (SP) (2020), IEEE, pp. 1643–1660.
[106] Xu, Y., Hu, L., Zhao, J., Qiu, Z., Ye, Y., and Gu, H. A survey on multilingual large language models: Corpora, alignment, and bias.
      arXiv preprint arXiv:2404.00929 (2024).
[107] Yang, A. Z., Le Goues, C., Martins, R., and Hellendoorn, V. Large language models for test-free fault localization. In Proceedings of
      the 46th IEEE/ACM International Conference on Software Engineering (2024), pp. 1–12.
[108] Yang, C., Zhao, Z., and Zhang, L. Kernelgpt: Enhanced kernel fuzzing via large language models. arXiv preprint arXiv:2401.00563
      (2023).
[109] Zhang, J., Wang, X., Zhang, H., Sun, H., Liu, X., Hu, C., and Liu, Y. Detecting condition-related bugs with control flow graph neural
      network. In Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Testing and Analysis (2023), pp. 1370–1382.
[110] Zhang, X., Muralee, S., Cherupattamoolayil, S., and Machiry, A. On the effectiveness of large language models for github
      workflows. arXiv preprint arXiv:2403.12446 (2024).
[111] Zhang, Y. Detecting code comment inconsistencies using llm and program analysis. In Companion Proceedings of the 32nd ACM
      International Conference on the Foundations of Software Engineering (2024), pp. 683–685.
[112] Zhang, Y., Yan, J., Qiao, L., and Gao, H. A novel approach of data race detection based on cnn-bilstm hybrid neural network. Neural
      Computing and Applications 34, 18 (2022), 15441–15455.
[113] Zhou, Y., Liu, S., Siow, J., Du, X., and Liu, Y. Devign: Effective vulnerability identification by learning comprehensive program
      semantics via graph neural networks. Advances in neural information processing systems 32 (2019).




                                                                                    , Vol. 1, No. 1, Article . Publication date: September 2025.
