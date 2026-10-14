                                         From Evaluation to Enhancement: Large Language Models
                                         for Zero-Knowledge Proof Code Generation
                                         ZHANTONG XUE, Hong Kong University of Science and Technology, China
                                         PINGCHUAN MA∗ , Zhejiang University of Technology, China and CipherInsight Limited, China
                                         ZHAOYU WANG, Hong Kong University of Science and Technology, China
                                         YUGUANG ZHOU, Hong Kong University of Science and Technology, China
                                         XIAOQIN ZHANG, Zhejiang University of Technology, China
arXiv:2509.11708v2 [cs.SE] 31 Jan 2026




                                         SHUAI WANG, Hong Kong University of Science and Technology, China and CipherInsight Limited, China
                                         JUERGEN RAHMEL, HSBC, China
                                         Zero-knowledge proofs (ZKPs) are increasingly deployed in domains such as privacy-preserving authentication,
                                         verifiable computation, and secure finance. However, authoring ZK programs remains challenging: unlike
                                         conventional software development, ZK programming manifests a fundamental paradigm shift from imperative
                                         computation to declarative verification. This process requires rigorous reasoning about finite field arithmetic
                                         and complex constraint systems (which is rare in common imperative languages), making it knowledge-
                                         intensive and error-prone. While large language models (LLMs) have demonstrated strong code generation
                                         capabilities in general-purpose languages, their effectiveness for ZK programming, where correctness hinges
                                         on both language mastery and constraint-level reasoning, remains unexplored. To address this gap, we
                                         propose ZK-Eval, a domain-specific evaluation pipeline that probes LLM capabilities on ZK programming
                                         at three levels: language knowledge, algebraic primitive competence, and end-to-end program generation.
                                         Our evaluation of four state-of-the-art LLMs reveals that while models demonstrate strong proficiency in
                                         language syntax, they struggle when implementing and composing algebraic primitives to specify correct
                                         constraint systems, frequently producing incorrect programs. Based on these insights, we introduce ZK-Coder,
                                         an agentic framework that augments LLMs with constraint sketching, guided retrieval, and interactive repair.
                                         Experiments with GPT-o3 on Circom and Noir show substantial gains, with success rates improving from
                                         20.29% to 87.85% and from 28.38% to 97.79%, respectively. With ZK-Eval and ZK-Coder, we establish a
                                         new basis for systematically measuring and augmenting LLMs in ZK code generation to lower barriers for
                                         practitioners and advance privacy computing.
                                         CCS Concepts: • Software and its engineering → Automatic programming; Domain specific languages; •
                                         Security and privacy → Cryptography; • Computing methodologies → Natural language processing.

                                         1   Introduction
                                         Zero-knowledge proofs (ZKPs) are a powerful cryptographic primitive that allow one party to prove
                                         knowledge of a statement without revealing the underlying witness. In practice, this means proving
                                         that a computation or claim is correct while keeping sensitive inputs private. ZKPs have moved far
                                         beyond theory: they are now central to privacy-preserving authentication, blockchain scalability,
                                         verifiable computation, and emerging applications across finance and security domains [23, 36,
                                         57, 60]. As demand for trustworthy computation grows, the ability to author, test, and verify ZKP
                                         programs has become a first-class concern in the software engineering community [25, 29, 46, 58, 72].
                                         ∗ Corresponding author



                                         Authors’ Contact Information: Zhantong Xue, Hong Kong University of Science and Technology, Hong Kong, China,
                                         zxueai@cse.ust.hk; Pingchuan Ma, Zhejiang University of Technology, Hangzhou, China and CipherInsight Limited, Hong
                                         Kong, China, pma@zjut.edu.cn; Zhaoyu Wang, Hong Kong University of Science and Technology, Hong Kong, China,
                                         zwangjz@cse.ust.hk; Yuguang Zhou, Hong Kong University of Science and Technology, Hong Kong, China, yzhougv@
                                         cse.ust.hk; Xiaoqin Zhang, Zhejiang University of Technology, Hangzhou, China, xqzhang@zjut.edu.cn; Shuai Wang,
                                         Hong Kong University of Science and Technology, Hong Kong, China and CipherInsight Limited, Hong Kong, China,
                                         shuaiw@cse.ust.hk; Juergen Rahmel, HSBC, Hong Kong, China, juergen.rahmel@hsbc.com.hk.


                                                                                                       , Vol. 1, No. 1, Article . Publication date: February 2026.
2         Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


    Goal: Given bit-vector and bit-       Mainstream Program               ZKP DSL Program           Goal: Given public bit-vector and
    vector , compute                                                                                       , prove that there exists a
              (i.e, hamming distance)                    Computational Task                          private bit-vector such that
         and print the result .                                                                               , where                 .
                                           Program to Compute               Program to Prove
    def pythonProgram():                    (write Instructions)             (write Constraints)    template CircomProgram {
                                                                                                      signal input x[3], w[3], y;
     # Read or declare inputs                     Compile / Intrepret             Compile             signal acc[3];
     x = [False, True, False]               Binary for CPU                 Arithmetic Circuit         for (var i = 0; i < 3; i++) {
     w = [True, False, False]                                                                           x[i] * (1 - x[i]) === 0;
                                                                                                        w[i] * (1 - w[i]) === 0;
     # Perform computation                                                                              acc[i]<==x[i]+w[i]-x[i]*w[i];
     y = sum(a != b for a, b                Execute                Input               Prove          }
             in zip(x, w))                                                                            component sum_op = Sum(3);
                                                                                                      sum_op.in <== acc;
     # Print the result
     print("y =", y)                        Output                                      Proof         sum_op.out === y;
                                                                                                    }


                           Declare           Specify Algebraic Verification Constraints                  Compute Satisfying Witnesses
    Typical Process of      Inputs              Call API-Gadgets (Optional)             Relation            Off-circuit          Satisfy
    ZKP Programming           &
                           Witnesses           Compose Algebraic Primitives                                 Compute              Relation



           Fig. 1. Illustrative Comparison Between the Process of Mainstream and ZK Programming.

 Table 1. Mainstream & ZK Program Comparison.                               ZK-Eval Benchmark                 ZK-Coder Pipeline

                                                                                 Toolchain Knowledge             Sketching Constraints
                                                                                                     +
       Aspect          Mainstream            ZK Program
      Paradigm    Imperative/OOP/Func      Constraint Systems
                                                                                 Primitive-level Usage          Constraint-guided RAG
    Comp. Model von Neumann Arch           Arithmetic Circuits
       Purpose          to Compute           to Prove/Verify                                        +
     Data Types       Int/Float/Str/...   Finite Field Elements                 End-to-end Generation            Interactive Gen-repair
     Mutability          Dynamic                  Static
    Control Flow    If/Loop/Recursion            Limited
     Side Effects           Yes              No, Pure Math
                                                                            Fig. 2. Overview of ZK-Eval and ZK-Coder.

   However, authoring ZK programs is challenging. Unlike mainstream programming, which builds
on the von Neumann model and imperative execution, ZKP programs boil down to specifying and
proving mathematical constraints over finite fields. In essence, this represents a paradigm shift from
computation to verification. Its development requires reasoning about finite field arithmetic and
constraint systems. As shown in Fig. 1 and Table 1, ZK programs do not describe how to execute
a computation but how to prove its correctness by compiling constraints into arithmetic circuits.
Developers must specify equations over inputs, outputs, and intermediate variables, carefully
wiring algebraic primitives to specify constraints enforcing correctness. Even small omissions or
miswirings can yield unsound or incomplete constraint systems, leading to errors that compilers
rarely flag. This makes ZK development knowledge-intensive, error-prone, and inaccessible to
non-experts, despite significant progress in proof systems and verification tools [7, 8, 34, 46, 58].
   As a result, ZK programming demands significantly more time and expertise than mainstream
software development, posing a steep barrier to entry for many practitioners. In contrast, recent
advances in large language models (LLMs) have lowered this barrier in general-purpose languages by
demonstrating strong code generation capabilities [31], achieving impressive results on benchmarks
such as HumanEval [10] and MBPP [50], and powering widely adopted tools like GitHub Copilot [21]
and Cursor [59]. This contrast naturally raises the question: to what extent can modern LLMs assist
in generating ZK code from natural language specifications? Answering this question requires more
than surface-level benchmarking. Compared to programming in mainstream languages, success in
ZK development hinges on three competencies: (i) knowledge of domain-specific languages (DSLs)
and their toolchains, (ii) mastery of algebraic primitives as atomic building blocks for constraint

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                      3


systems, and (iii) proficiency in modeling and specifying complex verification constraints. Existing
benchmarks focus only on mainstream programming paradigms and overlook these requirements.
    To measure this knowledge gap, this paper first introduces ZK-Eval, a domain-specific evaluation
pipeline that probes LLM capability at three levels: language knowledge, primitive-level competence,
and end-to-end program code generation (left panel of Fig. 2). We anticipate that this design would
provide a structured way to pinpoint where models succeed, where they fail, and why.
    As will be detailed in § 3, applying ZK-Eval to four SoTA LLMs (including advanced reasoning
models like GPT-o4-mini and GPT-o3) reveals a clear pattern. While models perform strongly
on language knowledge, their accuracy drops significantly (below 30%) when reasoning about
primitives or assembling verification constraints, highlighting a critical gap between syntactic
knowledge and end-to-end generation. These results underscore both the potential of LLMs to
democratize ZK development and the need for targeted augmentations to bridge this capability gap.
Motivated by these findings, we present ZK-Coder (right panel of Fig. 2), which combines three key
components: (i) a sketch layer (ZKSL) that explicitly models constraints using algebraic primitives,
(ii) retrieval-augmented generation to ground specifications in verified implementations, and (iii)
interactive refinement to fix constraint misspecifications. We observe that ZK-Coder achieves
substantial gains, improving code generation success rates from 20.29% to 87.85% on Circom and
from 28.38% to 97.79% on Noir (using GPT-o3). Ablation studies further confirm that sketching,
guided retrieval and interactive refinement are indispensable; removing either component causes a
significant performance drop (over 10%). In summary, our contributions are as follows:
(1) We propose ZK-Eval, a three-stage evaluation pipeline for systematically assessing LLM capa-
     bilities in ZK code generation.
(2) We introduce ZK-Coder, an agentic framework that augments LLMs with constraint sketching,
     guided retrieval, and interactive repair to improve reliability.
(3) We evaluate the performance of four state-of-the-art LLMs on ZK-Eval and demonstrate how
     ZK-Coder substantially improves end-to-end code generation.

2     Background
2.1    Zero-Knowledge Proofs and Programming Frameworks
Zero-knowledge proofs (ZKPs) are cryptographic protocols that allow one party to prove to another
that a statement is true without revealing any information beyond the validity of the statement
itself. Formally, the following properties are desired for a correct ZKP program.
(1) Completeness: If a statement is true, an honest prover can convince the verifier of its validity.
(2) Soundness: If a statement is false, no dishonest prover can convince the verifier of its validity.
(3) Zero-Knowledge: The verifier learns nothing beyond the validity of the statement itself.
These properties make ZKPs particularly useful in verifiable computation and privacy-preserving
applications [23, 36, 60]. However, ZK programming necessitates a fundamental paradigm shift from
imperative computation to declarative verification. Rather than writing instructions to calculate a
result, developers must model their high-level intent as an arithmetic representation 𝑅(𝑥, 𝑤) = 1
over a finite field, where 𝑥 denotes public inputs and 𝑤 denotes the private witness. This requirement
to faithfully enforce logical intent through field-arithmetic constraints is notoriously arduous for
humans; even minor errors in modeling can lead to under-constrained circuits (compromising
soundness) or over-constrained systems (breaking completeness) [8, 34, 46, 69].
   To mitigate this complexity, several programming frameworks have emerged, offering a diverse
range of abstractions. We categorize these into two primary design paradigms:
(1) Constraint-Oriented DSLs. Frameworks like Circom and Noir provide specialized syntax
    for expressing verification relations. Circom requires developers to think in terms of low-level

                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
4       Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


    circuit wiring and explicit signal management, which poses significant challenges for LLMs
    tasked with producing correct circuit templates [7, 25]. Conversely, Noir adopts a Rust-like
    syntax with strong typing, aligning more closely with the general-purpose coding corpora on
    which current LLMs are trained [30, 33].
(2) General-Purpose zkVMs. Emerging solutions like SP1 [35] and RISC0 [13] allow developers
    to compile standard Rust code into a restricted instruction set, generating proofs over the
    execution trace within a virtual machine. While they abstract away the constraint system
    entirely, they often incur substantial performance overhead. We consider these an orthogonal
    approach to our work, as we focus on the direct generation of circuits.
   In this work, we focus on Circom and Noir because they represent the most widely adopted
frontends in both academia [3, 45, 46, 56, 69] and industry (e.g., in Ethereum rollups and Aztec).
Furthermore, they occupy two complementary points on the abstraction spectrum: Circom tests an
LLM’s ability to perform circuit-level specification and constraint wiring, while Noir evaluates how
effectively models can adapt conventional coding proficiency to the verification-oriented paradigm.
By studying both, we capture the core technical challenges of ZKP development while ensuring
our findings have immediate practical relevance.

2.2    LLM-based Code Generation
Large Language Models (LLMs) have emerged as powerful assistants in software development,
enabling code generation from natural language prompts with tools like GitHub Copilot, Cursor,
and model-driven agents quickly translating intent into code [30, 31]. These systems are reshaping
engineering workflows, aiding in writing, testing, and documenting code by drawing on vast
amounts of publicly available repositories and documentation [21].
Framework. Modern LLM-based code generation typically follows an agentic framework [68,
76], where the model acts as an intelligent assistant, interpreting user intent, retrieving relevant
information, and producing code snippets or entire functions as needed. This process often involves
multiple iterations, with the model refining its output based on user feedback or additional context.
In this way, it can leverage off-the-shelf LLMs effectively without code-specific fine-tuning [17, 47].
However, to the best of our knowledge, there has been limited exploration of LLMs for code
generation for low-resource programming languages (LRPL) or DSLs especially for ZKP DSLs.
Benchmark. Benchmarks are a crucial component of LLM-based code generation research, playing
a vital role in understanding model performance and guiding improvements. Currently, their
accuracy and reasoning ability are usually evaluated on standard benchmarks on mainstream
programming languages such as HumanEval [10] and MBPP [50]. However, evaluation tools for
LRPLs and DSLs remain limited, hindering comprehensive assessments of LLM performance in these
contexts [20, 33]. Code generation for ZKP programs exemplifies the challenges and opportunities
in this space. Though benchmarks for LRPLs [6, 73] and DSLs [2, 40] exist, to our knowledge,
no standardized benchmark suite specifically targets ZKP code generation, requiring tailored
benchmarks and evaluation strategies.

3     Measuring LLM Capability for ZK Code Generation
As discussed in § 1 and § 2.1, ZK programming follows a proof-oriented model: developers translate
high-level intent into algebraic constraints over a finite field and produce proofs of satisfiability.
This shift yields a unique programming workflow depicted in Fig. 1, where developers construct
the verification relation by wiring together algebraic primitives (mathematical gates that enforce
logical invariants over finite fields). While witness computation still resembles conventional imper-
ative programming, the developer’s primary responsibility shifts to the rigorous specification of

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                                                          5


these verification constraints. To evaluate LLM proficiency in this critical domain, we assess two
foundational capabilities essential for end-to-end success: ➀ language and toolchain knowledge
and ➁ algebraic primitive competence.
(1) Language and Toolchain Knowledge. Developers must master domain-specific syntax, strict
    typing rules, and the semantics of field operations to structure valid constraint specification and
    witness assignments. Weakness in any of these areas routinely leads to programs that cannot
    be compiled or produce an invalid relation that renders the proof meaningless.
(2) Algebraic Primitive Competence. Algebraic primitives are the atomic building blocks of
    ZK constraint systems. Since arithmetic circuits lack native support for high-level operations,
    developers combine relational (e.g., comparators), logical (e.g., bitwise gates), and arithmetic
    (e.g., division, inversion) primitives to express logic. Competence in these atomic units is a
    prerequisite for constructing sound, higher-level application-specific constraint systems.
   These capabilities constitute two core dimensions of end-to-end ZK program generation. Without
language and toolchain knowledge, LLMs cannot produce compilable programs; without algebraic
primitive competence, programs cannot faithfully encode intended relations. Since ZK programming
requires integrating language-level fluency with deeper constraint modeling, existing mainstream
benchmarks [10, 27, 50] leave this integration unexplored. We introduce ZK-Eval to systematically
measure both dimensions and their integration in end-to-end tasks.

3.1       ZK-Eval Benchmark
To realize this benchmark design, we structure ZK-Eval in three stages, each targeting one capability
and their integration. We illustrate the design overview in Fig. 3.

        Phase 1: Language Competence                         Phase 2: Algebraic Primitives               Phase 3: End-to-end Verification Program

  Official Documents           Examples & Tutorials    ZK / Algebraic Libraries    Real-world Sources    Standardized Computational Coding Benchmarks
                                                                                                               HumanEval LiveCodeBench


              Top k                 LLM-aided                                                                  Filter
                                                                Summarize, Deduplicate and Filter
                                     Question
             Iterate
                                    Generation                                                           Rephrase Description       Adapt Oracle
      Until all docs covered                                                              Test-cases /
                                                         Algebraic                        Truth-Table
               Basic Advanced API Compile
              Syntax Topics   Usage Principles
                                               Total      Primitive                   Primitives' Task
                                                                        Experts                           Implement Testcase      Acceptance Cases
                                                       (e.g., Modulo)
  Circom        99      32     15       26     172                      Authored        Description        Generator Scripts       Rejection Cases
   Noir         87      37     24       16     164



        Validate, Calibrate & Cross-check               Cross-check & Monitor Test-case Quality             Validate & Monitor Test-case Quality


                               Fig. 3. The Three-Stage Evaluation Design of the ZK-Eval Benchmark.

3.1.1 Language and Toolchain Knowledge. We first evaluate whether LLMs possess the foundational
knowledge required to author ZK programs. As shown in the left side of Fig. 3, sources are collected
through web crawling of official documentation, including language specifications, tutorials, and API
references (e.g., Circom’s circomlib [26] and the Noir’s stdlib). Additionally, we gather publicly
available pedagogical examples from GitHub repositories [12, 54, 62, 63] and online tutorials [61]
to increase coverage of idiomatic usage. This yields 51 documents for Circom and 40 for Noir.
   Based on this knowledge base, we then design a pipeline to automatically generate multiple-choice
questions, a format widely adopted in prior evaluations of language models [11, 24, 43, 75]. Inspired
by earlier work on LLM-driven question generation [1, 28, 38, 41], our pipeline iteratively samples
subsets of documents and provides them to a large model, which composes candidate questions

                                                                                      , Vol. 1, No. 1, Article . Publication date: February 2026.
6       Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


and answers. This process is repeated until the full document collection has been exhaustively
covered, producing a diverse set of drafts.
   All generated questions are then subjected to rigorous expert validation. Three human reviewers
independently assess each item for factual correctness, clarity, and alignment with the intended
difficulty, with disagreements resolved through discussion to consensus. Cross-checking by the
authors ensures consistency across the set. Topic coverage is also verified to ensure that all major
aspects (as listed in the official documents) of the studied language are represented. We categorize
the questions into four groups: basic syntax (language grammar such as datatypes, statements,
operators, control flows, signals and buses), advanced topics (e.g., taggings, traits, generics), API
references (standard library APIs), and compiler principles (translation from source code to arithmetic
circuits). As shown in Fig. 3, the final benchmark consists of 172 questions for Circom and 164 for
Noir, with a balanced distribution across the four categories. Representative examples are provided
in the Supplementary Material and the full set of questions is provided in the Artifact.
3.1.2 Implementing and Using Algebraic Primitives to Specify Constraints. We assess the capability of
LLMs to implement and utilize algebraic primitives as the building blocks of ZK constraint systems.
Different from higher-level cryptographic (e.g., hash functions, signatures) and application-level
(e.g., account-balance checks, order-matching validity) APIs available in external libraries, these
encapsulate the core relational logic that developers must wire to define custom circuit behavior.
Technical Difficulty. We clarify that, constructing a benchmark that reflects the fundamental
algebraic patterns essential to real-world ZK programs is challenging. In existing codebases, core
relational logic is often entangled with application-specific boilerplate, making it difficult to isolate
and evaluate the underlying algebraic reasoning. To decouple and isolate these foundational patterns,
we systematically curate a set of primitives from widely adopted libraries. This process, illustrated
in Fig. 3, draws from three complementary sources: circomlib [26], zk-kit [44], and Z3Py [51].
(1) Standardized Libraries. We first include canonical primitives from circomlib and zk-kit,
     which represent the production standard for routine circuit instantiation.
(2) Agnostic Extraction. From these repositories, we manually extract and deduplicate algebraic
     primitives while filtering out application-specific composites. This ensures the benchmark
     captures the universal building blocks of ZK logic rather than application-specific patterns.
(3) Aligned Completeness. To ensure comprehensiveness, we cross-reference our set with the
     Z3Py SMT-solver interface and incorporate primitives with similar structures, guaranteeing
     completeness for algebraic constraint specification.
    The resulting benchmark consists of 35 algebraic primitives covering a wide range of categories:
(i) basic checks, including range tests and comparisons; (ii) logical gates, such as AND, OR, XOR, and
equality; (iii) arithmetic operators, such as addition, multiplication, integer division, exponentiation,
modular reduction, and inversion; and (iv) composite operators, such as sum and multiplexers (see
the full list in the Supplementary Material). This collection serves as a complete basis for constraint
specification; as these algebraic primitives represent the atomic operations of arithmetic circuits,
any non-trivial verification relation can be realized through their rigorous composition.
Practical Relevance. To check the practical relevance of our benchmark, we surveyed 37 production-
grade ZK repositories comprising 408 source files. Our analysis confirms that the selected algebraic
primitives are highly representative of real-world circuit logic: we achieve 97.30% and 94.59% cov-
erage for core arithmetic and relational primitives, respectively, which are universal to production
ZK systems. While logical (70.27%) and specialized composites (16.22%) appear less frequently,
they remain mathematically essential for logical completeness and the construction of complex
verification relations. Notably, it includes every one of the top 10 most frequently used primitives
identified in the survey, establishing a representative foundation.

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                      7


Task Setup. For each primitive, we author a concise task description that asks the LLM to implement
the primitive’s functional logic and use it to specify the intended algebraic relation. Following
established practice on test-case curation [10, 27], we craft test-cases that validate both completeness
(accepting valid witnesses) and soundness (rejecting invalid assignments). For finite primitives (e.g.,
logical xor), test-cases exhaustively enumerate the entire truth table. For primitives with larger
domains, we combine automated random input generation with edge-cases (e.g., field overflows,
zero-value or out-of-domain inputs), yielding at least 100 cases per primitive. To validate test rigor,
we injected artificial errors into ground-truth implementations (like a mutation testing process);
our tests detected 87.04% of these faults, confirming their effectiveness at catching subtle mistakes.
3.1.3 End-to-End ZK Program Generation. The final stage assesses LLMs to generate complete and
correct ZK programs to verify computational statements. Building upon the first two stages, it
evaluates the systemic integration of these skills to construct sound, multi-primitive constraint
systems that faithfully encode high-level verification relations.
Benchmark Design Rationale. To ensure a rigorous and trustworthy assessment in the absence
of a standardized ZK-specific generation dataset, we leverage canonical algorithmic baselines from
the well-established HumanEval dataset. We posit that ZK programming represents a fundamental
paradigm shift from imperative computation to algebraic verification rather than a shift in the appli-
cation domain itself. Since the core logic of production-grade ZK applications (e.g., private finance,
decentralized identity, and state-transition proofs) relies on universal algorithmic patterns (e.g.,
sorting, membership checks, and conditional branching), adapting these general algorithmic tasks
allows us to isolate the gap on computation-to-verification translation without the confounding
variables of application-specific requirements (e.g., application-specific API calling).
   To reflect the unique semantics of ZK proofs, we systematically transform the original benchmark
through three distinct adaptations, as illustrated in the right column of Fig. 3:
(1) Compatibility Filtering. We exclude tasks involving string manipulation and floating-point
    arithmetic which are not supported by DSLs. Variable-length output tasks are also excluded
    since they’re incompatible with the static nature of arithmetic circuits. Their removal ensures
    that evaluation focuses on the model’s constraint-reasoning ability rather than DSL limitations.
    This yields a curated set of 68 standalone tasks suitable for ZK synthesis.
(2) Verification Reformulation. We reformulate the natural language description of each com-
    putational task (defined as finding 𝑆 = 𝑃 (𝐼 ) for input 𝐼 ) into a verification problem. The LLM
    must generate a verification function 𝑉 (𝐼, 𝑆) ∈ {0, 1} that returns 1 if and only if the candidate
    solution 𝑆 satisfies the intended relation for input 𝐼 .
(3) Oracle Adaptation. Correspondingly, the ground-truth oracle solutions are rewritten from
    computational functions (𝑆 = 𝑃 (𝐼 )) to verification forms (𝑉 (𝐼, 𝑆)). To ensure these serve as a
    reliable ground truth, we adopt a declarative implementation style; for instance, a sorting task
    is verified by checking permutation and monotonicity predicates rather than re-executing a
    sorting algorithm. To align with the semantics of ZKPs, these oracles are restricted to finite field
    arithmetic (mod 𝑝) and avoid non-deterministic execution paths. Each oracle was manually
    authored and cross-validated against the original computational benchmarks to ensure its
    reliability as a reference for test-case preparation.
Quality Assurance. Following established practices in benchmark construction [39, 53, 66, 74, 77],
we implement a rigorous validation process to ensure the Soundness and Completeness of generated
programs. While traditional datasets provide only “Acceptance Cases” (Completeness), ZK programs
require “Rejection Cases” to ensure the circuit is properly constrained (Soundness). Thus we
implement test-case generators to produce input-solution pairs that a correct verifier must reject,
ensuring soundness validation. We cross-validate task descriptions, adapted oracles, and test-case

                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
8           Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel

                                                                                                                                                    Semantically Correct                 Syntactically Valid




                                                                                                   Pass@1 Noir Pass@1 Circom
                         Basic            Advanced                                                                             1.0
                        Syntax             Topics                                                                                       0.17 0.19 0.20 0.22 0.07 0.09 0.05 0.09
                       100%                                                                                                    0.5
           API                                         Compiling
                              80%                      Principles             Human Expert
                                                                              DeepSeek-V3
                                                                                                                               0.0
                                        60%
                                                                              o4-mini                                          1.0
                                                                              o3                                                        0.32 0.40 0.28 0.37 0.16 0.20 0.10 0.19
        Compiling                                         API                 Qwen3
        Principles                                                                                                             0.5
                                                                       Upper: Circom                                           0.0
                      Advanced                 Basic                    Lower: Noir
                       Topics                 Syntax                                                                                        o4-mini                  o3          DeepSeek-V3      Qwen3


Fig. 4. Accuracy of LLMs and Human Experts on the                                                Fig. 5. LLM Performance on End-to-end ZK Bench-
MCQ Benchmark for ZK Language Knowledge.                                                         marks. Annotated with average accuracy.
                                         On Circom Toolchain                                                                                 On Noir Toolchain
                                                                                                                                                                                                    1.00
    Arithmetic       0.05        0.08         0.01     0.01     0.43   0.07       0.35           0.09                                0.18      0.08           0.02        0.00    0.04    0.61
                                                                                                                                                                                                    0.80
Comparison           0.37        0.13         0.02     0.04     0.11   0.01       0.32           0.20                                0.11      0.02           0.01        0.00    0.08    0.59      0.60
Composites           0.06        0.08         0.00     0.01     0.36   0.06       0.44           0.17                                0.22      0.01           0.02        0.00    0.04    0.55      0.40
                                                                                                                                                                                                    0.20
Logical Ops          0.52        0.15         0.19     0.00     0.03   0.00       0.11           0.49                                0.15      0.11           0.00        0.00    0.00    0.25
                                                                                                                                                                                                    0.00
                  orrect            aints tional Modules Signals Syntax Typing                orrect                                    aints unc   tional       les
                                                                                                                                                             Modu Sign
                                                                                                                                                                       als Syntax Typing
                 C            Constr Func                                                    C                                 Constr       F

     Fig. 6. Average Error Distribution of Primitive Implementations Across Languages, Types, and Causes.

generators through manual review and injection of edge cases (e.g., all-zeros, field-overflows,
out-of-domain inputs, etc.). Collectively, this process yields 100 test cases per task with an average
distribution of 54.41% acceptance and 45.59% rejection cases. To quantify benchmark quality,
we injected syntactic mutations into the ground-truth oracles (mutation-testing); our test suites
detected 86.42% mutations, demonstrating high sensitivity to subtle errors.

3.2        Measurement Settings
Using ZK-Eval, we measure LLMs’ competencies on ZK code generation. Our study is guided by
the following three research questions (RQs):
• RQ1: Language & Toolchain Knowledge. Do LLMs understand the syntax, semantics, and
  standard library APIs of Circom and Noir?
• RQ2: Algebraic Primitive Competence. Can LLMs reliably implement and use algebraic
  primitives, the building blocks of ZK programs, to specify correct constraints?
• RQ3: End-to-End Generation. Can LLMs integrate these skills to produce complete, correct
  ZK programs on the intended computational relation?
  Each RQ corresponds directly to one component of ZK-Eval. For RQ1, models are tested on
curated multiple-choice questions covering language knowledge. For RQ2, they are instructed to
implement and use algebraic primitives which are then automatically validated against acceptance
and rejection test cases. For RQ3, they attempt end-to-end program generation to realize verification
constraints for general computational problems, whose correctness is judged by soundness and
completeness against dual test suites.
Model Selection. We evaluate 4 representative LLMs: OpenAI’s reasoning models GPT-o4-mini and
GPT-o3, along with DeepSeek-V3 and Qwen3. This mix of reasoning and open-weight non-reasoning
ones allows us to assess both family-specific and general trends. All models are run under identical
prompts and budgets, with 10 samples per task to estimate Pass@1 rates and reduce variance.

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                      9


3.3   (RQ1) Language & Toolchain Knowledge
Fig. 4 summarizes performance. Reasoning models perform best, with GPT-o4-mini reaching 88.1%
and GPT-o3 87.2%. Open-weight non-reasoning models perform noticeably worse, with DeepSeek-
V3 at 79.5% and Qwen3 at 78.9%. The human expert for reference scores 88.7%, similar to the
reasoning models. Overall, LLMs demonstrate strong competence in ZK language knowledge,
achieving accuracy within a few percentage points of the human expert.

 Finding ①: On Circom and Noir, LLMs display strong competence in ZK language knowledge.
 Reasoning models surpass open-weight ones and perform similar to human experts.

   We further examine performance across question categories and languages. LLMs achieve their
highest accuracy on questions about basic syntax and API references, reflecting familiarity with
fundamental constructs and widely used library templates. In contrast, accuracy drops on advanced
topics such as traits, signal taggings, and generics, which extend expressiveness but are less
commonly encountered. The lowest performance is observed on compiler principles, which probe
understanding of how source programs are transformed into arithmetic circuits, indicating that they
struggle with deeper aspects of arithmetic circuits and constraint semantics on finite fields. Notably,
there is no significant difference between Circom and Noir, suggesting that model competence
reflects general exposure to ZK languages rather than language-specific familiarity.

 Finding ②: LLMs excel at surface-level knowledge such as syntax and API references, but exhibit
 weaknesses in advanced language features and compiler principles.

   These findings are consistent with the nature of the knowledge base: official documents, public
tutorials, and examples are all widely accessible training material to LLMs. Thus, it is anticipated that
LLMs can achieve strong performance on such content. This suggests that (i) explicit augmentations
on language grammars or official documentations may be unnecessary (ii) LLMs exhibit strong
potential for ZK programming tasks but require further evaluations to reveal the bottlenecks.

3.4   (RQ2) Algebraic Primitive Competence
Language knowledge enables syntactic fluency, but ZK programming fundamentally requires the
ability to specify algebraic constraints. We next assess whether LLMs can use or implement algebraic
primitives, the atomic elements of constraint systems. Specifically, model outputs were analyzed
with automated scripts that classified errors based on compiler diagnostics and test outcomes. From
their distinct linguistic and functional effects, we grouped errors into six categories: (i) constraint
enforcement, where models failed to encode relations using equality constructs ( === in Circom,
 assert in Noir); (ii) modules, involving incorrect instantiation or usage of library components; (iii)
signal handling, specific to Circom, where mistakes occurred in declaring, assigning, or referencing
signals; (iv) syntax & parsing, where the generated code violated grammar rules; (v) typing &
resolution, where data types or variables were used inconsistently or incorrectly; and (vi) functional
errors, where code compiled but failed functional correctness tests.
   Fig. 6 shows the results and performance is consistently weak: even the best-performing category,
logical operations, reached only 52% accuracy in Circom and 49% in Noir. Comparison scored lower
(37% and 20%), while Arithmetic and Composites dropped to extremely low accuracy. This contrasts
sharply with the strong results on language-level knowledge: when asked to operationalize this
knowledge into specifying constraints with algebraic primitives, LLMs largely fail to produce
testable, correct implementations. This gap reflects the difficulty of code generation for low-resource
DSLs [33], exacerbated in ZK programming by the inherent programming paradigm shift [52].

                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
10      Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


 Finding ③: On Circom and Noir languages, LLMs perform consistently weak on implementing
 and using algebraic primitives to specify constraints across all categories.

   Typing & resolution errors are the most frequent. Noir enforces strict type matching, disal-
lowing implicit casts between fields and integers, while Circom distinguishes between variables
and signals. Models frequently mix types, reference undeclared identifiers, or redefine variables,
causing compilation failures. Signal handling errors, unique to Circom, are the next most common,
including declaring signals inside control-flow, reassigning them multiple times, or using them
before initialization. Constraint enforcement errors also recur: models generate invalid constraint
forms such as non-quadratic constraints (e.g., x * y * z === 1 ) or use off-circuit assertions.
These issues stem from ZK-specific semantics absent in conventional languages.
   Performance further varies by primitive type, reflecting library support and algebraic complexity.
Logical operations and comparisons, being boolean primitives or supported by libraries, are most
tractable. Arithmetic and Composites, such as exponentiation, modulo, floor division, or composites
like sum and product, lack native support and must be implemented from scratch. These tasks
demand reasoning over field arithmetic, careful handling of inverses and negatives, and explicit
soundness constraints. The very low accuracy here underscores the inability of current models to
generate implementations beyond those directly provided in libraries.

 Finding ④: LLMs handle boolean and comparison primitives better than arithmetic and compos-
 ite ones, where ZK-specific semantics and limited library support demand non-trivial reasoning.

3.5    (RQ3) End-to-End Generation
Fig. 5 summarizes the results on the end-to-end generation benchmark. Compared to language
knowledge and primitive-level tasks, performance drops substantially across all models. For Circom,
accuracy is very low: GPT-o3 reaches only 20% semantically correct and 22% syntactically valid
programs, while Qwen3 drops to 5% and 9%. Noir results are somewhat higher but still limited,
with GPT-o4-mini at 32% and 40% and Qwen3 at 10% and 19%.
  Several trends emerge from these results. First, Noir tasks consistently yield higher success
rates than Circom, likely due to Noir’s simpler type system and cleaner syntax, which reduce
opportunities for errors such as signal misuse or type mismatches that are pervasive in Circom.
Second, reasoning models substantially outperform open-weight ones: GPT-o4-mini and GPT-o3
are 2–3 times more successful than DeepSeek-V3 and Qwen3 across both languages, confirming
the model capability difference already observed in earlier tasks. Finally, the gap between syntactic
and semantic correctness underscores that being compilable alone is insufficient for assessing ZK
program quality: many outputs are compilable but suffer from under- or over-constrained relations.

 Finding ⑤: LLMs perform poorly on end-to-end code generation: reasoning models beats
 open-weight ones; Noir is easier than Circom; many programs compile but remain incorrect.

   This reveals the fundamental challenge of ZK programming: it requires not only language fluency
and primitive competence, but also the ability to architect multi-primitive constraint systems that
faithfully encode complex verification relations — a skill that current LLMs have not yet mastered.

4     Augmenting LLMs for ZK Code Generation
Based on the findings and gaps revealed from our empirical study in § 3, we introduce ZK-Coder,
an agentic framework to augment end-to-end ZK code generation. We first summarize the design
principles derived from our findings, then present the system.

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                        11


4.1   Design Principles Learned from the Findings
Findings ① and ② show that LLMs possess strong knowledge of ZK languages’ syntax, semantics,
and standard library APIs, achieving near expert-level accuracy. Overall, we interpret that knowl-
edge has been internalized during contemporary LLM’s pretraining stage, eliminating the need for
grammar prompting or documentation access in our augmentation. However, important challenges
remain that motivate our further exploration.
   In Findings ③ and ④, we observe that this knowledge does not translate into reliable primitive-
level generation. Generated code frequently suffers from typing errors, signal mismanagement, and
faulty constraint enforcement. Finding ⑤ also reveals these failures in end-to-end generation. To
bridge this gap, ZK-Coder introduces a sketch layer that decouples abstract constraint modeling
from low-level DSL implementation. By first formalizing relations in this intermediate represen-
tation, the framework can precisely map identified primitives to verified circuit templates and
usage hints via retrieval-augmented generation (RAG) [19]. Loosely speaking, this trades brittle
memorization for grounding. Once the logical “what” is defined in the sketch, retrieval provides
the exact “how” for DSL-specific wiring, collapsing the search space and enabling the reliable
composition of even rare algebraic snippets.
   Finally, Findings ③ and ⑤ highlight end-to-end program generation as the most challenging
setting, where generated programs often fail due to constraint-misspecification or under/over-
constrained logic. These failures directly undermine the reliability and necessitate mechanisms to
improve validity and faithfulness. To mitigate these failures, ZK-Coder introduces an interactive
refinement loop. The LLM proposes a program, queries the compiler as an oracle to check constraint
specification validity, and, once passes, self-supplies acceptance/rejection test cases to validate
relation faithfulness. By observing diagnostics and counterexamples, ZK-Coder repairs its code and
iterates the “generate-compile-test-repair” loop until these checks pass. This interaction transforms
failures into actionable feedback and guides candidates toward valid, faithful programs.

4.2   ZK-Coder
Based on these design principles, we developed ZK-Coder, illustrated in Fig. 7. ZK-Coder augments
LLMs with a structured pipeline that bridges natural-language problem descriptions and executable
ZK programs. It consists of three main stages: ➀ constraint formulation, ➁ sketch-guided analysis
and retrieval, and ➂ interactive generation and repair.
4.2.1 Constraint Formulation in Sketch Language. The first stage of ZK-Coder translates natural-
language requirements into a structured specification of verification constraints. Drawing on the
success of planning-based code generation [15, 32, 37, 65, 70], we introduce the ZK Sketch Language
(ZKSL), a Python-embedded Domain Specific Language (eDSL) designed to bridge the gap between
high-level intent and low-level circuit implementation.
   ZKSL is architected to allow LLMs to formalize constraint logic using familiar Pythonic syntax.
This isolates the mathematical “what” from the DSL-specific “how” by requiring the explicit model-
ing of constraints over typed inputs to mirror the verification nature of ZK programs. As formally
defined1 in Fig. 8, a ZKSL Program is structured around a verify function that accepts these
typed inputs and executes a sequence of constraint-declaration statements via engine.add(Φ) .
These formulas are composed of relational atoms that correspond to the algebraic primitives iden-
tified in § 3.1.2. Crucially, all operations within ZKSL are defined over finite fields (modulo 𝑝) to
faithfully reflect the mathematical foundation of ZK systems. This enables LLMs to express complex
verification relations using standardized constructs, serving as a direct logical precursor to the final
1We also provide concrete running examples in the Supplementary Material.



                                                              , Vol. 1, No. 1, Article . Publication date: February 2026.
12      Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


                    ❶ Constraint Formulation in ZKSL                                        ❷ Constraint-guided Analysis & Retrieval
                          def verify(engine: VerifyingEngine,                                                  Implies: Bool      Bool      Bool
                              ... # Input Variables
       Problem                                                                            Not a Constraint
                          ) -> VerifyingEngine:
      Description                engine.add(Implies(a, b[99]))                            Alias Resolution     GreaterEq: Field     Field     Bool
                                 for i in range(100):                                 Constraint Analysis
                                    if i < 10:
                                        engine.add(c[i] >= d[i])                                                               Knowledge
                                                                                                             Retrieve
                                 return engine                                                                                   Base
                                                                         Compile
      [Prompt] Given this problem, please formulate                    Failure                      Toimplement
                                                                                                    To implement...,
                                                                                                                 ...,please
                                                                                                                      please...
                                                                                                                             ...
      the verification constraints using ZKSL...

              [Prompt] Given this program,              OK                                           [Prompt] Given the knowledge and the
              provide an example case...                                     Code                    task, please write ZK program...
                                                             Compile
                               Success                                                               [Prompt] Read the error logs / error case
                                                        Failed
                                                                                                     and repair the program...
       Case                    Failed
                     Execute             Error Log / Case          Repair within Budget              ❸ Interactive Generation and Repair
                     (Prove)



                                   Fig. 7. Illustrative Overview on the Design of ZK-Coder.


  Program            𝑃    ::=      def verify(engine, 𝑥 1 :𝜏1, . . . , 𝑥𝑛 :𝜏𝑛 ) : 𝑆 ∗
       Type           𝜏   ::=      Field | Bool | Vec[𝜏]
      Stmt            𝑆   ::=      𝑥 = 𝐸 | engine.add(Φ) | for 𝑥 in 𝑅 : 𝑆 ∗ | if Φ : 𝑆 ∗ [else : 𝑆 ∗ ] | return engine
     Range           𝑅    ::=      range(𝐸) | range(𝐸, 𝐸)
   Formula           Φ    ::=      𝐴0 | not Φ | Φ and Φ | Φ or Φ | all(Φ for 𝑥 in 𝑅) | any(Φ for 𝑥 in 𝑅)
      Atom          𝐴0    ::=      𝐸 ⊲⊳ 𝐸 | 𝐺 (𝐸 1, . . . , 𝐸𝑛 )
      Expr           𝐸    ::=      𝑛 ∈ Z | True | False | 𝑥 | (𝐸) | 𝐸 + 𝐸 | 𝐸 − 𝐸 | 𝐸 ∗ 𝐸 | 𝐸 / 𝐸 | 𝐸%𝐸 | 𝐸//𝐸 | . . .
     RelOp           ⊲⊳   ::=      == | != | < | <= | > | >= | and | or | xor
 Primitives         𝐺     ::=      distinct(𝐸) | select(𝐸, 𝐸, 𝐸) | abs(𝐸) | sum(𝐸 for 𝑥 in 𝑅) | . . .


                                 Fig. 8. The Abstract Grammar of the ZK Sketch Language.

target code. It allows LLMs to decouple algebraic reasoning from the implementation-level details
(e.g., signal wiring and constraint encoding) of specific target DSLs.
   ZK-Coder prompts the LLM to generate these constraint specification sketches directly from
problem descriptions. To ensure the integrity of the sketch, the framework performs automated
syntactic and type/arity consistency checks. If a sketch is found to be invalid, the error trace is fed
back to the model for iterative refinement. By serving as a logical representation, ZKSL decouples
the complex task of algebraic constraint reasoning from the low-level specifics of ZK DSLs (e.g.,
signal wiring and constraint specification formats), reducing the overall generation complexity.
4.2.2 Sketch-guided Analysis and Retrieval. RAG is a powerful technique for grounding LLM gen-
eration in low-resource or domain-specific contexts [33]. ZK-Coder utilizes the ZKSL sketch as
a structural query to bridge the gap between abstract constraint specifications and code imple-
mentations. Since a ZK program is defined by a set of verification constraints composed of atomic
algebraic primitives, the framework traverses the sketch to extract each relation declared via
 engine.add(·) . To ensure precise retrieval, operators are canonicalized by normalizing aliases
(e.g., >= becomes GreaterEqThan) and distinguishing variants based on their arity and field-typing
(e.g., differentiating XOr for Booleans vs. Fields). This stage isolates the constituent units within
each constraint to determine the precise implementation hints required by the target DSL.

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     13


  To support this stage, we curate a knowledge base of verified implementations and idiomatic
usage patterns for the algebraic primitives defined in § 3.1.2. Instead of text-similarity ranking,
ZK-Coder then performs exact-match retrieval for each identified primitive. These patterns are
emitted in the original ZKSL specification order to preserve the program’s logical flow during final
code generation. This structured retrieval effectively grounds the generation process, collapsing
the search space and significantly curbing the model’s tendency to hallucinate incorrect constraint
semantics or signal-handling logic.
4.2.3 Interactive Refinement Loop. While the sketch provides a logical blueprint, our findings in
§ 3.4 and § 3.5 reveal a persistent gap: many generated programs successfully satisfy DSL grammar
rules but fail to faithfully encode the intended verification relation. Unlike mainstream software
where errors often manifest as runtime crashes, ZK programs frequently yield under-constrained
circuits or over-constrained systems, which silently accept invalid witnesses or sometimes reject
valid ones. To bridge this gap, we implement an Interactive Refinement Loop as follows.
(1) Constraint Construction Refinement. The candidate program is first submitted to the target
    compiler (e.g., Circom or Noir) to address DSL-specific failures identified in our study, such
    as signal mismanagement, illegal signal declarations in control flow, or constraint-encoding
    violations. We extract these diagnostic traces to iteratively refine the constraint wirings until
    they’re valid or reach the retry iteration threshold 𝑁 1 (𝑁 1 is set as 8 in our experiments).
(2) Relation Faithfulness Refinement. Once compilable, the framework validates constraint
    faithfulness. The agent generates representative “Acceptance” and “Rejection” test cases to
    verify that the circuit correctly enforces the intended relation, while evaluation test cases
    remain hidden to prevent data-leakage. If any test case fails, the counterexample is fed back to
    re-examine the algebraic constraints. This forms another refinement loop, and we set the retry
    threshold 𝑁 2 as 3 in our experiments.
  The above processes repeat until the program passes all functional checks or the budgets are
exhausted, practically converting failures into guided refinements without manual intervention.

5     Evaluation
We evaluate ZK-Coder on the task of generating zero-knowledge programs from natural language
specifications. Our evaluation is structured around the following research questions, with a focus
on end-to-end generation. To clarify, we do not re-evaluate language knowledge (RQ1) or primitive-
level coding (RQ2): the former is established in § 3.3, and the latter is handled by our sketching
and retrieval mechanism in § 4. Nevertheless, we include an ablation study (RQ5) to quantify the
contribution of each component.
• RQ4 (End-to-End Performance): How does ZK-Coder perform compared to baseline methods
  in generating correct ZK programs?
• RQ5 (Ablation Study): What is the effect of each design component, including the ZK sketch
  language, constraint-guided retrieval, and the interactive repair loop?
• RQ6 (Robust Generalization): How well does ZK-Coder generalize to novel, complex compu-
  tational tasks and real-world production-grade ZKP implementations?
• RQ7 (Failure Analysis): When ZK-Coder fails, what are common failure patterns, and how
  might they inform future research?

5.1    Experimental Setup
Our experiments are organized according to the research questions outlined above. For RQ4
(End-to-End Performance), we evaluate on the adapted HumanEval benchmark from ZK-Eval,

                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
14      Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


using the same four models from our measurement study. This comparison establishes how well
ZK-Coder outperforms baseline methods in generating correct and provable ZK programs.
  For RQ5 (Ablation Study), we conduct an ablation study on all four models, selectively disabling
each design component of ZK-Coder, including the sketch language, constraint-guided retrieval,
and the interactive repair loop. This aims to quantify their individual impact on overall performance.
  For RQ6 (Robust Generalization), we construct a new dataset following the adaptation method-
ology of ZK-Eval using LiveCodeBench. Unlike the simple and potentially contaminated Hu-
manEval, this benchmark contains harder, contamination-free, and more recent tasks. We evaluate
whether ZK-Coder continues to maintain high performance under more challenging scenarios.
  Finally, for RQ7 (Failure Analysis), we analyze cases where ZK-Coder fails, categorizing the
dominant error patterns and their underlying causes. This analysis highlights limitations of the
current pipeline and suggests avenues for future research.
  All experiments are conducted under a fixed repair budget (see § 4.2.3). The evaluation is
conducted on a Linux (Ubuntu 22.04 LTS) server equipped with 256 GiB of RAM.

5.2    RQ4: End-to-End Performance
We evaluate ZK-Coder’s end-to-end performance. To the best of our knowledge, since no prior
work directly addresses ZK program generation from natural language, we establish a simple but
meaningful baseline: prompting the model to generate ZK code directly from task descriptions,
with a summary of the target DSL’s grammar and few-shot examples. This setting captures the raw
capability of LLMs as a lower bound. We provide more baselines in § 5.3.
   We meticulously document the performance for the pipeline in three key stages: (1) Sketch
correctness measures whether the initial constraint sketch (in ZKSL) produced from the natural
language description is correct by passing all hidden test cases; (2) Repair pass rate is conditioned on
all correctly generated sketches, and reports the fraction of these that can be successfully repaired
by the interactive repair loop; (3) Program correctness is conditioned on all successfully repaired
programs, and measures the proportion that pass all hidden test cases. The final overall accuracy
aggregates across the full pipeline, reflecting end-to-end program generation accuracy. In addition,
we report the average token cost for each model, which quantifies the spending.

         Table 2. Comparative Per-stage Performance (Accuracy, Tokens) of ZK-Coder and Baseline.

                                   ZK-Coder Per-stage Performance       ZK-Coder Overall        Baseline
 Language          Model          (1) Sketch (2) Repair (3) Program     Accuracy  Avg.      Accuracy Avg.
                                 Correctness Pass Rate Correctness      (Pass@1) Token      (Pass@1) Token
                GPT-o4-mini         94.12%          91.72%     96.25%    83.38%   2350.31    17.35%   436.98
                  GPT-o3            97.30%          94.41%     95.64%    87.85%   2155.39    20.29%   433.35
     Circom
                Deepseek V3         72.15%          92.77%     74.10%    49.60%   2958.72     7.35%   325.28
                  Qwen 3            68.12%          79.07%     78.78%    42.43%   4979.72     4.90%   162.83
                GPT-o4-mini         94.12%          97.97%     96.38%    88.87%    648.95    32.21%   152.18
                  GPT-o3            97.94%          99.85%    100.00%    97.79%    750.63    28.38%   191.72
      Noir
                Deepseek V3         74.88%          93.36%     94.31%    68.66%    628.69    16.18%   100.91
                  Qwen 3            66.84%          91.88%     89.14%    54.74%   1260.43    11.27%   104.24


   Table 2 summarizes the comparative performance of ZK-Coder. Across all tested models and
languages, ZK-Coder achieves substantial gains over the baseline. On Circom, GPT-o3 leads with
87.85% accuracy, while open-weight models (DeepSeek V3, Qwen 3) improve from below 10%
baseline to 49.60% and 42.43%, respectively. On Noir, success rates are higher overall, likely due
to its Rust-like syntax being better aligned with pretraining data. GPT-o3 still leads with 97.79%

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                                                             15


accuracy, and GPT-o4-mini achieves 88.87%. Open-weight models also show strong gains: Qwen 3
improves from 11.27% to 54.74%, and DeepSeek V3 from 16.18% to 68.66%.
   The per-stage breakdown highlights the robustness of the pipeline. OpenAI models show excep-
tional “zero-shot” capabilities in sketching constraints, while open-weight models exhibit lower
correctness rates, suggesting that the leap from natural language to abstract constraint logic remains
a challenge for these models. The repair loop maintains strong success rates, exceeding 90% in most
settings, though Qwen 3 on Circom achieves 79.07%, indicating some difficulty in recovering from
initial errors. Final program correctness is high across most configurations, though DeepSeek V3
and Qwen 3 show comparatively lower rates on Circom, suggesting challenges in implementing
correct constraint logic. Overall, the integration of sketching, repair, and semantic validation yields
consistently executable and provable programs across the majority of settings.
   We also note that ZK-Coder incurs a higher token cost compared to the baseline, which is
expected since our agentic pipeline includes sketching, RAG and interactive repair. However, the
cost remains modest in practice, with each task requiring fewer than 5,000 tokens on average,
corresponding to less than 0.1 USD per task, making the gains in correctness highly cost-effective.

  Answer to RQ4: ZK-Coder delivers a significant improvement in end-to-end performance
  over the baseline method. These results confirm that our pipeline substantially enhances the
  performance on LLM-generating ZK programs.

5.3                   RQ5: Ablation Study


                    1.0
                                                                               Circom            Noir
Accuracy (Pass@1)




                    0.8            76.87%          72.00%                                        76.00%          74.59%
                          65.66%                                 64.63%                 64.48%
                    0.6                                                                                                             59.80%
                                          53.04%                                                        51.42%
                                                        46.37%                                                             43.31%
                    0.4
                                                                      26.04% 27.12%                                                               21.40%
                    0.2                                                                                                                  12.48%
                    0.0
                            No Ablation      (V1) No        (V2) No         (V3) No         (V4) No     (V5) Similarity-     (V6) Only       Baseline
                                              RAG            Sketch       Compile-Repair Execute-Repair based RAG              Repair


                            Fig. 9. Accuracy Comparison of ZK-Coder Ablation Variants (Averaged Across Models).

   To assess the role of each major component in ZK-Coder, we conduct an ablation study where
individual modules are disabled or replaced. The following variants are considered:
• No RAG (V1): Disables sketch-guided RAG for algebraic primitives, forcing the model to rely
  solely on its internal knowledge.
• No Sketch (V2): Removes the intermediate ZK constraint sketching and directly prompts the
  model to output full programs with RAG and the interactive repair loop.
• No Compile-Repair (V3): Eliminates the interactive repair loop for compiler-identified errors.
• No Execute-Repair (V4): Retains compiler-guided repair but disables execution and repair.
• Similarity-based RAG (V5): Replaces our sketch-guided retrieval with a naive text-embedding
  similarity retrieval on the task description.
• Only Repair (V6): Omits both retrieval and sketching, relying exclusively on test-and-repair.
   Figure 9 presents the Pass@1 accuracy for each ablation variant across Circom and Noir. The
results show that every component plays a critical role in the overall success of ZK-Coder. Starting

                                                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
16       Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


from a full-system average of 65.66% on Circom and 76.87% on Noir, we observe that removing
RAG on primitives (V1) causes a significant drop to 53.04% and 72.00% respectively. Disabling the
constraint sketching stage (V2) causes further degradation (46.37% on Circom, 64.63% on Noir),
highlighting the value of sketching as a scaffold for task understanding and constraint modeling.
The most severe drop arises from removing compile-repair (V3), with accuracy falling to 26.04% on
Circom and 27.12% on Noir, demonstrating that interactive repair is indispensable. Disabling execute-
repair (V4) also leads to measurable reductions (64.48% on Circom, 76.00% on Noir), confirming that
semantic validation contributes to robustness. Substituting primitive-in-sketch-guided retrieval
with a text-similarity-based strategy (V5) yields weaker performance (51.42% on Circom, 74.59%
on Noir), suggesting that sketch-guided retrieval is more effective particularly for Circom. Finally,
“Only Repair” (V6) achieves only 43.31% on Circom and 59.80% on Noir, showing that iterative
refinement alone cannot overcome the “computation-to-verification” gap. Compared with V6, the
full system achieves an up to 22.35% performance leap with modest token cost (20.46%-29.39%),
confirming that constraint sketching and template retrieval outperform blind repair cycles.

 Answer to RQ5: The ablation study shows that the strong performance of ZK-Coder relies on
 the synergy of sketching, sketch-guided RAG, and interactive repair. Removing or weakening
 any of these components causes noticeable accuracy drops.

5.4     RQ6: Robust Generalization
Our adapted HumanEval serves as a controlled benchmark to evaluate the core computation-to-
verification shift. To evaluate the robustness of ZK-Coder across varying levels of difficulty and
practical contexts, we extend our analysis to two additional datasets: (i) LiveCodeBench [27], which
focuses on high-complexity algorithmic challenges to assess the limits of the framework’s reasoning;
and (ii) a set of Production Case Studies curated from 37 open-source ZKP repositories. To ensure
the case studies are representative and avoid selection bias, we employed a reproducible filtering
process targeting high-frequency circuit patterns such as Merkle verification, state nullification,
etc. Details are provided in the Supplementary Material.


      Table 3. Generality Study on ZK-Coder’s Code Generation Performance (Averaged Across Models).

                               LiveCodeBench                          Production Coding Pattern Case Studies
 Language
              ZK-Coder      Repairing Baseline Simple Baseline    ZK-Coder Repairing Baseline Simple Baseline
     Circom      44.10%            14.07%                 1.72%    90.83%         83.33%           27.50%
      Noir       56.93%            33.95%                 9.89%    92.09%         89.17%           31.67%




   We establish two baselines: the Simple Baseline (direct generation) and the Repairing Baseline
(adding the interactive repair loop). Table 3 presents the results. On LiveCodeBench, ZK-Coder
achieves a dramatic performance leap, reaching 44.10% on Circom and 56.93% on Noir, significantly
outperforming the Repairing Baseline (14.07% and 33.95%). On Production Case Studies, ZK-Coder
reaches near-perfect success rates (90.83% on Circom and 92.09% on Noir). While the Repairing
Baseline also performs strongly, this high baseline is expected, as these studies focus on standardized,
commonly used verification patterns in a controlled context where the high-level logic is well-
defined. Nevertheless, ZK-Coder achieves a noticeable gain by bridging the “last mile” of correctness,
reducing subtle field-level constraint errors that persist in the baselines.

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                         17


 Answer to RQ6: Results from LiveCodeBench and production case studies confirm that ZK-
 Coder generalizes effectively across a spectrum of challenges, from high-complexity verification
 logic to standardized production coding patterns.

5.5    RQ7: Failure Analysis

         Table 4. Distribution of ZK-Coder’s Code Generation Failures (Averaged Across Models).

                   ➀ Repair         ➁ Sketched           ➂ False Acceptance    ➃ False Rejection     ➄ Mixed False
      Language
                 Budget Exceed   Constraint Incorrect   (Under-constrained)   (Over-constrained)       Acc / Rej
       Circom       31.67%              41.56%                 1.08%                 19.78%               5.92%
        Noir        12.60%              73.07%                 1.67%                 10.89%               1.78%



   Table 4 reports the distribution of ZK-Coder’s failure cases. Each column corresponds to a distinct
failure mode. Repair Budget Exceed indicates cases where the repair budget was exhausted without
producing any compilable program. Sketch Incorrect denotes that the generated constraint sketch
failed hidden test cases, suggesting an incorrect specification of the verification constraints. False
Acceptance corresponds to programs that erroneously accept invalid witnesses, while False Rejection
refers to programs that incorrectly reject valid witnesses. Mixed False Acc / Rej captures programs
that simultaneously exhibit both types of errors, reflecting severe constraint mis-specification.
   The data reveal that the two dominant sources of failures are ➀ and ➁. In both Circom and Noir,
these two together account for over 70% of failures. Failure ➀ often arises when the model is unable
to generate any compilable program, which is due to gaps in pretraining exposure to ZK-specific
constructs. Failure ➁, on the other hand, reflects errors in correctly modeling the verification
constraints from natural language descriptions. The less frequent categories (➂, ➃, ➄) typically
stem from incorrect constraint enforcement when translating a valid sketch into a concrete circuit.
These errors indicate local implementation mistakes rather than systemic failures of the pipeline.

 Answer to RQ7: In summary, Repair Budget Exceed and Sketched Constraint Incorrect constitute
 the most critical bottlenecks. The former highlights the need for more ZK-specific training data
 to improve raw generation capabilities, while the latter underscores the difficulty of grounding
 natural language descriptions in precise verification constraints.

6     Related Work
   LLM for DSL Code Generation. Emerging research has investigated the use of LLMs for generating
code in DSLs, a task made challenging by limited training data and specialized syntax [20, 33].
To mitigate these difficulties, grammar prompting [64], RAG techniques [4, 48], iterative refine-
ment [16], and knowledge transfer methods [5, 42] have been proposed. While most of these
methods (except knowledge transfer methods, which target mainstream computational languages)
can be adapted for ZKP code generation, our ablation study (§ 5.3) shows they remain ineffective.
ZK-Coder advances this area by designing a system tailored to the constraint paradigm of ZKPs.
   Code Generation Benchmarks. Most benchmarks for LLM-based code generation focus on general-
purpose languages [10, 27], with limited support for DSLs. A recent survey [33] reviews existing
DSL benchmarks and emphasizes the lack of standardized evaluation resources, highlighting the
need for benchmarks that capture DSL-specific paradigms, idioms, and practical applications. In
the case of ZKPs, to our knowledge, no systematic benchmark exists for ZKP code generation that
reflects ZK-specific requirements, namely proving a computation, a static arithmetic-circuit model,

                                                               , Vol. 1, No. 1, Article . Publication date: February 2026.
18      Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


and correctness defined by both acceptance and rejection. We provide a solution for this gap with
ZK-Eval, studying code generation bottlenecks and evaluating end-to-end tasks.
   Software Engineering for ZKP. The software engineering community has recently begun to
explore tools and methodologies for ZKP development, with significant emphasis on security.
Static analysis tools such as Circomspect [14], ZKAP [69], QED2 [46], CCC-Check [34], and halo2-
analyzer [55] identify specific vulnerability patterns, while testing tools [7, 58, 71] use fuzzing to
expose security issues. These tools are invaluable for post-hoc analysis and verification, and can be
integrated into our system for further security assurance. Our work complements these efforts by
focusing on the generation phase, leveraging LLMs’ capabilities to reduce engineering burden.

7    Discussion and Limitations
   ZKP Program Efficiency. Program efficiency for ZKPs is measured by the size of arithmetic circuits,
which directly determines prover cost and overall performance. To reduce circuit size, a range of
compilers have been proposed to optimize circuit construction [3, 45, 56], while new protocols
reduce cost through advanced arithmetizations with custom gates and lookup arguments [9, 18]. On
the programmer side, several techniques further improve efficiency, such as adopting ZK-friendly
hash functions [22], gate packing, and aggregating bits into single field elements. For LLM-based
code generation, however, producing efficient circuits is more challenging than generating correct
ones. As future work, we plan to survey optimization techniques and guide LLMs on this.
   LLM Training and Fine-tuning. Recent studies show that LLMs struggle with DSLs and other low-
resource languages due to the lack of high-quality training data [33], a challenge that is particularly
acute in the context of ZKPs [52]. This scarcity also limits the feasibility of fine-tuning approaches.
Our work takes a step toward mitigating this limitation by systematizing the generation of program
examples in ZK DSLs, which can support targeted training and domain adaptation of LLMs. These
examples can serve as a complementary resource for future research in ZK code generation.
   Real-World Representativeness. We examine the representativeness and scope of our evaluation
along two complementary dimensions. First, from a structural standpoint, the programs generated
in § 5.4 exhibit an average cyclomatic complexity of 22.81, which exceeds the average observed in
production-grade open-source ZK repositories (16.8 for Noir and 17.5 for Circom). This indicates
that our benchmarks not only mirror but often surpass the structural depth of real-world ZK logic.
Second, while our tasks are designed to isolate the core challenge of constraint specification, our
evaluation is not “API-blind.” We recognize that LLM capabilities in standard and cryptographic
API usage are already well established in prior work [49, 67, 78, 79]. Consequently, our test suite
focuses on verifying that these APIs are integrated correctly within the circuit logic, covering a
considerable number of real-world in-circuit invocations such as cryptographic primitives and
data-processing utilities. This dual focus ensures that ZK-Coder is evaluated against the rigorous
logical demands of production-level ZK development.

   Threats to Validity. We identify these potential threats. ➀ Our language-knowledge study uses
multiple-choice QA items that were initially generated with LLM assistance. To mitigate bias and
errors, we performed iterative human validation and cross-checking; while some residual noise may
remain, we expect it to have limited impact on the reported trends. ➁ The ZK-Eval assessment uses
hand-crafted test cases that exercise both accepting and rejecting behaviors of generated programs
and primitive usages. Although tests cannot prove correctness, they include representative corner
cases and explicit checks for soundness and completeness, which substantially reduce the risk of
false positives. The high mutation detection rate reported in § 3.1.3, achieved through oracle-guided
mutation testing, further supports this claim by demonstrating strong sensitivity to subtle constraint
specification errors. ➂ The reliability of our automated evaluation depends on test-case coverage.

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                            19


We mitigate this through extensive cross-validation and edge-case injection, achieving a high
mutation score. While this is not a formal proof of logical equivalence, it provides strong empirical
assurance of correctness. ➃ The choice of prompting strategy may influence LLM performance.
We employ standard zero-shot and few-shot prompting techniques without extensive prompt
engineering or fine-tuning. To ensure experimental integrity, we verified that no test cases or
ground-truth solutions were included in the prompts, preventing information leakage that could
artificially inflate success rates. ➄ Security is critical for ZKPs. While integration with auditing
tools [34, 46] could further enhance assurance, code generation from natural language specifications
may face inherent ambiguity and underspecification. Users must exercise caution and validate
generated code before deployment in security-critical application.

8   Conclusion
We presented ZK-Eval, the first benchmark for assessing LLM capability in ZK program generation,
revealing that models struggle with composing algebraic primitives for verification constraints.
To address this, we introduce ZK-Coder, which guides LLMs from constraint sketches to exe-
cutable code through sketch-guided retrieval and iterative refinement, significantly improving code
generation for both Circom and Noir.

References
 [1] Zahra Abbasiantaeb, Yifei Yuan, Evangelos Kanoulas, and Mohammad Aliannejadi. 2024. Let the llms talk: Simulating
     human-to-human conversational qa via zero-shot llm-to-llm interactions. In Proceedings of the 17th ACM International
     Conference on Web Search and Data Mining. 8–17.
 [2] Seif Abukhalaf, Mohammad Hamdaqa, and Foutse Khomh. 2023. On Codex prompt engineering for OCL generation: an
     empirical study. In 2023 IEEE/ACM 20th International Conference on Mining Software Repositories (MSR). IEEE, 148–157.
 [3] Aztec Labs. 2025. Noir: A Domain-Specific Language for Zero-Knowledge Programming. https://noir-lang.org.
     Accessed: 2025-08.
 [4] Nastaran Bassamzadeh and Chhaya Methani. 2024. A comparative study of DSL code generation: Fine-tuning vs.
     optimized retrieval augmentation. arXiv preprint arXiv:2407.02742 (2024).
 [5] Federico Cassano, John Gouwar, Francesca Lucchetti, Claire Schlesinger, Anders Freeman, Carolyn Jane Anderson,
     Molly Q Feldman, Michael Greenberg, Abhinav Jangda, and Arjun Guha. 2024. Knowledge transfer from high-resource
     to low-resource programming languages for code llms. Proceedings of the ACM on Programming Languages 8, OOPSLA2
     (2024), 677–708.
 [6] Federico Cassano, John Gouwar, Daniel Nguyen, Sydney Nguyen, Luna Phipps-Costin, Donald Pinckney, Ming-Ho Yee,
     Yangtian Zi, Carolyn Jane Anderson, Molly Q Feldman, Arjun Guha, Michael Greenberg, and Abhinav Jangda. 2022.
     MultiPL-E: A Scalable and Extensible Approach to Benchmarking Neural Code Generation. arXiv:2208.08227 [cs.LG]
     https://arxiv.org/abs/2208.08227
 [7] Stefanos Chaliasos, Imam Al-Fath, and Alastair Donaldson. 2025. Towards Fuzzing Zero-Knowledge Proof Circuits
     (Short Paper). In Proceedings of the 34th ACM SIGSOFT International Symposium on Software Testing and Analysis.
     98–104.
 [8] Stefanos Chaliasos, Jens Ernstberger, David Theodore, David Wong, Mohammad Jahanara, and Benjamin Livshits.
     2024. {SoK}: What Don’t We Know? Understanding Security Vulnerabilities in {SNARKs}. In 33rd USENIX Security
     Symposium (USENIX Security 24). 3855–3872.
 [9] Binyi Chen, Benedikt Bünz, Dan Boneh, and Zhenfei Zhang. 2023. HyperPlonk: Plonk with Linear-Time Prover and
     High-Degree Custom Gates. In Advances in Cryptology - EUROCRYPT 2023: 42nd Annual International Conference on
     the Theory and Applications of Cryptographic Techniques, Lyon, France, April 23–27, 2023, Proceedings, Part II (Lyon,
     France). Springer-Verlag, Berlin, Heidelberg, 499–530. doi:10.1007/978-3-031-30617-4_17
[10] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri Edwards,
     Yuri Burda, Nicholas Joseph, Greg Brockman, et al. 2021. Evaluating large language models trained on code. arXiv
     preprint arXiv:2107.03374 (2021).
[11] Peter Clark, Isaac Cowhey, Oren Etzioni, Tushar Khot, Ashish Sabharwal, Carissa Schoenick, and Oyvind Tafjord.
     2018. Think you have solved question answering? try arc, the ai2 reasoning challenge. arXiv preprint arXiv:1803.05457
     (2018).
[12] Noir Contributors. [n. d.]. Noir Examples. https://github.com/noir-lang/noir-examples. Accessed: 2025-08.


                                                                  , Vol. 1, No. 1, Article . Publication date: February 2026.
20      Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


[13] RISC Zero Contributors. 2025. RISC Zero: Universal Zero Knowledge. https://risczero.com/.
[14] Fredrick Dahlgren. 2022. It pays to be Circomspect. https://blog.trailofbits.com/2022/09/15/it-pays-to-be-circomspect/.
[15] Xun Deng, Sicheng Zhong, Honghua Dong, Jingyu Hu, Sidi Mohamed Beillahi, Xujie Si, and Fan Long. 2024. Assessing
     code generation with intermediate languages. arXiv preprint arXiv:2407.05411 (2024).
[16] Yangruibo Ding, Marcus J. Min, Gail Kaiser, and Baishakhi Ray. 2024. CYCLE: Learning to Self-Refine the Code
     Generation. Proc. ACM Program. Lang. 8, OOPSLA1, Article 108 (April 2024), 27 pages. doi:10.1145/3649825
[17] Yihong Dong, Xue Jiang, Jiaru Qian, Tian Wang, Kechi Zhang, Zhi Jin, and Ge Li. 2025. A Survey on Code Generation
     with LLM-based Agents. arXiv preprint arXiv:2508.00083 (2025).
[18] Ariel Gabizon, Zachary J. Williamson, and Oana-Madalina Ciobotaru. 2019. PLONK: Permutations over Lagrange-
     bases for Oecumenical Noninteractive arguments of Knowledge. IACR Cryptol. ePrint Arch. 2019 (2019), 953. https:
     //api.semanticscholar.org/CorpusID:201685538
[19] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yixin Dai, Jiawei Sun, Haofen Wang, and Haofen
     Wang. 2023. Retrieval-augmented generation for large language models: A survey. arXiv preprint arXiv:2312.10997 2, 1
     (2023).
[20] Alessandro Giagnorio, Alberto Martin-Lopez, and Gabriele Bavota. 2025. Enhancing code generation for low-resource
     languages: No silver bullet. arXiv preprint arXiv:2501.19085 (2025).
[21] GitHub. 2025. GitHub Copilot. https://github.com/features/copilot.
[22] Lorenzo Grassi, Dmitry Khovratovich, Christian Rechberger, Arnab Roy, and Markus Schofnegger. 2021. Poseidon: A
     new hash function for {Zero-Knowledge} proof systems. In 30th USENIX Security Symposium (USENIX Security 21).
     519–535.
[23] Sandeep Gupta. 2025. Zero-Knowledge Proofs for Privacy-Preserving Systems: A Survey Across Blockchain, Identity,
     and Beyond. Engineering and Technology Journal 10, 07 (July 2025), 5755–5761. doi:10.47191/etj/v10i07.23
[24] Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. 2020.
     Measuring massive multitask language understanding. arXiv preprint arXiv:2009.03300 (2020).
[25] Christoph Hochrainer, Anastasia Isychev, Valentin Wüstholz, and Maria Christakis. 2024. Fuzzing Processing Pipelines
     for Zero-Knowledge Circuits. arXiv preprint arXiv:2411.02077 (2024).
[26] iden3. 2025. circomlib: Standard Library for the Circom Language. https://github.com/iden3/circomlib. Accessed:
     2025-08-27.
[27] Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik
     Sen, and Ion Stoica. 2024. Livecodebench: Holistic and contamination free evaluation of large language models for
     code. arXiv preprint arXiv:2403.07974 (2024).
[28] Zimo Ji, Daoyuan Wu, Wenyuan Jiang, Pingchuan Ma, Zongjie Li, and Shuai Wang. 2025. Measuring and Augmenting
     Large Language Models for Solving Capture-the-Flag Challenges. arXiv preprint arXiv:2506.17644 (2025).
[29] Jinan Jiang, Xinghao Peng, Jinzhao Chu, and Xiapu Luo. 2025. ConsCS: Effective and Efficient Verification of Circom
     Circuits. In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE). IEEE Computer Society,
     737–737.
[30] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. 2024. A survey on large language models for code
     generation. arXiv preprint arXiv:2406.00515 (2024).
[31] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. 2025. A Survey on Large Language Models for
     Code Generation. ACM Trans. Softw. Eng. Methodol. (July 2025). doi:10.1145/3747588 Just Accepted.
[32] Xue Jiang, Yihong Dong, Lecheng Wang, Zheng Fang, Qiwei Shang, Ge Li, Zhi Jin, and Wenpin Jiao. 2024. Self-Planning
     Code Generation with Large Language Models. ACM Trans. Softw. Eng. Methodol. 33, 7, Article 182 (Sept. 2024),
     30 pages. doi:10.1145/3672456
[33] Sathvik Joel, Jie JW Wu, and Fatemeh H Fard. 2024. A survey on llm-based code generation for low-resource and
     domain-specific programming languages. arXiv preprint arXiv:2410.03981 (2024).
[34] Arman Kolozyan, Bram Vandenbogaerde, Janwillem Swalens, Lode Hoste, Stefanos Chaliasos, and Coen De Roover.
     2025. Language-Agnostic Detection of Computation-Constraint Inconsistencies in ZKP Programs via Value Inference.
     Cryptology ePrint Archive (2025).
[35] Succinct Labs. 2025. SP1: A Rust-based framework for zero-knowledge proofs. https://github.com/succinctlabs/sp1.
[36] Ryan Lavin, Xuekai Liu, Hardhik Mohanty, Logan Norman, Giovanni Zaarour, and Bhaskar Krishnamachari. 2024. A
     survey on the applications of zero-knowledge proofs. arXiv preprint arXiv:2408.00243 (2024).
[37] Jia Li, Ge Li, Yongmin Li, and Zhi Jin. 2023. Structured Chain-of-Thought Prompting for Code Generation.
     arXiv:2305.06599 [cs.SE] https://arxiv.org/abs/2305.06599
[38] Bang Liu, Haojie Wei, Di Niu, Haolan Chen, and Yancheng He. 2020. Asking questions the human way: Scalable
     question-answer generation from text corpus. In Proceedings of the web conference 2020. 2032–2043.
[39] Kaiyuan Liu, Youcheng Pan, Yang Xiang, Daojing He, Jing Li, Yexing Du, and Tianrun Gao. 2025. ProjectEval:
     A Benchmark for Programming Agents Automated Evaluation on Project-Level Code Generation. arXiv preprint


, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                              21


     arXiv:2503.07010 (2025).
[40] Mingjie Liu, Nathaniel Pinckney, Brucek Khailany, and Haoxing Ren. 2023. Verilogeval: Evaluating large language
     models for verilog code generation. In 2023 IEEE/ACM International Conference on Computer Aided Design (ICCAD).
     IEEE, 1–8.
[41] Lin Long, Rui Wang, Ruixuan Xiao, Junbo Zhao, Xiao Ding, Gang Chen, and Haobo Wang. 2024. On llms-driven
     synthetic data generation, curation, and evaluation: A survey. arXiv preprint arXiv:2406.15126 (2024).
[42] Federico Mora, Justin Wong, Haley Lepe, Sahil Bhatia, Karim Elmaaroufi, George Varghese, Joseph E Gonzalez,
     Elizabeth Polgreen, and Sanjit A Seshia. 2024. Synthetic programming elicitation for text-to-code in very low-resource
     programming and formal languages. Advances in Neural Information Processing Systems 37 (2024), 105151–105170.
[43] Aidar Myrzakhan, Sondos Mahmoud Bsharat, and Zhiqiang Shen. 2024. Open-llm-leaderboard: From multi-choice to
     open-style questions for llms evaluation, benchmark, and arena. arXiv preprint arXiv:2406.07545 (2024).
[44] Vivian Plasencia Nico Serrano. [n. d.]. ZK-Kit: A monorepo of reusable libraries for zero-knowledge technologies.
     https://github.com/zk-kit/zk-kit. Accessed: 2025-08.
[45] Alex Ozdemir, Fraser Brown, and Riad S Wahby. 2022. CirC: Compiler infrastructure for proof systems, software
     verification, and more. In 2022 IEEE Symposium on Security and Privacy (SP). IEEE, 2248–2266.
[46] Shankara Pailoor, Yanju Chen, Franklyn Wang, Clara Rodríguez, Jacob Van Geffen, Jason Morton, Michael Chu, Brian
     Gu, Yu Feng, and Işıl Dillig. 2023. Automated detection of under-constrained circuits in zero-knowledge proofs.
     Proceedings of the ACM on Programming Languages 7, PLDI (2023), 1510–1532.
[47] Ruwei Pan, Hongyu Zhang, and Chao Liu. 2025. CodeCoR: An LLM-based self-reflective multi-agent framework for
     code generation. arXiv preprint arXiv:2501.07811 (2025).
[48] Sameer Pimparkhede, Mehant Kammakomati, Srikanth Tamilselvam, Prince Kumar, Ashok Pon Kumar, and Pushpak
     Bhattacharyya. 2024. DocCGen: Document-based Controlled Code Generation. arXiv:2406.11925 [cs.SE] https:
     //arxiv.org/abs/2406.11925
[49] Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, et al.
     2023. Toolllm: Facilitating large language models to master 16000+ real-world apis. arXiv preprint arXiv:2307.16789
     (2023).
[50] Google Research. 2021. MBPP: Mostly Basic Python Problems Dataset. https://github.com/google-research/google-
     research/tree/master/mbpp. Accessed: 2025-08.
[51] Microsoft Research. [n. d.]. Z3 API in Python. https://ericpony.github.io/z3py-tutorial/guide-examples.htm. Accessed:
     2025-08.
[52] Nojan Sheybani, Anees Ahmed, Michel Kinsy, and Farinaz Koushanfar. 2025. Zero-Knowledge Proof Frameworks: A
     Systematic Survey. arXiv:2502.07063 [cs.CR] https://arxiv.org/abs/2502.07063
[53] Mohammed Latif Siddiq, Joanna Santos, Ridwanul Hasan Tanvir, Noshin Ulfat, Fahmid Al Rifat, and V Carvalho Lopes.
     2023. Exploring the effectiveness of large language models in generating unit tests. arXiv preprint arXiv:2305.00418 1, 3
     (2023).
[54] P. D. Sirin. [n. d.]. Circom Example. https://github.com/pisuthd/circom-example. Accessed: 2025-08.
[55] Fatemeh Heidari Soureshjani, Mathias Hall-Andersen, MohammadMahdi Jahanara, Jeffrey Kam, Jan Gorzny, and
     Mohsen Ahmadvand. 2023. Automated analysis of halo2 circuits. Cryptology ePrint Archive (2023).
[56] Marco Stronati, Denis Firsov, Antonio Locascio, and Benjamin Livshits. 2024. Clap: a Semantic-Preserving Optimizing
     eDSL for Plonkish Proof Systems. arXiv preprint arXiv:2405.12115 (2024).
[57] Haochen Sun, Jason Li, and Hongyang Zhang. 2024. zkLLM: Zero Knowledge Proofs for Large Language Models.
     arXiv:2404.16109 [cs.LG] https://arxiv.org/abs/2404.16109
[58] Hideaki Takahashi, Jihwan Kim, Suman Jana, and Junfeng Yang. 2025. zkFuzz: Foundation and Framework for Effective
     Fuzzing of Zero-Knowledge Circuits. arXiv preprint arXiv:2504.11961 (2025).
[59] Cursor team. 2025. Cursor. https://cursor.com.
[60] Tangem team. 2024. Zero-Knowledge Proofs in Blockchain: Beyond Privacy to Scalability and Security. https:
     //tangem.com/en/blog/post/zero-knowledge-proofs-in-blockchain-beyond-privacy-to-scalability-and-security/
[61] ERHAN TEZCAN. 2025. Circom 101. https://circom.erhant.me/. Accessed: 2025-08.
[62] ERHAN TEZCAN. 2025. Circomkit Examples. https://github.com/erhant/circomkit-examples/. Accessed: 2025-08.
[63] Thor. [n. d.]. Circuit Examples. https://github.com/thor314/circuit-examples. Accessed: 2025-08.
[64] Bailin Wang, Zi Wang, Xuezhi Wang, Yuan Cao, Rif A Saurous, and Yoon Kim. 2023. Grammar prompting for domain-
     specific language generation with large language models. Advances in Neural Information Processing Systems 36 (2023),
     65030–65055.
[65] Evan Wang, Federico Cassano, Catherine Wu, Yunfeng Bai, Will Song, Vaskar Nath, Ziwen Han, Sean Hendryx,
     Summer Yue, and Hugh Zhang. 2024. Planning in natural language improves llm search for code generation. arXiv
     preprint arXiv:2409.03733 (2024).



                                                                    , Vol. 1, No. 1, Article . Publication date: February 2026.
22      Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


[66] Shiqi Wang, Zheng Li, Haifeng Qian, Chenghao Yang, Zijian Wang, Mingyue Shang, Varun Kumar, Samson Tan,
     Baishakhi Ray, Parminder Bhatia, et al. 2022. ReCode: Robustness evaluation of code generation models. arXiv preprint
     arXiv:2212.10264 (2022).
[67] Yu Wang, Yijian Liu, Liheng Ji, Han Luo, Wenjie Li, Xiaofei Zhou, Chiyun Feng, Puji Wang, Yuhan Cao, Geyuan Zhang,
     et al. 2025. AICrypto: A comprehensive benchmark for evaluating cryptography capabilities of large Language models.
     arXiv preprint arXiv:2507.09580 (2025).
[68] Yanlin Wang, Wanjun Zhong, Yanxian Huang, Ensheng Shi, Min Yang, Jiachi Chen, Hui Li, Yuchi Ma, Qianxiang
     Wang, and Zibin Zheng. 2025. Agents in software engineering: Survey, landscape, and vision. Automated Software
     Engineering 32, 2 (2025), 1–36.
[69] Hongbo Wen, Jon Stephens, Yanju Chen, Kostas Ferles, Shankara Pailoor, Kyle Charbonnet, Isil Dillig, and Yu Feng.
     2024. Practical Security Analysis of {Zero-Knowledge} Proof Circuits. In 33rd USENIX Security Symposium (USENIX
     Security 24). 1471–1487.
[70] Jiaxin Wen, Jian Guan, Hongning Wang, Wei Wu, and Minlie Huang. 2024. Unlocking reasoning potential in large
     langauge models by scaling code-form planning. arXiv preprint arXiv:2409.12452 (2024).
[71] Dongwei Xiao, Zhibo Liu, Yiteng Peng, and Shuai Wang. 2025. Mtzk: Testing and exploring bugs in zero-knowledge
     (zk) compilers. In NDSS.
[72] Pei Xu, Yulei Sui, and Mark Staples. 2025. Towards Source Mapping for Zero-Knowledge Smart Contracts: Design and
     Preliminary Evaluation. In Proceedings of the 34th ACM SIGSOFT International Symposium on Software Testing and
     Analysis. 200–209.
[73] John Yang, Akshara Prabhakar, Karthik Narasimhan, and Shunyu Yao. 2023. InterCode: standardizing and benchmarking
     interactive coding with execution feedback. In Proceedings of the 37th International Conference on Neural Information
     Processing Systems (New Orleans, LA, USA) (NIPS ’23). Curran Associates Inc., Red Hook, NY, USA, Article 1035,
     29 pages.
[74] Zhiqiang Yuan, Yiling Lou, Mingwei Liu, Shiji Ding, Kaixin Wang, Yixuan Chen, and Xin Peng. 2023. No more manual
     tests? evaluating and improving chatgpt for unit test generation. arXiv preprint arXiv:2305.04207 (2023).
[75] Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi. 2019. Hellaswag: Can a machine really finish
     your sentence? arXiv preprint arXiv:1905.07830 (2019).
[76] Kechi Zhang, Jia Li, Ge Li, Xianjie Shi, and Zhi Jin. 2024. CodeAgent: Enhancing Code Generation with Tool-Integrated
     Agent Systems for Real-World Repo-level Coding Challenges. In Proceedings of the 62nd Annual Meeting of the Association
     for Computational Linguistics (Volume 1: Long Papers). 13643–13658.
[77] Shudan Zhang, Hanlin Zhao, Xiao Liu, Qinkai Zheng, Zehan Qi, Xiaotao Gu, Xiaohan Zhang, Yuxiao Dong, and Jie
     Tang. 2024. Naturalcodebench: Examining coding performance mismatch on humaneval and natural user prompts.
     arXiv preprint arXiv:2405.04520 (2024).
[78] Qiming Zhu, Jialun Cao, Yaojie Lu, Hongyu Lin, Xianpei Han, Le Sun, and Shing-Chi Cheung. 2025. Domaineval: An
     auto-constructed benchmark for multi-domain code generation. In Proceedings of the AAAI Conference on Artificial
     Intelligence, Vol. 39. 26148–26156.
[79] Terry Yue Zhuo, Minh Chien Vu, Jenny Chim, Han Hu, Wenhao Yu, Ratnadira Widyasari, Imam Nur Bani Yusuf, Haolan
     Zhan, Junda He, Indraneil Paul, et al. 2024. Bigcodebench: Benchmarking code generation with diverse function calls
     and complex instructions. arXiv preprint arXiv:2406.15877 (2024).


9    Illustrative Workflow Example
We demonstrate the workflow by using ZK-Coder to generate a ZKP program for proving the
correctness of a Sudoku solution in Fig. 10, a classical example in ZKP programming. This example
is deliberately chosen for its simplicity and demonstrative purposes. To clarify, this example is not
part of our evaluation suite.
   The problem is defined as: given a 4 × 4 Sudoku grid, the goal is to verify that each row, column,
and 2 × 2 block contains all digits 1–4 exactly once.
   In this illustrative workflow example, ZK-Coder first reads the problem description and formu-
lates it in ZKSL, encoding the necessary constraints on the Sudoku grid. The checker validates the
sketch and analyzes it to extract the set of algebraic primitives required. For each primitive, rele-
vant implementation hints are retrieved, and an initial Circom/Noir implementation is generated.
The compiler then checks this program for constraint validity, returning diagnostics that guide
interactive refinement. Once the code compiles, the model is prompted to generate a small test
instance (acceptance and rejection). If the resulting prover behavior deviates from expectations, the

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                                                                23


           Given a        Sudoku grid, the goal is to verify that each row,              We have retrieved the usage examples and / or from-scratch
           column, and       block contains all digits       exactly once.               implementations for these algebraic primitives...
 Problem                                                                      Retrival
           I've formulate the constraints using ZKSL:                                    Here is an implementation in Circom for the Sudoku problem...
             def verify(engine, grid: List[List]):                                       pragma circom 2.1.6;
 ZKCoder         engine.add(And(1 <= x, x <= 4)                                          ......
                                                                              ZKCoder
                     for row in grid for x in row)
                 for row in grid:                                                        This program attempts to declare signal in a for-loop, which is
                     engine.add(Distinct(row))                                           not allowed. Please fix that...
                                                                              Compiler
                 for col in zip(*grid):
                     engine.add(Distinct(col))                                           Here is the updated implementation...
                 for i in (0, 2):
                     for j in (0, 2):                                         ZKCoder    Here is a test case that the prover should accept...
                         engine.add(Distinct([grid[i+x][j+y]
                              for x in (0, 1) for y in (0, 1)]))                         This test case gets rejected by the prover, please repair again...
                 return engine                                                Prover
                                                                                         Here is the updated implementation...
           The formulation passed the checker. After analysis, we found
           that it requires And: bool   bool     bool, Distinct: int          ZKCoder
 Checker   bool, and LessEqThan: int int     bool.                                       Great! All oracles have passed. This process is done.




              Fig. 10. ZK-Coder’s Illustrative Example Workflow on Proving Sudoku Correctness.



model is asked to repair the program. This repair loop continues until either the program passes
the LLM-supplied tests or the repair budget is exhausted.
   We also present two concrete program examples generated by ZK-Coder for this Sudoku problem
in Fig. 11, in Circom and Noir respectively. Both programs implement the same verification logic.
We annotated the source code with comments to point out key sections, such as input signal
declarations, primitive imports or implementations, and composing algebraic primitives with field
arithmetic operations to implement the constraints outlined in the ZKSL sketch. For coding tasks
on production and application-specific scenarios, we also provide case studies on frequently used
ZKP coding patterns in production repositories in § 11.

10    Coverage Study on Algebraic Primitives in Real-World Repositories
In this section, we provide the detailed justification and comprehensive listing of the algebraic
primitives used in our study. As detailed in § 3.1.2, we constructed a dataset of algebraic primitives to
evaluate the ability of LLMs to specify verification constraints at the atomic level. These primitives
represent the foundational building blocks of all ZK arithmetic circuits. We present the complete
list of the 35 collected primitives in Table 5.
   Our selection is guided by these principles:
(1) Theoretical Completeness: These primitives are designed to be a functionally complete basis
    for ZK constraint specification. Since ZK programs are ultimately compiled into arithmetic
    circuits over a finite field F𝑝 , any polynomial relation can be decomposed into additions and
    multiplications. By including a broader set of logical, relational, and bitwise operators, we
    ensure that the benchmark can express any NP-complete relation.
(2) Expressiveness: While addition and multiplication are sufficient in theory, practical ZK devel-
    opment relies on higher-order gates (e.g., multiplexors, range-checks) to manage complexity.
    Our set includes these to mirror this practice.
(3) Excluding Application-Specific APIs: We intentionally exclude application-specific APIs (e.g.,
    Merkle tree operations, data-packing, etc.) to focus on the core algebraic atomic primitives
    that underpin all ZK programs and are central to constraint specification. Given that said, we
    still provide evaluations on real-world application-specific API calling scenarios through case
    studies on ZK-Coder in § 11.

                                                                                    , Vol. 1, No. 1, Article . Publication date: February 2026.
24         Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


     Circom Program Implementation on 4             4 Sudoku
 pragma circom 2.1.6;

 include "circomlib/gates.circom";                  Importing template (LessThan)                                           Implementing template
 include "circomlib/comparators.circom";               from standard library.                                           (PairwiseDistinct) from scratch.
 template PairwiseDistinct(n) { /* Detailed from-scratch implementation for this template omitted for brievity */ }

 template Sudoku4x4 () {
                                       Declaring public &                                              Implementing constraint: And(1 <= x, x <= 4) by
     signal input grid[16];
                                      private signal inputs.                                            assembling the LessThan primitive with field
       component range_checks[16][2];                                                     arithmetic and then enforce constraint with ===.
       for (var i = 0; i < 16; i++) {
           range_checks[i][0] = LessThan(32);      range_checks[i][1] = LessThan(32);
           range_checks[i][0].in <== [0, grid[i]];     range_checks[i][1].in <== [grid[i], 5];
           range_checks[i][0].out * range_checks[i][1].out === 1;
       }
                                                                                                       Implementing constraint: row- and column-wise
       component distinct_checks[3][4];                                                   distinct by using the PairwiseDistinct primitive.
       for (var i = 0; i < 4; i++) {
           distinct_checks[0][i] = PairwiseDistinct(4);
           distinct_checks[0][i].in <== [grid[i * 4 + 0], grid[i * 4 + 1], grid[i * 4 + 2], grid[i * 4 + 3]];
           distinct_checks[0][i].out === 1;

           distinct_checks[1][i] = PairwiseDistinct(4);
           distinct_checks[1][i].in <== [grid[0 * 4 + i], grid[1 * 4 + i], grid[2 * 4 + i], grid[3 * 4 + i]];
           distinct_checks[1][i].out === 1;
       }
                                                                                                      Implementing constraint: subgrid-wise distinct by
       for (var i = 0; i < 2; i++) { for (var j = 0; j < 2; j++) {                             using the PairwiseDistinct primitive.
           distinct_checks[2][i * 2 + j] = PairwiseDistinct(4);
           distinct_checks[2][i * 2 + j].in <== [grid[i * 2 + 0], grid[j * 2 + 0], grid[i * 2 + 1], grid[j * 2 + 1]];
           distinct_checks[2][i * 2 + j].out === 1;
       }}
 }
                                                                     Declare which input signals are public.
 component main { public [ grid ] } = Sudoku4x4();


     Noir Program Implementation on 4           4 Sudoku

 fn in_range_1_to_4(x: Field) -> bool {
     ((x as u32) >= 1) & ((x as u32) <= 4)
 }                                                                 Implementing function
                                                               (in_rage_1_to_4) from scratch.
 fn pairwise_distinct4(v: [Field; 4]) -> bool {
     let mut flag: bool = true;
     for i in 0..4 {
                                                   Implementing function
         for j in i..4 {
                                              (pairwise_distinct4) from scratch.
             flag = flag | (v[i] != v[j]);
         }
     }
     flag     Declaring public &
 }              private inputs.
                                                   Implementing constraint: And(1 <= x, x <= 4) by
 fn main(grid: pub [Field; 16]) {                 assembling the in_rage_1_to_4 function (primitive).
     for i in 0..16 {
         assert(in_range_1_to_4(grid[i]));                                                            Implementing constraint: row- and column-wise
     }                                                                                               distinct by using the pairwise_distinct4 function (as
                                                                                                                     algebraic primitive).
       for i in 0..4 {
           assert(pairwise_distinct4([grid[i * 4 + 0], grid[i * 4 + 1], grid[i * 4 + 2], grid[i * 4 + 3]]));
           assert(pairwise_distinct4([grid[0 * 4 + i], grid[1 * 4 + i], grid[2 * 4 + i], grid[3 * 4 + i]]));
       }

       for br in 0..2 {
           for bc in 0..2 {
               let r0 = 2 * br;                                                         Implementing constraint: subgrid-wise distinct by
               let r1 = 2 * br + 1;                                                       assembling the pairwise_distinct4 function (as
               let c0 = 2 * bc;                                                                       algebraic primitive).
               let c1 = 2 * bc + 1;
               assert(pairwise_distinct4([grid[r0 * 4 + c0], grid[r0 * 4 + c1], grid[r1 * 4 + c0], grid[r1 * 4 + c1]]));
           }
       }
 }




            Fig. 11. Example Implementation Generated by ZK-Coder (Upper: Circom, Lower: Noir).




, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     25


              Table 5. List of Collected Algebraic Primitives Used in ZK-Eval and ZK-Coder.

              Name              Category                 Typing                           Source
               And               Logical          Bool × Bool → Bool                   Circomlib
               And∗              Logical       Bool × . . . × Bool → Bool              Circomlib
                Or               Logical          Bool × Bool → Bool                   Circomlib
                Or∗              Logical       Bool × . . . × Bool → Bool              Circomlib
               XOr               Logical          Bool × Bool → Bool                   Circomlib
               XOr∗              Logical       Bool × . . . × Bool → Bool              Circomlib
               Not               Logical              Bool → Bool                      Circomlib
               Or⋄               Bitwise          Field × Field → Field          Completeness Aligning
               Or⋄∗              Bitwise       Field × . . . × Field → Field     Completeness Aligning
              And⋄               Bitwise          Field × Field → Field          Completeness Aligning
              And⋄∗              Bitwise       Field × . . . × Field → Field     Completeness Aligning
              XOr⋄               Bitwise          Field × Field → Field          Completeness Aligning
              XOr⋄∗              Bitwise       Field × . . . × Field → Field     Completeness Aligning
              Equal            Comparison         Field × Field → Bool             Circomlib, ZK-Kit
            NotEqual           Comparison         Field × Field → Bool             Circomlib, ZK-Kit
            LessThan           Comparison         Field × Field → Bool             Circomlib, ZK-Kit
        LessThanOrEqual        Comparison         Field × Field → Bool             Circomlib, ZK-Kit
          GreaterThan          Comparison         Field × Field → Bool             Circomlib, ZK-Kit
       GreaterThanOrEqual      Comparison         Field × Field → Bool             Circomlib, ZK-Kit
               Add             Arithmetic         Field × Field → Field                 ZK-Kit
             Subtract          Arithmetic         Field × Field → Field                 ZK-Kit
             Multiply          Arithmetic         Field × Field → Field                 ZK-Kit
              Divide           Arithmetic         Field × Field → Field                 ZK-Kit
             Modulo            Arithmetic         Field × Field → Field                 ZK-Kit
              Power            Arithmetic         Field × Field → Field                 ZK-Kit
           FloorDivide         Arithmetic         Field × Field → Field                 ZK-Kit
              Negate           Arithmetic             Field → Field                    Circomlib
            Absolute           Arithmetic             Field → Field                    Circomlib
             Inverse           Arithmetic             Field → Field                    Circomlib
               Sign            Arithmetic             Field → Field                    Circomlib
           Conditional         Composite      Bool × Field × Field → Field             Circomlib
          Conditional⋄         Composite      Bool × Bool × Bool → Bool                Circomlib
              Sum∗             Composite       Field × . . . × Field → Field           Circomlib
            Product∗           Composite       Field × . . . × Field → Field     Completeness Aligning
            Distinct∗          Composite       Field × . . . × Field → Field     Completeness Aligning



   To ensure the practical relevance of our primitive set, we conducted a systematic survey of
37 production-grade ZK repositories (listed in Table 6). We collected repositories using GitHub
search for projects implementing Circom or Noir, then filtered out toy, tutorial, and code-analysis
repositories. We further filtered based on popularity, retaining repositories with at least 30 stars
for Circom and 10 stars for Noir, resulting in 19 Circom and 18 Noir repositories. This yielded 408
source files for analysis.
   As shown in Table 7, our primitive set achieves high coverage. We achieve 97.30% and 94.59%
coverage for arithmetic and relational primitives, respectively. These categories form the “logical
heart” of nearly all analyzed 408 source files, appearing in 36 out of 37 repositories. Some categories,
such as Composite (16.22%) and specialized Logical operators (e.g., specific bitwise XORs), show

                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
26        Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


                 Table 6. List of Collected Circom (Upper) / Noir (Lower) Repositories on Github.

                      Name                        Description
                    selfxyz/self                  A passport authentication system using Circom.
                  lyronctk/zator                  Verified inference of a 512-layer neural network using recursive
                                                  SNARKs.
                FlynnSC/zk-hunt                   A prototype for an onchain game, which explores different ZK game
                                                  mechanics and information asymmetry.
           dmpierre/eth-private-market            Circom code using zk-snarks and ethereum for trustlessly selling.
            tiktok-privacy-innovation/            An implementation of trustless attestation verification based on
     trustless-attestation-verification-circom    Circom.
                  nobitex/sigmab                  Circom code on Private Proof of Reserves.
                erhant/zkbrainfuck                A Brainfuck (programming language) interpreter and virtual machine
                                                  implemented in Circom.
             ava-labs/EncryptedERC                The Encrypted ERC-20 (eERC) standard for secure and confidential
                                                  token transfers on Avalanche blockchains.
             zkFHE/circomlib-fhe                  Circom Circuit Library for Fully Homomorphic Encryption.
         microsoft/crescent-credentials           Crescent adds privacy to existing credentials with zero-knowledge.
            holyaustin/ZeroSecret                 A collection of Circom circuits for email verification, hashing, encryp-
                                                  tion, and more.
       inference-labs-inc/subnet-2-circom         source files for the circom implementation of Subnet 2’s incentive mech-
                                                  anism.
               pluto/aes-circuits                 Circom circuits implementing the AES encryption algorithm.
          EkuboProtocol/privacy-pools             Circom project implements a privacy pool based on the Privacy Pools
                                                  Paper.
          polymerdao/plonky2-circom               A Plonky2 verifier implemented in Circom.
               zkemail/zk-regex                   A Circom library for regex matching in zero-knowledge proofs.
              0xPolygon/pil-stark                 Generates a STARK proof from a State Machine written in PIL Language.
          rarimo/passport-zk-circuits             Circom circuits for passport authentication.
             nocturne-xyz/protocol                Circom circuits and smart contracts comprising the Nocturne protocol.
            AztecProtocol/aztec-nr                The Noir implementation of the Aztec blockchain protocol.
              zkemail/zkemail.nr                  A privacy-focused email system using zero-knowledge proofs.
          colinnielsen/ecrecover-noir             A Noir implementation of the Ethereum ecrecover.
       carpalsgrabby/zk-arch-noir-gauge           A Noir example that implements a simple “architecture style gauge” for
                                                  Web3 systems
                zkemail/noir-jwt                  A Noir library for handling JSON Web Tokens (JWTs) in zero-knowledge
                                                  proofs.
            zac-williamson/mpclib                 A library for multi-party computation (MPC) in Noir.
               noir-lang/noir_rsa                 A Noir library for RSA encryption and decryption.
          distributed-lab/noir-plume              Implementation of the PLUME protocol in Noir.
           distributed-lab/op_rand                A method of emulation of OP_RAND opcode on Bitcoin.
  attested-frontiers/openbanking.nr-circuit       A toolkit for verifying Openbanking payments with the Noir language.
              jtriley2p/etherleaks                Ring Signature-like Protocol for Anonymous Ethereum Signatures.
            noir-lang/noir-bignum                 A Noir library for big number arithmetic.
            hashcloak/noir-mpc-ml                 A Noir library for secure multi-party computation (MPC) machine
                                                  learning.
          noir-lang/noir_string_search            A Noir library for string searching algorithms.
       taurushq-io/private-CMTAT-aztec            Private version of CMTAT security token in Noir.
           noir-lang/noir_json_parser             A Noir library for parsing JSON data.
            noir-lang/noir_bigcurve               A Noir library that evaluates operations over elliptic curves instantiated
                                                  with an arbitrary prime field.
        defi-wonderland/aztec-standards           Comprehensive collection of reusable, standardized contracts for the
                                                  Aztec Network.




, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     27


               Table 7. Coverage and Frequency of Algebraic Primitives Across Repositories.

                    Primitive / Category         Repo Count      Coverage Score        Total Freq.
                    Category: Arithmetic              36              0.9730              6587
                    Category: Relational              35              0.9459              2428
                     Category: Logical                26              0.7027               547
                    Category: Composite                6              0.1622                9
                           AND                        17              0.4595               322
                            OR                        13              0.3514               32
                           NOT                        18              0.4865               103
                     BITWISE_AND                      12              0.3243               34
                          EQUAL                       34              0.9189              1771
                      NOT_EQUAL                       18              0.4865               70
                       LESS_THAN                      26              0.7027               218
                 LESS_THAN_OR_EQUAL                   19              0.5135               147
                    GREATER_THAN                      13              0.3514               29
               GREATER_THAN_OR_EQUAL                  10              0.2703               40
                           ADD                        36              0.9730              1859
                       SUBTRACT                       32              0.8649               874
                        MULTIPLY                      35              0.9459              2678
                          DIVIDE                      21              0.5676               104
                        MODULO                        20              0.5405               77
                          POWER                       12              0.3243               60
                         NEGATE                       10              0.2703               67
                     CONDITIONAL                      23              0.6216               153
                     BITWISE_XOR                       3              0.0811                3
                           XOR                         4              0.1081                46
                      BITWISE_OR                       2              0.0541                7
                         INVERSE                       5              0.1351                18
                        PRODUCT                        2              0.0541                2
                           SUM                         5              0.1351                7
                     FLOOR_DIVIDE                     11              0.2973               45



lower coverage. However, these remain essential for completeness. Overall, this coverage study
validates our primitive selection as practically relevant for evaluating LLM capabilities in ZK
program generation.

11     Case Studies on Frequently Used Production ZK Coding Patterns
Our adapted HumanEval and LiveCodeBench serve as a foundational benchmark to evaluate the
core computation-to-verification shift for ZKP programming. To evaluate the robustness of ZK-
Coder across practical contexts and domain-specific API using, we extend our analysis with a suite
of case studies derived from 37 production-grade Zero-Knowledge Proof repositories. This section
details the selection criteria, the specific patterns evaluated, and an elaboration on the performance
gains observed.

11.1    Selection Methodology
We utilize the same set of 37 production repositories analyzed in § 10 as the basis for our case studies.
To identify representative ZKP coding patterns, we conduct a systematic review aimed at isolating

                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
28      Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


logic that is functionally recurrent across real-world applications. To ensure methodological rigor
and mitigate selection bias, we employ a reproducible processing pipeline:
• Pattern Extraction: The authors perform a manual audit of the source code to extract coding
  patterns. We define a “coding pattern” as a non-trivial logic block that coordinates multiple
  primitives to enforce a high-level architectural invariant. Such patterns typically utilize interme-
  diate “hidden” signals (witnesses), maintain instance-independence (reusability), and compose
  specific APIs with algebraic constraints to describe high-level generalizable verification logic.
  This collaborative audit resulted in an initial set of 269 identified patterns.
• Clustering and Filtering: We aggregate these patterns into clusters based on their functional
  roles (e.g., Merkle tree verification, state nullification). We exclude patterns that are either secific
  to a single protocol (e.g., Aztec-specific logic in Noir) or functionally trivial (e.g., simple API
  wrappers), or occur only once. This yields a final set of 10 high-frequency, widely applicable
  coding patterns, summarized in Table 8.

                   Table 8. Frequently Used ZKP Coding Patterns in Production Repositories.

                Name                  Frequency    Description
  Merkle Tree Proof / Verification        34       Verify membership of a leaf in a Merkle tree using a path and root hash.
         Nullifier Derivation             16       Derive deterministic nullifiers from secrets to prevent double-spending.
    PubKey / PriKey Consistency           10       Verify that a public key is correctly derived from its private key counterpart.
       Chunked Data Hashing                7       Hash large inputs by decomposing them into smaller fixed-size chunks.
     Domain Separated Hashing              6       Apply domain separation to hash inputs for different logical contexts.
  Commitment Membership Proof             5        Verify membership in a set using a commitment-based proof.
   Bit-mask Selective Disclosure           3       Selectively reveal specific fields using bitmask encoding.
        Bitfield Data-packing              2       Pack multiple values into a single field using bitfield representation.
 ECDH Shared Secret Computation           2        Derive shared secrets using Elliptic Curve Diffie-Hellman.
   Private Ledger Balance Update          2        Update private balances while maintaining ledger consistency.




11.2     Evaluation
11.2.1 Setup. To ensure the validity of our results and mitigate the risk of data leakage (memory
recall of production code), we reformulated the task descriptions to use abstract terminology
while maintaining the underlying algebraic relations. We provide API references alongwith task
descriptions for all baselines to ensure fairness. We follow the experimental setup described in
§ 5, using both Circom and Noir as target DSLs with the same four LLM models. Correctness is
evaluated through test cases that are prepared using the same methodology as in § 3.1.
11.2.2 Results and Analysis. Results for ZK-Coder on these case studies are summarized in Table 3
(main paper). We provide detailed analysis on ZK-Coder’s performance for each pattern below.

11.3     Case Studies
We provide case studies on all ten frequently used ZKP coding patterns. For each case study, we
include the problem description, generated ZKSL constraint sketch, and the final implementation
in Circom. Noir is omitted for brevity, but is available in the replication package.
11.3.1 Merkle Tree Proof / Verification. Verifying a Merkle path requires navigating a recursive
hash chain while correctly handling left/right sibling positioning based on a bit-index. It is widely
used to prove data inclusion in a set privately and efficiently.
  Specifically, ZK-Coder first translates the problem into a ZKSL constraint sketch that captures
the core verification logic: compute the Merkle root via the ComputeMerkleRoot API, then enforce

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     29


conditional equality between the computed and expected roots using an implication constraint
( enable = 1 ⇒ computed_root = root ). This sketch guides the Circom implementation: the
API call is realized through a ComputeMerkleRoot component, while the implication is encoded
algebraically as (computed_root[i] - root[i]) * enable === 0 , leveraging field arithmetic
to gate the equality constraint. Boolean checks ensure enable and directions are binary,
completing the high-level pattern.

    Merkle Tree Proof / Verification

    Given a Merkle root, a leaf node, and a Merkle proof (path and directions), verify whether
    the leaf belongs to the tree. However, this verification is conditional upon a public enable
    flag.
    The process involves:
    (1) Recomputing the Merkle root from the leaf and the provided siblings using the
         ComputeMerkleRoot API.
    (2) If enable is 1 (true), the recomputed root must exactly match the provided public root.
    (3) If enable is 0 (false), the comparison constraint is relaxed, and any recomputed root is
        accepted.
    API Syntax:
     ComputeMerkleRoot(leaf, siblings, directions) : Returns a 4-element array repre-
    senting the computed hash root.
    • leaf : The starting data (array of 4 numbers).
    • siblings : A 2D array [depth][4] of neighbor hashes.
    • directions : A bit array indicating left/right path choices.

    def verify(
        engine: VerifyingEngine, root, enable, leaf, siblings, directions
    ) -> VerifyingEngine:
        computed_root = ComputeMerkleRoot(engine, leaf, siblings, directions)
        for i in range(4):
          engine.add(Implies(enable == IntVal(1), computed_root[i] == root[i]))
        return engine

    template CircuitProgram() {
        signal input root[4];
        signal input enable;
        signal input leaf[4];
        signal input siblings[12];
        signal input directions[3];

         // Boolean constraints for enable and directions
         signal enableBool;
         enableBool <== enable * (enable - 1);
         enableBool === 0;



                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
30       Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel



           signal dirBool[3];
           for (var i = 0; i < 3; i++) {
               dirBool[i] <== directions[i] * (directions[i] - 1);
               dirBool[i] === 0;
           }

           // Compute Merkle root with depth = 3
           component cmr = ComputeMerkleRoot(3);
           for (var j = 0; j < 4; j++) {
               cmr.leaf[j] <== leaf[j];
           }
           for (var k = 0; k < 12; k++) {
               cmr.siblings[k] <== siblings[k];
           }
           for (var d = 0; d < 3; d++) {
               cmr.directions[d] <== directions[d];
           }

         // Conditional equality via gating: (cmr.root[j] - root[j]) * enable == 0
          signal diff[4];
          signal gated[4];
          for (var t = 0; t < 4; t++) {
              diff[t] <== cmr.root[t] - root[t];
              gated[t] <== diff[t] * enable;
              gated[t] === 0;
          }
     }

11.3.2 Nullifier Derivation. Nullifier derivation binds a private nullifier and secret to a public
commitment while producing a separate public nullifier hash used for deterministic replay (double-
spend) prevention without revealing the secret nullifier. ZK-Coder encodes this as a small ZKSL
constraint sketch: compute an intermediate temp with HashTwo(secret, nullifier) , derive
 commitment as HashTwo(temp, amount) , and produce nullifierHash via HashOne(nullifier) .
The sketch enforces equality constraints between the declared outputs and the corresponding hash
results, which map directly to the Circom HashTwo and HashOne components in the implementa-
tion below. ZK-Coder then retrieves hints and instructions for this implementation mapping from
the sketch to complete the final code, and the high-level pattern is thus realized.

     Nullifier Derivation
     Implement a cryptographic commitment and nullifier derivation scheme. The goal is to
     bind a secret value and an amount to a specific nullifier using a multi-stage hashing process,
     while simultaneously generating a public nullifier hash for replay prevention.
     The process involves:
     (1) Deriving an intermediate temp value by hashing a private secret and a private
         nullifier using the HashTwo API.


, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     31



    (2) Deriving the final public commitment by hashing the temp value with a public amount
        using the HashTwo API.
    (3) Deriving a public nullifierHash from the private nullifier using the HashOne
        API to allow for deterministic double-spend prevention without revealing the nullifier
        itself.
    API Syntax:
     HashOne(value) : Returns a single field hash of one input.
     HashTwo(value1, value2) : Returns a single field hash of two inputs.

    def verify(
        engine: VerifyingEngine, amount, nullifier,
        secret, commitment, nullifierHash
    ) -> VerifyingEngine:
        temp = HashTwo(engine, secret, nullifier)
        engine.add(commitment == HashTwo(engine, temp, amount))
        engine.add(nullifierHash == HashOne(engine, nullifier))
        return engine

    template CircuitProgram() {
        signal input amount;
        signal input nullifier;
        signal input secret;
        signal input commitment;
        signal input nullifierHash;

         // temp = HashTwo(secret, nullifier)
         component h_temp = HashTwo();
         h_temp.a <== secret;
         h_temp.b <== nullifier;
         signal temp;
         temp <== h_temp.out;

         // commitment == HashTwo(temp, amount)
         component h_commit = HashTwo();
         h_commit.a <== temp;
         h_commit.b <== amount;
         commitment === h_commit.out;

         // nullifierHash == HashOne(nullifier)
         component h_nullifier = HashOne();
         h_nullifier.v <== nullifier;
         nullifierHash === h_nullifier.out;
    }

11.3.3 PubKey / PriKey Consistency. Verifying public/private key consistency ensures a private
scalar actually corresponds to a given public point on the Baby Jubjub curve without exposing the

                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
32      Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel


scalar. ZK-Coder encodes this as a ZKSL sketch: decompose the private key into 253 little-endian
bits, iterate those bits and conditionally add the precomputed base points (where BASE_POINTS[i]
= 2𝑖 ∗ 𝐺) to an accumulator using the PointAdd API, and enforce that the final accumulator equals
the provided public key. The sketch maps directly to Circom building blocks (e.g., conditional
additions are realized arithmetically via bit * (sum - acc) as hinted by ZK-Coder’s retrieved
material.)

     PubKey / PriKey Consistency

     Verify that a private key corresponds to a provided public key on the Baby Jubjub elliptic
     curve (Twisted Edwards form). Instead of using a high-level multiplier, you must implement
     the scalar multiplication logic manually.
     The process involves:
     (1) Decomposing the private key into a 253-bit array (little-endian).
     (2) Iterating through the bits. For each bit 𝑖 that is 1, add the corresponding precomputed
         base point 𝑃 = 2𝑖 ∗ 𝐺 to an accumulator.
     (3) The accumulator should start at the curve’s neutral element (0, 1).
     (4) Use the provided PointAdd API to perform the additions. Note that in a ZK circuit,
         you must handle the conditional addition (adding the point only if the bit is 1) using
         arithmetic gates rather than branching.
     Precomputed Base Points:
     A list of 253 points BASE_POINTS[i] is provided, where BASE_POINTS[i] = 2𝑖 ∗ 𝐺 .
     API Syntax:
      PointAdd(P1, P2) : Returns the sum of two points (x, y) on the Baby Jubjub curve.

     def verify(
         engine: VerifyingEngine, senderPublicKey, privKey, BASE_POINTS
     ) -> VerifyingEngine:
         assert len(senderPublicKey) == 2
         assert len(BASE_POINTS) == 506
         accX = IntVal(0)
         accY = IntVal(1)
         for i in range(253):
             twoPow = IntVal(1 << i)
             bit = (privKey // twoPow) % IntVal(2)
             engine.add(Or(bit == IntVal(0), bit == IntVal(1)))
             Px = BASE_POINTS[2*i]
             Py = BASE_POINTS[2*i+1]
             sx, sy = PointAdd(engine, (accX, accY), (Px, Py))
             accX = accX + bit * (sx - accX)
             accY = accY + bit * (sy - accY)
         engine.add(accX == senderPublicKey[0])
         engine.add(accY == senderPublicKey[1])
         return engine

     template CircuitProgram() {


, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     33



         signal input senderPublicKey[2];
         signal input privKey;
         signal input BASE_POINTS[506];

         // Decompose privKey into 253 bits
         component nb = Num2Bits(253);
         nb.in <== privKey;

         // Accumulators
         signal accX[254];
         signal accY[254];
         accX[0] <== 0;
         accY[0] <== 1;

         // Constraints to ensure each bit is 0 or 1 using OR(bit==0, bit==1)
         component eq0[253];
         component eq1[253];
         component orbit[253];

         // Point addition components and conditional updates
         component pa[253];
         signal deltaX[253];
         signal deltaY[253];
         signal stepX[253];
         signal stepY[253];

         for (var i = 0; i < 253; i++) {
             // Ensure bit is 0 or 1
             eq0[i] = IsEqual();
             eq1[i] = IsEqual();
             orbit[i] = OR();
             eq0[i].in[0] <== nb.out[i];
             eq0[i].in[1] <== 0;
             eq1[i].in[0] <== nb.out[i];
             eq1[i].in[1] <== 1;
             orbit[i].a <== eq0[i].out;
             orbit[i].b <== eq1[i].out;
             orbit[i].out === 1;

               // Point addition: (accX[i], accY[i]) + (Px, Py)
               pa[i] = PointAdd();
               pa[i].x1 <== accX[i];
               pa[i].y1 <== accY[i];
               pa[i].x2 <== BASE_POINTS[2*i];
               pa[i].y2 <== BASE_POINTS[2*i+1];




                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
34       Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel



                  // Conditional update: acc = acc + bit * (s - acc)
                  deltaX[i] <== pa[i].x3 - accX[i];
                  stepX[i] <== nb.out[i] * deltaX[i];
                  accX[i+1] <== accX[i] + stepX[i];

                  deltaY[i] <== pa[i].y3 - accY[i];
                  stepY[i] <== nb.out[i] * deltaY[i];
                  accY[i+1] <== accY[i] + stepY[i];
           }

           senderPublicKey[0] === accX[253];
           senderPublicKey[1] === accY[253];
     }


11.3.4 Chunked Data Hashing. Chunked data hashing manages large bitstring payloads by par-
titioning data into field-compatible segments, a common pattern in identity and large-scale data
attestation. ZK-Coder encodes this logic via a ZKSL sketch that first mandates boolean integrity
checks for the raw dataBits , then specifies the packing of four 190-bit segments into field elements
 c0..c3 via the BitsToNum transformation. Finally, the sketch defines a global commitment con-
straint where the dataCommitment must equal the output of HashFive(c0, c1, c2, c3, secretIdentity)
By retrieving targeted library implementations for the Bits2Num and HashFive primitives, ZK-
Coder correctly wires the bit-loop indices and component inputs, ensuring the circuit accurately
realizes the multi-stage hashing pipeline while maintaining field-capacity safety.

     Chunked Data Hashing

     Implement a chunked hashing scheme for a large bitstring payload. The goal is to securely
     commit to a long data array (e.g., identity data) by splitting it into chunks that fit within
     the circuit’s field capacity.
     The process involves:
     (1) Taking a private bit array dataBits of size 760.
     (2) Splitting the bits into 4 chunks of 190 bits each.
     (3) Converting each 190-bit chunk into a single field element (little-endian).
     (4) Passing the 4 derived field elements and a private secretIdentity into a hash function
         to produce a final dataCommitment .
     (5) Enforcing that the computed hash matches the public dataCommitment .
     API Syntax:
      BitsToNum(bits) : Converts an array of bits to a single field element.
      HashFive(in1, in2, in3, in4, in5) : Computes a hash of five inputs.

     def verify(
         engine: VerifyingEngine, dataCommitment, dataBits, secretIdentity
     ) -> VerifyingEngine:
         assert len(dataBits) == 760
         for b in dataBits:


, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     35



             engine.add(Or(b == IntVal(0), b == IntVal(1)))
         c0 = BitsToNum(dataBits[0:190])
         c1 = BitsToNum(dataBits[190:380])
         c2 = BitsToNum(dataBits[380:570])
         c3 = BitsToNum(dataBits[570:760])
         h = HashFive(engine, [c0, c1, c2, c3, secretIdentity])
         engine.add(h == dataCommitment)
         return engine

    template CircuitProgram() {
        signal input dataCommitment;
        signal input dataBits[760];
        signal input secretIdentity;

         // Enforce boolean constraints for each bit: v*(v-1) == 0
         signal bitcheck[760];
         for (var i = 0; i < 760; i++) {
             bitcheck[i] <== dataBits[i] * (dataBits[i] - 1);
             bitcheck[i] === 0;
         }

         // Pack bits into 4 chunks of 190 bits each (little-endian)
         component b2n0 = Bits2Num(190);
         component b2n1 = Bits2Num(190);
         component b2n2 = Bits2Num(190);
         component b2n3 = Bits2Num(190);
         for (var i = 0; i < 190; i++) {
             b2n0.in[i] <== dataBits[i];
             b2n1.in[i] <== dataBits[190 + i];
             b2n2.in[i] <== dataBits[380 + i];
             b2n3.in[i] <== dataBits[570 + i];
         }
         signal c0;
         signal c1;
         signal c2;
         signal c3;
         c0 <== b2n0.out;
         c1 <== b2n1.out;
         c2 <== b2n2.out;
         c3 <== b2n3.out;

         // Compute HashFive over [c0, c1, c2, c3, secretIdentity]
         component hf = HashFive();
         hf.v[0] <== c0;
         hf.v[1] <== c1;
         hf.v[2] <== c2;


                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
36       Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel



           hf.v[3] <== c3;
           hf.v[4] <== secretIdentity;

           // Enforce commitment equality
           hf.out === dataCommitment;
     }

11.3.5 Domain Separated Hashing. Domain separated hashing is a security-critical pattern that
ensures cryptographic non-malleability by binding a hash result to a specific logical context. ZK-
Coder captures this through a ZKSL sketch that formalizes the iterative “absorb-and-permute”
sponge construction: it initializes the verification state with the domainSeparator and recursively
computes intermediate states 𝑠𝑖 by summing the previous state with the current preimage element
before applying the MiMC7Permute transformation. The sketch explicitly models the data-flow
dependencies, ensuring that each permutation is strictly chained. By retrieving the specific MiMC7
round logic and permutation component signatures from its repository of production templates,
ZK-Coder correctly implements the signal wiring and intermediate summations, ultimately enforc-
ing an equality constraint between the final permutation output and the public outputHash to
guarantee context-specific integrity.

     Domain Separated Hashing

     Implement a domain-separated hash using a MiMC-7 sponge construction. Domain separa-
     tion prevents the same preimage from producing the same hash across different contexts
     by initializing the hash state with a unique domainSeparator .
     The process involves:
     (1) Initializing the internal hash state with the public domainSeparator .
     (2) Absorbing a list of private preimage field elements into the state iteratively.
     (3) After each absorption, applying the MiMC-7 permutation rounds.
     (4) Constraining the final state to match the public outputHash .
     API Syntax:
      MiMC7Permute(state) : Applies the 10-round MiMC-7 permutation to the current field
     element.

     def verify(
         engine: VerifyingEngine, domainSeparator, outputHash, preimage
     ) -> VerifyingEngine:
         s0 = domainSeparator
         s1 = MiMC7Permute(engine, s0 + preimage[0])
         s2 = MiMC7Permute(engine, s1 + preimage[1])
         s3 = MiMC7Permute(engine, s2 + preimage[2])
         engine.add(s3 == outputHash)
         return engine

     template CircuitProgram() {
         signal input domainSeparator;


, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     37



         signal input outputHash;
         signal input preimage[3];

         signal sum0;
         signal sum1;
         signal sum2;

         component p0 = MiMC7Permute();
         component p1 = MiMC7Permute();
         component p2 = MiMC7Permute();

         sum0 <== domainSeparator + preimage[0];
         p0.in <== sum0;

         sum1 <== p0.out + preimage[1];
         p1.in <== sum1;

         sum2 <== p1.out + preimage[2];
         p2.in <== sum2;

         outputHash === p2.out;
    }

11.3.6 Commitment Membership Proof. The commitment membership proof is a multi-stage verifi-
cation pattern that combines cryptographic binding with set inclusion logic. ZK-Coder models this
as a composite ZKSL sketch that simultaneously enforces two distinct relations: (1) a commitment
integrity check, which re-derives the positionCommitment using a HashThree of the private
coordinates and nonce; and (2) a disjunctive membership check, which asserts that the coordinate
pair (𝑥, 𝑦) matches at least one entry in the public whitelist setX and setY . The sketch specifies
the use of parallel equality checks ( IsEqual ) and a logical aggregation tree ( AND for coordinate
pairs, followed by a multi-input OR chain). ZK-Coder leverages these structural hints to retrieve
the appropriate boolean logic gates and hashing primitives, correctly implementing the nested
loop logic and signal wiring required to prove that the committed position is authorized without
revealing the specific index or the nonce.

    Commitment Membership Proof

    Verify that a private coordinate pair (x, y) and a private nonce correspond to a public
     positionCommitment , and additionally prove that the coordinate pair exists within a
    public whitelist of coordinates.
    The process involves:
    (1) Recomputing a hash of (x, y, nonce) and enforcing that it matches the public
         positionCommitment .
    (2) Iterating through two public arrays, setX and setY , to check if there exists an index
         i such that setX[i] == x AND setY[i] == y .
    (3) Enforcing that the membership condition is met (at least one match found).


                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
38      Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel



     API Syntax:
     HashThree(val1, val2, val3) : Computes the hash of three inputs.

     def verify(
         engine: VerifyingEngine, positionCommitment, setX, setY, x, y, nonce
     ) -> VerifyingEngine:
         h = HashThree(engine, x, y, nonce)
         engine.add(positionCommitment == h)
         engine.add(
             Or(
                 And(setX[0] == x, setY[0] == y),
                 And(setX[1] == x, setY[1] == y),
                 And(setX[2] == x, setY[2] == y),
                 And(setX[3] == x, setY[3] == y),
                 And(setX[4] == x, setY[4] == y)
             )
         )
         return engine

     template CircuitProgram() {
         signal input positionCommitment;
         signal input setX[5];
         signal input setY[5];
         signal input x;
         signal input y;
         signal input nonce;

           component hash = HashThree();
           hash.v1 <== x;
           hash.v2 <== y;
           hash.v3 <== nonce;

           positionCommitment === hash.out;

           component eqX[5];
           component eqY[5];
           component andXY[5];
           for (var i = 0; i < 5; i++) {
               eqX[i] = IsEqual();
               eqX[i].in[0] <== setX[i];
               eqX[i].in[1] <== x;
               eqY[i] = IsEqual();
               eqY[i].in[0] <== setY[i];
               eqY[i].in[1] <== y;
               andXY[i] = AND();



, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     39



               andXY[i].a <== eqX[i].out;
               andXY[i].b <== eqY[i].out;
         }

         component or01 = OR();
         or01.a <== andXY[0].out;
         or01.b <== andXY[1].out;

         component or02 = OR();
         or02.a <== andXY[2].out;
         or02.b <== andXY[3].out;

         component or03 = OR();
         or03.a <== or01.out;
         or03.b <== or02.out;

         component or04 = OR();
         or04.a <== or03.out;
         or04.b <== andXY[4].out;
         or04.out === 1;
    }

11.3.7 Bit-mask Selective Disclosure. Bit-mask selective disclosure is a fundamental privacy pattern
used to prove the authenticity of data while revealing only user-authorized fields. ZK-Coder
models this capability through a ZKSL sketch that integrates three critical verification layers: (1)
boolean input validation, which enforces that the disclosureSelector bits are strictly binary
to prevent under-constrained signal manipulation; (2) data integrity binding, which re-computes
the dataCommitment from the privateData using a HashArray primitive; and (3) conditional
masking logic. By sketching these relations, ZK-Coder ensures that the generated circuit correctly
forces the revealedData to zero when the selector is inactive, while faithfully copying private
values when active. The system retrieves the necessary quadratic constraint templates for the
boolean checks, successfully wiring the multi-signal loop to realize a secure, selective attestation.

    Bit-mask Selective Disclosure
    Implement a selective disclosure circuit using bitmask selectors. The circuit must prove
    that the revealedData array matches a hidden privateData array at indices where the
     disclosureSelector bit is set to 1, and contains 0 otherwise.
    The process involves:
    (1) Constraining the disclosureSelector array to contain only binary values (0 or 1).
    (2) Validating the integrity of the privateData against a public dataCommitment using
        hash.
    (3) For each index 𝑖, enforcing the relationship:
         revealedData[i] == privateData[i] * disclosureSelector[i] .
    (4) Proving that if disclosureSelector[i] is 0, the corresponding revealedData[i]
        is forced to be 0.


                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
40       Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel



     API Syntax:
     HashArray(array) : Computes the hash of a field array.

     def verify(
         engine: VerifyingEngine,
         dataCommitment, disclosureSelector, revealedData, privateData
     ) -> VerifyingEngine:
         assert len(disclosureSelector) == 4
         assert len(revealedData) == 4
         assert len(privateData) == 4
         for i in range(4):
             engine.add(Or(
                 disclosureSelector[i] == IntVal(0),
                 disclosureSelector[i] == IntVal(1)
             ))
          engine.add(revealedData[i] == privateData[i] * disclosureSelector[i])
         engine.add(dataCommitment == HashArray(engine, privateData))
         return engine

     template CircuitProgram() {
         signal input dataCommitment;
         signal input disclosureSelector[4];
         signal input revealedData[4];
         signal input privateData[4];

           // Enforce disclosureSelector[i] \in {0,1}
           signal sel_minus_one[4];
           signal computedRevealed[4];
           for (var i = 0; i < 4; i++) {
               sel_minus_one[i] <== disclosureSelector[i] - 1;
               disclosureSelector[i] * sel_minus_one[i] === 0;
               // revealedData[i] == privateData[i] * disclosureSelector[i]
               computedRevealed[i] <== privateData[i] * disclosureSelector[i];
               computedRevealed[i] === revealedData[i];
           }

           // Compute and constrain dataCommitment == HashArray(privateData)
           component hasher = HashArray(4);
           for (var i = 0; i < 4; i++) {
               hasher.v[i] <== privateData[i];
           }
           hasher.out === dataCommitment;
     }


11.3.8 Bitfield Data-packing. Bitfield data-packing is a fundamental optimization pattern in ZK
programming used to reduce the number of public signals and constraints by aggregating multiple

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     41


small values into a single field element. ZK-Coder models this through a ZKSL sketch that pri-
oritizes algebraic soundness and range integrity. The sketch defines two distinct sub-proofs: (1)
a range-enforcement proof, which utilizes the WithinRange primitive to ensure that msg_type
and msg_metadata do not exceed the 64-bit capacity, preventing field-overflow vulnerabilities;
and (2) an arithmetic reconstruction proof, which specifies the scaling logic (𝑚𝑠𝑔_𝑡𝑦𝑝𝑒 · 264 ) +
𝑚𝑠𝑔_𝑚𝑒𝑡𝑎𝑑𝑎𝑡𝑎. By sketching these requirements, ZK-Coder correctly identifies the need for high-
precision comparison components ( GreaterEqThan and LessEqThan ) and constant-time scaling.
The system retrieves the exact templates and hints for range checks, ensuring that the final Cir-
com/Noir code accurately implements the signals into the target packedValue without silent
overflow bugs.

    Bitfield Data-packing

    Implement a data packing and unpacking scheme using arithmetic scaling. You must pack
    two 64-bit unsigned integers (a type and metadata ) into a single field element, and then
    prove that a provided field element correctly decomposes into those two specific values.
    The process involves:
    (1) Packing: The packedValue is calculated as (𝑚𝑠𝑔_𝑡𝑦𝑝𝑒 · 264 ) + 𝑚𝑠𝑔_𝑚𝑒𝑡𝑎𝑑𝑎𝑡𝑎.
    (2) Range Proof: Enforcing that both msg_type and msg_metadata are valid 64-bit inte-
         gers (0 ≤ 𝑥 < 264 ).
    (3) Unpacking Proof: Enforcing that the public packedValue exactly matches the result
         of the arithmetic packing.
    API Syntax:
     WithinRange(value, bit_length) : Asserts that value is within the range of 0 to
    2𝑏𝑖𝑡 _𝑙𝑒𝑛𝑔𝑡ℎ − 1.

    def verify(
        engine: VerifyingEngine, packedValue, msg_type, msg_metadata
    ) -> VerifyingEngine:
        engine.add(IntVal(0) <= msg_type)
        engine.add(WithinRange(engine, msg_type, 64))
        engine.add(IntVal(0) <= msg_metadata)
        engine.add(WithinRange(engine, msg_metadata, 64))
        engine.add(packedValue == msg_type * IntVal(2 ** 64) + msg_metadata)
        return engine

    template CircuitProgram() {
        signal input packedValue;
        signal input msg_type;
        signal input msg_metadata;

         // Enforce 0 <= msg_type
         component ge1 = GreaterEqThan(252);
         ge1.in[0] <== msg_type;
         ge1.in[1] <== 0;
         ge1.out === 1;


                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
42       Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel



           // Enforce msg_type <= 2^64
           component le1 = LessEqThan(252);
           le1.in[0] <== msg_type;
           le1.in[1] <== 18446744073709551616;
           le1.out === 1;

           // Enforce 0 <= msg_metadata
           component ge2 = GreaterEqThan(252);
           ge2.in[0] <== msg_metadata;
           ge2.in[1] <== 0;
           ge2.out === 1;

           // Enforce msg_metadata <= 2^64
           component le2 = LessEqThan(252);
           le2.in[0] <== msg_metadata;
           le2.in[1] <== 18446744073709551616;
           le2.out === 1;

           // Compute packedValue == msg_type * 2^64 + msg_metadata
           signal high;
           high <== msg_type * 18446744073709551616;
           signal recombined;
           recombined <== high + msg_metadata;
           recombined === packedValue;
     }

11.3.9 ECDH Shared Secret Computation. The ECDH (Elliptic Curve Diffie-Hellman) shared secret
computation is a sophisticated cryptographic pattern essential for establishing secure commu-
nication channels within ZK protocols. ZK-Coder handles this task by drafting a ZKSL sketch
that focuses on the algebraic decomposition and scalar operations required for the Baby Jubjub
curve. The sketch defines a two-step verification process: (1) Bit-decomposition and range vali-
dation, which utilizes the Num2Bits primitive to convert the senderPrivateKey into a 253-bit
array while implicitly enforcing that the scalar fits within the curve’s subgroup order; and (2)
Any-Base scalar multiplication, which models the point multiplication 𝑃𝑠ℎ𝑎𝑟𝑒𝑑 = 𝑑𝑠𝑒𝑛𝑑𝑒𝑟 · 𝑃𝑟𝑒𝑐𝑒𝑖𝑣𝑒𝑟 .
By retrieving specialized Elliptic Curve templates for ScalarMulAny from its curated repository,
ZK-Coder ensures the correct wiring of bit signals to the scalar multiplication component. This
approach guarantees that the resulting coordinates match the public sharedKey without exposing
the private scalar, correctly implementing the complex non-linear constraints of Twisted Edwards
curve arithmetic.

     ECDH Shared Secret Computation

     Compute an ECDH shared key on the Baby Jubjub curve (Twisted Edwards form). This
     involves performing a scalar multiplication of an arbitrary public point (receiverPublicKey)
     by a private scalar (senderPrivateKey).
     The process involves:


, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     43



    (1) Decomposing the private key into a 253-bit array.
    (2) Performing Any-Base scalar multiplication: Result =
        senderPrivateKey * receiverPublicKey .
    (3) The circuit must verify that the provided sharedKey coordinates match the computed
        point.
    Note: For this task, you are provided with PointAdd and ScalarMulAny APIs.

    def verify(
       engine: VerifyingEngine, receiverPublicKey, sharedKey, senderPrivateKey
    ) -> VerifyingEngine:
        engine.add(And(
            senderPrivateKey>=IntVal(0),
            senderPrivateKey<IntVal(2**253)
        ))
        bits=[]
        for i in range(253):
            bit=(senderPrivateKey // IntVal(2 ** i)) % IntVal(2)
            engine.add(Or(bit == IntVal(0), bit == IntVal(1)))
            bits.append(bit)
        res_x, res_y = ScalarMulAny(
            engine, (receiverPublicKey[0], receiverPublicKey[1]), bits
        )
        engine.add(res_x == sharedKey[0])
        engine.add(res_y == sharedKey[1])
        return engine

    template CircuitProgram() {
        signal input receiverPublicKey[2];
        signal input sharedKey[2];
        signal input senderPrivateKey;

         // Decompose senderPrivateKey into 253 bits and enforce range < 2^253
         component bits = Num2Bits(253);
         bits.in <== senderPrivateKey;

         // Scalar multiplication: res = senderPrivateKey * receiverPublicKey
         component scalarMul = ScalarMulAny(253);
         for (var i = 0; i < 253; i++) {
             scalarMul.scalarBits[i] <== bits.out[i];
         }
         scalarMul.point[0] <== receiverPublicKey[0];
         scalarMul.point[1] <== receiverPublicKey[1];

         // Ensure the result equals the sharedKey
         scalarMul.out[0] === sharedKey[0];



                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
44       Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel



           scalarMul.out[1] === sharedKey[1];
     }

11.3.10 Private Ledger Balance Update. The private ledger balance update is a complex state-
transition pattern that encapsulates the core logic of privacy-preserving asset transfers. ZK-Coder
models this through a ZKSL sketch that coordinates three primary cryptographic objectives: (1) State
Consistency, which re-derives the oldBalanceCommitment to prove the user’s starting balance
without revealing it; (2) Double-Spend Prevention, which generates a deterministic nullifierHash
bound to the specific secret and commitment; and (3) Arithmetic Integrity, which verifies that the
balance subtraction (𝑛𝑒𝑤 = 𝑜𝑙𝑑 − 𝑠𝑝𝑒𝑛𝑑) is sound.
   The ZK-Coder sketch explicitly mandates a 64-bit range proof using the WithinRange primitive,
which effectively enforces the invariant oldBalance >= spendAmount . By retrieving range-check
templates, ZK-Coder correctly wires the intermediate secretPlusOne signals and ensures that the
final newBalanceCommitment is algebraically tied to the updated state. This systematic approach
allows the system to realize the full lifecycle of a private transaction while maintaining strict
field-level security.

     Private Ledger Balance Update

     Implement a private balance subtraction circuit. The circuit proves that a user can spend
     a specific amount from a hidden balance, resulting in a new hidden balance and a public
     nullifier.
     The process involves:
     (1) Recomputing the “Old Commitment” by hashing the oldBalance , secret , and
           nonce .
     (2) Verifying the “Old Commitment” matches the public oldBalanceCommitment .
     (3) Computing a deterministic public nullifierHash by hashing the secret , the
           oldBalanceCommitment , and a constant padding of 0 . This ensures the nullifier is
          bound to the specific balance state without revealing the secret.
     (4) Calculating newBalance = oldBalance - spendAmount .
     (5) Enforcing a 64-bit range proof on newBalance to ensure the subtraction did not under-
          flow in the prime field (effectively proving oldBalance >= spendAmount ).
     (6) Computing a newBalanceCommitment for the remaining funds by hashing the
           newBalance , a derived secret ( secret + 1 ), and the original nonce .
     API Syntax:
      HashThree(a, b, c) : Computes a hash of three field elements.
      WithinRange(value, bit_length) : Asserts that value is within the range of 0 to
     2𝑏𝑖𝑡 _𝑙𝑒𝑛𝑔𝑡ℎ − 1.

     def verify(
         engine: VerifyingEngine,
         oldBalanceCommitment, newBalanceCommitment, nullifierHash,
         spendAmount, oldBalance, secret, nonce
     ) -> VerifyingEngine:
         engine.add(HashThree(


, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     45



             engine, oldBalance, secret, nonce
             ) == oldBalanceCommitment)
         engine.add(HashThree(
             engine, secret, oldBalanceCommitment, IntVal(0)
             ) == nullifierHash)
         newBalance = oldBalance - spendAmount
         engine.add(newBalance >= IntVal(0))
         engine.add(WithinRange(engine, newBalance, 64))
         engine.add(HashThree(
             engine, newBalance, secret + IntVal(1), nonce
             ) == newBalanceCommitment)
         return engine

    template CircuitProgram() {
        signal input oldBalanceCommitment;
        signal input newBalanceCommitment;
        signal input nullifierHash;
        signal input spendAmount;
        signal input oldBalance;
        signal input secret;
        signal input nonce;

         // 1) HashThree(oldBalance, secret, nonce) == oldBalanceCommitment
         component hash1 = HashThree();
         hash1.in[0] <== oldBalance;
         hash1.in[1] <== secret;
         hash1.in[2] <== nonce;
         hash1.out === oldBalanceCommitment;

         // 2) HashThree(secret, oldBalanceCommitment, 0) == nullifierHash
         component hash2 = HashThree();
         hash2.in[0] <== secret;
         hash2.in[1] <== oldBalanceCommitment;
         hash2.in[2] <== 0;
         hash2.out === nullifierHash;

         // 3) newBalance = oldBalance - spendAmount
         signal newBalance;
         newBalance <== oldBalance - spendAmount;

         // 4) Ensure newBalance >= 0 <=> spendAmount <= oldBalance
         component lte = LessEqThan(252);
         lte.in[0] <== spendAmount;
         lte.in[1] <== oldBalance;
         lte.out === 1;



                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
46         Zhantong Xue, Pingchuan Ma, Zhaoyu Wang, Yuguang Zhou, Xiaoqin Zhang, Shuai Wang, and Juergen Rahmel



             // 5) Ensure newBalance fits in 64 bits
             component rangeCheck = WithinRange(64);
             rangeCheck.in <== newBalance;

             // 6) HashThree(newBalance, secret+1, nonce) == newBalanceCommitment
             signal secretPlusOne;
             secretPlusOne <== secret + 1;
             component hash3 = HashThree();
             hash3.in[0] <== newBalance;
             hash3.in[1] <== secretPlusOne;
             hash3.in[2] <== nonce;
             hash3.out === newBalanceCommitment;
      }

12     Task Filtering in Benchmark Curation
As discussed in the main paper, our end-to-end code generation dataset is constructed by adapting
tasks from HumanEval [10] and LiveCodeBench [27]. These benchmarks were selected for two pri-
mary reasons: first, they are widely recognized as the gold standard for evaluating code generation,
offering a diverse set of tasks that represent fundamental programming logic; and second, their
well-defined computational problems allow us to isolate and assess the critical “computation-to-
verification” paradigm shift inherent in ZK programming.
   The complete list of these filtered tasks is presented in Table 9 and Table 10. For brevity, we provide
only the task names and core requirements here; readers interested in the full task descriptions and
implementation details are encouraged to refer to our accompanying artifact.
   Furthermore, for a detailed analysis of our algebraic primitive benchmark, please see § 10. For
insights and case studies conducted on production-grade public repositories, refer to § 11.
                                Table 9. Filtered Task IDs from Adapting HumanEval.

                               Filtered Task IDs from HumanEval (Total 68 Tasks)
      3      5     8      9       13    24     31      33     35     36    37    39    40    41   42    43    46
      49     52    53     55      57     59     60      62     63    65    69    70    72    73   75     76    77
      83     85    88     90      94     97    102     106    108   109   110   114   115   116   121   122   123
     126    127   128    131     135    138    139     142    145   146   147   150   151   152   155   157   159


                             Table 10. Filtered Task IDs from Adapting LiveCodeBench.

                            Filtered Task IDs from LiveCodeBench (Total 34 Tasks)
      43     44    62     66      78     94    119     124    129   153   156   172   203   225   232   240   243
     250    261   265    280     290    297    305     322    323   336   346   353   367   373   375   384   389


13     Prompt Availability Statement
All prompts used in our experiments are available in the replication package. We provide exact
prompt templates with clearly marked placeholders that are filled with specific values during
ZK-Coder’s execution.

, Vol. 1, No. 1, Article . Publication date: February 2026.
From Evaluation to Enhancement: Large Language Models for Zero-Knowledge Proof Code Generation                     47


   To ensure methodological fairness, we employed standard zero-shot and few-shot prompting
techniques without extensive prompt engineering or fine-tuning. Additionally, we verified that no
test cases or ground-truth solutions were included in the prompts, preventing information leakage
that could artificially inflate success rates.
   While we omit raw prompts from this paper to maintain brevity, they are fully accessible in the
replication package for transparency and reproducibility.
Received 30 January 2026




                                                           , Vol. 1, No. 1, Article . Publication date: February 2026.
