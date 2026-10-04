# RagVerus: Repository-Level Program Verification with LLMs using Retrieval Augmented Generation

Si Cheng Zhong 1 , Jiading Zhu 1 † , Yifang Tian 1 † , and Xujie Si 1

University of Toronto, Canada sicheng.zhong@mail.utoronto.ca , six@cs.toronto.edu

Abstract. Scaling automated formal verification to real-world projects requires resolving cross-module dependencies and global contexts, which are challenges overlooked by existing function-centric methods. We introduce RagVerus, a framework that synergizes retrieval-augmented generation with context-aware prompting to automate proof synthesis for multi-module repositories, achieving a 27% relative improvement on our novel RepoVBench benchmark—the first repository-level dataset for Verus with 383 proof completion tasks. RagVerus triples proof pass rates on existing benchmarks under constrained language model budgets, demonstrating a scalable and sample-efficient verification.

# 1 Introduction

Good engineers favor well-written tests to confirm that code works correctly, at least for the tested inputs. In software verification, testing is replaced by a set of complete specification; a verifier conducts a compile-time check to ensure the implementation matches the specification, providing vital assurances especially for high-confidence systems in critical areas such as operating systems and financial applications [\[17](#page-11-0) [,32\]](#page-11-1). However, proof construction is a challenging process that requires domain expertise [\[29](#page-11-2) [,11](#page-10-0) [,15\]](#page-10-1). This process is time-consuming and non-trivial especially for large software projects.

Advances in generative AI for code completion have spurred interest in verification-aware program synthesis, aiming to simultaneously enhance code trustworthiness and automate proof generation [ [8](#page-10-2) [,30](#page-11-3) [,26\]](#page-11-4). Large language models (LLMs) streamline formal verification by rapidly sampling and iterating proof candidates, lowering barriers to adoption [ [4](#page-10-3) , [1](#page-10-4) , [3\]](#page-10-5). However, current functionlevel program verification approaches inherit vanilla retrieval models [\[32,](#page-11-1)[3\]](#page-10-5) from theorem proving that solely rely on finetuned embedding encoders using prior examples [\[31\]](#page-11-5), lacking the rich, precise domain knowledge of code syntax or project structure [\[24\]](#page-11-6). Moreover, existing datasets [\[21\]](#page-11-7) are derived for small-scale, isolated contexts, lacking evaluation in complex repository settings to reflect real practices in production.

We recognize the main challenges of repository-level verification tasks to be (1) the vast semantic context and (2) the identification of correct dependent premises, as noted in prior works studying large-scale verification in the theorem proving domain [17,31,10]. A major challenge in LLM proof generation is premise retrieval—selecting the minimal lemma set from a repository-level codebase that aids verification while fitting within the context window. Scaling verification to repository level adds complexity due to inter-dependencies in large codebases, while the lack of benchmark data limits furthur evaluation in the area.

To assess LLM-based formal repository-level program verification, we establish three main contributions in this paper:

We propose RAGVERUS, a new verification framework integrating retrieval-augmented generation (RAG) with context-aware prompting to guide LLMs in synthesizing verifiable code for interdependent, large-scale codebases. We provide a configurable RAG pipeline to enable systematic evaluation of diverse retrieval strategies (e.g., semantic search, dependency graphs) within a sandboxed Verus environment, informing cross-module dependencies and project-specific invariants.

We also construct RepoVBench, the first repository-level program verification benchmark, where we collect recent award-winning Verus projects and extract programs with complex dependencies. Specifically, we build a dataset containing 2073 functions with dependencies over 52 modules, supporting evaluation on 383 proof completion tasks.

We further evaluate RAGVERUS on two benchmarks: VerusBench from AUTOVERUS [30], which is a function-level verification benchmark, and the new repository-level verification benchmark, RepoVBench. On VerusBench, RAGVERUS demonstrates a 200+% improvement in proof pass rates compared to the non-RAG baseline under constrained sampling budgets. On RepoVBench, our framework produces contextually coherent proofs to solve 5% more of the benchmark (27% relative increase), outperforming isolated function-level approaches.

### 2 Background

Verus [12] is an SMT-based verification tool designed to formally verify Rust programs while leveraging Rust's powerful type system, in particular its linearity and borrow checking mechanisms. Users write its domain-specific language (DSL) inline with Rust, while dividing Rust code into three code modes: *specification* annotation, *proof* annotation, and *executable* implementation. Verification in Verus is performed by encoding Rust functions and their associated annotations as SMT formulas [5], which are then processed by an SMT solver such as Z3 [6]. Recently, AutoVerus [30], an LLM-based approach shows strong performance in automating proof completion in Verus solving nearly all tasks of VerusBench.

RAG [14] is a novel technique to enhance generative models by incorporating external knowledge retrieval, enabling more accurate and contextually relevant responses in knowledge-intensive tasks. Existing RAG methods [21,32] used in the software verification domain are relatively simple, such as directly comparing the method signatures and post-conditions. We draw inspiration from repository-level code generation [24] and theorem proving [31] domains, examining a framework to capture the structured nature of programming tasks.

# <span id="page-2-0"></span>3 RagVerus Framework

![](_page_2_Figure_3.jpeg)

Fig. 1: Illustration of the RagVerus Framework Pipeline

We propose RagVerus, a retrieval-augmented framework for LLM-based program verification, with a special focus on complex Verus projects. The framework modularizes verification task preparation, context retrieval methods, and proof generation models, leveraging repository information and verifier feedback to align domain knowledge.

### 3.1 The General Pipeline

As illustrated in Fig. [1,](#page-2-0) the RagVerus pipeline consists of three stages: 1) mining code properties, 2) retrieving task-specific information, and 3) finally generating proofs and/or verifiable code.

Mining Code Properties. We preprocess repository-wide code artifacts to extract verification-critical metadata (more details in Section 4.1), building on insights from context modeling in repository-level code generation [\[24\]](#page-11-6). Through static analysis over the codebase hierarchy, we identifying function/type signatures, method calls, module dependencies, and control/dataflow relationships essential for proof construction.

To enable efficient retrieval, RagVerus uses persistent vector stores where documents are encoded into embeddings using OpenAI's text-embedding-3-large [\[23\]](#page-11-8), indexed via FAISS [\[7\]](#page-10-11). Depending on the retrieval method chosen, either the Rust code themselves or their metadata is indexed. This hybrid representation preserves both syntactic and semantic patterns in the form of high-dimensional embeddings, enabling adaptive context retrieval in later stages.

Context Retrieval. We believe two general kinds of retrieval tasks are essential for repository verification. Few-shot example retrieval matches code snippets or metadata to provide contextual proof patterns and exemplar code-proof pairs, while Dependency retrieval identifies function signatures and domain-specific syntax necessary for constructing proofs. Retrieved contexts are integrated into prompts to guide proof generation, with examples expanded in Section [3.2.](#page-3-0)

### 4 S. Zhong et al.

Proof Generation. This stage accepts a generic code generation agent like AutoVerus. The framework processes Rust modules containing executable code and Verus specifications (pre-/post-conditions) without existing proof annotations. Language models synthesize verification annotations—loop invariants, assertions, and proof blocks—conditioned on retrieved contexts to produce a fully annotated Rust program. Verus compiler validates if specifications hold across all situations, with failed proofs triggering iterative refinement—feeding back compiler errors to the agent—if requested.

While being evaluated on proof generation tasks, RagVerus can also support flexible extensions for code generation as well as specification inference.

### <span id="page-3-0"></span>3.2 Instantiations of Retrieval Module

Building upon the modular framework established in Section 3.1, this subsection presents customizable retrieval modules tailored to address distinct program verification challenges, each designed to align with specific task requirements within the verification pipeline.

Few-Shot Example Retrieval Few-shot example retrieval in RagVerus involves selecting a small number of representative examples to guide the LLM's automated proof generation. The objective is to retrieve relevant code snippets or contexts as contextual prompts, ensuring that generated annotations adhere to correct styles and practices. To achieve this, the retrieval process leverages FAISS [\[7\]](#page-10-11) to identify the most semantically similar examples, implemented through LlamaIndex [\[20\]](#page-11-9). During retrieval, depending on the method chosen, either the input code or its metadata is used as the query vector. The FAISS vector store then retrieves the top-k most similar examples, with an ID filter ensuring that the input document itself is excluded from the retrieved examples.

Two separate vector indices are created for each dataset: one for code body embeddings and one for code informalization embeddings. The embeddings are built only with unverified files, but during retrieval, the corresponding verified files are also retrieved, forming input-output pairs as few-shot examples. We retain a maximum of three examples after ranking, prioritizing diversity and relevance. These examples provide contextual references that enhance the LLM's ability to generate relevant and accurate proofs [\[2\]](#page-10-12), ultimately improving the overall quality and precision of the verification process.

- Code-Based Example Selection. Searching by code embeddings effectively provides relevant reference examples by capturing structural and functional similarities between code implementations. This is particularly beneficial for the task of program verification, as it ensures that retrieved examples align with correct coding patterns and verification logic, improving the accuracy and consistency of proof generation.
- Informalization-Based Example Selection. This process generates natural language contexts of the target Rust function as supplementary

information for retrieval. It takes the code implementation and the essential metadata [\[24\]](#page-11-6) of each Rust function as input and produces a detailed natural language description of the function behaviour, which we refer to as the informalized code summary. Matching these summaries by semantic similarities during context retrieval enhances knowledge of relevant topics and verification flow on the topic.

![](_page_4_Figure_3.jpeg)

Fig. 2: Illustration of code informalization utility.

Dependency Retrieval Dependency retrieval identifies all relevant function signatures within the code repository that should serve as dependent premises for generating proofs for a particular task. A well-chosen premise pool provides essential context, such as file dependencies and variable typing, ensuring accurate and complete proof generation. Understanding premise dependencies involves knowing available functions and their interactions within the codebase. Accurately identifying these relevant functions creates an essential toolkit for the LLM to elaborate on, streamlining the generation process and minimizing redundant generation. We recommend three primary methods:

- Embedding-based Dependency Retrieval. This method heuristically operates with the assumption that functions similar to the input function can serve as its premises; for example, a function less\_than can serve as premise for less\_equal. Similarity is determined using embeddings derived from both the code itself and its functional summary. FAISS is used to perform nearest-neighbor retrieval in the embedding space.
- Finetuned Projection Matching. In this approach, a specialized embedding model is trained to project the embedding of the input code close to the embeddings of its logical premises. The model is trained using a set of human-labeled function-premise pairs, allowing it to learn the relationships between input functions and their relevant premises.
- Dependency Graph. This method leverages static analysis on the abstract syntax tree generated by the compiler to construct a dependency graph for the codebase. The premises of the input function are derived by traversing the call hierarchies and extracting functions on which the input function depends directly or indirectly.

These methods complement each other, with similarity retrieval providing a heuristic baseline, embedding projection leveraging learned relationships, and the dependency graph offering a deterministic, compiler-supported solution.

# 4 RepoVBench: A Repository-level Verification Benchmark

Existing benchmarks focus on function-level proof generation [\[30,](#page-11-3)[1\]](#page-10-4), where all contexts are self-contained in single files, and have become saturated—with tools like AutoVerus achieving over 90% success rates—offering little challenge or differentiation for emerging techniques. We introduce RepoVBench to address the absence of repository-level benchmarks in Verus, capturing complexities of full-scale codebases involving inter-module interactions and environmental dependencies.

Our new benchmark consists of three core components: Code (a curated set of repositories utilizing Verus), Environment (a standardized build setup), and Metric (evaluating verification effectiveness). We provide users with flexible control over running experiments, enabling customized assessments that reflect practical challenges in formal verification.

### 4.1 Creating Benchmark from Code Repositories

We generate benchmark datasets from Verus repositories by processing the Rust files through two modules that flexibly create downstream tasks and build supporting contexts for retrieval agents.

Code Masking with Verus Property Extractor. We build a new extraction tool utilizing a property parser from the Verus compiler to identify formal properties such as preconditions, postconditions, and invariants. We leverage the code mode hierarchy to precisely control over exec, spec, and proof code, enabling the flexible creation of various downstream tasks for evaluation. For instance, to create a proof completion task, we erase proof lines from the verified functions or modules to form queries. See Appendix [A](#page-12-0) for an illustrative example.

Metadata Generation. To build supporting contexts for the benchmark, we extract key metadata from Rust functions. We create a unique index of content by breaking down constructs like type and class definitions, making each function searchable for retrieval tasks. The metadata contains 1) various names including the file name, function name and construct name, 2) function's type signature, 3) methods invocations, 4) type identifiers and variable declarations appearing in the function, and 5) the function's code mode. We use code mode to assess whether a function can serve as potential dependencies in a selected type of task, guided by the exec-proof-spec hierarchy's constraint that higher-assurance modes (proof) cannot invoke lower-assurance implementations (exec).

## 4.2 RepoVBench Data Source and Environment

We build the initial RepoVBench upon the VeriSMo project [\[33\]](#page-11-10), a verified security module developed for confidential virtual machines (VMs) running on a specific AMD architecture. Using Rust and the Verus verification tool, VeriSMo performs permission-based reasoning to ensure memory safety and confidentiality.

We extracted 2,073 code pieces from VeriSMo, including macro definitions and functions, and parsed 1,656 indexable functions, out of which we identified 460 functions containing proof lines in the original code using the syntax tracer. We further filtered out functions that the compiler can automatically solve even without proof code, which resulted in 383 tasks for the benchmark. These tasks are functions that include spec in their definitions and require proof bodies to be completed, which in total consists of 8,108 lines of proof, a mean of 17 lines of proof per verification task (with a median of 8). We analyze the ground truth proofs and split the benchmark into two categories based on whether the proofs depend on other function calls — 52 Simple tasks, which have no dependencies, and 331 Complex tasks, which require dependencies.

Environment. We develop a build pipeline to evaluate RepoVBench in an encapsulated environment that ensures reproducible verification outcomes and enhances ease of experiment. For every request to test some varifiable code, we make a segregated work tree to track code changes, compile independently, and revert to clean states, allowing concurrent execution of different experiments.

Ongoing and Future Effort. We are in the process of expanding RepoVBench by adding a wider array of verification repositories. One immediate goal is to include Anvil [\[27\]](#page-11-11), a formal tool built upon Verus for verifying Kubernetes controller correctness. We anticipate RepoVBench will keep growing as Verus becomes increasingly popular over time.

### 4.3 Metric

The primary metric for evaluating the verification dataset is the number of success - tasks proven to be both correct and safe:

- Correctness The code is correct if the generated annotations pass Verus compilation, which checks for constraint propagation throughout the project, validating the required specifications and logical correctness.
- Safety The code is safe[1](#page-6-0) if the implementation lines stays unaltered, thus maintaining the original functionalities. We utilize the Lynette checker from AutoVerus to examine the code consistency.

As verification success is a rigid binary metric, the BLEU score similarity is more suitable for signaling gradual improvement. We may also consider the style of the generated code by comparing it to the ground-truth reference using BLEU score to assess the alignment with expected coding standards.

<span id="page-6-0"></span><sup>1</sup> following terminology in AutoVerus [\[30\]](#page-11-3) referring untampered implementation and specification as safe code

#### 5 Evaluation

We run the evaluation pipeline against two datasets respectively: VerusBench [30] and RepoVBench that we created. Although VerusBench is not a repository-level verification dataset, we conducted this experiment to confirm the performance increase after introducing the RAG module.

Model of Choice. We chose GPT-4o (gpt-4o-2024-08-06) [22], the newest version of large language model offered by OpenAI at the time of the experiment as our model of choice. The temperature is set to 1.0 during sampling.

Dataset Preparation and Example Pool Creation. For experiments with VerusBench [30], the dataset used for retrieval consists of unverified and verified Rust files from three benchmarks: Diffy, MBPP, and Misc. In addition, example Rust files originally used in the refinement phase of the AutoVerus [30] pipeline were also included. For experiments on RepovBench, only code documents within the repository are indexed and retrieved.

**RAG** modules. For few-shot example retrieval, we experimented with both the code index and the informalization index. For dependency retrieval, due to limited amount of data in our current dataset, we only evaluate the simple embedding-based dependency retrieval approach. We leave the more advanced approaches for dependency retrieval such as dependency graphs and embedding projection for future work.

#### 5.1 Evaluation on Function-Level Verification

While the full AutoVerus pipeline is already highly effective on this relatively small and constrained dataset (proving 137 out of 150 tasks in VerusBench) [30], our goal here is to demonstrate the effectiveness of RAG, which represents an orthogonal contribution. Therefore, we choose our baseline to be the direct-generation pipeline presented in the original AutoVerus paper. While the original process samples up to 125 answers, we limit sampling to 5 times for each of our setups to examine the benefits from retrieval modules.

The performance comparison between different retrieval strategies is shown in Table 1. RAGVERUS-Code denotes the results achieved by performing retrieval on the code index; similarly, RAGVERUS-Text retrieves on the informalization index.

RagVerus-Code consistently outperformed other methods, achieving the highest counts of correct, safe, and successful completions overall (87, 134, 84) and excelling particularly in MBPP. Retrieval using informalized summaries also substantially improved over the Baseline, with a notable edge over code-based retrieval in count of success for Diffy tasks (23 vs. 19). The experiment results confirmed that context retrieval methods contribute to the overall success of RagVerus. Comparing to the baseline results reported in the AutoVerus paper, the same baseline could only solve 67 tasks even with a maximum LLM invocation allowance of 125.

<span id="page-7-0"></span> $<sup>^{2}</sup>$  AutoVerus was also tested on the unpublished Verus-CloverBench

Model Task Correct (n, %) Safe (n, %) Success (n, %) Baseline 23 (29.5%) 60 (76.9%) 17 (21.8%) MBPP RAGVERUS - Code 54 (69.2%) 57 (73.1%) 74 (94.9%) RagVerus - Text 49 (62.8%) 68 (87.2%) 45 (57.7%) Baseline 3(7.9%)30 (78.9%) 2(5.3%)Diffv RAGVERUS - Code 19 (50.0%) 38 (100.0%) 19 (50.0%) RagVerus - Text 24 (63.2%) 37 (97.4%) 23 (60.5%) 21 (91.3%) 6 (26.1%) Baseline 7 (30.4%) Misc RagVerus - Code 11 (47.8%) 22 (95.7%) 11 (47.8%) RAGVERUS - Text 8 (34.8%) 22 (95.7%) 8 (34.8%) 111 (79.9%) Baseline 33 (23.7%) 25 (18.0%) All RagVerus - Code 87 (62.6%) 134 (96.4%) 84 (60.4%) 76 (54.7%) RagVerus - Text  $81\ (58.3\%)$ 127 (91.4%)

<span id="page-8-0"></span>**Table 1:** Evaluation results for VerusBench (MBPP, Diffy, Misc, and All tasks) with percentages based on total number of tasks in each category.

### 5.2 Evaluation on RepoVBench

Although we still examine proof completion on a per-function basis, repository-level verification becomes more challenging due to the need for coordinated reasoning across interdependent modules.

We run ablated trials of RAGVERUS on the new RepoVBench for proof-completion; specific model parameters are listed in Appendix B. We compare to two baselines, the direct-generation as well as the refinement pipelines from AUTOVERUS; we then augment each pipeline with our aforementioned retrieval module with code index. Resulting pass rates are shown in Table 2, reflecting a remarkable improvement on every setting augmented by context retrieval.

| Task            | Model                                                                             | Correct (n, %)                                                        | Safe (n, %)                                                          | Success (n, %)                                                        |
|-----------------|-----------------------------------------------------------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------|
| Simple 52 tasks | DirectGen greedy DirectGen sample Refinement (AUTOVERUS) DirectRAG Refinement+RAG | 2 (3.8%)<br>4 (7.7%)<br>8 (15.4%)<br>21 (40.4%)<br><b>24 (46.2</b> %) | 52 (100.0%)<br>48 (92.3%)<br>49 (94.2%)<br>52 (100.0%)<br>45 (86.5%) | 2 (3.8%)<br>4 (7.7%)<br>7 (13.5%)<br>21 (40.4%)<br><b>23 (44.2%</b> ) |
|                 | Refinement (AUTOVERUS) DirectRAG Refinement+RAG                                   | 63 (16.4%)<br>78 (20.4%)<br><b>84 (21.9%)</b>                         | <b>294 (76.8%)</b> 281 (73.4%) 266 (69.5%)                           | 59 (15.4%)<br>65 (17.0%)<br><b>75 (19.6%)</b>                         |

<span id="page-8-1"></span>**Table 2:** Evaluation results on RepoVBench (VeriSMo-Simple+Complex).

We note that even in the Complex setting, it is still a simplification over real-world verification challenges, as we assume that proof annotations are only erased for one function at a time. Nevertheless, we observe that information retrieved from the same repository provides constructive in-distribution examples to complete successful proofs, especially in the Simple category. Yet, over 55% Simple tasks are not solved by either model.

We argue that RepoVBench-Complex is still a very challenging task; over the actual 331 hard cases, the combination Refinement+RAG (75-23=52) only solves less than 16% of verification tasks, suggesting further innovations in both retrieval methods and generative agents would be necessary. For interested readers, qualitative analysis of the proof generation is discussed in Appendix [C.](#page-13-1)

# 6 Related Work

Automated program verification with LLM. While there exist various techniques for automated program verification with machine learning based methods like Code2Inv [\[25\]](#page-11-13), CIDER [\[19\]](#page-11-14) and Code2RelInv [\[28\]](#page-11-15), there has been recent advancements focusing on the integration of LLMs to enhance proof generation capabilities [\[29\]](#page-11-2). LLMs provide the potential to automate these processes by generating human-like proofs [\[29\]](#page-11-2) and code [\[16\]](#page-10-13). LLM-aided proof/code generation has been studied within verification-aware programming languages like Frama-C [\[9\]](#page-10-14), Dafny [\[13\]](#page-10-15) and Verus [\[12\]](#page-10-7). Recent work AutoVerus [\[30\]](#page-11-3) leverages LLMs for automated proof synthesis in Rust using finetuned knowledge bases and refinement processes. Clover [\[26\]](#page-11-4) addresses the case of SV where no specification is formally given, and attempts to autoformalize a specification in Dafny by aligning with the available implementations and documentations. LeanDojo [\[31\]](#page-11-5) introduces a large premise pool in Lean and uses fine-tuned retrieval models to perform RAG for proofs. Although these approaches differ in methodology and application areas, they all focus primarily on single-function verification.

Repository-level program verification. Repository-level program verification is a relatively emerging field with limited previous research addressing the inherent complexity of large software systems. Selene [\[32\]](#page-11-1) represents a pioneering effort in this domain, but the language focus, verification tooling, and dependency management approaches are different from RagVerus. While there has been recent development in repository-level LLM-based code generation [\[18\]](#page-11-16), RagVerus extends this domain into automated verification, ensuring not only the generation of code but also its formal correctness.

# 7 Conclusion and Future Work

RagVerus addresses repository-level verification via retrieval-augmented generation and context-aware prompting, enabling LLMs to synthesize proofs informed by cross-module dependencies and project-wide examples. Supporting this effort, RepoVBench provides the first repository-level benchmark for Verus, derived from real-world systems to reflect compositional reasoning challenges, and establishes a configurable playground for evaluating retrieval strategies. Future directions include implementing more fine-grained retrieval methods and expanding the benchmark to diverse repositories, possibly using self-evolved methods on verification code [\[4\]](#page-10-3). By bridging AI-driven synthesis with practical project demands, we hope this work lays a foundation for realistic, community-driven assessments on repository-level program verification tools.

# References

- <span id="page-10-4"></span>1. Aggarwal, P., Parno, B., Welleck, S.: Alphaverus: Bootstrapping formally verified code generation through self-improving translation and treefinement. arXiv preprint arXiv:2412.06176 (2024)
- <span id="page-10-12"></span>2. Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J.D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., et al.: Language models are few-shot learners. Advances in neural information processing systems 33, 1877–1901 (2020)
- <span id="page-10-5"></span>3. Chakraborty, S., Ebner, G., Bhat, S., Fakhoury, S., Fatima, S., Lahiri, S., Swamy, N.: Towards neural synthesis for smt-assisted proof-oriented programming. arXiv preprint arXiv:2405.01787 (2024)
- <span id="page-10-3"></span>4. Chen, T., Lu, S., Lu, S., Gong, Y., Yang, C., Li, X., Misu, M.R.H., Yu, H., Duan, N., Cheng, P., et al.: Automated proof generation for rust code via self-evolution. arXiv preprint arXiv:2410.15756 (2024)
- <span id="page-10-8"></span>5. Cho, C., Zhou, Y., Bosamiya, J., Parno, B.: A framework for debugging automated program verification proofs via proof actions. In: International Conference on Computer Aided Verification. pp. 348–361. Springer (2024)
- <span id="page-10-9"></span>6. De Moura, L., Bjørner, N.: Z3: An efficient smt solver. In: International conference on Tools and Algorithms for the Construction and Analysis of Systems. pp. 337–340. Springer (2008)
- <span id="page-10-11"></span>7. Johnson, J., Douze, M., Jégou, H.: Billion-scale similarity search with gpus. IEEE Transactions on Big Data 7(3), 535–547 (2019)
- <span id="page-10-2"></span>8. Kamath, A., Senthilnathan, A., Chakraborty, S., Deligiannis, P., Lahiri, S.K., Lal, A., Rastogi, A., Roy, S., Sharma, R.: Finding inductive loop invariants using large language models. arXiv preprint arXiv:2311.07948 (2023)
- <span id="page-10-14"></span>9. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.: Frama-c: A software analysis perspective. Formal aspects of computing 27(3), 573–609 (2015)
- <span id="page-10-6"></span>10. Klein, G., Andronick, J., Elphinstone, K., Murray, T., Sewell, T., Kolanski, R., Heiser, G.: Comprehensive formal verification of an os microkernel. ACM Transactions on Computer Systems (TOCS) 32(1), 1–70 (2014)
- <span id="page-10-0"></span>11. Lattuada, A., Hance, T., Bosamiya, J., Brun, M., Cho, C., LeBlanc, H., Srinivasan, P., Achermann, R., Chajed, T., Hawblitzel, C., et al.: Verus: A practical foundation for systems verification. In: Proceedings of the ACM SIGOPS 30th Symposium on Operating Systems Principles. pp. 438–454 (2024)
- <span id="page-10-7"></span>12. Lattuada, A., Hance, T., Cho, C., Brun, M., Subasinghe, I., Zhou, Y., Howell, J., Parno, B., Hawblitzel, C.: Verus: Verifying rust programs using linear ghost types. Proceedings of the ACM on Programming Languages 7(OOPSLA1), 286–315 (2023)
- <span id="page-10-15"></span>13. Leino, K.R.M.: Dafny: An automatic program verifier for functional correctness. In: International conference on logic for programming artificial intelligence and reasoning. pp. 348–370. Springer (2010)
- <span id="page-10-10"></span>14. Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.t., Rocktäschel, T., et al.: Retrieval-augmented generation for knowledge-intensive nlp tasks. Advances in Neural Information Processing Systems 33, 9459–9474 (2020)
- <span id="page-10-1"></span>15. Li, X., Li, X., Qiang, W., Gu, R., Nieh, J.: Spoq: Scaling {Machine-Checkable} systems verification in coq. In: 17th USENIX Symposium on Operating Systems Design and Implementation (OSDI 23). pp. 851–869 (2023)
- <span id="page-10-13"></span>16. Li, Y., Parsert, J., Polgreen, E.: Guiding enumerative program synthesis with large language models. In: International Conference on Computer Aided Verification. pp. 280–301. Springer (2024)

- <span id="page-11-0"></span>17. Li, Z., Sun, J., Murphy, L., Su, Q., Li, Z., Zhang, X., Yang, K., Si, X.: A survey on deep learning for theorem proving. arXiv preprint arXiv:2404.09939 (2024)
- <span id="page-11-16"></span>18. Liao, D., Pan, S., Sun, X., Ren, X., Huang, Q., Xing, Z., Jin, H., Li, Q.: A 3-codgen: A repository-level code generation framework for code reuse with local-aware, globalaware, and third-party-library-aware. IEEE Transactions on Software Engineering (2024)
- <span id="page-11-14"></span>19. Liu, J., Chen, Y., Tan, B., Dillig, I., Feng, Y.: Learning contract invariants using reinforcement learning. In: Proceedings of the 37th IEEE/ACM International Conference on Automated Software Engineering. pp. 1–11 (2022)
- <span id="page-11-9"></span>20. LlamaIndex: Llamaindex: Build knowledge assistants over your enterprise data. <https://www.llamaindex.ai/>, accessed: 2024-11-07
- <span id="page-11-7"></span>21. Misu, M.R.H., Lopes, C.V., Ma, I., Noble, J.: Towards ai-assisted synthesis of verified dafny methods. Proceedings of the ACM on Software Engineering 1(FSE), 812–835 (2024)
- <span id="page-11-12"></span>22. OpenAI: Hello GPT-4O (2024), <https://openai.com/index/hello-gpt-4o/>, [Accessed: 2024-11-07]
- <span id="page-11-8"></span>23. OpenAI: New embedding models and api updates (2024), [https://openai.com/](https://openai.com/index/new-embedding-models-and-api-updates/) [index/new-embedding-models-and-api-updates/](https://openai.com/index/new-embedding-models-and-api-updates/), accessed: 2025-01-31
- <span id="page-11-6"></span>24. Shrivastava, D., Larochelle, H., Tarlow, D.: Repository-level prompt generation for large language models of code. In: Proceedings of the 40th International Conference on Machine Learning. ICML'23, JMLR.org (2023)
- <span id="page-11-13"></span>25. Si, X., Naik, A., Dai, H., Naik, M., Song, L.: Code2inv: A deep learning framework for program verification. In: Computer Aided Verification: 32nd International Conference, CAV 2020, Los Angeles, CA, USA, July 21–24, 2020, Proceedings, Part II 32. pp. 151–164. Springer (2020)
- <span id="page-11-4"></span>26. Sun, C., Sheng, Y., Padon, O., Barrett, C.: Clover: Clo sed-loop ver ifiable code generation. In: International Symposium on AI Verification. pp. 134–155. Springer (2024)
- <span id="page-11-11"></span>27. Sun, X., Ma, W., Gu, J.T., Ma, Z., Chajed, T., Howell, J., Lattuada, A., Padon, O., Suresh, L., Szekeres, A., et al.: Anvil: Verifying liveness of cluster management controllers. In: 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24). pp. 649–666 (2024)
- <span id="page-11-15"></span>28. Wang, J., Wang, C.: Learning to synthesize relational invariants. In: Proceedings of the 37th IEEE/ACM International Conference on Automated Software Engineering. pp. 1–12 (2022)
- <span id="page-11-2"></span>29. Wen, C., Cao, J., Su, J., Xu, Z., Qin, S., He, M., Li, H., Cheung, S.C., Tian, C.: Enchanting program specification synthesis by large language models using static analysis and program verification. In: International Conference on Computer Aided Verification. pp. 302–328. Springer (2024)
- <span id="page-11-3"></span>30. Yang, C., Li, X., Misu, M.R.H., Yao, J., Cui, W., Gong, Y., Hawblitzel, C., Lahiri, S., Lorch, J.R., Lu, S., et al.: Autoverus: Automated proof generation for rust code. arXiv preprint arXiv:2409.13082 (2024)
- <span id="page-11-5"></span>31. Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P., Yu, S., Godil, S., Prenger, R.J., Anandkumar, A.: Leandojo: Theorem proving with retrieval-augmented language models. Advances in Neural Information Processing Systems 36 (2024)
- <span id="page-11-1"></span>32. Zhang, L., Lu, S., Duan, N.: Selene: Pioneering automated proof in software verification. arXiv preprint arXiv:2401.07663 (2024)
- <span id="page-11-10"></span>33. Zhou, Z., Chen, W., Gong, S., Hawblitzel, C., Cui, W., et al.: {VeriSMo}: A verified security module for confidential {VMs}. In: 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24). pp. 599–614 (2024)

# Appendix

# <span id="page-12-0"></span>A RepoVBench Data Example

We process code data to generate tasks and to prepare informative contexts, following the methods outlined in Section 4.1.

```
(a)
```

```
(b)
```

Fig. 3: Examples of code masking and metadata extraction using Verus-adapted tools. (a) an example of an original function and its masked counterpart, where proof annotations are replaced with MASKED\_LINE (highlighted in orange); (b) an example of the extracted metadata

# <span id="page-13-0"></span>B RepoVBench Experiment Setup

We maintain a similar LLM budget across experiments when evaluating on the RepoVBench in Section 5.2, so as to ensure a fair comparison between different approaches.

For all methods that require sampling, we set the temperature to t=1.0 for diverse generation results. Except for DirectGen greedy, which is our deterministic baseline, we set t=0 and only sample once.

Direct Generation. For DirectGen-sample and DirectRAG, we set the number of generations to a constant of 3 samples.

Refinement Generation. For Refinement and Refinement+RAG, we generate 2 initial samples and allow a maximum of 2 more repair steps, budgeting under 4 LLM calls.

We note again that the retrieval module used in Section 5.2 searches over VeriSMo contents only, and only uses code embedding information when conducting similarity retrieval.

# <span id="page-13-1"></span>C RepoVBench Qualitative Experiment Results

## Common failure modes in RepoVBench.

VeriSMo contains nested dependencies in proofs and often requires special formats of annotation different from common examples given by the official Verus tutorial.

Especially for models without our RAG assistance, we observe on the Simple dataset that they would produce answers that are logically correct to human, but miss subtle syntax in VeriSMo, such as not using the specially defined integer type for the particular module.

### Key Difficulties Faced in RepoVBench-Complex.

In Table [2,](#page-8-1) as reflected by the success rates between Refinement (59-7=52) and Refinement+RAG (75-23=52) on RepoVBench-Complex, the basic context references provided by the current retrieval method are too simple to provide much assistance in completing the hard verification tasks.

The current experiments fail to handle several situations:

- We observe that many contextually similar tasks in the hard category require different premise sets and proof style, requiring more specialized direction of retrieval
- The ground-truth premise pool is actually larger than the maximum number we return, demanding larger context capacity from the retrieval module
- Some tasks require super long proofs (> 80 proof annotation lines). We suspect any successful run would require hundreds of refinement cycles and compiler feedbacks, in addition to a fully complete premise pool, which is out of our current sampling budget

Generation Style. Since the number of verification success, as a binary metric, does not capture gradual improvement in code generation quality, We evaluate the code similarity with respect to the ground truth proof to reflect how much of the proofs are on the right directions. We analyze the average BLEU scores for selected pipeline settings from Section 5.2, calculated over the entire RepoVBench dataset.

We observe that both retrieval augmented pipelines produce more coherent answers, suggesting that they are utilizing the VeriSMo-specific contexts as expected.

Table 3: BLEU Scores between Method-Generated Answers and the Ground-Truth

| Code Source      | Average BLEU Score |
|------------------|--------------------|
| Unverified Query | 46.76              |
| DirectRAG        | 57.75              |
| Fullpipe Base    | 48.18              |
| Fullpipe RAG     | 55.97              |