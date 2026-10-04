# Towards Repository-Level Program Verification with Large Language Models

#### Si Cheng Zhong

University of Toronto Toronto, Ontario, Canada sicheng.zhong@mail.utoronto.ca

#### Xujie Si University of Toronto Toronto, Ontario, Canada

six@cs.toronto.edu

#### Abstract

Recent advancements in large language models (LLMs) suggest great promises in code and proof generations. However, scaling automated formal verification to real-world projects requires resolving cross-module dependencies and global contexts, which are crucial challenges overlooked by existing LLM-based methods with a special focus on targeting isolated, function-level verification tasks. To systematically explore and address the significant challenges of verifying entire software repositories, we introduce RVBench, the first verification benchmark explicitly designed for repository-level evaluation, constructed from four diverse and complex open-source Verus projects.

We further introduce RAGVERUS, an extensible framework that synergizes retrieval-augmented generation with context-aware prompting to automate proof synthesis for multi-module repositories. RAGVERUS *triples* proof pass rates on existing benchmarks under constrained model inference budgets, and achieves a 27% relative improvement on the more challenging RVBench benchmark, demonstrating a scalable and sample-efficient verification solution.

CCS Concepts: • Computing methodologies  $\rightarrow$  Knowledge representation and reasoning; Information extraction; • Theory of computation  $\rightarrow$  Logic and verification; Automated reasoning.

**Keywords:** Large Language Model, Trustworthy Code Generation

#### **ACM Reference Format:**

Si Cheng Zhong and Xujie Si. 2025. Towards Repository-Level Program Verification with Large Language Models. In *Proceedings of the 1st ACM SIGPLAN International Workshop on Language Models and Programming Languages (LMPL '25), October 12–18, 2025, Singapore, Singapore.* ACM, New York, NY, USA, 13 pages. https://doi.org/10.1145/3759425.3763382

<sup>0</sup>The benchmark and experimental artifact are publicly available at https://github.com/GouQi12138/RVBench

![](_page_0_Picture_12.jpeg)

This work is licensed under a Creative Commons Attribution 4.0 International License.

LMPL '25, Singapore, Singapore
© 2025 Copyright held by the owner/author(s).
ACM ISBN 979-8-4007-2148-9/25/10
https://doi.org/10.1145/3759425.3763382

#### 1 Introduction

High-assurance software, such as operating systems and financial infrastructure, demands rigorous correctness guarantees [21, 37]. Formal verification replaces testing with mathematical proofs that a program adheres to its specifications, offering exhaustive guarantees over all possible executions. Languages designed with verification in mind, such as Verus [16] and Dafny [17], leverage integrated language features and automated constraint solving to facilitate this process. Nevertheless, constructing proofs remains labor-intensive, requiring extensive human expertise to address complex invariants, lemma interactions, and solver constraints [15, 19, 34]. This expertise bottleneck intensifies in large-scale, real-world repositories, where proofs span across multiple interdependent modules, significantly complicating proof construction and premise selection.

Recent advancements in large language models (LLMs) have shown promising potential to alleviate the verification workload by automating proof synthesis [12, 31]. Methods leveraging LLMs iteratively generate candidate proofs, refine them based on compiler feedback, and adapt their training processes accordingly [2, 5, 7, 25, 35]. Despite these advancements, current research predominantly targets isolated, function-level tasks with limited complexity, overlooking the substantial challenges inherent in repository-level verification.

Repository-level program verification introduces unique difficulties due to extensive codebase sizes, intricate crossmodule dependencies, and custom-defined language constructs specific to each project. These complexities require the verifier to effectively navigate a large context, identify relevant lemmas, and adhere strictly to project-specific conventions—tasks that challenge both human verifiers and automated LLM-based systems.

To systematically evaluate and address these challenges, we introduce RVBench, the first benchmark specifically designed for repository-level verification tasks. RVBench is curated from four diverse and award-winning open-source Verus projects [4, 10, 32, 38], reflecting real-world verification challenges, including complex proof structures, intermodule lemma dependencies, and custom type definitions. This benchmark consists of 755 proof completion tasks across 337 modules and 3,464 functions, significantly scaling the

complexity compared to existing function-level benchmarks (i.e., 150 functions used in VerusBench [35]).

We further propose RAGVERUS, a simple retrieval-based framework tailored for repository-scale verification, which dynamically integrates contextually relevant examples and dependencies from extensive codebases into the LLM's reasoning process. Although retrieval-augmented generation (RAG) methods are well-established in natural language processing (NLP) and machine learning literature [13, 18], RAGVERUS'S distinct contribution lies in applying and evaluating these methods explicitly for the nuanced demands of repository-level verification tasks.

Experimental evaluations demonstrate that RAGVERUS significantly outperforms prior frameworks like AUTOVERUS [35] on both function-level and, more importantly, repository-level tasks. Our results highlight the critical role of hybrid retrieval strategies in navigating repository complexities, marking a substantial step towards scalable, automated verification methods.

In summary, this paper makes the following contributions:

- We introduce RVBench, the first benchmark for systematically evaluating repository-level verification in Verus, addressing a crucial gap in existing verification research.
- We propose RAGVERUS, a retrieval-based verification framework that leverages structured repository metadata to enhance LLM-driven proof synthesis.
- We conduct thorough experimental evaluations illustrating the advantages and current limitations of retrieval-based approaches to repository-level verification, thus setting a strong baseline for future improvements.

#### 2 Background

#### 2.1 The Verus Verifier

Verus [16] is a *verification-aware language* and SMT-based verification tool designed as an extension to Rust, an imperative programming language. It integrates Rust's strong ownership and type systems with formal methods, enabling developers to enforce logical correctness alongside memory safety. Verus introduces a domain-specific language (DSL) for embedding *specification*, *proof annotations*, and *executable code* inline, clearly delineating these three distinct code modes (an illustrative example is shown in Figure 1):

- 1. spec mode: Defines preconditions, postconditions, and logical requirements
  - e.g., requires x > 0, ensures result > 0.
- proof mode: Provides proof annotations, assertions, loop invariants, and lemma proofs necessary for bridging specifications to implementations
  - e.g., assert\_by(x > 0,  $\{...\}$ ), invariants i < N.
- 3. exec mode: Contains standard executable Rust code, compiled and executed normally, but checked against specifications at compile time.

The specifications and proofs defined in Verus are ghost annotations, erased at runtime but essential for static verification. This structured separation ensures clarity between functional logic and runtime behavior, aiding automated verification.

```
1 // Returns the greatest_lower_bound as evidence for the
       proof of correctness for the set data structure
2 fn get(&self, k: &K) -> (res: (ID, Ghost<KeyIterator<K>>)
      )
     requires
        self.valid(),
     ensures ({
        let (id, glb) = res;
        &&& id@ == self@[*k]
        &&& self.lows.greatest_lower_bound_spec(KeyIterator
             ::new_spec(*k), glb@)
        &&& id@.valid_physical_address()
10
     }),
11 {
     let ki = KeyIterator::new(k.clone());
12
     let glb = self.lows.greatest_lower_bound(&ki);
14
     proof {
        let glb_k = *glb.get();
        assert(self.lows@.contains_key(glb_k)); // OBSERVE
        let hi = choose |hi| self.lows.gap(glb, hi) && #[
             trigger] KeyIterator::between(glb, ki, hi);
        assert(KeyIterator::between(KeyIterator::new_spec(
             glb_k), ki, hi));
        assert(self.lows@.contains_key(glb_k)
            \&\& \  \  self.lows.gap(KeyIterator::new\_spec(glb\_k),
                 hi)
            && KeyIterator::between(KeyIterator::new_spec(
                 glb_k), KeyIterator::new_spec(*k), hi));
      let id = (*self.lows.get(glb.get()).unwrap()).
           clone_up_to_view();
      (id, Ghost(glb))
25 }
```

**Figure 1.** An annotated Verus function with spec in yellow and proof in orange. Note that each code mode can have *function calls* requiring dependency resolution from other sources.

Verus translates annotated Rust code into satisfiability modulo theories (SMT) formulas, subsequently verified by SMT solvers like Z3 [9]. Proof annotations guide the solver through complex scenarios [8], helping resolve ambiguities and bridging automation gaps during program verification.

#### 2.2 Large Language Models (LLMs) in Verification

Recent advancements in generative AI, particularly large language models (LLMs) such as GPT-4 [27] and Gemini [1], offer promising avenues for automating formal verification processes. These transformer-based architectures, trained on vast corpora of code, documentation, and mathematical texts, possess sophisticated probabilistic representations of syntax, semantics, and logical reasoning patterns.

Effective use of LLMs in verification typically involves strategies such as *chain-of-thought (CoT)* prompting and *retrieval-augmented generation (RAG)*. CoT prompting guides

models to systematically decompose proofs into explicit, logical sub-steps (e.g., "first, assert loop termination; next, apply Lemma identity..."), mimicking human expert reasoning. However, while CoT hints useful reasoning patterns, it does not address complex cross-module dependencies that are common in repository-level tasks.

To address this limitation, RAG methods dynamically retrieve contextually relevant knowledge, such as code snippets, lemma definitions, and project-specific conventions, to enrich the LLM's reasoning context. While early retrievalbased approaches primarily utilized syntactic matching, recent innovations incorporate semantic encoders that capture nuanced code relationships and structural dependencies [\[29,](#page-11-20) [36\]](#page-12-5). By embedding repository-specific metadata and inter-module contexts, these methods significantly enhance LLM accuracy and efficiency in generating verifiable proofs across extensive codebases.

# 3 **RVBench**: Creating A New Repository-level Verification Benchmark

Although existing benchmarks such as VerusBench have been instrumental in evaluating basic proof synthesis for isolated functions, their focus on self-contained tasks involving simple arithmetic reasoning and relevant invariants has led to near saturation [\[35\]](#page-12-3). These benchmarks lack the complexities inherent in real-world software, particularly crossmodule dependencies and environmental interactions. To address this gap, we introduce RVBench, the first repositorylevel benchmark for verification-aware languages, designed to evaluate tools on full-scale codebases mirroring industrial practices.

#### 3.1 Benchmark Construction and Scope

To ensure diverse, real-world challenges reflective of practical verification tasks, RVBench is curated from four prominent open-source Verus projects, each selected for its complexity, domain-specific logic, and inter-module dependencies:

- 1. VeriSMo [\[38\]](#page-12-4): A verified security module for confidential virtual machines (VMs), ensuring memory access safety and confidentiality via permission-based reasoning.
- 2. Anvil [\[32\]](#page-11-13): A framework for verifying Kubernetes controller correctness and liveness, leveraging Verus to enforce state-machine invariants in cloud-native systems.
- 3. IronKV [\[10\]](#page-11-12): A distributed key-value store with proofs for consensus protocols and network fault tolerance.
- 4. Vest [\[4\]](#page-11-11): A formally verified set of high-performance parsers and serializers for binary data formats.

Together, these repositories provide a rich set of 3,464 functions spread across 337 modules, forming a robust testbed for evaluating tools at the repository scale. We specifically

derive 755 proof completion tasks emphasizing cross-module reasoning and project-specific dependencies.

#### 3.2 Benchmark Creation Methodology

We established a rigorous methodology to ensure RVBench accurately captures the complexity of repository-level verification tasks. Specifically, we process Verus repositories into structured datasets through a two-stage pipeline: identifying taskable locations in individual functions, followed by static syntax analysis to build supporting metadata contexts for all functions and constructs.

3.2.1 Task Identification. We build a new line-parse tool leveraging Verus' compiler and code-mode parser to identify formal properties such as function modes, specification conditions, and proof invariants. By precisely controlling over the code mode hierarchy, we enable flexible creation of diverse evaluation tasks. For instance, proof completion tasks are generated by masking proof annotations (e.g., loop invariants, assertions) from verified functions and modules to form task queries.

3.2.2 Metadata Extraction. We extract repository-wide metadata from Rust codebases to index individual functions under the contextualized verification task, informed by context modeling in code generation [\[29\]](#page-11-20). The metadata indexing each function contains: i) the file name, any applicable construct name, and the function name; ii) the function's type signature; iii) method invocations; iv) type identifiers and variable declarations; and v) the function's code mode. Through static analysis over the current file, related parent/child structures, and imported modules, we model a linkage graph that captures control and data flow, revealing necessary premise relationships such as which proof function invokes which spec lemmas. This structured indexing enables precise evaluation of context-aware verification, where an agent must resolve interconnected dependencies and projectspecific semantics in an uninformed situation.

## 3.3 Proof Completion Tasks

We identify functions containing proof annotations from the parsed repositories and form task queries as:

- Input: A proof function or exec function that has complete specification lines (pre/post-conditions) but with all proof lines omitted.
- Expected output: A function together with proof annotations to replace the input, ideally ensuring syntactic and semantic correctness of the problem function.

The generated answer is inserted back into the codebase to compile for verification. We exclude all tasks where Verus can successfully verify even without proof annotations, such as trivial arithmetic properties resolvable by Z3's default tactics.

| Source                                                                           | Type<br>Constructs      | Functions                    | Proof<br>Tasks         | Proof<br>Lines                 | Complex<br>Tasks       |
|----------------------------------------------------------------------------------|-------------------------|------------------------------|------------------------|--------------------------------|------------------------|
| VerusBench[35]                                                                   | -                       | (150)                        | (150)                  | (~1,200)                       | (0)                    |
| VeriSMo                                                                          | 224                     | 1,656                        | 383                    | 7,962                          | 331                    |
| Vest:<br>Vest-core<br>Vest-example                                               | 45<br>35<br>10          | 1,013<br>739<br>274          | 214<br>179<br>35       | 1,227<br>1,055<br>172          | 198<br>164<br>34       |
| IronKV                                                                           | 34                      | 528                          | 129                    | 2,377                          | 117                    |
| Anvil (executable): Anvil-fluent Anvil-rabbitmq Anvil-replicaset Anvil-zookeeper | 34<br>9<br>14<br>2<br>9 | 267<br>64<br>112<br>17<br>74 | 29<br>7<br>9<br>5<br>8 | 479<br>106<br>175<br>106<br>92 | 27<br>6<br>9<br>4<br>8 |
| RVBench Total                                                                    | 337                     | 3,464                        | 755                    | 12,045                         | 673                    |

<span id="page-3-0"></span>Table 1. RVBench Composition across Four Verus Projects and Comparison with VerusBench

Table 1 summarizes important statistics of VerusBench (second row), verification tasks used in the previous work [35], and the newly constructed RVBench (third to seventh row), which consists of four Verus projects. Taking the VeriSMo project as an example, we extracted **224** project-specific type constructs and 2,073 code pieces, including macro definitions and functions, and parsed **1,656** indexable functions, out of which we identified 460 functions containing proof lines in the original code using the syntax tracer. We further filtered out functions that the Verus compiler can automatically solve even without proof code, which resulted in **383** tasks for the benchmark, consisting of **7,962** lines of proof in total.

Furthermore, we carefully analyze the ground-truth proofs and split the benchmark into two categories based on whether the proofs require premises (aka proof function dependencies):

- **Simple tasks**: Isolated functions whose proofs require project-specific macros and type definitions but no function calls. All tasks of VerusBench fall in this category.
- Complex tasks: Functions whose proofs require complicated premises, i.e., dependencies of other proof functions.

Simple tasks test contextual understanding of project-specific syntax (e.g., custom defined macros, types and constructs). For instance, a function may use a custom integer type (SecureInt) defined in a project header; understanding this type is essential for proof syntax, even if no premises are invovled. Complex tasks evaluate premise retrieval and integration (i.e., resolving inter-module proof functions). This categorization isolates distinct repository-level challenges, where RVBench differentiates localized syntax adaptation and systemic dependency resolution to provide a granular framework for diagnosing agent limitations.

<span id="page-3-1"></span>**Table 2.** Logic and Problem Characteristics of Proof-Completion Tasks: **LL**-Linear Logic, **SL**-Separation Logic, **TL**-Temporal Logic, **Cc**.-Concurrency, **Qt**.-Quantifiers

| Source             | LL       | SL       | TL | Cc.      | Qt.      |
|--------------------|----------|----------|----|----------|----------|
| RVBench Sources    |          |          |    |          |          |
| VeriSMo            | <b>✓</b> | <b>✓</b> | ×  | ✓        | <b>√</b> |
| IronKV             | ×        | ×        | ✓  | <b>√</b> | <b>√</b> |
| Anvil              | ×        | ×        | ✓  | ✓        | <b>√</b> |
| Vest               | ✓        | ×        | ×  | ×        | <b>√</b> |
| Previous Benchmark |          |          |    |          |          |
| VerusBench         | ×        | ×        | ×  | ×        | <b>✓</b> |

RVBench also introduces a significant increase in the logical reasoning complexity required for proof writing as highlighted in Table 2. For instance, verifying memory access confidentiality in VeriSMo necessitates reasoning with linear logic to track resource consumption and separation logic to handle disjoint memory. IronKV and Anvil's distributed consensus and fault tolerance aspects require temporal and concurrency reasoning, utilizing quantifiers [32]. Unlike VerusBench's isolated context, RVBench demands reasoning about modularity, resources, temporal evolution, and concurrency, reflecting real-world verification challenges.

#### 3.4 Evaluation Metrics

RVBench employs the following metrics and infrastructure to evaluate proof completion quality:

- **Correct**: The code is correct if the generated proof annotations pass Verus compilation, which verifies logical soundness across the entire project, validating the required specifications and any propagated constraints.
- **Intact**: The generated result is intact if the executable code and specifications remain unaltered, preserving

<span id="page-4-0"></span>![](_page_4_Figure_2.jpeg)

Figure 2. The RagVerus pipeline consists of three stages: 1) mining code properties, 2) retrieving task-specific information, and 3) generating proofs for verifiable code

the original functionality for verification. We check this by the Lynette syntax checker [\[35\]](#page-12-3), which validates code consistency for all exec and spec lines (e.g., no injected ensures or modified variable types). This metric is important because LLMs could simply overwrite the executable code and/or specifications, making generated proofs irrelevant regardless being correct or not.

• Success: The aggregated success metric requires a result to be both correct and intact. For example, a memory allocator proof that compiles (correct) but inadvertently modifies a pointer type (contaminated) is deemed a failure.

As verification success is a rigid binary metric, we also introduce a relaxed metric, which compares the generated code and proofs to the ground-truth reference using the BLEU score (Bilingual Evaluation Understudy) widely used in NLP tasks, measuring textual similarity between the two, to assess alignment with expected coding standards and term usages, thus signaling gradual improvement in proof generation.

## 4 RagVerus Framework

To effectively address the complexities inherent in repositorylevel verification, we introduce RagVerus, a retrieval-augmented generation (RAG) framework explicitly designed to leverage large language models (LLMs) for program verification at scale. As illustrated in Figure [2,](#page-4-0) RagVerus consists of three modules — repository indexing module, retrieval module, and proof generation module. Given that the proof generation module largely follows the design of the previous work [\[35\]](#page-12-3), we will primarily illustrate the first two modules.

#### 4.1 Repository Indexing

We prepare persistent indices for efficient retrieval of all contents within a verification task repository. This involves preprocessing: 1) code for all functions, and 2) natural language summaries derived from function metadata.

Code Indexing. For efficient retrieval of relevant verification contexts, we use persistent vector stores where code documents are encoded into high-dimensional embeddings using OpenAI's text-embedding-3-large model [\[28\]](#page-11-21), and are then retrieved via FAISS [\[11\]](#page-11-22), a fast indexing library. This approach allows us to capture the syntax and structures of code snippets, going beyond simple keyword matching.

Metadata Indexing. While statically extracted formal metadata provides a structured view of the existing codebase, it is unable to recover the missing premises of an unverified task function. Moreover, the high-level intent or semantic relationships between code elements are not always explicitly captured by static analysis.

To find the most relevant dependencies, we further informalize code and associated metadata into natural language descriptions (see Appendix [B](#page-9-0) for more details) and then index natural language descriptions. This informal natural language summary captures code behavior beyond syntax and allows us to retrieve functionally dependent examples, ensuring the verification process is guided by relevant context that aligns with the task's high-level intent.

To prevent potential data leakage, both indexing systems exclude the target function's own verified context (if present) during retrieval, ensuring proofs are synthesized solely from external dependencies for the unverified function.

#### 4.2 Retrieving Useful Contexts for Repository-level Verification

RagVerus employs two complementary retrieval strategies to enhance proof synthesis: 1) few-shot example retrieval, and 2) dependency retrieval. Retrieved contexts are integrated into the prompts to guide LLMs in generating verifiable code, balancing structural patterns (via examples) and logical prerequisites (via dependencies). The framework's modular design supports customized retrieval models to tailor specific verification challenges.

4.2.1 Few-Shot Example Retrieval. To guide LLMs to adhere to correct styles and practices, RagVerus uses fewshot retrieval to select representative problem-approach pairs from other verified examples. Using the tasked code or its informalized metadata as query, we retrieve syntactically or semantically similar, proof-masked functions paired with their verified counterparts, forming reference solution pairs.

To cover diverse proof styles, we source from multiple indices, including tutorial examples from the official Verus repository, tasks from VerusBench and RVBench, among many others. After ranking the retrieved candidates, we retain a maximum of three diverse and relevant examples per task query. These examples provide the LLM with contextual references for the proof-completion task [\[3\]](#page-11-23), improving verification quality and precision.

4.2.2 Dependency Retrieval. Dependency retrieval in RagVerus identifies cross-module function signatures, premises, and type definitions necessary to inform proof synthesis in large codebases while adhering to LLM context windows. This process addresses two critical needs:

- 1. Context Awareness: Integrates project-specific constructs, type definitions, and code conventions to ground proofs in repository-wide patterns and knowledge.
- 2. Premise Retrieval: Identifies premises, i.e., functions in spec or proof modes, that are potentially useful during the verification of the target task.

Well-chosen dependency hints resolve logical gaps in verification conditions while filtering noise, providing contexts on module interactions within the repository. Identifying a formatted list of verified dependent functions and constructs creates an essential toolkit for the LLM to elaborate on, streamlining the generation process and encouraging function reuse.

We evaluate a simple embedding-based approach using informalized metadata similarity to capture context and dependency relationships with the tasked function, covering both the related definitions and the dependent premises.

#### 4.3 Proof Generation

In RagVerus, proof generation involves synthesizing verification annotations such as loop invariants, quantifier logic, and termination conditions to link spec and exec modes explicitly. Given a partially annotated task function, the LLM generates complete, executable Verus annotations informed by the retrieved contexts. Generated proofs are rigorously validated using:

- Verus Compiler: Ensures logical correctness and compliance with the repository-wide specifications.
- Lynette Syntax Checker: Validates intactness, ensuring no unintended modifications occur in the executable or specification code.

If a proof fails initial validation, RagVerus optionally supports iterative refinement cycles, leveraging feedback from the verifier to iteratively enhance proof correctness.

## 5 Evaluation

We conducted comprehensive evaluations of RagVerus to rigorously assess its effectiveness in handling both functionlevel and repository-level verification tasks. These evaluations demonstrate the practical benefits as well as highlight the current limitations of retrieval-augmented verification.

#### 5.1 Baseline Methods & Setup

Direct Proof Generation. By leveraging LLMs' flexibility in code manipulation and by prompting the model with static Verus knowledge and expert-tuned instructions, we sample independent proof candidates that adhere to Verus' strict verification syntax. Given a single unverified Verus function, the LLM rewrites the entire file to insert complete proofs directly within the code using Verus' DSL, encompassing invariants, assertions, and standard lemma calls.

Ensemble Refinement. We improve the generated proof candidates by iteratively refining and repairing the verification annotations base on three approaches inAutoVerus[\[35\]](#page-12-3):

- Candidate Merging: Identifies and merges sound proofs from multiple candidate variants.
- Refine Templates: Applies rule-based corrections (e.g., fixing type mismatches in ghost code, changing regular u64 to ghost integer).
- Adaptive Repair: Instructs LLM repairs with elicited guiding examples for each kind of failure case (e.g., lacking invariants, syntax mismatches).

AutoVerus using refinement, achieved near-perfect automation on function-level tasks - 91% pass rate on VerusBench[\[35\]](#page-12-3).

#### 5.2 Retrieval-Augmented Methods

We augment upon the two baselines by incorporating two retrieval strategies: 1) few-shot retrieval and 2) dependency retrieval, to evaluate the effectiveness of RagVerus.

To ensure a fair comparison, we maintain an equal length of prompt instructions across all methods for the same task. The baselines are prompted with generic static examples, and RAG methods have dynamic examples. RAG methods only gain a potential advantage in context length when dependency retrieval is performed, up to 1000 more tokens.

We chose GPT-4o (version 2024-08-06) [\[27\]](#page-11-18), the most wellrounded model offered by OpenAI at the time of experiment as our model of choice for all baselines and augmented methods. The temperature was set to 1.0 for all sampling processes.

#### 5.3 Evaluation on Function-Level Verification Tasks

VerusBench comprises 150 function-level proof-completion tasks, demanding arithmetic reasoning and relevant invariants. We tested 139 available tasks from three sources<sup>1</sup>: Diffy [6], MBPP [26], and Verus tutorials.

Since VerusBench does not have dependencies to consider, we evaluated the isolated impact of adaptive few-shot retrieval. As the full refinement pipeline saturates this benchmark, we evaluated based on the direct generation pipeline, with and without retrieval augmentation. Our retrieval pool consisted of indexed files from VerusBench itself, official Verus tutorials, and example files used in AutoVerus' refinement phase. We limited sampling to five attempts per task to assess the benefits of different retrieval strategies within a constrained budget. Table 3 presents the performance comparison, where RAG-Code and RAG-Text denote retrieval based on code similarity and informalized-summary similarity, respectively.

<span id="page-6-1"></span>**Table 3.** Evaluation results on VerusBench with percentages based on total number of tasks in each category.

| Task        | Method    | Correct(n,%) | Intact(n,%) | Success(n,%) |
|-------------|-----------|--------------|-------------|--------------|
|             | DirectGen | 23 (29.5%)   | 60 (76.9%)  | 17 (21.8%)   |
| <b>MBPP</b> | RAG-Code  | 57 (73.1%)   | 74 (94.9%)  | 54 (69.2%)   |
|             | RAG-Text  | 49 (62.8%)   | 68 (87.2%)  | 45 (57.7%)   |
|             | DirectGen | 3 (7.9%)     | 30 (78.9%)  | 2 (5.3%)     |
| Diffy       | RAG-Code  | 19 (50.0%)   | 38 (100.0%) | 19 (50.0%)   |
|             | RAG-Text  | 24 (63.2%)   | 37 (97.4%)  | 23 (60.5%)   |
|             | DirectGen | 7 (30.4%)    | 21 (91.3%)  | 6 (26.1%)    |
| Tutorial    | RAG-Code  | 11 (47.8%)   | 22 (95.7%)  | 11 (47.8%)   |
|             | RAG-Text  | 8 (34.8%)    | 22 (95.7%)  | 8 (34.8%)    |
|             | DirectGen | 33 (23.7%)   | 111 (79.9%) | 25 (18.0%)   |
| Total       | RAG-Code  | 87 (62.6%)   | 134 (96.4%) | 84 (60.4%)   |
|             | RAG-Text  | 81 (58.3%)   | 127 (91.4%) | 76 (54.7%)   |

RAG-Code consistently achieved higher performance across all metrics, particularly excelling on MBPP. Retrieval using informalized summaries also significantly improved upon the baseline, notably outperforming code-based retrieval in Diffy (23 vs. 19). Notably, our RAG results with limited sampling (5 attempts) already outperformed the same baseline reported in the AUTOVERUS paper (44.7% success rate using up to 125 invocations), highlighting the value of task-specific context over fixed guidance.

While code-based retrieval captures structural similarity, informalized-summary retrieval aligns semantic meaning, showing an advantage on Diffy (array manipulation tasks within VerusBench). In cases where code structures can be

similar but verification targets are different, semantic differences in proof requirements make informalized summaries more effective for tasks like those in Diffy, where code index might overfit on syntax (e.g., condm.rs and ms1.rs have exactly the same sequential loop structures but require different logic reasoning—modulus operation vs. sum checking; refer to Appendix A for a detailed code comparison).

#### 5.4 Evaluation on RVBench

For repository-level verification, a preliminary run of the uninformed direct generation method on the VeriSMo subset (first two rows in Table 4) shows its inability even under the simple tasks. We therefore focus on the performance when retrieval or refinement are incorporated. Our experiments on RVBench added the entire benchmark's corpus as the retrieval pool for few-shot examples, whereas dependency retrieval was only scoped to the tasked repository for contextual type constructs and premise lemmas. We employed code similarity for few-shot retrieval and metadata matching for dependency retrieval.

We maintained a comparable LLM budget across all experiments to ensure a fair comparison of different approaches:

**Direct Generation**. We evaluated direct proof generation (DirectGen) with the addition of RAG for few-shot examples and dependencies (DirectRAG). We generated three samples per task by default. In a greedy decoding setting, we set the LLM temperature to zero and generate only once.

**Refinement Generation**. We establish a stronger baseline by incorporating the refinement process, both with (RAG+Refinement) and without (Refinement) retrieval augmentation. These methods generated two initial samples and allowed up to two subsequent repair steps, totaling a maximum of four LLM calls.

**5.4.1 Verification Results.** Repository-level verification introduces added complexity in coordinated reasoning across interdependent modules, even though our evaluation assesses proof completion per function. We note that the Complex task setting still represents a simplification of real-world repository verification, as we focus on proving one function at a time while assuming other functions and premises are already verified. Despite this simplification, retrieval of indistribution examples from the repository proved beneficial for successful proof completion.

The results in Table 4 demonstrate a clear performance improvement across all evaluated methods when augmented with contextualized retrieval. Yet, over 55% of Simple tasks remained unsolved by all models, and the RVBench-Complex subset presents a more significant challenge. For instance, within the 331 Complex tasks in RVBench-VeriSMo, RAG+Refinement achieved a success rate of under 16% (52 tasks), only on par with the non-RAG Refinement baseline (52 tasks). This highlights the need for further advancements

<span id="page-6-0"></span><sup>&</sup>lt;sup>1</sup>AutoVerus was also tested on one unpublished Verus-CloverBench [31]

<span id="page-7-0"></span>

| Task Method     |                  | Correct (n, %) |            | Intact (n, %) |             | Success (n, %) |            |
|-----------------|------------------|----------------|------------|---------------|-------------|----------------|------------|
|                 |                  | Overall        | Simple     | Overall       | Simple      | Overall        | Simple     |
| Verismo         |                  |                |            |               |             |                |            |
| 383 tasks       | DirectGen greedy | N/A            | 2 (3.8%)   | N/A           | 52 (100.0%) | N/A            | 2 (3.8%)   |
| 52 simple tasks | DirectGen sample | N/A            | 4 (7.7%)   | N/A           | 48 (92.3%)  | N/A            | 4 (7.7%)   |
| •               | Refinement       | 63 (16.4%)     | 8 (15.4%)  | 294 (76.8%)   | 49 (94.2%)  | 59 (15.4%)     | 7 (13.5%)  |
|                 | DirectRAG        | 78 (20.4%)     | 21 (40.4%) | 281 (73.4%)   | 52 (100.0%) | 65 (17.0%)     | 21 (40.4%) |
|                 | RAG+Refinement   | 84 (21.9%)     | 24 (46.2%) | 266 (69.5%)   | 45 (86.5%)  | 75 (19.6%)     | 23 (44.2%) |
| Ironkv          |                  |                |            |               |             |                |            |
| 129 tasks       | Refinement       | 22 (17.1%)     | 4 (33.3%)  | 98 (76.0%)    | 11 (91.7%)  | 21 (16.3%)     | 4 (33.3%)  |
| 12 simple tasks | DirectRAG        | 18 (14.0%)     | 2 (16.7%)  | 104 (80.6%)   | 10 (83.3%)  | 18 (14.0%)     | 2 (16.7%)  |
| •               | RAG+refinement   | 31 (24.0%)     | 4 (33.3%)  | 96 (74.4%)    | 10 (83.3%)  | 27 (20.9%)     | 4 (33.3%)  |
| Vest            |                  |                |            |               |             |                |            |
| Vest-core       | Refinement       | 17 (9.5%)      | 4 (26.7%)  | 157 (87.7%)   | 14 (93.3%)  | 11 (6.15%)     | 4 (26.7%)  |
| 179 tasks       | DirectRAG        | 23 (12.8%)     | 5 (33.3%)  | 152 (84.9%)   | 15 (100.0%) | 19 (10.6%)     | 5 (33.3%)  |
| 15 simple tasks | RAG+refinement   | 28 (15.6%)     | 5 (33.3%)  | 155 (86.6%)   | 14 (93.3%)  | 24 (13.4%)     | 5 (33.3%)  |
| Vest-exp        | Refinement       | 14 (40.0%)     | 1 (100.0%) | 21 (60.0%)    | 1 (100.0%)  | 14 (40.0%)     | 1 (100.0%) |
| 35 tasks        | DirectRAG        | 9 (25.7%)      | 0 (0.0%)   | 28 (80.0%)    | 1 (100.0%)  | 9 (25.7%)      | 0 (0.0%)   |
| 1 simple task   | RAG+refinement   | 15 (42.9%)     | 1 (100.0%) | 30 (85.7%)    | 1 (100.0%)  | 15 (42.9%)     | 1 (100.0%) |
| Anvil           |                  |                |            |               |             |                |            |
| 29 tasks        | Refinement       | 9 (30.0%)      | 1 (50.0%)  | 17 (56.7%)    | 2 (100.0%)  | 6 (20.0%)      | 1 (50.0%)  |
| 2 simple tasks  | DirectRAG        | 10 (33.3%)     | 0 (0.0%)   | 17 (56.7%)    | 2 (100.0%)  | 8 (26.7%)      | 0 (0.0%)   |
| -               | RAG+refinement   | 15 (50.0%)     | 1 (50.0%)  | 19 (63.3%)    | 2 (100.0%)  | 12 (40.0%)     | 1 (50.0%)  |

**Table 4.** Evaluation results on RVBench program verification tasks.

in both retrieval strategies and the capabilities of generative agents to tackle the complexities of repository-scale verification.

- **5.4.2 Ablation Study on Retrieval Strategies.** We conducted an ablation study on the IronKV subset of RVBench to understand the contribution of different retrieval context sources. IronKV, derived from the well-established IronFleet distributed system [10], provides a challenging yet manageable repository for this analysis. Our established baseline is the RAG+refinement approach, which employs a hybrid retrieval strategy: global code similarity for few-shot examples and local informalized summary similarity for dependency retrieval. The ablations are compared in Table 5.
- 1) Random Retrieval. When all contexts were randomly retrieved, performance dropped across all metrics (*Correct*, *Intact*, *Success*). This starkly highlights the crucial role of intelligent retrieval in providing pertinent information from the vast repository to the LLM. Randomly selected code snippets and function signatures not only fail to offer the necessary structural or semantic guidance, but also mislead the model, shown by a success rate lower than Refinement-only.
- 2) Index Types (Code Only vs. Metadata Only). When only use code similarity or summary similarity for both fewshot retrieval and dependency retrieval.

<span id="page-7-1"></span>**Table 5.** Ablation study results on Verified IronKV (Total tasks: 129).

| Ablation Config. | Method                     | Correct (n, %) | Intact<br>(n, %)         | Success (n, %) |
|------------------|----------------------------|----------------|--------------------------|----------------|
| Baselines        | RAG+refine<br>Refinement   |                |                          |                |
| Retrieval        | Random                     | 20 (15.5%)     | 100 (77.5%)              | 18 (14.0%)     |
| Indexing         | Code Only<br>Metadata Only |                | 96 (74.4%)<br>97 (75.2%) |                |
| RAG Scope        | Local Only                 | 19 (14.7%)     | 100 (77.5%)              | 16 (12.4%)     |
| Dependenc        | y GT Premise               | 23 (17.8%)     | 97 (75.2%)               | 22 (17.1%)     |

- Code Only: Showed a slight decrease in *Correct* rates but a marginal increase in *Success*. While it leveraged structural similarity to inform correct proof practices, raw code lacked context linkages needed for dependencies.
- Metadata Only: Yielded slightly better performance, indicating the strong utility of semantic similarity for both examples and contextual information. Metadata summaries captured high-level intents for semantically nuanced tasks, aligning with findings from functionlevel benchmarks.

- 3) Local-only Source. Limiting retrievals to only the tasked repository led to a substantial drop in all performance metrics. A diverse, global set of examples is essential for LLMs to learn generalizable syntax patterns and avoid overfitting on specific project conventions, which could limit their ability to leverage broader verification knowledge and successful proof strategies.
- 4) Ground Truth Premise. Solely providing ground-truth premise (function signature) lists for dependency retrieval decreased performance, indicating that LLMs require broader contextual information beyond isolated function signatures to effectively utilize dependencies. Our summary-based retrieval offered a holistic context, including usage, related type definitions, and implicit semantic relationships, which is crucial for the LLM to understand and apply the retrieved information.

In conclusion, effective repository verification with LLMs hinges on intelligent retrieval that covers a broad set of diverse examples and logical contexts. These elements collectively provide the necessary structural and semantic guidance for the LLM to navigate the complexities of repositorylevel reasoning.

## 5.5 Qualitative Analysis of **RVBench** Results

## 5.5.1 Common failure modes in **RVBench**.

RVBench tasks expose two key failure modes in non-RAGassisted models:

- 1. Customized Proof Dependencies: Proofs often require coordinating invariants and using non-standard proof functions, which is not a convention present in common Verus tutorials.
- 2. Project-Specific Syntax Mismatches: Even logically sound proofs fail due to subtle syntax deviations. Verus requires integer reasoning be performed using a ghost Integer type; non-RAG models frequently default to Rust's native i32, causing verification failures despite correct logic.

## 5.5.2 Key difficulties faced in **RVBench**-Complex.

From Table [4,](#page-7-0) as reflected in the success rates between Refinement (59-7=52) and RAG+Refinement (75-23=52) on RVBench-Complex, the basic context references provided by the current retrieval methods are too simple to support much assistance in completing the hard verification tasks that require more dependencies.

The current experiments fail to handle several situations:

- We observe that many contextually similar tasks in the hard category require different premise sets and proof style, requiring more specialized direction of retrieval.
- The ground-truth premise pool is actually larger than the maximum number of retrievals we return, demanding larger context capacity from the retrieval module.

• Some tasks require super long proofs (> 80 proof annotation lines). We suspect any successful run would require hundreds of refinement cycles and compiler feedbacks, in addition to a fully complete premise pool, which is out of our current sampling budget.

#### 5.5.3 Generation Style.

Since the number of verification success, as a binary metric, does not capture gradual improvement in the proof generation quality using LLMs, we evaluate the code similarity with respect to the ground truth proof to reflect how much of the proofs are in the right directions. We analyze the average BLEU scores between the generated code and the ground-truth code for selected pipeline settings.

Table 6. BLEU scores between generated answers and the ground-truth function

| Proof Source        | Average BLEU Score (↑) |
|---------------------|------------------------|
| Code without Proof  | 46.76                  |
| DirectGen Baseline  | 46.32                  |
| Refinement Baseline | 48.18                  |
| DirectRAG           | 57.75                  |
| RAG+Refinement      | 55.97                  |

We observe that both retrieval augmented pipelines produce more coherent answers, suggesting that they are utilizing the project-specific contexts as expected.

## 6 Related Work

Automated program verification with LLM. While there exist various techniques for automated program verification with machine learning based methods like Code2Inv [\[30\]](#page-11-26), CIDER [\[23\]](#page-11-27) and Code2RelInv [\[33\]](#page-12-6), there has been recent advancements focusing on the integration of LLMs to enhance proof generation capabilities [\[34\]](#page-12-2). LLMs provide the potential to automate these processes by generating human-like proofs [\[34\]](#page-12-2) and code [\[20\]](#page-11-28). LLM-aided proof/code generation has been studied within verification-aware programming languages like Frama-C [\[14\]](#page-11-29), Dafny [\[17\]](#page-11-2) and Verus [\[16\]](#page-11-1). Recent work AutoVerus [\[35\]](#page-12-3) leverages LLMs for automated proof synthesis in Rust using finetuned knowledge bases and refinement processes. Clover [\[31\]](#page-11-6) addresses the case of software verification where no specification is formally given, and attempts to autoformalize a specification in Dafny by aligning with the available implementations and documentations. LeanDojo [\[36\]](#page-12-5) introduces a large premise pool in Lean and uses fine-tuned retrieval models to perform RAG for proofs. Although these approaches differ in methodology and application areas, they all focus primarily on singlefunction verification.

Repository-level program verification. Repository-level program verification is a relatively emerging field with limited previous research addressing the inherent complexity of large software systems. Selene [\[37\]](#page-12-1), tailored on verifying the seL4 microkernel using the Isabelle theorem proving language, represents a pioneering effort in this domain, but the language focus, verification tooling, and dependency management approaches are different from RagVerus. While there has been recent development in repository-level LLMbased code generation [\[22\]](#page-11-30), RagVerus extends this domain into automated verification, ensuring formal correctness.

## 7 Future Work

Building upon the RagVerus framework and the RVBench benchmark, future research can focus on enhancing the scalability, precision, and intrinsic capabilities of LLM-driven verification for repository-level tasks. Key directions include:

Scaling Verification Beyond Individual Completions. Current approaches assume dependencies are pre-filled and pre-verified. Future work should extend verification to handle concurrent proof synthesis across multiple interdepen-

dent modules simultaneously. Completing specification, implementation, and verification in a single stack bridges the gap between benchmarks and the real-world codebases.

Specializing Retrieval for Structural and Semantic Dependencies. While RagVerus demonstrates the value of retrieval, significant challenges remain in accurately identifying complex premises and project-specific contexts. More fine-grained retrieval methods could involve finetuning embedding encoders to capture causal relations between callers and callees in code dependencies, moving beyond generic similarity metrics to retrieve essential type definitions, lemmas, and patterns for complex proof construction.

Improving Intrinsic LLM Capabilities for Verification Languages. Verification languages like Verus present unique syntactic and logical challenges for general-purpose LLMs. A promising direction is to enhance the intrinsic capabilities of LLMs in these niche domains. This can be achieved through fine-tuning on verification-specific corpora and leveraging feedback mechanisms from the compiler/verifier for reinforcement learning, enabling models to learn the verification syntax and improving their reasoning on the topic.

## 8 Conclusion

This paper tackles the challenge of scaling formal verification to repository-level by introducing RVBench, the first benchmark specifically designed for repository verification tasks in Verus, and RagVerus, a framework leveraging contextaware prompting to enhance LLM-based proof synthesis. By focusing on repository-level challenges, our work establishes foundational steps towards practical, automated verification suitable for large-scale, real-world software systems.

## Acknowledgements

This work was supported, in part, by Individual Discovery Grant program from the NSERC of Canada and the Canada CIFAR AI Chair Program. This work has also benefitted from the Microsoft Accelerate Foundation Models Research (AFMR) grant program. We thank Jiading Zhu and Yifang Tian for their early exploration on the idea, and Zhiyang Chen for his valuable feedback and revision suggestions.

# Appendix

## A Code Simiarity vs. Semantic Similarity

In VerusBench-Diffy, different problems are hard to differentiate by their code syntax. However, we still need to target individual problems to provide suitable guidance for proof completion. As an example, two functions condm.rs and ms1.rs both have the following serial-loop structure,

```
1 let mut i: usize = 0;
 2 while (i < N as usize) {
 3 ...
 4 i = i + 1;
 5 }
 6 i = 0;
 7 while (i < N as usize) {
 8 if(...) {...}
 9 else { ... }
10 i = i + 1;
11 }
```

making their code look similar at the syntax level. However, their required proofs and invariants are actually different; one deals with element selection, and the other handles numeric summation, thus requiring different reasoning guidance.

Metadata summaries recognize the functional differences and can be used to retrieve related examples effectively. As shown in Figure [3,](#page-10-0) the summaries explicitly identify that condm.rs deals with modulus operation at individual indices, while ms1.rs focuses on summation over the list.

# <span id="page-9-0"></span>B Data Processing during RagVerus

For any tasked repository, we formulate all available contents for retrieval before accepting a problem. We preprocess 1) the code for all functions, 2) metadata linking types and constructs, and 3) informalized semantic summaries.

Mining Code Properties. We process repository-wide code artifacts to extract verification-critical metadata following Section 3.2, building on insights from context modeling in repository-level code generation [\[29\]](#page-11-20).

- Context types: We identify function/type signatures, method calls, type identifiers and field declarations with in the target function
- Type sources: We look for the source definitions of the appearing context types from the current file, parent/child classes, and imports.

```
1 ...
2 ### Functionality Summary :
3 1. ** Loop 1**: Iterates over the vector from index `0`
        to `N-1`, setting each element to `0`.
4 2. ** Loop 2**: Iterates over the vector again from
       index `0` to `N -1`. If `N` is even , it increments
        each element by `2`; if `N` is odd , it
       increments each element by `1`.
5 3. ** Post - condition **: After the second loop , each
       element in `a` will have a value such that `a[k]
       % 2` is equal to `N % 2`.
6
7 ...
8
9 ### Invoked Functions :
11 - `a. set (i, value ) `: This function sets the element at
        index `i` of the vector `a` to `value `. This is
       a method of the `Vec ` type in Rust or a custom
       method provided by the `verus ` library .
```

```
1 ...
2 ### Functionality Summary :
3 - If `i` is 0 , it sets the first element of `sum ` to
          0.
4 - For all other indices , it adds the current element
          of `a` to the first element of `sum `. However ,
          since all elements of `a` are 0 , `sum [0]`
         remains 0.
5 - The function ensures that the first element of `
         sum ` is 0 at the end of execution , which is
         consistent with the specified `ensures `
         condition .
6 ...
8 ### Invoked Functions :
9 - `a. set (i, i % 1) `: This is a method call on the
       vector `a` to set the element at index `i` to `i
       % 1`.
10 - `sum . set (0 , 0) `: This is a method call on the vector
        `sum ` to set the element at index 0 to 0.
11 - `sum . set (0 , sum [0] + a[i]) `: This is a method call
       on the vector `sum ` to update the element at
       index 0 by adding the current element of `a` at
       index `i`.
```

Figure 3. Comparison of metadata summaries for condm.rs (left) and ms1.rs (right), where the informalized summaries explicitly identify the logic differences and the key objects being operated on.

For each function, we collect these contexts across the repository to build a linkage graph by analyzing the control/ dataflow via static analysis of the codebase hierarchy, reflecting module dependencies.

Informalizing Code Summaries. This stage generates natural language descriptions of Rust functions, termed informalized semantic summaries, to supplement the contexts. Using the code implementation and the processed metadata, we produce concise summaries using GPT-4o to encapsulate the function's purpose, behavior, and key properties. For example, a function performing cryptographic hashing can be summarized as: "Computes a SHA-256 hash of input bytes, enforcing non-null pointers and initializing a secure context..." Informalization-based example selection leverages these summaries during retrieval, matching them by semantic similarity to prioritize functionally analogous examples. This ensures retrieved contexts align with the target's verification intent rather than superficial syntax, addressing where syntax and static analysis fails.

![](_page_10_Figure_7.jpeg)

Figure 4. Code informalization summarizes the code functionalities. Here, one can identify through the summaries that is\_locked is a good helper candidate for the task add\_element.

Generating Vectorized Indices. To enable efficient retrieval, RagVerus uses persistent vector stores where documents are encoded into embeddings using OpenAI's textembedding-3-large model [\[28\]](#page-11-21). We encode the Rust code and their informalized summaries separately into high-dimensional embeddings; these embeddings are then indexed via FAISS [\[11\]](#page-11-22) (implemented through LlamaIndex [\[24\]](#page-11-31)), a library optimized for fast similarity search across large corpora. Two distinct indices are created for each kind of context sources:

- Unverified Index: Contains embeddings of unverified code and summaries, aligning with the input queries during proof synthesis.
- Verified Index: Stores fully verified code and their complete semantics, preserving ground-truth context for validation.

These indices capture both syntactic and semantic patterns and are stored persistently, enabling reuse across experiments without recomputing embeddings.

Handling Queries. Relevant contexts of a targeted task can be retrieved by querying the FAISS indices with the task's code or summary, where the item with the smallest embedding distance to the target is returned. To prevent data leakage during experiment, we filter the task's own context if found during retrieval, ensuring proofs are synthesized solely from external dependencies for the unverified task.

Addressing Repository Context in Verification. Rag-Verus effectively integrates the aforementioned semantic embeddings and static code analysis to prioritize domainspecific syntax (e.g., type definitions) and repository structure (e.g., dependencies). This ensures precise retrieval of relevant lemmas and invariants, avoiding over-retrieval while grounding LLM-generated proofs in verified project contexts.

## References

- <span id="page-11-19"></span>[1] 2024. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. arXiv[:2403.05530](https://arxiv.org/abs/2403.05530) [cs.CL] [https://arxiv.org/abs/](https://arxiv.org/abs/2403.05530) [2403.05530](https://arxiv.org/abs/2403.05530)
- <span id="page-11-7"></span>[2] Pranjal Aggarwal, Bryan Parno, and Sean Welleck. 2024. AlphaVerus: Bootstrapping formally verified code generation through self-improving translation and treefinement. arXiv preprint arXiv:2412.06176 (2024).
- <span id="page-11-23"></span>[3] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. Advances in neural information processing systems 33 (2020), 1877–1901.
- <span id="page-11-11"></span>[4] Yi Cai, Pratap Singh, Zhengyao Lin, and Bryan Parno. 2024. Vest: High-assurance and performant parsing and serialization of binary data formats verified in Verus. <https://tracycy.com/projects/vest>
- <span id="page-11-8"></span>[5] Saikat Chakraborty, Gabriel Ebner, Siddharth Bhat, Sarah Fakhoury, Sakina Fatima, Shuvendu Lahiri, and Nikhil Swamy. 2024. Towards Neural Synthesis for SMT-Assisted Proof-Oriented Programming. arXiv preprint arXiv:2405.01787 (2024).
- <span id="page-11-24"></span>[6] Supratik Chakraborty, Ashutosh Gupta, and Divyesh Unadkat. 2021. Diffy: Inductive Reasoning of Array Programs Using Difference Invariants. In Computer Aided Verification: 33rd International Conference, CAV 2021, Virtual Event, July 20–23, 2021, Proceedings, Part II. Springer-Verlag, Berlin, Heidelberg, 911–935. doi:[10.1007/978-3-030-81688-9\\_42](https://doi.org/10.1007/978-3-030-81688-9_42)
- <span id="page-11-9"></span>[7] Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Hao Yu, Nan Duan, Peng Cheng, et al. 2024. Automated Proof Generation for Rust Code via Self-Evolution. arXiv preprint arXiv:2410.15756 (2024).
- <span id="page-11-17"></span>[8] Chanhee Cho, Yi Zhou, Jay Bosamiya, and Bryan Parno. 2024. A Framework for Debugging Automated Program Verification Proofs via Proof Actions. In International Conference on Computer Aided Verification. Springer, 348–361.
- <span id="page-11-16"></span>[9] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An efficient SMT solver. In International conference on Tools and Algorithms for the Construction and Analysis of Systems. Springer, 337–340.
- <span id="page-11-12"></span>[10] Chris Hawblitzel, Jon Howell, Manos Kapritsos, Jacob R. Lorch, Bryan Parno, Michael L. Roberts, Srinath Setty, and Brian Zill. 2015. IronFleet: proving practical distributed systems correct. In Proceedings of the 25th Symposium on Operating Systems Principles (Monterey, California) (SOSP '15). Association for Computing Machinery, New York, NY, USA, 1–17. doi:[10.1145/2815400.2815428](https://doi.org/10.1145/2815400.2815428)
- <span id="page-11-22"></span>[11] Jeff Johnson, Matthijs Douze, and Hervé Jégou. 2019. Billion-scale similarity search with GPUs. IEEE Transactions on Big Data 7, 3 (2019), 535–547.
- <span id="page-11-5"></span>[12] Adharsh Kamath, Aditya Senthilnathan, Saikat Chakraborty, Pantazis Deligiannis, Shuvendu K Lahiri, Akash Lal, Aseem Rastogi, Subhajit Roy, and Rahul Sharma. 2023. Finding inductive loop invariants using large language models. arXiv preprint arXiv:2311.07948 (2023).
- <span id="page-11-14"></span>[13] Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick SH Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. Dense Passage Retrieval for Open-Domain Question Answering.. In EMNLP (1). 6769–6781.
- <span id="page-11-29"></span>[14] Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris Yakobowski. 2015. Frama-C: A software analysis perspective. Formal aspects of computing 27, 3 (2015), 573–609.
- <span id="page-11-3"></span>[15] Andrea Lattuada, Travis Hance, Jay Bosamiya, Matthias Brun, Chanhee Cho, Hayley LeBlanc, Pranav Srinivasan, Reto Achermann, Tej Chajed, Chris Hawblitzel, et al. 2024. Verus: A practical foundation for systems verification. In Proceedings of the ACM SIGOPS 30th Symposium on Operating Systems Principles. 438–454.
- <span id="page-11-1"></span>[16] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel.

- 2023. Verus: Verifying rust programs using linear ghost types. Proceedings of the ACM on Programming Languages 7, OOPSLA1 (2023), 286–315.
- <span id="page-11-2"></span>[17] K Rustan M Leino. 2010. Dafny: An automatic program verifier for functional correctness. In International conference on logic for programming artificial intelligence and reasoning. Springer, 348–370.
- <span id="page-11-15"></span>[18] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. 2020. Retrieval-augmented generation for knowledge-intensive nlp tasks. Advances in Neural Information Processing Systems 33 (2020), 9459–9474.
- <span id="page-11-4"></span>[19] Xupeng Li, Xuheng Li, Wei Qiang, Ronghui Gu, and Jason Nieh. 2023. Spoq: Scaling {Machine-Checkable} Systems Verification in Coq. In 17th USENIX Symposium on Operating Systems Design and Implementation (OSDI 23). 851–869.
- <span id="page-11-28"></span>[20] Yixuan Li, Julian Parsert, and Elizabeth Polgreen. 2024. Guiding enumerative program synthesis with large language models. In International Conference on Computer Aided Verification. Springer, 280–301.
- <span id="page-11-0"></span>[21] Zhaoyu Li, Jialiang Sun, Logan Murphy, Qidong Su, Zenan Li, Xian Zhang, Kaiyu Yang, and Xujie Si. 2024. A Survey on Deep Learning for Theorem Proving. In First Conference on Language Modeling. [https:](https://openreview.net/forum?id=zlw6AHwukB) [//openreview.net/forum?id=zlw6AHwukB](https://openreview.net/forum?id=zlw6AHwukB)
- <span id="page-11-30"></span>[22] Dianshu Liao, Shidong Pan, Xiaoyu Sun, Xiaoxue Ren, Qing Huang, Zhenchang Xing, Huan Jin, and Qinying Li. 2024. A 3-CodGen: A Repository-Level Code Generation Framework for Code Reuse with Local-Aware, Global-Aware, and Third-Party-Library-Aware. IEEE Transactions on Software Engineering (2024).
- <span id="page-11-27"></span>[23] Junrui Liu, Yanju Chen, Bryan Tan, Isil Dillig, and Yu Feng. 2022. Learning contract invariants using reinforcement learning. In Proceedings of the 37th IEEE/ACM International Conference on Automated Software Engineering. 1–11.
- <span id="page-11-31"></span>[24] LlamaIndex. [n. d.]. LlamaIndex: Build Knowledge Assistants over your Enterprise Data. <https://www.llamaindex.ai/>. Accessed: 2024-11-07.
- <span id="page-11-10"></span>[25] Chloe Loughridge, Qinyi Sun, Seth Ahrenbach, Federico Cassano, Chuyue Sun, Ying Sheng, Anish Mudide, Md Rakib Hossain Misu, Nada Amin, and Max Tegmark. 2024. DafnyBench: A Benchmark for Formal Software Verification. arXiv preprint arXiv:2406.08467 (2024).
- <span id="page-11-25"></span>[26] Md Rakib Hossain Misu, Cristina V Lopes, Iris Ma, and James Noble. 2024. Towards ai-assisted synthesis of verified dafny methods. Proceedings of the ACM on Software Engineering 1, FSE (2024), 812–835.
- <span id="page-11-18"></span>[27] OpenAI. 2024. Hello GPT-4O. <https://openai.com/index/hello-gpt-4o/> [Accessed: 2024-11-07].
- <span id="page-11-21"></span>[28] OpenAI. 2024. New embedding models and API updates. [https:](https://openai.com/index/new-embedding-models-and-api-updates/) [//openai.com/index/new-embedding-models-and-api-updates/](https://openai.com/index/new-embedding-models-and-api-updates/) Accessed: 2025-01-31.
- <span id="page-11-20"></span>[29] Disha Shrivastava, Hugo Larochelle, and Daniel Tarlow. 2023. Repository-level prompt generation for large language models of code. In Proceedings of the 40th International Conference on Machine Learning (Honolulu, Hawaii, USA) (ICML'23). JMLR.org, Article 1314, 23 pages.
- <span id="page-11-26"></span>[30] Xujie Si, Aaditya Naik, Hanjun Dai, Mayur Naik, and Le Song. 2020. Code2inv: A deep learning framework for program verification. In Computer Aided Verification: 32nd International Conference, CAV 2020, Los Angeles, CA, USA, July 21–24, 2020, Proceedings, Part II 32. Springer, 151–164.
- <span id="page-11-6"></span>[31] Chuyue Sun, Ying Sheng, Oded Padon, and Clark Barrett. 2024. Clover: Clo sed-Loop Ver ifiable Code Generation. In International Symposium on AI Verification. Springer, 134–155.
- <span id="page-11-13"></span>[32] Xudong Sun, Wenjie Ma, Jiawei Tyler Gu, Zicheng Ma, Tej Chajed, Jon Howell, Andrea Lattuada, Oded Padon, Lalith Suresh, Adriana Szekeres, et al. 2024. Anvil: Verifying liveness of cluster management controllers. In 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24). 649–666.

- <span id="page-12-6"></span><span id="page-12-0"></span>[33] Jingbo Wang and Chao Wang. 2022. Learning to synthesize relational invariants. In Proceedings of the 37th IEEE/ACM International Conference on Automated Software Engineering. 1–12.
- <span id="page-12-2"></span>[34] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun Li, Shing-Chi Cheung, and Cong Tian. 2024. Enchanting program specification synthesis by large language models using static analysis and program verification. In International Conference on Computer Aided Verification. Springer, 302–328.
- <span id="page-12-3"></span>[35] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui, Yeyun Gong, Chris Hawblitzel, Shuvendu Lahiri, Jacob R Lorch, Shuai Lu, et al. 2024. Autoverus: Automated proof generation for rust code. arXiv preprint arXiv:2409.13082 (2024).
- <span id="page-12-5"></span>[36] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J Prenger, and Animashree Anandkumar. 2024. Leandojo: Theorem proving with retrieval-augmented language models. Advances in Neural Information Processing Systems 36 (2024).
- <span id="page-12-1"></span>[37] Lichen Zhang, Shuai Lu, and Nan Duan. 2024. Selene: Pioneering Automated Proof in Software Verification. arXiv preprint arXiv:2401.07663 (2024).
- <span id="page-12-4"></span>[38] Ziqiao Zhou, Weiteng Chen, Sishuai Gong, Chris Hawblitzel, Weidong Cui, et al. 2024. {VeriSMo}: A verified security module for confidential {VMs}. In 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24). 599–614.

Received 2025-07-05; accepted 2025-08-08