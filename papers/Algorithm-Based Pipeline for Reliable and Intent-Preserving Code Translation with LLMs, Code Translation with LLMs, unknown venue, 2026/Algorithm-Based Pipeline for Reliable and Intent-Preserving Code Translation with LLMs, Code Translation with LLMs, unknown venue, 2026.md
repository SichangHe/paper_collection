                                              Algorithm-Based Pipeline for Reliable and Intent-Preserving
                                                            Code Translation with LLMs
                                                       Shahriar Rumi Dipto                                                   Saikat Mondal                                Chanchal K. Roy
                                              University of Saskatchewan, Canada                              University of Saskatchewan, Canada                University of Saskatchewan, Canada
                                                     rumi.dipto@usask.ca                                           saikat.mondal@usask.ca                             chanchal.roy@usask.ca

                                         ABSTRACT                                                                                        ACM Reference Format:
                                            Code translation, the automatic conversion of programs between                               Shahriar Rumi Dipto, Saikat Mondal, and Chanchal K. Roy. 2026. Algorithm-
                                                                                                                                         Based Pipeline for Reliable and Intent-Preserving Code Translation with
                                         languages, is a growing use case for Large Language Models (LLMs).
                                                                                                                                         LLMs. In 34th IEEE/ACM International Conference on Program Comprehension
                                         However, direct one-shot translation often fails to preserve pro-                               (ICPC ’26), Brazil. ACM, New York, NY, USA, 12 pages. https://doi.org/XX.
                                         gram intent, leading to errors in control flow, type handling, and I/O                          XXXX/XXXXXXX.XXXXXXX
arXiv:2602.16106v1 [cs.SE] 18 Feb 2026




                                         behavior. We propose an algorithm-based pipeline that introduces
                                         a language-neutral intermediate specification to capture these de-
                                         tails before code generation. This study empirically evaluates the                              1    INTRODUCTION
                                         extent to which structured planning can improve translation ac-                                    Reliable and intent-preserving code translation across program-
                                         curacy and reliability relative to direct translation. We conduct an                            ming languages has become a critical challenge in modern software
                                         automated paired experiment – direct and algorithm-based to trans-                              engineering (SE) [64]. Developers increasingly rely on automated
                                         late between Python and Java using five widely used LLMs on the                                 translation to reuse code, migrate legacy systems, and develop appli-
                                         Avatar and CodeNet datasets. For each combination (model, dataset,                              cations across platforms [35, 57, 58]. However, translated programs
                                         approach, and direction), we compile and execute the translated                                 often contain semantic bugs, compile-time/runtime failures, or logic
                                         program and run the tests provided. We record compilation results,                              drift, making them unreliable [43, 66]. Large-scale studies report
                                         runtime behavior, timeouts (e.g., infinite loop), and test outcomes.                            that up to 77.8% of translated programs do not compile or produce
                                         We compute accuracy from these tests, counting a translation as                                 incorrect results [43]. These failures commonly arise from improper
                                         correct only if it compiles, runs without exceptions or timeouts, and                           handling of data types, control flows, boundary conditions, or I/O
                                         passes all tests. We then map every failed compile-time and runtime                             operations, which distort the intended algorithmic behavior of the
                                         case to a unified, language-aware taxonomy and compare subtype                                  source program [27, 66]. Such faults increase debugging costs, intro-
                                         frequencies between the direct and algorithm-based approaches.                                  duce hidden defects, and reduce developer confidence in automated
                                         Overall, the Algorithm-based approach increases micro-average                                   translation pipelines [49]. As translation systems become integral
                                         accuracy from 67.7% to 78.5% (↑10.8%). It eliminates lexical and                                to software modernization [2], it is essential to mitigate these re-
                                         token errors by 100%, reduces incomplete constructs by 72.7%, and                               liability gaps. This work advances a reliability-oriented approach
                                         structural and declaration issues by 61.1%. It also substantially low-                          to LLM translation by introducing an algorithmic pipeline that
                                         ers runtime dependency and entry-point failures by 78.4%. These                                 preserves intent and reduces systematic failure modes.
                                         results demonstrate that algorithm-based pipelines enable more                                     Large Language Models (LLMs) have made code translation more
                                         reliable, intent-preserving code translation, providing a foundation                            practical and efficient by learning from large and diverse code
                                         for robust multilingual programming assistants.                                                 corpora. Despite strong fluency and generalization, recent stud-
                                                                                                                                         ies [19, 43, 66] show that LLM-translated code still suffers from
                                         CCS CONCEPTS                                                                                    frequent compilation errors and functional inconsistencies, with
                                                                                                                                         overall accuracy ranging only from 2.1% to 47.3% [43, 65].
                                         • Software and its engineering → Large Language Models; Source                                     The model often preserves the high-level algorithmic structure,
                                         code translation; Software migration; Software evolution.                                       but fails to capture critical low-level details. Slight deviations in
                                                                                                                                         type handling or I/O semantics can break an otherwise correct
                                         KEYWORDS                                                                                        algorithm. For example, when translating between languages with
                                         Automated code translation, Large Language Models, Algorithmic                                  different numeric parsing or division rules, an LLM may retain the
                                         representation, Program synthesis                                                               loop structure but alter boundary checks or off-by-one conditions.
                                                                                                                                         Similarly, input patterns that assume a particular tokenization or
                                                                                                                                         newline behavior can reorder operations or modify array dimen-
                                                                                                                                         sions, producing code that compiles but violates the intended logic
                                         Permission to make digital or hard copies of all or part of this work for personal or
                                         classroom use is granted without fee provided that copies are not made or distributed           of the source program [27, 66]. A task that should be a simple code
                                         for profit or commercial advantage and that copies bear this notice and the full citation       transfer often turns into long rounds of testing and fixing. Without
                                         on the first page. Copyrights for components of this work owned by others than the              a way to keep the original algorithm’s purpose clear during trans-
                                         author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
                                         republish, to post on servers or to redistribute to lists, requires prior specific permission   lation, teams end up with fragile code and lose trust in the process
                                         and/or a fee. Request permissions from permissions@acm.org.                                     [67]. To address this, a translation framework that first captures
                                         ICPC ’26, 2026, Brazil                                                                          a concise, language-neutral algorithm, including its inputs, data
                                         © 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM ISBN XXX-X-XXXX-XXXX-X/XXXX/XX                                                              structures, numeric rules, loop bounds, and output format, can help
                                         https://doi.org/XX.XXXX/XXXXXXX.XXXXXXX                                                         preserve intent, reduce failures, and restore reliability at scale.
ICPC ’26, 2026, Brazil                                                                                                                Dipto et al.


    Prior approaches to automated code translation fall into three        where challenges persist. In particular, we answered three research
main categories, but none explicitly enforce algorithmic intent be-       questions and made three contributions.
fore generation. First, rule-based and analysis-guided transpilers        RQ1 ) To what extent does an algorithm-based pipeline im-
[21, 26, 37, 44] encode explicit language-pair rules, but they of-        prove code translation performance relative to direct one-
ten produce non-idiomatic or unsafe code that requires extensive          shot translation? This research question examines whether adding
manual clean-up [25, 33]. This rigidity and upkeep burden make            an algorithmic step improves reliability when translations must
pure rule-based approaches ill-suited for evolving languages and          preserve control flow, type semantics, and I/O contracts. We con-
coding practices. Second, neural and unsupervised models trained          ducted paired Direct and Algorithm-based translations on Avatar
on large code corpora [49–51] outperformed traditional transpilers        and CodeNet datasets in both Python→Java and Java→Python,
on benchmark tasks but still lack subtle semantic alignment, often        recording compile success, runtime stability, and test accuracy. The
missing corner-case behaviors or misusing operators and data types.       algorithm-based approach achieved more consistent results across
Such errors indicate that purely neural approaches may generate           models, datasets, and directions, with clearer gains where structural
functionally incorrect code if the source’s intent isn’t fully captured   precision matters, improving micro-average accuracy from 67.7%
[50]. Third, LLM-centric pipelines perform post-hoc repair using          to 78.5% (↑10.8%).
test or compiler feedback, as in UniTrans [18, 64], or adopt bridge-      RQ2 ) What is the taxonomy and frequency distributions of
language strategies inspired by natural language translation, such        compile-time and runtime error types observed in each trans-
as InterTrans [17, 29, 36, 59]. However, these methods generally          lation pipeline? This research question goes beyond overall ac-
translate first and repair or route later, without explicitly enforcing   curacy to examine why translations fail, focusing on tokenization,
a compact, language-agnostic algorithm at inference time. In other        typing, indexing, imports, and program start-up or termination.
words, current LLM pipelines excel at post-hoc error correction but       We mapped each unsuccessful compile-time and runtime case to
do not inherently guarantee that the first-pass translation follows       a unified, language-aware taxonomy applied consistently across
all the source’s semantic contracts.                                      models, datasets, and directions, and computed their frequencies.
    In natural language translation, difficult language pairs are often   Parsing and Type Conversion errors dominate runtime failures
handled through a pivot language (e.g., French→English→German)            (55%) and remain the top category for both Direct and Algorithm-
[59]. This remains effective in multilingual machine translation,         based pipelines. At compile-time, Structural and Declaration Issues
where bridge languages help scale across language families without        are most frequent (54.6%), particularly in Python→Java, showing
exhaustive pairwise training [17]. Motivated by this principle, our       that the main challenge is preserving Java-style scaffolding and
work explicitly forces a language-agnostic algorithmic blueprint          highlighting the need for tighter file, class, and method templates
at inference time before final code generation. No prior work has         guided by grammar-constrained generation.
taken this inference-stage approach as a proactive safeguard for          RQ3 ) In which scenarios or code patterns does the algorithm-
semantic fidelity. Earlier systems either translate via another lan-      based pipeline reduce or eliminate specific error types com-
guage (bridging through actual code in a pivot PL) [36] or apply          pared to direct translation? This research question examines
repairs after translation [66]. By locking down the correctness of        whether a language-neutral algorithm sketch before code genera-
the algorithm upfront, our approach can then generate idiomatic           tion reduces the error modes that break fidelity in Python→Java and
code in the target language that already adheres to those invariants.     Java→Python translation. Using the same paired setup as RQ2 on
    To achieve this goal, we compared two LLM-based translation           Avatar and CodeNet, we aggregated taxonomy counts for Direct and
workflows: a direct pipeline (i.e., approach) and an algorithm-based      Algorithm pipelines and compared their frequencies. The algorithm-
pipeline that first generates a language-agnostic algorithm cap-          based approach shows clear reductions: runtime dependency and
turing I/O contracts, data structures, numeric rules, loop bounds,        entry-point errors drop from 89.2% to 10.8%, while compile-time
and output format before producing the target code. We evalu-             lexical and token errors fall from 100% to 0%, incomplete constructs
ated both translation directions using the Avatar and CodeNet             from 86.4% to 13.6%, and structural and declaration issues from
datasets with five LLMs: DeepSeek R1, DeepSeek V3, Llama 4                80.6% to 19.4%. A smaller group of errors, such as type or overload
Maverick, GPT-4o, and Qwen2.5. For each combination of model,             resolution and missing state or invalid references, persist or worsen,
dataset, approach, and direction (e.g. DeepSeek-R1 vs. Avatar vs.         showing where the algorithm helps less and where tighter semantic
Direct vs. Python→Java), we compiled the translated programs,             constraints remain needed.
executed the provided tests, and recorded three outcomes: compile         We position the algorithm-based pipeline as a general paradigm for
success/failure, runtime success/failure, and test success/failure.       reliable and intent-preserving code translation, shifting LLMs from
Failures were categorized into four groups: compile errors, runtime       token-level generation to contract-driven realization.
errors, test-only mismatches, and timeouts (e.g., infinite loop). Each
unsuccessful case was then mapped to a unified, language-aware            Replication Package can be found in our online appendix [16].
error taxonomy applied consistently across all models, datasets, and
directions. Finally, we aggregated subtype counts for both the Direct     2   MOTIVATING EXAMPLE
and Algorithm approaches, computed frequencies and percentages,              This section provides an example of how algorithm-based trans-
and marked a subtype as mitigated when the Algorithm error rate           lation prevents a common I/O pitfall in Java→Python translation.
was lower than the Direct error rate. This taxonomy-driven compar-           The Java program (see Figure 1a) first reads two numbers, then
ison reveals where the algorithm reduces specific failure modes and       reads two lists, and finally it scans those lists from the end to com-
                                                                          pute the answer. A direct Python translation breaks this contract
Algorithm-Based Pipeline for Reliable and Intent-Preserving Code Translation with LLMs                                                                     ICPC ’26, 2026, Brazil


                                    (a) Source code (Java)
                   ...                                                                                  and interpreted, while Java is statically typed and compiled. This
                   int n = input.nextInt();
                   int m = input.nextInt();                                                             difference makes translation non-trivial [28], requiring models to
                   ...
                   for (int i = 0; i < n; i++) req.add(input.nextInt());                                bridge structural, syntactic, and semantic differences. By evaluating
                   for (int i = 0; i < m; i++) pre.add(input.nextInt());
                   ...
                                                                                                        both directions on Avatar and CodeNet with the same automated
                                                                                                        evaluation pipeline for compilation, execution, and testing, we
   (b) Python code directly generated from   ... (c) Algorithm generated from source code               assessed how well LLMs handle cross-paradigm translation and
                source code                  Variables:
 data = list(map(int,
                                             ...
                                             - req: ArrayList<Integer> (size n, populated from input)
                                                                                                        structural mismatches between languages.
 input().split()))                           - pre: ArrayList<Integer> (size m, populated from input)
 n, m = data[0], data[1]                     ...
                                             Input/Output Operations:
 req = data[2:2 + n]                         - Read n and m via input.nextInt().
 pre = data[2 + n:2 + n + m]
 ...
                                             - Read n integers into req using a loop.
                                             - Read m integers into pre using a loop.                   3.2    LLM Models Used in Code Translation
                                             ...
 if req[i] > pre[j]: #IndexError here
 ...
                                             Logic Flow:
                                             1. Read n and m from standard input.                          We evaluated five top general-purpose LLMs from OpenRouter
                                             2. Populate req with n integers.
                                             3. Populate pre with m integers.
                                             ...
                                                                                                        [5], chosen to cover diverse architectures. Selection was guided
                                                                                                        by the BigCodeBench leaderboard (May 2025) [1] and OpenRouter
                                                  (d) Python code generated from algorithm              rankings (May 2025) [4], where these models appear near the top,
                                                 n, m = map(int,
                                                 sys.stdin.readline().split())                          indicating strong capabilities. Moreover, these LLMs are widely used
                                                 req = list(map(int,
                                                 sys.stdin.readline().split()))[:n]                     in many software engineering tasks such as code generation and
                                                 pre = list(map(int,
                                                 sys.stdin.readline().split()))[:m]                     code translation, where they performed promisingly [46, 62, 63].
                                                 ...                                                       ▶ DeepSeek R1 [22] is a reasoning-oriented model trained with
                                                                                                        supervised fine-tuning and multi-stage RL. We use it as a strong gen-
Figure 1: Motivating example showing how algorithm-based                                                eral baseline for structured problem solving. ▶ DeepSeek V3 [31] is
translation reduces errors compared to direct translation.                                              a large Mixture-of-Experts model with state-of-the-art open-source
                                                                                                        results on code and math, providing a top-tier reference. ▶ Llama
(see Figure 1b). It assumes all input comes on one line, builds lists
                                                                                                        4 Maverick [3] is a widely available open model not specifically
that are too short, and then Python raises IndexError (out-of-range)
                                                                                                        tuned for code, included to gauge general-purpose open-source
when it tries to access items that are not there. On the other hand,
                                                                                                        performance. ▶ GPT-4o [24] is a proprietary model with strong
the algorithm-based approach avoids this mistake (see Figure 1d).
                                                                                                        zero-shot performance in software engineering, serving as a state-
The algorithm (see Figure 1c) solved a problem of input clarity. It
                                                                                                        of-the-art commercial reference. ▶ Qwen2.5 (72B-Instruct) [47] is a
explicitly stated what to read, in what order, and how many values,
                                                                                                        high-capacity dense model with strong code and math skills and
so the code collects the exact data before any processing. Reading
                                                                                                        long-context support, serving as a competitive high-end baseline.
the counts first and then gathering exactly that many items keeps
list sizes correct, prevents out-of-bounds lookup, and makes the
downstream logic run reliably. This is a representative example                                         3.3    Translation Pipelines
of many. Therefore, a comprehensive study is required to explore
                                                                                                            To investigate the behavior of LLMs in automated code transla-
how algorithmic representations can overcome these challenges
                                                                                                        tion, we defined two parallel translation workflows: (1) Direct code
and enable more accurate and reliable code translation.
                                                                                                        translation and (2) Algorithm-based translation using a language-
                                                                                                        agnostic intermediate representation. We studied these pipelines
3     METHODOLOGY                                                                                       because direct translation is common in practice, yet it often drifts
  Figure 2 shows the overall methodology of our exploratory study.                                      on I/O operations, types, bounds, and output. While on the other
The details of each step are discussed below.                                                           hand, the algorithm-based pipeline adds a brief language-neutral
                                                                                                        algorithm to lock these details before coding, so we can test if
3.1      Dataset Preparation                                                                            it preserves intent and reduces compile or runtime failures. Both
    We evaluated on pre-processed subsets of Avatar [6] and CodeNet                                     workflows were applied to source code samples from the Avatar and
[45] curated by Pan et al. [43], widely used in recent LLM translation                                  CodeNet datasets and operated bidirectionally (Python→Java and
work [42, 66, 69]. These splits provided validated tests and clean                                      Java→Python). Each method was independently evaluated using
input–output pairs, allowing fully automated compilation and exe-                                       identical test cases and performance metrics, enabling a controlled
cution for a fair, like-for-like comparison between pipelines. Avatar                                   comparison between translation strategies.
is a parallel corpus of aligned Java-Python solutions for competitive                                       We used step-by-step, chain-of-thought prompting [56] to make
programming, ideal for a translation task between a statically and                                      the model reason through the task rather than copy surface code
a dynamically typed programming language. CodeNet is a large                                            patterns. It is well-suited to code translation in our setting because
multi-language corpus. We selected the Python and Java subsets,                                         most failures come from hidden constraints. It makes the model
with each program linked to a problem description and paired with                                       spell out these constraints before it writes code, which directly tar-
functional tests. This gives a broad coverage of algorithmic tasks                                      gets our top error sources [54]. In the Direct pipeline, the prompted
and enables automatic correctness checks.                                                               lists provide brief analysis steps but still ask the model to produce
    We focused on Python and Java in both datasets for our study                                        the target code in one pass. In the Algorithm-based pipeline, we
of cross-language code translation. These languages rank among                                          first asked for a language-agnostic algorithm, then used a second
the top four worldwide in the TIOBE index [52]. They also reflect                                       prompt to turn that algorithm into code in the target language.
different programming paradigms: Python is dynamically typed                                            Prompts were fixed across models and datasets. We evaluated only
ICPC ’26, 2026, Brazil                                                                                                                                                               Dipto et al.




                                           Translated                                                                      Successful         Accuracy and
                                          Code (Direct)                                                                    Translation     Failure Comparison Error Taxonomy
                                                                                                                                             (Direct vs. Algo-     (RQ2)
                                                                                                                                              based) (RQ1)
             Source      Large Language                                                Compilation Execution   Testing
              Code           Models

                                                                                                                              Failed     Error            Error Mitigation (Direct
                                           Generated      Large Language Translated Code
                                                                                                                            Translation Report            vs. Algo-based) (RQ3)
                                           Algorithm          Models       (Algo-based)


                                                                            Figure 2: Study Methodology

the final code (compile, runtime, tests), and the intermediate chain-                                Table 3: Prompt template used to generate code from algo-
of-thought text was stored for analysis but not graded.                                              rithm

Table 1: Prompt template used in the direct code translation                                             algorithm: <ALGORITHM>

                                                                                                         Let’s think step-by-step and generate complete, executable <TARGET_LANG>
   <SOURCE_LANG> code: <SOURCE_CODE>                                                                     code from the above algorusing the following instructions:
                                                                                                         Step 1: Analyze the algorithm requirements and identify data structures, in-
   Let’s think step-by-step and translate the above <SOURCE_LANG> code into                              put/output specifications, and core logic components
   functionally equivalent <TARGET_LANG> code using the following instruc-                               Step 2: Design the <TARGET_LANG> implementation and plan program struc-
   tions:                                                                                                ture, determine classes/functions, select appropriate data types, and language
   Step 1: Analyze the structure and identify main components, control flow, data                        constructs
   types, and dependencies                                                                               Step 3: Generate the complete code and implement logic flow with proper
   Step 2: Map <SOURCE_LANG> constructs to <TARGET_LANG> equivalents                                     syntax, add necessary imports/dependencies, handle edge cases, and ensure
   and determine required libraries                                                                      code compiles and executes correctly
   Step 3: Generate <TARGET_LANG> code preserving exact functionality, names,                            Step 4: Finally, provide only the <TARGET_LANG> code without any headers,
   logic, and program structure                                                                          comments, explanations, or examples
   Step 4: Finally, provide only the <TARGET_LANG> code without any headers,
   comments, explanations, or examples
                                                                                                              and focused the model on understanding and implementing
3.3.1 Direct Pipeline. In the direct translation approach, the                                                the intended logic. It tested the model’s ability to generate
source program (Python or Java) and a prompt (Table 1) were pro-                                              code from logical specifications rather than translating code
vided to the LLM, which generated the target-language code in a                                               line by line.
single step. This mirrors common practice, treating the LLM as a                                            • Target code generation. We then fed that algorithm back
bilingual code generator that can reuse surface cues from the source                                          to the LLM with a second prompt (Table 3) to produce code in
(e.g., variable names, data structures, control flow). This workflow                                          the target language. The model was instructed to implement
serves as the baseline for assessing one-shot source-to-target lan-                                           the specification using idiomatic syntax and types, rather
guage mapping without decomposition.                                                                          than mapping lines directly.

  Table 2: Prompt template used for algorithm generation                                              3.4      Evaluation
                                                                                                        After translation, we archived all artifacts for evaluation. For
   <SOURCE_LANG> code: <SOURCE_CODE>                                                                 each model on Avatar and CodeNet, we used the same automated
   Let’s think step-by-step and extract a detailed algorithm from the above
                                                                                                     process to compile the generated code, execute it on the dataset’s
   <SOURCE_LANG> code using the following instructions:                                              test suite, and record structured logs. From these logs, we produced
   Step 1: Identify the code structure and analyze function signatures, classes,                     summaries with accuracy, counts of compile failures, runtime fail-
   and program organization
   Step 2: Extract the core logic and trace execution flow, control structures, data
                                                                                                     ures, test case failures, and timeouts. We also kept error traces
   transformations, and I/O operations                                                               so failed runs can be mapped into our runtime and compile-time
   Step 3: Document the algorithm components and specify data types, depen-                          taxonomies. These standardized reports drive comparisons across
   dencies, and exact conditions                                                                     models, datasets, directions, and pipelines. The process is fully
   Step 4: Finally, provide only the detailed algorithm without any headers, com-
   ments, explanations, or examples                                                                  automated and performed independently for every combination
                                                                                                     defined by model, dataset, approach (Direct or Algorithm-based),
                                                                                                     and translation direction (Python→Java or Java→Python). A trans-
3.3.2 Algorithm-Based Pipeline. This approach separated rea-
                                                                                                     lation was considered correct only when it compiled successfully,
soning from code generation to test if an explicit algorithm step
                                                                                                     executed without exceptions or timeouts, and passed all test cases.
improves reliability and correctness. The workflow has two stages:
                                                                                                     These results provided consistent measures of compilation success,
     • Algorithm extraction. We designed a structured prompt                                         runtime stability, and functional correctness across combinations.
       (Table 2) through several iterations to guide the LLM in
       producing a step-by-step, language-agnostic algorithm that                                     3.4.1 Performance Comparison: Direct Vs. Algorithm-Based
       captures the program’s logic, including control flow, data                                     Translation (RQ1). For each combination, we reported the total
       operations, and I/O handling. This design reduced ambiguity                                    number of instances, the number of correct translations, and the
Algorithm-Based Pipeline for Reliable and Intent-Preserving Code Translation with LLMs                                                               ICPC ’26, 2026, Brazil


failures divided into four broad categories: (1) compile-time error                      precedence rule (compile-time before runtime) that fits our scenario,
(build fail due to syntax/imports/type issues), (2) runtime error                        avoiding double-counting and keeping labeling consistent in both
(program crashes or raises an exception while running), (3) test-                        Python→Java and Java→Python directions.
case failure (program runs but produces incorrect outputs on tests),                         For each approach (Direct and Algorithm), we counted the num-
and (4) timeout (program does not terminate within the time limit).                      ber of failures in each compile-time and runtime subtype and re-
This provided the top-level accuracy and failure profile used for                        ported both frequencies and percentages. For frequency, we com-
cross-combination comparisons.                                                           puted the grand-level proportions by summing raw counts across
   In addition to per-combination reporting, we computed a micro-                        all combinations and then normalizing by the corresponding grand
averaged translation accuracy by pooling all instances across mod-                       totals. Let C be the set of all combinations (model, dataset, approach,
els, datasets, directions, and approaches to summarize overall per-                      and direction). For each runtime subtype RE𝑘 ∈ {RE1, . . . , RE6 }, let
formance across the entire evaluation set. Micro-averaging is widely                     𝑛 RE𝑘 (𝑐) denote its count in combination 𝑐, treating cells marked
used to produce a single headline score over heterogeneous groups                        “×” as zero. The grand total for runtime and the overall frequency
[15, 53]. We adopted the same pooling idea, but applied it to correct                    of subtype RE𝑘 are
vs. incorrect outcomes in code translation rather than per-label F1.                                            6                       Í
                                                                                                                                         𝑐 ∈ C 𝑛 RE𝑘 (𝑐)
                                                                                                          ∑︁ ∑︁
   Let C be the set of all combinations (model, dataset, approach,                                 𝑁 RE =          𝑛 RE𝑘 (𝑐),    𝑓RE𝑘 =                  .   (2)
and direction), and for each combination 𝑐 ∈ C let 𝑁𝑐 denote the                                          𝑐∈C
                                                                                                                                              𝑁 RE
                                                                                                                 𝑘=1
number of instances and 𝐾𝑐 the number of correct translations.                           We applied the same procedure at compile-time. For each compile
For any subset of combinations 𝑆 ⊆ C (e.g., all Direct runs or all                       subtype CE 𝑗 ∈ {CE1, . . . , CE7 } with counts 𝑛 CE 𝑗 (𝑐), the grand total
Algorithm runs), the micro-average accuracy is                                           and frequencies are
                                                                                                               7                         Í
                                                                                                                                           𝑐 ∈ C 𝑛 CE 𝑗 (𝑐)
                                        Í
                                              𝐾𝑐                                                        ∑︁ ∑︁
                         Accmicro (𝑆) = Í𝑐 ∈𝑆 .                              (1)                 𝑁 CE =           𝑛 CE 𝑗 (𝑐),    𝑓CE 𝑗 =                    .   (3)
                                         𝑐 ∈𝑆 𝑁𝑐                                                        𝑐 ∈ C 𝑗=1
                                                                                                                                                𝑁 CE
We used this pooled measure for two reasons: (i) it reflects the
                                                                                         This approach yields a single, combination-agnostic distribution
probability that a randomly drawn instance from the full workload
                                                                                         for runtime and compile-time failures, without averaging per-row
is translated correctly (deployment-oriented view), and (ii) it re-
                                                                                         percentages.
spects size imbalance across combinations (large cells contribute
proportionally more evidence than small cells), avoiding the equal-                      3.4.3 Scenario and Pattern-Based Error Reduction Analysis
weighting bias of macro-averages.                                                        (RQ3). To understand where the algorithm helps, we compared the
                                                                                         aggregate frequency of each taxonomy subtype 𝑡 between Direct
3.4.2 Error Taxonomy and Frequency Analysis (RQ2). All                                   and Algorithm across all combinations (all models, datasets, and
unsuccessful translations in the compile-time and runtime buck-                          directions).
ets were mapped to a consistent taxonomy of subtypes appropri-                                                                                      algo
                                                                                            Let C be the set of combinations. Let 𝑛𝑡direct (𝑐) and 𝑛𝑡 (𝑐) denote
ate to the target language, and the same definitions were applied
                                                                                         the raw counts of failures labeled as type 𝑡 in combination 𝑐 under
uniformly across models, datasets, and directions. To build this
                                                                                         the direct and algorithm approaches, respectively. Then,
taxonomy in a reproducible way, we used well-established qualita-                                             ∑︁                                   ∑︁ algo
tive methods. We discovered and refined categories with thematic                            countdirect (𝑡) =     𝑛𝑡direct (𝑐), countalgo (𝑡) =        𝑛𝑡 (𝑐),
analysis and the constant comparative method by coding failures,                                                 𝑐∈C                                    𝑐∈C
comparing similar cases, and merging or splitting categories as                                        countall (𝑡) = countdirect (𝑡) + countalgo (𝑡).
needed [7, 13]. To keep the process rigorous for software engineer-
                                                                                         The reported percentages are,
ing data, we followed codebook-based content analysis guidelines
by writing a clear codebook with inclusion and exclusion rules,                                                 countdirect (𝑡)                    countalgo (𝑡)
                                                                                               𝑝 direct (𝑡) =                   ,   𝑝 algo (𝑡) =                 .     (4)
short definitions, and direction-aware examples for each runtime                                                 countall (𝑡)                       countall (𝑡)
and compile-time category, following Cruzes et al.’s guideline [14].                     A taxonomy type is considered mitigated when 𝑝 Algo (𝑡) is signifi-
Two annotators led this process. They first drafted the codebook,                        cantly lower than 𝑝 Direct (𝑡) (with the accompanying drop in raw
then ran a small pilot in which both independently labeled the                           frequency). This analysis was performed separately for compile-
same failures ("double-coding") to test clarity and consistency. They                    time and runtime subtypes.
discussed and resolved disagreements and then froze the taxon-
omy before labeling the entire set, following standard practice                          4     STUDY FINDINGS
for category stability [30]. After the pilot, the annotators refined
                                                                                           In this section, we present the findings of our study based on
the codebook, re-coded the pilot items, and then labeled the full
                                                                                         both quantitative and qualitative analyses.
dataset independently. Each failed translation receives one label
at the earliest failure stage. We report inter-rater reliability using
Cohen’s kappa and interpret it with accepted thresholds [8, 12].
                                                                                         4.1    Answering RQ1: Effective Performance of
In our study, the double-coded subset reached substantial agree-                                Algorithm-based Approach
ment (Cohen’s kappa = 89.3%), exceeding the commonly accepted                               Figure 3 represents the accuracy comparison, and Table 4 presents
70% threshold [8], and the remaining disagreements were resolved                         the error profile for every model, dataset, and direction in both
through discussion and agreement. Finally, we applied a simple                           pipelines (direct vs. algorithm-based). We evaluated whether adding
ICPC ’26, 2026, Brazil                                                                                                                                  Dipto et al.




Figure 3: Accuracy comparison of Direct vs Algorithm-based (Algo.) approaches across models and datasets for both translation
directions. Total per combination: Avatar (Python→Java): 𝑁 =250, Avatar (Java→Python): 𝑁 =249, CodeNet (Python→Java,
Java→Python): 𝑁 =200.
Table 4: Failure profile for Direct vs. Algo. across models,                              CodeNet (Java→Python), reflecting its ability to turn a precise spec-
datasets, approach and translation directions. RE = Run-                                  ification into consistent code. DeepSeek V3 improves across every
time error rate, CE = Compile-time error rate, TF = Test                                  combination, but with narrower margins, suggesting a solid direct
fail rate, TO = Timeout. Totals per combination: Avatar                                   baseline that still benefits from explicit contracts. GPT-4o changes
(Python→Java): 𝑁 =250, Avatar (Java→Python): 𝑁 =249, Co-                                  little on Python→Java because its direct baseline is already high,
deNet (Python→Java, Java→Python): 𝑁 =200. All values are                                  yet it gains on Java→Python where an algorithm helps preserve
in %.                                                                                     parsing discipline and loop bounds. When the algorithm is concrete,
                                                                                          Qwen2.5 helps by abstracting away token cues like identifiers or
                                          Python→Java              Java→Python            specific I/O idioms; accuracy can drop. Overall, the algorithm pays
 Model               Dataset   Appr.    RE    CE    TF     TO    RE     CE    TF    TO    off for typing and I/O-Intensive tasks, letting the model lock in data
                     Avatar
                               Direct 19.2 16.8     10      0    8.4    3.2 11.2    0     shapes, numeric rules, and output formats.
                               Algo.  8.8 0.8       12     0.4    8      0   5.6    0         The same pattern appears in the error breakdown. The algo-
 DeepSeek R1
                               Direct   6.5    9     0     0     10     5     12    0     rithm reduces Java-side compile breaks by making setup explicit.
                     CodeNet
                               Algo.     1    0.5   0.5    0      7     0     0.5   0
                                                                                          DeepSeek R1 cuts compile errors on Python→Java from 16.8% to
                               Direct   8.8   14.4 17.2    0.8   24.9   2     7.6    0
                     Avatar
                               Algo.    10     0.8 14      0.8   12.1   0     4.8   0.8
                                                                                          0.8%, and DeepSeek V3 similarly drops from 14.4% to 0.8%. Llama’s
 DeepSeek V3                                                                              big problem in Avatar (Python→Java) is runtime instability, which
                               Direct   2.5    6    1.5    0     34.5 1       0.5    0
                     CodeNet                                                              the algorithm reduces from 50.4% to 10.8% by specifying input
                               Algo.    0.5    2    0.5    0     27.5 0.5      0    0.5
                               Direct 50.4    1.2   11.6    0    18.5 6.4 18.5       0    parsing and loop bounds. Across Java→Python, compile errors of-
                     Avatar
 Llama 4 Maverick
                               Algo. 10.8     2.4    16    0.4   15.7 0.4 10        1.2   ten vanish for DeepSeek R1 and DeepSeek V3 once the algorithm
                     CodeNet
                               Direct   37    1.5   3.5    0     19.5 3.5     28     0    removes type and entry-point assumptions. Runtime crashes fall
                               Algo.    4.5    1     7     0     26.5 1.5     6.5   0.5   when the algorithm names the input contract and numeric rules, for
                               Direct   9.6   1.6   20.4   0.4   15.3   0     7.2   0     example GPT-4o on CodeNet drops from 28% to 20% and DeepSeek
                     Avatar
                               Algo.    10    2.4   19.2   0.4   12.1   0     7.2   0
 GPT-4o                                                                                   V3 on CodeNet from 34.5% to 27.5%. Residual failures cluster around
                               Direct   0.5    1     2     0     28     0     1.5   0
                     CodeNet
                               Algo.    0.5   2.5    1     0     20     0     0.5   0     parsing and conversion in Python targets, where tokenization and
                               Direct 14.4    5.6   19.2   0.4   16.1 0       10    0.8
                                                                                          end-of-file handling are still easy to get wrong if the algorithm is
                     Avatar                                                               not specific. Test-only mismatches usually decline when the algo-
                               Algo. 14.4     7.6   20.4   0.4   18.1 2.4     8.8   1.6
 Qwen2.5
                               Direct   2.5    4    4.5    0     29      1    5.5   0.5   rithm fixes output ordering and separators, though a few trade-offs
                     CodeNet
                               Algo.     2    5.5   1.5    0     29     1.5    4     0    arise in which stricter compile-time or runtime checks surface
                                                                                          new, smaller issues. Overall, the algorithm helps most by remov-
an explicit algorithm before generation improves translation qual-                        ing avoidable setup and I/O mistakes, leaving a smaller core of
ity. Overall, the algorithm-based workflow reduces compile-time                           input parsing and coercion problems that future constraints and
and runtime failures, with the largest gains in cases that stress                         lightweight validators can address.
input/output (I/O) handling and typing.                                                       Which approach is better: The algorithm-based pipeline is the
   The algorithm step lifts accuracy most where models benefit                            reliable choice overall. It gives the biggest accuracy gains for Llama 4
from committing to structure and I/O rules before emitting code.                          Maverick and DeepSeek R1, steady gains for DeepSeek V3, and clear
Llama 4 Maverick shows the largest gains on Python→Java, moving                           benefits for GPT-4o when the target is Python. Qwen2.5 is mixed
from 36.8% to 70.4% on Avatar and from 58% to 87.5% on CodeNet,                           and depends on the dataset. On errors, the algorithm most reliably
because the algorithm fixes type errors, loop bounds, and print for-                      avoids Java-side compile failures and often reduces runtime crashes
matting, which the direct translation often mishandles. DeepSeek                          when I/O and type errors matter. A few models drop slightly when
R1 also improves strongly in all four settings, for example, from                         the algorithm removes token-level cues they relied on. Overall, a
54% to 78% on Avatar (Python→Java) and from 73% to 92.5% on
Algorithm-Based Pipeline for Reliable and Intent-Preserving Code Translation with LLMs                                                       ICPC ’26, 2026, Brazil


                                                                                         4.2    Answering RQ2: Error Taxonomy and
                                                                                                Frequency Distribution Observed in Each
                                                                                                Combination
                                                                                            In our experiments, translated programs fail in four ways: run-
                                                                                         time errors, compile-time errors, test failures, and timeouts. Time-
                                                                                         outs are very rare, so we left them out. Test results show a clear
                                                                                         pattern. For Python→Java, direct and algorithm-based pipelines
                                                                                         have similar test-fail rates. For Java→Python, the algorithm-based
                                                                                         pipeline fails fewer tests than the direct one. This suggests that
                                                                                         moving from a statically typed language to a dynamically typed
                                                                                         one benefits from an explicit algorithm step, which helps keep the
                                                                                         intended behavior and output format. Since tests serve as external
                                                                                         judges rather than diagnosing specific error types, they do not fit
                                                                                         an error taxonomy. We analyzed compile-time and runtime failures,
                                                                                         mapped them to language-aware subtypes, reported frequencies for
                                                                                         both pipelines, and compared subtypes to see where the algorithm
                                                                                         reduces errors.
                                                                                            Constructing and analyzing the error taxonomy: We grouped
                                                                                         failures into two taxonomies: runtime and compile-time. Each group
                                                                                         is a type of mistake, not a specific diagnosis. The definitions work
                                                                                         for both Python→Java and Java→Python (Figure 4).
                                                                                            For runtime failures, Dependency & Entry-Point means the pro-
                                                                                         gram cannot start or cannot find what it needs. Parsing & Type
                                                                                         Conversion covers input reading and value conversion when I/O
                                                                                         styles or number rules differ. Index/Key Access covers out-of-range
         Figure 4: Error Taxonomy of Both Languages                                      indexes and missing keys as bounds or map rules change. Miss-
                                                                                         ing State & Invalid Reference means a value is unset, out of scope,
brief language-agnostic algorithm before code translation improves                       not yet built, or the target blocks the operation. Arithmetic Errors
structure and semantics, leading to fewer compile breaks, fewer                          covers illegal or unstable numeric work, including overflow and
runtime crashes, and fewer test-only mismatches.                                         underflow. Resource Exhaustion covers unbounded recursion or
Overall micro-average accuracy. We summarize each pipeline                               growth that drains memory or the stack.
with a pooled metric following Eq.1: For Direct,                                            For compile-time failures, Import/Namespace Resolution indi-
                                                                                         cates that packages or symbols are missing, with similar issues
                                           3043                                          sometimes appearing later in dynamic targets. Lexical & Token cov-
                    Accmicro (𝑑𝑖𝑟𝑒𝑐𝑡) =         = 67.7%,
                                           4495                                          ers scanner errors such as illegal characters or unexpected tokens.
   For Algorithm,                                                                        Incomplete constructs mean unterminated or half-formed syntax
                                                                                         when delimiters do not match. Structural & Declaration Issues cover
                                          3530
                     Accmicro (𝑎𝑙𝑔𝑜) =         = 78.5%.                                  broken class, function, or module shapes, or missing required parts
                                          4495                                           under stricter rules. Type/Overload Resolution means the compiler
   Thus, Algorithm improves the overall micro-average by                                 cannot match types or pick a method or a constructor. Literal Con-
                                                                                         straints covers invalid literal forms or ranges. Others is a small
                     Δmicro = 78.5% − 67.7% = 10.8%                                      catch-all for all residual diagnostics.
These pooled results support the earlier findings: the algorithm-                           These cause-based definitions support consistent aggregation
based approach is more balanced across models, datasets, and di-                         (calculated by Eq. 2 and Eq. 3) across models, datasets, and directions
rections, with clearer gains when precise control flow, typing, and                      (Table 5) and set up the error reduction analysis that follows.
I/O contracts matter.                                                                       Runtime failures: For an overall view, we combined Avatar and
   Best-performing model: DeepSeek R1 is the strongest overall                           CodeNet when counting failures. Across models, Parsing & Type
with the algorithm-based pipeline. It reaches the highest accuracy                       Conversion Issues (RE2) are the main runtime problem. DeepSeek
in all four settings and shows a balanced error profile, with compile                    R1 is typical here: RE2 is its largest bucket with 77 cases, well above
failures near zero, runtime failures down, and test failures low. It                     any other category for that model. DeepSeek V3 shows the same
outperforms other models because it is a reinforcement-learned rea-                      pattern with 205 RE2 cases, which confirms that parsing inputs and
soning model, architecturally a high-capacity MoE, and empirically                       coercing types are the hardest runtime steps. Llama 4 Maverick is
strong in code and math [22], so it faithfully follows the algorithm                     the outlier. Its largest bucket is Dependency & Entry-Point Issues
and emits stable idiomatic target scaffolds. This combination of a                       (RE1) with 177 cases, which reflects frequent start-up and pack-
clear algorithm and stable code generation explains its consistent                       aging mistakes. GPT-4o again aligns with the majority, with 152
wins across datasets and directions.                                                     in RE2, while Qwen2.5 is also parsing-led with 157 in RE2 and a
ICPC ’26, 2026, Brazil                                                                                                                                                      Dipto et al.


Table 5: Error Frequency by Taxonomy (RE1 = Dependency & Entry-Point Issues, RE2 = Parsing & Type Conversion Issues, RE3 = Index/Key
Access Issues, RE4 = Missing State & Invalid Reference, RE5 = Arithmetic Errors, RE6 = Resource Exhaustion, CE1 = Import/Namespace
Resolution, CE2 = Lexical & Token Errors, CE3 = Incomplete Constructs, CE4 = Structural & Declaration Issues, CE5 = Type/Overload Resolution
Errors, CE6 = Literal Constraints, CE7 = Others).

                                                                          Runtime Error                                           Compile-time Error
              Model              Dataset   Appr.          Python→Java                 Java→Python                    Python→Java                    Java→Python
                                                    RE1 RE2 RE3 RE4 RE5 RE6 RE1 RE2 RE3 RE4 RE5 RE6 CE1 CE2 CE3 CE4 CE5 CE6 CE7 CE1 CE2 CE3 CE4 CE5 CE6 CE7
                                           Direct   35   6    3   1   2     1    ×   14   4   ×    ×     3   ×   ×   4   38   ×    ×   ×    ×   ×      1   7    ×   ×   ×
                                 Avatar
                                           Algo.    4    13   3   1   1     ×    ×   15   2   ×    ×     3   ×   ×   ×   1    ×    ×   1    ×   ×      ×   ×    ×   ×   ×
              DeepSeek R1
                                           Direct   12   ×    ×   1   ×     ×    ×   16   4   ×    ×     ×   ×   ×   ×   18   ×    ×   ×    ×   1      3   6    ×   ×   ×
                                 CodeNet
                                           Algo.    1    ×    ×   1   ×     ×    ×   13   1   ×    ×     ×   ×   ×   ×   ×    ×    1   ×    ×   ×      ×   ×    ×   ×   ×
                                           Direct   ×    15   2   2   ×     3    ×   53   2   4    ×     3   4   9   2   17   1    1   2    ×   ×      2   3    ×   ×   ×
                                 Avatar
                                           Algo.    3    15   3   4   ×     ×    4   20   ×   4    ×     2   ×   ×   ×   1    1    ×   ×    ×   ×      ×   ×    ×   ×   ×
              DeepSeek V3
                                           Direct   1    2    ×   2   ×     ×    2   51   3   12   ×     1   3   5   ×   3    ×    1   ×    ×   ×      ×   2    ×   ×   ×
                                 CodeNet
                                           Algo.    ×    ×    ×   1   ×     ×    ×   49   3   3    ×     ×   3   ×   ×   ×    ×    1   ×    ×   ×      ×   1    ×   ×   ×
                                           Direct   105 7     5   3   1     5    1   31   5   7    ×     2   1   ×   ×   ×    2    ×   ×    ×   ×      ×   16   ×   ×   ×
                                 Avatar
                                           Algo.    ×   12    7   6   ×     2    3   27   6   1    ×     2   3   ×   1   1    1    ×   ×    ×   ×      ×   1    ×   ×   ×
              Llama 4 Maverick
                                           Direct   68 ×      1   1   ×     4    ×   30   3   6    ×     ×   ×   ×   3   ×    ×    ×   ×    ×   ×      3   4    ×   ×   ×
                                 CodeNet
                                           Algo.    ×   ×     1   7   ×     1    ×   38   4   10   1     ×   ×   ×   1   1    ×    ×   ×    ×   ×      ×   3    ×   ×   ×
                                           Direct   ×    15   5   1   ×     3    ×   27   3   5    ×     3   2   ×   ×   ×    1    ×   1    ×   ×      ×   ×    ×   ×   ×
                                 Avatar
                                           Algo.    ×    15   4   3   ×     3    1   23   1   2    ×     3   1   ×   1   3    1    ×   ×    ×   ×      ×   ×    ×   ×   ×
              GPT-4o
                                           Direct   ×    ×    ×   1   ×     ×    ×   44   6   6    ×     ×   ×   ×   ×   ×    2    ×   ×    ×   ×      ×   ×    ×   ×   ×
                                 CodeNet
                                           Algo.    ×    ×    ×   1   ×     ×    ×   28   4   8    ×     ×   3   ×   ×   ×    2    ×   ×    ×   ×      ×   ×    ×   ×   ×
                                           Direct   5    16   6   6   ×     3    ×   20   4   10   3     3   9   ×   ×   ×    2    2   1    ×   ×      ×   ×    ×   ×   ×
                                 Avatar
                                           Algo.    3    17   3   9   ×     4    7   18   1   14   ×     5   3   ×   ×   4    9    ×   3    ×   ×      ×   6    ×   ×   ×
              Qwen2.5
                                           Direct   2    ×    ×   3   ×     ×    ×   44   4   9    1     ×   2   ×   1   ×    1    1   3    ×   ×      ×   2    ×   ×   ×
                                 CodeNet
                                           Algo.    ×    1    ×   2   ×     1    2   41   1   13   1     ×   2   ×   ×   3    3    ×   3    ×   ×      ×   3    ×   ×   ×



secondary concentration in Missing State & Invalid Reference (RE4)                                 Index or Key Access 7.8%, RE6 Resource Exhaustion 4.5%, and RE5
(66). Across all models, RE2 dominates with 736 cases, followed by                                 Arithmetic 0.8%. For compile-time failures, Structural & Declaration
RE1 (259) and RE4 (170). These patterns suggest that most models                                   Issues (CE4, 54.6%) lead, reflecting malformed class or method scaf-
first struggle with reading and correctly converting inputs, while                                 folding or missing declaration elements under stricter target rules
some additionally attempt to bootstrap the program and identify                                    (for example, return types, braces or semicolons, class headers).
dependencies.                                                                                      The second most common is Import or Namespace Resolution (CE1,
   Compile-time failures: When we combined datasets, Struc-                                        13.6%), which points to unresolved packages or symbols during
tural & Declaration Issues (CE4) are the leading compile-time failure                              the build. Other compile groups occur at lower rates: CE5 Type or
across models. DeepSeek R1 shows the clearest example with 70                                      Overload Resolution 9.9%, CE3 Incomplete Constructs 8.3%, CE2
CE4 cases, indicating frequent problems with required declarations                                 Lexical and Token Errors 5.7%, CE7 Others 5.3%, and CE6 Literal
or program structure in the target language. DeepSeek V3 also                                      Constraints 2.7%.
concentrates on CE4 (27) with a secondary presence of Lexical &
Token Errors (CE2). Llama 4 Maverick follows the same pattern
with 26 in CE4 and far fewer elsewhere. GPT-4o is different: its com-                              4.3       RQ3: Scenario and Pattern-Specific Error
pile breaks are mostly Import/Namespace Resolution (CE1) with 6                                              Mitigation by Algorithm-based Approach
cases, consistent with a strong syntax baseline that still stumbles                                   For the subsequent analysis, we computed the aggregate fre-
on package setup. Qwen2.5 spreads across CE4 (18), CE1 (16), and                                   quency of each taxonomy subtype using Eq.4.
Type/Overload Resolution (CE5, 15), suggesting a mix of structure,                                    The algorithm-based translation mitigates several runtime error
imports, and typing issues. Aggregated across all models, CE4 is                                   categories relative to Direct (see Figure 5a). The clearest gain is
the clear headliner with 144 cases, followed by CE1 (36), CE5 (24),                                in Dependency & Entry-Point Issues, which fall from 231 of 259
and CE3 (22). Overall, these results indicate that many compile                                    (89.2%) under Direct to 28 of 259 (10.8%) under Algorithm, indicating
failures come from not meeting the target language’s structural and                                that an explicit algorithm clarifies program startup configuration
declaration rules, while import resolution and typing are the next                                 and required dependencies. Parsing & Type Conversion Issues also
most common pain points.                                                                           improve from 391 of 736 (53.1%) to 345 of 736 (46.9%)-as the al-
   Overall, the table 5 shows that runtime failures are dominated by                               gorithm specifies input formats and value coercions that stabilize
Parsing & Type Conversion (RE2, 55%), which signals breakdowns                                     execution-time parsing. Index/Key Access Issues dropped from 60
in input handling and numeric coercion when language I/O idioms                                    of 104 (57.7%) to 44 of 104 (42.3%), consistent with the algorithm
differ (for example, whitespace or tokenization rules, int or float                                making bounds and access patterns explicit. Resource Exhaustion
parsing, integer division). The next most frequent is Dependency &                                 declines from 34 of 60 (56.7%) to 26 of 60 (43.3%), likely because the
Entry-Point (RE1, 19.3%), indicating programs that cannot start or                                 algorithm emphasizes termination conditions and growth limits.
locate required components after translation (for example, missing                                 Arithmetic Errors decrease from 7 of 10 (70%) to 3 of 10 (30%) when
main, package, or module wiring). The remaining runtime groups                                     numeric rules are stated up front. One category does not mitigate:
appear less often: RE4 Missing State & Invalid Reference 12.7%, RE3                                Missing State & Invalid Reference rises from 80 of 170 (47.1%) to 90
Algorithm-Based Pipeline for Reliable and Intent-Preserving Code Translation with LLMs                                                      ICPC ’26, 2026, Brazil




Figure 5: Algorithm-based vs Direct: per-type error mitigation (RE1 = Dependency & Entry-Point Issues, RE2 = Parsing & Type
Conversion Issues, RE3 = Index/Key Access Issues, RE4 = Missing State & Invalid Reference, RE5 = Arithmetic Errors, RE6 = Resource
Exhaustion, CE1 = Import/Namespace Resolution, CE2 = Lexical & Token Errors, CE3 = Incomplete Constructs, CE4 = Structural & Declaration
Issues, CE5 = Type/Overload Resolution Errors, CE6 = Literal Constraints, CE7 = Others).

of 170 (52.9%), suggesting that the added structure introduced by                        reduced dependency and entry-point failures by 78.4% and cut
the algorithm can expose initialization and scoping slips that were                      runtime instability by over 50%. Clear separation of compile-time,
less frequent under Direct.                                                              runtime, and test-failure stages accelerates regression diagnosis
   At compile-time, algorithm-based translation markedly reduces                         and makes model replacement safer, since validators remain stable
syntax- and structure-sensitive failures (Figure 5b). Lexical & Token                    even if backend models change. The small planning overhead pays
Errors collapse from 15 of 15 (100%) under Direct to 0 of 15 (0%)                        back through lower defect density and faster recovery.
under Algorithm, showing that the algorithm enforces well-formed                            For LLM and systems researchers. Remaining issues stem
tokens. Incomplete constructs dropped from 19 of 22 (86.4%) to 3 of                      from weak enforcement of semantic constraints such as type reso-
22 (13.6%), reflecting clearer delimiter and block completion. Struc-                    lution and initialization scope. Future work should make algorithms
tural & Declaration Issues shrink from 116 of 144 (80.6%) to 28 of                       machine-checkable and integrate lightweight analyzers (type-width,
144 (19.4%) as the algorithm prescribes class/function skeletons and                     indexing, and output-format checks). Controlled ablations in which
required signatures. Import/Namespace Resolution improves more                           constraints are toggled can reveal which constraints contribute
modestly-from 21 of 36 (58.3%) to 15 of 36 (41.7%)-indicating partial                    most to reliability. Combining algorithm-guided generation with
standardization of imports with some environment-specific gaps re-                       lightweight validation offers a practical path toward fully reliable,
maining. Literal Constraints also improve, from 5 of 7 (71.4%) to 2 of                   intent-preserving multilingual code translation.
7 (28.6%), as the algorithm nudges literals toward target-legal forms.
Two categories do not exhibit any reduction: Type/Overload Resolu-
tion Errors increase from 9 of 26 (34.6%) to 17 of 26 (65.4%), implying
                                                                                         6   THREATS TO VALIDITY
that the algorithm’s more explicit APIs surface mismatches earlier
at compile-time, and Others remain unchanged at 7 of 14 (50%)                               Threat to external validity concerns the generalizability of our
under both approaches.                                                                   results. We used Python and Java as representative high-contrast
                                                                                         languages with dynamic and static typing to capture common trans-
                                                                                         lation challenges. Although the evaluation focused on this pair, the
5    IMPLICATIONS                                                                        framework is language agnostic and can generalize to other lan-
    For practitioners and tool builders. Teams should adopt an                           guage combinations with suitable prompt and test adaptations.
algorithm-based workflow for translation rather than a one-shot                             Threats to construct validity concern whether our measures cap-
approach. Empirically, this step improved overall accuracy by 10.8%                      ture the intended constructs of translation failure. Error types were
(67.7% to 78.5%), eliminated all lexical and token errors, and re-                       assigned manually, which introduced measurement subjectivity. We
duced incomplete constructs by 72.7% and structural or declaration                       mitigated this with a written codebook that mentions inclusion and
faults by 61.1%. These gains translate to fewer compile breaks and                       exclusion rules and direction-aware examples, a pilot double-coding
runtime crashes that would otherwise require manual debugging.                           pass, and precedence rules to avoid double-counting. Inter-rater
Developers should first prompt the model to produce a concise                            agreement on the double-coded subset is Cohen’s kappa = 0.893,
algorithm covering six items: (i) input handling, (ii) data structures,                  and any remaining disagreements were resolved by discussion.
(iii) numeric rules, (iv) index bases and loop bounds, (v) termina-                      These steps helped to ensure that the taxonomy is interpretable
tion, and (vi) output format. Treat this as a checklist–reject any                       and applied consistently.
plan that omits an item. Although generating this intermediate                              Threats to internal validity concern whether observed differences
algorithmic plan adds one extra model call, results show it removes                      actually arise from the algorithm step rather than from prompts,
most preventable errors and lowers post-translation debugging and                        decoding settings, or randomness. We fixed prompts and decoding
maintenance costs.                                                                       parameters for each condition, scripted the entire workflow, graded
    For engineering practice at scale. Run translation as a de-                          only the final code in both pipelines, standardized toolchains, and
terministic pipeline rather than a single LLM call. Keep algorithm                       kept full logs. Some randomness can still occur. We reduced it by
plans under version control, automatically validate them, and gen-                       running evaluations within a short time window and by using fixed
erate target code only after checks pass. In our study, this pipeline                    random seeds when the API allows.
ICPC ’26, 2026, Brazil                                                                                                                 Dipto et al.


   The other internal validity comes from the quality of the algo-          Intermediate Representations for Code Generation. A sec-
rithm. It helped only when the algorithm is specific. Missing ele-       ond line of work studies intermediate representations for code gen-
ments such as tokenization rules, end-of-file handling, data shapes,     eration. Chain-of-Thought prompting elicits stepwise reasoning
numeric policy, index bases, loop bounds, termination conditions,        before emitting answers [56], and Least-to-Most prompting de-
or output format can cause systematic errors. We mitigated this          composes hard tasks into simpler subproblems solved in sequence
with a fixed algorithm in the prompt (see section 3.3.2) and by re-      [68]. Program-Aided Language Models (PAL) push this idea further
jecting under-specified algorithm. This helped isolate the effect of     by asking the model to produce executable programs as interme-
planning from prompt design noise.                                       diate reasoning, offloading computation to a runtime [20], while
                                                                         Program-of-Thoughts uses structured, program-like steps to im-
                                                                         prove reliability on symbolic tasks [10]. Closer to our setting, a study
7    RELATED WORKS                                                       proposes transitive intermediate translations, routing a source pro-
   Traditional Code Translation. Early work in code translation          gram through one or more existing programming languages before
relied on program analysis with hand-crafted transformation rules        reaching the final target, and reports improved correctness when
to migrate programs between languages. In general, the literature        a direct translation struggles [36]. In contrast to transitive multi-
distinguishes two families of automated techniques: rule-based           language routes or general planning, we used a single, language-
systems and data-driven (learning-based) methods. Representa-            agnostic algorithm tailored to source-to-source translation. To our
tive rule-based tools include C2Rust [26] (translate code from C to      knowledge, no prior approach systematically leveraged a language-
Rust), CxGo [21] (translate code from C to Go), and Sharpen [37]         agnostic "natural language algorithm", something LLMs are good
& Java2CSharp [44] (translate code from Java to CSharp). How-            at generating as an intermediate step to make the semantics of the
ever, these systems are tightly coupled to each language. For ev-        code explicit before generating the actual code.
ery source-target pair, engineers must handwrite many rules for
functions, objects, and standard libraries, making the approach
difficult to scale [64]. In addition, the resulting translations often   8   CONCLUSION
lacks readability and may still exhibit correctness issues, further          Code translation with LLMs has become increasingly practical,
limiting their practical use [32, 38, 40]. Another line of work goes     but direct one-shot generation still fails to preserve low-level pro-
beyond hand-written rules and learns translation directly from data.     gram details essential to correctness. To address this, we introduced
These methods train on large code corpora, either supervised when        an algorithm-based pipeline that inserts a concise, language-neutral
parallel source-target pairs are available or unsupervised when          specification step before code generation to capture I/O behavior,
only monolingual code is available. Over time, the field has shifted     data structures, numeric rules, and loop bounds. We evaluated this
from statistical models [38, 39] to neural networks [11], then to        approach across five LLMs on Avatar and CodeNet, translating
pre-trained representations [28, 50, 51, 55, 69] and now to large        both Python→Java and Java→Python, and automatically tested
language models [36, 43, 64] reflecting a broader trend of using         each translation for compilation, runtime stability, and correctness.
scale and learned abstractions to improve accuracy and coverage.         Results show that the algorithmic step substantially improves re-
   Code Translation with LLMs. Instruction-tuned code LLMs               liability, raising the pooled micro-average accuracy from 67.7% to
trained on large, multilingual corpora now perform well on core          78.5% and reducing major failure modes: compile-time Lexical and
software engineering tasks such as code translation, summarization,      Token errors dropped to zero, Incomplete Constructs declined by
comprehension [9, 34, 41, 48] and increasingly on program repair         72.7%, Structural and Declaration issues by 61.1%, and runtime De-
[23, 60], where they can locate faults, propose patches, and validate    pendency and Entry-Point failures by 78.4%. DeepSeek R1 achieved
fixes with tests. Broad exposure to many languages helps these           the highest absolute gains, Llama 4 Maverick showed the largest rel-
models internalize syntax and common semantic patterns, enabling         ative improvement, GPT-4o benefited most on Java→Python, and
transfer across tasks and targets. At the same time, strong prompt       Qwen2.5 revealed where algorithms must be more specific. Overall,
design and minimal adaptation enable general-purpose LLMs to             these findings establish the algorithm-based pipeline as a practical
compete closely on similar benchmarks [61]. Although LLMs have           and general principle for reliable, intent-preserving code transla-
improved rapidly, their translated code remains unreliable. Many         tion with LLMs. Although the extra planning step introduces minor
open-source models score well on benchmarks but are not ready            computational overhead, it eliminates many preventable errors and
for production because they often miss the deeper semantics of a         reduces long-term debugging and maintenance costs. Future work
program [43]. Prior work tries to fix this after the fact, for exam-     will extend this framework to additional language pairs and multi-
ple, by generating synthetic test cases [64] or re-translating with      file projects, integrate property-based and semantic testing, and
compiler error messages [43, 64]. These efforts help, but they do        develop machine-checkable plan schemas for automated validation.
not directly test or strengthen the model’s understanding of the
intended computation [43, 64]. This raises a central question: How
much syntactic and semantic structure do these models preserve           ACKNOWLEDGMENTS
when translating code? Hence, unlike prior works that rely on post-         This research is supported in part by the Natural Sciences and En-
hoc fixes or prompt tweaks, we intervened an explicit algorithm          gineering Research Council of Canada (NSERC) Discovery Grants
before generation to lock I/O contracts, data structures, control        program, the Canada Foundation for Innovation’s John R. Evans
flow, and numeric rules, so the model grounds semantics before           Leaders Fund (CFI-JELF), and by the industry-stream NSERC CRE-
syntax.                                                                  ATE in Software Analytics Research (SOAR).
Algorithm-Based Pipeline for Reliable and Intent-Preserving Code Translation with LLMs                                                                      ICPC ’26, 2026, Brazil


REFERENCES                                                                                 [26] Immunant. 2025. C2Rust: Migrate C code to Rust. https://github.com/immunant/
 [1] [n. d.].           BigCodeBench Leaderboard – bigcode-bench.github.io.                     c2rust. Visited on 2025-08-27; Licensed under BSD-3-Clause.
     https://bigcode-bench.github.io/. [Accessed 13-09-2025].                              [27] Prithwish Jana, Piyush Jha, Haoyang Ju, Gautham Kishore, Aryan Mahajan, and
 [2] [n. d.]. How a single ChatGPT mistake cost us $10,000+ — asim.bearblog.dev.                Vijay Ganesh. 2023. CoTran: An LLM-Based Code Translator Using Reinforce-
     https://asim.bearblog.dev/how-a-single-chatgpt-mistake-cost-us-10000/. [Ac-                ment Learning with Feedback from Compiler and Symbolic Execution. In Euro-
     cessed 22-10-2025].                                                                        pean Conference on Artificial Intelligence. https://arxiv.org/pdf/2306.06755.pdf
 [3] [n. d.]. The Llama 4 herd: The beginning of a new era of natively multi-              [28] Mingsheng Jiao, Tingrui Yu, Xuan Li, Guanjie Qiu, Xiaodong Gu, and Beijun
     modal AI innovation-ai.meta.com. https://ai.meta.com/blog/llama-4-multimodal-              Shen. 2023. On the Evaluation of Neural Code Translation: Taxonomy and Bench-
     intelligence/. [Accessed 16-09-2025].                                                      mark. In 2023 38th IEEE/ACM International Conference on Automated Software
 [4] 2025. LLM Rankings | OpenRouter — openrouter.ai. https://openrouter.ai/                    Engineering (ASE). 1529–1541. doi:10.1109/ASE56229.2023.00114
     rankings. [Accessed 13-09-2025].                                                      [29] Yunsu Kim, Petre M. Petrov, Pavel Petrushkov, Shahram Khadivi, and Hermann
 [5] 2025. OpenRouter — openrouter.ai. https://openrouter.ai/. [Accessed 13-09-2025].           Ney. 2019. Pivot-based Transfer Learning for Neural Machine Translation be-
 [6] Wasi Uddin Ahmad, Md Golam Rahman Tushar, Saikat Chakraborty, and Kai-Wei                  tween Non-English Languages. In Conference on Empirical Methods in Natural
     Chang. 2021. AVATAR: A Parallel Corpus for Java-Python Program Translation.                Language Processing. https://api.semanticscholar.org/CorpusID:202712706
     (2021). https://api.semanticscholar.org/CorpusID:237304035                            [30] Klaus Krippendorff. 2018. Content analysis: An introduction to its methodology.
 [7] Virginia Braun and Victoria Clarke. 2006. Using thematic analysis in psy-                  Sage publications.
     chology. Qualitative Research in Psychology 3, 2 (2006), 77–101. doi:10.1191/         [31] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Cheng-
     1478088706qp063oa                                                                          gang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. 2024. Deepseek-v3
 [8] Ted Byrt et al. 1996. How good is that agreement? Epidemiology 7, 5 (1996), 561.           technical report. arXiv preprint arXiv:2412.19437 (2024).
 [9] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde                      [32] Fang Liu, Jia Li, and Li Zhang. 2023. Syntax and Domain Aware Model for Unsu-
     De Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph,               pervised Program Translation. In 2023 IEEE/ACM 45th International Conference
     Greg Brockman, et al. 2021. Evaluating large language models trained on code.              on Software Engineering (ICSE). 755–767. doi:10.1109/ICSE48619.2023.00072
     arXiv preprint arXiv:2107.03374 (2021).                                               [33] Yuchen Liu, Junhao Hu, Yingdi Shan, Ge Li, Yanzhen Zou, Yihong Dong, and Tao
[10] Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W. Cohen. 2022. Pro-                      Xie. 2025. LLMigrate: Transforming" Lazy" Large Language Models into Efficient
     gram of Thoughts Prompting: Disentangling Computation from Reasoning for                   Source Code Migrators. arXiv preprint arXiv:2503.23791 (2025).
     Numerical Reasoning Tasks. Trans. Mach. Learn. Res. 2023 (2022). https:               [34] Anton Lozhkov, Raymond Li, Loubna Ben Allal, Federico Cassano, Joel Lamy-
     //api.semanticscholar.org/CorpusID:253801709                                               Poirier, Nouamane Tazi, Ao Tang, Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei,
[11] Xinyun Chen, Chang Liu, and Dawn Song. 2018. Tree-to-tree neural networks for              et al. 2024. Starcoder 2 and the stack v2: The next generation. arXiv preprint
     program translation. In Proceedings of the 32nd International Conference on Neural         arXiv:2402.19173 (2024).
     Information Processing Systems (Montréal, Canada) (NIPS’18). Curran Associates        [35] Marcos Macedo, Yuan Tian, F. Côgo, and Bram Adams. 2024. Exploring the
     Inc., Red Hook, NY, USA, 2552–2562.                                                        Impact of the Output Format on the Evaluation of Large Language Models for
[12] Jacob Cohen. 1960. A coefficient of agreement for nominal scales. Educational              Code Translation. 2024 IEEE/ACM First International Conference on AI Foundation
     and psychological measurement 20, 1 (1960), 37–46.                                         Models and Software Engineering (Forge) Conference Acronym: (2024), 57–68. https:
[13] Juliet Corbin and Anselm Strauss. 2014. Basics of qualitative research: Techniques         //api.semanticscholar.org/CorpusId:268691363
     and procedures for developing grounded theory. Sage publications.                     [36] Marcos Macedo, Yuan Tian, Pengyu Nie, Filipe R. Cogo, and Bram Adams. 2025.
[14] Daniela S Cruzes and Tore Dyba. 2011. Recommended steps for thematic synthesis             INTERTRANS: Leveraging Transitive Intermediate Translations to Enhance LLM-
     in software engineering. In 2011 international symposium on empirical software             Based Code Translation. In 2025 IEEE/ACM 47th International Conference on
     engineering and measurement. IEEE, 275–284.                                                Software Engineering (ICSE). 1153–1164. doi:10.1109/ICSE55347.2025.00236
[15] Isaac Martín De Diego, Ana R. Redondo, Rubén R. Fernández, Jorge Navarro, and         [37] Mono. 2025. Sharpen: Automated Java→C# conversion utility. https://github.
     Javier M. Moguerza. 2022. General Performance Score for classification problems.           com/mono/sharpen. Visited on 2025-08-27; Archived on March 9, 2021; Licensed
     Applied Intelligence 52 (2022), 12049 – 12063. https://api.semanticscholar.org/            under GPL-2.0.
     CorpusID:246462458                                                                    [38] Anh Tuan Nguyen, Tung Thanh Nguyen, and Tien N Nguyen. 2013. Lexical
[16] Shahriar Rumi Dipto, Saikat Mondal, and Chanchal K. Roy. 2026. ICPC 2026                   statistical machine translation for language migration. In Proceedings of the 2013
     Replication Package. https://github.com/sdipto7/llm-code-translation.                      9th Joint Meeting on Foundations of Software Engineering. 651–654.
[17] Angela Fan, Shruti Bhosale, Holger Schwenk, Zhiyi Ma, Ahmed El-Kishky, Sid-           [39] Anh Tuan Nguyen, Tung Thanh Nguyen, and Tien N. Nguyen. 2014. Migrat-
     dharth Goyal, Mandeep Baines, Onur Celebi, Guillaume Wenzek, Vishrav Chaud-                ing code with statistical machine translation. In Companion Proceedings of the
     hary, et al. 2021. Beyond english-centric multilingual machine translation. Journal        36th International Conference on Software Engineering (Hyderabad, India) (ICSE
     of Machine Learning Research 22, 107 (2021), 1–48.                                         Companion 2014). Association for Computing Machinery, New York, NY, USA,
[18] Angela Fan, Beliz Gokkaya, Mark Harman, Mitya Lyubarskiy, Shubho Sengupta,                 544–547. doi:10.1145/2591062.2591072
     Shin Yoo, and Jie M Zhang. 2023. Large language models for software engineering:      [40] Anh Tuan Nguyen, Tung Thanh Nguyen, and Tien N Nguyen. 2015. Divide-and-
     Survey and open problems. In 2023 IEEE/ACM International Conference on Software            conquer approach for multi-phase statistical migration for source code (t). In
     Engineering: Future of Software Engineering (ICSE-FoSE). IEEE, 31–53.                      2015 30th IEEE/ACM International Conference on Automated Software Engineering
[19] Muhammad Farrukh, Smeet Shah, Baris Coskun, and M. Polychronakis. 2025.                    (ASE). IEEE, 585–596.
     SafeTrans: LLM-assisted Transpilation from C to Rust. ArXiv abs/2505.10708            [41] Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou,
     (2025). https://api.semanticscholar.org/CorpusId:278714965                                 Silvio Savarese, and Caiming Xiong. 2022. Codegen: An open large language
[20] Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang,                    model for code with multi-turn program synthesis. arXiv preprint arXiv:2203.13474
     Jamie Callan, and Graham Neubig. 2023. PAL: program-aided language models. In              (2022).
     Proceedings of the 40th International Conference on Machine Learning (Honolulu,       [42] Vikram Nitin, Rahul Krishna, and Baishakhi Ray. 2024. Spectra: Enhancing the
     Hawaii, USA) (ICML’23). JMLR.org, Article 435, 36 pages.                                   code translation ability of language models by generating multi-modal specifica-
[21] Gotranspile. 2025. cxgo: Tool for transpiling C to Go. https://github.com/                 tions. arXiv preprint arXiv:2405.18574 (2024).
     gotranspile/cxgo. Visited on 2025-08-27; Licensed under MIT.                          [43] Rangeet Pan, Ali Reza Ibrahimzada, Rahul Krishna, Divya Sankar, Lam-
[22] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin                     bert Pouguem Wassi, Michele Merler, Boris Sobolev, Raju Pavuluri, Saurabh
     Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. 2025. Deepseek-r1:                  Sinha, and Reyhaneh Jabbarvand. 2024. Lost in translation: A study of bugs
     Incentivizing reasoning capability in llms via reinforcement learning. arXiv               introduced by large language models while translating code. In Proceedings of
     preprint arXiv:2501.12948 (2025).                                                          the IEEE/ACM 46th International Conference on Software Engineering. 1–13.
[23] Kai Huang, Xiangxin Meng, Jian Zhang, Yang Liu, Wenjie Wang, Shuhao Li, and           [44] paulirwin. 2025. JavaToCSharp: A Java to C# converter. https://github.com/
     Yuqing Zhang. 2023. An Empirical Study on Fine-Tuning Large Language Models                paulirwin/JavaToCSharp. Visited on 28 August 2025; Latest release v3.0.0 (27
     of Code for Automated Program Repair. In 2023 38th IEEE/ACM International                  Nov 2023); Licensed under MIT.
     Conference on Automated Software Engineering (ASE). 1162–1174. doi:10.1109/           [45] Ruchir Puri, David S Kung, Geert Janssen, Wei Zhang, Giacomo Domeniconi,
     ASE56229.2023.00181                                                                        Vladimir Zolotov, Julian Dolby, Jie Chen, Mihir Choudhury, Lindsey Decker, et al.
[24] Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh,                     2021. Codenet: A large-scale ai for code dataset for learning a diversity of coding
     Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. 2024.            tasks. arXiv preprint arXiv:2105.12655 (2021).
     Gpt-4o system card. arXiv preprint arXiv:2410.21276 (2024).                           [46] Yuhao Qing, Boyu Zhu, Mingzhe Du, Zhijiang Guo, Terry Yue Zhuo, Qianru
[25] Ali Reza Ibrahimzada, Kaiyao Ke, Mrigank Pawagi, Muhammad Salman Abid,                     Zhang, Jie M Zhang, Heming Cui, Siu-Ming Yiu, Dong Huang, et al. 2025.
     Rangeet Pan, Saurabh Sinha, and Reyhaneh Jabbarvand. 2025. AlphaTrans: A                   EffiBench-X: A Multi-Language Benchmark for Measuring Efficiency of LLM-
     Neuro-Symbolic Compositional Approach for Repository-Level Code Translation                Generated Code. arXiv preprint arXiv:2505.13004 (2025).
     and Validation. Proc. ACM Softw. Eng. 2, FSE, Article FSE109 (June 2025), 23 pages.   [47] Qwen, :, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen
     doi:10.1145/3729379                                                                        Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang,
ICPC ’26, 2026, Brazil                                                                                                                                                Dipto et al.


     Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang                 //dl.acm.org/citation.cfm?id=3511157
     Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue,          [59] Hua Wu and Haifeng Wang. 2007. Pivot Language Approach for Phrase-Based
     Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tianyi Tang, Tingyu Xia,                Statistical Machine Translation. In Proceedings of the 45th Annual Meeting of
     Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan,                     the Association of Computational Linguistics, Annie Zaenen and Antal van den
     Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. 2025. Qwen2.5 Technical                 Bosch (Eds.). Association for Computational Linguistics, Prague, Czech Republic,
     Report. arXiv:2412.15115 [cs.CL] https://arxiv.org/abs/2412.15115                           856–863. https://aclanthology.org/P07-1108/
[48] Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiao-         [60] Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. 2023. Automated
     qing Ellen Tan, Yossi Adi, Jingyu Liu, Romain Sauvestre, Tal Remez, et al. 2023.            Program Repair in the Era of Large Pre-trained Language Models. In 2023
     Code llama: Open foundation models for code. arXiv preprint arXiv:2308.12950                IEEE/ACM 45th International Conference on Software Engineering (ICSE). 1482–
     (2023).                                                                                     1494. doi:10.1109/ICSE48619.2023.00129
[49] Baptiste Roziere, Marie-Anne Lachaux, Lowik Chanussot, and Guillaume Lample.           [61] Zeke Xiao, Qin Wang, Hammond Pearce, and Shiping Chen. 2025. Logic Meets
     2020. Unsupervised translation of programming languages. Advances in neural                 Magic: LLMs Cracking Smart Contract Vulnerabilities. 2025 IEEE International
     information processing systems 33 (2020), 20601–20611.                                      Conference on Blockchain and Cryptocurrency (ICBC) (2025), 1–3. https://api.
[50] Baptiste Roziere, Jie M Zhang, Francois Charton, Mark Harman, Gabriel Synnaeve,             semanticscholar.org/CorpusID:275471064
     and Guillaume Lample. 2021. Leveraging automated unit tests for unsupervised           [62] Ruiyang Xu, Jialun Cao, Mingyuan Wu, Wenliang Zhong, Yaojie Lu, Ben He,
     code translation. arXiv preprint arXiv:2110.06773 (2021).                                   Xianpei Han, Shing-Chi Cheung, and Le Sun. 2025. EmbedAgent: Benchmarking
[51] Marc Szafraniec, Baptiste Roziere, Hugh Leather, Francois Charton, Patrick La-              Large Language Models in Embedded System Development. arXiv preprint
     batut, and Gabriel Synnaeve. 2022. Code translation with compiler representa-               arXiv:2506.11003 (2025).
     tions. arXiv preprint arXiv:2207.03578 (2022).                                         [63] Pengyu Xue, Linhao Wu, Zhen Yang, Chengyi Wang, Xiang Li, Yuxiang Zhang,
[52] TIOBE Software. 2024. TIOBE Index for April 2024. https://www.tiobe.com/tiobe-              Jia Li, Ruikai Jin, Yifei Pei, Zhaoyan Shen, et al. 2025. ClassEval-T: Evaluating
     index/. Accessed: May 2025.                                                                 Large Language Models in Class-Level Code Translation. Proceedings of the ACM
[53] Matthew D. Turner, Chayan Chakrabarti, Thomas B. Jones, Jiawei F. Xu, Peter T.              on Software Engineering 2, ISSTA (2025), 1421–1444.
     Fox, George F. Luger, Angela R. Laird, and Jessica A. Turner. 2013. Automated          [64] Zhen Yang, Fang Liu, Zhongxing Yu, Jacky Wai Keung, Jia Li, Shuo Liu, Yifan
     annotation of functional imaging experiments via multi-label classification. Fron-          Hong, Xiaoxue Ma, Zhi Jin, and Ge Li. 2024. Exploring and unleashing the power
     tiers in Neuroscience 7 (2013). https://api.semanticscholar.org/CorpusID:7215230            of large language models in automated code translation. Proceedings of the ACM
[54] Guoqing Wang, Zeyu Sun, Zhihao Gong, Sixiang Ye, Yizhou Chen, Yifan Zhao,                   on Software Engineering 1, FSE (2024), 1585–1608.
     Qing-Lin Liang, and Dan Hao. 2024. Do Advanced Language Models Eliminate               [65] Zhen Yang, Fang Liu, Zhongxing Yu, Jacky Wai Keung, Jia Li, Shuo Liu, Yifan
     the Need for Prompt Engineering in Software Engineering? ArXiv abs/2411.02093               Hong, Xiaoxue Ma, Zhi Jin, and Ge Li. 2024. Exploring and Unleashing the Power
     (2024). https://api.semanticscholar.org/CorpusId:273811798                                  of Large Language Models in Automated Code Translation. ArXiv abs/2404.14646
[55] Yue Wang, Weishi Wang, Shafiq Joty, and Steven CH Hoi. 2021. Codet5: Identifier-            (2024). https://api.semanticscholar.org/CorpusID:269303184
     aware unified pre-trained encoder-decoder models for code understanding and            [66] Xin Yin, Chao Ni, Tien N Nguyen, Shaohua Wang, and Xiaohu Yang. 2024. Rec-
     generation. arXiv preprint arXiv:2109.00859 (2021).                                         tifier: Code translation with corrector via llms. arXiv preprint arXiv:2407.07472
[56] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi,                    (2024).
     Quoc V Le, Denny Zhou, et al. 2022. Chain-of-thought prompting elicits reasoning       [67] Hanliang Zhang, Cristina David, Meng Wang, Brandon Paulsen, and Daniel
     in large language models. Advances in neural information processing systems 35              Kroening. 2024. Scalable, Validated Code Translation of Entire Projects using
     (2022), 24824–24837.                                                                        Large Language Models. Proceedings of the ACM on Programming Languages 9
[57] Justin D. Weisz, Michael J. Muller, Stephanie Houde, John T. Richards, Steven I.            (2024), 1616 – 1641. http://dl.acm.org/citation.cfm?id=3729315
     Ross, Fernando Martinez, Mayank Agarwal, and Kartik Talamadupula. 2021.                [68] Denny Zhou, Nathanael Scharli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang,
     Perfection Not Required? Human-AI Partnerships in Code Translation. Pro-                    Dale Schuurmans, Olivier Bousquet, Quoc Le, and Ed H. Chi. 2022. Least-to-
     ceedings of the 26th International Conference on Intelligent User Interfaces (2021).        Most Prompting Enables Complex Reasoning in Large Language Models. ArXiv
     http://dl.acm.org/citation.cfm?id=3450656                                                   abs/2205.10625 (2022). https://api.semanticscholar.org/CorpusID:248986239
[58] Justin D. Weisz, Michael J. Muller, Steven I. Ross, Fernando Martinez, Stephanie       [69] Ming Zhu, Mohimenul Karim, Ismini Lourentzou, and Daphne Yao. 2024. Semi-
     Houde, Mayank Agarwal, Kartik Talamadupula, and John T. Richards. 2022.                     supervised code translation overcoming the scarcity of parallel code data. In
     Better Together? An Evaluation of AI-Supported Code Translation. Proceedings                Proceedings of the 39th IEEE/ACM International Conference on Automated Software
     of the 27th International Conference on Intelligent User Interfaces (2022). http:           Engineering. 1545–1556.
