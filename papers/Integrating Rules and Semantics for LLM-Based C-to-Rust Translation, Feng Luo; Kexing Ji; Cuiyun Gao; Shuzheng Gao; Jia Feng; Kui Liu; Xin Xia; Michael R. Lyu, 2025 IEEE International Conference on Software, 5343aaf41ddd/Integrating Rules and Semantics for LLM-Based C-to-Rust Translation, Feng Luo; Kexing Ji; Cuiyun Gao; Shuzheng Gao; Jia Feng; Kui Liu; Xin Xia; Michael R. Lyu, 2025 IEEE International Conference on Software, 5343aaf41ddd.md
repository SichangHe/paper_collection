                                            Integrating Rules and Semantics for LLM-Based
                                                         C-to-Rust Translation
                                             Feng Luo1 , Kexing Ji1 , Cuiyun Gao1∗ , Shuzheng Gao2 , Jia Feng1 , Kui Liu3 , Xin Xia4 , Michael R. Lyu2
                                                  1 School of Computer Science and Technology, Harbin Institute of Technology, Shenzhen, China
                                                2 Department of Computer Science and Engineering, The Chinese University of Hong Kong, China
                                                  3 Huawei Software Engineering Application Technology Lab, China 4 Zhejiang University, China

                                              hitszluofeng@foxmail.com, kexingji@stu.hit.edu.cn, gaocuiyun@hit.edu.cn, szgao23@cse.cuhk.edu.hk,
                                                        jfeng@std.uestc.edu.cn, kui.liu@huawei.com, xin.xia@acm.org, lyu@cse.cuhk.edu.hk
arXiv:2508.06926v1 [cs.SE] 9 Aug 2025




                                           Abstract—Automated translation of legacy C code into Rust         manual C-to-Rust migration presents significant challenges, in-
                                        aims to ensure memory safety while reducing the burden of            cluding Rust’s steep learning curve and the critical requirement
                                        manual migration. Early approaches in C-to-Rust translation          to preserve the original program’s semantics. Consequently,
                                        rely on static rule-based methods, but they suffer from limited
                                        coverage due to dependence on predefined rule patterns. Recent       the task of C-to-Rust translation, which aims at automatically
                                        works regard the task as a sequence-to-sequence problem by           generating semantically equivalent Rust code, has emerged as
                                        leveraging large language models (LLMs). Although these LLM-         a promising direction among academia and industry.
                                        based methods are capable of reducing unsafe code blocks, the           Early work on C-to-Rust translation has mainly centered
                                        translated code often exhibits issues in following Rust rules and    around rule-based approaches that rely on predefined patterns
                                        maintaining semantic consistency. On one hand, existing methods
                                        adopt a direct prompting strategy to translate the C code, which     to guide the translation process [7]–[9]. A representative
                                        struggles to accommodate the syntactic rules between C and Rust.     example is C2Rust [10], a static tool built on Clang [11]
                                        On the other hand, this strategy makes it difficult for LLMs to      and LLVM [12] that systematically converts C code into
                                        accurately capture the semantics of complex code.                    Rust. Subsequent methods extend C2Rust to better support
                                           To address these challenges, we propose IRENE, an LLM-            specific translation targets, such as parallel APIs [13] and
                                        based framework that Integrates RulEs aNd sEmantics to en-
                                        hance translation. IRENE consists of three modules: 1) a rule-       pointer constructs [14]–[16]. These rule-based methods offer
                                        augmented retrieval module that selects relevant translation ex-     the advantage of high efficiency and low computational cost.
                                        amples based on rules generated from a static analyzer developed     However, they heavily rely on predefined rules created by
                                        by us, thereby improving the handling of Rust rules; 2) a            experts, which are labor-intensive and suffer from the low
                                        structured summarization module that produces a structured           coverage problem [15], [17].
                                        summary for guiding LLMs to enhance the semantic under-
                                        standing of C code; 3) an error-driven translation module that          Recently, LLM-based methods have emerged as a promising
                                        leverages compiler diagnostics to iteratively refine translations.   paradigm for code translation [18]–[20]. These approaches
                                        We evaluate IRENE on two datasets (xCodeEval—a public                learn translation patterns from large-scale code corpora and
                                        dataset, HW-Bench—an industrial dataset provided by Huawei)          aiming at generating safe Rust code compared to rule-based
                                        and eight LLMs, focusing on translation accuracy and safety.         approaches [21], [22]. However, these methods solely rely on
                                        In the xCodeEval, IRENE consistently outperforms the strongest
                                        baseline method in all LLMs, achieving average improvements          the inherent capability of LLMs without explicit guidance,
                                        of 8.06% and 12.74% in the computational accuracy (CA) and           which often results in code that violates Rust’s rules. For
                                        compilation success rate (CSR), respectively. It also enhances the   example, as illustrated in Fig.1, the Rust code translated by
                                        safety of translated code, reducing the Unsafe Rate (UR) to 1.70%    instruction prompting (i.e., directly asking the model to trans-
                                        on average. In the HW-Bench, when compared to the strongest          late with a general instruction) fails to handle I/O operations
                                        baseline, IRENE improves CSR and reduces UR by an average
                                        of 0.33% and 26.00%, respectively.                                   and array types properly, violating Rust’s safety requirements.
                                                                                                             Some recent studies [23], [24] have attempted to integrate
                                                              I. I NTRODUCTION                               static rule-based analysis to improve LLMs’ performance.
                                           Legacy C projects remain vulnerable to memory safety              However, these approaches frequently employ static tools
                                        issues due to the language’s lack of built-in safety mecha-          like C2Rust rather than establishing verified safe translation
                                        nisms [1]–[3]. A study by Mozilla reveals that 94.00% high-          paradigms, which compromises the quality of translated code
                                        severity and critical security bugs in Firefox are related to        and yields insufficient safety guarantees. Moreover, LLMs
                                        memory safety, with C/C++ being the primary culprits [4].            often struggle to comprehensively understand the semantics of
                                        Rust [5] offers memory safety without garbage collection,            complex source programs, particularly when explicit descrip-
                                        combining the low-level control of C/C++ with the ease of use        tions of I/O types are absent. According to Yang et al. [25],
                                        of modern languages. For example, Nvidia has reimplemented           more than 50.00% of translation failures by large language
                                        the GPU driver Nova in Rust, and Google has adopted Rust             models stem from insufficient understanding of the source
                                        for new Android operating system components [6]. However,            code and unclear specification of I/O types. These limitations
                            Rule category: I/O                                                Rule category: Array
             Original C code            : C code snippet requiring             Original C code            : C code snippet requiring
             #include<stdio.h>          specific translation rules             #include <stdio.h>         specific translation rules
             #define For(i) for(i=1;i<=9;i++)                                  int prime[1005000];
             int main(){                                                       void init() {
                 int x,y,z,t,c1,c2,r1,r2,d1,d2;                                    if(j == cnt || i % primeList[j] != 0) {
                 scanf("%d%d%d%d%d%d",&r1,&r2,&c1,&c2,&d1,&d2);                        prime[i] = 1;
                 ...}                                                              ...}

             Rust Code Translated by Instruction Prompting                     Rust Code Translated by Instruction Prompting
                    Result:                                                           Result:
                    thread 'main' panicked at test.rs:                                error[E0277]: the type `[i32]` cannot be indexed
                    9:26:called `Option::unwrap()` on a `None` value                  by `i32` --> test.rs:21:19

              io::stdin().read_line(&mut input).unwrap();                         let mut j = 0;
              let mut iter = input.split_whitespace().map(|s|                     if j == cnt || i % prime_list[j] != 0 {
              s.parse::<i32>().unwrap());                                             prime[i] = 1;


             Rust Code Translated by IRENE                  Result:            Rust Code Translated by IRENE                  Result:
                                                            PASSED                                                            PASSED
                                                                                  let mut j = 0;
              io::stdin().read_to_string(&mut input).unwrap();                    if j == cnt || i % prime_list[j] != 0 {
              let mut parts = input.split_whitespace();                               prime[i as usize] = 1;

                               (a) Rule category: I/O                                        (b) Rule category: Array
Fig. 1: Two cases show that the Rust code translated by instruction prompting fails to handle I/O operations (a) and array types (b) properly
based on Qwen2.5-Coder-32B.

greatly hinders the practical deployment of LLMs in the task.           tational accuracy (CA) and 12.74% in compilation success rate
   To address these challenges, we propose IRENE, a rule-               (CSR). Moreover, IRENE contributes to safer translations by
augmented retrieval and structured summarization LLM-based              notably reducing the Unsafe Rate (UR) and Unsafe Loc Rate
framework for C-to-Rust translation. IRENE synergistically              (ULR) to 1.70% and 0.26% on average, outperforming both
integrates rules and semantics, consisting of three key compo-          static analysis tools and prompting methods. Our evaluation of
nents:                                                                  IRENE on the Huawei-developed industrial dataset HW-Bench
   • Rule-Augmented Retrieval Module: This module re-                   exhibits consistent performance trends. When compared to the
     trieves relevant translation pairs based on a set of static        strongest baseline, IRENE raises CSR by 0.33%, and reduces
     rules that reflect Rust-specific memory and type se-               UR and ULR by 26.00% and 10.49% on average, respectively.
     mantics, such as input handling conventions, and array                In summary, our main contributions are as follows:
     indexing patterns. These pairs provide targeted context
                                                                           • We identify two essential challenges in C-to-Rust trans-
     that helps the model adhere to Rust’s strict rules.
                                                                             lation: the need for safety-aware rule adaptation and
   • Structured Summarization Module: This module
                                                                             accurate semantic understanding
     prompts the model to first generate a summary of the C
                                                                           • We propose IRENE, a novel LLM-based framework
     code that describes its I/O types and overall functionality,
                                                                             for C-to-Rust translation that integrates rule-augmented
     aiming to produce more semantically faithful translations.
                                                                             retrieval, structured summarization, and iterative refine-
   • Error-Driven Translation Module: After the initial
                                                                             ment. Guided by safety-aware translation rules and se-
     translation, this module parses compiler diagnostic mes-
                                                                             mantic understanding, IRENE systematically improves
     sages and uses them to guide iterative refinement of
                                                                             translation quality and ensures compliance with Rust’s
     the Rust code. This feedback cycle leverages the LLM’s
                                                                             strict safety guarantees.
     ability to learn from error messages and improve its
                                                                           • Extensive experiments are conducted on multiple LLMs
     output.
                                                                             and datasets, showing that IRENE notably outperforms
   To validate the performance of IRENE, we conduct exper-                   all baselines in both translation accuracy and safety.
iments on a public and an industrial dataset (xCodeEval [26]
and HW-Bench). We compare IRENE with five representa-
tive prompt baselines on eight popular open-source LLMs.                                         II. M ETHODOLOGY
Extensive experimental results demonstrate the effectiveness
of IRENE. IRENE delivers consistent and substantial improve-               In this section, we propose IRENE, an LLM-based frame-
ments across both datasets. On the xCodeEval benchmark, we              work that integrates rules and semantics to enhance translation.
observe that IRENE outperforms the strongest baseline across            We first present the overview of IRENE and then elaborate on
all LLMs. It yields average improvements of 8.06% in compu-             its module details in the following subsections.
                                         Enhanced Translation Prompt Construction                                                           ③ Error-Driven Translation Module
                                            ① Rule-Augmented Retrieval Module                                                  Prompt                         Iteration
                                                                                 Demonstration Corpus                                                         Translate

                                                                                                    C-Rust Pair                Rule Hint
                                                           Rule Category: I/O
                                  I/O                                                             Rule category: I/O                                 LLM                  Rust code
                                                           Rule Description
                                                                                                  Score: 112.3                                                                   Compile
                            AST           Rule Library         Rule Hint
                                                                                          BM25
                                        Static Rule Analyzer                        Intra-Category Retrieval                  C-Rust Pair                      Failed

                                                                                                                                                     Error              Compilation
   C Code                                   ② Structured Summarization Module                                                                       Prompt                Result
                                                                                                                               C Code

                                Summarize    Params: 3 integers `n`, `a`, `b`                                                                              Error Prompt
                                             Return: An integer                                                                                   fn main() {          error[E0308]:
                                                                                                                                                      let mut z = 0;   mismatched
                      LLM                          Params & Return                Functionality           Summary             Summary                 for l in 1..n    Types --> test.rs:
                                                                                                                                                  ...                  67:51 ...




                                                                                Fig. 2: Overview of IRENE.

                                        Static Rule Analyzer & Alignment                               Algorithm 1: Static Rule Analyzer—DetectPointer
                                                                                                        Input: C source code CODEc
           Sample                                  Translate                                            Output: Set of Rhint triplets
           Filter           …                      Compile            …                               1 begin
Training                                                                   Demonstration
                                             LLM                                                            Parse CODEc into AST tree;
  Set                   C Code                                               Corpus                   2
                                                          Successed Compiled                          3     Function Walk(node):
                                                              Rust Code
                                                                                                      4         if node is pointer related then
                    Fig. 3: Demonstration corpus construction.                                        5              decl node ← Find the nearest enclosing
                                                                                                                      declaration;
A. Overview                                                                                           6              rule category ← ”Pointers”;
                                                                                                      7              code snippet ← extract corresponding code
   As illustrated in Fig. 2, IRENE consists of three main com-                                                        from CODEc ;
ponents organized into a pipeline. First, the rule-augmented                                          8              suggested Rust ←
                                                                                                                      I NFER P OINTERT YPE(code snippet);
retrieval module selects relevant translation examples Edemo
                                                                                                      9              rule description ←
based on syntactic rules Rhint extracted from our static                                                              code snippet+suggested Rust;
analyzer, aiming at reinforcing Rust’s safety rules. Next, the                                       10              Append {rule category, rule description} to
structured summarization module generates a structured                                                                Rhint ;
semantic summary Sc of the C code to improve the LLMs’                                               11                foreach child in node.children do
understanding and translation quality. These outputs (Edemo ,                                        12                    WALK(child);
Rhint , Sc ), along with the original C code (CODEc ) are
                                                                                                     13       WALK(AST.root);
composed into a prompt that guides the LLM to produce                                                14       return Rhint ;
initial Rust translations. Finally, the error-driven translation
module utilizes compiler diagnostics to iteratively refine the
output, correcting translation errors and enhancing safety.
                                                                                                     as guidance for the transformation process. Then, we design a
B. Rule-Augmented Retrieval Module                                                                   corresponding rule detection algorithm. The detection method
   This module is designed to help LLMs adapt to Rust’s strict                                       for pointer-related rules is illustrated in Algorithm 1, and
safety rules. First, we develop a static rule analyzer tailored to                                   similar strategies are applied to other rule categories. The
Rust’s memory and type safety requirements, which extracts                                           detection algorithm leverages the abstract syntax tree (AST)
necessary translation rules from the input CODEc . Then,                                             and outputs the rule hint Rhint , each represented as a triplet:
based on the identified rules, we retrieve the most relevant                                                     Rhint = <rule category, rule description>                                  (1)
translation examples from a curated demonstration repository.
These examples help the model understand how abstract rules                                          where the rule category indicates the type of transformation
are concretely applied during translation. In this way, the rules                                    rule detected, the code snippet refers to the minimal C
serve as a high-level guideline, while the examples provide                                          fragment that requires the application of the rule, and the
practical demonstrations, enabling the model to learn rule-to-                                       suggested Rust is the Rust code recommended by the rule.
code mappings more effectively.                                                                      Since Rhint is concise, it serves as an initial hint and requires
   1) Static Rule Analyzer: Building upon previous stud-                                             further augmentation via few-shot retrieval in the next step.
ies [15], [27], we summarize and extend a translation rule                                              2) Intra-Category Retrieval: This step aims to provide
library to enhance automation and consistency. A representa-                                         further augmentation for the rule-based translation process.
tive subset of the rule library is presented in Table I, serving                                     While the detection stage yields a suggested Rust type as
TABLE I: This table presents the taxonomy of rule categories designed in our Static Rule Analyzer. We present one representative rule
for each category. The complete rules can be found in our GitHub repository [28]. Each rule description summarizes the recommended
translation strategy, while the example column illustrates the actual translation of a representative C code snippet to Rust.

                                                                                                                  Examples
Category                         Description
                                                                                    C Code Snippets                                 Rust Code Snippets
                                                                                                                      struct Node { /* fields */ };
Pointers   Use Box<T>for malloc-allocated structs.                    struct Node* n = malloc(sizeof(struct Node));
                                                                                                                      let n = Box::new(Node::default());
                                                                                                                      let mut input = String::new();
                                                                      int a; float b;
  I/O      Replace scanf with read to string() + split whitespace()                                                   io::stdin().read to string(&mut input).unwrap();
                                                                      scanf(”%d %f”, &a, &b);
                                                                                                                      let mut parts = input.split whitespace();
                                                                      int sum = 0;                                    let mut sum: i64 = 0;
Mixtype    Cast mixed-width integers to a common type like i64
                                                                      sum = sum + (long long) dp[i] * dq[idx] ;       sum = sum + (dp[i] as i64 * dq[idx] as i64);
           Cast array indices to usize in Rust and                    int dp[100][2];                                 let dp = [[0; 2]; 100];
 Array
           use [[T; M]; N] for fixed-size multidimensional arrays.    res = res + dp[i + l][(l - 1) & 1];             res += dp[(i + l) as usize][((l - 1) & 1) as usize];



part of Rhint this suggestion is often partial or abstract.                            Based on the outputs of the previous modules, we construct
To bridge this gap, we retrieve concrete, structurally similar                       an enhanced translation prompt that integrates multiple sig-
translation examples from the demonstration corpus, offering                         nals:
richer contextual information to guide the model’s translation.                               prompt = <Rhint , Edemo , CODEc , Sc >          (4)
   We first construct a demonstration corpus to support
retrieval-based translation. As shown in Fig. 3, the construction                    This unified prompt provides the model with rule-level intent,
process involves random sampling and a two-step filtering                            retrieval-based demonstrations, and a high-level summary of
pipeline. Specifically, we randomly sample 30,000 instances                          the input code. Together, these elements guide the LLM
from the xCodeEval [26] training set. To prevent data leakage,                       towards producing more accurate, idiomatic, and semantically
we apply an initial filter. We then use the Qwen2.5-Coder-32B                        aligned Rust code.
model to generate the corresponding Rust code and apply a                            D. Error-Driven Translation Module
second filter by compiling the generated Rust code to ensure
                                                                                        This module is designed to exploit the LLM’s capacity
successful compilation. After filtering, we aligned the C and
                                                                                     for self-correction, using feedback from the Rust compiler to
Rust code to obtain 22,892 translation pairs in the final corpus.
                                                                                     iteratively refine the generated Rust code. After the initial Rust
We further annotate each sample in the corpus with rule
                                                                                     translation is generated, we first compile it using the rustc
categories using our Static Rule Analyzer. For retrieval, we
                                                                                     compiler. If any compilation errors are encountered, the error
adopt BM25 [29], a classic sparse retrieval algorithm from
                                                                                     messages are extracted and fed back into the model along with
the information retrieval domain, known for its effectiveness
                                                                                     the erroneous Rust output. The LLM is then prompted to revise
in capturing syntactic similarity between code snippets. Since
                                                                                     the translation, explicitly addressing the compiler diagnostics.
our approach emphasizes rule-level similarity, BM25 provides
                                                                                     This targeted approach enables the model to focus on specific
an effective mechanism for identifying structurally similar
                                                                                     issues, such as type mismatches, borrow checker violations,
examples.
                                                                                     or missing imports, without regenerating the entire code.
   To support translation via demonstration, we retrieve exam-
                                                                                        This module acts as a feedback cycle between the compiler
ples Edemo from the corpus that match the rule category of
                                                                                     and the LLM. By incorporating concrete error diagnostics, it
the input CODEc . Each retrieved example is denoted as
                                                                                     enhances the accuracy and safety of the final translation with
           Edemo = <c code, translated rust code>                            (2)     minimal human intervention.
C. Structured Summarization Module                                                                          III. E XPERIMENTAL S ETUP
   We introduce a structured summarization module that                               A. Research Questions
prompts the model to first produce a structured summary of
                                                                                       To evaluate IRENE’s performance in C-to-Rust translation,
the C code, thus ensuring that the subsequent Rust translation
                                                                                     we explore the following research questions:
remains semantically faithful. The key motivation is to extract
semantically relevant structural and type information from the                        RQ1: How does IRENE perform in terms of effectiveness
CODEc , in a form that is concise, interpretable, and beneficial                             and safety in C-to-Rust translation?
for downstream rule-based translation. This module aims to                            RQ2: What is the impact of each component of IRENE on
transform low-level C code into a higher-level description that                              the overall translation performance?
emphasizes semantic roles. The output acts as an intermediate                         RQ3: How does IRENE perform in industrial scenarios?
representation for guiding example retrieval and supporting                          B. Datasets
rule-aware translation. We denote this summarization process
                                                                                       Few-Shot Retrieval Corpus. We build a retrieval corpus
as a triplet:
                                                                                     composed of 22892 C-Rust translation pairs. Each example
            Sc = <Input, Output, F unctionality>                             (3)     includes both the original C code and the corresponding
Rust implementation. The corpus is used to provide few-shot      E. Performance Metrics
demonstrations for LLMs inference.                                 To evaluate the translation accuracy, we use the following
   Evaluation Set. We evaluate IRENE on two datasets:            two widely used performance metrics [25] in our evaluation:
xCodeEval and HW-Bench. For xCodeEval, we select 515               Computational Accuracy (CA) evaluates whether the can-
samples from the evaluation set, where each C code sample        didate translation generates the same outputs as the reference
passes all test cases and has a corresponding Rust implementa-   when given the same inputs. It can be formally defined as:
tion. For the HW-Bench, we randomly sample 100 C functions                              PN
from proprietary projects provided by Huawei, covering a                                      ca(yk , ŷk )
                                                                                CA = k=1                                    (5)
diverse set of industry scenarios.                                                      (      N
                                                                                          1, if Execk (yk ) = Execk (ŷk )
C. Baseline Methods                                                     ca(yk , ŷk ) =                                     (6)
                                                                                          0, otherwise
   In C-to-Rust translation experiments, we compare IRENE
with baselines as detailed below. Instruction provides the C     where N is the total number of evaluated code samples. yk and
code along with the prompt ‘Translate the following C code       ŷk represent the ground truth and the generated translation for
to Rust’ without any additional demonstration. In-context        the k-th sample, respectively. Ex∈Ck (·) denotes the execution
Learning (ICL) [30] includes several translation examples        result of a program on the k-th test case. The indicator function
in the prompt to help the model generate the target Rust         ca(yk , ŷk ) equals 1 if both outputs match, and 0 otherwise.
code. Retrieval-augment generation (RAG) [31] retrieves             Compilation Success Rate (CSR) measures the percent-
examples from the corpus similar to the target translation c     age of translated programs that successfully compile without
code and includes them in the input prompt. Chain-of-though      errors.
(CoT) [32] prompts the LLM to explain the translation steps         To evaluate the translation safety, following prior work [24],
before generating the Rust code, with demonstration examples     we use the metrics below:
identical to those in ICL. Vert [21] uses an LLM with few-shot      Unsafe Rate (UR) refers to the proportion of unsafe
examples and a two-stage refinement process. It first applies    samples in the dataset.
compiler-suggested fixes to the source code, then feeds the         Unsafe Loc Rate (ULR) denotes the ratio of unsafe lines
updated code and diagnostics back into the LLM for further       of code within each individual sample.
correction. C2Rust [10] is a widely used static rule tool that
                                                                                 IV. E XPERIMENTAL R ESULT
translates C code into Rust by using predefined rules.
                                                                 A. RQ1: Effectiveness of IRENE
D. Implementation Details                                           To investigate the effectiveness of IRENE in C-to-Rust
   LLM selection and setup. We evaluate IRENE on xCodeE-         translation, we compare IRENE with five representative
val with eight open-source LLMs, DeepSeek-Coder [33],            prompt baselines on eight popular open-source LLMs. Table II
Qwen2.5-Coder-Instruct [34], and Codellama [35], in response     presents the experimental results of IRENE along with base-
to the first two RQs. For RQ3, due to resource and time          line methods. For the safety performance, we compare IRENE
constraints, we limit our evaluation on HW-bench to the          with two static tools. Fig. 5 shows the safety performance.
Qwen2.5 series models only. We download these models from           Comparison of the translation accuracy metrics. As
HuggingFace [36] and utilize PyTorch [37] for deploying them     shown in Table II, IRENE consistently outperforms all base-
locally and performing inference.                                line methods across different LLMs. For example, compared
   The implementation of baselines and IRENE. For ICL,           to the strongest baseline method RAG, IRENE achieves an av-
we follow the prior work [38] and randomly sample four exam-     erage improvement of 8.06% and 12.74% on the CA and CSR
ples from the corpus. For RAG, we retrieve the most relevant     metrics, respectively. These results demonstrate that IRENE is
example using the BM25 algorithm. For Vert, we directly use      more effective in generating correct and compilable Rust code.
the replication packages released by the authors and adapt       Moreover, when analyzing the improvements across different
them to our tasks. For C2Rust, we use the C2Rust 0.20.0          LLMs, we observe that IRENE exhibits strong generalizability
version. For IRENE, we select the example with the highest       across models with varying parameter sizes. In particular, the
similarity and apply one iteration of refinement. Following      gains are more substantial for larger models. For instance,
prior work [39], we set a BM25 threshold of 100 based on         IRENE improves CA by 2.48% and 6.53% on average for
top-1 score distribution, covering 52.04% of the queries to      Deepseek-Coder-1.3B and Qwen2.5-Coder-1.5B, respectively,
ensure high-quality examples.                                    and achieves larger gains of 16.08% and 15.73% for Deepseek-
   Hyperparameter and environment settings. As for the           Coder-6.7B and Qwen2.5-Coder-7B. This discrepancy can be
hyperparameters of generation, we configure all LLMs with        explained by the limited instruction-following capability of
greedy decoding (temperature = 0, top-p = 1) to produce de-      smaller models, which often struggle to fully comprehend the
terministic outputs. We execute Python programs with Python      rule hints and semantic guidance provided by IRENE.
3.8.20 and compile all Rust programs with Rust 1.81.0.              To quantify the accuracy of each translation method, we
All experiments are conducted on an Ubuntu-20.04 server          adopt an evaluation strategy commonly used in other works[],
equipped with four NVIDIA A100 GPUs.                             measuring the overlap of the correctly translated code between
TABLE II: Comparison between IRENE and baselines on computational accuracy (CA) and compilation success rate (CSR). Under each
metric, the best performance is highlighted in bold.

                                        Deepseek-Coder                                                                            Qwen2.5-Coder                                                                                                                                         Codellama
  Approach                            1.3B                      6.7B                             1.5B                          7B                                              14B                                             32B                                        7B                                     34B
                               CA         CSR              CA       CSR                 CA           CSR                CA            CSR                           CA                 CSR                    CA                      CSR                        CA                 CSR                        CA    CSR
Instruction          4.85      20.78 19.03                         43.69                6.99          15.15            38.06        67.57                           45.44              74.17                 59.03                    87.18                 2.91                    7.57                     2.14              7.57
ICL                  6.21      64.08 27.96                         58.83                9.51          29.32            34.95        63.50                           48.35              75.53                 57.86                    82.33                 13.40                   41.75                    15.92            39.81
RAG                  6.41      70.68 30.49                         63.88                9.32          41.36            34.56        63.69                           53.20              79.03                 61.17                    84.27                 14.17                   39.22                    16.12            40.78
COT                  6.41      64.85 28.35                         57.67                9.90          33.98            34.17        64.66                           52.23              79.42                 58.64                    85.44                 12.82                   41.17                    17.09            43.50
Vert Venn diagram of optimized
                     1.55 code15.92
                                by method
                                          18.64                    64.66                5.44          11.65            38.83        67.57                           49.32              85.44                 60.19                    90.29                 0.97                    4.47                     3.50             31.46
                                                                             Venn diagram of optimized code by method
IRENE                          7.57         70.10        ICL
                                                       40.97       76.89                14.76         50.87            51.84 ICL 83.88                              63.88              93.59                 69.90                    95.92                 17.67                   50.29                    23.30            63.30
                                                           RAG                                                                 RAG
                                                           COT                                                                 COT
                                                           OURS                                                                OURS
                     RAG                    COT                                     RAG                    COT                                                                              100%                                     100%                                 100%                                      100%
                 13                          4                                      13                     17
                                 1                                                                                                                                                                                                                           49.32%
                                                                                                  6
             1                                    9                            4                                   8                                                                                              29.71%
                      7                 18                                              11                 6




                                                                                                                                            Unsafe Rate (Log)
        6                                             48                 5                                              57
                                256                                                               7
                                                                                                                                                                                                                               7.96%                       7.57%
                 5                           19                                    20                          9                                                                 6.99%
  ICL                                                 IRENE        ICL                                                   IRENE
                          19           19                                                    5         1                                                                                                                                                                                                 4.47%
                                 3                                                                5                                                                    3.11%                             3.30%

                                                                                                                                                                                                                                                                                                  1.75%
            (a) Qwen2.5-Coder-32B                                            (b) Qwen2.5-Coder-1.5B                                                                 1.36%                                                                        1.36%

                                                                                                                                                                                                                                                                                         0.78%
Fig. 4: Venn diagrams of successfully translated code generated by
IRENE without refinement and baseline methods on two different                                                                                                                                          2B                                  4B                                      B                                     B
                                                                                                                                                                                                  r-3                                 a-3                                     1.5                                   1.3
parameter sizes of LLMs.                                                                                                                                                                 o   de                                  am                                 d   er-                               d   er-
                                                                                                                                                                                                                            ll                                   Co                                    Co
                                                                                                                                                                                2.   5-C                                 de                                  -                                    k-
                                                                                                                                                                          en                                      Co                                   2.5                                   ee
                                                                                                                                                                                                                                                 en                                     pS
                                                                                                                                                                     Qw                                                                     Qw                                De
                                                                                                                                                                                                                                                                                 e

different methods. Figure 4 presents the Venn diagrams of                                                                                                                                                                             (a) UR

successfully translated code generated by IRENE without                                                                                                                                 94.15%                                      94.15%                               94.15%                                 94.15%
feedback and baseline methods. Regardless of parameter size,
IRENE consistently produces a larger number of uniquely cor-
                                                                                                                                                                                                                                                            12.65%
rect translations. Notably, IRENE identifies 48 and 57 unique
                                                                                                                                            Unsafe Loc Rate (Log)




correct translations in Qwen2.5-Coder-32B and Qwen2.5-
                                                                                                                                                                                3.02%                             3.24%
Coder-1.5B, respectively, while other methods only range
                                                                                                                                                                       1.37%                                                                       1.49%
from 4 to 13 and 5 to 17. This not only demonstrates the
                                                                                                                                                                    0.59%
generalizability of our framework, but also highlights that                                                                                                                                                                0.48%
                                                                                                                                                                                                                                             0.31%
the rule-based guidance provided by IRENE cannot be easily                                                                                                                                              0.12%                                                                                      0.13%
                                                                                                                                                                                                                                                                                               0.10%
replicated by other prompting strategies.
   Comparison of the translation safety metrics. As shown                                                                                                                                                                                                                               0.03%
in Fig. 5, IRENE significantly outperforms both traditional                                                                                                                                         B                                   B                                   B                                       B
                                                                                                                                                                                                -32                                 -34                                 1.5                                  1.3
static and LLM-based baselines in terms of safety. For in-                                                                                                                         o   de
                                                                                                                                                                                            r
                                                                                                                                                                                                                           a   ma                             d   er-                             d    er-
                                                                                                                                                                               5-C                                d   e ll                             -   Co                             k-   Co
                                                                                                                                                                          2.                                 Co                                  2.5                                 ee
stance, IRENE and Vert achieve an average reduction of                                                                                                               en                                                                     en                                  pS
                                                                                                                                                              Qw                                                                      Qw                                De
                                                                                                                                                                                                                                                                           e
82.82% and 98.30% on the UR metric when compared with
                                                                                                                                                                                                 IRENE                         Instruction                        Vert                       C2Rust
C2Rust. These results demonstrate the superiority of LLMs
in generating safe Rust code. Moreover, when compared to                                                                                                                                                                             (b) ULR
Vert, another LLM-based framework, our method achieves
                                                                                                                                      Fig. 5: Comparison between IRENE and three baselines on Unsafe
an average reduction of 15.73% on the UR. This indicates                                                                              Rate (UR) and Unsafe Loc Rate (ULR).
that even under the same LLM-based setting, IRENE is more
effective at producing safe Rust code. In addition, it consis-
tently demonstrates this capability across models of different
sizes. For example, on the larger Qwen2.5-Coder-32B model,                                                                            LLMs. For example, it yields an average reduction of 4.33%
IRENE reduces the Unsafe Rate by 5.63% compared to Vert,                                                                              compared to Vert. IRENE also demonstrates strong perfor-
and on the smaller Qwen2.5-Coder-1.5B model, it achieves a                                                                            mance across models of varying sizes—for instance, achieving
reduction of 47.96%.                                                                                                                  a 2.43% reduction on Qwen2.5-Coder-32B and 12.34% on
   In addition to the UR metric, we also evaluate the ULR,                                                                            Qwen2.5-Coder-1.5B. These results consistently demonstrate
which reflects the proportion of unsafe tokens in the trans-                                                                          that IRENE produces safer Rust code by effectively leveraging
lated code. Similarly, IRENE consistently achieves the best                                                                           rule-based guidance, achieving both accuracy and safety in the
results compared to both C2Rust and Vert across different                                                                             translation process.
        TABLE III: Results of ablation study in translation accuracy. Under each metric, the best performance is highlighted in bold.

                             Deepseek-Coder                                        Qwen2.5-Coder                                                 Codellama
     Approach             1.3B           6.7B             1.5B                7B                   14B                 32B                 7B              34B
                       CA     CSR     CA     CSR       CA     CSR      CA          CSR      CA           CSR    CA           CSR    CA          CSR      CA    CSR
-w/o rule-augmented   6.99   33.79   24.85    38.25    7.57   15.34   46.41        60.00   55.73       67.18   65.83       72.62   6.41         20.39   9.32    38.64
-w/o summarization    5.63   59.61   40.58    78.64   15.34   46.21   53.20        81.94   60.39       89.90   69.13       95.15   16.70        42.14   21.75   67.38
-w/o feedback         6.60   58.45   34.37    63.69   12.82   39.61   44.27        70.49   59.22       81.75   66.02       87.77   15.15        40.58   19.22   44.66
IRENE                 7.57   70.10   40.97    76.89   14.76   50.87   51.84        83.88   63.88       93.59   69.90       95.92   17.67        50.29   23.30   63.30

TABLE IV: An additional experiment about the summary’s quality. ”-better summary” indicates that each model’s summary is generated
by Qwen2.5-Coder-32B.

                             Deepseek-Coder                                    Qwen2.5-Coder                                                     Codellama
     Approach            1.3B           6.7B             1.5B                 7B                 14B                 32B                   7B             34B
                      CA     CSR     CA     CSR       CA     CSR      CA           CSR     CA          CSR     CA            CSR   CA           CSR     CA    CSR
-w/o summarization    5.63   59.61   40.58    78.64   15.34   46.21   53.20        81.94   60.39     89.90     69.13     95.15     16.70        42.14   21.75   67.38
-better summary       9.13   62.91   41.55    74.56   18.45   52.43   54.56        85.05   64.27     93.01     69.90     95.92     17.28        45.83   25.83   61.94
IRENE                 7.57   70.10   40.97    76.89   14.76   50.87   51.84        83.88   63.88     93.59     69.90     95.92     17.67        50.29   23.30   63.30




    Answer to RQ1: IRENE achieves notable improve-                             in CA after removing the summary. To further investigate this
    ments over baselines in both translation accuracy and                      counterintuitive result, we conducted an additional experiment
    safety across different LLMs. It improves CA and CSR                       in which we replaced each model’s self-generated summary
    by 8.06% and 12.74% over the strongest baseline,                           with the one produced by a more powerful model (Qwen2.5-
    demonstrating superior translation accuracy. In terms                      Coder-32B). As shown in Table IV, all models experience a
    of translation safety, it significantly outperforms both                   performance drop when the summary is removed. For instance,
    traditional static tools and LLM-based approaches—                         it suffers a 3.11% reduction in CA on Qwen2.5-Coder-1.5B.
    with an average UR and ULR reduced to just 1.70%                           These results indicate that the effectiveness of the summary
    and 0.26% on average, respectively.                                        largely depends on its quality.
                                                                                  In conclusion, only in rare cases may the model’s limited
                                                                               semantic understanding and generation capability prevent it
B. RQ2: Ablation Study                                                         from fully leveraging the benefits of the summary. In such
   To validate the effectiveness of each module in our frame-                  scenarios, providing a higher-quality summary generated by
work, we perform ablation experiments, as shown in Table III.                  a more powerful model can effectively compensate for this
   Rule-Augmented Retrieval Module. In this experiment,                        limitation.
we remove the rule hints and examples used by LLM to assess                       Error-driven Translation Module. This experiment is to
the effectiveness of the rule-augmented retrieval module. As                   reveal the impact of the error-driven translation module by
shown in Table III, this removal leads to a significant drop                   removing the refinement. As shown in Table III, the absence
in both CA and CSR across all model sizes. For example, on                     of compilation error feedback leads to a noticeable decline in
Qwen2.5-Coder-1.5B, the CA drops from 14.76% to 7.57%,                         performance. For example, it suffers an average reduction of
and the CSR drops from 50.87% to 15.34%. Similarly, on                         4.08% and 12.06% in CA and CSR, respectively. These results
Qwen2.5-Coder-14B, CA decreases from 63.88% to 55.73%,                         highlight the strong self-correction capabilities of LLMs when
and CSR from 93.59% to 67.18%. These results indicate that                     provided with concrete error information, emphasizing the
the rule-augmented module plays a crucial role in enhancing                    importance of iterative refinement during translation.
both the correctness and compilability of translated code. This                   To further evaluate the effect of iteration count, we conduct
suggests that the rule-augmented retrieval module helps LLMs                   additional experiments, with results shown in Fig. 6. The
better adapt to Rust’s strict rules.                                           results yield two main findings. First, increasing the number
   Structured Summarization Module. To assess the effec-                       of iterations leads to consistent improvements in both CA and
tiveness of the structured summarization module, we first                      CSR. Second, the gains begin to plateau after three iterations,
remove the summary generated by this component. Experi-                        indicating diminishing returns from further refinement.
mental results show that the absence of the summary leads
to performance degradation in most models. For example, in                            Answer to RQ2: All components in IRENE contribute
Qwen2.5-Coder-14B, the CA drops by 3.47% and the CSR by                               to the performance. Removing the rule-augmented
3.69%. This highlights the importance of providing the LLM                            retrieval module, structured summarization module,
with its own understanding of the source code.                                        or error-driven translation module leads to substantial
   However, as shown in Table III, a few smaller models, such                         performance decreases.
as Qwen2.5-Coder-1.5B and 7B, show a slight improvement
                                   Deepseek-Coder                                           Qwen2.5-Coder                                    Codellama




                                                                                                                          CA (%)
                                                                       CA (%)
              CA (%)




                                          Iteration                                                Iteration                                  Iteration
                                   Deepseek-Coder                                           Qwen2.5-Coder                                    Codellama
              CSR (%)




                                                                       CSR (%)




                                                                                                                          CSR (%)
                                           Iteration                                               Iteration                                  Iteration
                        (a) CA and CSR in Deepseek-Coder                         (b) CA and CSR in Qwen2.5-Coder                    (c) CA and CSR in Codellama
                                                                                                                                                                  1
                                           Fig. 6: The result of iteration counts in CA and CSR metrics with different LLMs.

TABLE V: Comparison between IRENE and baselines on CSR, UR
and ULR in the HW-Bench. Under each metric, the best performance                                        xCodeEval
is highlighted in bold.
                                                Qwen2.5-Coder                                           HW-Bench
 Approach                   7B                         14B                          32B
                CSR         UR     ULR       CSR       UR      ULR      CSR          UR     ULR
Instruction     20.00      25.00    9.14     20.00     29.00    9.83    27.00       33.00   15.17
ICL             26.00      35.00   10.02     37.00     26.00    9.18    32.00       34.00   14.33
RAG             36.00      38.00   10.53     51.00     33.00   11.60    41.00       36.00   14.04
COT             37.00      40.00   11.00     46.00     28.00    9.63    43.00       36.00   13.36
Vert            35.00      45.00   14.59     53.00     43.00   14.00    61.00       53.00   19.46      Fig. 7: Application domain distributions of xCodeEval and HW-
IRENE           30.00      23.00   7.87      57.00     25.00   5.33     63.00       15.00   3.37
                                                                                                       Bench.

                                                                                                       lowest UR and ULR across all LLMs, with an average reduc-
C. RQ3: Performance in Industrial Scenarios                                                            tion of 14.60% and 6.87%, respectively. These improvements
                                                                                                       highlight IRENE’s superiority in generating safer Rust code
   To assess the applicability of IRENE in the industrial
                                                                                                       compared to five baselines.
scenario, we collaborate with Huawei and randomly select
100 C functions from their product-line codebase. We apply                                                Overall, the results indicate that IRENE not only performs
IRENE to translate these functions into Rust, and compare                                              reliably in the public benchmark, but also generalizes well to
the results against several prompt-based baselines. Due to the                                         industrial scenario. Moreover, following prior work [40], we
limitations of time and resources, we conduct our experiment                                           analyze the application domain distributions of both xCodeE-
only on three open-source LLMs. The experimental result is                                             val and HW-Bench, as shown in Fig. 7. HW-Bench contains
shown in Table V.                                                                                      a higher proportion of operating system–related code, which
   Comparison of the translation accuracy metrics. In the                                              involves system interactions. Despite these challenges, IRENE
absence of practical verification methods, translation accuracy                                        maintains a strong safety performance.
is assessed solely based on the CSR metric, with CA omitted.
As shown in Table V, IRENE consistently achieves the highest                                                   Answer to RQ3: IRENE shows the effectiveness in
CSR across three LLMs. For instance, it yields an average im-                                                  industrial scenarios. On HW-Bench, IRENE achieves
provement of 22.20% under Qwen2.5-Coder-32B, indicating                                                        an average improvement of 12.33% in CSR, compared
strong robustness in handling diverse and complex industrial                                                   with all baselines under employed LLMs. In terms
code. Although other methods may occasionally perform better                                                   of safety, it achieves an average reduction of 14.60%
in CSR, such as in Qwen2.5-Coder-7B, IRENE still maintains                                                     in UR and 6.87% in ULR compared to all baselines
the lowest UR and ULR.                                                                                         across all LLMs. These results demonstrate strong
   Comparison of the translation safety metrics. In terms                                                      robustness and applicability in industrial codebases.
of safety, Table V demonstrates that IRENE achieves the
                                                                         (long long)). The LLM under instruction prompting trans-
                      Case-Summarization
                                                                         lation results in a type mismatch error (error[E0308]) due
     Original C code               Summary of C code                     to inconsistent types within a single expression. In contrast,
    if(b>=0){                  Function:   Starting from                 IRENE successfully addresses this by applying appropriate
       for(i=1; i<=b; i++){    position `a`, moves `b` steps             type conversions. (4) Pointers: As depicted in Fig. 9 (b), the
           m++;                in a circular manner within
       if(m>n) m=1;}}          the range 1 to `n`. If `b` is
                                                                         C code uses malloc to allocate n int memory for variable arr.
    else{m=a;                                                            The LLM under instruction prompting simply uses Vec::new(),
       for(i=1;i<=abs(b);i++){ positive, moves forward; if
           m--;                negative, moves backward.                 while IRENE enables the LLM to use Vec::with capacity(n),
       if(m==0) m=n;}}         Prints the final position.                which better matches the original C’s allocation semantics and
                                                                         avoids unnecessary reallocations.
     Rust Code Translated by Instruction Prompting
                                                                            The ability to better understand the code semantics.
              Result:
              Use modulo operation to directly replace step-
                                                                         The second advantage of IRENE lies in the code summary
              by-step simulation                                         generated by the LLM itself. Without the summary, the LLM
       if b >= 0 {
                                                                         focuses only on the surface structure of the code and tends to
           m = (a + b - 1) % n + 1;}                                     ignore critical semantic constraints. For instance, as illustrated
       else {
           m = (a + n - 1 + b.abs() % n) % n + 1;}                       in Fig 8, the model fails to recognize that the core logic
                                                                         involves the ”circular manner” and instead attempts to simplify
                                                       Result:
                                                                         the loop using modulo operations, which leads to incorrect
     Rust Code Translated by IRENE                                       results. In contrast, when a summary is provided, the clear
                                                       PASSED
       if b >= 0 {m = a;                                                 task description enhances the semantic understanding of the
           for _ in 1..=b {                                              code, guiding the model to generate more accurate translations.
               m += 1;   if m > n {m = 1;}
       else {m = a;                                                      For example, in Fig 8, the summary explicitly identifies the
           for _ in 1..=b.abs(){                                         “circular manner” behavior, effectively preventing the misuse
               m -= 1;   if m == 0 {m = n;}}
                                                                         of modulo operations.
Fig. 8: A case shows that how a structured summary ensures that
the subsequent Rust translation remains semantically faithful. In this   B. Threats to Validity
case, the LLM used is Qwen2.5-Coder-32B.
                                                                            For our study, we discuss three main threats to the validity:
                                                                            The selection of LLMs. One potential threat to validity
                         V. D ISCUSSION
                                                                         stems from the specific LLMs we evaluated. Since our primary
A. Why does IRENE work?                                                  goal is to enable deployment in industrial settings, we focused
   In this section, we identify the following two advantages             exclusively on eight popular open-source LLMs. This may
of IRENE, which can explain its effectiveness and safety in              limit the generalizability of our findings. In future work, we
C-to-Rust translation. For each advantage, we demonstrate the            plan to extend our evaluation to include closed-source models
corresponding cases, as shown in Fig. 1 and Fig. 8 - 9.                  such as ChatGPT and Gemini to further assess the general
   The ability to adapt to Rust’s specific rules. The first              effectiveness of our framework.
advantage of IRENE lies in its rule-based translation examples.             Potential data leakage. Given that the pre-training data of
LLMs heavily rely on pretraining knowledge. Without explicit             Deepseek-Coder and Qwen2.5-Coder is not publicly disclosed,
guidance, it is quite difficult for them to accurately apply Rust-       concerns about potential data leakage are understandable.
specific rules during translation. IRENE provides both rule              However, we observe that when these models are prompted
hints and concrete translation examples to assist the model,             without our framework, the translation quality significantly
guiding it to produce more accurate and idiomatic Rust code.             degrades. This discrepancy strongly suggests that IRENE ’s
As shown in Fig.1 and Fig.9, the Rust code translated by                 performance gains are not attributable to memorized training
IRENE demonstrates better correctness and explicitly handles             content.
Rust-specific rules. Specifically, for different rule categories:           Representativeness of datasets. Another threat comes from
(1) I/O: As shown in Fig. 1 (a), the original C code uses                the representativeness of the evaluation datasets. In this paper,
scanf to input multiple variables. The LLM under instruction             we use two datasets: one is the open-source XCodeEval, which
prompting chooses read line, which causes errors due to                  primarily consists of programming competition-style code; the
its semantic mismatch with scanf. In contrast, IRENE uses                other is a manually collected set of functions from proprietary
read to string combined with split whitespace, achieving a               industrial projects. Due to confidentiality constraints, the in-
semantically equivalent conversion. (2) Array: Fig. 1 (b)                dustrial dataset cannot be released publicly, which may hinder
demonstrates that IRENE correctly uses the usize type for                reproducibility and broader evaluation. In future work, we
indexing arrays, rather than the incorrect i32 used by the               plan to expand our evaluation to include more diverse and
LLM under instruction prompting. (3) Mixtype: As illustrated             representative codebases to further validate the generality of
in Fig. 9 (a), the C code uses explicit type casting (e.g.,              IRENE.
                      Rule category: Mixtype                                             Rule category: Pointer
         Original C code            : C code snippet requiring              Original C code            : C code snippet requiring
         int main() {               specific translation rules               int main()                specific translation rules
             static int ff[X + 1], dp[X + 1][N];                             {
             long long z = 0;                                                    int i,temp=0,n,k,x,*arr;
             for (l = 1; l < n; l++) {                                           arr=malloc(n*sizeof(int));
                 long long z = (long long) dp[i - 1][l] * \                      for(i=0;i<n;i++){
                 ff[i - 2] % MD;                                                     scanf("%d",&arr[i]);

         Rust Code Translated by Instruction Prompting                      Rust Code Translated by Instruction Prompting
                 Result:                                                             Result:
                 error[E0308]: mismatched Types -->                                  No pre-allocated space. Memory reallocation
                 test.rs:67:51 expected `u64`, found `usize`
                                                                              let mut arr = Vec::new();
           let mut z = 0;                                                     for _ in 0..n {
           for l in 1..n {                                                      let num: i32 = input.trim().parse().unwrap();
              let mut z = dp[i-1][l] as u64 * ff[i-2] % MD;                     arr.push(num);


         Rust Code Translated by IRENE                    Result:           Rust Code Translated by IRENE                  Result:
                                                          PASSED                                                           PASSED
           let mut z = 0;                                                    let mut arr: Vec<i32> = Vec::with_capacity(n);
           let mut z = (dp[i - 1][l] as i64 * \                              for _ in 0..n {
           ff[i - 2] as i64) % MD as i64;                                    arr.push(parts.next().unwrap().parse().unwrap());

                        (a) Rule category: Mixtype                                          (b) Rule category: Pointer
Fig. 9: Two additional cases illustrate that how IRENE improves translation results by addressing two different categories of rules based on
Qwen2.5-Coder-32B.


                     VI. R ELATED W ORK                                strategy. Syzygy [42] combines LLMs with sampling and test-
A. Rule-based C-to-Rust translation                                    based feedback. C2SaferRust [23] integrates call graph and
                                                                       data flow analysis with LLMs and feedback repair. SAC-
   Rule-based translation approaches rely on predefined trans-
                                                                       TOR [24] leverages static tools such as C2Rust and Crown to
formation rules and compiler tools to convert C code into
                                                                       assist LLMs. Compared to these approaches, IRENE enhances
structurally equivalent Rust code. These methods typically
                                                                       both static rule and semantic understanding, and produces
perform AST-level level transformations, mapping C con-
                                                                       more reliable and safer Rust code.
structs—including pointers, structs, and manual memory man-
agement—into Rust’s corresponding syntax and APIs. For                    In addition to these translation methods, some LLM-based
example, the widely used tool C2Rust [10], built on Clang              studies focus on specific aspects. For example, Hong et al.
and LLVM, translates C code into unsafe Rust through C-Rust            [43] target the translation of function signatures. Eniser et al.
FFI. Subsequent work [13]–[16], [41], builds on the C2Rust             [22] apply fuzz testing to validate translation correctness. Li et
tool, introducing improvements from various perspectives.              al. [44] conduct a user study to investigate how human experts
Emre et al. [15], [16] proposes the pseudo-safety technique,           perform code translation.
which addresses the problem of dereferencing raw pointers by
emulating C-style aliasing behavior using Rust’s raw pointers.
                                                                                               VII. C ONCLUSION
Concrat [13] developed a static analyzer specifically designed
to handle Lock API. Crown [14] defines a set of ownership
rules to guide the conversion of pointer types. In contrast to            In this paper, we propose IRENE, an LLM-based framework
these tools, IRENE combines predefined static analysis rules           for C-to-Rust translation. IRENE enhances the capabilities of
with summarization of the code to enhance the automation and           large language models by integrating both rule-based guid-
precision of rewriting.                                                ance and semantic understanding. It consists of three key
                                                                       components: a rule-augmented retrieval module, a structured
B. LLM-based C-to-Rust translation                                     summarization module, and an error-driven translation mod-
  LLM-based approaches employ LLMs to translate C pro-                 ule. Extensive experiments demonstrate the effectiveness of
grams into Rust by capturing patterns from programming                 IRENE across various models and settings. Ablation studies
corpora. LLM-based approaches incorporate structural and               further highlight the unique contributions of each component.
semantic information into prompts to guide translation, and            In future work, we plan to extend IRENE to support more
apply feedback to refine outputs. For instance, Vert [21] uses         programming languages, such as C++, and to tackle larger-
LLMs to generate Rust code from C with a feedback-based                scale translation tasks at the project level.
                              R EFERENCES                                         [24] T. Zhou, H. Lin, S. Jha, M. Christodorescu, K. Levchenko, and V. Chan-
                                                                                       drasekaran, “Llm-driven multi-step translation from C to rust using static
                                                                                       analysis,” CoRR, vol. abs/2503.12511, 2025.
 [1] J. Hong, “Improving automatic c-to-rust translation with static analysis,”
     in ICSE Companion, pp. 273–277, IEEE, 2023.                                  [25] Z. Yang, F. Liu, Z. Yu, J. W. Keung, J. Li, S. Liu, Y. Hong, X. Ma,
                                                                                       Z. Jin, and G. Li, “Exploring and unleashing the power of large language
 [2] H. Chen, Y. Mao, X. Wang, D. Zhou, N. Zeldovich, and M. F.
                                                                                       models in automated code translation,” Proc. ACM Softw. Eng., vol. 1,
     Kaashoek, “Linux kernel vulnerabilities: state-of-the-art defenses and
                                                                                       no. FSE, pp. 1585–1608, 2024.
     open problems,” in APSys, p. 5, ACM, 2011.
 [3] Z. Durumeric, J. Kasten, D. Adrian, J. A. Halderman, M. D. Bailey, F. Li,    [26] M. A. M. Khan, M. S. Bari, X. D. Long, W. Wang, M. R. Parvez,
     N. Weaver, J. Amann, J. Beekman, M. Payer, and V. Paxson, “The matter             and S. Joty, “Xcodeeval: An execution-based large scale multilingual
     of heartbleed,” in Internet Measurement Conference, pp. 475–488, ACM,             multitask benchmark for code understanding, generation, translation
     2014.                                                                             and retrieval,” in Proceedings of the 62nd Annual Meeting of the
                                                                                       Association for Computational Linguistics (Volume 1: Long Papers),
 [4] D. Herman, “Rewriting a browser component in rust.” https://hacks.
                                                                                       ACL 2024, Bangkok, Thailand, August 11-16, 2024 (L. Ku, A. Martins,
     mozilla.org/2019/02/rewriting-a-browser-component-in-rust/, 2019. Ac-
                                                                                       and V. Srikumar, eds.), pp. 6766–6805, Association for Computational
     cessed: 2025-05-19.
                                                                                       Linguistics, 2024.
 [5] Rust for Linux, “Nova: a rust-based gpu driver.” https://rust-for-linux.
     com/nova-gpu-driver, 2024. Accessed: 2025-05-19.                             [27] G. Ou, M. Liu, Y. Chen, X. Peng, and Z. Zheng, “Repository-level code
                                                                                       translation benchmark targeting rust,” CoRR, vol. abs/2411.13990, 2024.
 [6] Google Security Blog, “Rust in the android platform.” https://security.
     googleblog.com/2021/04/rust-in-android-platform.html, 2021.          Ac-     [28] IRENE, “Replication package of irene.” https://anonymous.4open.
     cessed: 2025-05-19.                                                               science/r/IRENE-2E0E, 2025.
 [7] H. Zhang, C. David, Y. Yu, and M. Wang, “Ownership guided C to               [29] S. E. Robertson and H. Zaragoza, “The probabilistic relevance frame-
     rust translation,” in CAV (3), vol. 13966 of Lecture Notes in Computer            work: BM25 and beyond,” Found. Trends Inf. Retr., vol. 3, no. 4,
     Science, pp. 459–482, Springer, 2023.                                             pp. 333–389, 2009.
 [8] J. Hong and S. Ryu, “To tag, or not to tag: Translating c’s unions to        [30] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal,
     rust’s tagged unions,” in ASE, pp. 40–52, ACM, 2024.                              A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-
 [9] M. Ling, Y. Yu, H. Wu, Y. Wang, J. R. Cordy, and A. E. Hassan, “In rust           Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. M. Ziegler,
     we trust - A transpiler from unsafe C to safer rust,” in ICSE-Companion,          J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray,
     pp. 354–355, ACM/IEEE, 2022.                                                      B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever,
[10] Immunant, “C2rust.” https://github.com/immunant/c2rust, 2022.                     and D. Amodei, “Language models are few-shot learners,” in NeurIPS,
                                                                                       2020.
[11] LLVM Project, “Clang: A c language family frontend for llvm.” https:
     //clang.llvm.org/. Accessed: 2025-05-26.                                     [31] W. Fan, Y. Ding, L. Ning, S. Wang, H. Li, D. Yin, T. Chua, and Q. Li,
[12] C. Lattner and V. S. Adve, “LLVM: A compilation framework for                     “A survey on RAG meeting llms: Towards retrieval-augmented large
     lifelong program analysis & transformation,” in 2nd IEEE / ACM                    language models,” in KDD, pp. 6491–6501, ACM, 2024.
     International Symposium on Code Generation and Optimization (CGO             [32] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi,
     2004), 20-24 March 2004, San Jose, CA, USA, pp. 75–88, IEEE                       Q. V. Le, and D. Zhou, “Chain-of-thought prompting elicits reasoning in
     Computer Society, 2004.                                                           large language models,” in Advances in Neural Information Processing
[13] J. Hong and S. Ryu, “Concrat: An automatic c-to-rust lock API translator          Systems 35: Annual Conference on Neural Information Processing
     for concurrent programs,” in 45th IEEE/ACM International Conference               Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 -
     on Software Engineering, ICSE 2023, Melbourne, Australia, May 14-20,              December 9, 2022 (S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave,
     2023, pp. 716–728, IEEE, 2023.                                                    K. Cho, and A. Oh, eds.), 2022.
[14] H. Zhang, C. David, Y. Yu, and M. Wang, “Ownership guided C to               [33] D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi,
     rust translation,” in Computer Aided Verification - 35th International            Y. Wu, Y. K. Li, F. Luo, Y. Xiong, and W. Liang, “Deepseek-coder:
     Conference, CAV 2023, Paris, France, July 17-22, 2023, Proceedings,               When the large language model meets programming - the rise of code
     Part III (C. Enea and A. Lal, eds.), vol. 13966 of Lecture Notes in               intelligence,” CoRR, vol. abs/2401.14196, 2024.
     Computer Science, pp. 459–482, Springer, 2023.                               [34] B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang,
[15] M. Emre, R. Schroeder, K. Dewey, and B. Hardekopf, “Translating C to              B. Yu, K. Dang, et al., “Qwen2. 5-coder technical report,” arXiv preprint
     safer rust,” Proc. ACM Program. Lang., vol. 5, no. OOPSLA, pp. 1–29,              arXiv:2409.12186, 2024.
     2021.                                                                        [35] B. Rozière, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi,
[16] M. Emre, P. Boyland, A. Parekh, R. Schroeder, K. Dewey, and B. Hard-              J. Liu, T. Remez, J. Rapin, A. Kozhevnikov, I. Evtimov, J. Bitton,
     ekopf, “Aliasing limits on translating C to safe rust,” Proc. ACM                 M. Bhatt, C. Canton-Ferrer, A. Grattafiori, W. Xiong, A. Défossez,
     Program. Lang., vol. 7, no. OOPSLA1, pp. 551–579, 2023.                           J. Copet, F. Azhar, H. Touvron, L. Martin, N. Usunier, T. Scialom, and
[17] J. Hong, “Improving automatic c-to-rust translation with static analysis,”        G. Synnaeve, “Code llama: Open foundation models for code,” CoRR,
     in 45th IEEE/ACM International Conference on Software Engineering:                vol. abs/2308.12950, 2023.
     ICSE 2023 Companion Proceedings, Melbourne, Australia, May 14-20,            [36] Hugging Face, Inc., “Hugging face: The platform for machine learning
     2023, pp. 273–277, IEEE, 2023.                                                    and nlp.” https://huggingface.co/. Accessed: 2025-05-26.
[18] M. Shiraishi and T. Shinagawa, “Context-aware code segmenta-                 [37] PyTorch Contributors, “Pytorch: An open source machine learning
     tion for c-to-rust translation using large language models,” CoRR,                framework.” https://pytorch.org/. Accessed: 2025-05-26.
     vol. abs/2409.10506, 2024.                                                   [38] S. Gao, X. Wen, C. Gao, W. Wang, H. Zhang, and M. R. Lyu, “What
[19] M. Shetty, N. Jain, A. Godbole, S. A. Seshia, and K. Sen, “Syzygy: Dual           makes good in-context demonstrations for code intelligence tasks with
     code-test C to (safe) rust translation using llms and dynamic analysis,”          llms?,” in 38th IEEE/ACM International Conference on Automated
     CoRR, vol. abs/2412.14234, 2024.                                                  Software Engineering, ASE 2023, Luxembourg, September 11-15, 2023,
[20] V. Nitin, R. Krishna, L. L. do Valle, and B. Ray, “C2saferrust: Trans-            pp. 761–773, IEEE, 2023.
     forming C projects into safer rust with neurosymbolic techniques,”           [39] P. Bailey, R. W. White, H. Liu, and G. Kumaran, “Mining historic query
     CoRR, vol. abs/2501.14257, 2025.                                                  trails to label long and rare search engine queries,” ACM Trans. Web,
[21] A. Z. H. Yang, Y. Takashima, B. Paulsen, J. Dodds, and D. Kroening,               vol. 4, no. 4, pp. 15:1–15:27, 2010.
     “Vert: Verified equivalent rust transpilation with large language models     [40] Y. Cheng, J. Chen, J. Chen, L. Chen, L. Chen, W. Chen, Z. Chen,
     as few-shot learners,” 2024.                                                      S. Geng, A. Li, B. Li, B. Li, L. Li, B. Liu, J. Liu, K. Liu, Q. Liu,
[22] H. F. Eniser, H. Zhang, C. David, M. Wang, M. Christakis, B. Paulsen,             S. Liu, S. Liu, T. Liu, T. Liu, Y. Liu, R. Long, J. Mai, G. Ning, Z. Y.
     J. Dodds, and D. Kroening, “Towards translating real-world code with              Peng, K. Shen, J. Su, J. Su, T. Sun, Y. Sun, Y. Tao, G. Wang, S. Wang,
     llms: A study of translating to rust,” CoRR, vol. abs/2405.11514, 2024.           X. Wang, Y. Wang, Z. Wang, J. Xia, L. Xiang, X. Xiao, Y. Xiao, C. Xi,
[23] V. Nitin, R. Krishna, L. L. do Valle, and B. Ray, “C2saferrust: Trans-            S. Xin, J. Xu, S. Xu, H. Yang, J. Yang, Y. Yang, J. Yuan, J. Zhang,
     forming C projects into safer rust with neurosymbolic techniques,”                Y. Zhang, Y. Zhang, S. Zheng, H. Zhu, and M. Zhu, “Fullstack bench:
     CoRR, vol. abs/2501.14257, 2025.                                                  Evaluating llms as full stack coders,” CoRR, vol. abs/2412.00535, 2024.
[41] J. Hong and S. Ryu, “Don’t write, but return: Replacing output pa-
     rameters with algebraic data types in c-to-rust translation,” Proc. ACM
     Program. Lang., vol. 8, no. PLDI, pp. 716–740, 2024.
[42] M. Shetty, N. Jain, A. Godbole, S. A. Seshia, and K. Sen, “Syzygy: Dual
     code-test C to (safe) rust translation using llms and dynamic analysis,”
     CoRR, vol. abs/2412.14234, 2024.
[43] J. Hong and S. Ryu, “Type-migrating c-to-rust translation using a large
     language model,” Empir. Softw. Eng., vol. 30, no. 1, p. 3, 2025.
[44] R. Li, B. Wang, T. Li, P. Saxena, and A. Kundu, “Translating C to rust:
     Lessons from a user study,” in 32nd Annual Network and Distributed
     System Security Symposium, NDSS 2025, San Diego, California, USA,
     February 24-28, 2025, The Internet Society, 2025.
