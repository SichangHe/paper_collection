## KVerus: Scalable and Resilient Formal Verification Proof Generation for Rust Code

[Yuwei Liu](https://orcid.org/0000-0001-5170-3388) Ant Group Hangzhou, China lyw458372@antgroup.com

[Minghua Wang](https://orcid.org/0000-0002-2270-2076) Ant Group Beijing, China minghua.wmh@antgroup.com

[Xinyi Wan](https://orcid.org/0009-0004-3543-499X) Ant Group Shanghai, China wanxinyi.wxy@antgroup.com

[Lin Huang](https://orcid.org/0009-0002-5659-1471) Ant Group Beijing, China linyu.hl@antgroup.com

[Yanhao Wang](https://orcid.org/0000-0002-6990-2972) Independent Beijing, China wangyanhao136@gmail.com

[Tao Wei](https://orcid.org/0000-0001-9537-7051) Ant Group Hangzhou, China lenx.wei@antgroup.com

#### Abstract

Formal verification provides the highest assurance of software correctness and security, but its application to large-scale, evolving systems remains a major challenge. While large language models (LLMs) have shown promise in automating proof generation, they often fail in real-world settings due to their inability to handle complex cross-module dependencies or changes in the codebase or the verification toolchain. We identify the fundamental problem as the Semantic-Structural Gap: LLMs operate on semantic code patterns, whereas formal verification is governed by rigid structural dependencies, a disconnect that leads to brittle, unsustainable proofs.

To bridge this gap, we propose a new paradigm of self-adaptive verification and present KVerus, a retrieval-augmented system for Verus-based Rust verification that can adapt to a complex and evolving software environment. KVerus constructs a dynamic knowledge base of code metadata, lemma semantics, and toolchain specifics. By combining dependency-aware program analysis, semantic lemma indexing, and error-driven self-refinement, it can navigate intricate cross-file dependencies to synthesize proofs and automatically repair proofs when faced with common evolutionary changes. Across three single-file benchmarks, KVerus verifies 80.2% of tasks, outperforming the state-of-the-art AutoVerus (56.9%) and degrades less than AutoVerus under breaking Verus updates. On three repository-level benchmarks with cross-file dependencies, KVerus achieves a 51.0% success rate, compared to 4.5% for a multi-round prompting baseline. Finally, on the Asterinas Rust OS kernel, KVerus produces upstream-accepted proofs that verify 23 previously unverified functions (21.0% of proof code) in the memory-management module. KVerus represents a significant step towards making formal verification a scalable and sustainable practice for modern, security-critical software.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

Conference'17, Washington, DC, USA

© 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 978-x-xxxx-xxxx-x/YYYY/MM <https://doi.org/10.1145/nnnnnnn.nnnnnnn>

#### ACM Reference Format:

Yuwei Liu, Xinyi Wan, Yanhao Wang, Minghua Wang, Lin Huang, and Tao Wei. 2026. KVerus: Scalable and Resilient Formal Verification Proof Generation for Rust Code. In . ACM, New York, NY, USA, [14](#page-13-0) pages. [https:](https://doi.org/10.1145/nnnnnnn.nnnnnnn) [//doi.org/10.1145/nnnnnnn.nnnnnnn](https://doi.org/10.1145/nnnnnnn.nnnnnnn)

#### 1 Introduction

Formal verification has long been considered the gold standard for ensuring the correctness and security of critical software systems. By enforcing strict safety constraints, formal verification can eliminate entire classes of bugs that often evade traditional testing, such as null dereferences, array out-of-bounds errors, and race conditions. Beyond these generic categories, it also addresses project-specific logical flaws embedded in system design by proving that the implementation adheres to a formal specification. This capability is virtually unattainable through traditional testing methods. Its effectiveness has been demonstrated across domains such as microkernels, cryptographic libraries, and verified compilers, e.g., seL4 [\[16\]](#page-12-0), CertiKOS [\[11\]](#page-11-0) and CompCert [\[21\]](#page-12-1). However, the strong guarantees come at the price of a substantial proof burden, making it challenging to apply such techniques to large-scale, evolving software systems.

Programs are typically verified either manually within an interactive theorem prover [\[5,](#page-11-1) [25,](#page-12-2) [27,](#page-12-3) [32\]](#page-12-4), or semi-automatically using deductive program verifiers,[1](#page-0-0) such as VST-A [\[39\]](#page-12-5) for C, Verus [\[17,](#page-12-6) [18\]](#page-12-7) for Rust, and Dafny [\[19\]](#page-12-8). Despite their differences, both approaches still impose substantial manual effort. Engineers often need to write thousands of lines of proof code, manage intricate dependency graphs, and continually adapt to changes in both the codebase and the verification toolchain. This brittleness, where small code changes or toolchain updates can invalidate extensive proofs, limits the scalability and sustainability of verification for large, modular systems such as operating systems, distributed runtimes, or storage stacks.

The rapid advancement of Large Language Models (LLMs) has sparked renewed interest in automating parts of the formal verification workflow. Recent studies [\[2,](#page-11-2) [7,](#page-11-3) [23,](#page-12-9) [24,](#page-12-10) [34,](#page-12-11) [37\]](#page-12-12) have demonstrated the potential of LLMs in small-scale verification tasks and code generation. However, these techniques consistently break down when

<span id="page-0-0"></span><sup>1</sup>By deductive, we refer to approaches where specifications and proof annotations accompany the source code, with the generated verification conditions discharged by a backend solver (typically SMT-based).

applied to large, modular, real-world codebases, where the complexity and scale introduce fundamental challenges.

In our analysis, we identify four key limitations that hinder the scalability of current LLM-based verification systems. First, LLMs often lack the contextual understanding required to reason across modular systems, making it difficult for them to determine which components are relevant to a specific verification goal. Second, they struggle with lemma discovery and reuse, which is a critical capability for scaling formal verification, especially when documentation of lemma functions is incomplete or outdated. Third, current models exhibit limited robustness to toolchain changes: even minor updates in systems such as Verus [2](#page-1-0) can invalidate existing proofs, and there is no built-in mechanism for automatic adaptation. Finally, most approaches fail to scale across modules, as they depend on brittle, manually maintained global specifications that cannot evolve gracefully alongside large, evolving codebases.

We argue these challenges are symptoms of a fundamental disconnect: the Semantic-Structural Gap. LLMs operate in a semantic world of text and code patterns. They recognize and generate code based on the patterns they were trained on. Formal verification, on the other hand, lives in a structural world governed by rigid dependency graphs, logical implications between lemmas, and the precise syntax rules of the verifier.

This gap highlights why current approaches, which generate proofs for a static codebase under a fixed toolchain once and for all, are ultimately unsustainable, particularly in practical or industrial settings. The crisis becomes evident when a breaking change occurs: a minor update to the toolchain can invalidate the LLM's semantic understanding, causing widespread proof failures. An LLM cannot natively perceive that a syntax change is a structural rule modification; it only sees a deviation from the semantic patterns on which it was trained. Without an understanding of the system's architectural blueprint, the LLM is unable to reason about how to repair the proofs. It would be akin to trying to fix a faulty bridge design by merely repainting it.

This challenge manifests acutely in emerging Rust verification frameworks such as Verus, as the language's rapid adoption in critical systems has spurred the creation of powerful yet fast-evolving toolchains. For instance, in CortenMM [\[38\]](#page-12-13), the verified memory management module of the general-purpose OS kernel Asterinas [\[28\]](#page-12-14), frequent updates to Verus repeatedly broke existing proofs and required manual intervention. Over six months, the verification code required eight synchronizations, averaging roughly once every three weeks. A similar phenomenon is observed even at the benchmark scale. Verus-Bench, a suite derived from AutoVerus, was significantly affected by recent syntax changes to loop constructs. To make it compatible with the latest release of Verus, more than 400 lines of code had to be revised, underscoring that both large-scale real-world verification efforts and relatively simple benchmarks are fragile under evolving toolchains.

Therefore, the only viable path forward is to bridge this Semantic-Structural Gap by architecting a self-evolving system that can adapt to changes over time. Instead of relying on a static "unstable generation," the focus must shift to continuous adaptation, where the

verification system is capable of evolving along with the codebase and toolchain.

To address this gap, we present KVerus, a retrieval-augmented, self-adaptive verification system designed to generate Verus-compatible proofs from high-level system specifications and source code. KVerus introduces several key innovations:

- (1) Dependency-Aware Program Analysis: The system performs metadata-level dependency extraction to identify relevant functions, types, and lemmas for each verification task.
- (2) Semantic Lemma Indexing: Lemmas are embedded and indexed using LLM-based summarization, enabling discovery and reuse even when documentation is incomplete.
- (3) Error-Driven Self-Refinement: When verification fails due to toolchain or codebase changes, KVerus performs knowledge-aware debugging and automatically regenerates affected proofs through an error-driven Refiner.

Specifically, our approach centers on a comprehensive knowledge base that the LLM queries using Retrieval-Augmented Generation (RAG) to select semantically relevant knowledge and streamline the proof generation process. This knowledge base integrates three essential types of knowledge, each corresponding to one of key innovations. First, to enable Dependency-Aware Program Analysis, we construct a code metadata knowledge graph by extracting function signatures and dependencies from the target code. Second, to support Semantic Lemma Indexing, we generate Lemma Knowledge by using an LLM to summarize existing lemmas into concise, searchable descriptions. Finally, the Error-Driven Self-Refinement capability is realized by a dedicated refinement module. This module leverages a continuously updated Verus Knowledge base and analyzes error types and diagnostic feedback from the verifier, iteratively refining the generated proof code until verification succeeds.

To evaluate its effectiveness, we conduct comprehensive experiments on three single-file benchmarks and three repository-level benchmarks involving complex cross-file dependencies. The results demonstrate that KVerus consistently outperforms the state-ofthe-art tool AutoVerus. On single-file tasks, KVerus achieves an 80.2% success rate—surpassing AutoVerus by 23.3%—while reducing token costs by over 50% and demonstrating superior robustness against breaking toolchain updates. On the repository-level benchmarks, KVerus achieves a 51.0% success rate, compared to 4.5% for a multi-round prompting baseline. Furthermore, we apply KVerus to the verification of the Asterinas Rust OS kernel, where it achieves an 8x improvement over strong prompting baselines. Notably, KVerus successfully verifies 23 previously unverified functions, covering 21.0% of the target memory management module, with proofs accepted into both the kernel mainline and the Verus standard library.

In summary, our contributions are:

- We identify the Semantic-Structural Gap as the fundamental bottleneck preventing current LLM-driven verification approaches from scaling, and categorize its primary symptoms.
- We propose a self-adaptive, retrieval-augmented system for formal verification across evolving, multi-module codebases.
- We implement KVerus, a novel verification pipeline combining semantic indexing, dependency analysis, error-aware generation, and self-refinement.

<span id="page-1-0"></span>In the context of Verus, the verification toolchain encompasses the Verus verifier, the underlying SMT solver (e.g., Z3), the Rust compiler, and the Verus standard library (vstd).

 We demonstrate KVERUS's superiority over state-of-the-art methods in accuracy, cost-efficiency, and robustness. Crucially, we prove its real-world utility by contributing accepted proof code to the Asterinas Rust OS kernel and the Verus standard library, verifying complex logic ranging from high-level specifications to bit-level implementations.

#### 2 Background and Motivation

#### 2.1 Formal Verification for Rust

Rust employs a rigorous ownership model and borrow-checking mechanism that greatly mitigate common memory safety vulnerabilities. However, absolute memory safety is not guaranteed, as unsafe code, logical flaws, and potential defects in the compiler or standard library may still introduce correctness and security risks. To address these limitations, formal methods such as model checking (e.g., Kani [35] or UnsafeCop [36]), deductive verification (e.g., Prusti [4], Creusot [10], or Verus [17, 18]), abstract interpretation (e.g., MIRAI [31]), and runtime verification (e.g., Miri [14]) have been applied to Rust programs to verify safety-critical properties. Notably, the Rust project itself has initiated efforts toward formal specification and verification of the standard library [1], underscoring the recognition within the Rust community that rigorous, machine-checked guarantees are essential to complement the language's safety-oriented design.

Among these approaches, Verus is a state-of-the-art Rust-native verifier. Inspired by recent advances in proof theories[12, 13, 15, 22], it extends Rust's syntax and type system with expressive specification constructs, such as preconditions, postconditions, invariants, and ghost states, allowing precise reasoning about functional correctness and safety properties. Using these extensions, Verus enables the verification of complex data structures and algorithms through fine-grained reasoning about ownership and auxiliary ghost state. These proof obligations and user-supplied assertions are then translated into verification conditions, which are discharged by SMT solvers (e.g., Z3[9]), significantly reducing the need for manual proofs compared to conventional interactive theorem provers. This balance between expressiveness and automation positions Verus as a practical tool for verifying real-world Rust software at scale[8, 30, 40].

Although Verus significantly automates the verification for Rust, recent research has explored the use of LLMs to further alleviate the manual proof burden. Tools such as AUTOVERUS [37], AlphaVerus [2], and SAFE [7] embed expert verification knowledge into prompt engineering and interactive refinement loops. Despite progress, these LLM-based systems remain inadequate for real-world Rust verification. Their core limitation, the Semantic-Structural Gap, prevents them from effectively mapping high-level proof intentions to explicit dependency graphs, rigorous logical entailments, and strict syntactic rules required by Verus. This gap becomes particularly severe when verifying real-world systems code with complex, cross-module dependencies, as illustrated by our motivating example.

#### 2.2 Motivation Example

Listing 1 presents an unproven Verus lemma function from CortenMM, the memory management module of the Asterinas kernel. The lemma, named lemma\_va\_range\_get\_tree\_path, formally verifies properties of the page table traversal path derived from a virtual address range va. The precondition (lines 3-4) requires that va satisfies va\_range\_wf, a predicate ensuring the range is well-formed. Specifically, va must lie within a valid virtual address space, its start must be strictly less than its end, and both addresses must be aligned to the required granularity (lines 12-17). The postconditions (lines 5-7) ensure two critical properties. First, every page table node ID in the sequence returned by va\_range\_get\_tree\_path(va) must satisfy the predicate NodeHelper::valid\_nid. Second, the length of the traversal path must equal 5 - va\_range\_get\_guard\_level(va), establishing a fixed structural relationship between the address range and its page table traversal depth. This lemma establishes the correctness of page table traversal over a given virtual address range, which is a key prerequisite for proving memory safety and functional correctness in the page table locking mechanism. Even understanding this lemma requires retrieving both the cursor functions in src/exec/rw/cursor.rs and the NodeHelper specifications in src/spec/utils.rs, illustrating the cross-module dependencies typical of real kernels.

Consequently, existing automated proof-generation methods [2, 7, 37] are unable to prove this lemma. Lacking a structural understanding of the codebase, they would not know to retrieve the necessary definitions from different files. Furthermore, without a mechanism for systematic lemma reuse, they cannot leverage existing knowledge, rendering the verification of such interconnected components intractable.

#### 2.3 Challenges

Our analysis reveals that the key limitations of LLM-based verification, which are symptoms of the underlying **Semantic-Structural Gap**, manifest as three concrete technical challenges when applied to real-world systems like Asterinas. Existing methods fail because they only utilize partial knowledge of the verification target, typically limited to language objects within a single file. To build a truly scalable system, we must therefore address the following challenges:

Challenge 1: Cross-Module Knowledge Extraction. AUTOVERUS, SAFE, and AlphaVerus simply provide the whole single file to LLMs. However, real-world software like the Rust OS kernel Asterinas spans dozens of modules, directories, and abstraction layers. We must automatically build a metadata dependency graph that captures all function definitions, type declarations, invariants, and inter-file dependencies, as well as collect every lemma function scattered across the codebase. Failing to extract this holistic view precludes end-to-end proof generation.

Challenge 2: Lemma Comprehension and Reuse. AUTOVERUS, SAFE, and AlphaVerus neither exploit previously proven lemmas in the verification target nor integrate Verus's built-in standard library. We need a Comprehender that (1) vectorizes annotated lemmas, (2) uses LLMs to generate natural-language summaries for unannotated lemmas, and (3) maintains an up-to-date, queryable lemma knowledge base. Effective lemma retrieval and guided reuse are essential to avoid redundant proofs and enable modular reasoning.

```
/// src/exec/rw/cursor/va_range.rs
                                                                                         pub proof fn lemma_va_range_get_tree_path(va: Range<Vaddr>)
  pub proof fn lemma_va_range_get_tree_path(va: Range<Vaddr>)
                                                                                           requires
                                                                                              va_range_wf(va),
       va_range_wf(va),
                                                                                            ensures
         va_range_get_tree_path(va).all(|id| NodeHelper::valid_nid(id)),
                                                                                           let guard_level = va_range_get_guard_level(va);
         va_range_get_tree_path(va).len() == 5 - va_range_get_guard_level(va),
                                                                                            let trace = va_level_to_trace(va.start, guard_level);
10
  }
                                                                                            lemma_va_range_get_guard_level(va);
                                                                                      11
12 pub open spec fn va_range_wf(va: Range<Vaddr>) -> bool {
                                                                                            lemma_va_level_to_trace_rec_len(va.start >> 12, guard_level);
     &&& valid_va_range(va)
                                                                                            let path = va_range_get_tree_path(va);
13
                                                                                      13
     &&& va.start < va.end
14
                                                                                            assert(path.len()
                                                                                                                    + trace.len())
                                                                                            assert(path.len() == 1 + trace.len()),
assert(path.len() == 5 - guard_level);
     &&& vaddr is aligned(va.start)
15
     && vaddr_is_aligned(va.end)
                                                                                            assert forall|i| 0 <= i < path.len() implies
                                                                                              NodeHelper::valid_nid(path[i]) by {
17
                                                                                      17
                                                                                              let nid = path[i];
                                                                                              if i == 0 {
19
   /// src/snec/utils rs
                                                                                      19
   impl NodeHelper {
                                                                                                   From src/spec/utils.r
     pub open spec fn valid_nid(nid: NodeId) -> bool {
21
                                                                                      21
                                                                                                NodeHelper::lemma_root_id();
         0 <= nid < Self::total_size()</pre>
22
                                                                                      22
                                                                                              } else {
                                                                                                       n Verus standard library
23
     }
                                                                                      23
                                                                                                let sub_trace = trace.subrange(0, i);
24
                                                                                      24
   }
                                                                                                    na_va_level_to_trace_valid(va.start, guard_level);
                                                                                      26
26
   /// src/mm/mod.rs
28 pub type Vaddr = usize;
```

nas that remains unproven.

<span id="page-3-0"></span>Listing 1: Motivation example. A lemma function from Asteri- Listing 2: KVERUS-generated proof for the motivation example. The highlighted code represents the generated proof, while comments indicate the source of external dependencies required for verification.

**Challenge 3**: Robust Adaptation to Language Evolution and LLM Limitations. AutoVerus, SAFE, and AlphaVerus embed human expert knowledge of Verus into the prompt. However, Verus is under active development. Here, we extend the notion of unstable generation, which was originally used to describe verification failures arising from changes to the verified source code [20], to include failures caused by modifications to the verification toolchain itself. In our setting, updates to Verus's syntax or feature set can render previously valid, LLM-generated proofs invalid, even when the underlying program logic remains correct. Moreover, LLMs have limited exposure to formal-verification languages, leading to broken or incorrect proof fragments. We must implement an automatically updatable Verus knowledge repository-extracting new documentation and examples after each breaking change-and design a Refiner that classifies Verus error messages, retrieves corrective guidance from the knowledge base, and iteratively refines LLM prompts to recover from failures.

#### Our Solution

To address these challenges, we designed KVERUS, a knowledgecentric framework that transforms disparate sources of information into a structured, actionable foundation for proof generation. As illustrated in Figure 1, the architecture is a pipeline of four key modules that systematically build and leverage this knowledge.

First, the Preprocessor module tackles Challenge 1 (Cross-Module Knowledge Extraction). It performs a deep static analysis of the entire codebase to construct a cross-module dependency graph. This process extracts essential code metadata, including all relevant function signatures, structures, traits, and their inter-file relationships, providing a holistic structural view of the verification

<span id="page-3-1"></span>Next, the Comprehender module addresses Challenge 2 (Lemma Comprehension and Reuse). It builds a semantic lemma knowledge base from two sources: it parses natural language descriptions from existing documentation and, for undocumented lemmas, uses an LLM to generate concise summaries from their formal specifications. This knowledge is then vectorized and indexed, creating a searchable repository that enables efficient lemma discovery and

With this structured knowledge in place, the core proof synthesis occurs in a two-stage loop. The Prover module is the primary proof generator. Guided by the dependency graph and leveraging RAG-based search over the lemma knowledge base, it synthesizes an initial proof attempt. This proof is then passed to the Refiner module, which confronts Challenge 3 (Robust Adaptation). If verification fails, this module analyzes the error diagnostics from the compiler and verifier, queries a continuously updated Verus knowledge base for corrective patterns, and iteratively refines the

This integrated workflow allows KVERUS to systematically gather the necessary cross-module context, including semantic dependencies that are not syntactically referenced by the verification target (e.g., lemma\_va\_level\_to\_trace\_rec\_len and vstd::seq::Seq :: subrange), retrieve the precise lemmas required, and automatically synthesize the complete, correct proof for the motivating example (see Listing 2).

#### **KVerus** Design

In this section, we present the design of KVERUS, detailing the architecture and functionality of its four main modules. The system is designed as a pipeline that systematically constructs, comprehends, and utilizes distinct types of knowledge to achieve robust, automated verification.

<span id="page-4-0"></span>![](_page_4_Figure_2.jpeg)

Figure 1: The workflow of KVERUS.

## <span id="page-4-1"></span>3.1 *Preprocessor*: Code and Lemma Preprocessing

The *Preprocessor* module analyzes the source code of the target verification library to construct a metadata dependency graph and to index lemma functions for subsequent retrieval and proof synthesis.

Metadata Dependency Graph. We build metadata dependency graph as a typed directed graph over Verus/Rust language objects. Each node is a language object identified by its fully-qualified path, including functions (and spec/lemma functions), composite types (structs/enums), traits, and type aliases. A directed edge  $u \rightarrow v$  indicates that verifying or type-checking u may require information about v. Each edge is labeled with a dependency type t. We model two families of dependencies. (A) Type/structure dependencies capture signature type references, composite containment, trait-impl relations, and type-alias relations. (B) Call/spec dependencies capture function/spec-function calls and references appearing in requires/ensures/invariants. For example, the signature of lemma\_va\_range\_get\_tree\_path (Listing 1) indicates dependencies on the spec functions va\_range\_wf, va\_range\_get\_tree\_path, and va\_range\_get\_guard\_level, the structure NodeHelper, and the type alias Vaddr.

**Dependent Code (Definition).** Given an unproven target function f, we define dependent code as the set of language objects collected by traversing outgoing metadata dependency graph edges from f with a maximum depth of 3. In our target projects, a maximum depth of 3 covers the vast majority of cross-file reference chains while keeping the retrieved context compact enough for LLM prompting. We deduplicate nodes by fully-qualified paths and

stop expanding a node once it is included. This dependency-scoped context provides cross-file information beyond a single file without indiscriminately including the entire repository.

Lemma Function Extraction. Lemma functions in Verus are special functions that do not execute at runtime but instead serve as logical assertions to assist in formal verification. They encode invariants, proof strategies, and domain-specific reasoning steps, enabling developers to modularize complex proofs into reusable components. Lemma functions are particularly important for verifying real-world software systems, which often rely on layered abstractions and intricate invariants. By leveraging lemmas, proofs can be decomposed into smaller, more manageable parts, thereby facilitating modular reasoning and promoting the reuse of previously verified knowledge. In KVERUS, we extract the signature of each lemma function, including its name, parameters, preconditions (requires), and postconditions (ensures), along with its comments and module location. This information is later used by the Comprehender module for semantic interpretation and by the Prover module to support lemma invocation during proof synthesis.

## 3.2 Comprehender: Knowledge Comprehension and Synthesis

The *Comprehender* module synthesizes knowledge by integrating two key components: a RAG module that comprehends and extracts natural language descriptions for lemma functions from source code and documentation to construct a lemma database, and an autoupdated Verus knowledge database. For the source code of lemma functions from the verification target, we extract the necessary

information in the Preprocessor module. For documentation from both the verification target and Verus, the content is parsed and indexed to enable efficient retrieval of natural language descriptions and usage examples.

Natural Language Description for Lemma Functions. To support efficient retrieval via RAG-based search, all extracted and synthesized knowledge is vectorized and stored in the database. Conventional RAG techniques are primarily designed for plain text and often perform poorly when applied to source code. In Verus, official lemma functions (primarily those related to arithmetic operations and common data structures such as sets, sequences, and maps) are typically accompanied by natural language comments specifying their preconditions and postconditions. However, third-party lemma functions, such as those in real-world projects, frequently lack such annotations or contain only minimal commentary. [Listing 3](#page-6-0) illustrates this contrast. The function lemma\_multiply\_divide\_lt (lines 1-10), from the Verus standard library, includes a detailed comment outlining its invocation conditions and the properties it ensures. In contrast, lemma\_va\_range\_get \_guard\_level (lines 14-18), from CortenMM, contains no descriptive annotation.

To address this gap, we leverage LLMs to automatically generate natural language descriptions for undocumented or sparsely documented lemma functions. For each function, we construct a prompt containing its full signature, including the name, parameters, and requires and ensures clauses. These synthesized descriptions are then vectorized and stored in the database alongside their wellannotated counterparts, enabling consistent and comprehensive retrieval during proof generation. The generated descriptions are shown in [Listing 3,](#page-6-0) lines 11-13, demonstrating how the LLM fills in missing semantic information to support downstream retrieval and reasoning.

Auto-updated Verus Knowledge. Previous works such as AutoVerus, SAFE, and AlphaVerus embed expert knowledge of Verus into carefully crafted prompts to improve the success rate of LLM-generated Verus proof code. However, as Verus is actively evolving, breaking changes in its syntax or features can render existing prompts outdated or incompatible, thereby reducing the effectiveness of proof generation. For example, a breaking change occurred regarding loop invariants. In previous versions of Verus, loops could be verified without explicit termination proofs. However, recently, Verus introduced a requirement that while loops must include a decreases clause to prove termination. This semantic shift, which is not reflected in AutoVerus's static prompts, caused the success rate on Verus-Bench tasks to drop from 86.0% to 58.0% [\(Table 2](#page-8-0) in [Section 5.1\)](#page-6-1).

To address this issue, we periodically parse the official Verus documentation to extract up-to-date knowledge. For instance, the document provides updated guidance on loop syntax and invariants.[3](#page-5-0) We index the content using the documentation title as a key to support efficient retrieval. Unlike systems relying on static, expert-curated rules, our knowledge base evolves automatically with the Verus toolchain, ensuring long-term robustness.

## 3.3 Prover: Knowledge-Driven Proof Generation

After extracting three types of knowledge, KVerus generates proof code based on the constructed knowledge base. For a given unproven target function to be verified, the Prover module first extracts the dependent code using the code metadata knowledge. It then employs the requirement analyzer to retrieve the necessary lemma functions from the lemma description database, constructing structured prompts for the LLM to facilitate proof generation.

Dependent Code (Usage). For a target function , the Prover queries Preprocessor to obtain the dependency-scoped context (dependent code) defined in [Section 3.1.](#page-4-1) The returned objects are serialized into compact snippets (signature/declaration, Verus specifications, comments, and module paths) and ordered by dependency type, with type/structure items placed before call/spec items. These snippets, together with the target function and retrieved lemma candidates, are incorporated into the structured proof-generation prompt.

Requirement Analyzer. Retrieving relevant lemma functions from the lemma description database requires natural language descriptions of the lemmas needed for proof generation, a capability lacking in conventional methods. KVerus addresses this limitation by combining the unproven function with its dependent code into a prompt, which is then provided to the LLM. The LLM generates natural language descriptions of the required lemmas, which are subsequently used to query the database for potential matches that meet the proof requirements.

## 3.4 Refiner: Error-Driven Proof Refinement

Formal verification languages exhibit severe data scarcity, with their public corpora on GitHub representing less than 1% of the volume available for general-purpose languages like Python or C++[4](#page-5-1) . This data sparsity contributes to the frequent syntax and verification errors observed in LLM-generated proofs.

To address these issues, we integrate the Refiner module into KVerus to iteratively refine the generated proof code until it passes verification. The Refiner module first classifies the encountered errors and, based on the error type, retrieves the corresponding knowledge from the Verus knowledge database. It then combines this knowledge with the erroneous proof code and the associated error message to construct a prompt, which is provided to the LLM for refinement.

Error Triager. Because of the LLM context length limitations and the "lost-in-the-middle" problem that arises when the context becomes excessively long, it is impractical to include all Verusrelated knowledge in a single prompt. To address this, we triage errors triggered by the generated proof code according to the error message and the location in the code where the error occurs. The error-corresponding Verus knowledge is then selectively incorporated into the prompt for refinement. The error triager currently applies a set of curated rules that leverage pattern matching and keyword extraction from Verus compiler output to classify failures into knowledge base categories such as loop invariants, arithmetic overflows, bit-vectors, and specification syntax.

<span id="page-5-0"></span><sup>3</sup><https://verus-lang.github.io/verus/guide/while.html>

<span id="page-5-1"></span><sup>4</sup>As of this writing, GitHub hosts about 21.9M Python, 5.9M C++, and 3.6M C repositories, but only 7.1K Rocq, 5.9K Lean, 1.2K Isabelle, and fewer than 50 Verus repositories.

```
1 /// Proof that if an integer is less than the product of two other integers,
2 /// then the quotient with one of them will be less than other.
3 /// Specifically, `a<b*c`, we know `a/b<c`
4 pub proof fn lemma_multiply_divide_lt(a: int, b: int, c: int)
5 requires
6 0 < b,
7 a < b * c,
8 ensures
9 a / b < c,
                                                                              1 /// Given a well-formed virtual address range,
                                                                              2 /// this lemma proves that the guard level is
                                                                              3 /// always between 1 and 4 (inclusive).
                                                                              4 pub proof fn lemma_va_range_get_guard_level(va: Range<Vaddr>)
                                                                              5 requires
                                                                              6 va_range_wf(va),
                                                                              7 ensures
                                                                              8 1 <= va_range_get_guard_level(va) <= 4,
```

<span id="page-6-0"></span>Listing 3: Function signature, comment, and specification of lemma functions from Verus and Asterinas. The highlighted comments are generated by KVerus.

New Lemmas. Occasionally, the LLM identifies the need for additional new lemma functions to facilitate the verification process. In such cases, KVerus integrates these newly generated lemma functions into the knowledge base for use in subsequent verification tasks.

## 4 Implementation

We implemented KVerus based on verus-analyzer [\[33\]](#page-12-22) and LangChain [\[6\]](#page-11-13) frameworks in about 5,837 lines of Python code and 1,015 lines of Rust code, all of which are open-sourced. Some noteworthy details are described below.

Code Metadata Extraction. We implement code metadata extraction on top of verus-analyzer, a rust-analyzer–derived front-end for Verus that exposes resolved symbols and type information. We build a project-wide language database for the target crate and assign each language object a stable identifier using its fully-qualified path (module path + name) to avoid ambiguity under imports and reexports. We extract four categories of objects—functions (including spec/lemma functions), composite types (structs/enums), traits, and type aliases—together with their source ranges and doc comments for later prompt serialization. We model two families of dependency relationships. (A) Type/structure dependencies include: (1) a function references a composite type or a type alias in its signature (parameter/return types); (2) a function is associated with a composite type (e.g., methods); (3) a composite type contains another type as a field/member; (4) a composite type is redefined via a type alias; (5) a trait is implemented for a composite type; and (6) a type alias defines a composite type. (B) Call/spec dependencies include: (7) a function/spec function calls another function/spec function in its body; and (8) a function/spec function references spec predicates or auxiliary definitions in requires/ensures/invariants.

Undocumented Verus Knowledge. As Verus is under active development, newly introduced features are often not immediately reflected in the documentation. To incorporate such knowledge into our knowledge base, we maintain a list of these features along with their corresponding pull requests, as developers typically describe new features in detail within the pull request. This process requires the involvement of a human verification expert to add new features with their pull request URLs and to remove entries once the documentation is updated.

#### 5 Evaluation

We evaluated KVerus in four crafted Verus benchmarks and two real-world Rust verification repositories and answered the following research questions (RQs):

RQ1. How effective is KVerus for single-file verification?

- RQ2. How effective is KVerus for repository-level verification under cross-file dependencies?
- RQ3. How does each type of knowledge contribute to KVerus's overall performance?

Beyond these core questions, we additionally evaluate practical dimensions including robustness against toolchain evolution and real-world integration in the Asterinas kernel.

Experiment Setup. All experiments were conducted on a server equipped with two Intel® Xeon® Gold 6230R CPUs (52 cores each, 2.10 GHz), 128 GB of RAM, and Ubuntu 24.04.1 LTS (64-bit). We configured KVerus to use the Claude Sonnet 4.0 [\[3\]](#page-11-14) model. The temperature parameter was fixed at 0.5 for all LLMs throughout the experiments. The maximum number of refinement queries was set to 10. Unless otherwise noted, we used Verus 20250813 with default settings. Each experiment was repeated three times, and we report the union of results across repetitions.

Comparison Tool. We compared KVerus with AutoVerus [\[37\]](#page-12-12) and AlphaVerus [\[2\]](#page-11-2). To ensure a fair comparison, we configured all tools to use the same underlying LLM, Claude Sonnet 4.0. Because AlphaVerus does not release its prompts [5](#page-6-2) , we developed a prompt for it. We also use Claude Sonnet 4.0 with 10 refinement queries as the baseline. Finally, SAFE [\[7\]](#page-11-3) was excluded from the comparison because it has not released its source code or models.

Dataset. We evaluated KVerus on four human-crafted benchmarks (Verus-Bench, MBPP, Human-Eval, and MathSpec-Bench) and two real-world verification works, Memory Allocator and CortenMM [\[38\]](#page-12-13). Verus-Bench was introduced by AutoVerus, whereas MBPP and Human-Eval were used by AlphaVerus. These three benchmarks consist of small, single-file verification tasks, where each target contains one or a few functions to be verified in isolation. We additionally introduce a new benchmark MathSpec-Bench[6](#page-6-3) , which is derived by translating developments of mathematical theories from Lean 4 into Verus and is designed to stress repository-level reasoning with extensive lemma invocations and cross-module dependencies. Finally, Memory Allocator and CortenMM provide a realistic end-to-end verification setting with non-trivial cross-file dependencies. In all experiments, we remove the existing proofs for the target functions while keeping shared lemmas intact, and require each tool to generate the missing proofs.

### <span id="page-6-1"></span>5.1 RQ1: Single-file Verification

In this section, we evaluated KVerus on three human-crafted singlefile benchmarks, Verus-Bench, MBPP, and Human-Eval.

<span id="page-6-3"></span><span id="page-6-2"></span><sup>5</sup>We requested the prompts from the AlphaVerus authors but did not receive a response. <sup>6</sup><https://github.com/rikosellic/verus-mathspec-bench>

<span id="page-7-0"></span>

| Benchmark   | #Task | KVerus  |           | AutoVerus |            | AlphaVerus |           | Baseline |           |
|-------------|-------|---------|-----------|-----------|------------|------------|-----------|----------|-----------|
|             |       | #Proved | Token     | #Proved   | Token      | #Proved    | Token     | #Proved  | Token     |
| Verus-Bench | 150   | 132     | 2,020,015 | 87        | 6,195,694  | 53         | 3,928,929 | 89       | 937,387   |
| MBPP        | 78    | 65      | 572,769   | 53        | 2,973,622  | 21         | 916,430   | 45       | 405,186   |
| Human-Eval  | 85    | 54      | 3,103,574 | 38        | 4,329,063  | 4          | 3,724,289 | 5        | 3,710,200 |
| SUM         | 313   | 251     | 5,696,358 | 178       | 13,498,379 | 78         | 8,569,648 | 139      | 5,052,773 |

Table 1: Proof success and token cost on single-file benchmarks.

<span id="page-7-1"></span>![](_page_7_Figure_4.jpeg)

Figure 2: Error types after the refinement.

Table 1 reports the number of proved tasks and token usage for KVerus, AutoVerus, AlphaVerus, and baseline method. KVerus successfully verified 251 of 313 tasks (80.2%) using 5,696,358 tokens, 1,912 LLM queries, and \$38.6, whereas AutoVerus verified 178 tasks (56.9%) with 13,498,379 tokens, 3,922 queries, and \$74.7, and AlphaVerus only verified 78 tasks (24.9%). The baseline method verified 44.4% of tasks but cost much less. Thus, KVerus achieved 23.3% more verified tasks while consuming only 43.2% of tokens and 48.8% of queries compared to AutoVerus. The advantage of KVerus is even more pronounced when compared with AlphaVerus and the baseline.

We categorize the remaining errors and report their absolute counts and relative proportions in Figure 2. In terms of total error count, KVERUS generates the lowest number of errors (155), representing a 40.1% reduction compared to AUTOVERUS (259) and a 38.9% reduction compared to the baseline (254). While verification errors constitute the primary failure mode for all evaluated tools, KVERUS reduces the absolute count of these errors to 103, whereas AUTOVERUS and AlphaVerus report 229 and 192 instances, respectively. Regarding syntax-level errors, the baseline shows a relative error rate of 48.8%, with *Type Mismatched* errors accounting for 30.7% (78) of its total errors. KVERUS reduces this specific error count to 15 (9.7%). Although AUTOVERUS reports the lowest syntax errors (30), its reliance on static prompting leads to errors in adapting to toolchain-specific requirements. Specifically,

AUTOVERUS generates 15 instances (5.8%) of *Decreases Missing* errors, while KVERUS eliminates this category entirely by leveraging its version-matched knowledge base. These results indicate that while KVERUS exhibits a higher relative proportion of syntax errors than AUTOVERUS, its knowledge-centric approach is more effective at minimizing the total error count and mitigating specific errors introduced by toolchain evolution.

We evaluate robustness to toolchain evolution by comparing KVERUS with the state-of-the-art AUTOVERUS across three Verus releases (20250328, 20250630, and 20250813). Table 2 presents the results. On the initial version (20250328), KVERUS verifies 254 tasks compared to 234 for AutoVerus, establishing an 8.5% performance lead. Release 20250630 introduced an undocumented internal regression that negatively affected both tools; however, KVERUS maintained a 16.0% lead over AutoVerus (217 vs. 187 verified tasks). The most significant divergence appears in release 20250813, which introduced a breaking requirement for explicit decreases clauses. Under this change, AutoVerus experienced a significant degradation, with the number of proved tasks dropping by 23.9% (from 234 to 178) compared to the initial version. In contrast, KVERUS remained highly stable, showing only a marginal 1.2% decline (from 254 to 251). Consequently, KVERUS's performance advantage over AutoVerus expanded to 41.0% in the latest release. This resilience is primarily attributable to KVERUS's ability to utilize version-matched Verus documentation during proof generation.

<span id="page-8-0"></span>Table 2: Evolution experiment on single-file benchmarks. K for KVERUS and A for AUTOVERUS.

| Benchmark    | 20250813  |     | 20250630 |     | 20250328  |     |
|--------------|-----------|-----|----------|-----|-----------|-----|
| 201011111111 | K         | A   | K        | A   | K         | Α   |
| Verus-Bench  | 132       | 87  | 108      | 90  | 130       | 129 |
| MBPP         | 65        | 53  | 67       | 57  | 70        | 62  |
| Human-Eval   | <b>54</b> | 38  | 42       | 40  | <b>54</b> | 43  |
| SUM          | 251       | 178 | 217      | 187 | 254       | 234 |

<span id="page-8-1"></span>Table 3: Per-task statistics comparison between the singlefile (Verus-Bench) and repository-level (CortenMM) benchmarks.

| Statistic | Verus-Bench | CortenMM |  |  |
|-----------|-------------|----------|--|--|
| Spec LoC  | 8           | 193      |  |  |
| Proof LoC | 10          | 195      |  |  |
| #Loop     | 1.6         | 0.02     |  |  |
| #Lemma    | 0.07        | 13.9     |  |  |

# 5.2 RQ2: Repository-level Verification under Cross-file Dependencies

In this section, we applied KVERUS to verify three repository-level benchmarks under cross-file dependencies: MathSpec-Bench, Memory Allocator, and CortenMM.

We compare between the single-file (Verus-Bench) and repositorylevel (CortenMM) benchmarks. As shown in Table 3, while Verus-Bench focuses on algorithmic patterns involving loops (1.6 per task), CortenMM represents a structural challenge with significantly larger specification and proof overhead (nearly 200 LoC). Crucially, CortenMM relies heavily on modular reasoning with 13.9 lemma invocations per task compared to only 0.07 in Verus-Bench, explaining the necessity for KVERUS's retrieval capabilities. Table 4 reports the number of proved tasks and token usage for KVerus and the baseline method. We do not include AutoVerus or AlphaVerus because they are designed for single-file verification and do not support repository-level verification across multiple modules and files. On MathSpec-Bench, KVERUS verifies 77.9% of tasks, whereas the baseline verifies only 9.6%. This drop is largely attributable to MathSpec-Bench's extensive use of lemma functions defined across multiple files and implemented in different traits. On the real-world benchmark CortenMM, KVERUS verifies 31.3% of tasks, while the baseline verifies only 3.0%. These results indicate that repository-scale verification remains challenging: our analysis suggests that performing retrieval and planning only once at the beginning of verification may fail to fetch all the dependent code and lemma functions required to complete a proof.

In addition, we further use KVERUS to complete previously unproven functions in CortenMM, the verified memory management module of the Asterinas kernel, and submit the generated proofs upstream. The changes are reviewed and accepted by the Asterinas

```
pub proof fn lemma_get_child_sound(nid: NodeId, offset: nat)
         Self::valid nid(nid).
         Self::nid_to_dep(nid) < 3,
        valid_pte_offset(offset),
        Self::valid_nid(Self::get_child(nid, offset)),
nid == Self::get_parent(Self::get_child(nid, offset)),
     let sz dep = level - 2:
10
     let sz_dep = ievel - 2,
let sz: nat = Self::tree_size_spec(sz_dep);
assert(offset * sz + 1 <= (offset + 1) * sz) by {
assert((offset + 1) * sz == offset * sz + sz) by {
12
13
           lemma_mul_is_distributive_add(sz, offset, 1);
14
15
      let child = Self::get_child(nid, offset);
17
      let trace = Self::lemma_nid_to_trace(nid);
      Self::lemma_trace_to_nid_increment(trace, offset);
19
      assert(Self::valid_trace((trace.push( offset)).drop_last()));
      assert(Self::nid_to_trace(child) == trace.push(offset)) by {
        Self::lemma_trace_to_nid_from_root(trace.push( offset));
     };
```

<span id="page-8-2"></span>Listing 4: lemma\_get\_child\_sound from CortenMM. We highlight the proof code generated by KVERUS.

developers. Overall, our evaluation shows that KVerus can automate proofs across three increasing levels of complexity. We next present representative case studies to illustrate these capabilities.

Mathematical properties of the tree model. The page table is modeled as a 4-level, full 512-ary tree, where each node represents a memory page. Each node is assigned a unique node ID via preorder traversal, and can also be represented by a trace—the sequence of offsets along the path from the root to the node. Structural notions such as ancestors, descendants, and subtrees are thus reduced to comparisons between IDs. Establishing this correspondence, however, requires non-trivial nonlinear arithmetic, which is beyond the direct capabilities of SMT solvers and remains challenging even for human reasoning. KVERUS handles this complexity by reusing existing lemmas about nonlinear arithmetic. For example, the get\_child function takes a node ID, derives its trace, appends a given offset, and maps it back to ID. In Listing 4, the associated lemma\_get\_child\_sound asserts two key facts: (i) the resulting ID lies within the valid range of node IDs (an arithmetic property, line 7), and (ii) its parent corresponds to the original node (a structural property, line 8). KVERUS proves the former by inserting assertions and invoking existing lemmas (line 14), and the latter by reasoning about sequences (lines 19-23).

Invariants of high-level system design. Moving up from arithmetic reasoning, Verus supports the verification of concurrent systems by encoding system designs as state machines. For example, Listing 5 illustrates the state machine of cursor operations in memory management, where a cursor locks a range of memory pages. The user specifies both the state fields and the transitions that manipulate them (lines 1-10). To ensure correctness, the user must also provide invariants that capture key system properties and prove that these invariants are preserved under all transitions. Such system-level reasoning is an advanced capability unique to Verus and remains beyond the scope of prior automation approaches. Despite the scarcity of examples of this Verus-specific technique, KVerus successfully learns its specialized syntax by parsing official

<span id="page-9-0"></span>

| Benchmark        | #Task |         | KVerus    | Baseline |           |  |
|------------------|-------|---------|-----------|----------|-----------|--|
|                  |       | #Proved | Token     | #Proved  | Token     |  |
| MathSpec-Bench   | 104   | 81      | 2,961,245 | 10       | 1,549,943 |  |
| Memory Allocator | 89    | 50      | 1,690,465 | 1        | 2,412,843 |  |
| CortenMM         | 166   | 52      | 5,041,957 | 5        | 4,890,698 |  |

Table 4: Proof success and token cost on repository-level benchmarks.

```
1 fields {
2 pub cpu_num: CpuId,
3 pub nodes: Map<NodeId, NodeState>,
4 pub cursors: Map<CpuId, CursorState>,
5 }
6
7 transition!{
8 // Update the CursorState on the given cpu
9 protocol_unlock_start(cpu: CpuId) { ... }
10 }
12 #[inductive(protocol_unlock_start)]
13 // The transition keeps invariants the wf_cursors and inv_non_overlapping
14 fn protocol_unlock_start_inductive(
15 pre: Self, post: Self, cpu: CpuId
16 ) {
17 assert(post.wf_cursors()) by {
18 assert forall |cpu_id: CpuId| #[trigger]
19 post.cursors.dom().contains(cpu_id) implies {
20 post.cursors[cpu_id].wf() && ...
21 } by {
22 // wf_cursors: only cursor on the given cpu changes
23 if cpu_id == cpu {
24 assert(pre.cursors[cpu_id] is Locked);
25 let rt = pre.cursors[cpu_id]->Locked_0;
26 assert(post.cursors[cpu_id] == CursorState::Locking(rt,
  ↩→ NodeHelper::next_outside_subtree(rt)));
27 assert(valid_cpu(post.cpu_num, cpu_id));
28 } else {
29 // Other CPUs unchanged
30 }
31 }
32 };
33
34 // inv_non_overlapping
35 ...
36 }
```

<span id="page-9-1"></span>Listing 5: protocol\_unlock\_start\_inductive and its dependent state fields and transition from CortenMM. We highlight the proof code generated by KVerus.

documentation and automates the proofs for 10 out of 15 transitions. Manual inspection reveals that the unprovable transitions are actually incorrect. Addressing such issues through specification generation or repair falls outside the scope of this work. We discuss this in [Section 6.1.](#page-10-0)

Functional correctness of executable code. At the implementation level, CortenMM employs bit-level manipulations in its executable code to boost performance, which are notoriously hard to verify. First, specifications are typically written with exponentials rather than bit-level operators, which eases reasoning but complicates alignment with the implementation. Second, these tricks depend on the precise coordination of multiple interdependent system parameters. Third, Verus delegates certain reasoning tasks to external solvers (e.g., bit\_vector, nonlinear\_arith), isolated from the surrounding proof context, requiring additional auxiliary assertions at the proof boundary—tedious and error-prone to maintain.

```
1 /// Verus specification
2 pub open spec fn page_size_spec<C: PagingConstsTrait>(level: PagingLevel)
  ↩→ -> usize
3 {
4 let base_page_bits = C::BASE_PAGE_SIZE().ilog2();
5 let pte_bits = C::PTE_SIZE().ilog2();
6 pow2((base_page_bits + (base_page_bits - pte_bits) * (level - 1)) as
  ↩→ nat) as usize
7 }
8
9 /// Verified code
10 pub fn page_size<C: PagingConstsTrait>(level: PagingLevel) -> (res: usize)
11 requires
12 1 <= level <= C::NR_LEVELS(),
13 ensures
14 res > 0,
15 is_power_2(res as int),
16 res == page_size_spec::<C>(level),
17 {
18 proof {
19 C::lemma_consts_properties();
20 C::lemma_consts_properties_derived();
21 let subpage_bits = nr_subpage_per_huge::<C>().ilog2();
22 assert(C::BASE_PAGE_SIZE() * pow2(subpage_bits * (level - 1)) <=
  ↩→ usize::MAX) by {
23 assert(subpage_bits * (level - 1) <= subpage_bits * C::NR_LEVELS())
24 by (nonlinear_arith)
25 requires
26 1 <= level <= C::NR_LEVELS(),
27 0 < nr_subpage_per_huge::<C>(),
28 ;
29 };
30 lemma_usize_shl_is_mul(C::BASE_PAGE_SIZE(),subpage_bits*(level-1));
31 }
32 /// Source code
33 C::BASE_PAGE_SIZE() << (nr_subpage_per_huge::<C>().ilog2() * (level -
  ↩→ 1))
34 }
```

<span id="page-9-2"></span>Listing 6: page\_size and its specification from CortenMM. We highlight the proof generated by KVerus.

[Listing 6](#page-9-2) shows the page\_size function, which returns the size of a memory page at a given level. Here C: PagingConstsTrait provides constants for memory management. Despite its straightforward design, verifying this function is nontrivial due to the interplay of overflow restrictions (line 22), trait and function dependencies (lines 19-20), external solver queries (lines 24-27), and bit operating lemmas (lines 30), all of which KVerus discharges automatically.

Overall results. KVerus generated 1,387 lines of proof code, including 6 newly introduced lemma functions, to formally verify 23 functions that were previously unverified. This newly generated code accounts for 21.0% of the total proof code. All generated proof code has been reviewed and accepted by the Asterinas developers. We also compare and discuss the differences between proof code generated by KVerus and that written by human experts in [Section 6.3.](#page-10-1)

## 5.3 RQ3: Ablation Study

This section evaluates the contribution of three types of knowledge in KVerus for proof code generation by disabling code metadata knowledge (w/o Code), lemma knowledge (w/o Lemma), and Verus knowledge (w/o Verus).

[Table 5](#page-11-15) summarizes the ablation results in terms of proof success and token cost. On the three single-file benchmarks (Verus-Bench, MBPP, and Human-Eval), removing Verus knowledge leads to the largest degradation in proof success (e.g., 54→4 on Human-Eval), indicating that version-aligned Verus documentation is crucial for handling Verus-specific syntax and proof obligations. In contrast, disabling code metadata or lemma knowledge has only marginal impact on these single-file tasks, with success changing by at most a few tasks. The trend reverses on the repository-level targets (MathSpec-Bench and CortenMM), where cross-file dependency resolution becomes the bottleneck: removing code metadata knowledge causes the largest drop in success (81→42 on MathSpec-Bench and 52→10 on CortenMM) and substantially increases token consumption, while removing lemma knowledge also yields notable degradations (81→63 and 52→7, respectively). Removing Verus knowledge in repository-level settings has a smaller but still measurable effect (81→75 and 52→22), suggesting that in-repo context can partially compensate for missing documentation, whereas structural knowledge remains the primary driver at repository scale. Overall, these results show that Verus knowledge primarily improves robustness in single-file verification, while code metadata and lemma knowledge are essential for scaling to repository-level verification under cross-file dependencies.

#### 6 Discussion

#### <span id="page-10-0"></span>6.1 Ensuring Specification Correctness

Like most proof generation tools, KVerus assumes that formal specifications—such as preconditions and postconditions—are correct and well-defined. While this assumption often holds for crafted benchmarks, real-world verification frequently breaks it. Incorrect specifications not only block proof generation but can also conceal critical bugs, undermining verification as a whole.

We argue that proof generation tools should evolve from passive consumers of specifications into active participants in their validation. Future work could leverage LLMs to detect inconsistencies between implementations, natural language comments, and formal specifications, and use repeated proof failures as heuristics to flag potentially flawed or infeasible specifications. This transforms proof generation from a simple pass/fail activity into an interactive process, creating a virtuous cycle where automated tools and human engineers collaborate to refine both the code and its specification.

#### 6.2 Reducing Dependence on Frontier LLMs

Our experiments indicate that the performance of KVerus depends heavily on advanced models like Claude 4.0, due to the limited public corpora for formal verification languages such as Verus [\(Table 1\)](#page-7-0). This strong reliance on frontier models highlights the challenge of balancing model capability with accessibility and reproducibility.

The principal contribution of KVerus lies in its systematic framework for organizing and presenting the syntax, semantics, and

domain knowledge of a formal language and project to an LLM. This structured approach facilitates more effective proof generation and, in principle, can be applied across different models, providing model-agnostic value beyond any single LLM. However, reliance on closed-source models limits reproducibility and broad accessibility. Future work could mitigate this through domain-specific fine-tuning, training smaller open-source models on curated formal methods corpora to cultivate specialized expertise. Reducing model dependency in this manner enhances reproducibility and broadens the applicability of automated proof generation.

#### <span id="page-10-1"></span>6.3 Generated vs. Human Proof Code

During the verification of CortenMM, we observed systematic differences between KVerus-generated proof code and proofs written by human experts. In particular, KVerus tends to discharge proof obligations using a more conservative, step-by-step style, whereas human experts more aggressively rely on the automated reasoning power of Verus's underlying SMT solver to keep proofs compact. We quantitatively compare generated and human-written proofs on the same targets. In a representative case with 7 specification clauses, the human proof consists of 34 lines across 2 proof blocks, while KVerus produces over 100 lines across 7 blocks, with more intermediate proof steps (#assert: 8 vs. 51; #lemma calls: 1 vs. 4). We further prototyped a simple proof-minimization pass that iteratively removes assert statements and re-runs verification after each removal, keeping the deletion only when the proof still verifies. Across the 23 newly verified CortenMM functions, this postprocessing reduces proof-code size by about 10% in LoC without changing verification outcomes, indicating that a non-trivial fraction of generated assertions are redundant given the SMT solver's reasoning power.

These observations highlight a current limitation of LLM-based synthesis: models typically lack an explicit cost model of SMT reasoning and therefore introduce additional assertions or helper invocations to reduce local uncertainty. Enabling solver-aware proof synthesis (e.g., using verifier/solver feedback to guide proof minimization while preserving verification success) is an important direction for future work.

### 7 Related Work

Automated Formal Verification for Rust. LLM-driven formal verification in Rust is an emerging area, with Verus as the primary framework. AutoVerus [\[37\]](#page-12-12) pioneered this space by using handcrafted prompts to mimic expert strategies on its Verus-Bench dataset. However, its context-unaware design, which relies on heuristics for common algorithms, does not generalize to complex, real-world software. Subsequent tools, SAFE [\[7\]](#page-11-3) and AlphaVerus [\[2\]](#page-11-2), introduce more sophisticated refinement phases. SAFE uses extensive GPT-4o generation to fine-tune a local model, while AlphaVerus employs a tree search guided by verifier feedback. While effective in constrained settings, these refinement-heavy strategies do not fundamentally address the Semantic-Structural Gap. Their search spaces become intractable in multi-module systems, and they lack resilience against toolchain evolution. KVerus departs from this by using a knowledge-centric architecture for robust, context-aware generation, avoiding both costly fine-tuning and intractable search.

<span id="page-11-15"></span>

| Benchmark        | #Task | KVerus  |           | w/o Code |           | w/o Lemma |           | w/o Verus |           |
|------------------|-------|---------|-----------|----------|-----------|-----------|-----------|-----------|-----------|
|                  |       | #Proved | Token     | #Proved  | Token     | #Proved   | Token     | #Proved   | Token     |
| Verus-Bench      | 150   | 110     | 2,020,015 | 110      | 2,018,914 | 108       | 1,822,615 | 88        | 2,382,647 |
| MBPP             | 78    | 65      | 572,769   | 66       | 574,365   | 64        | 518,769   | 46        | 445,704   |
| Human-Eval       | 85    | 54      | 3,103,574 | 53       | 3,114,245 | 50        | 2,700,285 | 4         | 4,081,220 |
| MathSpec-Bench   | 104   | 81      | 2,961,245 | 42       | 4,078,659 | 63        | 3,382,908 | 75        | 3,182,948 |
| Memory Allocator | 89    | 50      | 1,690,465 | 50       | 1,686,263 | 51        | 1,525,269 | 2         | 2,615,484 |
| CortenMM         | 166   | 52      | 5,041,957 | 10       | 7,058,740 | 7         | 6,655,383 | 22        | 5,798,251 |

Table 5: Proof success and token cost for the ablation study.

Beyond these, domain-specific tools like OwlC [\[29\]](#page-12-23) can automatically generate Rust code with Verus proofs from high-level security protocol specifications, but they do not target general-purpose verification.

Proof Generation for Software Verification. These challenges of context and evolution are not unique to Rust, but reflect broader issues in applying LLMs to software verification, particularly for deductive program verifiers like Verus and Dafny [\[19\]](#page-12-8). These differ from interactive theorem provers (ITPs) such as Coq [\[32\]](#page-12-4), Isabelle [\[27\]](#page-12-3), and Lean [\[25\]](#page-12-2). ITPs maintain explicit proof states that LLMs can manipulate step-by-step via tactic prediction, aided by the relatively large pre-training corpora available for these mature tools. Tools like Rango [\[34\]](#page-12-11) leverage this structure, using retrieval augmentation to find similar proof scripts and states to guide tactic prediction in Rocq. In contrast, KVerus is designed for the unique challenges of deductive verifiers where such explicit proof states are absent. It bridges the Semantic-Structural Gap not by predicting low-level tactics, but by building a rich, high-level knowledge base. Its self-adaptive design, particularly its automatically updated toolchain knowledge, provides the resilience to evolution that retrieval-only methods lack. A closer comparison is Dafny, another deductive verification language. LAUREL [\[26\]](#page-12-24) improves proof synthesis by localizing where assertions are needed and retrieving syntactically similar proofs to guide the LLM. While innovative, its reliance on syntactic similarity and its focus on single-file contexts mean that real-world challenges like complex inter-module dependencies remain unaddressed. KVerus is therefore distinguished as the first system designed with a knowledge-centric, self-adaptive architecture to explicitly target the structural complexity and evolutionary nature of modern software.

#### 8 Conclusion

In this paper, we addressed the dual challenges of structural complexity and continuous evolution in formal verification for largescale software. We identified the Semantic-Structural Gap as the fundamental reason why current LLM-based approaches are brittle, failing to adapt to repository-level codebases and evolving toolchains. To bridge this gap, we designed and implemented KVerus, a novel self-adaptive system that evolves with its environment by combining dependency-aware analysis with error-driven self-refinement. Our extensive evaluation demonstrates that KVerus significantly outperforms state-of-the-art methods in accuracy, cost-efficiency, and robustness, proving its practical utility by successfully verifying

complex modules in the Asterinas Rust OS kernel and contributing to the Verus standard library. Ultimately, this work marks a pivotal shift from static, one-shot proof generation to a paradigm of continuous, adaptive verification, laying the foundation for making formal methods a sustainable practice for modern, security-critical systems.

#### References

- <span id="page-11-7"></span>[1] Verify Rust Standard Library Effort, 2024. [https://model-checking.github.io/](https://model-checking.github.io/verify-rust-std) [verify-rust-std.](https://model-checking.github.io/verify-rust-std)
- <span id="page-11-2"></span>[2] Pranjal Aggarwal, Bryan Parno, and Sean Welleck. Alphaverus: Bootstrapping formally verified code generation through self-improving translation and treefinement. In Forty-second International Conference on Machine Learning (ICML 2025), 2025.
- <span id="page-11-14"></span>[3] Anthropic. Claude Sonnet 4, 2025. [https://www.anthropic.com/news/claude-4.](https://www.anthropic.com/news/claude-4)
- <span id="page-11-4"></span>[4] Vytautas Astrauskas, Aurel Bíly, Jonáš Fiala, Zachary Grannan, Christoph Math- ` eja, Peter Müller, Federico Poli, and Alexander J Summers. The prusti project: Formal verification for rust. In NASA Formal Methods Symposium, pages 88–108. Springer, 2022.
- <span id="page-11-1"></span>[5] Yves Bertot and Pierre Castéran. Interactive theorem proving and program development: Coq'Art: the calculus of inductive constructions. Springer Science & Business Media, 2013.
- <span id="page-11-13"></span>[6] Harrison Chase. LangChain, October 2022. [https://github.com/langchain-ai/](https://github.com/langchain-ai/langchain) [langchain.](https://github.com/langchain-ai/langchain)
- <span id="page-11-3"></span>[7] Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Hao Yu, Nan Duan, Peng Cheng, et al. Automated proof generation for rust code via self-evolution. In The Thirteenth International Conference on Learning Representations (ICLR 25), 2025.
- <span id="page-11-12"></span>[8] Xiangdong Chen, Zhaofeng Li, Jerry Zhang, Vikram Narayanan, and Anton Burtsev. Atmosphere: Practical verified kernels with rust and verus. SOSP '25, page 752–767, New York, NY, USA, 2025. Association for Computing Machinery.
- <span id="page-11-11"></span>[9] Leonardo De Moura and Nikolaj Bjørner. Z3: An efficient smt solver. In International conference on Tools and Algorithms for the Construction and Analysis of Systems, pages 337–340. Springer, 2008.
- <span id="page-11-5"></span>[10] Xavier Denis, Jacques-Henri Jourdan, and Claude Marché. Creusot: A foundry for the deductive verification of rust programs. In International Conference on Formal Engineering Methods, pages 90–105. Springer, 2022.
- <span id="page-11-0"></span>[11] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan Newman Wu, Jieung Kim, Vilhelm Sjöberg, and David Costanzo. CertiKOS: An extensible architecture for building certified concurrent OS kernels. In 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16), pages 653–669, 2016.
- <span id="page-11-8"></span>[12] Travis Hance, Jon Howell, Oded Padon, and Bryan Parno. Leaf: Modularity for temporary sharing in separation logic. Proceedings of the ACM on Programming Languages, 7(OOPSLA2):31–58, 2023.
- <span id="page-11-9"></span>[13] Travis Hance, Yi Zhou, Andrea Lattuada, Reto Achermann, Alex Conway, Ryan Stutsman, Gerd Zellweger, Chris Hawblitzel, Jon Howell, and Bryan Parno. Sharding the state machine: Automated modular reasoning for complex concurrent systems. In 17th USENIX Symposium on Operating Systems Design and Implementation (OSDI 23), pages 911–929, 2023.
- <span id="page-11-6"></span>[14] Ralf Jung, Benjamin Kimock, Christian Poveda, Eduardo Sánchez Muñoz, Oli Scherer, and Qian Wang. Miri: Practical undefined behavior detection for rust. Proc. ACM Program. Lang., 10(POPL), January 2026.
- <span id="page-11-10"></span>[15] Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. Iris: Monoids and invariants as an orthogonal basis for concurrent reasoning. ACM SIGPLAN Notices, 50(1):637–650, 2015.

- <span id="page-12-0"></span>[16] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt, Rafal Kolanski, Michael Norrish, et al. seL4: Formal verification of an OS kernel. In Proceedings of the ACM SIGOPS 22nd symposium on Operating systems principles, pages 207–220, 2009.
- <span id="page-12-6"></span>[17] Andrea Lattuada, Travis Hance, Jay Bosamiya, Matthias Brun, Chanhee Cho, Hayley LeBlanc, Pranav Srinivasan, Reto Achermann, Tej Chajed, Chris Hawblitzel, et al. Verus: A practical foundation for systems verification. In Proceedings of the ACM SIGOPS 30th Symposium on Operating Systems Principles, pages 438–454, 2024.
- <span id="page-12-7"></span>[18] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel. Verus: Verifying rust programs using linear ghost types. Proceedings of the ACM on Programming Languages, 7(OOPSLA1):286–315, 2023.
- <span id="page-12-8"></span>[19] K Rustan M Leino. Dafny: An automatic program verifier for functional correctness. In International conference on logic for programming artificial intelligence and reasoning, pages 348–370. Springer, 2010.
- <span id="page-12-21"></span>[20] K Rustan M Leino and Clément Pit-Claudel. Trigger selection strategies to stabilize program verifiers. In International Conference on Computer Aided Verification, pages 361–381. Springer, 2016.
- <span id="page-12-1"></span>[21] Xavier Leroy, Sandrine Blazy, Daniel Kästner, Bernhard Schommer, Markus Pister, and Christian Ferdinand. Compcert-a formally verified optimizing compiler. In ERTS 2016: Embedded Real Time Software and Systems, 8th European Congress, 2016.
- <span id="page-12-18"></span>[22] Jialin Li, Andrea Lattuada, Yi Zhou, Jonathan Cameron, Jon Howell, Bryan Parno, and Chris Hawblitzel. Linear types for large-scale systems verification. Proceedings of the ACM on Programming Languages, 6(OOPSLA1):1–28, 2022.
- <span id="page-12-9"></span>[23] Minghai Lu, Benjamin Delaware, and Tianyi Zhang. Proof automation with large language models. In Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering, pages 1509–1520, 2024.
- <span id="page-12-10"></span>[24] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. Specgen: Automated generation of formal program specifications via large language models. In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE), pages 16–28. IEEE, 2025.
- <span id="page-12-2"></span>[25] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language. In International Conference on Automated Deduction, pages 625–635. Springer, 2021.
- <span id="page-12-24"></span>[26] Eric Mugnier, Emmanuel Anaya Gonzalez, Nadia Polikarpova, Ranjit Jhala, and Zhou Yuanyuan. Laurel: Unblocking automated verification with large language models. Proceedings of the ACM on Programming Languages, 9(OOPSLA1):1519– 1545, 2025.
- <span id="page-12-3"></span>[27] Tobias Nipkow, Markus Wenzel, and Lawrence C Paulson. Isabelle/HOL: a proof assistant for higher-order logic. Springer, 2002.
- <span id="page-12-14"></span>[28] Yuke Peng, Hongliang Tian, Zhang Junyang, Ruihan Li, Chengjun Chen, Jianfeng Jiang, Jinyi Xian, Xiaolin Wang, Chenren Xu, Diyu Zhou, et al. Asterinas: A Linux ABI-Compatible, Rust-Based Framekernel OS with a Small and Sound TCB. In 2025 USENIX Annual Technical Conference (USENIX ATC 25), 2025.
- <span id="page-12-23"></span>[29] Pratap Singh, Joshua Gancher, and Bryan Parno. Owlc: Compiling security protocols to verified, secure, high-performance libraries. Cryptology ePrint Archive, 2025.
- <span id="page-12-19"></span>[30] Xudong Sun, Wenjie Ma, Jiawei Tyler Gu, Zicheng Ma, Tej Chajed, Jon Howell, Andrea Lattuada, Oded Padon, Lalith Suresh, Adriana Szekeres, et al. Anvil: Verifying liveness of cluster management controllers. In 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24), pages 649–666, 2024.
- <span id="page-12-17"></span>[31] MIRAI Developement Team. Mirai: an abstract interpreter for the rust compiler's mid-level intermediate representation (mir)., 2025. [https://github.com/endorlabs/](https://github.com/endorlabs/MIRAI) [MIRAI.](https://github.com/endorlabs/MIRAI)
- <span id="page-12-4"></span>[32] The Rocq Development Team. The rocq proof assistant v9.1.0, 2025. [https://rocq](https://rocq-prover.org)[prover.org.](https://rocq-prover.org)
- <span id="page-12-22"></span>[33] The Verus Developement Team. A verus compiler front-end for ides, 2026. [https://github.com/verus-lang/verus-analyzer.](https://github.com/verus-lang/verus-analyzer)
- <span id="page-12-11"></span>[34] Kyle Thompson, Nuno Saavedra, Pedro Carrott, Kevin Fisher, Alex Sanchez-Stern, Yuriy Brun, João F Ferreira, Sorin Lerner, and Emily First. Rango: Adaptive retrieval-augmented proving for automated software verification. In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE), pages 347–359. IEEE, 2025.
- <span id="page-12-15"></span>[35] Alexa VanHattum, Daniel Schwartz-Narbonne, Nathan Chong, and Adrian Sampson. Verifying dynamic trait objects in rust. In Proceedings of the 44th International Conference on Software Engineering: Software Engineering in Practice, pages 321– 330, 2022.
- <span id="page-12-16"></span>[36] Minghua Wang, Jingling Xue, Lin Huang, Yuan Zi, and Tao Wei. Unsafecop: Towards memory safety for real-world unsafe rust co de with p ractical bounded model checking. In International Symposium on Formal Methods, pages 307–324. Springer, 2024.
- <span id="page-12-12"></span>[37] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui, Yeyun Gong, Chris Hawblitzel, Shuvendu Lahiri, Jacob R Lorch, Shuai Lu, et al. Autoverus: Automated proof generation for rust code. Proceedings of the ACM on Programming Languages, 9(OOPSLA2):3454–3482, 2025.

- <span id="page-12-13"></span>[38] Junyang Zhang, Xiangcan Xu, Yonghao Zou, Zhe Tang, Xinyi Wan, Kang Hu, Siyuan Wang, Wenbo Xu, Di Wang, Hao Chen, Hongliang Tian, Lin Huang, Shoumeng Yan, Yuval Tamir, Yingwei Luo, Xiaolin Wang, Huashan Yu, Zhenlin Wang, and Diyu Zhou. CortenMM: Efficient Memory Management with Strong Correctness Guarantees. In Proceedings of the ACM SIGOPS 31th Symposium on Operating Systems Principles, 2025.
- <span id="page-12-5"></span>[39] Litao Zhou, Jianxing Qin, Qinshi Wang, Andrew W Appel, and Qinxiang Cao. Vst-a: A foundationally sound annotation verifier. Proceedings of the ACM on Programming Languages (POPL), 8:2069–2098, 2024.
- <span id="page-12-20"></span>[40] Ziqiao Zhou, Weiteng Chen, Sishuai Gong, Chris Hawblitzel, Weidong Cui, et al. VeriSMo: A verified security module for confidential VMs. In 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24), pages 599–614, 2024.

## A Proof Failures Caused by Incorrect Specifications

While verifying the state machine of Asterinas' RCU (Read-Copy-Update, a synchronization mechanism widely used in concurrent programming and operating systems), we aimed to prove that the transition shown in [Listing 7](#page-12-25) preserves all invariants of the state machine.

This transition specifies the behavior of protocol\_ lock\_skip, which updates the cursor state during the process of locking while skipping a node nid and its entire subtree. Because the parent node's PTE is void, the current node does not exist in the page table, implying that nid and all its descendants are unallocated. Consequently, the algorithm can skip directly to the next node outside the nid subtree and continue locking. Conceptually, this operation logically locks the entire subtree rooted at nid in a single step. The transition is designed to enforce the following properties:

- (1) Cursor state update: After skipping node nid, the CPU's CursorState changes from Locking(rt, nid) to Locking(rt, NodeHelper::next\_outside\_subtree( nid)).
- (2) PTE validation: Before skipping nid, its parent node's page table entry at the specified offset must be empty (pte\_array. is\_void(offset)).
- (3) Cursor consistency: Removing CursorState requires that \_nid == nid, ensuring the node matches the given parameter.

```
1 transition!{
2 protocol_lock_skip(cpu: CpuId, nid: NodeId) {
3 require(valid_cpu(pre.cpu_num, cpu));
4 require(NodeHelper::valid_nid(nid));
5 require(nid != NodeHelper::root_id());
6 remove cursors -=
7 [ cpu => let CursorState::Locking(rt, _nid) ];
8 require(_nid == nid);
9 require(NodeHelper::in_subtree_range(rt, nid));
10 let pa = NodeHelper::get_parent(nid);
11 let offset = NodeHelper::get_offset(nid);
12 require(nid != rt);
13 have pte_arrays >= [ pa => let pte_array ];
14 require(pte_array.is_void(offset));
15 add cursors += [ cpu => CursorState::Locking(
16 rt, NodeHelper::next_outside_subtree(nid)
17 ) ];
18 }
19 }
```

<span id="page-12-25"></span>Listing 7: Proof failure due to incorrect specification of protocol\_lock\_skip. We highlight the corrected lines added by human expert.

```
1 #[inductive(initialize)]
2 fn initialize_inductive(post: Self, cpu_num: CpuId) {
3 assert(post.wf_nodes()) by {
4 assert(forall|nid: NodeId|post.nodes.dom().contains(nid)
5 ==> #[trigger] NodeHelper::valid_nid(nid)) by {
6 NodeHelper::lemma_root_id();
7 }
8 }
9
10 assert forall |nid: NodeId| NodeHelper::valid_nid(nid)
11 && nid != NodeHelper::root_id()
12 implies {
13 let pa = NodeHelper::get_parent(nid);
14 let offset = NodeHelper::get_offset(nid);
15 !(post.pte_arrays.dom().contains(pa)
16 && post.pte_arrays[pa].is_alive(offset))
17 } by {
18 let pa = NodeHelper::get_parent(nid);
19 let offset = NodeHelper::get_offset(nid);
20 if pa == NodeHelper::root_id() {
21 NodeHelper::lemma_get_offset_sound(nid);
22 } else {
23 assert(!post.pte_arrays.dom().contains(pa));
24 }
25 }
26
27 assert forall |nid: NodeId|
28 #[trigger] NodeHelper::valid_nid(nid)
29 && nid != NodeHelper::root_id()
30 implies {
31 post.strays_filter(nid)
32 .kv_pairs()
33 .filter(|pair: ((NodeId, Paddr), bool)| pair.1 == false)
34 .len() <= 1
35 } by {
36 assert(post.strays_filter(nid).dom()
37 == Set::<(NodeId, Paddr)>::empty());
38 assert(post.strays_filter(nid).kv_pairs()
39 == Set::<((NodeId, Paddr), bool)>::empty());
40 let filtered = post.strays_filter(nid)
41 .kv_pairs()
42 .filter(|pair: ((NodeId, Paddr), bool)| pair.1 == false);
43 assert(filtered==Set::<((NodeId, Paddr), bool)>::empty());
44 }
45 }
```

<span id="page-13-2"></span>Listing 8: Proof code for initialize\_inductive written by human expert.

(4) Parent-child relationship correctness: NodeHelper::get \_parent(nid) and NodeHelper::get\_offset(nid) determine the parent and offset of nid.

Together, these properties are intended to guarantee the correctness and consistency of the locking process when skipping nodes.

However, this specification omits crucial conditions required for soundness, leading to proof failures:

- (1) Cursor range restriction: A cursor may only lock a subtree rooted at rt, and Locking(rt, node) excludes locking the final node. Thus, the state where node == next\_outside\_subtree(rt) (the first node beyond the rt subtree) is valid, indicating that the subtree is fully locked. Applying protocol\_lock\_skip in this state is invalid, as it moves the cursor beyond the rt subtree boundary, violating the wf\_cursor constraint.
- (2) Missing constraint nid != rt: If nid == rt, the procedure attempts to access the root node's parent, leading to an invalid system state.

Therefore, the specification in [Listing 7](#page-12-25) must be refined with the highlighted lines to ensure soundness.

```
1 #[inductive(initialize)]
2 fn initialize_inductive(post: Self, cpu_num: CpuId) {
3 // wf_nodes: Only root node exists, and root is valid
4 assert(post.wf_nodes()) by {
5 assert forall |nid: NodeId| #[trigger]
6 post.nodes.dom().contains(nid) implies
7 NodeHelper::valid_nid(nid) by {
8 assert(post.nodes.dom()==set![NodeHelper::root_id()]);
9 if post.nodes.dom().contains(nid) {
10 assert(nid == NodeHelper::root_id());
11 assert(NodeHelper::valid_nid(NodeHelper::root_id()))
12 by {
13 NodeHelper::lemma_root_id();
14 }
15 }
16 }
17 };
18
19 // wf_strays: Empty map trivially satisfies this
20 assert(post.wf_strays()) by {
21 assert(post.strays.dom().is_empty());
22 };
24 // inv_pt_node_pte_array_relationship: Contain only root
25 assert(post.inv_pt_node_pte_array_relationship()) by {
26 assert forall |nid: NodeId| post.nodes.dom().contains(nid)
27 <==> post.pte_arrays.dom().contains(nid) by {
28 assert(post.nodes.dom()==set![NodeHelper::root_id()]);
29 assert(post.pte_arrays.dom()==set![NodeHelper::root_id()]);
30 }
31 };
32
33 // inv_pt_node_pte_relationship: No non-root nodes exist
34 /* 35 lines of proof code here*/
35
36 // inv_non_overlapping: No cursors are in Locked state
37 /* 20 lines of proof code here*/
38
39 // inv_stray_at_most_one_false_per_node: Empty strays map
40 /* 15 lines of proof code here*/
41
42 // inv_pte_is_alive_implies_stray_has_false: No alive PTEs
43 /* 23 lines of proof code here*/
44 }
```

<span id="page-13-1"></span>Listing 9: Simplified proof code for initialize\_inductive generated by KVerus.

### B Differences between Generated and Human-Written Proof Code

[Listing 9](#page-13-1) and [Listing 8](#page-13-2) present the proof code generated by KVerus and written by a human expert. The human expert implemented 34 lines of proof code across 2 code blocks, whereas KVerus generated over 100 lines of proof code spread across 7 code blocks, corresponding to the 7 specifications.